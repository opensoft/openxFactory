"""The gate action as a TRANSACTION, and the merge ending as an OBSERVATION that
authorizes destruction (PR #49 adversarial review findings 1, 9 and 18).

Everything here is a regression: each test was written against the pre-fix code
first and FAILS on it. The three defects share one shape — a multi-step sequence
with no boundary, deciding on state it did not own.

**Finding 1 (Critical) — the commit was not bound to anything.** `commit_gate_action`
staged its paths and then ran a bare `git commit`, which commits the AMBIENT INDEX.
`SessionGit.staged_paths()`, written for exactly the missing check, had no caller at
all. Three reachable consequences, all reproduced by the review and all inverted
below: a pre-staged neighbour's file rode the action's commit; two overlapping
writers produced ONE commit carrying both actions' documents and records under only
the winner's `Gate-Action` trailer, while the loser was told it had failed; and —
with NO concurrency whatever — one failed commit left the action's own document and
record staged, so the human's retry committed TWO gate-action records in one commit,
one of them attesting to an action they had been told had failed. That last arm is
why the fix cannot be a `threading.Lock` and cannot be only a lock: the index must be
asserted, the commit must be bound to its declared paths, and a refusal must persist
nothing.

**Finding 9 (High) — reconciliation observed the wrong state and then destroyed.**
`merge_state` read only the LOCAL `main`, so a real GitHub merge (which advances the
REMOTE one) read as "not merged" and `open-pr` re-pushed the head branch the merge
had deleted. Its second half — "the tips differ" — is a property any EMPTY session
satisfies as soon as the base moves for any unrelated reason, so a session that had
written nothing was torn down and its branch deleted. And the verdict was never
re-checked before `git worktree remove --force` / `git branch -D`, so uncommitted
drafting and post-observation commits were destroyed with no recovery path.

**Finding 18 (Medium) — the immovability oracle's blind spot.** Covered in
`test_session_git.py`, where the guard and the fingerprint live.

House rules held throughout: scratch repos with LOCAL BARE remotes, `FakePullRequests`
and `FakeNotebookAdapter` at every seam, no network, no real `gh`, no real `nlm`
(`tests/hermeticity.py` makes both unreachable), and no real checkout is touched. The
concurrency tests interleave with injected BARRIERS and blocking pipe handshakes —
never a sleep, never a timing assumption.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT
from session_fixtures import (
    FakeNotebookAdapter, GATE_RECORDS_PREFIX, build_scratch_repo,
)

from ideation_dashboard import branch_session as bs
from ideation_dashboard import doxbench_hash as dh
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import session_git as sg
from ideation_dashboard import session_pr as spr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
DOC = "ideation/staging/demo-topic/note.md"
OTHER = "ideation/staging/demo-topic/somebody-elses-draft.md"
ALLOWLIST = (GATE_RECORDS_PREFIX, "ideation/staging/")
AT = "2026-07-27T12:00:00Z"


# --------------------------------------------------------------------------
# the world: a session worktree on a scratch checkout with a local bare origin
# --------------------------------------------------------------------------

@pytest.fixture
def session(scratch_repo):
    """The branch, its worktree, and a HumanGate rooted at the WORKTREE — the
    state every file-producing gate action starts from."""
    git = sg.SessionGit(scratch_repo.root)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    git.worktree_add(DRAFT, worktree, "main")
    gate = HumanGate(worktree, list(ALLOWLIST), human_actor="brett")
    return git, worktree, gate, scratch_repo


def _record(*, at: str = AT, action: str = gc.ACTION_EDIT_DOCUMENT,
            document: str = DOC) -> dict:
    stamp = bs.action_stamp(at)
    return gc.build_gate_action_record(
        actor="brett", action=action, at=at, ref=DRAFT, document=document,
        artifacts=[bs.commit_artifact(stamp)])


def _write(worktree: Path, relpath: str, text: str) -> str:
    target = worktree / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return relpath


def _act(gate, git, worktree, *, at: str = AT, documents=(DOC,), **over):
    return bs.commit_gate_action(gate, git, worktree=worktree, branch=DRAFT,
                                record=_record(at=at, document=documents[0]),
                                documents=list(documents), **over)


def _records_in(worktree: Path) -> list[Path]:
    return sorted((worktree / GATE_RECORDS_PREFIX).rglob("*.gate-action.yaml"))


def _committed_files(worktree: Path, sha: str) -> list[str]:
    out = subprocess.run(["git", "show", "--name-only", "--format=", sha],
                         cwd=str(worktree), text=True, capture_output=True,
                         check=True).stdout
    return sorted(l for l in out.split() if l)


def _tree_records(worktree: Path, sha: str) -> list[str]:
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha],
                         cwd=str(worktree), text=True, capture_output=True,
                         check=True).stdout
    return sorted(l for l in out.splitlines()
                  if l.strip().endswith(".gate-action.yaml"))


# ==========================================================================
# FINDING 1a — the commit is bound to its DECLARED paths, and a foreign index
# is a refusal rather than an ingredient
# ==========================================================================

def test_unrelated_pre_staged_work_refuses_the_action_instead_of_absorbing_it(
        session):
    """The review's REPRO 1, inverted. A shared checkout serves other sessions and
    other humans; `git add` is theirs to run. The action must not decide what to
    commit by reading an index it does not own."""
    git, worktree, gate, repo = session
    _write(worktree, OTHER, "someone else's paragraph\n")
    git.stage(worktree, [OTHER])                      # a NEIGHBOUR's staged work
    _write(worktree, DOC, "# Note\n\nmine.\n")
    ahead = git.commits_ahead("main", DRAFT)

    with pytest.raises(bs.SessionRefused) as exc:
        _act(gate, git, worktree)

    report = str(exc.value)
    assert OTHER in report, "the refusal must NAME the foreign path"
    assert "reset --" in report, "and give the human the remedy"
    # nothing of the action's own survives, and the neighbour's work is untouched
    assert git.commits_ahead("main", DRAFT) == ahead
    assert _records_in(worktree) == []
    assert git.staged_paths(worktree) == (OTHER,)
    assert (worktree / OTHER).read_text(encoding="utf-8") == \
        "someone else's paragraph\n"


def test_a_foreign_add_between_the_assertion_and_the_commit_cannot_enter_it(
        session):
    """The assertion alone would leave a window: another process may `git add`
    after the index has been checked. `git commit --only -- <declared>` closes it,
    so the binding does not depend on the check winning a race."""
    git, worktree, gate, repo = session
    _write(worktree, DOC, "# Note\n")
    _write(worktree, OTHER, "landed mid-action\n")
    real_commit = git.commit

    def commit_with_an_intruder(root, message, **kwargs):
        # exactly the interleaving the lock cannot prevent: a git process that is
        # not a session writer at all
        subprocess.run(["git", "add", "--", OTHER], cwd=str(worktree), check=True)
        return real_commit(root, message, **kwargs)

    git.commit = commit_with_an_intruder                          # type: ignore
    result = _act(gate, git, worktree)

    assert _committed_files(worktree, result.sha) == sorted(
        [DOC, result.record_relpath])
    assert OTHER not in _committed_files(worktree, result.sha)
    assert git.staged_paths(worktree) == (OTHER,), (
        "the intruder's path is still staged — untouched, and uncommitted")


def test_the_index_is_asserted_to_be_exactly_the_declared_set_after_staging(
        session):
    """SC-003's assertion, made against `staged_paths()` — the helper that existed
    for this check and had no caller. A `stage()` that quietly staged more (a
    pathspec that matched a sibling, a hook) must refuse, not commit."""
    git, worktree, gate, repo = session
    _write(worktree, DOC, "# Note\n")
    _write(worktree, OTHER, "swept in by a broken stage\n")
    real_stage = git.stage

    def stage_too_much(root, paths):
        staged = real_stage(root, paths)
        subprocess.run(["git", "add", "--", OTHER], cwd=str(worktree), check=True)
        return staged

    git.stage = stage_too_much                                    # type: ignore
    ahead = git.commits_ahead("main", DRAFT)

    with pytest.raises(bs.SessionRefused) as exc:
        _act(gate, git, worktree)

    assert "declared" in str(exc.value)
    assert git.commits_ahead("main", DRAFT) == ahead
    assert _records_in(worktree) == []


# ==========================================================================
# FINDING 1b — the action owns the worktree's index for its whole duration,
# across THREADS and across PROCESSES
# ==========================================================================

def test_two_threads_writing_one_session_produce_one_commit_each_and_a_refusal(
        session):
    """The review's REPRO 2, inverted, with a DETERMINISTIC interleaving.

    Writer A is held INSIDE its transaction (a barrier in its `stage`) while writer
    B attempts the whole action. Before the fix, B staged into the same index and
    A's commit carried A's document, B's document, A's record AND B's record under
    A's `Gate-Action` trailer, while B was handed a raw `index.lock` `GitError`.
    Now B is refused before it writes anything, and A's commit is exactly A's."""
    git, worktree, gate, repo = session
    a_doc = _write(worktree, "ideation/staging/demo-topic/a.md", "# A\n")
    b_doc = _write(worktree, "ideation/staging/demo-topic/b.md", "# B\n")

    a_is_inside = threading.Event()
    b_is_done = threading.Event()
    real_stage = git.stage

    def stage_then_wait(root, paths):
        staged = real_stage(root, paths)
        a_is_inside.set()
        assert b_is_done.wait(timeout=30), "the second writer never finished"
        return staged

    git.stage = stage_then_wait                                   # type: ignore
    outcome: dict = {}

    def writer_a():
        try:
            outcome["a"] = _act(gate, git, worktree,
                                at="2026-07-27T12:00:00Z", documents=(a_doc,))
        except BaseException as exc:                              # noqa: BLE001
            outcome["a"] = exc

    thread = threading.Thread(target=writer_a, daemon=True)
    thread.start()
    assert a_is_inside.wait(timeout=30), "the first writer never entered its action"

    # B is a SEPARATE SessionGit, exactly as a second request would be
    b_git = sg.SessionGit(repo.root)
    b_gate = HumanGate(worktree, list(ALLOWLIST), human_actor="brett")
    with pytest.raises(bs.SessionRefused) as exc:
        _act(b_gate, b_git, worktree, at="2026-07-27T12:00:01Z",
             documents=(b_doc,))
    b_report = str(exc.value)

    b_is_done.set()
    thread.join(timeout=30)
    assert not thread.is_alive()

    assert "already owns this session worktree's index" in b_report
    assert isinstance(outcome["a"], bs.GateActionCommit), outcome["a"]
    a_commit = outcome["a"]
    # A's commit is A's alone: ONE record, ONE document
    assert _committed_files(worktree, a_commit.sha) == sorted(
        [a_doc, a_commit.record_relpath])
    assert _tree_records(worktree, a_commit.sha) == [a_commit.record_relpath]
    assert git.commits_ahead("main", DRAFT) == 1
    # B persisted NOTHING — no record file, no staged path, no commit
    assert _records_in(worktree) == [worktree / a_commit.record_relpath]
    assert git.staged_paths(worktree) == ()

    # and B's retry, now that the lock is free, is an ordinary success
    retried = _act(b_gate, b_git, worktree, at="2026-07-27T12:00:02Z",
                   documents=(b_doc,))
    assert git.commits_ahead("main", DRAFT) == 2
    assert _tree_records(worktree, retried.sha) == sorted(
        [a_commit.record_relpath, retried.record_relpath])
    assert _committed_files(worktree, retried.sha) == sorted(
        [b_doc, retried.record_relpath])


LOCK_HOLDER = r"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from ideation_dashboard import session_git as sg

git = sg.SessionGit(sys.argv[2])
with git.worktree_action_lock(Path(sys.argv[3]), action="a rival CLI verb"):
    sys.stdout.write("held\n")
    sys.stdout.flush()
    sys.stdin.readline()          # blocks until the parent says go — no sleeps
sys.stdout.write("released\n")
sys.stdout.flush()
"""


