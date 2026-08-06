"""Repository selector, keyed serving routes, the refresh route, and the
plain-script invocation fix (openxFactory change `add-dashboard-repo-selector`,
tasks 2.4, 3.2, 3.5-3.6 and verification 5.1-5.4).

Three layers, each proven where it lives:

  * the PURE selector view model runs in node against `repo-selector-model.js`
    itself (the roster, the freshness header contract, the stale notice, the
    passive newer-data hint, and the sparse-station note) — skipped when node is
    absent, exactly like the sibling model harnesses;
  * serve.py is driven over real HTTP for the keyed snapshot route, the snapshot
    index, per-entry `/source` confinement, the freshness headers, and BOTH
    refresh bindings (including every refusal: off-loopback regenerate, an
    unknown pair, and an unreachable source leaving the prior view in place);
  * the D12 relative-import fix is proven the only way it can be — by starting
    `serve.py` as a PLAIN SCRIPT in a subprocess (which is exactly how the served
    container image starts it) and POSTing to an action route, where the old
    relative imports produced a 500 with a traceback in the log.
"""

from __future__ import annotations

import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
MODEL_JS = WEB / "views" / "repo-selector-model.js"
SERVE_PY = REPO_ROOT / "scripts" / "ideation_dashboard" / "serve.py"
NODE = shutil.which("node")


def _snapshot(repository="fixture-repo", revision=PINNED_REVISION):
    return generate_snapshot(BASE_REPO, repository, source_revision=revision,
                             git=FakeGit(head=revision))


def _write_snapshot(path: Path, repository="fixture-repo", revision=PINNED_REVISION):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_snapshot(repository, revision)), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# the PURE view model, run in node against the real module
# ---------------------------------------------------------------------------

_NODE_HARNESS = """
import * as m from './repo-selector-model.mjs';
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const roster = m.buildRoster(input.index);
const active = m.resolveActive(input.index, input.requested || null);
const stored = m.resolveActive(input.index, 'MedxFactory@main');
// the stored-key restore path exactly as app.js runs it: sessionStorage text ->
// roster validation -> active option
const restore = (text) => {
  const key = m.resolveStoredKey(input.index, text);
  const option = m.resolveActive(input.index, key);
  return { key, activeId: option ? option.id : null };
};
const out = {
  roster: roster.map((o) => ({ id: o.id, label: o.label, kind: o.kind,
                              available: o.available, reason: o.unavailableReason })),
  activeId: active ? active.id : null,
  storedId: stored ? stored.id : null,
  freshness: m.freshnessLabel(active, input.snapshot),
  stale: m.staleNotice(active),
  newer: m.newerAvailable(active, input.snapshot),
  hint: m.hintLabel(active),
  emptyStations: m.emptyStations(input.snapshot).map((s) => s.key),
  sparse: m.sparseNotice(active, input.snapshot),
  emptyRoster: m.buildRoster(null).length,
  noIndexActive: m.resolveActive(null, null),
  keyRoundTrip: m.keyId('openxFactory', null) + '|' + JSON.stringify(m.parseKeyId('a@feat/x')),
  // stored-key validation (the request-safety pass)
  restoreValid: restore('MedxFactory@main'),
  restoreStale: restore('GoneFactory@main'),
  restoreHostile: restore('evil.example.com:8080/x@main'),
  restoreEmpty: restore(null),
  restoreNoIndex: m.resolveStoredKey(null, 'MedxFactory@main'),
  hasKeys: [m.hasKey(input.index, 'MedxFactory@main'),
            m.hasKey(input.index, 'GoneFactory@main'),
            m.hasKey(input.index, { repository: 'openxFactory', ref: 'main' }),
            m.hasKey(null, 'MedxFactory@main'),
            m.hasKey(input.index, null)],
  safeSegments: ['openxFactory', 'feat/x', 'v1.2.3-rc', '..', 'a..b', 'a b', 'a?b',
                 'a&ref=x', 'a#b', 'a%2Fb', '<script>', '', 'x'.repeat(201)]
                .map((s) => m.safeKeySegment(s)),
  safeKeys: [m.safeKey({ repository: 'openxFactory', ref: null }),
             m.safeKey({ repository: 'openxFactory', ref: 'a b' }),
             m.safeKey(null)],
};
console.log(JSON.stringify(out));
"""


