// doxbench-chat.js — T053/T054 (US2): the doxBench chat rail view. Working
// subject, approved-model selector, bounded transcript, composer, and the
// dispatch discipline: complete CURRENT buffers through the INJECTED
// same-origin transport, composer preserved on every refusal (FR-016).
//
// Discipline mirrors doxbench-editor.js: this module imports ONLY the pure
// chat model. It opens no route, holds no URL, and computes no digest — the
// transports arrive injected from app.js's seam bundle, and the CURRENT
// editor buffers arrive through an injected provider read at SUBMIT time
// (never cached), which is what T054's "complete current buffers" means.
// Rendering is textContent-only; no markup-injection property is touched.
//
// The seam surface (`buildTurnRequest`, `createTurnDispatcher`) is exported
// pure and DOM-free so the Node suite pins the behavior without a browser;
// `mountDoxBenchChatRail` is the thin assembly over it.

import {
  createChatState, adoptCatalog, selectModel, editSubject, editComposer,
  beginTurn, settleTurnSuccess, settleTurnFailure, abortTurn,
  transcriptWindow, transcriptWireWindow, rekeyChatState, proposalsOf,
  refreshProposalCurrency, rejectProposal, markProposalApplied,
  markProposalAppliedAfterSwap, clearLocalFailure,
  recordLocalFailure, recordCatalogFailure, chatSnapshot, restoreChatState,
  canSend, MAX_MESSAGE_BYTES, MAX_WORKING_SUBJECT_BYTES,
} from "./doxbench-chat-model.js";

const CHAT_TURN_KIND = "workbench-chat-turn";
const CHAT_SUCCESS_KIND = "workbench-chat-turn-success";
const CHAT_FAILURE_KIND = "workbench-chat-turn-failure";

// FIXED local failure marker for a transport that never produced a released
// failure envelope (network refusal, pre-identity refusal shape, throw).
// Never composed from request, response, or error text (FR-020/FR-022).
const TRANSPORT_REFUSED = Object.freeze({
  error: "transport_refused",
  message: "the chat transport refused this turn",
});

// PR-stabilization R2: the unsettled-buffer pre-flight refusal is VISIBLE —
// a fixed local failure the note renders; never a silent dead button.
const BUFFERS_UNSETTLED = Object.freeze({
  error: "buffers_unsettled",
  message: "the buffers are still settling; try Send again in a moment",
});

// THE V1-WIRE BINDING LIMIT, stated (adversarial review of PR #207, F1).
//
// `buildTurnRequest` sends exactly the two buffers the RELEASED v1 chat-turn
// envelope has room for: the reserved `outline` key and the reserved `document`
// key. So a turn can only ever be about one of those two, and
// `active_document_path` can only ever name the reserved slot's own path — which
// is the invariant `staging-workbench.js` restores.
//
// Phase B lets a human SELECT a path-keyed loaded document, and the canvas and
// the selector honour it immediately. The CHAT cannot, until §13's co-resident
// widened family releases an envelope that carries the outline plus N documents
// and a declared bound-buffer key. Before this note existed, selecting such a
// buffer made the route refuse with its fixed redacted `turn_scope_refused`
// code — a governance refusal shown for a limitation of our own wire, which is
// the one thing a refusal must never be.
//
// So it is a STATED PRE-FLIGHT POSTURE instead: Send is unreachable, the reason
// is on the control and programmatically associated, and no provider or route is
// consulted at all. The house idiom (design §3.4): a capability that is absent
// says so; it does not fail on activation.
const CHAT_BINDING_UNRELEASED = Object.freeze({
  error: "chat_binding_unreleased",
  message: "this chat cannot be bound to a document loaded beside the tile's own "
    + "yet: the released turn envelope carries the outline and one document, so "
    + "select the outline or the tile's own document to send. Editing, Save and "
    + "the loaded set are unaffected.",
});

// T100 P1-2 (real-corpus finding): a pre-identity console-token refusal
// (legacy {ok,error,message} shape) must surface as a RECOVERABLE fixed
// message, never a wedged rail. The stale-token case names its remedy.
const CONSOLE_TOKEN_STALE = Object.freeze({
  error: "console_token_stale",
  message: "this page's console token is stale — reload the page to continue",
});

// Defense-in-depth for the same finding: whatever throws anywhere in the
// mounted send path, the rail settles to a visible failed-idle state.
const SEND_PATH_FAILED = Object.freeze({
  error: "send_path_failed",
  message: "sending failed unexpectedly; the message is preserved — try again",
});

// T104 F2: the two shapes the RELEASED contract-v1.27 request envelope refuses
// outright — `model_id: ""` (minLength 1) and `active_document_path: null`
// (a `confined_path` STRING; the BUFFER path is nullable, the active document
// path is not). Emitting either turned an answerable local condition into an
// opaque server refusal — "you did not pick a model" arrived as "the turn
// request is malformed" — so both are refused HERE, before the transport, in
// the operator's own vocabulary. The composer is preserved exactly as every
// other pre-flight refusal preserves it (FR-016).
const NO_MODEL_SELECTED = Object.freeze({
  error: "no_model_selected",
  message: "choose an approved model above before sending",
});

const NO_ACTIVE_DOCUMENT = Object.freeze({
  error: "no_active_document",
  message: "a turn grounds on a document you may edit, and none is active; "
    + "pick one in the Document tab first",
});

// T104 F5-5 + W-10: the FIXED refusals for an Apply the buffer seam would
// not take. One sentence used to answer for every refusal — but "ask again
// in a new turn" is only true for STALENESS; a click while an identity was
// still settling (or during a Save or a load) needed a moment, not a new
// turn, and a persistently-throwing seam looped the false advice forever.
// The seam now carries a fixed CODE and the mapping below is a WHITELIST:
// the seam's error text — like anything a throwing seam carries — is
// dropped unread, same discipline as TRANSPORT_REFUSED. Each sentence names
// its own recovery.
const PROPOSAL_APPLY_REFUSED = Object.freeze({
  error: "proposal_apply_refused",
  message: "this proposal no longer matches the buffer — ask again in a "
    + "new turn",
});

const PROPOSAL_APPLY_UNSETTLED = Object.freeze({
  error: "proposal_apply_unsettled",
  message: "the buffers are still settling — try Apply again in a moment",
});

const PROPOSAL_APPLY_FAILED = Object.freeze({
  error: "proposal_apply_failed",
  message: "the apply failed — the proposal stays reviewable; try again",
});

// the CODE whitelist: anything the seam does not spell exactly (a throw, a
// null, an unknown or absent code) is the generic failure, never staleness
function proposalApplyFailureFor(result) {
  if (result && result.code === "stale") return PROPOSAL_APPLY_REFUSED;
  if (result && result.code === "unsettled") return PROPOSAL_APPLY_UNSETTLED;
  return PROPOSAL_APPLY_FAILED;
}

// T104 F5-9 residual: the rail's OWN posture when it is offered (the
// transports exist, so it is mounted) but no model is selectable. The same
// sentence the shell's posture line derives (presentationPosture's
// editor-only note), restated in the rail so the two adjacent surfaces
// agree — the old rail rendered a fully-live-looking selector and composer
// right beside "chat is unavailable".
const CHAT_UNAVAILABLE_NOTE =
  "chat is unavailable — no approved model is configured; both editors "
  + "remain fully usable.";

// T104 F10-1: the rail's OTHER two unavailability postures, each its own
// fixed sentence. The configured-none note above answered for EVERY catalog
// failure — but a 403 stale console token is recoverable (the SAME reload
// vocabulary R-3 gave the chat-turn path names the remedy), and a 500 broken
// catalog is "the answer could not be read", not "nothing is configured".
// One selector, so the note and the model's fixed failure vocabulary can
// never drift.
const CATALOG_UNREADABLE_NOTE =
  "chat is unavailable — the model catalog could not be read; both editors "
  + "remain fully usable.";

