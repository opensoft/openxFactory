"""Branch-session harness + container-placement regressions (T001, T002, T004).

Three obligations, all of them safety nets that must fail LOUDLY the day a
finding stops being true:

  * the scratch world is real git (a bare `origin` on disk, a `main` checkout,
    a staged-topic fragment) and the served fingerprint filters EXACTLY the
    declared gate-records prefix and nothing else (T001, SC-002);
  * the fakes cannot reach a network or a real notebook, and the
    `PullRequestPort` fake has NO merge/approve/review/bypass operation at all
    (T002, FR-030, FR-043);
  * the worktree container `<repo>-worktrees/` is gitignored AND excluded from
    the NotebookLM book scan (T004, FR-005) — research R7's "no new ignore entry
    is needed" finding, encoded so it cannot silently stop being true.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT
from session_fixtures import (
    FakeNotebookAdapter,
    FakePullRequests,
    GATE_RECORDS_PREFIX,
    QuotaExhausted,
    _porcelain_path,
    build_scratch_repo,
    filter_declared_paths,
)

# The sync script is a hyphenated path, so it loads by spec like it does in
# tests/notebooklm — under its OWN module name here, so neither suite clobbers
# the other's copy in sys.modules.
_SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
_spec = importlib.util.spec_from_file_location("sync_books_session_scan", _SYNC_SCRIPT)
sync = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = sync
_spec.loader.exec_module(sync)


# --------------------------------------------------------------------------
# T001 — the scratch world and the immovability fingerprint
# --------------------------------------------------------------------------

def test_scratch_repo_is_real_git_with_a_bare_origin_and_a_staged_topic(scratch_repo):
    assert scratch_repo.branch() == "main"
    assert scratch_repo.origin.is_dir()
    assert scratch_repo.git("rev-parse", "--is-bare-repository",
                            cwd=scratch_repo.origin) == "true"
    # origin carries `main` at the same sha — pushed, not simulated.
    assert scratch_repo.origin_branches() == ("main",)
    assert scratch_repo.head() == scratch_repo.git("rev-parse", "main",
                                                   cwd=scratch_repo.origin)
    fragment = (scratch_repo.root / "ideation/staging"
                / scratch_repo.topic_id / "README.md")
    assert fragment.is_file()
    assert "Kind: staging-packet" in fragment.read_text(encoding="utf-8")
    # the container sits BESIDE the checkout, named <repo>-worktrees (FR-005)
    assert scratch_repo.container.name == f"{scratch_repo.repository}-worktrees"
    assert scratch_repo.container.parent == scratch_repo.root.parent


def test_served_fingerprint_filters_only_the_declared_gate_records_prefix(scratch_repo):
    before = scratch_repo.served_fingerprint()
    assert before.porcelain == ()

    # A main-resident gate record is a LEGITIMATE change to the served working
    # tree (plan Constraint 10): the fingerprint must not see it.
    scratch_repo.write(f"{GATE_RECORDS_PREFIX}demo/open-pr-1.gate-action.yaml", "x\n")
    after_record = scratch_repo.served_fingerprint()
    assert after_record.branch == before.branch
    assert after_record.head == before.head
    assert after_record.porcelain == ()

    # Anything ELSE in the working tree must show up, or the filter is a blindfold.
    scratch_repo.write("ideation/brainstorm/leak.md", "leaked\n")
    leaked = scratch_repo.served_fingerprint()
    assert any("ideation/brainstorm/leak.md" in line for line in leaked.porcelain)


def test_the_fingerprint_keeps_the_leading_space_of_a_modified_line(scratch_repo):
    """`git status --porcelain` emits ` M path` for a worktree-only
    modification, so stripping the output shifts every path by one character and
    the prefix filter then reads the WRONG path — which would silently stop the
    gate-records exclusion (and the leak detection) from working."""
    record = f"{GATE_RECORDS_PREFIX}.gitkeep"           # tracked, so it MODIFIES
    (scratch_repo.root / record).write_text("touched\n", encoding="utf-8")
    assert scratch_repo.served_fingerprint().porcelain == ()

    tracked = "ideation/staging/demo-topic/README.md"
    doc = scratch_repo.root / tracked
    doc.write_text(doc.read_text(encoding="utf-8") + "\nmore\n", encoding="utf-8")
    lines = scratch_repo.served_fingerprint().porcelain
    assert [_porcelain_path(l) for l in lines] == [tracked]


def test_fingerprint_filter_handles_rename_lines_by_their_new_path():
    lines = [
        "R  ideation/dashboard/gate-records/a -> ideation/dashboard/gate-records/b",
        "R  ideation/dashboard/gate-records/a -> ideation/brainstorm/b.md",
        "?? ideation/brainstorm/c.md",
    ]
    kept = filter_declared_paths(lines)
    assert kept == (lines[1], lines[2])


def test_scratch_repo_can_carry_a_remote_only_branch_without_fetching(scratch_repo):
    scratch_repo.add_remote_only_branch("draft/demo-topic-2")
    assert "draft/demo-topic-2" in scratch_repo.origin_branches()
    assert "draft/demo-topic-2" not in scratch_repo.local_branches()


def test_two_scratch_worlds_never_share_state(tmp_path):
    one = build_scratch_repo(tmp_path / "a")
    two = build_scratch_repo(tmp_path / "b", topic_id="other-topic")
    assert one.root != two.root
    assert one.head() != two.head() or one.topic_id != two.topic_id
    assert (two.root / "ideation/staging/other-topic/README.md").is_file()


def _global_hooks_world(tmp_path, *names: str) -> Path:
    """A GLOBAL git config pointing `core.hooksPath` at a directory of hooks that
    all FAIL — the shape husky / lefthook / `pre-commit` install."""
    hooks = tmp_path / "engineers-hooks"
    hooks.mkdir()
    for name in names:
        hook = hooks / name
        hook.write_text("#!/bin/sh\necho 'the engineer's own hook ran' >&2\nexit 1\n",
                        encoding="utf-8")
        hook.chmod(0o755)
    config = tmp_path / "gitconfig"
    config.write_text(f"[core]\n\thooksPath = {hooks}\n", encoding="utf-8")
    return config


def test_a_global_hooks_path_cannot_reach_a_scratch_repository(tmp_path, monkeypatch):
    """B10 (PR #49 second-review tail): the scratch world must not run the invoking
    ENGINEER's git hooks.

    `core.hooksPath` is the one global git setting that makes git execute the
    developer's own code inside our throwaway repositories, and every popular hook
    manager sets exactly it. With a failing `pre-commit` configured this way the
    session suite gave 195 errors + 10 failures, all raised at fixture setup as
    `CalledProcessError` on `git commit` — an error that names git and not hooks,
    so it reads as a broken branch rather than as a local configuration. Both ENDS
    are covered: the checkout's `pre-commit`/`pre-push` and the bare origin's
    `pre-receive`/`update`, since the harness pushes.

    The oracle is deliberately the WHOLE fixture rather than a config read: what
    must hold is that the scratch world still builds, and asserting the setting
    would pass a fixture that set it in the wrong repository."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(_global_hooks_world(
        tmp_path, "pre-commit", "pre-push", "pre-receive", "update")))
    # the world the fixture must survive is real: prove the hook WOULD fire
    unguarded = tmp_path / "unguarded"
    unguarded.mkdir()
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(unguarded)],
                   check=True, capture_output=True, text=True)
    (unguarded / "f.md").write_text("x\n", encoding="utf-8")
    for args in (["add", "f.md"],):
        subprocess.run(["git", "-C", str(unguarded), *args], check=True,
                       capture_output=True, text=True)
    refused = subprocess.run(
        ["git", "-C", str(unguarded), "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-m", "seed"], capture_output=True, text=True)
    assert refused.returncode != 0, "the probe hook did not fire — the test is inert"

    repo = build_scratch_repo(tmp_path / "world")

    assert repo.head(), "the seed commit did not land"
    assert repo.origin_branches() == ("main",), "the push did not land"
    # and a SESSION-shaped commit (the branch the gate actions ride) too
    repo.git("checkout", "-q", "-b", "draft/demo-topic")
    repo.write("ideation/staging/demo-topic/note.md", "# note\n\nStatus: draft\n")
    assert repo.commit("a gate action", "ideation/staging/demo-topic/note.md")
    repo.git("checkout", "-q", "main")


