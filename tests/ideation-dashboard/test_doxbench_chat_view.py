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

from ideation_dashboard import serve as serve_mod

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
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: "a".repeat(64), document: "b".repeat(64) },
  assistant_prose: prose, proposals: [] });
const FAILURE = { schema_version: 1, kind: "workbench-chat-turn-v2-failure",
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
const editorState = { active_buffer: "outline",
                      buffers: { outline: bufferOf("outline"),
                                 document: bufferOf("document") } };
let s = editComposer(editSubject(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"),
  "Working subject"), "What next?");

// ---- pure request builder ----
const req = buildTurnRequest({
  state: s, scopeKey: KEY, clientTurnId: "turn-x1",
  boundBuffer: "outline", editorState });
out.request = {
  keys: Object.keys(req).sort(),
  version: req.schema_version, kind: req.kind,
  turnId: req.client_turn_id, model: req.model_id,
  subject: req.working_subject, message: req.message,
  scopeKeys: Object.keys(req.scope).sort(),
  boundBuffer: req.bound_buffer,
  hasActiveDocumentPath: "active_document_path" in req,
  bufferKinds: req.buffers.map((b) => b.kind),
  bufferKeys: Object.keys(req.buffers[0]).sort(),
  outlineHash: req.buffers[0].content_hash,
  outlineBase: req.buffers[0].base_hash,
  docPath: req.buffers[1].path,
  transcript: req.transcript,
  lastAssistant: req.last_assistant_turn_id,
};

// ---- dispatcher: success / failure / refusal / one-in-flight ----
const success = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "turn-1", assistant_turn_id: "a-1", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "Processed in the approved tenant boundary" },
  bound_buffer: "docs/detail.md",
  observed_hashes: { outline: "d".repeat(64), "docs/detail.md": "d".repeat(64) },
  assistant_prose: "grounded answer", proposals: [] };
const failure = { schema_version: 1, kind: "workbench-chat-turn-v2-failure",
  client_turn_id: "turn-1", error: "model_failed",
  message: "the model request failed" };

// The dispatch scenarios below carry a BACKED document under the reserved key,
// which is the shape a restored Phase A session holds and a legal instance of
// the keyed set. The pure builder above keeps the null-path document buffer it
// always had.
const DOC_PATH = "docs/detail.md";
const editorStateWithDoc = { active_buffer: "document",
  buffers: {
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
    scopeKey: KEY, editorState: editorStateWithDoc });
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
    scopeKey: KEY, editorState: editorStateWithDoc });
  const second = await dispatcher.submit(s, {
    scopeKey: KEY, editorState: editorStateWithDoc });
  out.inFlight = { secondRefused: second.refused === true };
  resolveTurn();
  const settled = await first;
  out.inFlight.firstSettled = settled.state.phase;
  // distinct ids per accepted submit
  const third = await dispatcher.submit(settled.state, {
    scopeKey: KEY, editorState: editorStateWithDoc });
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
  const { sent, result } = await preflight(noModel, {});
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
  // SUPERSEDES the interim N4 posture (task 8.6, recorded WITH BRETT in the
  // PR #207 re-verification). Under the v1 wire, a turn bound to a document
  // loaded BESIDE the tile's own was refused pre-flight with a stated reason,
  // because the released envelope had room for exactly the outline plus one
  // reserved slot. The widened envelope carries the loaded set and DECLARES the
  // binding, so that same selection now SENDS: the request names that document
  // as the bound buffer and still carries every buffer the canvas holds.
  const LOADED = "ideation/staging/topic-x/other.md";
  const besideTheTile = { active_buffer: LOADED, buffers: {
    outline: bufferOf("outline"),
    document: { ...bufferOf("document"), path: DOC_PATH },
    [LOADED]: { ...bufferOf("document"), path: LOADED } } };
  const { sent, result } = await preflight(s, { editorState: besideTheTile });
  out.boundBesideTheTile = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    boundBuffer: sent ? sent.bound_buffer : "NOT-SENT",
    bufferPaths: sent ? sent.buffers.map((b) => b.path) : [],
    phase: result.state.phase,
    failure: result.state.lastFailure && result.state.lastFailure.error,
  };
}
{
  // An UNSETTLED buffer ANYWHERE in the loaded set is one identity the request
  // cannot declare, so the whole turn refuses pre-flight -- the check reads
  // every buffer the state holds rather than two named ones.
  const LOADED = "ideation/staging/topic-x/other.md";
  const oneUnsettled = { active_buffer: "outline", buffers: {
    outline: bufferOf("outline"),
    document: { ...bufferOf("document"), path: DOC_PATH },
    [LOADED]: { ...bufferOf("document"), path: LOADED, hash_pending: true } } };
  const { sent, result } = await preflight(s, { editorState: oneUnsettled });
  out.oneUnsettled = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    error: result.state.lastFailure && result.state.lastFailure.error,
  };
}

// ---- the outline-only turn, now DECLARED rather than implied by a null ----
{
  // The real-corpus majority case: the tile's only editable path IS its outline,
  // so the reserved document slot is not yet created. The turn binds to the
  // outline and SAYS SO; the widened envelope carries no `active_document_path`
  // at all, so nothing downstream can infer a binding from one.
  const outlineOnlyState = { active_buffer: "outline", buffers: {
    outline: bufferOf("outline"),                       // backed: docs/outline.md
    document: { ...bufferOf("document"), path: null } } };  // not yet created
  const { sent, result } = await preflight(s, { editorState: outlineOnlyState });
  out.outlineOnly = {
    refused: result.refused === true,
    transportCalled: sent !== null,
    boundBuffer: sent ? sent.bound_buffer : "NOT-SENT",
    hasActiveDocumentPath: sent ? ("active_document_path" in sent) : false,
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
    """RE-PINNED at contract-v1.34 (add-doxbench-editing-phase-b §13). The rail
    sends the WIDENED envelope: `bound_buffer` replaces `active_document_path`,
    which is not merely renamed but GONE -- the binding is declared, and the
    envelope carries no adjacent field anything could infer one from (D17)."""
    r = view_results["request"]
    assert r["keys"] == sorted([
        "schema_version", "kind", "client_turn_id", "scope",
        "bound_buffer", "working_subject", "message", "model_id",
        "last_assistant_turn_id", "transcript", "buffers"])
    assert r["hasActiveDocumentPath"] is False
    assert r["boundBuffer"] == "outline"
    assert r["version"] == 1
    assert r["kind"] == "workbench-chat-turn-v2"
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
    assert s["sentKind"] == "workbench-chat-turn-v2"
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


# ---- shapes the RELEASED envelope refuses never reach the wire ----
#
# `model_id` is still minLength 1 on the widened envelope, so an unselected model
# is still refused pre-flight, in the operator's own vocabulary, with the
# composer preserved (FR-016) and the transport never consulted.
#
# The `no_active_document` refusals that stood beside it are GONE with the v1
# wire that forced them (contract-v1.34, §13): that envelope made a turn declare
# ONE active document path, so an operator with several candidates had a choice
# to make before one could be named, and a tile with none had to prove it could
# ground on the outline instead. The widened envelope carries every loaded buffer
# and binds to the one the human SELECTED, so neither question can arise.

def test_an_unselected_model_is_refused_pre_flight_not_sent_as_empty(view_results):
    m = view_results["noModel"]
    assert m["refused"] is True
    assert m["transportCalled"] is False
    assert m["phase"] == "idle"
    assert m["composer"] == "What next?"
    assert m["error"] == "no_model_selected"
    assert "model" in m["message"]


def test_a_selection_beside_the_tiles_own_document_now_sends(view_results):
    """THE N4 DISSOLUTION, pinned (task 8.6 -> §13).

    The interim posture this supersedes was explicit and recorded WITH BRETT: a
    human could load and edit any number of documents and Save each, but the CHAT
    could not be re-pointed at one, because the released v1 envelope carried the
    outline plus one reserved slot and nothing else. Send was held closed for any
    other selection and the reason was visible on the control.

    The widened envelope ends it: the same selection sends, the request DECLARES
    that document as the bound buffer, and it still carries every buffer the
    canvas holds -- binding says what the chat works ON, never what it may see."""
    b = view_results["boundBesideTheTile"]
    assert b["refused"] is False, "the interim binding refusal is retired"
    assert b["transportCalled"] is True
    assert b["failure"] is None
    assert b["boundBuffer"] == "ideation/staging/topic-x/other.md"
    # GROUNDING is unnarrowed: the outline, the tile's own document, and the
    # document loaded beside it all ride the request.
    assert sorted(b["bufferPaths"]) == sorted(
        ["docs/outline.md", "docs/detail.md",
         "ideation/staging/topic-x/other.md"])
    assert b["phase"] == "idle"


def test_one_unsettled_buffer_anywhere_refuses_the_whole_turn(view_results):
    """The settled-identity pre-flight reads EVERY buffer the state holds, not
    the two Phase A named: a widened request declares one identity per buffer it
    carries, so a single unsettled buffer is a single undeclarable identity."""
    u = view_results["oneUnsettled"]
    assert u["refused"] is True
    assert u["transportCalled"] is False
    assert u["error"] == "buffers_unsettled"


# ---- the outline-only turn, the real-corpus majority case -------------------
#
# 16 of 21 real staged topics have exactly ONE editable path — the topic's own
# primary fragment, which the canvas loads as the OUTLINE. Under the v1 wire such
# a turn declared `active_document_path: null` and the reader had to infer that
# the outline was what it was about. It is now DECLARED.

def test_an_outline_only_tile_declares_the_outline_as_its_bound_buffer(
        view_results):
    o = view_results["outlineOnly"]
    assert o["refused"] is False, "the outline-only turn must not be refused"
    assert o["transportCalled"] is True
    assert o["boundBuffer"] == "outline"
    # The field the inference used is not on this envelope at all — the negative
    # F2/D17 asks for, proven at the wire rather than described.
    assert o["hasActiveDocumentPath"] is False
    # the outline is what the turn is bound to, and the document buffer is still
    # carried in its not-yet-created shape
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
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: { outline: OUTLINE_HASH, document: DOCUMENT_HASH },
  assistant_prose: "with proposals", proposals });
const base = editComposer(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"), "go");

let s = settleTurnSuccess(beginTurn(base), successWith([
  proposal("outline", OUTLINE_HASH), proposal("document", DOCUMENT_HASH)]));
s = refreshProposalCurrency(s, { outline: OUTLINE_HASH,
                                 document: DOCUMENT_HASH });

// F4 (adversarial review of the §13 slice): A PROPOSAL AGAINST A PATH-KEYED
// THIRD DOCUMENT, carried through the whole chain the widened wire makes
// possible -- adoption, the card model, and Apply. Every other fixture in this
// suite targets one of the two RESERVED keys, which a two-name literal would
// have served just as well; only a path-keyed target can tell the keyed map from
// the constant it replaced.
const THIRD = "ideation/staging/topic-x/third.md";
const THIRD_HASH = "c".repeat(64);
const wideSuccess = {
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-2", assistant_turn_id: "a-2", model_id: "model-a",
  bound_buffer: THIRD,
  // The RECORD's own buffer set -- which is what the permitted-target rule now
  // reads, instead of a module constant.
  observed_hashes: { outline: OUTLINE_HASH, document: DOCUMENT_HASH,
                     [THIRD]: THIRD_HASH },
  assistant_prose: "a proposal for the loaded document",
  proposals: [proposal(THIRD, THIRD_HASH)] };
let wide = settleTurnSuccess(beginTurn(base), wideSuccess);
wide = refreshProposalCurrency(wide, { outline: OUTLINE_HASH,
                                       document: DOCUMENT_HASH,
                                       [THIRD]: THIRD_HASH });
const wideApplied = [];
const wideActions = createProposalActions({
  applyProposal: async (target) => { wideApplied.push(target); return { ok: true }; } });
const afterWideApply = await wideActions.apply(wide, THIRD);
out.pathKeyedProposal = {
  adoptedKeys: Object.keys(proposalsOf(wide)),
  cards: proposalCardModel(wide).map(
    (card) => ({ target: card.target, label: card.label,
                 ariaLabel: card.ariaLabel, applyEnabled: card.applyEnabled })),
  appliedThrough: wideApplied,
  status: (proposalsOf(afterWideApply)[THIRD] || {}).status || null,
  // …and one that goes STALE re-scores by its own key, like any other.
  staleStatus: (proposalsOf(refreshProposalCurrency(
    wide, { outline: OUTLINE_HASH, document: DOCUMENT_HASH,
            [THIRD]: "d".repeat(64) }))[THIRD] || {}).status || null,
};
// The unroutable half: a target the RECORD did not observe is dropped, never
// rendered with an Apply control.
const unroutable = settleTurnSuccess(beginTurn(base), {
  ...wideSuccess,
  client_turn_id: "t-3",
  proposals: [proposal("ideation/staging/topic-x/never-supplied.md", THIRD_HASH)] });
out.unroutableProposal = { keys: Object.keys(proposalsOf(unroutable)),
                           cards: proposalCardModel(unroutable).length };

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
  applyProposal: async () => ({ ok: false, code: "stale" }) });
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
// W-10: an unsettled buffer is advised a MOMENT, never a new turn
const unsettledActions = createProposalActions({
  applyProposal: async () => ({ ok: false, code: "unsettled" }) });
const afterUnsettled = await unsettledActions.apply(s, "outline");
out.applyUnsettled = {
  error: afterUnsettled.lastFailure && afterUnsettled.lastFailure.error,
  message: afterUnsettled.lastFailure && afterUnsettled.lastFailure.message,
  status: proposalsOf(afterUnsettled).outline.status,
};
// The throwing seam maps to the GENERIC failure (W-10) — and its own detail
// is dropped unread, never echoed into the note.
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


