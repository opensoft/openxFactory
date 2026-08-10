"""The SHARED bullseye widget (views/bullseye.js; openxFactory
`add-workbench-bullseye-and-create` design D1/D6).

There is exactly ONE match-count bullseye renderer in the bundle, lifted out of
`views/lens.js` so the keyword-lens tab and the staging workbench's lens panel
cannot drift. Python-side only — no browser automation: the ACTUAL module runs in
node against a minimal DOM stub (skipped when node is absent), rendering a real
`buildLensModel` result, so the assertions are about the widget's OWN output
rather than a re-implementation of it.

What is pinned here:

  geometry -> DOM     one ring circle + one ring label per ring, one divider +
                      one label per sector, one dot group per dot — the counts
                      come from the model, never from a second layout rule.
  the no-checked case  a single "check a keyword" label and NO rings, so an
                      empty selection can never render a misleading target.
  the centre gesture   `onActivate` renders ONE focusable, role=button hit
                      region over the matches-ALL zone (design D6); with no
                      callback the region is ABSENT entirely, which is what
                      keeps the keyword-lens tab's SVG byte-identical to what it
                      drew before the lift.
  consumers            both surfaces import the widget, and neither keeps a
                      private `bullseye(` renderer.
  no transport         the widget is pure DOM over a model: no fetch, no dynamic
                      import, no external URL beyond the SVG XML namespace.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
BULLSEYE_JS = WEB / "views" / "bullseye.js"
LENS_MODEL_JS = WEB / "views" / "lens-model.js"
LENS_JS = WEB / "views" / "lens.js"
WORKBENCH_JS = WEB / "views" / "staging-workbench.js"
NODE = shutil.which("node")

# A minimal SVG-only DOM: every node records its tag, attributes, text, wired
# event types, and children, so the harness can report the tree as JSON. The
# widget touches nothing else (createElementNS + setAttribute + appendChild +
# textContent + addEventListener).
_NODE_HARNESS = """
globalThis.document = {
  createElementNS(ns, tag) {
    return {
      tag, attrs: {}, children: [], text: null, events: [], handlers: {},
      setAttribute(k, v) { this.attrs[k] = String(v); },
      appendChild(child) { this.children.push(child); return child; },
      // handlers are KEPT (not just their type names) so the harness can fire a
      // region and pin what it hands the caller, not merely that it is wired
      addEventListener(type, fn) { this.events.push(type); this.handlers[type] = fn; },
      set textContent(v) { this.text = v; },
      get textContent() { return this.text; },
    };
  },
};
const EV = { preventDefault() {} };
const { renderBullseye } = await import('./bullseye.js');
const { buildLensModel } = await import('./lens-model.js');
import { readFileSync } from 'node:fs';

function flatten(node, out) {
  out.push({ tag: node.tag, cls: node.attrs.class || null, attrs: node.attrs,
             text: node.text, events: node.events, node });
  for (const child of node.children) flatten(child, out);
  return out;
}

// Fire one region the way a human would: a click, then Enter, then Space, and
// report every region object the widget handed back. `keydown` with an ignored
// key must hand back nothing.
function fireAll(hit, sink) {
  const before = sink.length;
  hit.node.handlers.click(EV);
  hit.node.handlers.keydown({ ...EV, key: 'Enter' });
  hit.node.handlers.keydown({ ...EV, key: ' ' });
  hit.node.handlers.keydown({ ...EV, key: 'a' });
  return sink.slice(before);
}

