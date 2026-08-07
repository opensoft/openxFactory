"""Register-derived project aggregates + the composed merged view
(add-project-merged-projection, topic decisions D9–D11).

Python half: `SnapshotSource.derived_project_aggregates` (membership from
the register ∩ the registry, D11's collision rule, the no-member skip),
the index advertising derived aggregates, and `compose_view` resolving
declared AND derived ids with the hosted publishable-only guard.

Node half: the composed-view model — the D9 topic-tail cluster union, the
D10 read-only capability derivation, member-ref resolution — and the wheel
action table's `open-repo` jump visibility, run against the REAL modules.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_snapshot_registry import _published_tree, _write_snapshot

from ideation_dashboard import snapshot_registry as reg

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
NODE = shutil.which("node")

REGISTER = """\
schema_version: 1
kind: project-register
projects:
  - id: pilots
    name: Field Pilots
    repositories: [alpha, beta]
  - id: solo
    name: Solo
    repositories: [alpha, ghost-repo]
  - id: ghosts
    name: Ghosts
    repositories: [ghost-repo]
"""


def _source(tmp_path, register: str | None = REGISTER, **kwargs):
    published = tmp_path / "published"
    published.mkdir(exist_ok=True)
    _published_tree(published, repos=("alpha", "beta"))
    baked = _write_snapshot(tmp_path / "baked" / "snapshot.json", "alpha", "0" * 40)
    register_path = None
    if register is not None:
        register_path = tmp_path / "project-register.yaml"
        register_path.write_text(register, encoding="utf-8")
    source = reg.SnapshotSource(
        baked_snapshot=baked, repository="alpha",
        data_source=reg.DirectoryDataSource(published),
        project_register=register_path, **kwargs)
    source.bootstrap()
    return source


def test_derived_aggregates_follow_the_register_and_the_registry(tmp_path):
    source = _source(tmp_path)
    derived = {a.id: a for a in source.derived_project_aggregates()}
    # both members resolvable -> both in; an unknown repo is dropped from its
    # project; a project with NO resolvable member derives nothing
    assert derived["pilots"].members == [("alpha", "main"), ("beta", "main")]
    assert derived["pilots"].display_name == "Field Pilots"
    assert derived["solo"].members == [("alpha", "main")]
    assert "ghosts" not in derived


def test_a_declared_aggregate_wins_the_id_collision(tmp_path):
    source = _source(tmp_path)
    declared = reg.Aggregate(id="pilots", members=[("beta", "main")],
                             display_name="Hand-declared")
    source.registry.register_aggregate(declared)
    derived_ids = {a.id for a in source.derived_project_aggregates()}
    assert "pilots" not in derived_ids                 # explicit beats derived
    assert source.resolve_aggregate("pilots").display_name == "Hand-declared"


def test_the_index_advertises_derived_aggregates(tmp_path):
    source = _source(tmp_path)
    doc = source.index_document(peek=False)
    rows = {a["id"]: a for a in doc.get("aggregates") or []}
    assert rows["pilots"]["display_name"] == "Field Pilots"
    assert rows["pilots"]["members"] == [
        {"repository": "alpha", "ref": "main"},
        {"repository": "beta", "ref": "main"}]
    assert "ghosts" not in rows


def test_no_register_derives_nothing(tmp_path):
    source = _source(tmp_path, register=None)
    assert source.derived_project_aggregates() == []
    assert source.compose_view("pilots") is None


def test_compose_view_resolves_a_derived_project_aggregate(tmp_path):
    source = _source(tmp_path)
    composed = source.compose_view("pilots")
    assert composed is not None
    members = composed["generation"]["composed_from"]
    assert [m["repository"] for m in members] == ["alpha", "beta"]
    # namespaced ids, repository badges — the ratified composition, untouched
    assert all("::" in c["id"] for c in composed["clusters"])
    repos = {c["repository"] for c in composed["clusters"]}
    assert repos == {"alpha", "beta"}


def test_publishable_only_drops_session_members_before_composition(tmp_path):
    source = _source(tmp_path)
    source.registry.register_aggregate(reg.Aggregate(
        id="mixed", members=[("alpha", "main"), ("alpha", "draft/topic")]))
    open_view = source.compose_view("mixed")
    hosted_view = source.compose_view("mixed", publishable_only=True)
    assert [m["repository"] for m in
            hosted_view["generation"]["composed_from"]] == ["alpha"]
    # a declared aggregate with ONLY unpublishable members composes nothing
    source.registry.register_aggregate(reg.Aggregate(
        id="sessions", members=[("alpha", "draft/topic")]))
    assert source.compose_view("sessions", publishable_only=True) is None
    assert open_view is not None


# ---------------------------------------------------------------------------
# node half: composed-model union/gating + the wheel's open-repo row
# ---------------------------------------------------------------------------

_NODE_HARNESS = """
import { VIEW_INTERSECTION, VIEW_UNION, composedView, isComposed, itemTail,
         memberRef, readOnlyCaps, topicTail, unionClusters, visibleSnapshot }
  from './composed-model.mjs';
