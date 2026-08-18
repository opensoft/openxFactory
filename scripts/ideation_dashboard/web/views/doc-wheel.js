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

// THE THREE TILE VERBS (add-doxbench-editing-phase-b, Q3 ruled: "add a load
// button. read will still pull up an imersive reader experience of the doc in a
// large window. the new <Edit> button will then load this into the chat context.
// Once loaded and editable by chat, color this tile so we know is must be saved.
// also add a save button here. So we have read, edit, save and save only active
// if there are changes. the save acts same as the save button that is in the
// preview panel.")
//
// The CONTRACT names are read / load-for-editing / save (design D8). `read`
// replaces Phase A's `open`, which is a naming debt Phase A opened deliberately:
// it reserved the bare word "edit" for editing that happens INSIDE the app so
// this verb could exist without a third claimant to the word. The visible label
// follows Brett's annotation.
export const DOC_TILE_VERBS = Object.freeze(["read", "load-for-editing", "save"]);

// The fixed sentences each unreachable verb states. Stated rather than failing
// on activation, which is the delta's own rule: "load and save MUST be
// unreachable and MUST state that absence rather than failing when activated".
const READ_UNAVAILABLE = "the read-only viewer is not available in this embedding";
const NOT_CATALOGUED = "not a catalogued corpus document";
const LOAD_UNAVAILABLE =
  "loading for editing needs the editing capability, which this surface does not have";
const SAVE_UNAVAILABLE =
  "the governed Save needs the editing capability, which this surface does not have";
const SAVE_CONTEXT_ONLY =
  "this document is read-only context in the opened tile, not the tile's own "
  + "material, so it is not offered to the governed Save";
const SAVE_NOT_LOADED =
  "load this document for editing before saving it";
const SAVE_NOTHING_TO_DO =
  "this document has no unsaved changes";

