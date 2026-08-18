// doxBench's authoring canvas (010-doxbench-editor-chat, US1: tasks
// T033-T036, fix round T033c). Holds exactly the Outline and Document buffers,
// their debounced Markdown preview, the document-switch guard (with a real
// document picker to reach it), and per-buffer focus/selection/scroll
// persistence across every switch and context refresh (FR-003..FR-010,
// acceptance scenarios 1-5).
//
// PHASE A (add-doxbench-editing-phase-a, ratified 2026-08-15) MOVED ONE
// DECISION OUT OF THIS FILE AND SPLIT WHAT WAS LEFT:
//
//   THE CANVAS NO LONGER CHOOSES WHICH BUFFER IT SHOWS. It presents the ACTIVE
//   buffer, and the context region beside it makes that choice -- focusing the
//   `outline` SELECTION tab, or picking a row out of the scoped docs set. The
//   buffer tablist this file used to render is retired as a CONTROL: two
//   surfaces answering one question is how the two come to disagree. The labels
//   it carried survive as DOXBENCH_BUFFER_LABELS, which name buffers for
//   accessible names and say nothing about being clickable.
//
//   THE FREED LEVEL IS THE VIEW TABS. `Editor` (the active buffer's raw
//   Markdown) and `Preview` (its rendering) replace the side-by-side split
//   pane. Same rendering path, same debounce, same single mountSafeMarkdown
//   sink -- a layout change, not a rendering feature. `Preview` is selected at
//   mount because most opens are to read or resume, and switching INTO Preview
//   flushes the pending render, because the pane a human cannot see is exactly
//   the one a debounce may leave stale.
//
//   THE PANEL CARRIES ONE SAVE AND ONE CANCEL, outside both view tabs, so each
//   control and its answer are on screen whichever view the human stands on.
//   Save is unchanged in every respect except its count: it was already
//   whole-canvas (the dirty set over BUFFER_KINDS, one call to the seam,
//   ordering owned by ./doxbench-save.js) and merely drawn twice. Cancel is
//   the genuinely per-buffer half -- `discardBuffer` aimed at the ACTIVE buffer
//   and no other, because discard destroys unsaved human work and a single
//   control that silently reverted a buffer nobody was looking at would be this
//   surface's one irreversible surprise.
//
//   NOTHING ELSE MOVED. No Save semantics, no ordering, no authority, no
//   staleness rule: the per-buffer content-identity guard below is untouched,
//   and the consolidated controls sit INSIDE it rather than beside it.
//
// WHAT THIS MODULE DELIBERATELY DOES NOT OWN:
//
//   - transport of any kind. `loadSource` and `storage` are the caller's own
//     injected seams (a real mount wires them from the shell's own read path
//     and the browser's own tab-scoped storage); this module itself never
//     opens a network connection, a socket, a cross-tab store, or a shell
//     command, and it never dynamically imports anything. Without an
//     injected `loadSource`, every backed path degrades to an honest
//     "unavailable" state -- never a fabricated read (FR-007). Every one of
//     these absences is enforced structurally by
//     test_doxbench_mutation_boundary.py, both by reading this file's own
//     source text and by driving it end to end against traps that would
//     record any attempt.
//   - the governed Save itself. `save` is a SEAM, exactly like `loadSource`:
//     this module decides which buffers are dirty, hands them over, reports
//     the verdict, and adopts the bases the answer says landed. It performs no
//     ordering, chooses no action, and reaches nothing -- the orchestration
//     lives in ./doxbench-save.js and the authority lives at the gate.
//   - chat, model selection, or any provider concern -- later tracks.
//
// THE SAVE ARM IS GATED BY ITS SEAM, with exactly two states (US4/T079,
// FR-040's unreachable-control clause):
//
//   NO SEAM INJECTED -- the honest posture for a console with no governed Save
//   wired. Every Save-shaped control (the panel button, its visible note, the
//   guard's own Save choice, and the guard's sentence) is byte-for-byte what it
//   was before this arm existed: disabled, `aria-disabled="true"`, and naming
//   SAVE_UNAVAILABLE_REASON as VISIBLE text beside the control rather than only
//   in a hover title. `save()` and `resolveGuard("save")` refuse with that same
//   fixed reason and change nothing at all. Nothing in this posture reads the
//   seam, because there is none. Cancel is untouched by this gate: a discard
//   persists nothing, so it is not a Save-shaped control and never claims to be.
//
//   A SEAM INJECTED -- Save becomes real. The controls are enabled, the fixed
//   reason is GONE rather than merely restyled (a disabled-looking control that
//   still says Save is unavailable while Save works would be the worst of both),
//   and each buffer reports its own verdict in its own live status region. ONE
//   button, still two answers: collapsing the report would hide exactly the
//   partial-success case the buffer contract requires to stay separable.
//
// WHAT A SAVE MAY AND MAY NOT CHANGE HERE. Only buffers the answer reports
// `committed` advance, and they advance to the ref, revision, and content
// identity THE SERVER REPORTED -- through adoptSavedBase, which validates that
// identity by the state module's own strict rule. A refused buffer keeps its
// text, its base, and its dirty flag exactly. While a Save is in flight the
// canvas says so (`aria-busy`, a stated status, Save and Discard both taken
// away) and refuses a second Save and any edit rather than queueing them: the
// bytes handed over are the bytes the verdict describes, so an edit landing
// mid-flight would make the returned identity a lie. A Save that lands on a
// session ref REKEYS this canvas's working state onto that ref and clears the
// pre-session key, so a later restore cannot resurrect pre-session text over
// governed material (FR-038, FR-039).
//
// THE ONLY STATE AUTHORITY IS ./doxbench-state.js. Every buffer transition
// goes through its exported primitives -- createDoxBenchState /
// createBufferState for a load, beginBufferEdit + settleBufferHash for an
// edit, discardBuffer for Cancel and for the guard's Discard, replaceBuffer to
// advance the state, adoptActiveBuffer (the state module's own
// `setActiveBuffer`, aliased so the controller method of that name can keep it)
// for a selection change, and persistDoxBenchState / restoreDoxBenchState for
// session recovery. BUFFER_KINDS is likewise the single enumeration authority:
// nothing below enumerates `outline` and `document` by name, so widening the
// buffer set is a change to the buffer contract and to nothing on this surface.
// This module never computes `dirty` itself, never compares a content identity
// itself, and never mutates a returned buffer object -- they are frozen, and
// replaceBuffer is the only way forward.
//
// THE GENERATION CONTRACT, PAIRED CORRECTLY. `settleBufferHash` only accepts
// a completion whose generation and content match the buffer it is handed --
// so it MUST be handed the LIVE buffer at settle time (`state.buffers[kind]`),
// never the snapshot the edit started from (that snapshot's own generation
// trivially always matches its own completion, which would make the
// staleness check a no-op and let an in-flight hash silently overwrite a
// newer Discard, edit, or document switch). test_doxbench_state.py's own race
// harness demonstrates the same pairing rule independently of any DOM.
//
// THE ONLY MARKDOWN/HTML PATH IS mountSafeMarkdown, imported from
// ./viewer.js. This file writes NO raw HTML sink of its own, anywhere --
// nodes are built ONCE at mount time and mutated afterwards through
// textContent, .value, attributes, and classList; the two preview containers
// are the sole exception, and they are always written through
// mountSafeMarkdown, never through a raw markup assignment. Rendering the
// empty/unavailable placeholder is a function of CONTENT, not only of
// `load_state` (which the state module deliberately preserves across an
// edit): the instant a buffer's content is non-empty, that content renders,
// even if its `load_state` started `empty` or `unavailable` -- otherwise a
// human typing a brand-new outline would never see it (US1 acceptance
// scenario 2/3). An `unavailable` fact that predates a human's own typing
// still stays visible, stated ALONGSIDE the dirty status rather than in
// place of it, because it still governs what a later Save would mean.
//
// PERSISTENCE IS CONTINUOUS. Every settled state transition -- a completed
// edit, a Cancel, a buffer switch, a document switch -- is handed to
// persistDoxBenchState against the caller's injected storage, and destroy()
// persists once more on the way out. The VIEW choice is deliberately not
// persisted: it is which way the human is looking, not what they have. After
// destroy(), the controller goes fully inert: edit, discard, cancel,
// selectDocument, resolveGuard, setActiveBuffer and setActiveView all refuse
// rather than touch a torn-down mount.
//
// FOCUS is tracked explicitly, never left to the DOM to remember for free: a
// hidden pane cannot hold real focus in a real document, so this module
// records which buffer last received it and restores that focus when its
// editor becomes visible again -- and never invents focus for a buffer that was
// never actually focused. A buffer's editor is visible only while that buffer
// is ACTIVE and the `Editor` view tab is selected, so the capture-on-hide /
// re-apply-on-show discipline is keyed on that combined predicate rather than
// on the buffer alone. The document-switch guard follows the same discipline in
// miniature: opening it moves focus to its Discard choice; resolving or
// cancelling it returns focus to the Document buffer's own text -- selecting
// the `Editor` view first, because the guard is an argument about unsaved bytes
// and the answer belongs where those bytes are -- and it never traps focus.
//
// selectDocument REFUSES a path outside the scope (neither a context path
// nor an editable path) rather than loading it -- FR-007 says "the
// explicitly selected SCOPED document", not any path a caller might name.
// TWO routes now reach it -- the context region's scoped docs selection
// (Phase A's primary one) and the labelled document picker this module keeps
// in its own chrome, listing exactly `projection.active_document_candidates`
// -- and they share ONE refusal vocabulary and ONE guard, stated here rather
// than at either caller. Choosing a path while the Document buffer is dirty
// still blocks on the guard, and the picker still reverts its displayed value
// until that guard resolves.

import { mountSafeMarkdown } from "./viewer.js";
import {
  BUFFER_KINDS,
  ContentEncodingError,
  ContentSizeError,
  adoptSavedBase,
  beginBufferEdit,
  clearDoxBenchSession,
  createBufferState,
  createDoxBenchState,
  discardBuffer,
  persistDoxBenchState,
  rekeyDoxBenchState,
  replaceBuffer,
  restoreDoxBenchState,
  // ALIASED, not renamed: the state module owns "advance the state onto this
  // active buffer", and the controller method callers reach for is the one
  // that spells the whole selection act. Two things deserved the same name;
  // the import is the one that gives way.
  setActiveBuffer as adoptActiveBuffer,
  settleBufferHash,
} from "./doxbench-state.js";

// THE CANVAS'S VIEW TABS -- which VIEW of the one active buffer is shown.
// Rendered in the order `Editor`, `Preview` (raw before rendered reads as a
// progression) with `Preview` SELECTED at mount: reading order and selection
// are different questions and Phase A answers them differently on purpose.
export const DOXBENCH_VIEW_TABS = Object.freeze([
  { key: "editor", label: "Editor" },
  { key: "preview", label: "Preview" },
]);

