"""Executing gate routes — the LOCAL action center (openxFactory
`add-ideation-intent-plane` §3, tasks 3.1–3.3; specs/006-local-action-center).

Real-HTTP tests against serve.py: capability advertisement (loopback + actor
gated), dispose-possible accept persisting the register + gate-action record,
uncited rejection refused over the wire with nothing persisted, unknown verbs,
off-loopback refusal, and ratify executing. Hermetic: a fixture openxFactory
checkout under tmp_path, a fake pinned validator, no browser automation.
"""

from __future__ import annotations

import http.client
import json
import threading
from contextlib import contextmanager
from pathlib import Path

import yaml as yaml_mod

from conftest import (  # noqa: F401 (sys.path side effect)
    BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit,
    dashboard_web_root, find_openxfactory_validator, staging_fragment,
)

from ideation_dashboard import human_seen as hs
from opendox import serve as serve_mod
from opendox.boundary import BoundaryViolation, OutputBoundary
from openxdox.generator import generate_snapshot
from openxdox import gate_routes as gate_routes_mod
from opendox import authoring as authoring_mod
from opendox import workbench as wb_mod

# The § 5.2 shed moved the dashboard's served assets to the openDox leg with
# `serve.py`, so the pre-shed root this used to name is not a directory any
# more. `dashboard_web_root()` answers where they are from the manifest row of
# `web/index.html` — derived, not transcribed, so the day a row's destination
# changes this fixture follows it (RULED (a), `#656` comment `5625573095`;
# Copilot `PRRT_kwDOTAvnrs6hcKiV`).
WEB = dashboard_web_root()
VALIDATOR = find_openxfactory_validator()
XREF_VALIDATOR = hs.find_cross_reference_validator(REPO_ROOT)

# A complete organizer-evidence block for an add-as-cluster body (the human_seen
# contract). `over` patches any field; the revision is pinned to the fixture
# snapshot's source_revision so the one-anchor rule holds.
def _evidence(**over):
    ev = {
        "proposer": "brett",
        "repository": "fixture-repo",
        "path": "ideation/brainstorm/dtn-register.md",
        "revision": PINNED_REVISION,
        "section": "Notes",
        "passage_sha256": "b0f04c299263dd2496c601fbbd812d645ebade162c5a9aa15e8fe8b7a656bc7a",
        "rationale": "Two governance notes describe the same cluster; grouping them.",
        "confidence": 0.6,
        "alternatives": ["Fold into an existing governance cluster instead."],
    }
    ev.update(over)
    return ev


def _derived_entry(pid="pos-derived-x"):
    return {
        "id": pid, "title": "Derived", "claim": "c", "state": "latent",
        "origin": "ai-derived",
        "provenance": {"document": "d", "section": "s"},
        "derivation": {"worker_run": {
            "correlation_id": "DPOSS-1", "worker_profile": "derive-possibles",
            "prompt_contract_version": "derive-possibles-prompt-v1"},
            "disposition": "pending_review"},
        "claiming_clusters": ["cl-a"],
        "supporting_evidence": [{"document": "d", "section": "s",
                                 "passage_sha256": "0" * 64}],
    }


def _openx_root(tmp_path: Path) -> Path:
    root = tmp_path / "openx"
    (root / "ideation").mkdir(parents=True)
    # `topic-x` is worked to done, so the propose route's readiness gate
    # (add-staging-workbench) lets the commission through; `topic-blocked`
    # carries a standing open item, so the same gate refuses it. Both shapes
    # come from the shared conftest fixtures.
    for topic, text in (("topic-x", staging_fragment("Topic X", "topic-x")),
                        ("topic-blocked",
                         staging_fragment("Topic Blocked", "topic-blocked",
                                          resolved=False))):
        (root / "ideation" / "staging" / topic).mkdir(parents=True)
        (root / "ideation" / "staging" / topic / f"{topic}.md").write_text(
            text, encoding="utf-8")
    index = {"schema_version": 1, "kind": "ideation-cross-reference",
             "repository": "openxFactory",
             "generation": {"source_revision": "e" * 40,
                            "generator_version": "test"},
             "topic_entries": [{"id": "cl-a", "name": "A",
                                "members": [{"path": "p", "stage": "staged"}]}],
             "possibles_register": [_derived_entry()]}
    (root / "ideation" / "cross-reference.yaml").write_text(
        yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")
    return root


def _fake_validator(tmp_path: Path, accept: bool = True) -> Path:
    script = tmp_path / "fake_index_validator.py"
    script.write_text(f"import sys\nsys.exit(0 if {accept!r} else 1)\n",
                      encoding="utf-8")
    return script


@contextmanager
def _serving(tmp_path, *, host="127.0.0.1", actor="brett", validator=True,
             monkeypatch=None, snapshot=None,
             manifest_validator=None, xref_validator=None):
    if monkeypatch is not None:  # hermetic .md projection
        renderer_root = tmp_path / "fake-openx" / "scripts"
        renderer_root.mkdir(parents=True, exist_ok=True)
        (renderer_root / "render-ideation-cross-reference.py").write_text(
            "def render_markdown(index):\n    return '# projection\\n'\n",
            encoding="utf-8")
        monkeypatch.setenv("OPENXFACTORY_ROOT", str(tmp_path / "fake-openx"))
    root = _openx_root(tmp_path)
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot or {"generation": {}}), encoding="utf-8")
    httpd = serve_mod.build_server(
        WEB, snap_path, root, host=host, actor=actor,
        gate_index_validator=_fake_validator(tmp_path, accept=validator),
        gate_manifest_validator=manifest_validator,
        gate_xref_validator=xref_validator)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host,
               port, root)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _console_token(host, port):
    """The per-serve human-console token (FR-019's third clause; PR #49 review
    finding 2), read as the served page reads it — a same-origin
    `GET /capabilities`. Absent on a plane with no session capability, and the
    session verbs are the only ones that require it."""
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("GET", "/capabilities")
    response = conn.getresponse()
    caps = json.loads(response.read().decode("utf-8"))
    conn.close()
    return caps.get("console_token")


