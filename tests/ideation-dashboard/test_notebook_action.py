"""v2 "Open in NotebookLM" tile action (local-backend seam debut).

Covers the whole seam, following the existing ideation-dashboard conventions:

  * capability discovery — `compute_capabilities`/`_is_loopback` pure, plus the
    served-vs-local verdict (nlm + real checkout + loopback);
  * doc-set resolution — the pure snapshot→doc-set derivation per tile kind,
    including the proposal MINUS review/ records rule and unknown-tile null;
  * the action orchestration end-to-end over a FAKE nlm (a stateful in-memory
    shim, never the real CLI) + a tmp checkout: create-or-rebind, the
    content-hash no-op on re-click, the bound gitignored manifest, and the
    structured refusals (unknown kind/id, malformed id, nlm-failure, empty set);
  * serve.py over real HTTP — GET /capabilities on/off, POST happy path, the
    structured JSON refusals (never a traceback), and the loopback-only guard;
  * the web surface — notebook.js pure functions run in node (like model.js),
    and a source scan for the textContent/window.open discipline.

All against the REAL fixture snapshot (FakeGit + PINNED_REVISION), the same
substrate as test_generator.py/test_renderer.py."""

from __future__ import annotations

import http.client
import json
import re
import shutil
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import (  # noqa: F401
    BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit, find_openxfactory_validator,
)

from ideation_dashboard import notebook_action as na
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import workbench as wb
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
NOTEBOOK_JS = WEB / "views" / "notebook.js"
NODE = shutil.which("node")


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ----------------------------------------------------------------------------
# a stateful FAKE nlm — an in-memory notebook/source store. Tests NEVER touch
# the real CLI; the adapter's `runner` is injected with this callable.
# ----------------------------------------------------------------------------

class FakeNlm:
    def __init__(self, *, fail: bool = False) -> None:
        self.notebooks: dict[str, dict] = {}
        self.sources: dict[str, dict] = {}
        self._n = 0
        self.fail = fail
        self.calls: list[tuple] = []

    def _next(self, prefix: str) -> str:
        self._n += 1
        return f"{prefix}{self._n}"

    def add_calls(self) -> list[tuple]:
        return [c for c in self.calls if c[:2] == ("source", "add")]

    def __call__(self, *args, parse: bool = True, **kw):
        self.calls.append(args)
        if self.fail:
            raise RuntimeError("nlm boom")
        cmd = args[:2]
        if cmd == ("notebook", "list"):
            return list(self.notebooks.values())
        if cmd == ("notebook", "create"):
            nid = self._next("nb-")
            self.notebooks[nid] = {"id": nid, "title": args[2]}
            return {"id": nid, "title": args[2]}
        if cmd == ("notebook", "get"):
            nid = args[2]
            return {"id": nid, "url": "https://notebooklm.google.com/notebook/" + nid}
        if cmd == ("notebook", "delete"):
            self.notebooks.pop(args[2], None)
            return ""
        if cmd == ("source", "list"):
            return [s for s in self.sources.values() if s["notebook"] == args[2]]
        if cmd == ("source", "add"):
            sid = self._next("src-")
            self.sources[sid] = {"id": sid, "title": args[args.index("--title") + 1], "notebook": args[2]}
            return ""
        if cmd == ("source", "delete"):
            self.sources.pop(args[2], None)
            return ""
        raise AssertionError(f"unexpected nlm call: {args!r}")


def _adapter(fake: FakeNlm, *, available: bool = True) -> wb.NotebookAdapter:
    return wb.NotebookAdapter(runner=fake, available=available)


@pytest.fixture
def checkout(tmp_path):
    """An isolated, writable copy of the fixture repo so the manifest write
    (into ideation/workbench/) never touches the tracked fixture tree."""
    dest = tmp_path / "checkout"
    shutil.copytree(BASE_REPO, dest)
    return dest


# ----------------------------------------------------------------------------
# capability discovery (pure)
# ----------------------------------------------------------------------------