const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const [id, snapshot, checked, wire] of cases) {
  const model = buildLensModel(snapshot, { checked });
  // every region reports the subset it would seed a create with, so the harness
  // pins the sector -> keywords mapping (open question 2's ruling) and not just
  // the presence of a hit node
  const activations = [];
  const node = renderBullseye(model, wire
    ? { onActivate: (region) => activations.push(region), centreLabel: 'create here' }
    : null);
  const nodes = flatten(node, []);
  const centre = nodes.filter((n) => n.cls === 'bullseye-centre');
  const hits = nodes.filter((n) => n.cls === 'bullseye-sector');
  out[id] = {
    root: { tag: node.tag, cls: node.attrs.class, aria: node.attrs['aria-label'] },
    counts: {
      rings: nodes.filter((n) => n.cls === 'ring' || n.cls === 'ring zone0').length,
      centreRings: nodes.filter((n) => n.cls === 'ring zone0').length,
      ringLabels: nodes.filter((n) => n.cls === 'ringlab').length,
      sectors: nodes.filter((n) => n.cls === 'sector').length,
      sectorLabels: nodes.filter((n) => n.cls === 'seclab').length,
      dots: nodes.filter((n) => n.cls === 'lensdot').length,
      centre: centre.length,
      sectorHits: hits.length,
    },
    centre: centre.length ? {
      tag: centre[0].tag, role: centre[0].attrs.role,
      tabindex: centre[0].attrs.tabindex, aria: centre[0].attrs['aria-label'],
      events: centre[0].events, r: centre[0].attrs.r,
    } : null,
    sectorHits: hits.map((n) => ({
      tag: n.tag, role: n.attrs.role, tabindex: n.attrs.tabindex,
      aria: n.attrs['aria-label'], events: n.events, d: n.attrs.d,
      // the widget's own <title> child, the hover affordance
      title: (n.node.children[0] || {}).text || null,
      // what activating THIS region hands the caller: click, Enter, Space each
      // once; an ignored key adds nothing
      regions: fireAll(n, activations),
    })),
    centreRegions: centre.length ? fireAll(centre[0], activations) : [],
    labels: nodes.filter((n) => n.cls === 'ringlab').map((n) => n.text),
    docLabels: nodes.filter((n) => n.cls === 'doclab').map((n) => n.text),
    // a roomy dot carries its number INSIDE itself instead
    insideLabels: nodes.filter((n) => n.cls === 'dotnum').map((n) => n.text),
    // the names the numbers stand for: each dot circle's own <title> child
    dotTitles: nodes.filter((n) => n.tag === 'circle'
        && (n.cls || '').startsWith('dot'))
      .map((n) => (n.node.children[0] || {}).text || null),
    sectorLabels: nodes.filter((n) => n.cls === 'seclab').map((n) => n.text),
    sectorLabelAt: nodes.filter((n) => n.cls === 'seclab').map((n) => ({
      text: n.text, x: +n.attrs.x, y: +n.attrs.y })),
    arcs: nodes.filter((n) => n.cls === 'secarc').map((n) => n.attrs.style),
    ringLabelAt: nodes.filter((n) => n.cls === 'ringlab').map((n) => ({
      text: n.text, x: +n.attrs.x, y: +n.attrs.y })),
    sectorLines: nodes.filter((n) => n.cls === 'sector').map((n) => ({
      x1: +n.attrs.x1, y1: +n.attrs.y1, x2: +n.attrs.x2, y2: +n.attrs.y2 })),
    model: {
      rings: model.rings.length, sectors: model.sectors.length,
      dots: model.dots.length, checked: model.checked,
      centreRadius: (model.rings.find((r) => r.isCenter) || {}).outerRadius,
      dotRows: model.dots.map((d) => d.row),
      dotColumns: model.dots.map((d) => d.column),
      dotNumbers: model.dots.map((d) => d.number),
      dotCells: model.dots.map((d) => d.subsetKey),
      keywordLabels: model.keywordLabels,
      keywordHues: model.keywordHues,
      ringAngles: model.rings.map((x) => ({ label: x.label, at: x.labelAngle })),
      sectorHues: model.sectors.map((s) => ({
        key: s.subsetKey, matchCount: s.matchCount, at: s.angleDeg,
        span: s.spanDeg, hues: s.hues })),
      dotSizes: [...new Set(model.dots.map((d) => d.size))],
      sectorList: model.sectors.map((s) => ({
        subsetKey: s.subsetKey, keywords: s.keywords, matchCount: s.matchCount,
        isCenter: s.isCenter, spanDeg: s.spanDeg,
        outerRadius: s.outerRadius, innerRadius: s.innerRadius,
      })),
    },
  };
}
console.log(JSON.stringify(out));
"""


def _hand_snapshot():
    return {
        "repository": "fixture-repo",
        "generation": {"source_revision": "a" * 40},
        "documents": [
            {"id": "a.md", "path": "a.md", "topics": ["alpha", "beta"]},
            {"id": "b.md", "path": "b.md", "topics": ["alpha"]},
            {"id": "c.md", "path": "c.md", "topics": ["beta"]},
            {"id": "d.md", "path": "d.md", "topics": ["gamma"]},
        ],
        "keyword_index": [
            {"keyword": "alpha", "declared_doc_count": 2},
            {"keyword": "beta", "declared_doc_count": 2},
            {"keyword": "gamma", "declared_doc_count": 1},
        ],
    }


SNAP = _hand_snapshot()
# A cell with far more documents than one row holds, so the packing stacks
# rows and only the OUTER one may be labelled (Brett's 2026-08-07 ruling).
_CROWD_SUBSETS = [["b"], ["c"], ["d"], ["a", "b"], ["a", "c"], ["b", "c"],
                  ["a", "b", "c"]]
CROWDED = {
    "repository": "fixture-repo",
    "generation": {"source_revision": "c" * 40},
    # 24 documents in ONE cell (they match `a` alone, so they share a ring and
    # a sector), plus enough other subsets to make that sector's slice narrow —
    # which is what forces the packing to stack rows.
    "documents": (
        [{"id": f"doc-{i:02d}.md", "path": f"doc-{i:02d}.md", "topics": ["a"]}
         for i in range(24)]
        + [{"id": f"other-{i}.md", "path": f"other-{i}.md", "topics": s}
           for i, s in enumerate(_CROWD_SUBSETS)]),
    "keyword_index": [{"keyword": k, "declared_doc_count": 24}
                      for k in ("a", "b", "c", "d")],
}

CASES = [
    # (id, snapshot, checked, wire the centre gesture)
    ("crowded", CROWDED, ["a", "b", "c", "d"], False),
    ("two-checked", SNAP, ["alpha", "beta"], False),
    ("two-checked-wired", SNAP, ["alpha", "beta"], True),
    ("one-checked", SNAP, ["alpha"], False),
    ("none-checked", SNAP, [], False),
    ("none-checked-wired", SNAP, [], True),
]


def _render(tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS renderer probe")
    shutil.copy(BULLSEYE_JS, tmp_path / "bullseye.js")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.js")
    # ESM without renaming to .mjs: the widget imports "./lens-model.js" by name
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(CASES), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_bullseye_renders_the_models_geometry(tmp_path):
    r = _render(tmp_path)["two-checked"]
    assert r["root"]["tag"] == "svg" and r["root"]["cls"] == "bullseye"
    assert "rings by number of checked keywords matched" in r["root"]["aria"]
    # one ring circle + one label per ring; one divider + one label per sector;
    # one group per dot — every count is the model's own
    assert r["counts"]["rings"] == r["model"]["rings"] == 2
    assert r["counts"]["ringLabels"] == r["model"]["rings"]
    assert r["counts"]["sectors"] == r["model"]["sectors"]
    # every sector but the matches-ALL one is labelled: that one IS the shaded
    # centre, already named by its ring label, so a second label would be noise
    centres = sum(1 for s in r["model"]["sectorList"] if s["isCenter"])
    assert r["counts"]["sectorLabels"] == r["model"]["sectors"] - centres
    assert r["counts"]["dots"] == r["model"]["dots"] == 3
    # exactly ONE shaded centre zone, labelled "all N ✓"
    assert r["counts"]["centreRings"] == 1
    assert "all 2 ✓" in r["labels"]
    # The dots carry their matrix NUMBER, not the document name (Brett's
    # 2026-08-07 rulings): INSIDE the dot where the cell has room for a big
    # one, beside it otherwise. The name is not lost either way — it stays in
    # the dot's <title> and in the numbered matrix, which is the legend.
    assert set(r["docLabels"]) | set(r["insideLabels"]) == {"1", "2", "3"}
    assert all(t.startswith("#") and ".md" in t for t in r["dotTitles"]), r["dotTitles"]


def test_no_checked_keywords_renders_a_prompt_and_no_rings(tmp_path):
    r = _render(tmp_path)["none-checked"]
    assert r["counts"]["rings"] == 0
    assert r["counts"]["dots"] == 0
    assert r["labels"] == ["check a keyword to stratify the corpus"]
    # and with the gesture wired there is still nothing to activate
    wired = _render(tmp_path)["none-checked-wired"]
    assert wired["counts"]["centre"] == 0


def test_centre_gesture_is_present_only_when_wired(tmp_path):
    out = _render(tmp_path)
    # the keyword-lens tab supplies no callback: the region is ABSENT, so its SVG
    # is what it was before the widget lift (design D6)
    assert out["two-checked"]["counts"]["centre"] == 0
    wired = out["two-checked-wired"]
    assert wired["counts"]["centre"] == 1
    centre = wired["centre"]
    assert centre["tag"] == "circle"
    # focusable + announced + keyboard-reachable, not a bare click target
    assert centre["role"] == "button" and centre["tabindex"] == "0"
    assert centre["aria"] == "create here"
    assert set(centre["events"]) == {"click", "keydown"}
    # it covers the matches-ALL zone: the centre ring's own outer radius
    assert float(centre["r"]) == pytest.approx(
        round(wired["model"]["centreRadius"] * 100) / 100)
    # and it hands back the WHOLE checked set — click, Enter, and Space alike,
    # while an ignored key hands back nothing
    regions = wired["centreRegions"]
    assert len(regions) == 3
    for region in regions:
        assert region["kind"] == "centre"
        assert region["keywords"] == wired["model"]["checked"] == ["alpha", "beta"]


# ---- ring-sector activation (open question 2's ruling) --------------------------

def test_sector_regions_are_activatable_only_when_wired(tmp_path):
    """Brett's 2026-07-25 ruling on open question 2: activating ANY ring sector
    opens the create dialog seeded with that sector's matched combination, on the
    same keyboard terms as the centre region. The keyword-lens tab supplies no
    handler, so NO region exists there and its SVG is unchanged."""
    out = _render(tmp_path)
    # inert on the main lens tab: no centre region and no sector region at all
    assert out["two-checked"]["counts"]["centre"] == 0
    assert out["two-checked"]["counts"]["sectorHits"] == 0
    # the DRAWN sectors (dividers + labels) are identical either way — only the
    # hit regions appear, so the visible bullseye does not change
    for key in ("sectors", "sectorLabels", "rings", "ringLabels", "dots"):
        assert out["two-checked"]["counts"][key] == out["two-checked-wired"]["counts"][key]

    wired = out["two-checked-wired"]
    # three distinct matched subsets — alpha∧beta (the matches-ALL one), alpha,
    # beta — and the matches-ALL sector is left to the CENTRE region, so exactly
    # the two PROPER subsets get their own hit region
    subsets = wired["model"]["sectorList"]
    assert [s["subsetKey"] for s in subsets] == ["alpha ∧ beta", "alpha", "beta"]
    assert [s["isCenter"] for s in subsets] == [True, False, False]
    assert wired["counts"]["sectorHits"] == 2
    for hit in wired["sectorHits"]:
        assert hit["tag"] == "path"
        assert hit["role"] == "button" and hit["tabindex"] == "0"
        assert set(hit["events"]) == {"click", "keydown"}
        assert hit["aria"] and hit["aria"] == hit["title"]
        assert hit["d"].startswith("M ") and hit["d"].endswith(" Z")


def test_sector_activation_hands_back_that_sectors_keywords(tmp_path):
    """The sector -> keywords mapping: each region reports its OWN matched subset,
    so the caller seeds `Topics:` from it without re-deriving anything from the
    geometry or re-splitting the joined label."""
    wired = _render(tmp_path)["two-checked-wired"]
    by_key = {}
    for hit in wired["sectorHits"]:
        # click + Enter + Space all fire; the ignored key does not
        assert len(hit["regions"]) == 3
        kinds = {r["kind"] for r in hit["regions"]}
        keys = {r["subsetKey"] for r in hit["regions"]}
        assert kinds == {"sector"} and len(keys) == 1
        by_key[hit["regions"][0]["subsetKey"]] = hit["regions"][0]["keywords"]
    # exactly the two proper subsets, each carrying its own keyword list — NOT
    # the whole checked set
    assert by_key == {"alpha": ["alpha"], "beta": ["beta"]}
    # every sector's aria label names its own combination
    arias = sorted(hit["aria"] for hit in wired["sectorHits"])
    assert arias == ["create a document from the alpha combination (1 of 2 checked)",
                     "create a document from the beta combination (1 of 2 checked)"]


def test_sector_geometry_puts_each_subset_on_its_own_ring_band(tmp_path):
    """A sector is one distinct subset, so it lives on the ring for its own size:
    the band between that match count's outer radius and the next one in. The hit
    shape and the dots inside it come from ONE derivation."""
    wired = _render(tmp_path)["two-checked-wired"]
    subsets = {s["subsetKey"]: s for s in wired["model"]["sectorList"]}
    # three distinct subsets share the 360 degrees evenly
    assert {s["spanDeg"] for s in subsets.values()} == {120.0}
    # the matches-ALL subset reaches the centre; a 1-match subset sits in the
    # outer band, bounded inside by the centre ring's radius
    centre_r = wired["model"]["centreRadius"]
    assert subsets["alpha ∧ beta"]["matchCount"] == 2
    assert subsets["alpha ∧ beta"]["innerRadius"] == 0
    assert subsets["alpha ∧ beta"]["outerRadius"] == pytest.approx(centre_r)
    for key in ("alpha", "beta"):
        assert subsets[key]["matchCount"] == 1
        assert subsets[key]["innerRadius"] == pytest.approx(centre_r)
        assert subsets[key]["outerRadius"] > centre_r


def test_the_activation_handler_is_wired_only_where_a_gesture_exists():
    """Design D6 gave the KEYWORD lens tab no handler, so every region there is
    inert and its SVG is what it always drew. D21 (Brett, 2026-08-07) adds the
    repository vocabulary, whose regions DO have a gesture — the drill-in — so
    the tab now wires a handler under exactly one condition. This pins that
    condition: one call site, gated on the vocabulary, so the keyword lens
    cannot regain hit regions by accident."""
    # comments may DISCUSS the seam; only a wired property counts as supplying it
    lens = "\n".join(ln for ln in LENS_JS.read_text(encoding="utf-8").splitlines()
                     if not ln.lstrip().startswith("//"))
    workbench = WORKBENCH_JS.read_text(encoding="utf-8")

    # exactly ONE wiring in the lens, and only under the drill condition.
    # The lens now also passes `onDocument` (a dot is its document's checkbox),
    # so "passes no opts at all" is no longer the mechanism that keeps the
    # keyword vocabulary's regions inert — the INVARIANT is what matters and
    # it is asserted from both sides: the lens sets `onActivate` only when a
    # drill exists, and the renderer draws a region only when it is a function.
    assert lens.count("onActivate") == 1, "the lens tab wires the handler once"
    assert "if (ctx.onDrill) bullseyeOpts.onActivate = ctx.onDrill;" in lens, (
        "the activation handler must be set only for the vocabulary that has "
        "a gesture")
    renderer = BULLSEYE_JS.read_text(encoding="utf-8")
    assert 'if (typeof o.onActivate === "function") {' in renderer, (
        "hit regions must be gated on the HANDLER, never on the presence of "
        "an options object — otherwise any new option would grant them")
    # ...and the handler exists only for the repository vocabulary
    assert 'vocab.id === "repositories" && options.onDrillIn' in lens, (
        "the drill-in handler must be gated on the repository vocabulary")

    assert "onActivate:" in workbench, "the workbench must wire the create gesture"
    # and the workbench routes a SECTOR's own keywords into the seed
    assert 'region.kind === "sector"' in workbench
    assert "subset: [...region.keywords]" in workbench


def test_one_checked_keyword_centre_covers_the_whole_field(tmp_path):
    """With a single checked keyword the matches-ALL zone IS the outer circle —
    the gesture still resolves to exactly one region, never zero or two."""
    r = _render(tmp_path)["one-checked"]
    assert r["counts"]["rings"] == 1 and r["counts"]["centreRings"] == 1


# ---- one renderer, two consumers ------------------------------------------------

def test_both_surfaces_consume_the_shared_widget():
    lens = LENS_JS.read_text(encoding="utf-8")
    workbench = WORKBENCH_JS.read_text(encoding="utf-8")
    for name, body in (("lens.js", lens), ("staging-workbench.js", workbench)):
        assert 'from "./bullseye.js"' in body, f"{name} does not import the widget"
        assert "renderBullseye(" in body, f"{name} does not render the widget"
    # neither view keeps a private renderer: no local `function bullseye(` and no
    # second createElementNS-based SVG layout
    for name, body in (("lens.js", lens), ("staging-workbench.js", workbench)):
        assert "function bullseye(" not in body, f"{name} kept a private renderer"
        assert "createElementNS" not in body, f"{name} builds SVG of its own"


def test_bullseye_widget_has_no_network_primitive_and_no_markup_sink():
    body = BULLSEYE_JS.read_text(encoding="utf-8")
    assert "fetch(" not in body
    assert "import(" not in body
    # the widget only ever BUILDS nodes — it never assigns innerHTML at all
    assert not re.findall(r"\.innerHTML\s*=", body)
    external = re.compile(
        r"https?://(?!www\.w3\.org)|unpkg|jsdelivr|googleapis|cdnjs|"
        r"XMLHttpRequest|WebSocket|EventSource|navigator\.sendBeacon", re.IGNORECASE)
    offenders = [ln for ln in body.splitlines() if external.search(ln)]
    assert not offenders, f"external network primitive in bullseye.js: {offenders}"
    # every dynamic value binds through the svg() helper's textContent assignment
    assert "node.textContent = text" in body


def test_the_radar_labels_by_number_and_keeps_names_in_the_legend(tmp_path):
    """Brett's 2026-08-07 rulings: names are too large for the radar, so the
    radar carries INDEXES — and the two series use different alphabets so a
    label is never ambiguous about what it names. Documents are numbers,
    vocabulary is letters (A…Z, AA, …)."""
    r = _render(tmp_path)["two-checked"]
    # every dot is labelled, by number — nothing is dropped for width now
    drawn = r["docLabels"] + r["insideLabels"]
    assert sorted(drawn, key=int) == ["1", "2", "3"]
    assert len(drawn) == r["counts"]["dots"]
    # sectors are labelled by the keywords' RAIL LETTERS, not their names —
    # and never by numbers, which belong to documents
    for label in r["sectorLabels"]:
        assert re.fullmatch(r"[A-Z]+( ∧ [A-Z]+)*", label), label
    # and no name is lost: each dot's title carries #number, the basename, and
    # the keywords it matched
    assert all(re.match(r"#\d+ \w+\.md — ", t) for t in r["dotTitles"]), r["dotTitles"]


def test_packed_dots_never_touch_at_any_density(tmp_path):
    """Brett's 2026-08-07 ruling: "spread out the dots so they are not
    directly touching each other". `packCell` is the whole of that promise —
    it uses the cell's real area (rows down the ring band × the sector's arc)
    and shrinks the dot only when the area demands it, so the edge-to-edge
    gap never falls below DOT_GAP. Measured across the densities the corpus
    actually produces, including a cell far past its own capacity."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "pack.mjs").write_text("""
