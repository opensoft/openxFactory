"""GATEWAY PROVENANCE on every gate-action record
(openxFactory `add-workbench-branch-sessions` design D23; Brett's 2026-07-27
ruling, item 3 — "tag the event with the actual facts we know").

WHAT THE RULING SETTLED, and why this file exists at all. The console's
human/agent boundary is a CONSOLE-PRESENCE control — anti-CSRF / same-origin — and
NOT authentication. A process running as the identified human, on the human's own
machine, can read the per-serve console token from `/capabilities` or set
`XF_HUMAN_CONSOLE=1` and act as the human. Brett ACCEPTED that residual (item 1:
distinguishing the two needs the xForge-host identity work deferred under D22) and
AMENDED the ratified scenarios to say what is enforced (item 2, openxFactory's
stage). Item 3 is this repo's half: every record names the SURFACE the action
arrived on and HOW presence was shown, so an act performed through the accepted
residual is AUDITABLE rather than invisible.

Four claims, and each one fails for a different reason if the wiring is wrong:

  * **THE FACT TRAVELS FROM WHERE IT IS KNOWN.** Only `serve.py`'s handler knows a
    request presented this serve's console token; only `cli.py` knows whether
    presence came from a tty or a declaration. Both are asserted THROUGH THE REAL
    GATEWAY — a live loopback server over `http.client`, and `cli.main([...])` —
    never by handing a constant to the engine, because a constant proves only that
    the engine can write what it is told.

  * **THE THREE PROOFS ARE DISTINGUISHABLE.** `console-token`, `tty` and
    `declared` are separate values in the landed schema precisely so an auditor can
    filter for the weakest one. A build that collapsed them (or that recorded `tty`
    for a declaration) would satisfy "provenance is present" and still destroy the
    ruling's purpose.

  * **A BODY CANNOT SPELL IT.** A self-declared surface is worthless, so the
    parameter is a `Provenance` TYPE the gateways construct: a request body is a
    mapping, no route reads a `provenance` key from one, and the builder REFUSES a
    mapping outright. Asserted by posting a body that tries.

  * **IT VALIDATES.** Every record shown here is validated as a FILE by the pinned
    openxFactory validator against the landed schema, which is where `provenance`'s
    two required inner fields and its two enums actually live. This repo never
    modifies that schema; it reads it.

Hermetic on the `scratch_repo` harness (a throwaway checkout with a local BARE
origin): no network, no real `gh`/`nlm` (`tests/hermeticity.py`), no real-checkout
mutation, no sleeps, and every remote write goes through `FakePullRequests`.
"""

from __future__ import annotations

import http.client
import json
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT, find_openxfactory_validator

from session_fixtures import (
    FakeNotebookAdapter,
    FakePullRequests,
    build_scratch_repo,
)

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
RECORDS = gc.DEFAULT_RECORDS_DIR
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
AT = "2026-07-27T09:00:00Z"
VALIDATOR = find_openxfactory_validator()

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": f"ideation/staging/{TOPIC}/",
    "repository_context": REPO,
    "scope_kind": bs.STAGED_TOPIC,
    "scope_id": TOPIC,
}

HTTP_TOKEN = {"surface": "http", "console_presence": "console-token"}
CLI_TTY = {"surface": "cli", "console_presence": "tty"}
CLI_DECLARED = {"surface": "cli", "console_presence": "declared"}

needs_validator = pytest.mark.skipif(
    VALIDATOR is None, reason="pinned openxFactory validator not reachable")


# ==========================================================================
# helpers — the real gateways, and nothing else
# ==========================================================================

def _registry(repo, tmp_path, *, name="main-snapshot.json"):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


@contextmanager
def _serving(repo, snapshot_path, *, actor="brett", **kw):
    """A serve over REAL HTTP against the scratch checkout. Both outbound seams
    are faked at the ONE injection point each (FR-043, quickstart step 6): the
    notebook adapter and the pull-request port. Nothing here can reach a network."""
    kw.setdefault("adapter_factory", FakeNotebookAdapter)
    kw.setdefault("pull_request_factory", FakePullRequests)
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, host="127.0.0.1",
                                   actor=actor, **kw)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


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


