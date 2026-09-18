#!/usr/bin/env python3
"""FLOOR PART 4's runner: render ONE corpus through the PRE-SPLIT tree and
through the POST-SPLIT stack and compare the snapshots byte for byte
(`split-opendox-two-layer-product` § 5.5, design § D6 part 4, RULED OQ-1).

WHAT THE FLOOR ASKS FOR. Design § D6 (4) is one sentence — "the same corpus
served by the pre-split tree and by the post-split stack produces the same
snapshot digests" — and § 5.5 is three lines over it. RULED OQ-1 (`#656`
comment `5547060378`) made it one of four parts, none of which substitutes for
another, and "snapshot-equivalence only" was rejected on that record. The other
three parts left a runner behind (`validate-carve-manifest.py`,
`verify-carve-arrival.py`, `verify-carve-conformance.py`); this is the fourth.

WHAT THE TWO SIDES ARE, WHICH HAD TO BE MEASURED BEFORE ANYTHING COULD BE
WRITTEN (`attachments/lane-opendox/floor55/SCOPING-floor55.md`, 2026-09-18):

  * **the PRE-SPLIT TREE is a published annotated tag, not a fixture.**
    `opendox-carve-0` -> `b075fd91dc8fced8e1373825ba80220c33536bae`, which is
    FLOOR PART 1's own `carve_commit`, frozen by RULED (a) POST-SHED MODE
    (`#656` comment `5625573095`: "Carve digests stay frozen at `b075fd91` /
    `opendox-carve-0`"), already at origin, and already what the carve
    manifest's own header tells a reader to do once `phase:` flips: "ask about
    the carve's own line by CHECKING OUT A PRE-SHED REVISION". `--pre-ref`
    accepts any pre-shed ref, so the claim does not rest on one of them:
    `contract-v3.7` (`45bd9ee2`) and the last pre-shed commit `cc4ae9d3^`
    (`07a8a45b`) render the identical digest, measured.

    A RECORDED GOLDEN DIGEST WAS THE ALTERNATIVE AND IT IS THE WRONG
    INSTRUMENT, for the reason RULING OQ-K (`#656` comment `5609526215`) gave
    when it killed part 2's scalar: "a scalar in a ratified document is
    re-falsified by every merge". A digest committed here would also stop
    proving the half of § D6 (4) that is about the OLD side — that the
    pre-split tree still renders at all.

  * **the POST-SPLIT STACK is not any leg pull request.** openDox-code #25/#26
    and openXdox-code #23 carry no renderer between them (measured over their
    file lists). It is `openxdox.generator` + `openxdox.snapshot` at the
    openXdox-code leg THIS REPOSITORY ALREADY PINS, reached through
    openxFactory's own composition point — `scripts/carved_reach.py`, landed
    under RULED Q7 (`#656` comment `5626248666`) and the only place this
    repository spells the reach — over `scripts/doc_health/` (the half RULED
    DQ-1, `#656` comment `5547049745`, kept here) and
    `contracts/domain-profiles/openxfactory-engineering.yaml`, installed by
    `scripts/opendox_host.py::register_openxfactory()`.

    `carved_reach.module()` resolves the PRE-SHED path to the pinned
    post-split module BY READING THE MANIFEST ROW, so nothing below hard-codes
    which leg a module went to and the day a row is re-destined between the
    legs this file does not change.

WHY A RUNNER AND NOT A ONE-SHOT RECORDED RUN, which is the question parts 1-3
did not have to answer. Their subject is a tree that has stopped moving. THIS
ONE'S POST SIDE IS A PIN THAT MOVES: `openXdox`'s gitlink advances on every leg
bump, and each bump is a chance to break the projection with nothing red. A
recorded run proves the day it ran. This proves every merge, and it costs
about a second and a half.

WHY IT LIVES HERE AND IS NEVER COPIED INTO SIX REPOSITORIES —
`verify-carve-conformance.py`'s rule and `verify-carve-arrival.py`'s before it,
adopted verbatim and for the same reason: the floor is one obligation of one
change, and a runner copied six ways is six things to keep in step with one
definition of passing. Part 3 could hand its CHECKS to a destination as a
neutral module because a destination runs them over its own reader. Part 4 has
nothing to hand anybody: its POST side is this repository's own composition of
two pins, and there is exactly one of those.

THE PRE SIDE RUNS IN A SUBPROCESS, and that is not fastidiousness. Both trees
define `ideation_dashboard` AND `doc_health`. One interpreter would resolve
whichever landed on `sys.path` first, for both names, and could then report
equivalence against itself — a green run that measured one side twice. The
child is additionally started with `-I`, which closes a DIFFERENT door: a name
the archive does not carry would otherwise fall through to a `PYTHONPATH`, a
script directory or a user-site copy and silently complete a partial archive
out of another checkout. It does NOT remove system site-packages, and `-S`
cannot be used — the archived `doc_health` imports PyYAML, measured — so
`render_pre` says exactly where that boundary stops.

`source_revision` IS PINNED ON BOTH SIDES, and the run is meaningless without
it. Measured unpinned: the post side reads the checkout's HEAD through
`RealGit` (`ad089e8a…`) and the pre side — an archive, not a repository —
reads `unknown`; the digests then differ for a reason that has nothing to do
with the projection. The pre-split determinism suite already solved this with
`PINNED_REVISION = "abcd1234" * 5` and an injected `FakeGit`
(`tests/ideation-dashboard/conftest.py`:121-140), for the reason its own
comment gives: "the fixture base-repo lives INSIDE the openxFactory git repo,
so a real `RealGit` HEAD is unstable across commits". Both sides here get that
same pin and that same injected git, and `--source-revision` moves it for a
caller who needs to.

ONE CORPUS, TWO ENGINES — and `--corpus` is REPEATABLE. § D6 (4)'s subject is
"the SAME corpus served by" both sides, so both sides are pointed at the same
directory rather than each at its own copy; a state that moves the digest must
move BOTH digests, or the run is comparing two different questions. Repeating
the flag runs several states in one invocation, which is what makes an equal
result a measurement rather than a constant: of the four states the suite
runs, two MOVE the digest.

WHAT THIS RUNNER DELIBERATELY DOES NOT DO, REGISTERED BY NAME SO IT IS NOT
MISTAKEN FOR AN OVERSIGHT (the Q-P3 residue, owed to § 8.9 or a successor):
IT DOES NOT VALIDATE THE RENDERED SNAPSHOT AGAINST ITS SCHEMAS, because the
carve broke that path three ways and § D6 (4) asks for digests —
`canonical_bytes` reaches no validator. The three, measured:

  1. `openXdox/code/scripts/validate-ideation-dashboard-contracts.py` derives
     `SCHEMAS_DIR = ROOT / "contracts" / "schemas"` from its own `__file__`
     and openXdox-**code** carries no such directory, so it exits 2 with
     `ERROR … not found`; its ten schemas are split three ways —
     snapshot/index/gate-action at openXdox-**spec**,
     workbench/chat-turn/model-catalog at openDox-**spec**, and
     gate-intent/possibles-register/project-register/demotion-receipt HERE —
     so no single `--schemas-dir` closes it either.
  2. `openxdox/snapshot.py`:29's `VALIDATOR_RELPATH` is a `moved_verbatim` row
     and now names
     `openxFactory/scripts/validate-ideation-dashboard-contracts.py`,
     a path this repository shed at `cc4ae9d3`.
  3. `find_validator()` WALKS UP THE PARENTS, so a run started inside a
     checkout that still carries a pre-shed copy silently adopts it — a reader
     adopting its enclosing tree, which is the defect class floor37 § 6 already
     named, arriving a second time in a different module.

  Also unmeasured and NOT claimed here: the snapshot INDEX
  (`openxdox/snapshot_registry.py` and
  `ideation-dashboard-snapshot-index.schema.yaml`). § D6 (4) says "snapshot
  digests"; the index is a second artifact and would be a second runner.

Exit codes, and there are two:
  0  every corpus state rendered the same bytes on both sides
  2  ANY refusal, a digest difference included, and any environment failure

  There is deliberately NO exit 1, on `verify-carve-conformance.py`'s
  reasoning and enforced the same way: `main()` catches every `Exception` its
  own checks did not name and renders it as `equivalence-unreadable`, so the
  contract does not rest on a reader auditing every raise site.
  `KeyboardInterrupt` and `SystemExit` are the operator's acts and are left
  alone.

Run:
    python3 scripts/verify-snapshot-equivalence.py
    python3 scripts/verify-snapshot-equivalence.py --pre-ref contract-v3.7
    python3 scripts/verify-snapshot-equivalence.py --json \\
        --corpus tests/ideation-dashboard/fixtures/base-repo
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import io
import signal
import subprocess
import sys
import tarfile
import threading
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# `scripts/` goes on the path because `carved_reach` and `opendox_host` both
# live there and this file is a hyphenated entry point its own tests load by
# `spec_from_file_location`, where Python inserts nothing. GUARDED and
# therefore idempotent, on `verify-carve-conformance.py`'s idiom and for its
# stated reason: a test module that loads this file more than once would
# otherwise prepend a duplicate entry per load.
_SCRIPTS_DIR = str(ROOT / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

#: The pre-split tree, by the name RULED (a) froze it under. A TAG and not a
#: commit: `opendox-carve-0` is published, annotated and at origin, and
#: `.github/workflows/pytest-suite.yml` checks out with `fetch-depth: 0`, so it
#: is reachable on a runner without any extra step.
DEFAULT_PRE_REF = "opendox-carve-0"

#: The corpus. `not_moved / replicated_at_destination`, so the shed left it
#: here, and all 11 of its files are byte-identical at `b075fd91` and at
#: today's `main` — which is why one directory can serve both sides.
CORPUS_RELPATH = "tests/ideation-dashboard/fixtures/base-repo"

#: What the archive extracts: the pre-split RENDERER and the corpus machinery
#: it imports (`generator.py`:66 `from doc_health import corpus`). 147 files,
#: 5.7 MB, 0.07 s — the corpus itself is NOT extracted, because both sides
#: render the operator's `--corpus`.
ARCHIVE_PATHS = ("scripts/ideation_dashboard", "scripts/doc_health")

#: The two rows this run is about, spelled in their PRE-SHED form, which is the
#: only form `carved_reach` accepts and the form that makes the two sides
#: comparable: the same two names, resolved two ways.
GENERATOR_ROW = "scripts/ideation_dashboard/generator.py"
SNAPSHOT_ROW = "scripts/ideation_dashboard/snapshot.py"

#: `tests/ideation-dashboard/conftest.py`:140's constant and its FakeGit's
#: date, restated rather than imported: this file is a command-line entry point
#: and must not depend on a pytest conftest to know what it pins.
PINNED_SOURCE_REVISION = "abcd1234" * 5
PINNED_COMMIT_DATE = "2026-07-12T00:00:00+00:00"

#: What a revision may LOOK like. `FakeGit` accepts any string and the engine
#: never resolves the anchor, so without this `--source-revision HEAD` or
#: `--source-revision not-a-revision` would exit 0 over a snapshot stamped
#: with a non-commit (Copilot, PR #1105 round 3). Sha-1 and sha-256 object
#: ids both, on `hermes_runtime_validation/content.py`'s `_OBJECT_ID`.
OBJECT_ID = re.compile(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}")

#: The repository name the snapshot is stamped with. The determinism suite's,
#: so a digest measured here is the digest that suite measures.
REPOSITORY_NAME = "fixture-repo"

#: How many lines of the unified diff a `equivalence-digests-differ` prints
#: before it truncates. A refusal that is a wall of JSON is a refusal nobody
#: reads; `--json` then carries the WHOLE DIFF (and the digests and byte
#: counts) for a caller that wants it — not the two snapshots themselves,
#: which no caller has asked for and which would put two corpora in a refusal
#: (Copilot, PR #1105).
DIFF_LINE_CAP = 120

REFUSAL_CODES: tuple[str, ...] = (
    "equivalence-pre-ref-unreachable",
    "equivalence-pre-tree-unrenderable",
    "equivalence-reach-unavailable",
    "equivalence-profile-unregistered",
    "equivalence-digests-differ",
    #: The POST side's counterpart to `-pre-tree-unrenderable`, added with
    #: `render_post()`'s watchdog (Copilot on #1105 @9ed3def3, suppressed).
    #: The two sides now fail symmetrically: a side that does not finish
    #: rendering is a side that did not render.
    "equivalence-post-stack-unrenderable",
    #: The OBJECT STORE, as against the tree or the ref: a partial clone
    #: whose promisor remote was not consulted (this runner sets
    #: `GIT_NO_LAZY_FETCH=1` so it never is, mid-measurement), a corrupt
    #: pack, a revision whose blobs were never fetched. Separated from
    #: `-pre-tree-unrenderable` because the remedy is a fetch of objects and
    #: not a different `--pre-ref`, and the old message sent operators to
    #: replace a good ref (Copilot, PR #1105 round 6).
    "equivalence-object-store-incomplete",
    "equivalence-unreadable",
)

REMEDIATION = (
    "Remediation: ALL BUT ONE of these refusals are about THE RUN and are "
    "fixed at the run — a missing tag is fetched (`git fetch --tags`), "
    "objects a partial clone never carried are fetched deliberately (`git "
    "fetch origin <commit>`), an unmaterialized leg is initialized (`git "
    "submodule update --init --recursive openDox openXdox`), a leg that is "
    "off its pin or dirty is put back, a post-shed `--pre-ref` is replaced "
    "by a pre-shed one, an unregistered profile is registered. THE ONE THAT "
    "IS NOT, `equivalence-digests-differ`, is a finding about THE PROJECTION "
    "and the "
    "fix is at whichever side moved — never a re-recorded expectation, "
    "because § D6 (4) asks that the two sides AGREE and an expectation "
    "updated to match a drifted side is FLOOR PART 4 deleted. The floor's own "
    "text is `openspec/changes/split-opendox-two-layer-product/design.md` "
    "§ D6 (4) and its box is § 5.5 of that change's tasks.")


class EquivalenceRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so
    a caller can branch on the code without parsing prose, and the vocabulary
    is ENFORCED here rather than only declared above —
    `verify-carve-conformance.py`'s move, taken for its reason: pinning the
    tuple by a test catches a rename of the CONSTANT and not a raise site that
    invented a code the tuple never carried. The exit contract is unaffected:
    this `ValueError` is raised inside `main()`'s try and arrives as
    `equivalence-unreadable`, exit 2.
    """

    def __init__(self, code: str, detail: str,
                 payload: dict[str, Any] | None = None) -> None:
        if code not in REFUSAL_CODES:
            raise ValueError(
                f"{code!r} is not one of this runner's ratified refusal "
                f"codes ({', '.join(REFUSAL_CODES)}); a caller branching on "
                "the vocabulary would never see it")
        self.code = code
        self.detail = detail
        self.payload = payload or {}
        super().__init__(code, detail)

    def render(self, where: str) -> str:
        return f"FAIL {where}: {self.code} — {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# THE PRE SIDE — an archived tree, rendered in a child interpreter
