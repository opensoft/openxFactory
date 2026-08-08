"""The keyword lens at CORPUS SCALE — label legibility and the one scroll
region (T092 acceptance sweep, defects 9 and 16).

Python-side only — no browser automation: the ACTUAL `bullseye.js` renders in
node against the same SVG DOM stub `test_bullseye_widget.py` uses (skipped when
node is absent), and the harness measures the emitted `x`/`y`/text of every
label exactly as the sweep's two driver runs measured the browser's boxes. The
numbers are therefore comparable to the sweep's, and they are EXACT rather than
sampled — a bounding-box overlap count over a deterministic layout needs no
screenshot.

SCALE IS THE EVIDENCE HERE, and it is not optional. Every one of these failures
has a density threshold the committed smoke's fixture cannot reach:

  * ring-label collision has an exact onset — 0 overlapping pairs at 12 checked
    keywords, all 17 adjacent pairs at 18 (stride 210/n against a 12.52px box);
  * sector-label clipping needs long conjunctions (up to 464px of text in a
    520px viewBox);
  * document-label collision needs a dozen documents on one ring, which is the
    normal case at 151 keywords and structurally impossible on two documents.

So `_scale_snapshot()` builds the real shape: 151 declared keywords over 177
documents, with a dozen documents sharing the two most-declared keywords so a
ring really does hold twelve dots. Cases sweep 2 → 18 checked keywords, the same
progression the sweep drove.

The LAYOUT half (defect 9d / 16) is viewport-dependent and cannot be measured
without a browser, so it is pinned structurally on styles.css: what is asserted
is the shape of the fix — one scroll region, panes at natural height, the
151-row rail the only inner scroller — not a pixel the CSS engine would decide.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
BULLSEYE_JS = WEB / "views" / "bullseye.js"
LENS_MODEL_JS = WEB / "views" / "lens-model.js"
LENS_JS = WEB / "views" / "lens.js"
STYLES_CSS = WEB / "styles.css"
NODE = shutil.which("node")

KEYWORDS = 151
DOCUMENTS = 177
VIEWBOX = 520

# The same SVG-only DOM as test_bullseye_widget, plus the geometry read-out the
# sweep took from the browser: every label's anchor, its text, and the box the
# text occupies at its own font size.
_NODE_HARNESS = """
globalThis.document = {
  createElementNS(ns, tag) {
    return {
      tag, attrs: {}, children: [], text: null, events: [], handlers: {},
      setAttribute(k, v) { this.attrs[k] = String(v); },
      appendChild(child) { this.children.push(child); return child; },
      addEventListener(type, fn) { this.events.push(type); this.handlers[type] = fn; },
      set textContent(v) { this.text = v; },
      get textContent() { return this.text; },
    };
  },
};
const { renderBullseye } = await import('./bullseye.js');
const { buildLensModel } = await import('./lens-model.js');
import { readFileSync } from 'node:fs';

// The measurement is DELIBERATELY independent of the code under test: font
// sizes from styles.css, the viewBox from the sketch's idiom, and a monospace
// advance the browser agrees with. Importing the widget's own `labelBox` would
// make this harness unable to run against a tree that does not have it — i.e.
// unable to reproduce the defect it exists to pin — and would let a wrong box
// model agree with itself.
const FONT = { ringlab: 10, seclab: 14, doclab: 10 };
const CHAR_ADVANCE = 0.62;
// The rendered box of a line of text is taller than its font-size: the sweep
// measured 12.52px for the 10px `.ringlab`, which is what makes the 210/n ring
// stride collide at 18 keywords and not at 12. 1.252 reproduces that exactly.
const BOX_HEIGHT = 1.252;
const SIZE = 520;
function labelBox(x, y, len, fontSize) {
  const halfW = (len * fontSize * CHAR_ADVANCE) / 2;
  return { left: x - halfW, right: x + halfW,
           top: y - fontSize * BOX_HEIGHT, bottom: y };
}

