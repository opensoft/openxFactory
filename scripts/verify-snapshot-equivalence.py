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
import subprocess
import sys
import tempfile
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
    "equivalence-unreadable",
)

REMEDIATION = (
    "Remediation: FOUR of these refusals are about THE RUN and are fixed at "
    "the run — a missing tag is fetched (`git fetch --tags`), an "
    "unmaterialized leg is initialized (`git submodule update --init "
    "--recursive openDox openXdox`), a post-shed `--pre-ref` is replaced by a "
    "pre-shed one, an unregistered profile is registered. THE FIFTH, "
    "`equivalence-digests-differ`, is a finding about THE PROJECTION and the "
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
import sys
from pathlib import Path

scripts_dir, corpus, out_path, revision, date, repository = sys.argv[1:7]
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


def _git_environment() -> dict[str, str]:
    environment = {
        name: value for name, value in os.environ.items()
        if name not in _SCRUBBED_GIT_ENVIRONMENT
        and _INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None}
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


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
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"`git archive {pre_commit}` ({pre_ref}) carries none of "
            f"{', '.join(ARCHIVE_PATHS)}"
            f": {archive.stderr.decode('utf-8', 'replace').strip()}. That ref "
            "is POST-SHED — the § 5.2 shed removed the renderer from this "
            "repository — so it is not a pre-split tree and must not be read "
            "as one")
    extract = subprocess.run(["tar", "-x", "-C", str(into)],
                             input=archive.stdout, capture_output=True,
                             check=False, timeout=_GIT_TIMEOUT)
    if extract.returncode != 0:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"extracting the {pre_ref} ({pre_commit[:12]}) archive into "
            f"{into} failed: "
            f"{extract.stderr.decode('utf-8', 'replace').strip()}")
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
    out = scratch / "pre-snapshot.json"
    done = subprocess.run(
        [sys.executable, "-I", "-c", _PRE_RENDER_PROGRAM,
         str(tree / "scripts"), str(corpus), str(out), source_revision,
         PINNED_COMMIT_DATE, REPOSITORY_NAME],
        capture_output=True, text=True, check=False)
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


def post_side_identity(stack, pins: dict[str, str]) -> dict[str, str]:
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
    try:
        snap = generator.generate_snapshot(
            corpus, REPOSITORY_NAME, source_revision=source_revision,
            git=FakeGit(head=source_revision))
    except Exception as exc:  # noqa: BLE001 - narrowed by name below
        if type(exc).__name__ == "DomainProfileNotRegistered":
            raise EquivalenceRefusal(
                "equivalence-profile-unregistered",
                f"{type(exc).__name__}: {exc}") from exc
        raise
    return snapshot.canonical_bytes(snap)


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


def compare(pre: bytes, post: bytes, corpus: Path, pre_ref: str,
            post_label: str) -> dict[str, Any]:
    """One corpus state's verdict, or the refusal that NAMES the field.

    A refusal that printed two hex strings would tell an operator that
    something moved and nothing about what. The unified diff is what makes a
    red run actionable, and it is of the canonical JSON rather than of the
    bytes because the canonical form is one line.
    """
    pre_digest = hashlib.sha256(pre).hexdigest()
    post_digest = hashlib.sha256(post).hexdigest()
    state = {"corpus": str(corpus), "pre_bytes": len(pre),
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
        diff = [f"(the two sides differ in length alone: {len(pre)} vs "
                f"{len(post)} bytes, with no line that differs)"]
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
LEG_GITLINKS: tuple[tuple[str, str], ...] = (
    (".", "openDox"), ("openDox", "code"),
    (".", "openXdox"), ("openXdox", "code"),
)


def recorded_gitlink(parent: Path, path: str) -> tuple[str | None, str]:
    """(oid, source) for the gitlink `parent` RECORDS for `path`.

    THE INDEX WINS WHEN IT DISAGREES WITH HEAD, which is
    `scripts/verify-openxdox-pin.py::_recorded_gitlink`'s own ruling and is
    taken here for its reason: a one-commit re-pin must be checkable BEFORE it
    is committed, and a HEAD-first read answers for the commit being replaced.
    Only a FAILED index read — an environment problem, not a staged one —
    falls back to HEAD without comparing.
    """
    head = _git(parent, "rev-parse", "--verify", "--quiet",
                "--end-of-options", f"HEAD:{path}")
    head_oid = (head.stdout.strip()
                if head is not None and head.returncode == 0 else None)
    listed = _git(parent, "ls-files", "-s", "--", path)
    if listed is None or listed.returncode != 0:
        return head_oid, "HEAD"
    index_oid = None
    for line in listed.stdout.splitlines():
        fields = line.split(None, 3)
        if len(fields) >= 3 and fields[0] == "160000":
            index_oid = fields[1]
            break
    if index_oid != head_oid:
        return index_oid, "the index"
    return head_oid, "HEAD"


#: The two legs whose WORKING TREES this runner actually imports from.
#: `carved_reach.module()` resolves `openxdox.generator` off `openXdox/code/
#: src` on disk — not out of git — so these two are the ones whose cleanliness
#: is load-bearing. The two assembly roots are deliberately NOT here: their
#: only content that matters is the gitlink, and a staged or unstaged gitlink
#: move is already what `recorded_gitlink()` and the comparison below read.
IMPORTED_LEGS: tuple[str, ...] = ("openDox/code", "openXdox/code")


def worktree_dirt(leg: Path) -> list[str] | None:
    """`git status --porcelain` for one leg: the entries, or `None` when the
    question could not be ASKED.

    `None` is not "clean". A status read that failed or timed out learned
    nothing, and `carved_reach`'s rule holds one layer up as it does
    everywhere else in this file: a query that went unanswered must never
    stand in for the tree's own answer.
    """
    done = _git(leg, "status", "--porcelain", "--untracked-files=normal")
    if done is None or done.returncode != 0:
        return None
    return [line for line in done.stdout.splitlines() if line.strip()]


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
    for parent_rel, path in LEG_GITLINKS:
        parent = (ROOT / parent_rel).resolve()
        leg = (parent / path).resolve()
        recorded, source = recorded_gitlink(parent, path)
        if recorded is None:
            raise EquivalenceRefusal(
                "equivalence-reach-unavailable",
                f"{parent} records no gitlink for {path} in HEAD or in the "
                "index, so there is nothing to compare the checkout against. "
                "This runner reports which pinned commit rendered; a pin it "
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
        heads[f"{parent_rel}/{path}".lstrip("./")] = checked_out
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
                f"`git -C {leg} status --porcelain` FAILED or did not answer "
                f"within {_GIT_TIMEOUT}s, so whether the tree this run "
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
                "Rendering it would produce bytes that are not that commit's "
                "while the verdict named that commit. Commit the edit, stash "
                f"it, or `git -C {leg} checkout -- .` and re-run")
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
        # THE POST SIDE IS COMPOSED FIRST, AND THE ORDER IS DELIBERATE. It is
        # the claim's subject and the cheapest thing to prove absent: an
        # operator whose legs are not materialized, or whose process has no
        # § 4.4 profile, should be told THAT rather than told about a tag, and
        # extracting a 5.7 MB archive before discovering that the stack cannot
        # be composed at all is work done to reach a worse message.
        # `post_stack()` first, so `carved_reach.require()`'s own refusal —
        # the one that names `git submodule update` — wins over the pin
        # comparison for a checkout with no legs at all. NOTHING IS CLAIMED
        # BETWEEN THE TWO: the modules are imported here and not rendered
        # until after the pins are verified, so a leg off its pin refuses
        # before any digest exists to report.
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
