// THE WHEEL — the funnel-navigation deck (locked interaction spec, Track C,
// Brett-approved 2026-07-16; ideation-dashboard brainstorm). This realization
// is a FAITHFUL PORT of the locked prototype's mechanics (the "THE WHEEL —
// Ideation Funnel Navigator" mockup, recovered 2026-07-22 and preserved at
// the workspace root as wheel-original.html): flat reels with a tanh bulge
// and a CONTINUOUS magnification curve on the focused wheel only, a 40px
// scroll accumulator for whole-tile spins, live spring–damper elastic pulls
// (driven .020/.84, pulled .008/.90), balanced alignment that never seats a
// linked tile dead on the line, class-coded bezier threads anchored at tile
// edges, a badge rail of connection chips BELOW the focused centre tile, a
// discrete column carousel, and column hiding shipping BOTH candidate-3
// affordances (header eye -> thin rail, dock chips) over one state.
//
// Rendering is snapshot-only through the PURE wheel-model.js derivation; this
// module owns DOM, physics, and interaction. prefers-reduced-motion => every
// motion snaps instantly (no springs).
//
// EXPANDED TILES (Brett 2026-07-25) are an EXTENSION of that locked gesture,
// not a rework: a second click on the already-focused centre tile grows it in
// place and reveals its per-wheel ACTION ROW inside itself (the draft-proposal
// verb used to sit in the badge rail); every other tile click still just
// focuses. The state machine is the pure `nextExpanded` reducer and the verbs
// come from the pure WHEEL_ACTIONS table, both in wheel-model.js.
//
// The READ-ONLY verbs (Brett-approved 2026-07-25) ride the same extension point
// and carry NO capability gate, because none of them writes anything:
//   documents  read     -> the read-only source viewer (nav callback)
//   clusters   lens     -> the keyword lens, this cluster's topics checked
//   clusters   canvas   -> the cluster canvas, this cluster selected
//   staged     read     -> the SAME verb, pointed at the topic's primary
//                          fragment (the staged snapshot item carries file
//                          paths, not text)
//   active     packet   -> review the proposal packet: the change's own files,
//                          grouped proposal/design/tasks -> spec deltas ->
//                          the rest, each one a jump into the viewer
//   archived   landed   -> what actually landed: the archived change's
//                          spec-delta requirement headings, read through the
//                          viewer's own /source pass-through and summarised in
//                          an anchored flyout (a requirement list never fits a
//                          196x132 tile on a spinning drum).
// Both flyout verbs (landed · packet) share ONE anchored-panel scaffold
// (openFlyout below) — the panel chrome, the anchoring, and the teardown are the
// same problem; only the body differs.
//
// The expanded STAGED tile additionally carries a 3-LINE SUMMARY of its primary
// fragment (Brett 2026-07-25): the focus workspace is where a human decides what
// to work on, and the tile's staging id alone does not say what the topic IS. The
// text is read through the same /source pass-through, extracted by the PURE
// `fragmentSummary`, rendered textContent-only, and cached per session so
// re-expanding a tile never refetches.
//
// The one WRITING verb besides propose is the EXISTING SET-level "Open in
// NotebookLM" action (Brett 2026-07-25), surfaced here on the three set-bearing
// wheels (clusters / staged / active) with NO new transport: notebook.js's
// shared controller — the one app.js already hands the funnel, board, and canvas
// cards — renders the button, its pending state, the opened URL, and the
// structured refusal, so this view only maps a wheel to the backend's tile kind.

import { actionRowIsStale,
  buildWheelModel, connectionsOf, secondDegreeOf, gatherOf, alignTarget, computeReorder,
  SPRING, REEL, tileScale, linkedDrawDistance, actionsFor,
  nextExpanded, isExpandedTile, EXPANDED, WHEEL_KEYS, WHEEL_LABELS,
  tileBox, inReelWindow, drumProject, threadAnchorX, endpointScale, badgeRailBand, bandsOverlap,
  LANDED_KINDS, landedFromDeltas, specDeltaPaths,
  primaryFragmentPath, fragmentSummary, packetGroups,
  healthIndicator, healthBlock, jumpRepository } from "./wheel-model.js";
import { el } from "./helpers.js";
import { appliedOutcome, commissionedVerb, commissionedWorkflow, gateCapable,
  mountDisposeTray, mountProposeButton, mountWheelVerb } from "./dispose.js";
import { notebookCapable } from "./notebook.js";
import { SETTINGS_EVENT, currentDrumFactor } from "./settings.js";

const WIN_H = 430;       // wheel viewport rest height, px (CSS .wheelwin height)
const TILE_W = 196;      // tile width, px (CSS .wheeltile width)
const TILE_H = 56;       // resting tile height, px (CSS .wheeltile height)
const WHEEL_PIXELS_PER_STEP = 40;  // scroll accumulator: one tile per 40px
// The read-only source pass-through (serve.py, D15) — the SAME route the viewer
// reads document content from, and this view's only network read: the archived
// wheel's `landed` verb fetches spec-delta text through it, and the staged
// wheel's expanded tile fetches its primary fragment. ONE call site
// (`readSource`) serves both, so the bundle keeps exactly one fetch per route.
// The static served image has no such route; each reader then reports it inline,
// like the viewer's no-shim message.
const SOURCE_ROUTE = "/source/";
// The ACTIVE entry's keyed base (`/source/<repository>@<ref>/`), handed down by
// the app shell so a read resolves through THAT (repository, ref) entry's own
// root (add-dashboard-repo-selector task 2.2). Defaults to the plain route,
// which is what a single-repository serve and a bare embedding both mean.
let sourceBase = SOURCE_ROUTE;

// Read one repo-relative path through the pass-through. Never throws: an
// unreachable route (the served static image), a 404, or a read error all return
// null, and the caller degrades quietly.
async function readSource(path) {
  try {
    const response = await fetch(sourceBase + path, { cache: "no-store" });
    if (!response.ok) return null;
    return await response.text();
  } catch {
    return null;
  }
}

// The staged wheel's fragment SUMMARIES, cached for the SESSION (keyed by
// staging_id): re-expanding a tile — or expanding it after a spin took it away —
// must not refetch. A miss is stored too (`{ failed: true }`), so an unreachable
// /source is reported once and never retried per click. The snapshot is loaded
// once per page, so a cache entry can never outlive the text it summarises.
const summaryCache = new Map();

// The expanded tile's action row, DOM half of the extension point whose pure
// half is wheel-model.js's WHEEL_ACTIONS table: action id -> mounter. Adding a
// per-wheel verb is one row THERE plus one entry HERE; each mounter owns its own
// chrome and transport and receives `compact: true` so its button fits the row.
//
// The read-only verbs (read / lens / canvas) do no transport at all: they call
// the NAV callbacks the app shell threads in (`ctx.nav`), because app.js owns
// every cross-view wiring in this bundle (it is what wires the explorer to the
// viewer). `landed` is the one read verb with a data path of its own — the
// /source pass-through above, parsed by the pure `landedFromDeltas`; `packet`
// opens the same kind of flyout straight from snapshot data.
const ACTION_MOUNTERS = {
  propose: (row, item, opts) => mountProposeButton(row, item, { ...opts, compact: true }),
  // 011 add-wheel-action-verbs: one generic mounter, four verbs. `actionId` is
  // the verb, so the mounter needs no per-verb branch here.
  "promote-to-staging": (row, item, opts) =>
    mountWheelVerb(row, item, { ...opts, verb: "promote-to-staging" }),
  "research-brief": (row, item, opts) =>
    mountWheelVerb(row, item, { ...opts, verb: "research-brief" }),
  "derive-possibles": (row, item, opts) =>
    mountWheelVerb(row, item, { ...opts, verb: "derive-possibles" }),
  demote: (row, item, opts) =>
    mountWheelVerb(row, item, { ...opts, verb: "demote" }),
  // add-project-merged-projection (D10): the composed view's ONE verb — jump
  // to the tile's member repository (store the key + reload, the ratified
  // selector posture). Pure navigation; nothing is recorded or persisted.
  "open-repo": (row, item, opts) => {
    const repository = jumpRepository(item);
    const btn = el("button", "disposebtn dispose-intile wheelnavbtn",
      "⤴ open in " + repository);
    btn.type = "button";
    btn.title = "switch the active snapshot to this tile's repository";
    btn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      opts.nav?.openRepository?.(repository);
    });
    row.appendChild(btn);
    return btn;
  },
  read: (row, item, opts) => {
    const path = readPathOf(opts.wheelKey, item);
    return mountNavButton(row, {
      label: opts.label,
      title: opts.wheelKey === "staged"
        ? "open this topic's primary fragment in the read-only source viewer"
        : "open this document in the read-only source viewer",
      // no resolvable path (a staged topic with no markdown fragment) is the same
      // posture as no nav callbacks: DISABLED, never a live button that no-ops
      run: path && opts.nav?.openDoc &&
        (() => opts.nav.openDoc(
          path, opts.wheelKey === "documents" ? item.ref : null, item.ref)),
    });
  },
  lens: (row, item, opts) => mountNavButton(row, {
    label: opts.label,
    title: "open the keyword lens with this cluster's declared topics checked",
    run: opts.nav?.openLens && (() => opts.nav.openLens(item.ref?.topics || [], item.id)),
  }),
  canvas: (row, item, opts) => mountNavButton(row, {
    label: opts.label,
    title: "open the cluster canvas on this cluster",
    run: opts.nav?.openCanvas && (() => opts.nav.openCanvas(item.id)),
  }),
  landed: (row, item, opts) => mountFlyoutButton(row, item, opts),
  packet: (row, item, opts) => mountFlyoutButton(row, item, opts),
  notebook: (row, item, opts) => mountNotebookButton(row, item, opts),
  // The STAGING WORKBENCH verb (add-staging-workbench D6): a read-only nav verb
  // like read/lens/canvas — no transport of its own, just the app shell's
  // openWorkbench callback, and DISABLED (never a live no-op) when the shell
  // supplied no nav callbacks (a bare embedding).
  workbench: (row, item, opts) => mountNavButton(row, {
    label: opts.label,
    title: "open the staging workbench scoped to this " +
      (WORKBENCH_TILE_KINDS[opts.wheelKey] || "tile") + " (read-only)",
    run: WORKBENCH_TILE_KINDS[opts.wheelKey] && opts.nav?.openWorkbench &&
      (() => opts.nav.openWorkbench(WORKBENCH_TILE_KINDS[opts.wheelKey], item.id)),
  }),
};