// P3-8 (wave re-review P3 tail): the mount-to-catalog WINDOW. Between mount
// and the one-shot catalog ready settling, `models` is still null and no
// failure has been recorded — the page does not yet KNOW whether a model is
// configured, so the configured-none sentence was a claim it could not make
// (wrong for the whole fetch window on every capable plane). A fixed loading
// sentence holds the spot; the settled three-way posture below takes over
// the moment the ready adopts or records a failure.
const CHAT_CATALOG_LOADING_NOTE = "chat is checking the model catalog…";

function unavailabilityNote(stateValue) {
  if (stateValue.catalogFailure === "console_required") {
    return CONSOLE_TOKEN_STALE.message;
  }
  if (stateValue.catalogFailure) return CATALOG_UNREADABLE_NOTE;
  // models === null is "no catalog has answered yet" (createChatState's
  // starting shape; adoptCatalog and recordCatalogFailure are the only exits)
  if (stateValue.models === null) return CHAT_CATALOG_LOADING_NOTE;
  return CHAT_UNAVAILABLE_NOTE;
}

// T104 F10-2/4: the over-bound paste, refused VISIBLY. The pure model
// refuses by returning the IDENTICAL state (refused, never truncated) and
// render()'s unconditional value reassignment reverts the DOM — correct, but
// silent: the pasted text vanished with nothing said. Each fixed note names
// its BOUND and never the text (the editor's own visible "refused" line is
// the idiom); recordLocalFailure puts it on the same aria-live channel every
// other refusal renders through.
const MESSAGE_OVER_BOUND = Object.freeze({
  error: "message_over_bound",
  message: "this message exceeds the " + MAX_MESSAGE_BYTES
    + "-byte message bound — refused, never truncated; shorten it and try "
    + "again",
});

const SUBJECT_OVER_BOUND = Object.freeze({
  error: "subject_over_bound",
  message: "this working subject exceeds the " + MAX_WORKING_SUBJECT_BYTES
    + "-byte subject bound — refused, never truncated; shorten it",
});

// The ACTIONABLE half of the same refusal (T104 F2: "the refusal names no
// document the operator could pick instead"). When the tile HAS usable
// documents, the note names one; when it has none AND there is no outline to
// ground on either, it says so and names the only way forward, rather than
// leaving the operator to discover from an opaque `turn_scope_refused` that
// this tile can never chat.
function noActiveDocumentFailure(candidates) {
  const usable = (candidates || []).filter(
    (path) => typeof path === "string" && path);
  if (!usable.length) {
    return Object.freeze({
      error: "no_active_document",
      message: "this tile has no document you may edit, so a turn has nothing "
        + "to ground on — create one first, and it becomes available here",
    });
  }
  return Object.freeze({
    error: "no_active_document",
    message: NO_ACTIVE_DOCUMENT.message + " — for example "
      + usable[0] + (usable.length > 1
        ? " (" + (usable.length - 1) + " more available)" : ""),
  });
}

// G-1 (PR #63 re-verification, 2026-08-02): THE OUTLINE-ONLY TURN.
//
// Measured on the real corpus, 16 of 21 staged topics have exactly ONE
// editable path — the topic's own primary fragment, which this canvas loads
// as the OUTLINE. T104 F2 correctly stopped advertising the outline as an
// active DOCUMENT candidate (one file cannot be two independent buffers), so
// those tiles have no document to name. That is not "nothing to ground on":
// the outline IS the tile's material. Such a turn declares
// `active_document_path: null` — the shape the contract-v1.28 amendment makes
// legal, mirroring `buffer_state.path`, which is already nullable and is what
// the document buffer carries here.
//
// A backed OUTLINE buffer is the whole precondition: the scope authority
// publishes `outline_path` only when it is in-scope AND editable (T104 F2), so
// a non-null outline buffer path is exactly the case the server's own FR-015
// guard accepts with a null document.
function outlineOnlyTurnIsAvailable(editorStateValue) {
  const outline = editorStateValue && editorStateValue.buffers
    && editorStateValue.buffers.outline;
  const outlinePath = outline && outline.path;
  return typeof outlinePath === "string" && outlinePath.length > 0;
}

function hexOf(identity) {
  return typeof identity === "string" ? identity : String(identity && identity.hex);
}

function wireBuffer(bufferValue, kindValue, repositoryValue) {
  return {
    kind: kindValue,
    path: bufferValue.path === null || bufferValue.path === undefined
      ? null : String(bufferValue.path),
    repository: String(repositoryValue),
    base_ref: String(bufferValue.base_ref),
    base_revision: String(bufferValue.base_revision),
    base_hash: hexOf(bufferValue.base_hash),
    content_hash: hexOf(bufferValue.current_hash),
    content: String(bufferValue.content),
    dirty: bufferValue.dirty === true,
  };
}

export function buildTurnRequest(options) {
  const { state, scopeKey, clientTurnId, activeDocumentPath, editorState } = options;
  const buffers = editorState.buffers;
  return {
    schema_version: 1,
    kind: CHAT_TURN_KIND,
    client_turn_id: String(clientTurnId),
    scope: {
      repository: String(scopeKey.repository),
      ref: String(scopeKey.ref),
      tile_kind: String(scopeKey.tile_kind),
      tile_id: String(scopeKey.tile_id),
    },
    // T104 F2 + G-1: `model_id` must be minLength 1, enforced by
    // `createTurnDispatcher.submit` before this builder is reached (an absent
    // model is an answerable local refusal, not a malformed request).
    // `active_document_path` is NULLABLE per the contract-v1.28 amendment,
    // mirroring `buffer_state.path`: null is the outline-only turn, which the
    // dispatcher permits only when the outline buffer is backed and the tile
    // publishes no usable document candidate.
    active_document_path: activeDocumentPath === null
      || activeDocumentPath === undefined ? null : String(activeDocumentPath),
    working_subject: state.workingSubject,
    message: state.composer,
    model_id: state.selectedModelId === null ? "" : state.selectedModelId,
    last_assistant_turn_id: null,
    // T104 F5-2: the WIRE window, not the display transcript. The display
    // may legally hold a newest pair larger than the request-side transcript
    // bound (the server's 64,000 bytes); the request carries what fits,
    // oldest evicted first — possibly nothing — while the display keeps it.
    transcript: transcriptWireWindow(state).map(
      (turn) => ({ role: turn.role, content: turn.content })),
    buffers: [
      wireBuffer(buffers.outline, "outline", scopeKey.repository),
      wireBuffer(buffers.document, "document", scopeKey.repository),
    ],
  };
}

// PR #63 review + T101 ux CHK015: the SEND-MOMENT disclosure. Pure: the
// selected entry's server-declared data_handling text, or null when no
// model is selected (the view then shows nothing beside Send).
export function sendDisclosure(stateValue) {
  const models = stateValue.models || [];
  const entry = models.find(
    (m) => m.model_id === stateValue.selectedModelId
           && m.available === true);
  const handling = entry && entry.data_handling;
  return handling ? String(handling) : null;
}

function bufferSettled(bufferValue) {
  return Boolean(bufferValue) && bufferValue.hash_pending !== true
    && Boolean(bufferValue.current_hash);
}

