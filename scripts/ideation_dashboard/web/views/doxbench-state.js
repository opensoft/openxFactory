// Pure doxBench working-state primitives.
//
// This module stays import-free so the existing Node harness can execute the
// exact browser code. Content hashing is intentionally asynchronous because
// Web Crypto is the browser authority; callers that attach results to mutable
// buffers must pair the promise with their own generation token.

export const DOXBENCH_MAX_BUFFER_BYTES = 400_000;
export const CONTENT_IDENTITY_ALGORITHM = "sha256";

// THE KIND VOCABULARY, and nothing more (add-doxbench-editing-phase-b, design
// D1). Until Phase B this constant doubled as the STATE'S KEY LIST -- the
// buffer set was exactly `{outline, document}` and every consumer enumerated it
// through this array. That second job is gone: the state is now a KEYED SET,
// `outline` plus one key per loaded document, and the keys are read from
// `state.buffers` itself. What survives here is the two-value KIND vocabulary a
// buffer declares about itself.
export const BUFFER_KINDS = Object.freeze(["outline", "document"]);

// The two RESERVED keys. `outline` is permanently reserved for the buffer whose
// commit establishes the session ancestry every document commit descends from.
// `document` is reserved for AT MOST ONE not-yet-created buffer -- the create
// flow's unbacked slot, which cannot be keyed by a path because it has none --
// and is freed again when its first Save reports the path it created.
export const OUTLINE_BUFFER_KEY = "outline";
export const UNBACKED_DOCUMENT_BUFFER_KEY = "document";

// The declared bound on the loaded set (design D6). Reaching it REFUSES the
// load with the measured bound stated; it never evicts, because every loaded
// buffer may hold unsaved human text and an eviction policy is a policy that
// discards it.
export const DOXBENCH_MAX_LOADED_DOCUMENTS = 24;

export const DOXBENCH_SESSION_STATE_VERSION = 1;
export const DOXBENCH_SESSION_STATE_KIND = "doxbench-working-state";

const SCOPE_KINDS = new Set(["cluster", "possible", "staged"]);
const LOAD_STATES = new Set([
  "empty", "loading", "ready", "unavailable", "error",
]);
const BUFFER_KIND_SET = new Set(BUFFER_KINDS);
const SESSION_KEY_PREFIX = "doxbench:v1:";

const encoder = new TextEncoder();

export class ContentSizeError extends RangeError {
  constructor(actualBytes, limitBytes) {
    super(`content is ${actualBytes} UTF-8 bytes; maximum is ${limitBytes}`);
    this.name = "ContentSizeError";
    this.actualBytes = actualBytes;
    this.limitBytes = limitBytes;
  }
}

export class ContentEncodingError extends TypeError {
  constructor() {
    super("content contains an unpaired UTF-16 surrogate");
    this.name = "ContentEncodingError";
  }
}

function rejectUnpairedSurrogates(content) {
  for (let index = 0; index < content.length; index += 1) {
    const unit = content.charCodeAt(index);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      const next = content.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) {
        throw new ContentEncodingError();
      }
      index += 1;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      throw new ContentEncodingError();
    }
  }
}

function exactUtf8(content) {
  if (typeof content !== "string") {
    throw new TypeError("content must be a string");
  }
  rejectUnpairedSurrogates(content);
  return encoder.encode(content);
}

function validatedLimit(maxBytes) {
  if (!Number.isSafeInteger(maxBytes)) {
    throw new TypeError("maxBytes must be a non-negative safe integer");
  }
  if (maxBytes < 0) {
    throw new RangeError("maxBytes must be non-negative");
  }
  return maxBytes;
}

function bytesWithinLimit(content, maxBytes) {
  const limit = validatedLimit(maxBytes);
  const bytes = exactUtf8(content);
  if (bytes.byteLength > limit) {
    throw new ContentSizeError(bytes.byteLength, limit);
  }
  return bytes;
}

export function utf8Size(content) {
  return exactUtf8(content).byteLength;
}

export async function sha256Hex(
  content,
  { maxBytes = DOXBENCH_MAX_BUFFER_BYTES } = {},
) {
  const bytes = bytesWithinLimit(content, maxBytes);
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (value) =>
    value.toString(16).padStart(2, "0")
  ).join("");
}

export async function contentIdentity(
  content,
  { maxBytes = DOXBENCH_MAX_BUFFER_BYTES } = {},
) {
  return {
    algorithm: CONTENT_IDENTITY_ALGORITHM,
    hex: await sha256Hex(content, { maxBytes }),
  };
}

