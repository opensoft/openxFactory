"""THE WHEEL view-model derivation (wheel-model.js; the locked interaction
spec, Track C, Brett-approved 2026-07-16) and the snapshot-side projection it
depends on (fixtures.project_possibles carrying origin/derivation).

Python-side only — no browser automation: the ACTUAL wheel-model.js runs in
node (skipped when node is absent), both against the real fixture snapshot
and against hand snapshots that exercise the edge-class rules the
add-possibles-derivation-lane delta fixes:

  indexed     every snapshot-carried governed relation
  inferred    an UNDISPOSED ai-derived possible's edges (non-`indexed` rule;
              the delta's "Derived possibles are a distinct class until
              disposed"; a deferred verdict stays undisposed; an ACCEPTED
              derived possible is first-class register data -> indexed)
  synthesized honesty-rule demo placeholders, only while the register is
              empty, dash-brass and never confusable with indexed data

Plus the pure AUTOMATIC-ALIGNMENT math — the three connecting-string rules
(Brett 2026-08-21), which supersede the locked prototype's `balancedTarget`
and the 2026-07-23 span-midpoint delta:

  rule 1  a wheel showing NO connecting string centres its FILLED tiles in the
          band (`filledGroupCentre`), instead of keeping whatever position it
          held — which at load was slot 0, half the band blank filler
  rule 2  exactly ONE connected tile rests NEAR the line but not ON it, at the
          named `ALIGN.near` offset (0.8 slot, the prototype's own park value)
  rule 3  with SEVERAL connected tiles one of them sits ON the line — the
          minimal rotation from the wheel's current position (`centredChoice`),
          lowest index breaking a tie; the +0.45 dead-centre nudge that used to
          forbid exactly this is gone

— and the many-linked reorder permutation (Brett 2026-07-24) that seats linked
tiles in consecutive slots instead of stacking them.

The EXPANDED-TILE extension (Brett 2026-07-25) is unit-tested here too: the
`nextExpanded` gesture reducer (a second click on the focused centre tile
expands; Escape / focus change / spin / reorder / paging collapse; at most one
tile expanded) and the per-wheel `WHEEL_ACTIONS` table that decides which verbs
the expanded tile's action row offers — including the READ-ONLY verbs (documents
+ staged `read`, clusters `lens`/`canvas`, active `packet`, archived `landed`),
which carry NO capability gate because none of them writes anything.

The read verbs' PURE halves land here as well, all tested outside the browser
(the fetches themselves are wheel.js's):

  specDeltaPaths / landedFromDeltas   the archived `landed` summary: which of a
                                     change's files are spec deltas, and the
                                     requirement headings under each
                                     `## ADDED|MODIFIED|REMOVED Requirements`
                                     section, grouped by kind (prose traps
                                     included)
  primaryFragmentPath                the staged topic's primary fragment — the
                                     one file the expanded tile summarises and
                                     the `read` verb opens
  fragmentSummary                    that fragment's 3-line summary: frontmatter
                                     stripped, headings skipped, the controlled
                                     `Summary:` header preferred, else the first
                                     meaningful paragraph
  packetGroups                       the active `packet` flyout's grouping:
                                     proposal/design/tasks, then spec deltas by
                                     capability, then the rest
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit  # noqa: F401

from ideation_dashboard.fixtures import project_possibles
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
WHEEL_MODEL_JS = WEB / "views" / "wheel-model.js"
WHEEL_JS = WEB / "views" / "wheel.js"
NODE = shutil.which("node")

_NODE_HARNESS = """
import { buildWheelModel, connectionsOf, SPRING, REEL,
  tileOffset, tileScale, tileOpacity, linkedDrawDistance,
  WHEEL_KEYS } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const snapshot = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const m = buildWheelModel(snapshot);
const wheels = Object.fromEntries(m.wheels.map(w => [w.key, {
  count: w.items.length,
  items: w.items.map(it => ({ id: it.id, label: it.label, sub: it.sub,
                              demo: !!it.demo, derivedPending: !!it.derivedPending })),
  degrees: w.degrees,
}]));
const edges = m.edges.map(e => ({
  from: [e.from[0], m.wheels.find(w => w.key === e.from[0]).items[e.from[1]].id],
  to: [e.to[0], m.wheels.find(w => w.key === e.to[0]).items[e.to[1]].id],
  cls: e.cls,
}));
const focusConns = {};
for (const w of m.wheels) {
  if (w.items.length) focusConns[w.key] = connectionsOf(m, w.key, 0);
}
console.log(JSON.stringify({
  keys: WHEEL_KEYS, wheels, edges, demoMode: m.demoMode, focusConns,
  park: {
    inWindow: linkedDrawDistance(1.5),
    far: linkedDrawDistance(9),
    farNeg: linkedDrawDistance(-9),
    monotone: linkedDrawDistance(6) < linkedDrawDistance(9),
  },
  spring: SPRING,
  reel: REEL,
  layout: {
    offCentreFocused: tileOffset(2, true),
    offCentrePulled: tileOffset(2, false),
    scaleCentreFocused: tileScale(0, true),
    scalePulled: tileScale(0, false),
    opacityCentre: tileOpacity(0),
    opacityFar: tileOpacity(5),
  },
}));
"""


_DRUM_HARNESS = """
import { DRUM, drumCandidate, drumFactor } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({
  bounds: DRUM,
  resolved: cases.map(([, url, stored]) => drumFactor(url, stored)),
  candidates: cases.map(([, url]) => drumCandidate(url)),
}));
"""


_REORDER_HARNESS = """
import { computeReorder } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(cases.map(([n, linked, mid]) => {
  const r = computeReorder(n, linked, mid);
  return { blockLo: r.blockLo, k: r.k,
           sBy: [...r.sBy.entries()], iAt: [...r.iAt.entries()] };
})));
"""


_EXPAND_HARNESS = """
import { nextExpanded, isExpandedTile, actionsFor, WHEEL_ACTIONS, EXPANDED,
  tileScale, actionRowIsStale } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
