"""Workbench reference sets: manifest persistence + scratch notebooks + bounded
actions (plan "workbench.py"; change tasks 3.4; US7 T026/T027).

Three responsibilities, all behind the interactivity boundary:

  MANIFEST ENGINE (T026)  create/load/update `ideation-workbench` manifests
      under the gitignored `ideation/workbench/` prefix, WRITTEN THROUGH
      `boundary.OutputBoundary` and SCHEMA-VALID at every write (the pinned
      openxFactory validator is the authority; `save(..., validate=True)`
      re-checks it). Membership carries the override discipline the schema and
      spec require: a `manual-include` member and every `excluded` entry MUST
      carry a recorded `reason` — an override without one is REFUSED (raised as
      a `WorkbenchError`, never a silent set edit). Seed provenance,
      `action_history` appends, and the `xf-wb-*` notebook binding are managed
      here. `committed_manifests()` mirrors the validator's committed-manifest
      guard on the code side: a tracked manifest is session state that leaked
      into version control and is reported.

  NOTEBOOK ADAPTER (T026)  a thin, FULLY MOCKABLE wrapper over the `nlm` CLI
      (modelled on `scripts/sync-notebooklm-books.py`'s `nlm(*args)` shape).
      Every call goes through an injectable `runner`; tests inject a fake and
      NEVER touch the real `nlm`. When `nlm` is absent the adapter DEGRADES
      GRACEFULLY — it reports `skipped`/`not-available` and never crashes the
      caller. `orphan_sweep()` deletes any `xf-wb-*` notebook no live manifest
      still binds; wiring it into the real sync script is the aggregation lane's
      job (out of scope here — see the note at `orphan_sweep`).

  BOUNDED ACTIONS (T027)  `run_readiness` (a recorded NOT-AVAILABLE stub — the
      readiness panel is `add-ideation-cross-reference-readiness`; we never fake
      a score), `run_scoped_doc_health` (the real in-repo doc-health
      machinery invoked IN-PROCESS, scoped to the set's docs), and
      `draft_organize` (a `staging/<topic>/` packet SKELETON pre-filled from the
      set and written OUTSIDE `ideation/staging/` via
      `boundary.permit_draft_skeleton` — moving it into staging stays a human
      gate action).
"""

from __future__ import annotations

import copy
import hashlib
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

import yaml

from .boundary import OutputBoundary
from .snapshot import find_validator

# --------------------------------------------------------------------------
# contract constants (mirror ideation-workbench.schema.yaml — the READ-ONLY
# truth; these strings are transcribed, never invented)
# --------------------------------------------------------------------------
SCHEMA_VERSION = 1
KIND = "ideation-workbench"

# Gitignored prefixes. Manifests live directly under WORKBENCH_DIR; draft-organize
# skeletons under ORGANIZE_DIR (still under ideation/workbench/, i.e. OUTSIDE
# ideation/staging/, so `permit_draft_skeleton` accepts them).
WORKBENCH_DIR = "ideation/workbench/"
ORGANIZE_DIR = "ideation/workbench/organize/"

# member.via enum
VIA_RECIPE_MATCH = "recipe-match"
VIA_MANUAL_INCLUDE = "manual-include"
VIA_CLUSTER_SEED = "cluster-seed"
VIA_VALUES = frozenset({VIA_RECIPE_MATCH, VIA_MANUAL_INCLUDE, VIA_CLUSTER_SEED})

# seed.kind enum
SEED_CLUSTER = "cluster-seeded"
SEED_ADHOC = "ad-hoc"
SEED_RECIPE = "recipe"
SEED_KINDS = frozenset({SEED_CLUSTER, SEED_ADHOC, SEED_RECIPE})

# action_history.action enum (full vocabulary incl. the reserved canvas actions)
ACTION_NOTEBOOK = "notebook"
ACTION_READINESS = "readiness"
ACTION_DOC_HEALTH = "doc-health"
ACTION_DRAFT_ORGANIZE = "draft-organize"
ACTION_COMPOSE_POSSIBLE = "compose-possible"
ACTION_DERIVE_POSSIBLES = "derive-possibles"
# Lens "add as cluster" (US6 T024): widened additively into the pinned
# openxFactory ideation-workbench schema's action_history enum. Records the lens
# add-as-cluster action, now referencing the human-seen cross-reference-queue
# entry the submission writes (T028 realized 2026-07-14 — the pending_review
# intake contract landed; see human_seen.py).
ACTION_ADD_AS_CLUSTER = "add-as-cluster"
ACTION_VALUES = frozenset({
    ACTION_NOTEBOOK, ACTION_READINESS, ACTION_DOC_HEALTH, ACTION_DRAFT_ORGANIZE,
    ACTION_COMPOSE_POSSIBLE, ACTION_DERIVE_POSSIBLES, ACTION_ADD_AS_CLUSTER,
})

# notebook alias pattern (schema: "^xf-wb-.+$")
NOTEBOOK_PREFIX = "xf-wb-"

# The BRANCH-SESSION notebook namespace (007-workbench-branch-sessions T073;
# FR-037/FR-038, D11). Transcribed rather than imported so this module keeps its
# flat import graph — `branch_session.NOTEBOOK_PREFIX` is the derivation's home
# and a test pins the two EQUAL, because a drift here is exactly D11's defect: a
# session notebook inside the `xf-wb-` namespace would be an orphan from birth
# and the next routine sweep would delete it mid-session. The two namespaces are
# DISJOINT, and that disjointness is what keeps the sweep and the session
# lifecycle independent of one another (research R8).
SESSION_NOTEBOOK_PREFIX = "xf-session-"

# The KEY half of a session alias, transcribed from `branch_session` for the same
# flat-import-graph reason and pinned EQUAL by a test: every derived alias ends in
# `-k<12 lowercase hex>` (`notebook_key_digest`). `retire` requires it, so a
# title-keyed delete on the SHARED account cannot be handed a hand-built or stale
# pre-digest spelling (PR #49 hardening item 2's residual).
SESSION_KEY_SEPARATOR = "-k"
SESSION_KEY_DIGEST_CHARS = 12
_SESSION_KEY_SUFFIX = re.compile(
    rf"{re.escape(SESSION_KEY_SEPARATOR)}[0-9a-f]{{{SESSION_KEY_DIGEST_CHARS}}}$")

# The prefixes this module MANAGES. A notebook outside both is never created,
# never listed as a candidate, and never deleted by anything here.
MANAGED_NOTEBOOK_PREFIXES = (NOTEBOOK_PREFIX, SESSION_NOTEBOOK_PREFIX)

# scratch-notebook URL + managed-source-title conventions (v2 tile action). A
# projected source's title carries the doc's repo-relative path and a short
# content hash, so a re-click diffs by title + content hash (mirroring the
# lifecycle sync manifest's change-detection) with the notebook itself as the
# store — no extra per-source state on the manifest. The URL base is the
# fallback when `nlm notebook get` does not surface an explicit url field.
NOTEBOOK_URL_BASE = "https://notebooklm.google.com/notebook/"
SOURCE_HASH_SEP = "  #"   # a repo-relative posix path never contains a double space
_SOURCE_TITLE_RE = re.compile(r"^(?P<path>.+?) {2}#(?P<hash>[0-9a-f]{6,})$")
_NOTEBOOK_URL_KEYS = ("url", "share_url", "shareUrl", "notebook_url", "web_url", "link")
NLM_TIMEOUT = 45  # seconds — an nlm subprocess must never hang the loopback action

# Skip an implausibly large document rather than shipping it as a session source
# (mirrors notebook_action._MAX_SOURCE_BYTES, the tile action's own cap).
_MAX_SESSION_SOURCE_BYTES = 400_000

# --------------------------------------------------------------------------
# the session projection's AGGREGATE bounds (PR #49 second-review finding 21)
# --------------------------------------------------------------------------
#
# `_MAX_SESSION_SOURCE_BYTES` bounds ONE document. Nothing bounded the COUNT, and
# the count is the corpus's: `session_documents` reads every governed document in
# the session worktree, which on the real openxFactory checkout is 176 documents /
# 1.83 MB, and `_sync_sources` issues one `nlm source add` subprocess per document,
# SEQUENTIALLY, from inside the `create-document` gate route — so the HTTP request
# could not return until the whole projection finished. With `NLM_TIMEOUT` per call
# and no aggregate ceiling the arithmetic is 176 x 45s = 2.2 hours of a governed
# write waiting on an external SaaS: D19 / plan Constraint 8 violated by
# arithmetic rather than by a bug, since every individual call behaved correctly.
#
# TWO bounds, because they answer different failure shapes:
#
#   COUNT (`SESSION_SOURCE_COUNT_CAP`) — a corpus that grows without limit. Bounds
#   the number of sources one projection will attempt at all.
#   WALL CLOCK (`SESSION_PROJECTION_BUDGET`) — an `nlm` that is merely SLOW, which
#   the count cap cannot bound: 60 wedged calls is still 45 minutes. The deadline
#   is checked BEFORE each add, never mid-call, so the worst case is
#   `budget + NLM_TIMEOUT` = 135s rather than unbounded.
#
# The remainder is DEFERRED, not dropped: it is reported (`sources_deferred`, and
# the FR-042 notice `branch_session` builds from it) and the OFF-REQUEST route —
# `sync-notebooklm-books.py --session-ref <branch> --apply`, FR-040 — projects it
# with no bounds at all, resumably, because the diff is by title + content hash so
# a re-run adds only what is missing. That is what preserves D19 in both
# directions: the external service can neither block the governed write nor be
# left holding a silently truncated projection.
SESSION_SOURCE_COUNT_CAP = 60
SESSION_PROJECTION_BUDGET = 90.0  # seconds, for the WHOLE projection

