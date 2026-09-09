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
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
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

#: THE SECOND RATIFIED DELTA OVER THE SAME CAPABILITY.
#: `amend-mirror-floor-regeneration-merge-authority` (ratified 2026-09-08 by
#: Brett Heap, verbatim "merge 292 when green, then ratify 807"; openxFactory
#: PR #807 -> `6cc06288`) carries ONE `## MODIFIED` block restating requirement
#: 1 in full. Its scenarios are ratified text exactly as the parent's are, so
#: the mapping below reads BOTH files: a mapping that read only the parent
#: would report full coverage while seven ratified scenarios went unmeasured.
AMENDED_DELTA = (
    REPO_ROOT / "openspec/changes/amend-mirror-floor-regeneration-merge-authority"
    / "specs/review-lane-floor-mirror/spec.md")

#: THE ONE ARMING COMMAND THE NARROWED REQUIREMENT ADMITS, SPELLED EXACTLY.
#: The amendment narrowed requirement 1 from "SHALL NOT merge" to "SHALL NOT
#: merge BY ITS OWN ACT" and admitted the lane ARMING THE PLATFORM'S auto-merge
#: on its OWN pull request. Decision M-C fixes the admission BY EQUALITY rather
#: than by a loosened regex — exactly this string, exactly twice, in the
#: workflow only — and M-A/M-B fix the spelling: `--squash` on the lane's own
#: measured precedent (PR #732, one parent), the pull request named by the
#: lane's own head branch so one spelling serves both delivery paths.
ARMING_COMMAND = 'gh pr merge --auto --squash "${BOT_BRANCH}"'

#: EXACTLY HOW MANY TIMES IT MAY APPEAR: once on the `gh pr edit` path and once
#: on the `gh pr create` path. A THIRD occurrence is a second route to the
#: merge, which the requirement forbids in terms, and
#: `test_a_third_arming_occurrence_reds_this_control` is what notices.
ARMINGS_EXPECTED = 2

#: The two of the ten swept spellings the amendment narrows, and NOTHING ELSE.
#: They are narrowed FOR THE WORKFLOW ONLY: the driver keeps all ten, which is
#: the blast-radius bound the packet argued (`design.md` M-C) and which
#: `test_the_driver_names_no_disposal_act_at_all` creates rather than assumes.
NARROWED_FOR_THE_WORKFLOW = ("gh pr merge", "--auto")

#: Every disposal act the lane and its driver are forbidden to name, in the
#: spellings the GitHub CLI, the REST API and the GraphQL API actually use.
DISPOSAL_TERMS = (
    "gh pr merge", "gh pr review", "gh pr close", "--auto", "--admin",
    "enable-auto-merge", "--method PUT", "-X PUT", "/reviews",
    "enablePullRequestAutoMerge",
)

#: The merge endpoint reached through the raw API is still a merge.
RAW_API_MERGE_RE = r"gh api[^\n]*pulls/[^\n]*/merge"

#: The name of the delivery step the arming lives in, per decision M-A ("inside
#: the existing 'Open or update the single automated advance' step").
DELIVERY_STEP_NAME = "Open or update the single automated advance"

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


def _step(name: str) -> dict:
    """The named step of the lane's one job, from the PARSED workflow.

    Read from the parse rather than from the flat text so a second step doing
    the same thing under another credential cannot hide inside a comment or a
    neighbouring block.
    """
    for step in LANE_DOC["jobs"]["review-lane-repin"]["steps"]:
        if isinstance(step, dict) and step.get("name") == name:
            return step
    raise AssertionError(f"the lane has no step named {name!r}")


