"""T044 (US2): browser chat state/view behaviors — catalog adoption, composer
preservation, subsequent-edit currency, bounded transcript, and abort — for
the pure chat model `doxbench-chat-model.js` (T052) and, at the seam level,
the dispatch discipline `doxbench-chat.js` (T053/T054) must honour.

RED-FIRST: authored before either module exists (the module-missing Node
failure IS the red evidence), exactly like the earlier doxBench view suites.
One Node harness run produces a single JSON blob; every test asserts into it.

Wire facts pinned here come from the RELEASED contract-v1.27 chat-turn
schema: transcript turns spell `{role, content}` (the server-side dataclass's
`.text` is an internal name, not the wire), and an empty catalog `models`
array is a SUCCESS (editor-only posture), never an error.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")

CHAT_MODEL_JS = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" /
                 "views" / "doxbench-chat-model.js")

_HARNESS = """
import {
  DOXBENCH_CHAT_STATE_VERSION, DOXBENCH_CHAT_STATE_KIND,
  MAX_WORKING_SUBJECT_BYTES, MAX_MESSAGE_BYTES,
  MAX_TRANSCRIPT_TURNS, MAX_TRANSCRIPT_BYTES,
  createChatState, adoptCatalog, selectModel, editSubject, editComposer,
  beginTurn, settleTurnSuccess, settleTurnFailure, abortTurn,
  transcriptWindow, rekeyChatState,
} from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const OTHER_KEY = { repository: "fixture-repo", ref: "main",
                    tile_kind: "staged", tile_id: "keyword-lens" };
const ENTRY = { model_id: "model-a", label: "Approved authoring model",
                provider_class: "on-tenant", available: true,
                input_limit_bytes: 800000, output_limit_bytes: 900000,
                data_handling: "Processed in the approved tenant boundary" };
const OFF_ENTRY = { ...ENTRY, model_id: "model-off", available: false };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY, OFF_ENTRY] };
const EMPTY_ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                         models: [] };
const success = (prose) => ({
  schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: "a".repeat(64), document: "b".repeat(64) },
  assistant_prose: prose, proposals: [] });
const FAILURE = { schema_version: 1, kind: "workbench-chat-turn-failure",
                  client_turn_id: "t-1", error: "model_failed",
                  message: "the model request failed" };

// ---- constants / catalog adoption ----
out.constants = { version: DOXBENCH_CHAT_STATE_VERSION,
                  kind: DOXBENCH_CHAT_STATE_KIND,
                  subject: MAX_WORKING_SUBJECT_BYTES,
                  message: MAX_MESSAGE_BYTES,
                  turns: MAX_TRANSCRIPT_TURNS,
                  transcriptBytes: MAX_TRANSCRIPT_BYTES };
let s = createChatState(KEY);
out.freshFrozen = Object.isFrozen(s);
const adopted = adoptCatalog(s, ENVELOPE);
out.adopted = { models: adopted.models.length,
                unchangedOriginal: s.models === null || s.models.length === 0,
                pure: adopted !== s };
out.emptyIsEditorOnly = (() => {
  const e = adoptCatalog(s, EMPTY_ENVELOPE);
  return { models: e.models.length, failed: Boolean(e.lastFailure) };
})();
out.malformedRefused = (() => {
  const bad = adoptCatalog(s, { nope: true });
  return { models: bad.models === null ? null : bad.models.length };
})();
// ---- selection ----
const sel = selectModel(adopted, "model-a");
out.selected = sel.selectedModelId;
out.unavailableNotSelectable =
  selectModel(adopted, "model-off").selectedModelId === null &&
  selectModel(adopted, "no-such").selectedModelId === null;
// ---- composer bounds + preservation ----
let c = editComposer(sel, "What should we close next?");
out.composerHeld = c.composer;
out.overBoundRefused = (() => {
  const big = editComposer(c, "x".repeat(MAX_MESSAGE_BYTES + 1));
  return big.composer === c.composer;
})();
out.byteNotCodepoint = (() => {
  const s3 = editComposer(c, "\\u20ac".repeat(Math.ceil(MAX_MESSAGE_BYTES / 3) + 1));
  return s3.composer === c.composer;  // 3-byte chars: over in bytes, under in code points
})();
const subj = editSubject(c, "Working subject");
out.subjectHeld = subj.workingSubject;
// ---- one-in-flight + abort + failure preservation ----
let t = beginTurn(subj);
out.inFlight = t.phase;
out.secondBeginRefused = beginTurn(t) === t;
out.composerDuringFlight = t.composer;
const aborted = abortTurn(t);
out.abort = { phase: aborted.phase, composer: aborted.composer,
              transcript: transcriptWindow(aborted).length };
const failed = settleTurnFailure(beginTurn(subj), FAILURE);
out.failure = { phase: failed.phase, composer: failed.composer,
                error: failed.lastFailure && failed.lastFailure.error,
                message: failed.lastFailure && failed.lastFailure.message,
                transcript: transcriptWindow(failed).length };
// ---- success + transcript shape ----
const done = settleTurnSuccess(beginTurn(subj), success("grounded answer"));
const win = transcriptWindow(done);
out.success = { phase: done.phase, composer: done.composer,
                turns: win.length, roles: win.map((x) => x.role),
                fields: win.length ? Object.keys(win[0]).sort() : [],
                human: win.length ? win[0].content : null,
                assistant: win.length > 1 ? win[1].content : null };
// ---- subsequent-edit: composer editable again after settle ----
out.subsequentEdit = editComposer(done, "follow-up question").composer;
// ---- bounded transcript: eviction by whole turns ----
let b = subj;
for (let i = 0; i < MAX_TRANSCRIPT_TURNS; i += 1) {
  b = settleTurnSuccess(beginTurn(editComposer(b, "q" + i)),
                        success("a".repeat(6000)));
}
const bwin = transcriptWindow(b);
out.bounded = {
  turns: bwin.length,
  withinTurnCap: bwin.length <= MAX_TRANSCRIPT_TURNS,
  bytes: bwin.reduce((n, x) => n + Buffer.byteLength(x.content, "utf8"), 0),
  evenPairs: bwin.length % 2 === 0,
};
// ---- rekey isolation ----
const rk = rekeyChatState(b, OTHER_KEY);
out.rekey = { transcript: transcriptWindow(rk).length,
              composer: rk.composer, selected: rk.selectedModelId,
              sameKeyKeeps: rekeyChatState(b, KEY) === b ||
                            transcriptWindow(rekeyChatState(b, KEY)).length ===
                            bwin.length };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def chat_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench chat-model probe")
    if not CHAT_MODEL_JS.exists():
        pytest.fail("doxbench-chat-model.js does not exist yet (T052 red)")
    tmp_path = tmp_path_factory.mktemp("doxbench-chat")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "chat-harness.mjs"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_versioned_constants_match_the_plan_bounds(chat_results):
    c = chat_results["constants"]
    assert c["version"] == 1
    assert c["kind"] == "doxbench-chat-state"
    assert c["subject"] == 512
    assert c["message"] == 16_384
    assert c["turns"] == 20
    assert c["transcriptBytes"] == 64_000


def test_catalog_adoption_is_pure_and_empty_is_editor_only_success(chat_results):
    assert chat_results["freshFrozen"] is True
    assert chat_results["adopted"] == {
        "models": 2, "unchangedOriginal": True, "pure": True}
    assert chat_results["emptyIsEditorOnly"] == {"models": 0, "failed": False}
    assert chat_results["malformedRefused"]["models"] in (None, 0)


def test_only_available_models_are_selectable(chat_results):
    assert chat_results["selected"] == "model-a"
    assert chat_results["unavailableNotSelectable"] is True