# --------------------------------------------------------------------------

#: The child program. It is the three calls the pre-split determinism suite
#: made (`generate_snapshot(corpus, "fixture-repo", source_revision=PINNED,
#: git=FakeGit())` -> `snapshot.canonical_bytes`) with the conftest's FakeGit
#: inlined, because it executes INSIDE the archived tree and must import
#: nothing of today's.
_PRE_RENDER_PROGRAM = r'''
import os
import sys
from pathlib import Path

scripts_dir = os.environ["EQUIVALENCE_SCRIPTS"]
corpus = os.environ["EQUIVALENCE_CORPUS"]
out_path = os.environ["EQUIVALENCE_OUT"]
revision = os.environ["EQUIVALENCE_REVISION"]
date = os.environ["EQUIVALENCE_DATE"]
repository = os.environ["EQUIVALENCE_REPOSITORY"]
sys.path.insert(0, scripts_dir)


class FakeGit:
    def head_sha(self, repo):
        return revision

    def commit_date(self, repo, rev):
        return date


from ideation_dashboard import snapshot
from ideation_dashboard.generator import generate_snapshot

snap = generate_snapshot(Path(corpus), repository,
                         source_revision=revision, git=FakeGit())
Path(out_path).write_bytes(snapshot.canonical_bytes(snap))
'''


#: Environment names that can silently re-point a `git` read at another
#: object store, and the config channels that can do the same. Scrubbed for
#: `carved_reach._sanitized_git_environment()`'s stated reason and with its
#: vocabulary: a `<revision>:<path>` otherwise resolves through ambient
#: `GIT_DIR` / alternate-object-directory / replace-ref configuration, and
#: this runner's whole claim is that it read ONE named tree.
_SCRUBBED_GIT_ENVIRONMENT = frozenset({
    "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE", "GIT_CEILING_DIRECTORIES", "GIT_REPLACE_REF_BASE",
    "GIT_CONFIG", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_COUNT", "GIT_ATTR_NOSYSTEM", "GIT_NO_REPLACE_OBJECTS",
    "GIT_NO_LAZY_FETCH",
    # `GIT_CONFIG_PARAMETERS` IS THE ONE THAT IS EASY TO MISS, AND IT IS THE
    # WHOLE CHANNEL `git -c` PROPAGATES THROUGH (Copilot, PR #1105 round 2).
    # Disabling the global and system files and dropping the indexed
    # `GIT_CONFIG_KEY_n`/`VALUE_n` pairs leaves ambient `-c` settings — a
    # `core.alternateRefsCommand`, an `include.path` — still reaching these
    # supposedly hermetic object reads. Both of this repository's own scrubs
    # already carry it — `scripts/hermes_runtime_validation/content.py`:16-25
    # and `scripts/carved_reach.py`:796-806 — so this set MATCHES them rather
    # than exceeding them. (An earlier revision of this comment registered the
    # resolver as MISSING it. That was wrong, and Copilot caught it on round 4:
    # measured, `carved_reach._sanitized_git_environment()` drops it.)
    "GIT_CONFIG_PARAMETERS",
})
_INDEXED_GIT_CONFIG_ENVIRONMENT = re.compile(r"GIT_CONFIG_(KEY|VALUE)_\d+")

#: The same 30 seconds `carved_reach._git_run` gives its own reads, for its
#: reason: a partial clone or an unreachable promisor remote can make these
#: HANG rather than fail, and a runner that never returns answers nothing.
_GIT_TIMEOUT = 30

#: The PRE child's own bound. Generous against the measurement — a render of
#: the shipped corpus takes under a second — because it exists to stop a
#: non-terminating renderer hanging a required gate, not to police speed.
_CHILD_TIMEOUT = 300

#: Restoring a caller's timer with a delay of exactly `0` would CANCEL it
#: rather than restore it, so an inherited deadline that passed while the
#: post render held the timer comes back at a millisecond — small enough to
#: be immediate, large enough to be non-zero on any platform's timer
#: granularity. That deadline arrives LATE, which is true, rather than never,
#: which is not. It is reachable because OUR alarm can be DEFERRED: CPython
#: runs a signal handler only between bytecodes, so a pinned leg inside a C
#: extension that holds the GIL delays ours past its own bound.
_TIMER_FLOOR = 1e-3


def _git_environment() -> dict[str, str]:
    environment = {
        name: value for name, value in os.environ.items()
        if name not in _SCRUBBED_GIT_ENVIRONMENT
        and _INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None}
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    # SCRUBBED AND THEN NEVER SET WAS HALF A GUARD (Copilot on #1105
    # @9ed3def3, suppressed). Dropping an inherited `GIT_ATTR_NOSYSTEM` only
    # stops a caller DISABLING the system attributes file; `git archive` then
    # still consults `/etc/gitattributes`, where an `export-ignore` silently
    # changes WHICH FILES the pre-split tree carries. This runner's whole
    # claim is that it read one named tree, so the tree it reads must not vary
    # with the host it is read on.
    environment["GIT_ATTR_NOSYSTEM"] = "1"
    # A MEASUREMENT MUST NOT GO TO THE NETWORK IN THE MIDDLE OF ITSELF.
    # In a partial clone (`--filter=blob:none`, which is how this lane's own
    # clones are made) a read of an absent blob LAZILY FETCHES it from the
    # promisor remote, so `git archive` hangs for as long as the network
    # takes — or for ever, where the remote is unreachable — inside a runner
    # whose whole contract is to refuse rather than hang. Measured on a fresh
    # `--filter=blob:none` clone: with this set the archive fails `fatal:
    # could not fetch <oid> from promisor remote` (rc 128); without it the
    # same command exits 0 after a silent fetch. That failure is recognised
    # by name below, with the fetch the operator should run deliberately — so
    # the network happens on their word, and not inside the measurement.
    environment["GIT_NO_LAZY_FETCH"] = "1"
    return environment


#: What git says when an object it needs is not in the store and it was not
#: allowed to fetch it. MEASURED, on a `--filter=blob:none` clone archiving a
#: tag whose blobs the checkout never materialized — which is this runner's
#: own case, since `opendox-carve-0` is far behind any working tree:
#:
#:     warning: lazy fetching disabled; some objects may not be available
#:     fatal: could not fetch d943254485e0… from promisor remote
#:
#: (rc 128; the same archive without `GIT_NO_LAZY_FETCH=1` exits 0 after a
#: silent fetch). The remaining spellings are git's own for the same
#: condition met by another route: a promisor remote that is configured but
#: unreachable, and an object simply absent. A pathspec that matches nothing
#: — the other way `git archive` fails — matches NONE of these, and is left
#: to the generic diagnosis below it.
#: And what `git archive` says when NO path matched — measured:
#: `fatal: pathspec 'scripts/doc_health' did not match any files`. It fails
#: before writing anything, so a tree carrying neither archive path never
#: reaches the per-row check further down and must be diagnosed here.
_NO_PATHSPEC = re.compile(r"pathspec .* did not match|did not match any file",
                          re.IGNORECASE)

_PARTIAL_CLONE = re.compile(
    r"promisor remote|could not fetch|lazy fetch"
    r"|could not read from remote|missing (?:blob|object|tree)"
    r"|not a (?:tree|blob|commit) object|unable to read .{0,20}object",
    re.IGNORECASE)


def _git(repo: Path, *arguments: str, text: bool = True):
    """The ONE scrubbed, replacement-free, bounded `git -C <repo> …` here.

    `carved_reach._git_run`'s discipline, restated locally rather than
    imported: that helper is private to the resolver and this file is a
    command-line entry point, so borrowing it would couple an operator's
    runner to another module's underscore. Returns `None` when git could not
    be run at all or did not answer in time — never a partial answer wearing
    a successful one's clothes (Copilot, PR #1105).
    """
    try:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), *arguments],
            capture_output=True, text=text, check=False,
            timeout=_GIT_TIMEOUT, env=_git_environment())
    except subprocess.TimeoutExpired:
        return None
    except OSError:  # pragma: no cover - no git on PATH: the caller's
        return None            # problem, and it fails everywhere else too


