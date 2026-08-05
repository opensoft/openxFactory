"""The (repository, ref) SNAPSHOT REGISTRY and the serving-side data-source seam
(openxFactory change `add-dashboard-repo-selector`, tasks 2.1-2.3 and 3.3/3.4).

ONE registry, keyed on the PAIR (repository, ref), with `ref` DEFAULTING to
`main` (design D4). Every renderer route, the snapshot index, and both refresh
bindings address snapshots through this registry — there is no second path
convention anywhere in the serving layer. The served plane only ever exercises
`(repository, main)`; the ref key is carried from day one so the branch-session
and runtime-plane consumers bind to this seam instead of forcing it to be
re-cut.

WHAT AN ENTRY IS. One available snapshot plus the facts a viewer needs to trust
it: its repository and ref, the `source_revision` it projects, the
revision-derived `generated_at`, its ORIGIN, and — separately — the source ROOT
that entry's read-only `/source/` pass-through is confined to:

    local    generated on this host from a checkout (the local plane)
    fetched  pulled at runtime from the declared data source (the served plane)
    baked    shipped inside the image — a FIRST-BOOT and OFFLINE fallback ONLY
             (design D6), and never rendered silently: a baked entry is `stale`
             and carries the reason, which the renderer must show.

PER-ENTRY CONFINEMENT (task 2.2). `resolve_source` extends the single-root
containment check to a root PER ENTRY: reading a document through a
(repository, ref) entry cannot escape THAT entry's root, and an entry with no
declared root serves no documents at all (fail-closed) rather than falling back
to somebody else's checkout.

PUBLICATION REFUSAL (task 2.3). `assert_publishable` refuses any non-`main`
snapshot and any index containing one. Non-`main` snapshots are session-local
derived data: never published, never in the index the served plane fetches,
never shared state. The rule lands here, before
`add-workbench-branch-sessions` exists, so that change cannot accidentally
publish a worktree projection.

THE DATA SOURCE IS CONFIGURATION, NOT CONTRACT (design D5 + open question 1).
`DirectoryDataSource` reads a published tree from the filesystem;
`UrlDataSource` reads it over HTTP(S) from the SERVING side. Which one the
hosted plane uses (aggregation-repo raw files, a blob container, a ConfigMap) is
Brett's ratification, and swapping it changes a fetcher and no contract. Two
deliberate properties:

  * the fetch is SERVER-SIDE, so the browser bundle keeps its grep-proven
    same-origin boundary (`tests/ideation-dashboard/test_renderer.py`), and any
    read credential stays where credentials belong; and
  * the derived cache is IN-PROCESS (fetched bytes live on the entry, not on
    disk), so the served plane needs no writable path and a refresh writes
    nothing at all. The only write any refresh binding performs is the LOCAL
    regenerate's derived snapshot file, through the interactivity boundary.

No credential is hardcoded and none is read from a repository: `UrlDataSource`
takes a bearer token only from a named environment variable supplied by the
operator (`--data-source-token-env`), so the production source choice and its
credential remain a deployment decision.
"""

from __future__ import annotations

import contextlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

DEFAULT_REF = "main"
INDEX_KIND = "ideation-dashboard-snapshot-index"
INDEX_SCHEMA_VERSION = 1
DEFAULT_INDEX_NAME = "index.json"
# Where the publication lane writes, and therefore where the RULED hosted data
# source reads from (Brett, 2026-07-26, open question 1: the aggregation repo's
# raw files — the lane already writes exactly here, so no publication path is
# invented and the fetched file's commit SHA IS the snapshot's source_revision).
DEFAULT_PUBLISH_PATH = "health/ideation-dashboard"
GITHUB_RAW_HOST = "raw.githubusercontent.com"
# Server-side index-peek cache. The PASSIVE FRESHNESS HINT (Brett, 2026-07-26,
# open question 2) has the page poll the thin index every few minutes; the
# serving side answers those polls from this short-lived peek so N viewers cost
# the data source at most one index read per TTL. The index is thin BY DESIGN
# (D3) precisely so this is cheap.
PEEK_TTL_SECONDS = 60

ORIGIN_LOCAL = "local"
ORIGIN_FETCHED = "fetched"
ORIGIN_BAKED = "baked"

# The refresh bindings (design D7). `refetch` is the served plane's read-only
# re-pull; `regenerate` is the local plane's derived-artifact regeneration.
BINDING_REFETCH = "refetch"
BINDING_REGENERATE = "regenerate"

_FETCH_TIMEOUT_SECONDS = 15
_MAX_FETCH_BYTES = 32 * 1024 * 1024  # a snapshot is ~MBs; refuse a runaway body


class PublicationRefused(Exception):
    """A non-`main` snapshot (or an index carrying one) was offered for
    publication — session-local derived data is never shared state (task 2.3)."""


class DataSourceError(Exception):
    """The declared data source could not be read. Never fatal on the serving
    side: it degrades to the baked fallback with a stale banner (D6)."""


# --------------------------- keys ---------------------------

def normalize_ref(ref: str | None) -> str:
    """`ref` defaults to `main` (D4): None, empty, or whitespace all mean the
    shared truth every existing caller already means."""
    if ref is None:
        return DEFAULT_REF
    text = str(ref).strip()
    return text or DEFAULT_REF


def snapshot_key(repository: str, ref: str | None = None) -> tuple[str, str]:
    """The registry key. A ref-less request resolves to `(repository, 'main')`,
    which is why every pre-existing consumer keeps working unchanged."""
    return (str(repository), normalize_ref(ref))


def key_id(repository: str, ref: str | None = None) -> str:
    """The wire/DOM form of a key — `repository@ref`. Used by the keyed
    `/source/` prefix and by the selector's option values."""
    repo, ref_name = snapshot_key(repository, ref)
    return f"{repo}@{ref_name}"


def parse_key_id(text: str) -> tuple[str, str] | None:
    """Inverse of `key_id`; None when the text is not a key form. The registry
    still decides whether the parsed pair EXISTS — parsing is not admission."""
    if not text or "@" not in text:
        return None
    repo, _, ref = text.rpartition("@")
    if not repo:
        return None
    return snapshot_key(urllib.parse.unquote(repo), urllib.parse.unquote(ref))


