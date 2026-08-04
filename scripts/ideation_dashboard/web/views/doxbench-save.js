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
//   ORDER (FR-034). Outline before Document, from a DECLARED constant rather
//   than from whichever key an object literal happened to be iterated in. The
//   order is also a DEPENDENCY, not a preference: the Document is saved against
//   the session ancestry the Outline's commit establishes, so an Outline that
//   did not land leaves the Document with nothing to descend from and it is
//   reported `not_attempted` rather than sent anyway. One rule, fail-closed:
//   ANY earlier buffer that neither committed nor was unchanged stops the ones
//   behind it, and every stopped buffer says so in its own row.
//
//   ACTION (FR-031). A buffer that already has a path is the EXISTING edit
//   action; a buffer that has none yet is the EXISTING create action. Save adds
//   no third verb, and it adds no authority: the action named here is a REQUEST,
//   and the server answers it again from the tree it is about to write
//   (`branch_session.first_edit_eligibility`). A client that believed its own
//   answer would be claiming an authority it does not hold.
//
//   THE REPORT (FR-035). Every buffer gets its own row, always both of them,
//   always the same seven fields, so a partial outcome cannot be reported with
//   a field quietly missing or with two verdicts blended into one. Only rows
//   the server actually committed advance their base, and they advance it to the
//   identity the SERVER reported — never to the client's own optimistic guess.
//   A refused buffer keeps its text, its base, and its dirty flag untouched.
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

export const SAVE_BUFFER_ORDER = Object.freeze(["outline", "document"]);

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
  "an earlier buffer in the Save order did not land, so there is no session "
  + "ancestry for this one to be saved against -- nothing was sent";

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
  // honest absent-outline state. An absent kind is SKIPPED, not demanded;
  // a present kind must still be an object, and at least one buffer must
  // exist or there is nothing to save.
  let present = 0;
  for (const kind of SAVE_BUFFER_ORDER) {
    if (buffers[kind] == null) continue;
    plainObject(buffers[kind], `${kind} buffer`);
    present += 1;
  }
  if (present === 0) {
    throw new TypeError("doxBench buffers must carry at least one buffer");
  }
  return state;
}

// A content identity as the server and the state module both spell it, or null.
// Never coerced into existence: an absent or malformed identity is reported as
// absent, because inventing one is how an unverifiable claim becomes a fact.
//
// SHAPE, not charset. The lowercase-SHA-256 rule belongs where an identity is
// COMPUTED -- doxbench-state.js's own hashing authority -- and re-deciding it
// here would make this module a second, differently strict judge of a value it
// only ever reads and forwards. What it does insist on is that the identity
// names its algorithm and carries a digest of the declared width, because a
// base advanced onto a half-stated identity is unverifiable later.
const IDENTITY_HEX_LENGTH = 64;

function statedIdentity(value) {
  if (!value || typeof value !== "object") return null;
  const algorithm = nonEmptyString(value.algorithm);
  if (!algorithm || typeof value.hex !== "string"
      || value.hex.length !== IDENTITY_HEX_LENGTH) {
    return null;
  }
  return Object.freeze({ algorithm, hex: value.hex });
}

// WHICH existing action this path implies. A path the console loaded from a
// source is a rewrite; a buffer with no path yet has never been created.
function actionForPath(path) {
  return nonEmptyString(path) ? SAVE_ACTION_EDIT : SAVE_ACTION_CREATE;
}

