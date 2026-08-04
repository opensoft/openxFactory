"""T023 (010-doxbench-editor-chat), PARTIAL SLICE: the browser transport seams
`app.js` owns for the doxBench canvas.

T023's full text names source/hash foundations plus catalog, chat, and Save
transports. The source-LOADING seam is a read-only pass-through through the
SAME `/source` route the viewer already reads (D15), and the HASH-AUTHORITY
injection uses the shared `contentIdentity` from `doxbench-state.js`, never a
second digest implementation. Server-side catalog and chat routes plus the
catalog-only `WorkbenchModelPort` now exist. Their exact schema parity and
BROWSER consumers remain open under T005-T008, T050-T054; governed Save
remains open under T077-T080. This file proves what is built and pins the
deliberate absence of executable browser transports, so a future reader can
tell "not yet implemented" from "forgotten".

Six angles, mirroring test_renderer.py's and test_staging_workbench.py's own
house style (text/grep assertions for structure and absence, a Node harness
for behaviour, real HTTP for the server contract the seam assumes):

  (a) app.js defines a module-scope `createDoxBenchSourceLoader` factory that
      reaches the read-only /source base through the workbench's own CURRENT
      source base, with exactly one NEW `fetch(` call site (two total) and no
      second Markdown/hash implementation of its own.
  (b) app.js imports the shared `contentIdentity` hash from doxbench-state.js
      and injects it as the doxBench hash seam -- never a local SHA-256.
  (c) app.js contains no executable catalog/chat/Save transport or credential
      spelling, and comments the remaining tasks so the absence reads as
      deliberate.
  (d) staging-workbench.js accepts the new `doxbench` option, forwards its
      `loadSource`/`hash`/`storage` into `mountDoxBenchCanvas` verbatim
      (`storage` since R-1, 2026-08-02: the editor GATES persistence on that
      handle, so leaving it unforwarded meant no persistence at all -- the
      operator's reload lost unsaved buffers and a live probe found
      sessionStorage empty; the old "the fallback binds it anyway" theory was
      plausible and false), still issues no fetch of its own, and the three
      pinned
      option-destructure substrings from test_staging_workbench.py survive
      verbatim.
  (e) a Node behavioural harness drives the ACTUAL loader against an injected
      fake fetch: exact byte-for-byte content (CRLF, non-ASCII), the
      X-Snapshot-Ref -> `ref` surfacing, honest `null` on a non-ok response,
      an always-relative same-origin URL, and the source base read AT CALL
      TIME (a session re-key changes what the very next load requests).
  (f) a real ephemeral HTTP server proves the keyed
      `/source/<repository>@<ref>/<path>` route this seam assumes really
      returns the exact file bytes plus an `X-Snapshot-Ref` header.

`test_doxbench_view.py`'s own composition pin
(`test_staging_workbench_composes_the_doxbench_canvas_without_new_transport`)
was adjusted alongside this file (lead-adjudicated ownership extension) to
match: it now asserts the `mountDoxBenchCanvas(...)` call forwards exactly
the injected `loadSource`/`hash` seam and nothing else, while its own
transport-absence loop (`fetch(`, `XMLHttpRequest`, `doFetch`, `/actions/`)
is untouched -- that loop is the real guarantee this whole slice rests on.
"""

from __future__ import annotations

import http.client
import json
import re
import shutil
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, FakeGit

from ideation_dashboard import serve as serve_mod
from ideation_dashboard.generator import generate_snapshot

WEB = Path(__file__).resolve().parent.parent.parent / "scripts" / "ideation_dashboard" / "web"
APP_JS = WEB / "app.js"
STAGING_WORKBENCH_JS = WEB / "views" / "staging-workbench.js"
NODE = shutil.which("node")

# PIN EVOLUTION (T023 wire clause, 2026-07-30). This tuple names the task
# groups app.js must still COMMENT so a reader can tell deliberate absence from
# forgetfulness. Two entries are dropped because the absence they explained is
# gone, not because the pin was relaxed:
#   * "T005-T008" -- the schema gate is CLOSED. Both additive openxFactory
#     schemas are released and pinned at contract-v1.27
#     (`d09d5820de5b63b9528f6baea884a6dccde9b158`); a comment still citing them
#     as blocking would now be wrong.
#   * "T050/T051" -- both routes now exist, are enveloped, and are validated
#     against the released schemas, so they no longer block a browser transport.
# "T052-T054" STAYS: the chat UI (model, view, controller) is genuinely the next
# wave, and the transports this wave builds have no consumer until it lands.
# PIN EVOLUTION (T052-T054 landed, 2026-07-31): the tuple's own contract was
# "app.js must comment each REMAINING task group so transport absence reads
# as deliberate". The chat model, view, and rail wiring have all landed, so
# the set is EMPTY — the consuming test stays as the mechanism for any future
# deferral, and app.js's comments now record the landing as history.
REMAINING_TASK_GROUPS = ()

