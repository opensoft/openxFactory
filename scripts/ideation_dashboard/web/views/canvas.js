// Cluster canvas working surface (T020/T021, D12) — the three-pane war room
// where feat quality is decided. Snapshot-only: every value comes from the
// in-memory snapshot via buildCanvasModel; this view issues NO network or
// filesystem read. DOM-SAFETY: every dynamic value is bound through
// textContent (never innerHTML), the deliberate node-choice for a surface that
// renders arbitrary governance prose (doc summaries, claims, reasons, passage
// hashes) — so a document can never inject markup into the dashboard's page.
//
//   pane 1  MEMBER DOCS      exactly the cluster's Topics-derived edges.
//   pane 2  EVIDENCE BOARD   pinned passages (section ref + passage hash) plus
//                            the GAP PROMPTS as actionable slots.
//   pane 3  POSSIBLES RAIL   grouped by option set; choose-one drafts sibling
//                            supersessions; the composer drafts a register
//                            entry — both for HUMAN COMMIT, never auto-applied
//                            (T021).
//   LINEAGE STRIP            the downstream progression (staged picks →
//                            proposals → realized), rendered SEPARATELY so
//                            downstream artifacts never appear as members.
//
// Canvas machinery mutates NO source document and enters NOTHING into any
// register; AI suggest/derive trays are explicitly OUT of scope (follow-on
// deltas). The choose-one/composer affordances build a DRAFT PLAN and confirm,
// on screen, exactly what would be committed and where it lands — the actual
// boundary-written draft artifact is authored by canvas_drafts.py.

import {
  buildCanvasModel, listCanvasClusters, supersedePlan, composerPlan, DRAFTS_DIR,
} from "./canvas-model.js";

// textContent-only element builder (viewer.js discipline) — the `text` arg is
// ALWAYS set via textContent, never innerHTML.
function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

function basename(path) {
  return String(path).split("/").at(-1) || path;
}

function shortHash(h) {
  if (!h) return "";
  return String(h).slice(0, 8) + "…";
}

// ---- pane 1: member docs (strictly the Topics-derived edges) ----
function memberPane(model) {
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "member docs"));
  h.appendChild(el("span", "n", String(model.members.length)));
  pane.appendChild(h);

  for (const m of model.members) {
    const card = el("div", "card member");
    card.appendChild(el("div", "id", basename(m.document)));
    if (m.doc?.summary) card.appendChild(el("div", "summ", m.doc.summary));
    const topics = (m.matchedTopics || []).join(", ");
    if (topics) card.appendChild(el("span", "pill neutral", "Topics: " + topics));
    // flag an unclaimed member inline (the same doc also raises a gap slot in
    // the evidence board pane).
    const unclaimed = model.gaps.some(
      (g) => g.kind === "unclaimed-member" && g.document === m.document);
    if (unclaimed) card.appendChild(el("span", "pill blocked", "unclaimed by any possible"));
    pane.appendChild(card);
  }
  if (!model.members.length) pane.appendChild(el("div", "empty", "no member docs"));

  // draft-affordance (follow-on authoring story): proposing membership scaffolds
  // a Topics: edit in the human's editor — never written here.
  const propose = el("button", "cbtn", "＋ propose membership — scaffolds a Topics: edit for your editor (follow-on)");
  propose.type = "button";
  propose.disabled = true;
  pane.appendChild(propose);
  return pane;
}