def test_focus_restoration_is_by_identity_not_by_captured_node():
    """T104 F7-3+F7-4 (stated choice): the old pin asserted only
    `"restoreFocus" in source` and `".focus()" in source`, which stayed green
    with the behaviour broken -- and it WAS broken: the handlers captured
    `doc.activeElement`, renderCards() detached that node, and `.focus()` on
    a detached node no-ops, dropping focus to <body>. The behaviour is now
    pinned in the mounted-DOM harness below
    (`focus_throw_results` -- rebuilt-control focus after a refused Apply,
    the composer fallback after a terminal Apply/Reject); this source pin
    keeps only the identity discipline: card actions restore by proposal
    target + role, never by the captured node."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "restoreCardFocus(card.target" in source
    card_actions = source.split('el("button", "doxchat-card-apply"', 1)[1]
    card_actions = card_actions.split("function render()", 1)[0]
    assert "doc.activeElement" not in card_actions, (
        "a card action must not capture the node renderCards() is about to "
        "detach -- identity (target + role) is what survives the rebuild")


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
const unsettled = { active_buffer: "outline", buffers: {
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
  scopeKey: KEY, editorState: unsettled });
out.unsettled = { refused: refusal.refused === true, sent,
                  composer: refusal.state.composer };

// follow-up typing during a slow turn survives settlement
const begun = beginTurn(editComposer(s, "first question"));
const typedDuringFlight = editComposer(begun, "follow-up draft");
const settled = settleTurnSuccess(typedDuringFlight, {
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
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
// A dispatched turn declares its BOUND BUFFER (contract-v1.34), which the
// dispatcher reads off `active_buffer` -- so these scenarios, whose subject is
// abort/settlement rather than the binding itself, carry a selected document.
const DOC_PATH = "docs/detail.md";
const editorState = { active_buffer: "document", buffers: {
  outline: buffer("outline"),
  document: { ...buffer("document"), path: DOC_PATH } } };
const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "on-tenant" },
  bound_buffer: DOC_PATH,
  observed_hashes: { outline: "d".repeat(64), [DOC_PATH]: "d".repeat(64) },
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
    scopeKey: KEY, editorState,
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
    scopeKey: KEY, editorState: unsettled });
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
// The turn declares its BOUND BUFFER (contract-v1.34); this scenario's subject
// is the stale-token mapping, so it selects the tile's own document.
const DOC_PATH = "docs/detail.md";
const editorState = { active_buffer: "document", buffers: {
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
  scopeKey: KEY, editorState });
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


# (T104 F7-3: the old `test_the_send_handler_is_throw_proof_by_construction`
# asserted `source.count("finally") >= 2`, which stayed green with the
# settlement behaviour removed. Its replacement drives the MOUNTED rail --
# `test_a_throwing_chat_turn_seam_settles_the_mounted_rail_back_to_idle` and
# `test_an_unexpected_throw_inside_the_send_path_still_settles_visibly`
# below, against the focus_throw_results harness.)


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
  schema_version: 1, kind: "workbench-chat-turn-v2-success", client_turn_id: "t",
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

// P3-6 (wave re-review P3 tail): a CORRUPTED snapshot through the same door.
// (a) a turn with missing/non-string content used to fabricate the literal
//     string "undefined" (String(t.content)) -- such turns are DROPPED;
// (b) a turn with a foreign role is dropped the same way (well-formed turns
//     only; pair alignment beyond that is the snapshot author's problem);
// (c) an over-bound subject/composer is dropped WHOLE (refused, never
//     truncated -- the same byte rule editSubject/editComposer enforce live).
const corrupted = { ...snap,
  transcript: [
    { role: "human" },                                   // (a) content absent
    { role: "assistant", content: 42 },                  // (a) content non-string
    { role: "system", content: "not a released role" },  // (b) foreign role
    { role: "human", content: "kept" },
    { role: "assistant", content: "also kept" },
  ],
  workingSubject: "s".repeat(513),                       // (c) over the 512 bound
  composer: "c".repeat(16385),                           // (c) over the 16384 bound
};
const cleaned = restoreChatState(createChatState(KEY), corrupted,
  { outline: OUTLINE, document: DOCUMENT });
out.corrupted = {
  turns: transcriptWindow(cleaned).map((t) => [t.role, t.content]),
  subject: cleaned.workingSubject,
  composer: cleaned.composer,
};
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


def test_a_restored_turn_with_missing_or_non_string_content_is_dropped(
        restore_results):
    """P3-6(a) (wave re-review P3 tail): `String(t.content)` fabricated the
    literal string "undefined" for a restored turn whose content was missing
    or non-string -- invented transcript bytes shown as if the operator's
    conversation contained them. Such turns are dropped whole."""
    turns = restore_results["corrupted"]["turns"]
    assert ["human", "undefined"] not in turns
    assert not any("undefined" == content for _, content in turns), turns
    assert not any(content == "42" for _, content in turns), (
        "a non-string content was stringified instead of dropped")


def test_only_well_formed_turns_survive_a_restore(restore_results):
    """P3-6(b): a foreign-role turn is dropped beside the malformed-content
    ones -- only well-formed turns (released role AND string content) survive.
    Pair alignment beyond well-formedness is the snapshot author's problem
    (stated in the module comment); nothing here re-pairs."""
    assert restore_results["corrupted"]["turns"] == [
        ["human", "kept"], ["assistant", "also kept"]]


def test_an_over_bound_restored_subject_or_composer_is_dropped_whole(
        restore_results):
    """P3-6(c): the restore adopted workingSubject/composer on a bare typeof
    with no byte re-check, so a snapshot (hand-edited, or written by a future
    version with different bounds) could seed the live state with text the
    bounds refuse to ever send. Refused-never-truncated: an over-bound
    restored field is dropped whole."""
    assert restore_results["corrupted"]["subject"] == ""
    assert restore_results["corrupted"]["composer"] == ""


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
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
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
  boundBuffer: "document",
  editorState: { active_buffer: "document",
                 buffers: { outline: bufferOf("outline", "docs/outline.md"),
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


def test_a_throwing_apply_seam_maps_to_the_generic_failure(card_results):
    """W-10 (wave re-review): a throw is an internal failure, not staleness —
    the old shared sentence advised "ask again in a new turn" for a condition
    a new turn cannot fix, looping the false advice on a persistently
    throwing seam. The generic sentence is honest and still never echoes."""
    t = card_results["applyThrew"]
    assert t["error"] == "proposal_apply_failed"
    assert "buffer-side detail" not in (t["message"] or ""), (
        "the seam's own error text must be dropped unread, never echoed")
    assert "stays reviewable" in t["message"]
    assert "new turn" not in t["message"]


def test_an_unsettled_apply_is_advised_a_moment_not_a_new_turn(card_results):
    """W-10: the dominant NON-stale refusal — a click while a keystroke's
    identity is still settling — used to claim the proposal no longer
    matched. It matches; a moment's wait is the recovery, and the record
    stays reviewable."""
    u = card_results["applyUnsettled"]
    assert u["error"] == "proposal_apply_unsettled"
    assert "still settling" in u["message"]
    assert "new turn" not in u["message"]
    assert u["status"] == "current"


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
  // annotation round 2 asks WHERE the model selector sits, so the stub records
  // parentage the way every other DOM stub in this suite already does
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  // annotation round 2 reads `aria-describedby` back off the send button, so
  // the stub gains the reader that matches the setter it already had
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
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
const editorState = () => ({ active_buffer: "document", buffers: {
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
    editorState });
  await rail.ready;
  const note = byClass(host, "doxchat-unavailable")[0] || null;
  const selector = byClass(host, "doxchat-model")[0];
  const send = byClass(host, "doxchat-send")[0];
  out.emptyCatalog = {
    noteExists: Boolean(note),
    // annotation round 2: the note is sr-only, not hidden — it is the send
    // button's programmatic description now, so it must stay in the tree
    noteSrOnly: note ? String(note.className).includes("doxchat-sronly") : null,
    noteText: note ? note.textContent : null,
    selectorDisabled: selector.disabled === true,
    selectorInSendRow: Boolean(selector.parentNode
      && String(selector.parentNode.className).includes("doxchat-sendrow")),
    sendDisabled: send.disabled,
    sendTitle: send.title,
    sendDescribedBy: send.getAttribute("aria-describedby"),
    noteId: note ? note.id : null,
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
    editorState });
  const note = byClass(host, "doxchat-unavailable")[0] || null;
  const selector = byClass(host, "doxchat-model")[0];
  // P3-8: the mount-to-catalog window's own words are part of the pin -- the
  // rail must not claim a configuration fact ("no approved model is
  // configured") it cannot know until the one-shot catalog ready settles.
  const beforeCatalog = { noteText: note ? note.textContent : null,
                          selectorDisabled: selector.disabled === true };
  resolveCatalog({ schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] });
  await rail.ready;
  out.lateCatalog = {
    beforeCatalog,
    noteText: note ? note.textContent : null,
    selectorDisabled: selector.disabled === true,
    options: selector.children.map((o) => o.value),
  };
}

// ---- F5-5: a refused Apply renders a failure note and announces it ----
{
  const host = new Node("div"); host.ownerDocument = doc;
  const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
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
    editorState,
    applyProposal: async () => ({ ok: false, code: "stale",
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
    """F5-9 residual: the rail must not look fully live when no model is
    available. Send stays disabled and the reason is STATED.

    PIN EVOLUTION (Brett's 2026-08-18 annotation round 2: "add a model selector
    down next to the send button. make this text the hover text for the send
    button if no model selected"). Two halves of this pin moved. The note no
    longer STANDS as a visible line — it is sr-only, and its sentence is the
    send button's `title` and its `aria-describedby` target, which is where a
    human trying to send actually looks. And the selector no longer HIDES when
    nothing is selectable: it is a permanent part of the send row, rendered
    empty and DISABLED, which is the honest shape of this plane's posture (the
    server answers with a catalog, and the catalog is empty). What has not
    changed is the rule the pin exists for: the rail never looks live when it
    is not, and the reason is legible."""
    e = rail_dom_results["emptyCatalog"]
    assert e["noteExists"] is True
    assert e["noteSrOnly"] is True
    assert "chat is unavailable" in e["noteText"]
    assert "no approved model" in e["noteText"]
    # the selector is present, beside Send, and inert
    assert e["selectorInSendRow"] is True
    assert e["selectorDisabled"] is True
    assert e["sendDisabled"] is True
    # …and Brett's sentence IS the send button's hover text, and is associated
    # programmatically rather than by title alone
    assert e["sendTitle"] == e["noteText"]
    assert e["sendDescribedBy"] == e["noteId"]
    assert e["noteId"]


def test_a_catalog_arriving_later_replaces_the_note_with_the_live_selector(
        rail_dom_results):
    l = rail_dom_results["lateCatalog"]
    # before the catalog resolves the rail is honest about having no model
    assert "checking the model catalog" in l["beforeCatalog"]["noteText"]
    assert l["beforeCatalog"]["selectorDisabled"] is True
    # the rail was never unmounted, so the arriving catalog lights it up
    # a catalog with an available entry clears the reason and enables the
    # selector in place (annotation round 2: it never hid, so it never unhides)
    assert l["noteText"] == ""
    assert l["selectorDisabled"] is False
    assert "model-a" in l["options"]


def test_the_mount_to_catalog_window_reads_the_loading_sentence(
        rail_dom_results):
    """P3-8 (wave re-review P3 tail): the rail seeded CHAT_UNAVAILABLE_NOTE
    ("no approved model is configured") BEFORE the catalog had answered -- a
    configuration claim the page could not yet know, wrong for the whole
    fetch window on every capable plane. Until the one-shot ready settles
    (adopt or failure) the note reads a fixed loading sentence; the settled
    three-way posture (configured-none / stale token / unreadable) is pinned
    unchanged by the surrounding tests."""
    before = rail_dom_results["lateCatalog"]["beforeCatalog"]
    assert "checking the model catalog" in (before["noteText"] or "")
    assert "no approved model" not in (before["noteText"] or ""), (
        "the mount-to-catalog window claimed a configuration fact it "
        "cannot know yet")
    # and once the catalog settles empty, the configured-none sentence stands
    settled = rail_dom_results["emptyCatalog"]
    assert "no approved model" in settled["noteText"]


def test_a_path_keyed_proposal_is_adopted_rendered_and_applied(card_results):
    """F4: judgment call 9's claimed failure mode, MEASURED rather than asserted.

    Before the keyed map, `adoptProposals` filtered against a two-name literal
    and `proposalCardModel` enumerated the same two names — so a proposal against
    the third document a human loaded was dropped in silence: no record, no card,
    no Apply, and no refusal either. Every other fixture in this suite targets a
    RESERVED key, which the old literal served just as well, so nothing measured
    the difference."""
    r = card_results["pathKeyedProposal"]
    third = "ideation/staging/topic-x/third.md"
    assert r["adoptedKeys"] == [third], (
        "the record's own observed buffers are the permitted set")
    assert [card["target"] for card in r["cards"]] == [third]
    # The BADGE reads as a name a human recognizes; the full key stays available
    # to assistive technology, so two loaded documents sharing a basename are
    # never indistinguishable.
    assert r["cards"][0]["label"] == "third.md"
    assert third in r["cards"][0]["ariaLabel"]
    assert r["cards"][0]["applyEnabled"] is True
    # …and Apply routes to the seam under that key, then marks it applied.
    assert r["appliedThrough"] == [third]
    assert r["status"] == "applied"
    # Currency is per key like any other: move that buffer, that card goes stale.
    assert r["staleStatus"] == "stale"


def test_a_proposal_the_turn_did_not_observe_is_dropped_not_rendered(card_results):
    """The other half of the same rule: the permitted set is the RECORD's own
    buffer set, so an unroutable target is dropped rather than guessed at — and
    dropped means no card, which is the delta's "MUST NOT be rendered with an
    Apply control"."""
    r = card_results["unroutableProposal"]
    assert r["keys"] == []
    assert r["cards"] == 0


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


