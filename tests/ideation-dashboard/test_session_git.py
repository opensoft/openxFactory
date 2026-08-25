"""`session_git.py` against a REAL scratch repository (T007).

The one git-write surface in the dashboard, asserted on git's OWN behaviour
rather than on a fake: ref legality, worktree bookkeeping, commit counts, and
`ls-remote` against a bare `origin` are exactly what a fake runner would not
tell us (contracts/session-ports.md, research R10).

Two assertions here carry more weight than the rest:

  * the MANDATORY remote-only-branch fixture — a branch that exists ONLY in the
    bare `origin`, created inside it with `git update-ref` and never fetched.
    `remote_ordinals` must SEE it and `local_ordinals` must not. It is the only
    fixture that can tell a real `ls-remote` implementation apart from one that
    reads local refs (FR-026, D17);
  * the served-checkout immovability guard — `checkout` / `switch` / `reset` /
    `stash` against the served root RAISE, and the served fingerprint is
    unchanged around every operation (FR-004, SC-002).
"""

from __future__ import annotations

import subprocess

import pytest

from session_fixtures import GATE_RECORDS_PREFIX, build_scratch_repo

from ideation_dashboard import session_git as sg


class RecordingRunner:
    """Wraps the real runner and records every argv, so "never `git fetch`" is
    an assertion about the commands actually issued (FR-026) rather than a
    reading of the source."""

    def __init__(self) -> None:
        self.real = sg.SubprocessGitRunner()
        self.calls: list[tuple[str, ...]] = []

    def run(self, cwd, *args):
        self.calls.append(tuple(args))
        return self.real.run(cwd, *args)

    def subcommands(self) -> list[str]:
        return [next((a for a in call if not a.startswith("-")), "")
                for call in self.calls]


@pytest.fixture
def git_and_repo(scratch_repo):
    runner = RecordingRunner()
    return sg.SessionGit(scratch_repo.root, runner=runner), scratch_repo, runner


def _session_dir(repo, branch: str):
    return repo.container / "sessions" / branch.replace("/", "__")


# --------------------------------------------------------------------------
# worktree round-trips, with the served checkout never moving
# --------------------------------------------------------------------------

def test_worktree_add_creates_the_branch_and_the_directory(git_and_repo):
    git, repo, _ = git_and_repo
    before = repo.served_fingerprint()

    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")

    assert path.is_dir()
    assert (path / "ideation/staging/demo-topic/README.md").is_file()
    assert git.branch_exists("draft/demo-topic")
    assert path.resolve() in {p.resolve() for p in git.worktree_paths()}
    assert git.current_branch(path) == "draft/demo-topic"
    # SC-002: the served checkout did not move.
    assert repo.served_fingerprint() == before