def test_a_separate_process_holding_the_lock_refuses_the_in_process_action(
        session, tmp_path):
    """CLI PARITY (FR-024) is why a `threading.Lock` could never be the fix: the
    second writer is routinely `cli.py gate edit-document` in its OWN process,
    beside a `ThreadingHTTPServer` request. The lock is a file in the worktree's
    git dir, so it is visible across processes — proved here with a real child
    process and a blocking pipe handshake rather than any timing."""
    git, worktree, gate, repo = session
    _write(worktree, DOC, "# Note\n")
    script = tmp_path / "hold_the_lock.py"
    script.write_text(LOCK_HOLDER, encoding="utf-8")

    child = subprocess.Popen(
        [sys.executable, str(script), str(REPO_ROOT / "scripts"),
         str(repo.root), str(worktree)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        assert child.stdout.readline().strip() == "held"
        assert git.read_action_lock(worktree)["pid"] == child.pid

        with pytest.raises(bs.SessionRefused) as exc:
            _act(gate, git, worktree)
        report = str(exc.value)
        assert "a rival CLI verb" in report
        assert str(child.pid) in report

        assert _records_in(worktree) == []
        assert git.staged_paths(worktree) == ()
        assert git.commits_ahead("main", DRAFT) == 0
    finally:
        child.stdin.write("go\n")
        child.stdin.flush()
        child.wait(timeout=30)
    assert child.returncode == 0
    assert git.read_action_lock(worktree) is None

    # the lock released with the process: the same action now succeeds
    result = _act(gate, git, worktree)
    assert git.commits_ahead("main", DRAFT) == 1
    assert _committed_files(worktree, result.sha) == sorted(
        [DOC, result.record_relpath])


def test_a_lock_left_by_a_dead_process_is_broken_rather_than_deadlocking(
        session):
    """A crashed writer must not wedge the session forever. A holder whose pid is
    gone ON THIS HOST is conclusive — its index work is over by definition — and
    the emptiness assertion inside the action is what protects against residue it
    may have left."""
    git, worktree, gate, _ = session
    lock = git.action_lock_path(worktree)
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    lock.write_text(json.dumps({"pid": dead.pid, "host": socket.gethostname(),
                                "action": "a crashed writer",
                                "created": time.time()}), encoding="utf-8")
    _write(worktree, DOC, "# Note\n")

    result = _act(gate, git, worktree)

    assert git.commits_ahead("main", DRAFT) == 1
    assert _committed_files(worktree, result.sha) == sorted(
        [DOC, result.record_relpath])


def test_a_live_holder_is_never_broken_on_age_alone(session):
    """The staleness window is a fallback for a holder this process cannot
    interrogate, not a general licence: a LIVE pid stays authoritative however the
    window is set."""
    git, worktree, gate, _ = session
    lock = git.action_lock_path(worktree)
    holder = {"pid": os.getpid(), "host": socket.gethostname(),
              "action": "this very test", "created": 0}
    lock.write_text(json.dumps(holder), encoding="utf-8")
    assert sg.lock_is_stale(lock, holder, stale_seconds=0) is False, (
        "a LIVE holder is authoritative however old its lock is — breaking it on "
        "age would put two writers inside one index, which is the defect itself")
    _write(worktree, DOC, "# Note\n")
    with pytest.raises(bs.SessionRefused):
        _act(gate, git, worktree)
    lock.unlink()


# ==========================================================================
# FINDING 1c — every failure arm persists NOTHING, and the retry after one is
# exactly ONE record in ONE commit
# ==========================================================================

def _assert_no_residue(git, worktree, *, ahead: int, head: str,
                       document: str = DOC, document_gone: bool = True):
    """A refusal persists nothing: no commit, no record, no staged path, and — for
    a document this action CREATED — no orphan file either."""
    assert git.commits_ahead("main", DRAFT) == ahead
    assert git.head(worktree) == head
    assert _records_in(worktree) == []
    assert git.staged_paths(worktree) == ()
    if document_gone:
        assert not (worktree / document).exists()


def test_a_record_write_failure_leaves_nothing_behind(session, monkeypatch):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    head = git.head(worktree)
    monkeypatch.setattr(gc, "write_gate_action_record",
                        lambda *a, **k: (_ for _ in ()).throw(
                            OSError("the records volume is full")))

    with pytest.raises(OSError):
        _act(gate, git, worktree)

    _assert_no_residue(git, worktree, ahead=0, head=head)


def test_a_stage_failure_leaves_nothing_behind(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    head = git.head(worktree)

    def refuse(root, paths):
        raise sg.GitError(("add",), 128, "index.lock: File exists")

    git.stage = refuse                                            # type: ignore
    with pytest.raises(sg.GitError):
        _act(gate, git, worktree)

    _assert_no_residue(git, worktree, ahead=0, head=head)


def test_a_commit_failure_leaves_nothing_staged_and_no_record(session):
    """The review's REPRO 3, first half: this is the arm that needed NO second
    writer at all. Before the fix it left the action's document AND record staged,
    which is what made the retry commit two records."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    head = git.head(worktree)

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "unable to write new_index file")

    git.commit = refuse                                           # type: ignore
    with pytest.raises(sg.GitError):
        _act(gate, git, worktree)

    _assert_no_residue(git, worktree, ahead=0, head=head)


def test_a_post_commit_verification_failure_undoes_its_own_commit(session):
    """The last arm: the commit exists and the introduced-by check refuses it. The
    unwind is `reset --soft` back to the sha captured before the commit, so HEAD
    returns and the WORKING TREE is never touched — the commit was made moments
    earlier inside this action's own lock, so nothing but this action is undone."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    head = git.head(worktree)
    git.introduced_by = lambda *a, **k: "0" * 40                  # type: ignore

    with pytest.raises(bs.SessionRefused) as exc:
        _act(gate, git, worktree)

    assert "ONE commit" in str(exc.value)
    _assert_no_residue(git, worktree, ahead=0, head=head)


def test_a_tracked_document_is_left_exactly_as_the_action_found_it(session):
    """The unwind removes what the ACTION created; it never reverts a document git
    already tracks. Reverting one would discard whatever was in the working tree,
    which belongs to the human, not to this function — the same class of harm as
    finding 9's force-removal."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    first = _act(gate, git, worktree)
    rewritten = "# Note\n\nthe rewrite whose commit fails.\n"
    _write(worktree, DOC, rewritten)
    head = git.head(worktree)

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "disk full")

    git.commit = refuse                                           # type: ignore
    with pytest.raises(sg.GitError):
        _act(gate, git, worktree, at="2026-07-27T12:00:05Z")

    assert git.head(worktree) == head
    assert git.staged_paths(worktree) == ()
    assert _records_in(worktree) == [worktree / first.record_relpath]
    assert (worktree / DOC).read_text(encoding="utf-8") == rewritten, (
        "the human's bytes stay in the worktree; only the ACTION is undone")


def test_a_retry_after_a_failed_attempt_is_exactly_one_record_in_one_commit(
        session):
    """The review's REPRO 3, second half — the whole reason finding 1 is Critical
    without any concurrency. One transient commit failure, then the human retries;
    before the fix the retry's single commit carried TWO gate-action records, one of
    them attesting to an action the human had been told had failed."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    real_commit = git.commit
    attempts = {"n": 0}

    def fail_once(root, message, **kwargs):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise sg.GitError(("commit",), 128, "transient failure")
        return real_commit(root, message, **kwargs)

    git.commit = fail_once                                        # type: ignore
    with pytest.raises(sg.GitError):
        _act(gate, git, worktree, at="2026-07-27T12:00:00Z")

    # the retry is a FRESH action with its own stamp, as the human's re-post is
    _write(worktree, DOC, "# Note\n")
    result = _act(gate, git, worktree, at="2026-07-27T12:00:05Z")

    assert git.commits_ahead("main", DRAFT) == 1
    assert _tree_records(worktree, result.sha) == [result.record_relpath]
    assert _committed_files(worktree, result.sha) == sorted(
        [DOC, result.record_relpath])
    assert len(_records_in(worktree)) == 1
    stamps = [yaml.safe_load(p.read_text(encoding="utf-8"))["at"]
              for p in _records_in(worktree)]
    assert stamps == ["2026-07-27T12:00:05Z"], (
        "the refused attempt's record must not survive its refusal")


def test_the_sha_comes_from_the_commit_that_was_made_and_is_not_in_the_record(
        session):
    """Preserved properties, re-pinned because the transaction moved around them:
    the sha is captured inside the lock from the commit actually created, and it is
    never written into the record (FR-006)."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    result = _act(gate, git, worktree)

    assert result.sha == git.head(worktree)
    committed = git.git(worktree, "show", f"{result.sha}:{result.record_relpath}")
    assert result.sha not in committed
    assert yaml.safe_load(committed)["artifacts"] == [
        {"kind": gc.ART_COMMIT, "reference": result.stamp}]


# ==========================================================================
# FINDING 9 — the merge is OBSERVED correctly before anything is destroyed
# ==========================================================================

def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _live_session(repo, tmp_path, *, write=True):
    """A live session with one gate-action commit on its branch."""
    registry = _registry(repo, tmp_path)
    git = sg.SessionGit(repo.root)
    opened = bs.open_session(git, registry, repository=repo.repository,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                             checkout_root=repo.root)
    if write:
        gate = HumanGate(opened.worktree, list(ALLOWLIST), human_actor="brett")
        _write(opened.worktree, DOC, "# Note\n\nthe session's work.\n")
        bs.commit_gate_action(gate, git, worktree=opened.worktree, branch=DRAFT,
                              record=_record(), documents=[DOC])
    return registry, git, opened


def _merge_in_the_bare_origin(repo, tmp_path, branch=DRAFT, *,
                              delete_head=True) -> str:
    """The Merge Master's action as it REALLY happens: on the remote, by somebody
    else, with the served checkout never told. Performed in a second clone of the
    bare origin and pushed, then the head branch is auto-deleted — and NOTHING
    fetches, so the served checkout still shows the pre-merge `main`."""
    elsewhere = tmp_path / "merge-master-clone"
    subprocess.run(["git", "clone", "--quiet", str(repo.origin), str(elsewhere)],
                   check=True, capture_output=True)

    def run(*args):
        return subprocess.run(["git", *args], cwd=str(elsewhere), check=True,
                              text=True, capture_output=True).stdout.strip()

    run("config", "user.email", "merge-master@example.invalid")
    run("config", "user.name", "Merge Master")
    run("config", "commit.gpgsign", "false")
    run("merge", "--no-ff", "-m", f"Merge pull request for {branch}",
        f"origin/{branch}")
    run("push", "origin", "main")
    if delete_head:
        run("push", "origin", "--delete", branch)
    return run("rev-parse", "HEAD")


def _unrelated_commit_in_the_bare_origin(repo, tmp_path, *,
                                         name="somebody-else") -> str:
    """Somebody ELSE advances `origin/main`, in a second clone, and the served
    checkout is never told. This is not a merge of anything — it is the ordinary
    daily traffic of a SHARED served checkout, which is why "local `main` lags the
    remote" is that checkout's steady state (critic finding C2)."""
    elsewhere = tmp_path / f"{name}-clone"
    subprocess.run(["git", "clone", "--quiet", str(repo.origin), str(elsewhere)],
                   check=True, capture_output=True)

    def run(*args):
        return subprocess.run(["git", *args], cwd=str(elsewhere), check=True,
                              text=True, capture_output=True).stdout.strip()

    run("config", "user.email", f"{name}@example.invalid")
    run("config", "user.name", name)
    run("config", "commit.gpgsign", "false")
    target = elsewhere / "ideation" / "staging" / "demo-topic" / f"{name}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"# {name}\n\nunrelated work on main.\n", encoding="utf-8")
    run("add", "--", "ideation/staging/demo-topic/" + target.name)
    run("commit", "-m", f"{name}: an unrelated commit on main")
    run("push", "origin", "main")
    return run("rev-parse", "HEAD")


def _save(repo, registry, *, port, at=None):
    """One `open-pr` through the route — the save verb, as the human reaches it."""
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC}
    if at:
        body["at"] = at
    return gr.run_gate_action(
        "open-pr", body, checkout_root=repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=repo.repository, session_pull_requests=port)


# --------------------------------------------------------------------------
# critic finding C2 — a stale base gates the MERGE OBSERVATION, and nothing else
#
# The wave-1 repair for finding 9 made `open-pr` refuse whenever the served
# checkout's `main` lagged the remote's. On the shared checkout T092 drives, that
# is the STEADY STATE — so the save verb, the entire point of the feature,
# refused in normal operation, with a merge narrative about a branch that had
# never been pushed and therefore could not have merged. The two arms below are
# the two halves that have to hold at once.
# --------------------------------------------------------------------------

def test_the_first_save_of_a_never_pushed_session_survives_a_lagging_main(
        scratch_repo, tmp_path):
    """ARM 1 (the regression): a never-pushed session SAVES while local `main`
    merely lags `origin/main`. Nothing about that gap can hide a merge of a branch
    no pull request has ever seen."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    assert DRAFT not in scratch_repo.origin_branches()      # never pushed
    assert git.tracking_sha(DRAFT) is None                  # and never pushed FROM here
    remote_main = _unrelated_commit_in_the_bare_origin(scratch_repo, tmp_path)
    assert scratch_repo.head("main") != remote_main

    state = bs.merge_state(git, DRAFT)

    assert state.base_stale is False, state.reason
    assert state.merged is False
    assert state.remote_base == remote_main
    assert "has never left this checkout" in state.reason

    port = spr.FakePullRequests()
    status, payload = _save(scratch_repo, registry, port=port)

    assert status == 200, payload
    assert payload["pull_request"] == "https://example.invalid/pr/1"
    assert payload["merged"] is False
    assert ("push", DRAFT) in port.calls
    assert (scratch_repo.root / payload["record"]).is_file()


def test_a_save_after_a_dispatch_still_refuses_on_a_base_it_cannot_see(
        scratch_repo, tmp_path):
    """ARM 2 (finding 9's guarantee, intact): once the branch HAS been dispatched,
    a base this checkout cannot see blocks both answers again — because now the
    merge it cannot see may have happened, and the re-push would resurrect the head
    branch that merge deleted. The evidence here is the main-resident `open-pr`
    record alone: `FakePullRequests` never touches git, so there is no remote head
    and no remote-tracking ref to read."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    first = _save(scratch_repo, registry, port=port, at="2026-07-27T12:00:01Z")
    assert first[0] == 200, first[1]
    assert gr.dispatch_records_for(scratch_repo.root, gc.DEFAULT_RECORDS_DIR, DRAFT)
    remote_main = _unrelated_commit_in_the_bare_origin(scratch_repo, tmp_path)

    status, payload = _save(scratch_repo, registry, port=port,
                            at="2026-07-27T12:00:02Z")

    assert status == 409, payload
    assert "cannot be observed" in payload["message"]
    assert remote_main in payload["message"]
    assert "`open-pr` record already names" in payload["message"]
    assert port.calls.count(("push", DRAFT)) == 1, "nothing was pushed a second time"


def test_a_hand_pushed_branch_is_dispatch_enough_to_gate_the_stale_base(
        scratch_repo, tmp_path):
    """ARM 2, second signal: the remote-tracking ref. A branch pushed from this
    checkout leaves one, and it OUTLIVES the remote head a merge deletes — so it,
    not the presence of a remote head, is what says "this branch could already have
    landed"."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    scratch_repo.git("push", "origin", DRAFT)
    # the head branch is deleted where a merge deletes it — ON THE REMOTE, by
    # somebody else. The served checkout is never told, so its remote-tracking ref
    # for the branch survives (nothing here fetches, let alone prunes).
    scratch_repo.git("update-ref", "-d", f"refs/heads/{DRAFT}",
                     cwd=scratch_repo.origin)
    assert DRAFT not in scratch_repo.origin_branches()
    assert git.remote_sha(DRAFT) is None
    assert git.tracking_sha(DRAFT) is not None               # the surviving trace
    _unrelated_commit_in_the_bare_origin(scratch_repo, tmp_path)

    state = bs.merge_state(git, DRAFT)

    assert state.base_stale is True, state.reason
    assert "remote-tracking ref" in state.reason
    port = spr.FakePullRequests()
    status, payload = _save(scratch_repo, registry, port=port)
    assert status == 409, payload
    assert port.calls == [], "nothing was pushed and no pull request was touched"


def test_a_merge_that_only_the_remote_can_see_blocks_both_answers(
        scratch_repo, tmp_path):
    """The review's repro B, inverted. A real merge advances the REMOTE `main`;
    reading only the local one answered "not merged" with confidence and `open-pr`
    then RE-PUSHED the head branch the merge had just deleted. `ls-remote` is
    already permitted and side-effect-free (FR-026/D17 forbids only `fetch`), so the
    remote base is read, the mismatch is reported, and neither the teardown nor the
    push happens."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    scratch_repo.git("push", "origin", DRAFT)
    remote_main = _merge_in_the_bare_origin(scratch_repo, tmp_path)
    local_main = scratch_repo.head("main")
    assert remote_main != local_main

    state = bs.merge_state(git, DRAFT)

    assert state.base_stale is True
    assert state.merged is False
    assert state.remote_base == remote_main
    assert remote_main in state.reason and local_main in state.reason
    # the reconciliation destroys nothing on a base it cannot see
    reconciled = bs.reconcile_merged_session(git, opened,
                                             checkout_root=scratch_repo.root)
    assert reconciled.merged is False
    assert git.branch_exists(DRAFT) is True
    assert Path(opened.worktree).is_dir()

    # and the SAVE refuses rather than resurrecting the deleted head branch
    port = spr.FakePullRequests()
    status, payload = gr.run_gate_action(
        "open-pr", {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC},
        checkout_root=scratch_repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=scratch_repo.repository,
        session_pull_requests=port)
    assert status == 409, payload
    assert "does not contain" in payload["message"]
    assert remote_main in payload["message"]
    assert port.calls == [], "nothing was pushed and no pull request was touched"
    assert DRAFT not in scratch_repo.origin_branches()


def test_an_empty_session_is_never_merged_however_far_the_base_moves(
        scratch_repo, tmp_path):
    """The review's repro A, inverted. "Contained AND the tips differ" is satisfied
    by an EMPTY session as soon as `main` moves for ANY reason: one unrelated commit
    made a session that had written nothing look merged, and the reconciliation
    deleted its branch and force-removed its worktree. The observation now requires
    a merge commit that names THIS branch's tip as a merged parent, which an empty
    branch's tip — a base commit, and therefore only ever a FIRST parent — cannot
    be."""
    registry, git, opened = _live_session(scratch_repo, tmp_path, write=False)
    assert git.commits_ahead("main", DRAFT) == 0
    scratch_repo.write("ideation/staging/demo-topic/unrelated.md", "elsewhere\n")
    scratch_repo.commit("An unrelated commit on main",
                        "ideation/staging/demo-topic/unrelated.md")
    # and a real merge of ANOTHER branch, whose merge commit the empty tip is the
    # FIRST parent of — the sharpest form of the trap
    scratch_repo.git("branch", "other/work", "main")
    subprocess.run(["git", "worktree", "add", "--quiet",
                    str(tmp_path / "other-wt"), "other/work"],
                   cwd=str(scratch_repo.root), check=True, capture_output=True)
    scratch_repo.write("ideation/staging/demo-topic/theirs.md", "theirs\n",
                       cwd=tmp_path / "other-wt")
    scratch_repo.commit("Their work", "ideation/staging/demo-topic/theirs.md",
                        cwd=tmp_path / "other-wt")
    scratch_repo.git("merge", "--no-ff", "-m", "Merge other/work", "other/work")

    state = bs.merge_state(git, DRAFT)

    assert state.merged is False
    assert state.landed_by is None
    assert "delete a branch nobody merged" in state.reason
    assert bs.reconcile_merged_session(
        git, opened, checkout_root=scratch_repo.root).merged is False
    assert git.branch_exists(DRAFT) is True
    assert Path(opened.worktree).is_dir()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True


def test_a_real_merge_commit_is_still_recognised_and_names_its_landing(
        scratch_repo, tmp_path):
    """The positive control for the two tests above: the D18 shape is recognised,
    and the verdict now says WHICH merge commit landed the branch."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    tip = git.head(ref=DRAFT)
    scratch_repo.git("merge", "--no-ff", "-m", f"Merge {DRAFT}", DRAFT)
    landing = scratch_repo.head("main")

    state = bs.merge_state(git, DRAFT)

    assert state.merged is True
    assert state.tip == tip
    assert state.landed_by == landing
    assert landing in state.reason


def test_a_commit_landing_after_the_observation_is_not_deleted(scratch_repo,
                                                              tmp_path):
    """The review's repro C, inverted, with the interleaving injected at the exact
    window that existed: observe → [a gate action commits] → destroy. Before the
    fix the teardown force-removed the worktree and `git branch -D`'d the branch on
    the OLD verdict, and `git branch --contains <sha>` answered `<none>` — the
    commit was unreachable from any ref, with no recovery path in the response."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    scratch_repo.git("merge", "--no-ff", "-m", f"Merge {DRAFT}", DRAFT)
    gate = HumanGate(opened.worktree, list(ALLOWLIST), human_actor="brett")
    landed: dict = {}
    real_dirty = git.dirty_paths

    def commit_between_the_two_observations(worktree):
        # called exactly once, between the verdict and the re-observation
        if not landed:
            landed["busy"] = True
            _write(Path(opened.worktree), DOC, "# Note\n\nafter the merge.\n")
            landed["sha"] = bs.commit_gate_action(
                gate, git, worktree=opened.worktree, branch=DRAFT,
                record=_record(at="2026-07-27T12:00:09Z"), documents=[DOC]).sha
        return real_dirty(worktree)

    git.dirty_paths = commit_between_the_two_observations         # type: ignore

    with pytest.raises(bs.SessionRefused) as exc:
        bs.reconcile_merged_session(git, opened, checkout_root=scratch_repo.root)

    assert "no longer holds" in str(exc.value)
    assert landed["sha"]
    containing = subprocess.run(
        ["git", "branch", "--contains", landed["sha"], "--format=%(refname:short)"],
        cwd=str(scratch_repo.root), text=True, capture_output=True,
        check=True).stdout.split()
    assert DRAFT in containing, "the post-observation commit is still reachable"
    assert git.branch_exists(DRAFT) is True
    assert Path(opened.worktree).is_dir()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True


def test_the_teardown_refuses_a_stale_compare_and_swap_before_destroying(
        scratch_repo, tmp_path):
    """The compare-and-swap is a PRECONDITION of the teardown, not a courtesy of
    the caller: `expect_branch_sha` is checked before the registry entry is dropped
    and before `git worktree remove --force` runs, so a mismatch destroys nothing at
    all."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)

    with pytest.raises(bs.SessionRefused) as exc:
        bs.teardown_session(git, opened, checkout_root=scratch_repo.root,
                            registry=registry, delete_branch=True,
                            expect_branch_sha="0" * 40)

    assert "unreachable from any ref" in str(exc.value)
    assert Path(opened.worktree).is_dir()
    assert git.branch_exists(DRAFT) is True
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True


def test_a_merged_session_holding_uncommitted_work_is_not_force_removed(
        scratch_repo, tmp_path):
    """The review's repro E, inverted: `git worktree remove --force` deleted an
    in-progress document outright (`draft still on disk: False`). The merge ending
    holds no authority to discard drafting — `abandon-session` does (FR-022) — so it
    refuses and names both routes that keep the work."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    scratch_repo.git("merge", "--no-ff", "-m", f"Merge {DRAFT}", DRAFT)
    draft = Path(opened.worktree) / "ideation/staging/demo-topic/in-progress.md"
    draft.write_text("# Still writing this\n", encoding="utf-8")

    with pytest.raises(bs.SessionRefused) as exc:
        bs.reconcile_merged_session(git, opened, checkout_root=scratch_repo.root,
                                    registry=registry)

    report = str(exc.value)
    assert "in-progress.md" in report
    assert "abandon-session" in report
    assert draft.read_text(encoding="utf-8") == "# Still writing this\n"
    assert git.branch_exists(DRAFT) is True
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True


def test_a_refused_remote_delete_leaves_the_local_ref_so_the_delete_retries(
        scratch_repo, tmp_path):
    """The review's repro D, inverted. `git branch -D` is irreversible and the push
    is the fallible half, so the local delete ran first and left the remote branch
    alive with no local ref — and the next observation answered "no such branch,
    nothing to reconcile", i.e. the reconciliation could never be retried. The
    remote delete now goes FIRST."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    scratch_repo.git("push", "origin", DRAFT)
    scratch_repo.git("config", "receive.denyDeletes", "true", cwd=scratch_repo.origin)
    scratch_repo.git("merge", "--no-ff", "-m", f"Merge {DRAFT}", DRAFT)

    result = bs.reconcile_merged_session(git, opened,
                                        checkout_root=scratch_repo.root,
                                        registry=registry)

    assert result.merged is True
    assert result.teardown.branch_deleted is False
    assert result.teardown.branch_retained is True
    assert any("could not be deleted" in n for n in result.teardown.notes)
    assert git.branch_exists(DRAFT) is True, "the local ref survives the failure"
    assert DRAFT in scratch_repo.origin_branches()
    # and the delete is RETRYABLE: the observation still answers "merged"
    assert bs.merge_state(git, DRAFT).merged is True
    scratch_repo.git("config", "--unset", "receive.denyDeletes",
                     cwd=scratch_repo.origin)
    git.delete_branch(DRAFT, remote=True, safe=True)
    assert git.branch_exists(DRAFT) is False
    assert DRAFT not in scratch_repo.origin_branches()


def test_the_happy_merge_ending_still_ends_the_session_and_deletes_the_branch(
        scratch_repo, tmp_path):
    """The positive control for the whole finding-9 section: with a clean worktree,
    a real merge commit, and a stable tip, the ending is exactly what FR-033 says —
    and the branch delete is now git's own SAFE delete, which re-verifies
    containment rather than taking the caller's word for it."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    notebook.create(opened.notebook_alias)
    scratch_repo.git("merge", "--no-ff", "-m", f"Merge {DRAFT}", DRAFT)

    result = bs.reconcile_merged_session(git, opened,
                                        checkout_root=scratch_repo.root,
                                        registry=registry, notebook=notebook)

    assert result.merged is True
    assert sorted(result.teardown.torn_down) == ["notebook", "registry-entry",
                                                 "worktree"]
    assert result.teardown.branch_deleted is True
    assert result.teardown.branch_retained is False
    assert git.branch_exists(DRAFT) is False
    assert not Path(opened.worktree).exists()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is False


def test_an_unwind_refuses_when_the_branch_moved_after_it_read_as_empty(
        scratch_repo, tmp_path, monkeypatch):
    """Finding 9's RESIDUAL, closed (wave 2): the one neighbouring destructive site
    that was not compare-and-swapped.

    `unwind_opened_session` (the finding-3 repair) reads `commits_ahead` and then
    calls `teardown_session(delete_branch=True)`. With a second actor's gate-action
    commit landing in that window, the unwind force-removed the worktree and deleted
    the branch: `git branch --contains <sha>` answered `<none>`, the commit survived
    only as unreferenced garbage, and the returned notes were EMPTY, so the human was
    told nothing at all.

    The interleaving is DETERMINISTIC — the rival commit is made inside the
    `commits_ahead` read itself, which is exactly the window, with no sleep and no
    timing assumption."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    opened = bs.open_session(git, registry, repository=scratch_repo.repository,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                             checkout_root=scratch_repo.root)
    assert opened.joined is False
    real_commits_ahead = git.commits_ahead
    rival: dict = {}

    def commit_then_answer(base, branch):
        answer = real_commits_ahead(base, branch)        # reads 0 — the window opens
        if not rival:
            gate = HumanGate(opened.worktree, list(ALLOWLIST), human_actor="dana")
            _write(opened.worktree, DOC, "# the rival's work\n")
            rival["commit"] = bs.commit_gate_action(
                gate, git, worktree=opened.worktree, branch=DRAFT,
                record=_record(at="2026-07-27T12:00:09Z"), documents=[DOC])
        return answer

    git.commits_ahead = commit_then_answer                        # type: ignore

    notes = bs.unwind_opened_session(git, opened,
                                     checkout_root=scratch_repo.root)

    git.commits_ahead = real_commits_ahead                        # type: ignore
    assert notes, "an unwind that destroys nothing must say so — empty notes are the defect"
    assert "MOVED" in notes[0] and "NOT unwound" in notes[0]
    assert rival["commit"].sha[:12] in notes[0] or rival["commit"].sha in notes[0]
    # nothing was destroyed, and the rival's commit is reachable from its branch
    assert git.branch_exists(DRAFT) is True
    assert Path(opened.worktree).is_dir()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True
    contains = git.git(scratch_repo.root, "branch", "--contains",
                       rival["commit"].sha)
    assert DRAFT in contains


def test_an_unwind_of_a_genuinely_empty_session_still_removes_everything(
        scratch_repo, tmp_path):
    """The control the compare-and-swap must not break: with nothing landing in the
    window, a refused FIRST action still leaves no phantom session (finding 3's whole
    point). Without this the fix above could pass by refusing every unwind."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    opened = bs.open_session(git, registry, repository=scratch_repo.repository,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                             checkout_root=scratch_repo.root)

    notes = bs.unwind_opened_session(git, opened,
                                     checkout_root=scratch_repo.root)

    assert notes == ()
    assert git.branch_exists(DRAFT) is False
    assert not Path(opened.worktree).exists()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is False


# ==========================================================================
# FINDING 1's PUBLIC SURFACES — the 409 carries the engine's own lock reason,
# and says the rewrite is already on disk
# ==========================================================================

def _lock_holder(repo, worktree, tmp_path):
    """A REAL second process holding the action lock, handshaked over a pipe."""
    script = tmp_path / "hold_the_lock_for_a_route.py"
    script.write_text(LOCK_HOLDER, encoding="utf-8")
    child = subprocess.Popen(
        [sys.executable, str(script), str(REPO_ROOT / "scripts"),
         str(repo.root), str(worktree)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    assert child.stdout.readline().strip() == "held"
    return child


def _release(child):
    child.stdin.write("go\n")
    child.stdin.flush()
    child.wait(timeout=30)
    assert child.returncode == 0


def _open_through_the_route(repo, tmp_path):
    """One `create-document` through the ROUTE, so the session and its first
    document exist exactly as a request would have made them."""
    registry = _registry(repo, tmp_path)
    status, created = gr.run_gate_action(
        "create-document",
        {"title": "First Draft", "summary": "The session's first document.",
         "topics": ["alpha"], "area": f"ideation/staging/{TOPIC}/",
         "repository_context": REPO, "scope_kind": bs.STAGED_TOPIC,
         "scope_id": TOPIC},
        checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=repo.repository)
    assert status == 200, created
    return registry, created, bs.worktree_path(repo.root, DRAFT)


def test_a_lock_contention_through_the_ROUTE_is_a_409_carrying_the_engines_reason(
        scratch_repo, tmp_path):
    """The mapping the wave-1 repair left unpinned by name: only the engine-level
    exception TYPE was covered, so nothing asserted that the route ANSWERS a lock
    race with the engine's own words rather than a 500 or a generic message.

    And finding 1's residual, closed: `rewrite_session_document` runs BEFORE
    `commit_gate_action` claims the lock, so this 409 is returned over a worktree
    whose document already carries the replacement. The bytes are deliberately left
    alone (they are the human's only copy), so the REFUSAL has to say so — it used
    to be silent, and the leftover then trips the merge ending's uncommitted-work
    refusal with the human never told why their worktree is dirty."""
    registry, created, worktree = _open_through_the_route(scratch_repo, tmp_path)
    relpath = created["path"]
    committed = (worktree / relpath).read_bytes()
    git = sg.SessionGit(scratch_repo.root)
    child = _lock_holder(scratch_repo, worktree, tmp_path)
    try:
        status, payload = gr.run_gate_action(
            "edit-document",
            {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
             "document": relpath, "content": "# First Draft\n\nrewritten.\n"},
            checkout_root=scratch_repo.root, actor="brett", snapshot_path=None,
            session_registry=registry, repository=scratch_repo.repository)
    finally:
        _release(child)

    assert status == 409, payload
    message = payload["message"]
    # the ENGINE's own reason, verbatim, naming the rival holder
    assert "already owns this session worktree's index" in message
    assert "a rival CLI verb" in message and str(child.pid) in message
    # and the truth about the worktree the 409 was returned over
    assert relpath in message and "ALREADY CARRIES YOUR REPLACEMENT" in message
    assert f"git -C {worktree} checkout -- {relpath}" in message, (
        "the recovery command must name the SESSION WORKTREE — the served root "
        "does not hold this document at all")
    assert "refuses to reconcile over uncommitted work" in message
    # measured, not merely claimed: dirty, uncommitted, unrecorded
    assert (worktree / relpath).read_bytes() != committed
    assert relpath in set(git.dirty_paths(worktree))
    assert git.staged_paths(worktree) == ()
    assert git.commits_ahead("main", DRAFT) == 1
    assert _records_in(worktree) == [
        worktree / created["record"]]

    # the recovery the message names actually recovers
    git.git(worktree, "checkout", "--", relpath)
    assert (worktree / relpath).read_bytes() == committed


def test_a_lock_contention_through_the_CLI_is_the_same_refusal(
        scratch_repo, tmp_path, capsys, monkeypatch):
    """CLI PARITY (FR-024) for the same mapping: the second writer is routinely a
    `cli.py gate edit-document` in its own process beside a serve request, so the
    CLI must exit 1 with the engine's reason and the same on-disk truth — not a
    traceback and not a different sentence."""
    from ideation_dashboard import cli as cli_mod

    registry, created, worktree = _open_through_the_route(scratch_repo, tmp_path)
    relpath = created["path"]
    content_file = tmp_path / "replacement.md"
    content_file.write_text("# First Draft\n\nrewritten by the CLI.\n",
                            encoding="utf-8")
    monkeypatch.setenv("XF_HUMAN_CONSOLE", "1")
    child = _lock_holder(scratch_repo, worktree, tmp_path)
    capsys.readouterr()
    try:
        rc = cli_mod.main(["gate", "edit-document", "--repo-root",
                           str(scratch_repo.root), "--actor", "dana",
                           "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                           "--document", relpath,
                           "--content-file", str(content_file)])
    finally:
        _release(child)
    err = capsys.readouterr().err

    assert rc == 1
    assert "already owns this session worktree's index" in err
    assert str(child.pid) in err
    assert "ALREADY CARRIES YOUR REPLACEMENT" in err
    assert relpath in err
    git = sg.SessionGit(scratch_repo.root)
    assert git.staged_paths(worktree) == ()
    assert git.commits_ahead("main", DRAFT) == 1


def test_a_second_repository_scratch_world_is_untouched_by_any_of_this(tmp_path):
    """The house rule, asserted rather than assumed: every test above builds its own
    throwaway checkout and bare origin, so nothing here can reach a real tree. This
    one builds a SECOND world beside them and pins that the operations under test
    are scoped to the checkout they were handed."""
    other = build_scratch_repo(tmp_path / "second", repository="MedxFactory")
    git = sg.SessionGit(other.root)
    assert git.served_root == other.root.resolve()
    assert git.branch_exists(DRAFT) is False
    assert bs.merge_state(git, DRAFT).merged is False


# ==========================================================================
# T068 / T069 / T070 (010-doxbench-editor-chat, US4) — the ELIGIBLE FIRST-EDIT
# transaction: `branch_session.commit_first_edit`.
#
# `commit_gate_action` above is a transaction over an ALREADY-OPEN session. The
# first Save from doxBench is a harder shape, because the open is part of it:
# an eligible first Save must "atomically create or join that tile's branch
# session, revalidate the source, and persist only in the resulting session"
# (FR-032), and a failure must leave "no document change, commit, governance
# record, live registry entry, or orphan working tree" (FR-033).
#
# Two consequences drive every test below.
#
#   * The action lock is per-WORKTREE and the worktree does not exist until the
#     open, so the open cannot itself be under the lock. It is instead inside
#     the transaction's FAILURE DOMAIN: everything from the open onward unwinds,
#     and `unwind_opened_session` is the compensator — which is exactly why it
#     refuses to unwind a session that already carries commits, and why a JOINED
#     session is never torn down by a Save that failed inside it.
#   * The rollback is therefore ASYMMETRIC, and the data model says so
#     (`FirstEditTransaction`: OPENED_NEW -> UNWIND, JOINED -> RESTORE_BYTES).
#     A Save that opened the session removes the whole session on failure; a
#     Save that joined one restores the bytes it replaced and leaves the session
#     and its earlier commits standing.
#
# T068 pins the happy transaction step by step, T069 injects a fault at EVERY
# step, T070 races two of them and audits the cleanup.
# ==========================================================================

SEEDED = "ideation/staging/demo-topic/README.md"   # exists in the served checkout
OWNED_PREFIX = "ideation/staging/demo-topic/"
SAVE_AT = "2026-07-28T09:00:00Z"
SAVE_AT_LATER = "2026-07-28T09:00:05Z"
SAVE_TILE = bs.Tile(bs.STAGED_TOPIC, TOPIC)


def _save_gate_factory(actor="brett", *, watching=None, git=None, before=None):
    """The seam the transaction builds its worktree-rooted gate through.

    `watching` records the action-lock holder observed at the moment of the
    WRITE, which is how a test proves the write happened inside the lock rather
    than beside it. `before` runs immediately before the write and is where a
    fault or a handshake is injected."""
    def build(worktree):
        gate = HumanGate(worktree, list(ALLOWLIST), human_actor=actor,
                         session_root=worktree)
        real_rewrite = gate.rewrite_session_document
        real_create = gate.output.create_document

        def instrument(real):
            def wrapped(path, text):
                if watching is not None and git is not None:
                    watching["write"] = git.read_action_lock(worktree)
                if before is not None:
                    before(worktree)
                return real(path, text)
            return wrapped

        gate.rewrite_session_document = instrument(real_rewrite)   # type: ignore
        gate.output.create_document = instrument(real_create)      # type: ignore
        return gate
    return build


def _first_edit(repo, registry, *, document, content, base_hash=None,
                at=SAVE_AT, git=None, owned_prefix=OWNED_PREFIX,
                gate_factory=None, **over):
    return bs.commit_first_edit(
        git or sg.SessionGit(repo.root), registry,
        repository=repo.repository, tile=SAVE_TILE,
        document=document, content=content,
        gate_factory=gate_factory or _save_gate_factory(),
        checkout_root=repo.root, owned_prefix=owned_prefix,
        base_hash=base_hash, at=at, records_dir=GATE_RECORDS_PREFIX, **over)


def _seeded_hash(repo, document=SEEDED):
    return dh.sha256_hex((repo.root / document).read_text(encoding="utf-8"))


def _assert_no_session_residue(git, registry, repo, *, branch=DRAFT,
                               served=None):
    """FR-033, in full: no commit, no record, no live registry entry, no orphan
    worktree, no derived snapshot, no owner marker — and the served checkout
    exactly as the Save found it."""
    worktree = bs.worktree_path(repo.root, branch)
    assert git.branch_exists(branch) is False, f"{branch!r} survived the unwind"
    assert not worktree.exists(), f"{worktree} survived the unwind"
    assert bs.is_live(registry, repo.repository, branch) is False
    assert not bs.session_snapshot_path(repo.root, branch).is_file()
    assert bs.read_owner_marker(repo.root, branch) is None
    assert _records_in(repo.root) == []
    if served is not None:
        assert repo.served_fingerprint() == served


# --------------------------------------------------------------------------
# T068 — the transaction, step by step
# --------------------------------------------------------------------------

def test_a_first_save_with_no_live_session_OPENS_one_and_commits_inside_it(
        scratch_repo, tmp_path):
    """FR-032's create arm. One call turns "no session" into "a session holding
    exactly this Save's commit", and the served checkout never moves."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    outcome = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nthe first save.\n", git=git)

    assert outcome.joined is False
    assert outcome.ref == DRAFT
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True
    assert git.commits_ahead("main", DRAFT) == 1
    assert git.head(outcome.session.worktree) == outcome.commit.sha
    assert scratch_repo.served_fingerprint() == served


def test_a_first_save_with_a_live_session_JOINS_it_and_allocates_no_second_branch(
        scratch_repo, tmp_path):
    """FR-032's join arm. The tile has ONE session; a Save arriving while it is
    live joins it rather than opening a second ordinal beside it."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    before = git.commits_ahead("main", DRAFT)

    outcome = _first_edit(scratch_repo, registry, document=SEEDED,
                          content="# Demo Topic\n\njoined and saved.\n",
                          base_hash=_seeded_hash(scratch_repo), git=git)

    assert outcome.joined is True
    assert outcome.ref == DRAFT
    assert outcome.session.worktree == opened.worktree
    assert git.commits_ahead("main", DRAFT) == before + 1
    assert bs.existing_branch_names(git, bs.session_branch(bs.STAGED_TOPIC,
                                                           TOPIC)) == (DRAFT,)


def test_the_revalidation_and_the_write_both_happen_inside_the_action_lock(
        scratch_repo, tmp_path, monkeypatch):
    """R10's requirement, measured: the whole revalidate -> write -> record ->
    commit sequence owns this worktree's index exclusively. Both the
    revalidation and the write observe the lock HELD, by this action, naming
    this process — so no rival can land between the check and the mutation."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    watching: dict = {}
    real = bs.first_edit_base_refusal

    def probe(**kwargs):
        watching["revalidate"] = git.read_action_lock(
            bs.worktree_path(scratch_repo.root, DRAFT))
        return real(**kwargs)

    monkeypatch.setattr(bs, "first_edit_base_refusal", probe)

    _first_edit(scratch_repo, registry, document=SEEDED,
                content="# Demo Topic\n\nsaved under the lock.\n",
                base_hash=_seeded_hash(scratch_repo), git=git,
                gate_factory=_save_gate_factory(watching=watching, git=git))

    assert watching["revalidate"] is not None, (
        "the base was revalidated OUTSIDE the lock — a rival write could land "
        "between the check and the replacement")
    assert watching["write"] is not None, "the write happened outside the lock"
    assert watching["write"]["pid"] == os.getpid()
    assert str(gc.ACTION_EDIT_DOCUMENT) in str(watching["write"]["action"])


def test_the_first_save_releases_the_action_lock_when_it_is_done(
        scratch_repo, tmp_path):
    """A held lock outlives nothing: the next Save must be able to claim it."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    outcome = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nsaved.\n", git=git)

    assert git.read_action_lock(outcome.session.worktree) is None


def test_the_first_save_commits_its_document_and_its_record_as_ONE_commit(
        scratch_repo, tmp_path):
    """FR-034's per-document clause, from the commit's side."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    outcome = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nsaved.\n", git=git)

    worktree = Path(outcome.session.worktree)
    assert _committed_files(worktree, outcome.commit.sha) == sorted(
        [DOC, outcome.commit.record_relpath])
    assert _tree_records(worktree, outcome.commit.sha) == [
        outcome.commit.record_relpath]
    assert git.staged_paths(worktree) == ()


def test_the_first_save_asserts_the_worktree_still_holds_the_branch(
        scratch_repo, tmp_path, monkeypatch):
    """The drift window `commit_gate_action` closed, closed again here: the
    branch identity is re-asserted INSIDE the lock, so a worktree somebody moved
    between the join and the commit is a refusal rather than a commit landing on
    whatever it now holds."""
    registry, git, opened = _live_session(scratch_repo, tmp_path, write=False)
    calls: list[str] = []
    real = bs.assert_git_holds_branch

    def refuse(g, worktree, branch, *, during):
        calls.append(during)
        raise bs.SessionWorktreeDrifted(Path(worktree), branch,
                                        kind=bs.WORKTREE_DETACHED,
                                        during=during)

    monkeypatch.setattr(bs, "assert_git_holds_branch", refuse)
    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=SEEDED,
                    content="# Demo Topic\n\nwould have drifted.\n",
                    base_hash=_seeded_hash(scratch_repo), git=git)

    monkeypatch.setattr(bs, "assert_git_holds_branch", real)
    assert calls, "the branch identity was never re-asserted inside the lock"
    assert git.staged_paths(opened.worktree) == ()
    assert _records_in(opened.worktree) == []


def test_the_first_saves_record_carries_the_existing_action_and_its_branch(
        scratch_repo, tmp_path):
    """FR-031: Save owns no verb of its own. The record names the EXISTING
    create/edit action, names the session branch, and carries the commit
    artifact keyed to its own stamp."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    created = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nnew.\n", at=SAVE_AT, git=git)
    edited = _first_edit(scratch_repo, registry, document=SEEDED,
                         content="# Demo Topic\n\nchanged.\n",
                         base_hash=_seeded_hash(scratch_repo),
                         at=SAVE_AT_LATER, git=git)

    assert created.record["action"] == gc.ACTION_CREATE_DOCUMENT
    assert edited.record["action"] == gc.ACTION_EDIT_DOCUMENT
    for outcome, at in ((created, SAVE_AT), (edited, SAVE_AT_LATER)):
        assert outcome.record["target"]["ref"] == DRAFT
        artifacts = [a for a in outcome.record["artifacts"]
                     if a.get("kind") == gc.ART_COMMIT]
        assert len(artifacts) == 1
        assert artifacts[0]["reference"] == bs.action_stamp(at)


# --------------------------------------------------------------------------
# T069 — a fault at EVERY step of the transaction
#
# One assertion oracle for all of them (`_assert_no_session_residue`), because
# FR-033's list is the same list whichever step failed. The steps are taken in
# the order the transaction performs them.
# --------------------------------------------------------------------------

def test_step_precheck_an_ineligible_target_opens_nothing_at_all(
        scratch_repo, tmp_path):
    """STEP 0 (PRECHECK). Inherited material is refused before the open, so
    there is nothing to unwind — the cheapest possible failure."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    inherited = "ideation/staging/other-topic/README.md"
    scratch_repo.write(inherited, "# Other Topic\n\nnot this tile's.\n")
    scratch_repo.commit("Add another topic", inherited)
    served = scratch_repo.served_fingerprint()

    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=inherited,
                    content="# Other Topic\n\nrewritten.\n",
                    base_hash=_seeded_hash(scratch_repo, inherited), git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_open_a_failed_worktree_add_leaves_no_branch_or_registry_entry(
        scratch_repo, tmp_path):
    """STEP 1 (OPEN). The open itself fails. Nothing downstream ran, and the
    partial open must not survive as a phantom live session."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    def refuse(branch, path, base):
        raise sg.GitError(("worktree", "add"), 128, "could not create worktree")

    git.worktree_add = refuse                                   # type: ignore
    with pytest.raises((sg.GitError, bs.SessionRefused)):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever landed.\n", git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_lock_a_rival_process_holding_it_refuses_and_unwinds_the_open(
        scratch_repo, tmp_path):
    """STEP 2 (LOCK). The lock is claimed AFTER the open, so a rival holder
    means a session was opened and must now be removed again. This is the arm
    where FR-033's "no orphan working tree" is easiest to get wrong."""
    registry, git, opened = _live_session(scratch_repo, tmp_path, write=False)
    # Tear the fixture's session down to the pre-Save state, then let the Save
    # open its own — the rival takes the lock on the path the Save will use.
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    child = _lock_holder(scratch_repo, worktree, tmp_path)
    try:
        with pytest.raises(bs.SessionRefused) as exc:
            _first_edit(scratch_repo, registry, document=DOC,
                        content="# Note\n\nlost the race.\n", git=git)
    finally:
        _release(child)

    message = str(exc.value)
    assert "already owns this session worktree's index" in message
    assert str(child.pid) in message
    assert git.commits_ahead("main", DRAFT) == 0
    assert _records_in(worktree) == []


def test_step_revalidate_a_stale_base_unwinds_the_session_it_opened(
        scratch_repo, tmp_path):
    """STEP 3 (REVALIDATE). The source moved under the human's buffer. Nothing
    is written, and the session this Save opened for the attempt is gone."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=SEEDED,
                    content="# Demo Topic\n\nagainst a base that is gone.\n",
                    base_hash=dh.sha256_hex("# not on disk\n"), git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_write_a_failed_rewrite_unwinds_the_session_it_opened(
        scratch_repo, tmp_path):
    """STEP 4 (WRITE)."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    def explode(worktree):
        raise OSError("the session volume is full")

    with pytest.raises(OSError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever written.\n", git=git,
                    gate_factory=_save_gate_factory(before=explode))

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_record_a_failed_record_write_unwinds_everything(
        scratch_repo, tmp_path, monkeypatch):
    """STEP 5 (RECORD)."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        lambda *a, **k: (_ for _ in ()).throw(
                            OSError("the records volume is full")))

    with pytest.raises(OSError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nno record.\n", git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_stage_a_failed_stage_unwinds_everything(scratch_repo, tmp_path):
    """STEP 6 (STAGE)."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    def refuse(root, paths):
        raise sg.GitError(("add",), 128, "unable to write index")

    git.stage = refuse                                          # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever staged.\n", git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_commit_a_failed_commit_unwinds_everything(scratch_repo, tmp_path):
    """STEP 7 (COMMIT)."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "unable to write new_index file")

    git.commit = refuse                                         # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever committed.\n", git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_verify_a_failed_post_commit_check_undoes_its_own_commit(
        scratch_repo, tmp_path):
    """STEP 8 (VERIFY). The commit was MADE and then found not to resolve. It is
    reset away, and the session it rode is unwound with it — the hardest arm,
    because a naive unwind would refuse to remove a session "carrying commits"."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = scratch_repo.served_fingerprint()

    git.introduced_by = lambda path, **kwargs: "0" * 40         # type: ignore
    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nunverifiable.\n", git=git)

    _assert_no_session_residue(git, registry, scratch_repo, served=served)


def test_step_refresh_a_failed_projection_NEVER_undoes_a_landed_commit(
        scratch_repo, tmp_path, monkeypatch):
    """STEP 9 (REFRESH). The one step whose failure is REPORTED rather than
    unwound: after the commit, the commit is already law. A projection failure
    that rolled it back would destroy governed history to fix a cache."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    monkeypatch.setattr(bs, "refresh_session_snapshot",
                        lambda *a, **k: (_ for _ in ()).throw(
                            OSError("the snapshot volume is full")))

    outcome = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nlanded anyway.\n", git=git)

    assert git.commits_ahead("main", DRAFT) == 1
    assert git.head(outcome.session.worktree) == outcome.commit.sha
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True


def test_a_refused_save_into_a_JOINED_session_restores_bytes_and_keeps_it(
        scratch_repo, tmp_path):
    """The asymmetric half of the rollback (`FirstEditTransaction`: JOINED ->
    RESTORE_BYTES). A Save that JOINED an existing session must not tear that
    session down when it fails: the earlier commits are other actions' governed
    history. It restores the bytes it replaced and leaves everything else."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    worktree = Path(opened.worktree)
    committed = (worktree / DOC).read_bytes()
    head = git.head(worktree)

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "unable to write new_index file")

    git.commit = refuse                                         # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\na replacement that fails.\n",
                    base_hash=dh.sha256_hex(committed.decode("utf-8")), git=git)

    assert git.branch_exists(DRAFT) is True, (
        "a Save that JOINED a session must never tear it down on failure")
    assert worktree.is_dir()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True
    assert git.head(worktree) == head
    assert git.commits_ahead("main", DRAFT) == 1
    assert (worktree / DOC).read_bytes() == committed, (
        "the bytes the failed Save replaced were not restored")
    assert git.staged_paths(worktree) == ()
    assert len(_records_in(worktree)) == 1, (
        "the failed Save's record must not survive beside the earlier action's")