def test_compute_capabilities_requires_nlm_checkout_and_loopback():
    # `refresh` (add-dashboard-repo-selector D7) is OFF unless a binding is
    # supplied — no data source and no served checkout means no affordance.
    #
    # The `actions` dict GREW by one key on 2026-07-26
    # (007-workbench-branch-sessions T083): `session`, which FR-048 requires the
    # HOSTED probe to state rather than leave a reader to infer from the gate leg.
    # These assertions stay EXACT dict equality — the pin is not relaxed, it
    # measures one more thing (the hosted-confinement cases have their own tests
    # in test_session_snapshot.py).
    no_refresh = {"binding": None, "loopback_only": True}
    assert serve_mod.compute_capabilities(nlm_present=True, checkout_real=True, loopback=True) == {
        "actions": {"notebook": True, "gate": False, "refresh": False,
                    "session": False, "edit": False}, "actor": None,
        "refresh": no_refresh}
    # any missing leg -> the action is absent (the served image lacks all three)
    for kwargs in (
        {"nlm_present": False, "checkout_real": True, "loopback": True},
        {"nlm_present": True, "checkout_real": False, "loopback": True},
        {"nlm_present": True, "checkout_real": True, "loopback": False},
    ):
        assert serve_mod.compute_capabilities(**kwargs) == {
            "actions": {"notebook": False, "gate": False, "refresh": False,
                        "session": False, "edit": False}, "actor": None,
            "refresh": no_refresh}
    # the gate leg (intent-plane §3): loopback + real checkout + resolved actor.
    # The session leg carries the SAME three conditions — a session write IS a
    # gate write — and is stated separately so a hosted probe says "no session"
    # outright (FR-048).
    gated = serve_mod.compute_capabilities(
        nlm_present=False, checkout_real=True, loopback=True, actor="brett")
    assert gated["actions"]["gate"] is True and gated["actor"] == "brett"
    assert gated["actions"]["session"] is True


def test_is_loopback():
    assert serve_mod._is_loopback("127.0.0.1")
    assert serve_mod._is_loopback("::1")
    assert not serve_mod._is_loopback("0.0.0.0")
    assert not serve_mod._is_loopback("dashboard.example.org")


def test_checkout_real_rejects_empty_sentinel(tmp_path):
    empty = tmp_path / "srv-empty"
    empty.mkdir()
    assert serve_mod._checkout_real(BASE_REPO) is True
    assert serve_mod._checkout_real(empty) is False
    assert serve_mod._checkout_real(tmp_path / "does-not-exist") is False


# ----------------------------------------------------------------------------
# doc-set resolution (pure) — per tile kind, incl. proposal MINUS review/
# ----------------------------------------------------------------------------

def test_resolve_cluster_documents_are_member_docs():
    snap = _snapshot()
    docs = na.resolve_tile_documents("cluster", "cl-avatar", snap)
    cluster = next(c for c in snap["clusters"] if c["id"] == "cl-avatar")
    assert docs == [e["document"] for e in cluster["document_edges"]]


def test_resolve_staged_documents_are_topic_files():
    snap = _snapshot()
    docs = na.resolve_tile_documents("staged", "ideation-governance", snap)
    topic = next(t for t in snap["staged_topics"] if t["staging_id"] == "ideation-governance")
    assert docs == topic["files"]


def test_resolve_proposal_documents_drop_review_records():
    snap = {
        "changes": [{
            "id": "add-x",
            "files": [
                "openspec/changes/add-x/proposal.md",
                "openspec/changes/add-x/design.md",
                "openspec/changes/add-x/tasks.md",
                "openspec/changes/add-x/supporting-docs/note.md",
                "openspec/changes/add-x/review/2026-07-14-pre-realization-review.md",
            ],
        }],
    }
    docs = na.resolve_tile_documents("proposal", "add-x", snap)
    assert docs == [
        "openspec/changes/add-x/proposal.md",
        "openspec/changes/add-x/design.md",
        "openspec/changes/add-x/tasks.md",
        "openspec/changes/add-x/supporting-docs/note.md",
    ]
    assert all("review" not in Path(p).parts for p in docs)


def test_resolve_unknown_tile_and_kind_are_null():
    snap = _snapshot()
    assert na.resolve_tile_documents("cluster", "does-not-exist", snap) is None
    assert na.resolve_tile_documents("staged", "nope", snap) is None
    assert na.resolve_tile_documents("proposal", "nope", snap) is None
    assert na.resolve_tile_documents("bogus-kind", "cl-avatar", snap) is None


# ----------------------------------------------------------------------------
# run_notebook_action — orchestration over the fake nlm + tmp checkout
# ----------------------------------------------------------------------------