export function createTurnDispatcher(options) {
  const { transports, turnIdFactory } = options;
  const nextId = turnIdFactory
    || ((n) => "turn-" + Date.now().toString(36) + "-" + n);
  let pending = false;
  let accepted = 0;

  async function submit(stateValue, contextValue) {
    // ONE turn in flight per dispatcher (FR-018), mirrored by the model's
    // own identical-object refusal — both must agree before dispatch.
    const begun = beginTurn(stateValue);
    if (pending || begun === stateValue) {
      return { refused: true, state: stateValue };
    }
    pending = true;
    accepted += 1;
    const clientTurnId = String(nextId(accepted));
    try {
      // CURRENT buffers, read at submit time — never a cached copy (T054).
      const editorState = typeof contextValue.editorState === "function"
        ? contextValue.editorState() : contextValue.editorState;
      // PR #63 review (Copilot): an UNSETTLED buffer identity cannot be
      // declared on the wire — refuse pre-flight, composer preserved, the
      // transport never consulted.
      if (!editorState || !bufferSettled(editorState.buffers.outline)
          || !bufferSettled(editorState.buffers.document)) {
        // `begun` is in_flight, so the fixed-failure settlement applies:
        // idle again, composer preserved, the note visible (R2).
        return { refused: true,
                 state: settleTurnFailure(begun, BUFFERS_UNSETTLED) };
      }
      // F1 (PR #207 review): the SELECTED buffer is one the released envelope
      // cannot carry a turn about. Refused HERE — pre-flight, composer
      // preserved, the transport never consulted — with our own stated reason,
      // rather than shipped so the route can answer with a redacted governance
      // code for a limitation of our own wire.
      const binding = chatBindingPosture(editorState);
      if (!binding.ok) {
        return { refused: true,
                 state: settleTurnFailure(begun, CHAT_BINDING_UNRELEASED) };
      }
      // T104 F2: the two RELEASED-envelope violations, refused here rather
      // than shipped. Same settlement, same preserved composer.
      if (!stateValue.selectedModelId) {
        return { refused: true,
                 state: settleTurnFailure(begun, NO_MODEL_SELECTED) };
      }
      const activePath = contextValue.activeDocumentPath;
      if (activePath === null || activePath === undefined || activePath === "") {
        const candidates = typeof contextValue.documentCandidates === "function"
          ? contextValue.documentCandidates() : contextValue.documentCandidates;
        const usable = (candidates || []).filter(
          (path) => typeof path === "string" && path);
        // The tile HAS documents this turn could name and none is active: the
        // operator has a choice to make, so the F2 refusal stands and names
        // one (T104 F2, unchanged).
        //
        // With NO candidates the choice does not exist. If the outline is
        // backed, the turn grounds on it alone (G-1); only a tile with
        // neither is genuinely without context, and keeps the F2 refusal.
        if (usable.length || !outlineOnlyTurnIsAvailable(editorState)) {
          return { refused: true,
                   state: settleTurnFailure(
                     begun, noActiveDocumentFailure(usable)) };
        }
      }
      if (typeof contextValue.onBegin === "function") {
        contextValue.onBegin(begun);
      }
      const request = buildTurnRequest({
        state: stateValue, scopeKey: contextValue.scopeKey, clientTurnId,
        activeDocumentPath: contextValue.activeDocumentPath, editorState });
      let response = null;
      try {
        response = await transports.chatTurn(request);
      } catch (unused) {
        // The transport's own error text is DROPPED unread (FR-020/FR-022):
        // the fixed marker below is the whole failure surface.
        response = null;
      }
      // Settle against the LIVE state when the caller can supply it (the
      // mounted view adopts `begun` and keeps editing) — follow-up edits
      // made during a slow turn are then preserved by the model's own
      // settlement rule. Callers without a live getter settle `begun`.
      const liveState = typeof contextValue.liveState === "function"
        ? (contextValue.liveState() || begun) : begun;
      // PR-stabilization R1: when the caller supplied a live getter and the
      // live state has RELEASED the flight (abort, rekey), the turn is
      // ABANDONED — settling the stale snapshot would resurrect a dead turn
      // and clobber everything done since. Callers without a live getter
      // keep the settle-begun behavior.
      if (typeof contextValue.liveState === "function"
          && liveState.phase !== "in_flight") {
        return { abandoned: true, clientTurnId, state: liveState };
      }
      const settleBase = liveState.phase === "in_flight" ? liveState : begun;
      if (response && response.ok === true && response.payload
          && response.payload.kind === CHAT_SUCCESS_KIND) {
        return { ok: true, clientTurnId,
                 state: settleTurnSuccess(settleBase, response.payload) };
      }
      let failure = TRANSPORT_REFUSED;
      if (response && response.payload
          && response.payload.kind === CHAT_FAILURE_KIND) {
        failure = response.payload;
      } else if (response && response.payload
                 && (response.payload.error === "agent_invocation"
                     || response.payload.error === "console_required")) {
        // The pre-identity console gate refused. R-3 (2026-08-02): the
        // doxBench ROUTES spell this `console_required` while the gate-action
        // route spells it `agent_invocation` — the earlier fix caught only the
        // latter, which is why the operator still saw the generic refusal on a
        // stale token. Both spellings now name the reload remedy.
        failure = CONSOLE_TOKEN_STALE;
      }
      return { ok: false, clientTurnId,
               state: settleTurnFailure(settleBase, failure) };
    } finally {
      pending = false;
    }
  }

  return { submit };
}

// ---------------------------------------------------------------------------
// T063/T065 (US3): proposal review cards. The card model is PURE and
// render-ready; the action surface takes the INJECTED `applyProposal` seam
// (the buffer swap itself lives behind it — T064's revalidation runs at the
// swap), and a stale record never reaches that seam at all: its Apply is
// disabled and its note names the ONLY recovery, a new turn. No merge and
// no force path exist on this surface either.
// ---------------------------------------------------------------------------

// T100 P1-C(3): every terminal note NAMES its target buffer.
const _CARD_NOTES = Object.freeze({
  current: (t) => "replaces the " + t + " working copy after your review",
  stale: (t) => "the " + t + " buffer changed since this proposal was "
    + "written; ask again in a new turn",
  rejected: (t) => "rejected; the " + t
    + " proposal will not be offered again this turn",
  applied: (t) => "applied to the " + t
    + " working copy; Save remains the only exit",
});

// WHY SEND IS IN THE STATE IT IS IN — three cases, named rather than nested,
// so the reason a human cannot send is always readable on the control itself.
// Brett's 2026-08-18 annotation round 2: "make this text the hover text for the
// send button if no model selected." When the reason Send is unreachable is
// that no model is available or chosen, the button's tooltip IS the sentence
// that used to stand in the posture note — the same string, from the same one
// selector (`unavailabilityNote`), so the two can never drift. The generic
// "…and type a message" line is kept for the case where a model IS selected and
// the composer is simply empty, which is a different reason.
function sendTitle(inFlight, disabled, unavailableReason) {
  if (inFlight) return "a turn is in flight — one turn at a time per conversation";
  if (disabled && unavailableReason) return unavailableReason;
  if (disabled) return "type a message to send";
  return "send this turn";
}


export function proposalCardModel(stateValue) {
  const records = proposalsOf(stateValue);
  const cards = [];
  for (const target of ["outline", "document"]) {
    const record = records[target];
    if (!record) continue;
    cards.push(Object.freeze({
      target,
      status: record.status,
      summary: record.summary,
      applyEnabled: record.status === "current",
      rejectEnabled: record.status === "current" || record.status === "stale",
      ariaLabel: target + " proposal: " + record.summary,
      note: _CARD_NOTES[record.status](target),
    }));
  }
  return cards;
}

