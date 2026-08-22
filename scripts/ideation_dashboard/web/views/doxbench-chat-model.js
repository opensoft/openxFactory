// doxbench-chat-model.js — T052 (US2): PURE browser-session chat state for
// doxBench. Import-free like doxbench-state.js, by the same rule: the Node
// test harness imports this file alone, and purity is the enforced boundary
// (no fetch, no DOM, no storage, no timers — the transports live in app.js
// and the view in doxbench-chat.js).
//
// Every function returns NEW frozen values and never mutates its input.
// The TEXT bounds — subject, message, transcript — measure exact UTF-8 BYTES
// (never code points), mirroring doxbench-state.js's utf8Size and the feature's
// content-identity rule. ONE bound does not, and the exception is deliberate
// (fresh-eyes review F3, which caught this sentence claiming all of them do):
// CONTEXT_REDUCED_REASON_MAX_LENGTH counts CODE POINTS, because it mirrors the
// released schema's `maxLength` rather than a content identity, and JSON Schema
// counts `maxLength` in code points. Counting that one in bytes would refuse
// records the released contract accepts.
// Wire spellings follow the RELEASED contract-v1.27 chat-turn schema:
// transcript turns are `{role, content}` — the server-side dataclass's
// `.text` is an internal name, not the wire — and an empty catalog `models`
// array is a SUCCESS (FR-025 editor-only posture), never an error.
//
// Over-bound input is REFUSED (the same state is returned), never truncated:
// "no silent truncation is permitted" (plan.md Constraints).

export const DOXBENCH_CHAT_STATE_VERSION = 1;
export const DOXBENCH_CHAT_STATE_KIND = "doxbench-chat-state";
export const MAX_WORKING_SUBJECT_BYTES = 512;
export const MAX_MESSAGE_BYTES = 16_384;
export const MAX_TRANSCRIPT_TURNS = 20;
export const MAX_TRANSCRIPT_BYTES = 64_000;
export const CHAT_PHASES = Object.freeze(["idle", "in_flight"]);

const CATALOG_WIRE_KIND = "workbench-model-catalog";
const ENCODER = new TextEncoder();

function utf8Size(value) {
  return ENCODER.encode(value).length;
}

function frozenKey(keyValue) {
  return Object.freeze({
    repository: String(keyValue.repository),
    ref: String(keyValue.ref),
    tile_kind: String(keyValue.tile_kind),
    tile_id: String(keyValue.tile_id),
  });
}

function sameKey(a, b) {
  return (a.repository === b.repository && a.ref === b.ref
          && a.tile_kind === b.tile_kind && a.tile_id === b.tile_id);
}

function next(stateValue, patch) {
  return Object.freeze({ ...stateValue, ...patch });
}

// THE WORKING SUBJECT'S DEFAULT (promoted requirement "Browser-local doxBench
// conversation": "The working subject SHALL default from the tile's title or
// summary, remain editable"). It was unrealized -- this function seeded an empty
// subject and nothing ever filled it, which is what Brett's 2026-08-21
// annotation measured from the surface ("what is the box used for?") and what
// add-doxbench-editing-phase-b's Amendment 2 recorded as a realization gap.
//
// WHICH HALF OF "title or summary". The tile record carries a title and no
// summary: the workbench scope resolves ONE display title per tile kind
// (a cluster's `name`, a possible's `title`, a staged topic's `staging_id`) and
// the snapshot family declares no field NAMED summary on any of the three (the
// nearest summary-shaped field, `possible.claim`, is deliberately not used --
// the title is the one field all three kinds share, and a disjunction is
// satisfied by either half). So the caller hands down that one
// already-resolved title, and no second derivation and no unreachable summary
// branch is invented here.
//
// THE SEED OBEYS THE HUMAN EDIT'S OWN RULE, by going through it: `editSubject`
// refuses a non-string or over-512-byte value by returning the state unchanged,
// so an over-long title seeds NOTHING and the field stays empty (the placeholder
// then says what it is). A bounded PREFIX was considered and rejected: this
// module truncates nothing, and a clipped title is text the human never typed.
// Empty is always sendable, so the refused seed can never leave Send refusing a
// value nobody entered.
//
// A STORED VALUE ALWAYS WINS. `restoreChatState` runs after this one, on the
// same fresh state, and adopts the persisted subject over the seed -- see the
// note there for what an empty stored subject means.
export function createChatState(keyValue, subjectDefaultValue) {
  const fresh = Object.freeze({
    version: DOXBENCH_CHAT_STATE_VERSION,
    kind: DOXBENCH_CHAT_STATE_KIND,
    key: frozenKey(keyValue),
    models: null,            // null = catalog not adopted yet (distinct from [])
    // T104 F10-1: WHY there is no catalog, when the reason is a failure.
    // `models: null` alone cannot distinguish a catalog not fetched yet
    // against a fetch that was refused, so every failure rendered as the
    // configured-none posture. Fixed two-value vocabulary
    // ("console_required" | "unreadable"), set only by recordCatalogFailure
    // below, cleared by a successful adoption.
    catalogFailure: null,
    selectedModelId: null,
    workingSubject: "",
    composer: "",
    phase: "idle",
    pendingMessage: null,    // the composer content captured at beginTurn
    transcript: Object.freeze([]),
    lastFailure: null,
    proposals: NO_PROPOSALS,
    // WHAT THE LAST ANSWER RAN ON (contract-v1.40, task 10.7). The released
    // record now STATES the posture its context packet was assembled under, and
    // this is where that statement lands so the rail can show it. Null means
    // "no answer to describe, or an answer that stated no posture" — a fresh
    // conversation, a thread just switched to, or a record from a producer
    // older than contract-v1.40 — and is NOT a claim that the context was full.
    // It describes THE TRANSCRIPT'S LAST ASSISTANT ANSWER and changes exactly
    // when that answer does; see `beginTurn` for why a flight STARTING is not
    // one of those moments (adversarial review S4).
    // Deliberately a fact about the MOST RECENT ANSWER rather than a per-turn
    // annotation on the transcript: a transcript restored from the server's
    // thread sidecar carries no posture (the sidecar's turn header is a
    // fixed-arity format this release does not change), so per-turn badges
    // would be present on a lived-through turn and absent on the identical
    // restored one — a difference the reader would have to explain away.
    contextPacket: null,
  });
  return editSubject(fresh, subjectDefaultValue);
}

