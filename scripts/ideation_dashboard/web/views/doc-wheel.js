// THE DOCS-PANE WHEEL — the deck's drum, one column, in a third of the height.
//
// Operator annotation `vibe_1785602331813_gvku9sh2s`: "make the lower half be
// the same wheel of the docs we have used before. set the wheel radius to .4 the
// size of the subpane holding the wheel ... the selected tile can second click
// to expand like our main wheel."
//
// WHY THIS IS A SEPARATE MODULE AND NOT A FLAG ON renderWheel. `renderWheel` is
// a ~1200-line closure that renders SIX columns as a carousel with linked-tile
// threads, a badge rail, anchored flyouts, per-wheel action mounters and paging.
// A docs pane wants one reel and none of that. Passing a "just one column, no
// chrome" flag through all of it would make the deck's hardest module carry a
// second mode for a caller that uses a tenth of it.
//
// WHY IT IS STILL "THE SAME WHEEL". Everything a human can perceive about the
// motion is shared code, not a copy:
//
//   * `drumProject` — THE cylinder projection, lifted out of wheel.js when this
//     module became its second caller. Both drums place tiles by one function,
//     so tuning either tunes both and they cannot drift.
//   * `nextExpanded` — THE locked click gesture. "Second click to expand like
//     our main wheel" is that reducer, so this reuses it rather than
//     re-deriving when a click focuses and when it expands.
//   * `inReelWindow` — THE visibility predicate that drives focusability. A
//     second drum is a second chance to repeat defect 6 (25 off-window tiles
//     left in the tab order); sharing the predicate is what prevents it.
//   * `tileScale`/`tileBox` and the `.wheeltile` classes, so it reads and
//     measures like the deck. Opacity follows the deck's rule rather than the
//     exported `tileOpacity`, which is the older FLAT-reel curve the drum
//     superseded: a cylinder fades by its own foreshortening.
//
// WHY 0.4. The drum places tiles at `winH/2 ± R` for `R = winH × drumF`. At the
// deck's default 1.0 that spans `[-0.5·winH, 1.5·winH]`: most of a column is
// laid out outside its own window and survives only because the clip hides it —
// affordable in a 430px deck window, useless in a ~380px pane where the whole
// reel would be off-screen. At 0.4 the span is `[0.1·winH, 0.9·winH]`: every
// tile lands INSIDE the subpane, and tiles leave by wrapping over the drum's own
// horizon instead of running off the end. That is the operator's number, and it
// is the number that makes a drum work at this size.
import {
  drumProject, tileBox, tileScale, inReelWindow,
  nextExpanded, isExpandedTile, EXPANDED, SPRING,
} from "./wheel-model.js";
import { el } from "./helpers.js";

// `key` is the wheel identity `nextExpanded` reduces over. This drum has one
// column, so one constant name is the whole namespace.
export const DOC_WHEEL = Object.freeze({
  drumF: 0.4,
  tileH: 56,   // matches .wheeltile's CSS height, as the deck's TILE_H does
  key: "docs",
});

// Below this the pane is mid-layout (display:none, a pane not yet sized, the
// first frame before the split resolves). Projecting against a zero height
// divides by zero and lands every tile on one pixel, so we simply wait for the
// ResizeObserver to report a real box.
const MIN_WIN_H = 40;

// Do two `{key, i}` cells refer to the same tile? (Either being null is the
// "nothing expanded" state, so identity is the right comparison there.)
function sameCell(a, b) {
  if (!a || !b) return a === b;
  return a.key === b.key && a.i === b.i;
}

