// doxbench-chat-model.js — T052 (US2): PURE browser-session chat state for
// doxBench. Import-free like doxbench-state.js, by the same rule: the Node
// test harness imports this file alone, and purity is the enforced boundary
// (no fetch, no DOM, no storage, no timers — the transports live in app.js
// and the view in doxbench-chat.js).
//
// Every function returns NEW frozen values and never mutates its input.
// Bounds measure exact UTF-8 BYTES (never code points), mirroring
// doxbench-state.js's utf8Size and the feature's content-identity rule.
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

export function createChatState(keyValue) {
  return Object.freeze({
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
  });
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

export function rekeyChatState(stateValue, keyValue) {
  // FR-011/R12 browser-session isolation: a different scope key gets a
  // FRESH state (no transcript, composer, selection, or failure carryover);
  // the same key keeps the state untouched.
  if (sameKey(stateValue.key, keyValue)) {
    return stateValue;
  }
  return createChatState(keyValue);
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
  });
  // The re-score is the whole point of restoring these together.
  return currentHashes ? refreshProposalCurrency(restored, currentHashes)
    : restored;
}
