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
  buildLensModel, docSummaries, savePlan, clusterPlan, WORKBENCH_DIR,
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
    filterHint: "filter keywords…",
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
    filterHint: "filter repositories…",
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
  h.appendChild(el("span", null, vocab.terms));
  h.appendChild(el("span", "n", model.rail.length + " " + vocab.railCount));
  pane.appendChild(h);

  // #13 keyword-rail text filter — narrows the (long) declared rail. Filter
  // state lives on the lens state so it survives a draw() rebuild; typing just
  // toggles row visibility (no rebuild), so the input keeps focus.
  const filter = document.createElement("input");
  filter.className = "kwfilter";
  filter.type = "search";
  filter.placeholder = vocab.filterHint;
  filter.setAttribute("aria-label", "Filter " + vocab.terms);
  filter.value = ctx.getKwFilter();
  pane.appendChild(filter);

  const coocc = new Map();
  for (const hint of model.coOccurrence) coocc.set(hint.keyword, hint);

  const items = [];
  for (const kw of model.rail) {
    const row = el("label", "kwrow");
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
    row.appendChild(el("span", "kw", kw.keyword));

    const pin = el("button", "pinbtn" + (kw.pinned ? " pinned" : ""), kw.pinned ? "📌" : "📍");
    pin.type = "button";
    pin.title = kw.pinned ? "pinned (required) — click to unpin" : "pin = require";
    pin.setAttribute("aria-pressed", String(kw.pinned));
    pin.addEventListener("click", (ev) => { ev.preventDefault(); ctx.togglePinned(kw.keyword); });
    row.appendChild(pin);

    row.appendChild(el("span", "cnt", String(kw.declaredCount)));
    pane.appendChild(row);

    // co-occurrence hint under an UNCHECKED keyword (checked ones are already in).
    const hint = coocc.get(kw.keyword);
    let hintEl = null;
    if (hint && (hint.pulledInward || hint.newDocs)) {
      hintEl = el("div", "kwhint", hint.hint);
      pane.appendChild(hintEl);
    }
    items.push({ kw: String(kw.keyword).toLowerCase(), row, hintEl });
  }

  function applyKwFilter(value) {
    const q = String(value || "").trim().toLowerCase();
    for (const it of items) {
      const vis = !q || it.kw.includes(q);
      it.row.hidden = !vis;
      if (it.hintEl) it.hintEl.hidden = !vis;
    }
  }
  filter.addEventListener("input", () => { ctx.setKwFilter(filter.value); applyKwFilter(filter.value); });
  applyKwFilter(filter.value);

  pane.appendChild(el("div", "kwhint",
    "Declared Topics: only (solid dots). Inferred tags — hollow dots, radial " +
    "strength — arrive with document-cataloging; deferred in v1."));
  return pane;
}

// ---- pane 2: bullseye (the shared widget) + the always-present flat matrix ----

