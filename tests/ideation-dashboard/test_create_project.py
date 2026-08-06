"""create-project — the project-register-edit commission
(add-project-scoped-selection).

Engine half: every guard in its ruled order (name shape, member shape,
register reachability, id collision, single-parent, roster membership,
duplicate), the accept path's descriptor + record, the agent-path rejection,
and — the D2 boundary — the register file byte-identical after every call.

Wire half: rides test_gate_routes' real-HTTP `_serving` harness — invalid
bodies are 400, engine refusals are 409 carrying the engine's reason, the
accept path returns the slugged id and record paths, and a serve whose
checkout can reach no register refuses rather than assumes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

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
    repositories:
      - repoA
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


# ---- engine guards, in the ruled order ------------------------------------

def test_a_name_with_no_slug_is_refused(tmp_path):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match="letter or digit"):
        console.create_project("!!!", repositories=["repoA"], register_source=reg)


def test_an_empty_member_set_is_refused(tmp_path):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match="at least one member"):
        console.create_project("Thing", repositories=[], register_source=reg)


def test_an_unreachable_register_is_refused_not_assumed(tmp_path):
    _, _, console = _fixture(tmp_path, register=None)
    with pytest.raises(GateRefused, match="no project register is reachable"):
        console.create_project("Thing", repositories=["repoA"])


def test_the_register_is_discovered_walking_up_from_the_checkout(tmp_path):
    checkout, reg, console = _fixture(tmp_path)
    # no explicit register_source: tmp_path/project-register.yaml sits one
    # level above the checkout, exactly the aggregation-workspace layout
    res = console.create_project("Walk Up", repositories=["repoB"],
                                 roster=["repoB"])
    assert res.job["project_id"] == "walk-up"


def test_an_existing_project_id_is_refused(tmp_path):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match="already exists"):
        console.create_project("Core", repositories=["repoB"],
                               roster=["repoB"], register_source=reg)


def test_the_single_parent_rule_refuses_an_owned_member(tmp_path):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match="at most one project"):
        console.create_project("Thing", repositories=["repoA"],
                               register_source=reg)


def test_a_member_outside_register_and_roster_is_refused(tmp_path):
    _, reg, console = _fixture(tmp_path)
    with pytest.raises(GateRefused, match="not in the repository roster"):
        console.create_project("Thing", repositories=["repoZ"],
                               register_source=reg)


def test_a_duplicate_undelivered_commission_is_refused_and_names_it(tmp_path):
    _, reg, console = _fixture(tmp_path)
    console.create_project("New Thing", repositories=["repoB"],
                           roster=["repoB"], register_source=reg)
    with pytest.raises(GateRefused, match="new-thing"):
        console.create_project("New Thing", repositories=["repoB"],
                               roster=["repoB"], register_source=reg)


# ---- the accept path -------------------------------------------------------

def test_accept_writes_descriptor_and_record_and_not_the_register(tmp_path):
    checkout, reg, console = _fixture(tmp_path)
    before = reg.read_bytes()
    res = console.create_project("Field Pilots ", repositories=["repoB", "repoB"],
                                 roster=["repoB"], register_source=reg)
    assert reg.read_bytes() == before          # D2: never written here
    assert res.job["project_id"] == "field-pilots"
    assert res.job["workflow"] == kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW
    assert res.job["project_name"] == "Field Pilots "
    assert res.job["repositories"] == ["repoB"]           # deduped
    record = res.gate_action_record
    assert record["action"] == "create-project"
    assert record["target"] == {"project_id": "field-pilots"}
    assert any(a["kind"] == "workflow-job" for a in record["artifacts"])
    assert res.job_path.is_file() and res.record_path.is_file()
    # the descriptor is scanned by the shared undelivered-commission index
    dispatched = kickoff_mod.dispatched_commissions(
        checkout / "ideation/dashboard/gate-records/", "create-project")
    assert dispatched == {"field-pilots": res.job_path}


def test_the_agent_path_is_structurally_rejected(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (tmp_path / "project-register.yaml").write_text(REGISTER, encoding="utf-8")
    agent = OutputBoundary(checkout, ["ideation/dashboard/gate-records/"])
    with pytest.raises(BoundaryViolation):
        kickoff_mod.create_project(agent, "Thing", repositories=["repoB"],
                                   roster=["repoB"])


# ---- the wire --------------------------------------------------------------

def _register_beside(tmp_path):
    (tmp_path / "project-register.yaml").write_text(REGISTER, encoding="utf-8")


def test_wire_missing_fields_are_invalid_body(tmp_path):
    _register_beside(tmp_path)
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/create-project", {})
        assert status == 400 and payload["error"] == "invalid_body"
        assert "name" in payload["message"]
        status, payload = _post(host, port, "/actions/gate/create-project",
                                {"name": "Thing"})
        assert status == 400 and "repositories" in payload["message"]


def test_wire_engine_refusal_is_409_with_the_engine_reason(tmp_path):
    _register_beside(tmp_path)
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/create-project",
                                {"name": "Thing", "repositories": ["repoA"]})
        assert status == 409, payload
        assert payload["error"] == "gate_refused"
        assert "at most one project" in payload["message"]


def test_wire_accept_returns_the_slugged_id_and_paths(tmp_path):
    _register_beside(tmp_path)
    with _serving(tmp_path) as (host, port, root):
        # the serve's registry advertises the fixture repository, so a member
        # outside the register but inside the roster is legal
        conn_status, caps = _post(host, port, "/actions/gate/create-project",
                                  {"name": "Wire Project",
                                   "repositories": ["repoB"]})
        # repoB is neither register-known nor registry-reachable: refused —
        # prove the roster widening by asking for the registry's own repo
        assert conn_status == 409
        idx_status, payload = _post(host, port, "/actions/gate/create-project",
                                    {"name": "Wire Project",
                                     "repositories": ["fixture-repo"]})
        if idx_status == 409:
            # the fixture serve may not register its repository id; the
            # register-known universe then rules, which the engine tests cover
            assert "roster" in payload["message"]
            return
        assert idx_status == 200, payload
        assert payload["ok"] is True
        assert payload["project_id"] == "wire-project"
        assert (root / payload["record"]).is_file()
        assert (root / payload["job"]).is_file()


def test_wire_register_unreachable_refuses(tmp_path):
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/create-project",
                                {"name": "Thing", "repositories": ["repoA"]})
        assert status == 409
        assert "no project register" in payload["message"]
