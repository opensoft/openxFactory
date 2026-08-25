"""Sharded, bounded, resumable full-corpus baseline for the document
catalog (US2; feature tasks T010/T011).

Realizes the contract requirement "Full baseline and incremental
refresh" (openxFactory `add-document-cataloging`): cataloging begins
with one explicit, repository-sharded, resumable full-corpus baseline;
during baseline the report states progress without opening one issue
per legacy document; complete-coverage enforcement stays off until the
deterministic merge completes (research D5).

Everything here is a pure function of its inputs plus explicit
filesystem state under the baseline root — no wall-clock reads, no
randomness, stable ``(repo, locator)`` ordering, and byte-identical
rendering for identical inputs (research D3, via ``catalog.render``).

Baseline layout (all writes land under the catalog prefix
``inventory.is_generated_catalog_path`` excludes from discovery):

    health/document-catalog/baseline/
        shards/<repo...>/<NNNN>.yaml   immutable per-invocation
                                       shard-state artifacts; slash-
                                       separated repo IDs become subdirs
        merged.yaml                    deterministic fold over completed
                                       shard chains, ordered by repo —
                                       the first full catalog state
        baseline_complete.yaml         marker written ONLY by a full
                                       merge; gates complete-coverage
                                       enforcement

Shard model: each ``run_shard`` invocation walks the next ``budget``
entries of one repository's governed entry list and records them in a
new, immutable, sequence-numbered shard artifact carrying the resume
cursor (last locator processed), the ``complete`` flag, the shard
content hash, and the repository corpus hash (content identity of the
full entry list being walked). Resume is stateless: a later invocation
reads the persisted chain and continues after its cursor — "re-run,
skip completed shards" (research D5). A corpus that changed mid-
baseline no longer matches the chain's corpus hash, so the walk
restarts from the beginning as a new chain; the merged baseline stays
deterministic (spec edge case "A repository is unavailable
mid-baseline").

Merge model: ``merge_baseline`` folds the completed chain of every
governed repository — the REQUIRED ``repos`` corpus authority, plus
anything discovered on disk — in repo order into ``merged.yaml``
(exactly one entry per governed document, sorted ``(repo, locator)``),
then writes the ``baseline_complete`` marker. Any incomplete repository
— including a governed repository that was unavailable before its
first shard and so left no trace on disk — means no merge output and
no marker: its shard resumes later (spec edge case) instead of the
baseline freezing over a partial corpus.
A ``merged.yaml`` without the marker is a crashed merge, not a record —
it heals idempotently on retry (the ``run.yaml`` precedent in
``catalog``); once the marker exists the baseline is frozen and
post-baseline changes flow through the normal mechanical pass.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import catalog
from .catalog import CatalogError

BASELINE_DIR = catalog.CATALOG_DIR / "baseline"
SHARDS_DIR = BASELINE_DIR / "shards"
MERGED_NAME = "merged.yaml"
MARKER_NAME = "baseline_complete.yaml"

SHARD_KIND = "xfactory_document_catalog_baseline_shard"
MERGED_KIND = "xfactory_document_catalog_baseline"
MARKER_KIND = "xfactory_document_catalog_baseline_complete"
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ShardState:
    """Result of one bounded shard invocation (data-model.md "Baseline
    shard state"). ``processed`` counts this invocation's entries;
    ``cataloged`` is the active chain's cumulative coverage of the
    repository's ``total`` governed entries."""
    repo: str
    sequence: int
    path: Path
    budget: int
    start_after: str | None
    cursor: str | None
    complete: bool
    processed: int
    cataloged: int
    total: int
    corpus_hash: str


@dataclass(frozen=True)
class RepoProgress:
    """Aggregate per-repository coverage — counts only, never
    per-document identity (US2 acceptance 2)."""
    repo: str
    cataloged: int
    total: int
    complete: bool


@dataclass(frozen=True)
class BaselineProgress:
    """Coverage progress for progress-mode reporting: aggregate counts
    only, so an incomplete baseline never surfaces one missing-entry
    finding per legacy document."""
    repos: tuple
    cataloged: int
    total: int
    repos_complete: int
    repos_total: int
    complete: bool

    @property
    def percent(self) -> float:
        if self.total:
            return 100.0 * self.cataloged / self.total
        return 100.0 if self.complete else 0.0


# --- entry preparation ----------------------------------------------------------

def _locator_str(entry: dict) -> str:
    return catalog._locator(entry)[1]


def _prepare_entries(repo: str, entries) -> list[dict]:
    """Validate and canonically order one repository's full mechanical
    entry list: every entry belongs to ``repo``, locators are
    unambiguous and unique, freshness fields are resolved."""
    prepared = sorted(entries, key=catalog._entry_key)
    for entry in prepared:
        if entry.get("repo") != repo:
            raise ValueError(
                f"entry {catalog._entry_key(entry)} does not belong to "
                f"repository {repo!r}")
        for field in ("content_hash", "revision", "snapshot_id"):
            if not entry.get(field):
                raise ValueError(
                    f"baseline entry has no {field} — shards walk "
                    f"mechanical catalog entries: "
                    f"{catalog._entry_key(entry)}")
    catalog._keyed(prepared, repo)  # unique, unambiguous locator keys
    return prepared


def _canonical_hash(payload) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _corpus_hash(prepared: list[dict]) -> str:
    """Content identity of the repository entry list being walked:
    ordered ``(locator, content_hash)`` pairs. Revision or snapshot-id
    churn from unrelated commits never restarts a walk; any content,
    addition, or deletion change does."""
    return _canonical_hash(
        [[_locator_str(e), e["content_hash"]] for e in prepared])


# --- shard-state artifacts ------------------------------------------------------

def _repo_shards_dir(root: Path, repo: str) -> Path:
    return Path(root) / SHARDS_DIR / Path(*catalog._repo_segments(repo))


def _shard_path(root: Path, repo: str, sequence: int) -> Path:
    return _repo_shards_dir(root, repo) / f"{sequence:04d}.yaml"


# The shard fields every chain/progress/merge computation indexes
# directly (`_chain`, `run_shard`, `_chain_entries`, `progress`,
# `merge_baseline`). A recorded shard is machine-written and always
# carries them, but a truncated/torn write, bad merge, hand-edit, or
# foreign artifact could leave a valid-JSON but wrong-shape file that
# would otherwise KeyError deep inside a chain walk — the deterministic
# family must report that as a finding, never crash the whole run.
_SHARD_REQUIRED_KEYS = frozenset({
    "start_after", "corpus_hash", "cursor", "complete", "total",
    "entries", "sequence"})


def _load_shards(root: Path, repo: str) -> list[dict]:
    """Every recorded shard artifact for one repository, in sequence
    order. A shard file that is unparseable, is not a JSON object, or is
    missing a required shard field is corrupt persisted state and raises
    the controlled ``CatalogError`` its callers surface as a finding —
    never a raw ``JSONDecodeError``/``KeyError`` that would abort the
    whole doc-health run (the ``_load_yaml_json`` precedent in
    ``catalog``)."""
    shards_dir = _repo_shards_dir(root, repo)
    if not shards_dir.is_dir():
        return []
    paths = [p for p in shards_dir.iterdir()
             if p.is_file() and p.suffix == ".yaml" and p.stem.isdigit()]
    shards = []
    for p in sorted(paths, key=lambda p: int(p.stem)):
        try:
            shard = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise CatalogError(f"corrupt baseline shard {p}: {exc}")
        if not isinstance(shard, dict):
            raise CatalogError(
                f"corrupt baseline shard {p}: expected a JSON object, got "
                f"{type(shard).__name__}")
        missing = _SHARD_REQUIRED_KEYS - set(shard)
        if missing:
            raise CatalogError(
                f"corrupt baseline shard {p}: missing required shard "
                f"field(s) {', '.join(sorted(missing))}")
        shards.append(shard)
    return shards


def _chain(shards: list[dict]) -> list[dict]:
    """The active shard chain: the last contiguous run of shards over
    one corpus state. A shard with ``start_after: null`` starts a new
    chain (fresh walk or corpus-change restart) and supersedes earlier
    chains; a continuation must resume exactly at the previous shard's
    cursor over the same corpus hash, or it is an orphan."""
    chain: list[dict] = []
    for shard in shards:
        if shard["start_after"] is None:
            chain = [shard]
        elif (chain and not chain[-1]["complete"]
                and shard["corpus_hash"] == chain[-1]["corpus_hash"]
                and shard["start_after"] == chain[-1]["cursor"]):
            chain.append(shard)
        else:
            chain = []  # orphaned continuation — wait for a restart
    return chain


def _write_exclusive(path: Path, text: str) -> None:
    """Atomic, exclusive artifact write: the content lands complete in
    a UNIQUE per-invocation temp file first (``mkstemp``), then links
    into place — ``os.link`` fails if the target exists, so exactly one
    writer ever records a shard artifact and the recorded bytes are
    exactly the winning writer's. Racing same-sequence writers never
    share a temp name: the loser can neither truncate nor substitute
    the winner's content, and it fails closed with ``CatalogError``
    (never a stray ``FileNotFoundError`` from a winner unlinking a
    shared temp). An interrupted write can never leave a truncated
    artifact that would wedge resume: at worst an orphaned ``.tmp``
    file remains, invisible to shard loading. Perms are ``mkstemp``'s
    default 0600 — git normalizes modes on commit, so there is no need
    to widen them here."""
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        try:
            os.link(tmp, path)
        except FileExistsError:
            raise CatalogError(
                f"immutable baseline shard artifact already exists: {path}")
    finally:
        os.unlink(tmp)  # this invocation's own temp file, always present


# --- bounded, resumable shards (T010) -------------------------------------------

def run_shard(root, repo, budget, as_of, entries) -> ShardState:
    """Walk the next ``budget`` entries of one repository's baseline.

    ``entries`` is the repository's full mechanical catalog entry list
    (``catalog.mechanical_entries`` filtered to ``repo``) — supplied by
    the caller exactly as ``inventory.build_inventory`` is fed its
    corpus, so this module stays a pure function of explicit inputs.

    - Bounded: at most ``budget`` entries land in this invocation's
      shard artifact; ``complete`` is true only when the walk reached
      the end of the repository.
    - Resumable: resume state is the persisted shard chain itself. A
      new invocation continues after the last recorded cursor; a
      repository whose chain is already complete over the same corpus
      is a no-op that writes nothing.
    - Immutable: every invocation records a NEW sequence-numbered shard
      artifact; existing artifacts are never rewritten.
    - Deterministic restart: a corpus hash that no longer matches the
      chain restarts the walk from the beginning as a new chain, so the
      eventual merge is exactly one entry per governed document of ONE
      corpus state.
    - Once the ``baseline_complete`` marker exists the baseline is
      frozen: new shard work is refused — post-baseline changes flow
      through the normal mechanical pass.
    """
    root = Path(root)
    day = catalog._as_of_str(as_of)
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise ValueError(f"shard entry budget must be a positive int: "
                         f"{budget!r}")
    catalog._repo_segments(repo)  # validate the repository id early
    prepared = _prepare_entries(repo, entries)
    corpus_hash = _corpus_hash(prepared)

    shards = _load_shards(root, repo)
    chain = _chain(shards)
    if chain and chain[-1]["corpus_hash"] == corpus_hash:
        last = chain[-1]
        if last["complete"]:
            # Completed repository, unchanged corpus: skip (research D5).
            return ShardState(
                repo=repo, sequence=last["sequence"],
                path=_shard_path(root, repo, last["sequence"]),
                budget=budget, start_after=last["cursor"],
                cursor=last["cursor"], complete=True, processed=0,
                cataloged=len(prepared), total=len(prepared),
                corpus_hash=corpus_hash)
        start_after = last["cursor"]
        cataloged_before = sum(len(s["entries"]) for s in chain)
    else:
        start_after = None  # fresh walk, or corpus-change restart
        cataloged_before = 0

    if is_baseline_complete(root):
        raise CatalogError(
            "baseline is already complete — post-baseline corpus changes "
            "flow through the mechanical catalog pass, not new baseline "
            f"shards (repo {repo!r})")

    if start_after is None:
        remaining = prepared
    else:
        remaining = [e for e in prepared
                     if _locator_str(e) > start_after]
    batch = remaining[:budget]
    complete = len(batch) == len(remaining)
    cursor = _locator_str(batch[-1]) if batch else start_after

    sequence = shards[-1]["sequence"] + 1 if shards else 1
    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": SHARD_KIND,
        "status": "record",
        "repo": repo,
        "as_of": day,
        "sequence": sequence,
        "budget": budget,
        "start_after": start_after,
        "cursor": cursor,
        "complete": complete,
        "corpus_hash": corpus_hash,
        "total": len(prepared),
        "entries": batch,
        "shard_content_hash": _canonical_hash(batch),
    }
    path = _shard_path(root, repo, sequence)
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_exclusive(path, catalog.render(document))
    return ShardState(
        repo=repo, sequence=sequence, path=path, budget=budget,
        start_after=start_after, cursor=cursor, complete=complete,
        processed=len(batch), cataloged=cataloged_before + len(batch),
        total=len(prepared), corpus_hash=corpus_hash)


