"""Branch-session IDENTITY, liveness, and the commit-per-gate-action write path
(007-workbench-branch-sessions T008/T010/T015/T016).

A branch session persists NO descriptor (D10): no manifest, no schema, no
database. Everything below is DERIVED from the tile's scope identity, from git,
and from the snapshot registry, so it cannot rot — and so the derivations
themselves ARE the session's identity. A wrong derivation is not cosmetic: it
opens the wrong branch, joins another tile's session, or points a notebook at
the wrong worktree.

What lives here, and why it is not in `gate_routes.py` or `session_git.py`:
session identity is consumed by the routes, the CLI, the snapshot registry, and
the notebook tooling alike, so it cannot live inside any one of them.

Three derivations and one guard rail worth reading before changing anything:

  * `session_branch` — `draft/<topic-id>` for a staged topic, `<kind>/<id>` for
    a cluster or a possible, `-<ordinal>` appended for D17's NEW continuation.
    The staged-topic id is the dashboard's `topic_id` (the staging FOLDER name),
    and a colon-qualified corpus `Staging ID:` is REDUCED to its final segment —
    `git check-ref-format` rejects `:`, so taken literally the ratified
    requirement would make every staged-topic session unopenable (research R2).
  * `notebook_alias` — `xf-session-<repository>-<transformed-branch>-k<digest>`.
    The READABLE half is FR-037's transform (spec C9); the trailing digest of the
    exact (repository, branch) pair is what makes the derivation INJECTIVE, which
    the transform alone is not — it strips `draft/`, lowercases, and joins the
    two halves with a character both halves may contain (FR-037, spec C11; PR #49
    review finding 11). The `xf-session-` prefix is DISJOINT from the
    swept `xf-wb-*` reference-set namespace, so `workbench_orphan_sweep` can
    never take a live session notebook (FR-038, D11).
  * the ORDINAL — highest existing + 1 over the UNION of the remote's branches
    (`git ls-remote --heads`, mandatory against the two-machine race) and the
    local branches (mandatory because nothing here pushes before `open-pr`, so
    an abandoned branch may exist only locally) (FR-026, D17, G5).
  * the NAMESPACE-COLLISION guard — because the ratified ordinal spelling
    appends `-2`, tile `<t>-2`'s FIRST deterministic branch is spelled exactly
    like tile `<t>`'s SECOND session. So both the ordinal scan and the
    abandoned-branch scan EXCLUDE any branch that is another existing tile's
    deterministic name, and a genuine collision is a REFUSAL naming BOTH tiles
    rather than a silent join (FR-002, FR-026, G12).

# Not a lane result (plan Constraint 13 — T016)
#
# `scripts/execution_lane/result.py:14` declares
# `PROHIBITED_CLAIMS = ("branch", "commit", "pull_request", "approval",
# "merge")`: a worker's task RESULT may not claim any of those outcomes,
# because a worker proposes a patch and independent verification decides what
# happened to it. A gate-action RECORD is a different artifact with a different
# author: a HUMAN performed the action, and the record attests to what that
# human's own authority did. That is precisely why a session record MAY name a
# branch (`target.ref`), a commit (`kind: commit`), and a pull request
# (`kind: pull-request`) — the five names the lane forbids a worker to claim.
#
# The rule this comment exists to prevent someone "unifying" away: session
# outcomes are never routed through the execution-lane result type, and
# `validate_result` is never asked to bless a gate-action record. Two artifact
# families, two authorities, no shared type. If a future reader sees the
# overlapping vocabulary and reaches for a merge, the merge would either grant a
# worker the human's claims or strip the human's record of the only names that
# make it auditable.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from . import doxbench_hash
from . import gate_console
# `SessionGitRefused` is re-exported (see __all__) so a caller catching session
# refusals can catch both classes from one module: this module refuses on
# identity/shape, `session_git` refuses on git discipline (a stage-everything
# spelling, a path escaping the worktree, an immovable served checkout).
from .session_git import (GitError, SessionActionInProgress, SessionGit,
                          SessionGitRefused)

# Scope kinds, exactly as the tile transports spell them.
STAGED_TOPIC = "staged-topic"
CLUSTER = "cluster"
POSSIBLE = "possible"
SCOPE_KINDS = (STAGED_TOPIC, CLUSTER, POSSIBLE)

# The branch namespace per scope kind. A staged topic is `draft/` (the ratified
# spelling); every other scope uses its own kind as the namespace, so a cluster
# and a staged topic sharing an id can never collide.
STAGED_TOPIC_NAMESPACE = "draft"

# Worktrees live one level below the container root because Speckit's own
# feature worktrees use the SAME root (`.specify/extensions/git/git-config.yml`
# -> `worktree_root: ../codexFactory-worktrees`), and because a branch name
# containing `/` cannot be a directory name unflattened (research R7).
SESSIONS_SUBDIR = "sessions"
CONTAINER_SUFFIX = "-worktrees"
PATH_SEPARATOR = "__"

# A session's DERIVED snapshot: a sibling of `sessions/` inside the container,
# deliberately NOT inside the worktree and NOT under `sessions/` — see
# `snapshots_root` for both reasons.
SNAPSHOTS_SUBDIR = "session-snapshots"
SNAPSHOT_SUFFIX = ".snapshot.json"

# The branch namespaces a session can live in — the prefixes the bootstrap scans
# for a branch that has no worktree (FR-008, T033a).
SESSION_NAMESPACES = (STAGED_TOPIC_NAMESPACE, CLUSTER, POSSIBLE)

NOTEBOOK_PREFIX = "xf-session-"
# The KEY half of a session notebook alias (FR-037, spec C11): the
# separator and the digest width, named once so the alias and every
# reader of it agree. `-k` is unambiguous within the alias because the
# digest is ALWAYS the last segment, however many `-k…` runs the readable
# half happens to contain.
NOTEBOOK_KEY_SEPARATOR = "-k"
NOTEBOOK_KEY_DIGEST_CHARS = 12
DRAFT_BRANCH_PREFIX = STAGED_TOPIC_NAMESPACE + "/"

# The base a fresh session branch forks from: the served checkout's shared truth.
DEFAULT_BASE = "main"
# The remote name a refusal SPELLS when it has to name the human's own pull
# command (critic finding C5). The real one is read from the git seam
# (`SessionGit.remote`); this is only the fallback for a seam that declares none,
# and nothing here invokes a remote operation.
DEFAULT_REMOTE = "origin"

# FR-007: verbs whose effect reaches OUTSIDE the branch. A session branch is
# UNMERGED exploration, so anything that acts on the wider world from inside one
# would be acting on work no gate has accepted — the refusal is at the session
# ENTRY POINT, before a branch or a worktree exists, so a refused dispatch leaves
# nothing behind.
#
# `kickoff` and `propose` are real routes today: both write a workflow-job
# descriptor that commissions work OUTSIDE this repository's branch. (`propose`
# additionally carries FR-023's own live-session refusal, which is a different
# rule read from the other direction: FR-023 refuses `propose` because a session
# holds the tile; FR-007 refuses it because a session cannot dispatch.)
# `publish`, `build`, `rollout`, and `release` have NO route in this codebase —
# they are listed because FR-007 names them, so that adding one later cannot
# quietly acquire session authority it was never granted.
EXTERNALLY_DISPATCHING_VERBS = ("kickoff", "propose", "publish", "build",
                                "rollout", "release")

# The ratified ordinal spelling: `-2`, `-3`, … with NO leading zero. `-02` is
# not the spelling, so it is not read as an ordinal.
_ORDINAL_RE = re.compile(r"^-([1-9][0-9]*)$")
_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
# The action stamp's own shape — `gate_console._stamp` of an ISO date-TIME, which
# is what every production `at` is. Pinned here because a commit artifact's
# reference IS the stamp (`commit_artifact`), so a stamp that is not this shape is
# a reference the introduced-by rule cannot resolve (FR-006; tail finding B1).
_ACTION_STAMP_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z$")

# FR-025's two continuations, and the ONLY two. The human ANSWERS the
# resume-or-new report with one of these tokens — the HTTP body's `continuation`
# field and the CLI's `--continuation` flag are both spelled from here, so the
# refusal that offers the choice can name the exact answer it accepts.
CONTINUATION_RESUME = "resume"
CONTINUATION_NEW = "new"
CONTINUATIONS = (CONTINUATION_RESUME, CONTINUATION_NEW)

# What a teardown removed (FR-021). Reported in THIS order and only for what was
# actually torn down: a response that claimed a notebook nobody asked it to retire
# would be an audit entry that lies.
TORN_WORKTREE = "worktree"
TORN_REGISTRY_ENTRY = "registry-entry"
TORN_NOTEBOOK = "notebook"
TEARDOWN_STEPS = (TORN_WORKTREE, TORN_REGISTRY_ENTRY, TORN_NOTEBOOK)


class SessionRefused(Exception):
    """A structural session refusal: an illegal derived name, a path escaping
    the container, a split write. Raised before anything is persisted."""

    def report(self) -> str:
        """The refusal, as the human reads it. Named `report()` so a session
        refusal reads like a boundary refusal at every call site — "every
        refusal is reported, never silent" holds across the whole action layer
        (boundary.Refusal.report)."""
        return str(self)


class CrossTileCollision(SessionRefused):
    """A tile's deterministic branch name is ALSO another existing tile's
    ordinal form (`draft/<t>-2` is tile `<t>-2`'s first branch and tile `<t>`'s
    second). The branch cannot be attributed to one tile, so opening refuses and
    NAMES BOTH TILES rather than silently joining the other tile's session
    (FR-002, FR-026, G12)."""

    def __init__(self, tile: "Tile", other: "Tile", branch: str, *,
                 note: str | None = None) -> None:
        self.tile = tile
        self.other = other
        self.branch = branch
        super().__init__(
            f"branch {branch!r} is both the deterministic session branch of tile "
            f"{tile.scope_id!r} ({tile.scope_kind}) and tile {other.scope_id!r} "
            f"({other.scope_kind})'s ordinal-"
            f"{ordinal_of(branch, other.branch)} session branch. Refusing rather "
            "than joining another tile's session: resolve it by abandoning and "
            "cleaning up the other tile's session branch, or by renaming one "
            "tile (FR-002, FR-026)" + (f". {note}" if note else ""))


class AbandonedBranchSurvives(SessionRefused):
    """The tile's branch EXISTS but has no worktree — the shape an abandoned
    session leaves behind (FR-022 deletes nothing at abandon time). FR-025
    forbids choosing silently, so opening refuses here and NAMES both
    continuations; this IS the offered resume-or-new choice (T056), which is why
    the message reads like the prompt and names the exact answers it accepts.

    The refusal is the whole mechanism: there is no prompt STATE anywhere, so a
    session still persists no descriptor (D10) and two concurrent writers cannot
    answer two different halves of one stored question — each write either JOINs a
    live session (FR-027) or gets this report again."""

    def __init__(self, branch: str, ordinal_hint: str | None = None, *,
                 family: Sequence[str] = (),
                 remote_only: Sequence[str] = ()) -> None:
        self.branch = branch
        self.ordinal_hint = ordinal_hint
        # The tile's WHOLE surviving family, over the union of remote and local
        # refs (FR-026; PR #49 review finding 7). Naming only the base hid an
        # ordinal session's work from the human being asked to choose, and saying
        # nothing about a remote-only branch hid the ONE fact that decides which
        # continuation is even available here.
        self.family = tuple(family or (branch,))
        self.remote_only = tuple(remote_only)
        nxt = f" (the NEW branch would be {ordinal_hint!r})" if ordinal_hint else ""
        others = tuple(b for b in self.family if b != branch)
        also = (f" The tile's other surviving branches are "
                f"{', '.join(repr(b) for b in others)}; RESUME takes the most "
                f"recent one." if others else "")
        # The fetch instruction carries its REFSPEC. Without one, `git fetch
        # origin <branch>` creates no local branch and the RESUME that follows
        # refuses identically — the remedy read as if it worked (PR #234, Codex).
        fetch_hint = "; ".join(
            f"`git fetch origin refs/heads/{b}:refs/heads/{b}`"
            for b in self.remote_only)
        remote = (f" NOTE: {', '.join(repr(b) for b in self.remote_only)} "
                  f"{'exists' if len(self.remote_only) == 1 else 'exist'} ONLY on "
                  "the remote (read with `git ls-remote --heads`; no session "
                  "operation fetches, FR-026/D17) — fetch it yourself, WITH THE "
                  f"DESTINATION REFSPEC ({fetch_hint}), to RESUME it, or start a "
                  "NEW ordinal beside it."
                  if self.remote_only else "")
        answer = (f" Answer with continuation={CONTINUATION_RESUME!r} or "
                  f"continuation={CONTINUATION_NEW!r}.")
        super().__init__(
            f"branch {branch!r} survives with no worktree, which is what an "
            "ABANDONED session leaves behind — a session is not opened over it "
            "silently (FR-025). Two continuations exist and the choice is the "
            f"human's: RESUME {branch!r} under its existing name, or start a NEW "
            f"session at the next ordinal{nxt}." + also + remote + answer)


class LiveSessionRefused(SessionRefused):
    """FR-023: an externally-committing verb (`propose`) was invoked while a live
    branch session holds the tile. Keyed on the session's REGISTRY ENTRY and never
    on branch existence — a branch surviving an abandon does NOT block (D15)."""


class StaleSessionWorktree(SessionRefused):
    """A worktree directory with NO branch. The joint signal fails, so this is
    NOT a live session (FR-008, D10) — it is crash residue, surfaced for the
    human-invoked cleanup rather than adopted or silently overwritten."""

    def __init__(self, path: Path, branch: str) -> None:
        self.path = Path(path)
        self.branch = branch
        super().__init__(
            f"the sessions container holds {self.path} but branch {branch!r} does "
            "not exist. A worktree and its branch are a JOINT signal: either "
            "alone is NOT a live session (FR-008, D10), so this is stale residue "
            "— remove the directory (and `git worktree prune`) before opening a "
            "session on this tile.")


class DispatchNotRecorded(SessionRefused):
    """The pending-dispatch marker for an OPEN pull request could not be written,
    so nothing durable holds its URL (FR-029; PR #49 review finding 4, wave 2).

    NOT raised to the human as-is: `open-pr` catches it, because a marker is a
    RECOVERY AID and must never be the reason a pull request the human already has
    cannot be recorded. It exists so the failure is not silent — the caller reports
    the truth instead of promising a marker that is not there — and so the values
    the lost record needs travel with it.

    `url`, `at` and `actor` are exactly the FR-029 record's content. When the marker
    write fails and the record write then fails too, that record cannot be
    reconstructed from anything on disk, so the refusal text becomes its only
    copy and has to carry all three."""

    def __init__(self, branch: str, path: Path, reason: str, *, url: str,
                 at: str, actor: str) -> None:
        self.branch = branch
        self.path = Path(path)
        self.reason = reason
        self.url = url
        self.at = at
        self.actor = actor
        super().__init__(
            f"the pending-dispatch marker for {branch!r} could not be written to "
            f"{self.path} ({reason}), so nothing durable holds the pull request "
            f"{url} until its FR-029 record lands")


class EndingNotDurable(SessionRefused):
    """The session's ENDING could not be made durable, so it does not happen.

    An ending is only real if a later process can see it (FR-021, FR-008): the
    registry entry it drops is in-process, so the ONLY thing that survives a
    restart is the ending marker. `write_ending_marker` used to swallow `OSError`
    and return None while the teardown proceeded and reported an ending anyway —
    and the failure is CORRELATED with the one that leaves residue, because an
    unwritable container is also what makes `git worktree remove` fail. The
    reproduced result: the ended session came back LIVE on the next process start,
    a later write JOINED it, and the response said the opposite (PR #49 review
    finding 6, wave 2).

    Raised BEFORE anything is torn down, which is what makes it a refusal rather
    than a report: the session is still live, still joinable, and unchanged."""

    def __init__(self, branch: str, path: Path, reason: str) -> None:
        self.branch = branch
        self.path = Path(path)
        self.reason = reason
        super().__init__(
            f"refusing to end the session on {branch!r}: its ending cannot be made "
            f"DURABLE. The marker at {self.path} could not be written ({reason}), "
            "and a session's liveness registry entry is in-process — the marker is "
            "the ONLY thing a later process can read the ending from (FR-021, "
            "FR-008). Ending anyway would tear the worktree down while a restart "
            "re-derived the session as LIVE and let a later gate write JOIN it, "
            "with this response claiming it had ended. NOTHING was torn down: the "
            "session is still live and still joinable. Make the container "
            f"({self.path.parent}) writable — check the filesystem's permissions "
            "and free space — and run the ending again.")


class SessionWorktreeDrifted(SessionRefused):
    """The session's worktree no longer HOLDS the session's branch — so a write
    made here would land somewhere else (FR-006, FR-008, G13; SC-003).

    Distinct from `StaleSessionWorktree`, whose story is "the branch does not
    exist". Here both halves exist and DISAGREE, which is the harm the joint
    signal is for: the worktree was moved onto another branch by a human's shell,
    or left detached by an interrupted rebase/bisect, or its git association was
    pruned. The registry entry a long-lived serve holds cannot see any of that —
    it recorded the pairing once, at open, and nothing revokes it (PR #49 review
    finding 5, wave 2).

    `kind` is the bootstrap's own vocabulary for the same three conditions
    (`WORKTREE_ON_ANOTHER_BRANCH` / `WORKTREE_DETACHED` /
    `WORKTREE_UNKNOWN_TO_GIT`), so the live path and the re-derivation name a
    drift identically. Nothing is deleted and nothing is moved back: putting the
    human's own checkout back is the human's call."""

    def __init__(self, path: Path, branch: str, *, kind: str,
                 held: str | None = None, during: str = "a session write") -> None:
        self.path = Path(path)
        self.branch = branch
        self.kind = kind
        self.held = held
        self.during = during
        if kind == WORKTREE_ON_ANOTHER_BRANCH:
            found = f"git lists it on {held!r} instead"
            remedy = (f"`git -C {self.path} checkout {branch}` puts it back "
                      "(commit or stash the other branch's work first)")
        elif kind == WORKTREE_DETACHED:
            found = "git lists it as DETACHED, holding no branch at all"
            remedy = (f"finish or abort the rebase/bisect, then `git -C "
                      f"{self.path} checkout {branch}`")
        else:
            found = "git does not list that directory as a worktree at all"
            remedy = ("`git worktree prune` and re-open the session; the "
                      "directory is residue, not a session")
        super().__init__(
            f"refusing {during}: the session on {branch!r} expects its worktree "
            f"at {self.path} to hold that branch, and {found}. A worktree and its "
            "branch are a JOINT signal (FR-008, G13) and the write would land on "
            f"whatever the directory holds, ORPHANING it from {branch!r} while the "
            "record still attested to it — so this refuses instead. Nothing was "
            f"written. Remedy: {remedy}.")


class EndedSessionResidue(SessionRefused):
    """The session on this branch ALREADY ENDED (FR-021) and its teardown could
    not finish, so the worktree and the branch are both still there.

    Directory + branch is the shape a LIVE session has, which is why a contained
    `git worktree remove` failure used to come back live on the next process start
    and let a later gate write JOIN a session the human had ended (PR #49 review
    finding 6). The durable ending marker is what tells the two apart; this is the
    refusal that keeps the ending decided."""

    def __init__(self, path: Path, branch: str, ending: str,
                 residue: Sequence[str] = ()) -> None:
        self.path = Path(path)
        self.branch = branch
        self.ending = ending
        super().__init__(
            f"the session on {branch!r} already ENDED ({ending}) and its teardown "
            f"could not finish: {'; '.join(residue) or 'residue remains'}. A "
            "session ends ONCE (FR-021), so this worktree is residue and is NOT "
            f"joined however live it looks — remove {self.path}, run "
            "`git worktree prune`, and delete the branch if the ending was a MERGE "
            "(FR-033). The tile opens a NEW session afterwards.")


def _refuse_ended_session_residue(checkout_root: Path | str, branch: str,
                                  worktree: Path) -> None:
    marker = read_ending_marker(checkout_root, branch)
    if marker:
        raise EndedSessionResidue(worktree, branch,
                                  str(marker.get("ending") or "ending"),
                                  tuple(marker.get("residue") or ()))


class ExternalDispatchRefused(SessionRefused):
    """FR-007: a verb whose effect reaches OUTSIDE the branch, invoked from
    inside a session."""


class LiveProposalRefused(SessionRefused):
    """FR-024: the tile carries a live proposal, or a `propose` dispatch is
    still in flight. Two distinct messages, because naming `demote` when nothing
    has landed names a route the human cannot take (D20)."""


class NoActiveSession(SessionRefused):
    """A SESSION-ONLY verb reached a tile with no LIVE session (FR-016).

    Raised by `open_session(require_live=True)`, which is how a verb says "join
    the session or refuse — never open one". `edit-document` is the first such
    verb and Phase 6/7's `abandon-session` / `open-pr` are the others: each of
    them acts on a session that must already exist, and a verb that opened one to
    satisfy itself would become a second way to START work, deciding the tile's
    one-session-at-a-time rule by whoever typed first.

    `remedy` is the CALLER's sentence, because the route knows what the human
    should do instead and this module does not: `edit-document` names `edit-apply`
    (the main-resident redline path), while `abandon-session` has nothing to
    abandon and `open-pr` has nothing to save."""

    def __init__(self, tile: "Tile", branch: str, *, verb: str | None = None,
                 remedy: str | None = None) -> None:
        self.tile = tile
        self.branch = branch
        self.verb = verb
        subject = f"{verb!r} is valid ONLY inside an active branch session: " \
            if verb else ""
        tail = f" {remedy}" if remedy else ""
        super().__init__(
            f"{subject}no branch session is live on tile {tile.scope_id!r} "
            f"({tile.scope_kind}), whose session branch would be {branch!r}. "
            "Liveness is the session's registry entry, so a surviving branch or "
            "worktree directory is NOT a live session (FR-008, D15)." + tail)


# --------------------------------------------------------------------------
# identity derivations (FR-002, FR-037; T008)
# --------------------------------------------------------------------------

def reduce_scope_id(scope_id: str) -> str:
    """A colon-qualified corpus staging id -> its final segment
    (`openxFactory:staging:demo-topic` -> `demo-topic`).

    `git check-ref-format refs/heads/draft/openxFactory:staging:demo-topic`
    FAILS — `:` is disallowed in a ref name — while the dashboard's own
    identifier for the same tile is the staging FOLDER name, which is
    ref-legal. Reduction is therefore the rule, not a convenience (research R2,
    FR-002, spec C1)."""
    return str(scope_id or "").strip().rsplit(":", 1)[-1].strip()


def branch_namespace(scope_kind: str) -> str:
    if scope_kind == STAGED_TOPIC:
        return STAGED_TOPIC_NAMESPACE
    if scope_kind in (CLUSTER, POSSIBLE):
        return scope_kind
    raise SessionRefused(
        f"unknown scope kind {scope_kind!r}; a session opens on a tile whose "
        f"scope is one of {SCOPE_KINDS}")


def looks_ref_legal(branch: str) -> bool:
    """A conservative PURE pre-check, so an illegal derived name is refused
    before any subprocess runs. `git check-ref-format` remains the authority —
    `SessionGit.require_legal_ref` asks it before every git call (data-model
    validation rules)."""
    if not branch or branch != branch.strip():
        return False
    if branch.startswith("-") or branch.startswith("/") or branch.endswith("/"):
        return False
    if branch.endswith(".") or branch.endswith(".lock"):
        return False
    if ".." in branch or "//" in branch or "@{" in branch:
        return False
    if any(part in ("", ".") or part.endswith(".lock") for part in branch.split("/")):
        return False
    return re.fullmatch(r"[A-Za-z0-9._/-]+", branch) is not None


def session_branch(scope_kind: str, scope_id: str, *,
                   ordinal: int | None = None) -> str:
    """The tile's deterministic session branch — derived from the TILE's scope
    identity and NEVER from the actor (FR-002), so a second writer joins the
    same branch instead of opening a second session (FR-003).

    `ordinal` is D17's NEW continuation only: ordinal 1 IS the bare name, so an
    explicit 1 (or 0, or a negative, or a string) is a caller error rather than
    a silently accepted alias."""
    namespace = branch_namespace(scope_kind)
    reduced = reduce_scope_id(scope_id)
    if not reduced:
        raise SessionRefused(
            f"scope id {scope_id!r} reduces to nothing; a session branch needs a "
            "tile identity (FR-002)")
    if "/" in reduced:
        raise SessionRefused(
            f"scope id {reduced!r} is not a single path segment; a tile id is a "
            "staging FOLDER name, a `cl-*`, or a `pos-*` — never a path, so a "
            "crafted id cannot open a branch in another namespace (FR-002)")
    branch = f"{namespace}/{reduced}"
    if ordinal is not None:
        if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 2:
            raise SessionRefused(
                f"ordinal {ordinal!r} is not a session ordinal; the ratified "
                "spelling is -2, -3, … and ordinal 1 is the bare branch name "
                "(FR-025, FR-026)")
        branch = f"{branch}-{ordinal}"
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"derived branch {branch!r} is not a legal git ref; a colon-qualified "
            "staging id reduces to its final segment and nothing else is "
            "rewritten (FR-002, research R2)")
    return branch


def container_root(checkout_root: Path | str) -> Path:
    """`<repo-parent>/<repo>-worktrees/` — ALREADY gitignored by the aggregation
    repo's `*-worktrees/` and already excluded from the notebook scan, so this
    placement owes no new ignore entry (FR-005, research R7)."""
    root = Path(checkout_root).resolve()
    return root.parent / f"{root.name}{CONTAINER_SUFFIX}"


def sessions_root(checkout_root: Path | str) -> Path:
    return container_root(checkout_root) / SESSIONS_SUBDIR


def flatten_branch(branch: str) -> str:
    return branch.replace("/", PATH_SEPARATOR)


def worktree_path(checkout_root: Path | str, branch: str) -> Path:
    """The session worktree directory. A path that would escape the container is
    a REFUSAL, not a fallback (data-model validation rules)."""
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"refusing to derive a worktree path for {branch!r}: it is not a "
            "legal git ref, so it is not a session branch")
    root = sessions_root(checkout_root)
    candidate = (root / flatten_branch(branch)).resolve()
    if candidate == root.resolve() or root.resolve() not in candidate.parents:
        raise SessionRefused(
            f"worktree path for {branch!r} would resolve outside the sessions "
            f"container {root} (FR-005)")
    return root / flatten_branch(branch)


def snapshots_root(checkout_root: Path | str) -> Path:
    """Where a session's DERIVED snapshot lives: `<container>/session-snapshots/`.

    NOT inside the worktree, for two reasons that are both defects if ignored: a
    derived artifact in the worktree would appear in that branch's `git status`
    (which the split-write guard reads as a dirty path), and it would be one
    careless stage away from being committed onto a branch whose entire purpose is
    reviewable authored content. NOT under `sessions/` either, because the T033a
    bootstrap scans that directory for worktrees and a snapshot directory there
    would look like one. The container itself is already gitignored and already
    excluded from the notebook scan (plan Constraint 12), so this placement owes
    no new ignore entry."""
    return container_root(checkout_root) / SNAPSHOTS_SUBDIR


def session_snapshot_path(checkout_root: Path | str, branch: str) -> Path:
    """The session snapshot file for `branch` — flattened exactly like its
    worktree, so the two are obviously the same session on sight."""
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"refusing to derive a snapshot path for {branch!r}: it is not a legal "
            "git ref, so it is not a session branch")
    return snapshots_root(checkout_root) / f"{flatten_branch(branch)}{SNAPSHOT_SUFFIX}"


# --------------------------------------------------------------------------
# the PENDING-DISPATCH marker (FR-029; PR #49 review finding 4)
# --------------------------------------------------------------------------

# Where an `open-pr` that has already pushed and opened its pull request, but has
# not yet written its main-resident record, leaves the URL. A sibling of
# `session-snapshots/` inside the container, for the same two reasons: it is
# DERIVED operational state rather than a governed artifact (so it may not enter
# the gate-records tree the validators own), and the container is already
# gitignored and already excluded from the notebook scan. It outlives the branch,
# which is the whole point — the merge deletes the branch.
DISPATCH_SUBDIR = "session-dispatch"
DISPATCH_SUFFIX = ".dispatch.json"


def dispatch_marker_path(checkout_root: Path | str, branch: str) -> Path:
    """The pending-dispatch marker file for `branch`, flattened exactly like its
    worktree so the two are obviously the same session on sight."""
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"refusing to derive a dispatch marker path for {branch!r}: it is not "
            "a legal git ref, so it is not a session branch")
    return (container_root(checkout_root) / DISPATCH_SUBDIR
            / f"{flatten_branch(branch)}{DISPATCH_SUFFIX}")


def write_dispatch_marker(checkout_root: Path | str, branch: str, *, url: str,
                          at: str, actor: str) -> Path | None:
    """Record that the pull request for `branch` EXISTS but its FR-029 record
    does not yet (PR #49 review finding 4).

    FR-029 mandates the order push → open-or-update → write the record, so there
    is a window in which the remote write has happened and the durable audit has
    not. That window used to be invisible: a record write that failed returned a
    409 "refused" while the pull request was open, and if the branch then MERGED
    the reconciliation deleted it while the response asserted the record "stays on
    `main` and outlives the branch". The marker makes the window recoverable —
    the merge ending finalizes the missing record from it.

    A marker that cannot be written must never be the reason a pull request the
    human already has cannot be recorded, so the CALLER contains this failure and
    carries on to the record write. But it must not be SILENT (PR #49 review
    finding 4, wave 2): returning None by construction meant `open-pr`'s refusal
    text promised, unconditionally, that "a pending-dispatch marker holds the URL
    meanwhile, so if the pull request merges first the ending finalizes the record
    from it" — over a marker that did not exist. The FR-029 record was then
    permanently lost AND the human was told the opposite, which is the worse half:
    a reader who trusts that sentence stops looking for the record.

    So the failure RAISES `DispatchNotRecorded`, carrying the reason and everything
    the lost record needs, and `open-pr` reports what actually happened."""
    path = dispatch_marker_path(checkout_root, branch)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "branch": branch, "url": str(url), "at": str(at),
            "actor": str(actor)}, sort_keys=True) + "\n", encoding="utf-8")
    except OSError as exc:
        raise DispatchNotRecorded(branch, path, str(exc), url=str(url),
                                  at=str(at), actor=str(actor)) from exc
    return path


def read_dispatch_marker(checkout_root: Path | str, branch: str) -> dict | None:
    """The pending dispatch for `branch`, or None. An unreadable or unparseable
    marker is None: it can only ever ADD a record that would otherwise be missing,
    so a broken one must degrade to the pre-marker behaviour."""
    try:
        raw = dispatch_marker_path(checkout_root, branch).read_text(encoding="utf-8")
    except (OSError, SessionRefused):
        return None
    try:
        loaded = json.loads(raw)
    except ValueError:                               # pragma: no cover - defensive
        return None
    return loaded if isinstance(loaded, dict) and loaded.get("url") else None


def clear_dispatch_marker(checkout_root: Path | str, branch: str) -> None:
    """Drop the marker — the record it stood in for now exists."""
    try:
        dispatch_marker_path(checkout_root, branch).unlink(missing_ok=True)
    except (OSError, SessionRefused):                # pragma: no cover - defensive
        return


# --------------------------------------------------------------------------
# the ENDING marker (FR-021; PR #49 review finding 6)
# --------------------------------------------------------------------------

# Where an ending that could NOT finish says so. A sibling of `session-snapshots/`
# and `session-dispatch/` inside the already-gitignored container, for the same
# reason: it is DERIVED operational state, not a governed artifact and not a
# session descriptor (D10) — the governed audit of an abandon is still its
# MAIN-RESIDENT record, and of a merge its `open-pr` record.
ENDING_SUBDIR = "session-ended"
ENDING_SUFFIX = ".ended.json"

# The two endings (FR-021), as the marker spells them. Pinned as constants because
# FR-028's cleanup now READS the word — an `abandon` is what makes a surviving
# branch deletable, and a `merge` never is (PR #49 second-review finding 3).
ENDING_ABANDON = "abandon"
ENDING_MERGE = "merge"


def ending_marker_path(checkout_root: Path | str, branch: str) -> Path:
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"refusing to derive an ending marker path for {branch!r}: it is not "
            "a legal git ref, so it is not a session branch")
    return (container_root(checkout_root) / ENDING_SUBDIR
            / f"{flatten_branch(branch)}{ENDING_SUFFIX}")


def write_ending_marker(checkout_root: Path | str, branch: str, *, ending: str,
                        residue: Sequence[str] = ()) -> Path:
    """Record that this session ENDED and left residue behind (finding 6).

    `teardown_session` drops the registry entry FIRST — correct, because liveness
    IS the entry and a later step failing must not leave a live entry pointing at
    a worktree that is gone — and CONTAINS every later failure into `notes`. The
    consequence nobody wrote down: when `git worktree remove` cannot run (a
    `git worktree lock`, a read-only container, an in-use directory, an NFS or
    permission failure — no Python injection needed), the residue is DIRECTORY +
    BRANCH, which is EXACTLY the shape the FR-008 bootstrap read as LIVE. A fresh
    process brought the ended session back: `propose` was re-blocked and the next
    gate write JOINED a session the human had ended. On the MERGE ending it is
    worse — with the worktree still attached `git branch -D` refuses too, so
    FR-033's mandatory deletion silently did not happen and a MERGED session came
    back live. Phase 6 realization note 4's rationale ("residue the T033a bootstrap
    already reports as stale with its own remedy") was factually wrong for BOTH
    endings; this marker is what makes it true.

    NOT best-effort any more (PR #49 review finding 6, wave 2). It used to swallow
    `OSError` and return None while `teardown_session` proceeded regardless and
    appended a note asserting the ending "is recorded as ENDED for every later
    process". The replay pass reproduced the ORIGINAL harm verbatim through the
    CORRELATED failure — an unwritable container is the same root cause that makes
    `git worktree remove` fail — and the ended session came back LIVE on the next
    process start while a later write JOINED it, with the note attesting the
    opposite. A best-effort write cannot carry an ending guarantee, and a note that
    says it did is a false attestation.

    So this RAISES `EndingNotDurable`, and the endings go through
    `reserve_ending_marker` — before they destroy anything."""
    path = ending_marker_path(checkout_root, branch)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "branch": branch, "ending": str(ending),
            "residue": [str(item) for item in residue]}, sort_keys=True) + "\n",
            encoding="utf-8")
    except OSError as exc:
        raise EndingNotDurable(branch, path, str(exc)) from exc
    return path


def reserve_ending_marker(checkout_root: Path | str, branch: str, *,
                          ending: str) -> Path:
    """Establish the ending's DURABILITY before the ending destroys anything.

    The ordering IS the fix (finding 6, wave 2). `teardown_session` drops the
    registry entry first and CONTAINS every later failure, so by the time the
    residue is known the session is already non-live in this process and there is
    nothing left to refuse with: raising then would report a half-done ending, and
    swallowing is what resurrected it. Writing the marker FIRST inverts that — if
    the container cannot hold the ending, nothing has been torn down yet, so the
    ending is REFUSED, the session stays live exactly as it was, and the human gets
    the unwritable path and a remedy.

    It also breaks the correlation the replay pass exploited: the condition that
    makes `git worktree remove` fail (a read-only or full container) is usually the
    same condition that makes the marker unwritable, so testing the marker only
    AFTER the removal failed was testing it precisely in the world where it fails
    too.

    The reservation records `residue: []` — "this session ended; what its cleanup
    left behind is not known yet". Every later write only ADDS information: a clean
    teardown clears the marker, a teardown with residue rewrites it with the
    detail. Both may therefore be best-effort, because the ENDING is already
    durable and `read_ending_marker` already answers "ended".

    A process that dies mid-teardown leaves the reservation, which reads as ENDED.
    Deliberate: an ending the human commanded, whose cleanup may be half-done, must
    fail CLOSED. `EndedSessionResidue` names the cleanup, and every path that
    materializes a worktree again clears the marker, so a RESUME is never mistaken
    for the ending it grew out of."""
    return write_ending_marker(checkout_root, branch, ending=ending, residue=())


def read_ending_marker(checkout_root: Path | str, branch: str) -> dict | None:
    """The ending this branch's session already had, or None."""
    try:
        raw = ending_marker_path(checkout_root, branch).read_text(encoding="utf-8")
    except (OSError, SessionRefused):
        return None
    try:
        loaded = json.loads(raw)
    except ValueError:                               # pragma: no cover - defensive
        return None
    return loaded if isinstance(loaded, dict) else None


def clear_ending_marker(checkout_root: Path | str, branch: str) -> None:
    """Drop the marker: this branch has a worktree again (a RESUME, FR-025) or the
    residue is gone. Cleared by every path that materializes a worktree, so a
    resumed session is never mistaken for the ended one it grew out of."""
    try:
        ending_marker_path(checkout_root, branch).unlink(missing_ok=True)
    except (OSError, SessionRefused):                # pragma: no cover - defensive
        return


# --------------------------------------------------------------------------
# the SESSION-OWNER marker (FR-008, G12; PR #49 second-review finding 6)
# --------------------------------------------------------------------------

# WHICH TILE opened the session on a branch. A sibling of `session-snapshots/`,
# `session-dispatch/` and `session-ended/` inside the already-gitignored container,
# for the same reason all three are there: it is DERIVED OPERATIONAL STATE, not a
# governed artifact and not a session descriptor (D10) — liveness is still the
# registry entry and nothing else, and this file cannot make a dead session live.
#
# It exists because ownership is NOT derivable from the ref. `draft/<t>-2` is tile
# `<t>-2`'s first session and tile `<t>`'s second, and the FR-008 bootstrap
# re-derives entries from WORKTREES, which name a branch and never a tile. So after
# a restart — every CLI-parity verb is a restart — a tile's own ordinal session was
# read as the sibling tile's and silently vanished, and the next write forked the
# tile into two live sessions (finding 6, reproduced). The OPEN knows the answer;
# this is where it leaves it for the next process.
#
# ADVISORY, and deliberately so: a marker that cannot be written must never be the
# reason a session cannot open, so the write is contained and its absence degrades
# to FR-026's documented tie-break — the pre-existing behaviour — rather than to a
# failure.
OWNER_SUBDIR = "session-owner"
OWNER_SUFFIX = ".owner.json"


def owner_marker_path(checkout_root: Path | str, branch: str) -> Path:
    if not looks_ref_legal(branch):
        raise SessionRefused(
            f"refusing to derive a session-owner path for {branch!r}: it is not a "
            "legal git ref, so it is not a session branch")
    return (container_root(checkout_root) / OWNER_SUBDIR
            / f"{flatten_branch(branch)}{OWNER_SUFFIX}")


def write_owner_marker(checkout_root: Path | str, branch: str,
                       tile: "Tile",
                       base: tuple[str, str] | None = None,
                       base_aliases: tuple[str, ...] = ()) -> Path | None:
    """Record WHICH TILE this session belongs to — and, when the OPEN knew it,
    WHAT the session branched from as `(base_ref, base_revision)` plus the
    base's other recorded revision spellings (T104 R-12 / W-4: the durable
    half of the entry's `session_base`/`session_base_aliases`, read back by
    the next process's bootstrap). Contained: returns None when it could not
    be written (see the note above)."""
    try:
        path = owner_marker_path(checkout_root, branch)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"branch": branch, "scope_kind": str(tile.scope_kind),
                   "scope_id": str(tile.scope_id)}
        if base:
            payload["base_ref"] = str(base[0])
            payload["base_revision"] = str(base[1])
            if base_aliases:
                payload["base_revision_aliases"] = [str(a) for a in base_aliases]
        path.write_text(json.dumps(payload, sort_keys=True) + "\n",
                        encoding="utf-8")
        return path
    except (OSError, SessionRefused):
        return None


def read_owner_marker(checkout_root: Path | str, branch: str
                      ) -> tuple[str, str] | None:
    """The `(scope_kind, scope_id)` this branch's session belongs to, or None.

    The marker's own `branch` is verified: `flatten_branch` is not injective
    (`draft/foo__bar` and `draft/foo/bar` share a directory name — finding 5), and
    attributing one session's owner to another's branch is the very mistake this
    file exists to prevent."""
    try:
        raw = owner_marker_path(checkout_root, branch).read_text(encoding="utf-8")
    except (OSError, SessionRefused):
        return None
    try:
        loaded = json.loads(raw)
    except ValueError:                               # pragma: no cover - defensive
        return None
    if not isinstance(loaded, dict) or loaded.get("branch") != branch:
        return None
    kind, scope = loaded.get("scope_kind"), loaded.get("scope_id")
    if kind in SCOPE_KINDS and scope:
        return (str(kind), str(scope))
    return None


def read_base_marker(checkout_root: Path | str, branch: str
                     ) -> tuple[str, str] | None:
    """The `(base_ref, base_revision)` this branch's session was opened from,
    or None — same file, same branch verification, and the same advisory
    posture as `read_owner_marker`: a marker written before this wave (no
    base keys) reads as None and degrades to the original binding shape."""
    try:
        raw = owner_marker_path(checkout_root, branch).read_text(encoding="utf-8")
    except (OSError, SessionRefused):
        return None
    try:
        loaded = json.loads(raw)
    except ValueError:                               # pragma: no cover - defensive
        return None
    if not isinstance(loaded, dict) or loaded.get("branch") != branch:
        return None
    base_ref, base_revision = loaded.get("base_ref"), loaded.get("base_revision")
    if isinstance(base_ref, str) and base_ref and \
            isinstance(base_revision, str) and base_revision:
        return (base_ref, base_revision)
    return None


def read_base_marker_aliases(checkout_root: Path | str, branch: str
                             ) -> tuple[str, ...]:
    """The base's other recorded revision spellings (W-4), or () — same file,
    same branch verification, same advisory posture as the readers above."""
    try:
        raw = owner_marker_path(checkout_root, branch).read_text(encoding="utf-8")
        loaded = json.loads(raw)
    except (OSError, SessionRefused, ValueError):
        return ()
    if not isinstance(loaded, dict) or loaded.get("branch") != branch:
        return ()
    aliases = loaded.get("base_revision_aliases")
    if isinstance(aliases, list):
        return tuple(str(a) for a in aliases if isinstance(a, str) and a)
    return ()


def clear_owner_marker(checkout_root: Path | str, branch: str) -> None:
    """Drop it: this session is over (both endings). The branch may survive an
    abandon, and a RESUME writes the marker again from the tile that resumes."""
    try:
        owner_marker_path(checkout_root, branch).unlink(missing_ok=True)
    except (OSError, SessionRefused):                # pragma: no cover - defensive
        return


def branch_from_worktree_dir(path: Path | str) -> str:
    """The inverse of the flattening — the DISPLAY name for a worktree directory
    whose real branch git could not be asked for.

    NOT a session identity derivation any more (PR #49 review finding 5). The
    transform is not injective: `flatten_branch` maps both `draft/foo__bar` and
    `draft/foo/bar` to the directory `draft__foo__bar`, and both spellings pass
    `looks_ref_legal` AND `git check-ref-format`, so a staging folder literally
    named `foo__bar` made the bootstrap emit TWO contradictory stale rows for one
    live session and told the human to delete its worktree. The bootstrap now
    reads the branch off git's own porcelain and compares the directory to
    `flatten_branch(that branch)` — the forward direction, which IS a function."""
    return Path(path).name.replace(PATH_SEPARATOR, "/")


def notebook_key_digest(repository: str, branch: str) -> str:
    """The KEY half of the alias: a short digest of the exact (repository,
    branch) pair (FR-037, spec C11; PR #49 review finding 11).

    The pair is canonicalised with a `\\n` separator, which is legal in NEITHER
    half — `git check-ref-format` rejects a control character in a ref and a
    repository name is a directory name — so distinct keys always produce
    distinct payloads. Every other candidate separator is ref-legal (`_`, `.`,
    `-`, `/` all pass `looks_ref_legal`), which is precisely why the readable
    half cannot carry the guarantee on its own."""
    payload = f"{repository}\n{branch}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:NOTEBOOK_KEY_DIGEST_CHARS]


def notebook_alias_stem(repository: str, branch: str) -> str:
    """The READABLE half — FR-037's transform, verbatim and unchanged: strip a
    leading `draft/`, map every remaining `/` to `-`, lowercase the whole thing
    including the repository segment."""
    tail = str(branch or "")
    if tail.startswith(DRAFT_BRANCH_PREFIX):
        tail = tail[len(DRAFT_BRANCH_PREFIX):]
    tail = tail.replace("/", "-")
    if not str(repository or "").strip() or not tail.strip():
        raise SessionRefused(
            "a session notebook alias needs BOTH the repository and the branch — "
            "the alias is keyed on (repository, branch) (FR-037, C9)")
    return f"{NOTEBOOK_PREFIX}{repository}-{tail}".lower()


def notebook_alias(repository: str, branch: str) -> str:
    """`xf-session-<repository>-<transformed-branch>-k<key-digest>`
    (FR-037, spec C9 and C11).

    Two halves, and they answer two different questions. The READABLE half is
    FR-037's transform unchanged, so a human reading a NotebookLM title still
    sees which session it belongs to. The KEY half is what makes the derivation
    INJECTIVE, which the readable half is not and cannot be made to be.

    The transform is lossy in four independent ways, and PR #49 review finding 11
    reproduced all four over DISTINCT valid session keys:

      * stripping `draft/` erases the namespace, so `draft/cluster-cl-demo` and
        `cluster/cl-demo` collapse together — reachable with nothing but an
        unlucky staging FOLDER name, no privilege and no race;
      * lowercasing erases case, so `draft/Demo-Topic` and `draft/demo-topic` —
        two DIFFERENT tiles, since neither `reduce_scope_id` nor `Tile` case-folds
        — collapse together;
      * `/`→`-` and the `-` joining repository to branch are the same character,
        so `(openxFactory, draft/a-b)` and `(openxFactory-a, draft/b)` collapse
        together;
      * lowercasing the repository segment collapses two repositories that differ
        only in case.

    The consequence was silent and destructive: the second session REBOUND the
    first session's notebook, `_sync_sources`'s drop-what-left-the-set loop
    DELETED the first session's projected sources, and either teardown retired the
    notebook both were using. FR-037's own guarantee — "two live sessions can
    never share an alias" — was therefore false as written, which is why the fix
    is a spec delta (C11) and not only a patch.

    Appending the digest restores the guarantee by construction: the alias
    determines the key, so two live sessions cannot share one. It is belt AND
    braces with the OWNERSHIP refusal — `session_alias_owner`, consulted by
    `attach_session_notebook` at the one place a session's notebook comes into
    existence — which refuses a bind that would take another live session's alias
    however the alias came to collide. (This sentence named
    `assert_notebook_alias_unowned` until wave 2; no such function was ever
    written, so a maintainer grepping the name found nothing — the PR #49
    completeness critic caught it.)"""
    return (f"{notebook_alias_stem(repository, branch)}"
            f"{NOTEBOOK_KEY_SEPARATOR}{notebook_key_digest(repository, branch)}")


def session_alias_owner(registry: Any, alias: str, *,
                        exclude: tuple[str, str] | None = None
                        ) -> tuple[str, str] | None:
    """The LIVE session whose derived alias IS `alias`, or None (FR-037).

    A registry scan, because liveness IS the registry entry (FR-008) and the
    bootstrap re-derives it for every fresh process, so this sees the sessions of
    a CLI verb's own process exactly as it sees a serve's. Only session refs are
    considered — `main` is not a session and derives no session notebook."""
    keys = getattr(registry, "keys", None)
    if keys is None:
        return None
    try:
        pairs = [(str(repo), str(ref)) for repo, ref in keys()]
    except (TypeError, ValueError):                  # pragma: no cover - defensive
        return None
    for repo, ref in pairs:
        if exclude is not None and (repo, ref) == exclude:
            continue
        if not any(ref.startswith(f"{namespace}/") for namespace in SESSION_NAMESPACES):
            continue
        try:
            if notebook_alias(repo, ref) == alias:
                return repo, ref
        except SessionRefused:                       # pragma: no cover - defensive
            continue
    return None


def notebook_alias_collision_notice(alias: str, branch: str,
                                    owner: tuple[str, str]) -> str:
    """The FR-037/FR-042 notice: this session is OPEN, it has no notebook, and
    the reason is that another LIVE session already owns the alias."""
    repo, ref = owner
    return (
        f"the session on {branch!r} is OPEN and fully usable; it just has no "
        f"NotebookLM notebook: the alias {alias} is ALREADY OWNED by the live "
        f"session {repo}@{ref}, and binding it here would rebind that session's "
        "notebook and delete its projected sources. Two live sessions can never "
        "share an alias (FR-037), so nothing was created or touched. End that "
        "session, then `python3 scripts/sync-notebooklm-books.py "
        f"<workspace-root> --session-ref {branch} --apply` gives this one a "
        "notebook (FR-040, FR-042).")


# --------------------------------------------------------------------------
# the live tile inventory + the collision guard (FR-002, FR-026; G12)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Tile:
    """One live tile: the scope a session opens on. `scope_id` is stored
    REDUCED, so two spellings of the same staging id are one tile."""

    scope_kind: str
    scope_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope_id", reduce_scope_id(self.scope_id))

    @property
    def branch(self) -> str:
        return session_branch(self.scope_kind, self.scope_id)


@dataclass(frozen=True)
class TileInventory:
    """The LIVE tile inventory FR-026 requires the scans to be checked against —
    the staging folders and the cluster / possible registers. Passed in rather
    than discovered here, so the caller (the route, the CLI, a test) declares
    what exists and this module stays I/O-free."""

    tiles: tuple[Tile, ...] = ()

    @classmethod
    def from_scopes(cls, *, staged_topics: Iterable[str] = (),
                    clusters: Iterable[str] = (),
                    possibles: Iterable[str] = ()) -> "TileInventory":
        tiles = [Tile(STAGED_TOPIC, t) for t in staged_topics]
        tiles += [Tile(CLUSTER, c) for c in clusters]
        tiles += [Tile(POSSIBLE, p) for p in possibles]
        return cls(tuple(tiles))

    def branch_map(self) -> dict[str, Tile]:
        """Deterministic branch name -> the tile that owns it. An id that cannot
        produce a legal branch is skipped rather than raising: a hostile or
        malformed register entry must not break another tile's allocation."""
        out: dict[str, Tile] = {}
        for tile in self.tiles:
            try:
                out[tile.branch] = tile
            except SessionRefused:
                continue
        return out

    def other_branches(self, tile: Tile) -> dict[str, Tile]:
        return {b: t for b, t in self.branch_map().items() if t != tile}


def ordinal_of(branch: str, base: str) -> int | None:
    """Which ordinal of `base`'s family `branch` is, or None when it is not a
    family member at all. The base itself is ordinal 1.

    Deliberately strict: `draft/demo-topic-and-more`, `draft/demo-topical`, and
    `draft/demo-topic-02` are NOT family members. The first two are different
    tiles; the third is not the ratified `-2` spelling, and reading it as one
    would let a stray branch raise every future allocation."""
    if branch == base:
        return 1
    if not branch.startswith(base):
        return None
    match = _ORDINAL_RE.match(branch[len(base):])
    if not match:
        return None
    value = int(match.group(1))
    return value if value >= 2 else None


def tile_branch_family(names: Iterable[str], base: str, *,
                       excluded: Mapping[str, Tile] | Iterable[str] = ()) -> dict[int, str]:
    """`{ordinal: branch}` for every name in `base`'s family, EXCLUDING any
    branch that is another existing tile's deterministic name.

    The exclusion is FR-026's, and it applies to BOTH scans this feature runs —
    the ordinal computation and the abandoned-branch detection — so a `-2`
    branch belonging to another tile can neither be resumed as this tile's
    session nor consume this tile's ordinal."""
    skip = set(excluded)
    family: dict[int, str] = {}
    for name in names:
        if name in skip:
            continue
        ordinal = ordinal_of(name, base)
        if ordinal is not None:
            family[ordinal] = name
    return family


def next_ordinal(names: Iterable[str], base: str, *,
                 excluded: Mapping[str, Tile] | Iterable[str] = ()) -> int:
    """The highest EXISTING ordinal + 1 (FR-026, G5), skipping any candidate
    that is another existing tile's deterministic name.

    `names` is the UNION of the remote's and the local branches — see
    `existing_branch_names`. Both inputs are mandatory: without the remote two
    machines allocate the same ordinal (D17); without the local refs a
    never-pushed abandoned branch is invisible, and nothing in this feature
    pushes before `open-pr`."""
    skip = set(excluded)
    family = tile_branch_family(names, base, excluded=skip)
    candidate = (max(family) if family else 1) + 1
    # skip over any ordinal whose spelling belongs to ANOTHER tile
    while f"{base}-{candidate}" in skip:
        candidate += 1
    return candidate


def collision_owner(inventory: TileInventory, tile: Tile) -> Tile | None:
    """The OTHER tile whose ordinal form spells THIS tile's deterministic
    branch, or None. `draft/demo-topic-2` is tile `demo-topic-2`'s first branch
    and tile `demo-topic`'s second, so this is a real ambiguity whenever both
    tiles exist (FR-002, G12)."""
    try:
        branch = tile.branch
    except SessionRefused:
        return None
    for other_branch, other in sorted(inventory.other_branches(tile).items(),
                                      key=lambda kv: -len(kv[0])):
        if ordinal_of(branch, other_branch) not in (None, 1):
            return other
    return None


def assert_no_cross_tile_collision(inventory: TileInventory, tile: Tile,
                                   existing: Iterable[str]) -> None:
    """Refuse when this tile's deterministic branch EXISTS and cannot be
    attributed to one tile (FR-002, G12).

    Gated on the branch actually existing: while the name is unused there is
    nothing to join and nothing to cross, so a tile whose id merely LOOKS like
    another tile's ordinal form is not punished for it."""
    owner = collision_owner(inventory, tile)
    if owner is None:
        return
    branch = tile.branch
    if branch in set(existing):
        raise CrossTileCollision(tile, owner, branch)


# --------------------------------------------------------------------------
# the git-backed scans (FR-026) — remote UNION local, never one alone
# --------------------------------------------------------------------------

def existing_branch_names(git: SessionGit, base: str) -> tuple[str, ...]:
    """Every branch name beginning with `base`, from the REMOTE
    (`git ls-remote --heads`, never a fetch) UNION the LOCAL refs
    (`git branch --list`). Prefix-shaped, not family-filtered: filtering is
    `tile_branch_family`'s job, so the near-misses stay visible."""
    return tuple(sorted(set(git.remote_ordinals(base))
                        | set(git.local_ordinals(base))))


def allocate_ordinal(git: SessionGit, inventory: TileInventory,
                     tile: Tile) -> int:
    """The ordinal D17's NEW continuation allocates, computed over the union and
    against the live tile inventory."""
    base = tile.branch
    return next_ordinal(existing_branch_names(git, base), base,
                        excluded=inventory.other_branches(tile))


def new_session_branch(git: SessionGit, inventory: TileInventory,
                       tile: Tile) -> str:
    """The NEW continuation's branch name (FR-025/FR-026), validated with
    `git check-ref-format` before it is handed to any git write."""
    branch = session_branch(tile.scope_kind, tile.scope_id,
                            ordinal=allocate_ordinal(git, inventory, tile))
    git.require_legal_ref(branch)
    return branch


def deterministic_session_branch(git: SessionGit, inventory: TileInventory,
                                 tile: Tile) -> str:
    """This tile's OWN branch name, refusing on a genuine cross-tile collision
    (FR-002, G12) and validated with `git check-ref-format` first."""
    branch = tile.branch
    git.require_legal_ref(branch)
    assert_no_cross_tile_collision(inventory, tile,
                                   existing_branch_names(git, branch))
    return branch


def abandoned_branch_candidates(git: SessionGit, inventory: TileInventory,
                                tile: Tile) -> tuple[str, ...]:
    """The tile's own surviving branches, ordinal order — the input to the
    resume-or-new report (FR-025). Another tile's deterministic name is excluded
    here for the same reason it is excluded from the ordinal scan (FR-026)."""
    base = tile.branch
    family = tile_branch_family(existing_branch_names(git, base), base,
                               excluded=inventory.other_branches(tile))
    return tuple(family[o] for o in sorted(family))


# --------------------------------------------------------------------------
# liveness (T010; FR-008, D15, D10)
# --------------------------------------------------------------------------

def is_live(registry: Any, repository: str, branch: str) -> bool:
    """Is a branch session LIVE? A REGISTRY lookup, and nothing else.

    Neither a branch nor a worktree directory proves liveness ON ITS OWN: an
    abandoned branch survives its session by design (FR-022), and a crash can
    leave a worktree directory behind. Any code that infers liveness from either
    signal alone is a defect (D15, data-model liveness rule).

    THE SOLE EXCEPTION is the joint worktree+branch bootstrap re-derivation of
    task T033a. `SnapshotRegistry._entries` is an in-process dict, so a fresh
    process — the serve at start-up, and every CLI-parity verb, each its own
    process — would otherwise see NO live session and let `propose` proceed over
    unmerged drafts (the exact D15 hazard). That bootstrap re-registers a
    `(repository, branch)` entry for every worktree under the sessions container
    WHOSE BRANCH STILL EXISTS, reading the two signals JOINTLY and only there;
    D10 already names `git worktree list` as the session's derivation source, so
    it is the record's own recovery path rather than a new inference. A worktree
    with no branch — or a branch with no worktree — stays NON-LIVE and is
    surfaced as stale for the human-invoked cleanup."""
    getter = getattr(registry, "get", None)
    if getter is None:
        return False
    return getter(repository, branch) is not None


def tile_key(tile: "Tile | None") -> tuple[str, str] | None:
    """The tile as a plain `(scope_kind, scope_id)` pair — what a registry entry
    records so liveness can ask WHOSE session a ref is (finding 6). A pair rather
    than the `Tile` itself because the registry entry is a data record and must not
    hold behaviour."""
    if tile is None:
        return None
    return (str(tile.scope_kind), str(tile.scope_id))


def recorded_session_tile(registry: Any, repository: str, ref: str
                          ) -> tuple[str, str] | None:
    """The tile the registry entry for `ref` RECORDS, or None when it records none.

    None is a real answer, not a failure: the FR-008 bootstrap re-derives liveness
    from worktrees, which name branches and not tiles, so a fresh process's entries
    carry no owner until a verb JOINS one and states it."""
    getter = getattr(registry, "get", None)
    if getter is None:
        return None
    entry = getter(repository, ref)
    key = getattr(entry, "session_tile", None) if entry is not None else None
    if isinstance(key, (tuple, list)) and len(key) == 2:
        return (str(key[0]), str(key[1]))
    return None


def live_session_branches(registry: Any, repository: str, tile: "Tile", *,
                          inventory: "TileInventory | None" = None
                          ) -> tuple[str, ...]:
    """Every LIVE session branch belonging to THIS TILE, in ordinal order.

    A tile's session is not always at its deterministic name: D17's NEW
    continuation puts it at `draft/<topic>-2`, and after that the tile's ONE
    session lives there. So every liveness question a tile asks — FR-003's JOIN,
    FR-023's `propose` refusal, FR-027's prompt suppression — has to be asked over
    the tile's whole branch FAMILY, not over one spelling of it. A check that only
    looked at the base name would re-offer the resume-or-new prompt mid-session and
    let `propose` walk straight over an ordinal session.

    THE G12 EXCLUSION IS NOT AN EXCLUSION HERE (PR #49 second-review finding 6).
    Applied to ALLOCATION it is right and stays: a `-2` branch that is another
    existing tile's deterministic name must not be resumed as this tile's session
    and must not consume this tile's ordinal (`allocate_ordinal`,
    `abandoned_branch_candidates`, `assert_branch_cleanup_permitted`). Applied to
    LIVENESS it was wrong, because a live registry entry is not a NAME — it is a
    session that exists, and dropping it reported "no session" about a session. A
    tile whose session had moved to `-2` lost it the instant a sibling tile spelling
    that ordinal entered the inventory (a new staging folder, a cluster id, the
    nightly possibles regeneration): the next write forked the tile into a SECOND
    live session, and the first one's unmerged work could then be neither saved
    (`open-pr` joins the newer branch), abandoned (same), nor cleaned up (FR-028
    refuses the branch as not the tile's) — FR-003 and FR-027 both violated, in a
    state the realization notes called unreachable. Reproduced end to end.

    So OWNERSHIP is read, not guessed, in three cases:

      * the entry RECORDS this tile — it is this tile's session, whatever its
        spelling collides with, and it is never hidden;
      * the entry records ANOTHER tile — it is that tile's session and not this
        one's, which is the T049(c) case the exclusion was written for;
      * the entry records NO tile (a bootstrap reconstruction: a worktree names a
        branch, nothing names a tile) AND the ref is another inventory tile's
        deterministic name — a genuine AMBIGUITY. It raises `CrossTileCollision`
        naming both tiles and the live branch, because the one thing that must not
        happen is answering "no session" and opening a second one over it."""
    keys = getattr(registry, "keys", None)
    if keys is None:
        return ()
    try:
        refs = [str(ref) for repo, ref in keys() if str(repo) == str(repository)]
    except (TypeError, ValueError):                  # pragma: no cover - defensive
        return ()
    try:
        base = tile.branch
    except SessionRefused:                           # pragma: no cover - defensive
        return ()
    excluded = dict(inventory.other_branches(tile)) if inventory is not None else {}
    mine: dict[int, str] = {}
    for ref in refs:
        ordinal = ordinal_of(ref, base)
        if ordinal is None:
            continue
        owner = recorded_session_tile(registry, repository, ref)
        if owner is not None:
            if owner == tile_key(tile):
                mine[ordinal] = ref
            continue
        if ref in excluded:
            raise CrossTileCollision(
                excluded[ref], tile, ref,
                note=(f"a branch session is LIVE on {ref!r} and this process "
                      f"cannot tell which of the two tiles it belongs to — its "
                      f"registry entry was re-derived from the worktree, which "
                      f"names a branch and not a tile (FR-008's bootstrap). "
                      f"Answering 'no live session' here is what forked one tile "
                      f"into two (FR-003, FR-027), so this refuses instead: end "
                      f"that session (`open-pr` and merge, or `abandon-session`) "
                      f"from the tile that owns it, or rename one tile"))
        mine[ordinal] = ref
    return tuple(mine[o] for o in sorted(mine))


def assert_no_live_session(registry: Any, repository: str, tile: "Tile", *,
                           inventory: "TileInventory | None" = None,
                           verb: str = "propose") -> None:
    """Refuse an externally-committing verb while a live session holds the tile
    (FR-023, G2), naming the branch and BOTH resolutions.

    The refusal keys on the registry ENTRY, which is the whole point: a merged
    session and an abandoned session are both RESOLVED, and a branch that survives
    an abandon must NOT block — so this asks liveness and never `branch_exists`
    (D15). Both resolutions are named because a human whose `propose` was refused
    has two legitimate ways forward and neither is "wait"."""
    live = live_session_branches(registry, repository, tile, inventory=inventory)
    if not live:
        return
    branch = live[-1]
    raise LiveSessionRefused(
        f"{verb} refused: a branch session is LIVE on tile {tile.scope_id!r} "
        f"({tile.scope_kind}) at branch {branch!r}, which holds unmerged working "
        "state no gate has accepted — commissioning over it would propose one "
        "thing while another is being written (FR-023, D15). Resolve the session "
        "first, either way: save it (`open-pr`) and let its pull request MERGE, or "
        "`abandon-session` it with a reason. Either resolution clears this "
        "refusal, and a branch that SURVIVES an abandon does not block it.")


# --------------------------------------------------------------------------
# FR-007 — the externally-dispatching-verb refusal (T024)
# --------------------------------------------------------------------------

def assert_verb_stays_inside_session(verb: str | None, *,
                                     branch: str | None = None) -> None:
    """Refuse a verb whose effect reaches OUTSIDE the branch (FR-007).

    Called at the session ENTRY POINT — before the branch, the worktree, or the
    registry entry exist — so a refused dispatch persists nothing. The refusal
    REPORTS: it names the verb, the session it was attempted from, and why the
    two are incompatible, because a human who reached for `kickoff` inside a
    session needs to know the work must land on `main` first, not merely that
    the button did nothing."""
    if verb is None:
        return
    name = str(verb).strip()
    if name not in EXTERNALLY_DISPATCHING_VERBS:
        return
    where = f" (session branch {branch!r})" if branch else ""
    raise ExternalDispatchRefused(
        f"{name!r} is refused inside a branch session{where}: its effect reaches "
        "OUTSIDE the branch — a workflow dispatch that actually runs, a "
        "publication, an image build, or a rollout would act on unmerged "
        "exploration that no gate has accepted (FR-007). Save the session "
        "(`open-pr`) and let the pull request merge first; the verb is available "
        "on `main`, where the gate happens.")


# --------------------------------------------------------------------------
# FR-024 — the session-open precondition on a live proposal
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ProposalState:
    """What the tile's proposal pipeline looks like at session-open time.

    Two INDEPENDENT signals, because FR-024 owes two different messages:

      * `proposal_id` — a proposal that LANDED. The route back is `demote`, and
        the refusal names it.
      * `dispatch_in_flight` — a `propose` commission that was dispatched and has
        not been delivered. There is nothing to demote yet, so naming `demote`
        would name a route the human cannot take (D20); the refusal says the
        proposal has not landed instead.
    """

    proposal_id: str | None = None
    dispatch_in_flight: bool = False

    @property
    def live(self) -> bool:
        return bool(self.proposal_id) or bool(self.dispatch_in_flight)


def landed_proposal_ids(checkout_root: Path | str) -> dict[str, str]:
    """`{staging topic id: change id}` for every tile carrying a LANDED proposal
    (FR-024's other half; T055).

    Two signals, and BOTH are required, because each answers half the question:

      * the possibles register's PICK EDGE (`pick.staging_id` -> `pick.change_id`)
        is the only place the workspace records WHICH TILE a change came from — the
        same edge `generator._pick_links` reads, and the same one `demote`'s
        register-update note withdraws; and
      * the change's STATUS must be `active`, read through the generator's own
        `_iter_changes` so "active" means here exactly what it means in the funnel.
        An ARCHIVED change is not a live proposal: `plan_demotion` refuses anything
        non-active, so naming `demote` for one would name a route the human cannot
        take — the very failure D20 exists to prevent.

    Requiring both is also the forgiving direction: when a demotion has executed
    (the change folder removed, the pick edge withdrawn) EITHER half disappearing
    re-opens the tile, so a human who has not yet tidied the register is not locked
    out of their own topic.

    A malformed register is not this function's error to raise — the pinned
    validator owns conformance — so an unreadable one yields NO landed proposals
    and the tile stays open rather than becoming unworkable."""
    from .generator import _iter_changes        # the funnel's own status derivation
    from .register import CrossReferenceIndexAdapter

    root = Path(checkout_root)
    try:
        active = {change_id for change_id, status, _folder, _date
                  in _iter_changes(root) if status == "active"}
        entries = CrossReferenceIndexAdapter.discover(root).possibles()
    except Exception:  # noqa: BLE001 - a malformed input never blocks session work
        return {}
    landed: dict[str, str] = {}
    for entry in entries:
        pick = entry.get("pick") if isinstance(entry, Mapping) else None
        if not isinstance(pick, Mapping):
            continue
        staging_id = str(pick.get("staging_id") or "").strip()
        change_id = str(pick.get("change_id") or "").strip()
        if staging_id and change_id and change_id in active:
            landed.setdefault(staging_id, change_id)
    return landed


def proposal_state_for(tile: "Tile", *, records_root: Path | str | None = None,
                       proposal_ids: Mapping[str, str] | None = None,
                       checkout_root: Path | str | None = None
                       ) -> ProposalState:
    """Derive the tile's `ProposalState`.

    The IN-FLIGHT half reads the dispatched-but-undelivered `propose`
    workflow-jobs out of the served checkout's records tree, which is the SAME
    source `propose`'s own duplicate guard already reads
    (`kickoff.dispatched_propose_topics`) — one source of truth, not a second
    inference.

    The LANDED half (T055) is `landed_proposal_ids(checkout_root)`: a projection
    over the register's staged picks and the change status. An explicit
    `proposal_ids` mapping still wins, for a caller that already knows the answer
    (and for a test that wants one signal without a tree). This function is the ONE
    resolution point, which is why Phase 6 filled it in here rather than at every
    call site.

    Only a STAGED-TOPIC tile can carry a proposal: both signals are keyed on a
    staging id, and a cluster or possible tile has none."""
    from . import kickoff as kickoff_mod   # lazy: mirrors gate_console's cycle note

    staged = tile.scope_kind == STAGED_TOPIC
    landed = None
    if proposal_ids:
        landed = proposal_ids.get(tile.scope_id)
    elif checkout_root is not None and staged:
        landed = landed_proposal_ids(checkout_root).get(tile.scope_id)
    in_flight = False
    if records_root is not None and staged:
        in_flight = tile.scope_id in kickoff_mod.dispatched_propose_topics(records_root)
    return ProposalState(proposal_id=landed, dispatch_in_flight=in_flight)


def assert_no_live_proposal(state: ProposalState | None, tile: "Tile", *,
                            resuming: bool = False) -> None:
    """Refuse to OPEN or RESUME a session on a tile carrying a live proposal
    (FR-024, G3). The two messages are deliberately different strings, not one
    message with a variable in it, because they name different next actions."""
    if state is None or not state.live:
        return
    what = "resumed" if resuming else "opened"
    if state.proposal_id:
        raise LiveProposalRefused(
            f"no session is {what} on tile {tile.scope_id!r}: it carries the live "
            f"proposal {state.proposal_id!r}. A tile is worked OR proposed, never "
            "both — `demote` the proposal back to staging first, and the tile "
            "opens a session normally afterwards (FR-024).")
    raise LiveProposalRefused(
        f"no session is {what} on tile {tile.scope_id!r}: a `propose` commission "
        "for it was dispatched and the proposal has not landed yet, so there is "
        "nothing to send back and the tile is closed to session work until the "
        "authoring is delivered (FR-024, D20).")


# --------------------------------------------------------------------------
# session OPEN — idempotent open-or-join (T022; FR-001, FR-003, FR-005)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class SessionOpen:
    """The result of one open-or-join. A session persists NO descriptor (D10), so
    this is a return value and never a stored record: every field is re-derivable
    from the tile, from git, and from the registry."""

    repository: str
    tile: "Tile"
    branch: str
    worktree: Path
    joined: bool                 # True: JOINED a session that already existed
    entry: Any                   # the registry entry that KEYS liveness (FR-008)
    notebook_alias: str
    # The registry this session is keyed in, carried so the ACTION path can
    # regenerate the session's snapshot without every caller re-threading it
    # (FR-010, T034). None only for a caller that built a SessionOpen by hand.
    registry: Any = None
    # Whether the session's notebook has been created (T074, FR-036), and the
    # honest notice when it could not be (FR-042, D19). A session that opened
    # without a notebook is a complete session — the notice is a NOTIFICATION,
    # never a failure, and `notebook_created=False` with no notice is the
    # ordinary shape on a plane that declares no adapter at all.
    #
    # Both are filled by `attach_session_notebook`, which the gate action runs
    # AFTER its commit has landed — not by the open (PR #49 review finding 3).
    notebook_created: bool = False
    notebook_notice: str | None = None
    # The adapter this OPEN would create the notebook with, carried forward
    # rather than used here. A refused first create used to leave a real
    # NotebookLM notebook behind on the shared account with no unwind and no
    # route to reclaim the quota; deferring the create to the first SUCCESSFUL
    # commit removes the leak with no compensation logic at all, and FR-040's
    # `--session-ref` re-sync remains the documented retry route. None on a JOIN
    # (the notebook already exists) and on a plane that declares no adapter.
    pending_notebook: Any = None

    @property
    def opened(self) -> bool:
        return not self.joined


def session_entry(repository: str, branch: str, worktree: Path | str, *,
                  snapshot_path: Path | str | None = None,
                  tile: "Tile | None" = None,
                  session_base: tuple[str, str] | None = None,
                  session_base_aliases: tuple[str, ...] = ()) -> Any:
    """The `(repository, session-branch)` registry entry whose `source_root` is
    the worktree — the AUTHORITATIVE liveness signal (FR-008, FR-009).

    Built with the EXISTING entry type: no overlay, no diff layer, no second
    projection path (FR-009). `snapshot_path` is where the session's generated
    snapshot lands; `register_session_entry` supplies it, and liveness works
    without one (which is what let Phase 3 land before the projection existed).

    `assert_publishable` already refuses this entry for publication because its
    ref is not `main` (FR-012), so nothing extra is needed to keep a session
    snapshot out of a published index.

    `tile` records WHOSE session this is (finding 6). The ref cannot answer it — a
    `-2` branch is one tile's first session and another's second — so the caller
    that OPENED the session, the only place the answer exists, states it here."""
    from .snapshot_registry import SnapshotEntry   # lazy: keeps the import graph flat

    return SnapshotEntry(repository=repository, ref=branch,
                         source_root=Path(worktree),
                         snapshot_path=Path(snapshot_path) if snapshot_path else None,
                         display_name=f"{repository} @ {branch}",
                         session_tile=tile_key(tile),
                         session_base=session_base,
                         session_base_aliases=tuple(session_base_aliases))


# --------------------------------------------------------------------------
# the session PROJECTION — one registry entry, one generated snapshot
# (T033/T034; FR-009, FR-010)
# --------------------------------------------------------------------------

def register_session_entry(registry: Any, *, repository: str, branch: str,
                           worktree: Path | str, checkout_root: Path | str,
                           regenerate: bool = True, generator: Any = None,
                           project_register: Path | str | None = None,
                           tile: "Tile | None" = None,
                           session_base: tuple[str, str] | None = None,
                           session_base_aliases: tuple[str, ...] = ()) -> Any:
    """Register the session's entry and point it at the session's OWN snapshot
    (FR-009, T033).

    The registry's existing `register` is the whole mechanism: no overlay, no diff
    layer, no second projection path. Because the entry's `source_root` is the
    WORKTREE, every existing consumer follows the session without knowing sessions
    exist — the keyed snapshot route, the keyed `/source` confinement
    (`resolve_source` -> `resolve_within`), the freshness headers, and the local
    regenerate binding all read `entry.source_root`.

    `regenerate=False` registers against whatever snapshot is already on disk,
    which is what the bootstrap wants for a session whose last action already
    generated one (T033a) — re-running the generator for every live session at
    every process start would be work with no new answer.

    `tile` is carried onto the entry (finding 6): an OPEN knows whose session it is,
    and the BOOTSTRAP does not — a worktree names a branch, never a tile — so the
    bootstrap passes None and liveness treats that unknown honestly.

    `session_base` is carried onto the entry the same way (T104 R-12): the OPEN
    (or the bootstrap's marker read) is where the branch point is known, and the
    chat-turn binding check reads it back off the entry. None degrades to the
    original name-equality binding — advisory, never a refusal."""
    from .snapshot_registry import entry_from_snapshot_file

    snapshot_path = session_snapshot_path(checkout_root, branch)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    if not regenerate and snapshot_path.is_file():
        # An entry registered against a snapshot ALREADY on disk takes its
        # `source_revision` and `generated_at` OUT OF that snapshot — restating
        # them would let the freshness header (FR-011) say nothing, or worse say
        # something the bytes do not support.
        candidate = entry_from_snapshot_file(
            snapshot_path, repository=repository, ref=branch,
            source_root=Path(worktree), display_name=f"{repository} @ {branch}")
        candidate.session_tile = tile_key(tile)
        candidate.session_base = session_base
        candidate.session_base_aliases = tuple(session_base_aliases)
    else:
        candidate = session_entry(repository, branch, worktree,
                                  snapshot_path=snapshot_path, tile=tile,
                                  session_base=session_base,
                                  session_base_aliases=session_base_aliases)
    entry = _register_without_stealing_active(registry, candidate)
    if regenerate:
        _refresh_or_report(registry, repository=repository, branch=branch,
                           worktree=worktree, generator=generator,
                           project_register=project_register)
        entry = registry.get(repository, branch) or entry
    if session_base is not None:
        # The refresh re-registers a FRESH entry (same hazard as the owner
        # re-stamp below), so the base rides the same suppression.
        with contextlib.suppress(AttributeError):
            entry.session_base = session_base
            entry.session_base_aliases = tuple(session_base_aliases)
    if tile is not None:
        # RE-STAMP after the refresh: `SnapshotSource._regenerate` registers a FRESH
        # entry for the ref it regenerates, which would otherwise drop the owner and
        # take the tile's own live session back out of its liveness family (finding
        # 6). And leave the durable copy for the next process, which re-derives
        # entries from worktrees and cannot know whose session this is.
        with contextlib.suppress(AttributeError):
            entry.session_tile = tile_key(tile)
        write_owner_marker(checkout_root, branch, tile, base=session_base,
                           base_aliases=tuple(session_base_aliases))
    return entry


def unregister_session_entry(registry: Any, repository: str, branch: str) -> None:
    """Drop the session's entry — the SOLE way a session stops being live
    (FR-009, T033).

    `drop` is the registry's existing removal and there is deliberately no second
    removal path: liveness IS the entry (FR-008), so both endings (merge and
    abandon, FR-021) end a session by calling exactly this. The generated snapshot
    FILE is left behind for the teardown that removes the worktree with it — a
    dropped entry is already non-live, and deleting derived bytes is not what makes
    it so."""
    dropper = getattr(registry, "drop", None)
    if dropper is None:                              # pragma: no cover - defensive
        return
    dropper(repository, branch)


def refresh_session_snapshot(registry: Any, *, repository: str, branch: str,
                             worktree: Path | str, generator: Any = None,
                             project_register: Path | str | None = None) -> dict:
    """Regenerate the session's snapshot FROM THE WORKTREE, through the registry's
    EXISTING local refresh binding (FR-010, T034).

    `SnapshotSource.refresh` is the seam and this is a CALLER of it, not a second
    generator: with a checkout root and no data source its `refresh_binding` is
    `regenerate`, which re-runs the generator for ONE (repository, ref) against
    `entry.source_root` — the worktree — and rewrites that entry's derived
    snapshot through the interactivity boundary. The session's panels therefore
    refresh by the same mechanism `main`'s do.

    The ACTIVE entry is restored afterwards: `_regenerate` promotes what it
    regenerates, and a session snapshot must never become what the wheel, the
    funnel, and the pipeline board render (FR-014a)."""
    from .snapshot_registry import BINDING_REGENERATE, SnapshotSource

    source = SnapshotSource(checkout_root=Path(worktree), generator=generator,
                            project_register=project_register)
    # the shared registry IS the source's registry: the entry regenerated is the
    # one liveness is keyed on, never a copy of it
    source.registry = registry
    if source.refresh_binding != BINDING_REGENERATE:
        raise SessionRefused(
            f"the session worktree {worktree} is not a directory this process can "
            "regenerate from, so the session snapshot cannot be generated from the "
            "WORKTREE root as FR-010 requires")
    return _preserving_active(
        registry, lambda: source.refresh(repository=repository, ref=branch))


def _refresh_or_report(registry: Any, *, repository: str, branch: str,
                       worktree: Path | str, generator: Any = None,
                       project_register: Path | str | None = None) -> dict | None:
    """Regenerate, and on failure record the reason ON THE ENTRY instead of
    failing the caller.

    A session's liveness is its registry entry, not its projection (FR-008): a
    generator that cannot run must not un-live a session, and it certainly must not
    undo a commit that has already landed. The entry then reports itself
    UNAVAILABLE with the reason, which is the shape the selector already renders
    for an entry whose snapshot cannot be read."""
    try:
        return refresh_session_snapshot(
            registry, repository=repository, branch=branch, worktree=worktree,
            generator=generator, project_register=project_register)
    except Exception as exc:  # noqa: BLE001 - reported, never fatal (see docstring)
        entry = getattr(registry, "get", lambda *_: None)(repository, branch)
        if entry is not None:
            entry.unavailable_reason = (
                f"the session snapshot could not be generated: {exc}")
        return None


def _registered_worktree(registry: Any, repository: str, branch: str,
                         fallback: Path) -> Path:
    entry = getattr(registry, "get", lambda *_: None)(repository, branch)
    root = getattr(entry, "source_root", None) if entry is not None else None
    return Path(root) if root else fallback


def _git_knows_worktree(git: SessionGit, worktree: Path) -> bool:
    target = Path(worktree).resolve()
    for known in git.worktree_paths():
        try:
            if Path(known).resolve() == target:
                return True
        except OSError:                              # pragma: no cover - defensive
            continue
    return False


def normalize_continuation(continuation: str | None) -> str | None:
    """FR-025's answer, validated. `None` means "no answer given" — which is what
    makes the report the DEFAULT and the silent choice impossible; anything that is
    not one of the two tokens is a caller error rather than a guessed intent."""
    if continuation is None:
        return None
    value = str(continuation).strip().lower()
    if not value:
        return None
    if value not in CONTINUATIONS:
        raise SessionRefused(
            f"{continuation!r} is not a session continuation; the two FR-025 "
            f"continuations are {CONTINUATION_RESUME!r} (re-materialize a worktree "
            f"over the surviving branch under its existing name) and "
            f"{CONTINUATION_NEW!r} (open the next ordinal)")
    return value


def _recover_session_base(git: SessionGit, base: str, branch: str,
                          root: Path | str, *,
                          prefer_git: bool = False) -> tuple[str, str] | None:
    """The `(base_ref, base_revision)` this session grounds pre-session
    buffers against (T104 R-12): the durable marker when the OPEN left one,
    else git's own fork point — a session branch is created FROM its base
    and every gate action commits on the branch alone, so
    `merge-base <base> <branch>` IS the branch point. ADVISORY like the
    owner marker: None when neither source can answer, which degrades the
    binding check to its original name-equality shape rather than to a
    failure.

    `prefer_git=True` is for the arms that JUST created (or re-materialized)
    the branch, where git's fork point is ground truth: a marker there can
    only be crash residue from a PREVIOUS session of the same deterministic
    name, and reading it first resurrected a dead session's base and
    re-persisted it — self-healing never occurred (wave re-review, R-12
    machinery). The JOIN and bootstrap arms stay marker-first: the marker is
    the one source that remembers a non-default base."""
    def _from_marker() -> tuple[str, str] | None:
        return read_base_marker(root, branch)

    def _from_git() -> tuple[str, str] | None:
        try:
            revision = git.merge_base(base, branch)
        except (SessionGitRefused, GitError, OSError):
            return None
        return (base, revision) if revision else None

    first, second = ((_from_git, _from_marker) if prefer_git
                     else (_from_marker, _from_git))
    return first() or second()


def _session_base_aliases(registry: Any, repository: str, branch: str,
                          root: Path | str,
                          session_base: tuple[str, str] | None
                          ) -> tuple[str, ...]:
    """The base's OTHER recorded revision spellings (W-4, wave re-review).

    A real client's `base_revision` is not the branch point: the browser
    never receives a per-file revision, so it declares the serving
    projection's `source_revision` — the checkout HEAD at snapshot
    GENERATION time — while the branch point is the HEAD at OPEN time. Any
    main movement between snapshot bake and session open made the two
    differ forever, silently reverting R-12's acceptance to the refusal it
    closed (executed in the wave re-review, both directions). So the OPEN
    records the serving snapshot's revision beside the merge-base, the
    marker persists it, and the bootstrap reads it back verbatim — it can
    never be re-derived later, because the snapshot regenerates. Advisory
    like everything else here: () costs only the alias acceptance."""
    if session_base is None:
        return ()
    # The marker's aliases are trusted ONLY when its base agrees with the
    # recovered one: a crash-orphaned marker whose base a prefer-git arm just
    # overrode must not smuggle its aliases back in (wave re-review, R-12
    # machinery — one rule here rather than per-arm plumbing).
    if read_base_marker(root, branch) == session_base:
        aliases = read_base_marker_aliases(root, branch)
        if aliases:
            return aliases
    try:
        entry = getattr(registry, "get", lambda *_: None)(
            repository, session_base[0])
        revision = getattr(entry, "source_revision", None)
    except Exception:  # noqa: BLE001 - advisory, never the reason an open fails
        return ()
    if isinstance(revision, str) and revision and revision != session_base[1]:
        return (revision,)
    return ()


def open_session(git: SessionGit, registry: Any, *, repository: str,
                 tile: "Tile", inventory: TileInventory | None = None,
                 base: str = DEFAULT_BASE, verb: str | None = None,
                 proposal: ProposalState | None = None,
                 checkout_root: Path | str | None = None,
                 require_live: bool = False,
                 remedy: str | None = None,
                 continuation: str | None = None,
                 notebook: Any = None) -> SessionOpen:
    """Open the tile's branch session, or JOIN the one that already exists
    (FR-001, FR-003, FR-005). IDEMPOTENT: calling it again — from another actor,
    another request, another process — returns the same branch and the same
    worktree and creates nothing.

    Order matters, and each step is a refusal that persists nothing:

      1. FR-007: an externally-dispatching verb never opens a session (T024).
      2. FR-024: a tile carrying a live proposal is closed to session work, with
         the two distinct messages.
      3. FR-002/G12: the branch name is derived from the TILE and refused on a
         genuine cross-tile collision — never silently joined.
      4. FR-008: liveness is a REGISTRY lookup, asked over the tile's whole
         branch FAMILY (`live_session_branches`) because D17's NEW continuation
         moves the tile's session to `-2`. A live entry is a JOIN, full stop: no
         second worktree can appear and the resume-or-new report cannot re-fire
         mid-session (FR-027). The registry remains the ONLY thing that decides
         join-versus-open — but the joined entry's worktree is VALIDATED against
         git before it is handed back (`assert_git_holds_branch`), because an
         entry records the pairing once and nothing revokes it (PR #49 review
         finding 5, wave 2). That call can only turn a join into a refusal; it
         can never find a session, so liveness is still registry-only.
      5. Otherwise the branch and the worktree are read JOINTLY (D10):

         | branch | worktree | outcome                                        |
         |--------|----------|------------------------------------------------|
         | no     | no       | OPEN: `worktree add -b <branch> <path> <base>` |
         | yes    | yes      | ADOPT + JOIN — the bootstrap rule (T033a)      |
         | yes    | no       | the FR-025 CHOICE (see `continuation`)         |
         | no     | yes      | REFUSE: stale residue, human cleanup (FR-008)  |

    `continuation` is the human's answer to that choice (FR-025, T056), and the
    THIRD row is the only place it means anything:

      * absent -> `AbandonedBranchSurvives`, which IS the report: it names the
        surviving branch, both continuations, and the ordinal NEW would allocate.
      * `resume` -> `git worktree add <path> <branch>`: the EXISTING branch keeps
        its name and its history, so the resumed session builds ON the abandoned
        work rather than beside it.
      * `new` -> the next ordinal over the UNION of remote and local refs,
        excluding another tile's deterministic name (FR-026, G5, G12).

    An answer that arrives when there is nothing to continue from is refused
    rather than reinterpreted: with the deterministic name FREE, `new` would
    allocate `-2` over an unused base and `resume` has no branch to re-materialize.
    An answer that arrives while a session is LIVE never reaches here at all —
    step 4 JOINs first, which is exactly FR-027's suppression.

    The served checkout is never switched, reset, or stashed by any of it: the
    only writes are `git worktree add` (which acts on the container, not the
    served working tree) and the registry entry, which is in-process
    (FR-004, SC-002).

    `require_live=True` turns step 4 into a REQUIREMENT: a live entry is joined
    as always, and anything else raises `NoActiveSession` instead of opening —
    the shape a SESSION-ONLY verb needs (`edit-document`, T042; Phase 6/7's
    `abandon-session` / `open-pr`). It is a flag on this function rather than a
    second resolver so the ordering above stays the ONE ordering: FR-007's verb
    refusal and FR-024's live-proposal refusal are evaluated first, and they name
    the tile's real problem instead of "no session". `remedy` is the caller's
    verb-specific next step, appended to that refusal.

    `registry` is duck-typed on `get` / `register` so a caller may pass the
    serve's `SnapshotRegistry` (T025), a CLI-process registry (each verb is a
    fresh process — FR-008's bootstrap, T033a), or a test double.

    `notebook` is the INJECTED notebook adapter (T074, FR-036): when one is
    declared, an OPEN creates the session's `xf-session-*` notebook from the
    worktree's governed documents. A JOIN deliberately creates nothing — the
    notebook already exists, and re-projecting it on every gate action would be
    `nlm` traffic with no new answer; the FR-040 `--session-ref` re-sync is the
    refresh route, and it is also the retry route for a session that opened
    without one. A create that cannot happen DEGRADES: the session opens anyway
    and `notebook_notice` carries the honest reason (FR-042, D19)."""
    root = Path(checkout_root) if checkout_root is not None else git.served_root
    inventory = inventory if inventory is not None else TileInventory((tile,))
    if tile not in inventory.tiles:
        # A caller that declared an inventory the tile is not in still gets the
        # tile's own name checked against it; the tile itself is never absent
        # from its own collision check.
        inventory = TileInventory((*inventory.tiles, tile))

    continuation = normalize_continuation(continuation)
    assert_verb_stays_inside_session(verb)
    assert_no_live_proposal(proposal, tile,
                            resuming=continuation == CONTINUATION_RESUME)

    branch = deterministic_session_branch(git, inventory, tile)
    assert_verb_stays_inside_session(verb, branch=branch)

    live = live_session_branches(registry, repository, tile, inventory=inventory)
    if live:
        # The tile's ONE session, wherever its ordinal put it. When more than one
        # entry is somehow live the HIGHEST ordinal is joined — the most recent
        # continuation — rather than refusing, because a refusal here would leave
        # the tile with no route forward at all.
        #
        # That used to be justified with "FR-027's suppression makes the case
        # unreachable", which was FALSE (second-review finding 6): the G12 exclusion
        # was applied to LIVENESS, so a sibling tile appearing in the inventory hid
        # this tile's own ordinal session and the next write opened a second one.
        # `live_session_branches` no longer guesses ownership from the ref, so the
        # multi-entry case is genuinely residual rather than declared impossible.
        branch = live[-1]
        worktree = _registered_worktree(registry, repository, branch,
                                        worktree_path(root, branch))
        # The entry says this worktree is on this branch. It said so at OPEN, and
        # nothing revokes it — so ask git, before the caller's engine authors
        # anything into a directory that may have drifted (finding 5, wave 2).
        assert_git_holds_branch(git, worktree, branch,
                                during=f"the session JOIN on {branch!r}")
        # STAMP THE OWNER on a bootstrap-reconstructed entry (finding 6). Reaching
        # here means liveness has already established that this ref is THIS tile's
        # session — either the entry said so or it said nothing and nothing else
        # could claim it — so recording it now is what makes the answer survive an
        # inventory that grows a sibling tile later in this process's life. Never
        # an overwrite: an entry that names another tile never gets here.
        joined_entry = getattr(registry, "get", lambda *_: None)(repository, branch)
        if joined_entry is not None and \
                getattr(joined_entry, "session_tile", None) is None:
            with contextlib.suppress(AttributeError):
                joined_entry.session_tile = tile_key(tile)
        if joined_entry is not None and \
                getattr(joined_entry, "session_base", None) is None:
            # Same late-stamp rule for the session's base (T104 R-12): a
            # bootstrap-reconstructed entry predating the marker's base keys
            # can still recover its branch point from git, here where a real
            # worktree is guaranteed.
            with contextlib.suppress(AttributeError):
                recovered = _recover_session_base(git, base, branch, root)
                joined_entry.session_base = recovered
                joined_entry.session_base_aliases = _session_base_aliases(
                    registry, repository, branch, root, recovered)
        return SessionOpen(repository=repository, tile=tile, branch=branch,
                           worktree=worktree, joined=True,
                           entry=registry.get(repository, branch),
                           notebook_alias=notebook_alias(repository, branch),
                           registry=registry)

    if require_live:
        # A session-only verb: the JOIN above is the only outcome it accepts, so
        # nothing below this line — no branch, no worktree, no registry entry —
        # may be created on its behalf (FR-016).
        raise NoActiveSession(tile, branch, verb=verb, remedy=remedy)

    worktree = worktree_path(root, branch)
    branch_present = git.branch_exists(branch)
    directory_present = worktree.is_dir()
    # THE ABANDONED-BRANCH DETECTOR reads the union, and the whole FAMILY (FR-026,
    # G5, G12; PR #49 review finding 7). It used to be `git.branch_exists` on the
    # BASE NAME — local refs, one spelling — while `abandoned_branch_candidates`,
    # the union-and-family helper written for exactly this job, had no production
    # caller at all. Two reproduced consequences: a branch surviving only on the
    # REMOTE was invisible, so `open_session` forked a DIVERGENT local branch of
    # the same name over another machine's work with no resume-or-new report and
    # `push` then dead-ended non-fast-forward; and with only `draft/<t>-2`
    # surviving, the tile opened a fresh base branch and the ordinal session's
    # work was unreachable from it.
    surviving = () if directory_present else abandoned_branch_candidates(
        git, inventory, tile)

    if surviving:
        return _continue_abandoned(git, registry, repository=repository, tile=tile,
                                   inventory=inventory, surviving=surviving,
                                   root=root, base=base,
                                   continuation=continuation, notebook=notebook)
    if continuation is not None:
        raise SessionRefused(
            f"continuation={continuation!r} was answered for tile "
            f"{tile.scope_id!r} but there is no abandoned session branch to "
            f"continue from: no branch of {branch!r}'s family survives with a "
            "worktree missing. Nothing was opened — retry without a continuation "
            "and the tile opens under its ordinary naming rules (FR-025).")
    if directory_present and not branch_present:
        raise StaleSessionWorktree(worktree, branch)

    alias = notebook_alias(repository, branch)
    if branch_present and directory_present:
        # The joint signal, both halves present AND AGREEING: this IS the session,
        # and a fresh process re-deriving it is exactly the ONE permitted exception
        # to the registry-only liveness rule (D10, FR-008). T033a generalizes this
        # from "the tile being written" to "every worktree in the container".
        #
        # `_git_holds_branch` replaces a co-presence test (PR #49 review finding
        # 5): asking only whether git KNEW the directory adopted a worktree the
        # human had checked out onto another branch, or an interrupted rebase had
        # left detached, and the next gate action then committed there.
        if not _git_holds_branch(git, worktree, branch):
            raise StaleSessionWorktree(worktree, branch)
        _refuse_ended_session_residue(root, branch, worktree)
        joined = True
    else:
        git.worktree_add(branch, worktree, base)
        # a materialized worktree is a live session again, whatever ended before
        clear_ending_marker(root, branch)
        joined = False

    session_base = _recover_session_base(git, base, branch, root,
                                         prefer_git=not joined)
    entry = register_session_entry(registry, repository=repository, branch=branch,
                                   worktree=worktree, checkout_root=root, tile=tile,
                                   # Known HERE and nowhere later (T104 R-12): a
                                   # fresh branch's merge base with `base` is the
                                   # tip it was just created from, and an adopted
                                   # one recovers marker-first. The serving
                                   # snapshot's revision rides beside it (W-4).
                                   session_base=session_base,
                                   session_base_aliases=_session_base_aliases(
                                       registry, repository, branch, root,
                                       session_base))
    return SessionOpen(repository=repository, tile=tile, branch=branch,
                       worktree=worktree, joined=joined, entry=entry,
                       notebook_alias=alias, registry=registry,
                       # DEFERRED to the first successful commit (finding 3)
                       pending_notebook=None if joined else notebook)


def _continue_abandoned(git: SessionGit, registry: Any, *, repository: str,
                        tile: "Tile", inventory: TileInventory,
                        surviving: Sequence[str], root: Path,
                        continuation: str | None, base: str = DEFAULT_BASE,
                        notebook: Any = None) -> SessionOpen:
    """The FR-025 choice, resolved: report it, RESUME it, or open the NEW ordinal.

    Split out of `open_session` because it is the one place three requirements
    meet — FR-025's "never choose silently", FR-026's union-and-inventory ordinal,
    and FR-002's ref legality — and because the RESUME and NEW paths use two
    different git operations (`worktree add <path> <branch>` over an existing
    branch, versus `worktree add -b`) that must not be confusable.

    `surviving` is the tile's WHOLE surviving family in ordinal order, over the
    UNION of the remote and the local refs (PR #49 review finding 7). Two things
    follow that a base-name/local-only detector could not do: RESUME offers the
    MOST RECENT ordinal rather than the oldest one (with both `draft/<t>` and
    `draft/<t>-2` surviving, resuming the base left the `-2` session's work
    unreachable), and a branch that survives only ON THE REMOTE is REPORTED as
    such instead of being forked over. FR-026 forbids this scan from fetching, so
    a remote-only RESUME is a refusal that names the human's two real options —
    fetch it yourself, or start a NEW ordinal — because silently creating a
    divergent local branch of the same name is strictly worse than saying so."""
    resume_target = surviving[-1]                    # the most recent ordinal
    local = set(git.local_ordinals(tile.branch))
    remote_only = tuple(b for b in surviving if b not in local)
    if continuation is None:
        raise AbandonedBranchSurvives(
            resume_target, ordinal_hint=session_branch(
                tile.scope_kind, tile.scope_id,
                ordinal=allocate_ordinal(git, inventory, tile)),
            family=tuple(surviving), remote_only=remote_only)
    if continuation == CONTINUATION_RESUME:
        branch = resume_target
        if branch not in local:
            raise SessionRefused(
                f"{branch!r} survives only on the remote (`git ls-remote --heads`), "
                f"not in this checkout, so it cannot be RESUMED here: opening a "
                f"worktree would create a DIVERGENT local branch of the same name "
                f"over work this machine has never seen, and no session operation "
                f"fetches (FR-026, D17). Two real options: fetch it yourself "
                f"with an EXPLICIT DESTINATION REFSPEC — "
                f"`git fetch origin refs/heads/{branch}:refs/heads/{branch}` — "
                f"and answer continuation={CONTINUATION_RESUME!r} again, or "
                f"answer continuation={CONTINUATION_NEW!r} to start the next "
                "ordinal beside it. Nothing was opened.\n\n"
                "THE REFSPEC IS THE WHOLE INSTRUCTION, not decoration: "
                f"`git fetch origin {branch}` succeeds, prints nothing alarming, "
                "and creates NO local branch at all — it lands the objects in "
                "FETCH_HEAD and stops — so answering `resume` after it returns "
                "this identical refusal. Nor is `git checkout` a substitute: it "
                "creates the ref but CHECKS IT OUT here, and a branch that is "
                "checked out cannot also be given a worktree (PR #234, Codex).")
        worktree = worktree_path(root, branch)
        # A branch git already has CHECKED OUT cannot also be given a worktree —
        # git exits 128. Reached when a human materialized the ref with
        # `git checkout <branch>` instead of a refspec fetch, which is the
        # natural wrong move and was the one this refusal used to answer with a
        # raw GitError naming neither the cause nor the fix (PR #234, Codex).
        holder = git.checked_out_at(branch)
        if holder is not None:
            raise SessionRefused(
                f"{branch!r} is already CHECKED OUT at {holder}, so a session "
                f"worktree cannot be added for it — git allows a branch in one "
                f"working tree at a time. This is what `git checkout {branch}` "
                f"leaves behind; the session flow wants the branch PRESENT but "
                f"NOT checked out. Switch that tree back "
                f"(`git -C {holder} checkout {DEFAULT_BASE}`) and answer "
                f"continuation={CONTINUATION_RESUME!r} again. Nothing was "
                "opened.")
        git.worktree_add_existing(branch, worktree)
        # a RESUME is a live session again: the ending this branch had is over as
        # a fact about the PAST, and must not read as residue about the present
        clear_ending_marker(root, branch)
    else:
        branch = new_session_branch(git, inventory, tile)
        worktree = worktree_path(root, branch)
        if git.branch_exists(branch) or worktree.is_dir():
            # The allocation is computed over the union of remote and local refs, so
            # reaching here means the tree changed under us (a concurrent open, a
            # fetch). Refusing beats adopting a name this call did not allocate.
            raise SessionRefused(
                f"the NEW session branch {branch!r} appeared while it was being "
                "allocated, so this call did not create it; nothing was opened "
                "(FR-026) — retry, and the next ordinal is recomputed.")
        git.worktree_add(branch, worktree, base)
        clear_ending_marker(root, branch)
    session_base = _recover_session_base(git, base, branch, root,
                                         prefer_git=True)
    entry = register_session_entry(registry, repository=repository, branch=branch,
                                   worktree=worktree, checkout_root=root, tile=tile,
                                   # A RESUME recovers the branch point it was
                                   # abandoned with (marker-first, then git);
                                   # a NEW ordinal was just created from `base`
                                   # (T104 R-12), with the serving snapshot's
                                   # revision recorded beside it (W-4).
                                   session_base=session_base,
                                   session_base_aliases=_session_base_aliases(
                                       registry, repository, branch, root,
                                       session_base))
    # BOTH continuations are an OPEN, not a join: a RESUME re-materializes a
    # worktree whose notebook was retired when the session was abandoned (D16),
    # and a NEW ordinal is a different session with a different alias — so each
    # gets its own notebook (FR-036, FR-037). Created at the first successful
    # commit, exactly like the ordinary open (finding 3).
    alias = notebook_alias(repository, branch)
    return SessionOpen(repository=repository, tile=tile, branch=branch,
                       worktree=worktree, joined=False, entry=entry,
                       notebook_alias=alias, registry=registry,
                       pending_notebook=notebook)


def _preserving_active(registry: Any, action):
    """Run `action` and leave the registry's ACTIVE entry exactly as it was
    (FR-014a).

    Two existing mechanisms promote what they touch: `SnapshotRegistry.register`
    when nothing is active yet, and `SnapshotSource._regenerate` always
    (`active=True`). Both are right for `main` and wrong for a session — the
    session ref must enter the KEY SPACE and change nothing about what the wheel,
    the funnel, or the pipeline board render. Duck-typed throughout, because the
    registry may be a test double.

    ATOMIC (PR #49 review finding 10). This is a read-modify-write over one
    field — read the active key, run the action, put it back — and `serve.py` is
    a `ThreadingHTTPServer`, so two concurrent session regenerations interleaved
    into "both read main, both register, both restore" and left a DRAFT active
    (reproduced at function level with a forced interleave). The registry's own
    re-entrant lock covers the whole triple; a registry double that offers no
    `atomically` simply runs unsynchronized, exactly as before."""
    hold = getattr(registry, "atomically", None)
    with (hold() if callable(hold) else contextlib.nullcontext()):
        previous = getattr(registry, "active", None)
        result = action()
        set_active = getattr(registry, "set_active", None)
        if previous is not None and set_active is not None:
            current = getattr(registry, "active", None)
            if current is not None and current.key != previous.key:
                set_active(previous.repository, previous.ref)
        return result


def _register_without_stealing_active(registry: Any, entry: Any) -> Any:
    """Register the session entry WITHOUT changing which snapshot the shared
    surfaces show (FR-014a) — see `_preserving_active`."""
    return _preserving_active(registry, lambda: registry.register(entry))


# --------------------------------------------------------------------------
# the BOOTSTRAP re-derivation (T033a; FR-008, D10, D15, G13)
# --------------------------------------------------------------------------

# Why each half-signal is stale, and what the human does about it. Each kind is a
# distinct condition with a distinct remedy — "stale" is never a single bucket,
# because an abandoned branch is a legitimate thing to RESUME and crash residue is
# a directory to delete.
WORKTREE_WITHOUT_BRANCH = "worktree-without-branch"
BRANCH_WITHOUT_WORKTREE = "branch-without-worktree"
WORKTREE_UNKNOWN_TO_GIT = "worktree-unknown-to-git"
WORKTREE_DIRECTORY_MISSING = "worktree-directory-missing"
NOT_A_SESSION_DIRECTORY = "not-a-session-directory"
# The three the joint signal itself can fail in (PR #49 review findings 5 and 6).
# Each is a DIFFERENT condition with a different remedy, which is why none of them
# is folded into `worktree-without-branch`: a worktree on the wrong branch is a
# human's shell to be put back, a detached one is an interrupted rebase/bisect,
# and ended residue is a teardown to finish.
WORKTREE_ON_ANOTHER_BRANCH = "worktree-on-another-branch"
WORKTREE_DETACHED = "worktree-detached"
ENDED_SESSION_RESIDUE = "ended-session-residue"


@dataclass(frozen=True)
class StaleSession:
    """One half-signal found under the sessions container: NOT a live session, and
    surfaced for the human-invoked cleanup rather than adopted, resurrected, or
    silently overwritten (FR-008). Nothing in the bootstrap deletes anything."""

    kind: str
    branch: str
    path: Path | None
    reason: str


@dataclass(frozen=True)
class SessionBootstrap:
    """What one process's re-derivation found. A RETURN VALUE, not a record: a
    session persists no descriptor (D10), so this is re-derived at every process
    start and never stored."""

    repository: str
    live: tuple[Any, ...] = ()
    stale: tuple[StaleSession, ...] = ()
    errors: tuple[str, ...] = ()

    @property
    def branches(self) -> tuple[str, ...]:
        return tuple(str(entry.ref) for entry in self.live)

    def summary(self) -> str:
        """The human-readable report FR-008 owes for the stale half-signals."""
        parts = [f"{len(self.live)} live branch session(s)"
                 + (f": {', '.join(self.branches)}" if self.live else "")]
        parts += [f"stale [{note.kind}] {note.reason}" for note in self.stale]
        parts += [f"error: {message}" for message in self.errors]
        return "; ".join(parts)


def _known_worktrees(git: SessionGit) -> set[Path]:
    """Every worktree git itself knows about, resolved. D10 names
    `git worktree list` as the session's derivation source, so this is the record's
    own signal rather than an inference from a directory listing."""
    return set(_worktree_records(git))


def _worktree_records(git: SessionGit) -> dict[Path, Any]:
    """`{resolved path: WorktreeRecord}` — git's own porcelain, whole.

    The record carries the BRANCH each worktree holds, which is the half of the
    joint signal (FR-008, G13) the previous path-only parse discarded (PR #49
    review finding 5)."""
    records: dict[Path, Any] = {}
    for record in git.worktree_records():
        try:
            records[Path(record.path).resolve()] = record
        except OSError:                               # pragma: no cover - defensive
            continue
    return records


def _git_holds_branch(git: SessionGit, worktree: Path, branch: str) -> bool:
    """Does git list THIS directory as a worktree ON THIS BRANCH?

    The joint signal, asked as one question instead of two independent ones. The
    adoption arm of `open_session` used to ask only whether git knew the directory
    (`_git_knows_worktree`) — co-presence, never agreement — so a worktree the
    human had `git checkout`-ed onto another branch, or left detached by an
    interrupted rebase, was adopted as the tile's session and the next gate action
    committed somewhere else entirely (FR-008, G13; reproduced)."""
    record = git.worktree_branch(worktree)
    return record is not None and record.branch == branch


def worktree_drift(git: SessionGit, worktree: Path, branch: str) -> str | None:
    """WHICH way the joint signal fails here, in the bootstrap's own vocabulary —
    or None when git lists this directory as a worktree on this branch.

    `_git_holds_branch` answers the yes/no the adoption arm needs; a REFUSAL owes
    the human the condition and its remedy, and the three conditions have three
    different remedies (put the checkout back / finish the rebase / prune)."""
    record = git.worktree_branch(worktree)
    if record is None:
        return WORKTREE_UNKNOWN_TO_GIT
    if record.detached or record.branch is None:
        return WORKTREE_DETACHED
    return None if record.branch == branch else WORKTREE_ON_ANOTHER_BRANCH


def assert_git_holds_branch(git: SessionGit, worktree: Path | str, branch: str,
                            *, during: str) -> None:
    """Refuse unless git itself lists `worktree` as a worktree ON `branch`.

    THE CHECK A REGISTRY CANNOT MAKE (PR #49 review finding 5, wave 2). A
    registry entry records the branch/worktree pairing ONCE, when the session
    opened, and nothing revokes it: a long-lived `serve` whose worktree the human
    then moved onto another branch — or an interrupted rebase left detached — kept
    joining the entry and authorizing writes, and the writes landed on whatever
    the directory held. Reproduced end to end: the commit and its FR-029 record
    went onto `somebody-elses-branch` while the record ATTESTED
    `ref: draft/demo-topic`, and `draft/demo-topic` never moved.

    Asked at the two points that matter, for two different reasons:

      * `open_session`'s registry JOIN, so the drift is reported BEFORE the verb's
        engine authors anything into the drifted directory;
      * `_commit_gate_action_locked`, inside the worktree's cross-process action
        lock and before any write — which is the actual GUARANTEE, because the
        drift can also happen in the window between the join and the commit, and
        because the CLI reaches the commit through the bootstrap rather than
        through that JOIN.

    Liveness stays REGISTRY-ONLY (FR-008, D10): git is asked to VALIDATE the
    entry the registry already answered with, never to find a session. This can
    only turn a join into a refusal — it can never make a dead session live, and
    it registers nothing."""
    kind = worktree_drift(git, Path(worktree), branch)
    if kind is None:
        return
    held = getattr(git.worktree_branch(Path(worktree)), "branch", None)
    raise SessionWorktreeDrifted(Path(worktree), branch, kind=kind, held=held,
                                 during=during)


def _session_directories(root: Path) -> tuple[list[Path], list[str]]:
    sessions = sessions_root(root)
    if not sessions.is_dir():
        return [], []
    try:
        # dot-directories are skipped: nothing in this feature creates one, and a
        # tool that does has not created a session worktree
        return sorted(p for p in sessions.iterdir()
                      if p.is_dir() and not p.name.startswith(".")), []
    except OSError as exc:
        return [], [str(exc)]


def live_session_branches_of(git: SessionGit, checkout_root: Path | str
                             ) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """EVERY live session branch on this checkout — `(branches, errors)`.

    The reconciliation half of the joint signal (add-session-notebook-
    reconciliation): `live_session_worktree` answers about ONE branch a caller
    already names, and the session-namespace sweep has no branch to name — it
    starts from notebook titles it cannot invert, so it must ask the checkout
    which sessions are live and compare forward.

    THE BRANCH COMES FROM GIT, never from the directory name. That is
    `bootstrap_sessions`'s own rule (PR #49 review finding 5): the flattened
    directory name is DISPLAY, and a worktree whose git branch disagrees with the
    name its directory claims is the two halves of the joint signal contradicting
    each other. Here such a directory simply contributes no branch — the sweep's
    question is "which sessions are live", and a contradiction is not one.

    ERRORS ARE RETURNED, NOT SWALLOWED, and that is the whole point of the pair.
    An unreadable container, a git failure, a checkout that is not a repository:
    each yields FEWER live branches, which to a sweep comparing forward is
    indistinguishable from sessions having ended. The caller MUST fail closed on a
    non-empty error tuple rather than retire what it could not account for — the
    difference is unrecoverable once a notebook is gone.
    """
    root = Path(checkout_root).resolve()
    directories, errors = _session_directories(root)
    if not directories:
        return (), tuple(errors)
    try:
        records = _worktree_records(git)
    except (SessionGitRefused, GitError, OSError) as exc:
        return (), (*errors, str(exc))
    live: list[str] = []
    for path in directories:
        record = records.get(path.resolve())
        if record is None or record.detached or not record.branch:
            continue
        branch = record.branch
        if not looks_ref_legal(branch) or flatten_branch(branch) != path.name:
            continue
        # the joint signal, asked through the ONE function that owns it
        if live_session_worktree(git, root, branch) is not None:
            live.append(branch)
    return tuple(sorted(set(live))), tuple(errors)


def live_session_worktree(git: SessionGit, checkout_root: Path | str,
                          branch: str) -> Path | None:
    """The worktree of the LIVE session on `branch`, or None — the joint signal
    for ONE branch, for a fresh process that holds no registry.

    The SAME rule `bootstrap_sessions` applies per directory, factored out so the
    projection tooling cannot invent a second one (PR #49 review finding 12):
    `sync-notebooklm-books.py --session-ref` tested `worktree.is_dir()` and
    NOTHING else, so against crash residue whose git association had been pruned
    AND whose branch had been deleted it happily returned a target and drove
    notebook create / re-sync / retire against a dead session — while
    `bootstrap_sessions`, handed the identical directory, answered `live=()` and
    reported it stale. FR-008 makes that bootstrap "the ONLY place either may be
    read as evidence of a session"; this is that same single exception, asked
    about one branch instead of all of them.

    Four conditions, all of them git's own answer or a durable marker, none of
    them a directory's mere existence: the directory is there, git lists it as a
    worktree ON THIS BRANCH, the branch exists, and no ending marker says the
    session is over (FR-021)."""
    try:
        worktree = worktree_path(checkout_root, branch)
    except SessionRefused:
        return None
    try:
        if not worktree.is_dir() or not _git_holds_branch(git, worktree, branch):
            return None
        if not git.branch_exists(branch):
            return None
    except (GitError, SessionGitRefused, OSError):
        return None
    if read_ending_marker(checkout_root, branch):
        return None
    return worktree


def bootstrap_sessions(registry: Any, *, repository: str,
                       checkout_root: Path | str, git: SessionGit | None = None,
                       generator: Any = None,
                       project_register: Path | str | None = None
                       ) -> SessionBootstrap:
    """Re-derive THIS PROCESS's live session entries — the ONE permitted exception
    to registry-only liveness (FR-008, D10, D15, G13; T033a).

    `SnapshotRegistry._entries` is an in-process dict, so every fresh process — the
    serve at start-up, and every CLI-parity verb, each its own process — begins
    with NO session entries. Without this re-derivation a restart would 404 the
    session ref, turn the next JOIN into a SECOND session on the same tile, re-fire
    the resume-or-new prompt mid-session, and let `propose` proceed over unmerged
    drafts: the exact hazard D15 exists to prevent.

    The rule is the joint one, and it is applied here and nowhere else: for every
    worktree present under the sessions container WHOSE BRANCH STILL EXISTS,
    re-register the `(repository, branch)` entry. Either signal alone is NOT a live
    session — a crash leaves a directory behind, and an abandoned branch survives
    its session by design (FR-022) — so each half-signal is reported STALE for the
    human-invoked cleanup and nothing here deletes, prunes, or resumes anything.

    Never fatal: a served tree with no git, no container, or an unreadable one has
    no sessions, and the caller comes up exactly as it did before sessions existed.
    """
    root = Path(checkout_root)
    live: list[Any] = []
    stale: list[StaleSession] = []
    errors: list[str] = []
    if not container_root(root).is_dir():
        # No worktree container means no session has ever been materialized against
        # this checkout: there is nothing to re-derive and nothing to report, so the
        # bootstrap costs a `stat` and runs no git at all. That matters because the
        # served image's `--checkout-root` is an empty sentinel and most callers are
        # not session users — a "not a git repository" note at every start-up would
        # be noise about a normal condition.
        return SessionBootstrap(str(repository))
    try:
        git = git or SessionGit(root)
        records = _worktree_records(git)
        known = set(records)
    except (SessionGitRefused, GitError, OSError) as exc:
        return SessionBootstrap(str(repository), (), (), (str(exc),))

    directories, listing_errors = _session_directories(root)
    errors += listing_errors
    claimed: set[str] = set()
    for path in directories:
        named = branch_from_worktree_dir(path)       # DISPLAY only (finding 5)
        record = records.get(path.resolve())
        if record is None:
            stale.append(StaleSession(
                WORKTREE_UNKNOWN_TO_GIT, named, path,
                f"{path} sits under the sessions container but `git worktree list` "
                f"does not know it, so it is not a materialized worktree of "
                f"{named!r} and is NOT live (FR-008, D10) — remove the directory"))
            continue
        # THE JOINT SIGNAL, verified rather than derived (FR-008, G13; PR #49
        # review finding 5). git is asked WHICH BRANCH this worktree holds, and
        # the directory must be that branch's own flattening — the forward
        # transform, which is a function, instead of the `__` inverse, which is
        # not (`draft/foo__bar` and `draft/foo/bar` share a directory name).
        if record.detached or not record.branch:
            stale.append(StaleSession(
                WORKTREE_DETACHED, named, path,
                f"{path} is a worktree with a DETACHED HEAD, so it holds no branch "
                "and the joint worktree+branch signal fails: it is NOT a live "
                "session (FR-008, D10). A commit made through it would be "
                "reachable from no ref at all — check the branch back out inside "
                f"{path}, or remove the directory and run `git worktree prune`"))
            continue
        branch = record.branch
        if not looks_ref_legal(branch):              # pragma: no cover - defensive
            stale.append(StaleSession(
                NOT_A_SESSION_DIRECTORY, branch, path,
                f"{path} sits under the sessions container but {branch!r} is not a "
                "legal session branch name, so it belongs to no session and is NOT "
                "live (FR-008) — remove the directory"))
            continue
        if flatten_branch(branch) != path.name:
            stale.append(StaleSession(
                WORKTREE_ON_ANOTHER_BRANCH, branch, path,
                f"the session worktree {path} is on branch {branch!r}, not on the "
                f"branch its directory names ({named!r}): the worktree and the "
                "branch are a JOINT signal and these two halves DISAGREE, so this "
                "is NOT a live session (FR-008, D10). Registering it would key the "
                "session on one branch while every commit landed on the other — "
                f"check {named!r} back out inside {path} (nothing here changes it)"))
            continue
        claimed.add(branch)
        if not git.branch_exists(branch):
            stale.append(StaleSession(
                WORKTREE_WITHOUT_BRANCH, branch, path,
                f"the sessions container holds {path} but branch {branch!r} does "
                "not exist: a worktree and its branch are a JOINT signal, so this "
                "is crash residue and NOT a live session (FR-008, D10) — remove "
                "the directory and run `git worktree prune`"))
            continue
        ended = read_ending_marker(root, branch)
        if ended:
            # FR-021: this session ALREADY ENDED and its teardown could not finish
            # (PR #49 review finding 6). Directory + branch is the live SHAPE, so
            # without this the ending was undone by the next process start.
            stale.append(StaleSession(
                ENDED_SESSION_RESIDUE, branch, path,
                f"the session on {branch!r} already ENDED "
                f"({ended.get('ending') or 'ending'}) and its teardown could not "
                f"finish: {'; '.join(ended.get('residue') or ()) or 'residue remains'}"
                ". A session ends ONCE (FR-021), so this is residue and NOT a live "
                "session however live it looks — remove the directory, run "
                "`git worktree prune`, and delete the branch if the ending was a "
                "MERGE (FR-033). "
                # The marker is NAMED, with its path (critic finding C7): it is
                # what makes this a residue report rather than a live session, and
                # a human told to clean up residue could not find the file that
                # generates the message. Finish the teardown FIRST — the marker is
                # the record of what is unfinished.
                f"This verdict comes from {ending_marker_path(root, branch)}, "
                f"which records the ending and its residue and is designed to "
                f"outlive the branch; delete it once the teardown above is "
                f"finished (any open/resume/new on this branch clears it too)"))
            continue
        # WHOSE session this is, read from the owner marker the OPEN left (finding
        # 6). The joint signal says a session is live; it cannot say which tile owns
        # it, and guessing from the ref hid a tile's own ordinal session behind a
        # sibling tile's name. None when there is no marker, which is the
        # pre-existing state and degrades to FR-026's tie-break.
        owner = read_owner_marker(root, branch)
        live.append(register_session_entry(
            registry, repository=repository, branch=branch, worktree=path,
            checkout_root=root, tile=Tile(*owner) if owner else None,
            # a session whose last action already generated its snapshot needs no
            # new answer at process start; a missing one is generated now
            regenerate=not session_snapshot_path(root, branch).is_file(),
            generator=generator, project_register=project_register,
            # the branch point rides the same marker the owner does; a session
            # opened before the marker carried it recovers from git's own fork
            # point against the default base (T104 R-12, advisory)
            session_base=(recovered := _recover_session_base(
                git, DEFAULT_BASE, branch, root)),
            # aliases can only come from the marker here: the snapshot has
            # regenerated since the open, so its CURRENT revision proves
            # nothing about what clients of that session hold (W-4)
            session_base_aliases=read_base_marker_aliases(root, branch)
            if recovered else ()))

    stale += _missing_worktree_directories(known, root)
    stale += _branches_without_worktrees(git, root, claimed, errors)
    return SessionBootstrap(str(repository), tuple(live), tuple(stale),
                            tuple(errors))


def _missing_worktree_directories(known: set[Path], root: Path
                                  ) -> list[StaleSession]:
    """Worktrees git still tracks under the sessions container whose DIRECTORY is
    gone — bookkeeping residue. Reported, never pruned here: pruning is a git write
    and a process start is not the place for one."""
    sessions = sessions_root(root).resolve()
    out: list[StaleSession] = []
    for path in sorted(known):
        if path == sessions or sessions not in path.parents or path.is_dir():
            continue
        out.append(StaleSession(
            WORKTREE_DIRECTORY_MISSING, branch_from_worktree_dir(path), path,
            f"git still tracks a session worktree at {path} whose directory is "
            "gone, so it is NOT live (FR-008) — run `git worktree prune`"))
    return out


def _branches_without_worktrees(git: SessionGit, root: Path, claimed: set[str],
                                errors: list[str]) -> list[StaleSession]:
    """Session-namespace branches with no worktree — the shape an ABANDONED
    session leaves behind (FR-022 deletes nothing at abandon time).

    Not live, and deliberately not touched: FR-025 offers the human RESUME or a new
    ordinal, and FR-028's branch cleanup is human-invoked once the topic's proposal
    exists. The report names both, so "stale" here never reads as "delete me"."""
    out: list[StaleSession] = []
    for namespace in SESSION_NAMESPACES:
        try:
            names = git.local_ordinals(f"{namespace}/")
        except (SessionGitRefused, GitError, OSError) as exc:
            errors.append(str(exc))
            continue
        for branch in names:
            if branch in claimed:
                continue
            try:
                path = worktree_path(root, branch)
            except SessionRefused:                   # pragma: no cover - defensive
                path = None
            out.append(StaleSession(
                BRANCH_WITHOUT_WORKTREE, branch, path,
                f"branch {branch!r} exists with no session worktree — the shape an "
                "ABANDONED session leaves behind. It is NOT live (FR-008): resume "
                "it, start a NEW session at the next ordinal (FR-025), or clean it "
                "up once the topic's proposal exists (FR-028). Nothing here "
                "deletes it"))
    return out


# --------------------------------------------------------------------------
# session TEARDOWN — the ONE mechanism BOTH endings use (T052; FR-021, G8)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class SessionTeardown:
    """What one teardown actually did. A RETURN VALUE, never a record: a session
    persists no descriptor (D10), and the durable artifact of an ending is the
    verb's own MAIN-RESIDENT gate-action record.

    `torn_down` lists only what was really removed, and `notes` carries every
    step that could not be — because the response is read as an audit line, and a
    response claiming a notebook nobody retired is a false one."""

    repository: str
    branch: str
    worktree: Path
    torn_down: tuple[str, ...] = ()
    branch_retained: bool = True
    branch_deleted: bool = False
    notes: tuple[str, ...] = ()
    main_view: dict | None = None


def notebook_degradation_notice(alias: str, branch: str, detail: str) -> str:
    """The FR-042 / D19 notice: the session is OPEN, it has no notebook, and here
    is the honest reason.

    The PHRASING is the requirement, not a nicety. Notebooks are per TILE (D2) and
    the NotebookLM account is SHARED, its quota spent by three competing
    populations — the three lifecycle books, every live `xf-wb-*` reference set,
    and every live `xf-session-*` session — so the count that matters is the
    number of CONCURRENT TILES ACROSS EVERYONE working in the workspace. A notice
    phrased as "you have too many sessions" would name a cause the human cannot
    act on and blame them for someone else's tiles, so nothing here attributes the
    limit to the reader. The adapter's own detail leads, verbatim, because when the
    cause is something else entirely (no `nlm` on PATH) that is what the human
    needs to read."""
    return (
        f"the session on {branch!r} is OPEN and fully usable; it just has no "
        f"NotebookLM notebook ({alias}): {detail}. Notebooks are per TILE and the "
        "NotebookLM account is SHARED: its quota is spent on the three lifecycle "
        "books plus every live reference-set (`xf-wb-*`) and session "
        "(`xf-session-*`) notebook, so the count scales with the CONCURRENT TILES "
        "ACROSS EVERYONE in the workspace. Retire a finished tile's notebook, then "
        "`python3 scripts/sync-notebooklm-books.py <workspace-root> --session-ref "
        f"{branch} --apply` gives this session one (FR-042, FR-040, D19).")


def notebook_deferred_sources_notice(alias: str, branch: str, *, deferred: int,
                                     total: int) -> str:
    """The finding-21 notice: this session HAS its notebook, the projection was
    BOUNDED, and here is the one command that completes it.

    A truncated projection reported as an unqualified success is the same class of
    dishonesty as a failed retire reported as "already gone": the human would open
    the notebook, see part of their corpus, and have no way to know whether that is
    all of it. So the count is named, the reason is named as a bound rather than a
    failure (nothing went wrong — a governed write is not allowed to wait on 176
    sequential `nlm` calls, D19 / plan Constraint 8), and the remedy is the SAME
    FR-040 re-sync every other notebook notice points at, which is unbounded off
    the request path and resumable because the diff is by content hash."""
    return (
        f"the session on {branch!r} has its NotebookLM notebook ({alias}), and its "
        f"source projection was BOUNDED: {total - deferred} of {total} governed "
        f"documents were projected and {deferred} were DEFERRED. Nothing failed — "
        f"the notebook is created inside a governed write, and that write does not "
        f"wait on one `nlm` call per document (D19). Complete it off the request "
        f"path, unbounded and resumably, with `python3 "
        f"scripts/sync-notebooklm-books.py <workspace-root> --session-ref "
        f"{branch} --apply` (FR-040, FR-042).")


def create_session_notebook(notebook: Any, alias: str,
                            documents: Sequence[tuple[str, str]] = ()) -> Any:
    """Create the session's notebook through the INJECTED adapter (FR-036, T074).

    Duck-typed and tried in contract order, exactly like `retire_session_notebook`:
    `create_session` is the session operation `contracts/session-ports.md` names
    (and what the `nlm`-backed `workbench.NotebookAdapter` grew in T073), and
    `create` is what a test double spells. Both take (alias, sources), so the seam
    works with either without the caller knowing which it holds. The RESULT is
    returned unexamined — the caller decides what a failure means, because on this
    path a failure is a DEGRADATION and never an error (FR-042)."""
    if notebook is None:
        return None
    for name in ("create_session", "create"):
        operation = getattr(notebook, name, None)
        if callable(operation):
            return operation(alias, tuple(documents))
    raise SessionRefused(
        f"the declared notebook adapter {type(notebook).__name__} exposes neither "
        "`create_session` nor `create`, so a session notebook cannot be created "
        "at open (FR-036)")


def _session_notebook_documents(worktree: Path | str, repository: str
                                ) -> list[tuple[str, str]]:
    """The worktree's governed documents, in the shape the notebook projection
    consumes. `workbench.session_documents` is the ONE membership rule — the same
    one `sync-notebooklm-books.py --session-ref` re-syncs from (FR-036, FR-039) —
    imported lazily so this module's import graph stays flat."""
    from . import workbench as wb

    return wb.session_documents(worktree, repository=repository)


def open_session_notebook(notebook: Any, *, alias: str, branch: str,
                          worktree: Path | str, repository: str
                          ) -> tuple[bool, str | None]:
    """Create the session's notebook at OPEN, degrading rather than blocking.

    Returns (created, notice). EVERY failure mode lands in the notice and none of
    them reaches the caller as an exception: the adapter may DEGRADE (an absent
    `nlm` returns `ok=False, skipped=True`) or RAISE (a full-quota double raising
    `QuotaExhausted`), the worktree scan may fail on unreadable bytes, and in all
    of those cases the session is already open and must stay open (FR-042, D19).
    With no adapter declared there is nothing to create and nothing to say."""
    if notebook is None:
        return False, None
    try:
        documents = _session_notebook_documents(worktree, repository)
        result = create_session_notebook(notebook, alias, documents)
    except Exception as exc:  # noqa: BLE001 - a notebook never blocks a session
        return False, notebook_degradation_notice(alias, branch, str(exc))
    ok = bool(getattr(result, "ok", True)) if result is not None else False
    skipped = bool(getattr(result, "skipped", False))
    if ok and not skipped:
        # A REBIND is not a create (PR #49 review finding 11): `created=False`
        # means the account already held a notebook under this alias, which for a
        # key-derived alias can only be residue from an earlier session on the
        # same branch. The session HAS a notebook either way — but a human whose
        # notebook already contains someone else's projection needs to be told,
        # not left to discover it in NotebookLM.
        if getattr(result, "created", True) is False:
            return True, (
                f"the session on {branch!r} REUSED an existing NotebookLM "
                f"notebook ({alias}) rather than creating one: the account "
                "already held that alias, which is residue from an earlier "
                "session on this same branch. Its sources have been re-synced "
                "from this worktree; nothing else was kept (FR-036, FR-037).")
        deferred = int(getattr(result, "sources_deferred", 0) or 0)
        if deferred:
            # created AND notified — the same shape as the rebind above: the
            # session has a notebook, and something about it the human must know
            return True, notebook_deferred_sources_notice(
                alias, branch, deferred=deferred,
                total=int(getattr(result, "sources_total", 0) or 0))
        return True, None
    detail = str(getattr(result, "detail", "") or "the adapter reported no notebook")
    return False, notebook_degradation_notice(alias, branch, detail)


def attach_session_notebook(session: SessionOpen) -> SessionOpen:
    """Create the notebook a `SessionOpen` is still CARRYING, and return the
    session with the outcome recorded on it (FR-036, FR-042; PR #49 finding 3).

    The open no longer creates it. A session OPEN is five durable artifacts —
    branch, worktree, registry entry, snapshot, notebook — and the notebook was
    the one with no local unwind: a refused first create left a real notebook on
    the SHARED NotebookLM account, spending the quota FR-042's notice is about,
    with nothing but the human's own `nlm` to reclaim it. Creating it after the
    action's commit has landed removes the leak by removing the window, and it
    also means the notebook is projected from a worktree that HOLDS the
    document rather than from an empty one.

    Idempotent-by-consumption: the adapter is dropped from the returned session,
    so a second call creates nothing. A JOIN carries no adapter at all — the
    notebook already exists, and re-projecting it on every gate action would be
    `nlm` traffic with no new answer (FR-040's re-sync is the refresh route)."""
    from dataclasses import replace

    if session is None or getattr(session, "pending_notebook", None) is None:
        return session
    # THE BIND IS OWNED (FR-037; PR #49 review finding 11). The alias is
    # key-derived and therefore injective, but a bind that would take an alias
    # another LIVE session already derives must fail LOUDLY rather than rebind
    # that session's notebook and delete its sources — which is exactly what the
    # non-injective derivation did silently. Checked here, at the one place a
    # session's notebook comes into existence.
    alias = notebook_alias(session.repository, session.branch)
    owner = session_alias_owner(
        getattr(session, "registry", None), alias,
        exclude=(session.repository, session.branch))
    if owner is not None:
        return replace(session, pending_notebook=None, notebook_created=False,
                       notebook_notice=notebook_alias_collision_notice(
                           alias, session.branch, owner))
    created, notice = open_session_notebook(
        session.pending_notebook, alias=alias,
        branch=session.branch, worktree=session.worktree,
        repository=session.repository)
    return replace(session, pending_notebook=None, notebook_created=created,
                   notebook_notice=notice)


def unwind_opened_session(git: SessionGit, session: SessionOpen | None, *,
                          checkout_root: Path | str | None = None,
                          base: str = DEFAULT_BASE) -> tuple[str, ...]:
    """Undo an OPEN whose gate action then REFUSED (FR-001, FR-021; PR #49
    review finding 3).

    A session open is a five-artifact durable side effect performed BEFORE the
    fallible gate write. Every refusal after it — an existing target
    (`SOURCE_EDIT`), an unwritable records tree, a git failure, a split write —
    used to return "nothing was persisted" while leaving a branch, a worktree, a
    live registry entry and a snapshot behind: a PHANTOM live session that
    blocked `propose` (FR-023), was re-derived live by the next process's
    bootstrap (FR-008), and made the create permanently unretryable, because the
    retry JOINed the phantom and refused on the same existing target again.

    TWO conditions, and both are refusals to act rather than best-effort cleanup:

      * the session must have been NEWLY OPENED by this call (`joined is False`).
        A refusal on a JOIN must leave the live session exactly as it was — the
        human's earlier work is in it, and the failing action is not its owner.
      * the branch must carry NO gate-action commit. One commit per gate action
        is the evidence series (FR-006, D18); a branch that already carries one
        is not this action's to delete, however it got there.

    AND THE EMPTINESS VERDICT IS COMPARE-AND-SWAPPED (PR #49 review finding 9's
    residual, wave 2). "Carries no commit" is read here and acted on two steps
    later by a `git worktree remove --force` plus a `git branch -D`, so a second
    actor's gate-action commit landing in that window used to be force-deleted with
    EMPTY notes — `git branch --contains <sha>` answering `<none>`, the object
    surviving only as unreferenced garbage, and the human told nothing. The tip is
    therefore observed BEFORE the emptiness read and carried into
    `teardown_session` as `expect_branch_sha`, which already enforces it before the
    first destructive step and again inside `delete_branch`. This is the same
    mechanism the merge ending uses (`reconcile_merged_session`) — the one
    neighbouring destructive site that did not use it.

    Returns the notes a caller appends to its refusal: what could not be undone
    is REPORTED, never swallowed, because residue the human does not know about
    is the defect this function exists to remove."""
    if session is None or session.joined:
        return ()
    try:
        # ORDER MATTERS: the tip first, then emptiness. A commit landing between
        # the two reads is caught by the emptiness guard below; one landing after
        # both is caught by the compare-and-swap. Reading the tip second would
        # leave the window this residual is about wide open, because the newer tip
        # would then be the value the swap expects. A `None` tip means the branch
        # is already gone, so there is no commit for the swap to protect.
        observed_tip = git.branch_sha(session.branch)
        ahead = git.commits_ahead(base, session.branch)
    except (GitError, SessionGitRefused, OSError) as exc:
        return (f"the session opened on {session.branch!r} could not be unwound: "
                f"whether it carries any commit could not be read ({exc}). The "
                f"branch and its worktree are still there — end it with "
                f"`abandon-session` if it is not wanted.",)
    if ahead:
        return (f"the session opened on {session.branch!r} was NOT unwound: it "
                f"already carries {ahead} gate-action commit(s), which are "
                f"recorded human actions and are not this refusal's to delete "
                f"(FR-006, D18).",)
    try:
        torn = teardown_session(
            git, session, checkout_root=checkout_root,
            registry=getattr(session, "registry", None),
            # nothing was created: the notebook is deferred to the first successful
            # commit, and this call means no commit ever landed
            notebook=None,
            # the branch was created by this open and carries nothing, so the
            # ordinary "an abandon deletes nothing" rule (FR-022, G9) does not
            # apply — there is no exploration here to keep evidence of
            delete_branch=True,
            # the emptiness verdict above, made enforceable at the destructive step
            expect_branch_sha=observed_tip,
            ending="a refused first gate action, unwound")
    except EndingNotDurable as exc:
        # FIRST, because it is a SessionRefused subclass and the compare-and-swap
        # arm below must not absorb it. This function REPORTS; it must never
        # replace the caller's own refusal with a different exception (finding 3's
        # contract, kept). An ending that could not be made durable tore nothing
        # down, so the honest note is that the session survives — which is exactly
        # what the caller's refusal text then tells the human, instead of claiming
        # a clean unwind (finding 6, wave 2).
        return (f"the session opened on {session.branch!r} could not be unwound: "
                f"its ending could not be made durable ({exc.reason}), and ending "
                "it without that would let a later process re-derive it as LIVE. "
                "The branch, its worktree and its registry entry are all still "
                f"there — make {exc.path.parent} writable, then end it with "
                "`abandon-session` if it is not wanted.",)
    except SessionRefused as exc:
        # The COMPARE-AND-SWAP failed: something landed on the branch after this
        # call read it as empty, and `teardown_session` refused before destroying
        # anything. This function REPORTS rather than raising (its contract, kept),
        # so the caller's own refusal carries the fact that the session survives —
        # the alternative was a silent force-delete of a commit reachable from no
        # ref (finding 9's residual).
        return (f"the session opened on {session.branch!r} was NOT unwound: it "
                f"read as carrying no commit and then MOVED before it could be "
                f"undone ({exc.report()}). Whatever landed is a recorded human "
                "action and is not this refusal's to delete (FR-006, FR-033), so "
                "the branch, its worktree and its registry entry are all still "
                "there.",)
    notes = tuple(note for note in torn.notes
                  if "notebook" not in note and "registry entry" not in note)
    if torn.branch_retained:
        notes += (f"the branch {session.branch!r} this refused action opened "
                  "could not be deleted and survives with no worktree; it is NOT "
                  "live (FR-008) and can be resumed or cleaned up (FR-025, "
                  "FR-028).",)
    return notes


def retire_session_notebook(notebook: Any, *, repository: str, branch: str
                            ) -> tuple[bool, str]:
    """Retire the session's notebook through the INJECTED adapter (FR-021, D16).

    RETIRED, never re-pointed at `main`: there is no surviving post-session
    notebook and no route to one in this feature (FR-036). The adapter is
    duck-typed on ONE operation, `retire` — the session operation
    `contracts/session-ports.md` names.

    THERE IS NO `delete` FALLBACK ANY MORE (PR #49 second-review tail B2). It was
    here because the `nlm`-backed adapter already exposed `delete`, and the
    docstring advertised that "the seam works with either" — but the two are not
    interchangeable in the direction that matters. `NotebookAdapter.delete` is the
    SCRATCH namespace's operation: no session prefix guard, no key-derived-title
    guard, a listing taken from `xf-wb-*`, and `missing_ok=True`. An injected
    adapter exposing only `delete` therefore reported `(True, "no notebook titled
    'xf-session-…' (already gone)")` while issuing no delete at all and leaving the
    session's notebook alive on the SHARED account holding that session's unmerged
    documents — precisely the leg-(b) false success that `missing_ok=False` closed
    on `retire`, left standing on the alternative. Nothing in the tree reaches it
    today (the real adapter has both, so `retire` always won), which is why it went
    unnoticed rather than why it was safe. An adapter without `retire` is now
    REFUSED, loudly, instead of silently reporting a retirement.

    THE TARGET IS DERIVED HERE, from the session's own (repository, branch) key,
    and the caller cannot name a title (PR #49 hardening item 2). The alias used
    to be a STRING ARGUMENT and the adapter deletes by TITLE MATCH, so any caller
    holding a stale, hand-built or collided alias could delete a notebook that was
    not this session's — on a SHARED account where the neighbouring titles are
    other people's live sessions. Deriving it from the key that identifies the
    session makes the wrong notebook unnameable rather than merely unlikely.

    RETURNS (retired, detail) — the ADAPTER'S verdict, not "I invoked something"
    (PR #49 review finding 13). It used to return `True` whenever an operation
    existed, so a failed `nlm notebook delete`, an unreadable notebook list and an
    absent `nlm` were all reported to `teardown_session` as a retired notebook and
    landed in the ending's `torn_down`. An adapter that reports no structured
    result at all (a test double whose `retire` returns None) is taken at its word
    only because it raised nothing; every real failure has a channel."""
    alias = notebook_alias(repository, branch)
    if notebook is None:
        return False, "no notebook adapter is declared"
    operation = getattr(notebook, "retire", None)
    if callable(operation):
        result = operation(alias)
        if result is None:
            return True, f"the notebook {alias!r} was retired"
        ok = bool(getattr(result, "ok", False))
        skipped = bool(getattr(result, "skipped", False))
        detail = str(getattr(result, "detail", "") or "the adapter reported "
                     "no outcome")
        return (ok and not skipped), detail
    raise SessionRefused(
        f"the declared notebook adapter {type(notebook).__name__} exposes no "
        "`retire`, so a session notebook cannot be retired at teardown "
        "(FR-021, D16). A scratch-namespace `delete` is NOT a substitute: it "
        "carries neither the session prefix guard nor the key-derived-title "
        "guard, reads the `xf-wb-*` listing, and treats an absent title as "
        "success — it would report this session's notebook retired while it "
        "survives on the shared account")


def refresh_main_view(registry: Any, *, repository: str,
                      checkout_root: Path | str, ref: str | None = None,
                      generator: Any = None,
                      project_register: Path | str | None = None) -> dict | None:
    """Regenerate the SHARED view after a session ends (FR-021's last clause).

    The session ref has just LEFT the registry's key space, so the surfaces that
    were offering it — the selector's roster, the funnel, the tile's own state —
    must be re-derived from the served checkout or the human is left looking at a
    view that still advertises a session nobody can reach. It runs through the
    registry's EXISTING regenerate binding, exactly as `refresh_session_snapshot`
    does for the worktree, so this is a CALLER of the one refresh mechanism and not
    a second one. Returns None when there is nothing regenerable (a served plane, a
    registry with no local `main` entry) — an absent shared snapshot is not an
    error, and it must never be the reason a session cannot end."""
    from .snapshot_registry import (
        BINDING_REGENERATE, DEFAULT_REF, SnapshotSource,
    )

    target = ref or DEFAULT_REF
    getter = getattr(registry, "get", None)
    entry = getter(repository, target) if getter is not None else None
    if entry is None or getattr(entry, "snapshot_path", None) is None:
        return None
    source = SnapshotSource(checkout_root=Path(checkout_root), generator=generator,
                            project_register=project_register)
    source.registry = registry
    if source.refresh_binding != BINDING_REGENERATE:
        return None
    return _preserving_active(
        registry, lambda: source.refresh(repository=repository, ref=target))


def teardown_session(git: SessionGit, session: SessionOpen, *,
                     checkout_root: Path | str | None = None,
                     registry: Any = None, notebook: Any = None,
                     delete_branch: bool = False,
                     delete_remote_branch: bool = False,
                     expect_branch_sha: str | None = None,
                     ending: str | None = None,
                     generator: Any = None,
                     project_register: Path | str | None = None
                     ) -> SessionTeardown:
    """End a session: registry entry, notebook, worktree, and the shared view —
    the ONE teardown BOTH endings use (FR-021, G8; T052).

    ORDER, and why each step is where it is:

      1. the REGISTRY ENTRY first, because liveness IS the entry (FR-008): the
         session is unambiguously over from that instant, and a later step failing
         cannot leave a LIVE entry pointing at a worktree that is already gone —
         which would 500 the session ref instead of 404-ing it.
      2. the NOTEBOOK, through the injected adapter (D16).
      3. the WORKTREE and its DERIVED SNAPSHOT — `unregister_session_entry`
         deliberately leaves the generated file for exactly this step, since
         dropping the entry is what makes a session non-live and deleting derived
         bytes is not.
      4. the BRANCH, only when the caller asks (`delete_branch`). The MERGE ending
         asks (FR-033); an ABANDON never does and never may (FR-022, G9) — the
         surviving branch is the evidence FR-028's human cleanup later disposes of.
      5. the SHARED VIEW refresh.

    Every step after the first is CONTAINED: a failure is reported in `notes` and
    the session still ends. A `git worktree remove` that cannot run leaves residue
    the T033a bootstrap already reports as stale with its own remedy, and that is a
    strictly better outcome than a session which cannot be ended at all.

    `expect_branch_sha` is the merge ending's COMPARE-AND-SWAP (FR-033; PR #49
    finding 9). Step 3 removes the worktree with `--force` and step 4 deletes the
    branch, so a verdict computed on a tip that has since moved must not authorize
    either: checked here, BEFORE the first destructive step, and again inside
    `delete_branch`. The abandon ending passes none — it ends the session on the
    human's own authority and destroys no branch."""
    registry = registry if registry is not None else getattr(session, "registry", None)
    root = Path(checkout_root) if checkout_root is not None \
        else Path(getattr(git, "served_root", "."))
    repository = session.repository
    branch = session.branch
    worktree = Path(session.worktree)
    torn: set[str] = set()
    notes: list[str] = []

    if expect_branch_sha is not None:
        current = git.branch_sha(branch)
        if current != expect_branch_sha:
            raise SessionRefused(
                f"refusing to tear down the session on {branch!r}: the decision to "
                f"end it was made with the branch at {expect_branch_sha} and it is "
                f"at {current} now. Removing the worktree and deleting the branch "
                "would make whatever landed in between unreachable from any ref, so "
                "nothing is torn down (FR-033).")

    # STEP 0 — MAKE THE ENDING DURABLE, before anything is destroyed (finding 6,
    # wave 2). The registry entry below is in-process, so the marker is the ONLY
    # thing a later process can read this ending from. It used to be written LAST,
    # best-effort, in exactly the world where it fails: the container that cannot
    # be written is the container whose worktree cannot be removed. So this is
    # first, and it RAISES — with nothing torn down yet, an ending that cannot be
    # made durable is a refusal over a session that is still live, rather than a
    # report of an ending that did not persist.
    #
    # Deliberately AFTER the compare-and-swap above: a teardown refused because the
    # tip moved never happened, and must not leave an ending marker behind.
    ending_word = ending or (ENDING_MERGE if delete_branch else ENDING_ABANDON)
    reserve_ending_marker(root, branch, ending=ending_word)
    # The session is ending, so its OWNER marker has nothing left to answer for
    # (finding 6). Dropped rather than kept: a surviving abandoned branch belongs to
    # no live session, and a RESUME writes the marker again from the tile resuming
    # it. Contained, like the write — a marker that outlives its session can only
    # ever say who the LAST session on this branch belonged to, and liveness is
    # still the registry entry.
    clear_owner_marker(root, branch)

    if registry is not None:
        was_live = is_live(registry, repository, branch)
        unregister_session_entry(registry, repository, branch)
        if was_live:
            torn.add(TORN_REGISTRY_ENTRY)
        else:
            notes.append(
                f"no registry entry was live for {repository}@{branch}, so the "
                "session was already non-live before this teardown (FR-008)")
    else:
        notes.append("no session registry was declared, so no liveness entry "
                     "could be dropped (FR-008)")

    if notebook is not None:
        # The alias is DERIVED from the session's key here, never taken from the
        # carried field, so a retire can only ever name this session's own
        # notebook (hardening item 2). A carried field that disagrees is itself
        # reportable: it means something built a SessionOpen whose alias is not
        # its key's, and silently deleting either notebook would be a guess.
        derived = notebook_alias(repository, branch)
        if str(session.notebook_alias or "") != derived:
            notes.append(
                f"the session carried the notebook alias "
                f"{session.notebook_alias!r} while its (repository, branch) key "
                f"derives {derived!r}; only the DERIVED alias was retired, "
                "because a title that is not this session's may be another live "
                "session's notebook (FR-037, D16)")
        try:
            retired, detail = retire_session_notebook(
                notebook, repository=repository, branch=branch)
            if retired:
                torn.add(TORN_NOTEBOOK)
            else:
                notes.append(f"the session notebook {derived!r} was NOT retired: "
                             f"{detail}")
        except Exception as exc:  # noqa: BLE001 - reported; never blocks an ending
            notes.append(f"the session notebook {derived!r} could "
                         f"not be retired: {exc}")
    else:
        notes.append("no session notebook adapter is declared on this plane, so "
                     "there was no session notebook to retire")

    if _git_knows_worktree(git, worktree) or worktree.is_dir():
        try:
            git.worktree_remove(worktree)
            torn.add(TORN_WORKTREE)
        except (GitError, SessionGitRefused, OSError) as exc:
            notes.append(f"the session worktree {worktree} could not be removed: "
                         f"{exc} — remove the directory and run "
                         "`git worktree prune`")
    else:
        notes.append(f"no session worktree was present at {worktree}")
    try:
        snapshot = session_snapshot_path(root, branch)
        if snapshot.is_file():
            snapshot.unlink()
    except (OSError, SessionRefused) as exc:
        notes.append(f"the session's derived snapshot could not be removed: {exc}")

    branch_deleted = False
    if delete_branch:
        try:
            # `expect_sha` re-checks the tip immediately before the irreversible
            # step, and `safe=` makes git itself re-verify containment when the
            # caller reached here through the MERGE observation (FR-033).
            git.delete_branch(branch, remote=delete_remote_branch,
                              expect_sha=expect_branch_sha,
                              safe=expect_branch_sha is not None)
            branch_deleted = True
        except (GitError, SessionGitRefused) as exc:
            notes.append(f"the session branch {branch!r} could not be deleted: {exc}")

    main_view = None
    if registry is not None:
        try:
            main_view = refresh_main_view(registry, repository=repository,
                                         checkout_root=root, generator=generator,
                                         project_register=project_register)
        except Exception as exc:  # noqa: BLE001 - reported; never blocks an ending
            notes.append(f"the main view could not be refreshed: {exc}")

    retained = False
    try:
        retained = git.branch_exists(branch)
    except (GitError, SessionGitRefused) as exc:     # pragma: no cover - defensive
        notes.append(f"whether {branch!r} survives could not be read: {exc}")

    # THE ENDING WAS DECIDED AT STEP 0, and is already durable there. What is left
    # here only ADDS information (finding 6, wave 2): a teardown that left residue
    # rewrites the reservation with the detail, and a teardown that completed
    # cleanly clears it. Both may be best-effort precisely BECAUSE the ending is
    # already recorded — if the rewrite fails, `read_ending_marker` still answers
    # "ended", so the attestation below stays true and only the detail is missing.
    residue = _teardown_residue(git, worktree, branch, retained,
                                delete_branch=delete_branch)
    if residue:
        try:
            write_ending_marker(root, branch,
                                # named by the CALLER when it knows better: the
                                # finding-3 unwind is an ending too, and calling it
                                # a merge would put a wrong word in the remedy
                                ending=ending_word, residue=residue)
        except EndingNotDurable as exc:
            # Honest, and NOT a claim the ending failed: step 0's reservation holds,
            # so the session stays ended for every later process — the human simply
            # does not get the residue list from the marker.
            notes.append(
                f"the residue detail could not be added to this ending's marker "
                f"({exc.reason}); the ending itself is recorded and holds, so "
                f"{branch!r} stays non-live — the residue is the one listed in "
                "these notes")
        notes.append(
            f"this ending left residue ({'; '.join(residue)}) and is recorded as "
            f"ENDED for every later process: {branch!r} is NOT live and will not "
            "be re-derived as live (FR-008, FR-021)")
    else:
        clear_ending_marker(root, branch)
    return SessionTeardown(
        repository=repository, branch=branch, worktree=worktree,
        torn_down=tuple(step for step in TEARDOWN_STEPS if step in torn),
        branch_retained=retained, branch_deleted=branch_deleted,
        notes=tuple(notes), main_view=main_view)


def _teardown_residue(git: SessionGit, worktree: Path, branch: str,
                      retained: bool, *, delete_branch: bool) -> tuple[str, ...]:
    """What this ending could NOT remove, in the words the human needs.

    Only the two signals a FRESH PROCESS can see are residue: the worktree
    directory (with or without git's bookkeeping) and — on the MERGE ending, which
    FR-033 says must delete it — the branch. The notebook and the snapshot are
    not: neither makes a session look live to the bootstrap."""
    residue: list[str] = []
    try:
        if worktree.is_dir() or _git_knows_worktree(git, worktree):
            residue.append(f"the session worktree {worktree} is still there")
    except (GitError, SessionGitRefused, OSError):   # pragma: no cover - defensive
        residue.append(f"whether {worktree} survives could not be read")
    if delete_branch and retained:
        residue.append(f"the merged branch {branch!r} was not deleted (FR-033)")
    return tuple(residue)


# --------------------------------------------------------------------------
# FR-033 — the MERGE ending: observe the merge, then end the session (T066)
#
# The merge itself is EXTERNAL. It is the Merge Master's action under the existing
# ritual, enforced outside this dashboard by branch protection, and no verb here
# holds the authority to perform it (FR-030). So the merge ending cannot be
# COMMANDED — it can only be OBSERVED, and the observation is what triggers it.
#
# The observation is git's own, and it has THREE parts (PR #49 review finding 9
# replaced the second — see the repair note at the tail of tasks.md, which supersedes
# Phase 7 realization note 2):
#
#   1. the base this checkout can SEE must be the base the merge would have
#      advanced. The merge happens on GitHub and moves the REMOTE `main`; a served
#      checkout that has not pulled still shows the pre-merge one, and answering
#      "not merged" from it made `open-pr` re-push the head branch the merge had
#      deleted. `remote_sha` reads it with `ls-remote` — side-effect-free, never a
#      `fetch` (FR-026, D17) — and a local base that does not contain it makes the
#      answer `base_stale`: reconcile nothing, push nothing, report why.
#      SCOPED to what it can actually hide (PR #49 critic finding C2): a stale base
#      hides a MERGE, and only a branch that has already LEFT this checkout can
#      have merged. On a shared served checkout "local `main` lags the remote" is
#      the steady state, so gating the FIRST save of a never-pushed session on it
#      refused the save verb in normal operation, with a merge narrative about a
#      branch no pull request had ever seen. `branch_remote_presence` is the
#      predicate: no remote head, no remote-tracking ref, and no dispatch the
#      caller knows of means the answer is a CONFIDENT "not merged", and the push
#      proceeds. The moment any of those exists, the stale base blocks both
#      answers again exactly as finding 9 requires.
#   2. the session branch's tip is an ancestor of the base. Ancestry alone is not
#      enough — a session opened with nothing written yet has a branch tip
#      IDENTICAL to `main`, which is trivially an ancestor of it.
#   3. a MERGE COMMIT on the base names that tip as a MERGED parent. This is the
#      part that used to be "and the two tips DIFFER", which an EMPTY session
#      satisfies as soon as the base moves for ANY unrelated reason: the review
#      reproduced a fresh session torn down and its branch deleted after one
#      unrelated commit on `main`. An empty branch's tip is a base commit, so it can
#      only ever appear as a merge's FIRST parent, never as a merged one — the shape
#      excludes it structurally instead of by luck.
#
# The shape it recognises is therefore precisely D18's: a MERGE COMMIT, never a
# squash and never a rebase. That is deliberate, not a limitation. A squash-landed
# or rebase-landed branch is NOT an ancestor of the base, so its session stays LIVE
# and visible — which SURFACES the D18 violation (the per-action commit series is
# FDA traceability evidence) instead of quietly disposing of the evidence that it
# happened. Nothing here changes a repository merge setting; that flip is out of
# scope (FR-035, plan Constraint 7).
#
# NO gate-action record is written by the reconciliation, for the same reason
# `cleanup-abandoned-branch` writes none: the schema has no `merge` action, and the
# durable audit of this branch's life is the MAIN-RESIDENT `open-pr` record, which
# names the branch and the pull request and OUTLIVES the branch — which is the
# whole reason FR-029 mandates that residence.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class MergeState:
    """Whether the base already contains this branch, and WHY that answer.
    `reason` is populated on both answers, because "not merged" is a thing a human
    reads and acts on.

    The observation's INPUTS are carried too, because the destruction it authorizes
    has to be a compare-and-swap: `tip` is the branch sha the verdict was computed
    from, and a delete that finds a different one refuses (PR #49 finding 9).
    `base_stale` is the third answer the type needed — "this checkout cannot tell",
    which must block the reconciliation AND the re-push rather than being reported
    as a confident "not merged"."""

    branch: str
    base: str
    merged: bool
    reason: str
    tip: str | None = None
    base_tip: str | None = None
    remote_base: str | None = None
    base_stale: bool = False
    landed_by: str | None = None
    # WHY this branch is known to have left this checkout (PR #49 critic finding
    # C2). It is the input the `base_stale` answer depends on — a stale base can
    # only hide a merge of a branch that was pushed — so that answer carries it;
    # None everywhere else, including on the confident "never pushed" answer,
    # whose whole content is that there is no such reason.
    remote_presence: str | None = None


def branch_remote_presence(git: SessionGit, branch: str, *,
                           dispatched: str | None = None) -> str | None:
    """WHY `branch` is known to have left this checkout, or None (PR #49 critic
    finding C2).

    A branch that has never been pushed cannot have a pull request, so it cannot
    have merged — which is what makes a stale base IRRELEVANT to its first save.
    Three signals, any one of which is proof of a dispatch, and each of them
    side-effect-free:

      * it is on the remote NOW (`ls-remote`, never a `fetch` — FR-026, D17);
      * a local remote-tracking ref for it exists, which `git push` wrote and
        nothing here prunes — so it survives the merge that DELETES the remote
        head, and that is precisely the case finding 9 is about;
      * `dispatched`, the caller's own durable evidence: a main-resident `open-pr`
        record or a pending-dispatch marker naming the branch. Passed in because
        those live in the records tree and the container, which this module's git
        seam does not read.

    A git read that FAILS answers "presence" rather than "absence": the whole point
    is to be sure a re-push cannot resurrect a merged head branch, and an
    unanswerable remote is not that assurance."""
    if dispatched:
        return dispatched
    try:
        if git.remote_sha(branch):
            return (f"{branch!r} is on the remote now, so it has been pushed and "
                    "may already carry a pull request")
        if git.tracking_sha(branch):
            return (f"this checkout holds a remote-tracking ref for {branch!r}, so "
                    "it HAS been pushed from here — and a merge that deleted the "
                    "remote head would leave exactly this trace")
    except (GitError, SessionGitRefused, OSError) as exc:
        return (f"whether {branch!r} has been pushed could not be read ({exc}), "
                "which is not the assurance a re-push needs")
    return None


def merge_state(git: SessionGit, branch: str, *, base: str = DEFAULT_BASE,
                dispatched: str | None = None) -> MergeState:
    """Observe whether `branch` has been merged into `base` (FR-033).

    THREE answers, not two, and the order is the point (PR #49 finding 9, all four
    arms reproduced):

      1. **the base this checkout can see may not be the base the merge advanced.**
         The merge happens on GitHub: it moves the REMOTE `main`, and a served
         checkout that has not pulled still shows the pre-merge one. Reading only
         the local ref answered "not merged" about a branch that HAD merged, and
         `open-pr` then re-pushed the head branch the merge had deleted. So the
         remote base is read first — with `ls-remote --heads`, side-effect-free,
         never a `fetch` (FR-026, D17) — and a local base that does not CONTAIN it
         makes the answer `base_stale`: reconcile nothing, push nothing, say so.
         But ONLY for a branch that could have landed (critic finding C2): a
         stale base hides a merge, a merge needs a pull request, and a pull
         request needs a push. With no remote head, no remote-tracking ref and no
         `dispatched` evidence, "not merged" is a CONFIDENT answer rather than an
         unavailable one, and the first save of a never-pushed session is not
         held hostage to a shared checkout's steady state.
      2. **containment**: `base` must contain the branch's tip. A squash- or
         rebase-landed branch is not contained, so its session stays live and
         VISIBLE, which surfaces the D18 violation instead of disposing of the
         evidence that it happened.
      3. **the landing itself**: a merge commit on `base` whose merged parent IS
         this branch's tip. This replaces the old "and the tips differ" half, which
         an EMPTY session satisfied as soon as the base moved for ANY unrelated
         reason — reproduced: one unrelated commit on `main` made a session that had
         written nothing look merged, and the reconciliation deleted its branch and
         force-removed its worktree.

    A git read that cannot answer is answered as NOT merged — a false negative
    leaves a session live and reportable, while a false positive deletes work."""
    try:
        if not git.branch_exists(branch):
            return MergeState(branch, base, False,
                              f"branch {branch!r} does not exist, so there is "
                              "nothing to reconcile")
        tip = git.head(ref=branch)
        base_tip = git.head(ref=base)
        remote_base = git.remote_sha(base)
        if remote_base and remote_base != base_tip and not (
                git.has_object(remote_base)
                and git.is_ancestor(remote_base, base)):
            # Asked HERE and not above: it is the only answer that depends on it,
            # and it costs a second `ls-remote` round trip on a base that is
            # usually fresh.
            presence = branch_remote_presence(git, branch, dispatched=dispatched)
            # The remedy is NAMED, with the commands, because it is the one step
            # the merge ending cannot perform for the human (critic finding C5):
            # the runbook promised reconciliation "on the next `open-pr`" while
            # this refusal was the only place the pull was mentioned at all.
            served = getattr(git, "served_root", "<the served checkout>")
            remote = getattr(git, "remote", DEFAULT_REMOTE)
            if not presence:
                # The base this checkout can see is behind the remote's, and that
                # is the NORMAL state of a shared served checkout. It cannot hide
                # anything about THIS branch, though: nothing has ever pushed it,
                # so no pull request exists to have merged, and a push cannot
                # resurrect a head branch no merge has ever seen (critic C2).
                return MergeState(
                    branch, base, False,
                    f"{branch!r} has never left this checkout — it is not on the "
                    f"remote, no remote-tracking ref for it exists, and no "
                    f"`open-pr` record or pending dispatch names it — so no pull "
                    f"request can have merged it. The served checkout's {base} is "
                    f"at {base_tip} and the remote's at {remote_base}, which this "
                    f"checkout does not contain, but a base it cannot see cannot "
                    f"hide a merge that could not have happened: the session is "
                    f"NOT merged, nothing is reconciled, and the first save "
                    f"proceeds (FR-029, FR-033)",
                    tip=tip, base_tip=base_tip, remote_base=remote_base)
            return MergeState(
                branch, base, False,
                f"the served checkout's {base} is at {base_tip} but the remote's is "
                f"at {remote_base}, which this checkout does not contain: the base "
                f"the merge would have advanced is NOT the base visible here, so "
                f"whether {branch!r} merged cannot be observed — and it COULD have: "
                f"{presence}. Nothing is "
                f"reconciled and nothing is pushed — a re-push would resurrect a "
                f"head branch the merge may already have deleted, and a teardown "
                f"would delete a branch on a guess. UPDATE THE SERVED CHECKOUT "
                f"FIRST, in your own shell — `git -C {served} fetch {remote} "
                f"{base}` then `git -C {served} merge --ff-only {remote}/{base}` "
                f"— and run this save again: it then observes the merge and "
                f"reconciles the session. That pull is a NAMED, MANDATORY step of "
                f"the merge ending (`docs/ideation-dashboard-session-runbook.md` "
                f"§6), not a workaround: it is a human action outside this "
                f"dashboard because no session operation fetches (FR-026/D17).",
                tip=tip, base_tip=base_tip, remote_base=remote_base,
                base_stale=True, remote_presence=presence)
        if not git.is_ancestor(branch, base):
            return MergeState(
                branch, base, False,
                f"{base} does not contain {branch!r}'s tip, so its pull request "
                f"has not merged as a MERGE COMMIT. A session PR lands with a "
                f"merge commit and never a squash — the per-action commit series "
                f"is traceability evidence (D18) — so a squashed or rebased "
                f"landing leaves this session live and visible on purpose",
                tip=tip, base_tip=base_tip, remote_base=remote_base)
        landed_by = git.merge_landing(base, branch)
        if landed_by is None:
            if tip == base_tip:
                return MergeState(
                    branch, base, False,
                    f"{branch!r} and {base} are at the same commit: nothing has been "
                    "merged, this session has simply written nothing yet",
                    tip=tip, base_tip=base_tip, remote_base=remote_base)
            return MergeState(
                branch, base, False,
                f"{base} contains {branch!r}'s tip, but NO merge commit on {base} "
                f"names that tip as a merged parent — so this branch's commits are "
                f"in {base} without this branch having been merged into it (an empty "
                f"session whose base moved on, or a fast-forward/rebase landing). "
                f"Ending a session on that evidence would delete a branch nobody "
                f"merged, so it stays live and visible (FR-033, D18)",
                tip=tip, base_tip=base_tip, remote_base=remote_base)
    except (GitError, SessionGitRefused, OSError) as exc:
        return MergeState(branch, base, False,
                          f"whether {base} contains {branch!r} could not be read: "
                          f"{exc}")
    return MergeState(
        branch, base, True,
        f"{base} contains {branch!r}'s tip ({tip}) as a merged parent of merge "
        f"commit {landed_by}: the pull request merged as a merge commit (D18)",
        tip=tip, base_tip=base_tip, remote_base=remote_base, landed_by=landed_by)


@dataclass(frozen=True)
class MergeReconciliation:
    """What one reconciliation observed and did. A RETURN VALUE, never a record
    (D10): the durable audit is the MAIN-RESIDENT `open-pr` record."""

    repository: str
    branch: str
    merged: bool
    reason: str
    teardown: SessionTeardown | None = None


def reconcile_merged_session(git: SessionGit, session: SessionOpen, *,
                             checkout_root: Path | str | None = None,
                             base: str = DEFAULT_BASE, registry: Any = None,
                             notebook: Any = None,
                             delete_remote_branch: bool | None = None,
                             generator: Any = None,
                             project_register: Path | str | None = None
                             ) -> MergeReconciliation:
    """The MERGE ending (FR-033, G10): if — and only if — the base already contains
    the session's branch, end the session, DELETE the branch, and refresh the main
    view.

    It OBSERVES; it never asserts. A session whose pull request has not merged is
    left exactly as it was, with the reason reported: ending an unmerged session is
    `abandon-session`'s authority (FR-022) and this path holds none.

    The ending itself is `teardown_session` — the ONE mechanism both endings use
    (FR-021, G8) — called with `delete_branch=True`, which is the single thing that
    distinguishes the merge ending from the abandon ending. The main-view refresh
    is that teardown's last step, so it is not re-implemented here either.

    `delete_remote_branch` defaults to "only if the branch is actually on the
    remote": a session that never reached `open-pr` has no remote copy, and asking
    git to delete one would produce a note about a condition that is normal.

    OBSERVATION IS AUTHORITATIVE BEFORE ANYTHING IS DESTROYED (PR #49 finding 9).
    The teardown force-removes a worktree and deletes a branch, so between deciding
    and destroying there are three proofs, all of them prerequisites rather than
    afterthoughts:

      1. the verdict itself must be a real merge-commit landing, and not computed
         from a base this checkout cannot see (`merge_state`, above);
      2. the session worktree must hold NO uncommitted work. A merged session's
         worktree is clean; one that is not is holding drafting that `git worktree
         remove --force` would delete with no recovery path (reproduced), so this
         refuses and names the two routes that do not lose it;
      3. the verdict is RE-OBSERVED immediately before the teardown, and the tip it
         was computed from is carried into the branch delete as a compare-and-swap —
         a gate-action commit that landed after the first observation aborts the
         ending instead of being erased."""
    root = Path(checkout_root) if checkout_root is not None \
        else Path(getattr(git, "served_root", "."))
    state = merge_state(git, session.branch, base=base)
    if not state.merged:
        return MergeReconciliation(session.repository, session.branch, False,
                                   state.reason)
    _refuse_reconciling_over_uncommitted_work(git, session, state)
    # RE-OBSERVE: the first observation may be arbitrarily old by now (a threaded
    # server, a CLI process beside it), and everything below is irreversible.
    confirmed = merge_state(git, session.branch, base=base)
    if not confirmed.merged or confirmed.tip != state.tip:
        raise SessionRefused(
            f"refusing to end the session on {session.branch!r}: it was "
            f"{state.tip} when the merge was observed and the observation no longer "
            f"holds ({confirmed.reason}). Something landed on the branch after the "
            "merge was seen, and ending the session now would delete a worktree and "
            "a branch carrying work nothing has merged (FR-033). Save the new work "
            "with `open-pr` — it needs its own pull request — and the session ends "
            "when THAT merges.")
    if delete_remote_branch is None:
        try:
            # an EXACT membership test over the prefix scan `remote_ordinals`
            # already performs — side-effect-free, and never a `git fetch`
            delete_remote_branch = session.branch in git.remote_ordinals(
                session.branch)
        except (GitError, SessionGitRefused, OSError):
            delete_remote_branch = False
    torn = teardown_session(
        git, session, checkout_root=root, registry=registry, notebook=notebook,
        # the ONE difference between the two endings (FR-033 vs FR-022, G9/G10)
        delete_branch=True, delete_remote_branch=delete_remote_branch,
        # the compare-and-swap: the tip the verdict was computed from
        expect_branch_sha=confirmed.tip,
        generator=generator, project_register=project_register)
    return MergeReconciliation(session.repository, session.branch, True,
                               state.reason, torn)


def _refuse_reconciling_over_uncommitted_work(git: SessionGit, session: Any,
                                              state: MergeState) -> None:
    """A merged session whose worktree still holds uncommitted work is NOT ended.

    The teardown's `git worktree remove --force` deletes the directory outright, and
    the review reproduced an in-progress document destroyed exactly that way. The
    merge ending has no authority to discard drafting — `abandon-session` is the verb
    that does (FR-022), and it is named here — so the refusal is the safe answer and
    the session stays live and visible until a human decides."""
    worktree = Path(session.worktree)
    if not worktree.is_dir():
        return
    try:
        dirty = tuple(sorted(set(git.dirty_paths(worktree))))
    except (GitError, SessionGitRefused, OSError) as exc:   # pragma: no cover
        raise SessionRefused(
            f"refusing to end the session on {session.branch!r}: whether its "
            f"worktree {worktree} holds uncommitted work could not be read ({exc}), "
            "and the ending removes that worktree with `--force` (FR-033)") from exc
    if not dirty:
        return
    raise SessionRefused(
        f"the pull request for {session.branch!r} has merged, but its worktree "
        f"{worktree} still holds uncommitted work: {', '.join(dirty)}. Ending the "
        "session removes that worktree with `--force` and deletes the branch, which "
        "would destroy this work with no way to get it back (FR-033), so the ending "
        "refuses. Either commit it with a gate action and save it — it needs its own "
        "pull request, because this branch has already merged — or discard it "
        "deliberately with `abandon-session` (FR-022, the one verb that holds that "
        "authority).")


# --------------------------------------------------------------------------
# FR-028 — the human-invoked cleanup of an ABANDONED session's branch
# --------------------------------------------------------------------------

def abandon_records_for(checkout_root: Path | str, branch: str, *,
                        records_dir: str = gate_console.DEFAULT_RECORDS_DIR
                        ) -> tuple[Path, ...]:
    """Every MAIN-RESIDENT `abandon-session` gate-action record naming `branch`.

    The record's residence is what makes this readable at all: FR-022 puts it in
    the SERVED checkout's records tree precisely so it OUTLIVES the branch
    (plan Constraint 10). The `target.ref` is verified rather than inferred from
    the folder name, because `ref_target_id` is a slug and two refs can slug the
    same — a cleanup must not read another ref's abandon as this one's."""
    folder = (Path(checkout_root) / gate_console._prefix(records_dir)
              / gate_console.ref_target_id(branch))
    if not folder.is_dir():
        return ()
    found: list[Path] = []
    for path in sorted(folder.glob(
            f"{gate_console.ACTION_ABANDON_SESSION}-*.gate-action.yaml")):
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(loaded, Mapping):
            continue
        target = loaded.get("target")
        if isinstance(target, Mapping) and str(target.get("ref") or "") == branch:
            found.append(path)
    return tuple(found)


def abandon_proof(checkout_root: Path | str, branch: str, *,
                  records_dir: str = gate_console.DEFAULT_RECORDS_DIR
                  ) -> str | None:
    """WHY this branch's session is known to have been ABANDONED, or None
    (PR #49 second-review finding 3).

    Two admissible proofs, and both are durable by design — which is the point,
    because the thing they authorize is the deletion of the branch that carries
    the session's whole gate-action commit series (D18, FR-006):

      1. a MAIN-RESIDENT `abandon-session` record naming the ref. FR-022 puts it
         on `main` exactly so it survives this delete, and it carries the human's
         recorded reason.
      2. the durable ENDING MARKER saying `abandon`. It lives in the gitignored
         container, outlives the branch, and exists for the ending whose cleanup
         could not finish — the very case where a record write may have been the
         step that failed.

    ABSENCE OF LIVENESS IS NOT A PROOF and never becomes one. A crash, or a human
    following the stale-worktree remedy this module itself prints ("remove the
    directory and run `git worktree prune`"), makes a LIVE session non-live with
    nothing ended and nothing recorded — and the delete would then take the only
    copy of the evidence with it, while both surfaces attested that "the abandon
    record on `main` survives it"."""
    records = abandon_records_for(checkout_root, branch, records_dir=records_dir)
    if records:
        rel = records[-1].name
        return (f"its MAIN-RESIDENT `abandon-session` record {rel} names this ref, "
                "carries the recorded reason, and outlives this delete (FR-022)")
    marker = read_ending_marker(checkout_root, branch)
    if marker and str(marker.get("ending") or "") == ENDING_ABANDON:
        return (f"the durable ending marker "
                f"{ending_marker_path(checkout_root, branch).name} records "
                f"ending={ENDING_ABANDON!r} for this branch (FR-021)")
    return None


def assert_branch_cleanup_permitted(git: SessionGit, registry: Any, *,
                                    repository: str, tile: "Tile", branch: str,
                                    proposal: ProposalState | None,
                                    checkout_root: Path | str,
                                    inventory: TileInventory | None = None,
                                    records_dir: str = gate_console.DEFAULT_RECORDS_DIR
                                    ) -> str:
    """The FIVE preconditions of FR-028's cleanup, in the order they answer the
    human's question. Every one of them persists nothing. RETURNS the proof that
    the session was abandoned, so the caller reports what was verified instead of
    asserting it (PR #49 second-review finding 3).

      1. the branch is THIS TILE's (base or ordinal family, another tile's
         deterministic name EXCLUDED — G12). Deleting a branch on behalf of a tile
         that does not own it is the same defect as joining another tile's session.
      2. the topic's PROPOSAL EXISTS. Until then the retention window is open: an
         abandoned branch is the only surviving evidence of the exploration, and
         the reconciliation D17 describes reads it.
      3. a `propose` DISPATCH alone is NOT a proposal (the sharp clause): the
         commissioned authoring may never deliver one, so a dispatch must never
         make a branch deletable — and it must certainly never delete it.
      4. the session is not LIVE, and no worktree is attached. The affordance is
         offered for an ABANDONED session's branch; a live session's branch is
         deleted by nobody, and a branch with a worktree would leave that worktree
         broken (git would refuse the delete anyway, less legibly).
      5. the session WAS ABANDONED, proved by `abandon_proof` (PR #49
         second-review finding 3). The four preconditions above are all satisfied
         by a session that simply CRASHED — or by a human following the
         stale-worktree remedy this module prints — so the verb deleted the
         branch carrying the tile's entire gate-action commit series, which D18
         and FR-006 call the traceability evidence, leaving no record of the
         session anywhere while both surfaces attested "the abandon record on
         `main` survives it". Not-live is not abandoned, and this is the
         precondition that says so; contracts/gate-routes.md:207 requires the
         409 it raises."""
    inventory = inventory if inventory is not None else TileInventory((tile,))
    if tile not in inventory.tiles:
        inventory = TileInventory((*inventory.tiles, tile))
    base = tile.branch
    family = tile_branch_family([branch], base,
                               excluded=inventory.other_branches(tile))
    if not family:
        raise SessionRefused(
            f"{branch!r} is not a session branch of tile {tile.scope_id!r} "
            f"({tile.scope_kind}), whose branches are {base!r} and its ordinal "
            "forms. A cleanup deletes the tile's OWN abandoned branch and nothing "
            "else — another tile's branch is that tile's to resolve (FR-028, "
            "FR-002, G12).")
    if proposal is None or not proposal.proposal_id:
        if proposal is not None and proposal.dispatch_in_flight:
            raise SessionRefused(
                f"no cleanup of {branch!r}: a `propose` commission for tile "
                f"{tile.scope_id!r} was dispatched and the proposal has not landed "
                "yet. A dispatch is a commission, not a proposal — the authoring "
                "may never deliver one, so the branch is retained until it does "
                "(FR-028).")
        raise SessionRefused(
            f"no cleanup of {branch!r}: tile {tile.scope_id!r} carries no proposal "
            "yet, so the retention window is still open — the abandoned branch is "
            "the surviving evidence of that exploration until a proposal exists "
            "(FR-028).")
    if is_live(registry, repository, branch):
        raise SessionRefused(
            f"no cleanup of {branch!r}: a branch session is LIVE on it. The "
            "cleanup is offered for an ABANDONED session's branch — end the "
            "session first (`open-pr` and merge, or `abandon-session`), and the "
            "branch becomes eligible afterwards (FR-028, FR-022).")
    if not git.branch_exists(branch):
        raise SessionRefused(
            f"no cleanup of {branch!r}: no such branch exists in this checkout, so "
            "there is nothing to delete (FR-028).")
    worktree = worktree_path(checkout_root, branch)
    if worktree.is_dir() or _git_knows_worktree(git, worktree):
        raise SessionRefused(
            f"no cleanup of {branch!r}: a session worktree is still attached at "
            f"{worktree}. An ABANDONED session's branch has no worktree — this is "
            "either a live session this process cannot see or crash residue, so "
            "remove the directory and run `git worktree prune` first (FR-028, "
            "FR-008).")
    proof = abandon_proof(checkout_root, branch, records_dir=records_dir)
    if proof is None:
        raise SessionRefused(
            f"no cleanup of {branch!r}: NOTHING records that its session was "
            f"ABANDONED. This verb deletes the branch and writes no record of its "
            f"own — the durable audit is the MAIN-RESIDENT `abandon-session` "
            f"record — so with neither that record nor a `{ENDING_SUBDIR}` marker "
            f"saying {ENDING_ABANDON!r}, the delete would take the tile's whole "
            f"gate-action commit series with it and leave ZERO trace of the "
            f"session (FR-022, FR-028, FR-006, D18). A session that is merely "
            f"NOT LIVE was not abandoned: a crash, or the stale-worktree remedy "
            f"('remove the directory and run `git worktree prune`'), leaves "
            f"exactly this state. If the session is over, end it through "
            f"`abandon-session`, which records WHY and makes the branch eligible; "
            f"if this is residue of a session that was never ended, that is what "
            f"it is — stale residue, and deleting the evidence is not this verb's "
            f"authority.")
    return proof


# --------------------------------------------------------------------------
# the commit-per-gate-action write path (T015; FR-006, chg 2.6)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class GateActionCommit:
    """What ONE file-producing gate action produced. `sha` is RETURNED to the
    caller for the route / CLI response and is never written into the record —
    a commit cannot contain its own sha (FR-006)."""

    sha: str
    stamp: str
    branch: str
    record_path: Path            # absolute, inside the worktree
    record_relpath: str          # repo-relative, as the commit records it
    documents: tuple[str, ...]   # repo-relative, as the commit records them
    record: dict
    message: str
    # The freshness of the session snapshot this action regenerated (FR-010), or
    # None when no registry was declared or the projection could not be built.
    snapshot: dict | None = None
    # The session, as it stands AFTER this commit: the same object on every path
    # except the one where this commit was the first on a freshly opened session,
    # where the deferred notebook is created and recorded on it (FR-036, FR-042;
    # PR #49 finding 3). Callers read `notebook_notice` from here.
    session: Any = None


def action_stamp(at: str) -> str:
    """The action id: the `<stamp>` already in the record's filename. The
    commit message repeats it as a `Gate-Action: <stamp>` trailer, and the
    record's `commit`-kind artifact references it (FR-006)."""
    return gate_console._stamp(at)


def commit_message(action: str, stamp: str, *, summary: str | None = None) -> str:
    """One gate action, one commit, with the action id as a message TRAILER so a
    reader can walk from the record to its commit and back (FR-006)."""
    head = summary or f"{action}: session gate action"
    return f"{head}\n\nGate-Action: {stamp}\n"


def commit_artifact(stamp: str) -> dict:
    """The record's `commit`-kind artifact. Its `reference` is the ACTION ID, not
    a sha, and its resolution is DEFINED rather than literal: the referenced
    commit is the one that INTRODUCED the record file on the session branch
    (`git log --diff-filter=A -- <record-path>`), which is the action's own
    commit and, immediately after the action, the branch TIP. openxFactory's
    `gate-action-record` schema requires only `{kind, reference}`, and a
    resolvable reference satisfies it (data-model SessionCommit)."""
    return {"kind": gate_console.ART_COMMIT, "reference": stamp}


def _refuse_embedded_sha(record: Mapping[str, Any], stamp: str) -> None:
    for artifact in record.get("artifacts") or []:
        if not isinstance(artifact, Mapping):
            continue
        if artifact.get("kind") != gate_console.ART_COMMIT:
            continue
        reference = str(artifact.get("reference") or "")
        if reference != stamp:
            raise SessionRefused(
                f"a session record's commit artifact must reference its own "
                f"action stamp ({stamp!r}), not {reference!r}: a commit cannot "
                "contain its own sha, and the amend-then-restamp dance leaves "
                "the record naming a pre-amend sha the amend made unreachable "
                "(FR-006)")
        # THE SECOND ARM GUARDS THE STAMP, NOT THE REFERENCE (PR #49 second-review
        # tail B1). It used to re-test `reference` against `_SHA_RE` — but this
        # line is only reachable once `reference == stamp`, so it was never a
        # statement about the reference: it was a statement about the STAMP's
        # shape, made in the wrong place, and it could only ever be WRONG. With
        # the production `at` (`gate_console._utcnow()`) the stamp is
        # `20260727T152133Z`, which is not hex, so the arm was dead; with a
        # date-only `at` the stamp is `20260726`, which IS hex-shaped, so a
        # CORRECTLY formed record naming its own stamp was refused as "looks like
        # a sha". Asked of the stamp, the same intent is well-founded and
        # reachable: a stamp that could be mistaken for an abbreviated sha is not
        # a resolvable action id, and the introduced-by rule (FR-006) needs one.
        if not _ACTION_STAMP_RE.match(stamp):
            raise SessionRefused(
                f"the action stamp {stamp!r} is not a full action stamp "
                f"(YYYYMMDDTHHMMSSZ), so a commit artifact referencing it is "
                f"indistinguishable from an abbreviated sha "
                f"({'hex-shaped' if _SHA_RE.match(stamp) else 'unresolvable'}): "
                "the reference is the action id, resolved by the introduced-by "
                "rule, and a sha would name a commit the amend-then-restamp dance "
                "can make unreachable (FR-006)")


def _refuse_missing_commit_artifact(record: Mapping[str, Any], stamp: str) -> None:
    """A file-producing action's record MUST CARRY a `commit` artifact (PR #49
    tail finding B4).

    `_refuse_embedded_sha` validates every `commit` artifact that is PRESENT and
    never that one exists, and the enumerated refusals had no presence check — so
    an `edit-document` record whose only artifact was, say, an `other` reference to
    the document was accepted and COMMITTED onto the session branch, where the
    pinned openxFactory validator rejects it (`artifacts: ... does not contain items
    matching the given schema`, reproduced). That is a schema-invalid governance
    record permanently on the branch spec.md declares FDA traceability evidence,
    and the introduced-by chain FR-006 depends on has nothing to resolve."""
    for artifact in record.get("artifacts") or []:
        if isinstance(artifact, Mapping) and \
                artifact.get("kind") == gate_console.ART_COMMIT:
            return
    kinds = sorted({str(a.get("kind")) for a in record.get("artifacts") or []
                    if isinstance(a, Mapping)})
    raise SessionRefused(
        f"a file-producing gate action's record MUST carry a "
        f"{gate_console.ART_COMMIT!r} artifact referencing its own action stamp "
        f"({stamp!r}); this one carries {kinds or 'none'}. The record and the "
        f"commit are ONE action (FR-006) and openxFactory's gate-action-record "
        f"schema requires the artifact — a record without it is that schema's own "
        f"negative example, and committing it would put a record the pinned "
        f"validator REJECTS onto the branch whose per-action commit series is the "
        f"traceability evidence (D18, spec.md's validator requirement). Build it "
        f"with `commit_artifact(stamp)`. The main-resident verbs are the ones that "
        f"carry no commit artifact, and they do not come through here.")


def commit_gate_action(gate: Any, git: SessionGit, *, worktree: Path | str,
                       branch: str, record: dict,
                       documents: Sequence[str],
                       records_dir: str = gate_console.DEFAULT_RECORDS_DIR,
                       summary: str | None = None,
                       session: Any = None) -> GateActionCommit:
    """Write the record beside the action's documents and commit them TOGETHER,
    as exactly ONE commit on the session branch (FR-006, chg 2.6).

    `session` (a `SessionOpen`) additionally makes the action REGENERATE the
    session's snapshot (FR-010, T034). It rides here, on the one
    commit-per-gate-action path, precisely so a later session verb cannot add a
    write that forgets to: "no manual step between an action and its appearance"
    is then structural rather than a rule each verb must remember.

    Order, and why: the documents are already written into the worktree by the
    verb's own engine (the authoring scaffold, the rewrite path); this function
    writes the RECORD through the HumanGate — so the records path stays inside
    the gate's declared allowlist, and `write_gate_action_record`'s target-id
    chain (including the session-`ref` fallback) is the one used everywhere —
    then stages document(s) AND record with EXPLICIT paths, then commits once.

    It is a TRANSACTION, and PR #49 review finding 1 is why it has to be one. The
    whole stage → commit → capture-the-sha sequence runs under a CROSS-PROCESS lock
    on the worktree (`SessionGit.worktree_action_lock`), the commit is bound to its
    declared paths (`git commit --only`), the index is asserted EMPTY before staging
    and asserted to be EXACTLY `{documents} ∪ {record}` after, and any failure
    unwinds everything this call created. Before that, a bare `git commit` over the
    ambient index meant: a pre-staged neighbour's file rode the action's commit; two
    overlapping writers produced ONE commit carrying both actions' documents and
    records under only the winner's `Gate-Action` trailer while the loser was told
    it had failed; and — with no concurrency at all — one failed commit left the
    action's own document and record STAGED, so the human's retry committed TWO
    gate-action records in one commit. All three were reproduced.

    Seven refusals, each a defect it would otherwise hide:

      * a caller that would SPLIT document and record across commits. If a
        declared document is already CLEAN in the worktree it was committed by
        an earlier commit, so its record could only ride a different one.
      * a record whose `commit` artifact does not reference its own action stamp
        (or references something sha-shaped).
      * a record with NO `commit` artifact at all (PR #49 tail finding B4) — the
        presence check the five sha checks assumed. Without it a schema-invalid
        record, which the pinned openxFactory validator rejects, was committed
        onto the evidence branch.
      * a second writer already holding this worktree's action lock (the spec's
        "a losing race MUST fail loudly rather than silently clobbering").
      * an index that is not EMPTY when the action starts — foreign staged work, or
        a previous attempt's residue. Naming the paths and the remedy, because the
        alternative is absorbing them.
      * a post-stage index that is not exactly the declared set — the assertion
        SC-003 needs, made against `staged_paths()`, the helper that was written for
        this check and never called.
      * a commit whose `introduced_by` resolution does not land on the commit
        just made — which would mean the record's artifact reference does not
        resolve to this action's commit after all.

    The resulting sha is RETURNED for the response and never committed. It comes
    from the commit that was actually created, captured inside the lock, so no later
    HEAD read can report another writer's commit."""
    human = gate_console.require_human_gate(gate)
    root = Path(worktree).resolve()
    stamp = action_stamp(record["at"])
    _refuse_embedded_sha(record, stamp)
    _refuse_missing_commit_artifact(record, stamp)

    declared = [str(d).replace("\\", "/") for d in documents]
    if not declared:
        raise SessionRefused(
            "a file-producing gate action commits its documents WITH its record; "
            "an action that produced no document has nothing to co-commit "
            "(FR-006) — `open-pr` and `abandon-session` are main-resident and "
            "carry no commit artifact at all")
    for rel in declared:
        resolved = (root / rel).resolve()
        if resolved != root and root not in resolved.parents:
            raise SessionRefused(
                f"refusing {rel!r}: a session action's documents resolve inside "
                f"the session worktree {root}; a path that escapes is a refusal, "
                "not a fallback (data-model validation rules)")
    try:
        with git.worktree_action_lock(
                root, action=f"{record.get('action') or 'gate action'} {stamp}"):
            return _commit_gate_action_locked(
                human, git, root=root, branch=branch, record=record, stamp=stamp,
                declared=declared, records_dir=records_dir, summary=summary,
                session=session)
    except SessionActionInProgress as exc:
        # Re-raised in the SESSION vocabulary every surface already reports: the
        # routes and the CLI verbs turn a `SessionRefused` into a 409 / exit 1
        # carrying the engine's own reason, and a lock contention IS a session
        # precondition, not a git error.
        raise SessionRefused(str(exc)) from exc


def _commit_gate_action_locked(human: Any, git: SessionGit, *, root: Path,
                               branch: str, record: dict, stamp: str,
                               declared: Sequence[str], records_dir: str,
                               summary: str | None,
                               session: Any) -> GateActionCommit:
    """The body of one gate action, with this worktree's index owned exclusively.

    Split out so the transaction's shape is readable: observe, write, stage, assert,
    commit, verify — and on ANY failure, unwind to the state the action found."""
    # FIRST, and inside the lock: does this worktree still HOLD this branch?
    #
    # Every other assertion here is about WHAT enters the commit; this one is about
    # WHERE the commit lands, and without it the whole transaction was
    # branch-agnostic (PR #49 review finding 5, wave 2). `branch` arrives from the
    # caller's `SessionOpen` — a registry entry that recorded the pairing at open —
    # and a worktree the human's shell had moved took the commit onto whatever it
    # held, orphaning the action's document AND its record from the branch the
    # record attested to. `open_session`'s JOIN checks too, but it cannot be the
    # guarantee: the drift can happen in the window between the join and this
    # commit, and the CLI reaches here through the bootstrap instead. Under the
    # cross-process lock there is no such window left.
    assert_git_holds_branch(git, root, branch,
                            during=f"the gate action {stamp} on {branch!r}")
    dirty = set(git.dirty_paths(root))
    already_committed = [d for d in declared if d not in dirty]
    if already_committed:
        raise SessionRefused(
            "refusing to write a gate-action record in a different commit from "
            f"its documents: {', '.join(sorted(already_committed))} "
            f"{'is' if len(already_committed) == 1 else 'are'} already committed "
            "on this branch, so the record could only ride a second commit "
            "(FR-006)")
    foreign = git.staged_paths(root)
    if foreign:
        raise SessionRefused(
            "refusing to start a gate action in a worktree whose index is not "
            f"empty: {', '.join(sorted(foreign))} "
            f"{'is' if len(foreign) == 1 else 'are'} already staged. A gate action "
            "is exactly ONE commit carrying ITS documents and ITS record (FR-006, "
            "SC-003), and committing on top of a dirty index would fold that work "
            "into this action's commit under this action's `Gate-Action` trailer. "
            "Unstage it first — `git -C "
            f"{root} reset -- {' '.join(sorted(foreign))}` — then run the action "
            "again; nothing has been written.")

    # Which declared documents git has never tracked. Those exist only because THIS
    # action created them, so a refusal removes them; a TRACKED document carries
    # history and possibly human edits, and a refusal leaves the working tree
    # exactly as it found it rather than reverting somebody's drafting.
    tracked = set(git.tracked_paths(root, declared))
    created_here = tuple(d for d in declared if d not in tracked)
    before_head = git.head(root)

    record_path: Path | None = None
    staged: tuple[str, ...] = ()
    committed: str | None = None
    try:
        record_path = gate_console.write_gate_action_record(human, records_dir,
                                                           record)
        record_relpath = _relpath_within(record_path, root)
        expected = {*declared, record_relpath}
        staged = git.stage(root, [*declared, record_relpath])
        actual = set(git.staged_paths(root))
        if actual != expected:
            raise SessionRefused(
                "refusing to commit this gate action: the index holds "
                f"{', '.join(sorted(actual))} but the action declared "
                f"{', '.join(sorted(expected))}. A gate action's commit carries "
                "exactly its documents and its record — nothing else may enter it, "
                "and nothing of its own may be missing (FR-006, SC-003).")
        message = commit_message(record["action"], stamp, summary=summary)
        # `only=` binds the commit to the declared set even if a foreign `git add`
        # lands between the assertion above and the commit itself.
        committed = git.commit(root, message, only=[*declared, record_relpath])
        resolved = git.introduced_by(record_relpath, cwd=root)
        if resolved != committed:
            raise SessionRefused(
                f"the record's commit artifact does not resolve to this action's "
                f"commit (introduced-by gave {resolved!r}, the commit is "
                f"{committed!r}); the record and its documents must ride ONE commit "
                "(FR-006)")
    except BaseException as exc:
        notes = _unwind_gate_action(
            git, root, staged=staged, record_path=record_path,
            created_here=created_here, before_head=before_head,
            committed=committed)
        if notes and isinstance(exc, SessionRefused):
            raise SessionRefused(f"{exc}\n\n" + "\n".join(notes)) from exc
        raise
    snapshot = None
    registry = getattr(session, "registry", None) if session is not None else None
    if registry is not None:
        # FR-010: the session's bullseye, docs panel, and outline refresh as part
        # of THIS action. A projection failure is reported on the entry and never
        # unwinds the commit — the commit is already law (see `_refresh_or_report`).
        snapshot = _refresh_or_report(
            registry, repository=session.repository, branch=branch, worktree=root)
    # THE FIRST SUCCESSFUL COMMIT is where a freshly opened session's notebook is
    # created (FR-036; PR #49 finding 3). After the commit, deliberately: the open
    # is fallible right up to this line, and a notebook created before it leaked a
    # real one onto the shared account whenever the action then refused. It also
    # degrades and never raises (FR-042), so it cannot turn a landed commit into a
    # failure — the notice rides the response instead.
    session = attach_session_notebook(session)
    return GateActionCommit(
        sha=committed, stamp=stamp, branch=branch, record_path=record_path,
        record_relpath=record_relpath, documents=tuple(declared),
        record=record, message=message, snapshot=snapshot, session=session)


def _unwind_gate_action(git: SessionGit, root: Path, *,
                        staged: Sequence[str], record_path: Path | None,
                        created_here: Sequence[str], before_head: str,
                        committed: str | None) -> tuple[str, ...]:
    """Put the worktree back the way the action found it, and say what could not be
    put back.

    A refusal must persist NOTHING — the console says so, and PR #49 finding 1
    measured what happens when it does: a failed commit left the action's document
    and record staged, so the retry committed two gate-action records in one commit
    and one of them attested to an action the human had been told had failed.

    In reverse order of creation, each step contained so a failure in one does not
    strand the others:

      1. the COMMIT, if one was made and the verification then refused it.
         `reset --soft` moves HEAD back and leaves the working tree untouched — the
         commit was created moments ago inside this lock, so HEAD cannot have moved
         and nothing but this action is being undone.
      2. the INDEX entries this action staged.
      3. the RECORD file this action wrote.
      4. the declared documents git had never tracked before this action, which
         therefore exist only because of it. A tracked document is left exactly as
         found: reverting it would discard whatever was in the working tree, which
         is the human's, not this function's.

    Runs inside the action's lock, so it is racing nobody."""
    notes: list[str] = []
    if committed is not None:
        try:
            git.git(root, "reset", "--soft", before_head)
        except (GitError, SessionGitRefused) as exc:
            notes.append(
                f"the refused commit {committed} could NOT be undone ({exc}); it is "
                f"still the tip of this branch and must be reset by hand to "
                f"{before_head}")
    if staged:
        try:
            git.unstage(root, staged)
        except (GitError, SessionGitRefused) as exc:
            notes.append(f"the action's staged paths could not be unstaged ({exc}); "
                         f"run `git -C {root} reset -- {' '.join(staged)}` before "
                         "retrying, or the retry will commit them alongside its own")
    if record_path is not None:
        try:
            Path(record_path).unlink(missing_ok=True)
        except OSError as exc:
            notes.append(f"the gate-action record {record_path} could not be "
                         f"removed ({exc}); delete it before retrying, or the retry "
                         "will commit two records")
    for rel in created_here:
        target = root / rel
        try:
            if target.is_file():
                target.unlink()
        except OSError as exc:
            notes.append(f"{rel} was created by this action and could not be "
                         f"removed ({exc})")
    return tuple(notes)


def _relpath_within(path: Path, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise SessionRefused(
            f"{path} is not inside the session worktree {root}; a session record "
            "is written inside the worktree it rides (FR-006)") from exc


# ---------------------------------------------------------------------------
# The ELIGIBLE FIRST-EDIT transaction (010-doxbench-editor-chat, FR-031..FR-037)
#
# `commit_gate_action` above is a transaction over an ALREADY-OPEN session. An
# explicit Save from the doxBench console is a harder shape, because the OPEN is
# part of it: an eligible first Save must "atomically create or join that tile's
# branch session, revalidate the source, and persist only in the resulting
# session" (FR-032), and a failure must leave "no document change, commit,
# governance record, live registry entry, or orphan working tree" (FR-033).
#
# Nothing here is a new authority. The two existing document verbs do the
# persisting, the existing session primitives do the opening and the joining,
# `_commit_gate_action_locked` does the record-and-commit, and
# `unwind_opened_session` is the compensator. What is new is the COMPOSITION,
# and two things about it are worth stating because they are easy to get wrong:
#
#   1. The action lock is per-WORKTREE, and the worktree does not exist until
#      the open — so the open cannot be inside the lock. It is instead inside
#      this transaction's FAILURE DOMAIN: everything from the open onward
#      unwinds. The window between the open and the lock claim is covered by the
#      lock itself refusing loudly to a rival, and the session-allocation race
#      by `open_session`'s own ordinal machinery.
#   2. The rollback is ASYMMETRIC, and it has to be. A Save that OPENED the
#      session removes the whole session. A Save that JOINED one must not: the
#      commits already on that branch are other actions' governed history, so a
#      failure restores only the bytes THIS Save replaced and leaves everything
#      else exactly as it was found.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FirstEditEligibility:
    """Whether an eligible first Save may persist a path, and as WHICH existing
    action. Pure: it reads the two trees and answers, and persists nothing."""

    eligible: bool
    action: str | None = None
    document: str | None = None
    reason: str | None = None
    session_created: bool = False


@dataclass(frozen=True)
class FirstEditCommit:
    """What one eligible first Save persisted (data-model `SaveOutcome`'s
    per-buffer half, carrying the session and commit it rode)."""

    action: str
    document: str
    ref: str
    revision: str
    content_hash: dict
    joined: bool
    session: Any
    commit: GateActionCommit
    record: dict
    notes: tuple[str, ...] = ()

    @property
    def opened(self) -> bool:
        return not self.joined


def _first_edit_relpath(root: Path | str, document: str) -> str | None:
    """`document` as a slash-spelled path relative to `root`, or None when it is
    not under `root` at all.

    Deliberately NOT `_relpath_within`: that one REFUSES, in the vocabulary of a
    record that must ride its own worktree. This one ANSWERS, because eligibility
    is a question asked before anything is opened and an escaping path is one of
    the answers rather than an error to raise."""
    try:
        base = Path(root).resolve()
        candidate = Path(document)
        resolved = (candidate if candidate.is_absolute() else base / candidate).resolve()
        return resolved.relative_to(base).as_posix()
    except (OSError, ValueError):
        return None


def first_edit_eligibility(*, document: Any, checkout_root: Path | str,
                           owned_prefix: str | None,
                           worktree: Path | str | None = None,
                           tile: "Tile | None" = None) -> FirstEditEligibility:
    """May this buffer be saved, and through which EXISTING action (FR-031,
    FR-036)?

    A Save may reach exactly two things, which is the same pair the workbench's
    rewrite allowance already recognises:

      * the tile's OWN material — the folder a staged-topic tile is named after,
        passed in as `owned_prefix` so this module stays free of corpus layout
        and `gate_routes.tile_owned_prefix` remains the single source of that
        rule; and
      * a document THIS SESSION brought into existence — present in the session
        worktree and absent from the served checkout, which is the branch's base
        and is moved by no session operation (FR-004).

    Everything else that ALREADY EXISTS is inherited, cited,
    cluster-neighbourhood, or inbound material: read-only context in the
    workbench and a refusal here (FR-036). A path that exists NOWHERE is not
    inherited from anyone, so it stays eligible as a create even for a tile that
    owns no folder — inheriting nothing is not the same as being unable to
    author.

    `owned_prefix=None` is the fail-closed reading, matching
    `gate_routes.foreign_document_refusal`: without a declared folder only
    session-created and brand-new paths pass."""
    text = "" if document is None else str(document).strip()
    if not text:
        return FirstEditEligibility(
            False, reason="a buffer with no path has never been created, and a "
                          "filename is never guessed on the human's behalf "
                          "(FR-031)")
    base = Path(checkout_root)
    rel = _first_edit_relpath(base, text)
    if rel is None:
        return FirstEditEligibility(
            False, reason=f"refusing {text!r}: it resolves OUTSIDE the served "
                          f"checkout {base}, and a path that escapes is a "
                          "refusal rather than a value clamped back inside")
    served_has = (base / rel).is_file()
    in_worktree = bool(worktree) and (Path(worktree) / rel).is_file()
    prefix = str(owned_prefix or "").strip()
    owned = bool(prefix) and (rel == prefix.rstrip("/") or rel.startswith(prefix))
    session_created = bool(in_worktree and not served_has)
    if not owned and not session_created and served_has:
        kind = str(getattr(tile, "scope_kind", "") or "?")
        scope_id = str(getattr(tile, "scope_id", "") or "?")
        own = (f"documents under {prefix} (the topic's own material)" if prefix
               else "no folder of its own — a cluster or possible tile inherits "
                    "none")
        return FirstEditEligibility(
            False, reason=(
                f"refusing to save {rel!r}: it is NOT this tile's own material. "
                f"The console is open on tile {kind} {scope_id}, which owns "
                f"{own}, plus any document this session created. {rel!r} already "
                f"exists in the served checkout outside that material, so saving "
                f"it here would commit ANOTHER topic's document onto this tile's "
                f"branch under a gate-action record naming this session — an "
                f"overwrite that reads as authorised and is not. doxBench shows "
                f"inherited, cited, cluster-neighbourhood and inbound documents "
                f"as READ-ONLY CONTEXT for exactly this reason (FR-036). Nothing "
                f"was written."))
    action = (gate_console.ACTION_EDIT_DOCUMENT if (served_has or in_worktree)
              else gate_console.ACTION_CREATE_DOCUMENT)
    return FirstEditEligibility(True, action=action, document=rel,
                                session_created=session_created)


def first_edit_base_refusal(*, document: str, root: Path | str, action: str,
                            base_hash: str | None) -> str | None:
    """Why this Save's declared base is no longer the base on disk, or None.

    FR-032's revalidation clause. The buffer carries the identity of the text the
    human edited FROM; if the target no longer hashes to it, saving would
    overwrite newer material with a replacement composed against text that is
    gone. Asked immediately before the mutation and inside the lock, because the
    window that matters is the one the mutation itself opens.

    The create arm's base is the ABSENCE of the path, so a path that has since
    appeared is exactly as stale as a changed hash."""
    target = Path(root) / document
    if action == gate_console.ACTION_CREATE_DOCUMENT:
        if target.exists():
            return (f"refusing to create {document!r}: this Save was composed "
                    "against the ABSENCE of that path, and something has created "
                    "it since. Saving now would overwrite it while reporting a "
                    "create (FR-032). Reload the document and save again.")
        return None
    if not target.is_file():
        return (f"refusing to rewrite {document!r}: it no longer exists in the "
                "tree this Save would land in. A rewrite does not silently "
                "recreate a document that has been removed, because that would "
                "hide the removal (FR-032).")
    if not base_hash:
        return (f"refusing to rewrite {document!r}: the Save declared no base "
                "content identity, so the replacement cannot be revalidated "
                "against the bytes it would replace, and an unrevalidatable "
                "overwrite is refused rather than trusted (FR-032).")
    try:
        # T104 F10: read through the SAME lens the client hashed. `/source`
        # serves verbatim bytes and the browser's `Response.text()` keeps CR
        # and CRLF (dropping only a leading BOM), while `Path.read_text`'s
        # universal-newline translation collapses them — so a CRLF document's
        # base was recomputed over text the client never saw and every honest
        # Save of it was refused as stale, forever.
        current = doxbench_hash.sha256_hex(
            doxbench_hash.served_text(target.read_bytes()))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        # Wave re-review P3-5, considered and KEPT: the strict decode above is
        # a DELIBERATE asymmetry with the browser. The client's lenient
        # `Response.text()` computes an identity over U+FFFD-replaced text for
        # a non-UTF-8 file; this server refuses to fabricate one, so such a
        # file is honestly unsaveable through doxBench rather than silently
        # re-encoded. And the refusal states only the exception CLASS:
        # `str(UnicodeDecodeError)` embeds the offending byte value and its
        # offset from the file being edited, and a refusal never echoes
        # document content.
        return (f"refusing to rewrite {document!r}: its current bytes could not "
                f"be read to revalidate the base ({type(exc).__name__})")
    if current != str(base_hash):
        return (f"refusing to rewrite {document!r}: it was edited from base "
                f"{base_hash} but now holds {current}. The source moved "
                "underneath this buffer, so saving would overwrite newer text "
                "with a replacement composed against text that is gone "
                "(FR-032). Compare the two and save again.")
    return None


def commit_first_edit(git: SessionGit, registry: Any, *, repository: str,
                      tile: "Tile", document: str, content: Any,
                      gate_factory: Any, checkout_root: Path | str,
                      owned_prefix: str | None = None,
                      base_hash: str | None = None,
                      records_dir: str = gate_console.DEFAULT_RECORDS_DIR,
                      at: str | None = None, notes: str | None = None,
                      inventory: "TileInventory | None" = None,
                      base: str = DEFAULT_BASE, notebook: Any = None,
                      provenance: Any = None, summary: str | None = None,
                      continuation: str | None = None,
                      proposal: "ProposalState | None" = None,
                      thread_paths_for: Any = None) -> FirstEditCommit:
    """One eligible first Save: create-or-join this tile's session, revalidate
    the source, and persist exactly this document in the resulting session as
    ONE existing governance action (FR-031, FR-032, FR-034).

    `gate_factory(worktree)` builds the worktree-rooted `HumanGate` the write and
    the record both go through — injected so this module keeps constructing no
    gates of its own and so the HTTP route and any parity caller cannot diverge
    on how the gate is declared.

    `thread_paths_for` is the SEAM that makes a thread ride its document's Save
    (add-doxbench-editing-phase-b task 9.2). It is injected — the doxBench Save
    route passes `doxbench_threads.thread_commit_paths` — for two reasons: this
    module stays free of doxBench's own path rule, and the rule is applied to
    the NORMALISED document path this transaction settles on rather than to the
    caller's spelling of it, which is what keeps the committed sidecar the same
    file a turn actually wrote. `None` is every other caller, whose behaviour is
    byte-identical to before.

    On ANY failure the state the Save found is restored (FR-033). Which
    restoration depends on whether this Save opened the session or joined one,
    and the difference is not an optimization — tearing down a JOINED session
    would destroy other actions' governed commits."""
    root = Path(checkout_root)
    at = at or gate_console._utcnow()
    if not isinstance(content, str) or not content.strip():
        # A blank replacement is a delete in disguise, and no doxBench path
        # grants delete authority (FR-037). Refused before anything is opened.
        raise SessionRefused(
            "refusing an empty Save: a blank or absent replacement is a delete "
            "in disguise, and no doxBench path deletes a document (FR-037)")
    # PRECHECK, against the served checkout alone: the session-created allowance
    # cannot be evaluated before there is a worktree, but material that ALREADY
    # EXISTS outside this tile's own folder is definitively inherited, and
    # refusing it here costs nothing and opens nothing.
    verdict = first_edit_eligibility(document=document, checkout_root=root,
                                     owned_prefix=owned_prefix, tile=tile)
    if not verdict.eligible:
        raise SessionRefused(verdict.reason or "this buffer may not be saved")

    session = open_session(git, registry, repository=repository, tile=tile,
                           inventory=inventory, base=base,
                           verb=verdict.action, proposal=proposal,
                           checkout_root=root, continuation=continuation,
                           notebook=notebook)
    # THE OPEN IS INSIDE THIS SAVE'S FAILURE DOMAIN FROM HERE.
    worktree = Path(session.worktree)
    rel = verdict.document
    target = worktree / rel
    existed = target.is_file()
    original = target.read_bytes() if existed else None
    stamp = action_stamp(at)
    try:
        try:
            lock = git.worktree_action_lock(
                worktree, action=f"{verdict.action} {stamp}")
        except SessionActionInProgress as exc:
            raise SessionRefused(str(exc)) from exc
        try:
            with lock:
                return _commit_first_edit_locked(
                    git, session, gate_factory=gate_factory, worktree=worktree,
                    rel=rel, content=content, base_hash=base_hash,
                    records_dir=records_dir, at=at, stamp=stamp, notes=notes,
                    provenance=provenance, summary=summary,
                    checkout_root=root, owned_prefix=owned_prefix, tile=tile,
                    thread_paths_for=thread_paths_for)
        except SessionActionInProgress as exc:
            raise SessionRefused(str(exc)) from exc
    except BaseException as exc:
        unwound = _unwind_first_edit(
            git, session, checkout_root=root, base=base, worktree=worktree,
            rel=rel, existed=existed, original=original)
        if unwound and isinstance(exc, SessionRefused):
            raise SessionRefused(f"{exc}\n\n" + "\n".join(unwound)) from exc
        raise


def _commit_first_edit_locked(git: SessionGit, session: SessionOpen, *,
                              gate_factory: Any, worktree: Path, rel: str,
                              content: str, base_hash: str | None,
                              records_dir: str, at: str, stamp: str,
                              notes: str | None, provenance: Any,
                              summary: str | None, checkout_root: Path,
                              owned_prefix: str | None,
                              tile: "Tile",
                              thread_paths_for: Any = None) -> FirstEditCommit:
    """The body of one first Save, with this worktree's index owned exclusively.

    Order, and why: re-assert the branch, re-answer eligibility now that the
    worktree exists, revalidate the base, write, then hand the record-and-commit
    to the SAME locked helper every other gate action uses. Everything after the
    branch assertion is inside the caller's rollback."""
    # WHERE the commit would land, re-asserted now that nothing else can move it.
    assert_git_holds_branch(git, worktree, session.branch,
                            during=f"the first Save {stamp} on {session.branch!r}")
    # Eligibility, re-answered against the tree the write would touch: only now
    # can "this session created it" be evaluated at all (FR-043's consequence).
    verdict = first_edit_eligibility(document=rel, checkout_root=checkout_root,
                                     owned_prefix=owned_prefix,
                                     worktree=worktree, tile=tile)
    if not verdict.eligible:
        raise SessionRefused(verdict.reason or "this buffer may not be saved")
    refusal = first_edit_base_refusal(document=rel, root=worktree,
                                      action=verdict.action, base_hash=base_hash)
    if refusal is not None:
        raise SessionRefused(refusal)
    human = gate_console.require_human_gate(gate_factory(worktree))
    if Path(human.output.root).resolve() != worktree.resolve() \
            or human.session_root is None \
            or Path(human.session_root).resolve() != worktree.resolve():
        raise SessionRefused(
            f"the gate is rooted at {human.output.root} (declared session "
            f"worktree {human.session_root}) but this session's worktree is "
            f"{worktree}: a session write is made through a gate rooted at the "
            "WORKTREE and DECLARING it, so the write allowance and the record's "
            "residence are the same tree (FR-015)")
    # The two EXISTING document verbs, chosen by the path and by nothing else.
    if verdict.action == gate_console.ACTION_CREATE_DOCUMENT:
        human.output.create_document(rel, content)
    else:
        human.rewrite_session_document(rel, content)
    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=verdict.action, at=at, document=rel,
        notes=notes, provenance=provenance,
        artifacts=[commit_artifact(stamp)],
        # inside a session the record ALWAYS names its branch, or it audits
        # nothing
        ref=session.branch)
    _refuse_embedded_sha(record, stamp)
    _refuse_missing_commit_artifact(record, stamp)
    # THE THREAD RIDES ITS DOCUMENT'S SAVE (add-doxbench-editing-phase-b task
    # 9.2), through the DECLARED path set `_commit_gate_action_locked` already
    # commits as exactly ONE commit — that function is untouched, and this is
    # the ratified one-commit-per-gate-action rule APPLIED to a second artifact
    # rather than relaxed for it.
    #
    # ONLY A DIRTY SIDECAR JOINS, and the filter is not an optimisation: the
    # declared set must be dirty or the action refuses as "already committed"
    # (see the clause at the top of that function), so declaring a sidecar no
    # turn has written since the last Save would refuse every Save on a tile
    # whose thread had not moved.
    declared = [rel, *_dirty_thread_paths(git, worktree, rel, thread_paths_for)]
    commit = _commit_gate_action_locked(
        human, git, root=worktree, branch=session.branch, record=record,
        stamp=stamp, declared=declared, records_dir=records_dir,
        summary=summary or f"{verdict.action}: {rel}", session=session)
    return FirstEditCommit(
        action=verdict.action, document=rel, ref=session.branch,
        revision=commit.sha,
        content_hash=doxbench_hash.content_identity(content).as_dict(),
        joined=session.joined, session=commit.session or session, commit=commit,
        record=record)


def _dirty_thread_paths(git: SessionGit, worktree: Path, rel: str,
                        thread_paths_for: Any) -> tuple[str, ...]:
    """The thread sidecars this Save's commit carries, in declared order.

    Empty for every caller that injects no seam, and empty when the seam
    refuses the path (a document with no derivable sidecar has no thread) — an
    absence, never a failure of the Save."""

    if not callable(thread_paths_for):
        return ()
    try:
        candidates = tuple(thread_paths_for(rel))
    except Exception:  # noqa: BLE001 - a path with no sidecar simply has none
        return ()
    dirty = set(git.dirty_paths(worktree))
    return tuple(path for path in candidates if path in dirty)


def _unwind_first_edit(git: SessionGit, session: SessionOpen | None, *,
                       checkout_root: Path, base: str, worktree: Path,
                       rel: str, existed: bool,
                       original: bytes | None) -> tuple[str, ...]:
    """Restore what a failed first Save found, and report what could not be.

    ASYMMETRIC by design (data-model `FirstEditTransaction`):

      * a Save that OPENED the session removes the whole session
        (`unwind_opened_session`, which refuses to remove one that already
        carries commits — by this point `_commit_gate_action_locked` has already
        reset away its OWN commit, so an unverifiable commit is not mistaken for
        governed history);
      * a Save that JOINED one restores only the bytes it replaced. Those
        commits belong to other actions and are not this Save's to discard.

    Every step is contained: an unwind reports, and never raises over the failure
    that caused it."""
    notes: list[str] = []
    if session is not None and session.joined:
        target = worktree / rel
        # What this Save REPLACED. `_commit_gate_action_locked` deliberately
        # leaves a tracked document's replaced bytes alone, because in an
        # ordinary gate action those may be the human's only copy. Here they are
        # not: the buffer still holds them, and this Save is the only thing that
        # touched the file.
        if existed and original is not None:
            try:
                if target.is_file() and target.read_bytes() != original:
                    target.write_bytes(original)
            except OSError as exc:
                notes.append(
                    f"{rel} was replaced by this Save and could not be restored "
                    f"({exc}); the session worktree still holds the replacement "
                    f"— recover it with `git -C {worktree} checkout -- {rel}`")
        # What this Save CREATED (T104 F3). This used to be left to
        # `_commit_gate_action_locked`'s own unwind, but that unwind only covers
        # failures raised inside its `try:` — its branch assertion, its
        # already-committed check and its not-empty-index refusal all fire
        # BEFORE it, and the created file then stayed in the session worktree.
        # FR-033 says a failed first Save leaves no document change, and the
        # residue is also self-perpetuating: the create arm's declared base is
        # the ABSENCE of the path (`first_edit_base_refusal`), so every retry is
        # refused for a file only the failed attempt wrote.
        #
        # Guarded by GIT's own answer, never by `existed` alone: a path git
        # TRACKS carries history that is not this Save's to delete — including
        # the case where the commit landed and something after it failed — so
        # only an untracked path this Save found absent is removed. That is the
        # same test `_unwind_gate_action`'s `created_here` makes.
        elif not existed:
            try:
                if target.is_file() and not git.tracked_paths(worktree, [rel]):
                    target.unlink()
            except (OSError, GitError, SessionGitRefused) as exc:
                notes.append(
                    f"{rel} was created by this Save and could not be removed "
                    f"({exc}); it is still in the session worktree and will "
                    f"refuse the next Save of that buffer — remove it with "
                    f"`rm {worktree / rel}` before retrying")
        return tuple(notes)
    return unwind_opened_session(git, session, checkout_root=checkout_root,
                                 base=base)


__all__ = [
    "FirstEditCommit", "FirstEditEligibility", "commit_first_edit",
    "first_edit_base_refusal", "first_edit_eligibility",
    "CLUSTER", "POSSIBLE", "STAGED_TOPIC", "SCOPE_KINDS", "DEFAULT_BASE",
    "CONTINUATIONS", "CONTINUATION_NEW", "CONTINUATION_RESUME",
    "EXTERNALLY_DISPATCHING_VERBS", "SESSION_NAMESPACES",
    "TEARDOWN_STEPS", "TORN_NOTEBOOK", "TORN_REGISTRY_ENTRY", "TORN_WORKTREE",
    "BRANCH_WITHOUT_WORKTREE", "ENDED_SESSION_RESIDUE",
    "ENDING_ABANDON", "ENDING_MERGE",
    "NOT_A_SESSION_DIRECTORY",
    "WORKTREE_DETACHED", "WORKTREE_DIRECTORY_MISSING",
    "WORKTREE_ON_ANOTHER_BRANCH", "WORKTREE_UNKNOWN_TO_GIT",
    "WORKTREE_WITHOUT_BRANCH",
    "AbandonedBranchSurvives", "CrossTileCollision",
    "DispatchNotRecorded", "EndedSessionResidue",
    "EndingNotDurable",
    "ExternalDispatchRefused",
    "GateActionCommit", "LiveProposalRefused", "LiveSessionRefused",
    "MergeReconciliation", "MergeState",
    "NoActiveSession", "ProposalState",
    "SessionBootstrap", "SessionOpen", "SessionRefused", "SessionGitRefused",
    "SessionTeardown",
    "SessionWorktreeDrifted",
    "StaleSession", "StaleSessionWorktree", "Tile", "TileInventory",
    "abandoned_branch_candidates", "action_stamp", "allocate_ordinal",
    "assert_branch_cleanup_permitted", "assert_no_cross_tile_collision",
    "assert_no_live_proposal", "assert_no_live_session",
    "assert_git_holds_branch", "worktree_drift",
    "assert_verb_stays_inside_session", "attach_session_notebook",
    "bootstrap_sessions", "branch_from_worktree_dir",
    "branch_namespace", "clear_dispatch_marker", "collision_owner",
    "commit_artifact", "commit_gate_action", "commit_message", "container_root",
    "dispatch_marker_path", "read_dispatch_marker", "write_dispatch_marker",
    "clear_ending_marker", "ending_marker_path", "read_ending_marker",
    "clear_owner_marker", "owner_marker_path", "read_owner_marker",
    "write_owner_marker", "recorded_session_tile", "tile_key",
    "abandon_proof", "abandon_records_for", "branch_remote_presence",
    "reserve_ending_marker", "write_ending_marker",
    "deterministic_session_branch", "existing_branch_names", "flatten_branch",
    "is_live", "landed_proposal_ids", "live_session_branches",
    "live_session_branches_of", "live_session_worktree", "looks_ref_legal",
    "merge_state", "new_session_branch", "next_ordinal", "normalize_continuation",
    "create_session_notebook", "notebook_degradation_notice",
    "notebook_deferred_sources_notice",
    "notebook_alias", "notebook_alias_collision_notice", "notebook_alias_stem",
    "notebook_key_digest", "session_alias_owner",
    "open_session", "open_session_notebook", "ordinal_of",
    "proposal_state_for",
    "reconcile_merged_session", "reduce_scope_id", "refresh_main_view",
    "refresh_session_snapshot",
    "register_session_entry", "retire_session_notebook",
    "session_branch", "session_entry", "session_snapshot_path", "sessions_root",
    "snapshots_root", "teardown_session", "tile_branch_family",
    "unregister_session_entry", "unwind_opened_session", "worktree_path",
]