import { packCell, DOT_GAP, DOT_R, DOT_MIN_R, DOT_MAX_R } from './lens-model.mjs';
// (n, band inner, band outer, sector span) — a lone dot, a comfortable cell,
// a thin band at 18 keywords, the wide-open single-keyword case, and a cell
// with far more documents than its area can hold.
const CASES = [[1, 180, 210, 30], [6, 180, 210, 30], [12, 195, 210, 25.7],
               [20, 190, 202, 8.4], [60, 0, 210, 120], [200, 195, 210, 8]];
const out = [];
for (const [n, inner, outer, span] of CASES) {
  const dots = packCell(n, inner, outer, span, -90);
  let worst = Infinity;
  for (let i = 0; i < dots.length; i += 1) {
    for (let j = i + 1; j < dots.length; j += 1) {
      const a = dots[i], b = dots[j];
      const ax = a.radius * Math.cos(a.angleDeg * Math.PI / 180);
      const ay = a.radius * Math.sin(a.angleDeg * Math.PI / 180);
      const bx = b.radius * Math.cos(b.angleDeg * Math.PI / 180);
      const by = b.radius * Math.sin(b.angleDeg * Math.PI / 180);
      worst = Math.min(worst, Math.hypot(ax - bx, ay - by) - a.size - b.size);
    }
  }
  out.push({ n, placed: dots.length, size: dots[0].size,
             rows: new Set(dots.map((d) => d.radius.toFixed(3))).size,
             slots: [...new Set(dots.map((d) => d.slot))].sort(),
             gap: dots.length > 1 ? worst : null });
}
console.log(JSON.stringify({ out, DOT_GAP, DOT_R, DOT_MIN_R, DOT_MAX_R }));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "pack.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    for case in r["out"]:
        # every document is placed — crowding shrinks dots, never drops one
        assert case["placed"] == case["n"], case
        # …and no two of them touch, at any density
        if case["gap"] is not None:
            assert case["gap"] >= r["DOT_GAP"] - 0.01, case
        # the size stays within the declared band
        assert r["DOT_MIN_R"] <= case["size"] <= r["DOT_MAX_R"], case
        # labels alternate above/below wherever there is more than one dot
        assert case["slots"] == ([0] if case["n"] == 1 else [0, 1]), case

    by_n = {c["n"]: c for c in r["out"]}
    # a roomy cell takes the BIGGEST dot its area allows, not merely a
    # full-size one — that is what lets the number ride inside it
    assert by_n[6]["size"] > r["DOT_R"] and by_n[6]["rows"] == 1
    assert by_n[1]["size"] == r["DOT_MAX_R"]      # a lone dot: the maximum
    # a deep band uses its depth: the single-keyword case stacks rows
    assert by_n[60]["rows"] > 1 and by_n[60]["size"] >= r["DOT_R"]
    # a thin, narrow, overcrowded cell shrinks to the floor and still separates
    assert by_n[200]["size"] == r["DOT_MIN_R"]


def test_a_column_is_numbered_outer_lane_inward(tmp_path):
    """Brett's 2026-08-07 ruling: "number them incremental from outside lane
    to inside lane, then start again on the next row… this way it is smaller
    arithmetic for the user." Numbers follow the LAYOUT — cell by cell, then
    column by column, each column running outer lane inward — so the dots
    inboard of a labelled one are +1, +2, +3 instead of +(lane length), and a
    cell's numbers are contiguous at all (numbering by snapshot order
    scattered them across the corpus, which no spacing could fix)."""
    r = _render(tmp_path)["crowded"]["model"]
    rows, cols = r["dotRows"], r["dotColumns"]
    numbers, cells = r["dotNumbers"], r["dotCells"]
    assert numbers == sorted(numbers), "numbers must run in layout order"
    assert numbers[0] == 1 and numbers[-1] == len(numbers)

    # every cell owns a CONTIGUOUS block of numbers
    seen = {}
    for cell, number in zip(cells, numbers):
        seen.setdefault(cell, []).append(number)
    for cell, block in seen.items():
        assert block == list(range(block[0], block[0] + len(block))), (cell, block)

    # inside a cell, a column's numbers are consecutive and run outer-lane
    # inward — which is the whole of the "+1, +2, +3" promise
    for cell in seen:
        by_column = {}
        for c, lane, number, k in zip(cols, rows, numbers, cells):
            if k == cell:
                by_column.setdefault(c, []).append((lane, number))
        for column, entries in by_column.items():
            entries.sort()
            lanes = [lane for lane, _ in entries]
            nums = [n for _, n in entries]
            assert lanes == sorted(lanes)
            assert nums == list(range(nums[0], nums[0] + len(nums))), (column, entries)


def test_only_the_outer_row_of_a_ring_is_labelled(tmp_path):
    """Brett's 2026-08-07 ruling: "for each ring, only label the outer row of
    dots — we can infer the numbers of the ones that are inboard of those
    dots in that same ring." A cell's numbers run along its outer row and
    continue inward, so an inboard label is clutter that costs the outer
    row's legibility."""
    r = _render(tmp_path)["crowded"]
    rows = r["model"]["dotRows"]
    assert max(rows) >= 1, "the fixture must actually stack rows"
    cols = r["model"]["dotColumns"]
    # labelled = outer lane AND every other column (the ruling's second half;
    # halving the labels is what buys each survivor room to draw)
    eligible = sum(1 for row, c in zip(rows, cols) if row == 0 and c % 2 == 0)
    assert r["counts"]["dots"] == len(rows) == 31
    eligible_all = sum(1 for row in rows if row == 0)
    # a CROWDED cell alternates; a roomy one labels every outer-lane dot, so
    # the drawn set sits between the two (Brett's 2026-08-07 refinement)
    assert 0 < len(r["docLabels"]) <= eligible_all
    assert eligible <= eligible_all
    # the inboard dots are still DRAWN and still name themselves on hover
    assert len(r["dotTitles"]) == 31
    assert all(t and ".md" in t for t in r["dotTitles"])


def test_letters_index_the_vocabulary_and_keep_going_past_z(tmp_path):
    """Brett's 2026-08-07 ruling: documents keep numbers, the vocabulary
    (keywords, or repositories in the repository lens) takes letters —
    "if more than 26, then we can use AA, AB, ... ZZ, AAA". Bijective
    base-26, exactly as a spreadsheet counts columns, so the series never
    runs out and never repeats."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "letters.mjs").write_text("""
import { letterLabel } from './lens-model.mjs';
const probe = [1, 2, 26, 27, 28, 52, 53, 78, 702, 703, 704];
console.log(JSON.stringify({
  probe: probe.map(letterLabel),
  // the first 800 are all distinct — a repeat would make two rows of the
  // rail claim the same sector label
  distinct: new Set(Array.from({length: 800}, (_, i) => letterLabel(i + 1))).size,
  guard: [letterLabel(0), letterLabel(-3)],
}));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "letters.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)
    assert r["probe"] == ["A", "B", "Z", "AA", "AB", "AZ", "BA", "BZ",
                          "ZZ", "AAA", "AAB"]
    assert r["distinct"] == 800
    # a nonsense index still yields a usable label rather than an empty one
    assert r["guard"] == ["A", "A"]


def test_a_roomy_cell_labels_every_column_and_a_crowded_one_alternates(tmp_path):
    """Brett's 2026-08-07 refinement: "only number every other column when the
    cell is crowded". Crowding is measured, not assumed — it is the arc
    between adjacent columns out where the labels sit, against the width even
    a staggered pair needs."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "crowd.mjs").write_text("""
import { packCell, LABEL_MIN_ARC } from './lens-model.mjs';
const shape = (dots) => ({
  crowded: dots[0].crowded,
  labelledColumns: [...new Set(dots.filter((d) => d.labelled).map((d) => d.column))],
  outerColumns: [...new Set(dots.filter((d) => d.row === 0).map((d) => d.column))],
});
console.log(JSON.stringify({
  LABEL_MIN_ARC,
  lone: shape(packCell(1, 180, 210, 30, -90)),
  roomy: shape(packCell(5, 180, 210, 40, -90)),
  crowded: shape(packCell(20, 190, 202, 8.4, -90)),
}));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "crowd.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    # a lone dot is never "crowded" and always carries its label
    assert r["lone"]["crowded"] is False
    assert r["lone"]["labelledColumns"] == [0]
    # a roomy cell keeps full-size dots far enough apart to label them ALL
    assert r["roomy"]["crowded"] is False
    assert r["roomy"]["labelledColumns"] == r["roomy"]["outerColumns"]
    assert len(r["roomy"]["labelledColumns"]) > 1
    # a tight cell alternates — every other column, starting at the first
    assert r["crowded"]["crowded"] is True
    assert r["crowded"]["labelledColumns"] == \
        [c for c in r["crowded"]["outerColumns"] if c % 2 == 0]
    assert len(r["crowded"]["labelledColumns"]) * 2 >= \
        len(r["crowded"]["outerColumns"]) - 1