// T104 F5-7's shared question: does this catalog vouch for `candidate` as a
// SELECTABLE id? One rule for selection, adoption, restore, and the send
// gate — `selectModel`'s only-available-entries check was the rule, and it
// drifted because it lived only there. `models === null` means "no catalog
// adopted yet": nothing can be vouched for, so the answer is false.
function catalogVouchesFor(models, candidate) {
  if (typeof candidate !== "string" || candidate === "") return false;
  return Array.isArray(models) && models.some(
    (m) => m.model_id === candidate && m.available === true);
}

export function adoptCatalog(stateValue, envelopeValue) {
  // Only the released envelope shape is adopted; anything else leaves the
  // state unchanged (fail closed — the view keeps its editor-only posture).
  if (!envelopeValue || typeof envelopeValue !== "object"
      || envelopeValue.schema_version !== 1
      || envelopeValue.kind !== CATALOG_WIRE_KIND
      || !Array.isArray(envelopeValue.models)) {
    return stateValue;
  }
  const models = Object.freeze(envelopeValue.models.map(
    (entry) => Object.freeze({ ...entry })));
  return next(stateValue, {
    models,
    // A catalog that adopted IS readable: any earlier failure posture is
    // over (T104 F10-1).
    catalogFailure: null,
    // T104 F5-7's second half: the ARRIVING catalog re-validates whatever id
    // is held. A restore that ran before any catalog keeps its persisted id
    // on trust (see restoreChatState); this is where that trust is settled —
    // an id the new catalog cannot vouch for is dropped to null, so the
    // placeholder and the disabled Send agree instead of shipping an id the
    // server refuses as model_unavailable.
    selectedModelId: catalogVouchesFor(models, stateValue.selectedModelId)
      ? stateValue.selectedModelId : null,
  });
}

// T104 F10-1: a model-catalog FAILURE, recorded in the same fixed two-value
// vocabulary the transport's distinguished markers speak. Anything that is
// not the recoverable pre-identity console refusal is "unreadable" — the
// reason arrives as a marker chosen from the released error code, never as
// echoed server text (FR-020/FR-022), and this function re-normalizes so no
// third spelling can ever reach the view. The failure is a fact about the
// PLANE (which catalog answer this page got), not about the conversation, so
// chatSnapshot deliberately never persists it.
export function recordCatalogFailure(stateValue, reasonValue) {
  return next(stateValue, {
    catalogFailure: reasonValue === "console_required"
      ? "console_required" : "unreadable",
  });
}

export function selectModel(stateValue, modelIdValue) {
  const models = stateValue.models || [];
  const entry = models.find((m) => m.model_id === modelIdValue);
  if (!entry || entry.available !== true) {
    return stateValue;  // only available entries may be selected
  }
  return next(stateValue, { selectedModelId: entry.model_id });
}

export function editSubject(stateValue, textValue) {
  if (typeof textValue !== "string"
      || utf8Size(textValue) > MAX_WORKING_SUBJECT_BYTES) {
    return stateValue;  // refused, never truncated
  }
  return next(stateValue, { workingSubject: textValue });
}

export function editComposer(stateValue, textValue) {
  if (typeof textValue !== "string"
      || utf8Size(textValue) > MAX_MESSAGE_BYTES) {
    return stateValue;  // refused, never truncated
  }
  return next(stateValue, { composer: textValue });
}

// WHETHER A TURN COULD BE BUILT AT ALL — the one place that question is
// answered, so the view cannot drift from it.
//
// Found the hard way (operator, 2026-08-02): the view gated Send on
// `phase !== "idle"` and nothing else, so during a slow turn — composer
// already cleared, button still looking available — a second click sent an
// EMPTY message and the server refused it as malformed. The released request
// schema requires `message` minLength 1 and `model_id` minLength 1, so both an
// empty composer and an unselected model can ONLY ever produce a refusal. A
// surface that offers an action the contract forbids is lying about what it
// can do.
//
// Whitespace counts as empty: it is empty text wearing spaces, and trimming
// here does NOT mutate the composer — the human's text is never rewritten,
// only judged.
export function canSend(stateValue) {
  if (!stateValue || stateValue.phase !== "idle") return false;
  if (typeof stateValue.composer !== "string"
      || stateValue.composer.trim() === "") return false;
  // T104 F5-7: a non-empty id is not enough — it must name an AVAILABLE
  // entry of the adopted catalog, the same rule selectModel enforces. A
  // restored id awaiting its catalog (models still null) therefore keeps
  // Send closed: the selector is showing the placeholder in that window,
  // and a Send the selector contradicts would ship an id the server refuses
  // as model_unavailable with no data-handling disclosure ever shown.
  return catalogVouchesFor(stateValue.models, stateValue.selectedModelId);
}