function plainObject(value, name) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${name} must be an object`);
  }
  return value;
}

function nonEmptyString(value, name) {
  if (typeof value !== "string" || !value) {
    throw new TypeError(`${name} must be a non-empty string`);
  }
  return value;
}

function bufferKind(value) {
  if (!BUFFER_KIND_SET.has(value)) {
    throw new TypeError("buffer kind must be outline or document");
  }
  return value;
}

// ---------------------------------------------------------------------------
// BUFFER KEYS (design D1). The key of the outline buffer is the reserved word
// `outline`; the key of a document buffer is its own repository-relative PATH,
// so a document can be loaded at most once and no two buffers can claim the
// same file -- impossible by construction rather than by a lookup. A document
// with no path yet lives under the reserved `document` key until its first
// Save reports one.
// ---------------------------------------------------------------------------

function bufferKeyString(value, name) {
  return nonEmptyString(value, name);
}

// The key a buffer BELONGS under, derived from the buffer alone.
export function bufferKeyFor(bufferValue) {
  const buffer = plainObject(bufferValue, "buffer");
  if (buffer.kind === "outline") return OUTLINE_BUFFER_KEY;
  bufferKind(buffer.kind);
  return buffer.path === null || buffer.path === undefined
    ? UNBACKED_DOCUMENT_BUFFER_KEY
    : nonEmptyString(buffer.path, "buffer path");
}

// The declared DETERMINISTIC document order (design D3 point 4, and the
// selector's own listing order). Ascending lexicographic comparison of the
// buffer KEY by UTF-16 code unit -- `<` on the key string, with no locale, no
// collator, and no special case for the reserved `document` key, which orders
// as the literal string it is. "Any order" constrains the CONTRACT (documents
// impose no ordering rule on each other); it does not license a
// nondeterministic one, so the realization declares this one and pins it.
export const DOCUMENT_KEY_ORDER_RULE =
  "ascending lexicographic by buffer key (UTF-16 code unit)";

export function orderedDocumentKeys(bufferKeys) {
  const keys = Array.from(bufferKeys).filter(
    (key) => key !== OUTLINE_BUFFER_KEY,
  );
  keys.sort((left, right) => (left < right ? -1 : left > right ? 1 : 0));
  return Object.freeze(keys);
}

function normalizedScopeKey(value) {
  const key = plainObject(value, "scope key");
  const tileKind = nonEmptyString(key.tile_kind, "scope key tile_kind");
  if (!SCOPE_KINDS.has(tileKind)) {
    throw new TypeError("scope key tile_kind must be cluster, possible, or staged");
  }
  return Object.freeze({
    repository: nonEmptyString(key.repository, "scope key repository"),
    ref: nonEmptyString(key.ref, "scope key ref"),
    tile_kind: tileKind,
    tile_id: nonEmptyString(key.tile_id, "scope key tile_id"),
  });
}

function sameScopeKey(left, right) {
  return left.repository === right.repository
    && left.ref === right.ref
    && left.tile_kind === right.tile_kind
    && left.tile_id === right.tile_id;
}

function normalizedIdentity(value) {
  const identity = plainObject(value, "content identity");
  if (
    identity.algorithm !== CONTENT_IDENTITY_ALGORITHM
    || typeof identity.hex !== "string"
    || !/^[0-9a-f]{64}$/.test(identity.hex)
  ) {
    throw new TypeError("content identity must be a lowercase SHA-256 identity");
  }
  return Object.freeze({
    algorithm: CONTENT_IDENTITY_ALGORITHM,
    hex: identity.hex,
  });
}

function normalizedPath(value) {
  if (value === null) return null;
  return nonEmptyString(value, "buffer path");
}

function normalizedLoadState(value, path) {
  const state = value == null ? (path === null ? "empty" : "ready") : value;
  if (!LOAD_STATES.has(state)) {
    throw new TypeError(
      "load_state must be empty, loading, ready, unavailable, or error",
    );
  }
  return state;
}

function frozenBuffer(value) {
  return Object.freeze({
    kind: value.kind,
    repository: value.repository,
    path: value.path,
    owned: value.owned,
    base_ref: value.base_ref,
    base_revision: value.base_revision,
    base_hash: value.base_hash,
    base_content: value.base_content,
    current_hash: value.current_hash,
    content: value.content,
    dirty: value.dirty,
    load_state: value.load_state,
    hash_generation: value.hash_generation,
    hash_pending: value.hash_pending,
  });
}

function validatedBuffer(value) {
  const buffer = plainObject(value, "buffer");
  bufferKind(buffer.kind);
  nonEmptyString(buffer.repository, "buffer repository");
  normalizedPath(buffer.path);
  if (typeof buffer.owned !== "boolean") {
    throw new TypeError("buffer owned must be a boolean");
  }
  nonEmptyString(buffer.base_ref, "buffer base_ref");
  nonEmptyString(buffer.base_revision, "buffer base_revision");
  if (typeof buffer.base_content !== "string" || typeof buffer.content !== "string") {
    throw new TypeError("buffer content and base_content must be strings");
  }
  normalizedIdentity(buffer.base_hash);
  if (buffer.current_hash !== null) normalizedIdentity(buffer.current_hash);
  if (!Number.isSafeInteger(buffer.hash_generation) || buffer.hash_generation < 0) {
    throw new TypeError("buffer hash_generation must be a non-negative integer");
  }
  if (typeof buffer.hash_pending !== "boolean") {
    throw new TypeError("buffer hash_pending must be a boolean");
  }
  return buffer;
}

export async function createBufferState(descriptor, options = {}) {
  const input = plainObject(descriptor, "buffer descriptor");
  const kind = bufferKind(input.kind);
  const repository = nonEmptyString(input.repository, "buffer repository");
  const path = normalizedPath(input.path === undefined ? null : input.path);
  if (typeof input.owned !== "boolean") {
    throw new TypeError("buffer owned must be a boolean");
  }
  const baseRef = nonEmptyString(input.base_ref, "buffer base_ref");
  const baseRevision = nonEmptyString(
    input.base_revision,
    "buffer base_revision",
  );
  if (typeof input.content !== "string") {
    throw new TypeError("buffer content must be a string");
  }
  const hash = options.hash || contentIdentity;
  if (typeof hash !== "function") throw new TypeError("hash must be a function");
  const identity = normalizedIdentity(await hash(input.content));
  return frozenBuffer({
    kind,
    repository,
    path,
    owned: input.owned,
    base_ref: baseRef,
    base_revision: baseRevision,
    base_hash: identity,
    base_content: input.content,
    current_hash: identity,
    content: input.content,
    dirty: false,
    load_state: normalizedLoadState(input.load_state, path),
    hash_generation: 0,
    hash_pending: false,
  });
}

// Build the keyed buffer set: the reserved `outline` buffer plus ZERO OR MORE
// document buffers (design D1). `document` names the ONE reserved unbacked slot
// -- the create flow's not-yet-created artifact, and the shape a Phase A
// session was always built in -- while `documents` is the keyed set of loaded
// documents, each keyed by its own path. Passing neither is legal: an outline
// alone is a working state.
export async function createDoxBenchState(descriptor, options = {}) {
  const input = plainObject(descriptor, "doxBench state descriptor");
  const key = normalizedScopeKey(input.key);
  const pending = [["outline", createBufferState({
    ...plainObject(input.outline, "outline descriptor"),
    kind: "outline",
    repository: key.repository,
  }, options)]];
  if (input.document !== undefined && input.document !== null) {
    pending.push([UNBACKED_DOCUMENT_BUFFER_KEY, createBufferState({
      ...plainObject(input.document, "document descriptor"),
      kind: "document",
      repository: key.repository,
    }, options)]);
  }
  const documents = input.documents === undefined || input.documents === null
    ? {}
    : plainObject(input.documents, "documents descriptor map");
  for (const documentKey of Object.keys(documents)) {
    if (documentKey === OUTLINE_BUFFER_KEY) {
      throw new TypeError("the outline key is reserved for the outline buffer");
    }
    pending.push([documentKey, createBufferState({
      ...plainObject(documents[documentKey], "document descriptor"),
      kind: "document",
      repository: key.repository,
    }, options)]);
  }
  const built = await Promise.all(pending.map(([, promise]) => promise));
  const buffers = {};
  pending.forEach(([bufferKey], index) => {
    buffers[bufferKey] = built[index];
  });
  return validatedFrozenState({
    key,
    active_buffer: input.active_buffer || OUTLINE_BUFFER_KEY,
    buffers,
  });
}

// Begin an edit immediately and hash it asynchronously. While `hash_pending`
// is true, `current_hash` is deliberately null: exposing the previous digest
// beside newer text would be a false authority claim. Turn, Apply, and Save
// callers must wait for `completion` and settle it before continuing.
export function beginBufferEdit(bufferValue, content, options = {}) {
  const buffer = validatedBuffer(bufferValue);
  if (typeof content !== "string") {
    throw new TypeError("buffer content must be a string");
  }
  const hash = options.hash || contentIdentity;
  if (typeof hash !== "function") throw new TypeError("hash must be a function");
  const generation = buffer.hash_generation + 1;
  const pending = frozenBuffer({
    ...buffer,
    content,
    current_hash: null,
    dirty: content !== buffer.base_content,
    hash_generation: generation,
    hash_pending: true,
  });
  const completion = Promise.resolve()
    .then(() => hash(content))
    .then((identity) => Object.freeze({
      generation,
      content,
      identity: normalizedIdentity(identity),
    }));
  return Object.freeze({ buffer: pending, completion });
}

export function settleBufferHash(bufferValue, completionValue) {
  const buffer = validatedBuffer(bufferValue);
  const completion = plainObject(completionValue, "hash completion");
  if (
    completion.generation !== buffer.hash_generation
    || completion.content !== buffer.content
  ) {
    return Object.freeze({
      buffer,
      applied: false,
      reason: "stale_generation",
    });
  }
  const identity = normalizedIdentity(completion.identity);
  return Object.freeze({
    buffer: frozenBuffer({
      ...buffer,
      current_hash: identity,
      dirty: identity.hex !== buffer.base_hash.hex,
      hash_pending: false,
    }),
    applied: true,
    reason: null,
  });
}

// The base transition a GOVERNED SAVE leaves behind (010-doxbench-editor-chat
// T079, FR-035/FR-038). The text that landed is now this buffer's base, and it
// is described by the ref, revision, and content identity THE SERVER REPORTED --
// never by the client's own optimistic guess, which is the whole point of
// following the resulting session ref rather than assuming it.
//
// The adopted identity is validated by the SAME STRICT rule every identity this
// module writes into state is validated by: adoption WRITES state, and a base
// that cannot be verified later is worse than no base at all. A server answer
// that fails it is a refusal here (a thrown TypeError the caller reports),
// never a silently stored half-fact.
//
// The generation is stepped so a hash still in flight over the older text
// settles against a buffer that has moved on and is correctly dropped.
export function adoptSavedBase(bufferValue, savedValue) {
  const buffer = validatedBuffer(bufferValue);
  const saved = plainObject(savedValue, "saved base");
  const identity = normalizedIdentity(saved.content_hash);
  return frozenBuffer({
    ...buffer,
    base_ref: nonEmptyString(saved.ref, "saved base ref"),
    base_revision: nonEmptyString(saved.revision, "saved base revision"),
    base_hash: identity,
    base_content: buffer.content,
    current_hash: identity,
    dirty: false,
    hash_generation: buffer.hash_generation + 1,
    hash_pending: false,
  });
}

// Move working state onto another scope key, keeping both buffers exactly as
// they are (010-doxbench-editor-chat T079, FR-038/FR-039).
//
// A first Save creates or joins a branch session, so the buffers that were being
// edited against `main` now belong to the SESSION ref. No existing primitive can
// express that: `createDoxBenchState` re-reads content as its own base and would
// discard every unsaved change, which is the opposite of what a rekey means.
// The repository may not move -- a scope key naming another repository is a
// different corpus, not a rename -- and the buffers already carry that fact, so
// disagreement is refused rather than reconciled.
export function rekeyDoxBenchState(stateValue, keyValue) {
  const current = validatedDoxBenchState(stateValue);
  const key = normalizedScopeKey(keyValue);
  if (key.repository !== current.key.repository) {
    throw new TypeError(
      "a rekey may not move working state to another repository",
    );
  }
  return validatedFrozenState({
    key,
    active_buffer: current.active,
    buffers: current.buffers,
  });
}

export function discardBuffer(bufferValue) {
  const buffer = validatedBuffer(bufferValue);
  return frozenBuffer({
    ...buffer,
    content: buffer.base_content,
    current_hash: buffer.base_hash,
    dirty: false,
    hash_generation: buffer.hash_generation + 1,
    hash_pending: false,
  });
}

// THE KEYED-SET RULE (design D1; the delta's `doxBench editor buffer contract`).
// The exactly-two-keys throw is REPLACED, not relaxed into silence -- every
// clause below is a refusal:
//
//   * `outline` is PRESENT and its buffer declares kind `outline`;
//   * every OTHER key holds a buffer of kind `document`;
//   * the reserved `document` key appears at most once (it is one object key, so
//     that is structural) and is the ONLY key permitted to hold a buffer whose
//     path does not equal the key;
//   * every other document key EQUALS its own buffer's path, so a document is
//     loaded at most once and no two buffers can claim the same file -- which is
//     also checked directly, across the reserved key too;
//   * every buffer's repository equals the scope's;
//   * `active_buffer` names a key the set actually holds.
//
// BACKWARD COMPATIBILITY, deliberately (D1's migration-free property, task 4.5):
// a Phase A state is `{outline, document}` where the `document` buffer routinely
// carried a REAL path -- that was the single document slot. Such a state is a
// LEGAL INSTANCE here, because the reserved key admits a path-backed buffer as
// well as an unbacked one. That is why the restore path needs no migration, no
// envelope version bump, and no "old shape" branch. Every NEW load keys by path;
// the reserved key is only ever reached by the create flow or by a restored
// Phase A envelope, and `rekeyDocumentBuffer` moves it to its path.
function validatedDoxBenchState(value) {
  const state = plainObject(value, "doxBench state");
  const key = normalizedScopeKey(state.key);
  const buffers = plainObject(state.buffers, "doxBench buffers");
  const keys = Object.keys(buffers);
  if (!keys.includes(OUTLINE_BUFFER_KEY)) {
    throw new TypeError("doxBench state must contain the reserved outline buffer");
  }
  const validated = {};
  const documentKeys = [];
  const claimedPaths = new Set();
  for (const bufferKeyValue of keys) {
    const buffer = validatedBuffer(buffers[bufferKeyValue]);
    if (buffer.repository !== key.repository) {
      throw new TypeError("every buffer must use the same repository as the scope");
    }
    if (bufferKeyValue === OUTLINE_BUFFER_KEY) {
      if (buffer.kind !== "outline") {
        throw new TypeError("the outline key must hold the outline buffer");
      }
    } else {
      if (buffer.kind !== "document") {
        throw new TypeError("every key beside outline must hold a document buffer");
      }
      if (bufferKeyValue !== UNBACKED_DOCUMENT_BUFFER_KEY
          && buffer.path !== bufferKeyValue) {
        throw new TypeError("a document buffer's key must equal its own path");
      }
      if (buffer.path !== null) {
        if (claimedPaths.has(buffer.path)) {
          throw new TypeError("two buffers must not claim the same document path");
        }
        claimedPaths.add(buffer.path);
      }
      documentKeys.push(bufferKeyValue);
    }
    validated[bufferKeyValue] = buffer;
  }
  const active = bufferKeyString(state.active_buffer, "active buffer");
  if (!Object.prototype.hasOwnProperty.call(validated, active)) {
    throw new TypeError("active buffer must name a buffer the state holds");
  }
  return {
    state,
    key,
    active,
    buffers: validated,
    outline: validated[OUTLINE_BUFFER_KEY],
    documentKeys: orderedDocumentKeys(documentKeys),
  };
}

// One frozen state object, from one validated shape. Every exported transition
// funnels through here so no caller can assemble a state the validator would
// have refused.
function validatedFrozenState(candidate) {
  const current = validatedDoxBenchState(candidate);
  return Object.freeze({
    key: current.key,
    active_buffer: current.active,
    buffers: Object.freeze({ ...current.buffers }),
  });
}

// The loaded set, as the selector and the save order read it: the outline key
// first, then the document keys in the DECLARED deterministic order.
export function bufferKeysInOrder(stateValue) {
  const current = validatedDoxBenchState(stateValue);
  return Object.freeze([OUTLINE_BUFFER_KEY, ...current.documentKeys]);
}

export function loadedDocumentKeys(stateValue) {
  return validatedDoxBenchState(stateValue).documentKeys;
}

// Replace one buffer, in place, under the key it already occupies.
//
// The key is resolved rather than switched on a kind literal: an explicit
// `keyValue` wins; otherwise an outline buffer takes the reserved outline key; a
// document buffer that some existing key already holds AT THE SAME PATH stays
// under THAT key -- which is what keeps a restored Phase A buffer (a real path
// under the reserved `document` key) from silently re-keying itself on an
// ordinary edit; and only a genuinely new document lands on its derived key.
export function replaceBuffer(stateValue, bufferValue, keyValue) {
  const current = validatedDoxBenchState(stateValue);
  const buffer = validatedBuffer(bufferValue);
  if (buffer.repository !== current.key.repository) {
    throw new TypeError("replacement buffer must use the same repository as the scope");
  }
  let target;
  if (keyValue !== undefined && keyValue !== null) {
    target = bufferKeyString(keyValue, "buffer key");
  } else if (buffer.kind === "outline") {
    target = OUTLINE_BUFFER_KEY;
  } else {
    target = current.documentKeys.find(
      (candidate) => current.buffers[candidate].path === buffer.path,
    ) ?? bufferKeyFor(buffer);
  }
  return validatedFrozenState({
    key: current.key,
    active_buffer: current.active,
    buffers: { ...current.buffers, [target]: buffer },
  });
}

export function setActiveBuffer(stateValue, keyValue) {
  const current = validatedDoxBenchState(stateValue);
  return validatedFrozenState({
    key: current.key,
    active_buffer: bufferKeyString(keyValue, "active buffer"),
    buffers: current.buffers,
  });
}

// ---------------------------------------------------------------------------
// THE LOADED SET (the delta's `The doxBench loaded set is the outline plus the
// documents the human loaded`). Membership changes only here, and only by an
// act a human performed: `loadDocumentBuffer` is the ONE route in and
// `unloadDocumentBuffer` the one route out. A retrieval result, a proposal, the
// snapshot and an inherited edge all reach neither.
// ---------------------------------------------------------------------------

