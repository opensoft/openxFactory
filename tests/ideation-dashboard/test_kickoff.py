"""US9 next-step kickoff tests (T036) — the ratify-gated realization dispatch.

Every ratified "Next-step kickoff" scenario, against the fixture change tree:

  * kickoff is REFUSED without a recorded ratification — proven BOTH engine-side
    (`GateRefused`, before any write) AND validator-side (the pinned validator's
    `--context` kickoff-unratified rule);
  * after a console ratify, kickoff SUCCEEDS: it writes a `workflow-job` dispatch
    descriptor and a gate-action record CARRYING it (schema contains-rule),
    validator-clean with the ratified context; `job_status` renders "dispatched"
    from the record;
  * `ratified_change_ids` reads ratification the SAME way the validator does
    (snapshot `changes[].ratification` + sibling ratify records) so engine and
    validator agree;
  * kickoff, like every gate action, refuses an agent / OutputBoundary caller
    and reports it (structural, D16); the console never executes the workflow.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, FakeGit, find_openxfactory_validator

from ideation_dashboard import gate_console as gc
from ideation_dashboard import kickoff as ko
from ideation_dashboard.boundary import AGENT, GATE_SIDE_EFFECT, BoundaryViolation, HumanGate, OutputBoundary
from ideation_dashboard.generator import generate_snapshot

VALIDATOR = find_openxfactory_validator()
CHANGE = "add-ideation-governance"
AT_RATIFY = "2026-07-14T11:00:00Z"
AT_KICKOFF = "2026-07-14T12:00:00Z"


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _snapshot(root: Path) -> dict:
    return generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


def _gate(root: Path) -> HumanGate:
    return HumanGate(root, [gc.DEFAULT_RECORDS_DIR], human_actor="brett")


def _records_root(root: Path) -> Path:
    return root / gc.DEFAULT_RECORDS_DIR


def _validate(path: Path, *extra: str) -> subprocess.CompletedProcess:
    if VALIDATOR is None:
        pytest.skip("pinned openxFactory validator not reachable")
    return subprocess.run([sys.executable, str(VALIDATOR), *extra, str(path)],
                          capture_output=True, text=True)


# ============================================================================
# refusal without a recorded ratification (engine-side AND validator --context)
# ============================================================================

def test_kickoff_is_refused_engine_side_without_ratification(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    with pytest.raises(gc.GateRefused) as ei:
        gc.GateConsole(_gate(root)).kickoff(CHANGE, snapshot=snap, at=AT_KICKOFF)
    assert "ratification" in str(ei.value).lower()
    # nothing was written — the refusal is before any record.
    assert not _records_root(root).exists()


def test_kickoff_record_is_rejected_by_the_validator_without_ratification_context(tmp_path):
    # Build a kickoff record directly (as if authored) and validate it against
    # an empty context — the validator's D17 --context rule must flag it.
    root = _tree(tmp_path)
    # write a kickoff record via a HumanGate (bypassing the engine precondition
    # by pointing kickoff at an empty records tree is not possible; author the
    # record shape and validate it standalone).
    gate = _gate(root)
    record = gc.build_gate_action_record(
        actor="brett", action="kickoff", change_id=CHANGE, at=AT_KICKOFF,
        artifacts=[{"kind": "workflow-job", "reference": "job.yaml"}])
    rec_path = gc.write_gate_action_record(gate, gc.DEFAULT_RECORDS_DIR, record)
    empty = tmp_path / "empty-ctx"
    empty.mkdir()
    proc = _validate(rec_path, "--context", str(empty))
    assert proc.returncode == 1
    assert "kickoff-unratified" in proc.stdout


# ============================================================================
# success after a recorded ratification
# ============================================================================

def test_kickoff_after_ratify_dispatches_a_gated_workflow_job(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    console = gc.GateConsole(_gate(root))

    console.ratify(CHANGE, "Brett", at=AT_RATIFY)
    res = console.kickoff(CHANGE, snapshot=snap, at=AT_KICKOFF)

    # the workflow-job dispatch descriptor was written and is gated + recorded.
    assert res.job_path.is_file()
    assert res.job["kind"] == "workflow-job"
    assert res.job["gate_contract"] == "workflow-gate"
    assert res.job["workflow"] == ko.DEFAULT_WORKFLOW  # speckit-realization
    assert res.job["status"] == "dispatched"
    # the gate-action record CARRIES the workflow-job artifact (contains-rule).
    assert {a["kind"] for a in res.gate_action_record["artifacts"]} == {"workflow-job"}

    # job status renders FROM the record (the console never runs the workflow).
    assert ko.job_status(res.job) == "dispatched"
    assert ko.job_status(res.job_path) == "dispatched"

    # validator: clean with the ratified records tree as context.
    proc = _validate(res.record_path, "--context", str(_records_root(root)))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_kickoff_honours_a_declared_realization_outline_and_workflow(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    console = gc.GateConsole(_gate(root))
    console.ratify(CHANGE, "Brett", at=AT_RATIFY)
    res = console.kickoff(CHANGE, snapshot=snap, at=AT_KICKOFF,
                          outline="Run the MedxFactory diagnosis workflow.",
                          workflow="medx-diagnosis")
    assert res.job["realization_outline"] == "Run the MedxFactory diagnosis workflow."
    assert res.job["workflow"] == "medx-diagnosis"


# ============================================================================
# ratification lookup agrees with the validator; and the agent refusal
# ============================================================================

def test_ratified_change_ids_reads_snapshot_ratification(tmp_path):
    # An archived, ratified change in a snapshot is recognised without any records.
    snap = {"changes": [{"id": "add-x", "ratification": {"ratifier": "b", "date": "2026-07-01"}},
                        {"id": "add-y"}]}
    assert ko.ratified_change_ids(snapshot=snap) == {"add-x"}
    assert ko.is_ratified("add-x", snapshot=snap)
    assert not ko.is_ratified("add-y", snapshot=snap)


def test_ratified_change_ids_reads_sibling_ratify_records(tmp_path):
    root = _tree(tmp_path)
    gc.GateConsole(_gate(root)).ratify(CHANGE, "Brett", at=AT_RATIFY)
    assert CHANGE in ko.ratified_change_ids(records_root=_records_root(root))


def test_kickoff_refuses_an_agent_boundary_and_reports(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    agent = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR], actor=AGENT)
    with pytest.raises(BoundaryViolation) as ei:
        ko.kickoff(agent, CHANGE, snapshot=snap)
    assert ei.value.refusal.kind == GATE_SIDE_EFFECT
    assert agent.refusals and agent.refusals[-1].kind == GATE_SIDE_EFFECT


# ============================================================================
# add-wheel-action-verbs T007 — shared undelivered-commission index
#
# `dispatched_commissions` / `dispatched_targets` generalise the propose-only
# duplicate-commission guard to all four wheel verbs, keyed by (verb, target):
# each verb's target field lives in `COMMISSION_TARGET_KEY`, and the
# `<verb>-*.workflow-job.yaml` filename prefix scopes the on-disk scan so one
# verb's commission can never leak into another verb's index.
#
# These tests are written BEFORE the implementation exists (test-first): the
# expected failure right now is an AttributeError on the missing
# `COMMISSION_TARGET_KEY` / `dispatched_commissions` / `dispatched_targets`
# names, until T007 lands them in kickoff.py.
# ============================================================================

def _write_descriptor(root: Path, verb: str, fields: dict, *,
                      status: str = ko.STATUS_DISPATCHED, kind: str = gc.ART_WORKFLOW_JOB,
                      stamp: str = "20260714T120000Z", folder: str = "target") -> Path:
    """Write a `<verb>-<stamp>.workflow-job.yaml` descriptor (kind/status/fields)
    into `<root>/<folder>/` — mirrors the on-disk shape the index scans without
    needing a full repo fixture."""
    import yaml as yaml_mod
    directory = root / folder
    directory.mkdir(parents=True, exist_ok=True)
    doc = {"kind": kind, "schema_version": 1, "status": status, **fields}
    path = directory / f"{verb}-{stamp}.workflow-job.yaml"
    path.write_text(yaml_mod.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def test_commission_target_key_maps_each_verb_to_its_target_field():
    """COMMISSION_TARGET_KEY names the descriptor field each verb's commission is keyed by."""
    assert ko.COMMISSION_TARGET_KEY[gc.ACTION_PROPOSE] == "topic_id"
    assert ko.COMMISSION_TARGET_KEY[gc.ACTION_PROMOTE_TO_STAGING] == "possible_id"
    assert ko.COMMISSION_TARGET_KEY[gc.ACTION_DERIVE_POSSIBLES] == "cluster_id"
    assert ko.COMMISSION_TARGET_KEY[gc.ACTION_RESEARCH_BRIEF] == "possible_id"