# Literal spellings a CREDENTIAL, or a transport that reaches past a transport's
# job, would need. Deliberately NOT a bare "token" or "model" ban: both already
# occur in unrelated existing code and a blanket ban would be a false positive,
# not a real proof.
#
# PIN EVOLUTION (T023 wire clause, 2026-07-30). This tuple's own contract was
# "app.js executable lines must not name X BEFORE the catalog/chat/Save browser
# transports land". The catalog and chat transports have now LANDED, so exactly
# the two needles those transports must spell -- "catalog" and "chat", which
# appear only inside the two same-origin route paths -- are removed. Nothing
# else moves:
#   * every CREDENTIAL needle STAYS ("Authorization", "Bearer", "api-key",
#     "apiKey", "API_KEY"): a transport carries the console-presence token the
#     edit transport already carries and nothing else, and FR-020/FR-022 are
#     untouched by the contract release;
#   * "/save" STAYS: the Save seam still composes through swb-session.js's ONE
#     request site, never a route literal here (T080's pinned placement);
#   * "schema_version", "kind:", "model_id", "modelId", "provider" STAY, and
#     this is the load-bearing half of the evolution: a TRANSPORT moves bytes.
#     It does not build a request envelope, read a model id, or interpret a
#     provider class -- that is the chat MODEL's job (T052), and if any of these
#     appears in app.js the transport has grown into the thing it was supposed
#     to stay out of.
FORBIDDEN_LITERALS = (
    "/save", "Authorization", "Bearer",
    "api-key", "apiKey", "API_KEY", "schema_version", "kind:",
    "model_id", "modelId", "provider",
)

# The two same-origin routes the new transports call, and the ONE header they
# carry. Spelled here so the tests below pin the exact wire surface rather than
# a paraphrase of it.
CATALOG_ROUTE = "/workbench/model-catalog"
CHAT_TURN_ROUTE = "/actions/workbench/chat-turn"
CONSOLE_TOKEN_HEADER = "X-XF-Console-Token"


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ----------------------------------------------------------------------------
# (a) the source-loading seam: structure, call-site arithmetic, no re-implementation
# ----------------------------------------------------------------------------

def test_app_js_defines_a_module_scope_source_loader_factory():
    app = APP_JS.read_text(encoding="utf-8")
    assert "export function createDoxBenchSourceLoader(sourceBaseOf, injectedFetch) {" in app
    assert "return async function loadDoxBenchSource(path) {" in app
    # it reaches the read-only /source base through the WORKBENCH'S OWN
    # current source base -- a zero-arg closure read at call time, never a
    # snapshotted value
    assert "createDoxBenchSourceLoader(() => workbenchSourceBase)" in app
    assert 'cache: "no-store"' in app


def test_app_js_carries_exactly_the_four_named_fetch_call_sites():
    """PIN EVOLUTION (T023 wire clause): the cap rises from 2 to 4, one per
    NAMED call site, and each is asserted individually -- the cap is a budget
    on transports, so raising it without naming what filled it would make it
    meaningless. The four: the pre-existing snapshot fetch, the source-loading
    pass-through, and the two transports this wave adds (GET the released model
    catalog, POST a chat turn)."""
    app = APP_JS.read_text(encoding="utf-8")
    fetches = re.findall(r"fetch\(([^)]*)", app)
    assert len(fetches) == 4, (
        f"app.js must carry exactly four fetch( call sites (snapshot, source "
        f"pass-through, model-catalog GET, chat-turn POST), found: {fetches}"
    )
    assert any("snapshotUrl" in a or "snapshot" in a.lower() for a in fetches), (
        "the pre-existing snapshot fetch must still be present"
    )
    assert any("sourceBase" in a and "no-store" in a for a in fetches), (
        "the source-loading fetch must name the (workbench) source base and "
        "still pass cache: no-store"
    )
    assert sum("CATALOG_ROUTE" in a for a in fetches) == 1, (
        "exactly one call site may GET the model-catalog route"
    )
    assert sum("CHAT_TURN_ROUTE" in a for a in fetches) == 1, (
        "exactly one call site may POST a chat turn"
    )


