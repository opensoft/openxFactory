// Realization funnel view (T009). Grows the mockup's six-column docs-first
// funnel: SVG #edgeLayer hand-drawn edges, per-hop link tallies rendered
// VERBATIM from the snapshot's cluster.tallies (links, not cards), the
// five-column collapsed-docs modifier as the opt-in (six columns is default),
// and the mockup's hover-to-trace + click-to-pin interaction. Reads only the
// in-memory snapshot object app.js fetched; issues no network/filesystem read.
//
// v3 sweep:
//   #14  the source-docs column shows IDEATION docs (brainstorm+staging) by
//        default; a topic-less non-ideation doc no longer renders as an orphan
//        card. A "show full corpus" toggle brings the rest back.
//   #15  one-member clusters collapse into a single expandable "N singleton
//        topics" group so the multi-member clusters read as the signal.
//   #13  a stage filter on the source-docs column + a `search(term)` hook for
//        the global header search (filters the source-docs column).
// The snapshot->model derivation (model.js) is UNCHANGED — scoping/collapse are
// view-level and toggle card visibility; edges to a hidden card vanish through
// the same offsetParent guard the five-column collapse already relies on.
//
// DOM-SAFETY: every dynamic value binds through helpers.el's textContent (or a
// text node); innerHTML is only ever assigned a literal empty string to clear.

import { buildFunnelModel, visibleEdges } from "./model.js";
import { el, txt, basename, readinessHeat } from "./helpers.js";

const SVG_NS = "http://www.w3.org/2000/svg";

// A labelled <select>; the change handler is wired by the caller.
function selectControl(labelText, options) {
  const wrap = el("label");
  wrap.appendChild(txt(labelText + " "));
  const sel = document.createElement("select");
  for (const [value, text] of options) {
    const opt = document.createElement("option");
    opt.value = value;
    opt.textContent = text;
    sel.appendChild(opt);
  }
  wrap.appendChild(sel);
  return { wrap, sel };
}

function isIdeationDoc(d) {
  const p = d.path || "";
  return p.startsWith("ideation/brainstorm/") || p.startsWith("ideation/staging/");
}

// The drill-down affordance (T017/FR-008): only staged/proposal/realized
// tiles are backed by a real artifact folder in the snapshot, so only those
// three card builders accept `onOpenTile` and append this button. A separate
// button (rather than overloading the card's own click) keeps the funnel's
// existing hover-to-trace/click-to-pin gesture on the card intact.
function openButton(kind, id, onOpenTile) {
  const btn = el("button", "openbtn", "▸ open folder");
  btn.type = "button";
  btn.addEventListener("click", (ev) => {
    ev.stopPropagation();
    onOpenTile(kind, id);
  });
  return btn;
}

// ---- per-column card builders (render snapshot fields verbatim) ----

function docCard(node) {
  const d = node.document;
  const shared = (d.topics || []).length > 1;
  const card = el("div", "card stage-doc" + (shared ? " shared" : ""));
  card.id = node.domId;
  card.tabIndex = 0;
  card.dataset.node = "";
  // scoping/search metadata (#13/#14) — read by the visibility filter, never by the model.
  card.dataset.stage = d.stage || "";
  card.dataset.scoped = (isIdeationDoc(d) || (d.topics || []).length) ? "1" : "";
  card.dataset.hay = [d.path, d.stage, ...(d.topics || [])].filter(Boolean).join(" ").toLowerCase();
  card.appendChild(el("div", "id", basename(d.path)));
  const topicN = (d.topics || []).length;
  card.appendChild(el("div", "meta", (d.stage || "") + " · " + topicN + " topic" + (topicN === 1 ? "" : "s")));
  return card;
}

// a "<b>n</b> label" tally fragment, composed of nodes (no markup strings)
function tallyEntry(n, label) {
  const span = el("span");
  span.appendChild(el("b", null, String(n)));
  span.appendChild(txt(" " + label));
  return span;
}

function maybeNotebookButton(card, notebook, kind, id) {
  if (!notebook) return;
  const btn = notebook.button(kind, id);
  if (btn) card.appendChild(btn);
}

