"""SELECTING A DOCUMENT SWITCHES THE TRANSCRIPT TO ITS THREAD
(add-doxbench-editing-phase-b task 7.2's thread half, completed at §11).

The selection half landed with §7 and is pinned in `test_doxbench_composition.py`;
what waited on §9's sidecar store — and therefore on this slice — is the
TRANSCRIPT switch. Its two halves are pinned here: the pure model function that
adopts a thread's turns, driven through Node, and the ONE call site in the rail,
asserted against the view's own source (there is no second answer to "which
thread is this rail showing", which is the second state authority the task
forbids).
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
CHAT_MODEL_JS = VIEWS / "doxbench-chat-model.js"
CHAT_VIEW_JS = VIEWS / "doxbench-chat.js"

_HARNESS = """
import {
  MAX_TRANSCRIPT_TURNS, createChatState, adoptCatalog, settleTurnSuccess,
  beginTurn, editComposer, selectModel, transcriptWindow, proposalsOf,
  adoptThreadTranscript,
} from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved authoring model",
                provider_class: "on-tenant", available: true,
                input_limit_bytes: 800000, output_limit_bytes: 900000,
                data_handling: "Processed in the approved tenant boundary" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
const success = (prose) => ({
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "Processed in the approved tenant boundary" },
  bound_buffer: "ideation/staging/t/a.md",
  observed_hashes: { outline: "a".repeat(64) },
  assistant_prose: prose,
  proposals: [{ target: "outline", base_hash: "a".repeat(64),
                summary: "s", content: "c" }] });

// A lived-through conversation on document A, complete with a proposal.
let a = adoptCatalog(createChatState(KEY), ENVELOPE);
a = selectModel(a, "model-a");
a = editComposer(a, "what about A?");
a = beginTurn(a);
a = settleTurnSuccess(a, success("A's answer"));
out.before = {
  turns: transcriptWindow(a).map((t) => t.content),
  proposals: Object.keys(proposalsOf(a)).length,
};

// Selecting document B adopts B's OWN thread.
const b = adoptThreadTranscript(a, [
  { turn_id: "b1", model: "model-a", bound_buffer_key: "b.md",
    human: "what about B?", assistant: "B's answer" },
]);
out.switched = {
  turns: transcriptWindow(b).map((t) => t.content),
  roles: transcriptWindow(b).map((t) => t.role),
  proposals: Object.keys(proposalsOf(b)).length,
  failure: b.lastFailure,
  // the rest of the rail is UNTOUCHED: this is not a re-key
  model: b.selectedModelId,
  models: (b.models || []).length,
  key: b.key.tile_id,
  frozen: Object.isFrozen(b),
};

// A document with NO thread adopts an EMPTY transcript rather than leaving the
// previous document's conversation on screen.
const empty = adoptThreadTranscript(a, []);
out.empty = { turns: transcriptWindow(empty).length,
              model: empty.selectedModelId };

// A thread longer than the DISPLAY bound is evicted oldest-pair-first, exactly
// as a lived-through conversation would be.
const long = adoptThreadTranscript(a, Array.from({ length: 40 }, (_, n) => ({
  turn_id: "t" + n, model: "model-a", bound_buffer_key: "b.md",
  human: "q" + n, assistant: "a" + n })));
out.long = { turns: transcriptWindow(long).length,
             newest: transcriptWindow(long).slice(-1)[0].content,
             bound: MAX_TRANSCRIPT_TURNS };

// A non-array, a null, and a row that is not an object are all the empty
// transcript — a transport that answers oddly never invents a conversation.
out.junk = [null, undefined, "nope", [null, 3]].map(
  (value) => transcriptWindow(adoptThreadTranscript(a, value)).length);

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def switch_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the thread-switch probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-thread-switch")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "switch-harness.mjs"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_previous_document_s_conversation_really_was_on_screen(switch_results):
    """The fixture's own precondition: without it, "the transcript switched"
    could pass against a state that never held anything."""
    assert switch_results["before"]["turns"] == ["what about A?", "A's answer"]
    assert switch_results["before"]["proposals"] == 1


def test_selecting_a_document_shows_THAT_document_s_thread(switch_results):
    switched = switch_results["switched"]
    assert switched["turns"] == ["what about B?", "B's answer"]
    assert switched["roles"] == ["human", "assistant"]
    assert switched["frozen"] is True


def test_the_previous_document_s_proposals_and_failure_do_not_follow(
        switch_results):
    """A proposal targets a buffer the human is no longer looking at, and a
    failure is a fact about the previous document's turn."""
    assert switch_results["switched"]["proposals"] == 0
    assert switch_results["switched"]["failure"] is None


def test_the_switch_is_not_a_RE_KEY_and_leaves_the_plane_s_facts_alone(
        switch_results):
    """`rekeyChatState` clears the catalog and the model selection because the
    SCOPE moved. Selecting another document inside one scope moves neither."""
    switched = switch_results["switched"]
    assert switched["model"] == "model-a"
    assert switched["models"] == 1
    assert switched["key"] == "ideation-governance"


def test_a_document_with_no_thread_shows_an_EMPTY_transcript(switch_results):
    assert switch_results["empty"]["turns"] == 0
    assert switch_results["empty"]["model"] == "model-a"


def test_a_thread_longer_than_the_display_bound_is_evicted_oldest_first(
        switch_results):
    long = switch_results["long"]
    assert long["turns"] == long["bound"]
    assert long["newest"] == "a39"


def test_an_odd_answer_never_invents_a_conversation(switch_results):
    assert switch_results["junk"] == [0, 0, 0, 0]


# ---------------------------------------------------------------------------
# the RAIL's one call site (no second state authority)
# ---------------------------------------------------------------------------


def test_the_rail_switches_the_thread_from_exactly_one_place():
    view = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert view.count("switchThread(") == 2, (
        "one definition and one call site; a second call site would be a "
        "second answer to which thread this rail is showing")
    assert "await switchThread(wanted);" in view
    # …and the selection still moves FIRST, through the canvas's own primitive
    selection = view.split("loadedSelect.addEventListener", 1)[1]
    assert selection.index("await select(wanted)") < selection.index(
        "await switchThread(wanted)")


def test_the_TODO_that_named_this_task_is_gone():
    view = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "TODO(add-doxbench-editing-phase-b tasks.md §9)" not in view


def test_the_rail_reads_a_thread_and_never_writes_one():
    view = CHAT_VIEW_JS.read_text(encoding="utf-8")
    for forbidden in ("saveThread", "writeThread", "postThread", "method: \"POST\""):
        assert forbidden not in view, forbidden


def test_the_shell_supplies_the_thread_transport_to_the_rail():
    workbench = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    assert "loadThread:" in workbench
    assert "doxbench.thread(" in workbench


def test_an_absent_thread_transport_leaves_the_rail_exactly_as_it_was():
    """The seam is OPTIONAL: a plane with no thread transport keeps the pre-§11
    behaviour, which is what lets the editor-only posture stand unchanged."""
    view = CHAT_VIEW_JS.read_text(encoding="utf-8")
    body = view.split("async function switchThread(", 1)[1].split("\n  }", 1)[0]
    assert 'if (typeof load !== "function") return;' in body
