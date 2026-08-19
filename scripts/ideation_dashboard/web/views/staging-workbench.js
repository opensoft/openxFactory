// THE STAGING WORKBENCH foundation (openxFactory `add-staging-workbench`,
// design D4–D7; change tasks 4.2–4.6), now composing the doxBench authoring
// canvas. It is a full-screen view scoped to exactly ONE topic-bearing tile —
// a cluster, a possible, or a staged topic. The inherited docs/lens/outline
// context stays read-only; the adjacent Outline/Document canvas is browser-
// local editing until governed Save lands. It opens from the wheel's
// `open workbench` tile action (app.js threads `nav.openWorkbench` into
// wheel.js) and closes back to the wheel, which never went away underneath.
//
//   docs     the tile's document set from the PURE workbenchScope derivation
//            (staging-workbench-model.js) — one row per document, its
//            completeness bar and the five named signals with raw counts
//            rendered VERBATIM from the snapshot. A document the snapshot does
//            not score renders NO bar (design D7 — a zero bar would libel a
//            finished document as a stub). A possible's inherited
//            claiming-cluster members sit in their own labelled section,
//            never conflated with cited evidence.
//   lens     interconnectedness AT TILE SCOPE by RE-SCOPING the existing
//            keyword-lens derivation: the same `buildLensModel` the lens tab
//            uses, fed the scope's own documents and the snapshot's OWN
//            `keyword_index` seed filtered to the scope — no new analysis, no
//            new score, no new snapshot field, no snapshot re-read. The
//            match-count bullseye (the SHARED widget, bullseye.js — one renderer
//            in the bundle) draws that scoped model ABOVE the always-present flat
//            matrix, and the checked-keyword selection is SESSION state so a tab
//            switch never destroys it (add-workbench-bullseye-and-create D1–D4).
//   outline  the topic's outline material (a staged topic's primary fragment;
//            a possible's PICKED topic's fragment) rendered through the SAME
//            read-only `/source` pass-through the document viewer owns — this
//            module mounts viewer.js's renderViewer rather than fetching
//            anything itself, so the bundle keeps its fixed set of fetch call
//            sites and the degraded posture (no serve shim, 404 on the static
//            image) is EXACTLY the viewer's own inline message. A scope with
//            no outline gets an explicit empty state, never a fabricated one.
//            Above the rendering sits the TEMPLATED SECTION INDEX
//            (add-staged-topic-outline-template): the fragment's own headings and
//            `xspec:` fences, read by the pure outline-model.js, with a one-press
//            add for each required section the fragment lacks. An add writes into
//            the outline BUFFER and stops — the human's own Save carries it
//            through `edit-document`, so the tab gains no write verb.
//
// NO TRANSPORT IN THIS FILE (task 4.6, and pinned by test_staging_workbench.py):
// this module opens no route and carries no request of its own. The workbench's
// writes live in TWO sibling modules, both on the dispose.js / gate.js / lens.js
// injected-fetcher pattern:
//
//   swb-create.js   the human-only `create-document` gate verb
//                   (add-workbench-bullseye-and-create). Create-only: it brings a
//                   NEW document into existence and can never edit, delete, or
//                   overwrite anything.
//   swb-session.js  the BRANCH-SESSION verbs (007-workbench-branch-sessions
//                   T082): edit, save (`open-pr`), abandon. The notebook re-sync
//                   is DESCRIPTOR-ONLY in both gate postures (spec C10) — no
//                   route, no transport, no arithmetic on the bundle's call-site
//                   pin.
//
// No register entry, no `ideation-workbench` manifest (that is the OTHER
// workbench, the reference-set family of workbench.py; design D5 keeps the two
// senses apart), and no gate artifact beyond each verb's own gate-action record.
// With the gate capability absent every affordance — create and session alike —
// degrades to a copyable CLI descriptor and no write is reachable from the page.
// The doxBench Outline/Document canvas, its governed Save seam, and the chat
// rail (T055/T063: injected transports + the applyProposal seam into the live
// canvas controller) are all composed below.
//
// TWO THINGS CALLED A SESSION, kept apart (design D14). The BRANCH session is
// derived state on a git branch — its posture is derived in the transport-free
// model from the ACTIVE (repository, ref) key and the serving index's roster, and
// it is announced by its own indicator, distinct from the gate-capability pill.
// The WORKBENCH session (`lensSession` below) is the UI-lifetime checked-keyword
// selection and dies with the overlay.
//
// DOM-SAFETY: every dynamic value binds through textContent (the local el());
// innerHTML is only ever assigned a literal "" to clear. The one HTML-rendering
// surface inside the view is renderViewer's own vendored markdown-it, which
// escapes raw HTML by construction.

import {
  workbenchScope, doxbenchScopeProjection, lensScopeSnapshot, lensSessionSeed,
  toggleKeyword, createSeed, createOffered, rewritableDocuments, sessionPosture,
  sessionSurfaceHidden, presentationPosture,
  documentAbstract, docWheelEntries, existingOnTopic,
} from "./staging-workbench-model.js";
import { renderDocWheel } from "./doc-wheel.js";
import { buildLensModel } from "./lens-model.js";
import { renderBullseye } from "./bullseye.js";
import { mountCreateAffordance, openCreateDialog, createGateLive } from "./swb-create.js";
import {
  createdDocuments, documentCreated, endedSessions, mountSessionAffordances,
  openedSessions, sessionOpened,
} from "./swb-session.js";
import { primaryFragmentPath } from "./wheel-model.js";
import { insertSection, outlineModel } from "./outline-model.js";
import { renderViewer } from "./viewer.js";
import { mountDoxBenchCanvas } from "./doxbench-editor.js";
import { mountDoxBenchChatRail } from "./doxbench-chat.js";
import { clearDoxBenchSession } from "./doxbench-state.js";

// textContent-only element builder (lens.js / canvas.js discipline).
function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

function basename(path) {
  return String(path).split("/").at(-1) || String(path);
}

const TAB_DEFS = [
  { key: "docs", label: "docs" },
  { key: "lens", label: "lens" },
  { key: "outline", label: "outline" },
];

const KIND_LABELS = { cluster: "cluster", possible: "possible", staged: "staged topic" };

// A staging seed is always a STAGED topic in the TILE vocabulary — the key its
// save resolves a session through, and the key its create promotes it to once
// the tile exists. ONE spelling for both: the last time this vocabulary was
// applied in two places it diverged, the scope was dropped from the wire, and
// the create silently took its pre-session path (#152).
const DRAFT_TILE_KIND = "staged";

// The per-tab create labels (add-workbench-bullseye-and-create task 5.4–5.6).
// Each names what THAT tab's seeding actually produces, so the affordance never
// promises a document the seed does not describe.
const CREATE_LABELS = {
  docs: "＋ new document in this scope",
  lens: "＋ new document from the checked set",
  outline: "＋ new fragment in this topic",
};

// ---- the docs panel (task 4.3) ------------------------------------------------

// `docRow` and `completenessCell` lived here until 2026-08-03, rendering the
// flat list the wheel replaced. Both went with it rather than staying as dead
// code that draws a bar nobody can see. Their information did not go: the
// selected document's score AND its five signals are in the abstract above the
// wheel, and the score itself rides on every tile (see `docWheelEntries`), which
// is what the per-row bar was actually for. `docs.js` keeps its own unrelated
// `docRow` for the full-page documents view.

// THE ABSTRACT VIEW — the upper half of the split docs pane. Renders what the
// snapshot already derived for the selected document. textContent only.
function renderAbstract(host, doc) {
  host.innerHTML = "";
  const model = documentAbstract(doc);
  if (!model) {
    host.appendChild(el("div", "swb-empty",
      "select a document below to see what it declares"));
    return;
  }
  host.appendChild(el("div", "swb-abstracttitle", model.title));
  const meta = [model.stage, model.kind].filter(Boolean).join(" · ");
  if (meta) host.appendChild(el("div", "swb-abstractmeta", meta));
  if (model.note) {
    host.appendChild(el("div", "swb-empty", model.note));
    return;
  }
  if (model.summary) {
    const summary = el("div", "swb-abstractsummary", model.summary);
    summary.setAttribute("dir", "auto");
    host.appendChild(summary);
  }
  if (model.lands.length) {
    host.appendChild(el("div", "swb-abstractlabel", "feeds"));
    const lands = el("div", "swb-abstractlands");
    for (const entry of model.lands) {
      lands.appendChild(el("span", "swb-abstractchip", entry));
    }
    host.appendChild(lands);
  }
  if (model.topics.length) {
    host.appendChild(el("div", "swb-abstractlabel", "topics"));
    const topics = el("div", "swb-abstracttopics");
    for (const topic of model.topics) {
      topics.appendChild(el("span", "swb-abstractchip", topic));
    }
    host.appendChild(topics);
  }
  if (model.signals.length) {
    // The score alone explains nothing; the signals say WHICH part is thin.
    host.appendChild(el("div", "swb-abstractlabel",
      model.score === null ? "signals"
        : "signals · score " + model.score));
    const signals = el("div", "swb-abstractsignals");
    for (const signal of model.signals) {
      signals.appendChild(el("span", "swb-abstractchip",
        signal.name + " " + signal.count));
    }
    host.appendChild(signals);
  }
}

// `onBind` WAS the selection half of Phase A's model: choosing a document on the
// wheel bound the canvas's single document buffer — and therefore the chat — to
// that path, through the canvas's own `selectDocument`.
//
// add-doxbench-editing-phase-b RE-CUT that, and the adversarial review of PR #207
// is what surfaced why it had to. The ratified delta names exactly THREE selection
// routes — "the context region's `outline` selection tab SHALL select the
// `outline` buffer, LOADING A DOCUMENT SHALL SELECT THAT DOCUMENT, and the chat
// rail's loaded-document selector SHALL select among the loaded documents" — and a
// docs-row selection is not one of them. Keeping it was not merely redundant, it
// made the ratified loaded set UNREACHABLE: a tile click switched the single
// reserved slot to that path FIRST, so the LOAD that followed always found the
// document "already loaded" and the set could never hold two. The 24-document
// bound, the selector's multi-entry listing and the `A second document is loaded`
// scenario were all dead ends behind it — measured, not reasoned.
//
// So a wheel selection now moves the ABSTRACT above it and nothing else, which is
// the other half of the annotation that asked for the wheel in the first place
// ("for the top half when a doc is selected on the wheel, we load a viewer of
// that doc"), and the tile's own LOAD verb is the binding route.
// `verbs` (add-doxbench-editing-phase-b, Q3 ruled) carries the tile's two NEW
// verbs plus the live buffer state its marking is derived from. Injected exactly
// like every other seam on this surface, and OPTIONAL: without it the tile keeps
// its read verb and states the absence of the other two rather than failing on
// activation, which is the delta's own rule for a surface where editing is
// unreachable.
//
//   verbs.load(path)            -> Promise<{ok, error?}>
//   verbs.save(path)            -> Promise<{ok, error?}>
//   verbs.bufferStateFor(path)  -> {loaded, dirty, owned} | null   (LIVE, never cached)
function renderDocsPanel(pane, scope, onOpen, create, verbs) {
  // The wheel owns a RAF loop and a ResizeObserver, so the OUTGOING one has to
  // be torn down before its host DOM is discarded — a re-render on every scope
  // change would otherwise leak one animation loop per render, each observing
  // a detached node.
  pane.__docWheel?.destroy?.();
  pane.__docWheel = null;
  pane.innerHTML = "";
  // the pane's ACTIONS ROW (task 5.4): the create affordance seeded from the
  // tile — topics from the scope's keywords, area from the scope, the source
  // citation naming the scope by kind and id. Live button with the gate
  // capability; a copyable CLI descriptor without it.
  if (create) {
    const actions = el("div", "swb-actions");
    pane.appendChild(actions);
    create.mount(actions, "docs");
  }

  // THE VERTICAL SPLIT (operator annotation vibe_1785602331813_gvku9sh2s):
  // the selected document's abstract ABOVE, the selector BELOW.
  const split = el("div", "swb-docsplit");
  const abstract = el("div", "swb-docabstract");
  abstract.setAttribute("role", "region");
  abstract.setAttribute("aria-label", "selected document");
  // THE LOWER HALF IS THE WHEEL (the annotation's second half, delivered
  // 2026-08-03): "the same wheel of the docs we have used before" at 0.4 of
  // this subpane's radius. It is the deck's own drum — same projection, same
  // locked click gesture, same visibility predicate — over this scope's
  // documents flattened into one reel. Selecting a tile loads that document's
  // abstract ABOVE, which is the other half of the same annotation.
  const selector = el("div", "swb-docselector");
  split.append(abstract, selector);
  pane.appendChild(split);
  // WHERE A TILE VERB'S OUTCOME LANDS. A load refused at the loaded-set bound
  // and a save the governed pipeline declined are both facts the human must be
  // able to read; a control that swallowed them would be a control that lies
  // about whether their work is saved. Announced as well as shown.
  const note = el("div", "swb-docverbnote");
  note.setAttribute("aria-live", "polite");
  note.hidden = true;
  pane.appendChild(note);

  // A drum is one reel, so the sections flatten — carrying their labels onto
  // the tiles rather than losing them (see `docWheelEntries`).
  const entries = docWheelEntries(scope);
  let seeded = false;
  // PR #196 review F4: while the wheel is being RECONCILED to the document the
  // canvas actually holds, its own onSelect must not turn round and ask for
  // that document again — the reconcile is the canvas answering, not a human
  // choosing.
  let reconciling = false;
  const wheel = renderDocWheel(selector, entries, {
    onSelect: (entry) => {
      // The abstract above, and NOTHING else: a selection is not a binding route
      // under Phase B (see the note above this function). `seeded` and
      // `reconciling` survive because the reconcile below still drives this
      // callback, and neither a mount-time seed nor the canvas answering is a
      // human choosing anything.
      renderAbstract(abstract, entry ? entry.row.doc : null);
      if (!seeded) { seeded = true; return; }
      if (reconciling) return;
    },
    // SELECT and READ stay distinct verbs, as they were in the flat list:
    // selecting must not steal the read-only viewer, and reading (from the
    // expanded tile) must not be the only way to look at a document.
    onRead: onOpen ? (row) => onOpen(row) : null,
    // LOAD FOR EDITING — the ONE route into the loaded set (design D5). The
    // outcome is surfaced on the pane itself: a refusal (the loaded-set bound,
    // an out-of-scope path, a failed source read) must be VISIBLE, never a
    // click that appears to do nothing.
    onLoad: verbs && typeof verbs.load === "function"
      ? async (row) => {
          const outcome = await verbs.load(row.path);
          renderTileVerbNote(note, outcome, "load");
          wheel.refreshBufferState();
        }
      : null,
    // SAVE — the same governed pipeline the canvas Save reaches, scoped to this
    // document plus the outline-ancestry step (design D4). A second entry point
    // to one mechanism.
    onSave: verbs && typeof verbs.save === "function"
      ? async (row) => {
          const outcome = await verbs.save(row.path);
          renderTileVerbNote(note, outcome, "save");
          wheel.refreshBufferState();
        }
      : null,
    bufferStateFor: verbs && typeof verbs.bufferStateFor === "function"
      ? (path) => verbs.bufferStateFor(path)
      : null,
  });
  pane.__docWheel = wheel;
  // The pane's own refresh hook, so the shell can say "a buffer moved" without
  // knowing anything about the wheel.
  pane.__docWheelRefresh = () => wheel.refreshBufferState();

  // An empty scope has no tile to select, so nothing seeded the abstract: say
  // so explicitly rather than leaving the upper half blank.
  if (!entries.length) renderAbstract(abstract, null);

  // PR #196 review F4: the wheel is a SELECTION control over the same choice
  // the canvas's own picker makes, and the picker already reverts to the
  // document really loaded whenever a selection does not land (blocked by the
  // unsaved-edit guard, refused as out of scope, refused because the load
  // failed). The wheel had no such reconciliation and `selectPath` — written
  // for exactly this — had no caller at all, so the two controls and the
  // canvas could sit on three different documents at once. Returned to the
  // shell rather than reached for: this panel still knows nothing about the
  // canvas.
  return (path) => {
    if (path == null) return;
    reconciling = true;
    try { wheel.selectPath(path); } finally { reconciling = false; }
  };
}

