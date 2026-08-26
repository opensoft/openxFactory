"""Select-to-edit HTTP/UI contract.

The dashboard may ask the local human console to launch an editor, but it must
never rewrite document content itself.  The action is therefore:

* advertised only on a loopback plane with a real corpus checkout and actor;
* protected by the per-serve human-console token before the body is parsed;
* confined to a real, snapshot-listed file under the selected entry's source root;
* injectable in tests so the suite never launches a real desktop application.
"""

from __future__ import annotations

import http.client
import json
import shutil
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import serve as serve_mod
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
EDIT_JS = WEB / "views" / "edit.js"
NODE = shutil.which("node")


def _snapshot():
    return generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


@contextmanager
def _serving(tmp_path, *, actor="brett", launcher=None):
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(_snapshot()), encoding="utf-8")
    calls: list[list[str]] = []

    def fake_launcher(argv):
        calls.append(list(argv))
        return object()

    httpd = serve_mod.build_server(
        WEB,
        snap_path,
        BASE_REPO,
        head=PINNED_REVISION,
        actor=actor,
    )
    httpd.editor_launcher = launcher or fake_launcher
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port, calls
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    raw = None if body is None else json.dumps(body)
    conn.request(method, path, body=raw, headers=headers or {})
    resp = conn.getresponse()
    payload = json.loads(resp.read().decode("utf-8") or "{}")
    conn.close()
    return resp.status, payload


def _capabilities(host, port):
    status, payload = _request(host, port, "GET", "/capabilities")
    assert status == 200
    return payload


def _console_headers(caps):
    return {
        "Content-Type": "application/json",
        "X-XF-Console-Token": caps["console_token"],
    }


def test_edit_capability_requires_the_local_human_console():
    local = serve_mod.compute_capabilities(
        nlm_present=False, checkout_real=True, loopback=True, actor="brett")
    assert local["actions"]["edit"] is True
    for kwargs in (
        {"nlm_present": False, "checkout_real": False, "loopback": True,
         "actor": "brett"},
        {"nlm_present": False, "checkout_real": True, "loopback": False,
         "actor": "brett"},
        {"nlm_present": False, "checkout_real": True, "loopback": True,
         "actor": None},
    ):
        assert serve_mod.compute_capabilities(**kwargs)["actions"]["edit"] is False


@pytest.mark.parametrize("rel", [
    "ideation/staging/ideation-governance/README.md",
    "openspec/changes/add-ideation-governance/proposal.md",
])
def test_edit_route_launches_a_snapshot_listed_file_without_modifying_it(
        tmp_path, rel, monkeypatch):
    monkeypatch.delenv("EDITOR", raising=False)
    before = (BASE_REPO / rel).read_bytes()
    with _serving(tmp_path) as (host, port, calls):
        caps = _capabilities(host, port)
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": rel, "repository": "fixture-repo", "ref": "main"},
            headers=_console_headers(caps),
        )
    assert status == 200
    assert payload == {"ok": True, "path": rel}
    assert calls == [["xdg-open", str((BASE_REPO / rel).resolve())]]
    assert (BASE_REPO / rel).read_bytes() == before


def test_edit_route_honors_the_configured_editor(tmp_path, monkeypatch):
    monkeypatch.setenv("EDITOR", "code --wait")
    rel = "ideation/staging/ideation-governance/README.md"
    with _serving(tmp_path) as (host, port, calls):
        caps = _capabilities(host, port)
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": rel, "repository": "fixture-repo", "ref": "main"},
            headers=_console_headers(caps),
        )
    assert status == 200
    assert payload == {"ok": True, "path": rel}
    assert calls == [["code", "--wait", str((BASE_REPO / rel).resolve())]]


def test_rebinding_host_cannot_obtain_token_or_launch_an_editor(tmp_path):
    rel = "ideation/staging/ideation-governance/README.md"
    with _serving(tmp_path) as (host, port, calls):
        status, hostile_caps = _request(
            host, port, "GET", "/capabilities",
            headers={"Host": "rebound.example"})
        caps = _capabilities(host, port)
        headers = _console_headers(caps)
        headers["Host"] = "rebound.example"
        launched, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": rel, "repository": "fixture-repo", "ref": "main"},
            headers=headers,
        )
    assert status == 403
    assert hostile_caps["error"] == "invalid_host"
    assert "console_token" not in hostile_caps
    assert (launched, payload["error"]) == (403, "agent_invocation")
    assert calls == []


def test_configured_editor_inherits_the_console_for_terminal_programs():
    calls = []

    def popen(*args, **kwargs):
        calls.append((args, kwargs))
        return object()

    command = ["nvim", "/checkout/ideation/example.md"]
    serve_mod._launch_editor(command, configured_editor=True, popen=popen)
    assert calls == [((command,), {})]


def test_desktop_opener_is_detached_with_closed_streams():
    calls = []

    def popen(*args, **kwargs):
        calls.append((args, kwargs))
        return object()

    command = ["xdg-open", "/checkout/ideation/example.md"]
    serve_mod._launch_editor(command, configured_editor=False, popen=popen)
    assert calls == [((command,), {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "start_new_session": True,
    })]