// One buffer's answer to "does this need saving, may it be offered, and as
// WHICH existing action?" -- pure, so the whole plan can be inspected (and
// tested) without a transport existing at all.
function planRow(kind, buffer) {
  const action = actionForPath(buffer.path);
  const base = {
    kind,
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
  const state = validatedState(stateValue);
  const rows = [];
  for (const kind of SAVE_BUFFER_ORDER) {
    const buffer = state.buffers[kind];
    if (buffer == null) continue;  // T100 P1-3: absent kind, nothing to plan
    if (buffer.dirty !== true) continue;
    rows.push(planRow(kind, buffer));
  }
  return Object.freeze(rows);
}

function outcomeRow(kind, {
  status, action = null, ref = null, revision = null, content_hash = null,
  message = null,
} = {}) {
  // EXACTLY the seven declared fields, in one place, so no verdict can be
  // reported with one of them quietly absent (data-model PerBufferSaveOutcome).
  return Object.freeze({
    kind, status, action, ref, revision, content_hash, message,
  });
}

// The editor's seam request, reshaped into the state runSave plans from --
// pure, so the seam composition in app.js is one expression with no logic of
// its own (T080 client half). The request rows already carry every buffer
// field the planner reads.
export function savePlanState(request) {
  return Object.freeze({
    key: request.key,
    buffers: Object.freeze(Object.fromEntries(
      (request.buffers || []).map((row) => [row.kind, row]))),
  });
}

// What one plan row is handed to the transport. Note what is NOT here: the
// client's `owned` flag. Ownership is the server's answer from its own rule, and
// shipping the client's opinion of it would invite the server to trust it.
function transportRequest(key, row) {
  return Object.freeze({
    key,
    kind: row.kind,
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
function readVerdict(kind, row, answer) {
  if (!answer || typeof answer !== "object") {
    return outcomeRow(kind, {
      status: "refused", action: row.action,
      message: "the Save transport returned no verdict for this buffer",
    });
  }
  if (answer.ok !== true) {
    return outcomeRow(kind, {
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
  if (!identity) missing.push("the content identity it committed");
  if (missing.length) {
    return outcomeRow(kind, {
      status: "refused", action: row.action,
      message: "the governed Save reported success without naming "
        + missing.join(", ") + ", so this buffer's base was not advanced",
    });
  }
  return outcomeRow(kind, {
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

// Persist every changed buffer, Outline first, and report each one separately.
//
// `transport(request)` is the caller's ONE way to reach the governed action: it
// answers `{ ok: true, ref, revision, content_hash, ... }` or `{ ok: false,
// message }`, and whatever it throws is caught and reported as that buffer's
// refusal rather than escaping as a crash mid-Save.
export async function runSave(stateValue, options = {}) {
  const state = validatedState(stateValue);
  const transport = options.transport;
  if (typeof transport !== "function") {
    throw new TypeError("runSave requires an injected transport function");
  }
  const plan = saveOrder(state);
  const planned = new Map(plan.map((row) => [row.kind, row]));
  const rows = [];
  const buffers = { ...state.buffers };
  let blocked = false;

  for (const kind of SAVE_BUFFER_ORDER) {
    const row = planned.get(kind);
    if (!row) {
      // Not dirty: reported `unchanged` rather than silently omitted, and it
      // never blocks the buffer behind it -- there was nothing to land.
      rows.push(outcomeRow(kind, { status: "unchanged" }));
      continue;
    }
    if (blocked) {
      rows.push(outcomeRow(kind, {
        status: "not_attempted", action: row.action,
        message: BLOCKED_BY_EARLIER_REFUSAL,
      }));
      continue;
    }
    if (row.refusal) {
      // Withheld before the transport is reached: nothing is asked, so nothing
      // can be authorised by asking.
      rows.push(outcomeRow(kind, {
        status: "refused", action: row.action, message: row.refusal,
      }));
      blocked = true;
      continue;
    }
    let verdict;
    try {
      verdict = readVerdict(kind, row, await transport(transportRequest(state.key, row)));
    } catch (error) {
      verdict = outcomeRow(kind, {
        status: "refused", action: row.action,
        message: "the Save transport failed for this buffer -- "
          + ((error && error.message) || "unknown error"),
      });
    }
    rows.push(verdict);
    if (verdict.status === "committed") {
      buffers[kind] = advancedBuffer(state.buffers[kind], verdict);
    } else {
      blocked = true;
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
