"""The register-edit fulfilment lane (add-register-edit-lane).

Commissions are recorded through the REAL gate console; the lane then
applies them to a comment-bearing fixture register (create incl. the D17
empty form, add, remove — comments preserved), validates before writing,
stamps deliveries, refuses stale commissions, and — the git half — commits
only the register file and pushes to a bare fixture remote, leaving
descriptors dispatched whenever the push cannot land.

Wire half: the apply route runs the same code behind the loopback +
gate-actor boundary.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_gate_routes import _post, _serving

from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.gate_console import GateConsole
from ideation_dashboard import register_edit_lane as lane

REGISTER = """\
# Curated header comment — MUST survive every lane edit.
schema_version: 1
kind: project-register

projects:
  - id: core
    name: Core
    repositories:
      # the reference stack
      - repoA
  - id: hollow
    name: Hollow
    repositories: []

# No project groups yet. Trailing stub comment — must also survive.
"""


def _fixture(tmp_path):
    checkout = tmp_path / "checkout"
    checkout.mkdir(parents=True, exist_ok=True)
    register = tmp_path / "project-register.yaml"
    register.write_text(REGISTER, encoding="utf-8")
    gate = HumanGate(checkout, ["ideation/dashboard/gate-records/"],
                     human_actor="brett")
    return checkout, register, GateConsole(gate)


def test_the_lane_applies_create_add_and_remove_preserving_comments(tmp_path):
    checkout, register, console = _fixture(tmp_path)
    console.create_project("Field Pilots", repositories=[], register_source=register)
    console.edit_project("core", add=["repoB"], roster=["repoB"],
                         register_source=register)
    console.edit_project("hollow", add=["repoA"], register_source=register)

    report = lane.fulfil_once(checkout, git=False)
    assert report.error is None
    assert sorted(report.applied) == [
        ("create-project", "field-pilots"),
        ("edit-project", "core"),
        ("edit-project", "hollow")]
    assert report.skipped == []

    text = register.read_text(encoding="utf-8")
    doc = yaml.safe_load(text)
    projects = {p["id"]: p for p in doc["projects"]}
    assert projects["field-pilots"]["repositories"] == []       # D17 empty create
    assert projects["core"]["repositories"] == ["repoA", "repoB"]
    assert projects["hollow"]["repositories"] == ["repoA"]      # [] -> list
    # the curated comments survive the surgical edits
    assert "Curated header comment" in text
    assert "# the reference stack" in text
    assert "Trailing stub comment" in text

    # descriptors delivered with structured stamps
    for job in (checkout / "ideation/dashboard/gate-records").rglob("*.workflow-job.yaml"):
        doc = yaml.safe_load(job.read_text(encoding="utf-8"))
        assert doc["status"] == "delivered"
        assert doc["delivered_by"] == lane.DELIVERED_BY
        assert doc["delivered_at"]

    # idempotent: a second pass finds nothing
    again = lane.fulfil_once(checkout, git=False)
    assert again.applied == [] and again.skipped == []


def test_a_queued_series_delivers_oldest_first_in_one_pass(tmp_path):
    """Edits QUEUE (topic D18): one lane pass delivers a whole commission
    series — create, successive adds, a remove — in dispatch order, so the
    register lands exactly where the queue's net says."""
    checkout, register, console = _fixture(tmp_path)
    console.create_project("Field Pilots", repositories=[],
                           register_source=register)
    console.edit_project("field-pilots", add=["repoA"],
                         register_source=register)
    console.edit_project("field-pilots", add=["repoB"], roster=["repoB"],
                         register_source=register)
    console.edit_project("field-pilots", remove=["repoA"],
                         register_source=register)

    report = lane.fulfil_once(checkout, git=False)
    assert report.error is None
    assert report.skipped == []
    assert report.applied == [
        ("create-project", "field-pilots"),
        ("edit-project", "field-pilots"),
        ("edit-project", "field-pilots"),
        ("edit-project", "field-pilots")]
    doc = yaml.safe_load(register.read_text(encoding="utf-8"))
    projects = {p["id"]: p for p in doc["projects"]}
    assert projects["field-pilots"]["repositories"] == ["repoB"]
    for job in (checkout / "ideation/dashboard/gate-records").rglob(
            "*.workflow-job.yaml"):
        assert "status: delivered" in job.read_text(encoding="utf-8")


