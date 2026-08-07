"""edit-project — the membership-edit commission (add-opendox-project-header
D15).

Engine half: every guard in its ruled order (diff shape, register
reachability, project existence, addition universe + not-already-member,
removal membership, the at-least-one-member floor), the accept path's
descriptor + record, the agent rejection, and the D2 boundary — the register
byte-identical after every call. Edits QUEUE (topic D18, Brett's 2026-08-07
ruling): no single-flight guard; each commission validates against the
register with the project's pending commissions applied oldest-first, a
pending creation counts as the project existing, and same-second commissions
land as distinct descriptors.

Wire half: real-HTTP via test_gate_routes' `_serving`; plus the projection's
`pending_edits` plane reporting every queued, undelivered edit.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_gate_routes import _post, _serving

from ideation_dashboard.boundary import BoundaryViolation, HumanGate, OutputBoundary
from ideation_dashboard.gate_console import GateConsole, GateRefused
from ideation_dashboard import kickoff as kickoff_mod

REGISTER = """\
schema_version: 1
kind: project-register
projects:
  - id: core
    name: Core
    repositories: [repoA, repoB]
"""


def _fixture(tmp_path, register: str | None = REGISTER):
    checkout = tmp_path / "checkout"
    checkout.mkdir(parents=True, exist_ok=True)
    reg = None
    if register is not None:
        reg = tmp_path / "project-register.yaml"
        reg.write_text(register, encoding="utf-8")
    gate = HumanGate(checkout, ["ideation/dashboard/gate-records/"],
                     human_actor="brett")
    return checkout, reg, GateConsole(gate)


@pytest.mark.parametrize("kwargs,fragment", [
    ({}, "the diff is empty"),
    ({"add": ["x"], "remove": ["x"]}, "both added and removed"),
    ({"add": ["ghost"]}, "not in the repository roster"),
    ({"add": ["repoA"]}, "already a member"),
    ({"remove": ["ghost"]}, "not currently a member"),
])
def test_each_guard_refuses_with_its_own_reason(tmp_path, kwargs, fragment):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match=fragment):
        console.edit_project("core", register_source=reg, **kwargs)


def test_removing_the_last_member_is_legal(tmp_path):
    """Brett's 2026-08-06 ruling: an empty project awaits its next
    additions — the floor guard is gone."""
    _, reg, console = _fixture(tmp_path)
    res = console.edit_project("core", remove=["repoA", "repoB"],
                               register_source=reg)
    assert res.job["remove"] == ["repoA", "repoB"]


def test_a_missing_project_and_a_missing_register_refuse(tmp_path):
    # sibling roots: the bare fixture's upward discovery must not find the
    # register the first fixture wrote (it walks PARENTS, and tmp_path is a
    # shared ancestor)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    _, reg, console = _fixture(tmp_path / "a")
    with pytest.raises(GateRefused, match="no project 'nope'"):
        console.edit_project("nope", add=["repoA"], register_source=reg)
    _, _, bare = _fixture(tmp_path / "b", register=None)
    with pytest.raises(GateRefused, match="no project register is reachable"):
        bare.edit_project("core", add=["repoA"])


def test_accept_writes_descriptor_and_record_and_not_the_register(tmp_path):
    checkout, reg, console = _fixture(tmp_path)
    before = reg.read_bytes()
    res = console.edit_project("core", add=["repoC"], remove=["repoB"],
                               roster=["repoC"], register_source=reg)
    assert reg.read_bytes() == before          # D2: never written here
    assert res.job["project_id"] == "core"
    assert res.job["add"] == ["repoC"]
    assert res.job["remove"] == ["repoB"]
    assert res.job["workflow"] == kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW
    record = res.gate_action_record
    assert record["action"] == "edit-project"
    assert record["target"] == {"project_id": "core"}
    assert any(a["kind"] == "workflow-job" for a in record["artifacts"])
    dispatched = kickoff_mod.dispatched_commissions(
        checkout / "ideation/dashboard/gate-records/", "edit-project")
    assert dispatched == {"core": res.job_path}
    # Edits QUEUE (topic D18): no single-flight refusal — but the queued
    # state governs, so re-adding the still-pending repoC refuses honestly.
    with pytest.raises(GateRefused, match="already a member"):
        console.edit_project("core", add=["repoC"], roster=["repoC"],
                             register_source=reg)


def test_successive_edits_queue_and_validate_against_pending_state(tmp_path):
    """Topic D18 (Brett, 2026-08-07, after two live one-in-flight refusals
    while populating a project member by member): successive edits RECORD
    beside each other, each validated against the register with the queue
    applied oldest-first."""
    checkout, reg, console = _fixture(tmp_path)
    first = console.edit_project("core", add=["repoC"], roster=["repoC"],
                                 register_source=reg)
    second = console.edit_project("core", add=["repoD"], roster=["repoD"],
                                  register_source=reg)          # queues
    assert first.job_path != second.job_path
    # pending-applied state: repoD is now effectively a member...
    with pytest.raises(GateRefused, match="already a member"):
        console.edit_project("core", add=["repoD"], roster=["repoD"],
                             register_source=reg)
    # ...and a pending addition can be removed (net cancel), while a
    # register member with a pending removal can be re-added
    console.edit_project("core", remove=["repoC"], register_source=reg)
    console.edit_project("core", remove=["repoA"], register_source=reg)
    console.edit_project("core", add=["repoA"], register_source=reg)
    rows = kickoff_mod.dispatched_commission_rows(
        checkout / "ideation/dashboard/gate-records/", "edit-project")
    assert [r[0] for r in rows] == ["core"] * 5
    stamps = [r[2]["dispatched_at"] for r in rows]
    assert stamps == sorted(stamps)


def test_an_edit_on_a_pending_created_project_queues(tmp_path):
    """A dispatched create-project counts as the project existing (D18):
    a just-created project can be populated before its fulfilment lands,
    seeded by the creation's own member list."""
    checkout, reg, console = _fixture(tmp_path)
    console.create_project("Field Pilots", repositories=["repoA"],
                           register_source=reg)
    res = console.edit_project("field-pilots", add=["repoB"],
                               register_source=reg)
    assert res.job["add"] == ["repoB"]
    with pytest.raises(GateRefused, match="already a member"):
        console.edit_project("field-pilots", add=["repoA"],
                             register_source=reg)   # seeded by the creation
    console.edit_project("field-pilots", remove=["repoA"],
                         register_source=reg)       # a seed member removes
    with pytest.raises(GateRefused, match="no project 'ghost'"):
        console.edit_project("ghost", add=["repoA"], register_source=reg)


