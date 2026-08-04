// Pure doxBench working-state primitives.
//
// This module stays import-free so the existing Node harness can execute the
// exact browser code. Content hashing is intentionally asynchronous because
// Web Crypto is the browser authority; callers that attach results to mutable
// buffers must pair the promise with their own generation token.

export const DOXBENCH_MAX_BUFFER_BYTES = 400_000;
export const CONTENT_IDENTITY_ALGORITHM = "sha256";
export const BUFFER_KINDS = Object.freeze(["outline", "document"]);
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

function activeBufferKind(value) {
  if (!BUFFER_KIND_SET.has(value)) {
    throw new TypeError("active buffer must be outline or document");
  }
  return value;
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

export async function createDoxBenchState(descriptor, options = {}) {
  const input = plainObject(descriptor, "doxBench state descriptor");
  const key = normalizedScopeKey(input.key);
  const active = activeBufferKind(input.active_buffer || "outline");
  const [outline, documentBuffer] = await Promise.all([
    createBufferState({
      ...plainObject(input.outline, "outline descriptor"),
      kind: "outline",
      repository: key.repository,
    }, options),
    createBufferState({
      ...plainObject(input.document, "document descriptor"),
      kind: "document",
      repository: key.repository,
    }, options),
  ]);
  return Object.freeze({
    key,
    active_buffer: active,
    buffers: Object.freeze({
      outline,
      document: documentBuffer,
    }),
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
  return Object.freeze({
    key,
    active_buffer: current.active,
    buffers: Object.freeze({
      outline: current.outline,
      document: current.documentBuffer,
    }),
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

function validatedDoxBenchState(value) {
  const state = plainObject(value, "doxBench state");
  const key = normalizedScopeKey(state.key);
  const active = activeBufferKind(state.active_buffer);
  const buffers = plainObject(state.buffers, "doxBench buffers");
  const keys = Object.keys(buffers);
  if (
    keys.length !== BUFFER_KINDS.length
    || !BUFFER_KINDS.every((kind) => keys.includes(kind))
  ) {
    throw new TypeError("doxBench state must contain exactly outline and document");
  }
  const outline = validatedBuffer(buffers.outline);
  const documentBuffer = validatedBuffer(buffers.document);
  if (outline.kind !== "outline" || documentBuffer.kind !== "document") {
    throw new TypeError("doxBench buffers must match their outline/document slots");
  }
  for (const buffer of [outline, documentBuffer]) {
    if (buffer.repository !== key.repository) {
      throw new TypeError("both buffers must use the same repository as the scope");
    }
  }
  return { state, key, active, outline, documentBuffer };
}

export function replaceBuffer(stateValue, bufferValue) {
  const current = validatedDoxBenchState(stateValue);
  const buffer = validatedBuffer(bufferValue);
  if (buffer.repository !== current.key.repository) {
    throw new TypeError("replacement buffer must use the same repository as the scope");
  }
  return Object.freeze({
    key: current.key,
    active_buffer: current.active,
    buffers: Object.freeze({
      outline: buffer.kind === "outline" ? buffer : current.outline,
      document: buffer.kind === "document" ? buffer : current.documentBuffer,
    }),
  });
}

export function setActiveBuffer(stateValue, kindValue) {
  const current = validatedDoxBenchState(stateValue);
  const active = activeBufferKind(kindValue);
  return Object.freeze({
    key: current.key,
    active_buffer: active,
    buffers: Object.freeze({
      outline: current.outline,
      document: current.documentBuffer,
    }),
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
  const envelope = {
    schema_version: DOXBENCH_SESSION_STATE_VERSION,
    kind: DOXBENCH_SESSION_STATE_KIND,
    key: current.key,
    active_buffer: current.active,
    buffers: {
      outline: persistedBuffer(current.outline),
      document: persistedBuffer(current.documentBuffer),
    },
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
    if (
      bufferKeys.length !== BUFFER_KINDS.length
      || !BUFFER_KINDS.every((kind) => bufferKeys.includes(kind))
    ) {
      throw new TypeError("stored doxBench state must contain exactly two buffers");
    }
    const [outline, documentBuffer] = await Promise.all([
      restoredBuffer("outline", key.repository, buffers.outline, options),
      restoredBuffer("document", key.repository, buffers.document, options),
    ]);
    return Object.freeze({
      key,
      active_buffer: activeBufferKind(envelope.active_buffer),
      buffers: Object.freeze({
        outline,
        document: documentBuffer,
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
