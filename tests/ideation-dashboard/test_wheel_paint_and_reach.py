"""THE WHEEL's rendered geometry: what is reachable, and what paints over what
(T092 acceptance sweep, defects 6 and 14).

Python-side only — no browser automation: the ACTUAL `wheel-model.js` runs in
node (skipped when node is absent) at the sweep's own scale, and the wiring in
`wheel.js` and `styles.css` is pinned on their source. These four defects are
ARITHMETIC, not styling opinion: the sweep hit-tested every tile in a column and
measured every box, and every number below is one of those measurements.

  defect 6   a column renders ~31 tiles; 9 were mouse-reachable and 7 were
             inside the window. The other 22-25 were laid out at y=173-338
             while the window is y=395-890 — over the page header, the stat
             tiles and the tab strip — and they ALL kept `tabindex=0`, so a
             keyboard user tabbed through 25 invisible tiles and 45 Tab presses
             never reached the second of six columns.
  defect 14a the teal cluster-edge bundle was drawn ON TOP of the expanded
             tile's opaque card, crossing its left border and striking through
             "standing open items: 6". Read as z-order; it is not. drive3 found
             every CHILD inside the tile rect — the thread is not a child. The
             anchor was half the RESTING tile width while the endpoint is
             magnified, so the line started inside the card.
  defect 14b the focused tile's "15 clusters" badge landed on the NEXT tile in
             the column and covered its sub-line, in the DOCUMENTS and STAGED
             columns and in every wheel screenshot of the sweep.

SCALE IS THE POINT. A window holding 7 tiles cannot demonstrate a 31-tile
column, and the smoke's fixture wheels are far smaller than that, so the whole
class was unreachable by construction. `_column_cases` therefore sweeps the real
drum at the real window heights (430px rest, the 900px full-screen clamp) across
the whole rendered slot range, and asserts on COUNTS, not on one lucky tile.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
WHEEL_MODEL_JS = WEB / "views" / "wheel-model.js"
WHEEL_JS = WEB / "views" / "wheel.js"
STYLES_CSS = WEB / "styles.css"
NODE = shutil.which("node")

# wheel.js's own constants, restated so a drift in either fails here.
TILE_W = 196
TILE_H = 56
WIN_REST = 430

_NODE_HARNESS = """
import { tileBox, inReelWindow, threadAnchorX, endpointScale, badgeRailBand,
  bandsOverlap, tileScale, drumProject, REEL, EXPANDED } from './wheel-model.mjs';
import { readFileSync } from 'node:fs';

// THE cylinder projection — the real one, imported (2026-08-03). This harness
// used to carry its own transcription of wheel.js's private `drum()`, with a
// comment admitting that if the two ever disagreed these counts would stop
// meaning anything. They cannot disagree now: the projection was lifted into
// wheel-model.js as `drumProject` when the docs pane's wheel became a second
// caller, and this calls it.
function drum(d, bulged, winH, drumF, scaleF) {
  return drumProject({ d, bulged, winH, drumF, scaleF });
}

const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = {};

// ---- a whole rendered column, at the real drum -------------------------------
for (const [id, winH, drumF, scaleF, focusWheel, radius] of cases.columns) {
  const tiles = [];
  for (let d = -radius; d <= radius; d++) {
    const c = drum(d, focusWheel, winH, drumF, scaleF);
    const y = winH / 2 + c.y;
    const box = tileBox({ y, squash: c.squash, tileH: TILE_H_ * scaleF,
                          scale: tileScale(d, focusWheel) });
    tiles.push({ d, top: box.top, bottom: box.bottom, over: c.over,
                 inWindow: inReelWindow(box, winH, c.over) });
  }
  out[id] = {
    rendered: tiles.length,
    inWindow: tiles.filter((t) => t.inWindow).length,
    // a tile the predicate calls IN must actually intersect [0, winH]
    liars: tiles.filter((t) => t.inWindow && (t.bottom <= 0 || t.top >= winH)).length,
    // ...and one it calls OUT must be wholly outside it
    misses: tiles.filter((t) => !t.inWindow && t.bottom > 0 && t.top < winH
                                && !t.over).length,
    aboveWindow: tiles.filter((t) => t.bottom <= 0).length,
    belowWindow: tiles.filter((t) => t.top >= winH).length,
    tiles,
  };
}