export function createProposalActions(options) {
  const { applyProposal, liveState } = options;
  // W-3 (wave re-review): everything adopted DURING an action's await —
  // follow-up typing, a turn that settled, a currency re-score — lives in
  // the CURRENT state, and deriving the outcome from the click-time
  // snapshot clobbered all of it (executed: an Apply spanning a turn
  // settlement re-adopted the in-flight snapshot and wedged the rail at
  // "Sending…" with nothing in the air). This is the send path's R1
  // defense, extended to the card actions that were rewritten beside it.
  // Callers without a live getter keep the settle-snapshot behavior.
  const settleBase = (stateValue) => (typeof liveState === "function"
    ? (liveState() || stateValue) : stateValue);
  return {
    async apply(stateValue, targetValue) {
      const record = proposalsOf(stateValue)[targetValue];
      if (!record || record.status !== "current") {
        return stateValue;  // stale/terminal/absent: the seam is never consulted
      }
      let result = null;
      try {
        result = await applyProposal(targetValue, record);
      } catch (unused) {
        result = null;  // the buffer side's own detail is dropped unread
      }
      const live = settleBase(stateValue);
      if (!result || result.ok !== true) {
        // T104 F5-5: the swap refused, and the refusal is VISIBLE. The old
        // return of the identical state meant a clicked Apply produced zero
        // change on the surface — no note, no announcement — leaving the
        // operator to wonder whether anything ran. The record itself stays
        // reviewable (no status transition: a stale re-score belongs to
        // refreshProposalCurrency, which the next settled identity runs);
        // only the fixed local failure lands, on the same channel every
        // other refusal renders through — chosen by the seam's CODE (W-10),
        // so a settling buffer is advised a moment and only genuine
        // staleness is advised a new turn.
        return recordLocalFailure(live, proposalApplyFailureFor(result));
      }
      const liveRecord = proposalsOf(live)[targetValue];
      if (!liveRecord || liveRecord.base_hash !== record.base_hash
          || liveRecord.content !== record.content) {
        // The set moved on during the swap — a settled turn replaced the
        // proposals: the live truth wins, and a card that no longer exists
        // (or no longer says what was swapped) is never marked applied.
        return live;
      }
      // Field-identical record: any `stale` here is the apply's own doing
      // (the swap moved the buffer identity before this promise resolved),
      // so the after-swap transition keeps "applied" truthful. The landed
      // apply also CLEARS the local failure channel (W-11): a refusal note
      // left standing beside the applied announcement asserted two opposite
      // facts about the same proposal.
      return clearLocalFailure(markProposalAppliedAfterSwap(live, targetValue));
    },
    async reject(stateValue, targetValue) {
      return rejectProposal(settleBase(stateValue), targetValue);
    },
  };
}

// ---------------------------------------------------------------------------
// THE LOADED-DOCUMENT SELECTOR (add-doxbench-editing-phase-b, Q1 ruled:
// "make this a dropdown box that lists the files that have been loaded by
// clicking the edit button on the wheel. the selected one is the file we are
// working on. if not fit in one line, then use hover to expand to see full
// filename.")
//
// Phase A's rail header was a LABEL -- "Working on — <name> · Chatting about —
// …". Phase B makes it a SELECTOR, and the model behind it is pure and exported
// so the whole listing rule is pinnable without a DOM.
//
// D6: THE DROPDOWN IS THE OVERFLOW POLICY. A native scrolling select dissolves
// the many-open-edits problem by construction, so there is no folding, no
// least-recently-used chip row, and -- deliberately -- NO EVICTION anywhere:
// every loaded buffer may hold unsaved work, and a policy that evicted to make
// room would be a policy that discards human text. Reaching the loaded-set bound
// REFUSES the load with the measured bound stated, which is the state module's
// job, not this one's.
//
// D7: this is a SELECTION SURFACE, not a second state authority.
// `state.active_buffer` -- a buffer KEY -- remains the one answer to "what is
// selected". The selector renders it and sets it through the injected seam;
// loading sets it; the context region's outline tab sets it. Three routes, one
// value.
// ---------------------------------------------------------------------------

// Which buffer keys the RELEASED v1 envelope can carry a turn about. Both are
// reserved keys, and that is the whole of the closed set until §13.
const V1_BINDABLE_BUFFER_KEYS = Object.freeze(["outline", "document"]);

// The chat's binding posture for one editor state. PURE and exported, so the
// limitation is pinned without a DOM and read from exactly one place by the
// render, the dispatcher and the tests.
export function chatBindingPosture(editorStateValue) {
  const state = editorStateValue || null;
  const selected = state && typeof state.active_buffer === "string"
    ? state.active_buffer : null;
  if (selected === null) {
    // No state yet (the rail renders before the canvas's initial load settles).
    // Not a refusal: there is nothing to refuse about, and `canSend` already
    // holds Send closed until a model and a message exist.
    return Object.freeze({ ok: true, reason: null, selected: null });
  }
  if (V1_BINDABLE_BUFFER_KEYS.includes(selected)) {
    return Object.freeze({ ok: true, reason: null, selected });
  }
  return Object.freeze({
    ok: false, reason: CHAT_BINDING_UNRELEASED.message, selected });
}

export const LOADED_SELECTOR_EMPTY_NOTE =
  "no document is loaded — use a docs tile's load verb to work on one; the "
  + "outline is workable on its own";

const OUTLINE_BUFFER_KEY = "outline";
// The reserved unbacked/create key. Under the RELEASED v1 envelope this slot is
// not merely reserved -- it RIDES EVERY TURN, exactly as the outline does
// (`buildTurnRequest` sends `buffers.outline` and `buffers.document` and nothing
// else), which is why it can no more be unloaded than the outline can.
const RESERVED_DOCUMENT_BUFFER_KEY = "document";
const OUTLINE_ENTRY_LABEL = "Outline";
const UNBACKED_ENTRY_LABEL = "(not yet created)";

function basenameOf(path) {
  return String(path).split("/").at(-1) || String(path);
}

// The DISTINGUISHING label rule. A basename is what a human reads, so it is the
// default; but "a selector that cannot tell two files apart is worse than one
// that shows a longer name", so when two loaded documents share a basename each
// colliding entry grows leftwards one path segment at a time until every label
// in the collision is distinct. The full path always rides the entry as its
// hover/assistive name, so nothing is ever ambiguous to a reader who asks.
export function distinguishingLabels(paths) {
  const values = Array.from(paths, (path) => String(path));
  const labels = new Map();
  const bySuffixDepth = new Map();
  for (const path of values) {
    const base = basenameOf(path);
    if (!bySuffixDepth.has(base)) bySuffixDepth.set(base, []);
    bySuffixDepth.get(base).push(path);
  }
  for (const [, colliding] of bySuffixDepth) {
    if (colliding.length === 1) {
      labels.set(colliding[0], basenameOf(colliding[0]));
      continue;
    }
    let depth = 1;
    let assigned = null;
    // Grow the suffix until every label in THIS collision is distinct, bounded
    // by the longest path so the loop cannot run away on identical paths (which
    // the keyed buffer set makes impossible in the first place).
    const longest = Math.max(...colliding.map((p) => p.split("/").length));
    while (depth <= longest) {
      const candidate = new Map();
      for (const path of colliding) {
        candidate.set(path, path.split("/").slice(-depth).join("/"));
      }
      if (new Set(candidate.values()).size === colliding.length) {
        assigned = candidate;
        break;
      }
      depth += 1;
    }
    for (const path of colliding) {
      labels.set(path, assigned ? assigned.get(path) : path);
    }
  }
  return labels;
}