def test_dispatched_commissions_is_keyed_by_verb_and_target(tmp_path):
    """A dispatched promote-to-staging job for pos-a is found under its own verb only."""
    root = tmp_path / "records"
    path = _write_descriptor(root, gc.ACTION_PROMOTE_TO_STAGING,
                             {"possible_id": "pos-a"}, folder="pos-a")
    assert path.is_file()
    assert ko.dispatched_commissions(root, gc.ACTION_PROMOTE_TO_STAGING) == {"pos-a": path}
    assert ko.dispatched_commissions(root, gc.ACTION_RESEARCH_BRIEF) == {}
    assert ko.dispatched_commissions(root, gc.ACTION_PROPOSE) == {}


def test_dispatched_commissions_ignores_non_dispatched_status(tmp_path):
    """Only status == dispatched counts; delivered and retired descriptors are excluded."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_PROMOTE_TO_STAGING, {"possible_id": "pos-b"},
                      status="delivered", folder="pos-b")
    _write_descriptor(root, gc.ACTION_PROMOTE_TO_STAGING, {"possible_id": "pos-c"},
                      status="retired", folder="pos-c")
    assert ko.dispatched_targets(root, gc.ACTION_PROMOTE_TO_STAGING) == set()


def test_dispatched_commissions_ignores_non_workflow_job_kind(tmp_path):
    """A dispatched descriptor whose kind isn't workflow-job is ignored."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_PROMOTE_TO_STAGING, {"possible_id": "pos-d"},
                      kind="gate-action-record", folder="pos-d")
    assert ko.dispatched_targets(root, gc.ACTION_PROMOTE_TO_STAGING) == set()