def _run_model(payload, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "repo-selector-model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    data = tmp_path / "input.json"
    data.write_text(json.dumps(payload), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _index(**over):
    index = {
        "schema_version": 1, "kind": "ideation-dashboard-snapshot-index",
        "entries": [
            {"repository": "openxFactory", "ref": "main", "snapshot": "openxFactory-snapshot.json",
             "source_revision": "a" * 40, "generated_at": "2026-07-26T08:00:00Z",
             "origin": "fetched", "stale": False, "available": True},
            {"repository": "MedxFactory", "ref": "main", "snapshot": "MedxFactory-snapshot.json",
             "source_revision": "b" * 40, "generated_at": "2026-07-25T08:00:00Z",
             "origin": "fetched", "stale": False, "available": True,
             "display_name": "MedxFactory (medical)"},
            {"repository": "agenttower", "ref": "main", "snapshot": "agenttower-snapshot.json",
             "source_revision": "c" * 40, "origin": "fetched", "stale": False,
             "available": False, "unavailable_reason": "snapshot not retrievable"},
        ],
        "aggregates": [{"id": "xFactory", "display_name": "xFactory (all submodules)",
                        "members": [{"repository": "openxFactory"},
                                    {"repository": "MedxFactory", "ref": "main"}]}],
    }
    index.update(over)
    return index


def test_model_roster_is_the_index_and_only_the_index(tmp_path):
    r = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert [o["id"] for o in r["roster"]] == [
        "openxFactory@main", "MedxFactory@main", "agenttower@main", "xFactory@main"]
    assert r["roster"][1]["label"] == "MedxFactory (medical)"
    # an indexed-but-unfetchable repository stays SELECTABLE and says why
    assert r["roster"][2]["available"] is False
    assert r["roster"][2]["reason"] == "snapshot not retrievable"
    assert r["roster"][3]["kind"] == "aggregate"
    # no index at all -> no roster, no active option: today's single-snapshot page
    assert r["emptyRoster"] == 0
    assert r["noIndexActive"] is None
    assert r["keyRoundTrip"].startswith("openxFactory@main|")


def test_model_defaults_to_openxfactory_and_honours_a_stored_choice(tmp_path):
    r = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert r["activeId"] == "openxFactory@main"     # today's behaviour preserved
    assert r["storedId"] == "MedxFactory@main"      # a viewer's choice wins


def test_model_restores_a_stored_key_only_when_the_index_still_offers_it(tmp_path):
    """A stored (repository, ref) pair is a viewer PREFERENCE, not an instruction.
    It is validated against the roster before anything addresses a request with it:
    the pair the index advertises is kept, a pair that has left the index (or was
    never index-shaped) falls back to the default exactly as if nothing had been
    stored. Two bugs in one check — a vanished repository fetched forever, and
    storage-supplied text reaching the snapshot request URL (jssecurity:S8476)."""
    r = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)

    assert r["restoreValid"]["key"] == {"repository": "MedxFactory", "ref": "main"}
    assert r["restoreValid"]["activeId"] == "MedxFactory@main"

    # a repository that has left the roster: no stored key survives, and the
    # default (never the ghost) is what gets loaded
    assert r["restoreStale"]["key"] is None
    assert r["restoreStale"]["activeId"] == "openxFactory@main"

    # storage that does not hold an index-shaped pair is simply not honoured
    assert r["restoreHostile"]["key"] is None
    assert r["restoreHostile"]["activeId"] == "openxFactory@main"
    assert r["restoreEmpty"]["key"] is None
    assert r["restoreEmpty"]["activeId"] == "openxFactory@main"
    assert r["restoreNoIndex"] is None          # no index -> nothing to validate against

    assert r["hasKeys"] == [True, False, True, False, False]


def test_model_allow_lists_every_segment_that_can_reach_a_request_url(tmp_path):
    """The SHAPE half of request safety: a segment is rebuilt from the allow-list
    or refused. Query/path/fragment punctuation, `..`, whitespace, percent-escapes
    and over-long values never become part of a URL, so the index (a fetched,
    third-party document) cannot steer the shell's one state fetch."""
    r = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert r["safeSegments"] == [
        "openxFactory", "feat/x", "v1.2.3-rc",              # kept, unchanged
        None, None, None, None, None, None, None, None,     # .. a..b " " ? & # % <>
        None, None,                                        # empty, over-length
    ]
    assert r["safeKeys"] == [
        {"repository": "openxFactory", "ref": "main"},      # a null ref means main
        None,                                              # an unusable ref sinks the key
        None,
    ]


def test_app_shell_validates_the_stored_key_and_gates_both_request_builders():
    """app.js is the shell that owns the sole STATE fetch, so the wiring is pinned
    here: the stored key goes through `resolveStoredKey` before it can become
    active, and BOTH request builders (the snapshot URL and the keyed /source base)
    build from `safeKey`'s rebuilt pair rather than from the index's own strings."""
    app = (WEB / "app.js").read_text(encoding="utf-8")
    assert "resolveActive(index, resolveStoredKey(index, storedKey()))" in app, \
        "the stored key must be roster-validated before it becomes active"
    # the snapshot fetch and the /source base each derive from the allow-listed key
    for builder in ("function snapshotUrl(active) {", "function sourceBaseFor(active) {"):
        body = app.split(builder, 1)[1].split("\n}", 1)[0]
        assert "safeKey(active)" in body, f"{builder} does not gate on safeKey"
        assert "active.repository" not in body, f"{builder} still uses the raw index value"
    # and the raw stored text is read in exactly ONE place — through the validator
    calls = [line.strip() for line in app.splitlines()
             if "storedKey()" in line and "function storedKey()" not in line]
    assert calls == ["const active = resolveActive(index, resolveStoredKey(index, storedKey()));"]


def test_model_freshness_header_names_repo_ref_sha_and_stamp(tmp_path):
    r = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert r["freshness"] == "openxFactory @ main · " + "a" * 12 + " · generated 2026-07-26"
    assert r["stale"] is None


def test_model_stale_notice_is_loud_for_a_baked_fallback(tmp_path):
    index = _index()
    index["entries"][0].update({"origin": "baked", "stale": True,
                                "stale_reason": "the declared data source is unreachable",
                                "generated_at": "2026-07-20T08:00:00Z"})
    r = _run_model({"index": index, "snapshot": _snapshot()}, tmp_path)
    assert "stale snapshot" in r["stale"]
    assert "unreachable" in r["stale"]
    assert "2026-07-20" in r["stale"]               # the banner NAMES its generated-at


def test_model_passive_hint_fires_only_when_the_source_advertises_newer_data(tmp_path):
    quiet = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert quiet["newer"] is False

    index = _index()
    index["entries"][0].update({"latest_source_revision": "f" * 40,
                                "latest_generated_at": "2026-07-27T08:00:00Z",
                                "newer_available": True})
    loud = _run_model({"index": index, "snapshot": _snapshot()}, tmp_path)
    assert loud["newer"] is True
    assert "newer data available" in loud["hint"] and "refresh" in loud["hint"]


def test_model_names_the_empty_stations_of_a_sparse_repository(tmp_path):
    sparse = {"repository": "agenttower",
              "generation": {"source_revision": "c" * 40},
              "documents": [], "clusters": [], "possibles": [], "staged_topics": [],
              "changes": [{"id": "add-thing", "status": "active"}]}
    r = _run_model({"index": _index(), "requested": "agenttower@main",
                    "snapshot": sparse}, tmp_path)
    assert r["emptyStations"] == ["documents", "clusters", "possibles", "staged_topics"]
    assert "no ideation documents" in r["sparse"]
    assert "honest" in r["sparse"]                  # sparse is rendered, never refused
    full = _run_model({"index": _index(), "snapshot": _snapshot()}, tmp_path)
    assert full["sparse"] is None


# ---------------------------------------------------------------------------
# serve.py: the keyed routes, the index, and the freshness headers
# ---------------------------------------------------------------------------

@contextmanager
def _serving(**kwargs):
    httpd = serve_mod.build_server(WEB, kwargs.pop("snapshot"), kwargs.pop("checkout_root"),
                                  head=PINNED_REVISION, actor="tester", **kwargs)
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
    headers = {k.lower(): v for k, v in resp.getheaders()}
    status = resp.status
    conn.close()
    return status, headers, body


def _post(host, port, path, obj=None):
    conn = http.client.HTTPConnection(host, port, timeout=15)
    body = json.dumps(obj or {}).encode("utf-8")
    conn.request("POST", path, body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    raw = resp.read()
    status = resp.status
    conn.close()
    return status, (json.loads(raw) if raw else {})


def _published(root: Path, repos=("alpha", "beta")):
    root.mkdir(parents=True, exist_ok=True)
    entries = []
    for i, repository in enumerate(repos):
        revision = str(i + 1) * 40
        path = _write_snapshot(root / f"{repository}-snapshot.json", repository, revision)
        entry = reg.entry_from_snapshot_file(path, repository=repository)
        entry.location = path.name
        entries.append(entry)
    (root / "index.json").write_text(json.dumps(reg.build_index(entries, published=True)),
                                     encoding="utf-8")
    return entries


def test_single_repository_serve_is_unchanged_and_offers_one_entry(tmp_path):
    """The no-index plane: a server built exactly as every existing caller builds
    one serves its one snapshot at the same route, with one index entry."""
    snap = _write_snapshot(tmp_path / "snapshot.json")
    with _serving(snapshot=snap, checkout_root=BASE_REPO) as (host, port, _):
        status, headers, body = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
        istatus, _iheaders, ibody = _get(host, port, serve_mod.SNAPSHOT_INDEX_ROUTE)
    assert status == 200 and json.loads(body)["repository"] == "fixture-repo"
    assert headers["x-snapshot-repository"] == "fixture-repo"
    assert headers["x-snapshot-ref"] == "main"
    assert headers["x-snapshot-origin"] == "local"
    assert headers["x-snapshot-stale"] == "false"
    index = json.loads(ibody)
    assert index["kind"] == "ideation-dashboard-snapshot-index"
    assert [(e["repository"], e["ref"]) for e in index["entries"]] == [("fixture-repo", "main")]
    assert index["active"] == {"repository": "fixture-repo", "ref": "main"}


def test_keyed_snapshot_route_serves_each_registered_pair(tmp_path):
    published = tmp_path / "published"
    _published(published)
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(published)) as (host, port, _):
        _s, _h, active = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
        _s, beta_headers, beta = _get(host, port,
                                      serve_mod.SNAPSHOT_ROUTE + "?repository=beta&ref=main")
        _s2, _h2, refless = _get(host, port, serve_mod.SNAPSHOT_ROUTE + "?repository=beta")
        missing, _mh, _mb = _get(host, port, serve_mod.SNAPSHOT_ROUTE + "?repository=nope")
    assert json.loads(active)["repository"] == "alpha"
    assert json.loads(beta)["repository"] == "beta"
    assert beta_headers["x-snapshot-repository"] == "beta"
    assert beta_headers["x-snapshot-origin"] == "fetched"
    assert json.loads(refless)["repository"] == "beta"   # a ref-less request means main
    assert missing == 404


def test_keyed_source_route_confines_reads_per_entry(tmp_path):
    published = tmp_path / "published"
    _published(published)
    alpha_root = tmp_path / "checkouts" / "alpha"
    (alpha_root / "docs").mkdir(parents=True)
    (alpha_root / "docs" / "a.md").write_text("alpha only\n", encoding="utf-8")
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(published),
                  source_roots={"alpha": alpha_root}) as (host, port, _):
        ok, headers, body = _get(host, port, "/source/alpha@main/docs/a.md")
        # beta declared NO root: fail-closed, never another entry's checkout
        no_root, _h, _b = _get(host, port, "/source/beta@main/docs/a.md")
        escape, _h2, _b2 = _get(host, port, "/source/alpha@main/../../etc/passwd")
        # the unkeyed form still resolves through the ACTIVE entry
        plain, _h3, _b3 = _get(host, port, "/source/docs/a.md")
    assert ok == 200 and body == b"alpha only\n"
    assert headers["x-snapshot-repository"] == "alpha"
    assert no_root == 404
    assert escape == 404
    assert plain == 200


