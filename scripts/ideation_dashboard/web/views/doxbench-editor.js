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
//   whole-canvas (the dirty set over the buffer set, one call to the seam,
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
// PHASE B (add-doxbench-editing-phase-b, ratified 2026-08-18) WIDENED THE
// BUFFER SET AND THEREFORE CHANGED THE SOURCE OF THIS FILE'S ENUMERATION --
// AND NOTHING ABOUT ITS STRUCTURE:
//
//   Phase A said the widening would be "a change to the buffer contract and to
//   nothing on this surface", and its own task list expected this file to be
//   verified UNCHANGED. That expectation was WRONG in one narrow, structural
//   way, and it is recorded here as a FINDING rather than papered over: this
//   controller did not read the buffer set, it read `BUFFER_KINDS` -- the KIND
//   vocabulary -- AS the state's key list. `perBuffer(seed)` seeded from it, the
//   per-buffer DOM was built by looping it, every dirty/visibility/sync pass
//   iterated it, and `setActiveBuffer` refused anything outside it. Two literal
//   buffer names were therefore baked into the view's own structure by way of a
//   constant that no longer means what those loops assumed, which is exactly
//   what the ratified requirement refuses.
//
//   SO THE ENUMERATION SOURCE MOVED TO THE STATE (`bufferKeysInOrder`), and the
//   loops, the maps, the DOM registry and the refusals are the same loops, maps,
//   registry and refusals over a set whose LENGTH is now the human's decision.
//   `BUFFER_KINDS` survives here for exactly one window -- the mount, before any
//   working state exists -- and says so at each site.
//
//   THE PER-BUFFER DOM IS LAZY AND IDEMPOTENT (`ensureBufferDom`). It builds one
//   key's status region, textarea and preview ONCE and can be called again for
//   the same key without building a second set. At mount it is called for
//   `BUFFER_KINDS` in order, so the initial DOM is byte-for-byte what Phase A
//   built; a key the loaded set GAINS gets the same treatment on arrival.
//
//   THE CANVAS STILL PRESENTS EXACTLY ONE BUFFER, with exactly ONE Save and ONE
//   Cancel. No second buffer-selection tablist appears here -- the delta forbids
//   it, and the loaded-document SELECTOR lives on the chat rail, which is a
//   different surface reading this controller's `loadedBuffers()`.
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
// for a selection change, loadDocumentBuffer / unloadDocumentBuffer for the
// LOADED SET's one way in and one way out, and persistDoxBenchState /
// restoreDoxBenchState for session recovery. That module is likewise the single
// ENUMERATION authority: `bufferKeysInOrder(state)` answers "which buffers are
// there, in which order", so nothing below enumerates `outline` and `document`
// by name and widening the buffer set changes the buffer contract and no
// structure on this surface. This module never computes `dirty` itself, never
// compares a content identity itself, and never mutates a returned buffer
// object -- they are frozen, and replaceBuffer is the only way forward.
//
// THE LOADED SET'S ONE ENTRY ROUTE reaches this file as
// `loadDocumentForEditing(path)` -- the controller half of the `docs` tile's
// load verb (design D5: a retrieval result, a proposal, the snapshot and an
// inherited edge all reach it never). It uses the SAME injected `loadSource`
// seam `selectDocument` uses, refuses at the bound with the MEASURED number
// rather than evicting a buffer that may hold unsaved work (D6), and SELECTS an
// already-loaded path instead of re-reading it, because a re-read would
// silently discard that buffer's unsaved text.
//
// THE GENERATION CONTRACT, PAIRED CORRECTLY. `settleBufferHash` only accepts
// a completion whose generation and content match the buffer it is handed --
// so it MUST be handed the LIVE buffer at settle time (`state.buffers[key]`),
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
  // THE KIND VOCABULARY, and -- since Phase B -- nothing else. It is read at
  // exactly one place below (the mount window, before working state exists) and
  // never as the state's key list.
  BUFFER_KINDS,
  ContentEncodingError,
  ContentSizeError,
  DOXBENCH_MAX_LOADED_DOCUMENTS,
  LOAD_REFUSED_ALREADY_LOADED,
  LOAD_REFUSED_BOUND_REACHED,
  LOAD_REFUSED_RESERVED_KEY,
  OUTLINE_BUFFER_KEY,
  UNLOAD_REFUSED_DIRTY,
  UNBACKED_DOCUMENT_BUFFER_KEY,
  adoptSavedBase,
  beginBufferEdit,
  // THE ENUMERATION AUTHORITY: the state's own keys, outline first, then the
  // loaded documents in the module's declared deterministic order.
  bufferKeysInOrder,
  clearDoxBenchSession,
  createBufferState,
  createDoxBenchState,
  discardBuffer,
  loadDocumentBuffer,
  loadedDocumentKeys,
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
  unloadDocumentBuffer,
} from "./doxbench-state.js";

// THE CANVAS'S VIEW TABS -- which VIEW of the one active buffer is shown.
// Rendered in the order `Editor`, `Preview` (raw before rendered reads as a
// progression) with `Preview` SELECTED at mount: reading order and selection
// are different questions and Phase A answers them differently on purpose.
export const DOXBENCH_VIEW_TABS = Object.freeze([
  { key: "editor", label: "Editor" },
  { key: "preview", label: "Preview" },
]);

// The RESERVED buffer LABELS, which are not a control. This is what is left of
// the retired buffer tablist: names for accessible names and status regions,
// keyed by the two RESERVED keys `doxbench-state.js` owns. A key with no label
// here names itself through `bufferLabelFor` below, so widening the buffer set
// cannot silently produce an unnamed surface.
export const DOXBENCH_BUFFER_LABELS = Object.freeze({
  outline: "Outline",
  document: "Document",
});

// THE LABEL RULE FOR A PATH KEY, declared here and pinned by a test, because
// Phase B keys document buffers by PATH and a path is not a label a human reads.
//
//   1. A RESERVED key (`outline`, the unbacked `document` create slot) keeps its
//      word from DOXBENCH_BUFFER_LABELS. Unchanged from Phase A, byte for byte.
//   2. A path key labels as the SHORTEST TRAILING PATH SUFFIX that no OTHER
//      loaded document key shares -- its basename where basenames are unique,
//      `<folder>/<file>` where two loaded documents share a basename, and so on
//      up to the whole path. Two entries a human cannot tell apart is the one
//      thing the ratified selector requirement calls worse than a long name, and
//      the same honesty is owed to the canvas's own accessible names, which is
//      why the rule lives here rather than in the rail that renders the list.
//   3. Labels are RECOMPUTED whenever the key set changes (`refreshBufferLabels`
//      below), because a collision can arrive later: the second file named
//      `README.md` must lengthen the FIRST one's label too.
function trailingPathSegments(pathKey, segments) {
  const parts = String(pathKey).split("/");
  return parts.slice(Math.max(0, parts.length - segments)).join("/");
}

function bufferLabelFor(bufferKey, siblingKeys) {
  const reserved = DOXBENCH_BUFFER_LABELS[bufferKey];
  if (reserved) return reserved;
  const others = Array.from(siblingKeys).filter(
    (candidate) => candidate !== bufferKey
      && candidate !== OUTLINE_BUFFER_KEY
      && candidate !== UNBACKED_DOCUMENT_BUFFER_KEY,
  );
  const depth = String(bufferKey).split("/").length;
  for (let segments = 1; segments <= depth; segments += 1) {
    const candidate = trailingPathSegments(bufferKey, segments);
    const shared = others.some(
      (other) => trailingPathSegments(other, segments) === candidate,
    );
    if (!shared) return candidate;
  }
  // Unreachable while keys are unique paths (the state module refuses two
  // buffers claiming one path), and still stated rather than assumed.
  return String(bufferKey);
}

// THE CSS SLUG RULE, likewise declared and pinned. The class names this canvas
// writes embed the buffer they belong to (`doxbench-status-outline`), and a path
// is not a legal class fragment at all -- so:
//
//   1. The two RESERVED keys produce EXACTLY today's fragments (`outline`,
//      `document`), so every existing stylesheet rule and DOM assertion keeps
//      matching byte for byte.
//   2. A path key produces its sanitised basename plus a short deterministic
//      digest of the WHOLE key. The digest is what makes the fragment UNIQUE:
//      `a/b.md` and `a-b.md` sanitise alike, and two boxes sharing one class
//      would make a stylesheet rule or a test selector ambiguous about which
//      buffer it named.
const SLUG_DIGEST_RADIX = 16;

function slugDigest(value) {
  // FNV-1a, 32-bit -- a few lines, no imports, deterministic across runs. It is
  // a NAMING aid and never a content identity: the one content-identity
  // authority is doxbench-state.js's SHA-256 hashing, and nothing here is ever
  // compared against a hash.
  let digest = 0x811c9dc5;
  const text = String(value);
  for (let at = 0; at < text.length; at += 1) {
    digest ^= text.charCodeAt(at);
    digest = Math.imul(digest, 0x01000193) >>> 0;
  }
  return digest.toString(SLUG_DIGEST_RADIX).padStart(8, "0");
}

