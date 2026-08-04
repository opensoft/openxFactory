// doxBench's two-buffer authoring canvas (010-doxbench-editor-chat, US1:
// tasks T033-T036, fix round T033c). Mounts exactly the Outline and Document
// buffers, their debounced Markdown preview, the document-switch guard (with
// a real document picker to reach it), and per-buffer focus/selection/scroll
// persistence across tab switches and context refreshes (FR-003..FR-010,
// acceptance scenarios 1-5).
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
//   wired. Every Save-shaped control (the per-buffer button, its visible note,
//   the guard's own Save choice, and the guard's sentence) is byte-for-byte
//   what it was before this arm existed: disabled, `aria-disabled="true"`, and
//   naming SAVE_UNAVAILABLE_REASON as VISIBLE text beside the control rather
//   than only in a hover title. `save()` and `resolveGuard("save")` refuse with
//   that same fixed reason and change nothing at all. Nothing in this posture
//   reads the seam, because there is none.
//
//   A SEAM INJECTED -- Save becomes real. The controls are enabled, the fixed
//   reason is GONE rather than merely restyled (a disabled-looking control that
//   still says Save is unavailable while Save works would be the worst of both),
//   and each buffer reports its own verdict in its own live status region.
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
// edit, discardBuffer for Discard, replaceBuffer to advance the two-buffer
// state, setActiveBuffer for a tab switch, and persistDoxBenchState /
// restoreDoxBenchState for session recovery. This module never computes
// `dirty` itself, never compares a content identity itself, and never
// mutates a returned buffer object -- they are frozen, and replaceBuffer is
// the only way forward.
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
// edit, a Discard, a tab switch, a document switch -- is handed to
// persistDoxBenchState against the caller's injected storage, and destroy()
// persists once more on the way out. After destroy(), the controller goes
// fully inert: edit, discard, selectDocument, resolveGuard, and setActiveTab
// all refuse rather than touch a torn-down mount.
//
// FOCUS is tracked explicitly, never left to the DOM to remember for free: a
// hidden pane cannot hold real focus in a real document, so this module
// records which buffer last received it and restores that focus when its
// tab becomes visible again -- and never invents focus for a buffer that was
// never actually focused. The document-switch guard follows the same
// discipline in miniature: opening it moves focus to its Discard choice;
// resolving or cancelling it returns focus to the Document buffer, and it
// never traps focus.
//
// selectDocument REFUSES a path outside the scope (neither a context path
// nor an editable path) rather than loading it -- FR-007 says "the
// explicitly selected SCOPED document", not any path a caller might name.
// The one way a human reaches selectDocument at all is the labelled document
// picker this module renders in the Document pane, listing exactly
// `projection.active_document_candidates`; choosing a path while the buffer
// is dirty reverts the control's displayed value until the guard resolves.

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
  setActiveBuffer,
  settleBufferHash,
} from "./doxbench-state.js";

export const DOXBENCH_BUFFER_TABS = Object.freeze([
  { key: "outline", label: "Outline" },
  { key: "document", label: "Document" },
]);

// A fixed, honest string. This slice never wires a governed Save action, so
// every Save-shaped control (the per-buffer button, its visible note, and
// the guard's own Save choice) states exactly this instead of pretending to
// be reachable.
export const SAVE_UNAVAILABLE_REASON =
  "Save is not wired in this preview -- the governed Save action ships in a later change";

// The wired posture's own honest notes. They state what Save DOES so the
// enabled control is as legible as the disabled one was, and they deliberately
// never contain SAVE_UNAVAILABLE_REASON -- a wired canvas that still carried
// that sentence would be lying in the opposite direction.
export const SAVE_WIRED_NOTE =
  "Save persists only the changed buffers, Outline before Document, through the "
  + "existing governance actions";
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

const DESTROYED_REASON = "this doxBench canvas has been destroyed";
const DEFAULT_PREVIEW_DELAY_MS = 150;
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