export const LOAD_REFUSED_ALREADY_LOADED = "already_loaded";
export const LOAD_REFUSED_BOUND_REACHED = "loaded_set_bound_reached";
export const UNLOAD_REFUSED_DIRTY = "unsaved_edits";

// Add a document buffer under its path key, or -- when the loaded set already
// holds that path -- SELECT the buffer that is already there and report it.
// Re-reading the document from source would silently discard its unsaved text,
// which is the one thing the scenario forbids, so the existing buffer is never
// replaced.
export function loadDocumentBuffer(stateValue, bufferValue, options = {}) {
  const current = validatedDoxBenchState(stateValue);
  const buffer = validatedBuffer(bufferValue);
  if (buffer.kind !== "document") {
    throw new TypeError("only a document buffer can join the loaded set");
  }
  if (buffer.repository !== current.key.repository) {
    throw new TypeError("a loaded buffer must use the same repository as the scope");
  }
  const existing = current.documentKeys.find(
    (candidate) => current.buffers[candidate].path === buffer.path,
  );
  if (existing !== undefined) {
    return Object.freeze({
      state: validatedFrozenState({
        key: current.key,
        active_buffer: existing,
        buffers: current.buffers,
      }),
      key: existing,
      loaded: false,
      refusal: LOAD_REFUSED_ALREADY_LOADED,
      bound: null,
      measured: current.documentKeys.length,
    });
  }
  const bound = Number.isSafeInteger(options.maxLoadedDocuments)
    ? options.maxLoadedDocuments
    : DOXBENCH_MAX_LOADED_DOCUMENTS;
  if (current.documentKeys.length >= bound) {
    // REFUSE and state the number (design D6). Nothing already loaded is
    // evicted: every loaded buffer may hold unsaved work, so making room would
    // be discarding human text.
    return Object.freeze({
      state: validatedFrozenState({
        key: current.key,
        active_buffer: current.active,
        buffers: current.buffers,
      }),
      key: null,
      loaded: false,
      refusal: LOAD_REFUSED_BOUND_REACHED,
      bound,
      measured: current.documentKeys.length,
    });
  }
  const target = bufferKeyFor(buffer);
  return Object.freeze({
    state: validatedFrozenState({
      key: current.key,
      active_buffer: target,
      buffers: { ...current.buffers, [target]: buffer },
    }),
    key: target,
    loaded: true,
    refusal: null,
    bound,
    measured: current.documentKeys.length + 1,
  });
}

