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
# PIN EVOLUTION (T104 F8-1, 2026-08-04): with the roster empty, the consumer's
# for-loop body never ran — one permanently green test asserting NOTHING. The
# consumer is now parametrized over the roster, so an empty roster collects no
# per-group assertion (pytest surfaces the empty parameter set as a skip, not
# a pass), and a repopulated roster re-enables one visible test per group. The
# POSITIVE claim the emptiness rests on — every seam the shell consumes is
# actually declared by app.js — gets its own companion test below instead of
# hiding inside a vacuous green.
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
    """PIN EVOLUTION (T023 wire clause, then add-doxbench-editing-phase-b §9.5,
    then add-doxbench-distilled-abstract §7.9): the cap rose from 2 to 4, to 5,
    and now to 6, one per NAMED call site, each asserted individually -- the cap
    is a budget on transports, so raising it without naming what filled it would
    make it meaningless. The six: the pre-existing snapshot fetch, the
    source-loading pass-through, the two transports the T023 wave added (GET the
    released model catalog, POST a chat turn), the THREAD READ, and the
    DOCUMENT-ABSTRACT route.

    The thread seam is a GET and only a GET: a thread is written by a TURN,
    through the Save gate, so a write call site here would be a second write
    route to the record.

    The abstract route is a NEW same-origin serve.py route rather than a scoped
    chat turn, ruled 1(c)(i): the chat-turn assembler requires an outline
    buffer, a non-blank human message and a transcript, and an abstract request
    carries none of them, so smuggling one through that envelope would have
    meant widening a released contract to carry a request it was not written
    for. Its body is a CLOSED shape -- scope, subject path, model id -- and
    carries no buffer, because the server reads the subject's SAVED bytes."""
    app = APP_JS.read_text(encoding="utf-8")
    fetches = re.findall(r"fetch\(([^)]*)", app)
    assert len(fetches) == 6, (
        f"app.js must carry exactly six fetch( call sites (snapshot, source "
        f"pass-through, model-catalog GET, chat-turn POST, thread GET, "
        f"document-abstract POST), found: {fetches}"
    )
    assert sum("DOCUMENT_ABSTRACT_ROUTE" in a for a in fetches) == 1, (
        "exactly one call site may reach the document-abstract route"
    )
    assert sum("threadUrl" in a for a in fetches) == 1, (
        "exactly one call site may GET a document's thread"
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
    # add-doxbench-editing-phase-b §9.5: the thread READ route joins them under
    # the same rule.
    assert 'const THREAD_ROUTE = "/workbench/thread";' in app
    # Each route path appears exactly ONCE in the file: in its own constant.
    assert app.count(CATALOG_ROUTE) == 1
    assert app.count(CHAT_TURN_ROUTE) == 1
    assert app.count("/workbench/thread") == 1


def test_the_thread_transport_names_no_field_of_the_query_it_carries():
    """A TRANSPORT MOVES BYTES, and this one is handed an already-built
    parameter object for the same reason the turn submitter is handed an
    already-built envelope: a transport that spelled the scope's own field names
    would have grown into the thing that decides what a request says."""
    app = APP_JS.read_text(encoding="utf-8")
    body = app.split("export function createDoxBenchThreadLoader(", 1)[1] \
              .split("\nexport function ", 1)[0]
    for forbidden in ("tile_kind", "tile_id", "repository", "schema_version"):
        assert forbidden not in body, forbidden
    assert "method:" not in body, (
        "the thread seam is a GET and only a GET: a thread is written by a "
        "turn, through the Save gate")


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


@pytest.mark.parametrize("task_group", REMAINING_TASK_GROUPS)
def test_app_js_documents_the_remaining_tasks_for_the_absent_seams(task_group):
    # One collected test PER deferred group. An empty roster therefore
    # contributes zero passing assertions (T104 F8-1: the old for-loop body
    # never executed, so the test was green while proving nothing).
    app = APP_JS.read_text(encoding="utf-8")
    assert task_group in app, (
        f"app.js must comment remaining tasks {task_group} so a future reader "
        f"can tell the browser transport absence is deliberate, not forgotten"
    )


# Every seam the SHELL reads off its `doxbench` option bundle, in either the
# guarded (`doxbench?.loadSource`) or bare (`doxbench.catalog`) spelling.
_SHELL_SEAM_USE = re.compile(r"\bdoxbench(?:\?\.|\.)(\w+)\b")


def test_app_js_declares_every_seam_the_shell_consumes():
    """T104 F8-1 companion: the POSITIVE claim behind the empty roster above.
    An empty REMAINING_TASK_GROUPS asserts "nothing is deferred any more" —
    which is only true while app.js's `doxbenchSeams` literal really declares
    every seam the staging-workbench shell consumes. Derive the consumed set
    from the shell's own source (so a newly consumed seam extends this pin by
    itself) and require each one as a key in the bundle app.js builds (same
    split technique as the bundle test in section (a) above)."""
    shell = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    consumed = sorted(set(_SHELL_SEAM_USE.findall(shell)))
    assert consumed, (
        "the shell no longer reads any doxbench seam at all — if that is a "
        "real re-architecture, this pin and the roster need re-derivation, "
        "not deletion"
    )
    app = APP_JS.read_text(encoding="utf-8")
    bundle = app.split("const doxbenchSeams = {", 1)[1].split("};", 1)[0]
    missing = [s for s in consumed if not re.search(rf"\b{s}\s*:", bundle)]
    assert not missing, (
        f"the shell consumes doxbench seam(s) {missing} that app.js's "
        f"doxbenchSeams literal never declares — the empty "
        f"REMAINING_TASK_GROUPS roster would be claiming completion falsely"
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
    # T104 F7-7: the clear targets the INJECTED storage seam, exactly as the
    # editor's own re-key clear does (doxbench-editor.js threads `storage`).
    # The one-argument call fell through to ambient window.sessionStorage, so
    # under any injected storage -- the shell harness's FakeStorage, or a
    # future non-window seam -- the ended session's record was never removed
    # (FR-039 silently unmet). The behavioural pin lives in
    # test_doxbench_view.py's mounted-shell harness.
    assert "doxbench?.storage" in call, (
        "clearDoxBenchSession must be handed the injected doxbench storage "
        "seam, never left to the ambient window global")


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

// 3: a 403 console refusal yields the DISTINGUISHED stale-token failure --
// never a bare null (T104 F10-1: null collapsed a recoverable stale token
// into "no approved model is configured")
queue.push(fakeResponse({ ok: false, status: 403,
  payload: { ok: false, error: 'console_required', message: 'no' } }));
const catalog3 = await loadCatalog();

// 4: the token is read AT CALL TIME (a capability re-probe / session re-key)
token = 'console-token-two';
queue.push(fakeResponse({ ok: true, status: 200, payload: ENVELOPE }));
const catalog4 = await loadCatalog();

// 5: a 500 (or any other non-ok answer) is the could-not-be-read failure --
// distinguished from BOTH the stale token and the configured-none success
queue.push(fakeResponse({ ok: false, status: 500,
  payload: { ok: false, error: 'catalog_unavailable', message: 'boom' } }));
const catalog5 = await loadCatalog();

// 6: the gate-action route spells the same pre-identity refusal
// `agent_invocation` (the R-3 pair) -- same stale-token mapping
queue.push(fakeResponse({ ok: false, status: 403,
  payload: { ok: false, error: 'agent_invocation', message: 'no' } }));
const catalog6 = await loadCatalog();

// 7: a non-ok answer whose body cannot even be parsed still maps to the
// fixed could-not-be-read failure, never a throw and never an echo
queue.push(fakeResponse({ ok: false, status: 502, unparseable: true }));
const catalog7 = await loadCatalog();

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
                             catalog5, catalog6, catalog7,
                             turn1, turn2, turn3, calls,
                             requestUnmutated: REQUEST }));