import { WHEEL_ACTIONS, actionsFor, jumpRepository } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const snapshot = input.snapshot;
const view = composedView(snapshot);
// D19 — the visible set under each mode, over the SAME composed fixture
const shape = (s) => ({
  clusters: s.clusters.map((c) => c.id),
  documents: (s.documents || []).map((d) => d.id),
  members: s.generation.composed_from.map((m) => m.repository),
});
const visible = {
  everyMember: shape(visibleSnapshot(snapshot, null, VIEW_UNION)),
  unionAlpha: shape(visibleSnapshot(snapshot, ['alpha'], VIEW_UNION)),
  intersection: shape(visibleSnapshot(snapshot, ['alpha', 'beta'], VIEW_INTERSECTION)),
  none: shape(visibleSnapshot(snapshot, [], VIEW_UNION)),
  ghost: shape(visibleSnapshot(snapshot, ['alpha', 'nope'], VIEW_UNION)),
  soloTallies: composedView(visibleSnapshot(snapshot, ['alpha'], VIEW_UNION))
    .clusters.map((c) => [c.id, c.tallies.document_links, c.repositories]),
  passthrough: visibleSnapshot({ clusters: [{ id: 'cl-a' }] }, ['x'], VIEW_UNION),
  tails: [itemTail({ id: 'a::x' }), itemTail({ staging_id: 't' }),
          itemTail({ keyword: 'k' }), itemTail(null)],
};
const env = { composed: isComposed(snapshot), gate: false, notebook: false,
              commissioned: () => false, applied: null };
const plainEnv = { ...env, composed: false };
const clusterItem = { id: 'cl-kill-switch',
  ref: view.clusters.find((c) => c.id === 'cl-kill-switch') };
