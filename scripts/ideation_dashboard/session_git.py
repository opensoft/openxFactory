"""The ONLY git-WRITE surface in the dashboard (007-workbench-branch-sessions
T005/T006; contracts/session-ports.md).

Before this module the dashboard scripts contained no `git commit`, `git add`,
`git push`, or `gh pr` anywhere — every git subprocess was a READ (research
R4). Git writes are therefore a NEW capability class, and the whole point of
putting them in one file is that the audit surface is one file: if a later task
needs a git write somewhere else, that is a design smell, not a shortcut.

Four structural rules, enforced by construction rather than by convention:

  1. **The served checkout never moves** (FR-004, SC-002). Every command routes
     through ONE funnel (`SessionGit.git`), and that funnel decides what a
     command is allowed to do by asking two questions the CALLER cannot lie
     about: does the argv carry a git ROUTING option (`-C`, `--git-dir`,
     `--work-tree`, `--exec-path`, `--namespace`), and does the cwd resolve
     INSIDE the served checkout? A routing option is refused outright, at every
     cwd, because it redirects the command at a repository the guard did not
     inspect; and a cwd at or under the served root may run only the ALLOWLISTED
     read/bookkeeping subcommands (`SERVED_ALLOWED_SUBCOMMANDS`). PR #49 review
     finding 18 measured all three bypasses the previous cwd-equality denylist
     permitted — a served SUBDIRECTORY, `git -C <served>`, and
     `git --git-dir <served>/.git --work-tree <served>` each moved the served
     checkout, and `stage()` + `commit()` at the served root advanced its HEAD.
     An allowlist cannot be bypassed by naming a subcommand nobody thought of.
     Session writes reach a branch only through its own worktree.
  2. **Staging is explicit-path only** (shared-tree discipline, root CLAUDE.md).
     `stage()` refuses `-A`, `--all`, `-u`, `.`, `*`, `:/`, an empty list, any
     option-shaped token, and any path escaping the worktree. A shared checkout
     serves other sessions; `git add -A` would sweep their work into this
     commit.
  3. **There is NO amend operation** (FR-006). One `commit` per gate action,
     carrying the action's documents AND its record together. A commit cannot
     contain its own sha, so the record embeds none: the record names its own
     action stamp, the commit message repeats it as a `Gate-Action: <stamp>`
     trailer, and the resulting sha is RETURNED to the caller for the response.
     The amend-then-restamp dance would leave a record naming a pre-amend sha
     the amend made unreachable, so the operation simply does not exist here.
  4. **A gate action owns the worktree's index for its whole duration**
     (FR-006, SC-003; PR #49 review finding 1). `commit(only=[...])` spells
     `git commit --only -- <paths>`, so the commit contains the action's DECLARED
     paths and nothing else even if a foreign path is staged concurrently; and
     `worktree_action_lock()` is a CROSS-PROCESS lock (an `O_EXCL` link into the
     worktree's own git dir), because the second writer is routinely a separate
     CLI process and a `threading.Lock` cannot see one. git's own `index.lock`
     serializes each individual subprocess but NOT the multi-step
     stage → commit → sha-capture action, which is exactly why the winner used to
     absorb the loser's document and record under the winner's `Gate-Action`
     trailer while the loser was told it had failed.

`remote_ordinals` uses `git ls-remote --heads`, which is side-effect-free, and
NEVER `git fetch` (FR-026, D17): the remote is a necessary input to ordinal
allocation because two machines must not allocate the same one, but reading it
must not touch local refs. `local_ordinals` is equally mandatory — nothing in
this feature pushes before `open-pr`, so a never-pushed abandoned branch exists
only locally — and the next ordinal is computed over the UNION of the two by
`branch_session.py`, which owns the tile-identity semantics this module has no
opinion about.

The runner is injected (`GitRunner`), so a caller may substitute one; the tests
prefer a REAL throwaway repository with a local bare `origin`, because git's own
behaviour (ref legality, worktree bookkeeping, commit counts) is what they are
asserting (research R10).
"""

from __future__ import annotations

import contextlib
import json
import os
import socket
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Protocol, Sequence

# The one prefix the SERVED checkout's working tree may legitimately change in:
# `propose` / `demote` / `dispose` already write their records here, and so do
# the main-resident `open-pr` / `abandon-session` records (plan Constraint 10).
# The immovability fingerprint excludes it for exactly that reason.
GATE_RECORDS_PREFIX = "ideation/dashboard/gate-records/"

# Subcommands that MOVE a checkout. Named separately from the allowlist because
# their refusal message is the one a human most needs to read (FR-004) — the
# allowlist below is what actually decides.
FORBIDDEN_SERVED_SUBCOMMANDS = ("checkout", "switch", "reset", "stash", "restore")

# The ONLY subcommands permitted with a cwd at or under the served checkout: reads
# plus the ref/worktree bookkeeping the session lifecycle genuinely performs there
# (worktree add/remove/list/prune, branch create/delete, the remote branch delete).
# Nothing that touches the served working tree, its index, or its HEAD is here —
# `add`, `commit`, `mv`, `rm`, `merge`, `clean`, `apply`, `am`, `rebase`,
# `cherry-pick`, `revert`, `update-ref`, `symbolic-ref`, `update-index`,
# `sparse-checkout`, `filter-branch` and the five FORBIDDEN_SERVED_SUBCOMMANDS all
# fall through to a refusal because they are ABSENT, which is the property a
# denylist could never have (PR #49 finding 18).
SERVED_ALLOWED_SUBCOMMANDS = frozenset({
    "branch", "cat-file", "check-ref-format", "diff", "for-each-ref", "log",
    "ls-files", "ls-remote", "ls-tree", "merge-base", "push", "remote",
    "rev-list", "rev-parse", "show", "show-ref", "status", "worktree",
})

# Refused at EVERY cwd. `fetch`/`pull` would touch local refs; the remote is read
# with `ls-remote` and NEVER fetched.
#
# WHERE THAT RULE ACTUALLY LIVES, corrected 2026-08-21 (PR #234 review, P3-A).
# This comment used to say "FR-026/D17 is explicit", which reads as a citation of
# ratified spec prose. It is not one. The rule's only written home is a
# SANCTIONED-DEVIATION note inside a realization task —
# `openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/tasks.md:97`,
# "(`git ls-remote --heads`, never a fetch)" — plus this guard and the refusal
# texts that cite it. `FR-026`/`D17` are that change's own feature and decision
# numbering, not requirement ids in any promoted spec: no requirement under
# `openspec/specs/` carries the never-fetch rule at all.
#
# PROMOTION CANDIDATE, recorded because the gap is the interesting part: this
# rule carries real architectural weight — it is why the resume path cannot
# materialize a remote branch itself, which is the whole shape of §12's colleague
# hand-off (PR #234, Codex P1) — and a rule that decides that much while living
# only in an archived change's task note is one an implementer can neither find
# nor safely weigh. It belongs in a ratified requirement. Raising that is a
# separate change with its own proposal; this note is the pointer, not the fix.
FORBIDDEN_ANYWHERE_SUBCOMMANDS = ("fetch", "pull")