// G-1: the outline-only posture, stated in the two places the operator looks
// for a document — the picker's own label and the Document buffer's status.
export const OUTLINE_ONLY_LABEL =
  "Active document — none: this tile's outline is its only editable "
  + "document, and chat grounds on it";
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

  // ---- mutable controller state, declared before DOM construction so the --
  // ---- document picker's initial option list can read it synchronously. --
  let currentProjection = projection;
  let state = null; // the doxbench-state.js state object, once loaded
  let activeTab = "outline";
  let activeDocumentPath = "activeDocumentPath" in options
    ? options.activeDocumentPath
    : (currentProjection.active_document_candidates
      && currentProjection.active_document_candidates[0]) || null;
  let guardTargetPath = null; // set while the guard blocks a selectDocument
  let destroyed = false;
  let saving = false;         // a governed Save is in flight (wired posture only)
  const savingKinds = new Set();   // the buffers THIS Save handed over
  // The last Save verdict for each buffer, as the sentence its status region
  // states. Cleared by the next local action on that buffer, because a "saved"
  // line beside freshly typed text would be stale the instant it is read.
  const saveOutcomes = { outline: null, document: null };
  const rememberedFocus = { outline: false, document: false };
  const previewTimers = { outline: null, document: null };

  // ---- fixed DOM, built ONCE. Every later update mutates it in place. -----
  const titleText = options.title || currentProjection.title || null;
  const canvasLabel = "doxBench" + (titleText ? " · " + titleText : "");
  host.setAttribute("role", "region");
  host.setAttribute("aria-label", canvasLabel);
  const heading = el("h2", "doxbench-heading", canvasLabel);

  const tablist = el("div", "doxbench-tabs");
  tablist.setAttribute("role", "tablist");
  tablist.setAttribute("aria-label", "doxBench buffers");

  const panes = el("div", "doxbench-panes");

  const tabButtons = {};
  const paneEls = {};
  const textareas = {};
  const previews = {};
  const statusEls = {};
  const discardButtons = {};
  const saveButtons = {};
  let documentPicker = null;

  for (const tab of DOXBENCH_BUFFER_TABS) {
    const tabId = instanceId + "-tab-" + tab.key;
    const paneId = instanceId + "-pane-" + tab.key;
    const previewId = instanceId + "-preview-" + tab.key;

    const tabBtn = el("button", "doxbench-tab", tab.label);
    tabBtn.type = "button";
    tabBtn.id = tabId;
    tabBtn.setAttribute("role", "tab");
    tabBtn.setAttribute("aria-controls", paneId);
    tabBtn.addEventListener("click", () => { setActiveTab(tab.key); });
    // CHK007 (T100 AT measurement, 2026-08-02: FAIL — correct semantics but
    // no roving tabindex, so Arrow/Home/End moved focus nowhere). The WAI-ARIA
    // APG tablist pattern: exactly ONE tab is tabbable at a time
    // (applyTabVisibility maintains it), Left/Right (plus Up/Down, which the
    // operator tried first) move selection with focus, Home/End jump to the
    // ends, and the arrow keys are consumed so they no longer scroll the page.
    tabBtn.addEventListener("keydown", (ev) => {
      const keys = {
        ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1,
      };
      const order = DOXBENCH_BUFFER_TABS.map((t) => t.key);
      let next = null;
      if (ev.key in keys) {
        const at = order.indexOf(activeTab);
        next = order[(at + keys[ev.key] + order.length) % order.length];
      } else if (ev.key === "Home") {
        next = order[0];
      } else if (ev.key === "End") {
        next = order[order.length - 1];
      }
      if (next === null) return;
      ev.preventDefault();   // no page scroll from an arrow inside a tablist
      setActiveTab(next);
      tabButtons[next].focus();
    });
    tablist.appendChild(tabBtn);
    tabButtons[tab.key] = tabBtn;

    const pane = el("div", "doxbench-pane doxbench-pane-" + tab.key);
    pane.id = paneId;
    pane.setAttribute("role", "tabpanel");
    pane.setAttribute("aria-labelledby", tabId);

    const toolbar = el("div", "doxbench-toolbar");
    const status = el("span", "doxbench-status");
    status.setAttribute("aria-live", "polite");
    const discardBtn = el("button", "doxbench-discard", "Discard");
    discardBtn.type = "button";
    discardBtn.title = "restore this buffer to its last loaded or saved text";
    discardBtn.addEventListener("click", () => { discard(tab.key); });
    const saveBtn = el("button", "doxbench-save", "Save");
    saveBtn.type = "button";
    if (saveSeam) {
      saveBtn.title = "save this canvas's changed buffers through the existing "
        + "governance actions";
      saveBtn.setAttribute("aria-disabled", "false");
      saveBtn.addEventListener("click", () => { save(); });
    } else {
      saveBtn.disabled = true;
      saveBtn.title = SAVE_UNAVAILABLE_REASON;
      saveBtn.setAttribute("aria-disabled", "true");
    }
    const saveNoteId = instanceId + "-save-note-" + tab.key;
    const saveNote = el("span", "doxbench-save-note",
                        saveSeam ? SAVE_WIRED_NOTE : SAVE_UNAVAILABLE_REASON);
    saveNote.id = saveNoteId;
    saveBtn.setAttribute("aria-describedby", saveNoteId);
    toolbar.append(status, discardBtn, saveBtn, saveNote);

    const editarea = el("div", "doxbench-editarea");
    const textarea = document.createElement("textarea");
    textarea.className = "doxbench-textarea";
    textarea.setAttribute("aria-label", tab.label + " buffer text");
    textarea.setAttribute("aria-describedby", previewId);
    textarea.addEventListener("input", async () => {
      const result = await edit(tab.key, textarea.value);
      if (!result.ok) {
        // Refused honestly and VISIBLY: the human's keystroke or paste must
        // never just vanish with nothing said (CHK016/CHK019).
        status.textContent = "refused -- " + result.error;
        status.classList.add("doxbench-status-error");
      } else {
        status.classList.remove("doxbench-status-error");
      }
    });
    textarea.addEventListener("focus", () => { rememberedFocus[tab.key] = true; });
    const preview = el("div", "doxbench-preview doxbench-preview-" + tab.key);
    preview.id = previewId;
    preview.setAttribute("aria-label", tab.label + " preview");
    editarea.append(textarea, preview);

    if (tab.key === "document") {
      // The one way a human reaches selectDocument (T035 / acceptance
      // scenario 4): a labelled, keyboard-reachable picker naming exactly
      // the scoped candidates. No transport -- it only calls the local
      // selectDocument(path) method.
      //
      // G-1 (PR #63 re-verification): a tile whose ONLY editable path is its
      // own primary fragment — which this canvas loads as the OUTLINE, and
      // which is therefore not offered as a DOCUMENT (T104 F2) — has no
      // candidate to pick. That posture is STATED here rather than rendered as
      // an empty control that does nothing: chat still works on such a tile,
      // grounded on the outline alone.
      const candidatePaths = currentProjection.active_document_candidates || [];
      const pickerLabel = el("label", "doxbench-picker-label",
        candidatePaths.length ? "Active document" : OUTLINE_ONLY_LABEL);
      const picker = document.createElement("select");
      picker.className = "doxbench-document-picker";
      picker.setAttribute("aria-label", "choose the active Document buffer");
      picker.disabled = candidatePaths.length === 0;
      for (const candidate of candidatePaths) {
        const opt = document.createElement("option");
        opt.value = candidate;
        opt.textContent = basename(candidate);
        picker.appendChild(opt);
      }
      if (activeDocumentPath != null) picker.value = activeDocumentPath;
      picker.addEventListener("change", async () => {
        const target = picker.value;
        const result = await selectDocument(target);
        if (result.status === "blocked") {
          // Never silently replace the edited buffer, and never leave the
          // control lying about which document is actually active.
          picker.value = activeDocumentPath;
        }
      });
      pickerLabel.appendChild(picker);
      pane.append(pickerLabel, toolbar, editarea);
      documentPicker = picker;
    } else {
      pane.append(toolbar, editarea);
    }
    panes.appendChild(pane);

    paneEls[tab.key] = pane;
    textareas[tab.key] = textarea;
    previews[tab.key] = preview;
    statusEls[tab.key] = status;
    discardButtons[tab.key] = discardBtn;
    saveButtons[tab.key] = saveBtn;
  }

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

  host.append(heading, tablist, panes, guardHost);

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

  function syncBufferDom(kind) {
    const buffer = state.buffers[kind];
    const textarea = textareas[kind];
    // Only reassign `.value` when it actually differs: real browsers can
    // move the caret to the end of a textarea whose `.value` is reassigned
    // even to its OWN current string, so a live-typing edit (whose DOM value
    // already matches) must never re-touch it. A programmatic edit,
    // Discard, or document switch always DOES differ, so it still syncs.
    if (textarea.value !== buffer.content) textarea.value = buffer.content;
    statusEls[kind].textContent = statusLine(kind, buffer);
    statusEls[kind].classList.toggle("is-dirty", buffer.dirty);
    if (saveSeam) {
      // With a governed Save wired, Discard restores the last SAVED text, so it
      // stays available on a clean buffer (a no-op there, and a control that
      // flickered between postures mid-Save would be worse). Only an in-flight
      // Save takes it away. Without a seam this is untouched: a clean buffer has
      // nothing to restore, so Discard is disabled exactly as before.
      statusEls[kind].setAttribute("aria-busy", savingKinds.has(kind) ? "true" : "false");
      saveButtons[kind].disabled = saving;
      saveButtons[kind].setAttribute("aria-disabled", saving ? "true" : "false");
      discardButtons[kind].disabled = saving;
      if (documentPicker) documentPicker.disabled = saving;
      guardSaveBtn.disabled = saving;
      guardDiscardBtn.disabled = saving;
      guardCancelBtn.disabled = saving;
    } else {
      discardButtons[kind].disabled = !buffer.dirty;
    }
  }

  // The status region states, in order: what a Save is doing to this buffer
  // right now, what the last Save said about it, and whether it currently holds
  // unsaved changes. Each buffer gets its OWN sentence -- a partial outcome
  // reported as one blended verdict would be exactly the lie FR-035 forbids.
  function statusLine(kind, buffer) {
    const dirtyText = bufferStatusText(kind, buffer);
    if (savingKinds.has(kind)) return "saving this buffer -- " + dirtyText;
    const outcome = saveOutcomes[kind];
    return outcome ? outcome + " -- " + dirtyText : dirtyText;
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

  function forgetSaveOutcome(kind) {
    if (saveOutcomes[kind] !== null) saveOutcomes[kind] = null;
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
    const dirtyText = buffer.dirty ? "unsaved changes" : "no unsaved changes";
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
    return Promise.all([flushOne("outline"), flushOne("document")]);
  }

  function applyTabVisibility() {
    for (const tab of DOXBENCH_BUFFER_TABS) {
      const isActive = tab.key === activeTab;
      tabButtons[tab.key].setAttribute("aria-selected", String(isActive));
      // CHK007 roving tabindex: the selected tab is the ONLY tabbable one, so
      // Tab enters the strip once and the arrows move within it (APG).
      tabButtons[tab.key].tabIndex = isActive ? 0 : -1;
      tabButtons[tab.key].classList.toggle("doxbench-tab-active", isActive);
      paneEls[tab.key].hidden = !isActive;
      // A hidden pane cannot hold real focus; a shown pane that previously
      // held it gets it back. A pane that never held focus never steals it.
      if (isActive && rememberedFocus[tab.key]) {
        textareas[tab.key].focus();
      }
    }
  }

  function setActiveTab(kind) {
    if (destroyed) return activeTab;
    if (kind !== "outline" && kind !== "document") {
      throw new TypeError("setActiveTab kind must be outline or document");
    }
    if (activeTab === kind) return activeTab;
    activeTab = kind;
    if (state) state = setActiveBuffer(state, kind);
    applyTabVisibility();
    persistNow();
    return activeTab;
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
    forgetSaveOutcome(kind);
    const before = state.buffers[kind];
    const pending = beginBufferEdit(before, text, hashOptions);
    state = replaceBuffer(state, pending.buffer);
    syncBufferDom(kind);
    let completion;
    try {
      completion = await pending.completion;
    } catch (error) {
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
    forgetSaveOutcome(kind);
    const discarded = discardBuffer(state.buffers[kind]);
    state = replaceBuffer(state, discarded);
    syncBufferDom(kind);
    renderPreviewNow(kind);
    persistNow();
    return Promise.resolve({ ok: true });
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
    const changed = BUFFER_KINDS.filter((kind) => state.buffers[kind].dirty);
    if (!changed.length) {
      // Nothing to persist reaches no governance action at all: the seam is not
      // called in order to discover it had nothing to do.
      for (const kind of BUFFER_KINDS) {
        saveOutcomes[kind] = saveOutcomeSentence(unchangedRow(kind));
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
      forgetSaveOutcome(kind);
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
      for (const kind of changed) saveOutcomes[kind] = "Save refused -- " + reason;
      for (const kind of BUFFER_KINDS) syncBufferDom(kind);
      return { status: "refused", reason };
    }
    let landedRef = null;
    for (const row of outcomeRowsOf(outcome)) {
      if (!row || !BUFFER_KINDS.includes(row.kind)) continue;
      if (row.status === "committed") {
        try {
          state = replaceBuffer(state, adoptSavedBase(state.buffers[row.kind], row));
          if (landedRef === null && typeof row.ref === "string") landedRef = row.ref;
        } catch (error) {
          // A commit whose reported identity the state module refuses is NOT
          // adopted: the buffer keeps its text and its dirty flag, and the
          // human is told, rather than being handed a base nothing can verify.
          saveOutcomes[row.kind] = "Save reported a commit this canvas could not "
            + "adopt -- " + ((error && error.message) || "unknown error")
            + "; this buffer keeps its unsaved text";
          continue;
        }
      }
      saveOutcomes[row.kind] = saveOutcomeSentence(row);
    }
    const previousRef = scopeKey().ref;
    if (landedRef !== null) rekeyTo(landedRef);
    for (const kind of BUFFER_KINDS) syncBufferDom(kind);
    persistNow();
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
    forgetSaveOutcome("document");
    const descriptor = await loadDescriptor("document", path);
    const buffer = await createBufferState(
      { kind: "document", repository: scopeKey().repository, ...descriptor },
      hashOptions,
    );
    state = replaceBuffer(state, buffer);
    activeDocumentPath = path;
    if (documentPicker) documentPicker.value = path == null ? "" : path;
    syncBufferDom("document");
    renderPreviewNow("document");
    persistNow();
    return { status: "switched", reason: null };
  }

  async function selectDocument(path) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
    if (path === activeDocumentPath) return { status: "unchanged", reason: null };
    if (path !== null && !isInScope(path)) {
      // FR-007: "the explicitly selected SCOPED document" -- a path this
      // scope never declared (neither context nor editable) is refused
      // outright, never loaded and never silently substituted.
      return { status: "refused", reason: "out_of_scope" };
    }
    if (state.buffers.document.dirty) {
      showGuard(path);
      return { status: "blocked", reason: "dirty_document" };
    }
    return switchDocument(path);
  }

  async function resolveGuard(choice) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (choice === "save") {
      if (!saveSeam) {
        // MUST refuse and change nothing -- no switch, no persistence, and the
        // guard stays open: the human still has to choose Discard or Cancel.
        return { status: "refused", reason: SAVE_UNAVAILABLE_REASON };
      }
      if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
      const outcome = await save();
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
      textareas.document.focus();
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
      textareas.document.focus();
      return { status: "cancelled", reason: null };
    }
    if (choice === "discard") {
      const target = guardTargetPath;
      guardTargetPath = null;
      hideGuard();
      await discard("document");
      const result = await switchDocument(target);
      textareas.document.focus();
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
      tab: (kind) => tabButtons[kind] || null,
      discard: (kind) => discardButtons[kind] || null,
      save: (kind) => saveButtons[kind] || null,
      guard: () => guardHost,
      // additive, beyond the fixed minimum set: a per-buffer status region
      // and the document picker, both needed to test the fix round's
      // visible-refusal and scope-guard behaviour.
      status: (kind) => statusEls[kind] || null,
      documentPicker: () => documentPicker,
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
    persistNow();
  }

  async function initialLoad() {
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
      activeTab = restored.active_buffer;
      activeDocumentPath = restored.buffers.document.path;
      if (documentPicker && activeDocumentPath != null) documentPicker.value = activeDocumentPath;
    } else {
      const [outline, documentDescriptor] = await Promise.all([
        loadDescriptor("outline", currentProjection.outline_path),
        loadDescriptor("document", activeDocumentPath),
      ]);
      state = await createDoxBenchState(
        { key, active_buffer: activeTab, outline, document: documentDescriptor },
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
    applyTabVisibility();
    syncBufferDom("outline");
    syncBufferDom("document");
    renderPreviewNow("outline");
    renderPreviewNow("document");
  }

  applyTabVisibility(); // the honest default shape before the load settles
  const readyPromise = initialLoad();

  // T064/T065 wire: apply a VALIDATED typed proposal to ONE buffer through
  // the live edit path. The identity gate runs HERE, at the swap, against
  // the SETTLED current identity (the same rule doxbench-state.js's pure
  // `applyProposalToBuffer` enforces for non-controller callers); on any
  // mismatch the apply refuses fixed and the buffer is untouched. Recovery
  // is a new turn — no force path exists.
  async function applyProposal(kind, proposal) {
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    const buffer = state.buffers[kind];
    if (!buffer || buffer.hash_pending || !buffer.current_hash
        || !proposal || proposal.base_hash !== buffer.current_hash.hex) {
      return { ok: false, error: "this proposal no longer matches the buffer" };
    }
    return edit(kind, String(proposal.content));
  }

  return {
    ready: readyPromise,
    state: () => state,
    activeTab: () => activeTab,
    setActiveTab,
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
    discard,
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