// Leave the loaded set. A DIRTY buffer is refused unless the caller states an
// explicit discard, because dropping it destroys unsaved work exactly as Cancel
// does -- and Cancel at least says so.
export function unloadDocumentBuffer(stateValue, keyValue, options = {}) {
  const current = validatedDoxBenchState(stateValue);
  const target = bufferKeyString(keyValue, "buffer key");
  if (target === OUTLINE_BUFFER_KEY) {
    throw new TypeError("the outline buffer is reserved and cannot be unloaded");
  }
  const buffer = current.buffers[target];
  if (buffer === undefined) {
    throw new TypeError("unload must name a buffer the loaded set holds");
  }
  if (buffer.dirty === true && options.discardUnsavedEdits !== true) {
    return Object.freeze({
      state: validatedFrozenState({
        key: current.key,
        active_buffer: current.active,
        buffers: current.buffers,
      }),
      unloaded: false,
      refusal: UNLOAD_REFUSED_DIRTY,
    });
  }
  const remaining = { ...current.buffers };
  delete remaining[target];
  return Object.freeze({
    state: validatedFrozenState({
      key: current.key,
      active_buffer: current.active === target ? OUTLINE_BUFFER_KEY : current.active,
      buffers: remaining,
    }),
    unloaded: true,
    refusal: null,
  });
}