# --------------------------------------------------------------------------
# T104 F3 (PR #63 second review, P1 branch_session.py:4405): the JOINED arm's
# CREATE residue
#
# `_unwind_first_edit`'s joined arm restores the bytes a Save REPLACED. Its
# comment justified doing nothing about a document the Save CREATED by saying
# `_commit_gate_action_locked` has already removed it — true only for a failure
# raised INSIDE that helper's own `try:`. Its first three refusals (the branch
# assertion, the already-committed check, and the not-empty-index check) are
# raised BEFORE that `try:`, so `_unwind_gate_action` never runs and the file
# this Save created stayed in the session worktree.
#
# The residue is not merely untidy: FR-033 says a failed first Save leaves no
# document change, and the leftover file then makes the buffer PERMANENTLY
# unsaveable — the create arm's base is the ABSENCE of the path
# (`first_edit_base_refusal`), so every retry is refused for a path only the
# failed attempt created.
# --------------------------------------------------------------------------

CREATED = "ideation/staging/demo-topic/created-by-this-save.md"


def _stage_foreign_work(git, worktree: Path) -> str:
    """Somebody else's work, STAGED in the shared session worktree — the exact
    precondition `_commit_gate_action_locked`'s not-empty-index refusal exists
    for, and it fires before that helper's own rollback try-block."""
    foreign = "ideation/staging/demo-topic/somebody-elses-staged-work.md"
    _write(worktree, foreign, "# Theirs\n\nstaged, uncommitted.\n")
    git.stage(worktree, [foreign])
    assert git.staged_paths(worktree) == (foreign,)
    return foreign