def pre_ref_commit(pre_ref: str, repo: Path) -> str:
    """The commit `--pre-ref` names, or the refusal that names the fetch.

    Separated from the archive below so that "this checkout has never heard of
    that ref" and "that ref's tree carries no renderer" are DIFFERENT findings.
    They have different remedies and only one of them is an operator error
    about the run rather than about the tree.
    """
    # `--end-of-options` BEFORE the revision, so a `--pre-ref` that begins
    # with a dash is read as a REVISION and not as a git option (Copilot,
    # PR #1105). It is command-line input, and the boundary belongs here.
    done = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
                f"{pre_ref}^{{commit}}")
    if done is None:
        # A QUERY THAT DID NOT ANSWER HAS NOT ESTABLISHED THAT THE REF IS
        # ABSENT (Copilot, PR #1105 round 3). `_git()` answers `None` for a
        # timeout and for a missing git as well as for a process that could
        # not start, and telling an operator to `git fetch --tags` because a
        # promisor remote hung would send them to fix the wrong thing. The
        # named code stays for a COMPLETED, nonzero `rev-parse`.
        raise EquivalenceRefusal(
            "equivalence-unreadable",
            f"`git rev-parse` for {pre_ref!r} in {repo} could not be run or "
            f"did not answer within {_GIT_TIMEOUT}s, so this run never "
            "learned whether that ref exists. A partial clone whose promisor "
            "remote is unreachable hangs here rather than failing, and an "
            "unanswered query is not the repository's answer that the ref is "
            "absent")
    if done.returncode != 0 or not done.stdout.strip():
        raise EquivalenceRefusal(
            "equivalence-pre-ref-unreachable",
            f"{pre_ref!r} resolves to no commit in {repo}. The default is the "
            f"published annotated tag {DEFAULT_PRE_REF!r} (FLOOR PART 1's own "
            "carve_commit, frozen by RULED (a), `#656` comment `5625573095`) "
            "— run `git fetch --tags` in this checkout, or name a pre-shed "
            "revision this clone already carries. A shallow or "
            "single-branch clone reaches it with `git fetch --tags "
            "--unshallow`; `.github/workflows/pytest-suite.yml` checks out "
            "with `fetch-depth: 0` for exactly this reason")
    return done.stdout.strip()


def _absence(repo: Path, commit: str) -> str | None:
    """WHICH of the archive paths that commit's tree does not carry, or
    `None` when this runner could not establish that at all.

    `git archive` fails as soon as ONE pathspec matches nothing, so the
    refusal above must not assume both are missing. And `None` is not a
    phrasing problem, which is what the first version of this treated it as
    (Copilot, PR #1115): a tree read that FAILED may be an incomplete object
    store rather than a shed renderer, so the caller must drop the post-shed
    DIAGNOSIS too — not merely soften its wording — because that diagnosis
    ends "the objects are not the problem", which is exactly what an
    unanswered read cannot establish.
    """
    missing: list[str] = []
    for path in ARCHIVE_PATHS:
        done = _git(repo, "ls-tree", "--name-only", commit, "--", path)
        if done is None or done.returncode != 0:
            return None
        if not done.stdout.strip():
            missing.append(path)
    if not missing:
        return None
    if len(missing) == len(ARCHIVE_PATHS):
        return "carries NEITHER " + " nor ".join(ARCHIVE_PATHS)
    carried = [path for path in ARCHIVE_PATHS if path not in missing]
    return (f"carries {' and '.join(carried)} but NOT "
            + " nor ".join(missing))


def extract_pre_tree(pre_commit: str, repo: Path, into: Path,
                     pre_ref: str) -> Path:
    """`git archive` the pre-split renderer into a scratch tree.

    THE RESOLVED COMMIT IS WHAT IS ARCHIVED, never the raw `--pre-ref` a
    second time. `main()` resolves the ref once and the evidence line quotes
    THAT commit; re-resolving a mutable name here would let a branch or a
    force-updated tag move between the two reads and leave the runner
    recording commit A while rendering commit B (Copilot, PR #1105). The ref
    is still carried, for the messages — a refusal that named a sha and not
    the name the operator typed would be a worse refusal.

    A `git worktree` would also work and is deliberately not used: it mutates
    the repository's administrative state, and openxFactory's own doc-health
    misreports from inside one (`release-inventory-drift` reports four extra
    errors in a worktree regardless of commit). An archive touches nothing.
    """
    into.mkdir(parents=True, exist_ok=True)
    # NO `--end-of-options` HERE, and `git archive` is why: it would make the
    # `--` separator itself a pathspec (measured: `fatal: pathspec '--' did
    # not match any files`). The guarantee the marker gives `rev-parse` is
    # already held a better way — what arrives here is a RESOLVED 40-hex
    # commit, which cannot be read as an option at all.
    archive = _git(repo, "archive", "--format=tar", pre_commit, "--",
                   *ARCHIVE_PATHS, text=False)
    if archive is None:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"`git archive {pre_commit}` did not answer within "
            f"{_GIT_TIMEOUT}s. A partial clone whose promisor remote is "
            "unreachable hangs here rather than failing, and a query that "
            "went unanswered is not a tree that carries nothing")
    if archive.returncode != 0:
        stderr = archive.stderr.decode("utf-8", "replace").strip()
        # THE OBJECT STORE IS NOW ITS OWN FINDING, AND IT IS THE LIKELIEST
        # ONE HERE (Copilot, PR #1105 round 6). This runner sets
        # `GIT_NO_LAZY_FETCH=1`, so in a partial clone an absent blob FAILS
        # instead of quietly fetching, and the failure lands exactly here.
        # Telling that operator the tree carries no renderer would send them
        # to replace a good `--pre-ref`; what they need is the objects, and
        # the fetch that gets them.
        if _PARTIAL_CLONE.search(stderr):
            raise EquivalenceRefusal(
                "equivalence-object-store-incomplete",
                f"`git archive {pre_commit}` ({pre_ref}) could not read the "
                f"objects it needs: {stderr or '(no error output)'}. This is "
                "a PARTIAL OR INCOMPLETE OBJECT STORE, not a tree without a "
                "renderer and not a post-shed ref. A `--filter=blob:none` "
                "clone carries the commits but not their blobs, and this "
                "runner refuses to fetch them mid-measurement "
                "(`GIT_NO_LAZY_FETCH=1`): a gate that reaches for the "
                "network is a gate that hangs when the network is not "
                f"there. Fetch them deliberately — `git -C {repo} fetch "
                f"origin {pre_commit}` — or use a clone without a partial "
                "filter, then re-run")
        # AND THE PATHSPEC FAILURE IS THE POST-SHED REF, NAMED AS ONE
        # (Copilot, PR #1115). `git archive` fails before it writes anything
        # when NO path matches, so a tree that carries neither archive path
        # never reaches the per-row check below — and until the object store
        # got its own code above, this message was written for the store
        # case and told that operator to fetch objects before changing
        # `--pre-ref`, which is precisely backwards for a ref whose tree has
        # shed the renderer. Both halves are classified now, so neither
        # borrows the other's remedy.
        if _NO_PATHSPEC.search(stderr):
            # AND IT SAYS WHICH PATH, BECAUSE `git archive` FAILS ON ANY ONE
            # OF THEM (Copilot, PR #1115). The first wording said the tree
            # carried NEITHER archive path, which is only true when both are
            # absent — a tree that shed one of them would have been described
            # inaccurately in the refusal that names it.
            absence = _absence(repo, pre_commit)
            if absence is None:
                raise EquivalenceRefusal(
                    "equivalence-pre-tree-unrenderable",
                    f"`git archive {pre_commit}` ({pre_ref}) matched none of "
                    + " or ".join(ARCHIVE_PATHS)
                    + f": {stderr or '(no error output)'}. This runner then "
                    "could not read that commit's tree to say WHICH of them "
                    "is missing, so it does NOT claim the ref is post-shed: "
                    "a tree read that failed may itself be an incomplete "
                    f"object store. Ask it directly — `git -C {repo} ls-tree "
                    f"{pre_commit[:12]} -- " + " ".join(ARCHIVE_PATHS)
                    + "` — before changing --pre-ref")
            raise EquivalenceRefusal(
                "equivalence-pre-tree-unrenderable",
                f"{pre_ref} ({pre_commit[:12]}) "
                + absence
                + f": {stderr or '(no error output)'}. `contract-v4.0` and "
                "every commit on `main` since the § 5.2 shed are in exactly "
                "this state. A post-shed ref is an operator error about "
                f"--pre-ref, not a pass: name {DEFAULT_PRE_REF!r} or another "
                "pre-shed revision. The objects are not the problem — the "
                "ref resolved and git read its tree well enough to know "
                "these paths are not in it")
        # AND WHAT IS LEFT IS UNDIAGNOSED, WHICH THIS SAYS RATHER THAN
        # GUESSES AT. The two conditions an archive fails under here are
        # classified above; a third — a permission error, a full disk, a git
        # that broke in a way this file has not met — gets its stderr and
        # both remedies as POSSIBILITIES, because a confident wrong
        # diagnosis is what the two branches above exist to stop.
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"`git archive {pre_commit}` ({pre_ref}) FAILED: "
            + (stderr or "(no error output)")
            + ". The ref itself resolved and this runner cannot tell from "
            "that output which condition it met — it is neither the object "
            "store nor a pathspec that matched nothing, both of which are "
            "reported by name. Read the error above: if objects are missing, "
            f"`git -C {repo} fetch origin {pre_commit}`; if the tree has "
            "shed the renderer, name a pre-shed --pre-ref. Whether the tree "
            "carries the renderer is answered separately, below")
    _extract_safely(archive.stdout, into, pre_ref)
    for row in (GENERATOR_ROW, SNAPSHOT_ROW):
        if not (into / row).is_file():
            raise EquivalenceRefusal(
                "equivalence-pre-tree-unrenderable",
                f"{pre_ref} carries no {row}. `contract-v4.0` and every "
                "commit on `main` since the § 5.2 shed are in exactly this "
                "state — their `ideation_dashboard` package survives without "
                "its renderer and importing it raises `ImportError: cannot "
                "import name 'snapshot'`. A post-shed ref is an operator "
                f"error about --pre-ref, not a pass: name {DEFAULT_PRE_REF!r} "
                "or another pre-shed revision")
    return into


def _extract_safely(archive_bytes: bytes, into: Path, pre_ref: str) -> None:
    """Extract the archive IN-PROCESS, with every member checked first.

    `tar -x` was the first spelling and it was two holes at once (Copilot, PR
    #1105 round 7): GNU tar reads `TAR_OPTIONS` out of the ambient
    environment, so a caller could alter the extraction of a file this runner
    is about to import; and a member that is a SYMLINK, a hard link, a device
    or a path escaping `into` would be written as given, which is how an
    archive reaches outside the directory that is supposed to contain it. The
    isolation the `-I` child rests on is the isolation of THIS directory, so a
    member that leaves it defeats the measurement rather than merely being
    untidy.

    `tarfile` with `filter="data"` is the standard library's own answer to
    exactly this (CVE-2007-4559's remediation) and it is applied as well as
    the explicit check, not instead of it: the check states the rule in this
    file, in terms a reader can hold against the refusal.
    """
    rejected: list[str] = []
    members: list[tarfile.TarInfo] = []
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r|") as bundle:
        for member in bundle:
            name = member.name
            if not (member.isreg() or member.isdir()):
                rejected.append(f"{name} ({member.type!r}, not a regular "
                                "file or a directory)")
                continue
            target = Path(name)
            if target.is_absolute() or ".." in target.parts:
                rejected.append(f"{name} (escapes the extraction directory)")
                continue
            members.append(member)
            bundle.extract(member, path=into, filter="data")
    if rejected:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"the {pre_ref} archive carries members this runner will not "
            f"extract:\n" + "\n".join(f"    {row}" for row in rejected[:20]) +
            "\nA pre-split tree is read for its Python modules; a symlink, a "
            "device or a path leaving the extraction directory would let the "
            "isolated child read bytes from outside the archive, which is the "
            "isolation this measurement rests on")
    if not members:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"the {pre_ref} archive is empty, so there is no pre-split tree "
            "to render")