def test_same_second_commissions_land_as_distinct_descriptors(tmp_path):
    """The descriptor path embeds a second-resolution stamp and the artifact
    writer overwrites silently — queued same-second commissions must bump
    the stamp, never share a path."""
    checkout, reg, console = _fixture(tmp_path)
    at = "2026-08-07T02:14:40Z"
    first = console.edit_project("core", add=["repoC"], roster=["repoC"],
                                 register_source=reg, at=at)
    second = console.edit_project("core", add=["repoD"], roster=["repoD"],
                                  register_source=reg, at=at)
    assert first.job_path != second.job_path
    assert second.job["dispatched_at"] == "2026-08-07T02:14:41Z"
    rows = kickoff_mod.dispatched_commission_rows(
        checkout / "ideation/dashboard/gate-records/", "edit-project")
    assert len(rows) == 2


def test_the_agent_path_is_structurally_rejected(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (tmp_path / "project-register.yaml").write_text(REGISTER, encoding="utf-8")
    agent = OutputBoundary(checkout, ["ideation/dashboard/gate-records/"])
    with pytest.raises(BoundaryViolation):
        kickoff_mod.edit_project(agent, "core", remove=["repoB"])


# ---- the wire --------------------------------------------------------------

def _register_beside(tmp_path):
    (tmp_path / "project-register.yaml").write_text(REGISTER, encoding="utf-8")


def test_wire_shapes_and_refusals(tmp_path):
    _register_beside(tmp_path)
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/edit-project", {})
        assert status == 400 and "project_id" in payload["message"]
        status, payload = _post(host, port, "/actions/gate/edit-project",
                                {"project_id": "core", "add": "not-a-list"})
        assert status == 400 and "list" in payload["message"]
        status, payload = _post(host, port, "/actions/gate/edit-project",
                                {"project_id": "nope", "add": ["repoA"]})
        assert status == 409 and "no project 'nope'" in payload["message"]


def test_wire_accept_and_the_pending_edits_plane(tmp_path):
    """D15 + the D-e posture: an accepted edit returns its lists, and the
    projection's `pending_edits` plane reports it until delivery. Edits
    QUEUE over the wire too (D18): a second commission while the first is
    undelivered records beside it, and the plane carries BOTH rows,
    oldest first."""
    import http.client

    _register_beside(tmp_path)
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/edit-project",
                                {"project_id": "core", "remove": ["repoB"]})
        assert status == 200, payload
        assert payload["ok"] is True
        assert payload["remove"] == ["repoB"] and payload["add"] == []
        assert (root / payload["record"]).is_file()
        assert (root / payload["job"]).is_file()
        status, queued = _post(host, port, "/actions/gate/edit-project",
                               {"project_id": "core", "add": ["repoB"]})
        assert status == 200, queued            # D18: queues, never bounces
        assert queued["job"] != payload["job"]

        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("GET", "/project-register.json")
        projection = json.loads(conn.getresponse().read().decode("utf-8"))
        conn.close()
        edits = projection["pending_edits"]
        assert [(e["add"], e["remove"]) for e in edits] == [
            ([], ["repoB"]), (["repoB"], [])]
        assert all(e["project_id"] == "core" for e in edits)
        # truth plane untouched
        assert projection["projects"][0]["repositories"] == ["repoA", "repoB"]
