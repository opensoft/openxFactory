"""THE DOCS-PANE WHEEL: the deferred half of the docs split, at 0.4 radius.

RED-FIRST: authored before `doc-wheel.js` exists.

SOURCE. The second half of operator annotation `vibe_1785602331813_gvku9sh2s`,
verbatim — the half deliberately left out of the previous slice:

    "make the lower half be the same wheel of the docs we have used before. set
     the wheel radius to .4 the size of the subpane holding the wheel. since we
     are doing this as the bottom half, that would be .2 of the docs pane. the
     selected tile can second click to expand like our main wheel. for the top
     half when a doc is selected on the wheel, we load a viewer of that doc."

WHAT "THE SAME WHEEL" HAS TO MEAN. Not a lookalike. The previous slice shipped
an interim flat selector precisely because a second drum that merely RESEMBLED
the deck would drift from it the first time either was tuned — and the wheel is
the most heavily tuned surface in the dashboard (a live radius knob, a `?drum=`
compare-by-URL path, a locked prototype's reel constants). So the identity is
enforced by construction, not by eye:

  * the cylinder projection is ONE exported function, `drumProject`, which
    wheel.js's private `drum()` now calls and this wheel calls too;
  * the expand gesture is the SAME pure reducer, `nextExpanded` — the operator
    asked for "second click to expand like our main wheel", and that reducer IS
    that gesture, so reusing it is the only way the two can stay identical;
  * focusability is driven by the SAME predicate, `inReelWindow` (defect 6).

WHY 0.4 IS THE RIGHT NUMBER, and not an arbitrary shrink. The drum places tiles
at `winH/2 ± R` where `R = winH × drumF`. At factor 1.0 (the deck's original
default) that range is `[-0.5·winH, 1.5·winH]` — most of the column is laid
out far outside its own window and survives only because the clip stops it
painting. At 0.4 the range is `[0.1·winH, 0.9·winH]`: every tile the drum
places lands INSIDE the subpane, and tiles leave by wrapping over the drum's
own horizon rather than by running off
the end. In a pane a third the height of the deck's window that is the
difference between a wheel and a clipped list.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
DOC_WHEEL_JS = VIEWS / "doc-wheel.js"
WHEEL_MODEL_JS = VIEWS / "wheel-model.js"
SHELL_JS = VIEWS / "staging-workbench.js"
MODEL_JS = VIEWS / "staging-workbench-model.js"
STYLES = WEB / "styles.css"

# The lower half as MEASURED on the merged pane restructure (2026-08-03):
# a 379px selector below a 280px abstract.
SUBPANE_H = 379
TILE_H = 56

_HARNESS = """
import { drumProject, tileBox, tileScale, inReelWindow, nextExpanded, REEL }
  from './wheel-model.js';
import { docWheelEntries } from './staging-workbench-model.js';
import { DOC_WHEEL } from './doc-wheel.js';

const SUBPANE_H = %(subpane)d, TILE_H = %(tileh)d;

// One whole rendered column at a given knob, exactly as the view places it.
// BULGED AND FOCUSED, because doc-wheel.js renders it that way and the test has
// to model the code: a single-column drum IS the focused wheel — there is no
// second column for focus to be anywhere else — so it gets the tanh bulge and
// the continuous magnification curve toward 1.35 at the centre, exactly as the
// deck's focused column does.
function column(drumF, winH) {
  const tiles = [];
  for (let d = -12; d <= 12; d++) {
    const c = drumProject({ d, bulged: true, winH, drumF, scaleF: 1 });
    const y = winH / 2 + c.y;
    const box = tileBox({ y, squash: c.squash, tileH: TILE_H,
                          scale: tileScale(d, true) });
    tiles.push({ d, y, over: c.over, top: box.top, bottom: box.bottom,
                 inWindow: inReelWindow(box, winH, c.over) });
  }
  return tiles;
}

const SCOPE = { sections: [
  { label: 'topic folder documents', note: 'n', inherited: false, documents: [
      // scored, as a catalogued corpus document is
      { path: 'ideation/staging/t/a.md', completeness: { score: 0.7 },
        doc: { path: 'ideation/staging/t/a.md', summary: 'A', stage: 'staged' } },
      // NOT scored — the flat list drew no bar for these, deliberately
      { path: 'ideation/staging/t/b.md', doc: { path: 'ideation/staging/t/b.md' } },
  ]},
  { label: 'inherited', note: 'n', inherited: true, documents: [
      { path: 'docs/c.md', resolved: false, doc: { path: 'docs/c.md' } },
  ]},
]};

