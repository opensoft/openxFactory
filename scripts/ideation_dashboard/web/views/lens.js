// Keyword-lens set-builder surface (T023/T024, D13) — the front door of the
// canvas: how a human names an intensional cluster the machine clustering
// missed. Snapshot-only: every value comes from the in-memory snapshot via
// lens-model.js; this view issues NO network or filesystem read. DOM-SAFETY:
// every dynamic value is bound through textContent (never innerHTML), so a
// document's declared topics / summaries / prose can never inject markup.
//
//   keyword rail   check = stratify, pin = require; declared counts + the
//                  deterministic co-occurrence hints. W1 (pinned ⊆ checked) is
//                  enforced UPSTREAM here: pinning auto-checks, unchecking unpins.
//   bullseye       rings by match count (innermost = all checked), sectored by
//                  matched subset, solid declared dots — computed SVG geometry,
//                  drawn by the SHARED widget (views/bullseye.js) this view and
//                  the staging workbench's lens panel both consume, so there is
//                  exactly ONE bullseye renderer in the bundle (D1 of
//                  add-workbench-bullseye-and-create).
//   matrix         the ALWAYS-PRESENT flat view of the SAME membership (a flat
//                  matrix MUST be available — never a toggle-only alternate).
//   forming set    the auto-included centre + near-miss candidates + the recipe
//                  line; overrides (+/−, T024) require a recorded reason.
//
// The recipe write-back (save recipe / add as cluster) is authored by lens.py
// through the interactivity boundary and materialised by the tested engine;
// serve.py stays read-only, so this surface builds a PLAN and confirms on
// screen exactly what would be persisted (the canvas.js pattern).

import {
  buildLensModel, docSummaries, railStats, termMatches,
  savePlan, clusterPlan, WORKBENCH_DIR,
  recipeRequest, clusterRequest, LENS_SAVE_ROUTE, LENS_CLUSTER_ROUTE,
} from "./lens-model.js";
// The SVG bullseye renderer lives in ONE place (add-workbench-bullseye-and-create
// design D1): this view and the staging workbench's lens panel consume the same
// widget, so the two surfaces cannot drift. This tab supplies no `onActivate`,
// so the rendered SVG is exactly what it was before the lift.
import { renderBullseye } from "./bullseye.js";
import { identitiesFor, isComposed, repositoryVocabulary } from "./composed-model.js";

// add-shared-identity-seeds: DRAFTING route (writes nothing; returns the
// register row + detail section as TEXT for a human to merge).
export const DTN_SEED_ROUTE = "/actions/dtn-seed";
// The STAGING-QUEUE seed: a topic fragment drafted from documents the human
// selected in the matrix. Same discipline as the register seed — loopback,
// write-nothing, TEXT the human places.
export const STAGING_SEED_ROUTE = "/actions/staging-seed";

//: How many of the ranked relationships the rail offers. Enough to choose
//: from, short enough to read; the whole list is the model's `pairs`.
const RELATIONSHIPS_SHOWN = 12;

// D21 (Brett, 2026-08-07: "our repo selector is now very similar to the lens
// function but for documents in repos vs keywords in documents") — the lens
// serves TWO VOCABULARIES through one widget. Only the words differ; every
// derivation, the bullseye geometry, and the co-occurrence hints are shared,
// because `repositoryVocabulary()` hands this module a snapshot in the shape
// it already reads.
export const VOCABULARIES = {
  keywords: {
    id: "keywords",
    title: "keyword lens",
    term: "keyword",
    terms: "keywords",
    railCount: "declared",
    searchHint: "search keywords…",
    railNote: "One dot per document; rings by how many checked keywords it "
      + "matches (centre = all of them). Pin = require.",
    note: "Rings by match count (centre = matches every checked keyword); "
      + "pin = require (hard filter). Overrides are evidence — a manual +/− "
      + "needs a recorded reason. Nothing is persisted until you save; "
      + "machinery enters nothing into the register.",
  },
  repositories: {
    id: "repositories",
    title: "repository lens",
    term: "repository",
    terms: "repositories",
    railCount: "members",
    searchHint: "search repositories…",
    railNote: "One dot per document identity; rings by how many visible "
      + "repositories carry it (centre = every one, ring 1 = only one). "
      + "Pin = require.",
    note: "One dot per DOCUMENT IDENTITY; rings by how many visible "
      + "repositories carry it (centre = every one of them, ring 1 = only "
      + "one). This is the filter's union/shared toggle drawn out: union is "
      + "ring 1 and inward, shared is ring 2 and inward. Pin = require. "
      + "Activate the centre or a sector to drill the dashboard into exactly "
      + "those documents.",
  },
};

// textContent-only element builder (canvas.js discipline).
function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

function shortName(path) { return String(path).split("/").pop() || path; }

// In-page override-reason capture (a11y #19) — replaces the blocking
// window.prompt(). Renders a small labelled form into `container`; on save with
// a non-empty reason it clears the form and calls `onConfirm(reason)`. All
// dynamic values bind through textContent (el()); innerHTML is only ever
// cleared. The engine still refuses a reasonless override, so an empty submit
// simply does nothing — nothing lands silently.
function renderReasonForm(container, labelText, onConfirm) {
  // single clearing helper — keeps innerHTML assignment on its own line
  function clear() {
    container.innerHTML = "";
  }
  clear();
  const form = el("div", "reason-form");
  form.appendChild(el("span", "rf-label", labelText));
  const input = document.createElement("input");
  input.type = "text";
  input.setAttribute("aria-label", labelText);
  const save = el("button", "cbtn", "record reason");
  save.type = "button";
  const cancel = el("button", "cbtn", "cancel");
  cancel.type = "button";
  function submit() {
    const reason = input.value.trim();
    if (!reason) { input.focus(); return; }
    clear();
    onConfirm(reason);
  }
  save.addEventListener("click", submit);
  cancel.addEventListener("click", clear);
  input.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") { ev.preventDefault(); submit(); }
    else if (ev.key === "Escape") { ev.preventDefault(); clear(); }
  });
  form.appendChild(input);
  form.appendChild(save);
  form.appendChild(cancel);
  container.appendChild(form);
  input.focus();
}

// On-screen confirmation of a save-recipe / add-as-cluster PLAN (T024) —
// textContent-bound, so drafted prose can never inject markup. States plainly
// where the manifest lands and, for add-as-cluster, that the human-seen proposal
// enters the cross-reference queue with a pending_review disposition (T028
// realized; the tested engine lens.add_as_cluster submits it).
function renderPlan(container, plan, opts) {
  const o = opts || {};
  container.innerHTML = "";
  const box = el("div", "draft-confirm");
  const title = plan.kind === "add-as-cluster"
    ? "planned: add as cluster (workbench set + human-seen proposal)"
    : "planned: save recipe (workbench manifest)";
  box.appendChild(el("div", "dc-h", title));
  box.appendChild(el("div", "dc-line", "set: " + plan.name + " · repository " + plan.repository));
  box.appendChild(el("div", "dc-line", plan.recipeLine));
  box.appendChild(el("div", "dc-line", "members (" + plan.members.length + "):"));
  for (const m of plan.members) {
    const tag = m.via === "manual-include" ? " (manual + — “" + m.reason + "”)" : " (recipe-match)";
    box.appendChild(el("div", "dc-line", "  • " + shortName(m.document) + tag));
  }
  if (plan.excluded.length) {
    box.appendChild(el("div", "dc-line", "excluded (" + plan.excluded.length + "):"));
    for (const e of plan.excluded) {
      box.appendChild(el("div", "dc-line", "  − " + shortName(e.document) + " — “" + e.reason + "”"));
    }
  }
  box.appendChild(el("div", "dc-line", "lands at: " + plan.landsAt));
  if (plan.pendingNote) box.appendChild(el("div", "dc-note", plan.pendingNote));
  // GATE SEAM (add-lens-gate-verbs): when the local gate capability is live
  // (loopback + real checkout + resolved actor), the plan gains an execute
  // affordance that posts to the verb route. On the deployed static image the
  // capability is absent, so this whole block is skipped and the panel stays
  // plan-only — byte-for-byte the read-only posture that ships today.
  if (gateLive(o.caps)) {
    mountExecute(box, plan, o);
  } else {
    box.appendChild(el("div", "dc-note",
      "The tested engine (lens.py) materialises this through the boundary; the " +
      "read-only surface confirms the plan — nothing is written from the browser."));
  }
  container.appendChild(box);
}