def test_app_js_contains_no_second_markdown_or_sanitizer_implementation():
    app = APP_JS.read_text(encoding="utf-8")
    assert "markdownit(" not in app
    assert "renderSafeMarkdownHtml(" not in app
    assert "mountSafeMarkdown(" not in app


# ----------------------------------------------------------------------------
# (a2) the CATALOG and CHAT-TURN transports (T023 wire clause, 2026-07-30)
#
# Both routes are released, enveloped, and server-side validated, so the two
# transports T023 always named are built here -- and ONLY the transports. They
# are composed exactly like `createDoxBenchSourceLoader`: a module-scope factory
# closing over an injected fetch and a call-time token reader, returning one
# async function that moves bytes. No rendering, no persisting, no envelope
# building, no field reading. Their CONSUMER is the chat UI (T052-T054), which
# is the next wave; this wave builds and bundles them.
# ----------------------------------------------------------------------------

def test_app_js_defines_the_two_transport_factories_at_module_scope():
    app = APP_JS.read_text(encoding="utf-8")
    assert "export function createDoxBenchCatalogLoader(consoleTokenOf, injectedFetch) {" in app
    assert "export function createDoxBenchTurnSubmitter(consoleTokenOf, injectedFetch) {" in app
    assert "return async function loadDoxBenchCatalog() {" in app
    assert "return async function submitDoxBenchTurn(request) {" in app


def test_the_two_routes_are_module_constants_not_inline_literals():
    app = APP_JS.read_text(encoding="utf-8")
    assert f'const CATALOG_ROUTE = "{CATALOG_ROUTE}";' in app
    assert f'const CHAT_TURN_ROUTE = "{CHAT_TURN_ROUTE}";' in app
    # Each route path appears exactly ONCE in the file: in its own constant.
    assert app.count(CATALOG_ROUTE) == 1
    assert app.count(CHAT_TURN_ROUTE) == 1


def test_the_transports_are_bundled_on_the_doxbench_seam_and_nothing_else():
    """app.js BUILDS and BUNDLES; it never renders or persists with a seam.
    The bundle gains the two transports beside the existing loadSource/hash/save
    entries, each closing over the CAPS-derived console token read at call time
    (a capability re-probe or session re-key is honoured by the next call)."""
    app = APP_JS.read_text(encoding="utf-8")
    bundle = app.split("const doxbenchSeams = {", 1)[1].split("};", 1)[0]
    assert "loadSource: createDoxBenchSourceLoader(() => workbenchSourceBase)" in bundle
    assert "hash: contentIdentity" in bundle
    assert "catalog: createDoxBenchCatalogLoader(() => caps?.console_token)" in bundle
    assert "chatTurn: createDoxBenchTurnSubmitter(() => caps?.console_token)" in bundle


def test_the_transports_carry_only_the_console_presence_header():
    app = APP_JS.read_text(encoding="utf-8")
    assert f'const CONSOLE_TOKEN_HEADER = "{CONSOLE_TOKEN_HEADER}";' in app
    # The SAME header the edit transport already carries -- never a second
    # credential-shaped header, and never a credential of any kind (the
    # credential needles in FORBIDDEN_LITERALS remain banned above).
    assert app.count(CONSOLE_TOKEN_HEADER) == 1


def test_the_transports_neither_render_nor_persist_nor_read_turn_fields():
    """The transports must stay transports. A field read here would mean the
    chat MODEL's job (T052) leaked into app.js -- which is what the surviving
    `schema_version`/`kind:`/`model_id`/`provider` bans above catch -- and a
    storage or DOM write would mean the same for the view."""
    app = APP_JS.read_text(encoding="utf-8")
    factories = app.split("export function createDoxBenchCatalogLoader", 1)[1].split(
        "async function loadSnapshot", 1)[0]
    for forbidden in ("sessionStorage", "localStorage", "innerHTML",
                      "document.", "renderMarkdown", "assistant_prose",
                      "proposals", "observed_hashes", "client_turn_id"):
        assert forbidden not in factories, forbidden


# ----------------------------------------------------------------------------
# (b) the hash-authority injection: the shared contentIdentity, never a local one
# ----------------------------------------------------------------------------

def test_app_js_imports_the_shared_hash_authority():
    app = APP_JS.read_text(encoding="utf-8")
    assert 'import { contentIdentity } from "./views/doxbench-state.js";' in app
    assert "hash: contentIdentity" in app