def is_publishable_ref(ref: str | None) -> bool:
    return normalize_ref(ref) == DEFAULT_REF


def assert_publishable(repository: str, ref: str | None) -> None:
    """Refuse publication of a non-`main` snapshot (task 2.3)."""
    if not is_publishable_ref(ref):
        raise PublicationRefused(
            f"{repository}@{normalize_ref(ref)}: a snapshot for a ref other than "
            f"{DEFAULT_REF!r} is session-local derived data and is never published "
            f"(add-dashboard-repo-selector task 2.3)")


# --------------------------- entries ---------------------------

@dataclass
class SnapshotEntry:
    """One (repository, ref) snapshot the registry can serve."""

    repository: str
    ref: str = DEFAULT_REF
    snapshot_path: Path | None = None
    payload: bytes | None = None          # in-process derived cache (fetched bytes)
    source_root: Path | None = None       # this entry's /source confinement root
    source_revision: str | None = None
    generated_at: str | None = None
    origin: str = ORIGIN_LOCAL
    display_name: str | None = None
    stale: bool = False
    stale_reason: str | None = None
    location: str | None = None           # the index location this entry came from
    unavailable_reason: str | None = None
    # WHICH TILE's session this entry is, as `(scope_kind, scope_id)` — set only on
    # session entries, and only by the code that OPENED the session, which is the
    # one place the answer is known. It is not derivable from the ref: a `-2` branch
    # is tile `<t>-2`'s first session and tile `<t>`'s second, and reading liveness
    # by the ref alone hid a tile's OWN live session as soon as a sibling tile
    # spelling that ordinal entered the inventory (PR #49 second-review finding 6).
    # None on a bootstrap-reconstructed entry, where the worktree names a branch and
    # nothing names a tile — `branch_session.live_session_branches` treats that
    # unknown as an AMBIGUITY rather than an absence.
    session_tile: tuple[str, str] | None = None
    # WHAT THIS SESSION BRANCHED FROM, as `(base_ref, base_revision)` — set only
    # on session entries, by the OPEN that created the branch (the one place the
    # answer exists) or re-derived by the bootstrap from the session's own
    # durable marker/git. It is what lets the chat-turn binding check accept a
    # buffer still based on the pre-session ref (T104 R-12, reviewer ruling
    # 2026-08-02): acceptance is on the recorded REVISION, never the ref name
    # alone. None degrades to the original name-equality binding — advisory,
    # exactly like `session_tile` above, and never the reason a session fails.
    session_base: tuple[str, str] | None = None

    def __post_init__(self) -> None:
        self.ref = normalize_ref(self.ref)
        if self.snapshot_path is not None:
            self.snapshot_path = Path(self.snapshot_path)
        if self.source_root is not None:
            self.source_root = Path(self.source_root)

    @property
    def key(self) -> tuple[str, str]:
        return (self.repository, self.ref)

    @property
    def key_id(self) -> str:
        return key_id(self.repository, self.ref)

    @property
    def available(self) -> bool:
        """Whether this entry can actually serve bytes. An indexed-but-unfetchable
        entry stays in the registry as UNAVAILABLE so the selector can say so
        while the active view keeps rendering (spec: "An indexed snapshot cannot
        be fetched")."""
        if self.payload is not None:
            return True
        return bool(self.snapshot_path and self.snapshot_path.is_file())

    def read_bytes(self) -> bytes | None:
        """The snapshot bytes — the in-process cache first, then the file."""
        if self.payload is not None:
            return self.payload
        if self.snapshot_path is None:
            return None
        try:
            return self.snapshot_path.read_bytes()
        except OSError:
            return None

    def read_json(self) -> dict | None:
        raw = self.read_bytes()
        if raw is None:
            return None
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def short_revision(self) -> str:
        return (self.source_revision or "")[:12] or "unknown"

    def freshness(self) -> dict:
        """The header contract (design D11): `repo @ ref · short SHA ·
        generated-at`, plus the origin and the stale verdict the banner needs.
        Serving-side additive fields on top of the index locator shape."""
        return {
            "repository": self.repository,
            "ref": self.ref,
            "source_revision": self.source_revision,
            "source_revision_short": self.short_revision(),
            "generated_at": self.generated_at,
            "origin": self.origin,
            "stale": bool(self.stale),
            "stale_reason": self.stale_reason,
            "available": self.available,
            "unavailable_reason": self.unavailable_reason,
        }

    def index_entry(self) -> dict:
        """This entry as a snapshot-INDEX entry (the openxFactory
        `ideation-dashboard-snapshot-index` locator shape) plus the additive
        serving-side freshness fields consumers may ignore."""
        out: dict[str, Any] = {
            "repository": self.repository,
            "ref": self.ref,
            "snapshot": self.location or (
                self.snapshot_path.name if self.snapshot_path else f"{self.repository}-snapshot.json"),
            "source_revision": self.source_revision or "unknown",
        }
        if self.generated_at:
            out["generated_at"] = self.generated_at
        if self.display_name:
            out["display_name"] = self.display_name
        out.update({
            "origin": self.origin,
            "stale": bool(self.stale),
            "available": self.available,
        })
        if self.stale_reason:
            out["stale_reason"] = self.stale_reason
        if self.unavailable_reason:
            out["unavailable_reason"] = self.unavailable_reason
        return out


def entry_from_snapshot_file(
    path: Path | str,
    *,
    repository: str | None = None,
    ref: str | None = None,
    source_root: Path | str | None = None,
    origin: str = ORIGIN_LOCAL,
    stale: bool = False,
    stale_reason: str | None = None,
    display_name: str | None = None,
) -> SnapshotEntry:
    """Build an entry from a snapshot ON DISK, reading its repository and its
    generation stamp OUT OF the snapshot rather than restating them: the
    snapshot is the source of those facts and a divergent index is a bug."""
    path = Path(path)
    doc: dict = {}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        doc = {}
    gen = doc.get("generation") if isinstance(doc.get("generation"), dict) else {}
    return SnapshotEntry(
        repository=str(repository or doc.get("repository") or "unknown"),
        ref=normalize_ref(ref),
        snapshot_path=path,
        source_root=Path(source_root) if source_root is not None else None,
        source_revision=(gen or {}).get("source_revision"),
        generated_at=(gen or {}).get("generated_at"),
        origin=origin,
        stale=stale,
        stale_reason=stale_reason,
        display_name=display_name,
    )