def test_cluster_action_creates_notebook_and_binds_manifest(checkout):
    snap = _snapshot()
    fake = FakeNlm()
    result = na.run_notebook_action(
        tile_kind="cluster", tile_id="cl-avatar", snapshot=snap,
        checkout_root=checkout, adapter=_adapter(fake), now="2026-07-15T00:00:00Z")

    assert result["notebook_alias"] == "xf-wb-cluster-cl-avatar"
    assert result["created"] is True
    assert result["sources"] == 1
    assert result["url"].endswith("/notebook/nb-1")

    # the bound manifest lives under the gitignored workbench prefix and binds
    # the alias (so the orphan sweep keeps the notebook alive).
    manifest = checkout / "ideation" / "workbench" / "cluster-cl-avatar.workbench.yaml"
    assert manifest.is_file()
    import yaml
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    assert data["notebook"] == {"alias": "xf-wb-cluster-cl-avatar"}
    assert data["seed"] == {"kind": "cluster-seeded", "cluster_id": "cl-avatar"}
    assert data["kind"] == "ideation-workbench"


def test_staged_and_proposal_doc_sets_flow_through(checkout):
    snap = _snapshot()
    fake = FakeNlm()
    staged = na.run_notebook_action(
        tile_kind="staged", tile_id="ideation-governance", snapshot=snap,
        checkout_root=checkout, adapter=_adapter(fake), now="2026-07-15T00:00:00Z")
    assert staged["notebook_alias"] == "xf-wb-staged-ideation-governance"
    assert staged["sources"] == 1
    # ad-hoc seed with a recorded manual-include reason (not cluster-seeded)
    import yaml
    data = yaml.safe_load((checkout / "ideation" / "workbench"
                           / "staged-ideation-governance.workbench.yaml").read_text())
    assert data["seed"] == {"kind": "ad-hoc"}
    assert data["members"][0]["via"] == "manual-include"
    assert data["members"][0]["reason"]


def test_reclick_is_a_content_hash_no_op(checkout):
    snap = _snapshot()
    fake = FakeNlm()
    first = na.run_notebook_action(
        tile_kind="cluster", tile_id="cl-avatar", snapshot=snap,
        checkout_root=checkout, adapter=_adapter(fake), now="2026-07-15T00:00:00Z")
    adds_after_first = len(fake.add_calls())
    assert adds_after_first == 1 and first["created"] is True

    second = na.run_notebook_action(
        tile_kind="cluster", tile_id="cl-avatar", snapshot=snap,
        checkout_root=checkout, adapter=_adapter(fake), now="2026-07-15T00:01:00Z")
    # unchanged content -> rebind (not created) and NO new source add
    assert second["created"] is False
    assert len(fake.add_calls()) == adds_after_first
    assert len(fake.sources) == 1


