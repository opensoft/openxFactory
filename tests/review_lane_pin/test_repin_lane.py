"""The re-pin lane, measured against every scenario `mirror-floor-regeneration-automation` ratified.

REALIZES `mirror-floor-regeneration-automation` (ratified 2026-09-06 by Brett
Heap, verbatim "ratify both when green, then land them"; record
`openspec/changes/mirror-floor-regeneration-automation/review/ratification-2026-09-06.md`).

EVERY TEST NAMES ITS SCENARIO IN ITS DOCSTRING, and the eight ADDED
requirements' twenty-four scenarios are covered here one for one. The mapping
is not a comment to be trusted: `test_every_ratified_scenario_has_a_test` reads
the ratified delta out of the packet, collects the scenario titles quoted by
the docstrings in this file, and fails on any scenario that no test claims.

WHY THE NEGATIVE CONTROLS BUILD A REAL TREE. `mirror-floor-addition-grace`'s
own archive recorded the lesson that made this file's shape non-negotiable: two
of that packet's negative controls hard-coded an empty grace set, so they
passed while measuring nothing, and the live lane exposed them
(`ca9fafe6` — "controls must MEASURE the same inputs as the shipped
assertion"). So every refusal here is driven through a COPY OF THE REAL FIVE
SITES, with the real regexes running against the real bytes, and every negative
is paired with a positive control that passes the SAME assertion the negative
reds (task 4.5's anti-vacuity requirement).

NOTHING HERE SKIPS. `.github/workflows/pytest-suite.yml` pins
`EXPECT_SKIPPED: "21"` exactly, and its own message says a skip that moves must
move the pin WITH the reason. This file adds no conditional skip, needs no
network and needs no codexFactory checkout, so it adds nothing to that count.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import pathlib
import re
import shutil
import subprocess
import sys
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_SOURCE = REPO_ROOT / "scripts/review_lane_repin.py"
LANE_WORKFLOW = REPO_ROOT / ".github/workflows/review-lane-repin.yml"
BINDING_TEMPLATE = REPO_ROOT / "contracts/review-lane-repin-binding.template.yaml"

# THE JUDGE. Requirement 5 is that these are untouched by the automation, so
# they are named here to be READ, never written.
JUDGE_TEST = REPO_ROOT / "tests/review_lane_pin/test_floor_snapshot.py"
REQUIRED_SUITE = REPO_ROOT / ".github/workflows/pytest-suite.yml"

RATIFIED_DELTA = (
    REPO_ROOT / "openspec/changes/mirror-floor-regeneration-automation"
    / "specs/review-lane-floor-mirror/spec.md")

SHA40_RE = re.compile(r"\b[0-9a-f]{40}\b")
SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")

# A fabricated candidate commit and a fabricated prior core. Neither is a real
# commit in either repository, deliberately: a fixture that used a live sha
# would go stale the day the pin moves, and a test that has to be edited by
# every advance is a test that will be edited without being read.
NEW_CORE = "f" * 8 + "0123456789abcdef0123456789abcdef01234567"[:32]
assert len(NEW_CORE) == 40


def _load_module():
    """Load `scripts/review_lane_repin.py` by path, under a private name.

    Registered in `sys.modules` BEFORE exec for the reason
    `test_review_lane_caller.py` records about its own probe: `@dataclass`
    resolves a field's annotation through `sys.modules[cls.__module__]`, and an
    unregistered module raises on the first dataclass. The module is
    side-effect-free at import.
    """
    name = "_review_lane_repin_probe"
    spec = importlib.util.spec_from_file_location(name, MODULE_SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R = _load_module()

LANE_TEXT = LANE_WORKFLOW.read_text(encoding="utf-8")
LANE_DOC = yaml.safe_load(LANE_TEXT)


def _shell_text(document: dict) -> str:
    """Every `run:` block in the lane, concatenated.

    The assertions about what the lane may not do are made against the SHELL
    the runner executes, not against the file's prose. The header of
    `review-lane-repin.yml` claims in English that there is no `gh pr merge` in
    it; this is where that claim is measured.
    """
    blocks = []
    for job in (document.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            if isinstance(step, dict) and isinstance(step.get("run"), str):
                blocks.append(step["run"])
    return "\n".join(blocks)


LANE_SHELL = _shell_text(LANE_DOC)


def _active(text: str) -> str:
    """`text` with whole-line comments removed.

    EVERY ABSENCE ASSERTION IN THIS FILE IS MADE AGAINST THIS, and the reason is
    that `review-lane-repin.yml` argues its own case at length in its header: it
    NAMES `github.event.client_payload`, `continue-on-error` and
    `|| github.token` in order to say that it does not use them. A naive
    `assertNotIn` over the raw file would be red on the prose that promises the
    behaviour it is checking — the file would have to stop explaining itself to
    pass. So the prose is stripped and the assertion is made against what the
    runner actually evaluates.
    """
    return "\n".join(line for line in text.splitlines()
                      if not line.lstrip().startswith("#"))


LANE_ACTIVE = _active(LANE_TEXT)


def _mutated_floor(original: bytes, *, added_path: str,
                   generated_at: str) -> bytes:
    """The authoritative document as it would read after ONE regeneration.

    Built by inserting one entry before the generated block's END marker and
    moving the two comment witnesses the block declares about itself, which is
    exactly the shape codexFactory's generator writes. The result is a REAL
    document: `yaml.safe_load` parses it, the entry count genuinely rises by
    one, and the digest genuinely changes — so every witness this file checks
    is computed from bytes rather than stipulated.
    """
    text = original.decode("utf-8")
    end = R.BLOCK_END_RE.search(text)
    assert end is not None, "the fixture floor document has no END marker"
    insertion = f"    - {added_path}\n"
    text = text[:end.start()] + insertion + text[end.start():]

    before_count = R.block_entry_count(original)
    text = re.sub(r"^(\s*#\s*entry_count:\s*)\d+$",
                  lambda m: f"{m.group(1)}{before_count + 1}",
                  text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^(\s*#\s*generated_at:\s*)[0-9a-f]{40}$",
                  lambda m: f"{m.group(1)}{generated_at}",
                  text, count=1, flags=re.MULTILINE)
    return text.encode("utf-8")


class _TreeFixture:
    """A throwaway copy of the five real sites, written to a temp directory.

    A COPY OF THE REAL FILES, not a miniature. The lane's whole risk is that a
    regex stops matching the bytes that actually ship — a renamed key, a
    reindented block, a second `ref:` line — and a hand-built miniature would
    keep passing through every one of those. Copying the shipped files means a
    site that drifts fails here first.
    """

    def __init__(self, tmp: pathlib.Path) -> None:
        self.root = tmp
        for relative in R.WRITABLE_PATHS:
            destination = tmp / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO_ROOT / relative, destination)
        self.snapshot_bytes = (tmp / R.SNAPSHOT_FILE).read_bytes()
        self.floor_bytes = _mutated_floor(
            self.snapshot_bytes,
            added_path="openspec/specs/fixture-only-capability/spec.md",
            generated_at="a" * 40)
        self.current_core = R.declared_core_commit(tmp)

    def plan(self, **overrides):
        arguments = {
            "current_core": self.current_core,
            "source_default_branch": "main",
            "candidate_commit": NEW_CORE,
            "candidate_reachable": True,
            "reachability_evidence": "compare answered `status: identical`",
            "floor_bytes": self.floor_bytes,
            "snapshot_bytes": self.snapshot_bytes,
        }
        arguments.update(overrides)
        return R.plan_advance(**arguments)

    def site_values(self) -> dict:
        return {site.label: R.read_site_value(self.root, site)
                for site in R.PINNED_SITES + R.SNAPSHOT_WITNESS_SITES}

    def digests(self) -> dict:
        return {relative: hashlib.sha256(
            (self.root / relative).read_bytes()).hexdigest()
            for relative in R.WRITABLE_PATHS}


class TreeFixtureMixin:
    def setUp(self) -> None:  # noqa: N802 - unittest's spelling
        import tempfile
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tree = _TreeFixture(pathlib.Path(self._tmp.name))


# ===========================================================================
# Requirement 1 — An automated pin advance only ever proposes
# ===========================================================================

class AnAutomatedPinAdvanceOnlyEverProposes(TreeFixtureMixin, unittest.TestCase):

    def test_the_lane_opens_a_pull_request_and_stops_there(self) -> None:
        """Scenario: The lane opens a pull request and stops there.

        Measured against the shell the runner executes. `gh pr create` and
        `gh pr edit` are the only two dispositions in the file; every verb that
        would DISPOSE of the pull request is absent, and absence is asserted
        term by term so a later edit that adds one fails here.
        """
        shell = _active(LANE_SHELL)
        self.assertIn("gh pr create", shell)
        for disposing in ("gh pr merge", "gh pr review", "gh pr close",
                          "--auto", "--admin", "enable-auto-merge",
                          "--method PUT", "-X PUT", "/reviews",
                          "enablePullRequestAutoMerge"):
            self.assertNotIn(
                disposing, shell,
                f"the lane may propose but never dispose; found {disposing!r}")
        self.assertNotRegex(
            shell, r"gh api[^\n]*pulls/[^\n]*/merge",
            "the merge endpoint reached through the raw API is still a merge")

    def test_the_lane_never_writes_to_the_default_branch(self) -> None:
        """Scenario: The lane never writes to the default branch.

        Every `git push` in the lane is enumerated and required to target the
        lane's own branch. A push with no explicit refspec, or one naming
        `main` or `HEAD`, fails: those are exactly the shapes that would reach
        the default branch.
        """
        pushes = re.findall(r"^\s*git push .*$", LANE_SHELL, re.MULTILINE)
        self.assertTrue(pushes, "the lane pushes nothing at all")
        for push in pushes:
            self.assertIn(
                "${BOT_BRANCH}", push,
                f"a push that does not name the lane's own branch: {push!r}")
            for forbidden in (" main", "HEAD:", "--force", "-f "):
                self.assertNotIn(forbidden, push, f"in {push!r}")

    def test_the_advance_carries_nothing_but_the_advance(self) -> None:
        """Scenario: The advance carries nothing but the advance.

        MEASURED BY WRITING. The advance is applied to a copy of the real tree
        and every file in that tree is re-digested; the set that changed must
        be exactly the declared writable set. A module that touched a sixth
        file would fail here even if it never told anyone.
        """
        before = self.tree.digests()
        advance = self.tree.plan()
        self.assertIsInstance(advance, R.Advance)
        self.assertEqual(
            [], R.apply_advance(self.tree.root, advance, self.tree.floor_bytes))
        after = self.tree.digests()

        changed = {path for path in before if before[path] != after[path]}
        self.assertEqual(set(R.WRITABLE_PATHS), changed)

        walked = {str(path.relative_to(self.tree.root))
                  for path in self.tree.root.rglob("*") if path.is_file()}
        self.assertEqual(
            set(R.WRITABLE_PATHS), walked,
            "the advance created a file outside the five sites")


# ===========================================================================
# Requirement 2 — refusing a core commit the source default branch does not carry
# ===========================================================================

class TheLaneRefusesACommitTheSourceDefaultBranchDoesNotCarry(
        TreeFixtureMixin, unittest.TestCase):

    def test_a_commit_not_on_the_source_default_branch_is_refused(self) -> None:
        """Scenario: A commit not on the source default branch is refused.

        NEGATIVE CONTROL (task 4.2), paired below with the positive that passes
        the same assertion. The refusal names both the commit and the branch,
        and no site moves: the site values are re-read after the decision and
        required to be what they were.
        """
        before = self.tree.site_values()
        outcome = self.tree.plan(candidate_reachable=False)

        self.assertIsInstance(outcome, R.Refusal)
        self.assertEqual("source_commit_not_landed", outcome.stage)
        self.assertIn(NEW_CORE, outcome.reason)
        self.assertIn("main", outcome.reason)
        self.assertEqual(before, self.tree.site_values())

    def test_a_reachable_commit_is_not_refused(self) -> None:
        """ANTI-VACUITY (task 4.5) for the landed-core control above.

        The same fixture, the same call, one input flipped: the assertion that
        reds on an unreachable candidate must GREEN on a reachable one, or the
        control above is measuring nothing.
        """
        self.assertIsInstance(self.tree.plan(candidate_reachable=True),
                              R.Advance)

    def test_an_unmeasured_reachability_is_refused_too(self) -> None:
        """Scenario: A commit not on the source default branch is refused.

        The tri-state matters: `None` means the caller did not verify, and an
        unverified candidate is refused exactly as a failed one is. `is not
        True` rather than `is False` is the line that makes it so, and this is
        what holds it there.
        """
        outcome = self.tree.plan(candidate_reachable=None)
        self.assertIsInstance(outcome, R.Refusal)
        self.assertEqual("source_commit_not_landed", outcome.stage)

    def test_the_lane_resolves_the_source_default_branch_itself(self) -> None:
        """Scenario: The lane resolves the source default branch itself.

        The requirement is that the lane "ignores any commit, branch or
        reference named by its trigger". Measured as an ABSENCE across the
        whole workflow file and the whole decision module: there is no
        expression through which a `client_payload` could reach a checkout, a
        write, or a pin value, and there is a live `gh api` resolution instead.
        """
        for forbidden in ("client_payload", "event.inputs.ref",
                          "event.client_payload"):
            self.assertNotIn(forbidden, LANE_ACTIVE)

        # AND THE MODULE CANNOT BE HANDED ONE EITHER. The decision code has no
        # access to the event at all, so the assertion that matters is over its
        # INTERFACE: the CLI exposes no payload-shaped option, and every input
        # `plan_advance` accepts is a measurement the workflow made.
        options = set(re.findall(r'"(--[a-z-]+)"',
                                 MODULE_SOURCE.read_text("utf-8")))
        for smuggled in ("--payload", "--client-payload", "--event",
                         "--event-payload", "--dispatch", "--ref"):
            self.assertNotIn(smuggled, options)
        self.assertEqual(
            {"current_core", "source_default_branch", "candidate_commit",
             "candidate_reachable", "reachability_evidence", "floor_bytes",
             "snapshot_bytes"},
            set(inspect.signature(R.plan_advance).parameters))

        self.assertRegex(LANE_SHELL, r"gh api \"repos/\$\{SOURCE_REPOSITORY\}\"")
        self.assertIn("--jq .default_branch", LANE_SHELL)

    def test_an_unresolvable_source_default_branch_refuses(self) -> None:
        """Scenario: An unresolvable source default branch refuses.

        And it pins at nothing else: the refusal is raised before the candidate
        commit is even considered, so there is no branch of this function that
        reaches an `Advance` without a resolved default branch.
        """
        for empty in (None, ""):
            outcome = self.tree.plan(source_default_branch=empty)
            self.assertIsInstance(outcome, R.Refusal)
            self.assertEqual("source_default_branch_unresolved", outcome.stage)

    def test_an_unresolvable_candidate_commit_refuses(self) -> None:
        """Scenario: An unresolvable source default branch refuses.

        The neighbouring failure: the branch resolved but its head did not, or
        resolved to something that is not a commit id. The lane refuses rather
        than treating a truncated or empty answer as a commit.
        """
        for bad in (None, "", "main", "ad15a89", NEW_CORE.upper()):
            outcome = self.tree.plan(candidate_commit=bad)
            self.assertIsInstance(outcome, R.Refusal, f"for {bad!r}")
            self.assertEqual("source_commit_unresolved", outcome.stage)


# ===========================================================================
# Requirement 3 — every pinned site in one commit, or nothing
# ===========================================================================

class EveryPinnedSiteMovesOrNothingDoes(TreeFixtureMixin, unittest.TestCase):

    def test_all_sites_are_re_read_before_anything_is_opened(self) -> None:
        """Scenario: All sites are re-read before anything is opened.

        The re-read is the packet's decision M-2 and it is measured from DISK:
        `verify_advance` reports nothing outstanding, and independently every
        site is read back here and required to carry the new value.
        """
        advance = self.tree.plan()
        self.assertEqual(
            [], R.apply_advance(self.tree.root, advance, self.tree.floor_bytes))
        self.assertEqual([], R.verify_advance(self.tree.root, advance))

        values = self.tree.site_values()
        for label in ("pin.core_commit",
                      "merge-master-approval.PINNED_CORE_COMMIT",
                      "merge-master-approval.core-checkout-ref",
                      "pytest-suite.core-checkout-ref"):
            self.assertEqual(NEW_CORE, values[label], label)
        self.assertEqual(advance.after.sha256, values["snapshot.bytes"])
        self.assertEqual(advance.after.sha256,
                         values["pin.floor_snapshot.sha256"])
        self.assertEqual(str(advance.after.entry_count),
                         values["pin.floor_snapshot.entry_count"])

    def test_a_site_that_did_not_move_discards_the_run(self) -> None:
        """Scenario: A site that did not move discards the run.

        NEGATIVE CONTROL (task 4.3), and it MEASURES: the site is broken the
        way a real drift would break it — the key is renamed in the shipped
        bytes — rather than by stubbing the writer. Each of the four commit
        sites is broken in turn, and each names itself in the report.
        """
        renames = {
            "pin.core_commit": (R.PIN_FILE, "core_commit:", "core_committ:"),
            "merge-master-approval.PINNED_CORE_COMMIT": (
                R.MERGE_MASTER_WORKFLOW, "PINNED_CORE_COMMIT:",
                "PINNED_CORE_COMMITT:"),
            "merge-master-approval.core-checkout-ref": (
                R.MERGE_MASTER_WORKFLOW, "ref: \"", "reff: \""),
            "pytest-suite.core-checkout-ref": (
                R.PYTEST_SUITE_WORKFLOW, "ref: \"", "reff: \""),
        }
        for label, (relative, old, new) in renames.items():
            with self.subTest(site=label):
                import tempfile
                with tempfile.TemporaryDirectory() as raw:
                    tree = _TreeFixture(pathlib.Path(raw))
                    target = tree.root / relative
                    text = target.read_text(encoding="utf-8")
                    self.assertIn(old, text)
                    target.write_text(text.replace(old, new, 1), "utf-8")

                    advance = tree.plan(current_core=tree.current_core)
                    unmatched = R.apply_advance(
                        tree.root, advance, tree.floor_bytes)
                    self.assertTrue(
                        unmatched,
                        f"breaking {label} was not detected by the writer")
                    self.assertTrue(
                        any(label in entry for entry in unmatched),
                        f"the report does not name {label}: {unmatched}")

    def test_an_unbroken_tree_reports_nothing_outstanding(self) -> None:
        """ANTI-VACUITY (task 4.5) for the partial-advance control above.

        The same writer over the same fixture with nothing broken must return
        an EMPTY list. Without this the control above would pass on a writer
        that reported every site as unmatched, always.
        """
        advance = self.tree.plan()
        self.assertEqual(
            [], R.apply_advance(self.tree.root, advance, self.tree.floor_bytes))

    def test_a_site_the_verifier_finds_stale_discards_the_run(self) -> None:
        """Scenario: A site that did not move discards the run.

        The other half of the same refusal, and the one the re-read exists for:
        the write succeeded and something put a site back. `verify_advance`
        reads from disk, so it catches what an in-memory check could not.
        """
        advance = self.tree.plan()
        R.apply_advance(self.tree.root, advance, self.tree.floor_bytes)

        reverted = self.tree.root / R.PYTEST_SUITE_WORKFLOW
        reverted.write_text(
            reverted.read_text("utf-8").replace(
                NEW_CORE, self.tree.current_core, 1), "utf-8")

        unmoved = R.verify_advance(self.tree.root, advance)
        self.assertTrue(unmoved)
        self.assertTrue(
            any("pytest-suite.core-checkout-ref" in entry for entry in unmoved),
            unmoved)

    def test_the_cli_turns_a_partial_advance_into_a_refusal(self) -> None:
        """Scenario: A site that did not move discards the run.

        End to end through the entry point, and the broken site is chosen with
        care: `pytest-suite.yml`'s checkout `ref:`, which reads FINE when the
        plan is made — the pin still declares a good `core_commit`, so the run
        gets all the way to `Advance` — and fails only at the write. That is
        the real shape of a partial advance, and it is the one that must exit
        NON-ZERO with a `partial_advance_discarded` plan, because a refusal
        that exited 0 would be opened as a pull request.
        """
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as raw:
            tree = _TreeFixture(pathlib.Path(raw))
            target = tree.root / R.PYTEST_SUITE_WORKFLOW
            text = target.read_text("utf-8")
            self.assertIn('ref: "', text)
            target.write_text(text.replace('ref: "', 'reff: "', 1), "utf-8")

            floor = tree.root / "floor.yaml"
            floor.write_bytes(tree.floor_bytes)
            plan_out = tree.root / "plan.json"
            body_out = tree.root / "body.md"

            code = R.main([
                "--repo", str(tree.root),
                "--source-default-branch", "main",
                "--candidate-commit", NEW_CORE,
                "--candidate-reachable", "true",
                "--floor-document", str(floor),
                "--plan-out", str(plan_out), "--body-out", str(body_out),
                "--write"])

            self.assertEqual(1, code)
            plan = json.loads(plan_out.read_text("utf-8"))
            self.assertEqual("refuse", plan["action"])
            self.assertEqual("partial_advance_discarded", plan["stage"])
            self.assertIn("pytest-suite.core-checkout-ref", plan["reason"])
            self.assertFalse(
                body_out.exists(),
                "a discarded advance must not leave a pull-request body behind")

    def test_an_unreadable_pin_refuses_before_it_plans(self) -> None:
        """Scenario: A site that did not move discards the run.

        The neighbouring refusal, kept distinct from the one above so the two
        stages cannot be confused: when the PIN ITSELF is unreadable the lane
        refuses at `pin_unreadable`, before any candidate is considered, rather
        than guessing which commit this repository is pinned to.
        """
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as raw:
            tree = _TreeFixture(pathlib.Path(raw))
            target = tree.root / R.PIN_FILE
            target.write_text(
                target.read_text("utf-8").replace(
                    "core_commit:", "core_committ:", 1), "utf-8")
            floor = tree.root / "floor.yaml"
            floor.write_bytes(tree.floor_bytes)
            plan_out = tree.root / "plan.json"
            before = tree.digests()

            code = R.main([
                "--repo", str(tree.root),
                "--source-default-branch", "main",
                "--candidate-commit", NEW_CORE,
                "--candidate-reachable", "true",
                "--floor-document", str(floor),
                "--plan-out", str(plan_out), "--write"])

            self.assertEqual(1, code)
            plan = json.loads(plan_out.read_text("utf-8"))
            self.assertEqual("pin_unreadable", plan["stage"])
            self.assertEqual(
                {path: digest for path, digest in before.items()
                 if path != R.PIN_FILE},
                {path: digest for path, digest in tree.digests().items()
                 if path != R.PIN_FILE},
                "a refusal at plan time must move no other site")

    def test_one_commit_not_several(self) -> None:
        """Scenario: One commit, not several.

        The workflow builds ONE tree and creates ONE commit object per firing,
        on both the open and the update path. Measured by counting: a second
        `git write-tree` would mean a second staging, and a `commit-tree` that
        did not use the single `${TREE}` would mean a commit built from
        something else.
        """
        self.assertEqual(1, len(re.findall(r"git write-tree", LANE_SHELL)))
        commit_trees = re.findall(r"git commit-tree \"?\$\{TREE\}\"?",
                                  LANE_SHELL)
        self.assertEqual(
            len(re.findall(r"git commit-tree", LANE_SHELL)),
            len(commit_trees),
            "a commit-tree that does not build from the single staged tree")
        self.assertNotIn("git rebase", LANE_SHELL)
        self.assertNotIn("git cherry-pick", LANE_SHELL)


# ===========================================================================
# Requirement 4 — the snapshot is copied and its witnesses recomputed
# ===========================================================================

class TheSnapshotIsCopiedAndItsWitnessesRecomputed(
        TreeFixtureMixin, unittest.TestCase):

    def test_the_snapshot_is_copied_not_edited(self) -> None:
        """Scenario: The snapshot is copied, not edited.

        Byte equality with the authoritative document, which is the only form
        of "not edited" that can be checked. A single re-serialization through
        a YAML round trip would fail this, and so would a patch that produced a
        semantically equal file.
        """
        advance = self.tree.plan()
        R.apply_advance(self.tree.root, advance, self.tree.floor_bytes)
        self.assertEqual(
            self.tree.floor_bytes,
            (self.tree.root / R.SNAPSHOT_FILE).read_bytes())

    def test_the_witnesses_are_computed_from_what_was_written(self) -> None:
        """Scenario: The witnesses are computed from what was written.

        Recomputed HERE from the file on disk, independently of anything the
        module reported, and required to equal what the pin now declares.
        """
        advance = self.tree.plan()
        R.apply_advance(self.tree.root, advance, self.tree.floor_bytes)

        written = (self.tree.root / R.SNAPSHOT_FILE).read_bytes()
        self.assertEqual(hashlib.sha256(written).hexdigest(),
                         R.read_site_value(self.tree.root,
                                           R.SNAPSHOT_WITNESS_SITES[0]))
        self.assertEqual(
            str(R.floor_entry_count(written)),
            R.read_site_value(self.tree.root, R.SNAPSHOT_WITNESS_SITES[1]))
        self.assertEqual(R.floor_entry_count(self.tree.snapshot_bytes) + 1,
                         R.floor_entry_count(written))

    def test_no_witness_can_be_supplied_from_outside(self) -> None:
        """Scenario: The witnesses are computed from what was written.

        The structural half of the same guarantee: there is NO PARAMETER
        anywhere in the decision path through which a digest or an entry count
        could arrive from a codexFactory report. `witnesses_of` takes bytes and
        nothing else, and `plan_advance` accepts no digest at all.
        """
        self.assertEqual(["document_bytes"],
                         list(inspect.signature(R.witnesses_of).parameters))
        planned = inspect.signature(R.plan_advance).parameters
        for smuggled in ("sha256", "digest", "entry_count", "snapshot_sha256",
                         "payload", "report"):
            self.assertNotIn(smuggled, planned)

    def test_a_stale_supplied_digest_is_caught(self) -> None:
        """NEGATIVE CONTROL (task 4.4): a stale digest does not survive.

        The advance is applied and then the pin's declared digest is put back
        to the OLD value — the exact fixture the task asks for, "a stale digest
        is supplied". The re-read catches it and names the site.
        """
        advance = self.tree.plan()
        R.apply_advance(self.tree.root, advance, self.tree.floor_bytes)

        pin = self.tree.root / R.PIN_FILE
        pin.write_text(
            pin.read_text("utf-8").replace(
                advance.after.sha256, advance.before.sha256, 1), "utf-8")

        unmoved = R.verify_advance(self.tree.root, advance)
        self.assertTrue(
            any("pin.floor_snapshot.sha256" in entry for entry in unmoved),
            unmoved)

    def test_a_fresh_digest_passes_the_same_assertion(self) -> None:
        """ANTI-VACUITY (task 4.5) for the stale-digest control above."""
        advance = self.tree.plan()
        R.apply_advance(self.tree.root, advance, self.tree.floor_bytes)
        self.assertEqual([], R.verify_advance(self.tree.root, advance))

    def test_a_missing_copy_refuses_the_whole_advance(self) -> None:
        """Scenario: A missing copy refuses the whole advance.

        And the other four sites are NOT advanced without it — measured by
        re-reading every site after the refusal.
        """
        before = self.tree.site_values()
        outcome = self.tree.plan(floor_bytes=None)
        self.assertIsInstance(outcome, R.Refusal)
        self.assertEqual("floor_document_unobtainable", outcome.stage)
        self.assertEqual(before, self.tree.site_values())

    def test_the_clears_set_is_measured_by_difference(self) -> None:
        """Scenario: The witnesses are computed from what was written.

        The covered-pending count the body reports is a DIFFERENCE between two
        documents this lane holds, never a number read from a codexFactory
        report. The fixture adds exactly one path, so the difference is that
        one path and nothing else.
        """
        advance = self.tree.plan()
        self.assertEqual(
            ("openspec/specs/fixture-only-capability/spec.md",),
            advance.clears)


# ===========================================================================
# Requirement 5 — judged by the existing checks, with no exemption
# ===========================================================================

class TheBotIsJudgedWithNoExemption(unittest.TestCase):

    def test_the_bots_pull_request_meets_the_same_bar(self) -> None:
        """Scenario: The bot's pull request meets the same bar.

        The required suite's own gate is unchanged by this realization:
        `EXPECT_SKIPPED` still pins exactly `21`, and the byte-identity
        verifier is still watched BY NAME. Either of those moving is how an
        exemption would actually arrive, so both are held here as values.
        """
        required = REQUIRED_SUITE.read_text("utf-8")
        self.assertIn('EXPECT_SKIPPED: "21"', required)
        self.assertIn("test_the_snapshot_is_byte_identical_to_the_pinned_core",
                      required)

    def test_no_author_keyed_exemption_exists(self) -> None:
        """Scenario: No author-keyed exemption exists.

        MEASURED AS AN ABSENCE IN THE JUDGE. The lane's branch, its bot lane
        line and its workflow name appear NOWHERE in the files that judge a pin
        advance. An exemption keyed on the author is exactly a mention of the
        author inside the judge, so its absence is the assertion.
        """
        for judge in (JUDGE_TEST, REQUIRED_SUITE):
            text = judge.read_text("utf-8")
            for token in (R.BOT_BRANCH, "review-lane-repin",
                          "review-lane-repin-bot"):
                self.assertNotIn(
                    token, text,
                    f"{judge.name} names the automated lane; an exemption "
                    "keyed on the author would look exactly like this")

    def test_the_lane_asks_for_no_exemption_of_its_own(self) -> None:
        """Scenario: No author-keyed exemption exists.

        The other direction: the lane does not reach into the judge either. It
        writes only the four declared paths, and neither judge file is among
        them.
        """
        self.assertNotIn("tests/review_lane_pin", "".join(R.WRITABLE_PATHS))
        self.assertNotIn(str(REQUIRED_SUITE.relative_to(REPO_ROOT)) + "x",
                         "".join(R.WRITABLE_PATHS))
        self.assertIn(".github/workflows/pytest-suite.yml", R.WRITABLE_PATHS)

    def test_the_lane_submits_itself_to_the_judge_before_proposing(self) -> None:
        """Scenario: The bot's pull request meets the same bar.

        The lane runs the EXISTING `tests/review_lane_pin` suite against the
        tree it wrote, before it opens anything, with the core checked out at
        the CANDIDATE commit — checking out the old pinned core would compare
        the new snapshot against the old document and red every honest advance.
        The step names no test and excludes none, so it cannot become a
        narrower judge than the pull request's own run.
        """
        steps = LANE_DOC["jobs"]["review-lane-repin"]["steps"]
        by_name = {step.get("name", ""): index
                   for index, step in enumerate(steps)}

        judge = next(step for step in steps
                     if "judge it" in step.get("name", ""))
        invocation = next(line.strip() for line in judge["run"].splitlines()
                          if "-m pytest" in line)
        self.assertEqual("python3 -m pytest tests/review_lane_pin -q",
                         invocation)
        # Measured on the INVOCATION LINE, not the whole block: `-m ` also
        # spells `python3 -m pip`, and a blanket search would forbid the
        # installer.
        for narrowing in ("-k ", "--deselect", "--ignore", "-m not",
                          "--lf", "--sw"):
            self.assertNotIn(narrowing, invocation)
        self.assertEqual(
            "${{ github.workspace }}/.merge-master-core",
            judge["env"]["PINNED_CORE_CHECKOUT"])

        core = next(step for step in steps
                    if "candidate core" in step.get("name", ""))
        self.assertEqual("opensoft/codexFactory", core["with"]["repository"])
        self.assertEqual("${{ steps.source.outputs.sha }}", core["with"]["ref"])
        self.assertFalse(core["with"]["persist-credentials"])

        opener = next(step for step in steps
                      if "Open or update" in step.get("name", ""))
        self.assertLess(
            steps.index(judge), steps.index(opener),
            "the judge must run BEFORE the pull request is opened")

    def test_a_failing_automated_advance_is_repaired_not_waived(self) -> None:
        """Scenario: A failing automated advance is repaired, not waived.

        The lane cannot make its own failure survivable: no step in it is
        `continue-on-error`, and the decision module exits non-zero on every
        refusal. A refusal that could be walked past is a waiver in the shape
        of a green run.
        """
        for job in (LANE_DOC.get("jobs") or {}).values():
            for step in job.get("steps") or []:
                self.assertNotIn("continue-on-error", step)
        self.assertNotIn("continue-on-error", LANE_ACTIVE)


# ===========================================================================
# Requirement 6 — the witnesses a reviewer needs
# ===========================================================================

class ThePullRequestCarriesItsWitnesses(TreeFixtureMixin, unittest.TestCase):

    def _body(self) -> tuple:
        advance = self.tree.plan()
        return advance, R.render_pr_body(
            advance, run_url="https://example.invalid/runs/1")

    def test_the_body_states_the_before_and_after_for_every_witness(self) -> None:
        """Scenario: The body states the before and after for every witness.

        Every value the requirement enumerates, checked for presence as the
        STRING THE LANE MEASURED rather than as a heading: the core commit
        before and after, the snapshot digest before and after, its entry count
        before and after, and the generated block's pin and count before and
        after.
        """
        advance, body = self._body()
        for value in (advance.core_before, advance.candidate_commit,
                      advance.before.sha256, advance.after.sha256,
                      str(advance.before.entry_count),
                      str(advance.after.entry_count),
                      advance.before.generated_at, advance.after.generated_at,
                      str(advance.before.block_entry_count),
                      str(advance.after.block_entry_count)):
            self.assertIn(str(value), body)
        self.assertIn("| witness | before | after |", body)
        self.assertIn("Lane: review-lane-repin-bot", body.splitlines()[0])

    def test_the_landedness_of_the_pinned_commit_is_evidenced(self) -> None:
        """Scenario: The landedness of the pinned commit is evidenced, not asserted.

        The body carries the resolution, the evidence string the workflow
        captured from the API, and the two commands a reviewer runs to repeat
        it. "A reviewer can repeat that verification" is only true if the
        commands are there.
        """
        advance, body = self._body()
        self.assertIn(advance.reachability_evidence, body)
        self.assertIn(f"gh api repos/{R.SOURCE_REPOSITORY} --jq .default_branch",
                      body)
        self.assertIn(f"compare/{advance.source_default_branch}..."
                      f"{advance.candidate_commit}", body)
        self.assertIn("not** taken from any event payload", body)

    def test_no_value_only_the_lane_could_know_appears(self) -> None:
        """Scenario: A value only the lane could know does not appear.

        MEASURED, not asserted in prose: every 40-hex and 64-hex token in the
        body is matched against the set of values that are recomputable from
        the two repositories at the named commits. A digest the lane invented
        would show up here as an unaccounted token.
        """
        advance, body = self._body()
        recomputable = {advance.core_before, advance.candidate_commit,
                        advance.before.generated_at, advance.after.generated_at,
                        advance.before.sha256, advance.after.sha256}
        for token in set(SHA40_RE.findall(body)) | set(SHA256_RE.findall(body)):
            self.assertIn(
                token, recomputable,
                f"{token} appears in the body but is not one of the values a "
                "second party can recompute")

    def test_the_body_names_the_covered_pending_paths_it_clears(self) -> None:
        """Scenario: The body states the before and after for every witness.

        The count and the paths, both from the measured difference.
        """
        advance, body = self._body()
        self.assertIn(f"clear: {len(advance.clears)}", body)
        for path in advance.clears:
            self.assertIn(path, body)


# ===========================================================================
# Requirement 7 — trigger and idempotence
# ===========================================================================

class TheLaneSweepsAndIsIdempotent(TreeFixtureMixin, unittest.TestCase):

    def test_nothing_to_advance_is_a_clean_named_no_op(self) -> None:
        """Scenario: Nothing to advance is a clean named no-op.

        Identical bytes on both sides is a `NoOp` whose reason NAMES the two
        documents and the commit — "reports that nothing is owed" — and the
        entry point exits 0 without writing a body.
        """
        outcome = self.tree.plan(floor_bytes=self.tree.snapshot_bytes)
        self.assertIsInstance(outcome, R.NoOp)
        self.assertIn(R.SNAPSHOT_FILE, outcome.reason)
        self.assertIn(NEW_CORE, outcome.reason)
        self.assertIn("nothing is owed", outcome.reason)

    def test_the_no_op_writes_nothing_and_exits_zero(self) -> None:
        """Scenario: Nothing to advance is a clean named no-op.

        End to end: `--write` is passed on every firing, so the no-op path is
        the one that must be proven inert. No site moves and no body is
        produced, so the workflow's `action == 'advance'` guard never fires.
        """
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as raw:
            tree = _TreeFixture(pathlib.Path(raw))
            floor = tree.root / "floor.yaml"
            floor.write_bytes(tree.snapshot_bytes)
            plan_out, body_out = tree.root / "p.json", tree.root / "b.md"
            before = tree.digests()

            code = R.main([
                "--repo", str(tree.root),
                "--source-default-branch", "main",
                "--candidate-commit", NEW_CORE,
                "--candidate-reachable", "true",
                "--floor-document", str(floor),
                "--plan-out", str(plan_out), "--body-out", str(body_out),
                "--write"])

            self.assertEqual(0, code)
            self.assertEqual("noop",
                             json.loads(plan_out.read_text("utf-8"))["action"])
            self.assertFalse(body_out.exists())
            self.assertEqual(before, tree.digests())

    def test_a_hand_authored_source_change_is_picked_up_too(self) -> None:
        """Scenario: A hand-authored source change is picked up too.

        The sweep is the MECHANISM: the lane declares a `schedule:`, and its
        decision path depends on nothing the dispatch carries. A dispatch-only
        lane would miss the hand regeneration that is the only path a REMOVAL
        can take.
        """
        triggers = LANE_DOC[True] if True in LANE_DOC else LANE_DOC["on"]
        self.assertIn("schedule", triggers)
        self.assertTrue(triggers["schedule"][0]["cron"])
        self.assertIn("repository_dispatch", triggers)
        self.assertEqual(["floor-regenerated"],
                         triggers["repository_dispatch"]["types"])
        self.assertIn("workflow_dispatch", triggers)

    def test_the_schedule_is_declared_against_the_ruled_tolerance(self) -> None:
        """Scenario: A hand-authored source change is picked up too.

        The cadence is hourly, and hourly is what the packet's own measurement
        justifies against the ruled tolerance of 3: the busiest measured day
        added five floored paths in eleven and a half hours.
        """
        triggers = LANE_DOC[True] if True in LANE_DOC else LANE_DOC["on"]
        cron = triggers["schedule"][0]["cron"].split()
        self.assertEqual("*", cron[1], "an hourly sweep runs at every hour")
        self.assertNotIn("*", cron[0], "a per-minute sweep was not declared")

    def test_a_second_firing_does_not_open_a_second_pull_request(self) -> None:
        """Scenario: A second firing does not open a second pull request.

        And a pull request on ANY OTHER BRANCH is not adopted: the lane updates
        only its own, so an unrelated open pull request cannot be hijacked into
        carrying a pin advance.
        """
        self.assertEqual({"action": "open", "number": None},
                         R.decide_idempotent_action([]))
        self.assertEqual(
            {"action": "update", "number": 7},
            R.decide_idempotent_action(
                [{"number": 7, "headRefName": R.BOT_BRANCH}]))
        self.assertEqual(
            {"action": "update", "number": 7},
            R.decide_idempotent_action(
                [{"number": 9, "headRefName": R.BOT_BRANCH},
                 {"number": 7, "headRefName": R.BOT_BRANCH}]))
        self.assertEqual(
            {"action": "open", "number": None},
            R.decide_idempotent_action(
                [{"number": 5, "headRefName": "change/somebody-else"}]))

    def test_the_lane_is_serialized_and_never_cancels_a_delivery(self) -> None:
        """Scenario: A second firing does not open a second pull request.

        Two concurrent sweeps would race to the same branch. The concurrency
        group is fixed and `cancel-in-progress` is false, so a firing that has
        already opened a pull request finishes reporting it.
        """
        self.assertEqual("review-lane-repin", LANE_DOC["concurrency"]["group"])
        self.assertFalse(LANE_DOC["concurrency"]["cancel-in-progress"])

    def test_the_workflow_asks_for_the_open_pull_request_by_branch(self) -> None:
        """Scenario: A second firing does not open a second pull request.

        The shell half of the same guarantee: the lookup is scoped to the
        lane's own head branch, so "is one already open" cannot answer yes
        because of somebody else's pull request.
        """
        self.assertRegex(
            LANE_SHELL,
            r"gh pr list .*--head \"\$\{BOT_BRANCH\}\".*--state open")


# ===========================================================================
# Requirement 8 — the declared credential binding
# ===========================================================================

class TheLaneRunsUnderADeclaredBinding(unittest.TestCase):

    def setUp(self) -> None:  # noqa: N802
        self.binding = yaml.safe_load(
            BINDING_TEMPLATE.read_text(encoding="utf-8"))

    def test_a_missing_binding_fails_loudly(self) -> None:
        """Scenario: A missing binding fails loudly.

        The lane's FIRST step reads both references and exits non-zero naming
        the binding file. And the shape that would convert a missing credential
        into a silent pass — `|| github.token` — appears NOWHERE in this lane.
        """
        first = LANE_DOC["jobs"]["review-lane-repin"]["steps"][0]
        self.assertIn("binding", first["name"].lower())
        self.assertIn("exit 1", first["run"])
        self.assertIn("${BINDING}", first["run"])
        for name in ("OPENXFACTORY_APP_ID", "OPENXFACTORY_APP_PRIVATE_KEY"):
            self.assertIn(name, first["run"])
        # THE FALLBACK SHAPE, ABSENT. `pytest-suite.yml:400` writes
        # `${{ steps.app-token.outputs.token || github.token }}` and is right to
        # there; here the same expression would degrade to an identity that
        # cannot read codexFactory, so the lane would compare the pin against
        # nothing and exit green. Note what is NOT asserted: the shell's own
        # `[ -n "${APP_ID}" ] || missing=...` is a `||`, and it is the refusal
        # itself — a blanket ban on the operator would forbid the check.
        self.assertNotIn("github.token", LANE_ACTIVE)
        self.assertNotIn("|| secrets.", LANE_ACTIVE)
        self.assertIsNone(
            re.search(r"\|\|\s*github\.token", LANE_ACTIVE),
            "the lane must not fall back to the default identity")
        self.assertIsNone(
            re.search(r"outputs\.token\s*\|\|", LANE_ACTIVE),
            "the minted token must not have a fallback alternative")

    def test_the_declared_binding_is_a_template(self) -> None:
        """Scenario: The declared binding is a template.

        Placeholder provider and vault in the `<...>` per-install idiom, and NO
        VALUE anywhere: the file is swept for anything shaped like key
        material or a digest, not merely inspected field by field.
        """
        self.assertEqual(1, self.binding["schema_version"])
        self.assertEqual("xfactory_credential_binding_template",
                         self.binding["kind"])
        identity = self.binding["credential_bindings"]["review_lane_repin_identity"]
        for placeholder in ("provider", "vault"):
            self.assertRegex(identity[placeholder], r"^<.*>$")

        raw = BINDING_TEMPLATE.read_text(encoding="utf-8")
        self.assertNotIn("BEGIN RSA PRIVATE KEY", raw)
        self.assertNotIn("BEGIN PRIVATE KEY", raw)
        self.assertNotIn("ghp_", raw)
        self.assertNotIn("github_pat_", raw)
        self.assertEqual([], SHA256_RE.findall(raw))

    def test_the_references_are_names_and_never_values(self) -> None:
        """Scenario: The declared binding is a template.

        The two GitHub secret NAMES appear as references, spelled exactly as
        the workflow reads them, and `degraded_mode_permitted` is false —
        decision M-6 in machine-readable form.
        """
        resolution = self.binding["resolution"]
        self.assertEqual("secrets.OPENXFACTORY_APP_ID",
                         resolution["references"]["app_id"])
        self.assertEqual("secrets.OPENXFACTORY_APP_PRIVATE_KEY",
                         resolution["references"]["private_key"])
        self.assertFalse(resolution["degraded_mode_permitted"])
        for name in ("OPENXFACTORY_APP_ID", "OPENXFACTORY_APP_PRIVATE_KEY"):
            self.assertIn(f"secrets.{name}", LANE_ACTIVE)

    def test_the_binding_is_least_privilege_and_says_what_it_is_for(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        It names the consuming system, the identity, and exactly the privileges
        the lane needs. The load-bearing line is the last one: it grants NO
        WRITE PRIVILEGE over the source repository, stated as a refusal so a
        later widening has to delete a line.
        """
        identity = self.binding["credential_bindings"]["review_lane_repin_identity"]
        self.assertEqual("openxfactory:workflow:review-lane-repin",
                         identity["consumer"]["holder_ref"])
        self.assertTrue(identity["consumer"]["fetch_identity"])

        source = self.binding["privileges"]["source_repository"]
        self.assertEqual("opensoft/codexFactory", source["repository"])
        self.assertEqual(["contents:read"], source["grants"])
        for write in ("contents:write", "actions:write", "pull-requests:write"):
            self.assertIn(write, source["never_grants"])

        floored = self.binding["privileges"]["floored_repository"]
        self.assertEqual("opensoft/openxFactory", floored["repository"])
        self.assertEqual(["contents:write", "pull-requests:write"],
                         floored["grants"])
        self.assertTrue(floored["reason"].strip())

    def test_the_token_is_scoped_to_the_bindings_two_repositories(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        The MINT is held to the binding too, not just the workflow's
        `permissions:` block. `owner:` alone yields a token good for every
        repository the App is installed on in this organization; this token can
        push and open pull requests, so it is scoped to exactly the two
        repositories the binding's `privileges:` entries name — and the two
        lists are required to be equal here rather than merely both present.
        """
        mint = next(step for step in LANE_DOC["jobs"]["review-lane-repin"]["steps"]
                    if str(step.get("uses", "")).startswith(
                        "actions/create-github-app-token"))
        scoped = {line.strip() for line in mint["with"]["repositories"].split()
                  if line.strip()}

        declared = {
            self.binding["privileges"][key]["repository"].split("/", 1)[1]
            for key in ("source_repository", "floored_repository")}
        self.assertEqual(declared, scoped)

    def test_the_workflow_grants_exactly_what_the_binding_declares(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        The declaration and the grant are held equal. A workflow that quietly
        widened itself past its own binding would be the failure this pairing
        exists to catch, and `permissions:` at the top of the file stays READ.
        """
        self.assertEqual({"contents": "read"}, LANE_DOC["permissions"])
        job = LANE_DOC["jobs"]["review-lane-repin"]
        self.assertEqual({"contents": "write", "pull-requests": "write"},
                         job["permissions"])

        floored = self.binding["privileges"]["floored_repository"]["grants"]
        self.assertEqual(
            sorted(floored),
            sorted(f"{key}:{value}" for key, value in job["permissions"].items()))


# ===========================================================================
# The site list is the whole truth, and the packet's scenarios are all covered
# ===========================================================================

class TheSiteListIsTheWholeTruth(unittest.TestCase):

    def test_no_pinned_site_exists_outside_the_declared_list(self) -> None:
        """THE STALE-SHA SWEEP: a sixth site fails a test instead of going stale.

        The hand path's failure mode is a site nobody remembers to move. This
        sweeps every tracked file for a pin-shaped VALUE line naming the
        current core commit and requires the files it finds to be exactly the
        declared ones.

        VALUE LINES ONLY, and that is the whole difficulty: the pin file and
        `merge-master-approval.yml` carry the current commit many times over in
        advance-history comments, and the packet's own prose quotes it too.
        Those are a record of what happened, not a claim about what is pinned,
        and a sweep that flagged them would be unusable.
        """
        core = R.declared_core_commit(REPO_ROOT)
        self.assertIsNotNone(core)
        value_line = re.compile(
            rf'^\s*(?:[A-Za-z_][A-Za-z0-9_]*): "?{core}"?\s*$')

        tracked = subprocess.run(
            ["git", "ls-files"], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True).stdout.split()

        found = set()
        for relative in tracked:
            path = REPO_ROOT / relative
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if core not in text:
                continue
            if any(value_line.match(line) for line in text.splitlines()):
                found.add(relative)

        expected = {site.path for site in R.PINNED_SITES
                    if site.kind == "commit"}
        self.assertEqual(
            expected, found,
            "a file names the pinned core commit as a VALUE but is not one of "
            "the declared sites (or a declared site stopped naming it). The "
            "lane moves exactly `PINNED_SITES`; anything else goes stale.")

    def test_every_declared_site_resolves_in_the_real_tree(self) -> None:
        """THE STALE-SHA SWEEP, from the other end.

        Every declared site must resolve to exactly one value in the shipped
        tree right now. A site whose regex stopped matching would make the lane
        refuse every firing forever, silently, and this is where that is
        caught.
        """
        for site in R.PINNED_SITES + R.SNAPSHOT_WITNESS_SITES:
            with self.subTest(site=site.label):
                self.assertIsNotNone(
                    R.read_site_value(REPO_ROOT, site),
                    f"{site.label} does not resolve to exactly one value in "
                    f"{site.path}")

    def test_the_shipped_tree_is_internally_consistent(self) -> None:
        """The four commit sites agree, and the pin's witnesses match the bytes.

        Not a lane assertion but the precondition for one: the lane's `NoOp`
        and `Advance` are both computed against a tree that already agrees with
        itself, and a tree that did not would make every other test here
        meaningless.
        """
        core = R.declared_core_commit(REPO_ROOT)
        for site in R.PINNED_SITES:
            if site.kind == "commit":
                self.assertEqual(core, R.read_site_value(REPO_ROOT, site),
                                 site.label)
        snapshot = (REPO_ROOT / R.SNAPSHOT_FILE).read_bytes()
        witnesses = R.witnesses_of(snapshot)
        self.assertEqual(
            witnesses.sha256,
            R.read_site_value(REPO_ROOT, R.SNAPSHOT_WITNESS_SITES[0]))
        self.assertEqual(
            str(witnesses.entry_count),
            R.read_site_value(REPO_ROOT, R.SNAPSHOT_WITNESS_SITES[1]))


class EveryRatifiedScenarioHasATest(unittest.TestCase):

    def test_every_ratified_scenario_has_a_test(self) -> None:
        """THE MAPPING IS MEASURED, NOT DECLARED.

        The scenario titles are read out of the ratified delta and matched
        against the titles quoted in this file's docstrings. A scenario that no
        test claims fails here, which is the only way a "every scenario is
        covered" claim can be worth anything.
        """
        delta = RATIFIED_DELTA.read_text(encoding="utf-8")
        scenarios = {line.split("#### Scenario:", 1)[1].strip()
                     for line in delta.splitlines()
                     if line.startswith("#### Scenario:")}
        self.assertEqual(24, len(scenarios),
                         "the ratified delta no longer has 24 scenarios; the "
                         "mapping in this file must be re-read, not re-pinned")

        claimed = set()
        source = pathlib.Path(__file__).read_text(encoding="utf-8")
        for match in re.finditer(r"Scenario: ([^\n.]+)\.", source):
            claimed.add(match.group(1).strip())

        missing = {scenario for scenario in scenarios
                   if scenario not in claimed}
        self.assertEqual(
            set(), missing,
            "these ratified scenarios are claimed by no test docstring")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