# --------------------------- source containment (pure) ---------------------------

# The only dot-FILE extensions `/source` serves. The corpus has exactly one
# legitimate dotfile family — `openspec/changes/*/.openspec.yaml`, which the
# generator lists in `changes[].files` and the explorer renders as clickable
# rows — so this is deliberately a short allowlist and not "any dotfile".
SERVED_DOTFILE_SUFFIXES = frozenset({".yaml", ".yml", ".md", ".json"})

def resolve_within(root: Path, url_tail: str) -> Path | None:
    """Resolve `<tail>` to an absolute FILE under `root`, or None to reject.
    Rejects absolute paths, NUL bytes, every escape of the root (`..`,
    percent-encoded `..`, symlinks) and every DOT-DIRECTORY inside it —
    percent-decoding happens BEFORE both checks so `%2e%2e` and `%2egit` cannot
    slip past. This is the single-root check `serve.resolve_source_path` has
    always applied, lifted here so it can be applied PER REGISTRY ENTRY
    (task 2.2).

    THE DOT-DIRECTORY EXCLUSION (T092 acceptance sweep, defect 10). `/source`
    served the served checkout's entire `.git`: `GET /source/.git/config`
    answered 200 text/plain with the full remote configuration — in a real
    checkout an https remote with an embedded PAT, handed straight to any page
    on the CSP-free local origin — and `/source/.git/logs/HEAD` answered with
    committer name and email. Bounded today only by the loopback bind, which is
    not a boundary the resolver may rely on.

    CONFINEMENT IS NOT WHAT WAS MISSING, and this must not be mistaken for a
    rewrite of it: traversal was and is correctly blocked (encoded
    `../../../etc/passwd` -> 404), which is exactly why the escape-shaped tests
    all passed while this was open. What was missing is a LEGITIMATE-PATH,
    FORBIDDEN-TARGET rule.

    The rule has two halves, and the second is narrower than "no dots" on
    purpose:

      * NO DOT-DIRECTORY, ever. Every component but the last is refused if it
        begins with a dot. That is where the credentials actually live —
        `.git/config`, `.git/logs/HEAD`, `.github/`, `.ssh/`, `.aws/` — and
        `/source` exists to serve governance documents, of which a dot-directory
        holds none.
      * A DOT-FILE only if it carries a projected extension. The corpus really
        does have one legitimate dotfile: every OpenSpec change folder holds
        `.openspec.yaml`, the generator's `rglob` puts all 48 of them into
        `changes[].files`, and the explorer renders that list as clickable rows.
        Refusing every dot-prefixed name would 404 a path the surface itself
        offers. So an extensionless or unrecognised dot-file — `.env`,
        `.gitignore`, `.npmrc`, `.env.production` — is refused, and
        `.openspec.yaml` is served.

    A `.git` (or any dot-directory) named as the LAST component is refused by
    the `is_file()` check below, so the first half needs no special case for
    it."""
    rel = urllib.parse.unquote(url_tail)
    rel = rel.split("?", 1)[0].split("#", 1)[0]
    if not rel or rel.startswith("/") or "\x00" in rel:
        return None
    parts = [p for p in rel.replace("\\", "/").split("/") if p not in ("", ".")]
    if any(p.startswith(".") and p != ".." for p in parts[:-1]):
        return None
    if parts and parts[-1].startswith(".") and parts[-1] != "..":
        if PurePosixPath(parts[-1]).suffix not in SERVED_DOTFILE_SUFFIXES:
            return None
    root = Path(root).resolve()
    try:
        resolved = (root / rel).resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    if resolved != root and not resolved.is_relative_to(root):
        return None
    if not resolved.is_file():
        return None
    return resolved


# --------------------------- the registry ---------------------------

@dataclass
class Aggregate:
    """A composed cross-repository selection, declared by the index as member
    (repository, ref) pairs. Composition reads the index and the snapshots it
    names — it NEVER scans a repository (spec: "An aggregate selection is
    rendered"). The rendering SHAPE stays the staged topic's open question 1;
    what is fixed here is only that it composes from the index."""

    id: str
    members: list[tuple[str, str]] = field(default_factory=list)
    display_name: str | None = None