// ---- thread anchors against the endpoint's REAL card -------------------------
out.anchors = cases.anchors.map(([id, d, focusWheel, expanded, scaleF]) => {
  const scale = endpointScale(d, focusWheel, expanded);
  const centreX = 500;
  const half = (TILE_W_ / 2) * scaleF * scale;   // the card's own half-width
  const right = threadAnchorX(centreX, true, TILE_W_ * scaleF, scale);
  const left = threadAnchorX(centreX, false, TILE_W_ * scaleF, scale);
  return { id, scale, half,
           rightInset: (centreX + half) - right,   // >0 means INSIDE the card
           leftInset: left - (centreX - half) };
});

// ---- the badge rail's band against the reel -----------------------------------
out.rail = cases.rails.map(([id, winH, scaleF, expandedH]) => {
  const band = badgeRailBand(winH, scaleF, expandedH);
  const covered = [];
  for (let d = -3; d <= 3; d++) {
    const c = drum(d, true, winH, 1, scaleF);
    const y = winH / 2 + c.y;
    const box = tileBox({ y, squash: c.squash, tileH: TILE_H_ * scaleF,
                          scale: tileScale(d, true) });
    if (bandsOverlap(box, band)) covered.push(d);
  }
  return { id, band, covered };
});

out.constants = { spacing: REEL.spacing, bulge: REEL.bulge,
                  expandedScale: EXPANDED.scale };
console.log(JSON.stringify(out));
"""


def _run(cases, tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    harness = (_NODE_HARNESS
               .replace("TILE_H_", str(TILE_H))
               .replace("TILE_W_", str(TILE_W)))
    (tmp_path / "harness.mjs").write_text(harness, encoding="utf-8")
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# (id, winH, drumFactor, wheelScale, isFocusWheel, rendered radius)
#
# The radius is wheel.js's own: max(REEL.visible, ceil((pi/2)*winH /
# (spacing*scale))) + 1, so `rendered` below is the real per-column tile count —
# 31 at the rest height, which is exactly what the sweep hit-tested.
COLUMNS = [
    ("rest-focus", WIN_REST, 1, 1, True, 13),
    ("rest-pulled", WIN_REST, 1, 1, False, 13),
    ("tall-focus", 900, 1, 1, True, 25),
    ("fullscreen", 900, 1, 1.33, True, 19),
    ("tight-drum", WIN_REST, 0.3, 1, True, 13),
]

ANCHORS = [
    ("focused", 0, True, False, 1),
    ("expanded", 0, True, True, 1),
    ("resting-focus-wheel", 3, True, False, 1),
    ("pulled", 1, False, False, 1),
    ("expanded-fullscreen", 0, True, True, 1.33),
]

RAILS = [
    ("focused", WIN_REST, 1, None),
    ("expanded", WIN_REST, 1, 132),
    ("expanded-with-summary", WIN_REST, 1, 144),
]

CASES = {"columns": [list(c) for c in COLUMNS],
         "anchors": [list(a) for a in ANCHORS],
         "rails": [list(r) for r in RAILS]}


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    return _run(CASES, tmp_path_factory.mktemp("wheel-paint"))


# ---------------------------------------------------------------------------
# defect 6 — off-window tiles
# ---------------------------------------------------------------------------

def test_a_real_column_renders_far_more_tiles_than_the_window_holds(measured):
    """The premise, asserted so the rest of this file is not measuring a
    two-tile fixture. 27 rendered against 7 in the window at the rest height is
    the sweep's own shape (it counted 31 and 7 at its viewport)."""
    col = measured["rest-focus"]
    assert col["rendered"] >= 27, col["rendered"]
    assert col["inWindow"] <= 9, col["inWindow"]
    assert col["rendered"] - col["inWindow"] >= 18, \
        "the fixture is too small to demonstrate the defect"


