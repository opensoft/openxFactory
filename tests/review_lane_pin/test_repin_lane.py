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
        # THE SET MOVED ONCE, AND THE REASON IS RECORDED RATHER THAN THE PIN
        # BEING WIDENED QUIETLY. `floor_source_path` was added by M-1 step (1)
        # of `relocate-review-authority-floor-mirror`: during the governed
        # relocation the lane resolves an ORDERED list of candidate paths, and
        # WHICH one answered is a MEASUREMENT THE WORKFLOW MADE — the same class
        # as `candidate_reachable` or `reachability_evidence`, and the exact
        # thing this assertion exists to admit. It is not payload-shaped: it
        # cannot come from an event, it is compared against the module's own
        # declared candidate list, and it changes no decision — only which path
        # the witnesses name. It returns to seven at M-1 step (3), when the list
        # returns to one entry and the parameter has nothing left to say.
        self.assertEqual(
            {"current_core", "source_default_branch", "candidate_commit",
             "candidate_reachable", "reachability_evidence", "floor_bytes",
             "snapshot_bytes", "floor_source_path"},
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

        The two mechanisms that stop an exemption arriving quietly are still in
        place: the skip count is PINNED to an exact integer, and the
        byte-identity verifier is watched BY NAME.

        WHAT IS DELIBERATELY NOT ASSERTED: that the pin equals `21`. The count
        legitimately moves whenever a conditional skip is added or removed
        anywhere in the suite, WITH its reason — the required workflow says so
        itself. Pinning the number here would red an unrelated lane's honest
        pull request and teach everyone to edit this file, which is the
        opposite of a guard. What must not happen is the pin DISAPPEARING or
        the named watch being dropped, and that is what is measured.
        """
        required = REQUIRED_SUITE.read_text("utf-8")
        self.assertRegex(required, r'EXPECT_SKIPPED: "\d+"')
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

        THE WRITABLE SET IS EXACTLY THE PINNED SITES THE PACKET NAMES, AND ONE
        OF THEM IS A JUDGE FILE. That is not an oversight and the earlier
        wording of this test got it wrong: `.github/workflows/pytest-suite.yml`
        IS the required suite, and it IS writable, because it is pinned site 4
        — it carries the core checkout `ref:` that every advance must move.
        Saying "neither judge file is writable" would have been false.

        So the true property, asserted in three parts:

        * the writable set EQUALS the set of paths `PINNED_SITES` names —
          neither wider nor narrower, so a fifth writable path cannot be added
          without this failing;
        * `tests/review_lane_pin/test_floor_snapshot.py` — the judge whose
          assertions decide a pin advance — is ABSENT from it, and so is every
          other test in the repository;
        * and the one judge file that IS writable is reachable at exactly ONE
          line, that line is the checkout `ref:`, and it is not
          `EXPECT_SKIPPED` or any assertion. The lane can move the pin inside
          the judge; it cannot touch what the judge decides.
        """
        writable = set(R.WRITABLE_PATHS)

        # 1. Exactly the pinned sites. Measured as an equality so the set
        #    cannot quietly grow a fifth member.
        self.assertEqual({site.path for site in R.PINNED_SITES}, writable)
        self.assertIn(
            R.PYTEST_SUITE_WORKFLOW, writable,
            "pytest-suite.yml is pinned site 4 and MUST be writable")

        # 2. The judge whose assertions decide an advance is not writable, and
        #    neither is any other test. Named, not inferred.
        self.assertNotIn(str(JUDGE_TEST.relative_to(REPO_ROOT)), writable)
        self.assertNotIn("tests/review_lane_pin/test_floor_snapshot.py",
                         writable)
        self.assertFalse(
            any(path.startswith("tests/") for path in writable),
            f"the lane may not write any test: {sorted(writable)}")

        # 3. Inside the judge file it MAY write, its reach is one line.
        site = next(s for s in R.PINNED_SITES
                    if s.path == R.PYTEST_SUITE_WORKFLOW)
        required = REQUIRED_SUITE.read_text("utf-8")
        self.assertEqual(
            1, len(site.pattern.findall(required)),
            "the lane's pattern must reach exactly one line of the required "
            "workflow")
        line = next(l for l in required.splitlines() if site.pattern.match(l))
        self.assertIn("ref:", line)
        self.assertNotIn("EXPECT_SKIPPED", line)

    def test_the_lane_installs_only_from_the_hashed_lockfile(self) -> None:
        """Scenario: The bot's pull request meets the same bar.

        EVERY `pip install` IN THE LANE IS ENUMERATED and required to be the
        repository's hashed-lockfile form. An unpinned `pip install <name>`
        resolves whatever PyPI serves at run time — no version, no hash — and
        this lane advances the pin that chooses this repository's judge, so an
        unpinned dependency here is a supply-chain path straight into that
        decision.

        Asserted over the shell the runner executes, with comments stripped, so
        the prose above the step cannot satisfy it.
        """
        shell = _active(LANE_SHELL) + "\n" + "\n".join(
            str(step.get("run", ""))
            for job in LANE_DOC["jobs"].values()
            for step in job["steps"]
            if isinstance(step, dict))

        installs = re.findall(r"^\s*(?:python3 -m )?pip install .*$",
                              _active(shell), re.MULTILINE)
        self.assertTrue(installs, "the lane installs nothing at all")
        for install in installs:
            self.assertIn("--require-hashes", install, install)
            self.assertIn("-r requirements/hermes-runtime-contracts.lock",
                          install, install)

        # And the lock genuinely carries what the lane imports and runs, so the
        # single install is not a pin that happens to omit the dependency.
        lock = (REPO_ROOT / "requirements/hermes-runtime-contracts.lock"
                ).read_text(encoding="utf-8")
        for pinned in ("pyyaml==", "pytest=="):
            self.assertIn(pinned, lock.lower())

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
        self.assertEqual("codeXfactory/codexFactory", core["with"]["repository"])
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
        self.assertEqual("codeXfactory/codexFactory", source["repository"])
        self.assertEqual(["contents:read"], source["grants"])
        for write in ("contents:write", "actions:write", "pull-requests:write"):
            self.assertIn(write, source["never_grants"])

        floored = self.binding["privileges"]["floored_repository"]
        self.assertEqual("opensoft/openxFactory", floored["repository"])
        self.assertEqual(["contents:write", "pull-requests:write", "workflows:write"],
                         floored["grants"])
        self.assertTrue(floored["reason"].strip())

    @staticmethod
    def _mints() -> list[dict]:
        return [step for step in LANE_DOC["jobs"]["review-lane-repin"]["steps"]
                if str(step.get("uses", "")).startswith(
                    "actions/create-github-app-token")]

    @staticmethod
    def _requested_grants(mint: dict) -> list[str]:
        """A mint's `permission-<key>: <level>` inputs as the binding spells
        them (`key:level`, hyphenated key)."""
        return sorted(f"{key[len('permission-'):]}:{value}"
                      for key, value in mint["with"].items()
                      if key.startswith("permission-"))

    def test_the_token_is_scoped_to_the_bindings_two_repositories(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        The MINT is held to the binding too, not just the workflow's
        `permissions:` block. `owner:` alone yields a token good for every
        repository the App is installed on in this organization, and ONE token
        over both repositories carries the same permissions over both — which
        would mint `contents: write` over codexFactory, the write the binding
        refuses. So there is one mint per repository the binding's
        `privileges:` entries name, each scoped to exactly that repository, and
        the set of minted repositories equals the set declared.
        """
        mints = self._mints()
        self.assertEqual(2, len(mints), [m.get("name") for m in mints])
        minted = []
        for mint in mints:
            scoped = [line.strip() for line in str(mint["with"]["repositories"]).split()
                      if line.strip()]
            self.assertEqual(1, len(scoped), mint.get("name"))
            minted.extend(scoped)
        declared = {
            self.binding["privileges"][key]["repository"].split("/", 1)[1]
            for key in ("source_repository", "floored_repository")}
        self.assertEqual(declared, set(minted))
        self.assertEqual(len(minted), len(set(minted)))

    def test_each_mint_requests_exactly_its_repository_grants(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        Each token requests EXACTLY the `grants:` the binding declares for the
        one repository it is scoped to — no permission-* input the binding does
        not list, none missing. A mint with no permission-* inputs at all would
        inherit every permission the installation carries (the shape the first
        realization had), so an empty request set is a failure here too.
        """
        by_repo = {
            self.binding["privileges"][key]["repository"].split("/", 1)[1]:
                sorted(self.binding["privileges"][key]["grants"])
            for key in ("source_repository", "floored_repository")}
        for mint in self._mints():
            repo = str(mint["with"]["repositories"]).strip()
            requested = self._requested_grants(mint)
            self.assertTrue(requested, f"{mint.get('name')} requests no permission")
            self.assertEqual(by_repo[repo], requested, mint.get("name"))

    def test_the_workflow_grants_exactly_what_the_binding_declares(self) -> None:
        """Scenario: The binding is least-privilege and says what it is for.

        The declaration and the grant are held together. The `permissions:`
        block at the top of the file stays READ; the job's GITHUB_TOKEN block
        never exceeds the binding's grants for this repository (GITHUB_TOKEN has
        no `workflows` key — the App token, not it, pushes the workflow-file
        sites); and the authoring mint requests the binding's grants exactly.
        """
        self.assertEqual({"contents": "read"}, LANE_DOC["permissions"])
        job = LANE_DOC["jobs"]["review-lane-repin"]
        self.assertEqual({"contents": "write", "pull-requests": "write"},
                         job["permissions"])

        floored = sorted(self.binding["privileges"]["floored_repository"]["grants"])
        job_grants = sorted(f"{key}:{value}" for key, value in job["permissions"].items())
        self.assertTrue(set(job_grants) <= set(floored), (job_grants, floored))

        authoring = next(m for m in self._mints()
                         if str(m["with"]["repositories"]).strip() == "openxFactory")
        self.assertEqual(floored, self._requested_grants(authoring))

    @staticmethod
    def _assert_workflow_file_sites_are_granted(binding: dict, authoring_mint: dict) -> None:
        """THE CHECK, as a function both the positive test and its negative
        control call: if any pinned site lives under `.github/workflows/`, the
        floored grants MUST include `workflows:write` and the authoring mint
        MUST request `permission-workflows: write` — GitHub refuses an App push
        touching a workflow file without it (run 34033398015, 2026-09-06). It
        first proves such a site exists, so a site list that dropped both
        workflow files fails here rather than passing by absence."""
        workflow_sites = [site for site in R.PINNED_SITES
                          if ".github/workflows/" in str(site.path)]
        assert workflow_sites, "no pinned site is a workflow file; the premise is gone"
        floored = binding["privileges"]["floored_repository"]
        assert "workflows:write" in floored["grants"], floored["grants"]
        assert authoring_mint["with"].get("permission-workflows") == "write", \
            authoring_mint["with"]
        # Never on the default branch: the refusal stays beside the grant.
        assert "workflows:write-to-default-branch" in floored["never_grants"]

    def _authoring_mint(self) -> dict:
        return next(m for m in self._mints()
                    if str(m["with"]["repositories"]).strip() == "openxFactory")

    def test_workflow_file_sites_require_the_workflows_grant(self) -> None:
        """MEASURED from the site list, not asserted — see
        `_assert_workflow_file_sites_are_granted`. Runs against the REAL
        binding and the REAL authoring mint."""
        self._assert_workflow_file_sites_are_granted(self.binding, self._authoring_mint())

    def test_negative_control_a_binding_without_the_workflows_grant_is_caught(self) -> None:
        """The same check, run against a copy of the real binding with
        `workflows:write` removed, MUST raise — and again against a copy of the
        real mint without `permission-workflows` — proving it measures the
        grant on each side rather than passing on the shape of the file."""
        import copy
        stripped_binding = copy.deepcopy(self.binding)
        stripped_binding["privileges"]["floored_repository"]["grants"].remove("workflows:write")
        with self.assertRaises(AssertionError):
            self._assert_workflow_file_sites_are_granted(stripped_binding, self._authoring_mint())

        stripped_mint = copy.deepcopy(self._authoring_mint())
        del stripped_mint["with"]["permission-workflows"]
        with self.assertRaises(AssertionError):
            self._assert_workflow_file_sites_are_granted(self.binding, stripped_mint)

        # And the real pair still passes, so the control is about the mutation.
        self._assert_workflow_file_sites_are_granted(self.binding, self._authoring_mint())


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


# ═══════════════════════════════════════════════════════════════════════════
# M-1 STEP (1): DUAL-PATH ACCEPTANCE DURING THE GOVERNED RELOCATION
#
# Realizes `relocate-review-authority-floor-mirror` (ratified 2026-09-08 by
# Brett Heap, verbatim "ratify 293 and 817 when green, then realize them";
# landed as openxFactory #817 -> `c98a0544`). codexFactory is relocating the
# authoritative floor document off every CODEOWNERS prefix
# (`relocate-review-authority-floor`, codexFactory #293 -> `e4e13599`), and a
# two-repository move cannot be atomic: if codexFactory moved first, every
# firing of this lane would refuse `floor_document_unobtainable`.
#
# WHAT THESE CASES PIN, and each is a decision of that packet rather than a
# taste of this author's:
#   M-2  the list is ORDERED and the PATH IN FORCE IS FIRST, which is what makes
#        this realization an observable NO-OP until the document actually moves;
#   M-3  the refusal keeps its identifier and fires only when NO candidate
#        resolved, naming every path tried;
#   M-4  the binding's `source_documents:` is an ADDITIONAL declared site, a
#        RECOMMENDATION with MQ-2 still open — so it is asserted to AGREE when
#        present and asserted to be depended upon by NOTHING;
#   M-6  `contracts/review-lane-pin.yaml` does NOT move in this step;
#   M-7  the lane never SEARCHES beyond the declared list.
# ═══════════════════════════════════════════════════════════════════════════

PIN_FILE = REPO_ROOT / "contracts/review-lane-pin.yaml"

#: The ordered list, restated here as a LITERAL for the same reason the lane and
#: the module each restate it: a value read from the artifact it is used to
#: check makes the check a tautology. This is the fourth independent
#: declaration, and the point of the first test below is that all of them agree.
EXPECTED_CANDIDATES = (
    "scripts/merge_master/openxfactory-review-authority-floor.yaml",
    "floor/openxfactory-review-authority-floor.yaml",
)


def _workflow_candidates() -> tuple[str, ...]:
    """The lane's declared list, read out of the workflow's `env:` block."""
    for job in LANE_DOC["jobs"].values():
        declared = (job.get("env") or {}).get("FLOOR_IN_SOURCE_CANDIDATES")
        if declared:
            return tuple(line.strip() for line in declared.splitlines()
                         if line.strip())
    return ()


def _binding_source_documents() -> tuple[str, ...] | None:
    """The binding's declared read surface, or None when M-4 is not taken."""
    doc = yaml.safe_load(BINDING_TEMPLATE.read_text(encoding="utf-8"))
    declared = ((doc.get("privileges") or {}).get("source_repository") or {}
                ).get("source_documents")
    return None if declared is None else tuple(declared)


def _floor_document(entries: int) -> bytes:
    """The smallest document `floor_entry_count` accepts, with N entries.

    Hand-built rather than copied from the vendored snapshot: these cases are
    about WHICH PATH the bytes came from, not about what the bytes say, and a
    fixture that carried the real floor would go stale on every regeneration.
    """
    paths = "\n".join(f"    - governance/p{i}.yaml" for i in range(entries))
    return (f"schema_version: 1\nkind: repository_gate_floor\n"
            f"floor:\n  id: probe\n  repository: opensoft/openxFactory\n"
            f"  never_clearable_paths:\n{paths}\n").encode("utf-8")


def _fetch_step() -> dict:
    for job in LANE_DOC["jobs"].values():
        for step in job.get("steps", []):
            if step.get("id") == "floor":
                return step
    raise AssertionError("the lane has no `floor` fetch step")


class DualPathAcceptance(unittest.TestCase):
    """The declared candidate list, and the properties the packet ratified."""

    def test_every_declaration_of_the_list_carries_the_same_ordered_list(self):
        """Scenario: The declarations are asserted to agree.

        THE DUPLICATION IS DELIBERATE AND THIS IS WHAT HOLDS IT HONEST. The
        workflow, the module and this test each carry the list as a literal,
        because `scripts/review_lane_repin.py` records that "a value read from
        the artifact it is used to check makes the check a tautology". Nothing
        reads the list from the binding at run time either. So the agreement is
        ASSERTED rather than arranged, and a hand that edits one site and not
        the others reds here instead of shipping a lane whose three declarations
        disagree about where the document lives.
        """
        self.assertEqual(EXPECTED_CANDIDATES, tuple(R.FLOOR_IN_SOURCE_CANDIDATES),
                         "the module's list disagrees with this test's literal")
        self.assertEqual(EXPECTED_CANDIDATES, _workflow_candidates(),
                         "the workflow's list disagrees with the module's")
        binding = _binding_source_documents()
        if binding is not None:
            self.assertEqual(
                EXPECTED_CANDIDATES, binding,
                "the binding declares a read surface that disagrees with the "
                "list the lane actually resolves — M-4 is documentation, and "
                "documentation that lies is worse than none")

    def test_the_two_single_path_declarations_equal_candidate_one(self):
        """Scenario: The declarations are asserted to agree.

        TWO SITES DECLARE ONE PATH RATHER THAN THE LIST, AND CONFLATING THEM
        WITH THE LIST IS THE MISTAKE THIS CASE EXISTS TO STOP.
        `test_floor_snapshot.py`'s `FLOOR_IN_CORE` and the literal in
        `test_review_lane_caller.py` both declare what
        `contracts/review-lane-pin.yaml` NAMES — and M-6 freezes that pin until
        M-1 step (3). Making either carry the successor would land step (3)
        early and point a live pin at a file codexFactory has not created. So
        the assertion that fits them is HEAD-EQUALITY: each must equal candidate
        one, the path in force, and each must NOT yet name the successor.
        """
        for path in (REPO_ROOT / "tests/review_lane_pin/test_floor_snapshot.py",
                     REPO_ROOT / "tests/review_lane_pin/test_review_lane_caller.py"):
            text = path.read_text(encoding="utf-8")
            self.assertIn(
                EXPECTED_CANDIDATES[0], text,
                f"{path.name} no longer declares the path in force; it "
                "declares what the pin names, and the pin does not move until "
                "M-1 step (3)")
            self.assertNotIn(
                EXPECTED_CANDIDATES[1], text,
                f"{path.name} already names the successor path — that is M-1 "
                "step (3) landing early, ahead of the file existing")

    def test_the_path_in_force_is_first_so_this_realization_is_a_no_op(self):
        """Scenario: The first candidate resolves and nothing is different.

        M-2, AND IT IS THE SAFETY ARGUMENT FOR LANDING THIS AHEAD OF ANOTHER
        REPOSITORY'S CHANGE. Until codexFactory actually moves the file,
        candidate one always resolves and the lane behaves exactly as it did
        with a single path. Newest-first would change behaviour on the day this
        landed rather than on the day the document moved, and the ordering is
        therefore load-bearing rather than cosmetic.
        """
        self.assertEqual(
            EXPECTED_CANDIDATES[0], R.FLOOR_IN_SOURCE,
            "the module's single-valued name must still be the path in force")
        self.assertEqual(
            "scripts/merge_master/openxfactory-review-authority-floor.yaml",
            EXPECTED_CANDIDATES[0],
            "candidate one is the path codexFactory has NOT yet moved away "
            "from; if this ever needs editing, that is M-1 step (3) and it is "
            "a separate ratified act")

    def test_the_refusal_names_every_candidate_and_fires_only_when_none_resolve(self):
        """Scenario: A missing copy refuses the whole advance.

        M-3. The identifier does not change, no variant is introduced, and the
        message names the WHOLE set tried — a migration that has gone wrong in
        both directions must read as one refusal rather than as a puzzle about
        which path was meant.
        """
        outcome = R.plan_advance(
            current_core="a" * 40, source_default_branch="main",
            candidate_commit="b" * 40, candidate_reachable=True,
            reachability_evidence="ev", floor_bytes=None,
            snapshot_bytes=b"whatever")
        payload = outcome.as_dict()
        self.assertEqual("refuse", payload["action"])
        self.assertEqual("floor_document_unobtainable", payload["stage"])
        for candidate in EXPECTED_CANDIDATES:
            self.assertIn(candidate, payload["reason"],
                          "the refusal must name every path it tried")

    def test_a_later_candidate_carries_its_own_name_into_every_witness(self):
        """Scenario: A later candidate resolves during a governed relocation.

        The witness a reviewer reads and the path the lane read are ONE value,
        carried on the outcome rather than re-derived where the body is built,
        so they cannot drift apart during the migration window.
        """
        successor = EXPECTED_CANDIDATES[1]
        outcome = R.plan_advance(
            current_core="a" * 40, source_default_branch="main",
            candidate_commit="b" * 40, candidate_reachable=True,
            reachability_evidence="ev", floor_bytes=_floor_document(3),
            snapshot_bytes=_floor_document(2), floor_source_path=successor)
        self.assertEqual("advance", outcome.as_dict()["action"])
        self.assertEqual(successor, outcome.as_dict()["floor_source_path"])
        self.assertEqual(successor, outcome.floor_source_path)

    def test_a_noop_names_the_path_it_actually_read(self):
        """Scenario: The first candidate resolves and nothing is different."""
        same = _floor_document(2)
        outcome = R.plan_advance(
            current_core="a" * 40, source_default_branch="main",
            candidate_commit="b" * 40, candidate_reachable=True,
            reachability_evidence="ev", floor_bytes=same, snapshot_bytes=same,
            floor_source_path=EXPECTED_CANDIDATES[1])
        payload = outcome.as_dict()
        self.assertEqual("noop", payload["action"])
        self.assertIn(EXPECTED_CANDIDATES[1], payload["reason"])

    def test_an_undeclared_obtained_path_is_refused_and_never_echoed(self):
        """The reported path is VALIDATED, not echoed.

        It is written into the witness lines, the pull-request body and the
        repeat commands a reviewer runs, so a mis-wiring would put a path this
        lane never resolves in front of the one person checking it. The refusal
        composes with M-7: the lane never searches beyond the declared list, so
        a path outside it is a WIRING FAULT and not a relocation, and the
        message says so rather than leaving a reader to infer it.
        """
        outcome = R.plan_advance(
            current_core="a" * 40, source_default_branch="main",
            candidate_commit="b" * 40, candidate_reachable=True,
            reachability_evidence="ev", floor_bytes=_floor_document(3),
            snapshot_bytes=_floor_document(2),
            floor_source_path="scripts/merge_master/somewhere-else.yaml")
        payload = outcome.as_dict()
        self.assertEqual("refuse", payload["action"])
        self.assertEqual("floor_source_path_undeclared", payload["stage"])
        self.assertIn("scripts/merge_master/somewhere-else.yaml",
                      payload["reason"],
                      "the refusal must name the value it was handed")
        for candidate in EXPECTED_CANDIDATES:
            self.assertIn(candidate, payload["reason"],
                          "the refusal must name the declared set")
        self.assertIn("wiring fault", payload["reason"])

        # AND IT DOES NOT FIRE ON THE HONEST CASES. A declared path advances,
        # and an ABSENT value falls back to the path in force — the shape the
        # workflow produces when it reports nothing.
        for good in (*EXPECTED_CANDIDATES, None, ""):
            ok = R.plan_advance(
                current_core="a" * 40, source_default_branch="main",
                candidate_commit="b" * 40, candidate_reachable=True,
                reachability_evidence="ev", floor_bytes=_floor_document(3),
                snapshot_bytes=_floor_document(2), floor_source_path=good)
            self.assertEqual("advance", ok.as_dict()["action"],
                             f"a declared or absent value must not refuse: {good!r}")

    def test_the_lane_never_searches_beyond_the_declared_list(self):
        """Scenario: The document is never discovered.

        M-7, AND IT IS A NEGATIVE CONTROL RATHER THAN A READING OF INTENT. A
        discovered file is one an author in the OTHER repository can plant, and
        whatever is found here is byte-copied into this repository's witnessed
        snapshot. So the fetch step is asserted to contain no discovery verb and
        no wildcard, and the module is asserted to name no path outside the
        declared list.
        """
        run = _fetch_step()["run"]
        for forbidden in ("/search/", "search?", "--jq '.tree",
                          "git ls-files", "basename", "find ", "grep -r"):
            self.assertNotIn(
                forbidden, run,
                f"the fetch step performs discovery via {forbidden!r}; the "
                "lane resolves the declared list and refuses, never searches")
        self.assertNotIn(
            "*", run.split("FLOOR_IN_SOURCE_CANDIDATES")[-1],
            "a wildcard in the resolution loop is a search by another name")
        source = MODULE_SOURCE.read_text(encoding="utf-8")
        stray = [line for line in source.splitlines()
                 if "openxfactory-review-authority-floor.yaml" in line
                 and not any(c in line for c in EXPECTED_CANDIDATES)]
        self.assertEqual([], stray,
                         "the module names a floor path outside the declared "
                         "candidate list")

    def test_the_binding_declaration_is_documentation_and_nothing_depends_on_it(self):
        """M-4 is a RECOMMENDATION and MQ-2 is OPEN, so nothing may need it.

        The ratified requirement mandates the declaration in the lane's own
        sources and the run-time prohibition; the binding is an ADDITIONAL site.
        Vetoing M-4 must delete that block and nothing else, so this asserts
        that neither the lane nor the module READS the binding for this list —
        which is also the tautology bar the packet inherited.
        """
        run = _fetch_step()["run"]
        self.assertNotIn("BINDING", run,
                         "the fetch step reads the binding at run time")
        source = MODULE_SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("source_documents", source,
                         "the module reads the binding's declared read surface, "
                         "which makes the agreement check a tautology")
        binding_text = BINDING_TEMPLATE.read_text(encoding="utf-8")
        if "source_documents" in binding_text:
            self.assertIn(
                "MQ-2", binding_text,
                "the block must record that it is a recommendation with an "
                "open question, so a reader does not take it for a mandate")

    def test_the_pin_does_not_move_in_this_step(self):
        """M-6: `contracts/review-lane-pin.yaml` advances at step (3), not here.

        It is a LIVE pin naming exactly ONE path, and it must name a path that
        exists. Advancing it now would point it at a file codexFactory has not
        yet created; that is why the packet sequences it last.
        """
        pin = yaml.safe_load(PIN_FILE.read_text(encoding="utf-8"))
        named = [entry.get("path") for entry in (pin.get("pinned_members") or [])]
        named.append((pin.get("floor_snapshot") or {}).get("of"))
        self.assertIn(
            EXPECTED_CANDIDATES[0], named,
            "the pin must still name the path in force; moving it is M-1 step "
            "(3) and needs the successor to exist first")
        self.assertNotIn(
            EXPECTED_CANDIDATES[1], named,
            "the pin already names the successor path — that is M-1 step (3) "
            "landing early, before codexFactory has created it")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