class SnapshotRegistry:
    """The ONE snapshot registry, keyed (repository, ref).

    MUTATION IS SERIALIZED (PR #49 review finding 10). `serve.py` is a
    `ThreadingHTTPServer`, so two requests mutate this object concurrently, and
    the invariant FR-014a needs — "`main` stays ACTIVE while a session entry
    enters the key space" — is a READ-MODIFY-WRITE over `_active`
    (`branch_session._preserving_active`: read the active key, run the action,
    put it back). Interleaved, two of those leave a DRAFT globally active, which
    is what the wheel, the funnel and the pipeline board then render.

    A `threading.RLock` is the RIGHT tool here and not an under-reach: this
    registry is per-PROCESS in-memory state (`_entries` is a plain dict, which is
    why `bootstrap_sessions` has to re-derive liveness in every new process).
    There is no cross-process registry to race over. The cross-process writer
    conflict is the WORKTREE INDEX, and that is owned by
    `session_git.worktree_action_lock()`, which is a real file lock."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], SnapshotEntry] = {}
        self._aggregates: dict[str, Aggregate] = {}
        self._active: tuple[str, str] | None = None
        self._lock = threading.RLock()

    @contextlib.contextmanager
    def atomically(self):
        """Hold the registry for a read-modify-write. Re-entrant, so a mutator
        called inside the block is safe."""
        with self._lock:
            yield self

    # ---- registration ----
    def register(self, entry: SnapshotEntry, *, active: bool = False) -> SnapshotEntry:
        with self._lock:
            previous = self._entries.get(entry.key)
            if previous is not None and entry.session_tile is None:
                # THE SESSION'S OWNER IS STICKY (PR #49 second-review finding 6).
                # `SnapshotSource._regenerate` re-registers a FRESH entry for every
                # ref it regenerates — which for a session happens on every gate
                # action (FR-010) — and a rebuilt entry knows the ref but not the
                # tile. Losing the owner there took the tile's own live session out
                # of its own liveness family the moment a sibling tile spelling that
                # ordinal appeared. Carried forward here, at the ONE place entries
                # are replaced, rather than at each of the callers.
                entry.session_tile = previous.session_tile
            if previous is not None and entry.session_base is None:
                # The session's BASE rides the same stickiness (T104 R-12): only
                # the OPEN knows it, every regenerate would otherwise drop it,
                # and losing it re-refuses the post-partial-Save turn the R-12
                # ruling makes valid.
                entry.session_base = previous.session_base
            self._entries[entry.key] = entry
            if active or self._active is None:
                self._active = entry.key
            return entry

    def register_aggregate(self, aggregate: Aggregate) -> Aggregate:
        with self._lock:
            self._aggregates[aggregate.id] = aggregate
            return aggregate

    def drop(self, repository: str, ref: str | None = None) -> None:
        with self._lock:
            self._entries.pop(snapshot_key(repository, ref), None)

    # ---- lookup ----
    def get(self, repository: str, ref: str | None = None) -> SnapshotEntry | None:
        """Ref-less lookups resolve to `main` (D4)."""
        return self._entries.get(snapshot_key(repository, ref))

    def entries(self) -> list[SnapshotEntry]:
        """Registered entries, ordered by (repository, ref) — a stable roster."""
        return [self._entries[k] for k in sorted(self._entries)]

    def aggregates(self) -> list[Aggregate]:
        return [self._aggregates[k] for k in sorted(self._aggregates)]

    def keys(self) -> list[tuple[str, str]]:
        return sorted(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def active(self) -> SnapshotEntry | None:
        if self._active is None:
            return None
        return self._entries.get(self._active)

    def set_active(self, repository: str, ref: str | None = None) -> SnapshotEntry | None:
        with self._lock:
            entry = self.get(repository, ref)
            if entry is not None:
                self._active = entry.key
            return entry

    def resolve(self, repository: str | None, ref: str | None = None) -> SnapshotEntry | None:
        """The one resolution every route uses: a named pair, or the ACTIVE entry
        when no repository is named (which is what `/snapshot.json` with no query
        means — today's behaviour, unchanged)."""
        if repository is None or repository == "":
            return self.active
        return self.get(repository, ref)

    # ---- per-entry source confinement (task 2.2) ----
    def resolve_source(self, repository: str | None, ref: str | None, tail: str) -> Path | None:
        """Resolve a `/source/` read THROUGH one entry, confined to that entry's
        own root. An unknown pair, or an entry with no declared root, serves
        nothing (fail-closed — never another entry's checkout)."""
        entry = self.resolve(repository, ref)
        if entry is None or entry.source_root is None:
            return None
        return resolve_within(entry.source_root, tail)

    # ---- the index (openxFactory `ideation-dashboard-snapshot-index`) ----
    def index_document(self, *, published: bool = False) -> dict:
        """Compose the snapshot index from the registry. `published=True` applies
        the publication rule: a non-`main` entry — or a non-`main` AGGREGATE MEMBER
        — refuses the whole index (task 2.3), because a published index is shared
        state.

        The member half was missing (PR #49 review finding 14, wave 2). The
        finding-14 repair reasoned from "a session ref is structurally
        unpublishable", and for `entries` it is; `aggregates[].members` is the
        second place this document carries `(repository, ref)` pairs and nothing
        checked it, so a published index could name the branch of unmerged work.
        The check is here, over BOTH collections, so the premise is true of the
        document rather than of one field."""
        entries = self.entries()
        if published:
            for entry in entries:
                assert_publishable(entry.repository, entry.ref)
            for aggregate in self.aggregates():
                for repository, ref in aggregate.members:
                    assert_publishable(repository, ref)
        doc: dict[str, Any] = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "kind": INDEX_KIND,
            "entries": [e.index_entry() for e in entries],
        }
        newest = [e.generated_at for e in entries if e.generated_at]
        if newest:
            doc["generated_at"] = max(newest)
        aggregates = self.aggregates()
        if aggregates:
            doc["aggregates"] = [{
                "id": a.id,
                **({"display_name": a.display_name} if a.display_name else {}),
                "members": [{"repository": r, "ref": f} for r, f in a.members],
            } for a in aggregates]
        if not published and self._active is not None:
            # Serving-side only: which entry the server considers ACTIVE. Additive,
            # ignored by any consumer that does not know it (and absent from a
            # published index, which has no notion of "active").
            doc["active"] = {"repository": self._active[0], "ref": self._active[1]}
        return doc

    # ---- aggregate composition (from the index, never a repository scan) ----
    def compose_aggregate(self, aggregate_id: str) -> dict | None:
        """Compose one snapshot-shaped document from an aggregate's member
        snapshots. Ids are namespaced `<repository>::<id>` — including inside
        every edge reference — so two repositories can carry the same cluster id
        without corrupting either one's edges, and each item carries its
        `repository` so a renderer can badge it. Members with no available
        snapshot are skipped (degrade, never refuse)."""
        aggregate = self._aggregates.get(aggregate_id)
        if aggregate is None:
            return None
        members = [self.get(repo, ref) for repo, ref in aggregate.members]
        snapshots = [(m, m.read_json()) for m in members if m is not None]
        loaded = [(m, doc) for m, doc in snapshots if isinstance(doc, dict)]
        return compose_snapshots(aggregate, loaded)


# --------------------------- aggregate composition (pure) ---------------------------

_COLLECTIONS = ("documents", "clusters", "possibles", "staged_topics", "changes",
                "keyword_index")


