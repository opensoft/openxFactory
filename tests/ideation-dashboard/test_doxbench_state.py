"""doxBench's keyed buffer set and its generation-safe hashing.

Phase A held exactly two buffers here. `add-doxbench-editing-phase-b` widened
the contract to a KEYED SET -- the permanently reserved `outline` key plus one
key per loaded document, each keyed by its own repository-relative path -- and
this module pins both halves: the Phase A shape as a still-LEGAL INSTANCE
(design D1's migration-free property) and the widened rules that only Phase B
can exercise.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

STATE_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-state.js"
)
NODE = shutil.which("node")


_STATE_HARNESS = """
import {
  BUFFER_KINDS,
  beginBufferEdit,
  contentIdentity,
  createBufferState,
  createDoxBenchState,
  discardBuffer,
  replaceBuffer,
  settleBufferHash,
  setActiveBuffer,
} from './doxbench-state.mjs';

const key = {
  repository: 'fixture-repo',
  ref: 'main',
  tile_kind: 'staged',
  tile_id: 'topic-x',
};
const state = await createDoxBenchState({
  key,
  outline: {
    path: 'ideation/staging/topic-x/topic-x.md',
    owned: true,
    base_ref: 'main',
    base_revision: '1'.repeat(40),
    content: '# Outline\\n',
  },
  document: {
    path: 'ideation/staging/topic-x/detail.md',
    owned: true,
    base_ref: 'main',
    base_revision: '1'.repeat(40),
    content: '# Document\\n',
  },
});
const emptyOutline = await createBufferState({
  kind: 'outline',
  repository: key.repository,
  path: null,
  owned: true,
  base_ref: key.ref,
  base_revision: '1'.repeat(40),
  content: '',
});

const originalDocument = state.buffers.document;
let releaseFirst;
const firstGate = new Promise((resolve) => { releaseFirst = resolve; });
const first = beginBufferEdit(originalDocument, '# First edit\\n', {
  hash: async (content) => {
    await firstGate;
    return contentIdentity(content);
  },
});
const second = beginBufferEdit(first.buffer, '# Second edit\\n');
const secondCompletion = await second.completion;
const secondSettlement = settleBufferHash(second.buffer, secondCompletion);
releaseFirst();
const firstCompletion = await first.completion;
const staleSettlement = settleBufferHash(secondSettlement.buffer, firstCompletion);

const pendingDiscard = beginBufferEdit(
  secondSettlement.buffer,
  '# Will be discarded\\n',
);
const discarded = discardBuffer(pendingDiscard.buffer);
const discardedCompletion = await pendingDiscard.completion;
const lateAfterDiscard = settleBufferHash(discarded, discardedCompletion);

const unchangedPending = beginBufferEdit(discarded, discarded.base_content);
const unchanged = settleBufferHash(
  unchangedPending.buffer,
  await unchangedPending.completion,
);

const outlinePending = beginBufferEdit(
  state.buffers.outline,
  '# Revised outline\\n',
);
const revisedOutline = settleBufferHash(
  outlinePending.buffer,
  await outlinePending.completion,
).buffer;
const withOutline = replaceBuffer(state, revisedOutline);
const activeDocument = setActiveBuffer(withOutline, 'document');

const failures = {};
for (const [name, action] of Object.entries({
  badKind: () => createBufferState({
    kind: 'notes',
    repository: key.repository,
    path: null,
    owned: false,
    base_ref: key.ref,
    base_revision: '1'.repeat(40),
    content: '',
  }),
  wrongRepository: () => replaceBuffer(state, {
    ...state.buffers.document,
    repository: 'other-repo',
  }),
  thirdBuffer: () => setActiveBuffer(state, 'notes'),
})) {
  try {
    await action();
  } catch (error) {
    failures[name] = { name: error.constructor.name, message: error.message };
  }
}