// ---- execute affordance (capability-gated) ---------------------------------

function gateLive(caps) {
  return !!(caps && caps.actions && caps.actions.gate);
}

async function postPlan(route, body, fetcher) {
  const doFetch = fetcher || fetch;
  const response = await doFetch(route, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  try {
    return await response.json();
  } catch {
    return { ok: false, message: "malformed response (HTTP " + response.status + ")" };
  }
}

// Render the landing confirmation (success) or the engine's refusal verbatim.
// textContent-bound like every other value here.
function renderOutcome(container, result) {
  container.innerHTML = "";
  if (result && result.ok) {
    const ok = el("div", "dc-landed");
    ok.appendChild(el("div", "dc-h", "landed ✓ — recorded gate dispatch"));
    ok.appendChild(el("div", "dc-line", "manifest: " + result.manifest));
    if (result.pending_entry) {
      ok.appendChild(el("div", "dc-line", "pending entry: " + result.pending_entry));
    }
    ok.appendChild(el("div", "dc-line", "gate-action record: " + result.record));
    if (result.note) ok.appendChild(el("div", "dc-note", result.note));
    container.appendChild(ok);
  } else {
    const refused = el("div", "dc-refused");
    refused.appendChild(el("div", "dc-h", "refused ✕"));
    refused.appendChild(el("div", "dc-line", (result && result.message) || "gate action failed"));
    container.appendChild(refused);
  }
}

// The execute button + its result area. A save-recipe plan posts immediately;
// an add-as-cluster plan first collects the human-seen organizer evidence (the
// engine refuses an incomplete submission, and that refusal renders here).
function mountExecute(box, plan, o) {
  const result = el("div", "dc-result");
  result.setAttribute("aria-live", "polite");
  const bar = el("div", "dc-exec");
  const run = el("button", "cbtn",
    plan.kind === "add-as-cluster" ? "execute → add as cluster" : "execute → save recipe");
  run.type = "button";
  run.title = "EXECUTES via the local gate route (actor: " + ((o.caps && o.caps.actor) || "local") + ")";

  async function dispatch(body, route) {
    run.disabled = true;
    const payload = await postPlan(route, body, o.fetcher);
    renderOutcome(result, payload);
    if (!(payload && payload.ok)) run.disabled = false;  // let a refused plan be retried
  }

  run.addEventListener("click", () => {
    if (plan.kind === "add-as-cluster") {
      renderEvidenceForm(result, (o.caps && o.caps.actor) || "", (evidence) => {
        dispatch(clusterRequest(plan, evidence), LENS_CLUSTER_ROUTE);
      });
    } else {
      dispatch(recipeRequest(plan), LENS_SAVE_ROUTE);
    }
  });
  bar.appendChild(run);
  box.appendChild(bar);
  box.appendChild(result);
}

// The human-seen organizer evidence form (add-as-cluster only). Collects the
// full contract the engine requires; a blank/short field is NOT pre-validated —
// the engine refuses and the reason renders verbatim (single source of truth).
function renderEvidenceForm(container, actor, onSubmit) {
  function clear() {
    container.innerHTML = "";
  }
  clear();
  const form = el("div", "reason-form evidence-form");
  form.appendChild(el("span", "rf-label",
    "human-seen evidence (organizer contract — the engine refuses an incomplete one):"));
  const fields = [
    ["proposer", "proposer", actor],
    ["revision", "committed revision (40/64-hex)", ""],
    ["path", "source path", ""],
    ["section", "section", ""],
    ["passage_sha256", "passage sha256 (64-hex)", ""],
    ["rationale", "rationale", ""],
    ["confidence", "confidence 0–1", ""],
    ["alternatives", "alternatives (comma-separated; may be empty)", ""],
  ];
  const inputs = {};
  for (const [key, label, value] of fields) {
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.setAttribute("aria-label", label);
    input.setAttribute("placeholder", label);
    inputs[key] = input;
    form.appendChild(input);
  }
  const submit = el("button", "cbtn", "execute");
  submit.type = "button";
  const cancel = el("button", "cbtn", "cancel");
  cancel.type = "button";
  submit.addEventListener("click", () => {
    const alts = inputs.alternatives.value.split(",").map((s) => s.trim()).filter((s) => s);
    const conf = parseFloat(inputs.confidence.value);
    onSubmit({
      proposer: inputs.proposer.value.trim(),
      revision: inputs.revision.value.trim(),
      path: inputs.path.value.trim(),
      section: inputs.section.value.trim(),
      passage_sha256: inputs.passage_sha256.value.trim(),
      rationale: inputs.rationale.value.trim(),
      confidence: Number.isNaN(conf) ? inputs.confidence.value.trim() : conf,
      alternatives: alts,
    });
  });
  cancel.addEventListener("click", clear);
  form.appendChild(submit);
  form.appendChild(cancel);
  container.appendChild(form);
}

// ---- pane 1: keyword rail (check = stratify, pin = require) ----

function keywordRail(model, ctx) {
  // `pane-rail` (T092 acceptance sweep, defect 9d): the lens now scrolls as ONE
  // region, and this is the one pane that must not — 151 declared keywords is
  // ~10,370px of rows, and unbounded it would set the height of the region the
  // bullseye and the matrix live in.
  const vocab = ctx.vocab;
  const pane = el("div", "pane pane-rail");
  const h = el("div", "pane-h");
  // This header IS the vocabulary selector where both vocabularies mean
  // something (Brett, 2026-08-08: "this area can select the keyword or
  // repo"); on a single-repository view it stays the plain label it was.
  if (ctx.vocabularies) {
    h.appendChild(ctx.vocabularies());
  } else {
    h.appendChild(el("span", null, vocab.terms));
  }
  h.appendChild(el("span", "n", model.rail.length + " " + vocab.railCount));
  pane.appendChild(h);

  // #13 keyword-rail text filter — narrows the (long) declared rail. Filter
  // state lives on the lens state so it survives a draw() rebuild; typing just
  // toggles row visibility (no rebuild), so the input keeps focus.
  // SEARCH, not filter (Brett, 2026-08-08: "the filter should be a search in
  // this case. filter implies it will affect right away the applied results.
  // but search means we need to still check the box to select it"). The
  // behaviour was always search — typing only hides rows and never touches
  // the checked set — so what was wrong was the word.
  const searchRow = el("div", "railsearch");
  const search = document.createElement("input");
  search.className = "kwfilter";
  search.type = "search";
  search.placeholder = vocab.searchHint;
  search.setAttribute("aria-label", "Search " + vocab.terms);
  search.title = "finds " + vocab.terms + " — every word must appear, in any "
    + "order, and hyphens count as spaces. Tick a row to include it.";
  search.value = ctx.getKwFilter();
  searchRow.appendChild(search);

  // ALL / NONE over what the search is SHOWING (the repo dropdown's two bulk
  // moves, brought to the rail). Scoping them to the shown rows is what makes
  // them safe next to a search box: "search campaign, take all of them".
  const bulk = el("span", "railbulk");
  const allBtn = el("button", "filterbulk", "all");
  allBtn.type = "button";
  const noneBtn = el("button", "filterbulk", "none");
  noneBtn.type = "button";
  bulk.append(allBtn, noneBtn);
  searchRow.appendChild(bulk);
  pane.appendChild(searchRow);

  // WHAT THE RADAR IS SHOWING, in the pane that has the room (Brett,
  // 2026-08-08: "this is the area we have more space to utilize. move the
  // bullseye description into here somehow. create intuitive information").
  // It replaces the bullseye's own header, which cost a title's height at
  // the top of the screen to say the same two numbers.
  const summary = el("div", "railsummary");
  const shown = model.checked.length;
  // the stat-tile idiom the rest of the shell uses: the number alone, then
  // one caption saying what it counts and over what
  summary.appendChild(el("div", "railsum-v", String(model.universe.length)));
  summary.appendChild(el("div", "railsum-k",
    vocab.id === "repositories"
      ? "document identities on the radar, across " + shown + " of "
        + model.rail.length + " repositories"
      : "documents matching " + shown + " of " + model.rail.length
        + " checked keywords"));
  summary.appendChild(el("div", "railsum-note", vocab.railNote));
  pane.appendChild(summary);

  // THE RELATIONSHIPS THAT ALREADY EXIST (Brett, 2026-08-08). The rail used
  // to ask the human to guess which of 447 keywords overlap; this offers the
  // strongest overlaps outright, and one click opens the radar ON that pair
  // instead of on an empty centre. Repository vocabularies skip it — with a
  // handful of members the rail IS the list.
  if (vocab.id === "keywords" && (model.pairs || []).length) {
    const rel = el("div", "railrel");
    const relH = el("div", "pane-h");
    relH.appendChild(el("span", null, "relationships"));
    relH.appendChild(el("span", "n", model.pairs.length + " pairs"));
    rel.appendChild(relH);
    // The count carries its UNIT. It was a bare number and had to be asked
    // about (Brett, 2026-08-08: "there is a number. what is that number
    // mean?") — a number a reader has to hover to understand is a number
    // that has not been labelled.
    rel.appendChild(el("div", "railrel-note",
      "Keyword pairs that already share documents — the count is how many "
      + "documents carry BOTH. Opening one checks both."));
    for (const pair of model.pairs.slice(0, RELATIONSHIPS_SHOWN)) {
      const row = el("button", "relrow");
      row.type = "button";
      row.title = "check " + pair.a + " and " + pair.b + " — "
        + pair.documents + " document" + (pair.documents === 1 ? "" : "s")
        + " carry both";
      row.appendChild(el("span", "relpair", pair.a + " + " + pair.b));
      row.appendChild(el("span", "reln", pair.documents
        + (pair.documents === 1 ? " doc" : " docs")));
      row.addEventListener("click", () => ctx.only([pair.a, pair.b]));
      rel.appendChild(row);
    }
    pane.appendChild(rel);
  }

  const coocc = new Map();
  for (const hint of model.coOccurrence) coocc.set(hint.keyword, hint);
  // per-term contribution, from the SAME dots the radar draws
  const stats = railStats(model);

  // The connected terms first; the LONG TAIL — terms carried by a single
  // document, two thirds of this rail — waits behind a toggle rather than
  // burying them. A checked one is always listed, so nothing in the current
  // selection can hide.
  const solos = model.rail.filter((k) => k.solo && !k.checked);
  const showSolos = ctx.getShowSolos();
  const listed = showSolos ? model.rail
    : model.rail.filter((k) => !k.solo || k.checked);

  const items = [];
  for (const kw of listed) {
    // A repository row is a TILE: few rows, a tall pane, and real facts to
    // carry. A keyword row stays compact — 305 of them is a list, not tiles.
    const row = el("label", "kwrow" + (vocab.id === "repositories" ? " repotile" : ""));
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = kw.checked;
    cb.dataset.kw = kw.keyword;
    cb.setAttribute("aria-label", "check " + kw.keyword + " (stratify)");
    if (ctx.vocab.id === "repositories") {
      cb.setAttribute("aria-label", "show " + kw.keyword + " in the view");
    }
    cb.addEventListener("change", () => ctx.toggleChecked(kw.keyword));
    row.appendChild(cb);
    const tag = el("span", "kwnum", kw.label);
    // the SAME hue the bullseye paints this term's arc and letter with
    // only the HUE — the theme picks the lightness it needs to read
    if (kw.hue != null) tag.style.setProperty("--h", String(kw.hue));
    row.appendChild(tag);
    row.appendChild(el("span", "kw", kw.keyword));

    const pin = el("button", "pinbtn" + (kw.pinned ? " pinned" : ""), kw.pinned ? "📌" : "📍");
    pin.type = "button";
    pin.title = kw.pinned ? "pinned (required) — click to unpin" : "pin = require";
    pin.setAttribute("aria-pressed", String(kw.pinned));
    pin.addEventListener("click", (ev) => { ev.preventDefault(); ctx.togglePinned(kw.keyword); });
    row.appendChild(pin);

    row.appendChild(el("span", "cnt", String(kw.declaredCount)));
    if (vocab.id === "repositories") {
      const s = stats[kw.keyword];
      const line = el("span", "repostat");
      if (!kw.checked) {
        line.textContent = kw.declaredCount + " identities · hidden from the view";
      } else if (!s) {
        line.textContent = "nothing on the radar";
      } else {
        line.textContent = s.shared + " shared with another repository · "
          + s.only + " only here";
      }
      row.appendChild(line);
    }
    pane.appendChild(row);

    // co-occurrence hint under an UNCHECKED keyword (checked ones are already in).
    const hint = coocc.get(kw.keyword);
    let hintEl = null;
    if (hint && (hint.pulledInward || hint.newDocs)) {
      hintEl = el("div", "kwhint", hint.hint);
      pane.appendChild(hintEl);
    }
    items.push({ kw: String(kw.keyword).toLowerCase(),
                 term: kw.keyword, row, hintEl });
  }

  function shownTerms(value) {
    return items.filter((it) => termMatches(it.term, value)).map((it) => it.term);
  }
  function labelBulk(value) {
    const n = shownTerms(value).length;
    const all = n === items.length;
    allBtn.textContent = all ? "all" : "all " + n;
    // the count rides the title even unscoped: checking every one of 447
    // keywords is a legitimate act with a visible cost (a 447-ring radar),
    // and the reader should see the number before the click, not after
    allBtn.title = (all ? "check every " + vocab.term + " (" + n + ")"
      : "check the " + n + " " + vocab.terms + " this search shows")
      + " — nothing is applied until a row is checked";
    noneBtn.title = all ? "uncheck every " + vocab.term
      : "uncheck the " + n + " " + vocab.terms + " this search shows";
  }
  allBtn.addEventListener("click", () => ctx.setChecked(shownTerms(search.value), true));
  noneBtn.addEventListener("click", () => ctx.setChecked(shownTerms(search.value), false));

  function applyKwFilter(value) {
    labelBulk(value);
    for (const it of items) {
      const vis = termMatches(it.term, value);
      it.row.hidden = !vis;
      if (it.hintEl) it.hintEl.hidden = !vis;
    }
  }
  search.addEventListener("input", () => {
    ctx.setKwFilter(search.value);
    applyKwFilter(search.value);
  });
  applyKwFilter(search.value);

  if (solos.length) {
    const toggle = el("button", "railmore",
      showSolos
        ? "hide the " + solos.length + " single-document " + vocab.terms
        : "show " + solos.length + " more on a single document only");
    toggle.type = "button";
    toggle.title = "a " + vocab.term + " carried by a single document can "
      + "only ever put one dot on the radar";
    toggle.addEventListener("click", () => ctx.setShowSolos(!showSolos));
    pane.appendChild(toggle);
  }

  pane.appendChild(el("div", "kwhint",
    "Declared Topics: only (solid dots). Inferred tags — hollow dots, radial " +
    "strength — arrive with document-cataloging; deferred in v1."));
  return pane;
}

// ---- pane 2: bullseye (the shared widget) + the always-present flat matrix ----

function matrix(model, ctx) {
  const table = el("table", "lensmatrix");
  table.setAttribute("aria-label", "Keyword membership matrix (flat view of the bullseye)");
  const head = el("tr");
  const pickHead = el("th", "pickcol");
  head.appendChild(pickHead);
  head.appendChild(el("th", null, "#"));
  head.appendChild(el("th", null, "doc"));
  // the column heads carry the keyword's RAIL LETTER too, so a sector label
  // like "A ∧ G" reads straight off this table
  for (const k of model.checked) {
    const tag = model.keywordLabels ? model.keywordLabels[k] : null;
    head.appendChild(el("th", null, tag ? tag + " " + k : k));
  }
  head.appendChild(el("th", null, "ring"));
  table.appendChild(head);
  // check/uncheck every listed row at once — the same all/none the rail has,
  // because a selection over 53 rows is not built one tick at a time
  if (model.matrix.length && ctx.pickDoc) {
    const all = el("input");
    all.type = "checkbox";
    all.title = "select every listed document";
    all.setAttribute("aria-label", "select every listed document");
    all.checked = model.matrix.every((r) => ctx.isPicked(r.document));
    all.addEventListener("change", () =>
      ctx.pickDocs(model.matrix.map((r) => r.document), all.checked));
    pickHead.appendChild(all);
  }
  for (const r of model.matrix) {
    const tr = el("tr");
    tr.dataset.doc = r.document;
    // SELECTION (Brett, 2026-08-08: "I should have a checkbox on each one to
    // generate the seed from checked"). The row's own box, so the set is
    // built where the evidence is read rather than retyped somewhere else.
    const pick = el("td", "pickcol");
    if (ctx.pickDoc) {
      const box = el("input");
      box.type = "checkbox";
      box.checked = ctx.isPicked(r.document);
      box.title = "include " + r.document + " in the drafted seed";
      box.setAttribute("aria-label", "select " + r.document);
      box.addEventListener("change", () => ctx.pickDoc(r.document, box.checked));
      pick.appendChild(box);
    }
    tr.appendChild(pick);
    // the matrix IS the radar's legend: #N here is the number on that dot
    tr.appendChild(el("td", "docnum", String(r.number)));
    tr.appendChild(el("td", null, String(r.document).split("/").pop() || r.document));
    for (const cell of r.cells) tr.appendChild(el("td", null, cell.present ? "✓" : "·"));
    tr.appendChild(el("td", null, r.ring));
    table.appendChild(tr);
  }
  if (!model.matrix.length) {
    const tr = el("tr");
    const td = el("td", "empty", "no documents match the checked keywords");
    td.setAttribute("colspan", String(model.checked.length + 4));
    tr.appendChild(td);
    table.appendChild(tr);
  }
  return table;
}

// The drafted DTN seed (add-shared-identity-seeds): register-format TEXT the
// human merges. Rendered read-only with a copy control — this surface never
// writes the register, and says so, exactly as the neutrality lane's
// machine-drafted seeds enter through a human merge.
function renderSeed(container, data) {
  container.innerHTML = "";
  const box = el("div", "draft-confirm");
  box.appendChild(el("div", "dc-h",
    "drafted register seed " + data.dtn + " — nothing is written"));
  box.appendChild(el("div", "dc-note",
    "Merge this into " + data.register + ": the row into the Candidate List "
    + "table, the section into Candidate Details. The seed enters the "
    + "register lifecycle only when you merge it."));
  const text = data.row + "\n\n" + data.section;
  const pre = el("pre", "seedtext", text);
  box.appendChild(pre);
  const copy = el("button", "cbtn", "copy");
  copy.type = "button";
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(text);
      copy.textContent = "copied";
    } catch {
      // clipboard denied: the text is on screen and selectable anyway
      copy.textContent = "select the text above";
    }
  });
  box.appendChild(copy);
  container.appendChild(box);
}

