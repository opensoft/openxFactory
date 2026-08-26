// doxBench's ordered Save orchestration (010-doxbench-editor-chat, US4:
// T077/T078). Pure state in, one INJECTED transport, a truthful per-buffer
// verdict out.
//
// This module stays import-free, exactly like ./doxbench-state.js, so the Node
// harness that drives it executes the same bytes the browser does. It therefore
// carries no primitive of its own for reaching anything: the transport is
// handed in, and it is the only way out of this file.
//
// WHAT SAVE OWNS: order, per-buffer action, and the honest report. Nothing else.
//
//   ORDER (FR-034, re-cut by add-doxbench-editing-phase-b design D3). Phase A
//   declared a fixed ORDERED PAIR with a fail-closed CHAIN. Phase B holds N
//   documents, and keeping the chain would have got the semantics wrong, so the
//   rule is restated rather than the list lengthened:
//
//     1. The `outline` buffer, when dirty, is persisted FIRST. Its commit
//        establishes the session ancestry every document commit descends from --
//        the module's own recorded reason, unchanged.
//     2. A dirty outline that did NOT land stops EVERY document, each reported
//        `not_attempted` with the missing-ancestry reason. Unchanged from Phase A.
//     3. Every dirty document is then attempted INDEPENDENTLY. One document's
//        refusal stops NO other document, because documents carry no ancestry
//        dependency on each other: each save is one gate action producing one
//        commit on the same branch, and commit n+1 descends from commit n
//        regardless of which document n held. Keeping the chain here would
//        report untried work as blocked by a refusal that had nothing to do
//        with it -- a false statement about both buffers.
//     4. Documents run in a DECLARED DETERMINISTIC order (ascending
//        lexicographic by buffer key). Brett's rule is "documents in any order",
//        which constrains the CONTRACT -- no ordering rule is imposed on
//        documents -- and does not license a nondeterministic one, because a
//        commit series no test can pin is not a commit series anybody can read.
//
//   ACTION (FR-031). A buffer that already has a path is the EXISTING edit
//   action; a buffer that has none yet is the EXISTING create action. Save adds
//   no third verb, and it adds no authority: the action named here is a REQUEST,
//   and the server answers it again from the tree it is about to write
//   (`branch_session.first_edit_eligibility`). A client that believed its own
//   answer would be claiming an authority it does not hold.
//
//   THE REPORT (FR-035). Every buffer gets its own row, always all of them,
//   always the same seven fields, so a partial outcome cannot be reported with
//   a field quietly missing or with two verdicts blended into one. Only rows
//   the server actually committed advance their base, and they advance it to the
//   identity the SERVER reported — never to the client's own optimistic guess.
//   A refused buffer keeps its text, its base, and its dirty flag untouched.
//   The row SHAPE is unchanged by Phase B; there are simply more rows, and
//   `wholeStatus`'s `partial` verdict becomes much more likely, which is why the
//   ratified per-buffer reporting rule matters more after the widening than
//   before it.
//
// WHAT SAVE DOES NOT OWN:
//
//   * DIRTINESS. `buffer.dirty` is doxbench-state.js's answer and is read, never
//     recomputed. There is no hashing here at all, which is also why there is no
//     asynchronous work in this module beyond awaiting the transport itself.
//   * OWNERSHIP. `buffer.owned` is PRESENTATION INPUT. A buffer the console is
//     showing as read-only context is WITHHELD here and reported refused, which
//     only ever declines to ask — it can never license anything, because a
//     withheld request reaches no authority at all. The reverse reading would be
//     the bug: `owned === true` is not permission, so it is not sent to the
//     server either, and the server decides ownership for every request it does
//     receive from its OWN rule (gate_routes.tile_owned_prefix, FR-036).
//   * MUTATION OF ANY KIND beyond returning new frozen objects. Nothing here
//     touches the served checkout, a branch, a record, or browser storage.

// THE ANCESTRY KEY. Permanently reserved, and the only literal buffer name this
// module knows -- because the outline's commit IS the session ancestry, which is
// the whole reason the save order has a rule at all.
export const OUTLINE_BUFFER_KEY = "outline";

// The DECLARED document order (design D3 point 4). Ascending lexicographic
// comparison of the buffer key by UTF-16 code unit -- no locale, no collator, no
// special case for the reserved `document` key, which orders as the literal
// string it is. Spelled here rather than imported because this module, like
// ./doxbench-state.js, stays import-free so the Node harness executes the
// browser's exact bytes; a companion test asserts the two spellings agree.
export const SAVE_DOCUMENT_ORDER_RULE =
  "ascending lexicographic by buffer key (UTF-16 code unit)";