def test_a_sector_is_drawn_at_its_own_ring_not_at_the_rim(tmp_path):
    """Brett's 2026-08-07 finding: "the A intersection B is the inside ring
    right? we have A Int B label on the upper right of the ring — what is
    that for?" It was that sector's name, pinned at the rim whatever ring it
    belonged to: a three-keyword sector's label sat ~60px outside the dot it
    named, in the band where the one-keyword sectors live. A sector's
    documents only ever occupy its own ring band, so its label and its
    divider now reach only that far, and the label's distance from the centre
    tells the reader which ring it names."""
    import math

    r = _render(tmp_path)["two-checked"]
    bands = {s["subsetKey"]: s for s in r["model"]["sectorList"]}
    assert any(s["matchCount"] > 1 for s in bands.values()), \
        "the fixture needs a multi-keyword sector to be worth measuring"

    radius = lambda p: math.hypot(p["x"] - 260, p["y"] - 260)  # noqa: E731
    labelled = {p["text"]: p for p in r["sectorLabelAt"]}
    for key, sec in bands.items():
        if sec["isCenter"]:
            # the matches-ALL sector IS the shaded centre, named by its ring
            continue
        letters = " ∧ ".join(
            r["model"]["keywordLabels"][k] for k in sec["keywords"])
        at = labelled.get(letters)
        if at is None:
            continue                       # dropped on collision, still valid
        # the label sits just OUTSIDE its own band, never at the rim
        assert sec["outerRadius"] <= radius(at) <= sec["outerRadius"] + 30, \
            (letters, radius(at), sec["outerRadius"])

    # and the dividers span only their own band, rather than the full radius
    for line in r["sectorLines"]:
        inner = math.hypot(line["x1"] - 260, line["y1"] - 260)
        outer = math.hypot(line["x2"] - 260, line["y2"] - 260)
        # (endpoints are rounded to 2dp for the SVG, so compare with slack)
        assert outer <= 210.05 and inner < outer
        assert any(abs(inner - s["innerRadius"]) < 0.05
                   and abs(outer - s["outerRadius"]) < 0.05
                   for s in bands.values()), (inner, outer)


def test_dots_sit_centred_in_their_ring_band(tmp_path):
    """Brett's 2026-08-07 ruling: "instead of the document dots being along
    the outer edge of the ring, lets center them radially." Rows were laid
    from the band's outer edge inward, so a cell using fewer lanes than its
    band admits clung to the ring line above it with the space below empty.
    The used lanes are now centred on the band's midline — and a single lane
    lands exactly on it, which is where a lone dot has always belonged."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "centre.mjs").write_text("""
import { packCell } from './lens-model.mjs';
const CASES = [[1, 180, 210, 30], [4, 180, 210, 40], [12, 157, 210, 45],
               [40, 0, 105, 360]];
console.log(JSON.stringify(CASES.map(([n, inner, outer, span]) => {
  const dots = packCell(n, inner, outer, span, -90);
  const radii = [...new Set(dots.map((d) => d.radius))].sort((a, b) => b - a);
  return { n, inner, outer, mid: (inner + outer) / 2, radii,
           centre: (radii[0] + radii[radii.length - 1]) / 2 };
})));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "centre.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    for case in json.loads(proc.stdout):
        # the lanes in use straddle the band's midline, whatever their number
        assert abs(case["centre"] - case["mid"]) < 0.001, case
        # a single lane IS the midline — not the outer edge it used to hug
        if len(case["radii"]) == 1:
            assert abs(case["radii"][0] - case["mid"]) < 0.001, case
        # and nothing escapes the band it belongs to
        assert case["radii"][0] <= case["outer"] and \
            case["radii"][-1] >= case["inner"], case


def test_a_roomy_cell_enlarges_its_dots_and_puts_the_number_inside(tmp_path):
    """Brett's 2026-08-07 ruling: "if there exists space in the slice, then
    spread out and enlarge the dots and place the number inside the dot. for
    congested, what we have works well." Both regimes, measured: a cell with
    room takes the biggest dot its area allows and carries its number inside
    — where it collides with nothing, so EVERY such dot is numbered — while a
    congested cell keeps small dots and the outside-label rules unchanged."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "room.mjs").write_text("""
import { packCell, DOT_MAX_R, DOT_R, LABEL_INSIDE_MIN_R } from './lens-model.mjs';
const shape = (dots, spanDeg) => ({
  size: dots[0].size,
  inside: dots.every((d) => d.inside),
  labelled: dots.filter((d) => d.labelled).length,
  count: dots.length,
  // how much of its slice the cell actually uses
  spread: Math.max(...dots.map((d) => d.angleDeg))
        - Math.min(...dots.map((d) => d.angleDeg)),
  usable: spanDeg * 0.9,
});
console.log(JSON.stringify({
  DOT_MAX_R, DOT_R, LABEL_INSIDE_MIN_R,
  lone: shape(packCell(1, 140, 210, 120, -90), 120),
  roomy: shape(packCell(4, 140, 210, 120, -90), 120),
  congested: shape(packCell(20, 190, 202, 8.4, -90), 8.4),
}));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "room.mjs")],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    # a lone dot in a wide slice takes the maximum size and holds its number
    assert r["lone"]["size"] == r["DOT_MAX_R"]
    assert r["lone"]["inside"] is True and r["lone"]["labelled"] == 1

    # a roomy cell: big dots, every one numbered inside, and SPREAD across
    # the slice rather than bunched against its centre line
    assert r["roomy"]["size"] >= r["LABEL_INSIDE_MIN_R"]
    assert r["roomy"]["inside"] is True
    assert r["roomy"]["labelled"] == r["roomy"]["count"]
    assert r["roomy"]["spread"] > r["roomy"]["usable"] * 0.9

    # congested: small dots, no inside numbers, and only some dots labelled —
    # the behaviour that was already working, left alone
    assert r["congested"]["size"] < r["DOT_R"]
    assert r["congested"]["inside"] is False
    assert r["congested"]["labelled"] < r["congested"]["count"]


def test_a_ring_label_sits_where_its_own_ring_is_empty(tmp_path):
    """Brett's 2026-08-07 ruling: "move the ring labels clear of the dot
    band." Radial clearance is not available — a band at 14 checked keywords
    is 15px deep and the dots sit on its midline, which is exactly why an
    11px dot began covering the label — so the label moves ANGULARLY, into
    the widest arc that ring leaves empty."""
    import math

    r = _render(tmp_path)["crowded"]["model"]
    by_ring = {}
    for sec in r["sectorHues"]:
        by_ring.setdefault(sec["matchCount"], []).append(sec)
    for ring in r["ringAngles"]:
        count = int(ring["label"].split()[-2]) if ring["label"].startswith("all") \
            else int(ring["label"].split()[0])
        occupied = by_ring.get(count, [])
        if not occupied:
            continue
        for sec in occupied:
            # the label's angle clears every sector's slice on that ring
            delta = abs((ring["at"] - sec["at"] + 180) % 360 - 180)
            assert delta > sec["span"] / 2, (ring, sec, delta)


def test_each_term_carries_one_hue_from_the_rail_to_the_ring(tmp_path):
    """Brett's 2026-08-07 ruling: "use a color for the Repo in the list and
    then use that for the color of that portion of the ring. But this should
    be subtle." One hue per vocabulary term, chosen by golden angle so rail
    neighbours are never hue neighbours; the widget paints a sector's arc in
    ONE SEGMENT PER KEYWORD, so a combination sector shows every term it
    belongs to instead of picking one. Only the hue is decided in code —
    weight and opacity live in the stylesheet, which is what keeps the change
    subtle and the theme in charge."""
    r = _render(tmp_path)["crowded"]
    hues = r["model"]["keywordHues"]
    assert len(set(hues.values())) == len(hues), hues        # all distinct
    assert all(0 <= h < 360 for h in hues.values())

    # a sector's hues ARE its keywords' hues, in the sector's own order
    for sec in r["model"]["sectorHues"]:
        keywords = sec["key"].split(" ∧ ")
        assert sec["hues"] == [hues[k] for k in keywords], sec

    # one arc per keyword per sector, each carrying its HUE as a custom
    # property. It used to carry a whole `stroke: hsl(H 45% 55%)` — which is
    # how a tint ended up dark-on-dark — so the stylesheet now composes the
    # colour and the theme owns the lightness.
    expected = sum(len(s["hues"]) for s in r["model"]["sectorHues"])
    assert len(r["arcs"]) == expected
    assert all(a and re.fullmatch(r"--h: \d+", a) for a in r["arcs"]), r["arcs"]


def test_the_label_faces_match_the_stylesheet():
    """The widget restates the label font sizes because SVG cannot ask CSS
    for a box before it lays out — so the two copies have to agree, or the
    collision maths reasons about a label narrower than the one drawn. They
    silently diverged when the sector letters were enlarged (Brett's
    2026-08-07 'the letters denoting repos are not large enough'): the
    stylesheet said 12px while the geometry still assumed 9.5."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    js = BULLSEYE_JS.read_text(encoding="utf-8")
    declared = dict(re.findall(
        r"(\w+):\s*([\d.]+)", re.search(r"const FONT = \{([^}]*)\}", js).group(1)))
    for cls, key in (("ringlab", "ring"), ("seclab", "sector"), ("doclab", "doc")):
        m = re.search(r"\.bullseye \." + cls + r"\s*\{[^}]*font-size:\s*([\d.]+)px",
                      css, re.S)
        assert m, cls
        assert float(m.group(1)) == float(declared[key]), (cls, m.group(1), declared)


def test_the_wheel_fit_constants_match_the_stylesheet():
    """wheel.js computes the deck's fit against the column width and the deck
    gap, so its copies of those numbers must match the stylesheet — the same
    class of divergence the bullseye's FONT copy already suffered. A silent
    drift here mis-scales the deck and the stage tiles above it stop lining
    up with the columns they head."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    js = (WEB / "views" / "wheel.js").read_text(encoding="utf-8")
    column_w = float(re.search(r"const COLUMN_W = ([\d.]+)", js).group(1))
    deck_gap = float(re.search(r"const DECK_GAP = ([\d.]+)", js).group(1))
    # anchor at line start: `:fullscreen .wheeldeck` overrides the gap and
    # would otherwise be the first match (it is, at 28px — this test caught it)
    css_col = float(re.search(
        r"(?m)^\.wheelcol\s*\{[^}]*?flex:\s*0 0 calc\(([\d.]+)px", css, re.S).group(1))
    css_gap = float(re.search(
        r"(?m)^\.wheeldeck\s*\{[^}]*?gap:\s*([\d.]+)px", css, re.S).group(1))
    assert column_w == css_col, (column_w, css_col)
    assert deck_gap == css_gap, (deck_gap, css_gap)
    # and the stage tiles share that gap, which is what puts the two rows on
    # one grid
    tiles_gap = float(re.search(
        r"(?m)^\.tiles\s*\{[^}]*?gap:\s*([\d.]+)px", css, re.S).group(1))
    assert tiles_gap == deck_gap, (tiles_gap, deck_gap)