// The drafted STAGING fragment: the queue's own format, as text. Deliberately
// a SCAFFOLD — the header block, the documents, and the terms they share are
// computed; the argument is not, and the draft says which sections a human
// still has to write. A staging fragment that argued its own case would be
// the machine deciding what is worth staging.
function renderStagingSeed(container, data, ctx) {
  container.innerHTML = "";
  const box = el("div", "draft-confirm");
  // ONE TITLE LINE carrying everything (Brett, 2026-08-08). The panel sits
  // under the radar in the pane's most expensive vertical space, so its chrome
  // is a single row: the title, the action, and the way out.
  const head = el("div", "dc-h");
  const title = el("span", "dc-title", "drafted staging seed — nothing is written");
  // The placement instructions moved ONTO the title as its hover ("make this
  // a hover popup if I hover on the title… that will save some room"). They
  // are read once, and re-read rarely; a permanent two-line note costs the
  // document viewport underneath it on every draft.
  title.title = "Place this at " + data.path + " and finish the sections "
    + "marked TO WRITE. It enters the queue when you commit it and add its "
    + "row to ideation/staging/INDEX.md.";
  head.appendChild(title);
  // MOVE IT, do not copy it (Brett, 2026-08-08: "we need to not 'copy' this.
  // we need to have button to move this to doxBench"), and the action rides
  // the title line rather than a row of its own.
  //
  // OFFERED ONLY WHERE IT CAN LAND. A MERGED PROJECT view is a read-only
  // projection across repositories — `readOnlyCaps` strips gate/session/edit
  // by design, because there is no such thing as writing to "a project", only
  // to one of its members. This button used to be offered there anyway and
  // refused after the click, in an otherwise empty overlay (Brett,
  // 2026-08-08: "clicked open in doxBench. but it was blank"). A dead end
  // discovered at the last step is worse than one declared at the first, so
  // the refusal is stated HERE, beside the seed, and names where to go.
  const owners = ctx && ctx.ownersOf ? ctx.ownersOf(data.documents) : [];
  if (ctx && ctx.onOpenDoxbench && ctx.canCreate) {
    const move = el("button", "cbtn", "open in doxBench");
    move.type = "button";
    move.title = "carry this seed into doxBench as a new document: the "
      + "staging area, the shared terms and the provenance are filled in, "
      + "and you write the rest there";
    move.addEventListener("click", () => ctx.onOpenDoxbench(data));
    head.appendChild(move);
  } else if (ctx && ctx.onOpenDoxbench && owners.length === 1
             && ctx.onOpenRepository) {
    // ONE owner is not a decision, it is a destination — so offer the jump
    // rather than instructions to perform it. The shell re-keys to that
    // member and every verb works as it does on any single-repository view.
    const go = el("button", "cbtn", "open " + owners[0] + " to draft");
    go.type = "button";
    go.title = "A project view composes published snapshots and is read-only:"
      + " a document is created IN a repository, not in a project. This "
      + "switches to " + owners[0] + ", where the create is live. The "
      + "selection does not survive the switch — the same documents draft "
      + "this seed again there.";
    go.addEventListener("click", () => ctx.onOpenRepository(owners[0]));
    head.appendChild(go);
  } else if (ctx && ctx.onOpenDoxbench) {
    // SEVERAL owners IS a decision: these documents live in different
    // repositories, and which one owns the new document is the human's call,
    // not a click the machine can make for them.
    const why = el("span", "dc-why", owners.length
      ? "read-only here — these live in " + owners.join(", ")
        + "; open the one that should own the new document"
      : "read-only here — open a single repository to draft this");
    why.title = "A project view composes published snapshots from several "
      + "repositories, so it can be read but never written: a document is "
      + "created IN a repository, not in a project. The seed above is "
      + "complete — the same selection drafts it again there.";
    head.appendChild(why);
  }
  // A WAY BACK (Brett, 2026-08-08: "there is no back from this widget"). A
  // panel that can only be replaced by drafting something else is a panel the
  // human is stuck in; dismissing it costs nothing because nothing was
  // written, and the same selection redrafts it byte for byte.
  const back = el("button", "dc-close", "×");
  back.type = "button";
  back.title = "dismiss this draft — nothing was written, and the same "
    + "selection drafts it again";
  back.setAttribute("aria-label", "dismiss the drafted seed");
  back.addEventListener("click", () => {
    // the DOM-safety guard requires a clearing assignment to stand alone, so
    // a non-clearing one can never hide on the end of a line
    container.innerHTML = "";
    // the bar's action reads `draft` again once there is no draft to replace
    if (ctx && ctx.redraw) ctx.redraw();
  });
  head.appendChild(back);
  box.appendChild(head);
  // The panel is a VIEWPORT: it does not scroll, the DOCUMENT inside it does
  // ("this window does not need a scrollbar. lets make it a viewport and only
  // scroll the document inside"). Two nested scrollers put the chrome out of
  // reach of the very scroll that was trying to read the text.
  box.appendChild(el("pre", "seedtext", data.text));
  container.appendChild(box);
}