def _run_pre_child(tree: Path, corpus: Path, out: Path,
                   source_revision: str) -> subprocess.CompletedProcess:
    """The one child-interpreter invocation, BOUNDED. Separated so the
    timeout and the call it bounds are one thing to read.

    THE INPUTS TRAVEL IN THE ENVIRONMENT AND NOT IN ARGV (Copilot, PR #1105
    round 10; SonarCloud `pythonsecurity:S8705`, the last one open on this
    file). `--corpus` is operator input, and argv is the one channel where a
    value's POSITION decides how it is read: the program is passed to `-c`,
    so everything after it is `sys.argv[1:]` and a mis-ordered or empty
    element silently shifts the tuple unpack — the corpus becoming the output
    path, the revision becoming the corpus. Environment entries are read BY
    NAME, and a name that is missing raises `KeyError` in the child rather
    than rendering something else. `-I` implies `-E`, which ignores the
    `PYTHON*` variables only, so these six arrive intact; the ambient
    environment is carried forward unchanged beneath them, because the child
    imports PyYAML out of the same site-packages this process uses.
    """
    return subprocess.run(
        [sys.executable, "-I", "-c", _PRE_RENDER_PROGRAM],
        capture_output=True, text=True, check=False, timeout=_CHILD_TIMEOUT,
        env={**os.environ,
             "EQUIVALENCE_SCRIPTS": str(tree / "scripts"),
             "EQUIVALENCE_CORPUS": str(corpus),
             "EQUIVALENCE_OUT": str(out),
             "EQUIVALENCE_REVISION": source_revision,
             "EQUIVALENCE_DATE": PINNED_COMMIT_DATE,
             "EQUIVALENCE_REPOSITORY": REPOSITORY_NAME})


def render_pre(tree: Path, corpus: Path, scratch: Path, pre_ref: str,
               source_revision: str) -> bytes:
    """The archived tree's canonical snapshot bytes, from a child interpreter.

    THE SEPARATE PROCESS is what carries the isolation; `-I` closes ONE of the
    two doors the `sys.path.insert` leaves open. The insert wins every name the
    archived tree HAS, but a name it LACKS — a submodule dropped from the
    archive, a helper a future pre-shed ref imports — falls through to whatever
    comes next, and a `PYTHONPATH`, a script directory or a user-site copy
    would then silently complete a partial archive out of ANOTHER CHECKOUT.
    Those `-I` removes.

    WHAT IT DOES NOT REMOVE, SAID PLAINLY BECAUSE THIS DOCSTRING USED TO CLAIM
    OTHERWISE (Copilot, PR #1105 round 3): the interpreter's SYSTEM
    site-packages. An installed distribution can still complete a partial
    archive. `-S` is not used, and the reason is measured: the archived
    `doc_health` imports PyYAML, so `python3 -S` cannot import
    `ideation_dashboard.generator` at all — `ModuleNotFoundError: No module
    named 'yaml'`. The remaining exposure is narrow and SYMMETRIC: it is the
    same interpreter and the same installed distributions the POST side runs
    on, so an installed package cannot make the two sides agree where the
    projection does not.
    """
    # ONE OUTPUT PATH PER CORPUS STATE, AND THE PREVIOUS ONE IS REMOVED
    # FIRST (Copilot, PR #1105 round 8). `--corpus` is repeatable and every
    # state shared this file: a child that exited 0 WITHOUT writing — a
    # renderer that returns early, a permitted pre-shed ref whose entry point
    # differs — would leave `out.is_file()` true from the state before, and
    # this state would then be compared against the PREVIOUS state's bytes.
    # Against a post side rendered for the current corpus that is a false
    # DIFFERENCE, and against a repeated corpus a false EQUIVALENCE; either
    # way it is the last thing this runner may do, which is answer about a
    # measurement it did not take. The name carries the corpus, and the file
    # is unlinked before the child runs, so "no output" stays refusable.
    stamp = hashlib.sha256(str(corpus).encode("utf-8")).hexdigest()[:16]
    out = scratch / f"pre-{stamp}.json"
    out.unlink(missing_ok=True)
    try:
        done = _run_pre_child(tree, corpus, out, source_revision)
    except subprocess.TimeoutExpired as exc:
        # THE ONLY CHILD THAT WAS UNBOUNDED (Copilot, PR #1105 round 7).
        # `--pre-ref` accepts any pre-shed revision, so a renderer that
        # loops — or a corpus it cannot finish — would hang a REQUIRED gate
        # rather than refuse. The git reads and the archive were already
        # bounded; this one is now too, and a timeout is a tree that did not
        # render, which is exactly what this refusal says.
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"the {pre_ref} tree at {tree} did not finish rendering {corpus} "
            f"within {_CHILD_TIMEOUT}s. A pre-split render of the shipped "
            "corpus takes under a second, so a run that reaches this limit "
            "has met a renderer or a corpus that does not terminate") from exc
    if done.returncode != 0 or not out.is_file():
        tail = (done.stderr or done.stdout).strip().splitlines()
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"the {pre_ref} tree at {tree} did not render {corpus}: "
            f"{tail[-1] if tail else f'exit {done.returncode}, no output'}")
    return out.read_bytes()


# --------------------------------------------------------------------------
# THE POST SIDE — this repository's own composition of the two pins
# --------------------------------------------------------------------------

class FakeGit:
    """The injected git both sides get, so `generation.source_revision` and any
    derived `generated_at` are pinned rather than read off a moving HEAD."""

    def __init__(self, head: str = PINNED_SOURCE_REVISION,
                 date: str = PINNED_COMMIT_DATE) -> None:
        self._head = head
        self._date = date

    def head_sha(self, repo) -> str:
        return self._head

    def commit_date(self, repo, revision: str) -> str:
        return self._date


def post_stack(register_profile: bool = True):
    """`(generator, snapshot)` at the pinned legs, through the ONE reach.

    `carved_reach.require()` first, and EAGERLY: `install()` defers its refusal
    to the name that is asked for, which is right for a conftest that runs in
    every invocation and wrong for an entry point that is about to reach either
    way. Its own docstring says so.
    """
    # THE NO-NETWORK GUARANTEE MUST COVER THE WHOLE MEASUREMENT, AND THIS
    # FILE'S `_git()` IS NOT THE WHOLE OF IT (Copilot, PR #1115).
    # `carved_reach._git_run()` is a SHARED reader with its own sanitizer,
    # and that sanitizer builds from `os.environ` minus a scrub list which
    # does not contain this name (measured: `carved_reach.py:796-806`, and
    # `"GIT_NO_LAZY_FETCH" in _sanitized_git_environment()` is True once it
    # is set here). So the guard is set on THE PROCESS, before the reach is
    # imported: a manifest or tree read on the post side would otherwise
    # still lazy-fetch from a promisor remote in a partial clone — the one
    # thing `GIT_NO_LAZY_FETCH` exists here to stop — and would do it in the
    # half of the run this file does not issue the git commands for. It
    # outlives the call, which is what a process-wide guarantee means.
    os.environ["GIT_NO_LAZY_FETCH"] = "1"
    import carved_reach
    try:
        carved_reach.require()
    except carved_reach.CarveReachUnavailable as exc:
        raise EquivalenceRefusal(
            "equivalence-reach-unavailable", str(exc)) from exc
    carved_reach.install()
    if register_profile:
        # NOT WRAPPED, AND THAT IS THE POINT (Copilot, PR #1105).
        # `register_openxfactory()` raises `AlreadyRegistered` when some other
        # profile already holds the process, and the composite can refuse a
        # malformed declaration; neither is "no profile is registered", and a
        # refusal that called them that would send an operator to run the
        # registration that is already the problem. They reach the blanket
        # instead and arrive as `equivalence-unreadable` NAMING the exception,
        # which is what `equivalence-unreadable` is for.
        # `equivalence-profile-unregistered` is reserved for the one failure
        # it describes: the engine asked for a profile and found none.
        import opendox_host
        opendox_host.register_openxfactory()
    return (carved_reach.module(GENERATOR_ROW),
            carved_reach.module(SNAPSHOT_ROW))


def post_side_identity(stack, pins: dict[str, str]) -> dict[str, Any]:
    """What the post side ACTUALLY IS, derived from the resolved modules.

    `carved_reach.module()` answers from the MANIFEST ROW, so which leg a row
    arrives at is a fact about a document and a `re_destined:` block can move
    it (RULED Q6, `#656` comment `5648044785`). A verdict that spelled
    `openxdox.generator` and `openXdox-code` into its own text would then
    render the new modules and report the old leg — the evidence line naming a
    pin that did not render, one more time and by a route the pin checks
    cannot see (Copilot, PR #1105 round 3). Nothing below is spelled: the
    dotted names come off the imported modules and the leg comes off where
    their files are.
    """
    def leg_of(module) -> str:
        origin = Path(getattr(module, "__file__", "") or "").resolve()
        for candidate in sorted(pins, key=len, reverse=True):
            root = (ROOT / candidate).resolve()
            if origin == root or root in origin.parents:
                return candidate
        return "unresolved"

    # PER ROW, NOT PER STACK (Copilot, PR #1105 round 4).
    # `carved_reach.module()` resolves the generator row and the snapshot row
    # INDEPENDENTLY, and a `re_destined:` block is per row, so the two can
    # legitimately arrive at different legs. Deriving one leg from the
    # generator alone and printing it for both would make the evidence line
    # false in exactly the case this derivation exists to survive. A mixed
    # stack is not refused — the manifest permits it — it is REPORTED.
    resolved = [(module.__name__, leg_of(module)) for module in stack]
    # FAIL-CLOSED, and the first revision of this function was not (Copilot,
    # PR #1105 round 5). A module resolving OUTSIDE every verified pin root is
    # a post side this run cannot name a commit for, and printing a label with
    # no sha while exiting 0 is the "silence reads as a pass" failure the whole
    # file is built to refuse. The lawful cases are covered: a `re_destined:`
    # row moves a module BETWEEN the legs, and both legs are verified.
    stray = [name for name, leg in resolved if leg == "unresolved"]
    if stray:
        raise EquivalenceRefusal(
            "equivalence-reach-unavailable",
            f"{', '.join(stray)} resolved to a file outside every verified "
            f"pin root ({', '.join(sorted(pins))}), so this run cannot say "
            "which commit rendered the post side. `carved_reach` is the one "
            "place this repository reaches into the pinned legs; a module "
            "arriving from anywhere else is an unpinned stack wearing a "
            "pinned stack's name, and a verdict naming no commit is not a "
            "verdict")
    modules = " + ".join(name for name, _ in resolved)
    legs: list[str] = []
    for _, leg in resolved:
        if leg not in legs:
            legs.append(leg)
    parts = [f"{leg} {pins[leg][:12]}" if pins.get(leg) else leg
             for leg in legs]
    label = (f"{modules} at the pinned {parts[0]}" if len(parts) == 1 else
             f"{modules} at the pinned " + " and ".join(parts) +
             " (a MIXED-leg stack)")
    return {"post_modules": modules,
            "post_leg": legs[0],
            "post_leg_commit": pins.get(legs[0], ""),
            "post_legs": legs,
            "post_module_legs": {name: leg for name, leg in resolved},
            "post_label": label}