def test_dispatched_commissions_ignores_descriptor_missing_target_field(tmp_path):
    """A dispatched descriptor missing its verb's target field is ignored."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_PROMOTE_TO_STAGING, {}, folder="pos-e")
    assert ko.dispatched_targets(root, gc.ACTION_PROMOTE_TO_STAGING) == set()


def test_dispatched_targets_cross_verb_independence(tmp_path):
    """A dispatched research-brief job for pos-a does not leak into promote-to-staging's targets."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_RESEARCH_BRIEF, {"possible_id": "pos-a"}, folder="pos-a")
    assert "pos-a" in ko.dispatched_targets(root, gc.ACTION_RESEARCH_BRIEF)
    assert "pos-a" not in ko.dispatched_targets(root, gc.ACTION_PROMOTE_TO_STAGING)


def test_each_verb_is_scoped_by_its_own_target_field(tmp_path):
    """derive-possibles is indexed by cluster_id; a descriptor using topic_id instead is not found."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_DERIVE_POSSIBLES, {"cluster_id": "cl-a"}, folder="cl-a")
    _write_descriptor(root, gc.ACTION_DERIVE_POSSIBLES, {"topic_id": "cl-b"}, folder="cl-b",
                      stamp="20260714T120001Z")
    assert ko.dispatched_targets(root, gc.ACTION_DERIVE_POSSIBLES) == {"cl-a"}


def test_dispatched_propose_topics_is_a_thin_wrapper_over_dispatched_targets(tmp_path):
    """dispatched_propose_topics stays a public alias of dispatched_targets(root, 'propose'), legacy file included."""
    root = tmp_path / "records"
    _write_descriptor(root, gc.ACTION_PROPOSE, {"topic_id": "topic-a"}, folder="topic-a")
    assert ko.dispatched_propose_topics(root) == {"topic-a"}
    assert ko.dispatched_propose_topics(root) == ko.dispatched_targets(root, gc.ACTION_PROPOSE)


def test_dispatched_commissions_tolerates_a_missing_or_non_directory_records_root(tmp_path):
    """An absent, None, or non-directory records root yields an empty index, not a crash."""
    missing = tmp_path / "does-not-exist"
    not_a_dir = tmp_path / "not-a-dir"
    not_a_dir.write_text("nope", encoding="utf-8")
    assert ko.dispatched_commissions(missing, gc.ACTION_PROMOTE_TO_STAGING) == {}
    assert ko.dispatched_commissions(None, gc.ACTION_PROMOTE_TO_STAGING) == {}
    assert ko.dispatched_commissions(not_a_dir, gc.ACTION_PROMOTE_TO_STAGING) == {}
    assert ko.dispatched_targets(missing, gc.ACTION_PROMOTE_TO_STAGING) == set()


def test_dispatched_commissions_skips_malformed_yaml(tmp_path):
    """Malformed YAML in a descriptor file is skipped rather than raising."""
    root = tmp_path / "records"
    directory = root / "pos-f"
    directory.mkdir(parents=True)
    (directory / f"{gc.ACTION_PROMOTE_TO_STAGING}-20260714T120000Z.workflow-job.yaml").write_text(
        "not: [valid yaml", encoding="utf-8")
    assert ko.dispatched_targets(root, gc.ACTION_PROMOTE_TO_STAGING) == set()


# ============================================================================
# add-wheel-action-verbs T013–T016d — the three COMMISSION engines
#
# Each verb records a commission and performs none of the work it commissions:
# one `workflow-job` descriptor plus one gate-action record, and nothing else.
# The invariants these pin are fail-closed ones, so every refusal test also
# asserts that NOTHING was persisted.
# ============================================================================

import yaml as _yaml

from doc_health import derive_possibles as _dp

AT_C = "2026-08-02T09:00:00Z"


def _register_entry(pid="pos-a", state="latent", origin=None, outcome=None):
    entry = {"id": pid, "title": "T", "claim": "c", "state": state,
             "provenance": {"document": "d", "section": "s"}}
    if state in ("rejected", "superseded"):
        entry["reason"], entry["citation"] = "r", "c"
    if state == "picked":
        entry["pick"] = {"staging_id": "topic-x"}
    if origin:
        entry["origin"] = origin
    if origin == "ai-derived":
        entry["derivation"] = {
            "worker_run": {"correlation_id": "D-1",
                           "worker_profile": "derive-possibles",
                           "prompt_contract_version": "v1"},
            "disposition": "pending_review"}
        if outcome:
            entry["derivation"]["human_disposition"] = {
                "outcome": outcome, "authority": "brett"}
    return entry


def _commission_root(tmp_path, register=None, clusters=("cl-a",)):
    """A checkout carrying a possibles register, plus the snapshot the
    cluster-scoped verb validates against."""
    root = tmp_path / "checkout"
    (root / "ideation").mkdir(parents=True)
    index = {"schema_version": 1, "kind": "ideation-cross-reference",
             "repository": "openxFactory",
             "generation": {"source_revision": "e" * 40, "generator_version": "t"},
             "topic_entries": [{"id": c, "name": c,
                                "members": [{"path": "p", "stage": "staged"}]}
                               for c in clusters],
             "possibles_register": [_register_entry()] if register is None else register}
    (root / "ideation" / "cross-reference.yaml").write_text(
        _yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
    return root


def _commission_gate(root, actor="brett"):
    return HumanGate(root, [gc.DEFAULT_RECORDS_DIR], human_actor=actor)


def _snapshot_with(clusters=("cl-a",)):
    return {"clusters": [{"id": c, "name": c} for c in clusters]}


def _register_bytes(root):
    return (root / "ideation" / "cross-reference.yaml").read_bytes()


def _written(root):
    """Every file the commission wrote under the records tree."""
    rec = root / gc.DEFAULT_RECORDS_DIR
    return sorted(p for p in rec.rglob("*") if p.is_file()) if rec.is_dir() else []


# ---- T013 promote-to-staging ---------------------------------------------

def test_promote_to_staging_commissions_and_leaves_the_register_untouched(tmp_path):
    """The accept path: exactly one descriptor + one record, and the possibles
    register is BYTE-IDENTICAL afterwards (FR-008/FR-009, SC-005)."""
    root = _commission_root(tmp_path)
    before = _register_bytes(root)
    res = ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C)
    assert res.job["workflow"] == "staging-fragment-authoring"
    assert res.job["possible_id"] == "pos-a"
    assert res.job["status"] == ko.STATUS_DISPATCHED
    assert _register_bytes(root) == before          # no pick edge, no state change
    assert len(_written(root)) == 2                 # the descriptor and its record


@pytest.mark.parametrize("entry,fragment", [
    (_register_entry(origin="ai-derived"), "no human disposition"),
    (_register_entry(origin="ai-derived", outcome="deferred"), "deferred"),
    (_register_entry(origin="ai-derived", outcome="rejected"), "not 'accepted'"),
    (_register_entry(state="rejected"), "rejected"),
    (_register_entry(state="superseded"), "superseded"),
    (_register_entry(state="picked"), "picked"),
])
def test_promote_to_staging_refuses_every_non_promotable_state(tmp_path, entry, fragment):
    """FR-011: each refused state names itself, and persists nothing."""
    root = _commission_root(tmp_path, register=[entry])
    before = _register_bytes(root)
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), entry["id"], at=AT_C)
    assert fragment in str(exc.value)
    assert _register_bytes(root) == before
    assert _written(root) == []


def test_promote_to_staging_refuses_an_absent_register_id(tmp_path):
    """The target must exist in the PINNED CHECKOUT's register (FR-023)."""
    root = _commission_root(tmp_path)
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-nope", at=AT_C)
    assert "pos-nope" in str(exc.value)
    assert _written(root) == []


