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
  documentAbstract, docWheelEntries,
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

function renderDocsPanel(pane, scope, onOpen, create) {
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

  // A drum is one reel, so the sections flatten — carrying their labels onto
  // the tiles rather than losing them (see `docWheelEntries`).
  const entries = docWheelEntries(scope);
  const wheel = renderDocWheel(selector, entries, {
    onSelect: (entry) => renderAbstract(abstract, entry ? entry.row.doc : null),
    // SELECT and OPEN stay distinct verbs, as they were in the flat list:
    // selecting must not steal the read-only viewer, and opening (from the
    // expanded tile) must not be the only way to look at a document.
    onOpen: onOpen ? (row) => onOpen(row) : null,
  });
  pane.__docWheel = wheel;

  // An empty scope has no tile to select, so nothing seeded the abstract: say
  // so explicitly rather than leaving the upper half blank.
  if (!entries.length) renderAbstract(abstract, null);
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

// `sourceBase` is the ACTIVE (repository, ref)'s own keyed `/source/` base
// (PR #49 review finding 16). Without it `renderViewer` fell back to the unkeyed
// `/source/`, which the server resolves to the ACTIVE REGISTRY ENTRY — and the
// active entry is deliberately kept on `main` for a session's whole life
// (FR-014a). So the outline of a DRAFT view rendered `main`'s bytes, or 404'd
// for a document the session had just created, while the docs row beside it —
// which app.js keys correctly — showed the session's own. US2 acceptance
// scenario 5 and FR-010 both name the outline explicitly, and spec §US2 calls
// this exact failure "specifically dangerous — a draft view mistaken for main".
function renderOutlinePanel(pane, snapshot, scope, create, sourceBase, edit) {
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
  const host = el("div", "swb-outline");
  pane.appendChild(host);
  // read-only, through the viewer's own /source pass-through: renderViewer owns
  // the fetch, the divergence banner, and the degraded no-shim / 404 message —
  // exactly the document viewer's posture, because it IS the document viewer.
  const doc = (snapshot.documents || []).find((d) => d.path === path) || null;
  renderViewer(host, { path, doc, sourceBase, edit });
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
    btn.addEventListener("click", () => { activeTab = def.key; drawTab(); });
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
        caps, fetcher, slot: (extra || {}).slot,
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
      caps, fetcher, actor: (caps && caps.actor) || null,
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
    if (activeTab === "docs") {
      renderDocsPanel(pane, scope, onOpenDoc
        ? (row) => onOpenDoc(row.path, row.doc) : null, create);
    } else if (activeTab === "lens") {
      // the session survives the tab switch and reseeds on a scope change —
      // the panel itself never builds a selection (design D4)
      lensSession = lensSessionSeed(lensSession,
        lensScopeSnapshot(snapshot, scope), scope);
      renderLensPanel(pane, snapshot, scope, lensSession, create);
    } else {
      renderOutlinePanel(pane, snapshot, scope, create, sourceBase, edit);
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
    railController.restore(companion, {
      outline: hexOf(live.buffers.outline),
      document: hexOf(live.buffers.document),
    });
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
    postureNote.textContent = plane.note || "";
    postureNote.hidden = !plane.note;
    const canvasOffered = !!scope && createGateLive(caps) && !sessionSurfaceHidden(caps) &&
      !!active?.repository && !!active?.ref;
    canvas.hidden = !canvasOffered;
    if (!canvasOffered) return;
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
      // currency so stale reaches the RENDERED cards.
      onIdentitySettled: () => {
        if (!railController || !canvasController) return;
        const current = canvasController.state();
        if (!current) return;
        const hexOf = (b) => (b && b.current_hash && b.current_hash.hex) || null;
        railController.refreshCurrency({
          outline: hexOf(current.buffers.outline),
          document: hexOf(current.buffers.document),
        });
      },
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
            postureNote.textContent = refreshed.note || "";
            postureNote.hidden = !refreshed.note;
          }
        },
        applyProposal: (target, record) => (canvasController
          ? canvasController.applyProposal(target, record)
          : null),
        editorState: () => canvasController && canvasController.state(),
        activeDocumentPath: () => {
          const current = canvasController && canvasController.state();
          return current ? current.buffers.document.path : null;
        },
        // T104 F2: the documents a turn on this tile may actually name — the
        // scope authority's own intersection, so a "no active document"
        // refusal names one the operator can pick instead of stopping at the
        // refusal. Read from the projection this canvas was mounted on; the
        // shell derives nothing of its own here.
        documentCandidates: () => projection.active_document_candidates || [],
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

  function open(kind, id) {
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
    for (const [, btn] of tabButtons) btn.setAttribute("aria-selected", "false");
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
        const verdict = await seams.save({
          key: {
            repository: seed.repository,
            ref: loaded.ref || null,
            // the SCOPE the edit resolves its branch session from
            tile_kind: "staged",
            tile_id: seed.scopeId,
          },
          buffers: [{
            kind: "document", action: "edit", document: path, content,
            base_hash: seams.hash(loaded.content),
            base_ref: loaded.ref || null,
            base_revision: loaded.revision || null,
          }],
        });
        const row = verdict && verdict.buffers && verdict.buffers.document;
        if (row && row.status === "committed") return { committed: true };
        return { refused: (row && row.message) || "the save was refused" };
      } catch (err) {
        return { refused: (err && err.message) || "the save failed" };
      }
    }

    function showPane(id) {
      for (const [key, btn] of buttons) {
        btn.setAttribute("aria-selected", String(key === id));
        btn.disabled = key === id;
      }
      pane.innerHTML = "";
      if (id === "details") {
        openCreateDialog(pane, seed, {
          caps: authoring, fetcher,
          label: "create document",
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
              // saying which is the difference between a retry and a mystery
              pane.appendChild(el("div", "swb-draftfail",
                "the document was created, but its body was refused: "
                + wrote.refused));
            }
            if (onOpenDoc) onOpenDoc(path, null);
          },
          onSessionOpened: (result) => {
            sessionOpened(result.ref);
            documentCreated(result.ref, result.path);
            drawSession();
            return rekeyToSession(result.ref);
          },
        });
        return;
      }
      // THE BODY IS YOURS TO WRITE (Brett, 2026-08-09). The header block is
      // NOT here: the create generates it from the fields on `details`, so
      // offering an edit of a header that is about to be regenerated would be
      // offering an edit that is discarded. What is editable is exactly what
      // the create does not write.
      pane.appendChild(el("div", "swb-draftnote",
        "The body of the fragment, drafted from your selection and yours to "
        + "edit. The HEADER comes from the fields on `details`. Creating "
        + "opens the branch session for this topic, lands the header, and "
        + "writes this body over it in the same session — two governed verbs, "
        + "one action, and never on main."));
      const area = document.createElement("textarea");
      area.className = "swb-draftbody";
      area.value = bodyText;
      area.setAttribute("aria-label", "the document's body");
      area.addEventListener("input", () => { bodyText = area.value; });
      pane.appendChild(area);
      const go = el("button", "cbtn", "name it and create →");
      go.type = "button";
      go.addEventListener("click", () => showPane("details"));
      pane.appendChild(go);
    }

    for (const tab of tabs) {
      const btn = el("button", "swb-drafttab", tab.label);
      btn.type = "button";
      btn.setAttribute("role", "tab");
      btn.addEventListener("click", () => showPane(tab.id));
      buttons.set(tab.id, btn);
      strip.appendChild(btn);
    }
    body.appendChild(strip);
    body.appendChild(pane);
    showPane("document");
    closeBtn.focus();
  }

  return { open, close, openDraft };
}
