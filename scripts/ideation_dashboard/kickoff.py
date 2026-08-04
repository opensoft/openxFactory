"""Next-step kickoff dispatch under the workflow-gate contract (plan
"kickoff.py"; change task 3.13; US9 T035).

After a recorded ratification the console offers the change's declared
realization outline and dispatches a recorded, gated workflow job (a Speckit
realization workflow in codexFactory; a domain workflow in a DomainxFactory).
It RENDERS job status from records and never executes the workflow itself — the
actual workflow run is external and out of scope; this module records the
DISPATCH DESCRIPTOR only.

Two guards, both structural:

  * HUMAN-ONLY. Kickoff is a gate action, so its entrypoint demands a
    `boundary.HumanGate` via `gate_console.require_human_gate` — an
    OutputBoundary / agent path is rejected and reported, exactly like the
    other gate actions.
  * READINESS-GATED (add-staging-workbench D9). `propose` — the sibling
    staging->proposal commission below — REFUSES a topic whose health is not
    `ready`, recomputed LIVE from the pinned checkout through the generator's
    `live_topic_health` (never the served snapshot). See `_require_ready`.
  * RATIFY-GATED (D17). Kickoff is downstream of the ratify gate: it REFUSES
    (`GateRefused`) a change carrying no recorded ratification. The
    ratification is read the SAME WAY the pinned validator's `--context` rule
    reads it (`ratified_change_ids_from`): from a snapshot's
    `changes[].ratification` and/or a sibling `ratify` gate-action record (or a
    standalone ratification-record artifact) under the records tree. So the
    engine-side refusal and the validator-side `--context` precondition agree
    by construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .gate_console import (
    ACTION_DERIVE_POSSIBLES,
    ACTION_KICKOFF,
    ACTION_PROMOTE_TO_STAGING,
    ACTION_PROPOSE,
    ACTION_RESEARCH_BRIEF,
    ART_WORKFLOW_JOB,
    DEFAULT_RECORDS_DIR,
    GateRefused,
    _prefix,
    _render_yaml,
    _rel_to_records,
    _stamp,
    _utcnow,
    build_gate_action_record,
    find_possible,
    promotability_refusal,
    require_human_gate,
    write_gate_action_record,
)

# The common codexFactory realization workflow. Domain workflows (e.g. a
# MedxFactory diagnosis workflow) pass their own `workflow` id; this is only the
# default for the engineering factory (spec: "commonly a Speckit realization
# workflow in codexFactory").
DEFAULT_WORKFLOW = "speckit-realization"

# The staging->proposal commissioning workflow (add-propose-verb): the same
# recorded-dispatch mechanic as kickoff, one lifecycle boundary earlier. The
# job names the authoring work; an agent lane (or a terminal session, until
# that lane exists) fulfils it as an ordinary OpenSpec change.
DEFAULT_PROPOSAL_WORKFLOW = "proposal-authoring"

WORKFLOW_GATE_CONTRACT = "workflow-gate"
STATUS_DISPATCHED = "dispatched"

# add-wheel-action-verbs (011): the workflows the three new verbs COMMISSION.
# None of these lanes exists yet (NG-001) — a dispatched job is a recorded,
# visible commission a terminal session fulfils by hand, exactly the interim
# posture `propose` and `kickoff` each carried before their lanes ran.
DEFAULT_STAGING_FRAGMENT_WORKFLOW = "staging-fragment-authoring"
DEFAULT_DERIVE_POSSIBLES_WORKFLOW = "derive-possibles"
DEFAULT_RESEARCH_BRIEF_WORKFLOW = "possible-research-brief"


# --------------------------------------------------------------------------
# ratification lookup (agrees with the validator's --context rule)
# --------------------------------------------------------------------------

def ratified_change_ids(*, snapshot: dict | None = None,
                        records_root: Path | str | None = None) -> set[str]:
    """Change ids carrying a recorded ratification — read from a snapshot's
    `changes[].ratification` and/or `ratify` gate-action records (and standalone
    ratification-record artifacts) under `records_root`. Mirrors the pinned
    validator's `ratified_change_ids_from` so engine and validator agree."""
    ids: set[str] = set()
    if snapshot:
        for ch in snapshot.get("changes") or []:
            if isinstance(ch, dict) and ch.get("ratification") and ch.get("id"):
                ids.add(ch["id"])
    root = Path(records_root) if records_root is not None else None
    if root is not None and root.is_dir():
        for fp in sorted(list(root.rglob("*.yaml")) + list(root.rglob("*.yml"))):
            try:
                doc = yaml.safe_load(fp.read_text(encoding="utf-8"))
            except (yaml.YAMLError, OSError):
                continue
            if not isinstance(doc, dict):
                continue
            if doc.get("kind") == "gate-action-record" and doc.get("action") == "ratify":
                cid = (doc.get("target") or {}).get("change_id")
                if cid:
                    ids.add(cid)
            if doc.get("kind") == "ratification-record" and doc.get("change_id"):
                ids.add(doc["change_id"])
    return ids


