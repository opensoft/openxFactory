"""T045 (US2): privacy sentinels for the doxBench chat client — secret,
endpoint, prompt, content, and unsaved-text leakage (FR-011, FR-020, FR-022).

Two layers, mirroring the mutation-boundary discipline:

* STATIC needles over the two chat modules' source: no transport primitive,
  no URL scheme, no credential-shaped literal, no innerHTML, and no storage
  primitive may appear — chat state is browser-session-scoped IN MEMORY and
  is never persisted (unsaved text must not outlive the session, FR-011).
* BEHAVIORAL dumps via the Node harness: a refused over-bound message never
  enters state; a settled failure retains only the two fixed released
  fields; no state dump after a turn carries buffer content or an endpoint.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")

_VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
CHAT_MODEL_JS = _VIEWS / "doxbench-chat-model.js"
CHAT_VIEW_JS = _VIEWS / "doxbench-chat.js"

# One list, both files: the chat client may neither open a transport of its
# own (injected seams only), nor persist, nor render markup, nor carry a
# credential-shaped or endpoint-shaped literal. `http`/`https` are banned
# outright — even comments must find another spelling, so a scanner needs
# no comment-parsing carve-out that a later edit could hide behind.
FORBIDDEN_SOURCE_NEEDLES = (
    "fetch(",
    "XMLHttpRequest",
    "WebSocket",
    "EventSource",
    "navigator.sendBeacon",
    "innerHTML",
    "outerHTML",
    "insertAdjacentHTML",
    "document.cookie",
    "localStorage",
    "sessionStorage",
    "indexedDB",
    "http://",
    "https://",
    "ws://",
    "wss://",
    "Authorization",
    "Bearer",
    "api_key",
    "apikey",
    "secret",
    "credential",
)


@pytest.mark.parametrize("module_path", [CHAT_MODEL_JS, CHAT_VIEW_JS],
                         ids=["chat-model", "chat-view"])
def test_chat_module_source_carries_no_transport_storage_or_secret_markers(module_path):
    source = module_path.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SOURCE_NEEDLES:
        assert needle.lower() not in source, needle


def test_the_chat_view_reaches_no_module_but_the_chat_model():
    """Import allowlist: the view may import ONLY the pure chat model (and
    nothing may import the transports directly — they arrive injected)."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    imports = [line for line in source.splitlines()
               if line.strip().startswith("import ") or ' from "' in line]
    froms = [line for line in imports if ' from "' in line]
    assert froms, "expected at least one static import"
    for line in froms:
        assert '"./doxbench-chat-model.js"' in line, line
    model_source = CHAT_MODEL_JS.read_text(encoding="utf-8")
    assert ' from "' not in model_source, "the chat model must stay import-free"


_PRIVACY_HARNESS = """
import { createChatState, adoptCatalog, selectModel, editComposer,
         beginTurn, settleTurnFailure, MAX_MESSAGE_BYTES }
  from "./doxbench-chat-model.mjs";
import { createTurnDispatcher } from "./doxbench-chat.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved authoring model",
                provider_class: "on-tenant", available: true,
                input_limit_bytes: 800000, output_limit_bytes: 900000,
                data_handling: "Processed in the approved tenant boundary" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
let s = selectModel(adoptCatalog(createChatState(KEY), ENVELOPE), "model-a");

// A REFUSED over-bound message must never enter any state dump.
const SECRET_OVERSIZE = "leak-sentinel-oversize-" + "x".repeat(MAX_MESSAGE_BYTES);
out.refusedInputAbsent = !JSON.stringify(editComposer(s, SECRET_OVERSIZE))
  .includes("leak-sentinel-oversize-");

// A settled failure retains ONLY the two fixed released fields — nothing
// from a wider (hostile) failure payload survives into state.
const hostile = { schema_version: 1, kind: "workbench-chat-turn-failure",
  client_turn_id: "t-1", error: "model_failed",
  message: "the model request failed",
  endpoint: "leak-sentinel-endpoint", api_material: "leak-sentinel-key" };
const failed = settleTurnFailure(beginTurn(editComposer(s, "ok?")), hostile);
const failedDump = JSON.stringify(failed);
out.failureFieldSet = Object.keys(failed.lastFailure).sort();
out.hostileFieldsAbsent = !failedDump.includes("leak-sentinel-endpoint")
  && !failedDump.includes("leak-sentinel-key");

// After a dispatched turn, the chat state must not retain buffer CONTENT
// (the request carried it to the server; state keeps only the transcript).
const buffer = (kind) => ({ kind, path: null, owned: true, base_ref: "main",
  base_revision: "r1", base_hash: "c".repeat(64),
  current_hash: "d".repeat(64),
  content: "leak-sentinel-unsaved-buffer-text", dirty: true });
// T104 F2: the released envelope names an active document, so this leak
// probe -- whose subject is what the STATE retains -- carries one.
const DOC_PATH = "docs/detail.md";
const editorState = { buffers: {
  outline: buffer("outline"),
  document: { ...buffer("document"), path: DOC_PATH } } };
const dispatcher = createTurnDispatcher({
  transports: { chatTurn: async () => ({ ok: false, status: 502, payload: {
    schema_version: 1, kind: "workbench-chat-turn-failure",
    client_turn_id: "turn-1", error: "model_failed",
    message: "the model request failed" } }) },
  turnIdFactory: (n) => "turn-" + n });
const result = await dispatcher.submit(editComposer(s, "ok?"), {
  scopeKey: KEY, activeDocumentPath: DOC_PATH, editorState });
out.bufferContentAbsent = !JSON.stringify(result.state)
  .includes("leak-sentinel-unsaved-buffer-text");
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def privacy_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench privacy probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-privacy")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    view_source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(view_source, encoding="utf-8")
    harness = tmp_path / "privacy-harness.mjs"
    harness.write_text(_PRIVACY_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_refused_over_bound_message_never_enters_state(privacy_results):
    assert privacy_results["refusedInputAbsent"] is True


def test_a_settled_failure_keeps_only_the_two_fixed_released_fields(privacy_results):
    assert privacy_results["failureFieldSet"] == ["error", "message"]
    assert privacy_results["hostileFieldsAbsent"] is True


def test_chat_state_never_retains_unsaved_buffer_content(privacy_results):
    assert privacy_results["bufferContentAbsent"] is True