// The staging seed, in the shape the workbench's CREATE dialog reads. Only
// what was COMPUTED crosses over — the area, the terms every selected document
// carries, and where the seed came from. Title and summary stay empty on
// purpose: the create refuses without them, which is the same rule the seed
// itself states by marking them TO WRITE.
export function createSeedFromStagingSeed(data, repository) {
  const path = String(data?.path || "");
  const area = path.includes("/") ? path.slice(0, path.lastIndexOf("/") + 1) : "";
  const topics = (data?.shared || []).length
    ? [...data.shared] : [...(data?.partial || [])];
  return {
    tab: "docs",
    area,
    title: "",
    summary: "",
    topics,
    repositoryContext: repository || "",
    repository: repository || "",
    kind: "capability-proposal",
    // a staged fragment is born `staged`, which is one of the three statuses a
    // create accepts — a document is never born ratified
    status: "staged",
    source: "drafted from a lens selection of "
      + (data?.documents || []).length + " documents",
    documents: [...(data?.documents || [])],
    seedText: String(data?.text || ""),
  };
}

// ---- pane 3b: DRILL-IN (D21) — the repository lens's third pane ----------
//
// One labelled row per region the bullseye draws, innermost first: the centre
// (carried by every visible repository) and each sector (an exact repository
// combination). The rows are the discoverable twin of the bullseye's hit
// regions, and both call the same `ctx.onDrill`.
// A row's plain-English name for its repository combination. The pane is
// 270px wide and was reading as one run of jargon ("centre — carried by all
// 2 2 docs drill in draft DTN seed"), which is Brett's 2026-08-07 note: "I do
// not understand how to use this section. The words are jumbled together and
// do not make clear intuitive UI." Say what the set IS, in repository names.
function combinationName(row, everyVisible) {
  const names = row.keywords;
  if (names.length === 1) return "only in " + names[0];
  if (row.matchCount === everyVisible) {
    return "in all " + names.length + " visible repositories";
  }
  if (names.length === 2) return "in " + names[0] + " and " + names[1];
  return "in " + names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
}