@pytest.mark.parametrize("case", [c[0] for c in COLUMNS])
def test_the_window_predicate_matches_the_rendered_box_exactly(measured, case):
    """No tile is called visible whose box is outside the window, and no tile
    intersecting the window is called invisible. This is the assertion the two
    clips could not make: they hid the tiles from paint and from the mouse while
    the tab order kept all 31."""
    col = measured[case]
    assert col["liars"] == 0, f"{case}: tiles reported in-window that are not"
    assert col["misses"] == 0, f"{case}: visible tiles reported out-of-window"


@pytest.mark.parametrize("case", [c[0] for c in COLUMNS if c[0] != "tight-drum"])
def test_tiles_are_laid_out_on_both_sides_of_the_window(measured, case):
    """The sweep found them ABOVE the window, over the page chrome. Both
    directions exist at the default drum, so the predicate is exercised on
    both."""
    col = measured[case]
    assert col["aboveWindow"] > 0, f"{case}: nothing above the window to exclude"
    assert col["belowWindow"] > 0, f"{case}: nothing below the window to exclude"


def test_a_tight_drum_excludes_by_the_horizon_instead(measured):
    """The other exclusion route, which the knob's low end is entirely made of:
    at drum 0.3 the reel wraps inside the window, so an out-of-window tile is
    one PAST THE HORIZON (drawn at opacity 0) rather than one placed over the
    page chrome. Both routes must reach the same `tabindex`/`aria-hidden`
    decision, which is why `inReelWindow` takes `over` at all."""
    col = measured["tight-drum"]
    excluded = [t for t in col["tiles"] if not t["inWindow"]]
    assert excluded, "the tight drum excludes nothing"
    assert all(t["over"] for t in excluded), \
        "a tight-drum tile was excluded for a reason other than the horizon"


def test_the_centre_tile_is_always_in_the_window(measured):
    for case, *_ in COLUMNS:
        centre = next(t for t in measured[case]["tiles"] if t["d"] == 0)
        assert centre["inWindow"], f"{case}: the focus line is outside the window"


def test_focusability_and_hit_testing_come_from_the_one_predicate():
    """wheel.js's half. `tabindex`, `aria-hidden` and the pointer-events class
    are all driven from `inReelWindow` — three attributes that used to disagree,
    now one decision. A blank filler slot is never a tab stop."""
    src = WHEEL_JS.read_text(encoding="utf-8")
    block = src.split("function layoutTile(", 1)[1].split("\n  }", 1)[0]
    assert "inReelWindow(box, winH, c.over)" in block
    assert 'tile.tabIndex = onWindow ? 0 : -1' in block
    assert 'tile.setAttribute("aria-hidden", "true")' in block
    assert 'tile.removeAttribute("aria-hidden")' in block
    assert 'tile.classList.toggle("wheeloffwindow", !onWindow)' in block
    assert 'tile.getAttribute("role") === "button"' in block, \
        "a blank filler slot would be pulled into the tab order"


def test_an_off_window_tile_takes_no_pointer_events():
    css = STYLES_CSS.read_text(encoding="utf-8")
    assert ".wheeltile.wheeloffwindow { pointer-events: none; }" in css


