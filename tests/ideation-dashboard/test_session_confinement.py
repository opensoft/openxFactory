"""IDENTITY, AUTHORITY, CONFINEMENT — the PR #49 adversarial-review repairs
(findings 2, 8, 10, 14, 16).

Five defects, one theme: something the session surface is supposed to be
CONFINED to was inferred from ambient context instead of being carried,
declared, or checked.

  * **finding 2** — FR-019's third clause ("reject and report any agent or
    automated invocation") had no runtime realization on either public surface.
    Two of the three clauses were enforced before the body parse; the third was
    discharged only by in-process object type, which neither a scripted loopback
    POST nor a `cli.main([...])` call is ever asked about. Both surfaces now
    require a HUMAN CONSOLE declaration and refuse without one.

  * **finding 8** — repository identity was ambient on all three legs: the HTTP
    body named no repository (so the server used whichever registry entry was
    ACTIVE, which the client-side selector does not move), `create-document`
    keyed its session off a DOCUMENT HEADER field while its siblings keyed off
    the checkout, and `gh` was invoked with no `--repo`, so an inherited
    `GH_REPO` chose the pull request's repository.

  * **finding 10** — a registry refresh could EVICT live sessions (`_refetch`
    rebuilds the registry from an index that structurally cannot carry a session
    ref) or leave a draft globally ACTIVE (`_regenerate` promotes what it
    touches, and the serve's refresh route skipped the caller-side guard).

  * **finding 14** — the hosted plane admitted session rows into the registry
    and projected them in `/snapshot-index.json`, and the renderer printed the
    posture line and the CLI descriptors for them.

  * **finding 16** — the workbench's OUTLINE pane fetched the unkeyed
    `/source/`, which the server resolves to the ACTIVE (main) entry, so a draft
    view's outline rendered main's bytes or 404'd.

Every test here builds its world in `tmp_path` on the `scratch_repo` harness
(a throwaway checkout with a local BARE origin). No serve is pointed at a real
tree, no `gh`/`nlm` is reachable (`tests/hermeticity.py`), and nothing here
performs a network read or write.
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

from conftest import REPO_ROOT

from session_fixtures import FakeNotebookAdapter, build_scratch_repo

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import session_git as sg
from ideation_dashboard import session_pr as spr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
RECORDS = gc.DEFAULT_RECORDS_DIR
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": f"ideation/staging/{TOPIC}/",
    "repository_context": REPO,
    "scope_kind": bs.STAGED_TOPIC,
    "scope_id": TOPIC,
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _registry(repo, tmp_path, *, name="main-snapshot.json"):
    """A registry in the shape a serve holds one: `(repository, main)`
    registered and ACTIVE, source-rooted at the served checkout. Written OUTSIDE
    the checkout so building it never moves the served tree."""
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _create_raw(repo, registry, **over):
    actor = over.pop("actor", "brett")
    return gr.run_gate_action(
        "create-document", {**CREATE_BODY, **over},
        checkout_root=repo.root, actor=actor, snapshot_path=None,
        session_registry=registry, repository=repo.repository)


@contextmanager
def _serving(repo, snapshot_path, *, host="127.0.0.1", actor="tester", **kw):
    # the notebook seam is ALWAYS a fake here (FR-043): the hermeticity shim puts
    # an `nlm` on PATH, so `available()` says yes and an un-injected serve would
    # build the real adapter
    kw.setdefault("adapter_factory", FakeNotebookAdapter)
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, host=host,
                                   actor=actor, **kw)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _served_snapshot(repo, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


def _console_headers(host, port):
    """The headers a request from the SERVED PAGE carries (finding 2): the
    per-serve human-console token, read the only way the page can read it — a
    same-origin `GET /capabilities`, which no cross-origin caller can read."""
    status, caps = _request(host, port, "GET", "/capabilities")
    assert status == 200, caps
    token = caps.get("console_token")
    assert token, caps
    return {serve_mod.CONSOLE_TOKEN_HEADER: token}


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    raw = json.dumps(body).encode("utf-8") if body is not None else None
    hdrs = dict(headers or {})
    if raw is not None:
        hdrs.setdefault("Content-Type", "application/json")
        hdrs["Content-Length"] = str(len(raw))
    conn.request(method, path, body=raw, headers=hdrs)
    response = conn.getresponse()
    payload = response.read().decode("utf-8")
    status = response.status
    conn.close()
    try:
        return status, json.loads(payload)
    except ValueError:
        return status, payload


# ==========================================================================
# FINDING 2 — FR-019's third clause has a RUNTIME realization on both surfaces
# ==========================================================================

def test_a_scripted_http_session_verb_is_refused_and_reported(scratch_repo,
                                                              tmp_path, capsys):
    """The reproduction, inverted: a bare `http.client` POST used to tear a live
    session down with `200` and a gate-action record naming the HUMAN.

    It now refuses BEFORE the body is parsed — the same place the loopback and
    actor clauses refuse — and REPORTS the reason on the server log, which is
    what "reject AND report" asks for. The wire gets one fixed sentence: nothing
    request-derived reaches a response body."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    git = sg.SessionGit(scratch_repo.root)

    with _serving(scratch_repo, snapshot) as (host, port):
        status, payload = _request(host, port, "POST",
                                   "/actions/gate/create-document",
                                   body=CREATE_BODY)

    assert (status, payload["error"]) == (403, "agent_invocation"), payload
    assert payload["message"] == serve_mod.AGENT_INVOCATION_REFUSAL
    assert not git.branch_exists(DRAFT)
    assert not list((scratch_repo.root / RECORDS).rglob("*.gate-action.yaml"))
    assert "agent_invocation refused (create-document)" in capsys.readouterr().err


def test_a_cross_origin_simple_request_cannot_end_a_session(scratch_repo,
                                                            tmp_path):
    """The strongest arm of the reproduction, and the one a human could not have
    prevented: a CSRF-shaped SIMPLE request — `Content-Type: text/plain`,
    `Origin: https://evil.example`, no preflight — tore a live session down with
    `200`. Any page open in the engineer's browser could drive session verbs on
    the loopback plane.

    Two independent reasons it now refuses (a simple request may set neither a
    JSON content type nor a custom header), so removing either one still leaves
    the class closed."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    registry_seed = _registry(scratch_repo, tmp_path)   # a real live session
    assert _create_raw(scratch_repo, registry_seed)[0] == 200
    git = sg.SessionGit(scratch_repo.root)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    assert worktree.exists()

    with _serving(scratch_repo, snapshot) as (host, port):
        token = _console_headers(host, port)[serve_mod.CONSOLE_TOKEN_HEADER]
        # (a) the simple request: no custom header is even possible
        simple, simple_body = _request(
            host, port, "POST", "/actions/gate/abandon-session",
            body={"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                  "reason": "drive-by"},
            headers={"Content-Type": "text/plain",
                     "Origin": "https://evil.example"})
        # (b) and even WITH the token, a foreign origin is refused
        stolen, stolen_body = _request(
            host, port, "POST", "/actions/gate/abandon-session",
            body={"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                  "reason": "drive-by"},
            headers={"Origin": "https://evil.example",
                     serve_mod.CONSOLE_TOKEN_HEADER: token})

    assert (simple, simple_body["error"]) == (403, "agent_invocation")
    assert (stolen, stolen_body["error"]) == (403, "agent_invocation")
    assert worktree.exists()
    assert git.branch_exists(DRAFT)


def test_the_served_console_is_not_refused(scratch_repo, tmp_path):
    """The other half of a fail-closed check: the human's own console still
    works. A request carrying this serve's token, a JSON content type, and its
    own origin lands."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        headers = dict(_console_headers(host, port))
        headers["Origin"] = f"http://{host}:{port}"
        status, payload = _request(host, port, "POST",
                                   "/actions/gate/create-document",
                                   body=CREATE_BODY, headers=headers)

    assert status == 200, payload
    assert payload["ref"] == DRAFT


def test_the_console_token_is_per_serve_and_absent_where_sessions_are(
        scratch_repo, tmp_path):
    """The token exists only where session verbs do, and never twice. A plane
    with no session capability mints none — and a handler with no token refuses
    every session verb, which is the fail-closed direction."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        first = _console_headers(host, port)[serve_mod.CONSOLE_TOKEN_HEADER]
    with _serving(scratch_repo, snapshot) as (host, port):
        second = _console_headers(host, port)[serve_mod.CONSOLE_TOKEN_HEADER]
    assert first != second and len(first) >= 32

    # the HOSTED plane advertises no session, so it mints no console token
    with _serving(scratch_repo, snapshot, host="0.0.0.0") as (host, port):
        status, caps = _request(host, port, "GET", "/capabilities")
    assert status == 200
    assert caps["actions"]["session"] is False
    assert serve_mod.CONSOLE_TOKEN_FIELD not in caps

    assert serve_mod.CONSOLE_TOKEN_FIELD not in serve_mod._DEFAULT_CAPABILITIES
    assert serve_mod.DashboardHandler.console_token is None


def test_the_renderer_presents_the_console_token_from_the_capability_probe():
    """The page's side of the same contract: ONE header-name definition in the
    pure model, consulted by both write transports, sourced from the capability
    probe app.js already performs. No new fetch, no second definition."""
    views = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
    model = (views / "staging-workbench-model.js").read_text(encoding="utf-8")
    assert f'export const CONSOLE_TOKEN_HEADER = "{serve_mod.CONSOLE_TOKEN_HEADER}"' in model
    assert f'export const CONSOLE_TOKEN_FIELD = "{serve_mod.CONSOLE_TOKEN_FIELD}"' in model
    for name in ("swb-session.js", "swb-create.js"):
        body = (views / name).read_text(encoding="utf-8")
        assert "headers: consoleHeaders(caps)" in body, name
        # the header name itself is never a literal outside the model
        assert serve_mod.CONSOLE_TOKEN_HEADER not in body, name
        # and the transport pin is untouched: still exactly one write literal
        assert body.count('method: "POST"') == 1, name


# ==========================================================================
# A STRANDED PAGE REPAIRS ITSELF (Brett, 2026-08-09)
#
# The token is per-serve and the page reads `/capabilities` ONCE, at load, so a
# tab that outlives a restart presents the previous serve's token and every
# guarded write refuses. Brett hit it on a real create — with a title, a summary
# and a body already typed into the form.
#
# The repair is a RE-READ, never `location.reload()`: the refusal fires exactly
# when there is written work in the page, and a reload would discard it to fix a
# header. These tests pin the two halves — the WIRE property the retry rests on
# (a stale token is refused before anything happens, so re-sending is safe), and
# the RENDERER policy that acts on it.
# ==========================================================================

def test_a_stale_console_token_refuses_before_any_write_and_a_re_read_lands(
        scratch_repo, tmp_path, capsys):
    """The reproduction and its repair, at the wire.

    The FIRST serve's token is presented to the SECOND serve — exactly what an
    open tab does after a restart. It refuses `agent_invocation` and NOTHING
    happens: no branch, no worktree, no gate-action record. That is what makes
    an automatic retry legitimate rather than a way to double-write.

    Then the repair: re-read `/capabilities`, present the new token, send the
    SAME body. It lands."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    git = sg.SessionGit(scratch_repo.root)

    with _serving(scratch_repo, snapshot) as (host, port):
        stale = _console_headers(host, port)[serve_mod.CONSOLE_TOKEN_HEADER]

    # the serve restarted under the open tab
    with _serving(scratch_repo, snapshot) as (host, port):
        origin = f"http://{host}:{port}"
        refused_status, refused = _request(
            host, port, "POST", "/actions/gate/create-document",
            body=CREATE_BODY,
            headers={serve_mod.CONSOLE_TOKEN_HEADER: stale, "Origin": origin})

        # the server did nothing — the whole basis of the retry
        assert (refused_status, refused["error"]) == (403, "agent_invocation")
        assert refused["message"] == serve_mod.AGENT_INVOCATION_REFUSAL
        assert not git.branch_exists(DRAFT)
        assert not list((scratch_repo.root / RECORDS).rglob("*.gate-action.yaml"))
        assert "the console token does not match this serve's" in capsys.readouterr().err

        # THE REPAIR: re-probe, take the new token, re-send the SAME body
        fresh = dict(_console_headers(host, port))
        assert fresh[serve_mod.CONSOLE_TOKEN_HEADER] != stale
        fresh["Origin"] = origin
        landed_status, landed = _request(
            host, port, "POST", "/actions/gate/create-document",
            body=CREATE_BODY, headers=fresh)

    assert landed_status == 200, landed
    assert landed["ref"] == DRAFT
    assert git.branch_exists(DRAFT)