"""


@pytest.mark.skipif(NODE is None, reason="node not available for the doxBench transport probe")
def test_the_catalog_and_chat_transports_behave_correctly_against_an_injected_fetch(tmp_path):
    """The ACTUAL transports, driven against an injected fake fetch -- the same
    strip-and-import harness the source loader uses. What is proven: verbatim
    pass-through in both directions, the empty-catalog SUCCESS posture, a
    DISTINGUISHED fixed failure on every catalog refusal (T104 F10-1: the old
    null collapsed a recoverable 403 stale token and a 500 broken catalog
    into one misdiagnosis, "no approved model is configured"), status+payload
    on every turn outcome, `payload: null` on an unparseable body, same-origin
    relative URLs only, the exact console header, and the token read at CALL
    time."""
    results = _run_node_harness(tmp_path, _TRANSPORT_HARNESS, "transport-harness.mjs")

    envelope_models = results["catalog1"]["models"]
    assert results["catalog1"]["schema_version"] == 1
    assert results["catalog1"]["kind"] == "workbench-model-catalog"
    assert envelope_models[0]["model_id"] == "opaque-local-id"
    assert results["catalog2"]["models"] == []          # success, not null
    # T104 F10-1: the refusal is DISTINGUISHED by the body's released error
    # code, and nothing else from the body is carried (no message, no echo).
    assert results["catalog3"] == {"failed": "console_required"}
    assert results["catalog4"]["kind"] == "workbench-model-catalog"
    assert results["catalog5"] == {"failed": "unreadable"}
    assert results["catalog6"] == {"failed": "console_required"}
    assert results["catalog7"] == {"failed": "unreadable"}

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
    assert len(calls) == 10
    assert [c["url"] for c in calls[:7]] == [CATALOG_ROUTE] * 7
    assert [c["url"] for c in calls[7:]] == [CHAT_TURN_ROUTE] * 3
    for call in calls:
        assert call["url"].startswith("/"), "must be a same-origin relative URL"
        assert "://" not in call["url"], "must never be an absolute/off-origin URL"

    # GET the catalog: no method, no body, no-store, console header only.
    for call in calls[:7]:
        assert "method" not in call["opts"]
        assert "body" not in call["opts"]
        assert call["opts"]["cache"] == "no-store"
        assert set(call["opts"]["headers"]) == {CONSOLE_TOKEN_HEADER}
    # the token was re-read at call time
    assert calls[0]["opts"]["headers"][CONSOLE_TOKEN_HEADER] == "console-token-one"
    assert calls[3]["opts"]["headers"][CONSOLE_TOKEN_HEADER] == "console-token-two"

    # POST a turn: JSON content type plus the console header, and nothing else.
    for call in calls[7:]:
        assert call["opts"]["method"] == "POST"
        assert set(call["opts"]["headers"]) == {"Content-Type", CONSOLE_TOKEN_HEADER}
        assert call["opts"]["headers"]["Content-Type"] == "application/json"
        assert json.loads(call["opts"]["body"]) == {
            "schema_version": 1, "kind": "workbench-chat-turn",
            "opaque": "passthrough"}


# ----------------------------------------------------------------------------
# (e2) T104 F7-2: the STORAGE seam value is guarded. `window.sessionStorage`'s
# GETTER itself throws SecurityError when the browser blocks site data --
# app.js's own storedKey() documents exactly that and wraps its read -- yet
# the `doxbenchSeams` bundle read it UNGUARDED inside main()'s single try, so
# a browser blocking cookies replaced the ENTIRE dashboard with a false
# "Could not load the snapshot" error. The guard degrades blocked storage to
# the documented no-persistence posture (a null seam: the views already treat
# "no storage supplied" as "no persistence") while the dashboard renders.
# ----------------------------------------------------------------------------

_STORAGE_GUARD_HARNESS = r"""
import { guardedSessionStorage } from './app.mjs';