console.log(JSON.stringify({
  bufferKinds: BUFFER_KINDS,
  initial: state,
  emptyOutline,
  race: {
    originalDocument,
    firstPending: first.buffer,
    secondPending: second.buffer,
    settled: secondSettlement,
    stale: staleSettlement,
  },
  discard: {
    discarded,
    late: lateAfterDiscard,
  },
  unchanged,
  replacement: {
    withOutline,
    activeDocument,
  },
  failures,
}));
"""


@pytest.fixture(scope="module")
def state_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench state probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-state")
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    harness = tmp_path / "state-harness.mjs"
    harness.write_text(_STATE_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_phase_a_two_buffer_shape_is_still_a_legal_instance(state_results):
    """RE-PINNED by `add-doxbench-editing-phase-b` (task 4.7).

    Phase A pinned an exactly-two RULE here and said in its own docstring that
    "Phase B is what re-cuts it". It has been re-cut: the state is a keyed set,
    `outline` plus N documents. What this test now pins is the property D1 was
    CHOSEN for -- a state built the Phase A way (the reserved `outline` key plus
    the reserved `document` key) is a LEGAL INSTANCE of the widened shape, so no
    migration, no envelope version bump and no "old shape" branch exists
    anywhere. The widened rules are pinned by their own tests below.

    `BUFFER_KINDS` is still asserted, and still holds the same two values --
    it survives as the KIND vocabulary a buffer declares about itself. It has
    stopped being the state's key list, which is why the keys are read from
    `state.buffers` here rather than from the constant.
    """
    assert state_results["bufferKinds"] == ["outline", "document"]
    state = state_results["initial"]
    assert list(state["buffers"]) == ["outline", "document"]
    assert state["active_buffer"] == "outline"
    assert state["key"] == {
        "repository": "fixture-repo",
        "ref": "main",
        "tile_kind": "staged",
        "tile_id": "topic-x",
    }
    assert state["buffers"]["outline"]["content"] == "# Outline\n"
    assert state["buffers"]["document"]["content"] == "# Document\n"


def test_initial_buffers_track_exact_clean_base_and_current_identity(state_results):
    for buffer in state_results["initial"]["buffers"].values():
        assert buffer["base_content"] == buffer["content"]
        assert buffer["base_hash"] == buffer["current_hash"]
        assert buffer["base_hash"]["algorithm"] == "sha256"
        assert len(buffer["base_hash"]["hex"]) == 64
        assert buffer["dirty"] is False
        assert buffer["hash_pending"] is False
        assert buffer["hash_generation"] == 0
        assert buffer["load_state"] == "ready"


def test_pathless_outline_is_explicit_empty_state_not_fabricated(state_results):
    outline = state_results["emptyOutline"]
    assert outline["kind"] == "outline"
    assert outline["path"] is None
    assert outline["base_content"] == ""
    assert outline["content"] == ""
    assert outline["load_state"] == "empty"
    assert outline["dirty"] is False


def test_newer_hash_completion_wins_and_stale_completion_is_ignored(state_results):
    race = state_results["race"]
    assert race["firstPending"]["hash_pending"] is True
    assert race["firstPending"]["current_hash"] is None
    assert race["secondPending"]["hash_generation"] == (
        race["firstPending"]["hash_generation"] + 1
    )
    assert race["settled"]["applied"] is True
    assert race["settled"]["buffer"]["content"] == "# Second edit\n"
    assert race["settled"]["buffer"]["current_hash"]["algorithm"] == "sha256"
    assert race["settled"]["buffer"]["dirty"] is True
    assert race["stale"]["applied"] is False
    assert race["stale"]["reason"] == "stale_generation"
    assert race["stale"]["buffer"] == race["settled"]["buffer"]
    assert race["originalDocument"]["content"] == "# Document\n"


def test_discard_restores_base_and_invalidates_inflight_hash(state_results):
    result = state_results["discard"]
    discarded = result["discarded"]
    assert discarded["content"] == discarded["base_content"] == "# Document\n"
    assert discarded["current_hash"] == discarded["base_hash"]
    assert discarded["dirty"] is False
    assert discarded["hash_pending"] is False
    assert result["late"]["applied"] is False
    assert result["late"]["buffer"] == discarded


def test_editing_back_to_exact_base_derives_clean_state(state_results):
    unchanged = state_results["unchanged"]
    assert unchanged["applied"] is True
    assert unchanged["buffer"]["dirty"] is False
    assert unchanged["buffer"]["current_hash"] == unchanged["buffer"]["base_hash"]


def test_buffer_replacement_is_targeted_and_the_active_buffer_is_independent(state_results):
    replacement = state_results["replacement"]
    with_outline = replacement["withOutline"]
    assert with_outline["buffers"]["outline"]["content"] == "# Revised outline\n"
    assert with_outline["buffers"]["outline"]["dirty"] is True
    assert with_outline["buffers"]["document"]["content"] == "# Document\n"
    assert with_outline["active_buffer"] == "outline"
    assert replacement["activeDocument"]["active_buffer"] == "document"


def test_invalid_buffer_shapes_and_an_unheld_active_key_are_refused(state_results):
    """RE-PINNED by `add-doxbench-editing-phase-b` (task 4.7).

    The KIND vocabulary is unchanged and still refuses `notes`. What moved is
    the ACTIVE-BUFFER rule: Phase A's `active_buffer` was a two-value enum
    (`outline | document`), and the ratified Phase B contract makes it a KEY of
    the state's own buffer set -- "`active_buffer` names a key the set actually
    holds" -- because the set is now `outline` plus N loaded documents and a
    fixed enum cannot name them. The assertion is NOT weakened: selecting a
    buffer the state does not hold is still a hard refusal, and the message
    states the new rule rather than the retired enum.
    """
    failures = state_results["failures"]
    assert failures["badKind"] == {
        "name": "TypeError",
        "message": "buffer kind must be outline or document",
    }
    assert "same repository" in failures["wrongRepository"]["message"]
    assert failures["thirdBuffer"] == {
        "name": "TypeError",
        "message": "active buffer must name a buffer the state holds",
    }


# ===========================================================================
# T079 (010-doxbench-editor-chat, US4): the two transitions a GOVERNED SAVE
# needs, which no existing primitive can express.
#
# `adoptSavedBase` is the base transition after a commit landed: the text that
# was saved becomes the buffer's base, described by the ref, revision, and
# content identity THE SERVER REPORTED. It is separate from `settleBufferHash`
# on purpose — that one settles an identity this module COMPUTED for text the
# human typed; this one records a foreign fact about text that is now committed
# history. The identity is validated by the same strict lowercase-SHA-256 rule,
# because adoption WRITES state and a base nobody can verify later is worse than
# no base at all.
#
# `rekeyDoxBenchState` moves working state onto another scope key while keeping
# both buffers byte-identical. `createDoxBenchState` cannot express it: it reads
# content as its own base and would discard every unsaved change, which is the
# opposite of what a rekey means — a first Save opens a branch session, and the
# buffers that were being edited against `main` now belong to the session ref
# (FR-038, FR-039).
#
# Pins FR-035, FR-038 and FR-039 at the state module's own surface.
# ===========================================================================

_SAVE_TRANSITION_HARNESS = """
import {
  adoptSavedBase,
  beginBufferEdit,
  createDoxBenchState,
  persistDoxBenchState,
  rekeyDoxBenchState,
  replaceBuffer,
  scopeStorageKey,
  settleBufferHash,
} from './doxbench-state.mjs';