// The selector's whole listing, derived from the LIVE editor state and nothing
// else. The reserved `outline` entry leads, because the outline is a buffer the
// selector must be able to name: the ratified rule is that the selector's
// selected entry IS the selected buffer, and every route must leave the
// selector, the canvas and the chat agreeing -- a selector that could not show
// an outline selection would disagree with the canvas the moment the outline tab
// was focused.
export function loadedSelectorModel(editorStateValue) {
  const state = editorStateValue || null;
  const buffers = (state && state.buffers) || {};
  const keys = Object.keys(buffers);
  // F6 (PR #207 review): the reserved `document` slot is present in EVERY state
  // the canvas produces — `initialLoad` builds it — and while its `path` is null
  // it is the create flow's not-yet-created artifact, not a loaded document. A
  // buffer nobody loaded must not be listed as loaded, and counting it made the
  // ratified empty state unreachable: `documentCount` was never zero, so the
  // honest "no document is loaded" sentence could never render. Same rule the
  // canvas's own `loadedBuffers()` applies, spelled once per module because both
  // stay import-free.
  const documentKeys = keys.filter((key) => {
    if (key === OUTLINE_BUFFER_KEY) return false;
    const buffer = buffers[key];
    return Boolean(buffer && buffer.path !== null && buffer.path !== undefined);
  });
  // The DECLARED order, spelled exactly as doxbench-state.js declares it:
  // ascending lexicographic by buffer key (UTF-16 code unit). A listing whose
  // order depended on insertion would reorder itself under the human's cursor.
  documentKeys.sort((left, right) => (left < right ? -1 : left > right ? 1 : 0));
  const labels = distinguishingLabels(
    documentKeys.map((key) => {
      const buffer = buffers[key];
      return buffer && buffer.path ? buffer.path : key;
    }));
  const selected = state && typeof state.active_buffer === "string"
    ? state.active_buffer : OUTLINE_BUFFER_KEY;
  const entries = [];
  if (Object.prototype.hasOwnProperty.call(buffers, OUTLINE_BUFFER_KEY)) {
    const outline = buffers[OUTLINE_BUFFER_KEY];
    entries.push(Object.freeze({
      key: OUTLINE_BUFFER_KEY,
      reserved: true,
      label: OUTLINE_ENTRY_LABEL,
      fullName: outline && outline.path ? String(outline.path) : UNBACKED_ENTRY_LABEL,
      kind: "outline",
      owned: outline ? outline.owned === true : false,
      dirty: outline ? outline.dirty === true : false,
      selected: selected === OUTLINE_BUFFER_KEY,
    }));
  }
  for (const key of documentKeys) {
    const buffer = buffers[key];
    const path = buffer && buffer.path ? String(buffer.path) : null;
    entries.push(Object.freeze({
      key,
      // N3 (PR #207 re-verification): the reserved key is a RESERVED entry, not an
      // ordinary loaded document, even when it carries a real path. Listing it is
      // right -- it is selectable and the chat binds to it -- but treating it as
      // ordinary made Unload reachable for it, and emptying it left
      // `buildTurnRequest` reading `buffers.document.path` on an absent buffer.
      // That threw, was caught as the generic unsettled-buffer failure, and the
      // rail then said "still settling; try Send again in a moment" forever.
      reserved: key === RESERVED_DOCUMENT_BUFFER_KEY,
      label: path === null ? UNBACKED_ENTRY_LABEL : labels.get(path) || basenameOf(path),
      fullName: path === null ? UNBACKED_ENTRY_LABEL : path,
      kind: "document",
      owned: buffer ? buffer.owned === true : false,
      dirty: buffer ? buffer.dirty === true : false,
      selected: selected === key,
    }));
  }
  return Object.freeze({
    entries: Object.freeze(entries),
    selected,
    documentCount: documentKeys.length,
    // The HONEST empty state: the control is rendered and says so, rather than
    // hiding, and the outline stays selectable and workable beside it.
    emptyNote: documentKeys.length === 0 ? LOADED_SELECTOR_EMPTY_NOTE : null,
  });
}

// One counter per module load, so each mounted rail's sr-only reason carries an
// id no sibling rail can collide with (the canvas does the same for its own
// per-instance ids).
let railSequence = 0;