// The buffer LABELS, which are not a control. This is what is left of the
// retired buffer tablist: names for accessible names and status regions,
// keyed by the enumeration `doxbench-state.js` owns. A kind with no label
// here names itself, so widening BUFFER_KINDS cannot silently produce an
// unnamed surface.
export const DOXBENCH_BUFFER_LABELS = Object.freeze({
  outline: "Outline",
  document: "Document",
});

function bufferLabel(kind) {
  return DOXBENCH_BUFFER_LABELS[kind] || String(kind);
}

// A fixed, honest string. This slice never wires a governed Save action, so
// every Save-shaped control (the panel button, its visible note, and the
// guard's own Save choice) states exactly this instead of pretending to be
// reachable.
export const SAVE_UNAVAILABLE_REASON =
  "Save is not wired in this preview -- the governed Save action ships in a later change";

// SAVE_WIRED_NOTE IS RETIRED (Brett's 2026-08-18 annotation round 2: "remove
// these lines. the UI must be intuitive and not rely on this text to inform
// the user"). It stood permanently under the tab row explaining what Save
// does — "Save persists only the changed buffers, …" — which is the one thing
// the CONTROL can say by itself: Save is disabled while nothing is dirty and
// enabled the moment something is, so the button's own state carries the
// sentence the note used to spell out. What has no control to carry it, and
// therefore stays, is the UNAVAILABLE reason below: a Save that cannot run at
// all is not a state a disabled button can tell apart from a nothing-to-save state.

// Cancel's own fixed sentence. It names the ACT and the SCOPE of the act,
// because one control that could have reverted any buffer must say which one
// it is aimed at -- the active one, and no other.
export const CANCEL_TITLE =
  "restore the active buffer to its last loaded or saved text -- no other "
  + "buffer changes, and nothing is persisted";
export const GUARD_SAVE_WIRED_NOTE =
  "Save persists this Document buffer first, and then the switch continues";

// A losing race is told, never queued: two Saves in flight would be two
// governance actions for one human decision.
export const SAVE_BUSY_REASON =
  "a Save is already in flight for this canvas -- wait for it to settle before "
  + "starting another";
// The bytes handed over are the bytes the verdict describes.
export const EDIT_DURING_SAVE_REASON =
  "a Save is in flight for this canvas -- the text being saved cannot change "
  + "underneath it, so this edit was not applied";

// T104 F6-2: the fixed vocabulary for the window BEFORE working state exists.
// The textareas are built (and visible) before initialLoad() settles, so a
// keystroke can arrive while `state` is still null; it must be refused with
// this stated line, never dropped on a TypeError (CHK016/CHK019). Fixed
// wording on purpose -- like every refusal in this module it names the
// situation, never the content.
export const EDITOR_LOADING_REASON =
  "this canvas is still loading its sources -- editing is refused until the "
  + "load settles";
// T104 F6-6: the prefix for a load that FAILED (a hashing bound, a broken
// restore). The rest of the sentence is the state module's own size/encoding
// message -- byte counts and classes only, never document text.
const LOAD_FAILURE_PREFIX = "this canvas could not load its sources -- ";

const DESTROYED_REASON = "this doxBench canvas has been destroyed";
const DEFAULT_PREVIEW_DELAY_MS = 150;
// Long enough to be read at reading speed, short enough that it is plainly an
// EVENT and not the standing text annotation round 2 retired.
const DEFAULT_EVENT_NOTE_MS = 9000;
const FALLBACK_REVISION = "0".repeat(40);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

function basename(path) {
  if (path == null) return "";
  const value = String(path);
  return value.split("/").at(-1) || value;
}

// ---------------------------------------------------------------------------
// T104 F10-3 -- the EOL lens, the client half of FR-045's byte-exact
// round-trip. A <textarea>'s API value is LF-normalized BY SPECIFICATION: CR
// and CRLF both read back as LF no matter what was assigned. So a CRLF
// document loaded byte-exactly from /source (the server half landed with the
// base-lens fix) could never round-trip: the first keystroke silently
// rewrote every line ending, the buffer read dirty against an unchanged
// file, and syncBufferDom's value comparison could never settle (the two
// spellings cannot compare equal). The lens keeps the two domains explicit:
//
//   BUFFER DOMAIN -- the document's real bytes. Identity, dirtiness, the
//   Save payload, and persistence all live here, untouched.
//   DISPLAY DOMAIN -- what the textarea holds: the LF projection the browser
//   would impose anyway, written and compared consistently so the sync
//   settles.
//
// The document's flavor is derived from its own loaded base: the FIRST line
// break names it (deterministic, and mixed-EOL strays then unify to that
// flavor on the first keystroke -- a documented choice, not an accident).
// A lone-CR-only base is deliberately left in the LF class: a textarea
// destroys lone CRs before we ever see them, and fabricating them back would
// be a guess about bytes we cannot verify -- such a file's first edit
// honestly reads dirty instead.
// ---------------------------------------------------------------------------

function eolFlavorOf(baseContent) {
  const first = /\r\n|\r|\n/.exec(baseContent);
  return first && first[0] === "\r\n" ? "crlf" : "lf";
}

// Buffer domain -> display domain: exactly the projection the textarea API
// applies itself, done eagerly so comparisons happen in ONE domain.
function displayText(content) {
  return content.replace(/\r\n?/g, "\n");
}

// Display domain -> buffer domain, re-applying the document's own flavor.
// `\r?\n` (not bare `\n`) keeps the mapping idempotent: a harness textarea
// that never normalized still converts cleanly instead of doubling CRs.
function bufferTextFor(displayValue, flavor) {
  return flavor === "crlf" ? displayValue.replace(/\r?\n/g, "\r\n") : displayValue;
}

// P3-1 (wave re-review P3 tail): the first-break rule's one honest cost,
// STATED. Unifying a mixed-EOL document on the first keystroke makes the
// buffer dirty while the textarea's display is byte-identical to the loaded
// text -- invisible dirtiness, and a Save then commits a whole-file
// line-ending diff nobody saw coming. When that is the ONLY difference (the
// display projections agree while the bytes do not), the status line says so
// in this fixed sentence instead of the bare "unsaved changes" a reader
// could never square with an unchanged-looking buffer. Fixed vocabulary, on
// purpose: it names the situation, never the content.
const EOL_ONLY_DIRTY_STATUS =
  "unsaved changes -- line endings only: this document mixed CR LF styles "
  + "and saving unifies them";

function eolOnlyDirty(buffer) {
  return buffer.dirty
    && buffer.content !== buffer.base_content
    && displayText(buffer.content) === displayText(buffer.base_content);
}

// G-1: the outline-only posture. It used to be stated twice -- on the canvas
// picker's own label and in the Document buffer's status -- and the picker's
// half retired with the picker (Brett's 2026-08-15 annotation round). The
// status is where it belonged anyway: it is a fact about the BUFFER, not about
// a control, and it is still on screen for a tile whose only editable path is
// its own primary fragment.
const OUTLINE_ONLY_STATUS =
  "no separate document on this tile — the outline is its only editable "
  + "document, and chat grounds on it";

function emptyStatement(kind) {
  return kind === "outline"
    ? "_(no outline yet -- start typing in the Outline buffer to create one)_"
    : "_(no document selected)_";
}

function unavailableStatement(kind) {
  return kind === "outline"
    ? "_(outline source unavailable -- could not load this content)_"
    : "_(document source unavailable -- could not load this content)_";
}

let mountSequence = 0;

