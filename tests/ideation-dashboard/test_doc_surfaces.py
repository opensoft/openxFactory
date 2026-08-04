"""The two corpus-WIDE document surfaces, at corpus SCALE (T092 acceptance
sweep, defects 7 and 15).

Python-side only — no browser automation: the ACTUAL `views/docs.js` and
`views/lineage.js` run in node against a minimal HTML DOM stub (skipped when
node is absent), exactly as `test_bullseye_widget.py` runs the real bullseye
against an SVG stub. Both modules import `views/helpers.js`, so the harness
copies that too and the modules stay unmodified.

WHY THE CORPUS HERE IS BIG AND MULTI-TOPIC. Both defects are invisible on the
committed smoke's two-document, one-topic world by construction:

  * defect 7 (the doc list is inert) is a per-ROW affordance, and nobody clicks
    a row in a world with two of them — the sweep found it on 177;
  * defect 15 (the DOCUMENTS stat tile's sub-line does not sum to its headline)
    needs stages OUTSIDE draft/staged/brainstorm to exist at all. On a fixture
    whose documents are all brainstorm-stage the hardcoded three-stage sub-line
    is accidentally complete, and the bug cannot appear.

So `_scale_snapshot()` builds the real corpus's own shape: 177 documents across
five staging topics and the brainstorm area, with the sweep's measured
eight-stage distribution (draft 65 · brainstorm 39 · staged 32 · record 20 ·
ratified 12 · standard 6 · superseded 2 · retired 1). The arithmetic assertions
below are on the WHOLE distribution, not on the three stages that used to be
hardcoded, so re-hardcoding any subset fails here.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
DOCS_JS = WEB / "views" / "docs.js"
LINEAGE_JS = WEB / "views" / "lineage.js"
HELPERS_JS = WEB / "views" / "helpers.js"
STYLES_CSS = WEB / "styles.css"
APP_JS = WEB / "app.js"
NODE = shutil.which("node")

# The sweep's measured distribution on openxFactory main at 88284e3 — 177
# documents, eight stages, of which only three were ever named by the stat tile.
STAGE_TALLY = {
    "draft": 65, "brainstorm": 39, "staged": 32, "record": 20,
    "ratified": 12, "standard": 6, "superseded": 2, "retired": 1,
}
TOPICS = ("avatar-pilot-hardening", "qualify-avatar-live-voice",
          "client-layer-tuning", "client-credential-escrow-registry",
          "doc-health-followups")

# A minimal HTML DOM: enough for helpers.el + the two views (createElement,
# createTextNode, className/textContent/title/tabIndex, classList.add,
# setAttribute, appendChild, addEventListener, and the literal `innerHTML = ""`
# clear both views use). Every node records what was set on it so the harness
# can report the tree as JSON — and, crucially, KEEPS its handlers so a row can
# actually be activated rather than merely inspected for wiring.
_NODE_HARNESS = """
function makeNode(tag) {
  return {
    tag, className: '', text: null, attrs: {}, classes: [], children: [],
    events: [], handlers: {}, tabIndex: undefined, title: undefined, value: '',
    classList: { add(c) { this.owner.classes.push(c); } },
    setAttribute(k, v) { this.attrs[k] = String(v); },
    appendChild(child) { this.children.push(child); return child; },
    addEventListener(type, fn) { this.events.push(type); this.handlers[type] = fn; },
    set innerHTML(v) {
      if (v !== '') throw new Error('innerHTML assigned a non-empty string: ' + v);
      this.children.length = 0;
    },
    get innerHTML() { return ''; },
    set textContent(v) { this.text = v; },
    get textContent() { return this.text; },
  };
}
globalThis.document = {
  createElement(tag) {
    const node = makeNode(tag);
    node.classList.owner = node;
    return node;
  },
  createTextNode(s) { const n = makeNode('#text'); n.text = String(s); return n; },
};
const { renderDocs } = await import('./docs.js');
const { renderStats } = await import('./lineage.js');
import { readFileSync } from 'node:fs';

function flatten(node, out) {
  out.push(node);
  for (const child of node.children) flatten(child, out);
  return out;
}
function classesOf(node) {
  return String(node.className || '').split(' ').filter(Boolean).concat(node.classes);
}
function textOf(node) {
  return flatten(node, []).map((n) => n.text).filter((t) => t != null).join(' ');
}
function rowsOf(root) {
  return flatten(root, []).filter((n) => classesOf(n).includes('docrow'));
}
function describeRow(row) {
  return {
    classes: classesOf(row), role: row.attrs.role || null,
    tabIndex: row.tabIndex === undefined ? null : row.tabIndex,
    title: row.title === undefined ? null : row.title,
    events: row.events.slice(),
  };
}

const snapshot = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const EV = { preventDefault() {} };
const out = {};

