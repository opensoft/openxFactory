"""The staged-to-proposal readiness gate (openxFactory `add-staging-workbench`,
change tasks 3.1-3.3; design D9).

`propose` refuses a staging topic whose health is not `ready`, evaluated LIVE
against the pinned checkout with the SAME deterministic scoring the generator
uses. Every scenario of the "Staged-to-proposal readiness gate" requirement:

  * a topic with standing open questions is refused, naming each document and its
    standing count; a topic whose questions are all closed but whose document is
    under the threshold is refused, citing that score against the contract
    constant; a `stub` folder is refused too;
  * a ready topic commissions exactly as `add-propose-verb` realized it —
    workflow-job descriptor plus a `propose` gate-action record;
  * every refusal persists NOTHING (no job, no record, no directory), like the
    existing missing-topic and duplicate refusals it sits beside;
  * STALENESS: a snapshot showing `ready` does not help — the live evaluation
    governs, citing the marker the snapshot has not yet seen;
  * NO OVERRIDE (Brett's 2026-07-25 ruling): no argument, no keyword, no
    environment variable bypasses the guard;
  * the action stays HUMAN-ONLY — the agent path is refused before the gate is
    even consulted.

The guard lives at the propose ENGINE (`kickoff.propose`), the single choke point
every surface passes through — the loopback route (`gate_routes`), the CLI
(`cli gate propose`), and a direct call all reach it, so all three are gated
identically; `test_gate_routes.py` covers the same refusal over real HTTP.
"""

from __future__ import annotations

import inspect
import shutil
from pathlib import Path

import pytest

from conftest import (  # noqa: F401  (sys.path side effect)
    BASE_REPO, PINNED_REVISION, FakeGit, staging_fragment, thin_fragment,
)

from ideation_dashboard import cli
from ideation_dashboard import completeness as C
from ideation_dashboard import gate_console as gc
from ideation_dashboard import kickoff as ko
from ideation_dashboard.boundary import (
    AGENT, GATE_SIDE_EFFECT, BoundaryViolation, HumanGate, OutputBoundary,
)
from ideation_dashboard.generator import generate_snapshot

AT = "2026-07-25T12:00:00Z"


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _gate(root: Path) -> HumanGate:
    return HumanGate(root, [gc.DEFAULT_RECORDS_DIR], human_actor="brett")


def _stage(root: Path, topic: str, text: str | None = None) -> str:
    """Put one document in a staging topic folder; return its repo-relative path."""
    folder = root / "ideation" / "staging" / topic
    folder.mkdir(parents=True, exist_ok=True)
    rel = f"ideation/staging/{topic}/{topic}.md"
    if text is not None:
        (root / rel).write_text(text, encoding="utf-8")
    return rel


def _persisted(root: Path) -> list[Path]:
    """Everything a commission would leave behind: the workflow-job descriptor
    and the gate-action record. A refusal leaves this empty."""
    return sorted(root.rglob("*.workflow-job.yaml")) + \
        sorted(root.rglob("*.gate-action.yaml"))


def _propose(root: Path, topic: str, *, at: str = AT, **kw):
    return gc.GateConsole(_gate(root)).propose(topic, at=at, **kw)


# ============================================================================
# refusals — each blocker cited concretely, nothing persisted
# ============================================================================

def test_a_topic_with_standing_open_questions_is_refused_naming_document_and_count(tmp_path):
    root = _tree(tmp_path)
    rel = _stage(root, "gate-topic",
                 staging_fragment("Gate Topic", "gate-topic", resolved=False))
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "gate-topic")
    message = str(ei.value)
    assert "not ready" in message and "developing" in message
    assert f"{rel} carries 2 standing open items" in message
    assert _persisted(root) == []          # the refusal persists NOTHING


def test_a_standing_marker_token_blocks_the_same_way(tmp_path):
    root = _tree(tmp_path)
    rel = _stage(root, "gate-topic",
                 staging_fragment("Gate Topic", "gate-topic",
                                  markers=("TODO — decide the exit path.",)))
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "gate-topic")
    assert f"{rel} carries 1 standing open item" in str(ei.value)
    assert _persisted(root) == []


def test_closed_questions_but_an_underdone_document_is_refused_citing_the_constant(tmp_path):
    root = _tree(tmp_path)
    rel = _stage(root, "thin-topic", thin_fragment("Thin Topic", "thin-topic"))
    health = generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION,
                              git=FakeGit())
    score = next(t for t in health["staged_topics"]
                 if t["staging_id"] == "thin-topic")["health"]["doc_score_min"]
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "thin-topic")
    message = str(ei.value)
    assert "standing open" not in message          # every question IS closed
    assert f"{rel} scores {score} below READY_MIN_SCORE {C.READY_MIN_SCORE}" in message
    assert _persisted(root) == []


def test_a_stub_folder_is_refused_with_the_one_fact_it_has(tmp_path):
    root = _tree(tmp_path)
    _stage(root, "stub-topic")                     # folder exists, no corpus doc
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "stub-topic")
    assert "stub" in str(ei.value)
    assert "no corpus documents" in str(ei.value)
    assert _persisted(root) == []