// The wheel -> staging-workbench scope-kind map for the three TOPIC-BEARING
// wheels (the workbenchScope derivation's own kind vocabulary). documents /
// active / archived are absent by design: their tiles are not topic-bearing,
// and the pure table offers them no row anyway.
const WORKBENCH_TILE_KINDS = { clusters: "cluster", possibles: "possible", staged: "staged" };

// The two flyout verbs' chrome, by action id: the button's tooltip and the
// pending label it wears while a read is in flight ("" = no read, so no pending
// state — `packet` renders straight from the snapshot).
const FLYOUT_VERBS = {
  landed: {
    title: "what landed: the archived change's spec-delta requirements",
    pending: "reading…",
  },
  packet: {
    title: "review the proposal packet: proposal, design, tasks, and spec deltas",
    pending: "",
  },
};

// The wheel -> notebook_action.py TILE_KINDS map for the three SET-bearing
// wheels. A wheel item's `id` IS the tile id the backend resolves against the
// current snapshot (clusters -> cluster id, staged -> staging_id, active ->
// change id — see buildItems in wheel-model.js), so no per-wheel id plumbing is
// needed. documents/archived are absent by design: the action is SET-level and
// realized changes are deliberately out of scope.
const NOTEBOOK_TILE_KINDS = { clusters: "cluster", staged: "staged", active: "proposal" };

// The repo-relative path the `read` verb opens, per wheel. A DOCUMENT tile is a
// document: the catalogued path when the snapshot carries one, else the item id
// (which IS the path for documents). A STAGED tile is a topic FOLDER: the verb
// opens its primary fragment (the pure path selector), and there may be none.
function readPathOf(wheelKey, item) {
  if (wheelKey === "staged") return primaryFragmentPath(item?.id, item?.ref?.files);
  return item?.ref?.path || item?.id || "";
}

// A read-only verb's button: the in-tile propose button's compact chrome minus
// any transport. `run` is falsy when the app shell supplied no nav callbacks (an
// embedding without app.js) — the verb then shows DISABLED rather than looking
// live and doing nothing.
function mountNavButton(row, { label, title, run }) {
  const btn = el("button", "disposebtn dispose-intile wheelnavbtn", label || "open");
  btn.type = "button";
  btn.title = run ? title : title + " — unavailable here";
  btn.disabled = !run;
  if (run) btn.addEventListener("click", (ev) => { ev.stopPropagation(); run(); });
  row.appendChild(btn);
  return btn;
}

// A FLYOUT verb (archived `landed` · active `packet`): one click opens this
// tile's anchored panel. `opts.showFlyout(actionId, item)` is the view's own
// opener — it owns the anchor, the panel's lifetime, and the body — so this
// mounter is just the button and its in-flight state.
function mountFlyoutButton(row, item, opts) {
  const verb = FLYOUT_VERBS[opts.actionId] || {};
  const btn = el("button", "disposebtn dispose-intile wheelnavbtn",
    opts.label || opts.actionId || "open");
  btn.type = "button";
  btn.title = verb.title || "";
  btn.addEventListener("click", async (ev) => {
    ev.stopPropagation();
    if (!opts.showFlyout) return;
    const label = btn.textContent;
    btn.disabled = true;
    if (verb.pending) btn.textContent = verb.pending;
    try {
      await opts.showFlyout(opts.actionId, item);
    } finally {
      btn.disabled = false;
      btn.textContent = label;
    }
  });
  row.appendChild(btn);
  return btn;
}

// The SET-level "Open in NotebookLM" verb. It REUSES the shared controller
// (`opts.notebook`, built once in app.js from the single /capabilities probe):
// the controller owns the click cycle — disable + "opening NotebookLM…" pending
// text, the POST, opening the returned url, and the structured refusal rendered
// inline through textContent — exactly as on the funnel/board/canvas cards. This
// mounter adds only the wheel->tile-kind mapping and the compact in-tile chrome,
// so there is one implementation of the action, not two.
function mountNotebookButton(row, item, opts) {
  const kind = NOTEBOOK_TILE_KINDS[opts.wheelKey];
  // `button()` returns null when the capability is not live, so a wheel whose
  // table row slipped through without the capability still mounts nothing live.
  const wrap = kind && opts.notebook ? opts.notebook.button(kind, item.id) : null;
  if (!wrap) {
    // declared by the pure table but unmountable in this embedding (no shared
    // controller threaded in): show it DISABLED rather than dropping a declared
    // verb, the same posture as a nav verb with no callbacks.
    const stub = el("button", "disposebtn dispose-intile nbbtn", opts.label || "notebook");
    stub.type = "button";
    stub.disabled = true;
    stub.title = "open in NotebookLM — unavailable here";
    row.appendChild(stub);
    return stub;
  }
  const btn = wrap.querySelector("button");
  if (btn) {
    // compact row chrome (the propose button's .dispose-intile pill), and the
    // table's short label in place of the card affordance's long one — the tile
    // is 196px wide and already carries other verbs. runClick re-reads
    // textContent at click time, so the pending/restore cycle is unaffected.
    btn.classList.add("disposebtn", "dispose-intile");
    btn.textContent = opts.label || btn.textContent;
    btn.title = "open this " + kind + " tile's document set in NotebookLM";
  }
  row.appendChild(wrap);
  return wrap;
}

// Read the named spec deltas through the read-only pass-through. An unreadable
// file counts as FAILED (readSource never throws) and the flyout says so inline.
async function fetchDeltaTexts(paths) {
  const files = [];
  let failed = 0;
  for (const path of paths) {
    const text = await readSource(path);
    if (text === null) failed += 1;
    else files.push({ path, text });
  }
  return { files, failed };
}

function clamp(v, lo, hi) {
  return Math.min(hi, Math.max(lo, v));
}

// The tile's stacking order: focused on top, on-line tiles next, then
// falling off with distance (never below 1).
function tileZ(focused, ad) {
  if (focused) return "6";
  if (ad < 0.5) return "5";
  return String(Math.max(1, 4 - Math.round(ad)));
}

// Drop rendered tiles that left the reel window, keeping banded (linked)
// tiles wherever they are.
function pruneTiles(tiles, lo, hi, linked) {
  for (const [i, tile] of tiles) {
    if ((i < lo || i > hi) && !linked.has(i)) { tile.remove(); tiles.delete(i); }
  }
}

// One thread's bezier: horizontal-tangent cubic between the two anchors.
function threadPath(x0, y0, x1, y1) {
  const mx = (x0 + x1) / 2;
  return "M " + x0 + " " + y0 + " C " + mx + " " + y0 + ", " +
    mx + " " + y1 + ", " + x1 + " " + y1;
}

