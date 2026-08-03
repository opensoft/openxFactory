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
    selectedModelId: null,
    workingSubject: "",
    composer: "",
    phase: "idle",
    pendingMessage: null,    // the composer content captured at beginTurn
    transcript: Object.freeze([]),
    lastFailure: null,
    proposals: Object.freeze({ outline: null, document: null }),
  });
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
  return next(stateValue, { models });
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
  return typeof stateValue.selectedModelId === "string"
    && stateValue.selectedModelId !== "";
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

function boundedAppend(transcriptValue, humanContent, assistantContent) {
  const turns = transcriptValue.concat([
    Object.freeze({ role: "human", content: String(humanContent) }),
    Object.freeze({ role: "assistant", content: String(assistantContent) }),
  ]);
  // Evict oldest WHOLE human/assistant pairs until both released bounds
  // hold — never split a pair, never truncate a turn's content.
  const bytesOf = (list) => list.reduce(
    (n, turn) => n + utf8Size(turn.content), 0);
  let window = turns;
  while (window.length > MAX_TRANSCRIPT_TURNS
         || bytesOf(window) > MAX_TRANSCRIPT_BYTES) {
    window = window.slice(2);
    if (window.length === 0) { break; }
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
    proposals: adoptProposals(successPayload.proposals),
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
const PROPOSAL_TARGETS = Object.freeze(["outline", "document"]);
const NO_PROPOSALS = Object.freeze({ outline: null, document: null });

function proposalRecord(raw, statusValue) {
  return Object.freeze({
    target: String(raw.target),
    base_hash: String(raw.base_hash),
    summary: String(raw.summary),
    content: String(raw.content),
    status: statusValue,
  });
}

function adoptProposals(payloadProposals) {
  const records = { outline: null, document: null };
  for (const raw of payloadProposals || []) {
    if (PROPOSAL_TARGETS.includes(raw && raw.target)) {
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
  const records = { outline: before.outline, document: before.document };
  let changed = false;
  for (const target of PROPOSAL_TARGETS) {
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
    proposals: PROPOSAL_TARGETS.map((target) => records[target])
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
  const records = { outline: null, document: null };
  for (const raw of Array.isArray(snapshotValue.proposals)
      ? snapshotValue.proposals : []) {
    if (!PROPOSAL_TARGETS.includes(raw && raw.target)) continue;
    // TERMINAL statuses survive verbatim (an applied proposal stays applied);
    // everything else is re-scored below against the restored bytes.
    const status = (raw.status === "applied" || raw.status === "rejected")
      ? raw.status : "current";
    records[raw.target] = proposalRecord(raw, status);
  }
  const transcript = Object.freeze(
    (Array.isArray(snapshotValue.transcript) ? snapshotValue.transcript : [])
      .filter((t) => t && (t.role === "human" || t.role === "assistant"))
      .map((t) => Object.freeze({ role: t.role, content: String(t.content) })));
  const restored = next(stateValue, {
    workingSubject: typeof snapshotValue.workingSubject === "string"
      ? snapshotValue.workingSubject : stateValue.workingSubject,
    selectedModelId: typeof snapshotValue.selectedModelId === "string"
      ? snapshotValue.selectedModelId : null,
    composer: typeof snapshotValue.composer === "string"
      ? snapshotValue.composer : "",
    transcript,
    proposals: Object.freeze(records),
  });
  // The re-score is the whole point of restoring these together.
  return currentHashes ? refreshProposalCurrency(restored, currentHashes)
    : restored;
}

// ---- the prompt panel's model families and effort levels ---------------------
//
// WHY EFFORT IS A MODEL_ID AND NOT A FIELD. The released chat-turn request
// envelope is CLOSED and its properties are fixed; there is no effort field,
// and the catalog entry is closed too. So an effort level cannot travel as its
// own value without changing the released contract. `model_id` is the one
// channel whose MEANING the catalog owns, so an effort level is advertised as
// a separate entry: `<family>:<effort>`.
//
// That turns out to be the stronger arrangement rather than a workaround. A
// slider over catalog entries can only ever offer a configuration the plane
// already published as approved AND available — withdraw an entry and the
// position disappears. An effort field would have been a free parameter the
// console asserted; this is a choice among things the plane advertised.
//
// The grouping below is a DISPLAY convention and nothing more. Two rules keep
// it honest, and both are pinned by tests: the console only ever sends an id it
// was handed (it never composes one), and when the catalog advertises no
// variants no slider is rendered at all.

// The runtime's own set, read off the CLI's refusal message ("Valid values:
// low, medium, high, xhigh, max"). Ordered weakest to strongest, because a
// slider's positions have to ascend and a catalog is a set, not a sequence.
export const EFFORT_LEVELS = Object.freeze(
  ["low", "medium", "high", "xhigh", "max"]);

// The separator is a DOT, and that is the released schema's choice, not a
// preference: `model_id` is constrained to `^[A-Za-z0-9][A-Za-z0-9._-]*$`, so a
// colon is illegal and the catalog route refuses an envelope carrying one. Of
// the three legal punctuation marks, `-` already appears inside every family id
// and `_` in none of them, so `.` is the one that reads as a separator.
//
// A dot is SAFE here only because of the membership guard below: a provider id
// like `claude-haiku-4.5` has the suffix `5`, which is not an effort level, so
// it stays one whole family exactly as it should.
const EFFORT_SEPARATOR = ".";

function splitModelId(modelIdValue) {
  const id = typeof modelIdValue === "string" ? modelIdValue : "";
  const cut = id.lastIndexOf(EFFORT_SEPARATOR);
  if (cut <= 0) return { familyId: id, effort: null };
  const suffix = id.slice(cut + 1);
  // ONLY a real level counts. A provider is free to put dots in its own
  // identifiers, and reading `claude-haiku-4.5` as an effort would invent a
  // family the catalog never advertised.
  if (!EFFORT_LEVELS.includes(suffix)) return { familyId: id, effort: null };
  return { familyId: id.slice(0, cut), effort: suffix };
}

// The effort a model id names, or null when it names none.
export function effortOfModelId(modelIdValue) {
  return splitModelId(modelIdValue).effort;
}

// The family a model id belongs to — itself, when it carries no effort.
export function familyOfModelId(modelIdValue) {
  return splitModelId(modelIdValue).familyId;
}

// The catalog's AVAILABLE entries, collapsed into families in catalog order.
// Each family carries its advertised efforts (ascending) and, when it has one,
// the plain no-effort entry.
export function modelFamilies(modelsValue) {
  const order = [];
  const byId = new Map();
  for (const entry of modelsValue || []) {
    // `available: false` is the plane WITHDRAWING a configuration; it must not
    // become a menu row or a slider position.
    if (!entry || entry.available !== true) continue;
    const { familyId, effort } = splitModelId(entry.model_id);
    if (!familyId) continue;
    let family = byId.get(familyId);
    if (!family) {
      family = { familyId, label: "", handling: "", variants: [], plainId: null };
      byId.set(familyId, family);
      order.push(family);
    }
    // Variants of one family share a label and handling text by convention —
    // the effort lives in the id, not the prose. First one wins if they differ.
    if (!family.label) family.label = String(entry.label || familyId);
    if (!family.handling && entry.data_handling) {
      family.handling = String(entry.data_handling);
    }
    if (effort === null) family.plainId = entry.model_id;
    else family.variants.push({ effort, modelId: entry.model_id });
  }
  return order.map((family) => Object.freeze({
    familyId: family.familyId,
    label: family.label,
    handling: family.handling,
    plainId: family.plainId,
    efforts: Object.freeze(EFFORT_LEVELS.filter(
      (level) => family.variants.some((v) => v.effort === level))),
    variants: Object.freeze(family.variants.map(Object.freeze)),
  }));
}

// The ADVERTISED id for one effort of a family, or null when the catalog does
// not offer it. Returning the entry's own id — never a composed string — is
// what keeps the slider inside what the plane approved.
export function modelIdForEffort(familyValue, effortValue) {
  if (!familyValue || !familyValue.variants) return null;
  const hit = familyValue.variants.find((v) => v.effort === effortValue);
  return hit ? hit.modelId : null;
}

// The family a state's selection belongs to, or null.
export function selectedFamily(stateValue, familiesValue) {
  const wanted = familyOfModelId(stateValue && stateValue.selectedModelId);
  if (!wanted) return null;
  return (familiesValue || []).find((f) => f.familyId === wanted) || null;
}

// Switching family keeps the effort the human already chose when the new
// family advertises it; otherwise it lands on that family's strongest offer
// below the current one, and failing that its plain entry. Never null when the
// family has anything selectable at all.
export function modelIdOnFamilyChange(familyValue, currentEffortValue) {
  if (!familyValue) return null;
  const efforts = familyValue.efforts || [];
  if (!efforts.length) return familyValue.plainId;
  if (efforts.includes(currentEffortValue)) {
    return modelIdForEffort(familyValue, currentEffortValue);
  }
  const wantedRank = EFFORT_LEVELS.indexOf(currentEffortValue);
  if (wantedRank < 0) return modelIdForEffort(familyValue, efforts[0]);
  let best = efforts[0];
  for (const level of efforts) {
    if (EFFORT_LEVELS.indexOf(level) <= wantedRank) best = level;
  }
  return modelIdForEffort(familyValue, best);
}
