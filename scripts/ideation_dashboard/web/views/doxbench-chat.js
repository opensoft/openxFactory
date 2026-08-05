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

// T104 F5-5: the FIXED refusal for an Apply the buffer seam would not take.
// The seam's dominant refusal is staleness caught at the swap itself
// (doxbench-editor.applyProposal revalidates the base against the SETTLED
// current identity), and its own error text — like anything a throwing seam
// carries — is dropped unread, same discipline as TRANSPORT_REFUSED: this
// sentence, the canvas's own vocabulary for that condition, is the whole
// failure surface, and it names the only recovery.
const PROPOSAL_APPLY_REFUSED = Object.freeze({
  error: "proposal_apply_refused",
  message: "this proposal no longer matches the buffer — ask again in a "
    + "new turn",
});

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
function sendTitle(inFlight, disabled) {
  if (inFlight) return "a turn is in flight — one turn at a time per conversation";
  if (disabled) return "select an approved model and type a message to send";
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
        // other refusal renders through.
        return recordLocalFailure(live, PROPOSAL_APPLY_REFUSED);
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
  const subjectInput = el("input", "doxchat-subject");
  subjectInput.setAttribute("aria-label", "working subject");
  subjectInput.setAttribute("autocomplete", "off");
  subjectInput.setAttribute("dir", "auto");
  const selector = el("select", "doxchat-model");
  selector.setAttribute("aria-label", "approved model");
  // T104 F5-9 residual: the rail's own unavailability posture. It stands in
  // for the selector while the catalog has no available entry (including
  // before any catalog has adopted), so the rail never looks fully live
  // beside the shell's "chat is unavailable" posture line; a catalog that
  // arrives later swaps it back for the live selector through the ordinary
  // render — the rail is never unmounted for this. P3-8: it is SEEDED with
  // the loading sentence, not the configured-none claim — at construction
  // the catalog has not answered, and render() keeps whichever sentence
  // unavailabilityNote derives from the state's own facts.
  const unavailableNote = el("div", "doxchat-unavailable",
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
  host.append(header, subjectInput, selector, unavailableNote, transcriptList,
              cardsHost, announce, failureNote, composer, disclosure, sendBtn);

  function renderHeader() {
    const es = typeof editorState === "function" ? editorState() : editorState;
    const nameOf = (b) => {
      if (!b) return "(absent)";
      if (b.path === null || b.path === undefined) return "(not yet created)";
      return String(b.path).split("/").at(-1);
    };
    const outline = es && es.buffers ? es.buffers.outline : null;
    const documentBuffer = es && es.buffers ? es.buffers.document : null;
    header.textContent = "Chatting about — Outline: " + nameOf(outline)
      + " · Document: " + nameOf(documentBuffer);
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
    // T104 F5-9: exactly one of {selector, unavailability note} shows. No
    // available entry — a null catalog (not yet adopted or refused) or an
    // adopted empty one (FR-025 editor-only) — is the note's condition, the
    // same fact that keeps canSend false. WHICH sentence the note carries is
    // the model's catalogFailure fact (T104 F10-1): stale token, unreadable
    // catalog, or the configured-none default.
    const selectable = (state.models || []).some(
      (entry) => entry.available === true);
    selector.hidden = !selectable;
    unavailableNote.hidden = selectable;
    unavailableNote.textContent = unavailabilityNote(state);
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
    sendBtn.disabled = !canSend(state);
    sendBtn.textContent = inFlight ? "Sending…" : "Send";
    sendBtn.title = sendTitle(inFlight, sendBtn.disabled);
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