def test_composer_bounds_measure_utf8_bytes_and_refuse_never_truncate(chat_results):
    assert chat_results["composerHeld"] == "What should we close next?"
    assert chat_results["overBoundRefused"] is True
    assert chat_results["byteNotCodepoint"] is True
    assert chat_results["subjectHeld"] == "Working subject"


def test_one_turn_in_flight_and_the_composer_is_preserved_throughout(chat_results):
    assert chat_results["inFlight"] == "in_flight"
    assert chat_results["secondBeginRefused"] is True
    assert chat_results["composerDuringFlight"] == "What should we close next?"


def test_abort_returns_to_idle_preserving_composer_and_appending_nothing(chat_results):
    assert chat_results["abort"] == {
        "phase": "idle", "composer": "What should we close next?",
        "transcript": 0}


def test_a_fixed_failure_preserves_the_composer_verbatim_fr016(chat_results):
    f = chat_results["failure"]
    assert f["phase"] == "idle"
    assert f["composer"] == "What should we close next?"
    assert f["error"] == "model_failed"
    assert f["message"] == "the model request failed"
    assert f["transcript"] == 0


def test_success_appends_released_shaped_turns_and_clears_the_composer(chat_results):
    s = chat_results["success"]
    assert s["phase"] == "idle"
    assert s["composer"] == ""
    assert s["turns"] == 2
    assert s["roles"] == ["human", "assistant"]
    # RELEASED transcript_turn spelling: role/content (never `text`).
    assert s["fields"] == ["content", "role"]
    assert s["human"] == "What should we close next?"
    assert s["assistant"] == "grounded answer"


def test_the_composer_is_editable_again_after_settlement(chat_results):
    assert chat_results["subsequentEdit"] == "follow-up question"


def test_the_transcript_stays_within_both_bounds_evicting_whole_turns(chat_results):
    b = chat_results["bounded"]
    assert b["withinTurnCap"] is True
    assert b["bytes"] <= 64_000
    assert b["evenPairs"] is True
    assert b["turns"] >= 2


def test_rekey_isolates_browser_session_state_per_scope_fr011(chat_results):
    r = chat_results["rekey"]
    assert r["transcript"] == 0
    assert r["composer"] == ""
    assert r["selected"] is None
    assert r["sameKeyKeeps"] is True


# ---------------------------------------------------------------------------
# T053/T054 (red-first): the chat view's SEAM surface — the pure released
# wire-request builder and the injected-transport dispatch orchestrator in
# doxbench-chat.js. DOM assembly is deliberately thin and textContent-only;
# behavior is pinned here at the seams, DOM-free, exactly like the editor's
# discipline. The module imports ONLY doxbench-chat-model.js (+ viewer seam).
# ---------------------------------------------------------------------------

CHAT_VIEW_JS = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" /
                "views" / "doxbench-chat.js")