function bufferSlug(bufferKey) {
  if (Object.prototype.hasOwnProperty.call(DOXBENCH_BUFFER_LABELS, bufferKey)) {
    return String(bufferKey);
  }
  const base = String(bufferKey).split("/").at(-1) || String(bufferKey);
  const sanitised = base.replace(/[^A-Za-z0-9_-]+/g, "-")
    .replace(/^-+/, "").replace(/-+$/, "");
  return (sanitised || "doc") + "-" + slugDigest(bufferKey);
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

// The Unload control's REASONS. Carried over verbatim from the rail control this
// one replaces so no accessible text was lost in the move (Amendment 1), then
// NARROWED by Amendment 2 (2026-08-21, Brett, ruled via browser annotation): the
// reserved set is the OUTLINE ALONE. The outline's sentence is unchanged and is
// the only one that still says "never unloaded".
//
// The `document` slot's sentence is gone, because the fact it stated is no longer
// true: a BACKED reserved slot in the neutral position unloads like any other
// document. What is left under that key is the UNBACKED slot, and it is inert for
// a different reason entirely — it names no document, so there is nothing to take
// out of the loaded set. Cancel is the control that acts on it; Unload has no
// subject.
export const UNLOAD_OUTLINE_RESERVED_TITLE =
  "the outline is a reserved buffer every turn carries, and is never unloaded";
export const UNLOAD_UNBACKED_DOCUMENT_TITLE =
  "this document has not been created yet, so there is nothing to unload — "
  + "Cancel restores it, and its first Save gives it a path";
export const UNLOAD_NOTHING_SELECTED_TITLE =
  "no loaded document is selected";

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

// ---------------------------------------------------------------------------
// PHASE B's fixed refusal vocabulary for the LOADED SET. Fixed wording, on
// purpose, like every other refusal in this module: each names the SITUATION and
// never the content. The bound's sentence is built rather than fixed because the
// ratified scenario requires the MEASURED number to be stated -- "refuse and say
// the number" is the house pattern here, chosen over the other house pattern
// (degrade softly) because the soft degradation would be discarding human text.
// ---------------------------------------------------------------------------

export const NOT_LOADED_REASON =
  "this document is not in the loaded set, so there is no buffer to act on -- "
  + "load it for editing first";
export const OUTLINE_IS_RESERVED_REASON =
  "the outline buffer is reserved for this scope and cannot be unloaded -- its "
  + "commit is the session ancestry every document save descends from";
export const OUTLINE_HAS_NO_TILE_SAVE_REASON =
  "the outline is saved by the canvas Save, which is the one control it has -- a "
  + "per-document Save belongs to a document's own tile";
export const CONTEXT_ONLY_SAVE_REASON =
  "this buffer is read-only context in the opened tile, not the tile's own "
  + "material, so it has no reachable Save here";
export const UNLOAD_DIRTY_REASON =
  "this document has unsaved changes -- unloading it would drop them, so it "
  + "refuses until they are saved or explicitly discarded";

// F12 (PR #207 review): a repository-root file named exactly `outline` (or
// exactly `document`) cannot be keyed by its own path without claiming a key the
// format reserves. Named, so the human is told which file and why, instead of the
// generic "the load failed" a thrown validator error could only become.
export function reservedKeyReason(path) {
  return "this document's own path is " + String(path) + ", which is a key the "
    + "buffer set reserves -- the outline and the one not-yet-created document "
    + "hold those two names, so a document at this path cannot join the loaded "
    + "set; rename or move it to load it";
}

export function boundReachedReason(bound, measured) {
  return "the loaded set already holds " + String(measured) + " documents, which "
    + "is its declared bound of " + String(bound) + " -- nothing is unloaded to "
    + "make room, because a loaded buffer may hold unsaved work";
}

// #290: the sentence EVERY surface uses for a commit this canvas could not
// adopt -- the buffer's own status region, the one transient line, the tile's
// verdict, and the document-switch guard's reason. Built here, once, and
// exported for the same reason the two reasons above are: a test asserting a
// copy of it pins the copy, so a reword leaves the pin describing nothing while
// still passing. Three surfaces agreeing "in fact" means agreeing on THIS
// string, not on three hand-written near-matches of it.
export function unadoptedCommitReason(detail) {
  return "Save reported a commit this canvas could not adopt -- "
    + (detail || "unknown error") + "; this buffer keeps its unsaved text";
}

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

// The placeholder statements read the buffer's KIND, never its key: a key is a
// path once the loaded set widens, and "could not load this
// ideation/staging/topic/detail.md content" is a sentence about a filename where
// the reader needed a sentence about a KIND of buffer. The kind vocabulary is
// still exactly two words, which is why it is the honest one to render here.
function emptyStatement(bufferKind) {
  return bufferKind === "outline"
    ? "_(no outline yet -- start typing in the Outline buffer to create one)_"
    : "_(no document selected)_";
}

function unavailableStatement(bufferKind) {
  return bufferKind === "outline"
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
  // PHASE B, THE ONE LOADED-SET NOTIFICATION, and deliberately ONE mechanism:
  // an INJECTED CALLBACK, exactly like `onIdentitySettled`, `onSaveLanded` and
  // `onCompanionRestored`. A listener registry (`onLoadedSetChanged(fn)`) was the
  // alternative and is refused here on house-idiom grounds: every other
  // notification out of this module is a seam the composition hands in, a
  // registry would be a second spelling of the same thing, and a second spelling
  // is how two callers come to disagree about who is subscribed. Fired whenever
  // the loaded SET or the SELECTION changes -- which are the two facts the chat
  // rail's selector and the docs wheel's tile marking both render.
  const onLoadedSetChanged = options.onLoadedSetChanged;
  // The declared BOUND on the loaded set (design D6). Injectable for the same
  // reason the timers are: a bound a test cannot pin is a bound a test cannot
  // measure, and the refusal has to STATE the number.
  const maxLoadedDocuments = Number.isSafeInteger(options.maxLoadedDocuments)
    ? options.maxLoadedDocuments
    : DOXBENCH_MAX_LOADED_DOCUMENTS;
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
  // The reserved outline key is where every mount opens, and it is the one key
  // the state contract guarantees is present -- so it is named from the state
  // module's own reserved constant rather than read off the kind vocabulary's
  // first element, which only happened to spell the same word.
  let activeBuffer = OUTLINE_BUFFER_KEY;
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
  const savingKeys = new Set();   // the buffers THIS Save handed over
  // Every per-buffer map below gains its entry LAZILY, per key, as
  // `ensureBufferDom` registers that key -- never seeded from a fixed name list.
  // Phase A seeded them from `BUFFER_KINDS` and called that "not baking in two";
  // it was, because that constant is the KIND vocabulary and not the state's key
  // list. A map that grows with the loaded set is the same map, honestly sourced.
  //
  // The last verdict STATED for each buffer -- a Save's per-buffer answer, or
  // the sentence a Cancel leaves behind naming the buffer it reverted. Cleared
  // by the next local action on that buffer, because a "saved" line beside
  // freshly typed text would be stale the instant it is read.
  const statedOutcomes = {};
  const rememberedFocus = {};
  // The last selection/scroll each buffer's editor held while visible (FR-010):
  // written by applyVisibility as that editor goes hidden -- by a buffer switch
  // OR by a switch into Preview -- and read back as it returns.
  const rememberedView = {};
  const previewTimers = {};
  // What applyVisibility last applied, so a transition can be recognised: an
  // editor going hidden is when its view is captured, an editor becoming
  // visible is when focus and scroll are restored, and a preview becoming
  // visible is when a pending render must be flushed (D2).
  const editorShown = {};
  const previewShown = {};
  // The human-readable label per key, recomputed by `refreshBufferLabels`
  // whenever the key set changes (the collision rule needs the whole set).
  const bufferLabels = {};

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

  // THE EVENT NOTE JOINS THE STATUS ROW FIRST, so every per-buffer status region
  // can be inserted BEFORE it and the row's child order stays exactly what Phase
  // A rendered: the statuses, then the transient event line, then the Save note.
  // A status region built later (a document the human loads mid-session) lands
  // with its siblings rather than after the event line, and `insertBefore`
  // against a reference node that is already a child is the only form a real DOM
  // accepts -- inserting before a non-child throws.
  statusbar.appendChild(eventNote);

  // ONE key's DOM, built ONCE, IDEMPOTENTLY. This is Phase A's per-buffer
  // construction loop with its `for (const kind of BUFFER_KINDS)` header removed
  // and its body given a key: the nodes, classes, attributes and listeners are
  // the same nodes, classes, attributes and listeners. Called for the kind
  // vocabulary at mount (so the initial DOM is byte-for-byte Phase A's) and for
  // any key the loaded set later GAINS. Called twice for one key it does
  // nothing, which is what makes a re-load of an unloaded path reuse the boxes it
  // already had instead of orphaning them in the panes.
  function ensureBufferDom(bufferKey) {
    if (Object.prototype.hasOwnProperty.call(textareas, bufferKey)) {
      // A key that was UNLOADED left its nodes in place, blanked and hidden, so
      // that a re-load reuses them instead of orphaning a pane full of dead
      // boxes. The revival therefore belongs HERE, where the reuse happens.
      statusEls[bufferKey].hidden = false;
      return;
    }
    // Lazy per-buffer bookkeeping, registered with the DOM that carries it so
    // the two can never disagree about which keys exist.
    statedOutcomes[bufferKey] = null;
    rememberedFocus[bufferKey] = false;
    rememberedView[bufferKey] = null;
    previewTimers[bufferKey] = null;
    editorShown[bufferKey] = false;
    previewShown[bufferKey] = false;
    if (!(bufferKey in bufferLabels)) {
      bufferLabels[bufferKey] = bufferLabelFor(bufferKey, [bufferKey]);
    }
    const label = bufferLabel(bufferKey);
    const slug = bufferSlug(bufferKey);
    const previewId = instanceId + "-preview-" + slug;

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
      "doxbench-status doxbench-status-" + slug + " doxbench-sronly");
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

    const editorBox = el("div", "doxbench-bufferbox doxbench-bufferbox-" + slug);
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
      const result = await edit(bufferKey, readBufferValue(bufferKey));
      if (!result.ok) {
        // Refused honestly and VISIBLY: the human's keystroke or paste must
        // never just vanish with nothing said (CHK016/CHK019). The LIVE label is
        // read, not the one captured at construction: a basename collision that
        // arrives later lengthens this buffer's label too.
        const named = bufferLabel(bufferKey);
        status.textContent = named + ": refused -- " + result.error;
        status.classList.add("doxbench-status-error");
        stateEvent(named + ": refused -- " + result.error);
      } else {
        status.classList.remove("doxbench-status-error");
      }
    });
    textarea.addEventListener("focus", () => { rememberedFocus[bufferKey] = true; });
    editorBox.appendChild(textarea);
    viewPaneEls.editor.appendChild(editorBox);

    const previewBox = el("div", "doxbench-bufferbox doxbench-bufferbox-" + slug);
    const preview = el("div", "doxbench-preview doxbench-preview-" + slug);
    preview.id = previewId;
    preview.setAttribute("aria-label", label + " preview");
    // T104 F9-2 (FR-045): the preview renders the SAME content-derived bytes
    // as the textarea it is a view of, so it derives its direction the same way.
    preview.setAttribute("dir", "auto");
    previewBox.appendChild(preview);
    viewPaneEls.preview.appendChild(previewBox);

    bufferBoxes.editor[bufferKey] = editorBox;
    bufferBoxes.preview[bufferKey] = previewBox;
    textareas[bufferKey] = textarea;
    previews[bufferKey] = preview;
    statusEls[bufferKey] = status;

    // THE STATUS BAR: one compact row under the tab row, carrying each buffer's
    // own live status region and the Save note. The per-buffer verdict surface is
    // LOAD-BEARING -- a partial Save (one buffer committed, another refused) is
    // reported per buffer by the ratified buffer contract, and every stated
    // refusal on this surface lands in these same regions -- so a key that joins
    // the loaded set gets its own region here, on arrival, or a Save could not
    // report a verdict about it at all. Each line NAMES its buffer visibly
    // (`statusLine` prefixes the label): stacked unlabelled they rendered as
    // "no unsaved changesno unsaved changes", two identical sentences a reader
    // could not attribute -- which is what the annotated screenshot shows.
    statusbar.insertBefore(status, eventNote);
  }

  // THE MOUNT WINDOW, and the ONE place this file still reads the KIND
  // vocabulary as a list of keys. It is legitimate here and nowhere else:
  // `state` is null until `initialLoad` settles, there is no buffer set to
  // enumerate yet, and the shape a fresh mount always builds is the reserved
  // outline plus the reserved document slot -- exactly `BUFFER_KINDS`, in
  // exactly this order. Keeping it makes the initial DOM byte-for-byte Phase A's;
  // every enumeration AFTER the load reads the state.
  for (const kind of BUFFER_KINDS) ensureBufferDom(kind);

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
  // UNLOAD -- the slot's THIRD occupant, and the one that is alone when it is
  // there (Brett's 2026-08-21 annotation: "if there is a change to save or
  // cancel, then have those buttons. if no changes, then have that be 'unload'
  // button."; Amendment 1 on both doxbench phase changes authorizes it).
  //
  // It replaces the rail's standalone control, and it is the SAME act: it calls
  // the same `unloadDocument` controller the rail's seam forwarded to, with all
  // three refusal layers -- controller, state module, and this control's own
  // reachability rule -- left standing. Those layers are now belt-and-braces
  // rather than the live path, which is exactly what they should be: the dirty
  // case cannot reach this button at all, so `discardUnsavedEdits` is never
  // passed and the two-press arm flow has nothing left to arm.
  const unloadBtn = el("button", "doxbench-unload", "Unload");
  unloadBtn.type = "button";
  unloadBtn.disabled = true;
  unloadBtn.hidden = true;
  unloadBtn.addEventListener("click", () => { unloadActiveBuffer(); });
  // …and its reason as VISIBLE TEXT, on the Save note's own idiom. An INERT
  // Unload cannot take focus, so a `title` alone is reachable by neither a
  // keyboard nor a screen reader -- the same argument this capability already
  // makes for an unreachable Save's reason, which holds doubly here because the
  // control is disabled rather than merely uninformative. The title stays too;
  // this is an addition, not a replacement.
  const unloadNoteId = instanceId + "-unload-note";
  const unloadNote = el("span", "doxbench-unload-note");
  unloadNote.id = unloadNoteId;
  unloadNote.hidden = true;
  unloadBtn.setAttribute("aria-describedby", unloadNoteId);
  const actions = el("div", "doxbench-actions");
  actions.append(cancelBtn, saveBtn, unloadBtn);
  statusbar.appendChild(saveNote);
  statusbar.appendChild(unloadNote);

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

  // ---- THE ENUMERATION, in one place -------------------------------------
  //
  // WHICH BUFFERS ARE THERE. The STATE answers it, in the state module's own
  // declared order (outline first, then loaded documents ascending by key), so
  // every loop, sync, dirty check and visibility pass below carries a set whose
  // length is the human's decision rather than a constant's length.
  //
  // The `BUFFER_KINDS` fallback covers exactly the MOUNT WINDOW -- the paint
  // between `mountDoxBenchCanvas` returning and `initialLoad` settling, where
  // there is no state to read and the DOM that exists is precisely the DOM the
  // mount built for the kind vocabulary. Every other reader of this function runs
  // with state present.
  function bufferKeysNow() {
    return state ? bufferKeysInOrder(state) : BUFFER_KINDS;
  }

  // "Is this a buffer this canvas HOLDS?" -- the widened form of Phase A's
  // `BUFFER_KINDS.includes(...)` guard. Membership is a question about the state,
  // not about a name list, which is the whole difference the delta asks for.
  function holdsBufferKey(bufferKey) {
    if (typeof bufferKey !== "string" || bufferKey === "") return false;
    if (!state) return BUFFER_KINDS.includes(bufferKey);
    return Object.prototype.hasOwnProperty.call(state.buffers, bufferKey);
  }

  // The key the loaded set holds for a PATH, or null. This is what makes
  // "load the same document twice" and "select a document already loaded" resolve
  // to a SELECTION instead of a second read: re-reading would discard the
  // buffer's unsaved text, which the ratified scenario forbids outright.
  function documentKeyForPath(path) {
    if (!state || path === null || path === undefined) return null;
    for (const bufferKey of loadedDocumentKeys(state)) {
      if (state.buffers[bufferKey].path === path) return bufferKey;
    }
    return null;
  }

  function bufferLabel(bufferKey) {
    return bufferLabels[bufferKey]
      || DOXBENCH_BUFFER_LABELS[bufferKey]
      || String(bufferKey);
  }

  // Recompute every label and re-state it on the DOM that carries it. Called
  // whenever the KEY SET changes, because the collision rule is a fact about the
  // whole set: the second `README.md` to be loaded lengthens the FIRST one's
  // label as well as its own, and a label only computed at construction would
  // leave two identical accessible names on screen.
  function refreshBufferLabels() {
    const keys = bufferKeysNow();
    for (const bufferKey of keys) {
      bufferLabels[bufferKey] = bufferLabelFor(bufferKey, keys);
    }
    for (const bufferKey of keys) {
      const label = bufferLabel(bufferKey);
      if (statusEls[bufferKey]) {
        statusEls[bufferKey].setAttribute("aria-label", label + " buffer status");
      }
      if (textareas[bufferKey]) {
        textareas[bufferKey].setAttribute("aria-label", label + " buffer text");
      }
      if (previews[bufferKey]) {
        previews[bufferKey].setAttribute("aria-label", label + " preview");
      }
    }
  }

  // THE ONE LOADED-SET / SELECTION NOTIFICATION (see `onLoadedSetChanged` above).
  // A frozen snapshot, so the rail and the wheel re-render from what they were
  // handed instead of calling back into a controller mid-transition. Contained,
  // because a composition that fails to re-render must never turn a load, an
  // unload or a selection into a failure of the act itself.
  function notifyLoadedSetChanged() {
    if (destroyed || typeof onLoadedSetChanged !== "function") return;
    try {
      onLoadedSetChanged(Object.freeze({
        active: activeBuffer,
        keys: bufferKeys(),
        documents: loadedBuffers(),
      }));
    } catch (unused) {
      // the seam's own detail is dropped unread; the act still happened
    }
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
  function readBufferValue(key) {
    const buffer = state ? state.buffers[key] : null;
    return bufferTextFor(
      textareas[key].value,
      buffer ? eolFlavorOf(buffer.base_content) : "lf",
    );
  }

  function syncBufferDom(key) {
    const buffer = state.buffers[key];
    const textarea = textareas[key];
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
    statusEls[key].textContent = statusLine(key, buffer);
    statusEls[key].classList.toggle("is-dirty", buffer.dirty);
    if (saveSeam) {
      statusEls[key].setAttribute("aria-busy", savingKeys.has(key) ? "true" : "false");
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
    const anythingDirty = bufferKeysNow().some((key) => state.buffers[key].dirty);
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
      // THE SLOT SWAPS (Amendment 1). One control slot, two occupancies: the
      // Save/Cancel pair while the loaded set holds unsaved work, a single
      // Unload while it does not.
      //
      // ANY-buffer-dirty, not selected-buffer-dirty, and `anythingDirty` is
      // deliberately the SAME derivation Save's own reachability reads one line
      // up -- one answer to "is this canvas holding unsaved work", never two.
      // Selected-buffer-dirty would withdraw the only Save from a human whose
      // outline still held unsaved text merely because they had stepped onto a
      // clean document.
      //
      // A Save in flight keeps the PAIR on screen, and that is pinned
      // behaviourally. Note honestly WHICH term delivers it today: a buffer stays
      // dirty until `adoptSavedBase` rebases it, and `save()` clears `saving` in
      // its `finally` BEFORE that rebase runs, so throughout the flight
      // `anythingDirty` is still true and `!anythingDirty` alone already holds
      // the pair. `!saving` is therefore a DEFENSIVE term with no reachable state
      // of its own right now -- kept because it states the intent directly, and
      // because it is the guard that would matter the moment that ordering
      // changed and a buffer went clean while the seam was still open. It is
      // pinned structurally rather than behaviourally for exactly that reason;
      // a behavioural test would be asserting nothing.
      const showUnload = !anythingDirty && !saving;
      saveBtn.hidden = showUnload;
      cancelBtn.hidden = showUnload;
      unloadBtn.hidden = !showUnload;
      if (showUnload) {
        syncUnloadControl();
      } else {
        // The pair is on screen, so Unload's reason has nothing to explain --
        // a note left standing beside Save would describe a control that is
        // not there.
        unloadNote.textContent = "";
        unloadNote.hidden = true;
      }
    } else {
      // No gate at all: Save was never reachable here and stays that way, with
      // its reason beside it as visible text. Cancel is local and follows the
      // active buffer exactly as it always did. THE SLOT DOES NOT SWAP HERE --
      // a surface that cannot save must go on saying so, and an ungated surface
      // has no reachable editing, so an unconditional swap would have made that
      // stated absence unreachable for good.
      cancelBtn.disabled = !activeDirty;
    }
  }

  // THE ONE REACHABILITY RULE for Unload, derived from the SELECTED buffer and
  // shared by the render and the click path so the two cannot drift.
  //
  // AMENDMENT 2 (2026-08-21, Brett, ruled via browser annotation: "if I do the
  // workflow to edit a document, and then cancel instead of save, then try to
  // unload, the unload button is stippled. It should allow the document to
  // unload. only the outline can never unload. we always want that to be loaded.
  // If saved or canceled so the document is in neutral position, then we can
  // unload it."). The rule NARROWED here from the rail control's two-key
  // withholding to the outline alone:
  //
  //   * the OUTLINE is refused, permanently -- it is the one key the state
  //     module itself throws on, and every turn carries it;
  //   * a buffer the loaded set does not HOLD has nothing to act on;
  //   * an UNBACKED buffer -- the create flow's not-yet-created slot, held under
  //     the reserved `document` key with a null path -- has nothing to act on
  //     either. It is a buffer, but it is not a document in the loaded set (it is
  //     the one entry `loadedBuffers` filters out for exactly this reason), so
  //     there is no membership for Unload to end. That is the SAME predicate the
  //     selector lists by, stated once here rather than a second time.
  //
  // Cleanliness needs no term of its own: the slot only shows Unload while
  // nothing in the loaded set is dirty, which is the "neutral position" the
  // ruling names -- saved or cancelled, either way the buffer holds no unsaved
  // work by the time this control is on screen.
  //
  // Where it cannot act the control stays RENDERED and visibly inert with the
  // reason stated, which is the posture the tile's Save verb already uses -- an
  // absent control answers no question, and a slot that emptied itself would
  // collapse the tab row on every selection change.
  function unloadableBufferKey() {
    const key = activeBuffer;
    if (key === OUTLINE_BUFFER_KEY) return null;
    if (!state || !holdsBufferKey(key)) return null;
    const buffer = state.buffers[key];
    return (buffer && buffer.path !== null && buffer.path !== undefined)
      ? key : null;
  }

  function syncUnloadControl() {
    const key = activeBuffer;
    const unloadable = unloadableBufferKey() !== null;
    unloadBtn.disabled = !unloadable;
    unloadBtn.setAttribute("aria-disabled", unloadable ? "false" : "true");
    if (unloadable) {
      // It NAMES the buffer it would act on: one control that could unload any
      // loaded document must say which one it is aimed at, exactly as Cancel
      // does for the buffer it reverts.
      const buffer = state.buffers[key];
      const named = (buffer && buffer.path) ? String(buffer.path) : key;
      unloadBtn.title = "unload " + named + " from the loaded set";
      // Reachable: the control speaks for itself, so the note stands down.
      unloadNote.textContent = "";
      unloadNote.hidden = true;
      return;
    }
    let reason = UNLOAD_NOTHING_SELECTED_TITLE;
    if (key === OUTLINE_BUFFER_KEY) {
      reason = UNLOAD_OUTLINE_RESERVED_TITLE;
    } else if (key === UNBACKED_DOCUMENT_BUFFER_KEY) {
      // Only reachable for the UNBACKED slot now: a backed one under this same
      // reserved key is unloadable and never lands here.
      reason = UNLOAD_UNBACKED_DOCUMENT_TITLE;
    }
    unloadBtn.title = reason;
    unloadNote.textContent = reason;
    unloadNote.hidden = false;
  }

  // The click path. It re-derives reachability THROUGH THE SAME PREDICATE the
  // render used rather than trusting the render to have disabled the control --
  // the same belt-and-braces the rail's handler kept, and one rule rather than a
  // second copy of it, so a narrowing applied to one can never miss the other.
  // `discardUnsavedEdits` is never passed, because this control is unreachable
  // while anything is dirty.
  function unloadActiveBuffer() {
    const key = unloadableBufferKey();
    if (key === null) return;
    // `unloadDocument` owns the whole tail: it announces its own refusals, moves
    // the selection to the outline, and re-syncs the panel through
    // `syncBufferDom`. Only the SUCCESS line is this control's to add.
    const outcome = unloadDocument(key);
    if (outcome && outcome.ok === true) {
      stateEvent("unloaded " + key + " from the loaded set");
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
  function statusLine(key, buffer) {
    const dirtyText = bufferStatusText(key, buffer);
    // EVERY line NAMES ITS BUFFER (Brett's 2026-08-15 annotation round). The
    // two regions used to sit stacked in the chrome with no visible label, so a
    // clean canvas rendered "no unsaved changes" twice with nothing to
    // attribute either sentence to -- and a PARTIAL Save, whose whole point is
    // that one buffer committed and the other refused, was exactly the case
    // that unlabelled pair could not report. The accessible name carried the
    // buffer already; now the visible text does too.
    const prefix = bufferLabel(key) + ": ";
    if (savingKeys.has(key)) return prefix + "saving this buffer -- " + dirtyText;
    const outcome = statedOutcomes[key];
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

  function forgetStatedOutcome(key) {
    if (statedOutcomes[key] !== null) statedOutcomes[key] = null;
  }

  // The status is a function of CONTENT first: an unsaved-changes fact
  // always wins once there is any typed text, even for a buffer that
  // started `empty` or `unavailable` (the state module preserves that
  // load_state across every edit on purpose). An `unavailable` origin still
  // stays stated, alongside the dirty fact rather than instead of it -- a
  // later Save would still need to know the loaded base is unresolved.
  function bufferStatusText(key, buffer) {
    if (buffer.content === "") {
      if (buffer.load_state === "empty") {
        if (key === OUTLINE_BUFFER_KEY) {
          return "no outline yet -- start typing to create one";
        }
        // G-1: "no document selected" is only true where one COULD be.
        return (currentProjection.active_document_candidates || []).length
          ? "no document selected"
          : OUTLINE_ONLY_STATUS;
      }
      if (buffer.load_state === "unavailable") {
        // The buffer's KIND, not its key: a key is a path once the loaded set
        // widens, and "could not load this ideation/staging/x/detail.md" reads as
        // a sentence about a filename where the reader needed one about a buffer.
        return "source unavailable -- could not load this " + buffer.kind;
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
  function renderPreviewNow(key) {
    const buffer = state.buffers[key];
    let text;
    if (buffer.content !== "") {
      text = buffer.content;
    } else if (buffer.load_state === "empty") {
      text = emptyStatement(buffer.kind);
    } else if (buffer.load_state === "unavailable") {
      text = unavailableStatement(buffer.kind);
    } else {
      text = "";
    }
    mountSafeMarkdown(previews[key], text);
  }

  // Live typing is debounced; every other buffer-content change (initial
  // load, Discard, a document switch) renders at once -- there is nothing to
  // debounce about a single discrete action.
  function schedulePreview(key) {
    if (previewTimers[key]) clearTimeout(previewTimers[key].timer);
    let resolveFn;
    const promise = new Promise((resolve) => { resolveFn = resolve; });
    const timer = setTimeout(() => {
      previewTimers[key] = null;
      renderPreviewNow(key);
      resolveFn();
    }, previewDelayMs);
    previewTimers[key] = { timer, resolve: resolveFn, promise };
    return promise;
  }

  function flushOne(key) {
    const pending = previewTimers[key];
    if (!pending) return Promise.resolve();
    clearTimeout(pending.timer);
    previewTimers[key] = null;
    renderPreviewNow(key);
    pending.resolve();
    return Promise.resolve();
  }

  function flushPreview() {
    return Promise.all(bufferKeysNow().map((key) => flushOne(key)));
  }

  // A buffer's EDITOR is on screen only while that buffer is active AND the
  // `Editor` view tab is selected; its PREVIEW only while it is active and
  // `Preview` is selected. Two axes, one predicate each -- everything below
  // (focus, scroll capture, the D2 flush) keys on these rather than on the
  // buffer alone, which is what made the old single-axis bookkeeping correct
  // when there was only one axis.
  function editorVisible(key) {
    return key === activeBuffer && activeView === "editor";
  }

  function previewVisible(key) {
    return key === activeBuffer && activeView === "preview";
  }

  // ONE function owns what is on screen, because the two axes interact: which
  // buffer is active, and which view of it is selected. Ordering is
  // load-bearing throughout and each step says why.
  function applyVisibility() {
    // THE SET, read ONCE per pass. Every step below walks the SAME keys, so a
    // load or an unload cannot land between two steps and leave one of them
    // walking a set the others did not.
    const keys = bufferKeysNow();
    // 1. CAPTURE FIRST. FR-010's selection/scroll clause (T104: `viewState` was
    //    exported with no production caller and NOTHING ever wrote the values
    //    back): hiding a pane drops its layout box, and the browser drops the
    //    textarea's scroll offset with it -- so the view is captured on the way
    //    out, BEFORE anything below is hidden, and re-applied on the way back.
    for (const key of keys) {
      if (editorShown[key] && !editorVisible(key)) {
        rememberedView[key] = viewState(key);
      }
    }
    // 2. D2: a preview about to BECOME visible is brought up to the buffer's
    //    current content first, so the switch never displays a rendering the
    //    debounce had not yet applied. The existing flush, the existing single
    //    rendering path -- no second pipeline. Switching into `Editor` needs no
    //    such step: raw text is never debounced.
    for (const key of keys) {
      if (previewVisible(key) && !previewShown[key]) flushOne(key);
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
    for (const key of keys) {
      const isActive = key === activeBuffer;
      bufferBoxes.editor[key].hidden = !isActive;
      bufferBoxes.preview[key].hidden = !isActive;
    }
    // 5. RESTORE LAST, and only for an editor that just appeared. A hidden pane
    //    cannot hold real focus; a shown one that previously held it gets it
    //    back, and one that never held focus never steals it. Scroll is
    //    re-applied after focus() because focus may scroll the caret into view
    //    and must not win over the human's place.
    for (const key of keys) {
      const nowVisible = editorVisible(key);
      if (nowVisible && !editorShown[key]) {
        if (rememberedFocus[key]) textareas[key].focus();
        const view = rememberedView[key];
        if (view) {
          const textarea = textareas[key];
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
      editorShown[key] = nowVisible;
      previewShown[key] = previewVisible(key);
    }
  }

  // WHICH BUFFER. The context region calls this (through the composition), and
  // so does the chat rail's loaded-document selector; the view tabs never do --
  // they answer which VIEW, and a realization that let them choose a buffer is
  // exactly what the delta refuses.
  //
  // Selection has exactly ONE value (design D7): `state.active_buffer`. Three
  // routes reach it -- this method, a load, and the `outline` selection tab --
  // and all three land here or in `loadDocumentForEditing`, which is what lets
  // the requirement say the selector, the canvas and the chat must agree.
  function setActiveBuffer(key) {
    if (destroyed) return activeBuffer;
    if (!holdsBufferKey(key)) {
      // MEMBERSHIP, not a name list. Phase A asked `BUFFER_KINDS.includes(key)`
      // and called that "reading the enumeration"; under Phase B the kind
      // vocabulary is not the key set, so the honest question is whether this
      // canvas HOLDS the buffer -- which refuses an unloaded path, an unloaded
      // key, and a typo alike, and stays true however wide the set becomes.
      throw new TypeError("setActiveBuffer key must name a buffer this canvas holds");
    }
    if (activeBuffer === key) return activeBuffer;
    activeBuffer = key;
    if (state) state = adoptActiveBuffer(state, key);
    applyVisibility();
    syncPanelControls();   // Cancel is aimed at the buffer that just changed
    persistNow();
    // GATED, NOT BUILT: switching the selected document must also switch which
    // per-document THREAD the chat shows and appends to, and (through the adapter)
    // which harness session it speaks to. Both are tasks.md §9 threads and §11
    // harness bridge, downstream of the blocking verify list, so this slice
    // deliberately stops at the notification below.
    notifyLoadedSetChanged();
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
  function focusBufferEditor(key) {
    setActiveView("editor");
    const target = editorVisible(key) ? key : activeBuffer;
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

  async function edit(key, text) {
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    // The bytes handed to the seam are the bytes the verdict will describe, so
    // they may not move underneath it. Refused visibly, like every other
    // refused edit -- the keystroke never just vanishes.
    if (saving) return { ok: false, error: EDIT_DURING_SAVE_REASON };
    // T104 F6-2/F6-6: no working state yet (or ever, after a failed load) --
    // a stated refusal, never a TypeError off `state.buffers` below.
    if (!state) return { ok: false, error: unloadedReason() };
    // PHASE B: the key space is OPEN (any repository path could be named), so an
    // unheld key is refused with a stated reason rather than dereferenced. Under
    // Phase A the two names were the only reachable arguments and this could not
    // arise; widening the set widens what a caller can get wrong.
    if (!holdsBufferKey(key)) return { ok: false, error: NOT_LOADED_REASON };
    forgetStatedOutcome(key);
    const before = state.buffers[key];
    const pending = beginBufferEdit(before, text, hashOptions);
    state = replaceBuffer(state, pending.buffer);
    syncBufferDom(key);
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
      if (state.buffers[key].hash_generation === pending.buffer.hash_generation) {
        state = replaceBuffer(state, before);
        syncBufferDom(key);
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
    const settled = settleBufferHash(state.buffers[key], completion);
    if (settled.applied) {
      state = replaceBuffer(state, settled.buffer);
      syncBufferDom(key);
      schedulePreview(key);
      persistNow();
      // T100 P1-A: tell the composition a buffer identity moved, so the
      // chat rail can refresh proposal CURRENCY in the rendered DOM (the
      // model rule existed; this is the missing view wiring).
      if (typeof onIdentitySettled === "function") {
        onIdentitySettled(key, settled.buffer.current_hash);
      }
    }
    return { ok: true, error: null };
  }

  function discard(key) {
    if (destroyed) return Promise.resolve({ ok: false, error: DESTROYED_REASON });
    if (saving) return Promise.resolve({ ok: false, error: SAVE_BUSY_REASON });
    // T104 F6-2/F6-6: the same stated refusal as edit() -- there is no buffer
    // to restore before the load settles.
    if (!state) return Promise.resolve({ ok: false, error: unloadedReason() });
    if (!holdsBufferKey(key)) {
      return Promise.resolve({ ok: false, error: NOT_LOADED_REASON });
    }
    forgetStatedOutcome(key);
    const discarded = discardBuffer(state.buffers[key]);
    state = replaceBuffer(state, discarded);
    syncBufferDom(key);
    renderPreviewNow(key);
    persistNow();
    // T104 F6-1: Discard MOVES the buffer's identity (current_hash goes back
    // to the base), so the composition must hear it exactly like an edit --
    // otherwise the rail's proposal cards keep 'current' + an enabled Apply
    // against text the buffer no longer holds.
    if (typeof onIdentitySettled === "function") {
      onIdentitySettled(key, discarded.current_hash);
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
    const key = activeBuffer;
    const result = await discard(key);
    if (!result.ok) return { ...result, key };
    statedOutcomes[key] = "Cancel reverted the " + bufferLabel(key)
      + " buffer to its last loaded or saved text";
    syncBufferDom(key);
    return { ok: true, key };
  }

  // ---- the governed Save, entirely behind the posture gate ----------------

  // What one changed buffer is handed over as. The seam is given FACTS about the
  // buffer and no instructions: which existing action to use, and in which
  // order, are the orchestrator's answers (./doxbench-save.js), and whether the
  // write is permitted at all is the gate's.
  function bufferRequestRow(key) {
    const buffer = state.buffers[key];
    return {
      // THE BUFFER KEY, which Phase A spelled `kind`. `savePlanState` keys its
      // rows by `row.key ?? row.kind`, and the field had to be renamed rather
      // than left to carry a PATH under the word `kind` -- which would be a false
      // statement about the field, and the same rename ./doxbench-save.js made to
      // its plan and outcome rows for the same reason.
      key,
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

  function unchangedRow(key) {
    return {
      key, status: "unchanged", action: null, ref: null, revision: null,
      content_hash: null, message: null,
    };
  }

  function outcomeRowsOf(outcome) {
    return outcome && Array.isArray(outcome.buffers) ? outcome.buffers : [];
  }

  // The commits `save()` could not adopt, off the outcome it annotated (#290).
  // ONE reader for the field, so every surface that reports "why is this buffer
  // still dirty" answers from the same list rather than from its own idea of it.
  function unadoptedRowsOf(outcome) {
    return outcome && Array.isArray(outcome.unadopted) ? outcome.unadopted : [];
  }

  function outcomeReasonFor(key, outcome) {
    // #290: A COMMIT THIS CANVAS COULD NOT ADOPT IS ASKED ABOUT FIRST. Its row
    // says `committed` -- the server did commit -- so answering from the row
    // hands the caller "saved as edit-document on draft/…" about a buffer that
    // is still dirty, which is the sentence the document-switch guard printed
    // under "Save did not land the Document buffer". The honest answer is the
    // one the buffer's own status region is already showing.
    for (const row of unadoptedRowsOf(outcome)) {
      if (row && row.key === key) return row.message + ".";
    }
    for (const row of outcomeRowsOf(outcome)) {
      if (row && row.key === key) return saveOutcomeSentence(row) + ".";
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
  //
  // `options.only` (design D4) NARROWS the act to one document plus the
  // outline-ancestry step, which is what a `docs` tile's own Save is. It is a
  // RESTRICTION and never a widening: the pipeline, the seam, the ordering rule,
  // the per-buffer report and the authority are all the ones the canvas Save
  // uses, and the only difference is that fewer buffers are offered. There is no
  // force, no bypass and no second write route here -- an additional entry point
  // MUST NOT widen what the act may do (the ratified control-authority scenario).
  async function save(options = {}) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (!saveSeam) return { status: "refused", reason: SAVE_UNAVAILABLE_REASON };
    if (saving) return { status: "refused", reason: SAVE_BUSY_REASON };
    // T104 F6-2/F6-6: nothing loaded means nothing to hand the seam.
    if (!state) return { status: "refused", reason: unloadedReason() };
    const only = options.only === undefined || options.only === null
      ? null
      : [].concat(options.only);
    // THE SCOPE OF THIS ACT. Unscoped it is every buffer the canvas holds; scoped
    // it is the named documents PLUS the outline, because the ancestry step cannot
    // be skipped -- a scoped entry point that skipped it would be a way to commit
    // a document without the ancestry the ordering rule requires. The scope is
    // intersected with the keys the state HOLDS, so a caller naming an unloaded
    // key narrows to the ancestry step rather than inventing a buffer.
    const held = bufferKeysNow();
    const scope = only === null
      ? held
      : held.filter((key) => key === OUTLINE_BUFFER_KEY || only.includes(key));
    const changed = scope.filter((key) => state.buffers[key].dirty);
    if (!changed.length) {
      // Nothing to persist reaches no governance action at all: the seam is not
      // called in order to discover it had nothing to do. Only the buffers IN
      // SCOPE are restated: claiming `unchanged` for a document this act was not
      // about would be a verdict about a buffer nobody asked after.
      for (const key of scope) {
        statedOutcomes[key] = saveOutcomeSentence(unchangedRow(key));
        syncBufferDom(key);
      }
      return {
        status: "unchanged", reason: null,
        buffers: scope.map(unchangedRow),
      };
    }
    saving = true;
    for (const key of changed) savingKeys.add(key);
    for (const key of scope) {
      forgetStatedOutcome(key);
      syncBufferDom(key);      // states the busy fact; moves no focus
    }
    let outcome = null;
    let failure = null;
    try {
      outcome = await saveSeam({
        key: scopeKey(),
        buffers: changed.map(bufferRequestRow),
        // THE SCOPE, ON THE REQUEST. The orchestrator's own `only` (design D4)
        // is what keeps the ancestry step in and every other loaded document out,
        // so the composition that builds the seam forwards this field into
        // `runSave`. Absent (the canvas Save) it is simply not there, and the
        // whole-canvas behaviour is byte-for-byte Phase A's.
        ...(only === null ? {} : { only }),
      });
    } catch (error) {
      failure = (error && error.message) || "unknown error";
    } finally {
      saving = false;
      savingKeys.clear();
    }
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (failure !== null) {
      // A seam that threw persisted nothing this canvas can see, so no base
      // moves and every buffer it was handed says what happened.
      const reason = "the Save seam failed -- " + failure;
      for (const key of changed) statedOutcomes[key] = "Save refused -- " + reason;
      for (const key of scope) syncBufferDom(key);
      stateEvent("Save refused -- " + reason);
      return { status: "refused", reason };
    }
    let landedRef = null;
    // T104 F6-1: the buffers whose base actually ADVANCED through
    // adoptSavedBase -- exactly the identities the composition must re-score
    // proposal currency against, and ONLY those (a refused buffer's identity
    // did not move, so no notification may claim it did).
    const adoptedKeys = [];
    // #290: …and the buffers whose commit this canvas COULD NOT adopt --
    // the exact complement, and a fact NO outcome row carries. The row says
    // `committed`, because the server did commit; the adoption that failed is
    // this canvas's own act, discovered here and nowhere else. Left here it was
    // reported to the human (their buffer stayed dirty and said so) and hidden
    // from every reader of the Save's answer, so `tileSaveVerdict` computed
    // success from rows that had no way to know. It therefore travels WITH the
    // outcome, below, in the same sentence the buffer's own region carries.
    const unadopted = [];
    // R-5 (#81): THE ONE VISIBLE LINE IS A CHOICE, so it is made ONCE, here,
    // rather than by whichever row happened to be reported last. Rows arrive in
    // SAVE ORDER, and a Save that refused the ancestry step reports the outline's
    // refusal followed by one `not_attempted` per document BECAUSE OF IT -- a
    // cause and its consequences. Calling `stateEvent` per row let every later
    // consequence overwrite the cause, so the human read "the outline did not
    // land" off the last document and the refusal that produced it never
    // appeared. The line therefore carries the FIRST row with something to
    // report, which in save order is the first failing cause. Nothing is hidden
    // by choosing: every row still gets its own durable sr-only sentence, which
    // is where the per-buffer report lives (FR-035).
    let leadEvent = null;
    const leadWith = (text) => { if (leadEvent === null) leadEvent = text; };
    for (const row of outcomeRowsOf(outcome)) {
      // A verdict about a buffer this canvas does not hold is skipped, not
      // applied: `holdsBufferKey` asks the STATE, so an outcome row naming an
      // unloaded key (or a key from a stale in-flight answer) can never be
      // adopted onto a buffer that is not there.
      if (!row || !holdsBufferKey(row.key)) continue;
      if (row.status === "committed") {
        try {
          // The key is passed EXPLICITLY, so the advanced buffer lands under the
          // key the verdict named rather than being re-resolved from its path.
          // The two agree today; stating it means a create's not-yet-pathed
          // buffer can never quietly move keys on a Save.
          state = replaceBuffer(
            state, adoptSavedBase(state.buffers[row.key], row), row.key);
          adoptedKeys.push(row.key);
          if (landedRef === null && typeof row.ref === "string") landedRef = row.ref;
        } catch (error) {
          // A commit whose reported identity the state module refuses is NOT
          // adopted: the buffer keeps its text and its dirty flag, and the
          // human is told, rather than being handed a base nothing can verify.
          statedOutcomes[row.key] = unadoptedCommitReason(error && error.message);
          leadWith(bufferLabel(row.key) + ": " + statedOutcomes[row.key]);
          // THE SAME SENTENCE, carried out of here (#290). Not a second wording
          // of the same fact: the verdict a tile reads and the region a human
          // reads are then incapable of contradicting each other, which is the
          // whole complaint -- `ok: true` over a region saying "unsaved".
          unadopted.push(Object.freeze({
            key: row.key, message: statedOutcomes[row.key] }));
          continue;
        }
      }
      statedOutcomes[row.key] = saveOutcomeSentence(row);
      // A committed buffer needs no event: Save going disabled and the buffer
      // going clean IS the report. Neither does an `unchanged` one -- there was
      // nothing to save in it, which is not something a human must be told over
      // the thing that actually failed. That row used to arrive FIRST from the
      // orchestrator itself (a tile Save scoped to one document, the reserved
      // outline key prepended whether the state held one or not), so offering
      // the line to every row that was not committed handed it the vacuous row
      // and buried the refusal -- #81 again, from the other end. Issue #291
      // stopped the orchestrator inventing that row, and the guard below still
      // stands regardless: the rows this loop reads are whatever the SEAM
      // reports, and `unchanged` remains a status a seam may state.
      //
      // The offer therefore comes from the WITHHELD set, which is the same set
      // `tileSaveVerdict` leads with (`refused`/`not_attempted`), so the two
      // surfaces agree in fact rather than only in the common case. A commit
      // this canvas could not adopt offers the line too, from its own branch
      // above. There is one line and there may be several such rows, so the
      // offer is only taken by the first of them (`leadWith`, above).
      if (row.status === "refused" || row.status === "not_attempted") {
        leadWith(bufferLabel(row.key) + ": " + saveOutcomeSentence(row));
      }
    }
    // …and the chosen line is shown once, after every row has been read, so the
    // one on screen is the first failing cause and not the last consequence.
    stateEvent(leadEvent);
    // #290: THE ADOPTION RESULT TRAVELS WITH THE OUTCOME. What the seam
    // returned is what the governed Save DID, and it is not touched -- a row
    // that committed still says `committed`, because rewriting the server's own
    // verdict would be a false statement in the other direction. What is added
    // is what this canvas then did with it, which no row could carry and which
    // every reader of this answer needs: the commits it could not adopt, named,
    // with the reason the human is already reading. It is an array on EVERY
    // answer a seam returned -- empty when everything was adopted -- so a
    // reader never has to tell an empty list apart from a silent one. (The
    // refusals above return before a seam is reached: there is no outcome to
    // annotate, and `tileSaveVerdict` reads the field defensively for exactly
    // that reason.)
    const settled = outcome && typeof outcome === "object"
      ? Object.freeze({ ...outcome, unadopted: Object.freeze(unadopted) })
      : outcome;
    const previousRef = scopeKey().ref;
    if (landedRef !== null) rekeyTo(landedRef);
    for (const key of scope) syncBufferDom(key);
    persistNow();
    // T104 F6-1: adoption moved these buffers onto the server-reported
    // identity, so the composition hears it AFTER adoptSavedBase (and the
    // rekey) landed -- with the post-transition hash, the same shape edit()
    // reports.
    if (typeof onIdentitySettled === "function") {
      for (const key of adoptedKeys) {
        onIdentitySettled(key, state.buffers[key].current_hash);
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
        await onSaveLanded(landedRef, settled);
      } catch (unused) {
        // the seam's own detail is dropped unread; the Save still landed
      }
    }
    return settled;
  }

  // THE TILE SAVE (design D4, and the `docs`-tile requirement's SAVE verb). ONE
  // MECHANISM, A SECOND ENTRY POINT -- which is the opposite of a second save
  // path: it calls the SAME `save()` above with `only` set, so the ordering rule,
  // the seam, the gate, the per-buffer verdicts and the surfaces they are reported
  // on are all unchanged, and the outline's ancestry step still runs and still
  // REPORTS. It refuses everything `save()` refuses, plus a key this canvas does
  // not hold and the outline itself (the outline's own control is the canvas
  // Save; a "tile save" for the outline would be a third Save with no tile).
  // ITS ANSWER carries BOTH readings of the same verdict, and hides neither: the
  // full per-buffer report (`status` + `buffers`, exactly what `save()` returns,
  // because it IS what `save()` returned) AND the `{ok, error}` pair a tile's own
  // note reads. `ok` is true only where nothing was refused and nothing was left
  // unattempted, so a PARTIAL — the outline landed, the document did not, or the
  // reverse — reads as NOT ok on the tile while staying separately readable per
  // buffer, which is the case the ratified per-buffer reporting rule exists for.
  //
  // #290: `ok` IS COMPUTED FROM BOTH HALVES OF WHAT HAPPENED -- what the
  // governed Save reported per buffer, AND what this canvas could do with it.
  // It used to read the rows alone, which cannot see an adoption failure: the
  // row of a commit this canvas refused to adopt says `committed` (the server
  // committed it) and the whole-Save status says `committed` too, so the tile
  // reported `ok: true, error: null` over a buffer whose own status region said
  // it kept its unsaved text. A tile MUST NOT be able to claim a success the
  // buffer beside it contradicts, so the unadopted set is a failing cause here
  // exactly as a refusal is -- whatever future trigger reaches that branch.
  //
  // The chosen sentence follows the SAME rule as the one visible line (#81):
  // the FIRST failing cause in save order, since rows arrive as a cause and its
  // consequences. `outcome.status` is left exactly as the Save stated it; it is
  // the governed action's own verdict, and this canvas's failure to adopt is
  // not a fact about what the server did.
  function tileSaveVerdict(outcome) {
    const rows = outcomeRowsOf(outcome);
    const unadopted = new Map(
      unadoptedRowsOf(outcome).map((row) => [row.key, row.message]));
    let lead = null;
    let failed = false;
    for (const row of rows) {
      // An unadopted row is read FIRST: it is a `committed` row, so asking the
      // withheld question about it would answer "nothing wrong here".
      const failure = unadopted.has(row.key)
        ? unadopted.get(row.key)
        : ((row.status === "refused" || row.status === "not_attempted")
          ? saveOutcomeSentence(row)
          : null);
      if (failure === null) continue;
      failed = true;
      if (lead === null) lead = failure;
    }
    const ok = !failed
      && (outcome.status === "committed" || outcome.status === "unchanged");
    const error = ok
      ? null
      : (lead || outcome.reason || "the governed Save reported no verdict");
    return { ...outcome, ok, error };
  }

  async function saveDocument(key) {
    if (destroyed) {
      return { status: "refused", reason: DESTROYED_REASON,
               ok: false, error: DESTROYED_REASON };
    }
    if (!state) {
      return { status: "refused", reason: unloadedReason(),
               ok: false, error: unloadedReason() };
    }
    if (key === OUTLINE_BUFFER_KEY) {
      return { status: "refused", reason: OUTLINE_HAS_NO_TILE_SAVE_REASON,
               ok: false, error: OUTLINE_HAS_NO_TILE_SAVE_REASON };
    }
    if (!holdsBufferKey(key)) {
      return { status: "refused", reason: NOT_LOADED_REASON,
               ok: false, error: NOT_LOADED_REASON };
    }
    // A context-only buffer is withheld by ./doxbench-save.js with its own stated
    // reason, and the tile must not offer a reachable Save for it at all (design
    // D2) -- so this states the absence HERE rather than letting the human learn
    // it from a refusal after the act. It confers nothing either way: `owned` is
    // presentation input, and the gate answers ownership for every request it
    // does receive from its own rule.
    if (state.buffers[key].owned !== true) {
      return { status: "refused", reason: CONTEXT_ONLY_SAVE_REASON,
               ok: false, error: CONTEXT_ONLY_SAVE_REASON };
    }
    return tileSaveVerdict(await save({ only: key }));
  }

  // ---- THE LOADED SET: one way in, one way out ----------------------------

  // What the chat rail's selector and the wheel's tile marking render. Documents
  // only -- the outline is not a loaded document, it is the reserved buffer every
  // session has -- in the state module's declared order, frozen so a caller
  // cannot mutate the answer and call it state.
  //
  // THE RESERVED UNBACKED SLOT IS NOT A LOADED DOCUMENT WHILE IT HAS NO PATH.
  // Every mount builds it (it is the create flow's not-yet-created artifact), so
  // listing it unconditionally would mean the selector could NEVER render its
  // empty state -- and "nothing is loaded yet" is a state the ratified selector
  // requirement says must be rendered honestly rather than hidden. The moment the
  // slot names a document (Phase A's selection route puts a real path there) it
  // IS a document the human is working on, and it is listed, under the reserved
  // label the whole surface already uses for it.
  function loadedBuffers() {
    if (!state) return Object.freeze([]);
    const listed = loadedDocumentKeys(state).filter(
      (key) => state.buffers[key].path !== null);
    return Object.freeze(listed.map((key) => {
      const buffer = state.buffers[key];
      return Object.freeze({
        key,
        path: buffer.path,
        label: bufferLabel(key),
        // Carried so the tile can withhold its Save and its must-save marking for
        // read-only context material instead of stating an authority it lacks.
        owned: buffer.owned,
        dirty: buffer.dirty,
        active: key === activeBuffer,
      });
    }));
  }

  function bufferKeys() {
    return Object.freeze(Array.from(bufferKeysNow()));
  }

  // THE ONE ENTRY ROUTE INTO THE LOADED SET (design D5). Reads the document
  // through the SAME injected `loadSource` seam `selectDocument` uses -- no second
  // read path, no transport of its own -- adds it under its PATH key, gives it its
  // DOM, and selects it.
  //
  // Four refusals, each stating its own situation and changing nothing:
  //   * out of scope -- FR-007's rule, unchanged: a path this scope never declared
  //     is refused outright rather than loaded.
  //   * the BOUND -- refused with the MEASURED number (design D6). Nothing already
  //     loaded is evicted, because every loaded buffer may hold unsaved work and a
  //     policy that evicts to make room is a policy that discards human text.
  //   * a load that could not be read or hashed -- the state module's own message
  //     (byte counts and classes only, never document text).
  //   * a Save in flight -- the bytes handed over may not move underneath it.
  // And ONE non-refusal that is easy to get wrong: a path the loaded set ALREADY
  // holds is SELECTED and reported `already_loaded`, without re-reading source,
  // because re-reading would silently discard that buffer's unsaved text.
  async function loadDocumentForEditing(path, loadOptions = {}) {
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    if (!state) return { ok: false, error: unloadedReason() };
    if (typeof path !== "string" || path === "") {
      return refuseLoad(path, "a load must name a document path");
    }
    // Stated, not merely returned: a click that appears to do nothing is the
    // failure mode every refusal on this surface exists to prevent.
    if (saving) return refuseLoad(path, SAVE_BUSY_REASON);
    const existing = documentKeyForPath(path);
    if (existing !== null) {
      setActiveBuffer(existing);
      return { ok: true, key: existing, already_loaded: true, error: null };
    }
    if (!isInScope(path)) return refuseLoad(path, "out_of_scope");
    const bound = Number.isSafeInteger(loadOptions.maxLoadedDocuments)
      ? loadOptions.maxLoadedDocuments
      : maxLoadedDocuments;
    const measured = loadedDocumentKeys(state).length;
    if (measured >= bound) {
      // Refused BEFORE the source is read: a refusal that first reads the document
      // it is about to decline has done work the human never authorised, and the
      // rail-before-provider ordering is this surface's house pattern.
      return refuseLoad(path, boundReachedReason(bound, measured), {
        refusal: LOAD_REFUSED_BOUND_REACHED, bound, measured,
      });
    }
    let buffer;
    try {
      const descriptor = await loadDescriptor("document", path);
      buffer = await createBufferState(
        { kind: "document", repository: scopeKey().repository, ...descriptor },
        hashOptions,
      );
    } catch (error) {
      if (destroyed) return { ok: false, error: DESTROYED_REASON };
      return refuseLoad(
        path,
        error instanceof ContentEncodingError || error instanceof ContentSizeError
          ? error.message
          : "this document could not be loaded",
      );
    }
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    const result = loadDocumentBuffer(state, buffer, { maxLoadedDocuments: bound });
    if (result.loaded !== true) {
      // The state module is the authority on membership, so its refusal wins even
      // where the checks above already answered -- and both refusals are stated in
      // the module's own vocabulary rather than reduced to a generic failure.
      state = result.state;
      if (result.refusal === LOAD_REFUSED_ALREADY_LOADED && result.key) {
        activeBuffer = result.key;
        applyVisibility();
        syncPanelControls();
        persistNow();
        notifyLoadedSetChanged();
        return { ok: true, key: result.key, already_loaded: true, error: null };
      }
      let reason = "this document could not join the loaded set";
      if (result.refusal === LOAD_REFUSED_BOUND_REACHED) {
        reason = boundReachedReason(result.bound, result.measured);
      } else if (result.refusal === LOAD_REFUSED_RESERVED_KEY) {
        reason = reservedKeyReason(path);
      }
      return refuseLoad(path, reason,
        { refusal: result.refusal, bound: result.bound, measured: result.measured },
      );
    }
    state = result.state;
    // The DOM for a key the set just GAINED, and the labels for the whole set --
    // a basename collision arriving now lengthens the label of the document that
    // was already there, not only of this one.
    ensureBufferDom(result.key);
    refreshBufferLabels();
    // `loadDocumentBuffer` already made this the selected buffer in the STATE (one
    // selection value, three routes -- design D7), so the controller mirrors it
    // rather than calling setActiveBuffer and settling the same fact twice.
    activeBuffer = result.key;
    applyVisibility();
    syncBufferDom(result.key);
    renderPreviewNow(result.key);
    persistNow();
    // A brand-new buffer is the largest identity move there is, so the composition
    // hears it exactly as it hears an edit, a discard or a switch.
    if (typeof onIdentitySettled === "function") {
      onIdentitySettled(result.key, buffer.current_hash);
    }
    // GATED, NOT BUILT: a newly loaded document also gets its own THREAD sidecar
    // (tasks.md §9) and joins the staged-set knowledge service's packet
    // (tasks.md §10), both downstream of the blocking verify list.
    notifyLoadedSetChanged();
    return {
      ok: true, key: result.key, already_loaded: false, error: null,
      bound: result.bound, measured: result.measured,
    };
  }

  // THE ONE WAY OUT. A dirty buffer is REFUSED unless the caller states the
  // discard explicitly, because dropping it destroys unsaved work exactly as
  // Cancel does -- and Cancel at least says which buffer it reverted.
  //
  // THE ASYMMETRY RECORDED HERE ON 2026-08-21 IS LARGELY DISSOLVED, and by the
  // UI moving to meet this method rather than the other way round. It used to be
  // that this method hard-refused only the OUTLINE key while every UI path
  // withheld BOTH reserved keys. Amendment 2 (Brett, ruled via browser
  // annotation the same day) narrowed the reserved set to the outline alone, so
  // the two layers now name the same permanent refusal.
  //
  // What remains is not an asymmetry of AUTHORITY but of SUBJECT: the canvas
  // control additionally withholds an UNBACKED buffer, because a slot that names
  // no document has no loaded-set membership to end. This method still accepts
  // that key and the state module still honours it, which is right for a public
  // method -- a caller that genuinely wants the create slot out of the set is
  // asking a coherent question. It is simply not a question a control with no
  // subject can pose.
  function unloadDocument(key, unloadOptions = {}) {
    if (destroyed) return { ok: false, error: DESTROYED_REASON };
    if (saving) return { ok: false, error: SAVE_BUSY_REASON };
    if (!state) return { ok: false, error: unloadedReason() };
    if (key === OUTLINE_BUFFER_KEY) {
      return { ok: false, error: OUTLINE_IS_RESERVED_REASON };
    }
    if (!holdsBufferKey(key)) return { ok: false, error: NOT_LOADED_REASON };
    const discardUnsavedEdits = unloadOptions.discardUnsavedEdits === true;
    const result = unloadDocumentBuffer(state, key, { discardUnsavedEdits });
    if (result.unloaded !== true) {
      const reason = result.refusal === UNLOAD_REFUSED_DIRTY
        ? UNLOAD_DIRTY_REASON
        : "this document could not leave the loaded set";
      stateEvent(bufferLabel(key) + ": " + reason);
      return { ok: false, error: reason, refusal: result.refusal };
    }
    state = result.state;
    // A pending preview render for a buffer that is GONE would dereference a
    // buffer the state no longer holds, so the timer is cleared here rather than
    // left to fire against an absent key.
    if (previewTimers[key]) {
      clearTimeout(previewTimers[key].timer);
      previewTimers[key].resolve();
      previewTimers[key] = null;
    }
    // The nodes stay in the panes, hidden and blanked, and their registry entry
    // stays with them: re-loading the same path then REUSES the boxes it already
    // had. Removing them and rebuilding on a re-load is the version of this that
    // orphans a pane full of dead boxes, and `ensureBufferDom` is idempotent
    // precisely so this half can be the cheap one.
    bufferBoxes.editor[key].hidden = true;
    bufferBoxes.preview[key].hidden = true;
    textareas[key].disabled = true;
    statusEls[key].textContent = "";
    statusEls[key].hidden = true;
    statedOutcomes[key] = null;
    rememberedFocus[key] = false;
    rememberedView[key] = null;
    editorShown[key] = false;
    previewShown[key] = false;
    // The state module moved the selection to the outline when the unloaded buffer
    // held it; the controller mirrors that one value rather than deciding it.
    activeBuffer = state.active_buffer;
    refreshBufferLabels();
    applyVisibility();
    syncBufferDom(activeBuffer);
    persistNow();
    notifyLoadedSetChanged();
    return { ok: true, error: null };
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
    forgetStatedOutcome(UNBACKED_DOCUMENT_BUFFER_KEY);
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
    // THE RESERVED SELECTION SLOT, NAMED EXPLICITLY. Phase B's `replaceBuffer`
    // resolves an omitted key by PATH, so a switch to a different document would
    // have landed as a NEW key beside the old one instead of replacing the buffer
    // the docs wheel is driving -- two buffers for one selection, and the state
    // module's own duplicate-path refusal waiting the moment the paths met. The
    // reserved `document` key is exactly what this route has always used (the
    // state module admits a path-backed buffer there, which is why a Phase A
    // session restores unchanged), so stating it keeps this route's behaviour
    // byte-for-byte what it was. Joining the LOADED SET is a different act with a
    // different route: `loadDocumentForEditing`.
    state = replaceBuffer(state, buffer, UNBACKED_DOCUMENT_BUFFER_KEY);
    activeDocumentPath = path;
    // PR #196 review F7: the remembered caret and scroll belong to the
    // document that just LEFT. Re-applying them to whatever the next document
    // happens to be puts the human at an offset with no relationship to the
    // text under it (and, past the new document's end, at a caret the browser
    // silently clamps). A whole-buffer replacement has no view to remember, so
    // the entry is dropped rather than carried across.
    rememberedView[UNBACKED_DOCUMENT_BUFFER_KEY] = null;
    // Phase A: loading a document IS binding to it. The canvas presents the
    // active buffer and the chat works on it, so a switch that left the outline
    // active would show one thing and edit another.
    // F9: `setActiveBuffer` notifies ONLY when the selection actually moves --
    // it early-returns on an already-active key. So whether this switch has
    // already fired the tail depends on where the selection was, and the tail
    // below is conditioned on exactly that. Both cases must fire it once: a
    // switch that moved the selection is covered by `setActiveBuffer`, and one
    // that did not still replaced the whole buffer's CONTENT, which the wheel
    // and the selector need to hear.
    const selectionMoved = activeBuffer !== UNBACKED_DOCUMENT_BUFFER_KEY;
    setActiveBuffer(UNBACKED_DOCUMENT_BUFFER_KEY);
    syncBufferDom(UNBACKED_DOCUMENT_BUFFER_KEY);
    renderPreviewNow(UNBACKED_DOCUMENT_BUFFER_KEY);
    persistNow();
    // T104 F6-1: a switch replaces the WHOLE Document buffer, the largest
    // identity move of all -- the composition hears the new buffer's settled
    // identity so stale proposal cards drop their 'current' claim.
    if (typeof onIdentitySettled === "function") {
      onIdentitySettled(UNBACKED_DOCUMENT_BUFFER_KEY, buffer.current_hash);
    }
    // …and only when `setActiveBuffer` did not already say it.
    if (!selectionMoved) notifyLoadedSetChanged();
    return { status: "switched", reason: null };
  }

  // ONE refusal vocabulary for BOTH routes into selectDocument -- the context
  // region's scoped docs selection and this module's own picker. The sentence
  // is stated HERE rather than at either caller, so neither can drift and
  // neither can refuse silently (CHK016/CHK019). "blocked" is deliberately not
  // routed through it: the guard IS its own statement.
  function refuseSelection(reason) {
    const sentence = bufferLabel(UNBACKED_DOCUMENT_BUFFER_KEY)
      + ": refused -- " + reason;
    const region = statusEls[UNBACKED_DOCUMENT_BUFFER_KEY];
    if (region) region.textContent = sentence;
    stateEvent(sentence);
    return { status: "refused", reason };
  }

  // The LOAD verb's own refusal, in the same one-vocabulary discipline: the
  // sentence is stated here so no caller can drift and none can refuse silently.
  // It names the document by its BASENAME rather than by a buffer label, because a
  // refused load has no buffer to be labelled -- that is what was refused.
  function refuseLoad(path, reason, extra = {}) {
    const named = path ? basename(path) : "this document";
    stateEvent(named + ": refused -- " + reason);
    return { ok: false, key: null, error: reason, ...extra };
  }

  async function selectDocument(path) {
    if (destroyed) return { status: "refused", reason: DESTROYED_REASON };
    if (saving) return refuseSelection(SAVE_BUSY_REASON);
    // T104 F6-2/F6-6: refused BEFORE the unchanged/scope answers -- with no
    // state there is no dirty check to run and nothing to switch away from,
    // and "unchanged" would be a claim about a buffer that does not exist.
    if (!state) return refuseSelection(unloadedReason());
    if (path === activeDocumentPath) {
      // Already in the reserved selection slot, so nothing switches -- but
      // choosing it is still an act of BINDING, and the chat follows the active
      // buffer.
      setActiveBuffer(UNBACKED_DOCUMENT_BUFFER_KEY);
      return { status: "unchanged", reason: null };
    }
    // PHASE B: a path the LOADED SET already holds under its own key is SELECTED,
    // never re-read. Two reasons, and both are ratified rules rather than
    // conveniences: re-reading would silently discard that buffer's unsaved text
    // ("A document already loaded is loaded again"), and a second buffer claiming
    // one path is a state the module refuses outright -- which this route would
    // otherwise have walked straight into by loading it into the reserved slot.
    const alreadyLoaded = documentKeyForPath(path);
    if (alreadyLoaded !== null) {
      setActiveBuffer(alreadyLoaded);
      return { status: "unchanged", reason: null };
    }
    if (path !== null && !isInScope(path)) {
      // FR-007: "the explicitly selected SCOPED document" -- a path this
      // scope never declared (neither context nor editable) is refused
      // outright, never loaded and never silently substituted.
      return refuseSelection("out_of_scope");
    }
    // The guard is about the RESERVED SELECTION SLOT's own unsaved text, which is
    // the buffer this route is about to replace. A session restored without that
    // slot (Phase B can unload it) has nothing to guard, and reading `.dirty` off
    // an absent buffer would be a TypeError where a plain "nothing to guard" is
    // the truth.
    const selectionBuffer = state.buffers[UNBACKED_DOCUMENT_BUFFER_KEY];
    if (selectionBuffer && selectionBuffer.dirty) {
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
      const guarded = state.buffers[UNBACKED_DOCUMENT_BUFFER_KEY];
      if (guarded && guarded.dirty) {
        // The Document did not land, so there is nothing to switch away from
        // safely: the guard stays open, states WHY in its own assertive region,
        // and puts focus back on the choice that can still resolve it.
        const reason = outcomeReasonFor(UNBACKED_DOCUMENT_BUFFER_KEY, outcome);
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
      focusBufferEditor(UNBACKED_DOCUMENT_BUFFER_KEY);
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
      focusBufferEditor(UNBACKED_DOCUMENT_BUFFER_KEY);
      return { status: "cancelled", reason: null };
    }
    if (choice === "discard") {
      const target = guardTargetPath;
      guardTargetPath = null;
      hideGuard();
      await discard(UNBACKED_DOCUMENT_BUFFER_KEY);
      const result = await switchDocument(target);
      focusBufferEditor(UNBACKED_DOCUMENT_BUFFER_KEY);
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

  function viewState(key) {
    const textarea = textareas[key];
    return {
      selectionStart: textarea.selectionStart,
      selectionEnd: textarea.selectionEnd,
      scrollTop: textarea.scrollTop,
      focused: globalThis.document.activeElement === textarea,
    };
  }

  function elements() {
    return {
      textarea: (key) => textareas[key] || null,
      preview: (key) => previews[key] || null,
      // A VIEW tab, keyed by view -- the buffer tablist it replaced is gone, so
      // there is nothing to look up by buffer key here any more.
      viewTab: (key) => viewTabButtons[key] || null,
      // ONE of each, so neither takes an argument: asking for "the Save of the
      // outline" is a question the panel no longer has an answer to.
      save: () => saveBtn,
      cancel: () => cancelBtn,
      // Amendment 1: the slot's third occupant, and the visible note carrying
      // its reason while it is inert.
      unload: () => unloadBtn,
      unloadNote: () => unloadNote,
      guard: () => guardHost,
      // additive, beyond the fixed minimum set: a per-buffer status region
      // and the document picker, both needed to test the fix round's
      // visible-refusal and scope-guard behaviour.
      status: (key) => statusEls[key] || null,
      // the transient visible line annotation round 2 introduced, so a test can
      // measure that an EVENT was shown without waiting on its own timer
      eventNote: () => eventNote,
    };
  }

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    // Every timer this mount ever scheduled -- read off the REGISTRY rather than
    // off the state, because a buffer that was unloaded still owns its entry here
    // and a timer left running on a torn-down mount is a timer nobody can stop.
    for (const key of Object.keys(previewTimers)) {
      if (previewTimers[key]) {
        clearTimeout(previewTimers[key].timer);
        previewTimers[key] = null;
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
        // The reserved SELECTION slot's path, when the restored session has one.
        // A Phase A record always did (`{outline, document}`, which is why it
        // restores unchanged); a Phase B record whose reserved slot was unloaded
        // does not, and reading `.path` off an absent buffer would turn a restore
        // into the stated load FAILURE for no reason.
        const restoredSelection = restored.buffers[UNBACKED_DOCUMENT_BUFFER_KEY];
        activeDocumentPath = restoredSelection ? restoredSelection.path : null;
        // EVERY RESTORED KEY GETS ITS DOM. The mount built the reserved pair; a
        // restored session can carry any number of loaded documents beside them,
        // and a buffer with no status region is a buffer no Save could report a
        // verdict about.
        for (const bufferKey of bufferKeysInOrder(state)) ensureBufferDom(bufferKey);
        // …and a region the mount built for a key the RESTORED state does not
        // hold is blanked and hidden, exactly as an unload leaves one. Left
        // alone it would stand there stating the loading line forever, which is
        // a sentence about a buffer that does not exist.
        for (const bufferKey of Object.keys(statusEls)) {
          if (holdsBufferKey(bufferKey)) continue;
          bufferBoxes.editor[bufferKey].hidden = true;
          bufferBoxes.preview[bufferKey].hidden = true;
          textareas[bufferKey].disabled = true;
          statusEls[bufferKey].textContent = "";
          statusEls[bufferKey].hidden = true;
        }
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
      refreshBufferLabels();
      applyVisibility();
      for (const key of bufferKeysInOrder(state)) {
        syncBufferDom(key);
        renderPreviewNow(key);
      }
      // The loaded set and the selection are both settled now, so the rail's
      // selector and the wheel's tile marking can render from a real answer
      // instead of an empty one.
      notifyLoadedSetChanged();
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
      // Every region this mount BUILT carries the failure: `state` is null, so
      // there is no buffer set to enumerate, and the registry is the honest
      // answer to "which regions exist to be told".
      for (const key of Object.keys(statusEls)) {
        statusEls[key].textContent = bufferLabel(key) + ": " + loadFailureReason;
        statusEls[key].classList.add("doxbench-status-error");
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
  async function applyProposal(key, proposal) {
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
    const buffer = state.buffers[key];
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
    return edit(key, flavored);
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
    // ---- PHASE B: the LOADED SET's surface -------------------------------
    //
    // Every member here is a READ of, or a stated ACT on, the one buffer set the
    // state module owns. None of them is a second state authority: the selector
    // renders `loadedBuffers()` and calls `setActiveBuffer`, the tile calls
    // `loadDocumentForEditing` / `unloadDocument` / `saveDocument`, and
    // `state.active_buffer` remains the single answer to "what is selected".
    //
    // `loadDocumentForEditing(path, {maxLoadedDocuments})` resolves to
    //   `{ok: true, key, already_loaded, bound?, measured?, error: null}` or
    //   `{ok: false, key: null, error, refusal?, bound?, measured?}`.
    // `unloadDocument(key, {discardUnsavedEdits})` resolves to
    //   `{ok, error, refusal?}` -- refusing a dirty buffer without the discard.
    // `saveDocument(key)` resolves to the SAME outcome shape `save()` reports,
    //   because it IS `save()`, scoped (design D4).
    // `loadedBuffers()` is a frozen array of frozen
    //   `{key, path, label, owned, dirty, active}` rows, documents only, in the
    //   state module's declared order.
    // `bufferKeys()` is that order including the reserved outline key first.
    loadDocumentForEditing,
    unloadDocument,
    saveDocument,
    loadedBuffers,
    bufferKeys,
  };
}