def test_app_js_defines_no_sha256_of_its_own():
    app = APP_JS.read_text(encoding="utf-8")
    assert "crypto.subtle" not in app
    assert "sha256Hex" not in app
    assert not re.search(r"\bfunction\s+sha256\w*\(", app)
    # SHA-256's first initial-hash-value word, hex-spelled -- a hand-rolled
    # digest would need it; the shared authority in doxbench-state.js is the
    # only place it may legitimately live (it doesn't spell it either -- it
    # defers to Web Crypto), so its absence here is a real proof, not a guess.
    assert "6a09e667" not in app


# ----------------------------------------------------------------------------
# (c) deliberate absence: no catalog/chat/Save transport, no credential spelling
# ----------------------------------------------------------------------------

def test_app_js_contains_no_catalog_chat_save_or_credential_transport():
    app = APP_JS.read_text(encoding="utf-8")
    # Full-line comments describe the current server-side foundations and the
    # remaining browser work. Scan executable lines so accurate commentary is
    # not mistaken for an implemented transport.
    scan = "\n".join(
        line for line in app.splitlines()
        if not line.lstrip().startswith("//")
    )
    for needle in FORBIDDEN_LITERALS:
        assert needle not in scan, (
            f"app.js executable lines must not name {needle!r} before the "
            f"catalog/chat/Save browser transports land"
        )


def test_app_js_documents_the_remaining_tasks_for_the_absent_seams():
    app = APP_JS.read_text(encoding="utf-8")
    for task_group in REMAINING_TASK_GROUPS:
        assert task_group in app, (
            f"app.js must comment remaining tasks {task_group} so a future reader "
            f"can tell the browser transport absence is deliberate, not forgotten"
        )


# ----------------------------------------------------------------------------
# (d) the staging-workbench.js pass-through: accepts, does not itself transport
# ----------------------------------------------------------------------------

def test_staging_workbench_accepts_the_doxbench_option_between_index_and_sourcebase():
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    # the three pinned option-destructure substrings (test_staging_workbench.py,
    # test_workbench_posture_and_affordances_are_capability_derived /
    # test_the_outline_pane_reads_through_the_active_keys_source_base) --
    # unmoved, verbatim
    assert "{ onOpenDoc, caps, fetcher, active, index," in view
    assert "sourceBase, edit, onSessionRekey," in view
    assert "onSessionEnded, onScopeOpened } = {})" in view
    destructure = view.split("{ onOpenDoc, caps, fetcher, active, index,", 1)[1].split(
        "onSessionEnded, onScopeOpened } = {})", 1
    )[0]
    assert "doxbench," in destructure, "the new option must be accepted in the destructure"
    assert destructure.index("doxbench,") < destructure.index("sourceBase, edit, onSessionRekey,"), (
        "doxbench must sit between index, and sourceBase, edit, onSessionRekey,"
    )


def _call_arguments(source: str, call: str) -> str:
    """The argument text of ONE call, isolated by a balanced-paren scan from
    the call's own `(` -- so a check on it cannot be satisfied by a
    neighbouring line that happens to contain the same substrings (the same
    discipline test_session_confinement.py's own `_call_arguments` uses)."""
    start = source.index(call) + len(call)
    depth = 1
    for i in range(start, len(source)):
        if source[i] == "(":
            depth += 1
        elif source[i] == ")":
            depth -= 1
            if depth == 0:
                return source[start:i]
    raise AssertionError(f"the call {call!r} is never closed in this source")


def test_staging_workbench_forwards_loadsource_and_hash_into_the_canvas_mount():
    """T023, lead-adjudicated ownership extension: the `doxbench` option
    accepted above is forwarded into `mountDoxBenchCanvas` verbatim -- the
    ONLY seam this composition carries, and never a transport of its own
    (test_staging_workbench_still_issues_no_transport_of_its_own, below,
    still holds).

    PIN EVOLUTION (R-1, 2026-08-02). This test previously asserted
    `"storage" not in call`, on the stated theory that "doxbench-state.js's
    own sessionStorageOf fallback binds real session persistence at the
    mount, so an explicit handle would be a second spelling of the same
    binding". That theory was PLAUSIBLE AND FALSE, and the operator's
    real-corpus runs disproved it: a reload destroyed unsaved buffers, and a
    live probe found sessionStorage EMPTY after a real keystroke. The
    fallback exists but is UNREACHABLE from this mount, because
    doxbench-editor.js gates both `persistNow` and its restore on a truthy
    `storage` handle -- with none forwarded it never calls into
    doxbench-state.js at all, so the fallback never runs. The handle is now
    forwarded (injected at the app.js composition root, never read from a
    global inside a view), which is what makes persistence real; the FR-039
    clearing path stays pinned by
    test_staging_workbench_clears_doxbench_state_when_a_session_ends below,
    and the RENDERED restore is pinned live by the T098 smoke's step 10d."""
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    call = _call_arguments(view, "mountDoxBenchCanvas(canvas, projection,")
    assert "title: scope.title" in call
    assert "loadSource: doxbench?.loadSource" in call
    assert "hash: doxbench?.hash" in call
    assert "storage: doxbench?.storage" in call, (
        "R-1: the storage handle must be forwarded -- the editor gates "
        "persistence on it, so an unforwarded handle means no persistence")
    # Still injected, never grabbed: no view may reach for a storage global.
    for global_grab in ("window.sessionStorage", "globalThis.sessionStorage",
                        "localStorage"):
        assert global_grab not in view, global_grab


