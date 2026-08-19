"""Deterministic scan -> snapshot dict (plan "generator.py"; change task 3.1).

Reuses `scripts/doc_health/corpus.py` (repo discovery, doc iteration, header
parsing, promoted-spec/change-id enumeration) and its `RealGit` for the
`generation.source_revision` anchor; adds ideation-specific derivation
(Topics->cluster edges, possibles-register read, change task-progress) on top.

THE KEYSTONE (US1). This is the sole component that scans the repository; every
renderer reads only the snapshot it emits. The projection is deterministic — the
same working tree yields a BYTE-IDENTICAL snapshot (SC-001):

  * NO wall clock. `generation.source_revision` is the anchor; any
    `generation.generated_at` derives from that revision's commit date through
    the injected git abstraction, never `datetime.now()`. Because the fixture
    base-repo lives INSIDE the openxFactory git repo, `RealGit` HEAD is unstable
    across commits, so `source_revision` is accepted explicitly (and a `git`
    abstraction is injectable — tests pass a `FakeGit`) so byte-identity tests
    can pin it.
  * Stable ordering everywhere — documents by path (== id), clusters/possibles
    by id, keywords by keyword, staged topics by staging_id, edges by document —
    and canonical rendering is delegated to `snapshot.canonical_json`.

Derivation rules (from the ratified spec / the five pinned schemas):
  * doc -> cluster edges come from declared `Topics:` headers ONLY; each edge
    lists the topics that matched (FR-003).
  * cluster tallies count LINKS, not cards (SC-005).
  * cluster lineage (staged_picks / proposals / realized) is DISTINCT from the
    member edges (spec "Member pane derivation").
  * possibles project one-for-one from the consolidated register through
    `fixtures.project_possibles` (states / reason / citation / pick /
    option_set / claiming_clusters / evidence) with NO historical fabrication:
    a document without a `Possible feats:` section carries no possibles (FR-004).
  * keyword_index carries DECLARED counts only (inferred deferred until
    document-cataloging lands).
  * project / project_group resolve via the project-register adapter; an
    unregistered repository renders ungrouped (its own implicit project).
  * every emitted document carries a deterministic `completeness` object and
    every staged topic a `health` aggregate, both computed by the ONE pure
    scoring module (`completeness.py`, add-staging-workbench design D1/D2/D8)
    over text this module has already loaded — no model call, no clock, so
    byte-identity holds. Health reads the topic FOLDER's own corpus documents
    ONLY; documents that merely declare the topic as a destination contribute
    nothing. `live_topic_health` below serves the propose route's readiness
    gate through the same functions (design D9), which is why the guard itself
    never scans the tree.
  * each change carries its own `folder` + recursive `files` listing (an
    additive field beyond the pinned schema's explicit properties, which it
    tolerates) — the drill-down explorer's (US4) sole source for a
    proposal/realized tile's contents, mirroring `staged_topics[].files`.

The rendered snapshot is validated against the pinned schema by the generator's
callers (`snapshot.validate_or_raise`); this module never restates the schema.
"""

from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from doc_health import TAXONOMY, corpus
from doc_health.corpus import RealGit

from . import GENERATOR_VERSION, completeness, fixtures
from .register import CrossReferenceIndexAdapter, ProjectRegisterAdapter

# Header window matches doc_health.corpus.STATUS_SCAN_LINES: governance headers
# live in the doc's first lines.
HEADER_SCAN_LINES = corpus.STATUS_SCAN_LINES

# The lifecycle vocabulary the snapshot schema's document `stage`
# (lifecycle_status enum) accepts, reused verbatim from the doc-health suite's
# status-validity family (doc_health.TAXONOMY) rather than restated from the
# schema — this module never restates the schema (see snapshot.validate_or_raise).
LIFECYCLE_STATUSES = TAXONOMY

_CHECKED_RE = re.compile(r"(?m)^\s*[-*]\s*\[[xX]\]")
_UNCHECKED_RE = re.compile(r"(?m)^\s*[-*]\s*\[ \]")
_ARCHIVE_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)")
# The only revision shape `RealGitDates.commit_date` accepts: a (possibly
# abbreviated) hex commit sha — the documented `source_revision` anchor form.
_REVISION_RE = re.compile(r"[0-9a-fA-F]{4,64}")


# --------------------------- injectable git abstraction ---------------------------