def _post(host, port, path, body):
    payload = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(payload))}
    token = _console_token(host, port)
    if token:
        headers["X-XF-Console-Token"] = token
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("POST", path, body=payload, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    conn.close()
    return response.status, data


def _get(host, port, path):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("GET", path)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    conn.close()
    return response.status, data


def _register(root: Path):
    index = yaml_mod.safe_load(
        (root / "ideation" / "cross-reference.yaml").read_text("utf-8"))
    return index["possibles_register"]


# ---- capability advertisement --------------------------------------------------

def test_capabilities_advertise_gate_on_loopback_with_actor(tmp_path,
                                                            monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, _root):
        status, caps = _get(host, port, "/capabilities")
    assert status == 200
    assert caps["actions"]["gate"] is True
    assert caps["actor"] == "brett"


def test_capabilities_off_without_actor(tmp_path, monkeypatch):
    # actor=None + a checkout with no git identity resolves no actor ->
    # fail-closed capability
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)
    with _serving(tmp_path, actor=None, monkeypatch=monkeypatch) as (host, port, _r):
        status, caps = _get(host, port, "/capabilities")
        assert caps["actions"]["gate"] is False and caps["actor"] is None
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "accepted"})
    assert status == 403 and body["error"] == "action_unavailable"


def test_off_loopback_bind_refuses_gate_actions(tmp_path, monkeypatch):
    with _serving(tmp_path, host="0.0.0.0", monkeypatch=monkeypatch) as (host, port, root):
        status, caps = _get(host, port, "/capabilities")
        assert caps["actions"]["gate"] is False
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "accepted"})
        assert status == 403 and body["error"] == "loopback_only"
        assert "human_disposition" not in _register(root)[0]["derivation"]


# ---- dispose-possible over HTTP -------------------------------------------------

def test_accept_over_http_persists_register_and_record(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "accepted", "note": "from the tray"})
        assert status == 200 and body["ok"] is True
        assert body["state"] == "latent" and body["outcome"] == "accepted"
        entry = _register(root)[0]
        assert entry["derivation"]["human_disposition"]["outcome"] == "accepted"
        assert entry["derivation"]["human_disposition"]["authority"] == "brett"
        record_path = root / body["record"]
        assert record_path.is_file()
        record = yaml_mod.safe_load(record_path.read_text(encoding="utf-8"))
        assert record["action"] == "dispose-possible"
        assert record["actor"] == "brett"


def test_uncited_reject_refused_on_the_wire_and_nothing_persists(tmp_path,
                                                                 monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        before = (root / "ideation" / "cross-reference.yaml").read_bytes()
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "rejected"})
        assert status == 409 and body["error"] == "gate_refused"
        assert "citation" in body["message"]  # the engine's reason reaches the panel
        assert (root / "ideation" / "cross-reference.yaml").read_bytes() == before


def test_rejected_index_validation_persists_nothing(tmp_path, monkeypatch):
    with _serving(tmp_path, validator=False, monkeypatch=monkeypatch) as (host, port, root):
        before = (root / "ideation" / "cross-reference.yaml").read_bytes()
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "accepted"})
        assert status == 409 and body["error"] == "gate_refused"
        assert (root / "ideation" / "cross-reference.yaml").read_bytes() == before


def test_invalid_and_unknown_bodies(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, _root):
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": "pos-derived-x",
                              "outcome": "promoted"})
        assert status == 400 and body["error"] == "invalid_body"
        status, body = _post(host, port, "/actions/gate/frobnicate",
                             {"anything": True})
        assert status == 404 and body["error"] == "unknown_verb"


# ---- ratify over HTTP ------------------------------------------------------------

def test_ratify_executes_and_writes_records(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/ratify",
                             {"change_id": "add-example-change"})
        assert status == 200 and body["ok"] is True
        assert body["ratifier"] == "brett"
        assert (root / body["record"]).is_file()