def test_the_lens_screen_takes_the_page_and_scrolls_its_own_panes():
    """Brett's 2026-08-08 ruling: "when we are on the lens screen we want to
    remove anything not lens related… give as much screen as possible to the
    radar widget and the list of documents below. We want the radar widget to
    stay and scroll the document window and the repo window if it should need
    it." Three properties, each in one place: the shell marks the lens screen,
    the stylesheet hides the stage tiles on it, and the lens region itself
    does NOT scroll — its panes do, so the radar holds while the matrix under
    it and the rail beside it move."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    app = (WEB / "app.js").read_text(encoding="utf-8")

    # the shell marks the screen, and only for the lens
    assert 'classList.toggle("lensfull", target.view === "view-lens")' in app

    # the tiles are hidden there
    assert re.search(r"\.wrap\.lensfull\s*>\s*#stats\s*\{[^}]*display:\s*none", css)

    # the region does not scroll; each pane owns its own
    lens = re.search(r"(?m)^\.lens\s*\{([^}]*)\}", css).group(1)
    assert "overflow: hidden" in lens, lens
    assert "min-height: 0" in lens, lens
    for pane, rule in (("pane-rail", r"\.lens \.pane-rail\s*\{([^}]*)\}"),
                       ("pane-drill", r"\.lens \.pane-drill\s*\{([^}]*)\}")):
        body = re.search(rule, css).group(1)
        assert "overflow-y: auto" in body, (pane, body)
    # the matrix takes the height left under the radar and scrolls
    matrix = re.search(r"\.lens \.pane-bullseye > \.lensmatrix\s*\{([^}]*)\}",
                       css).group(1)
    assert "flex: 1 1 auto" in matrix and "overflow: auto" in matrix, matrix
    # …and the radar itself never shrinks to make room for it
    svg = re.search(r"\.lens \.pane-bullseye > \.bullseye\s*\{([^}]*)\}",
                    css).group(1)
    assert "flex: none" in svg, svg


def test_rail_stats_split_each_term_into_shared_and_only(tmp_path):
    """Brett's 2026-08-08 annotation: "make the repo tiles much larger and add
    more repo info into the tile." The fact worth adding is the one the radar
    is already drawing — how much of a repository's corpus it shares with
    another visible repository, and how much is its alone. Derived from the
    SAME dots, so the rail and the radar can never disagree."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "stats.mjs").write_text("""
import { buildLensModel, railStats } from './lens-model.mjs';
import { readFileSync } from 'node:fs';
const snapshot = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const model = buildLensModel(snapshot, { checked: ['a', 'b', 'c'] });
console.log(JSON.stringify({
  stats: railStats(model),
  universe: model.universe.length,
  empty: railStats(null),
}));
""", encoding="utf-8")
    snapshot = {
        "repository": "trio",
        "documents": [
            {"id": "all.md", "topics": ["a", "b", "c"]},
            {"id": "ab.md", "topics": ["a", "b"]},
            {"id": "onlya.md", "topics": ["a"]},
            {"id": "onlyc.md", "topics": ["c"]},
        ],
        "keyword_index": [{"keyword": k, "declared_doc_count": 1}
                          for k in ("a", "b", "c")],
    }
    data = tmp_path / "snap.json"
    data.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "stats.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    # a: three documents, two of them shared with b and/or c, one its own
    assert r["stats"]["a"] == {"total": 3, "shared": 2, "only": 1}
    assert r["stats"]["b"] == {"total": 2, "shared": 2, "only": 0}
    assert r["stats"]["c"] == {"total": 2, "shared": 1, "only": 1}
    # every document on the radar is counted once per term that carries it
    assert sum(s["total"] for s in r["stats"].values()) == 3 + 2 + 2
    assert r["universe"] == 4
    assert r["empty"] == {}


def test_cooccurrence_ranks_the_rail_and_offers_the_real_overlaps(tmp_path):
    """Brett's 2026-08-08 finding: "our keyword radar is not very usefull. our
    documents all tend to have only one keyword." Measured, the corpus says
    something more specific — 447 keywords over 150 tagged documents, 292 of
    them carried by a single document — so the overlap IS there (2,158 pairs
    share a document) and what was missing was any way to find it. The rail
    now ranks by connectivity and marks the long tail, and the model offers
    the strongest overlaps outright."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "co.mjs").write_text("""
import { buildLensModel, coOccurrence } from './lens-model.mjs';
import { readFileSync } from 'node:fs';
const snapshot = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const model = buildLensModel(snapshot, { checked: [] });
console.log(JSON.stringify({
  co: coOccurrence(snapshot),
  rail: model.rail.map((r) => [r.label, r.keyword, r.degree, r.solo]),
  pairs: model.pairs.map((p) => [p.a, p.b, p.documents]),
}));
""", encoding="utf-8")
    # `hub` rides three documents and meets everything; `lonely` has one
    # document of its own, so it can never bring a second dot
    snapshot = {
        "documents": [
            {"id": "1.md", "topics": ["hub", "alpha", "beta"]},
            {"id": "2.md", "topics": ["hub", "alpha"]},
            {"id": "3.md", "topics": ["hub", "beta"]},
            {"id": "4.md", "topics": ["lonely"]},
        ],
        "keyword_index": [
            {"keyword": "alpha", "declared_doc_count": 2},
            {"keyword": "beta", "declared_doc_count": 2},
            {"keyword": "hub", "declared_doc_count": 3},
            {"keyword": "lonely", "declared_doc_count": 1},
        ],
    }
    data = tmp_path / "snap.json"
    data.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "co.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    # every pair that shares a document, strongest first
    assert r["pairs"] == [["alpha", "hub", 2], ["beta", "hub", 2],
                          ["alpha", "beta", 1]]
    # connectivity: how many OTHER terms each meets
    assert r["co"]["degree"] == {"hub": 2, "alpha": 2, "beta": 2}
    assert "lonely" not in r["co"]["degree"]

    # the rail leads with the most connected, and letters follow that order —
    # so A is the term worth checking first, not the alphabetically first
    assert [row[1] for row in r["rail"]] == ["hub", "alpha", "beta", "lonely"]
    assert [row[0] for row in r["rail"]] == ["A", "B", "C", "D"]
    # the long tail is marked: carried by ONE document, whatever its degree
    assert [row[3] for row in r["rail"]] == [False, False, False, True]


def test_a_tint_is_a_hue_in_code_and_a_colour_in_the_stylesheet():
    """Brett's 2026-08-08 report: "several tiles are black on black and user
    cannot read." The cause was mine — the hue feature's own comment says
    "only the HUE is chosen here… saturation, lightness and opacity stay in
    the stylesheet, which is what keeps the theme in charge", and then the
    code wrote complete `hsl(H 45% 42%)` strings. 42% lightness reads on
    white and vanishes on the #1C2028 panel. This pins the rule the comment
    always claimed: views set a hue, the stylesheet picks the lightness, and
    each theme picks its own."""
    web = WEB / "views"
    for name in ("lens.js", "bullseye.js", "staging-workbench.js"):
        body = (web / name).read_text(encoding="utf-8")
        for match in re.findall(r"hsl\([^)]*\)", body):
            assert "var(--tint" in match, (name, match)

    css = (WEB / "styles.css").read_text(encoding="utf-8")
    # a light default…
    light = re.search(r"(?m)^:root \{(.*?)\n\}", css, re.S).group(1)
    assert "--tint-l:" in light and "--tint-s:" in light
    # …and BOTH dark paths override it: the media query for the system
    # preference and the attribute for an explicit choice
    for block in (r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\n  \}",
                  r':root\[data-theme="dark"\] \{(.*?)\n\}'):
        body = re.search(block, css, re.S)
        assert body and "--tint-l:" in body.group(1), block


def test_the_rail_search_is_forgiving_but_not_fuzzy(tmp_path):
    """Brett's 2026-08-08 note: "it should be a search, elastic search."
    Every word must appear, in any order, with hyphens read as spaces — a
    controlled vocabulary is full of compounds and the human should not have
    to remember which way round `doc-workflow` goes. Deliberately not fuzzy:
    a typo silently returning the wrong keyword is worse than returning
    nothing, when the result decides what the radar is about."""
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "m.mjs").write_text("""
import { termMatches } from './lens-model.mjs';
const CASES = [
  ['doc-workflow', 'work doc'], ['doc-workflow', 'doc-work'],
  ['doc-workflow', 'WORKFLOW'], ['ideation-dashboard', 'dash'],
  ['doc-management', 'doc management'], ['anything', ''],
  ['doc-workflow', 'xyz'], ['doc-workflow', 'doc xyz'],
  ['doc-workflow', 'dcowrkflow'],
];
console.log(JSON.stringify(CASES.map(([t, q]) => termMatches(t, q))));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "m.mjs")], capture_output=True,
                          text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout) == [
        True,    # out of order
        True,    # hyphen typed as the separator
        True,    # case-insensitive
        True,    # substring of a compound
        True,    # space where the term has a hyphen
        True,    # empty query matches everything
        False,   # no match
        False,   # EVERY word must appear, not any
        False,   # not fuzzy: a scrambled typo finds nothing
    ]


def test_every_custom_property_the_stylesheet_reads_is_one_it_defines():
    """`.sigrid-head` said `background: var(--bg, #fff)` and `--bg` is not a
    token this stylesheet defines, so the FALLBACK took over and painted a
    white bar across the dark theme (Brett, 2026-08-08). An undefined custom
    property does not fail loudly — it silently becomes its fallback, which is
    why this has to be checked rather than noticed."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    defined = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\(\s*(--[a-z0-9-]+)", css))
    # `--h` is set by the VIEWS at render time (the per-term hue), never here
    undefined = read - defined - {"--h", "--cols"}
    assert undefined == set(), undefined


def test_a_button_reset_states_its_own_colour():
    """A <button> does not inherit `color` — it takes the UA's `buttontext`,
    which is black in both themes. A rule that strips a button's background
    without naming its colour therefore ships black text on whatever ground it
    lands on: `.relrow` rendered at contrast 1.18 on the dark panel."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    for block in re.findall(r"(?m)^\.[^{}]*\{[^}]*\}", css):
        if "background: none" not in block or "border: none" not in block:
            continue
        selector = block.split("{")[0].strip()
        assert "color:" in block, selector