class RealGitDates:
    """The two git facts the generator needs, on top of the doc-health `RealGit`
    reuse base: the scanned repo's HEAD sha (the `source_revision` anchor) and a
    revision's committer date-time (the ONLY source of `generated_at` — never the
    wall clock). Degrades to None on any failure so generation still succeeds
    (with `generated_at` omitted) outside a git checkout."""

    def __init__(self, git: RealGit | None = None) -> None:
        self._git = git or RealGit()

    def head_sha(self, repo: Path) -> str | None:
        return self._git.head_sha(Path(repo))

    def commit_date(self, repo: Path, revision: str) -> str | None:
        # Containment: `revision` can arrive from the CLI (--source-revision).
        # The anchor is documented as a commit sha, so anything not shaped like
        # one (option-shaped strings, refs, rev expressions) is refused here —
        # degrading to None like every other failure, which merely omits
        # `generated_at` — and the `--` end-of-options marker means even an
        # accepted value can never be parsed by git as an option.
        if not _REVISION_RE.fullmatch(revision):
            return None
        proc = subprocess.run(
            ["git", "-C", str(repo), "show", "-s", "--format=%cI", revision, "--"],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            return None
        out = proc.stdout.strip()
        return out or None


# --------------------------- header parsing ---------------------------

def _header_value(text: str, name: str) -> str | None:
    """First `Name: value` header value in the doc's header window, else None."""
    prefix = name + ":"
    for line in text.splitlines()[:HEADER_SCAN_LINES]:
        if line.startswith(prefix):
            return line[len(prefix):].strip() or None
    return None


def parse_topics(text: str) -> list[str]:
    """Declared `Topics:` subjects (comma-separated), the doc->cluster edge
    source. Order preserved as authored; the generator sorts derived structures."""
    raw = _header_value(text, "Topics")
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def _titleize(topic: str) -> str:
    """Fallback cluster display name for a topic ABSENT from the cross-reference
    index: a hyphen/underscore-separated slug becomes spaced title case
    (`doc-health` -> `Doc Health`). Interior casing is preserved (only the first
    letter of each word is upper-cased, so an acronym slug is not mangled). An
    empty/degenerate slug returns the raw topic."""
    words = [w for w in re.split(r"[-_]+", topic) if w]
    return " ".join(w[:1].upper() + w[1:] for w in words) or topic


def _cluster_name(topic: str, entry: dict | None) -> str:
    """The cluster's display name: the cross-reference index topic entry's `name`
    when the index carries an entry for this cluster id, else the titleized
    topic slug."""
    name = (entry or {}).get("name")
    if isinstance(name, str) and name.strip():
        return name
    return _titleize(topic)


def _scored_readiness(entry: dict | None) -> dict[str, int] | None:
    """A cluster's readiness in the flat `{tier: score}` shape the funnel's
    readiness-heat renders — SCORED tiers only. A tier without an integer `score`
    (an `unscored` bootstrap tier) is omitted, and an all-unscored panel yields
    None so the heat binding stays DORMANT until the scoring worker emits numbers,
    at which point it renders with no dashboard change (the index owns the shape;
    this is the numeric projection of it)."""
    tiers = ((entry or {}).get("readiness") or {}).get("tiers") or []
    heat: dict[str, int] = {}
    for tier in tiers:
        if not isinstance(tier, dict):
            continue
        name, score = tier.get("tier"), tier.get("score")
        if isinstance(name, str) and isinstance(score, int) and not isinstance(score, bool):
            heat[name] = score
    return heat or None


def _cluster_conflict_flags(entry: dict | None) -> list | None:
    """A cluster's inter-tier conflict flags, copied VERBATIM from the
    cross-reference index topic entry. Absent (the bootstrap state) yields None."""
    flags = (entry or {}).get("conflict_flags")
    return flags if isinstance(flags, list) and flags else None


def _staging_topic_of(path: str) -> str | None:
    """The staging topic id a document lives under, or None."""
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "ideation" and parts[1] == "staging":
        return parts[2]
    return None


# --------------------------- change enumeration ---------------------------

def _archived_change(arch: Path) -> tuple[str, str, Path, str | None]:
    """One archived change folder's tuple: the canonical id strips the archive
    date prefix (which becomes the archive_date)."""
    m = _ARCHIVE_DATE_RE.match(arch.name)
    if m:
        return (m.group(2), "archived", arch, m.group(1))
    return (arch.name, "archived", arch, None)


def _iter_changes(repo_root: Path) -> list[tuple[str, str, Path, str | None]]:
    """(change_id, status, folder, archive_date) per change — active folders
    under openspec/changes/ and archived (date-prefixed) folders under
    openspec/changes/archive/."""
    base = repo_root / "openspec" / "changes"
    out: list[tuple[str, str, Path, str | None]] = []
    if not base.is_dir():
        return out
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        if child.name == "archive":
            out.extend(_archived_change(arch)
                       for arch in sorted(child.iterdir()) if arch.is_dir())
        else:
            out.append((child.name, "active", child, None))
    return out


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _task_progress(folder: Path) -> dict[str, int] | None:
    tasks = folder / "tasks.md"
    if not tasks.is_file():
        return None
    text = _read(tasks)
    completed = len(_CHECKED_RE.findall(text))
    total = completed + len(_UNCHECKED_RE.findall(text))
    if total == 0:
        return None
    return {"completed": completed, "total": total}


def _load_openspec_meta(folder: Path) -> dict:
    """A change's `.openspec.yaml` metadata as a dict (empty when absent or
    malformed) — the governed per-change metadata file OpenSpec writes."""
    path = folder / ".openspec.yaml"
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(_read(path))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _declared_origin_staging(folder: Path) -> str | None:
    """The staging topic a change RECORDS as its own origin, or None.

    Read from the change's `.openspec.yaml` `origin:` block — the artifact the
    FORWARD transition writes (`proposal-support.write_origin_block`) at the
    moment the topic becomes a change. That makes it the one origin statement
    that survives the transition: a possibles-register pick edge points at the
    staging FOLDER, and the forward transition removes that folder, so a
    resolution reading only pick edges fails for exactly the changes that
    actually reached proposal (measured: 12 of 12 active changes reported
    `origin_staging_id: None`, and the corpus held ONE pick edge, carrying no
    `change_id`).

    Only `kind: staged` answers. An `ad_hoc` origin means the change did not come
    from staging, so there is no topic to return to and the demote's refusal is
    correct rather than something to paper over.

    THE ID COMES FROM `origin.path`, not `origin.id`. The declared id is
    namespaced (`<repo>:staging:<topic>`) while this field is compared against
    `staged_topics[].staging_id`, which is the bare topic. Deriving it from the
    path keeps one spelling of the id's shape rather than teaching a second place
    how to take a namespaced id apart.

    THE TOPIC IS THE FIRST SEGMENT AFTER `ideation/staging/`, not the path's
    BASENAME. `proposal-support.py transition` accepts any directory below
    `ideation/staging/` as its source, so a real declared origin can read
    `ideation/staging/my-topic/openspec` — and a basename rule answers `openspec`,
    a topic nobody named, into which the demote would then silently plan every
    returning file. A path that is not below `ideation/staging/` answers NOTHING
    rather than being guessed at: the origin contract puts staged sources there,
    and a malformed declaration is a refusal case, not a parsing challenge."""
    origin = _load_openspec_meta(folder).get("origin")
    if not isinstance(origin, dict) or origin.get("kind") != "staged":
        return None
    path = origin.get("path")
    if not isinstance(path, str):
        return None
    parts = [part for part in path.strip().split("/") if part not in ("", ".")]
    if parts[:2] != ["ideation", "staging"] or len(parts) < 3:
        return None
    return parts[2]


def _ratifier_of(folder: Path) -> str | None:
    """The recorded ratifying authority for a change, read from a GOVERNED
    artifact — the change's OpenSpec metadata (`.openspec.yaml`, `ratified_by`/
    `ratifier`). Deliberately NOT the `Ratified by:` proposal header: that header
    names the DOC a change ratifies (0/36 real changes carry it on the change
    itself), not who ratified the change. Returns None when no artifact records a
    ratifier — the current corpus reality — so ratification stays dormant rather
    than fabricating an authority."""
    meta = _load_openspec_meta(folder)
    for key in ("ratified_by", "ratifier"):
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _ratification(folder: Path, archive_date: str | None, status: str) -> dict[str, str] | None:
    """A change's recorded ratification, when determinable. The DATE derives from
    the archive folder's `YYYY-MM-DD-<id>` prefix (`archive_date`); the RATIFIER
    from the change's OpenSpec metadata (`_ratifier_of`). The pinned snapshot
    schema requires BOTH fields together (`ratification.required: [ratifier,
    date]`), so a date-only object is contract-invalid and would fail the pinned
    validator, skipping the nightly lane. The object is therefore emitted ONLY
    when both resolve and stays ABSENT otherwise — dormant until a governed
    ratifier lands, then rendered as `ratified <date> · <ratifier>` with no
    dashboard change."""
    if status != "archived" or not archive_date:
        return None
    ratifier = _ratifier_of(folder)
    if not ratifier:
        return None
    return {"ratifier": ratifier, "date": archive_date}


def _release_frontmatter(folder: Path) -> tuple[str | None, str | None]:
    """`code_surface:` / `target_release:` release-realization front-matter, or
    (None, None) when the proposal declares neither."""
    proposal = folder / "proposal.md"
    if not proposal.is_file():
        return None, None
    text = _read(proposal)
    return _header_value(text, "code_surface"), _header_value(text, "target_release")


def _change_files(folder: Path, repo_root: Path) -> list[str]:
    """Repo-relative, recursive file listing of a change's own folder — the
    explorer's (US4/T017) sole source for a proposal/realized tile's contents
    (FR-008): `proposal.md`/`design.md`/`tasks.md` plus any `specs/*/spec.md`
    (spec deltas) and `supporting-docs/*` living inside that same folder, by
    the OpenSpec change-folder convention. Mirrors `staged_topics[].files`
    exactly so the explorer never scans the repo — it reads this list from
    the snapshot verbatim (change 3.11). Additive: the pinned
    `ideation-dashboard-snapshot.schema.yaml` tolerates unknown `change`
    properties (no `additionalProperties: false`), so this needs no schema
    edit (spec Edge Cases: "the snapshot schema is extended by delta and the
    generator populates it")."""
    return sorted(
        p.relative_to(repo_root).as_posix()
        for p in folder.rglob("*") if p.is_file()
    )


# --------------------------- per-document degradation ---------------------------

def _document_exclusion_reason(doc: corpus.Doc) -> str | None:
    """Why this document cannot produce a schema-valid `documents[]` entry, or
    None when it can.

    `stage` is the ONLY required, non-nullable, header-derived document field:
    the schema types it as the `lifecycle_status` enum, so a missing/unparseable
    `Status:` header (stage None) or a value outside the vocabulary poisons the
    entry — and, because JSON-Schema validation is whole-document, one such
    document fails the ENTIRE snapshot and DoSes the nightly lane. The other
    header-derived fields cannot poison the entry: `kind`/`summary` are nullable
    (`[string, "null"]`), `topics` empties are already filtered, and
    `id`/`path`/`repository` never come from a header. So the generator degrades
    PER DOCUMENT here — an offending doc is EXCLUDED from `documents[]` (never
    emitted with `stage: null`) and reported to the caller — instead of emitting
    a snapshot the pinned validator rejects wholesale. A missing/invalid Status
    header is a corpus defect the governed doc-health status-validity family
    already errors on; the dashboard is a downstream projection and must not be
    DoSed by it (it surfaces the exclusion via lane detail instead)."""
    if doc.status is None:
        return "missing or unparseable Status: header"
    if doc.status not in LIFECYCLE_STATUSES:
        return f"unrecognized lifecycle status {doc.status!r}"
    return None


# --------------------------- projection helpers ---------------------------
#
# One helper per snapshot section; `generate_snapshot` below is pure
# orchestration. Behavior is identical to the previous inline body — the
# byte-identity tests (test_snapshot_determinism) pin that.

def _document_entry(d: corpus.Doc, *, vocabulary: frozenset[str]) -> dict[str, Any]:
    """One schema-valid `documents[]` entry (the caller has already screened
    the doc through `_document_exclusion_reason`), including its deterministic
    `completeness` object (add-staging-workbench task 2.5).

    `vocabulary` is the snapshot's keyword vocabulary — the union of every
    INCLUDED document's declared topics — which is why scoring happens in the
    projection's second pass: `keyword_coverage` and `link_degree` resolve
    against the corpus-wide derivation, not against this document alone. An
    EXCLUDED document never reaches here, so it carries no completeness and no
    dangling score survives its exclusion."""
    topics = parse_topics(d.text)
    entry: dict[str, Any] = {
        "id": d.path,
        "path": d.path,
        "stage": d.status,
        "kind": d.kind,
        "summary": _header_value(d.text, "Summary"),
        "topics": topics,
    }
    captured = _header_value(d.text, "Captured")
    if captured:
        entry["dates"] = {"captured": captured}
    staging_topic = _staging_topic_of(d.path)
    if staging_topic:
        entry["destinations"] = {"staged_topics": [staging_topic]}
    entry["completeness"] = completeness.document_completeness(
        text=d.text, kind=d.kind, topics=topics,
        destinations=entry.get("destinations"), vocabulary=vocabulary)
    return entry


def _project_documents(
    docs: list[corpus.Doc],
    excluded_documents: list[dict[str, str]] | None,
) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, set[str]]]:
    """Documents (funnel column 1): the entries plus the topic->docs and
    staging-topic->topics maps the cluster/keyword sections derive from.
    Per-document degradation: a doc that cannot produce a schema-valid entry is
    excluded (and reported through `excluded_documents` when a list is
    supplied) rather than poisoning the whole snapshot — its topics are NOT
    threaded into clusters/keywords either, so no dangling edge survives it.

    TWO PASSES over the (already loaded) docs, deliberately: pass one derives
    the topic maps — and with them the keyword vocabulary — from every included
    document, pass two builds the entries so each one's `completeness` can score
    `keyword_coverage`/`link_degree` against that corpus-wide vocabulary. No
    document is re-read; the second pass only re-parses the `Topics:` header."""
    topic_to_docs: dict[str, list[str]] = defaultdict(list)
    staged_topic_topics: dict[str, set[str]] = defaultdict(set)
    included: list[corpus.Doc] = []
    for d in sorted(docs, key=lambda d: d.path):
        defect = _document_exclusion_reason(d)
        if defect is not None:
            if excluded_documents is not None:
                excluded_documents.append({"path": d.path, "reason": defect})
            continue
        included.append(d)
        topics = parse_topics(d.text)
        sid = _staging_topic_of(d.path)
        if sid:
            staged_topic_topics[sid].update(topics)
        for t in topics:
            topic_to_docs[t].append(d.path)
    vocabulary = frozenset(topic_to_docs)
    doc_entries = [_document_entry(d, vocabulary=vocabulary) for d in included]
    return doc_entries, topic_to_docs, staged_topic_topics