# ---- propose over HTTP (add-propose-verb) ---------------------------------------

def test_propose_commissions_and_writes_records(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/propose",
                             {"topic_id": "topic-x", "note": "from the wheel"})
        assert status == 200 and body["ok"] is True
        assert body["workflow"] == "proposal-authoring"
        record = yaml_mod.safe_load((root / body["record"]).read_text("utf-8"))
        assert record["action"] == "propose"
        assert record["actor"] == "brett"
        assert record["target"] == {"topic_id": "topic-x"}
        assert record["artifacts"][0]["kind"] == "workflow-job"
        job = yaml_mod.safe_load((root / body["job"]).read_text("utf-8"))
        assert job["topic_id"] == "topic-x"
        assert job["status"] == "dispatched"
        assert job["dispatched_by"] == "brett"


def test_propose_missing_topic_refused_persists_nothing(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/propose",
                             {"topic_id": "no-such-topic"})
        assert status == 409 and body["error"] == "gate_refused"
        assert "no staging topic" in body["message"]
        assert not list(root.rglob("*.workflow-job.yaml"))


def test_propose_duplicate_commission_refused(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/propose",
                             {"topic_id": "topic-x"})
        assert status == 200
        status, body = _post(host, port, "/actions/gate/propose",
                             {"topic_id": "topic-x"})
        assert status == 409 and body["error"] == "gate_refused"
        assert "already carries a dispatched" in body["message"]
        assert len(list(root.rglob("propose-*.workflow-job.yaml"))) == 1


def test_propose_requires_topic_id(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, _root):
        status, body = _post(host, port, "/actions/gate/propose", {})
        assert status == 400 and body["error"] == "invalid_body"


def test_propose_readiness_gate_refuses_over_the_wire_with_its_blockers(tmp_path, monkeypatch):
    # The staged-to-proposal readiness gate (add-staging-workbench) is enforced at
    # the engine every surface passes through, so the loopback route surfaces the
    # SAME refusal — 409 gate_refused carrying the named blockers — and persists
    # nothing. Engine-level coverage lives in test_readiness_gate.py.
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/propose",
                             {"topic_id": "topic-blocked"})
        assert status == 409 and body["error"] == "gate_refused"
        assert "not ready" in body["message"]
        assert ("ideation/staging/topic-blocked/topic-blocked.md carries 2 "
                "standing open items") in body["message"]
        assert "no override" in body["message"]
        assert not list(root.rglob("*.workflow-job.yaml"))
        assert not list(root.rglob("*.gate-action.yaml"))


# ---- lens gate verbs over HTTP (add-lens-gate-verbs) ----------------------------
# The served snapshot carries the fixture corpus so the route re-evaluates the
# recipe server-side (never trusting a browser member list); the pinned dashboard
# + cross-reference validators are injected so the manifest/queue writes are
# schema-validated at landing exactly as production does.

import pytest  # noqa: E402

_LENS_SKIP = pytest.mark.skipif(
    VALIDATOR is None or XREF_VALIDATOR is None,
    reason="pinned openxFactory validator(s) not reachable")


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())


@contextmanager
def _serving_lens(tmp_path, monkeypatch, **kw):
    with _serving(tmp_path, monkeypatch=monkeypatch, snapshot=_snapshot(),
                  manifest_validator=VALIDATOR, xref_validator=XREF_VALIDATOR,
                  **kw) as ctx:
        yield ctx


@_LENS_SKIP
def test_lens_save_recipe_lands_manifest_and_record(tmp_path, monkeypatch):
    with _serving_lens(tmp_path, monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "Governance lens",
                              "checked": ["ideation-governance"]})
        assert status == 200 and body["ok"] is True
        assert body["verb"] == "lens-save-recipe"
        manifest = root / body["manifest"]
        assert manifest.is_file()
        assert "ideation/workbench/" in body["manifest"]
        loaded = yaml_mod.safe_load(manifest.read_text("utf-8"))
        assert loaded["kind"] == "ideation-workbench"
        assert loaded["recipe"]["checked"] == ["ideation-governance"]
        assert loaded["seed"]["kind"] == "recipe"
        # the gate-action record lands beside it, honestly named + attributed.
        record = yaml_mod.safe_load((root / body["record"]).read_text("utf-8"))
        assert record["action"] == "lens-save-recipe"
        assert record["actor"] == "brett"
        assert record["target"] == {"set": "governance-lens"}
        assert record["artifacts"][0]["reference"] == body["manifest"]


@_LENS_SKIP
def test_lens_save_recipe_reasonless_override_refused_persists_nothing(tmp_path, monkeypatch):
    with _serving_lens(tmp_path, monkeypatch) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "Bad override",
                              "checked": ["ideation-governance"],
                              "includes": {"ideation/brainstorm/avatar-client-lab.md": ""}})
        assert status == 409 and body["error"] == "gate_refused"
        assert "reason" in body["message"]  # the engine's override guard verbatim
        assert not (root / "ideation" / "workbench" / "bad-override.workbench.yaml").exists()
        assert not list(root.rglob("*.gate-action.yaml"))