def test_unreachable_source_serves_the_baked_fallback_with_a_stale_header(tmp_path):
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(tmp_path / "nowhere")) as (host, port, _):
        status, headers, body = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
        _i, _ih, ibody = _get(host, port, serve_mod.SNAPSHOT_INDEX_ROUTE)
    assert status == 200 and json.loads(body)["repository"] == "alpha"
    assert headers["x-snapshot-origin"] == "baked"
    assert headers["x-snapshot-stale"] == "true"
    entry = json.loads(ibody)["entries"][0]
    assert entry["stale"] is True and entry["stale_reason"]


# ---------------------------------------------------------------------------
# the refresh route: two bindings, every refusal
# ---------------------------------------------------------------------------

def test_local_regenerate_reflects_a_new_document_without_a_restart(tmp_path):
    """The mission's acceptance, over HTTP: a document lands in the served
    checkout, the local refresh regenerates, and the SAME running server serves
    it — no restart, and only the derived snapshot was written."""
    checkout = tmp_path / "checkout"
    shutil.copytree(BASE_REPO, checkout)
    snap = _write_snapshot(tmp_path / "run" / "snapshot.json", "fixture-repo")
    with _serving(snapshot=snap, checkout_root=checkout,
                  repository="fixture-repo") as (host, port, _):
        _s, _h, before = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
        assert not [d for d in json.loads(before)["documents"]
                    if d["path"].endswith("brand-new-note.md")]
        (checkout / "ideation" / "brainstorm" / "brand-new-note.md").write_text(
            "# Brand new note\n\nStatus: brainstorm\nKind: note\n"
            "Summary: landed after the server started\nTopics: ideation-dashboard\n",
            encoding="utf-8")
        status, result = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
        _s2, headers, after = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
    assert status == 200, result
    assert result["ok"] is True and result["binding"] == "regenerate"
    assert [d for d in json.loads(after)["documents"]
            if d["path"].endswith("brand-new-note.md")], "the new document is not in the view"
    assert headers["x-snapshot-origin"] == "local"