// Move the reserved unbacked buffer onto the path the SERVER reported for it
// (task 4.4; the delta's re-key scenario). The create flow's buffer had no path
// to be keyed by; the server's first Save answer gives it one, and the reserved
// key is freed WITHOUT carrying anything from the buffer that left it.
//
// The hash generation is stepped, exactly as every other base transition steps
// it, so a hash still in flight over the older text settles against a buffer
// that has moved on and is correctly dropped. Stepping twice (once in
// `adoptSavedBase`, once here) is harmless: the counter is monotonic and only
// ever used to drop stale settles.
export function rekeyDocumentBuffer(stateValue, fromKeyValue, pathValue) {
  const current = validatedDoxBenchState(stateValue);
  const from = bufferKeyString(fromKeyValue, "buffer key");
  if (from === OUTLINE_BUFFER_KEY) {
    throw new TypeError("the outline key is reserved and cannot be re-keyed");
  }
  const buffer = current.buffers[from];
  if (buffer === undefined) {
    throw new TypeError("a re-key must name a buffer the state holds");
  }
  const path = nonEmptyString(pathValue, "re-keyed buffer path");
  if (path !== from && Object.prototype.hasOwnProperty.call(current.buffers, path)) {
    throw new TypeError("a re-key must not overwrite another loaded document");
  }
  const moved = frozenBuffer({
    ...buffer,
    path,
    hash_generation: buffer.hash_generation + 1,
    hash_pending: false,
  });
  const buffers = { ...current.buffers };
  delete buffers[from];
  buffers[path] = moved;
  return validatedFrozenState({
    key: current.key,
    active_buffer: current.active === from ? path : current.active,
    buffers,
  });
}

