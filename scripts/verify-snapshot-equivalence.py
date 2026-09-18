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
the archive does not carry would otherwise fall through to a `PYTHONPATH` or
user-site copy and silently complete a partial archive out of another tree.

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

#: The repository name the snapshot is stamped with. The determinism suite's,
#: so a digest measured here is the digest that suite measures.
REPOSITORY_NAME = "fixture-repo"

#: How many lines of the unified diff a `equivalence-digests-differ` prints
#: before it truncates. A refusal that is a wall of JSON is a refusal nobody
#: reads; the JSON payload carries the whole of both sides for a caller that
#: wants it.
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


def pre_ref_commit(pre_ref: str, repo: Path) -> str:
    """The commit `--pre-ref` names, or the refusal that names the fetch.

    Separated from the archive below so that "this checkout has never heard of
    that ref" and "that ref's tree carries no renderer" are DIFFERENT findings.
    They have different remedies and only one of them is an operator error
    about the run rather than about the tree.
    """
    done = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet",
         f"{pre_ref}^{{commit}}"],
        capture_output=True, text=True, check=False)
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


def extract_pre_tree(pre_ref: str, repo: Path, into: Path) -> Path:
    """`git archive` the pre-split renderer into a scratch tree.

    A `git worktree` would also work and is deliberately not used: it mutates
    the repository's administrative state, and openxFactory's own doc-health
    misreports from inside one (`release-inventory-drift` reports four extra
    errors in a worktree regardless of commit). An archive touches nothing.
    """
    into.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", pre_ref, "--",
         *ARCHIVE_PATHS],
        capture_output=True, check=False)
    if archive.returncode != 0:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"`git archive {pre_ref}` carries none of "
            f"{', '.join(ARCHIVE_PATHS)}"
            f": {archive.stderr.decode('utf-8', 'replace').strip()}. That ref "
            "is POST-SHED — the § 5.2 shed removed the renderer from this "
            "repository — so it is not a pre-split tree and must not be read "
            "as one")
    extract = subprocess.run(["tar", "-x", "-C", str(into)],
                             input=archive.stdout, capture_output=True,
                             check=False)
    if extract.returncode != 0:
        raise EquivalenceRefusal(
            "equivalence-pre-tree-unrenderable",
            f"extracting the {pre_ref} archive into {into} failed: "
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

    THE SEPARATE PROCESS is what carries the isolation; `-I` closes the door
    the `sys.path.insert` leaves open. The insert wins every name the archived
    tree HAS, but a name it LACKS — a submodule dropped from the archive, a
    helper a future pre-shed ref imports — falls through to whatever comes
    next, and a `PYTHONPATH` or user-site copy would then silently complete a
    partial archive out of another tree. Isolated, there is nothing after the
    insert but the standard library, so a missing piece fails loudly and
    arrives as `equivalence-pre-tree-unrenderable` rather than as a pass.
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
        import opendox_host
        try:
            opendox_host.register_openxfactory()
        except Exception as exc:  # noqa: BLE001 - re-raised as a named refusal
            raise EquivalenceRefusal(
                "equivalence-profile-unregistered",
                f"registering {opendox_host.PROFILE_PATH.name} raised "
                f"{type(exc).__name__}: {exc}") from exc
    return (carved_reach.module(GENERATOR_ROW),
            carved_reach.module(SNAPSHOT_ROW))


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
        if type(exc).__name__ in ("DomainProfileNotRegistered",
                                  "AlreadyRegistered"):
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


def compare(pre: bytes, post: bytes, corpus: Path,
            pre_ref: str) -> dict[str, Any]:
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
        fromfile=f"PRE  {pre_ref}", tofile="POST pinned openXdox-code",
        lineterm=""))
    shown = diff[:DIFF_LINE_CAP]
    if len(diff) > DIFF_LINE_CAP:
        shown.append(f"  … {len(diff) - DIFF_LINE_CAP} more diff line(s); "
                     "re-run with --json for both snapshots in full")
    state["diff"] = diff
    raise EquivalenceRefusal(
        "equivalence-digests-differ",
        f"over {corpus} the two sides rendered DIFFERENT snapshots.\n"
        f"  PRE  {pre_ref}: {len(pre)} bytes, sha256 {pre_digest}\n"
        f"  POST pinned openXdox-code: {len(post)} bytes, sha256 "
        f"{post_digest}\n" + "\n".join(shown),
        payload=state)


def leg_commit(leg: str) -> str | None:
    """The sha of a materialized leg, for the record the verdict leaves.

    The CHECKED-OUT commit and not the gitlink the superproject records: it is
    the one that actually rendered, and the two differ exactly when somebody
    has moved a leg under the run — which is a thing the evidence line should
    show rather than hide.
    """
    done = subprocess.run(
        ["git", "-C", str(ROOT / leg), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False)
    return done.stdout.strip() or None


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
          f"({summary['pre_commit'][:12]}) "
          f"and the post-split stack (openxdox.generator + openxdox.snapshot "
          f"at the pinned openXdox-code "
          f"{(summary['openxdox_code'] or 'uninitialized')[:12]}, through "
          f"scripts/carved_reach.py) render byte-identical snapshots at the "
          f"pinned source_revision {summary['source_revision'][:8]}…")
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
        stack = post_stack(register_profile=not args.no_register_profile)
        pre_commit = pre_ref_commit(args.pre_ref, ROOT)
        where = f"{args.pre_ref} ({pre_commit[:12]})"
        summary: dict[str, Any] = {
            "result": "ok",
            "pre_ref": args.pre_ref,
            "pre_commit": pre_commit,
            "openxdox_code": leg_commit("openXdox/code"),
            "opendox_code": leg_commit("openDox/code"),
            "source_revision": args.source_revision,
            "repository": REPOSITORY_NAME,
            "states": [],
        }
        with tempfile.TemporaryDirectory(
                prefix="snapshot-equivalence-") as tmp:
            scratch = Path(tmp)
            tree = extract_pre_tree(args.pre_ref, ROOT, scratch / "pre")
            for corpus in corpora:
                pre = render_pre(tree, corpus, scratch, args.pre_ref,
                                 args.source_revision)
                post = render_post(stack, corpus, args.source_revision)
                summary["states"].append(
                    compare(pre, post, corpus, args.pre_ref))
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