// The whole ordering rule, in one exported function, so no caller can iterate a
// buffer map's own key order and call it an order.
//
// The outline leads WHEN THE KEY SET HOLDS ONE, and is not invented when it does
// not (issue #291). The prepend used to be unconditional, which stated the
// reserved key as a fact about this MODULE rather than about the state it was
// handed, and so named a buffer for the legitimate absent-outline state this
// file skips everywhere else (see `validatedState` below). Membership is read
// the way the state module reads it -- the key is in the set, or it is not.
export function saveBufferOrder(bufferKeys) {
  const keys = Array.from(bufferKeys);
  const documents = keys.filter((key) => key !== OUTLINE_BUFFER_KEY);
  documents.sort((left, right) => (left < right ? -1 : left > right ? 1 : 0));
  return Object.freeze(keys.includes(OUTLINE_BUFFER_KEY)
    ? [OUTLINE_BUFFER_KEY, ...documents]
    : documents);
}

export const SAVE_ACTION_EDIT = "edit-document";
export const SAVE_ACTION_CREATE = "create-document";

// The four per-buffer verdicts, and the four whole-Save ones. `not_attempted` is
// deliberately distinct from `refused`: "the server said no" and "this was never
// asked" are different facts about the same buffer, and collapsing them would
// hide which one happened.
export const SAVE_BUFFER_STATUSES = Object.freeze([
  "unchanged", "committed", "refused", "not_attempted",
]);
export const SAVE_STATUSES = Object.freeze([
  "unchanged", "committed", "partial", "refused",
]);

const UNSETTLED_IDENTITY_REFUSAL =
  "this buffer's content identity has not settled yet, so the bytes cannot be "
  + "saved with a stated identity -- wait for the edit to settle and save again";

const CONTEXT_ONLY_REFUSAL =
  "this buffer is read-only context in the opened tile, not the tile's own "
  + "material, so it is not offered to the governed Save (FR-036)";

const BLOCKED_BY_EARLIER_REFUSAL =
  "the outline did not land, so there is no session ancestry for this document "
  + "to be saved against -- nothing was sent";

function plainObject(value, name) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${name} must be an object`);
  }
  return value;
}

function nonEmptyString(value) {
  return typeof value === "string" && value !== "" ? value : null;
}

function validatedState(value) {
  const state = plainObject(value, "doxBench state");
  const buffers = plainObject(state.buffers, "doxBench buffers");
  // T100 P1-3 (real-corpus finding): a staged topic with NO outline
  // document legitimately has an ABSENT outline buffer — the design's own
  // honest absent-outline state. An absent key is SKIPPED, not demanded;
  // a present key must still be an object, and at least one buffer must
  // exist or there is nothing to save.
  //
  // Phase B: the keys come from the STATE, in the declared order, rather than
  // from a two-name constant. That is the whole widening at this layer.
  const order = saveBufferOrder(Object.keys(buffers));
  let present = 0;
  for (const key of order) {
    if (buffers[key] == null) continue;
    plainObject(buffers[key], `${key} buffer`);
    present += 1;
  }
  if (present === 0) {
    throw new TypeError("doxBench buffers must carry at least one buffer");
  }
  return Object.freeze({ state, order });
}

// A content identity as the server and the state module both spell it, or null.
// Never coerced into existence: an absent or malformed identity is reported as
// absent, because inventing one is how an unverifiable claim becomes a fact.
//
// THE SAME RULE THE ADOPTING MODULE APPLIES (#290). This used to insist on
// SHAPE ONLY -- any non-empty algorithm, any 64 characters -- on the reasoning
// that the lowercase-SHA-256 rule belongs where an identity is COMPUTED
// (doxbench-state.js's own hashing authority) and that re-deciding it here would
// make this module a second, differently strict judge of a value it only reads
// and forwards. The second half of that reasoning was wrong, and the divergence
// it licensed was the defect: the identity accepted HERE is the identity the
// canvas immediately WRITES into working state through `adoptSavedBase`, which
// accepts only a lowercase SHA-256 one. So an uppercase-hex or `sha512` answer
// read `committed` in this module and threw in that one -- a buffer left dirty
// under a Save reported as landed. Two rules for one value, read and written one
// step apart, is not defence in depth; it is a gap. There is now ONE rule, and
// this module applies it where the value is READ: a stated identity nothing can
// adopt is not a landing, and saying so here is what makes the report true.
//
// It is SPELLED here rather than imported because this module stays
// import-free -- pinned by test_doxbench_mutation_boundary.py's
// `test_the_save_module_has_no_import_statement`, so the Node harness executes
// the browser's exact bytes -- exactly as the document-order rule above is
// re-spelled rather than imported. A companion test
// (test_doxbench_save.py::test_the_reader_and_the_writer_judge_a_content_identity_identically)
// asks BOTH modules the same candidate identities and asserts their answers
// agree, so the two spellings cannot drift apart again unnoticed.
const CONTENT_IDENTITY_ALGORITHM = "sha256";
const CONTENT_IDENTITY_HEX = /^[0-9a-f]{64}$/;

// THE TWO WAYS A STATED IDENTITY FAILS, in the words the refusal is built from.
// Exported because a test that copies a sentence pins the COPY: reword the
// module and the copy silently stops describing it, which is how a pin quietly
// becomes decoration. Asserting the module's own constant is the same move
// `boundReachedReason` makes in doxbench-editor.js, and it keeps the two facts
// -- never stated, versus stated unusably -- distinguishable by test as well as
// by eye.
export const IDENTITY_NOT_STATED = "the content identity it committed";
export const IDENTITY_NOT_ADOPTABLE =
  IDENTITY_NOT_STATED + " as a lowercase SHA-256 identity";

function statedIdentity(value) {
  // AN ARRAY IS NOT AN IDENTITY, even carrying both properties. `typeof [] ===
  // "object"`, so the shape test above admitted one while the adopting module's
  // `plainObject` refuses it -- a fourth divergence, unreachable through JSON
  // but reachable from any caller that hands this module a live value, and one
  // that falsifies the agreement the companion test exists to assert.
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  if (value.algorithm !== CONTENT_IDENTITY_ALGORITHM
      || typeof value.hex !== "string"
      || !CONTENT_IDENTITY_HEX.test(value.hex)) {
    return null;
  }
  return Object.freeze({
    algorithm: CONTENT_IDENTITY_ALGORITHM, hex: value.hex,
  });
}