def test_a_failed_create_into_a_JOINED_session_leaves_no_residue_on_any_axis(
        scratch_repo, tmp_path):
    """FR-033 in full for the CREATE arm of a JOINED Save: file, index,
    worktree, registry and record all exactly as the Save found them."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    worktree = Path(opened.worktree)
    foreign = _stage_foreign_work(git, worktree)
    head = git.head(worktree)
    records_before = len(_records_in(worktree))
    dirty_before = set(git.dirty_paths(worktree))

    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=CREATED,
                    content="# New\n\na document this Save creates.\n")

    # FILE: the document this Save created is gone.
    assert not (worktree / CREATED).exists(), (
        "the document this failed Save created survived in the session worktree")
    # INDEX: exactly what was staged before, and nothing of this Save's.
    assert git.staged_paths(worktree) == (foreign,)
    # WORKTREE: no new path of any kind, and the served checkout untouched.
    assert set(git.dirty_paths(worktree)) == dirty_before
    assert not (scratch_repo.root / CREATED).exists()
    # REGISTRY: a JOINED session is never torn down by a Save that failed in it.
    assert git.branch_exists(DRAFT) is True
    assert worktree.is_dir()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True
    # RECORD: no gate-action record, and no commit carrying one.
    assert len(_records_in(worktree)) == records_before
    assert git.head(worktree) == head
    assert git.commits_ahead("main", DRAFT) == 1


def test_a_retry_after_a_failed_create_into_a_JOINED_session_still_lands(
        scratch_repo, tmp_path):
    """The consequence of the residue, stated as behaviour: with the fault
    cleared the SAME Save must land. A leftover file makes the create arm's own
    base revalidation refuse forever, because that arm's declared base is the
    ABSENCE of the path."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    worktree = Path(opened.worktree)
    foreign = _stage_foreign_work(git, worktree)

    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=CREATED,
                    content="# New\n\nattempt one.\n")

    git.unstage(worktree, [foreign])
    outcome = _first_edit(scratch_repo, registry, document=CREATED,
                          content="# New\n\nattempt two.\n", at=SAVE_AT_LATER)

    assert outcome.action == gc.ACTION_CREATE_DOCUMENT
    assert outcome.joined is True
    assert (worktree / CREATED).read_text(encoding="utf-8") == \
        "# New\n\nattempt two.\n"
    assert git.commits_ahead("main", DRAFT) == 2
    assert _committed_files(worktree, outcome.commit.sha) == sorted(
        [CREATED, outcome.commit.record_relpath])