export function scopeStorageKey(keyValue) {
  const key = normalizedScopeKey(keyValue);
  return SESSION_KEY_PREFIX + encodeURIComponent(JSON.stringify([
    key.repository,
    key.ref,
    key.tile_kind,
    key.tile_id,
  ]));
}

function sessionStorageOf(injected) {
  if (injected) return injected;
  try {
    return globalThis.window?.sessionStorage || globalThis.sessionStorage || null;
  } catch {
    return null;
  }
}

function persistedBuffer(buffer) {
  return {
    path: buffer.path,
    owned: buffer.owned,
    base_ref: buffer.base_ref,
    base_revision: buffer.base_revision,
    base_content: buffer.base_content,
    content: buffer.content,
    load_state: buffer.load_state,
  };
}

export function persistDoxBenchState(stateValue, injectedStorage,
                                     companionValue) {
  let current;
  try {
    current = validatedDoxBenchState(stateValue);
  } catch {
    return false;
  }
  const storage = sessionStorageOf(injectedStorage);
  if (!storage) return false;
  // The KEYED SET, written under its own keys. The envelope's
  // `schema_version` does NOT move (design D1): a Phase A record is
  // `{outline, document}`, which is a legal instance of this shape, so nothing
  // previously written becomes unreadable and no migration branch exists.
  const persistedBuffers = {};
  for (const bufferKeyValue of Object.keys(current.buffers)) {
    persistedBuffers[bufferKeyValue] = persistedBuffer(
      current.buffers[bufferKeyValue]);
  }
  const envelope = {
    schema_version: DOXBENCH_SESSION_STATE_VERSION,
    kind: DOXBENCH_SESSION_STATE_KIND,
    key: current.key,
    active_buffer: current.active,
    buffers: persistedBuffers,
  };
  // R-1 (operator requirement: "reopening the same tile continues the work").
  // The chat working state — subject, selected model, transcript AND the
  // PROPOSAL SET — rides in the SAME record as the buffers, deliberately:
  // proposals reference buffer content hashes, so restoring one without the
  // other resurrects cards whose bases no longer match the restored text.
  // One record means one atomic write and one atomic read. The blob is
  // OPAQUE here (this module owns buffers, not chat semantics) and the
  // restorer recomputes proposal currency against the restored hashes, so a
  // drifted base can only ever come back as STALE, never as current.
  if (companionValue !== undefined && companionValue !== null) {
    envelope.companion = companionValue;
  }
  try {
    storage.setItem(scopeStorageKey(current.key), JSON.stringify(envelope));
    return true;
  } catch {
    return false;
  }
}