# ---------------------------------------------------------------------------
# T104 F7-3 + F7-4 + F10-1 (rail half) + F10-2/4: the MOUNTED rail, driven
# against a fake DOM that models the two browser facts the findings turn on:
#
#   * FOCUS follows connectedness. `focus()` on a detached node no-ops, and a
#     focused node that is detached loses focus (activeElement -> null here,
#     <body> in a browser). This is what made the old captured-node
#     restoreFocus a silent no-op after every card action (F7-4).
#   * textContent = "" DETACHES the previous children -- renderCards()'s
#     rebuild is exactly that.
#
# One node process, one JSON blob, same instrument as _RAIL_DOM_HARNESS.
# ---------------------------------------------------------------------------

_FOCUS_THROW_HARNESS = """
const doc = { activeElement: null };

function isConnected(node) {
  let n = node;
  while (n) {
    if (n.__root) return true;
    n = n.parentNode;
  }
  return false;
}

class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.hidden = false;
    this._disabled = false; this.value = ''; this.parentNode = null;
    this.title = ''; this.type = '';
  }
  // P3-7's third browser fact, beside connectedness and detach-on-rebuild:
  // DISABLING the focused control drops focus (activeElement -> <body> in a
  // browser, null here). This is exactly what happens to the Send button the
  // moment a send settles successfully -- the composer clears, canSend goes
  // false, render() disables it -- so a captured-node restore has nowhere
  // honest to land.
  get disabled() { return this._disabled; }
  set disabled(v) {
    this._disabled = !!v;
    if (this._disabled && doc.activeElement === this) doc.activeElement = null;
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) {
    for (const child of this.children) child._detach();
    this.children = []; this._text = String(value);
  }
  _detach() {
    this.parentNode = null;
    if (doc.activeElement === this) doc.activeElement = null;
    for (const child of this.children) child._detach();
  }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  // annotation round 2 reads `aria-describedby` back off the send button, so
  // the stub gains the reader that matches the setter it already had
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() {
    // a real browser refuses focus on detached or disabled controls
    if (!isConnected(this) || this.disabled === true) return;
    doc.activeElement = this;
  }
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
}
doc.createElement = (tag) => new Node(tag);
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const fire = async (node, type) => {
  for (const fn of node.listeners[type] || []) await fn({});
};

import { mountDoxBenchChatRail } from "./doxbench-chat.mjs";
import { MAX_MESSAGE_BYTES, MAX_WORKING_SUBJECT_BYTES }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const GOOD_CATALOG = async () => ({ schema_version: 1,
  kind: "workbench-model-catalog", models: [ENTRY] });
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "# " + kind, dirty: false });
const editorState = () => ({ active_buffer: "document", buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md") } });
const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
  assistant_prose: "answer",
  proposals: [{ target: "outline", base_hash: "d".repeat(64),
                summary: "Rework the outline", content: "# New outline" }] };

function mountRail(overrides = {}) {
  const host = new Node("div");
  host.__root = true;
  host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: overrides.catalog || GOOD_CATALOG,
      chatTurn: overrides.chatTurn
        || (async () => ({ ok: true, status: 200, payload: SUCCESS })) },
    // P3-3 needs a LIVE editor-state provider whose identities can move
    // between submit and settle; every other scenario keeps the fixed one.
    editorState: overrides.editorState || editorState,
    applyProposal: overrides.applyProposal || (async () => ({ ok: true })),
    // The tile title the shell hands down. Left ABSENT by default so every
    // pre-existing scenario keeps mounting with an empty subject box.
    subjectDefault: overrides.subjectDefault,
    onState: overrides.onState });
  return { host, rail };
}

async function propose(host) {
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "please propose"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
}

// ---- F7-4(a): a REFUSED Apply restores focus to the REBUILT Apply control ----
{
  const { host, rail } = mountRail({
    applyProposal: async () => ({ ok: false }) });
  await rail.ready;
  await propose(host);
  const applyBefore = byClass(host, "doxchat-card-apply")[0];
  applyBefore.focus();
  await fire(applyBefore, "click");
  const applyAfter = byClass(host, "doxchat-card-apply")[0];
  out.refusedApplyFocus = {
    rebuilt: applyAfter !== applyBefore,
    afterEnabled: applyAfter.disabled === false,
    activeIsRebuiltApply: doc.activeElement === applyAfter,
    activeIsStaleNode: doc.activeElement === applyBefore,
    activeIsNull: doc.activeElement === null,
  };
}

// ---- F7-4(b): a SUCCESSFUL Apply terminalizes the card (both actions
// disabled), so focus falls back to the stated survivor: the composer ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  const apply = byClass(host, "doxchat-card-apply")[0];
  apply.focus();
  await fire(apply, "click");
  out.appliedFocus = {
    applyDisabled: byClass(host, "doxchat-card-apply")[0].disabled,
    activeIsComposer:
      doc.activeElement === byClass(host, "doxchat-composer")[0],
    activeIsNull: doc.activeElement === null,
  };
}

// ---- F7-4(c): Reject terminalizes too -- same composer fallback ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  const reject = byClass(host, "doxchat-card-reject")[0];
  reject.focus();
  await fire(reject, "click");
  out.rejectedFocus = {
    rejectDisabled: byClass(host, "doxchat-card-reject")[0].disabled,
    activeIsComposer:
      doc.activeElement === byClass(host, "doxchat-composer")[0],
  };
}

// ---- F7-3(a): a THROWING chatTurn seam settles the mounted rail ----
{
  const { host, rail } = mountRail({
    chatTurn: async () => { throw new Error("socket died: private detail"); } });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "still here?"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const note = byClass(host, "doxchat-failure")[0];
  const send = byClass(host, "doxchat-send")[0];
  out.throwingTurn = {
    phase: rail.state().phase,
    error: rail.state().lastFailure && rail.state().lastFailure.error,
    noteHidden: note.hidden,
    noteText: note.textContent,
    composer: composer.value,
    sendDisabled: send.disabled,
    sendLabel: send.textContent,
  };
  // P3-4's negative half: a TURN failure is not a present-tense claim about
  // the composer's text, so typing must NOT clear it (only the over-bound
  // notes gained the same-field clear).
  composer.value = "typed after the failure"; await fire(composer, "input");
  out.throwingTurn.failureAfterTyping =
    rail.state().lastFailure && rail.state().lastFailure.error;
}

// ---- F7-3(b): an UNEXPECTED throw past the dispatcher's own catches (here:
// a render callback exploding mid-flight) still settles to the visible
// failed-idle state -- the finally-discipline, exercised rather than
// grepped-for ----
{
  let armed = true;
  const mounted = mountRail({
    onState: (s) => {
      if (armed && s.phase === "in_flight") {
        armed = false;
        throw new Error("render exploded mid-flight");
      }
    } });
  await mounted.rail.ready;
  const selector = byClass(mounted.host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(mounted.host, "doxchat-composer")[0];
  composer.value = "does this wedge?"; await fire(composer, "input");
  let escaped = null;
  try {
    await fire(byClass(mounted.host, "doxchat-send")[0], "click");
  } catch (error) {
    escaped = String((error && error.message) || error);
  }
  const note = byClass(mounted.host, "doxchat-failure")[0];
  const send = byClass(mounted.host, "doxchat-send")[0];
  out.sendPathThrow = {
    escaped,
    phase: mounted.rail.state().phase,
    error: mounted.rail.state().lastFailure
      && mounted.rail.state().lastFailure.error,
    noteHidden: note.hidden,
    composer: composer.value,
    sendDisabled: send.disabled,
    sendLabel: send.textContent,
  };
}

// ---- F10-1: the catalog loader's DISTINGUISHED failures render honest
// postures (the transport contract: { failed: "console_required" | "unreadable" }) ----
async function catalogPosture(catalog) {
  const { host, rail } = mountRail({ catalog });
  await rail.ready;
  const note = byClass(host, "doxchat-unavailable")[0];
  const selector = byClass(host, "doxchat-model")[0];
  const send = byClass(host, "doxchat-send")[0];
  return {
    // annotation round 2: the note is sr-only and the selector is disabled
    // rather than hidden, so the posture is read off those two facts plus the
    // send button's own stated reason
    noteSrOnly: String(note.className).includes("doxchat-sronly"),
    noteText: note.textContent,
    selectorDisabled: selector.disabled === true,
    sendDisabled: send.disabled,
    sendTitle: send.title,
  };
}
out.staleTokenCatalog = await catalogPosture(
  async () => ({ failed: "console_required" }));
out.unreadableCatalog = await catalogPosture(
  async () => ({ failed: "unreadable" }));
out.throwingCatalog = await catalogPosture(
  async () => { throw new Error("connection refused: private detail"); });
out.configuredNoneCatalog = await catalogPosture(
  async () => ({ schema_version: 1, kind: "workbench-model-catalog",
                 models: [] }));

// ---- F10-2/4: the over-bound paste is refused VISIBLY, never truncated ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  const composer = byClass(host, "doxchat-composer")[0];
  const subject = byClass(host, "doxchat-subject")[0];
  const note = byClass(host, "doxchat-failure")[0];

  // an in-bound edit first: no failure invented
  composer.value = "a fair question"; await fire(composer, "input");
  out.inBoundEdit = {
    composer: rail.state().composer,
    failure: rail.state().lastFailure,
  };

  // the over-bound paste: refused, reverted, and SAID
  composer.value = "x".repeat(MAX_MESSAGE_BYTES + 1);
  await fire(composer, "input");
  out.overBoundComposer = {
    noteHidden: note.hidden,
    noteText: note.textContent,
    ariaLive: note.attributes["aria-live"],
    error: rail.state().lastFailure && rail.state().lastFailure.error,
    domReverted: composer.value,
    stateComposer: rail.state().composer,
    echoed: note.textContent.includes("xxx"),
  };

  // the subject bound gets its own naming
  subject.value = "y".repeat(MAX_WORKING_SUBJECT_BYTES + 1);
  await fire(subject, "input");
  out.overBoundSubject = {
    noteText: note.textContent,
    error: rail.state().lastFailure && rail.state().lastFailure.error,
    domReverted: subject.value,
    stateSubject: rail.state().workingSubject,
    echoed: note.textContent.includes("yyy"),
  };

  // P3-4: an in-bound edit of a DIFFERENT field leaves the standing note
  // alone -- the composer's shortening says nothing about the subject's bound
  composer.value = "a shorter question"; await fire(composer, "input");
  out.inBoundAfterRefusal = {
    composer: rail.state().composer,
    error: rail.state().lastFailure && rail.state().lastFailure.error,
  };

  // P3-4: the SAME-FIELD in-bound edit clears ITS OWN over-bound note -- the
  // note is a present-tense claim ("this working subject exceeds...") that
  // went false the moment the text fit the bound
  subject.value = "a subject that fits"; await fire(subject, "input");
  out.inBoundSubjectClears = {
    subject: rail.state().workingSubject,
    error: (rail.state().lastFailure && rail.state().lastFailure.error) || null,
    noteHidden: note.hidden,
  };

  // ...and the composer's own bound behaves identically
  composer.value = "x".repeat(MAX_MESSAGE_BYTES + 1);
  await fire(composer, "input");
  const messageFailureBack =
    rail.state().lastFailure && rail.state().lastFailure.error;
  composer.value = "short again"; await fire(composer, "input");
  out.inBoundComposerClears = {
    messageFailureBack,
    error: (rail.state().lastFailure && rail.state().lastFailure.error) || null,
    noteHidden: note.hidden,
  };
}

// ---- W-11: a LANDED Apply clears the failure its refusal left behind ----
{
  let calls = 0;
  const { host, rail } = mountRail({
    applyProposal: async () => (++calls === 1 ? { ok: false } : { ok: true }) });
  await rail.ready;
  await propose(host);
  await fire(byClass(host, "doxchat-card-apply")[0], "click"); // refused
  const refusedVisible = !byClass(host, "doxchat-failure")[0].hidden;
  await fire(byClass(host, "doxchat-card-apply")[0], "click"); // lands
  out.applyClearsFailure = {
    refusedVisible,
    afterError: (rail.state().lastFailure
                 && rail.state().lastFailure.error) || null,
    noteHidden: byClass(host, "doxchat-failure")[0].hidden,
    proposalStatus: (rail.state().proposals["outline"] || {}).status || null,
  };
}

// ---- W-3(a): follow-up typing during a slow Apply SURVIVES, and the
// proposal still lands applied -- the card actions settle against the LIVE
// state, never the click-time snapshot ----
{
  let releaseApply;
  const gate = new Promise((resolve) => { releaseApply = resolve; });
  const { host, rail } = mountRail({
    applyProposal: async () => { await gate; return { ok: true }; } });
  await rail.ready;
  await propose(host);
  const apply = byClass(host, "doxchat-card-apply")[0];
  const clickSettled = fire(apply, "click");        // the seam is in flight
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "typed during the apply await";
  await fire(composer, "input");
  releaseApply();
  await clickSettled;
  out.applyRace = {
    composerState: rail.state().composer,
    composerDom: byClass(host, "doxchat-composer")[0].value,
    proposalStatus: (rail.state().proposals["outline"] || {}).status || null,
  };
}

// ---- W-3(b): an Apply spanning a TURN SETTLEMENT never resurrects the dead
// flight -- pre-fix this adopted the in-flight snapshot: phase came back
// "in_flight" with nothing in the air, the settled answer vanished from the
// transcript, and Send read "Sending…" forever ----
{
  let releaseApply;
  const gate = new Promise((resolve) => { releaseApply = resolve; });
  let turnCalls = 0;
  let releaseTurn;
  const turnGate = new Promise((resolve) => { releaseTurn = resolve; });
  const { host, rail } = mountRail({
    applyProposal: async () => { await gate; return { ok: true }; },
    chatTurn: async () => {
      turnCalls += 1;
      if (turnCalls > 1) await turnGate;            // only turn 2 is slow
      return { ok: true, status: 200, payload: SUCCESS };
    } });
  await rail.ready;
  await propose(host);                              // turn 1: proposals render
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "a follow-up question"; await fire(composer, "input");
  const turnSettled = fire(byClass(host, "doxchat-send")[0], "click");
  const apply = byClass(host, "doxchat-card-apply")[0];
  const applySettled = fire(apply, "click");        // Apply spans the flight
  releaseTurn();
  await turnSettled;                                // turn 2 settles mid-Apply
  releaseApply();
  await applySettled;
  const send = byClass(host, "doxchat-send")[0];
  out.applyAcrossSettlement = {
    phase: rail.state().phase,
    transcriptTurns: rail.state().transcript.length,
    sendLabel: send.textContent,
  };
}

// ---- P3-3: a turn settling AFTER the active buffer moved re-scores its
// just-adopted proposals against the LIVE editor identities -- the identity
// event that would have re-scored them fired BEFORE they existed ----
{
  let currentHex = "d".repeat(64);
  const liveEditorState = () => ({ active_buffer: "document", buffers: {
    outline: { ...bufferOf("outline", "docs/outline.md"),
               current_hash: { algorithm: "sha256", hex: currentHex } },
    document: bufferOf("document", "docs/detail.md") } });
  let releaseTurn;
  const turnGate = new Promise((resolve) => { releaseTurn = resolve; });
  const { host, rail } = mountRail({
    editorState: liveEditorState,
    chatTurn: async () => { await turnGate;
      return { ok: true, status: 200, payload: SUCCESS }; } });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "please propose"; await fire(composer, "input");
  const sendSettled = fire(byClass(host, "doxchat-send")[0], "click");
  currentHex = "e".repeat(64);   // the buffer identity moves DURING the flight
  releaseTurn();
  await sendSettled;
  const applyBtn = byClass(host, "doxchat-card-apply")[0] || null;
  out.settleTimeCurrency = {
    status: (rail.state().proposals.outline || {}).status || null,
    applyDisabled: applyBtn ? applyBtn.disabled : null,
  };
}

// ---- CODEX-4 (Codex review of PR #210): the settlement re-score must cover
// EVERY live buffer, not the two Phase A named. Both scenarios below are chosen
// to DISCRIMINATE — each one's answer differs before and after the fix, which a
// scenario whose answer happens to match by accident cannot do:
//   (c) the reserved slot is PRESENT and the path-keyed buffer did NOT move.
//       Before: the re-score ran with a two-key map, so that buffer scored
//       against `undefined` and the card came back falsely STALE.
//   (d) the reserved slot is ABSENT and the path-keyed buffer DID move.
//       Before: the guard read `buffers.document`, found nothing, and skipped the
//       re-score entirely — the card stayed CURRENT with an enabled Apply
//       against text the buffer no longer held, which is Codex's own reading.
{
  const LOADED = 'ideation/staging/topic-x/loaded.md';
  const withReservedSlot = () => ({ active_buffer: LOADED, buffers: {
    outline: bufferOf('outline', 'docs/outline.md'),
    document: bufferOf('document', 'docs/detail.md'),
    [LOADED]: bufferOf('document', LOADED) } });
  const SUCCESS_C = {
    schema_version: 1, kind: 'workbench-chat-turn-v2-success',
    client_turn_id: 't', assistant_turn_id: 'a', model_id: 'model-a',
    bound_buffer: LOADED,
    observed_hashes: { outline: 'd'.repeat(64), document: 'd'.repeat(64),
                       [LOADED]: 'd'.repeat(64) },
    assistant_prose: 'answer',
    proposals: [{ target: LOADED, base_hash: 'd'.repeat(64),
                  summary: 'Rework the loaded document',
                  content: '# New loaded document' }] };
  const { host, rail } = mountRail({
    editorState: withReservedSlot,
    chatTurn: async () => ({ ok: true, status: 200, payload: SUCCESS_C }) });
  await rail.ready;
  const selector = byClass(host, 'doxchat-model')[0];
  selector.value = 'model-a'; await fire(selector, 'change');
  const composer = byClass(host, 'doxchat-composer')[0];
  composer.value = 'please propose'; await fire(composer, 'input');
  await fire(byClass(host, 'doxchat-send')[0], 'click');
  const applyBtn = byClass(host, 'doxchat-card-apply')[0] || null;
  out.unmovedLoadedCurrency = {
    status: (rail.state().proposals[LOADED] || {}).status || null,
    applyDisabled: applyBtn ? applyBtn.disabled : null,
  };
}
{
  const LOADED = 'ideation/staging/topic-x/loaded.md';
  let loadedHex = 'd'.repeat(64);
  // NO reserved `document` slot: the shape a session holds once its create was
  // re-keyed onto a path.
  const noReservedSlot = () => ({ active_buffer: LOADED, buffers: {
    outline: bufferOf('outline', 'docs/outline.md'),
    [LOADED]: { ...bufferOf('document', LOADED),
                current_hash: { algorithm: 'sha256', hex: loadedHex } } } });
  const SUCCESS_D = {
    schema_version: 1, kind: 'workbench-chat-turn-v2-success',
    client_turn_id: 't', assistant_turn_id: 'a', model_id: 'model-a',
    bound_buffer: LOADED,
    observed_hashes: { outline: 'd'.repeat(64), [LOADED]: 'd'.repeat(64) },
    assistant_prose: 'answer',
    proposals: [{ target: LOADED, base_hash: 'd'.repeat(64),
                  summary: 'Rework the loaded document',
                  content: '# New loaded document' }] };
  let releaseTurn;
  const turnGate = new Promise((resolve) => { releaseTurn = resolve; });
  const { host, rail } = mountRail({
    editorState: noReservedSlot,
    chatTurn: async () => { await turnGate;
      return { ok: true, status: 200, payload: SUCCESS_D }; } });
  await rail.ready;
  const selector = byClass(host, 'doxchat-model')[0];
  selector.value = 'model-a'; await fire(selector, 'change');
  const composer = byClass(host, 'doxchat-composer')[0];
  composer.value = 'please propose'; await fire(composer, 'input');
  const sendSettled = fire(byClass(host, 'doxchat-send')[0], 'click');
  loadedHex = 'e'.repeat(64);   // the LOADED buffer moves DURING the flight
  releaseTurn();
  await sendSettled;
  const applyBtn = byClass(host, 'doxchat-card-apply')[0] || null;
  out.movedLoadedCurrency = {
    status: (rail.state().proposals[LOADED] || {}).status || null,
    applyDisabled: applyBtn ? applyBtn.disabled : null,
    hasReservedSlot: Object.prototype.hasOwnProperty.call(
      noReservedSlot().buffers, 'document'),
  };
}

// ---- P3-7: send-path focus by INTENT, not by captured node. A successful
// send clears the composer, canSend goes false, render() disables Send --
// the captured node can no longer take focus, and the keyboard operator
// landed on <body> ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "a successful send"; await fire(composer, "input");
  const send = byClass(host, "doxchat-send")[0];
  send.focus();
  await fire(send, "click");
  out.successSendFocus = {
    sendDisabled: send.disabled,
    activeIsComposer:
      doc.activeElement === byClass(host, "doxchat-composer")[0],
    activeIsNull: doc.activeElement === null,
  };
}

// ---- P3-7's failure half: a FAILED send preserves the composer and
// re-enables Send -- a keyboard operator who was ON Send stays there ----
{
  const FAILURE = { ok: false, status: 502, payload: {
    schema_version: 1, kind: "workbench-chat-turn-v2-failure",
    client_turn_id: "t", error: "model_failed",
    message: "the model request failed" } };
  const { host, rail } = mountRail({ chatTurn: async () => FAILURE });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "a failing send"; await fire(composer, "input");
  const send = byClass(host, "doxchat-send")[0];
  send.focus();
  await fire(send, "click");
  out.failedSendFocus = {
    sendDisabled: send.disabled,
    activeIsSend: doc.activeElement === send,
  };
  // ...and one whose focus was NOT on Send lands on the composer, where the
  // preserved message is edited for the retry
  const second = mountRail({ chatTurn: async () => FAILURE });
  await second.rail.ready;
  const selector2 = byClass(second.host, "doxchat-model")[0];
  selector2.value = "model-a"; await fire(selector2, "change");
  const composer2 = byClass(second.host, "doxchat-composer")[0];
  composer2.value = "another failing send"; await fire(composer2, "input");
  composer2.focus();
  await fire(byClass(second.host, "doxchat-send")[0], "click");
  out.failedSendFocusElsewhere = {
    activeIsComposer: doc.activeElement === composer2,
  };
}

// ---- the promoted working-subject default, ON THE MOUNTED RAIL: the box the
// human sees opens carrying the tile's title, and stays editable ----
{
  const TITLE = "keyword lens and edge degree";
  const { host, rail } = mountRail({ subjectDefault: TITLE });
  await rail.ready;
  const subject = byClass(host, "doxchat-subject")[0];
  const seededValue = subject.value;
  const seededState = rail.state().workingSubject;
  // …and it is a DEFAULT, not a fixed label: typing replaces it, and emptying
  // it empties it (the placeholder is what shows then).
  subject.value = "why does the funnel disagree with the wheel?";
  await fire(subject, "input");
  const typed = rail.state().workingSubject;
  subject.value = "";
  await fire(subject, "input");
  out.seededSubject = {
    seededValue, seededState, typed,
    cleared: rail.state().workingSubject,
    clearedValue: subject.value,
    placeholder: subject.attributes.placeholder,
    // the human's 512-byte refusal is untouched by the seed
    ariaLabel: subject.attributes["aria-label"],
  };
}
// …and a rail mounted with NO default still opens empty, so the placeholder
// path the annotation round added is not a dead branch.
{
  const { host, rail } = mountRail({});
  await rail.ready;
  const subject = byClass(host, "doxchat-subject")[0];
  out.unseededSubject = { value: subject.value,
                          state: rail.state().workingSubject,
                          placeholder: subject.attributes.placeholder };
}
// …and a tile title the 512-byte bound refuses seeds NOTHING, never a clipped
// prefix: the box opens empty and sendable rather than holding text the human
// never typed and the field itself would refuse.
{
  const { host, rail } = mountRail({
    subjectDefault: "t".repeat(MAX_WORKING_SUBJECT_BYTES + 1) });
  await rail.ready;
  const subject = byClass(host, "doxchat-subject")[0];
  out.overLongSeed = { value: subject.value,
                       state: rail.state().workingSubject,
                       failure: rail.state().lastFailure };
}
// ---- BRETT'S SCENARIO, THE CLIENT HALF (Amendment 2 follow-up 1) ----------
// A set unloaded down to the outline refuses AT SEND, and what the human reads
// is the SERVER's sentence, verbatim -- not a marker the rail substitutes for
// it. That distinction is live, not hypothetical: the CATALOG failure path
// deliberately re-normalizes server text into a two-value vocabulary
// (`recordCatalogFailure`), so "the rail renders whatever the route said" is a
// property of THIS channel that a future tidy-up could quietly remove, taking
// the whole improvement with it.
//
// The expected string is injected from `serve.py`'s own constant, so the rail
// and the route cannot drift into saying different things about one state.
{
  const NO_DOCUMENT_FAILURE = {
    schema_version: 1, kind: "workbench-chat-turn-v2-failure",
    client_turn_id: "t-1", error: "invalid_turn_request",
    message: __NO_DOCUMENT_MESSAGE__ };
  const { host, rail } = mountRail({
    chatTurn: async () => ({ ok: false, status: 400,
                             payload: NO_DOCUMENT_FAILURE }) });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "which open question should we close next?";
  await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const note = byClass(host, "doxchat-failure")[0];
  out.noDocumentRefusal = {
    phase: rail.state().phase,
    error: rail.state().lastFailure && rail.state().lastFailure.error,
    noteHidden: note.hidden,
    noteText: note.textContent,
    composer: composer.value,
    composerState: rail.state().composer,
  };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def focus_throw_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the mounted-rail focus/throw probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-focus-throw")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "focus-throw-harness.mjs"
    # The route's OWN sentence, carried into the browser probe rather than
    # retyped: a copy here would let the two halves drift and still pass.
    harness.write_text(
        _FOCUS_THROW_HARNESS.replace(
            "__NO_DOCUMENT_MESSAGE__",
            json.dumps(serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)),
        encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_refused_apply_keeps_focus_on_the_rebuilt_apply_control(
        focus_throw_results):
    """F7-4: the card stays reviewable after a refused Apply, so the REBUILT
    Apply button (same proposal target, same role) is where keyboard focus
    must land -- the old captured-node restore no-opped on the detached node
    and focus fell to <body>."""
    f = focus_throw_results["refusedApplyFocus"]
    assert f["rebuilt"] is True, "precondition: renderCards really rebuilt"
    assert f["afterEnabled"] is True, "precondition: the card stays actionable"
    assert f["activeIsStaleNode"] is False
    assert f["activeIsNull"] is False, "focus dropped to <body> -- the finding"
    assert f["activeIsRebuiltApply"] is True


def test_a_terminal_apply_falls_back_to_the_composer(focus_throw_results):
    """F7-4, the stated fallback: an applied card disables both its actions,
    so the equivalent control cannot take focus -- the composer is the
    surviving control the operator acts through next (every terminal note
    names a NEW TURN as the only continuation)."""
    a = focus_throw_results["appliedFocus"]
    assert a["applyDisabled"] is True, "precondition: the card terminalized"
    assert a["activeIsNull"] is False
    assert a["activeIsComposer"] is True


def test_a_reject_falls_back_to_the_composer_too(focus_throw_results):
    r = focus_throw_results["rejectedFocus"]
    assert r["rejectDisabled"] is True
    assert r["activeIsComposer"] is True


def test_a_throwing_chat_turn_seam_settles_the_mounted_rail_back_to_idle(
        focus_throw_results):
    """F7-3 replacement, half one: the mounted rail driven with a THROWING
    chatTurn seam. The phase settles back to idle, the composer is preserved
    verbatim, Send re-enables (labelled Send again, not a dead Sending...),
    the fixed failure note renders, and the seam's own error text is dropped
    unread."""
    t = focus_throw_results["throwingTurn"]
    assert t["phase"] == "idle"
    assert t["error"] == "transport_refused"
    assert t["noteHidden"] is False
    assert "socket died" not in t["noteText"], "the throw's text must be dropped"
    assert t["composer"] == "still here?"
    assert t["sendDisabled"] is False
    assert t["sendLabel"] == "Send"


def test_an_unexpected_throw_inside_the_send_path_still_settles_visibly(
        focus_throw_results):
    """F7-3 replacement, half two -- the wedge class the old
    `count("finally") >= 2` grep claimed to cover: a throw PAST the
    dispatcher's own catches (a render callback exploding mid-flight) must
    never leave the rail wedged in_flight with a dead Send. The
    finally-discipline settles it to the fixed failed-idle state, composer
    preserved."""
    s = focus_throw_results["sendPathThrow"]
    assert s["escaped"], "precondition: the throw really escaped the dispatcher"
    assert s["phase"] == "idle"
    assert s["error"] == "send_path_failed"
    assert s["noteHidden"] is False
    assert s["composer"] == "does this wedge?"
    assert s["sendDisabled"] is False
    assert s["sendLabel"] == "Send"


def test_a_stale_console_token_catalog_failure_names_the_reload_remedy(
        focus_throw_results):
    """F10-1: a 403 console_required/agent_invocation catalog refusal (the
    transport's { failed: "console_required" }) renders the SAME recoverable
    stale-token vocabulary R-3 uses on the chat-turn path -- never the
    configured-none misdiagnosis."""
    s = focus_throw_results["staleTokenCatalog"]
    # PIN EVOLUTION (annotation round 2): the sentence is sr-only and is the
    # send button's hover text; the selector is present-and-disabled rather than
    # hidden. WHICH sentence each failure carries — the whole point of F10-1 —
    # is unchanged.
    assert s["noteSrOnly"] is True
    assert "console token is stale" in s["noteText"]
    assert "reload" in s["noteText"]
    assert "no approved model" not in s["noteText"]
    assert s["sendTitle"] == s["noteText"]
    assert s["selectorDisabled"] is True
    assert s["sendDisabled"] is True


def test_an_unreadable_catalog_gets_its_own_fixed_sentence(focus_throw_results):
    """F10-1: a 500 (or any other non-token failure) renders the
    could-not-be-read posture -- a fixed sentence DISTINCT from "no approved
    model is configured", because "nothing is configured" and "the answer
    could not be read" are different facts with different remedies."""
    u = focus_throw_results["unreadableCatalog"]
    assert u["noteSrOnly"] is True
    assert "could not be read" in u["noteText"]
    assert "no approved model" not in u["noteText"]
    assert u["sendTitle"] == u["noteText"]
    assert u["selectorDisabled"] is True
    assert u["sendDisabled"] is True


def test_a_throwing_catalog_transport_reads_as_unreadable_not_configured_none(
        focus_throw_results):
    t = focus_throw_results["throwingCatalog"]
    assert t["noteSrOnly"] is True
    assert "could not be read" in t["noteText"]
    assert "connection refused" not in t["noteText"], "no echoed error text"
    assert "no approved model" not in t["noteText"]


def test_an_empty_catalog_keeps_the_configured_none_note(focus_throw_results):
    """models: [] is a SUCCESS (FR-025) and keeps the existing editor-only
    sentence -- the two failure postures above must not absorb it."""
    e = focus_throw_results["configuredNoneCatalog"]
    assert e["noteSrOnly"] is True
    assert "no approved model is configured" in e["noteText"]
    assert "could not be read" not in e["noteText"]
    # …and this is the sentence Brett pointed at: it is the send button's hover
    # text now (annotation round 2), not a standing line
    assert e["sendTitle"] == e["noteText"]


def test_an_over_bound_composer_paste_renders_and_announces_the_bound(
        focus_throw_results):
    """F10-2: the over-bound paste was refused by the model (identical state)
    and reverted by render()'s value reassignment -- correct, but SILENT: the
    pasted text vanished with nothing said. The refusal now lands on the
    aria-live failure note in fixed vocabulary naming the BOUND, never the
    text; refused-never-truncated stands."""
    o = focus_throw_results["overBoundComposer"]
    assert o["noteHidden"] is False
    assert o["ariaLive"] == "polite", "the note must be an announced region"
    assert str(16_384) in o["noteText"], "the note names the message bound"
    assert o["error"] == "message_over_bound"
    assert o["echoed"] is False, "the pasted text must never be echoed"
    # refused, never truncated: the state held nothing of the paste, and the
    # DOM reverted to the last accepted text
    assert o["stateComposer"] == "a fair question"
    assert o["domReverted"] == "a fair question"


def test_an_over_bound_subject_paste_names_its_own_bound(focus_throw_results):
    o = focus_throw_results["overBoundSubject"]
    assert str(512) in o["noteText"], "the note names the subject bound"
    assert o["error"] == "subject_over_bound"
    assert o["echoed"] is False
    assert o["stateSubject"] == ""
    assert o["domReverted"] == ""


def test_in_bound_edits_follow_the_existing_last_failure_lifecycle(
        focus_throw_results):
    """PIN EVOLUTION, P3-4 (wave re-review P3 tail): the lifecycle this test
    pins CHANGED, deliberately. MESSAGE_OVER_BOUND / SUBJECT_OVER_BOUND are
    PRESENT-TENSE claims ("this message exceeds the ... bound") that go false
    the moment the text is shortened -- and in the editor-only posture, where
    no turn ever settles, nothing else could clear them: the note was
    permanent. The old rule this test pinned ("an input event neither clears
    nor replaces the standing failure note") therefore left the rail
    asserting a falsehood forever.

    The new rule, exactly as narrow as the falsehood: a successful in-bound
    edit clears ITS OWN field's over-bound note (composer clears
    message_over_bound, subject clears subject_over_bound) and NOTHING else
    -- the other field's note stands, and every non-bound failure class
    (transport_refused here) keeps the existing settlement-only lifecycle."""
    clean = focus_throw_results["inBoundEdit"]
    assert clean["composer"] == "a fair question"
    assert clean["failure"] is None
    # a composer edit does not clear the SUBJECT's standing note
    after = focus_throw_results["inBoundAfterRefusal"]
    assert after["composer"] == "a shorter question"
    assert after["error"] == "subject_over_bound"
    # the subject's own in-bound edit clears its own note
    subject_clear = focus_throw_results["inBoundSubjectClears"]
    assert subject_clear["subject"] == "a subject that fits"
    assert subject_clear["error"] is None
    assert subject_clear["noteHidden"] is True
    # the composer's own bound behaves identically
    composer_clear = focus_throw_results["inBoundComposerClears"]
    assert composer_clear["messageFailureBack"] == "message_over_bound"
    assert composer_clear["error"] is None
    assert composer_clear["noteHidden"] is True
    # and a non-bound failure is untouched by typing
    assert focus_throw_results["throwingTurn"]["failureAfterTyping"] == \
        "transport_refused"


def test_typing_during_a_slow_apply_survives_and_the_proposal_still_lands(
        focus_throw_results):
    """W-3 (wave re-review): `adopt(await proposalActions.apply(state, ...))`
    derived the outcome from the CLICK-TIME snapshot, so everything adopted
    during the seam's await -- follow-up typing here -- was silently
    destroyed. The card actions now settle against the LIVE state, the same
    R1 defense the send path already had."""
    race = focus_throw_results["applyRace"]
    assert race["composerState"] == "typed during the apply await"
    assert race["composerDom"] == "typed during the apply await"
    assert race["proposalStatus"] == "applied"


def test_an_apply_spanning_a_turn_settlement_never_resurrects_the_flight(
        focus_throw_results):
    """W-3's wedge half: an Apply clicked during an in-flight turn, with the
    turn settling during the Apply's await, used to re-adopt the in-flight
    snapshot -- phase back to "in_flight" with no flight in the air, the
    settled answer gone from the transcript, Send disabled at "Sending..."
    forever (rail.abort() has no production caller; only a remount
    recovered). The live-state settle keeps the settled turn."""
    settled = focus_throw_results["applyAcrossSettlement"]
    assert settled["phase"] == "idle"
    assert settled["transcriptTurns"] == 4, \
        "the settled turn's pair must survive the overlapping Apply"
    assert settled["sendLabel"] != "Sending…"


def test_a_turn_settling_after_the_buffer_moved_renders_its_proposal_stale(
        focus_throw_results):
    """P3-3 (wave re-review P3 tail): proposals adopted from an in-flight
    turn rendered `current` unconditionally even when a document
    switch/discard landed during the flight -- the identity event that would
    have re-scored them fired BEFORE the proposals existed, so the card
    offered an enabled Apply against text the buffer no longer held (the
    swap-time gate would refuse it, but the card was lying until then). The
    success settle path now re-scores the just-adopted set against the LIVE
    editor identities."""
    probe = focus_throw_results["settleTimeCurrency"]
    assert probe["status"] == "stale", (
        "a proposal grounded on the pre-move identity rendered current")
    assert probe["applyDisabled"] is True


def test_send_focus_follows_intent_not_the_captured_node(focus_throw_results):
    """P3-7 (wave re-review P3 tail): after a successful send the composer
    clears, canSend goes false, Send disables -- and restoreFocus(captured
    node) no-opped on the now-disabled control, landing a keyboard operator
    on <body> (the class F7-4 fixed for the cards). Focus is now restored by
    INTENT: a send that settled successfully focuses the composer (where the
    next message starts); a failed send focuses the re-enabled Send control
    if that is where focus was, else the composer (where the preserved
    message is edited for the retry)."""
    success = focus_throw_results["successSendFocus"]
    assert success["sendDisabled"] is True, (
        "precondition: the settled send really disabled the control")
    assert success["activeIsNull"] is False, "focus dropped to <body>"
    assert success["activeIsComposer"] is True
    failed = focus_throw_results["failedSendFocus"]
    assert failed["sendDisabled"] is False, (
        "precondition: the failed send re-enabled the control")
    assert failed["activeIsSend"] is True
    elsewhere = focus_throw_results["failedSendFocusElsewhere"]
    assert elsewhere["activeIsComposer"] is True


def test_a_landed_apply_clears_the_failure_its_refusal_left_behind(
        focus_throw_results):
    """W-11 (wave re-review): `markProposalApplied` never touched
    `lastFailure`, so after a refused-then-successful Apply the rail rendered
    TWO live regions asserting opposite facts about the same proposal — the
    applied announcement beside the still-visible "no longer matches the
    buffer" note. A landed apply now clears the local failure; a refusal
    still records it."""
    probe = focus_throw_results["applyClearsFailure"]
    assert probe["refusedVisible"] is True, "the refusal itself must stay visible"
    assert probe["proposalStatus"] == "applied"
    assert probe["afterError"] is None
    assert probe["noteHidden"] is True


def test_the_settlement_rescore_covers_every_live_buffer(focus_throw_results):
    """CODEX-4 (Codex review of PR #210), through the REAL mount.

    The success-time re-score enumerated `outline` and `document` — the two names
    Phase A had — so a PATH-KEYED document was scored against a hash the map did
    not hold, or not scored at all. Both scenarios here DISCRIMINATE: each one's
    answer differs before and after the fix.

    (d) The reserved slot is absent and the loaded buffer MOVED mid-flight. The
    old guard read `buffers.document`, found nothing, and skipped the re-score
    entirely — so the card stayed CURRENT with an enabled Apply against text the
    buffer no longer held. The swap-time guard would still have refused the
    click; this is about the card telling the truth before anyone clicks it."""
    moved = focus_throw_results["movedLoadedCurrency"]
    assert moved["hasReservedSlot"] is False
    assert moved["status"] == "stale"
    assert moved["applyDisabled"] is True


def test_the_settlement_rescore_leaves_an_unmoved_buffer_current(focus_throw_results):
    """(c), the other direction, so the fix cannot be "mark everything stale":
    the reserved slot is PRESENT and the loaded buffer did NOT move, and the
    proposal must come back CURRENT and applicable. Before the fix the two-key
    map scored it against `undefined` and the card read falsely stale — a human
    told to ask again in a new turn for no reason at all."""
    unmoved = focus_throw_results["unmovedLoadedCurrency"]
    assert unmoved["status"] == "current"
    assert unmoved["applyDisabled"] is False


# ---------------------------------------------------------------------------
# THE PROMOTED WORKING-SUBJECT DEFAULT (capability `ideation-dashboard`,
# requirement "Browser-local doxBench conversation": "The working subject SHALL
# default from the tile's title or summary, remain editable, and affect
# authoring focus only").
#
# It was ratified and promoted but never built: `createChatState` seeded an
# empty subject and nothing ever filled it, which is what Brett's 2026-08-21
# annotation measured from the running surface ("what is the box used for? i do
# not know how to use it") and what add-doxbench-editing-phase-b's Amendment 2
# recorded as a realization gap needing its own slice. This is that slice's
# evidence: the seed lands, a stored human value still wins over it, the field
# is still a field, and the 512-byte bound is still refused-never-truncated on
# both the seeded and the typed side.
# ---------------------------------------------------------------------------


def test_the_mounted_rail_opens_with_the_tiles_title_in_the_subject_box(
        focus_throw_results):
    """The realization, where a human meets it: the box the annotation asked
    about opens carrying the tile's own title instead of empty."""
    s = focus_throw_results["seededSubject"]
    assert s["seededValue"] == "keyword lens and edge degree"
    assert s["seededState"] == "keyword lens and edge degree"
    # the affordances the annotation round added are untouched by the seed
    assert s["placeholder"].startswith("working subject — e.g.")
    assert s["ariaLabel"] == "working subject"


def test_the_seeded_subject_is_a_default_and_not_a_fixed_label(
        focus_throw_results):
    """"remain editable" is half the requirement's sentence: typing replaces the
    seed, and emptying the box empties it — a default the human cannot overrule
    would be a label wearing a text box."""
    s = focus_throw_results["seededSubject"]
    assert s["typed"] == "why does the funnel disagree with the wheel?"
    assert s["cleared"] == ""
    assert s["clearedValue"] == ""


def test_a_rail_mounted_with_no_tile_title_still_opens_empty(
        focus_throw_results):
    """The placeholder path stays reachable: a mount handed no default (an older
    caller, or a composition with no tile record to offer) opens empty, and the
    placeholder the 2026-08-21 annotation added is what shows there."""
    u = focus_throw_results["unseededSubject"]
    assert u["value"] == ""
    assert u["state"] == ""
    assert u["placeholder"].startswith("working subject — e.g.")


def test_a_tile_title_past_the_bound_seeds_nothing_rather_than_a_prefix(
        focus_throw_results):
    """The over-long SOURCE, decided against truncation. The 512-byte bound is
    refused-never-truncated on both sides, so a seeded prefix would be text the
    human never typed AND text this module's own rule forbids inventing; a
    seeded value the field would itself refuse is simply incoherent. Empty is
    always sendable, so seeding nothing can never leave Send refusing a value
    nobody entered — and no over-bound failure note is invented for a value the
    human did not type."""
    o = focus_throw_results["overLongSeed"]
    assert o["value"] == ""
    assert o["state"] == ""
    assert o["failure"] is None


def test_the_no_document_refusal_reaches_the_rail_as_the_routes_own_sentence(
        focus_throw_results):
    """Amendment 2 follow-up 1, the client half: what the human READS when a set
    unloaded down to the outline is sent.

    The route now names the cause and the remedy instead of saying only that the
    request is malformed, and this pins that the improvement actually arrives.
    The rail must render the ROUTE's sentence verbatim -- the expected string is
    `serve.py`'s own constant, injected into the probe, so a message changed on
    one side and not the other fails here rather than shipping two surfaces that
    describe one state differently.

    NOT a redundant restatement of the composer-preservation tests above. Those
    hold for any failure whatsoever; this one holds for THIS failure, and its
    real target is the substitution risk: `recordCatalogFailure` deliberately
    replaces server text with a fixed two-value marker on the catalog channel,
    so a later tidy-up that "made the turn channel consistent" with it would
    silently discard the sentence this change exists to deliver."""
    r = focus_throw_results["noDocumentRefusal"]
    assert r["error"] == "invalid_turn_request", (
        "the CODE is deliberately unchanged: the class really is a malformed "
        "request, and only the sentence got more useful")
    assert r["noteHidden"] is False, "a refusal the human cannot see is no fix"
    assert r["noteText"] == serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT
    # The sentence has to carry BOTH halves to be worth the change: the cause
    # (what is wrong) and the remedy (what to do). Named separately so a future
    # edit that keeps the string non-empty but drops one half still fails.
    assert "no document" in r["noteText"], "the cause is named"
    assert "load" in r["noteText"], "the remedy is named"
    # FR-016 for this refusal specifically: the question survives the trip, so
    # loading a document and pressing Send again is all the human has to do.
    assert r["composer"] == "which open question should we close next?"
    assert r["composerState"] == r["composer"]
    assert r["phase"] == "idle", "the rail is ready to send the fixed turn"


# --- the pure model's own half: seeding, precedence, and the bounds ---------

_SUBJECT_DEFAULT_HARNESS = """
import { createChatState, editSubject, rekeyChatState, chatSnapshot,
         restoreChatState, MAX_WORKING_SUBJECT_BYTES }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "r", ref: "main", tile_kind: "staged", tile_id: "t" };
const SESSION_KEY = { ...KEY, ref: "swb/session/t" };
const OTHER_KEY = { ...KEY, tile_id: "other-topic" };
const TITLE = "ideation governance";
const byteLen = (text) => Buffer.byteLength(text, "utf8");

// ---- the seed itself ----
out.seeded = createChatState(KEY, TITLE).workingSubject;
out.unseeded = createChatState(KEY).workingSubject;
out.frozen = Object.isFrozen(createChatState(KEY, TITLE));
// a title EXACTLY at the bound seeds whole -- the refusal is > 512, not >= 512
const AT_BOUND = "b".repeat(MAX_WORKING_SUBJECT_BYTES);
out.atBound = { bytes: byteLen(createChatState(KEY, AT_BOUND).workingSubject),
                whole: createChatState(KEY, AT_BOUND).workingSubject === AT_BOUND };
// ---- the over-long source: nothing, never a prefix ----
const OVER = "o".repeat(MAX_WORKING_SUBJECT_BYTES + 1);
out.overLong = { seeded: createChatState(KEY, OVER).workingSubject,
                 isPrefixOfSource: OVER.startsWith(
                   createChatState(KEY, OVER).workingSubject)
                   && createChatState(KEY, OVER).workingSubject.length > 0 };
// BYTES, never code points: 171 three-byte characters are 513 bytes and 171
// code points, so a length-based bound would seed this one and the byte rule
// refuses it -- the same discrimination the composer's own bound test uses.
const WIDE = "\\u20ac".repeat(Math.ceil(MAX_WORKING_SUBJECT_BYTES / 3) + 1);
out.wideSource = { bytes: byteLen(WIDE), codePoints: WIDE.length,
                   seeded: createChatState(KEY, WIDE).workingSubject };
// a non-string source (an absent title, a tile record that lost it) seeds
// nothing rather than the string "undefined"
out.nonStringSources = [undefined, null, 42, {}].map(
  (bad) => createChatState(KEY, bad).workingSubject);

// ---- editability, and the human's own bound ----
const seeded = createChatState(KEY, TITLE);
out.retyped = editSubject(seeded, "a different focus").workingSubject;
out.emptied = editSubject(seeded, "").workingSubject;
// the 512 refusal still holds for a HUMAN edit of a seeded box: the identical
// state object comes back (which is how the view knows to say so)
const refused = editSubject(seeded, OVER);
out.humanOverBoundRefused = { identical: refused === seeded,
                              held: refused.workingSubject };

// ---- a STORED value wins over the default ----
const typed = editSubject(createChatState(KEY, TITLE), "the human's own focus");
out.storedWins = restoreChatState(createChatState(KEY, TITLE),
  chatSnapshot(typed), {}).workingSubject;
// ...INCLUDING a deliberately emptied one: the default must not resurrect the
// title over a box the human emptied on purpose
const emptied = editSubject(createChatState(KEY, TITLE), "");
out.clearedStoredWins = { stored: chatSnapshot(emptied).workingSubject,
                          restored: restoreChatState(createChatState(KEY, TITLE),
                            chatSnapshot(emptied), {}).workingSubject };
// a snapshot of an UNRECOGNIZED shape is refused fail-closed, which leaves the
// seeded state exactly as it was -- the seed is not collateral of the refusal
out.foreignSnapshotKeepsSeed = restoreChatState(createChatState(KEY, TITLE),
  { kind: "nope" }, {}).workingSubject;

// ---- a fresh conversation on a new key is seeded like a mount ----
out.rekeySeeds = rekeyChatState(typed, SESSION_KEY, TITLE).workingSubject;
out.rekeyDropsTheTypedValue =
  rekeyChatState(typed, SESSION_KEY, TITLE).workingSubject !== typed.workingSubject;
out.rekeyOtherTile = rekeyChatState(typed, OTHER_KEY, "another tile").workingSubject;
out.sameKeyUntouched = rekeyChatState(typed, KEY, TITLE) === typed;
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def subject_default_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the working-subject default probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-subject-default")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "subject-default-harness.mjs"
    harness.write_text(_SUBJECT_DEFAULT_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_fresh_chat_state_defaults_its_subject_from_the_tile_title(
        subject_default_results):
    """The promoted requirement's first clause, in the module that owns what a
    fresh conversation holds. `createChatState` seeded `workingSubject: ""` and
    nothing downstream ever filled it, so the box a human opened was always
    empty — the realization gap Amendment 2 recorded."""
    assert subject_default_results["seeded"] == "ideation governance"
    assert subject_default_results["frozen"] is True
    # a caller with no title to offer still gets the pre-existing empty state
    assert subject_default_results["unseeded"] == ""
    assert subject_default_results["nonStringSources"] == ["", "", "", ""]


def test_a_title_exactly_at_the_bound_seeds_whole(subject_default_results):
    """The refusal is OVER the bound, not at it — a 512-byte title is a legal
    subject and seeds verbatim, which is what keeps the over-long case below a
    real discrimination rather than an off-by-one."""
    a = subject_default_results["atBound"]
    assert a["bytes"] == 512
    assert a["whole"] is True


def test_a_title_past_the_bound_seeds_nothing_never_a_bounded_prefix(
        subject_default_results):
    """The over-long SOURCE. `editSubject` refuses an over-bound value and
    truncates nothing ("no silent truncation is permitted"), and the seed goes
    through that same rule rather than around it: a clipped title is text the
    human never typed, and a default the field itself would refuse is
    incoherent. Empty is always a sendable subject, so nothing seeded can make
    Send refuse a value nobody entered."""
    o = subject_default_results["overLong"]
    assert o["seeded"] == ""
    assert o["isPrefixOfSource"] is False, (
        "the over-long title was truncated into the box instead of refused")


def test_the_seed_bound_measures_utf8_bytes_and_not_code_points(
        subject_default_results):
    """The same byte discrimination the composer's bound carries: 171 three-byte
    characters are 513 BYTES and 171 code points, so a length-based check would
    seed a subject the server's own `validate_working_subject` then refuses."""
    w = subject_default_results["wideSource"]
    assert w["bytes"] > 512 and w["codePoints"] < 512, "precondition"
    assert w["seeded"] == ""


def test_the_seeded_subject_remains_editable_and_still_refuses_over_bound_edits(
        subject_default_results):
    """"remain editable", plus the half a default could quietly break: the
    512-byte refusal is unchanged for a human edit of a SEEDED box, and it
    still refuses by returning the identical state object, which is the one
    signal the view reads to render the refusal note."""
    assert subject_default_results["retyped"] == "a different focus"
    assert subject_default_results["emptied"] == ""
    h = subject_default_results["humanOverBoundRefused"]
    assert h["identical"] is True
    assert h["held"] == "ideation governance", "the refused edit kept the seed"


def test_a_stored_working_subject_wins_over_the_tile_default(
        subject_default_results):
    """The precedence rule. The rail mounts seeded and the restore lands after
    it, so the persisted subject must overrule the default — otherwise
    reopening a tile would overwrite the focus a human wrote with the tile's
    title."""
    assert subject_default_results["storedWins"] == "the human's own focus"


def test_an_emptied_stored_subject_is_not_re_seeded_from_the_title(
        subject_default_results):
    """THE SUBTLE HALF, decided and documented in the module. The snapshot
    spells the subject as a plain string with no absent/null marker, so the
    stored form cannot distinguish "the human emptied this box" from "nothing
    was ever put in it" by the field alone. The stored value wins either way:
    of the two readings, putting the title back over a box someone emptied on
    purpose overrules a person, while leaving an unfilled box empty costs one
    keystroke — and with the seed in place, an empty stored subject can only
    come from an emptying or from a tile whose title seeds nothing anyway."""
    c = subject_default_results["clearedStoredWins"]
    assert c["stored"] == "", "precondition: the emptied subject persisted empty"
    assert c["restored"] == ""


def test_a_refused_foreign_snapshot_leaves_the_seeded_subject_standing(
        subject_default_results):
    """The fail-closed door and the seed agree: an unrecognized blob returns the
    state untouched, so the tile default survives a snapshot that could not be
    read (rather than the refusal costing the human their default too)."""
    assert subject_default_results["foreignSnapshotKeepsSeed"] == "ideation governance"


def test_a_rekeyed_conversation_is_seeded_like_a_fresh_mount(
        subject_default_results):
    """FR-011 isolation gives a moved scope key a FRESH conversation, and a
    fresh conversation is seeded exactly like a mount — so a Save moving this
    tile onto its session ref comes back with the tile's subject rather than
    the empty box the un-threaded default would have left."""
    r = subject_default_results
    assert r["rekeySeeds"] == "ideation governance"
    assert r["rekeyDropsTheTypedValue"] is True
    assert r["rekeyOtherTile"] == "another tile"
    # …and an unchanged key still returns the identical state object
    assert r["sameKeyUntouched"] is True

# ---------------------------------------------------------------------------
# THE MENU OFFERS A ROUTING RULE (contract-v1.38, add-doxbench-editing-phase-b
# task 11.7) — AND THE VIEW IS UNCHANGED
#
# The ratified scenario's first THEN is that a routing entry "MUST declare
# itself a routing rule and carry the handling badge of every model it may route
# to", and the sibling scenario's is that the selector "MUST show exactly the
# available catalog entries and their data-handling badges". The release
# satisfies both WITHOUT a view change, and this is the probe that says so
# rather than an argument in prose: the option text a routing entry renders
# already contains every routed model's badge, because the released contract
# REQUIRES the rule's own `data_handling` to carry them (the delegated
# validator's covering rule) and this view already renders that string.
#
# So the JS below is the SHIPPED renderer, not a modified one. If a future
# release moved the badges off `data_handling` into a per-target list, this test
# would fail and a view change would then be owed.
# ---------------------------------------------------------------------------

_ROUTING_MENU_HARNESS = """
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
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() {}
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
}
const doc = { createElement: (tag) => new Node(tag), activeElement: null };
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));

import { mountDoxBenchChatRail, sendDisclosure } from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };

// The PACKAGED contract-v1.38 positive, verbatim in the parts that matter:
// the rule's badge carries both routed badges, which is what the covering rule
// requires of any conformant catalog.
const ON_TENANT = "Processed in the approved tenant boundary; no retention.";
const HOSTED = "Zero retention; content leaves the tenant boundary for inference only.";
const RULE_BADGE = "Routes by role. / " + ON_TENANT + " / " + HOSTED;
const CATALOG = { schema_version: 1, kind: "workbench-model-catalog", models: [
  { model_id: "auto", label: "Automatic (routes by role)",
    provider_class: "routing-rule", available: true,
    input_limit_bytes: 2048, output_limit_bytes: 8192,
    data_handling: RULE_BADGE, routing_rule: true,
    routes_to: ["routed-on-tenant-1", "routed-hosted-zr-1"],
    resolved_model_id: "routed-on-tenant-1" },
  { model_id: "routed-on-tenant-1", label: "Approved authoring model (routable)",
    provider_class: "on-tenant", available: true, input_limit_bytes: 800000,
    output_limit_bytes: 900000, data_handling: ON_TENANT },
  { model_id: "routed-hosted-zr-1", label: "Hosted zero-retention model (routable)",
    provider_class: "hosted-zero-retention", available: true,
    input_limit_bytes: 2048, output_limit_bytes: 8192, data_handling: HOSTED },
]};
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "# " + kind, dirty: false });
const editorState = () => ({ active_buffer: "document", buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md") } });

const host = new Node("div"); host.ownerDocument = doc;
const rail = mountDoxBenchChatRail(host, {
  scopeKey: KEY,
  transports: { catalog: async () => CATALOG, chatTurn: async () => null },
  editorState });
await rail.ready;
const selector = byClass(host, "doxchat-model")[0];
out.options = selector.children.map((o) => ({ value: o.value,
                                              text: o.textContent }));
out.selectorDisabled = selector.disabled === true;

// The send-moment disclosure for the RULE, through the shipped pure function.
const chosen = selectModel(adoptCatalog(createChatState(KEY), CATALOG), "auto");
out.disclosure = sendDisclosure(chosen);
out.badges = { onTenant: ON_TENANT, hosted: HOSTED, rule: RULE_BADGE };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def routing_menu_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the routing-rule menu probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-routing-menu")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "routing-menu-harness.mjs"
    harness.write_text(_ROUTING_MENU_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_menu_shows_the_routing_rule_carrying_every_routed_badge(
        routing_menu_results):
    """The scenario, claimed ON THE MENU. The `auto` option is offered beside
    the models it may route to, and its own visible text carries BOTH of their
    handling badges — so a human choosing `auto` reads the posture of everything
    it might reach, which is the whole point of the requirement's "because"
    clause."""
    options = routing_menu_results["options"]
    badges = routing_menu_results["badges"]
    assert [o["value"] for o in options] == [
        "", "auto", "routed-on-tenant-1", "routed-hosted-zr-1"]
    auto = next(o for o in options if o["value"] == "auto")
    assert badges["onTenant"] in auto["text"]
    assert badges["hosted"] in auto["text"]
    assert "Automatic (routes by role)" in auto["text"]
    assert routing_menu_results["selectorDisabled"] is False


def test_the_send_disclosure_for_a_routing_rule_is_the_union_badge(
        routing_menu_results):
    """The send-moment disclosure needs no change either, for the same reason:
    it names the SELECTED entry's own `data_handling`, and for a rule that
    string is the union."""
    assert routing_menu_results["disclosure"] == (
        routing_menu_results["badges"]["rule"])
    assert routing_menu_results["badges"]["onTenant"] in (
        routing_menu_results["disclosure"])
    assert routing_menu_results["badges"]["hosted"] in (
        routing_menu_results["disclosure"])


# ---------------------------------------------------------------------------
# THE REDUCED POSTURE IS VISIBLE TO THE HUMAN (contract-v1.39,
# add-doxbench-editing-phase-b task 10.7)
#
# This is the half of task 10.7 that was GATED, and the reason the task stayed
# open after its packet half landed: the ratified sentence ends "with the
# reduced posture STATED", the packet stated it, and no human could read it.
# The release put the posture on the record; this probe is what makes "and on
# the surface" evidence instead of an argument.
#
# It drives the SHIPPED `doxbench-chat.js` bytes through a real mount (P1-7 —
# a probe executes shipped bytes, never a paraphrase), sends turns through the
# real dispatcher, and reads the rendered note back off the DOM stub.
# ---------------------------------------------------------------------------

_POSTURE_HARNESS = """
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.hidden = false;
    this.disabled = false; this.value = ''; this.writes = [];
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  // S1's INSTRUMENT. The defect this probe exists to catch is an ORDER — a text
  // mutation performed while the node is still `hidden`, i.e. while it is out
  // of the accessibility tree and no live region can observe it. An assertion
  // read AFTER render() cannot see that: both orders end with the same
  // attributes. So the stub records `hidden` AT THE MOMENT the write happens.
  set textContent(value) {
    this.writes.push({ text: String(value), hiddenAtWrite: this.hidden });
    this.children = []; this._text = String(value);
  }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
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

import { mountDoxBenchChatRail, reducedContextNote, REDUCED_CONTEXT_LEAD }
  from "./doxbench-chat.mjs";
import { createChatState, settleTurnSuccess, beginTurn,
         adoptThreadTranscript, chatSnapshot, restoreChatState }
  from "./doxbench-chat-model.mjs";

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
const editorState = () => ({ active_buffer: "document", buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md") } });

// The reason VERBATIM from `doxbench_packet.REDUCED_NO_KNOWLEDGE_SERVICE`, so
// what this probe renders is what a real degraded turn actually carries.
const REASON = "the staged-set knowledge service is unavailable, so this packet"
  + " carries the selected thread and the loaded buffers only, with NO corpus"
  + " evidence; no unbounded context was substituted and no rail was bypassed"
  + " to reach a provider";
out.reason = REASON;
out.lead = REDUCED_CONTEXT_LEAD;

const recordWith = (contextPacket) => {
  const record = { schema_version: 1,
    kind: "workbench-chat-turn-v2-success",
    client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
    selected_model: { requested_model_id: "model-a", routing_rule: false,
                      data_handling: "on-tenant" },
    bound_buffer: "outline",
    observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
    assistant_prose: "answer", proposals: [] };
  if (contextPacket !== undefined) record.context_packet = contextPacket;
  return record;
};

// One mounted rail per case, each sending ONE real turn through the shipped
// dispatcher and reading the rendered note back.
async function railCase(contextPacket) {
  const host = new Node("div"); host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => ({ ok: true, status: 200,
                               payload: recordWith(contextPacket) }) },
    editorState });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "what does the note say?"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const note = byClass(host, "doxchat-context")[0];
  // S1: EVERY non-empty write, and whether the node was hidden when it
  // happened. A write performed while hidden is a write no live region saw.
  //
  // READ ALL OF THEM, NOT THE LAST ONE — measured, and this is the trap the
  // reviewer named. Under the defect order a reduced turn produces TWO
  // non-empty writes: the render that settles the turn writes the text while
  // the node is still hidden (the announcement is lost there), and a LATER
  // re-render writes the same text again with the node already visible. Reading
  // `writes[writes.length - 1]` sees only the benign second one and reports
  // clean — which is exactly what it did, and the revert-test caught it.
  const written = note ? note.writes.filter((wr) => wr.text !== "") : [];
  return {
    // true iff SOME text was written into the note while it was hidden
    anyWriteWhileHidden: written.some((wr) => wr.hiddenAtWrite === true),
    firstWriteHidden: written.length ? written[0].hiddenAtWrite : null,
    nonEmptyWrites: written.length,
    exists: Boolean(note),
    hidden: note ? note.hidden : null,
    text: note ? note.textContent : null,
    live: note ? note.getAttribute("aria-live") : null,
    // the answer still arrived: a degraded turn is a SUCCESSFUL turn
    transcript: rail.state().transcript.length,
    statePosture: rail.state().contextPacket
      ? rail.state().contextPacket.posture : null,
  };
}