def test_a_failed_rewrite_into_a_JOINED_session_still_keeps_the_tracked_file(
        scratch_repo, tmp_path):
    """The other half of the same arm, unchanged and pinned so the create-side
    removal cannot grow into deleting a TRACKED document: a failed REWRITE
    restores the replaced bytes and the file stays."""
    registry, git, opened = _live_session(scratch_repo, tmp_path)
    worktree = Path(opened.worktree)
    committed = (worktree / DOC).read_bytes()
    foreign = _stage_foreign_work(git, worktree)

    with pytest.raises(bs.SessionRefused):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\na replacement that fails.\n",
                    base_hash=dh.sha256_hex(committed.decode("utf-8")))

    assert (worktree / DOC).read_bytes() == committed
    assert git.staged_paths(worktree) == (foreign,)


def test_a_retry_after_an_unwound_first_save_is_exactly_one_commit(
        scratch_repo, tmp_path):
    """The unwind is COMPLETE enough to retry over: the human fixes the fault
    and saves again, and the branch carries one commit and one record — not the
    residue of the first attempt plus the second."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    attempts = {"n": 0}
    real_commit = git.commit

    def fail_once(root, message, **kwargs):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise sg.GitError(("commit",), 128, "transient failure")
        return real_commit(root, message, **kwargs)

    git.commit = fail_once                                      # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nattempt one.\n", at=SAVE_AT, git=git)
    _assert_no_session_residue(git, registry, scratch_repo)

    outcome = _first_edit(scratch_repo, registry, document=DOC,
                          content="# Note\n\nattempt two.\n",
                          at=SAVE_AT_LATER, git=git)

    worktree = Path(outcome.session.worktree)
    assert git.commits_ahead("main", DRAFT) == 1
    assert len(_records_in(worktree)) == 1
    assert _committed_files(worktree, outcome.commit.sha) == sorted(
        [DOC, outcome.commit.record_relpath])


# --------------------------------------------------------------------------
# T070 — two first Saves at once, and the cleanup audit
# --------------------------------------------------------------------------

def test_two_concurrent_first_saves_open_ONE_session_and_one_of_them_refuses(
        scratch_repo, tmp_path):
    """The race that matters: two first Saves for the SAME tile, arriving with
    no session live. Exactly one branch and one worktree may exist afterwards,
    the loser must fail LOUDLY rather than silently clobbering, and — the part
    a naive compensator gets wrong — the loser's unwind must not remove the
    session the WINNER is committing in."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    a_is_inside = threading.Event()
    b_is_done = threading.Event()

    def hold(worktree):
        a_is_inside.set()
        assert b_is_done.wait(timeout=30), "the second Save never finished"

    outcome: dict = {}

    def saver_a():
        try:
            outcome["a"] = _first_edit(
                scratch_repo, registry, document=DOC,
                content="# Note\n\nwriter A.\n", at=SAVE_AT, git=git,
                gate_factory=_save_gate_factory(before=hold))
        except BaseException as exc:                            # noqa: BLE001
            outcome["a"] = exc

    thread = threading.Thread(target=saver_a, daemon=True)
    thread.start()
    assert a_is_inside.wait(timeout=30), "the first Save never entered its write"

    # B is a SEPARATE SessionGit, exactly as a second request would be.
    b_git = sg.SessionGit(scratch_repo.root)
    with pytest.raises(bs.SessionRefused) as exc:
        _first_edit(scratch_repo, registry, document=SEEDED,
                    content="# Demo Topic\n\nwriter B.\n",
                    base_hash=_seeded_hash(scratch_repo), at=SAVE_AT_LATER,
                    git=b_git)
    b_report = str(exc.value)

    b_is_done.set()
    thread.join(timeout=30)
    assert not thread.is_alive()

    assert not isinstance(outcome["a"], BaseException), outcome["a"]
    assert "already owns this session worktree's index" in b_report
    # ONE session, and it is the winner's
    assert bs.existing_branch_names(git, bs.session_branch(bs.STAGED_TOPIC,
                                                           TOPIC)) == (DRAFT,)
    worktree = Path(outcome["a"].session.worktree)
    assert worktree.is_dir(), (
        "the loser's rollback removed the winner's worktree")
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True, (
        "the loser's rollback dropped the winner's registry entry")
    assert git.commits_ahead("main", DRAFT) == 1
    assert len(_records_in(worktree)) == 1
    # and B wrote nothing at all
    assert (worktree / SEEDED).read_text(encoding="utf-8") == \
        (scratch_repo.root / SEEDED).read_text(encoding="utf-8")