def _shell_function(source: str, name: str) -> str:
    """The named shell function's DEFINITION, cut out of `source` verbatim.

    THIS IS WHAT MAKES THE EXECUTED TESTS BELOW MEASUREMENTS RATHER THAN
    RE-STATEMENTS. `mirror-floor-addition-grace`'s archive (`ca9fafe6`) taught
    this repository that "controls must MEASURE the same inputs as the shipped
    assertion"; a harness that carried its OWN copy of the witness logic would
    pass forever while the workflow drifted. The bytes executed below are the
    bytes the runner executes, cut out of the workflow at test time.

    A MISSING FUNCTION IS A NAMED FAILURE, NOT A `ValueError`. If the workflow
    is edited so a function this harness executes no longer exists — or its
    closing brace stops sitting at the definition's own indent — the test that
    depends on it must say WHICH function it could not find, or the next reader
    is left decoding a bare substring error from `str.index`.
    """
    marker = f"{name}() {{"
    start = source.find(marker)
    if start < 0:
        raise AssertionError(
            f"the delivery step defines no shell function {name!r}; the "
            "harness executes the workflow's OWN bytes and there are none to "
            "execute")
    line_start = source.rfind("\n", 0, start) + 1
    indent = source[line_start:start]
    end_marker = f"\n{indent}}}\n"
    end = source.find(end_marker, start)
    if end < 0:
        raise AssertionError(
            f"the shell function {name!r} has no closing `}}` at its own "
            f"indent ({len(indent)} spaces); the definition could not be cut "
            "out of the workflow")
    return textwrap.dedent(source[line_start:end + len(end_marker)])


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

    def test_the_lane_opens_a_pull_request_arms_and_stops_there(self) -> None:
        """Scenario: The lane opens a pull request and stops there.

        AS NARROWED 2026-09-08 by
        `amend-mirror-floor-regeneration-merge-authority`: the lane "opens a
        pull request carrying that advance and takes no further action on it
        BEYOND ARMING THE PLATFORM'S AUTO-MERGE on that same pull request AND
        it neither merges BY ITS OWN ACT nor approves that pull request".

        RENAMED WITH THE FLIP, DELIBERATELY. `tasks.md` 3.2 names this case by
        its old name, `test_the_lane_opens_a_pull_request_and_stops_there`, and
        that name stopped describing what it asserts: the lane now takes one
        further act. The SCENARIO title in this docstring is the ratified one
        and is unchanged, which is what the mapping reads.

        MEASURED IN BOTH DIRECTIONS, AND THE NARROWING IS BOUNDED BY EQUALITY.
        The positive: the delivery step really does open (or update) a pull
        request AND really does arm, so the lane is neither inert nor silently
        unchanged. The negative: EIGHT of the ten disposal spellings are still
        refused in the workflow, and the two that are narrowed are admitted
        only inside the one exact arming command — asserted by equality and by
        an occurrence count, so a third `gh pr merge` anywhere reds this test.
        """
        shell = _active(LANE_SHELL)
        self.assertIn("gh pr create", shell)
        self.assertIn("gh pr edit", shell)

        # THE ADMISSION, BY EQUALITY. Exactly two occurrences — one per
        # delivery path — and exactly this spelling, so the arming cannot
        # quietly become a wider command.
        self.assertEqual(
            ARMINGS_EXPECTED, shell.count("gh pr merge"),
            "the lane names `gh pr merge` other than exactly twice; the "
            "amendment admits ONE arming command, once per delivery path")
        self.assertEqual(
            ARMINGS_EXPECTED, shell.count(ARMING_COMMAND),
            "the arming is not the exact admitted spelling, twice: "
            + ARMING_COMMAND)
        # ...and no `gh pr merge` occurrence may lack `--auto`: a bare merge is
        # the act the requirement still forbids by the lane's OWN act.
        for call in re.findall(r"gh pr merge[^\n]*", shell):
            self.assertIn("--auto", call, f"a merge that is not an arming: {call!r}")
        # `--auto` appears ONLY in the arming, so the flag cannot leak onto
        # some other call later.
        self.assertEqual(ARMINGS_EXPECTED, shell.count("--auto"))

        # THE EIGHT THAT ARE STILL REFUSED IN THE WORKFLOW.
        still_refused = tuple(term for term in DISPOSAL_TERMS
                              if term not in NARROWED_FOR_THE_WORKFLOW)
        self.assertEqual(8, len(still_refused))
        for disposing in still_refused:
            self.assertNotIn(
                disposing, shell,
                f"the lane may propose and arm, but never dispose; found "
                f"{disposing!r}")
        self.assertNotRegex(
            shell, RAW_API_MERGE_RE,
            "the merge endpoint reached through the raw API is still a merge")

        # ANTI-VACUITY, both halves: the refused set is proven capable of
        # firing, and so is the narrowed one, so a future edit to either tuple
        # cannot silently turn this case into a no-op.
        self.assertIn(still_refused[0], "gh pr review --approve")
        self.assertIn(NARROWED_FOR_THE_WORKFLOW[0], "gh pr merge --squash")

    def test_an_envelope_approved_fully_green_advance_merges_with_no_human_act(
            self) -> None:
        """Scenario: An envelope-approved, fully green pin advance merges with no human act.

        WHAT IS MEASURABLE HERE IS THAT THE LANE'S LAST ACT IS THE ARMING, and
        that is the whole of what the scenario asks of the LANE — "the lane
        performs no act at merge time, its last act having been the arming".
        The merge itself is the platform's, on a predicate this repository's
        rulesets hold; § 4.1 of the packet is what observes it live, and this
        case is deliberately not a stand-in for that.

        So: the arming lives in the delivery step, it is the LAST command that
        step runs on either path, and no step of the job that comes after it
        touches the pull request at all.
        """
        step = _step(DELIVERY_STEP_NAME)
        run = step["run"]
        self.assertEqual(2, run.count(ARMING_COMMAND))

        # On each path the arming (and the reporting of it) is the last thing
        # done. Measured by position: nothing that names the pull request
        # follows the final `report_the_arming` call.
        after = run[run.rindex("report_the_arming") + len("report_the_arming"):]
        for verb in ("gh pr ", "git push", "gh api"):
            self.assertNotIn(verb, after,
                             f"the lane acts on its pull request after arming: {verb!r}")

        # And no LATER step of the job reaches the pull request either.
        steps = LANE_DOC["jobs"]["review-lane-repin"]["steps"]
        for later in steps[steps.index(step) + 1:]:
            self.assertNotIn("gh pr ", _active(later.get("run") or ""),
                             f"step {later.get('name')!r} acts after the arming")

    def test_a_parked_pin_advance_is_not_merged(self) -> None:
        """Scenario: A parked pin advance is not merged.

        A PARK FIRES NOTHING BECAUSE THE LANE HOLDS NO PREDICATE. The arming is
        `--auto` and only `--auto`: there is no unconditional merge, no
        `--admin`, no raw merge endpoint and no merge queue, so a pull request
        the envelope parks simply stays open exactly as an unarmed one would.

        Measured as the ABSENCE of any second route AND as the absence of any
        branch in the lane that reads a verdict and acts on it: the lane reads
        no review decision, no mergeable state and no check conclusion.
        """
        shell = _active(LANE_SHELL)
        for call in re.findall(r"gh pr merge[^\n]*", shell):
            self.assertIn("--auto", call)
            self.assertNotIn("--admin", call)
        for verdict in ("reviewDecision", "mergeStateStatus", "mergeable",
                        "statusCheckRollup", "--admin", "merge_queue",
                        "merge-queue"):
            self.assertNotIn(
                verdict, shell,
                "the lane reads a disposal verdict and could act on it; the "
                f"platform holds the predicate, not this lane: {verdict!r}")

    def test_a_further_advance_owed_while_armed_updates_and_re_arms(self) -> None:
        """Scenario: A further advance owed while the armed pull request is parked updates it and re-arms.

        THE UPDATE PATH IS DELIVERY, NOT DISPOSAL, and the requirement says so
        in terms: where a further advance is owed while an ARMED pull request
        is open, the lane "SHALL take that same update path and SHALL re-arm
        the platform's auto-merge on that pull request idempotently".

        Measured on the delivery step's two branches, cut out of the shipped
        text: the `gh pr edit` branch updates the ONE open pull request rather
        than opening a second, and it carries an arming of its own that is
        BYTE-IDENTICAL to the open path's — so an armed intent the platform
        dropped is restored, and one it kept is left exactly as it is.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        head, _, tail = run.partition('if [ -n "${OPEN_PR}" ]; then')
        self.assertTrue(tail, "the single-flight update branch is gone")
        update_branch, _, open_branch = tail.partition("\nelse\n")
        self.assertTrue(open_branch, "the open branch is gone")

        self.assertIn("gh pr edit", update_branch)
        self.assertNotIn("gh pr create", update_branch)
        self.assertIn("gh pr create", open_branch)

        self.assertEqual(1, update_branch.count(ARMING_COMMAND),
                         "the update path does not re-arm exactly once")
        self.assertEqual(1, open_branch.count(ARMING_COMMAND),
                         "the open path does not arm exactly once")
        self.assertEqual(0, head.count(ARMING_COMMAND),
                         "an arming runs before either delivery path")

        # IDEMPOTENT MEANS UNCONDITIONAL. The re-arming is not guarded on what
        # the previous state was — the lane never has to reason about whether
        # the platform kept the intent.
        for branch in (update_branch, open_branch):
            arming_line = next(line for line in branch.splitlines()
                               if ARMING_COMMAND in line)
            self.assertNotIn("autoMergeRequest", arming_line)
            self.assertTrue(
                arming_line.strip().startswith("if ARM_OUTPUT="),
                f"the arming is conditioned on something: {arming_line!r}")

    def test_a_head_that_moves_after_an_approval_is_not_merged_on_that_approval(
            self) -> None:
        """Scenario: A head that moves after an approval is not merged on that approval.

        ENFORCED BY PLATFORM RULE, AND THE LANE'S PART IS TO NOT INTERFERE.
        This repository's rulesets carry `dismiss_stale_reviews_on_push: true`
        (18834180) and `require_last_push_approval: true` (18962101), so an
        approval dies when the head moves. What this case measures is the only
        half the lane can get wrong: it MOVES the head on its update path (a
        real push, never a force), and it takes no act that could preserve,
        re-solicit or re-issue an approval across that move.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        self.assertIn("git commit-tree", run)
        self.assertRegex(run, r"git push origin \"\$\{BOT_BRANCH\}\"")
        for forcing in ("--force", "--force-with-lease", " -f "):
            self.assertNotIn(forcing, run)
        shell = _active(LANE_SHELL)
        for solicitation in ("gh pr review", "/reviews", "--approve",
                             "dismissPullRequestReview", "/dismissals",
                             "requested_reviewers", "--add-reviewer"):
            self.assertNotIn(
                solicitation, shell,
                f"the lane touches the approval that binds the head: {solicitation!r}")

    def test_the_lane_never_posts_an_approval_under_any_identity(self) -> None:
        """Scenario: The lane never posts an approval.

        NEGATIVE CONTROL (a) OF `tasks.md` 3.3, AND IT MEASURES: it varies the
        SAME inputs the shipped sweep reads — the workflow's executable shell
        and the driver's source — rather than asserting over a hard-coded set.
        That is the `mirror-floor-addition-grace` lesson (`ca9fafe6`), learned
        in this repository when two controls hard-coded empty sets and so could
        never have failed.

        Every approval and dismissal spelling is checked against BOTH inputs,
        and each is proven capable of firing against a string that contains it
        — one provocation per spelling, so a typo in any single pattern reds
        here instead of passing forever.
        """
        approval_spellings = (
            r"gh\s+pr\s+review",
            r"--approve\b",
            r"createPullRequestReview",
            r"submitPullRequestReview",
            r"/reviews\b",
            r"dismissPullRequestReview",
            r"/dismissals\b",
        )
        shell = _active(LANE_SHELL)
        driver = MODULE_SOURCE.read_text(encoding="utf-8")
        for spelling in approval_spellings:
            self.assertNotRegex(
                shell, spelling,
                f"the lane names an approval or dismissal act: {spelling}")
            self.assertNotRegex(
                driver, spelling,
                f"the driver names an approval or dismissal act: {spelling}")

        provocations = (
            "gh pr review 1 --approve",
            "gh pr merge 1 --approve",
            "mutation { createPullRequestReview }",
            "mutation { submitPullRequestReview }",
            "gh api repos/o/r/pulls/1/reviews",
            "mutation { dismissPullRequestReview }",
            "gh api repos/o/r/pulls/1/reviews/2/dismissals",
        )
        self.assertEqual(len(approval_spellings), len(provocations))
        for spelling, provocation in zip(approval_spellings, provocations):
            self.assertRegex(provocation, spelling, spelling)

    def test_a_third_arming_occurrence_reds_this_control(self) -> None:
        """Scenario: No mechanism can release the arming, and the lane says so.

        NEGATIVE CONTROL (b) OF `tasks.md` 3.3. The requirement forbids "a
        SECOND ROUTE TO THE MERGE"; the two armings are one route stated once
        per delivery path, and a THIRD occurrence of `gh pr merge` anywhere in
        the lane is the shape a second route would take.

        IT MEASURES THE SAME INPUT THE SHIPPED SWEEP READS: the count is taken
        from the workflow's own executable shell, and the control is then
        proven capable of failing by running the identical count over that same
        text with one more arming spliced into it.
        """
        shell = _active(LANE_SHELL)

        def armings(text: str) -> int:
            return text.count("gh pr merge")

        self.assertEqual(ARMINGS_EXPECTED, armings(shell))
        self.assertGreater(
            armings(shell + "\n" + ARMING_COMMAND), ARMINGS_EXPECTED,
            "the counter cannot see a third arming; this control measures "
            "nothing")

    def test_the_driver_names_no_disposal_act_at_all(self) -> None:
        """Scenario: The lane opens a pull request and stops there.

        NEGATIVE CONTROL (c) OF `tasks.md` 3.3, AND IT IS NEW RATHER THAN
        CARRIED. `_shell_text()` reads only the workflow's `run:` blocks, so
        `scripts/review_lane_repin.py` — the module that actually writes the
        five sites — HAS NEVER BEEN SWEPT in this repository. codexFactory's
        twin could call its driver's untouched sweep the blast-radius bound of
        the narrowing; here that bound has to be CREATED before it can be
        claimed, and this is it.

        ALL TEN terms stay refused in the driver, including the two the
        workflow now admits: the driver arms nothing.
        """
        driver = MODULE_SOURCE.read_text(encoding="utf-8")
        self.assertEqual(10, len(DISPOSAL_TERMS))
        for term in DISPOSAL_TERMS:
            self.assertNotIn(
                term, driver,
                f"the driver names a disposal act: {term!r}. The narrowing "
                "moved the WORKFLOW's boundary and nothing else")
        self.assertNotRegex(driver, RAW_API_MERGE_RE)

        # ANTI-VACUITY, one provocation per term, so a typo in any single entry
        # reds here rather than quietly measuring nothing.
        provocations = (
            'subprocess.run(["gh", "pr", "merge"])  # gh pr merge',
            "# gh pr review --approve",
            "# gh pr close 1",
            "# --auto",
            "# --admin",
            "# enable-auto-merge",
            "# --method PUT",
            "# -X PUT",
            "# /reviews",
            "# enablePullRequestAutoMerge",
        )
        self.assertEqual(len(DISPOSAL_TERMS), len(provocations))
        for term, provocation in zip(DISPOSAL_TERMS, provocations):
            self.assertIn(term, provocation, term)

    def test_no_mechanism_can_release_the_arming_and_the_lane_says_so(self) -> None:
        """Scenario: No mechanism can release the arming, and the lane says so.

        TWO HALVES, AND THE SECOND IS THE ONE THAT IS EASY TO SKIP.

        THE LANE SAYS SO: the armed witness carries the inertness clause in
        words — no candidate class admits this lane, so the arming cannot
        complete and the pull request waits for the same human merge word a
        hand-authored advance needs — and it NAMES the successor that will make
        the clause false, so the day it stops being true is the day one lane
        deletes one sentence. Ruled by Brett Heap on 2026-09-09, verbatim
        "rule land inert, this lane realizes it" (openxFactory #745 comment
        5601338925), against `tasks.md` box 1.3.

        THE LANE DOES NOT WIDEN ANYTHING: it names no ruleset, no bypass list,
        no envelope enrolment and no floor removal — the four acts the
        requirement forbids by name in this scenario.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        tail = next(line for line in run.splitlines()
                    if line.strip().startswith("ARMED_TAIL="))
        for clause in ("NO CANDIDATE CLASS ADMITS THIS LANE TODAY",
                       "the arming is inert",
                       "human merge word",
                       "admit-review-lane-repin-to-merge-approval-envelope"):
            self.assertIn(clause, tail,
                          f"the inertness is not declared: {clause!r}")

        shell = _active(LANE_SHELL)
        for widening in ("rulesets", "bypass_actors", "bypass-actors",
                         ".github/merge-approval-envelope", "candidates:",
                         "never_clearable", "SPECS_FLOOR_PATHS"):
            self.assertNotIn(
                widening, shell,
                f"the lane reaches for a widening act: {widening!r}")

    def test_the_arming_is_reported_where_the_run_is_read(self) -> None:
        """Scenario: The arming is reported where the run is read.

        BOTH SURFACES, AND THE FOLLOWING FIRING TOO (decision M-E). The arming
        emits a `::notice` AND a step-summary line naming the pull request and
        the head it armed at, both read from the platform so another party can
        recompute them; and a separate READ-ONLY step says, on the next firing,
        what became of the pull request the last one armed.

        THE REPORTING STEP MUST NEVER START ACTING, so it is swept for every
        disposal term of its own — AND IT IS WHERE THE RESIDUAL IS DISCLOSED
        (Codex P1 on openxFactory #844). An open advance is reported as ARMED
        or as NOT armed, and the NOT-armed branch states the retry condition
        exactly: the arming lives in the DELIVERY step, so the no-op firing
        this step belongs to re-attempts nothing. Re-arming from here would be
        a THIRD occurrence of the arming command, which decision M-C admits by
        EQUALITY at two and a named control reds at three — so the disclosure
        is the act, and the widening is refused.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        self.assertIn("::notice title=review-lane-repin::", run)
        self.assertIn('echo "${witness}" >> "$GITHUB_STEP_SUMMARY"', run)
        for value in ("auto-merge ARMED on #${number} at ${head_oid}",
                      "headRefOid"):
            self.assertIn(value, run)

        outcome = _step("Report what became of the last automated advance")
        outcome_run = _active(outcome["run"])
        self.assertIn("--state all", outcome_run)
        self.assertIn("MERGED at", outcome_run)
        self.assertIn("still OPEN", outcome_run)
        self.assertIn("CLOSED unmerged", outcome_run)

        # THE OPEN CASE IS TWO BRANCHES, and the platform field it splits on is
        # really requested, or the ARMED branch could never be reached.
        self.assertIn("autoMergeRequest", outcome_run)
        self.assertIn("still OPEN with auto-merge ARMED", outcome_run)
        self.assertIn("still OPEN and auto-merge is NOT armed", outcome_run)
        # ...and the NOT-armed branch says exactly WHEN the lane tries again,
        # in the same words the delivery step's refusal witness uses, so a
        # reader is not told two different things by the two surfaces.
        retry_condition = ("re-attempts it only on its next firing that "
                           "delivers an advance")
        self.assertIn(retry_condition, outcome_run)
        self.assertIn("that firing moves the head first", outcome_run)
        # THE DISCLOSURE IS NOT AN ARMING. This step reads; the sweep below is
        # what holds it to that, and it is the reason the residual is disclosed
        # here rather than closed by a third arming.
        for term in DISPOSAL_TERMS:
            self.assertNotIn(
                term, outcome_run,
                f"a step that only READS state names a disposal act: {term!r}")

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
# The arming, EXECUTED rather than read
#
# WHY A SECOND CLASS AND WHY IT RUNS SHELL. Everything above reads the
# workflow's text. "A refused arming is a recorded outcome and never a failed
# advance" and "an unreadable value is SAID rather than left blank" are claims
# about which BRANCH a value reaches and what comes out of it, and a text
# assertion cannot decide either. So the two shell functions the delivery step
# defines are cut out of the shipped workflow and EXECUTED against a stand-in
# `gh`, and the emitted lines are asserted by equality.
#
# THE STAND-IN IS THE ONLY FAKE. The bytes under test are the workflow's own,
# read at test time by `_shell_function`, so a drift between the harness and
# the lane is impossible by construction rather than by discipline.
# ===========================================================================

class TheArmingIsExecutedNotJustRead(unittest.TestCase):

    #: A fabricated head. Not a live sha, deliberately: a fixture that used one
    #: would go stale the day the branch moves.
    HEAD = "b" * 40

    def _execute(self, rc: int, output: str, *,
                 view: str = "", view_fails: bool = False) -> tuple:
        """Run the delivery step's OWN witness functions against a stand-in `gh`.

        Returns `(completed_process, summary_text, gh_call_log)`.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        armed_tail = next(line for line in run.splitlines()
                          if line.strip().startswith("ARMED_TAIL="))
        script = "\n".join((
            "set -uo pipefail",
            armed_tail.strip(),
            _shell_function(run, "command_safe"),
            _shell_function(run, "report_the_arming"),
            'report_the_arming "$1" "$2"',
        ))
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            bin_dir = tmp / "bin"
            bin_dir.mkdir()
            gh = bin_dir / "gh"
            gh.write_text(
                "#!/usr/bin/env bash\n"
                'printf "%s\\n" "$*" >> "$GH_CALL_LOG"\n'
                'if [ -n "${GH_VIEW_FAIL:-}" ]; then exit 1; fi\n'
                'printf "%s\\n" "$GH_VIEW_OUTPUT"\n',
                encoding="utf-8")
            gh.chmod(0o755)
            summary = tmp / "summary.md"
            summary.write_text("", encoding="utf-8")
            log = tmp / "gh.log"
            log.write_text("", encoding="utf-8")
            env = dict(os.environ)
            env.update({
                "PATH": f"{bin_dir}:{env['PATH']}",
                "GITHUB_STEP_SUMMARY": str(summary),
                "GITHUB_REPOSITORY": "opensoft/openxFactory",
                "BOT_BRANCH": R.BOT_BRANCH,
                "GH_CALL_LOG": str(log),
                "GH_VIEW_OUTPUT": view if view else f"732 {self.HEAD}",
            })
            if view_fails:
                env["GH_VIEW_FAIL"] = "1"
            proc = subprocess.run(
                ["bash", "-c", script, "harness", str(rc), output],
                capture_output=True, text=True, env=env)
            return proc, summary.read_text(encoding="utf-8"), log.read_text(
                encoding="utf-8")

    def _notices(self, proc) -> list:
        return [line for line in proc.stdout.splitlines()
                if line.startswith("::notice")]

    @staticmethod
    def _armed_tail() -> str:
        """`ARMED_TAIL`'s VALUE, cut out of the shipped workflow.

        Read rather than restated, for the reason `_shell_function` gives: a
        harness carrying its own copy of the tail would keep passing while the
        lane's wording drifted. Used by the three variant cases below to assert
        HOW the tail is joined, which is the whole of Copilot's finding on
        openxFactory #844.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        line = next(candidate for candidate in run.splitlines()
                    if candidate.strip().startswith("ARMED_TAIL="))
        value = line.strip()[len("ARMED_TAIL="):]
        assert value.startswith('"') and value.endswith('"'), value
        return value[1:-1]

    def _assert_the_tail_is_joined_cleanly(self, summary: str) -> None:
        """The witness reaches `ARMED_TAIL` through " — " and never a full stop.

        COPILOT, openxFactory #844: the tail opens lowercase ("the platform
        merges..."), so a branch that appended it after a period produced a
        sentence starting in lower case. The fix is one join for all three
        variants, and this is where "all three" is measured rather than
        promised: the same assertion runs from the armed, the already-enabled
        and the refused case, against the tail READ FROM THE WORKFLOW.
        """
        tail = self._armed_tail()
        self.assertFalse(tail[:1].isupper(),
                         "the tail no longer opens lowercase; re-read this "
                         "join rather than re-pinning it")
        self.assertTrue(
            summary.strip().endswith(" \u2014 " + tail),
            f"the witness does not reach ARMED_TAIL through an em-dash join: "
            f"{summary!r}")
        self.assertNotIn(". " + tail, summary,
                         "the tail is appended after a full stop and reads as "
                         "a sentence starting in lower case")

    def test_a_successful_arming_names_the_pull_request_and_the_head(self) -> None:
        """Scenario: The arming is reported where the run is read.

        THE VALUES ARE READ FROM THE PLATFORM, AND THE LINE IS ASSERTED BY
        EQUALITY. Both surfaces carry the same sentence, the `gh pr view` that
        supplies the number and the head really is called, and the inertness
        clause is present while it is true.
        """
        proc, summary, log = self._execute(0, "")
        self.assertEqual(0, proc.returncode, proc.stderr)
        expected_prefix = f"auto-merge ARMED on #732 at {self.HEAD} — "
        self.assertEqual(1, len(self._notices(proc)), proc.stdout)
        self.assertTrue(self._notices(proc)[0].startswith(
            "::notice title=review-lane-repin::" + expected_prefix),
            self._notices(proc))
        self.assertTrue(summary.strip().startswith(expected_prefix), summary)
        self.assertIn("NO CANDIDATE CLASS ADMITS THIS LANE TODAY", summary)
        self.assertIn("headRefOid", log)
        self._assert_the_tail_is_joined_cleanly(summary)

    def test_a_refused_arming_is_a_recorded_outcome_not_a_failed_advance(self) -> None:
        """Scenario: A parked pin advance is not merged.

        THE ONE FAILURE MODE THAT WILL ACTUALLY HAPPEN. Community discussion
        #190610 reports that enabling auto-merge returns HTTP 422 until every
        merge requirement is ALREADY met — precisely the state of this lane's
        pull request for as long as no candidate class admits it. The refusal
        must therefore be a REPORTED outcome: the function exits zero, the
        platform's own message is carried verbatim, and the line says the
        advance is delivered and names WHEN the arming is re-attempted.

        THE RETRY CONDITION IS STATED EXACTLY, AND THAT IS A NARROWING OF WHAT
        THIS LINE FIRST SAID (Codex P1 on openxFactory #844). "the lane will
        re-arm on its next firing" promised an hourly retry the lane does not
        perform: the arming lives in the DELIVERY step, gated
        `steps.repin.outputs.action == 'advance'`, so a no-op firing never
        reaches it. What the lane actually does — re-attempt on the next firing
        that DELIVERS an advance, which moves the head first — is what the line
        now says, and the residual is recorded on openxFactory #745 rather than
        closed by widening the arming to a third occurrence M-C forbids.

        PROVEN CAPABLE OF FAILING by the paired positive above: the same
        function on a zero status emits the ARMED line instead.
        """
        message = "GraphQL: Pull request is not in the correct state (422)"
        proc, summary, _ = self._execute(1, message)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn("auto-merge NOT armed on #732", summary)
        self.assertIn(message, summary)
        self.assertIn(
            "re-attempts the arming only on its next firing that delivers an "
            "advance", summary)
        # THE OVER-PROMISE IS REFUSED BY NAME, so restoring it reds here.
        self.assertNotIn("re-arm on its next firing", summary)
        self.assertNotIn("auto-merge ARMED", summary)
        self._assert_the_tail_is_joined_cleanly(summary)

    def test_an_already_armed_pull_request_is_an_idempotent_success(self) -> None:
        """Scenario: A further advance owed while the armed pull request is parked updates it and re-arms.

        RE-ARMING AN ARMED PULL REQUEST MUST NOT READ AS A FAILURE. The
        platform answers "auto-merge is already enabled"; the lane records that
        as ARMED and says which, so a reader is never told the arming was
        refused when the intent is standing.
        """
        proc, summary, _ = self._execute(
            1, "X GitHub Actions: auto-merge is already enabled on this pull request")
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn(f"auto-merge ARMED on #732 at {self.HEAD} (already enabled)",
                      summary)
        self.assertNotIn("NOT armed", summary)
        self._assert_the_tail_is_joined_cleanly(summary)

    def test_an_unreadable_pull_request_is_named_rather_than_left_blank(self) -> None:
        """Scenario: The arming is reported where the run is read.

        WITHOUT THE FALLBACKS a transient `gh pr view` failure emits "ARMED on
        # at " — the witness whose whole purpose is to name the head an
        approval must bind to, naming nothing, silently. The lesson is this
        repository's own: an absent reading is not a value.
        """
        proc, summary, _ = self._execute(0, "", view_fails=True)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn("auto-merge ARMED on #an UNREADABLE number at an "
                      "UNREADABLE head", summary)
        # The control in the other direction: a readable view names neither.
        _, readable, _ = self._execute(0, "")
        self.assertNotIn("UNREADABLE", readable)

    def test_the_notice_payload_cannot_forge_a_workflow_command(self) -> None:
        """Scenario: No mechanism can release the arming, and the lane says so.

        A `::notice` MESSAGE IS A PARSED LINE AND THIS PAYLOAD IS THE
        PLATFORM'S OWN TEXT. GitHub Actions percent-DECODES the message, so a
        refusal carrying the literal characters `%0A` would become a newline in
        the log and whatever followed it would become a SECOND workflow
        command. The escape runs `%` FIRST, or the escapes would themselves be
        re-escaped, and the step SUMMARY — which parses no commands — keeps the
        platform's own bytes.
        """
        forged = "refused%0A::error::forged"
        proc, summary, _ = self._execute(1, forged)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertEqual(1, len(self._notices(proc)), proc.stdout)
        for line in proc.stdout.splitlines():
            self.assertFalse(line.startswith("::error::"),
                             f"the payload forged a workflow command: {line!r}")
        self.assertIn("%250A", proc.stdout)
        self.assertIn(forged, summary)

    def test_the_escaper_encodes_percent_first(self) -> None:
        """Scenario: The arming is reported where the run is read.

        THE ORDER IS THE WHOLE OF THE ESCAPE, and it is not observable through
        the arming step's own inputs today — the refusal branch flattens
        newlines to spaces before the payload ever reaches the escaper — so it
        is measured against the shipped function DIRECTLY rather than left as a
        comment nobody can check. `%` must be substituted FIRST or the escapes
        it writes are themselves re-escaped: a payload carrying a literal
        `%0A` beside a real newline must come out with the literal INERT
        (`%250A`) and the real newline ENCODED (`%0A`), and reversing the two
        lines turns the real newline into visible text instead.
        """
        run = _step(DELIVERY_STEP_NAME)["run"]
        script = "\n".join((
            "set -uo pipefail",
            _shell_function(run, "command_safe"),
            'command_safe "$1"',
        ))
        proc = subprocess.run(
            ["bash", "-c", script, "harness", "a%0Ab\nc"],
            capture_output=True, text=True)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertEqual("a%250Ab%0Ac", proc.stdout)