export function beginTurn(stateValue) {
  // ONE turn in flight per conversation key (FR-018): a second begin is
  // refused by returning the identical state object.
  if (stateValue.phase !== "idle") {
    return stateValue;
  }
  // THE POSTURE NOTE IS NOT CLEARED HERE, and an earlier version of this
  // release cleared it here — which its adversarial review (S4) broke in one
  // move: a reduced answer followed by a FAILED follow-up left the reduced
  // answer holding the transcript with its disclosure GONE. That is precisely
  // the lost-badge defect this release cited when it rejected per-turn badges,
  // reappearing at rail level.
  //
  // THE INVARIANT IS SIMPLER THAN THE CLEAR WAS: the note describes THE
  // TRANSCRIPT'S LAST ASSISTANT ANSWER. So it changes exactly when that answer
  // does, and every path that replaces the answer already replaces the posture
  // beside it. There are FOUR of them, and the fourth was missing from this
  // list until the adversarial review found it (NEW-1): `settleTurnSuccess`
  // adopts the new record's (null included, for a producer older than
  // contract-v1.40), `adoptThreadTranscript` clears it with the transcript it
  // replaces, `rekeyChatState` starts fresh, and `restoreChatState` adopts the
  // SNAPSHOT's — which is why the snapshot now carries one. A flight STARTING
  // replaces no answer, so it changes nothing: while a turn is in the air the
  // note still describes the answer still on screen, which is true.
  //
  // The alternative the review offered — restore the posture in
  // `settleTurnFailure` — was REJECTED: `beginTurn` would have to stash the
  // value for `settleTurnFailure` to hand back, and `abortTurn` and
  // `recordLocalFailure` would each need the same restore, so ONE invariant
  // would be re-implemented at three sites instead of not being violated at
  // one.
  return next(stateValue, {
    phase: "in_flight",
    pendingMessage: stateValue.composer,
  });
}

export function abortTurn(stateValue) {
  // Local abandon only: nothing is appended, the composer survives verbatim.
  if (stateValue.phase !== "in_flight") {
    return stateValue;
  }
  return next(stateValue, { phase: "idle", pendingMessage: null });
}

function transcriptBytes(turnsValue) {
  return turnsValue.reduce((n, turn) => n + utf8Size(turn.content), 0);
}

function boundedAppend(transcriptValue, humanContent, assistantContent) {
  const turns = transcriptValue.concat([
    Object.freeze({ role: "human", content: String(humanContent) }),
    Object.freeze({ role: "assistant", content: String(assistantContent) }),
  ]);
  // Evict oldest WHOLE human/assistant pairs until both released bounds
  // hold — never split a pair, never truncate a turn's content.
  //
  // T104 F5-2: …and never evict the NEWEST pair. This is the DISPLAY
  // transcript, and a single LEGAL pair can exceed MAX_TRANSCRIPT_BYTES on
  // its own (message ≤ 16,384 + server-bounded prose ≤ 65,536 = up to
  // 81,920 bytes against a 64,000 bound) — the old loop kept evicting until
  // the bound held and emptied the transcript INCLUDING the answer that had
  // just arrived. The 64,000-byte bound mirrors the SERVER's REQUEST-side
  // transcript bound (doxbench_turns.MAX_TRANSCRIPT_BYTES) and is honoured
  // where it belongs, on the wire (`transcriptWireWindow` below); the
  // operator's answer never vanishes from the surface it was answered on.
  // The oversized pair remains ordinary history: the moment a newer pair
  // lands it is oldest, evictable, and evicted.
  let window = turns;
  while (window.length > 2
         && (window.length > MAX_TRANSCRIPT_TURNS
             || transcriptBytes(window) > MAX_TRANSCRIPT_BYTES)) {
    window = window.slice(2);
  }
  return Object.freeze(window);
}

// T104 F5-2: the WIRE window — what the next turn REQUEST may carry as its
// `transcript`, distinct from what the operator is shown. The request-side
// bounds are the server's own: 64,000 bytes, and MAX_TRANSCRIPT_TURNS = 20
// TURNS — i.e. 10 whole human/assistant pairs, which is what the loop below
// enforces (P3-5 fixed this comment: it used to say "MAX_TRANSCRIPT_TURNS
// pairs", twice the real bound; the code was always right). Eviction is
// oldest-first by whole pairs, and when even the newest pair alone exceeds
// the byte bound the honest answer is to send what fits — an EMPTY wire
// transcript — while the display above keeps the pair. Shipping OLDER pairs
// that would fit without the newest was considered and REJECTED: a wire
// transcript whose most recent context predates the question it accompanies
// misgrounds the turn, so contiguity-with-recency wins over salvage.
// Turn-cap semantics stay enforced on the display side (boundedAppend, as
// before); this window re-checks both bounds because a RESTORED transcript
// reaches the wire without passing through boundedAppend.
export function transcriptWireWindow(stateValue) {
  let window = stateValue.transcript;
  while (window.length > 0
         && (window.length > MAX_TRANSCRIPT_TURNS
             || transcriptBytes(window) > MAX_TRANSCRIPT_BYTES)) {
    window = window.slice(2);
  }
  return Object.freeze(window);
}

// The released `context_packet.reduced_reason` ceiling, restated here because
// this module cannot read the schema — the same discipline
// `serve.CONTEXT_REDUCED_REASON_MAX_LENGTH` gets, and a test pins BOTH to the
// released `maxLength` so the three cannot drift into three ceilings. CODE
// POINTS, matching what JSON Schema counts and what the server enforces.
export const CONTEXT_REDUCED_REASON_MAX_LENGTH = 500;