def _ns(repository: str, value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return value
    return f"{repository}::{value}"


def _namespace_item(repository: str, ref: str, item: Any) -> Any:
    """Namespace one collection item's own id and every id it references."""
    if not isinstance(item, dict):
        return item
    out = dict(item)
    out["repository"] = repository
    out["ref"] = ref
    if isinstance(out.get("id"), str):
        out["id"] = _ns(repository, out["id"])
    for key in ("claiming_clusters", "members", "documents"):
        if isinstance(out.get(key), list) and all(isinstance(v, str) for v in out[key]):
            out[key] = [_ns(repository, v) for v in out[key]]
    if isinstance(out.get("document_edges"), list):
        out["document_edges"] = [
            {**e, "document": _ns(repository, e.get("document"))} if isinstance(e, dict) else e
            for e in out["document_edges"]
        ]
    if isinstance(out.get("option_set"), dict) and isinstance(out["option_set"].get("members"), list):
        opt = dict(out["option_set"])
        opt["members"] = [_ns(repository, v) for v in opt["members"]]
        out["option_set"] = opt
    if isinstance(out.get("pick"), dict):
        out["pick"] = dict(out["pick"])
    return out


def compose_snapshots(aggregate: Aggregate,
                      members: Iterable[tuple[SnapshotEntry, dict]]) -> dict:
    """Merge member snapshots into one snapshot-shaped composed view."""
    composed: dict[str, Any] = {
        "schema_version": 1,
        "kind": "ideation-dashboard-snapshot",
        "repository": aggregate.id,
        "generation": {"source_revision": "composed", "composed_from": []},
    }
    for key in _COLLECTIONS:
        composed[key] = []
    revisions: list[str] = []
    stamps: list[str] = []
    for entry, doc in members:
        repo = str(doc.get("repository") or entry.repository)
        for key in _COLLECTIONS:
            items = doc.get(key)
            if isinstance(items, list):
                composed[key].extend(
                    _namespace_item(repo, entry.ref, item) for item in items)
        gen = doc.get("generation") if isinstance(doc.get("generation"), dict) else {}
        rev = (gen or {}).get("source_revision")
        stamp = (gen or {}).get("generated_at")
        if rev:
            revisions.append(f"{repo}@{entry.ref}:{rev}")
        if stamp:
            stamps.append(stamp)
        composed["generation"]["composed_from"].append({
            "repository": repo, "ref": entry.ref, "source_revision": rev,
        })
    if revisions:
        composed["generation"]["source_revision"] = "composed:" + ",".join(sorted(revisions))
    if stamps:
        composed["generation"]["generated_at"] = max(stamps)
    return composed


# --------------------------- index parsing (read-side) ---------------------------

def parse_index(doc: Any) -> tuple[list[dict], list[Aggregate]]:
    """Read an index document into (entry dicts, aggregates). Read-through and
    tolerant: a malformed entry is dropped rather than raising, because the
    pinned openxFactory validator — not this reader — is where a malformed index
    is an error. Unknown properties are ignored (the family's additive
    posture)."""
    if not isinstance(doc, dict):
        return [], []
    entries: list[dict] = []
    for raw in doc.get("entries") or []:
        if not isinstance(raw, dict):
            continue
        repository = raw.get("repository")
        location = raw.get("snapshot")
        if not isinstance(repository, str) or not repository:
            continue
        if not isinstance(location, str) or not location:
            continue
        entries.append({
            "repository": repository,
            "ref": normalize_ref(raw.get("ref")),
            "snapshot": location,
            "source_revision": raw.get("source_revision"),
            "generated_at": raw.get("generated_at"),
            "display_name": raw.get("display_name"),
        })
    aggregates: list[Aggregate] = []
    for raw in doc.get("aggregates") or []:
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str):
            continue
        members: list[tuple[str, str]] = []
        for member in raw.get("members") or []:
            if isinstance(member, dict) and isinstance(member.get("repository"), str):
                members.append(snapshot_key(member["repository"], member.get("ref")))
        if members:
            aggregates.append(Aggregate(id=raw["id"], members=members,
                                        display_name=raw.get("display_name")))
    return entries, aggregates


def build_index(entries: Iterable[SnapshotEntry], *, published: bool = True,
                aggregates: Iterable[Aggregate] = ()) -> dict:
    """Build a publishable index document from entries (the lane's writer).
    Refuses a non-`main` entry when publishing (task 2.3)."""
    registry = SnapshotRegistry()
    for entry in entries:
        registry.register(entry)
    for aggregate in aggregates:
        registry.register_aggregate(aggregate)
    return registry.index_document(published=published)


# --------------------------- data sources (serving side only) ---------------------------

class DirectoryDataSource:
    """A published snapshot tree on the filesystem (a checked-out data source, a
    mounted volume, or a test fixture). Reads are confined to the declared root
    by the same containment check every `/source/` read uses."""

    kind = "directory"

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)

    def describe(self) -> str:
        return f"directory:{self.root}"

    def read(self, relpath: str) -> bytes:
        target = resolve_within(self.root, relpath)
        if target is None:
            raise DataSourceError(f"{self.describe()}: {relpath} is not readable")
        try:
            return target.read_bytes()
        except OSError as exc:
            raise DataSourceError(f"{self.describe()}: {relpath}: {exc}") from exc


class UrlDataSource:
    """A published snapshot tree behind an HTTP(S) base URL, read by the SERVING
    side (never the browser — design D5). The concrete production source is
    Brett's open-question-1 ratification; this is the seam, not the ruling.

    A bearer token is taken ONLY from a named environment variable the operator
    supplies, so no credential is ever written in a repository, and the token
    never leaves the serving process."""

    kind = "url"

    def __init__(self, base_url: str, *, token_env: str | None = None,
                 opener: Callable[..., Any] | None = None,
                 timeout: int = _FETCH_TIMEOUT_SECONDS) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.token_env = token_env
        self._opener = opener or urllib.request.urlopen
        self.timeout = timeout

    def describe(self) -> str:
        return f"url:{self.base_url}"

    def _url(self, relpath: str) -> str:
        rel = str(relpath).lstrip("/")
        if ".." in rel.split("/"):
            raise DataSourceError(f"{self.describe()}: refusing traversal in {relpath!r}")
        return urllib.parse.urljoin(self.base_url, urllib.parse.quote(rel))

    def read(self, relpath: str) -> bytes:
        url = self._url(relpath)
        scheme = urllib.parse.urlsplit(url).scheme
        if scheme not in ("http", "https"):
            raise DataSourceError(f"{self.describe()}: refusing non-HTTP scheme {scheme!r}")
        request = urllib.request.Request(url, method="GET")
        token = os.environ.get(self.token_env) if self.token_env else None
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            # The URL is composed from operator configuration (a base URL flag)
            # plus an index-declared relative location, never from a browser
            # request; the scheme is checked above (S5144/S3649 rationale).
            with self._opener(request, timeout=self.timeout) as response:  # NOSONAR
                return response.read(_MAX_FETCH_BYTES)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raise DataSourceError(f"{self.describe()}: {relpath}: {exc}") from exc


