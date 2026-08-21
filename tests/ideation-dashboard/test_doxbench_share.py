"""SHARE-SESSION — tasks.md §12 of add-doxbench-editing-phase-b.

The verb that hands a live workbench session to a colleague. Every test here is
against the REAL route, a REAL git remote (a bare repo on disk, never a network),
and the REAL port seam — because the thing §12 asserts is a set of ABSENCES, and
an absence is only worth something if the presence is genuinely reachable.

The table this file holds the surface to:

| task | the claim | where it is asserted |
|---|---|---|
| 12.1 | commit threads -> the port's EXISTING `push` -> return the ref | `test_a_share_commits_the_threads_then_pushes` |
| 12.1 | no pull request, no review, no approval or merge authority | `test_a_share_never_reaches_a_forbidden_port_member` |
| 12.2 | nothing pushes implicitly | `test_no_implicit_path_reaches_a_push` + the behavioural pair |
| 12.3 | nothing new is reported honestly, not pushed again | `test_a_second_share_with_nothing_new_reports_and_does_not_push` |
| 12.4 | loopback-only, fail-closed actor, console presence, human gate | the POSTURE section |
| 12.5 | the colleague resumes and SEES THE THREADS | the RESUME section, incl. P3-17 |
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import (FORBIDDEN_PUSH_TOKENS,
                      NO_IMPLICIT_PUSH_MODULES,
                      find_openxfactory_validator)
from session_fixtures import FakePullRequests, build_scratch_repo

from ideation_dashboard import branch_session as bs
from ideation_dashboard import doxbench_hash as dh
from ideation_dashboard import doxbench_threads as dt
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import session_git as sg
from ideation_dashboard import session_pr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

REPO_ROOT = Path(__file__).resolve().parents[2]
TOPIC = "demo-topic"
BRANCH = "draft/demo-topic"
RECORDS = gc.DEFAULT_RECORDS_DIR
VALIDATOR = find_openxfactory_validator()

pytestmark_validator = pytest.mark.skipif(
    VALIDATOR is None, reason="pinned openxFactory validator not reachable")


# ===========================================================================
# the world: a real bare origin, a served checkout, a live session
# ===========================================================================

def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _act(repo, registry, verb, body, **over):
    over.setdefault("provenance", gc.HTTP_CONSOLE_TOKEN)
    return gr.run_gate_action(
        verb, body, checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=repo.repository, **over)


def _session_world(tmp_path):
    """A live session holding one document, opened through the real route."""
    repo = build_scratch_repo(tmp_path)
    registry = _registry(repo, tmp_path)
    status, created = _act(repo, registry, "create-document", {
        "title": "First Draft", "summary": "The session's first document.",
        "topics": ["alpha"], "area": f"ideation/staging/{TOPIC}/",
        "repository_context": repo.repository, "repository": repo.repository,
        "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC})
    assert status == 200, created
    return repo, registry, created


def _worktree(repo):
    return bs.worktree_path(repo.root, BRANCH)


def _scope():
    return {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC}


def _share(repo, registry, port=None, **over):
    return _act(repo, registry, "share-session", _scope(),
                session_pull_requests=port if port is not None
                else FakePullRequests(), **over)


def _save(repo, registry, document_rel: str, content: str, **over):
    """The doxBench GOVERNED SAVE. It must be `first-edit`, not `edit-document`:
    only first-edit injects the thread seam (`thread_paths_for`), so only it
    carries a sidecar with its document. A test that used the other verb would
    assert the thread filter against a route that has no filter."""
    body = {**_scope(), "document": document_rel, "content": content}
    # FR-032: an overwrite is revalidated against the bytes it would replace, so
    # the Save declares the hash of what it read. Taken from the WORKTREE, which
    # is what the session is actually editing.
    current = _worktree(repo) / document_rel
    if current.is_file():
        body["base_hash"] = dh.sha256_hex(current.read_text(encoding="utf-8"))
    return _act(repo, registry, "first-edit", body, **over)


def _write_thread(repo, document_rel: str, body: str = "a working note") -> str:
    """Leave a DIRTY sidecar for `document_rel`, the way a turn does: written
    into the session worktree and not committed by anything."""
    rel = dt.thread_path_for(document_rel)
    target = _worktree(repo) / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"# thread\n\nStatus: record\n\n{body}\n", encoding="utf-8")
    return rel


def _origin_sha(repo, branch: str = BRANCH) -> str | None:
    out = subprocess.run(
        ["git", "-C", str(repo.origin), "rev-parse", "--verify", branch],
        capture_output=True, text=True)
    return out.stdout.strip() or None


class RealPush(FakePullRequests):
    """The fake port with ONE member made real: `push` runs an actual `git push`
    into the bare origin, so the colleague half of §12.5 fetches something that
    genuinely got there.

    Everything else stays fake and RECORDED, which is the point: the forbidden
    members remain reachable, so a verb that called one would be caught rather
    than merely unobserved."""

    def __init__(self, worktree: Path, **kw):
        super().__init__(**kw)
        self._worktree = Path(worktree)

    def push(self, branch: str) -> None:
        super().push(branch)          # keeps `calls` and `pushed` honest
        subprocess.run(
            ["git", "-C", str(self._worktree), "push", "--set-upstream",
             "origin", branch],
            check=True, capture_output=True, text=True)


# ===========================================================================
# 12.1 — THE VERB: commit threads, push, return the ref. And nothing else.
# ===========================================================================

def test_a_share_commits_the_threads_then_pushes(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    rel = _write_thread(repo, created["path"])
    port = FakePullRequests()

    status, shared = _share(repo, registry, port)

    assert status == 200, shared
    assert shared["shared"] is True
    assert shared["threads"] == [rel]
    assert shared["pushed_ref"] == f"refs/heads/{BRANCH}"
    assert port.pushed == [BRANCH]
    # the sidecar is COMMITTED now, not merely present
    assert rel not in _dirty(repo)


def _dirty(repo) -> tuple[str, ...]:
    out = subprocess.run(
        ["git", "-C", str(_worktree(repo)), "status", "--porcelain",
         "--untracked-files=all"],
        capture_output=True, text=True, check=True)
    return tuple(line[3:] for line in out.stdout.splitlines() if line.strip())


def test_the_returned_ref_is_the_branch_ref_that_was_pushed(tmp_path):
    """The requirement's phrase "returns the pushed ref" means the REF, and the
    response's `revision` is the sha it points at — both, because a colleague
    needs the name to fetch and the reviewer needs the sha to know what they
    got."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    port = RealPush(_worktree(repo))

    status, shared = _share(repo, registry, port)

    assert status == 200, shared
    assert shared["pushed_ref"] == f"refs/heads/{BRANCH}"
    assert shared["revision"] == _origin_sha(repo)