const key = {
  repository: 'fixture-repo',
  ref: 'main',
  tile_kind: 'staged',
  tile_id: 'topic-x',
};
const sessionKey = { ...key, ref: 'draft/topic-x' };
const base = await createDoxBenchState({
  key,
  outline: {
    path: 'ideation/staging/topic-x/topic-x.md',
    owned: true,
    base_ref: 'main',
    base_revision: '1'.repeat(40),
    content: '# Outline\\n',
  },
  document: {
    path: 'ideation/staging/topic-x/detail.md',
    owned: true,
    base_ref: 'main',
    base_revision: '1'.repeat(40),
    content: '# Document\\n',
  },
});

// One dirty buffer, settled, exactly as a Save would find it.
const pending = beginBufferEdit(base.buffers.outline, '# Outline edited\\n');
const dirtyOutline = settleBufferHash(
  pending.buffer, await pending.completion,
).buffer;
const dirty = replaceBuffer(base, dirtyOutline);

const SAVED = {
  ref: 'draft/topic-x',
  revision: 'a'.repeat(40),
  content_hash: { algorithm: 'sha256', hex: 'b'.repeat(64) },
};
const adopted = adoptSavedBase(dirtyOutline, SAVED);

// Every way a reported base can be untrustworthy, refused rather than stored.
const failures = {};
function record(name, fn) {
  try { fn(); failures[name] = null; }
  catch (err) { failures[name] = err.constructor.name + ': ' + err.message; }
}
record('nonHexIdentity', () => adoptSavedBase(dirtyOutline, {
  ...SAVED, content_hash: { algorithm: 'sha256', hex: 'z'.repeat(64) } }));
record('shortIdentity', () => adoptSavedBase(dirtyOutline, {
  ...SAVED, content_hash: { algorithm: 'sha256', hex: 'b'.repeat(63) } }));
record('wrongAlgorithm', () => adoptSavedBase(dirtyOutline, {
  ...SAVED, content_hash: { algorithm: 'sha1', hex: 'b'.repeat(64) } }));
record('absentIdentity', () => adoptSavedBase(dirtyOutline, {
  ref: SAVED.ref, revision: SAVED.revision }));
record('blankRef', () => adoptSavedBase(dirtyOutline, { ...SAVED, ref: '' }));
record('blankRevision', () => adoptSavedBase(dirtyOutline, {
  ...SAVED, revision: '' }));
record('otherRepository', () => rekeyDoxBenchState(dirty, {
  ...sessionKey, repository: 'another-repo' }));

// The rekey keeps the dirty buffer exactly, and persists under the SESSION key.
const rekeyed = rekeyDoxBenchState(dirty, sessionKey);
class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.values.delete(k); }
}
const storage = new FakeStorage();
const persisted = persistDoxBenchState(
  replaceBuffer(rekeyed, adopted), storage);

console.log(JSON.stringify({
  dirtyOutline,
  adopted,
  failures,
  rekeyedKey: rekeyed.key,
  rekeyedOutline: rekeyed.buffers.outline,
  rekeyedDocument: rekeyed.buffers.document,
  sameDocumentObject: rekeyed.buffers.document === dirty.buffers.document,
  originalKey: dirty.key,
  persisted,
  storedKeys: [...storage.values.keys()],
  sessionStorageKey: scopeStorageKey(sessionKey),
  originalStorageKey: scopeStorageKey(key),
}));
"""


@pytest.fixture(scope="module")
def save_transition_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench Save-transition probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-save-transition")
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    harness = tmp_path / "save-transition-harness.mjs"
    harness.write_text(_SAVE_TRANSITION_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_adopting_a_saved_base_takes_the_servers_identity_ref_and_revision(
        save_transition_results):
    """FR-038: the buffer follows what the SERVER reported, not the client's
    optimistic guess — and the text that landed becomes the base, so the buffer
    is clean against exactly the bytes that were committed."""
    before = save_transition_results["dirtyOutline"]
    after = save_transition_results["adopted"]
    assert before["dirty"] is True
    assert after["dirty"] is False
    assert after["base_ref"] == "draft/topic-x"
    assert after["base_revision"] == "a" * 40
    assert after["base_hash"] == {"algorithm": "sha256", "hex": "b" * 64}
    assert after["base_content"] == "# Outline edited\n"
    assert after["content"] == before["content"]
    # the buffer's own identity is now the committed one, so a later Discard
    # restores the SAVED text rather than the pre-Save text
    assert after["current_hash"] == after["base_hash"]
    assert after["hash_pending"] is False


def test_adopting_a_saved_base_steps_the_generation_so_an_inflight_hash_is_dropped(
        save_transition_results):
    """The same pairing rule every other transition obeys: a hash still in flight
    over the pre-Save text must not settle onto a buffer whose base has moved."""
    before = save_transition_results["dirtyOutline"]
    after = save_transition_results["adopted"]
    assert after["hash_generation"] == before["hash_generation"] + 1


@pytest.mark.parametrize("case", [
    "nonHexIdentity", "shortIdentity", "wrongAlgorithm", "absentIdentity",
    "blankRef", "blankRevision",
])
def test_an_unverifiable_reported_base_is_refused_rather_than_stored(
        save_transition_results, case):
    """Adoption WRITES state, so it validates by the module's own strict rule. A
    server answer that cannot be verified later is a refusal now — never a
    half-fact quietly persisted, which is precisely how a stale-authority defect
    outlives the action that caused it."""
    failure = save_transition_results["failures"][case]
    assert failure is not None, f"{case} was accepted"
    assert "TypeError" in failure


def test_rekeying_moves_the_scope_key_and_keeps_both_buffers_exactly(
        save_transition_results):
    """FR-038: a first Save creates or joins a session, so the working state now
    belongs to the SESSION ref. Every unsaved change survives the move — a rekey
    that discarded them would be a data-loss bug wearing a refresh's clothes."""
    assert save_transition_results["originalKey"]["ref"] == "main"
    assert save_transition_results["rekeyedKey"] == {
        "repository": "fixture-repo", "ref": "draft/topic-x",
        "tile_kind": "staged", "tile_id": "topic-x",
    }
    assert save_transition_results["rekeyedOutline"] == \
        save_transition_results["dirtyOutline"]
    assert save_transition_results["rekeyedOutline"]["dirty"] is True
    # untouched buffers are not even copied
    assert save_transition_results["sameDocumentObject"] is True