// WHICH existing action this path implies. A path the console loaded from a
// source is a rewrite; a buffer with no path yet has never been created.
function actionForPath(path) {
  return nonEmptyString(path) ? SAVE_ACTION_EDIT : SAVE_ACTION_CREATE;
}

// One buffer's answer to "does this need saving, may it be offered, and as
// WHICH existing action?" -- pure, so the whole plan can be inspected (and
// tested) without a transport existing at all.
function planRow(key, buffer) {
  const action = actionForPath(buffer.path);
  const base = {
    // THE BUFFER KEY, which Phase A spelled `kind`. The row's first field always
    // named the buffer it is about; under Phase A that identifier happened to be
    // the two-value kind, and under Phase B it is the buffer KEY -- `outline`,
    // the reserved `document` create slot, or a document's own path. Renamed
    // rather than left to carry a path under the word `kind`, which would be a
    // false statement about the field. The row still has exactly seven fields.
    key,
    action,
    document: buffer.path === undefined ? null : buffer.path,
    content: typeof buffer.content === "string" ? buffer.content : null,
    // The base identity travels as the HEX the server revalidates against. A
    // create's base is the ABSENCE of the path, so it declares none.
    base_hash: action === SAVE_ACTION_CREATE
      ? null
      : (statedIdentity(buffer.base_hash)?.hex ?? null),
    base_ref: buffer.base_ref ?? null,
    base_revision: buffer.base_revision ?? null,
    owned: buffer.owned === true,
    refusal: null,
  };
  if (buffer.owned !== true) {
    return Object.freeze({ ...base, refusal: CONTEXT_ONLY_REFUSAL });
  }
  if (buffer.hash_pending === true || statedIdentity(buffer.current_hash) === null) {
    return Object.freeze({ ...base, refusal: UNSETTLED_IDENTITY_REFUSAL });
  }
  if (base.content === null) {
    return Object.freeze({
      ...base,
      refusal: "this buffer holds no text to save",
    });
  }
  return Object.freeze(base);
}

// The declared plan: the buffers that need saving, in the declared order.
// A CLEAN buffer is skipped -- FR-031 persists only changed buffers -- and
// skipping is not reordering: the buffers that remain keep their places.
export function saveOrder(stateValue) {
  const { state, order } = validatedState(stateValue);
  const rows = [];
  for (const key of order) {
    const buffer = state.buffers[key];
    if (buffer == null) continue;  // T100 P1-3: absent key, nothing to plan
    if (buffer.dirty !== true) continue;
    rows.push(planRow(key, buffer));
  }
  return Object.freeze(rows);
}