// Did the answer a stored posture BELONGS TO survive the restore? The posture
// describes the transcript's last assistant answer, and `restoreChatState`
// drops malformed rows WHOLE — so the question is about the SNAPSHOT's own
// terminal row, not about whatever the filter happened to leave at the tail.
// Same well-formedness test the transcript filter uses, so the two cannot
// disagree about what "survived" means.
function storedTerminalAnswerSurvived(snapshotValue) {
  const rows = snapshotValue && Array.isArray(snapshotValue.transcript)
    ? snapshotValue.transcript : [];
  const last = rows.length ? rows[rows.length - 1] : null;
  return Boolean(last) && last.role === "assistant"
    && typeof last.content === "string";
}

// THE RELEASED `context_packet` OBJECT, adopted from a success record
// (contract-v1.40, task 10.7). Total by refusal, in the shape every other
// adopter in this module uses: anything that is not the released two-field
// statement becomes null, and null renders nothing.
//
// FAIL-CLOSED ON A CONTRADICTION, not fail-open. The released schema refuses a
// `reduced` with no reason and a `full` WITH one, so a payload carrying either
// did not come from a conformant producer — and the wrong answer would be to
// keep the half of it that looked usable. `reduced` with no readable reason is
// exactly the "silent degradation" the requirement exists to prevent, and
// showing the bare words "reduced context" with no reason would be that
// degradation wearing a badge. Both drop to null.
function adoptContextPacket(carrier) {
  // ONE validator for BOTH readers, because they carry the SAME object: a
  // success record's `context_packet` and the persisted snapshot's. Naming the
  // stored field `context_packet` (and not a camelCase sibling) is deliberate —
  // the released object shape travels whole, so no third spelling of the
  // posture exists, and a malformed stored blob fails closed on the same
  // PAIRING rule a malformed wire record does.
  //
  // "THE SAME RULE" IS NOT "THE SAME VERDICT", and the difference is worth
  // naming (adversarial review). This adopter NORMALIZES: it reads the two
  // fields it knows and returns a fresh two-key object, so an extra key on a
  // stored blob is silently dropped and the posture still adopts. The released
  // shape is CLOSED and REFUSES that instance outright. Both are right for
  // where they sit — a wire contract must refuse what it did not admit, and a
  // browser-local blob that gained a key from a future build should still
  // render the posture it does carry rather than going blank — but they are
  // different verdicts, and only the pairing and the posture vocabulary are
  // enforced identically on both sides.
  const raw = carrier && carrier.context_packet;
  if (!raw || typeof raw !== "object") return null;
  const posture = raw.posture;
  const reason = raw.reduced_reason;
  // TWO DIFFERENT QUESTIONS, because the released shape asks two (Copilot
  // review of PR #256, finding 2).
  //
  // `full` refuses the field for BEING THERE — `not: {required:
  // [reduced_reason]}` is about the KEY, so presence is own-key presence and a
  // value of `""` or `null` is still a key that is present. This read
  // `hasReason` for both arms, so `{posture: "full", reduced_reason: ""}`
  // adopted as a clean full posture though the shape refuses that instance
  // outright.
  //
  // `reduced` refuses the field for being UNUSABLE — the shape requires it AND
  // bounds it at `minLength: 1`, so a blank or null reason is refused there for
  // a different reason and by a different test. Do not collapse these.
  const reasonPresent = Object.prototype.hasOwnProperty.call(
    raw, "reduced_reason");
  // …AND WITHIN THE RELEASED CEILING (Codex review of PR #256). "Usable" used
  // to mean "a non-empty string", so a malformed transport's oversized reason
  // — the dispatcher validates only `ok` and `kind` — reached browser state,
  // the live region, and from there the persisted snapshot. The server refuses
  // an over-ceiling reason pre-dispatch; this is the same rule on the reading
  // side, for the payloads the server did not author.
  // COUNTED IN CODE POINTS, because that is what `maxLength` counts (Codex
  // review of PR #256). `String.length` is UTF-16 code UNITS: a conformant
  // 300-emoji reason has 300 code points and a `.length` of 600, so the first
  // version of this ceiling DISCARDED a record the released contract accepts
  // and hid the very disclosure the release exists to show. `[...reason]`
  // iterates code points. Exactly the mistake this release argued against on
  // the server side — where a byte-counting guard would have refused a
  // conformant 1,500-byte CJK reason — arriving on the browser side in the
  // other unit.
  const reasonUsable = typeof reason === "string" && reason !== ""
    && [...reason].length <= CONTEXT_REDUCED_REASON_MAX_LENGTH;
  if (posture === "full") {
    return reasonPresent ? null : Object.freeze({ posture: "full" });
  }
  if (posture === "reduced" && reasonUsable) {
    return Object.freeze({ posture: "reduced", reduced_reason: reason });
  }
  return null;
}