def _console_headers(host, port):
    """The headers a request FROM THE SERVED PAGE carries: this serve's own
    console token, read the only way the page can read it — a same-origin
    `GET /capabilities`."""
    status, caps = _request(host, port, "GET", "/capabilities")
    assert status == 200, caps
    token = caps.get("console_token")
    assert token, caps
    return {serve_mod.CONSOLE_TOKEN_HEADER: token,
            "Origin": f"http://{host}:{port}"}


def _post(host, port, verb, body):
    return _request(host, port, "POST", f"/actions/gate/{verb}", body=body,
                    headers=_console_headers(host, port))


def _served_snapshot(repo, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


def _validate(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                          capture_output=True, text=True)


def _assert_valid(path: Path) -> None:
    proc = _validate(path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 error(s)" in proc.stdout


def _loaded(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _tty(monkeypatch):
    """An INTERACTIVE terminal, and no declaration: the CLI's other proof.

    The suite's autouse `declared_human_console` fixture exports
    `XF_HUMAN_CONSOLE=1` for every test, so the declaration must be REMOVED here or
    `tty` is unreachable — which is itself the precedence this pins."""
    monkeypatch.delenv(cli_mod.HUMAN_CONSOLE_ENV, raising=False)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True, raising=False)


# ==========================================================================
# THE TYPE — validated at construction, and not something a body can be
# ==========================================================================

def test_the_vocabulary_is_the_landed_schemas(monkeypatch):
    assert gc.SURFACES == ("http", "cli", "intent-plane")
    assert gc.CONSOLE_PRESENCES == ("console-token", "tty", "declared",
                                    "ingress-auth")
    assert gc.HTTP_CONSOLE_TOKEN.as_record() == HTTP_TOKEN
    assert gc.CLI_TTY.as_record() == CLI_TTY
    assert gc.CLI_DECLARED.as_record() == CLI_DECLARED
    # add-ideation-intent-plane task 4.3: the apply lane's own pair — the
    # third door, grown in the schema and here in lockstep.
    assert gc.INTENT_INGRESS.as_record() == {
        "surface": "intent-plane", "console_presence": "ingress-auth"}


def test_an_unknown_surface_or_proof_cannot_be_constructed():
    with pytest.raises(gc.GateRefused) as refused:
        gc.Provenance("ssh", gc.PRESENCE_TTY)
    assert "surface" in str(refused.value)
    with pytest.raises(gc.GateRefused):
        gc.Provenance(gc.SURFACE_CLI, "sudo")


def test_there_is_no_value_meaning_presence_was_not_shown():
    """The schema names no such value BECAUSE such a call is refused before a
    record exists. A build that invented one would let a record claim the boundary
    held when it had not been tested — the invisible residual, relocated."""
    for spelling in ("none", "unknown", "not-shown", "", "false"):
        with pytest.raises(gc.GateRefused):
            gc.Provenance(gc.SURFACE_HTTP, spelling)


def test_the_builder_refuses_a_mapping_which_is_what_a_body_could_carry():
    """The type IS the control: a request body can carry a `{surface: ...}` dict
    and nothing else, so the builder must not accept one even if some future route
    passed it through by mistake."""
    with pytest.raises(gc.GateRefused) as refused:
        gc.build_gate_action_record(
            actor="brett", action=gc.ACTION_RATIFY, at=AT, change_id="add-x",
            artifacts=[{"kind": gc.ART_RATIFICATION_RECORD, "reference": "r.yaml"}],
            provenance=dict(HTTP_TOKEN))          # type: ignore[arg-type]
    assert "OBSERVED" in str(refused.value)


def test_a_record_without_provenance_is_the_pre_growth_shape_byte_for_byte():
    """The schema requires `provenance` in NO conditional because pre-growth
    records exist and must stay valid. That posture is only real if the builder
    still emits the pre-growth shape when no gateway declares itself."""
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_RATIFY, at=AT, change_id="add-x",
        artifacts=[{"kind": gc.ART_RATIFICATION_RECORD, "reference": "r.yaml"}])
    assert "provenance" not in record
    assert list(record) == ["schema_version", "kind", "actor", "action",
                            "target", "at", "artifacts"]


def test_provenance_is_stamped_in_the_schemas_own_property_order():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_RATIFY, at=AT, change_id="add-x",
        artifacts=[{"kind": gc.ART_RATIFICATION_RECORD, "reference": "r.yaml"}],
        provenance=gc.HTTP_CONSOLE_TOKEN)
    assert list(record) == ["schema_version", "kind", "actor", "action",
                            "target", "provenance", "at", "artifacts"]
    assert record["provenance"] == HTTP_TOKEN