def test_unknown_kind_id_and_malformed_id_are_client_errors(checkout):
    snap = _snapshot()
    adapter = _adapter(FakeNlm())
    with pytest.raises(na.NotebookActionError) as unknown_kind:
        na.run_notebook_action(tile_kind="doc", tile_id="cl-avatar", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert unknown_kind.value.status == 400
    assert unknown_kind.value.code == na.ERR_UNKNOWN_TILE_KIND

    with pytest.raises(na.NotebookActionError) as bad_id:
        na.run_notebook_action(tile_kind="cluster", tile_id="../etc/passwd", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert bad_id.value.status == 400
    assert bad_id.value.code == na.ERR_INVALID_TILE_ID

    with pytest.raises(na.NotebookActionError) as unknown_id:
        na.run_notebook_action(tile_kind="cluster", tile_id="cl-nope", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert unknown_id.value.status == 404
    assert unknown_id.value.code == na.ERR_UNKNOWN_TILE


def test_error_catalog_messages_are_fixed_and_input_free():
    # The wire never carries request-derived data: every catalog message is a
    # fixed literal, and an error's body() is built ONLY from the catalog.
    for code, (status, message) in na.ERROR_CATALOG.items():
        assert isinstance(status, int) and message
        assert na.error_body(code) == {"error": code, "message": message}
    err = na.NotebookActionError(na.ERR_UNKNOWN_TILE, log_detail="cl-EVIL private detail")
    assert err.body() == {"error": "unknown_tile",
                          "message": "tile not found in the current snapshot"}
    assert "cl-EVIL" not in str(err.body())  # detail is server-side-only


def test_nlm_failure_degrades_to_structured_503(checkout):
    snap = _snapshot()
    fake = FakeNlm(fail=True)  # every nlm call raises; adapter degrades
    adapter = _adapter(fake)
    with pytest.raises(na.NotebookActionError) as exc:
        na.run_notebook_action(tile_kind="cluster", tile_id="cl-avatar", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert exc.value.status == 503
    assert exc.value.code == na.ERR_NLM_FAILED
    # the nlm detail is captured for the server log, never in the wire body
    assert exc.value.log_detail
    assert exc.value.body() == na.error_body(na.ERR_NLM_FAILED)
    # no manifest is written when the projection never succeeds
    assert not (checkout / "ideation" / "workbench").exists() or \
        not any((checkout / "ideation" / "workbench").glob("*.workbench.yaml"))


def test_nlm_unavailable_is_503(checkout):
    snap = _snapshot()
    adapter = _adapter(FakeNlm(), available=False)
    with pytest.raises(na.NotebookActionError) as exc:
        na.run_notebook_action(tile_kind="cluster", tile_id="cl-avatar", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert exc.value.status == 503
    assert exc.value.code == na.ERR_NLM_UNAVAILABLE


def test_tile_with_no_readable_documents_is_422(checkout):
    # a cluster whose member doc is not present in the checkout resolves to an
    # empty (all-confined-away) set -> 422, never a fabricated notebook.
    snap = {"repository": "fixture-repo",
            "clusters": [{"id": "cl-ghost",
                          "document_edges": [{"document": "ideation/brainstorm/not-here.md"}]}]}
    adapter = _adapter(FakeNlm())
    with pytest.raises(na.NotebookActionError) as exc:
        na.run_notebook_action(tile_kind="cluster", tile_id="cl-ghost", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert exc.value.status == 422
    assert exc.value.code == na.ERR_NO_READABLE_DOCUMENTS


def test_document_paths_are_confined_to_the_checkout(checkout):
    # a hostile snapshot path can never escape the checkout root: it is dropped
    # by the read-side guard, leaving no readable doc -> 422 (never a read of
    # /etc/passwd).
    snap = {"repository": "fixture-repo",
            "clusters": [{"id": "cl-eek",
                          "document_edges": [{"document": "../../../../etc/passwd"}]}]}
    adapter = _adapter(FakeNlm())
    with pytest.raises(na.NotebookActionError) as exc:
        na.run_notebook_action(tile_kind="cluster", tile_id="cl-eek", snapshot=snap,
                               checkout_root=checkout, adapter=adapter)
    assert exc.value.status == 422


def test_bound_manifest_is_schema_valid(checkout):
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout for the pinned validator")
    snap = _snapshot()
    na.run_notebook_action(tile_kind="proposal", tile_id="add-ideation-governance", snapshot=snap,
                           checkout_root=checkout, adapter=_adapter(FakeNlm()), now="2026-07-15T00:00:00Z")
    manifest = next((checkout / "ideation" / "workbench").glob("*.workbench.yaml"))
    result = wb.validate_manifest(manifest, validator=validator, strict=True)
    assert result.ok, result.summary()


# ----------------------------------------------------------------------------
# serve.py over real HTTP — capabilities probe + the loopback-only POST action
# ----------------------------------------------------------------------------

@contextmanager
def _serving(checkout_root, *, adapter_factory):
    snap_path = checkout_root / "run-snapshot.json"
    snap_path.write_text(json.dumps(_snapshot()), encoding="utf-8")
    # actor pinned for determinism: without it build_server would resolve the
    # environment's global git user.name into the capability verdict.
    httpd = serve_mod.build_server(WEB, snap_path, checkout_root,
                                   head=PINNED_REVISION, adapter_factory=adapter_factory,
                                   actor="tester")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port, httpd
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _get(host, port, path):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = resp.read()
    status = resp.status
    conn.close()
    return status, body


def _post_json(host, port, path, obj):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("POST", path, body=json.dumps(obj).encode("utf-8"),
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    body = resp.read()
    status = resp.status
    conn.close()
    return status, (json.loads(body) if body else {})


def test_capabilities_route_reports_available_when_nlm_present(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, _):
        status, body = _get(host, port, serve_mod.CAPABILITIES_ROUTE)
    assert status == 200
    # The local plane also offers the REGENERATE refresh binding (a real
    # checkout on a loopback bind) — add-dashboard-repo-selector D7.
    #
    # The payload GREW by one key on 2026-07-27 (PR #49 review finding 2):
    # `console_token`, the per-serve human-console token FR-019's third clause is
    # realized with. It is minted ONLY where the session capability is true, and
    # this route is the only place it is published — the served page reads it
    # same-origin, and no cross-origin page can. It is a fresh random value per
    # serve, so it is checked for shape here and the rest of the payload stays
    # EXACT dict equality (the pin is not relaxed; it measures one more thing).
    caps = json.loads(body)
    token = caps.pop("console_token")
    assert isinstance(token, str) and len(token) >= 32
    # add-dashboard-account-menu: `hosted_actor` grew onto the payload the same
    # additive way `console_token` did — resolved per request from the
    # gateway-stamped `X-Auth-Request-User` header, `None` when absent, as here
    # (no gateway in front of this loopback probe). Popped so the rest of the
    # payload stays EXACT dict equality; the pin is not relaxed.
    assert caps.pop("hosted_actor") is None
    assert caps == {
        "actions": {"notebook": True, "gate": True, "refresh": True,
                    "session": True, "edit": True},
        "actor": "tester",
        # THE ONE REPOSITORY THIS SERVE WRITES TO (add-composed-view-authoring).
        # Declared rather than inferred: under a composed project view the
        # rendered snapshot's `repository` is the PROJECT id, which names no
        # repository and is refused by `refuse_foreign_repository`. Reported
        # from the same authority that refusal uses, so a client handed this
        # value can never be refused for naming the wrong one.
        "repository": "fixture-repo",
        "refresh": {"binding": "regenerate", "loopback_only": True}}


def test_capabilities_route_reports_unavailable_when_nlm_absent(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake, available=False)) as (host, port, _):
        status, body = _get(host, port, serve_mod.CAPABILITIES_ROUTE)
    assert status == 200
    caps = json.loads(body)
    assert caps["actions"]["notebook"] is False   # nlm absent
    assert caps["actions"]["gate"] is True        # gate leg independent of nlm


def test_post_notebook_action_happy_path(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, _):
        status, body = _post_json(host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
                                  {"tile_kind": "cluster", "tile_id": "cl-avatar"})
    assert status == 200, body
    assert body["notebook_alias"] == "xf-wb-cluster-cl-avatar"
    assert body["created"] is True
    assert body["url"].startswith("https://notebooklm.google.com/notebook/")


def test_post_unknown_tile_is_structured_404(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, _):
        status, body = _post_json(host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
                                  {"tile_kind": "cluster", "tile_id": "cl-nope"})
    assert status == 404
    # structured catalog refusal, never a traceback — and never the raw input
    assert body == na.error_body(na.ERR_UNKNOWN_TILE)
    assert "cl-nope" not in json.dumps(body)


def test_post_never_reflects_request_data(checkout):
    # Request-derived values (however hostile) never appear in any response
    # body: every refusal is a fixed catalog {error, message} pair.
    marker = "EVIL-MARKER-<script>alert(1)</script>"
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, _):
        status, body = _post_json(host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
                                  {"tile_kind": "cluster", "tile_id": marker})
    assert status == 400
    assert body == na.error_body(na.ERR_INVALID_TILE_ID)
    assert "EVIL-MARKER" not in json.dumps(body)


def test_post_action_unavailable_when_capability_off(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake, available=False)) as (host, port, _):
        status, body = _post_json(host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
                                  {"tile_kind": "cluster", "tile_id": "cl-avatar"})
    assert status == 503
    assert body == na.error_body(na.ERR_ACTION_UNAVAILABLE)


def test_post_action_rejected_on_non_loopback_bind(checkout):
    # Simulate a non-loopback bind config: the write route is refused with 403
    # even when the capability would otherwise be present (defence in depth).
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, httpd):
        handler_cls = getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)
        handler_cls.loopback = False
        status, body = _post_json(host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
                                  {"tile_kind": "cluster", "tile_id": "cl-avatar"})
    assert status == 403
    assert body == na.error_body(na.ERR_LOOPBACK_ONLY)


def test_post_malformed_body_is_400(checkout):
    fake = FakeNlm()
    with _serving(checkout, adapter_factory=lambda: _adapter(fake)) as (host, port, _):
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("POST", serve_mod.ACTIONS_NOTEBOOK_ROUTE, body=b"not json",
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        status = resp.status
        body = json.loads(resp.read())
        conn.close()
    assert status == 400
    assert body == na.error_body(na.ERR_INVALID_BODY)


# ----------------------------------------------------------------------------
# notebook.js — pure functions run in node (like model.js), + a source scan
# ----------------------------------------------------------------------------

_NB_HARNESS = """
import { notebookCapable, probeCapabilities, postNotebookAction,
         createNotebookAction, CAPABILITIES_ROUTE, ACTIONS_NOTEBOOK_ROUTE } from './notebook.mjs';
const ok = async () => ({ ok: true, status: 200, json: async () => ({ actions: { notebook: true } }) });
const notFound = async () => ({ ok: false, status: 404, json: async () => ({}) });
const boom = async () => { throw new Error('down'); };
// the backend's catalog refusal shape: the human message is preferred, the
// stable code is the fallback for older/odd bodies.
const postErr = async () => ({ ok: false, status: 503,
  json: async () => ({ error: 'nlm_unavailable', message: 'nlm unavailable - notebook action skipped, not blocked' }) });
const postErrCodeOnly = async () => ({ ok: false, status: 503, json: async () => ({ error: 'nlm_unavailable' }) });
let postErrMsg = null;
try { await postNotebookAction({ tile_kind: 'cluster', tile_id: 'c' }, postErr); }
catch (e) { postErrMsg = e.message; }
let postErrCode = null;
try { await postNotebookAction({ tile_kind: 'cluster', tile_id: 'c' }, postErrCodeOnly); }
catch (e) { postErrCode = e.message; }
console.log(JSON.stringify({
  capYes: notebookCapable({ actions: { notebook: true } }),
  capNoFalse: notebookCapable({ actions: { notebook: false } }),
  capNoMissing: notebookCapable({}),
  capNoNull: notebookCapable(null),
  probeOn: (await probeCapabilities(ok)).actions.notebook,
  probe404: (await probeCapabilities(notFound)).actions.notebook,
  probeThrow: (await probeCapabilities(boom)).actions.notebook,
  disabledButtonIsNull: createNotebookAction({ enabled: false }).button('cluster', 'c') === null,
  postErrMsg,
  postErrCode,
  routes: [CAPABILITIES_ROUTE, ACTIONS_NOTEBOOK_ROUTE],
}));
"""


def _run_node_notebook(tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS probe")
    shutil.copy(NOTEBOOK_JS, tmp_path / "notebook.mjs")
    (tmp_path / "harness.mjs").write_text(_NB_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_notebook_js_capability_and_degradation(tmp_path):
    r = _run_node_notebook(tmp_path)
    assert r["capYes"] is True
    assert r["capNoFalse"] is False and r["capNoMissing"] is False and r["capNoNull"] is False
    # the probe degrades to "not available" on a 404 (static image) or a throw (file://)
    assert r["probeOn"] is True
    assert r["probe404"] is False and r["probeThrow"] is False
    # a disabled controller mounts no button; the POST surfaces the backend's
    # fixed catalog message (preferred) or the stable code (fallback)
    assert r["disabledButtonIsNull"] is True
    assert r["postErrMsg"] == "nlm unavailable - notebook action skipped, not blocked"
    assert r["postErrCode"] == "nlm_unavailable"
    assert r["routes"] == ["/capabilities", "/actions/notebook"]


def test_notebook_js_is_textcontent_safe_and_opens_with_noopener():
    text = NOTEBOOK_JS.read_text(encoding="utf-8")
    # no innerHTML ASSIGNMENT anywhere (this module composes with textContent
    # only; a comment may still name the sink it deliberately avoids)
    assert not re.search(r"\.innerHTML\s*=", text)
    # a new tab is opened with noopener (no reverse-tabnabbing handle)
    assert 'window.open(url, "_blank", "noopener")' in text
    # the only two fetches target the two named backend-seam routes
    fetch_args = re.findall(r"fetch\(([^,]+),", text)
    assert {a.strip() for a in fetch_args} == {"CAPABILITIES_ROUTE", "ACTIONS_NOTEBOOK_ROUTE"}