// host: a DOM element this module owns completely from here on.
// projection: the doxbenchScopeProjection shape (staging-workbench-model.js).
// options: { loadSource(path), hash, storage, activeDocumentPath,
//            previewDelayMs, title }. `title` (when supplied) is purely
// cosmetic and falls back to projection.title -- neither is required.
export function mountDoxBenchCanvas(host, projection, options = {}) {
  const onIdentitySettled = options.onIdentitySettled;
  // R-1: an injected provider for the COMPANION working state (the chat
  // rail's), persisted in the SAME record as the buffers, and a sink for the
  // one restored beside them. The canvas never interprets the blob.
  const companionOf = options.companionOf;
  const onCompanionRestored = options.onCompanionRestored;
  // T104 F1: THE SAVE HAND-OFF. A Save that lands on a branch session moves
  // this canvas onto that ref (`rekeyTo` below), and used to tell nobody --
  // so the shell's active/source base, the session bar and the chat rail's
  // scope key all stayed on the pre-session ref and every later turn named a
  // scope the buffers had left. The canvas still re-keys ITSELF; this seam
  // exists so the composition can re-key everything else (FR-038).
  const onSaveLanded = options.onSaveLanded;
  const instanceId = "doxbench-" + (mountSequence += 1);
  const loadSource = typeof options.loadSource === "function" ? options.loadSource : null;
  // THE GATE ITSELF. Absent seam, absent Save -- and every Save-shaped control
  // below stays exactly what it was before this arm existed.
  const saveSeam = typeof options.save === "function" ? options.save : null;
  const hashOptions = typeof options.hash === "function" ? { hash: options.hash } : {};
  const storage = options.storage || null;
  const previewDelayMs = Number.isFinite(options.previewDelayMs)
    ? options.previewDelayMs
    : DEFAULT_PREVIEW_DELAY_MS;
  // How long a transient event line stays on screen (annotation round 2).
  const eventNoteMs = Number.isFinite(options.eventNoteMs)
    ? options.eventNoteMs
    : DEFAULT_EVENT_NOTE_MS;

  // ---- mutable controller state, declared before DOM construction so the --
  // ---- document picker's initial option list can read it synchronously. --
  let currentProjection = projection;
  let state = null; // the doxbench-state.js state object, once loaded
  // WHICH BUFFER the canvas presents. The context region chooses it; this is
  // where that choice lands, and `state.active_buffer` is its one persisted
  // spelling.
  let activeBuffer = BUFFER_KINDS[0];
  // WHICH VIEW of that buffer is shown. `Preview` at mount (Q5), never
  // persisted -- it is where the human is looking, not what they have.
  let activeView = "preview";
  let activeDocumentPath = "activeDocumentPath" in options
    ? options.activeDocumentPath
    : (currentProjection.active_document_candidates
      && currentProjection.active_document_candidates[0]) || null;
  let guardTargetPath = null; // set while the guard blocks a selectDocument
  let destroyed = false;
  // T104 F6-6: set when initialLoad() itself fails (state stays null). The
  // refusal every entry point states then names the FAILURE instead of a
  // "still loading" that would never come true.
  let loadFailureReason = null;
  let saving = false;         // a governed Save is in flight (wired posture only)
  const savingKinds = new Set();   // the buffers THIS Save handed over
  // Every per-buffer map below is seeded FROM the enumeration rather than from
  // the two names it happens to hold today (Phase A: no surface bakes in
  // "two").
  const perBuffer = (seed) => Object.fromEntries(
    BUFFER_KINDS.map((kind) => [kind, seed]));
  // The last verdict STATED for each buffer -- a Save's per-buffer answer, or
  // the sentence a Cancel leaves behind naming the buffer it reverted. Cleared
  // by the next local action on that buffer, because a "saved" line beside
  // freshly typed text would be stale the instant it is read.
  const statedOutcomes = perBuffer(null);
  const rememberedFocus = perBuffer(false);
  // The last selection/scroll each buffer's editor held while visible (FR-010):
  // written by applyVisibility as that editor goes hidden -- by a buffer switch
  // OR by a switch into Preview -- and read back as it returns.
  const rememberedView = perBuffer(null);
  const previewTimers = perBuffer(null);
  // What applyVisibility last applied, so a transition can be recognised: an
  // editor going hidden is when its view is captured, an editor becoming
  // visible is when focus and scroll are restored, and a preview becoming
  // visible is when a pending render must be flushed (D2).
  const editorShown = perBuffer(false);
  const previewShown = perBuffer(false);

  // ---- fixed DOM, built ONCE. Every later update mutates it in place. -----
  const titleText = options.title || currentProjection.title || null;
  const canvasLabel = "doxBench" + (titleText ? " · " + titleText : "");
  host.setAttribute("role", "region");
  // THE REGION'S NAME, and the only place this canvas states it (Brett's
  // 2026-08-15 annotation round: "why do we need this line? i do not see what
  // it is adding to our UI"). The `h2.doxbench-heading` that used to render
  // this same string above the tabs is retired: it duplicated the accessible
  // name a screen reader already announces on entering the region, cost a row
  // of a narrow panel, and named nothing the surface did not already say. The
  // two sibling regions beside it — `swb-context` and `doxbench-rail` — have
  // always been named exactly this way, with `aria-label` and no heading, so
  // this is the house idiom rather than a new one.
  host.setAttribute("aria-label", canvasLabel);

  // THE TAB ROW: the view tabs on the left, the panel's two controls on the
  // right, in ONE row (Brett's 2026-08-15 annotation round: "place the save
  // and cancel in line with the tabs"). They remain OUTSIDE both tabpanels and
  // are scoped to neither view, so each control and the answer it gets are on
  // screen whichever view the human is standing on — the ratified placement
  // rule, satisfied by a row rather than by a block of its own.
  const tabrow = el("div", "doxbench-tabrow");
  // …and the row beneath it. It used to STAND there stating each buffer's
  // state; annotation round 2 retired that (the controls carry it now), so what
  // is left is sr-only: the per-buffer live regions, the gate-absent reason,
  // and one TRANSIENT visible line for events.
  const statusbar = el("div", "doxbench-statusbar");
  // THE EVENT NOTE. An event, not standing text: a refusal or a Save that did
  // not wholly land appears here, visibly, and clears itself. Everything a
  // human can read off a control's own state -- clean, dirty, saving -- never
  // reaches it. `eventNoteMs` is injectable for the same reason
  // `previewDelayMs` is: a timer a test cannot pin is a timer a test cannot
  // trust.
  const eventNote = el("div", "doxbench-eventnote");
  eventNote.setAttribute("aria-live", "polite");
  eventNote.hidden = true;
  let eventNoteTimer = null;

  // THE VIEW TABLIST: `Editor` / `Preview`, over whichever buffer is active.
  // It answers WHICH VIEW and nothing else — the buffer choice belongs to the
  // context region, and its aria-label says so rather than claiming "buffers".
  const viewTablist = el("div", "doxbench-viewtabs");
  viewTablist.setAttribute("role", "tablist");
  viewTablist.setAttribute("aria-label", "view of the active doxBench buffer");

  const panes = el("div", "doxbench-panes");

  const viewTabButtons = {};
  const viewPaneEls = {};
  // One box per (view, buffer): the view pane shows or hides the whole VIEW,
  // and the box inside it shows or hides ONE buffer. The textareas and preview
  // containers themselves are still built exactly once and mutated afterwards.
  const bufferBoxes = { editor: {}, preview: {} };
  const textareas = {};
  const previews = {};
  const statusEls = {};

  for (const view of DOXBENCH_VIEW_TABS) {
    const viewTabId = instanceId + "-viewtab-" + view.key;
    const viewPaneId = instanceId + "-viewpane-" + view.key;

    const tabBtn = el("button", "doxbench-viewtab", view.label);
    tabBtn.type = "button";
    tabBtn.id = viewTabId;
    tabBtn.setAttribute("role", "tab");
    tabBtn.setAttribute("aria-controls", viewPaneId);
    tabBtn.addEventListener("click", () => { setActiveView(view.key); });
    // CHK007 (T100 AT measurement, 2026-08-02: FAIL — correct semantics but
    // no roving tabindex, so Arrow/Home/End moved focus nowhere). The WAI-ARIA
    // APG tablist pattern, carried over from the retired buffer tablist
    // UNCHANGED because it was measured and fixed once already: exactly ONE
    // tab is tabbable at a time (applyVisibility maintains it), Left/Right
    // (plus Up/Down, which the operator tried first) move selection with
    // focus, Home/End jump to the ends, and the arrow keys are consumed so
    // they no longer scroll the page.
    tabBtn.addEventListener("keydown", (ev) => {
      const keys = {
        ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1,
      };
      const order = DOXBENCH_VIEW_TABS.map((t) => t.key);
      let next = null;
      if (ev.key in keys) {
        const at = order.indexOf(activeView);
        next = order[(at + keys[ev.key] + order.length) % order.length];
      } else if (ev.key === "Home") {
        next = order[0];
      } else if (ev.key === "End") {
        next = order[order.length - 1];
      }
      if (next === null) return;
      ev.preventDefault();   // no page scroll from an arrow inside a tablist
      setActiveView(next);
      viewTabButtons[next].focus();
    });
    viewTablist.appendChild(tabBtn);
    viewTabButtons[view.key] = tabBtn;

    const viewPane = el("div", "doxbench-viewpane doxbench-viewpane-" + view.key);
    viewPane.id = viewPaneId;
    viewPane.setAttribute("role", "tabpanel");
    viewPane.setAttribute("aria-labelledby", viewTabId);
    // PR #196 review F5 (WCAG 2.1.1): `Preview` is the tab a mount LANDS on,
    // and it is a scrollable region whose only content is rendered Markdown --
    // no focusable node inside it at all, so a keyboard-only human could reach
    // the panel with Tab and then not scroll it. The APG's own remedy for a
    // tabpanel with no focusable content is to make the panel itself tabbable.
    // Applied to BOTH panes: `Editor` gains a harmless extra stop before its
    // textarea, and the rule stays true if a pane's content ever changes.
    viewPane.tabIndex = 0;
    panes.appendChild(viewPane);
    viewPaneEls[view.key] = viewPane;
  }

  for (const kind of BUFFER_KINDS) {
    const label = bufferLabel(kind);
    const previewId = instanceId + "-preview-" + kind;

    // VISUALLY HIDDEN, and still a live region (Brett's 2026-08-18 annotation
    // round 2: "remove these lines. the UI must be intuitive and not rely on
    // this text to inform the user"). The lines Brett is looking at are the
    // STANDING ones -- "Outline: no unsaved changes" beside "Document: no
    // unsaved changes" -- and he is right that a control's own enabled state
    // says that better than a sentence does. But these regions are not only
    // decoration: they are the per-buffer verdict surface the ratified buffer
    // contract requires a partial Save to be readable in, they are where every
    // stated refusal on this canvas lands, and they are announced. So they stay
    // in the DOM, sr-only, exactly as `doxchat-announce` does one region over --
    // the same house idiom. What a sighted human needs to SEE is the EVENT half
    // (a refusal, a Save that did not wholly land), and that goes to the
    // transient note below rather than standing here forever.
    const status = el("span",
      "doxbench-status doxbench-status-" + kind + " doxbench-sronly");
    status.setAttribute("aria-live", "polite");
    // ONE Save, still TWO answers: each buffer keeps its own status region, and
    // both are on screen at once, so the partial-success case (one buffer
    // committed, the other refused) stays separately readable with a single
    // button on the panel.
    status.setAttribute("aria-label", label + " buffer status");
    // T104 F6-2: the load posture is STATED from the first paint, in the same
    // region every other buffer fact is stated in -- this module's one idiom
    // for "why the surface refuses" (the unwired Save note works the same
    // way). syncBufferDom replaces it the moment real state exists.
    status.textContent = label + ": " + EDITOR_LOADING_REASON;

    const editorBox = el("div", "doxbench-bufferbox doxbench-bufferbox-" + kind);
    const textarea = document.createElement("textarea");
    textarea.className = "doxbench-textarea";
    textarea.setAttribute("aria-label", label + " buffer text");
    textarea.setAttribute("aria-describedby", previewId);
    // T104 F9-4 (FR-044): governed buffer text is never autofill fodder — the
    // chat rail already refuses autofill on its inputs; the canvas matches.
    textarea.setAttribute("autocomplete", "off");
    // T104 F9-2 (FR-045): the buffer's direction comes from its own bytes
    // (first strong directional character), so RTL drafts read as RTL without
    // anyone configuring anything — the chat rail's composer idiom.
    textarea.setAttribute("dir", "auto");
    // T104 F6-2: the surface is DISABLED until working state exists -- the
    // honest structural sibling of the disabled Save control: a real browser
    // then physically refuses the keystroke instead of feeding it to a
    // listener that has nothing to apply it to. syncBufferDom re-enables it
    // on the first sync (which only ever runs with state present), and a
    // failed load (F6-6) leaves it disabled beside its stated failure.
    textarea.disabled = true;
    textarea.addEventListener("input", async () => {
      // T104 F10-3: the textarea speaks the display domain (LF); the buffer
      // speaks the document's own bytes. Re-apply the loaded base's flavor
      // BEFORE the edit path hashes or persists anything.
      const result = await edit(kind, readBufferValue(kind));
      if (!result.ok) {
        // Refused honestly and VISIBLY: the human's keystroke or paste must
        // never just vanish with nothing said (CHK016/CHK019).
        status.textContent = label + ": refused -- " + result.error;
        status.classList.add("doxbench-status-error");
        stateEvent(label + ": refused -- " + result.error);
      } else {
        status.classList.remove("doxbench-status-error");
      }
    });
    textarea.addEventListener("focus", () => { rememberedFocus[kind] = true; });
    editorBox.appendChild(textarea);
    viewPaneEls.editor.appendChild(editorBox);

    const previewBox = el("div", "doxbench-bufferbox doxbench-bufferbox-" + kind);
    const preview = el("div", "doxbench-preview doxbench-preview-" + kind);
    preview.id = previewId;
    preview.setAttribute("aria-label", label + " preview");
    // T104 F9-2 (FR-045): the preview renders the SAME content-derived bytes
    // as the textarea it is a view of, so it derives its direction the same way.
    preview.setAttribute("dir", "auto");
    previewBox.appendChild(preview);
    viewPaneEls.preview.appendChild(previewBox);

    bufferBoxes.editor[kind] = editorBox;
    bufferBoxes.preview[kind] = previewBox;
    textareas[kind] = textarea;
    previews[kind] = preview;
    statusEls[kind] = status;
  }

  // THE CANVAS'S OWN DOCUMENT PICKER IS RETIRED (Brett's 2026-08-15 annotation
  // round: "we do not need this section now that the left panel will let us
  // select the active document"). The context region's docs wheel is now the
  // sole human route to a document, which is what Phase A's model asked for in
  // the first place -- left selects.
  //
  // NOTHING GUARDED WENT WITH IT. Phase A design D3 kept this picker because
  // its dirty-Document guard was load-bearing, and at the time the guard, the
  // revert and the refusal sentence lived partly in the picker's own change
  // handler. The PR #196 review moved all three INTO `selectDocument` (F4/F6):
  // one refusal vocabulary, one guard, and a reconcile that puts the context
  // region's own selection back on the document the canvas really holds. So
  // the control could go without taking a rule with it -- which is exactly the
  // order those two changes had to happen in.
  //
  // G-1 (PR #63 re-verification) survives too, and in a better place: a tile
  // whose ONLY editable path is its own primary fragment has no document to
  // pick, and that posture is STATED in the Document buffer's own status line
  // (`OUTLINE_ONLY_STATUS`) rather than as an empty control that does nothing.

  // THE STATUS BAR: one compact row under the tab row, carrying each buffer's
  // own live status region and the Save note. The per-buffer verdict surface is
  // LOAD-BEARING and had to survive the chrome's retirement intact -- a partial
  // Save (one buffer committed, the other refused) is reported per buffer by
  // the ratified buffer contract, and every stated refusal on this surface
  // lands in these same regions. What changed is that each line now NAMES its
  // buffer visibly (`statusLine` prefixes the label): stacked in the old chrome
  // they rendered as "no unsaved changesno unsaved changes", two identical
  // sentences a reader could not attribute -- which is what the annotated
  // screenshot shows.
  for (const kind of BUFFER_KINDS) statusbar.appendChild(statusEls[kind]);
  statusbar.appendChild(eventNote);

  // CANCEL -- the panel's narrow half. It is `discardBuffer` aimed at the
  // ACTIVE buffer and nothing else: discard destroys unsaved human work and
  // has no cross-buffer dependency, so a control that silently reverted a
  // buffer the human is not looking at would be this surface's one
  // irreversible surprise. It persists nothing, so the Save posture gate below
  // does not govern it.
  const cancelBtn = el("button", "doxbench-cancel", "Cancel");
  cancelBtn.type = "button";
  cancelBtn.title = CANCEL_TITLE;
  // P3-2 (wave re-review P3 tail): DISABLED from construction, like the
  // textareas (the F6-2 honest posture) -- its click handler drops cancel()'s
  // refusal object, so through the loading window (and forever after a failed
  // load, where syncBufferDom never runs) an enabled control was a silently
  // dead one. The first syncBufferDom re-derives the real enabled state.
  cancelBtn.disabled = true;
  cancelBtn.addEventListener("click", () => { cancel(); });

  // SAVE -- the panel's broad half, and semantically exactly what it already
  // was: no argument, the dirty set over the buffer enumeration, one call to
  // the seam, ordering and action choice owned by ./doxbench-save.js. The only
  // thing Phase A changed is that it is drawn once instead of twice.
  const saveBtn = el("button", "doxbench-save", "Save");
  saveBtn.type = "button";
  if (saveSeam) {
    saveBtn.title = "save this canvas's changed buffers through the existing "
      + "governance actions";
    // P3-2: the WIRED control is still not reachable before working state
    // exists -- save() refuses with the loading line and the click handler
    // drops that refusal, so the button mounts disabled like everything
    // else and the first syncBufferDom flips it live.
    saveBtn.disabled = true;
    saveBtn.setAttribute("aria-disabled", "true");
    saveBtn.addEventListener("click", () => { save(); });
  } else {
    saveBtn.disabled = true;
    saveBtn.title = SAVE_UNAVAILABLE_REASON;
    saveBtn.setAttribute("aria-disabled", "true");
  }
  const saveNoteId = instanceId + "-save-note";
  // Empty in the WIRED posture (annotation round 2 retired the sentence that
  // used to stand here) and the fixed reason where there is no gate at all --
  // which the ratified requirement needs as VISIBLE text beside the control,
  // not a hover title, because an unreachable Save is not something a disabled
  // button can tell apart from a nothing-to-save state.
  const saveNote = el("span", "doxbench-save-note",
                      saveSeam ? "" : SAVE_UNAVAILABLE_REASON);
  saveNote.hidden = !!saveSeam;
  saveNote.id = saveNoteId;
  saveBtn.setAttribute("aria-describedby", saveNoteId);
  // The two controls sit in their own group INSIDE the tab row but OUTSIDE the
  // tablist element: a button inside `role=tablist` would be announced as a tab
  // and would join the roving-tabindex arrow cycle, which is precisely the
  // confusion the two-level naming exists to prevent. The Save NOTE stays in
  // the status row, where the sentences live.
  const actions = el("div", "doxbench-actions");
  actions.append(cancelBtn, saveBtn);
  statusbar.appendChild(saveNote);

  // The document-switch guard (FR-007 / acceptance scenario 4): one
  // persistent region, built once, shown only while a dirty Document buffer
  // blocks a selectDocument call. Save is offered here too -- disabled, the
  // same fixed reason, stated as visible text -- so the guard never implies
  // an authority the surface does not have. Discard and Cancel are real,
  // keyboard-reachable buttons; a disabled control is skipped in tab order
  // by construction, so the effective reachable order is Discard then
  // Cancel. Opening the guard moves focus to Discard; resolving it (by any
  // choice that actually resolves) returns focus to the Document buffer.
  const guardHost = el("div", "doxbench-guard");
  guardHost.hidden = true;
  guardHost.setAttribute("role", "alertdialog");
  guardHost.setAttribute("aria-label", "unsaved Document changes");
  const guardStatus = el("p", "doxbench-guard-status");
  guardStatus.setAttribute("aria-live", "assertive");
  const guardSaveBtn = el("button", "doxbench-guard-save", "Save");
  guardSaveBtn.type = "button";
  if (saveSeam) {
    guardSaveBtn.title = "save the Document buffer, then continue the switch";
    guardSaveBtn.setAttribute("aria-disabled", "false");
    guardSaveBtn.addEventListener("click", () => { resolveGuard("save"); });
  } else {
    guardSaveBtn.disabled = true;
    guardSaveBtn.title = SAVE_UNAVAILABLE_REASON;
    guardSaveBtn.setAttribute("aria-disabled", "true");
  }
  const guardSaveNoteId = instanceId + "-guard-save-note";
  const guardSaveNote = el("span", "doxbench-guard-save-note",
                           saveSeam ? GUARD_SAVE_WIRED_NOTE : SAVE_UNAVAILABLE_REASON);
  guardSaveNote.id = guardSaveNoteId;
  guardSaveBtn.setAttribute("aria-describedby", guardSaveNoteId);
  const guardDiscardBtn = el("button", "doxbench-guard-discard", "Discard");
  guardDiscardBtn.type = "button";
  guardDiscardBtn.addEventListener("click", () => { resolveGuard("discard"); });
  const guardCancelBtn = el("button", "doxbench-guard-cancel", "Cancel");
  guardCancelBtn.type = "button";
  guardCancelBtn.addEventListener("click", () => { resolveGuard("cancel"); });
  guardHost.append(guardStatus, guardSaveBtn, guardSaveNote, guardDiscardBtn, guardCancelBtn);

  tabrow.append(viewTablist, actions);
  host.append(tabrow, statusbar, panes, guardHost);

  // The LOADED state's key is the authority once there is one: a Save that
  // lands on a session ref rekeys that state, and a later context refresh
  // carrying the pre-session projection must not silently undo the move.
  function scopeKey() { return state ? state.key : currentProjection.key; }

  function ownedFlag(path) {
    if (path === null) return true; // nothing to "not own" for a not-yet-created buffer
    return (currentProjection.editable_paths || []).includes(path);
  }

  function isInScope(path) {
    const contextPaths = currentProjection.context_paths || [];
    const editablePaths = currentProjection.editable_paths || [];
    return contextPaths.includes(path) || editablePaths.includes(path);
  }

  function baseRevisionOf(loaded) {
    return (loaded && loaded.revision) || currentProjection.source_revision || FALLBACK_REVISION;
  }

  // Produces a plain descriptor -- never a hashed/frozen buffer -- so the
  // ONE hashing authority stays createDoxBenchState / createBufferState.
  async function loadDescriptor(kind, path) {
    const key = scopeKey();
    const owned = ownedFlag(path);
    if (path === null) {
      return { path: null, owned, base_ref: key.ref, base_revision: baseRevisionOf(null), content: "" };
    }
    if (!loadSource) {
      return {
        path, owned, base_ref: key.ref, base_revision: baseRevisionOf(null),
        content: "", load_state: "unavailable",
      };
    }
    let loaded = null;
    try {
      loaded = await loadSource(path);
    } catch {
      loaded = null;
    }
    if (!loaded || typeof loaded.content !== "string") {
      return {
        path, owned, base_ref: key.ref, base_revision: baseRevisionOf(null),
        content: "", load_state: "unavailable",
      };
    }
    return {
      path, owned,
      base_ref: loaded.ref || key.ref,
      base_revision: baseRevisionOf(loaded),
      content: loaded.content,
    };
  }

  function persistNow() {
    if (!storage || !state) return;
    persistDoxBenchState(state, storage,
      typeof companionOf === "function" ? companionOf() : undefined);
  }

  // T104 F6-2: what an entry point states while `state` is still null -- the
  // loading line, or the load's own stated failure once there is one (F6-6).
  function unloadedReason() {
    return loadFailureReason || EDITOR_LOADING_REASON;
  }

  // T104 F10-3: the buffer-domain bytes the textarea currently represents.
  // Before state exists there is no base to take a flavor from, and every
  // entry point refuses anyway, so the identity mapping is safe.
  function readBufferValue(kind) {
    const buffer = state ? state.buffers[kind] : null;
    return bufferTextFor(
      textareas[kind].value,
      buffer ? eolFlavorOf(buffer.base_content) : "lf",
    );
  }

  function syncBufferDom(kind) {
    const buffer = state.buffers[kind];
    const textarea = textareas[kind];
    // T104 F6-2: the first sync is the moment real working state backs the
    // surface, so the mount-time disabled posture ends here (this function is
    // never reached with a null state).
    textarea.disabled = false;
    // Only reassign `.value` when it actually differs: real browsers can
    // move the caret to the end of a textarea whose `.value` is reassigned
    // even to its OWN current string, so a live-typing edit (whose DOM value
    // already matches) must never re-touch it. A programmatic edit,
    // Discard, or document switch always DOES differ, so it still syncs.
    //
    // T104 F10-3: BOTH sides of the comparison live in the display domain --
    // the textarea can only ever hold the LF projection, so comparing it
    // against raw CRLF buffer bytes could never come out equal and this sync
    // re-touched the value (and the caret) on every call, forever.
    const display = displayText(buffer.content);
    if (textarea.value !== display) textarea.value = display;
    statusEls[kind].textContent = statusLine(kind, buffer);
    statusEls[kind].classList.toggle("is-dirty", buffer.dirty);
    if (saveSeam) {
      statusEls[kind].setAttribute("aria-busy", savingKinds.has(kind) ? "true" : "false");
    }
    syncPanelControls();
  }

  // The PANEL's own controls answer for the whole canvas (Save) and for the
  // ACTIVE buffer (Cancel), so their posture is derived ONCE here rather than
  // once per buffer -- with one of each on screen, deriving it per buffer would
  // just be the last buffer in the loop winning. Called by syncBufferDom and by
  // every change of which buffer is active.
  function syncPanelControls() {
    if (!state) return;   // the mount-time disabled posture stands until a load
    // THE CONTROLS CARRY THE STATE (Brett's 2026-08-18 annotation round 2:
    // "the UI must be intuitive and not rely on this text to inform the user").
    // "Nothing is dirty" used to be a SENTENCE standing under the tab row; it is
    // a control state, and the control says it better: Save is reachable exactly
    // when there is something to save, Cancel exactly when there is something to
    // revert. A human reads that off the row without reading anything.
    const anythingDirty = BUFFER_KINDS.some((kind) => state.buffers[kind].dirty);
    const activeDirty = state.buffers[activeBuffer].dirty;
    if (saveSeam) {
      // An in-flight Save still takes both away -- that posture is about the
      // bytes being in flight, not about what is dirty.
      saveBtn.disabled = saving || !anythingDirty;
      saveBtn.setAttribute("aria-disabled",
                           saving || !anythingDirty ? "true" : "false");
      cancelBtn.disabled = saving || !activeDirty;
      guardSaveBtn.disabled = saving;
      guardDiscardBtn.disabled = saving;
      guardCancelBtn.disabled = saving;
    } else {
      // No gate at all: Save was never reachable here and stays that way, with
      // its reason beside it as visible text. Cancel is local and follows the
      // active buffer exactly as it always did.
      cancelBtn.disabled = !activeDirty;
    }
  }

  // ONE TRANSIENT VISIBLE LINE, for the half of the retired status text a human
  // must not miss: an EVENT. A refusal, or a Save that did not wholly land --
  // never a state a control already shows. It clears itself, because standing
  // text is what annotation round 2 removed; the sr-only per-buffer regions
  // keep the durable, per-buffer detail for assistive technology and for the
  // partial-Save contract.
  function stateEvent(text) {
    if (destroyed || !text) return;
    if (eventNoteTimer !== null) clearTimeout(eventNoteTimer);
    eventNote.textContent = String(text);
    eventNote.hidden = false;
    eventNoteTimer = setTimeout(() => {
      eventNoteTimer = null;
      eventNote.textContent = "";
      eventNote.hidden = true;
    }, eventNoteMs);
  }

  // The status region states, in order: what a Save is doing to this buffer
  // right now, what the last Save said about it, and whether it currently holds
  // unsaved changes. Each buffer gets its OWN sentence -- a partial outcome
  // reported as one blended verdict would be exactly the lie FR-035 forbids.
  function statusLine(kind, buffer) {
    const dirtyText = bufferStatusText(kind, buffer);
    // EVERY line NAMES ITS BUFFER (Brett's 2026-08-15 annotation round). The
    // two regions used to sit stacked in the chrome with no visible label, so a
    // clean canvas rendered "no unsaved changes" twice with nothing to
    // attribute either sentence to -- and a PARTIAL Save, whose whole point is
    // that one buffer committed and the other refused, was exactly the case
    // that unlabelled pair could not report. The accessible name carried the
    // buffer already; now the visible text does too.
    const prefix = bufferLabel(kind) + ": ";
    if (savingKinds.has(kind)) return prefix + "saving this buffer -- " + dirtyText;
    const outcome = statedOutcomes[kind];
    return prefix + (outcome ? outcome + " -- " + dirtyText : dirtyText);
  }

  // One buffer's verdict, as the sentence a human reads. Never a status code on
  // its own: "refused" without the reason is not a report.
  function saveOutcomeSentence(row) {
    const message = typeof row.message === "string" && row.message ? row.message : null;
    if (row.status === "committed") {
      return "saved as " + (row.action || "the existing action")
        + " on " + (row.ref || "the session branch");
    }
    if (row.status === "refused") {
      return "Save refused -- " + (message || "no reason was reported");
    }
    if (row.status === "not_attempted") {
      return "Save not attempted -- " + (message || "an earlier buffer did not land");
    }
    return "nothing to save in this buffer";
  }

  function forgetStatedOutcome(kind) {
    if (statedOutcomes[kind] !== null) statedOutcomes[kind] = null;
  }

  // The status is a function of CONTENT first: an unsaved-changes fact
  // always wins once there is any typed text, even for a buffer that
  // started `empty` or `unavailable` (the state module preserves that
  // load_state across every edit on purpose). An `unavailable` origin still
  // stays stated, alongside the dirty fact rather than instead of it -- a
  // later Save would still need to know the loaded base is unresolved.
  function bufferStatusText(kind, buffer) {
    if (buffer.content === "") {
      if (buffer.load_state === "empty") {
        if (kind === "outline") return "no outline yet -- start typing to create one";
        // G-1: "no document selected" is only true where one COULD be.
        return (currentProjection.active_document_candidates || []).length
          ? "no document selected"
          : OUTLINE_ONLY_STATUS;
      }
      if (buffer.load_state === "unavailable") {
        return "source unavailable -- could not load this " + kind;
      }
      return buffer.dirty ? "unsaved changes" : "no unsaved changes";
    }
    // P3-1: display-invisible dirtiness gets its own sentence (only reachable
    // here -- an empty content can never be display-identical to a dirty base).
    const dirtyText = buffer.dirty
      ? (eolOnlyDirty(buffer) ? EOL_ONLY_DIRTY_STATUS : "unsaved changes")
      : "no unsaved changes";
    if (buffer.load_state === "unavailable") {
      return dirtyText + " (source unavailable -- the original could not be loaded)";
    }
    return dirtyText;
  }

  // The preview is ALSO a function of CONTENT first, for the identical
  // reason: once there is any typed text, that text renders through
  // mountSafeMarkdown, no matter what load_state says.
  function renderPreviewNow(kind) {
    const buffer = state.buffers[kind];
    let text;
    if (buffer.content !== "") {
      text = buffer.content;
    } else if (buffer.load_state === "empty") {
      text = emptyStatement(kind);
    } else if (buffer.load_state === "unavailable") {
      text = unavailableStatement(kind);
    } else {
      text = "";
    }
    mountSafeMarkdown(previews[kind], text);
  }

  // Live typing is debounced; every other buffer-content change (initial
  // load, Discard, a document switch) renders at once -- there is nothing to
  // debounce about a single discrete action.
  function schedulePreview(kind) {
    if (previewTimers[kind]) clearTimeout(previewTimers[kind].timer);
    let resolveFn;
    const promise = new Promise((resolve) => { resolveFn = resolve; });
    const timer = setTimeout(() => {
      previewTimers[kind] = null;
      renderPreviewNow(kind);
      resolveFn();
    }, previewDelayMs);
    previewTimers[kind] = { timer, resolve: resolveFn, promise };
    return promise;
  }

  function flushOne(kind) {
    const pending = previewTimers[kind];
    if (!pending) return Promise.resolve();
    clearTimeout(pending.timer);
    previewTimers[kind] = null;
    renderPreviewNow(kind);
    pending.resolve();
    return Promise.resolve();
  }

  function flushPreview() {
    return Promise.all(BUFFER_KINDS.map((kind) => flushOne(kind)));
  }

  // A buffer's EDITOR is on screen only while that buffer is active AND the
  // `Editor` view tab is selected; its PREVIEW only while it is active and
  // `Preview` is selected. Two axes, one predicate each -- everything below
  // (focus, scroll capture, the D2 flush) keys on these rather than on the
  // buffer alone, which is what made the old single-axis bookkeeping correct
  // when there was only one axis.
  function editorVisible(kind) {
    return kind === activeBuffer && activeView === "editor";
  }

  function previewVisible(kind) {
    return kind === activeBuffer && activeView === "preview";
  }

  // ONE function owns what is on screen, because the two axes interact: which
  // buffer is active, and which view of it is selected. Ordering is
  // load-bearing throughout and each step says why.
  function applyVisibility() {
    // 1. CAPTURE FIRST. FR-010's selection/scroll clause (T104: `viewState` was
    //    exported with no production caller and NOTHING ever wrote the values
    //    back): hiding a pane drops its layout box, and the browser drops the
    //    textarea's scroll offset with it -- so the view is captured on the way
    //    out, BEFORE anything below is hidden, and re-applied on the way back.
    for (const kind of BUFFER_KINDS) {
      if (editorShown[kind] && !editorVisible(kind)) {
        rememberedView[kind] = viewState(kind);
      }
    }
    // 2. D2: a preview about to BECOME visible is brought up to the buffer's
    //    current content first, so the switch never displays a rendering the
    //    debounce had not yet applied. The existing flush, the existing single
    //    rendering path -- no second pipeline. Switching into `Editor` needs no
    //    such step: raw text is never debounced.
    for (const kind of BUFFER_KINDS) {
      if (previewVisible(kind) && !previewShown[kind]) flushOne(kind);
    }
    // 3. The view tabs. Selection has exactly ONE spelling: aria-selected. The
    //    stylesheet's selected-tab rule keys on it directly (T104 F9-6 retired
    //    the parallel "-active" shadow class the old buffer strip toggled in
    //    lockstep: a second spelling of one state that could only ever drift).
    for (const view of DOXBENCH_VIEW_TABS) {
      const selected = view.key === activeView;
      viewTabButtons[view.key].setAttribute("aria-selected", String(selected));
      // CHK007 roving tabindex: the selected tab is the ONLY tabbable one, so
      // Tab enters the strip once and the arrows move within it (APG).
      viewTabButtons[view.key].tabIndex = selected ? 0 : -1;
      viewPaneEls[view.key].hidden = !selected;
    }
    // 4. Which buffer each view pane is showing.
    for (const kind of BUFFER_KINDS) {
      const isActive = kind === activeBuffer;
      bufferBoxes.editor[kind].hidden = !isActive;
      bufferBoxes.preview[kind].hidden = !isActive;
    }
    // 5. RESTORE LAST, and only for an editor that just appeared. A hidden pane
    //    cannot hold real focus; a shown one that previously held it gets it
    //    back, and one that never held focus never steals it. Scroll is
    //    re-applied after focus() because focus may scroll the caret into view
    //    and must not win over the human's place.
    for (const kind of BUFFER_KINDS) {
      const nowVisible = editorVisible(kind);
      if (nowVisible && !editorShown[kind]) {
        if (rememberedFocus[kind]) textareas[kind].focus();
        const view = rememberedView[kind];
        if (view) {
          const textarea = textareas[kind];
          if (typeof textarea.setSelectionRange === "function") {
            textarea.setSelectionRange(view.selectionStart, view.selectionEnd);
          } else {
            // the test shim's textarea carries plain properties
            textarea.selectionStart = view.selectionStart;
            textarea.selectionEnd = view.selectionEnd;
          }
          textarea.scrollTop = view.scrollTop;
        }
      }
      editorShown[kind] = nowVisible;
      previewShown[kind] = previewVisible(kind);
    }
  }

  // WHICH BUFFER. The context region calls this (through the composition); the
  // view tabs never do -- they answer which VIEW, and a realization that let
  // them choose a buffer is exactly what the delta refuses.
  function setActiveBuffer(kind) {
    if (destroyed) return activeBuffer;
    if (!BUFFER_KINDS.includes(kind)) {
      // Reads the enumeration rather than naming today's two buffers, so the
      // refusal stays true if the buffer contract ever widens.
      throw new TypeError("setActiveBuffer kind must name a declared buffer");
    }
    if (activeBuffer === kind) return activeBuffer;
    activeBuffer = kind;
    if (state) state = adoptActiveBuffer(state, kind);
    applyVisibility();
    syncPanelControls();   // Cancel is aimed at the buffer that just changed
    persistNow();
    return activeBuffer;
  }

  // WHICH VIEW of that buffer. No state authority is involved: this is where
  // the human is looking, not what they have, so nothing is persisted.
  function setActiveView(key) {
    if (destroyed) return activeView;
    if (!DOXBENCH_VIEW_TABS.some((view) => view.key === key)) {
      throw new TypeError("setActiveView key must name a declared view tab");
    }
    if (activeView === key) return activeView;
    activeView = key;
    applyVisibility();
    return activeView;
  }

  // Putting the human back on a buffer's own TEXT after the document-switch
  // guard closes: the `Editor` view is selected first, because focus on a
  // hidden pane is not focus at all in a real document -- and for the same
  // reason the requested buffer is only focused when it IS the buffer on
  // screen, the active one standing in otherwise.
  //
  // WHAT THIS MUST NOT DO IS RE-BIND (PR #196 review F1). It used to call
  // setActiveBuffer, which made CANCEL -- the "no, leave it alone" choice --
  // silently move the chat's working context onto the document and PERSIST it:
  // a human on the outline who declined a document switch came back bound to
  // the document. Resolving the guard is a decision about a SWITCH, never
  // about which buffer the chat works on. Where a switch really did happen,
  // `switchDocument` has already bound to it, so nothing is lost here.
  function focusBufferEditor(kind) {
    setActiveView("editor");
    const target = editorVisible(kind) ? kind : activeBuffer;
    textareas[target].focus();
  }

  function showGuard(path) {
    guardTargetPath = path;
    guardHost.hidden = false;
    // Both choices are named either way. The unwired sentence still carries the
    // fixed reason, because there Save is not a choice at all; the wired one
    // stops claiming it, because there it is.
    guardStatus.textContent = "The Document buffer has unsaved changes. Switching to "
      + basename(path) + (saveSeam
        ? " needs Save or Discard."
        : " needs Save (" + SAVE_UNAVAILABLE_REASON + ") or Discard.");
    guardDiscardBtn.focus();
  }

  function hideGuard() {
    guardHost.hidden = true;
    guardStatus.textContent = "";
  }

  async function edit(kind, text) {
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    // The bytes handed to the seam are the bytes the verdict will describe, so
    // they may not move underneath it. Refused visibly, like every other
    // refused edit -- the keystroke never just vanishes.
    if (saving) return { ok: false, error: EDIT_DURING_SAVE_REASON };
    // T104 F6-2/F6-6: no working state yet (or ever, after a failed load) --
    // a stated refusal, never a TypeError off `state.buffers` below.
    if (!state) return { ok: false, error: unloadedReason() };
    forgetStatedOutcome(kind);
    const before = state.buffers[kind];
    const pending = beginBufferEdit(before, text, hashOptions);
    state = replaceBuffer(state, pending.buffer);
    syncBufferDom(kind);
    let completion;
    try {
      completion = await pending.completion;
    } catch (error) {
      // P3-10: the corpse check comes FIRST, same as the settle path below --
      // a destroy that landed while this hash was in flight already persisted
      // its own final record, and a rollback here would mutate and re-sync a
      // torn-down mount.
      if (destroyed) return { ok: false, error: DESTROYED_REASON };
      // Refused honestly: never a silent crash, never a corrupted buffer. The
      // buffer keeps its previous content, hash, and dirty flag exactly --
      // but only while THIS edit is still the live one. The refusal path is
      // subject to the same staleness rule as the settle below: if a newer
      // edit, Discard, or document switch landed while this hash was in
      // flight, restoring `before` here would clobber that newer work, which
      // is precisely the bug the live-buffer pairing exists to prevent. So the
      // rollback is guarded by the same generation comparison.
      if (state.buffers[kind].hash_generation === pending.buffer.hash_generation) {
        state = replaceBuffer(state, before);
        syncBufferDom(kind);
      }
      const message = error instanceof ContentEncodingError || error instanceof ContentSizeError
        ? error.message
        : "could not process this edit -- " + (error && error.message ? error.message : "unknown error");
      return { ok: false, error: message };
    }
    // P3-10 (wave re-review P3 tail): a hash that settles AFTER destroy()
    // stops here, before any persist or notification. destroy() ends in its
    // OWN persistNow (its last legitimate write, made while `destroyed` is
    // already true -- which is why this guard lives on the settle path and
    // not inside persistNow itself), and the FR-039 clear may then remove
    // that record; letting this continuation run re-persisted the cleared
    // record under the dead key and fired a late onIdentitySettled into a
    // torn-down composition.
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    // Paired against the LIVE buffer, never the snapshot this edit started
    // from -- that snapshot's own generation would trivially always match
    // its own completion, defeating the staleness check entirely (a real
    // bug this slice once had). A newer Discard, edit, or document switch
    // that landed while this hash was in flight now correctly wins: this
    // completion is simply dropped when `settled.applied` is false.
    const settled = settleBufferHash(state.buffers[kind], completion);
    if (settled.applied) {
      state = replaceBuffer(state, settled.buffer);
      syncBufferDom(kind);
      schedulePreview(kind);
      persistNow();
      // T100 P1-A: tell the composition a buffer identity moved, so the
      // chat rail can refresh proposal CURRENCY in the rendered DOM (the
      // model rule existed; this is the missing view wiring).
      if (typeof onIdentitySettled === "function") {
        onIdentitySettled(kind, settled.buffer.current_hash);
      }
    }
    return { ok: true, error: null };
  }

  function discard(kind) {
    if (destroyed) return Promise.resolve({ ok: false, error: DESTROYED_REASON });
    if (saving) return Promise.resolve({ ok: false, error: SAVE_BUSY_REASON });
    // T104 F6-2/F6-6: the same stated refusal as edit() -- there is no buffer
    // to restore before the load settles.
    if (!state) return Promise.resolve({ ok: false, error: unloadedReason() });
    forgetStatedOutcome(kind);
    const discarded = discardBuffer(state.buffers[kind]);
    state = replaceBuffer(state, discarded);
    syncBufferDom(kind);
    renderPreviewNow(kind);
    persistNow();
    // T104 F6-1: Discard MOVES the buffer's identity (current_hash goes back
    // to the base), so the composition must hear it exactly like an edit --
    // otherwise the rail's proposal cards keep 'current' + an enabled Apply
    // against text the buffer no longer holds.
    if (typeof onIdentitySettled === "function") {
      onIdentitySettled(kind, discarded.current_hash);
    }
    return Promise.resolve({ ok: true });
  }

  // CANCEL, the panel's one discard. It is `discard` aimed at the ACTIVE buffer
  // and nothing else -- no whole-canvas reversal, no force path, no second
  // write route (it writes nothing at all) -- and it SAYS which buffer it
  // reverted, because a control that could have been aimed at either one owes
  // the human that sentence. The identity notification rides `discard`, so a
  // Cancel refreshes proposal currency exactly as the guard's Discard does.
  async function cancel() {
    const kind = activeBuffer;
    const result = await discard(kind);
    if (!result.ok) return { ...result, kind };
    statedOutcomes[kind] = "Cancel reverted the " + bufferLabel(kind)
      + " buffer to its last loaded or saved text";
    syncBufferDom(kind);
    return { ok: true, kind };
  }

  // ---- the governed Save, entirely behind the posture gate ----------------

  // What one changed buffer is handed over as. The seam is given FACTS about the
  // buffer and no instructions: which existing action to use, and in which
  // order, are the orchestrator's answers (./doxbench-save.js), and whether the
  // write is permitted at all is the gate's.
  function bufferRequestRow(kind) {
    const buffer = state.buffers[kind];
    return {
      kind,
      path: buffer.path,
      content: buffer.content,
      base_ref: buffer.base_ref,
      base_revision: buffer.base_revision,
      base_hash: buffer.base_hash,
      // T100 P1-B (run-2 blocker): the SETTLED identity must travel with the
      // row — omitting it made planRow read `current_hash: undefined` and
      // refuse EVERY dirty buffer as unsettled, on every topic, forever.
      current_hash: buffer.current_hash,
      hash_pending: buffer.hash_pending,
      dirty: buffer.dirty,
      // PRESENTATION INPUT ONLY: whether this console is showing the buffer as
      // the opened tile's own material. It is not permission and is never
      // treated as any -- the gate answers ownership from its own rule for every
      // request it receives (FR-036).
      owned: buffer.owned,
    };
  }

  function unchangedRow(kind) {
    return {
      kind, status: "unchanged", action: null, ref: null, revision: null,
      content_hash: null, message: null,
    };
  }

  function outcomeRowsOf(outcome) {
    return outcome && Array.isArray(outcome.buffers) ? outcome.buffers : [];
  }

  function outcomeReasonFor(kind, outcome) {
    for (const row of outcomeRowsOf(outcome)) {
      if (row && row.kind === kind) return saveOutcomeSentence(row) + ".";
    }
    return (outcome && outcome.reason) || "the Save reported no verdict for it.";
  }

  // A Save that landed on a branch session moves this canvas's working state
  // onto that ref and takes the pre-session key away, so a later restore cannot
  // resurrect pre-session text over governed material (FR-038, FR-039).
  function rekeyTo(ref) {
    const previous = scopeKey();
    if (!ref || ref === previous.ref) return;
    let next;
    try {
      next = rekeyDoxBenchState(state, { ...previous, ref });
    } catch {
      return;   // a key the state module refuses is never forced through
    }
    state = next;
    currentProjection = { ...currentProjection, key: next.key };
    if (storage) clearDoxBenchSession(previous, storage);
    persistNow();
  }

  // Persist every changed buffer through the injected seam, and report what it
  // said -- per buffer, truthfully, advancing only the bases that landed.
  async function save() {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (!saveSeam) return { status: "refused", reason: SAVE_UNAVAILABLE_REASON };
    if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
    // T104 F6-2/F6-6: nothing loaded means nothing to hand the seam.
    if (!state) return { status: "refused", reason: unloadedReason() };
    const changed = BUFFER_KINDS.filter((kind) => state.buffers[kind].dirty);
    if (!changed.length) {
      // Nothing to persist reaches no governance action at all: the seam is not
      // called in order to discover it had nothing to do.
      for (const kind of BUFFER_KINDS) {
        statedOutcomes[kind] = saveOutcomeSentence(unchangedRow(kind));
        syncBufferDom(kind);
      }
      return {
        status: "unchanged", reason: null,
        buffers: BUFFER_KINDS.map(unchangedRow),
      };
    }
    saving = true;
    for (const kind of changed) savingKinds.add(kind);
    for (const kind of BUFFER_KINDS) {
      forgetStatedOutcome(kind);
      syncBufferDom(kind);      // states the busy fact; moves no focus
    }
    let outcome = null;
    let failure = null;
    try {
      outcome = await saveSeam({
        key: scopeKey(),
        buffers: changed.map(bufferRequestRow),
      });
    } catch (error) {
      failure = (error && error.message) || "unknown error";
    } finally {
      saving = false;
      savingKinds.clear();
    }
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (failure !== null) {
      // A seam that threw persisted nothing this canvas can see, so no base
      // moves and every buffer it was handed says what happened.
      const reason = "the Save seam failed -- " + failure;
      for (const kind of changed) statedOutcomes[kind] = "Save refused -- " + reason;
      for (const kind of BUFFER_KINDS) syncBufferDom(kind);
      stateEvent("Save refused -- " + reason);
      return { status: "refused", reason };
    }
    let landedRef = null;
    // T104 F6-1: the buffers whose base actually ADVANCED through
    // adoptSavedBase -- exactly the identities the composition must re-score
    // proposal currency against, and ONLY those (a refused buffer's identity
    // did not move, so no notification may claim it did).
    const adoptedKinds = [];
    for (const row of outcomeRowsOf(outcome)) {
      if (!row || !BUFFER_KINDS.includes(row.kind)) continue;
      if (row.status === "committed") {
        try {
          state = replaceBuffer(state, adoptSavedBase(state.buffers[row.kind], row));
          adoptedKinds.push(row.kind);
          if (landedRef === null && typeof row.ref === "string") landedRef = row.ref;
        } catch (error) {
          // A commit whose reported identity the state module refuses is NOT
          // adopted: the buffer keeps its text and its dirty flag, and the
          // human is told, rather than being handed a base nothing can verify.
          statedOutcomes[row.kind] = "Save reported a commit this canvas could not "
            + "adopt -- " + ((error && error.message) || "unknown error")
            + "; this buffer keeps its unsaved text";
          stateEvent(bufferLabel(row.kind) + ": " + statedOutcomes[row.kind]);
          continue;
        }
      }
      statedOutcomes[row.kind] = saveOutcomeSentence(row);
      // A committed buffer needs no event: Save going disabled and the buffer
      // going clean IS the report. Anything else -- refused, not attempted, a
      // commit this canvas could not adopt -- is exactly what a human must not
      // miss, so it takes the transient line as well as its own sr-only region.
      if (row.status !== "committed") {
        stateEvent(bufferLabel(row.kind) + ": " + saveOutcomeSentence(row));
      }
    }
    const previousRef = scopeKey().ref;
    if (landedRef !== null) rekeyTo(landedRef);
    for (const kind of BUFFER_KINDS) syncBufferDom(kind);
    persistNow();
    // T104 F6-1: adoption moved these buffers onto the server-reported
    // identity, so the composition hears it AFTER adoptSavedBase (and the
    // rekey) landed -- with the post-transition hash, the same shape edit()
    // reports.
    if (typeof onIdentitySettled === "function") {
      for (const kind of adoptedKinds) {
        onIdentitySettled(kind, state.buffers[kind].current_hash);
      }
    }
    // T104 F1: hand the landed ref to the composition, AFTER this canvas has
    // adopted it and persisted under it, and only when it actually moved.
    // Awaited so the Save is not reported settled while half the page is
    // still on the old key; contained, because a composition that fails to
    // re-key must never turn a landed governance action into a failure.
    if (landedRef !== null && landedRef !== previousRef
        && typeof onSaveLanded === "function") {
      try {
        await onSaveLanded(landedRef, outcome);
      } catch (unused) {
        // the seam's own detail is dropped unread; the Save still landed
      }
    }
    return outcome;
  }

  async function switchDocument(path) {
    // W-8 (wave re-review): the guard's Save arm awaits a Save whose
    // onSaveLanded hand-off can REMOUNT this canvas (the shell's recanvas on
    // a key change destroys the controller). Continuing here on the corpse
    // mutated state, PERSISTED under the rekeyed session key after destroy()
    // had written its own record — a reload in that window resurrected the
    // wrong active document — and fired a late onIdentitySettled into a
    // torn-down composition. Checked at entry AND after the awaited loads,
    // because the destroy can land during either window.
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    forgetStatedOutcome("document");
    // PR #196 review F6: the load is CONTAINED. `createBufferState` genuinely
    // rejects -- a document past the byte bound raises ContentSizeError, an
    // undecodable one ContentEncodingError -- and every caller here reaches
    // this through a click handler that drops the returned promise, so a
    // rejection dead-lettered as an unhandled rejection: nothing said, and the
    // control that asked for the switch left showing a document that never
    // loaded. Contained into the SAME stated refusal every other selection
    // failure speaks, which is also what lets the context region resync.
    // Nothing has been replaced at this point, so the buffer is untouched.
    let buffer;
    try {
      const descriptor = await loadDescriptor("document", path);
      buffer = await createBufferState(
        { kind: "document", repository: scopeKey().repository, ...descriptor },
        hashOptions,
      );
    } catch (error) {
      if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
      // Size and encoding failures speak the state module's own message --
      // byte counts and classes only, NEVER document text (the non-echoing
      // rule); anything else gets the fixed generic sentence.
      return refuseSelection(
        error instanceof ContentEncodingError || error instanceof ContentSizeError
          ? error.message
          : "this document could not be loaded",
      );
    }
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    state = replaceBuffer(state, buffer);
    activeDocumentPath = path;
    // PR #196 review F7: the remembered caret and scroll belong to the
    // document that just LEFT. Re-applying them to whatever the next document
    // happens to be puts the human at an offset with no relationship to the
    // text under it (and, past the new document's end, at a caret the browser
    // silently clamps). A whole-buffer replacement has no view to remember, so
    // the entry is dropped rather than carried across.
    rememberedView.document = null;
    // Phase A: loading a document IS binding to it. The canvas presents the
    // active buffer and the chat works on it, so a switch that left the outline
    // active would show one thing and edit another.
    setActiveBuffer("document");
    syncBufferDom("document");
    renderPreviewNow("document");
    persistNow();
    // T104 F6-1: a switch replaces the WHOLE Document buffer, the largest
    // identity move of all -- the composition hears the new buffer's settled
    // identity so stale proposal cards drop their 'current' claim.
    if (typeof onIdentitySettled === "function") {
      onIdentitySettled("document", buffer.current_hash);
    }
    return { status: "switched", reason: null };
  }

  // ONE refusal vocabulary for BOTH routes into selectDocument -- the context
  // region's scoped docs selection and this module's own picker. The sentence
  // is stated HERE rather than at either caller, so neither can drift and
  // neither can refuse silently (CHK016/CHK019). "blocked" is deliberately not
  // routed through it: the guard IS its own statement.
  function refuseSelection(reason) {
    const sentence = bufferLabel("document") + ": refused -- " + reason;
    if (statusEls.document) statusEls.document.textContent = sentence;
    stateEvent(sentence);
    return { status: "refused", reason };
  }

  async function selectDocument(path) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (saving) return refuseSelection(SAVE_BUSY_REASON);
    // T104 F6-2/F6-6: refused BEFORE the unchanged/scope answers -- with no
    // state there is no dirty check to run and nothing to switch away from,
    // and "unchanged" would be a claim about a buffer that does not exist.
    if (!state) return refuseSelection(unloadedReason());
    if (path === activeDocumentPath) {
      // Already loaded, so nothing switches -- but choosing it is still an act
      // of BINDING, and the chat follows the active buffer.
      setActiveBuffer("document");
      return { status: "unchanged", reason: null };
    }
    if (path !== null && !isInScope(path)) {
      // FR-007: "the explicitly selected SCOPED document" -- a path this
      // scope never declared (neither context nor editable) is refused
      // outright, never loaded and never silently substituted.
      return refuseSelection("out_of_scope");
    }
    if (state.buffers.document.dirty) {
      showGuard(path);
      return { status: "blocked", reason: "dirty_document" };
    }
    return switchDocument(path);
  }

  async function resolveGuard(choice) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    // T104 F6-2/F6-6: the guard can only ever OPEN over a dirty loaded
    // buffer, but the method is public -- refuse rather than let the save arm
    // below dereference a null state.
    if (!state) return { status: "refused", reason: unloadedReason() };
    if (choice === "save") {
      if (!saveSeam) {
        // MUST refuse and change nothing -- no switch, no persistence, and the
        // guard stays open: the human still has to choose Discard or Cancel.
        return { status: "refused", reason: SAVE_UNAVAILABLE_REASON };
      }
      if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
      const outcome = await save();
      // W-8: the Save above may have triggered the shell's remount (its
      // onSaveLanded hand-off destroys this controller when the key moves).
      // The corpse must stop HERE — the fresh mount owns everything after.
      if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
      if (state.buffers.document.dirty) {
        // The Document did not land, so there is nothing to switch away from
        // safely: the guard stays open, states WHY in its own assertive region,
        // and puts focus back on the choice that can still resolve it.
        const reason = outcomeReasonFor("document", outcome);
        guardStatus.textContent = "Save did not land the Document buffer: " + reason
          + " It still has unsaved changes -- choose Discard to drop them, or "
          + "Cancel to keep editing.";
        guardDiscardBtn.focus();
        return { status: "refused", reason };
      }
      if (!guardTargetPath) {
        hideGuard();
        return { status: outcome.status, reason: null };
      }
      const target = guardTargetPath;
      guardTargetPath = null;
      hideGuard();
      const switched = await switchDocument(target);
      focusBufferEditor("document");
      return switched;
    }
    if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
    if (!guardTargetPath) {
      hideGuard();
      return { status: "cancelled", reason: null };
    }
    if (choice === "cancel") {
      hideGuard();
      guardTargetPath = null;
      focusBufferEditor("document");
      return { status: "cancelled", reason: null };
    }
    if (choice === "discard") {
      const target = guardTargetPath;
      guardTargetPath = null;
      hideGuard();
      await discard("document");
      const result = await switchDocument(target);
      focusBufferEditor("document");
      return result;
    }
    throw new TypeError('resolveGuard choice must be "save", "cancel", or "discard"');
  }

  async function refreshContext(nextProjection) {
    if (nextProjection) currentProjection = nextProjection;
    // Buffer text, focus, selection, and scroll are untouched by a
    // docs/lens/context refresh (FR-010) -- only later ownership/path lookups
    // consult the newer projection.
  }

  function viewState(kind) {
    const textarea = textareas[kind];
    return {
      selectionStart: textarea.selectionStart,
      selectionEnd: textarea.selectionEnd,
      scrollTop: textarea.scrollTop,
      focused: globalThis.document.activeElement === textarea,
    };
  }

  function elements() {
    return {
      textarea: (kind) => textareas[kind] || null,
      preview: (kind) => previews[kind] || null,
      // A VIEW tab, keyed by view -- the buffer tablist it replaced is gone, so
      // there is nothing to look up by buffer kind here any more.
      viewTab: (key) => viewTabButtons[key] || null,
      // ONE of each, so neither takes an argument: asking for "the Save of the
      // outline" is a question the panel no longer has an answer to.
      save: () => saveBtn,
      cancel: () => cancelBtn,
      guard: () => guardHost,
      // additive, beyond the fixed minimum set: a per-buffer status region
      // and the document picker, both needed to test the fix round's
      // visible-refusal and scope-guard behaviour.
      status: (kind) => statusEls[kind] || null,
      // the transient visible line annotation round 2 introduced, so a test can
      // measure that an EVENT was shown without waiting on its own timer
      eventNote: () => eventNote,
    };
  }

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    for (const kind of BUFFER_KINDS) {
      if (previewTimers[kind]) {
        clearTimeout(previewTimers[kind].timer);
        previewTimers[kind] = null;
      }
    }
    if (eventNoteTimer !== null) {
      clearTimeout(eventNoteTimer);
      eventNoteTimer = null;
    }
    persistNow();
  }

  async function initialLoad() {
    // T104 F6-6: the whole load is contained. `createDoxBenchState` (and the
    // hashing inside it) can genuinely fail -- a document past the byte bound
    // raises ContentSizeError -- and the returned ready promise has no
    // production consumer, so an uncaught rejection here used to dead-letter:
    // `state` stayed null forever and the canvas rendered as a silently
    // broken editor whose every keystroke threw. The catch below turns that
    // into the stated refuse-visibly posture instead (same shape as the
    // loading window, with the failure named).
    try {
      const key = scopeKey();
      let restored = null;
      let restoredCompanion = null;
      if (storage) {
        try {
          restored = await restoreDoxBenchState(key, storage, hashOptions);
          if (restored && restored.companion) restoredCompanion = restored.companion;
        } catch {
          restored = null;
        }
      }
      if (restored) {
        state = restored;
        // The RESTORED selection wins: which buffer was active is working
        // state, persisted with the buffers. Which VIEW was showing is not --
        // `Preview` is where every mount opens.
        activeBuffer = restored.active_buffer;
        activeDocumentPath = restored.buffers.document.path;
      } else {
        const [outline, documentDescriptor] = await Promise.all([
          loadDescriptor("outline", currentProjection.outline_path),
          loadDescriptor("document", activeDocumentPath),
        ]);
        state = await createDoxBenchState(
          { key, active_buffer: activeBuffer, outline, document: documentDescriptor },
          hashOptions,
        );
      }
      // R-1, ordering fixed (T104 F1, doxbench-editor.js:1022): the companion
      // blob is handed over AFTER `state` is assigned and still BEFORE the first
      // render, so the rail's restored proposals are re-scored against these
      // restored bytes. It used to fire while `state` was still null, so the
      // shell's `applyPendingCompanion()` read a null canvas state, bailed, and
      // left the blob pending — the restored subject, model, composer,
      // transcript and PROPOSALS were then only ever applied if a non-empty
      // model catalog happened to load afterwards.
      if (restoredCompanion && typeof onCompanionRestored === "function") {
        onCompanionRestored(restoredCompanion);
      }
      applyVisibility();
      for (const kind of BUFFER_KINDS) {
        syncBufferDom(kind);
        renderPreviewNow(kind);
      }
    } catch (error) {
      // The stated failure. Size and encoding failures speak the state
      // module's own message -- byte counts and classes only, NEVER document
      // text (the non-echoing rule) -- anything else gets the fixed generic
      // sentence. Both status regions carry it (the load is one fact about
      // the whole canvas), the surfaces stay disabled, and every entry point
      // now refuses with this same line through unloadedReason().
      loadFailureReason = LOAD_FAILURE_PREFIX + (
        error instanceof ContentEncodingError || error instanceof ContentSizeError
          ? error.message
          : "the load failed before any buffer state existed"
      );
      for (const kind of BUFFER_KINDS) {
        statusEls[kind].textContent = bufferLabel(kind) + ": " + loadFailureReason;
        statusEls[kind].classList.add("doxbench-status-error");
      }
      stateEvent(loadFailureReason);
    }
  }

  applyVisibility(); // the honest default shape before the load settles
  const readyPromise = initialLoad();

  // T064/T065 wire: apply a VALIDATED typed proposal to ONE buffer through
  // the live edit path. The identity gate runs HERE, at the swap, against
  // the SETTLED current identity (the same rule doxbench-state.js's pure
  // `applyProposalToBuffer` enforces for non-controller callers); on any
  // mismatch the apply refuses fixed and the buffer is untouched. Recovery
  // is a new turn — no force path exists.
  async function applyProposal(kind, proposal) {
    // W-10 (wave re-review): every refusal used to collapse into one
    // staleness sentence, so a click while a keystroke's hash was still
    // settling -- or during a Save, or a load -- was advised "ask again in a
    // new turn", which is false in both halves: the proposal matched, and a
    // moment's wait was the recovery. Each refusal now carries a fixed CODE
    // (never free text) the rail maps to its own vocabulary; the sentences
    // here remain the canvas's and are never echoed by the rail.
    if (destroyed) {
      return { ok: false, code: "unavailable", error: DESTROYED_REASON };
    }
    // T104 F6-2/F6-6: no state, no identity to gate against -- a stated
    // refusal, never a TypeError.
    if (!state) {
      return { ok: false, code: "unavailable", error: unloadedReason() };
    }
    const buffer = state.buffers[kind];
    if (!buffer || !proposal) {
      return { ok: false, code: "unavailable",
               error: "this proposal has nothing to apply to" };
    }
    if (buffer.hash_pending || !buffer.current_hash) {
      return { ok: false, code: "unsettled",
               error: "the buffer identity is still settling" };
    }
    if (proposal.base_hash !== buffer.current_hash.hex) {
      return { ok: false, code: "stale",
               error: "this proposal no longer matches the buffer" };
    }
    // W-2 (wave re-review): a proposal enters through the SAME EOL lens as
    // a keystroke. Models typically emit LF regardless of the document's
    // flavor, and applying that verbatim made the buffer pure LF -- a Save
    // then committed an every-line-ending rewrite, and the NEXT keystroke
    // flipped the whole file back to the base's flavor: two byte-level
    // outcomes for one reviewed proposal, re-opening the silent-mass-rewrite
    // class F10-3 closed for typing. The proposal's text is projected into
    // the display domain and re-flavored exactly like read-back, so the
    // buffer stays uniformly in the document's own line-ending discipline.
    const flavored = bufferTextFor(
      displayText(String(proposal.content)),
      eolFlavorOf(buffer.base_content));
    return edit(kind, flavored);
  }

  return {
    ready: readyPromise,
    state: () => state,
    // WHICH BUFFER (the context region's answer, mirrored into working state)
    // and WHICH VIEW (this panel's own, deliberately not persisted). Two
    // levels, two nouns, no word doing double duty.
    activeBuffer: () => activeBuffer,
    setActiveBuffer,
    activeView: () => activeView,
    setActiveView,
    // T104 F1: the non-destructive half of a session key change. A create (or
    // any other verb) that opens the session moves the whole overlay onto a
    // new ref; the composition used to answer that by tearing the canvas down
    // and rebuilding it from `/source`, which discards unsaved buffers. This
    // moves the working state onto the new ref with both buffers exactly as
    // they are -- the same call the Save path already makes for itself, and a
    // no-op when the ref has not moved.
    rekey: (ref) => { rekeyTo(ref); },
    edit,
    applyProposal,
    // `discard` stays the per-buffer primitive (the guard's Discard choice is
    // its other caller); `cancel` is the panel control, aimed at the active
    // buffer.
    discard,
    cancel,
    save,
    saving: () => saving,
    selectDocument,
    resolveGuard,
    flushPreview,
    refreshContext,
    viewState,
    elements,
    destroy,
  };
}