def test_promote_to_staging_accepts_a_derived_possible_with_an_accepted_verdict(tmp_path):
    root = _commission_root(
        tmp_path, register=[_register_entry(origin="ai-derived", outcome="accepted")])
    assert ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C).job["possible_id"] == "pos-a"


def test_promote_to_staging_refuses_an_agent_boundary(tmp_path):
    root = _commission_root(tmp_path)
    boundary = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR])
    with pytest.raises(BoundaryViolation):
        ko.promote_to_staging(boundary, "pos-a", at=AT_C)
    assert boundary.refusals and boundary.refusals[0].kind == GATE_SIDE_EFFECT
    assert _written(root) == []


def test_promote_to_staging_refuses_a_duplicate_undelivered_commission(tmp_path):
    root = _commission_root(tmp_path)
    ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C)
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-a",
                              at="2026-08-02T10:00:00Z")
    assert "dispatched" in str(exc.value)
    assert len(_written(root)) == 2                 # the second wrote nothing


def test_the_duplicate_refusal_locates_the_blocking_descriptor(tmp_path):
    """FR-026: the human has to be able to FIND the job to edit its status.
    A bare filename does not locate anything once the records tree holds more
    than a handful of jobs, so the refusal carries the path relative to the
    records root — and that path must actually resolve to the descriptor."""
    root = _commission_root(tmp_path)
    first = ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C)
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-a",
                              at="2026-08-02T10:00:00Z")

    named = str(exc.value).split("(")[1].split(")")[0]
    assert "/" in named, f"refusal named a bare filename: {named!r}"
    records_root = first.job_path.parent
    while records_root.name and not (records_root / named).exists():
        records_root = records_root.parent
    assert (records_root / named).resolve() == first.job_path.resolve()