function clusterCard(node, notebook) {
  const c = node.cluster;
  const card = el("div", "card cluster-card stage-brainstorm");
  card.id = node.domId;
  card.tabIndex = 0;
  card.dataset.node = "";
  card.appendChild(el("div", "title", c.name || c.id));
  const memberN = (c.document_edges || []).length;
  card.appendChild(el("div", "meta", memberN + " contributing doc" + (memberN === 1 ? "" : "s")));
  // tallies VERBATIM from the snapshot (links, not cards)
  const t = c.tallies || {};
  const tally = el("div", "tally");
  tally.appendChild(tallyEntry(t.document_links != null ? t.document_links : memberN, "doc links"));
  tally.appendChild(tallyEntry(t.possible_links != null ? t.possible_links : 0, "possible links"));
  card.appendChild(tally);
  const heat = readinessHeat(c.readiness);
  if (heat) card.appendChild(heat);
  for (const flag of c.conflict_flags || []) {
    card.appendChild(el("span", "pill blocked", typeof flag === "string" ? flag : (flag.label || "conflict")));
  }
  maybeNotebookButton(card, notebook, "cluster", c.id);
  return card;
}

function possibleMeta(p, state, shared) {
  if (state === "picked" && p.pick) {
    let meta = "picked → " + (p.pick.staging_id || "");
    if (p.pick.change_id) meta += " · " + p.pick.change_id;
    return meta;
  }
  if ((state === "rejected" || state === "superseded") && p.reason) return state + " — " + p.reason;
  if (shared) return state + " — claimed by " + p.claiming_clusters.length + " clusters";
  return state;
}

function possibleCard(node) {
  const p = node.possible;
  const state = p.state || "latent";
  const shared = (p.claiming_clusters || []).length > 1;
  const card = el("div", "card possible " + state + " stage-brainstorm" + (shared ? " shared" : ""));
  card.id = node.domId;
  card.tabIndex = 0;
  card.dataset.node = "";
  card.appendChild(el("span", "dot"));
  const body = el("div");
  body.appendChild(el("div", "title", p.title || p.id));
  body.appendChild(el("div", "meta", possibleMeta(p, state, shared)));
  card.appendChild(body);
  return card;
}

function stagedCard(node, onOpenTile, notebook) {
  const t = node.staged;
  const card = el("div", "card stage-staged");
  card.id = node.domId;
  card.tabIndex = 0;
  card.dataset.node = "";
  card.appendChild(el("div", "title", t.staging_id));
  let meta;
  if (t.target_change) meta = "→ " + t.target_change;
  else {
    const n = (t.files || []).length;
    meta = n + " file" + (n === 1 ? "" : "s") + " · no pick yet";
  }
  card.appendChild(el("div", "meta", meta));
  if (t.readiness_state) card.appendChild(el("span", "pill neutral", t.readiness_state));
  if (onOpenTile) card.appendChild(openButton("staged", t.staging_id, onOpenTile));
  maybeNotebookButton(card, notebook, "staged", t.staging_id);
  return card;
}

function changeCard(node, stageClass, onOpenTile, kind, notebook) {
  const c = node.change;
  const card = el("div", "card " + stageClass);
  card.id = node.domId;
  card.tabIndex = 0;
  card.dataset.node = "";
  card.appendChild(el("div", "id", c.id));
  card.appendChild(el("span", "pill stage", c.status || ""));
  if (c.ratification) {
    card.appendChild(el("div", "meta", "ratified " + c.ratification.date + " · " + c.ratification.ratifier));
  }
  const tp = c.task_progress;
  if (tp?.total) {
    const pct = Math.round((100 * (tp.completed || 0)) / tp.total);
    const bar = el("div", "progress");
    const fill = el("span");
    fill.style.width = pct + "%";
    bar.appendChild(fill);
    card.appendChild(bar);
    card.appendChild(el("div", "meta", (tp.completed || 0) + " / " + tp.total + " tasks"));
  }
  if (onOpenTile) card.appendChild(openButton(kind, c.id, onOpenTile));
  // only the active-proposal column carries the NotebookLM action (kind guard);
  // realized/archived tiles do not (the action is for live governance material).
  if (kind === "proposal") maybeNotebookButton(card, notebook, "proposal", c.id);
  return card;
}

const CARD_BUILDERS = {
  possibles: (n) => possibleCard(n),
  staged: (n, cb, nb) => stagedCard(n, cb, nb),
  proposals: (n, cb, nb) => changeCard(n, "stage-proposal", cb, "proposal", nb),
  realized: (n, cb) => changeCard(n, "stage-realized", cb, "realized"),
};

// #15: multi-member clusters render as cards; one-member clusters fold into a
// single expandable group so the (many) singletons stop dominating the column.
// An empty STATION says what is absent in THIS repository rather than leaving a
// blank region or a bare dash (add-dashboard-repo-selector design D10: sparse is
// rendered, never refused — a sparse funnel is an honest funnel, and adoption of
// an ideation convention is never a precondition of being selectable).
function emptyStation(label) {
  return el("div", "empty", "no " + label + " in this repository");
}