# --- deterministic merge and enforcement gate (T011) ----------------------------

def _discovered_repos(root: Path) -> list[str]:
    shards_root = Path(root) / SHARDS_DIR
    if not shards_root.is_dir():
        return []
    repos = set()
    for path in shards_root.rglob("*.yaml"):
        if (path.is_file() and path.stem.isdigit()
                and path.parent != shards_root):
            repos.add(path.parent.relative_to(shards_root).as_posix())
    return sorted(repos)


def _chain_entries(repo: str, chain: list[dict]) -> list[dict]:
    entries = [e for shard in chain for e in shard["entries"]]
    if len(entries) != chain[-1]["total"]:
        raise CatalogError(
            f"baseline shard chain for {repo!r} is corrupted: "
            f"{len(entries)} entries recorded, "
            f"{chain[-1]['total']} governed")
    return entries


def merge_baseline(root, as_of, repos) -> Path | None:
    """Deterministic fold of every completed repository chain, ordered
    by repo; writes ``merged.yaml`` and then the ``baseline_complete``
    marker. Returns the marker path, or None while any repository —
    named in ``repos`` or discovered on disk — is still incomplete
    (nothing lands; complete-coverage enforcement stays off).

    ``repos`` is REQUIRED: the full governed repository set, supplied
    by the caller that owns corpus discovery (exactly as ``run_shard``
    is fed its entries). The merge cannot derive it from disk — a
    governed repository that was unavailable before its first shard
    leaves no trace under ``shards/``, and merging without naming it
    would freeze the baseline over a partial corpus and permanently
    refuse the late repository's shards (FR-005 / SC-001; spec edge
    case "A repository is unavailable mid-baseline: its shard resumes
    later"). Repositories discovered on disk but absent from ``repos``
    still gate and fold, so recorded shard state is never silently
    dropped.

    The fold is a pure function of the recorded shard chains, so
    re-merging renders byte-identical output regardless of shard
    budgets or interleaving. Re-merging after completion is an
    idempotent no-op for an identical fold; a fold that would differ
    from the recorded baseline is refused (the merged baseline is
    immutable — later corpus changes flow through the mechanical pass).

    A repository's folded entries can legitimately carry different
    per-entry ``revision``/``snapshot_id`` values when its chain spanned
    more than one ``run_shard`` invocation and an unrelated commit (no
    governed-content change) landed in between: chain continuation is
    gated on ``_corpus_hash`` (content only), never on revision, so
    resumability over a long multi-session walk is deliberately not
    coupled to per-repo revision uniformity (research D5). This is
    narrower than the ordinary mechanical pass's ``_snapshot_document``,
    which does reject mixed revisions/snapshot-ids within one snapshot —
    that guard protects a single atomic corpus walk, not a baseline
    whose whole purpose is spanning sessions.
    """
    root = Path(root)
    day = catalog._as_of_str(as_of)
    if repos is None or isinstance(repos, (str, bytes)):
        raise ValueError(
            "merge_baseline requires the full governed repository set — "
            "a repository unavailable before its first shard is invisible "
            f"on disk and must still gate the merge: {repos!r}")
    governed = sorted({str(r) for r in repos})
    if not governed:
        raise ValueError(
            "merge_baseline requires a non-empty governed repository set: "
            "an empty set would freeze the baseline over a partial corpus")
    for repo in governed:
        catalog._repo_segments(repo)  # validate repository ids early
    expected = sorted(set(_discovered_repos(root)) | set(governed))

    chains = {}
    for repo in expected:
        chain = _chain(_load_shards(root, repo))
        if not chain or not chain[-1]["complete"]:
            return None  # incomplete baseline: no merge, no marker
        chains[repo] = chain

    entries, coverage = [], {}
    seen = set()
    for repo in expected:  # deterministic fold ordered by repo
        repo_entries = _chain_entries(repo, chains[repo])
        for entry in repo_entries:
            key = catalog._entry_key(entry)
            if key in seen:
                raise CatalogError(
                    f"baseline merge found a duplicate catalog key: {key}")
            seen.add(key)
        coverage[repo] = {
            "entries": len(repo_entries),
            "corpus_hash": chains[repo][-1]["corpus_hash"],
        }
        entries.extend(repo_entries)

    merged_document = {
        "schema_version": SCHEMA_VERSION,
        "kind": MERGED_KIND,
        "status": "record",
        "repos": coverage,
        "entries": entries,
    }
    rendered = catalog.render(merged_document)
    merged_sha = hashlib.sha256(rendered.encode()).hexdigest()
    baseline_dir = root / BASELINE_DIR
    merged_path = baseline_dir / MERGED_NAME
    marker_path = baseline_dir / MARKER_NAME

    def _recorded_sha() -> str:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        return marker.get("merged_sha256", "")

    def _publish_recorded(sha: str) -> None:
        # Only marker-era code writes merged.yaml, atomically from the
        # recorded fold's content-addressed sidecar: a pre-marker
        # merged.yaml (crashed legacy merge) is replaced whole, never
        # blended, and a winner that crashed between recording the
        # marker and publishing merged.yaml is healed by any later
        # merge of the identical fold.
        if merged_path.is_file() and hashlib.sha256(
                merged_path.read_bytes()).hexdigest() == sha:
            return
        sidecar = baseline_dir / f"merged.{sha}.yaml"
        if not sidecar.is_file():
            if merged_path.is_file():
                return  # legacy pre-sidecar record; load_baseline verifies
            raise CatalogError(
                "baseline marker exists but neither merged.yaml nor its "
                f"recorded sidecar does — unrecoverable record: {sha}")
        fd, tmp_name = tempfile.mkstemp(
            dir=baseline_dir, prefix=MERGED_NAME + ".", suffix=".tmp")
        os.close(fd)
        os.unlink(tmp_name)
        os.link(sidecar, tmp_name)
        os.replace(tmp_name, merged_path)

    if marker_path.is_file():  # fast path; the exclusive claim below is
        if _recorded_sha() == merged_sha:  # what actually decides races
            _publish_recorded(merged_sha)
            return marker_path  # idempotent re-merge of the same fold
        raise CatalogError(
            "baseline is already merged: the recorded baseline is "
            "immutable and a differing fold is refused")

    # Stage this fold content-addressed: identical folds share one
    # sidecar name, so losing this exclusive write to an identical fold
    # is a completed no-op and no racer ever touches another fold's
    # bytes.
    baseline_dir.mkdir(parents=True, exist_ok=True)
    sidecar_path = baseline_dir / f"merged.{merged_sha}.yaml"
    try:
        _write_exclusive(sidecar_path, rendered)
    except CatalogError:
        if sidecar_path.read_text(encoding="utf-8") != rendered:
            raise CatalogError(
                "content-addressed baseline sidecar does not match its "
                f"own hash — refusing to proceed: {sidecar_path}")

    # The completion marker is the single exclusive claim: exactly one
    # fold is ever recorded, decided by os.link — never check-then-act.
    try:
        _write_exclusive(marker_path, catalog.render({
            "schema_version": SCHEMA_VERSION,
            "kind": MARKER_KIND,
            "status": "record",
            "as_of": day,
            "repos": {repo: coverage[repo]["entries"] for repo in coverage},
            "total_entries": len(entries),
            "merged_sha256": merged_sha,
        }))
    except CatalogError:
        if _recorded_sha() != merged_sha:
            raise CatalogError(
                "baseline is already merged: the recorded baseline is "
                "immutable and a differing fold is refused")
        # identical fold recorded by a racer: fall through and heal the
        # canonical file if the recording merge crashed before publish

    _publish_recorded(_recorded_sha())
    return marker_path