export function settleTurnSuccess(stateValue, successPayload) {
  if (stateValue.phase !== "in_flight") {
    return stateValue;
  }
  return next(stateValue, {
    phase: "idle",
    // PR #63 review (Codex P1): settlement clears the composer ONLY when it
    // still holds the submitted message — follow-up typing during a slow
    // turn survives verbatim.
    composer: stateValue.composer === stateValue.pendingMessage
      ? "" : stateValue.composer,
    pendingMessage: null,
    lastFailure: null,
    proposals: adoptProposals(successPayload),
    // THE RELEASED POSTURE, ADOPTED (contract-v1.40, task 10.7). Read from the
    // record and never re-derived here: the server assembled the packet, so the
    // browser has no second way to know. A record from a producer older than
    // v1.40 carries no `context_packet` at all, which adopts as null — silence,
    // not a claim that the context was full.
    contextPacket: adoptContextPacket(successPayload),
    transcript: boundedAppend(
      stateValue.transcript,
      stateValue.pendingMessage === null ? "" : stateValue.pendingMessage,
      successPayload.assistant_prose),
  });
}

export function settleTurnFailure(stateValue, failurePayload) {
  // FR-016: the composer is preserved VERBATIM; only the two fixed released
  // fields are retained (never request or provider content).
  if (stateValue.phase !== "in_flight") {
    return stateValue;
  }
  return next(stateValue, {
    phase: "idle",
    pendingMessage: null,
    lastFailure: Object.freeze({
      error: String(failurePayload && failurePayload.error),
      message: String(failurePayload && failurePayload.message),
    }),
  });
}

// T104 F5-5: a LOCAL fixed failure, for refusals that happen at idle.
// `settleTurnFailure` is phase-gated to in_flight because it settles a
// FLIGHT; a refused proposal Apply happens with no turn in the air, yet its
// refusal must reach the same visible channel (lastFailure → the rendered
// failure note and the live region) instead of returning the identical
// state — zero visible change was the finding. Only the two fixed fields
// are retained, same discipline as settleTurnFailure: never request,
// response, or buffer content.
export function recordLocalFailure(stateValue, failurePayload) {
  return next(stateValue, {
    lastFailure: Object.freeze({
      error: String(failurePayload && failurePayload.error),
      message: String(failurePayload && failurePayload.message),
    }),
  });
}

export function transcriptWindow(stateValue) {
  return stateValue.transcript;
}

// add-doxbench-editing-phase-b task 7.2: SELECTING A DOCUMENT SWITCHES THE
// TRANSCRIPT TO THAT DOCUMENT'S THREAD.
//
// The thread is the SERVER's record — one sidecar per document, on the session
// branch — so this function does not invent one: it adopts the turns the thread
// route answered with, and adopts an EMPTY transcript where that document has
// no thread yet. An empty transcript is the honest answer for a document nobody
// has talked about, and leaving the previous document's conversation on screen
// was the real defect: the next turn's wire transcript would then carry ANOTHER
// document's conversation as this one's context.
//
// NO SECOND STATE AUTHORITY. This replaces `transcript` and nothing else
// decides what it holds; the same display bounds apply, through the same
// `boundedAppend`-shaped eviction the wire window re-checks. `proposals` and
// `lastFailure` are cleared because both are facts about the PREVIOUS
// document's turn, and a proposal targeting a buffer the human is no longer
// looking at is exactly the stale Apply control the currency rules exist to
// prevent.
export function adoptThreadTranscript(stateValue, turnsValue) {
  // A TURN IN FLIGHT BELONGS TO THE DOCUMENT IT WAS SENT FOR (adversarial
  // review P2-9). Switching while `phase === "in_flight"` used to swap the
  // transcript under the running turn, and `settleTurnSuccess` then appended
  // document A's question and answer onto document B's transcript — which is
  // also B's WIRE transcript, so A's conversation became B's context on B's
  // next turn, and A's proposal was restored under B with a live Apply
  // control. Reproduced from the UI with no server race.
  //
  // REFUSED, by returning the identical state object — the same "no" every
  // other refusal in this module gives (`beginTurn` on a second begin,
  // `rekeyChatState` on an unchanged key). The rail's caller renders the
  // selector back to the buffer the conversation is still bound to, so the
  // selection and the transcript cannot disagree.
  if (stateValue.phase === "in_flight") {
    return stateValue;
  }
  const rows = Array.isArray(turnsValue) ? turnsValue : [];
  let transcript = Object.freeze(rows.flatMap((turn) => {
    if (!turn || typeof turn !== "object") return [];
    return [
      Object.freeze({ role: "human", content: String(turn.human || "") }),
      Object.freeze({ role: "assistant", content: String(turn.assistant || "") }),
    ];
  }));
  // A thread can be longer than the DISPLAY bounds: it is a durable record and
  // they are a window. Evict oldest whole pairs, exactly as an appended turn
  // would be evicted, so a restored thread and a lived-through conversation
  // render under one rule.
  while (transcript.length > 2
         && (transcript.length > MAX_TRANSCRIPT_TURNS
             || transcriptBytes(transcript) > MAX_TRANSCRIPT_BYTES)) {
    transcript = Object.freeze(transcript.slice(2));
  }
  return next(stateValue, {
    transcript,
    proposals: NO_PROPOSALS,
    lastFailure: null,
    // …and the posture goes with them, for the same reason: it is a fact about
    // the PREVIOUS document's last answer, and the restored thread carries no
    // posture of its own (the server's sidecar does not record one). Leaving it
    // would caption this document's conversation with another's context.
    contextPacket: null,
  });
}

export function rekeyChatState(stateValue, keyValue, subjectDefaultValue) {
  // FR-011/R12 browser-session isolation: a different scope key gets a
  // FRESH state (no transcript, composer, selection, or failure carryover);
  // the same key keeps the state untouched.
  //
  // A fresh conversation is a fresh conversation, so it is SEEDED like a mount:
  // the default is threaded through rather than dropped, which is why a Save
  // moving this tile onto its session ref comes back with the tile's subject
  // instead of an empty box.
  if (sameKey(stateValue.key, keyValue)) {
    return stateValue;
  }
  return createChatState(keyValue, subjectDefaultValue);
}

