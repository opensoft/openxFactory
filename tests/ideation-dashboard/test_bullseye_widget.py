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
    // the names the numbers stand for: each dot circle's own <title> child
    dotTitles: nodes.filter((n) => (n.cls || '').startsWith('dot'))
      .map((n) => (n.node.children[0] || {}).text || null),
    sectorLabels: nodes.filter((n) => n.cls === 'seclab').map((n) => n.text),
    model: {
      rings: model.rings.length, sectors: model.sectors.length,
      dots: model.dots.length, checked: model.checked,
      centreRadius: (model.rings.find((r) => r.isCenter) || {}).outerRadius,
      dotRows: model.dots.map((d) => d.row),
      dotColumns: model.dots.map((d) => d.column),
      dotNumbers: model.dots.map((d) => d.number),
      dotCells: model.dots.map((d) => d.subsetKey),
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
    assert r["counts"]["sectorLabels"] == r["model"]["sectors"]
    assert r["counts"]["dots"] == r["model"]["dots"] == 3
    # exactly ONE shaded centre zone, labelled "all N ✓"
    assert r["counts"]["centreRings"] == 1
    assert "all 2 ✓" in r["labels"]
    # The dots carry their matrix NUMBER, not the document name (Brett's
    # 2026-08-07 ruling: names are too large for the radar). The name is not
    # lost — it stays in the dot's <title> and in the numbered matrix beside
    # the widget, which is the legend the numbers index.
    assert set(r["docLabels"]) == {"1", "2", "3"}
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

    # exactly ONE wiring in the lens, and it passes nothing when un-gated
    assert lens.count("onActivate") == 1, "the lens tab wires the handler once"
    assert "ctx.onDrill ? { onActivate: ctx.onDrill } : undefined" in lens, (
        "the keyword vocabulary must still pass NO opts — an undefined second "
        "argument is what keeps its regions inert")
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
    """Brett's 2026-08-07 ruling: "the keywords and doc names are too large to
    be putting on the radar screen — number the keywords and docs, then just
    put the number on the radar." The numbers are short enough that the
    collision machinery stops dropping labels, which is the whole point: at
    corpus scale the old names were either clipped or silently omitted."""
    r = _render(tmp_path)["two-checked"]
    # every dot is labelled, by number — nothing is dropped for width now
    assert sorted(r["docLabels"], key=int) == ["1", "2", "3"]
    assert len(r["docLabels"]) == r["counts"]["dots"]
    # sectors are labelled by the keywords' RAIL numbers, not their names
    for label in r["sectorLabels"]:
        assert re.fullmatch(r"\d+( ∧ \d+)*", label), label
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
import { packCell, DOT_GAP, DOT_R, DOT_MIN_R } from './lens-model.mjs';
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
console.log(JSON.stringify({ out, DOT_GAP, DOT_R, DOT_MIN_R }));
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
        assert r["DOT_MIN_R"] <= case["size"] <= r["DOT_R"], case
        # labels alternate above/below wherever there is more than one dot
        assert case["slots"] == ([0] if case["n"] == 1 else [0, 1]), case

    by_n = {c["n"]: c for c in r["out"]}
    # a roomy cell keeps FULL-SIZE dots rather than shrinking pre-emptively
    assert by_n[6]["size"] == r["DOT_R"] and by_n[6]["rows"] == 1
    # a deep band uses its depth: the single-keyword case stacks rows
    assert by_n[60]["rows"] > 1 and by_n[60]["size"] == r["DOT_R"]
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
    assert 0 < len(r["docLabels"]) <= eligible
    # the inboard dots are still DRAWN and still name themselves on hover
    assert len(r["dotTitles"]) == 31
    assert all(t and ".md" in t for t in r["dotTitles"])