function buildClusterColumn(stack, nodes, onToggle, notebook, label) {
  if (!nodes.length) { stack.appendChild(emptyStation(label || "topic clusters")); return; }
  const multi = nodes.filter((n) => (n.cluster.document_edges || []).length > 1);
  const singles = nodes.filter((n) => (n.cluster.document_edges || []).length <= 1);
  for (const n of multi) stack.appendChild(clusterCard(n, notebook));
  if (!singles.length) return;
  const det = document.createElement("details");
  det.className = "singleton-group";
  const sum = document.createElement("summary");
  sum.textContent = singles.length + " singleton topic" + (singles.length === 1 ? "" : "s")
    + " (one contributing doc each)";
  det.appendChild(sum);
  const inner = el("div", "col-stack");
  for (const n of singles) inner.appendChild(clusterCard(n, notebook));
  det.appendChild(inner);
  det.addEventListener("toggle", onToggle);
  stack.appendChild(det);
}

// ---- static legend, composed of nodes (no markup strings) ----

function legendDot(styleText) {
  const s = el("span");
  s.style.cssText = "width:9px;height:9px;border-radius:50%;display:inline-block;" + styleText;
  return s;
}

function legendEntry(children, styleText) {
  const g = el("span", "g");
  if (styleText) g.style.cssText = styleText;
  for (const c of children) g.appendChild(c);
  return g;
}

function buildLegend() {
  const legend = el("div", "legend");
  legend.appendChild(legendEntry([legendDot("border:1.5px dashed var(--faint-ink)"), txt(" latent possible")]));
  legend.appendChild(legendEntry([legendDot("background:var(--st-staged)"), txt(" picked at organize gate")]));
  const strike = el("span", null, "superseded");
  strike.style.textDecoration = "line-through";
  legend.appendChild(legendEntry([strike]));
  legend.appendChild(legendEntry([el("span", "edge-key dashed"), txt(" topic claim (many-to-many)")]));
  const pick = el("span", "edge-key");
  pick.style.background = "var(--edge-pick)";
  legend.appendChild(legendEntry([pick, txt(" pick edge")]));
  const flow = el("span", "edge-key");
  flow.style.background = "var(--edge-flow)";
  legend.appendChild(legendEntry([flow, txt(" gate flow")]));
  legend.appendChild(legendEntry([txt("hover to trace · click to pin the thread")], "margin-left:auto"));
  return legend;
}

// variant toggle: six columns default, five-column collapse opt-in
function buildVariantToggle() {
  const variant = el("div", "variant");
  variant.setAttribute("role", "group");
  variant.setAttribute("aria-label", "Funnel variant");
  const v6 = el("button", "vbtn", "6 columns · docs → clusters (default)");
  v6.setAttribute("aria-pressed", "true");
  const v5 = el("button", "vbtn", "5 columns · clusters only (collapse docs)");
  v5.setAttribute("aria-pressed", "false");
  variant.appendChild(v6);
  variant.appendChild(v5);
  return { variant, v6, v5 };
}

// ---- column/head assembly (extracted so renderFunnel stays an orchestrator) ----

function columnHead(col, onlyDocs) {
  const head = el("div", "colhead" + onlyDocs);
  head.appendChild(txt(col.label + " "));
  const n = el("span", "n", String(col.nodes.length));
  head.appendChild(n);
  if (col.gate) {
    head.appendChild(txt(" "));
    head.appendChild(el("span", "gatehead", col.gate));
  }
  return { head, n };
}

function fillDocsStack(stack, nodes, docCards, label) {
  const station = label || "source docs";
  if (!nodes.length) {
    stack.appendChild(emptyStation(station));
    return null;
  }
  for (const node of nodes) {
    const card = docCard(node);
    docCards.push(card);
    stack.appendChild(card);
  }
  // The source-doc FILTER can empty a populated station too — say which state the
  // reader is looking at rather than leaving a blank column (design D10's honesty
  // rule applied to the filtered case).
  const note = el("div", "empty", "no " + station + " match the current filters");
  note.hidden = true;
  stack.appendChild(note);
  return note;
}

function fillDefaultStack(stack, col, onOpenTile, notebook) {
  if (!col.nodes.length) stack.appendChild(emptyStation(col.label));
  for (const node of col.nodes) stack.appendChild(CARD_BUILDERS[col.key](node, onOpenTile, notebook));
}