# --------------------------------------------------------------------------
# T002 — the fakes: no network, no real notebook, no approval authority
# --------------------------------------------------------------------------

@pytest.mark.parametrize("forbidden", ["merge", "approve", "review",
                                       "self_review", "bypass_protection",
                                       "enable_auto_merge"])
def test_fake_pull_requests_exposes_no_approval_operation(forbidden):
    # FR-030: the ABSENCE is the enforcement, not a refusal message.
    assert not hasattr(FakePullRequests(), forbidden)


def test_fake_pull_requests_is_idempotent_per_branch_and_records_calls():
    port = FakePullRequests()
    port.push("draft/demo-topic")
    first = port.open_or_update("draft/demo-topic", base="main", title="t", body="b")
    again = port.open_or_update("draft/demo-topic", base="main", title="t", body="b")
    assert again == first
    assert port.find_open("draft/demo-topic") == first
    assert port.find_open("draft/other") is None
    assert ("push", "draft/demo-topic") in port.calls


def test_fake_notebook_adapter_records_the_session_lifecycle():
    adapter = FakeNotebookAdapter()
    adapter.create("xf-session-openxfactory-demo-topic", ["a.md"])
    adapter.resync("xf-session-openxfactory-demo-topic", ["a.md", "b.md"])
    assert adapter.live_aliases() == ("xf-session-openxfactory-demo-topic",)
    adapter.retire("xf-session-openxfactory-demo-topic")
    assert adapter.live_aliases() == ()


