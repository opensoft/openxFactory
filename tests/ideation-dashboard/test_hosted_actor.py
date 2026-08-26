"""THE HOSTED ACTOR on `/capabilities` (add-dashboard-account-menu).

The dox-auth gateway stamps the verified username into `X-Auth-Request-User` on
every proxied request (having stripped any client value first). This change
surfaces that header on `/capabilities` as an additive, PER-REQUEST,
DISPLAY-ONLY `hosted_actor` field — `null` when the header is absent — beside
the existing per-request `repository` field.

Three claims, each failing for its own reason if the wiring is wrong:

  * **PRESENT → the stamped username.** A request carrying the header reads the
    value back on `hosted_actor`, resolved per request (not from startup).
  * **ABSENT → `null`.** A local / loopback serve with no header reads `null`.
  * **THE FIELD AUTHORIZES NOTHING (Requirement 2).** On a HOSTED (non-loopback)
    plane the write/gate/edit actions are all `false`, and they STAY `false`
    whether or not the header is present — the capability verdict is keyed on
    the loopback console verdict, never on identity presence. A gated write
    stays refused with the header present.

Reuses the real-HTTP harness the provenance suite established: a live loopback
server over `http.client`, both outbound seams faked (`FakeNotebookAdapter`,
`FakePullRequests`), so nothing here can reach a network.
"""

from __future__ import annotations

import http.client
import json
import threading
from contextlib import contextmanager
from pathlib import Path

from conftest import REPO_ROOT

from session_fixtures import (
    FakeNotebookAdapter,
    FakePullRequests,
)

from ideation_dashboard import serve as serve_mod
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
AUTH_HEADER = "X-Auth-Request-User"


@contextmanager
def _serving(repo, snapshot_path, *, host="127.0.0.1", actor="brett", **kw):
    """A serve over REAL HTTP against the scratch checkout. `host` is injectable
    so the HOSTED (non-loopback) plane can be exercised — a serve on `0.0.0.0`
    is classified non-loopback and grants no write/gate/edit action."""
    kw.setdefault("adapter_factory", FakeNotebookAdapter)
    kw.setdefault("pull_request_factory", FakePullRequests)
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, host=host,
                                   actor=actor, **kw)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    raw = json.dumps(body).encode("utf-8") if body is not None else None
    hdrs = dict(headers or {})
    if raw is not None:
        hdrs.setdefault("Content-Type", "application/json")
        hdrs["Content-Length"] = str(len(raw))
    conn.request(method, path, body=raw, headers=hdrs)
    response = conn.getresponse()
    payload = response.read().decode("utf-8")
    status = response.status
    conn.close()
    try:
        return status, json.loads(payload)
    except ValueError:
        return status, payload


def _served_snapshot(repo, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


# ==========================================================================
# PRESENT → the stamped username; ABSENT → null
# ==========================================================================

def test_a_stamped_header_reads_back_on_hosted_actor(scratch_repo, tmp_path):
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    with _serving(scratch_repo, snapshot) as (host, port):
        status, caps = _request(host, port, "GET", "/capabilities",
                                headers={AUTH_HEADER: "alice"})
    assert status == 200, caps
    assert caps["hosted_actor"] == "alice"


def test_no_header_reads_null(scratch_repo, tmp_path):
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    with _serving(scratch_repo, snapshot) as (host, port):
        status, caps = _request(host, port, "GET", "/capabilities")
    assert status == 200, caps
    assert caps["hosted_actor"] is None


def test_a_blank_header_reads_null_not_empty_string(scratch_repo, tmp_path):
    """The serve reports `null`, not `""`, for a present-but-empty header — the
    account menu must fall through to its local label, not to an empty name."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    with _serving(scratch_repo, snapshot) as (host, port):
        status, caps = _request(host, port, "GET", "/capabilities",
                                headers={AUTH_HEADER: ""})
    assert status == 200, caps
    assert caps["hosted_actor"] is None


# ==========================================================================
# THE GUARD (Requirement 2) — the header flips no capability verdict
# ==========================================================================

def test_on_a_hosted_plane_the_header_flips_no_capability_verdict(scratch_repo,
                                                                  tmp_path):
    """A HOSTED (non-loopback) serve grants no write/gate/edit action — and the
    presence of a stamped `hosted_actor` does NOT change that. The verdict is
    keyed on the loopback console verdict, never on identity presence, so the
    `actions` map is byte-identical with and without the header."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    with _serving(scratch_repo, snapshot, host="0.0.0.0") as (host, port):
        _s, without = _request(host, port, "GET", "/capabilities")
        _s2, with_actor = _request(host, port, "GET", "/capabilities",
                                   headers={AUTH_HEADER: "alice"})

    # the identity differs; the verdict does not
    assert without["hosted_actor"] is None
    assert with_actor["hosted_actor"] == "alice"
    assert with_actor["actions"] == without["actions"]
    for verb in ("gate", "edit", "session"):
        assert with_actor["actions"][verb] is False, verb


def test_a_gated_write_stays_refused_with_the_header_present(scratch_repo,
                                                             tmp_path):
    """Requirement 2's scenario: a hosted request carrying a stamped actor still
    cannot write or gate. The session verb is refused exactly as it is without
    the header — the header buys no authority."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    body = {"title": "x", "summary": "y", "topics": ["a"],
            "area": "ideation/staging/demo-topic/",
            "repository_context": scratch_repo.repository,
            "scope_kind": "staged-topic", "scope_id": "demo-topic"}
    with _serving(scratch_repo, snapshot, host="0.0.0.0") as (host, port):
        status, payload = _request(host, port, "POST",
                                   "/actions/gate/create-document", body=body,
                                   headers={AUTH_HEADER: "alice"})
    assert status != 200, payload