def test_the_renderer_repairs_a_stale_token_by_re_reading_it_never_by_reloading():
    """The renderer's side. ONE policy in the pure model, ONE re-read in the
    composition root, and both write transports routed through them.

    The load-bearing assertion is the LAST one: no module on this path may
    reach for `location.reload()`. A reload would fix the header by throwing
    away the textarea, the selection and the drafted seed — the work the
    refusal interrupted."""
    views = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
    model = (views / "staging-workbench-model.js").read_text(encoding="utf-8")

    # the retriable set is exactly the codes serve.py emits from its
    # console gate — the refusals raised BEFORE any body read or any write
    assert "export const CONSOLE_REFUSAL_CODES" in model
    assert '"agent_invocation"' in model and '"console_required"' in model
    assert serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED == "console_required"
    assert "export async function withConsoleRepair(send, repair)" in model
    # what a page that could NOT repair itself says — never the raw refusal
    assert "export const CONSOLE_STRANDED_MESSAGE" in model
    assert "reload to continue" in model
    assert serve_mod.AGENT_INVOCATION_REFUSAL not in model

    # both write transports build their header INSIDE the retried send (so the
    # second attempt presents the repaired token) and route through the policy
    for name in ("swb-session.js", "swb-create.js"):
        body = (views / name).read_text(encoding="utf-8")
        assert "withConsoleRepair(send, repair)" in body, name
        assert "const send = async () => {" in body, name
        assert "headers: consoleHeaders(caps)" in body, name

    # the re-read itself: the composition root, through the capability probe
    # app.js already performs (no new route, no new fetch call site), and it
    # MUTATES the objects the views hold by reference
    app = (views.parent / "app.js").read_text(encoding="utf-8")
    assert "export function createConsoleRepair(capsObjects, probe) {" in app
    assert "const readCapabilities = probe || probeCapabilities;" in app
    assert "caps[CONSOLE_TOKEN_FIELD] = token;" in app
    assert "createConsoleRepair([probedCaps, caps])" in app

    # THE RULING: not one of these modules reloads the page. Read on EXECUTABLE
    # lines only — the comments say `location.reload()` precisely to record why
    # it is not called.
    for label, source in (("model", model), ("app.js", app),
                          ("swb-session.js",
                           (views / "swb-session.js").read_text(encoding="utf-8")),
                          ("swb-create.js",
                           (views / "swb-create.js").read_text(encoding="utf-8")),
                          ("staging-workbench.js",
                           (views / "staging-workbench.js").read_text(encoding="utf-8"))):
        code = "\n".join(line for line in source.splitlines()
                         if not line.lstrip().startswith(("//", "*", "/*")))
        assert "location.reload" not in code, label