def test_local_regenerate_is_refused_off_loopback(tmp_path):
    snap = _write_snapshot(tmp_path / "snapshot.json")
    with _serving(snapshot=snap, checkout_root=BASE_REPO) as (host, port, httpd):
        handler = getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)
        handler.loopback = False
        status, body = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
    assert status == 403
    assert body["error"] == "loopback_only"


def test_hosted_refetch_is_allowed_off_loopback_because_it_is_a_read(tmp_path):
    published = tmp_path / "published"
    _published(published, repos=("alpha",))
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(published)) as (host, port, httpd):
        handler = getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)
        handler.loopback = False   # the served plane binds 0.0.0.0 behind the ingress
        _c, caps, _cb = _get(host, port, serve_mod.CAPABILITIES_ROUTE)
        status, body = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE,
                             {"repository": "alpha"})
    assert status == 200, body
    assert body["binding"] == "refetch"
    assert body["source_revision"] == "1" * 40
    assert caps  # headers came back; the capability payload itself is asserted below


def test_capabilities_report_the_hosted_refetch_binding(tmp_path):
    published = tmp_path / "published"
    _published(published, repos=("alpha",))
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(published)) as (host, port, _):
        _s, _h, body = _get(host, port, serve_mod.CAPABILITIES_ROUTE)
    caps = json.loads(body)
    assert caps["actions"]["refresh"] is True
    assert caps["refresh"] == {"binding": "refetch", "loopback_only": False}