// ---- pane 2: evidence board + gap prompts ----
function evidencePane(model) {
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "evidence board"));
  h.appendChild(el("span", "n", model.evidence.length + " pinned"));
  pane.appendChild(h);

  for (const pin of model.evidence) {
    const passage = el("div", "passage");
    // A read-projection v1 shows the pin's coordinates (doc · section · hash),
    // not the passage prose (prose is source pass-through in the viewer, D15).
    passage.appendChild(el("div", "ptitle", pin.possibleTitle));
    const src = el("div", "src");
    src.textContent = basename(pin.document) +
      (pin.section ? " · §" + pin.section : "") +
      (pin.passage_sha256 ? " · passage " + shortHash(pin.passage_sha256) : "");
    passage.appendChild(src);
    pane.appendChild(passage);
  }
  if (!model.evidence.length) pane.appendChild(el("div", "empty", "no pinned evidence"));

  // pin-passage draft-affordance (follow-on: authoring/workbench story).
  const pin = el("button", "cbtn", "＋ pin passage from a member doc (follow-on)");
  pin.type = "button";
  pin.disabled = true;
  pane.appendChild(pin);

  // GAP PROMPTS as actionable slots — both derivations from the snapshot.
  for (const g of model.gaps) {
    const slot = el("div", "gapslot");
    if (g.kind === "unclaimed-member") {
      slot.appendChild(el("div", "title", "gap: " + basename(g.document) + " unclaimed by any possible"));
      slot.appendChild(el("div", "meta",
        (g.summary ? g.summary + " — " : "") +
        "a latent feat is waiting to be named here. Compose it in the possibles rail →"));
    } else {
      slot.appendChild(el("div", "title", "gap: possible has no document support"));
      slot.appendChild(el("div", "meta",
        "“" + g.possibleTitle + "” (" + g.state + ") pins no passage — pin evidence from a member doc."));
    }
    pane.appendChild(slot);
  }
  return pane;
}

// ---- pane 3: possibles rail (T021 makes this interactive) ----
function possibleCard(p) {
  const state = p.state || "latent";
  const card = el("div", "card possible " + state);
  card.appendChild(el("span", "dot"));
  const body = el("div");
  body.appendChild(el("div", "title", p.title || p.id));
  let meta = state;
  if (state === "picked" && p.pick) {
    meta = "picked → " + (p.pick.staging_id || "");
    if (p.pick.change_id) meta += " · " + p.pick.change_id;
  } else if ((state === "rejected" || state === "superseded") && p.reason) {
    meta = state + " — " + p.reason;
  }
  body.appendChild(el("div", "meta", meta));
  card.appendChild(body);
  return { card, body };
}

// The possibles rail (T021): option-set CHOOSE-ONE drafts sibling
// supersessions; the COMPOSER drafts a new latent register entry. Both build a
// DRAFT PLAN and confirm — on screen — exactly what would be committed and
// where it lands (a run-local drafts dir under the boundary allowlist); the
// register is never touched here. The boundary-written artifact is authored by
// canvas_drafts.py — this v1 read-projection surface has no write-back endpoint
// (serve.py is read-only), so the browser confirms the plan while the tested
// Python engine materialises the validated draft file.
function possiblesRail(model, ctx) {
  const pane = el("div", "pane");
  const h = el("div", "pane-h");
  h.appendChild(el("span", null, "possibles — this cluster"));
  h.appendChild(el("span", "n", String(model.possibles.length)));
  pane.appendChild(h);

  for (const p of model.standalone) pane.appendChild(possibleCard(p).card);

  for (const os of model.optionSets) {
    const box = el("div", "optset");
    box.appendChild(el("div", "oh", "option set · " + os.id + " — choose one; siblings draft superseded"));
    for (const p of os.members) {
      const { card, body } = possibleCard(p);
      const choose = el("button", "cbtn", "choose this — draft sibling supersession");
      choose.type = "button";
      choose.addEventListener("click", () => {
        const plan = supersedePlan(ctx.snapshot, model.cluster.id, os.id, p.id);
        ctx.confirmSupersede(plan);
      });
      body.appendChild(choose);
      box.appendChild(card);
    }
    pane.appendChild(box);
  }
  if (!model.possibles.length) pane.appendChild(el("div", "empty", "no possibles claim this cluster"));

  pane.appendChild(composerForm(model, ctx));

  // AI suggest/derive trays are explicitly OUT of scope (follow-on deltas) —
  // surfaced as an inert note so the boundary is visible on the surface.
  pane.appendChild(el("div", "canvas-ai-note",
    "AI suggest / derive-possibles trays are out of scope here — follow-on deltas."));
  return pane;
}