def is_ratified(change_id: str, *, snapshot: dict | None = None,
                records_root: Path | str | None = None) -> bool:
    return change_id in ratified_change_ids(snapshot=snapshot, records_root=records_root)


# --------------------------------------------------------------------------
# workflow-job dispatch descriptor + kickoff
# --------------------------------------------------------------------------

def build_workflow_job(
    change_id: str, *, workflow: str, outline: str, actor: str, at: str,
    status: str = STATUS_DISPATCHED,
) -> dict:
    """The recorded dispatch descriptor (the `workflow-job` artifact). It NAMES
    the gated workflow to run under the workflow-gate contract; the run itself
    is external — this descriptor is what the console renders status from."""
    return {
        "kind": ART_WORKFLOW_JOB,
        "schema_version": 1,
        "change_id": change_id,
        "workflow": workflow,
        "gate_contract": WORKFLOW_GATE_CONTRACT,
        "realization_outline": outline,
        "status": status,
        "dispatched_by": actor,
        "dispatched_at": at,
    }


@dataclass
class KickoffResult:
    job: dict
    gate_action_record: dict
    record_path: Path
    job_path: Path


def kickoff(
    gate: Any, change_id: str, *, snapshot: dict | None = None,
    outline: str | None = None, workflow: str = DEFAULT_WORKFLOW,
    at: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
    records_root: Path | str | None = None, provenance=None,
) -> KickoffResult:
    """Dispatch the ratified change's next step: write the workflow-job
    descriptor + a gate-action record carrying it. REFUSES (`GateRefused`) a
    change with no recorded ratification. Human-only; the entrypoint demands a
    HumanGate."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    root = records_root if records_root is not None else (human.output.root / records_dir)
    if not is_ratified(change_id, snapshot=snapshot, records_root=root):
        raise GateRefused(
            f"kickoff refused: change {change_id!r} carries no recorded ratification "
            "— kickoff is downstream of the ratify gate (D17). Ratify it first.")

    outline = outline or f"Speckit realization workflow for {change_id} (codexFactory)."
    job = build_workflow_job(change_id, workflow=workflow, outline=outline,
                             actor=human.human_actor, at=at)
    base = f"{_prefix(records_dir)}{change_id}"
    job_path = human.write_gate_artifact(
        f"{base}/kickoff-{_stamp(at)}.workflow-job.yaml",
        _render_yaml(job, "# workflow-job dispatch descriptor — recorded + gated; the workflow runs externally.\n"))
    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_KICKOFF, change_id=change_id, at=at,
        provenance=provenance,
        artifacts=[{"kind": ART_WORKFLOW_JOB, "reference": _rel_to_records(job_path, human)}])
    record_path = write_gate_action_record(human, records_dir, record)
    return KickoffResult(job, record, record_path, job_path)


def job_status(job: dict | str | Path) -> str | None:
    """Render a dispatched job's status FROM ITS RECORD (the console never runs
    the workflow, so status is whatever the descriptor records). Accepts the job
    dict or a path to the descriptor."""
    if isinstance(job, (str, Path)):
        try:
            job = yaml.safe_load(Path(job).read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            return None
    return (job or {}).get("status") if isinstance(job, dict) else None


# --------------------------------------------------------------------------
# propose: staged-topic proposal commissioning (add-propose-verb)
# --------------------------------------------------------------------------

def build_proposal_job(
    topic_id: str, *, workflow: str, outline: str, actor: str, at: str,
    status: str = STATUS_DISPATCHED,
) -> dict:
    """The recorded commissioning descriptor for proposal authoring — the
    same `workflow-job` artifact kind kickoff writes, targeting a staging
    `topic_id` instead of a ratified `change_id`. The console never authors
    the proposal; this descriptor is the recorded commission."""
    return {
        "kind": ART_WORKFLOW_JOB,
        "schema_version": 1,
        "topic_id": topic_id,
        "workflow": workflow,
        "gate_contract": WORKFLOW_GATE_CONTRACT,
        "authoring_outline": outline,
        "status": status,
        "dispatched_by": actor,
        "dispatched_at": at,
    }


# --------------------------------------------------------------------------
# THE SHARED UNDELIVERED-COMMISSION INDEX (add-wheel-action-verbs design D2;
# 011 FR-025/FR-026/FR-027)
#
# One index, keyed by (VERB, TARGET ID), behind every commission verb's
# duplicate refusal. The two-part key is what makes the verbs independent: a
# research brief must not block a promotion on the same possible.
#
# The `<verb>-` FILENAME PREFIX is load-bearing — it is how the scan scopes
# itself to one verb. Renaming a descriptor file silently disables the guard,
# so `_commission_glob` and the writers below must stay in agreement.
#
# `dispatched_propose_topics` keeps its name, signature, and behaviour exactly
# (task 2.3: "propose keeps its behaviour"); it is now a thin wrapper.
# --------------------------------------------------------------------------

#: verb -> the descriptor field carrying that verb's target id.
COMMISSION_TARGET_KEY: dict[str, str] = {
    ACTION_PROPOSE: "topic_id",
    ACTION_PROMOTE_TO_STAGING: "possible_id",
    ACTION_DERIVE_POSSIBLES: "cluster_id",
    ACTION_RESEARCH_BRIEF: "possible_id",
}


def _commission_glob(verb: str) -> str:
    """The descriptor filename pattern for `verb`. The prefix IS the index key
    (see the note above) — keep in step with every writer."""
    return f"{verb}-*.workflow-job.yaml"


def dispatched_commissions(records_root: Path | str | None,
                           verb: str) -> dict[str, Path]:
    """`{target id -> descriptor path}` for DISPATCHED, UNDELIVERED `verb`
    jobs under `records_root`.

    "Undelivered" is exactly `status == STATUS_DISPATCHED`: a delivered or
    retired commission records another status, and that field is human-editable
    in the checkout — which is how a human unblocks a job they fulfilled by
    hand. The PATH is returned, not merely the id, because a duplicate refusal
    has to name the blocking descriptor (FR-026).
    """
    found: dict[str, Path] = {}
    root = Path(records_root) if records_root is not None else None
    if root is None or not root.is_dir():
        return found
    target_key = COMMISSION_TARGET_KEY.get(verb)
    if not target_key:
        return found
    for fp in sorted(root.rglob(_commission_glob(verb))):
        try:
            doc = yaml.safe_load(fp.read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            continue
        if (isinstance(doc, dict) and doc.get("kind") == ART_WORKFLOW_JOB
                and doc.get("status") == STATUS_DISPATCHED and doc.get(target_key)):
            found.setdefault(doc[target_key], fp)
    return found


def dispatched_targets(records_root: Path | str | None, verb: str) -> set[str]:
    """Target ids carrying a dispatched, undelivered `verb` commission."""
    return set(dispatched_commissions(records_root, verb))


def dispatched_propose_topics(records_root: Path | str | None) -> set[str]:
    """Topic ids carrying a dispatched, undelivered `propose` workflow-job
    under `records_root` — the duplicate-commission guard's source of truth
    (a delivered commission records a non-`dispatched` status externally).

    Unchanged in name, signature, and behaviour; now one call into the shared
    index above.
    """
    return dispatched_targets(records_root, ACTION_PROPOSE)


@dataclass
class ProposeResult:
    job: dict
    gate_action_record: dict
    record_path: Path
    job_path: Path


def _require_ready(checkout_root: Path, topic_id: str) -> None:
    """THE STAGED-TO-PROPOSAL READINESS GATE (add-staging-workbench design D9;
    requirement "Staged-to-proposal readiness gate").

    A topic cannot move from staging toward proposal while its open questions
    stand or its documents fall short of the ready bar. The check is evaluated
    LIVE against the pinned checkout at request time — never against the served
    snapshot, which is regenerated nightly and can trail the tree by a working
    day — through the SAME deterministic scoring module the generator uses
    (`completeness`, reached via the generator's `live_topic_health`, the sole
    component that scans the repository). So the tile's health icon and this
    refusal are the same computation over different vintages of the tree, and
    when they disagree THIS one governs.

    The refusal cites the blockers verbatim (each document with standing open
    items and its count; each document below `READY_MIN_SCORE` with its score
    and the constant) and persists NOTHING — it is raised before the first
    write, exactly like the missing-topic and duplicate refusals above.

    NO OVERRIDE (Brett's 2026-07-25 ruling): there is no parameter, header, or
    console affordance that bypasses this — a blocker is cleared by closing it.
    Any future override would be a recorded gate action defined by a successor
    change, never a silent bypass, so nothing here takes a flag.
    """
    from . import completeness  # the ONE scoring module — generator + this guard
    from .generator import live_topic_health  # lazy: mirrors the cycle note above

    health = live_topic_health(checkout_root, topic_id)
    if health.get("status") == completeness.STATUS_READY:
        return
    raise GateRefused(
        f"propose refused: staging topic {topic_id!r} is not ready "
        f"(live health {health.get('status')!r}, recomputed from the pinned "
        f"checkout, not the snapshot) — {completeness.refusal_reason(health)}. "
        "Close the blockers and propose again; v1 carries no override.")


def propose(
    gate: Any, topic_id: str, *, outline: str | None = None,
    workflow: str = DEFAULT_PROPOSAL_WORKFLOW, note: str | None = None,
    at: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
    records_root: Path | str | None = None,
    staging_root: Path | str | None = None,
    session_precondition: Any = None,
    provenance=None,
) -> ProposeResult:
    """Commission proposal authoring for one staging topic: write the
    `workflow-job` descriptor + a `propose` gate-action record. REFUSES a
    topic with no directory under the checkout's `ideation/staging/`, a
    duplicate commission while a dispatched job for the topic is undelivered,
    and — the staged-to-proposal readiness gate (add-staging-workbench) — a
    topic whose LIVE health status is not `ready`. Human-only; the entrypoint
    demands a HumanGate (add-propose-verb).

    `staging_root` redirects the EXISTENCE check only; readiness always
    evaluates the gate's own pinned checkout (`human.output.root`), because
    health is derived from the repository-wide projection (design D9).

    `session_precondition` (007-workbench-branch-sessions T054, FR-023) is an
    OPTIONAL zero-argument callable the caller supplies to refuse a `propose` while
    a live BRANCH SESSION holds the tile. It is a callable because this module must
    not learn what a snapshot registry is, and it is called HERE — after the
    missing-topic and duplicate-dispatch refusals, before the readiness gate and
    before any write — for two reasons: a tile that does not exist or already
    carries an undelivered commission has a MORE SPECIFIC problem than "a session
    holds it", and readiness would otherwise answer first with a misleading reason
    (a tile being worked in a session is, by construction, usually not `ready`, so
    the human would be told to close blockers when the real answer is "resolve the
    session"). `_require_ready`'s position relative to the writes is unchanged."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    root = records_root if records_root is not None else (human.output.root / records_dir)
    staging = (Path(staging_root) if staging_root is not None
               else human.output.root / "ideation" / "staging")
    if not (staging / topic_id).is_dir():
        raise GateRefused(
            f"propose refused: no staging topic {topic_id!r} under "
            f"{staging} — the target must exist in the pinned checkout.")
    if topic_id in dispatched_propose_topics(root):
        raise GateRefused(
            f"propose refused: topic {topic_id!r} already carries a "
            "dispatched, undelivered propose commission — deliver or retire "
            "that job before commissioning again.")
    if session_precondition is not None:
        session_precondition()
    _require_ready(human.output.root, topic_id)

    outline = outline or (
        f"Author the OpenSpec change for staging topic {topic_id!r}: "
        "proposal, design decisions, tasks, spec deltas, strict validation, "
        "README record — delivered for human review and ratification.")
    job = build_proposal_job(topic_id, workflow=workflow, outline=outline,
                             actor=human.human_actor, at=at)
    base = f"{_prefix(records_dir)}{topic_id}"
    job_path = human.write_gate_artifact(
        f"{base}/propose-{_stamp(at)}.workflow-job.yaml",
        _render_yaml(job, "# workflow-job commissioning descriptor — recorded + gated; the authoring runs externally.\n"))
    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_PROPOSE, topic_id=topic_id, at=at,
        notes=note, provenance=provenance,
        artifacts=[{"kind": ART_WORKFLOW_JOB, "reference": _rel_to_records(job_path, human)}])
    record_path = write_gate_action_record(human, records_dir, record)
    return ProposeResult(job, record, record_path, job_path)


# ==========================================================================
# THE THREE COMMISSION VERBS (add-wheel-action-verbs; 011 FR-007/013/017)
#
# ONE MECHANIC, three targets. Each verb writes a `workflow-job` descriptor
# plus a gate-action record carrying it, and performs NONE of the work it
# commissions — the lanes that fulfil these jobs do not exist yet (NG-001).
# This is `propose`'s shape, deliberately reused rather than re-abstracted:
# design D2 requires ONE audit shape across kickoff, propose, and these three.
#
# GUARD ORDER, every verb, all before the first write (FR-024a):
#     human gate -> target existence -> promotability* -> duplicate -> writes
# (*promote-to-staging only). A more specific reason wins: absent beats
# non-promotable, non-promotable beats duplicate.
#
# SOURCES OF TRUTH DIFFER, deliberately (FR-023):
#     promote-to-staging / research-brief -> the PINNED CHECKOUT's register
#     derive-possibles                    -> the SNAPSHOT's cluster set
# The register is mutable between bakes so it must be re-read from the tree; a
# cluster has no register file of its own, so the snapshot IS its source.
#
# NOTHING is written on any refusal path: every guard raises before the first
# `write_gate_artifact` call.
# ==========================================================================


@dataclass
class CommissionResult:
    """What a recorded commission produced. Mirrors `ProposeResult`."""
    job: dict
    gate_action_record: dict
    record_path: Path
    job_path: Path


def build_commission_job(
    verb: str, target_id: str, *, workflow: str, outline: str, actor: str,
    at: str, status: str = STATUS_DISPATCHED, topic_slug: str | None = None,
) -> dict:
    """The recorded commissioning descriptor for one wheel action-row verb —
    the same `workflow-job` artifact kind kickoff and propose write, keyed by
    the verb's own target field (`COMMISSION_TARGET_KEY`)."""
    job = {
        "kind": ART_WORKFLOW_JOB,
        "schema_version": 1,
        COMMISSION_TARGET_KEY[verb]: target_id,
        "workflow": workflow,
        "gate_contract": WORKFLOW_GATE_CONTRACT,
        "authoring_outline": outline,
        "status": status,
        "dispatched_by": actor,
        "dispatched_at": at,
    }
    if topic_slug:
        # OPTIONAL by contract (FR-012): omitted entirely when not supplied, so
        # the fulfilling step chooses the destination topic.
        job["topic_slug"] = topic_slug
    return job


def _locate(descriptor: Path, records_root) -> str:
    """The descriptor as a path the human can act on.

    A bare filename is not locatable once the records tree holds more than a
    handful of jobs, and `dispatched_commissions` returns the PATH precisely
    so the refusal can name it. Relative to the records root when it lies
    below it; otherwise the full path rather than a name that could match
    several files.
    """
    try:
        return str(descriptor.relative_to(Path(records_root)))
    except (TypeError, ValueError):
        return str(descriptor)


def _refuse_duplicate(verb: str, target_id: str, records_root) -> None:
    """Refuse a second commission while an earlier one is undelivered.

    Keyed by (verb, target) so one verb never blocks another on the same
    target (FR-027), and the refusal NAMES the blocking descriptor so the human
    can find it and edit its status (FR-026).
    """
    blocking = dispatched_commissions(records_root, verb).get(target_id)
    if blocking is not None:
        raise GateRefused(
            f"{verb} refused: {target_id!r} already carries a dispatched, "
            f"undelivered {verb} commission ({_locate(blocking, records_root)})"
            " — deliver or retire that job before commissioning again.")


def _commission(
    verb: str, gate: Any, target_id: str, *, workflow: str, outline: str,
    note: str | None, at: str | None, records_dir: str,
    records_root: Path | str | None, provenance, topic_slug: str | None = None,
    precondition=None,
) -> CommissionResult:
    """The shared write half, reached only after every guard has passed."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    root = records_root if records_root is not None else (human.output.root / records_dir)
    if precondition is not None:
        precondition(human)
    _refuse_duplicate(verb, target_id, root)

    job = build_commission_job(verb, target_id, workflow=workflow,
                               outline=outline, actor=human.human_actor, at=at,
                               topic_slug=topic_slug)
    base = f"{_prefix(records_dir)}{target_id}"
    job_path = human.write_gate_artifact(
        f"{base}/{verb}-{_stamp(at)}.workflow-job.yaml",
        _render_yaml(job, "# workflow-job commissioning descriptor — recorded + gated; "
                          "the commissioned work runs externally.\n"))
    record = build_gate_action_record(
        actor=human.human_actor, action=verb, at=at, notes=note,
        provenance=provenance,
        artifacts=[{"kind": ART_WORKFLOW_JOB,
                    "reference": _rel_to_records(job_path, human)}],
        **{COMMISSION_TARGET_KEY[verb]: target_id})
    record_path = write_gate_action_record(human, records_dir, record)
    return CommissionResult(job, record, record_path, job_path)


def promote_to_staging(
    gate: Any, possible_id: str, *, topic: str | None = None,
    outline: str | None = None, workflow: str = DEFAULT_STAGING_FRAGMENT_WORKFLOW,
    note: str | None = None, at: str | None = None,
    records_dir: str = DEFAULT_RECORDS_DIR,
    records_root: Path | str | None = None, provenance=None,
) -> CommissionResult:
    """Commission the organization of ONE ACCEPTED possible into a staging
    fragment. Writes the descriptor + record and NOTHING else.

    The possibles register is NOT mutated (FR-008): the `latent -> picked` pick
    edge needs `pick.staging_id`, and no staging topic exists at commission
    time, so the fulfilling step writes the edge when it delivers the fragment
    (design D4). Refuses an absent register id, a non-promotable possible (see
    `gate_console.promotability_refusal`), a duplicate, and an agent caller.

    Deliberately does NOT inherit `propose`'s staged-readiness gate or its
    branch-session precondition (NG-012): both are defined over a STAGING TOPIC,
    and a possible is not one.
    """
    def _guard(human):
        entry = find_possible(human.output.root, possible_id)
        if entry is None:
            raise GateRefused(
                f"promote-to-staging refused: no possible {possible_id!r} in "
                "the pinned checkout's possibles register.")
        reason = promotability_refusal(entry)
        if reason is not None:
            raise GateRefused(f"promote-to-staging refused: {reason}.")

    outline = outline or (
        f"Organize possible {possible_id!r} into ideation/staging/<topic>/ as a "
        "fragment; deliver the fragment together with the possible's "
        "latent -> picked pick edge citing the real staging id.")
    return _commission(
        ACTION_PROMOTE_TO_STAGING, gate, possible_id, workflow=workflow,
        outline=outline, note=note, at=at, records_dir=records_dir,
        records_root=records_root, provenance=provenance, topic_slug=topic,
        precondition=_guard)


def derive_possibles(
    gate: Any, cluster_id: str, *, snapshot: dict | None = None,
    outline: str | None = None, workflow: str = DEFAULT_DERIVE_POSSIBLES_WORKFLOW,
    note: str | None = None, at: str | None = None,
    records_dir: str = DEFAULT_RECORDS_DIR,
    records_root: Path | str | None = None, provenance=None,
) -> CommissionResult:
    """Commission a CLUSTER-SCOPED run of the promoted possibles-derivation
    lane. Scopes and records a run; derives nothing and creates no register
    entry (FR-013).

    The cluster is validated against the SNAPSHOT's cluster set (FR-014) —
    unlike the two possibles verbs, which read the checkout's register. With no
    snapshot there is no cluster set to validate against, so the commission is
    refused rather than assumed.

    The lane's own contract is unchanged and not restated: delivered candidates
    still arrive `origin: ai-derived` / `pending_review` and still require a
    human disposition (FR-015).
    """
    def _guard(human):
        clusters = (snapshot or {}).get("clusters") if isinstance(snapshot, dict) else None
        if not isinstance(clusters, list):
            raise GateRefused(
                "derive-possibles refused: no snapshot cluster set is available "
                "to validate the target against — the cluster cannot be assumed.")
        if not any(isinstance(c, dict) and c.get("id") == cluster_id for c in clusters):
            raise GateRefused(
                f"derive-possibles refused: cluster {cluster_id!r} is not in the "
                "snapshot's cluster set.")

    outline = outline or (
        f"Run the bounded, read-only derive-possibles lane scoped to cluster "
        f"{cluster_id!r}; candidates arrive origin: ai-derived with machine "
        "disposition pending_review and await a human verdict.")
    return _commission(
        ACTION_DERIVE_POSSIBLES, gate, cluster_id, workflow=workflow,
        outline=outline, note=note, at=at, records_dir=records_dir,
        records_root=records_root, provenance=provenance, precondition=_guard)


def research_brief(
    gate: Any, possible_id: str, *, outline: str | None = None,
    workflow: str = DEFAULT_RESEARCH_BRIEF_WORKFLOW, note: str | None = None,
    at: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
    records_root: Path | str | None = None, provenance=None,
) -> CommissionResult:
    """Commission an evidence brief for a possible BEFORE the human rules on it.

    NO REGISTER-STATE GUARD, deliberately (FR-018a). "Pre-verdict" states that
    the UNDISPOSED case is ACCEPTED — not that a disposed possible is refused.
    The wheel hides the verb once the possible is disposed, so the engine is
    permissive where the view is tidy; a refusal here would encode the wrong
    contract. Guards are existence, duplicate, and the human gate only.

    The brief informs a verdict and never makes one: it does not dispose the
    possible, edit its register entry, or attach evidence to it (FR-018), and it
    is never a precondition for disposing (FR-019).
    """
    def _guard(human):
        if find_possible(human.output.root, possible_id) is None:
            raise GateRefused(
                f"research-brief refused: no possible {possible_id!r} in the "
                "pinned checkout's possibles register.")

    outline = outline or (
        f"Research possible {possible_id!r} before its verdict: sources, prior "
        "art, and overlap with existing capabilities and specs, delivered as "
        "staging-compatible material accompanying the possible. It informs the "
        "human's disposition and never makes it.")
    return _commission(
        ACTION_RESEARCH_BRIEF, gate, possible_id, workflow=workflow,
        outline=outline, note=note, at=at, records_dir=records_dir,
        records_root=records_root, provenance=provenance, precondition=_guard)
