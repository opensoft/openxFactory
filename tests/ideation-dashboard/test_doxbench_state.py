"""Pure two-buffer state and generation-safe hashing for doxBench."""

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


def test_state_contains_exactly_outline_and_document_buffers(state_results):
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


def test_buffer_replacement_is_targeted_and_active_tab_is_independent(state_results):
    replacement = state_results["replacement"]
    with_outline = replacement["withOutline"]
    assert with_outline["buffers"]["outline"]["content"] == "# Revised outline\n"
    assert with_outline["buffers"]["outline"]["dirty"] is True
    assert with_outline["buffers"]["document"]["content"] == "# Document\n"
    assert with_outline["active_buffer"] == "outline"
    assert replacement["activeDocument"]["active_buffer"] == "document"


def test_invalid_buffer_shapes_and_third_primary_buffer_are_refused(state_results):
    failures = state_results["failures"]
    assert failures["badKind"] == {
        "name": "TypeError",
        "message": "buffer kind must be outline or document",
    }
    assert "same repository" in failures["wrongRepository"]["message"]
    assert failures["thirdBuffer"] == {
        "name": "TypeError",
        "message": "active buffer must be outline or document",
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