// The composer form (T021): name + title + claim + optional evidence pins from
// the cluster's board → drafts a latent possibles-register entry for human
// commit.
function composerForm(model, ctx) {
  const box = el("div", "composer");
  box.appendChild(el("span", "ch", "compose possible → draft register entry (human commits)"));

  const name = el("input");
  name.setAttribute("aria-label", "Possible id");
  name.placeholder = "id — e.g. regulated-traceability-profile";
  const title = el("input");
  title.setAttribute("aria-label", "Possible title");
  title.placeholder = "title";
  const claim = el("textarea");
  claim.setAttribute("aria-label", "Possible claim");
  claim.rows = 2;
  claim.placeholder = "one-line claim…";
  box.appendChild(name);
  box.appendChild(title);
  box.appendChild(claim);

  // attach evidence: one checkbox per distinct pinned document on the board.
  const boardDocs = [];
  const seen = new Set();
  for (const pin of model.evidence) {
    if (!seen.has(pin.document)) { seen.add(pin.document); boardDocs.push(pin.document); }
  }
  const checks = [];
  if (boardDocs.length) {
    const attach = el("div", "attach");
    attach.appendChild(el("span", "ch", "attach pinned evidence"));
    for (const doc of boardDocs) {
      const label = el("label", "attach-row");
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.value = doc;
      checks.push(cb);
      label.appendChild(cb);
      label.appendChild(el("span", null, basename(doc)));
      attach.appendChild(label);
    }
    box.appendChild(attach);
  }

  const draftBtn = el("button", "cbtn", "draft register entry (human commits)");
  draftBtn.type = "button";
  draftBtn.addEventListener("click", () => {
    const evidenceDocuments = checks.filter((c) => c.checked).map((c) => c.value);
    const plan = composerPlan(ctx.snapshot, model.cluster.id, {
      id: name.value, title: title.value, claim: claim.value, evidenceDocuments,
    });
    ctx.confirmComposer(plan);
  });
  box.appendChild(draftBtn);
  return box;
}

// On-screen confirmation of a drafted transition/entry — textContent-bound, so
// arbitrary drafted prose can never inject markup. Shows what is drafted and
// the declared output path it lands at; states plainly that nothing entered the
// register.
function renderConfirm(container, plan, kind) {
  container.innerHTML = "";
  if (!plan) {
    container.appendChild(el("div", "meta", "nothing to draft for this selection"));
    return;
  }
  const box = el("div", "draft-confirm");
  if (kind === "supersede") {
    box.appendChild(el("div", "dc-h", "drafted: option-set supersession (human commits)"));
    box.appendChild(el("div", "dc-line",
      "chosen: " + plan.chosenId + " · supersedes " + plan.siblings.length +
      " sibling" + (plan.siblings.length === 1 ? "" : "s")));
    for (const s of plan.siblings) {
      box.appendChild(el("div", "dc-line", "  • " + s.title + " (" + s.id + "): " + s.fromState + " → superseded"));
    }
    box.appendChild(el("div", "dc-line", "reason: " + plan.reason));
    box.appendChild(el("div", "dc-line", "citation: " + plan.citation));
    box.appendChild(el("div", "dc-line", "lands at: " + plan.landsAt));
  } else {
    box.appendChild(el("div", "dc-h", "drafted: possibles-register entry (human commits)"));
    box.appendChild(el("div", "dc-line", "id: " + (plan.id || "(missing)")));
    box.appendChild(el("div", "dc-line", "title: " + (plan.title || "(missing)")));
    box.appendChild(el("div", "dc-line", "claim: " + (plan.claim || "(missing)")));
    box.appendChild(el("div", "dc-line", "state: " + plan.state));
    box.appendChild(el("div", "dc-line", "provenance doc: " + (plan.provenanceDoc || "(none)")));
    box.appendChild(el("div", "dc-line", "attached evidence pins: " + plan.evidenceCount));
    box.appendChild(el("div", "dc-line", "lands at: " + plan.landsAt));
  }
  box.appendChild(el("div", "dc-note",
    "Machinery drafted this under a declared output path (" + DRAFTS_DIR +
    "); NOTHING entered the register — a human reviews and commits."));
  container.appendChild(box);
}

