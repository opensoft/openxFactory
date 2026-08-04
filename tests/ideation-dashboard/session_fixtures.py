"""Branch-session test harness (007-workbench-branch-sessions T001/T002).

Three things live here, and every session test builds on them:

  * `scratch_repo` — a THROWAWAY git repository in `tmp_path` with a local BARE
    `origin`, a minimal staged-topic fragment, and a worktree container beside
    it. Research R10's rule is absolute: no session test points a serve or a
    session operation at a real checkout or at a fixture corpus, because a serve
    with `--checkout-root` WRITES into whatever tree it is given (a proven
    hazard). Everything is `tmp_path`, and `origin` is a bare repo on disk — so
    `git ls-remote` is exercised for real with NO network.

  * `served_fingerprint()` — the immovability assertion (FR-004, SC-002): the
    served checkout's branch, `rev-parse HEAD`, and `git status --porcelain`,
    with the DECLARED `ideation/dashboard/gate-records/` prefix filtered OUT of
    the porcelain, because the main-resident `open-pr` / `abandon-session`
    records land there legitimately (plan Constraint 10, SC-002). It is
    implemented here with plain `subprocess` rather than by calling
    `session_git.served_checkout_fingerprint`, deliberately: a test that asserts
    immovability with the same helper the implementation uses would pass a
    broken implementation that lied identically in both directions.

  * `FakePullRequests` / `FakeNotebookAdapter` — so no test can reach a network
    or create a real NotebookLM notebook (FR-043).

`FakePullRequests` and `PullRequest` are RE-EXPORTED from
`scripts/ideation_dashboard/session_pr.py`, which T063 (Phase 7) created: the
fake is declared beside the port it implements and beside the real
`GhPullRequests`, so the three cannot drift apart. This module keeps the names so
every pre-Phase-7 import site still works, and there is exactly ONE definition.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

# The ONE definition of the port's fake (T063) — re-exported, never re-declared.
from ideation_dashboard.session_pr import (  # noqa: F401 - re-export
    FakePullRequests, PullRequest, PullRequestPort, PullRequestRefused,
)

# The ONE staged-topic shape, from the plainly named module rather than from the
# ambient `conftest` name (PR #49 review finding 19a): pytest deletes
# `sys.modules["conftest"]` before importing each directory's conftest, so a
# `from conftest import ...` executed inside a fixture BODY resolves to whichever
# conftest was imported LAST — which made this harness's own shapes depend on
# collection order and raise `ImportError` at setup in the reverse order.
from staging_shapes import staging_fragment

# The one prefix the served checkout's working tree may legitimately change in
# (plan Constraint 10): `propose` / `demote` / `dispose` already write here, and
# so do the main-resident `open-pr` / `abandon-session` records.
GATE_RECORDS_PREFIX = "ideation/dashboard/gate-records/"

DEFAULT_REPOSITORY = "openxFactory"
DEFAULT_TOPIC = "demo-topic"

# The directory `core.hooksPath` is pointed at in every scratch repository: it
# exists and is EMPTY, so git finds no hook of any name (PR #49 second-review tail
# B10).
#
# WHY THE HARNESS MUST SAY THIS. A scratch repository inherits the invoking
# engineer's GLOBAL git config, and `core.hooksPath` is the one global setting that
# makes git run THEIR code inside our throwaway repositories — husky, lefthook and
# `pre-commit` all install exactly that. With a failing `pre-commit` configured
# globally (an ordinary setup), five session modules gave 195 errors + 10 failures,
# every one of them raised at FIXTURE SETUP as
# `CalledProcessError: Command '['git','commit','-m','Seed the scratch corpus']'
# returned non-zero exit status 1` — an error naming git rather than hooks, and
# therefore indistinguishable from a broken branch. The identical world with that
# one config line removed passed 232. The T092 acceptance pass is not reproducible
# on a machine whose suite cannot run, so this is hermeticity in the same sense
# `tests/hermeticity.py` means it: the ambient installation must not change the
# answer. `commit.gpgsign` was already pinned here for the same reason — signing is
# the OTHER global that fails a scratch commit — and hooks were the gap.
#
# Set on BOTH ends of the scratch world: the checkout runs `pre-commit`/`pre-push`,
# and the bare origin runs `pre-receive`/`update` on the harness's own `git push`.
# Repository-LOCAL config, deliberately, rather than `GIT_CONFIG_GLOBAL` in the
# hermeticity fixture: it is scoped to the repositories this harness owns, so it
# cannot alter how any other test reads any other repository.
HOOKS_NEUTRAL_DIRNAME = ".no-hooks"


# --------------------------------------------------------------------------
# the served-checkout fingerprint (SC-002)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ServedFingerprint:
    """Branch + HEAD + filtered porcelain. Branch and HEAD must be
    BYTE-IDENTICAL across every session operation; the porcelain may differ
    only inside the declared gate-records prefix."""

    branch: str
    head: str
    porcelain: tuple[str, ...]


def _porcelain_names(line: str) -> tuple[str, ...]:
    """EVERY path a `git status --porcelain` line names.

    Both halves of a rename, deliberately (PR #49 review finding 18). Keeping only
    the DESTINATION made this oracle blind to exactly the event it exists to catch:
    `git mv ideation/staging/<topic>/notes.md ideation/dashboard/gate-records/…`
    produces one line whose destination is declared, so the line was filtered away
    and the fingerprint reported the served checkout UNCHANGED while a governed file
    had left the tree. The production filter had the same hole, which is why the
    two AGREEING proved nothing — see `test_session_git.py` for the oracle that now
    asserts the move is DETECTED rather than that two copies of a filter agree."""
    body = line[3:] if len(line) > 3 else ""
    halves = body.split(" -> ", 1) if " -> " in body else [body]
    return tuple(half.strip().strip('"') for half in halves)


def _porcelain_path(line: str) -> str:
    """Where the line's content now IS (a rename's destination)."""
    return _porcelain_names(line)[-1]


def filter_declared_paths(lines, prefix: str = GATE_RECORDS_PREFIX) -> tuple[str, ...]:
    """Drop a line only when EVERY path it names is inside `prefix`."""
    return tuple(l for l in lines
                 if not (_porcelain_names(l)
                         and all(p.startswith(prefix)
                                 for p in _porcelain_names(l))))


def fingerprint_of(root: Path, *, prefix: str = GATE_RECORDS_PREFIX) -> ServedFingerprint:
    def raw(*args: str) -> str:
        done = subprocess.run(["git", *args], cwd=str(root), text=True,
                              capture_output=True, check=True)
        # only the TRAILING newline: a porcelain line for a worktree-only
        # modification BEGINS with a space (` M path`), and stripping it would
        # shift every path by one character.
        return done.stdout.rstrip("\n")

    return ServedFingerprint(
        branch=raw("rev-parse", "--abbrev-ref", "HEAD").strip(),
        head=raw("rev-parse", "HEAD").strip(),
        # `--untracked-files=all` so every porcelain line names a FILE: an
        # untracked directory summary line (`?? ideation/brainstorm/`) would
        # make the prefix filter coarser than the declared prefix.
        porcelain=filter_declared_paths(
            raw("status", "--porcelain", "--untracked-files=all").splitlines(),
            prefix))


# --------------------------------------------------------------------------
# the scratch world
# --------------------------------------------------------------------------

@dataclass
class ScratchRepo:
    """A throwaway served checkout + its bare `origin` + its worktree
    container. `repository` is the registry-key repository NAME the dashboard
    uses, and the checkout directory is named after it so the container is
    exactly `<repo>-worktrees/` (FR-005, research R7)."""

    root: Path                  # the SERVED checkout (never switched/reset)
    origin: Path                # a BARE repository acting as `origin`
    container: Path             # <repo>-worktrees/  (sibling of the checkout)
    repository: str = DEFAULT_REPOSITORY
    topic_id: str = DEFAULT_TOPIC

    # ---- plumbing ----
    def git(self, *args: str, cwd: Path | None = None) -> str:
        done = subprocess.run(["git", *args], cwd=str(cwd or self.root),
                              text=True, capture_output=True, check=True)
        return done.stdout.strip()

    def write(self, relpath: str, text: str, *, cwd: Path | None = None) -> Path:
        target = (cwd or self.root) / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def commit(self, message: str, *paths: str, cwd: Path | None = None) -> str:
        """Stage EXPLICIT paths and commit. Never `git add -A` — the shared-tree
        house rule holds in the fixtures too."""
        assert paths, "stage explicit paths (never -A)"
        self.git("add", "--", *paths, cwd=cwd)
        self.git("commit", "-m", message, cwd=cwd)
        return self.git("rev-parse", "HEAD", cwd=cwd)

    # ---- reads ----
    def head(self, ref: str = "HEAD") -> str:
        return self.git("rev-parse", ref)

    def branch(self) -> str:
        return self.git("rev-parse", "--abbrev-ref", "HEAD")

    def local_branches(self) -> tuple[str, ...]:
        return tuple(self.git("branch", "--format=%(refname:short)").splitlines())

    def origin_branches(self) -> tuple[str, ...]:
        listed = self.git("for-each-ref", "--format=%(refname:short)", "refs/heads/",
                          cwd=self.origin)
        return tuple(l for l in listed.splitlines() if l)

    def served_fingerprint(self) -> ServedFingerprint:
        return fingerprint_of(self.root)

    # ---- the mandatory remote-only branch (T007, T049b) ----
    def add_remote_only_branch(self, name: str, at: str | None = None) -> str:
        """Create `name` INSIDE the bare origin with `git update-ref` and do NOT
        fetch afterwards, so the branch exists remotely and has NO local ref.
        This is the only fixture that can tell a real `ls-remote` implementation
        apart from one that reads local refs (contracts/session-ports.md)."""
        sha = at or self.head()
        self.git("update-ref", f"refs/heads/{name}", sha, cwd=self.origin)
        assert name in self.origin_branches()
        assert name not in self.local_branches(), (
            "a remote-only fixture branch must not exist locally")
        return sha


def hooks_neutral_dir(tmp_path: Path) -> Path:
    """The empty directory a scratch repository's `core.hooksPath` points at, made
    once per `tmp_path` (B10). An EMPTY DIRECTORY rather than `/dev/null` so the
    setting reads the same on any platform and so a future fixture that needs a
    deliberate hook has somewhere to put it."""
    target = Path(tmp_path) / HOOKS_NEUTRAL_DIRNAME
    target.mkdir(parents=True, exist_ok=True)
    return target


def build_scratch_repo(tmp_path: Path, *, repository: str = DEFAULT_REPOSITORY,
                       topic_id: str = DEFAULT_TOPIC,
                       extra_topics: tuple[str, ...] = ()) -> ScratchRepo:
    """Build the scratch world: bare origin, served checkout on `main` with one
    staged-topic fragment (plus any `extra_topics`), the gate-records prefix
    present, and an empty worktree container beside the checkout.

    Every ambient git setting that could change the ANSWER is pinned locally in
    both repositories — identity, signing, and hook execution (see
    `HOOKS_NEUTRAL_DIRNAME`)."""
    hooks = hooks_neutral_dir(tmp_path)
    origin = tmp_path / f"{repository}.git"
    subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(origin)],
                   check=True, capture_output=True, text=True)
    # the RECEIVING end's hooks (`pre-receive`, `update`) come from the same global
    # setting, so the harness's own `git push` would run them too
    subprocess.run(["git", "-C", str(origin), "config", "core.hooksPath", str(hooks)],
                   check=True, capture_output=True, text=True)

    root = tmp_path / repository
    root.mkdir()
    repo = ScratchRepo(root=root, origin=origin,
                       container=tmp_path / f"{repository}-worktrees",
                       repository=repository, topic_id=topic_id)
    repo.git("init", "--initial-branch=main")
    repo.git("config", "user.email", "harness@example.invalid")
    repo.git("config", "user.name", "Session Harness")
    repo.git("config", "commit.gpgsign", "false")
    repo.git("config", "core.hooksPath", str(hooks))
    repo.git("remote", "add", "origin", str(origin))

    staged: list[str] = []
    for topic in (topic_id, *extra_topics):
        rel = f"ideation/staging/{topic}/README.md"
        repo.write(rel, staging_fragment(topic.replace("-", " ").title(), topic))
        staged.append(rel)
    repo.write(f"{GATE_RECORDS_PREFIX}.gitkeep", "")
    repo.commit("Seed the scratch corpus", *staged, f"{GATE_RECORDS_PREFIX}.gitkeep")
    repo.git("push", "-u", "origin", "main")

    # The container is a SIBLING of the checkout, so in this scratch world it is
    # outside the repository entirely. In the real workspace it sits inside the
    # AGGREGATION repo, which is what `*-worktrees/` ignores (research R7) — see
    # test_session_harness.py for that regression.
    repo.container.mkdir()
    return repo


@pytest.fixture
def scratch_repo(tmp_path):
    return build_scratch_repo(tmp_path)


# --------------------------------------------------------------------------
# FakePullRequests — no network, ever (FR-043; contracts/session-ports.md).
# Imported from `session_pr` at the head of this module (T063); only the fixture
# wrapper lives here.
# --------------------------------------------------------------------------

@pytest.fixture
def fake_pull_requests():
    return FakePullRequests()


# --------------------------------------------------------------------------
# FakeNotebookAdapter — never a real notebook (FR-043, FR-042)
# --------------------------------------------------------------------------

@dataclass
class FakeNotebook:
    alias: str
    sources: tuple[str, ...] = ()
    retired: bool = False


class FakeNotebookAdapter:
    """The injected notebook seam. `quota_exhausted=True` makes `create` refuse
    with a quota error so the session-open path can be asserted to DEGRADE
    rather than block (FR-042, D19) — and the notice's phrasing (concurrent
    TILES across everyone, never "your sessions") is asserted on the caller's
    message, not here."""

    QUOTA_MESSAGE = "notebook quota exhausted"

    def __init__(self, *, available: bool = True, quota_exhausted: bool = False,
                 scratch: tuple[str, ...] = ()) -> None:
        self._available = available
        self.quota_exhausted = quota_exhausted
        self.notebooks: dict[str, FakeNotebook] = {}
        self.scratch = list(scratch)
        self.calls: list[tuple] = []

    def available(self) -> bool:
        return self._available

    def list_scratch(self) -> list[str]:
        self.calls.append(("list_scratch",))
        return list(self.scratch)

    def create(self, alias: str, sources=()) -> FakeNotebook:
        self.calls.append(("create", alias, tuple(sources)))
        if self.quota_exhausted:
            raise QuotaExhausted(self.QUOTA_MESSAGE)
        nb = FakeNotebook(alias=alias, sources=tuple(sources))
        self.notebooks[alias] = nb
        return nb

    def resync(self, alias: str, sources=()) -> FakeNotebook:
        self.calls.append(("resync", alias, tuple(sources)))
        nb = self.notebooks.get(alias)
        if nb is None:
            raise KeyError(alias)
        nb.sources = tuple(sources)
        return nb

    def retire(self, alias: str) -> None:
        self.calls.append(("retire", alias))
        nb = self.notebooks.get(alias)
        if nb is not None:
            nb.retired = True

    def live_aliases(self) -> tuple[str, ...]:
        return tuple(sorted(a for a, nb in self.notebooks.items() if not nb.retired))


class QuotaExhausted(Exception):
    """The notebook quota is full — a DEGRADATION signal, never a blocker."""


@pytest.fixture
def fake_notebook_adapter():
    return FakeNotebookAdapter()


@pytest.fixture
def fake_cli_notebook(monkeypatch):
    """The CLI's notebook seam, FAKED — the injection `cli._notebook_port`'s own
    docstring already promised ("a named seam purely so a test injects
    `FakeNotebookAdapter`: no test may create a real notebook (FR-043)").

    A CLI verb is a FRESH PROCESS-shaped call with no handler in front of it, so
    unlike the HTTP surface it has no `adapter_factory` to pass: the seam is the
    module attribute. Every verb in the test gets the SAME adapter, so a test that
    invokes the CLI twice can assert what the CLI did to ONE session's notebook —
    which is what makes this an assertion rather than merely a muzzle.

    Requesting this fixture is how a CLI test stays inside FR-043. Forgetting it
    is no longer silent: `tests/hermeticity.py` makes the default runner raise."""
    from ideation_dashboard import cli as cli_mod

    adapter = FakeNotebookAdapter()
    monkeypatch.setattr(cli_mod, "_notebook_port", lambda repo_root: adapter)
    return adapter


@pytest.fixture(autouse=True)
def declared_human_console(monkeypatch):
    """The CLI's HUMAN-CONSOLE declaration, made explicitly for the suite
    (FR-019's third clause; PR #49 review finding 2).

    A CLI session verb now refuses an invocation that cannot show it is a human
    at a console — an interactive terminal, or this explicit declaration for a
    non-interactive human shell. A pytest process has no terminal and IS an
    automated invocation, so it must DECLARE, exactly as a `nohup`-ed human shell
    would. That is the point of making the declaration a runtime check rather than
    an assumption: it is now something a caller has to do, visibly, and something
    a test can withhold.

    Autouse so no CLI test has to think about it, and `monkeypatch`-scoped so it
    is gone the moment the test ends. The refusal is asserted in
    `test_session_confinement.py`, which deletes the variable it sets."""
    from ideation_dashboard import cli as cli_mod

    monkeypatch.setenv(cli_mod.HUMAN_CONSOLE_ENV, "1")