function drillPane(model, ctx) {
  const pane = el("div", "pane pane-drill");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "drill in"));
  h.appendChild(el("span", "n", model.universe.length + " identities"));
  pane.appendChild(h);
  // The pane says what it is FOR before it lists anything — it is the one
  // place in the lens whose rows are sets rather than items.
  pane.appendChild(el("div", "drill-note",
    "Each row is the documents carried by one combination of repositories. "
    + "Drill in scopes the whole dashboard to that set; the seed drafts a "
    + "candidate-register entry for a set two or more repositories share."));

  // Group the dots by their repository combination; the centre is the
  // combination that IS the whole checked set.
  const groups = new Map();
  for (const dot of model.dots || []) {
    if (!groups.has(dot.subsetKey)) {
      groups.set(dot.subsetKey, {
        subsetKey: dot.subsetKey, keywords: dot.matchedSubset,
        matchCount: dot.matchCount, documents: [],
      });
    }
    groups.get(dot.subsetKey).documents.push(dot.document);
  }
  const rows = [...groups.values()].sort(
    (a, b) => b.matchCount - a.matchCount
      || (a.subsetKey < b.subsetKey ? -1 : 1));

  if (!rows.length) {
    pane.appendChild(el("div", "drill-empty",
      "No " + ctx.vocab.term + " is visible — tick one to draw the bullseye."));
    return pane;
  }
  for (const row of rows) {
    const isCentre = row.matchCount === model.checked.length;
    const n = row.documents.length;
    // TWO lines, not one: what the set is, then what you can do with it.
    const line = el("div", "drill-row");
    line.appendChild(el("div", "drill-what",
      combinationName(row, model.checked.length)));
    const acts = el("div", "drill-acts");
    acts.appendChild(el("span", "drill-count",
      n + " document" + (n === 1 ? "" : "s")));

    const go = el("button", "cbtn", "drill in");
    go.type = "button";
    go.title = "scope the dashboard to these " + n
      + " document" + (n === 1 ? "" : "s");
    go.disabled = !ctx.onDrill;
    go.addEventListener("click", () => ctx.onDrill({
      kind: isCentre ? "centre" : "sector",
      keywords: row.keywords,
      subsetKey: row.subsetKey,
    }));
    acts.appendChild(go);

    // add-shared-identity-seeds: a CONVERGENT region (two or more carriers)
    // is the promotion process's first candidate rule met, so it can be
    // drafted as a DTN register seed. A single-carrier row cannot — one
    // repository having something is not convergence — so it does not offer
    // the control at all rather than showing a dead one.
    if (ctx.onSeed && row.matchCount >= 2) {
      const seed = el("button", "cbtn", "draft seed");
      seed.type = "button";
      seed.title = "draft a candidate-register seed for the documents these "
        + row.matchCount + " repositories share (text you merge; nothing is "
        + "written)";
      seed.addEventListener("click", () => ctx.onSeed(row.keywords, seed));
      seed.dataset.carriers = String(row.matchCount);
      acts.appendChild(seed);
    }
    line.appendChild(acts);
    pane.appendChild(line);
  }
  return pane;
}

// The SIGNATURE GRID used to sit here — the same membership as a picture,
// collapsed behind its own finding. It is GONE from this pane (Brett,
// 2026-08-08: "we do not need this in this view… add the room to make the
// viewport to the doc list larger"). Even collapsed it cost a row of the
// pane's scarcest space, and this view is now a drafting surface: radar,
// drafted seed, document list. The derivation it read (`signatureSummary`)
// stays in the model, unused here, for the surface that wants it next.