# Git's own repository-ROUTING options. They redirect a command at a repository
# and working tree that are not the cwd's, so a guard that inspected only the cwd
# was answering the wrong question (PR #49 finding 18, reproduced three ways).
# Refused at every cwd: every legitimate operation here passes its `cwd` instead.
GIT_ROUTING_OPTIONS = ("-C", "--git-dir", "--work-tree", "--exec-path",
                       "--namespace", "--super-prefix")

# The gate-action lock (FR-006, SC-003). It lives in the WORKTREE's own git dir,
# so it is per-session, it is cleaned up with the worktree, and — being a file —
# it is visible to a separate CLI process as well as to a second server thread.
ACTION_LOCK_NAME = "xf-session-action.lock"

# How long a lock may sit before a NEW writer is allowed to break it. A crashed
# holder on THIS host is detected immediately by its dead pid; the window is the
# fallback for a holder this process cannot interrogate (another host sharing the
# tree over a network filesystem, an unparseable payload).
ACTION_LOCK_STALE_SECONDS = 900

# Every spelling of "stage everything", plus the pathspec magic that reaches
# outside the caller's declared paths. Refused before git is invoked.
STAGE_EVERYTHING_TOKENS = frozenset({
    "-A", "--all", "-u", "--update", "--no-all", ".", "*", ":/", ":/.", "--",
})


class GitError(RuntimeError):
    """A git command failed. Carries the argv and git's own stderr, because a
    session refusal is only useful if the human can read the engine's reason."""

    def __init__(self, args: Sequence[str], returncode: int, stderr: str) -> None:
        self.argv = tuple(args)
        self.returncode = returncode
        self.stderr = (stderr or "").strip()
        super().__init__(f"git {' '.join(args)} failed ({returncode}): {self.stderr}")


class SessionGitRefused(Exception):
    """A STRUCTURAL refusal by this module — an illegal derived ref, a
    stage-everything spelling, a path escaping the worktree, a protected branch.
    Raised before git is invoked, so nothing is half-done."""


class ServedCheckoutImmovable(SessionGitRefused):
    """The served checkout may not be switched, reset, stashed, or restored by
    any session operation (FR-004). This is the guard firing."""


class SessionActionInProgress(SessionGitRefused):
    """Another writer already owns this session worktree's index (FR-006).

    A gate action is stage → commit → capture-the-sha, and that sequence is a
    TRANSACTION: git's own `index.lock` serializes each subprocess but not the
    action, so two overlapping actions used to produce one commit carrying both
    actions' documents and records under only the winner's `Gate-Action` trailer.
    The loser is now told this, loudly, before anything is written — which is
    exactly the "a losing race MUST fail loudly rather than silently clobbering"
    the spec's edge case asks for.

    `holder` carries whatever the lock file said about the writer that owns it, so
    the refusal can name it rather than say "someone"."""

    def __init__(self, message: str, *, holder: dict | None = None) -> None:
        self.holder = dict(holder or {})
        super().__init__(message)


# --------------------------------------------------------------------------
# the injectable runner
# --------------------------------------------------------------------------

class GitRunner(Protocol):
    def run(self, cwd: Path, *args: str) -> subprocess.CompletedProcess: ...


class SubprocessGitRunner:
    """The real runner: `git` as a subprocess, output captured, never checked
    here (the funnel raises `GitError` so every failure carries git's stderr)."""

    def run(self, cwd: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=str(cwd), text=True,
                              capture_output=True, check=False)


# --------------------------------------------------------------------------
# the immovability guard — a pure function, so it is testable on its own
# --------------------------------------------------------------------------

def command_subcommand(args: Sequence[str]) -> str:
    """The git subcommand in an argv, skipping leading `-c key=value` style
    options — a guard that only looked at `args[0]` would be bypassed by
    `git -c core.pager=cat checkout main`."""
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg == "-c" or arg == "--config-env":
            skip_next = True
            continue
        if arg.startswith("-"):
            continue
        return arg
    return ""


def command_routing_options(args: Sequence[str]) -> tuple[str, ...]:
    """The repository-ROUTING options an argv carries (`-C`, `--git-dir`,
    `--work-tree`, `--exec-path`, `--namespace`), in both the separate-value and
    the `--opt=value` spellings.

    These are the bypasses PR #49 finding 18 reproduced: they retarget the command
    at a repository the guard never looked at, so `cwd` stopped being the truth
    about what the command would touch. Every operation in this module passes an
    explicit `cwd` instead, so a routing option is never a legitimate input here —
    which makes "refuse them all" both safe and complete."""
    found: list[str] = []
    for arg in args:
        for option in GIT_ROUTING_OPTIONS:
            if arg == option or arg.startswith(f"{option}="):
                found.append(option)
    return tuple(dict.fromkeys(found))


def targets_served_checkout(served_root: Path, cwd: Path) -> bool:
    """Whether a command run in `cwd` acts on the SERVED checkout.

    Resolved by CONTAINMENT, not string equality: `<served>/ideation` is the
    served checkout's working tree just as much as `<served>` is, and a `git
    checkout` run there moves it identically (measured). Session worktrees live in
    `<repo>-worktrees/` — a SIBLING of the checkout by construction
    (`branch_session.container_root`) — so containment never misclassifies one."""
    try:
        here = Path(cwd).resolve()
        served = Path(served_root).resolve()
    except OSError:                                  # pragma: no cover - defensive
        return str(cwd) == str(served_root)
    return here == served or served in here.parents