// S4: a reduced answer, then a FAILED follow-up. The reduced answer is STILL
// the transcript's last assistant turn, so its disclosure must still be there.
async function reducedThenFailure() {
  const host = new Node("div"); host.ownerDocument = doc;
  let turn = 0;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => {
        turn += 1;
        return turn === 1
          ? { ok: true, status: 200,
              payload: recordWith({ posture: "reduced", reduced_reason: REASON }) }
          : { ok: false, status: 502,
              payload: { schema_version: 1,
                         kind: "workbench-chat-turn-v2-failure",
                         client_turn_id: "t", error: "model_failed",
                         message: "The model could not answer this turn." } };
      } },
    editorState });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  const note = byClass(host, "doxchat-context")[0];
  const send = byClass(host, "doxchat-send")[0];

  composer.value = "first question"; await fire(composer, "input");
  await fire(send, "click");
  const afterReduced = { hidden: note.hidden, text: note.textContent };

  composer.value = "second question"; await fire(composer, "input");
  await fire(send, "click");
  const afterFailure = {
    hidden: note.hidden, text: note.textContent,
    transcript: rail.state().transcript.length,
    lastAssistant: rail.state().transcript[
      rail.state().transcript.length - 1].content,
    failureShown: !byClass(host, "doxchat-failure")[0].hidden,
  };
  return { afterReduced, afterFailure };
}