def github_raw_base_url(owner_repo: str, *, ref: str = DEFAULT_REF,
                        path: str = DEFAULT_PUBLISH_PATH) -> str:
    """The RULED hosted binding (Brett, 2026-07-26, open question 1): the
    aggregation repository's published tree, read as RAW FILES. Composed from
    configuration — owner/repo, ref, and path are operator flags, and the
    read-only token is a deploy-time environment variable name — so nothing here
    hardcodes a source or a credential, and a later ratification that moves to a
    blob container changes a fetcher and no contract."""
    slug = str(owner_repo).strip().strip("/")
    if slug.count("/") != 1 or not all(slug.split("/")):
        raise ValueError(f"expected OWNER/REPO, got {owner_repo!r}")
    tree = str(path or "").strip("/")
    tail = f"{slug}/{ref}/" + (f"{tree}/" if tree else "")
    return f"https://{GITHUB_RAW_HOST}/{tail}"


def data_source_from_options(*, directory: Path | str | None = None,
                             url: str | None = None,
                             token_env: str | None = None,
                             opener: Callable[..., Any] | None = None):
    """The ONE place a data source is chosen from configuration. None means "no
    declared source", which is the local plane and the first-boot served plane —
    both of which then render the baked/local entry."""
    if directory:
        return DirectoryDataSource(directory)
    if url:
        return UrlDataSource(url, token_env=token_env, opener=opener)
    return None


# --------------------------- the serving-side source (D5/D6/D7) ---------------------------