def test_a_stale_commission_refuses_and_stays_dispatched(tmp_path):
    checkout, register, console = _fixture(tmp_path)
    console.edit_project("core", remove=["repoA"], register_source=register)
    # the register moves under the commission: repoA is already gone
    register.write_text(REGISTER.replace("      # the reference stack\n      - repoA\n",
                                         "      - repoZ\n"), encoding="utf-8")
    report = lane.fulfil_once(checkout, git=False)
    assert report.applied == []
    assert len(report.skipped) == 1
    verb, pid, reason = report.skipped[0]
    assert (verb, pid) == ("edit-project", "core")
    assert "not currently a member" in reason
    job = next((checkout / "ideation/dashboard/gate-records").rglob(
        "edit-project-*.workflow-job.yaml"))
    assert "status: dispatched" in job.read_text(encoding="utf-8")


def test_the_git_half_commits_only_the_register_and_pushes(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    work = tmp_path / "aggregation"
    subprocess.run(["git", "clone", "-q", str(remote), str(work)], check=True)
    for k, v in (("user.name", "test"), ("user.email", "t@example.com")):
        subprocess.run(["git", "-C", str(work), "config", k, v], check=True)
    (work / "project-register.yaml").write_text(REGISTER, encoding="utf-8")
    (work / "unrelated.txt").write_text("other sessions' work\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(work), "add", "project-register.yaml"], check=True)
    subprocess.run(["git", "-C", str(work), "commit", "-q", "-m", "seed",
                    "--", "project-register.yaml"], check=True)
    subprocess.run(["git", "-C", str(work), "push", "-q"], check=True)

    checkout = work / "corpus"
    checkout.mkdir()
    console = GateConsole(HumanGate(checkout, ["ideation/dashboard/gate-records/"],
                                    human_actor="brett"))
    console.edit_project("core", add=["repoB"], roster=["repoB"])

    report = lane.fulfil_once(checkout, git=True)
    assert report.error is None, report.as_dict()
    assert report.applied == [("edit-project", "core")]
    assert report.committed and report.pushed
    # ONLY the register rode the commit; the dirty unrelated file did not
    show = subprocess.run(["git", "-C", str(work), "show", "--stat", "--name-only",
                           "HEAD"], capture_output=True, text=True, check=True)
    assert "project-register.yaml" in show.stdout
    assert "unrelated.txt" not in show.stdout
    status = subprocess.run(["git", "-C", str(work), "status", "--porcelain"],
                            capture_output=True, text=True, check=True)
    assert "unrelated.txt" in status.stdout                     # still theirs


def test_a_push_failure_leaves_descriptors_dispatched(tmp_path):
    # a plain directory: git add/commit fail, so the ruling's failure path runs
    checkout, register, console = _fixture(tmp_path)
    console.edit_project("core", add=["repoB"], roster=["repoB"],
                         register_source=register)
    report = lane.fulfil_once(checkout, git=True)
    assert report.error is not None
    assert report.applied == []
    # the file IS edited (Brett's ruling), the descriptor stays dispatched
    assert "repoB" in register.read_text(encoding="utf-8")
    job = next((checkout / "ideation/dashboard/gate-records").rglob(
        "edit-project-*.workflow-job.yaml"))
    assert "status: dispatched" in job.read_text(encoding="utf-8")


def test_wire_the_apply_route_runs_the_lane(tmp_path):
    # a `pool` project makes repoB register-known, so the wire commission's
    # roster guard admits it (multi-parent: joining core too is legal)
    (tmp_path / "project-register.yaml").write_text(
        REGISTER + "  - id: pool\n    repositories:\n      - repoB\n",
        encoding="utf-8")
    with _serving(tmp_path) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/edit-project",
                                {"project_id": "core", "add": ["repoB"]})
        assert status == 200, payload
        status, payload = _post(host, port, "/actions/apply-register-edits", {})
        # the fixture register's parent is no git repo, so the lane reports
        # the git failure while the file itself carries the edit — the
        # ruling's exact failure envelope, over the wire
        assert status == 409, payload
        assert payload["ok"] is False
        assert "git" in str(payload.get("error", ""))
        assert "repoB" in (tmp_path / "project-register.yaml").read_text(encoding="utf-8")