# ==========================================================================
# THE CLI GATEWAY — which proof, observed where it is known
# ==========================================================================

def test_the_cli_names_the_declaration_as_its_own_weakest_proof(monkeypatch):
    monkeypatch.setenv(cli_mod.HUMAN_CONSOLE_ENV, "1")
    assert cli_mod.console_presence() == gc.PRESENCE_DECLARED
    assert cli_mod.cli_provenance().as_record() == CLI_DECLARED


def test_the_cli_names_a_terminal_as_a_tty(monkeypatch):
    _tty(monkeypatch)
    assert cli_mod.console_presence() == gc.PRESENCE_TTY
    assert cli_mod.cli_provenance().as_record() == CLI_TTY


def test_a_declaration_beats_a_terminal_so_the_weakest_proof_is_recorded(
        monkeypatch):
    """Both true at once is the case an audit consumer must not be able to miss:
    a script that exports the variable inside a human's terminal session is
    recorded as `declared`, never upgraded to `tty`."""
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True, raising=False)
    monkeypatch.setenv(cli_mod.HUMAN_CONSOLE_ENV, "1")
    assert cli_mod.console_presence() == gc.PRESENCE_DECLARED


def test_no_presence_no_provenance_and_the_old_predicate_still_answers(
        monkeypatch):
    """`human_console_present` is now derived from `console_presence`, so the
    admission decision and the recorded proof cannot drift apart."""
    monkeypatch.delenv(cli_mod.HUMAN_CONSOLE_ENV, raising=False)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False, raising=False)
    assert cli_mod.console_presence() is None
    assert cli_mod.human_console_present() is False
    assert cli_mod.cli_provenance() is None


# ==========================================================================
# THE HTTP GATEWAY — every session verb, through the real route
# ==========================================================================

@needs_validator
def test_every_session_verbs_record_names_the_http_door(scratch_repo, tmp_path):
    """The whole loop on ONE session, through the live server: open it with
    `create-document`, rewrite with `edit-document`, and end it — once by saving
    (`open-pr`) and, on a second session, by abandoning it. Every record names
    `http` + `console-token`, and every record VALIDATES as a file.

    The two residences are exercised deliberately: `edit-document`'s record lives
    on the branch inside the worktree, `open-pr`'s and `abandon-session`'s live in
    the served checkout (FR-029, plan Constraint 10)."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        status, created = _post(host, port, "create-document", CREATE_BODY)
        assert status == 200, created
        status, edited = _post(host, port, "edit-document", {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "document": created["path"],
            "content": "# First Draft\n\nrewritten on the http door.\n"})
        assert status == 200, edited
        status, saved = _post(host, port, "open-pr",
                              {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC})
        assert status == 200, saved

    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    # create-document + edit-document: SESSION-RESIDENT, read from the worktree
    for payload, action in ((created, gc.ACTION_CREATE_DOCUMENT),
                            (edited, gc.ACTION_EDIT_DOCUMENT)):
        path = worktree / payload["record"]
        record = _loaded(path)
        assert record["action"] == action
        assert record["provenance"] == HTTP_TOKEN, action
        _assert_valid(path)
    # open-pr: MAIN-RESIDENT, read from the served checkout
    path = scratch_repo.root / saved["record"]
    record = _loaded(path)
    assert record["action"] == gc.ACTION_OPEN_PR
    assert record["provenance"] == HTTP_TOKEN
    _assert_valid(path)


@needs_validator
def test_the_abandon_records_http_door_is_named_and_validates(scratch_repo,
                                                             tmp_path):
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        status, created = _post(host, port, "create-document", CREATE_BODY)
        assert status == 200, created
        status, ended = _post(host, port, "abandon-session", {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "reason": "the spike answered its question"})
        assert status == 200, ended

    path = scratch_repo.root / ended["record"]
    record = _loaded(path)
    assert record["action"] == gc.ACTION_ABANDON_SESSION
    assert record["provenance"] == HTTP_TOKEN
    _assert_valid(path)


def test_a_body_that_supplies_its_own_provenance_cannot_influence_the_record(
        scratch_repo, tmp_path):
    """The load-bearing negative. A caller that could spell its own surface could
    launder an action through a door it never used — which would make the whole
    tag worse than absent. The body's `provenance` is ignored on both counts: no
    route reads the key, and the value it carries is a mapping the builder refuses.
    """
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")
    lie = {"surface": "cli", "console_presence": "tty"}

    with _serving(scratch_repo, snapshot) as (host, port):
        status, created = _post(host, port, "create-document",
                                {**CREATE_BODY, "provenance": lie})
        assert status == 200, created

    record = _loaded(bs.worktree_path(scratch_repo.root, DRAFT) / created["record"])
    assert record["provenance"] == HTTP_TOKEN


def test_a_refused_non_console_call_writes_no_record_to_tag(scratch_repo,
                                                            tmp_path, capsys):
    """The other side of the same coin: presence that was NOT shown never produces
    a record at all on a session verb, which is precisely why the vocabulary needs
    no value for it (and why the enforcement path is unchanged by this growth)."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        status, payload = _request(host, port, "POST",
                                   "/actions/gate/create-document",
                                   body=CREATE_BODY)

    assert (status, payload["error"]) == (403, "agent_invocation"), payload
    assert not list((scratch_repo.root / RECORDS).rglob("*.gate-action.yaml"))
    assert "agent_invocation refused (create-document)" in capsys.readouterr().err


