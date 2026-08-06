"""edit-project — the membership-edit commission (add-opendox-project-header
D15).

Engine half: every guard in its ruled order (diff shape, register
reachability, project existence, addition universe + not-already-member,
removal membership, the at-least-one-member floor, duplicate via the shared
index), the accept path's descriptor + record, the agent rejection, and the
D2 boundary — the register byte-identical after every call.

Wire half: real-HTTP via test_gate_routes' `_serving`; plus the projection's
`pending_edits` plane reporting a dispatched, undelivered edit.
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
    ({"remove": ["repoA", "repoB"]}, "no member repositories"),
])
def test_each_guard_refuses_with_its_own_reason(tmp_path, kwargs, fragment):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match=fragment):
        console.edit_project("core", register_source=reg, **kwargs)


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
    # (verb, target) scoping: an undelivered EDIT does not block a CREATE
    with pytest.raises(GateRefused, match="undelivered edit-project"):
        console.edit_project("core", add=["repoC"], roster=["repoC"],
                             register_source=reg)


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
                                {"project_id": "core",
                                 "remove": ["repoA", "repoB"]})
        assert status == 409 and "no member repositories" in payload["message"]


def test_wire_accept_and_the_pending_edits_plane(tmp_path):
    """D15 + the D-e posture: an accepted edit returns its lists, and the
    projection's `pending_edits` plane reports it until delivery."""
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

        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("GET", "/project-register.json")
        projection = json.loads(conn.getresponse().read().decode("utf-8"))
        conn.close()
        assert projection["pending_edits"] == [{
            "project_id": "core", "add": [], "remove": ["repoB"],
            "dispatched_at": projection["pending_edits"][0]["dispatched_at"]}]
        # truth plane untouched
        assert projection["projects"][0]["repositories"] == ["repoA", "repoB"]