@_LENS_SKIP
def test_lens_save_recipe_duplicate_name_refused(tmp_path, monkeypatch):
    with _serving_lens(tmp_path, monkeypatch) as (host, port, root):
        first, _ = _post(host, port, "/actions/gate/lens-save-recipe",
                         {"name": "Dupe lens", "checked": ["ideation-governance"]})
        assert first == 200
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "Dupe lens", "checked": ["ideation-governance"]})
        assert status == 409 and body["error"] == "gate_refused"
        assert "already exists" in body["message"]
        # exactly one manifest for the slug; the second never overwrote it.
        assert len(list(root.rglob("dupe-lens.workbench.yaml"))) == 1


@_LENS_SKIP
def test_lens_save_recipe_validation_failure_persists_nothing(tmp_path, monkeypatch):
    # a rejecting manifest validator => the write is refused (reject-and-report).
    # Distinct filename: `_serving` reuses fake_index_validator.py for the index
    # validator, so the manifest validator needs its own script.
    reject = tmp_path / "fake_manifest_validator.py"
    reject.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
    with _serving(tmp_path, monkeypatch=monkeypatch, snapshot=_snapshot(),
                  manifest_validator=reject, xref_validator=XREF_VALIDATOR) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "Rejected lens", "checked": ["ideation-governance"]})
        assert status == 409 and body["error"] == "gate_refused"
        assert not list(root.rglob("*.gate-action.yaml"))


@_LENS_SKIP
def test_lens_add_as_cluster_lands_manifest_pending_and_record(tmp_path, monkeypatch):
    with _serving_lens(tmp_path, monkeypatch) as (host, port, root):
        index_before = (root / "ideation" / "cross-reference.yaml").read_bytes()
        status, body = _post(host, port, "/actions/gate/lens-add-as-cluster",
                             {"name": "Cluster lens",
                              "checked": ["ideation-governance"],
                              "evidence": _evidence()})
        assert status == 200 and body["ok"] is True
        assert body["verb"] == "lens-add-as-cluster"
        assert (root / body["manifest"]).is_file()
        pending = root / body["pending_entry"]
        assert pending.is_file()
        assert body["pending_entry"].startswith("ideation/workbench/cross-reference-queue/")
        entry = yaml_mod.safe_load(pending.read_text("utf-8"))["topic_entries"][0]
        assert entry["origin"] == "human-seen"
        assert entry["human_seen"]["disposition"] == "pending_review"
        record = yaml_mod.safe_load((root / body["record"]).read_text("utf-8"))
        assert record["action"] == "lens-add-as-cluster"
        assert {a["reference"] for a in record["artifacts"]} == {
            body["manifest"], body["pending_entry"]}
        # the GENERATED cross-reference index is NEVER written by this verb.
        assert (root / "ideation" / "cross-reference.yaml").read_bytes() == index_before


@_LENS_SKIP
def test_lens_add_as_cluster_missing_evidence_refused_persists_nothing(tmp_path, monkeypatch):
    with _serving_lens(tmp_path, monkeypatch) as (host, port, root):
        index_before = (root / "ideation" / "cross-reference.yaml").read_bytes()
        status, body = _post(host, port, "/actions/gate/lens-add-as-cluster",
                             {"name": "No evidence lens",
                              "checked": ["ideation-governance"],
                              "evidence": {}})
        assert status == 409 and body["error"] == "gate_refused"
        assert "evidence" in body["message"]  # the evidence contract, verbatim
        # NOTHING persists: no manifest, no queue entry, no record, index intact.
        assert not (root / "ideation" / "workbench" / "no-evidence-lens.workbench.yaml").exists()
        assert not list(root.rglob("*.human-seen.yaml"))
        assert not list(root.rglob("*.gate-action.yaml"))
        assert (root / "ideation" / "cross-reference.yaml").read_bytes() == index_before


def test_lens_verbs_off_loopback_refused(tmp_path, monkeypatch):
    with _serving(tmp_path, host="0.0.0.0", monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "x", "checked": ["ideation-governance"]})
        assert status == 403 and body["error"] == "loopback_only"
        assert not list(root.rglob("*.workbench.yaml"))


def test_lens_save_recipe_requires_name_and_keyword(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch, snapshot=_snapshot()) as (host, port, _root):
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"checked": ["ideation-governance"]})
        assert status == 400 and body["error"] == "invalid_body"
        status, body = _post(host, port, "/actions/gate/lens-save-recipe",
                             {"name": "no keywords", "checked": []})
        assert status == 400 and body["error"] == "invalid_body"