const out = {};

// 1: no `window` at all (this Node process) -- null, never a ReferenceError
out.noWindow = guardedSessionStorage();

// 2: the blocked-site-data browser: the GETTER ITSELF throws (SecurityError
// in the field; any throw here) -- null, never a propagated throw
globalThis.window = {
  get sessionStorage() { throw new Error('blocked site data'); },
};
out.blocked = guardedSessionStorage();

// 3: a live storage passes through UNTOUCHED (same object, not a wrapper)
const live = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
globalThis.window = { sessionStorage: live };
out.liveIsSameObject = guardedSessionStorage() === live;

console.log(JSON.stringify(out));
"""


@pytest.mark.skipif(NODE is None, reason="node not available for the storage-guard probe")
def test_the_storage_seam_guard_degrades_blocked_storage_to_null(tmp_path):
    """Behavioural half (stated choice: the guard is exported and driven under
    node with a throwing getter, since main() itself needs a full DOM). A
    blocked or absent sessionStorage yields null -- the no-persistence
    posture -- and a live one passes through as the same object."""
    results = _run_node_harness(tmp_path, _STORAGE_GUARD_HARNESS,
                                "storage-guard-harness.mjs")
    assert results["noWindow"] is None
    assert results["blocked"] is None
    assert results["liveIsSameObject"] is True


def test_the_seam_bundle_reads_storage_only_through_the_guard():
    """Source half: the bundle keeps its pinned `storage` KEY (the F8
    seam-declaration pin) but its VALUE goes through the guard -- app.js may
    never read `window.sessionStorage` outside a try/catch, because the
    getter is what throws under blocked site data."""
    app = APP_JS.read_text(encoding="utf-8")
    bundle = app.split("const doxbenchSeams = {", 1)[1].split("};", 1)[0]
    assert "storage: guardedSessionStorage()," in bundle
    assert "storage: window.sessionStorage" not in app, (
        "the unguarded read is exactly what a blocked-storage browser turns "
        "into a false whole-dashboard snapshot error")
    # every remaining EXECUTABLE window.sessionStorage read sits inside a try
    # block (storedKey, storeKey, and the guard itself)
    for lineno, line in enumerate(app.splitlines(), 1):
        if "window.sessionStorage" not in line or \
                line.lstrip().startswith("//"):
            continue
        assert "return window.sessionStorage" in line.strip() or \
            "window.sessionStorage.setItem" in line, (
                f"app.js:{lineno}: unexpected sessionStorage read shape: "
                f"{line.strip()}")


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


# ---------------------------------------------------------------------------
# T104 F5-1 (doxBench review, 2026-08-04): the verdict mapping put the
# server's own create-vs-edit resolution on the WRONG branch. The route's
# SUCCESS payload is what carries `verb` (gate_routes.first_edit_response:
# `"verb": outcome.action`); its refusals carry none — yet `firstEditVerdict`
# attached `action` only to the ok:false return, where doxbench-save's
# readVerdict never reads it, and OMITTED it from ok:true, where readVerdict
# adopts `answer.action` into the committed row. The server's answer could
# therefore never override the client's prediction. Same site, second bug:
# the ok:false branch dereferenced `payload.verb` after the `!payload` guard
# had already matched, so a transport that produced NO payload at all threw a
# TypeError instead of mapping to the fixed refusal.
# ---------------------------------------------------------------------------

_VERDICT_HARNESS = """
import { firstEditVerdict } from "./staging-workbench-model.mjs";