class _RenderTimeout(BaseException):
    """The watchdog fired. Never leaves `render_post()` — it is re-raised
    there as a named refusal.

    It derives from `BaseException` and not from `Exception` for the reason
    `KeyboardInterrupt` and `asyncio.CancelledError` do. It is not a failure
    OF the renderer that the renderer might reasonably handle; it is this
    file taking control BACK from it. And the renderer is PINNED THIRD-PARTY
    CODE: an ordinary `except Exception:` anywhere inside it — a retry, a
    cleanup, a "log and carry on" — would consume the alarm and return as
    though the render had finished, turning the refusal this file promises
    into a silent verdict computed from whatever was half-built when the
    alarm landed (Copilot on #1110, thread r4047-`_RenderTimeout`).
    """


def arm_render_watchdog(seconds: float):
    """Bound the IN-PROCESS post render, or answer `None` where it cannot be.

    THE POST SIDE STAYS IN THIS PROCESS, so the PRE child's `timeout=` is not
    available to it — and that placement is deliberate rather than incidental:
    it is the only stack this process has imported, and the PRE side, the one
    that would collide with it, is already in a child of its own. Moving it
    out to gain a timeout would undo the thing the timeout is protecting.

    So the bound is a `SIGALRM` watchdog instead. Without one, a
    non-terminating regression in a FUTURE pinned leg — the post side is a pin
    that MOVES, which is this runner's whole reason to exist — hangs the
    required `pytest-suite` job until its own 35-minute limit rather than
    returning the refusal this file promises for every other failure.

    Answers `None`, and the render then runs unbounded, where a watchdog is
    not available: a platform with no `SIGALRM`, or a caller on a thread that
    is not the main one, where `signal.signal` raises. Degrading there is
    right — the alternative is refusing a run for the interpreter's shape
    rather than for anything about the projection — and it is the ONLY place
    in this file that degrades rather than refusing, which is why it says so.

    A CALLER'S OWN DEADLINE IS NOT OURS TO CANCEL. A process gets ONE
    `ITIMER_REAL`, so arming ours destroys whatever an embedding harness set
    — `pytest-timeout` in its `signal` method, a supervising runner, a caller
    that bounded this whole verification. Where the inherited deadline is
    EARLIER than the bound asked for here, arming would LOOSEN it, so we
    leave it alone and answer `None`: the render runs under the caller's
    tighter bound, which is what that bound was set for. Where it is later,
    we arm, and `disarm()` puts back what is LEFT of it — floored just above
    zero, so a deadline that expired while we rendered fires the moment
    control returns rather than never — with its interval and its handler
    (Copilot on #1110, suppressed).
    """
    if not (hasattr(signal, "SIGALRM") and hasattr(signal, "setitimer")
            and hasattr(signal, "getitimer")):
        return None
    if threading.current_thread() is not threading.main_thread():
        return None
    inherited, interval = signal.getitimer(signal.ITIMER_REAL)
    if inherited and inherited <= seconds:
        return None
    armed_at = time.monotonic()

    def _fire(signum, frame):  # noqa: ARG001 - the handler signature
        raise _RenderTimeout(seconds)

    previous = signal.signal(signal.SIGALRM, _fire)
    signal.setitimer(signal.ITIMER_REAL, seconds)

    def disarm() -> None:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        if inherited:
            left = inherited - (time.monotonic() - armed_at)
            signal.setitimer(signal.ITIMER_REAL,
                             max(left, _TIMER_FLOOR), interval)

    return disarm


def render_post(stack, corpus: Path, source_revision: str) -> bytes:
    """The pinned stack's canonical snapshot bytes, in THIS interpreter.

    The post side needs no subprocess: it is the only stack this process has
    imported, and the pre side — the one that would collide with it — is
    already in a child of its own.

    A `DomainProfileNotRegistered` from the engine arrives as a NAMED refusal
    rather than a traceback, because it is the one failure an operator can
    cause simply by composing the run themselves: the arrived generator reads
    `"picked"` and `"staged"` through `domain_profile.current()` where the
    pre-split blob held the literals (RULING C2, § 4.4), so with no profile
    registered it refuses instead of rendering openXdox's own words.
    """
    generator, snapshot = stack
    disarm = arm_render_watchdog(_CHILD_TIMEOUT)
    try:
        snap = generator.generate_snapshot(
            corpus, REPOSITORY_NAME, source_revision=source_revision,
            git=FakeGit(head=source_revision))
        # CANONICALIZATION IS INSIDE THE BOUND. It is the snapshot leg's own
        # code, this function promises canonical BYTES rather than an object,
        # and a pinned leg that does not terminate while SERIALIZING hangs
        # the gate exactly as one that does not terminate while generating
        # does (Copilot on #1110, thread r4047-canonicalization).
        rendered = snapshot.canonical_bytes(snap)
    except _RenderTimeout as exc:
        raise EquivalenceRefusal(
            "equivalence-post-stack-unrenderable",
            f"the pinned post-split stack did not finish rendering {corpus} "
            f"within {_CHILD_TIMEOUT}s. A render of the shipped corpus takes "
            "under a second, so a run that reaches this limit has met a "
            "pinned leg that does not terminate — which is exactly what a "
            "gate over a MOVING pin exists to catch, and it must arrive as a "
            "refusal rather than as a job that ran out of time") from exc
    except Exception as exc:  # noqa: BLE001 - narrowed by name below
        if type(exc).__name__ == "DomainProfileNotRegistered":
            raise EquivalenceRefusal(
                "equivalence-profile-unregistered",
                f"{type(exc).__name__}: {exc}") from exc
        raise
    finally:
        if disarm is not None:
            disarm()
    return rendered


# --------------------------------------------------------------------------
# the comparison
# --------------------------------------------------------------------------

def _pretty(raw: bytes) -> list[str]:
    """Canonical bytes as indented, key-sorted JSON lines, for the diff.

    Falls back to the raw text where the bytes are not JSON at all, so a
    refusal about a difference never turns into a refusal about this function.
    """
    try:
        return json.dumps(json.loads(raw.decode("utf-8")), indent=2,
                          sort_keys=True).splitlines()
    except Exception:  # noqa: BLE001 - see the docstring
        return raw.decode("utf-8", "replace").splitlines()


def _first_byte_difference(pre: bytes, post: bytes) -> str:
    """Where two byte strings first part company, in words an operator can
    act on — for the case where no TEXT difference survives decoding."""
    for offset in range(min(len(pre), len(post))):
        if pre[offset] != post[offset]:
            low = max(0, offset - 8)
            high = offset + 8
            return (f"first differing byte at offset {offset}: "
                    f"PRE {pre[low:high]!r} / POST {post[low:high]!r}")
    return (f"one side is a prefix of the other: {len(pre)} vs {len(post)} "
            "bytes, equal up to the shorter")


def projected_documents(raw: bytes) -> int | None:
    """How many documents a rendered snapshot projects, or `None` when the
    bytes are not a snapshot at all."""
    try:
        return len(json.loads(raw.decode("utf-8")).get("documents") or [])
    except Exception:  # noqa: BLE001 - a caller that must not crash on this
        return None


def compare(pre: bytes, post: bytes, corpus: Path, pre_ref: str,
            post_label: str) -> dict[str, Any]:
    """One corpus state's verdict, or the refusal that NAMES the field.

    A refusal that printed two hex strings would tell an operator that
    something moved and nothing about what. The unified diff is what makes a
    red run actionable, and it is of the canonical JSON rather than of the
    bytes because the canonical form is one line.
    """
    # AN EXISTING DIRECTORY IS NOT A CORPUS (Copilot, PR #1105 round 7). The
    # `is_dir()` guard in `main()` catches a path that is not there; it does
    # NOT catch one that is there and EMPTY, or pointed at the wrong root. The
    # reader then projects nothing, both sides render the same vacuous
    # snapshot, and the run reports OK — which is the precise false pass that
    # guard exists to prevent, arriving through the case it does not cover.
    # Asked of the RENDERED snapshot rather than of the directory's globs: the
    # engine's own answer about what it read beats this file's guess at what
    # it should have.
    projected = projected_documents(pre)
    if not projected:
        raise EquivalenceRefusal(
            "equivalence-unreadable",
            f"{corpus} projected {0 if projected == 0 else 'no readable'} "
            "document(s), so both sides rendered the same empty snapshot and "
            "would have compared equal. An empty directory, or one pointed at "
            "the wrong root, is not a corpus: silence must not read as a pass")
    pre_digest = hashlib.sha256(pre).hexdigest()
    post_digest = hashlib.sha256(post).hexdigest()
    state = {"corpus": str(corpus), "documents": projected,
             "pre_bytes": len(pre),
             "post_bytes": len(post), "pre_sha256": pre_digest,
             "post_sha256": post_digest, "equivalent": pre == post}
    if pre == post:
        return state
    diff = list(difflib.unified_diff(
        _pretty(pre), _pretty(post),
        fromfile=f"PRE  {pre_ref}", tofile=f"POST {post_label}", lineterm=""))
    if not diff:
        # A FORMATTING-ONLY DIFFERENCE STILL HAS TO BE SHOWN (Copilot, PR
        # #1105 round 3). `_pretty()` re-serializes and splits lines, which
        # ERASES exactly the differences the byte comparison exists to catch
        # at the margin — a canonical trailing newline, indentation, key
        # order — and an `equivalence-digests-differ` whose diff is empty is
        # the refusal without the half that makes it actionable. Fall back to
        # the raw text with line endings visible.
        diff = list(difflib.unified_diff(
            [repr(line) for line in
             pre.decode("utf-8", "replace").splitlines(keepends=True)],
            [repr(line) for line in
             post.decode("utf-8", "replace").splitlines(keepends=True)],
            fromfile=f"PRE  {pre_ref} (raw)",
            tofile=f"POST {post_label} (raw)", lineterm=""))
    if not diff:
        # AND THE LAST RESORT MUST NOT INVENT A CAUSE (Copilot, PR #1105
        # round 9). The earlier wording said "they differ in length alone"
        # and then printed two EQUAL lengths whenever both sides carried
        # distinct invalid UTF-8 that `decode(errors="replace")` flattened to
        # the same text — a false diagnostic in the one place an operator has
        # nothing else to read. This states what is actually known: where the
        # bytes first part company, or that one is a prefix of the other.
        diff = [f"(no line differs after decoding; the difference is at the "
                f"BYTE level — {_first_byte_difference(pre, post)})"]
    shown = diff[:DIFF_LINE_CAP]
    if len(diff) > DIFF_LINE_CAP:
        shown.append(f"  … {len(diff) - DIFF_LINE_CAP} more diff line(s); "
                     "re-run with --json for the whole diff")
    state["diff"] = diff
    raise EquivalenceRefusal(
        "equivalence-digests-differ",
        f"over {corpus} the two sides rendered DIFFERENT snapshots.\n"
        f"  PRE  {pre_ref}: {len(pre)} bytes, sha256 {pre_digest}\n"
        f"  POST {post_label}: {len(post)} bytes, sha256 "
        f"{post_digest}\n" + "\n".join(shown),
        payload=state)