function removeStoredKey(storage, key) {
  try {
    storage.removeItem(key);
  } catch {
    // Storage can be blocked or exhausted. Recovery still degrades to absent.
  }
}

async function restoredBuffer(kind, repository, raw, options) {
  const saved = plainObject(raw, `${kind} stored buffer`);
  if (typeof saved.base_content !== "string" || typeof saved.content !== "string") {
    throw new TypeError("stored buffer content must be strings");
  }
  const base = await createBufferState({
    kind,
    repository,
    path: saved.path === undefined ? null : saved.path,
    owned: saved.owned,
    base_ref: saved.base_ref,
    base_revision: saved.base_revision,
    content: saved.base_content,
    load_state: saved.load_state,
  }, options);
  if (saved.content === saved.base_content) return base;
  const hash = options.hash || contentIdentity;
  const identity = normalizedIdentity(await hash(saved.content));
  return frozenBuffer({
    ...base,
    content: saved.content,
    current_hash: identity,
    dirty: identity.hex !== base.base_hash.hex,
  });
}

export async function restoreDoxBenchState(
  keyValue,
  injectedStorage,
  options = {},
) {
  const key = normalizedScopeKey(keyValue);
  const storageKey = scopeStorageKey(key);
  const storage = sessionStorageOf(injectedStorage);
  if (!storage) return null;
  let raw;
  try {
    raw = storage.getItem(storageKey);
  } catch {
    return null;
  }
  if (!raw) return null;
  try {
    const envelope = plainObject(JSON.parse(raw), "stored doxBench state");
    if (
      envelope.schema_version !== DOXBENCH_SESSION_STATE_VERSION
      || envelope.kind !== DOXBENCH_SESSION_STATE_KIND
    ) {
      throw new TypeError("stored doxBench state has an unsupported version");
    }
    const storedKey = normalizedScopeKey(envelope.key);
    if (!sameScopeKey(key, storedKey)) {
      throw new TypeError("stored doxBench state belongs to another scope");
    }
    const companion = envelope.companion === undefined
      ? null : envelope.companion;
    const buffers = plainObject(envelope.buffers, "stored doxBench buffers");
    const bufferKeys = Object.keys(buffers);
    if (!bufferKeys.includes(OUTLINE_BUFFER_KEY)) {
      throw new TypeError("stored doxBench state must contain the outline buffer");
    }
    // An envelope whose KEYS disagree with its own buffers is refused rather
    // than reconciled: a stored document key that is not the reserved one must
    // equal the path it stored, or the record cannot be trusted to say which
    // file the text belongs to. A Phase A record -- `{outline, document}`, its
    // `document` slot carrying a real path -- passes unchanged, which is D1's
    // migration-free property.
    for (const bufferKeyValue of bufferKeys) {
      if (bufferKeyValue === OUTLINE_BUFFER_KEY
          || bufferKeyValue === UNBACKED_DOCUMENT_BUFFER_KEY) {
        continue;
      }
      const stored = plainObject(buffers[bufferKeyValue], "stored buffer");
      if (stored.path !== bufferKeyValue) {
        throw new TypeError("a stored document key must equal its own path");
      }
    }
    const restored = await Promise.all(bufferKeys.map((bufferKeyValue) =>
      restoredBuffer(
        bufferKeyValue === OUTLINE_BUFFER_KEY ? "outline" : "document",
        key.repository, buffers[bufferKeyValue], options)));
    const restoredBuffers = {};
    bufferKeys.forEach((bufferKeyValue, index) => {
      restoredBuffers[bufferKeyValue] = restored[index];
    });
    return Object.freeze({
      ...validatedFrozenState({
        key,
        active_buffer: envelope.active_buffer,
        buffers: restoredBuffers,
      }),
      // R-1: handed back with the buffers it was written beside, so the
      // caller restores BOTH or neither.
      companion,
    });
  } catch {
    removeStoredKey(storage, storageKey);
    return null;
  }
}