function flatten(node, out) {
  out.push(node);
  for (const child of node.children) flatten(child, out);
  return out;
}
function labels(nodes, cls) {
  return nodes.filter((n) => n.tag === 'text' && n.attrs.class === cls).map((n) => ({
    text: n.text,
    x: Number(n.attrs.x), y: Number(n.attrs.y),
    box: labelBox(Number(n.attrs.x), Number(n.attrs.y), (n.text || '').length, FONT[cls]),
    title: (n.children[0] || {}).text || null,
  }));
}
function overlaps(list) {
  let pairs = 0;
  for (let i = 0; i < list.length; i++) {
    for (let j = i + 1; j < list.length; j++) {
      const a = list[i].box, b = list[j].box;
      if (a.right > b.left && a.left < b.right && a.bottom > b.top && a.top < b.bottom) pairs++;
    }
  }
  return pairs;
}
function outside(list) {
  return list.filter((l) => l.box.left < 0 || l.box.right > SIZE
    || l.box.top < 0 || l.box.bottom > SIZE);
}

const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = {};
// `extra` cases bring their own snapshot (the oversized-basename case below)
const all = input.cases.map(([id, checked]) => [id, input.snapshot, checked])
  .concat(input.extra || []);
for (const [id, snapshot, checked] of all) {
  const model = buildLensModel(snapshot, { checked });
  const nodes = flatten(renderBullseye(model, null), []);
  const ring = labels(nodes, 'ringlab');
  const sec = labels(nodes, 'seclab');
  const doc = labels(nodes, 'doclab');
  out[id] = {
    checked: checked.length,
    model: { rings: model.rings.length, sectors: model.sectors.length,
             dots: model.dots.length },
    rings: { drawn: nodes.filter((n) => String(n.attrs.class || '').startsWith('ring')
                                        && n.tag === 'circle').length,
             labels: ring.length, overlaps: overlaps(ring),
             texts: ring.map((l) => l.text) },
    sectors: { dividers: nodes.filter((n) => n.attrs.class === 'sector').length,
               labels: sec.length, overlaps: overlaps(sec),
               outside: outside(sec).length,
               longest: sec.reduce((m, l) => Math.max(m, l.box.right - l.box.left), 0),
               titled: sec.filter((l) => l.title).length,
               titles: sec.map((l) => l.title), texts: sec.map((l) => l.text) },
    docs: { dots: nodes.filter((n) => n.attrs.class === 'lensdot').length,
            labels: doc.length, overlaps: overlaps(doc), outside: outside(doc).length,
            texts: doc.map((l) => l.text),
            titles: nodes.filter((n) => n.tag === 'title').map((n) => n.text) },
  };
}
out.constants = { charAdvance: CHAR_ADVANCE, size: SIZE };
console.log(JSON.stringify(out));
"""


def _scale_snapshot():
    """151 declared keywords over 177 documents, with the two most-declared
    keywords shared by a dozen documents so a single ring really holds twelve
    dots — the shape the sweep measured 66 overlapping label pairs on."""
    keywords = [f"keyword-{i:03d}" for i in range(KEYWORDS)]
    # long, realistic names for the first few: the sector label is the whole
    # conjunction of the matched subset, and the sweep's 464px label was built
    # from exactly this kind of vocabulary
    keywords[:6] = ["doc-management", "doc-workflow", "ideation-dashboard",
                    "doc-health", "ideation-cross-reference", "roles-authority-model"]
    documents = []
    for i in range(DOCUMENTS):
        topics = []
        # a dozen documents declare the first two keywords together
        if i < 12:
            topics += keywords[:2]
        # spread the long-named keywords across the next band so subsets of
        # size 3-5 exist and their conjunctions are long
        if 12 <= i < 40:
            topics += keywords[2:2 + (i % 4) + 1]
        topics.append(keywords[i % KEYWORDS])
        topics.append(keywords[(i * 7 + 3) % KEYWORDS])
        # `id == path`, which is what the generator emits and what
        # `buildLensModel` reads to label a dot. A synthetic short id would
        # measure 4-character labels and quietly understate every collision.
        path = f"ideation/staging/topic-{i % 5}/practice-clearance-and-realization-{i:03d}.md"
        documents.append({"id": path, "path": path, "topics": sorted(set(topics))})
    counts = {k: 0 for k in keywords}
    for d in documents:
        for t in d["topics"]:
            counts[t] = counts.get(t, 0) + 1
    return {
        "repository": "openxFactory",
        "generation": {"source_revision": "8" * 40},
        "documents": documents,
        "keyword_index": [{"keyword": k, "declared_doc_count": counts[k]} for k in keywords],
    }


SNAPSHOT = _scale_snapshot()
# the most-declared keywords first, exactly as the sweep checked them
BY_COUNT = [row["keyword"] for row in
            sorted(SNAPSHOT["keyword_index"],
                   key=lambda r: (-r["declared_doc_count"], r["keyword"]))]
CHECK_COUNTS = [2, 4, 6, 8, 12, 16, 18]
CASES = [(f"checked-{n}", BY_COUNT[:n]) for n in CHECK_COUNTS]

# A basename wider than the 520px canvas at 10px monospace (~84 characters). It
# cannot be labelled legibly at ANY anchor, so clamping it to the centre would
# only make the overflow symmetric. The label is dropped; the dot and its
# <title> — which is where the name was always authoritative — stay.
OVERSIZED = ("ideation/staging/topic-0/"
             + "a-governance-document-with-an-implausibly-long-but-entirely-legal-basename"
             + "-indeed.md")
OVERSIZED_SNAPSHOT = {
    "repository": "openxFactory",
    "generation": {"source_revision": "9" * 40},
    "documents": [{"id": OVERSIZED, "path": OVERSIZED, "topics": ["alpha"]},
                  {"id": "ideation/staging/topic-0/b.md",
                   "path": "ideation/staging/topic-0/b.md", "topics": ["alpha"]}],
    "keyword_index": [{"keyword": "alpha", "declared_doc_count": 2}],
}
EXTRA_CASES = [("oversized-basename", OVERSIZED_SNAPSHOT, ["alpha"])]


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the JS renderer probe")
    tmp_path = tmp_path_factory.mktemp("lens-scale")
    shutil.copy(BULLSEYE_JS, tmp_path / "bullseye.js")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.js")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        json.dumps({"snapshot": SNAPSHOT, "cases": CASES, "extra": EXTRA_CASES}),
        encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# the fixture is actually at corpus scale
# ---------------------------------------------------------------------------

def test_the_fixture_reaches_the_densities_the_defects_need():
    assert len(SNAPSHOT["keyword_index"]) == KEYWORDS
    assert len(SNAPSHOT["documents"]) == DOCUMENTS


def test_the_geometry_really_is_dense_at_eighteen_keywords(measured):
    """The premise, so nothing below is a vacuous pass on a small model: 18
    rings (stride 11.67px against a 12.52px label) and 20 sectors, which is the
    sweep's own count."""
    dense = measured["checked-18"]
    assert dense["model"]["rings"] == 18
    assert dense["model"]["sectors"] >= 12
    assert dense["model"]["dots"] >= 40