# ==========================================================================
# THE CLI GATEWAY — every session verb, through cli.main
# ==========================================================================

def _cli_session(repo, tmp_path, monkeypatch, *, actor="brett"):
    """Open a session through the CLI itself, with the notebook seam faked."""
    monkeypatch.setattr(cli_mod, "_notebook_port",
                        lambda repo_root: FakeNotebookAdapter())
    rc = cli_mod.main(["gate", "create-document", "--repo-root", str(repo.root),
                       "--actor", actor, "--area", f"ideation/staging/{TOPIC}/",
                       "--title", "First Draft",
                       "--summary", "The session's first document.",
                       "--topics", "alpha", "--repository-context", REPO,
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC])
    assert rc == 0
    return bs.worktree_path(repo.root, DRAFT)


def _session_records(root: Path, action: str) -> list[Path]:
    return sorted(Path(root).rglob(f"{action}-*.gate-action.yaml"))


@needs_validator
def test_every_session_verbs_record_names_the_cli_door(scratch_repo, tmp_path,
                                                        monkeypatch):
    """The CLI's whole loop, `declared` (a pytest process is a non-interactive
    human shell that DECLARES, exactly as a `nohup`-ed one would — the autouse
    fixture makes that declaration). The records are the same shapes the HTTP door
    produced, with the other surface named."""
    worktree = _cli_session(scratch_repo, tmp_path, monkeypatch)
    content = tmp_path / "replacement.md"
    content.write_text("# First Draft\n\nrewritten on the cli door.\n",
                       encoding="utf-8")
    port = FakePullRequests()
    monkeypatch.setattr(cli_mod, "_pull_request_port", lambda *a, **k: port)

    assert cli_mod.main([
        "gate", "edit-document", "--repo-root", str(scratch_repo.root),
        "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
        "--document", f"ideation/staging/{TOPIC}/first-draft.md",
        "--content-file", str(content)]) == 0
    assert cli_mod.main([
        "gate", "open-pr", "--repo-root", str(scratch_repo.root),
        "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
        "--scope-id", TOPIC]) == 0

    for root, action in (
            (worktree, gc.ACTION_CREATE_DOCUMENT),
            (worktree, gc.ACTION_EDIT_DOCUMENT),
            (scratch_repo.root, gc.ACTION_OPEN_PR)):
        found = _session_records(root, action)
        assert len(found) == 1, (action, found)
        assert _loaded(found[0])["provenance"] == CLI_DECLARED, action
        _assert_valid(found[0])