export function mountDoxBenchChatRail(host, options = {}) {
  const {
    scopeKey, transports, editorState, activeDocumentPath, onState,
  } = options;
  const doc = host.ownerDocument;
  let state = createChatState(scopeKey);
  // T104 F1: the key a turn DECLARES. It used to be the object literal
  // destructured above, captured once at mount, so a Save that moved the
  // buffers onto a branch session left every later turn naming the pre-session
  // ref — the disagreement the server's FR-015 buffer binding refuses. `rekey`
  // now moves this too, which is what makes it a re-key rather than a state
  // reset.
  let currentScopeKey = scopeKey;
  // The catalog is a property of the PLANE, not of the conversation, and it is
  // fetched exactly once (in `ready` below). `rekeyChatState` correctly starts
  // a FRESH conversation on a new scope key (FR-011 isolation), which would
  // otherwise leave the rail with no models and no way back to any — a second
  // dead end in place of the first.
  let catalogEnvelope = null;
  let destroyed = false;
  const dispatcher = createTurnDispatcher({
    transports, turnIdFactory: options.turnIdFactory });
  const proposalActions = createProposalActions({
    applyProposal: options.applyProposal || (async () => null),
    // W-3: the card actions settle against the rail's LIVE state, so a
    // turn that lands or typing that happens during the seam's await is
    // never clobbered by the click-time snapshot.
    liveState: () => state });

  const el = (tag, className, text) => {
    const node = doc.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };

  // T100 P1-C (operator ruling: dual-target stays, disclosure fixed): a
  // persistent header names BOTH buffers a turn grounds on and a proposal
  // may rewrite, updating as the active document changes.
  const header = el("div", "doxchat-header");
  // THE LOADED-DOCUMENT SELECTOR (Q1 ruled). A native scrolling select, so the
  // control IS the overflow policy (D6) and the surface introduces no second
  // spelling of selection: it is the same element idiom the approved-model
  // selector already uses, keyboard-reachable with the platform's own semantics.
  const loadedSelect = el("select", "doxchat-loaded");
  loadedSelect.setAttribute("aria-label", "loaded document");
  // A workbench selection, not a form answer — the same autofill refusal every
  // other authoring control on this surface carries.
  loadedSelect.setAttribute("autocomplete", "off");
  // The SELECTED entry's FULL name, for assistive technology. The visible label
  // may be a basename (or the shortest distinguishing suffix); "the full name
  // MUST be available to assistive technology" is a separate obligation from
  // hover, and a title attribute alone does not discharge it.
  const loadedFull = el("div", "doxchat-loaded-full doxchat-sronly");
  loadedFull.setAttribute("aria-live", "polite");
  // The honest empty state — rendered, never hidden.
  const loadedEmpty = el("div", "doxchat-loaded-empty");
  // THE UNLOAD AFFORDANCE (PR #207 review, F9). The ratified loaded-set
  // requirement says "a document SHALL leave the loaded set only by an explicit
  // human act, and that act MUST refuse or require an explicit discard while the
  // buffer is dirty" — and the state primitive for it shipped with no control, so
  // the act did not exist and the declared bound was a dead end: a session that
  // reached it could never get back under it.
  //
  // It lives HERE, beside the selector, because this is the surface that presents
  // the loaded set — the same reason the selector is here. It is scoped to the
  // SELECTED entry, which is the one a human is looking at, and it is unreachable
  // while the outline is selected: the outline's key is permanently reserved and
  // it is the one buffer that rides every turn.
  const unloadBtn = el("button", "doxchat-unload", "Unload");
  unloadBtn.type = "button";
  const loadedNote = el("div", "doxchat-loaded-note");
  loadedNote.setAttribute("aria-live", "polite");
  loadedNote.hidden = true;
  const subjectInput = el("input", "doxchat-subject");
  subjectInput.setAttribute("aria-label", "working subject");
  subjectInput.setAttribute("autocomplete", "off");
  subjectInput.setAttribute("dir", "auto");
  const selector = el("select", "doxchat-model");
  selector.setAttribute("aria-label", "approved model");
  // The choice is workbench state, not a form answer — the same autofill
  // refusal every other authoring control on this surface carries.
  selector.setAttribute("autocomplete", "off");
  // T104 F5-9 residual: the rail's own unavailability posture. It stands in
  // for the selector while the catalog has no available entry (including
  // before any catalog has adopted), so the rail never looks fully live
  // beside the shell's "chat is unavailable" posture line; a catalog that
  // arrives later swaps it back for the live selector through the ordinary
  // render — the rail is never unmounted for this. P3-8: it is SEEDED with
  // the loading sentence, not the configured-none claim — at construction
  // the catalog has not answered, and render() keeps whichever sentence
  // unavailabilityNote derives from the state's own facts.
  const unavailableNote = el("div", "doxchat-unavailable doxchat-sronly",
                             CHAT_CATALOG_LOADING_NOTE);
  const transcriptList = el("ul", "doxchat-transcript");
  transcriptList.setAttribute("aria-label", "chat transcript");
  const failureNote = el("div", "doxchat-failure");
  failureNote.hidden = true;
  failureNote.setAttribute("aria-live", "polite");
  const cardsHost = el("div", "doxchat-proposals");
  cardsHost.setAttribute("aria-label", "typed proposals");
  // T100 P2: the applied/rejected outcome is ANNOUNCED, not whispered — a
  // visually-hidden assertive-free live region beside the cards.
  const announce = el("div", "doxchat-announce");
  announce.setAttribute("aria-live", "polite");
  const composer = el("textarea", "doxchat-composer");
  composer.setAttribute("aria-label", "chat message");
  composer.setAttribute("autocomplete", "off");
  composer.setAttribute("dir", "auto");
  // T101 ux CHK015 + PR #63 review: the send-moment disclosure sits beside
  // Send and always names the SELECTED model's server-declared handling.
  const disclosure = el("div", "doxchat-disclosure");
  disclosure.setAttribute("aria-live", "polite");
  const sendBtn = el("button", "doxchat-send", "Send");
  sendBtn.type = "button";
  // THE SEND ROW (Brett's 2026-08-18 annotation round 2: "add a model selector
  // down next to the send button"). The approved-model selector used to sit up
  // by the working subject, three regions away from the control its choice
  // governs; it belongs where the turn is sent from. Same element, same
  // `selectModel` binding, same `canSend` authority — only its place moved.
  const sendrow = el("div", "doxchat-sendrow");
  sendrow.append(selector, sendBtn);
  // …and the unavailability sentence goes sr-only: it is the send button's
  // stated REASON now (title + aria-describedby below), not a standing line.
  // "make this text the hover text for the send button if no model selected."
  // The class is set at CONSTRUCTION rather than through classList, because the
  // rail's own DOM stub is deliberately minimal and this module has never
  // needed classList — a view that reaches for one API more than it must is a
  // view its harness has to grow to match.
  unavailableNote.id = "doxchat-unavailable-" + (railSequence += 1);
  sendBtn.setAttribute("aria-describedby", unavailableNote.id);
  host.append(header, loadedSelect, unloadBtn, loadedNote, loadedEmpty,
              loadedFull, subjectInput,
              unavailableNote, transcriptList,
              cardsHost, announce, failureNote, composer, disclosure, sendrow);

  // SELECTING IS IMMEDIATE, and it is not a state authority: the seam owns the
  // move, `state.active_buffer` remains the one answer, and this handler only
  // asks. No confirmation step, because changing which buffer is selected
  // replaces no content and destroys nothing — the unsaved-edit guard is not
  // extended to selection now that documents are held side by side rather than
  // in one slot.
  //
  // TODO(add-doxbench-editing-phase-b tasks.md §9): switching the selection must
  // also switch WHICH THREAD the transcript shows and appends to. The thread
  // sidecar and its persistence land in the threads slice; this handler is the
  // one place that call belongs, and it is deliberately left as the selection
  // move alone rather than half-wired to a store that does not exist yet.
  loadedSelect.addEventListener("change", async () => {
    const wanted = String(loadedSelect.value || "");
    const model = loadedSelectorModel(liveEditorState());
    if (!model.entries.some((entry) => entry.key === wanted)) {
      // A value naming no held buffer is put back rather than acted on: the
      // selector renders the selection, it never invents one.
      renderLoadedSelector();
      return;
    }
    const select = options.selectBuffer;
    if (typeof select === "function") await select(wanted);
    renderLoadedSelector();
    renderHeader();
  });

  // The unload act: explicit, scoped to the selected document, and REFUSED while
  // that buffer is dirty unless the human states the discard — which they do by
  // pressing it a second time, on a control that has changed its own label to say
  // what the second press means. Dropping unsaved work silently is the one thing
  // this control must never do.
  let unloadArmedKey = null;
  unloadBtn.addEventListener("click", async () => {
    const model = loadedSelectorModel(liveEditorState());
    const chosen = model.entries.find((entry) => entry.selected);
    // Refused here as well as withheld above (N3): a reserved buffer leaving the
    // set is the one act that can wedge the chat, so the click path does not
    // depend on the render having disabled the control.
    if (!chosen || chosen.kind !== "document" || chosen.reserved === true) return;
    const unload = options.unloadBuffer;
    if (typeof unload !== "function") return;
    const arming = unloadArmedKey === chosen.key;
    const outcome = await unload(chosen.key, { discardUnsavedEdits: arming });
    if (outcome && outcome.ok === true) {
      unloadArmedKey = null;
      loadedNote.textContent = "unloaded — its unsaved edits, if any, are gone";
      loadedNote.hidden = false;
    } else {
      // ARMED, not performed: the refusal names what a second press will do.
      unloadArmedKey = chosen.key;
      loadedNote.textContent = (outcome && outcome.error)
        || "this document was not unloaded";
      loadedNote.hidden = false;
    }
    renderLoadedSelector();
    renderHeader();
  });

  function liveEditorState() {
    return typeof editorState === "function" ? editorState() : editorState;
  }

  // The selector is rebuilt from the live state on every render, which is what
  // makes "the selector, the canvas and the chat agree" structural rather than a
  // rule three call sites have to remember.
  function renderLoadedSelector() {
    const model = loadedSelectorModel(liveEditorState());
    loadedSelect.textContent = "";
    for (const entry of model.entries) {
      const option = el("option", "doxchat-loaded-option", entry.label);
      option.value = entry.key;
      // HOVER reveals the full name (Q1's own words), and the same string is
      // handed to assistive technology.
      option.setAttribute("title", entry.fullName);
      option.setAttribute("aria-label", entry.fullName);
      if (entry.selected) option.setAttribute("selected", "selected");
      // A context-only document is loadable for grounding and conversation, and
      // its non-owned status rides the entry so the surface never implies it can
      // be saved here (design D2).
      if (entry.kind === "document" && entry.owned !== true) {
        option.setAttribute("data-owned", "false");
      }
      if (entry.dirty) option.setAttribute("data-dirty", "true");
      loadedSelect.appendChild(option);
    }
    loadedSelect.value = model.selected;
    loadedSelect.disabled = model.entries.length === 0;
    loadedEmpty.textContent = model.emptyNote || "";
    loadedEmpty.hidden = model.emptyNote === null;
    const chosen = model.entries.find((entry) => entry.selected);
    loadedFull.textContent = chosen
      ? "Working on " + chosen.fullName
      : "no buffer is selected";
    // Unload is reachable only for a selected DOCUMENT, and only where the seam
    // exists at all: on a surface with no editing capability there is no loaded
    // set to leave.
    const unloadable = Boolean(chosen) && chosen.kind === "document"
      && chosen.reserved !== true
      && typeof options.unloadBuffer === "function";
    unloadBtn.disabled = !unloadable;
    if (!unloadable) {
      unloadArmedKey = null;
      unloadBtn.textContent = "Unload";
      if (chosen && chosen.reserved === true) {
        // ONE sentence for both reserved keys, because it is one fact: under the
        // released envelope the outline and the reserved document slot are the two
        // buffers every turn carries, so unloading either would leave the chat
        // unable to build a turn at all.
        unloadBtn.title = chosen.kind === "outline"
          ? "the outline is a reserved buffer that rides every turn, and is never "
            + "unloaded"
          : "this is the tile's own document, a reserved buffer that rides every "
            + "turn, and is never unloaded — load another document to work beside it";
      } else {
        unloadBtn.title = "no loaded document is selected";
      }
      return;
    }
    const armed = unloadArmedKey === chosen.key;
    unloadBtn.textContent = armed ? "Discard and unload" : "Unload";
    unloadBtn.title = armed
      ? "press again to DISCARD this document's unsaved edits and unload it"
      : "unload " + chosen.fullName + " from the loaded set";
  }

  function renderHeader() {
    const es = liveEditorState();
    const nameOf = (b) => {
      if (!b) return "(absent)";
      if (b.path === null || b.path === undefined) return "(not yet created)";
      return String(b.path).split("/").at(-1);
    };
    // add-doxbench-editing-phase-a: the chat's WORKING CONTEXT is the canvas's
    // ACTIVE BUFFER — the one the context region selected — and it is read
    // straight off the live editor state rather than tracked a second time
    // here. Grounding is unchanged and still names EVERY buffer: binding says
    // what the chat is working ON, never what it may see.
    //
    // add-doxbench-editing-phase-b: "every loaded document" is now a SET, so the
    // header states the binding and the COUNT rather than enumerating two fixed
    // names it no longer has. The enumeration lives in the selector beside it,
    // which is where a human can also act on it.
    const bound = es && es.buffers ? es.buffers[es.active_buffer] : null;
    const boundName = bound ? nameOf(bound) : "(absent)";
    const model = loadedSelectorModel(es);
    const grounded = model.documentCount === 1
      ? "1 loaded document"
      : String(model.documentCount) + " loaded documents";
    header.textContent = "Working on — " + boundName
      + " · Chatting about — Outline: "
      + nameOf(es && es.buffers ? es.buffers.outline : null)
      + " · " + grounded;
    renderLoadedSelector();
  }

  // (The captured-node `restoreFocus` helper that used to live here went
  // with P3-7: the send path was its last caller, and it embodied exactly
  // the restore-by-node pattern F7-4 and P3-7 retired.)

  // T104 F7-4: focus after a card action is restored by IDENTITY (proposal
  // target + role), never by the captured node — renderCards() rebuilds the
  // whole cards host, so the node a handler captured is detached by the time
  // the action settles, and `.focus()` on a detached node no-ops, dropping
  // focus to <body>. The editor solves this class the same way (it remembers
  // WHICH buffer held focus, not the node). `cardControls` is rebuilt by
  // every renderCards pass, so the lookup always answers with the LIVE
  // control for that identity.
  let cardControls = { outline: null, document: null };

  function restoreCardFocus(targetValue, roleValue) {
    const rebuilt = cardControls[targetValue];
    const control = rebuilt && rebuilt[roleValue];
    if (control && control.disabled !== true) {
      control.focus();
      return;
    }
    // The stated FALLBACK: the card reached a terminal state (applied /
    // rejected) and both its actions are disabled, so the equivalent control
    // cannot take focus. The composer is the surviving control the operator
    // acts through next — every terminal note names a NEW TURN as the only
    // continuation, and the composer is where one starts.
    composer.focus();
  }

  function renderCards() {
    cardsHost.textContent = "";
    cardControls = { outline: null, document: null };
    for (const card of proposalCardModel(state)) {
      const item = el("div", "doxchat-card doxchat-card-" + card.status);
      item.setAttribute("role", "group");
      item.setAttribute("aria-label", card.ariaLabel);
      const badge = el("span", "doxchat-card-target",
                       card.target.toUpperCase());
      const summaryNode = el("span", "doxchat-card-summary", card.summary);
      summaryNode.setAttribute("dir", "auto");
      item.append(badge, summaryNode,
                  el("span", "doxchat-card-note", card.note));
      const applyBtn = el("button", "doxchat-card-apply", "Apply");
      applyBtn.type = "button";
      applyBtn.disabled = !card.applyEnabled;
      applyBtn.addEventListener("click", async () => {
        const before = proposalsOf(state)[card.target];
        const failureBefore = state.lastFailure;
        adopt(await proposalActions.apply(state, card.target));
        const after = proposalsOf(state)[card.target];
        if (before && after && before.status !== "applied"
            && after.status === "applied") {
          announce.textContent =
            "Proposal applied to the working copy. Save remains the only exit.";
        } else if (state.lastFailure && state.lastFailure !== failureBefore) {
          // T104 F5-5: the refused Apply is ANNOUNCED like the applied
          // transition above, with the same fixed sentence the failure note
          // renders — a change a screen reader hears, not just a note a
          // sighted operator might spot.
          announce.textContent = state.lastFailure.message;
        }
        restoreCardFocus(card.target, "apply");
      });
      const rejectBtn = el("button", "doxchat-card-reject", "Reject");
      rejectBtn.type = "button";
      rejectBtn.disabled = !card.rejectEnabled;
      rejectBtn.addEventListener("click", async () => {
        adopt(await proposalActions.reject(state, card.target));
        restoreCardFocus(card.target, "reject");
      });
      item.append(applyBtn, rejectBtn);
      cardControls[card.target] = { apply: applyBtn, reject: rejectBtn };
      cardsHost.appendChild(item);
    }
  }

  function render() {
    renderHeader();
    subjectInput.value = state.workingSubject;
    composer.value = state.composer;
    selector.textContent = "";
    const placeholder = el("option", "", "select an approved model");
    placeholder.value = "";
    selector.appendChild(placeholder);
    for (const entry of state.models || []) {
      if (entry.available !== true) continue;
      // PR #63 review (Codex P2): each selectable model carries its
      // handling text, reviewable before selection.
      const handling = entry.data_handling ? String(entry.data_handling) : "";
      const opt = el("option", "",
        handling ? entry.label + " — " + handling : String(entry.label));
      opt.value = entry.model_id;
      selector.appendChild(opt);
    }
    disclosure.textContent = sendDisclosure(state) || "";
    disclosure.hidden = !sendDisclosure(state);
    // T104 F5-9 originally traded the SELECTOR against the unavailability NOTE:
    // exactly one of the two showed. Brett's 2026-08-18 annotation round 2
    // changes both halves. The selector is a permanent part of the send row —
    // "add a model selector down next to the send button" — so with no
    // available entry it renders EMPTY AND DISABLED rather than vanishing,
    // which is the honest shape of this plane's posture: the server exposes a
    // catalog and it is empty, not absent. And the note is no longer a standing
    // line at all: it is sr-only, and its sentence is the send button's stated
    // reason. WHICH sentence it carries is unchanged — the model's
    // catalogFailure fact (T104 F10-1): stale token, unreadable catalog, or the
    // configured-none default.
    const selectable = (state.models || []).some(
      (entry) => entry.available === true);
    selector.disabled = !selectable;
    unavailableNote.textContent = selectable ? "" : unavailabilityNote(state);
    selector.value = state.selectedModelId || "";
    transcriptList.textContent = "";
    for (const turn of transcriptWindow(state)) {
      const item = el("li", "doxchat-turn doxchat-" + turn.role, turn.content);
      item.setAttribute("dir", "auto");
      transcriptList.appendChild(item);
    }
    renderCards();
    failureNote.hidden = !state.lastFailure;
    failureNote.textContent = state.lastFailure
      ? state.lastFailure.message : "";
    // ONE authority for "may this turn be sent", shared with the model
    // (`canSend`), plus a label that SAYS a turn is running. Disabling alone
    // explained nothing: the operator clicked twice during a slow turn
    // precisely because the button still looked available, and the second
    // click sent an empty message the schema refused as malformed.
    const inFlight = state.phase !== "idle";
    // F1 (PR #207 review): a selection the released envelope cannot carry holds
    // Send closed BEFORE any provider is reached, and the reason rides the
    // control and the sr-only region the control already points at with
    // `aria-describedby` — so it is programmatically associated rather than
    // living only in a hover title.
    const binding = chatBindingPosture(liveEditorState());
    sendBtn.disabled = !canSend(state) || !binding.ok;
    sendBtn.textContent = inFlight ? "Sending…" : "Send";
    // The reason is a MODEL reason only while no model is actually selectable or
    // selected; once one is chosen, an empty composer is a different reason and
    // must not borrow this sentence.
    // The BINDING reason wins when it applies: it names a limitation of this
    // surface's own wire, which no model choice can fix.
    const modelReason = !binding.ok
      ? binding.reason
      : (state.selectedModelId ? null : unavailabilityNote(state));
    sendBtn.title = sendTitle(inFlight, sendBtn.disabled, modelReason);
    if (!binding.ok) unavailableNote.textContent = binding.reason;
    if (typeof onState === "function") onState(state);
  }

  function adopt(nextState) {
    if (destroyed) return;
    state = nextState;
    render();
  }

  // T104 F10-2/4: the model refuses an over-bound edit by returning the
  // IDENTICAL state object — the one case an input event can produce it,
  // since an in-bound edit always builds a new state (even for equal text).
  // The refusal lands on the visible channel (recordLocalFailure), naming
  // the bound; the render that follows reverts the DOM to the last accepted
  // text, which is the refused-never-truncated posture made visible.
  //
  // P3-4 (wave re-review P3 tail): the over-bound notes are PRESENT-TENSE
  // claims ("this message exceeds the ... bound") that go false the moment
  // the text is shortened — and in the editor-only posture, where no turn
  // ever settles, nothing else could clear them: the note was permanent. So
  // a successful in-bound edit clears ITS OWN field's note, and ONLY that:
  // the other field's note and every other failure class (transport, apply,
  // send-path) keep the existing settlement-only lifecycle.
  const clearedOwnBound = (nextState, boundError) =>
    (nextState.lastFailure && nextState.lastFailure.error === boundError
      ? clearLocalFailure(nextState) : nextState);
  subjectInput.addEventListener("input", () => {
    const next = editSubject(state, subjectInput.value);
    adopt(next === state
      ? recordLocalFailure(state, SUBJECT_OVER_BOUND)
      : clearedOwnBound(next, SUBJECT_OVER_BOUND.error));
  });
  composer.addEventListener("input", () => {
    const next = editComposer(state, composer.value);
    adopt(next === state
      ? recordLocalFailure(state, MESSAGE_OVER_BOUND)
      : clearedOwnBound(next, MESSAGE_OVER_BOUND.error));
  });
  selector.addEventListener("change",
    () => adopt(selectModel(state, selector.value)));
  sendBtn.addEventListener("click", async () => {
    // P3-7 (wave re-review P3 tail): focus is restored by INTENT, never by
    // the captured node — the F7-4 class, on the send path. A send that
    // settles successfully clears the composer, canSend goes false, and
    // render() disables Send: `.focus()` on the captured, now-disabled
    // control no-ops and a keyboard operator landed on <body>. What is
    // captured is only the FACT that Send held focus, for the failure case.
    const sendHadFocus = doc.activeElement === sendBtn;
    let succeeded = false;
    let settled = false;
    try {
      const result = await dispatcher.submit(state, {
        scopeKey: currentScopeKey,
        activeDocumentPath: typeof activeDocumentPath === "function"
          ? activeDocumentPath() : (activeDocumentPath ?? null),
        // T104 F2: the tile's USABLE documents, so a no-active-document
        // refusal can name one instead of leaving the operator to guess.
        documentCandidates: options.documentCandidates,
        editorState,
        // Refused states carry the visible fixed note (R2); abandoned
        // results hand back the live state unchanged (R1) — adopt whatever
        // came back and restore focus.
        onBegin: adopt,
        liveState: () => state,
      });
      if (result.state) adopt(result.state);
      succeeded = result.ok === true;
      // P3-3 (wave re-review P3 tail): proposals adopted from an in-flight
      // turn scored `current` unconditionally — a document switch or Discard
      // landing DURING the flight fired its identity event before these
      // proposals existed, so nothing ever re-scored them and the card
      // offered an enabled Apply against text the buffer no longer held.
      // Re-score the just-adopted set against the LIVE editor identities.
      // An UNSETTLED identity (hash_pending) cannot re-score, so the
      // re-score is skipped entirely in that window — the stated choice:
      // that buffer's own settle fires onIdentitySettled, which reaches
      // refreshCurrency through the composition moments later.
      if (succeeded) {
        const liveEditor = typeof editorState === "function"
          ? editorState() : editorState;
        const outline = liveEditor && liveEditor.buffers
          && liveEditor.buffers.outline;
        const documentBuffer = liveEditor && liveEditor.buffers
          && liveEditor.buffers.document;
        if (bufferSettled(outline) && bufferSettled(documentBuffer)) {
          adopt(refreshProposalCurrency(state, {
            outline: hexOf(outline.current_hash),
            document: hexOf(documentBuffer.current_hash),
          }));
        }
      }
      settled = true;
    } finally {
      // T100 P1-2 defense-in-depth: an unexpected throw anywhere above must
      // never leave the rail wedged in_flight with a dead Send — settle to
      // the fixed failed-idle state, composer preserved (SEND_PATH_FAILED).
      if (!settled && state.phase === "in_flight") {
        adopt(settleTurnFailure(state, SEND_PATH_FAILED));
      }
      // P3-7, the intent rules. SUCCESS: the composer, where the next
      // message starts. FAILURE (refusals and abandons included): the
      // re-enabled Send control if that is where the operator was — the
      // retry is one keypress — else the composer, where the preserved
      // message is edited. The disabled check keeps the fallback honest for
      // failures that leave Send closed (e.g. no model selected).
      if (succeeded) {
        composer.focus();
      } else if (sendHadFocus && sendBtn.disabled !== true) {
        sendBtn.focus();
      } else {
        composer.focus();
      }
    }
  });

  const ready = (async () => {
    if (transports && typeof transports.catalog === "function") {
      let envelope = null;
      try {
        envelope = await transports.catalog();
      } catch (unused) {
        envelope = null;  // a THROWN transport: the answer was not read
      }
      // T104 F10-1: the transport's outcomes, each to its honest posture.
      // A distinguished failure ({ failed }) carries its fixed reason; a
      // null (thrown transport, unparseable 200) IS a catalog that could
      // not be read; a 200 body that is not the released envelope shape
      // (adoptCatalog refuses it, fail closed) is the same fact. Only a
      // real adoption clears the failure and lights the selector.
      if (envelope && envelope.failed) {
        adopt(recordCatalogFailure(state, envelope.failed));
      } else if (envelope) {
        const adopted = adoptCatalog(state, envelope);
        if (adopted === state) {
          adopt(recordCatalogFailure(state, "unreadable"));
        } else {
          catalogEnvelope = envelope;
          adopt(adopted);
        }
      } else {
        adopt(recordCatalogFailure(state, "unreadable"));
      }
    } else {
      // P3-8: no catalog transport means no answer will EVER settle -- the
      // loading sentence would stand forever, a different lie. The honest
      // fact is "this plane cannot read a catalog", which IS the unreadable
      // posture. (The shell only mounts the rail with both transports, so
      // this arm is a composition-error backstop, not a production path.)
      adopt(recordCatalogFailure(state, "unreadable"));
    }
  })();
  render();

  return {
    ready,
    state: () => state,
    rekey(keyValue) {
      currentScopeKey = keyValue;
      let next = rekeyChatState(state, keyValue);
      // A FRESH conversation on the new key (transcript, composer, subject,
      // proposals and failure all cleared — FR-011), but the plane's already
      // fetched catalog is re-adopted so the rail can still be used. Only
      // reached when the key really moved: `rekeyChatState` returns the same
      // state object for an unchanged key. A catalog FAILURE is a fact about
      // the PLANE, exactly like the catalog itself, so it survives the
      // conversation reset too (T104 F10-1) — otherwise a re-key would
      // silently downgrade the honest failure posture to configured-none.
      if (next !== state && catalogEnvelope) {
        next = adoptCatalog(next, catalogEnvelope);
      } else if (next !== state && state.catalogFailure) {
        next = recordCatalogFailure(next, state.catalogFailure);
      }
      adopt(next);
    },
    refreshCurrency(currentHashes) {
      adopt(refreshProposalCurrency(state, currentHashes));
    },
    // R-1: the pure blob the shell persists beside the buffers, and the
    // restore that re-scores proposals against the restored bytes.
    snapshot() { return chatSnapshot(state); },
    restore(snapshotValue, currentHashes) {
      adopt(restoreChatState(state, snapshotValue, currentHashes));
    },
    abort() { adopt(abortTurn(state)); },
    destroy() {
      destroyed = true;
      host.textContent = "";
    },
  };
}
