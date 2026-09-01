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
rather than a hole:** `EXPECT_SKIPPED` in `pytest-suite.yml` is pinned EXACTLY,
so a checkout that quietly stopped working moves the count off its pin and turns
the REQUIRED check red with a named cause. Silent degradation becomes visible.
Everything else here either passes or fails, following
`test_review_lane_caller.py`'s rule for the same reason.

TWO TIERS, as in that module: the shipped bytes first, then negative controls one
mutation away, so a check that has quietly stopped checking is visible.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import re
import subprocess
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


def locate_pinned_core() -> pathlib.Path | None:
    """The checked-out pinned core, or None when nothing supplied one."""
    declared = os.environ.get(CORE_ENV_VAR)
    candidates = ([pathlib.Path(declared)] if declared else []) + list(CORE_FALLBACKS)
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
        """
        surface = tracked_paths_under(FLOORED_PREFIX)
        # ANTI-VACUITY. An empty surface satisfies any floor, so an assertion
        # over one is an assertion over nothing. This repository has carried
        # promoted specs since long before the floor did.
        self.assertGreater(
            len(surface), 0,
            "no tracked path under %r — the coverage assertion below would pass "
            "over any floor at all, including an empty one" % FLOORED_PREFIX)
        missing = uncovered(surface, self.entries)
        self.assertEqual(
            missing, [],
            "%d tracked path(s) under %r are ABSENT from the floor's "
            "never_clearable_paths:\n  %s\n\n"
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
            % (len(missing), FLOORED_PREFIX, "\n  ".join(missing)))

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

    On the normal path the checkout in `pytest-suite.yml` succeeds, this test
    RUNS, and the suite's skipped count stays on its exact pin. If the
    cross-repository fetch ever stops working — a revoked App grant, a
    codexFactory outage, a rewritten history — this test skips, the count moves
    off `EXPECT_SKIPPED`, and the REQUIRED check goes red naming the drift. The
    coverage assertion above keeps holding from the snapshot throughout, so an
    outage never wedges the repository; it only becomes IMPOSSIBLE TO MISS.

    That trade is the whole design: *"the exact skip pin converts 'the
    cross-repository fetch quietly stopped working' from a silent degradation
    into a red required check with a named cause"* — which is the defect class
    CSC-F16 and CSC-F14 are about.
    """

    def test_the_snapshot_is_byte_identical_to_the_pinned_core(self) -> None:
        core = locate_pinned_core()
        if core is None:
            raise unittest.SkipTest(
                "no pinned decision core on disk (set %s, or place a "
                "codexFactory checkout at .merge-master-core). In CI this skip "
                "means the cross-repository checkout FAILED: the suite's exact "
                "skip pin moves and this required check goes red."
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
        """Ordering guard: a control that never passes proves nothing."""
        self.assertEqual(uncovered(self.surface, self.entries), [])

    def test_a_fabricated_off_floor_spec_path_is_refused(self) -> None:
        """LQ-A7's falsification, run through the SHIPPED expression.

        The fabrication is in the SURFACE rather than in the floor, because that
        is the direction the real failure arrives from: somebody adds a spec.
        """
        fabricated = "openspec/specs/a-capability-nobody-floored/spec.md"
        self.assertNotIn(fabricated, self.entries)
        missing = uncovered(self.surface + [fabricated], self.entries)
        self.assertEqual(
            missing, [fabricated],
            "the coverage assertion must name the uncovered path, and only it")

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

    def test_the_core_locator_refuses_a_directory_without_the_floor(self) -> None:
        """The skip is only legitimate when the core really is absent."""
        environ = dict(os.environ)
        try:
            os.environ[CORE_ENV_VAR] = str(REPO_ROOT / "does-not-exist")
            self.assertIsNone(locate_pinned_core())
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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