def test_staging_workbench_clears_doxbench_state_when_a_session_ends():
    """FR-039 (T081, re-scoped 2026-07-30 wiring wave): ending a session by
    merge or abandon clears the browser-local doxBench working state persisted
    under that session ref. The SESSION branch is captured BEFORE the shell
    rebinds to main -- after the rebind nothing remembers which ref died --
    and the clear runs only once the end is confirmed (a null next means the
    session did not actually end)."""
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    assert 'clearDoxBenchSession' in view, "the shell must import the clearing helper"
    assert 'from "./doxbench-state.js"' in view
    handler = view.split("onSessionEnded: async () => {", 1)[1].split(
        "onRerender:", 1)[0]
    assert "endedBranch" in handler, "the session branch must be captured pre-rebind"
    idx_confirm = handler.index("if (!next?.snapshot || !scope) return null;")
    idx_clear = handler.index("clearDoxBenchSession(")
    assert idx_clear > idx_confirm, "clear only after the end is confirmed"
    call = _call_arguments(handler, "clearDoxBenchSession(")
    assert "ref: endedBranch" in call
    assert "tile_kind: scope.kind" in call and "tile_id: scope.id" in call


def test_staging_workbench_still_issues_no_transport_of_its_own():
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    assert "fetch(" not in view
    assert "XMLHttpRequest" not in view
    assert "doFetch" not in view


# ----------------------------------------------------------------------------
# (e) Node behavioural harness: the ACTUAL loader against an injected fake fetch
# ----------------------------------------------------------------------------

_CRLF_CONTENT = "line one\r\nline two — café éclair\r\n日本語\n"

_LOADER_HARNESS = r"""
import { createDoxBenchSourceLoader } from './app.mjs';

function fakeResponse({ ok, content, ref }) {
  return {
    ok,
    status: ok ? 200 : 404,
    headers: { get: (name) => (name === 'X-Snapshot-Ref' ? (ref ?? null) : null) },
    text: async () => content,
  };
}

const calls = [];
const queue = [];
const fakeFetch = async (url, opts) => {
  calls.push({ url, opts });
  const next = queue.shift();
  if (!next) throw new Error('no fake response queued for ' + url);
  return next;
};

let currentBase = '/source/repo-a@main/';
const loader = createDoxBenchSourceLoader(() => currentBase, fakeFetch);

const CRLF_CONTENT = """ + repr(_CRLF_CONTENT).replace("'", "\"") + r""";

// 1: a 200 response yields exact byte-for-byte content (CRLF + non-ASCII) and
// surfaces X-Snapshot-Ref as `ref`
queue.push(fakeResponse({ ok: true, content: CRLF_CONTENT, ref: 'sha-ref-1' }));
const result1 = await loader('docs/a.md');

// 2: a 200 response with no X-Snapshot-Ref header surfaces `ref: null`
queue.push(fakeResponse({ ok: true, content: 'no ref present', ref: null }));
const result2 = await loader('docs/b.md');

// 3: a non-ok response yields null (the editor's own honest "unavailable")
queue.push(fakeResponse({ ok: false, content: '', ref: null }));
const result3 = await loader('docs/missing.md');

// 4: the source base is read AT CALL TIME -- changing it between calls
// changes what the very next load requests (a session re-key)
currentBase = '/source/repo-b@draft%2Ftopic/';
queue.push(fakeResponse({ ok: true, content: 'second base content', ref: 'sha-ref-2' }));
const result4 = await loader('docs/c.md');

console.log(JSON.stringify({ result1, result2, result3, result4, calls }));
"""