// --- wired: every row opens the read-only viewer -----------------------------
const opened = [];
const wiredRoot = document.createElement('div');
renderDocs(wiredRoot, snapshot, { onOpenDoc: (path, doc) => opened.push([path, doc && doc.path]) });
const wiredRows = rowsOf(wiredRoot);
// activate the FIRST, a MIDDLE and the LAST row by click, then by Enter and
// Space on the first — the three gestures the affordance promises
// An UNWIRED row has no handler at all, which is the defect itself — fire what
// is there rather than throwing, so this reports "nothing opened" instead of
// taking the unrelated stat-tile cases down with a harness crash.
const fire = (row, type, ev) => { if (row && row.handlers[type]) row.handlers[type](ev); };
const probeIdx = [0, Math.floor(wiredRows.length / 2), wiredRows.length - 1];
for (const i of probeIdx) fire(wiredRows[i], 'click', EV);
const afterClicks = opened.length;
fire(wiredRows[0], 'keydown', { ...EV, key: 'Enter' });
fire(wiredRows[0], 'keydown', { ...EV, key: ' ' });
fire(wiredRows[0], 'keydown', { ...EV, key: 'a' });
out.wired = {
  rows: wiredRows.length,
  rowShapes: wiredRows.map(describeRow),
  probeIdx,
  clickOpened: opened.slice(0, afterClicks),
  keyOpened: opened.slice(afterClicks),
  rowNames: wiredRows.map((r) => textOf(r)),
};

// --- unwired: no affordance at all -------------------------------------------
const bareRoot = document.createElement('div');
renderDocs(bareRoot, snapshot);
out.unwired = { rowShapes: rowsOf(bareRoot).map(describeRow) };

// --- the stats strip ----------------------------------------------------------
const statsRoot = document.createElement('div');
renderStats(statsRoot, snapshot);
out.stats = flatten(statsRoot, []).filter((n) => classesOf(n).includes('tile'))
  .map((t) => {
    const part = (cls) => {
      const hit = flatten(t, []).find((n) => classesOf(n).includes(cls));
      return hit ? textOf(hit) : null;
    };
    return { k: part('k'), v: part('v'), s: part('s') };
  });
console.log(JSON.stringify(out));
"""


def _scale_snapshot():
    """177 documents across five staging topics plus the brainstorm area, with
    the sweep's own eight-stage distribution."""
    documents = []
    n = 0
    for stage, count in STAGE_TALLY.items():
        for i in range(count):
            topic = TOPICS[n % len(TOPICS)]
            area = "ideation/brainstorm" if stage == "brainstorm" else \
                (f"ideation/staging/{topic}" if stage in ("staged", "draft") else "docs")
            documents.append({
                "id": f"{stage}-{i}",
                "path": f"{area}/{stage}-{i:03d}.md",
                "stage": stage,
                "kind": "note",
                "summary": f"{stage} document {i}",
                "topics": [topic, "shared-keyword"],
            })
            n += 1
    return {
        "repository": "openxFactory",
        "generation": {"source_revision": "8" * 40, "generated_at": "2026-07-28T00:00:00+00:00"},
        "documents": documents,
        "clusters": [{"id": f"c{i}", "name": f"cluster {i}"} for i in range(151)],
        "possibles": [], "staged_topics": [{"id": t} for t in TOPICS], "changes": [],
    }


SNAPSHOT = _scale_snapshot()


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the JS renderer probe")
    tmp_path = tmp_path_factory.mktemp("doc-surfaces")
    for src in (DOCS_JS, LINEAGE_JS, HELPERS_JS):
        shutil.copy(src, tmp_path / src.name)
    # ESM without renaming: the views import "./helpers.js" by name
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(SNAPSHOT), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# defect 7 — the doc list is completely inert while advertising itself clickable
# ---------------------------------------------------------------------------

def test_the_corpus_wide_list_renders_a_row_per_document():
    assert sum(STAGE_TALLY.values()) == 177, "the scale fixture is not corpus-shaped"


def test_every_doc_row_is_an_activatable_control(rendered):
    """The sweep's measurement, inverted: 177 rows, zero click handlers, zero
    tabindex, zero role, computed cursor `auto`. Every row now carries the whole
    control contract — a hover class the CSS is scoped to, a role, a tab stop,
    a title, and BOTH activation gestures."""
    shapes = rendered["wired"]["rowShapes"]
    assert len(shapes) == 177, f"expected a row per document, got {len(shapes)}"
    for shape in shapes:
        assert "docrow" in shape["classes"]
        assert "docrow-open" in shape["classes"], "the hover affordance is not stamped"
        assert shape["role"] == "button"
        assert shape["tabIndex"] == 0
        assert shape["title"] and shape["title"].startswith("open ")
        assert set(shape["events"]) == {"click", "keydown"}


def test_clicking_a_row_opens_that_rows_document(rendered):
    """Not merely 'a handler is wired': the row hands back ITS OWN path. Three
    rows spread across the 177 — first, middle, last — so a handler closed over
    the wrong loop variable fails rather than passing on row 0."""
    wired = rendered["wired"]
    opened = wired["clickOpened"]
    assert len(opened) == len(wired["probeIdx"]) == 3
    for (path, doc_path), idx in zip(opened, wired["probeIdx"]):
        assert path, "a row opened with an empty path"
        assert path == doc_path, "the row handed back a document that is not its own"
        # the row displays dirname and basename in separate elements, so both
        # halves of the path it handed back must be the ones it rendered
        head, _, tail = path.rpartition("/")
        shown = wired["rowNames"][idx]
        assert tail in shown and (head + "/") in shown, \
            f"row {idx} opened {path}, which is not the document it displays: {shown!r}"
    assert len({p for p, _ in opened}) == 3, "three different rows opened one document"