class SnapshotSource:
    """What `serve.py` holds: the registry, the optional data source, the baked
    fallback, and the two refresh bindings.

    BOOTSTRAP (D1/D6): try the data source; on ANY failure register the baked
    snapshot as a STALE fallback carrying the reason. The degradation is never
    silent — the entry says it is baked and the renderer shows it.

    REFRESH (D7): `refetch` re-pulls the index and the active snapshot into the
    in-process cache and writes nothing; `regenerate` re-runs the generator
    against the served checkout for one (repository, ref) and writes ONLY the
    derived snapshot artifact, through the interactivity boundary. Neither can
    publish, build, or roll out anything."""

    def __init__(
        self,
        *,
        baked_snapshot: Path | str | None = None,
        repository: str | None = None,
        ref: str | None = None,
        checkout_root: Path | str | None = None,
        data_source=None,
        index_name: str = DEFAULT_INDEX_NAME,
        source_roots: dict[str, Path] | None = None,
        local_index: Path | str | None = None,
        generator: Callable[..., dict] | None = None,
        project_register: Path | str | None = None,
        peek_ttl_seconds: float = PEEK_TTL_SECONDS,
    ) -> None:
        self.baked_snapshot = Path(baked_snapshot) if baked_snapshot else None
        self.checkout_root = Path(checkout_root) if checkout_root else None
        self.data_source = data_source
        self.index_name = index_name
        # Declared confinement roots, keyed canonically: `repo` means
        # `repo@main`, `repo@ref` names the pair explicitly.
        self.source_roots = {
            key_id(*(parse_key_id(raw) or snapshot_key(raw))): Path(value)
            for raw, value in (source_roots or {}).items()
        }
        self.local_index = Path(local_index) if local_index else None
        self.registry = SnapshotRegistry()
        # one writer at a time through `refresh` (finding 10) — see its docstring
        self._refresh_lock = threading.RLock()
        self._generator = generator
        self.project_register = Path(project_register) if project_register else None
        self.errors: list[str] = []
        self.baked_repository = repository
        self.baked_ref = normalize_ref(ref)
        self._peek: dict[tuple[str, str], dict] | None = None
        self._peek_at: float = 0.0
        self.peek_ttl_seconds = float(peek_ttl_seconds)

    # ---- bootstrap ----
    def bootstrap(self) -> SnapshotRegistry:
        """Populate the registry: the declared data source first, then a local
        index, then the baked/local snapshot as the fallback."""
        if self.data_source is not None:
            try:
                self._load_from_data_source()
                self._register_baked(fallback_only=True)
                return self.registry
            except DataSourceError as exc:
                self.errors.append(str(exc))
        if self.local_index is not None:
            try:
                self._load_from_local_index()
            except DataSourceError as exc:
                self.errors.append(str(exc))
        self._register_baked(fallback_only=False)
        return self.registry

    def _source_root_for(self, repository: str, ref: str) -> Path | None:
        """This entry's declared confinement root. Explicit `--source-root`
        declarations win; the baked/local entry falls back to the served
        checkout root; anything else serves no documents (fail-closed)."""
        declared = self.source_roots.get(key_id(repository, ref))
        if declared is not None:
            return declared
        if (repository, ref) == (self.baked_repository, self.baked_ref):
            return self.checkout_root
        return None

    def _register_baked(self, *, fallback_only: bool) -> None:
        """Register the baked/local snapshot. When a data source already
        supplied this pair, the baked copy is NOT registered over it (fetched
        data wins); when nothing else is available it becomes the entry, marked
        stale iff a data source was declared and failed (D6)."""
        if self.baked_snapshot is None or not self.baked_snapshot.is_file():
            return
        probe = entry_from_snapshot_file(
            self.baked_snapshot, repository=self.baked_repository, ref=self.baked_ref)
        repository = probe.repository
        self.baked_repository = self.baked_repository or repository
        if fallback_only and self.registry.get(repository, self.baked_ref) is not None:
            return
        declared_source = self.data_source is not None
        probe.source_root = self._source_root_for(repository, probe.ref)
        probe.origin = ORIGIN_BAKED if declared_source else ORIGIN_LOCAL
        if declared_source:
            probe.stale = True
            probe.stale_reason = (
                "the declared data source is unreachable — showing the snapshot baked "
                "into this image" + (f" ({self.errors[-1]})" if self.errors else ""))
        self.registry.register(probe, active=self.registry.active is None)

    def _load_from_data_source(self) -> None:
        raw = self.data_source.read(self.index_name)
        try:
            doc = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise DataSourceError(f"{self.data_source.describe()}: {self.index_name} is not JSON: {exc}") from exc
        entries, aggregates = parse_index(doc)
        if not entries:
            raise DataSourceError(f"{self.data_source.describe()}: {self.index_name} names no snapshot")
        for meta in entries:
            self._register_fetched(meta)
        for aggregate in aggregates:
            self.registry.register_aggregate(aggregate)
        preferred = self.baked_repository
        if preferred and self.registry.get(preferred, DEFAULT_REF) is not None:
            self.registry.set_active(preferred, DEFAULT_REF)

    def _register_fetched(self, meta: dict) -> SnapshotEntry:
        """Fetch one indexed snapshot into the IN-PROCESS cache. A member that
        cannot be fetched is registered UNAVAILABLE (with the reason) instead of
        being dropped, so the selector reports that repository unavailable while
        the active view keeps rendering."""
        repository, ref = snapshot_key(meta["repository"], meta.get("ref"))
        entry = SnapshotEntry(
            repository=repository, ref=ref,
            source_root=self._source_root_for(repository, ref),
            source_revision=meta.get("source_revision"),
            generated_at=meta.get("generated_at"),
            display_name=meta.get("display_name"),
            origin=ORIGIN_FETCHED,
            location=meta.get("snapshot"),
        )
        try:
            entry.payload = self.data_source.read(meta["snapshot"])
        except DataSourceError as exc:
            entry.unavailable_reason = str(exc)
            self.errors.append(str(exc))
        else:
            doc = entry.read_json() or {}
            gen = doc.get("generation") if isinstance(doc.get("generation"), dict) else {}
            entry.source_revision = entry.source_revision or (gen or {}).get("source_revision")
            entry.generated_at = entry.generated_at or (gen or {}).get("generated_at")
        return self.registry.register(entry)

    def _load_from_local_index(self) -> None:
        """A LOCAL index file (the multi-repository local plane): snapshot
        locations resolve relative to the index file itself, exactly as a
        published index resolves relative to its data source."""
        path = self.local_index
        try:
            doc = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DataSourceError(f"local index {path}: {exc}") from exc
        entries, aggregates = parse_index(doc)
        if not entries:
            raise DataSourceError(f"local index {path} names no snapshot")
        base = Path(path).resolve().parent
        for meta in entries:
            repository, ref = snapshot_key(meta["repository"], meta.get("ref"))
            snapshot_path = (base / meta["snapshot"]).resolve()
            entry = entry_from_snapshot_file(
                snapshot_path, repository=repository, ref=ref,
                source_root=self._source_root_for(repository, ref),
                origin=ORIGIN_LOCAL, display_name=meta.get("display_name"))
            entry.location = meta.get("snapshot")
            if not snapshot_path.is_file():
                entry.unavailable_reason = f"snapshot not found: {meta['snapshot']}"
            self.registry.register(entry)
        for aggregate in aggregates:
            self.registry.register_aggregate(aggregate)
        preferred = self.baked_repository
        if preferred and self.registry.get(preferred, DEFAULT_REF) is not None:
            self.registry.set_active(preferred, DEFAULT_REF)

    # ---- the passive freshness hint (Brett 2026-07-26, open question 2) ----
    def peek_hints(self, *, now: float | None = None) -> dict[tuple[str, str], dict]:
        """What the DATA SOURCE's index currently advertises, per (repository,
        ref) — the raw material for the "newer data available" badge. Cheap by
        construction (the index is thin, D3) and cached for `PEEK_TTL_SECONDS`.

        A failed peek is SILENT: no hint, no banner, no error surfaced. The hint
        is an advertisement, not a projection — the stale banner (D6) is the
        mechanism for "what you are looking at is old", and conflating the two
        would cry wolf every time the source blinked."""
        if self.data_source is None:
            return {}
        stamp = time.monotonic() if now is None else now
        if self._peek is not None and (stamp - self._peek_at) < self.peek_ttl_seconds:
            return self._peek
        hints: dict[tuple[str, str], dict] = {}
        try:
            raw = self.data_source.read(self.index_name)
            doc = json.loads(raw.decode("utf-8"))
        except (DataSourceError, ValueError, UnicodeDecodeError):
            self._peek, self._peek_at = {}, stamp
            return {}
        entries, _aggregates = parse_index(doc)
        for meta in entries:
            hints[snapshot_key(meta["repository"], meta.get("ref"))] = {
                "source_revision": meta.get("source_revision"),
                "generated_at": meta.get("generated_at"),
            }
        self._peek, self._peek_at = hints, stamp
        return hints

    def index_document(self, *, peek: bool = True) -> dict:
        """The registry's index PLUS, per entry, what the data source currently
        advertises (`latest_source_revision` / `latest_generated_at`) and whether
        that beats the loaded bytes (`newer_available`). Additive serving-side
        fields: a consumer that does not know them ignores them, and on a plane
        with no data source they are simply absent."""
        doc = self.registry.index_document()
        hints = self.peek_hints() if peek else {}
        if not hints:
            return doc
        newer_any = False
        for raw in doc.get("entries") or []:
            hint = hints.get(snapshot_key(raw.get("repository"), raw.get("ref")))
            if not hint:
                continue
            latest_rev = hint.get("source_revision")
            latest_at = hint.get("generated_at")
            if latest_rev:
                raw["latest_source_revision"] = latest_rev
            if latest_at:
                raw["latest_generated_at"] = latest_at
            newer = bool(latest_rev and raw.get("source_revision") != latest_rev)
            if newer:
                raw["newer_available"] = True
                newer_any = True
        if newer_any:
            doc["newer_available"] = True
        return doc

    # ---- the two refresh bindings (D7) ----
    @property
    def refresh_binding(self) -> str | None:
        """Which binding this plane offers. A declared data source means the
        served plane's read-only re-pull; otherwise a real checkout means the
        local plane's regenerate; otherwise no refresh affordance at all."""
        if self.data_source is not None:
            return BINDING_REFETCH
        if self.checkout_root is not None and Path(self.checkout_root).is_dir():
            return BINDING_REGENERATE
        return None

    def refresh(self, *, repository: str | None = None, ref: str | None = None) -> dict:
        """Run this plane's refresh binding for one (repository, ref). Returns a
        result dict; raises DataSourceError / PublicationRefused / ValueError on
        refusal so the caller reports inline and leaves the prior view in place."""
        binding = self.refresh_binding
        # SERIALIZED against every other refresh (finding 10). Both bindings are
        # read-modify-writes over the whole registry — `_refetch` REPLACES the
        # object, `_regenerate` decides the active key from what it read — and
        # `serve.py` is a `ThreadingHTTPServer`. The lock lives on the SOURCE
        # rather than on the registry precisely because `_refetch` swaps the
        # registry out: a lock held on the object being replaced would not cover
        # its successor.
        with self._refresh_lock:
            if binding == BINDING_REFETCH:
                return self._refetch(repository=repository, ref=ref)
            if binding == BINDING_REGENERATE:
                return self._regenerate(repository=repository, ref=ref)
        raise DataSourceError("no refresh binding is available on this plane")

    def _refetch(self, *, repository: str | None, ref: str | None) -> dict:
        """SERVED binding: re-read the index and the requested snapshot into the
        in-process cache. Writes nothing anywhere. A failure raises and the
        registry keeps the entries it already had."""
        previous_active = self.registry.active
        raw = self.data_source.read(self.index_name)
        try:
            doc = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise DataSourceError(f"{self.data_source.describe()}: {self.index_name} is not JSON") from exc
        entries, aggregates = parse_index(doc)
        if not entries:
            raise DataSourceError(f"{self.data_source.describe()}: {self.index_name} names no snapshot")
        fresh = SnapshotRegistry()
        wanted = snapshot_key(repository, ref) if repository else (
            previous_active.key if previous_active else None)
        target: SnapshotEntry | None = None
        for meta in entries:
            key = snapshot_key(meta["repository"], meta.get("ref"))
            entry = SnapshotEntry(
                repository=key[0], ref=key[1],
                source_root=self._source_root_for(*key),
                source_revision=meta.get("source_revision"),
                generated_at=meta.get("generated_at"),
                display_name=meta.get("display_name"),
                origin=ORIGIN_FETCHED, location=meta.get("snapshot"))
            # Only the ACTIVE (requested) snapshot is re-pulled; the rest keep
            # whatever bytes the registry already holds. The index is cheap and
            # the snapshots are not (design D3's traffic-shape argument).
            if wanted is None or key == wanted:
                entry.payload = self.data_source.read(meta["snapshot"])
                target = entry
            else:
                held = self.registry.get(*key)
                if held is not None and held.payload is not None:
                    entry.payload = held.payload
            fresh.register(entry, active=(wanted is not None and key == wanted))
        for aggregate in aggregates:
            fresh.register_aggregate(aggregate)
        if target is None and wanted is not None:
            raise DataSourceError(
                f"{wanted[0]}@{wanted[1]} is not in {self.index_name}")
        # CARRY OVER WHAT THE INDEX STRUCTURALLY CANNOT (PR #49 review finding
        # 10a). A session ref is never publishable (`assert_publishable`), so it
        # can never appear in a published index — and this method REPLACES the
        # whole registry with one rebuilt from that index. Liveness IS the
        # registry entry (FR-008), so one refresh of `main` silently ENDED every
        # live session in the process: `edit-document` and `open-pr` then 409'd
        # until the serve restarted, over a worktree and a branch that were still
        # there. Refreshing derived data is a READ and must not end a session.
        for held in self.registry.entries():
            if not is_publishable_ref(held.ref):
                fresh.register(held)
        self.registry = fresh
        if wanted is not None:
            self.registry.set_active(*wanted)
        self._register_baked(fallback_only=True)
        active = self.registry.active
        return {"binding": BINDING_REFETCH, "entries": len(self.registry),
                **(active.freshness() if active else {})}

    def _regenerate(self, *, repository: str | None, ref: str | None) -> dict:
        """LOCAL binding: re-run the generator against the served checkout for
        one (repository, ref) and rewrite that entry's derived snapshot. The ONLY
        write any refresh performs, it lands through the interactivity boundary,
        and it needs no server restart because the route re-reads the file."""
        previous = self.registry.active
        entry = self.registry.resolve(repository, ref)
        if entry is None:
            raise ValueError(f"unknown snapshot {repository}@{normalize_ref(ref)}")
        if entry.snapshot_path is None:
            raise ValueError(f"{entry.key_id}: no local snapshot path to regenerate")
        root = entry.source_root or self.checkout_root
        if root is None or not Path(root).is_dir():
            raise ValueError(f"{entry.key_id}: no served checkout to regenerate from")
        from ideation_dashboard import snapshot as snapshot_mod
        from ideation_dashboard.boundary import OutputBoundary
        generate = self._generator
        if generate is None:
            from ideation_dashboard.generator import generate_snapshot
            generate = generate_snapshot
        snapshot = generate(
            Path(root), entry.repository,
            project_register_source=self.project_register,
        )
        target = Path(entry.snapshot_path)
        boundary = OutputBoundary(target.parent, [target.name])
        snapshot_mod.write_snapshot(snapshot, target, boundary)
        refreshed = entry_from_snapshot_file(
            target, repository=entry.repository, ref=entry.ref,
            source_root=entry.source_root, origin=ORIGIN_LOCAL)
        refreshed.location = entry.location
        refreshed.display_name = entry.display_name
        # A REGENERATE NO LONGER PROMOTES A SESSION REF (PR #49 review finding
        # 10b). `active=True` is right for `main` — regenerating the snapshot the
        # human is looking at should keep them looking at it — and WRONG for a
        # session: FR-014a requires the wheel, the funnel, the pipeline board and
        # `index.active` to stay on `main` for a session's whole life. The only
        # compensation for this used to live in the CALLER
        # (`branch_session._preserving_active`), so the serve's own
        # `POST /actions/refresh` skipped it: one click of the header's regenerate
        # button while the page was on the session ref made an UNMERGED DRAFT the
        # process-global active entry, and a fresh page load then OPENED on it.
        # The guard belongs in the mutator, where a future caller cannot forget
        # it — Phase 4 realization note 3's invariant, made structural.
        already_active = (previous is not None and previous.key == entry.key)
        self.registry.register(
            refreshed, active=(already_active or is_publishable_ref(entry.ref)))
        return {"binding": BINDING_REGENERATE, "entries": len(self.registry),
                **refreshed.freshness()}