export function renderDocWheel(host, entries, opts = {}) {
  const onSelect = typeof opts.onSelect === "function" ? opts.onSelect : null;
  const onOpen = typeof opts.onOpen === "function" ? opts.onOpen : null;
  const drumF = Number.isFinite(opts.drumF) ? opts.drumF : DOC_WHEEL.drumF;

  host.innerHTML = "";
  host.classList.add("swb-docwheel");

  if (!entries.length) {
    host.appendChild(el("div", "swb-empty",
      "this scope resolves no documents in the snapshot"));
    return { destroy() {}, focused: () => null };
  }

  host.setAttribute("role", "listbox");
  host.setAttribute("aria-label", "documents in this scope");
  host.tabIndex = 0;

  const port = el("div", "swb-docwheelport");
  host.appendChild(port);

  // ---- state ----
  let pos = 0;              // live centre index (fractional while spinning)
  let target = 0;           // the index being sprung toward
  let vel = 0;
  let expanded = null;      // { key, i } | null — at most one, per the reducer
  let winH = 0;
  let raf = null;
  let destroyed = false;

  const tiles = entries.map((entry, i) => buildTile(entry, i));

  function buildTile(entry, i) {
    // A DIV with role=option, not a <button>: the expanded tile hosts a real
    // button inside itself, and a button nested in a button is invalid HTML
    // whose inner activation browsers do not deliver — the same reason the deck
    // uses role=button divs.
    const tile = el("div", "wheeltile swb-doctile");
    tile.setAttribute("role", "option");
    tile.setAttribute("aria-selected", "false");
    tile.setAttribute("aria-expanded", "false");
    tile.tabIndex = -1;
    if (!entry.resolved) tile.classList.add("swb-doctile-unresolved");
    if (entry.inherited) tile.classList.add("swb-doctile-inherited");
    tile.appendChild(el("span", "wheellabel", entry.label));
    // The sub-line carries what the section headings used to say. An inherited
    // document is not this tile's own and must keep saying so.
    const bits = [entry.section];
    if (entry.stage) bits.push(entry.stage);
    if (entry.kind) bits.push(entry.kind);
    const sub = el("span", "wheelsub", bits.filter(Boolean).join(" · "));
    // The completeness score sits where the deck's tiles show link degree, and
    // an unscored document shows the deck's "·" rather than a misleading 0.
    const score = el("span", "wheeldegree",
      entry.score === null ? "·" : entry.score.toFixed(2));
    score.title = entry.score === null
      ? "not scored in this snapshot"
      : "completeness score " + entry.score + " (structural, not a quality verdict)";
    sub.appendChild(score);
    tile.appendChild(sub);
    tile.title = entry.path;
    tile.addEventListener("click", (ev) => {
      // a click on the expanded tile's own action is that action's, not the
      // tile's (the button also stops propagation; this is the backstop)
      if (ev.target !== tile && ev.target.closest?.(".wheelactions")) return;
      activate(i, tile);
    });
    tile.addEventListener("keydown", (ev) => {
      if (ev.target !== tile) return;
      if (ev.key !== "Enter" && ev.key !== " ") return;
      ev.preventDefault();   // Space must not scroll the pane
      activate(i, tile);
    });
    port.appendChild(tile);
    return tile;
  }

  // THE GESTURE, deferred to the locked reducer: a click on a tile that is not
  // on the line focuses it; a click once it IS on the line expands it; a click
  // on the expanded tile collapses it. `centred` is read off the class layout
  // stamps, so the gesture and the rendering agree by construction — the deck's
  // rule, for the same reason.
  function activate(i, tile) {
    const centred = tile.classList.contains("wheelfocused");
    const next = nextExpanded(expanded, { type: "tile", key: DOC_WHEEL.key, i, centred });
    const changed = !sameCell(next, expanded);
    expanded = next;
    if (!centred) setFocus(i);
    if (changed) layout();
  }

  function setFocus(i) {
    const next = Math.max(0, Math.min(entries.length - 1, i));
    if (next === target) return;
    target = next;
    // Spinning away from an expanded tile collapses it, exactly as the deck's
    // "spin" event does.
    expanded = nextExpanded(expanded, { type: "spin", key: DOC_WHEEL.key });
    if (onSelect) onSelect(entries[target], target);
    start();
  }

  // ---- the spring, and the frame ----
  // NO ANIMATION FRAME, NO ANIMATION — but still a correct wheel. The shell is
  // also mounted headlessly (the node shell harness, and any embedding without
  // a compositor), where `requestAnimationFrame` does not exist. Spinning then
  // SNAPS to the target instead of springing to it: the reel lands in exactly
  // the place it would have sprung to, so selection, focusability and the
  // gesture stay correct and only the motion is absent.
  const RAF = typeof requestAnimationFrame === "function"
    ? requestAnimationFrame : null;

  function start() {
    if (destroyed) return;
    if (!RAF) { pos = target; vel = 0; layout(); return; }
    if (raf !== null) return;
    raf = RAF(step);
  }

  function step() {
    raf = null;
    const { k, damping } = SPRING.driven;
    vel += (target - pos) * k;
    vel *= damping;
    pos += vel;
    if (Math.abs(target - pos) < 0.001 && Math.abs(vel) < 0.001) {
      pos = target; vel = 0;
    } else {
      start();
    }
    layout();
  }

  function layout() {
    if (destroyed) return;
    winH = host.clientHeight;
    // THE FINITENESS CHECK IS THE POINT, not the comparison. A bare
    // `winH < MIN_WIN_H` is FALSE for `undefined` and for `NaN`, so a host that
    // cannot be measured — display:none, a pane not yet sized, a DOM stub with
    // no layout — would sail past the guard and get divided by, placing every
    // tile at NaN. Stated explicitly so it reads as deliberate.
    if (!Number.isFinite(winH) || winH < MIN_WIN_H) return; // observer calls back
    for (let i = 0; i < tiles.length; i++) {
      layoutTile(tiles[i], i - pos, i);
    }
  }

  function layoutTile(tile, d, i) {
    const c = drumProject({ d, bulged: true, winH, drumF, scaleF: 1 });
    const y = winH / 2 + c.y;
    const s = tileScale(d, true);
    const isExpanded = isExpandedTile(expanded, DOC_WHEEL.key, i);
    const box = tileBox({
      y, squash: c.squash, tileH: DOC_WHEEL.tileH, scale: s, expanded: isExpanded,
    });
    // DEFECT 6, which cost a keyboard user 45 Tab presses to reach the second of
    // six columns: the clip stopped off-window tiles painting and stopped the
    // mouse, and left every one of them in the tab order. One predicate drives
    // focusability, aria-hidden and pointer-events, so keyboard and mouse agree
    // with what is visible. An expanded tile is on the axis by construction.
    const onWindow = isExpanded || inReelWindow(box, winH, c.over);
    tile.tabIndex = onWindow ? 0 : -1;
    if (onWindow) tile.removeAttribute("aria-hidden");
    else tile.setAttribute("aria-hidden", "true");
    tile.classList.toggle("wheeloffwindow", !onWindow);

    const centred = Math.abs(d) < 0.5;
    tile.classList.toggle("wheelfocused", centred);
    tile.setAttribute("aria-selected", centred ? "true" : "false");
    tile.setAttribute("aria-expanded", isExpanded ? "true" : "false");
    tile.classList.toggle("wheelexpanded", isExpanded);

    if (isExpanded) {
      tile.style.transform = "translate(0, " + y.toFixed(1) + "px) translateY(-50%) " +
        "scale(" + EXPANDED.scale.toFixed(3) + ")";
      tile.style.opacity = "1";
      tile.style.zIndex = "9";
      mountActions(tile, i);
    } else {
      tile.style.transform = "translate(0, " + box.translateY.toFixed(1) + "px) " +
        "scale(" + s.toFixed(3) + ", " + (s * c.squash).toFixed(3) + ")";
      // FADE BY THE DRUM'S OWN FORESHORTENING, and paint NOTHING past the
      // horizon — the deck's rule, and measurement is why it is here. The reel
      // wraps at a 0.4 radius long before it runs out of tiles, so the tiles
      // beyond the horizon all stack on the two poles: 12 tiles rendered at 5
      // distinct positions. Faded to a floor they would have smeared a pile of
      // ghost tiles across the top and bottom of the pane. `over` is the drum
      // saying "this one is round the back", and the answer is opacity 0.
      const cosFade = Math.min(1, Math.max(0.15, c.squash));
      tile.style.opacity = c.over ? "0" : cosFade.toFixed(2);
      // Nearer the line paints over further from it, so the pile at each pole
      // cannot cover the tiles a human is actually reading.
      tile.style.zIndex = String(Math.max(0, 20 - Math.round(Math.abs(d))));
      const actions = tile.querySelector(".wheelactions");
      if (actions) actions.remove();
    }
  }

  // The expanded tile's action row. The docs pane's one verb is the read-only
  // viewer it has always offered — expanding brings it INSIDE the tile instead
  // of requiring the human to find it elsewhere, which is what expansion is for.
  function mountActions(tile, i) {
    if (tile.querySelector(".wheelactions")) return;
    const row = el("div", "wheelactions");
    const entry = entries[i];
    const open = el("button", "swb-docopen", "open");
    open.type = "button";
    open.title = "open " + entry.path + " in the read-only source viewer";
    if (onOpen && entry.resolved) {
      open.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onOpen(entry.row, entry);
      });
    } else {
      open.disabled = true;
      open.title = entry.resolved
        ? "the read-only viewer is not available in this embedding"
        : "not a catalogued corpus document";
    }
    row.appendChild(open);
    tile.appendChild(row);
  }

  // ---- input ----
  function onKeyDown(ev) {
    let handled = true;
    if (ev.key === "ArrowDown") setFocus(target + 1);
    else if (ev.key === "ArrowUp") setFocus(target - 1);
    else if (ev.key === "Home") setFocus(0);
    else if (ev.key === "End") setFocus(entries.length - 1);
    else if (ev.key === "Escape" && expanded) {
      expanded = nextExpanded(expanded, { type: "collapse" });
      layout();
    } else handled = false;
    if (handled) ev.preventDefault();
  }

  function onWheelEvent(ev) {
    ev.preventDefault();
    setFocus(target + (ev.deltaY > 0 ? 1 : -1));
  }

  host.addEventListener("keydown", onKeyDown);
  host.addEventListener("wheel", onWheelEvent, { passive: false });

  // THE HEIGHT TRAP, twice paid for on this surface: a pane measured at mount is
  // routinely still zero, and a wheel laid out against zero puts every tile on
  // one line and never recovers. Observe the host and lay out whenever it has a
  // real box.
  let observer = null;
  if (typeof ResizeObserver === "function") {
    observer = new ResizeObserver(() => layout());
    observer.observe(host);
  }
  layout();
  if (onSelect) onSelect(entries[0], 0);

  return {
    destroy() {
      destroyed = true;
      if (raf !== null && typeof cancelAnimationFrame === "function") {
        cancelAnimationFrame(raf);
      }
      raf = null;
      if (observer) observer.disconnect();
      host.removeEventListener("keydown", onKeyDown);
      host.removeEventListener("wheel", onWheelEvent);
    },
    focused: () => entries[target] || null,
    // exposed for the pane: select by path when something else changes selection
    selectPath(path) {
      const i = entries.findIndex((e) => e.path === path);
      if (i >= 0) setFocus(i);
    },
  };
}