def test_the_signature_grid_left_the_lens_and_its_derivation_stayed(tmp_path):
    """Brett, 2026-08-08: "we do not need this in this view… add the room to
    make the viewport to the doc list larger." The grid earned its collapse
    when he asked what value it brought; this pane has since become a DRAFTING
    surface — radar, drafted seed, document list — and even one collapsed row
    costs the list. The derivation stays in the model, unused here, because it
    is correct and tested and the next surface that wants the picture should
    not have to rewrite it."""
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert "matrixGraphic" not in lens
    assert "signatureSummary" not in lens.split("// The SIGNATURE GRID used to sit here")[0]
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    assert "details.gridwrap" not in css

    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "m.mjs").write_text("""
import { signatureSummary } from './lens-model.mjs';
const cells = (bits) => bits.split('').map((b, i) => ({ keyword: 'k' + i, present: b === '1' }));
console.log(JSON.stringify(signatureSummary({ matrix: [
  { document: 'a.md', cells: cells('110') },
  { document: 'b.md', cells: cells('110') },
  { document: 'c.md', cells: cells('101') },
]})));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "m.mjs")], capture_output=True,
                          text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    found = json.loads(proc.stdout)
    assert found["repeatedGroups"] == 1 and found["groups"] == [["a.md", "b.md"]]


def test_the_drafted_panel_is_a_viewport_with_one_title_line(tmp_path):
    """Three annotations of 2026-08-08, all the same economy: this panel sits
    in the pane's most expensive vertical space, so its CHROME is one row and
    everything else is the document.

      * the placement note moved onto the title as a hover ("make this a hover
        popup… that will save some room") — it is read once and re-read
        rarely, and a permanent two-line note costs the viewport under it on
        every single draft;
      * the action moved up to that same line;
      * the panel itself no longer scrolls ("lets make it a viewport and only
        scroll the document inside") — two nested scrollers put the panel's
        own chrome out of reach of the scroll trying to read the text.
    """
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    panel = lens.split("function renderStagingSeed")[1].split("\n}")[0]
    assert 'el("div", "dc-note"' not in panel        # the note is gone…
    assert "title.title = " in panel                  # …and is the title's hover
    assert 'el("div", "dc-acts")' not in panel        # no action row of its own
    # title, action and dismiss all ride the one header
    assert panel.index('head.appendChild(title)') < panel.index("move.addEventListener") \
        < panel.index("head.appendChild(back)")
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    assert ".pane-bullseye .canvas-confirm { flex: none; margin-top: 10px; overflow: visible; }" in css
    assert ".draft-confirm .seedtext { max-height: 300px; overflow: auto;" in css


def test_the_pick_bar_puts_clear_under_the_checkboxes_and_the_action_in_the_middle():
    """Brett, 2026-08-08: "move this under the checkboxes. label it clear #",
    and "the doc is drafted. this should be Re-Draft. Also move this to center
    on the bottom line."

    The count was a separate sentence beside a bare `clear`; on the button it
    is both the number and the way to undo it, in one control, positioned
    under the column it undoes. The draft action is centred because it is the
    one thing the bar is for — and it says `re-draft` over a draft that
    already exists, rather than implying a second, separate seed.
    """
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    bar = lens.split("function pickBar")[1].split("\n}")[0]
    assert 'n ? "clear " + n : "clear"' in bar
    assert 'ctx.hasDraft() ? "re-draft" : "draft staging seed"' in bar
    # clear first (left), then the action, then the hint — the DOM order the
    # three-cell grid positions
    assert bar.index("clear.type") < bar.index("draft.type") < bar.index('"pickn"')
    # a label whose length changes must not drag the centre: a three-cell grid,
    # not a flex row
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    pick = re.search(r"\.pickbar \{(.*?)\n\}", css, re.S).group(1)
    assert "grid-template-columns: 1fr auto 1fr" in pick
    assert ".pickbar > .cbtn:first-child { justify-self: start; }" in css
    # and the bar re-renders when a draft lands or is dismissed, or the label
    # would still read `draft` over an existing one
    assert "redraw() { draw(); }" in lens
    assert "if (ctx && ctx.redraw) ctx.redraw();" in lens


def test_every_view_of_a_document_publishes_the_same_key():
    """Brett, 2026-08-08: "when I hover on one of these documents, the
    corresponding dot should light up." Three renderers draw the same document
    — the radar's dot, the matrix's row, the grid's row — and the reader was
    joining them by eye. Each publishes `data-doc`; ONE delegated listener in
    the pane does the lighting, so no renderer knows about any other and a
    redraw cannot strand a listener."""
    bullseye = (WEB / "views" / "bullseye.js").read_text(encoding="utf-8")
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert '"data-doc": String(d.document)' in bullseye
    assert "tr.dataset.doc = r.document" in lens        # the matrix row
    # (the signature grid was the third view and has since left this pane;
    # the join is written over `[data-doc]`, so it covers however many views
    # publish the key rather than a fixed list of them)
    assert 'pane.querySelectorAll("[data-doc]")' in lens
    # one delegated pair on the pane, not per-row listeners
    assert lens.count('pane.addEventListener("pointerover"') == 1
    assert lens.count('pane.addEventListener("pointerout"') == 1
    # a document id is a PATH: `/` and `.` are selector syntax, so it must be
    # escaped before it goes into querySelectorAll
    assert "cssEscape(doc)" in lens
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    for rule in ("tr.lit > td", ".bullseye .lensdot.lit .dot"):
        assert rule in css, rule


def test_the_matrix_selection_is_the_seeds_only_input():
    """The checkbox column exists to feed ONE action, and the action names only
    the documents: the route recomputes their terms from its own snapshot, so
    the client cannot assert a convergence the corpus does not have."""
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert 'STAGING_SEED_ROUTE = "/actions/staging-seed"' in lens
    # the request carries documents and the project — never terms or evidence
    body = re.search(r"postPlan\(STAGING_SEED_ROUTE, \{(.*?)\}, fetcher\)",
                     lens, re.S).group(1)
    assert "documents:" in body and "project_id:" in body
    for forbidden in ("shared", "topics", "keywords", "text"):
        assert forbidden + ":" not in body, forbidden
    # this view still holds no network primitive of its own
    for primitive in ("fetch(", "XMLHttpRequest", "navigator.sendBeacon"):
        assert primitive not in lens, primitive


def test_the_hovered_dot_pulses_and_the_selected_dot_has_its_own_colour():
    """Brett, 2026-08-08: "we need more for the hover over doc. lets try
    making the dot pulse… if I do check boxes, those dots need to change
    color." Two different jobs. The pulse is a MOMENTARY cue — a ring of 32
    identical circles is a field the eye has to search, and motion is the one
    channel it locates without searching. The colour is a STANDING state that
    must read with no pointer anywhere near it."""
    css = (WEB / "styles.css").read_text(encoding="utf-8")

    # the pulse: opacity, not size — the packing put these dots as close as
    # they can legibly sit, so a dot that grew would touch its neighbours
    pulse = re.search(r"@keyframes lensdot-pulse \{(.*?)\n\}", css, re.S).group(1)
    assert "opacity" in pulse and "transform" not in pulse and "r:" not in pulse
    assert "animation: lensdot-pulse" in css
    # …and it is OPTIONAL: the lit dot still carries its outline and bold
    # label, so a reader who has asked for less motion loses nothing
    reduce = re.findall(r"@media \(prefers-reduced-motion: reduce\) \{(.*?)\n\}",
                        css, re.S)
    assert any("lensdot.lit .dot { animation: none" in block for block in reduce)

    # the selection colour is its OWN token, defined in every theme block.
    # It was first drawn in `--edge-pick`, which is the same teal as
    # `--st-staged`: measured rgb(31,168,152) for both a selected and an
    # unselected dot, i.e. no change at all.
    assert "--picked:" in css
    assert css.count("--picked:") >= 3          # :root + both dark paths
    assert ".bullseye .lensdot.picked .dot" in css
    for line in re.findall(r"(?m)^\s*--picked: (\S+);", css):
        assert line != "#0D9488" and line != "#1FA898", line
    # and the selection reads the same in all three views, like the hover does
    for rule in (".lensmatrix tr.picked", ".sigrid-row.picked"):
        assert rule in css, rule

    # the mark is applied by the LENS over the whole pane — the bullseye
    # renders a membership model and knows nothing about a selection
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert 'node.classList.add("picked")' in lens
    assert "picked" not in (WEB / "views" / "bullseye.js").read_text(encoding="utf-8")


def test_the_drafted_seed_moves_to_doxbench_instead_of_being_copied(tmp_path):
    """Brett, 2026-08-08: "we need to not 'copy' this. we need to have button
    to move this to doxBench. and open the doxBench UI if the user moves
    forward." Copying makes the HUMAN the transport — paste it somewhere, keep
    the topic and the terms straight by hand. The seed travels instead, as a
    prefilled CREATE, and only what was COMPUTED crosses: the staging area,
    the shared terms, the provenance. Title and summary stay empty because the
    create refuses without them, which is the same rule the seed states by
    marking them TO WRITE."""
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert "navigator.clipboard" not in lens.split("renderStagingSeed")[1].split(
        "createSeedFromStagingSeed")[0]
    assert "open in doxBench" in lens
    assert "ctx.onOpenDoxbench(data)" in lens
    # app.js owns the jump, exactly as it does for every other cross-view verb
    app = (WEB / "app.js").read_text(encoding="utf-8")
    assert "openDraft: (seed) => stagingWorkbench.openDraft(seed)" in app
    assert "onOpenDoxbench: ctx.nav.openDraft" in app
    # and the workbench reuses the GOVERNED create — no second write path and
    # no second session concept, so save/abandon behave as they always have
    swb = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    assert "function openDraft(seed)" in swb
    # the create dialog now lives on the draft view's `details` tab rather than
    # filling the overlay body (see the draft-view test below)
    assert "openCreateDialog(pane, seed" in swb
    assert "return { open, close, openDraft };" in swb
    # an ungated plane says so rather than offering a submit that cannot land
    draft_body = swb.split("function openDraft(seed)")[1].split("\n  }")[0]
    # the SERVE's posture, not the composed view's projection
    assert "createGateLive(authoring)" in draft_body

    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WEB / "views" / "lens.js", tmp_path / "lens.mjs")
    for dep in ("lens-model.js", "bullseye.js", "composed-model.js"):
        shutil.copy(WEB / "views" / dep, tmp_path / dep)
    (tmp_path / "m.mjs").write_text("""
import { createSeedFromStagingSeed } from './lens.mjs';
const seed = createSeedFromStagingSeed({
  path: 'ideation/staging/doc-workflow/doc-workflow.md',
  shared: ['doc-workflow', 'governance'], partial: ['lens'],
  documents: ['a.md', 'b.md'], text: '# Staged: TO WRITE',
}, 'openxFactory');
const noShared = createSeedFromStagingSeed({
  path: 'ideation/staging/x/x.md', shared: [], partial: ['only-some'],
  documents: ['a.md'],
}, 'openxFactory');
console.log(JSON.stringify([seed, noShared]));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "m.mjs")], capture_output=True,
                          text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    seed, no_shared = json.loads(proc.stdout)
    assert seed["area"] == "ideation/staging/doc-workflow/"
    assert seed["topics"] == ["doc-workflow", "governance"]
    assert seed["status"] == "staged"          # never born ratified
    assert seed["kind"] == "capability-proposal"
    assert seed["repository"] == "openxFactory"
    assert "2 documents" in seed["source"]
    # Title and Summary now carry DEFAULTS (Brett, 2026-08-09) — see
    # `test_every_create_field_carries_a_default_so_nothing_blocks_the_create`
    # for what they derive from and why the summary is marked.
    assert seed["title"] == "doc-workflow + governance"
    assert seed["summary"].startswith("TO WRITE — ")
    # with no shared spine, the partial terms carry the topics rather than
    # leaving a create that would be refused for having none
    assert no_shared["topics"] == ["only-some"]


def test_the_drafted_seed_panel_sits_under_the_radar_and_can_be_dismissed():
    """Brett, 2026-08-08: "there is no back from this widget. this widget
    should move up to the bottom of the radar." It began as a full-width block
    below the whole three-pane layout; the foot of the bullseye pane was no
    better (measured 2,772px down, past the entire matrix). It belongs
    directly under the radar, where the eye already is — and it must be
    dismissable, because a panel that can only be replaced by drafting
    something else is a panel the human is stuck in."""
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    # mounted by the PANE, not by the view root
    assert "root.appendChild(confirm)" not in lens
    assert "if (ctx.confirmHost) pane.appendChild(ctx.confirmHost);" in lens
    # …directly after the radar, before the grid and the matrix
    pane = lens.split("function bullseyePane")[1]
    order = [pane.index("renderBullseye"), pane.index("ctx.confirmHost"),
             pane.index("matrix(model")]
    assert order == sorted(order), order
    # dismissing costs nothing: nothing was written, and the same selection
    # drafts it again byte for byte
    assert 'el("button", "dc-close"' in lens
    assert "dismiss this draft" in lens
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    assert ".pane-bullseye .canvas-confirm" in css
    assert ".pane-bullseye .canvas-confirm:empty { display: none; }" in css


def test_the_doxbench_handoff_is_offered_only_where_it_can_land():
    """Brett, 2026-08-08: "i added some docs to the seed and did a draft. then
    clicked open in doxBench. but it was blank."

    The cause was mine and it was a DEAD END, not a rendering fault. A project
    view is a read-only projection — `readOnlyCaps` strips gate/session/edit
    by design, because there is no such thing as writing to "a project", only
    to one of its member repositories. The button was offered there anyway and
    refused after the click, in an otherwise empty overlay.

    A dead end discovered at the last step is worse than one declared at the
    first, so the decision moved to where the button is drawn, and it has
    three outcomes rather than two:

      * the plane can create        -> the button
      * exactly ONE repository owns the selection -> the JUMP to it, because
        one owner is a destination, not a decision
      * SEVERAL own it             -> the reason, naming them, because which
        repository owns a NEW document is the human's call and not a click
        the machine can make for them
    """
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    panel = lens.split("function renderStagingSeed")[1].split("\n}")[0]
    # the offer is conditional on the capability, not attempted and refused
    assert "ctx.onOpenDoxbench && ctx.canCreate" in panel
    assert "owners.length === 1" in panel and "ctx.onOpenRepository" in panel
    assert "dc-why" in panel
    # the three branches are exclusive and ordered: create, jump, explain
    assert panel.index("ctx.canCreate") < panel.index("owners.length === 1") \
        < panel.index('el("span", "dc-why"')
    # the capability read is the gate, and the owners come from the COMPOSED
    # snapshot the lens already holds — no new fetch to answer either question
    assert "canCreate: !!(createCaps && createCaps.actions" in lens
    assert "ownersOf(documents)" in lens
    for primitive in ("fetch(", "XMLHttpRequest", "navigator.sendBeacon"):
        assert primitive not in lens, primitive
    # app.js owns the jump, as it owns every other cross-view move
    app = (WEB / "app.js").read_text(encoding="utf-8")
    assert "onOpenRepository: ctx.nav.openRepository" in app
    # …and the overlay's own guard still says something true and actionable
    # rather than rendering empty, since reaching it is now a programming error
    swb = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    guard = swb.split("function openDraft(seed)")[1].split("\n  }")[0]
    assert "created IN a repository" in guard
    assert "nothing was lost" in guard


def test_the_serve_declares_the_repository_it_can_write_to():
    """Brett, 2026-08-08: "yes, we need to draft from a project view."

    A project view is composed, and `readOnlyCaps` strips every acting
    capability from it — correctly for a TILE-BOUND verb, whose repository
    this serve has no writable checkout for. Creating a new document binds to
    no tile: it lands in the serve's own checkout. So one affordance reads the
    SERVE's capability rather than the VIEW's projection.

    For that it must know which repository the serve writes to, and it must
    not GUESS: under a composed view the rendered snapshot's `repository` is
    the PROJECT id, which names no repository and is refused by
    `refuse_foreign_repository`. The serve declares it instead, from the same
    authority the refusal uses, so the two cannot disagree.
    """
    serve = (REPO_ROOT / "scripts" / "ideation_dashboard" / "serve.py").read_text(
        encoding="utf-8")
    caps_route = serve.split("if path == CAPABILITIES_ROUTE:")[1].split(
        "if path == WORKBENCH_MODEL_CATALOG_ROUTE:")[0]
    assert "self._session_repository()" in caps_route
    assert 'payload["repository"]' in caps_route
    # a copy, never a mutation of the shared capability dict
    assert "dict(self.capabilities)" in caps_route

    app = (WEB / "app.js").read_text(encoding="utf-8")
    assert "writableRepository: probedCaps?.repository || null" in app
    # the UNSTRIPPED probe reaches exactly two consumers: the lens's hand-off
    # (through the tab context) and the workbench's openDraft (direct)
    assert "createCaps: ctx.probedCaps" in app
    assert "createCaps: probedCaps" in app
    assert app.count("createCaps:") == 2

    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert "createCaps && createCaps.actions && createCaps.actions.gate" in lens
    assert "&& writableRepository" in lens
    # the create names the DECLARED repository, never the view's own
    assert "createSeedFromStagingSeed(data, writableRepository || repository)" in lens

    swb = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    draft = swb.split("function openDraft(seed)")[1].split("\n  }")[0]
    assert "const authoring = createCaps || caps;" in draft
    assert "createGateLive(authoring)" in draft
    assert "caps: authoring" in draft
    # …and only openDraft: every tile-bound surface keeps the stripped caps
    assert swb.count("createCaps") <= 3


def test_a_dot_is_its_documents_checkbox():
    """Brett, 2026-08-09: "when I click a dot. make it work like checking the
    box on the doc. turn it red and check the box in the list."

    The radar is where a convergence is READ, so it should be where the
    selection is MADE. Both write the same `pickDoc`, so the dot's colour and
    the row's tick are one state rendered twice and cannot disagree — which is
    the whole reason not to give the dot a selection of its own.
    """
    renderer = BULLSEYE_JS.read_text(encoding="utf-8")
    # the renderer publishes a seam; it holds no selection and knows no lens
    assert "const onDocument = typeof o.onDocument === \"function\"" in renderer
    assert "onDocument(String(d.document))" in renderer
    # a dot click must not also fire the region beneath it, which drills in
    dot = renderer.split("if (onDocument) {")[1].split("}")[0]
    assert "ev.stopPropagation()" in dot
    # …and it stays ignorant of what a selection IS: no state, no class, no
    # notion of picked-ness anywhere in the widget (prose may discuss the
    # checked keyword set — that is the model's vocabulary, not a selection)
    code = "\n".join(ln for ln in renderer.splitlines()
                      if not ln.lstrip().startswith("//"))
    for word in ("picked", "isPicked", "selection"):
        assert word not in code, word

    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert "bullseyeOpts.onDocument = (doc) => ctx.pickDoc(doc, !ctx.isPicked(doc))" in lens
    # the KEYBOARD path stays the matrix checkbox: 95 focusable dots would
    # flood the tab order to no benefit, and the box is already reachable
    assert 'box.setAttribute("aria-label", "select " + r.document)' in lens


def test_a_staged_tile_opens_its_packet_rather_than_repointing_the_dashboard():
    """Brett, 2026-08-09: "from a staged tile I click open in <repo>, it
    reloads the doxBench in that repo. it should not do that. it should just
    load the workBench with that staging packet."

    A staged TOPIC is not repository-shaped the way a document tile is: it is
    a packet whose material can span members, and what a human wants from it
    is the packet. `open workbench` already gives exactly that, scoped, on a
    composed view (verified live) — with no reload and no repointing of the
    whole dashboard. Offering both put the heavier, wrong move beside the
    right one, so the jump leaves the staged wheel and stays everywhere its
    tile IS one repository's document.
    """
    model = (WEB / "views" / "wheel-model.js").read_text(encoding="utf-8")
    staged = model.split("  staged: [")[1].split("\n  ],")[0]
    code = "\n".join(ln for ln in staged.splitlines()
                      if not ln.lstrip().startswith("//"))
    assert "workbenchRow" in code
    assert "openRepoRow" not in code
    # …and every other wheel keeps it
    for wheel in ("documents", "clusters", "possibles"):
        block = model.split("  " + wheel + ": [")[1].split("\n  ],")[0]
        assert "openRepoRow" in block, wheel


def test_a_reload_bearing_control_returns_you_to_the_view_you_were_on():
    """Brett, 2026-08-09: "can we make the repo jump silent on the other
    wheels? currently we take the user back to home page and the user must
    drill back to where they were."

    FIVE controls store a key and reload — the repository jump, the
    repository/project selector, a refresh, and clearing a drill-in — and
    every one of them landed on the first tab. A jump taken FROM the wheel
    arrived on the funnel, so the human re-navigated to the place they had
    just been looking at.

    The TAB is the right thing to keep, and the only thing: after a repository
    jump the tile you were on does not exist in the repository you jumped to,
    which is the point of jumping. Restoring the view puts you where you were
    looking; restoring a tile would restore something that is gone.
    """
    app = (WEB / "app.js").read_text(encoding="utf-8")
    # remembered on EVERY activation, so it is right however the tab changed —
    # a click, a keyboard arrow, or a programmatic `goto` from a wheel verb
    assert "storeTab(target.view);" in app
    show = app.split("function show(target, focusTab) {")[1].split("\n  }")[0]
    assert "storeTab" in show
    # …and restored only to a view this plane actually has
    assert "const remembered = TABS.find((t) => t.view === storedTab());" in app
    assert "show(remembered || TABS[0], false);" in app
    # through the SAME guarded seam every other stored preference uses: under
    # blocked site data the getter itself throws, and a preference that cannot
    # be stored is not an error
    tab_helpers = app.split("function storedTab()")[1].split("function initTabs")[0]
    assert tab_helpers.count("guardedSessionStorage()") == 2
    assert tab_helpers.count("try {") == 2


def test_a_switch_re_renders_in_place_and_leaves_no_listener_behind():
    """Brett, 2026-08-09: "yes, get rid of the flash too."

    Five controls used to store a key and reload the page. Re-rendering in
    place instead means every listener and observer a render installs must
    come OFF before the next one goes on — otherwise the second Escape press
    runs two handlers, the third runs three, and the leak grows with every
    switch a human makes.

    ONE AbortController per render is the whole mechanism: everything a render
    binds passes `{ signal }`, and starting the next render aborts the last.
    A view needs no `destroy()` — it honours the signal it is handed. This
    pins that rule, because it is a rule that cannot be half-applied: an
    unscoped listener leaks silently and only shows up as a handler running
    twice, long after the change that caused it.
    """
    app = (WEB / "app.js").read_text(encoding="utf-8")
    # the shell re-renders rather than navigating
    assert "window.location.reload()" not in app
    assert "function nextRenderScope()" in app
    scope = app.split("function nextRenderScope()")[1].split("\n}")[0]
    assert "renderScope.abort()" in scope and "new AbortController()" in scope
    assert "const signal = nextRenderScope();" in app

    # every module that binds OUTSIDE its own root honours the signal
    def bindings(text):
        """Each `document.addEventListener(...)` call, whole — a handler body
        holds its own `);`, so the arguments have to be read by matching
        parentheses rather than by a lazy regex."""
        out, needle = [], "document.addEventListener("
        i = text.find(needle)
        while i != -1:
            j, depth = i + len(needle) - 1, 0
            while j < len(text):
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            out.append(text[i:j + 1])
            i = text.find(needle, j)
        return out

    for name, expected in (("wheel.js", 3), ("explorer.js", 1),
                           ("staging-workbench.js", 1)):
        body = (WEB / "views" / name).read_text(encoding="utf-8")
        binds = bindings(body)
        assert len(binds) == expected, (name, len(binds))
        for bind in binds:
            assert "{ signal }" in bind, (name, bind[:90])

    # an observer outlives listeners unless something disconnects it
    for name in ("wheel.js", "funnel.js"):
        body = (WEB / "views" / name).read_text(encoding="utf-8")
        if "new ResizeObserver" in body:
            assert 'signal?.addEventListener("abort"' in body, name

    # the settings gear stays bound ONCE for the life of the page: it owns no
    # snapshot state, so a re-render must not rebind it (and must not unbind it)
    assert "initSettings();" in app.split("async function render()")[0]
    assert "initSettings" not in app.split("async function render()")[1]


def test_the_vocabulary_switch_states_its_counts_and_abbreviates_when_squeezed():
    """Brett, 2026-08-09: "in the lens screen we lost our keyword/repo
    selector… these buttons could state the number of that item in the button
    '134 Keywords' and '3 Repositories'. if the screen estate is too small,
    then abbreviate to 134 KW and 3 Repos."

    The switch was there — on a multi-repository project, where both
    vocabularies mean something — but two bare lowercase words in a header are
    easy to miss entirely. The COUNT is what makes the pair read as a choice
    between two vocabularies, and it answers "how much is over there?" before
    you switch to find out.
    """
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    # each vocabulary owns both spellings, beside its other words
    for word in ('termsTitle: "Keywords"', 'termsShort: "KW"',
                 'termsTitle: "Repositories"', 'termsShort: "Repos"'):
        assert word in lens, word
    # the counts come from each vocabulary's OWN source — the declared keyword
    # index, and the composed view's members
    assert "keywords: (snapshot?.keyword_index || []).length" in lens
    assert "repositoryVocabulary(composed).keyword_index || []" in lens
    # both spellings ride on the button, so the choice is a text swap and never
    # a re-render
    assert "btn.dataset.full" in lens and "btn.dataset.short" in lens

    # WHICH ONE FITS IS MEASURED, not guessed from a character count: the width
    # depends on the theme's font and the reader's zoom
    fit = lens.split("function fitVocabSwitch(root)")[1].split("\n}")[0]
    assert "head.scrollWidth > head.clientWidth" in fit
    assert "dataset.full" in fit and "dataset.short" in fit
    # …and it runs on every draw, after the panes are in the DOM — a width is
    # not knowable before then
    draw = lens.split("function draw()")[1].split("\n  }")[0]
    assert "fitVocabSwitch(lens)" in draw
    assert draw.index("appendChild") < draw.index("fitVocabSwitch")

    # the measurement needs a single nowrap row to overflow
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    assert ".pane-rail .pane-h { flex-wrap: nowrap; overflow: hidden; }" in css
    assert "white-space: nowrap" in css.split(".vocabswitch {")[1].split("}")[0]

    # the count chip is GONE: the buttons carry the counts, so it repeated one
    # of the two and competed for the width that decides the spelling
    rail = lens.split("function keywordRail(model, ctx)")[1].split("\n}")[0]
    head = rail.split("const h = el(\"div\", \"pane-h\")")[1].split("pane.appendChild(h)")[0]
    assert "vocab.railCount" not in head
    assert "ctx.vocabularies()" in head


def test_the_vocabulary_switch_is_on_every_plane_and_says_why_when_it_cannot_switch():
    """Brett, 2026-08-09: "this widget is where we should select the Keyword vs
    Repo and just made the buttons that will abbreviate when needed. but I do
    not see those buttons."

    The switch used to render only where BOTH vocabularies had something to
    say, which meant it vanished from every single-repository view — two of
    the six projects in the register — and a control that comes and goes is a
    control a human cannot learn to look for.

    It is now unconditional. Where there is no member set, the repository
    button is OFFERED and DISABLED with the reason on it rather than hidden:
    `1 Repository` is a fact worth stating, and a lens over one member would
    draw every document in a single ring and compare nothing.
    """
    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    # built unconditionally — no `composed ? … : null`
    assert "const vocabularies = () => {" in lens
    assert "const vocabularies = composed ?" not in lens
    # a one-repository view still counts ONE, and says why it cannot switch
    assert "? (repositoryVocabulary(composed).keyword_index || []).length : 1" in lens
    assert 'const unavailable = candidate.id === "repositories" && !composed;' in lens
    assert "there is no member set to lens" in lens
    # unavailable must not look the same as "this is the current vocabulary"
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    assert ".vocabbtn:disabled:not(.vocabon)" in css
    # …and `1 Repositories` is the kind of detail that makes a surface feel
    # machine-written, on a case this control now renders on every load
    for word in ('termsOne: "Keyword"', 'termsOne: "Repository"',
                 'termsShortOne: "Repo"'):
        assert word in lens, word
    assert "n === 1 ? candidate.termsOne : candidate.termsTitle" in lens


def test_the_draft_view_lands_on_an_editable_body_with_its_fields_behind_a_tab():
    """Brett, 2026-08-09: "go direct in to let the user start working on the
    doc", then "do the create-then-edit so I can write the body".

    The draft view opens on the BODY, editable, with the header fields on a
    `details` tab. Creating runs both governed verbs as one action: the create
    opens the branch session for this topic's scope and lands the header, and
    the edit resolves that same live session and writes the body over it.

    The scope is what makes the second verb reachable, and it needed no new
    contract: `firstEditBody` already carries `scope_kind`/`scope_id` off the
    save key, and the staging seed had computed the name from the start. My
    first reading — that a lens draft could never reach `edit-document` — was
    wrong, and wrong in the direction of proposing a contract change that was
    not needed.
    """
    swb = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    draft = swb.split("function openDraft(seed)")[1]
    assert '{ id: "document", label: "document" }' in draft
    assert '{ id: "details", label: "details" }' in draft
    assert 'showPane("document");' in draft          # the document is what opens
    assert 'el("textarea")' in draft or 'createElement("textarea")' in draft
    assert "bodyText = area.value" in draft          # …and it is editable

    # the HEADER is not offered for editing: the create regenerates it, so an
    # edit of it would be an edit that is discarded
    assert 'seedText.indexOf("\\n## ")' in draft

    # create-then-edit, through the EXISTING save seam — no new transport
    assert "seams.save({" in draft
    assert 'tile_kind: "staged"' in draft
    assert "tile_id: seed.scopeId" in draft
    assert "loaded.content" in draft                 # the created header survives
    # a body that fails after the header lands says exactly that
    assert "the document was created, but its body was refused" in draft

    lens = (WEB / "views" / "lens.js").read_text(encoding="utf-8")
    assert 'scopeKind: "staged-topic"' in lens
    assert "scopeId: String(data?.staging_id" in lens
    # the id is RETURNED by the drafter, not parsed out of the fragment's prose
    seed_py = (REPO_ROOT / "scripts" / "doc_health" / "staging_seed.py").read_text(
        encoding="utf-8")
    assert '"staging_id": self.staging_id' in seed_py


def test_every_create_field_carries_a_default_so_nothing_blocks_the_create(tmp_path):
    """Brett, 2026-08-09: "default the name to the concatenation of the
    keywords… or the first word of each doc if the docs and repo view… for
    topics, if no intersection then list the same keywords as the title. does
    this now get us defaults for all?"

    It does. Title, Topics and Summary all derive from ONE set of terms, so
    they cannot describe different things, and with Area/Status/Kind already
    seeded nothing is left empty for the create to refuse.

    The summary carries the `TO WRITE` marker at Brett's instruction: the field
    is filled so the create is never blocked, and the marker keeps it honest,
    because doc-health reads a summary as a completeness signal and a derived
    one that read hand-written would quietly inflate the corpus's own health.
    """
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    for dep in ("lens-model.js", "bullseye.js", "composed-model.js"):
        shutil.copy(WEB / "views" / dep, tmp_path / dep)
    shutil.copy(WEB / "views" / "lens.js", tmp_path / "lens.mjs")
    (tmp_path / "m.mjs").write_text("""
import { createSeedFromStagingSeed, selectionTerms } from './lens.mjs';
const shared = createSeedFromStagingSeed({
  path: 'ideation/staging/doc-workflow/doc-workflow.md',
  shared: ['doc-workflow', 'governance'], partial: [],
  documents: ['a.md', 'b.md'],
}, 'openxFactory');
const untagged = createSeedFromStagingSeed({
  path: 'ideation/staging/x/x.md', shared: [], partial: [],
  documents: ['docs/document-catalog-adoption.md', 'docs/README.md'],
}, 'openxFactory');
console.log(JSON.stringify([shared, untagged,
  selectionTerms({ shared: [], partial: ['only-some'], documents: ['z.md'] })]));
""", encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "m.mjs")], capture_output=True,
                          text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    shared, untagged, partial_terms = json.loads(proc.stdout)

    # SHARED TERMS name the document, its topics, and its summary
    assert shared["title"] == "doc-workflow + governance"
    assert shared["topics"] == ["doc-workflow", "governance"]
    assert shared["summary"].startswith("TO WRITE — doc-workflow + governance:")
    assert "2 documents" in shared["summary"]

    # NO INTERSECTION falls back to the first word of each document's basename,
    # which is all a repository selection has to offer
    assert untagged["title"] == "document + README"
    assert untagged["topics"] == ["document", "README"]
    assert untagged["summary"].startswith("TO WRITE — document + README:")

    # a partial intersection is preferred over the filenames
    assert partial_terms == ["only-some"]

    # …and nothing the create refuses is left empty
    for field in ("title", "summary", "topics", "area", "status", "kind"):
        assert untagged[field], field