function outcomeRow(key, {
  status, action = null, ref = null, revision = null, content_hash = null,
  message = null,
} = {}) {
  // EXACTLY the seven declared fields, in one place, so no verdict can be
  // reported with one of them quietly absent (data-model PerBufferSaveOutcome).
  return Object.freeze({
    key, status, action, ref, revision, content_hash, message,
  });
}

// The editor's seam request, reshaped into the state runSave plans from --
// pure, so the seam composition in app.js is one expression with no logic of
// its own (T080 client half). The request rows already carry every buffer
// field the planner reads.
//
// EACH ROW STATES ITS OWN KEY. A Phase B caller sends `key`; a caller that
// sends only `kind` -- the create flow's single-document seam request, which
// legitimately IS the reserved `document` slot mid-create -- keys by that, which
// is exactly the reserved key the state module would have given it. Neither is
// guessed from the path: a row that named its key and then keyed by its path
// would move a buffer the caller was not asking to move.
export function savePlanState(request) {
  return Object.freeze({
    key: request.key,
    buffers: Object.freeze(Object.fromEntries(
      (request.buffers || []).map((row) => [row.key ?? row.kind, row]))),
  });
}

// What one plan row is handed to the transport. Note what is NOT here: the
// client's `owned` flag. Ownership is the server's answer from its own rule, and
// shipping the client's opinion of it would invite the server to trust it.
function transportRequest(scopeKey, row) {
  return Object.freeze({
    key: scopeKey,
    // The transport's own field keeps its Phase A spelling AND its Phase A
    // meaning: it is the buffer's KIND, which is what the server-side verb cares
    // about, and it is derived here rather than carried from the row so the wire
    // shape does not acquire a path under the word `kind`.
    kind: row.key === OUTLINE_BUFFER_KEY ? "outline" : "document",
    action: row.action,
    document: row.document,
    content: row.content,
    base_hash: row.base_hash,
    base_ref: row.base_ref,
    base_revision: row.base_revision,
  });
}

// The transport's answer, read strictly. An `ok` verdict that cannot state
// where it landed, which revision it produced, or what identity it committed is
// not a landing this module will advance a base on -- it is reported as a
// refusal naming what was missing, because a base advanced onto an unstated
// identity is a lie that survives into every later Save.
function readVerdict(key, row, answer) {
  if (!answer || typeof answer !== "object") {
    return outcomeRow(key, {
      status: "refused", action: row.action,
      message: "the Save transport returned no verdict for this buffer",
    });
  }
  if (answer.ok !== true) {
    return outcomeRow(key, {
      status: "refused", action: row.action,
      message: nonEmptyString(answer.message)
        || "the governed Save refused this buffer and stated no reason",
    });
  }
  const ref = nonEmptyString(answer.ref);
  const revision = nonEmptyString(answer.revision);
  const identity = statedIdentity(answer.content_hash);
  const missing = [];
  if (!ref) missing.push("the session ref it landed on");
  if (!revision) missing.push("the revision it produced");
  if (!identity) {
    // An identity that was never stated and one stated in a form nothing can
    // verify later are DIFFERENT facts about the same answer, so the refusal
    // says which happened rather than collapsing them -- the same reason
    // `not_attempted` is kept distinct from `refused` above. Both are the same
    // verdict, though: `refused`, in the vocabulary this module already has,
    // because a base advanced onto either is unverifiable from then on.
    missing.push(answer.content_hash == null
      ? IDENTITY_NOT_STATED
      : IDENTITY_NOT_ADOPTABLE);
  }
  if (missing.length) {
    return outcomeRow(key, {
      status: "refused", action: row.action,
      message: "the governed Save reported success without naming "
        + missing.join(", ") + ", so this buffer's base was not advanced",
    });
  }
  return outcomeRow(key, {
    status: "committed",
    // the action the SERVER performed when it says so, since it is the one that
    // answered new-versus-existing against the tree it wrote
    action: nonEmptyString(answer.action) || row.action,
    ref, revision, content_hash: identity,
  });
}

// The buffer a committed row leaves behind: the text that landed is now this
// buffer's base, described by the identity, revision and ref the SERVER
// reported. The generation is stepped so a hash still in flight over the older
// text settles against a buffer that has moved on and is dropped.
function advancedBuffer(buffer, verdict) {
  return Object.freeze({
    ...buffer,
    base_ref: verdict.ref,
    base_revision: verdict.revision,
    base_hash: verdict.content_hash,
    base_content: buffer.content,
    current_hash: verdict.content_hash,
    dirty: false,
    hash_generation: Number.isSafeInteger(buffer.hash_generation)
      ? buffer.hash_generation + 1
      : 1,
    hash_pending: false,
  });
}