def test_the_existing_refusals_stand_unchanged(tmp_path):
    root = _tree(tmp_path)
    _stage(root, "gate-topic", staging_fragment("Gate Topic", "gate-topic"))
    # missing topic — still the first refusal, before any readiness scan
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "no-such-topic")
    assert "no staging topic" in str(ei.value)
    # duplicate commission — still refused after a ready topic commissions once
    _propose(root, "gate-topic")
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "gate-topic", at="2026-07-25T13:00:00Z")
    assert "already carries a dispatched" in str(ei.value)


# ============================================================================
# the ready path — the commission proceeds exactly as add-propose-verb realized
# ============================================================================

def test_a_ready_topic_commissions_the_descriptor_and_the_gate_action_record(tmp_path):
    root = _tree(tmp_path)
    _stage(root, "gate-topic", staging_fragment("Gate Topic", "gate-topic"))
    res = _propose(root, "gate-topic")
    assert res.job["kind"] == "workflow-job"
    assert res.job["topic_id"] == "gate-topic"
    assert res.job["workflow"] == ko.DEFAULT_PROPOSAL_WORKFLOW
    assert res.job["status"] == "dispatched"
    assert res.job["gate_contract"] == ko.WORKFLOW_GATE_CONTRACT
    assert res.gate_action_record["action"] == gc.ACTION_PROPOSE
    assert res.gate_action_record["target"] == {"topic_id": "gate-topic"}
    assert {a["kind"] for a in res.gate_action_record["artifacts"]} == {"workflow-job"}
    assert res.job_path.is_file() and res.record_path.is_file()


def test_the_gate_reads_the_topic_folder_only(tmp_path):
    # a blocked SIBLING topic, and an unfinished note that names this topic as a
    # destination, must not hold a finished fragment hostage (design D8)
    root = _tree(tmp_path)
    _stage(root, "gate-topic", staging_fragment("Gate Topic", "gate-topic"))
    _stage(root, "other-topic",
           staging_fragment("Other", "gate-topic", resolved=False,
                            markers=("TODO — unrelated.",)))
    assert _propose(root, "gate-topic").job["topic_id"] == "gate-topic"


# ============================================================================
# staleness: the live evaluation governs (design D9)
# ============================================================================

def test_a_snapshot_saying_ready_does_not_help_once_the_checkout_gains_a_marker(tmp_path):
    root = _tree(tmp_path)
    rel = _stage(root, "gate-topic", staging_fragment("Gate Topic", "gate-topic"))
    stale = generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION,
                             git=FakeGit())
    assert next(t for t in stale["staged_topics"]
                if t["staging_id"] == "gate-topic")["health"]["status"] == C.STATUS_READY

    # the tree moves on; the served snapshot does not (it is regenerated nightly)
    (root / rel).write_text(
        staging_fragment("Gate Topic", "gate-topic",
                         markers=("TODO — a question re-opened after the snapshot.",)),
        encoding="utf-8")
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "gate-topic")
    assert f"{rel} carries 1 standing open item" in str(ei.value)
    assert "pinned checkout, not the snapshot" in str(ei.value)
    assert _persisted(root) == []
    # the stale snapshot still says ready — display truth only, never the gate's
    assert next(t for t in stale["staged_topics"]
                if t["staging_id"] == "gate-topic")["health"]["status"] == C.STATUS_READY


# ============================================================================
# no override, one choke point, human-only
# ============================================================================

def test_no_parameter_or_keyword_can_bypass_the_gate(tmp_path):
    root = _tree(tmp_path)
    _stage(root, "gate-topic",
           staging_fragment("Gate Topic", "gate-topic", resolved=False))
    # v1 carries NO override path: propose exposes no force/override/skip knob
    params = set(inspect.signature(ko.propose).parameters)
    assert not {p for p in params
                if any(word in p for word in ("force", "override", "bypass", "skip",
                                              "ignore", "unsafe"))}
    assert not {p for p in set(inspect.signature(gc.GateConsole.propose).parameters)
                if any(word in p for word in ("force", "override", "bypass", "skip"))}
    # ...and the console says so in its refusal, so the honest response is to
    # close the blocker
    with pytest.raises(gc.GateRefused) as ei:
        _propose(root, "gate-topic")
    assert "no override" in str(ei.value)
    # the CLI exposes no bypass flag either
    cli_source = Path(inspect.getsourcefile(cli)).read_text("utf-8")
    for flag in ("--force", "--override", "--skip-readiness", "--no-gate"):
        assert flag not in cli_source, flag


def test_the_guard_sits_at_the_one_choke_point_every_surface_passes_through():
    # the loopback route and the CLI both execute propose through the console,
    # which is `kickoff.propose` — so all three surfaces are gated identically.
    from ideation_dashboard import gate_routes
    assert "propose" in gate_routes.EXECUTING_VERBS
    assert "kickoff_mod.propose" in inspect.getsource(gc.GateConsole.propose)
    assert "console.propose" in inspect.getsource(cli.cmd_gate_propose)
    assert "_require_ready" in inspect.getsource(ko.propose)


def test_the_agent_path_is_still_rejected_before_the_gate_is_consulted(tmp_path):
    root = _tree(tmp_path)
    _stage(root, "gate-topic", staging_fragment("Gate Topic", "gate-topic"))
    agent = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR], actor=AGENT)
    with pytest.raises(BoundaryViolation) as ei:
        ko.propose(agent, "gate-topic", at=AT)
    assert ei.value.refusal.kind == GATE_SIDE_EFFECT
    assert agent.refusals and agent.refusals[-1].kind == GATE_SIDE_EFFECT
    assert _persisted(root) == []
