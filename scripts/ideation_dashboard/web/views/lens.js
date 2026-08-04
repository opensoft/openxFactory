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
  const pane = el("div", "pane pane-rail");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "keywords"));
  h.appendChild(el("span", "n", model.rail.length + " declared"));
  pane.appendChild(h);

  // #13 keyword-rail text filter — narrows the (long) declared rail. Filter
  // state lives on the lens state so it survives a draw() rebuild; typing just
  // toggles row visibility (no rebuild), so the input keeps focus.
  const filter = document.createElement("input");
  filter.className = "kwfilter";
  filter.type = "search";
  filter.placeholder = "filter keywords…";
  filter.setAttribute("aria-label", "Filter keywords");
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

function bullseyePane(model) {
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "bullseye — " + model.checked.length + " keyword" +
    (model.checked.length === 1 ? "" : "s") + " checked"));
  h.appendChild(el("span", "n", model.universe.length + " docs"));
  pane.appendChild(h);
  pane.appendChild(renderBullseye(model));
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

  // lens query state (Sets for check/pin; plain maps for overrides). W1 is kept
  // as an INVARIANT of these mutators — pinned is never allowed to leave checked.
  const state = {
    checked: new Set(options.checked || []),
    pinned: new Set(options.pinned || []),
    includes: {},   // doc -> reason (manual + on a non-matching doc)
    excludes: {},   // doc -> reason (manual − on a matching doc)
    kwFilter: "",   // keyword-rail text filter (survives draw rebuilds)
  };
  const summaries = docSummaries(snapshot);
  const repository = snapshot.repository || "";

  const head = el("div", "canvas-head");
  head.appendChild(el("span", "cname", "keyword lens"));
  head.appendChild(el("span", "pill stage", "bullseye set-builder · D13"));
  head.appendChild(el("span", "canvas-note",
    "Rings by match count (centre = matches every checked keyword); pin = require " +
    "(hard filter). Overrides are evidence — a manual +/− needs a recorded reason. " +
    "Nothing is persisted until you save; machinery enters nothing into the register."));

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
    getKwFilter() { return state.kwFilter; },
    setKwFilter(v) { state.kwFilter = String(v || ""); },
    toggleChecked(keyword) {
      if (state.checked.has(keyword)) {
        state.checked.delete(keyword);
        state.pinned.delete(keyword);   // W1: a pin can't outlive its check
      } else {
        state.checked.add(keyword);
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
    const model = buildLensModel(snapshot, query());
    lens.innerHTML = "";
    lens.appendChild(keywordRail(model, ctx));
    lens.appendChild(bullseyePane(model));
    lens.appendChild(formingPane(model, ctx));
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
      const declared = new Set(buildLensModel(snapshot, query()).rail.map((k) => k.keyword));
      state.checked = new Set((keywords || []).filter((k) => declared.has(k)));
      state.pinned = new Set();
      draw();
    },
  };
}