@needs_validator
def test_the_cli_abandon_record_names_the_cli_door_and_validates(scratch_repo,
                                                                 tmp_path,
                                                                 monkeypatch):
    _cli_session(scratch_repo, tmp_path, monkeypatch)

    assert cli_mod.main([
        "gate", "abandon-session", "--repo-root", str(scratch_repo.root),
        "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
        "--reason", "the spike answered its question"]) == 0

    found = _session_records(scratch_repo.root, gc.ACTION_ABANDON_SESSION)
    assert len(found) == 1, found
    assert _loaded(found[0])["provenance"] == CLI_DECLARED
    _assert_valid(found[0])


@needs_validator
def test_the_tty_proof_reaches_the_record_and_is_distinguishable(scratch_repo,
                                                                 tmp_path,
                                                                 monkeypatch):
    """The SAME verb, the SAME surface, a DIFFERENT proof — and the record says so.
    Without this the three enum values would be decoration: a build that hard-coded
    `declared` on the CLI would pass every other test in this file."""
    _tty(monkeypatch)
    worktree = _cli_session(scratch_repo, tmp_path, monkeypatch)

    found = _session_records(worktree, gc.ACTION_CREATE_DOCUMENT)
    assert len(found) == 1, found
    assert _loaded(found[0])["provenance"] == CLI_TTY
    _assert_valid(found[0])


# ==========================================================================
# THE PRE-EXISTING VERBS — the point is to know which door ANY action came
# through, so the verbs that predate sessions are tagged too
#
# Their ENFORCEMENT posture is deliberately unchanged: `serve.py` refuses a
# non-console call only on the session verbs, because widening the refusal is a
# separate decision with its own compatibility surface. What IS widened is the
# OBSERVATION — a pure header read with no side effect — so a pre-existing verb
# driven from the human's own page is tagged like everything else. A pre-existing
# verb invoked without console presence still lands, and writes NO provenance
# rather than a guessed one; that gap is reported in the realization note.
# ==========================================================================

@needs_validator
def test_a_pre_existing_verbs_record_names_the_http_door(scratch_repo, tmp_path):
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        status, payload = _post(host, port, "ratify",
                                {"change_id": "add-demo-change"})
        assert status == 200, payload

    path = scratch_repo.root / payload["record"]
    record = _loaded(path)
    assert record["action"] == gc.ACTION_RATIFY
    assert record["provenance"] == HTTP_TOKEN
    _assert_valid(path)


def test_a_pre_existing_verb_without_console_presence_still_lands_untagged(
        scratch_repo, tmp_path):
    """Honesty over uniformity. The pre-existing verbs' refusal posture is NOT
    widened here, so a non-console call to one still succeeds — and its record
    carries no `provenance`, because there is no honest value for "presence was
    not shown" and inventing one would be the defect the ruling corrected."""
    snapshot = _served_snapshot(scratch_repo, tmp_path / "snapshot.json")

    with _serving(scratch_repo, snapshot) as (host, port):
        status, payload = _request(host, port, "POST", "/actions/gate/ratify",
                                   body={"change_id": "add-demo-change"})
        assert status == 200, payload

    record = _loaded(scratch_repo.root / payload["record"])
    assert "provenance" not in record


@needs_validator
def test_a_pre_existing_verbs_cli_record_names_the_cli_door(scratch_repo,
                                                            tmp_path):
    assert cli_mod.main(["gate", "ratify", "--repo-root", str(scratch_repo.root),
                         "--actor", "brett", "--change-id", "add-demo-change"]) == 0

    found = _session_records(scratch_repo.root, gc.ACTION_RATIFY)
    assert len(found) == 1, found
    assert _loaded(found[0])["provenance"] == CLI_DECLARED
    _assert_valid(found[0])


# ==========================================================================
# THE ROUTE LAYER — it never derives the fact, and it never reads it from a body
# ==========================================================================