function buildColumns(model, inner, onOpenTile, requestDraw, notebook) {
  const colheads = el("div", "colheads");
  const cols = el("div", "funnel-cols");
  const docCards = [];
  let docHeadN = null;
  let docsEmptyNote = null;
  for (const col of model.columns) {
    const onlyDocs = col.collapsible ? " only-docs" : "";
    const { head, n } = columnHead(col, onlyDocs);
    colheads.appendChild(head);
    const stack = el("div", "col-stack" + onlyDocs);
    if (col.key === "docs") {
      docHeadN = n;
      docsEmptyNote = fillDocsStack(stack, col.nodes, docCards, col.label);
    } else if (col.key === "clusters") {
      buildClusterColumn(stack, col.nodes, requestDraw, notebook, col.label);
    } else {
      fillDefaultStack(stack, col, onOpenTile, notebook);
    }
    cols.appendChild(stack);
  }
  inner.appendChild(colheads);
  inner.appendChild(cols);
  return { docCards, docHeadN, docsEmptyNote };
}

// #14/#13: whether a source-doc card is visible for the current scope/stage/
// search. Edges to a hidden doc vanish via the offsetParent guard in draw().
function docCardVisible(card, state) {
  if (state.search && !card.dataset.hay.includes(state.search)) return false;
  if (state.docStage && card.dataset.stage !== state.docStage) return false;
  if (!state.fullCorpus && !card.dataset.scoped) return false;
  return true;
}

// ---- directional trace (ancestors + descendants only, so hovering one
// cluster does not flood into a sibling through a shared possible) ----

function reach(id, edges) {
  const down = new Set([id]);
  let grew = true;
  while (grew) {
    grew = false;
    for (const e of edges) if (down.has(e.from) && !down.has(e.to)) { down.add(e.to); grew = true; }
  }
  const up = new Set([id]);
  grew = true;
  while (grew) {
    grew = false;
    for (const e of edges) if (up.has(e.to) && !up.has(e.from)) { up.add(e.from); grew = true; }
  }
  return new Set([...down, ...up]);
}

function applyTrace(tc, id) {
  const hot = reach(id, tc.getEdges());
  tc.inner.classList.add("focused");
  tc.paths.forEach((p) => p.classList.toggle("hot", hot.has(p.dataset.from) && hot.has(p.dataset.to)));
  tc.nodes.forEach((n) => n.classList.toggle("hot", hot.has(n.id)));
}

function clearTrace(tc) {
  tc.inner.classList.remove("focused");
  tc.paths.forEach((p) => p.classList.remove("hot"));
  tc.nodes.forEach((n) => n.classList.remove("hot"));
}

function setPinned(tc, id) {
  tc.pinned = id;
  tc.nodes.forEach((n) => n.classList.toggle("pinned", n.id === tc.pinned));
  if (tc.pinned) applyTrace(tc, tc.pinned);
  else clearTrace(tc);
}

function restoreTrace(tc) {
  if (tc.pinned) applyTrace(tc, tc.pinned);
  else clearTrace(tc);
}

function toggleNodePin(tc, nodeId) {
  const next = tc.pinned === nodeId ? null : nodeId;
  setPinned(tc, next);
  if (!next) applyTrace(tc, nodeId);
}

// Wires the hover-to-trace / click-to-pin gesture on every [data-node] card.
// Returns the trace context so the variant switch can clear an active pin.
function wireTrace(inner, paths, getEdges) {
  const tc = { inner, paths, getEdges, nodes: inner.querySelectorAll("[data-node]"), pinned: null };
  tc.nodes.forEach((node) => {
    node.addEventListener("mouseenter", () => applyTrace(tc, node.id));
    node.addEventListener("mouseleave", () => restoreTrace(tc));
    node.addEventListener("focus", () => applyTrace(tc, node.id));
    node.addEventListener("blur", () => restoreTrace(tc));
    node.addEventListener("click", () => toggleNodePin(tc, node.id));
    node.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); setPinned(tc, tc.pinned === node.id ? null : node.id); }
    });
  });
  return tc;
}

// ---- view assembly (orchestrator) ----