// One tile verb's outcome, stated. FIXED phrasing per class, with the seam's own
// reason appended when it supplies one — the seam's reasons are this surface's
// own sentences (a measured bound, a governed refusal), never provider or
// document text.
function renderTileVerbNote(note, outcome, verb) {
  if (!note) return;
  const ok = Boolean(outcome && outcome.ok);
  const reason = outcome && typeof outcome.error === "string" ? outcome.error : "";
  if (ok) {
    note.textContent = verb === "save"
      ? "saved through the governed Save"
      : "loaded for editing — the chat and the canvas are on it now";
  } else {
    note.textContent = (verb === "save"
      ? "the governed Save did not land"
      : "this document was not loaded")
      + (reason ? " — " + reason : "");
  }
  note.hidden = false;
}

// WHICH lens section is showing. Module-scope like the lens session itself:
// the panel is re-rendered on every keyword toggle, and a human who opened the
// matrix should not be thrown back to the keyword rail by their own click.
let lensSection = "keywords";

// ---- the lens panel (task 4.4) ------------------------------------------------
//
// A CHECKBOX rail over the scope's keywords, the MATCH-COUNT BULLSEYE, and the
// always-present flat matrix — the SAME membership derivation the lens tab
// renders (lens-model.js's buildLensModel) drawn by the SAME widget
// (bullseye.js), bounded to the tile so the human is not thrown out of their
// scope. Checking/unchecking re-runs the derivation over the SAME scoped
// projection; nothing new is analysed and nothing is read from the network.
//
// The checked set is the SHELL's session state (`session.checked`, design D4):
// this panel never reseeds it, which is what lets `lens -> docs -> lens` return
// to the selection the human left — and that selection is also the `Topics:`
// seed for a create from this tab.

function renderLensPanel(pane, snapshot, scope, session, create) {
  const scoped = lensScopeSnapshot(snapshot, scope);

  function draw() {
    pane.innerHTML = "";
    const model = buildLensModel(scoped, { checked: [...session.checked] });
    pane.appendChild(el("div", "swb-lensnote",
      "the keyword lens RE-SCOPED to this tile: " + scoped.documents.length +
      " document" + (scoped.documents.length === 1 ? "" : "s") +
      " · keyword counts are the snapshot's corpus-wide declared counts, verbatim"));

    const rail = el("div", "swb-lensrail");
    // (appended into its subtab pane below, not onto the panel)
    for (const kw of model.rail) {
      const chip = el("label", "swb-kw");
      const box = document.createElement("input");
      box.type = "checkbox";
      box.checked = kw.checked;
      box.setAttribute("aria-label", "check " + kw.keyword + " (stratify within this scope)");
      box.addEventListener("change", () => {
        session.checked = toggleKeyword(session.checked, kw.keyword);
        draw();
      });
      chip.appendChild(box);
      // the number the SHARED bullseye labels this keyword's sectors with —
      // the rail is that widget's legend here exactly as it is in the lens tab
      const tag = el("span", "swb-kwnum", kw.label);
      if (kw.hue != null) tag.style.setProperty("--h", String(kw.hue));
      chip.appendChild(tag);
      chip.appendChild(el("span", "swb-kwname", kw.keyword));
      chip.appendChild(el("span", "swb-kwcount", String(kw.declaredCount)));
      rail.appendChild(chip);
    }
    if (!model.rail.length) {
      rail.appendChild(el("div", "swb-empty",
        "this scope touches no declared keywords"));
    }
    pane.appendChild(rail);

    // the FORMING row (task 5.5): what the checked set currently forms, plus the
    // labelled create affordance. The bullseye's centre ring opens the SAME
    // dialog into the SAME slot with the SAME seed, so the fast gesture and the
    // discoverable, keyboard-reachable button can never diverge (design D6).
    const forming = el("div", "swb-forming");
    forming.appendChild(el("span", "swb-formingline",
      model.checked.length
        ? "forming: " + model.matched.length + " of " + scoped.documents.length +
          " scoped document" + (scoped.documents.length === 1 ? "" : "s") +
          " match all " + model.checked.length + " checked (" +
          model.checked.join(" ✓ ") + " ✓)"
        : "forming: nothing yet — check a keyword to stratify this scope"));
    const dialog = el("div", "swb-cslot");
    // the LIVE checked set is the lens tab's `Topics:` seed and its `Source:`
    // recipe citation (design D7) — read at draw time, so it is always the set
    // the human is looking at
    const live = { slot: dialog, checked: [...session.checked] };
    if (create) create.mount(forming, "lens", live);
    pane.appendChild(forming);

    // THE LENS IN THREE SUBTABS (operator annotation
    // vibe_1785602062606_397p8iakz: "restructure this so that the 3 sections
    // of the lens widget are in 3 subtabs"). The three sections are the
    // keyword rail, the bullseye, and the flat matrix — previously stacked in
    // one long scroll inside a third of the panel.
    //
    // The NOTE and the FORMING LINE stay outside them: they state what the
    // checked keywords currently select, which the bullseye and matrix are
    // both unreadable without. A status line hidden behind a tab is a status
    // line nobody reads.
    //
    // Full APG tablist, matching the context strip above it — roving
    // tabindex, arrows, Home/End. CHK007 failed on this surface once for
    // exactly the semantics-without-keyboard gap; a new strip does not get to
    // repeat it.
    const subtabs = el("div", "swb-subtabs");
    subtabs.setAttribute("role", "tablist");
    subtabs.setAttribute("aria-label", "lens sections");
    const subpanes = el("div", "swb-subtabpanes");
    const SECTIONS = [
      { key: "keywords", label: "keywords" },
      { key: "bullseye", label: "bullseye" },
      { key: "matrix", label: "matrix" },
    ];
    const subButtons = new Map();
    const subPanes = new Map();
    for (const { key, label } of SECTIONS) {
      const btn = el("button", "swb-subtab", label);
      btn.type = "button";
      btn.setAttribute("role", "tab");
      btn.addEventListener("click", () => showSection(key));
      subtabs.appendChild(btn);
      subButtons.set(key, btn);
      const host = el("div", "swb-subtabpane");
      host.setAttribute("role", "tabpanel");
      host.setAttribute("aria-label", label);
      subpanes.appendChild(host);
      subPanes.set(key, host);
    }
    function showSection(key) {
      lensSection = key;
      for (const [name, btn] of subButtons) {
        const on = name === key;
        btn.setAttribute("aria-selected", String(on));
        btn.tabIndex = on ? 0 : -1;
        btn.classList.toggle("swb-subtab-active", on);
        subPanes.get(name).hidden = !on;
      }
    }
    subtabs.addEventListener("keydown", (ev) => {
      const order = SECTIONS.map((s) => s.key);
      const at = order.indexOf(lensSection);
      let next = null;
      if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = order[(at + 1) % order.length];
      else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = order[(at - 1 + order.length) % order.length];
      else if (ev.key === "Home") next = order[0];
      else if (ev.key === "End") next = order[order.length - 1];
      if (!next) return;
      ev.preventDefault();
      showSection(next);
      subButtons.get(next).focus();
    });
    pane.append(subtabs, subpanes);
    subPanes.get("keywords").appendChild(rail);
    pane.appendChild(dialog);

    // the SHARED bullseye widget, ABOVE the always-present matrix (design
    // D1/D3). EVERY region is an activatable create gesture — the matches-ALL
    // centre AND each ring sector (Brett's 2026-07-25 ruling on open question
    // 2) — ONLY when the create affordance is offered at all. A sector seeds
    // `Topics:` from its OWN matched combination; the centre seeds the whole
    // checked set, exactly like the labelled button above.
    subPanes.get("bullseye").appendChild(renderBullseye(model, create ? {
      centreLabel: "create a document from the " + model.checked.length +
        " checked keyword" + (model.checked.length === 1 ? "" : "s"),
      onActivate: (region) => create.open(dialog, "lens",
        region && region.kind === "sector"
          ? { ...live, subset: [...region.keywords] }
          : live),
    } : null));

    // the flat matrix — the same membership as the bullseye above it, at tile
    // scope (docs matching >= 1 checked keyword, ring = match count). ALWAYS
    // rendered: it is the readable view of the SVG, never a toggle-only alternate.
    const table = el("table", "lensmatrix swb-matrix");
    table.setAttribute("aria-label",
      "keyword membership matrix, scoped to this tile");
    const head = el("tr");
    // "#" indexes the bullseye above: dot #N is this table's row N
    head.appendChild(el("th", null, "#"));
    head.appendChild(el("th", null, "doc"));
    for (const k of model.checked) {
      const tag = model.keywordLabels ? model.keywordLabels[k] : null;
      head.appendChild(el("th", null, tag ? tag + " " + k : k));
    }
    head.appendChild(el("th", null, "ring"));
    table.appendChild(head);
    for (const r of model.matrix) {
      const tr = el("tr");
      tr.appendChild(el("td", "docnum", String(r.number)));
      tr.appendChild(el("td", null, basename(r.document)));
      for (const cell of r.cells) tr.appendChild(el("td", null, cell.present ? "✓" : "·"));
      tr.appendChild(el("td", null, r.ring));
      table.appendChild(tr);
    }
    if (!model.matrix.length) {
      const tr = el("tr");
      const td = el("td", "swb-empty", model.checked.length
        ? "no scoped documents match the checked keywords"
        : "check a keyword to stratify this scope");
      td.setAttribute("colspan", String(model.checked.length + 3));
      tr.appendChild(td);
      table.appendChild(tr);
    }
    subPanes.get("matrix").appendChild(table);
    showSection(lensSection);
  }

  draw();
}

// ---- the outline panel (task 4.5) ---------------------------------------------

function outlineEmpty(pane, message) {
  pane.appendChild(el("div", "swb-empty swb-outline-empty", message));
}

// ---- the templated section index + the add-section affordance -----------------
//      (add-staged-topic-outline-template tasks 3.2-3.4)
//
// WHAT THE INDEX SAYS, and what it deliberately does not. The section model
// (outline-model.js) reads the fragment's OWN `## ` headings and `xspec:` fences,
// fence-aware, so a fragment that merely QUOTES the canonical skeleton is not
// reported as having adopted it. Everything below is presentation over that one
// verdict: no second scanner, no content-sniffing, and no heading the file does
// not carry.
//
// NON-CONFORMANCE IS NOT AN ERROR STATE (task 3.3). Conformance is REQUIRED
// only for topics staged after the template ratified and OPT-IN for the 30-odd
// that came before, so most fragments in the corpus carry none of it. A
// pre-template fragment renders its real sections and one calm sentence saying
// the shape is earned when the topic is next worked -- never a warning, never a
// count of failures, and never a rewrite as a side effect of opening the tab.

// One line per state, and each one is about the TOPIC's stage of migration
// rather than about a fault in the file.
function outlineStateLine(model) {
  if (model.state === "conforming") {
    return "conforming — the three required sections are present and every open "
      + "question carries its four sub-fields";
  }
  if (model.state === "pre-template") {
    return "staged before the outline template — it carries none of the required "
      + "sections yet, which is the opt-in posture, not a fault. The shape is "
      + "earned when the topic is next worked, never by opening it here.";
  }
  return "partly templated — the sections below are what the fragment carries; "
    + "the rest are still to be written when the topic is next worked";
}

const OUTLINE_ROLE_LABELS = {
  required: "required", added: "added", "proposal-element": "proposal element",
};

// The provenance line stamped on a section this affordance adds. UTC, because
// the date is a governance record on the document rather than a clock reading
// for the reader — a local-time stamp would make the same act carry two
// different dates depending on who performed it.
function provenanceDate() {
  return new Date().toISOString().slice(0, 10);
}

// THE REFUSAL VOCABULARY, mapped from the seam's CODE and never from its text.
//
// W-10's lesson, and both other consumers of `applyProposal` already forbid the
// shortcut: doxbench-chat.js calls its mapping a WHITELIST and drops the seam's
// error text unread, and the canvas states the codes "remain the canvas's and are
// never echoed". Echoing them here reached a human with "this proposal no longer
// matches the buffer" — a noun this tab never uses — and with a settling-window
// sentence carrying no recovery, which is exactly the collapse W-10 undid. Each
// sentence below names its own recovery, in the tab's own voice.
const ADD_SECTION_UNSETTLED =
  "the outline buffer's identity is still settling — press add again in a moment";
const ADD_SECTION_STALE =
  "the outline buffer moved while this section was being composed — press add "
  + "again to compose it against the current text";