export function clearDoxBenchSession(keyValue, injectedStorage) {
  const key = normalizedScopeKey(keyValue);
  const storage = sessionStorageOf(injectedStorage);
  if (!storage) return false;
  try {
    storage.removeItem(scopeStorageKey(key));
    return true;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// T064 (US3): reversible ONE-buffer local Apply. IMMEDIATE exact-identity
// revalidation happens here — at the swap itself, not merely at review time
// (FR-028): the proposal's base identity must equal the buffer's SETTLED
// current identity byte-for-byte, or the Apply refuses with null and the
// buffer is untouched. Recovery from a refusal is a NEW TURN; there is no
// force path. An accepted Apply is an ORDINARY tracked edit
// (`beginBufferEdit`), so reversibility needs no new machinery: `dirty` is
// derived against the same base content, Discard reverts it exactly like a
// human edit, and Save remains the only exit to persistence.
// ---------------------------------------------------------------------------

export function applyProposalToBuffer(bufferValue, proposalValue, options = {}) {
  const buffer = validatedBuffer(bufferValue);
  if (buffer.hash_pending || !buffer.current_hash) {
    return null;  // an unsettled identity cannot be revalidated against
  }
  const base = proposalValue && proposalValue.base_hash;
  if (base !== buffer.current_hash.hex) {
    return null;  // stale: the buffer moved since the model saw it
  }
  return beginBufferEdit(buffer, String(proposalValue.content), options);
}