def test_a_share_never_reaches_a_forbidden_port_member(tmp_path):
    """12.1's whole negative: no pull request, no review request, no approval or
    merge authority. Asserted against the port's own call log, so it covers what
    the verb DID rather than what its source says."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    port = FakePullRequests()

    status, shared = _share(repo, registry, port)

    assert status == 200, shared
    reached = {name for name, *_ in port.calls}
    assert reached == {"push"}
    for forbidden in gr.FORBIDDEN_SHARE_OPERATIONS:
        assert forbidden not in reached
    assert port.opened == [] if hasattr(port, "opened") else True


def test_the_forbidden_set_is_derived_from_the_port_not_restated():
    """A port that grows a fourth member must FAIL this, not silently widen the
    verb — which is why the constant is derived rather than written out.

    THE MEMBERSHIP ASSERTION IS LOAD-BEARING, and its absence was a real hole
    (PR #234, Copilot). Both the constant and this test derive the forbidden set
    the same way — `PORT_OPERATIONS` minus `push` — so if `push` ever left the
    port, both sides would move together, the set-difference below would still
    hold, and `push not in FORBIDDEN` would still hold because the whole port
    would be forbidden. The invariant this test exists to guard would be dead
    while the test stayed green. Reproduced by removing `push` from
    `PORT_OPERATIONS`: the test passed. Asserting the ANTECEDENT is what makes
    the derivation checkable."""
    # the antecedent: the member the verb is allowed to reach must EXIST
    assert "push" in session_pr.PORT_OPERATIONS
    # the derivation: everything else on the port is forbidden to this verb
    assert set(gr.FORBIDDEN_SHARE_OPERATIONS) == (
        set(session_pr.PORT_OPERATIONS) - {"push"})
    assert "push" not in gr.FORBIDDEN_SHARE_OPERATIONS
    assert gr.FORBIDDEN_SHARE_OPERATIONS


def test_a_share_takes_no_title_and_no_body(tmp_path):
    """Those fields exist on `open-pr` to name a pull request. A verb that opens
    none has nothing to name, and accepting them would imply it does."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    port = FakePullRequests()

    status, shared = _act(
        repo, registry, "share-session",
        {**_scope(), "title": "please review", "body": "a description"},
        session_pull_requests=port)

    assert status == 200, shared
    # accepted as an ordinary unknown field and IGNORED — never forwarded
    assert all(name == "push" for name, *_ in port.calls)


# ===========================================================================
# 12.2 — NOTHING PUSHES IMPLICITLY
# ===========================================================================

def test_no_implicit_path_reaches_a_push(tmp_path):
    """The §11 source sweep, EXTENDED rather than restated. These four modules
    are where a turn, a Save, a compaction or a scheduled task lives, and none of
    them may reach a remote write. The share verb deliberately does NOT live in
    any of them: it lives in `gate_routes.py`, beside the only other verb on this
    surface that writes to a remote."""
    assert {"serve.py", "doxbench_threads.py", "doxbench_bridge.py",
            "doxbench_mcp.py"} <= set(NO_IMPLICIT_PUSH_MODULES), (
        "§12 may widen §11's sweep, never narrow it")
    for module in NO_IMPLICIT_PUSH_MODULES:
        source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                  / module).read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_PUSH_TOKENS:
            assert forbidden not in source, (module, forbidden)