def test_refresh_failure_preserves_the_prior_view_and_reports_inline(tmp_path):
    published = tmp_path / "published"
    _published(published, repos=("alpha",))
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    with _serving(snapshot=baked, checkout_root=BASE_REPO, repository="alpha",
                  data_source=reg.DirectoryDataSource(published)) as (host, port, _):
        (published / "index.json").unlink()        # the source goes away
        status, body = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
        _s, _h, still = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
    assert status == 502
    assert body["ok"] is False and body["error"] == "source_unreachable"
    assert "previous snapshot is still shown" in body["message"]
    assert json.loads(still)["repository"] == "alpha"   # the view survived


def test_refresh_refuses_an_unknown_pair_and_a_malformed_body(tmp_path):
    snap = _write_snapshot(tmp_path / "snapshot.json")
    with _serving(snapshot=snap, checkout_root=BASE_REPO) as (host, port, _):
        unknown, ubody = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE,
                               {"repository": "nope"})
        bad, bbody = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE,
                           {"repository": ["not", "a", "string"]})
    assert unknown == 404 and ubody["error"] == "unknown_snapshot"
    assert bad == 400 and bbody["error"] == "invalid_body"


def test_refresh_is_unavailable_when_the_plane_offers_no_binding(tmp_path):
    """Fail-closed: no data source and no real checkout -> the affordance is
    absent in /capabilities AND refused at the route."""
    snap = _write_snapshot(tmp_path / "snapshot.json", "alpha")
    empty = tmp_path / "srv-empty"
    empty.mkdir()
    with _serving(snapshot=snap, checkout_root=empty, repository="alpha") as (host, port, _):
        _s, _h, caps = _get(host, port, serve_mod.CAPABILITIES_ROUTE)
        status, body = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
    assert json.loads(caps)["actions"]["refresh"] is False
    assert status == 403 and body["error"] == "action_unavailable"