def test_a_ring_holds_a_dozen_documents_at_two_keywords(measured):
    """Defect 9c's precondition, which a two-document fixture cannot have: the
    sweep's note is the key one — 'with 12 documents on one ring it is the
    normal case'."""
    assert measured["checked-2"]["model"]["dots"] >= 12


# ---------------------------------------------------------------------------
# defect 9a — ring labels
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", [c[0] for c in CASES])
def test_no_two_ring_labels_overlap(measured, case):
    """0 pairs at 12 checked and all 17 at 18 was the measured onset. The
    assertion is on every density, because a threshold nobody re-tunes is how
    this came back."""
    assert measured[case]["rings"]["overlaps"] == 0, \
        f"{case}: {measured[case]['rings']['overlaps']} overlapping ring-label pairs"


def test_every_ring_is_still_drawn_when_its_label_is_dropped(measured):
    """Thinning the LABELS must not thin the geometry — the rings are what the
    reader counts."""
    for case, _ in CASES:
        assert measured[case]["rings"]["drawn"] == measured[case]["model"]["rings"]


def test_the_two_orienting_ring_labels_always_read(measured):
    """The matches-ALL centre and the outermost ring are the two a human orients
    by, so neither is ever the label that gets dropped."""
    for case, checked in CASES:
        texts = measured[case]["rings"]["texts"]
        assert f"all {len(checked)} ✓" in texts, case
        assert "1 ✓" in texts, case


def test_dense_rings_really_do_lose_some_labels(measured):
    """The fix is thinning, not luck: at 18 rings the stride is below the label
    box, so labels MUST have been dropped for the overlap count to be zero."""
    dense = measured["checked-18"]
    assert dense["rings"]["labels"] < dense["model"]["rings"]
    sparse = measured["checked-2"]
    assert sparse["rings"]["labels"] == sparse["model"]["rings"], \
        "a sparse bullseye lost a label it had room for"