_REPAIR_HARNESS = r"""
import { createConsoleRepair } from './app.mjs';
import { firstEditTransport } from './views/swb-session.js';
import {
  CONSOLE_REFUSAL_CODES, CONSOLE_STRANDED_MESSAGE, consoleRefusal,
  withConsoleRepair,
} from './views/staging-workbench-model.js';

const TOKEN_HEADER = 'X-XF-Console-Token';
const REFUSED = { ok: false, error: 'agent_invocation', message: 'FR-019 …' };
const GATE_REFUSED = { ok: false, error: 'gate_refused',
                       message: 'the document already exists' };

function response(payload) {
  return { ok: payload.ok === true, status: payload.ok === true ? 200 : 403,
           async json() { return payload; } };
}

// ---- (1) the real transport + the REAL repair ------------------------------
// The page loaded against a serve that has since restarted: `probedCaps` (what
// `openDraft` creates through) and `caps` (the projection every tile-bound
// surface reads) both still carry the old token, exactly as app.js holds them.
const TYPED = '# the body the human typed\n\nnot to be thrown away.\n';
const calls = [];
const expected = 'token-new';                     // what the RESTARTED serve wants
const probedCaps = { actions: { gate: true, session: true },
                     console_token: 'token-old' };
const caps = { ...probedCaps };                   // readOnlyCaps copies, so: two objects
const fetcher = async (url, options) => {
  const presented = options.headers[TOKEN_HEADER];
  calls.push({ url, presented, body: JSON.parse(options.body) });
  return response(presented === expected
    ? { ok: true, verb: 'edit-document', ref: 'draft/demo-topic',
        commit: 'c0ffee', document: 'ideation/staging/demo-topic/draft.md',
        record: 'rec-1', content_hash: { hex: 'abc' }, session: { ref: 'x' } }
    : REFUSED);
};
let probes = 0;
const repair = createConsoleRepair([probedCaps, caps], async () => {
  probes += 1;                                    // the same-origin /capabilities GET
  return { actions: { gate: true, session: true }, console_token: expected };
});
const request = {
  key: { repository: 'openxFactory', tile_kind: 'staged', tile_id: 'demo-topic' },
  document: 'ideation/staging/demo-topic/draft.md',
  content: TYPED,
};
const verdict = await firstEditTransport({ fetcher, caps, repair })(request);

// a plane that answers with NO console token cannot be retried against
const noConsole = await createConsoleRepair(
  [{ console_token: 'x' }], async () => ({ actions: { notebook: false } }))();

// ---- (2) the policy, driven directly on its four other paths ---------------
async function policy(answers, repairAnswer) {
  const sent = [];
  const queue = [...answers];
  let repaired = 0;
  const result = await withConsoleRepair(
    async () => { sent.push(1); return queue.shift(); },
    async () => { repaired += 1; return repairAnswer; });
  return { result, sends: sent.length, repaired };
}

const landsFirstTime = await policy([{ ok: true, ref: 'r' }], true);
const noRepairPossible = await policy([REFUSED], false);
const refusedTwice = await policy([REFUSED, REFUSED], true);
const otherRefusal = await policy([GATE_REFUSED], true);
const retryHitsGate = await policy([REFUSED, GATE_REFUSED], true);
const noRepairSeam = await withConsoleRepair(async () => REFUSED, null);

console.log(JSON.stringify({
  verdict, calls, probes, noConsole,
  token: caps.console_token, probedToken: probedCaps.console_token,
  codes: CONSOLE_REFUSAL_CODES,
  stranded: CONSOLE_STRANDED_MESSAGE,
  recognises: [consoleRefusal(REFUSED),
               consoleRefusal({ ok: false, error: 'console_required' }),
               consoleRefusal(GATE_REFUSED),
               consoleRefusal({ ok: true }),
               consoleRefusal(null)],
  landsFirstTime, noRepairPossible, refusedTwice, otherRefusal, retryHitsGate,
  noRepairSeam,
}));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node not available")
def test_a_stranded_page_retries_once_and_the_drafted_body_survives(tmp_path):
    """The behavioural proof, on the REAL transport (`firstEditTransport`, the
    doxBench governed Save — `submitSession`'s heaviest caller, whose body is
    the whole editor buffer).

    Two sends, one re-probe, and the second send carries the SAME body it did
    the first time. That equality IS the requirement: nothing the human wrote
    was re-derived, re-prompted, or lost."""
    web_copy = tmp_path / "web"
    shutil.copytree(WEB, web_copy)
    (web_copy / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (web_copy / "vendor" / "package.json").write_text('{"type": "commonjs"}',
                                                      encoding="utf-8")
    # app.js ends in a top-level `await main();`, so it is imported through the
    # same strip-and-import copy test_doxbench_transport.py's harnesses use.
    original = (web_copy / "app.js").read_text(encoding="utf-8").rstrip()
    assert original.endswith("await main();"), "harness precondition failed"
    (web_copy / "app.mjs").write_text(
        original[: -len("await main();")].rstrip() + "\n", encoding="utf-8")
    harness = web_copy / "repair-harness.mjs"
    harness.write_text(_REPAIR_HARNESS, encoding="utf-8")
    proc = subprocess.run([shutil.which("node"), str(harness)],
                          capture_output=True, text=True, timeout=60, cwd=web_copy)
    assert proc.returncode == 0, proc.stderr
    r = json.loads(proc.stdout)

    # (1) the recovery, on the real transport
    assert r["verdict"]["ok"] is True, r["verdict"]
    assert r["verdict"]["ref"] == "draft/demo-topic"
    assert r["probes"] == 1, "exactly one re-probe, never a poll"
    assert len(r["calls"]) == 2, r["calls"]
    assert r["calls"][0]["presented"] == "token-old"
    assert r["calls"][1]["presented"] == "token-new"
    # the repair wrote through to BOTH capability objects the shell holds — the
    # probe (what `openDraft` creates through) and its read-only projection
    assert r["token"] == r["probedToken"] == "token-new"
    # a plane that answers with no console token is not retried against
    assert r["noConsole"] is False
    # THE POINT: the retry re-sends what the human wrote, byte for byte
    assert r["calls"][0]["body"] == r["calls"][1]["body"]
    assert r["calls"][0]["body"]["content"].startswith("# the body the human typed")
    assert r["calls"][0]["url"] == r["calls"][1]["url"] == "/actions/gate/first-edit"

    # the retriable set, and what it does and does not recognise
    assert r["codes"] == ["agent_invocation", "console_required"]
    assert r["recognises"] == [True, True, False, False, False]

    # a landed action never re-probes and never sends twice
    assert r["landsFirstTime"] == {"result": {"ok": True, "ref": "r"},
                                   "sends": 1, "repaired": 0}

    # a plane that could not hand back a console token is not retried against:
    # no second send, and the human is told plainly rather than shown FR-019's
    # four clauses
    assert r["noRepairPossible"]["sends"] == 1
    assert r["noRepairPossible"]["result"] == {
        "ok": False, "error": "console_stranded", "message": r["stranded"]}
    assert r["stranded"] == (
        "this page was loaded against an earlier serve — reload to continue")

    # refused twice: exactly two sends — never a third, never a loop
    assert r["refusedTwice"]["sends"] == 2
    assert r["refusedTwice"]["result"]["error"] == "console_stranded"

    # a refusal that is NOT a console refusal is the engine's own answer and
    # reaches the human verbatim, with no re-probe behind it
    assert r["otherRefusal"] == {"result": {"ok": False, "error": "gate_refused",
                                            "message": "the document already exists"},
                                 "sends": 1, "repaired": 0}
    # …and so does one the RETRY runs into: the repair worked, the action did not
    assert r["retryHitsGate"]["sends"] == 2
    assert r["retryHitsGate"]["result"]["error"] == "gate_refused"

    # with no repair seam injected at all, the page fails closed and says so
    assert r["noRepairSeam"]["error"] == "console_stranded"


def test_the_session_rekey_asks_the_serve_which_repository_a_session_lives_in(
        scratch_repo, tmp_path):
    """MEASURED, 2026-08-10, on the multi-repository local plane. A create from
    a PROJECT view landed — `200`, branch `draft/company-provisioning-…`
    opened, the session snapshot generated — and the page then asked for

        GET /snapshot.json?repository=xfactory&ref=draft/company-provisioning-…
        -> 404 no such snapshot

    because `xfactory` is a PROJECT id, not a repository. The session opened and
    its document view never did; the human read `the session opened, but its
    document view could not be loaded`.

    The create itself already follows the ruling — lens.js hands the create the
    SERVE'S writable repository, never the composed view's `repository`, which
    is the project id. The RE-KEY that follows the create did not: it read the
    view's own key, and under a composed view `sourceKeyFor(null)` is null, so
    it fell through to the project id.

    Two halves, both pinned here: the WIRE fact that makes inference wrong (a
    session ref is a row under the repository that owns it and under no other
    name), and the renderer asking `/capabilities` — which declares the
    repository this serve writes to — before any view-derived fallback."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    registry_seed = _registry(scratch_repo, tmp_path)
    assert _create_raw(scratch_repo, registry_seed)[0] == 200

    with _serving(scratch_repo, snapshot) as (host, port):
        _s, caps = _request(host, port, "GET", "/capabilities")
        _s, index = _request(host, port, "GET", "/snapshot-index.json")
        rows = {(e["repository"], e["ref"]) for e in index["entries"]}
        # the session is an ordinary row under the SERVE'S repository (FR-014)
        assert (scratch_repo.repository, DRAFT) in rows, rows
        assert caps["repository"] == scratch_repo.repository
        # …and that is the ONLY name it answers to: any other id at the same
        # ref is `no such snapshot`, which is exactly what a project id got
        own, _ = _request(
            host, port, "GET",
            f"/snapshot.json?repository={scratch_repo.repository}&ref={DRAFT}")
        inferred, _ = _request(
            host, port, "GET",
            f"/snapshot.json?repository=a-project-id&ref={DRAFT}")

    assert own == 200
    assert inferred == 404, (
        "a name that is not the owning repository must not resolve a session "
        "snapshot — which is why the browser may not infer one")

    app = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "app.js"
           ).read_text(encoding="utf-8")
    rekey = app.split("const rekeyToSession = async (ref) => {", 1)[1].split(
        "\n    };", 1)[0]
    code = "\n".join(line for line in rekey.splitlines()
                     if not line.lstrip().startswith("//"))
    assert "probedCaps?.repository" in code, (
        "the re-key must ask the serve which repository it writes to")
    assert code.index("probedCaps?.repository") \
        < code.index("workbenchSourceKey?.repository") \
        < code.index("active?.repository"), (
            "the serve's declaration comes FIRST — the view-derived fallbacks "
            "resolve to the project id on a composed view")
    # the UNSTRIPPED probe, never the composed projection: `readOnlyCaps` copies
    # the probe's read-only facts, but this must not depend on which one a
    # render produced
    assert "caps?.repository" not in code


def test_a_scripted_cli_session_verb_is_refused_on_every_verb(
        scratch_repo, tmp_path, monkeypatch, capsys, fake_cli_notebook):
    """The CLI half of the reproduction: `cli.main(["gate", "abandon-session",
    "--actor", "codex-agent-bot", …])` returned 0 and tore the session down,
    with the record naming the bot. `--actor` is free text, so nothing about the
    invocation was ever asked whether it was a human.

    The declaration is withheld here (`monkeypatch.delenv`, undoing the suite's
    `declared_human_console`) and stdin is not a terminal, which is exactly the
    shape of an agent or CI invocation. Every session subcommand refuses, and
    none of them persists anything."""
    monkeypatch.delenv(cli_mod.HUMAN_CONSOLE_ENV, raising=False)
    assert cli_mod.human_console_present() is False
    content = tmp_path / "body.md"
    content.write_text("# x\n", encoding="utf-8")
    common = ["--repo-root", str(scratch_repo.root), "--actor", "codex-agent-bot",
              "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC]
    invocations = {
        "create-document": ["--title", "T", "--summary", "S", "--topics", "a",
                            "--repository-context", REPO],
        "edit-document": ["--document", "x.md", "--content-file", str(content)],
        "open-pr": [],
        "abandon-session": ["--reason", "scripted"],
        "cleanup-abandoned-branch": ["--ref", DRAFT],
    }
    before = scratch_repo.served_fingerprint()

    for verb, extra in invocations.items():
        code = cli_mod.main(["gate", verb, *common, *extra])
        err = capsys.readouterr().err
        assert code == 1, verb
        assert "human-only (FR-019)" in err, verb
        assert cli_mod.HUMAN_CONSOLE_ENV in err, verb

    assert not sg.SessionGit(scratch_repo.root).branch_exists(DRAFT)
    assert scratch_repo.served_fingerprint() == before
    assert fake_cli_notebook.calls == []


def test_an_interactive_terminal_is_a_human_console(monkeypatch):
    """The positive derivation, both ways: a terminal IS the declaration, and an
    explicit declaration stands in for one in a non-interactive human shell."""
    class _Tty:
        @staticmethod
        def isatty():
            return True

    monkeypatch.delenv(cli_mod.HUMAN_CONSOLE_ENV, raising=False)
    monkeypatch.setattr(cli_mod.sys, "stdin", _Tty)
    assert cli_mod.human_console_present() is True

    class _Pipe:
        @staticmethod
        def isatty():
            return False

    monkeypatch.setattr(cli_mod.sys, "stdin", _Pipe)
    assert cli_mod.human_console_present() is False
    for declared in ("1", "true", "YES", "on"):
        monkeypatch.setenv(cli_mod.HUMAN_CONSOLE_ENV, declared)
        assert cli_mod.human_console_present() is True, declared
    monkeypatch.setenv(cli_mod.HUMAN_CONSOLE_ENV, "0")
    assert cli_mod.human_console_present() is False


def test_the_two_older_fr019_clauses_still_refuse_first(scratch_repo, tmp_path,
                                                        monkeypatch):
    """The new clause is THIRD, deliberately: an off-loopback bind still answers
    `loopback_only` and an unresolved actor still answers `action_unavailable`,
    both before any body parse, so the refusals their own tests pin are
    unchanged."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot, host="0.0.0.0") as (host, port):
        hosted, hosted_body = _request(host, port, "POST",
                                       "/actions/gate/abandon-session",
                                       body={"scope_id": TOPIC})
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *_a, **_k: None)
    with _serving(scratch_repo, snapshot, actor=None) as (host, port):
        no_actor, no_actor_body = _request(host, port, "POST",
                                           "/actions/gate/abandon-session",
                                           body={"scope_id": TOPIC})

    assert (hosted, hosted_body["error"]) == (403, "loopback_only")
    assert (no_actor, no_actor_body["error"]) == (403, "action_unavailable")


# ==========================================================================
# FINDING 8 — the repository is CARRIED, not inferred
# ==========================================================================

def test_a_session_action_naming_another_repository_is_refused(scratch_repo,
                                                               tmp_path):
    """Leg (a): the selected repository and the written repository were allowed
    to differ, silently.

    Reproduced during the adjudication on a two-repository local plane: the page
    was reading repoB (`GET /snapshot.json?repository=repoB`, which resolves
    WITHOUT moving `registry.active`), and its `create-document` opened a branch,
    a worktree, a document and a registry row in repoA — keyed to repoA, and
    therefore invisible to the page that created it. The route had no repository
    input at all, so there was nothing to disagree with.

    The body now carries the repository the page is reading, and a value this
    surface cannot honour REFUSES. Fail-closed: nothing is persisted, and the
    refusal names only the served repository."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    before = scratch_repo.served_fingerprint()

    status, payload = _create_raw(scratch_repo, registry, repository="MedxFactory")

    assert status == 409, payload
    assert payload["error"] == "repository_mismatch"
    assert "MedxFactory" not in json.dumps(payload)      # request data stays off the wire
    assert REPO in payload["message"]
    assert not git.branch_exists(DRAFT)
    assert not bs.worktree_path(scratch_repo.root, DRAFT).exists()
    assert registry.get(REPO, DRAFT) is None
    assert scratch_repo.served_fingerprint() == before


def test_every_session_verb_refuses_a_foreign_repository(scratch_repo, tmp_path):
    """The confinement is the DISPATCH's, not one verb's: every verb that can
    open, write into, or end a session is covered by the same check, so a later
    verb cannot be added outside it."""
    registry = _registry(scratch_repo, tmp_path)
    bodies = {
        "create-document": CREATE_BODY,
        "edit-document": {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                          "document": "x.md", "content": "y"},
        "open-pr": {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC},
        "abandon-session": {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                            "reason": "no"},
        "cleanup-abandoned-branch": {"scope_kind": bs.STAGED_TOPIC,
                                     "scope_id": TOPIC, "ref": DRAFT},
        # T080 (2026-07-30): the first-Save verb joins the sweep the moment it
        # joins SESSION_BEARING_VERBS -- exactly the tripwire this test declares.
        "first-edit": {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                       "document": "x.md", "content": "y"},
    }
    assert set(bodies) == set(gr.SESSION_BEARING_VERBS)

    for verb, body in bodies.items():
        status, payload = gr.run_gate_action(
            verb, {**body, "repository": "MedxFactory"},
            checkout_root=scratch_repo.root, actor="brett", snapshot_path=None,
            session_registry=registry, repository=scratch_repo.repository)
        assert (status, payload["error"]) == (409, "repository_mismatch"), verb


def test_a_session_action_naming_the_served_repository_is_untouched(scratch_repo,
                                                                    tmp_path):
    """The check is a CONFINEMENT, not a blanket required field: the value the page
    actually sends is the served repository, and a body that names none at all
    behaves exactly as before ON A PLANE THAT REACHES ONE REPOSITORY — which is
    every CLI-parity call site and every single-repository serve. Where more than
    one is reachable the field is required; see
    `test_a_body_that_names_no_repository_refuses_when_more_than_one_is_reachable`."""
    registry = _registry(scratch_repo, tmp_path)

    status, payload = _create_raw(scratch_repo, registry, repository=REPO)

    assert status == 200, payload
    assert payload["ref"] == DRAFT


# ---- leg (a), wave 2: a body that names NOTHING ------------------------------

def _two_repository_plane(tmp_path):
    """The review's own two-repository local plane: repoA SERVED and active, repoB
    reachable through the client-side selector, per-entry `source_root`s."""
    a = build_scratch_repo(tmp_path / "a", repository="repoA", topic_id="a-topic")
    b = build_scratch_repo(tmp_path / "b", repository="repoB",
                           topic_id="b-only-topic")
    registry = reg.SnapshotRegistry()
    for repo, active in ((a, True), (b, False)):
        path = tmp_path / f"{repo.repository}.json"
        path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                        encoding="utf-8")
        registry.register(reg.entry_from_snapshot_file(
            path, repository=repo.repository, ref=reg.DEFAULT_REF,
            source_root=repo.root), active=active)
    return a, b, registry