export function renderDocWheel(host, entries, opts = {}) {
  const onSelect = typeof opts.onSelect === "function" ? opts.onSelect : null;
  // `onRead` is the verb's contract name; `onOpen` is the retired Phase A
  // spelling, still accepted so a caller that has not been re-pointed keeps its
  // reader rather than losing it silently.
  const onRead = typeof opts.onRead === "function"
    ? opts.onRead
    : (typeof opts.onOpen === "function" ? opts.onOpen : null);
  const onLoad = typeof opts.onLoad === "function" ? opts.onLoad : null;
  const onSave = typeof opts.onSave === "function" ? opts.onSave : null;
  // LIVE buffer state for one path, or null. D9: the marking is driven off live
  // session-local buffer state and is NEVER persisted — "has an open unsaved
  // edit" is a fact about a browser, and the snapshot is a regenerated derived
  // projection whose generator cannot observe one.
  const bufferStateFor = typeof opts.bufferStateFor === "function"
    ? opts.bufferStateFor
    : () => null;
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
    // The loaded/loaded-and-dirty marking is applied on EVERY layout pass, to
    // every tile — expanded or not — because "this document has unsaved work" is
    // a fact a human must be able to see across the whole reel, not only on the
    // one tile they happen to have open.
    markTile(tile, entries[i]);

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

  // The expanded tile's action row: READ, LOAD FOR EDITING, SAVE. Expanding
  // brings them INSIDE the tile instead of requiring the human to find them
  // elsewhere, which is what expansion is for.
  //
  // The row is REBUILT on every expanded layout pass rather than mutated,
  // because Save's reachability is a function of live buffer state and a control
  // whose enabled state lagged the buffer it governs would be the one thing this
  // row must never be: wrong about whether work is unsaved.
  function mountActions(tile, i) {
    const existing = tile.querySelector(".wheelactions");
    if (existing) existing.remove();
    const row = el("div", "wheelactions");
    const entry = entries[i];
    const live = bufferStateFor(entry.path) || null;
    const loaded = Boolean(live && live.loaded);
    const dirty = Boolean(live && live.dirty);
    // OWNERSHIP is the tile's own answer about its material, and a live buffer's
    // answer wins when one exists (design D2): a context-only document is
    // LOADABLE for grounding and conversation, and its buffer carries
    // `owned: false`, which the governed Save already withholds.
    const owned = live && typeof live.owned === "boolean"
      ? live.owned
      : entry.owned !== false;

    // ---- READ: unchanged. Needs no gate capability, so it stays available
    // wherever the document is catalogued at all.
    const read = el("button", "swb-docopen swb-docread", "read");
    read.type = "button";
    read.title = "read " + entry.path + " in the immersive read-only viewer";
    if (onRead && entry.resolved) {
      read.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onRead(entry.row, entry);
      });
    } else {
      read.disabled = true;
      read.title = entry.resolved ? READ_UNAVAILABLE : NOT_CATALOGUED;
    }
    row.appendChild(read);

    // ---- LOAD FOR EDITING: how a document JOINS the loaded set, and the ONLY
    // route in (design D5). Labelled with Brett's own word.
    const load = el("button", "swb-docload", loaded ? "loaded" : "edit");
    load.type = "button";
    if (onLoad && entry.resolved) {
      load.title = loaded
        ? entry.path + " is loaded for editing — selecting it here brings the "
          + "chat and the canvas back to it"
        : "load " + entry.path + " into the chat context for editing";
      load.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onLoad(entry.row, entry);
      });
    } else {
      load.disabled = true;
      load.title = entry.resolved ? LOAD_UNAVAILABLE : NOT_CATALOGUED;
    }
    row.appendChild(load);

    // ---- SAVE: the SAME governed pipeline the canvas Save reaches, scoped to
    // this document plus the outline-ancestry step (design D4). A second ENTRY
    // POINT, never a second save path, and it widens no authority: it is
    // reachable only while this document's buffer is dirty, and visibly inert
    // otherwise, so the control's own state answers "does this need saving"
    // without a sentence of standing text.
    const save = el("button", "swb-docsave", "save");
    save.type = "button";
    if (!onSave || !entry.resolved) {
      save.disabled = true;
      save.title = entry.resolved ? SAVE_UNAVAILABLE : NOT_CATALOGUED;
    } else if (!owned) {
      // D2: no reachable Save on a context-only tile, and — below — no
      // must-save marking either, because marking a document "must be saved"
      // when the tile may not save it would be a false statement about the
      // surface's own authority.
      save.disabled = true;
      save.title = SAVE_CONTEXT_ONLY;
    } else if (!loaded) {
      save.disabled = true;
      save.title = SAVE_NOT_LOADED;
    } else if (!dirty) {
      save.disabled = true;
      save.title = SAVE_NOTHING_TO_DO;
    } else {
      save.title = "save " + entry.path + " through the governed Save";
      save.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onSave(entry.row, entry);
      });
    }
    row.appendChild(save);
    tile.appendChild(row);
  }

  // THE TILE MARKING, in the wheel's existing class idiom rather than a second
  // visual language. Two states are distinguishable because Brett named both:
  // LOADED (the tile is in the chat context) and LOADED-AND-DIRTY (it must be
  // saved). A context-only document can be loaded but is never marked as needing
  // a save (design D2/D9).
  function markTile(tile, entry) {
    const live = bufferStateFor(entry.path) || null;
    const loaded = Boolean(live && live.loaded);
    const owned = live && typeof live.owned === "boolean"
      ? live.owned
      : entry.owned !== false;
    const needsSave = loaded && owned && Boolean(live && live.dirty);
    tile.classList.toggle("swb-docloaded", loaded);
    tile.classList.toggle("swb-docneedssave", needsSave);
    // Announced as well as coloured: colour alone is not an accessible state.
    if (needsSave) tile.setAttribute("data-doxbench-buffer", "loaded-dirty");
    else if (loaded) tile.setAttribute("data-doxbench-buffer", "loaded");
    else tile.removeAttribute("data-doxbench-buffer");
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
    // The pane's way of saying "the loaded set or a buffer's dirtiness moved":
    // re-lay-out so every tile's marking and the expanded tile's Save
    // reachability are re-derived from the live state. Nothing is cached here,
    // which is what makes the marking impossible to leave stale.
    refreshBufferState() {
      if (destroyed) return;
      layout();
    },
  };
}