// each expand case replays its event list through the reducer, recording the
// state after every event (the trail) and the final state
const expand = cases.expand.map(([, current, events]) => {
  let state = current;
  const trail = [];
  for (const ev of events) { state = nextExpanded(state, ev); trail.push(state); }
  return { final: state, trail,
           selfProbe: isExpandedTile(state, 'staged', 1) };
});
const actions = cases.actions.map(([, key, item, env]) => actionsFor(key, item, env));
const stale = {
  identical: actionRowIsStale(['a','b'], ['a','b']),
  retired: actionRowIsStale(['promote-to-staging','research-brief'], ['research-brief']),
  appeared: actionRowIsStale(['research-brief'], ['promote-to-staging','research-brief']),
  reordered: actionRowIsStale(['a','b'], ['b','a']),
  bothEmpty: actionRowIsStale([], []),
  emptied: actionRowIsStale(['demote'], []),
};
console.log(JSON.stringify({
  expand, actions, stale,
  wheelsWithActions: Object.keys(WHEEL_ACTIONS),
  expandedScale: EXPANDED.scale,
  focusScale: tileScale(0, true),
}));
"""


_LANDED_HARNESS = """
import { landedFromDeltas, specDeltaPaths, isSpecDeltaPath,
  LANDED_KINDS } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({
  kinds: LANDED_KINDS,
  landed: cases.landed.map(([, files]) => landedFromDeltas(files)),
  paths: cases.paths.map(([, files]) => ({
    selected: specDeltaPaths(files),
    flags: (files || []).map((p) => isSpecDeltaPath(p)),
  })),
}));
"""


_STAGED_HARNESS = """
import { primaryFragmentPath, fragmentSummary, packetGroups } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({
  paths: cases.paths.map(([, id, files]) => primaryFragmentPath(id, files)),
  summaries: cases.summaries.map(([, text]) => fragmentSummary(text)),
  packets: cases.packets.map(([, files, folder]) => packetGroups(files, folder)),
}));
"""


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())


def _run_wheel_model(snapshot, tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _run_reorder(cases, tmp_path):
    """Run every (n, linkedIdxs, mid) case through the ACTUAL computeReorder,
    returning {case id: {blockLo, k, sBy, iAt}} with the Maps as int dicts."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "reorder.mjs").write_text(_REORDER_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "reorder-cases.json"
    cases_path.write_text(
        json.dumps([[n, linked, mid] for _, n, linked, mid, _ in cases]),
        encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "reorder.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = {}
    for (cid, *_rest), r in zip(cases, json.loads(proc.stdout)):
        out[cid] = {"blockLo": r["blockLo"], "k": r["k"],
                    "sBy": {int(k): int(v) for k, v in r["sBy"]},
                    "iAt": {int(k): int(v) for k, v in r["iAt"]}}
    return out


def _run_drum(cases, tmp_path):
    """Run every (url, stored) case through the ACTUAL drumFactor/drumCandidate,
    returning {"bounds": DRUM, "resolved": {case id: factor},
    "candidates": {case id: clamped-url-candidate-or-None}}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "drum.mjs").write_text(_DRUM_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "drum-cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "drum.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    ids = [cid for cid, *_ in cases]
    return {"bounds": out["bounds"],
            "resolved": dict(zip(ids, out["resolved"])),
            "candidates": dict(zip(ids, out["candidates"]))}


def _run_expand(expand_cases, action_cases, tmp_path):
    """Run the expand gesture + per-wheel action table through the ACTUAL
    nextExpanded / actionsFor, returning
    {"expand": {case id: {final, trail, selfProbe}},
     "actions": {case id: [descriptor, ...]}, plus the table + scale facts}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "expand.mjs").write_text(_EXPAND_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "expand-cases.json"
    cases_path.write_text(json.dumps({"expand": expand_cases,
                                      "actions": action_cases}), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "expand.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return {
        "expand": dict(zip([c[0] for c in expand_cases], out["expand"])),
        "actions": dict(zip([c[0] for c in action_cases], out["actions"])),
        "wheelsWithActions": out["wheelsWithActions"],
        "expandedScale": out["expandedScale"],
        "focusScale": out["focusScale"],
        "stale": out["stale"],
    }


def _run_landed(landed_cases, path_cases, tmp_path):
    """Run the archived wheel's PURE landed parser (landedFromDeltas) and the
    delta-path selector (specDeltaPaths) through the ACTUAL wheel-model.js,
    returning {"kinds": LANDED_KINDS, "landed": {case id: summary},
    "paths": {case id: {selected, flags}}}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "landed.mjs").write_text(_LANDED_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "landed-cases.json"
    cases_path.write_text(json.dumps({"landed": landed_cases, "paths": path_cases}),
                          encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "landed.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return {
        "kinds": out["kinds"],
        "landed": dict(zip([c[0] for c in landed_cases], out["landed"])),
        "paths": dict(zip([c[0] for c in path_cases], out["paths"])),
    }


def _run_staged(path_cases, summary_cases, packet_cases, tmp_path):
    """Run the staged wheel's fragment selection + summary extraction and the
    active wheel's packet grouping through the ACTUAL wheel-model.js, returning
    {"paths": {case id: path}, "summaries": {case id: text},
     "packets": {case id: [group, ...]}}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "staged.mjs").write_text(_STAGED_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "staged-cases.json"
    cases_path.write_text(json.dumps({"paths": path_cases, "summaries": summary_cases,
                                      "packets": packet_cases}), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "staged.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return {
        "paths": dict(zip([c[0] for c in path_cases], out["paths"])),
        "summaries": dict(zip([c[0] for c in summary_cases], out["summaries"])),
        "packets": dict(zip([c[0] for c in packet_cases], out["packets"])),
    }


def _derived(pid="pos-derived-x", *, disposed=None, cluster="cl-a"):
    entry = {
        "id": pid, "title": "Derived " + pid, "claim": "c", "state": "latent",
        "origin": "ai-derived",
        "derivation": {
            "worker_run": {"correlation_id": "DPOSS-1",
                           "worker_profile": "derive-possibles",
                           "prompt_contract_version": "derive-possibles-prompt-v1"},
            "disposition": "pending_review",
        },
        "claiming_clusters": [cluster],
        "supporting_evidence": [{"document": "d.md", "section": "s",
                                 "passage_sha256": "0" * 64}],
    }
    if disposed:
        entry["derivation"]["human_disposition"] = {
            "outcome": disposed, "authority": "gate"}
    return entry


def _hand_snapshot(possibles):
    return {
        "documents": [{"id": "d.md", "status": "brainstorm"}],
        "clusters": [
            {"id": "cl-a", "name": "Alpha", "topics": ["a"],
             "tallies": {"document_links": 1},
             "document_edges": [{"document": "d.md"}],
             "lineage": {"staged_picks": ["st-a"]}},
            {"id": "cl-b", "name": "Beta", "topics": ["b"],
             "tallies": {"document_links": 0}, "document_edges": []},
        ],
        "possibles": possibles,
        "staged_topics": [{"staging_id": "st-a", "files": ["f1", "f2"]}],
        "changes": [
            {"id": "add-x", "status": "active", "files": ["p"],
             "origin_staging_id": "st-a"},
            {"id": "add-y", "status": "archived", "files": []},
        ],
    }


# ---- deck shape --------------------------------------------------------------

def test_six_wheels_in_locked_funnel_order(tmp_path):
    r = _run_wheel_model(_snapshot(), tmp_path)
    assert r["keys"] == ["documents", "clusters", "possibles", "staged",
                         "active", "archived"]
    assert set(r["wheels"]) == set(r["keys"])


def test_spring_constants_are_the_locked_physics(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    assert r["spring"] == {"driven": {"k": 0.020, "damping": 0.84},
                           "pulled": {"k": 0.008, "damping": 0.90}}


# ---- materialized cross-class edges ------------------------------------------

def test_real_relations_are_indexed_edges(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    kinds = {(e["from"][0], e["to"][0]) for e in r["edges"]}
    # the realization data contract's edge families all materialize
    assert ("documents", "clusters") in kinds
    assert ("clusters", "staged") in kinds
    assert ("staged", "active") in kinds
    for e in r["edges"]:
        if not e["from"][1].startswith("demo-") and not e["to"][1].startswith("demo-"):
            assert e["cls"] == "indexed"


def test_undisposed_derived_possible_edges_are_inferred(tmp_path):
    snap = _hand_snapshot([_derived("pos-derived-open"),
                           _derived("pos-derived-deferred", disposed="deferred"),
                           _derived("pos-derived-accepted", disposed="accepted")])
    r = _run_wheel_model(snap, tmp_path)
    cls_by_possible = {e["to"][1]: e["cls"] for e in r["edges"]
                       if e["to"][0] == "possibles"}
    # undisposed (incl. deferred) -> non-`indexed` (the delta's distinct-class
    # rule); an ACCEPTED derived possible is real register data -> indexed
    assert cls_by_possible["pos-derived-open"] == "inferred"
    assert cls_by_possible["pos-derived-deferred"] == "inferred"
    assert cls_by_possible["pos-derived-accepted"] == "indexed"
    subs = {it["id"]: it for it in r["wheels"]["possibles"]["items"]}
    assert subs["pos-derived-open"]["derivedPending"] is True
    assert subs["pos-derived-open"]["sub"] == "pending review"
    assert subs["pos-derived-accepted"]["derivedPending"] is False
    assert r["demoMode"] is False


# ---- the possibles honesty rule ----------------------------------------------

def test_honesty_rule_synthesizes_demo_possibles_only_when_register_empty(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    assert r["demoMode"] is True
    demo = r["wheels"]["possibles"]["items"]
    assert demo and all(it["demo"] and it["sub"] == "demo" for it in demo)
    demo_edges = [e for e in r["edges"] if e["to"][0] == "possibles"]
    assert demo_edges and all(e["cls"] == "synthesized" for e in demo_edges)
    # never a pick edge from a demo possible (a pick is a human act)
    assert not any(e["from"][0] == "possibles" for e in r["edges"])

    real = _run_wheel_model(_hand_snapshot([_derived()]), tmp_path)
    assert real["demoMode"] is False
    assert not any(it["demo"] for it in real["wheels"]["possibles"]["items"])


# ---- degrees + connections -----------------------------------------------------

def test_degrees_count_every_touching_edge(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    wheels = r["wheels"]
    docs = wheels["documents"]
    # d.md touches exactly its doc->cluster edge
    assert docs["degrees"][docs["items"].index(
        next(it for it in docs["items"] if it["id"] == "d.md"))] == 1
    staged = wheels["staged"]
    # st-a: cluster->staged + staged->active + demo edges never touch staged
    assert staged["degrees"][0] == 2


def test_connections_group_linked_indices_per_wheel(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    conns = r["focusConns"]["clusters"]  # cluster cl-a at index 0
    assert "documents" in conns and "staged" in conns


# ---- second-degree connections (Brett 2026-07-25: always-on second-degree,
# dimmed) -------------------------------------------------------------------
#
# secondDegreeOf walks model.adjacency ONE HOP past connectionsOf: focusing a
# tile also surfaces every item one hop beyond its direct links (e.g. a
# document that links several clusters also surfaces those clusters' OTHER
# member documents), excluding the focused item and anything already
# first-degree, deduped, sorted — plus the REAL graph edges (first-degree
# item -> second-degree neighbour, never focus -> second-degree) the renderer
# draws its dimmed connectors from.

_SECOND_DEGREE_HARNESS = """
import { buildWheelModel, connectionsOf, secondDegreeOf } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(cases.map(([, snapshot, wheelKey, itemIndex]) => {
  const m = buildWheelModel(snapshot);
  const idOf = (key, i) => (m.wheels.find((w) => w.key === key)?.items[i]?.id) ?? null;
  const firstRaw = connectionsOf(m, wheelKey, itemIndex);
  const first = {};
  for (const key of Object.keys(firstRaw)) first[key] = firstRaw[key].map((i) => idOf(key, i));
  const raw = secondDegreeOf(m, wheelKey, itemIndex);
  const items = {};
  for (const key of Object.keys(raw)) {
    if (key === 'edges') continue;
    items[key] = raw[key].map((i) => idOf(key, i));
  }
  const edges = raw.edges.map((e) => ({
    from: [e.from[0], idOf(e.from[0], e.from[1])],
    to: [e.to[0], idOf(e.to[0], e.to[1])],
  }));
  return { first, items, edges, raw };
})));
"""


def _run_second_degree(cases, tmp_path):
    """Run every (id, snapshot, wheelKey, itemIndex) case through the ACTUAL
    secondDegreeOf, returning {case id: {first, items, edges, raw}}: `first`/
    `items`/`edges` resolved to ids for readable assertions, `raw` the
    untranslated { wheelKey: [index, ...], edges: [...] } secondDegreeOf
    actually returns (for the sortedness/dedup/determinism checks)."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "seconddeg.mjs").write_text(_SECOND_DEGREE_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "seconddeg-cases.json"
    cases_path.write_text(
        json.dumps([[cid, snap, key, idx] for cid, snap, key, idx in cases]),
        encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "seconddeg.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return dict(zip([c[0] for c in cases], out))


# A hub of clusters sharing documents: d1 is linked by THREE clusters
# (cl-a, cl-b, cl-d); cl-a and cl-d both ALSO link d2 (a convergent second-degree
# path), so d2 must appear only once in the item list despite two real edges
# reaching it. cl-c/d4 is a disconnected decoy (never reachable from d1); d5 is
# fully isolated (no edges at all).
def _hub_snapshot():
    return {
        "documents": [
            {"id": "d1.md", "status": "brainstorm"},
            {"id": "d2.md", "status": "brainstorm"},
            {"id": "d3.md", "status": "brainstorm"},
            {"id": "d4.md", "status": "brainstorm"},
            {"id": "d5.md", "status": "brainstorm"},
        ],
        "clusters": [
            {"id": "cl-a", "name": "Alpha", "topics": ["a"],
             "tallies": {"document_links": 2},
             "document_edges": [{"document": "d1.md"}, {"document": "d2.md"}]},
            {"id": "cl-b", "name": "Beta", "topics": ["b"],
             "tallies": {"document_links": 2},
             "document_edges": [{"document": "d1.md"}, {"document": "d3.md"}]},
            {"id": "cl-c", "name": "Gamma", "topics": ["c"],
             "tallies": {"document_links": 1},
             "document_edges": [{"document": "d4.md"}]},
            {"id": "cl-d", "name": "Delta", "topics": ["d"],
             "tallies": {"document_links": 2},
             "document_edges": [{"document": "d1.md"}, {"document": "d2.md"}]},
        ],
        # a real (unrelated) possible keeps demoMode off, so no synthesized
        # cluster->possible edges muddy the hub's adjacency
        "possibles": [{"id": "pos-unrelated", "title": "Unrelated", "state": "latent",
                       "claim": "c", "claiming_clusters": []}],
        "staged_topics": [],
        "changes": [],
    }


# A chain across wheel classes: a cluster's first degree is a possible it
# claims; that possible's own pick reaches a STAGED topic — the second-degree
# hop the possibles wheel sits between.
def _chain_snapshot():
    return {
        "documents": [],
        "clusters": [{"id": "cl-x", "name": "X", "topics": ["x"],
                      "tallies": {"document_links": 0}, "document_edges": []}],
        "possibles": [{"id": "p1", "title": "P1", "state": "latent", "claim": "c",
                       "claiming_clusters": ["cl-x"], "pick": {"staging_id": "st-y"}}],
        "staged_topics": [{"staging_id": "st-y", "files": ["f1"]}],
        "changes": [],
    }


SECOND_DEGREE_CASES = [
    ("hub-doc-focus", _hub_snapshot(), "documents", 0),
    # d4: reachable only through cl-c, whose sole document edge IS d4 itself —
    # no other document to surface, so second degree is empty despite a
    # nonempty first degree
    ("hub-isolated-cluster-neighbour", _hub_snapshot(), "documents", 3),
    # d5: no edges at all — first AND second degree both empty
    ("hub-fully-isolated", _hub_snapshot(), "documents", 4),
    ("chain-cluster-to-staged", _chain_snapshot(), "clusters", 0),
    # cl-b in the plain hand snapshot carries no edges of its own
    ("empty-snapshot", _hand_snapshot([]), "clusters", 1),
]


def test_second_degree_hub_shows_sibling_documents_via_shared_clusters(tmp_path):
    r = _run_second_degree(SECOND_DEGREE_CASES, tmp_path)["hub-doc-focus"]
    # first degree: d1's own three clusters
    assert set(r["first"]["clusters"]) == {"cl-a", "cl-b", "cl-d"}
    # second degree: the OTHER documents those clusters link — d2 (shared by
    # cl-a AND cl-d) and d3 (cl-b) — deduped to one entry each
    assert sorted(r["items"]["documents"]) == ["d2.md", "d3.md"]
    # the focused document and every first-degree cluster are excluded from
    # the second-degree result entirely
    assert "d1.md" not in r["items"]["documents"]
    assert "clusters" not in r["items"] or not r["items"]["clusters"]
    # d4 (cl-c's document — a cluster never reached from d1) never leaks in
    assert "d4.md" not in r["items"]["documents"]


def test_second_degree_edges_anchor_at_the_first_degree_item_not_the_focus(tmp_path):
    r = _run_second_degree(SECOND_DEGREE_CASES, tmp_path)["hub-doc-focus"]
    assert all(e["from"][0] == "clusters" and e["to"][0] == "documents"
               for e in r["edges"])
    assert all(e["from"][1] != "d1.md" for e in r["edges"])  # never the focus
    edge_pairs = {(e["from"][1], e["to"][1]) for e in r["edges"]}
    assert ("cl-a", "d2.md") in edge_pairs
    assert ("cl-d", "d2.md") in edge_pairs
    assert ("cl-b", "d3.md") in edge_pairs


def test_second_degree_dedupes_items_but_keeps_every_real_edge(tmp_path):
    """d2 is reached through TWO distinct real edges (cl-a and cl-d both link
    it) — the item list dedupes to one entry, but both edges still draw."""
    r = _run_second_degree(SECOND_DEGREE_CASES, tmp_path)["hub-doc-focus"]
    assert r["items"]["documents"].count("d2.md") == 1
    to_d2 = [e for e in r["edges"] if e["to"] == ["documents", "d2.md"]]
    assert len(to_d2) == 2
    assert {e["from"][1] for e in to_d2} == {"cl-a", "cl-d"}


def test_second_degree_crosses_wheel_classes_cluster_to_staged_via_possibles(tmp_path):
    r = _run_second_degree(SECOND_DEGREE_CASES, tmp_path)["chain-cluster-to-staged"]
    assert r["first"] == {"possibles": ["p1"]}
    assert r["items"] == {"staged": ["st-y"]}
    assert r["edges"] == [{"from": ["possibles", "p1"], "to": ["staged", "st-y"]}]


def test_second_degree_is_empty_when_nothing_reaches_beyond_first_degree(tmp_path):
    r = _run_second_degree(SECOND_DEGREE_CASES, tmp_path)
    for cid in ("hub-isolated-cluster-neighbour", "hub-fully-isolated", "empty-snapshot"):
        assert r[cid]["items"] == {}, cid
        assert r[cid]["edges"] == [], cid


def test_second_degree_output_is_sorted_deduped_and_deterministic(tmp_path):
    runs = [_run_second_degree(SECOND_DEGREE_CASES, tmp_path) for _ in range(2)]
    assert runs[0] == runs[1]  # same input -> byte-identical output
    for cid in ("hub-doc-focus", "chain-cluster-to-staged", "hub-fully-isolated"):
        raw = runs[0][cid]["raw"]
        for key, idxs in raw.items():
            if key == "edges":
                continue
            assert idxs == sorted(idxs), (cid, key)
            assert len(idxs) == len(set(idxs)), (cid, key)  # no duplicate indices


# ---- gathering: first + second degree fold into one reel window (Brett
# 2026-07-25) ----------------------------------------------------------------
#
# gatherOf folds each wheel's SECOND-degree tiles into the wheel-gathering the
# reorder + elastic alignment already ran on first-degree tiles, so first- and
# second-degree tiles come to rest near each other in the visible window. Per
# OTHER wheel it returns first / second / gather (the union the reorder packs) /
# align (first-degree when the wheel has any — priority, they sit on the line —
# else the second-degree set, so a wheel reached ONLY at second degree still
# spins in). Deterministic, sorted, deduped — the same node harness as above.

_GATHER_HARNESS = """
import { buildWheelModel, gatherOf } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(cases.map(([, snapshot, wheelKey, itemIndex]) => {
  const m = buildWheelModel(snapshot);
  const idOf = (key, i) => (m.wheels.find((w) => w.key === key)?.items[i]?.id) ?? null;
  const raw = gatherOf(m, wheelKey, itemIndex);
  const resolved = {};
  for (const key of Object.keys(raw)) {
    const g = raw[key];
    resolved[key] = {
      first: g.first.map((i) => idOf(key, i)),
      second: g.second.map((i) => idOf(key, i)),
      gather: g.gather.map((i) => idOf(key, i)),
      align: g.align.map((i) => idOf(key, i)),
    };
  }
  return { resolved, raw };
})));
"""


def _run_gather(cases, tmp_path):
    """Run every (id, snapshot, wheelKey, itemIndex) case through the ACTUAL
    gatherOf, returning {case id: {resolved, raw}}: `resolved` maps each wheel
    key to {first, second, gather, align} resolved to ids, `raw` keeps the index
    lists for the sortedness/dedup/determinism checks."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "gather.mjs").write_text(_GATHER_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "gather-cases.json"
    cases_path.write_text(
        json.dumps([[cid, snap, key, idx] for cid, snap, key, idx in cases]),
        encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "gather.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return dict(zip([c[0] for c in cases], out))


# A cluster whose STAGED wheel is reached at BOTH degrees: cl-x links st-1
# directly (lineage staged_picks) AND links possible p1, whose own pick reaches
# st-2 — so the staged wheel's gather carries st-1 first-degree and st-2
# second-degree, and its `align` must keep st-1 (first-degree priority) alone.
def _gather_priority_snapshot():
    return {
        "documents": [],
        "clusters": [{"id": "cl-x", "name": "X", "topics": ["x"],
                      "tallies": {"document_links": 0}, "document_edges": [],
                      "lineage": {"staged_picks": ["st-1"]}}],
        "possibles": [{"id": "p1", "title": "P1", "state": "latent", "claim": "c",
                       "claiming_clusters": ["cl-x"], "pick": {"staging_id": "st-2"}}],
        "staged_topics": [{"staging_id": "st-1", "files": ["f1"]},
                          {"staging_id": "st-2", "files": ["f2"]}],
        "changes": [],
    }


GATHER_CASES = [
    ("hub-doc", _hub_snapshot(), "documents", 0),
    ("chain-cluster", _chain_snapshot(), "clusters", 0),
    ("priority-both-degrees", _gather_priority_snapshot(), "clusters", 0),
    # d5 has no edges at all — nothing to gather in any wheel
    ("isolated", _hub_snapshot(), "documents", 4),
]


def test_gather_folds_second_degree_tiles_into_the_reel(tmp_path):
    r = _run_gather(GATHER_CASES, tmp_path)["hub-doc"]["resolved"]
    # the two wheels the hub focus reaches: its own clusters (first degree) and
    # the sibling documents one hop beyond (second degree)
    assert set(r) == {"clusters", "documents"}
    # first-degree clusters gather as first degree, nothing second
    assert set(r["clusters"]["first"]) == {"cl-a", "cl-b", "cl-d"}
    assert r["clusters"]["second"] == []
    assert set(r["clusters"]["gather"]) == {"cl-a", "cl-b", "cl-d"}
    # the documents wheel is reached ONLY at second degree — d2/d3 now GATHER
    # (before this ruling the docs wheel had no gather target and stayed put)
    assert r["documents"]["first"] == []
    assert sorted(r["documents"]["second"]) == ["d2.md", "d3.md"]
    assert sorted(r["documents"]["gather"]) == ["d2.md", "d3.md"]


def test_gather_gives_first_degree_priority_on_the_line(tmp_path):
    """A wheel reached at BOTH degrees packs first + second into `gather`, but
    POSITIONS on the first-degree tiles alone (`align`) so they rest on the
    focus line and second-degree tiles gather around them."""
    r = _run_gather(GATHER_CASES, tmp_path)["priority-both-degrees"]["resolved"]
    staged = r["staged"]
    assert staged["first"] == ["st-1"]           # direct lineage pick
    assert staged["second"] == ["st-2"]          # via the claimed possible
    assert staged["gather"] == ["st-1", "st-2"]  # both packed, index-sorted
    assert staged["align"] == ["st-1"]           # ...but only first sits on the line
    # a wheel with only first-degree links aligns on them (no fallback needed)
    assert r["possibles"]["first"] == ["p1"]
    assert r["possibles"]["align"] == ["p1"]


def test_gather_aligns_on_second_degree_when_no_first_degree(tmp_path):
    """The docs wheel off a hub focus, and the staged wheel off a cluster->
    possible chain, are reached only at second degree — `align` falls back to
    the second-degree set so the wheel still spins its tiles into view."""
    out = _run_gather(GATHER_CASES, tmp_path)
    docs = out["hub-doc"]["resolved"]["documents"]
    assert docs["align"] == docs["second"] == sorted(docs["second"])
    chain = out["chain-cluster"]["resolved"]
    assert chain["possibles"]["align"] == ["p1"]        # first degree
    assert chain["staged"]["first"] == []
    assert chain["staged"]["align"] == ["st-y"]          # second-degree fallback


def test_gather_is_empty_when_nothing_links(tmp_path):
    assert _run_gather(GATHER_CASES, tmp_path)["isolated"]["resolved"] == {}


def test_gather_output_is_sorted_deduped_and_deterministic(tmp_path):
    runs = [_run_gather(GATHER_CASES, tmp_path) for _ in range(2)]
    assert runs[0] == runs[1]  # same input -> byte-identical output
    for cid in ("hub-doc", "chain-cluster", "priority-both-degrees"):
        for key, g in runs[0][cid]["raw"].items():
            for field in ("first", "second", "gather", "align"):
                idxs = g[field]
                assert idxs == sorted(idxs), (cid, key, field)
                assert len(idxs) == len(set(idxs)), (cid, key, field)


# ---- the three AUTOMATIC-ALIGNMENT rules (Brett 2026-08-21) ---------------------
#
# `alignTarget(linkedIndices, {position, itemCount})` decides where a wheel comes
# to rest when something ELSE is focused, keyed on how many of its own tiles the
# focused context is threading to (`gatherOf(...).align`, mapped into slot
# space). A human's own click still centres any tile dead on the line; that is
# wheel.js's `setFocus` and these rules never see it.
#
#   rule 1  NO connecting string     -> `filledGroupCentre(itemCount)`: the real
#                                       tiles centre in the band, position-
#                                       independent, no tile favoured
#   rule 2  exactly ONE string       -> that tile parks `ALIGN.near` (0.8 slot)
#                                       off the line — below it, or above when it
#                                       sits too near the top edge
#   rule 3  SEVERAL strings          -> `centredChoice(indices, position)`: one
#                                       connected tile lands exactly ON the line,
#                                       the one needing the smallest rotation,
#                                       lowest index breaking a tie
#
# Each case is (id, linkedIndices, position, itemCount).

_ALIGN_HARNESS = """
import { alignTarget, filledGroupCentre, centredChoice, ALIGN }
  from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({
  near: ALIGN.near,
  results: cases.map(([, linked, position, itemCount]) => ({
    target: alignTarget(linked, { position, itemCount }),
    centre: filledGroupCentre(itemCount),
    choice: centredChoice(linked, position),
  })),
}));
"""


def _run_align(cases, tmp_path):
    """Run every (id, linkedIndices, position, itemCount) case through the
    ACTUAL alignTarget, returning (ALIGN.near, {case id: result})."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "align.mjs").write_text(_ALIGN_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "align-cases.json"
    cases_path.write_text(json.dumps([list(c) for c in cases]), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "align.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return out["near"], dict(zip([c[0] for c in cases], out["results"]))


ALIGN_CASES = [
    # rule 1 — no connecting string: the filled group centres, wherever the
    # wheel happens to be and whatever its parity
    ("none-odd", [], 0, 7),
    ("none-even", [], 0, 8),
    ("none-single-tile", [], 0, 1),
    ("none-empty-wheel", [], 0, 0),
    ("none-from-the-bottom", [], 6, 7),
    # rule 2 — one string: near the line, never on it
    ("one-mid", [4], 0, 10),
    ("one-top-edge", [0], 0, 10),
    ("one-bottom-edge", [9], 0, 10),
    ("one-on-a-single-tile-wheel", [0], 0, 1),
    # rule 3 — several strings: one connected tile takes the line
    ("many-nearest-below", [2, 4, 8], 7.0, 10),
    ("many-nearest-above", [2, 4, 8], 2.1, 10),
    ("many-exact-tie", [2, 6], 4.0, 10),
    # the three cases the SUPERSEDED prototype math answered differently
    ("was-balanced-pair", [2, 4], 0, 10),
    ("was-dead-centre-nudge", [3, 4, 5], 0, 10),
    ("was-span-midpoint", [0, 1, 9], 0, 10),
]


def test_rule1_a_wheel_with_no_string_centres_its_filled_tiles(tmp_path):
    """No thread reaches this wheel, so nothing is aligned ON: the real tiles —
    slots 0..count-1, everything outside them blank filler — centre in the band,
    biased toward no tile. Position-independent by construction."""
    _, r = _run_align(ALIGN_CASES, tmp_path)
    assert r["none-odd"]["target"] == pytest.approx(3.0)    # 7 tiles: 0..6
    assert r["none-even"]["target"] == pytest.approx(3.5)   # 8 tiles: between 3/4
    assert r["none-single-tile"]["target"] == pytest.approx(0.0)
    # the same answer from anywhere on the drum — a wheel that was spun to the
    # bottom still returns to the centred group
    assert r["none-from-the-bottom"]["target"] == r["none-odd"]["target"]
    # ...and each equals `filledGroupCentre`, the rule's own named helper
    for cid in ("none-odd", "none-even", "none-single-tile", "none-from-the-bottom"):
        assert r[cid]["target"] == pytest.approx(r[cid]["centre"]), cid
    # an EMPTY wheel has nothing to centre: null, and the deck keeps its position
    assert r["none-empty-wheel"]["target"] is None
    assert r["none-empty-wheel"]["centre"] is None


def test_rule2_a_single_string_rests_near_the_line_not_on_it(tmp_path):
    """One connected tile parks at the NAMED `ALIGN.near` offset — near the
    centreline, deliberately off it, because a tile exactly on the line
    collapses its thread into a flat connector."""
    near, r = _run_align(ALIGN_CASES, tmp_path)
    assert near == pytest.approx(0.8)   # the locked prototype's own park value
    assert r["one-mid"]["target"] == pytest.approx(4 - near)      # below the line
    assert r["one-top-edge"]["target"] == pytest.approx(near)     # ...above at the top
    assert r["one-bottom-edge"]["target"] == pytest.approx(9 - near)
    # NEAR, NOT ON: the connected tile never lands on the line, not even when it
    # is the wheel's only tile (the band clamp widens by `near` for exactly this)
    for cid, i in (("one-mid", 4), ("one-top-edge", 0), ("one-bottom-edge", 9),
                   ("one-on-a-single-tile-wheel", 0)):
        assert r[cid]["target"] != pytest.approx(i), cid
        assert abs(r[cid]["target"] - i) == pytest.approx(near), cid


def test_rule3_several_strings_put_one_connected_tile_on_the_line(tmp_path):
    """With several connected tiles the wheel MAY seat one dead-centre, and
    does: exactly one connected tile, chosen by MINIMAL ROTATION from the
    wheel's current position, with the lowest index breaking a tie."""
    _, r = _run_align(ALIGN_CASES, tmp_path)
    # the target IS an index in the linked set — a tile on the line, not between
    assert r["many-nearest-below"]["target"] == pytest.approx(8)   # from 7.0
    assert r["many-nearest-above"]["target"] == pytest.approx(2)   # from 2.1
    # equidistant (|2-4| == |6-4|) -> the lower index, deterministically
    assert r["many-exact-tie"]["target"] == pytest.approx(2)
    # `centredChoice` is the named decision and the target is exactly it
    for cid in ("many-nearest-below", "many-nearest-above", "many-exact-tie"):
        assert r[cid]["target"] == pytest.approx(r[cid]["choice"]), cid


def test_the_superseded_prototype_alignment_math_is_gone(tmp_path):
    """The three cases that pinned `balancedTarget`: a group no longer rests on
    its span midpoint, and the +0.45 dead-centre nudge — whose entire purpose
    was to keep a tile OFF the line — is removed rather than scoped, because
    rule 3 is its inverse."""
    _, r = _run_align(ALIGN_CASES, tmp_path)
    assert r["was-balanced-pair"]["target"] == pytest.approx(2)      # was 3.0
    assert r["was-dead-centre-nudge"]["target"] == pytest.approx(3)  # was 3.55
    assert r["was-span-midpoint"]["target"] == pytest.approx(0)      # was 4.5
    # every one of them now seats a CONNECTED tile on the line
    for cid, linked in (("was-balanced-pair", [2, 4]),
                        ("was-dead-centre-nudge", [3, 4, 5]),
                        ("was-span-midpoint", [0, 1, 9])):
        assert r[cid]["target"] in [pytest.approx(i) for i in linked], cid


def test_the_deck_routes_every_automatic_alignment_through_the_rules():
    """wheel.js's half: the three rules are decided in ONE place, and the things
    the ruling explicitly preserves are still preserved.

    A second alignment path is how the rules drift apart, so `alignFor` — the
    only mapping from item space into slot space — must be the only caller of
    the pure `alignTarget`, and every automatic resting position (the live pull,
    the post-reorder re-seat, the pre-focus rest) must come through it."""
    src = WHEEL_JS.read_text(encoding="utf-8")
    assert src.count("alignTarget(") == 1, \
        "alignTarget must have exactly ONE call site in the deck: alignFor"
    align_for = src.split("function alignFor(", 1)[1].split("\n  }", 1)[0]
    assert "alignTarget(alignIdxs.map((i) => slotOf(w.key, i))" in align_for
    assert "position: from, itemCount: w.items.length" in align_for

    # the LIVE pull: an empty align set is rule 1, not a skipped wheel, so the
    # old clamp-to-item-range (which fought rule 2's off-line park) is gone too
    retarget = src.split("function retarget(", 1)[1].split("\n  }", 1)[0]
    assert "alignFor(w, gather[w.key]?.align || [], pos[w.key])" in retarget
    assert "clamp(t," not in retarget, \
        "alignTarget owns the band clamp; a second one re-centres rule 2's park"

    # the post-reorder re-seat is automatic alignment too: it must not simply
    # rest the wheel on the raw block centre
    reorder = src.split("function applyReorder(", 1)[1].split("\n  }", 1)[0]
    assert "alignFor(w, align, mid)" in reorder
    assert "target[key] = t;" in reorder

    # rule 1 before any focus exists: the deck opens with filled groups centred
    assert "filledGroupCentre(w.items.length) ?? 0" in src

    # PRESERVED. A human's own click still centres the clicked tile dead on the
    # line — these rules govern AUTOMATIC alignment, never user intent.
    set_focus = src.split("function setFocus(", 1)[1].split("\n  }", 1)[0]
    assert "target[key] = slotOf(key, i);" in set_focus
    # PRESERVED. reduced motion still snaps, and the locked springs still drive.
    assert "if (reduceMotion) {" in src
    assert "focus?.key === w.key ? SPRING.driven : SPRING.pulled" in src


def test_linked_tiles_park_inside_the_edge_fade_band(tmp_path):
    # linked tiles beyond the near band park INSIDE the edge-fade zone
    # (<= ~2.5 steps), leaving the outer rows to fade for the cylinder read
    park = _run_wheel_model(_hand_snapshot([]), tmp_path)["park"]
    assert park["inWindow"] == pytest.approx(1.5)        # verbatim inside ~1.8
    assert 1.8 < park["far"] < 2.6                       # parked short of the fade band
    assert park["farNeg"] == pytest.approx(-park["far"]) # symmetric
    assert park["monotone"] is True


def test_reel_geometry_matches_the_locked_prototype(tmp_path):
    r = _run_wheel_model(_hand_snapshot([]), tmp_path)
    assert r["reel"] == {"spacing": 58, "bulge": 15, "visible": 6}
    layout = r["layout"]
    import math
    assert layout["offCentreFocused"] == pytest.approx(2 * 58 + math.tanh(2) * 15)
    assert layout["offCentrePulled"] == pytest.approx(2 * 58)  # bulge is focus-only
    assert layout["scaleCentreFocused"] == pytest.approx(1.35)  # .92 + .43
    assert layout["scalePulled"] == pytest.approx(0.95)         # never magnifies
    assert layout["opacityCentre"] == 1
    assert layout["opacityFar"] == pytest.approx(0.22)          # floor


# ---- the drum-radius knob ("wheel diameter" setting) ----------------------------
#
# (id, urlRaw, storedRaw) -> the factor wheel.js draws with. The knob's whole
# contract: an explicit `?drum=` URL param WINS (the compare-by-URL tuning tool),
# else the saved setting, else the default 0.5; a parseable POSITIVE number is
# clamped into [0.3, 2.0] rather than discarded (a stale tuning URL still renders
# a legible wheel); anything else — absent, non-numeric, zero, negative — is "no
# opinion" and falls through to the next source.
DRUM_CASES = [
    ("url-wins-over-stored", "0.5", "1.5"),
    ("url-absent-uses-stored", None, "1.5"),
    ("url-garbage-uses-stored", "abc", "1.5"),
    ("url-empty-uses-stored", "", "1.5"),
    ("url-zero-uses-stored", "0", "1.5"),
    ("url-negative-uses-stored", "-1", "1.25"),
    ("both-absent-default", None, None),
    ("stored-garbage-default", None, "{}"),
    ("stored-negative-default", None, "-3"),
    ("url-over-max-clamps", "9", None),
    ("url-under-min-clamps", "0.05", None),
    ("stored-over-max-clamps", None, "500"),
    ("stored-under-min-clamps", None, "0.01"),
    ("url-at-min", "0.3", None),
    ("url-at-max", "2.0", None),
    ("numeric-not-string", 1.4, None),
]


def test_drum_bounds_are_the_settings_knob(tmp_path):
    """The slider's range/step/default are wheel geometry, not UI trivia."""
    r = _run_drum(DRUM_CASES, tmp_path)
    assert r["bounds"] == {"min": 0.3, "max": 2.0, "step": 0.05, "default": 0.5}


def test_drum_url_param_wins_over_the_saved_setting(tmp_path):
    r = _run_drum(DRUM_CASES, tmp_path)["resolved"]
    assert r["url-wins-over-stored"] == pytest.approx(0.5)   # not the stored 1.5
    assert r["url-absent-uses-stored"] == pytest.approx(1.5)


def test_drum_invalid_inputs_fall_back_through_precedence(tmp_path):
    out = _run_drum(DRUM_CASES, tmp_path)
    r = out["resolved"]
    # non-numeric / empty / non-positive URL values are "no opinion": stored wins
    assert r["url-garbage-uses-stored"] == pytest.approx(1.5)
    assert r["url-empty-uses-stored"] == pytest.approx(1.5)
    assert r["url-zero-uses-stored"] == pytest.approx(1.5)
    assert r["url-negative-uses-stored"] == pytest.approx(1.25)
    # ...and an unusable stored value (corrupt JSON left in localStorage,
    # negative) lands on the default rather than a broken cylinder
    assert r["both-absent-default"] == pytest.approx(0.5)
    assert r["stored-garbage-default"] == pytest.approx(0.5)
    assert r["stored-negative-default"] == pytest.approx(0.5)
    # the single-candidate view of the same rule
    assert out["candidates"]["url-garbage-uses-stored"] is None
    assert out["candidates"]["url-zero-uses-stored"] is None
    assert out["candidates"]["numeric-not-string"] == pytest.approx(1.4)


def test_drum_clamps_at_both_bounds(tmp_path):
    r = _run_drum(DRUM_CASES, tmp_path)["resolved"]
    assert r["url-over-max-clamps"] == pytest.approx(2.0)
    assert r["url-under-min-clamps"] == pytest.approx(0.3)
    assert r["stored-over-max-clamps"] == pytest.approx(2.0)
    assert r["stored-under-min-clamps"] == pytest.approx(0.3)
    # the bounds themselves survive untouched
    assert r["url-at-min"] == pytest.approx(0.3)
    assert r["url-at-max"] == pytest.approx(2.0)


# ---- the many-linked reorder permutation ---------------------------------------
#
# (id, n, linkedIdxs, mid, expected blockLo). blockLo is the locked formula
# clamp(round(mid) - floor((k-1)/2), 0, max(0, n - k)) — note k == 0 leaves an
# EMPTY block whose blockLo is inert (floor(-1/2) == -1 shifts it up one), so
# the permutation is the identity regardless of where blockLo lands.
REORDER_CASES = [
    ("mid-block", 10, [2, 5, 8], 5.0, 4),
    ("clamped-low", 10, [3, 4, 5], 0.0, 0),
    ("clamped-high", 10, [1, 2, 3, 4], 9.0, 6),
    ("k-near-n-low", 5, [0, 1, 2, 3], 0.0, 0),
    ("k-near-n-high", 5, [0, 1, 2, 3], 4.0, 1),
    ("whole-wheel", 4, [0, 1, 2, 3], 2.0, 0),
    ("single-edge-low", 8, [0], 0.0, 0),
    ("single-edge-high", 8, [7], 7.0, 7),
    ("unsorted-input", 6, [4, 1], 2.0, 2),
    ("fractional-mid", 10, [4, 6], 3.4, 3),
    ("half-mid-rounds-up", 10, [1, 8], 2.5, 3),
    ("empty-linked", 5, [], 2.0, 3),
    ("out-of-range", 5, [-1, 2, 7], 2.0, 2),
    ("one-item-wheel", 1, [0], 0.0, 0),
    ("empty-wheel", 0, [], 0.0, 0),
]

# The linked items each case actually seats (out-of-range indices ignored).
def _linked_in_range(n, linked):
    return sorted(i for i in linked if 0 <= i < n)


# JS `Math.round` breaks ties UPWARD; Python's round() is banker's rounding, so
# re-deriving the locked formula here needs the JS rule (mid 2.5 -> 3).
def _js_round(x):
    return math.floor(x + 0.5)


def test_reorder_permutation_is_a_bijection(tmp_path):
    results = _run_reorder(REORDER_CASES, tmp_path)
    for cid, n, linked, _mid, _lo in REORDER_CASES:
        r = results[cid]
        slots = set(range(n))
        assert set(r["sBy"]) == slots, cid          # every item mapped
        assert set(r["sBy"].values()) == slots, cid  # onto every slot, once
        assert set(r["iAt"]) == slots, cid
        assert r["iAt"] == {s: i for i, s in r["sBy"].items()}, cid  # inverses
        assert r["k"] == len(_linked_in_range(n, linked)), cid


def test_reorder_seats_linked_items_contiguously_at_the_clamped_mid(tmp_path):
    results = _run_reorder(REORDER_CASES, tmp_path)
    for cid, n, linked, mid, expected_lo in REORDER_CASES:
        r = results[cid]
        assert r["blockLo"] == expected_lo, cid
        L = _linked_in_range(n, linked)
        # sorted-index order across consecutive slots blockLo..blockLo+k-1
        assert [r["sBy"][i] for i in L] == \
            list(range(r["blockLo"], r["blockLo"] + r["k"])), cid
        if not L:
            continue
        # the block stays inside the reel and hugs round(mid) unless an edge
        # clamp pulled it back
        assert 0 <= r["blockLo"] <= n - r["k"], cid
        wanted = _js_round(mid) - (r["k"] - 1) // 2
        assert r["blockLo"] == max(0, min(wanted, n - r["k"])), cid


def test_reorder_preserves_relative_order_of_unlinked_items(tmp_path):
    results = _run_reorder(REORDER_CASES, tmp_path)
    for cid, n, linked, _mid, _lo in REORDER_CASES:
        r = results[cid]
        L = set(_linked_in_range(n, linked))
        rest = [i for i in range(n) if i not in L]
        got = [r["sBy"][i] for i in rest]
        assert got == sorted(got), cid           # i < j => slot(i) < slot(j)
        # ...and they fill exactly the slots the linked block left over
        assert got == [s for s in range(n)
                       if not r["blockLo"] <= s < r["blockLo"] + r["k"]], cid


def test_reorder_identity_when_nothing_seats_a_block(tmp_path):
    """No linked items (and out-of-range-only input) => untouched wheel."""
    results = _run_reorder(REORDER_CASES, tmp_path)
    for cid in ("empty-linked", "empty-wheel"):
        r = results[cid]
        assert r["k"] == 0
        assert r["sBy"] == {i: i for i in r["sBy"]}
    # a single in-range link at its own index is likewise the identity
    ident = results["out-of-range"]
    assert ident["k"] == 1 and ident["sBy"] == {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}


def test_reorder_whole_wheel_linked_is_the_identity(tmp_path):
    """k == n leaves no leftover slots: the block spans the reel from 0."""
    results = _run_reorder(REORDER_CASES, tmp_path)
    r = results["whole-wheel"]
    assert r["k"] == 4 and r["blockLo"] == 0
    assert r["sBy"] == {0: 0, 1: 1, 2: 2, 3: 3}


# ---- the expanded tile: gesture reducer ----------------------------------------
#
# (id, starting state, events). The gesture EXTENDS the locked click gesture:
# clicking an unfocused tile only focuses; clicking the tile that is already
# focused AND centred expands it in place; clicking it again collapses. Escape,
# focus changes, spins of that wheel, the reorder choreography, paging, and
# teardown all arrive as {"type": "collapse"}.
TILE_1 = {"key": "staged", "i": 1}
EXPAND_CASES = [
    ("first-click-focuses-only", None,
     [{"type": "tile", "key": "staged", "i": 1, "centred": False}]),
    ("second-click-expands", None,
     [{"type": "tile", "key": "staged", "i": 1, "centred": False},
      {"type": "tile", "key": "staged", "i": 1, "centred": True}]),
    ("third-click-collapses", TILE_1,
     [{"type": "tile", "key": "staged", "i": 1, "centred": True}]),
    ("escape-collapses", TILE_1, [{"type": "collapse"}]),
    ("other-tile-same-wheel-collapses", TILE_1,
     [{"type": "tile", "key": "staged", "i": 4, "centred": False}]),
    ("other-wheel-centred-tile-replaces", TILE_1,
     [{"type": "tile", "key": "possibles", "i": 0, "centred": True}]),
    ("spin-that-wheel-collapses", TILE_1, [{"type": "spin", "key": "staged"}]),
    ("spin-another-wheel-keeps", TILE_1, [{"type": "spin", "key": "documents"}]),
    ("unknown-event-keeps", TILE_1, [{"type": "resize"}]),
    ("collapse-is-idempotent", None, [{"type": "collapse"}, {"type": "collapse"}]),
    ("reopen-after-collapse", TILE_1,
     [{"type": "collapse"},
      {"type": "tile", "key": "staged", "i": 1, "centred": True}]),
]


def test_expand_needs_a_second_click_on_the_already_centred_tile(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["expand"]
    # the locked gesture is untouched: an unfocused tile only focuses
    assert r["first-click-focuses-only"]["final"] is None
    # ...and the second click on that now-focused centre tile expands it
    assert r["second-click-expands"]["trail"] == [None, TILE_1]
    assert r["second-click-expands"]["selfProbe"] is True
    assert r["reopen-after-collapse"]["final"] == TILE_1


def test_expanded_tile_collapses_on_every_locked_trigger(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["expand"]
    for cid in ("third-click-collapses", "escape-collapses",
                "other-tile-same-wheel-collapses", "spin-that-wheel-collapses"):
        assert r[cid]["final"] is None, cid
    # a spin of a DIFFERENT wheel (the pull, not this tile's reel) leaves it open
    assert r["spin-another-wheel-keeps"]["final"] == TILE_1
    # an event the reducer does not know never silently closes a human's tile
    assert r["unknown-event-keeps"]["final"] == TILE_1
    assert r["collapse-is-idempotent"]["trail"] == [None, None]


def test_only_one_tile_is_ever_expanded(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["expand"]
    # focus TRANSFERS across wheels; the new wheel's centred tile takes over
    # rather than adding a second open tile
    assert r["other-wheel-centred-tile-replaces"]["final"] == {"key": "possibles", "i": 0}
    for case in r.values():
        for state in case["trail"]:
            assert state is None or set(state) == {"key", "i"}


def test_expanded_scale_exceeds_the_focus_magnification(tmp_path):
    """Expanding must always READ as growth, so it outgrows the 1.35x focus."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)
    assert r["focusScale"] == pytest.approx(1.35)
    assert r["expandedScale"] > r["focusScale"]


# ---- the expanded tile: per-wheel action table ----------------------------------
#
# (id, wheel key, item, env). The table is the extension point Brett grows: one
# row per verb, gated by a PURE predicate over the item and the session env
# (gate capability live, already commissioned this session, applied verdict).
ACTION_CASES = [
    ("staged-gated", "staged", {"id": "st-a"}, {"gate": True, "commissioned": False}),
    ("staged-ungated", "staged", {"id": "st-a"}, {"gate": False, "commissioned": False}),
    ("staged-commissioned", "staged", {"id": "st-a"}, {"gate": True, "commissioned": True}),
    ("staged-no-env", "staged", {"id": "st-a"}, None),
    ("staged-no-item", "staged", None, {"gate": True}),
    ("possibles-gated", "possibles", {"id": "pos-a"}, {"gate": True}),
    ("documents-gated", "documents", {"id": "d.md"}, {"gate": True}),
    ("clusters-gated", "clusters", {"id": "cl-a"}, {"gate": True}),
    ("active-gated", "active", {"id": "add-x"}, {"gate": True}),
    ("archived-gated", "archived", {"id": "add-y"}, {"gate": True}),
    # the read-only verbs on the DEPLOYED image's env: no gate capability, no
    # actor, nothing commissioned — they must still be offered.
    ("documents-ungated", "documents", {"id": "d.md"}, {"gate": False}),
    ("clusters-ungated", "clusters", {"id": "cl-a"}, {"gate": False}),
    ("archived-ungated", "archived", {"id": "add-y"}, {"gate": False}),
    ("documents-no-env", "documents", {"id": "d.md"}, None),
    ("clusters-no-item", "clusters", None, {"gate": False}),
    ("active-ungated", "active", {"id": "add-x"}, {"gate": False}),
    ("possibles-ungated", "possibles", {"id": "pos-a"}, {"gate": False}),
    # the SET-level NotebookLM verb: its OWN capability flag (`notebook`), on
    # exactly the three set-bearing wheels. The gate capability is orthogonal —
    # a notebook-capable session offers it whether or not the gate is live.
    ("clusters-notebook", "clusters", {"id": "cl-a"}, {"gate": False, "notebook": True}),
    ("staged-notebook", "staged", {"id": "st-a"},
     {"gate": True, "commissioned": False, "notebook": True}),
    ("staged-notebook-ungated", "staged", {"id": "st-a"}, {"gate": False, "notebook": True}),
    ("staged-notebook-commissioned", "staged", {"id": "st-a"},
     {"gate": True, "commissioned": True, "notebook": True}),
    ("active-notebook", "active", {"id": "add-x"}, {"gate": False, "notebook": True}),
    # ...and the wheels the action deliberately excludes (a single document is
    # not a set; realized changes are out of scope) stay unchanged.
    ("documents-notebook", "documents", {"id": "d.md"}, {"gate": False, "notebook": True}),
    ("archived-notebook", "archived", {"id": "add-y"}, {"gate": False, "notebook": True}),
    ("possibles-notebook", "possibles", {"id": "pos-a"}, {"gate": False, "notebook": True}),
    ("active-notebook-false", "active", {"id": "add-x"}, {"notebook": False}),
    ("active-no-item-notebook", "active", None, {"notebook": True}),
    # ---- 011 add-wheel-action-verbs: the four action-row verbs ----------
    # possibles promotability is computed from facts the snapshot ALREADY
    # projects onto a tile (state / derivedPending / demo) — no new field.
    ("w-promotable", "possibles",
     {"id": "pos-a", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-a", "state": "latent"}}, {"gate": True}),
    ("w-derived-pending", "possibles",
     {"id": "pos-b", "demo": False, "derivedPending": True,
      "ref": {"id": "pos-b", "state": "latent"}}, {"gate": True}),
    ("w-derived-deferred", "possibles",
     {"id": "pos-c", "demo": False, "derivedPending": True,
      "ref": {"id": "pos-c", "state": "latent"}}, {"gate": True}),
    ("w-rejected", "possibles",
     {"id": "pos-d", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-d", "state": "rejected"}}, {"gate": True}),
    ("w-superseded", "possibles",
     {"id": "pos-e", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-e", "state": "superseded"}}, {"gate": True}),
    ("w-picked", "possibles",
     {"id": "pos-f", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-f", "state": "picked"}}, {"gate": True}),
    ("w-demo", "possibles",
     {"id": "demo-cl-a", "demo": True, "derivedPending": False,
      "ref": {"id": "demo-cl-a", "state": "latent"}}, {"gate": True}),
    ("w-cluster", "clusters", {"id": "cl-a"}, {"gate": True}),
    ("w-active", "active", {"id": "add-x"}, {"gate": True}),
    ("w-archived", "archived", {"id": "add-y"}, {"gate": True}),
    ("w-possibles-gateoff", "possibles",
     {"id": "pos-a", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-a", "state": "latent"}}, {"gate": False}),
    ("w-cluster-gateoff", "clusters", {"id": "cl-a"}, {"gate": False}),
    ("w-active-gateoff", "active", {"id": "add-x"}, {"gate": False}),
    # per-(verb, target) session retirement: commissioning ONE possibles verb
    # must not retire the other (FR-027/FR-033).
    ("w-brief-commissioned", "possibles",
     {"id": "pos-a", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-a", "state": "latent"}},
     {"gate": True, "commissioned": {"research-brief": True}}),
    ("w-promote-commissioned", "possibles",
     {"id": "pos-a", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-a", "state": "latent"}},
     {"gate": True, "commissioned": {"promote-to-staging": True}}),
    ("w-demote-recorded", "active", {"id": "add-x"},
     {"gate": True, "commissioned": {"demote": True}}),
    ("w-cluster-commissioned", "clusters", {"id": "cl-a"},
     {"gate": True, "commissioned": {"derive-possibles": True}}),
    # the legacy tile-wide boolean still means "everything on this tile"
    # CAPTURED LIVE (2026-08-02) from the served wheel model in a real browser,
    # not authored here: `buildWheelModel(<served snapshot>)` -> possibles item.
    # The register state lives under `ref`; there is NO top-level `state`. An
    # authored flat fixture hid a defect in which `promote-to-staging` never
    # rendered on the real dashboard at all.
    ("w-real-projection-accepted", "possibles",
     {"id": "pos-ok", "label": "Promotable", "sub": "latent",
      "demo": False, "derivedPending": False,
      "ref": {"id": "pos-ok", "title": "Promotable", "claim": "c",
              "state": "latent", "origin": "ai-derived",
              "claiming_clusters": ["cl-a"],
              "derivation": {"worker_run": {"correlation_id": "D-1",
                                            "worker_profile": "w",
                                            "prompt_contract_version": "v1"},
                             "disposition": "pending_review",
                             "human_disposition": {"outcome": "accepted",
                                                   "authority": "brett"}}}},
     {"gate": True}),
    ("w-real-deferred", "possibles",
     {"id": "pos-def", "label": "Deferred", "sub": "pending review",
      "demo": False, "derivedPending": True,
      "ref": {"id": "pos-def", "title": "Deferred", "claim": "c",
              "state": "latent", "origin": "ai-derived",
              "derivation": {"worker_run": {"correlation_id": "D-3",
                                            "worker_profile": "w",
                                            "prompt_contract_version": "v1"},
                             "disposition": "pending_review",
                             "human_disposition": {"outcome": "deferred",
                                                   "authority": "brett"}}}},
     {"gate": True}),
    ("w-real-projection-pending", "possibles",
     {"id": "pos-pending", "label": "Awaiting verdict", "sub": "pending review",
      "demo": False, "derivedPending": True,
      "ref": {"id": "pos-pending", "title": "Awaiting verdict", "claim": "c",
              "state": "latent", "origin": "ai-derived",
              "claiming_clusters": ["cl-a"],
              "derivation": {"worker_run": {"correlation_id": "D-2",
                                            "worker_profile": "w",
                                            "prompt_contract_version": "v1"},
                             "disposition": "pending_review"}}},
     {"gate": True}),
    ("w-legacy-boolean", "possibles",
     {"id": "pos-a", "demo": False, "derivedPending": False,
      "ref": {"id": "pos-a", "state": "latent"}}, {"gate": True, "commissioned": True}),
]


def test_action_table_offers_draft_proposal_only_on_gated_staged_tiles(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert [a["id"] for a in r["staged-gated"]] == ["read", "propose", "workbench"]
    assert r["staged-gated"][1]["label"] == "▶ draft proposal"
    # the capability gate is the same fail-closed rule as the dispose tray — the
    # read-only verbs are all that is left without it...
    assert [a["id"] for a in r["staged-ungated"]] == ["read", "workbench"]
    assert [a["id"] for a in r["staged-no-env"]] == ["read", "workbench"]
    # ...and the WRITE verb retires once this session commissioned the topic
    assert [a["id"] for a in r["staged-commissioned"]] == ["read", "workbench"]
    assert r["staged-no-item"] == []


def test_action_table_rows_sit_in_funnel_order(tmp_path):
    """The table reads in the deck's own order. Every wheel now carries a row —
    the possibles wheel's FIRST table verb is the read-only workbench
    (add-staging-workbench; its dispose verbs stay in the badge-rail tray)."""
    out = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)
    assert out["wheelsWithActions"] == ["documents", "clusters", "possibles",
                                        "staged", "active", "archived"]
    # every wheel offers at least one read-only verb, capability or not
    for cid in ("documents-ungated", "clusters-ungated", "possibles-ungated",
                "staged-ungated", "active-ungated", "active-gated",
                "active-notebook-false", "archived-ungated"):
        assert out["actions"][cid], cid


def test_read_only_verbs_need_no_gate_capability(tmp_path):
    """read / lens / canvas / packet / landed / workbench only READ — they must
    appear on the deployed static image too, where `actions.gate` is false and
    no actor is resolved."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert [a["id"] for a in r["documents-ungated"]] == ["read"]
    assert [a["id"] for a in r["clusters-ungated"]] == ["lens", "canvas", "workbench"]
    assert [a["id"] for a in r["possibles-ungated"]] == ["workbench"]
    assert [a["id"] for a in r["staged-ungated"]] == ["read", "workbench"]
    assert [a["id"] for a in r["active-ungated"]] == ["packet"]
    assert [a["id"] for a in r["archived-ungated"]] == ["landed"]
    # ...and the gated env offers exactly the same read-only verbs, plus the
    # staged wheel's one WRITE verb
    assert [a["id"] for a in r["documents-gated"]] == ["read"]
    assert [a["id"] for a in r["clusters-gated"]] == \
        ["lens", "canvas", "derive-possibles", "workbench"]
    # a possibles tile carrying NO projected state is not promotable and not
    # known-undisposed, so neither commission verb is offered — the view fails
    # closed on missing facts exactly as the engine does (011 FR-010a).
    assert [a["id"] for a in r["possibles-gated"]] == ["workbench"]
    assert [a["id"] for a in r["staged-gated"]] == ["read", "propose", "workbench"]
    assert [a["id"] for a in r["active-gated"]] == ["packet", "demote"]
    assert [a["id"] for a in r["archived-gated"]] == ["landed"]
    # every descriptor carries the label the mounter renders
    assert r["documents-ungated"][0]["label"] == "▤ read"
    assert [a["label"] for a in r["clusters-ungated"]] == \
        ["◎ lens", "▦ canvas", "▣ open workbench"]
    assert r["archived-ungated"][0]["label"] == "✓ landed"
    assert r["active-ungated"][0]["label"] == "▩ packet"
    # documents and staged share ONE read verb — same id, same label, same mounter
    assert r["staged-ungated"][0] == r["documents-ungated"][0]
    # a missing env is still legal (the reducer never assumes a session)...
    assert [a["id"] for a in r["documents-no-env"]] == ["read"]
    # ...but no item means no verbs at all
    assert r["clusters-no-item"] == []


def test_workbench_verb_on_exactly_the_three_topic_bearing_wheels(tmp_path):
    """The `open workbench` row (add-staging-workbench D6) sits on clusters,
    possibles, and staged — the topic-bearing wheels — with NO visible
    predicate: gate capability on AND off, notebook capability or not,
    commissioned or not, the read-only verb is always offered. documents /
    active / archived tiles are not topic-bearing and gain nothing."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    offered = (
        "clusters-gated", "clusters-ungated", "clusters-notebook",
        "possibles-gated", "possibles-ungated", "possibles-notebook",
        "staged-gated", "staged-ungated", "staged-no-env",
        "staged-commissioned", "staged-notebook", "staged-notebook-ungated",
        "staged-notebook-commissioned",
    )
    for cid in offered:
        assert "workbench" in [a["id"] for a in r[cid]], cid
    excluded = (
        "documents-gated", "documents-ungated", "documents-no-env",
        "documents-notebook", "active-gated", "active-ungated",
        "active-notebook", "archived-gated", "archived-ungated",
        "archived-notebook",
    )
    for cid in excluded:
        assert "workbench" not in [a["id"] for a in r[cid]], cid
    # ONE shared row: same id, same label on all three wheels (one table row,
    # one mounter — the extension-point discipline)
    labels = {next(a["label"] for a in r[cid] if a["id"] == "workbench")
              for cid in ("clusters-gated", "possibles-gated", "staged-gated")}
    assert labels == {"▣ open workbench"}
    # ...and no item still means no verbs at all
    assert r["staged-no-item"] == []
    assert r["clusters-no-item"] == []


def test_notebook_verb_only_on_the_three_set_bearing_wheels(tmp_path):
    """The SET-level NotebookLM action surfaces the EXISTING backend route, so it
    appears on exactly the wheels notebook_action.py's TILE_KINDS resolves —
    clusters (cluster) · staged (staged) · active (proposal). documents (a single
    doc, not a set) and archived (realized material) are excluded by design."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert [a["id"] for a in r["clusters-notebook"]] == \
        ["lens", "canvas", "notebook", "workbench"]
    assert [a["id"] for a in r["staged-notebook"]] == \
        ["read", "propose", "notebook", "workbench"]
    assert [a["id"] for a in r["active-notebook"]] == ["packet", "notebook"]
    # excluded wheels keep exactly the verbs they already had
    assert [a["id"] for a in r["documents-notebook"]] == ["read"]
    assert [a["id"] for a in r["archived-notebook"]] == ["landed"]
    assert [a["id"] for a in r["possibles-notebook"]] == ["workbench"]
    # one shared label, so the three rows are the same verb
    labels = {next(a["label"] for a in r[cid] if a["id"] == "notebook")
              for cid in ("clusters-notebook", "staged-notebook", "active-notebook")}
    assert labels == {"◇ notebook"}
    # ...and no item still means no verbs, capability or not
    assert r["active-no-item-notebook"] == []


def test_notebook_verb_needs_its_own_capability_not_the_gate(tmp_path):
    """`env.notebook` (the /capabilities notebook flag) is the ONLY switch: absent
    it, no wheel offers the verb; present it, the verb is offered whatever the
    gate capability says, and it never retires with the propose commission."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    # capability absent -> no notebook row anywhere, whatever the gate says (the
    # read-only verbs and the gated propose verb are unaffected)
    for cid in ("staged-gated", "clusters-gated", "active-gated",
                "active-notebook-false"):
        assert "notebook" not in [a["id"] for a in r[cid]], cid
    # capability present, gate absent -> the read verbs plus the notebook one
    assert [a["id"] for a in r["staged-notebook-ungated"]] == \
        ["read", "notebook", "workbench"]
    # ...and it OUTLIVES the propose verb's session retirement
    assert [a["id"] for a in r["staged-notebook-commissioned"]] == \
        ["read", "notebook", "workbench"]


# ---- the staged tile's health chrome (pure; add-staging-workbench D10) ---------
#
# (id, health object). The FOCUSED tile face carries the compact tri-state
# indicator (healthIndicator) and the EXPANDED tile the full block
# (healthBlock), both VERBATIM from the snapshot's `health` — the helpers must
# return null for a pre-growth snapshot (no health object) or an unknown
# status, so the renderer never computes or guesses a state client-side.
_HEALTH_READY = {
    "standing_open_items": 0, "doc_score_min": 0.7123, "doc_score_mean": 0.8,
    "blockers": [], "status": "ready",
}
_HEALTH_DEVELOPING = {
    "standing_open_items": 3, "doc_score_min": 0.41, "doc_score_mean": 0.62,
    "blockers": [
        {"kind": "standing_open_items",
         "document": "ideation/staging/t/a.md", "count": 2},
        {"kind": "standing_open_items",
         "document": "ideation/staging/t/b.md", "count": 1},
        {"kind": "below_ready_threshold",
         "document": "ideation/staging/t/a.md", "score": 0.41, "threshold": 0.6},
    ],
    "status": "developing",
}
_HEALTH_STUB = {
    "standing_open_items": 0, "doc_score_min": 0.0, "doc_score_mean": 0.0,
    "blockers": [], "status": "stub",
}

HEALTH_CASES = [
    ("ready", _HEALTH_READY),
    ("developing", _HEALTH_DEVELOPING),
    ("stub", _HEALTH_STUB),
    ("one-item", {**_HEALTH_READY, "standing_open_items": 1,
                  "status": "developing",
                  "blockers": [{"kind": "standing_open_items",
                                "document": "ideation/staging/t/a.md",
                                "count": 1}]}),
    # a pre-growth snapshot's staged topic has NO health object at all
    ("absent", None),
    # ...and a status outside the contract's tri-state is never guessed at
    ("unknown-status", {**_HEALTH_READY, "status": "blocked"}),
    ("empty-object", {}),
    # a blocker kind the contract does not define is still SHOWN, named
    ("unknown-blocker", {**_HEALTH_DEVELOPING,
                         "blockers": [{"kind": "mystery",
                                       "document": "ideation/staging/t/c.md"}]}),
]

_HEALTH_HARNESS = """
import { healthIndicator, healthBlock, HEALTH_STATUSES } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({
  statuses: HEALTH_STATUSES,
  indicators: cases.map(([, health]) => healthIndicator(health)),
  blocks: cases.map(([, health]) => healthBlock(health)),
}));
"""


def _run_health(cases, tmp_path):
    """Run every (id, health) case through the ACTUAL healthIndicator /
    healthBlock, returning {"statuses": [...], "indicators": {id: ...},
    "blocks": {id: ...}}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    (tmp_path / "health.mjs").write_text(_HEALTH_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "health-cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "health.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    ids = [cid for cid, *_ in cases]
    return {"statuses": out["statuses"],
            "indicators": dict(zip(ids, out["indicators"])),
            "blocks": dict(zip(ids, out["blocks"]))}


def test_health_indicator_is_the_snapshot_tri_state(tmp_path):
    out = _run_health(HEALTH_CASES, tmp_path)
    assert out["statuses"] == ["ready", "developing", "stub"]
    ind = out["indicators"]
    assert ind["ready"]["status"] == "ready"
    assert ind["developing"]["status"] == "developing"
    assert ind["stub"]["status"] == "stub"
    # shape-coded glyphs, one per status, distinct at drum scale
    glyphs = {ind[cid]["glyph"] for cid in ("ready", "developing", "stub")}
    assert len(glyphs) == 3
    # the hover title carries the standing count VERBATIM (0 stays 0, 1 is
    # singular — the snapshot's own number, never recomputed)
    assert "0 standing open items" in ind["ready"]["title"]
    assert "3 standing open items" in ind["developing"]["title"]
    assert "1 standing open item" in ind["one-item"]["title"]


def test_health_chrome_absent_on_a_pre_growth_snapshot(tmp_path):
    """No health object -> NO indicator and NO block (the renderer must never
    compute health itself); an unknown status is likewise never guessed at."""
    out = _run_health(HEALTH_CASES, tmp_path)
    for cid in ("absent", "unknown-status", "empty-object"):
        assert out["indicators"][cid] is None, cid
        assert out["blocks"][cid] is None, cid


def test_health_block_renders_the_snapshot_verbatim(tmp_path):
    out = _run_health(HEALTH_CASES, tmp_path)
    block = out["blocks"]["developing"]
    assert block["status"] == "developing"
    # min/mean and standing count are the snapshot's own numbers
    assert block["lines"] == [
        "standing open items: 3",
        "doc score min 0.41 · mean 0.62",
    ]
    # every blocker appears, naming its document and its count or its score
    # against the threshold — the same facts the gate's refusal cites
    assert block["blockers"] == [
        "ideation/staging/t/a.md — 2 standing open items",
        "ideation/staging/t/b.md — 1 standing open item",
        "ideation/staging/t/a.md — score 0.41 < threshold 0.6",
    ]
    # a ready topic renders an empty blockers list, never an invented one
    assert out["blocks"]["ready"]["blockers"] == []
    # the fixed-precision score survives verbatim (never re-rounded)
    assert "0.7123" in out["blocks"]["ready"]["lines"][1]
    # an unknown blocker kind is shown (named), never silently dropped
    assert out["blocks"]["unknown-blocker"]["blockers"] == [
        "ideation/staging/t/c.md — blocked (mystery)",
    ]


# ---- the archived wheel's "landed" summary (pure parser) -----------------------
#
# The snapshot carries a realized change's FILE LIST; what LANDED is the
# requirement headings inside its spec deltas. wheel.js fetches those files
# through the read-only /source pass-through and hands the text here.
_ARCHIVE = "openspec/changes/archive/2026-07-09-add-doc-health/"
DELTA_HEALTH = _ARCHIVE + "specs/doc-health/spec.md"
DELTA_LIFECYCLE = _ARCHIVE + "specs/document-lifecycle/spec.md"

DELTA_HEALTH_TEXT = """## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twelve check families.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run

## ADDED Requirements

### Requirement: Finding severity and regression handling
Every finding SHALL carry one severity.

#### Scenario: A regression opens
- **WHEN** a new error finding appears
- **THEN** the run MUST open a regression

### Requirement: Contested resolutions need a citation
A contested finding SHALL NOT be auto-fixed.
"""

# The prose traps: a Requirements heading inside a FENCED example, a requirement
# heading under a non-delta section, and delta wording quoted in prose.
DELTA_LIFECYCLE_TEXT = """# add-doc-health spec delta

## Why
The prose below quotes ### Requirement: Quoted In Prose mid-sentence.

## REMOVED Requirements

### Requirement: Free-form status values
Free-form `Status:` values SHALL no longer be accepted.

## Notes

### Requirement: Not a delta requirement at all
This sits under a plain section, not a delta section.

```markdown
## ADDED Requirements

### Requirement: Fenced example only
```
"""

LANDED_CASES = [
    ("one-delta", [{"path": DELTA_HEALTH, "text": DELTA_HEALTH_TEXT}]),
    ("two-deltas", [{"path": DELTA_HEALTH, "text": DELTA_HEALTH_TEXT},
                    {"path": DELTA_LIFECYCLE, "text": DELTA_LIFECYCLE_TEXT}]),
    ("prose-traps", [{"path": DELTA_LIFECYCLE, "text": DELTA_LIFECYCLE_TEXT}]),
    ("non-delta-files", [{"path": _ARCHIVE + "proposal.md", "text": DELTA_HEALTH_TEXT},
                         {"path": _ARCHIVE + "tasks.md",
                          "text": "### Requirement: from a task list\n"},
                         {"path": _ARCHIVE + "supporting-docs/notes.md",
                          "text": "## ADDED Requirements\n\n### Requirement: support note\n"}]),
    ("empty-list", []),
    ("null-input", None),
    ("missing-text", [{"path": DELTA_HEALTH}]),
    ("non-string-text", [{"path": DELTA_HEALTH, "text": 42}]),
    ("no-headings", [{"path": DELTA_HEALTH, "text": "just prose, no headings\n"}]),
    ("blank-title", [{"path": DELTA_HEALTH,
                      "text": "## ADDED Requirements\n\n### Requirement:\n"}]),
    ("crlf", [{"path": DELTA_HEALTH,
               "text": "## ADDED Requirements\r\n\r\n### Requirement: CRLF survives\r\n"}]),
]

PATH_CASES = [
    ("change-folder", [_ARCHIVE + "proposal.md", _ARCHIVE + "design.md",
                       _ARCHIVE + "tasks.md", DELTA_HEALTH, DELTA_LIFECYCLE,
                       _ARCHIVE + "supporting-docs.tar.gz"]),
    ("no-deltas", [_ARCHIVE + "proposal.md"]),
    ("null-files", None),
    ("specs-dir-but-not-spec-md", [_ARCHIVE + "specs/doc-health/notes.md"]),
]


def test_landed_groups_requirement_titles_by_delta_kind(tmp_path):
    r = _run_landed(LANDED_CASES, PATH_CASES, tmp_path)
    assert r["kinds"] == ["ADDED", "MODIFIED", "REMOVED"]
    one = r["landed"]["one-delta"]
    assert [q["title"] for q in one["groups"]["MODIFIED"]] == \
        ["Deterministic check families"]
    assert [q["title"] for q in one["groups"]["ADDED"]] == \
        ["Finding severity and regression handling",
         "Contested resolutions need a citation"]
    assert one["groups"]["REMOVED"] == []
    assert one["total"] == 3
    assert one["files"] == [DELTA_HEALTH]
    # each requirement carries the capability its delta targets (from the path)
    assert {q["capability"] for q in one["groups"]["ADDED"]} == {"doc-health"}
    two = r["landed"]["two-deltas"]
    assert two["total"] == 4
    assert [q["capability"] for q in two["groups"]["REMOVED"]] == ["document-lifecycle"]
    assert two["files"] == [DELTA_HEALTH, DELTA_LIFECYCLE]


def test_landed_ignores_prose_fences_and_non_delta_sections(tmp_path):
    """A requirement heading only LANDS under a declared delta section — never
    from a fenced example, a plain section, or prose that quotes the syntax."""
    r = _run_landed(LANDED_CASES, PATH_CASES, tmp_path)["landed"]["prose-traps"]
    assert [q["title"] for q in r["groups"]["REMOVED"]] == ["Free-form status values"]
    assert r["total"] == 1, r["groups"]
    titles = [q["title"] for group in r["groups"].values() for q in group]
    assert "Fenced example only" not in titles
    assert "Not a delta requirement at all" not in titles
    assert "Quoted In Prose mid-sentence." not in titles


def test_landed_ignores_files_that_are_not_spec_deltas(tmp_path):
    """proposal/design/tasks/supporting docs are never read as deltas, even when
    their text happens to carry the delta syntax."""
    r = _run_landed(LANDED_CASES, PATH_CASES, tmp_path)["landed"]["non-delta-files"]
    assert r == {"files": [], "groups": {"ADDED": [], "MODIFIED": [], "REMOVED": []},
                 "total": 0}


def test_landed_handles_empty_and_malformed_input(tmp_path):
    r = _run_landed(LANDED_CASES, PATH_CASES, tmp_path)["landed"]
    empty = {"files": [], "groups": {"ADDED": [], "MODIFIED": [], "REMOVED": []},
             "total": 0}
    # nothing to read, no files, an unreadable body, a titleless heading: an
    # honest empty summary, never a throw and never an invented requirement
    assert r["empty-list"] == empty
    assert r["null-input"] == empty
    assert r["missing-text"] == empty
    assert r["non-string-text"] == empty
    assert r["no-headings"] == {**empty, "files": [DELTA_HEALTH]}
    assert r["blank-title"] == {**empty, "files": [DELTA_HEALTH]}
    # a CRLF checkout parses identically to LF
    assert [q["title"] for q in r["crlf"]["groups"]["ADDED"]] == ["CRLF survives"]


def test_spec_delta_paths_select_only_change_folder_deltas(tmp_path):
    """The landed verb fetches EXACTLY the `specs/<capability>/spec.md` files —
    the same shape the explorer groups as "spec deltas"."""
    r = _run_landed(LANDED_CASES, PATH_CASES, tmp_path)["paths"]
    assert r["change-folder"]["selected"] == [DELTA_HEALTH, DELTA_LIFECYCLE]
    assert r["change-folder"]["flags"] == [False, False, False, True, True, False]
    assert r["no-deltas"]["selected"] == []
    assert r["null-files"]["selected"] == []
    assert r["specs-dir-but-not-spec-md"]["selected"] == []


def test_landed_parses_a_real_archived_change_delta(tmp_path):
    """End-to-end against the REAL corpus: the first archived change in the
    pinned openxFactory checkout whose deltas the parser can read."""
    archive = REPO_ROOT.parent.parent / "openxFactory" / "openspec" / "changes" / "archive"
    deltas = sorted(archive.glob("*/specs/*/spec.md"))
    if not deltas:
        pytest.skip("no archived spec deltas in the sibling openxFactory checkout")
    files = [{"path": str(p.relative_to(archive.parents[2])),
              "text": p.read_text(encoding="utf-8")} for p in deltas[:4]]
    r = _run_landed([("real", files)], PATH_CASES, tmp_path)["landed"]["real"]
    assert r["total"] > 0, "the real archive must yield landed requirements"
    for kind, group in r["groups"].items():
        for req in group:
            assert req["title"].strip() == req["title"] and req["title"]
            assert req["capability"], (kind, req)


# ---- the staged wheel: primary fragment + 3-line summary (pure) ----------------
#
# A staged tile carries the topic's FILE LIST, so both the expanded tile's summary
# and its `read` verb first have to pick ONE file. Selection is path-only:
# `<staging_id>.md`, else the shallowest markdown file (a topic-root fragment
# beats an `openspec/` proposal draft).
_STAGING = "ideation/staging/client-layer-tuning/"
FRAGMENT_CASES = [
    ("named-fragment", "client-layer-tuning",
     [_STAGING + "openspec/proposal.md", _STAGING + "client-layer-tuning.md",
      _STAGING + "notes.md"]),
    # no file carries the topic's own name: the shallowest markdown wins
    ("shallowest-wins", "github-administration-plane",
     ["ideation/staging/github-administration-plane/openspec/tasks.md",
      "ideation/staging/github-administration-plane/multi-app-identity.md"]),
    ("single-file", "worker-host-app", ["ideation/staging/worker-host-app/x.md"]),
    # a path-shaped id still matches by basename
    ("path-shaped-id", "ideation/staging/client-layer-tuning",
     [_STAGING + "openspec/proposal.md", _STAGING + "client-layer-tuning.md"]),
    ("case-insensitive", "Client-Layer-Tuning", [_STAGING + "client-layer-tuning.md"]),
    ("no-markdown", "topic", ["ideation/staging/topic/manifest.yaml"]),
    ("empty-files", "topic", []),
    ("null-files", "topic", None),
    ("no-id", None, [_STAGING + "openspec/proposal.md"]),
]

# The real staging-fragment shape: an h1, then the document-lifecycle controlled
# header block whose `Summary:` field wraps over several lines.
FRAGMENT_TEXT = """# Staged: Client Layer Tuning (scaffold roles, schemas)

Status: staged
Kind: architecture
Summary: Make the Client layer tunable: extend the neutral scaffold with the
house-team `roles/` and ship the client content schemas.
Topics: client-hermes, company-policy
Staging ID: openxFactory:staging:client-layer-tuning

## Claims (decided 2026-07-22)

1. **Shape settled.** `roles/` joins the client shape.
"""

SUMMARY_CASES = [
    ("controlled-header", FRAGMENT_TEXT),
    ("frontmatter", "---\nstatus: staged\nkind: architecture\n---\n\n"
                    "# Title\n\nThe body's first paragraph is the summary.\n"),
    ("headings-only", "# Title\n\n## Section\n\n### Deeper\n"),
    ("first-paragraph", "# Title\n\nA plain fragment with no header block at all,\n"
                        "wrapped over two source lines.\n\n## Claims\n\nlater prose\n"),
    # a header block with no Summary field is METADATA: skipped, not summarised
    ("header-without-summary", "# Title\n\nStatus: staged\nKind: architecture\n\n"
                               "The paragraph after the metadata block.\n"),
    ("fenced-first", "# Title\n\n```yaml\nsummary: not prose\n```\n\nThe real prose.\n"),
    ("setext-heading", "Title Underlined\n================\n\nThe prose below it.\n"),
    ("emphasis-unwrapped", "# T\n\nA **bold** claim about `code` and *stress*.\n"),
    ("crlf", "---\r\nstatus: staged\r\n---\r\n\r\n# Title\r\n\r\n"
             "Summary: A CRLF checkout reads identically.\r\n"),
    ("long", "# T\n\n" + ("word " * 200) + "\n"),
    ("blank", "   \n\n\t\n"),
    ("empty", ""),
    ("null", None),
    ("non-string", 42),
    ("unterminated-frontmatter", "---\nstatus: staged\n\n# Title\n\nprose\n"),
]


def test_primary_fragment_prefers_the_topic_named_markdown_file(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["paths"]
    assert r["named-fragment"] == _STAGING + "client-layer-tuning.md"
    assert r["path-shaped-id"] == _STAGING + "client-layer-tuning.md"
    assert r["case-insensitive"] == _STAGING + "client-layer-tuning.md"
    # no name match: the topic-root fragment beats the openspec/ draft
    assert r["shallowest-wins"] == \
        "ideation/staging/github-administration-plane/multi-app-identity.md"
    assert r["single-file"] == "ideation/staging/worker-host-app/x.md"
    assert r["no-id"] == _STAGING + "openspec/proposal.md"
    # nothing to read is "" — the tile then shows no summary and a DISABLED verb
    assert r["no-markdown"] == ""
    assert r["empty-files"] == ""
    assert r["null-files"] == ""


def test_fragment_summary_prefers_the_controlled_summary_header(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["summaries"]
    # the wrapped Summary: field, joined into one line, backticks unwrapped
    assert r["controlled-header"] == (
        "Make the Client layer tunable: extend the neutral scaffold with the "
        "house-team roles/ and ship the client content schemas.")
    # the h1 (which restates the tile's own title) never leaks in, and neither
    # does a following field or section
    assert "Staged:" not in r["controlled-header"]
    assert "Topics:" not in r["controlled-header"]
    assert "Claims" not in r["controlled-header"]


def test_fragment_summary_strips_frontmatter_and_skips_headings(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["summaries"]
    assert r["frontmatter"] == "The body's first paragraph is the summary."
    assert r["crlf"] == "A CRLF checkout reads identically."
    assert r["setext-heading"] == "The prose below it."
    # a heading-only fragment has nothing to say, and says nothing
    assert r["headings-only"] == ""


def test_fragment_summary_falls_back_to_the_first_meaningful_paragraph(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["summaries"]
    assert r["first-paragraph"] == \
        "A plain fragment with no header block at all, wrapped over two source lines."
    # a header block WITHOUT a Summary field is metadata: skipped, never rendered
    assert r["header-without-summary"] == "The paragraph after the metadata block."
    # fenced code is not prose
    assert r["fenced-first"] == "The real prose."
    assert r["emphasis-unwrapped"] == "A bold claim about code and stress."


def test_fragment_summary_clamps_and_survives_malformed_input(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["summaries"]
    # the tile clamps to three DISPLAY lines in CSS; the extraction clamps the
    # string so a whole fragment is never carried into the DOM
    assert len(r["long"]) <= 241 and r["long"].endswith("…")
    assert r["long"].startswith("word word")
    # blank / absent / non-string / truncated input: "" — never a throw
    for cid in ("blank", "empty", "null", "non-string", "unterminated-frontmatter"):
        assert r[cid] == "", cid


# ---- the active wheel: proposal-packet grouping (pure) -------------------------

_CHANGE = "openspec/changes/add-cross-factory-ideation-routing"
PACKET_CASES = [
    ("full-packet", [_CHANGE + "/.openspec.yaml", _CHANGE + "/tasks.md",
                     _CHANGE + "/specs/doc-health/spec.md", _CHANGE + "/proposal.md",
                     _CHANGE + "/specs/ideation-routing/spec.md", _CHANGE + "/design.md",
                     _CHANGE + "/supporting-docs/manifest.yaml"], _CHANGE),
    ("no-folder-recorded", [_CHANGE + "/proposal.md",
                            _CHANGE + "/supporting-docs/manifest.yaml"], None),
    ("proposal-only", [_CHANGE + "/proposal.md"], _CHANGE),
    ("deltas-only", [_CHANGE + "/specs/doc-health/spec.md"], _CHANGE),
    ("empty-files", [], _CHANGE),
    ("null-files", None, _CHANGE),
]


def test_packet_groups_read_in_review_order(tmp_path):
    """proposal -> design -> tasks first (whatever order the snapshot lists them
    in), then the spec deltas labelled by capability, then everything else."""
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["packets"]
    groups = r["full-packet"]
    assert [g["label"] for g in groups] == ["packet", "spec deltas", "other files"]
    assert [f["name"] for f in groups[0]["files"]] == \
        ["proposal.md", "design.md", "tasks.md"]
    # every spec delta is named `spec.md`, so the CAPABILITY is the useful label
    assert [f["name"] for f in groups[1]["files"]] == ["doc-health", "ideation-routing"]
    assert [f["name"] for f in groups[2]["files"]] == \
        [".openspec.yaml", "supporting-docs/manifest.yaml"]
    # the path each button opens is the full repo-relative one, never the label
    assert groups[0]["files"][0]["path"] == _CHANGE + "/proposal.md"
    assert groups[1]["files"][0]["path"] == _CHANGE + "/specs/doc-health/spec.md"


def test_packet_groups_drop_empty_groups_and_degrade_quietly(tmp_path):
    r = _run_staged(FRAGMENT_CASES, SUMMARY_CASES, PACKET_CASES, tmp_path)["packets"]
    assert [g["label"] for g in r["proposal-only"]] == ["packet"]
    assert [g["label"] for g in r["deltas-only"]] == ["spec deltas"]
    # no files at all: no groups (the flyout then says so in one line)
    assert r["empty-files"] == []
    assert r["null-files"] == []
    # no recorded change folder: names fall back to basenames
    assert [f["name"] for g in r["no-folder-recorded"] for f in g["files"]] == \
        ["proposal.md", "manifest.yaml"]


# ---- real fixture snapshot end-to-end ------------------------------------------

def test_wheel_model_derives_from_the_real_fixture_snapshot(tmp_path):
    r = _run_wheel_model(_snapshot(), tmp_path)
    assert r["wheels"]["documents"]["count"] > 0
    assert r["wheels"]["clusters"]["count"] > 0
    assert r["edges"], "the fixture snapshot must materialize edges"
    for e in r["edges"]:
        assert e["cls"] in ("indexed", "inferred", "synthesized")


# ---- snapshot projection (the WHEEL's data dependency) --------------------------

def test_project_possibles_carries_origin_and_derivation_additively():
    projected = project_possibles(
        [_derived("pos-derived-open") |
         {"provenance": {"document": "ideation/brainstorm/x.md",
                         "section": "derived-from cluster cl-a"}}],
        worked_example_docs=set())  # NOT a worked example: guard must exempt
    assert len(projected) == 1
    p = projected[0]
    assert p["origin"] == "ai-derived"
    assert p["derivation"]["disposition"] == "pending_review"
    assert "provenance" not in p  # register-only field stays register-only


def test_no_fabrication_guard_still_drops_non_derived_strays():
    stray = {"id": "pos-stray", "title": "S", "claim": "c", "state": "latent",
             "provenance": {"document": "ideation/brainstorm/x.md",
                            "section": "Possible feats"}}
    assert project_possibles([stray], worked_example_docs=set()) == []


# ==========================================================================
# 011 add-wheel-action-verbs — the four action-row verbs (W1–W12)
#
# The pure table decides what an expanded tile OFFERS. It is an approximation
# of the engine's authority: the engine re-reads the pinned checkout and may
# still refuse (FR-010a/FR-023). These cases pin the OFFER, not the outcome.
# ==========================================================================

def test_w1_promotable_possible_offers_both_commission_verbs(tmp_path):
    """W1: a latent, non-derived, non-demo possible is promotable.

    The item here is the REAL shape the wheel's builder emits — the register
    state lives under `ref`, not at the top level. An earlier version of these
    cases invented a flat `{"id","state"}` item, and that fiction hid a defect
    in which `promote-to-staging` never rendered on the real dashboard at all
    (found by driving the page with Playwright, 2026-08-02)."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert [a["id"] for a in r["w-promotable"]] == \
        ["promote-to-staging", "research-brief", "workbench"]


def test_w2_w3_undisposed_derived_offers_research_only(tmp_path):
    """W2/W3: awaiting a verdict — and a `deferred` verdict, which the view's
    own helper already classes as undisposed — offer the brief but NOT the
    promotion. `deferred` is not an acceptance."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    for cid in ("w-derived-pending", "w-derived-deferred"):
        ids = [a["id"] for a in r[cid]]
        assert "research-brief" in ids, cid
        assert "promote-to-staging" not in ids, cid


@pytest.mark.parametrize("cid", ["w-rejected", "w-superseded", "w-picked"])
def test_w4_terminal_and_picked_possibles_offer_no_promotion(tmp_path, cid):
    """W4: only a `latent` possible is promotable."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert "promote-to-staging" not in [a["id"] for a in r[cid]]


def test_w5_demo_placeholder_offers_no_register_targeting_verb(tmp_path):
    """W5: a synthesized demo possible has no register entry, so offering a
    verb the engine must refuse would be a guaranteed dead end."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    ids = [a["id"] for a in r["w-demo"]]
    assert "promote-to-staging" not in ids and "research-brief" not in ids


def test_w6_cluster_tile_offers_derive_possibles(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert "derive-possibles" in [a["id"] for a in r["w-cluster"]]


def test_w7_w8_demote_is_offered_on_active_and_never_on_archived(tmp_path):
    """W7/W8: `archived` tiles also carry a change id, but the engine refuses a
    non-`active` change — so the column choice is enforced, not styled."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert "demote" in [a["id"] for a in r["w-active"]]
    assert "demote" not in [a["id"] for a in r["w-archived"]]


def test_w9_gate_off_offers_none_of_the_four_verbs(tmp_path):
    """W9 / SC-008: with the capability off, zero of this feature's verbs
    render on any column."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    new_verbs = {"promote-to-staging", "research-brief", "derive-possibles", "demote"}
    for cid in ("w-possibles-gateoff", "w-cluster-gateoff", "w-active-gateoff"):
        assert not (new_verbs & {a["id"] for a in r[cid]}), cid


def test_w10_retirement_is_per_verb_not_per_tile(tmp_path):
    """W10 — the case that CANNOT pass without the environment seam (FR-033b).
    Commissioning one possibles verb must leave the other offered."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    after_brief = [a["id"] for a in r["w-brief-commissioned"]]
    assert "research-brief" not in after_brief      # retired
    assert "promote-to-staging" in after_brief      # untouched

    after_promote = [a["id"] for a in r["w-promote-commissioned"]]
    assert "promote-to-staging" not in after_promote
    assert "research-brief" in after_promote


def test_w11_demote_and_derive_retire_for_the_session(tmp_path):
    """W11: demote participates in retirement too — it carries no engine-side
    duplicate guard, so this is the only thing standing between a double-click
    and a second full artifact set."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert "demote" not in [a["id"] for a in r["w-demote-recorded"]]
    assert "derive-possibles" not in [a["id"] for a in r["w-cluster-commissioned"]]


def test_legacy_tile_wide_commissioned_boolean_still_retires_everything(tmp_path):
    """The seam is backward-compatible: a plain boolean keeps its old meaning,
    so every pre-existing caller and case is unaffected."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    ids = [a["id"] for a in r["w-legacy-boolean"]]
    assert "promote-to-staging" not in ids and "research-brief" not in ids
    assert ids == ["workbench"]      # the read-only verb survives


def test_w12_every_pre_existing_verb_survives_on_every_column(tmp_path):
    """W12 / FR-040: the new rows ADD; they never displace. This is the
    unchanged-rows guarantee stated as one assertion."""
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    assert [a["id"] for a in r["documents-gated"]] == ["read"]
    assert [a["id"] for a in r["archived-gated"]] == ["landed"]
    assert [a["id"] for a in r["staged-gated"]] == ["read", "propose", "workbench"]
    # the three columns this feature fills keep their prior verbs, in order
    assert [a["id"] for a in r["clusters-gated"]][:2] == ["lens", "canvas"]
    assert [a["id"] for a in r["clusters-gated"]][-1] == "workbench"
    assert [a["id"] for a in r["possibles-gated"]][-1] == "workbench"
    assert [a["id"] for a in r["active-gated"]][0] == "packet"


def test_new_verb_labels_are_distinct_and_stable(tmp_path):
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    labels = {a["id"]: a["label"] for cid in ("w-promotable", "w-cluster", "w-active")
              for a in r[cid]}
    assert labels["promote-to-staging"] == "▲ promote to staging"
    assert labels["research-brief"] == "✻ research brief"
    assert labels["derive-possibles"] == "✦ derive possibles"
    assert labels["demote"] == "◀ demote"


# ---- the live-captured projection (regression, Playwright 2026-08-02) ------

def test_real_served_projection_offers_the_right_verbs(tmp_path):
    """The item objects here were CAPTURED from the served wheel model running
    in a real browser, then pasted verbatim. They are the shape production
    actually produces.

    This exists because the authored fixtures were wrong in a way that mattered:
    they put the register `state` at the item's top level, but the builder emits
    `{id, label, sub, demo, derivedPending, ref}` with the state under `ref`. The
    promotability predicate read `item.state`, got `undefined` for every real
    tile, and `promote-to-staging` never rendered on the dashboard — while every
    unit test passed. Only driving the page caught it.
    """
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    # an ACCEPTED derived possible is promotable — and, being DISPOSED, must
    # NOT be offered a pre-verdict brief (FR-032/FR-018a: the view hides it once
    # the possible is disposed, while the engine stays permissive)
    assert [a["id"] for a in r["w-real-projection-accepted"]] == \
        ["promote-to-staging", "workbench"]
    # one still awaiting a verdict is NOT — the guard is not broadened
    ids = [a["id"] for a in r["w-real-projection-pending"]]
    assert "research-brief" in ids and "promote-to-staging" not in ids


# ---- D-3 root cause: the action row must be RECONCILED, not left alone -----

def test_action_row_staleness_is_a_pure_decision(tmp_path):
    """FR-033 requires retirement to REMOVE the row entry, not disable it. The
    wheel's redraw therefore has to notice when the offered verb set changed.

    `actionRowIsStale` is that decision, extracted so it is testable: the mounted
    row is stale exactly when the set of verbs it holds differs from the set the
    table now offers. It must answer NO for an unchanged set — that is what
    preserves a mounter's own post-refusal state and an open reason form across
    the redraw, which is why the old blanket early-return existed.
    """
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["stale"]
    assert r["identical"] is False        # unchanged -> leave the row alone
    assert r["bothEmpty"] is False
    assert r["reordered"] is False        # a set comparison, not a sequence one
    assert r["retired"] is True           # a verb went away -> rebuild
    assert r["appeared"] is True
    assert r["emptied"] is True


# ---- D-4: the brief is a PRE-VERDICT verb in the view ----------------------

def test_research_brief_is_hidden_once_a_closing_verdict_exists(tmp_path):
    """D-4 (Playwright-found) — FR-032/FR-018a scope the brief's VISIBILITY to an
    UNDISPOSED possible: "legal before disposition; the view hides it once
    disposed". The engine stays permissive by design (clarify Q22's
    engine-permissive / view-tidy split) — this is a view rule only.

    `deferred` does NOT close the window. The shipped `isUndisposedDerived`
    already rules that a deferred verdict "keeps it awaiting", so a deferred
    possible is still undisposed here and still gets the brief.
    """
    r = _run_expand(EXPAND_CASES, ACTION_CASES, tmp_path)["actions"]
    # HIDDEN: a closing verdict was recorded
    assert "research-brief" not in [a["id"] for a in r["w-real-projection-accepted"]]
    # SHOWN: no verdict yet
    assert "research-brief" in [a["id"] for a in r["w-real-projection-pending"]]
    # SHOWN: deferred keeps the possible awaiting a ruling
    assert "research-brief" in [a["id"] for a in r["w-real-deferred"]]
    # SHOWN: human-authored with no disposition recorded at all
    assert "research-brief" in [a["id"] for a in r["w-promotable"]]
    # promote-to-staging is untouched by this rule
    assert "promote-to-staging" in [a["id"] for a in r["w-real-projection-accepted"]]
    assert "promote-to-staging" not in [a["id"] for a in r["w-real-deferred"]]