B_ONLY_BODY = {
    "title": "B Only Draft", "summary": "The repoB page's document.",
    "topics": ["alpha"], "area": "ideation/brainstorm/",
    "repository_context": "repoB",
    "scope_kind": bs.STAGED_TOPIC, "scope_id": "b-only-topic",
}


def test_a_body_that_names_no_repository_refuses_when_more_than_one_is_reachable(
        tmp_path):
    """The review's ORIGINAL reproduction, which wave 1 left succeeding: the body
    carries no `repository` key at all, so the server substituted its own active
    entry and created the branch, the worktree, the document and the registry row
    in repoA for a tile that exists only in repoB (re-reproduced by the wave-2
    replay pass, byte for byte).

    The field is REQUIRED-OR-DERIVED now. Here it cannot be derived — two
    repositories are reachable and the server has no way to know which one the
    page was reading — so the action refuses and persists nothing."""
    a, b, registry = _two_repository_plane(tmp_path)
    branch = "draft/b-only-topic"

    status, payload = gr.run_gate_action(
        "create-document", dict(B_ONLY_BODY), checkout_root=a.root, actor="brett",
        snapshot_path=None, session_registry=registry, repository="repoA",
        tile_inventory=gr.discover_tile_inventory(b.root))

    assert (status, payload["error"]) == (409, "repository_unresolved"), payload
    assert "repoA" in payload["message"] and "repoB" in payload["message"]
    assert not sg.SessionGit(a.root).branch_exists(branch)
    assert not bs.worktree_path(a.root, branch).exists()
    assert not sg.SessionGit(b.root).branch_exists(branch)
    assert registry.keys() == [("repoA", "main"), ("repoB", "main")]
    assert not (a.root / "ideation" / "brainstorm" / "b-only-draft.md").exists()


def test_every_session_verb_refuses_a_repository_it_cannot_establish(tmp_path):
    """Like the foreign-repository sweep, the unresolved case is the DISPATCH's:
    no verb that opens, writes into, or ends a session can be reached with an
    ambient repository."""
    a, _b, registry = _two_repository_plane(tmp_path)
    bodies = {
        "create-document": B_ONLY_BODY,
        "edit-document": {"scope_kind": bs.STAGED_TOPIC,
                          "scope_id": "b-only-topic",
                          "document": "x.md", "content": "y"},
        "open-pr": {"scope_kind": bs.STAGED_TOPIC, "scope_id": "b-only-topic"},
        "abandon-session": {"scope_kind": bs.STAGED_TOPIC,
                            "scope_id": "b-only-topic", "reason": "no"},
        "cleanup-abandoned-branch": {"scope_kind": bs.STAGED_TOPIC,
                                     "scope_id": "b-only-topic",
                                     "ref": "draft/b-only-topic"},
        # T080 (2026-07-30): same tripwire, unresolved-repository leg.
        "first-edit": {"scope_kind": bs.STAGED_TOPIC,
                       "scope_id": "b-only-topic",
                       "document": "x.md", "content": "y"},
    }
    assert set(bodies) == set(gr.SESSION_BEARING_VERBS)

    for verb, body in bodies.items():
        status, payload = gr.run_gate_action(
            verb, dict(body), checkout_root=a.root, actor="brett",
            snapshot_path=None, session_registry=registry, repository="repoA")
        assert (status, payload["error"]) == (409, "repository_unresolved"), verb


def test_the_repository_it_names_is_still_honoured_on_a_multi_repository_plane(
        tmp_path):
    """The refusal is about an ABSENT identity, not about there being two
    repositories: the served repository, NAMED, still works, and repoB's name is
    still refused as foreign. So the fix closes a hole without closing the
    surface."""
    a, _b, registry = _two_repository_plane(tmp_path)
    body = {**B_ONLY_BODY, "scope_id": "a-topic", "repository_context": "repoA"}

    ok_status, ok_payload = gr.run_gate_action(
        "create-document", {**body, "repository": "repoA"}, checkout_root=a.root,
        actor="brett", snapshot_path=None, session_registry=registry,
        repository="repoA", tile_inventory=gr.discover_tile_inventory(a.root))
    foreign, foreign_payload = gr.run_gate_action(
        "create-document", {**body, "repository": "repoB"}, checkout_root=a.root,
        actor="brett", snapshot_path=None, session_registry=registry,
        repository="repoA", tile_inventory=gr.discover_tile_inventory(a.root))

    assert ok_status == 200, ok_payload
    assert ok_payload["ref"] == "draft/a-topic"
    assert (foreign, foreign_payload["error"]) == (409, "repository_mismatch")


def test_the_reachable_roster_comes_from_the_registry_and_tolerates_absence():
    """`reachable_repositories` feeds a refusal, so a registry it cannot read must
    contribute nothing rather than guess: no registry, and a double whose
    `entries()` raises, both name zero repositories (which keeps the pre-existing
    single-repository behaviour)."""
    class _Broken:
        def entries(self):
            raise RuntimeError("unreadable roster")

    assert gr.reachable_repositories(None) == ()
    assert gr.reachable_repositories(object()) == ()
    assert gr.reachable_repositories(_Broken()) == ()

    registry = reg.SnapshotRegistry()
    registry.register(reg.SnapshotEntry(repository="repoB", ref="main"))
    registry.register(reg.SnapshotEntry(repository="repoA", ref="main"))
    registry.register(reg.SnapshotEntry(repository="repoA", ref=DRAFT))
    assert gr.reachable_repositories(registry) == ("repoA", "repoB")


def test_a_named_repository_with_nothing_to_compare_against_refuses(scratch_repo):
    """Fail-closed in the other direction too: "cannot verify" is not
    "matches"."""
    status, payload = gr.run_gate_action(
        "create-document", {**CREATE_BODY, "repository": REPO},
        checkout_root=scratch_repo.root, actor="brett", snapshot_path=None,
        session_registry=None, repository=None)

    assert (status, payload["error"]) == (409, "repository_mismatch")