# ===========================================================================
# The OUTCOME REPORT, executed rather than read
#
# WHY THIS CLASS EXISTS. `Report what became of the last automated advance`
# ends its command substitution with `2>/dev/null || true` and falls back to
# "the last automated pin advance could not be read from the platform on this
# firing" — deliberately, because a step that only reports may never fail an
# advance. The cost of that guard is that a jq program which stopped PARSING
# would degrade in TOTAL SILENCE: every firing would emit the fallback and
# nothing would ever say why. Until this class, nothing measured that program.
#
# RAISED BY A REVIEW FINDING THAT WAS WRONG, AND KEPT BECAUSE THE PLACE IT
# POINTED AT WAS RIGHT. Copilot, on openxFactory #844, read the MERGED
# branch's `\(... // "an unreadable commit")` as an unescaped nested string
# that would stop jq parsing. It does not — a jq interpolation opens an
# expression context in which a string literal is ordinary, and the branch
# renders correctly on both a present and an absent oid, which is what the
# cases below MEASURE rather than argue. But the finding named a real class of
# silent failure that had no control, so the refutation is landed AS one
# instead of being thrown away in a review reply nobody re-reads.
#
# THE BYTES ARE THE SHIPPED ONES, cut out of the workflow at test time by the
# same idiom `_shell_function` uses for the delivery step's shell.
# ===========================================================================