function matrix(model) {
  const table = el("table", "lensmatrix");
  table.setAttribute("aria-label", "Keyword membership matrix (flat view of the bullseye)");
  const head = el("tr");
  head.appendChild(el("th", null, "doc"));
  for (const k of model.checked) head.appendChild(el("th", null, k));
  head.appendChild(el("th", null, "ring"));
  table.appendChild(head);
  for (const r of model.matrix) {
    const tr = el("tr");
    tr.appendChild(el("td", null, String(r.document).split("/").pop() || r.document));
    for (const cell of r.cells) tr.appendChild(el("td", null, cell.present ? "✓" : "·"));
    tr.appendChild(el("td", null, r.ring));
    table.appendChild(tr);
  }
  if (!model.matrix.length) {
    const tr = el("tr");
    const td = el("td", "empty", "no documents match the checked keywords");
    td.setAttribute("colspan", String(model.checked.length + 2));
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

// ---- pane 3b: DRILL-IN (D21) — the repository lens's third pane ----------
//
// One labelled row per region the bullseye draws, innermost first: the centre
// (carried by every visible repository) and each sector (an exact repository
// combination). The rows are the discoverable twin of the bullseye's hit
// regions, and both call the same `ctx.onDrill`.
function drillPane(model, ctx) {
  const pane = el("div", "pane pane-drill");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "drill in"));
  h.appendChild(el("span", "n", model.universe.length + " identities"));
  pane.appendChild(h);

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
    const line = el("div", "drill-row");
    const label = isCentre
      ? "centre — carried by all " + row.matchCount
      : "carried by " + row.matchCount + " — " + row.keywords.join(" ∧ ");
    line.appendChild(el("span", "drill-label", label));
    line.appendChild(el("span", "n", row.documents.length + " doc"
      + (row.documents.length === 1 ? "" : "s")));
    const go = el("button", "cbtn", "drill in");
    go.type = "button";
    go.title = "scope the dashboard to these " + row.documents.length
      + " document" + (row.documents.length === 1 ? "" : "s");
    go.disabled = !ctx.onDrill;
    go.addEventListener("click", () => ctx.onDrill({
      kind: isCentre ? "centre" : "sector",
      keywords: row.keywords,
      subsetKey: row.subsetKey,
    }));
    line.appendChild(go);
    // add-shared-identity-seeds: a CONVERGENT region (two or more carriers)
    // is the promotion process's first candidate rule met, so it can be
    // drafted as a DTN register seed. Single-carrier regions cannot — one
    // repository having something is not convergence — and say why.
    if (ctx.onSeed) {
      const seed = el("button", "cbtn", "draft DTN seed");
      seed.type = "button";
      seed.disabled = row.matchCount < 2;
      seed.title = row.matchCount < 2
        ? "only one repository carries these — a candidate needs two or more"
        : "draft a candidate-register seed for these " + row.matchCount
          + " carriers (text you merge; nothing is written)";
      seed.addEventListener("click", () => ctx.onSeed(row.keywords, seed));
      seed.dataset.carriers = String(row.matchCount);
      line.appendChild(seed);
    }
    pane.appendChild(line);
  }
  return pane;
}

function bullseyePane(model, ctx) {
  const vocab = ctx.vocab;
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  const n = model.checked.length;
  h.appendChild(el("span", null, "bullseye — " + n + " " +
    (n === 1 ? vocab.term : vocab.terms) +
    (vocab.id === "repositories" ? " visible" : " checked")));
  h.appendChild(el("span", "n", model.universe.length +
    (vocab.id === "repositories" ? " identities" : " docs")));
  pane.appendChild(h);
  // The activate gesture is wired ONLY for the repository vocabulary, whose
  // regions have a drill-in to run; the keyword tab keeps the SVG it drew
  // before (no callback => no hit regions at all).
  pane.appendChild(renderBullseye(model,
    ctx.onDrill ? { onActivate: ctx.onDrill } : undefined));
  // the flat matrix is ALWAYS rendered alongside — not a toggle-only alternate.
  pane.appendChild(matrix(model));
  return pane;
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
  };
  const summaries = docSummaries(working);
  const repository = working.repository || "";

  const head = el("div", "canvas-head");
  head.appendChild(el("span", "cname", vocab.title));
  head.appendChild(el("span", "pill stage", "bullseye set-builder · D13"));
  if (composed) {
    // The switch only exists where BOTH vocabularies mean something: a
    // single-repository view has no member set to lens over.
    const swap = el("span", "vocabswitch");
    for (const candidate of [VOCABULARIES.keywords, VOCABULARIES.repositories]) {
      const btn = el("button", "vocabbtn"
        + (candidate.id === vocab.id ? " vocabon" : ""), candidate.terms);
      btn.type = "button";
      btn.disabled = candidate.id === vocab.id;
      btn.title = "lens over " + candidate.terms;
      btn.addEventListener("click", () => renderLens(root, snapshot,
        { ...options, vocabulary: candidate.id }));
      swap.appendChild(btn);
    }
    head.appendChild(swap);
  }
  head.appendChild(el("span", "canvas-note", vocab.note));

  const lens = el("div", "lens");
  const status = el("div", "canvas-status");
  status.setAttribute("aria-live", "polite");
  const confirm = el("div", "canvas-confirm");
  confirm.setAttribute("aria-live", "polite");

  root.appendChild(head);
  root.appendChild(lens);
  root.appendChild(confirm);
  root.appendChild(status);

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