export function renderWheel(root, snapshot, ctx) {
  const caps = ctx?.caps || null;
  // Cross-view navigation callbacks from the app shell (app.js): openDoc(path,
  // doc) opens the read-only viewer; openLens(keywords, clusterId) and
  // openCanvas(clusterId) switch tab AND hand the target view its preselection.
  // Absent in a bare embedding — the read verbs then render disabled.
  const nav = ctx?.nav || null;
  // The SHARED "Open in NotebookLM" controller (notebook.js), built once by the
  // app shell from the one /capabilities probe and handed to every view that
  // mounts the action. Absent in a bare embedding, like `nav`.
  const notebook = ctx?.notebook || null;
  // add-project-merged-projection (D10): the app shell says whether this
  // render is a COMPOSED view — the tiles then offer the open-in-repo jump.
  const composed = !!ctx?.composed;
  // The active (repository, ref) source base for this render (see `sourceBase`).
  if (ctx?.sourceBase) sourceBase = ctx.sourceBase;
  const model = buildWheelModel(snapshot);
  const reduceMotion = typeof matchMedia === "function" &&
    matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- state ----
  const pos = {}, vel = {}, target = {}, acc = {};
  for (const w of model.wheels) {
    pos[w.key] = 0; vel[w.key] = 0; target[w.key] = 0; acc[w.key] = 0;
  }
  // Reorder permutation per wheel (Brett 2026-07-24): when a focus links
  // MANY tiles in one wheel, the old parking curve stacked them on top of
  // each other. Instead the pulled wheel REARRANGES: linked items take
  // consecutive display slots at the centre; everything else fills the
  // leftover slots in original order. slotBy: item index -> display slot;
  // itemAt: the inverse. Identity when absent. `chor` holds the spin-out /
  // re-seat / spin-in choreography (the swap happens while the window is
  // faded, so tiles never visibly teleport).
  const slotBy = {}, itemAt = {}, chor = {};
  const REORDER = { outMs: 240, spring: { k: 0.045, damping: 0.82 } };
  function slotOf(key, i) {
    const m = slotBy[key];
    return m && m.has(i) ? m.get(i) : i;
  }
  function itemAtSlot(key, s) {
    const m = itemAt[key];
    if (!m) return s;
    return m.has(s) ? m.get(s) : -1; // unmapped slot on a permuted wheel: blank
  }
  // (`computeReorder`, the permutation itself, is pure -> wheel-model.js.)

  const hidden = new Set(); // column hiding: ONE state behind both affordances
  let focus = null;         // { key, i }
  let expanded = null;      // { key, i } — the ONE expanded tile, or null
  let flyout = null;        // { host, tile } — the expanded tile's anchored flyout
  let liveIndex = null;     // the driven wheel's last live-pull index
  let railKey = "";         // last rendered badge-rail focus, "key:i"
  let page = 0;
  let raf = null;
  let winH = WIN_H;         // live window height (grows in full screen)
  let winTop = 34;          // wheel-window top within the port (below headers)
  let scaleF = 1;           // live --wheel-scale (1.33 in full screen)
  // The drum-radius knob, MUTABLE: it is the "wheel diameter" setting (header
  // gear), so the slider retargets the cylinder mid-session. settings.js owns
  // the load-time precedence (?drum= URL wins, else the saved setting, else 1)
  // and announces changes; see onSettingsChange below.
  let drumF = currentDrumFactor();

  // ---- scaffold ----
  root.innerHTML = "";
  const bar = el("div", "wheelbar");
  const prev = el("button", "wheelnav", "←");
  prev.type = "button"; prev.title = "previous column (←)";
  const next = el("button", "wheelnav", "→");
  next.type = "button"; next.title = "next column (→)";
  const hint = el("span", "wheelhint",
    "hover a wheel and scroll to spin · click a tile to focus, click it again " +
    "for its actions · ←/→ page columns");
  const full = el("button", "wheelnav wheelfull", "\u26f6");
  full.type = "button"; full.title = "full screen";
  full.setAttribute("aria-label", "toggle full screen");
  full.addEventListener("click", () => {
    if (document.fullscreenElement === root) document.exitFullscreen();
    else root.requestFullscreen();
  });
  function refreshWinH() {
    const visibleKey = WHEEL_KEYS.find((k) => !hidden.has(k));
    const win = visibleKey ? cols[visibleKey].win : null;
    winH = (win && win.clientHeight) || WIN_H;
    scaleF = Number.parseFloat(
      getComputedStyle(port).getPropertyValue("--wheel-scale")) || 1;
    // Pin the centre band to the WHEEL AXIS — the vertical centre of the
    // wheel windows — not the outer port's 50%: the windows sit below the
    // column headers, so the two centres drift apart as the viewport grows.
    // Rect math, not offsetTop: the win's offsetParent is the column, not
    // the port.
    if (win) {
      winTop = win.getBoundingClientRect().top -
        port.getBoundingClientRect().top;
    }
    const axisY = winTop + winH / 2;
    band.style.top = (axisY - 46 * scaleF).toFixed(0) + "px";
    pageTo(page); // re-derive the carousel transform for the new geometry
    drawAll();
  }
  function onFullscreenChange() {
    if (!root.isConnected) {
      document.removeEventListener("fullscreenchange", onFullscreenChange);
      return;
    }
    const active = document.fullscreenElement === root;
    full.textContent = active ? "\u2921" : "\u26f6";
    full.title = active ? "exit full screen" : "full screen";
    // the window height changes with the CSS :fullscreen override; re-measure
    // after layout settles
    requestAnimationFrame(refreshWinH);
  }
  document.addEventListener("fullscreenchange", onFullscreenChange);
  // LIVE settings: the wheel-diameter slider changes the drum radius while the
  // view is open — re-measure (the axis/threads are built for the cylinder) and
  // redraw on the next frame, no reload. Same self-removing teardown as
  // onFullscreenChange: the view can remount into a fresh root, and a stale
  // listener would keep redrawing a detached DOM.
  function onSettingsChange(ev) {
    if (!root.isConnected) {
      document.removeEventListener(SETTINGS_EVENT, onSettingsChange);
      return;
    }
    const factor = ev?.detail?.drum;
    if (!Number.isFinite(factor) || factor === drumF) return;
    drumF = factor;
    requestAnimationFrame(refreshWinH);
  }
  document.addEventListener(SETTINGS_EVENT, onSettingsChange);
  bar.append(prev, hint, next, full);
  if (model.demoMode) {
    bar.appendChild(el("span", "wheeldemo-note",
      "possibles are synthesized demo placeholders (register empty) — dashed brass, never indexed data"));
  }
  root.appendChild(bar);

  const port = el("div", "wheelport");
  port.tabIndex = 0; // ←/→ and ↑/↓ keys land here
  const deck = el("div", "wheeldeck");
  const band = el("div", "wheelcenterband");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "wheelthreads");
  port.append(band, deck, svg);
  root.appendChild(port);

  const dock = el("div", "wheeldock");
  root.appendChild(dock);

  // ---- per-wheel DOM ----
  const cols = {}; // key -> { col, win, rail, tiles: Map(index -> tileEl) }
  for (const w of model.wheels) {
    const col = el("section", "wheelcol");
    col.dataset.wheel = w.key;
    const header = el("header", "wheelhead");
    const eye = el("button", "wheeleye", "👁");
    eye.type = "button";
    eye.title = "hide the " + w.label + " column";
    eye.setAttribute("aria-label", "hide the " + w.label + " column");
    eye.addEventListener("click", () => setHidden(w.key, true));
    header.append(el("span", "wheelname", w.label),
                  el("span", "wheelcount", String(w.items.length)), eye);
    const win = el("div", "wheelwin");
    win.dataset.wheel = w.key;
    // the badge rail: the focused centre tile's connection chips live BELOW
    // the tile (the locked prototype's rail), never inside it.
    const badgeRail = el("div", "wheelbadges");
    badgeRail.hidden = true;
    win.appendChild(badgeRail);
    // the vertical rail label shown only while collapsed
    const showRail = el("button", "wheelrail", w.label);
    showRail.type = "button";
    showRail.title = "show the " + w.label + " column";
    showRail.addEventListener("click", () => setHidden(w.key, false));
    col.append(header, win, showRail);
    deck.appendChild(col);
    cols[w.key] = { col, win, badgeRail, tiles: new Map() };

    // the locked prototype's scroll accumulator: 40 wheel-pixels = one
    // whole-tile step, so a trackpad glide spins several tiles smoothly.
    win.addEventListener("wheel", (ev) => {
      ev.preventDefault();
      acc[w.key] += ev.deltaY;
      const steps = Math.trunc(acc[w.key] / WHEEL_PIXELS_PER_STEP);
      if (steps) {
        acc[w.key] -= steps * WHEEL_PIXELS_PER_STEP;
        spin(w.key, steps);
      }
    }, { passive: false });
  }

  // ---- column hiding (both affordances, one state) ----
  function setHidden(key, isHidden) {
    // Hiding a column whose tile is EXPANDED must collapse it first: a hidden
    // column stops being drawn, so the open tile would keep its action row (live
    // buttons and all) behind the rail until it was shown again.
    if (isHidden && expanded?.key === key) collapseExpanded();
    if (isHidden) hidden.add(key); else hidden.delete(key);
    cols[key].col.classList.toggle("wheelhidden", isHidden);
    renderDock();
    drawAll();
  }
  function renderDock() {
    dock.innerHTML = "";
    for (const key of WHEEL_KEYS) {
      if (!hidden.has(key)) continue;
      const chip = el("button", "wheeldockchip", WHEEL_LABELS[key]);
      chip.type = "button";
      chip.title = "show the " + WHEEL_LABELS[key] + " column";
      chip.addEventListener("click", () => setHidden(key, false));
      dock.appendChild(chip);
    }
    dock.hidden = dock.childElementCount === 0;
  }
  renderDock();

  // ---- carousel (discrete, no pixel scrolling) ----
  function pageTo(p) {
    const visible = WHEEL_KEYS.filter((k) => !hidden.has(k));
    page = clamp(p, 0, Math.max(0, visible.length - 1));
    const first = cols[visible[Math.min(page, visible.length - 1)]];
    if (deck.scrollWidth <= port.clientWidth) {
      // everything fits (e.g. full screen): stay centred, no carousel shift
      deck.style.transform = "";
    } else if (first) {
      deck.style.transform =
        "translateX(" + (-first.col.offsetLeft) + "px)";
    }
    drawThreads();
  }
  function pageToColumn(key) {
    collapseExpanded(); // the carousel moves out from under an expanded tile
    if (hidden.has(key)) setHidden(key, false);
    const visible = WHEEL_KEYS.filter((k) => !hidden.has(k));
    pageTo(Math.max(0, visible.indexOf(key) - 1));
    cols[key].col.classList.remove("wheelpulse");
    // force a reflow so removing/re-adding the class restarts the animation
    cols[key].col.getBoundingClientRect();
    cols[key].col.classList.add("wheelpulse");
  }
  // Paging is a USER carousel move (pageTo itself is also called by the
  // geometry re-measure, which must NOT collapse a tile the human just opened).
  function pageBy(delta) { collapseExpanded(); pageTo(page + delta); }
  prev.addEventListener("click", () => pageBy(-1));
  next.addEventListener("click", () => pageBy(1));
  port.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowLeft") { ev.preventDefault(); pageBy(-1); }
    else if (ev.key === "ArrowRight") { ev.preventDefault(); pageBy(1); }
    else if (ev.key === "ArrowUp" && focus) { ev.preventDefault(); spin(focus.key, -1); }
    else if (ev.key === "ArrowDown" && focus) { ev.preventDefault(); spin(focus.key, 1); }
  });

  // ---- the expanded tile (the 2026-07-25 extension of the locked gesture) ----
  // State lives here; the TRANSITIONS are the pure reducer in wheel-model.js, so
  // the trigger matrix (second click, Escape, focus change, spin, reorder,
  // paging, teardown) is unit-tested outside the DOM.
  function sameCell(a, b) {
    return (!a && !b) || (!!a && !!b && a.key === b.key && a.i === b.i);
  }
  function expandEvent(ev) {
    const nextState = nextExpanded(expanded, ev);
    if (sameCell(nextState, expanded)) return false;
    expanded = nextState;
    closeFlyout(); // the flyout belongs to ONE expanded tile; the tile just moved
    drawAll();
    return true;
  }
  function collapseExpanded() {
    return expanded ? expandEvent({ type: "collapse" }) : false;
  }
  // Escape collapses from anywhere the keypress can reach (the tile itself, the
  // action row's buttons, the port). Same self-removing teardown as the
  // fullscreen/settings listeners: the view can remount into a fresh root.
  function onKeydown(ev) {
    if (!root.isConnected) {
      document.removeEventListener("keydown", onKeydown);
      closeFlyout(); // the flyout lives on <body>: never outlive its view
      return;
    }
    if (ev.key !== "Escape") return;
    // Escape closes the open flyout too — it is the expanded tile's panel, and
    // it is appended to <body>, so nothing else would take it down.
    const hadFlyout = !!flyout;
    if (collapseExpanded() || hadFlyout) {
      closeFlyout();
      ev.stopPropagation();
    }
  }
  document.addEventListener("keydown", onKeydown);

  // ---- the anchored flyout (shared by the `landed` and `packet` verbs) --------
  // Neither a requirement list nor a packet file list can live INSIDE the
  // expanded tile: the box is 196x132 CSS px on a drum whose window clips
  // vertically (.wheelwin clip-path), so growing it further would either shear
  // the panel or swallow the reel. Both therefore open as a FIXED flyout anchored
  // to the tile — the settings-panel pattern in this bundle, adopted for the
  // same reason (the app shell clips overflow). It belongs to the ONE expanded
  // tile: every collapse trigger closes it (expandEvent above), and only ONE
  // flyout is ever open, so the two verbs share this whole scaffold and differ
  // only in the body they render.
  function closeFlyout() {
    if (!flyout) return;
    flyout.host.remove();
    flyout = null;
  }
  // Anchor to the right of the tile, flipping left when the viewport would clip
  // it, and clamped into the window vertically.
  function placeFlyout() {
    if (!flyout) return;
    if (!root.isConnected || !flyout.tile.isConnected) { closeFlyout(); return; }
    const r = flyout.tile.getBoundingClientRect();
    const w = flyout.host.offsetWidth;
    const h = flyout.host.offsetHeight;
    const right = r.right + 10;
    const left = right + w <= window.innerWidth ? right : Math.max(8, r.left - 10 - w);
    flyout.host.style.left = left.toFixed(0) + "px";
    flyout.host.style.top =
      clamp(r.top + r.height / 2 - h / 2, 8, Math.max(8, window.innerHeight - h - 8))
        .toFixed(0) + "px";
  }
  function flyoutHead(item, closeLabel) {
    const head = el("div", "wheelfly-head");
    head.appendChild(el("span", "wheelfly-title", item.id));
    const close = el("button", "wheelfly-close", "✕");
    close.type = "button";
    close.title = "close";
    close.setAttribute("aria-label", closeLabel);
    close.addEventListener("click", (ev) => { ev.stopPropagation(); closeFlyout(); });
    head.appendChild(close);
    return head;
  }
  // Open THE flyout for `item`, anchored on `tile`. `pending` (when given) is the
  // note shown while `prepare()` reads; `render(body, data)` then fills the body
  // with `prepare`'s result. A verb with no read (`packet`) renders immediately.
  async function openFlyout(item, tile, { ariaLabel, closeLabel, pending, prepare, render }) {
    closeFlyout();
    if (!tile) return;
    const host = el("aside", "wheelfly");
    host.setAttribute("role", "dialog");
    host.setAttribute("aria-label", ariaLabel);
    host.appendChild(flyoutHead(item, closeLabel));
    const body = el("div", "wheelfly-body");
    if (prepare && pending) body.appendChild(el("div", "wheelfly-note", pending));
    host.appendChild(body);
    // clicks inside the flyout are the flyout's (it is a sibling of the deck,
    // but the tile's own handlers must not see them)
    host.addEventListener("click", (ev) => ev.stopPropagation());
    document.body.appendChild(host);
    flyout = { host, tile };
    placeFlyout();
    const data = prepare ? await prepare() : null;
    // the human may have collapsed the tile (or spun the wheel) mid-read
    if (!flyout || flyout.host !== host || !host.isConnected) return;
    body.textContent = "";
    render(body, data);
    placeFlyout();
  }
  // Verb -> opener. The mounted button knows only its action id, so the wiring
  // stays one entry here (the DOM half of the pure table's row).
  function showFlyout(actionId, item, tile) {
    if (actionId === "landed") return showLanded(item, tile);
    if (actionId === "packet") return showPacket(item, tile);
    return Promise.resolve();
  }
  // The summary body: the realization facts the snapshot already carries, then
  // the requirement titles the pure parser found, grouped by delta kind.
  // textContent ONLY (el()) — this renders FETCHED governance prose.
  function renderLandedBody(body, item, result, summary) {
    const change = item.ref || {};
    if (change.code_surface) {
      body.appendChild(el("div", "wheelfly-line", "code surface: " + change.code_surface));
    }
    if (change.target_release) {
      body.appendChild(el("div", "wheelfly-line", "target release: " + change.target_release));
    }
    for (const kind of LANDED_KINDS) {
      const reqs = summary.groups[kind];
      if (!reqs.length) continue;
      body.appendChild(el("div", "wheelfly-kind", kind + " (" + reqs.length + ")"));
      for (const req of reqs) {
        const line = el("div", "wheelfly-req", req.title);
        if (req.capability) {
          line.appendChild(document.createTextNode(" "));  // keep the text readable
          line.appendChild(el("span", "wheelfly-cap", req.capability));
        }
        body.appendChild(line);
      }
    }
    if (!summary.total) {
      // "nothing landed" and "nothing could be read" are DIFFERENT statements —
      // an unreadable delta says so in the error line below, never as an absence.
      const requested = result.files.length + result.failed;
      if (!requested) {
        body.appendChild(el("div", "wheelfly-note",
          "this archived change records no spec deltas"));
      } else if (summary.files.length) {
        body.appendChild(el("div", "wheelfly-note",
          "no requirement headings in this change's spec deltas"));
      }
    }
    // Quiet inline failure — never a thrown error, never a silent empty panel.
    if (result.failed) {
      body.appendChild(el("div", "wheelfly-err",
        result.files.length
          ? result.failed + " of " + (result.failed + result.files.length) +
            " spec deltas could not be read from /source"
          : "could not read the spec deltas — the read-only /source pass-through " +
            "is unavailable here (run generate-and-open for the local viewer)"));
    }
  }
  function showLanded(item, tile) {
    return openFlyout(item, tile, {
      ariaLabel: "what landed from " + item.id,
      closeLabel: "close the landed summary",
      pending: "reading the spec deltas…",
      prepare: () => fetchDeltaTexts(specDeltaPaths(item.ref?.files)),
      render: (body, result) =>
        renderLandedBody(body, item, result, landedFromDeltas(result.files)),
    });
  }

  // ---- the "packet" flyout (active wheel's review verb) ----------------------
  // The proposal packet is the change's OWN files, grouped the way a reviewer
  // reads them (pure `packetGroups`): proposal/design/tasks, then the spec
  // deltas by capability, then the rest. Each entry is a BUTTON that hands the
  // path to nav.openDoc — the same read-only viewer the `read` verb uses — and
  // closes the flyout, because the viewer overlay would cover it anyway. No
  // fetch of its own: the file list is snapshot data, and an unavailable /source
  // degrades inside the viewer with the viewer's own message.
  function renderPacketBody(body, item) {
    const change = item.ref || {};
    const progress = change.task_progress;
    if (progress && Number.isFinite(progress.total)) {
      body.appendChild(el("div", "wheelfly-line",
        "tasks: " + (progress.completed ?? 0) + " / " + progress.total));
    }
    const groups = packetGroups(change.files, change.folder);
    for (const group of groups) {
      body.appendChild(el("div", "wheelfly-kind",
        group.label + " (" + group.files.length + ")"));
      for (const entry of group.files) {
        const btn = el("button", "wheelfly-file", entry.name);
        btn.type = "button";
        btn.title = nav?.openDoc
          ? "open " + entry.path + " in the read-only source viewer"
          : entry.path + " — the source viewer is unavailable here";
        btn.disabled = !nav?.openDoc;
        btn.addEventListener("click", (ev) => {
          ev.stopPropagation();
          closeFlyout();                  // the viewer overlay covers the flyout
          nav.openDoc(entry.path, null, item.ref);
        });
        body.appendChild(btn);
      }
    }
    if (!groups.length) {
      body.appendChild(el("div", "wheelfly-note",
        "this change records no packet files"));
    }
  }
  function showPacket(item, tile) {
    return openFlyout(item, tile, {
      ariaLabel: "the proposal packet of " + item.id,
      closeLabel: "close the packet list",
      render: (body) => renderPacketBody(body, item),
    });
  }

  // ---- focus, spin, and the elastic pull ----
  function wheelByKey(key) {
    return model.wheels.find((w) => w.key === key);
  }
  function spin(key, steps) {
    expandEvent({ type: "spin", key }); // spinning a wheel closes its open tile
    const n = wheelByKey(key).items.length;
    if (!n) return;
    const s = clamp(Math.round(target[key]) + steps, 0, n - 1);
    const item = itemAtSlot(key, s);
    if (item >= 0) setFocus(key, item);
  }
  function setFocus(key, i) {
    expandEvent({ type: "collapse" }); // focusing ANY tile closes the open one
    focus = { key, i };
    target[key] = slotOf(key, i);
    liveIndex = null; // force a live re-pull on the next frame
    scheduleReorders();
    kick();
  }
  // Start the reorder choreography on every pulled wheel whose gathered tiles
  // are not already seated together: fade + whirl out, re-seat while hidden,
  // roll back in. Single gathers never stack, so they keep the plain pull.
  // GATHERING (Brett 2026-07-25) seats the wheel's FIRST- and SECOND-degree
  // tiles together — `gatherOf(...).gather` is the union the block packs, so a
  // wheel reached only at second degree (docs off a focused staged topic's
  // clusters) now spins its neighbourhood into the window instead of sitting
  // still. First-degree priority is applied in `retarget` (it aligns on them).
  function scheduleReorders() {
    if (!focus) return;
    const gather = gatherOf(model, focus.key, focus.i);
    for (const w of model.wheels) {
      if (w.key === focus.key) continue;
      const linked = gather[w.key]?.gather || [];
      if (linked.length < 2) continue;
      const next = computeReorder(w.items.length, linked, pos[w.key]);
      const seated = linked.every((i) => {
        const s = slotOf(w.key, i);
        return s >= next.blockLo && s < next.blockLo + next.k;
      });
      if (seated) continue;
      // the choreography rebuilds this wheel's tiles: nothing stays expanded
      // through it (setFocus, its only caller, has already collapsed — this
      // keeps the rule true if the choreography ever starts from elsewhere).
      collapseExpanded();
      chor[w.key] = { state: "out", t0: performance.now(), next };
      cols[w.key].win.classList.add("wheelreorder");
    }
  }
  // The mid-choreography swap: install the permutation and rebuild this
  // wheel's tiles while its window is faded out, then roll back in.
  function applyReorder(key) {
    const c = chor[key];
    slotBy[key] = c.next.sBy; itemAt[key] = c.next.iAt;
    const { tiles } = cols[key];
    for (const tile of tiles.values()) tile.remove();
    tiles.clear();
    const n = wheelByKey(key).items.length;
    const mid = clamp(c.next.blockLo + (c.next.k - 1) / 2, 0, Math.max(0, n - 1));
    pos[key] = mid + 6; vel[key] = 0; target[key] = mid;
    c.state = "in";
    cols[key].win.classList.remove("wheelreorder");
  }
  // The LIVE pull: as the driven wheel crosses each tile mid-spin, connected
  // wheels retarget continuously rather than jumping once at settle.
  function retarget(fromIndex) {
    if (!focus) return;
    const gather = gatherOf(model, focus.key, fromIndex);
    for (const w of model.wheels) {
      if (w.key === focus.key) continue;
      if (chor[w.key]) continue; // the choreography owns this wheel's target
      // align on the FIRST-degree tiles when the wheel has any (they rest on
      // the line; second-degree gather around them inside the seated block),
      // else on the second-degree set so a purely-second-degree wheel still
      // comes into view rather than staying put.
      const align = gather[w.key]?.align || [];
      const t = alignTarget(align.map((i) => slotOf(w.key, i)));
      if (t !== null) target[w.key] = clamp(t, 0, Math.max(0, w.items.length - 1));
    }
  }

  // ---- physics ----
  // Advance one wheel one frame toward its target; returns true while moving.
  function advanceWheel(key, spring) {
    if (reduceMotion) {
      vel[key] = 0;
      if (pos[key] === target[key]) return false;
      pos[key] = target[key];
      return true;
    }
    vel[key] += (target[key] - pos[key]) * spring.k;
    vel[key] *= spring.damping;
    const settled = Math.abs(vel[key]) <= 0.0004 &&
      Math.abs(target[key] - pos[key]) <= 0.002;
    if (settled) {
      pos[key] = target[key];
      vel[key] = 0;
      return false;
    }
    pos[key] += vel[key];
    return true;
  }
  function step() {
    raf = null;
    let moving = false;
    if (focus) {
      // pos is in SLOT space; the live pull needs the ITEM crossing the
      // line — on a permuted wheel the two differ, and feeding the slot to
      // connectionsOf retargets every pulled wheel off the wrong item.
      const liveSlot = clamp(Math.round(pos[focus.key]), 0,
        Math.max(0, wheelByKey(focus.key).items.length - 1));
      const liveItem = itemAtSlot(focus.key, liveSlot);
      if (liveItem >= 0 && liveItem !== liveIndex) {
        liveIndex = liveItem;
        retarget(liveItem);
      }
    }
    for (const w of model.wheels) {
      const c = chor[w.key];
      if (c && c.state === "out") {
        if (reduceMotion || performance.now() - c.t0 >= REORDER.outMs) {
          applyReorder(w.key);
        } else {
          // whirl away while the window fades — the swap happens hidden
          vel[w.key] = Math.max(vel[w.key], 1.4);
          pos[w.key] += vel[w.key];
          moving = true;
          continue;
        }
      }
      const spring = c ? REORDER.spring
        : (focus?.key === w.key ? SPRING.driven : SPRING.pulled);
      if (advanceWheel(w.key, spring)) moving = true;
      else if (c) delete chor[w.key];
    }
    drawAll();
    if (moving) kick();
  }
  function kick() {
    if (raf === null) raf = requestAnimationFrame(step);
  }

  // ---- tiles ----
  function tileFor(w, i) {
    const it = w.items[i];
    if (!it) { // filler slot past the item range: the drum stays full
      const blank = el("div", "wheeltile wheelblank");
      blank.dataset.wheel = w.key;
      blank.dataset.index = String(i);
      return blank;
    }
    // A DIV with role=button, NOT a <button>: an expanded tile hosts a row of
    // real action buttons INSIDE itself, and a button nested in a button is
    // invalid HTML whose inner activation browsers do not deliver. role +
    // tabIndex + Enter/Space keeps the tile's click, focus-ring, and keyboard
    // semantics identical to the <button> it replaces.
    const tile = el("div", "wheeltile");
    tile.setAttribute("role", "button");
    tile.tabIndex = 0;
    tile.setAttribute("aria-expanded", "false");
    tile.dataset.wheel = w.key;
    tile.dataset.index = String(i);
    if (it.demo) tile.classList.add("wheel-demo");
    if (it.derivedPending) tile.classList.add("wheel-derived");
    tile.appendChild(el("span", "wheellabel", it.label));
    const sub = el("span", "wheelsub", it.sub || "");
    const degree = w.degrees[i] || 0;
    sub.appendChild(el("span", "wheeldegree", degree ? String(degree) : "·"));
    tile.appendChild(sub);
    tile.addEventListener("click", (ev) => {
      // a click on an action inside the expanded tile is that action's, not the
      // tile's (the mounted buttons also stopPropagation; this is the backstop)
      if (ev.target !== tile && ev.target.closest?.(".wheelactions")) return;
      activateTile(w.key, i, tile);
    });
    tile.addEventListener("keydown", (ev) => {
      if (ev.target !== tile) return;          // keys inside the action row
      if (ev.key !== "Enter" && ev.key !== " ") return;
      ev.preventDefault();                     // Space must not scroll the port
      activateTile(w.key, i, tile);
    });
    return tile;
  }
  // The tile gesture: an UNFOCUSED tile FOCUSES (clicking a linked tile in
  // another wheel is the same gesture — focus TRANSFERS and the pull radiates
  // from it instead; locked spec). The tile that is already focused AND seated
  // on the line EXPANDS in place, and the expanded tile collapses. `centred` is
  // read off the class layoutTile stamps, so the gesture and the rendering
  // agree on "on the line" by construction.
  function activateTile(key, i, tile) {
    const centred = tile.classList.contains("wheelfocused");
    expandEvent({ type: "tile", key, i, centred });
    if (!centred) setFocus(key, i);
  }

  // CYLINDER projection (live-tuning experiment, Brett 2026-07-24): each
  // wheel is a spinning drum seen edge-on whose RADIUS equals the viewport
  // height. A tile d steps from centre sits at arc angle
  // θ = d·spacing/R, lands at y = R·sin θ, and foreshortens vertically by
  // cos θ — tiles visibly wrap over the drum's horizon instead of sliding a
  // flat list. (Supersedes the flat reel + tanh bulge while we tune.)
  // Radius knob (the "wheel diameter" setting; `drumF` above): 1 -> R =
  // viewport height (gentle, ~±30° visible); 0.5 -> R = half height (full
  // horizon at the viewport edges — the classic slot-drum wrap). Default 1 per
  // Brett's opening spec. Both tuning paths stay open: `?drum=` still wins at
  // load for compare-by-URL, and the header gear's slider tunes it live.

  // The arithmetic moved to wheel-model.js's `drumProject` (2026-08-03) when
  // the docs pane's wheel became a second caller: "the same wheel" has to mean
  // the same projection, and two copies drift the first time either is tuned.
  // This closure stays as the binding of the live tuning state (`winH` grows in
  // full screen, `scaleF` tracks --wheel-scale, `drumF` is the settings knob).
  function drum(d, bulged) {
    return drumProject({ d, bulged, winH, drumF, scaleF });
  }

  // Apply one tile's frame on the drum: cylinder placement + vertical
  // foreshortening, the focused wheel keeping its continuous magnification
  // curve toward 1.35 at centre. Linked tiles keep a readable opacity floor.
  // `isSecondDeg` (Brett 2026-07-25: always-on second-degree, dimmed) buys the
  // tile ONLY a faint edging class — it never touches placement, opacity,
  // scale, or z-index, so a second-degree tile reads exactly like an ordinary
  // resting tile except for that hairline hint.
  function layoutTile(tile, d, isFocusWheel, isLinked, focused, appliedVerdict,
    isExpanded, isSecondDeg) {
    const c = drum(d, isFocusWheel);
    const y = winH / 2 + c.y;
    const s = tileScale(d, isFocusWheel);
    // WHAT IS ACTUALLY IN THE WINDOW (T092 acceptance sweep, defect 6). The
    // drum places roughly 31 tiles per column and the window holds 7; the rest
    // land over the page header, the stat tiles and the tab strip. The clip
    // stops them painting and stops the mouse, and stopped nothing else — they
    // all kept `tabindex=0`, so a keyboard user tabbed through 25 invisible
    // tiles. `inReelWindow` is now the ONE predicate behind focusability,
    // `aria-hidden` and pointer-events, so keyboard and mouse agree with what
    // is visible. An EXPANDED tile is on the axis by construction.
    const box = tileBox({ y, squash: c.squash, tileH: TILE_H * scaleF, scale: s,
      expanded: !!isExpanded });
    // A blank filler slot is not a control and never entered the tab order —
    // only a real item tile carries `role="button"`, so only it is re-keyed.
    const onWindow = isExpanded || inReelWindow(box, winH, c.over);
    if (tile.getAttribute("role") === "button") tile.tabIndex = onWindow ? 0 : -1;
    if (onWindow) tile.removeAttribute("aria-hidden");
    else tile.setAttribute("aria-hidden", "true");
    tile.classList.toggle("wheeloffwindow", !onWindow);
    if (isExpanded) {
      // The expanded tile is placed by its CENTRE — translateY(-50%) is
      // self-relative, so the CSS height growth animates symmetrically about
      // the drum axis instead of dragging the box down as it grows. It keeps the
      // axis, drops the foreshortening squash (it IS the centre tile), and
      // paints above every tile, chip, and thread.
      tile.style.transform = "translate(0, " + y.toFixed(1) + "px) translateY(-50%) " +
        "scale(" + EXPANDED.scale.toFixed(3) + ")";
      tile.style.opacity = "1";
      tile.style.zIndex = "9";
    } else {
      tile.style.transform = "translate(0, " + (y - 28 * scaleF * c.squash).toFixed(1) + "px) " +
        "scale(" + s.toFixed(3) + ", " + (s * c.squash).toFixed(3) + ")";
      const cosFade = clamp(c.squash, 0.15, 1);
      const opacity = c.over ? 0 : (isLinked ? Math.max(cosFade, 0.9) : cosFade);
      tile.style.opacity = opacity.toFixed(2);
      tile.style.zIndex = tileZ(focused, Math.abs(d));
    }
    tile.classList.toggle("wheelexpanded", !!isExpanded);
    tile.classList.toggle("wheelfocused", !!focused);
    tile.classList.toggle("wheellinked", isLinked);
    tile.classList.toggle("wheel-seconddeg", !!isSecondDeg);
    // session-local applied overlay (two-plane rendering): a disposition
    // this session decorates the tile until the snapshot is regenerated —
    // the snapshot-derived model itself is never mutated.
    tile.classList.toggle("wheelapplied", !!appliedVerdict);
    tile.dataset.applied = appliedVerdict || "";
    return box;   // the caller needs the RENDERED band (defect 14b's rail check)
  }
  // The expanded tile's CONTENTS: an action row below the label/sub, built from
  // the pure per-wheel table (wheel-model.js WHEEL_ACTIONS) through
  // ACTION_MOUNTERS. Mounted on expansion and torn down on collapse, so a
  // collapsed tile never carries a stale button — but an ALREADY-mounted row is
  // left alone, so a mounter's own state (the propose button disabling itself on
  // success) survives the redraw that follows it.
  // Which of this feature's verbs has acted on this tile THIS SESSION, if any.
  // Drives the decoration above; never read from the snapshot.
  const WHEEL_VERBS_BY_COLUMN = {
    possibles: ["promote-to-staging", "research-brief"],
    clusters: ["derive-possibles"],
    active: ["demote"],
  };
  function sessionActOn(wheelKey, itemId) {
    for (const verb of WHEEL_VERBS_BY_COLUMN[wheelKey] || []) {
      if (commissionedVerb(verb, itemId)) return verb;
    }
    return null;
  }

  function syncActions(tile, w, idx, isExpanded) {
    tile.setAttribute("aria-expanded", isExpanded ? "true" : "false");
    const existing = tile.querySelector(".wheelactions");
    if (!isExpanded) { if (existing) existing.remove(); return; }
    const item = w.items[idx];
    const env = {
      gate: gateCapable(caps),
      // add-project-merged-projection (D10): a composed render's tiles offer
      // the open-in-repo jump and nothing gate-bearing (the app shell also
      // strips the acting capabilities, so `gate` above is already false).
      composed: composed,
      // 011 FR-033b: a PER-VERB lookup, not a tile-wide boolean. `actionsFor`
      // resolves it per row, so each row's predicate still reads a plain
      // boolean and means "THIS verb's act is recorded for this tile this
      // session". Retirement REMOVES the row (there is no disabled control
      // left for a keyboard user to meet).
      commissioned: (verbId) => !!commissionedVerb(verbId, item.id),
      applied: appliedOutcome(item.id),
      // the notebook action's OWN capability (the same /capabilities probe, a
      // different flag): it is live only on a loopback local backend with nlm.
      notebook: notebookCapable(caps),
    };
    const specs = actionsFor(w.key, item, env);
    // RECONCILE rather than skip (011 FR-033). An already-mounted row is left
    // alone while it still offers the same verbs — that is what preserves an
    // open reason form, the focus inside it, and a control re-enabled after a
    // refusal. But once a verb RETIRES the row is stale, and leaving it alone
    // would keep a disabled control on screen where the requirement says the
    // entry must be gone.
    if (existing) {
      const mounted = String(existing.dataset.verbs || "").split(" ").filter(Boolean);
      if (!actionRowIsStale(mounted, specs.map((s) => s.id))) return;
      existing.remove();
    }
    const row = el("div", "wheelactions");
    row.dataset.verbs = specs.map((s) => s.id).join(" ");
    for (const spec of specs) {
      const mount = ACTION_MOUNTERS[spec.id];
      if (mount) {
        // the descriptor owns the LABEL (pure table); the mounter owns chrome,
        // nav, and transport. `showFlyout` carries this tile as the flyout anchor;
        // `wheelKey` is what maps a set-bearing wheel to its notebook tile kind.
        mount(row, item, {
          label: spec.label,
          actionId: spec.id,
          wheelKey: w.key,
          nav,
          notebook,
          onApplied: () => drawAll(),
          showFlyout: (verb, it) => showFlyout(verb, it, tile),
        });
      } else {
        // a table row with no mounter yet: show it disabled rather than
        // silently dropping a declared verb
        const stub = el("button", "disposebtn dispose-intile", spec.label || spec.id);
        stub.type = "button";
        stub.disabled = true;
        row.appendChild(stub);
      }
    }
    if (!row.childElementCount) {
      // no verbs for this wheel yet, or every verb retired for this item
      row.appendChild(el("span", "wheelactions-none", "no actions available"));
    }
    tile.appendChild(row);
  }

  // The expanded STAGED tile's 3-line fragment summary, mounted between the
  // title/sub and the action row (the action row's `margin-top: auto` keeps it
  // pinned to the bottom, so the summary simply takes the room the taller box
  // opens up). Same lifecycle as the action row: mounted on expansion, torn down
  // on collapse, and an already-mounted summary is left alone by later redraws.
  // The `wheel-hassummary` class is what buys the extra height (styles.css
  // re-points the ONE --wheel-expanded-h knob, so the badge rail follows).
  function syncSummary(tile, w, idx, isExpanded) {
    const existing = tile.querySelector(".wheelsummary");
    if (!isExpanded || w.key !== "staged") {
      if (existing) existing.remove();
      tile.classList.remove("wheel-hassummary");
      return;
    }
    if (existing) return;
    const item = w.items[idx];
    const path = primaryFragmentPath(item.id, item.ref?.files);
    if (!path) return;                 // no markdown fragment: no summary, no room
    const box = el("div", "wheelsummary", "");
    tile.insertBefore(box, tile.querySelector(".wheelactions"));
    tile.classList.add("wheel-hassummary");
    fillSummary(box, item.id, path);
  }
  // Fill one summary box from the session cache, reading /source on a miss.
  // textContent ONLY (el()) — this renders FETCHED governance prose. Quiet
  // degradation, the same posture as the landed flyout: an unreachable
  // pass-through says so in one faint line rather than throwing or leaving the
  // box mysteriously blank.
  function paintSummary(box, entry) {
    if (!box.isConnected) return;
    box.classList.toggle("wheelsummary-quiet", !entry.text);
    box.textContent = entry.text ||
      (entry.failed
        ? "summary unavailable — the read-only /source pass-through is not served here"
        : "this fragment carries no summary text");
  }
  async function fillSummary(box, stagingId, path) {
    const cached = summaryCache.get(stagingId);
    if (cached) { paintSummary(box, cached); return; }
    box.classList.add("wheelsummary-quiet");
    box.textContent = "reading the fragment…";
    const text = await readSource(path);
    const entry = text === null
      ? { text: "", failed: true }
      : { text: fragmentSummary(text), failed: false };
    summaryCache.set(stagingId, entry);
    paintSummary(box, entry);
    placeFlyout();                     // the box may have grown; keep the anchor
  }

  // ---- the staged tile's health chrome (add-staging-workbench D10) ----------
  // Two levels, matching the tile interaction model: the FOCUSED (centred,
  // first-click) face carries a compact tri-state indicator; the EXPANDED
  // (second-click) tile renders the full health block. Resting drum faces stay
  // unadorned. Everything shown comes VERBATIM from the snapshot's `health`
  // object through the pure helpers (healthIndicator / healthBlock, which
  // return null on a pre-growth snapshot — then NOTHING mounts and nothing is
  // computed client-side). The display never gates: propose's allow/refuse is
  // the server-side readiness gate's, evaluated live, and its refusal message
  // (rendered by the propose button's own refusal panel) is the authoritative
  // account when the snapshot has drifted — this chrome neither suppresses nor
  // restates it.
  function syncHealthIndicator(tile, item, focused, isExpanded) {
    const existing = tile.querySelector(".wheelhealth-ind");
    // the compact indicator belongs to the FOCUSED face; the expanded tile
    // carries the full block instead (its status line restates the tri-state)
    const indicator = focused && !isExpanded
      ? healthIndicator(item.ref?.health) : null;
    if (!indicator) { if (existing) existing.remove(); return; }
    if (existing) return; // already mounted for this focus; health is per-snapshot
    const badge = el("span", "wheelhealth-ind wheelhealth-" + indicator.status,
      indicator.glyph);
    badge.title = indicator.title;
    badge.setAttribute("aria-label", indicator.title);
    tile.appendChild(badge);
  }
  function syncHealthBlock(tile, item, isExpanded) {
    const existing = tile.querySelector(".wheelhealth-block");
    const block = isExpanded ? healthBlock(item.ref?.health) : null;
    if (!block) {
      if (existing) existing.remove();
      tile.classList.remove("wheel-hashealth");
      return;
    }
    if (existing) return; // mounted once per expansion, like the action row
    const box = el("div", "wheelhealth-block");
    box.appendChild(el("div", "wheelhealth-status wheelhealth-" + block.status,
      block.glyph + " " + block.status));
    for (const line of block.lines) {
      box.appendChild(el("div", "wheelhealth-line", line));
    }
    for (const blocker of block.blockers) {
      box.appendChild(el("div", "wheelhealth-blocker", blocker));
    }
    tile.insertBefore(box, tile.querySelector(".wheelactions"));
    tile.classList.add("wheel-hashealth");
  }
  function syncHealth(tile, w, idx, focused, isExpanded) {
    if (w.key !== "staged") return; // only staged topics carry a health aggregate
    const item = w.items[idx];
    syncHealthIndicator(tile, item, focused, isExpanded);
    syncHealthBlock(tile, item, isExpanded);
  }

  // The indices to render: the reel window plus every banded (linked) tile,
  // so every connection is visible on the portal (parked at the window edge
  // when the reel distance exceeds the window).
  function drawIndices(lo, hi, linked) {
    const indices = new Set();
    for (let i = lo; i <= hi; i++) indices.add(i);
    for (const i of linked) indices.add(i);
    return [...indices].sort((a, b) => a - b);
  }
  function drawWheel(w) {
    const { win, tiles } = cols[w.key];
    if (hidden.has(w.key)) return;
    const p = pos[w.key];
    const radius = Math.max(REEL.visible,
      Math.ceil((Math.PI / 2) * winH / (REEL.spacing * scaleF))) + 1;
    // UNCLAMPED: indices past the item range render as blank filler tiles,
    // so a sparse wheel (3 possibles) still reads as a full spinning drum.
    const lo = Math.floor(p) - radius;
    const hi = Math.ceil(p) + radius;
    const isFocusWheel = focus?.key === w.key;
    const conns = focus ? connectionsOf(model, focus.key, focus.i) : {};
    const linkedItems = new Set(isFocusWheel ? [] : conns[w.key] || []);
    const hasPerm = !!slotBy[w.key];
    const linkedSlots = new Set([...linkedItems].map((i) => slotOf(w.key, i)));
    // Second-degree items: they now GATHER (Brett 2026-07-25) — `scheduleReorders`
    // and `retarget` fold them into the reorder + elastic alignment through
    // `gatherOf`, so they come to rest near the first-degree tiles in the window
    // (a wheel reached ONLY at second degree spins in rather than sitting still).
    // Here they keep the DIMMED second-degree styling, not the teal first-degree
    // linked band or parking: they gather AROUND the first-degree tiles, which
    // keep priority on the line. The badge rail below stays first-degree only.
    const secondDeg = focus ? secondDegreeOf(model, focus.key, focus.i) : {};
    const secondItems = new Set(secondDeg[w.key] || []);

    pruneTiles(tiles, lo, hi, linkedSlots);
    // Parking only applies to UN-reordered wheels (a reordered wheel's links
    // are contiguous by construction): a parked link (beyond ~1.8 steps)
    // draws on top of whatever tile owns that slot — fade the covered tile
    // so the link floats readably instead of colliding.
    const parkedDs = [];
    if (!isFocusWheel && !hasPerm) {
      for (const s of linkedSlots) {
        const dRaw = s - p;
        if (Math.abs(dRaw) > 1.8) parkedDs.push(linkedDrawDistance(dRaw));
      }
    }
    // THE BADGE RAIL'S OWN BAND (T092 acceptance sweep, defect 14b). The rail
    // is parked below the focused centre tile, which the reel's locked spacing
    // leaves only ~6px of room for, so its chips land on the NEXT tile and
    // cover its sub-line — measured in the DOCUMENTS and STAGED columns and
    // present in every wheel screenshot of the sweep. Reserving the 13px would
    // mean moving Brett's locked reel geometry, so the rail is treated as the
    // parked link directly above already is: the tile it crosses is faded, and
    // the chips take the solid backdrop (styles.css), so the rail reads as the
    // focused tile's own floating chrome rather than a half-rendered neighbour.
    const railShowing = isFocusWheel
      && WHEEL_KEYS.some((k) => k !== w.key && (conns[k] || []).length);
    const expandedTile = isFocusWheel && expanded ? tiles.get(slotOf(w.key, focus.i)) : null;
    const railBand = railShowing
      ? badgeRailBand(winH, scaleF, expandedTile?.classList.contains("wheelexpanded")
        ? (expandedTile.classList.contains("wheel-hassummary") ? 144 : 132)
        : null)
      : null;
    for (const s of drawIndices(lo, hi, linkedSlots)) {
      const idx = itemAtSlot(w.key, s);
      let tile = tiles.get(s);
      if (!tile) { tile = tileFor(w, idx); tiles.set(s, tile); win.appendChild(tile); }
      const dRaw = s - p;
      const isLinked = linkedSlots.has(s);
      const d = (!isFocusWheel && isLinked && !hasPerm)
        ? linkedDrawDistance(dRaw) : dRaw;
      const focused = isFocusWheel && idx === focus.i && Math.abs(d) < 0.6;
      // The tile's SESSION-LOCAL decoration. Formerly the dispose verdict on
      // the possibles column alone; 011 extends it to the tiles the four
      // action-row verbs act on, so a recorded commission or a recorded
      // demotion is visible without touching the snapshot (FR-034). View state
      // only: nothing is persisted and a reload clears it.
      const appliedVerdict = w.items[idx]
        ? ((w.key === "possibles" ? appliedOutcome(w.items[idx].id) : null)
           || sessionActOn(w.key, w.items[idx].id))
        : null;
      const isExpanded = !!w.items[idx] && isExpandedTile(expanded, w.key, idx);
      const isSecondDeg = !isLinked && secondItems.has(idx);
      const box = layoutTile(tile, d, isFocusWheel, isLinked, focused, appliedVerdict,
        isExpanded, isSecondDeg);
      if (w.items[idx]) {
        // summary before health, so the expanded staged tile mounts in reading
        // order: label · sub · summary · health block · action row
        syncSummary(tile, w, idx, isExpanded);
        syncHealth(tile, w, idx, focused, isExpanded);
        syncActions(tile, w, idx, isExpanded);
      }
      if (!isLinked && parkedDs.some((pd) => Math.abs(d - pd) < 0.75)) {
        tile.style.opacity = (Number.parseFloat(tile.style.opacity) * 0.2).toFixed(2);
      }
      // the same rule, applied to the badge rail's own band: the focused tile
      // owns the rail, so it is never the tile that cedes to it
      if (railBand && !focused && !isExpanded && bandsOverlap(box, railBand)) {
        tile.classList.add("wheelrailcovered");
        tile.style.opacity = (Number.parseFloat(tile.style.opacity) * 0.25).toFixed(2);
      } else {
        tile.classList.remove("wheelrailcovered");
      }
    }
    if (isFocusWheel) renderBadgeRail(w.key, conns);
    else cols[w.key].badgeRail.hidden = true;
  }

  // The badge rail (locked prototype): "n <class>" chips per connected wheel,
  // parked BELOW the focused centre tile; clicking a chip pages the carousel
  // to that column (expanding it if collapsed) and pulses it.
  function renderBadgeRail(key, conns) {
    const rail = cols[key].badgeRail;
    const railFor = key + ":" + (focus?.i ?? "");
    rail.hidden = false;
    if (railKey === railFor) return;
    railKey = railFor;
    rail.innerHTML = "";
    let any = false;
    for (const k of WHEEL_KEYS) {
      const linked = conns[k];
      if (!linked?.length || k === key) continue;
      any = true;
      const chip = el("button", "wheelchip", linked.length + " " + WHEEL_LABELS[k]);
      chip.type = "button";
      chip.title = "view the " + linked.length + " connected " + WHEEL_LABELS[k];
      chip.addEventListener("click", (ev) => {
        ev.stopPropagation();
        pageToColumn(k);
      });
      rail.appendChild(chip);
    }
    if (!any) rail.appendChild(el("span", "wheelchip wheelchip-none", "no links yet"));
    // the dispose tray (local action center, add-ideation-intent-plane §3):
    // mounts beside the chips when the focused tile is a pending_review
    // derived possible, the gate capability is live (loopback + actor), and
    // no verdict has been applied this session.
    if (key === "possibles" && focus && gateCapable(caps)) {
      const item = wheelByKey("possibles").items[focus.i];
      if (item?.derivedPending && !appliedOutcome(item.id)) {
        mountDisposeTray(rail, item, { onApplied: () => { railKey = ""; drawAll(); } });
      }
    }
    // (the propose button is NOT here: per-wheel verbs moved INSIDE the tile,
    // visible only while it is expanded — see syncActions + ACTION_MOUNTERS.
    // The rail keeps the locked prototype's connection chips and the possibles
    // dispose tray.)
  }

  // ---- threads (SVG beziers, class-coded, anchored at tile edges) ----
  function colCentreX(key) {
    const { col } = cols[key];
    // deck-space x, corrected by the carousel transform
    const m = /translateX\((-?\d+(?:\.\d+)?)px\)/.exec(deck.style.transform || "");
    const shift = m ? Number.parseFloat(m[1]) : 0;
    return col.offsetLeft + shift + col.offsetWidth / 2;
  }
  function tileY(key, i, focused) {
    return winTop + winH / 2 +
      drum(slotOf(key, i) - pos[key], focus?.key === key).y;
  }
  // Class per linked endpoint for the CURRENT focus (both edge directions).
  function threadClasses() {
    const classByEdge = new Map();
    for (const e of model.edges) {
      const [fk, fi] = e.from, [tk, ti] = e.to;
      if (fk === focus.key && fi === focus.i) classByEdge.set(tk + ":" + ti, e.cls);
      if (tk === focus.key && ti === focus.i) classByEdge.set(fk + ":" + fi, e.cls);
    }
    return classByEdge;
  }
  // Is `idx` on wheel `key` currently a rendered tile? Second-degree
  // connectors (below) never force a tile into view — they only draw when
  // the second-degree endpoint already happens to be on screen.
  function tileRendered(key, idx) {
    return !hidden.has(key) && cols[key].tiles.has(slotOf(key, idx));
  }
  function drawThreads() {
    svg.replaceChildren();
    svg.setAttribute("viewBox", "0 0 " + port.clientWidth + " " + port.clientHeight);
    if (!focus || hidden.has(focus.key)) return;
    const conns = connectionsOf(model, focus.key, focus.i);
    const classByEdge = threadClasses();
    const cx0 = colCentreX(focus.key);
    const y0 = tileY(focus.key, focus.i, true);
    // The FOCUSED endpoint's real half-width (T092 acceptance sweep, defect
    // 14a). It is magnified — 1.35x focused, EXPANDED.scale expanded — and the
    // anchor used to be half the RESTING width, so the teal bundle began ~37px
    // inside the expanded card and struck through its health line.
    const focusScale = endpointScale(0, true,
      isExpandedTile(expanded, focus.key, focus.i));
    // Rendered position of every first-degree tile ("key:i" -> { cx, y }),
    // captured while drawing its thread, so the second-degree pass below
    // anchors at the EXACT same point rather than recomputing (and risking
    // drifting from) the parked/reordered geometry.
    const firstPos = new Map();
    for (const [key, linked] of Object.entries(conns)) {
      if (hidden.has(key)) continue;
      const cx1 = colCentreX(key);
      // anchor threads at the facing tile EDGES (the locked prototype), so
      // pulled tiles resting off-centre keep visible curvature at rest.
      const goRight = cx1 >= cx0;
      const x0 = threadAnchorX(cx0, goRight, TILE_W * scaleF, focusScale);
      for (const i of linked) {
        // parked linked tiles are always in-window now; anchor the thread
        // at the same parked geometry the tile renders with.
        const dRaw = slotOf(key, i) - pos[key];
        const dd = slotBy[key] ? dRaw : linkedDrawDistance(dRaw);
        const y1 = winTop + winH / 2 + drum(dd).y;
        // the far endpoint's own half-width, by the same one definition
        const x1 = threadAnchorX(cx1, !goRight, TILE_W * scaleF,
          endpointScale(dd, false, isExpandedTile(expanded, key, i)));
        firstPos.set(key + ":" + i, { cx: cx1, y: y1 });
        const cls = classByEdge.get(key + ":" + i) || "indexed";
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", threadPath(x0, y0, x1, y1));
        path.setAttribute("class", "wheelthread thread-" + cls);
        svg.appendChild(path);
      }
    }
    // ---- second-degree connectors (Brett 2026-07-25: always-on
    // second-degree, dimmed) --------------------------------------------
    // One dimmed bezier per REAL edge from a first-degree tile to its
    // second-degree neighbour (never from the focused tile itself — the pure
    // `secondDegreeOf` already anchors edges at the first-degree endpoint).
    // Drawn only when BOTH ends are already on screen: a second-degree tile
    // is never forced into view the way a first-degree link is, so this is
    // purely an additional line over whatever is already rendered.
    for (const edge of secondDegreeOf(model, focus.key, focus.i).edges || []) {
      const [fk, fi] = edge.from;
      const [tk, ti] = edge.to;
      if (hidden.has(fk) || hidden.has(tk)) continue;
      const from = firstPos.get(fk + ":" + fi);
      if (!from || !tileRendered(tk, ti)) continue;
      const toCx = colCentreX(tk);
      const toY = tileY(tk, ti);
      const goRight = toCx >= from.cx;
      const xFrom = threadAnchorX(from.cx, goRight, TILE_W * scaleF,
        endpointScale(0, false, isExpandedTile(expanded, fk, fi)));
      const xTo = threadAnchorX(toCx, !goRight, TILE_W * scaleF,
        endpointScale(0, false, isExpandedTile(expanded, tk, ti)));
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", threadPath(xFrom, from.y, xTo, toY));
      path.setAttribute("class", "wheelthread thread-seconddeg");
      svg.appendChild(path);
    }
  }

  function drawAll() {
    for (const w of model.wheels) drawWheel(w);
    drawThreads();
    placeFlyout(); // keep the flyout on its tile (and drop it if the tile went)
  }

  // initial focus (locked prototype): the richest DOCUMENT — the one with the
  // highest total degree — centred and aligned, no entry spin.
  const docsWheel = model.wheels.find((w) => w.key === "documents" && w.items.length);
  const start = docsWheel || model.wheels.find((w) => w.items.length);
  if (start) {
    let best = 0, bestDegree = -1;
    start.degrees.forEach((degree, i) => {
      if (degree > bestDegree) { bestDegree = degree; best = i; }
    });
    pos[start.key] = best;
    setFocus(start.key, best);
  }
  drawAll();
  pageTo(0);

  // The wheel window's CSS height tracks the browser viewport, so the 430px
  // WIN_H fallback is wrong the moment layout settles: measure after first
  // paint and on every later size change, or the drum axis/radius/threads
  // are all built for the wrong cylinder.
  requestAnimationFrame(refreshWinH);
  const sizeObserver = new ResizeObserver(() => {
    if (!root.isConnected) { sizeObserver.disconnect(); closeFlyout(); return; }
    refreshWinH();
  });
  sizeObserver.observe(port);

  return {
    redraw() { drawAll(); pageTo(page); },
    // global header search: centre the first matching tile (docs first).
    search(term) {
      const needle = String(term || "").trim().toLowerCase();
      if (!needle) return;
      for (const w of model.wheels) {
        const i = w.items.findIndex((it) =>
          it.label.toLowerCase().includes(needle) ||
          String(it.id).toLowerCase().includes(needle));
        if (i >= 0) {
          if (hidden.has(w.key)) setHidden(w.key, false);
          setFocus(w.key, i);
          return;
        }
      }
    },
  };
}