class TheOutcomeReportIsExecutedNotJustRead(unittest.TestCase):

    #: The reporting step, by the name the workflow gives it.
    STEP = "Report what became of the last automated advance"

    @classmethod
    def _program(cls) -> str:
        """The jq program, cut verbatim out of the shipped step.

        A MISSING PROGRAM IS A NAMED FAILURE, for `_shell_function`'s reason:
        if the step is rewritten so there is nothing to cut, the case must say
        so rather than leave the next reader decoding a substring error.
        """
        run = _step(cls.STEP)["run"]
        marker = "| jq -r '"
        start = run.find(marker)
        if start < 0:
            raise AssertionError(
                f"the step {cls.STEP!r} no longer pipes into `jq -r '...'`; "
                "this harness runs the workflow's OWN program and there is "
                "none to cut out")
        start += len(marker)
        end = run.find("' 2>/dev/null", start)
        if end < 0:
            raise AssertionError(
                f"the jq program in {cls.STEP!r} has no closing quote before "
                "`2>/dev/null`; the cut cannot be made")
        return run[start:end]

    def _render(self, listing: str, program: str = None):
        """Run the program over `listing`, as the step pipes it."""
        jq = shutil.which("jq")
        self.assertIsNotNone(
            jq, "jq is not on PATH; the lane's reporting step needs it at run "
                "time and this control needs it to measure that step")
        return subprocess.run(
            [jq, "-r", self._program() if program is None else program],
            input=listing, capture_output=True, text=True)

    def test_every_branch_of_the_outcome_report_parses_and_renders(self) -> None:
        """Scenario: The arming is reported where the run is read.

        SIX FIXTURES, EACH THE SHAPE `gh pr list --json
        number,state,mergeCommit,autoMergeRequest` really returns. A branch
        that stopped parsing, or that rendered the wrong sentence, reds here
        instead of degrading into a fallback nobody reads.
        """
        cases = (
            ("[]",
             "no previous automated pin advance has ever been opened"),
            ('[{"number":732,"state":"MERGED",'
             '"mergeCommit":{"oid":"9ffc6252"},"autoMergeRequest":null}]',
             "#732 MERGED at 9ffc6252"),
            # THE BRANCH THE FINDING NAMED: the nested literal inside the
            # interpolation, reached by an ABSENT oid, which is the only way
            # the `//` fallback fires at all.
            ('[{"number":732,"state":"MERGED","mergeCommit":null,'
             '"autoMergeRequest":null}]',
             "#732 MERGED at an unreadable commit"),
            ('[{"number":733,"state":"OPEN","mergeCommit":null,'
             '"autoMergeRequest":{"enabledAt":"2026-09-09T00:00:00Z"}}]',
             "#733 is still OPEN with auto-merge ARMED"),
            ('[{"number":733,"state":"OPEN","mergeCommit":null,'
             '"autoMergeRequest":null}]',
             "#733 is still OPEN and auto-merge is NOT armed"),
            ('[{"number":734,"state":"CLOSED","mergeCommit":null,'
             '"autoMergeRequest":null}]',
             "#734 was CLOSED unmerged"),
        )
        for listing, expected in cases:
            with self.subTest(expected=expected):
                proc = self._render(listing)
                self.assertEqual(
                    0, proc.returncode,
                    f"jq refused the shipped program: {proc.stderr}")
                self.assertEqual("", proc.stderr)
                self.assertIn(expected, proc.stdout)

    def test_the_not_armed_branch_states_the_retry_condition_when_rendered(
            self) -> None:
        """Scenario: The arming is reported where the run is read.

        THE DISCLOSURE IS ASSERTED ON THE RENDERED LINE, not on the program's
        source, because a reader meets it rendered. This is the residual Codex
        raised as P1 on openxFactory #844: the arming lives in the DELIVERY
        step, gated `steps.repin.outputs.action == 'advance'`, so the no-op
        firing this step belongs to re-attempts nothing — and a re-arm from
        here would be a THIRD occurrence of the arming command, which decision
        M-C admits by EQUALITY at two.
        """
        proc = self._render('[{"number":733,"state":"OPEN",'
                            '"mergeCommit":null,"autoMergeRequest":null}]')
        self.assertEqual(0, proc.returncode, proc.stderr)
        for clause in ("the arming lives in the delivery step",
                       "re-attempts it only on its next firing that delivers "
                       "an advance",
                       "that firing moves the head first"):
            self.assertIn(clause, proc.stdout, clause)
        # AND IT IS STILL ONLY A REPORT: the rendered line names no act.
        for term in DISPOSAL_TERMS:
            self.assertNotIn(term, proc.stdout)

    def test_this_control_can_actually_see_a_parse_failure(self) -> None:
        """ANTI-VACUITY, the `ca9fafe6` lesson applied to a new harness.

        A parse check that cannot observe a parse failure is worth nothing. The
        shipped program is mutated into one jq really does refuse — its final
        `end` removed — and the same runner is required to report that, so the
        cases above are PROVEN capable of firing rather than assumed to be.
        """
        program = self._program().rstrip()
        self.assertTrue(program.endswith("end"), program[-40:])
        broken = self._render("[]", program=program[:-len("end")])
        self.assertNotEqual(
            0, broken.returncode,
            "a program jq should refuse was accepted; this harness cannot see "
            "a parse failure")
        # ...and the control in the other direction: unmutated, it is accepted.
        self.assertEqual(0, self._render("[]").returncode)

    # -- THE READ ITSELF, not just the program it feeds -----------------------
    #
    # A SECOND SILENT FAILURE, ONE LAYER OUT (Copilot on openxFactory #844).
    # The program above can only render what it is given, and the step used to
    # give it `[]` whenever `gh pr list` FAILED — so an expired token or a
    # transient API error rendered "no previous automated pin advance has ever
    # been opened on this branch": a positive claim about the platform, made on
    # a firing that could not read the platform. The cases below execute the
    # step's OWN shell against a `gh` that refuses, so "unreadable" and "none"
    # are told apart by measurement rather than by reading the source.

    #: The sentence the step falls back to when it has no answer.
    UNREADABLE = ("the last automated pin advance could not be read from the "
                  "platform on this firing")

    #: The sentence that is a CLAIM about the platform, and must therefore
    #: never be reached by a firing that failed to read it.
    NONE_EVER = ("no previous automated pin advance has ever been opened on "
                 "this branch")

    def _run_the_step(self, *, listing: str = "[]", gh_fails: bool = False,
                      script: str = None):
        """Execute the shipped reporting step, with `gh` stubbed.

        THE BYTES ARE THE STEP'S OWN, taken from the parsed workflow, for
        `_shell_function`'s reason: a harness carrying its own copy of the
        guard would keep passing while the lane drifted back to coercing a
        failed read into an empty one. Only `gh` is replaced, because a test
        may not call the platform.

        Returns `(proc, summary)`.
        """
        self.assertIsNotNone(
            shutil.which("jq"),
            "jq is not on PATH; the reporting step needs it at run time and "
            "this control needs it to measure that step")
        run = _step(self.STEP)["run"] if script is None else script
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            bin_dir = tmp / "bin"
            bin_dir.mkdir()
            gh = bin_dir / "gh"
            gh.write_text(
                "#!/usr/bin/env bash\n"
                'if [ -n "${GH_LIST_FAIL:-}" ]; then\n'
                '  printf "%s\\n" "gh: HTTP 401 Bad credentials" >&2\n'
                "  exit 1\n"
                "fi\n"
                'printf "%s\\n" "$GH_LIST_OUTPUT"\n',
                encoding="utf-8")
            gh.chmod(0o755)
            summary = tmp / "summary.md"
            summary.write_text("", encoding="utf-8")
            env = dict(os.environ)
            env.update({
                "PATH": f"{bin_dir}:{env['PATH']}",
                "GITHUB_STEP_SUMMARY": str(summary),
                "GITHUB_REPOSITORY": "opensoft/openxFactory",
                "BOT_BRANCH": R.BOT_BRANCH,
                "GH_LIST_OUTPUT": listing,
            })
            if gh_fails:
                env["GH_LIST_FAIL"] = "1"
            proc = subprocess.run(["bash", "-c", run],
                                  capture_output=True, text=True, env=env)
            return proc, summary.read_text(encoding="utf-8")

    def test_a_listing_the_platform_refused_is_reported_unreadable(self) -> None:
        """Scenario: The arming is reported where the run is read.

        THE STEP'S HEADER PROMISES THAT AN UNAVAILABLE LISTING IS REPORTED AS
        UNKNOWN, and until this control nothing held the code to it: the read
        was `|| echo '[]'`, so a refused listing rendered the NONE_EVER
        sentence — the same masking `merge-master-approval.yml`'s gather
        refuses in terms. Measured by running the step's own shell with a `gh`
        that exits non-zero: the outcome must be the unreadable fallback, on
        BOTH surfaces, and must not be the claim.
        """
        proc, summary = self._run_the_step(gh_fails=True)

        # IT STILL NEVER FAILS THE RUN. That is the other half of the header.
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn(self.UNREADABLE, proc.stdout)
        self.assertIn(self.UNREADABLE, summary)
        self.assertNotIn(self.NONE_EVER, proc.stdout)
        self.assertNotIn(self.NONE_EVER, summary)
        # ...and the notice is still one escaped workflow command, not the
        # platform's error body echoed into the log.
        self.assertEqual(
            [f"::notice title=review-lane-repin::{self.UNREADABLE}"],
            self._notice_lines(proc))
        # A STEP THAT ONLY READS NAMES NO DISPOSAL ACT, on this branch either.
        for term in DISPOSAL_TERMS:
            self.assertNotIn(term, proc.stdout)

    def test_a_listing_that_really_is_empty_still_says_so(self) -> None:
        """ANTI-VACUITY, first direction (task 4.5).

        The fix must distinguish the two cases, not collapse both into
        "unreadable". The SAME step, the SAME runner, one input flipped: `gh`
        succeeds and returns a genuinely empty listing, and the claim about the
        platform is then exactly what should be reported.
        """
        proc, summary = self._run_the_step(listing="[]")
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn(self.NONE_EVER, proc.stdout)
        self.assertIn(self.NONE_EVER, summary)
        self.assertNotIn(self.UNREADABLE, proc.stdout)

    def test_a_listing_that_reads_is_rendered_end_to_end(self) -> None:
        """ANTI-VACUITY, second direction, and the whole path at once.

        The cases above could both pass on a step that reported nothing useful
        at all. A real listing is run through the shipped shell — not just the
        cut-out program — so the guard is proven to pass a SUCCESSFUL read
        through to the sentence the platform's answer deserves.
        """
        proc, _ = self._run_the_step(
            listing='[{"number":732,"state":"MERGED",'
                    '"mergeCommit":{"oid":"9ffc6252"},"autoMergeRequest":null}]')
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn("#732 MERGED at 9ffc6252", proc.stdout)
        self.assertNotIn(self.UNREADABLE, proc.stdout)

    def test_this_control_can_actually_see_the_masking_come_back(self) -> None:
        """ANTI-VACUITY for the refusal case, by MUTATION.

        `ca9fafe6` again: a control that cannot observe the defect it names is
        worth nothing. The shipped script is mutated back into the exact shape
        the finding was about — the listing's failure coerced with
        `|| echo '[]'`, which makes the guard's own test succeed on a failed
        read — and the runner is required to report the NONE_EVER claim from a
        `gh` that refused. If a future edit reintroduces the coercion, the case
        above reds; this proves it.
        """
        run = _step(self.STEP)["run"]
        marker = "2>/dev/null)\"; then"
        self.assertIn(
            marker, run,
            "the reporting step no longer guards its listing with `if "
            "LAST=\"$(gh pr list ... )\"; then`; this mutation has nothing to "
            "undo and the refusal case above may be measuring nothing")
        masked = run.replace(marker, "2>/dev/null || echo '[]')\"; then", 1)
        self.assertNotEqual(run, masked)

        proc, summary = self._run_the_step(gh_fails=True, script=masked)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn(
            self.NONE_EVER, proc.stdout,
            "the coerced read did NOT produce the false claim, so the refusal "
            "case above is not measuring the defect it names")
        self.assertNotIn(self.UNREADABLE, summary)

    @staticmethod
    def _notice_lines(proc) -> list:
        return [line for line in proc.stdout.splitlines()
                if line.startswith("::notice")]


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
        # THE SET MOVED TWICE, OUT AND BACK, AND BOTH MOVES ARE RECORDED RATHER
        # THAN THE PIN BEING WIDENED QUIETLY. M-1 step (1) of
        # `relocate-review-authority-floor-mirror` ADDED `floor_source_path`:
        # while the governed relocation had TWO candidate paths declared, WHICH
        # one answered was a measurement the workflow made — the same class as
        # `candidate_reachable`, and the exact thing this assertion exists to
        # admit. M-1 STEP (3) REMOVED IT AGAIN, ON THE PACKET'S OWN TERMS, and
        # the step-(1) comment said it would: the list is back to ONE entry, the
        # workflow's declaration is asserted equal to the module's, so the path
        # obtained is `FLOOR_IN_SOURCE` by construction and the parameter had
        # nothing left to say. THE SET IS SEVEN AGAIN — every one of them a
        # measurement, none of them payload-shaped — and the next governed
        # relocation re-adds the eighth with the entry it belongs to.
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

    @staticmethod
    def _scenarios(delta: pathlib.Path) -> set:
        return {line.split("#### Scenario:", 1)[1].strip()
                for line in delta.read_text(encoding="utf-8").splitlines()
                if line.startswith("#### Scenario:")}

    def test_every_ratified_scenario_has_a_test(self) -> None:
        """THE MAPPING IS MEASURED, NOT DECLARED.

        The scenario titles are read out of the ratified deltas and matched
        against the titles quoted in this file's docstrings. A scenario that no
        test claims fails here, which is the only way a "every scenario is
        covered" claim can be worth anything.

        RE-READ 2026-09-09, NOT RE-PINNED, WHICH IS WHAT THE OLD FAILURE
        MESSAGE ASKED FOR. `amend-mirror-floor-regeneration-merge-authority`
        added a SECOND ratified delta over the same capability — one
        `## MODIFIED` block restating requirement 1 — so this case now reads
        both files. Reading only the parent would have reported full coverage
        while seven newly ratified scenarios went unmeasured, which is exactly
        the failure this case exists to prevent. THE THREE COUNTS ARE STATED
        SEPARATELY so a change to either delta names itself: 24 in the parent,
        10 in the amendment, and 31 DISTINCT titles, because the amendment
        carries three of the parent's titles forward (one with narrowed
        bullets, two verbatim) rather than inventing new ones.
        """
        parent = self._scenarios(RATIFIED_DELTA)
        amended = self._scenarios(AMENDED_DELTA)
        self.assertEqual(24, len(parent),
                         "the parent delta no longer has 24 scenarios; the "
                         "mapping in this file must be re-read, not re-pinned")
        self.assertEqual(10, len(amended),
                         "the amendment's block no longer has 10 scenarios; "
                         "the mapping in this file must be re-read, not "
                         "re-pinned")
        scenarios = parent | amended
        self.assertEqual(31, len(scenarios),
                         "the two ratified deltas no longer carry 31 distinct "
                         "scenarios; re-read the mapping, do not re-pin it")
        self.assertEqual(
            3, len(parent & amended),
            "the amendment no longer carries exactly three of the parent's "
            "titles forward; re-read which, do not adjust this by arithmetic")

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
# M-1 STEP (3): THE MIGRATION WINDOW IS CLOSED AND THE LIST IS ONE ENTRY AGAIN
#
# Realizes `relocate-review-authority-floor-mirror` (ratified 2026-09-08 by
# Brett Heap, verbatim "ratify 293 and 817 when green, then realize them";
# landed as openxFactory #817 -> `c98a0544`). THE THREE STEPS ARE DONE IN ORDER:
# (1) this repository accepted BOTH paths (#823 -> `5c782f29`), observed no-op
# against the old path on run 34303730483; (2) codexFactory moved the document
# off every CODEOWNERS prefix (its #297 -> `8165d1f3`), observed on run
# 34311220954, which obtained it at the successor and reported step (3) as owed;
# (3) is this file's current state — the superseded entry is gone.
#
# WHAT THESE CASES PIN, and each is a decision of that packet rather than a
# taste of this author's:
#   M-2  the list is ORDERED and first-obtained-wins — with one entry the order
#        is trivial, and the ORDERING RULE is what the next window inherits;
#   M-3  the refusal keeps its identifier and fires only when NO candidate
#        resolved, naming every path tried;
#   M-4  the binding's `source_documents:` is an ADDITIONAL declared site, a
#        RECOMMENDATION with MQ-2 still open — so it is asserted to AGREE when
#        present and asserted to be depended upon by NOTHING;
#   M-6  `contracts/review-lane-pin.yaml` names the document AT `core_commit`,
#        which is a DIFFERENT question from where the lane fetches it — see
#        `test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit`,
#        the box the packet expected to tick here and could not;
#   M-7  the lane never SEARCHES beyond the declared list.
# ═══════════════════════════════════════════════════════════════════════════