def test_a_rekey_may_not_move_working_state_to_another_repository(
        save_transition_results):
    """A scope key naming another repository is a different corpus, not a rename,
    and the buffers already carry the repository they were loaded from."""
    failure = save_transition_results["failures"]["otherRepository"]
    assert failure is not None
    assert "another repository" in failure


def test_rekeyed_state_persists_under_the_session_scope_key(
        save_transition_results):
    """FR-039's other half: the working state is now stored against the session
    ref, which is what makes the pre-session key safe to clear."""
    assert save_transition_results["persisted"] is True
    assert save_transition_results["storedKeys"] == [
        save_transition_results["sessionStorageKey"]]
    assert save_transition_results["originalStorageKey"] not in \
        save_transition_results["storedKeys"]


# ===========================================================================
# add-doxbench-editing-phase-b, tasks 4.1-4.6: the KEYED BUFFER SET.
#
# `outline` is permanently reserved and carries the session ancestry role its
# commit already had. Every other key is a document buffer keyed by its own
# repository-relative PATH -- which is what makes "load the same document twice"
# impossible by construction rather than by a lookup -- except the ONE reserved
# `document` key, which holds the create flow's not-yet-created artifact until a
# first Save reports the path it created (design D1).
#
# Everything the design claims is UNCHANGED at this layer is exercised here on
# N buffers rather than two: the generation guard is applied per buffer with no
# shared counter, and `beginBufferEdit` / `settleBufferHash` / `adoptSavedBase`
# / `discardBuffer` / `applyProposalToBuffer` are each still one-buffer-in,
# one-buffer-out.
# ===========================================================================