def test_a_save_commits_the_thread_and_pushes_nothing(tmp_path):
    """The behavioural half, which the source sweep cannot give: a real Save
    through the real route, with a port that would RECORD a push, and no push."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    port = FakePullRequests()

    status, edited = _save(repo, registry, created["path"],
                           "# First Draft\n\nrewritten.\n",
                           session_pull_requests=port)

    assert status == 200, edited
    assert port.calls == []
    assert port.pushed == []
    assert _origin_sha(repo) is None      # the branch never left the machine


def test_the_session_branch_is_absent_from_the_remote_until_the_verb_runs(
        tmp_path):
    """The disclosure claim, end to end and unmediated by any port: after a
    document is created and Saved, the bare origin has never heard of the
    branch."""
    repo, registry, created = _session_world(tmp_path)
    _save(repo, registry, created["path"],
          "# First Draft\n\nrewritten again.\n")

    assert _origin_sha(repo) is None

    _share(repo, registry, RealPush(_worktree(repo)))

    assert _origin_sha(repo) is not None


# ===========================================================================
# 12.3 — NOTHING NEW, REPORTED HONESTLY
# ===========================================================================

def test_a_second_share_with_nothing_new_reports_and_does_not_push(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    first = RealPush(_worktree(repo))
    status, shared = _share(repo, registry, first)
    assert status == 200 and shared["shared"] is True, shared

    second = FakePullRequests()
    status, again = _share(repo, registry, second)

    assert status == 200, again
    assert again["shared"] is False
    assert second.calls == []                      # the port was never touched
    assert "nothing new to share" in again["reason"]
    assert BRANCH in again["reason"]


def test_nothing_new_is_two_conditions_not_one(tmp_path):
    """A run of Saves leaves NO dirty sidecar and unpushed commits — the ORDINARY
    state, because nothing pushes implicitly. Reading only dirtiness would call
    that "nothing to share" and strand the colleague, so the plan checks both."""
    repo, registry, created = _session_world(tmp_path)
    _save(repo, registry, created["path"],
          "# First Draft\n\nsaved, never shared.\n")

    port = RealPush(_worktree(repo))
    status, shared = _share(repo, registry, port)

    assert status == 200, shared
    assert shared["shared"] is True
    assert shared["threads"] == []                 # nothing dirty to commit
    assert port.pushed == [BRANCH]                 # but plenty to publish
    assert shared["record_resident"] == "main"


def test_the_nothing_new_report_names_what_it_checked(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    _share(repo, registry, RealPush(_worktree(repo)))

    status, again = _share(repo, registry, FakePullRequests())

    assert status == 200
    reason = again["reason"]
    assert "no uncommitted thread sidecars" in reason
    assert "already holds this branch" in reason
    assert "Nothing was pushed" in reason


# ===========================================================================
# 12.4 — THE GATE POSTURE
# ===========================================================================

def test_a_blank_actor_fails_closed(tmp_path):
    repo, registry, _created = _session_world(tmp_path)
    status, refused = gr.run_gate_action(
        "share-session", _scope(), checkout_root=repo.root, actor="",
        snapshot_path=None, session_registry=registry,
        repository=repo.repository,
        session_pull_requests=FakePullRequests())
    assert status != 200
    assert refused.get("ok") is False


def test_a_plane_with_no_port_refuses_and_names_the_plane_rule(tmp_path):
    """The push identity follows the PLANE rule the Save already carries: the
    invoking engineer's own credential, never a stored service identity. A plane
    that declares no port therefore has no identity to push with, and says so."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])

    status, refused = _act(repo, registry, "share-session", _scope(),
                           session_pull_requests=None)

    assert status != 200
    message = json.dumps(refused)
    assert "no identity to push with" in message
    assert "INVOKING ENGINEER" in message