// ---------------------------------------------------------------------------
// T062 (US3): TypedProposal review state — per-target INDEPENDENT
// current/stale/rejected/applied transitions (FR-026..FR-029). Staleness is
// derived by EXACT hash comparison against the CURRENT buffer identity and
// recomputed on every buffer edit event (`refreshProposalCurrency`);
// `applied` and `rejected` are TERMINAL. The ONLY recovery from stale is a
// new turn (the next success REPLACES the whole set): no merge and no
// force-apply exist here, and test_doxbench_proposals.py pins the absence.
// The actual buffer mutation lives in doxbench-state.js (T064) — this model
// only tracks review status, so acting on one target can never disturb the
// other's record or any buffer.
// ---------------------------------------------------------------------------

export const PROPOSAL_STATUSES = Object.freeze([
  "current", "stale", "rejected", "applied"]);

// THE TARGET SET IS THE RECORD'S OWN (contract-v1.34, add-doxbench-editing-phase-b
// §13). It used to be a module constant of two names, because the v1 wire declared
// `typed_proposal.target` as a two-value enum and no other target could reach this
// module. The widened family releases a BUFFER-KEY target, so the closed set is
// the one the turn itself states: `observed_hashes` is keyed by buffer and holds
// exactly the buffers the request supplied and the model was therefore shown.
//
// Reading it from the RECORD rather than from a constant is the same rule the
// server derives its own permitted set by, and it makes "a target the request did
// not supply" and "a target whose shown identity we do not hold" one question. A
// target outside it is DROPPED rather than recorded, which is the delta's own rule
// ("refused as unroutable and MUST NOT be rendered with an Apply control"). Both
// families answer it: a v1 record carries the same object under the two reserved
// keys.
function permittedTargetsOf(successPayload) {
  const observed = successPayload && successPayload.observed_hashes;
  if (!observed || typeof observed !== "object") return [];
  return Object.keys(observed);
}

// The DECLARED order proposals are read and rendered in: the reserved outline
// first -- it is the buffer every turn carries -- then the documents in the rule
// every home spells identically:
//   ascending lexicographic by buffer key (UTF-16 code unit)
// Same order the selector and the save plan use, and the same rule STRING, which
// is what a companion test pins across the homes. A card list whose order
// depended on object insertion would reshuffle under the cursor.
export function orderedProposalTargets(records) {
  const keys = Object.keys(records || {}).filter((key) => records[key]);
  const documents = keys.filter((key) => key !== "outline").sort(
    (left, right) => (left < right ? -1 : left > right ? 1 : 0));
  return keys.includes("outline") ? ["outline", ...documents] : documents;
}

const NO_PROPOSALS = Object.freeze({});

function proposalRecord(raw, statusValue) {
  return Object.freeze({
    target: String(raw.target),
    base_hash: String(raw.base_hash),
    summary: String(raw.summary),
    content: String(raw.content),
    status: statusValue,
  });
}

function adoptProposals(successPayload) {
  const permitted = permittedTargetsOf(successPayload);
  const records = {};
  for (const raw of (successPayload && successPayload.proposals) || []) {
    if (raw && permitted.includes(raw.target)) {
      records[raw.target] = proposalRecord(raw, "current");
    }
  }
  return Object.freeze(records);
}

export function proposalsOf(stateValue) {
  return stateValue.proposals || NO_PROPOSALS;
}

export function refreshProposalCurrency(stateValue, currentHashes) {
  const before = proposalsOf(stateValue);
  const records = { ...before };
  let changed = false;
  for (const target of Object.keys(records)) {
    const record = records[target];
    if (!record) continue;
    if (record.status === "applied" || record.status === "rejected") continue;
    const status = record.base_hash === String(currentHashes[target])
      ? "current" : "stale";
    if (status !== record.status) {
      records[target] = Object.freeze({ ...record, status });
      changed = true;
    }
  }
  if (!changed) return stateValue;
  return next(stateValue, { proposals: Object.freeze(records) });
}

function transitionProposal(stateValue, targetValue, fromStatuses, toStatus) {
  const before = proposalsOf(stateValue);
  const record = before[targetValue];
  if (!record || !fromStatuses.includes(record.status)) {
    return stateValue;  // absent, terminal, or stale-for-apply: refused
  }
  const records = { ...before,
    [targetValue]: Object.freeze({ ...record, status: toStatus }) };
  return next(stateValue, { proposals: Object.freeze(records) });
}

export function rejectProposal(stateValue, targetValue) {
  return transitionProposal(stateValue, targetValue,
                            ["current", "stale"], "rejected");
}

export function markProposalApplied(stateValue, targetValue) {
  // ONLY a current proposal may be applied — stale refuses with the
  // identical state; recovery is a new turn, never an override.
  return transitionProposal(stateValue, targetValue, ["current"], "applied");
}

export function clearLocalFailure(stateValue) {
  // W-11 (wave re-review): a landed apply is a SUCCESS event for the local
  // failure channel, exactly as a settled turn is — leaving the refusal note
  // standing put two live regions in contradiction ("Proposal applied…"
  // beside "this proposal no longer matches the buffer"). Pure and narrow:
  // only the local lastFailure clears; nothing else moves.
  if (!stateValue.lastFailure) return stateValue;
  return { ...stateValue, lastFailure: null };
}