function bullseyePane(model, ctx) {
  // `pane-bullseye`: the radar HOLDS and the matrix beneath it scrolls
  // (Brett, 2026-08-08). NO HEADER — what it said now reads in the rail,
  // which has the room, and the radar starts at the top of the screen
  // instead of a title-height below it.
  const pane = el("div", "pane pane-bullseye");
  // The activate gesture is wired ONLY for the repository vocabulary, whose
  // regions have a drill-in to run; the keyword tab keeps the SVG it drew
  // before (no callback => no hit regions at all).
  // A DOT IS ITS DOCUMENT'S CHECKBOX (Brett, 2026-08-09: "when I click a dot.
  // make it work like checking the box on the doc. turn it red and check the
  // box in the list"). Both write `ctx.pickDoc`, so the dot's colour and the
  // row's tick are one state rendered twice and cannot disagree.
  const bullseyeOpts = {};
  if (ctx.onDrill) bullseyeOpts.onActivate = ctx.onDrill;
  if (ctx.pickDoc) {
    bullseyeOpts.onDocument = (doc) => ctx.pickDoc(doc, !ctx.isPicked(doc));
  }
  pane.appendChild(renderBullseye(model,
    Object.keys(bullseyeOpts).length ? bullseyeOpts : undefined));
  // The drafted-seed panel sits DIRECTLY UNDER THE RADAR (Brett, 2026-08-08:
  // "this widget should move up to the bottom of the radar"). It began as a
  // full-width block below the whole three-pane layout; moving it to the foot
  // of this pane left it 2,772px down, past the whole matrix, which is the
  // same problem in a new place. Here it appears where the eye already is.
  if (ctx.confirmHost) pane.appendChild(ctx.confirmHost);
  // the flat matrix is ALWAYS rendered alongside — not a toggle-only alternate.
  pane.appendChild(matrix(model, ctx));
  if (ctx.pickDoc) pane.appendChild(pickBar(model, ctx));
  // SELECTED documents wear their state in every view (Brett, 2026-08-08:
  // "those dots need to change color. those are the ones I am thinking of
  // making a document about"). Applied over the whole pane once all three
  // renderers have run, and keyed the same way the hover join is — the
  // bullseye renders a membership model and knows nothing of a selection.
  if (ctx.pickDoc) {
    for (const node of pane.querySelectorAll("[data-doc]")) {
      if (ctx.isPicked(node.dataset.doc)) node.classList.add("picked");
    }
  }

  // THE JOIN, done once for the whole pane. Every view of a document carries
  // `data-doc`, so pointing at any one of them lights the others — the dot,
  // its table row, its grid row. Delegated from the pane: three renderers
  // publish a key, nothing subscribes to anything, and a redraw cannot leave
  // a stale listener behind.
  const lit = (doc, on) => {
    for (const node of pane.querySelectorAll('[data-doc="' + cssEscape(doc) + '"]')) {
      node.classList.toggle("lit", on);
    }
  };
  pane.addEventListener("pointerover", (e) => {
    const node = e.target.closest ? e.target.closest("[data-doc]") : null;
    if (node) lit(node.dataset.doc, true);
  });
  pane.addEventListener("pointerout", (e) => {
    const node = e.target.closest ? e.target.closest("[data-doc]") : null;
    if (node) lit(node.dataset.doc, false);
  });
  return pane;
}

// A document id is a path — it can carry `/`, `.` and `-`, which a selector
// reads as syntax. `CSS.escape` where the browser has it (every target does);
// the fallback keeps the node tests, which run without a DOM shim, honest.
function cssEscape(value) {
  const text = String(value);
  return (typeof CSS !== "undefined" && CSS.escape)
    ? CSS.escape(text) : text.replace(/["\\]/g, "\\$&");
}

// The selection's own bar: what is chosen, how to clear it, and the one thing
// a chosen set is FOR (Brett, 2026-08-08: "generate the seed from checked").
function pickBar(model, ctx) {
  const bar = el("div", "pickbar");
  const n = ctx.pickedCount();
  // CLEAR carries the count and sits at the LEFT, under the checkbox column it
  // undoes (Brett, 2026-08-08: "move this under the checkboxes. label it
  // clear #"). The count was a separate sentence; on the button it is both
  // the number and the way to undo it, in one control.
  const clear = el("button", "cbtn", n ? "clear " + n : "clear");
  clear.type = "button";
  clear.disabled = !n;
  clear.title = n
    ? "unselect all " + n + " selected document" + (n === 1 ? "" : "s")
    : "no documents are selected";
  clear.addEventListener("click", () => ctx.clearPicks());
  bar.appendChild(clear);
  // the DRAFT action is CENTRED on the bar — the one thing this bar is for
  const draft = el("button", "cbtn",
    // "the doc is drafted. this should be Re-Draft" — a second press over the
    // same panel replaces a draft that already exists, and the label says so
    // rather than implying a second, separate seed.
    ctx.hasDraft() ? "re-draft" : "draft staging seed");
  draft.type = "button";
  draft.disabled = !n;
  draft.title = "Draft a staging-queue fragment covering the selected "
    + "documents and the terms they share. Nothing is written — the draft is "
    + "text you carry into doxBench or place yourself.";
  draft.addEventListener("click", () => ctx.onStagingSeed(draft));
  bar.appendChild(draft);
  // the right cell balances the centre; it states the empty case, which is the
  // only time this bar has anything to explain
  bar.appendChild(el("span", "pickn", n
    ? "" : "tick documents to draft from them"));
  return bar;
}

// ---- pane 3: forming set (read-only preview; overrides + persistence in T024) ----

function whyLine(member, summaries) {
  if (member.via === "recipe-match") return "matches all checked ✓ · auto-included from centre";
  if (member.via === "manual-include") return "manual + · reason: “" + member.reason + "”";
  return "";
}

function formingPane(model, ctx) {
  const summaries = ctx.summaries;
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "forming cluster"));
  h.appendChild(el("span", "n", model.formingSet.members.length + " included"));
  pane.appendChild(h);

  for (const m of model.formingSet.members) {
    const row = el("div", "setrow");
    const left = el("span");
    const info = summaries[m.document] || {};
    left.appendChild(el("span", "nm", info.base || String(m.document).split("/").pop()));
    left.appendChild(el("div", "why", whyLine(m, summaries)));
    row.appendChild(left);
    ctx.memberControls(row, m);
    pane.appendChild(row);
  }
  for (const c of model.formingSet.candidates) {
    const row = el("div", "setrow candidate");
    const left = el("span");
    const info = summaries[c.document] || {};
    left.appendChild(el("span", "nm", info.base || String(c.document).split("/").pop()));
    left.appendChild(el("div", "why", "ring " + c.matchCount + " · not yet included"));
    row.appendChild(left);
    ctx.candidateControls(row, c);
    pane.appendChild(row);
  }
  if (!model.formingSet.members.length && !model.formingSet.candidates.length) {
    pane.appendChild(el("div", "empty", "check keywords to form a set"));
  }

  pane.appendChild(el("div", "recipe", model.recipeLine));
  ctx.persistControls(pane);
  return pane;
}

// ---- view assembly ----