def guard_served_command(served_root: Path, cwd: Path,
                         args: Sequence[str]) -> bool:
    """True when this argv is permitted. False when it could move the SERVED
    checkout, or when it routes around the cwd the guard was given (FR-004).

    Three questions, in the order that makes the answer independent of caller
    honesty:

      1. does the argv carry a git ROUTING option? Then the cwd says nothing about
         what the command would touch — refused at every cwd.
      2. is the subcommand refused everywhere (`fetch`, `pull`)? FR-026/D17 reads
         the remote with `ls-remote` and never fetches.
      3. does the cwd resolve at or under the served checkout? Then the subcommand
         must be in `SERVED_ALLOWED_SUBCOMMANDS` — an ALLOWLIST, so a subcommand
         nobody enumerated is refused rather than permitted.

    A worktree is disposable, so inside a session worktree only (1) and (2) apply:
    the write operations exist precisely to run there."""
    if command_routing_options(args):
        return False
    subcommand = command_subcommand(args)
    if subcommand in FORBIDDEN_ANYWHERE_SUBCOMMANDS:
        return False
    if not targets_served_checkout(served_root, cwd):
        return True
    return subcommand in SERVED_ALLOWED_SUBCOMMANDS


# --------------------------------------------------------------------------
# the fingerprint
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class WorktreeRecord:
    """ONE `git worktree list --porcelain` entry, whole (PR #49 finding 5).

    `branch` is the short name the worktree HOLDS — the answer the joint
    worktree/branch signal (FR-008, G13) is about, and the field the previous
    path-only parse discarded. `detached` and `prunable` are the two states in
    which there is no branch to be joint WITH; `locked` is the state in which
    `git worktree remove` refuses, which is how a teardown leaves residue."""

    path: Path
    branch: str | None = None
    detached: bool = False
    locked: bool = False
    prunable: bool = False


@dataclass(frozen=True)
class ServedFingerprint:
    """Branch + HEAD + filtered porcelain (FR-004, SC-002). Branch and HEAD must
    be BYTE-IDENTICAL across every session operation. The porcelain comparison
    EXCLUDES the declared gate-records prefix, where the main-resident `open-pr`
    / `abandon-session` records legitimately land."""

    branch: str
    head: str
    porcelain: tuple[str, ...]


def porcelain_path(line: str) -> str:
    """The path a `git status --porcelain` line names; a rename line carries
    `old -> new` and the NEW path is where the content now IS, which is what the
    split-write guard (`dirty_paths`) asks about."""
    return porcelain_paths(line)[-1]


def porcelain_paths(line: str) -> tuple[str, ...]:
    """EVERY path a `git status --porcelain` line names — both halves of a rename
    or copy, in `old, new` order.

    The immovability filter needs both (PR #49 review finding 18, reproduced):
    `git mv ideation/staging/<topic>/notes.md ideation/dashboard/gate-records/…`
    produces ONE line whose destination is inside the declared records prefix, so a
    filter that could only see the destination dropped the line entirely and
    reported the served checkout UNCHANGED while a governed staging file had left
    the tree. A line is excluded only when EVERY path it names is declared."""
    body = line[3:] if len(line) > 3 else ""
    halves = body.split(" -> ", 1) if " -> " in body else [body]
    return tuple(half.strip().strip('"') for half in halves) or ("",)


def declared_only(line: str, prefix: str) -> bool:
    """True when every path the line names is inside `prefix` — the only shape the
    served checkout's working tree may legitimately change in (SC-002)."""
    paths = porcelain_paths(line)
    return bool(paths) and all(p.startswith(prefix) for p in paths)