export function markProposalAppliedAfterSwap(stateValue, targetValue) {
  // W-3 (wave re-review): the ONE widening the apply-SETTLE path needs
  // beyond the current-only rule above. The swap's own edit re-scores the
  // clicked record to `stale` before the seam's promise resolves
  // (self-induced staleness — the buffer moved because the apply moved it),
  // and the mark now runs against the LIVE state after that re-score. The
  // caller proves the live record is field-identical to the record the seam
  // actually swapped, so "applied" stays truthful; every other stale record
  // still refuses through `markProposalApplied`'s current-only rule.
  return transitionProposal(stateValue, targetValue, ["current", "stale"],
                            "applied");
}

// ---------------------------------------------------------------------------
// R-1 (2026-08-02): the PURE persistable snapshot of chat working state and
// its restore. This module still touches NO storage primitive — the shell
// writes the blob beside the buffers (one atomic record) and hands it back
// here. `restoreChatState` deliberately does NOT trust stored proposal
// statuses: it re-derives them from the RESTORED buffer hashes via
// refreshProposalCurrency, so a proposal whose base moved while the tile was
// closed can only come back STALE, never `current`. That is the correctness
// rule the operator named: restoring buffers without re-scoring proposals
// would resurrect cards whose bases no longer match the text.
// ---------------------------------------------------------------------------

export const CHAT_SNAPSHOT_VERSION = 1;
export const CHAT_SNAPSHOT_KIND = "doxbench-chat-working-state";

export function chatSnapshot(stateValue) {
  const records = proposalsOf(stateValue);
  return {
    schema_version: CHAT_SNAPSHOT_VERSION,
    kind: CHAT_SNAPSHOT_KIND,
    // WHAT THE RESTORED ANSWER RAN ON (contract-v1.40; adversarial review
    // NEW-2). The transcript survives a tile being closed and reopened, so its
    // disclosure has to survive with it — a restored reduced answer with no
    // note is the same lost-badge defect S4 found on the failure path, one
    // lifecycle up. Omitted entirely when there is nothing to say, so a
    // conversation with no posture writes the same blob it always did.
    //
    // NO VERSION BUMP, and that is a judgement call with a cost on the other
    // side. `restoreChatState` fail-closes on an unrecognized `schema_version`
    // and keeps the FRESH state, so bumping would discard every snapshot in
    // existence on the first reopen after the upgrade — the operator's
    // composer text, subject, model choice and proposals, to add a caption.
    // An OPTIONAL field invalidates nothing instead: an old blob lacks the key
    // and restores to posture-unknown, which renders no note and is exactly
    // today's behaviour; a NEW blob read by an OLDER build is ignored, because
    // this restore reads named fields and never enumerates. Both directions
    // safe, nothing discarded — the same additive reasoning the released wire
    // contracts use when they grow without moving `contract_schema_version`.
    ...(stateValue.contextPacket
      ? { context_packet: stateValue.contextPacket } : {}),
    workingSubject: stateValue.workingSubject,
    selectedModelId: stateValue.selectedModelId,
    composer: stateValue.composer,
    transcript: transcriptWindow(stateValue).map(
      (turn) => ({ role: turn.role, content: turn.content })),
    proposals: orderedProposalTargets(records).map((target) => records[target])
      .filter(Boolean)
      .map((record) => ({
        target: record.target, base_hash: record.base_hash,
        summary: record.summary, content: record.content,
        status: record.status,
      })),
  };
}