def test_a_plane_with_no_registry_refuses(tmp_path):
    repo = build_scratch_repo(tmp_path)
    status, refused = gr.run_gate_action(
        "share-session", _scope(), checkout_root=repo.root, actor="brett",
        snapshot_path=None, session_registry=None,
        repository=repo.repository,
        session_pull_requests=FakePullRequests())
    assert status != 200
    assert "no session registry" in json.dumps(refused)


def test_share_session_is_session_bearing_so_console_presence_is_enforced():
    """Membership is what subjects the verb to FR-019's third clause at the HTTP
    door — the agent-invocation refusal every remote-writing verb carries."""
    assert "share-session" in gr.SESSION_BEARING_VERBS
    assert "share-session" in gr.EXECUTING_VERBS


def test_the_verb_declares_the_tile_scope_or_refuses(tmp_path):
    repo, registry, _created = _session_world(tmp_path)
    status, refused = _act(repo, registry, "share-session", {},
                           session_pull_requests=FakePullRequests())
    assert status != 200
    assert "scope_kind" in json.dumps(refused)


def test_there_is_no_live_session_to_share(tmp_path):
    """Fail-closed on a tile with no session, with the verb's own remedy."""
    repo = build_scratch_repo(tmp_path)
    registry = _registry(repo, tmp_path)
    status, refused = _share(repo, registry)
    assert status != 200
    assert "share-session" in json.dumps(refused)


def test_the_share_gate_is_narrower_than_the_save_gate():
    """A Save WRITES a sidecar through its gate and so must declare the thread
    prefix. A share writes none — it commits sidecars already on disk — so
    granting the prefix here would widen the allowlist for a write that does not
    exist."""
    build = gr.share_session_gate_factory("brett", RECORDS)
    gate = build(Path("/tmp"))
    allowed = list(getattr(gate.output, "allowed", None)
                   or getattr(gate.output, "allowlist", []))
    assert any(RECORDS in str(entry) for entry in allowed)
    assert not any(dt.THREAD_PREFIX in str(entry) for entry in allowed)


# ===========================================================================
# 12.5 — THE COLLEAGUE RESUMES, AND P3-17 IS DISCHARGED
# ===========================================================================

def _colleague_clone(tmp_path, repo) -> Path:
    """A DIFFERENT machine: a fresh clone of the bare origin, which can only ever
    see what was actually pushed.

    Named `openxFactory` inside its own directory because the session machinery
    keys the registry on the checkout's directory name."""
    dest = tmp_path / "colleague" / repo.repository
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", str(repo.origin), str(dest)],
                   check=True, capture_output=True, text=True)
    for key, value in (("user.email", "colleague@example.invalid"),
                       ("user.name", "Colleague")):
        subprocess.run(["git", "-C", str(dest), "config", key, value],
                       check=True, capture_output=True, text=True)
    return dest