# manifest / member field order for a human-readable render (schema property order)
_MANIFEST_ORDER = (
    "schema_version", "kind", "repository", "name", "created", "updated",
    "members", "excluded", "seed", "recipe", "action_history", "notebook",
)
_MEMBER_ORDER = ("document", "via", "reason")


class WorkbenchError(Exception):
    """A refused workbench mutation (reason-discipline / vocabulary / binding).
    Raised, never silent — the message is the durable 'why' behind the refusal."""


class ManifestInvalid(Exception):
    """A saved manifest failed the pinned validator (or it could not run)."""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _utcnow() -> str:
    """Wall-clock UTC stamp. A manifest is live session state (NOT deterministic,
    unlike the snapshot), so ordinary wall-clock is correct here."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# A slug is a FILENAME COMPONENT, and a filename component is bounded (T092
# acceptance sweep, defect 2). `lens-save-recipe` derives its default set name
# from the CHECKED KEYWORDS — "lens " + every one of them — so at roughly 13-14
# ordinary corpus keywords the slug passes the 255-byte limit every mainstream
# filesystem enforces, and the verb died with an unhandled `OSError: [Errno 36]
# File name too long` inside the DUPLICATE CHECK: a 500 reading "gate action
# failed; see the server log", from a gated verb, at ordinary usage, before it
# could even refuse. Bounding it here rather than at one call site is deliberate:
# every derived path in this family runs through `slug` (the manifest, the
# notebook alias, the gate-action record's target directory), and a bound applied
# to one of them would have left the others crashing.
#
# 200 characters against a 255-byte limit: the longest suffix any caller appends
# is `.workbench.yaml` (15), and the remaining 40 are headroom for the next
# caller rather than a computed minimum. The alphabet is `[a-z0-9-]`, so
# characters and bytes are the same count.
MAX_SLUG_CHARS = 200

# The truncated form's key half — the same SHAPE `branch_session.notebook_alias`
# uses for the same reason (a readable stem cannot carry injectivity, so the key
# is appended): `<truncated stem>-k<digest>`.
_SLUG_KEY_SEPARATOR = "-k"
_SLUG_KEY_DIGEST_CHARS = 16


def _slug_key_digest(value: str) -> str:
    """A 64-bit FNV-1a digest of the FULL slug, hex, zero-padded.

    NOT sha256, and the difference is a requirement rather than a preference:
    lens-model.js renders the "lands at:" path SYNCHRONOUSLY in the confirm
    dialog and `test_lens.py` pins the two derivations byte-identical, while the
    browser's only built-in sha256 (`crypto.subtle.digest`) is async-only. FNV-1a
    is a few lines of integer arithmetic in both languages and is exactly as
    injective as this needs to be — it disambiguates two long set names that
    truncate to the same stem; it defends nothing against an adversary, and the
    input is the operator's own set name."""
    digest = 0xCBF29CE484222325
    for byte in value.encode("ascii", "ignore"):
        digest = ((digest ^ byte) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{digest:016x}"


def slug(value: str) -> str:
    """A single safe path segment from an untrusted set name (no slashes, no dot
    sequences) — mirrors sync-notebooklm-books.slug_part so a hostile name never
    traverses the workspace — and BOUNDED at `MAX_SLUG_CHARS`, so a
    machine-derived name can never produce a path the filesystem refuses.

    A slug at or under the bound is UNCHANGED, so every existing set keeps the
    path it already has. A longer one is truncated and keyed: the stem stays
    readable and the digest of the whole slug keeps two different long names
    apart, which matters here precisely because the long names are DERIVED (a
    checked-keyword set) and two of them can differ only in their tail.

    Mirrored by `lens-model.js`'s `slug`, locked byte-identical by
    `test_lens.py::test_js_and_python_persistence_constants_agree`."""
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        return "untitled"
    if len(value) <= MAX_SLUG_CHARS:
        return value
    keep = MAX_SLUG_CHARS - len(_SLUG_KEY_SEPARATOR) - _SLUG_KEY_DIGEST_CHARS
    stem = value[:keep].rstrip("-")
    return f"{stem}{_SLUG_KEY_SEPARATOR}{_slug_key_digest(value)}"


def manifest_relpath(name: str) -> str:
    """Repo-relative manifest path under the gitignored workbench prefix."""
    return f"{WORKBENCH_DIR}{slug(name)}.workbench.yaml"


def notebook_alias(name: str) -> str:
    """The scratch-notebook alias for a set (xf-wb-<slug>)."""
    return f"{NOTEBOOK_PREFIX}{slug(name)}"


def content_hash(text: str) -> str:
    """Short content digest for source change-detection (mirrors
    sync-notebooklm-books.sync_book's manifest digest, truncated)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def managed_source_title(path: str, text: str) -> str:
    """A projected source's title: the doc's repo-relative path plus a short
    content hash — the diff key on re-click."""
    return f"{path}{SOURCE_HASH_SEP}{content_hash(text)}"


def parse_managed_source_title(title: str) -> tuple[str, str] | None:
    """(path, hash) parsed from a managed source title, or None for any source
    this action never wrote — so a human-added source is never touched."""
    match = _SOURCE_TITLE_RE.match(title or "")
    return (match.group("path"), match.group("hash")) if match else None


def _reordered(entry: dict, order: Sequence[str]) -> dict:
    out: dict[str, Any] = {}
    for key in order:
        if key in entry and entry[key] is not None:
            out[key] = entry[key]
    # preserve any forward-compatible unknown keys (the schema is additive)
    for key, value in entry.items():
        if key not in out and value is not None:
            out[key] = value
    return out


# --------------------------------------------------------------------------
# manifest engine (T026)
# --------------------------------------------------------------------------

class Workbench:
    """An in-memory `ideation-workbench` manifest with the mutation discipline
    the schema and spec require. `.data` is the plain dict a `save()` renders."""

    def __init__(self, data: dict) -> None:
        self.data = data

    # ---- construction ----
    @classmethod
    def create(
        cls, repository: str, name: str, *,
        seed: str = SEED_ADHOC, cluster_id: str | None = None,
        recipe: dict | None = None, now: str | None = None,
    ) -> "Workbench":
        if seed not in SEED_KINDS:
            raise WorkbenchError(f"unknown seed kind {seed!r} (expected one of {sorted(SEED_KINDS)})")
        if seed == SEED_CLUSTER and not (cluster_id and cluster_id.strip()):
            raise WorkbenchError("a cluster-seeded set requires cluster_id (schema allOf)")
        if seed == SEED_RECIPE and not recipe:
            raise WorkbenchError("a recipe-seeded set requires a recipe block (schema allOf)")
        now = now or _utcnow()
        seed_block: dict[str, Any] = {"kind": seed}
        if seed == SEED_CLUSTER:
            seed_block["cluster_id"] = cluster_id
        data: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "kind": KIND,
            "repository": repository,
            "name": name,
            "created": now,
            "updated": now,
            "members": [],
            "seed": seed_block,
        }
        wb = cls(data)
        if recipe is not None:
            wb.set_recipe(recipe, now=now)
        return wb

    @classmethod
    def load(cls, path: Path | str) -> "Workbench":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("kind") != KIND:
            raise WorkbenchError(f"{path}: not an {KIND} manifest")
        return cls(data)

    # ---- internal ----
    def _touch(self, now: str | None) -> None:
        self.data["updated"] = now or _utcnow()

    # ---- membership (override discipline: overrides are evidence, never silent) ----
    def add_member(self, document: str, via: str, *, reason: str | None = None,
                   now: str | None = None) -> None:
        if via not in VIA_VALUES:
            raise WorkbenchError(f"unknown member via {via!r} (expected one of {sorted(VIA_VALUES)})")
        if via == VIA_MANUAL_INCLUDE and not (reason and reason.strip()):
            raise WorkbenchError(
                "a manual-include member REQUIRES a recorded reason — a human "
                "override is captured evidence, never a silent set edit")
        entry: dict[str, Any] = {"document": document, "via": via}
        if reason and reason.strip():
            entry["reason"] = reason.strip()
        members = [m for m in self.data.get("members", []) if m.get("document") != document]
        members.append(_reordered(entry, _MEMBER_ORDER))
        self.data["members"] = members
        self._touch(now)

    def remove_member(self, document: str, *, now: str | None = None) -> bool:
        """Drop a member (e.g. a source removed from the bound notebook). The
        corpus document is UNTOUCHED — the manifest only drops the reference
        (spec scenario "A source removed from an xf-wb-* notebook"). Returns
        whether a member was present."""
        before = self.data.get("members", [])
        after = [m for m in before if m.get("document") != document]
        self.data["members"] = after
        if len(after) != len(before):
            self._touch(now)
            return True
        return False

    def exclude(self, document: str, reason: str, *, now: str | None = None) -> None:
        if not (reason and reason.strip()):
            raise WorkbenchError(
                "an excluded entry REQUIRES a recorded reason — negative "
                "evidence for a recipe-matching doc the human removed, never silent")
        excluded = [e for e in self.data.get("excluded", []) if e.get("document") != document]
        excluded.append({"document": document, "reason": reason.strip()})
        self.data["excluded"] = excluded
        # an excluded doc is not simultaneously a member
        self.data["members"] = [m for m in self.data.get("members", []) if m.get("document") != document]
        self._touch(now)

    # ---- recipe (D13) ----
    def set_recipe(self, recipe: dict, *, now: str | None = None) -> None:
        checked = recipe.get("checked") or []
        if not checked:
            raise WorkbenchError("a recipe requires at least one checked keyword")
        pinned = recipe.get("pinned") or []
        stray = set(pinned) - set(checked)
        if stray:
            raise WorkbenchError(
                f"recipe pinned keyword(s) {sorted(stray)} are not in checked "
                "(validator rule W1: pinned MUST be a subset of checked)")
        self.data["recipe"] = recipe
        self._touch(now)

    # ---- action history ----
    def record_action(self, action: str, *, at: str | None = None,
                       reference: str | None = None, now: str | None = None) -> dict:
        if action not in ACTION_VALUES:
            raise WorkbenchError(f"unknown action {action!r} (expected one of {sorted(ACTION_VALUES)})")
        # `now` is the moment the action happens: it stamps both `at` (unless an
        # explicit `at` is given) and the manifest's `updated`.
        entry: dict[str, Any] = {"action": action, "at": at or now or _utcnow()}
        if reference and reference.strip():
            entry["reference"] = reference.strip()
        self.data.setdefault("action_history", []).append(entry)
        self._touch(now or entry["at"])
        return entry

    # ---- notebook binding ----
    def bind_notebook(self, alias: str | None = None, *, now: str | None = None) -> str:
        alias = alias or notebook_alias(self.data["name"])
        if not re.fullmatch(r"xf-wb-.+", alias):
            raise WorkbenchError(f"notebook alias {alias!r} must match ^xf-wb-.+$")
        self.data["notebook"] = {"alias": alias}
        self._touch(now)
        return alias

    def notebook_alias(self) -> str | None:
        return (self.data.get("notebook") or {}).get("alias")

    def member_documents(self) -> list[str]:
        return [m["document"] for m in self.data.get("members", []) if m.get("document")]

    # ---- serialization ----
    def to_dict(self) -> dict:
        data = copy.deepcopy(self.data)
        data["members"] = [_reordered(m, _MEMBER_ORDER) for m in data.get("members", [])]
        return _reordered(data, _MANIFEST_ORDER)

    def render(self) -> str:
        body = yaml.safe_dump(self.to_dict(), sort_keys=False,
                              default_flow_style=False, allow_unicode=True)
        header = (
            "# ideation-workbench manifest — GITIGNORED session state (never commit).\n"
            "# Saved by a workbench action through the interactivity boundary; a manifest\n"
            "# in TRACKED content is rejected by the committed-manifest guard.\n"
        )
        return header + body


# --------------------------------------------------------------------------
# persistence + validation
# --------------------------------------------------------------------------

@dataclass
class ManifestValidation:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    validator: Path | None

    def summary(self) -> str:
        if self.validator is None:
            return "validator not found (no reachable openxFactory checkout)"
        tail = (self.stdout or self.stderr).strip().splitlines()
        return tail[-1] if tail else f"returncode={self.returncode}"


def validate_manifest(path: Path | str, *, validator: Path | None = None,
                      strict: bool = False, search_from: Path | None = None) -> ManifestValidation:
    """Validate a written manifest with the pinned validator (single-file mode,
    kind auto-detected). Single-file mode does NOT run the committed-manifest
    guard (that is a repo scan) — so validating a manifest under a tmp/gitignored
    path checks schema + workbench rules cleanly."""
    path = Path(path).resolve()
    validator = validator or find_validator(search_from or path.parent)
    if validator is None:
        return ManifestValidation(False, -1, "", "validator not found", None)
    cmd = [sys.executable, str(validator), str(path)]
    if strict:
        cmd.append("--strict")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return ManifestValidation(proc.returncode == 0, proc.returncode,
                              proc.stdout, proc.stderr, validator)


def save(wb: Workbench, boundary: OutputBoundary, *, relpath: str | None = None,
         validate: bool = False, validator: Path | None = None,
         strict: bool = False) -> Path:
    """Render and write a manifest THROUGH the interactivity boundary (its
    allowlist must include `ideation/workbench/`). With `validate=True` the
    written file is re-checked by the pinned validator and a failure raises
    `ManifestInvalid` — the schema-valid-at-every-write safety net.

    A FAILED VALIDATION LEAVES NOTHING BEHIND (T092 acceptance sweep, defect 4).
    The write used to stand: the route answered 409 "validator not found (no
    reachable openxFactory checkout)", the human read `refused ✕` — and the fully
    populated manifest was on disk anyway, unrecorded (no gate-action record is
    written on a refusal) and POISONING the retry, because the identical recipe
    then refused with "a workbench set named … already exists". A refusal that
    mutates the tree is a direct contradiction of the gate contract this surface
    exists to enforce, and "the schema-valid-at-every-write safety net" was
    write-then-validate, which is not that.

    The validator is a subprocess over a real FILE, so the file has to exist to be
    checked; the write is therefore UNWOUND rather than deferred, and the unwind
    restores what was there — the previous bytes when this save overwrote an
    existing manifest, and nothing at all when it created one. The state after a
    refusal is byte-for-byte the state before it, which is what makes the retry
    work."""
    rel = relpath or manifest_relpath(wb.data["name"])
    target = Path(boundary.root) / rel
    try:
        previous = target.read_bytes() if target.is_file() else None
    except OSError:                     # unreadable: treat as unknown, restore nothing
        previous = None
    written = boundary.write_output(rel, wb.render())
    if validate:
        result = validate_manifest(written, validator=validator, strict=strict,
                                   search_from=written.parent)
        if not result.ok:
            _unwind_write(written, previous)
            raise ManifestInvalid(
                f"{written}: {result.summary()}\n{result.stdout}{result.stderr}"
                .rstrip() +
                "\nnothing was persisted: the manifest this save wrote has been "
                "unwound, so the set name is free and an identical retry is the "
                "whole remedy")
    return written


def _unwind_write(written: Path, previous: bytes | None) -> None:
    """Put `written` back the way the save found it — previous bytes, or gone.

    Best-effort by construction: the unwind runs on a path already refused, and
    an unwind that raised would replace a legible refusal with an unrelated one.
    What it must never do is leave a HALF state, which is why the restore writes
    the previous bytes rather than deleting them."""
    try:
        if previous is None:
            written.unlink(missing_ok=True)
        else:
            written.write_bytes(previous)
    except OSError:                                  # pragma: no cover - defensive
        pass


# --------------------------------------------------------------------------
# committed-manifest detection (code-side mirror of the validator guard)
# --------------------------------------------------------------------------

def committed_manifests(repo: Path | str) -> list[str]:
    """Tracked YAML files that are `ideation-workbench` manifests (outside the
    reference `examples/` tree). Mirrors the pinned validator's committed-manifest
    guard: a saved manifest is session state and belongs under gitignored
    `ideation/workbench/`. Returns [] when git is unavailable."""
    repo = Path(repo)
    try:
        out = subprocess.run(["git", "-C", str(repo), "ls-files", "*.yaml", "*.yml"],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, OSError):  # FileNotFoundError is an OSError
        return []
    offenders: list[str] = []
    for rel in (ln for ln in out.stdout.splitlines() if ln.strip()):
        if rel.startswith(("examples/", "contracts/schemas/")):
            continue
        try:
            doc = yaml.safe_load((repo / rel).read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            continue
        if isinstance(doc, dict) and doc.get("kind") == KIND:
            offenders.append(rel)
    return offenders


def assert_no_committed_manifests(repo: Path | str) -> None:
    offenders = committed_manifests(repo)
    if offenders:
        raise WorkbenchError(
            "workbench manifest(s) committed/tracked (session state must stay "
            f"under gitignored {WORKBENCH_DIR}): {offenders}")


# --------------------------------------------------------------------------
# scratch-notebook adapter (T026) — thin, fully mockable, degrades gracefully
# --------------------------------------------------------------------------

def _default_runner(*args: str, parse: bool = True, timeout: float = NLM_TIMEOUT):
    """The real `nlm(*args)` subprocess call, modelled on
    sync-notebooklm-books.nlm. Raises on a non-zero exit, a missing binary, or a
    timeout — the adapter catches that and degrades. A `timeout` is enforced so a
    stuck `nlm` never hangs the loopback action. Never called by tests (they
    inject a fake runner)."""
    import json
    try:
        res = subprocess.run(["nlm", *args], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"nlm {' '.join(args[:3])}... timed out after {timeout}s") from exc
    if res.returncode != 0:
        raise RuntimeError(f"nlm {' '.join(args[:3])}...: {res.stderr.strip()[:300]}")
    if not parse:
        return res.stdout
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return res.stdout


@dataclass
class NotebookResult:
    """Outcome of a notebook action. `skipped` marks the graceful-degradation
    path (nlm absent or errored); `ok` marks a real success."""
    action: str
    ok: bool
    skipped: bool
    detail: str
    alias: str | None = None
    notebook_id: str | None = None


@dataclass(frozen=True)
class NotebookListing:
    """A listing that knows whether it FAILED (PR #49 review finding 13).

    `list_titled` / `list_sources` returned a bare `list` and collapsed an ERRORED
    listing into an EMPTY one, so absence of evidence was read as evidence of
    absence: a failed `nlm notebook list` made `_delete_titled` report "already
    gone" for a notebook that plainly existed, a failed `nlm source list` made
    `_sync_sources` diff against nothing and re-add every source, and
    `_ensure_notebook` would have CREATED a second notebook titled the same as
    the one it could not see.

    `ok=False` means "could not determine", which is a third answer and must stay
    distinguishable from "determined: nothing". `rows` is empty in that case and
    `detail` carries the adapter's own reason, verbatim, for the notice the human
    reads (FR-042)."""

    ok: bool
    rows: tuple[dict, ...] = ()
    detail: str = ""


def _notebook_title(nb: dict) -> str | None:
    if not isinstance(nb, dict):
        return None
    return nb.get("title") or nb.get("name") or nb.get("emoji_title")


def _notebook_id(nb: dict) -> str | None:
    if not isinstance(nb, dict):
        return None
    return nb.get("id") or nb.get("notebook_id") or nb.get("project_id")


def _created_notebook_id(out: Any) -> str | None:
    """The id a `notebook create` echoed, under either CLI shape: a JSON
    object (the pre-0.5.26 `--json` answer, kept for a runner that still
    parses one) or 0.5.26's plain text, which prints an `ID: <uuid>` line.
    None when neither is readable — the caller resolves from a fresh list."""
    if isinstance(out, dict):
        return _notebook_id(out)
    m = re.search(r"\bID:\s*([0-9A-Za-z-]+)", str(out or ""))
    return m.group(1) if m else None


def _source_id(source: dict) -> str | None:
    if not isinstance(source, dict):
        return None
    return source.get("id") or source.get("source_id")


def _notebook_url(nb: Any, notebook_id: str | None) -> str | None:
    """A shareable notebook URL from `nlm notebook get --json`: an explicit url
    field when present, else the deterministic notebook URL built from its id."""
    nid = notebook_id
    if isinstance(nb, dict):
        for key in _NOTEBOOK_URL_KEYS:
            value = nb.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        nid = _notebook_id(nb) or notebook_id
    return f"{NOTEBOOK_URL_BASE}{nid}" if nid else None


def _rows_of(out: Any, key: str) -> list[dict]:
    """The row dicts of an nlm JSON payload — either a bare list or a
    `{<key>: [...]}` wrapper. Anything else (an error string, None) is empty."""
    if isinstance(out, list):
        rows = out
    elif isinstance(out, dict):
        rows = out.get(key)
    else:
        rows = None
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _require_prefix(alias: str, prefix: str, kind: str) -> str:
    """Refuse an alias from the WRONG managed namespace (FR-038, D11).

    The refusal is the enforcement: a session operation handed an `xf-wb-` alias
    would let a session end delete a reference set, and a scratch operation
    handed an `xf-session-` alias would let the sweep take a live session. Both
    are the same defect from opposite sides, so both raise."""
    if not str(alias or "").startswith(prefix):
        raise WorkbenchError(
            f"{kind} notebook alias {alias!r} must start with {prefix!r} — the "
            f"{NOTEBOOK_PREFIX!r} and {SESSION_NOTEBOOK_PREFIX!r} namespaces are "
            "disjoint and no operation crosses between them")
    return alias


def _require_key_derived(alias: str) -> str:
    """Refuse a session alias that was not DERIVED from a (repository, branch) key
    (PR #49 hardening item 2's residual, wave 2).

    The hardening removed the hazard at the session SEAM —
    `branch_session.retire_session_notebook` takes no alias argument at all and
    derives the title itself — but `retire` remained an unguarded title-keyed
    delete on a SHARED account: any caller written directly against
    `adapter.retire("<string>")` could name a neighbour's notebook, and the only
    guard was a prefix. A prefix is not an owner.

    The DERIVATION's own shape is the guard that a prefix cannot be: every alias
    `branch_session.notebook_alias` produces ends in
    `-k<12 lowercase hex>` — `notebook_key_digest`, the half that makes the
    alias injective (FR-037, C11). A hand-built or STALE pre-digest spelling
    (`xf-session-openxfactory-victim`, the readable half alone) therefore cannot
    be handed to a delete, which is the exact title the wave-2 replay pass showed
    surviving on a shared account beside a live session's notebook. It is still
    not proof of ownership — nothing at this layer can be — but a caller now has
    to hold a value only the key derivation produces.

    Transcribed rather than imported, like `SESSION_NOTEBOOK_PREFIX` above, so
    this module's import graph stays flat; a test pins the shape against
    `branch_session.notebook_alias`'s real output."""
    if not _SESSION_KEY_SUFFIX.search(str(alias or "")):
        raise WorkbenchError(
            f"session notebook alias {alias!r} is not KEY-DERIVED: a session "
            f"alias ends in {SESSION_KEY_SEPARATOR}<12 hex> "
            "(`branch_session.notebook_key_digest`, the half that makes the alias "
            "injective), and a delete on a SHARED account may only name a title "
            "the session's own (repository, branch) key produces. Derive it with "
            "`branch_session.notebook_alias(repository, branch)` — or, better, "
            "call `branch_session.retire_session_notebook`, which takes the key "
            "and no title at all (FR-037, C11)")
    return alias


def managed_notebook_prefix(alias: str) -> str:
    """Which managed namespace `alias` belongs to, or a refusal. Used by the
    shared projection path so ONE mechanism serves both namespaces."""
    for prefix in MANAGED_NOTEBOOK_PREFIXES:
        if str(alias or "").startswith(prefix):
            return prefix
    raise WorkbenchError(
        f"notebook alias {alias!r} is in neither managed namespace "
        f"({NOTEBOOK_PREFIX!r} for reference sets, {SESSION_NOTEBOOK_PREFIX!r} "
        "for branch sessions), so nothing here creates, syncs, or deletes it")


def session_documents(worktree: Path | str, *, repository: str | None = None,
                      max_bytes: int = _MAX_SESSION_SOURCE_BYTES
                      ) -> list[tuple[str, str]]:
    """The session notebook's source set, read FROM the session WORKTREE
    (FR-036, FR-039; T073).

    Membership is the corpus's own rule, not a second one: `doc_health.corpus`'s
    governed roots (`contracts/ docs/ examples/ ideation/ templates/`, `tests/`
    and `installs/` never scanned) plus a declared `Status:` header — the same
    "membership follows Status" the lifecycle books use. Returns
    (worktree-relative posix path, text) pairs in the shape `project_documents`
    consumes, so create-at-open and the `--session-ref` re-sync project exactly
    the same set.

    Reading the WORKTREE is the whole point: the session's documents live on an
    unmerged branch, so a scan of the served checkout would show the human
    `main`'s copies of their own drafts."""
    from doc_health import corpus            # lazy: keeps this module's graph flat

    root = Path(worktree)
    docs = corpus.load_docs(repository or root.name, root)
    return [(doc.path, doc.text) for doc in docs
            if doc.status and len(doc.text.encode("utf-8")) <= max_bytes]


class NotebookAdapter:
    """Fully-mockable `nlm` adapter for `xf-wb-*` scratch notebooks.

    Construction is injectable end-to-end so tests never call the real CLI:
      * `runner(*args, parse=True)` — the nlm subprocess shape (default: real).
      * `available` — force the availability verdict (default: probe
        `shutil.which("nlm")`).
    Every action returns a `NotebookResult`; an nlm error or an absent binary
    degrades to `skipped=True` rather than raising to the caller.
    """

    def __init__(self, runner: Callable[..., Any] | None = None, *,
                 available: bool | None = None) -> None:
        self.runner = runner or _default_runner
        self._available = available

    def available(self) -> bool:
        if self._available is not None:
            return self._available
        return shutil.which("nlm") is not None

    def _unavailable(self, action: str, alias: str | None) -> NotebookResult:
        return NotebookResult(action, ok=False, skipped=True,
                              detail="nlm unavailable — notebook action skipped, not blocked",
                              alias=alias)

    def create(self, alias: str) -> NotebookResult:
        """Create a scratch notebook titled `alias` (xf-wb-<name>)."""
        _require_prefix(alias, NOTEBOOK_PREFIX, "scratch")
        return self._create_titled(alias)

    def _create_titled(self, alias: str) -> NotebookResult:
        """The create itself, prefix-guard already applied by the caller — the
        one place `nlm notebook create` is spoken, shared by the scratch and the
        session namespace so neither can drift in its degradation behaviour.

        Spoken WITHOUT `--json`: nlm 0.5.26 REJECTS that flag on `create`
        (every other call form this adapter uses still carries it), which is
        the drift the T092 re-run hit live on 2026-08-04 — the at-open session
        notebook degraded on every create until the FR-040 sync route was
        driven by hand. The plain form is in both CLI generations' vocabulary;
        the id is taken from whatever shape the CLI answered, and a create
        that echoed no readable id is NOT a failure — `_ensure_notebook`
        resolves it from a fresh title listing."""
        if not self.available():
            return self._unavailable("create", alias)
        try:
            out = self.runner("notebook", "create", alias)
        except Exception as exc:  # noqa: BLE001
            # degrade, never crash the caller
            return NotebookResult("create", ok=False, skipped=True,
                                  detail=f"nlm error: {exc}", alias=alias)
        return NotebookResult("create", ok=True, skipped=False, detail="created",
                              alias=alias, notebook_id=_created_notebook_id(out))

    def list_titled_result(self, prefix: str) -> NotebookListing:
        """Notebooks whose title starts with `prefix`, as a listing that reports
        whether it could be read at all (PR #49 review finding 13).

        The prefix is the ONLY candidacy rule anywhere in this module, which is
        what makes each namespace immune to the other's operations (FR-038,
        research R8)."""
        if not self.available():
            return NotebookListing(
                ok=False,
                detail="nlm unavailable — the notebook list could not be read")
        try:
            out = self.runner("notebook", "list", "--json")
        except Exception as exc:  # noqa: BLE001 - reported, never raised
            return NotebookListing(ok=False, detail=f"nlm error: {exc}")
        return NotebookListing(ok=True, rows=tuple(
            nb for nb in _rows_of(out, "notebooks")
            if (_notebook_title(nb) or "").startswith(prefix)))

    def list_titled(self, prefix: str) -> list[dict]:
        """The rows of `list_titled_result`, empty when it could not be read.

        Kept for the READ-ONLY callers that legitimately treat "cannot tell" and
        "nothing" alike; every caller that goes on to DELETE or CREATE something
        must use `list_titled_result` instead, because for those two the
        difference decides whether the account is mutated."""
        return list(self.list_titled_result(prefix).rows)

    def list_scratch(self) -> list[dict]:
        """Notebooks whose title matches the `xf-wb-*` scratch convention — the
        sweep's candidate set, and the reason a session notebook can never be a
        candidate (FR-038)."""
        return self.list_titled(NOTEBOOK_PREFIX)

    def list_scratch_result(self) -> NotebookListing:
        return self.list_titled_result(NOTEBOOK_PREFIX)

    def list_sessions(self) -> list[dict]:
        """Notebooks whose title matches the `xf-session-*` convention. Never a
        sweep candidate set: a session notebook's life is bound to its SESSION,
        which ends by retiring it (FR-036, D16), not by a sweep."""
        return self.list_titled(SESSION_NOTEBOOK_PREFIX)

    def list_sessions_result(self) -> NotebookListing:
        return self.list_titled_result(SESSION_NOTEBOOK_PREFIX)

    # ---- session operations (T073; contracts/session-ports.md) ----
    def create_session(self, alias: str, documents: Sequence[tuple[str, str]] = ()
                       ) -> Any:
        """Create the SESSION notebook `alias` and sync `documents` into it.

        The session twin of `create`, with its own prefix guard: an `xf-wb-`
        alias handed here is a REFUSAL, never a courtesy, because the two
        namespaces exist precisely so one mechanism cannot take the other's
        notebooks (FR-038, D11). With documents it returns a `ProjectionResult`
        (create-or-rebind plus the title+content-hash source diff — the notebook
        itself is the store, so a session needs NO manifest, which is what keeps
        `_out_of_scope_workbench_dirs` from silently disabling the sweep,
        research R8); with none it returns the `NotebookResult` of the create.
        Degrades, never raises: a full quota is `ok=False` and the CALLER decides
        what that means (FR-042, D19).

        THIS IS THE BOUNDED ROUTE (finding 21). A session notebook is created from
        inside the `create-document` gate action, so the projection here carries the
        aggregate bounds — one source per governed document in the worktree is 176
        sequential subprocesses on the real corpus, and a governed write must not
        wait on that. The remainder is reported as `sources_deferred` and completed
        off the request path by `sync-notebooklm-books.py --session-ref`, which
        calls `project_documents` directly and unbounded."""
        _require_prefix(alias, SESSION_NOTEBOOK_PREFIX, "session")
        if documents:
            return project_documents(self, alias, list(documents),
                                     max_sources=SESSION_SOURCE_COUNT_CAP,
                                     budget=SESSION_PROJECTION_BUDGET)
        return self._create_titled(alias)

    def retire(self, alias: str) -> NotebookResult:
        """Retire the SESSION notebook `alias` — the ending both routes take
        (FR-021, D16). RETIRED, never re-pointed at `main`: there is no surviving
        post-session notebook and no route to one in this feature (FR-036). An
        `xf-wb-` alias is refused here for the same reason `create_session`
        refuses one, and an alias that is not KEY-DERIVED is refused too (PR #49
        hardening item 2's residual, wave 2)."""
        _require_prefix(alias, SESSION_NOTEBOOK_PREFIX, "session")
        _require_key_derived(alias)
        return self._delete_titled(alias, "retire", self.list_sessions_result(),
                                   missing_ok=False)

    def delete(self, alias: str) -> NotebookResult:
        """Delete the scratch notebook titled `alias` (resolved to an id via the
        list). A missing notebook is a benign no-op."""
        return self._delete_titled(alias, "delete", None)

    def _delete_titled(self, alias: str, action: str,
                       listing: NotebookListing | None, *,
                       missing_ok: bool = True) -> NotebookResult:
        """Delete the notebook titled EXACTLY `alias` within one namespace.

        A listing that could not be read is "could not determine", never "already
        gone" (PR #49 review finding 13): reporting a deletion nobody performed
        leaves a notebook holding a session's unmerged branch documents alive on
        the SHARED account while the ending's response says it was retired.

        `missing_ok` says whether "no notebook by this title" is a SUCCESS. For the
        scratch `delete` it is — the sweep's job is that the title is gone, however
        it got that way. For a session `retire` it is NOT (PR #49 review finding 8,
        leg b, wave 2): the ending derives the alias from the session's
        `(repository, branch)` key, and the whole point of the derivation is that a
        DIFFERENT key derives a different alias. Reported as `ok=True … (already
        gone)`, an ending whose key had drifted — `create-document --repository
        MedxFactory` in an `openxFactory` checkout, then an `abandon-session` that
        re-derived `openxFactory` — printed `torn down: worktree, registry-entry,
        notebook` at exit 0 while the real notebook survived on the SHARED account
        holding that session's unmerged documents (reproduced by the wave-2 replay
        pass). An absent title is now `ok=False, skipped=True`, which
        `teardown_session` turns into "the session notebook … was NOT retired: …"
        and keeps out of `torn_down` — the ending still completes (a notebook never
        blocks one, FR-042), it simply stops claiming something it did not do."""
        if not self.available():
            return self._unavailable(action, alias)
        if listing is None:
            listing = self.list_scratch_result()
        if not listing.ok:
            return NotebookResult(
                action, ok=False, skipped=True, alias=alias,
                detail=f"could not determine whether the notebook {alias!r} "
                       f"exists, so nothing was deleted: {listing.detail}")
        match = next((nb for nb in listing.rows
                      if _notebook_title(nb) == alias), None)
        if match is None and missing_ok:
            return NotebookResult(action, ok=True, skipped=False,
                                  detail=f"no notebook titled {alias!r} "
                                         "(already gone)", alias=alias)
        if match is None:
            others = sorted(t for t in (_notebook_title(nb) for nb in listing.rows)
                            if t and t != alias)
            return NotebookResult(
                action, ok=False, skipped=True, alias=alias,
                detail=(f"no notebook titled {alias!r} exists, so nothing was "
                        f"{action}d. This alias is DERIVED from the session's "
                        "(repository, branch) key, so a session opened under a "
                        "different repository key (a `--repository` that differs "
                        "between the create and the ending) has a notebook under "
                        "a different title, which is then ORPHANED on the shared "
                        "account and must be retired by hand"
                        + (f". The account holds {len(others)} other session "
                           f"notebook(s): {', '.join(others)}" if others else "")))
        nb_id = _notebook_id(match)
        try:
            self.runner("notebook", "delete", nb_id, "--confirm", parse=False)
        except Exception as exc:  # noqa: BLE001
            return NotebookResult(action, ok=False, skipped=True,
                                  detail=f"nlm error: {exc}", alias=alias, notebook_id=nb_id)
        return NotebookResult(action, ok=True, skipped=False, detail="deleted",
                              alias=alias, notebook_id=nb_id)

    # ---- source projection (v2 tile action): list/add/delete + notebook url ----
    def list_sources_result(self, notebook_id: str | None) -> NotebookListing:
        """The notebook's sources, as a listing that reports whether it could be
        read (PR #49 review finding 13). An unreadable source list is what the
        projection must NOT diff against: doing so re-adds every source."""
        if not self.available():
            return NotebookListing(
                ok=False,
                detail="nlm unavailable — the source list could not be read")
        if not notebook_id:
            return NotebookListing(
                ok=False, detail="no notebook id, so no sources could be read")
        try:
            out = self.runner("source", "list", notebook_id, "--json")
        except Exception as exc:  # noqa: BLE001 - reported, never raised
            return NotebookListing(ok=False, detail=f"nlm error: {exc}")
        return NotebookListing(ok=True, rows=tuple(_rows_of(out, "sources")))

    def list_sources(self, notebook_id: str | None) -> list[dict]:
        """The rows of `list_sources_result`, empty when unreadable — for the
        read-only callers only (see `list_titled`)."""
        return list(self.list_sources_result(notebook_id).rows)

    def add_source(self, notebook_id: str, title: str, text: str) -> NotebookResult:
        """Add a titled text source to a notebook."""
        if not self.available():
            return self._unavailable("add-source", None)
        try:
            self.runner("source", "add", notebook_id, "--text", text, "--title", title, parse=False)
        except Exception as exc:  # noqa: BLE001
            return NotebookResult("add-source", ok=False, skipped=True,
                                  detail=f"nlm error: {exc}", notebook_id=notebook_id)
        return NotebookResult("add-source", ok=True, skipped=False, detail="added",
                              notebook_id=notebook_id)

    def delete_source(self, source_id: str) -> NotebookResult:
        """Delete a source by id (a stale/replaced projected source)."""
        if not self.available() or not source_id:
            return self._unavailable("delete-source", None)
        try:
            self.runner("source", "delete", source_id, "--confirm", parse=False)
        except Exception as exc:  # noqa: BLE001
            return NotebookResult("delete-source", ok=False, skipped=True, detail=f"nlm error: {exc}")
        return NotebookResult("delete-source", ok=True, skipped=False, detail="deleted")

    def notebook_url(self, notebook_id: str | None) -> str | None:
        """The shareable URL for a notebook (`nlm notebook get <id> --json`),
        or None when nlm is unavailable/errors."""
        if not self.available() or not notebook_id:
            return None
        try:
            out = self.runner("notebook", "get", notebook_id, "--json")
        except Exception:  # noqa: BLE001
            return None
        return _notebook_url(out, notebook_id)


@dataclass
class SweepResult:
    skipped: bool
    detail: str
    deleted: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)


def live_notebook_aliases(repo_root: Path | str, *, workbench_dir: str = WORKBENCH_DIR) -> set[str]:
    """Notebook aliases still bound by a live manifest under `ideation/workbench/`."""
    wb_dir = Path(repo_root) / workbench_dir
    aliases: set[str] = set()
    if not wb_dir.is_dir():
        return aliases
    for path in sorted(wb_dir.glob("*.workbench.yaml")):
        try:
            wb = Workbench.load(path)
        except (WorkbenchError, OSError):
            continue
        alias = wb.notebook_alias()
        if alias:
            aliases.add(alias)
    return aliases


def orphan_sweep(repo_root: Path | str, adapter: NotebookAdapter, *,
                 workbench_dir: str = WORKBENCH_DIR) -> SweepResult:
    """Delete every `xf-wb-*` notebook that NO live manifest binds — the deletion
    of a manifest removes its bound notebook on the next sweep (spec scenario "A
    workbench manifest is deleted").

    OUT OF SCOPE (noted for the aggregation lane): wiring this into the real
    `scripts/sync-notebooklm-books.py` nightly/sync pass. This function is the
    reusable sweep primitive; the sync script should call it with a real
    `NotebookAdapter` and the aggregation checkout root."""
    live = live_notebook_aliases(repo_root, workbench_dir=workbench_dir)
    if not adapter.available():
        return SweepResult(skipped=True, detail="nlm unavailable — orphan sweep skipped, not blocked")
    listing = adapter.list_scratch_result()
    if not listing.ok:
        # "could not read the account" is not "the account holds nothing"
        # (PR #49 review finding 13): a sweep that reported `swept 0 orphan(s)`
        # over an unreadable list would read as a clean account.
        return SweepResult(skipped=True,
                           detail=f"the notebook list could not be read, so "
                                  f"nothing was swept: {listing.detail}")
    deleted: list[str] = []
    kept: list[str] = []
    for nb in listing.rows:
        title = _notebook_title(nb)
        if not title:
            continue
        if title in live:
            kept.append(title)
            continue
        result = adapter.delete(title)
        (deleted if result.ok and not result.skipped else kept).append(title)
    return SweepResult(skipped=False, detail=f"swept {len(deleted)} orphan(s)",
                       deleted=deleted, kept=kept)


# --------------------------------------------------------------------------
# document projection (v2 tile action): create-or-rebind an xf-wb-* notebook
# and sync a doc set as titled text sources, diffing by title + content hash
# --------------------------------------------------------------------------

@dataclass
class ProjectionResult:
    """Outcome of projecting a doc set into an `xf-wb-*` notebook. `skipped`
    marks the graceful-degradation path (nlm absent/errored); `ok` a real
    success. `created` distinguishes a fresh notebook from a rebind."""
    ok: bool
    skipped: bool
    detail: str
    alias: str
    notebook_id: str | None = None
    url: str | None = None
    created: bool = False
    sources_total: int = 0
    sources_added: int = 0
    sources_removed: int = 0
    # DEFERRED by an aggregate bound (finding 21): desired sources this projection
    # deliberately did not attempt, so the caller can say so. Zero on the
    # unbounded (off-request) route, and never a failure — the sources that were
    # projected are projected, and the rest are one re-sync away.
    sources_deferred: int = 0


def _ensure_notebook(adapter: NotebookAdapter, alias: str,
                     prefix: str = NOTEBOOK_PREFIX
                     ) -> tuple[str | None, bool, NotebookResult | None]:
    """Resolve the managed notebook titled `alias`, creating it when absent.
    Returns (notebook_id, created, failure) — `failure` is a NotebookResult the
    caller degrades on.

    `prefix` selects the namespace: the listing and the create both stay inside
    it, so a session create can never rebind a reference set and vice versa.

    A listing that could not be READ is a failure, not "absent" (PR #49 review
    finding 13). Treating it as absent would create a SECOND notebook titled the
    same as the one the account already holds — the duplicate the title-keyed
    diff store cannot then tell apart."""
    def resolve() -> tuple[dict | None, NotebookResult | None]:
        listing = adapter.list_titled_result(prefix)
        if not listing.ok:
            return None, NotebookResult(
                "resolve", ok=False, skipped=True, alias=alias,
                detail=f"the notebook list could not be read, so nothing was "
                       f"created or synced: {listing.detail}")
        return next((nb for nb in listing.rows
                     if _notebook_title(nb) == alias), None), None

    match, failure = resolve()
    if failure is not None:
        return None, False, failure
    if match is not None:
        return _notebook_id(match), False, None
    result = (adapter.create(alias) if prefix == NOTEBOOK_PREFIX
              else adapter.create_session(alias))
    if not result.ok:
        return None, False, result
    notebook_id = result.notebook_id
    if not notebook_id:  # create did not echo an id — resolve it from a fresh list
        match, failure = resolve()
        if failure is not None:
            return None, True, failure
        notebook_id = _notebook_id(match) if match else None
    return notebook_id, True, None


def _existing_by_path(sources: Sequence[dict]) -> dict[str, list[tuple[str | None, str]]]:
    """Managed sources indexed path -> [(source_id, hash)]. Unmanaged sources
    (no `path  #hash` title) are ignored so a human-added source is never touched."""
    by_path: dict[str, list[tuple[str | None, str]]] = {}
    for source in sources:
        parsed = parse_managed_source_title(_notebook_title(source) or "")
        if parsed is None:
            continue
        path, digest = parsed
        by_path.setdefault(path, []).append((_source_id(source), digest))
    return by_path


# Every source operation below counts OUTCOMES, never intentions (PR #49 review
# finding 13). `_delete_sources` used to increment `removed` for every id it
# passed to `delete_source` and `_sync_one` returned `1` added whatever
# `add_source` answered, so a half-failed replacement — prior source deleted, new
# one not added — reported `+1/-1 changed` over a notebook that was now EMPTY.

def _succeeded(result: Any) -> bool:
    """Did the adapter really do it? `ok and not skipped` is the adapter's own
    contract for a real success (`NotebookResult`), and a caller that ignores it
    is reporting that it INVOKED something, not that it worked."""
    return bool(getattr(result, "ok", False)) and not bool(
        getattr(result, "skipped", False))


def _delete_sources(adapter: NotebookAdapter,
                    entries: Sequence[tuple[str | None, str]]
                    ) -> tuple[int, list[str]]:
    """Returns (really removed, failures)."""
    removed = 0
    failures: list[str] = []
    for source_id, _digest in entries:
        if not source_id:
            failures.append("a managed source carries no id and could not be "
                            "removed")
            continue
        result = adapter.delete_source(source_id)
        if _succeeded(result):
            removed += 1
        else:
            failures.append(f"source {source_id} was not removed "
                            f"({getattr(result, 'detail', 'no detail')})")
    return removed, failures


def _sync_one(adapter: NotebookAdapter, notebook_id: str, title: str, text: str,
              want_hash: str, current: Sequence[tuple[str | None, str]]
              ) -> tuple[int, int, list[str]]:
    """Sync a single desired path: a content-hash match is a NO-OP (only stale
    duplicates for that path are pruned); otherwise replace with the new source.
    Returns (really added, really removed, failures)."""
    if any(digest == want_hash for _sid, digest in current):
        stale = [(sid, digest) for sid, digest in current if digest != want_hash]
        removed, failures = _delete_sources(adapter, stale)
        return 0, removed, failures
    removed, failures = _delete_sources(adapter, current)
    result = adapter.add_source(notebook_id, title, text)
    if not _succeeded(result):
        failures.append(f"{title!r} was not added "
                        f"({getattr(result, 'detail', 'no detail')})")
        return 0, removed, failures
    return 1, removed, failures


def _sync_sources(adapter: NotebookAdapter, notebook_id: str,
                  desired: dict[str, tuple[str, str, str]],
                  existing_sources: Sequence[dict], *,
                  max_sources: int | None = None,
                  deadline: float | None = None
                  ) -> tuple[int, int, list[str], int]:
    """Add/replace only changed sources (title + content-hash diff) and drop
    managed sources whose path left the set. Returns
    (added, removed, failures, deferred) — the first three counted from what the
    adapter actually reported.

    `max_sources` and `deadline` are the aggregate bounds (finding 21). Both DEFER
    rather than fail: the paths not attempted are counted and left ALONE. Which
    ones they are is deterministic — sorted by path — so two runs over one corpus
    project the same subset, and the deadline is consulted BEFORE each `_sync_one`
    so no adapter call is abandoned half-way.

    THE PRUNE LOOP STILL READS THE FULL `desired`. A deferred path has not "left
    the set", and treating it as if it had would DELETE the source a previous
    unbounded re-sync added — a bounded open and an unbounded re-sync would then
    take turns undoing each other."""
    by_path = _existing_by_path(existing_sources)
    added = removed = deferred = 0
    failures: list[str] = []
    ordered = sorted(desired.items())
    attempted = ordered if max_sources is None else ordered[:max_sources]
    deferred = len(ordered) - len(attempted)
    for index, (path, (title, text, want_hash)) in enumerate(attempted):
        if deadline is not None and time.monotonic() >= deadline:
            # the budget is spent: everything left, INCLUDING this path, is deferred
            deferred += len(attempted) - index
            break
        one_added, one_removed, one_failed = _sync_one(
            adapter, notebook_id, title, text, want_hash, by_path.get(path, []))
        added += one_added
        removed += one_removed
        failures.extend(one_failed)
    for path, entries in by_path.items():
        if path not in desired:
            one_removed, one_failed = _delete_sources(adapter, entries)
            removed += one_removed
            failures.extend(one_failed)
    return added, removed, failures, deferred


def project_documents(adapter: NotebookAdapter, alias: str,
                      documents: Sequence[tuple[str, str]], *,
                      max_sources: int | None = None,
                      budget: float | None = None) -> ProjectionResult:
    """Create-or-rebind the managed notebook `alias` and sync `documents`
    (a sequence of (relative_path, text)) as titled text sources, diffing by
    title + content hash so a re-click with unchanged content is a no-op.

    ONE mechanism serves both managed namespaces (T073): `xf-wb-*` reference sets
    project a tile's doc set, `xf-session-*` notebooks project a session
    WORKTREE's `session_documents`. The alias itself selects the namespace, and an
    alias in neither is refused — the notebook is the diff store in both cases, so
    neither needs any on-disk manifest.

    Degrades gracefully: an unavailable or errored `nlm` yields `skipped=True`;
    it never raises to the caller. Degrading is not the same as SUCCEEDING,
    though (PR #49 review finding 13): `ok=True` was returned unconditionally
    once the sync loop had run, so a projection that deleted the prior source and
    failed to add its replacement reported `+1/-0 changed` over an EMPTY notebook
    and suppressed the FR-042 notice its caller would otherwise have shown.

    BOUNDED OR NOT IS THE CALLER'S CALL (finding 21). `max_sources` / `budget`
    default to NONE — unbounded, which is what the human-invoked routes want (the
    tile action, and `sync-notebooklm-books.py --session-ref`, both of which are a
    human waiting at their own terminal). `NotebookAdapter.create_session` supplies
    the session bounds, because that one runs inside a gate route where an
    unbounded projection holds a governed write open. The deferred remainder is
    REPORTED, never silently dropped, and the unbounded route completes it."""
    started = time.monotonic()
    prefix = managed_notebook_prefix(alias)
    if not adapter.available():
        return ProjectionResult(ok=False, skipped=True, alias=alias,
                                detail="nlm unavailable — notebook action skipped, not blocked")
    notebook_id, created, failure = _ensure_notebook(adapter, alias, prefix)
    if failure is not None:
        return ProjectionResult(ok=False, skipped=failure.skipped, alias=alias,
                                created=created, detail=failure.detail)
    if not notebook_id:
        return ProjectionResult(ok=False, skipped=True, alias=alias, created=created,
                                detail="could not resolve the notebook id after create")
    desired = {path: (managed_source_title(path, text), text, content_hash(text))
               for path, text in documents}
    # The CURRENT state is what the diff is computed against, so an unreadable
    # one is a refusal to sync rather than a diff against nothing (which would
    # re-add every source the notebook already holds).
    current = adapter.list_sources_result(notebook_id)
    if not current.ok:
        return ProjectionResult(
            ok=False, skipped=True, alias=alias, notebook_id=notebook_id,
            created=created, sources_total=len(desired),
            detail=f"the notebook's current sources could not be read, so "
                   f"nothing was synced: {current.detail}")
    added, removed, failures, deferred = _sync_sources(
        adapter, notebook_id, desired, current.rows, max_sources=max_sources,
        deadline=None if budget is None else started + budget)
    detail = f"{len(desired)} source(s); +{added}/-{removed} changed"
    if deferred:
        detail = (f"{detail}; {deferred} source(s) DEFERRED by this projection's "
                  f"aggregate bound (at most {max_sources} source(s) and "
                  f"{budget}s of wall clock, so an external service cannot hold a "
                  f"governed write open — D19): re-sync to project the remainder")
    if failures:
        detail = f"{detail}; {len(failures)} operation(s) FAILED: " \
                 f"{'; '.join(failures)}"
    return ProjectionResult(
        ok=not failures, skipped=False, alias=alias, notebook_id=notebook_id,
        url=adapter.notebook_url(notebook_id), created=created,
        sources_total=len(desired), sources_added=added, sources_removed=removed,
        sources_deferred=deferred, detail=detail)


# --------------------------------------------------------------------------
# bounded actions (T027)
# --------------------------------------------------------------------------

@dataclass
class ActionResult:
    """Outcome of a bounded workbench action. `status` is one of
    `completed | not-available | skipped`; `reference` is the optional
    job/artifact ref recorded in `action_history`."""
    action: str
    status: str
    detail: str = ""
    reference: str | None = None
    findings: list = field(default_factory=list)

    @property
    def completed(self) -> bool:
        return self.status == "completed"


READINESS_NOT_AVAILABLE_REF = "readiness/not-available"


def run_readiness(wb: Workbench | None = None, *, now: str | None = None) -> ActionResult:
    """Readiness scoring STUB. The readiness panel is a SEPARATE change
    (`add-ideation-cross-reference-readiness`, not yet landed): this action
    emits a RECORDED not-available result and NEVER fabricates a score. When a
    manifest is supplied the not-available action is appended to
    `action_history` so the attempt is auditable, not silent."""
    result = ActionResult(
        ACTION_READINESS, "not-available", reference=READINESS_NOT_AVAILABLE_REF,
        detail="readiness scoring lands with add-ideation-cross-reference-readiness; "
               "no score emitted")
    if wb is not None:
        wb.record_action(ACTION_READINESS, reference=result.reference, now=now)
    return result


# doc-health families safe to scope to a doc SUBSET: pure per-document checks
# that need neither the full corpus nor git (verified against
# scripts/doc_health/families.py — both read only `ctx.docs`).
DEFAULT_SCOPED_FAMILIES = ("status-validity", "tag-hygiene")


def run_scoped_doc_health(
    repo_root: Path | str, documents: Sequence[str], *,
    repository: str | None = None, as_of: date | None = None,
    families: Sequence[str] = DEFAULT_SCOPED_FAMILIES,
    wb: Workbench | None = None, reference: str | None = None,
    now: str | None = None,
) -> ActionResult:
    """Run the REAL in-repo doc-health machinery IN-PROCESS, scoped to the
    set's `documents` (repo-relative posix paths == the snapshot's `document.id`
    in this repo). Only the pure per-document families run (see
    DEFAULT_SCOPED_FAMILIES) — subprocess is unnecessary because the suite is
    importable and these families consume nothing but the doc list, so an
    in-process call with a filtered `ctx.docs` is faithful and cheap.

    Degrades gracefully: if the doc-health package is unimportable the action is
    recorded not-available rather than crashing."""
    try:
        from doc_health import DEFAULT_THRESHOLDS, corpus as dh_corpus
        from doc_health.families import FAMILIES
        from doc_health.runner import Context, run_suite
    except Exception as exc:  # noqa: BLE001
        result = ActionResult(ACTION_DOC_HEALTH, "not-available",
                              detail=f"doc-health machinery unavailable: {exc}")
        if wb is not None:
            wb.record_action(ACTION_DOC_HEALTH, reference="health/not-available", now=now)
        return result

    repo_root = Path(repo_root).resolve()
    repository = repository or repo_root.name
    wanted = set(documents)
    scoped_docs = [d for d in dh_corpus.load_docs(repository, repo_root) if d.path in wanted]

    ctx = Context(
        repo_paths={repository: repo_root}, docs=scoped_docs, capabilities={},
        change_ids={}, git=dh_corpus.RealGit(), thresholds=dict(DEFAULT_THRESHOLDS),
        as_of=as_of or date.today(), agg_root=None,
    )
    findings: list = []
    skips: list = []
    for fam in families:
        if fam not in FAMILIES:
            raise WorkbenchError(f"unknown doc-health family {fam!r}")
        # only_family != None ⇒ run_suite skips preflight (see runner.run_suite)
        run = run_suite(ctx, fam, set())
        findings.extend(run.findings)
        skips.extend(run.skips)
    # defensive: keep only findings on the scoped docs
    findings = [f for f in findings if getattr(f, "path", None) in wanted]

    ref = reference or f"health/scoped/{slug(repository)}-{len(wanted)}docs"
    result = ActionResult(
        ACTION_DOC_HEALTH, "completed", reference=ref, findings=findings,
        detail=f"{len(findings)} finding(s) over {len(scoped_docs)} scoped doc(s) "
               f"(families: {', '.join(families)})")
    if wb is not None:
        wb.record_action(ACTION_DOC_HEALTH, reference=ref, now=now)
    return result


def organize_topic(wb: Workbench, *, topic: str | None = None) -> str:
    return slug(topic or wb.data.get("name") or "untitled")


def organize_skeleton_relpath(topic: str) -> str:
    """The draft-organize skeleton path — under the gitignored organize prefix,
    i.e. OUTSIDE ideation/staging/ (moving into staging is a human gate action)."""
    return f"{ORGANIZE_DIR}{slug(topic)}/{slug(topic)}.md"


def render_organize_skeleton(wb: Workbench, *, topic: str, now: str | None = None) -> str:
    """A header-compliant `staging/<topic>/` packet SKELETON pre-filled from the
    set. Carries the full document-lifecycle header set (H1, Status, Kind,
    Summary, Topics, Repository context, Captured) PLUS the staging-packet fields
    (Staging ID, Target capabilities, Source) and the feat-spec-shaped body
    (target capability / delta type / claims / open questions / exit path).

    Status is `draft`, NOT `staged` — the skeleton is pre-staging material; a
    human relocates it into ideation/staging/ as a gate action."""
    now = now or _utcnow()
    name = wb.data.get("name", topic)
    repository = wb.data.get("repository", "")
    members = wb.member_documents()
    seed_kind = (wb.data.get("seed") or {}).get("kind", SEED_ADHOC)
    # Topics: prefer a recipe's checked keywords, else the topic slug.
    recipe = wb.data.get("recipe") or {}
    topics = ", ".join(recipe.get("checked") or [slug(topic)])
    member_lines = "\n".join(f"- {doc}" for doc in members) or "- (no members recorded)"

    return (
        f"# Staged (DRAFT): {name}\n\n"
        "Status: draft\n"
        "Kind: staging-packet\n"
        f"Summary: DRAFT organize skeleton pre-filled from workbench set "
        f"\"{name}\". Review the TODOs, then move this packet into "
        f"ideation/staging/{slug(topic)}/ as a HUMAN GATE ACTION.\n"
        f"Topics: {topics}\n"
        f"Repository context: {repository}\n"
        f"Captured: {now[:10]}\n"
        f"Staging ID: {repository}:staging:{slug(topic)}\n"
        "Target capabilities: TODO (ADDED | MODIFIED | REMOVED — human to declare)\n"
        f"Source: workbench set \"{name}\" (seed {seed_kind}); draft-organize action {now}\n\n"
        "> DRAFT skeleton written OUTSIDE `ideation/staging/` by the workbench\n"
        "> draft-organize action. Machinery NEVER stages — moving material into\n"
        "> `ideation/staging/` remains a human gate action. Fill the TODOs first.\n\n"
        "## Target capability\n\n"
        "TODO — the capability this reference set would realize.\n\n"
        "## Delta type\n\n"
        "TODO — ADDED | MODIFIED | REMOVED.\n\n"
        "## Claims\n\n"
        "TODO — the load-bearing claims the set's evidence supports.\n\n"
        "## Reference set members\n\n"
        f"{member_lines}\n\n"
        "## Open questions\n\n"
        "TODO — what must be resolved before this can be staged.\n\n"
        "## Exit path\n\n"
        "TODO — the OpenSpec change / promotion this packet targets.\n"
    )


def draft_organize(wb: Workbench, boundary: OutputBoundary, *,
                   topic: str | None = None, now: str | None = None) -> ActionResult:
    """Pre-fill a `staging/<topic>/` packet SKELETON from the set and write it
    OUTSIDE `ideation/staging/` through `boundary.permit_draft_skeleton` (which
    REFUSES a staging path). Records the draft-organize action on the manifest
    with the skeleton path as its reference."""
    topic = organize_topic(wb, topic=topic)
    rel = organize_skeleton_relpath(topic)
    resolved = boundary.permit_draft_skeleton(rel)  # refuses ideation/staging/*
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(render_organize_skeleton(wb, topic=topic, now=now), encoding="utf-8")
    result = ActionResult(ACTION_DRAFT_ORGANIZE, "completed", reference=rel,
                          detail=f"organize skeleton written to {rel} (outside ideation/staging/)")
    wb.record_action(ACTION_DRAFT_ORGANIZE, reference=rel, now=now)
    return result