PIN_FILE = REPO_ROOT / "contracts/review-lane-pin.yaml"

#: The ordered list, restated here as a LITERAL for the same reason the lane and
#: the module each restate it: a value read from the artifact it is used to
#: check makes the check a tautology. This is the fourth independent
#: declaration, and the point of the first test below is that all of them agree.
EXPECTED_CANDIDATES = (
    "floor/openxfactory-review-authority-floor.yaml",
)

#: WHERE THE DOCUMENT LIVED BEFORE THE RELOCATION, and it is still where it
#: lives AT THE PINNED COMMIT. Not a candidate: the lane must never resolve it
#: again, because codexFactory's default branch no longer carries it (measured
#: 2026-09-09: `HTTP 404` at `8165d1f3`). It is here because the PIN still names
#: it, truthfully — see the last test in this class.
FLOOR_BEFORE_RELOCATION = (
    "scripts/merge_master/openxfactory-review-authority-floor.yaml")

#: The `core_commit` this repository is pinned to, which PREDATES codexFactory's
#: relocation. Measured 2026-09-09: the successor path is `HTTP 404` at this
#: commit, and `FLOOR_BEFORE_RELOCATION` resolves there (15456 bytes, sha256
#: `926d536d…abf3c0` — the digest the pin declares). Restated as a literal so
#: the case below can tell "the pin has not advanced yet" from "the pin has
#: advanced and its document path was left behind".
PRE_RELOCATION_CORE = "4b12ba83add713666a94129fc45552d8989f8488"