def _pid_alive(pid: int) -> bool:
    """Whether a process id is still running on THIS host. `signal 0` asks the
    kernel without touching the process; `PermissionError` means it exists and
    belongs to somebody else, which for a lock holder is still ALIVE."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:                                  # pragma: no cover - defensive
        return True
    return True


# --------------------------------------------------------------------------
# the cross-process gate-action lock (FR-006, SC-003; PR #49 finding 1)
# --------------------------------------------------------------------------

def _read_lock(path: Path) -> dict | None:
    """The holder payload, or None when the file is absent. An unparseable file is
    reported as an empty holder rather than as "unlocked" — a lock nobody can read
    is still a lock, and only the staleness window may break it."""
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:                                  # pragma: no cover - defensive
        return {}
    try:
        loaded = json.loads(raw)
    except ValueError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _lock_age(path: Path, holder: dict) -> float:
    created = holder.get("created")
    if isinstance(created, (int, float)):
        return max(0.0, time.time() - float(created))
    try:
        return max(0.0, time.time() - path.stat().st_mtime)
    except OSError:                                  # pragma: no cover - defensive
        return 0.0


def lock_is_stale(path: Path, holder: dict, *,
                  stale_seconds: float = ACTION_LOCK_STALE_SECONDS) -> bool:
    """Whether a held lock may be broken.

    A holder this process CAN interrogate is answered by its pid and nothing else:
    dead means the transaction is over and the lock may be taken; ALIVE means the
    lock is authoritative however old it is. Breaking a live holder's lock on age
    would put two writers inside one worktree's index, which is the whole defect.

    Only a holder that cannot be interrogated — another host sharing the tree, a
    payload that will not parse, a file with no pid — waits out `stale_seconds`."""
    pid = holder.get("pid")
    host = holder.get("host")
    if isinstance(pid, int) and host == socket.gethostname():
        return not _pid_alive(pid)
    return _lock_age(path, holder) > stale_seconds


def _lock_refusal(path: Path, holder: dict) -> SessionActionInProgress:
    who = holder.get("action") or "a gate action"
    pid = holder.get("pid")
    host = holder.get("host")
    where = f" (pid {pid} on {host})" if pid else ""
    return SessionActionInProgress(
        f"refusing to start a gate action: {who}{where} already owns this session "
        f"worktree's index and has not finished. A gate action is ONE commit "
        f"carrying its documents and its record together, so two overlapping "
        f"writers would put both actions' files in one commit under one action's "
        f"trailer (FR-006, SC-003) — the losing writer is refused instead. Wait for "
        f"the other action to finish and run this one again; if that writer is gone, "
        f"the lock {path} is released automatically once it is stale.",
        holder=holder)


def _claim_lock(path: Path, payload: dict, *,
                stale_seconds: float = ACTION_LOCK_STALE_SECONDS) -> Path:
    """Create `path` atomically WITH its payload already in it, or refuse.

    `open(O_CREAT|O_EXCL)` then write leaves a window in which the file exists and
    is EMPTY, and a competitor reading it there could not tell a fresh lock from an
    abandoned one. Writing a temp file and `os.link`-ing it into place closes the
    window: the name appears only when the content is already complete."""
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, sort_keys=True) + "\n"
    temp = path.with_name(f"{path.name}.{os.getpid()}.{uuid.uuid4().hex}")
    temp.write_text(body, encoding="utf-8")
    try:
        try:
            os.link(temp, path)
            return path
        except FileExistsError:
            holder = _read_lock(path) or {}
            if not lock_is_stale(path, holder, stale_seconds=stale_seconds):
                raise _lock_refusal(path, holder) from None
            with contextlib.suppress(FileNotFoundError):
                os.unlink(path)
            try:
                os.link(temp, path)
            except FileExistsError:
                # somebody else won the break; theirs is fresh, so this one loses
                raise _lock_refusal(path, _read_lock(path) or {}) from None
            return path
    finally:
        with contextlib.suppress(OSError):
            temp.unlink()


# --------------------------------------------------------------------------
# the operation set (contracts/session-ports.md)
# --------------------------------------------------------------------------

class SessionGit:
    """Session git operations, each scoped with an explicit `cwd` inside a
    worktree or a READ against the served checkout."""

    def __init__(self, served_root: Path | str, *, runner: GitRunner | None = None,
                 remote: str = "origin",
                 records_prefix: str = GATE_RECORDS_PREFIX) -> None:
        self.served_root = Path(served_root).resolve()
        self.runner: GitRunner = runner or SubprocessGitRunner()
        self.remote = remote
        self.records_prefix = records_prefix

    # ---- the ONE funnel ----
    def git_raw(self, cwd: Path | str, *args: str) -> str:
        """Run one git command and return its stdout with only the TRAILING
        newline removed. Guards the served checkout FIRST (before git is
        invoked), then raises `GitError` with git's own stderr on a non-zero
        exit.

        Leading whitespace is significant in `git status --porcelain`, whose
        first line begins with a space for a worktree-only modification
        (` M path`) — stripping it would shift every path by one character and
        make the fingerprint's prefix filter read the wrong path."""
        self._guard(cwd, args)
        done = self.runner.run(Path(cwd), *args)
        if done.returncode != 0:
            raise GitError(args, done.returncode, done.stderr or "")
        return (done.stdout or "").rstrip("\n")

    def _guard(self, cwd: Path | str, args: Sequence[str]) -> None:
        """Raise `ServedCheckoutImmovable` when the guard refuses, with the reason
        the human needs: which of the three questions answered no."""
        if guard_served_command(self.served_root, Path(cwd), args):
            return
        routing = command_routing_options(args)
        subcommand = command_subcommand(args)
        if routing:
            raise ServedCheckoutImmovable(
                f"refusing `git {subcommand or '<no subcommand>'}` carrying "
                f"{', '.join(routing)}: a repository-ROUTING option retargets the "
                "command at a repository and working tree this guard never "
                "inspected, so the served checkout could be moved from any cwd "
                "(FR-004). Every operation here passes an explicit `cwd` instead")
        if subcommand in FORBIDDEN_ANYWHERE_SUBCOMMANDS:
            raise ServedCheckoutImmovable(
                f"refusing `git {subcommand}`: the remote is read with "
                "`ls-remote --heads`, which is side-effect-free, and NEVER fetched "
                "— a fetch touches local refs, which ordinal allocation reads "
                "(FR-026, D17)")
        raise ServedCheckoutImmovable(
            f"refusing `git {subcommand or '<no subcommand>'}` against the served "
            f"checkout {self.served_root} (cwd {Path(cwd)}): a cwd at or under the "
            "served checkout may run only "
            f"{', '.join(sorted(SERVED_ALLOWED_SUBCOMMANDS))} — no session "
            "operation may switch, reset, stash, restore, merge, clean, stage, or "
            "commit there (FR-004). Session writes reach a branch only through "
            "that branch's own worktree")

    def git(self, cwd: Path | str, *args: str) -> str:
        """`git_raw` with the output stripped — the ordinary read/write form."""
        return self.git_raw(cwd, *args).strip()

    def _try(self, cwd: Path | str, *args: str) -> tuple[bool, str]:
        """A read whose FAILURE is an answer (`check-ref-format`, an absent
        branch) rather than an error."""
        self._guard(cwd, args)
        done = self.runner.run(Path(cwd), *args)
        return done.returncode == 0, (done.stdout or "").strip()

    # ---- ref legality: every derived name is validated before any git call ----
    def check_ref_format(self, branch: str) -> bool:
        """git's OWN answer for `refs/heads/<branch>`. A colon-qualified corpus
        staging id fails here, which is why `branch_session.reduce_scope_id`
        exists (research R2, data-model validation rules)."""
        if not branch or branch.startswith("-"):
            return False
        ok, _ = self._try(self.served_root, "check-ref-format",
                          f"refs/heads/{branch}")
        return ok

    def require_legal_ref(self, branch: str) -> str:
        if not self.check_ref_format(branch):
            raise SessionGitRefused(
                f"{branch!r} is not a legal git branch name "
                "(`git check-ref-format refs/heads/<branch>` refused it); a "
                "derived session branch is validated before any git call")
        return branch

    # ---- worktrees ----
    def worktree_add(self, branch: str, path: Path | str, base: str) -> Path:
        """`git worktree add -b <branch> <path> <base>` — the OPEN path. `base`
        is the served checkout's `main`; this is never a `checkout` in the
        served tree."""
        self.require_legal_ref(branch)
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.git(self.served_root, "worktree", "add", "-b", branch,
                 str(target), base)
        return target

    def worktree_add_existing(self, branch: str, path: Path | str) -> Path:
        """`git worktree add <path> <branch>` — the RESUME path (FR-025): a
        worktree re-materialized over an EXISTING branch, keeping its name."""
        self.require_legal_ref(branch)
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.git(self.served_root, "worktree", "add", str(target), branch)
        return target

    def checked_out_at(self, branch: str) -> str | None:
        """The working tree that currently has `branch` CHECKED OUT, or None.

        `git for-each-ref --format=%(worktreepath)` fills that field exactly when
        some working tree holds the ref, which is the condition `git worktree
        add` refuses with exit 128. Asking BEFORE the add turns a raw GitError
        naming neither cause nor remedy into the session vocabulary's own
        refusal (PR #234, Codex P1).

        A pure REF READ: no remote contact, no fetch, nothing written — so it is
        legal on the served checkout and costs the resume path nothing."""
        listed = self.git(self.served_root, "for-each-ref",
                          "--format=%(worktreepath)", f"refs/heads/{branch}")
        for line in listed.splitlines():
            if line.strip():
                return line.strip()
        return None

    def worktree_remove(self, path: Path | str) -> None:
        """`git worktree remove --force <path>` — teardown, BOTH endings
        (FR-021). Removes the directory and git's bookkeeping; the BRANCH
        survives, which is what makes an abandoned branch abandonable."""
        self.git(self.served_root, "worktree", "remove", "--force", str(path))

    def worktree_records(self) -> tuple["WorktreeRecord", ...]:
        """Every worktree git knows about, WITH the branch each one holds.

        `git worktree list --porcelain` emits a `worktree <path>` line followed by
        `HEAD <sha>` and then either `branch refs/heads/<name>` or `detached`, plus
        `locked`/`prunable` when they apply. Until PR #49 review finding 5 this
        method kept only the FIRST line and threw the rest away, which left every
        consumer — the bootstrap, `_known_worktrees`, `open_session`'s adoption arm
        — structurally unable to ask the one question that matters: WHICH BRANCH
        does this worktree hold? They asked "is there a directory?" and "does a
        branch by this directory's decoded name exist?" instead, and a worktree
        sitting on another branch was registered as the session — after which the
        next gate action's commit landed on that other branch while the response
        and the evidence chain named the session's (reproduced through the real
        CLI). The branch is git's own answer and it was already on the wire."""
        listed = self.git_raw(self.served_root, "worktree", "list", "--porcelain")
        records: list[WorktreeRecord] = []
        path: Path | None = None
        branch: str | None = None
        detached = locked = prunable = False
        for line in listed.splitlines() + [""]:
            if line.startswith("worktree "):
                path = Path(line[len("worktree "):])
                branch, detached, locked, prunable = None, False, False, False
            elif line.startswith("branch "):
                ref = line[len("branch "):].strip()
                branch = ref[len("refs/heads/"):] \
                    if ref.startswith("refs/heads/") else ref
            elif line.strip() == "detached":
                detached = True
            elif line == "locked" or line.startswith("locked "):
                locked = True
            elif line == "prunable" or line.startswith("prunable "):
                prunable = True
            elif not line.strip() and path is not None:
                records.append(WorktreeRecord(path, branch, detached, locked,
                                              prunable))
                path = None
        return tuple(records)

    def worktree_paths(self) -> tuple[Path, ...]:
        """Every worktree git knows about, served root included. D10 names
        `git worktree list` as the session's derivation source. Derived from
        `worktree_records` so there is ONE parse of git's porcelain."""
        return tuple(record.path for record in self.worktree_records())

    def worktree_branch(self, path: Path | str) -> "WorktreeRecord | None":
        """git's own record for the worktree at `path`, or None when git does not
        know that directory as a worktree at all."""
        target = Path(path).resolve()
        for record in self.worktree_records():
            try:
                if record.path.resolve() == target:
                    return record
            except OSError:                          # pragma: no cover - defensive
                continue
        return None

    def worktree_prune(self) -> None:
        """Drop bookkeeping for worktree directories that no longer exist — the
        stale-directory reconciliation's cleanup half (FR-008)."""
        self.git(self.served_root, "worktree", "prune")

    # ---- branches ----
    def branch_exists(self, branch: str) -> bool:
        ok, _ = self._try(self.served_root, "show-ref", "--verify", "--quiet",
                          f"refs/heads/{branch}")
        return ok

    def branch_sha(self, branch: str) -> str | None:
        """The sha `refs/heads/<branch>` currently points at, or None when the
        branch does not exist. The compare-and-swap input for a delete."""
        ok, listed = self._try(self.served_root, "show-ref", "--hash",
                               f"refs/heads/{branch}")
        return listed.strip() or None if ok else None

    def path_last_commit_at(self, path: Path | str) -> str | None:
        """The committer date of the newest commit touching a repository path."""
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.served_root / candidate
        resolved = candidate.resolve()
        if resolved != self.served_root and not resolved.is_relative_to(
                self.served_root):
            raise SessionGitRefused(
                f"refusing to inspect history for {path!r}: it escapes the "
                f"served checkout {self.served_root}")
        rel = resolved.relative_to(self.served_root).as_posix()
        ok, recorded_at = self._try(
            self.served_root, "log", "-1", "--format=%cI", "--", rel)
        return recorded_at.strip() or None if ok else None

    def _atomic_delete_ref(self, branch: str, expect_sha: str) -> None:
        """Delete one local branch with Git's expected-old-value transaction.

        This is the deliberately narrow exception to the served-checkout command
        allowlist: callers cannot issue arbitrary ``update-ref`` commands, and
        this helper can only delete the already validated ``refs/heads`` name at
        the exact observed object id.
        """
        ref = f"refs/heads/{self.require_legal_ref(branch)}"
        done = self.runner.run(
            self.served_root, "update-ref", "-d", ref, expect_sha)
        if done.returncode != 0:
            current = self.branch_sha(branch)
            if current != expect_sha:
                raise SessionGitRefused(
                    f"refusing to delete {branch!r}: it was at {expect_sha} when "
                    f"cleanup was authorized and is at {current} now. Git's "
                    "atomic expected-value ref transaction preserved the changed "
                    "ref; observe it and decide again")
            raise GitError(
                ("update-ref", "-d", ref, expect_sha), done.returncode,
                done.stderr or "")

    def restore_branch_if_absent(self, branch: str, sha: str) -> None:
        """Atomically restore a just-deleted ref only while it remains absent."""
        ref = f"refs/heads/{self.require_legal_ref(branch)}"
        done = self.runner.run(
            self.served_root, "update-ref", ref, sha, "0" * len(sha))
        if done.returncode != 0:
            current = self.branch_sha(branch)
            raise SessionGitRefused(
                f"could not restore {branch!r} at {sha}: the ref is now "
                f"{current}; refusing to overwrite it")

    def delete_branch(self, branch: str, *, remote: bool = False,
                      expect_sha: str | None = None, safe: bool = False) -> None:
        """Delete a session branch. Used by the merge ending (FR-033) and the
        human-invoked abandoned-branch cleanup (FR-028) — never by an abandon,
        which deletes nothing.

        Two orderings matter, and both were wrong before PR #49 finding 9:

          * `expect_sha` makes the delete a COMPARE-AND-SWAP. The caller observed a
            tip and decided, on the strength of that tip, that the branch was
            merged; if the tip has moved since, a gate-action commit landed after
            the observation and `-D` would make it unreachable from any ref
            (reproduced). A moved tip refuses instead.
          * the REMOTE delete runs FIRST. `git branch -D` is irreversible and the
            push is the fallible half, so doing the local one first left the remote
            branch alive, the local ref gone, and the operation unretryable — the
            next observation answered "no such branch, nothing to reconcile".

        `safe=True` spells `git branch -d`, which makes git itself re-check that the
        branch is contained in HEAD. The merge ending uses it; FR-028's cleanup
        deletes a branch nobody merged and therefore cannot."""
        if branch in ("main", "master", "HEAD"):
            raise SessionGitRefused(
                f"refusing to delete {branch!r}: session branch deletion is for "
                "session branches only (FR-033, FR-028)")
        if branch == self.current_branch(self.served_root):
            raise SessionGitRefused(
                f"refusing to delete {branch!r}: it is the served checkout's "
                "current branch (FR-004)")
        checked_out = self.checked_out_at(branch)
        if checked_out:
            raise SessionGitRefused(
                f"refusing to delete {branch!r}: it is checked out at "
                f"{checked_out}")
        if expect_sha is not None:
            current = self.branch_sha(branch)
            if current != expect_sha:
                raise SessionGitRefused(
                    f"refusing to delete {branch!r}: it was at {expect_sha} when the "
                    f"decision to delete it was made and it is at {current} now, so "
                    "work landed on it after that observation and deleting it would "
                    "make that work unreachable from any ref (FR-033). Observe the "
                    "branch again and decide again")
        if remote and self.has_remote():
            # FIRST, because it is the fallible one: a failed push must leave the
            # local ref in place so the whole delete is retryable
            self.git(self.served_root, "push", self.remote, "--delete", branch)
        if expect_sha is not None and not safe:
            self._atomic_delete_ref(branch, expect_sha)
        else:
            self.git(self.served_root, "branch", "-d" if safe else "-D", branch)

    # ---- staging + commit: explicit paths, ONE commit, no amend ----
    def stage(self, worktree: Path | str, paths: Iterable[str]) -> tuple[str, ...]:
        """`git add -- <explicit paths>` inside the worktree.

        NEVER `git add -A`. The checkout is shared with other sessions and
        sweeping their uncommitted work into this commit is the exact failure
        the house rule exists to prevent, so every stage-everything spelling is
        refused BEFORE git is invoked."""
        root = Path(worktree).resolve()
        cleaned: list[str] = []
        for raw in paths:
            rel = str(raw).replace("\\", "/").strip()
            if not rel:
                raise SessionGitRefused("stage() takes explicit paths; an empty "
                                        "path is not one")
            if rel in STAGE_EVERYTHING_TOKENS or rel.startswith("-") or rel.startswith(":"):
                raise SessionGitRefused(
                    f"refusing to stage {rel!r}: stage() takes EXPLICIT paths "
                    "only — `git add -A` (and every other stage-everything "
                    "spelling) would sweep other sessions' uncommitted work "
                    "into this commit")
            resolved = (root / rel).resolve()
            if resolved != root and root not in resolved.parents:
                raise SessionGitRefused(
                    f"refusing to stage {rel!r}: it resolves outside the session "
                    f"worktree {root} (confinement, not a fallback)")
            cleaned.append(rel)
        if not cleaned:
            raise SessionGitRefused(
                "stage() requires at least one explicit path — a gate action "
                "with nothing to stage has nothing to commit")
        self.git(root, "add", "--", *cleaned)
        return tuple(cleaned)

    def unstage(self, worktree: Path | str, paths: Iterable[str]) -> tuple[str, ...]:
        """`git reset -q -- <explicit paths>` inside the worktree: take exactly
        these paths OUT of the index, leaving the working tree alone.

        The unwind half of the gate-action transaction (FR-006). A failed action
        must persist NOTHING, and an action that staged its document and record and
        then failed to commit used to leave both staged — so the human's retry
        committed TWO gate-action records in ONE commit, under only the retry's
        trailer (PR #49 finding 1, reproduced with no concurrency at all).

        NEVER a bare `git reset` and never `--hard`: the working tree is where the
        human's drafting lives, and this operation may not touch it."""
        root = Path(worktree).resolve()
        cleaned = tuple(str(p).replace("\\", "/").strip() for p in paths)
        cleaned = tuple(p for p in cleaned if p)
        if not cleaned:
            return ()
        for rel in cleaned:
            if rel.startswith("-") or rel.startswith(":"):
                raise SessionGitRefused(
                    f"refusing to unstage {rel!r}: explicit paths only")
        self.git(root, "reset", "-q", "--", *cleaned)
        return cleaned

    def commit(self, worktree: Path | str, message: str, *,
               only: Sequence[str] | None = None) -> str:
        """ONE commit per gate action, carrying document(s) AND record. Returns
        the resulting sha for the caller's RESPONSE — it is never written into
        the record, because a commit cannot contain its own sha (FR-006).

        `only` binds the commit to an EXACT path set: `git commit --only -- <paths>`
        builds the commit from those paths and DISREGARDS everything else in the
        index. Without it a bare `git commit` commits the ambient index, so a
        pre-staged neighbour's file — or a second writer's document and record —
        rode the action's commit under the action's `Gate-Action` trailer (PR #49
        finding 1, reproduced three ways). The caller passes its declared documents
        plus its record; nothing else can enter the commit even if a foreign `git
        add` lands between the stage and the commit.

        There is deliberately no amend, no reword, and no squash counterpart."""
        root = Path(worktree)
        if not (message or "").strip():
            raise SessionGitRefused("a gate-action commit requires a message "
                                    "carrying its `Gate-Action: <stamp>` trailer")
        args: list[str] = ["commit", "-m", message]
        if only is not None:
            declared = [str(p).replace("\\", "/").strip() for p in only]
            declared = [p for p in declared if p]
            if not declared:
                raise SessionGitRefused(
                    "commit(only=…) takes the action's EXPLICIT declared paths; an "
                    "empty set would fall back to the ambient index, which is the "
                    "absorption this argument exists to prevent (FR-006)")
            for rel in declared:
                if rel in STAGE_EVERYTHING_TOKENS or rel.startswith("-") \
                        or rel.startswith(":"):
                    raise SessionGitRefused(
                        f"refusing to commit {rel!r}: commit(only=…) takes EXPLICIT "
                        "paths only, never a stage-everything spelling")
            args += ["--only", "--", *declared]
        self.git(root, *args)
        return self.head(root)

    def staged_paths(self, worktree: Path | str) -> tuple[str, ...]:
        """What is currently staged in the worktree — the input to the
        one-commit-per-action check.

        Called BEFORE staging (the index must be empty: anything already there is
        somebody else's, or a failed attempt's residue) and AGAIN after, where it
        must equal exactly the action's declared documents plus its record. Until
        PR #49 finding 1 this helper had no caller at all: it was written for the
        check and the check was never made."""
        listed = self.git(Path(worktree), "diff", "--cached", "--name-only")
        return tuple(l for l in listed.splitlines() if l)

    def tracked_paths(self, worktree: Path | str,
                      paths: Iterable[str]) -> tuple[str, ...]:
        """Which of `paths` git already TRACKS (`git ls-files -- <paths>`).

        The gate-action unwind reads it before staging: a declared document git has
        never heard of exists only because THIS action created it, so a refusal
        removes it; a tracked document carries history and human edits, so a
        refusal leaves the working tree exactly as it found it."""
        cleaned = [str(p).replace("\\", "/").strip() for p in paths]
        cleaned = [p for p in cleaned if p and not p.startswith("-")]
        if not cleaned:
            return ()
        listed = self.git(Path(worktree), "ls-files", "--", *cleaned)
        return tuple(l.strip() for l in listed.splitlines() if l.strip())

    # ---- the gate-action transaction lock (FR-006, SC-003) ----
    def action_lock_path(self, worktree: Path | str) -> Path:
        """The lock file for one session worktree, inside that worktree's OWN git
        dir (`<served>/.git/worktrees/<name>/`), which is where its index lives and
        which git removes with the worktree."""
        git_dir = self.git(Path(worktree), "rev-parse", "--absolute-git-dir")
        return Path(git_dir) / ACTION_LOCK_NAME

    def read_action_lock(self, worktree: Path | str) -> dict | None:
        """Whatever the lock file says about its holder, or None when unlocked."""
        try:
            return _read_lock(self.action_lock_path(worktree))
        except (GitError, SessionGitRefused, OSError):    # pragma: no cover
            return None

    @contextlib.contextmanager
    def worktree_action_lock(self, worktree: Path | str, *,
                             action: str = "gate action",
                             stale_seconds: float = ACTION_LOCK_STALE_SECONDS
                             ) -> Iterator[Path]:
        """Own this worktree's index for the duration of one gate action.

        CROSS-PROCESS by construction: an `O_EXCL` link of a fully written payload
        into the worktree's git dir. A `threading.Lock` would have been useless —
        CLI parity (FR-024) means the second writer is routinely a separate process
        (`cli.py gate edit-document` beside a `ThreadingHTTPServer` request), and
        the review reproduced exactly that shape.

        NON-BLOCKING on purpose. The spec's edge case says a losing race MUST fail
        loudly rather than silently clobber, so the loser is refused immediately and
        told who holds the lock — nobody waits, nothing is queued, and the refusal
        is deterministic rather than timing-dependent.

        Stale-lock policy: a holder whose pid is gone on THIS host is broken
        immediately (its index work is over by definition, and the emptiness check
        inside the action is what protects against residue it left); any other
        holder is broken only after `stale_seconds`. A lock is never silently
        ignored."""
        path = self.action_lock_path(worktree)
        payload = {
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "action": action,
            "worktree": str(Path(worktree)),
            "created": time.time(),
        }
        _claim_lock(path, payload, stale_seconds=stale_seconds)
        try:
            yield path
        finally:
            with contextlib.suppress(OSError):
                path.unlink()

    def dirty_paths(self, worktree: Path | str) -> tuple[str, ...]:
        """Every path the worktree's status names (untracked included). The
        split-write guard reads it: a declared document that is already CLEAN
        was committed by an earlier commit, so its record could only ride a
        different one (FR-006)."""
        listed = self.git_raw(Path(worktree), "status", "--porcelain",
                              "--untracked-files=all")
        return tuple(porcelain_path(l) for l in listed.splitlines() if l.strip())

    # ---- ordinal inputs (FR-026, D17) ----
    def has_remote(self) -> bool:
        _, listed = self._try(self.served_root, "remote")
        return self.remote in listed.split()

    def remote_ordinals(self, prefix: str) -> tuple[str, ...]:
        """Branch names on the REMOTE beginning with `prefix`, read with
        `git ls-remote --heads` — side-effect-free, and NEVER `git fetch`.
        MANDATORY: without the remote, two machines allocate the same ordinal
        (FR-026, D17). Returns () when no remote is configured, which is a real
        condition for a local-only scratch checkout, not an error.

        The result is a raw PREFIX scan: deciding which of those names belong to
        this tile's ordinal family (and which are another tile's deterministic
        name) is `branch_session`'s job, not this module's."""
        if not self.has_remote():
            return ()
        listed = self.git(self.served_root, "ls-remote", "--heads", self.remote,
                          f"{prefix}*")
        names = []
        for line in listed.splitlines():
            if "\t" not in line:
                continue
            ref = line.split("\t", 1)[1].strip()
            name = ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref
            if name.startswith(prefix):
                names.append(name)
        return tuple(sorted(set(names)))

    def remote_sha(self, branch: str) -> str | None:
        """The sha `refs/heads/<branch>` points at ON THE REMOTE, read with
        `git ls-remote --heads` — side-effect-free, and NEVER a `git fetch`
        (FR-026, D17).

        The merge observation needs it: a real GitHub merge advances the REMOTE
        base, and a served checkout that has not pulled still shows the pre-merge
        `main`. Reading the base only locally meant the reconciliation answered
        "not merged" about a branch that HAD merged, and then re-pushed the head
        branch the merge had deleted (PR #49 finding 9, reproduced). Returns None
        when there is no remote or no such remote branch — a real condition for a
        local-only scratch checkout, not an error."""
        if not self.has_remote():
            return None
        listed = self.git(self.served_root, "ls-remote", "--heads", self.remote,
                          f"refs/heads/{branch}")
        for line in listed.splitlines():
            if "\t" not in line:
                continue
            sha, ref = line.split("\t", 1)
            if ref.strip() in (f"refs/heads/{branch}", branch):
                return sha.strip() or None
        return None

    def tracking_sha(self, branch: str) -> str | None:
        """The sha this checkout's `refs/remotes/<remote>/<branch>` points at, or
        None — a purely LOCAL ref read (`git rev-parse --verify`), no remote
        contact of any kind.

        It answers one question no other read can: has this branch ever LEFT this
        checkout? `git push` writes the remote-tracking ref, and nothing in this
        feature prunes it, so the ref survives the remote head's deletion — which
        is exactly the case that matters. `remote_sha` says "it is on the remote
        NOW", and a merge that deletes the head branch makes that None again,
        indistinguishable from a branch that was never pushed at all. The two are
        very different: only the first can already have merged (PR #49 critic
        finding C2)."""
        ok, sha = self._try(self.served_root, "rev-parse", "--verify", "--quiet",
                            f"refs/remotes/{self.remote}/{branch}")
        value = sha.strip()
        return value if ok and value else None

    def has_object(self, sha: str) -> bool:
        """Whether this checkout HAS the object `sha` (`git cat-file -e`). Asked
        about a remote tip that was never fetched: an unknown object is proof the
        local base is behind the remote one, which is the honest reading of a stale
        served checkout."""
        if not sha:
            return False
        ok, _ = self._try(self.served_root, "cat-file", "-e", f"{sha}^{{commit}}")
        return ok

    def merge_landing(self, base: str, branch: str) -> str | None:
        """The MERGE COMMIT on `base` that landed `branch` — or None.

        D18 mandates a merge commit, so the shape is exact and checkable: a commit
        reachable from `base`, not reachable from `branch`, on an ancestry path from
        `branch`, whose SECOND (or later) parent IS `branch`'s tip. That is a
        positive proof the branch's own commits came into the base through a merge
        of THIS branch.

        It replaces the previous "the tips differ" half of the observation, which
        any EMPTY session satisfied as soon as the base moved for any unrelated
        reason — the review reproduced a fresh session being torn down and its
        branch deleted after one unrelated commit on `main`. An empty branch's tip
        is a base commit, so it appears only as a FIRST parent, never as a merged
        one, and the shape below excludes it structurally rather than by luck."""
        tip = self.branch_sha(branch)
        if not tip:
            return None
        ok, listed = self._try(self.served_root, "rev-list", "--merges", "--parents",
                               "--ancestry-path", f"{branch}..{base}")
        if not ok:
            return None
        for line in listed.splitlines():
            parts = [p for p in line.split() if p]
            if len(parts) < 3:
                continue
            # parts[0] is the merge commit, parts[1] its FIRST parent, the rest the
            # branches it merged IN
            if tip in parts[2:]:
                return parts[0]
        return None

    def local_ordinals(self, prefix: str) -> tuple[str, ...]:
        """Branch names in the LOCAL refs beginning with `prefix`
        (`git branch --list`). Also MANDATORY: nothing in this feature pushes
        before `open-pr`, so a never-pushed abandoned branch exists only here
        (FR-026)."""
        listed = self.git(self.served_root, "branch", "--list", f"{prefix}*",
                          "--format=%(refname:short)")
        return tuple(sorted(l.strip() for l in listed.splitlines()
                            if l.strip().startswith(prefix)))

    # ---- the record's `commit` artifact resolution (FR-006) ----
    def introduced_by(self, path: str, *, cwd: Path | str | None = None,
                      ref: str | None = None) -> str | None:
        """`git log --diff-filter=A --format=%H -- <path>` — the commit that
        INTRODUCED `path`. That is how a record's `commit`-kind artifact
        reference resolves: the record carries its own action stamp, and the
        commit it names is the one that added the record file, which immediately
        after the action is the branch TIP. Returns None when the path was never
        added on this history."""
        args = ["log", "--diff-filter=A", "--format=%H"]
        if ref:
            args.append(ref)
        args += ["--", path]
        listed = self.git(Path(cwd) if cwd else self.served_root, *args)
        lines = [l.strip() for l in listed.splitlines() if l.strip()]
        # newest first; the commit that INTRODUCED it is the oldest match
        return lines[-1] if lines else None

    # ---- reads ----
    def head(self, cwd: Path | str | None = None, ref: str = "HEAD") -> str:
        return self.git(Path(cwd) if cwd else self.served_root, "rev-parse", ref)

    def current_branch(self, cwd: Path | str | None = None) -> str:
        return self.git(Path(cwd) if cwd else self.served_root,
                        "rev-parse", "--abbrev-ref", "HEAD")

    def merge_base(self, base: str, branch: str) -> str | None:
        """`git merge-base <base> <branch>` — the revision the branch forked
        from. A READ whose failure (unrelated histories, an absent ref) is an
        answer: None. It is how a session's recorded base is re-derived when
        the OPEN that knew it is a previous process (T104 R-12): a session
        branch is created FROM its base and every gate action commits on the
        branch alone, so the merge base IS the branch point."""
        ok, sha = self._try(self.served_root, "merge-base", base, branch)
        return sha or None if ok else None

    def is_ancestor(self, ref: str, base: str) -> bool:
        """`git merge-base --is-ancestor <ref> <base>` — whether `base` already
        CONTAINS `ref`'s tip. A READ whose failure is an answer.

        Part of the merge observation FR-033's ending is triggered by
        (`branch_session.merge_state`): after the Merge Master lands a session
        pull request as the MERGE COMMIT D18 mandates, the session branch's tip is
        an ancestor of `main`. It is never sufficient on its own, and the
        "and the tips DIFFER" half that used to complete it was not sufficient
        either — an EMPTY session satisfies both as soon as the base moves for any
        unrelated reason (PR #49 review finding 9, reproduced: one unrelated commit
        on `main` made a session that had written nothing look merged). The
        positive proof is `merge_landing`, below: a merge commit on the base whose
        merged parent IS this branch's tip."""
        ok, _ = self._try(self.served_root, "merge-base", "--is-ancestor",
                          ref, base)
        return ok

    def commits_ahead(self, base: str, branch: str) -> int:
        """`git rev-list --count <base>..<branch>` — SC-003's promise that a
        session branch is EXACTLY one commit per gate action ahead of its fork
        point, and the assertion an amend-based implementation could not pass."""
        return int(self.git(self.served_root, "rev-list", "--count",
                            f"{base}..{branch}") or "0")

    def served_checkout_fingerprint(self) -> ServedFingerprint:
        """The immovability assertion (FR-004, SC-002). `--untracked-files=all`
        so every porcelain line names a FILE: an untracked-directory summary
        line would make the prefix filter coarser than the declared prefix."""
        porcelain = self.git_raw(self.served_root, "status", "--porcelain",
                                 "--untracked-files=all").splitlines()
        return ServedFingerprint(
            branch=self.current_branch(self.served_root),
            head=self.head(self.served_root),
            # a line is dropped only when EVERY path it names is declared: a rename
            # OUT of the governed tree INTO the records prefix names both, and
            # filtering on the destination alone reported it as no change at all
            # (PR #49 finding 18, reproduced)
            porcelain=tuple(l for l in porcelain
                            if not declared_only(l, self.records_prefix)))