def is_baseline_complete(root) -> bool:
    """The complete-coverage enforcement gate: true only once the
    deterministic merge has written the ``baseline_complete`` marker."""
    return (Path(root) / BASELINE_DIR / MARKER_NAME).is_file()


def load_baseline(root) -> dict | None:
    """The merged baseline document — but only once the completion
    marker exists (an unmarked ``merged.yaml`` is a crashed merge, not
    a record). Verifies the marker's recorded content hash."""
    root = Path(root)
    marker_path = root / BASELINE_DIR / MARKER_NAME
    merged_path = root / BASELINE_DIR / MERGED_NAME
    if not marker_path.is_file():
        return None
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CatalogError(f"corrupt baseline marker {marker_path}: {exc}")
    if not isinstance(marker, dict):
        raise CatalogError(
            f"corrupt baseline marker {marker_path}: expected a JSON object")
    if not merged_path.is_file():
        raise CatalogError(
            "baseline marker exists but merged.yaml is missing — re-run "
            "merge_baseline with the identical fold to heal the crashed "
            "publish")
    rendered = merged_path.read_text(encoding="utf-8")
    if hashlib.sha256(rendered.encode()).hexdigest() != \
            marker.get("merged_sha256"):
        raise CatalogError(
            "merged baseline does not match its completion marker")
    try:
        data = json.loads(rendered)
    except ValueError as exc:
        raise CatalogError(f"corrupt merged baseline {merged_path}: {exc}")
    if not isinstance(data, dict):
        raise CatalogError(
            f"corrupt merged baseline {merged_path}: expected a JSON object")
    return data