function wholeStatus(rows) {
  const landed = rows.some((row) => row.status === "committed");
  const withheld = rows.some(
    (row) => row.status === "refused" || row.status === "not_attempted",
  );
  if (!landed && !withheld) return "unchanged";
  if (landed && withheld) return "partial";
  return landed ? "committed" : "refused";
}

// Persist every changed buffer -- the outline first as ANCESTRY, then the
// documents INDEPENDENTLY in the declared order -- and report each one
// separately.
//
// `transport(request)` is the caller's ONE way to reach the governed action: it
// answers `{ ok: true, ref, revision, content_hash, ... }` or `{ ok: false,
// message }`, and whatever it throws is caught and reported as that buffer's
// refusal rather than escaping as a crash mid-Save.
//
// `options.only` (design D4) restricts the act to ONE document plus the
// ancestry step, which is what a `docs` tile's own Save is: the same pipeline
// through the same transport, scoped to the document whose tile carries the
// control, because a control that lives on one document's tile and is enabled by
// that document's state must not persist three other documents the human is not
// looking at. Every buffer it did NOT act on is reported `unchanged` if clean
// and OMITTED if it was simply out of scope -- never reported as refused, which
// would be a false statement about a buffer nobody asked about.
export async function runSave(stateValue, options = {}) {
  const { state, order } = validatedState(stateValue);
  const transport = options.transport;
  if (typeof transport !== "function") {
    throw new TypeError("runSave requires an injected transport function");
  }
  const scoped = options.only === undefined || options.only === null
    ? null
    : new Set([OUTLINE_BUFFER_KEY].concat(options.only));
  const plan = saveOrder(state);
  const planned = new Map(plan.map((row) => [row.key, row]));
  const rows = [];
  const buffers = { ...state.buffers };
  // ANCESTRY, and nothing else. Phase A's fail-closed chain stopped every buffer
  // behind ANY refusal; Phase B stops documents on the OUTLINE alone, because
  // documents carry no ancestry dependency on each other and reporting one
  // document's refusal as the cause of another's untried work is a false
  // statement about both.
  let ancestryMissing = false;

  for (const key of order) {
    if (scoped !== null && !scoped.has(key)) continue;
    const row = planned.get(key);
    if (!row) {
      // A buffer the state does not HOLD gets no verdict at all (issue #291):
      // a verdict is a statement of fact about a buffer, and there is no fact
      // to state about one that does not exist. `== null` is the same
      // not-held rule `validatedState` and `saveOrder` already read, so the
      // report cannot name a buffer the planner declined to plan.
      if (state.buffers[key] == null) continue;
      // Held but not dirty: reported `unchanged` rather than silently omitted,
      // and it never blocks anything -- there was nothing to land.
      rows.push(outcomeRow(key, { status: "unchanged" }));
      continue;
    }
    if (key !== OUTLINE_BUFFER_KEY && ancestryMissing) {
      rows.push(outcomeRow(key, {
        status: "not_attempted", action: row.action,
        message: BLOCKED_BY_EARLIER_REFUSAL,
      }));
      continue;
    }
    if (row.refusal) {
      // Withheld before the transport is reached: nothing is asked, so nothing
      // can be authorised by asking.
      rows.push(outcomeRow(key, {
        status: "refused", action: row.action, message: row.refusal,
      }));
      if (key === OUTLINE_BUFFER_KEY) ancestryMissing = true;
      continue;
    }
    let verdict;
    try {
      verdict = readVerdict(key, row,
                            await transport(transportRequest(state.key, row)));
    } catch (error) {
      verdict = outcomeRow(key, {
        status: "refused", action: row.action,
        message: "the Save transport failed for this buffer -- "
          + ((error && error.message) || "unknown error"),
      });
    }
    rows.push(verdict);
    if (verdict.status === "committed") {
      buffers[key] = advancedBuffer(state.buffers[key], verdict);
    } else if (key === OUTLINE_BUFFER_KEY) {
      ancestryMissing = true;
    }
  }

  return Object.freeze({
    status: wholeStatus(rows),
    buffers: Object.freeze(rows),
    state: Object.freeze({
      key: state.key,
      active_buffer: state.active_buffer,
      buffers: Object.freeze(buffers),
    }),
  });
}