@_LENS_SKIP
def test_lens_verbs_reject_the_agent_path(tmp_path):
    # An OutputBoundary (the machinery/agent chokepoint — no gate authority) handed
    # to either lens driver is rejected AND reported, exactly like every gate
    # action; nothing is built or written.
    snapshot = _snapshot()
    root = tmp_path / "checkout"
    root.mkdir()
    boundary = OutputBoundary(root, [gate_routes_mod.gate_console.DEFAULT_RECORDS_DIR,
                                     wb_mod.WORKBENCH_DIR], actor="agent")
    with pytest.raises(BoundaryViolation):
        gate_routes_mod.execute_lens_save_recipe(
            boundary, repository="fixture-repo", name="agent set",
            checked=["ideation-governance"], pinned=[], snapshot=snapshot,
            includes={}, excludes={},
            records_dir=gate_routes_mod.gate_console.DEFAULT_RECORDS_DIR)
    with pytest.raises(BoundaryViolation):
        gate_routes_mod.execute_lens_add_as_cluster(
            boundary, repository="fixture-repo", name="agent set",
            checked=["ideation-governance"], pinned=[], snapshot=snapshot,
            includes={}, excludes={}, submission=None,
            records_dir=gate_routes_mod.gate_console.DEFAULT_RECORDS_DIR)
    assert boundary.refusals and boundary.refusals[0].kind == "gate-side-effect"
    assert not list(root.rglob("*.yaml"))


# ---- create-document over HTTP (add-workbench-bullseye-and-create) ---------------
# The staging workbench's ONE write: the human-only gate verb that brings a NEW
# ideation document into existence through the ALREADY-TESTED authoring scaffold.
# The route is transport — the controlled header block, the slug()-normalized
# filename, and the create-only refusal are the engine's, surfaced verbatim here.

import subprocess  # noqa: E402
import sys  # noqa: E402

CREATE_ROUTE = "/actions/gate/create-document"


def _create_body(**over):
    body = {"area": "ideation/brainstorm/", "title": "Lens launch session",
            "summary": "What the centre ring is for.",
            "topics": ["ideation-governance", "doc-health"]}
    body.update(over)
    return body


def _headers(text: str) -> dict:
    """The header block of a created document, as a {field: value} map."""
    out = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        if ":" in line and not line.startswith("#"):
            key, _, value = line.partition(":")
            out.setdefault(key.strip(), value.strip())
    return out


def test_create_document_lands_the_scaffold_and_the_record(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body(
            source="staging workbench scope: cluster cl-a"))
        assert status == 200 and body["ok"] is True
        assert body["verb"] == "create-document"
        # the filename is the engine's slug() of the title — a hostile title can
        # never traverse the workspace
        assert body["path"] == "ideation/brainstorm/lens-launch-session.md"
        doc = root / body["path"]
        assert doc.is_file()
        text = doc.read_text(encoding="utf-8")
        # the H1 carries the family suffix and the controlled header block is in
        # the README's declared order
        assert text.startswith("# Lens launch session — Brainstorm\n")
        head = _headers(text)
        assert head["Status"] == "brainstorm"
        assert head["Kind"] == "note"
        assert head["Summary"] == "What the centre ring is for."
        assert head["Topics"] == "ideation-governance, doc-health"
        # Repository context defaults from the SERVED snapshot
        assert head["Repository context"] == "fixture-repo"
        assert head["Source"] == "staging workbench scope: cluster cl-a"
        assert "## Possible feats" in text
        # the gate-action record names the created document, both as the target
        # and as its one artifact
        record = yaml_mod.safe_load((root / body["record"]).read_text("utf-8"))
        assert record["action"] == "create-document"
        assert record["actor"] == "brett"
        assert record["target"] == {"document": body["path"]}
        # open question 4's RULING: a first-class `document` kind, not `other`
        assert record["artifacts"] == [{"kind": "document", "reference": body["path"]}]
        # the record files under a slug derived from the DOCUMENT (design D10
        # consequence b — the derivation used to KeyError on a document target)
        assert "ideation-brainstorm-lens-launch-session/" in body["record"]


def test_create_document_into_staging_still_carries_brainstorm(tmp_path, monkeypatch):
    """Brett's 2026-07-25 ruling on design open question 1: the `Status:` is
    `brainstorm` in EVERY area — "these are brainstorm docs". The area is NOT
    consulted (an earlier pass derived `staged` here and the ruling REVERSED
    it): what ties this document to the packet is that it LANDED inside
    `ideation/staging/topic-x/`, which is what the topic's folder-scoped health
    and readiness read; the status only says what stage it is at."""
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body(
            area="ideation/staging/topic-x/", title="Fragment two"))
        assert status == 200
        # PLACEMENT is unchanged — the staged-tile area seeding still applies
        assert body["path"] == "ideation/staging/topic-x/fragment-two.md"
        assert body["status"] == "brainstorm"
        head = _headers((root / body["path"]).read_text(encoding="utf-8"))
        assert head["Status"] == "brainstorm"
        # and the engine grew no area-derived helper to reverse later
        assert not hasattr(authoring_mod, "status_for_area")