#: The remedy the reach refusals name, kept in one place so the two that quote
#: it cannot drift apart.
INIT_COMMAND_HINT = ("git submodule update --init --recursive "
                     "openDox openXdox")

#: The two nested legs, as (parent repository, gitlink path) pairs read in
#: order: openxFactory records `openDox`, `openDox` records `code`. Both
#: levels are checked, because a run reads modules out of the INNER one and
#: only the outer pin is what an openxFactory commit declares.
#: PARENTS COME BEFORE THEIR CHILDREN, and `verify_pins()` depends on it: a
#: nested gitlink is read out of the exact commit the parent's own row
#: verified, so that row must already have run. A test asserts the ordering.
LEG_GITLINKS: tuple[tuple[str, str], ...] = (
    (".", "openDox"), ("openDox", "code"), ("openDox", "spec"),
    (".", "openXdox"), ("openXdox", "code"), ("openXdox", "spec"),
)


#: What `recorded_gitlink()` answers as its SOURCE when it found no gitlink:
#: naming both places it looked, because "records no gitlink in HEAD" would
#: leave a reader wondering about the index.
_NO_RECORD_SOURCE = "HEAD or the index"


def _gitlink_at_commit(parent: Path, outer: str,
                       path: str) -> tuple[str | None, str]:
    """The gitlink `path` has IN THE TREE of the commit `outer`."""
    source = f"the commit {outer[:12]} its own parent records for it"
    oid, kind = _gitlink_in_tree(parent, outer, path)
    if oid is None and kind is not None:
        return None, f"{source} — it records a {kind} at that path, not a "\
                     "submodule"
    return oid, source


def _gitlink_in_tree(parent: Path, revision: str,
                     path: str) -> tuple[str | None, str | None]:
    """(oid, note) for the gitlink `revision`'s tree carries at `path`.

    `oid` is `None` both when the path is ABSENT (note `None`) and when
    something that is not a submodule sits there (note names what does), and
    an unreadable tree RAISES rather than answering either.

    # ONE `ls-tree`, BECAUSE IT ANSWERS ALL THREE QUESTIONS AT ONCE — is the
    # path there, is it a GITLINK, and what is its object id. `rev-parse
    # <commit>:<path>` was the first spelling and answered only the last: it
    # returns an oid for ANY tree entry, so a parent commit carrying a
    # regular file or a directory at `code` after a type-changing update
    # yielded that blob or tree id AS THE NESTED PIN, and the run then
    # reported an off-pin checkout instead of saying no gitlink is recorded
    # (Copilot, PR #1115). The index-first path has always required mode
    # `160000`; this one now does too, which is `verify-openxdox-pin.py`'s
    # rule as well. ABSENT AND UNREADABLE ALSO STAY APART, since `rev-parse
    # --quiet` conflated them: a tree read that FAILED is an incomplete
    # object store, not a missing submodule declaration.
    """
    listed = _git(parent, "ls-tree", "--full-tree", revision, "--", path)
    if listed is None or listed.returncode != 0:
        raise EquivalenceRefusal(
            "equivalence-object-store-incomplete",
            f"{parent} could not be asked what {revision} records for "
            f"{path}: the tree read FAILED or did not answer within "
            f"{_GIT_TIMEOUT}s. That is an OBJECT STORE that cannot answer "
            "about a revision this run has already accepted, not a missing "
            "submodule declaration — fetch its objects deliberately "
            f"(`git -C {parent} fetch origin {revision}`) and re-run")
    row = listed.stdout.strip()
    if not row:
        return None, None
    fields = row.split(None, 3)
    if len(fields) < 3 or fields[0] != "160000":
        return None, (fields[1] if len(fields) > 1 else "something")
    return fields[2], None


def _gitlink_index_first(parent: Path, path: str) -> tuple[str | None, str]:
    """The gitlink this repository RECORDS for `path`, index first."""
    # HEAD IS READ THE SAME WAY THE NESTED PATH IS (Copilot, PR #1115). It
    # was `rev-parse HEAD:<path>`, which answers for ANY tree entry, so when
    # the index read failed and this fell back to HEAD a type-changed file or
    # directory at a pin path was returned AS A RECORDED GITLINK — the very
    # defect just closed one function away, left standing in its sibling.
    head_oid, _kind = _gitlink_in_tree(parent, "HEAD", path)
    listed = _git(parent, "ls-files", "-s", "--", path)
    if listed is None or listed.returncode != 0:
        return head_oid, ("HEAD" if head_oid else _NO_RECORD_SOURCE)
    index_oid, conflicted = _staged_gitlink(listed.stdout)
    if index_oid is None and conflicted:
        raise EquivalenceRefusal(
            "equivalence-reach-unavailable",
            f"{parent} has {path} CONFLICTED in its index "
            f"({', '.join(conflicted)}) and carries no stage-0 entry for it, "
            "so this repository records no pin for that leg right now. "
            f"Resolve the merge in {parent} (`git status` names the paths) "
            "and re-run: a runner that read one of the conflict stages would "
            "report a pin no commit has declared")
    if index_oid != head_oid:
        return index_oid, ("the index" if index_oid else _NO_RECORD_SOURCE)
    return head_oid, ("HEAD" if head_oid else _NO_RECORD_SOURCE)


def _staged_gitlink(listing: str) -> tuple[str | None, list[str]]:
    """(the stage-0 gitlink, the conflict stages) out of `ls-files -s`.

    STAGE 0 OR NOTHING (Copilot, PR #1105 round 3, accepted without argument
    and owed since). `git ls-files -s` lists stages 1, 2 and 3 for a path in
    an unresolved merge, so taking the FIRST `160000` row would read the
    MERGE BASE's gitlink — or THEIRS — as the pin this repository records,
    compare the checkout against a commit nobody has declared, and refuse or
    pass on it. There is no recorded pin during a conflict; that is a state
    to name, not to guess through.
    """
    # EVERY NONZERO STAGE IS A CONFLICT, WHATEVER ITS MODE (Copilot, PR
    # #1115). Filtering to `160000` FIRST meant a merge between a gitlink and
    # a regular file — stages 1/2/3 with mixed modes — left `conflicted`
    # empty, so an unresolved conflict was reported as "no record" and could
    # fall back to HEAD. The stages are collected first and the mode is
    # required only of the stage-0 row, which is the one that would be used.
    stage_zero: str | None = None
    conflicted: list[str] = []
    for line in listing.splitlines():
        fields = line.split(None, 3)
        if len(fields) < 3:
            continue
        mode, oid, stage = fields[0], fields[1], fields[2]
        if stage != "0":
            conflicted.append(f"stage {stage} {mode} {oid[:12]}")
        elif mode == "160000":
            stage_zero = oid
    return stage_zero, conflicted


def recorded_gitlink(parent: Path, path: str,
                     outer: str | None = None) -> tuple[str | None, str]:
    """(oid, source) for the gitlink `parent` RECORDS for `path`.

    THE INDEX WINS WHEN IT DISAGREES WITH HEAD, which is
    `scripts/verify-openxdox-pin.py::_recorded_gitlink`'s own ruling and is
    taken here for its reason: a one-commit re-pin must be checkable BEFORE it
    is committed, and a HEAD-first read answers for the commit being replaced.
    Only a FAILED index read — an environment problem, not a staged one —
    falls back to HEAD without comparing.

    WITH `outer`, NEITHER WINS: the gitlink is read out of THAT COMMIT'S TREE
    (Copilot, PR #1105 round 10). The index-first rule is right for the pin
    THIS repository declares and wrong one level down, where the question is
    not "what is staged in the nested checkout" but "what does the commit the
    superproject records actually contain". A `code` gitlink staged inside
    `openDox` is in no commit openxFactory has declared, yet the index-first
    read would take it as the recorded pin and pass a leg the superproject
    never pinned — while `openDox`'s own HEAD still matched, so the level
    above stayed green. Reading `<outer>:<path>` closes that: the chain is
    resolved from the exact commit being claimed, at every level.
    """
    if outer is not None:
        return _gitlink_at_commit(parent, outer, path)
    return _gitlink_index_first(parent, path)


#: The two legs whose WORKING TREES this runner actually imports from.
#: `carved_reach.module()` resolves `openxdox.generator` off `openXdox/code/
#: src` on disk — not out of git — so these two are the ones whose cleanliness
#: is load-bearing. The two assembly roots are deliberately NOT here: their
#: only content that matters is the gitlink, and a staged or unstaged gitlink
#: move is already what `recorded_gitlink()` and the comparison below read.
#: MEASURED, NOT ASSUMED, AND NARROWER THAN THE PIN SET (Copilot, PR #1115).
#: An earlier commit in this act added the two `spec` mounts here beside the
#: pin set, and that was over-reach: `carved_reach.LEGS` installs exactly two
#: roots — `openDox/code/src` and `openXdox/code/src` — and `module()`
#: refuses a row that is not a `.py` at a code leg, so NOTHING can be
#: imported out of a spec mount through this reach. Sweeping a tree this run
#: cannot import from can only refuse a run for a state that cannot change
#: its result, which is the false-refusal defect this same act fixed for the
#: flag scan. The spec mounts stay in LEG_GITLINKS, because they ARE pins the
#: superproject records and verifying them is honest; they leave this tuple,
#: which is about what renders.
IMPORTED_LEGS: tuple[str, ...] = ("openDox/code", "openXdox/code")


#: The ONE ignored class the sweep passes over: CPython's compiled bytecode,
#: which this runner CREATES by importing the legs, so counting it would make
#: every run after the first refuse. Measured at the two code legs: 45 and 21
#: ignored files under `src`, all of them this.
#:
#: EXACTLY `__pycache__/<name>.pyc`, AND THE ALTERNATION THAT WAS HERE FIRST
#: WAS A HOLE (Copilot, PR #1115; SonarCloud `python:S5850` on the same line,
#: which is what an unparenthesised top-level `|` usually means). `\.pyc$`
#: alone allowlisted a `.pyc` ANYWHERE under the import surface, and a
#: sourceless `src/foo.pyc` sitting where `foo.py` would sit is a perfectly
#: ordinary import candidate — so the allowlist for the one artifact this
#: runner creates would have admitted a module it did not.
_GENERATED_BYTECODE = re.compile(r"(?:^|/)__pycache__/[^/]+\.pyc$")