# ---- T014 derive-possibles -----------------------------------------------

def test_derive_possibles_commissions_against_the_snapshot(tmp_path):
    """The cluster is validated against the SNAPSHOT, not the register
    (FR-014) — the deliberate asymmetry with the two possibles verbs."""
    root = _commission_root(tmp_path)
    res = ko.derive_possibles(_commission_gate(root), "cl-a",
                              snapshot=_snapshot_with(), at=AT_C)
    assert res.job["workflow"] == "derive-possibles"
    assert res.job["cluster_id"] == "cl-a"
    assert len(_written(root)) == 2


def test_derive_possibles_creates_no_register_entry(tmp_path):
    """FR-013: the console derives nothing and adds nothing to the register."""
    root = _commission_root(tmp_path)
    before = _register_bytes(root)
    ko.derive_possibles(_commission_gate(root), "cl-a",
                        snapshot=_snapshot_with(), at=AT_C)
    assert _register_bytes(root) == before


def test_derive_possibles_refuses_a_cluster_absent_from_the_snapshot(tmp_path):
    root = _commission_root(tmp_path)
    with pytest.raises(gc.GateRefused) as exc:
        ko.derive_possibles(_commission_gate(root), "cl-nope",
                            snapshot=_snapshot_with(), at=AT_C)
    assert "cl-nope" in str(exc.value)
    assert _written(root) == []