export function restoreChatState(stateValue, snapshotValue, currentHashes) {
  if (!snapshotValue || typeof snapshotValue !== "object"
      || snapshotValue.schema_version !== CHAT_SNAPSHOT_VERSION
      || snapshotValue.kind !== CHAT_SNAPSHOT_KIND) {
    return stateValue;   // unknown shape: keep the fresh state, fail closed
  }
  const records = {};
  for (const raw of Array.isArray(snapshotValue.proposals)
      ? snapshotValue.proposals : []) {
    // Any buffer KEY may have been a target (contract-v1.34); a restored record
    // whose buffer is no longer loaded re-scores to `stale` below, because
    // `refreshProposalCurrency` holds no current hash for it. Fail-closed by the
    // same rule that scores every other restored proposal, not by a second one.
    if (!raw || typeof raw.target !== "string" || !raw.target) continue;
    // TERMINAL statuses survive verbatim (an applied proposal stays applied);
    // everything else is re-scored below against the restored bytes.
    const status = (raw.status === "applied" || raw.status === "rejected")
      ? raw.status : "current";
    records[raw.target] = proposalRecord(raw, status);
  }
  // P3-6(a)/(b): only WELL-FORMED turns survive a restore — a released role
  // AND a real string content. `String(t.content)` used to FABRICATE the
  // literal string "undefined" for a turn whose content was missing or
  // non-string: invented transcript bytes rendered as if the operator's own
  // conversation contained them. Such turns are dropped whole, like the
  // foreign-role turns beside them. Beyond well-formedness, PAIR ALIGNMENT
  // is the snapshot author's problem: a dropped turn can leave human and
  // assistant turns unpaired, and this restore deliberately does not
  // re-pair — the display and the wire window both operate on turns, and
  // reconstructing pairs from a corrupted snapshot would be fabrication of
  // a different kind.
  const transcript = Object.freeze(
    (Array.isArray(snapshotValue.transcript) ? snapshotValue.transcript : [])
      .filter((t) => t && (t.role === "human" || t.role === "assistant")
        && typeof t.content === "string")
      .map((t) => Object.freeze({ role: t.role, content: t.content })));
  const restored = next(stateValue, {
    // P3-6(c): a persisted field is adopted only if it still fits its own
    // byte bound — the same exact-UTF-8 rule editSubject/editComposer
    // enforce live. Refused-never-truncated: an over-bound (or non-string)
    // restored field is dropped WHOLE, to the empty string, never trimmed
    // to fit; otherwise a hand-edited or future-versioned snapshot could
    // seed the state with text the bounds refuse to ever send.
    //
    // AN EMPTY STORED SUBJECT STANDS — it is NOT re-seeded from the tile
    // default `createChatState` just applied. The snapshot spells the subject
    // as a plain string with no absent/null marker, so the stored form cannot
    // tell an emptied box apart from one nothing was ever put into, by the
    // field alone; of the two readings the human's is the one worth being
    // wrong about, because putting the title back over an emptied box
    // overrules a person, while leaving an unfilled box empty costs one
    // keystroke. (Going forward the ambiguity barely exists: a fresh state is
    // seeded, so an empty stored subject can only come of a human emptying it
    // or of a tile whose title seeds nothing — where re-seeding would land on
    // the same empty box anyway. The one real gap is a record written by a
    // build predating the seeding, and the shell's per-tab session store
    // cannot carry one past the browser session it was written in.) An
    // over-bound stored subject lands on the same empty box rather than on the
    // default, by the rule above: a stored record answers for this
    // conversation, corrupt field included.
    workingSubject: typeof snapshotValue.workingSubject === "string"
      && utf8Size(snapshotValue.workingSubject) <= MAX_WORKING_SUBJECT_BYTES
      ? snapshotValue.workingSubject : "",
    // T104 F5-7: a persisted id is a claim about a catalog that may have
    // changed while the tile was closed, so it is adopted ONLY if the
    // restored state's catalog vouches for it (selectModel's own rule; the
    // old bare typeof check bypassed it and armed Send behind a placeholder
    // selector). With NO catalog adopted yet (models === null) the id is
    // KEPT — R-1 continuity: restore usually runs before the plane's
    // catalog fetch settles, and nulling here would cost the operator their
    // choice on every reopen — while `canSend` refuses to arm until a
    // catalog vouches, and `adoptCatalog` re-validates the held id the
    // moment one arrives. Either way the placeholder and the disabled Send
    // agree.
    selectedModelId: typeof snapshotValue.selectedModelId !== "string"
      ? null
      : (stateValue.models === null
        || catalogVouchesFor(stateValue.models, snapshotValue.selectedModelId)
        ? snapshotValue.selectedModelId : null),
    composer: typeof snapshotValue.composer === "string"
      && utf8Size(snapshotValue.composer) <= MAX_MESSAGE_BYTES
      ? snapshotValue.composer : "",
    transcript,
    proposals: Object.freeze(records),
    // THE FOURTH ANSWER-REPLACING PATH (adversarial review NEW-1). This
    // replaces the transcript WHOLESALE, so it replaces the answer the note
    // describes — and it used to leave `contextPacket` untouched, which the
    // reviewer reproduced: a restored answer captioned by a note that never
    // described it. Reachability was nil (the sole caller restores onto a
    // freshly mounted rail, where it is already null) and the SENTENCE was
    // false, which is what mattered: three places claimed the enumeration was
    // complete at three paths.
    //
    // It adopts the SNAPSHOT's posture rather than nulling, which is NEW-2's
    // half: a blob that carries one restores the disclosure with the answer, a
    // blob that does not restores to silence. Both go through the same
    // `adoptContextPacket` a wire record does, so a hand-edited or
    // future-versioned blob claiming `reduced` with no readable reason fails
    // closed to null instead of captioning the transcript with a reduction
    // nobody can check.
    //
    // …AND ONLY IF THE ANSWER IT DESCRIBES SURVIVED THE RESTORE (Codex review
    // of PR #256). The posture describes THE TRANSCRIPT'S LAST ASSISTANT
    // ANSWER, and this restore drops malformed turns WHOLE (P3-6(a)/(b) above),
    // so the answer the stored posture belonged to may simply not be here.
    // Three reproduced cases: an empty transcript with a valid packet rendered
    // a reduction note for no answer at all; a blob whose assistant turn was
    // filtered did the same; and dropping only the NEWEST assistant turn
    // captioned the OLDER answer with the newer one's posture — the
    // wrong-answer caption this invariant exists to prevent, arriving by a
    // third route after S4 and NEW-1.
    //
    // The test is THE SNAPSHOT'S OWN TERMINAL TURN, not the filtered tail —
    // corrected after Codex broke the first version of this guard on exactly
    // the case its shape could not see. Checking only the filtered transcript
    // cannot tell the original terminal answer from an EARLIER retained one:
    // `[human, assistant "older", assistant(malformed)]` filters down to a tail
    // that IS an assistant turn, so the guard passed and captioned the older
    // answer with the newer answer's posture — the very defect it was added to
    // prevent, one layer in.
    //
    // So adoption asks whether the answer the posture BELONGS TO survived: the
    // snapshot's own last transcript row must be a well-formed assistant turn.
    // If it was dropped, or if the conversation ended on a human turn (a tile
    // closed mid-question), there is no answer on screen for the posture to
    // describe and it goes.
    contextPacket: storedTerminalAnswerSurvived(snapshotValue)
      ? adoptContextPacket(snapshotValue) : null,
  });
  // The re-score is the whole point of restoring these together.
  return currentHashes ? refreshProposalCurrency(restored, currentHashes)
    : restored;
}