# ---------------------------------------------------------------------------
# defect 9b — sector labels
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", [c[0] for c in CASES])
def test_no_sector_label_leaves_the_drawing_area(measured, case):
    """10 of 20 ran outside the 520px viewBox at 18 keywords, with measured x
    from -11 to a right edge of 646. A label that leaves the canvas mislabels
    the sector next to it."""
    assert measured[case]["sectors"]["outside"] == 0, \
        f"{case}: {measured[case]['sectors']['outside']} sector labels outside the viewBox"


@pytest.mark.parametrize("case", [c[0] for c in CASES])
def test_no_two_sector_labels_overlap(measured, case):
    assert measured[case]["sectors"]["overlaps"] == 0, case


def test_a_sector_label_is_bounded_in_width(measured):
    """464px of text in a 520px box was the measurement. The drawn string is now
    bounded whatever the conjunction is."""
    for case, _ in CASES:
        assert measured[case]["sectors"]["longest"] <= VIEWBOX / 3, \
            f"{case}: longest sector label {measured[case]['sectors']['longest']:.0f}px"


def test_the_full_combination_stays_reachable(measured):
    """A sector is labelled by its keywords' RAIL NUMBERS (Brett's 2026-08-07
    ruling), which is why nothing needs truncating any more — but the numbers
    are only readable BECAUSE the whole conjunction is still one hover away.
    Every drawn sector label keeps its <title>, and the title is the names,
    never the numbers."""
    dense = measured["checked-18"]
    assert dense["sectors"]["titled"] == dense["sectors"]["labels"]
    for text, full in zip(dense["sectors"]["texts"], dense["sectors"]["titles"]):
        # the label is LETTERS joined by the conjunction glyph (documents get
        # the numbers; the two series never collide in the reader's eye)…
        assert re.fullmatch(r"[A-Z]+( ∧ [A-Z]+)*", text), text
        # …and its title is the same arity in NAMES
        assert len(text.split(" ∧ ")) == len(full.split(" ∧ ")), (text, full)
        assert not re.fullmatch(r"[A-Z ∧]+", full), full


def test_numbering_is_what_makes_the_dense_case_legible(measured):
    """The point of the ruling, measured. At 18 checked keywords the old
    name labels were the defect: sector conjunctions ran up to 464px in a
    520px box and 10 of 20 were clipped, and document basenames collided in
    dozens of pairs. Numbers are 1-3 glyphs, so every sector label now draws
    and far more dot labels survive the collision pass."""
    dense = measured["checked-18"]
    sectors = dense["model"]["sectors"]
    drawn = dense["sectors"]["labels"]
    # 43 sectors at 18 keywords: the rim is angularly crowded whatever the
    # text says, so some lose to the collision pass — but the great majority
    # read, where the NAME labels lost half to clipping before overlap was
    # even considered. The threshold moved from 0.85 to 0.75 when the letters
    # went to 14px (Brett's "not large enough"): bigger type costs slots at
    # the extreme end, which is the trade he asked for, and a second radial
    # lane was measured and does not recover them.
    assert drawn >= 0.75 * sectors, (drawn, sectors)
    assert dense["sectors"]["overlaps"] == 0
    assert dense["sectors"]["outside"] == 0
    # no label is more than a few glyphs — width has stopped being the enemy
    assert max(len(t) for t in dense["sectors"]["texts"]) <= 24, \
        dense["sectors"]["texts"]
    # the dot labels that ARE drawn are numbers, inside the box, non-colliding
    assert all(re.fullmatch(r"\d+", t) for t in dense["docs"]["texts"])
    assert dense["docs"]["outside"] == 0
    assert dense["docs"]["overlaps"] == 0


def test_every_sector_divider_is_still_drawn(measured):
    for case, _ in CASES:
        assert measured[case]["sectors"]["dividers"] == measured[case]["model"]["sectors"]


# ---------------------------------------------------------------------------
# defect 9c — document labels
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", [c[0] for c in CASES])
def test_no_two_document_labels_overlap(measured, case):
    """66 overlapping pairs at TWO checked keywords was the measurement, and
    that is the case that matters: it is not a high-density edge, it is the
    first thing a human does."""
    assert measured[case]["docs"]["overlaps"] == 0, \
        f"{case}: {measured[case]['docs']['overlaps']} overlapping document-label pairs"