def test_the_route_layer_declares_provenance_and_derives_nothing():
    """A structural pin on the seam itself: `run_gate_action` TAKES the fact, and
    no module under `ideation_dashboard` reads a `provenance` key out of a body."""
    import inspect

    assert "provenance" in inspect.signature(gr.run_gate_action).parameters
    package = Path(gr.__file__).parent
    offenders = []
    for module in sorted(package.glob("*.py")):
        for n, line in enumerate(module.read_text(encoding="utf-8").splitlines(), 1):
            if 'body.get("provenance")' in line or "body\\[\"provenance\"\\]" in line:
                offenders.append(f"{module.name}:{n}: {line.strip()}")
    assert not offenders, offenders


def test_an_undeclared_gateway_writes_the_pre_growth_shape(scratch_repo, tmp_path):
    """`run_gate_action` called with no gateway (a caller that is neither door)
    writes a record with no provenance — never a default. A default would be a
    guess, and a guessed door is worse than an absent one."""
    registry = _registry(scratch_repo, tmp_path)
    status, created = gr.run_gate_action(
        "create-document", dict(CREATE_BODY), checkout_root=scratch_repo.root,
        actor="brett", snapshot_path=None, session_registry=registry,
        repository=scratch_repo.repository)
    assert status == 200, created

    record = _loaded(bs.worktree_path(scratch_repo.root, DRAFT) / created["record"])
    assert "provenance" not in record


def test_the_lens_records_inline_builder_stamps_the_same_block(tmp_path):
    """The lens verbs build their record INLINE (their `target.set` has no builder
    keyword), so the block's presence and POSITION are asserted separately — the
    one place the two builders could drift."""
    gate = HumanGate(tmp_path, [RECORDS], human_actor="brett")
    path, _rel = gr._write_lens_record(
        gate, RECORDS, action=gr.ACTION_LENS_SAVE_RECIPE, set_slug="demo-set",
        at=AT, artifacts=[{"kind": gc.ART_OTHER, "reference": "m.yaml"}],
        provenance=gc.CLI_TTY)

    record = _loaded(path)
    assert list(record)[:6] == ["schema_version", "kind", "actor", "action",
                                "target", "provenance"]
    assert record["provenance"] == CLI_TTY
    with pytest.raises(gc.GateRefused):
        gr._write_lens_record(
            gate, RECORDS, action=gr.ACTION_LENS_SAVE_RECIPE, set_slug="other-set",
            at=AT, artifacts=[{"kind": gc.ART_OTHER, "reference": "m.yaml"}],
            provenance=dict(CLI_TTY))            # type: ignore[arg-type]


def test_no_record_banner_promises_more_than_the_gate_enforces(tmp_path):
    """Brett's ruling item 2, in this repo's prose. BOTH banners written into
    records — the shared one and the lens verbs' own — used to say agents
    "structurally cannot author one". After item 1 that is false in exactly the way
    the ratified scenarios were, so each says what is enforced (a console-PRESENCE
    control) and points at `provenance`.

    Asserted on the BYTES OF A WRITTEN RECORD, not on module source: the source
    quotes the superseded sentence in the amendment note that records why it
    changed, which is the discipline the shipped-feature-amendment rule asks for
    and must not be mistaken for the claim itself."""
    gate = HumanGate(tmp_path, [RECORDS], human_actor="brett")
    shared = gc.write_gate_action_record(
        gate, RECORDS, gc.build_gate_action_record(
            actor="brett", action=gc.ACTION_RATIFY, at=AT, change_id="add-x",
            provenance=gc.HTTP_CONSOLE_TOKEN,
            artifacts=[{"kind": gc.ART_RATIFICATION_RECORD,
                        "reference": "r.yaml"}]))
    lens, _rel = gr._write_lens_record(
        gate, RECORDS, action=gr.ACTION_LENS_SAVE_RECIPE, set_slug="banner-set",
        at=AT, artifacts=[{"kind": gc.ART_OTHER, "reference": "m.yaml"}],
        provenance=gc.HTTP_CONSOLE_TOKEN)

    for path in (shared, lens):
        text = path.read_text(encoding="utf-8")
        assert "structurally cannot author" not in text, path
        assert "console-PRESENCE control" in text, path
        assert "provenance" in text, path