const out = {};
const SUCCESS = {
  ok: true, verb: "create-document", ref: "draft/topic-x",
  commit: "c".repeat(40), document: "ideation/staging/topic-x/detail.md",
  record: "ideation/dashboard/gate-records/draft-topic-x/create.yaml",
  content_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  session: "opened",
};
out.success = firstEditVerdict(SUCCESS);
out.successWithoutVerb = firstEditVerdict({ ...SUCCESS, verb: undefined });
try {
  out.nullPayload = firstEditVerdict(null);
  out.nullThrew = null;
} catch (error) {
  out.nullThrew = String((error && error.message) || error);
}
out.refusal = firstEditVerdict({ ok: false, message: "the base moved" });
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def verdict_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the first-edit verdict probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-verdict")
    shutil.copy(WEB / "views" / "staging-workbench-model.js",
                tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "verdict-harness.mjs"
    harness.write_text(_VERDICT_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_success_verdict_carries_the_servers_own_verb_as_action(verdict_results):
    """The half readVerdict actually reads: `answer.action` on a COMMITTED row
    is the server's `verb`, so the server's create-vs-edit answer — decided
    against the tree it wrote — overrides the client's prediction."""
    v = verdict_results["success"]
    assert v["ok"] is True
    assert v["action"] == "create-document"
    assert v["revision"] == "c" * 40
    assert v["ref"] == "draft/topic-x"
    assert v["content_hash"] == {"algorithm": "sha256", "hex": "d" * 64}


def test_a_success_without_a_verb_reports_action_null_not_invented(verdict_results):
    assert verdict_results["successWithoutVerb"]["action"] is None


def test_a_null_transport_payload_maps_to_the_fixed_refusal_not_a_typeerror(
        verdict_results):
    """The `!payload` guard must protect the WHOLE ok:false branch: a transport
    that produced no payload at all yields the mapped fixed refusal, never a
    null dereference."""
    assert verdict_results["nullThrew"] is None, (
        f"firstEditVerdict(null) still throws: {verdict_results['nullThrew']!r}")
    refused = verdict_results["nullPayload"]
    assert refused["ok"] is False
    assert refused["message"] == (
        "the Save transport returned no verdict for this buffer")
    # The refusal branch carries NO action field at all: the route's refusals
    # carry no verb (only success does), and the Save seam's reader keeps the
    # client's own plan row for a refused buffer anyway.
    assert "action" not in refused


def test_a_refusals_own_message_still_passes_through(verdict_results):
    r = verdict_results["refusal"]
    assert r["ok"] is False
    assert r["message"] == "the base moved"
    assert "action" not in r