def test_derive_possibles_refuses_when_no_snapshot_is_available(tmp_path):
    """Fail closed: with no snapshot there is no cluster set to validate
    against, so the commission is refused rather than assumed."""
    root = _commission_root(tmp_path)
    with pytest.raises(gc.GateRefused):
        ko.derive_possibles(_commission_gate(root), "cl-a", snapshot=None, at=AT_C)
    assert _written(root) == []


def test_derive_possibles_refuses_a_duplicate_and_an_agent(tmp_path):
    root = _commission_root(tmp_path)
    ko.derive_possibles(_commission_gate(root), "cl-a",
                        snapshot=_snapshot_with(), at=AT_C)
    with pytest.raises(gc.GateRefused):
        ko.derive_possibles(_commission_gate(root), "cl-a",
                            snapshot=_snapshot_with(), at="2026-08-02T11:00:00Z")
    boundary = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR])
    with pytest.raises(BoundaryViolation):
        ko.derive_possibles(boundary, "cl-a", snapshot=_snapshot_with(), at=AT_C)


# ---- T015 research-brief --------------------------------------------------

def test_research_brief_commissions_and_leaves_the_entry_untouched(tmp_path):
    root = _commission_root(tmp_path)
    before = _register_bytes(root)
    res = ko.research_brief(_commission_gate(root), "pos-a", at=AT_C)
    assert res.job["workflow"] == "possible-research-brief"
    assert res.job["possible_id"] == "pos-a"
    assert _register_bytes(root) == before          # never disposes, never edits
    assert len(_written(root)) == 2


