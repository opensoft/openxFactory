"""CSC-C6's required-check home: the floor's completeness, asserted where it blocks.

WHY THIS MODULE EXISTS, IN THE SEAT'S OWN WORDS. CSC-C6 (BLOCKING, Gate-Rules
Council 2026-08-31) requires the coverage assertion
`set(tracked paths under prefix) ⊆ set(floor entries)` to run *"on a check
somebody is required to look at — **not** on the openxFactory advisory lane
alone, which blocks nobody (CSC-F14)"*, and to fail red *"on the commit that adds
a spec off the floor"*. LQ-A7 (BLOCKING) names the same assertion and homes it in
`merge-master-approval.yml`, *"which already produces `tree_paths.txt`, so the
assertion is a set difference over data on hand"*. **Brett Heap ruled BOTH,
LAYERED** (record §6.1): LQ-A7's set difference lands in the advisory lane, and
CSC-C6's required-check home was commissioned as the feasibility question CSC
itself named. That question was answered FEASIBLE on 2026-09-01, and this module
is the answer's load-bearing half.

`pytest-suite` is REQUIRED on `opensoft/openxFactory` by organization ruleset
`21538893`. A pull request cannot merge while it is red. That is the whole point:
CSC's objection was never that the assertion was hard to write, it was that an
assertion nobody must look at is not a guard.

HOW IT STAYS HERMETIC. The assertion reads two things: `git ls-files
openspec/specs` and a file on disk. `tests/hermeticity.py` makes `nlm`, `gh` and
`omp` unreachable; it blocks neither. The file on disk is
`contracts/review-lane-floor-snapshot.yaml`, a BYTE COPY of the floor document at
the commit `contracts/review-lane-pin.yaml` pins — the same shape
`contracts/openxwallet-pin.yaml` uses for a foreign artifact, and the same shape
`merge-master-approval.yml` uses when it crosses the boundary in the workflow
step and keeps the evaluation offline.

AND WHY A COPY IS NOT ENOUGH ON ITS OWN. A snapshot missing entries reds
conservatively; a snapshot carrying an entry the real floor lacks is a SILENT
FALSE GREEN — the CSC-F16 defect species, filed by CSC against its own condition.
So `pytest-suite.yml` also checks out the pinned core (`continue-on-error`) and
`TheFreshnessVerifier` below compares the two byte for byte. **That comparison is
the only skipping test in `tests/review_lane_pin/`, and its skip is the alarm
rather than a hole:** `pytest-suite.yml` reads the JUnit report and requires
THIS TESTCASE, BY NAME, to have run and passed, so a checkout that quietly
stopped working turns the REQUIRED check red with a named cause. Silent
degradation becomes visible. Everything else here either passes or fails,
following `test_review_lane_caller.py`'s rule for the same reason.

THE NAME IS THE SIGNAL, AND THE COUNT IS THE BACKSTOP — in that order, and the
order was corrected. The first cut relied on `EXPECT_SKIPPED` alone: the skip
makes 22, the pin says 21, red. Codex (P2, PR #569) found that an AGGREGATE
cannot see this: on a run where the checkout fails AND some other conditional
skip starts running, +1 and −1 cancel, the pin still reads 21, and the required
check is GREEN with this comparison gone — the CSC-F16 silent-false-green shape
inside the guard against CSC-F16. The named-testcase assertion cannot be
cancelled by anything happening elsewhere in the suite; the exact skip pin
stays, doing the job it was actually built for.

TWO TIERS, as in that module: the shipped bytes first, then negative controls one
mutation away, so a check that has quietly stopped checking is visible.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PIN = REPO_ROOT / "contracts/review-lane-pin.yaml"
SNAPSHOT = REPO_ROOT / "contracts/review-lane-floor-snapshot.yaml"
PYTEST_SUITE = REPO_ROOT / ".github/workflows/pytest-suite.yml"

PINNED_REPOSITORY = "opensoft/codexFactory"
FLOOR_REPOSITORY = "opensoft/openxFactory"

# The path the pinned core keeps the floor document at. Restated as a literal
# rather than read from the pin, for the reason `test_review_lane_caller.py`
# states about the job id: asserting the file equals itself is a tautology.
FLOOR_IN_CORE = "scripts/merge_master/openxfactory-review-authority-floor.yaml"

# THE FLOORED SURFACE. `openspec/specs` is what the (b′) act enumerated (record
# §8, "THE EXTENSION — ALL 53, PINNED AND REGENERATED"), and it is a CODE
# CONSTANT here for the same reason `merge-master-approval.yml` makes it one: the
# generated block declares its prefix in a COMMENT, and a prefix read out of
# prose narrows silently when the prose changes.
FLOORED_PREFIX = "openspec/specs"

# WHERE A CHECKED-OUT PINNED CORE MAY BE FOUND. The environment variable is what
# `pytest-suite.yml` sets; the two relative fallbacks let a developer reproduce
# the freshness check by putting a codexFactory checkout in either place.
CORE_ENV_VAR = "PINNED_CORE_CHECKOUT"
CORE_FALLBACKS = (REPO_ROOT / ".merge-master-core",
                  REPO_ROOT.parent / ".merge-master-core")

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
GENERATED_AT_RE = re.compile(
    r"^\s*#\s*generated_at:\s*([0-9a-f]{40})\s*$", re.MULTILINE)


def tracked_paths_under(prefix: str) -> list[str]:
    """Every path git tracks under `prefix`, at the working tree's index.

    `git ls-files` and nothing else: no network, no other repository, no
    subprocess the hermeticity module has anything to say about.
    """
    result = subprocess.run(
        ["git", "ls-files", "--", prefix],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def floor_entries(document_text: str) -> list[str]:
    document = yaml.safe_load(document_text)
    if not isinstance(document, dict):
        raise AssertionError("the floor snapshot is not a YAML mapping")
    floor = document.get("floor")
    if not isinstance(floor, dict):
        raise AssertionError("the floor snapshot declares no `floor` mapping")
    entries = floor.get("never_clearable_paths")
    if not isinstance(entries, list) or not entries:
        raise AssertionError(
            "the floor snapshot declares no non-empty `never_clearable_paths`")
    return list(entries)


def uncovered(surface, entries) -> list[str]:
    """CSC-C6's assertion, as one expression: `surface - entries`.

    A function rather than an inline set difference so the negative controls can
    drive the SAME code the positive does. A falsification that exercises a
    reimplementation proves nothing about what ships.
    """
    return sorted(set(surface) - set(entries))


# --- mirror-floor-addition-grace: the REQUIRED lane's own classification ----
#
# RATIFIED 2026-09-05 by Brett Heap, in session, verbatim "ratify the
# companion when green, then realize it" (packet
# `openspec/changes/mirror-floor-addition-grace/`). Mirrors the pinned core's
# `merge_master.repository_floor_drift.evaluate_floor_completeness` — NOT by
# IMPORTING it (authoring decision A: the pinned core checkout carries
# `continue-on-error: true` below by design, so an importing REQUIRED
# assertion could only skip on an outage — a CSC-F16 silent-false-green — or
# fail for a cause no candidate can fix, which this file's own rule forbids).
# The mirror is written LOCALLY, from git alone, and is FALSIFIED by replaying
# the core's own exported vectors (`TheVectorReplay`, below `NegativeControls`)
# rather than by importing the function it mirrors.
#
# A tracked path absent from the floor is COVERED-PENDING, not uncovered, when
# the candidate's own diff CREATES it, or when it was added to the base branch
# after the floor snapshot's declared `generated_at` (B1) — never for a
# removal, a rename or a modification, and never for an unmeasurable base or
# pin (fail-safe, the default). These two reason strings are the pinned core's
# own (`repository_floor_drift.PENDING_CREATED_BY_CANDIDATE` /
# `PENDING_ADDED_TO_BASE_AFTER_PIN`), copied as literals rather than imported,
# for the same reason the rule itself is mirrored rather than imported.
PENDING_CREATED_BY_CANDIDATE = "created_by_candidate"
PENDING_ADDED_TO_BASE_AFTER_PIN = "added_to_base_after_pin"

# The base branch this checkout can resolve. `origin/main` first — the
# PUBLISHED branch is what a pin window and a candidate's own diff are
# measured against — falling back to a local `main` for a checkout with no
# remote-tracking ref (a fixture, a bare mirror). Neither resolving is one of
# the fail-safe cases the requirement names: no grace from either half of the
# rule, on a checkout the required assertion cannot orient itself in.
BASE_BRANCH_CANDIDATES = ("origin/main", "main")


def _git(*arguments: str, repo: pathlib.Path = REPO_ROOT
         ) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], cwd=repo, capture_output=True, text=True)


def resolve_base_branch(repo: pathlib.Path = REPO_ROOT) -> str | None:
    """The base branch ref this checkout can resolve, or None (fail-safe).

    `repo` defaults to this repository's real root; a test may pass a
    synthetic repository to exercise the resolution order without touching
    the real checkout.
    """
    for ref in BASE_BRANCH_CANDIDATES:
        result = _git("rev-parse", "--verify", "--quiet", ref, repo=repo)
        if result.returncode == 0 and result.stdout.strip():
            return ref
    return None


def created_since_merge_base(
    base_ref: str, prefix: str, repo: pathlib.Path = REPO_ROOT
) -> tuple[str, ...] | None:
    """Paths under `prefix` THIS CANDIDATE'S OWN diff creates, or None.

    `git diff --name-status --diff-filter=A <merge-base>..HEAD -- <prefix>`,
    against the MERGE BASE of HEAD and `base_ref` — never HEAD's raw diff
    against `base_ref` directly, which would also charge this candidate for
    commits `base_ref` gained after it branched. `--diff-filter=A` alone
    already excludes a modification (`M`), a removal (`D`) and — on a git
    checkout with rename detection at its default threshold, which this
    invocation neither disables nor configures — a rename (`R`): none of
    those statuses is `A`, so none is counted as created. `None` when the
    merge base cannot be computed: no candidate diff is measurable, so this
    half of the rule grants nothing, exactly as the requirement's fail-safe
    states.
    """
    merge_base = _git("merge-base", "HEAD", base_ref, repo=repo)
    if merge_base.returncode != 0 or not merge_base.stdout.strip():
        return None
    result = _git(
        "diff", "--name-status", "--diff-filter=A",
        "%s..HEAD" % merge_base.stdout.strip(), "--", prefix, repo=repo)
    if result.returncode != 0:
        return None
    created = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].startswith("A"):
            created.append(parts[-1])
    return tuple(sorted(created))


def pin_window(
    generated_at: str | None, base_ref: str, prefix: str,
    repo: pathlib.Path = REPO_ROOT,
) -> tuple[str, ...] | None:
    """B1's window: paths added to `base_ref` after `generated_at`, or None.

    Byte for byte the pinned core's own invocation
    (`specs_floor_block.paths_added_after_pin`), copied rather than
    paraphrased: `--name-only --pretty=format:` are load-bearing, since
    without them `git log` emits commit headers rather than a path list — a
    mirror parsing that would be reading a different thing from the core it
    mirrors. `None` — no grace — when `generated_at` is absent, malformed, does
    not resolve, or is not an ancestor of `base_ref`: an unresolvable pin is a
    reason to refuse, never a reason to excuse.
    """
    if not generated_at or not SHA40_RE.match(generated_at):
        return None
    resolved = _git("rev-parse", "--verify", "--quiet", generated_at, repo=repo)
    if resolved.returncode != 0 or not resolved.stdout.strip():
        return None
    pin = resolved.stdout.strip()
    ancestor = _git("merge-base", "--is-ancestor", pin, base_ref, repo=repo)
    if ancestor.returncode != 0:
        return None
    result = _git(
        "log", "--diff-filter=A", "--name-only", "--pretty=format:",
        "%s..%s" % (pin, base_ref), "--", prefix, repo=repo)
    if result.returncode != 0:
        return None
    return tuple(sorted(
        {line.strip() for line in result.stdout.splitlines() if line.strip()}))


def graced_uncovered(surface, entries, created, window):
    """`uncovered()`, minus the grace — THE mirrored completeness rule.

    `created` and `window` are each `None` (not measured — grants nothing from
    that half) or a tuple of paths (measured, possibly empty). Returns
    `(uncovered, pending)`: `uncovered` a sorted tuple of paths, `pending` a
    tuple of `(path, reason)` pairs sorted by path — the same two-result shape
    `evaluate_floor_completeness` returns as `.uncovered` and `.pending`, so a
    divergence between this function and the pinned core is a divergence in
    DATA, falsified by `TheVectorReplay`, never a divergence in shape.

    A path CREATED by this candidate's own diff wins over a path merely inside
    the pin window when (in principle) both could apply to the same path —
    checked in that order, matching the pinned core's own branching.
    """
    off_floor = uncovered(surface, entries)
    created_set = set(created or ())
    window_set = set(window or ())
    unc: list[str] = []
    pending: list[tuple[str, str]] = []
    for path in off_floor:
        if created is not None and path in created_set:
            pending.append((path, PENDING_CREATED_BY_CANDIDATE))
        elif window is not None and path in window_set:
            pending.append((path, PENDING_ADDED_TO_BASE_AFTER_PIN))
        else:
            unc.append(path)
    return tuple(unc), tuple(sorted(pending))


def locate_pinned_core() -> pathlib.Path | None:
    """The checked-out pinned core, or None when nothing supplied one.

    `PINNED_CORE_CHECKOUT` IS AUTHORITATIVE WHEN SET, and the fallbacks apply
    only when it is not. That asymmetry is deliberate and it is the same rule
    the rest of this design follows: a caller that NAMES a core and does not get
    it must be told so, not quietly handed a different tree that happens to be
    lying around. Falling back there would verify the snapshot against something
    nobody asked for and report it as a pass — the silent-degradation shape the
    exact skip pin exists to make impossible.

    The fallbacks stay for the developer case, where nothing is named and a
    checkout in the obvious place is a convenience rather than a claim.
    """
    declared = os.environ.get(CORE_ENV_VAR)
    candidates = ([pathlib.Path(declared)] if declared
                  else list(CORE_FALLBACKS))
    for candidate in candidates:
        if (candidate / FLOOR_IN_CORE).is_file():
            return candidate
    return None


def pinned_core_checkout_step(document: dict) -> dict:
    """The one step in `pytest-suite.yml` that checks out the decision core."""
    found = []
    for job in (document.get("jobs") or {}).values():
        for step in (job or {}).get("steps") or []:
            with_block = (step or {}).get("with") or {}
            if with_block.get("repository") == PINNED_REPOSITORY:
                found.append(step)
    if len(found) != 1:
        raise AssertionError(
            "expected exactly one checkout of %s in %s, found %d"
            % (PINNED_REPOSITORY, PYTEST_SUITE.name, len(found)))
    return found[0]


class TheRealFiles(unittest.TestCase):
    """Tier 1 — the shipped bytes, not a fixture."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot_bytes = SNAPSHOT.read_bytes()
        cls.snapshot_text = SNAPSHOT.read_text(encoding="utf-8")
        cls.pin = yaml.safe_load(PIN.read_text(encoding="utf-8"))
        cls.declaration = cls.pin.get("floor_snapshot") or {}
        cls.entries = floor_entries(cls.snapshot_text)
        found = GENERATED_AT_RE.findall(cls.snapshot_text)
        cls.generated_at = found[0] if len(found) == 1 else None

    def test_the_snapshot_exists_and_the_pin_declares_it(self) -> None:
        self.assertTrue(SNAPSHOT.is_file(), f"missing snapshot: {SNAPSHOT}")
        self.assertEqual(
            self.declaration.get("path"),
            str(SNAPSHOT.relative_to(REPO_ROOT)),
            "the pin must name the snapshot it vouches for")
        self.assertEqual(
            self.declaration.get("of"), FLOOR_IN_CORE,
            "the pin must name WHICH document in the pinned core this copies")
        self.assertEqual(
            self.declaration.get("taken_at"), "core_commit",
            "a snapshot taken at anything but the pinned commit is a copy of a "
            "document this repository does not consume")

    def test_the_snapshot_matches_the_digest_the_pin_declares(self) -> None:
        """The byte-identity claim, checked rather than asserted in prose.

        Same discipline as `contracts/openxwallet-pin.yaml`'s eight digests and
        `scripts/verify-openxwallet-pin.py`'s `pin-digest-mismatch` refusal: a
        vendored copy nobody verifies is a copy that has already drifted.
        """
        declared = self.declaration.get("sha256")
        self.assertRegex(str(declared), r"^[0-9a-f]{64}$",
                         "the pin must declare a 64-hex sha256 for the snapshot")
        self.assertEqual(
            hashlib.sha256(self.snapshot_bytes).hexdigest(), declared,
            "SNAPSHOT DIGEST MISMATCH: %s does not hash to the `sha256` "
            "declared in %s. The snapshot is a witness; an edited witness "
            "proves nothing. Re-copy it from the pinned core and recompute."
            % (SNAPSHOT.relative_to(REPO_ROOT), PIN.relative_to(REPO_ROOT)))

    def test_the_snapshot_is_this_repositorys_floor_document(self) -> None:
        document = yaml.safe_load(self.snapshot_text)
        self.assertEqual(document.get("schema_version"), 1)
        self.assertEqual(document.get("kind"), "repository_gate_floor")
        floor = document.get("floor") or {}
        self.assertEqual(
            floor.get("repository"), FLOOR_REPOSITORY,
            "a snapshot of some other repository's floor would assert coverage "
            "over a surface this repository does not own")
        self.assertTrue(str(floor.get("id") or "").strip())

    def test_the_pin_declares_the_snapshots_entry_count(self) -> None:
        """A second, independent witness to the number, in the reviewed file."""
        self.assertEqual(
            self.declaration.get("entry_count"), len(self.entries),
            "the pin declares %r floor entries and the snapshot carries %d"
            % (self.declaration.get("entry_count"), len(self.entries)))

    def test_every_tracked_openspec_spec_path_is_on_the_floor(self) -> None:
        """CSC-C6, AND THE POINT OF THIS MODULE.

        LQ-A7's falsification, stated by LQ: *"seed one uncovered spec path and
        the lane must go red."* Here it reds a REQUIRED check.

        GRACED since `mirror-floor-addition-grace`: a path this candidate's own
        diff creates, or that landed on the base branch after the snapshot's
        declared `generated_at`, is COVERED-PENDING rather than uncovered — see
        `graced_uncovered` above. Neither half of the grace is measurable on a
        checkout with no base branch or no resolvable pin, and on such a
        checkout this assertion behaves EXACTLY as it did before the grace
        existed: fail-safe, and the default.
        """
        surface = tracked_paths_under(FLOORED_PREFIX)
        # ANTI-VACUITY. An empty surface satisfies any floor, so an assertion
        # over one is an assertion over nothing. This repository has carried
        # promoted specs since long before the floor did.
        self.assertGreater(
            len(surface), 0,
            "no tracked path under %r — the coverage assertion below would pass "
            "over any floor at all, including an empty one" % FLOORED_PREFIX)
        base_ref = resolve_base_branch()
        created = (created_since_merge_base(base_ref, FLOORED_PREFIX)
                   if base_ref is not None else None)
        window = (pin_window(self.generated_at, base_ref, FLOORED_PREFIX)
                  if base_ref is not None else None)
        missing, pending = graced_uncovered(surface, self.entries, created, window)
        if pending:
            # "a graced run says what is OWED" (task 2.3): informational, not
            # asserted — a passing run still records that a regeneration is
            # owed, rather than the grace going unremarked because nothing
            # failed.
            print(
                "GRACED (covered-pending, regeneration OWED): %d path(s): %s"
                % (len(pending),
                   ", ".join("%s (%s)" % item for item in pending)))
        self.assertEqual(
            missing, (),
            "%d tracked path(s) under %r are ABSENT from the floor's "
            "never_clearable_paths and NOT covered by the addition grace:\n"
            "  %s\n\n"
            "%s"
            "The enumeration is EXACT, so a spec added off the floor is a spec "
            "the floor does not protect. The repair is ordered, across two "
            "repositories:\n"
            "  1. a codexFactory pull request regenerating the block at an "
            "openxFactory commit that carries the new path "
            "(scripts/merge_master/generate_specs_floor_block.py);\n"
            "  2. an openxFactory pull request advancing "
            "contracts/review-lane-pin.yaml core_commit, the two pin literals "
            "in .github/workflows/merge-master-approval.yml, the core checkout "
            "ref in .github/workflows/pytest-suite.yml, and this snapshot with "
            "its digest — all in lockstep;\n"
            "  3. the addition.\n"
            "See the pinned core's docs/repository-gate-floor-repair-runbook.md."
            % (len(missing), FLOORED_PREFIX, "\n  ".join(missing),
               ("%d path(s) ARE covered-pending and do not count against this "
                "failure: %s\n\n"
                % (len(pending),
                   ", ".join("%s (%s)" % item for item in pending))
                if pending else "")))

    def test_the_generated_block_declares_the_commit_it_was_derived_at(self) -> None:
        """LA-A1: *"the object must be PINNED, not described."*

        The generated block's header carries `generated_at`, the openxFactory
        commit `git ls-tree` was run against. It is a repo-local value living in
        `contracts/**`, which is inside the derivation-pin sweep roots, and it
        RESOLVES — so it is declared in `scripts/doc_health/pin_class.py` as a
        NON-MEMBER, with its reason, rather than as a member. The measurement
        behind that choice is in `contracts/review-lane-pin.yaml` beside the
        `floor_snapshot` block and in the `NON_MEMBERS` row itself.

        So THIS is the check that the pin is present and well-formed, and the
        `sha256` plus the freshness comparison are what bind it to real bytes.
        """
        found = GENERATED_AT_RE.findall(self.snapshot_text)
        self.assertEqual(
            len(found), 1,
            "the snapshot must carry exactly one `generated_at` pin in the "
            "generated block's header, found %d" % len(found))
        self.assertRegex(found[0], SHA40_RE)

    def test_the_required_suite_checks_out_the_pinned_core(self) -> None:
        """The fourth site the core commit is written, tied to the pin.

        Without this the freshness verifier could compare the snapshot against
        SOME codexFactory tree rather than against the one this repository
        consumes, which is a comparison that proves nothing.
        """
        document = yaml.safe_load(PYTEST_SUITE.read_text(encoding="utf-8"))
        step = pinned_core_checkout_step(document)
        with_block = step.get("with") or {}
        self.assertEqual(
            with_block.get("ref"), self.pin.get("core_commit"),
            "PIN DRIFT: %s checks out %s@%s but %s declares core_commit %s. "
            "Change BOTH in one reviewed diff."
            % (PYTEST_SUITE.relative_to(REPO_ROOT), PINNED_REPOSITORY,
               with_block.get("ref"), PIN.relative_to(REPO_ROOT),
               self.pin.get("core_commit")))
        self.assertIs(
            step.get("continue-on-error"), True,
            "the core checkout must NOT be able to fail this required job "
            "directly: a required check that fails for reasons the candidate "
            "cannot fix blocks everything (pytest-suite.yml's own rule). Its "
            "failure is surfaced by the exact skip pin instead.")
        self.assertFalse(
            str(with_block.get("path") or "").startswith("openxFactory"),
            "the core must be checked out BESIDE this repository's tree, not "
            "inside it: a foreign checkout under the repo root is visible to "
            "every test that scans the real tree")

    def test_the_required_suite_hands_the_core_to_the_test(self) -> None:
        text = PYTEST_SUITE.read_text(encoding="utf-8")
        self.assertIn(
            CORE_ENV_VAR, text,
            "the pytest step must export %s so the freshness verifier can find "
            "the checkout; without it the verifier skips on every run and the "
            "skip pin moves" % CORE_ENV_VAR)

    def test_the_required_suite_watches_the_verifier_by_name(self) -> None:
        """The node id in the workflow must be THIS test's, still.

        `pytest-suite.yml` asserts the freshness verifier RAN AND PASSED by
        looking its `<testcase>` up in the JUnit report by classname and name —
        the fix for the Codex P2 finding on PR #569, which observed that the
        aggregate `EXPECT_SKIPPED` pin cannot distinguish "the verifier
        vanished" from "the verifier vanished and something else started
        running", and goes GREEN on the pair.

        A watcher pointed at a node id that no longer exists is the same defect
        one level up, so the pair is asserted here against the LIVE class and
        method objects: rename either and this fails on the developer's machine,
        naming the two strings to move. (In CI the rename would red anyway — the
        verdict becomes `absent` — but it would red as a mystery.)
        """
        text = PYTEST_SUITE.read_text(encoding="utf-8")
        # pytest's JUnit `classname` is the node id with `/` and the `.py`
        # suffix folded to dots, taken from the path relative to rootdir — NOT
        # `__module__`, which is the bare `test_floor_snapshot` here because
        # `tests/` carries no `__init__.py`. Rebuild it the way the report does.
        module_path = pathlib.Path(__file__).resolve().relative_to(REPO_ROOT)
        classname = "%s.%s" % (
            ".".join(module_path.with_suffix("").parts),
            TheFreshnessVerifier.__name__)
        testname = (TheFreshnessVerifier
                    .test_the_snapshot_is_byte_identical_to_the_pinned_core
                    .__name__)
        for label, value in (("FRESHNESS_CLASSNAME", classname),
                             ("FRESHNESS_TESTNAME", testname)):
            self.assertIn(
                '%s: "%s"' % (label, value), text,
                "%s in %s must name the freshness verifier's live node id "
                "(%s), or the required check watches nothing. Move it with the "
                "rename, in the same diff."
                % (label, PYTEST_SUITE.relative_to(REPO_ROOT), value))

    def test_the_required_suite_watches_the_vector_replay_by_name(self) -> None:
        """The SECOND watched pair, task 2.7 — same discipline, applied again.

        `mirror-floor-addition-grace` moves `EXPECT_SKIPPED` 21 -> 22 and adds
        a second named watch, `VECTOR_REPLAY_CLASSNAME` / `VECTOR_REPLAY_TESTNAME`,
        for the same reason `FRESHNESS_CLASSNAME` / `FRESHNESS_TESTNAME` exist:
        an aggregate skip count cannot tell "the vector replay stopped running"
        from "the vector replay stopped running AND some other conditional skip
        started", and goes green on the canceling pair. Asserted here against
        the LIVE class and method objects, same as the freshness pair above.
        """
        text = PYTEST_SUITE.read_text(encoding="utf-8")
        module_path = pathlib.Path(__file__).resolve().relative_to(REPO_ROOT)
        classname = "%s.%s" % (
            ".".join(module_path.with_suffix("").parts),
            TheVectorReplay.__name__)
        testname = TheVectorReplay.test_every_vector_replays.__name__
        for label, value in (("VECTOR_REPLAY_CLASSNAME", classname),
                             ("VECTOR_REPLAY_TESTNAME", testname)):
            self.assertIn(
                '%s: "%s"' % (label, value), text,
                "%s in %s must name the vector replay's live node id (%s), or "
                "the required check watches nothing. Move it with the rename, "
                "in the same diff."
                % (label, PYTEST_SUITE.relative_to(REPO_ROOT), value))

    def test_the_snapshot_is_a_declared_non_member_of_the_pin_class(self) -> None:
        """The exclusion must be DECLARED, and it must still be there.

        The snapshot's `generated_at` is a resolvable 40-hex value inside the
        derivation-pin sweep roots, so `pin_class.py` has to say something about
        it. What it says is `NON_MEMBERS`, with the measurement — and an
        exclusion nobody can read is indistinguishable from a coverage gap, so
        this asserts the row exists AND that it carries a real reason.
        """
        import importlib.util
        import sys

        name = "_floor_snapshot_pin_class_probe"
        spec = importlib.util.spec_from_file_location(
            name, REPO_ROOT / "scripts/doc_health/pin_class.py")
        module = importlib.util.module_from_spec(spec)
        # Registered before exec: `@dataclass` resolves annotations through
        # `sys.modules[cls.__module__].__dict__`. Same note as the caller test.
        sys.modules[name] = module
        spec.loader.exec_module(module)

        relative = str(SNAPSHOT.relative_to(REPO_ROOT))
        reason = module.non_member_reason(relative)
        self.assertIsNotNone(
            reason,
            "%s carries a resolvable commit (`generated_at`) inside the sweep "
            "roots, so the pin class must declare it — as a member or as a "
            "non-member. Silence is a coverage gap." % relative)
        self.assertGreater(len(reason), 40, "the exclusion must state WHY")
        self.assertNotIn(
            "generated_at", module.PIN_KEY_VOCABULARY,
            "declaring `generated_at` as a member key widens the sweep "
            "repo-wide over files whose `generated_at` is an ISO timestamp, "
            "and classifies this comment-carried value twice. The measurement "
            "is in the NON_MEMBERS row; do not undo it by adding a member.")

    def test_the_snapshot_is_routed_to_a_code_owner(self) -> None:
        owners = (REPO_ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
        self.assertRegex(
            owners,
            r"(?m)^/contracts/review-lane-floor-snapshot\.yaml\s+@\S+",
            "the snapshot is the bytes a REQUIRED check asserts against, so it "
            "must be routed to a human owner like the pin beside it")


class TheFreshnessVerifier(unittest.TestCase):
    """Tier 1b — the snapshot against the AUTHORITATIVE floor, when reachable.

    THE ONLY SKIPPING TEST IN THIS DIRECTORY, and the skip is load-bearing.

    On the normal path the checkout in `pytest-suite.yml` succeeds and this test
    RUNS. If the cross-repository fetch ever stops working — a revoked App
    grant, a codexFactory outage, a rewritten history — this test skips and the
    REQUIRED check goes red naming the drift. The coverage assertion above keeps
    holding from the snapshot throughout, so an outage never wedges the
    repository; it only becomes IMPOSSIBLE TO MISS.

    WHAT MAKES IT RED, EXACTLY, AND IN WHICH ORDER:

    1. `pytest-suite.yml`'s pin step looks THIS testcase up in
       `pytest-report.xml` by classname and name — `FRESHNESS_CLASSNAME` /
       `FRESHNESS_TESTNAME` there — and requires the verdict `passed`. Absent,
       skipped, failed and errored each fail the job with
       *"snapshot freshness verifier did not run — pinned core checkout
       unavailable or test removed"*. This is the load-bearing signal.
    2. `EXPECT_SKIPPED` remains pinned exactly, and the skip still moves it to
       22. That is the backstop and the general skip discipline, no longer the
       primary signal: an aggregate cannot distinguish this skip appearing from
       this skip appearing WHILE another conditional skip starts running, and
       goes green on the pair. Codex raised it as P2 on PR #569; the named
       assertion above is the answer, and the reason it is stated first.

    That trade is the whole design: *"the exact skip pin converts 'the
    cross-repository fetch quietly stopped working' from a silent degradation
    into a red required check with a named cause"* — now converted by the name
    rather than by the count, which is the defect class CSC-F16 and CSC-F14 are
    about, applied once more to the guard itself.
    """

    def test_the_snapshot_is_byte_identical_to_the_pinned_core(self) -> None:
        core = locate_pinned_core()
        if core is None:
            raise unittest.SkipTest(
                "FRESHNESS-VERIFIER-DID-NOT-RUN: no pinned decision core on "
                "disk (set %s, or place a codexFactory checkout at "
                ".merge-master-core). In CI this skip means the "
                "cross-repository checkout FAILED: pytest-suite.yml requires "
                "this testcase to have PASSED in the JUnit report and fails "
                "the required check by name when it did not."
                % CORE_ENV_VAR)
        authoritative = (core / FLOOR_IN_CORE).read_bytes()
        vendored = SNAPSHOT.read_bytes()
        self.assertEqual(
            hashlib.sha256(vendored).hexdigest(),
            hashlib.sha256(authoritative).hexdigest(),
            "SNAPSHOT IS STALE: %s differs from %s in the pinned core at %s. "
            "The vendored copy is what the required coverage assertion reads, "
            "so a stale copy can assert coverage the real floor does not give. "
            "Re-copy it and recompute the digest in %s."
            % (SNAPSHOT.relative_to(REPO_ROOT), FLOOR_IN_CORE,
               yaml.safe_load(PIN.read_text(encoding="utf-8"))["core_commit"],
               PIN.relative_to(REPO_ROOT)))


class NegativeControls(unittest.TestCase):
    """Tier 2 — each positive above is one mutation from failing."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot_text = SNAPSHOT.read_text(encoding="utf-8")
        cls.entries = floor_entries(cls.snapshot_text)
        cls.surface = tracked_paths_under(FLOORED_PREFIX)

    def test_the_unmutated_surface_is_a_positive_first(self) -> None:
        """Ordering guard: a control that never passes proves nothing.

        Moved onto the GRACED expression (authoring decision E): a control that
        never drives the same code the shipped assertion drives proves nothing
        about what ships. `created=()` / `window=()` — measured, and empty —
        so this exercises the graced expression's own no-grace-needed path
        rather than either fail-safe branch (those are `NegativeControls`
        below).
        """
        self.assertEqual(
            graced_uncovered(self.surface, self.entries, (), ()), ((), ()))

    def test_a_fabricated_off_floor_spec_path_is_refused(self) -> None:
        """LQ-A7's falsification, run through the SHIPPED (graced) expression.

        The fabrication is in the SURFACE rather than in the floor, because that
        is the direction the real failure arrives from: somebody adds a spec.

        THE FABRICATED PATH IS CREATED BY NO DIFF AND LIES IN NO WINDOW, SO IT
        STAYS REFUSED — asserted in those words (authoring decision E), so the
        grace can never be misread as "additions are free". `created=()` /
        `window=()`: both halves of the rule were MEASURED here, and neither
        carries this path.
        """
        fabricated = "openspec/specs/a-capability-nobody-floored/spec.md"
        self.assertNotIn(fabricated, self.entries)
        missing, pending = graced_uncovered(
            self.surface + [fabricated], self.entries, (), ())
        self.assertEqual(
            missing, (fabricated,),
            "the coverage assertion must name the uncovered path, and only it "
            "— a fabricated path created by no diff and lying in no measured "
            "pin window is refused, exactly as before the grace existed")
        self.assertEqual(
            pending, (),
            "a path no diff creates and no window carries must not be "
            "reported covered-pending")

    def test_a_floor_that_lost_one_entry_is_refused(self) -> None:
        """The other direction: the floor narrows while the surface holds.

        The victim is drawn from the INTERSECTION rather than from
        `surface[0]`, so this control stays a one-mutation control even when the
        surface is independently broken — otherwise a run with an off-floor spec
        already present would report two uncovered paths and this control would
        fail for somebody else's reason.
        """
        covered = [p for p in self.surface if p in set(self.entries)]
        self.assertGreater(len(covered), 0, "nothing to remove from the floor")
        victim = covered[0]
        surviving = [e for e in self.entries if e != victim]
        self.assertNotEqual(surviving, self.entries, "mutation did not apply")
        self.assertIn(victim, uncovered(self.surface, surviving))

    def test_a_bare_directory_entry_protects_nothing(self) -> None:
        """Exact set membership, restated as a control.

        The floor names files. A floor of the DIRECTORY would match none of
        them, which is why the (b′) act enumerated 53 paths rather than one
        prefix — and why a future editor must not "simplify" it.
        """
        self.assertEqual(
            len(uncovered(self.surface, [FLOORED_PREFIX])), len(self.surface))

    def test_a_mutated_snapshot_fails_its_digest(self) -> None:
        declared = (yaml.safe_load(PIN.read_text(encoding="utf-8"))
                    ["floor_snapshot"]["sha256"])
        mutated = self.snapshot_text + "\n# an edit nobody recorded\n"
        self.assertNotEqual(
            hashlib.sha256(mutated.encode("utf-8")).hexdigest(), declared,
            "the digest check must catch a snapshot edited without its digest")

    def test_a_named_core_that_is_absent_does_not_fall_back(self) -> None:
        """The skip is only legitimate when the NAMED core really is absent.

        FOUND BY CI, NOT BY REASONING, AND RECORDED SO IT STAYS FOUND. The first
        run of this module on a runner failed here with
        `PosixPath('.../openxFactory/.merge-master-core') is not None`: the
        locator had been written to try the declared path AND THEN the
        fallbacks, and on a runner `REPO_ROOT.parent/.merge-master-core` is a
        real codexFactory checkout — `GITHUB_WORKSPACE` is the parent of the
        repository checkout, which is where `pytest-suite.yml` puts it.

        Locally the fallbacks are empty and the bug was invisible. What it would
        have cost in production is worse than a red control: a run whose named
        core was missing would have verified the snapshot against whatever tree
        was lying beside the repository and reported a PASS. So the locator now
        treats the variable as authoritative when set, and this is the control.
        """
        environ = dict(os.environ)
        try:
            os.environ[CORE_ENV_VAR] = str(REPO_ROOT / "does-not-exist")
            self.assertIsNone(
                locate_pinned_core(),
                "a NAMED core that is absent must produce None — and therefore "
                "a skip, and therefore a moved skip count — rather than a "
                "silent fall back to a different tree")
        finally:
            os.environ.clear()
            os.environ.update(environ)

    def test_the_fallbacks_apply_only_when_nothing_is_named(self) -> None:
        """...and the developer convenience still works, unnamed.

        The other half of the asymmetry, asserted so a later simplification
        cannot quietly delete either branch.
        """
        import tempfile

        environ = dict(os.environ)
        with tempfile.TemporaryDirectory() as raw:
            fake = pathlib.Path(raw)
            (fake / FLOOR_IN_CORE).parent.mkdir(parents=True)
            (fake / FLOOR_IN_CORE).write_text("schema_version: 1\n")
            try:
                os.environ.pop(CORE_ENV_VAR, None)
                # By `sys.modules[__name__]` rather than by importing this
                # module's own name: `tests/review_lane_pin/` carries no
                # `__init__.py`, so the import name depends on collection, and
                # a control that depends on collection order is not a control.
                import sys

                module = sys.modules[__name__]
                original = module.CORE_FALLBACKS
                module.CORE_FALLBACKS = (fake,)
                try:
                    self.assertEqual(module.locate_pinned_core(), fake)
                finally:
                    module.CORE_FALLBACKS = original
            finally:
                os.environ.clear()
                os.environ.update(environ)

    def test_the_core_locator_finds_a_tree_that_carries_the_floor(self) -> None:
        """...and it must actually find one, or the skip is unfalsifiable."""
        import tempfile
        environ = dict(os.environ)
        with tempfile.TemporaryDirectory() as raw:
            fake = pathlib.Path(raw)
            (fake / FLOOR_IN_CORE).parent.mkdir(parents=True)
            (fake / FLOOR_IN_CORE).write_text("schema_version: 1\n")
            try:
                os.environ[CORE_ENV_VAR] = str(fake)
                self.assertEqual(locate_pinned_core(), fake)
            finally:
                os.environ.clear()
                os.environ.update(environ)


class TheGraceItself(unittest.TestCase):
    """Tier 2b — the grace's own negative controls (task 2.5).

    `NegativeControls` above falsifies the SHIPPED assertion by mutating its
    real inputs. These controls falsify `graced_uncovered` itself, at the
    classification level and — for the two measurement functions the git
    plumbing actually runs — against real, disposable git repositories built
    fresh per test, never against this repository's own history.
    """

    # -- the classification, given already-measured created/window sets ------

    def test_a_created_path_is_pending(self) -> None:
        path = "openspec/specs/new-capability/spec.md"
        missing, pending = graced_uncovered([path], [], (path,), None)
        self.assertEqual(missing, ())
        self.assertEqual(pending, ((path, PENDING_CREATED_BY_CANDIDATE),))

    def test_a_path_added_to_base_after_the_pin_is_pending(self) -> None:
        path = "openspec/specs/somebody-elses-capability/spec.md"
        missing, pending = graced_uncovered([path], [], (), (path,))
        self.assertEqual(missing, ())
        self.assertEqual(pending, ((path, PENDING_ADDED_TO_BASE_AFTER_PIN),))

    def test_a_modification_a_copy_a_rename_and_a_removal_are_not_pending(
        self,
    ) -> None:
        """None of the four ever populates `created` or `window` — by
        construction, since `--diff-filter=A` on the required lane's own
        measurement (and B1's own `--diff-filter=A` window) only ever
        contains additions — so a path absent from both, MEASURED, stays
        uncovered regardless of which of the four is why it is absent."""
        path = "openspec/specs/touched-but-not-created/spec.md"
        for label in ("modification", "copy", "rename", "removal"):
            with self.subTest(status=label):
                missing, pending = graced_uncovered([path], [], (), ())
                self.assertEqual(missing, (path,), label)
                self.assertEqual(pending, (), label)

    def test_an_unmeasurable_created_set_grants_nothing_from_that_half(
        self,
    ) -> None:
        path = "openspec/specs/unmeasurable-base/spec.md"
        missing, pending = graced_uncovered([path], [], None, None)
        self.assertEqual(missing, (path,))
        self.assertEqual(pending, ())
        # The OTHER half can still independently grace the same path — an
        # unmeasurable base does not disable the pin window's own grace.
        missing, pending = graced_uncovered([path], [], None, (path,))
        self.assertEqual(missing, ())
        self.assertEqual(pending, ((path, PENDING_ADDED_TO_BASE_AFTER_PIN),))

    def test_an_unmeasurable_pin_window_grants_nothing_from_that_half(
        self,
    ) -> None:
        path = "openspec/specs/unmeasurable-pin/spec.md"
        missing, pending = graced_uncovered([path], [], (), None)
        self.assertEqual(missing, (path,))
        self.assertEqual(pending, ())
        # The OTHER half can still independently grace the same path.
        missing, pending = graced_uncovered([path], [], (path,), None)
        self.assertEqual(missing, ())
        self.assertEqual(pending, ((path, PENDING_CREATED_BY_CANDIDATE),))

    # -- the actual git plumbing, against disposable repositories ------------

    @staticmethod
    def _run(repo: pathlib.Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=repo, check=True,
                        capture_output=True, text=True)

    @classmethod
    def _init_repo(cls, repo: pathlib.Path) -> None:
        cls._run(repo, "init", "-q", "-b", "main")
        cls._run(repo, "config", "user.email", "test@example.invalid")
        cls._run(repo, "config", "user.name", "test")

    @staticmethod
    def _write(repo: pathlib.Path, relative: str, text: str) -> None:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    @classmethod
    def _commit(cls, repo: pathlib.Path, message: str) -> str:
        cls._run(repo, "add", "-A")
        cls._run(repo, "commit", "-q", "-m", message)
        return cls._run_capture(repo, "rev-parse", "HEAD")

    @staticmethod
    def _run_capture(repo: pathlib.Path, *arguments: str) -> str:
        result = subprocess.run(["git", *arguments], cwd=repo, check=True,
                                 capture_output=True, text=True)
        return result.stdout.strip()

    def test_created_since_merge_base_finds_a_real_addition(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._commit(repo, "base")
            # `main` stays AT the base commit — never fast-forwarded — and the
            # candidate's own commit lands on a divergent branch, matching a
            # real pull request's shape. Committing everything straight onto
            # `main` would make `merge-base HEAD main` equal HEAD itself and
            # the diff since it vacuously empty, which would make the
            # exclusion controls below pass for no reason at all.
            self._run(repo, "checkout", "-q", "-b", "candidate")
            self._write(repo, "openspec/specs/beta/spec.md", "beta\n")
            self._commit(repo, "add beta")
            created = created_since_merge_base(
                "main", "openspec/specs", repo=repo)
            self.assertEqual(created, ("openspec/specs/beta/spec.md",))

    def test_created_since_merge_base_excludes_a_modification(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._commit(repo, "base")
            self._run(repo, "checkout", "-q", "-b", "candidate")
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha, edited\n")
            self._commit(repo, "modify alpha")
            created = created_since_merge_base(
                "main", "openspec/specs", repo=repo)
            self.assertEqual(created, ())

    def test_created_since_merge_base_excludes_a_removal(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._write(repo, "openspec/specs/beta/spec.md", "beta\n")
            self._commit(repo, "base")
            self._run(repo, "checkout", "-q", "-b", "candidate")
            (repo / "openspec/specs/beta/spec.md").unlink()
            self._commit(repo, "remove beta")
            created = created_since_merge_base(
                "main", "openspec/specs", repo=repo)
            self.assertEqual(created, ())

    def test_created_since_merge_base_excludes_a_rename(self) -> None:
        """A rename is detected as `R`, not `A`, at git's default similarity
        threshold (measured directly: `git diff --name-status` on this
        scenario reports `R100`), so `--diff-filter=A` alone already excludes
        it without this invocation configuring rename detection itself."""
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(
                repo, "openspec/specs/alpha/spec.md",
                "alpha content, long enough for similarity detection\n")
            self._commit(repo, "base")
            self._run(repo, "checkout", "-q", "-b", "candidate")
            (repo / "openspec/specs/alpha").rename(repo / "openspec/specs/renamed")
            self._run(repo, "add", "-A")
            self._run(repo, "commit", "-q", "-m", "rename alpha")
            created = created_since_merge_base(
                "main", "openspec/specs", repo=repo)
            self.assertEqual(created, ())

    def test_pin_window_finds_a_path_added_after_the_pin(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            pin = self._commit(repo, "pinned commit")
            self._write(repo, "openspec/specs/delta/spec.md", "delta\n")
            self._commit(repo, "bystander addition")
            window = pin_window(pin, "main", "openspec/specs", repo=repo)
            self.assertEqual(window, ("openspec/specs/delta/spec.md",))

    def test_pin_window_excludes_a_path_older_than_the_pin(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._write(repo, "openspec/specs/delta/spec.md", "delta\n")
            pin = self._commit(repo, "pinned commit, already carries delta")
            self._write(repo, "docs/note.md", "unrelated\n")
            self._commit(repo, "unrelated change")
            window = pin_window(pin, "main", "openspec/specs", repo=repo)
            self.assertEqual(window, ())

    def test_pin_window_is_none_for_an_unresolvable_pin(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._commit(repo, "base")
            fake_pin = "a" * 40
            window = pin_window(fake_pin, "main", "openspec/specs", repo=repo)
            self.assertIsNone(window)

    def test_pin_window_is_none_for_a_non_ancestor_pin(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "openspec/specs/alpha/spec.md", "alpha\n")
            self._commit(repo, "base")
            self._run(repo, "checkout", "-q", "--orphan", "unrelated")
            self._run(repo, "reset", "-q", "--hard")
            self._write(repo, "docs/other.md", "other line\n")
            other = self._commit(repo, "unrelated history")
            self._run(repo, "checkout", "-q", "main")
            window = pin_window(other, "main", "openspec/specs", repo=repo)
            self.assertIsNone(window)

    def test_resolve_base_branch_prefers_origin_main(self) -> None:
        with tempfile.TemporaryDirectory() as bare_raw, \
             tempfile.TemporaryDirectory() as clone_raw:
            bare = pathlib.Path(bare_raw)
            self._run(bare, "init", "-q", "--bare")
            origin = pathlib.Path(clone_raw) / "origin-seed"
            origin.mkdir()
            self._init_repo(origin)
            self._write(origin, "README.md", "seed\n")
            self._commit(origin, "seed")
            self._run(origin, "remote", "add", "bare", str(bare))
            self._run(origin, "push", "-q", "bare", "main")
            clone_dir = pathlib.Path(clone_raw) / "clone"
            subprocess.run(
                ["git", "clone", "-q", str(bare), str(clone_dir)],
                check=True, capture_output=True, text=True)
            self.assertEqual(resolve_base_branch(repo=clone_dir), "origin/main")

    def test_resolve_base_branch_falls_back_to_local_main(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._write(repo, "README.md", "seed\n")
            self._commit(repo, "seed")
            self.assertEqual(resolve_base_branch(repo=repo), "main")

    def test_resolve_base_branch_is_none_when_neither_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            self._init_repo(repo)
            self._run(repo, "checkout", "-q", "-b", "trunk")
            self._write(repo, "README.md", "seed\n")
            self._commit(repo, "seed")
            # `main` was never created — only `trunk` — and there is no
            # `origin` remote, so neither candidate resolves.
            self.assertIsNone(resolve_base_branch(repo=repo))


class TheVectorReplay(unittest.TestCase):
    """Tier 1c — falsified by the pinned core's own hand-written vectors.

    THE FALSIFIER FOR `graced_uncovered`, task 2.6. `NegativeControls` and
    `TheGraceItself` above exercise the mirror against cases this authoring
    session thought of; this class exercises it against
    `tests/merge-master/fixtures/floor-addition-grace/vectors.json`, the
    pinned core's OWN hand-written, independently-maintained falsifier for
    `evaluate_floor_completeness` — "the falsifier of the implementation, not
    a recording of it" (the fixture's own README). A divergence between this
    repository's mirror and the core's ratified rule shows up here as a
    failing vector, per the fixture's own stated purpose, rather than as a
    contradictory verdict on somebody's pull request.

    SKIPS — NEVER FAILS — when the pinned core is absent, same discipline as
    `TheFreshnessVerifier`, and for the same reason: this is a REQUIRED
    check, and a cross-repository outage must not be able to fail it for a
    cause no candidate can fix. Watched BY NAME in `pytest-suite.yml`
    (`VECTOR_REPLAY_CLASSNAME` / `VECTOR_REPLAY_TESTNAME`,
    `test_the_required_suite_watches_the_vector_replay_by_name` above), same
    as the freshness verifier, and for the same reason: an aggregate skip
    count cannot tell this skip apart from a canceling pair.

    Compares only `tracked_under_prefix`, `uncovered` and `pending` — the
    facts the REQUIRED lane's simplified, git-only mirror actually computes.
    `stage` / `ok` / `escalated` / `refused_removals` / `already_unreachable`
    fold in drift attribution and D-3 tolerance, neither of which the
    required lane implements (design.md §2: LQ-A7 is completeness only; drift
    is the advisory lane's LA-A2/CPL-C1 and D-3 is the advisory lane's own
    escalation) — comparing them here would assert a property this mirror
    does not claim to have.
    """

    VECTORS_RELATIVE = "tests/merge-master/fixtures/floor-addition-grace/vectors.json"

    @staticmethod
    def _reconstruct_post_merge(base_tree_paths, changed_entries):
        """A MINIMAL, LOCAL port of the pinned core's post-merge
        reconstruction (`post_merge_tree_paths` / `_classify_changed_entries`),
        for this replay only — translating the vector fixture's GitHub-shaped
        `changed_entries` (`status` one of added/modified/renamed/copied/
        removed/…) into the `(post_merge_surface, created)` pair
        `graced_uncovered` needs. NOT used by the real git-based assertion
        above, which measures both directly from git and never sees a
        `status` field at all — that asymmetry is design.md §2's own subject.
        """
        removed: set[str] = set()
        present: set[str] = set()
        created: set[str] = set()
        for entry in changed_entries:
            filename = entry["filename"]
            status = entry.get("status")
            previous = entry.get("previous_filename")
            if status == "removed":
                removed.add(filename)
                continue
            if status == "renamed":
                if previous:
                    removed.add(previous)
                present.add(filename)
                continue
            present.add(filename)
            if status == "added":
                created.add(filename)
        base = set(base_tree_paths)
        post = (base - removed) | present
        return post, created

    def _replay_one(self, vector_input: dict) -> dict:
        prefix = vector_input["prefix"]
        if not isinstance(prefix, str) or not prefix.replace("/", "").strip():
            raise ValueError(
                "prefix %r names no floored surface" % (prefix,))
        normalized = prefix.rstrip("/") + "/"
        post, created = self._reconstruct_post_merge(
            vector_input["base_tree_paths"], vector_input["changed_entries"])
        tracked = tuple(sorted(p for p in post if p.startswith(normalized)))
        entries = list(vector_input["floor_paths"])
        window = vector_input["added_since_pin"]
        missing, pending = graced_uncovered(
            tracked, entries,
            created if created else (),
            tuple(window) if window is not None else None)
        return {
            "tracked_under_prefix": len(tracked),
            "uncovered": list(missing),
            "pending": [{"path": p, "reason": r} for p, r in pending],
        }

    def test_every_vector_replays(self) -> None:
        core = locate_pinned_core()
        if core is None:
            raise unittest.SkipTest(
                "VECTOR-REPLAY-DID-NOT-RUN: no pinned decision core on disk "
                "(set %s, or place a codexFactory checkout at "
                ".merge-master-core). In CI this skip means the "
                "cross-repository checkout FAILED: pytest-suite.yml requires "
                "this testcase to have PASSED in the JUnit report and fails "
                "the required check by name when it did not."
                % CORE_ENV_VAR)
        path = core / self.VECTORS_RELATIVE
        self.assertTrue(
            path.is_file(),
            "pinned core present but %s is missing — the fixture this replay "
            "falsifies against does not exist at %s" % (self.VECTORS_RELATIVE, core))
        fixture = json.loads(path.read_text(encoding="utf-8"))
        vectors = fixture.get("vectors") or []
        refused_vectors = fixture.get("refused_vectors") or []
        # A TRUNCATED FIXTURE MUST NOT PASS VACUOUSLY (task 2.6).
        self.assertGreater(
            len(vectors), 0,
            "the pinned core's vector fixture carries no accepted vectors — "
            "a truncated fixture would pass this replay vacuously")
        self.assertGreater(
            len(refused_vectors), 0,
            "the pinned core's vector fixture carries no refused vectors — "
            "a truncated fixture would pass this replay vacuously")
        for vector in vectors:
            with self.subTest(vector=vector["name"]):
                got = self._replay_one(vector["input"])
                expect = vector["expect"]
                self.assertEqual(
                    got["tracked_under_prefix"], expect["tracked_under_prefix"],
                    vector["name"])
                self.assertEqual(got["uncovered"], expect["uncovered"], vector["name"])
                self.assertEqual(got["pending"], expect["pending"], vector["name"])
        for vector in refused_vectors:
            with self.subTest(vector=vector["name"]):
                with self.assertRaises(Exception) as ctx:
                    self._replay_one(vector["input"])
                self.assertIn(
                    vector["expect"]["message_contains"], str(ctx.exception),
                    vector["name"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