def test_create_document_honours_an_explicit_creatable_status(tmp_path, monkeypatch):
    """The field stays editable (the ruling keeps the human's override): a create
    that names `staged` gets `staged`, in any area."""
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body(
            area="ideation/brainstorm/", title="Organized already",
            status="staged"))
        assert status == 200 and body["status"] == "staged"
        head = _headers((root / body["path"]).read_text(encoding="utf-8"))
        assert head["Status"] == "staged"


def test_create_document_existing_target_refuses_and_leaves_it_byte_identical(
        tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        first, body = _post(host, port, CREATE_ROUTE, _create_body())
        assert first == 200
        target = root / body["path"]
        before = target.read_bytes()
        records_before = len(list(root.rglob("*.gate-action.yaml")))
        status, refusal = _post(host, port, CREATE_ROUTE, _create_body(
            summary="a different summary entirely"))
        # the engine's create-only refusal, surfaced verbatim as a conflict
        assert status == 409 and refusal["error"] == "gate_refused"
        assert "create-only" in refusal["message"]
        assert "source-edit" in refusal["message"]
        assert target.read_bytes() == before          # never overwritten
        # a refusal persists NOTHING — not even a record of the attempt
        assert len(list(root.rglob("*.gate-action.yaml"))) == records_before


def test_create_document_invalid_bodies_refuse_and_write_nothing(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        for body in ({"summary": "s", "topics": ["t"]},                 # no title
                     {"title": "t", "topics": ["t"]},                   # no summary
                     _create_body(topics=[]),                           # no topics
                     _create_body(topics="alpha"),                       # not a list
                     _create_body(area="../escape/"),                    # traversal
                     _create_body(status="ratified")):                   # not creatable
            status, payload = _post(host, port, CREATE_ROUTE, body)
            assert status == 400, body
            assert payload["error"] == "invalid_body", body
        assert not list((root / "ideation").glob("brainstorm/*.md"))
        assert not list(root.rglob("*.gate-action.yaml"))


def test_create_document_repository_context_can_be_overridden(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body(
            title="Explicit context", repository_context="openxFactory"))
        assert status == 200
        head = _headers((root / body["path"]).read_text(encoding="utf-8"))
        assert head["Repository context"] == "openxFactory"


def test_create_document_off_loopback_refuses(tmp_path, monkeypatch):
    with _serving(tmp_path, host="0.0.0.0", monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body())
        assert status == 403 and body["error"] == "loopback_only"
        assert not list(root.rglob("lens-launch-session.md"))
        assert not list(root.rglob("*.gate-action.yaml"))


def test_create_document_without_a_resolved_actor_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)
    with _serving(tmp_path, actor=None, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body())
        assert status == 403 and body["error"] == "action_unavailable"
        assert not list(root.rglob("lens-launch-session.md"))


def test_create_document_rejects_the_agent_path(tmp_path):
    """Design D11, structural: an OutputBoundary (the machinery/agent chokepoint)
    handed to the driver is rejected AND reported before anything is written —
    document creation BY an agent stays the separate `authoring.agent_capture`
    surface with its own header enforcement."""
    root = tmp_path / "checkout"
    root.mkdir()
    boundary = OutputBoundary(root, [gate_routes_mod.gate_console.DEFAULT_RECORDS_DIR],
                              actor="agent")
    with pytest.raises(BoundaryViolation):
        gate_routes_mod.execute_create_document(
            boundary, area="ideation/brainstorm/", title="Agent doc",
            summary="s", topics=["t"], repository_context="fixture-repo",
            records_dir=gate_routes_mod.gate_console.DEFAULT_RECORDS_DIR)
    assert boundary.refusals and boundary.refusals[0].kind == "gate-side-effect"
    assert not list(root.rglob("*.md"))
    assert not list(root.rglob("*.yaml"))


@pytest.mark.skipif(VALIDATOR is None,
                    reason="pinned openxFactory validator not reachable")
def test_create_document_record_validates_against_the_grown_schema(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch,
                  snapshot=_snapshot()) as (host, port, root):
        status, body = _post(host, port, CREATE_ROUTE, _create_body())
        assert status == 200
        proc = subprocess.run([sys.executable, str(VALIDATOR),
                               str(root / body["record"])],
                              capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 error(s)" in proc.stdout


# ==========================================================================
# 011 add-wheel-action-verbs — the four executing routes (C1–C9)
#
# Same transport, same response discipline, four more verbs. Every refusal test
# asserts the checkout is byte-identical afterwards, so "persists nothing" is
# measured rather than claimed.
# ==========================================================================

_SNAP_WITH_CLUSTER = {"generation": {},
                      "clusters": [{"id": "cl-a", "name": "A"}],
                      "changes": [{"id": "add-x", "status": "active",
                                   "folder": "openspec/changes/add-x",
                                   "files": ["openspec/changes/add-x/proposal.md"],
                                   "origin_staging_id": "topic-x"}]}


def _tree_fingerprint(root: Path):
    """Every file under the checkout with its bytes — the measurable form of
    'the refusal persisted nothing'."""
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _human_possible(pid="pos-human"):
    return {"id": pid, "title": "H", "claim": "c", "state": "latent",
            "provenance": {"document": "d", "section": "s"}}


# ---- C1/C2: accept shapes and invalid bodies ------------------------------

def test_commission_routes_accept_and_return_the_documented_payload(tmp_path):
    """C1 — each commission returns ok, its verb, its target key, the workflow,
    and checkout-relative record and job paths."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        index = yaml_mod.safe_load(
            (root / "ideation" / "cross-reference.yaml").read_text("utf-8"))
        index["possibles_register"].append(_human_possible())
        (root / "ideation" / "cross-reference.yaml").write_text(
            yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")

        for verb, body, key, workflow in (
            ("promote-to-staging", {"possible_id": "pos-human"}, "possible_id",
             "staging-fragment-authoring"),
            ("research-brief", {"possible_id": "pos-human"}, "possible_id",
             "possible-research-brief"),
            ("derive-possibles", {"cluster_id": "cl-a"}, "cluster_id",
             "derive-possibles"),
        ):
            status, payload = _post(host, port, f"/actions/gate/{verb}", body)
            assert status == 200, (verb, payload)
            assert payload["ok"] is True and payload["verb"] == verb
            assert payload[key] == body[key]
            assert payload["workflow"] == workflow
            assert (root / payload["record"]).is_file()
            assert (root / payload["job"]).is_file()
            assert payload["hint"]


@pytest.mark.parametrize("verb,field", [
    ("promote-to-staging", "possible_id"),
    ("research-brief", "possible_id"),
    ("derive-possibles", "cluster_id"),
    ("demote", "change_id"),
])
def test_missing_required_field_is_invalid_body_not_a_refusal(tmp_path, verb, field):
    """C2 — a malformed request is 400 invalid_body; only the ENGINE refuses
    with 409."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        status, payload = _post(host, port, f"/actions/gate/{verb}", {})
        assert status == 400
        assert payload["error"] == "invalid_body"
        assert field in payload["message"]


# ---- C3/C4: engine refusals carry the engine's reason and persist nothing --

@pytest.mark.parametrize("verb,body,fragment", [
    ("promote-to-staging", {"possible_id": "pos-derived-x"}, "disposition"),
    ("promote-to-staging", {"possible_id": "pos-nope"}, "pos-nope"),
    ("research-brief", {"possible_id": "pos-nope"}, "pos-nope"),
    ("derive-possibles", {"cluster_id": "cl-nope"}, "cl-nope"),
    ("demote", {"change_id": "add-x"}, "reason"),
    ("demote", {"change_id": "no-such", "reason": "r"}, "no-such"),
])
def test_engine_refusals_are_409_and_persist_nothing(tmp_path, verb, body, fragment):
    """C3 + C4 — the message is the engine's own reason, and the checkout is
    byte-identical afterwards."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        before = _tree_fingerprint(root)
        status, payload = _post(host, port, f"/actions/gate/{verb}", body)
        assert status == 409, payload
        assert payload["ok"] is False and payload["error"] == "gate_refused"
        assert fragment in payload["message"]
        assert _tree_fingerprint(root) == before


def test_duplicate_commission_is_refused_and_names_the_descriptor(tmp_path):
    """C3/FR-026 — the second dispatch is refused and points at the file whose
    status a human must edit."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        ok, first = _post(host, port, "/actions/gate/derive-possibles",
                          {"cluster_id": "cl-a"})
        assert ok == 200
        after_first = _tree_fingerprint(root)
        status, payload = _post(host, port, "/actions/gate/derive-possibles",
                                {"cluster_id": "cl-a"})
        assert status == 409
        assert Path(first["job"]).name in payload["message"]
        assert _tree_fingerprint(root) == after_first     # the second wrote nothing


def test_a_commission_of_one_verb_does_not_block_another_on_the_same_target(tmp_path):
    """C8 — the duplicate guard is keyed by (verb, target)."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        index = yaml_mod.safe_load(
            (root / "ideation" / "cross-reference.yaml").read_text("utf-8"))
        index["possibles_register"].append(_human_possible())
        (root / "ideation" / "cross-reference.yaml").write_text(
            yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")
        assert _post(host, port, "/actions/gate/research-brief",
                     {"possible_id": "pos-human"})[0] == 200
        assert _post(host, port, "/actions/gate/promote-to-staging",
                     {"possible_id": "pos-human"})[0] == 200


def test_research_brief_on_a_disposed_possible_is_accepted(tmp_path):
    """C7 — the engine carries NO register-state guard (FR-018a). The view
    hides the verb once disposed; the route still accepts it. A test asserting
    a refusal here would encode the wrong contract."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        index = yaml_mod.safe_load(
            (root / "ideation" / "cross-reference.yaml").read_text("utf-8"))
        entry = _human_possible("pos-picked")
        entry.update(state="picked", pick={"staging_id": "topic-x"})
        index["possibles_register"].append(entry)
        (root / "ideation" / "cross-reference.yaml").write_text(
            yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")
        status, payload = _post(host, port, "/actions/gate/research-brief",
                                {"possible_id": "pos-picked"})
        assert status == 200, payload


# ---- C6/C9: demote plans, records, and never executes ---------------------

def test_demote_writes_all_four_artifacts_and_moves_no_file(tmp_path):
    """C6 + FR-002/FR-003 — transition manifest, executable plan,
    register-update note and the reasoned record; the corpus is untouched."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        corpus_before = {k: v for k, v in _tree_fingerprint(root).items()
                         if not k.startswith("ideation/dashboard/")}
        status, payload = _post(host, port, "/actions/gate/demote",
                                {"change_id": "add-x", "reason": "not agreed"})
        assert status == 200, payload
        assert payload["verb"] == "demote" and payload["change_id"] == "add-x"
        assert (root / payload["plan"]).is_file()
        assert (root / payload["record"]).is_file()
        assert "workflow" not in payload and "job" not in payload
        written = sorted(p.name for p in
                         (root / payload["record"]).parent.glob("demote-*"))
        assert any(n.endswith(".transition-manifest.yaml") for n in written)
        assert any(n.endswith(".plan.yaml") for n in written)
        assert any(n.endswith(".register-update.md") for n in written)
        record = yaml_mod.safe_load((root / payload["record"]).read_text("utf-8"))
        assert record["reason"] == "not agreed"
        # THE corpus invariant: nothing outside the records tree changed
        corpus_after = {k: v for k, v in _tree_fingerprint(root).items()
                        if not k.startswith("ideation/dashboard/")}
        assert corpus_after == corpus_before


def test_demote_route_exposes_no_execution_switch(tmp_path):
    """C9 — an execution flag on the body must not run the plan. The corpus
    moves stay a separate, deliberately human-run step (NG-005)."""
    with _serving(tmp_path, snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/demote",
                                {"change_id": "add-x", "reason": "r",
                                 "execute": True, "--execute": True})
        assert status == 200
        assert not (root / "ideation" / "staging" / "topic-x" / "proposal.md").exists()
        import inspect
        from openxdox import gate_console as gc_mod
        assert "execute" not in inspect.signature(gc_mod.demote).parameters


def test_demote_refuses_a_non_active_change(tmp_path):
    """FR-005 — only an active proposal is demoted, which is exactly what makes
    `archived` an illegal host column for the verb."""
    snap = {"generation": {},
            "changes": [{"id": "add-old", "status": "archived",
                         "folder": "openspec/changes/add-old", "files": []}]}
    with _serving(tmp_path, snapshot=snap) as (host, port, root):
        status, payload = _post(host, port, "/actions/gate/demote",
                                {"change_id": "add-old", "reason": "r"})
        assert status == 409
        assert "archived" in payload["message"]


def test_demote_refuses_when_the_served_snapshot_is_unusable(tmp_path):
    """FR-004a — with no snapshot there is no change set to resolve against, so
    the route refuses structurally rather than guessing."""
    with _serving(tmp_path, snapshot={"generation": {}}) as (host, port, root):
        before = _tree_fingerprint(root)
        status, payload = _post(host, port, "/actions/gate/demote",
                                {"change_id": "add-x", "reason": "r"})
        assert status == 409
        assert _tree_fingerprint(root) == before


# ---- C5: the agent path, for all four verbs -------------------------------

@pytest.mark.parametrize("verb,body", [
    ("promote-to-staging", {"possible_id": "pos-derived-x"}),
    ("research-brief", {"possible_id": "pos-derived-x"}),
    ("derive-possibles", {"cluster_id": "cl-a"}),
    ("demote", {"change_id": "add-x", "reason": "r"}),
])
def test_agent_path_is_structurally_rejected_for_every_new_verb(
        tmp_path, monkeypatch, verb, body):
    """C5 — with no resolvable actor there is no human to gate on, so the verb
    is unreachable rather than merely discouraged, and nothing is written.

    Route-level half of the human-only guarantee. The ENGINE half — an
    OutputBoundary (agent) caller raising BoundaryViolation — is pinned per verb
    in test_kickoff.py; the route can never reach it because it only ever
    constructs a HumanGate."""
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)
    with _serving(tmp_path, actor=None, monkeypatch=monkeypatch,
                  snapshot=_SNAP_WITH_CLUSTER) as (host, port, root):
        before = _tree_fingerprint(root)
        status, payload = _post(host, port, f"/actions/gate/{verb}", body)
        assert status == 403 and payload["error"] == "action_unavailable"
        assert _tree_fingerprint(root) == before


def test_all_four_verbs_are_in_the_executing_set(tmp_path):
    for verb in ("demote", "promote-to-staging", "derive-possibles", "research-brief"):
        assert verb in gate_routes_mod.EXECUTING_VERBS