def test_enter_and_space_open_a_row_and_other_keys_do_not(rendered):
    """Keyboard parity with the mouse (the explorer's rows already have it).
    Enter and Space each open once; an ignored key opens nothing."""
    assert len(rendered["wired"]["keyOpened"]) == 2


def test_an_unwired_list_advertises_nothing(rendered):
    """The other acceptable state the sweep named: 'or they are visibly
    non-interactive'. With no `onOpenDoc` the row carries no role, no tab stop
    and no `docrow-open`, so the CSS hover restyle below cannot reach it."""
    for shape in rendered["unwired"]["rowShapes"]:
        assert shape["role"] is None
        assert shape["tabIndex"] is None
        assert shape["events"] == []
        assert "docrow-open" not in shape["classes"]


def test_the_hover_affordance_is_scoped_to_rows_that_open_something():
    """The CSS half of the same decision. `.docrow:hover` restyled the border on
    every row in the corpus-wide list; the restyle now names only the classes
    that carry a handler, so an inert row cannot look interactive again."""
    css = STYLES_CSS.read_text(encoding="utf-8")
    assert ".docrow:hover" not in css, \
        "the unscoped hover restyle is back — every inert row advertises itself again"
    assert ".docrow-open:hover, .explorer-row:hover { border-color: var(--faint-ink); }" in css
    assert ".docrow-open, .explorer-row { cursor: pointer; }" in css


def test_the_doc_tab_is_wired_to_the_one_cross_view_jump():
    """app.js owns every cross-view jump; the doc list must reach the SAME
    read-only overlay the wheel's `read` verb uses, not a second viewer."""
    app = APP_JS.read_text(encoding="utf-8")
    block = app.split('{ tab: "tab-docs"', 1)[1].split("},", 1)[0]
    assert "renderDocs(root, snap, { onOpenDoc: ctx.nav.openDoc })" in block


# ---------------------------------------------------------------------------
# defect 15 — the DOCUMENTS stat tile's sub-line does not sum to its headline
# ---------------------------------------------------------------------------

def _documents_tile(rendered):
    tiles = {t["k"]: t for t in rendered["stats"]}
    assert "Documents" in tiles, tiles
    return tiles["Documents"]


def _subline_numbers(sub):
    return [int(m) for m in re.findall(r"(\d+)", sub)]


def test_the_documents_sub_line_sums_to_its_own_headline(rendered):
    """177 over 'draft 65 · staged 32 · brainstorm 39' = 136 silently dropped 41
    documents. Whatever shape the sub-line takes, its numbers must add up to the
    headline it sits under — that is the whole contract."""
    tile = _documents_tile(rendered)
    assert tile["v"] == "177"
    assert sum(_subline_numbers(tile["s"])) == 177, \
        f"the sub-line does not sum to the headline: {tile['s']!r}"


def test_the_documents_sub_line_accounts_for_the_stages_it_does_not_name(rendered):
    """Partial is allowed — 'say +41 other' — silent is not. Every stage the
    sub-line does not name by itself is carried in an explicit remainder."""
    tile = _documents_tile(rendered)
    sub = tile["s"]
    named = {stage: count for stage, count in STAGE_TALLY.items() if stage in sub}
    unnamed = sum(count for stage, count in STAGE_TALLY.items() if stage not in named)
    assert named, "the sub-line names no stage at all"
    for stage, count in named.items():
        assert f"{stage} {count}" in sub, f"{stage} is named with the wrong count: {sub!r}"
    if unnamed:
        assert f"+{unnamed} other" in sub, \
            f"{unnamed} documents are dropped without a remainder: {sub!r}"


def test_the_stat_tile_and_the_board_footer_agree(rendered):
    """The sweep's sharpest complaint was self-contradiction: the pipeline
    board's footer does this arithmetic completely one tab away. Both now derive
    from the whole distribution, so the two surfaces cannot disagree."""
    tile = _documents_tile(rendered)
    for stage, count in STAGE_TALLY.items():
        if stage in tile["s"]:
            assert f"{stage} {count}" in tile["s"]
    assert sum(_subline_numbers(tile["s"])) == sum(STAGE_TALLY.values())


def test_the_stage_names_are_not_hardcoded_in_the_stat_tile():
    """lineage.js:44 hardcoded exactly three stage names directly under a comment
    claiming to have fixed this class of bug. The derivation now reads the
    corpus's own distribution."""
    src = LINEAGE_JS.read_text(encoding="utf-8")
    strip = src.split("export function renderStats", 1)[1].split("\n}", 1)[0]
    hardcoded = [name for name in ("draft", "staged", "brainstorm")
                 if f'stageCount("{name}")' in strip]
    assert not hardcoded, f"stage names hardcoded back into the stat tile: {hardcoded}"