// ---- view assembly ----
export function renderCanvas(root, snapshot, opts) {
  const options = opts || {};
  const notebook = options.notebook || null;
  root.innerHTML = "";
  const clusters = listCanvasClusters(snapshot);

  if (!clusters.length) {
    root.appendChild(el("div", "empty", "no clusters in the snapshot"));
    return;
  }

  // deterministic default: the first cluster (snapshot order), overridable by
  // the caller (app.js may pass a selected cluster id).
  let selected = options.clusterId && clusters.some((c) => c.id === options.clusterId)
    ? options.clusterId : clusters[0].id;

  const head = el("div", "canvas-head");
  const cname = el("span", "cname");
  head.appendChild(cname);
  head.appendChild(el("span", "pill stage", "cluster canvas · D12"));
  head.appendChild(el("span", "canvas-note",
    "Members are exactly this cluster's Topics: edges; downstream artifacts live in the lineage strip. " +
    "Every action assembles a draft a human commits — machinery enters nothing into the register."));
  // "Open in NotebookLM" for the selected cluster (v2 tile action) — rebuilt per
  // selection; empty (and absent from the DOM) when the capability probe said no.
  const nbHolder = el("span", "canvas-nb");
  head.appendChild(nbHolder);

  // cluster picker
  const picker = el("div", "canvas-picker");
  picker.setAttribute("role", "group");
  picker.setAttribute("aria-label", "Cluster");
  const buttons = new Map();
  for (const c of clusters) {
    const b = el("button", "cpick");
    b.type = "button";
    let gapNote = "";
    if (c.gapCount) gapNote = " · " + c.gapCount + " gap" + (c.gapCount === 1 ? "" : "s");
    b.textContent = c.name + " (" + c.memberCount + "d · " + c.possibleCount + "p" + gapNote + ")";
    b.addEventListener("click", () => select(c.id));
    picker.appendChild(b);
    buttons.set(c.id, b);
  }

  const scroller = el("div", "scroller");
  const canvas = el("div", "canvas");
  scroller.appendChild(canvas);

  const lineageStrip = el("div", "lineage-strip");
  const confirm = el("div", "canvas-confirm");
  confirm.setAttribute("aria-live", "polite");
  const status = el("div", "canvas-status");
  status.setAttribute("aria-live", "polite");

  root.appendChild(head);
  root.appendChild(picker);
  root.appendChild(scroller);
  root.appendChild(lineageStrip);
  root.appendChild(confirm);
  root.appendChild(status);

  const ctx = {
    snapshot,
    status,
    options,
    confirmSupersede: (plan) => renderConfirm(confirm, plan, "supersede"),
    confirmComposer: (plan) => renderConfirm(confirm, plan, "composer"),
  };

  function renderLineageStrip(model) {
    lineageStrip.innerHTML = "";
    const rows = [
      ["staged picks", model.lineage.staged_picks, "staged"],
      ["proposals", model.lineage.proposals, "proposal"],
      ["realized", model.lineage.realized, "realized"],
    ].filter(([, ids]) => ids?.length);
    lineageStrip.appendChild(el("div", "lk", "lineage strip — downstream of this cluster (never members)"));
    if (!rows.length) {
      lineageStrip.appendChild(el("span", "meta", "no downstream lineage yet"));
      return;
    }
    for (const [label, ids, chipClass] of rows) {
      const row = el("div", "lineage-row");
      row.appendChild(el("span", "lk", label));
      for (const id of ids) row.appendChild(el("span", "lchip " + chipClass, id));
      lineageStrip.appendChild(row);
    }
  }

  function select(clusterId) {
    selected = clusterId;
    const model = buildCanvasModel(snapshot, clusterId);
    for (const [id, b] of buttons) b.setAttribute("aria-pressed", String(id === clusterId));
    cname.textContent = model.cluster.name || model.cluster.id;
    nbHolder.textContent = "";  // clear (textContent, never innerHTML)
    if (notebook) {
      const btn = notebook.button("cluster", clusterId);
      if (btn) nbHolder.appendChild(btn);
    }
    canvas.innerHTML = "";
    canvas.appendChild(memberPane(model));
    canvas.appendChild(evidencePane(model));
    canvas.appendChild(possiblesRail(model, ctx));
    renderLineageStrip(model);
    confirm.innerHTML = "";
    status.textContent = "";
  }

  select(selected);
  return {
    redraw: () => select(selected),
    // PRESELECTION entry point (the wheel's clusters -> canvas jump,
    // 2026-07-25): the post-mount twin of `opts.clusterId`. An id the snapshot
    // does not carry is ignored — the surface keeps its current cluster rather
    // than blanking.
    select(clusterId) {
      if (buttons.has(clusterId)) select(clusterId);
    },
  };
}