_VIEW_HARNESS = """
import { buildTurnRequest, createTurnDispatcher }
  from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer, editSubject,
         transcriptWindow }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved authoring model",
                provider_class: "on-tenant", available: true,
                input_limit_bytes: 800000, output_limit_bytes: 900000,
                data_handling: "Processed in the approved tenant boundary" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
const bufferOf = (kind) => ({
  kind, path: kind === "outline" ? "docs/outline.md" : null,
  owned: true, base_ref: "main", base_revision: "r1",
  base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  content: "# " + kind, dirty: kind === "outline",
});
const editorState = { buffers: { outline: bufferOf("outline"),
                                 document: bufferOf("document") } };
let s = editComposer(editSubject(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"),
  "Working subject"), "What next?");

// ---- pure request builder ----
const req = buildTurnRequest({
  state: s, scopeKey: KEY, clientTurnId: "turn-x1",
  activeDocumentPath: null, editorState });
out.request = {
  keys: Object.keys(req).sort(),
  version: req.schema_version, kind: req.kind,
  turnId: req.client_turn_id, model: req.model_id,
  subject: req.working_subject, message: req.message,
  scopeKeys: Object.keys(req.scope).sort(),
  bufferKinds: req.buffers.map((b) => b.kind),
  bufferKeys: Object.keys(req.buffers[0]).sort(),
  outlineHash: req.buffers[0].content_hash,
  outlineBase: req.buffers[0].base_hash,
  docPath: req.buffers[1].path,
  transcript: req.transcript,
  lastAssistant: req.last_assistant_turn_id,
};

// ---- dispatcher: success / failure / refusal / one-in-flight ----
const success = { schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "turn-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
  assistant_prose: "grounded answer", proposals: [] };
const failure = { schema_version: 1, kind: "workbench-chat-turn-failure",
  client_turn_id: "turn-1", error: "model_failed",
  message: "the model request failed" };

// T104 F2: a turn the RELEASED envelope would accept names a document
// (`active_document_path` is a non-empty confined_path there -- only the
// BUFFER path is nullable), so the dispatch scenarios below carry one. The
// pure builder above keeps the null-path document buffer it always had.
const DOC_PATH = "docs/detail.md";
const editorStateWithDoc = { buffers: {
  outline: bufferOf("outline"),
  document: { ...bufferOf("document"), path: DOC_PATH } } };

async function run(payload, opts = {}) {
  let sent = null;
  const transports = { chatTurn: async (body) => {
    sent = body;
    if (opts.reject) throw new Error("transport refused pre-flight");
    return { ok: payload.kind.endsWith("success"), status: 200, payload };
  } };
  const dispatcher = createTurnDispatcher({
    transports, turnIdFactory: (n) => "turn-" + n });
  const result = await dispatcher.submit(s, {
    scopeKey: KEY, activeDocumentPath: DOC_PATH,
    editorState: editorStateWithDoc });
  return { sent, result };
}
{
  const { sent, result } = await run(success);
  out.success = {
    settled: result.state.phase, composer: result.state.composer,
    turns: transcriptWindow(result.state).length,
    sentKind: sent.kind, sentTurnId: sent.client_turn_id,
    freshBuffers: sent.buffers[0].content_hash === "d".repeat(64),
  };
}
{
  const { result } = await run(failure);
  out.failure = { settled: result.state.phase,
                  composer: result.state.composer,
                  error: result.state.lastFailure.error,
                  turns: transcriptWindow(result.state).length };
}
{
  const { result } = await run(success, { reject: true });
  out.refusal = { settled: result.state.phase,
                  composer: result.state.composer,
                  hasFailure: Boolean(result.state.lastFailure),
                  turns: transcriptWindow(result.state).length };
}
{
  // one-in-flight: the second submit against the SAME pending state refuses
  let resolveTurn;
  const gate = new Promise((res) => { resolveTurn = res; });
  const transports = { chatTurn: async () => { await gate;
    return { ok: true, status: 200, payload: success }; } };
  const dispatcher = createTurnDispatcher({
    transports, turnIdFactory: (n) => "turn-" + n });
  const first = dispatcher.submit(s, {
    scopeKey: KEY, activeDocumentPath: DOC_PATH,
    editorState: editorStateWithDoc });
  const second = await dispatcher.submit(s, {
    scopeKey: KEY, activeDocumentPath: DOC_PATH,
    editorState: editorStateWithDoc });
  out.inFlight = { secondRefused: second.refused === true };
  resolveTurn();
  const settled = await first;
  out.inFlight.firstSettled = settled.state.phase;
  // distinct ids per accepted submit
  const third = await dispatcher.submit(settled.state, {
    scopeKey: KEY, activeDocumentPath: DOC_PATH,
    editorState: editorStateWithDoc });
  out.inFlight.freshId = third.clientTurnId !== settled.clientTurnId;
}

// ---- T104 F2: the two RELEASED-envelope violations are refused HERE ----
async function preflight(stateValue, context) {
  let sent = null;
  const transports = { chatTurn: async (body) => {
    sent = body;
    return { ok: true, status: 200, payload: success };
  } };
  const dispatcher = createTurnDispatcher({
    transports, turnIdFactory: (n) => "turn-" + n });
  const result = await dispatcher.submit(stateValue, {
    scopeKey: KEY, editorState: editorStateWithDoc, ...context });
  return { sent, result };
}
{
  // no model selected: the released envelope refuses `model_id: ""`
  const noModel = editComposer(editSubject(
    adoptCatalog(createChatState(KEY), ENVELOPE), "Working subject"),
    "What next?");
  const { sent, result } = await preflight(
    noModel, { activeDocumentPath: DOC_PATH });
  out.noModel = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    phase: result.state.phase,
    composer: result.state.composer,
    error: result.state.lastFailure && result.state.lastFailure.error,
    message: result.state.lastFailure && result.state.lastFailure.message,
  };
}
{
  // no active document, but the tile HAS usable ones: the note names one
  const { sent, result } = await preflight(s, {
    activeDocumentPath: null,
    documentCandidates: () => ["ideation/staging/topic-x/new.md",
                               "ideation/staging/topic-x/other.md"],
  });
  out.noDocument = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    phase: result.state.phase,
    composer: result.state.composer,
    error: result.state.lastFailure && result.state.lastFailure.error,
    message: result.state.lastFailure && result.state.lastFailure.message,
  };
}
{
  // no active document, NO candidates, and no outline either: genuinely no
  // context, so the F2 refusal stands and says what to do instead
  const outlineless = { buffers: {
    outline: { ...bufferOf("outline"), path: null },
    document: { ...bufferOf("document"), path: null } } };
  let sent = null;
  const transports = { chatTurn: async (body) => { sent = body;
    return { ok: true, status: 200, payload: success }; } };
  const dispatcher = createTurnDispatcher({
    transports, turnIdFactory: (n) => "turn-" + n });
  const result = await dispatcher.submit(s, {
    scopeKey: KEY, editorState: outlineless,
    activeDocumentPath: null, documentCandidates: () => [] });
  out.noDocumentAtAll = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    error: result.state.lastFailure && result.state.lastFailure.error,
    message: result.state.lastFailure && result.state.lastFailure.message,
  };
}

// ---- G-1: the OUTLINE-ONLY turn proceeds with a null active document ----
{
  // the real-corpus majority case: no usable document candidate, but the
  // outline IS backed and in scope, so the turn grounds on it alone
  const outlineOnlyState = { buffers: {
    outline: bufferOf("outline"),                       // backed: docs/outline.md
    document: { ...bufferOf("document"), path: null } } };  // not yet created
  const { sent, result } = await preflight(s, {
    editorState: outlineOnlyState,
    activeDocumentPath: null, documentCandidates: () => [] });
  out.outlineOnly = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    activeDocumentPath: sent ? sent.active_document_path : "NOT-SENT",
    hasKey: sent ? ("active_document_path" in sent) : false,
    outlineBufferPath: sent ? sent.buffers[0].path : null,
    documentBufferPath: sent ? sent.buffers[1].path : "NOT-SENT",
    phase: result.state.phase,
  };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def view_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench chat-view probe")
    if not CHAT_VIEW_JS.exists():
        pytest.fail("doxbench-chat.js does not exist yet (T053/T054 red)")
    tmp_path = tmp_path_factory.mktemp("doxbench-chat-view")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "view-harness.mjs"
    harness.write_text(_VIEW_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_request_builder_emits_the_released_request_shape(view_results):
    r = view_results["request"]
    assert r["keys"] == sorted([
        "schema_version", "kind", "client_turn_id", "scope",
        "active_document_path", "working_subject", "message", "model_id",
        "last_assistant_turn_id", "transcript", "buffers"])
    assert r["version"] == 1
    assert r["kind"] == "workbench-chat-turn"
    assert r["turnId"] == "turn-x1"
    assert r["model"] == "model-a"
    assert r["subject"] == "Working subject"
    assert r["message"] == "What next?"
    assert r["scopeKeys"] == ["ref", "repository", "tile_id", "tile_kind"]
    assert r["transcript"] == []
    assert r["lastAssistant"] is None


def test_buffers_are_mapped_current_and_complete_at_submit_time(view_results):
    r = view_results["request"]
    assert r["bufferKinds"] == ["outline", "document"]
    assert r["bufferKeys"] == sorted([
        "kind", "path", "repository", "base_ref", "base_revision",
        "base_hash", "content_hash", "content", "dirty"])
    # identities flatten to the released bare 64-hex spelling
    assert r["outlineHash"] == "d" * 64
    assert r["outlineBase"] == "c" * 64
    assert r["docPath"] is None


def test_a_success_settles_clears_composer_and_appends_turns(view_results):
    s = view_results["success"]
    assert s["settled"] == "idle"
    assert s["composer"] == ""
    assert s["turns"] == 2
    assert s["sentKind"] == "workbench-chat-turn"
    assert s["freshBuffers"] is True


def test_a_released_failure_preserves_the_composer_fr016(view_results):
    f = view_results["failure"]
    assert f["settled"] == "idle"
    assert f["composer"] == "What next?"
    assert f["error"] == "model_failed"
    assert f["turns"] == 0


def test_a_transport_refusal_preserves_the_composer_and_reports_fixed(view_results):
    r = view_results["refusal"]
    assert r["settled"] == "idle"
    assert r["composer"] == "What next?"
    assert r["hasFailure"] is True
    assert r["turns"] == 0


def test_one_turn_in_flight_and_fresh_ids_per_accepted_submit(view_results):
    i = view_results["inFlight"]
    assert i["secondRefused"] is True
    assert i["firstSettled"] == "idle"
    assert i["freshId"] is True


# ---- T104 F2: shapes the RELEASED envelope refuses never reach the wire ----
#
# contract-v1.27's request requires `model_id` minLength 1 and
# `active_document_path` to be a non-empty `confined_path` (only the BUFFER
# path is nullable there). The rail emitted `""` and `null` for them, so two
# answerable local conditions -- no model picked, no document active -- arrived
# as an opaque server refusal, or as `turn_scope_refused` naming nothing the
# operator could pick instead. Both are now refused pre-flight, in the
# operator's own vocabulary, with the composer preserved (FR-016) and the
# transport never consulted.

def test_an_unselected_model_is_refused_pre_flight_not_sent_as_empty(view_results):
    m = view_results["noModel"]
    assert m["refused"] is True
    assert m["transportCalled"] is False
    assert m["phase"] == "idle"
    assert m["composer"] == "What next?"
    assert m["error"] == "no_model_selected"
    assert "model" in m["message"]


def test_no_active_document_is_refused_pre_flight_naming_a_usable_one(view_results):
    d = view_results["noDocument"]
    assert d["refused"] is True
    assert d["transportCalled"] is False
    assert d["phase"] == "idle"
    assert d["composer"] == "What next?"
    assert d["error"] == "no_active_document"
    # ACTIONABLE: the refusal names a document the operator can actually pick
    assert "ideation/staging/topic-x/new.md" in d["message"]


def test_a_tile_with_no_usable_document_says_so_and_names_the_way_forward(
        view_results):
    """SCOPED by G-1: this refusal now covers the tile that has neither a
    candidate NOR a backed outline — genuinely nothing to ground on. A tile
    whose outline IS backed takes the outline-only path below instead."""
    d = view_results["noDocumentAtAll"]
    assert d["refused"] is True
    assert d["transportCalled"] is False
    assert d["error"] == "no_active_document"
    assert "create one" in d["message"]


# ---- G-1: the outline-only turn, the real-corpus majority case -------------
#
# 16 of 21 real staged topics have exactly ONE editable path — the topic's own
# primary fragment, which the canvas loads as the OUTLINE and which T104 F2
# therefore does not offer as a DOCUMENT. Those tiles have no document to name.
# Before contract-v1.28 that made a legal turn impossible and the rail refused;
# now the turn declares `active_document_path: null`, mirroring the
# already-nullable `buffer_state.path` the document buffer carries here.

def test_an_outline_only_tile_sends_a_turn_with_a_null_active_document(
        view_results):
    o = view_results["outlineOnly"]
    assert o["refused"] is False, "the outline-only turn must not be refused"
    assert o["transportCalled"] is True
    # the key is PRESENT and null — absent and null are different facts, and
    # the released envelope requires the key
    assert o["hasKey"] is True
    assert o["activeDocumentPath"] is None
    # the outline is what the turn grounds on, and the document buffer is the
    # not-yet-created shape
    assert o["outlineBufferPath"] == "docs/outline.md"
    assert o["documentBufferPath"] is None
    assert o["phase"] == "idle"


# ---------------------------------------------------------------------------
# T060/T063/T065 (US3, red-first): proposal review cards — a11y-bearing pure
# card model, independent targets, prose-only rendering, current Apply
# through the INJECTED applyProposal seam, stale comparison + new-turn
# recovery, and focus-restoration wiring. DOM-free at the seams, like the
# rest of this suite; the live focus behavior itself is deferred to the
# T098-T100 Playwright pass and pinned here at source level.
# ---------------------------------------------------------------------------

_CARDS_HARNESS = """
import { proposalCardModel, createProposalActions }
  from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer, beginTurn,
         settleTurnSuccess, refreshProposalCurrency, proposalsOf }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const OUTLINE_HASH = "a".repeat(64);
