"""The PULL-REQUEST PORT — the one seam through which a session's work leaves
this machine (007-workbench-branch-sessions T063/T064; FR-029, FR-030, FR-034,
D22; `contracts/session-ports.md`).

`open-pr` is the FIRST dashboard verb that performs a REMOTE write: research R4
found no `git push` and no `gh pr` anywhere in the dashboard scripts before this
feature. That whole capability lives here, behind three operations and NOTHING
else, so that:

  * no test needs a network — every one of them runs against `FakePullRequests`
    (FR-043), and the real adapter's argv is unit-tested through an injected
    runner rather than by invoking `gh`;
  * the REMOTE-WRITE IDENTITY is confined to exactly one class rather than spread
    through a user story (FR-034);
  * and the verb PROVABLY holds no approval authority (FR-030).

**The absence is the enforcement.** There is deliberately no `merge`, `approve`,
`review`, `self_review`, `bypass_protection`, `enable_auto_merge`, or any other
operation that could land or bless a pull request — not on the protocol, not on
the fake, not on the real adapter. A refusal message could be deleted by a later
edit; a method that does not exist cannot be called at all. The merge is the Merge
Master's action under the EXISTING ritual, enforced outside this dashboard by
branch protection, and `PullRequest` carries `url` / `number` / `state` and
nothing a caller could act on.

**The identity is RULED (FR-034, D22 — Brett, 2026-07-26).** On this LOCAL plane
the push and the pull request use the INVOKING ENGINEER'S OWN credential: their
existing `gh` authentication, with no GitHub App and no stored token, so the
remote write is attributable to the human who performed the gate action. The
per-domain-App convention made the codexFactory App look like the plausible
answer and the ruling says it is not. `GhPullRequests` therefore reads the AMBIENT
auth: it accepts no token argument, stores nothing, and synthesizes no credential.
On the HOSTED plane the verb must use the openxfactory domain App once that App
exists and never a personal credential — and the hosted plane is not built in this
feature (FR-048), so this adapter has NO hosted mode and no plane switch. A
successor change adds that adapter beside this one; it never adds a mode to this
one.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

# The port's WHOLE operation set, declared as data so a test can assert on it and
# a fourth operation cannot arrive quietly (FR-030).
PORT_OPERATIONS = ("push", "open_or_update", "find_open")

STATE_OPEN = "open"
DEFAULT_REMOTE = "origin"
DEFAULT_BASE = "main"


class PullRequestRefused(Exception):
    """The remote refused, and the reason is the ENGINE's — reported verbatim.

    `gh`'s own words reach the human unchanged (contracts/cli.md: "a
    missing/invalid `gh` auth is reported verbatim as the engine's refusal"),
    because a paraphrase of an auth failure is the one thing that cannot be acted
    on. Carries no credential and never echoes one: the adapter holds none."""


@dataclass(frozen=True)
class PullRequest:
    """A pull request as this feature is allowed to know it: where it is, which
    number it is, and what state it is in. NOTHING that would let a caller merge
    or approve — no head sha, no review handle, no mergeable flag, no node id."""

    url: str
    number: int
    state: str = STATE_OPEN


# --------------------------------------------------------------------------
# WHAT A SAVE MAY REWRITE (PR #49 second-review finding R2-13)
# --------------------------------------------------------------------------
#
# `title` / `body` are WHAT THE HUMAN SUPPLIED on THIS save, and empty means
# "supplied nothing". `default_title` / `default_body` are what the pull request
# is NAMED when it has to be CREATED and the human named nothing.
#
# The distinction is the whole fix. The route used to substitute its generated
# defaults on BOTH paths, so a second save with the form left blank issued
# `gh pr edit --title 'Session draft/<topic>: <topic>' --body '<the notice>'` and
# REPLACED a reviewer-facing description a human had written — silently, reported
# as `updated: true`, on a series whose per-action commits are FDA-clearance
# traceability evidence (D18). The UI copy told the human the opposite.
#
# So on the UPDATE path only the fields the caller actually supplied are sent, and
# a save that supplied neither issues no edit at all. The defaults are passed
# separately rather than pre-applied by the caller because only the port knows
# whether it is creating or updating — it performs the `find_open` read itself, and
# a caller's earlier read is a race, not an answer.
@runtime_checkable
class PullRequestPort(Protocol):
    """Push the session branch, open or update its pull request, find the open
    one. Three operations, and the absence of every other one is FR-030."""

    def push(self, branch: str) -> None: ...

    def open_or_update(self, branch: str, *, base: str, title: str,
                       body: str, default_title: str = "",
                       default_body: str = "") -> PullRequest: ...

    def find_open(self, branch: str) -> PullRequest | None: ...


# --------------------------------------------------------------------------
# the FAKE — used by EVERY test (FR-043)
# --------------------------------------------------------------------------

class FakePullRequests:
    """In-memory `PullRequestPort`. Records every call so the FR-029 ordering, the
    FR-032 idempotency, and the FR-030 absent operations are all assertable.

    `fail_push` / `fail_open` make the port refuse with a given message, which is
    how the route's "the engine's reason, verbatim" refusal is tested without a
    real remote.

    It MODELS THE REAL ADAPTER'S EDIT SEMANTICS (finding R2-13): the pull
    request's title and body are stored in `texts` and mutated by an update, and
    only the fields a save actually supplied change. Without that the fake returned
    the existing `PullRequest` untouched, so "a blank second save silently replaced
    the human's description" was not expressible through it at all — the divergence
    that made the defect invisible to the suite.

    The recorded `open_or_update` call carries the EFFECTIVE title and body — what
    the pull request reads after the call — because that is the thing a test wants
    to assert, and on the create path it is where the defaults become visible.

    Lives HERE rather than in the test harness (T063) so the fake and the real
    adapter are declared beside each other and cannot drift apart;
    `tests/ideation-dashboard/session_fixtures.py` re-exports this ONE
    definition."""

    def __init__(self, *, fail_push: str | None = None,
                 fail_open: str | None = None) -> None:
        self.calls: list[tuple] = []
        self.pushed: list[str] = []
        self.open_prs: dict[str, PullRequest] = {}
        # branch -> (title, body) as the pull request currently reads
        self.texts: dict[str, tuple[str, str]] = {}
        self._next = 1
        self._fail_push = fail_push
        self._fail_open = fail_open

    def push(self, branch: str) -> None:
        self.calls.append(("push", branch))
        if self._fail_push:
            raise PullRequestRefused(self._fail_push)
        self.pushed.append(branch)

    def open_or_update(self, branch: str, *, base: str, title: str = "",
                       body: str = "", default_title: str = "",
                       default_body: str = "") -> PullRequest:
        existing = self.open_prs.get(branch)
        if existing is not None:
            # the UPDATE path: only what was supplied changes (finding R2-13)
            was_title, was_body = self.texts.get(branch, ("", ""))
            effective = (title or was_title, body or was_body)
        else:
            effective = (title or default_title, body or default_body)
        self.calls.append(("open_or_update", branch, base, *effective))
        if self._fail_open:
            raise PullRequestRefused(self._fail_open)
        self.texts[branch] = effective
        if existing is not None:
            return existing
        pr = PullRequest(url=f"https://example.invalid/pr/{self._next}",
                         number=self._next)
        self._next += 1
        self.open_prs[branch] = pr
        return pr

    def text(self, branch: str) -> tuple[str, str]:
        """The pull request's `(title, body)` as it currently reads — the read a
        test needs to assert that a save preserved what a human wrote."""
        return self.texts.get(branch, ("", ""))

    def find_open(self, branch: str) -> PullRequest | None:
        self.calls.append(("find_open", branch))
        return self.open_prs.get(branch)


# --------------------------------------------------------------------------
# the REAL adapter — the invoking engineer's OWN ambient `gh` auth (D22)
# --------------------------------------------------------------------------

class CommandRunner(Protocol):
    """One subprocess invocation. Injected so the adapter's ARGV is unit-testable
    without ever invoking `git` or `gh` — and so no test can reach a network, a
    real credential, or a real pull request."""

    def run(self, *args: str, cwd: Path | None = None
            ) -> subprocess.CompletedProcess: ...


# --------------------------------------------------------------------------
# REPOSITORY CONFINEMENT (PR #49 review finding 8, leg c)
# --------------------------------------------------------------------------
#
# `git push` is pinned to a repository by its `cwd` — it writes to THIS
# checkout's `origin`, full stop. `gh` is not: it resolves its target from
# `GH_REPO` FIRST, ahead of the checkout's remotes (`gh help environment`). So a
# shell that happens to export `GH_REPO=opensoft/MedxFactory` made `open-pr` push
# the session branch to the served checkout's origin and then open/edit/list the
# pull request in a DIFFERENT repository — reproduced during the PR #49
# adjudication, right down to the wrong-repository URL reported to the human.
#
# Two moves, both here, because this is the one class that speaks `gh`:
#
#   1. the AMBIENT REDIRECTS ARE SCRUBBED from the child environment. `GH_REPO`
#      and `GH_HOST` choose WHICH repository/host a command targets; they are not
#      authentication, and removing them cannot cost the engineer their identity.
#      EVERY other variable — the whole of `gh`'s own configuration and git's
#      credential-helper environment — is inherited untouched, because that
#      inheritance IS the D22 identity. This scrub narrows the TARGET and never
#      the CREDENTIAL: nothing here reads, sets, or forwards one.
#   2. the TARGET IS NAMED EXPLICITLY. `--repo <[HOST/]OWNER/REPO>`, derived from
#      the same remote `git push` writes to, is passed on every `gh` invocation.
#      An origin this cannot parse (a local bare repository, which is what every
#      test uses) yields no pin, and `gh` then resolves from the checkout's own
#      remotes — the correct repository either way, because the redirecting
#      variables are gone.
#
# Neither move accepts, stores, synthesizes, or forwards a credential.
AMBIENT_TARGET_OVERRIDES = ("GH_REPO", "GH_HOST")

_GITHUB_HOST = "github.com"


def child_env(base: dict | None = None) -> dict:
    """The environment a `git`/`gh` child gets: the caller's own, minus the
    variables that REDIRECT the target repository or host.

    Pure and separately testable — the wiring is `SubprocessCommandRunner.run`."""
    env = dict(os.environ if base is None else base)
    for name in AMBIENT_TARGET_OVERRIDES:
        env.pop(name, None)
    return env


def parse_repo_pin(remote_url: str) -> str | None:
    """`OWNER/REPO` (or `HOST/OWNER/REPO` off github.com) for a remote URL, or
    None when the URL names no hosted repository.

    Understands the three spellings a real `origin` carries — `https://host/o/r`,
    `ssh://git@host/o/r`, and the scp-like `git@host:o/r` — with an optional
    `.git` suffix. A filesystem path (`/tmp/…/origin.git`, `../bare.git`) is NOT a
    hosted repository and yields None rather than a guess."""
    url = str(remote_url or "").strip()
    if not url or url.startswith("file://"):
        return None
    host = ""
    tail = ""
    if "://" in url:
        _scheme, _sep, rest = url.partition("://")
        authority, _slash, tail = rest.partition("/")
        host = authority.rpartition("@")[2]
    elif ":" in url and not url.startswith("/") and not url.startswith("."):
        authority, _colon, tail = url.partition(":")
        host = authority.rpartition("@")[2]
    else:
        return None
    host = host.partition(":")[0].strip().lower()
    parts = [p for p in tail.strip("/").split("/") if p]
    if not host or len(parts) < 2:
        return None
    owner, name = parts[-2], parts[-1]
    if name.endswith(".git"):
        name = name[:-len(".git")]
    if not owner or not name:
        return None
    slug = f"{owner}/{name}"
    return slug if host == _GITHUB_HOST else f"{host}/{slug}"


class SubprocessCommandRunner:
    """The production runner. `shell=False` always (the argv is a list, never a
    string), and the ENVIRONMENT is inherited apart from the two variables that
    REDIRECT `gh` at another repository or host (`child_env`) — the inheritance
    that remains IS the D22 identity: `gh` and git's credential helper find the
    engineer's own authentication exactly as they do when the engineer types the
    command. Nothing here sets, reads, or forwards a token."""

    def run(self, *args: str, cwd: Path | None = None
            ) -> subprocess.CompletedProcess:
        return subprocess.run(list(args), cwd=str(cwd) if cwd else None,
                              text=True, capture_output=True, check=False,
                              env=child_env())


class GhPullRequests:
    """`PullRequestPort` over the engineer's OWN `gh` authentication (FR-034, D22).

    Two binaries and no third: `git push` for the branch (git's credential helper,
    which `gh auth setup-git` wires to the very same ambient auth) and `gh pr` for
    the pull request. Both inherit the engineer's AUTHENTICATION environment
    untouched; only the two variables that redirect `gh` at another REPOSITORY
    are removed, and the target is named explicitly instead (`repo_pin`, review
    finding 8) — so the pull request can only ever be opened in the repository
    the branch was pushed to.

    What this class deliberately does NOT have, and why:

      * NO token/credential/App parameter, and no attribute that could hold one.
        The identity is ambient by ruling, so accepting one would create a second,
        unruled identity path (D22) — and a stored token is a credential this
        repository must never hold (working rule 4).
      * NO hosted mode and no plane switch. The hosted plane's identity is the
        openxfactory domain App and the hosted plane is not built here (FR-048);
        a mode flag would be a place for a personal credential to reach it.
      * NO merge/approve/review/protection operation (FR-030) — see the module
        docstring.

    Every refusal is `PullRequestRefused` carrying the command's own stderr
    verbatim, so a missing `gh auth` reaches the human as `gh`'s own sentence."""

    def __init__(self, repo_root: Path | str, *,
                 remote: str = DEFAULT_REMOTE,
                 runner: CommandRunner | None = None) -> None:
        self.repo_root = Path(repo_root)
        self.remote = remote
        self.runner: CommandRunner = runner or SubprocessCommandRunner()
        self._pin_resolved = False
        self._pin: str | None = None

    # ---- the one funnel ----
    def _run(self, *args: str) -> str:
        done = self.runner.run(*args, cwd=self.repo_root)
        if done.returncode != 0:
            raise PullRequestRefused(
                (done.stderr or done.stdout or "").strip()
                or f"`{' '.join(args)}` failed with exit code {done.returncode}")
        return (done.stdout or "").strip()

    # ---- repository confinement (finding 8, leg c) ----
    def repo_pin(self) -> str | None:
        """The `--repo` target, read ONCE from the same remote `git push` writes
        to. Unresolvable is not an error: `gh` then resolves from this checkout's
        remotes, which is the same repository, and the redirecting environment
        variables have already been scrubbed by the runner."""
        if not self._pin_resolved:
            self._pin_resolved = True
            self._pin = self._read_remote_pin()
        return self._pin

    def _read_remote_pin(self) -> str | None:
        try:
            done = self.runner.run("git", "remote", "get-url", self.remote,
                                   cwd=self.repo_root)
        except (OSError, subprocess.SubprocessError):
            return None
        if getattr(done, "returncode", 1) != 0:
            return None
        return parse_repo_pin(getattr(done, "stdout", "") or "")

    def _gh_pr(self, subcommand: str, *rest: str) -> str:
        """`gh pr <subcommand>` with the repository named EXPLICITLY whenever the
        origin says which one it is. One funnel, so no third `gh` call site can
        be added without the pin."""
        pin = self.repo_pin()
        args = ["gh", "pr", subcommand]
        if pin:
            args += ["--repo", pin]
        return self._run(*args, *rest)

    # ---- the three operations, and only these three ----
    def push(self, branch: str) -> None:
        """Push the session branch with the ambient credential. `--set-upstream`
        so a re-invocation is an ordinary update rather than a second first-push
        (FR-032); never `--force`, because a session branch's history is the
        per-action evidence series D18 protects."""
        self._run("git", "push", "--set-upstream", self.remote, branch)

    def open_or_update(self, branch: str, *, base: str = DEFAULT_BASE,
                       title: str = "", body: str = "",
                       default_title: str = "",
                       default_body: str = "") -> PullRequest:
        """Open the pull request, or EDIT the one this branch already has and
        report it (FR-032). Never a second PR for one branch: the `find_open`
        read decides which of the two `gh` commands runs.

        On the UPDATE path only the fields the caller SUPPLIED are sent, and a
        caller that supplied neither issues no `gh pr edit` at all (finding
        R2-13): `gh pr edit --title X --body Y` REPLACES both, so passing
        generated defaults there overwrote a reviewer-facing description a human
        had written. On the CREATE path the pull request has to be named
        something, and that is what `default_title` / `default_body` are for."""
        existing = self.find_open(branch)
        if existing is not None:
            edits: list[str] = []
            if title:
                edits += ["--title", title]
            if body:
                edits += ["--body", body]
            if edits:
                self._gh_pr("edit", branch, *edits)
            return existing
        url = self._gh_pr("create", "--head", branch, "--base", base,
                          "--title", title or default_title,
                          "--body", body or default_body).splitlines()
        created = self.find_open(branch)
        if created is not None:
            return created
        # `gh pr create` prints the URL; the number is its last path segment.
        # Reached only when the list read cannot see the PR it just created.
        location = (url[-1].strip() if url else "")
        return PullRequest(url=location, number=_number_from_url(location))

    def find_open(self, branch: str) -> PullRequest | None:
        """The branch's OPEN pull request, or None. Side-effect-free."""
        raw = self._gh_pr("list", "--head", branch, "--state", "open",
                          "--json", "number,url,state", "--limit", "1")
        try:
            listed = json.loads(raw or "[]")
        except ValueError as exc:
            raise PullRequestRefused(
                f"`gh pr list` did not return JSON for {branch!r}: {exc}") from exc
        if not isinstance(listed, list) or not listed:
            return None
        first = listed[0] if isinstance(listed[0], dict) else {}
        return PullRequest(url=str(first.get("url") or ""),
                           number=int(first.get("number") or 0),
                           state=str(first.get("state") or STATE_OPEN).lower())


def _number_from_url(url: str) -> int:
    tail = str(url or "").rstrip("/").rsplit("/", 1)[-1]
    return int(tail) if tail.isdigit() else 0


__all__ = [
    "AMBIENT_TARGET_OVERRIDES", "DEFAULT_BASE", "DEFAULT_REMOTE",
    "PORT_OPERATIONS", "STATE_OPEN",
    "CommandRunner", "FakePullRequests", "GhPullRequests", "PullRequest",
    "PullRequestPort", "PullRequestRefused", "SubprocessCommandRunner",
    "child_env", "parse_repo_pin",
]