def worktree_dirt(leg: Path) -> list[str] | None:
    """The cleanliness sweep for one leg: the entries, or `None` when the
    question could not be ASKED.

    `None` is not "clean". A read that failed or timed out learned nothing,
    and `carved_reach`'s rule holds one layer up as it does everywhere else
    in this file: a query that went unanswered must never stand in for the
    tree's own answer.

    THREE READS, NOT ONE `status` (Copilot, PR #1105 round 6, registered in
    the form that works). `--ignored` was the proposed remedy and it is
    unusable here: measured, it reports 3 and 4 `__pycache__` entries in the
    two code legs — ignored by each leg's own `.gitignore` and written by
    THIS RUNNER'S own imports — so a gate using it refuses on every run after
    the first. What is asked instead is exactly what matters:

    * `git diff --name-only HEAD -- src` — tracked edits, staged or not,
      under the import surface (the registered `--quiet` spelling is the same
      query; the names are taken because the refusal prints them). A leg
      with no `src` is diffed whole: there is no narrower surface to scope
      to, and scoping to a path that is not there would measure nothing.
    * `git ls-files --others --exclude-standard` — untracked files that are
      NOT ignored, which is the half `--ignored` drowned.
    * `git ls-files -v`, for the flags — a lowercase tag is
      `assume-unchanged` and `S` is `skip-worktree`. Both make git report a
      modified file as clean, so a leg carrying either can be edited with
      every other read above still answering "clean". A sweep that cannot
      see the state it is asserting is not a sweep.
    """
    scope = ["--", "src"] if (leg / "src").is_dir() else []
    rows: list[str] = []
    if scope:
        # AND THE IGNORED FILES UNDER THE IMPORT SURFACE, MINUS THE ONE CLASS
        # THIS RUNNER MAKES ITSELF (Copilot, PR #1115). `--exclude-standard`
        # drops EVERY ignored path, and an ignored `.py` under `src` is still
        # perfectly importable — it can shadow a module or be imported
        # outright — so excluding the whole class let a leg render bytes that
        # are in no commit while the verdict named one. The allowlist is
        # exactly CPython's compiled bytecode, which this runner's own
        # imports create: measured, the two code legs carry 45 and 21 ignored
        # files under `src` and EVERY ONE of them is a `__pycache__` `.pyc`.
        # Scoped to the import surface, because that is where an ignored file
        # can change what renders; a leg with no `src` has no such surface.
        ignored = _names(leg, "!! ", "ls-files", "--others", "--ignored",
                         "--exclude-standard", *scope)
        if ignored is None:
            return None
        rows += [row for row in ignored
                 if not _GENERATED_BYTECODE.search(row[3:])]
    for prefix, arguments in ((" M ", ("diff", "--name-only", "HEAD",
                                       *scope)),
                              ("?? ", ("ls-files", "--others",
                                       "--exclude-standard"))):
        named = _names(leg, prefix, *arguments)
        if named is None:
            return None
        rows += named
    # THE SAME SCOPE AS THE OTHER TWO READS (Copilot, PR #1115, suppressed).
    # The tracked diff and the ignored scan look at the import surface; a
    # flag scan over the WHOLE leg would refuse for an `assume-unchanged` bit
    # on a file that cannot reach `carved_reach`'s imports at all — a false
    # refusal in a required gate, which is a worse failure than the one it
    # would be guarding against.
    hidden = _flagged(leg, *scope)
    if hidden is None:
        return None
    return rows + hidden


def _names(leg: Path, prefix: str, *arguments: str) -> list[str] | None:
    """One name-per-line git read, each name given `prefix`, or `None` when
    the question could not be ASKED."""
    done = _git(leg, *arguments)
    if done is None or done.returncode != 0:
        return None
    return [f"{prefix}{name}" for name in done.stdout.splitlines()
            if name.strip()]


def _flagged(leg: Path, *scope: str) -> list[str] | None:
    """The `assume-unchanged` / `skip-worktree` entries, which `ls-files -v`
    marks with a lowercase tag and an `S` — the state that makes git report
    an EDITED file as clean, and so the state no other read here can see."""
    done = _git(leg, "ls-files", "-v", *scope)
    if done is None or done.returncode != 0:
        return None
    return [f"{line[0]}! {line[2:]}" for line in done.stdout.splitlines()
            if len(line) >= 3 and line[1] == " "
            and (line[0].islower() or line[0] == "S")]


def _dirt_kind(row: str) -> str:
    """Which of the four kinds a sweep row is, since each has its own remedy
    and two of them are spelled with a `!`."""
    if row.startswith("??"):
        return "untracked"
    if row.startswith("!!"):
        return "ignored"
    if row[1:2] == "!":
        return "hidden"
    return "tracked"


def _clean_advice(dirt: list[str], leg: Path) -> str:
    """The remediation that actually restores THIS tree.

    `git checkout -- .` restores TRACKED paths only, and a plain `git stash`
    leaves untracked files behind — so for a `??` entry the first spelling of
    this message sent an operator to a command that could not make the next
    run clean (Copilot on #1105 @9ed3def3, suppressed). `worktree_dirt()`
    reports both kinds, so the advice branches on what is actually there.
    """
    kinds = {_dirt_kind(row) for row in dirt}
    untracked = "untracked" in kinds
    hidden = "hidden" in kinds
    ignored = "ignored" in kinds
    tracked = "tracked" in kinds
    remedies = []
    if tracked:
        remedies.append(f"commit the edits or `git -C {leg} checkout -- .`")
    if untracked:
        remedies.append(
            f"`git -C {leg} stash -u` or `git -C {leg} clean -fd` the "
            "UNTRACKED entries (`checkout -- .` will not remove them, and a "
            "plain stash would leave them)")
    if hidden:
        # A THIRD KIND, AND THE ONLY ONE THAT SURVIVES THE OTHER TWO: an
        # `assume-unchanged` or `skip-worktree` bit makes git report an
        # edited file as clean, so `checkout -- .` restores nothing and the
        # next run reads the same tree as clean again. CLEARING THE FLAG IS
        # HALF THE REMEDY (Copilot, PR #1115): the edit it was hiding then
        # shows up as an ordinary modification and the promised re-run
        # refuses a second time, so the restore is named here with it.
        remedies.append(
            f"clear the hidden flags — `git -C {leg} update-index "
            "--no-assume-unchanged --no-skip-worktree <path>` — for the "
            "`h!`/`S!` entries above, AND THEN commit, stash or "
            f"`git -C {leg} checkout --` those same paths: while the flags "
            "are set git reports those files as clean however they are "
            "edited, and clearing a flag reveals the edit rather than "
            "removing it")
    if ignored:
        remedies.append(
            f"remove the IGNORED entries under the import surface (`git -C "
            f"{leg} clean -fdX -- src`, or delete them): git ignores them "
            "and Python imports them anyway, which is the whole reason they "
            "are reported")
    return "Then re-run: " + "; ".join(remedies)


def unmaterialized_legs() -> list[str]:
    """Which pinned mounts are not THERE, read without importing anything.

    RUN BEFORE `post_stack()`, and that is the whole point (Copilot, PR #1105
    round 6). Composing the stack is how this file learns almost everything,
    but it is not free and it is not read-only: `import carved_reach` installs
    a meta-path finder, `install()` mutates the import system for the rest of
    the process, and importing out of a leg writes `__pycache__` INTO the leg
    whose cleanliness the next check is about to assert. Doing all of that to
    discover that a submodule directory is empty is work with side effects
    performed to reach a worse message — `carved_reach`'s own refusal names a
    module, and what an operator with an uninitialized checkout needs named is
    the checkout.

    A `git` read would answer this too and is deliberately not used: the
    question is whether the FILES are on disk for the import machinery, which
    is a question about the filesystem, and a leg can be perfectly recorded in
    every index while its directory is empty. That is exactly the state a
    fresh clone without `--recurse-submodules` is in.
    """
    absent: list[str] = []
    for parent_rel, path in LEG_GITLINKS:
        leg = (ROOT / parent_rel / path)
        if not leg.is_dir():
            absent.append(f"{leg} — no such directory")
        elif not any(child.name != ".git" for child in leg.iterdir()):
            # `.git` ITSELF DOES NOT COUNT (Copilot, PR #1115). A mount
            # holding only submodule metadata — `submodule update
            # --no-checkout`, or an update interrupted between clone and
            # checkout — has files in it and no working tree, which is the
            # state this probe exists to name.
            absent.append(f"{leg} — no working tree: the directory holds "
                          "nothing but submodule metadata, so the gitlink is "
                          "recorded and nothing was ever checked out")
        elif not (leg / ".git").exists():
            absent.append(f"{leg} — no `.git`: a copied source tree rather "
                          "than a checkout, so no pin can be verified for it")
    return absent


def superproject_state() -> dict[str, Any]:
    """THE ROOT CHECKOUT'S OWN revision and dirt, for the EVIDENCE.

    Never a refusal, and the asymmetry with the legs is the point (Copilot,
    PR #1105 round 4). The legs are pinned, so a dirty leg makes the verdict's
    own sentence false and must refuse. The root is not pinned by anything
    here — and it is the tree this runner is EDITED in, so refusing on its
    dirt would make the gate unusable by the only people who change it.

    But it is not irrelevant either, which is why it is carried: the post side
    is composed out of ROOT's `scripts/carved_reach.py`, `scripts/
    opendox_host.py` and `contracts/domain-profiles/`, none of them pinned by
    the gitlinks above. A reader holding two runs with different digests can
    tell from this line whether the composition was the same.
    """
    head = _git(ROOT, "rev-parse", "--verify", "--quiet", "--end-of-options",
                "HEAD")
    revision = (head.stdout.strip()
                if head is not None and head.returncode == 0 else "")
    done = _git(ROOT, "status", "--porcelain", "--untracked-files=normal")
    # AND THE SAME BLIND SPOT THIS ACT FIXES FOR THE LEGS (Copilot, PR #1115,
    # suppressed). A plain `status` cannot see an edit hidden by an
    # `assume-unchanged` or `skip-worktree` bit, so the evidence line could
    # read `working tree clean` while `carved_reach.py`, `opendox_host.py` or
    # the profile — the UNPINNED half this line exists to carry — had been
    # edited. The root is still never refused on; it is reported truthfully
    # or reported as unknown.
    hidden = _flagged(ROOT)
    if done is None or done.returncode != 0 or hidden is None:
        return {"root_revision": revision or "unknown",
                "root_worktree": "unknown", "root_worktree_entries": None}
    rows = [line for line in done.stdout.splitlines() if line.strip()]
    return {"root_revision": revision or "unknown",
            "root_worktree": "dirty" if rows or hidden else "clean",
            "root_worktree_entries": len(rows) + len(hidden)}