def _run_node_harness(tmp_path, harness_source, harness_name):
    """Copy the web tree, strip app.js's top-level `await main();` so it can be
    imported as a module, run `harness_source` under node, and return its JSON.

    Factored out when the catalog/chat transports landed (T023 wire clause):
    two harnesses now drive app.js exports the same way, and a second copy of
    this setup would be a second thing to keep in sync."""
    web_copy = tmp_path / "web"
    shutil.copytree(WEB, web_copy)
    # app.js (and everything it imports) is hand-written ES module source with
    # NO package.json of its own; force the copied tree to ESM so the whole
    # import graph resolves, and force the vendored markdown-it back to
    # CommonJS (its own UMD shape assumes it, same override
    # test_doxbench_view.py's editor harness already uses).
    (web_copy / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (web_copy / "vendor" / "package.json").write_text('{"type": "commonjs"}', encoding="utf-8")

    original = (web_copy / "app.js").read_text(encoding="utf-8")
    assert original.rstrip().endswith("await main();"), (
        "harness precondition failed: app.js must end with the top-level "
        "`await main();` call for this strip-and-import harness to be valid"
    )
    trimmed = original.rstrip()
    trimmed = trimmed[: -len("await main();")].rstrip() + "\n"
    (web_copy / "app.mjs").write_text(trimmed, encoding="utf-8")

    harness = web_copy / harness_name
    harness.write_text(harness_source, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness)], capture_output=True, text=True, timeout=30, cwd=web_copy,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@pytest.mark.skipif(NODE is None, reason="node not available for the doxBench source-loader probe")
def test_source_loader_behaves_correctly_against_an_injected_fetch(tmp_path):
    results = _run_node_harness(tmp_path, _LOADER_HARNESS, "loader-harness.mjs")

    assert results["result1"] == {"content": _CRLF_CONTENT, "ref": "sha-ref-1"}
    assert results["result2"] == {"content": "no ref present", "ref": None}
    assert results["result3"] is None
    assert results["result4"] == {"content": "second base content", "ref": "sha-ref-2"}

    calls = results["calls"]
    assert len(calls) == 4
    assert calls[0]["url"] == "/source/repo-a@main/docs/a.md"
    assert calls[1]["url"] == "/source/repo-a@main/docs/b.md"
    assert calls[2]["url"] == "/source/repo-a@main/docs/missing.md"
    # the base changed between calls 3 and 4 -- proof the loader re-reads it
    # at call time rather than closing over a stale value
    assert calls[3]["url"] == "/source/repo-b@draft%2Ftopic/docs/c.md"
    for call in calls:
        assert call["opts"] == {"cache": "no-store"}
        assert call["url"].startswith("/"), "must be a same-origin relative URL"
        assert "://" not in call["url"], "must never be an absolute/off-origin URL"



_TRANSPORT_HARNESS = r"""
import { createDoxBenchCatalogLoader, createDoxBenchTurnSubmitter } from './app.mjs';

function fakeResponse({ ok, status, payload, unparseable }) {
  return {
    ok,
    status,
    json: async () => {
      if (unparseable) throw new Error('not json');
      return payload;
    },
  };
}

const calls = [];
const queue = [];
const fakeFetch = async (url, opts) => {
  calls.push({ url, opts });
  const next = queue.shift();
  if (!next) throw new Error('no fake response queued for ' + url);
  return next;
};

let token = 'console-token-one';
const loadCatalog = createDoxBenchCatalogLoader(() => token, fakeFetch);
const submitTurn = createDoxBenchTurnSubmitter(() => token, fakeFetch);

const ENVELOPE = {
  schema_version: 1,
  kind: 'workbench-model-catalog',
  models: [{ model_id: 'opaque-local-id', label: 'Approved authoring model',
             provider_class: 'on-tenant', available: true,
             input_limit_bytes: 800000, output_limit_bytes: 900000,
             data_handling: 'Processed in the approved tenant boundary' }],
};

// 1: a 200 catalog response is surfaced VERBATIM, envelope and all
queue.push(fakeResponse({ ok: true, status: 200, payload: ENVELOPE }));
const catalog1 = await loadCatalog();

// 2: the empty editor-only posture is a SUCCESS, not a null
queue.push(fakeResponse({ ok: true, status: 200,
  payload: { schema_version: 1, kind: 'workbench-model-catalog', models: [] } }));
const catalog2 = await loadCatalog();

// 3: a refusal yields null -- the caller keeps its own honest editor-only state
queue.push(fakeResponse({ ok: false, status: 403,
  payload: { ok: false, error: 'console_required', message: 'no' } }));
const catalog3 = await loadCatalog();

// 4: the token is read AT CALL TIME (a capability re-probe / session re-key)
token = 'console-token-two';
queue.push(fakeResponse({ ok: true, status: 200, payload: ENVELOPE }));
const catalog4 = await loadCatalog();

// 5: a turn POST returns status AND payload -- a refusal carries meaning, so
// the transport never collapses it to null
const REQUEST = { schema_version: 1, kind: 'workbench-chat-turn', opaque: 'passthrough' };
queue.push(fakeResponse({ ok: false, status: 403, payload: {
  schema_version: 1, kind: 'workbench-chat-turn-failure',
  client_turn_id: 'turn-1', error: 'model_capability_unavailable', message: 'no' } }));
const turn1 = await submitTurn(REQUEST);

// 6: a success envelope passes through untouched and uninterpreted
queue.push(fakeResponse({ ok: true, status: 200, payload: {
  schema_version: 1, kind: 'workbench-chat-turn-success', client_turn_id: 'turn-2' } }));
const turn2 = await submitTurn(REQUEST);

// 7: an unparseable body is `payload: null`, never a throw and never invented
queue.push(fakeResponse({ ok: false, status: 500, unparseable: true }));
const turn3 = await submitTurn(REQUEST);

console.log(JSON.stringify({ catalog1, catalog2, catalog3, catalog4,
                             turn1, turn2, turn3, calls,
                             requestUnmutated: REQUEST }));
"""