def _colleague_registry(root: Path, repository: str, tmp_path):
    path = tmp_path / f"colleague-snapshot-{root.name}.json"
    path.write_text(json.dumps(generate_snapshot(root, repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repository, ref=reg.DEFAULT_REF,
        source_root=root), active=True)
    return registry


def _colleague_join(clone: Path, repository: str, tmp_path, *,
                    continuation=None):
    """THE REAL SUPPORTED SESSION JOIN, driven exactly as every session-bearing
    verb drives it: `open_session` over the colleague's own checkout.

    This is the whole point of Codex's P1 on PR #234. The first version of the
    resume test checked out the branch by hand and read files off disk, which
    proved the BYTES travelled and proved nothing at all about the ratified
    scenario's words — "open the tile, join the session"."""
    git = sg.SessionGit(clone)
    return bs.open_session(
        git, _colleague_registry(clone, repository, tmp_path),
        repository=repository, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
        inventory=gr.discover_tile_inventory(clone), checkout_root=clone,
        continuation=continuation)


def _fetch_command_from(message: str) -> list[str]:
    """The fetch command the REFUSAL ITSELF printed, parsed out so the test can
    RUN it. Pinning the remedy by executing it is the only way it cannot rot:
    the previous hint (`git fetch origin <branch>`, no refspec) returned 0,
    created no local branch, and left the human at the identical refusal."""
    found = re.search(r"`(git fetch origin [^`]+)`", message)
    assert found, f"the refusal names no fetch command: {message}"
    return found.group(1).split()


def _share_then_resume(tmp_path, note: str):
    """Share a discussed document, then JOIN the session from a fresh clone
    through the real flow. Returns (rel, session, worktree)."""
    repo, registry, created = _session_world(tmp_path)
    rel = _write_thread(repo, created["path"], note)
    status, shared = _share(repo, registry, RealPush(_worktree(repo)))
    assert status == 200 and shared["shared"], shared

    clone = _colleague_clone(tmp_path, repo)

    # THE TILE IS OPENED FIRST, with no answer — the colleague gets the
    # resume-or-new report, exactly as FR-025 requires. A session is never
    # opened over a surviving branch silently, not even a shared one.
    with pytest.raises(bs.AbandonedBranchSurvives) as reported:
        _colleague_join(clone, repo.repository, tmp_path)

    # THE REMEDY IS RUN, not read: the refusal's own fetch command, parsed out
    # of its text and executed. See `_fetch_command_from`.
    with pytest.raises(bs.SessionRefused) as refused:
        _colleague_join(clone, repo.repository, tmp_path,
                        continuation=bs.CONTINUATION_RESUME)
    subprocess.run(_fetch_command_from(str(refused.value)), cwd=clone,
                   check=True, capture_output=True, text=True)

    session = _colleague_join(clone, repo.repository, tmp_path,
                              continuation=bs.CONTINUATION_RESUME)
    assert str(reported.value)
    return repo, created, rel, session, Path(session.worktree)


def test_a_colleague_fetches_the_branch_and_joins_the_session(tmp_path):
    """12.5 end to end, through the SUPPORTED FLOW: share, clone, fetch, and
    JOIN THE SESSION — then find the session's documents and its threads inside
    the session worktree the join materialized.

    The earlier version of this test checked the branch out by hand and read
    files off disk. That proved the bytes travelled and proved nothing about the
    ratified scenario's words — "open the tile, join the session" — and it hid a
    real defect (PR #234, Codex P1): the resume path refused a remote-only
    branch, and the remedy it printed could not work."""
    _repo, created, rel, session, worktree = _share_then_resume(
        tmp_path, "the reasoning behind the draft")

    assert session.branch == BRANCH
    assert worktree.is_dir(), "the join must materialize a session worktree"
    assert (worktree / created["path"]).is_file()
    thread = worktree / rel
    assert thread.is_file(), sorted(
        x.name for x in worktree.rglob("*.thread.md"))
    assert "the reasoning behind the draft" in thread.read_text(encoding="utf-8")


def test_a_discussed_but_never_saved_document_thread_still_arrives(tmp_path):
    """P3-17, DISCHARGED — the tail §11 could not close and recorded here, and
    now proved through the REAL session join rather than a manual checkout.

    The document is created, then DISCUSSED and never Saved again. Its sidecar is
    dirty and no Save will ever carry it, so before §12 it would sit uncommitted
    and the colleague would resume with the thread silently missing. The share
    verb sweeps it as its own gate action, so it travels — and the colleague
    finds it by JOINING the session, which is the path that matters."""
    repo, _created, rel, _session, worktree = _share_then_resume(
        tmp_path, "we argued about the framing")
    del repo

    assert (worktree / rel).is_file(), (
        "P3-17 regression: the thread did not survive the real resume")
    assert "we argued about the framing" in (
        worktree / rel).read_text(encoding="utf-8")


def test_the_refusal_names_a_fetch_that_actually_materializes_the_branch(
        tmp_path):
    """The remedy defect on its own, pinned in isolation (PR #234, Codex P1
    link 3): the refspec-less form the refusal USED to print succeeds, creates
    no local branch, and leaves the colleague at the identical refusal."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    _share(repo, registry, RealPush(_worktree(repo)))
    clone = _colleague_clone(tmp_path, repo)

    with pytest.raises(bs.SessionRefused) as refused:
        _colleague_join(clone, repo.repository, tmp_path,
                        continuation=bs.CONTINUATION_RESUME)

    # the OLD hint: succeeds, and does nothing that helps
    subprocess.run(["git", "fetch", "origin", BRANCH], cwd=clone, check=True,
                   capture_output=True, text=True)
    assert sg.SessionGit(clone).local_ordinals("draft/") == ()

    # the hint the refusal actually prints now: creates the local ref, and
    # deliberately does NOT check it out
    subprocess.run(_fetch_command_from(str(refused.value)), cwd=clone,
                   check=True, capture_output=True, text=True)
    assert sg.SessionGit(clone).local_ordinals("draft/") == (BRANCH,)
    assert sg.SessionGit(clone).checked_out_at(BRANCH) is None


def test_a_branch_checked_out_by_hand_refuses_with_its_own_remedy(tmp_path):
    """Codex P1 link 4: `git checkout <branch>` creates the ref but CHECKS IT
    OUT, and git allows a branch in one working tree at a time — so the resume
    used to die as a raw GitError 128 naming neither cause nor fix."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    _share(repo, registry, RealPush(_worktree(repo)))
    clone = _colleague_clone(tmp_path, repo)
    subprocess.run(["git", "checkout", BRANCH], cwd=clone, check=True,
                   capture_output=True, text=True)

    with pytest.raises(bs.SessionRefused) as refused:
        _colleague_join(clone, repo.repository, tmp_path,
                        continuation=bs.CONTINUATION_RESUME)

    message = str(refused.value)
    assert "already CHECKED OUT" in message
    assert "one working tree at a time" in message
    assert "Nothing was opened" in message

    # and the remedy it names resolves it
    subprocess.run(["git", "checkout", bs.DEFAULT_BASE], cwd=clone, check=True,
                   capture_output=True, text=True)
    session = _colleague_join(clone, repo.repository, tmp_path,
                              continuation=bs.CONTINUATION_RESUME)
    assert Path(session.worktree).is_dir()


def test_the_sweep_is_cross_document_and_the_save_filter_is_not(tmp_path):
    """Both halves in one place, because §12 must add the first WITHOUT weakening
    the second: a share carries every dirty sidecar, and a Save still carries
    only its own document's."""
    repo, registry, created = _session_world(tmp_path)
    status, second = _act(repo, registry, "create-document", {
        "title": "Second Draft", "summary": "Another document.",
        "topics": ["alpha"], "area": f"ideation/staging/{TOPIC}/",
        "repository_context": repo.repository, "repository": repo.repository,
        **_scope()})
    assert status == 200, second

    first_thread = _write_thread(repo, created["path"], "notes on one")
    second_thread = _write_thread(repo, second["path"], "notes on two")

    # A Save of the FIRST document carries only the FIRST thread.
    status, edited = _save(repo, registry, created["path"],
                           "# First Draft\n\nsaved.\n")
    assert status == 200, edited
    assert first_thread not in _dirty(repo), (
        "the Save must carry its OWN document's sidecar (task 9.2)")
    assert second_thread in _dirty(repo), (
        "a Save must not sweep another document's sidecar")

    # The SHARE then carries what is left, across documents.
    status, shared = _share(repo, registry, RealPush(_worktree(repo)))
    assert status == 200, shared
    assert shared["threads"] == [second_thread]


def test_the_sweep_takes_dirty_paths_and_filters_by_prefix_and_suffix():
    assert dt.shareable_thread_paths([]) == ()
    assert dt.shareable_thread_paths(["ideation/docs/a.md"]) == ()
    assert dt.shareable_thread_paths(
        [f"{dt.THREAD_PREFIX}z/z.md{dt.THREAD_SUFFIX}",
         f"{dt.THREAD_PREFIX}a/a.md{dt.THREAD_SUFFIX}"]) == (
        f"{dt.THREAD_PREFIX}a/a.md{dt.THREAD_SUFFIX}",
        f"{dt.THREAD_PREFIX}z/z.md{dt.THREAD_SUFFIX}")
    # a file under the prefix that is NOT a sidecar is not swept
    assert dt.shareable_thread_paths([f"{dt.THREAD_PREFIX}README.md"]) == ()


# ===========================================================================
# THE RECORD — both residencies, both validated against the pinned schema
# ===========================================================================

def _validate(path: Path):
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                          capture_output=True, text=True)