const DOCUMENT_HASH = "b".repeat(64);
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
  models: [{ model_id: "model-a", label: "Approved", provider_class: "on-tenant",
             available: true, input_limit_bytes: 800000,
             output_limit_bytes: 900000, data_handling: "on-tenant" }] };
const proposal = (target, base) => ({ target, base_hash: base,
  summary: "Rework the " + target, content: "# New " + target });
const successWith = (proposals) => ({
  schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: OUTLINE_HASH, document: DOCUMENT_HASH },
  assistant_prose: "with proposals", proposals });
const base = editComposer(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"), "go");

let s = settleTurnSuccess(beginTurn(base), successWith([
  proposal("outline", OUTLINE_HASH), proposal("document", DOCUMENT_HASH)]));
s = refreshProposalCurrency(s, { outline: OUTLINE_HASH,
                                 document: DOCUMENT_HASH });

// card model: both targets, a11y-bearing, apply enabled only when current
out.cards = proposalCardModel(s);
const stale = refreshProposalCurrency(s, { outline: "e".repeat(64),
                                           document: DOCUMENT_HASH });
out.staleCards = proposalCardModel(stale);
out.proseOnly = proposalCardModel(settleTurnSuccess(beginTurn(base),
                                                    successWith([])));

// actions: current Apply goes through the INJECTED seam then marks applied;
// a refusing seam (stale at the buffer) leaves the record un-applied
const applied = [];
const actions = createProposalActions({
  applyProposal: async (target, record) => { applied.push(target); return { ok: true }; } });
const afterApply = await actions.apply(s, "outline");
out.applySeam = { calls: applied,
                  status: proposalsOf(afterApply).outline.status,
                  sibling: proposalsOf(afterApply).document.status };
const refusingActions = createProposalActions({
  applyProposal: async () => null });
const afterRefusal = await refusingActions.apply(s, "outline");
out.applyRefused = proposalsOf(afterRefusal).outline.status;
// T104 F5-5: the refusal is VISIBLE — a fixed local failure lands on
// lastFailure (the same channel every other refusal renders through), while
// everything else stays exactly as it was: the record stays reviewable, the
// sibling untouched, the phase idle.
out.applyRefusedFailure = {
  error: afterRefusal.lastFailure && afterRefusal.lastFailure.error,
  message: afterRefusal.lastFailure && afterRefusal.lastFailure.message,
  status: proposalsOf(afterRefusal).outline.status,
  sibling: proposalsOf(afterRefusal).document.status,
  phase: afterRefusal.phase,
  composerUnchanged: afterRefusal.composer === s.composer,
};
// The throwing seam maps to the SAME fixed failure — and its own detail is
// dropped unread, never echoed into the note.
const throwingActions = createProposalActions({
  applyProposal: async () => {
    throw new Error("buffer-side detail that must never surface"); } });
const afterThrow = await throwingActions.apply(s, "outline");
out.applyThrew = {
  error: afterThrow.lastFailure && afterThrow.lastFailure.error,
  message: afterThrow.lastFailure && afterThrow.lastFailure.message,
};
const afterReject = (await refusingActions.reject(s, "document"));
out.rejected = proposalsOf(afterReject).document.status;
// a stale record never reaches the seam at all
const staleCalls = [];
const staleActions = createProposalActions({
  applyProposal: async (t) => { staleCalls.push(t); return { ok: true }; } });
const afterStaleApply = await staleActions.apply(stale, "outline");
out.staleNeverDispatches = { calls: staleCalls,
  status: proposalsOf(afterStaleApply).outline.status };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def card_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench card probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-cards")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "cards-harness.mjs"
    harness.write_text(_CARDS_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_card_model_carries_both_targets_independently_with_a11y_names(card_results):
    cards = card_results["cards"]
    assert [c["target"] for c in cards] == ["outline", "document"]
    for card in cards:
        assert card["status"] == "current"
        assert card["applyEnabled"] is True
        assert card["rejectEnabled"] is True
        assert card["summary"].startswith("Rework the ")
        assert card["ariaLabel"] == (
            card["target"] + " proposal: " + card["summary"])
        assert "note" in card


def test_a_stale_card_disables_apply_and_names_the_new_turn_recovery(card_results):
    stale_outline = card_results["staleCards"][0]
    assert stale_outline["status"] == "stale"
    assert stale_outline["applyEnabled"] is False
    assert "new turn" in stale_outline["note"]
    sibling = card_results["staleCards"][1]
    assert sibling["status"] == "current"
    assert sibling["applyEnabled"] is True


def test_prose_only_renders_no_cards_at_all(card_results):
    assert card_results["proseOnly"] == []


def test_current_apply_dispatches_the_seam_then_marks_applied(card_results):
    a = card_results["applySeam"]
    assert a["calls"] == ["outline"]
    assert a["status"] == "applied"
    assert a["sibling"] == "current"


def test_a_refusing_buffer_seam_leaves_the_record_unapplied(card_results):
    assert card_results["applyRefused"] == "current"


def test_reject_flows_through_the_action_surface(card_results):
    assert card_results["rejected"] == "rejected"


def test_a_stale_record_never_reaches_the_apply_seam(card_results):
    s = card_results["staleNeverDispatches"]
    assert s["calls"] == []
    assert s["status"] == "stale"


def test_focus_restoration_is_wired_after_card_actions():
    """Source-level pin (the live behavior is the Playwright pass's): the
    card action handler captures the active element and restores focus after
    the state adoption re-render."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "restoreFocus" in source
    assert ".focus()" in source


# ---------------------------------------------------------------------------
# PR #63 review response + T101 ux CHK015: the send-moment data-handling
# disclosure, per-model handling visibility, autofill/direction hardening,
# unsettled-buffer pre-flight refusal, and follow-up-edit preservation.
# ---------------------------------------------------------------------------

def test_send_disclosure_names_the_selected_models_data_handling():
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "sendDisclosure" in source
    assert "doxchat-disclosure" in source


def test_authoring_inputs_disable_autofill_and_derive_direction():
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert 'setAttribute("autocomplete", "off")' in source
    assert 'setAttribute("dir", "auto")' in source


_REVIEW_HARNESS = """
import { sendDisclosure, createTurnDispatcher }
  from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer,
         beginTurn, settleTurnSuccess } from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "Processed in the approved tenant boundary" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
let s = selectModel(adoptCatalog(createChatState(KEY), ENVELOPE), "model-a");
out.disclosure = sendDisclosure(s);
out.noneSelected = sendDisclosure(createChatState(KEY));

// unsettled buffers refuse pre-flight (composer preserved, transport unused)
const unsettled = { buffers: {
  outline: { kind: "outline", path: "docs/o.md", base_ref: "main",
             base_revision: "r1", base_hash: "c".repeat(64),
             current_hash: null, hash_pending: true, content: "#", dirty: true },
  document: { kind: "document", path: null, base_ref: "main",
              base_revision: "r1", base_hash: "c".repeat(64),
              current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
              hash_pending: false, content: "#", dirty: false } } };
let sent = 0;
const dispatcher = createTurnDispatcher({
  transports: { chatTurn: async () => { sent += 1; return null; } },
  turnIdFactory: (n) => "turn-" + n });
const withText = editComposer(s, "hello?");
const refusal = await dispatcher.submit(withText, {
  scopeKey: KEY, activeDocumentPath: null, editorState: unsettled });
out.unsettled = { refused: refusal.refused === true, sent,
                  composer: refusal.state.composer };

// follow-up typing during a slow turn survives settlement
const begun = beginTurn(editComposer(s, "first question"));
const typedDuringFlight = editComposer(begun, "follow-up draft");
const settled = settleTurnSuccess(typedDuringFlight, {
  schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: "a".repeat(64), document: "b".repeat(64) },
  assistant_prose: "answer", proposals: [] });