// The locked gesture, driven as the view drives it.
const g = [];
let st = null;
st = nextExpanded(st, { type: 'tile', key: 'docs', i: 2, centred: false });
g.push(['click-away', st]);
st = nextExpanded(st, { type: 'tile', key: 'docs', i: 2, centred: true });
g.push(['click-centred', st]);
st = nextExpanded(st, { type: 'tile', key: 'docs', i: 2, centred: true });
g.push(['click-again', st]);

process.stdout.write(JSON.stringify({
  mini: column(DOC_WHEEL.drumF, SUBPANE_H),
  deck: column(1, SUBPANE_H),
  drumF: DOC_WHEEL.drumF,
  entries: docWheelEntries(SCOPE),
  empty: docWheelEntries({ sections: [] }),
  gesture: g,
  spacing: REEL.spacing,
}));
""" % {"subpane": SUBPANE_H, "tileh": TILE_H}


@pytest.fixture(scope="module")
def probe(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doc-wheel probe")
    tmp = tmp_path_factory.mktemp("doc-wheel")
    # Real filenames, not `.mjs` stubs: `doc-wheel.js` imports its siblings by
    # their own names, so the copy has to preserve the graph. A `type: module`
    # package makes node read these `.js` files as the ES modules they are.
    (tmp / "package.json").write_text('{"type":"module"}', encoding="utf-8")
    for src in (WHEEL_MODEL_JS, MODEL_JS, DOC_WHEEL_JS, VIEWS / "helpers.js"):
        if not src.exists():
            pytest.fail(f"{src.name} does not exist yet")
        shutil.copy(src, tmp / src.name)
    harness = tmp / "probe.js"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30, cwd=tmp)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# the radius the operator asked for, and why it is the right one
# ---------------------------------------------------------------------------


def test_the_doc_wheel_uses_the_radius_the_annotation_names(probe):
    """"set the wheel radius to .4 the size of the subpane holding the wheel"."""
    assert probe["drumF"] == pytest.approx(0.4)


def test_at_this_radius_every_tile_the_drum_places_is_inside_the_subpane(probe):
    """THE reason 0.4 works in a small pane. R = 0.4·winH, so the drum's own
    extent is winH/2 ± 0.4·winH — the whole reel lands inside its window and
    tiles leave by wrapping over the horizon, not by running off the end."""
    radius = SUBPANE_H * probe["drumF"]
    lo, hi = SUBPANE_H / 2 - radius, SUBPANE_H / 2 + radius
    for tile in probe["mini"]:
        if tile["over"]:
            continue
        # `y` is the PLACED centre (winH/2 + projection), so the drum's extent
        # is winH/2 ± R rather than ±R.
        assert lo - 0.5 <= tile["y"] <= hi + 0.5, (
            f"tile {tile['d']} is placed at {tile['y']}, outside the drum's own "
            f"extent [{lo:.1f}, {hi:.1f}]")
        assert tile["top"] >= 0, (
            f"tile {tile['d']} is drawn above the top of its subpane: {tile}")
        assert tile["bottom"] <= SUBPANE_H, (
            f"tile {tile['d']} is drawn below the bottom of its subpane: {tile}")


def test_the_decks_own_radius_would_not_fit_this_pane(probe):
    """The contrast that makes the previous test a fact about 0.4 rather than
    a fact about small numbers: at factor 1.0 (the deck's original default),
    tiles the drum has NOT taken over the horizon are still laid out beyond
    both edges of a pane this size, surviving only because the clip hides
    them."""
    outside = [t for t in probe["deck"] if not t["over"]
               and (t["top"] < 0 or t["bottom"] > SUBPANE_H)]
    assert outside, (
        "at drum 1.0 in a 379px pane nothing lands outside the window — then "
        "0.4 buys nothing and this slice's premise is wrong")


def test_the_wheel_is_not_so_tight_that_it_shows_one_document(probe):
    """A drum wound tight enough to fit is useless if it only ever presents a
    single tile: the operator asked for the wheel BECAUSE it shows neighbours."""
    reachable = [t for t in probe["mini"] if t["inWindow"]]
    assert len(reachable) >= 5, (
        f"only {len(reachable)} tiles are in the window at drum "
        f"{probe['drumF']} — that is a list with extra steps")


# ---------------------------------------------------------------------------
# "the same wheel" — enforced by shared code, not by resemblance
# ---------------------------------------------------------------------------


def test_the_projection_has_exactly_one_definition():
    """`drumProject` is THE cylinder projection. wheel.js must call it rather
    than keep its own copy, or "the same wheel" degrades to "a similar wheel"
    the first time either is tuned."""
    model = WHEEL_MODEL_JS.read_text(encoding="utf-8")
    assert "export function drumProject" in model
    wheel = (VIEWS / "wheel.js").read_text(encoding="utf-8")
    assert "drumProject" in wheel, "wheel.js no longer uses the shared projection"
    body = re.search(r"function drum\(d, bulged\) \{(.*?)\n  \}", wheel, re.S)
    assert body, "wheel.js's drum() closure is gone — check this pin still means something"
    assert "Math.sin" not in body.group(1), (
        "wheel.js has re-grown its own copy of the projection")


def test_the_doc_wheel_reuses_the_projection_rather_than_its_own_trigonometry():
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "drumProject" in source
    assert "Math.sin" not in source, (
        "the doc wheel computes its own cylinder placement; it must call "
        "drumProject so the two drums cannot diverge")


def test_second_click_expands_through_the_same_locked_reducer(probe):
    """"the selected tile can second click to expand like our main wheel" — so
    the gesture must BE the main wheel's reducer, not a re-derivation of it."""
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "nextExpanded" in source, (
        "the doc wheel hand-rolls its expand gesture instead of reusing the "
        "locked reducer the main wheel uses")
    steps = dict((name, state) for name, state in probe["gesture"])
    assert steps["click-away"] is None, "a click on an off-centre tile only focuses"
    assert steps["click-centred"] == {"key": "docs", "i": 2}, (
        "the second click, once the tile is on the line, expands it")
    assert steps["click-again"] is None, "a third click collapses"


def test_off_window_tiles_are_not_focusable(probe):
    """DEFECT 6, which cost a keyboard user 45 Tab presses to reach the second
    of six columns. A second drum is a second chance to repeat it, so the doc
    wheel must drive tabIndex from the same predicate."""
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "inReelWindow" in source, (
        "the doc wheel does not use inReelWindow — its off-window tiles will "
        "sit in the tab order exactly as defect 6 did")
    assert "tabIndex" in source
    assert [t for t in probe["mini"] if not t["inWindow"]], (
        "no tile is off-window at this radius, so the predicate is untested here")


def test_nothing_past_the_horizon_paints(probe):
    """MEASURED FAILURE, pinned (2026-08-03). At a 0.4 radius the reel wraps
    over the drum's horizon long before it runs out of documents, so every tile
    round the back stacks on one of the two poles — the rig measured 12 tiles at
    5 distinct positions. Faded to `tileOpacity`'s 0.22 floor that is a pile of
    ghost tiles smeared across the top and bottom of the pane. The deck already
    solved this: fade by the drum's OWN foreshortening and paint nothing that is
    `over`. This wheel does the same, which is also what makes it the same
    wheel."""
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "c.over" in source, (
        "the wheel never consults the drum's horizon flag")
    assert 'opacity = c.over ? "0"' in source, (
        "tiles past the drum's horizon are not hidden; they will pile up "
        "visibly at the poles")
    # The CALL, not the word: the module is allowed to name `tileOpacity` in
    # prose to explain why a drum does not use it.
    assert "tileOpacity(" not in source, (
        "the flat-reel opacity curve is back — the deck fades a DRUM by its "
        "foreshortening (clamp(squash, .15, 1)), not by step distance")
    assert "c.squash" in source
    assert [t for t in probe["mini"] if t["over"]], (
        "no tile is over the horizon at this radius, so the rule is untested")


def test_the_tiles_are_the_wheels_own_chrome():
    """Same wheel means it LOOKS like the wheel too — the tile classes are the
    deck's, so one stylesheet change moves both."""
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "wheeltile" in source
    assert "wheellabel" in source


# ---------------------------------------------------------------------------
# the entries, and the sections they came from
# ---------------------------------------------------------------------------


def test_the_wheel_carries_every_document_in_the_scope(probe):
    """A drum is ONE reel. The docs pane groups documents into sections, so
    flattening is required — and must not silently drop a section."""
    paths = [e["path"] for e in probe["entries"]]
    assert paths == ["ideation/staging/t/a.md", "ideation/staging/t/b.md",
                     "docs/c.md"]


def test_a_flattened_document_still_says_which_section_it_came_from(probe):
    """The section headings carried real meaning — inherited documents are not
    the tile's own. Flattening into one reel must move that onto the tile, not
    lose it."""
    entries = probe["entries"]
    assert entries[0]["section"] == "topic folder documents"
    assert entries[2]["section"] == "inherited"
    assert entries[2]["inherited"] is True
    assert entries[0]["inherited"] is False


def test_each_entry_is_labelled_by_its_filename(probe):
    assert [e["label"] for e in probe["entries"]] == ["a.md", "b.md", "c.md"]


def test_an_empty_scope_yields_no_entries(probe):
    assert probe["empty"] == []


def test_the_completeness_score_survives_the_move_from_bars_to_tiles(probe):
    """WHAT THE DELETED ROWS DID THAT THE ABSTRACT DOES NOT. The flat list drew
    a completeness bar on EVERY row, which is how a human spotted the thin
    document without opening any of them. The abstract shows the SELECTED
    document's score and all five signals, so the detail survives — but
    comparison across documents would not have, and that was the bar's real
    job. So the score rides on every tile."""
    scores = [e["score"] for e in probe["entries"]]
    assert scores[0] == pytest.approx(0.7)
    assert scores[1] is None, "an unscored document must not be given a number"
    assert scores[2] is None


def test_an_unscored_document_shows_the_decks_dot_not_a_zero(probe):
    """Design D7, carried over: a missing completeness object is NO score —
    stated, so the absence is legible — and never a 0.00 that reads as a
    verdict of 'empty'."""
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert 'entry.score === null ? "·"' in source or '"·"' in source, (
        "the tile has no absent-score rendering; an unscored document will "
        "either show nothing or be given a number nobody computed")
    assert "toFixed(2)" in source


def test_an_unresolved_document_cannot_be_opened(probe):
    """The flat list refused the viewer for a document that is not a catalogued
    corpus document. The wheel's expanded tile must refuse it too."""
    assert probe["entries"][2]["resolved"] is False
    assert probe["entries"][0]["resolved"] is True
    source = DOC_WHEEL_JS.read_text(encoding="utf-8")
    assert "entry.resolved" in source, (
        "the expanded tile never checks whether the document is catalogued")
    assert "disabled" in source, (
        "nothing disables the open control for an uncatalogued document")


def test_the_flat_list_left_no_dead_renderer_behind():
    """`docRow`/`completenessCell` rendered the list the wheel replaced. Dead
    code that draws a bar nobody can see is exactly the class of defect this
    surface keeps producing, so they went with the list they served.
    (`docs.js` keeps its own unrelated `docRow` for the documents page.)"""
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "function docRow(" not in source
    assert "function completenessCell(" not in source


# ---------------------------------------------------------------------------
# wiring: the pane, the abstract, and the retired deferral
# ---------------------------------------------------------------------------


def test_the_docs_pane_mounts_the_wheel():
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "renderDocWheel" in source, "the docs pane still has no wheel"
    assert "doc-wheel.js" in source


def test_selecting_on_the_wheel_loads_that_documents_abstract():
    """"for the top half when a doc is selected on the wheel, we load a viewer
    of that doc" — the wheel's selection must drive the abstract built in the
    previous slice."""
    source = SHELL_JS.read_text(encoding="utf-8")
    # ANCHORED ON THE CALL, not on a character distance. This used to take a
    # ±2500-character window around the FIRST `renderDocWheel` occurrence — the
    # import line — so any edit between the import and the mount could fail it
    # while the wiring was perfectly intact (2026-08-10, and the wiring was).
    # A proximity pin also never proved the claim in the docstring: two names
    # sitting near each other is not a selection driving an abstract.
    mount = source.index("renderDocWheel(selector")
    window = source[mount:mount + 600]
    assert "onSelect:" in window, "the mount declares no selection callback"
    assert "renderAbstract(abstract," in window, (
        "the wheel's selection is not wired to the abstract above it")


def test_the_deferral_note_is_gone():
    """The previous slice left a note saying the wheel was ruled out and a flat
    selector stood in its place. Shipping the wheel while that note survives
    would leave the file lying about itself."""
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "NOT YET A WHEEL" not in source.upper(), (
        "the interim-selector note outlived the interim selector")
    assert "ruled out of this slice" not in source


def test_the_wheel_pane_is_styled():
    """The rail once shipped with ZERO rules under a green suite. Any new
    surface declares its own."""
    styles = STYLES.read_text(encoding="utf-8")
    for selector in (".swb-docwheel",):
        assert selector in styles, f"{selector} has no rules at all"