def test_no_publication_build_or_rollout_route_exists(tmp_path):
    """The pod holds no build/rollout/publication authority (design D1): every
    such path is simply not a route."""
    snap = _write_snapshot(tmp_path / "snapshot.json")
    with _serving(snapshot=snap, checkout_root=BASE_REPO) as (host, port, _):
        for path in ("/actions/publish", "/actions/build", "/actions/rollout",
                     "/actions/rebake", "/actions/dispatch"):
            status, body = _post(host, port, path, {})
            assert status >= 400, f"{path} must not be served"
            assert body.get("error")


# ---------------------------------------------------------------------------
# D12: serve.py runs as a PLAIN SCRIPT, and its POST routes work there
# ---------------------------------------------------------------------------

@contextmanager
def _plain_script_server(tmp_path, extra_args=(), env=None):
    """Start serve.py the way the container image does — `python serve.py …`,
    NOT `python -m ideation_dashboard.serve` — and hand back its URL. The
    checkout is a COPY: this server's routes can write (the regenerate binding
    does), and a test never writes into the committed fixture tree."""
    snap = _write_snapshot(tmp_path / "snapshot.json")
    checkout = tmp_path / "checkout"
    shutil.copytree(BASE_REPO, checkout)
    proc = subprocess.Popen(
        [sys.executable, "-u", str(SERVE_PY), "--snapshot", str(snap),
         "--checkout-root", str(checkout), "--host", "127.0.0.1", "--port", "0",
         "--actor", "tester", *extra_args],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        cwd=str(tmp_path), env=env)
    port = None
    deadline = time.time() + 30
    try:
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                break
            match = re.search(r"http://127\.0\.0\.1:(\d+)/", line)
            if match:
                port = int(match.group(1))
                break
        assert port, "serve.py did not report a URL when run as a plain script"
        yield "127.0.0.1", port, proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover
            proc.kill()