const docItem = { id: 'alpha::doc', ref: { id: 'alpha::doc', repository: 'alpha' } };
const out = {
  composed: isComposed(snapshot),
  tails: [topicTail('alpha::cl-x'), topicTail('cl-plain')],
  unionIds: view.clusters.map((c) => c.id).sort(),
  merged: view.clusters.find((c) => c.id === 'cl-kill-switch'),
  passthrough: composedView({ generation: {} , clusters: [{ id: 'cl-a' }] }).clusters,
  caps: readOnlyCaps({ actions: { gate: true, refresh: true, notebook: true },
                       actor: 'brett' }),
  memberRefs: [memberRef(snapshot, 'beta'), memberRef(snapshot, 'nope')],
  clusterActions: actionsFor('clusters', clusterItem, env).map((a) => a.id),
  docActions: actionsFor('documents', docItem, env).map((a) => a.id),
  plainDocActions: actionsFor('documents', docItem, plainEnv).map((a) => a.id),
  jumps: [jumpRepository(docItem), jumpRepository(clusterItem),
          jumpRepository({ ref: { repositories: ['a', 'b'] } })],
  visible,
};
console.log(JSON.stringify(out));
"""


def _run_node(payload, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WEB / "views" / "composed-model.js", tmp_path / "composed-model.mjs")
    shutil.copy(WEB / "views" / "wheel-model.js", tmp_path / "wheel-model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    data = tmp_path / "input.json"
    data.write_text(json.dumps(payload), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _composed_snapshot():
    return {
        "repository": "pilots",
        "generation": {"source_revision": "composed", "composed_from": [
            {"repository": "alpha", "ref": "main", "source_revision": "1" * 40},
            {"repository": "beta", "ref": "session/x", "source_revision": "2" * 40},
        ]},
        "documents": [
            {"id": "alpha::docs/shared.md", "repository": "alpha"},
            {"id": "beta::docs/shared.md", "repository": "beta"},
            {"id": "alpha::docs/only-alpha.md", "repository": "alpha"},
        ],
        "clusters": [
            {"id": "alpha::cl-kill-switch", "name": "Kill Switch",
             "repository": "alpha", "ref": "main",
             "document_edges": [{"document": "alpha::d1"}],
             "tallies": {"document_links": 2}},
            {"id": "beta::cl-kill-switch", "name": "Kill Switch",
             "repository": "beta", "ref": "session/x",
             "document_edges": [{"document": "beta::d2"}],
             "tallies": {"document_links": 3}},
            {"id": "beta::cl-only-beta", "name": "Only Beta",
             "repository": "beta", "ref": "session/x",
             "tallies": {"document_links": 1}},
        ],
    }


def test_the_union_merges_same_topic_clusters_and_gates_read_only(tmp_path):
    r = _run_node({"snapshot": _composed_snapshot()}, tmp_path)
    assert r["composed"] is True
    assert r["tails"] == ["cl-x", "cl-plain"]
    # D9: one tile per topic tail; single-member groups keep the merged shape
    assert r["unionIds"] == ["cl-kill-switch", "cl-only-beta"]
    merged = r["merged"]
    assert merged["repositories"] == ["alpha", "beta"]
    assert merged["tallies"] == {"document_links": 5}
    assert [e["document"] for e in merged["document_edges"]] == ["alpha::d1", "beta::d2"]
    assert len(merged["composed_members"]) == 2
    # a non-composed snapshot passes through untouched
    assert r["passthrough"] == [{"id": "cl-a"}]
    # D10: every acting capability off, the read-only facts untouched
    assert r["caps"]["actions"] == {"gate": False, "refresh": True,
                                    "notebook": False, "session": False,
                                    "edit": False}
    assert r["caps"]["actor"] == "brett"
    # the jump ref comes from the composition stamps (session member kept)
    assert r["memberRefs"] == ["session/x", "main"]


def test_the_visible_set_narrows_the_composed_view_under_both_modes(tmp_path):
    """Topic D19 (Brett, 2026-08-07): the composed view spans the VISIBLE
    member set — union (everything the ticked repositories have) or
    intersection (only what EVERY ticked repository has). Narrowing happens
    before the cluster union, so tallies count the visible set only, and
    `composed_from` is trimmed so the freshness header names what is on
    screen."""
    v = _run_node({"snapshot": _composed_snapshot()}, tmp_path)["visible"]

    # no stored set: every member, exactly the pre-D19 composition
    assert v["everyMember"]["members"] == ["alpha", "beta"]
    assert v["everyMember"]["clusters"] == [
        "alpha::cl-kill-switch", "beta::cl-kill-switch", "beta::cl-only-beta"]

    # union of one: that repository's items, and composed_from follows
    assert v["unionAlpha"]["members"] == ["alpha"]
    assert v["unionAlpha"]["clusters"] == ["alpha::cl-kill-switch"]
    assert v["unionAlpha"]["documents"] == [
        "alpha::docs/shared.md", "alpha::docs/only-alpha.md"]

    # intersection: only identities BOTH carry — the shared doc and the
    # shared topic survive as each repository's own row (badged, separately
    # openable); alpha's private document and beta's private cluster do not
    assert v["intersection"]["documents"] == [
        "alpha::docs/shared.md", "beta::docs/shared.md"]
    assert v["intersection"]["clusters"] == [
        "alpha::cl-kill-switch", "beta::cl-kill-switch"]

    # the two ends: nothing ticked empties honestly, an unknown id is ignored
    assert v["none"] == {"clusters": [], "documents": [], "members": []}
    assert v["ghost"]["members"] == ["alpha"]

    # narrow-then-union: the tally counts alpha's 2 links, not the merged 5
    assert v["soloTallies"] == [["cl-kill-switch", 2, ["alpha"]]]

    # a non-composed snapshot passes through untouched
    assert v["passthrough"] == {"clusters": [{"id": "cl-a"}]}
    # one tail expression serves namespaced ids and the unnamespaced keys
    assert v["tails"] == ["x", "t", "k", ""]


def test_the_open_repo_jump_offers_itself_only_on_composed_views(tmp_path):
    r = _run_node({"snapshot": _composed_snapshot()}, tmp_path)
    assert "open-repo" in r["docActions"]
    assert "open-repo" not in r["plainDocActions"]
    # the merged multi-repo cluster tile offers NO jump (ambiguous target);
    # its drill-in distinguishes the members instead
    assert "open-repo" not in r["clusterActions"]
    assert r["jumps"] == ["alpha", None, None]


def test_wire_the_snapshot_route_serves_a_project_aggregate(tmp_path):
    """Task 1.2: `?repository=<project-id>` composes the derived aggregate;
    an unknown id still 404s."""
    import http.client
    import threading

    from ideation_dashboard import serve as serve_mod

    source = _source(tmp_path)
    httpd = serve_mod.build_server(
        WEB, tmp_path / "baked" / "snapshot.json", tmp_path,
        snapshot_source=source)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address[:2]
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/snapshot.json?repository=pilots&ref=main")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))
        conn.close()
        assert response.status == 200
        assert [m["repository"] for m in
                body["generation"]["composed_from"]] == ["alpha", "beta"]
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/snapshot.json?repository=no-such&ref=main")
        assert conn.getresponse().status == 404
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)
