// Doc list view (T010). Every governed ideation document, grouped by area, with
// its declared Topics: chips. Snapshot-only and read-only: the workbench
// tick-to-assemble gesture and the ✎ select-to-edit escape hatch are later
// stories (US7 / US8), so this view lists but never mutates.
//
// v3 sweep: buckets by a FIXED area map (#16 — the old lastArea comparison
// emitted the "other" header twice, once for the pre-ideation paths and again
// for the post-ideation ones), and grows a filter-by-stage / filter-by-area /
// sort control plus a `search(term)` hook for the global header search (#13).
//
// DOM-SAFETY: every dynamic value binds through helpers.el's textContent;
// innerHTML is only ever assigned a literal empty string to clear.

import { el, basename } from "./helpers.js";

// Fixed bucket order: ideation areas first, then the read-only reference bucket
// exactly ONCE (the #16 fix — no reliance on document sort order).
const AREA_ORDER = ["ideation/brainstorm", "ideation/staging", "other (read-only reference)"];

function areaOf(path) {
  if (path.startsWith("ideation/brainstorm/")) return "ideation/brainstorm";
  if (path.startsWith("ideation/staging/")) return "ideation/staging";
  return "other (read-only reference)";
}
function dirOf(path) {
  const i = path.lastIndexOf("/");
  return i >= 0 ? path.slice(0, i + 1) : "";
}

// Recency key: whichever declared date a document carries (absent -> "" sorts
// last). Only surfaced as a sort option when at least one document has a date.
function docDate(d) {
  const dt = d.dates || {};
  return dt.updated || dt.captured || dt.created || "";
}

// Lower-cased match haystack for the global search (path/title/stage/topics).
function docHaystack(d) {
  return [d.path, d.summary, d.kind, d.stage, ...(d.topics || [])]
    .filter(Boolean).join(" ").toLowerCase();
}

function sortDocs(docs, key) {
  const out = docs.slice();
  if (key === "stage") {
    out.sort((a, b) => (a.stage || "").localeCompare(b.stage || "") || a.path.localeCompare(b.path));
  } else if (key === "recency") {
    out.sort((a, b) => docDate(b).localeCompare(docDate(a)) || a.path.localeCompare(b.path));
  } else {
    out.sort((a, b) => a.path.localeCompare(b.path));
  }
  return out;
}

// One row. `onOpen` (T092 acceptance sweep, defect 7) is what makes the row the
// document-opening affordance it always LOOKED like: the corpus-wide list is the
// surface a human reaches for first, and it was the only document surface in the
// app that could not open anything — 177 rows with a `:hover` border restyle,
// no click handler, no tabindex, no role, computed cursor `auto`. Both lanes of
// the sweep reproduced it independently.
//
// The row opens the SAME read-only explorer/viewer overlay the wheel's `read`
// verb and the workbench's docs rows already open (app.js owns that wiring, as
// it owns every cross-view jump) — this view still never mutates and still holds
// no transport.
//
// The affordance and the behaviour are ONE decision, deliberately: with no
// `onOpen` the row carries no role, no tabindex and no `docrow-open` class, and
// the hover restyle is scoped to `.docrow-open` in styles.css. So a row can
// never again advertise itself as clickable while being inert — the two states
// the sweep said are the only acceptable ones are the only two this can render.
function docRow(d, onOpen) {
  const row = el("div", "docrow");
  const info = el("span");
  info.appendChild(el("span", "name", basename(d.path)));
  const where = [dirOf(d.path), d.stage, d.kind].filter(Boolean).join(" · ");
  info.appendChild(el("div", "where", where));
  row.appendChild(info);
  const chips = el("span", "chips");
  for (const t of d.topics || []) chips.appendChild(el("span", "tchip", t));
  row.appendChild(chips);
  if (typeof onOpen === "function") {
    row.classList.add("docrow-open");
    row.setAttribute("role", "button");
    row.tabIndex = 0;
    row.title = "open " + d.path + " in the read-only viewer";
    row.addEventListener("click", () => onOpen(d.path, d));
    row.addEventListener("keydown", (ev) => {
      if (ev.key !== "Enter" && ev.key !== " ") return;
      ev.preventDefault();               // Space must not scroll the list
      onOpen(d.path, d);
    });
  }
  return row;
}

// A labelled <select>. Options is a list of [value, text]; the change handler
// is wired by the caller.
function selectControl(labelText, options) {
  const wrap = el("label");
  wrap.appendChild(document.createTextNode(labelText + " "));
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

function renderList(list, docs, onOpen) {
  list.innerHTML = "";
  if (!docs.length) {
    list.appendChild(el("div", "empty", "no documents match the current filters"));
    return;
  }
  const byArea = new Map();
  for (const d of docs) {
    const a = areaOf(d.path);
    if (!byArea.has(a)) byArea.set(a, []);
    byArea.get(a).push(d);
  }
  // one header per area, in the fixed order — the "other" bucket can appear once
  for (const area of AREA_ORDER) {
    const group = byArea.get(area);
    if (!group?.length) continue;
    list.appendChild(el("div", "docgroup", area + " (" + group.length + ")"));
    for (const d of group) list.appendChild(docRow(d, onOpen));
  }
}

export function renderDocs(root, snapshot, opts) {
  const onOpen = (opts || {}).onOpenDoc;
  const documents = snapshot.documents || [];
  root.innerHTML = "";

  const legend = el("div", "legend");
  legend.appendChild(el("span", "g",
    "every governed ideation document (read-only projection · regenerate to refresh)"));
  root.appendChild(legend);

  const stages = [...new Set(documents.map((d) => d.stage).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b));
  const areas = AREA_ORDER.filter((a) => documents.some((d) => areaOf(d.path) === a));
  const hasDates = documents.some((d) => docDate(d));

  const state = { stage: "", area: "", sort: "path", search: "" };

  const bar = el("div", "filterbar");
  const stageCtl = selectControl("stage", [["", "all"], ...stages.map((s) => [s, s])]);
  const areaCtl = selectControl("area", [["", "all"], ...areas.map((a) => [a, a])]);
  const sortOptions = [["path", "path"], ["stage", "stage"]];
  if (hasDates) sortOptions.push(["recency", "recency"]);
  const sortCtl = selectControl("sort", sortOptions);
  const count = el("span", "count");
  bar.appendChild(stageCtl.wrap);
  bar.appendChild(areaCtl.wrap);
  bar.appendChild(sortCtl.wrap);
  bar.appendChild(count);
  root.appendChild(bar);

  const list = el("div", "doclist");
  root.appendChild(list);

  function visible() {
    const docs = documents.filter((d) =>
      (!state.stage || d.stage === state.stage)
      && (!state.area || areaOf(d.path) === state.area)
      && (!state.search || docHaystack(d).includes(state.search)));
    return sortDocs(docs, state.sort);
  }
  function apply() {
    const docs = visible();
    renderList(list, docs, onOpen);
    count.textContent = docs.length + " of " + documents.length + " docs";
  }

  stageCtl.sel.addEventListener("change", () => { state.stage = stageCtl.sel.value; apply(); });
  areaCtl.sel.addEventListener("change", () => { state.area = areaCtl.sel.value; apply(); });
  sortCtl.sel.addEventListener("change", () => { state.sort = sortCtl.sel.value; apply(); });

  apply();
  return {
    redraw: apply,
    search(term) { state.search = String(term || "").trim().toLowerCase(); apply(); },
  };
}