const ADD_SECTION_UNAVAILABLE =
  "the outline buffer is not available for editing on this console — nothing "
  + "was written";
const ADD_SECTION_REFUSED =
  "the insertion was refused and nothing was written — press add again";

function addSectionRefusal(outcome) {
  const code = outcome && typeof outcome.code === "string" ? outcome.code : null;
  if (code === "unsettled") return ADD_SECTION_UNSETTLED;
  if (code === "stale") return ADD_SECTION_STALE;
  if (code === "unavailable") return ADD_SECTION_UNAVAILABLE;
  return ADD_SECTION_REFUSED;
}

// One add, end to end: the insert is computed against what the OUTLINE BUFFER
// holds (never against the stored bytes rendered below it, which is exactly the
// human's unsaved work behind), and it lands through the canvas's own
// `applyProposal` — the settled-identity gate, the line-ending re-flavor and the
// same `edit()` a keystroke goes through. This function performs NO write of its
// own, opens no route, and calls no gate action.
//
// `required` marks the GAP-ROW route, where the caller asks by the contract's own
// label and the section lands under its canonical heading and seed. The free-form
// route leaves it false and gets the human's heading verbatim.
async function runAddSection(seam, path, note, title, after, required) {
  note.hidden = false;
  const live = seam.buffer();
  if (!live) {
    note.textContent = "the outline buffer is not loaded yet — nothing was written";
    return null;
  }
  // The buffer and this panel resolve the fragment through the SAME
  // `primaryFragmentPath` rule, so a disagreement is a defect rather than a
  // situation to paper over: refused, said out loud, and nothing written.
  if (live.path !== path) {
    note.textContent = "the canvas is holding a different outline (" + live.path
      + ") — nothing was written";
    return null;
  }
  const patch = insertSection(live.text, {
    title, after, required, addedBy: seam.actor, date: provenanceDate(),
  });
  if (!patch.ok) {
    // The MODEL's reasons are this tab's own sentences (it is our pure module,
    // written for this surface), so they are stated verbatim. The SEAM's are not,
    // which is why the branch below maps a code instead.
    note.textContent = patch.reason;
    return null;
  }
  const outcome = await seam.apply(live.baseHash, patch.text);
  if (!outcome || outcome.ok !== true) {
    note.textContent = addSectionRefusal(outcome);
    return null;
  }
  const where = patch.mode === "end"
    ? "at the end of the outline"
    : patch.mode + ' "' + patch.target + '"';
  // WHAT HAPPENED AND WHAT DID NOT, in one sentence: the text is in the buffer,
  // it is unsaved, and the human's existing Save is what commits it. This
  // affordance is not a write and must never read like one. The heading NAMED is
  // the one written, not the one asked for — a required section lands under its
  // canonical skeleton heading.
  note.textContent = 'added "' + patch.heading + '" to the outline buffer ' + where
    + " with Added-by provenance — unsaved: the canvas Save carries it through "
    + "edit-document on the session branch";
  return outcome;
}

// The add controls. `seam` null means editing is not live on this plane, and
// then every control renders DISABLED WITH NO LISTENER BOUND (task 3.4): the
// affordance still says what it would be, because a surface that hides its own
// authority teaches the reader nothing, but there is no write path to reach —
// the same posture viewer.js's "open in editor" button and the docs tile's
// load/save verbs already take where the capability is absent.
function mountAddSection(host, model, path, seam) {
  const note = el("div", "swb-outlinenote");
  note.setAttribute("aria-live", "polite");
  note.hidden = true;
  const absent = "adding a section needs the local human console's editing "
    + "capability — this plane has none, so no write path is offered";

  // `intent()` is read at CLICK time, never closed over at build time: the
  // free-form control's two values are whatever the human has typed and chosen
  // by then.
  function addControl(label, cls, intent) {
    const btn = el("button", "swb-cbtn swb-outlineadd " + cls, label);
    btn.type = "button";
    if (!seam) {
      // NO LISTENER IS BOUND. Disabled alone would still leave a write path on
      // the page for anything that re-enabled the node; there is nothing here to
      // reach.
      btn.disabled = true;
      btn.title = absent;
      return btn;
    }
    btn.title = "insert the section skeleton into the outline buffer — your Save "
      + "commits it through edit-document";
    btn.addEventListener("click", async () => {
      btn.disabled = true;
      try {
        const asked = intent();
        await runAddSection(seam, path, note, asked.title, asked.after,
                            asked.required === true);
      } finally {
        btn.disabled = false;
      }
    });
    return btn;
  }

  // The MISSING required sections, each its own one-press add scoped to its
  // canonical place. The template's own order decides where it lands, so an add
  // never moves what a human already wrote.
  for (const gap of model.gaps) {
    if (gap.kind !== "missing-section") continue;
    const row = el("div", "swb-outlinegap");
    row.appendChild(el("span", "swb-outlinegaplabel",
      "no " + gap.label + " section"));
    // `required` is the load-bearing flag: the button asks by the contract's
    // LABEL, so the model may resolve it loosely to the canonical heading and
    // seed. Nothing else in the tab is allowed that latitude.
    const asked = { title: gap.label, after: null, required: true };
    row.appendChild(addControl("add it", "swb-outlineaddgap", () => asked));
    host.appendChild(row);
  }
  // …and the questions the contract says are incomplete. STATED ONLY: the
  // affordance adds SECTIONS, and filling a sub-field is the human's sentence to
  // write, not a slot for this surface to stuff.
  for (const gap of model.gaps) {
    if (gap.kind !== "incomplete-question") continue;
    host.appendChild(el("div", "swb-outlinegap",
      gap.label + " — still to carry " + gap.missing.join(", ")));
  }

  // The free-form add, scoped EXPLICITLY: the human names the section and the
  // one it goes behind, and that target is the patch's addressing key.
  const form = el("div", "swb-cfield swb-outlineform");
  const titleLabel = el("label", "swb-clabel", "add a section");
  const titleInput = el("input", "swb-outlinetitle");
  titleInput.type = "text";
  titleInput.setAttribute("placeholder", "section heading");
  // Named for assistive navigation. The visible `label` beside it carries no
  // `for`/`id` pair, and a placeholder is not an accessible name — it disappears
  // the moment the human types.
  titleInput.setAttribute("aria-label", "heading of the section to add");
  titleInput.disabled = !seam;
  const afterLabel = el("label", "swb-clabel", "after");
  const afterSelect = el("select", "swb-outlineafter");
  afterSelect.setAttribute("aria-label",
    "the section the new one is added after — the patch's addressing key");
  afterSelect.disabled = !seam;
  const endOption = el("option", null, "(the end of the outline)");
  endOption.value = "";
  afterSelect.appendChild(endOption);
  for (const section of model.sections) {
    const option = el("option", null, section.title);
    option.value = section.title;
    afterSelect.appendChild(option);
  }
  form.append(titleLabel, titleInput, afterLabel, afterSelect,
    addControl("add", "swb-outlineaddfree", () => ({
      title: String(titleInput.value || "").trim(),
      after: afterSelect.value || null,
    })));
  host.appendChild(form);
  if (!seam) host.appendChild(el("div", "swb-lensnote", absent));
  host.appendChild(note);
}

// The whole index, rendered from the loaded text the viewer handed back.
function renderOutlineIndex(host, text, path, seam) {
  host.innerHTML = "";
  const model = outlineModel(text);
  // "AS STORED" is not decoration. This index describes the SAVED fragment while
  // the canvas beside it holds unsaved work, so after an add a gap row here still
  // reports a section the buffer already has — and without the label that reads as
  // the page contradicting itself rather than as the two honest answers the
  // deliberate two-renderings split gives (see `renderOutlinePanel`).
  const header = el("div", "swb-abstractlabel", "outline template — as stored");
  header.title = "the sections in the SAVED fragment; the canvas beside this "
    + "holds your unsaved edits, so the two differ by exactly that much";
  host.appendChild(header);
  host.appendChild(el("div", "swb-lensnote swb-outlinestate", outlineStateLine(model)));
  if (!model.sections.length) {
    host.appendChild(el("div", "swb-empty",
      "this fragment carries no `## ` sections outside its code fences"));
  }
  for (const section of model.sections) {
    const row = el("div", "swb-outlinerow");
    row.appendChild(el("span", "swb-outlinetitleline", section.title));
    row.appendChild(el("span", "swb-abstractchip",
      OUTLINE_ROLE_LABELS[section.role] || section.role));
    row.appendChild(el("span", "swb-outlineline", "line " + section.line));
    if (section.addedBy) {
      row.appendChild(el("span", "swb-outlineprov", "Added-by: " + section.addedBy));
    }
    host.appendChild(row);
  }
  mountAddSection(host, model, path, seam);
}

// `sourceBase` is the ACTIVE (repository, ref)'s own keyed `/source/` base
// (PR #49 review finding 16). Without it `renderViewer` fell back to the unkeyed
// `/source/`, which the server resolves to the ACTIVE REGISTRY ENTRY — and the
// active entry is deliberately kept on `main` for a session's whole life
// (FR-014a). So the outline of a DRAFT view rendered `main`'s bytes, or 404'd
// for a document the session had just created, while the docs row beside it —
// which app.js keys correctly — showed the session's own. US2 acceptance
// scenario 5 and FR-010 both name the outline explicitly, and spec §US2 calls
// this exact failure "specifically dangerous — a draft view mistaken for main".
//
// `sections` (add-staged-topic-outline-template task 3.2) is the ADD-SECTION
// seam, or null where editing is not live on this plane. It is the shell's
// narrow window onto the outline buffer — read the live text and its settled
// identity, hand back the whole next text — and nothing more: no transport, no
// gate action, and no second state authority over the buffer.
function renderOutlinePanel(pane, snapshot, scope, create, sourceBase, edit, sections) {
  pane.innerHTML = "";
  // task 5.6: "new fragment in this topic" — offered for STAGED scopes only and
  // HIDDEN (never disabled) for a cluster or a possible, which have no staging
  // topic folder to write a fragment into. `createOffered` owns that rule.
  if (create && create.offered("outline")) {
    const actions = el("div", "swb-actions");
    pane.appendChild(actions);
    create.mount(actions, "outline");
  }
  if (!scope.outline) {
    outlineEmpty(pane, scope.kind === "possible"
      ? "this possible has no outline yet — it has not been picked into a staging topic"
      : "this scope carries no outline material — outlines belong to staged topics");
    return;
  }
  // the SAME deterministic fragment selection the staged wheel's read verb and
  // 3-line summary use (wheel-model.js) — never a second path rule
  const path = primaryFragmentPath(scope.outline.stagingId, scope.outline.files);
  if (!path) {
    outlineEmpty(pane, "the topic folder carries no markdown fragment to outline");
    return;
  }
  if (scope.outline.from === "picked-topic") {
    pane.appendChild(el("div", "swb-lensnote",
      "outline of the PICKED staging topic " + scope.outline.stagingId +
      " (the pick is recorded register data)"));
  }
  // THE TEMPLATED SECTION INDEX, above the rendered fragment. It is built from
  // the bytes the viewer loads and hands back (`onText`), so it needs no fetch of
  // its own and cannot describe a fragment that never arrived: on a failed or
  // degraded load this host stays empty and the viewer's own message stands
  // alone.
  const index = el("div", "swb-outlineindex");
  pane.appendChild(index);
  const host = el("div", "swb-outline");
  pane.appendChild(host);
  // read-only, through the viewer's own /source pass-through: renderViewer owns
  // the fetch, the divergence banner, and the degraded no-shim / 404 message —
  // exactly the document viewer's posture, because it IS the document viewer.
  //
  // TWO RENDERINGS OF "THE OUTLINE" SURVIVE ON PURPOSE (Phase A): this one says
  // what is STORED in the source, and the canvas on the right says what the
  // human HAS unsaved. Collapsing them would answer one question and lose the
  // other, so focusing this selection tab makes the outline the active buffer
  // over there without changing what is rendered here.
  const doc = (snapshot.documents || []).find((d) => d.path === path) || null;
  renderViewer(host, { path, doc, sourceBase, edit,
    onText: (text) => renderOutlineIndex(index, text, path, sections) });
}

// ---- the full-screen shell (task 4.2) ------------------------------------------