@pytest.mark.parametrize("entry", [
    _register_entry(state="latent", origin="ai-derived"),               # awaiting
    _register_entry(state="latent", origin="ai-derived", outcome="accepted"),
    _register_entry(state="latent", origin="ai-derived", outcome="deferred"),
    _register_entry(state="rejected"),
    _register_entry(state="superseded"),
    _register_entry(state="picked"),
])
def test_research_brief_has_no_register_state_guard(tmp_path, entry):
    """FR-018a: 'pre-verdict' means the UNDISPOSED case is ACCEPTED, not that a
    disposed one is refused. The engine carries NO state guard at all — the view
    hides the verb once disposed, the engine stays permissive. A test asserting
    a refusal here would encode the wrong contract."""
    root = _commission_root(tmp_path, register=[entry])
    assert ko.research_brief(_commission_gate(root), entry["id"], at=AT_C)


def test_research_brief_refuses_absent_id_duplicate_and_agent(tmp_path):
    root = _commission_root(tmp_path)
    with pytest.raises(gc.GateRefused):
        ko.research_brief(_commission_gate(root), "pos-nope", at=AT_C)
    assert _written(root) == []
    ko.research_brief(_commission_gate(root), "pos-a", at=AT_C)
    with pytest.raises(gc.GateRefused):
        ko.research_brief(_commission_gate(root), "pos-a", at="2026-08-02T12:00:00Z")
    boundary = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR])
    with pytest.raises(BoundaryViolation):
        ko.research_brief(boundary, "pos-a", at=AT_C)


def test_a_brief_does_not_block_a_promotion_on_the_same_possible(tmp_path):
    """FR-027: the duplicate guard is keyed by (verb, target), so one verb's
    commission never retires another's."""
    root = _commission_root(tmp_path)
    ko.research_brief(_commission_gate(root), "pos-a", at=AT_C)
    assert ko.promote_to_staging(_commission_gate(root), "pos-a",
                                 at="2026-08-02T13:00:00Z")


# ---- T016 guard order -----------------------------------------------------

def test_absent_target_is_reported_as_absent_not_as_non_promotable(tmp_path):
    """FR-024a: the more specific reason wins."""
    root = _commission_root(tmp_path, register=[])
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-ghost", at=AT_C)
    message = str(exc.value)
    assert "pos-ghost" in message
    assert "latent" not in message      # not a promotability complaint


def test_non_promotable_target_is_reported_by_state_not_as_a_duplicate(tmp_path):
    """A non-promotable possible that ALSO carries an undelivered commission
    reports its state, because that is the more specific problem."""
    root = _commission_root(tmp_path, register=[_register_entry()])
    ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C)   # now dispatched
    index = _yaml.safe_load((root / "ideation" / "cross-reference.yaml").read_text("utf-8"))
    index["possibles_register"][0]["state"] = "rejected"
    index["possibles_register"][0].update(reason="r", citation="c")
    (root / "ideation" / "cross-reference.yaml").write_text(
        _yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-a",
                              at="2026-08-02T14:00:00Z")
    assert "rejected" in str(exc.value)


# ---- T016a audit shape ----------------------------------------------------

@pytest.mark.parametrize("verb,call,target_key,target", [
    ("promote-to-staging", "promote_to_staging", "possible_id", "pos-a"),
    ("research-brief", "research_brief", "possible_id", "pos-a"),
    ("derive-possibles", "derive_possibles", "cluster_id", "cl-a"),
])
def test_commission_record_carries_its_descriptor_and_the_right_target(
        tmp_path, verb, call, target_key, target):
    """FR-028 / design D2 — ONE audit shape across every commission: the record
    references its own workflow-job, targets the verb's own key, and carries NO
    disposition outcome (that belongs to dispose-possible)."""
    root = _commission_root(tmp_path)
    kwargs = {"snapshot": _snapshot_with()} if call == "derive_possibles" else {}
    res = getattr(ko, call)(_commission_gate(root), target, at=AT_C, **kwargs)
    record = _yaml.safe_load(res.record_path.read_text(encoding="utf-8"))
    assert record["action"] == verb
    assert record["target"] == {target_key: target}
    assert "outcome" not in record["target"]
    refs = [a["reference"] for a in record["artifacts"]
            if a["kind"] == gc.ART_WORKFLOW_JOB]
    assert len(refs) == 1
    assert (root / refs[0]).resolve() == res.job_path.resolve()


