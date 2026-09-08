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

from conftest import (BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit,
                      serve_surface_paths, serve_surface_source)

from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
MODEL_JS = WEB / "views" / "repo-selector-model.js"
SERVE_PY = REPO_ROOT / "scripts" / "ideation_dashboard" / "serve.py"
NODE = shutil.which("node")

# The D12 relative-import guard (see test_serve_module_uses_no_relative_imports
# below): a single shared pattern, used both by the production scan and by
# test_the_relative_import_guard_catches_every_dot_and_segment_depth, so a
# future narrowing of the regex turns the pinning test red rather than leaving
# it green against its own separately-maintained copy. Matches one or more
# leading dots (sibling- or parent-relative) followed by an optional
# dotted module path (`pkg`, `pkg.sub`, ...) before `import`.
RELATIVE_IMPORT_RE = re.compile(r"\s*from\s+\.+[\w.]*\s+import\b")


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
    # EVERY FILE THE SERVE IS MADE OF (§ 2.4 PR 2 of 4 split it into four):
    # the D12 hazard is a property of the SCRIPT, and a relative import in a
    # module the script imports 500s exactly the same route. Widened, never
    # narrowed — one of these files is still `serve.py` itself.
    # RELATIVE_IMPORT_RE matches one or more leading dots (sibling- or
    # PARENT-relative: `from .. import y`, `from ..pkg import y`) followed by
    # an optional DOTTED module path (`from .pkg.sub import y`, `from
    # ..pkg.sub import y`) — a bare `\.\w*` catches only a single-segment
    # sibling import and misses both widenings, and all of them fail
    # identically once serve.py runs as a plain script (Copilot review, PR
    # #748).
    offenders = [
        f"{path.name} {n}: {line.strip()}"
        for path in serve_surface_paths()
        for n, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1)
        if RELATIVE_IMPORT_RE.match(line)
    ]
    assert not offenders, "relative import in the serve (D12):\n" + "\n".join(
        offenders)
    # Second widening in this same edit (undisclosed in the PR-2 repoint
    # table's row 11, which describes only the offenders scan above): these
    # three POSITIVE anchors moved from `SERVE_PY.read_text()` to the whole
    # surface too. Only `notebook_action` actually moved (now
    # serve_project.py only); `workbench` and `gate_routes` still resolve in
    # serve.py at their pre-split lines, so pinning them to the surface is
    # strictly a widening, never a narrowing — nothing here goes hollow.
    text = serve_surface_source()
    assert "from ideation_dashboard import notebook_action" in text
    assert "from ideation_dashboard import workbench" in text
    assert "from ideation_dashboard import gate_routes" in text