out.followUp = { composer: settled.composer,
                 turns: settled.transcript.length,
                 human: settled.transcript[0].content };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def review_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench review-response probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-review")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "review-harness.mjs"
    harness.write_text(_REVIEW_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_send_disclosure_is_the_selected_entries_handling_text(review_results):
    assert review_results["disclosure"] == (
        "Processed in the approved tenant boundary")
    assert review_results["noneSelected"] is None


def test_unsettled_buffers_refuse_pre_flight_preserving_the_composer(review_results):
    u = review_results["unsettled"]
    assert u["refused"] is True
    assert u["sent"] == 0
    assert u["composer"] == "hello?"


def test_follow_up_typing_during_a_slow_turn_survives_settlement(review_results):
    f = review_results["followUp"]
    assert f["composer"] == "follow-up draft"
    assert f["turns"] == 2
    assert f["human"] == "first question"


# ---------------------------------------------------------------------------
# PR-stabilization synthesis (2026-07-31): regression-review defects R1/R2.
# R1: a turn ABANDONED mid-flight (abort/rekey) must never settle — the
# dispatcher refuses to settle when the live state has released the flight.
# R2: the unsettled-buffer pre-flight refusal must be VISIBLE — a fixed
# local failure note, never a silent dead button.
# ---------------------------------------------------------------------------

_SYNTH_HARNESS = """
import { createTurnDispatcher } from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer,
         abortTurn, transcriptWindow } from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
const buffer = (kind) => ({ kind, path: null, owned: true, base_ref: "main",
  base_revision: "r1", base_hash: "c".repeat(64),
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "#", dirty: false });
// T104 F2: a dispatched turn names a document (the released envelope's
// `active_document_path` is a non-empty confined_path), so these scenarios --
// whose subject is abort/settlement, not the null-path lifecycle -- carry one.
const DOC_PATH = "docs/detail.md";
const editorState = { buffers: {
  outline: buffer("outline"),
  document: { ...buffer("document"), path: DOC_PATH } } };
const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
  assistant_prose: "late answer", proposals: [] };
const base = editComposer(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"), "hello");

// R1: abort mid-flight, keep editing; the late response must be ABANDONED.
{
  let live = base;
  let release;
  const gate = new Promise((res) => { release = res; });
  const dispatcher = createTurnDispatcher({
    transports: { chatTurn: async () => { await gate;
      return { ok: true, status: 200, payload: SUCCESS }; } },
    turnIdFactory: (n) => "turn-" + n });
  const pending = dispatcher.submit(live, {
    scopeKey: KEY, activeDocumentPath: DOC_PATH, editorState,
    onBegin: (s) => { live = s; }, liveState: () => live });
  live = abortTurn(live);                       // human abandons the flight
  live = editComposer(live, "different");       // and keeps working
  release();
  const result = await pending;
  out.abandoned = { flag: result.abandoned === true,
                    settledState: result.state === live,
                    turns: transcriptWindow(live).length,
                    composer: live.composer };
}

// R2: unsettled buffers refuse VISIBLY — a fixed failure the view renders.
{
  const unsettled = { buffers: { ...editorState.buffers,
    outline: { ...editorState.buffers.outline,
               current_hash: null, hash_pending: true } } };
  const dispatcher = createTurnDispatcher({
    transports: { chatTurn: async () => null },
    turnIdFactory: (n) => "turn-" + n });
  const result = await dispatcher.submit(base, {
    scopeKey: KEY, activeDocumentPath: null, editorState: unsettled });
  out.unsettled = { refused: result.refused === true,
                    error: result.state.lastFailure
                      && result.state.lastFailure.error,
                    message: result.state.lastFailure
                      && result.state.lastFailure.message,
                    composer: result.state.composer,
                    phase: result.state.phase };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def synth_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench synthesis probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-synth")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "synth-harness.mjs"
    harness.write_text(_SYNTH_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_an_aborted_flight_never_settles_and_live_work_survives(synth_results):
    a = synth_results["abandoned"]
    assert a["flag"] is True
    assert a["settledState"] is True   # the dispatcher hands back the LIVE state
    assert a["turns"] == 0             # nothing appended from the dead turn
    assert a["composer"] == "different"


def test_the_unsettled_buffer_refusal_is_visible_and_fixed(synth_results):
    u = synth_results["unsettled"]
    assert u["refused"] is True
    assert u["error"] == "buffers_unsettled"
    assert isinstance(u["message"], str) and u["message"]
    assert u["composer"] == "hello"
    assert u["phase"] == "idle"


# ---------------------------------------------------------------------------
# T100 P1-2 (operator finding, real corpus, 2026-08-01): a console-token
# refusal (legacy {ok,error,message} 403) wedged the rail — Send stayed
# disabled until reload. Every transport non-2xx settles the failure path,
# the stale-token case gets a RECOVERABLE fixed message, and the mounted
# send handler is throw-proof (any unexpected error still returns the rail
# to idle with a visible fixed failure).
# ---------------------------------------------------------------------------

_WEDGE_HARNESS = """
import { createTurnDispatcher } from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const buffer = (kind) => ({ kind, path: null, owned: true, base_ref: "main",
  base_revision: "r1", base_hash: "c".repeat(64),
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "#", dirty: false });
// T104 F2: the released envelope requires a named active document; this
// scenario's subject is the stale-token mapping, so it carries one.
const DOC_PATH = "docs/detail.md";
const editorState = { buffers: {
  outline: buffer("outline"),
  document: { ...buffer("document"), path: DOC_PATH } } };
const base = editComposer(selectModel(adoptCatalog(createChatState(KEY),
  { schema_version: 1, kind: "workbench-model-catalog", models: [ENTRY] }),
  "model-a"), "hello?");

// The EXACT operator scenario: 403 with the legacy pre-identity shape.
const dispatcher = createTurnDispatcher({
  transports: { chatTurn: async () => ({ ok: false, status: 403,
    payload: { ok: false, error: "agent_invocation",
               message: "the console token does not match this serve's" } }) },
  turnIdFactory: (n) => "turn-" + n });
const result = await dispatcher.submit(base, {
  scopeKey: KEY, activeDocumentPath: DOC_PATH, editorState });
out.stale = { phase: result.state.phase,
              composer: result.state.composer,
              error: result.state.lastFailure && result.state.lastFailure.error,
              message: result.state.lastFailure && result.state.lastFailure.message };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def wedge_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench wedge probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-wedge")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "wedge-harness.mjs"
    harness.write_text(_WEDGE_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_stale_console_token_refusal_settles_recoverably(wedge_results):
    s = wedge_results["stale"]
    assert s["phase"] == "idle"
    assert s["composer"] == "hello?"
    assert s["error"] == "console_token_stale"
    assert "reload" in s["message"]


def test_the_send_handler_is_throw_proof_by_construction():
    """Source pin for the wedge class the harness cannot reproduce: whatever
    throws inside the mounted send path, the handler's finally-discipline
    returns the rail to a visible failed-idle state instead of a dead
    button."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "SEND_PATH_FAILED" in source
    assert source.count("finally") >= 2  # dispatcher slot + send handler


# ---------------------------------------------------------------------------
# R-1 (operator requirement, 2026-08-02): reopening the same tile CONTINUES
# the work — buffers AND the proposal set restore together. The correctness
# rule the operator named: a restored proposal must be re-scored against the
# RESTORED bytes, so a base that moved while the tile was closed comes back
# STALE, never `current`.
# ---------------------------------------------------------------------------

_RESTORE_HARNESS = """
import { createChatState, adoptCatalog, selectModel, editComposer, editSubject,
         beginTurn, settleTurnSuccess, proposalsOf, chatSnapshot,
         restoreChatState, transcriptWindow }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "r", ref: "main", tile_kind: "staged", tile_id: "t" };
const OUTLINE = "a".repeat(64);
const DOCUMENT = "b".repeat(64);
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const proposal = (target, base) => ({ target, base_hash: base,
  summary: "Rework the " + target, content: "# New " + target });
let s = editSubject(editComposer(selectModel(adoptCatalog(createChatState(KEY),
  { schema_version: 1, kind: "workbench-model-catalog", models: [ENTRY] }),
  "model-a"), "draft question"), "Working subject");
s = settleTurnSuccess(beginTurn(s), {
  schema_version: 1, kind: "workbench-chat-turn-success", client_turn_id: "t",
  assistant_turn_id: "a", model_id: "model-a",
  observed_hashes: { outline: OUTLINE, document: DOCUMENT },
  assistant_prose: "answer",
  proposals: [proposal("outline", OUTLINE), proposal("document", DOCUMENT)] });

const snap = chatSnapshot(s);
out.snapshot = { kind: snap.kind, proposals: snap.proposals.length,
                 transcript: snap.transcript.length,
                 subject: snap.workingSubject, model: snap.selectedModelId };

// Restore into a FRESH state with UNCHANGED hashes: both proposals current.
const same = restoreChatState(createChatState(KEY), snap,
  { outline: OUTLINE, document: DOCUMENT });
out.sameHashes = { outline: proposalsOf(same).outline.status,
                   document: proposalsOf(same).document.status,
                   transcript: transcriptWindow(same).length,
                   subject: same.workingSubject,
                   model: same.selectedModelId };

// Restore where the OUTLINE bytes moved while the tile was closed: that
// proposal must come back STALE, the sibling still current.
const drifted = restoreChatState(createChatState(KEY), snap,
  { outline: "e".repeat(64), document: DOCUMENT });
out.driftedHashes = { outline: proposalsOf(drifted).outline.status,
                      document: proposalsOf(drifted).document.status };

// A foreign/garbage blob is refused fail-closed (fresh state kept).
out.foreign = restoreChatState(createChatState(KEY), { kind: "nope" },
  { outline: OUTLINE, document: DOCUMENT }).workingSubject;
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def restore_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the chat restore probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-restore")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "restore-harness.mjs"
    harness.write_text(_RESTORE_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_chat_snapshot_carries_subject_model_transcript_and_proposals(restore_results):
    s = restore_results["snapshot"]
    assert s["kind"] == "doxbench-chat-working-state"
    assert s["proposals"] == 2
    assert s["transcript"] == 2
    assert s["subject"] == "Working subject"
    assert s["model"] == "model-a"


def test_restoring_against_unchanged_bytes_keeps_proposals_current(restore_results):
    r = restore_results["sameHashes"]
    assert r["outline"] == "current"
    assert r["document"] == "current"
    assert r["transcript"] == 2
    assert r["subject"] == "Working subject"
    assert r["model"] == "model-a"


def test_a_proposal_whose_base_moved_while_closed_restores_stale(restore_results):
    d = restore_results["driftedHashes"]
    assert d["outline"] == "stale"
    assert d["document"] == "current"


def test_a_foreign_snapshot_is_refused_fail_closed(restore_results):
    assert restore_results["foreign"] == ""


def test_the_stale_console_token_mapping_covers_both_route_spellings():
    """R-3: the doxBench routes spell the pre-identity refusal
    `console_required` while the gate-action route spells it
    `agent_invocation` — the first fix caught only the latter, which is why a
    stale token still showed the generic message."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert '=== "agent_invocation"' in source
    assert '=== "console_required"' in source
    from ideation_dashboard import serve as serve_mod
    assert serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED == "console_required"


# ---------------------------------------------------------------------------
# T104 F5-2 (doxBench review, 2026-08-04): the DISPLAY transcript and the
# WIRE window are different bounds. A single LEGAL pair (message <= 16,384 +
# assistant prose <= 65,536 = up to 81,920 bytes) exceeds the 64,000-byte
# bound, which mirrors the SERVER's REQUEST-side transcript bound
# (doxbench_turns.MAX_TRANSCRIPT_BYTES) and therefore belongs to the wire.
# The old boundedAppend applied it to the display and evicted from the front
# until it held — emptying the transcript INCLUDING the answer that had just
# arrived. The operator's answer must never vanish; the next request's
# transcript must still fit the wire.
# ---------------------------------------------------------------------------

_OVERSIZED_HARNESS = """
import { buildTurnRequest } from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer, beginTurn,
         settleTurnSuccess, transcriptWindow, transcriptWireWindow,
         MAX_MESSAGE_BYTES, MAX_TRANSCRIPT_BYTES }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
const success = (prose) => ({
  schema_version: 1, kind: "workbench-chat-turn-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  observed_hashes: { outline: "a".repeat(64), document: "b".repeat(64) },
  assistant_prose: prose, proposals: [] });
const bytesOf = (turns) => turns.reduce(
  (n, t) => n + Buffer.byteLength(t.content, "utf8"), 0);
const base = selectModel(adoptCatalog(createChatState(KEY), ENVELOPE), "model-a");

// A LEGAL oversized pair: 16,000-byte message (under MAX_MESSAGE_BYTES),
// 60,000-byte answer (under the server's 65,536 prose bound) — 76,000 bytes
// together, over the 64,000-byte wire bound.
const BIG_Q = "m".repeat(16000);
const BIG_A = "a".repeat(60000);
let s = settleTurnSuccess(beginTurn(editComposer(base, BIG_Q)), success(BIG_A));
const displayed = transcriptWindow(s);
out.oversizedDisplayed = {
  turns: displayed.length,
  roles: displayed.map((t) => t.role),
  humanBytes: displayed.length ? Buffer.byteLength(displayed[0].content, "utf8") : 0,
  assistantBytes: displayed.length > 1
    ? Buffer.byteLength(displayed[1].content, "utf8") : 0,
  totalBytes: bytesOf(displayed),
};

// The wire window over the SAME state: what fits — here nothing, because
// even the newest pair alone exceeds the bound — while the display keeps it.
const wire = transcriptWireWindow(s);
out.wire = { turns: wire.length, bytes: bytesOf(wire) };

// And the actual next REQUEST uses the wire window, not the display.
const bufferOf = (kind, path) => ({
  kind, path, base_ref: "main", base_revision: "r1",
  base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  content: "# " + kind, dirty: false });
const req = buildTurnRequest({
  state: editComposer(s, "follow-up"), scopeKey: KEY, clientTurnId: "turn-n",
  activeDocumentPath: "docs/detail.md",
  editorState: { buffers: { outline: bufferOf("outline", "docs/outline.md"),
                            document: bufferOf("document", "docs/detail.md") } } });
out.requestTranscript = { turns: req.transcript.length,
                          bytes: bytesOf(req.transcript) };

// Once a NEWER pair lands, the oversized pair is oldest and evictable: the
// display drops it and keeps the new answer.
const after = settleTurnSuccess(beginTurn(editComposer(s, "next question")),
                                success("short answer"));
const afterWin = transcriptWindow(after);
out.afterNextTurn = { turns: afterWin.length,
                      human: afterWin.length ? afterWin[0].content : null,
                      totalBytes: bytesOf(afterWin) };

// Ordinary pairs behave exactly as before: display and wire agree.
let ord = base;
for (let i = 0; i < 3; i += 1) {
  ord = settleTurnSuccess(beginTurn(editComposer(ord, "q" + i)),
                          success("answer " + i));
}
out.ordinary = {
  displayTurns: transcriptWindow(ord).length,
  wireTurns: transcriptWireWindow(ord).length,
  identical: transcriptWireWindow(ord) === transcriptWindow(ord)
    || JSON.stringify(transcriptWireWindow(ord))
       === JSON.stringify(transcriptWindow(ord)),
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def oversized_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the oversized-pair probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-oversized")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "oversized-harness.mjs"
    harness.write_text(_OVERSIZED_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_an_oversized_legal_pair_stays_displayed(oversized_results):
    """The operator's answer never vanishes: the newest pair survives the
    display window even when it alone exceeds the wire bound."""
    d = oversized_results["oversizedDisplayed"]
    assert d["turns"] == 2, "the just-arrived pair was evicted from the display"
    assert d["roles"] == ["human", "assistant"]
    assert d["humanBytes"] == 16_000
    assert d["assistantBytes"] == 60_000
    assert d["totalBytes"] == 76_000  # legal, and over the 64,000 wire bound


def test_the_wire_window_still_respects_the_request_side_bound(oversized_results):
    """The 64,000-byte bound mirrors the server's REQUEST-side transcript
    bound and is enforced where the request is built: when even the newest
    pair alone exceeds it, the wire transcript is empty — sent, not lied
    about — while the display keeps the pair."""
    w = oversized_results["wire"]
    assert w["bytes"] <= 64_000
    assert w["turns"] == 0
    r = oversized_results["requestTranscript"]
    assert r["bytes"] <= 64_000
    assert r["turns"] == 0


def test_the_oversized_pair_is_evicted_once_a_newer_pair_lands(oversized_results):
    a = oversized_results["afterNextTurn"]
    assert a["turns"] == 2
    assert a["human"] == "next question"
    assert a["totalBytes"] <= 64_000


def test_ordinary_pairs_display_and_wire_identically(oversized_results):
    o = oversized_results["ordinary"]
    assert o["displayTurns"] == 6
    assert o["wireTurns"] == 6
    assert o["identical"] is True


# ---------------------------------------------------------------------------
# T104 F5-7 (doxBench review, 2026-08-04): a PERSISTED `selectedModelId` is a
# claim about a catalog that may have changed while the tile was closed.
# `restoreChatState` adopted it on a bare typeof check, bypassing
# `selectModel`'s only-available-entries rule — so after the R-1 restore a
# stale id rendered the selector's PLACEHOLDER while `canSend` said true and
# the dispatcher shipped an id the server refuses as model_unavailable, with
# no data-handling disclosure shown. The invariant pinned here: canSend is
# never true while the selector would show the placeholder — i.e. the send
# gate requires the selected id to name an AVAILABLE catalog entry, restore
# only adopts an id its catalog can vouch for, and a catalog arriving later
# (adoptCatalog) re-validates whatever id is held.
# ---------------------------------------------------------------------------

_STALE_MODEL_HARNESS = """
import { createChatState, adoptCatalog, selectModel, editComposer,
         restoreChatState, canSend }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "r", ref: "main", tile_kind: "staged", tile_id: "t" };
const entry = (id, available) => ({ model_id: id, label: "Approved " + id,
  provider_class: "on-tenant", available, input_limit_bytes: 800000,
  output_limit_bytes: 900000, data_handling: "on-tenant" });
const envelope = (models) => ({ schema_version: 1,
  kind: "workbench-model-catalog", models });
const snapshot = (modelId) => ({
  schema_version: 1, kind: "doxbench-chat-working-state",
  workingSubject: "subject", selectedModelId: modelId,
  composer: "ready to send", transcript: [], proposals: [] });

// 1) restore into a state whose catalog does NOT carry the persisted id
const withCatalog = adoptCatalog(createChatState(KEY),
                                 envelope([entry("model-a", true)]));
const stale = restoreChatState(withCatalog, snapshot("model-gone"), null);
out.staleId = { selected: stale.selectedModelId, canSend: canSend(stale) };

// 2) restore of an id the catalog vouches for survives
const valid = restoreChatState(withCatalog, snapshot("model-a"), null);
out.validId = { selected: valid.selectedModelId, canSend: canSend(valid) };

// 3) the persisted id names an entry the catalog carries but marks
//    UNAVAILABLE: same refusal as absent
const offCatalog = adoptCatalog(createChatState(KEY),
                                envelope([entry("model-a", false)]));
const off = restoreChatState(offCatalog, snapshot("model-a"), null);
out.unavailableId = { selected: off.selectedModelId, canSend: canSend(off) };

// 4) restore BEFORE any catalog (models === null): the id is kept for the
//    catalog to re-validate, but the send gate stays closed until it does —
//    the placeholder and the disabled Send agree in the meantime
const early = restoreChatState(createChatState(KEY), snapshot("model-a"), null);
out.noCatalogYet = { selected: early.selectedModelId, canSend: canSend(early) };

// 5) the catalog then arrives CARRYING the id: it lights up
const vouched = adoptCatalog(early, envelope([entry("model-a", true)]));
out.catalogVouches = { selected: vouched.selectedModelId,
                       canSend: canSend(vouched) };

// 6) the catalog then arrives WITHOUT the id: adoptCatalog closes the other
//    half — the held id is dropped, never shipped
const revoked = adoptCatalog(early, envelope([entry("model-b", true)]));
out.catalogRevokes = { selected: revoked.selectedModelId,
                       canSend: canSend(revoked) };

// 7) a live selection is untouched by a catalog that still vouches for it
const live = editComposer(selectModel(withCatalog, "model-a"), "hello");
const readopted = adoptCatalog(live, envelope([entry("model-a", true)]));
out.liveKept = { selected: readopted.selectedModelId,
                 canSend: canSend(readopted) };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def stale_model_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the stale-model restore probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-stale-model")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "stale-model-harness.mjs"
    harness.write_text(_STALE_MODEL_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_stale_persisted_model_id_is_not_adopted_on_restore(stale_model_results):
    s = stale_model_results["staleId"]
    assert s["selected"] is None, (
        "a persisted id the restored catalog cannot vouch for must fall back "
        "to the placeholder, not silently arm Send")
    assert s["canSend"] is False


def test_a_vouched_persisted_model_id_survives_restore(stale_model_results):
    v = stale_model_results["validId"]
    assert v["selected"] == "model-a"
    assert v["canSend"] is True


def test_an_unavailable_entry_is_refused_like_an_absent_one(stale_model_results):
    u = stale_model_results["unavailableId"]
    assert u["selected"] is None
    assert u["canSend"] is False


def test_restore_before_any_catalog_keeps_the_id_but_never_arms_send(
        stale_model_results):
    """The decided posture for the models === null window: the id is KEPT so
    the operator's choice survives the reopen (R-1 continuity), and the send
    gate stays closed until a catalog vouches for it — so canSend is never
    true while the selector shows the placeholder."""
    n = stale_model_results["noCatalogYet"]
    assert n["selected"] == "model-a"
    assert n["canSend"] is False


def test_a_later_catalog_revalidates_the_held_id_both_ways(stale_model_results):
    assert stale_model_results["catalogVouches"] == {
        "selected": "model-a", "canSend": True}
    assert stale_model_results["catalogRevokes"] == {
        "selected": None, "canSend": False}


def test_a_live_selection_survives_a_catalog_that_still_vouches_for_it(
        stale_model_results):
    assert stale_model_results["liveKept"] == {
        "selected": "model-a", "canSend": True}


def test_a_refused_apply_records_a_visible_fixed_failure(card_results):
    """T104 F5-5: a refused Apply used to return the identical state — zero
    visible change, the operator left staring at an armed button that did
    nothing. The refusal now lands on lastFailure in the rail's own fixed
    vocabulary; the record stays reviewable and nothing else moves."""
    f = card_results["applyRefusedFailure"]
    assert f["error"] == "proposal_apply_refused"
    assert "no longer matches the buffer" in f["message"]
    assert "new turn" in f["message"], "the note must name the only recovery"
    assert f["status"] == "current", "the record stays reviewable"
    assert f["sibling"] == "current", "the other target's record is untouched"
    assert f["phase"] == "idle"
    assert f["composerUnchanged"] is True


def test_a_throwing_apply_seam_maps_to_the_same_fixed_failure(card_results):
    t = card_results["applyThrew"]
    assert t["error"] == "proposal_apply_refused"
    assert "buffer-side detail" not in (t["message"] or ""), (
        "the seam's own error text must be dropped unread, never echoed")
    assert "no longer matches the buffer" in t["message"]


# ---------------------------------------------------------------------------
# T104 F5-5 + F5-9 (doxBench review, 2026-08-04): the MOUNTED rail, driven
# against a minimal DOM (the same instrument test_staging_workbench.py's
# ending-replay harness uses).
#
# F5-5: clicking Apply on a proposal the injected seam refuses must RENDER a
# failure note and ANNOUNCE it — the old path returned the identical state,
# so a refused Apply produced zero visible change.
#
# F5-9 residual: with no selectable model, the shell's posture line says
# "chat is unavailable" while a fully-rendered rail mounts beside it. The
# rail now carries its OWN posture — an in-rail unavailability note shown
# whenever state.models has no available entry, replaced by the live
# selector when a catalog with one arrives (the rail is never unmounted, so
# the existing onState path still lights it up).
# ---------------------------------------------------------------------------

_RAIL_DOM_HARNESS = """
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.hidden = false;
    this.disabled = false; this.value = '';
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  appendChild(child) { this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() {}
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
}
const doc = { createElement: (tag) => new Node(tag), activeElement: null };
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const fire = async (node, type) => {
  for (const fn of node.listeners[type] || []) await fn({});
};

import { mountDoxBenchChatRail } from "./doxbench-chat.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "# " + kind, dirty: false });
const editorState = () => ({ buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md") } });

// ---- F5-9: empty catalog -> in-rail unavailability note ----
{
  const host = new Node("div"); host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [] }),
      chatTurn: async () => null },
    editorState, activeDocumentPath: () => "docs/detail.md" });
  await rail.ready;
  const note = byClass(host, "doxchat-unavailable")[0] || null;
  const selector = byClass(host, "doxchat-model")[0];
  out.emptyCatalog = {
    noteExists: Boolean(note),
    noteHidden: note ? note.hidden : null,
    noteText: note ? note.textContent : null,
    selectorHidden: selector.hidden,
    sendDisabled: byClass(host, "doxchat-send")[0].disabled,
  };
}