# ---- T016b descriptor naming (research trap 5) ---------------------------

@pytest.mark.parametrize("call,target,kwargs", [
    ("promote_to_staging", "pos-a", {}),
    ("research_brief", "pos-a", {}),
    ("derive_possibles", "cl-a", {"snapshot": _snapshot_with()}),
])
def test_descriptor_filename_prefix_is_the_duplicate_index_key(
        tmp_path, call, target, kwargs):
    """FR-028a + trap 5: the descriptor lands in the per-target folder under
    `<verb>-<stamp>.workflow-job.yaml`, and the shared index finds it BY that
    verb prefix. Rename the file and the duplicate guard dies silently."""
    root = _commission_root(tmp_path)
    verb = {"promote_to_staging": "promote-to-staging",
            "research_brief": "research-brief",
            "derive_possibles": "derive-possibles"}[call]
    res = getattr(ko, call)(_commission_gate(root), target, at=AT_C, **kwargs)
    assert res.job_path.name.startswith(f"{verb}-")
    assert res.job_path.name.endswith(".workflow-job.yaml")
    assert res.job_path.parent.name == target
    found = ko.dispatched_commissions(root / gc.DEFAULT_RECORDS_DIR, verb)
    assert found == {target: res.job_path}


# ---- T016c the duplicate refusal names the blocking descriptor -----------

def test_duplicate_refusal_names_the_blocking_descriptor_path(tmp_path):
    """FR-026 / SC-007: the human needs a remedy, so the refusal points at the
    file whose status they must edit."""
    root = _commission_root(tmp_path)
    first = ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C)
    with pytest.raises(gc.GateRefused) as exc:
        ko.promote_to_staging(_commission_gate(root), "pos-a",
                              at="2026-08-02T15:00:00Z")
    assert first.job_path.name in str(exc.value)


# ---- T016d the optional topic slug ---------------------------------------

def test_topic_slug_is_omitted_when_not_supplied(tmp_path):
    """FR-012: a commission without a slug is ACCEPTED and records no slug."""
    root = _commission_root(tmp_path)
    job = ko.promote_to_staging(_commission_gate(root), "pos-a", at=AT_C).job
    assert "topic_slug" not in job


def test_topic_slug_is_recorded_when_supplied(tmp_path):
    root = _commission_root(tmp_path)
    job = ko.promote_to_staging(_commission_gate(root), "pos-a",
                                topic="my-topic", at=AT_C).job
    assert job["topic_slug"] == "my-topic"


# ---- T021/T022 the GateConsole delegates (FR-031) ------------------------

@pytest.mark.parametrize("call,target,kwargs", [
    ("promote_to_staging", "pos-a", {}),
    ("research_brief", "pos-a", {}),
    ("derive_possibles", "cl-a", {"snapshot": _snapshot_with()}),
])
def test_each_new_verb_is_reachable_through_its_gate_console_delegate(
        tmp_path, call, target, kwargs):
    """FR-031: the delegates mirror `GateConsole.propose` and reach the same
    engine, so the route and CLI can both go through the console facade."""
    root = _commission_root(tmp_path)
    console = gc.GateConsole(_commission_gate(root))
    res = getattr(console, call)(target, at=AT_C, **kwargs)
    assert res.job_path.is_file() and res.record_path.is_file()
    assert res.job["status"] == ko.STATUS_DISPATCHED


def test_gate_console_construction_still_refuses_an_agent(tmp_path):
    """The facade's own human-only guard is unchanged by the new delegates."""
    root = _commission_root(tmp_path)
    with pytest.raises(BoundaryViolation):
        gc.GateConsole(OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR]))