@pytest.mark.skipif(NODE is None, reason="node not available for the doxBench transport probe")
def test_the_catalog_and_chat_transports_behave_correctly_against_an_injected_fetch(tmp_path):
    """The ACTUAL transports, driven against an injected fake fetch -- the same
    strip-and-import harness the source loader uses. What is proven: verbatim
    pass-through in both directions, the empty-catalog SUCCESS posture, an
    honest `null` on a catalog refusal, status+payload on every turn outcome,
    `payload: null` on an unparseable body, same-origin relative URLs only, the
    exact console header, and the token read at CALL time."""
    results = _run_node_harness(tmp_path, _TRANSPORT_HARNESS, "transport-harness.mjs")

    envelope_models = results["catalog1"]["models"]
    assert results["catalog1"]["schema_version"] == 1
    assert results["catalog1"]["kind"] == "workbench-model-catalog"
    assert envelope_models[0]["model_id"] == "opaque-local-id"
    assert results["catalog2"]["models"] == []          # success, not null
    assert results["catalog3"] is None                  # refusal -> honest null
    assert results["catalog4"]["kind"] == "workbench-model-catalog"

    assert results["turn1"] == {"ok": False, "status": 403, "payload": {
        "schema_version": 1, "kind": "workbench-chat-turn-failure",
        "client_turn_id": "turn-1", "error": "model_capability_unavailable",
        "message": "no"}}
    assert results["turn2"]["ok"] is True
    assert results["turn2"]["payload"]["kind"] == "workbench-chat-turn-success"
    assert results["turn3"] == {"ok": False, "status": 500, "payload": None}
    # The request object is passed through, never rewritten by the transport.
    assert results["requestUnmutated"] == {
        "schema_version": 1, "kind": "workbench-chat-turn", "opaque": "passthrough"}

    calls = results["calls"]
    assert len(calls) == 7
    assert [c["url"] for c in calls[:4]] == [CATALOG_ROUTE] * 4
    assert [c["url"] for c in calls[4:]] == [CHAT_TURN_ROUTE] * 3
    for call in calls:
        assert call["url"].startswith("/"), "must be a same-origin relative URL"
        assert "://" not in call["url"], "must never be an absolute/off-origin URL"

    # GET the catalog: no method, no body, no-store, console header only.
    for call in calls[:4]:
        assert "method" not in call["opts"]
        assert "body" not in call["opts"]
        assert call["opts"]["cache"] == "no-store"
        assert set(call["opts"]["headers"]) == {CONSOLE_TOKEN_HEADER}
    # the token was re-read at call time
    assert calls[0]["opts"]["headers"][CONSOLE_TOKEN_HEADER] == "console-token-one"
    assert calls[3]["opts"]["headers"][CONSOLE_TOKEN_HEADER] == "console-token-two"

    # POST a turn: JSON content type plus the console header, and nothing else.
    for call in calls[4:]:
        assert call["opts"]["method"] == "POST"
        assert set(call["opts"]["headers"]) == {"Content-Type", CONSOLE_TOKEN_HEADER}
        assert call["opts"]["headers"]["Content-Type"] == "application/json"
        assert json.loads(call["opts"]["body"]) == {
            "schema_version": 1, "kind": "workbench-chat-turn",
            "opaque": "passthrough"}