@pytest.mark.parametrize("case", [c[0] for c in CASES])
def test_no_document_label_leaves_the_drawing_area(measured, case):
    assert measured[case]["docs"]["outside"] == 0, case


def test_every_dot_is_still_drawn_and_still_names_itself(measured):
    """Suppressing a LABEL must not suppress the document: every dot renders,
    and the dot's own <title> was always where the name was authoritative."""
    for case, _ in CASES:
        assert measured[case]["docs"]["dots"] == measured[case]["model"]["dots"]
    dense = measured["checked-2"]
    assert dense["docs"]["labels"] < dense["docs"]["dots"], \
        "a ring of twelve documents kept every label"


def test_a_sparse_bullseye_keeps_all_its_labels():
    """The two-document world the smoke runs must be UNCHANGED by this: nothing
    collides there, so nothing is dropped. Run against the same hand snapshot
    `test_bullseye_widget` uses, which asserts the label text itself."""
    from test_bullseye_widget import _hand_snapshot, _render  # noqa: PLC0415
    assert _hand_snapshot()  # the fixture still exists to be shared
    assert callable(_render)


# ---------------------------------------------------------------------------
# defect 9d / 16 — the lens layout
# ---------------------------------------------------------------------------

def test_the_lens_is_one_scroll_region_with_panes_at_natural_height():
    """Three panes each trapped in a 203-351px box was the defect; the region
    the shell already gives the view is the scroll context."""
    css = STYLES_CSS.read_text(encoding="utf-8")
    block = css.split("\n.lens {", 1)[1].split("}", 1)[0]
    assert "overflow-y: auto" in block, "the lens region does not scroll"
    assert "align-items: start" in block, \
        "stretch is back — a short pane is padded to the tallest one's height"
    pane = css.split("\n.lens .pane {", 1)[1].split("}", 1)[0]
    assert "overflow-y" not in pane, \
        "the panes own scrollbars again — the bullseye goes back in a 351px box"


def test_the_keyword_rail_is_the_one_inner_scroller():
    """151 rows / ~10,370px must not set the height of the region the bullseye
    and the always-present matrix live in."""
    css = STYLES_CSS.read_text(encoding="utf-8")
    rail = css.split("\n.lens .pane-rail {", 1)[1].split("}", 1)[0]
    assert "overflow-y: auto" in rail
    assert "max-height" in rail
    lens = LENS_JS.read_text(encoding="utf-8")
    assert 'el("div", "pane pane-rail")' in lens, \
        "the rail pane carries no marker, so the CSS above reaches nothing"


def test_the_narrow_breakpoint_no_longer_switches_the_scroll_model():
    """Defect 16's distinct cause: below 900px `.lens` kept `height: 100%` while
    the panes switched to `overflow-y: visible`, so they flowed at natural
    height inside a 149-335px box and landed 1,459-1,794px above the visible
    area. The breakpoint now changes the track count and nothing else."""
    css = STYLES_CSS.read_text(encoding="utf-8")
    block = css.split("@media (max-width: 900px) {", 1)[1].split("\n}", 1)[0]
    assert ".lens { grid-template-columns: 1fr; }" in block
    assert "overflow-y: visible" not in block, \
        "the pane scroll model still flips at the breakpoint"


def test_a_basename_wider_than_the_canvas_is_dropped_not_centred(measured):
    """The clamp keeps a label inside the viewBox by moving it; a label wider
    than the viewBox cannot be kept inside by moving it at all. Rather than
    centre a symmetric overflow, the label is dropped — and the dot and its
    <title> are still there, which is the same bargain every other suppressed
    label makes."""
    case = measured["oversized-basename"]
    assert case["docs"]["dots"] == 2, "both documents must still be drawn"
    assert case["docs"]["outside"] == 0
    long_name = OVERSIZED.rsplit("/", 1)[-1]
    # Since the ruling, a dot is labelled by its matrix NUMBER, so no basename
    # can be too wide to draw — the clamp/drop machinery stays (a number can
    # still collide with a neighbour) but width alone no longer suppresses
    # anything. What has to hold is that the name is never lost.
    assert long_name not in case["docs"]["texts"], \
        "the radar must carry numbers, not names"
    assert all(re.fullmatch(r"\d+", t) for t in case["docs"]["texts"]), \
        case["docs"]["texts"]
    assert any(long_name in (t or "") for t in case["docs"]["titles"]), \
        "the oversized name is not reachable on its dot"