export function renderFunnel(root, snapshot, opts) {
  const onOpenTile = opts?.onOpenTile || null;
  const notebook = opts?.notebook || null;
  const model = buildFunnelModel(snapshot);
  root.innerHTML = "";

  const state = { fullCorpus: false, docStage: "", search: "" };
  const docCol = model.columns.find((c) => c.key === "docs");
  const docNodes = docCol ? docCol.nodes : [];

  const { variant, v6, v5 } = buildVariantToggle();
  root.appendChild(variant);

  // #14 source-docs scope + #13 stage filter
  const filterbar = el("div", "filterbar");
  const scopeCtl = selectControl("source docs",
    [["ideation", "ideation only (default)"], ["all", "show full corpus"]]);
  const docStages = [...new Set(docNodes.map((n) => n.document.stage).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b));
  const stageCtl = selectControl("stage", [["", "all"], ...docStages.map((s) => [s, s])]);
  const docCount = el("span", "count");
  filterbar.appendChild(scopeCtl.wrap);
  filterbar.appendChild(stageCtl.wrap);
  filterbar.appendChild(docCount);
  root.appendChild(filterbar);

  root.appendChild(buildLegend());

  const scroller = el("div", "scroller");
  const inner = el("div", "funnel-inner");
  inner.id = "funnel";
  const layer = document.createElementNS(SVG_NS, "svg");
  layer.setAttribute("class", "edges");
  layer.id = "edgeLayer";
  layer.setAttribute("aria-hidden", "true");
  inner.appendChild(layer);

  const { docCards, docHeadN, docsEmptyNote } = buildColumns(
    model, inner, onOpenTile, () => draw(), notebook);
  scroller.appendChild(inner);
  root.appendChild(scroller);

  // ---- edge drawing (mockup approach: cubic beziers on the SVG layer) ----
  let collapsed = false;
  let edges = visibleEdges(model, { collapsed });
  const paths = [];

  function anchor(elm, side) {
    const c = inner.getBoundingClientRect();
    const r = elm.getBoundingClientRect();
    return { x: (side === "right" ? r.right : r.left) - c.left, y: r.top + r.height / 2 - c.top };
  }
  function draw() {
    if (inner.offsetParent === null) return; // funnel tab hidden
    layer.innerHTML = "";
    paths.length = 0;
    layer.setAttribute("viewBox", "0 0 " + inner.scrollWidth + " " + inner.scrollHeight);
    layer.setAttribute("width", inner.scrollWidth);
    layer.setAttribute("height", inner.scrollHeight);
    for (const e of edges) {
      const a = document.getElementById(e.from);
      const b = document.getElementById(e.to);
      if (!a || !b) continue;
      if (a.offsetParent === null || b.offsetParent === null) continue; // hidden in this variant
      const p1 = anchor(a, "right");
      const p2 = anchor(b, "left");
      const mx = (p1.x + p2.x) / 2;
      const path = document.createElementNS(SVG_NS, "path");
      path.setAttribute("d", "M" + p1.x + " " + p1.y + " C" + mx + " " + p1.y + ", " + mx + " " + p2.y + ", " + p2.x + " " + p2.y);
      path.setAttribute("class", e.kind);
      path.dataset.from = e.from;
      path.dataset.to = e.to;
      layer.appendChild(path);
      paths.push(path);
    }
  }

  const trace = wireTrace(inner, paths, () => edges);

  function refreshDocs() {
    let shown = 0;
    for (const card of docCards) {
      const vis = docCardVisible(card, state);
      card.hidden = !vis;
      if (vis) shown += 1;
    }
    if (docHeadN) docHeadN.textContent = String(shown);
    if (docsEmptyNote) docsEmptyNote.hidden = shown > 0;
    docCount.textContent = shown + " of " + docCards.length + " docs";
    draw();
  }

  function setVariant(isCollapsed) {
    collapsed = isCollapsed;
    inner.classList.toggle("collapsed-docs", collapsed);
    v5.setAttribute("aria-pressed", String(collapsed));
    v6.setAttribute("aria-pressed", String(!collapsed));
    edges = visibleEdges(model, { collapsed });
    setPinned(trace, null);
    draw();
  }
  v5.addEventListener("click", () => setVariant(true));
  v6.addEventListener("click", () => setVariant(false));
  scopeCtl.sel.addEventListener("change", () => { state.fullCorpus = scopeCtl.sel.value === "all"; refreshDocs(); });
  stageCtl.sel.addEventListener("change", () => { state.docStage = stageCtl.sel.value; refreshDocs(); });

  const ro = new ResizeObserver(() => draw());
  ro.observe(inner);
  refreshDocs();
  requestAnimationFrame(draw);

  return {
    redraw: draw,
    search(term) { state.search = String(term || "").trim().toLowerCase(); refreshDocs(); },
  };
}