@pytest.mark.parametrize("line", [
    "from . import x",
    "from .pkg import x",
    "from .. import x",
    "from ..pkg import x",
    "  from ... import x",
    "from .pkg.sub import x",
    "from ..pkg.sub import x",
])
def test_the_relative_import_guard_catches_every_dot_and_segment_depth(line):
    """A prior version of this guard's regex (`\\.\\w*`, one dot and at most
    one module segment) matched `from . import x` and `from .pkg import x`
    but silently missed both a PARENT-relative import (`from .. import x`,
    `from ..pkg import x`) and a MULTI-SEGMENT one (`from .pkg.sub import
    x`, `from ..pkg.sub import x`) — all of which fail identically once
    serve.py runs as a plain script. Exercises the SAME `RELATIVE_IMPORT_RE`
    the production scan above uses (not a separately-maintained copy), so a
    future narrowing of that one pattern is caught here by a red test, not by
    a production 500."""
    assert RELATIVE_IMPORT_RE.match(line), (
        f"the relative-import guard does not match {line!r}")


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
import { buildPendingProjects, buildProjects, buildRoster, scopeRoster } from './repo-selector-model.mjs';
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const roster = buildRoster(input.index);
const projects = buildProjects(input.projection);
const ids = (scope) => scopeRoster(roster, projects, scope).map((o) => o.id);
const out = {
  projects,
  pending: buildPendingProjects(input.projection),
  scopedIds: ids(input.scope),
  clearedIds: ids(null),
  unknownIds: ids('no-such-project'),
  noProjection: buildProjects(null),
  noPendingProjection: buildPendingProjects(null),
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
    # rows with no id or the wrong shape are dropped, not thrown — but a row
    # WITHOUT members is a legal EMPTY project (D17), kept with a normalized
    # empty list whether the member key is absent or []
    assert r["malformed"] == [
        {"id": "x", "name": "x", "repositories": []},
        {"id": "y", "name": "y", "repositories": []},
    ]


def test_an_empty_project_surfaces_in_the_picker_and_scopes_to_nothing(tmp_path):
    """D17 regression (Brett, 2026-08-06): the register carried the empty
    project `xfactory`, create-project correctly refused the duplicate — yet
    the dropdown never listed it, because the picker model still required a
    member. An empty project must surface (it is selected first, populated
    via the filter's add line); scoped, it truthfully narrows to no members
    while addableRepositories keeps offering the whole known universe."""
    projection = _projection()
    projection["projects"].append(
        {"id": "xfactory", "name": "xFactory", "repositories": []})
    r = _run_projects({"index": _index(), "projection": projection,
                       "scope": "xfactory"}, tmp_path)
    assert [p["id"] for p in r["projects"]] == ["core", "medx", "xfactory"]
    assert r["scopedIds"] == []


def test_pending_commissions_render_beside_truth_never_inside_it(tmp_path):
    """Design D-e: `pending` is the INTENT plane — a fresh create-project
    commission is visible, deduplicated against the register the moment the
    fulfilment lands, and never scope-bearing (it is absent from `projects`,
    so scoping falls through to the unknown-project degrade)."""
    projection = _projection()
    projection["pending"] = [
        {"id": "field-pilots", "name": "Field Pilots", "repositories": ["x"]},
        {"id": "core", "name": "Core (already landed)"},   # register wins
        {"id": "", "name": "malformed"},
        None,
    ]
    r = _run_projects({"index": _index(), "projection": projection,
                       "scope": "field-pilots"}, tmp_path)
    assert r["pending"] == [{"id": "field-pilots", "name": "Field Pilots"}]
    assert [p["id"] for p in r["projects"]] == ["core", "medx"]
    # a pending id never scopes: full roster, exactly the unknown-scope degrade
    assert r["scopedIds"] == r["clearedIds"]
    assert r["noPendingProjection"] == []


# ---------------------------------------------------------------------------
# The openDox project-first header derivations (add-opendox-project-header
# D13/D14/D15): the current-project default, the filter rows, manage-mode
# diffing, and the pending-edit plane — run in node against the REAL model.
# ---------------------------------------------------------------------------

_HEADER_HARNESS = """
import { addableRepositories, buildPendingEdits, buildProjects, buildRoster,
         defaultProjectScope, netPendingEdit, projectFilterRows,
         repositoryVisible, toggleVisibility, visibleRepositories }
  from './repo-selector-model.mjs';
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const roster = buildRoster(input.index);
const projects = buildProjects(input.projection);
const project = projects.find((p) => p.id === input.projectId) || null;
const out = {
  netQueued: netPendingEdit(input.queuedEdits || [], project),
  netNone: netPendingEdit([], project),
  // D19 — the visible set: default, stored, stale, deliberate none, toggles
  visible: [visibleRepositories(project, {}),
            visibleRepositories(project, { medx: ['agenttower', 'MedxFactory'] }),
            visibleRepositories(project, { medx: ['departed'] }),
            visibleRepositories(project, { medx: [] }),
            visibleRepositories(null, {})],
  toggles: [toggleVisibility(['MedxFactory'], 'agenttower', project?.repositories),
            toggleVisibility(['MedxFactory', 'agenttower'], 'MedxFactory',
                             project?.repositories)],
  scopes: [defaultProjectScope(projects, input.stored),
           defaultProjectScope(projects, 'no-such'),
           defaultProjectScope(projects, null),
           defaultProjectScope([], 'anything')],
  rows: projectFilterRows(roster, project).map((r) => ({
    kind: r.kind,
    repository: r.repository || null,
    hasOption: !!r.option,
    available: r.option ? r.option.available : null,
    // which REF a row resolves to: a repository row must be main, a session
    // row must be its own branch (2026-08-10)
    ref: r.option ? r.option.ref : null,
  })),
  noProjectRows: projectFilterRows(roster, null),
  addable: addableRepositories(roster, projects, project),
  visibility: [repositoryVisible('MedxFactory', project,
                 { repository: 'MedxFactory', ref: 'main' }),
               repositoryVisible('agenttower', project,
                 { repository: 'medx', ref: 'main' }),
               repositoryVisible('agenttower', project,
                 { repository: 'MedxFactory', ref: 'main' }),
               repositoryVisible('agenttower', project, null)],
  pendingEdits: buildPendingEdits(input.projection),
};
console.log(JSON.stringify(out));
"""


def _run_header(payload, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "repo-selector-model.mjs")
    (tmp_path / "harness.mjs").write_text(_HEADER_HARNESS, encoding="utf-8")
    data = tmp_path / "input.json"
    data.write_text(json.dumps(payload), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _header_projection():
    return {"projects": [
        {"id": "medx", "name": "Medx",
         "repositories": ["MedxFactory", "agenttower", "ghost-repo"]},
        {"id": "core", "name": "Core", "repositories": ["openxFactory"]},
    ], "pending_edits": [
        {"project_id": "medx", "add": ["openChart"], "remove": ["agenttower"]},
        {"project_id": "", "add": ["junk"]},
        None,
    ]}


def _header_index():
    index = _index()
    index["aggregates"] = [{"id": "medx", "display_name": "Medx (all)",
                            "members": [{"repository": "MedxFactory"},
                                        {"repository": "agenttower"}]}]
    return index


def test_the_header_model_derivations(tmp_path):
    r = _run_header({"index": _header_index(),
                     "projection": _header_projection(),
                     "projectId": "medx", "stored": "core"}, tmp_path)
    # D13: stored-if-real, else first, null when no projects exist
    assert r["scopes"] == ["core", "medx", "medx", None]
    # D14: the all-repos line first (armed — the index carries the medx
    # aggregate), then one row per member; the unpublished member has no
    # option; the unavailable one keeps its honest flag
    assert r["rows"][0] == {"kind": "all", "repository": None,
                            "hasOption": True, "available": True, "ref": "main"}
    assert r["rows"][1:] == [
        {"kind": "repo", "repository": "MedxFactory", "hasOption": True,
         "available": True, "ref": "main"},
        {"kind": "repo", "repository": "agenttower", "hasOption": True,
         "available": False, "ref": "main"},
        {"kind": "repo", "repository": "ghost-repo", "hasOption": False,
         "available": None, "ref": None},
    ]
    assert r["noProjectRows"] == []
    # D16: the add line's candidates — roster + register known, minus members
    assert r["addable"] == ["openxFactory"]
    # D16: the eyeball — the active single repo, or any member under the
    # project's own merged view; never without an active view
    assert r["visibility"] == [True, True, False, False]
    # the pending-edit plane drops malformed rows
    assert r["pendingEdits"] == [{"projectId": "medx", "add": ["openChart"],
                                  "remove": ["agenttower"]}]


def test_a_repository_row_is_main_and_a_live_session_is_its_own_row(tmp_path):
    """MEASURED on the live plane, 2026-08-10, answering Brett's "how do I get
    to the rest of the workbench on this doc?".

    A repository row took the FIRST roster option for that repository, and the
    serving index lists a repository's refs sorted — so `draft/…` sorts before
    `main`. Clicking `openxFactory` keyed the whole dashboard to whichever
    branch happened to sort first: a session the human had not chosen and could
    not see they were on. The same arbitrary pick was the ONLY way onto a
    session branch, which is why the branch a create had just opened looked
    unreachable — it was reachable by accident, under the wrong name.

    Both halves: a repository row resolves to MAIN deliberately, and every
    other advertised ref becomes an addressable session row of its own (FR-014
    — the index advertises a live session as an ordinary row, so this asks the
    server nothing new)."""
    index = _header_index()
    # two live sessions on one member, plus one on a member that has no main,
    # in the sorted order the serve really publishes them in
    index["entries"] = [
        {"repository": "MedxFactory", "ref": "draft/beta", "available": True,
         "snapshot": "medx-beta.json"},
        {"repository": "MedxFactory", "ref": "draft/alpha", "available": True,
         "snapshot": "medx-alpha.json"},
        *index["entries"],
        {"repository": "ghost-repo", "ref": "draft/only", "available": True,
         "snapshot": "ghost.json"},
    ]
    r = _run_header({"index": index, "projection": _header_projection(),
                     "projectId": "medx", "stored": "medx"}, tmp_path)
    rows = [(x["kind"], x["repository"], x["ref"]) for x in r["rows"]]

    # the repository row is MAIN, never the first-sorted draft
    assert ("repo", "MedxFactory", "main") in rows
    assert ("repo", "MedxFactory", "draft/beta") not in rows
    # …and each live session is its own row, under its repository
    assert ("session", "MedxFactory", "draft/beta") in rows
    assert ("session", "MedxFactory", "draft/alpha") in rows
    # a member that publishes ONLY a session still resolves — it falls back
    # rather than vanishing — and is not then repeated as a session row
    assert ("repo", "ghost-repo", "draft/only") in rows
    assert ("session", "ghost-repo", "draft/only") not in rows
    # ordering: a session sits directly under the repository it belongs to
    medx = rows.index(("repo", "MedxFactory", "main"))
    assert rows[medx + 1][0] == "session" and rows[medx + 1][1] == "MedxFactory"
    # main is never offered twice
    assert sum(1 for k, repo, ref in rows
               if repo == "MedxFactory" and ref == "main") == 1


def test_queued_edits_net_into_one_overlay(tmp_path):
    """Topic D18 — edits queue, so the popover's badge overlay is the NET of
    the project's queued rows replayed oldest-first: a later addition
    cancels a pending removal (and vice versa), a duplicate never doubles,
    and an 'addition' of an existing member badges nothing."""
    queued = [
        {"projectId": "medx", "add": ["openChart"], "remove": []},
        {"projectId": "medx", "add": [], "remove": ["agenttower"]},
        {"projectId": "medx", "add": ["agenttower"], "remove": []},
        {"projectId": "medx", "add": [], "remove": ["openChart"]},
        {"projectId": "medx", "add": ["HealthLinc", "HealthLinc",
                                      "MedxFactory"], "remove": []},
        {"projectId": "other", "add": ["ignored"], "remove": []},
    ]
    r = _run_header({"index": _header_index(),
                     "projection": _header_projection(),
                     "projectId": "medx", "stored": None,
                     "queuedEdits": queued}, tmp_path)
    assert r["netQueued"] == {"add": ["HealthLinc"], "remove": []}
    assert r["netNone"] is None


def test_the_visible_set_resolves_against_current_membership(tmp_path):
    """Topic D19 — the eyeball became the control, so the stored set is
    resolved against the project's CURRENT members: nothing stored means
    every member (the composition's own default), a stored set narrows in
    member order, a set membership outlived falls back to every member
    rather than a view of nothing, and a deliberate empty set stays
    empty."""
    r = _run_header({"index": _header_index(),
                     "projection": _header_projection(),
                     "projectId": "medx", "stored": None}, tmp_path)
    members = ["MedxFactory", "agenttower", "ghost-repo"]
    assert r["visible"] == [
        members,                                   # never ticked
        ["MedxFactory", "agenttower"],             # stored, in member order
        members,                                   # stale set -> the default
        [],                                        # the human's "none"
        [],                                        # no project at all
    ]
    # a tick adds or removes, always leaving the set in member order
    assert r["toggles"] == [["MedxFactory", "agenttower"], ["agenttower"]]