def _assert_valid(path: Path) -> None:
    proc = _validate(path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 error(s)" in proc.stdout


@pytestmark_validator
def test_the_branch_resident_share_record_validates(tmp_path):
    """WITH dirty sidecars the record rides their commit onto the branch, so it
    is read back from the worktree — and it travels to the colleague."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])

    status, shared = _share(repo, registry, FakePullRequests())

    assert status == 200, shared
    assert shared["record_resident"] == "branch"
    record = _worktree(repo) / shared["record"]
    loaded = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_SHARE_SESSION
    assert loaded["target"]["ref"] == BRANCH
    assert [a["kind"] for a in loaded["artifacts"]] == [gc.ART_COMMIT]
    _assert_valid(record)


@pytestmark_validator
def test_the_main_resident_share_record_validates(tmp_path):
    """WITH nothing to commit there is nothing to co-commit, so the record is
    main-resident exactly as `open-pr`'s is."""
    repo, registry, created = _session_world(tmp_path)
    _save(repo, registry, created["path"], "# First Draft\n\nsaved.\n")

    status, shared = _share(repo, registry, RealPush(_worktree(repo)))

    assert status == 200, shared
    assert shared["record_resident"] == "main"
    record = repo.root / shared["record"]
    loaded = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_SHARE_SESSION
    assert loaded["target"]["ref"] == BRANCH
    assert loaded["artifacts"][0]["reference"] == f"refs/heads/{BRANCH}"
    _assert_valid(record)


def test_the_record_names_the_branch_and_the_pushed_ref(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    status, shared = _share(repo, registry, FakePullRequests())
    assert status == 200
    loaded = yaml.safe_load(
        (_worktree(repo) / shared["record"]).read_text(encoding="utf-8"))
    assert loaded["target"]["ref"] == shared["branch"]
    assert shared["pushed_ref"] == f"refs/heads/{loaded['target']['ref']}"


def test_the_action_is_in_the_pinned_schema_enum():
    """The contract-v1.36 growth this verb needed. Read from the schema itself,
    so a revert of that cut fails HERE rather than at record-write time."""
    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "schemas"
         / "gate-action-record.schema.yaml").read_text(encoding="utf-8"))
    assert gc.ACTION_SHARE_SESSION in schema["properties"]["action"]["enum"]


