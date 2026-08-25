"""The ENDINGS and the two mutual-exclusion gates (007-workbench-branch-sessions
T045-T051; FR-021-FR-028, FR-019).

Phases 3-5 opened a session, projected it, and wrote inside it. This file proves a
session can STOP — and that a tile is never both worked and proposed, from either
direction.

Five claims earn their own section:

  * **Abandon tears down, and records WHY on `main`** (FR-021, FR-022). The
    worktree, the registry entry, and the session notebook go; the pushed branch
    and any open pull request stay, untouched by the verb (the pull-request port is
    never even called). The record is MAIN-RESIDENT — the SERVED checkout's
    `ideation/dashboard/gate-records/`, exactly where `propose` / `demote` /
    `dispose` write — and adds NO commit to the session branch, because FR-028's
    cleanup DELETES that branch and a branch-resident reason-record would die with
    it. The discriminating assertion is exactly that: delete the branch through the
    FR-028 route and read the reason back.

  * **`propose` is refused by the LIVE SESSION, not by the branch** (FR-023). It
    refuses while a session holds the tile, naming the branch and both resolutions,
    and persists nothing; it proceeds after a merge, and it proceeds after an
    abandon EVEN THOUGH the abandoned branch survives — a surviving branch is
    evidence, not unresolved working state. The pre-existing missing-topic,
    duplicate-dispatch, and agent refusals are unchanged.

  * **A proposed tile is closed to session work** (FR-024), with the TWO distinct
    messages: an existing proposal names `demote`; a dispatched-and-undelivered
    `propose` job says the proposal has not landed, because naming `demote` would
    name a route the human cannot take (D20).

  * **The abandoned branch is never chosen silently** (FR-025-FR-027). The tile
    reports the branch and offers RESUME or NEW; RESUME re-materializes a worktree
    over the EXISTING branch keeping its name; NEW allocates the next ordinal over
    the UNION of remote and local refs; a second writer after the choice JOINS; and
    a MERGED tile is reworked with no prompt at all, because the merge deleted the
    branch.

  * **The cleanup is human-invoked and late** (FR-028). It is offered only once the
    topic's PROPOSAL exists — never as a consequence of a `propose` DISPATCH, whose
    commissioned authoring may never produce one.

Every test builds on the `scratch_repo` harness (a throwaway checkout with a local
bare `origin`). No serve here is ever pointed at a real or fixture tree — a serve
WRITES into whatever `--checkout-root` it is given (research R10).
"""

from __future__ import annotations

import http.client
import inspect
import json
import shutil
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT

from session_fixtures import FakeNotebookAdapter, FakePullRequests, build_scratch_repo
from staging_shapes import staging_fragment

from ideation_dashboard import branch_session as bs
from ideation_dashboard import doxbench_hash
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import kickoff as kickoff_mod
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import BoundaryViolation, OutputBoundary
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
CHANGE = "add-demo-topic"
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
RECORDS = gc.DEFAULT_RECORDS_DIR
ABANDON_ROUTE = "/actions/gate/abandon-session"
CLEANUP_ROUTE = "/actions/gate/cleanup-abandoned-branch"

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
    """A registry in the shape a serve holds one: `(repository, main)` registered
    and ACTIVE, with the served checkout as its source root. Written OUTSIDE the
    checkout, so building it never moves the served tree."""
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
    """One `create-document` through the ROUTE — the gesture that OPENS (or joins,
    or refuses on) the tile's session. Returns (status, payload)."""
    actor = over.pop("actor", "brett")
    return gr.run_gate_action(
        "create-document", {**CREATE_BODY, **over},
        checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry, repository=repo.repository)


def _create(repo, registry, **over):
    status, payload = _create_raw(repo, registry, **over)
    assert status == 200, payload
    return payload


def _abandon(repo, registry, *, reason="the spike answered its question",
             actor="brett", notebook=None, scope_id=TOPIC, **over):
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": scope_id}
    if reason is not None:
        body["reason"] = reason
    body.update(over)
    return gr.run_gate_action(
        "abandon-session", body, checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry, repository=repo.repository,
        session_notebook=notebook)


def _cleanup(repo, registry, *, ref=DRAFT, actor="brett", scope_id=TOPIC, **over):
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": scope_id, "ref": ref}
    body.update(over)
    return gr.run_gate_action(
        "cleanup-abandoned-branch", body, checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry, repository=repo.repository)


def _propose(repo, registry, *, topic_id=TOPIC, actor="brett"):
    return gr.run_gate_action(
        "propose", {"topic_id": topic_id}, checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry, repository=repo.repository)


def _session(repo, tmp_path, **over):
    """A live session with one document in it. Returns (registry, created, worktree)."""
    registry = _registry(repo, tmp_path, **over)
    created = _create(repo, registry)
    return registry, created, bs.worktree_path(repo.root, DRAFT)


def _land_proposal(repo, *, topic=TOPIC, change_id=CHANGE):
    """A LANDED proposal on the tile: the register's pick edge plus an ACTIVE
    change folder. Both halves are required — the pick names WHICH tile a change
    came from, and only an `active` change is demotable (`plan_demotion`)."""
    repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": repo.repository,
        "generation": {"source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-demo", "title": "Demo", "claim": "c", "state": "picked",
             "pick": {"staging_id": topic, "change_id": change_id}},
        ],
    }, sort_keys=False))
    repo.write(f"openspec/changes/{change_id}/proposal.md",
               "# Why\n\nA landed proposal for the tile.\n")
    # When this helper follows an abandon, pin the proposal commit to that
    # durable record's second-resolution timestamp. Git commits made from the
    # served checkout and Python records made around a session worktree can
    # otherwise observe a small clock skew and make an after-abandon fixture
    # look older. Equality is deliberately admissible ("no earlier than") and
    # the explicit older-evidence test below still proves the refusal boundary.
    abandon_records = sorted((repo.root / RECORDS).rglob(
        "abandon-session-*.gate-action.yaml"))
    recorded_at = None
    if abandon_records:
        abandonment = yaml.safe_load(
            abandon_records[-1].read_text(encoding="utf-8"))
        if isinstance(abandonment, dict) and isinstance(abandonment.get("at"), str):
            recorded_at = abandonment["at"]
    repo.commit("Land a proposal on the tile", "ideation/cross-reference.yaml",
                f"openspec/changes/{change_id}/proposal.md", at=recorded_at)


def _write_staged_origin(repo, folder, *, topic=TOPIC):
    repo.write(f"{folder}/.openspec.yaml", yaml.safe_dump({
        "schema": "spec-driven",
        "origin": {
            "kind": "staged",
            "id": f"{repo.repository}:staging:{topic}",
            "path": f"ideation/staging/{topic}",
        },
    }, sort_keys=False))


def _write_demotion_manifest(repo, *, topic=TOPIC, change_id=CHANGE):
    rel = (f"{RECORDS}{change_id}/demote-20260820T120000Z."
           "transition-manifest.yaml")
    repo.write(rel, yaml.safe_dump({
        "format_version": 1,
        "transition": "demote",
        "change_id": change_id,
        "destination": {
            "kind": "staged", "id": topic,
            "path": f"ideation/staging/{topic}",
        },
        "origin": {"kind": "change", "path": f"openspec/changes/{change_id}"},
        "transitioned_at": "2099-08-20T12:00:00Z",
        "files": [{
            "from": f"openspec/changes/{change_id}/proposal.md",
            "to": f"ideation/staging/{topic}/README.md",
        }],
    }, sort_keys=False))
    return rel


def _withdraw_proposal(repo, *, change_id=CHANGE):
    """What an EXECUTED demotion leaves behind: the change folder is gone
    (`remove-empty`) and the register's pick edge is withdrawn
    (`withdraw-picks`) — the two steps `gate_console.executable_plan` emits."""
    repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": repo.repository,
        "generation": {"source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-demo", "title": "Demo", "claim": "c", "state": "latent"},
        ],
    }, sort_keys=False))
    (repo.root / "openspec" / "changes" / change_id / "proposal.md").unlink()
    (repo.root / "openspec" / "changes" / change_id).rmdir()
    repo.git("add", "--", "ideation/cross-reference.yaml",
             f"openspec/changes/{change_id}")
    repo.git("commit", "-m", f"Demote {change_id} back to staging")


def _dispatch_propose(repo, *, topic=TOPIC, at="2026-07-26T09:00:00Z"):
    """A dispatched-and-undelivered `propose` workflow-job — the same artifact
    `propose`'s own duplicate guard reads (`kickoff.dispatched_propose_topics`)."""
    rel = f"{RECORDS}{topic}/propose-{gc._stamp(at)}.workflow-job.yaml"
    repo.write(rel, yaml.safe_dump(kickoff_mod.build_proposal_job(
        topic, workflow=kickoff_mod.DEFAULT_PROPOSAL_WORKFLOW,
        outline="author it", actor="brett", at=at), sort_keys=False))
    return rel


def _push(repo, branch):
    repo.git("push", "origin", branch)
    assert branch in repo.origin_branches()


def _abandon_records(repo):
    return sorted((repo.root / RECORDS).rglob("abandon-session-*.gate-action.yaml"))


def _teardown(repo, session, *, delete_branch=False, notebook=None):
    """The teardown as the OTHER ending reaches it (FR-021): Phase 7's merge verb
    is not built yet, so the merge ending is exercised through the shared teardown
    with the branch deletion FR-033 asks for."""
    return bs.teardown_session(
        sg.SessionGit(repo.root), session, checkout_root=repo.root,
        notebook=notebook, delete_branch=delete_branch)


def _open(repo, registry, *, scope_id=TOPIC, **over):
    git = sg.SessionGit(repo.root)
    tile = bs.Tile(bs.STAGED_TOPIC, scope_id)
    return bs.open_session(git, registry, repository=repo.repository, tile=tile,
                           checkout_root=repo.root, **over)


@contextmanager
def _serving(repo, snapshot_path, *, host="127.0.0.1", actor="tester"):
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, host=host,
                                   actor=actor)
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