def test_the_http_route_refuses_a_create_for_another_repository(scratch_repo,
                                                                tmp_path):
    """The same refusal over the REAL serve handler, which is the surface the
    repository selector talks to."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    git = sg.SessionGit(scratch_repo.root)

    with _serving(scratch_repo, snapshot) as (host, port):
        status, payload = _request(
            host, port, "POST", "/actions/gate/create-document",
            body={**CREATE_BODY, "repository": "MedxFactory"},
            headers=_console_headers(host, port))

    assert (status, payload["error"]) == (409, "repository_mismatch"), payload
    assert not git.branch_exists(DRAFT)


# ---- leg (c): `gh` is pinned to the repository `git push` writes to ----------

class RecordingRunner:
    """An injected command runner: the real `gh`/`git push` are never invoked."""

    def __init__(self, replies=None, fail=None) -> None:
        self.commands: list[tuple[str, ...]] = []
        self.replies = dict(replies or {})
        self.fail = dict(fail or {})

    def run(self, *args, cwd=None):
        self.commands.append(tuple(args))
        key = " ".join(args[:3])
        code, err = self.fail.get(key, (0, ""))
        return subprocess.CompletedProcess(list(args), code,
                                           self.replies.get(key, ""), err)


GH_ORIGIN = "https://github.com/opensoft/openxFactory.git"


@pytest.mark.parametrize("url,expected", [
    ("https://github.com/opensoft/openxFactory.git", "opensoft/openxFactory"),
    ("https://github.com/opensoft/openxFactory", "opensoft/openxFactory"),
    ("git@github.com:opensoft/openxFactory.git", "opensoft/openxFactory"),
    ("ssh://git@github.com/opensoft/openxFactory.git", "opensoft/openxFactory"),
    ("https://ghe.example.com/opensoft/openxFactory.git",
     "ghe.example.com/opensoft/openxFactory"),
    # a local bare remote is NOT a hosted repository — no guess is made
    ("/tmp/scratch/origin.git", None),
    ("../origin.git", None),
    ("file:///tmp/scratch/origin.git", None),
    ("", None),
])
def test_the_repository_pin_is_read_from_the_origin_url(url, expected):
    assert spr.parse_repo_pin(url) == expected


def test_every_gh_invocation_names_the_repository_git_pushes_to(scratch_repo):
    """Leg (c): `gh` resolves `GH_REPO` AHEAD of the checkout's remotes, so a
    shell exporting `GH_REPO=opensoft/MedxFactory` made the branch land in this
    checkout's origin while `gh pr list/create/edit` — and the URL reported to
    the human — targeted a DIFFERENT repository (reproduced).

    The target is now named explicitly on every `gh` invocation, derived from the
    same remote `git push` writes to, so the ambient variable cannot choose it."""
    runner = RecordingRunner(replies={
        "git remote get-url": GH_ORIGIN,
        "gh pr list": "[]",
        "gh pr create": "https://github.com/opensoft/openxFactory/pull/7\n",
    })
    adapter = spr.GhPullRequests(scratch_repo.root, runner=runner)

    adapter.push(DRAFT)
    adapter.open_or_update(DRAFT, base="main", title="T", body="B")

    gh_calls = [c for c in runner.commands if c[0] == "gh"]
    assert gh_calls, runner.commands
    for command in gh_calls:
        assert "--repo" in command, command
        assert command[command.index("--repo") + 1] == "opensoft/openxFactory"
    # the remote is read ONCE, however many `gh` commands run
    assert sum(1 for c in runner.commands if c[:3] == ("git", "remote", "get-url")) == 1


def test_an_existing_pull_request_is_edited_in_the_pinned_repository(scratch_repo):
    """The `pr edit` / `pr list` path is the dangerous one — it MUTATES a pull
    request that already exists — so it carries the pin too."""
    runner = RecordingRunner(replies={
        "git remote get-url": GH_ORIGIN,
        "gh pr list": json.dumps([{"number": 12, "url": "https://x/12",
                                   "state": "OPEN"}]),
    })
    adapter = spr.GhPullRequests(scratch_repo.root, runner=runner)

    adapter.open_or_update(DRAFT, base="main", title="T2", body="B2")

    edit = [c for c in runner.commands if c[:3] == ("gh", "pr", "edit")]
    assert edit and edit[0][3:5] == ("--repo", "opensoft/openxFactory"), edit


def test_an_unhosted_origin_yields_no_pin_and_no_guess(scratch_repo):
    """A local bare `origin` (what every test uses, and what a detached clone
    has) names no hosted repository. The adapter does not invent one: `gh` then
    resolves from THIS checkout's remotes, which is the same repository, and the
    redirecting variables have already been removed from its environment."""
    runner = RecordingRunner(replies={"git remote get-url": str(scratch_repo.origin),
                                      "gh pr list": "[]"})
    adapter = spr.GhPullRequests(scratch_repo.root, runner=runner)

    adapter.find_open(DRAFT)

    assert adapter.repo_pin() is None
    assert ("gh", "pr", "list", "--head", DRAFT, "--state", "open",
            "--json", "number,url,state", "--limit", "1") in runner.commands


def test_the_child_environment_drops_the_ambient_repository_redirects():
    """The second half of leg (c): `GH_REPO` / `GH_HOST` choose WHICH repository
    and host a `gh` command targets. They are removed from the child's
    environment; everything else — the whole of the engineer's ambient
    authentication (FR-034, D22) — is inherited untouched."""
    base = {"PATH": "/usr/bin", "GH_REPO": "opensoft/MedxFactory",
            "GH_HOST": "ghe.example.com", "GH_CONFIG_DIR": "/home/brett/.config/gh",
            "HOME": "/home/brett"}

    env = spr.child_env(base)

    assert set(spr.AMBIENT_TARGET_OVERRIDES) == {"GH_REPO", "GH_HOST"}
    assert "GH_REPO" not in env and "GH_HOST" not in env
    assert env["GH_CONFIG_DIR"] == "/home/brett/.config/gh"
    assert env["PATH"] == "/usr/bin" and env["HOME"] == "/home/brett"
    assert base["GH_REPO"] == "opensoft/MedxFactory"      # the caller's own env is not mutated
    # and the production runner is the thing that applies it
    source = Path(spr.__file__).read_text(encoding="utf-8")
    assert "env=child_env()" in source


# ---- leg (b): the create keys its session the way its siblings do ------------

def test_create_document_keys_the_session_off_the_repository_not_the_header(
        scratch_repo, tmp_path, fake_cli_notebook, capsys):
    """Leg (b): `create-document` was the ONE session verb with no
    `--repository`, and it used `--repository-context` — a DOCUMENT HEADER field
    — as the registry and notebook key. A create with `--repository-context
    "openxFactory ideation"` therefore named its notebook
    `xf-session-openxfactory ideation-demo-topic` while the abandon that ended
    the same session looked for `xf-session-openxfactory-demo-topic`, found
    nothing, and reported "torn down: … notebook" over a notebook that survived
    (reproduced, orphaned notebook and all).

    One derivation now: `--repository`, else the checkout directory's name — the
    same `<repo>` beside `<repo>-worktrees/` convention every sibling uses."""
    content = tmp_path / "body.md"
    content.write_text("# x\n", encoding="utf-8")

    code = cli_mod.main([
        "gate", "create-document", "--repo-root", str(scratch_repo.root),
        "--actor", "brett", "--title", "First Draft",
        "--summary", "The session's first document.", "--topics", "alpha",
        "--area", f"ideation/staging/{TOPIC}/",
        "--repository-context", "openxFactory ideation",
        "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC])
    assert code == 0, capsys.readouterr()

    expected = bs.notebook_alias(scratch_repo.root.name, DRAFT)
    assert fake_cli_notebook.live_aliases() == (expected,)

    code = cli_mod.main([
        "gate", "abandon-session", "--repo-root", str(scratch_repo.root),
        "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
        "--reason", "the spike answered its question"])
    assert code == 0, capsys.readouterr()

    # the ending retired the notebook the OPEN created — no orphan, and the
    # report is honest
    assert fake_cli_notebook.live_aliases() == ()
    assert ("retire", expected) in fake_cli_notebook.calls


def test_create_document_offers_the_same_repository_flag_as_its_siblings():
    """contracts/cli.md and the runbook both say `--repository` is available on
    every session verb. It was available on four of five."""
    parser = cli_mod.build_parser()
    flags = {}
    for verb in ("create-document", "edit-document", "open-pr",
                 "abandon-session", "cleanup-abandoned-branch"):
        actions = _subparser(parser, "gate", verb)._actions
        flags[verb] = {opt for action in actions for opt in action.option_strings}
    for verb, options in flags.items():
        assert "--repository" in options, verb


def _subparser(parser, *path):
    node = parser
    for name in path:
        choices = None
        for action in node._actions:
            if getattr(action, "choices", None) and name in action.choices:
                choices = action.choices
                break
        assert choices is not None, name
        node = choices[name]
    return node


# ---- leg (a), wave 3: the key's repository half is BOUND, not re-read --------
#
# Second-review finding R2-11. Wave 1 and wave 2 both left `serve.py` deriving the
# session key's repository half from `registry.active` PER REQUEST — and `active`
# is what the human moves. One legitimate refresh of ANOTHER repository on a
# `--local-index` plane therefore re-keyed every session verb: `edit-document`
# 409'd `repository_mismatch` naming a repository the served checkout is not, and
# `propose` — deliberately outside `refuse_foreign_repository`, because it is a
# main-resident verb — walked straight over the live session it should refuse
# (FR-023, D15). The repository half of a session key is a fact about the SERVED
# CHECKOUT, so it is resolved once per process and handed to every dispatch.

def _local_index_plane(tmp_path):
    """A real two-repository LOCAL-INDEX plane (`--local-index`, a shipped flag):
    repoA is the SERVED checkout, repoB is reachable through the selector, and each
    entry declares its own `source_root`."""
    a = build_scratch_repo(tmp_path / "a", repository="repoA", topic_id="a-topic")
    b = build_scratch_repo(tmp_path / "b", repository="repoB", topic_id="b-topic")
    published = tmp_path / "local-index"
    published.mkdir()
    entries = []
    for repo in (a, b):
        path = published / f"{repo.repository}-snapshot.json"
        path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                        encoding="utf-8")
        entry = reg.entry_from_snapshot_file(path, repository=repo.repository)
        entry.location = path.name
        entries.append(entry)
    index = published / reg.DEFAULT_INDEX_NAME
    index.write_text(json.dumps(reg.build_index(entries, published=True)),
                     encoding="utf-8")
    return a, b, index, published / f"{a.repository}-snapshot.json"


def test_a_refresh_of_another_repository_does_not_re_key_the_session(tmp_path):
    """R2-11, over the REAL serve, in the exact order the human performs it:
    a live session on repoA, one `POST /actions/refresh` for repoB (which promotes
    repoB@main to ACTIVE, as `_regenerate` legitimately does for a publishable
    ref), and then the two verbs that used to be re-keyed by it.

    Both must behave as if the refresh had not happened, because it changed
    nothing about which checkout is served: `edit-document` naming repoA is
    honoured, and `propose` on the tile still REFUSES over the live session."""
    a, b, index, snapshot = _local_index_plane(tmp_path)
    branch = "draft/a-topic"
    opened = bs.open_session(
        sg.SessionGit(a.root), reg.SnapshotRegistry(), repository=a.repository,
        tile=bs.Tile(bs.STAGED_TOPIC, "a-topic"), checkout_root=a.root)
    assert Path(opened.worktree).is_dir()

    with _serving(a, snapshot, local_index=index,
                  source_roots={"repoA": a.root, "repoB": b.root}
                  ) as (host, port):
        headers = _console_headers(host, port)
        # the bootstrap re-derived the session for this process (FR-008)
        _s, before = _request(host, port, "GET", "/snapshot-index.json")
        assert (a.repository, branch) in {(e["repository"], e["ref"])
                                          for e in before["entries"]}
        refreshed, refresh_payload = _request(
            host, port, "POST", "/actions/refresh",
            body={"repository": "repoB", "ref": reg.DEFAULT_REF})
        _s, after = _request(host, port, "GET", "/snapshot-index.json")
        edited, edit_payload = _request(
            host, port, "POST", "/actions/gate/edit-document", headers=headers,
            body={"scope_kind": bs.STAGED_TOPIC, "scope_id": "a-topic",
                  "repository": "repoA",
                  "document": "ideation/staging/a-topic/README.md",
                  "content": "# A Topic\n\nrewritten inside the session.\n"})
        proposed, propose_payload = _request(
            host, port, "POST", "/actions/gate/propose", headers=headers,
            body={"topic_id": "a-topic"})

    assert refreshed == 200, refresh_payload
    # the refresh really did move the ACTIVE entry — the precondition of the defect
    assert after["active"] == {"repository": "repoB", "ref": reg.DEFAULT_REF}

    assert edited == 200, edit_payload
    assert edit_payload["ref"] == branch
    assert edit_payload["record"].startswith(RECORDS)

    assert proposed == 409, propose_payload
    assert propose_payload["error"] == "gate_refused"
    assert branch in propose_payload["message"]
    assert "LIVE" in propose_payload["message"]
    # and nothing was commissioned: FR-023's refusal persists no job
    assert list((a.root / "ideation" / "dashboard" / "jobs").glob("*")) == [] \
        if (a.root / "ideation" / "dashboard" / "jobs").is_dir() else True


def test_the_session_repository_is_resolved_once_per_process(tmp_path):
    """The mechanism, asserted directly: the value handed to every dispatch is the
    SERVED checkout's own repository (what `_bootstrap_session_entries` registered
    the live sessions under), bound onto the handler class at build time — so no
    request can read a different one, whatever the human selects."""
    a, b, index, snapshot = _local_index_plane(tmp_path)
    httpd = serve_mod.build_server(WEB, snapshot, a.root,
                                   repository=a.repository, actor="tester",
                                   local_index=index,
                                   source_roots={"repoA": a.root, "repoB": b.root},
                                   adapter_factory=FakeNotebookAdapter)
    try:
        # `RequestHandlerClass` is the `functools.partial` that binds the web dir;
        # `.func` is the class `build_server` stamped its declarations onto
        handler = object.__new__(httpd.RequestHandlerClass.func)
        assert handler.session_repository == "repoA"
        assert handler._session_repository() == "repoA"
        source = handler.source
        source.refresh(repository="repoB", ref=reg.DEFAULT_REF)
        assert source.registry.active.repository == "repoB"    # the human moved it
        assert handler._session_repository() == "repoA"         # the key did not
    finally:
        httpd.server_close()


# ==========================================================================
# FINDING 10 — a refresh never ends a session, and never promotes a draft
# ==========================================================================

def _published_tree(root: Path, repository: str, snapshot: dict,
                    index_name: str = reg.DEFAULT_INDEX_NAME) -> Path:
    """A published data source (the SERVED plane's binding): one snapshot plus
    the index that names it. Session refs can never appear here — the index
    refuses to publish a non-`main` entry — which is exactly why a rebuild from
    it used to destroy them."""
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{repository}-snapshot.json"
    path.write_text(json.dumps(snapshot), encoding="utf-8")
    entry = reg.entry_from_snapshot_file(path, repository=repository)
    entry.location = path.name
    (root / index_name).write_text(
        json.dumps(reg.build_index([entry], published=True)), encoding="utf-8")
    return root


def test_a_refetch_over_a_live_session_leaves_the_session_live(scratch_repo,
                                                               tmp_path):
    """Finding 10a: `_refetch` REPLACES the registry with one rebuilt from the
    published index — and a session ref is structurally unpublishable AS AN ENTRY
    (the qualification matters: wave 2 found `aggregates[].members` publishing one,
    which is finding 14's second field), so every live session was destroyed by a
    refresh of `main`.

    Liveness IS the registry entry (FR-008), so the human's session was over as
    far as the process was concerned: `edit-document` and `open-pr` both 409'd
    until the serve restarted, over a worktree and a branch that were still
    sitting there. Refreshing derived data is a READ."""
    snapshot = generate_snapshot(scratch_repo.root, scratch_repo.repository)
    published = _published_tree(tmp_path / "published", REPO, snapshot)
    source = reg.SnapshotSource(
        baked_snapshot=None, repository=REPO, checkout_root=scratch_repo.root,
        data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    assert source.refresh_binding == reg.BINDING_REFETCH
    # a live session, registered exactly as `open_session` registers one
    session_entry = reg.SnapshotEntry(repository=REPO, ref=DRAFT,
                                      source_root=scratch_repo.root)
    session_entry.payload = json.dumps(snapshot).encode("utf-8")
    bs._register_without_stealing_active(source.registry, session_entry)
    assert bs.is_live(source.registry, REPO, DRAFT) is True

    result = source.refresh(repository=REPO, ref=reg.DEFAULT_REF)

    assert result["binding"] == reg.BINDING_REFETCH
    assert bs.is_live(source.registry, REPO, DRAFT) is True
    survivor = source.registry.get(REPO, DRAFT)
    assert survivor is not None and survivor.source_root == scratch_repo.root
    assert survivor.payload == session_entry.payload
    # and the refresh still did its job: main is fresh and ACTIVE
    assert source.registry.active.key == (REPO, reg.DEFAULT_REF)


def test_a_regenerate_of_a_session_ref_does_not_make_the_draft_active(
        scratch_repo, tmp_path):
    """Finding 10b, the deterministic half: `_regenerate` registered with
    `active=True` unconditionally, and the ONLY compensation lived in the CALLER
    (`branch_session._preserving_active`), so the serve's own refresh route
    skipped it entirely.

    The guard now lives in the MUTATOR, which is what makes Phase 4 realization
    note 3's invariant ("any future code path that registers a session entry must
    go through it") structural rather than a thing to remember."""
    main_path = tmp_path / "main.json"
    main_path.write_text(
        json.dumps(generate_snapshot(scratch_repo.root, scratch_repo.repository)),
        encoding="utf-8")
    source = reg.SnapshotSource(baked_snapshot=main_path, repository=REPO,
                                checkout_root=scratch_repo.root)
    source.bootstrap()
    assert source.refresh_binding == reg.BINDING_REGENERATE
    session_path = tmp_path / "session.json"
    session_path.write_text(main_path.read_text(encoding="utf-8"), encoding="utf-8")
    session_entry = reg.entry_from_snapshot_file(
        session_path, repository=REPO, ref=DRAFT, source_root=scratch_repo.root)
    bs._register_without_stealing_active(source.registry, session_entry)
    assert source.registry.active.key == (REPO, reg.DEFAULT_REF)

    source.refresh(repository=REPO, ref=DRAFT)

    assert source.registry.active.key == (REPO, reg.DEFAULT_REF)
    assert source.index_document()["active"] == {"repository": REPO,
                                                 "ref": reg.DEFAULT_REF}
    # regenerating MAIN still keeps the human on main — the pre-existing
    # behaviour this narrowing must not have changed
    source.refresh(repository=REPO, ref=reg.DEFAULT_REF)
    assert source.registry.active.key == (REPO, reg.DEFAULT_REF)


def test_the_refresh_route_never_repoints_the_shared_surfaces_at_a_draft(
        scratch_repo, tmp_path):
    """The same defect through the ROUTE the human actually clicks: the header's
    regenerate button posts `{repository, ref}` taken from the ACTIVE selection,
    and the roster legitimately offers the session ref (FR-014) — so one click
    while the page was on the session view made an UNMERGED DRAFT the
    process-global active entry. A ref-less `GET /snapshot.json` then served the
    draft, and `index.active` named it, so a fresh page load OPENED on it."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    registry = _registry(scratch_repo, tmp_path)
    assert _create_raw(scratch_repo, registry)[0] == 200      # a real live session

    with _serving(scratch_repo, snapshot) as (host, port):
        before, index_before = _request(host, port, "GET", "/snapshot-index.json")
        assert (REPO, DRAFT) in {(e["repository"], e["ref"])
                                 for e in index_before["entries"]}
        status, payload = _request(host, port, "POST", "/actions/refresh",
                                   body={"repository": REPO, "ref": DRAFT})
        _s, index_after = _request(host, port, "GET", "/snapshot-index.json")
        _h, headers = _request(host, port, "GET", "/snapshot.json")

    assert status == 200, payload
    assert index_after["active"] == {"repository": REPO, "ref": reg.DEFAULT_REF}
    # the session row is still advertised — confinement is about what is ACTIVE,
    # never about hiding the session from the plane that owns it (FR-014)
    assert (REPO, DRAFT) in {(e["repository"], e["ref"])
                             for e in index_after["entries"]}


def test_concurrent_session_regenerations_keep_main_active(scratch_repo, tmp_path):
    """The unsynchronized read-modify-write, with a FORCED interleave — a
    barrier, no sleeps, and an outcome assertion rather than a timing one.

    `_preserving_active` reads the active key, runs an action that PROMOTES what
    it touches (`_regenerate` registers `active=True`), and puts the key back.
    Two of those interleaved leave a DRAFT active for good: T1 reads `main` and
    promotes `draft/a`; T2 then reads `draft/a` as "previous" and promotes
    `draft/b`; T1 restores `main`; T2 restores `draft/a`. FR-014a is broken and
    stays broken — the wheel, the funnel and the pipeline board render an
    unmerged draft, and `index.active` names it.

    The barrier is how the WRONG behaviour announces itself: it can only be
    satisfied if two writers are inside one read-modify-write at the same time.
    With the registry's re-entrant lock the second writer cannot get in, the
    barrier BREAKS by construction, and the assertion is on the resulting state —
    so the test does not depend on how fast anything runs, only on whether
    overlap is possible at all."""
    registry = _registry(scratch_repo, tmp_path)
    inside = threading.Barrier(2, timeout=1.0)
    overlapped = threading.Event()
    done: list[str] = []

    def promote(ref: str):
        entry = reg.SnapshotEntry(repository=REPO, ref=ref,
                                  source_root=scratch_repo.root)

        def action():
            # exactly what `_regenerate` does to a session entry it refreshes
            registry.register(entry, active=True)
            try:
                inside.wait()
                overlapped.set()
            except threading.BrokenBarrierError:
                pass                      # mutual exclusion held — the good path
            return entry

        bs._preserving_active(registry, action)
        done.append(ref)

    threads = [threading.Thread(target=promote, args=(ref,))
               for ref in ("draft/a", "draft/b")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
        assert not thread.is_alive()

    assert sorted(done) == ["draft/a", "draft/b"]
    assert overlapped.is_set() is False, \
        "two writers were inside one active read-modify-write at once"
    assert registry.get(REPO, "draft/a") is not None
    assert registry.get(REPO, "draft/b") is not None
    assert registry.active.key == (REPO, reg.DEFAULT_REF)


# ==========================================================================
# FINDING 14 — the hosted plane exposes NOTHING of the session capability
# ==========================================================================

def test_the_hosted_index_advertises_main_only_over_a_session_bearing_checkout(
        scratch_repo, tmp_path):
    """Finding 14: `_bootstrap_session_entries` ran BEFORE the bind was even
    classified and unconditionally, so an engineer serving a real checkout with
    `--host 0.0.0.0` admitted every live session into a HOSTED registry —
    and `/snapshot-index.json` names no ref, so `hosted_ref_refused` never saw
    it. The branch names of unmerged work (the topic and cluster ids) were
    published to anyone who could reach the bind, and the selector offered a row
    that could only ever 403.

    Contradicts spec US7 acceptance scenario 1 and FR-048 directly, and no
    realization note licenses it."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    registry = _registry(scratch_repo, tmp_path)
    assert _create_raw(scratch_repo, registry)[0] == 200
    assert bs.worktree_path(scratch_repo.root, DRAFT).exists()

    with _serving(scratch_repo, snapshot, host="0.0.0.0") as (host, port):
        status, index = _request(host, port, "GET", "/snapshot-index.json")
        _c, caps = _request(host, port, "GET", "/capabilities")
        refless_status, _refless = _request(host, port, "GET", "/snapshot.json")

    assert status == 200
    refs = {(e["repository"], e["ref"]) for e in index["entries"]}
    assert refs == {(REPO, reg.DEFAULT_REF)}
    assert DRAFT not in json.dumps(index)
    assert index.get("active", {}).get("ref") == reg.DEFAULT_REF
    assert caps["actions"]["session"] is False
    assert refless_status == 200          # main still serves, untouched


def test_the_local_plane_still_advertises_its_own_session(scratch_repo, tmp_path):
    """The other side of the same rule: confining the HOSTED plane must not
    confine the plane this whole feature lives on (FR-014, FR-048)."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    registry = _registry(scratch_repo, tmp_path)
    assert _create_raw(scratch_repo, registry)[0] == 200

    with _serving(scratch_repo, snapshot) as (host, port):
        status, index = _request(host, port, "GET", "/snapshot-index.json")

    assert status == 200
    assert (REPO, DRAFT) in {(e["repository"], e["ref"]) for e in index["entries"]}


def test_a_hosted_plane_never_serves_or_names_a_resolved_session_ref(scratch_repo,
                                                                     tmp_path):
    """The REF-LESS hole, which composes with finding 10b: `hosted_ref_refused`
    inspected only the ref a request NAMED, and a request that names none
    resolves to the ACTIVE entry. A non-`main` active entry was therefore
    servable off-loopback with no key in sight — and its ref was stamped on the
    freshness headers of every response, `/capabilities` included.

    The pathological state is built directly (a session entry ACTIVE on a hosted
    registry) through `build_server`'s existing `snapshot_source` seam, because
    it is exactly what findings 10b and 14 together used to produce."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    source = reg.SnapshotSource(baked_snapshot=snapshot, repository=REPO,
                                checkout_root=scratch_repo.root)
    source.bootstrap()
    session_entry = reg.SnapshotEntry(repository=REPO, ref=DRAFT,
                                      source_root=scratch_repo.root)
    session_entry.payload = snapshot.read_bytes()
    source.registry.register(session_entry, active=True)
    assert source.registry.active.ref == DRAFT

    with _serving(scratch_repo, snapshot, host="0.0.0.0",
                  snapshot_source=source) as (host, port):
        refless, body = _request(host, port, "GET", "/snapshot.json")
        keyed, keyed_body = _request(
            host, port, "GET", f"/snapshot.json?repository={REPO}&ref={DRAFT}")
        unkeyed_source, _s = _request(
            host, port, "GET", "/source/ideation/staging/demo-topic/demo-topic.md")
        caps_status, caps = _request(host, port, "GET", "/capabilities")
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("GET", "/capabilities")
        response = conn.getresponse()
        response.read()
        headers = {k.lower(): v for k, v in response.getheaders().items()} \
            if hasattr(response.getheaders(), "items") \
            else {k.lower(): v for k, v in response.getheaders()}
        conn.close()

    assert (refless, body["error"]) == (403, "session_unavailable")
    assert (keyed, keyed_body["error"]) == (403, "session_unavailable")
    assert unkeyed_source == 403
    # the probe still answers, and does not NAME the session ref anywhere —
    # the freshness headers ride on EVERY response, `/capabilities` included
    assert caps_status == 200 and caps["actions"]["session"] is False
    assert headers.get("x-snapshot-ref") is None
    assert DRAFT not in " ".join(f"{k}:{v}" for k, v in headers.items())


def test_a_hosted_response_never_names_a_session_ref_in_its_headers(scratch_repo,
                                                                    tmp_path):
    """The header half, isolated on the pure projection + the divergence
    stamper, so the rule is one definition rather than three route patches."""
    document = {"entries": [{"repository": REPO, "ref": reg.DEFAULT_REF},
                            {"repository": REPO, "ref": DRAFT},
                            {"repository": REPO, "ref": "cluster/cl-x"}],
                "active": {"repository": REPO, "ref": DRAFT}}

    projected = serve_mod.hosted_index(document)

    assert [e["ref"] for e in projected["entries"]] == [reg.DEFAULT_REF]
    assert "active" not in projected
    # the LOCAL plane's projection is the document itself, untouched
    assert serve_mod.hosted_index({"entries": [{"repository": REPO,
                                                "ref": reg.DEFAULT_REF}],
                                   "active": {"repository": REPO,
                                              "ref": reg.DEFAULT_REF}})["active"]


# ---- finding 14, wave 2: the OTHER field that carries (repository, ref) -------

def _every_ref_in(document) -> tuple[str, ...]:
    """Every `ref` value anywhere in a projected document, at any depth.

    Deliberately structure-blind: the wave-1 repair projected `entries` and
    `active` and missed `aggregates[].members`, which is the second field carrying
    `(repository, ref)` pairs, and a field-by-field assertion would have missed it
    exactly as the repair did. A future field lands in this scan for free."""
    found: list[str] = []
    if isinstance(document, dict):
        if isinstance(document.get("ref"), str):
            found.append(document["ref"])
        for value in document.values():
            found.extend(_every_ref_in(value))
    elif isinstance(document, list):
        for item in document:
            found.extend(_every_ref_in(item))
    return tuple(found)


def _aggregate_registry(scratch_repo, tmp_path, *, refs=(DRAFT,)):
    """A registry holding `main` plus session entries, with an AGGREGATE naming
    them as members — the shape `parse_index` builds from a local index file that
    declares one, and the shape the wave-2 critic reproduced the leak on."""
    registry = _registry(scratch_repo, tmp_path)
    for ref in refs:
        entry = reg.SnapshotEntry(repository=REPO, ref=ref,
                                  source_root=scratch_repo.root)
        entry.payload = b"{}"
        registry.register(entry)
    registry.register_aggregate(reg.Aggregate(
        id="everything", display_name="Everything",
        members=[(REPO, reg.DEFAULT_REF), *((REPO, ref) for ref in refs)]))
    return registry


def test_the_hosted_index_never_names_a_session_ref_as_an_aggregate_member(
        scratch_repo, tmp_path):
    """The reachable metadata leak the wave-1 finding-14 repair missed, and the
    premise it rested on ("a session ref is structurally unpublishable") corrected:
    `hosted_index` projected `entries` and `active` and left
    `aggregates[].members` — which `index_document` emits as `{repository, ref}`
    pairs — on the wire, so `GET /snapshot-index.json` off-loopback returned 200
    carrying `draft/<topic>` while `entries` was correctly main-only.

    Content stays confined either way (`?ref=…` is still 403), so what leaked is
    the topic id of unmerged work — the class FR-048 exists to prevent."""
    registry = _aggregate_registry(scratch_repo, tmp_path,
                                   refs=(DRAFT, "cluster/cl-secret-7"))
    document = registry.index_document()

    assert DRAFT in json.dumps(document)          # the LOCAL document names it
    projected = serve_mod.hosted_index(document)

    assert set(_every_ref_in(projected)) == {reg.DEFAULT_REF}
    assert DRAFT not in json.dumps(projected)
    assert "cl-secret-7" not in json.dumps(projected)
    # the aggregate SURVIVES, narrowed to its publishable members
    assert [a["id"] for a in projected["aggregates"]] == ["everything"]
    assert projected["aggregates"][0]["members"] == [
        {"repository": REPO, "ref": reg.DEFAULT_REF}]
    assert projected["aggregates"][0]["display_name"] == "Everything"


def test_an_aggregate_of_only_session_refs_is_dropped_from_a_hosted_index():
    """An aggregate is defined by the snapshots it composes, so one whose members
    are ALL unpublishable is dropped whole rather than published as a name with
    nothing behind it (a hosted plane composing it would find nothing to render).
    The `aggregates` key disappears with the last aggregate."""
    document = {"entries": [{"repository": REPO, "ref": reg.DEFAULT_REF}],
                "aggregates": [{"id": "drafts",
                                "members": [{"repository": REPO, "ref": DRAFT}]}]}

    projected = serve_mod.hosted_index(document)

    assert "aggregates" not in projected
    assert _every_ref_in(projected) == (reg.DEFAULT_REF,)


def test_the_hosted_route_publishes_no_session_ref_in_any_field(scratch_repo,
                                                                tmp_path):
    """The same rule over the REAL route off-loopback, which is where the critic
    measured the 200: the response BYTES carry no session ref in any field."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    source = reg.SnapshotSource(baked_snapshot=snapshot, repository=REPO,
                                checkout_root=scratch_repo.root)
    source.bootstrap()
    session_entry = reg.SnapshotEntry(repository=REPO, ref=DRAFT,
                                      source_root=scratch_repo.root)
    session_entry.payload = snapshot.read_bytes()
    source.registry.register(session_entry)
    source.registry.register_aggregate(reg.Aggregate(
        id="everything", members=[(REPO, reg.DEFAULT_REF), (REPO, DRAFT)]))

    with _serving(scratch_repo, snapshot, host="0.0.0.0",
                  snapshot_source=source) as (host, port):
        status, index = _request(host, port, "GET", "/snapshot-index.json")
    with _serving(scratch_repo, snapshot, snapshot_source=source) as (host, port):
        local_status, local_index = _request(host, port, "GET",
                                             "/snapshot-index.json")

    assert status == 200
    assert set(_every_ref_in(index)) == {reg.DEFAULT_REF}
    assert DRAFT not in json.dumps(index)
    # and the LOCAL plane is untouched: it still advertises the member
    assert local_status == 200
    assert DRAFT in json.dumps(local_index)


def test_a_published_index_refuses_a_session_ref_in_an_aggregate_member():
    """The publisher half, which is where "structurally unpublishable" was false:
    `build_index(published=True)` applied `assert_publishable` to entries and never
    to aggregate members, so a published index could name unmerged work. The check
    now covers BOTH collections of the document."""
    entries = [reg.SnapshotEntry(repository=REPO, ref=reg.DEFAULT_REF)]
    aggregate = reg.Aggregate(id="everything",
                              members=[(REPO, reg.DEFAULT_REF), (REPO, DRAFT)])

    with pytest.raises(reg.PublicationRefused) as refusal:
        reg.build_index(entries, published=True, aggregates=[aggregate])

    assert DRAFT in str(refusal.value)
    # the same registry, unpublished, still composes for the local plane
    document = reg.build_index(entries, published=False, aggregates=[aggregate])
    assert len(document["aggregates"][0]["members"]) == 2


def test_the_hosted_plane_renders_no_session_surface_at_all():
    """The RENDERER half (finding 14): `sessionActionsLive` collapsed "no
    authority, here is the CLI" (FR-046) and "no sessions at all" (FR-048) into
    one boolean, so the hosted page announced that a session was live, named its
    branch, and printed filled-in `gate edit-document` / `open-pr` /
    `abandon-session` invocations for it.

    The discriminator is the capability's own statement. `sessionSurfaceHidden`
    is asked FIRST in both the mount and the view's `drawSession`, and the whole
    bar goes with it — posture chip included."""
    views = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
    model = (views / "staging-workbench-model.js").read_text(encoding="utf-8")
    session = (views / "swb-session.js").read_text(encoding="utf-8")
    view = (views / "staging-workbench.js").read_text(encoding="utf-8")

    assert "export function sessionSurfaceHidden(caps)" in model
    assert "return actions.session === false;" in model
    # the mount refuses BEFORE the descriptor path it used to fall into
    assert "if (sessionSurfaceHidden(o.caps)) return null;" in session
    assert session.index("sessionSurfaceHidden(o.caps)") < \
        session.index("if (!sessionActionsLive(o.caps))")
    # and the bar (posture chip included) is hidden, not merely emptied
    assert "sessionbar.hidden = !scope || sessionSurfaceHidden(caps);" in view


# ==========================================================================
# FINDING 16 — the outline reads the SESSION worktree, not main
# ==========================================================================

def test_the_unkeyed_source_route_resolves_to_main_while_a_session_is_live(
        scratch_repo, tmp_path):
    """The server-side fact the renderer defect turned into a lie: the ACTIVE
    entry is deliberately kept on `main` for a session's whole life (FR-014a),
    and the unkeyed `/source/` resolves to the ACTIVE entry. So an outline that
    dropped the key did not merely lose precision — it read a DIFFERENT TREE.

    This is the oracle the fix is measured against; it must keep holding, because
    the unkeyed route's behaviour is correct for every non-session reader."""
    registry = _registry(scratch_repo, tmp_path)
    created = _create_raw(scratch_repo, registry)[1]
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    relative = created["path"]

    assert (worktree / relative).exists()
    assert not (scratch_repo.root / relative).exists()      # absent at main
    assert registry.active.ref == reg.DEFAULT_REF
    assert registry.resolve_source(None, None, relative) is None
    keyed = registry.resolve_source(REPO, DRAFT, relative)
    assert keyed is not None and keyed.read_text(encoding="utf-8").strip()


def _call_arguments(source: str, call: str) -> str:
    """The argument text of ONE call, so a source pin cannot be satisfied by a
    neighbouring line that happens to contain the same token.

    Balanced-paren scan from the call's own `(` — the argument list spans lines and
    contains nested object/arrow parens, so a `split(");")` would cut it short."""
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


def test_the_outline_pane_reads_through_the_active_keys_source_base():
    """Finding 16: `app.js` computed the keyed `/source/<repo>@<ref>/` base and
    used it for the explorer/viewer, but the workbench mount was handed only
    `{ onOpenDoc, caps, active, index }` — and a test PINNED that omission. The
    outline pane's `renderViewer(host, { path, doc })` therefore fell through to
    `viewer.js`'s `"/source/"` default.

    Consequence, both halves measured: a document the session EDITED rendered
    `main`'s bytes, and a document the session CREATED 404'd — on the one pane
    US2 acceptance scenario 5 and FR-010 name explicitly. The docs row beside it
    was keyed correctly the whole time, so the page disagreed with itself.

    The renderer stays TRANSPORT-FREE: the viewer owns the fetch, and threading a
    base string adds no call site (FR-047's counts are unchanged).

    The spellings below gained a trailing argument each in
    `add-staged-topic-outline-template` (the add-section seam, and the viewer's
    `onText` read-back the section index is built from). What this test guards is
    unchanged: `sourceBase` and `edit` must still be THREADED to the pane and on
    to the viewer, because dropping either is what put a draft view on `main`'s
    bytes. Both additions are transport-free — no new call site, no second fetch
    of the same bytes.

    THE CALL-SITE PIN IS A REGEX, and the review that made it one is the reason.
    Widening the declaration made the plain substring
    `renderOutlinePanel(pane, snapshot, scope, create, sourceBase, edit,` a
    prefix of the DECLARATION as well as the call, so it stopped constraining the
    call at all: the reviewer replaced `sourceBase` with `null` at the call site
    and the whole suite stayed green — exactly the finding-16 regression this test
    exists to catch. The pattern below must therefore run through the call's own
    closing arguments, which the declaration cannot supply."""
    web = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
    view = (web / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    app = (web / "app.js").read_text(encoding="utf-8")

    assert ("function renderOutlinePanel(pane, snapshot, scope, create, "
            "sourceBase, edit, sections)") in view
    assert re.search(
        r"renderOutlinePanel\(pane, snapshot, scope, create, sourceBase, edit,"
        r"\s*outlineSectionSeam\(\)\);", view), (
            "the outline pane must be CALLED with the active key's own sourceBase "
            "and edit action, not a default or a null")
    assert "renderViewer(host, { path, doc, sourceBase, edit," in view
    assert "sourceBase, edit, onSessionRekey," in view
    assert "onSessionEnded, onScopeOpened } = {})" in view
    # Shell viewers get a fixed key derived from their selected entry. The
    # workbench alone owns a mutable key, so closing a draft overlay cannot
    # redirect a main explorer edit into the branch checkout.
    assert "const sourceKey = sourceKeyFor(entry);" in app
    assert "edit: createEditAction({ caps, key: sourceKey })" in app
    assert "let workbenchSourceKey = sourceKeyFor(null);" in app
    assert "currentSourceKey" not in app
    assert "const nextSourceBase = sourceBaseFor(next);" in app, (
        "the re-key must go through the SAME derivation, never a second rule")
    rekey = app.split("const rekeyToSession = async (ref) => {", 1)[1].split(
        "\n    };", 1)[0]
    assert rekey.index("nextSnapshot = await loadSnapshot(next);") \
        < rekey.index("workbenchSourceBase = nextSourceBase;") \
        < rekey.index("workbenchSourceKey = next;"), (
            "source reads and edit writes must stay on main until the session "
            "snapshot loads, then adopt the session together")
    reset = app.split("const resetEndedSession = async () => {", 1)[1].split(
        "\n    };", 1)[0]
    assert reset.index('const next = safeKey({ repository, ref: "main" });') \
        < reset.index("nextSnapshot = await loadSnapshot(next);") \
        < reset.index("workbenchSourceBase = nextSourceBase;") \
        < reset.index("workbenchSourceKey = next;"), (
            "ending a session must load main before source reads and edit writes "
            "adopt it together")
    assert "catch" not in reset, (
        "a failed main refresh must retain the displayed branch's edit key; "
        "switching only the key would cross-wire branch bytes to main")
    assert "snapshot: nextSnapshot" in reset and "index: nextIndex || index" in reset
    assert "explorer.openDoc(path, doc, workbenchSourceKey)" in app
    # AND the hand-over is asserted INSIDE the mount call's own argument list
    # (wave 2). This assertion used to be a bare `"sourceBase });" in app`, which
    # the UNRELATED `initTabs(snapshot, { …, sourceBase });` line satisfied: the
    # wave-2 critic dropped `sourceBase });` from the `mountStagingWorkbench(`
    # call, left 129/129 tests green, and reproduced the whole defect in a real
    # browser. A substring test that any neighbouring line can satisfy pins
    # nothing, so the call is isolated first.
    assert "sourceBase" in _call_arguments(app, "mountStagingWorkbench("), (
        "the workbench mount must be handed the keyed source base — the outline "
        "pane's reads go through it, and app.js is the only place it exists")
    # and no transport arrived in the view or the pure model with it
    assert "fetch(" not in view
    model = (web / "views" / "staging-workbench-model.js").read_text(encoding="utf-8")
    assert "fetch(" not in model