export function renderLens(root, snapshot, opts) {
  const options = opts || {};
  // The gate capability verdict (from app.js's single /capabilities probe) and
  // an injectable fetcher (test seam). Gate-off => the plan panel stays
  // plan-only, exactly as the deployed static image renders.
  const caps = options.caps || null;
  // The UNSTRIPPED capability and the serve's own writable repository, read by
  // exactly one affordance: the drafted seed's hand-off into doxBench. Absent
  // (an older mount, the hosted plane), the hand-off simply is not offered.
  const createCaps = options.createCaps || caps;
  const writableRepository = options.writableRepository || null;
  const fetcher = options.fetcher || null;
  root.innerHTML = "";

  // D21 — the vocabulary. `composedSnapshot` is the UNNARROWED composed
  // snapshot (app.js hands the lens the whole aggregate on purpose: the rail
  // is the control surface for the visible set, so it must see every member,
  // exactly as the keyword rail sees every declared keyword).
  const composed = isComposed(options.composedSnapshot)
    ? options.composedSnapshot : null;
  const vocab = VOCABULARIES[
    options.vocabulary === "repositories" && composed ? "repositories" : "keywords"];
  const working = vocab.id === "repositories"
    ? repositoryVocabulary(composed) : snapshot;

  // The vocabulary switch. Built here (it needs `options` and `vocab`) and
  // MOUNTED by the rail's header, which is the area Brett pointed at. Offered
  // only where both vocabularies mean something — a single-repository view
  // has no member set to lens over. Each button carries its vocabulary's note
  // as its title: the explanation the head used to print in three lines.
  const vocabularies = composed ? () => {
    const swap = el("span", "vocabswitch");
    for (const candidate of [VOCABULARIES.keywords, VOCABULARIES.repositories]) {
      const btn = el("button", "vocabbtn"
        + (candidate.id === vocab.id ? " vocabon" : ""), candidate.terms);
      btn.type = "button";
      btn.disabled = candidate.id === vocab.id;
      btn.title = candidate.note;
      btn.addEventListener("click", () => renderLens(root, snapshot,
        { ...options, vocabulary: candidate.id }));
      swap.appendChild(btn);
    }
    return swap;
  } : null;

  // lens query state (Sets for check/pin; plain maps for overrides). W1 is kept
  // as an INVARIANT of these mutators — pinned is never allowed to leave checked.
  const state = {
    // D21: the repository lens opens on the CURRENT visible set (every member
    // by default), because an empty rail would draw an empty bullseye and the
    // set already has a meaning here — unlike keywords, which start unchosen.
    checked: new Set(vocab.id === "repositories"
      ? (options.visible || (working.keyword_index || []).map((k) => k.keyword))
      : (options.checked || [])),
    pinned: new Set(options.pinned || []),
    includes: {},   // doc -> reason (manual + on a non-matching doc)
    excludes: {},   // doc -> reason (manual − on a matching doc)
    kwFilter: "",   // keyword-rail text filter (survives draw rebuilds)
    showSolos: false,  // single-document terms are collapsed until asked for
    // documents the human ticked in the matrix — the set a staging seed is
    // drafted from. Deliberately NOT the forming set: that one is a cluster
    // recipe's membership, this one is a reading selection that survives a
    // redraw and is thrown away with the view.
    picked: new Set(),
  };
  const summaries = docSummaries(working);
  const repository = working.repository || "";

  // NO HEAD (Brett, 2026-08-08: "remove this area, it takes too much
  // screen. use the area in annotate 4 to select keyword or repo"). The tab
  // already names the view, and the one control the head carried — the
  // vocabulary switch — now lives in the rail's own header, which was
  // otherwise just a label. The note it carried survives as the switch's
  // title, so the explanation is a hover away rather than three lines tall.
  const lens = el("div", "lens");
  const status = el("div", "canvas-status");
  status.setAttribute("aria-live", "polite");
  const confirm = el("div", "canvas-confirm");
  confirm.setAttribute("aria-live", "polite");

  root.appendChild(lens);
  root.appendChild(status);
  // `confirm` is NOT appended here (Brett, 2026-08-08: "this widget should
  // move up to the bottom of the radar"). It was a full-width block below the
  // whole three-pane layout, a screen away from the button that produced it.
  // The bullseye pane adopts it on every draw, so a drafted seed appears at
  // the foot of the pane whose action produced it.

  function query() {
    return {
      checked: [...state.checked],
      pinned: [...state.pinned],
      includes: state.includes,
      excludes: state.excludes,
    };
  }

  // the interaction context threaded into the panes. T023 wires check/pin; the
  // override + persistence controls are inert placeholders here and become
  // interactive in T024.
  const ctx = {
    summaries,
    repository,
    vocab,
    vocabularies,
    confirmHost: confirm,
    // whether a drafted panel is currently on screen — the draft button's
    // label reads `re-draft` over one that already exists
    hasDraft() { return confirm.childElementCount > 0; },
    // A create needs the human gate ON THE SERVE — not on the view. D10
    // strips every acting capability from a composed snapshot because "a gate
    // verb binds to one served checkout, and a composed view has none": true
    // of a verb bound to a TILE, whose repository this serve has no writable
    // checkout for. A NEW staging document binds to no tile — it lands in the
    // serve's own checkout — so this affordance asks the unstripped probe and
    // requires a writable repository to name (Brett, 2026-08-08: "yes, we
    // need to draft from a project view").
    canCreate: !!(createCaps && createCaps.actions && createCaps.actions.gate
                  && writableRepository),
    onOpenRepository: options.onOpenRepository || null,
    // which member repositories carry these documents — so a refusal can say
    // WHERE to go rather than only that this is not the place
    ownersOf(documents) {
      const wanted = new Set((documents || []).map(String));
      const out = new Set();
      for (const doc of (composed && composed.documents) || []) {
        const id = String(doc?.id == null ? "" : doc.id);
        const tail = id.includes("::") ? id.slice(id.indexOf("::") + 2) : id;
        if (doc?.repository && (wanted.has(id) || wanted.has(tail)
            || wanted.has(String(doc.path || "")))) {
          out.add(String(doc.repository));
        }
      }
      return [...out].sort();
    },
    redraw() { draw(); },
    // The hand-off to doxBench. The lens knows what was drafted; app.js owns
    // every cross-view jump, exactly as it does for the wheel's verbs, so the
    // seed is translated into the create dialog's own shape here and the
    // opening happens there.
    onOpenDoxbench: options.onOpenDoxbench
      ? (data) => options.onOpenDoxbench(
          // the SERVE's repository, never `working.repository` — under a
          // composed view that is the PROJECT id, and a create naming a
          // repository this serve does not serve is refused by the route
          createSeedFromStagingSeed(data, writableRepository || repository))
      : null,
    // add-shared-identity-seeds — draft a register seed for a convergent
    // region. Loopback-only server side; the response is TEXT, so this
    // affordance is legitimately available on the read-only composed view
    // (nothing is written, exactly as the neutrality lane drafts seeds a
    // human merges).
    onSeed: vocab.id === "repositories" && composed
      ? async (repositories, button) => {
          const label = button.textContent;
          button.disabled = true;
          button.textContent = "drafting…";
          status.textContent = "";
          try {
            // through the SAME transport the plan panel uses: this view holds
            // no network primitive of its own (the injected fetcher or the
            // passed `fetch` reference, never a call written here).
            const data = await postPlan(DTN_SEED_ROUTE, {
              project_id: composed.repository,
              // the whole visible set defines the carrier question…
              repositories: [...state.checked],
              // …and the region's own combination is what gets drafted, so
              // the seed covers exactly the row that was clicked.
              combination: repositories,
            }, fetcher);
            if (!data || data.ok !== true) {
              status.textContent = "seed refused: "
                + (data?.message || data?.error || "no answer");
              return;
            }
            renderSeed(confirm, data);
          } catch (err) {
            status.textContent = "seed failed: " + (err?.message || "error");
          } finally {
            button.disabled = false;
            button.textContent = label;
          }
        }
      : null,
    // D21 — the bullseye's activate gesture, wired only for repositories.
    onDrill: vocab.id === "repositories" && options.onDrillIn
      ? (region) => options.onDrillIn({
          region,
          checked: [...state.checked],
          identities: identitiesFor(working, [...state.checked], region),
        })
      : null,
    // ---- the matrix selection (Brett, 2026-08-08) ----
    isPicked(doc) { return state.picked.has(doc); },
    pickedCount() { return state.picked.size; },
    pickDoc(doc, on) {
      if (on) state.picked.add(doc); else state.picked.delete(doc);
      draw();
    },
    pickDocs(docs, on) {
      for (const doc of docs || []) {
        if (on) state.picked.add(doc); else state.picked.delete(doc);
      }
      draw();
    },
    clearPicks() { state.picked = new Set(); draw(); },
    // Draft a STAGING-QUEUE fragment from the selected documents. A staging
    // seed, not a DTN register seed: the register's question is "do two
    // factories carry the same artifact", and the question a reader of this
    // radar has is "these documents keep meeting — what is the topic?". The
    // server recomputes each document's terms from its own snapshot; the
    // client names the documents and never the evidence, exactly as the
    // register seed does.
    onStagingSeed: async (button) => {
      const label = button.textContent;
      button.disabled = true;
      button.textContent = "drafting…";
      status.textContent = "";
      try {
        const data = await postPlan(STAGING_SEED_ROUTE, {
          project_id: composed ? composed.repository : repository,
          documents: [...state.picked],
        }, fetcher);
        if (!data || data.ok !== true) {
          status.textContent = "seed refused: "
            + (data?.message || data?.error || "no answer");
          return;
        }
        renderStagingSeed(confirm, data, ctx);
        // the bar is already drawn, so it has to be redrawn to read `re-draft`
        draw();
      } catch (err) {
        status.textContent = "seed failed: " + (err?.message || "error");
      } finally {
        button.disabled = false;
        button.textContent = label;
      }
    },
    getKwFilter() { return state.kwFilter; },
    setKwFilter(v) { state.kwFilter = String(v || ""); },
    toggleChecked(keyword) {
      if (state.checked.has(keyword)) {
        state.checked.delete(keyword);
        state.pinned.delete(keyword);   // W1: a pin can't outlive its check
      } else {
        state.checked.add(keyword);
      }
      // D21: in the repository vocabulary a tick IS the visible set (Brett's
      // ruling: ticking in either place moves both). Written through, never
      // reloaded — the lens holds the whole composed aggregate, so it redraws
      // any subset locally, and the rest of the shell picks the set up on its
      // next render exactly as it picks up a popover tick.
      if (vocab.id === "repositories" && options.onVisible) {
        options.onVisible([...state.checked]);
      }
      draw();
    },
    // BULK check/uncheck (Brett's 2026-08-08 all/none). One state change, one
    // write-through, one draw — toggling N terms one at a time would redraw
    // the radar N times and write the visible set N times.
    getShowSolos() { return state.showSolos; },
    setShowSolos(on) { state.showSolos = !!on; draw(); },
    // open the radar on EXACTLY these terms — the relationships list's click,
    // which replaces the selection rather than adding to it, so the pair is
    // what the rings are about
    only(terms) {
      state.checked = new Set(terms || []);
      state.pinned = new Set();
      if (vocab.id === "repositories" && options.onVisible) {
        options.onVisible([...state.checked]);
      }
      draw();
    },
    setChecked(terms, on) {
      for (const term of terms || []) {
        if (on) state.checked.add(term);
        else { state.checked.delete(term); state.pinned.delete(term); }
      }
      if (vocab.id === "repositories" && options.onVisible) {
        options.onVisible([...state.checked]);
      }
      draw();
    },
    togglePinned(keyword) {
      if (state.pinned.has(keyword)) {
        state.pinned.delete(keyword);
      } else {
        state.pinned.add(keyword);
        state.checked.add(keyword);     // W1: pinning implies checking
      }
      draw();
    },
    // ---- overrides (T024): a manual +/− REQUIRES a recorded reason. The
    // reason is captured here and the engine (workbench.add_member/exclude)
    // refuses without one — the override is evidence, never a silent set edit.
    memberControls(row, member) {
      const pm = el("span", "pm");
      if (member.via === "manual-include") {
        // undoing an earlier manual + (no reason needed to retract an add).
        const undo = el("button", "cbtn", "−");
        undo.type = "button";
        undo.title = "remove this manual include";
        undo.addEventListener("click", () => { delete state.includes[member.document]; draw(); });
        pm.appendChild(undo);
      } else {
        // − on a matching (centre) doc: an exclusion override — reason required.
        const minus = el("button", "cbtn", "−");
        minus.type = "button";
        minus.title = "exclude (records negative evidence — a reason is required)";
        minus.addEventListener("click", () => {
          renderReasonForm(status, "Exclude " + shortName(member.document) +
            " — record WHY (negative evidence, required):",
            (reason) => { state.excludes[member.document] = reason; draw(); });
        });
        pm.appendChild(minus);
      }
      row.appendChild(pm);
    },
    candidateControls(row, candidate) {
      const pm = el("span", "pm");
      const plus = el("button", "cbtn", "＋");
      plus.type = "button";
      plus.title = "include this near-miss (records a reason — required)";
      plus.addEventListener("click", () => {
        renderReasonForm(status, "Include " + shortName(candidate.document) +
          " — record WHY it belongs (required):",
          (reason) => { state.includes[candidate.document] = reason; draw(); });
      });
      pm.appendChild(plus);
      row.appendChild(pm);
    },
    persistControls(pane) {
      const box = el("div", "lens-persist");
      const save = el("button", "cbtn", "save recipe (workbench manifest)");
      save.type = "button";
      save.addEventListener("click", () => {
        const model = buildLensModel(snapshot, query());
        renderPlan(confirm, savePlan(model, repository, ctx.setName()), { caps, fetcher });
      });
      const cluster = el("button", "cbtn",
        "→ add as cluster (workbench set + human-seen proposal)");
      cluster.type = "button";
      cluster.addEventListener("click", () => {
        const model = buildLensModel(snapshot, query());
        renderPlan(confirm, clusterPlan(model, repository, ctx.setName()), { caps, fetcher });
      });
      box.appendChild(save);
      box.appendChild(cluster);
      box.appendChild(el("div", "lens-pending",
        "Persisted through the interactivity boundary to " + WORKBENCH_DIR +
        " (gitignored). Nothing enters the register or any queue from here."));
      pane.appendChild(box);
    },
    setName() {
      const kw = [...state.checked];
      return kw.length ? "lens " + kw.join(" ") : "lens set";
    },
  };

  function draw() {
    const model = buildLensModel(working, query());
    lens.innerHTML = "";
    lens.appendChild(keywordRail(model, ctx));
    lens.appendChild(bullseyePane(model, ctx));
    // The forming/persistence pane is the KEYWORD recipe's: a repository set
    // is a view, not a set to save, so the repository vocabulary shows the
    // drill-in pane in its place (which is also the labelled affordance the
    // bullseye's hit regions require — a hit region alone is undiscoverable).
    lens.appendChild(vocab.id === "repositories"
      ? drillPane(model, ctx) : formingPane(model, ctx));
  }

  draw();
  return {
    redraw: draw,
    // PRESELECTION entry point (the wheel's clusters -> lens jump, 2026-07-25):
    // the same thing `opts.checked` does at mount time, available after mount
    // because app.js renders each view once and then re-activates it. Checks
    // exactly the DECLARED keywords named (an undeclared one is dropped rather
    // than added to the rail — the rail is the snapshot's declared vocabulary),
    // and clears pins so a jump never arrives with a hidden hard filter.
    focusKeywords(keywords) {
      const declared = new Set(buildLensModel(working, query()).rail.map((k) => k.keyword));
      state.checked = new Set((keywords || []).filter((k) => declared.has(k)));
      state.pinned = new Set();
      draw();
    },
  };
}