def test_plain_script_invocation_serves_get_and_post_routes(tmp_path):
    """The D12 regression: under plain-script invocation the old relative
    `from . import …` imports made EVERY POST route 500 (the handler died before
    writing a response — a client saw the connection close). Here the new refresh
    route runs its binding and the unknown-action refusal — the path that goes
    through the error catalog, i.e. the crash site — answers structurally.

    (The notebook route is deliberately NOT posted: it would project a real
    scratch notebook. Its import path is pinned statically instead, below.)"""
    with _plain_script_server(tmp_path) as (host, port, _proc):
        snap_status, _h, snap_body = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
        index_status, _ih, index_body = _get(host, port, serve_mod.SNAPSHOT_INDEX_ROUTE)
        refresh_status, refresh_body = _post(host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
        unknown_status, unknown_body = _post(host, port, "/actions/nope", {})
    assert snap_status == 200 and json.loads(snap_body)["repository"] == "fixture-repo"
    assert index_status == 200
    assert json.loads(index_body)["kind"] == "ideation-dashboard-snapshot-index"
    # the regenerate binding ran — never a 500 traceback
    assert refresh_status == 200, refresh_body
    assert refresh_body["binding"] == "regenerate"
    assert unknown_status != 500 and unknown_body.get("error")


def test_hosted_posts_do_not_load_notebook_only_dependencies(tmp_path):
    """The lean hosted image has no PyYAML: refetch and route refusals must not
    import the NotebookLM/workbench stack merely because the request is POST."""
    published = tmp_path / "published"
    _published(published, repos=("fixture-repo",))
    blocked = tmp_path / "blocked-imports"
    blocked.mkdir()
    (blocked / "yaml.py").write_text(
        "raise RuntimeError('PyYAML must not load in the hosted POST plane')\n",
        encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(blocked), env.get("PYTHONPATH")) if part)
    with _plain_script_server(
            tmp_path,
            extra_args=("--data-source-dir", str(published),
                        "--repository", "fixture-repo",
                        "--host", "0.0.0.0"),
            env=env) as (host, port, _proc):
        refresh_status, refresh_body = _post(
            host, port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
        unknown_status, unknown_body = _post(host, port, "/actions/nope", {})
        notebook_status, notebook_body = _post(
            host, port, serve_mod.ACTIONS_NOTEBOOK_ROUTE,
            {"tile_kind": "cluster", "tile_id": "anything"})
    assert refresh_status == 200, refresh_body
    assert refresh_body["binding"] == "refetch"
    assert unknown_status == 404
    assert unknown_body["error"] == "unknown_action"
    assert notebook_status == 403
    assert notebook_body["error"] == "loopback_only"


def test_serve_module_uses_no_relative_imports(tmp_path):
    """The D12 fix, pinned: serve.py is the module the container runs as a plain
    SCRIPT, where a relative import has no parent package. A new `from . import …`
    here would 500 a POST route in production while every module-invoked test
    stayed green — so the absence is asserted, not assumed."""
    text = SERVE_PY.read_text(encoding="utf-8")
    offenders = [
        f"{n}: {line.strip()}"
        for n, line in enumerate(text.splitlines(), 1)
        if re.match(r"\s*from\s+\.\w*\s+import\b", line)
    ]
    assert not offenders, "relative import in serve.py (D12):\n" + "\n".join(offenders)
    assert "from ideation_dashboard import notebook_action" in text
    assert "from ideation_dashboard import workbench" in text
    assert "from ideation_dashboard import gate_routes" in text


def test_module_invocation_still_works(tmp_path):
    """The documented live-serve command (`python3 -m ideation_dashboard.serve`)
    keeps working — the fix adds a path, it does not move one."""
    snap = _write_snapshot(tmp_path / "snapshot.json")
    proc = subprocess.Popen(
        [sys.executable, "-u", "-m", "ideation_dashboard.serve",
         "--snapshot", str(snap), "--checkout-root", str(BASE_REPO),
         "--host", "127.0.0.1", "--port", "0"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        cwd=str(REPO_ROOT / "scripts"))
    try:
        port = None
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                break
            match = re.search(r"http://127\.0\.0\.1:(\d+)/", line)
            if match:
                port = int(match.group(1))
                break
        assert port, "module invocation did not report a URL"
        status, body = _post("127.0.0.1", port, serve_mod.ACTIONS_REFRESH_ROUTE, {})
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover
            proc.kill()
    assert status == 200, body
    assert body["binding"] == "regenerate"


# ---------------------------------------------------------------------------
# Project scoping (add-project-scoped-selection): buildProjects + scopeRoster,
# run in node against the REAL model exactly like the roster derivations above.
# ---------------------------------------------------------------------------

_PROJECT_HARNESS = """
import { buildProjects, buildRoster, scopeRoster } from './repo-selector-model.mjs';
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const roster = buildRoster(input.index);
const projects = buildProjects(input.projection);
const ids = (scope) => scopeRoster(roster, projects, scope).map((o) => o.id);
const out = {
  projects,
  scopedIds: ids(input.scope),
  clearedIds: ids(null),
  unknownIds: ids('no-such-project'),
  noProjection: buildProjects(null),
  malformed: buildProjects({ projects: [{ id: '' }, { id: 'x' },
                                        { id: 'y', repositories: [] },
                                        'junk', null] }),
};
console.log(JSON.stringify(out));
"""


def _run_projects(payload, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "repo-selector-model.mjs")
    (tmp_path / "harness.mjs").write_text(_PROJECT_HARNESS, encoding="utf-8")
    data = tmp_path / "input.json"
    data.write_text(json.dumps(payload), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _projection():
    return {"kind": "project-register-projection", "projects": [
        {"id": "core", "name": "Core", "repositories": ["openxFactory"]},
        {"id": "medx", "name": "Medx", "repositories": ["MedxFactory", "agenttower"]},
    ]}


def test_project_scoping_narrows_the_roster_to_members(tmp_path):
    r = _run_projects({"index": _index(), "projection": _projection(),
                       "scope": "medx"}, tmp_path)
    assert [p["id"] for p in r["projects"]] == ["core", "medx"]
    # members only — including the unavailable one (it stays selectable and
    # says why, exactly as in the unscoped roster); the aggregate drops out
    # because it is not composed purely of medx members
    assert r["scopedIds"] == ["MedxFactory@main", "agenttower@main"]


def test_clearing_or_unknown_scope_restores_the_full_roster(tmp_path):
    r = _run_projects({"index": _index(), "projection": _projection(),
                       "scope": "medx"}, tmp_path)
    full = ["openxFactory@main", "MedxFactory@main", "agenttower@main", "xFactory@main"]
    assert r["clearedIds"] == full
    # a stored project that stopped existing degrades to unscoped, silently
    assert r["unknownIds"] == full


def test_an_aggregate_survives_scoping_only_when_purely_member_composed(tmp_path):
    projection = {"projects": [
        {"id": "both", "name": "Both",
         "repositories": ["openxFactory", "MedxFactory"]},
    ]}
    r = _run_projects({"index": _index(), "projection": projection,
                       "scope": "both"}, tmp_path)
    assert r["scopedIds"] == ["openxFactory@main", "MedxFactory@main", "xFactory@main"]


def test_projection_absence_and_malformed_rows_degrade_to_nothing(tmp_path):
    r = _run_projects({"index": _index(), "projection": None, "scope": None},
                      tmp_path)
    assert r["noProjection"] == []
    # rows with no id, no members, or the wrong shape are dropped, not thrown
    assert r["malformed"] == []