#: How the two SINGLE-PATH declarations are read back out of the two test files
#: that carry them. Extracted precisely rather than by substring: a comment
#: naming a path is not a declaration, and only the declaration is asserted.
FLOOR_IN_CORE_RE = re.compile(r'^FLOOR_IN_CORE = "([^"]+)"$', re.MULTILINE)
CALLER_LITERAL_RE = re.compile(
    r'assertIn\(\s*"([^"]*openxfactory-review-authority-floor\.yaml)"')


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


class TheDeclaredCandidateList(unittest.TestCase):
    """The declared candidate list, and the properties the packet ratified.

    ONE ENTRY, and the cases below are what keeps it honest at one.
    """

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

    def test_the_list_has_returned_to_one_entry(self):
        """Scenario: The list is returned to one entry.

        M-1 STEP (3), AND IT IS THE REQUIREMENT RATHER THAN TIDYING. Two
        standing homes would mean the lane no longer knows where the document
        lives, and a file reappearing at the abandoned path — by a revert, a bad
        cherry-pick, or an author who did not read the relocation — would be
        byte-copied into this repository's witnessed snapshot. So the window a
        governed relocation opens is CLOSED once one firing has resolved the
        successor, which run 34311220954 (2026-09-09T04:30Z) did.

        The scenario *A later candidate resolves during a governed relocation*
        cannot fire while one entry is declared; the loop, the classification
        and the two-branch witness stay in the lane for the next window, and the
        module's `floor_source_path` parameter went with the entry it served.
        """
        self.assertEqual(
            1, len(R.FLOOR_IN_SOURCE_CANDIDATES),
            "the candidate list is a MIGRATION WINDOW bounded by a named "
            "governed relocation, not a standing choice of homes; a second "
            "entry needs a ratified packet naming the relocation that opened "
            "it")
        self.assertEqual(
            "floor/openxfactory-review-authority-floor.yaml",
            R.FLOOR_IN_SOURCE,
            "the single declared path is the successor codexFactory moved the "
            "document to at its #297 (`8165d1f3`)")
        self.assertEqual(EXPECTED_CANDIDATES[0], R.FLOOR_IN_SOURCE,
                         "the module's single-valued name must be the head of "
                         "its own list")
        self.assertNotIn(
            FLOOR_BEFORE_RELOCATION, R.FLOOR_IN_SOURCE_CANDIDATES,
            "the superseded path must not be resolvable again: codexFactory's "
            "default branch does not carry it, so anything appearing there is "
            "a revert or a plant rather than the authoritative document")

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

    def test_a_noop_names_the_declared_path(self):
        """Scenario: The first candidate resolves and nothing is different.

        WHICH IS WHAT EVERY FIRING SINCE THE RELOCATION HAS DONE: D-3 fixed the
        document's bytes across the move, so the lane reads the successor, finds
        the vendored snapshot byte-identical, and advances nothing. The no-op
        must NAME the path it read, because that name is now the only thing in
        the report that distinguishes a lane reading the relocated document from
        a lane reading a stale one.
        """
        same = _floor_document(2)
        outcome = R.plan_advance(
            current_core="a" * 40, source_default_branch="main",
            candidate_commit="b" * 40, candidate_reachable=True,
            reachability_evidence="ev", floor_bytes=same, snapshot_bytes=same)
        payload = outcome.as_dict()
        self.assertEqual("noop", payload["action"])
        self.assertIn(EXPECTED_CANDIDATES[0], payload["reason"])
        self.assertNotIn(FLOOR_BEFORE_RELOCATION, payload["reason"])

    def test_the_lane_passes_no_option_the_module_does_not_accept(self):
        """THE HALF-REMOVAL IS THE FAILURE MODE THIS CASE EXISTS FOR.

        M-1 step (3) deleted `--floor-source-path` from BOTH the lane and the
        module, and either half left behind would break the lane where nothing
        else looks: an option the parser does not define makes `argparse` exit
        2, so the step fails on every firing — including the hourly sweep no
        human is watching. So the invocation's options are read out of the
        workflow and each is required to exist in the module's parser.
        """
        run = ""
        for job in LANE_DOC["jobs"].values():
            for step in job.get("steps", []):
                if "review_lane_repin.py" in (step.get("run") or ""):
                    run = step["run"]
        self.assertIn("review_lane_repin.py", run,
                      "the lane no longer invokes the decision module")
        passed = set(re.findall(r"(--[a-z-]+)", run.split(
            "review_lane_repin.py", 1)[1]))
        defined = set(re.findall(r'add_argument\("(--[a-z-]+)"',
                                 MODULE_SOURCE.read_text("utf-8")))
        self.assertTrue(passed, "the invocation passes no options at all")
        self.assertEqual(
            set(), passed - defined,
            "the lane passes options the decision module does not define")

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

    def test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit(self):
        """M-6, AND THE ONE BOX M-1 STEP (3) COULD NOT TICK.

        THE PIN AND THE CANDIDATE LIST ANSWER DIFFERENT QUESTIONS, and the
        packet's box 4.2 read them as one. `contracts/review-lane-pin.yaml`
        declares `taken_at: core_commit`: its `floor_snapshot.of` and its
        `pinned_members` entry say where the document lives AT `core_commit`,
        the commit whose decision core judges this repository. The candidate
        list says where the lane FETCHES it, at codexFactory's default-branch
        head. Those were the same path until 2026-09-09 and are not any more.

        MEASURED, NOT ARGUED (2026-09-09, contents API, raw bytes):

          * `floor/…` at `4b12ba83` (this pin) -> **HTTP 404**;
          * `scripts/merge_master/…` at `4b12ba83` -> 15456 bytes, sha256
            `926d536d…abf3c0`, the digest the pin declares;
          * `scripts/merge_master/…` at `8165d1f3` (codexFactory main) -> 404;
          * `floor/…` at `8165d1f3` -> the same 15456 bytes and digest.

        So advancing the pin's document path NOW would make a live pin name a
        path that does not exist at the commit it pins, and would take
        `test_floor_snapshot.py`'s freshness verifier offline with it —
        `locate_pinned_core()` finds the checkout BY that path, so it would
        return None, the verifier would skip, and `pytest-suite`'s named-verdict
        gate would red for a reason that reads like a failed checkout.

        WHY `core_commit` HAS NOT MOVED, and it is not neglect: codexFactory
        D-3 fixed the document's bytes across the relocation, so every firing
        since has been a NO-OP and the lane has had nothing to advance. The pin
        moves at codexFactory's next floor REGENERATION.

        WHAT THIS CASE THEREFORE ASSERTS is the invariant that is true in both
        states and self-clearing at the boundary: while the pin sits at the
        pre-relocation commit, every declaration of the pinned core's copy names
        the path that commit carries; the moment the lane advances `core_commit`
        off it, this case reds until all four move together. That red IS box
        4.2, and it says so in its own message.
        """
        pin = yaml.safe_load(PIN_FILE.read_text(encoding="utf-8"))
        core = pin.get("core_commit")
        expected = (FLOOR_BEFORE_RELOCATION if core == PRE_RELOCATION_CORE
                    else EXPECTED_CANDIDATES[0])

        self.assertEqual(
            expected, (pin.get("floor_snapshot") or {}).get("of"),
            "the pin's `floor_snapshot.of` must name the document as the "
            "PINNED core carries it. If `core_commit` has just advanced past "
            "codexFactory's relocation (`8165d1f3`), this is M-1 step (3) box "
            "4.2 falling due: move `of`, the `pinned_members` entry, "
            "`test_floor_snapshot.py`'s `FLOOR_IN_CORE` and "
            "`test_review_lane_caller.py`'s literal to "
            f"`{EXPECTED_CANDIDATES[0]}` in the same diff")
        named = [entry.get("path") for entry in (pin.get("pinned_members") or [])]
        self.assertIn(
            expected, named,
            "the pin must name the floor document at the commit it pins, so a "
            "re-point ceremony knows what to re-verify")

        for path, pattern in (
                (REPO_ROOT / "tests/review_lane_pin/test_floor_snapshot.py",
                 FLOOR_IN_CORE_RE),
                (REPO_ROOT / "tests/review_lane_pin/test_review_lane_caller.py",
                 CALLER_LITERAL_RE)):
            found = pattern.search(path.read_text(encoding="utf-8"))
            self.assertIsNotNone(
                found, f"{path.name} no longer declares the pinned core's copy "
                       "in the shape this assertion reads")
            self.assertEqual(
                expected, found.group(1),
                f"{path.name} declares the pinned core's copy at a path the "
                "pin does not name. These two files and the pin move TOGETHER "
                "or the freshness verifier is comparing the snapshot against "
                "nothing")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