def test_a_concurrent_second_save_that_JOINS_still_gets_its_own_commit(
        scratch_repo, tmp_path):
    """Serialized rather than refused: once the winner's lock is released, the
    joining Save proceeds and produces its OWN commit and record. Two Saves,
    two governance actions, one session (FR-034)."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    first = _first_edit(scratch_repo, registry, document=DOC,
                        content="# Note\n\nfirst.\n", at=SAVE_AT, git=git)
    second = _first_edit(scratch_repo, registry, document=SEEDED,
                         content="# Demo Topic\n\nsecond.\n",
                         base_hash=_seeded_hash(scratch_repo),
                         at=SAVE_AT_LATER, git=git)

    worktree = Path(first.session.worktree)
    assert first.joined is False and second.joined is True
    assert git.commits_ahead("main", DRAFT) == 2
    assert len(_records_in(worktree)) == 2
    assert first.commit.sha != second.commit.sha
    assert _committed_files(worktree, second.commit.sha) == sorted(
        [SEEDED, second.commit.record_relpath])


def test_an_unwound_first_save_leaves_the_container_as_it_found_it(
        scratch_repo, tmp_path):
    """The registry/worktree cleanup audit, at the level of the CONTAINER: not
    merely "this branch's worktree is gone" but "the sessions directory holds
    nothing", so a half-removed directory cannot be mistaken for a live session
    by `bootstrap_sessions` in a later process."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    sessions = bs.sessions_root(scratch_repo.root)
    before = sorted(p.name for p in sessions.iterdir()) if sessions.is_dir() else []

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "unable to write new_index file")

    git.commit = refuse                                         # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever landed.\n", git=git)

    after = sorted(p.name for p in sessions.iterdir()) if sessions.is_dir() else []
    assert after == before
    assert git.worktree_paths() == (Path(scratch_repo.root),)
    bootstrap = bs.bootstrap_sessions(registry, repository=scratch_repo.repository,
                                      checkout_root=scratch_repo.root, git=git)
    assert bootstrap.live == ()
    assert bootstrap.stale == ()
    assert bootstrap.errors == ()