def verify_pins() -> dict[str, str]:
    """Every nested leg is CHECKED OUT AT THE COMMIT ITS PARENT RECORDS.

    WITHOUT THIS THE EVIDENCE LINE IS NOT TRUE BY CONSTRUCTION, and that is
    the whole reason it exists (Copilot, PR #1105). § 8.2's line says the post
    side rendered "at the pinned openXdox-code <sha>"; `carved_reach` imports
    out of the nested WORKTREE, so a leg left detached at some other commit —
    by a bisect, a half-finished bump, a copied tree — renders perfectly well
    and the line then names a pin that did not render. Reporting the
    checked-out sha instead of refusing was this file's first answer and it is
    the wrong one: it makes a true statement about a run nobody asked for.

    Two levels per leg, as `verify-openxdox-pin.py` checks them: the recorded
    gitlink and the checked-out revision are separate required comparisons,
    because only one of them catches each case.

    A gitlink that cannot be READ refuses too. `carved_reach`'s own rule — a
    query that went unanswered is not an answer — applies exactly: nothing was
    learned about the pin, so nothing may be claimed for it.
    """
    heads: dict[str, str] = {}
    declared: dict[str, str] = {}
    for parent_rel, path in LEG_GITLINKS:
        parent = (ROOT / parent_rel).resolve()
        leg = (parent / path).resolve()
        # THE CHAIN IS RESOLVED FROM THE EXACT OUTER COMMIT, level by level
        # (Copilot, PR #1105 round 10). The superproject's own gitlinks are
        # read index-first, because a re-pin must be checkable before it is
        # committed; every level BELOW is read out of the commit the level
        # above just verified, because nothing staged inside a nested
        # checkout is part of any pin this repository has declared.
        outer = None if parent_rel == "." else declared[parent_rel]
        recorded, source = recorded_gitlink(parent, path, outer)
        if recorded is None:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"{parent} records no gitlink for {path} in {source}, so "
                "there is nothing to compare the checkout against. This "
                "runner reports which pinned commit rendered; a pin it "
                "cannot read is a claim it cannot make")
        head = _git(leg, "rev-parse", "--verify", "--quiet",
                    "--end-of-options", "HEAD")
        checked_out = (head.stdout.strip()
                       if head is not None and head.returncode == 0 else None)
        if checked_out is None:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"`git -C {leg} rev-parse HEAD` FAILED or did not answer "
                f"within {_GIT_TIMEOUT}s, so this run never learned which "
                f"revision {leg} is checked out at and cannot compare it "
                f"with the {recorded} its parent {parent} records (read from "
                f"{source}). That is an UNREADABLE checkout — a leg with no "
                "usable git metadata, a copied source tree, a store whose "
                "objects are not there — and it is a different condition from "
                "a checkout that is simply off its pin, which this runner "
                f"reports separately. Run `{INIT_COMMAND_HINT}`")
        if checked_out != recorded:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"{leg} is checked out at {checked_out}, but {parent} records "
                f"{recorded} for {path} (read from {source}). The post side "
                "is reached through the PINS, and a leg moved out from under "
                "them renders something this run has no name for — run "
                f"`{INIT_COMMAND_HINT}` to put the checkout back on its pin")
        key = f"{parent_rel}/{path}".lstrip("./")
        heads[key] = checked_out
        declared[key] = recorded
    # AND THE TREE ON DISK IS THE COMMIT, NOT MERELY AT IT (Copilot, PR #1105
    # round 2). `carved_reach.module()` imports off the nested WORKING TREE,
    # so an uncommitted edit under a leg's `src/` renders bytes that are not
    # the pinned commit's while every check above still passes and the verdict
    # still names that commit — the same false evidence line the gitlink
    # comparison exists to prevent, arriving one layer lower.
    # `verify-openxdox-pin.py` records this exact gap in terms; here it is
    # closed rather than recorded, because this runner's whole output is a
    # claim about which commit rendered.
    for leg_path in IMPORTED_LEGS:
        leg = (ROOT / leg_path).resolve()
        dirt = worktree_dirt(leg)
        if dirt is None:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"the cleanliness sweep of {leg} — its tracked diff, its "
                "ignored and untracked files, and its `ls-files -v` flags — "
                f"FAILED or did not answer within {_GIT_TIMEOUT}s per read, "
                f"so whether the tree this run "
                f"imports from IS the commit {heads[leg_path]} it is checked "
                "out at went unmeasured. A pin this runner could not verify "
                "is a pin it must not report")
        if dirt:
            listed = "\n".join(f"    {entry}" for entry in dirt[:20])
            more = (f"\n    … {len(dirt) - 20} more" if len(dirt) > 20 else "")
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"{leg} is checked out at {heads[leg_path]} but its working "
                f"tree is DIRTY, and this runner imports from the tree:\n"
                f"{listed}{more}\n"
                "Rendering it would produce bytes that are not that "
                "commit's while the verdict named that commit. "
                + _clean_advice(dirt, leg))
    return heads



def _refused(exc: EquivalenceRefusal, args: argparse.Namespace,
             where: str) -> int:
    """The ONE refusal exit: `--json` object or the rendered human message."""
    if args.json:
        print(json.dumps({"result": "refused", "code": exc.code,
                          "detail": exc.detail, "pre_ref": args.pre_ref,
                          **exc.payload}))
    else:
        print(exc.render(where), file=sys.stderr)
    return 2


def _print_ok(summary: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary))
        return
    total = len(summary["states"])
    print(f"OK — {total} of {total} corpus state(s) equivalent: the "
          f"pre-split tree {summary['pre_ref']} "
          f"({summary['pre_commit'][:12]}) and the post-split stack "
          f"({summary['post_label']}, through scripts/carved_reach.py) render "
          f"byte-identical snapshots at the pinned source_revision "
          f"{summary['source_revision'][:8]}…")
    for state in summary["states"]:
        print(f"  {state['corpus']}  {state['pre_bytes']} bytes  "
              f"sha256 {state['pre_sha256']}")
    # THE COMPOSITION'S OWN TREE, carried because it is NOT one of the pins
    # above: `carved_reach.py`, `opendox_host.py` and the § 4.4 profile are
    # read out of this checkout, and two runs of this runner can differ by
    # them alone while every pinned leg matches (Copilot, PR #1105 round 4).
    entries = summary.get("root_worktree_entries")
    counted = ""
    if entries:
        plural = "entry" if entries == 1 else "entries"
        counted = f" ({entries} uncommitted {plural})"
    print(f"  composed in {ROOT} at "
          f"{str(summary.get('root_revision', 'unknown'))[:12]}, working "
          f"tree {summary.get('root_worktree', 'unknown')}{counted}"
          " — the pinned legs above are verified clean; this line is the "
          "UNPINNED half of the composition")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify-snapshot-equivalence.py",
        description=("Render one corpus through the pre-split tree and the "
                     "post-split stack and compare the snapshots byte for "
                     "byte — FLOOR PART 4 of split-opendox § D6 (RULED "
                     "OQ-1)."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--pre-ref", metavar="REF", default=DEFAULT_PRE_REF,
        help=(f"the pre-split revision (default: {DEFAULT_PRE_REF}, FLOOR "
              "PART 1's carve_commit). Any PRE-SHED ref is accepted — "
              "contract-v3.7 re-proves the same digest"))
    parser.add_argument(
        "--corpus", metavar="DIR", action="append", default=None,
        help=(f"a corpus both sides render (default: {CORPUS_RELPATH}). "
              "REPEATABLE: each one is a corpus state, and the verdict counts "
              "them"))
    parser.add_argument(
        "--source-revision", metavar="SHA", default=PINNED_SOURCE_REVISION,
        help=("the revision both sides stamp the snapshot with (default: the "
              "determinism suite's pin). Unpinned, the two sides diverge on "
              "the anchor alone and the comparison means nothing"))
    parser.add_argument(
        "--no-register-profile", action="store_true",
        help=("do not call opendox_host.register_openxfactory() — for a host "
              "that has composed and registered the § 4.4 profile itself. "
              "With no profile registered anywhere the engine refuses and "
              "this runner reports equivalence-profile-unregistered"))
    parser.add_argument(
        "--json", action="store_true",
        help="print one JSON object on stdout instead of the human lines")
    args = parser.parse_args(argv)

    where = args.pre_ref
    try:
        if OBJECT_ID.fullmatch(args.source_revision) is None:
            raise EquivalenceRefusal(
                "equivalence-unreadable",
                f"--source-revision {args.source_revision!r} is not an object "
                "id. Both sides stamp the snapshot with this value through an "
                "INJECTED git that resolves nothing, so a name — `HEAD`, a "
                "branch, a typo — would render, compare equal and exit 0 over "
                "a snapshot anchored to something that is not a commit. Give "
                "40 or 64 hex characters (the default is the determinism "
                "suite's own pin)")
        corpora = [Path(c).resolve() for c in
                   (args.corpus or [ROOT / CORPUS_RELPATH])]
        for corpus in corpora:
            if not corpus.is_dir():
                raise EquivalenceRefusal(
                    "equivalence-unreadable",
                    f"--corpus {corpus} is not a directory. A run over a "
                    "corpus that is not there would render two empty "
                    "snapshots and report them equal, and silence must not "
                    "read as a pass")
        # THE POST SIDE COMES FIRST, AND THE ORDER IS DELIBERATE. It is the
        # claim's subject and the cheapest thing to prove absent: an operator
        # whose legs are not materialized, or whose process has no § 4.4
        # profile, should be told THAT rather than told about a tag, and
        # extracting a 5.7 MB archive before discovering that the stack
        # cannot be composed at all is work done to reach a worse message.
        # THE FILESYSTEM PROBE COMES FIRST OF ALL, and this comment used to
        # say `post_stack()` did (Copilot, PR #1115 — it was the opposite of
        # the implemented, tested order). Composing imports the legs, which
        # installs a meta-path finder and writes `__pycache__` INTO the tree
        # whose cleanliness the next check asserts; discovering an empty
        # submodule directory that way costs those side effects and answers
        # in terms of a module name rather than of the checkout. NOTHING IS
        # CLAIMED BETWEEN ANY OF THEM: the modules are imported here and not
        # rendered until after the pins are verified, so a leg off its pin
        # refuses before any digest exists to report.
        absent = unmaterialized_legs()
        if absent:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                "the pinned legs are not materialized in this checkout:\n"
                + "\n".join(f"    {row}" for row in absent)
                + f"\nRun `{INIT_COMMAND_HINT}`. This is read off the "
                "filesystem BEFORE the stack is composed, so that a checkout "
                "with no legs is told about its legs rather than about a "
                "module it has never heard of")
        stack = post_stack(register_profile=not args.no_register_profile)
        pins = verify_pins()
        pre_commit = pre_ref_commit(args.pre_ref, ROOT)
        where = f"{args.pre_ref} ({pre_commit[:12]})"
        summary: dict[str, Any] = {
            "result": "ok",
            "pre_ref": args.pre_ref,
            "pre_commit": pre_commit,
            "openxdox_code": pins["openXdox/code"],
            "opendox_code": pins["openDox/code"],
            "pins": pins,
            **post_side_identity(stack, pins),
            "source_revision": args.source_revision,
            "repository": REPOSITORY_NAME,
            **superproject_state(),
            "states": [],
        }
        with tempfile.TemporaryDirectory(
                prefix="snapshot-equivalence-") as tmp:
            scratch = Path(tmp)
            tree = extract_pre_tree(pre_commit, ROOT, scratch / "pre",
                                    args.pre_ref)
            for corpus in corpora:
                pre = render_pre(tree, corpus, scratch, args.pre_ref,
                                 args.source_revision)
                post = render_post(stack, corpus, args.source_revision)
                summary["states"].append(
                    compare(pre, post, corpus, args.pre_ref,
                            summary["post_label"]))
    except EquivalenceRefusal as exc:
        return _refused(exc, args, where)
    # A `_RenderTimeout` can still land in the sliver between the guarded
    # render and `disarm()`, where `render_post()` no longer maps it — and it
    # is a `BaseException`, so the guard below, which is `Exception` ON
    # PURPOSE, would not hold the exit contract for it. It is this file's own
    # control-flow signal and not the operator's, so it refuses in this
    # file's vocabulary rather than leaving a traceback and EXIT 1.
    except _RenderTimeout:
        return _refused(
            EquivalenceRefusal(
                "equivalence-post-stack-unrenderable",
                "the pinned post-split stack did not finish rendering "
                f"within {_CHILD_TIMEOUT}s"),
            args, where)
    # THE EXIT CONTRACT, HELD BY CODE AND NOT BY INSPECTION. Everything above
    # refuses in this file's own vocabulary; anything that does not — a leg
    # whose module raises on import, an OSError the checks did not name, a bug
    # here — would otherwise leave `main()` as a traceback and EXIT 1, which
    # the module docstring says does not exist. It is `Exception` and not
    # `BaseException`: a `KeyboardInterrupt` or a `SystemExit` is the
    # operator's act and must not be re-labelled a finding.
    except Exception as exc:  # noqa: BLE001
        return _refused(
            EquivalenceRefusal("equivalence-unreadable",
                               f"{type(exc).__name__}: {exc}"),
            args, where)
    _print_ok(summary, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