def test_fake_notebook_adapter_can_exhaust_the_quota():
    adapter = FakeNotebookAdapter(quota_exhausted=True)
    with pytest.raises(QuotaExhausted):
        adapter.create("xf-session-openxfactory-demo-topic")
    assert adapter.live_aliases() == ()


# --------------------------------------------------------------------------
# T004 — the container is gitignored and unscannable (FR-005; research R7)
# --------------------------------------------------------------------------

def find_aggregation_root(start: Path | None = None) -> Path | None:
    """The xFactory aggregation checkout: the ancestor carrying `.gitmodules`
    and an `openxFactory/` directory. None when unreachable (a bare clone of
    this repo alone), in which case the real-tree half of the regression skips
    and the synthetic half still runs."""
    base = (start or REPO_ROOT).resolve()
    for d in [base, *base.parents]:
        if (d / ".gitmodules").is_file() and (d / "openxFactory").is_dir():
            return d
    return None


def _check_ignore(root: Path, relpath: str) -> str | None:
    done = subprocess.run(["git", "check-ignore", "-v", relpath],
                          cwd=str(root), text=True, capture_output=True,
                          check=False)
    return done.stdout.strip() or None


def test_worktree_container_is_gitignored_in_the_aggregation_repo():
    agg = find_aggregation_root()
    if agg is None:
        pytest.skip("no aggregation checkout reachable from this tree")
    for rel in ("xFactories/codexFactory-worktrees/",
                "xFactories/codexFactory-worktrees/sessions/draft__demo-topic/",
                "xFactories/codexFactory-worktrees/sessions/draft__demo-topic/a.md",
                "openxFactory-worktrees/sessions/draft__demo-topic/"):
        matched = _check_ignore(agg, rel)
        assert matched is not None, f"{rel} is NOT gitignored — FR-005 broke"
        # the finding is specifically that the EXISTING `*-worktrees/` pattern
        # covers it, so no new ignore entry is owed (research R7)
        assert matched.endswith("*-worktrees/\t" + rel) or "*-worktrees/" in matched


def test_the_worktrees_pattern_covers_the_sessions_sub_path(tmp_path):
    """The synthetic half: an aggregation-shaped repo whose ONLY relevant
    ignore line is the one research R7 found. Proves the PATTERN semantics
    independently of the real workspace's ignore file."""
    root = tmp_path / "aggregation"
    root.mkdir()
    subprocess.run(["git", "init", "--initial-branch=main", str(root)],
                   check=True, capture_output=True, text=True)
    (root / ".gitignore").write_text("*-worktrees/\n", encoding="utf-8")
    assert _check_ignore(root, "xFactories/codexFactory-worktrees/") is not None
    assert _check_ignore(
        root, "xFactories/codexFactory-worktrees/sessions/draft__t/doc.md") is not None
    # and it does NOT over-reach into the governed repo itself
    assert _check_ignore(root, "xFactories/codexFactory/docs/doc.md") is None