# ===========================================================================
# SHARING IS NOT PROMOTION (task 9.4's consumer)
# ===========================================================================

def test_the_verb_consults_the_promotion_exclusion_rather_than_restating_it():
    for prefix in dt.promotion_excluded_prefixes():
        assert prefix in gr.SHARE_IS_NOT_PROMOTION
    assert "promotes nothing" in gr.SHARE_IS_NOT_PROMOTION


def test_a_share_response_says_it_promoted_nothing(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"])
    status, shared = _share(repo, registry, FakePullRequests())
    assert status == 200
    assert "promoted" in shared["promotion"]


# ===========================================================================
# THE PLAN — a side-effect-free read, which is what makes 12.3 free
# ===========================================================================

def test_the_plan_touches_no_remote_and_no_index(tmp_path):
    repo, registry, created = _session_world(tmp_path)
    rel = _write_thread(repo, created["path"])
    _session, git = gr.resolve_session(
        (bs.STAGED_TOPIC, TOPIC), checkout_root=repo.root, registry=registry,
        repository=repo.repository, records_dir=RECORDS,
        tile_inventory=None, verb="share-session", require_live=True,
        remedy="")

    plan = gr.plan_share(git, worktree=_worktree(repo), branch=BRANCH)

    assert plan.threads == (rel,)
    assert plan.commits is True
    assert plan.unpushed is True
    assert plan.nothing_new is False
    assert _origin_sha(repo) is None          # read only: nothing was pushed
    assert rel in _dirty(repo)                # read only: nothing was staged


# ===========================================================================
# THE FAILURE WINDOW — the branch-resident record written BEFORE the push
#
# Adopted from the §12 adversarial review (P3-3), which reproduced it and ruled
# the design CONTAINED rather than broken. It is pinned here because
# "contained" is a claim about behaviour, and an unpinned claim about behaviour
# is a comment.
#
# The window exists because the two halves of a share cannot be made atomic: a
# branch-resident record must ride the commit it describes (FR-006), so it is
# written before the push it names. What makes that safe is not that the record
# is always true in isolation — it is that a record claiming an unshared push
# CANNOT BE READ BY ANYONE until the push it claims actually succeeds, because
# the only copy of it is on a branch no remote has.
# ===========================================================================

def test_a_failed_push_leaves_the_false_record_where_nobody_can_read_it(
        tmp_path):
    repo, registry, created = _session_world(tmp_path)
    rel = _write_thread(repo, created["path"], "written before the push failed")

    refusing = FakePullRequests(fail_push="the remote rejected this push")
    status, refused = _share(repo, registry, refusing)

    # the verb refuses, in the port's own words
    assert status == 409, refused
    assert refused["error"] == "gate_refused"
    assert "rejected this push" in json.dumps(refused)

    # the sidecar IS committed and the record IS on the branch — the window
    assert rel not in _dirty(repo), "the thread commit stands"
    branch_records = sorted(
        (_worktree(repo) / RECORDS).rglob("share-session-*.gate-action.yaml"))
    assert len(branch_records) == 1, branch_records

    # ...AND THE CONTAINMENT: nothing left the machine, so the record claiming a
    # share is unreachable by the colleague it would mislead.
    assert _origin_sha(repo) is None
    assert not list((repo.root / RECORDS).rglob(
        "share-session-*.gate-action.yaml")), (
        "no main-resident record may exist for a push that did not happen")


def test_the_retry_after_a_failed_push_self_heals(tmp_path):
    """The second half of the containment: the next invocation sees the branch
    as `unpushed` (nothing is dirty any more) and shares it for real."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"], "written before the push failed")
    _share(repo, registry, FakePullRequests(fail_push="the remote said no"))
    assert _origin_sha(repo) is None

    status, shared = _share(repo, registry, RealPush(_worktree(repo)))

    assert status == 200, shared
    assert shared["shared"] is True
    # nothing was dirty this time, so this share took the main-resident path
    assert shared["threads"] == []
    assert shared["record_resident"] == "main"
    assert _origin_sha(repo) is not None


def test_the_healed_trail_is_two_records_each_individually_truthful(tmp_path):
    """What an auditor finds afterwards, pinned so the composite is not a
    surprise: the BRANCH carries the failed attempt's record and the SERVED
    checkout carries the successful one."""
    repo, registry, created = _session_world(tmp_path)
    _write_thread(repo, created["path"], "the attempt that did not land")
    _share(repo, registry, FakePullRequests(fail_push="nope"))
    _share(repo, registry, RealPush(_worktree(repo)))

    on_branch = sorted(
        (_worktree(repo) / RECORDS).rglob("share-session-*.gate-action.yaml"))
    on_main = sorted(
        (repo.root / RECORDS).rglob("share-session-*.gate-action.yaml"))
    assert len(on_branch) == 1, on_branch
    assert len(on_main) == 1, on_main
    # and the colleague can now read the branch one, which by then is TRUE: the
    # branch really has been shared, by the retry.
    clone = _colleague_clone(tmp_path, repo)
    subprocess.run(["git", "-C", str(clone), "checkout", BRANCH],
                   check=True, capture_output=True, text=True)
    assert list((clone / RECORDS).rglob("share-session-*.gate-action.yaml"))