// ---- F5-9: a catalog arriving later replaces the note with the selector ----
{
  const host = new Node("div"); host.ownerDocument = doc;
  let resolveCatalog;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: () => new Promise((res) => { resolveCatalog = res; }),
      chatTurn: async () => null },
    editorState, activeDocumentPath: () => "docs/detail.md" });
  const note = byClass(host, "doxchat-unavailable")[0] || null;
  const selector = byClass(host, "doxchat-model")[0];
  const beforeCatalog = { noteHidden: note ? note.hidden : null,
                          selectorHidden: selector.hidden };
  resolveCatalog({ schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] });
  await rail.ready;
  out.lateCatalog = {
    beforeCatalog,
    noteHidden: note ? note.hidden : null,
    selectorHidden: selector.hidden,
    options: selector.children.map((o) => o.value),
  };
}

// ---- F5-5: a refused Apply renders a failure note and announces it ----
{
  const host = new Node("div"); host.ownerDocument = doc;
  const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-success",
    client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
    observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
    assistant_prose: "answer",
    proposals: [{ target: "outline", base_hash: "d".repeat(64),
                  summary: "Rework the outline", content: "# New outline" }] };
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => ({ ok: true, status: 200, payload: SUCCESS }) },
    editorState, activeDocumentPath: () => "docs/detail.md",
    applyProposal: async () => ({ ok: false,
      error: "this proposal no longer matches the buffer" }) });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "please propose"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const stateBefore = rail.state();
  await fire(byClass(host, "doxchat-card-apply")[0], "click");
  const failureNote = byClass(host, "doxchat-failure")[0];
  const announce = byClass(host, "doxchat-announce")[0];
  out.refusedApply = {
    cardsBefore: stateBefore.proposals.outline
      && stateBefore.proposals.outline.status,
    noteHidden: failureNote.hidden,
    noteText: failureNote.textContent,
    announced: announce.textContent,
    status: rail.state().proposals.outline.status,
    transcript: rail.state().transcript.length,
    composer: rail.state().composer,
  };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def rail_dom_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the mounted-rail DOM probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-rail-dom")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "rail-dom-harness.mjs"
    harness.write_text(_RAIL_DOM_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_an_empty_catalog_mount_renders_the_in_rail_unavailability_note(
        rail_dom_results):
    """F5-9 residual: the rail beside the shell's "chat is unavailable"
    posture line must not look fully live. The in-rail note states the same
    posture in the rail's own fixed vocabulary and stands in for the
    selector; Send stays disabled (that half was already fixed)."""
    e = rail_dom_results["emptyCatalog"]
    assert e["noteExists"] is True
    assert e["noteHidden"] is False
    assert "chat is unavailable" in e["noteText"]
    assert "no approved model" in e["noteText"]
    assert e["selectorHidden"] is True, (
        "an empty selector rendered beside the unavailability posture is the "
        "contradiction this finding names")
    assert e["sendDisabled"] is True


def test_a_catalog_arriving_later_replaces_the_note_with_the_live_selector(
        rail_dom_results):
    l = rail_dom_results["lateCatalog"]
    # before the catalog resolves the rail is honest about having no model
    assert l["beforeCatalog"] == {"noteHidden": False, "selectorHidden": True}
    # the rail was never unmounted, so the arriving catalog lights it up
    assert l["noteHidden"] is True
    assert l["selectorHidden"] is False
    assert "model-a" in l["options"]


def test_a_refused_apply_renders_a_failure_note_and_announces_it(
        rail_dom_results):
    """F5-5's pin: clicking Apply on a proposal the seam refuses produces a
    VISIBLE, non-echoing failure — the note renders, the live region
    announces, and the state is otherwise unchanged (the record stays
    reviewable, the transcript and composer untouched)."""
    r = rail_dom_results["refusedApply"]
    assert r["cardsBefore"] == "current", "precondition: an applicable card"
    assert r["noteHidden"] is False
    assert "no longer matches the buffer" in r["noteText"]
    assert r["announced"] == r["noteText"], (
        "the announcement carries the same fixed sentence the note renders")
    # non-echoing: the proposal's own content never appears in the refusal
    assert "New outline" not in r["noteText"]
    assert r["status"] == "current"
    assert r["transcript"] == 2
    assert r["composer"] == ""
