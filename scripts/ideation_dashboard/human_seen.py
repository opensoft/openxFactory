"""Human-seen-cluster submission into the cross-reference recommendation queue
(change 3.5; US7 T028).

The T028 blocker cleared 2026-07-14: `add-ideation-cross-reference-readiness`
realized the pending_review intake contract in
`openxFactory/contracts/schemas/ideation-cross-reference.schema.yaml` — the
`human_seen` intake $def (proposer + evidence + `disposition: pending_review`),
the organizer `score_evidence` shape (committed revision, passage hash, section
ref, rationale, confidence, alternatives), and `origin: human-seen` on a
`topic_entry`. This module builds that intake from a workbench reference set,
REFUSES a submission lacking the full evidence contract BEFORE persistence (spec
scenario "A submission lacks evidence": rejected before persistence), and writes
the pending_review entry into the cross-reference queue.

QUEUE LOCATION. The cross-reference index (`ideation/cross-reference.yaml`) is a
GENERATED, deterministic projection owned by the sibling change's machinery; the
dashboard reads it read-through (`register.py`) and never rewrites it. A
human-seen submission is a PENDING-REVIEW proposal that becomes a topic cluster
only on a disposing authority's acceptance (a human gate) — so it lands in a
pending queue under the gitignored `ideation/workbench/` tree (the
`canvas_drafts.py` precedent), NEVER in the generated index. On acceptance a
human folds it into the index, retaining its `origin: human-seen` provenance
(spec scenario "A human-seen cluster is accepted"). It MUST NOT bypass review.

VALIDATION. The submission is wrapped in a minimal `ideation-cross-reference`
index envelope (the kind it becomes on acceptance) and validated by the pinned
openxFactory validator `scripts/validate-ideation-cross-reference.py` — the same
subprocess-delegate pattern `snapshot.py`/`workbench.py` use; the schema is never
restated here. A freshly submitted entry carries no `readiness`, so the
validator's gate/spread arithmetic does not fire, and a no-promoted-fit
`extension_fit` needs no capability resolution.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from output_boundary import OutputBoundary
# The neutral path slug, at its own home rather than through `workbench`
# (openDox under design D3): this module is openxFactory's own engineering
# adapter and STAYS, so the import it used to make is the edge RULING OQ-2
# forbids. OQ-B re-plumb B-1, ruled on `#656` 2026-09-09.
from path_slug import slug

# The pinned cross-reference index validator (add-ideation-cross-reference-
# readiness task 2.3), reached by walking up to the aggregation checkout — the
# same path-agnostic discovery `snapshot.find_validator` uses for the dashboard
# validator.
XREF_VALIDATOR_RELPATH = (
    Path("openxFactory") / "scripts" / "validate-ideation-cross-reference.py"
)

# The pending-review queue — UNDER the gitignored `ideation/workbench/` prefix
# (never the generated index), so a submission is session/proposal state a human
# disposes, exactly like a canvas draft. Kept in sync with the boundary allowlist
# every workbench action already declares (`workbench.WORKBENCH_DIR`).
QUEUE_DIR = "ideation/workbench/cross-reference-queue/"

# Contract literals transcribed from `ideation-cross-reference.schema.yaml` (the
# READ-ONLY truth; never invented here).
KIND = "ideation-cross-reference"
SCHEMA_VERSION = 1
ORIGIN_HUMAN_SEEN = "human-seen"
PENDING_REVIEW = "pending_review"
TAG_SOURCE_TOPICS = "topics-header"

# Field order for a human-readable intake (schema property order).
_ENTRY_ORDER = ("id", "name", "topics", "tag_sources", "origin", "members",
                "extension_fit", "human_seen")
_MEMBER_ORDER = ("repository", "path", "stage", "document", "matched_tags")
_HUMAN_SEEN_ORDER = ("proposer", "recipe_reference", "disposition", "evidence")
_EVIDENCE_ORDER = ("source_ref", "rationale", "confidence", "alternatives", "disposition")
_SOURCE_REF_ORDER = ("repository", "path", "revision", "section", "passage_sha256")

# The two contract FORMATS JSON Schema would only catch after a write; enforced
# here so nothing malformed reaches the queue (routing-reference kernel:
# `passage_sha256` 64-hex, `full_commit_revision` 40- or 64-hex lowercase).
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REVISION_RE = re.compile(r"^([0-9a-f]{40}|[0-9a-f]{64})$")


class SubmissionRefused(Exception):
    """A human-seen submission refused BEFORE persistence — the full organizer
    evidence contract is incomplete or malformed (missing proposer / passage
    hash / revision / section / rationale, a bad confidence, etc.). Raised, never
    silent (spec scenario "A submission lacks evidence": rejected before
    persistence)."""


class SubmissionInvalid(Exception):
    """A written submission failed the pinned cross-reference validator (or it
    could not run) — the schema-valid-at-every-write safety net."""


@dataclass
class HumanSeenSubmission:
    """The human-authored evidence + provenance for a human-seen cluster — the
    ORGANIZER evidence contract the panel's tier scores use (NOT the lighter
    cataloger pin). `alternatives` is a (possibly empty) list, exactly as the
    organizer requires; `extension_fit` defaults to an explicit no-promoted-fit
    statement (a freshly-seen set is exploratory)."""
    proposer: str
    repository: str
    path: str
    revision: str
    section: str
    passage_sha256: str
    rationale: str
    confidence: float
    alternatives: Sequence[str] = ()
    recipe_reference: str | None = None
    extension_fit: Mapping[str, Any] | None = None


@dataclass
class SubmissionResult:
    """The outcome of a successful human-seen submission."""
    path: Path        # the queue entry written on disk
    relpath: str      # its repo-relative path (the action_history reference)
    index: dict       # the intake wrapped in its ideation-cross-reference envelope
    cluster_id: str   # the topic-entry id it will carry on acceptance


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _reorder(entry: dict, order: Sequence[str]) -> dict:
    out: dict[str, Any] = {}
    for key in order:
        if key in entry and entry[key] is not None:
            out[key] = entry[key]
    for key, value in entry.items():  # keep forward-compatible unknowns (additive)
        if key not in out and value is not None:
            out[key] = value
    return out


# --------------------------------------------------------------------------
# evidence completeness — refuse BEFORE persistence
# --------------------------------------------------------------------------

def require_complete_evidence(sub: HumanSeenSubmission) -> None:
    """Refuse a submission missing ANY required evidence field, or carrying a
    malformed passage hash / revision / confidence, BEFORE any write (spec
    scenario "A submission lacks evidence"). This is the gate that keeps an
    incomplete human-seen proposal out of the queue entirely."""
    missing: list[str] = []
    if not _nonempty(sub.proposer):
        missing.append("proposer")
    for name, value in (
        ("evidence.source_ref.repository", sub.repository),
        ("evidence.source_ref.path", sub.path),
        ("evidence.source_ref.revision", sub.revision),
        ("evidence.source_ref.section", sub.section),
        ("evidence.source_ref.passage_sha256", sub.passage_sha256),
        ("evidence.rationale", sub.rationale),
    ):
        if not _nonempty(value):
            missing.append(name)
    if missing:
        raise SubmissionRefused(
            f"human-seen submission is missing required evidence {sorted(set(missing))} — "
            "the full organizer evidence contract (proposer + committed revision + "
            "passage hash + section ref + rationale + confidence + alternatives) is "
            "required; a submission without it is rejected before persistence")

    if not isinstance(sub.confidence, (int, float)) or isinstance(sub.confidence, bool) \
            or not (0.0 <= float(sub.confidence) <= 1.0):
        raise SubmissionRefused(
            f"evidence.confidence {sub.confidence!r} must be a number in [0, 1]")
    if not _SHA256_RE.match(sub.passage_sha256):
        raise SubmissionRefused(
            f"evidence.source_ref.passage_sha256 {sub.passage_sha256!r} must be the "
            "64-hex sha256 of the pinned passage")
    if not _REVISION_RE.match(sub.revision):
        raise SubmissionRefused(
            f"evidence.source_ref.revision {sub.revision!r} must be a FULL committed "
            "revision (40- or 64-hex lowercase), never an abbreviation")
    if not isinstance(sub.alternatives, (list, tuple)):
        raise SubmissionRefused("evidence.alternatives must be a list (possibly empty)")
    # The contract types each alternative as a non-empty string
    # (`alternatives.items = {type: string, minLength: 1}`). With validate=False
    # (the default) nothing else guards the list CONTENTS, so a non-string or an
    # empty/blank string would otherwise be serialized into the queue; refuse it
    # here, before persistence, exactly like every other malformed evidence field.
    bad = [alt for alt in sub.alternatives if not _nonempty(alt)]
    if bad:
        raise SubmissionRefused(
            f"evidence.alternatives entries must be non-empty strings; got {bad!r} "
            "(contract: alternatives items are strings with minLength 1)")


# --------------------------------------------------------------------------
# intake builders (topic_entry with origin: human-seen + human_seen block)
# --------------------------------------------------------------------------

def build_evidence(sub: HumanSeenSubmission) -> dict:
    """The organizer `score_evidence` block: source_ref (repository + POSIX path +
    FULL revision + section + passage hash) + rationale + confidence + alternatives
    + `disposition: pending_review`."""
    source_ref = _reorder({
        "repository": sub.repository,
        "path": sub.path,
        "revision": sub.revision,
        "section": sub.section,
        "passage_sha256": sub.passage_sha256,
    }, _SOURCE_REF_ORDER)
    return _reorder({
        "source_ref": source_ref,
        "rationale": sub.rationale,
        "confidence": float(sub.confidence),
        "alternatives": list(sub.alternatives),
        "disposition": PENDING_REVIEW,
    }, _EVIDENCE_ORDER)


def _default_extension_fit() -> dict:
    return {
        "has_promoted_fit": False,
        "statement": ("No promoted capability is claimed; this is an exploratory "
                      "human-seen set awaiting review."),
    }


def _snapshot_docs(snapshot: Mapping) -> dict[str, dict]:
    return {d["id"]: d for d in (snapshot.get("documents") or [])
            if isinstance(d, dict) and d.get("id")}


def build_members(member_ids: Sequence[str], snapshot: Mapping, *,
                  matched_topics: Sequence[str] = ()) -> list[dict]:
    """One `member` per workbench document, joining the snapshot for its `stage`
    (the controlled `Status:` value) and repo-relative `path`. Refuses a member
    absent from the snapshot — its stage cannot be resolved without fabrication."""
    docs = _snapshot_docs(snapshot)
    checked = set(matched_topics)
    members: list[dict] = []
    for doc_id in member_ids:
        doc = docs.get(doc_id)
        if doc is None:
            raise SubmissionRefused(
                f"workbench member {doc_id!r} is not in the snapshot — its stage cannot "
                "be resolved without fabrication; regenerate the snapshot first")
        member: dict[str, Any] = {"path": doc.get("path") or doc_id, "stage": doc.get("stage")}
        if doc.get("id"):
            member["document"] = doc["id"]
        matched = [t for t in (doc.get("topics") or []) if t in checked]
        if matched:
            member["matched_tags"] = matched
        members.append(_reorder(member, _MEMBER_ORDER))
    return members


def build_intake_entry(*, cluster_id: str, name: str, topics: Sequence[str],
                       members: Sequence[dict], submission: HumanSeenSubmission,
                       recipe_reference: str | None = None,
                       tag_sources: Sequence[str] = (TAG_SOURCE_TOPICS,)) -> dict:
    """The `topic_entry` a human-seen submission becomes on acceptance: origin
    `human-seen` + the required `human_seen` intake block (proposer + evidence +
    `pending_review`). Refuses a topic-less cluster (the schema requires at least
    one defining topic)."""
    if not topics:
        raise SubmissionRefused(
            "a human-seen cluster requires at least one topic (the recipe's checked "
            "keywords define the intensional cluster)")
    human_seen = {
        "proposer": submission.proposer,
        "disposition": PENDING_REVIEW,
        "evidence": build_evidence(submission),
    }
    ref = recipe_reference if recipe_reference is not None else submission.recipe_reference
    if ref:
        human_seen["recipe_reference"] = ref
    fit = dict(submission.extension_fit) if submission.extension_fit else _default_extension_fit()
    entry = {
        "id": cluster_id,
        "name": name,
        "topics": list(topics),
        "tag_sources": list(tag_sources),
        "origin": ORIGIN_HUMAN_SEEN,
        "members": list(members),
        "extension_fit": fit,
        "human_seen": _reorder(human_seen, _HUMAN_SEEN_ORDER),
    }
    return _reorder(entry, _ENTRY_ORDER)


def build_index(entry: dict, *, repository: str | None, source_revision: str,
                generator_version: str | None = None) -> dict:
    """Wrap a single intake entry in the minimal `ideation-cross-reference` index
    envelope the pinned validator recognises — the kind the entry becomes on
    acceptance. `generated_at` is deliberately OMITTED (the index derives it from
    the revision, never the wall clock); this queue entry carries only the anchor
    revision the evidence pins cite."""
    generation: dict[str, Any] = {"source_revision": source_revision}
    if generator_version:
        generation["generator_version"] = generator_version
    index: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
    }
    if repository:
        index["repository"] = repository
    index["generation"] = generation
    index["topic_entries"] = [entry]
    return index


# --------------------------------------------------------------------------
# paths + render + write + validate
# --------------------------------------------------------------------------

def queue_relpath(cluster_id: str) -> str:
    """Repo-relative queue path under the gitignored cross-reference queue."""
    return f"{QUEUE_DIR}{slug(cluster_id)}.human-seen.yaml"


def render_submission(index: dict) -> str:
    """Serialize the intake index to YAML with a provenance banner."""
    body = yaml.safe_dump(index, sort_keys=False, default_flow_style=False, allow_unicode=True)
    header = (
        "# Human-seen cluster submission (change 3.5 / T028) — a pending_review\n"
        "# proposal into the cross-reference recommendation queue. GITIGNORED session\n"
        "# state under ideation/workbench/ (never the generated index); a disposing\n"
        "# authority reviews it and, on acceptance, folds it into\n"
        "# ideation/cross-reference.yaml as a topic cluster (origin: human-seen).\n"
    )
    return header + body


def find_cross_reference_validator(start: Path | None = None) -> Path | None:
    """Walk up from `start` (or cwd) to the aggregation checkout and return the
    pinned cross-reference validator, or None when no openxFactory checkout is
    reachable — path-agnostic, mirroring `snapshot.find_validator`."""
    base = (start or Path.cwd()).resolve()
    for directory in [base, *base.parents]:
        candidate = directory / XREF_VALIDATOR_RELPATH
        if candidate.is_file():
            return candidate
    return None


@dataclass
class SubmissionValidation:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    validator: Path | None

    def summary(self) -> str:
        if self.validator is None:
            return "cross-reference validator not found (no reachable openxFactory checkout)"
        tail = (self.stdout or self.stderr).strip().splitlines()
        return tail[-1] if tail else f"returncode={self.returncode}"


def validate_submission(path: Path | str, *, validator: Path | None = None,
                        repo: Path | str | None = None, strict: bool = False,
                        search_from: Path | None = None) -> SubmissionValidation:
    """Validate a written submission with the pinned cross-reference validator
    (single-file mode, kind auto-detected). `--repo` supplies the capability set
    for any promoted extension-fit citation; it defaults to the validator's own
    openxFactory checkout."""
    path = Path(path).resolve()
    validator = validator or find_cross_reference_validator(search_from or path.parent)
    if validator is None:
        return SubmissionValidation(False, -1, "", "cross-reference validator not found", None)
    repo = repo if repo is not None else validator.resolve().parents[1]
    cmd = [sys.executable, str(validator), str(path), "--repo", str(repo)]
    if strict:
        cmd.append("--strict")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return SubmissionValidation(proc.returncode == 0, proc.returncode,
                                proc.stdout, proc.stderr, validator)


# --------------------------------------------------------------------------
# the high-level submission path (workbench set -> queue entry)
# --------------------------------------------------------------------------

def _recipe_checked(w) -> list[str]:
    recipe = w.data.get("recipe") or {}
    return list(recipe.get("checked") or [])


def submit_from_workbench(
    w, snapshot: Mapping, submission: HumanSeenSubmission, boundary: OutputBoundary, *,
    now: str | None = None, relpath: str | None = None,
    validate: bool = False, validator: Path | None = None, repo: Path | str | None = None,
) -> SubmissionResult:
    """Build the human-seen intake from the workbench reference set + the
    submission evidence, REFUSE before persistence when the evidence is
    incomplete, write the `pending_review` entry into the cross-reference queue
    THROUGH the boundary, and (validate=True) re-check it with the pinned
    cross-reference validator. Never rewrites the generated index — the queue is
    gitignored proposal state a human disposes.

    Returns the SubmissionResult (queue path + intake). Raises `SubmissionRefused`
    on incomplete evidence and `SubmissionInvalid` on a validator failure. `now`
    is accepted for action-threading symmetry with the other workbench actions;
    the submission itself carries NO wall-clock stamp (the index derives its
    provenance from `source_revision`, never the clock)."""
    _ = now  # intentionally clock-free (see docstring)
    require_complete_evidence(submission)                       # refuse BEFORE any write

    # ONE determinism anchor (finding 4). The cross-reference envelope's
    # `generation.source_revision` and the human_seen evidence
    # `source_ref.revision` are BOTH full-commit provenance anchors, and the
    # contract treats them as the SAME corpus snapshot (the schema reuses the
    # snapshot's `generation` verbatim; "scores cite exactly this corpus
    # snapshot"). So when the workbench snapshot names a revision it MUST equal
    # the submission's cited revision — otherwise the queue entry would record two
    # conflicting anchors. Refuse the mismatch before persistence (the module's
    # refuse-before-write discipline) rather than silently privileging one; when
    # the snapshot carries no revision there is no conflict and the evidence
    # revision stands as the sole anchor.
    snapshot_revision = (snapshot.get("generation") or {}).get("source_revision")
    if snapshot_revision and snapshot_revision != submission.revision:
        raise SubmissionRefused(
            f"provenance anchor mismatch: the workbench snapshot was generated at "
            f"{snapshot_revision!r} but the submission evidence pins revision "
            f"{submission.revision!r}. The cross-reference envelope carries ONE "
            "determinism anchor (generation.source_revision) that the evidence "
            "source_ref.revision must cite; regenerate the snapshot at the cited "
            "revision, or cite the passage at the snapshot revision, so they agree")

    checked = _recipe_checked(w)
    member_ids = w.member_documents()
    # Topics DEFINE the cluster (schema `topics`, minItems 1). A recipe-seeded set
    # takes its checked keywords (the intensional definition); an ad-hoc set
    # (seed.kind ad-hoc / no recipe.checked) has none, so — matching the schema's
    # "bootstrapped from the Topics: headers" — fall back to the union of the
    # member documents' declared topics from the snapshot (finding 2). A genuinely
    # topic-less set (no recipe AND no member carries a topic) is still refused by
    # build_intake_entry.
    docs = _snapshot_docs(snapshot)
    topics = list(checked) or sorted({
        t for doc_id in member_ids for t in (docs.get(doc_id, {}).get("topics") or [])})
    members = build_members(member_ids, snapshot, matched_topics=topics)
    name = w.data.get("name") or "human-seen set"
    cluster_id = f"human-seen-{slug(name)}"

    # The recipe is offered as rationale (change 3.10): a re-runnable pointer to
    # the workbench set / keyword-lens recipe that formed this human-seen cluster.
    recipe_reference = submission.recipe_reference
    if recipe_reference is None and checked:
        recipe_reference = (f"workbench:{w.data.get('name', name)} "
                            f"(keyword lens: {', '.join(checked)})")

    entry = build_intake_entry(cluster_id=cluster_id, name=name, topics=topics,
                               members=members, submission=submission,
                               recipe_reference=recipe_reference)
    # The envelope anchor is the evidence revision — equal to the snapshot revision
    # when the snapshot names one (enforced above), else the evidence revision alone.
    source_revision = snapshot_revision or submission.revision
    index = build_index(entry, repository=snapshot.get("repository"),
                        source_revision=source_revision)

    rel = relpath or queue_relpath(cluster_id)
    written = boundary.write_output(rel, render_submission(index))
    if validate:
        result = validate_submission(written, validator=validator, repo=repo,
                                     search_from=written.parent)
        if not result.ok:
            raise SubmissionInvalid(
                f"{written}: {result.summary()}\n{result.stdout}{result.stderr}".rstrip())
    return SubmissionResult(path=written, relpath=rel, index=index, cluster_id=cluster_id)