// Mounts the one staging-workbench overlay into `container` (called once, from
// app.js — the explorer pattern). `onOpenDoc(path, doc)`, when supplied, lets a
// docs row jump into the read-only source viewer overlay — and is also where a
// freshly created document lands (task 5.8). `caps` is app.js's ONE capability
// verdict: it decides the posture pill (task 5.9) and whether the create
// affordances are live buttons or copyable CLI descriptors (task 5.7). `fetcher`
// is the injectable transport seam swb-create.js and swb-session.js take.
//
// `active` and `index` (007-workbench-branch-sessions T082) are the two READ-ONLY
// inputs the BRANCH-SESSION posture is derived from: the ACTIVE (repository, ref)
// key the shell fetched its snapshot with, and the serving index's roster, where a
// live session is an ordinary (repository, ref) row (FR-014). Neither is a
// transport, and both are things app.js already holds — the workbench derives the
// posture rather than asking the server a second question (FR-045).
//
// `onSessionRekey(ref)` (T092 acceptance sweep, defect 5) is the SHELL's answer to
// "the create just opened a session — re-key to it". The overlay carries no
// transport, so app.js owns the fetch; the create awaits it, and only after the
// session snapshot loads do source reads and edit writes adopt the new key
// together. `onSessionEnded()` resets those bindings to the surviving main
// checkout when an abandon or already-merged save retires the branch entry.
//
// Returns `{ open(kind, id), close() }`; `open` is what the wheel's tile action
// reaches through `nav.openWorkbench`.
export function mountStagingWorkbench(container, snapshot,
                                      { onOpenDoc, caps, fetcher, active, index,
                                        // T023 (010-doxbench-editor-chat, partial slice): the
                                        // loadSource + hash seam bundle app.js builds
                                        // (createDoxBenchSourceLoader + the shared
                                        // contentIdentity), forwarded verbatim into the
                                        // doxBench canvas mount below (drawCanvas). This file
                                        // creates no transport of its own -- it only forwards
                                        // what it is handed.
                                        doxbench,
                                        // The UNSTRIPPED capability, used by
                                        // `openDraft` ALONE. Every tile-bound
                                        // surface keeps `caps` — on a composed
                                        // view those verbs genuinely have no
                                        // checkout to bind to. A new document
                                        // binds to no tile.
                                        createCaps,
                                        // The shell's ONE console-token
                                        // re-read (app.js
                                        // `createConsoleRepair`), forwarded
                                        // verbatim to the two write
                                        // transports. This overlay never
                                        // calls it — it carries no transport
                                        // and holds no capability of its own.
                                        consoleRepair,
                                        // the caller's render scope: this
                                        // overlay binds a document listener
                                        signal,
                                        sourceBase, edit, onSessionRekey,
                                        onSessionEnded, onScopeOpened } = {}) {
  // The wheel behind this overlay stays on the shell snapshot while a create
  // may temporarily adopt a branch snapshot inside the workbench. Reopening
  // from that wheel must therefore start from the shell state again; otherwise
  // the retained branch projection can be rendered with a newly reset main key.
  let shellSnapshot = snapshot;
  let shellActive = active;
  let shellIndex = index;
  let shellSourceBase = sourceBase;
  container.innerHTML = "";
  const overlay = el("div", "swb-overlay");
  overlay.hidden = true;
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");

  const panel = el("div", "swb-panel");
  const head = el("div", "swb-head");
  const titles = el("div", "swb-titles");
  const title = el("span", "swb-title");
  title.id = "swb-title";
  overlay.setAttribute("aria-labelledby", title.id);
  const subtitle = el("div", "swb-subtitle");
  titles.append(title, subtitle);
  // THE PILL (task 5.9 / design D9): capability-derived posture, never a
  // constant. With the gate off it reads exactly what the hosted image has
  // always shown; with the gate on it states the ONE write it can perform and
  // the actor who would perform it — a surface that misdescribes its own
  // authority is worse than one with no pill.
  const gateOn = createGateLive(caps);
  const readonly = el("span", "pill " + (gateOn ? "stage" : "neutral"),
    gateOn ? "gate: create-document" : "read-only");
  readonly.title = gateOn
    ? "doxBench's ONE write is the human-only create-document gate verb " +
      "(create-only, recorded; actor: " + ((caps && caps.actor) || "local") +
      ") — it never edits or deletes an existing document"
    : "doxBench writes nothing here — every create affordance is a " +
      "copyable CLI descriptor on this host";
  const closeBtn = el("button", "swb-close", "✕ back to the wheel");
  closeBtn.type = "button";
  // FULL SCREEN: a class on the overlay, not the Fullscreen API — the panel is
  // a dialog inside the page, and a real fullscreen request would take the
  // whole document with it and strip the browser chrome the operator uses to
  // move between the dashboard and their editor.
  const fullscreenBtn = el("button", "swb-fullscreen", "⛶");
  fullscreenBtn.type = "button";
  fullscreenBtn.setAttribute("aria-label", "expand doxBench to fill the window");
  fullscreenBtn.setAttribute("aria-pressed", "false");
  fullscreenBtn.title = "fill the window";
  fullscreenBtn.addEventListener("click", () => {
    const on = !overlay.classList.contains("is-fullscreen");
    overlay.classList.toggle("is-fullscreen", on);
    fullscreenBtn.setAttribute("aria-pressed", on ? "true" : "false");
    fullscreenBtn.setAttribute(
      "aria-label",
      on ? "restore doxBench to its normal size"
         : "expand doxBench to fill the window");
    fullscreenBtn.title = on ? "restore size" : "fill the window";
  });
  head.append(titles, readonly, fullscreenBtn, closeBtn);

  // THE SESSION BAR (FR-045/FR-044): a row of its own under the head, holding
  // the BRANCH-SESSION posture indicator and the session affordances. It is
  // deliberately NOT the pill above and NOT a tab: the pill states what
  // AUTHORITY this plane has, while this states what BRANCH the view is on and
  // whether it is a draft view — two different honesties, and a single chip
  // trying to be both would be neither. Scope-level rather than tab-level,
  // because a session belongs to the tile, not to a panel.
  const sessionbar = el("div", "swb-sessionbar");
  const posturechip = el("span", "swb-posture");
  const sessionhost = el("div", "swb-sessionhost");
  sessionbar.append(posturechip, sessionhost);

  const tabbar = el("div", "swb-tabs");
  tabbar.setAttribute("role", "tablist");
  const body = el("div", "swb-body");

  // THE THREE-REGION LAYOUT (010-doxbench-editor-chat FR-003): retained
  // docs/lens context (the existing tabbar + body, untouched in identity —
  // `drawTab()`'s own `body.innerHTML = ""` still clears ONLY this region)
  // beside the doxBench authoring canvas. `.swb-regions` is a row so a THIRD
  // region (the pending chat rail) can slot in behind a
  // `.swb-regions.has-rail` modifier class without a re-layout — nothing
  // ships an empty rail region this slice cannot back.
  const context = el("div", "swb-context");
  context.append(tabbar, body);
  const canvas = el("div", "doxbench-canvas");
  // T092 (FR-003/FR-041): the two live regions are LANDMARKS with accessible
  // names, so assistive navigation lands on them by name; the pending chat
  // rail will be the third when its wave arrives.
  context.setAttribute("role", "region");
  context.setAttribute("aria-label", "docs and lens context");
  canvas.setAttribute("role", "region");
  canvas.setAttribute("aria-label", "doxBench authoring canvas");
  // T055 (FR-003): the THIRD region the `.has-rail` modifier was reserved
  // for — a named landmark like its two siblings, hidden until a chat-capable
  // plane with both injected transports backs it.
  const rail = el("div", "doxbench-rail");
  rail.hidden = true;
  rail.setAttribute("role", "region");
  rail.setAttribute("aria-label", "doxBench chat rail");
  const regions = el("div", "swb-regions");
  regions.append(context, canvas, rail);

  // WORKSPACE CONTROLS (operator ask, 2026-08-02). Brett stopped mid-session
  // because the surface was too cramped to think in: "we need a button on the
  // window to make it full screen ... and a button on each of the 1/3 panes to
  // make them the size of the window with the other 2 1/3 panes taking a
  // thinner slice."
  //
  // EQUAL THIRDS REMAINS THE DEFAULT (his ruling on annotation
  // vibe_1785561229002_13j8c18kk). Expand is a TEMPORARY OVERRIDE layered on
  // top: one `is-expanded-<region>` class at a time, cleared by pressing the
  // same control again. The compressed panes THIN, they never hide — the
  // context they hold must stay readable, which is why the CSS gives them a
  // min-width floor rather than `display: none`.
  //
  // Pure DOM + one class on `regions`: no layout arithmetic in JS, so the
  // stylesheet stays the single authority on geometry.
  const EXPANDABLE = [
    { key: "context", node: context, label: "docs and lens context" },
    { key: "rail", node: rail, label: "chat rail" },
    { key: "canvas", node: canvas, label: "authoring canvas" },
  ];
  let expanded = null;

  function applyExpansion() {
    for (const { key } of EXPANDABLE) {
      regions.classList.toggle("is-expanded-" + key, expanded === key);
    }
    for (const { key, btn } of expandControls) {
      const on = expanded === key;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.textContent = on ? "⤡" : "⤢";
    }
  }

  // The canvas and rail CLEAR their own containers when they mount
  // (`drawCanvas` does `canvas.innerHTML = ""`), which silently removed the
  // canvas control the first time this shipped — two buttons rendered where
  // three were constructed, and only a rendered-geometry measurement caught
  // it. So attachment is idempotent and re-asserted after every pane draw
  // rather than done once at construction.
  function attachExpandControls() {
    for (const { node, btn } of expandControls) {
      if (btn.parentElement !== node) node.appendChild(btn);
    }
  }

  const expandControls = EXPANDABLE.map(({ key, node, label }) => {
    const btn = el("button", "swb-expand", "⤢");
    btn.type = "button";
    btn.setAttribute("aria-label", "expand the " + label);
    btn.setAttribute("aria-pressed", "false");
    btn.title = "give this pane most of the width; the other two thin to a "
      + "sliver. Press again for equal thirds.";
    btn.addEventListener("click", () => {
      expanded = expanded === key ? null : key;
      applyExpansion();
    });
    node.appendChild(btn);
    return { key, node, btn };
  });

  applyExpansion();

  // T090/T091 (FR-040/FR-025): the ONE presentation-posture answer, explained
  // inline where it changes what is offered, announced politely, and never
  // displacing the retained context beside it. Hidden entirely when the
  // posture needs no explanation.
  const postureNote = el("div", "swb-posture-note");
  postureNote.hidden = true;
  postureNote.setAttribute("aria-live", "polite");

  panel.append(head, sessionbar, postureNote, regions);
  overlay.appendChild(panel);
  container.appendChild(overlay);

  let lastFocused = null;
  let scope = null;
  let activeTab = "docs";
  // THE LENS SESSION (design D4): the checked-keyword selection lives HERE, at
  // the shell's scope lifetime, beside activeTab — so a tab switch preserves it
  // and only a new scope (or a close-and-reopen) reseeds from the scope's own
  // keywords. `lensSessionSeed` owns that rule and is unit-tested pure.
  let lensSession = null;
  const tabButtons = new Map();
  for (const def of TAB_DEFS) {
    const btn = el("button", "swb-tab", def.label);
    btn.type = "button";
    btn.setAttribute("role", "tab");
    btn.addEventListener("click", () => {
      activeTab = def.key;
      drawTab();
      bindCanvasToSelectionTab(def.key);
    });
    // CHK007 (T100 AT, re-reported 2026-08-02): this CONTEXT strip is the
    // second `role=tablist` on the surface and had no roving tabindex
    // either — the operator's re-report lands here. Same WAI-ARIA APG
    // pattern as the canvas buffer strip: one tabbable tab, Left/Right and
    // Up/Down move selection with focus, Home/End to the ends, arrows
    // consumed so they never scroll the page instead.
    btn.addEventListener("keydown", (ev) => {
      const steps = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      const order = TAB_DEFS.map((d) => d.key);
      let next = null;
      if (ev.key in steps) {
        const at = order.indexOf(activeTab);
        next = order[(at + steps[ev.key] + order.length) % order.length];
      } else if (ev.key === "Home") {
        next = order[0];
      } else if (ev.key === "End") {
        next = order[order.length - 1];
      }
      if (next === null) return;
      ev.preventDefault();
      activeTab = next;
      drawTab();
      bindCanvasToSelectionTab(next);
      tabButtons.get(next).focus();
    });
    tabbar.appendChild(btn);
    tabButtons.set(def.key, btn);
  }

  function close() {
    overlay.hidden = true;
    body.innerHTML = "";
    sessionhost.innerHTML = "";
    if (canvasController && typeof canvasController.destroy === "function") {
      canvasController.destroy();
    }
    canvasController = null;
    canvas.innerHTML = "";
    teardownRail();
    scope = null;
    lensSession = null;   // closing discards the selection (design D4)
    if (typeof lastFocused?.focus === "function") lastFocused.focus();
    lastFocused = null;
  }
  closeBtn.addEventListener("click", close);
  overlay.addEventListener("click", (ev) => { if (ev.target === overlay) close(); });
  // scoped to the caller's RENDER (see app.js `nextRenderScope`)
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !overlay.hidden) { ev.stopPropagation(); close(); }
  }, { signal });

  // The create seam handed to every panel (tasks 5.4–5.8). ONE seeding rule per
  // tab (staging-workbench-model.js `createSeed`), ONE dialog, and ONE place the
  // capability verdict is consulted — so no panel can grow its own posture.
  const create = {
    offered(tab) { return createOffered(scope, tab); },
    seed(tab, extra) { return createSeed(snapshot, scope, tab, extra || {}); },
    options(extra) {
      return {
        caps, fetcher, repair: consoleRepair, slot: (extra || {}).slot,
        label: CREATE_LABELS[activeTab],
        // task 5.8: land on the document, not on a path string. The snapshot
        // predates the new file, so the viewer resolves it through the same
        // read-only source pass-through every other document read uses.
        onOpenDoc: onOpenDoc ? (path) => onOpenDoc(path, null) : null,
        // A create inside a tile scope OPENS or JOINS the tile's branch session
        // (FR-001). The session bar's posture was derived from a roster fetched at
        // boot, which cannot know that yet, so the shell is told and re-derives —
        // this is app.js's cross-module wiring role applied inside the overlay,
        // and it is why swb-create.js does not import swb-session.js.
        //
        // T092 defect 5, the headline "editing is broken" experience: redrawing the
        // session bar was ALL this used to do, so the page stayed keyed to `main`
        // — where FR-014a guarantees the new document is not — and the human read
        // `created ✓` beside `could not load … (HTTP 404)`, with the rewrite picker
        // offering only the two documents that predated their create. Three things
        // happen here now, in this order and for three different reasons:
        //   1. the created path joins the page-lifetime overlay, so the picker
        //      offers it IMMEDIATELY and the route agrees (a session may rewrite
        //      what it created — `gate_routes.foreign_document_refusal`);
        //   2. the bar re-derives, as before;
        //   3. the shell re-keys to the session ref. swb-create AWAITS the
        //      returned hand-off before its `onOpenDoc` jump — that keeps the
        //      source read and edit action on `main` until the session snapshot
        //      is ready, then moves both together before opening the document,
        //      WITHOUT widening `main`, which must never carry a draft.
        onSessionOpened: (result) => {
          sessionOpened(result.ref);
          documentCreated(result.ref, result.path);
          drawSession();
          return rekeyToSession(result.ref);
        },
      };
    },
    mount(host, tab, extra) {
      if (!this.offered(tab)) return null;
      return mountCreateAffordance(host, this.seed(tab, extra),
        { ...this.options(extra), label: CREATE_LABELS[tab] });
    },
    open(host, tab, extra) {
      if (!this.offered(tab)) return null;
      return openCreateDialog(host, this.seed(tab, extra),
        { ...this.options(extra), label: CREATE_LABELS[tab] });
    },
  };

  // THE SESSION BAR's draw (FR-044/FR-045). Called on every open and again after
  // an ENDING, so the affordances RE-DERIVE from the same posture derivation
  // rather than staying open against a session that is over: a save that came
  // back `merged: true` ended it (FR-033), an abandon ended it (FR-021), and
  // `endedSessions()` is the page-lifetime overlay both land in.
  function drawSession() {
    posturechip.textContent = "";
    posturechip.title = "";
    sessionhost.innerHTML = "";
    // FR-048 (review finding 14): a plane that declares `session: false` is the
    // HOSTED plane and shows no session surface at all — not the posture line
    // naming an unmerged branch, and not the affordance row. The whole bar goes,
    // so there is nothing for a later branch of this function to leak.
    sessionbar.hidden = !scope || sessionSurfaceHidden(caps);
    if (!scope || sessionSurfaceHidden(caps)) return;
    const posture = sessionPosture(scope,
      // the SNAPSHOT is passed for the G12 question the posture has to ask
      // (finding 18): which refs in this tile's ordinal family are another
      // ADVERTISED tile's own session branch. It is the same tile inventory the
      // engine's `discover_tile_inventory` unions, read from the projection the
      // page already holds — no route and no second liveness signal.
      { active, index, snapshot,
        opened: openedSessions(), ended: endedSessions() });
    posturechip.textContent = posture.label;
    posturechip.title = posture.detail;
    posturechip.classList.toggle("is-draft", posture.ownTile);
    posturechip.classList.toggle("is-live", posture.live && !posture.ownTile);
    mountSessionAffordances(sessionhost, {
      scope,
      posture,
      // The edit picker's options: the documents this tile's session MAY rewrite
      // — the tile's own material plus what this page's creates landed in the
      // session (`rewritableDocuments`). A path is chosen rather than typed.
      //
      // This used to be every resolved path in `scope.documents`, i.e. every
      // section flattened — and the comment here justified it as "the scope's OWN
      // resolved document paths … a path outside the worktree refuses". Worktree
      // containment is not topic ownership: the T092 sweep picked another topic's
      // staged document out of the CLUSTER NEIGHBOURHOOD section this same panel
      // labels "not the topic's own material" and REPLACED it, on this tile's
      // branch, under a gate record that read as authorised. The route refuses it
      // now too (`gate_routes.foreign_document_refusal`) — the picker is UI, the
      // route is the boundary, and they are deliberately the same sentence.
      documents: rewritableDocuments(scope, createdDocuments(posture.branch)),
    }, {
      caps, fetcher, repair: consoleRepair,
      actor: (caps && caps.actor) || null,
      onSessionEnded: async () => {
        if (typeof onSessionEnded !== "function") return null;
        // FR-039 (T081): capture the tile's own session branch BEFORE the
        // rebind below — ending a session must clear the doxBench working
        // state persisted under that session ref, and after the rebind
        // nothing here remembers which ref died. Captured now, cleared only
        // once the end is CONFIRMED (a null next means it did not end).
        const endedBranch = sessionPosture(scope, {
          active, index, snapshot,
          opened: openedSessions(), ended: endedSessions(),
        }).branch;
        const next = await onSessionEnded();
        if (!next?.snapshot || !scope) return null;
        // T104 F1 (staging-workbench.js:709): the canvas is torn down BEFORE
        // the FR-039 clear, never after. `destroy()` ends in `persistNow()`,
        // which re-wrote the very session-keyed record the clear had just
        // removed — so the ended session's working state came straight back.
        // Destroying here is right for an ENDING (unlike a re-key): the
        // session is gone and its working state is deliberately cleared, so
        // the canvas must be rebuilt from the surviving main view below.
        if (canvasController && typeof canvasController.destroy === "function") {
          canvasController.destroy();
        }
        if (endedBranch && active?.repository) {
          // T104 F7-7: the clear targets the INJECTED storage seam — the
          // same handle the canvas persisted through, and the same threading
          // the editor's own re-key clear already does. The one-argument
          // call fell through to the ambient window storage global, so under
          // any injected storage the ended session's record silently
          // survived (FR-039 unmet under the very seam the shell forwards).
          clearDoxBenchSession({
            repository: active.repository, ref: endedBranch,
            tile_kind: scope.kind, tile_id: scope.id,
          }, doxbench?.storage);
        }
        const shellWasCurrent = shellActive?.repository === active?.repository &&
          shellActive?.ref === active?.ref;
        snapshot = next.snapshot;
        if (next?.active) active = next.active;
        if (next?.index) index = next.index;
        if (next?.sourceBase) sourceBase = next.sourceBase;
        // A dashboard loaded directly on the session has no pre-existing main
        // shell baseline. Once that session ends, advance the baseline to the
        // surviving main state; aggregate/main shells remain unchanged.
        if (shellWasCurrent) {
          shellSnapshot = snapshot;
          shellActive = active;
          shellIndex = index;
          shellSourceBase = sourceBase;
        }
        scope = workbenchScope(snapshot, scope.kind, scope.id);
        drawHead();
        // The old pane may contain bytes fetched from the retired branch. Rebuild
        // it from main before the shared edit action becomes reachable again.
        drawTab();
        drawCanvas();
        return next;
      },
      onRerender: drawSession,
    });
  }

  function drawTab() {
    for (const [key, btn] of tabButtons) {
      btn.setAttribute("aria-selected", String(key === activeTab));
      // CHK007 roving tabindex on the context strip (APG).
      btn.tabIndex = key === activeTab ? 0 : -1;
      btn.classList.toggle("swb-tab-active", key === activeTab);
    }
    body.innerHTML = "";
    if (!scope) {
      body.appendChild(el("div", "swb-empty",
        "this tile is not present in main — reload to see the current dashboard"));
      return;
    }
    const pane = el("div", "swb-pane swb-pane-" + activeTab);
    body.appendChild(pane);
    // PR #196 review F4: the docs pane hands back the reconcile the shell needs
    // to put the wheel back on the document the canvas really holds. A redraw
    // rebuilds the wheel, so the previous pane's reconcile is dropped with it
    // and the new one is adopted here.
    reconcileDocsSelection = null;
    if (activeTab === "docs") {
      reconcileDocsSelection = renderDocsPanel(pane, scope, onOpenDoc
        ? (row) => onOpenDoc(row.path, row.doc) : null, create,
        docTileVerbs());
      syncContextSelection();   // a fresh wheel starts where the canvas is
    } else if (activeTab === "lens") {
      // the session survives the tab switch and reseeds on a scope change —
      // the panel itself never builds a selection (design D4)
      lensSession = lensSessionSeed(lensSession,
        lensScopeSnapshot(snapshot, scope), scope);
      renderLensPanel(pane, snapshot, scope, lensSession, create);
    } else {
      renderOutlinePanel(pane, snapshot, scope, create, sourceBase, edit,
        outlineSectionSeam());
    }
  }

  // The scope's own header line — the count the T092 sweep watched stay at
  // "2 documents (1 inherited)" through a create. Factored out of `open` so the
  // re-key below can refresh it without re-opening the overlay.
  function drawHead() {
    if (!scope) {
      title.textContent = "doxBench";
      subtitle.textContent = "the ended session's tile is not present in main";
      return;
    }
    title.textContent = scope.title;
    subtitle.textContent = (KIND_LABELS[scope.kind] || scope.kind) + " · " +
      scope.id + " · " + scope.counts.documents + " document" +
      (scope.counts.documents === 1 ? "" : "s") +
      (scope.counts.inherited ? " (" + scope.counts.inherited + " inherited)" : "");
  }

  // THE doxBench CANVAS (010-doxbench-editor-chat FR-003/FR-040): offered
  // only on a capable local plane with a real, session-eligible (repository,
  // ref) key — gate-off or hosted stays exactly read-only-context, the same
  // posture rule the session bar already applies. `loadSource` and `hash`
  // come from the `doxbench` seam bundle app.js builds (T023) and are
  // forwarded here verbatim — this file opens no route and computes no
  // digest of its own; a caller that supplies no `doxbench` option leaves
  // both undefined, and the canvas degrades to its own honest "unavailable"
  // state exactly as before. `storage` is deliberately NOT forwarded: the
  // merge/abandon clearing path (FR-039) is T081 and is still open, so
  // wiring session-storage persistence now would make that gap live. Any
  // previous controller is destroyed before a new one mounts, so a
  // tab/session change never leaks a stale doxBench instance.
  let canvasController = null;
  let railController = null;
  // PR #63 review (Codex/Copilot): the posture note's approvedModelCount is
  // LIVE — fed back by the rail's adopted catalog through a pure callback
  // (the shell still opens no route). Zero until a catalog really loads.
  let approvedModelCount = 0;
  // T104 F10-1: the rail-reported catalog FAILURE, beside the count and by
  // the same channel. Without it every catalog failure fell through the
  // ladder to approvedModelCount === 0's "no approved model is configured" —
  // a misdiagnosis for both the recoverable stale token and the unreadable
  // catalog. Null until the rail reports one; reset on rail teardown.
  let railCatalogFailure = null;
  // R-1: the restored chat blob may arrive before the rail mounts (the canvas
  // restores during its own initial load), so it is held and applied as soon
  // as both sides exist — buffers and proposals never diverge.
  let pendingCompanion = null;
  function applyPendingCompanion() {
    if (!pendingCompanion || !railController || !canvasController) return;
    const live = canvasController.state();
    if (!live) return;
    const hexOf = (b) => (b && b.current_hash && b.current_hash.hex) || null;
    // T104 F1: taken and CLEARED before the restore, never after. `restore`
    // adopts new rail state, which renders, which calls back into `onState`
    // -- and this function is now called from there unconditionally, so a
    // blob still pending at that moment is re-applied forever.
    const companion = pendingCompanion;
    pendingCompanion = null;
    const restoreHashes = {};
    for (const key of Object.keys(live.buffers || {})) {
      restoreHashes[key] = hexOf(live.buffers[key]);
    }
    railController.restore(companion, restoreHashes);
  }
  function teardownRail() {
    if (railController && typeof railController.destroy === "function") {
      railController.destroy();
    }
    railController = null;
    regions.classList.toggle("has-rail", false);
    rail.hidden = true;
    approvedModelCount = 0;  // a torn-down rail reports no models (R5)
    railCatalogFailure = null;  // …and no catalog failure either (F10-1)
    // T104 F1: a companion blob captured for the tile being torn down must
    // never be applied to the NEXT tile's rail — it was cleared only on a
    // successful apply, so a blob left pending by a failed one crossed the
    // tile boundary and broke FR-011 conversation isolation.
    pendingCompanion = null;
  }
  // T104 F1: the tile's doxBench scope projection, derived in ONE place so a
  // non-destructive refresh cannot drift from what the mount used.
  function canvasProjection() {
    const posture = sessionPosture(scope,
      { active, index, snapshot, opened: openedSessions(), ended: endedSessions() });
    return doxbenchScopeProjection(snapshot, scope.kind, scope.id, {
      repository: active.repository,
      ref: active.ref,
      outlinePathFor: (outline) => primaryFragmentPath(outline.stagingId, outline.files),
      createdDocuments: createdDocuments(posture.branch),
    });
  }
  function railScopeKey() {
    return { repository: active.repository, ref: active.ref,
             tile_kind: scope.kind, tile_id: scope.id };
  }
  // ---- THE SELECTION HALF (add-doxbench-editing-phase-a) ------------------
  //
  // The context region chooses which buffer the canvas presents, and therefore
  // which buffer the chat works on. Both routes below go through the CANVAS's
  // own primitives — `setActiveBuffer` and `selectDocument`, which own the
  // state authority, the scope refusal, and the unsaved-Document guard. This
  // file adds no second context-tracking mechanism and no second guard: it
  // says which selection happened and lets the canvas answer.
  //
  // The switch is IMMEDIATE and has no confirm step, because changing which
  // buffer is ACTIVE replaces no content. The guard that DOES interrupt is
  // unchanged and unrelated: switching to a different DOCUMENT with unsaved
  // edits replaces buffer content, so `selectDocument` still blocks on it —
  // on this route exactly as on the canvas picker's.
  function bindCanvasToSelectionTab(tabKey) {
    if (tabKey !== "outline") return;   // `docs` binds per ROW, below; `lens` binds nothing
    if (!canvasController || typeof canvasController.setActiveBuffer !== "function") return;
    canvasController.setActiveBuffer("outline");
    // The rail states which buffer it is working on, read live off the canvas
    // state. A pure selection change moves no content identity, so nothing
    // else would have told it.
    refreshRailFromCanvas();
  }
  async function bindCanvasToDocument(path) {
    if (!canvasController || typeof canvasController.selectDocument !== "function") return;
    // PR #196 review F6: the canvas contains its own load failures now, so this
    // resolves with a stated refusal rather than rejecting — but the await is
    // what makes the two lines below run AFTER the answer instead of before it,
    // and the catch is defence in depth for a seam that ever regressed (an
    // unhandled rejection here would leave the wheel showing a document that
    // never loaded, with nothing said).
    let outcome = null;
    try {
      outcome = await canvasController.selectDocument(path);
    } catch (unused) {
      outcome = { status: "refused", reason: null };
    }
    // F3: the rail states which buffer it is WORKING ON, and choosing the
    // document already loaded (`unchanged`) still moves that binding — so the
    // refresh runs on every outcome, not only the ones that switch. Without it
    // the rail kept saying "Working on — outline" beside a chat now bound to
    // the document.
    refreshRailFromCanvas();
    // F4: unless the switch actually landed, the wheel must go back to the
    // document the canvas really holds — the same reconciliation the canvas's
    // own picker has always done for itself. A `blocked` outcome leaves the
    // guard open; if the human then resolves it with Discard, the switch fires
    // `onIdentitySettled` and the reconcile below runs again through
    // `syncContextSelection`, landing the wheel on the document that won.
    if (!outcome || (outcome.status !== "switched" && outcome.status !== "unchanged")) {
      syncContextSelection();
    }
    // RETURNED for the load route (the only caller since Phase B stopped a docs
    // row selection from binding): the tile states the outcome, so the verb has
    // to be able to read it.
    return outcome;
  }
  // ---- THE TILE VERBS (add-doxbench-editing-phase-b, Q3 ruled) -------------
  //
  // Every one goes through the CANVAS's own primitives, exactly as the selection
  // half above does: the canvas owns the loaded set, the state authority, the
  // scope refusal and the governed Save, and this file says which verb a human
  // invoked. No second loaded-set store, no second save path, no widened
  // authority — the tile's Save is a second ENTRY POINT to one mechanism.
  //
  // Absent where editing is absent: with no canvas controller the seam returns
  // no functions at all, and the tile then STATES the absence rather than
  // failing on activation.
  function docTileVerbs() {
    // F3 (PR #207 review): where EDITING is unreachable the tile must offer no
    // load and no save AT ALL -- the ratified rule is that they "MUST be
    // unreachable and MUST state that absence rather than failing when
    // activated". Returning live functions that answered "not wired" on click was
    // failing on activation with the wrong sentence, which is the exact posture
    // the requirement forbids. `read` is untouched: it needs no gate capability.
    //
    // The predicate is `canvasOffered()` -- THE SAME derivation `drawCanvas`
    // uses to decide whether to mount an editing canvas at all -- and
    // deliberately NOT `canvasController !== null`. The docs pane is drawn
    // BEFORE the canvas mounts (`drawTab` runs first), so a controller check
    // would have withheld the verbs on every capable surface too: the tile
    // would say "no editing capability" on a console that has one. Asking the
    // capability directly cannot be fooled by mount ordering, and the verbs
    // below re-check the controller at CLICK time, by which point it exists.
    if (!canvasOffered()) {
      return { bufferStateFor: () => null };
    }
    return {
      load: async (path) => {
        // Re-checked at CLICK time, not at render time: the docs pane is drawn
        // before the canvas mounts, so a human who clicks before the mount
        // settles gets a stated refusal rather than a thrown handler.
        if (!canvasController
            || typeof canvasController.loadDocumentForEditing !== "function") {
          return { ok: false,
                   error: "this console has no editing seam wired" };
        }
        // TWO ROUTES, and which one applies is a fact about the RESERVED SLOT.
        //
        // While that slot is UNBACKED — a scope whose projection published no
        // document, and the create flow's not-yet-created artifact — the first
        // load FILLS it, through `selectDocument`. That keeps the released v1
        // envelope's own document present (it carries the outline plus the
        // reserved slot and nothing else) and keeps Phase A's unsaved-edit guard
        // on the one transition that still REPLACES a buffer's content, which is
        // exactly the narrowing the delta predicted: the guard is "unchanged by
        // this rule WHERE IT STILL APPLIES" and is never extended to selection.
        //
        // Once the slot is backed, a load ADDS a path-keyed buffer beside it and
        // replaces nothing — which is what makes the loaded set a set.
        const reserved = reservedDocumentPath();
        let outcome = null;
        try {
          if (reserved === null) {
            const switched = await bindCanvasToDocument(path);
            outcome = switched && (switched.status === "switched"
                                   || switched.status === "unchanged")
              ? { ok: true, key: "document", error: null }
              : { ok: false,
                  error: (switched && switched.reason)
                    || "this document was not loaded" };
          } else {
            outcome = await canvasController.loadDocumentForEditing(path);
          }
        } catch (unused) {
          outcome = { ok: false, error: "the load failed" };
        }
        syncContextFromCanvas();
        refreshDocTiles();
        return outcome || { ok: false, error: "the load was refused" };
      },
      save: async (path) => {
        if (!canvasController
            || typeof canvasController.saveDocument !== "function") {
          return { ok: false, error: "the governed Save is not wired here" };
        }
        // F2 (PR #207 review): `saveDocument` takes a BUFFER KEY, not a path,
        // and the two differ for exactly the buffer every restored Phase A
        // session holds -- a real document under the RESERVED `document` key.
        // Passing the path made the tile's Save enabled (the marking resolves by
        // path and found it) and then refused (the save resolved by key and did
        // not). The key is the one `bufferStateFor` already resolved, so it is
        // read from there rather than derived a second time.
        const live = docBufferState(path);
        const key = live && live.key ? live.key : path;
        let outcome = null;
        try {
          outcome = await canvasController.saveDocument(key);
        } catch (unused) {
          outcome = { ok: false, error: "the Save failed" };
        }
        syncContextFromCanvas();
        return outcome || { ok: false, error: "the Save was refused" };
      },
      // LIVE, read at paint time and never cached (design D9): "has an open
      // unsaved edit" is a fact about a browser, and the snapshot's generator
      // cannot observe one, so it is never written anywhere.
      bufferStateFor: docBufferState,
    };
  }
  // The one resolver from a document PATH to the live buffer that holds it,
  // carrying the KEY it is held under (F2). Both the tile's marking and the
  // tile's Save read it, so the control's enabled state and the act it performs
  // cannot resolve to different buffers.
  function docBufferState(path) {
    const live = canvasController && canvasController.state();
    if (!live || !live.buffers) return null;
    for (const key of Object.keys(live.buffers)) {
      const buffer = live.buffers[key];
      if (buffer && buffer.kind === "document" && buffer.path === path) {
        return { loaded: true, dirty: buffer.dirty === true,
                 owned: buffer.owned === true, key };
      }
    }
    return { loaded: false, dirty: false, owned: true, key: null };
  }
  // ---- THE ADD-SECTION SEAM (add-staged-topic-outline-template task 3.2) ----
  //
  // The outline tab's add-section affordance writes into the OUTLINE BUFFER and
  // stops there. The human's existing Save is what carries the new section to the
  // branch through `edit-document`; this seam performs no write, opens no route,
  // and invokes no gate verb. That is the whole of the ruling: section-scoped
  // patching is a patch-TARGETING detail, so it introduces no second write verb.
  //
  // `apply` is the canvas's OWN `applyProposal`, reused rather than paralleled.
  // It is the existing primitive for "swap one buffer's whole text": it gates on
  // the SETTLED content identity (so an insert computed against text the buffer
  // has since moved off is refused, never forced), re-applies the document's own
  // line-ending flavor (without which one reviewed insertion becomes a whole-file
  // EOL rewrite — the defect the buffer contract's proposal path already paid
  // for), and lands through the same `edit()` a keystroke does, which is what
  // makes the dirty state, the hashing and the Save plan identical to typing. A
  // second insertion method would have to re-earn all three.
  //
  // WITHHELD, not degraded, where editing is not live (task 3.4). The predicate
  // is `canvasOffered()` — the same derivation `drawCanvas` and `docTileVerbs`
  // use, and deliberately not `canvasController !== null`, because `drawTab` runs
  // BEFORE the canvas mounts and a controller check would withhold the affordance
  // on every capable console too. A null seam makes the controls inert with no
  // listener bound.
  function outlineSectionSeam() {
    if (!canvasOffered()) return null;
    return {
      actor: (caps && caps.actor) || "local",
      // Read at CLICK time, never cached: "what the outline buffer holds" is a
      // fact about this browser a moment ago.
      buffer: () => {
        const live = canvasController && canvasController.state();
        const buffer = live && live.buffers ? live.buffers.outline : null;
        if (!buffer) return null;
        return { path: buffer.path, text: buffer.content,
                 baseHash: (buffer.current_hash && buffer.current_hash.hex) || null };
      },
      // Every refusal this seam makes for itself carries a CODE, in the same
      // vocabulary `applyProposal` answers in, because the panel maps codes and
      // never echoes text (W-10). A refusal with no code would fall through to
      // the panel's generic sentence rather than the accurate one.
      apply: async (baseHash, text) => {
        if (!canvasController
            || typeof canvasController.applyProposal !== "function") {
          return { ok: false, code: "unavailable",
                   error: "this console has no editing seam wired" };
        }
        try {
          return await canvasController.applyProposal(
            "outline", { base_hash: baseHash, content: text });
        } catch (unused) {
          return { ok: false, code: "failed", error: "the insertion failed" };
        }
      },
    };
  }
  // "A buffer moved" — repaint the tiles' loaded / loaded-and-dirty marking and
  // the expanded tile's Save reachability from the live state.
  function refreshDocTiles() {
    const pane = body.querySelector
      ? body.querySelector(".swb-pane-docs")
      : null;
    if (pane && typeof pane.__docWheelRefresh === "function") {
      pane.__docWheelRefresh();
    }
  }
  // The wheel's reconcile, as adopted by the last docs draw (null on the other
  // selection tabs, where there is no wheel to reconcile).
  let reconcileDocsSelection = null;
  // WHICH DOCUMENT THE CANVAS IS ON, in ONE place (add-doxbench-editing-phase-b).
  //
  // Phase A could read `state.buffers.document.path`: there was exactly one
  // document slot, so "the document the canvas holds" was a single well-defined
  // value whichever buffer happened to be SELECTED. Phase B holds N, so the
  // question needs a stated rule, and this is it:
  //
  //   1. the SELECTED buffer's path, when a document is selected — that is the
  //      document the human is working on, and it is what the wheel must
  //      reconcile to and what a released v1 turn must name; otherwise
  //   2. the FIRST loaded document in the declared order, because the outline
  //      being selected does not mean the canvas holds no document — it means the
  //      human stepped to the outline, and the docs wheel must still sit on the
  //      document they were on rather than snapping back to the top of the reel;
  //   3. `null` when nothing is loaded.
  //
  // Reading it in TWO places with two spellings is exactly how the wheel and the
  // canvas came to disagree before (PR #196 review F4), so both callers below
  // read this.
  function canvasDocumentPath() {
    const current = canvasController && canvasController.state();
    if (!current || !current.buffers) return null;
    const selected = current.buffers[current.active_buffer];
    if (selected && selected.kind === "document" && selected.path) {
      return selected.path;
    }
    const documentKeys = Object.keys(current.buffers)
      .filter((key) => key !== "outline")
      .sort((left, right) => (left < right ? -1 : left > right ? 1 : 0));
    for (const key of documentKeys) {
      const buffer = current.buffers[key];
      if (buffer && buffer.path) return buffer.path;
    }
    return null;
  }
  // The RESERVED `document` slot's own path, or null -- the question the LOAD
  // route asks to decide whether a first load FILLS the unbacked slot or ADDS a
  // path-keyed buffer beside it. It stopped being a wire question at
  // contract-v1.34, when the widened envelope started carrying the whole loaded
  // set; it remains a state question, and it is still a different one from
  // `canvasDocumentPath` above, which answers "which document is the human on"
  // for the WHEEL.
  function reservedDocumentPath() {
    const current = canvasController && canvasController.state();
    if (!current || !current.buffers) return null;
    const reserved = current.buffers.document;
    return reserved && reserved.path ? reserved.path : null;
  }
  function syncContextSelection() {
    if (typeof reconcileDocsSelection !== "function") return;
    const path = canvasDocumentPath();
    if (path == null) return;
    reconcileDocsSelection(path);
  }
  // T100 P1-A, factored out (Phase A): every settled identity refreshes the
  // rail's proposal currency so stale reaches the RENDERED cards — and the same
  // pass re-renders the rail's header, which is where the bound buffer is
  // stated. A pure selection change calls it directly for that second reason.
  // Still a PURE callback: it reads the live controller and opens no route.
  function syncContextFromCanvas() {
    refreshRailFromCanvas();
    syncContextSelection();
  }
  function refreshRailFromCanvas() {
    if (!railController || !canvasController) return;
    const current = canvasController.state();
    if (!current || !current.buffers) return;
    const hexOf = (b) => (b && b.current_hash && b.current_hash.hex) || null;
    // add-doxbench-editing-phase-b: currency is refreshed for EVERY buffer key
    // the canvas holds, not two fixed names. A proposal's target is a buffer key
    // now, so a currency map that carried only two of N keys would leave a
    // proposal against a third document permanently unable to go stale.
    const hashes = {};
    for (const key of Object.keys(current.buffers)) {
      hashes[key] = hexOf(current.buffers[key]);
    }
    railController.refreshCurrency(hashes);
  }
  function canvasHoldsUnsavedWork() {
    const live = canvasController && canvasController.state();
    if (!live || !live.buffers) return false;
    return Object.values(live.buffers).some((b) => b && b.dirty === true);
  }
  // THE KEY CHANGE, non-destructively where it has to be (T104 F1).
  //
  // Every session key change used to answer with `drawCanvas()`, which
  // destroys the controller and rebuilds both buffers from `/source` — so a
  // create-document (or a Save) landing while the human had unsaved text
  // discarded it silently: no dirty check, no guard, no warning, and
  // `destroy()` persisted the doomed state under the OLD key on the way out.
  // The seam written for exactly this — the canvas's own `refreshContext`,
  // plus the `rekey` that moves working state onto a ref keeping both buffers
  // as they are — had no production caller at all.
  //
  // With no unsaved work the full remount is still the cleaner answer (it
  // reloads bases from the ref the view now reads), so the destructive path
  // stays for that case and for a canvas that is not mounted.
  function recanvasForKeyChange({ canvasAlreadyRekeyed = false } = {}) {
    if (!canvasController || !canvasHoldsUnsavedWork()) {
      drawCanvas();
      return;
    }
    if (!canvasAlreadyRekeyed && typeof canvasController.rekey === "function") {
      canvasController.rekey(active.ref);
    }
    if (typeof canvasController.refreshContext === "function") {
      canvasController.refreshContext(canvasProjection());
    }
    // EVERY consumer follows the ref, not just the canvas: the rail's scope
    // key is what its next turn declares, and it was captured by value at
    // mount (`railController.rekey` had no caller anywhere in the bundle).
    if (railController && typeof railController.rekey === "function") {
      railController.rekey(railScopeKey());
    }
  }
  // ONE rule for whether the plane's posture stands as an inline line (Brett's
  // 2026-08-18 annotation round 2, on the `editor-only` instance of it: "add a
  // model selector down next to the send button. make this text the hover text
  // for the send button if no model selected").
  //
  // A CHAT rung's sentence is now the send button's stated reason — tooltip and
  // `aria-describedby`, inside the rail, where the human is trying to act — so
  // it does not stand here as well. The PLANE rungs (hosted, gate-off, unkeyed,
  // source-unavailable) keep the inline note: they explain a canvas that is
  // WITHHELD or degraded, the rail is not even mounted for most of them, and
  // there is no control to hang the sentence on.
  function showPostureNote(plane) {
    const stands = !!plane.note && plane.chat !== true;
    postureNote.textContent = stands ? plane.note : "";
    postureNote.hidden = !stands;
  }

  // WHETHER THIS SURFACE OFFERS EDITING AT ALL — one derivation, read by the
  // canvas mount and by the docs tile's verbs (F3), so the tile can never claim a
  // capability the canvas withheld or deny one it has.
  function canvasOffered() {
    return !!scope && createGateLive(caps) && !sessionSurfaceHidden(caps)
      && !!active?.repository && !!active?.ref;
  }
  function drawCanvas() {
    if (canvasController && typeof canvasController.destroy === "function") {
      canvasController.destroy();
    }
    canvasController = null;
    canvas.innerHTML = "";
    teardownRail();
    // T091: state the plane's posture BEFORE deciding the canvas, so a
    // withheld canvas is explained rather than silently absent. The offering
    // decision itself is unchanged and stays pinned below; `approvedModelCount`
    // is LIVE — fed back by the mounted rail's adopted catalog (see the
    // onState wiring below) and reset to zero on rail teardown.
    const plane = presentationPosture({
      gateLive: createGateLive(caps),
      surfaceHidden: sessionSurfaceHidden(caps),
      repository: active?.repository,
      ref: active?.ref,
      sourceAvailable: !!(doxbench && doxbench.loadSource),
      approvedModelCount,
      catalogFailure: railCatalogFailure,
    });
    showPostureNote(plane);
    const offered = canvasOffered();
    canvas.hidden = !offered;
    if (!offered) return;
    // the SAME posture derivation drawSession() already uses, so the
    // session-created documents doxBench treats as editable never drift from
    // what the session bar itself would call this tile's own session
    const projection = canvasProjection();
    canvasController = mountDoxBenchCanvas(canvas, projection, {
      title: scope.title,
      loadSource: doxbench?.loadSource,
      hash: doxbench?.hash,
      save: doxbench?.save,
      // R-1 (2026-08-02): per-key session storage IS now forwarded. It was
      // withheld while FR-039 clearing was open (T081); that landed, so the
      // deferral's own condition is discharged. Buffers AND the chat rail's
      // working state (subject/model/transcript/PROPOSALS) persist in ONE
      // record per scope key, so reopening the same tile continues the work
      // and a restored proposal is re-scored against the restored bytes.
      storage: doxbench?.storage,
      companionOf: () => (railController ? railController.snapshot() : null),
      onCompanionRestored: (companion) => {
        pendingCompanion = companion;
        applyPendingCompanion();
      },
      // T104 F1: the Save hand-off. The canvas re-keys ITSELF onto the
      // session ref; this is how everything else follows — the shell's
      // active/source base, the session bar, and the rail's scope key.
      onSaveLanded: (ref) => adoptSessionRef(ref, { canvasAlreadyRekeyed: true }),
      // T100 P1-A: every settled identity refreshes the rail's proposal
      // currency so stale reaches the RENDERED cards — and (PR #196 review F4)
      // puts the context region's own selection back on whichever document the
      // canvas ended up holding, which is how a guard resolved with Discard
      // reaches the wheel.
      onIdentitySettled: syncContextFromCanvas,
    });
    // T055: the chat rail mounts ONLY when the seam bundle carries BOTH
    // injected transports — the shell forwards them verbatim and opens no
    // route of its own. The rail reads the CURRENT editor buffers through
    // the live controller at submit time (T054), so buffer focus and state
    // are never disturbed: the canvas mount above is byte-identical to the
    // pre-rail wiring.
    const railOffered = !!(doxbench && doxbench.catalog && doxbench.chatTurn);
    regions.classList.toggle("has-rail", railOffered);
    rail.hidden = !railOffered;
    if (railOffered) {
      railController = mountDoxBenchChatRail(rail, {
        scopeKey: { repository: active.repository, ref: active.ref,
                    tile_kind: scope.kind, tile_id: scope.id },
        transports: { catalog: doxbench.catalog, chatTurn: doxbench.chatTurn },
        onState: (chatState) => {
          // R-1 (T104 F1): the rail exists now, so a blob restored before it
          // mounted can be applied. UNCONDITIONALLY — this used to sit inside
          // the `count !== approvedModelCount` branch below, so the restored
          // chat working state (subject, model, composer, transcript,
          // PROPOSALS) was silently dropped on every remount unless a
          // non-empty model catalog happened to load, which never happens in
          // the shipped zero-adapter posture.
          applyPendingCompanion();
          const models = chatState.models || [];
          const count = models.filter((m) => m.available === true).length;
          // T104 F10-1: the FAILURE moves the note too, not only the count —
          // a failed catalog never changes the count (it stays zero), which
          // is exactly why the misdiagnosed "no approved model is
          // configured" note used to stand unchallenged.
          const failure = chatState.catalogFailure || null;
          if (count !== approvedModelCount
              || failure !== railCatalogFailure) {
            approvedModelCount = count;
            railCatalogFailure = failure;
            const refreshed = presentationPosture({
              gateLive: createGateLive(caps),
              surfaceHidden: sessionSurfaceHidden(caps),
              repository: active?.repository,
              ref: active?.ref,
              sourceAvailable: !!(doxbench && doxbench.loadSource),
              approvedModelCount,
              catalogFailure: railCatalogFailure,
            });
            showPostureNote(refreshed);
          }
        },
        applyProposal: (target, record) => (canvasController
          ? canvasController.applyProposal(target, record)
          : null),
        editorState: () => canvasController && canvasController.state(),
        // add-doxbench-editing-phase-b: the rail's loaded-document SELECTOR
        // reaches the selection through the canvas's own primitive, which owns
        // the state authority. D7: three routes, one value -- this one, the
        // context region's outline tab, and a load -- and the selector never
        // becomes a second state authority.
        // F9: the loaded set's one way OUT, reached through the canvas's own
        // primitive, which owns the dirty refusal. The rail states the outcome.
        unloadBuffer: async (key, unloadOptions) => {
          if (!canvasController
              || typeof canvasController.unloadDocument !== "function") {
            return { ok: false, error: "unloading is not wired on this console" };
          }
          let outcome = null;
          try {
            outcome = await canvasController.unloadDocument(key, unloadOptions);
          } catch (unused) {
            outcome = { ok: false, error: "the unload failed" };
          }
          syncContextFromCanvas();
          refreshDocTiles();
          return outcome || { ok: false, error: "the unload was refused" };
        },
        selectBuffer: async (key) => {
          if (!canvasController
              || typeof canvasController.setActiveBuffer !== "function") return;
          canvasController.setActiveBuffer(key);
          syncContextFromCanvas();
          refreshDocTiles();
        },
        // (The v1 wire's narrowing stood here: the rail's active-document option
        // was pinned to the RESERVED slot's own path, because the released
        // envelope carried that one document and nothing else, and beside it the
        // candidate list a "no active document" refusal named. contract-v1.34's
        // widened family carries the whole loaded set and a DECLARED bound-buffer
        // key, so the rail reads its binding off the one selection authority
        // itself and neither option exists any more -- task 8.6's N4 posture ends
        // here, as that record said it would.)
      });
    }
    // PR #196 review F3, the mount-time half: the rail's header names the
    // canvas's buffers, and the canvas HAS none until its initial load settles
    // -- so the header rendered "(absent)" and stayed that way until some
    // unrelated event happened to re-render the rail. One refresh when the load
    // resolves, guarded because the controller may already have been torn down
    // and replaced by then.
    const mounted = canvasController;
    if (mounted && mounted.ready && typeof mounted.ready.then === "function") {
      mounted.ready.then(() => {
        if (canvasController === mounted) syncContextFromCanvas();
      });
    }
    // LAST, after every mount: each pane's controller clears its own host, so
    // a control appended at construction is gone by the time the pane renders.
    // Re-asserted here rather than at the top of the draw — an earlier
    // placement was itself wiped by the mount that follows it, and only a
    // rendered-geometry measurement showed two controls where three were
    // constructed.
    attachExpandControls();
    applyExpansion();
  }

  // T092 defect 5 — RE-KEY THE OVERLAY TO THE SESSION THE CREATE JUST OPENED.
  //
  // `onSessionRekey` resolves only after the shell has fetched the session's own
  // view of the world and moved source/edit routing together. What is adopted
  // here is deliberately partial, and the two halves are separate decisions:
  //
  //   ADOPTED — `active` (so the posture stops saying "this view is main" about a
  //   view that is now reading the session, and reads FR-045's own DRAFT VIEW
  //   sentence instead), `index`, `snapshot`, `sourceBase`, the re-derived scope,
  //   the header line, and the session bar.
  //
  //   NOT REDRAWN — the open tab's body. The create's confirmation ("created ✓",
  //   the record, the branch, the commit) is rendered there, and an asynchronous
  //   re-render arriving a tick later would eat the engine's own report of the
  //   most consequential thing the human just did. That is exactly the T088
  //   defect the ending's report already had to be rescued from; the panel
  //   re-derives on the next tab switch, from the adopted snapshot.
  //
  // The page BEHIND the overlay is untouched: the wheel, the funnel and the board
  // stay on `main`, because a draft never appears in a shared surface (FR-014a) —
  // which is the state `sessionPosture`'s DRAFT VIEW detail already describes.
  //
  // T104 F1: this is now the ONE adoption path for a session key change,
  // reached from the create (`rekeyToSession`) and from a governed Save that
  // opened or joined a session (`onSaveLanded`). The difference between them
  // is only who moved the canvas: the Save path's canvas has already re-keyed
  // ITSELF (doxbench-editor `rekeyTo`, which also takes the pre-session
  // storage key away), so it says so.
  function adoptSessionRef(ref, { canvasAlreadyRekeyed = false } = {}) {
    if (!ref || typeof onSessionRekey !== "function") return Promise.resolve(null);
    return Promise.resolve(onSessionRekey(ref)).then((next) => {
      if (!next || !next.snapshot || !scope) return null;
      snapshot = next.snapshot;
      if (next.active) active = next.active;
      if (next.index) index = next.index;
      if (next.sourceBase) sourceBase = next.sourceBase;
      scope = workbenchScope(snapshot, scope.kind, scope.id);
      drawHead();
      drawSession();
      recanvasForKeyChange({ canvasAlreadyRekeyed });
      return next;
    });
  }
  function rekeyToSession(ref) {
    return adoptSessionRef(ref);
  }

  // Give back whatever a draft stood down. A draft holds `docs`/`lens`/`outline`
  // because they read a TILE and a draft has none; the moment one exists — a
  // scoped open, or the create that MAKES the tile — they are meaningful again
  // and must say so. Factored out because there are now two ways back.
  function releaseHeldTabs() {
    for (const [, btn] of tabButtons) {
      if (btn && btn.dataset && btn.dataset.draftHeld) {
        btn.disabled = false;
        btn.title = "";
        delete btn.dataset.draftHeld;
      }
    }
  }

  function open(kind, id) {
    releaseHeldTabs();          // a scoped open restores whatever a draft stood down
    lastFocused = document.activeElement;
    snapshot = shellSnapshot;
    active = shellActive;
    index = shellIndex;
    sourceBase = shellSourceBase;
    scope = workbenchScope(snapshot, kind, id);
    activeTab = "docs";
    lensSession = null;   // a fresh open is a fresh selection (design D4)
    overlay.hidden = false;
    if (!scope) {
      // a stale click after regeneration, or a synthesized demo possible: say
      // so plainly rather than rendering an empty scope as if it were real
      title.textContent = "doxBench";
      subtitle.textContent = (KIND_LABELS[kind] || kind) + " · " + id;
      body.innerHTML = "";
      body.appendChild(el("div", "swb-empty",
        "this tile does not resolve in the snapshot — regenerate and reload"));
      for (const [, btn] of tabButtons) btn.setAttribute("aria-selected", "false");
      drawSession();          // an unresolvable tile gets NO session affordances
      drawCanvas();           // and no stale doxBench canvas from a prior open
      closeBtn.focus();
      return;
    }
    if (typeof onScopeOpened === "function") {
      const routed = onScopeOpened(scope.ref);
      if (routed?.active) active = routed.active;
      if (routed?.sourceBase) sourceBase = routed.sourceBase;
    }
    drawHead();
    drawSession();
    drawTab();
    drawCanvas();
    closeBtn.focus();
  }

  // ---- lens -> doxBench (Brett, 2026-08-08) --------------------------------
  //
  // "we need to have button to move this to doxBench. and open the doxBench UI
  // if the user moves forward." A drafted staging seed is not a tile, so it
  // resolves no `workbenchScope` — and it does not need to. What it needs is
  // the thing a tile create already does: the GOVERNED create, which opens or
  // joins a branch session and lands the new document there rather than on
  // main. So this entry point opens the overlay with no scope and hands the
  // seed straight to the same dialog, which means no second write path, no
  // second session concept, and save/abandon behave exactly as they do for
  // every other created document.
  function openDraft(seed) {
    lastFocused = document.activeElement;
    snapshot = shellSnapshot;
    active = shellActive;
    index = shellIndex;
    sourceBase = shellSourceBase;
    scope = null;                 // a draft has no tile; the seed IS the scope
    activeTab = "docs";
    lensSession = null;
    overlay.hidden = false;
    title.textContent = "doxBench — new document";
    subtitle.textContent = seed?.source || "from a lens selection";
    body.innerHTML = "";
    // THE SCOPE-BOUND TABS STAND DOWN while a draft is open (Brett,
    // 2026-08-09: "if I click the docs tab, that screen disappears and no way
    // to get it back"). `docs`, `lens` and `outline` all derive from a TILE,
    // and a draft has none until it is created — so they rendered empty AND
    // destroyed the draft, with no route back to it. Disabled with the reason
    // on them is the honest state; a scoped `open()` gives them back.
    for (const [key, btn] of tabButtons) {
      btn.setAttribute("aria-selected", "false");
      btn.disabled = true;
      if (btn.dataset) btn.dataset.draftHeld = "1";
      btn.title = "this is a new document — " + key + " reads a tile's own "
        + "material, and there is no tile until it is created";
    }
    drawSession();
    drawCanvas();
    // The create is GATED, and an ungated plane says so rather than offering a
    // dialog whose submit cannot land (the same posture the rest of this
    // overlay takes).
    // the SERVE's posture, not the view's projection
    const authoring = createCaps || caps;
    if (!createGateLive(authoring) || sessionSurfaceHidden(authoring)) {
      // Defence in depth: the lens no longer OFFERS the jump where it cannot
      // land, so reaching this is a programming error rather than a posture —
      // it still says something true and actionable rather than showing an
      // empty overlay (Brett, 2026-08-08: "it was blank").
      body.appendChild(el("div", "swb-empty",
        "this view is read-only, so a document cannot be created from it — a "
        + "merged project composes several repositories and a document is "
        + "created IN a repository. Switch to the one that owns this material "
        + "and draft there; nothing was lost."));
      closeBtn.focus();
      return;
    }
    // LAND ON THE DOCUMENT, not on a form (Brett, 2026-08-09: "prefill all
    // these fields and just make them available to edit if the user wants…
    // make this doc meta data available as a tab. but go direct in to let the
    // user start working on the doc"). The form alone in an overlay whose
    // other regions have no scope is what read as "the doxWorkbench is empty":
    // the thing the human came to see — the drafted fragment — was not on
    // screen at all.
    // The seed is a whole fragment: a header block, then the prose. The create
    // writes the header from its own fields, so only the PROSE is the human's
    // — split at the first `## `, where every drafted fragment's body begins.
    const seedText = String(seed.seedText || "");
    const bodyAt = seedText.indexOf("\n## ");
    let bodyText = bodyAt >= 0 ? seedText.slice(bodyAt + 1) : seedText;

    const strip = el("div", "swb-drafttabs");
    const pane = el("div", "swb-draftpane");
    // TWO PANES BUILT ONCE, TOGGLED — not one pane rebuilt per tab (Brett's
    // ruling, 2026-08-10: keep the tabs, put ONE save on both). Rebuilding was
    // also quietly destructive: switching document -> details -> document threw
    // the create form away and rebuilt it from the seed, so a Title or Summary
    // the human had already rewritten was silently restored to its default.
    // The body survived only because `bodyText` lives in this closure.
    const bodyPane = el("div", "swb-draftbodypane");
    const detailsPane = el("div", "swb-draftdetails");
    // The chrome the ONE action lives in. Outside both panes, so `save` and the
    // answer it gets are on screen whichever tab the human is standing on.
    const chrome = el("div", "swb-draftchrome");
    const tabs = [
      { id: "document", label: "document" },
      { id: "details", label: "details" },
    ];
    const buttons = new Map();

    // Write the edited body over the freshly created document, through the
    // SAME gate verb the console uses everywhere else. It carries the scope
    // because `edit-document` resolves its session from one; the save seam's
    // own request shape has no scope field, which is why this posts directly —
    // the pattern `submitCreate` in swb-create.js already follows.
    // Write the edited body over the freshly created document, through the
    // SAME save seam the canvas uses — no new transport anywhere, because
    // `firstEditBody` ALREADY carries a scope: it reads `tile_kind`/`tile_id`
    // off the key. That was the missing piece all along (Brett: "is the issue
    // that we do not have a name to save it under?"), and the staging seed had
    // computed the name from the start.
    async function writeBody(path) {
      if (!bodyText.trim()) return null;      // nothing written, nothing to save
      const seams = doxbench || {};
      if (!seams.loadSource || !seams.save || !seams.hash) {
        return { refused: "this console has no editing seam wired" };
      }
      let loaded = null;
      try {
        loaded = await seams.loadSource(path);
      } catch {
        loaded = null;
      }
      if (!loaded || typeof loaded.content !== "string") {
        return { refused: "the created document could not be read back" };
      }
      // the created header, then the human's body: the create owns the one and
      // the human owns the other, and neither overwrites the other's half
      const content = loaded.content.replace(/\s*$/, "") + "\n\n" + bodyText;
      try {
        // AWAITED. `contentIdentity` is async (SHA-256 through `crypto.subtle`,
        // which returns a promise), so an un-awaited call hands the planner a
        // PROMISE where it expects `{algorithm, hex}` — `statedIdentity` reads
        // that as no identity at all and refuses the buffer. The base was
        // already being passed that way; both are awaited here, in the try, so
        // an oversize buffer refuses with its own message instead of throwing.
        const [baseIdentity, currentIdentity] = await Promise.all(
          [seams.hash(loaded.content), seams.hash(content)]);
        const verdict = await seams.save({
          key: {
            repository: seed.repository,
            ref: loaded.ref || null,
            // the SCOPE the edit resolves its branch session from
            tile_kind: DRAFT_TILE_KIND,
            tile_id: seed.scopeId,
          },
          // THE BUFFER THE SAVE PLANNER ACTUALLY READS (measured in a browser,
          // 2026-08-10: this body was NEVER written — the plan reported
          // `unchanged`, the transport was never called, and the human read
          // "the save was refused" over a document that had simply been left
          // alone). `saveOrder`/`planRow` in doxbench-save.js read four fields
          // this row did not carry, each of which fails CLOSED:
          //
          //   * `dirty` — `saveOrder` plans only `dirty === true` (FR-031
          //     persists only CHANGED buffers). Absent, the row was skipped
          //     before anything else was looked at. It is dirty by
          //     construction: it is the created header with the body appended.
          //   * `path` — `planRow` reads the document path from `path` and
          //     DERIVES the action from it (`actionForPath`: a path present is
          //     a rewrite). `document`/`action` were this file's own spelling
          //     and neither was ever read.
          //   * `owned` — a buffer that does not declare ownership is refused
          //     as context-only. The session owns the document it just created.
          //   * `current_hash` — an unsettled identity is refused. It is
          //     settled here: the content is composed synchronously above.
          buffers: [{
            kind: "document", path, content, dirty: true, owned: true,
            current_hash: currentIdentity,
            base_hash: baseIdentity,
            base_ref: loaded.ref || null,
            base_revision: loaded.revision || null,
          }],
        });
        // `runSave` reports an ARRAY of per-buffer outcome rows (data-model
        // PerBufferSaveOutcome), one per kind — never a map. Indexing it as one
        // gave `undefined` for every save, so even a COMMITTED body would have
        // read as refused.
        // add-doxbench-editing-phase-b: the per-buffer outcome row's first
        // field is `key` (the BUFFER KEY) rather than `kind`. This seam request
        // declares no key, so `savePlanState` keys it by its `kind` -- which
        // lands it on the reserved `document` slot, exactly what a create's
        // not-yet-keyed buffer is.
        const row = (verdict && Array.isArray(verdict.buffers)
          ? verdict.buffers.find((r) => r && r.key === "document") : null);
        if (row && row.status === "committed") return { committed: true };
        return { refused: (row && row.message) || "the save was refused" };
      } catch (err) {
        return { refused: (err && err.message) || "the save failed" };
      }
    }

    // THE CREATE IS THE END OF THE DRAFT (Brett, 2026-08-10: "after it is
    // created, the tabs for the window are not functional. I cannot do
    // anything from that point on that document").
    //
    // A draft stands `docs`/`lens`/`outline` down because they read a TILE and
    // a draft has none. The create MAKES the tile — the document lands in
    // `ideation/staging/<topic>/` on the session branch, and the session's own
    // regenerated snapshot carries it — so from that moment the reason those
    // tabs were held is false, and leaving them held is a dead end: the create
    // lands and there is nothing to do next.
    //
    // So the overlay stops being a draft and BECOMES that tile's workbench, on
    // the session snapshot: the tabs come back, the head names the topic, the
    // docs pane lists the created document, and the session bar offers the
    // verbs that continue the work.
    //
    // WHICH TILE — matched on the DOCUMENT PATH the create just reported, and
    // deliberately NOT on `seed.scopeId`. Both are called `staging_id` and they
    // are NOT the same string: the seed's is the branch session's composite
    // scope (`<repository>:staging:<topic>`, staging_seed.py) and the
    // snapshot's is the bare topic. Measured, 2026-08-10 — passing the seed's
    // through resolved no tile and the promotion silently did nothing. Reading
    // the path is exact and assumes no vocabulary at all; deriving one spelling
    // from the other would be this file guessing a server naming rule, which is
    // the class of mistake that dropped the create's scope in #152.
    //
    // If no tile carries the document, the draft is left exactly as it is: an
    // overlay whose panes still hold the human's fragment beats a blank one
    // (Brett, 2026-08-08: "it was blank").
    let adopted = null;
    function promoteDraftToTile(createdPath) {
      const rel = String(createdPath || "");
      if (!adopted || !adopted.snapshot || !rel) return;
      const tile = (adopted.snapshot.staged_topics || []).find(
        (t) => (t && t.files || []).some((f) => String(f) === rel));
      const promoted = tile
        ? workbenchScope(adopted.snapshot, DRAFT_TILE_KIND, tile.staging_id)
        : null;
      if (!promoted) return;
      snapshot = adopted.snapshot;
      if (adopted.active) active = adopted.active;
      if (adopted.index) index = adopted.index;
      if (adopted.sourceBase) sourceBase = adopted.sourceBase;
      scope = promoted;
      activeTab = "docs";
      releaseHeldTabs();
      drawHead();
      drawSession();
      drawTab();            // rebuilds `body` — the draft strip and pane go
      drawCanvas();
    }

    function showPane(id) {
      for (const [key, btn] of buttons) {
        btn.setAttribute("aria-selected", String(key === id));
        btn.disabled = key === id;
      }
      // TOGGLE, never rebuild: the panes and the form inside them are built
      // once, so a tab switch cannot discard what the human has typed into
      // either of them.
      bodyPane.hidden = id !== "document";
      detailsPane.hidden = id !== "details";
    }

    function buildDraftPanes() {
      {
        openCreateDialog(detailsPane, seed, {
          caps: authoring, fetcher, repair: consoleRepair,
          label: "create document",
          // SAVE, not create (Brett, 2026-08-10: "it seems to the user that we
          // already have a document and what we want to do is save the
          // document"). By the time this is on screen the document IS there —
          // his body, his fields — and only the engine calls it a create.
          submitLabel: "save",
          runningLabel: "saving… (opening the branch session)",
          // the ONE action, in the chrome, on screen from BOTH tabs
          actionsHost: chrome,
          // the body is what the human came to write; the fields must not
          // steal the caret when the overlay opens on the document tab
          focusOnMount: false,
          // CREATE-THEN-EDIT, in ONE action. The create opened the branch
          // session for this topic's scope; the edit resolves that same LIVE
          // session and writes the body over the header. Both verbs carry the
          // scope the staging seed computed — which is the whole of what was
          // missing when this first refused (Brett: "is the issue that we do
          // not have a name to save it under?").
          onOpenDoc: async (path) => {
            const wrote = await writeBody(path);
            if (wrote && wrote.refused) {
              // the document EXISTS with its header and only the body failed:
              // saying which is the difference between a retry and a mystery.
              // Into the CHROME, beside the outcome the save already reported,
              // because the promotion below rebuilds everything else.
              chrome.appendChild(el("div", "swb-draftfail",
                "the document was created, but its body was refused: "
                + wrote.refused));
            }
            if (onOpenDoc) onOpenDoc(path, null);
            // LAST, because it rebuilds `body` (T088's lesson: a re-render
            // destroys the host an outcome was written into). Everything above
            // has finished writing into the draft pane by the time this runs.
            promoteDraftToTile(path);
          },
          onSessionOpened: async (result) => {
            sessionOpened(result.ref);
            documentCreated(result.ref, result.path);
            drawSession();
            // The re-key itself, WITHOUT the DOM half: `adoptSessionRef` bails
            // on a draft (it guards `!scope`, and a draft has none), so the
            // routing hand-off is taken here and the adoption is held until
            // `onOpenDoc` above has run.
            adopted = typeof onSessionRekey === "function"
              ? await onSessionRekey(result.ref) : null;
            return adopted;
          },
        });
      }
      // THE BODY IS YOURS TO WRITE (Brett, 2026-08-09). The header block is
      // NOT here: the create generates it from the fields on `details`, so
      // offering an edit of a header that is about to be regenerated would be
      // offering an edit that is discarded. What is editable is exactly what
      // the create does not write.
      //
      // THE SECOND BUTTON IS GONE (Brett, 2026-08-10: "There is a button name
      // and create it. what is that for?" and "what if we remove both those
      // buttons?"). It read `name it and create →` and created nothing — it
      // switched tabs, which the tabs above already do. Two controls promising
      // a create, one of them navigation, was the confusion written out. What
      // remains is one `save`, in the chrome below, reachable from both tabs.
      // WHAT YOU ALREADY HAVE, BEFORE YOU SAVE (Brett, 2026-08-10: "if same
      // keywords, then we want to list it in the doxBench too. so the user
      // knows he now has two of this topic"). Every create-only refusal tonight
      // was this fact arriving too late — from the engine, after the press.
      const already = existingOnTopic(shellSnapshot, seed.topics, seed.area);
      if (already.length) {
        const collides = already.filter((r) => r.inFolder);
        const box = el("div", "swb-draftexisting");
        box.appendChild(el("div", "swb-draftexistinghead", collides.length
          ? "⚠ " + collides.length + " document"
            + (collides.length === 1 ? "" : "s")
            + " already in " + seed.area
            + " — saving a new one under the same name is refused"
          : already.length + " existing document"
            + (already.length === 1 ? "" : "s") + " already carry"
            + (already.length === 1 ? "" : "") + " these keywords"));
        for (const row of already.slice(0, 8)) {
          const line = el("div", "swb-draftexistingrow");
          line.appendChild(el("span", "swb-dxpath", row.path));
          if (row.shared.length) {
            line.appendChild(el("span", "swb-dxterms",
              row.shared.join(" · ")));
          }
          if (row.inFolder) {
            line.appendChild(el("span", "swb-dxsame", "same folder"));
          }
          box.appendChild(line);
        }
        if (already.length > 8) {
          box.appendChild(el("div", "swb-draftexistingrow",
            "…and " + (already.length - 8) + " more"));
        }
        box.appendChild(el("div", "swb-dxnote",
          "Nothing here blocks you: a second document on a shared topic is "
          + "ordinary. But if one of these IS what you are about to write, "
          + "rewrite that one instead — open it from the docs pane on its "
          + "session branch — and if the name collides, change Title or Area "
          + "on `details` first."));
        bodyPane.appendChild(box);
      }
      bodyPane.appendChild(el("div", "swb-draftnote",
        "The body of the fragment, drafted from your selection and yours to "
        + "edit. Its HEADER — title, summary, topics — is on the `details` "
        + "tab, already filled in, and the SUMMARY there still says "
        + "`TO WRITE`: replace it before you save. `save` lands both, on a "
        + "branch of this topic's own and never on main."));
      const area = document.createElement("textarea");
      area.className = "swb-draftbody";
      area.value = bodyText;
      area.setAttribute("aria-label", "the document's body");
      area.addEventListener("input", () => { bodyText = area.value; });
      bodyPane.appendChild(area);
    }

    for (const tab of tabs) {
      const btn = el("button", "swb-drafttab", tab.label);
      btn.type = "button";
      btn.setAttribute("role", "tab");
      btn.addEventListener("click", () => showPane(tab.id));
      buttons.set(tab.id, btn);
      strip.appendChild(btn);
    }
    pane.append(bodyPane, detailsPane, chrome);
    body.appendChild(strip);
    body.appendChild(pane);
    buildDraftPanes();     // both, ONCE — `showPane` only toggles from here on
    showPane("document");
    closeBtn.focus();
  }

  return { open, close, openDraft };
}