def test_worktree_remove_then_add_existing_is_the_resume_path(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    repo.write("notes.md", "session work\n", cwd=path)
    git.stage(path, ["notes.md"])
    sha = git.commit(path, "One gate action\n\nGate-Action: 20260726T000000Z")

    before = repo.served_fingerprint()
    git.worktree_remove(path)
    assert not path.exists()
    # the BRANCH survives the worktree removal — an abandoned branch (FR-022)
    assert git.branch_exists("draft/demo-topic")

    git.worktree_add_existing("draft/demo-topic", path)
    assert path.is_dir()
    assert (path / "notes.md").read_text(encoding="utf-8") == "session work\n"
    assert git.head(path) == sha
    assert repo.served_fingerprint() == before


def test_worktree_add_refuses_an_illegal_branch_name_before_touching_git(git_and_repo):
    git, repo, runner = git_and_repo
    path = _session_dir(repo, "bad")
    before = len(runner.calls)
    with pytest.raises(sg.SessionGitRefused):
        git.worktree_add("draft/openxFactory:staging:demo", path, "main")
    assert not path.exists()
    # the refusal happened on the derived NAME; git ran only the check-ref-format
    # read, never a worktree write (data-model validation rules)
    assert runner.subcommands()[before:] == ["check-ref-format"]


# --------------------------------------------------------------------------
# staging and committing: explicit paths, one commit, no amend
# --------------------------------------------------------------------------

def test_stage_takes_explicit_paths_and_commit_returns_the_sha(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    fork = git.head(path)

    repo.write("ideation/staging/demo-topic/note.md", "# Note\n", cwd=path)
    repo.write(f"{GATE_RECORDS_PREFIX}demo-topic/create-document-1.gate-action.yaml",
               "kind: gate-action-record\n", cwd=path)
    staged = git.stage(path, ["ideation/staging/demo-topic/note.md",
                              f"{GATE_RECORDS_PREFIX}demo-topic/"
                              "create-document-1.gate-action.yaml"])
    assert len(staged) == 2
    sha = git.commit(path, "create-document\n\nGate-Action: 20260726T000000Z")

    assert sha == git.head(path)
    assert git.commits_ahead("main", "draft/demo-topic") == 1
    # both files ride the SAME commit (FR-006)
    listed = subprocess.run(["git", "show", "--name-only", "--format=", sha],
                            cwd=str(path), text=True, capture_output=True,
                            check=True).stdout.split()
    assert "ideation/staging/demo-topic/note.md" in listed
    assert any(l.endswith("create-document-1.gate-action.yaml") for l in listed)


@pytest.mark.parametrize("bad", [["-A"], ["--all"], ["."], ["-u"], ["*"], [":/"],
                                 ["--"], ["../escape.md"]])
def test_stage_refuses_every_stage_everything_spelling(git_and_repo, bad):
    git, repo, runner = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    before = len(runner.calls)
    with pytest.raises(sg.SessionGitRefused):
        git.stage(path, bad)
    # refused BEFORE git ran — the shared-tree house rule is structural
    assert runner.calls[before:] == []


def test_stage_refuses_an_empty_path_list(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    with pytest.raises(sg.SessionGitRefused):
        git.stage(path, [])


def test_there_is_no_amend_operation_anywhere_on_the_surface():
    # FR-006: one commit per gate action, and a commit cannot contain its own
    # sha, so the amend-then-restamp dance must not be reachable at all.
    for name in ("amend", "commit_amend", "reword", "squash"):
        assert not hasattr(sg.SessionGit, name)
    source = (sg.__file__ and open(sg.__file__, encoding="utf-8").read()) or ""
    assert "--amend" not in source


def test_commit_refuses_when_nothing_is_staged(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    with pytest.raises(sg.GitError):
        git.commit(path, "empty\n\nGate-Action: x")


# --------------------------------------------------------------------------
# introduced_by — the record's `commit` artifact resolution (FR-006)
# --------------------------------------------------------------------------

def test_introduced_by_resolves_the_commit_that_added_the_record(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")

    record = f"{GATE_RECORDS_PREFIX}demo-topic/create-document-1.gate-action.yaml"
    repo.write(record, "kind: gate-action-record\n", cwd=path)
    git.stage(path, [record])
    first = git.commit(path, "create-document\n\nGate-Action: one")

    # a LATER commit touching the same file must not become the answer
    repo.write(record, "kind: gate-action-record\nnotes: touched\n", cwd=path)
    git.stage(path, [record])
    second = git.commit(path, "edit-document\n\nGate-Action: two")

    assert first != second
    assert git.introduced_by(record, cwd=path) == first
    assert git.introduced_by("nothing/here.yaml", cwd=path) is None


# --------------------------------------------------------------------------
# the ordinal inputs: ls-remote (never fetch) UNION local refs (FR-026, D17)
# --------------------------------------------------------------------------

def test_remote_ordinals_sees_a_branch_that_exists_only_in_the_bare_origin(git_and_repo):
    git, repo, runner = git_and_repo
    # MANDATORY fixture: created inside the bare origin, never fetched.
    repo.add_remote_only_branch("draft/demo-topic-2")

    remote = git.remote_ordinals("draft/demo-topic")
    local = git.local_ordinals("draft/demo-topic")

    assert "draft/demo-topic-2" in remote
    assert "draft/demo-topic-2" not in local, (
        "local_ordinals must read LOCAL refs — a remote-only branch is not one")
    assert "fetch" not in runner.subcommands(), (
        "remote_ordinals must be side-effect-free: ls-remote, never fetch")
    assert "ls-remote" in runner.subcommands()


def test_local_ordinals_sees_a_never_pushed_branch_the_remote_cannot(git_and_repo):
    git, repo, _ = git_and_repo
    # Nothing pushes before `open-pr`, so this is the ORDINARY case (FR-026).
    git.worktree_add("draft/demo-topic", _session_dir(repo, "draft/demo-topic"), "main")

    assert "draft/demo-topic" in git.local_ordinals("draft/demo-topic")
    assert "draft/demo-topic" not in git.remote_ordinals("draft/demo-topic")


def test_ordinal_scans_do_not_leak_a_sibling_prefix(git_and_repo):
    git, repo, _ = git_and_repo
    git.worktree_add("draft/demo-topic-and-more",
                     _session_dir(repo, "draft/demo-topic-and-more"), "main")
    repo.add_remote_only_branch("draft/demo-topical")

    names = set(git.local_ordinals("draft/demo-topic")) | set(
        git.remote_ordinals("draft/demo-topic"))
    # the raw scan is prefix-shaped by design; the FAMILY filter (base or
    # base-<int>) belongs to branch_session, and these two prove the raw scan
    # hands over the near-misses rather than swallowing them silently
    assert "draft/demo-topic-and-more" in names
    assert "draft/demo-topical" in names


def test_ordinal_scans_degrade_when_no_remote_is_configured(tmp_path):
    repo = build_scratch_repo(tmp_path)
    repo.git("remote", "remove", "origin")
    git = sg.SessionGit(repo.root)
    assert git.has_remote() is False
    assert git.remote_ordinals("draft/") == ()
    assert git.local_ordinals("draft/") == ()


# --------------------------------------------------------------------------
# delete_branch — merge ending (FR-033) and the human cleanup (FR-028)
# --------------------------------------------------------------------------

def test_delete_branch_removes_the_local_ref_and_optionally_the_remote(git_and_repo):
    git, repo, _ = git_and_repo
    path = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", path, "main")
    repo.write("notes.md", "x\n", cwd=path)
    git.stage(path, ["notes.md"])
    git.commit(path, "one\n\nGate-Action: one")
    repo.git("push", "origin", "draft/demo-topic")
    git.worktree_remove(path)

    assert "draft/demo-topic" in repo.origin_branches()
    git.delete_branch("draft/demo-topic", remote=True)
    assert not git.branch_exists("draft/demo-topic")
    assert "draft/demo-topic" not in repo.origin_branches()


def test_delete_branch_refuses_main_and_the_current_served_branch(git_and_repo):
    git, _, _ = git_and_repo
    with pytest.raises(sg.SessionGitRefused):
        git.delete_branch("main")


def test_expected_sha_delete_atomically_preserves_a_concurrently_moved_ref(
        scratch_repo):
    path = _session_dir(scratch_repo, "draft/demo-topic")
    setup = sg.SessionGit(scratch_repo.root)
    setup.worktree_add("draft/demo-topic", path, "main")
    scratch_repo.write("notes.md", "session work\n", cwd=path)
    setup.stage(path, ["notes.md"])
    expected = setup.commit(path, "session work\n\nGate-Action: one")
    setup.worktree_remove(path)
    moved_to = scratch_repo.head("main")

    class AdvancingRunner(RecordingRunner):
        def run(self, cwd, *args):
            if args[:3] == (
                    "update-ref", "-d", "refs/heads/draft/demo-topic"):
                self.real.run(
                    cwd, "update-ref", "refs/heads/draft/demo-topic",
                    moved_to, expected)
            return super().run(cwd, *args)

    git = sg.SessionGit(scratch_repo.root, runner=AdvancingRunner())
    with pytest.raises(sg.SessionGitRefused, match="atomic expected-value"):
        git.delete_branch("draft/demo-topic", expect_sha=expected)

    assert git.branch_sha("draft/demo-topic") == moved_to


# --------------------------------------------------------------------------
# the served-checkout immovability guard (FR-004; chg 2.3)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("forbidden", [
    ("checkout", "-b", "sneaky"),
    ("switch", "-c", "sneaky"),
    ("reset", "--hard", "HEAD~1"),
    ("stash", "push"),
    ("restore", "."),
    ("-c", "core.pager=cat", "checkout", "main"),
])
def test_the_guard_refuses_moving_the_served_checkout(git_and_repo, forbidden):
    git, repo, runner = git_and_repo
    before = repo.served_fingerprint()
    n = len(runner.calls)
    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(git.served_root, *forbidden)
    assert runner.calls[n:] == [], "the guard fires BEFORE git is invoked"
    assert repo.served_fingerprint() == before


def test_no_exported_operation_can_move_the_served_checkout(git_and_repo):
    """The structural half of FR-004: the guard is on the ONE funnel every
    operation goes through, so no exported operation can route around it.

    PR #49 review finding 18 measured that this test's docstring was a claim the
    test did not make — it checked the pure function at cwd==served and
    cwd==worktree and NOTHING ELSE, so a served SUBDIRECTORY and `-C`/`--git-dir`
    walked straight through. All three cwd/argv shapes are pinned here now, and the
    live reproductions live in the finding-18 section below."""
    git, repo, _ = git_and_repo
    subdirectory = git.served_root / "ideation"
    worktree = repo.container / "sessions/draft__x"
    for sub in sg.FORBIDDEN_SERVED_SUBCOMMANDS:
        assert sg.guard_served_command(git.served_root, git.served_root, (sub,)) is False
        # a served SUBDIRECTORY is the served checkout's working tree too
        assert sg.guard_served_command(git.served_root, subdirectory, (sub,)) is False
        # and a routing option makes the cwd irrelevant, from ANY cwd
        assert sg.guard_served_command(
            git.served_root, worktree, ("-C", str(git.served_root), sub)) is False
        assert sg.guard_served_command(
            git.served_root, worktree,
            ("--git-dir", f"{git.served_root}/.git", "--work-tree",
             str(git.served_root), sub)) is False
        # the same subcommand inside a session worktree is not this guard's
        # business — the guard is about the SERVED root, which is what must
        # never move (a worktree is disposable)
        assert sg.guard_served_command(git.served_root, worktree, (sub,)) is True


def test_the_guard_allows_the_reads_and_writes_the_contract_names(git_and_repo):
    git, repo, _ = git_and_repo
    for allowed in (("rev-parse", "HEAD"), ("status", "--porcelain"),
                    ("worktree", "list"), ("branch", "--list"),
                    ("ls-remote", "--heads"), ("log", "-1"),
                    ("check-ref-format", "refs/heads/x")):
        assert sg.guard_served_command(git.served_root, git.served_root, allowed) is True


# --------------------------------------------------------------------------
# served_checkout_fingerprint (FR-004, SC-002)
# --------------------------------------------------------------------------

def test_served_fingerprint_matches_the_independent_harness_reading(git_and_repo):
    git, repo, _ = git_and_repo
    mine = git.served_checkout_fingerprint()
    theirs = repo.served_fingerprint()
    assert (mine.branch, mine.head, mine.porcelain) == (
        theirs.branch, theirs.head, theirs.porcelain)


# ==========================================================================
# PR #49 review finding 18 — the immovability guard is STRUCTURAL, and the
# fingerprint's blind spot is inverted
#
# The review reproduced three bypasses of the old cwd-equality denylist, each of
# which actually MOVED the served checkout, plus a fingerprint (and a "independent"
# test oracle that duplicated its logic) which could not see content renamed OUT of
# the governed tree INTO the declared records prefix. The tests below are the
# reproductions, inverted:
#
#   * a served SUBDIRECTORY, `git -C <served>`, and `git --git-dir/--work-tree`
#     are refused, and the served branch is asserted UNCHANGED after each;
#   * the served root permits an ALLOWLIST, so `merge`, `clean`, `add`, `commit`
#     and every other unenumerated subcommand are refused because they are ABSENT
#     rather than because someone remembered them;
#   * `stage()` and `commit()` cannot advance the served HEAD;
#   * the fingerprint DETECTS a staged `git mv` out of `ideation/staging/`, which
#     is the assertion `test_served_fingerprint_matches_the_independent_harness_
#     reading` above could never make: agreement between two copies of the same
#     filter proves only that they are the same copy.
# ==========================================================================

@pytest.mark.parametrize("routing", [
    ("-C", "{served}", "checkout", "other-branch"),
    ("--git-dir", "{served}/.git", "--work-tree", "{served}", "checkout",
     "other-branch"),
    ("--git-dir={served}/.git", "checkout", "other-branch"),
    ("-C", "{served}", "switch", "other-branch"),
    ("--exec-path", "/tmp", "status"),
])
def test_git_routing_options_are_refused_from_any_cwd(git_and_repo, routing):
    """A routing option retargets the command at a repository the guard never
    inspected, so `cwd` stopped being the truth about what would be touched. Driven
    from a SESSION WORKTREE — the cwd the old guard treated as none of its business
    — because that is exactly where the review's reproduction ran."""
    git, repo, runner = git_and_repo
    repo.git("branch", "other-branch", "main")
    worktree = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", worktree, "main")
    before = repo.served_fingerprint()
    args = tuple(a.format(served=repo.root) for a in routing)
    n = len(runner.calls)

    with pytest.raises(sg.ServedCheckoutImmovable) as exc:
        git.git(worktree, *args)

    assert runner.calls[n:] == [], "the guard fires BEFORE git is invoked"
    assert "ROUTING" in str(exc.value)
    assert repo.served_fingerprint() == before
    assert repo.branch() == before.branch


def test_a_served_subdirectory_cannot_move_the_served_checkout(git_and_repo):
    """`<served>/ideation` IS the served checkout's working tree, and a `git
    checkout` run there moves it identically — measured. The guard now resolves the
    target by CONTAINMENT rather than by string-equality with the served root."""
    git, repo, _ = git_and_repo
    repo.git("branch", "other-branch", "main")
    before = repo.served_fingerprint()

    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(repo.root / "ideation", "checkout", "other-branch")

    assert repo.served_fingerprint() == before
    assert repo.branch() == "main"


@pytest.mark.parametrize("argv", [
    ("merge", "other-branch"),
    ("clean", "-fdx"),
    ("add", "--", "ideation"),
    ("commit", "-m", "not from here"),
    ("rm", "-r", "ideation"),
    ("mv", "ideation", "elsewhere"),
    ("update-ref", "refs/heads/main", "other-branch"),
    ("symbolic-ref", "HEAD", "refs/heads/other-branch"),
    ("apply", "/dev/null"),
    ("cherry-pick", "other-branch"),
    ("rebase", "other-branch"),
    ("sparse-checkout", "init"),
])
def test_the_served_root_permits_only_the_allowlisted_subcommands(git_and_repo,
                                                                 argv):
    """An ALLOWLIST is the property a denylist could never have: the guard used to
    name five subcommands, so `merge` and `clean -fdx` at the served root were
    permitted (measured). Nothing that touches the served working tree, index, or
    HEAD is on the list, so a subcommand nobody thought of is refused."""
    git, repo, runner = git_and_repo
    repo.git("branch", "other-branch", "main")
    before = repo.served_fingerprint()
    n = len(runner.calls)

    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(repo.root, *argv)

    assert runner.calls[n:] == []
    assert repo.served_fingerprint() == before


def test_the_allowlist_still_admits_every_operation_the_contract_names(git_and_repo):
    """The other half of an allowlist: it must not break the lifecycle. Every
    subcommand `session_git` actually runs against the served root is present."""
    for allowed in ("check-ref-format", "worktree", "show-ref", "branch", "push",
                    "rev-parse", "status", "ls-remote", "log", "merge-base",
                    "rev-list", "remote", "cat-file", "ls-files"):
        assert allowed in sg.SERVED_ALLOWED_SUBCOMMANDS, allowed
    for refused in sg.FORBIDDEN_SERVED_SUBCOMMANDS:
        assert refused not in sg.SERVED_ALLOWED_SUBCOMMANDS
    for refused in ("add", "commit", "merge", "clean", "update-ref", "rm", "mv"):
        assert refused not in sg.SERVED_ALLOWED_SUBCOMMANDS


def test_stage_and_commit_cannot_advance_the_served_head(git_and_repo):
    """The review drove `stage()` + `commit()` at the served root and watched its
    HEAD move from one sha to another — so SC-002's "HEAD unchanged" had no
    structural backstop at all. Both are refused now, by absence."""
    git, repo, _ = git_and_repo
    repo.write("ideation/staging/demo-topic/sneaky.md", "not through here\n")
    before = repo.served_fingerprint()

    with pytest.raises(sg.ServedCheckoutImmovable):
        git.stage(repo.root, ["ideation/staging/demo-topic/sneaky.md"])
    with pytest.raises(sg.ServedCheckoutImmovable):
        git.commit(repo.root, "sneaky\n\nGate-Action: none")

    after = repo.served_fingerprint()
    assert after.head == before.head
    assert after.branch == before.branch


@pytest.mark.parametrize("cwd_kind", ["served", "worktree"])
def test_fetch_is_refused_at_every_cwd(git_and_repo, cwd_kind):
    """FR-026/D17: the remote is read with `ls-remote`, which is side-effect-free,
    and NEVER fetched — a fetch touches the local refs ordinal allocation reads."""
    git, repo, runner = git_and_repo
    worktree = _session_dir(repo, "draft/demo-topic")
    git.worktree_add("draft/demo-topic", worktree, "main")
    cwd = repo.root if cwd_kind == "served" else worktree
    n = len(runner.calls)

    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(cwd, "fetch", "origin")

    assert runner.calls[n:] == []
    assert "fetch" not in runner.subcommands()


def test_a_rename_out_of_the_governed_tree_into_the_records_prefix_is_detected(
        git_and_repo):
    """The fingerprint's blind spot, inverted. `git mv ideation/staging/<topic>/
    notes.md ideation/dashboard/gate-records/notes.md` produces ONE porcelain line
    whose DESTINATION is declared — so a filter that kept only the destination
    dropped the line and reported the served checkout UNCHANGED while a governed
    staging file had left the tree (reproduced, in production AND in the harness
    oracle, which duplicated the same filter).

    This is the oracle the previous "the two agree" test could not be: it asserts a
    KNOWN move is DETECTED."""
    git, repo, _ = git_and_repo
    source = f"ideation/staging/{repo.topic_id}/notes.md"
    repo.write(source, "governed content\n")
    repo.commit("Add a governed staging file", source)
    base = git.served_checkout_fingerprint()
    assert base.porcelain == ()

    destination = f"{GATE_RECORDS_PREFIX}notes.md"
    repo.git("mv", source, destination)
    line = repo.git("status", "--porcelain", "--untracked-files=all")
    assert " -> " in line and line.strip().endswith(destination)

    after = git.served_checkout_fingerprint()
    assert after != base, (
        "content that LEFT the governed tree must change the fingerprint even when "
        "it landed inside the declared records prefix (SC-002)")
    assert any(source in l for l in after.porcelain)
    # the harness oracle is genuinely independent AND sees it too
    assert repo.served_fingerprint().porcelain == after.porcelain
    assert not (repo.root / source).exists()


def test_a_line_wholly_inside_the_records_prefix_is_still_excluded(git_and_repo):
    """The other direction, so the fix is a narrowing and not a blunt removal: a
    rename WITHIN the declared prefix names only declared paths and stays filtered
    out, because that prefix is where the main-resident records legitimately land."""
    git, repo, _ = git_and_repo
    first = f"{GATE_RECORDS_PREFIX}demo-topic/open-pr-1.gate-action.yaml"
    repo.write(first, "action: open-pr\n")
    repo.commit("A main-resident record", first)
    base = git.served_checkout_fingerprint()

    repo.git("mv", first, f"{GATE_RECORDS_PREFIX}demo-topic/open-pr-2.gate-action.yaml")

    assert git.served_checkout_fingerprint() == base
    assert sg.declared_only(
        f"R  {first} -> {GATE_RECORDS_PREFIX}demo-topic/open-pr-2.gate-action.yaml",
        GATE_RECORDS_PREFIX) is True


def test_served_fingerprint_excludes_only_the_declared_records_prefix(git_and_repo):
    git, repo, _ = git_and_repo
    base = git.served_checkout_fingerprint()

    repo.write(f"{GATE_RECORDS_PREFIX}demo-topic/abandon-session-1.gate-action.yaml",
               "reason: changed my mind\n")
    assert git.served_checkout_fingerprint() == base

    repo.write("ideation/staging/demo-topic/leak.md", "leak\n")
    moved = git.served_checkout_fingerprint()
    assert moved != base
    assert moved.branch == base.branch and moved.head == base.head


# --------------------------------------------------------------------------
# check_ref_format — every derived name is validated before any git call
# --------------------------------------------------------------------------

@pytest.mark.parametrize("ref,ok", [
    ("draft/demo-topic", True),
    ("draft/demo-topic-2", True),
    ("cluster/cl-accessibility", True),
    ("possible/pos-derived-thing", True),
    ("draft/openxFactory:staging:demo", False),   # research R2's real staging id
    ("draft/demo topic", False),
    ("draft/demo..topic", False),
    ("draft/demo~1", False),
    ("draft/", False),
    ("", False),
])
def test_check_ref_format_is_gits_own_answer(git_and_repo, ref, ok):
    git, _, _ = git_and_repo
    assert git.check_ref_format(ref) is ok