def test_edit_route_reports_a_fixed_failure_when_the_editor_cannot_launch(
        tmp_path):
    def fail(_argv):
        raise OSError("private launcher detail")

    rel = "ideation/staging/ideation-governance/README.md"
    with _serving(tmp_path, launcher=fail) as (host, port, calls):
        caps = _capabilities(host, port)
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": rel, "repository": "fixture-repo", "ref": "main"},
            headers=_console_headers(caps),
        )
    assert status == 500
    assert payload == {
        "ok": False,
        "error": "editor_launch_failed",
        "message": "the editor could not be opened; see the server log",
    }
    assert "private launcher detail" not in json.dumps(payload)
    assert calls == []


@pytest.mark.parametrize("body", [
    [],
    {"path": 7},
    {"path": "ideation/example.md"},
    {"path": "ideation/example.md", "repository": "fixture-repo"},
    {"path": "ideation/example.md", "repository": "", "ref": "main"},
    {"path": "ideation/example.md", "repository": "fixture-repo", "ref": ""},
    {"path": "ideation/example.md", "repository": 7},
    {"path": "ideation/example.md", "ref": 7},
])
def test_edit_route_refuses_an_invalid_body_before_launch(tmp_path, body):
    with _serving(tmp_path) as (host, port, calls):
        caps = _capabilities(host, port)
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body=body,
            headers=_console_headers(caps),
        )
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert calls == []


def test_edit_route_refuses_a_non_console_request_before_launch(tmp_path):
    with _serving(tmp_path) as (host, port, calls):
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": "../../../../etc/passwd"},
            headers={"Content-Type": "application/json"},
        )
    assert status == 403
    assert payload["error"] == "agent_invocation"
    assert calls == []


@pytest.mark.parametrize("path", [
    "../../../../etc/passwd",
    "ideation/staging/ideation-governance/no-longer-there.md",
    "project-register.yaml",
])
def test_edit_route_refuses_unavailable_documents(tmp_path, path):
    with _serving(tmp_path) as (host, port, calls):
        caps = _capabilities(host, port)
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": path, "repository": "fixture-repo", "ref": "main"},
            headers=_console_headers(caps),
        )
    assert status == 404
    assert payload["error"] == "document_unavailable"
    assert calls == []


def test_edit_route_is_unavailable_without_a_resolved_actor(tmp_path, monkeypatch):
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *args, **kwargs: None)
    with _serving(tmp_path, actor=None) as (host, port, calls):
        caps = _capabilities(host, port)
        assert caps["actions"]["edit"] is False
        status, payload = _request(
            host,
            port,
            "POST",
            "/actions/edit",
            body={"path": "ideation/staging/ideation-governance/README.md"},
            headers={"Content-Type": "application/json"},
        )
    assert status == 403
    assert payload["error"] == "action_unavailable"
    assert calls == []


_EDIT_HARNESS = """
import { createEditAction, editCapable } from './edit.mjs';

const calls = [];
const fetcher = async (url, options) => {
  calls.push({ url, options });
  return {
    ok: true,
    status: 200,
    async json() { return { ok: true, path: JSON.parse(options.body).path }; },
  };
};
const caps = {
  actions: { edit: true },
  console_token: 'console-token',
};
const key = { repository: 'fixture-repo', ref: 'main' };
const action = createEditAction({ caps, key: () => key, fetcher });
const result = await action.open('ideation/example.md');
let missingKeyError = null;
try {
  await createEditAction({ caps, key: null, fetcher }).open('ideation/example.md');
} catch (err) {
  missingKeyError = err.message;
}
console.log(JSON.stringify({
  result,
  missingKeyError,
  calls,
  capable: editCapable(caps),
  noToken: editCapable({ actions: { edit: true } }),
  unavailableEnabled: createEditAction({ caps: { actions: { edit: false } } }).enabled,
}));
"""


@pytest.mark.skipif(not NODE, reason="node not available")
def test_edit_js_posts_the_selected_key_with_the_console_token(tmp_path):
    shutil.copy(EDIT_JS, tmp_path / "edit.mjs")
    harness = tmp_path / "harness.mjs"
    harness.write_text(_EDIT_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness)], cwd=tmp_path, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["result"] == {"ok": True, "path": "ideation/example.md"}
    assert result["missingKeyError"] == "the selected document has no editable source key"
    assert result["capable"] is True
    assert result["noToken"] is False
    assert result["unavailableEnabled"] is False
    [call] = result["calls"]
    assert call["url"] == "/actions/edit"
    assert call["options"]["method"] == "POST"
    assert call["options"]["headers"] == {
        "Content-Type": "application/json",
        "X-XF-Console-Token": "console-token",
    }
    assert json.loads(call["options"]["body"]) == {
        "path": "ideation/example.md",
        "repository": "fixture-repo",
        "ref": "main",
    }