def test_session_worktrees_never_reach_a_lifecycle_book(tmp_path):
    """FR-039 / research R7's second half: the book scan excludes the worktree
    container by name AND anything under a nested `.git`, so a session worktree
    contributes NO source, title, or repository to any of the lifecycle books."""
    doc = "Status: staged\n"
    root = tmp_path / "workspace"
    (root / "openxFactory/ideation/staging/real").mkdir(parents=True)
    (root / "openxFactory/ideation/staging/real/README.md").write_text(
        "# Real\n\n" + doc, encoding="utf-8")
    governed = root / "xFactories/codexFactory"
    (governed / "docs").mkdir(parents=True)
    (governed / ".git").mkdir()
    (governed / "docs/real-doc.md").write_text("# Governed\n\n" + doc, encoding="utf-8")
    (root / ".gitmodules").write_text(
        '[submodule "codexFactory"]\n\tpath = xFactories/codexFactory\n'
        "\turl = https://example.invalid/codexFactory.git\n", encoding="utf-8")

    # a SESSION worktree, exactly where FR-005 puts it
    session = root / "xFactories/codexFactory-worktrees/sessions/draft__demo-topic"
    (session / "ideation/staging/demo-topic").mkdir(parents=True)
    (session / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
    (session / "ideation/staging/demo-topic/README.md").write_text(
        "# Session draft\n\n" + doc, encoding="utf-8")

    # `scan` returns (desired, specs) since split-ideation-book-per-repo
    # (2026-08-10) — this test still unpacked the pre-split dict and failed with
    # `'tuple' object has no attribute 'items'` on every run. Repaired here
    # rather than left red; the CLAIM being tested is untouched.
    desired, _specs = sync.scan(root)

    assert desired  # the scan produced books
    for book, entries in desired.items():
        for relpath, title in entries.items():
            assert "-worktrees" not in relpath, (
                f"book {book} projected a worktree source: {relpath}")
            assert "Session draft" not in title
            assert "sessions/" not in relpath
    # the control: the governed and openxFactory documents DID project, so the
    # assertion above is not passing on an empty scan. The ideation family is
    # PER-REPOSITORY since split-ideation-book-per-repo, so the control looks
    # across the whole family instead of one shared `ideation` key — which keeps
    # it proving what it always proved (the scan was not empty) without this
    # test taking a position on how that family is keyed.
    ideation = {relpath
                for key, entries in desired.items()
                if key.startswith(sync.IDEATION_KEY_PREFIX)
                for relpath in entries}
    assert any(r.endswith("openxFactory/ideation/staging/real/README.md")
               for r in ideation), sorted(ideation)
    assert any(r.endswith("xFactories/codexFactory/docs/real-doc.md")
               for r in ideation), sorted(ideation)


def test_pinned_factory_paths_never_admits_a_worktree_container(tmp_path):
    """The other exclusion research R7 names: `pinned_factory_paths` is
    pin-state driven, and its no-.gitmodules fallback drops `*-worktrees` by
    suffix. Both halves asserted, so removing either is a test failure."""
    root = tmp_path / "workspace"
    (root / "xFactories/codexFactory").mkdir(parents=True)
    (root / "xFactories/codexFactory-worktrees/sessions").mkdir(parents=True)

    # fallback (no .gitmodules): suffix heuristic
    assert sync.pinned_factory_paths(root) == ["xFactories/codexFactory"]

    # pin-state (with .gitmodules): only pinned paths
    (root / ".gitmodules").write_text(
        '[submodule "codexFactory"]\n\tpath = xFactories/codexFactory\n'
        "\turl = https://example.invalid/codexFactory.git\n", encoding="utf-8")
    assert sync.pinned_factory_paths(root) == ["xFactories/codexFactory"]