// …and the inverse: a reduced answer REPLACED by a full one clears the note,
// because the answer the note described is no longer the last one.
async function reducedThenFullSuccess() {
  const host = new Node("div"); host.ownerDocument = doc;
  let turn = 0;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => {
        turn += 1;
        return { ok: true, status: 200, payload: recordWith(
          turn === 1 ? { posture: "reduced", reduced_reason: REASON }
                     : { posture: "full" }) };
      } },
    editorState });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  const note = byClass(host, "doxchat-context")[0];
  const send = byClass(host, "doxchat-send")[0];
  composer.value = "first question"; await fire(composer, "input");
  await fire(send, "click");
  const afterReduced = { hidden: note.hidden, text: note.textContent };
  composer.value = "second question"; await fire(composer, "input");
  await fire(send, "click");
  return { afterReduced,
           afterFull: { hidden: note.hidden, text: note.textContent } };
}

out.s4Failure = await reducedThenFailure();
out.s4FullSuccess = await reducedThenFullSuccess();
out.reduced = await railCase({ posture: "reduced", reduced_reason: REASON });
out.full = await railCase({ posture: "full" });
out.omitted = await railCase(undefined);
// A record that contradicts itself. The released schema refuses both of these,
// so they cannot come from a conformant producer -- the surface still has to
// decide, and it decides SILENCE rather than a half-statement.
out.reducedNoReason = await railCase({ posture: "reduced" });
out.fullWithReason = await railCase({ posture: "full", reduced_reason: REASON });