_KEYED_SET_HARNESS = """
import {
  DOCUMENT_KEY_ORDER_RULE,
  DOXBENCH_MAX_LOADED_DOCUMENTS,
  LOAD_REFUSED_ALREADY_LOADED,
  LOAD_REFUSED_BOUND_REACHED,
  OUTLINE_BUFFER_KEY,
  UNBACKED_DOCUMENT_BUFFER_KEY,
  UNLOAD_REFUSED_DIRTY,
  applyProposalToBuffer,
  beginBufferEdit,
  bufferKeyFor,
  bufferKeysInOrder,
  createBufferState,
  createDoxBenchState,
  discardBuffer,
  loadDocumentBuffer,
  loadedDocumentKeys,
  orderedDocumentKeys,
  persistDoxBenchState,
  rekeyDocumentBuffer,
  replaceBuffer,
  restoreDoxBenchState,
  scopeStorageKey,
  setActiveBuffer,
  settleBufferHash,
  unloadDocumentBuffer,
} from './doxbench-state.mjs';

const key = {
  repository: 'fixture-repo',
  ref: 'main',
  tile_kind: 'staged',
  tile_id: 'topic-x',
};
const BASE_REVISION = '1'.repeat(40);

function descriptor(path, content, owned = true) {
  return { path, owned, base_ref: 'main', base_revision: BASE_REVISION, content };
}

async function documentBuffer(path, content, owned = true) {
  return createBufferState({
    kind: 'document', repository: key.repository, ...descriptor(path, content, owned),
  }, {});
}

// ---- the widened construction: outline plus three path-keyed documents ----
const zulu = 'ideation/staging/topic-x/zulu.md';
const alpha = 'ideation/staging/topic-x/alpha.md';
const middle = 'ideation/staging/topic-x/nested/alpha.md';
const state = await createDoxBenchState({
  key,
  outline: descriptor('ideation/staging/topic-x/topic-x.md', '# Outline\\n'),
  documents: {
    [zulu]: descriptor(zulu, '# Zulu\\n'),
    [alpha]: descriptor(alpha, '# Alpha\\n'),
    [middle]: descriptor(middle, '# Middle\\n'),
  },
});

// ---- outline-only construction is legal: an outline alone is a state ----
const outlineOnly = await createDoxBenchState({
  key, outline: descriptor(null, ''),
});

// ---- load a fourth while the first is DIRTY: neither is disturbed ----
const dirtyPending = beginBufferEdit(state.buffers[alpha], '# Alpha edited\\n');
const dirtyAlpha = settleBufferHash(
  dirtyPending.buffer, await dirtyPending.completion).buffer;
const withDirty = replaceBuffer(state, dirtyAlpha);
const fourth = 'ideation/staging/topic-x/delta.md';
const loadedFourth = loadDocumentBuffer(
  withDirty, await documentBuffer(fourth, '# Delta\\n'));

// ---- load one ALREADY loaded: it is selected, never re-read ----
const reloaded = loadDocumentBuffer(
  loadedFourth.state, await documentBuffer(alpha, '# Alpha from source\\n'));

// ---- the bound REFUSES and states the number; nothing is evicted ----
let filling = state;
for (let index = 0; index < DOXBENCH_MAX_LOADED_DOCUMENTS; index += 1) {
  const path = 'ideation/staging/topic-x/fill-' + String(index) + '.md';
  const result = loadDocumentBuffer(filling, await documentBuffer(path, '#\\n'));
  if (!result.loaded) break;
  filling = result.state;
}
const atBound = loadedDocumentKeys(filling).length;
const overBound = loadDocumentBuffer(
  filling, await documentBuffer('ideation/staging/topic-x/one-too-many.md', '#\\n'));

// ---- unload: refused while dirty, permitted with an explicit discard ----
const unloadDirty = unloadDocumentBuffer(withDirty, alpha);
const unloadDiscarded = unloadDocumentBuffer(
  withDirty, alpha, { discardUnsavedEdits: true });
const unloadSelected = unloadDocumentBuffer(
  setActiveBuffer(state, zulu), zulu);

// ---- the reserved unbacked slot, and its RE-KEY on the created path ----
const created = await createDoxBenchState({
  key,
  outline: descriptor('ideation/staging/topic-x/topic-x.md', '# Outline\\n'),
  document: { path: null, owned: true, base_ref: 'main',
              base_revision: BASE_REVISION, content: '# New\\n' },
});
const createdPath = 'ideation/staging/topic-x/created.md';
const rekeyed = rekeyDocumentBuffer(
  setActiveBuffer(created, UNBACKED_DOCUMENT_BUFFER_KEY),
  UNBACKED_DOCUMENT_BUFFER_KEY, createdPath);

// ---- the validator's refusals ----
const failures = {};
function record(name, action) {
  try { action(); failures[name] = null; }
  catch (error) { failures[name] = error.message; }
}
record('keyNotPath', () => setActiveBuffer({
  ...state,
  buffers: { ...state.buffers, 'ideation/staging/topic-x/wrong.md':
    state.buffers[alpha] },
}, OUTLINE_BUFFER_KEY));
record('missingOutline', () => {
  const buffers = { ...state.buffers };
  delete buffers[OUTLINE_BUFFER_KEY];
  return setActiveBuffer({ ...state, buffers }, alpha);
});
record('duplicatePath', () => setActiveBuffer({
  ...state,
  buffers: { ...state.buffers,
    [UNBACKED_DOCUMENT_BUFFER_KEY]: state.buffers[alpha] },
}, OUTLINE_BUFFER_KEY));
record('outlineKeyHoldsDocument', () => setActiveBuffer({
  ...state,
  buffers: { ...state.buffers, [OUTLINE_BUFFER_KEY]: state.buffers[alpha] },
}, alpha));
record('documentKeyHoldsOutline', () => setActiveBuffer({
  ...state,
  buffers: { ...state.buffers, [alpha]: state.buffers[OUTLINE_BUFFER_KEY] },
}, OUTLINE_BUFFER_KEY));
record('outlineUnloaded', () => unloadDocumentBuffer(state, OUTLINE_BUFFER_KEY));
record('rekeyOntoLoaded', () => rekeyDocumentBuffer(state, alpha, zulu));
try {
  await createDoxBenchState({
    key, outline: descriptor(null, ''),
    documents: { outline: descriptor(null, '') },
  });
  failures.reservedOutlineDescriptor = null;
} catch (error) {
  failures.reservedOutlineDescriptor = error.message;
}

// ---- the per-buffer generation guard, applied N times ----
const alphaEdit = beginBufferEdit(state.buffers[alpha], '# A\\n');
const zuluEdit = beginBufferEdit(state.buffers[zulu], '# Z\\n');
const bothPending = replaceBuffer(
  replaceBuffer(state, alphaEdit.buffer), zuluEdit.buffer);
const alphaSettled = settleBufferHash(
  bothPending.buffers[alpha], await alphaEdit.completion);
// The OTHER buffer's completion must not settle this one: content and
// generation are both buffer-scoped, so a cross-buffer settle is stale.
const crossSettle = settleBufferHash(
  bothPending.buffers[alpha], await zuluEdit.completion);

// ---- a PHASE A envelope restores unchanged (design D1, task 4.5) ----
class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.values.delete(k); }
}
const phaseAStorage = new FakeStorage();
// Captured byte-for-byte from a Phase A build's own writer: schema_version 1,
// kind doxbench-working-state, exactly the two reserved keys, and the document
// slot carrying a REAL path -- which is what a Phase A session actually held.
const PHASE_A_ENVELOPE = {
  schema_version: 1,
  kind: 'doxbench-working-state',
  key,
  active_buffer: 'document',
  buffers: {
    outline: {
      path: 'ideation/staging/topic-x/topic-x.md', owned: true,
      base_ref: 'main', base_revision: BASE_REVISION,
      base_content: '# Outline\\n', content: '# Outline\\n', load_state: 'ready',
    },
    document: {
      path: 'ideation/staging/topic-x/detail.md', owned: true,
      base_ref: 'main', base_revision: BASE_REVISION,
      base_content: '# Detail\\n', content: '# Detail edited\\n',
      load_state: 'ready',
    },
  },
};
phaseAStorage.setItem(scopeStorageKey(key), JSON.stringify(PHASE_A_ENVELOPE));
const phaseARestored = await restoreDoxBenchState(key, phaseAStorage, {});

// ---- the widened set round-trips through persist/restore ----
const roundTripStorage = new FakeStorage();
const roundTripWritten = persistDoxBenchState(
  setActiveBuffer(withDirty, zulu), roundTripStorage);
const roundTripped = await restoreDoxBenchState(key, roundTripStorage, {});
// A stored document key that disagrees with its own stored path is refused.
const disagreeingStorage = new FakeStorage();
disagreeingStorage.setItem(scopeStorageKey(key), JSON.stringify({
  ...PHASE_A_ENVELOPE,
  active_buffer: 'outline',
  buffers: {
    outline: PHASE_A_ENVELOPE.buffers.outline,
    'ideation/staging/topic-x/other.md': PHASE_A_ENVELOPE.buffers.document,
  },
}));
const disagreeing = await restoreDoxBenchState(key, disagreeingStorage, {});

// ---- Apply still targets exactly ONE buffer, by key ----
const proposal = {
  base_hash: state.buffers[zulu].current_hash.hex,
  content: '# Zulu proposed\\n',
};
const applied = applyProposalToBuffer(state.buffers[zulu], proposal);
const appliedState = replaceBuffer(state, applied.buffer);
const discardedOne = replaceBuffer(
  appliedState, discardBuffer(appliedState.buffers[zulu]));

console.log(JSON.stringify({
  orderRule: DOCUMENT_KEY_ORDER_RULE,
  bound: DOXBENCH_MAX_LOADED_DOCUMENTS,
  reservedKeys: [OUTLINE_BUFFER_KEY, UNBACKED_DOCUMENT_BUFFER_KEY],
  keys: Object.keys(state.buffers),
  keysInOrder: bufferKeysInOrder(state),
  documentKeys: loadedDocumentKeys(state),
  orderedFromUnsorted: orderedDocumentKeys([zulu, OUTLINE_BUFFER_KEY, alpha, middle]),
  bufferKeyForDocument: bufferKeyFor(state.buffers[alpha]),
  bufferKeyForUnbacked: bufferKeyFor(created.buffers[UNBACKED_DOCUMENT_BUFFER_KEY]),
  bufferKeyForOutline: bufferKeyFor(state.buffers[OUTLINE_BUFFER_KEY]),
  outlineOnly: { keys: Object.keys(outlineOnly.buffers),
                 active: outlineOnly.active_buffer },
  load: {
    key: loadedFourth.key,
    loaded: loadedFourth.loaded,
    active: loadedFourth.state.active_buffer,
    keys: Object.keys(loadedFourth.state.buffers),
    firstStillDirty: loadedFourth.state.buffers[alpha].dirty,
    firstStillEdited: loadedFourth.state.buffers[alpha].content,
  },
  reload: {
    loaded: reloaded.loaded,
    refusal: reloaded.refusal,
    key: reloaded.key,
    active: reloaded.state.active_buffer,
    contentUnchanged: reloaded.state.buffers[alpha].content,
    dirtyPreserved: reloaded.state.buffers[alpha].dirty,
    keyCount: Object.keys(reloaded.state.buffers).length,
  },
  boundRefusal: {
    atBound,
    loaded: overBound.loaded,
    refusal: overBound.refusal,
    bound: overBound.bound,
    measured: overBound.measured,
    nothingEvicted: loadedDocumentKeys(overBound.state).length,
  },
  unload: {
    dirtyRefused: unloadDirty.unloaded,
    dirtyReason: unloadDirty.refusal,
    dirtyStillHeld: Object.keys(unloadDirty.state.buffers).includes(alpha),
    discarded: unloadDiscarded.unloaded,
    discardedKeys: Object.keys(unloadDiscarded.state.buffers),
    othersUntouched: unloadDiscarded.state.buffers[zulu].content,
    selectedFellBackToOutline: unloadSelected.state.active_buffer,
  },
  rekey: {
    beforeKeys: Object.keys(created.buffers),
    afterKeys: Object.keys(rekeyed.buffers),
    path: rekeyed.buffers[createdPath].path,
    active: rekeyed.active_buffer,
    generationStepped: rekeyed.buffers[createdPath].hash_generation
      > created.buffers[UNBACKED_DOCUMENT_BUFFER_KEY].hash_generation,
    reservedKeyFree: Object.prototype.hasOwnProperty.call(
      rekeyed.buffers, UNBACKED_DOCUMENT_BUFFER_KEY),
  },
  failures,
  generations: {
    alphaGeneration: bothPending.buffers[alpha].hash_generation,
    zuluGeneration: bothPending.buffers[zulu].hash_generation,
    outlineGeneration: bothPending.buffers[OUTLINE_BUFFER_KEY].hash_generation,
    alphaSettled: alphaSettled.applied,
    crossSettleApplied: crossSettle.applied,
    crossSettleReason: crossSettle.reason,
  },
  phaseA: phaseARestored === null ? null : {
    keys: Object.keys(phaseARestored.buffers),
    active: phaseARestored.active_buffer,
    documentPath: phaseARestored.buffers.document.path,
    documentDirty: phaseARestored.buffers.document.dirty,
    documentContent: phaseARestored.buffers.document.content,
    outlineClean: phaseARestored.buffers.outline.dirty,
  },
  roundTrip: {
    written: roundTripWritten,
    keys: roundTripped === null ? null : Object.keys(roundTripped.buffers),
    active: roundTripped === null ? null : roundTripped.active_buffer,
    dirtyPreserved: roundTripped === null
      ? null : roundTripped.buffers[alpha].dirty,
  },
  disagreeingRestore: disagreeing,
  apply: {
    appliedKeys: Object.keys(appliedState.buffers),
    appliedDirty: appliedState.buffers[zulu].dirty,
    othersClean: appliedState.buffers[alpha].dirty,
    discardedBack: discardedOne.buffers[zulu].content,
    discardedClean: discardedOne.buffers[zulu].dirty,
  },
  loadRefusalCodes: {
    alreadyLoaded: LOAD_REFUSED_ALREADY_LOADED,
    bound: LOAD_REFUSED_BOUND_REACHED,
    dirtyUnload: UNLOAD_REFUSED_DIRTY,
  },
}));
"""