def _pick_links(
    possibles: list[dict[str, Any]],
) -> tuple[dict[str, int], dict[str, str], dict[str, str]]:
    """cluster<-possible edge counts and staging/change pick links, derived
    from the projected possibles (the register is the source of truth for
    both)."""
    cluster_possible_counts: dict[str, int] = defaultdict(int)
    pick_by_staging: dict[str, str] = {}
    for poss in possibles:
        for cid in poss.get("claiming_clusters") or []:
            cluster_possible_counts[cid] += 1
        pick = poss.get("pick")
        if pick and pick.get("staging_id") and pick.get("change_id"):
            pick_by_staging.setdefault(pick["staging_id"], pick["change_id"])
    change_origin_staging = {chg: sid for sid, chg in pick_by_staging.items()}
    return cluster_possible_counts, pick_by_staging, change_origin_staging


def _change_entry(
    change_id: str, status: str, folder: Path, archive_date: str | None,
    repo_root: Path, change_origin_staging: dict[str, str],
) -> dict[str, Any]:
    """One `changes[]` entry, including the folder/files drill-down listing.

    `origin_staging_id` follows a DECLARED PRECEDENCE ORDER rather than one
    source: the change's own recorded staged origin first, then the
    possibles-register pick edge. The order is stated as an order rather than a
    replacement so a pick edge keeps working wherever one still exists; the
    recorded origin leads because it is the source the forward transition writes
    and does not destroy. (An explicitly supplied topic outranks both, and is
    applied by `gate_console.plan_demotion`, which is where a human's argument
    arrives.)"""
    code_surface, target_release = _release_frontmatter(folder)
    change: dict[str, Any] = {
        "id": change_id,
        "status": status,
        "code_surface": code_surface,
        "target_release": target_release,
        "origin_staging_id": (_declared_origin_staging(folder)
                              or change_origin_staging.get(change_id)),
    }
    ratification = _ratification(folder, archive_date, status)
    if ratification:
        change["ratification"] = ratification
    task_progress = _task_progress(folder)
    if task_progress:
        change["task_progress"] = task_progress
    change["folder"] = folder.relative_to(repo_root).as_posix()
    files = _change_files(folder, repo_root)
    if files:
        change["files"] = files
    return change