// The note describes the LAST ANSWER, so a new flight clears it.
{
  const settled = settleTurnSuccess(
    beginTurn(createChatState(KEY)),
    recordWith({ posture: "reduced", reduced_reason: REASON }));
  out.afterSettle = reducedContextNote(settled);
  out.duringNextFlight = reducedContextNote(beginTurn(settled));
  // …and switching documents replaces the transcript with the SERVER's thread,
  // which carries no posture of its own.
  out.afterThreadSwitch = reducedContextNote(
    adoptThreadTranscript(settled, [{ human: "q", assistant: "a" }]));
}

// NEW-1/NEW-2: the SNAPSHOT round trip, which is the fourth answer-replacing
// path and the one that survives a tile being closed.
{
  const reduced = settleTurnSuccess(
    beginTurn({ ...createChatState(KEY), composer: "q" }),
    recordWith({ posture: "reduced", reduced_reason: REASON }));
  const full = settleTurnSuccess(
    beginTurn({ ...createChatState(KEY), composer: "z" }),
    recordWith({ posture: "full" }));

  // (a) a snapshot of a reduced conversation CARRIES the posture …
  const blob = chatSnapshot(reduced);
  out.snapshotCarries = Boolean(blob.context_packet)
    && blob.context_packet.posture === "reduced"
    && blob.context_packet.reduced_reason === REASON;
  // … INCLUDING an explicitly full one, which is not a quirk: this release's
  // own doctrine is that absent and `full` are DIFFERENT facts, so a snapshot
  // that dropped `full` would restore "unknown" over a posture somebody
  // checked — re-introducing the inference-by-absence the release forbids.
  // Read defensively: if the key stops being written this must REPORT that,
  // not crash the harness and make the failure look like a broken probe.
  out.snapshotCarriesFull =
    (chatSnapshot(full).context_packet || {}).posture === "full";
  // The key is omitted only when there is NO posture to state: a conversation
  // with no answer yet, or one whose answer came from a producer older than
  // contract-v1.39. That is the case whose blob is unchanged from before.
  out.snapshotOmitsWhenUnknown =
    !("context_packet" in chatSnapshot(createChatState(KEY)));

  // (b) restoring it onto a FRESH rail brings the disclosure back with the
  //     answer it describes.
  out.restoredReduced = reducedContextNote(
    restoreChatState(createChatState(KEY), blob, {})) !== null;

  // (c) NEW-1: restoring a DIFFERENT conversation over a reduced one must not
  //     leave the old note captioning the new answer.
  const otherBlob = chatSnapshot(full);
  const crossed = restoreChatState(reduced, otherBlob, {});
  out.restoreClearsStale = reducedContextNote(crossed) === null;
  out.crossedLastAssistant =
    crossed.transcript[crossed.transcript.length - 1].content;

  // (d) an OLD blob — one written before contract-v1.39 — restores to silence
  //     rather than being refused, which is what makes the field additive.
  const legacy = { ...blob };
  delete legacy.context_packet;
  out.legacyBlobRestores = {
    note: reducedContextNote(restoreChatState(createChatState(KEY), legacy, {})),
    transcript: restoreChatState(createChatState(KEY), legacy, {})
      .transcript.length,
  };

  // (e) a blob that CONTRADICTS itself fails closed by the same rule a wire
  //     record does. ASSERTED ON THE ADOPTED STATE, not on the rendered note:
  //     `reducedContextNote` carries its own second guard on the same rule, so
  //     a note-level assertion passes even when the adopter trusts the blob —
  //     measured, by a revert-test (R39) that came back GREEN reading the note.
  //     The state is where the adopter's verdict actually lands.
  const contradictions = [
    { posture: "reduced" },                                   // no reason
    { posture: "reduced", reduced_reason: "" },               // empty reason
    { posture: "full", reduced_reason: REASON },              // full WITH one
    { posture: "degraded", reduced_reason: REASON },          // unknown posture
    "reduced",                                                // not an object
  ];
  out.contradictoryBlobs = contradictions.map((cp) =>
    restoreChatState(createChatState(KEY), { ...blob, context_packet: cp }, {})
      .contextPacket);
  // …and the honest blob still adopts, so the guard is not simply refusing
  // everything.
  out.goodBlobAdopts = restoreChatState(
    createChatState(KEY), blob, {}).contextPacket;
}