# ----------------------------------------------------------------------------
# (f) real HTTP: the keyed /source/<repository>@<ref>/<path> route this seam
#     assumes really behaves as assumed
# ----------------------------------------------------------------------------

@contextmanager
def _serving_keyed(tmp_path, *, head):
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(_snapshot()), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap_path, BASE_REPO, head=head, repository="fixture-repo")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _raw_get(host, port, raw_path, method="GET"):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.putrequest(method, raw_path, skip_host=False, skip_accept_encoding=True)
    conn.putheader("Host", f"{host}:{port}")
    conn.endheaders()
    resp = conn.getresponse()
    body = resp.read()
    headers = {k.lower(): v for k, v in resp.getheaders()}
    conn.close()
    return resp.status, headers, body


def test_keyed_source_route_returns_exact_bytes_and_the_snapshot_ref_header(tmp_path):
    rel = "ideation/brainstorm/legacy-note.md"
    with _serving_keyed(tmp_path, head=PINNED_REVISION) as (host, port):
        status, headers, body = _raw_get(host, port, "/source/fixture-repo@main/" + rel)
    assert status == 200
    assert body == (BASE_REPO / rel).read_bytes()
    assert headers.get("x-snapshot-ref") == "main"
    assert headers.get("x-snapshot-repository") == "fixture-repo"


# ----------------------------------------------------------------------------
# (g) T080 client half: the mount-site save-seam adapter (2026-07-30 slice)
# ----------------------------------------------------------------------------

def test_the_save_seam_is_composed_in_the_sibling_transport_and_forwarded():
    """The doctrinal placement the pins themselves mandate: the ROUTE is a
    model constant, the POSTER lives in swb-session.js (the sibling verbs
    module, through its ONE request site `submitSession` — no new request
    site, no new write-method literal), app.js bundles the ready-made seam
    into its `doxbench` option, and the shell FORWARDS it exactly like
    loadSource/hash. The shell and model stay transport-free."""
    model = (WEB / "views" / "staging-workbench-model.js").read_text(
        encoding="utf-8")
    assert 'FIRST_EDIT_ROUTE = "/actions/gate/first-edit"' in model
    assert "[SESSION_FIRST_EDIT]: FIRST_EDIT_ROUTE," in model
    session = (WEB / "views" / "swb-session.js").read_text(encoding="utf-8")
    assert "export function firstEditTransport(" in session
    seam_fn = session.split("export function firstEditTransport(", 1)[1]
    assert "submitSession(" in seam_fn.split("export function", 1)[0], (
        "the transport must post through the ONE existing request site")
    assert "SESSION_FIRST_EDIT" in seam_fn.split("export function", 1)[0]
    assert session.count('method: "POST"') == 1, (
        "still exactly one write-method literal in the sibling module")
    assert 'from "./doxbench-save.js"' not in session, (
        "the sibling keeps its no-sibling-import harness discipline")
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    assert "save: doxbench?.save," in view
    app = APP_JS.read_text(encoding="utf-8")
    assert 'import { firstEditTransport } from "./views/swb-session.js";' in app
    assert "runSave(" in app and "savePlanState(request)" in app


def test_the_seam_mappings_are_pure_model_functions():
    """Body and verdict mapping live in the transport-free model module, so
    the wire vocabulary (scope_kind/scope_id, the hex spelling of base_hash,
    commit->revision) is derived and testable without a transport — and the
    `kind:`-bearing body never needs to be spelled in app.js."""
    model = (WEB / "views" / "staging-workbench-model.js").read_text(
        encoding="utf-8")
    assert "export function firstEditBody(" in model
    assert "export function firstEditVerdict(" in model
    body_fn = model.split("export function firstEditBody(", 1)[1].split(
        "export function", 1)[0]
    assert "scope_kind" in body_fn and "scope_id" in body_fn
    assert "base_hash" in body_fn
    verdict_fn = model.split("export function firstEditVerdict(", 1)[1].split(
        "export function", 1)[0] if model.count("export function") > model.index(
        "firstEditVerdict") else model.split(
        "export function firstEditVerdict(", 1)[1]
    assert "revision" in verdict_fn and "commit" in verdict_fn, (
        "the verdict mapping must translate the verb's commit into the "
        "seam's revision")


def test_the_shell_still_creates_no_transport_of_its_own_with_the_seam_wired():
    """The composition uses ONLY the injected fetcher: wiring the seam must not
    add a transport primitive to the shell (the same discipline the sibling
    verb modules follow)."""
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    assert "fetch(" not in view
    assert "XMLHttpRequest" not in view
    assert "doFetch" not in view
    assert "sendBeacon" not in view