@pytest.fixture(scope="module")
def keyed_set_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench keyed-set probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-keyed-set")
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    harness = tmp_path / "keyed-set-harness.mjs"
    harness.write_text(_KEYED_SET_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_buffer_set_is_keyed_by_path_with_outline_reserved(keyed_set_results):
    """Task 4.1/4.2: `outline` reserved, every other key a document's own path."""
    assert keyed_set_results["reservedKeys"] == ["outline", "document"]
    assert sorted(keyed_set_results["keys"]) == sorted([
        "outline",
        "ideation/staging/topic-x/alpha.md",
        "ideation/staging/topic-x/nested/alpha.md",
        "ideation/staging/topic-x/zulu.md",
    ])
    assert keyed_set_results["bufferKeyForOutline"] == "outline"
    assert keyed_set_results["bufferKeyForDocument"] == \
        "ideation/staging/topic-x/alpha.md"
    # A not-yet-created buffer has no path to be keyed by, so it takes the ONE
    # reserved slot.
    assert keyed_set_results["bufferKeyForUnbacked"] == "document"


def test_an_outline_alone_is_a_legal_working_state(keyed_set_results):
    """`createDoxBenchState` builds `outline` plus ZERO or more documents: a
    scope opened with nothing loaded is a state, not a defect."""
    assert keyed_set_results["outlineOnly"]["keys"] == ["outline"]
    assert keyed_set_results["outlineOnly"]["active"] == "outline"


def test_the_document_order_is_declared_and_deterministic(keyed_set_results):
    """Design D3 point 4: "any order" constrains the CONTRACT, not the code.
    The realization DECLARES lexicographic-by-key so the commit series is
    reproducible, and the outline always leads because its commit is the
    ancestry."""
    assert keyed_set_results["orderRule"] == (
        "ascending lexicographic by buffer key (UTF-16 code unit)")
    assert keyed_set_results["documentKeys"] == [
        "ideation/staging/topic-x/alpha.md",
        "ideation/staging/topic-x/nested/alpha.md",
        "ideation/staging/topic-x/zulu.md",
    ]
    assert keyed_set_results["keysInOrder"][0] == "outline"
    assert keyed_set_results["keysInOrder"][1:] == keyed_set_results["documentKeys"]
    # The order is a function of the KEYS alone, never of insertion order.
    assert keyed_set_results["orderedFromUnsorted"] == \
        keyed_set_results["documentKeys"]


def test_loading_a_second_document_disturbs_neither_the_first_nor_its_edits(
        keyed_set_results):
    """The delta's `A second document is loaded` scenario: both buffers exist
    under their own path keys with their own dirty state and base identity, and
    loading the second replaces, discards, and flushes nothing."""
    load = keyed_set_results["load"]
    assert load["loaded"] is True
    assert load["key"] == "ideation/staging/topic-x/delta.md"
    assert load["active"] == "ideation/staging/topic-x/delta.md"
    assert len(load["keys"]) == 5
    assert load["firstStillDirty"] is True
    assert load["firstStillEdited"] == "# Alpha edited\n"


def test_loading_an_already_loaded_document_selects_it_and_never_re_reads_it(
        keyed_set_results):
    """The delta's `A document already loaded is loaded again` scenario:
    re-reading from source would silently discard the buffer's unsaved text, so
    the existing buffer becomes the selected one instead."""
    reload = keyed_set_results["reload"]
    assert reload["loaded"] is False
    assert reload["refusal"] == "already_loaded"
    assert reload["key"] == "ideation/staging/topic-x/alpha.md"
    assert reload["active"] == "ideation/staging/topic-x/alpha.md"
    assert reload["contentUnchanged"] == "# Alpha edited\n"
    assert reload["dirtyPreserved"] is True
    assert reload["keyCount"] == 5


def test_the_loaded_set_bound_refuses_and_states_the_number(keyed_set_results):
    """Design D6: the bound REFUSES with the measured bound stated. There is no
    eviction anywhere, because every loaded buffer may hold unsaved work and a
    policy that evicts to make room is a policy that discards human text."""
    refusal = keyed_set_results["boundRefusal"]
    assert refusal["atBound"] == keyed_set_results["bound"]
    assert refusal["loaded"] is False
    assert refusal["refusal"] == "loaded_set_bound_reached"
    assert refusal["bound"] == keyed_set_results["bound"]
    assert refusal["measured"] == keyed_set_results["bound"]
    assert refusal["nothingEvicted"] == keyed_set_results["bound"]


def test_unloading_a_dirty_document_refuses_until_the_discard_is_explicit(
        keyed_set_results):
    """The delta's `A dirty document is unloaded` scenario: dropping the buffer
    destroys unsaved work exactly as Cancel does, so it refuses unless the
    caller states the discard."""
    unload = keyed_set_results["unload"]
    assert unload["dirtyRefused"] is False
    assert unload["dirtyReason"] == "unsaved_edits"
    assert unload["dirtyStillHeld"] is True
    assert unload["discarded"] is True
    assert "ideation/staging/topic-x/alpha.md" not in unload["discardedKeys"]
    assert unload["othersUntouched"] == "# Zulu\n"
    # Unloading the SELECTED buffer falls back to the reserved outline, which is
    # always present -- never to an absent key.
    assert unload["selectedFellBackToOutline"] == "outline"


def test_the_reserved_unbacked_buffer_is_re_keyed_to_the_created_path(
        keyed_set_results):
    """Task 4.4 and the delta's `An unbacked document buffer is first saved`
    scenario: the reserved key is freed WITHOUT carrying anything from the buffer
    that left it, and the generation is stepped as every base transition steps
    it, so a hash still in flight over the older text is dropped."""
    rekey = keyed_set_results["rekey"]
    assert rekey["beforeKeys"] == ["outline", "document"]
    assert sorted(rekey["afterKeys"]) == sorted([
        "outline", "ideation/staging/topic-x/created.md"])
    assert rekey["path"] == "ideation/staging/topic-x/created.md"
    assert rekey["active"] == "ideation/staging/topic-x/created.md"
    assert rekey["generationStepped"] is True
    assert rekey["reservedKeyFree"] is False


def test_the_keyed_set_validator_refuses_every_disagreeing_shape(keyed_set_results):
    """Task 4.2: the exactly-two-keys throw is REPLACED, not relaxed into
    silence. Each clause below is its own refusal."""
    failures = keyed_set_results["failures"]
    assert "must equal its own path" in failures["keyNotPath"]
    assert "reserved outline buffer" in failures["missingOutline"]
    assert "same document path" in failures["duplicatePath"]
    assert "must hold the outline buffer" in failures["outlineKeyHoldsDocument"]
    assert "must hold a document buffer" in failures["documentKeyHoldsOutline"]
    assert "reserved and cannot be unloaded" in failures["outlineUnloaded"]
    assert "another loaded document" in failures["rekeyOntoLoaded"]
    assert "reserved for the outline buffer" in \
        failures["reservedOutlineDescriptor"]


def test_the_staleness_guard_is_applied_per_buffer_and_shares_no_counter(
        keyed_set_results):
    """Task 4.6: widening the set means applying the SAME buffer-scoped guard N
    times. No force path, no cross-buffer settle, no shared generation."""
    generations = keyed_set_results["generations"]
    assert generations["alphaGeneration"] == 1
    assert generations["zuluGeneration"] == 1
    # Editing two documents left the outline's own counter exactly where it was.
    assert generations["outlineGeneration"] == 0
    assert generations["alphaSettled"] is True
    # One buffer's completion can never settle another's.
    assert generations["crossSettleApplied"] is False
    assert generations["crossSettleReason"] == "stale_generation"


def test_a_phase_a_session_envelope_restores_unchanged(keyed_set_results):
    """Task 4.5 and design D1's migration-free property, proven against a
    CAPTURED Phase A envelope: `{outline, document}` with a real path under the
    reserved key, `schema_version` 1, restored with its unsaved edit intact and
    no migration branch anywhere."""
    phase_a = keyed_set_results["phaseA"]
    assert phase_a is not None, "a Phase A envelope must restore, not be discarded"
    assert sorted(phase_a["keys"]) == ["document", "outline"]
    assert phase_a["active"] == "document"
    assert phase_a["documentPath"] == "ideation/staging/topic-x/detail.md"
    assert phase_a["documentContent"] == "# Detail edited\n"
    assert phase_a["documentDirty"] is True
    assert phase_a["outlineClean"] is False


def test_the_widened_set_round_trips_and_a_disagreeing_key_is_refused(
        keyed_set_results):
    round_trip = keyed_set_results["roundTrip"]
    assert round_trip["written"] is True
    assert len(round_trip["keys"]) == 4
    assert round_trip["active"] == "ideation/staging/topic-x/zulu.md"
    assert round_trip["dirtyPreserved"] is True
    # An envelope whose keys disagree with its own buffers is refused rather
    # than reconciled -- the record cannot be trusted to say which file the text
    # belongs to, and a refused restore degrades to absent.
    assert keyed_set_results["disagreeingRestore"] is None


def test_apply_and_discard_still_touch_exactly_one_buffer(keyed_set_results):
    """Design's central claim about this layer: the per-buffer primitives are
    unchanged, so N buffers is the same primitive applied N times."""
    apply = keyed_set_results["apply"]
    assert len(apply["appliedKeys"]) == 4
    assert apply["appliedDirty"] is True
    assert apply["othersClean"] is False
    assert apply["discardedBack"] == "# Zulu\n"
    assert apply["discardedClean"] is False