def _project_changes(
    repo_root: Path, change_origin_staging: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Changes (funnel columns 5-6) plus the id->status map lineage needs."""
    changes: list[dict[str, Any]] = []
    change_status: dict[str, str] = {}
    for change_id, status, folder, archive_date in _iter_changes(repo_root):
        change_status[change_id] = status
        changes.append(_change_entry(change_id, status, folder, archive_date,
                                     repo_root, change_origin_staging))
    changes.sort(key=lambda c: c["id"])
    return changes, change_status


def _folder_member_docs(
    staging_id: str, doc_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """The projected entries for the documents that LIVE in a staging topic's
    folder — health's only inputs (design D8). A document that merely declares
    the topic as a `destinations` target is inbound context and is NOT here."""
    return [e for e in doc_entries if _staging_topic_of(e["path"]) == staging_id]


def _project_staged_topics(
    repo_root: Path, pick_by_staging: dict[str, str],
    doc_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Staged topics (funnel column 4), each carrying its `health` aggregate
    (add-staging-workbench design D8) computed from its FOLDER's own corpus
    documents only."""
    staged_topics: list[dict[str, Any]] = []
    staging_base = repo_root / "ideation" / "staging"
    if not staging_base.is_dir():
        return staged_topics
    for topic_dir in sorted(staging_base.iterdir()):
        if not topic_dir.is_dir():
            continue
        sid = topic_dir.name
        files = sorted(
            p.relative_to(repo_root).as_posix()
            for p in topic_dir.rglob("*") if p.is_file()
        )
        st: dict[str, Any] = {"staging_id": sid}
        if files:
            st["files"] = files
        target_change = pick_by_staging.get(sid)
        if target_change:
            st["target_change"] = target_change
        st["health"] = completeness.topic_health(
            _folder_member_docs(sid, doc_entries))
        staged_topics.append(st)
    return staged_topics


# --------------------------- the gate's live evaluation ---------------------------

def live_topic_health(
    repo_root: Path | str, staging_id: str, *, repository: str = "checkout",
) -> dict[str, Any]:
    """ONE staging topic's health, recomputed LIVE from the pinned checkout —
    the staged-to-proposal readiness gate's input (design D9).

    The snapshot is regenerated nightly, so its `health` object can trail the
    checkout by a working day; a gate that refuses (or worse, allows) on
    yesterday's tree teaches people to distrust it. So the gate never reads the
    served snapshot: it calls this, which scans the pinned tree through the SAME
    projection the snapshot uses (so the vocabulary and edge degrees are the
    same derivation) and aggregates through the SAME `completeness.topic_health`.
    This keeps the generator the sole component that scans the repository — the
    guard itself scans nothing.

    A topic with no folder — or a folder with no corpus documents — yields
    `stub`; the caller's own missing-topic refusal is what distinguishes the two
    (and runs first)."""
    root = Path(repo_root).resolve()
    docs = corpus.load_docs(repository, root)
    doc_entries, _topic_to_docs, _staged = _project_documents(docs, None)
    return completeness.topic_health(_folder_member_docs(staging_id, doc_entries))


def live_tile_scopes(
    repo_root: Path | str, *, repository: str = "checkout",
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`(cluster ids, possible ids)`, recomputed LIVE from the pinned checkout —
    the other two thirds of the LIVE TILE INVENTORY FR-026's scans are checked
    against (007-workbench-branch-sessions; PR #49 review finding 7).

    The route had the ids only because it happened to hold a served snapshot, and
    every CLI session verb passed none — so the SAME checkout yielded two
    different tile universes and G12's cross-tile exclusions were silently OFF on
    the CLI: a gate write on tile `cl-foo` resolved onto tile `cl-foo-2`'s LIVE
    session branch, and `assert_branch_cleanup_permitted` admitted deleting
    another tile's branch. Both refused on HTTP, both permitted on the CLI —
    FR-020's parity promise broken in the destructive direction.

    Derived the same way `generate_snapshot` derives them, and HERE for the same
    reason `live_topic_health` lives here: the generator is the sole component
    that scans the repository, so a second scan elsewhere would be a second
    derivation that could disagree. Cluster ids are `cl-<topic>` over every
    declared `Topics:` keyword (`_project_documents`'s `topic_to_docs`), possible
    ids come from the possibles register. A malformed register yields fewer
    possibles rather than raising — the pinned validator owns conformance — but a
    corpus that cannot be scanned raises, because a SILENTLY narrower inventory is
    exactly the defect this function exists to remove."""
    root = Path(repo_root).resolve()
    docs = corpus.load_docs(repository, root)
    _entries, topic_to_docs, _staged = _project_documents(docs, None)
    clusters = tuple(f"cl-{topic}" for topic in sorted(topic_to_docs))
    try:
        possibles = tuple(
            str(entry["id"]) for entry in
            CrossReferenceIndexAdapter.discover(root).possibles()
            if isinstance(entry, dict) and entry.get("id"))
    except Exception:  # noqa: BLE001 - a malformed register never blocks a session
        possibles = ()
    return clusters, tuple(sorted(set(possibles)))


def _project_clusters(
    topic_to_docs: dict[str, list[str]],
    possibles: list[dict[str, Any]],
    cluster_possible_counts: dict[str, int],
    staged_topic_topics: dict[str, set[str]],
    pick_by_staging: dict[str, str],
    change_status: dict[str, str],
    topic_entry_by_id: dict[str, dict],
) -> list[dict[str, Any]]:
    """Clusters (funnel column 2; D11/D12 working surface). The display name,
    readiness heat, and conflict flags come from the cross-reference index's
    topic entry whose id equals the cluster id (`cl-<topic>`); a cluster absent
    from the index falls back to a titleized name and carries no readiness."""
    clusters: list[dict[str, Any]] = []
    for topic in sorted(topic_to_docs):
        cid = "cl-" + topic
        entry = topic_entry_by_id.get(cid)
        member_docs = sorted(set(topic_to_docs[topic]))
        edges = [{"document": doc_id, "matched_topics": [topic]} for doc_id in member_docs]
        cluster: dict[str, Any] = {
            "id": cid,
            "name": _cluster_name(topic, entry),
            "topics": [topic],
            "document_edges": edges,
            "tallies": {
                "document_links": len(edges),
                "possible_links": cluster_possible_counts.get(cid, 0),
            },
        }
        readiness = _scored_readiness(entry)
        if readiness:
            cluster["readiness"] = readiness
        conflict_flags = _cluster_conflict_flags(entry)
        if conflict_flags:
            cluster["conflict_flags"] = conflict_flags
        lineage = _cluster_lineage(
            cid, topic, possibles, staged_topic_topics, pick_by_staging, change_status)
        if lineage:
            cluster["lineage"] = lineage
        clusters.append(cluster)
    return clusters


def _generation_stamp(
    git: Any, repo_root: Path, source_revision: str | None,
    generated_at: str | None, generator_version: str,
) -> dict[str, Any]:
    """The generation stamp (no wall clock): `generated_at`, when not passed,
    derives from the revision's commit date and is omitted when unresolvable."""
    if source_revision is None:
        source_revision = git.head_sha(repo_root) or "unknown"
    if generated_at is None and source_revision not in (None, "unknown"):
        generated_at = git.commit_date(repo_root, source_revision)
    generation: dict[str, Any] = {
        "source_revision": source_revision,
        "generator_version": generator_version,
    }
    if generated_at:
        generation["generated_at"] = generated_at
    return generation


# --------------------------- the projection ---------------------------

def generate_snapshot(
    repo_root: Path | str,
    repository: str,
    *,
    source_revision: str | None = None,
    generated_at: str | None = None,
    git: Any | None = None,
    generator_version: str = GENERATOR_VERSION,
    project_register_source: Path | None = None,
    possibles_source: Path | None = None,
    excluded_documents: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Scan `repo_root` (one repository) and return the deterministic snapshot
    dict. `source_revision` should be passed explicitly for a stable projection
    (the fixture tree's real HEAD is unstable); when omitted it is read from
    `git.head_sha`. `generated_at`, when not passed, derives from the revision's
    commit date via `git.commit_date` — never the wall clock — and is omitted
    when unresolvable. `git` defaults to a `RealGitDates`; tests inject a
    `FakeGit`.

    `excluded_documents`, when a list is supplied, is populated (in document-path
    order, so it stays deterministic) with `{"path", "reason"}` records for every
    document dropped by `_document_exclusion_reason` — a projection defect that is
    reported, never fatal. The snapshot dict itself stays strictly
    contract-shaped (the exclusion channel is out-of-band)."""
    repo_root = Path(repo_root).resolve()
    git = git or RealGitDates()

    # ---- documents (funnel column 1) ----
    docs = corpus.load_docs(repository, repo_root)
    doc_entries, topic_to_docs, staged_topic_topics = _project_documents(
        docs, excluded_documents)
    path_to_doc_id = {e["path"]: e["id"] for e in doc_entries}

    # ---- cross-reference index (funnel columns 2-3): the possibles register
    #      (projected one-for-one, no fabrication for docs without a
    #      `Possible feats:` section) and the topic entries clusters read their
    #      display name / readiness / conflict flags from ----
    index = (CrossReferenceIndexAdapter(possibles_source) if possibles_source is not None
             else CrossReferenceIndexAdapter.discover(repo_root))
    possibles = fixtures.project_possibles(
        index.possibles(),
        worked_example_docs=fixtures.worked_example_doc_ids(docs),
        path_to_doc_id=path_to_doc_id,
    )
    cluster_possible_counts, pick_by_staging, change_origin_staging = \
        _pick_links(possibles)

    # ---- changes (5-6), staged topics (4), clusters (2) ----
    changes, change_status = _project_changes(repo_root, change_origin_staging)
    staged_topics = _project_staged_topics(repo_root, pick_by_staging, doc_entries)
    clusters = _project_clusters(topic_to_docs, possibles, cluster_possible_counts,
                                 staged_topic_topics, pick_by_staging, change_status,
                                 index.topic_entry_by_id())

    # ---- keyword index (rail seed): DECLARED counts only ----
    keyword_index = [
        {"keyword": topic, "declared_doc_count": len(set(topic_to_docs[topic]))}
        for topic in sorted(topic_to_docs)
    ]

    snapshot: dict[str, Any] = {
        "schema_version": 1,
        "kind": "ideation-dashboard-snapshot",
        "repository": repository,
        "generation": _generation_stamp(git, repo_root, source_revision,
                                        generated_at, generator_version),
        "documents": doc_entries,
        "clusters": clusters,
        "possibles": possibles,
        "staged_topics": staged_topics,
        "changes": changes,
        "keyword_index": keyword_index,
    }

    # ---- project grouping (D10): absent == ungrouped implicit project ----
    project_register = (ProjectRegisterAdapter(project_register_source)
                        if project_register_source is not None
                        else ProjectRegisterAdapter.discover(repo_root))
    project, project_group = project_register.resolve(repository)
    if project:
        snapshot["project"] = project
    if project_group:
        snapshot["project_group"] = project_group
    # ADDITIVE full membership (multi-project ruling, 2026-08-06): every
    # declaring project in register order; first element == the primary above.
    memberships = project_register.projects_of(repository)
    if memberships:
        snapshot["projects"] = memberships

    return snapshot


def _cluster_lineage(
    cid: str,
    topic: str,
    possibles: list[dict[str, Any]],
    staged_topic_topics: dict[str, set[str]],
    pick_by_staging: dict[str, str],
    change_status: dict[str, str],
) -> dict[str, Any]:
    """Downstream funnel progression of a cluster — DISTINCT from its member
    edges. staged_picks = staged topics feeding this cluster (topic match);
    proposals/realized = the active/archived changes those staged picks and this
    cluster's picked possibles flow into."""
    staged_picks = sorted(
        sid for sid, topics in staged_topic_topics.items() if topic in topics)

    change_ids: set[str] = set()
    for poss in possibles:
        if cid in (poss.get("claiming_clusters") or []) and poss.get("state") == "picked":
            change_id = (poss.get("pick") or {}).get("change_id")
            if change_id:
                change_ids.add(change_id)
    for sid in staged_picks:
        change_id = pick_by_staging.get(sid)
        if change_id:
            change_ids.add(change_id)

    proposals = sorted(c for c in change_ids if change_status.get(c) == "active")
    realized = sorted(c for c in change_ids if change_status.get(c) == "archived")

    lineage: dict[str, Any] = {}
    if staged_picks:
        lineage["staged_picks"] = staged_picks
    if proposals:
        lineage["proposals"] = proposals
    if realized:
        lineage["realized"] = realized
    return lineage