def _console_token(host, port):
    """The per-serve human-console token (FR-019's third clause; PR #49 review
    finding 2), read the ONLY way the served page can read it — a same-origin
    `GET /capabilities`. A test that drives the route drives it as the CONSOLE
    does; the refusal for a caller that cannot is asserted in
    `test_session_confinement.py`."""
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("GET", "/capabilities")
    response = conn.getresponse()
    caps = json.loads(response.read().decode("utf-8"))
    conn.close()
    return caps.get("console_token")


def _post_raw(host, port, path, raw: bytes):
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(raw))}
    token = _console_token(host, port)
    if token:
        headers["X-XF-Console-Token"] = token
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("POST", path, body=raw, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    conn.close()
    return response.status, data


def _post(host, port, path, body):
    return _post_raw(host, port, path, json.dumps(body).encode("utf-8"))


# ==========================================================================
# T045 — abandon tears down, keeps the branch and the PR, and records WHY on main
# ==========================================================================

def test_abandon_tears_down_the_session_and_leaves_the_branch_and_pr_alone(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    notebook = FakeNotebookAdapter()
    notebook.create(bs.notebook_alias(REPO, DRAFT))       # Phase 8 does this at open
    pull_requests = FakePullRequests()
    _push(scratch_repo, DRAFT)                            # already-pushed history
    pull_requests.open_or_update(DRAFT, base="main", title="t", body="b")
    pull_requests.calls.clear()
    ahead = git.commits_ahead("main", DRAFT)
    head_before = git.head(ref=DRAFT)

    status, payload = _abandon(scratch_repo, registry, notebook=notebook,
                               reason="the spike answered its question")

    assert status == 200, payload
    assert payload["verb"] == "abandon-session"
    assert payload["ref"] == DRAFT
    assert payload["reason"] == "the spike answered its question"
    assert sorted(payload["torn_down"]) == ["notebook", "registry-entry", "worktree"]
    assert payload["branch_retained"] is True

    # torn down: the worktree directory, git's bookkeeping, the registry entry,
    # and the notebook — all three of FR-021's halves
    assert not worktree.exists()
    assert worktree not in git.worktree_paths()
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert registry.keys() == [(REPO, reg.DEFAULT_REF)]
    assert notebook.notebooks[bs.notebook_alias(REPO, DRAFT)].retired is True
    assert notebook.live_aliases() == ()

    # NOT torn down: the branch, its history, and the pull request. The port is
    # not even called — an abandon closes no PR on the human's behalf (FR-022).
    assert git.branch_exists(DRAFT) is True
    assert git.head(ref=DRAFT) == head_before
    assert git.commits_ahead("main", DRAFT) == ahead
    assert DRAFT in scratch_repo.origin_branches()
    assert pull_requests.calls == []
    assert pull_requests.open_prs[DRAFT].state == "open"


def test_the_abandon_record_is_main_resident_and_adds_no_commit_to_the_branch(
        scratch_repo, tmp_path):
    """Residence is the load-bearing half (plan Constraint 10): the reason-record
    is the artifact D17's reconciliation reads, and FR-028's cleanup DELETES the
    branch — so a branch-resident record would self-destruct."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    ahead = git.commits_ahead("main", DRAFT)
    head_before = git.head(ref=DRAFT)

    status, payload = _abandon(scratch_repo, registry, reason="wrong shape")

    assert status == 200, payload
    record_path = scratch_repo.root / payload["record"]
    assert record_path.is_file()                          # in the SERVED checkout
    assert payload["record"].startswith(RECORDS)
    assert _abandon_records(scratch_repo) == [record_path]

    record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
    assert record["kind"] == gc.RECORD_KIND
    assert record["action"] == gc.ACTION_ABANDON_SESSION
    assert record["actor"] == "brett"
    assert record["target"] == {"ref": DRAFT}
    assert record["reason"] == "wrong shape"
    # NO commit artifact, and no commit on the branch to carry one
    assert gc.ART_COMMIT not in [a["kind"] for a in record["artifacts"]]
    assert "commit" not in payload
    assert git.commits_ahead("main", DRAFT) == ahead
    assert git.head(ref=DRAFT) == head_before
    assert payload["record"] not in git.git(
        scratch_repo.root, "log", "--format=", "--name-only", DRAFT).split()


def test_the_abandon_reason_survives_the_fr028_branch_cleanup(scratch_repo,
                                                              tmp_path):
    """The discriminating assertion: delete the branch through the real FR-028
    route and read the reason back. A branch-resident record would be gone."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    abandoned = _abandon(scratch_repo, registry, reason="the approach was wrong")[1]
    _land_proposal(scratch_repo)                          # opens the cleanup window

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 200, payload
    assert payload["deleted"] is True
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False
    reread = yaml.safe_load(
        (scratch_repo.root / abandoned["record"]).read_text(encoding="utf-8"))
    assert reread["reason"] == "the approach was wrong"
    assert reread["target"]["ref"] == DRAFT


def test_abandon_with_no_live_session_refuses_and_tears_down_nothing(scratch_repo,
                                                                     tmp_path):
    registry = _registry(scratch_repo, tmp_path)
    before = scratch_repo.served_fingerprint()

    status, payload = _abandon(scratch_repo, registry)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "abandon" in payload["message"].lower()
    assert _abandon_records(scratch_repo) == []
    assert not (scratch_repo.container / "sessions").exists()
    assert scratch_repo.served_fingerprint() == before


def test_the_served_checkout_moves_only_inside_the_declared_records_path(
        scratch_repo, tmp_path):
    """SC-002: branch and HEAD byte-identical, and the porcelain differs only
    inside `ideation/dashboard/gate-records/` — which is why the fingerprint
    filters exactly that prefix."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    before = scratch_repo.served_fingerprint()

    _abandon(scratch_repo, registry, reason="enough for now")

    assert scratch_repo.served_fingerprint() == before
    raw = scratch_repo.git("status", "--porcelain", "--untracked-files=all")
    assert any(RECORDS in line for line in raw.splitlines())


def test_the_verbs_are_declared_and_dispatched(scratch_repo):
    assert "abandon-session" in gr.EXECUTING_VERBS
    assert "cleanup-abandoned-branch" in gr.EXECUTING_VERBS
    for verb in ("abandon-sessions", "cleanup-abandoned-branches"):
        status, payload = gr.run_gate_action(
            verb, {}, checkout_root=scratch_repo.root, actor="brett")
        assert status == 404 and payload["error"] == "unknown_verb"


# ==========================================================================
# T046 — the reason is required, and FR-019 holds on BOTH surfaces
# ==========================================================================

def test_a_blank_or_missing_reason_is_a_400_and_tears_down_nothing(scratch_repo,
                                                                   tmp_path):
    """FR-022: the reason is durable signal, like a demotion's. A 409 here would
    say the precondition was the session's; it is the body's."""
    registry, created, worktree = _session(scratch_repo, tmp_path)

    for reason in (None, "", "   ", "\n\t"):
        status, payload = _abandon(scratch_repo, registry, reason=reason)
        assert status == 400, repr(reason)
        assert payload["error"] == "invalid_body", repr(reason)
        assert "reason" in payload["message"], repr(reason)

    for raw in (7, ["why"], {"why": "x"}):                # not text at all
        status, payload = gr.run_gate_action(
            "abandon-session",
            {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "reason": raw},
            checkout_root=scratch_repo.root, actor="brett",
            session_registry=registry, repository=REPO)
        assert status == 400, repr(raw)
        assert payload["error"] == "invalid_body", repr(raw)

    assert worktree.is_dir()                              # nothing was torn down
    assert bs.is_live(registry, REPO, DRAFT) is True
    assert _abandon_records(scratch_repo) == []


def test_a_body_naming_no_tile_is_a_shaping_error(scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    for body in ({"reason": "x"},
                 {"scope_kind": bs.STAGED_TOPIC, "reason": "x"},
                 {"scope_id": TOPIC, "reason": "x"},
                 {"scope_kind": "not-a-kind", "scope_id": TOPIC, "reason": "x"}):
        status, payload = gr.run_gate_action(
            "abandon-session", body, checkout_root=scratch_repo.root,
            actor="brett", session_registry=registry, repository=REPO)
        assert status == 400, body
        assert payload["error"] == "invalid_body", body
    assert bs.is_live(registry, REPO, DRAFT) is True


def test_the_abandon_route_refuses_off_loopback_before_the_body_is_parsed(
        scratch_repo, tmp_path):
    """The body sent here is not even a JSON object: an `invalid_body` answer
    would prove the parse ran first, which is the ordering FR-019 forbids."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, served, host="0.0.0.0") as (host, port):
        shaped = _post(host, port, ABANDON_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "reason": "no"})
        unparseable = _post_raw(host, port, ABANDON_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "loopback_only", payload
    assert worktree.is_dir()
    assert _abandon_records(scratch_repo) == []


def test_the_abandon_route_fails_closed_with_no_resolved_actor(scratch_repo,
                                                               tmp_path,
                                                               monkeypatch):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)

    with _serving(scratch_repo, served, actor=None) as (host, port):
        shaped = _post(host, port, ABANDON_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "reason": "no"})
        unparseable = _post_raw(host, port, ABANDON_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "action_unavailable", payload
    assert worktree.is_dir()
    assert _abandon_records(scratch_repo) == []


def test_the_abandon_agent_path_is_rejected_before_anything_is_torn_down(
        scratch_repo, tmp_path):
    """Structural (D16): an `OutputBoundary` — the machinery/agent chokepoint —
    is refused by `require_human_gate` before the teardown is attempted, and the
    refusal is REPORTED on the offending object's own ledger."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = _open(scratch_repo, registry)
    agent = OutputBoundary(scratch_repo.root, [RECORDS], actor="agent")

    with pytest.raises(BoundaryViolation):
        gr.execute_abandon_session(agent, git, session=session, reason="nope",
                                   records_dir=RECORDS, checkout_root=scratch_repo.root)

    assert agent.refusals and agent.refusals[0].kind == "gate-side-effect"
    assert worktree.is_dir()
    assert bs.is_live(registry, REPO, DRAFT) is True
    assert _abandon_records(scratch_repo) == []


def test_the_abandon_cli_verb_enforces_the_human_gate_itself(scratch_repo,
                                                              tmp_path, capsys):
    """The CLI is a FRESH PROCESS with no `serve.py` handler in front of it, so
    FR-019 is a PER-VERB obligation here (contracts/cli.md)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    # the obligation is PER VERB, and it is discharged through one shared helper
    # the verb calls FIRST — before the session is resolved and before any write
    assert "_session_identity_gate" in inspect.getsource(
        cli_mod.cmd_gate_abandon_session)
    assert "require_human_gate" in inspect.getsource(
        cli_mod._session_identity_gate)

    with pytest.raises(SystemExit) as exited:                # missing --actor
        cli_mod.main(["gate", "abandon-session", "--repo-root",
                      str(scratch_repo.root), "--scope-kind", bs.STAGED_TOPIC,
                      "--scope-id", TOPIC, "--reason", "no"])
    assert exited.value.code != 0
    assert worktree.is_dir()

    capsys.readouterr()
    rc = cli_mod.main(["gate", "abandon-session", "--repo-root",
                       str(scratch_repo.root), "--actor", "   ",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--reason", "no"])
    assert rc == 1
    assert "refused" in capsys.readouterr().err
    assert worktree.is_dir()
    assert _abandon_records(scratch_repo) == []


def test_the_abandon_cli_verb_tears_the_session_down_and_reports_it(scratch_repo,
                                                                     tmp_path,
                                                                     capsys,
                                                                     fake_cli_notebook):
    """CLI parity (FR-020, quickstart step 5): a fresh process re-derives its own
    session registry (T033a) — without that a CLI verb sees no session at all.

    `fake_cli_notebook` is load-bearing: the abandon RETIRES the session notebook
    (T074, FR-021, D16), so with no fake at `cli._notebook_port` this test ran real
    `nlm notebook list` and would have run `notebook delete --confirm` by TITLE
    MATCH against the shared account (FR-043; PR #49 finding 17). Injected, the
    retire is asserted rather than escaping."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    capsys.readouterr()

    rc = cli_mod.main(["gate", "abandon-session", "--repo-root",
                       str(scratch_repo.root), "--actor", "dana",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--reason", "spike only"])

    assert rc == 0
    out = capsys.readouterr().out
    assert DRAFT in out
    assert "RETAINED" in out
    assert not worktree.exists()
    records = _abandon_records(scratch_repo)
    assert len(records) == 1
    record = yaml.safe_load(records[0].read_text(encoding="utf-8"))
    assert record["actor"] == "dana"
    assert record["reason"] == "spike only"
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True
    # the notebook is RETIRED through the INJECTED port, by the session's own
    # alias — and nothing else on the account is touched (FR-021, D16)
    alias = bs.notebook_alias(REPO, DRAFT)
    assert fake_cli_notebook.calls == [("retire", alias)]


def test_the_cli_offers_no_bypass_flag_for_the_endings():
    parser = cli_mod.build_parser()
    args = parser.parse_args(["gate", "abandon-session", "--repo-root", ".",
                              "--actor", "brett", "--scope-kind",
                              bs.STAGED_TOPIC, "--scope-id", TOPIC,
                              "--reason", "why"])
    assert args.func is cli_mod.cmd_gate_abandon_session
    assert args.records_dir == gc.DEFAULT_RECORDS_DIR       # _add_gate_identity_args
    with pytest.raises(SystemExit):                         # --reason is required
        parser.parse_args(["gate", "abandon-session", "--repo-root", ".",
                           "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
                           "--scope-id", TOPIC])
    cleanup = parser.parse_args(["gate", "cleanup-abandoned-branch",
                                 "--repo-root", ".", "--actor", "brett",
                                 "--scope-kind", bs.STAGED_TOPIC,
                                 "--scope-id", TOPIC, "--ref", DRAFT])
    assert cleanup.func is cli_mod.cmd_gate_cleanup_abandoned_branch
    with pytest.raises(SystemExit):                         # --ref is required
        parser.parse_args(["gate", "cleanup-abandoned-branch", "--repo-root", ".",
                           "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
                           "--scope-id", TOPIC])


# ==========================================================================
# T047 — `propose` is gated by the LIVE SESSION, never by the branch (FR-023)
# ==========================================================================

def test_propose_refuses_while_a_session_is_live_and_persists_nothing(scratch_repo,
                                                                      tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    before = scratch_repo.served_fingerprint()

    status, payload = _propose(scratch_repo, registry)

    assert status == 409
    assert payload["error"] == "gate_refused"
    message = payload["message"]
    assert DRAFT in message                               # names the branch
    assert "open-pr" in message and "merge" in message.lower()   # resolution 1
    assert "abandon" in message                                  # resolution 2
    # nothing persisted: no job, no record, and the session untouched
    assert list((scratch_repo.root / RECORDS).rglob("propose-*.workflow-job.yaml")) == []
    assert list((scratch_repo.root / RECORDS).rglob("propose-*.gate-action.yaml")) == []
    assert bs.is_live(registry, REPO, DRAFT) is True
    assert scratch_repo.served_fingerprint() == before


def test_propose_refuses_when_the_live_session_is_an_ordinal_branch(scratch_repo,
                                                                    tmp_path):
    """FR-023 keys on the tile's LIVE session, and after a NEW continuation that
    session lives at `draft/<topic>-2`. A refusal that only looked at the
    deterministic name would let `propose` walk straight over it."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    second = _create(scratch_repo, registry, continuation=bs.CONTINUATION_NEW)
    assert second["ref"] == f"{DRAFT}-2"

    status, payload = _propose(scratch_repo, registry)

    assert status == 409
    assert f"{DRAFT}-2" in payload["message"]


def test_propose_proceeds_once_the_session_ends_by_the_merge_route(scratch_repo,
                                                                   tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    session = _open(scratch_repo, registry)
    _teardown(scratch_repo, session, delete_branch=True)   # the merge ending

    status, payload = _propose(scratch_repo, registry)

    assert status == 200, payload
    assert payload["topic_id"] == TOPIC
    assert (scratch_repo.root / payload["job"]).is_file()
    assert (scratch_repo.root / payload["record"]).is_file()


def test_propose_proceeds_after_an_abandon_even_though_the_branch_survives(
        scratch_repo, tmp_path):
    """FR-023's sharpest clause: the refusal keys on the live SESSION, not on
    branch existence — a surviving abandoned branch is evidence, not unresolved
    working state (US4 scenario 3)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _push(scratch_repo, DRAFT)
    _abandon(scratch_repo, registry, reason="parked")
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(DRAFT) is True                # the branch SURVIVES

    status, payload = _propose(scratch_repo, registry)

    assert status == 200, payload
    assert git.branch_exists(DRAFT) is True                # and propose kept it
    assert DRAFT in scratch_repo.origin_branches()


def test_the_pre_existing_propose_refusals_still_hold(scratch_repo, tmp_path):
    """FR-023 adds ONE precondition; it removes none."""
    registry = _registry(scratch_repo, tmp_path)

    missing = _propose(scratch_repo, registry, topic_id="no-such-topic")
    assert missing[0] == 409 and "no staging topic" in missing[1]["message"]

    first = _propose(scratch_repo, registry)
    assert first[0] == 200, first[1]
    duplicate = _propose(scratch_repo, registry)
    assert duplicate[0] == 409
    assert "dispatched" in duplicate[1]["message"]
    assert len(list((scratch_repo.root / RECORDS).rglob(
        "propose-*.workflow-job.yaml"))) == 1

    agent = OutputBoundary(scratch_repo.root, [RECORDS], actor="agent")
    with pytest.raises(BoundaryViolation):
        kickoff_mod.propose(agent, TOPIC, records_dir=RECORDS)
    assert agent.refusals and agent.refusals[0].kind == "gate-side-effect"


def test_the_propose_cli_verb_refuses_while_a_session_is_live(scratch_repo,
                                                              tmp_path, capsys):
    """Quickstart step 5's first command. A CLI verb is its own process, so it
    re-derives the registry (T033a) before answering the liveness question —
    without that, `propose` would proceed over unmerged drafts (the D15 hazard)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    capsys.readouterr()

    rc = cli_mod.main(["gate", "propose", "--repo-root", str(scratch_repo.root),
                       "--actor", "brett", "--topic-id", TOPIC])

    assert rc == 1
    err = capsys.readouterr().err
    assert DRAFT in err
    assert "abandon" in err
    assert list((scratch_repo.root / RECORDS).rglob("propose-*.workflow-job.yaml")) == []


# ==========================================================================
# T048 — a tile carrying a live proposal is closed to session work (FR-024)
# ==========================================================================

def test_a_gate_write_on_a_proposed_tile_opens_nothing_and_names_demote(
        scratch_repo, tmp_path):
    registry = _registry(scratch_repo, tmp_path)
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    before = scratch_repo.served_fingerprint()

    status, payload = _create_raw(scratch_repo, registry)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "demote" in payload["message"]
    assert CHANGE in payload["message"]
    # nothing opened, nothing persisted
    assert git.branch_exists(DRAFT) is False
    assert not (scratch_repo.container / "sessions").exists()
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert scratch_repo.served_fingerprint() == before


def test_a_first_edit_on_a_proposed_tile_opens_nothing_and_names_demote(
        scratch_repo, tmp_path):
    """FR-024's missing arm (T104 final queue Q-1, ruled FIX-FIRST
    2026-08-09). The doxBench Save is a session-OPENING gesture exactly like
    `create-document`, so a proposed tile must refuse it with the same
    demote message — instead of opening a session that no verb can then
    save or abandon (the verb-orphan reproduced live by the T098 smoke:
    every session verb refused on the tile while its session stood open).
    The route used to call `execute_first_edit` without deriving the
    proposal state, so `assert_no_live_proposal(None, …)` returned
    immediately — the F4 class: a parameter discarded at its only
    production call site."""
    registry = _registry(scratch_repo, tmp_path)
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    before = scratch_repo.served_fingerprint()

    document = f"ideation/staging/{TOPIC}/README.md"
    # the SERVED bytes through the production lens (strict decode, no newline
    # translation) — `read_text` would silently normalize a CRLF fixture into
    # a hash no real client sends (Copilot review finding on this PR; the
    # W-7 class, where LF-only fixtures mask the divergence)
    base = doxbench_hash.served_text(
        (scratch_repo.root / document).read_bytes())
    status, payload = gr.run_gate_action(
        "first-edit",
        {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
         "document": document,
         "content": staging_fragment("Demo Topic", TOPIC) + "\nSaved.\n",
         "base_hash": doxbench_hash.content_identity(base).hex},
        checkout_root=scratch_repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=scratch_repo.repository)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "demote" in payload["message"]
    assert CHANGE in payload["message"]
    # nothing opened, nothing persisted — the create-document twin, verbatim
    assert git.branch_exists(DRAFT) is False
    assert not (scratch_repo.container / "sessions").exists()
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert scratch_repo.served_fingerprint() == before


def test_a_dispatched_and_undelivered_propose_says_the_proposal_has_not_landed(
        scratch_repo, tmp_path):
    """D20's distinct message: naming `demote` would name a route the human
    cannot take, because nothing has landed to demote."""
    registry = _registry(scratch_repo, tmp_path)
    _dispatch_propose(scratch_repo)

    status, payload = _create_raw(scratch_repo, registry)

    assert status == 409
    message = payload["message"]
    assert "not landed" in message
    assert "demote" not in message
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False


def test_after_a_demotion_the_tile_opens_a_session_normally(scratch_repo,
                                                            tmp_path):
    registry = _registry(scratch_repo, tmp_path)
    _land_proposal(scratch_repo)
    assert _create_raw(scratch_repo, registry)[0] == 409

    _withdraw_proposal(scratch_repo)

    created = _create(scratch_repo, registry)
    assert created["ref"] == DRAFT
    assert created["joined"] is False
    assert bs.is_live(registry, REPO, DRAFT) is True


def test_the_landed_half_reads_the_register_pick_and_the_change_status(
        scratch_repo, tmp_path):
    """The derivation, stated: a tile carries a live proposal when the register's
    pick edge names it AND that change is ACTIVE. An archived change is not a live
    proposal (there is nothing to demote — `plan_demotion` refuses it)."""
    _land_proposal(scratch_repo)
    assert bs.landed_proposal_ids(scratch_repo.root) == {TOPIC: CHANGE}

    archive = scratch_repo.root / "openspec" / "changes" / "archive" / f"2026-07-26-{CHANGE}"
    archive.parent.mkdir(parents=True, exist_ok=True)
    (scratch_repo.root / "openspec" / "changes" / CHANGE).rename(archive)
    assert bs.landed_proposal_ids(scratch_repo.root) == {}


# ==========================================================================
# T049 — RESUME or NEW, never a silently chosen name (FR-025, FR-026, FR-027)
# ==========================================================================

def test_resume_or_new_is_offered_on_a_tile_whose_abandoned_branch_survives(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    git = sg.SessionGit(scratch_repo.root)

    status, payload = _create_raw(scratch_repo, registry)

    assert status == 409
    message = payload["message"]
    assert DRAFT in message                                # reports the branch
    assert "resume" in message.lower()                     # continuation 1
    assert f"{DRAFT}-2" in message                         # continuation 2, named
    # and nothing was chosen: no second branch, no worktree, no session
    assert git.local_ordinals(DRAFT) == (DRAFT,)
    assert not worktree.exists()
    assert bs.is_live(registry, REPO, DRAFT) is False


def test_resume_re_materializes_a_worktree_over_the_existing_branch(scratch_repo,
                                                                     tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    head_before = git.head(ref=DRAFT)
    _abandon(scratch_repo, registry, reason="back in a bit")

    resumed = _create(scratch_repo, registry, title="Second Draft",
                      continuation=bs.CONTINUATION_RESUME)

    assert resumed["ref"] == DRAFT                          # the EXISTING name
    assert worktree.is_dir()
    assert bs.is_live(registry, REPO, DRAFT) is True
    # the branch kept its history: the resumed session builds ON the abandoned work
    assert git.head(ref=DRAFT) != head_before
    assert git.commits_ahead("main", DRAFT) == 2
    assert (worktree / created["path"]).is_file()           # the first document
    assert git.local_ordinals(DRAFT) == (DRAFT,)            # no second branch


def test_new_allocates_the_next_ordinal_against_a_surviving_local_branch(
        scratch_repo, tmp_path):
    """T049 case (a) — the NEVER-PUSHED abandon. Nothing pushes before `open-pr`,
    so a remote-only ordinal scan would collide with the surviving LOCAL branch."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    assert DRAFT not in scratch_repo.origin_branches()      # never pushed

    fresh = _create(scratch_repo, registry, title="Fresh Start",
                    continuation=bs.CONTINUATION_NEW)

    assert fresh["ref"] == f"{DRAFT}-2"
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(f"{DRAFT}-2") is True
    assert git.branch_exists(DRAFT) is True                 # the abandoned one stays
    assert git.commits_ahead("main", f"{DRAFT}-2") == 1     # forked from main
    assert bs.worktree_path(scratch_repo.root, f"{DRAFT}-2").is_dir()
    assert not worktree.exists()                            # and NOT the old one
    assert bs.is_live(registry, REPO, f"{DRAFT}-2") is True


def test_new_allocates_above_a_branch_that_exists_only_on_the_remote(scratch_repo,
                                                                      tmp_path):
    """T049 case (b) — the REMOTE-ONLY branch (D17's two-machine race). Created
    inside the bare origin with `git update-ref` and NEVER fetched, so this is the
    only fixture that discriminates a real `ls-remote` from local-ref reading."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    scratch_repo.add_remote_only_branch(f"{DRAFT}-2")
    assert f"{DRAFT}-2" not in scratch_repo.local_branches()

    fresh = _create(scratch_repo, registry, title="Third Time",
                    continuation=bs.CONTINUATION_NEW)

    assert fresh["ref"] == f"{DRAFT}-3"
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(f"{DRAFT}-3") is True
    assert git.branch_exists(f"{DRAFT}-2") is False          # still remote-only
    assert f"{DRAFT}-2" in scratch_repo.origin_branches()


def test_a_live_cross_tile_ordinal_branch_is_neither_resumed_nor_consumed(
        tmp_path):
    """T049 case (c) — G12 at the LIFECYCLE level. `draft/demo-topic-2` is tile
    `demo-topic-2`'s OWN first branch: tile `demo-topic` must neither resume it as
    its own session nor consume it as its ordinal."""
    repo = build_scratch_repo(tmp_path, extra_topics=("demo-topic-2",))
    registry = _registry(repo, tmp_path)
    other = _create(repo, registry, scope_id="demo-topic-2",
                    area="ideation/staging/demo-topic-2/", title="Other Tile")
    assert other["ref"] == f"{DRAFT}-2"
    mine = _create(repo, registry)                          # tile demo-topic
    assert mine["ref"] == DRAFT
    other_worktree = bs.worktree_path(repo.root, f"{DRAFT}-2")
    _abandon(repo, registry, reason="parked")               # abandons demo-topic

    offered = _create_raw(repo, registry)
    assert offered[0] == 409
    assert DRAFT in offered[1]["message"]
    assert f"{DRAFT}-3" in offered[1]["message"]            # the NEW name SKIPS -2

    fresh = _create(repo, registry, continuation=bs.CONTINUATION_NEW)
    assert fresh["ref"] == f"{DRAFT}-3"

    # the other tile's session is untouched: same branch, same worktree, still live
    assert bs.is_live(registry, repo.repository, f"{DRAFT}-2") is True
    assert other_worktree.is_dir()
    assert (other_worktree / other["path"]).is_file()
    git = sg.SessionGit(repo.root)
    assert git.commits_ahead("main", f"{DRAFT}-2") == 1


def test_a_second_writer_after_the_choice_joins_instead_of_seeing_the_prompt(
        scratch_repo, tmp_path):
    """FR-027: once either continuation has opened a session, every later writer
    JOINS it — otherwise concurrent writers could answer the prompt differently
    and fork one tile into two sessions (D17's second trap)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    fresh = _create(scratch_repo, registry, continuation=bs.CONTINUATION_NEW)

    second = _create(scratch_repo, registry, title="Joined Draft", actor="dana")

    assert second["ref"] == f"{DRAFT}-2"
    assert second["joined"] is True
    git = sg.SessionGit(scratch_repo.root)
    assert git.local_ordinals(DRAFT) == (DRAFT, f"{DRAFT}-2")
    assert git.commits_ahead("main", f"{DRAFT}-2") == 2      # both documents
    # `keys()` is a SORTED roster, so the session ref sorts before `main`
    assert registry.keys() == [(REPO, f"{DRAFT}-2"), (REPO, reg.DEFAULT_REF)]


# --------------------------------------------------------------------------
# second-review finding 6 — the G12 exclusion is not applied to LIVENESS
#
# Applied to ALLOCATION the exclusion is right (T049(c) above). Applied to
# LIVENESS it hid a tile's OWN live session the moment a SIBLING TILE spelling
# that ordinal entered the inventory — a new staging folder is enough — and the
# next write forked the tile into two live sessions whose first one could then be
# neither saved, abandoned nor cleaned up. Ownership is now recorded by the OPEN
# (registry entry + a durable container marker for the next process) instead of
# guessed from the ref.
# --------------------------------------------------------------------------

def _grow_the_inventory(repo, topic: str):
    """A SIBLING TILE appears whose deterministic branch spells the live session's
    ordinal name. A staging folder is all it takes — no collision, no minting."""
    rel = f"ideation/staging/{topic}/README.md"
    repo.write(rel, f"# {topic}\n\nStatus: staged\n")
    repo.commit(f"Stage {topic}", rel)


def test_a_tiles_own_ordinal_session_survives_a_sibling_tile_appearing(
        scratch_repo, tmp_path):
    """The reproduction, inverted. Tile `demo-topic`'s session is at
    `draft/demo-topic-2`; staging `demo-topic-2` then makes that ordinal ALSO a
    sibling tile's deterministic name. The session must stay this tile's."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    ordinal = _create(scratch_repo, registry, continuation=bs.CONTINUATION_NEW)
    assert ordinal["ref"] == f"{DRAFT}-2"
    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)
    inventory = gr.discover_tile_inventory(scratch_repo.root)
    assert bs.live_session_branches(registry, REPO, tile,
                                    inventory=inventory) == (f"{DRAFT}-2",)

    _grow_the_inventory(scratch_repo, "demo-topic-2")
    grown = gr.discover_tile_inventory(scratch_repo.root)
    assert bs.Tile(bs.STAGED_TOPIC, "demo-topic-2") in grown.tiles

    # the tile's own session is STILL live and still its own
    assert bs.live_session_branches(registry, REPO, tile,
                                    inventory=grown) == (f"{DRAFT}-2",)
    # ... so the next write JOINS it instead of forking a second live session
    joined = _create(scratch_repo, registry, title="Later Work")
    assert joined["ref"] == f"{DRAFT}-2"
    assert joined["joined"] is True
    assert [key for key in registry.keys() if key[1] != reg.DEFAULT_REF] == \
        [(REPO, f"{DRAFT}-2")], "one tile, ONE live session (FR-003)"
    # and `propose` is still refused by it (FR-023, D15)
    status, payload = _propose(scratch_repo, registry)
    assert status == 409, payload
    assert f"{DRAFT}-2" in payload["message"]


def test_the_owner_marker_carries_the_answer_into_the_next_process(scratch_repo,
                                                                  tmp_path):
    """Every CLI-parity verb is a fresh process, and the FR-008 bootstrap re-derives
    liveness from WORKTREES — which name a branch and never a tile. The owner marker
    is what makes the re-derived entry say whose session it is."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    assert _create(scratch_repo, registry,
                   continuation=bs.CONTINUATION_NEW)["ref"] == f"{DRAFT}-2"
    _grow_the_inventory(scratch_repo, "demo-topic-2")
    assert bs.read_owner_marker(scratch_repo.root, f"{DRAFT}-2") == \
        (bs.STAGED_TOPIC, TOPIC)

    fresh = reg.SnapshotRegistry()                   # a NEW process's registry
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)

    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)
    grown = gr.discover_tile_inventory(scratch_repo.root)
    assert bs.recorded_session_tile(fresh, REPO, f"{DRAFT}-2") == \
        (bs.STAGED_TOPIC, TOPIC)
    assert bs.live_session_branches(fresh, REPO, tile,
                                    inventory=grown) == (f"{DRAFT}-2",)


def test_the_session_base_is_recorded_at_open_and_survives_the_next_process(
        scratch_repo, tmp_path):
    """T104 R-12 (reviewer ruling 2026-08-02): the OPEN is the one place the
    branch point is known, so it records `(base_ref, base_revision)` on the
    entry and durably in the same marker the owner rides; the FR-008
    bootstrap re-derives it, and a marker that predates the base keys
    recovers from git's own fork point. This is what lets the chat-turn
    binding check accept a buffer still based on the pre-session ref after
    any restart."""
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    fork = sg.SessionGit(scratch_repo.root).head(ref="main")

    entry = registry.get(REPO, DRAFT)
    assert entry is not None and entry.session_base == ("main", fork)
    assert bs.read_base_marker(scratch_repo.root, DRAFT) == ("main", fork)

    fresh = reg.SnapshotRegistry()                   # a NEW process's registry
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)
    rederived = fresh.get(REPO, DRAFT)
    assert rederived is not None and rederived.session_base == ("main", fork)

    # a marker WITHOUT the base keys (a session opened before this wave)
    # degrades to git's fork point, not to a failure
    bs.write_owner_marker(scratch_repo.root, DRAFT,
                          bs.Tile(bs.STAGED_TOPIC, TOPIC))
    assert bs.read_base_marker(scratch_repo.root, DRAFT) is None
    recovered = reg.SnapshotRegistry()
    bs.bootstrap_sessions(recovered, repository=REPO,
                          checkout_root=scratch_repo.root)
    entry = recovered.get(REPO, DRAFT)
    assert entry is not None and entry.session_base == ("main", fork)


def test_a_fresh_open_prefers_gits_fork_point_over_a_crash_orphaned_marker(
        scratch_repo, tmp_path):
    """Wave re-review (R-12 machinery): the fresh-open arm consulted the
    marker FIRST, so a crash-orphaned marker — a previous session of the same
    deterministic branch name, ended by hand without `clear_owner_marker` —
    was read back as the NEW session's base and re-persisted by the register:
    the record was wrong and self-healing never occurred. The arms that JUST
    created (or re-materialized) the branch now prefer git's own fork point,
    stale marker ALIASES are distrusted whenever the marker's base disagrees
    with the recovered one, and the register heals the marker."""
    registry = _registry(scratch_repo, tmp_path)
    bs.write_owner_marker(scratch_repo.root, DRAFT,
                          bs.Tile(bs.STAGED_TOPIC, TOPIC),
                          base=("main", "f" * 40), base_aliases=("e" * 40,))
    _create(scratch_repo, registry)

    fork = sg.SessionGit(scratch_repo.root).head(ref="main")
    entry = registry.get(REPO, DRAFT)
    assert entry is not None and entry.session_base == ("main", fork)
    assert "e" * 40 not in entry.session_base_aliases
    # the marker is healed to the truth the open just derived
    assert bs.read_base_marker(scratch_repo.root, DRAFT) == ("main", fork)


def test_the_serving_snapshots_revision_is_recorded_as_a_base_alias(
        scratch_repo, tmp_path):
    """W-4 (wave re-review): a real client's `base_revision` is the serving
    snapshot's generation-time HEAD — the browser never receives a per-file
    revision — while the branch point is the OPEN-time HEAD. When main moves
    between snapshot bake and session open, the two differ forever, and
    R-12's revision-equality acceptance silently reverted to the refusal it
    closed (executed in the re-review, both directions). The OPEN now
    records the serving snapshot's revision beside the merge-base, durably:
    it can never be re-derived later, because the snapshot regenerates."""
    registry = _registry(scratch_repo, tmp_path)
    snap_rev = registry.get(REPO, reg.DEFAULT_REF).source_revision

    # main moves AFTER the snapshot is baked and BEFORE the session opens —
    # the exact window that reverted R-12 on a real plane
    scratch_repo.write("ideation/brainstorm/later-note.md",
                       "Status: brainstorm\n\n# Later\n")
    scratch_repo.commit("Advance main past the baked snapshot",
                        "ideation/brainstorm/later-note.md")
    _create(scratch_repo, registry)

    fork = sg.SessionGit(scratch_repo.root).head(ref="main")
    assert fork != snap_rev, "the window under test requires real movement"
    entry = registry.get(REPO, DRAFT)
    assert entry is not None and entry.session_base == ("main", fork)
    assert entry.session_base_aliases == (snap_rev,)
    assert bs.read_base_marker_aliases(scratch_repo.root, DRAFT) == (snap_rev,)

    # the alias survives the next process — read back from the marker, never
    # re-derived from a snapshot that has since regenerated
    fresh = reg.SnapshotRegistry()
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)
    rederived = fresh.get(REPO, DRAFT)
    assert rederived is not None
    assert rederived.session_base_aliases == (snap_rev,)


def test_an_ownerless_live_ordinal_is_an_ambiguity_and_never_an_absence(
        scratch_repo, tmp_path):
    """With no owner recorded anywhere — a session that predates the marker, or a
    container that could not hold it — the two readings of `draft/demo-topic-2` are
    indistinguishable. The one answer that must not be given is "no live session",
    because that is what opened a second one over it: it refuses, naming both tiles
    and the live branch."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="restarting")
    assert _create(scratch_repo, registry,
                   continuation=bs.CONTINUATION_NEW)["ref"] == f"{DRAFT}-2"
    _grow_the_inventory(scratch_repo, "demo-topic-2")
    bs.clear_owner_marker(scratch_repo.root, f"{DRAFT}-2")
    fresh = reg.SnapshotRegistry()
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)
    assert bs.recorded_session_tile(fresh, REPO, f"{DRAFT}-2") is None

    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)
    grown = gr.discover_tile_inventory(scratch_repo.root)
    with pytest.raises(bs.CrossTileCollision) as caught:
        bs.live_session_branches(fresh, REPO, tile, inventory=grown)

    message = str(caught.value)
    assert f"{DRAFT}-2" in message
    assert TOPIC in message and "demo-topic-2" in message
    assert "LIVE" in message


def test_a_declared_continuation_never_forks_a_live_session(scratch_repo,
                                                             tmp_path):
    """The same suppression from the other side: a stale prompt answered while a
    session is live JOINS rather than allocating a second branch."""
    registry, created, worktree = _session(scratch_repo, tmp_path)

    joined = _create(scratch_repo, registry, title="Late Answer",
                     continuation=bs.CONTINUATION_NEW)

    assert joined["ref"] == DRAFT
    assert joined["joined"] is True
    assert sg.SessionGit(scratch_repo.root).branch_exists(f"{DRAFT}-2") is False


def test_a_merged_tile_is_reworked_with_no_prompt_at_all(scratch_repo, tmp_path):
    """FR-033 deletes the branch at the merge, so the tile's next session is an
    ordinary OPEN under the deterministic name — no prompt, no ordinal."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    session = _open(scratch_repo, registry)
    _teardown(scratch_repo, session, delete_branch=True)     # the merge ending
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(DRAFT) is False

    reworked = _create(scratch_repo, registry, title="Rework")

    assert reworked["ref"] == DRAFT                          # NOT `-2`
    assert reworked["joined"] is False
    assert git.commits_ahead("main", DRAFT) == 1
    assert git.branch_exists(f"{DRAFT}-2") is False


def test_an_unknown_continuation_is_a_shaping_error(scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")

    status, payload = _create_raw(scratch_repo, registry, continuation="RESUME!")

    assert status == 400
    assert payload["error"] == "invalid_body"
    assert "resume" in payload["message"] and "new" in payload["message"]


def test_a_continuation_with_nothing_to_continue_from_refuses(scratch_repo,
                                                               tmp_path):
    """A prompt answered after the branch is gone (a cleanup landed in between)
    refuses rather than allocating `-2` over a free deterministic name."""
    registry = _registry(scratch_repo, tmp_path)

    for continuation in (bs.CONTINUATION_RESUME, bs.CONTINUATION_NEW):
        status, payload = _create_raw(scratch_repo, registry,
                                      continuation=continuation)
        assert status == 409, continuation
        assert "no abandoned session branch" in payload["message"], continuation
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False


# ==========================================================================
# T050 — FR-024 wins over the prompt
# ==========================================================================

def test_the_prompt_is_not_offered_on_a_proposed_tile_with_an_abandoned_branch(
        scratch_repo, tmp_path):
    """US4 scenario 9: a tile carrying BOTH a live proposal and a surviving
    abandoned branch is closed to session work — the branch is not resumed and no
    ordinal is offered."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)

    status, payload = _create_raw(scratch_repo, registry)

    assert status == 409
    message = payload["message"]
    assert "demote" in message
    assert "resume" not in message.lower()
    assert f"{DRAFT}-2" not in message
    assert git.local_ordinals(DRAFT) == (DRAFT,)             # nothing allocated
    assert not worktree.exists()                             # nothing resumed


def test_an_explicit_resume_on_a_proposed_tile_refuses_with_the_resume_wording(
        scratch_repo, tmp_path):
    """FR-024 covers open AND resume, and the refusal says which one it refused."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)

    status, payload = _create_raw(scratch_repo, registry,
                                  continuation=bs.CONTINUATION_RESUME)

    assert status == 409
    assert "resumed" in payload["message"]
    assert "demote" in payload["message"]
    assert not worktree.exists()


# ==========================================================================
# T051 — the cleanup is human-invoked, and only after the proposal EXISTS
# ==========================================================================

def test_cleanup_is_refused_while_the_topic_has_no_proposal(scratch_repo,
                                                             tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "retention" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_cleanup_is_refused_while_only_a_propose_dispatch_exists(scratch_repo,
                                                                 tmp_path):
    """FR-028's sharpest clause: a `propose` DISPATCH is a commission, not a
    proposal — its authoring may never deliver one, so the branch stays."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    proposed = _propose(scratch_repo, registry)
    assert proposed[0] == 200, proposed[1]                   # the dispatch lands

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409
    assert "not landed" in payload["message"]
    # and the dispatch itself deleted nothing: cleanup is never automatic
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_cleanup_deletes_the_branch_once_the_proposal_exists(scratch_repo,
                                                              tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    before = scratch_repo.served_fingerprint()

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 200, payload
    assert payload["verb"] == "cleanup-abandoned-branch"
    assert payload["ref"] == DRAFT
    assert payload["deleted"] is True
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False
    assert scratch_repo.served_fingerprint() == before
    # the attestation is now a REPORT of verified evidence (second-review finding 3)
    assert "abandon-session-" in payload["abandon_proof"]
    assert payload["abandon_proof"] in payload["hint"]
    assert payload["retention_release"]["kind"] == bs.RETENTION_ACTIVE_PROPOSAL
    assert len(payload["pre_delete_head"]) == 40
    cleanup_record = scratch_repo.root / payload["record"]
    loaded = yaml.safe_load(cleanup_record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_CLEANUP_ABANDONED_BRANCH
    assert loaded["cleanup"]["pre_delete_head"] == payload["pre_delete_head"]
    assert loaded["cleanup"]["status"] == "completed"
    assert loaded["cleanup"]["retention_release"]["scope_id"] == TOPIC


def test_matching_proposal_evidence_from_before_abandonment_requires_fresh_release(
        scratch_repo, tmp_path, monkeypatch):
    archived = f"openspec/changes/archive/2026-08-20-{CHANGE}"
    _write_staged_origin(scratch_repo, archived)
    scratch_repo.write(f"{archived}/proposal.md", "# Older archived proposal\n")
    scratch_repo.commit(
        "Archive older proposal custody",
        f"{archived}/.openspec.yaml", f"{archived}/proposal.md")
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    monkeypatch.setattr(gc, "_utcnow", lambda: "2099-08-25T12:00:00Z")
    _abandon(scratch_repo, registry, reason="parked after older proposal work")

    status, payload = _cleanup(scratch_repo, registry)
    assert status == 409, payload
    assert "before the session was abandoned" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True

    status, payload = _cleanup(
        scratch_repo, registry,
        retention_release_reason="reviewed the exact abandoned head separately")
    assert status == 200, payload
    assert payload["retention_release"]["kind"] == bs.RETENTION_EXPLICIT_HUMAN


def test_branch_advanced_after_abandonment_requires_explicit_current_head_release(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    abandoned_head = sg.SessionGit(scratch_repo.root).branch_sha(DRAFT)
    _land_proposal(scratch_repo)
    advanced_head = scratch_repo.head("main")
    scratch_repo.git(
        "update-ref", f"refs/heads/{DRAFT}", advanced_head, abandoned_head)

    status, payload = _cleanup(scratch_repo, registry)
    assert status == 409, payload
    assert "branch now points" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_sha(DRAFT) == advanced_head

    status, payload = _cleanup(
        scratch_repo, registry,
        retention_release_reason="reviewed and released the advanced current head")
    assert status == 200, payload
    assert payload["pre_delete_head"] == advanced_head


def test_active_declared_origin_releases_cleanup_without_a_pick_edge(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _write_staged_origin(scratch_repo, f"openspec/changes/{CHANGE}")
    scratch_repo.write(f"openspec/changes/{CHANGE}/proposal.md", "# Why\n")
    scratch_repo.commit(
        "Record proposal custody after abandonment",
        f"openspec/changes/{CHANGE}/.openspec.yaml",
        f"openspec/changes/{CHANGE}/proposal.md")

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 200, payload
    evidence = payload["retention_release"]
    assert evidence["kind"] == bs.RETENTION_ACTIVE_PROPOSAL
    assert evidence["change_id"] == CHANGE
    assert evidence["references"] == [f"openspec/changes/{CHANGE}/.openspec.yaml"]


def test_archived_exact_origin_releases_cleanup_after_the_tile_disappears(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    archived = f"openspec/changes/archive/2026-08-20-{CHANGE}"
    _write_staged_origin(scratch_repo, archived)
    scratch_repo.write(f"{archived}/proposal.md", "# Archived proposal\n")
    scratch_repo.commit(
        "Archive proposal custody after abandonment",
        f"{archived}/.openspec.yaml", f"{archived}/proposal.md")
    shutil.rmtree(scratch_repo.root / "ideation" / "staging" / TOPIC)

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 200, payload
    assert payload["retention_release"]["kind"] == bs.RETENTION_ARCHIVED_CHANGE
    assert payload["retention_release"]["change_id"] == CHANGE


def test_execution_receipt_releases_cleanup_for_the_exact_destination(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    manifest = _write_demotion_manifest(scratch_repo)
    scratch_repo.write(
        f"{RECORDS}{CHANGE}/demote-20260820T120100Z.execution-receipt.yaml",
        yaml.safe_dump({
            "schema_version": 1,
            "kind": gc.DEMOTION_EXECUTION_KIND,
            "actor": "brett",
            "change_id": CHANGE,
            "status": "executed",
            "destination": {
                "kind": "staged", "id": TOPIC,
                "path": f"ideation/staging/{TOPIC}",
            },
            "executed_at": "2099-08-20T12:01:00Z",
            "transition_manifest": manifest,
            "returned_moves": [{
                "from": f"openspec/changes/{CHANGE}/proposal.md",
                "to": f"ideation/staging/{TOPIC}/README.md",
            }],
            "returned_artifacts": [f"ideation/staging/{TOPIC}/README.md"],
            "removed_change_folder": True,
        }, sort_keys=False))

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 200, payload
    assert payload["retention_release"]["kind"] == bs.RETENTION_EXECUTED_DEMOTION


def test_legacy_manifest_requires_an_exact_returned_artifact(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _write_demotion_manifest(scratch_repo)

    refused, payload = _cleanup(scratch_repo, registry)
    assert refused == 409, payload
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True

    scratch_repo.write(
        f"ideation/staging/{TOPIC}/openspec/INDEX.md",
        f"Draft proposals returned from demoted change {CHANGE}-long.\n")
    near_match, payload = _cleanup(scratch_repo, registry)
    assert near_match == 409, payload

    scratch_repo.write(
        f"ideation/staging/{TOPIC}/openspec/INDEX.md",
        f"Draft proposals returned from demoted change {CHANGE}.\n")
    accepted, payload = _cleanup(scratch_repo, registry)
    assert accepted == 200, payload
    assert payload["retention_release"]["kind"] == bs.RETENTION_LEGACY_DEMOTION


def test_ambiguous_active_pick_fallbacks_fail_closed(scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    scratch_repo.write(f"openspec/changes/{CHANGE}/proposal.md", "# Why\n")
    scratch_repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1,
        "kind": "ideation-cross-reference",
        "repository": scratch_repo.repository,
        "generation": {
            "source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-a", "title": "A", "claim": "a", "state": "picked",
             "pick": {"staging_id": TOPIC, "change_id": CHANGE}},
            {"id": "pos-b", "title": "B", "claim": "b", "state": "picked",
             "pick": {"staging_id": "another-topic", "change_id": CHANGE}},
        ],
    }, sort_keys=False))

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409, payload
    assert "ambiguous" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_ad_hoc_origin_is_not_reinterpreted_through_pick_fallback(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    scratch_repo.write(f"openspec/changes/{CHANGE}/proposal.md", "# Why\n")
    scratch_repo.write(
        f"openspec/changes/{CHANGE}/.openspec.yaml",
        "schema: spec-driven\norigin:\n  kind: ad_hoc\n")
    scratch_repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": scratch_repo.repository,
        "generation": {
            "source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [{
            "id": "pos-demo", "title": "Demo", "claim": "c",
            "state": "picked",
            "pick": {"staging_id": TOPIC, "change_id": CHANGE},
        }],
    }, sort_keys=False))
    scratch_repo.commit(
        "Record ad hoc proposal",
        f"openspec/changes/{CHANGE}/proposal.md",
        f"openspec/changes/{CHANGE}/.openspec.yaml",
        "ideation/cross-reference.yaml")

    status, payload = _cleanup(scratch_repo, registry)
    assert status == 409, payload
    assert "no accepted retention-release evidence" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_unrelated_ambiguous_pick_does_not_block_exact_declared_origin(
        scratch_repo):
    exact = "add-exact"
    ambiguous = "add-ambiguous"
    _write_staged_origin(
        scratch_repo, f"openspec/changes/{exact}", topic=TOPIC)
    scratch_repo.write(f"openspec/changes/{exact}/proposal.md", "# Exact\n")
    scratch_repo.write(f"openspec/changes/{ambiguous}/proposal.md", "# Other\n")
    scratch_repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": scratch_repo.repository,
        "generation": {
            "source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-a", "title": "A", "claim": "a", "state": "picked",
             "pick": {"staging_id": "other-a", "change_id": ambiguous}},
            {"id": "pos-b", "title": "B", "claim": "b", "state": "picked",
             "pick": {"staging_id": "other-b", "change_id": ambiguous}},
        ],
    }, sort_keys=False))

    assert bs.landed_proposal_ids(scratch_repo.root)[TOPIC] == exact


def test_receipt_and_manifest_destination_mismatch_is_not_execution_proof(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    manifest = _write_demotion_manifest(
        scratch_repo, topic="another-topic")
    scratch_repo.write(
        f"{RECORDS}{CHANGE}/demote-20260820T120100Z.execution-receipt.yaml",
        yaml.safe_dump({
            "schema_version": 1,
            "kind": gc.DEMOTION_EXECUTION_KIND,
            "actor": "brett",
            "change_id": CHANGE,
            "status": "executed",
            "destination": {
                "kind": "staged", "id": TOPIC,
                "path": f"ideation/staging/{TOPIC}",
            },
            "executed_at": "2026-08-20T12:01:00Z",
            "transition_manifest": manifest,
            "returned_artifacts": [f"ideation/staging/{TOPIC}/README.md"],
            "removed_change_folder": True,
        }, sort_keys=False))

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409, payload
    assert "no accepted retention-release evidence" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_missing_tile_without_disposition_or_explicit_release_stays_retained(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    shutil.rmtree(scratch_repo.root / "ideation" / "staging" / TOPIC)

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409, payload
    assert "missing tile" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_explicit_human_release_cleans_a_true_orphan_and_records_why(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    shutil.rmtree(scratch_repo.root / "ideation" / "staging" / TOPIC)

    status, payload = _cleanup(
        scratch_repo, registry,
        retention_release_reason="duplicate captured in governance change #42",
        superseding_references=["openspec/changes/add-governed-successor"])

    assert status == 200, payload
    evidence = payload["retention_release"]
    assert evidence["kind"] == bs.RETENTION_EXPLICIT_HUMAN
    assert evidence["reason"].startswith("duplicate captured")
    record = yaml.safe_load(
        (scratch_repo.root / payload["record"]).read_text(encoding="utf-8"))
    assert record["reason"] == evidence["reason"]
    assert record["cleanup"]["retention_release"][
        "superseding_references"] == ["openspec/changes/add-governed-successor"]


@pytest.mark.parametrize("scope_kind,scope_id", [
    (bs.CLUSTER, "cl-orphan"),
    (bs.POSSIBLE, "pos-orphan"),
])
def test_non_staged_orphans_use_the_explicit_human_release_lane(
        scratch_repo, tmp_path, scope_kind, scope_id):
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile(scope_kind, scope_id)
    inventory = bs.TileInventory((tile,))
    session = bs.open_session(
        git, registry, repository=REPO, tile=tile, inventory=inventory,
        checkout_root=scratch_repo.root)
    gate = gr.HumanGate(scratch_repo.root, [RECORDS], human_actor="brett")
    gr.execute_abandon_session(
        gate, git, session=session, reason="parked", records_dir=RECORDS,
        checkout_root=scratch_repo.root)

    result = gr.execute_cleanup_abandoned_branch(
        gate, git, tile=tile, ref=tile.branch, registry=registry,
        repository=REPO, checkout_root=scratch_repo.root,
        records_dir=RECORDS, tile_inventory=inventory,
        retention_release_reason="deliberately discarded after triage")

    assert result["deleted"] is True
    assert result["retention_release"]["kind"] == bs.RETENTION_EXPLICIT_HUMAN
    assert result["retention_release"]["scope_kind"] == scope_kind


def test_cleanup_unwinds_its_record_when_branch_deletion_fails(
        scratch_repo, tmp_path, monkeypatch):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)
    before = set((scratch_repo.root / RECORDS).rglob(
        "cleanup-abandoned-branch-*.gate-action.yaml"))

    def fail_delete(*_args, **_kwargs):
        raise RuntimeError("injected delete failure")

    monkeypatch.setattr(git, "delete_branch", fail_delete)
    with pytest.raises(RuntimeError, match="injected delete failure"):
        gr.execute_cleanup_abandoned_branch(
            gr.HumanGate(scratch_repo.root, [RECORDS], human_actor="brett"),
            git, tile=tile, ref=DRAFT, registry=registry, repository=REPO,
            checkout_root=scratch_repo.root, records_dir=RECORDS,
            tile_inventory=bs.TileInventory((tile,)))

    after = set((scratch_repo.root / RECORDS).rglob(
        "cleanup-abandoned-branch-*.gate-action.yaml"))
    assert after == before
    assert git.branch_exists(DRAFT) is True


def test_cleanup_restores_the_exact_ref_when_record_finalization_fails(
        scratch_repo, tmp_path, monkeypatch):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    expected = git.branch_sha(DRAFT)
    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)

    def fail_finalize(*_args, **_kwargs):
        raise OSError("injected finalization failure")

    monkeypatch.setattr(gc, "replace_gate_action_record", fail_finalize)
    with pytest.raises(bs.SessionRefused, match="exact ref was restored"):
        gr.execute_cleanup_abandoned_branch(
            gr.HumanGate(scratch_repo.root, [RECORDS], human_actor="brett"),
            git, tile=tile, ref=DRAFT, registry=registry, repository=REPO,
            checkout_root=scratch_repo.root, records_dir=RECORDS,
            tile_inventory=bs.TileInventory((tile,)))

    assert git.branch_sha(DRAFT) == expected
    assert not tuple((scratch_repo.root / RECORDS).rglob(
        "cleanup-abandoned-branch-*.gate-action.yaml"))


def test_cleanup_refuses_gate_and_git_roots_that_do_not_match(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(bs.SessionRefused, match="same repository"):
        gr.execute_cleanup_abandoned_branch(
            gr.HumanGate(other, [RECORDS], human_actor="brett"),
            sg.SessionGit(scratch_repo.root),
            tile=bs.Tile(bs.STAGED_TOPIC, TOPIC), ref=DRAFT,
            registry=registry, repository=REPO,
            checkout_root=scratch_repo.root, records_dir=RECORDS,
            tile_inventory=bs.TileInventory(
                (bs.Tile(bs.STAGED_TOPIC, TOPIC),)),
            retention_release_reason="would release if roots matched")


def test_explicit_release_body_rejects_blank_superseding_references(
        scratch_repo, tmp_path):
    registry, _created, _worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")

    status, payload = _cleanup(
        scratch_repo, registry,
        retention_release_reason="discarded deliberately",
        superseding_references=["  "])

    assert status == 400, payload
    assert "superseding_references" in payload["message"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_explicit_release_has_cli_and_http_parity(tmp_path, capsys, monkeypatch):
    cli_repo = build_scratch_repo(tmp_path / "cli")
    cli_registry, _created, _worktree = _session(cli_repo, tmp_path / "cli-state")
    _abandon(cli_repo, cli_registry, reason="parked")
    monkeypatch.setenv("XF_HUMAN_CONSOLE", "1")

    cli_rc = cli_mod.main([
        "gate", "cleanup-abandoned-branch", "--repo-root", str(cli_repo.root),
        "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
        "--scope-id", TOPIC, "--ref", DRAFT,
        "--retention-release-reason", "discarded after duplicate review",
        "--superseding-reference", "openspec/changes/add-successor",
    ])
    cli_out = capsys.readouterr().out

    assert cli_rc == 0
    assert "explicit-human-release" in cli_out
    assert "gate-action record" in cli_out
    assert sg.SessionGit(cli_repo.root).branch_exists(DRAFT) is False

    http_repo = build_scratch_repo(tmp_path / "http")
    http_registry, _created, _worktree = _session(
        http_repo, tmp_path / "http-state")
    _abandon(http_repo, http_registry, reason="parked")
    served = _served_snapshot(http_repo, tmp_path / "http-served.json")
    with _serving(http_repo, served, actor="brett") as (host, port):
        status, payload = _post(host, port, CLEANUP_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC,
            "scope_id": TOPIC,
            "ref": DRAFT,
            "retention_release_reason": "discarded after duplicate review",
            "superseding_references": ["openspec/changes/add-successor"],
        })

    assert status == 200, payload
    assert payload["retention_release"]["kind"] == bs.RETENTION_EXPLICIT_HUMAN
    assert payload["record"].endswith(".gate-action.yaml")
    assert sg.SessionGit(http_repo.root).branch_exists(DRAFT) is False


# --------------------------------------------------------------------------
# second-review finding 3 — NOT LIVE IS NOT ABANDONED
#
# The four original preconditions are all satisfied by a session that simply
# CRASHED, or by a human following the stale-worktree remedy this build itself
# prints ("remove the directory and run `git worktree prune`"). The verb then
# deleted the branch carrying the tile's ENTIRE gate-action commit series — the
# traceability evidence of D18/FR-006 — with no record surviving anywhere, while
# both surfaces told the human "the abandon record on `main` survives it".
# --------------------------------------------------------------------------

def _lose_liveness_without_an_abandon(repo, registry, worktree):
    """Exactly what a crash — or the remedy the dashboard prints — leaves behind:
    the worktree directory gone and pruned, the branch surviving, and NOTHING
    ended. The registry entry goes with the directory because liveness is
    per-process and the next process re-derives it from the worktree that is no
    longer there (FR-008, T033a)."""
    shutil.rmtree(worktree)
    repo.git("worktree", "prune")
    registry.drop(repo.repository, DRAFT)
    assert bs.is_live(registry, repo.repository, DRAFT) is False
    assert sg.SessionGit(repo.root).branch_exists(DRAFT) is True
    assert bs.abandon_proof(repo.root, DRAFT) is None


def test_cleanup_refuses_a_branch_whose_session_was_never_abandoned(scratch_repo,
                                                                    tmp_path):
    """The HTTP leg. The whole gate-action commit series must still be reachable
    afterwards — before the fifth precondition, `git branch --contains` on the
    action's own sha printed nothing at all."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    action_sha = git.head(ref=DRAFT)
    _lose_liveness_without_an_abandon(scratch_repo, registry, worktree)
    _land_proposal(scratch_repo)

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409, payload
    assert payload["error"] == "gate_refused"
    assert "NOTHING records that its session was ABANDONED" in payload["message"]
    assert "stale residue" in payload["message"]
    # nothing was deleted, and the evidence series is still reachable from its ref
    assert git.branch_exists(DRAFT) is True
    containing = scratch_repo.git("branch", "--contains", action_sha,
                                  "--format=%(refname:short)").split()
    assert DRAFT in containing
    assert list((scratch_repo.root / RECORDS).rglob("*.gate-action.yaml")) == []


def test_the_cli_cleanup_refuses_the_same_state_the_runbook_command_hits(
        scratch_repo, tmp_path, capsys, monkeypatch):
    """The CLI leg — the runbook's own invocation. It printed "the abandon record
    on `main` survives it" over a session nobody had abandoned, and exited 0."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _lose_liveness_without_an_abandon(scratch_repo, registry, worktree)
    _land_proposal(scratch_repo)
    monkeypatch.setenv("XF_HUMAN_CONSOLE", "1")
    capsys.readouterr()

    rc = cli_mod.main(["gate", "cleanup-abandoned-branch", "--repo-root",
                       str(scratch_repo.root), "--actor", "brett",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--ref", DRAFT])
    captured = capsys.readouterr()

    assert rc == 1
    assert "NOTHING records that its session was ABANDONED" in captured.err
    assert "survives it" not in captured.out
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_the_durable_ending_marker_is_the_second_admissible_proof(scratch_repo,
                                                                  tmp_path):
    """The ending marker records `ending='abandon'` and OUTLIVES the branch, so it
    proves the abandon for the case where the main-resident record no longer does —
    an untracked records tree cleaned by hand, say. Nothing infers the abandon from
    the absence of liveness in either arm."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    for record in (scratch_repo.root / RECORDS).rglob(
            "abandon-session-*.gate-action.yaml"):
        record.unlink()
    _land_proposal(scratch_repo)
    assert bs.abandon_proof(scratch_repo.root, DRAFT) is None
    bs.write_ending_marker(scratch_repo.root, DRAFT, ending=bs.ENDING_ABANDON)

    status, payload = _cleanup(
        scratch_repo, registry,
        retention_release_reason="legacy marker reviewed against current head")

    assert status == 200, payload
    assert bs.ENDING_ABANDON in payload["abandon_proof"]
    assert ".ended.json" in payload["abandon_proof"]
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False
    assert payload["retention_release"]["kind"] == bs.RETENTION_EXPLICIT_HUMAN


def test_a_merge_ending_marker_is_not_an_abandon(scratch_repo, tmp_path):
    """The marker arm reads the WORD, not the file's existence: FR-033's ending
    leaves `ending='merge'`, which authorizes no FR-028 cleanup."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _lose_liveness_without_an_abandon(scratch_repo, registry, worktree)
    _land_proposal(scratch_repo)
    bs.write_ending_marker(scratch_repo.root, DRAFT, ending=bs.ENDING_MERGE)

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409, payload
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_cleanup_refuses_a_live_session_branch(scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _land_proposal(scratch_repo)

    status, payload = _cleanup(scratch_repo, registry)

    assert status == 409
    message = payload["message"].lower()
    assert "live" in message and "abandoned" in message
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True
    assert worktree.is_dir()


def test_cleanup_refuses_another_tiles_branch_and_a_ref_that_is_not_a_session(
        tmp_path):
    repo = build_scratch_repo(tmp_path, extra_topics=("demo-topic-2",))
    registry = _registry(repo, tmp_path)
    _land_proposal(repo)
    git = sg.SessionGit(repo.root)
    git.git(repo.root, "branch", f"{DRAFT}-2", "main")       # tile demo-topic-2's

    for ref in (f"{DRAFT}-2", "main", "draft/other-topic", ""):
        status, payload = _cleanup(repo, registry, ref=ref)
        assert status in (400, 409), ref
        assert payload["error"] in ("gate_refused", "invalid_body"), ref
    assert git.branch_exists(f"{DRAFT}-2") is True
    assert git.branch_exists("main") is True


def test_the_cleanup_route_refuses_off_loopback_before_the_body_is_parsed(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, served, host="0.0.0.0") as (host, port):
        shaped = _post(host, port, CLEANUP_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "ref": DRAFT})
        unparseable = _post_raw(host, port, CLEANUP_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "loopback_only", payload
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_the_cleanup_route_fails_closed_with_no_resolved_actor(scratch_repo,
                                                               tmp_path,
                                                               monkeypatch):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)

    with _serving(scratch_repo, served, actor=None) as (host, port):
        shaped = _post(host, port, CLEANUP_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "ref": DRAFT})
        unparseable = _post_raw(host, port, CLEANUP_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "action_unavailable", payload
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True


def test_the_cleanup_agent_path_is_rejected_before_the_branch_is_touched(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    agent = OutputBoundary(scratch_repo.root, [RECORDS], actor="agent")

    with pytest.raises(BoundaryViolation):
        gr.execute_cleanup_abandoned_branch(
            agent, git, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC), ref=DRAFT,
            registry=registry, repository=REPO, checkout_root=scratch_repo.root,
            records_dir=RECORDS)

    assert agent.refusals and agent.refusals[0].kind == "gate-side-effect"
    assert git.branch_exists(DRAFT) is True


def test_the_cleanup_cli_verb_enforces_the_human_gate_and_deletes_the_branch(
        scratch_repo, tmp_path, capsys):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _abandon(scratch_repo, registry, reason="parked")
    _land_proposal(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    assert "_session_identity_gate" in inspect.getsource(
        cli_mod.cmd_gate_cleanup_abandoned_branch)
    assert "require_human_gate" in inspect.getsource(
        cli_mod._session_identity_gate)

    with pytest.raises(SystemExit) as exited:                # missing --actor
        cli_mod.main(["gate", "cleanup-abandoned-branch", "--repo-root",
                      str(scratch_repo.root), "--scope-kind", bs.STAGED_TOPIC,
                      "--scope-id", TOPIC, "--ref", DRAFT])
    assert exited.value.code != 0
    assert git.branch_exists(DRAFT) is True

    capsys.readouterr()
    rc = cli_mod.main(["gate", "cleanup-abandoned-branch", "--repo-root",
                       str(scratch_repo.root), "--actor", "   ",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--ref", DRAFT])
    assert rc == 1
    assert "refused" in capsys.readouterr().err
    assert git.branch_exists(DRAFT) is True

    capsys.readouterr()
    rc = cli_mod.main(["gate", "cleanup-abandoned-branch", "--repo-root",
                       str(scratch_repo.root), "--actor", "brett",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--ref", DRAFT])
    assert rc == 0
    assert DRAFT in capsys.readouterr().out
    assert git.branch_exists(DRAFT) is False


# ==========================================================================
# T052 — the teardown is ONE mechanism, shared by both endings (FR-021)
# ==========================================================================

def test_the_teardown_is_shared_and_the_merge_ending_adds_only_the_deletion(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    session = _open(scratch_repo, registry)
    notebook = FakeNotebookAdapter()
    notebook.create(session.notebook_alias)
    snapshot = bs.session_snapshot_path(scratch_repo.root, DRAFT)
    assert snapshot.is_file()

    result = _teardown(scratch_repo, session, delete_branch=True,
                       notebook=notebook)

    assert result.branch == DRAFT
    assert sorted(result.torn_down) == ["notebook", "registry-entry", "worktree"]
    assert result.branch_deleted is True
    assert result.branch_retained is False
    assert not worktree.exists()
    assert not snapshot.exists()                  # the derived bytes go with it
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert notebook.live_aliases() == ()
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False
    # the main view was refreshed, and it is still what the shared surfaces show
    assert registry.active.ref == reg.DEFAULT_REF


def test_the_teardown_reports_a_notebook_it_could_not_reach_and_still_ends_the_session(
        scratch_repo, tmp_path):
    """A session's liveness is its registry entry (FR-008): an unreachable
    notebook must not leave a session half-ended."""
    class Failing(FakeNotebookAdapter):
        def retire(self, alias):
            self.calls.append(("retire", alias))
            raise RuntimeError("nlm is unavailable")

    registry, created, worktree = _session(scratch_repo, tmp_path)
    session = _open(scratch_repo, registry)
    notebook = Failing()

    result = _teardown(scratch_repo, session, notebook=notebook)

    assert "notebook" not in result.torn_down
    assert any("nlm is unavailable" in note for note in result.notes)
    assert "worktree" in result.torn_down and "registry-entry" in result.torn_down
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert not worktree.exists()


def test_abandon_reports_honestly_when_no_notebook_adapter_is_declared(
        scratch_repo, tmp_path):
    """Phase 8 injects the adapter; until then the response must not claim a
    notebook was retired when nothing was asked to retire one."""
    registry, created, worktree = _session(scratch_repo, tmp_path)

    status, payload = _abandon(scratch_repo, registry, reason="no notebook here")

    assert status == 200, payload
    assert payload["torn_down"] == ["worktree", "registry-entry"]
    assert "notebook" in payload["hint"]