def test_an_unwound_first_save_leaves_no_ending_marker_blocking_the_retry(
        scratch_repo, tmp_path):
    """The unwind ends a session, and an ending is DURABLE by design — so the
    unwind has to leave the tile openable again, or the human's next Save is
    refused by the residue of their own failed one."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    def refuse(root, message, **kwargs):
        raise sg.GitError(("commit",), 128, "unable to write new_index file")

    git.commit = refuse                                         # type: ignore
    with pytest.raises(sg.GitError):
        _first_edit(scratch_repo, registry, document=DOC,
                    content="# Note\n\nnever landed.\n", git=git)

    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is None
    reopened = bs.open_session(git, registry,
                               repository=scratch_repo.repository,
                               tile=SAVE_TILE, checkout_root=scratch_repo.root)
    assert reopened.joined is False
    assert reopened.branch == DRAFT


def test_a_first_save_never_pushes_and_never_touches_the_origin(
        scratch_repo, tmp_path):
    """FR-037's remaining clause at this layer: the Save persists on a local
    branch. Dispatch stays `open-pr`, and nothing here reaches the remote."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    origin_before = scratch_repo.origin_branches()

    _first_edit(scratch_repo, registry, document=DOC,
                content="# Note\n\nlocal only.\n", git=git)

    assert scratch_repo.origin_branches() == origin_before
    assert git.tracking_sha(DRAFT) is None