// NEW-3: typing in the composer must not re-announce the same sentence.
{
  const host = new Node("div"); host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => ({ ok: true, status: 200,
        payload: recordWith({ posture: "reduced", reduced_reason: REASON }) }) },
    editorState });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "ask"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const note = byClass(host, "doxchat-context")[0];
  const afterTurn = note.writes.length;
  // seven keystrokes, the reviewer's own measurement
  for (const ch of "abcdefg") {
    composer.value += ch; await fire(composer, "input");
  }
  out.rewrites = {
    afterTurn,
    afterTyping: note.writes.length,
    stillShown: !note.hidden,
    text: note.textContent,
  };
}

process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def posture_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the context-posture probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-posture")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "posture-harness.mjs"
    harness.write_text(_POSTURE_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_reduced_turn_states_the_posture_and_its_reason_on_the_surface(
        posture_results):
    """THE RELEASE'S POINT, on the rendered surface. A turn that ran on the
    declared reduced packet renders a visible, live-announced note naming the
    reduction AND its reason — the reason verbatim, because "reduced context"
    with no why is the silent degradation with a label on it.

    The answer is still there: `transcript` is the human turn plus the
    assistant's, which is the ratified "MUST NOT ... make the editors
    unusable" half holding at the same time."""
    reduced = posture_results["reduced"]
    assert reduced["exists"] is True
    assert reduced["hidden"] is False
    assert reduced["text"] == posture_results["lead"] + posture_results["reason"]
    assert "reduced context" in reduced["text"]
    assert "no unbounded context was substituted" in reduced["text"]
    assert reduced["live"] == "polite"
    assert reduced["transcript"] == 2
    assert reduced["statePosture"] == "reduced"


def test_the_note_is_UN_HIDDEN_BEFORE_its_text_is_written(posture_results):
    """S1, and the reason the `aria-live` assertion above is not enough. A
    `hidden` node is out of the accessibility tree, so text written into one
    while it is still hidden is a mutation no live region observed — the
    "live-announced" claim would be false and the attribute would still read
    `polite`. This release shipped that order the wrong way round and its
    adversarial review caught it.

    ASSERTED OVER EVERY WRITE, not the last one. Under the defect order the
    settling render writes the text while the node is still hidden and a LATER
    re-render writes the identical text with it already visible; an assertion
    that reads only the final write sees the benign one and passes. That is not
    hypothetical — this test was written that way first, and the R27
    revert-test came back GREEN with the defect restored, which is how the
    weakness was found."""
    reduced = posture_results["reduced"]
    assert reduced["nonEmptyWrites"] >= 1
    assert reduced["firstWriteHidden"] is False
    assert reduced["anyWriteWhileHidden"] is False


def test_a_reduced_answer_keeps_its_disclosure_through_a_FAILED_follow_up(
        posture_results):
    """S4, reproduced and closed. The reviewer's sequence: a reduced answer,
    then a follow-up that FAILS. The reduced answer is still the transcript's
    last assistant turn — it is still on screen, and it still ran without
    corpus evidence — so stripping its disclosure is the lost-badge defect this
    release cited when it rejected per-turn badges, reappearing at rail level.

    The note now survives, because it is keyed to the ANSWER rather than to a
    flight starting. The failure note appears beside it: two true statements,
    about two different things."""
    r = posture_results["s4Failure"]
    assert r["afterReduced"]["hidden"] is False
    assert r["afterFailure"]["hidden"] is False, "the disclosure was stripped"
    assert r["afterFailure"]["text"] == r["afterReduced"]["text"]
    assert r["afterFailure"]["transcript"] == 2
    assert r["afterFailure"]["lastAssistant"] == "answer"
    assert r["afterFailure"]["failureShown"] is True


def test_a_full_answer_REPLACING_a_reduced_one_clears_the_note(posture_results):
    """The other half of S4's invariant, and what stops the fix from becoming a
    note that never goes away: when the answer the note described is replaced
    by a FULL one, the note goes with it."""
    r = posture_results["s4FullSuccess"]
    assert r["afterReduced"]["hidden"] is False
    assert r["afterFull"]["hidden"] is True
    assert r["afterFull"]["text"] == ""


def test_a_full_turn_shows_nothing_new(posture_results):
    """The other half of the treatment, and it is deliberate rather than
    unfinished: a standing "full context" badge is a line every operator learns
    to stop reading, which is exactly how the reduced one would stop being
    noticed. The note element still EXISTS (so nothing has to be created at the
    moment it is needed) and renders hidden and empty."""
    full = posture_results["full"]
    assert full["exists"] is True
    assert full["hidden"] is True
    assert full["text"] == ""
    assert full["statePosture"] == "full"
    assert full["transcript"] == 2


def test_a_record_with_no_posture_renders_no_phantom_badge(posture_results):
    """A producer older than contract-v1.39 states no posture, and the surface
    says nothing rather than inventing one. Absence is not `full` and it is not
    `reduced`; it is silence, and silence is what it renders."""
    omitted = posture_results["omitted"]
    assert omitted["hidden"] is True
    assert omitted["text"] == ""
    assert omitted["statePosture"] is None
    assert omitted["transcript"] == 2


@pytest.mark.parametrize("case", ["reducedNoReason", "fullWithReason"])
def test_a_self_contradicting_record_renders_nothing_rather_than_half_of_it(
        posture_results, case):
    """FAIL-CLOSED ON THE SURFACE TOO. The released schema refuses both of
    these, so neither can come from a conformant producer — but the adopter is
    the last thing between a record and a human, and the wrong move would be to
    keep whichever half looked renderable. A `reduced` with no readable reason
    would render the words "reduced context" over a reduction nobody can check,
    which is the failure this requirement is written against."""
    result = posture_results[case]
    assert result["hidden"] is True
    assert result["text"] == ""
    assert result["statePosture"] is None
    # …and the ANSWER is not withheld: a malformed posture is a defect in the
    # record's metadata, never a reason to drop the turn the human asked for.
    assert result["transcript"] == 2


def test_the_note_describes_the_last_answer_and_a_flight_does_not_move_it(
        posture_results):
    """THE INVARIANT, RESTATED AFTER S4 — and this test used to assert its
    opposite. It read "a new flight clears it", which is what produced the
    stripped-disclosure defect: a flight STARTING replaces no answer, so while
    the next question is in the air the answer on screen is still the reduced
    one and its disclosure is still true of it.

    What the note tracks is the transcript's last assistant answer. Every path
    that replaces that answer replaces the posture beside it, so nothing needs
    to clear it on the way out."""
    assert posture_results["afterSettle"] == (
        posture_results["lead"] + posture_results["reason"])
    assert posture_results["duringNextFlight"] == (
        posture_results["lead"] + posture_results["reason"])


def test_switching_documents_does_not_caption_the_new_thread_with_the_old_one(
        posture_results):
    """The same rule at the other exit. `adoptThreadTranscript` replaces the
    transcript with the SERVER'S record of the newly selected document, and that
    record carries no posture — so leaving the previous document's note up would
    caption one conversation with a fact about another, which is the exact defect
    class P2-9 found for the transcript itself."""
    assert posture_results["afterThreadSwitch"] is None


def test_the_snapshot_carries_the_posture_and_omits_it_when_there_is_none(
        posture_results):
    """NEW-2, taken as CLOSE rather than defer. Unlike the thread sidecar — a
    durable on-disk format whose parser has fixed arity, correctly left alone —
    the chat snapshot is a browser-local blob this release fully controls, so
    the disclosure can survive a tile being closed and reopened without a
    migration. A conversation with NO posture to state — no answer yet, or an
    answer from a producer older than contract-v1.39 — writes the blob it
    always did."""
    assert posture_results["snapshotCarries"] is True
    assert posture_results["restoredReduced"] is True
    # An explicitly FULL posture is persisted too, and that is the doctrine
    # rather than an oversight: absent and `full` are different facts
    # everywhere else in this release, so dropping `full` here would restore
    # "unknown" over a posture somebody checked.
    assert posture_results["snapshotCarriesFull"] is True
    # The key is absent only when there is no posture to state at all — which
    # is the case whose blob is unchanged from before contract-v1.39.
    assert posture_results["snapshotOmitsWhenUnknown"] is True


def test_restoring_a_snapshot_does_not_leave_a_STALE_note_on_a_new_answer(
        posture_results):
    """NEW-1: `restoreChatState` is the FOURTH answer-replacing path, and it
    used to leave `contextPacket` untouched while replacing the transcript
    wholesale. The reviewer reproduced a restored answer captioned by a note
    that never described it. Reachability was nil — the sole caller restores
    onto a freshly mounted rail — but three places claimed the enumeration of
    answer-replacing paths was complete at three, and it was four."""
    assert posture_results["restoreClearsStale"] is True
    assert posture_results["crossedLastAssistant"] == "answer"


def test_a_snapshot_written_before_this_release_still_restores(posture_results):
    """What makes the snapshot field ADDITIVE rather than a version bump: a
    blob with no `context_packet` restores its transcript unharmed and simply
    renders no note — exactly the behaviour before this release. Bumping
    `CHAT_SNAPSHOT_VERSION` would instead have discarded every stored blob on
    the first reopen, because `restoreChatState` fail-closes on an unrecognized
    version and keeps the fresh state."""
    legacy = posture_results["legacyBlobRestores"]
    assert legacy["note"] is None
    assert legacy["transcript"] == 2


def test_a_contradictory_stored_posture_fails_closed_like_a_wire_one(
        posture_results):
    """One validator, both readers. A hand-edited blob claiming `reduced` with
    no readable reason adopts to NOTHING, rather than captioning the restored
    transcript with a reduction nobody can check.

    ASSERTED ON THE ADOPTED STATE, not on the rendered note. `reducedContextNote`
    holds its own second guard on the same rule, so a note-level assertion is
    satisfied even when the adopter trusts the blob whole — which a revert-test
    proved by coming back GREEN (R39) with the validation removed. The state is
    where the adopter's verdict lands, so that is what this pins."""
    assert posture_results["contradictoryBlobs"] == [None, None, None, None, None]
    # …and the guard is discriminating, not merely refusing everything.
    assert posture_results["goodBlobAdopts"] == {
        "posture": "reduced",
        "reduced_reason": posture_results["reason"],
    }


def test_typing_does_not_RE_ANNOUNCE_the_same_disclosure(posture_results):
    """NEW-3. `render()` runs on every keystroke, and re-writing a live region
    with identical text re-announces it — the reviewer measured seven repeats
    of the same 227-character sentence while typing one follow-up question. The
    note is written only when its text actually changes, so the write count is
    unmoved by typing while the note stays visible and unchanged."""
    r = posture_results["rewrites"]
    assert r["afterTyping"] == r["afterTurn"], "the disclosure was re-announced"
    assert r["stillShown"] is True
    assert r["text"] == posture_results["lead"] + posture_results["reason"]