# ---------------------------------------------------------------------------
# defect 14a — the edge bundle over the expanded card
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", [a[0] for a in ANCHORS])
def test_a_thread_never_starts_inside_the_card_it_anchors_to(measured, case):
    """The whole defect in one assertion. A positive inset means the anchor is
    INSIDE the endpoint's own box — which is how the teal bundle crossed the
    expanded card's left border and struck through its health line."""
    anchor = next(a for a in measured["anchors"] if a["id"] == case)
    assert anchor["rightInset"] <= 0.001, \
        f"{case}: the thread starts {anchor['rightInset']:.1f}px inside the card"
    assert anchor["leftInset"] <= 0.001, \
        f"{case}: the thread starts {anchor['leftInset']:.1f}px inside the card"


def test_the_anchor_tracks_the_endpoints_own_magnification(measured):
    """Not merely 'outside' — AT the edge, so the locked prototype's
    edge-anchored curvature is preserved rather than pushed off the tile."""
    byid = {a["id"]: a for a in measured["anchors"]}
    assert byid["expanded"]["scale"] == pytest.approx(measured["constants"]["expandedScale"])
    assert byid["focused"]["scale"] == pytest.approx(1.35)
    assert byid["pulled"]["scale"] == pytest.approx(0.95)
    # the expanded card really is wider than the resting one the old anchor used
    assert byid["expanded"]["half"] > TILE_W / 2 + 30


def test_every_thread_endpoint_goes_through_the_one_anchor_helper():
    """wheel.js's half: no hand-rolled `(TILE_W / 2) * scaleF` survives, in
    either the first-degree or the second-degree pass."""
    src = WHEEL_JS.read_text(encoding="utf-8")
    threads = src.split("function drawThreads(", 1)[1].split("\n  }", 1)[0]
    assert "(TILE_W / 2)" not in threads, \
        "a thread endpoint still anchors at the RESTING half-width"
    assert threads.count("threadAnchorX(") == 4
    assert threads.count("endpointScale(") == 4


# ---------------------------------------------------------------------------
# defect 14b — the badge rail over the next tile
# ---------------------------------------------------------------------------

def test_the_rail_really_does_cross_a_reel_tile(measured):
    """The premise. The rail sits 8px below the focused box and the next tile
    starts ~6px later, so it overlaps — and reserving the 13px would mean moving
    Brett's locked reel spacing, which this change does not do."""
    focused = next(r for r in measured["rail"] if r["id"] == "focused")
    assert focused["covered"], "nothing to cede: the premise no longer holds"
    assert 0 not in focused["covered"], "the focused tile must never cede its own rail"


def test_the_expanded_rail_is_pushed_clear_of_its_own_card(measured):
    """The expanded posture already derives the rail offset from the one height
    knob; this pins that it clears the taller box rather than sitting behind it."""
    for case, expanded_h in (("expanded", 132), ("expanded-with-summary", 144)):
        band = next(r for r in measured["rail"] if r["id"] == case)["band"]
        half = (expanded_h / 2) * measured["constants"]["expandedScale"]
        assert band["top"] > WIN_REST / 2 + half, f"{case}: the rail is behind the card"


def test_the_covered_tile_is_ceded_the_way_a_parked_link_already_is():
    """wheel.js's half, and the CSS's. The rule is the one already in the file
    for a parked link — fade the covered tile so the floating chrome reads —
    applied to the rail's own band, and the chips take a solid backdrop in every
    posture instead of only the expanded one."""
    src = WHEEL_JS.read_text(encoding="utf-8")
    block = src.split("function drawWheel(", 1)[1].split("\n  }", 1)[0]
    assert "badgeRailBand(winH, scaleF" in block
    assert "bandsOverlap(box, railBand)" in block
    assert '!focused && !isExpanded' in block, \
        "the focused tile would fade itself out from under its own rail"
    css = STYLES_CSS.read_text(encoding="utf-8")
    assert ".wheelchip:not(:hover) {" in css
    assert ".wheeltile.wheelrailcovered { pointer-events: none; }" in css
    # the expanded-only backdrop rule is gone: it was the narrower half of this
    assert ".wheelwin:has(.wheeltile.wheelexpanded) .wheelchip:not(:hover)" not in css