# --- progress-mode reporting (T011) ---------------------------------------------

def progress(root) -> BaselineProgress:
    """Coverage progress for progress-mode reporting: aggregate counts
    per repository and overall — no per-document identity, so an
    incomplete baseline reports percentages instead of one
    missing-entry finding per legacy document (US2 acceptance 2)."""
    root = Path(root)
    repos = []
    for repo in _discovered_repos(root):
        shards = _load_shards(root, repo)
        chain = _chain(shards)
        cataloged = sum(len(s["entries"]) for s in chain)
        # `chain` is empty here only for a shard directory that could
        # not have been produced by `run_shard`'s exclusive-write path:
        # every successful write either starts a fresh chain
        # (`start_after: None`, never orphaned by `_chain`) or
        # continues the chain it just read, and a losing racer fails
        # closed instead of persisting an incompatible shard. This
        # branch is a defensive fallback for a foreign/corrupted shard
        # directory only; `shards[-1]` (the highest recorded sequence)
        # is the freshest artifact on disk and the best available
        # proxy for `total` when no active chain exists to trust.
        latest = chain[-1] if chain else shards[-1]
        repos.append(RepoProgress(
            repo=repo, cataloged=cataloged, total=latest["total"],
            complete=bool(chain and chain[-1]["complete"])))
    return BaselineProgress(
        repos=tuple(repos),
        cataloged=sum(r.cataloged for r in repos),
        total=sum(r.total for r in repos),
        repos_complete=sum(1 for r in repos if r.complete),
        repos_total=len(repos),
        complete=is_baseline_complete(root))
