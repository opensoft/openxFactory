"""The seven ratified scenarios of `extend-merge-master-envelope-to-floor-bot-lanes`
whose mechanism lives in THIS repository, and a completeness pin over all
seventeen.

RATIFIED 2026-09-07 by Brett Heap, verbatim *"ratify 746 and 272 as recommended
when green, then land them"* — a pair word over openxFactory #746 and
codexFactory #272; record
`openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/review/ratification-2026-09-07.md`.
Realized on the later word *"tick 5.0 in the amendment, then realize 6.3"*
(2026-09-07T19:19Z, recorded on openxFactory #745 and codexFactory #232).

THE SPLIT IS MECHANICAL, NOT A COMMENT TO BE TRUSTED. Decision N-5 puts the
CODE in codexFactory and the RULES here, so most of this packet's scenarios are
measured against codexFactory's envelope, its caller and its regeneration lane.
The ones measured HERE are the ones whose subject is openxFactory's own
mechanism: the never-clearable floor composed OVER the envelope, and the re-pin
lane that writes this repository's judge. `test_every_ratified_scenario_is_
accounted_for` reads BOTH ratified deltas out of the packet, collects the
scenario titles this file's docstrings quote, and requires every remaining
title to appear in `DELEGATED` with the codexFactory module that carries it —
so a scenario cannot go uncovered by nobody noticing, and the delegation cannot
rot into a claim about a file that stopped naming it.

NEGATIVE CONTROLS MEASURE. `mirror-floor-addition-grace`'s archive recorded the
lesson (`ca9fafe6`, "controls must MEASURE the same inputs as the shipped
assertion"), and it binds here: every refusal below is driven through the real
bytes of the real workflow or the real config, and every negative is paired
with a positive that passes the same assertion the negative reds.

NOTHING HERE SKIPS. `.github/workflows/pytest-suite.yml` pins
`EXPECT_SKIPPED: "21"` exactly. This module adds no conditional skip, needs no
network and needs no codexFactory checkout.
"""

from __future__ import annotations

import pathlib
import re
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]

PACKET = (ROOT / "openspec" / "changes"
          / "extend-merge-master-envelope-to-floor-bot-lanes")
DELTAS = (PACKET / "specs" / "roles-authority-model" / "spec.md",
          PACKET / "specs" / "review-lane-floor-mirror" / "spec.md")

ENVELOPE = ROOT / ".github" / "merge-approval-envelope.yml"
APPROVAL = ROOT / ".github" / "workflows" / "merge-master-approval.yml"
REPIN_LANE = ROOT / ".github" / "workflows" / "review-lane-repin.yml"
REPIN_DRIVER = ROOT / "scripts" / "review_lane_repin.py"
PIN = ROOT / "contracts" / "review-lane-pin.yaml"
FLOOR_SNAPSHOT = ROOT / "contracts" / "review-lane-floor-snapshot.yaml"

#: Scenario titles carried by codexFactory, with the module that carries each.
#: Read by the completeness pin below; a title here that this file also claims
#: is a duplicate the pin refuses, and a title in neither is an uncovered
#: scenario the pin refuses.
DELEGATED = {
    "A trusted machine identity outside its enrolled surface":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "Widening the enrolment":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "Withdrawing an enrolment":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "A kill switch outside the diff":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "An approved candidate with no merge mechanism named":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "Admission conditions taken from observed pull requests":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "A shape guarantee the envelope cannot measure":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "The lane writes a path its class does not name":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "An approval is recorded on the artifact":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
    "A park is recorded with the same facts":
        "codexFactory tests/merge-master/test_floor_regeneration_enrolment.py",
}


def _executable(path: pathlib.Path) -> str:
    """A workflow's text with COMMENT LINES REMOVED.

    An assertion about what a lane DOES must read what the lane RUNS: these
    files discuss, at length, the verbs they must never use.
    """
    return "\n".join(line for line in path.read_text(encoding="utf-8").splitlines()
                     if not line.lstrip().startswith("#"))


def _step(doc: dict, fragment: str) -> dict:
    for job in doc["jobs"].values():
        for step in job.get("steps") or []:
            if fragment in str(step.get("name") or ""):
                return step
    raise AssertionError(f"no step named like {fragment!r}")


# ═══ roles-authority-model — the floor composed OVER the envelope ════════════


class TheFloorIsComposedOverTheEnvelope(unittest.TestCase):

    def test_an_enrolled_candidate_touches_the_floor(self) -> None:
        """Scenario: An enrolled candidate touches the floor.

        "WHEN an enrolled candidate satisfies every envelope condition but its
         changed paths include a never-clearable floor member THEN the approval
         parks, naming the floor member it touched AND the envelope's own
         verdict does not override the refusal."

        MEASURED AS AN ORDERING, which is the whole of the requirement. The
        refusal is read out of the caller's executable text and its POSITION is
        asserted: the floor test must precede every approval-shaped step, or
        "composed OVER" would be a comment rather than a control flow.
        """
        text = _executable(APPROVAL)
        self.assertIn('if [ "${FLOOR_MATCHED:-}" != "0" ]; then', text)
        self.assertIn("a never-clearable path is never autonomously approvable, "
                      "whatever the envelope says", text)
        floor_at = text.index('if [ "${FLOOR_MATCHED:-}" != "0" ]; then')
        submit_at = text.index("-f event=APPROVE")
        self.assertLess(floor_at, submit_at,
                        "the floor refusal does not precede the approval; it is "
                        "not composed OVER the envelope")

    def test_the_floor_measurement_is_unavailable(self) -> None:
        """Scenario: The floor measurement is unavailable.

        "WHEN the floor evaluation is skipped, fails, or yields no measured
         count THEN the approval parks as though the floor were touched AND
         absence of a measurement is never read as zero matches."

        THE CONTROL RUNS THE SHIPPED PREDICATE UNDER BASH rather than reasoning
        about `${VAR:-}`. Four values are fed to the literal condition lifted
        from the workflow: the empty string, an unset variable, a non-zero
        count and `0`. Only the last may pass — and it MUST, or the test would
        be satisfied by a predicate that refuses everything.
        """
        import subprocess

        # THE CONDITION IS ONE NAMED LITERAL, ASSERTED AGAINST THE WORKFLOW
        # (Copilot round 1 on #770 asked for this and it is right on
        # legibility, though its premise — that the old form would fail on the
        # correct workflow — was not: `predicate.split(";")[0] + ";"` yielded
        # exactly `if [ "${FLOOR_MATCHED:-}" != "0" ];`, which IS a substring
        # of the shipped `... ]; then`, and the test passed. The objection to
        # keep is that nobody should have to compute that to read it.)
        CONDITION = 'if [ "${FLOOR_MATCHED:-}" != "0" ]; then'
        self.assertIn(CONDITION, _executable(APPROVAL))
        # The local probe is the SHIPPED condition with a reportable body, so
        # the bytes under test are the workflow's own and only the branches are
        # this test's.
        predicate = f'{CONDITION} echo PARK; else echo PASS; fi'

        def answer(assignment: str) -> str:
            script = f"{assignment}\n{predicate}\n"
            return subprocess.run(["bash", "-c", script], capture_output=True,
                                  text=True, check=True).stdout.strip()

        self.assertEqual(answer('FLOOR_MATCHED=""'), "PARK",
                         "an empty measurement was read as zero matches")
        self.assertEqual(answer("unset FLOOR_MATCHED"), "PARK",
                         "an absent measurement was read as zero matches")
        self.assertEqual(answer('FLOOR_MATCHED="1"'), "PARK")
        # ANTI-VACUITY: the only value that passes really does pass.
        self.assertEqual(answer('FLOOR_MATCHED="0"'), "PASS")

    def test_a_ruled_carve_for_one_candidate(self) -> None:
        """Scenario: A ruled carve for one candidate.

        "WHEN an owner admits one named candidate over one named floor member
         THEN the floor member remains declared on the floor AND any other
         candidate touching that member is refused exactly as before."

        NO CARVE WAS RULED — decision N-1 admits the codexFactory regeneration
        lane only, so N-1b stays dormant — and the operative half of the
        requirement is that a carve is never a removal. What is provable today
        is that nothing was removed and nothing was carved: the member is still
        declared, the refusal is still unconditional, and no candidate id
        appears anywhere near it.
        """
        snapshot = FLOOR_SNAPSHOT.read_text(encoding="utf-8")
        self.assertIn("contracts/review-lane-pin.yaml", snapshot,
                      "the never-clearable member whose ground is that a "
                      "clearable pin 'would let a pull request choose its own "
                      "judge' has left the vendored floor snapshot")
        text = _executable(APPROVAL)
        # The refusal names no candidate and admits no exception.
        refusal = text[text.index('if [ "${FLOOR_MATCHED:-}" != "0" ]; then'):]
        refusal = refusal[:refusal.index("fi")]
        for carve_shaped in ("candidate_id", "CANDIDATE", "unless", "except"):
            self.assertNotIn(carve_shaped, refusal,
                             f"the floor refusal is conditioned on "
                             f"{carve_shaped!r}; a carve was authored")


# ═══ roles-authority-model — a lane that writes its own repository's judge ═══


class TheJudgeSelectingLane(unittest.TestCase):

    def test_a_judge_selecting_lane_proposed_for_enrolment(self) -> None:
        """Scenario: A judge-selecting lane proposed for enrolment.

        "WHEN an enrolment is proposed for a lane that writes the artifact
         naming the repository's judge THEN the enrolment records the
         safeguards bounding the values the lane can propose, and the residual
         risk that remains after them AND an enrolment recording no safeguard
         set is refused."

        THE RE-PIN LANE IS NOT ENROLLED, and that is measured first: the
        envelope declares exactly one candidate and it is not this lane. The
        second half — that a proposal for it must record safeguards and the
        residual risk — is measured in the ratified packet, which is where the
        proposal lives: N-1b enumerates five safeguards and states the residual
        risk in its own words rather than arguing it away.
        """
        doc = yaml.safe_load(ENVELOPE.read_text(encoding="utf-8"))
        ids = [c["id"] for c in doc["candidates"]]
        self.assertEqual(ids, ["intent-rolling-custody"],
                         "openxFactory's envelope enrols a class it was not "
                         "granted; the re-pin lane stays on a human word")
        for candidate in doc["candidates"]:
            self.assertNotEqual(candidate.get("expected_head_ref"),
                                "bot/review-lane-repin")
            for admitted in candidate["path_allowlist"]:
                self.assertNotIn("review-lane-pin", admitted)
        design = (PACKET / "design.md").read_text(encoding="utf-8")
        self.assertIn("The residual risk under (ii), stated plainly rather than "
                      "argued away", design)
        for safeguard in ("The lane cannot choose an arbitrary core",
                          "The candidate core judges the candidate",
                          "The five sites move together or nothing opens",
                          "The rules are read from the base branch",
                          "A human can still veto by closing the pull request"):
            self.assertIn(safeguard, design, safeguard)

    def test_the_proposed_judge_is_exercised_on_the_candidate(self) -> None:
        """Scenario: The proposed judge is exercised on the candidate.

        "WHEN such a lane's pull request proposes a new judge THEN the required
         checks that decide the pull request run against the proposed judge,
         not against the superseded one AND those checks are inside the
         conditions the approval quantifies over."

        Measured on the shipped suite: the freshness verifier checks out THE
        PIN THE PULL REQUEST PROPOSES — the head tree's own value — so it is
        the proposed core that judges the candidate, and it runs in
        `pytest-suite`, which `require_all_checks: true` quantifies over.
        """
        suite = ROOT / ".github" / "workflows" / "pytest-suite.yml"
        doc = yaml.safe_load(suite.read_text(encoding="utf-8"))
        step = _step(doc, "Check out the pinned decision core")
        checked_out = str((step.get("with") or {}).get("ref") or "")
        recorded = re.search(r'core_commit: "([0-9a-f]{40})"',
                             PIN.read_text(encoding="utf-8")).group(1)
        self.assertEqual(checked_out, recorded,
                         "the freshness verifier runs against a core other "
                         "than the one this tree pins, so a re-pin pull "
                         "request would be judged by the SUPERSEDED core")
        verifier = (ROOT / "tests" / "review_lane_pin"
                    / "test_floor_snapshot.py").read_text(encoding="utf-8")
        self.assertIn("class TheFreshnessVerifier", verifier)
        # And the all-green condition really does quantify over it.
        envelope = yaml.safe_load(ENVELOPE.read_text(encoding="utf-8"))
        for candidate in envelope["candidates"]:
            self.assertIs(candidate.get("require_all_checks"), True)
            self.assertNotIn("pytest-suite",
                             candidate.get("check_exclusions") or [])


# ═══ review-lane-floor-mirror — the re-pin's ordering ════════════════════════


class TheRePinOrdering(unittest.TestCase):

    def test_the_re_pin_follows_the_regeneration(self) -> None:
        """Scenario: The re-pin follows the regeneration.

        "WHEN the re-pin lane runs THEN it resolves the source repository's
         default branch at run time and proposes that head and no other commit
         AND a commit named by the trigger payload, a tag, a branch or a
         pull-request head is refused."

        DECISION N-3 ADDS NO MECHANISM, so what is asserted is that the
        property already holds STRUCTURALLY. Both halves are measured against
        the lane's executable text: it asks the API for the default branch on
        every firing, and it reads no reference from anywhere else.
        """
        text = _executable(REPIN_LANE)
        self.assertIn('gh api "repos/${SOURCE_REPOSITORY}" --jq .default_branch',
                      text)
        self.assertIn("refuses and pins at no other reference", text)
        # NOT A REFERENCE FROM THE TRIGGER. The payload is never read, and the
        # driver has no `--ref` for one to be handed to.
        for payload_read in ("client_payload", "event.inputs.ref",
                             "github.event.client_payload"):
            self.assertNotIn(payload_read, text, payload_read)
        driver = REPIN_DRIVER.read_text(encoding="utf-8")
        self.assertNotIn('"--ref"', driver)
        self.assertIn("It writes nothing outside the five sites", driver)

    def test_the_regeneration_has_not_landed(self) -> None:
        """Scenario: The regeneration has not landed.

        "WHEN a floor regeneration has been opened in the source repository but
         has not landed on its default branch THEN the re-pin lane proposes the
         unchanged prior core and opens nothing, rather than pinning the
         unlanded commit."

        THE CONTROL IS THE API CALL ITSELF, and it is what makes the scenario
        true rather than hoped for: `.default_branch` names a BRANCH, and the
        lane resolves that branch's head. An unlanded pull-request head is not
        on it, so there is no value the lane could take that names one — and
        with nothing to move, the driver's five-site move is a no-op and it
        opens nothing.
        """
        text = _executable(REPIN_LANE)
        self.assertIn(".default_branch", text)
        # The spellings by which a lane could name an UNLANDED head. `/merge`
        # alone would red on `.merge-master-core` and on
        # `merge-master-approval.yml`, so each pattern names a pull-request
        # reference and nothing else.
        for unlanded in (r"refs/pull", r"/pulls/\d", r"pulls/\$",
                         r"pull_request\.head", r"refs/pull/\d+/merge"):
            self.assertIsNone(re.search(unlanded, text), unlanded)
        # ANTI-VACUITY: the sweep is proven capable of firing.
        self.assertIsNotNone(re.search(r"refs/pull", "refs/pull/9/merge"))
        driver = REPIN_DRIVER.read_text(encoding="utf-8")
        self.assertIn("It moves ALL FIVE SITES or it opens nothing", driver)
        # The pin currently on disk is a 40-hex commit, not a ref name — so the
        # site the lane rewrites cannot hold a branch or a tag.
        #
        # READ AS YAML, NOT SCRAPED (Copilot round 1 on #770). The earlier form
        # fell back to `re.search(...).group(1)`, which raises a bare
        # `AttributeError: 'NoneType' object has no attribute 'group'` if the
        # line is ever unquoted, reformatted or absent — a failure naming
        # neither the file nor the key. `core_commit` is a TOP-LEVEL key of this
        # document (measured: its top-level keys are `schema_version`, `kind`,
        # `repository`, `core_commit`, …), so there is nothing to scrape for.
        pin = yaml.safe_load(PIN.read_text(encoding="utf-8"))
        self.assertIn("core_commit", pin,
                      f"{PIN.name} declares no top-level `core_commit`; the "
                      f"re-pin lane's first site has moved or been renamed, and "
                      f"this test can no longer say what the lane may propose")
        core = str(pin["core_commit"])
        self.assertRegex(
            core, r"^[0-9a-f]{40}$",
            f"{PIN.name}'s `core_commit` is {core!r}, not a 40-hex commit. A "
            f"branch or tag here is exactly the 'choose its own judge' state "
            f"the floor member exists to prevent")


# ═══ the completeness pin ════════════════════════════════════════════════════


class EveryRatifiedScenarioIsAccountedFor(unittest.TestCase):

    def test_every_ratified_scenario_is_accounted_for(self) -> None:
        """Not one of the seventeen may go uncovered by nobody noticing.

        The ratified deltas are read out of the packet; the titles this file's
        docstrings quote are collected; everything left must appear in
        `DELEGATED` naming the codexFactory module that carries it. A scenario
        in neither place fails here, and a scenario in BOTH fails too — a
        duplicate claim hides which file is really the check.
        """
        titles: list[str] = []
        for delta in DELTAS:
            self.assertTrue(delta.is_file(), delta)
            titles += re.findall(r"^#### Scenario: (.+)$",
                                 delta.read_text(encoding="utf-8"),
                                 flags=re.MULTILINE)
        self.assertEqual(len(titles), 17,
                         f"the ratified deltas carry {len(titles)} scenarios, "
                         f"not the 17 the ratification record measured")

        source = pathlib.Path(__file__).read_text(encoding="utf-8")
        claimed = set(re.findall(r"^\s*\"\"\"Scenario: (.+?)\.$", source,
                                 flags=re.MULTILINE))

        uncovered = [t for t in titles
                     if t not in claimed and t not in DELEGATED]
        self.assertEqual(uncovered, [], f"scenarios nobody carries: {uncovered}")
        both = sorted(claimed & set(DELEGATED))
        self.assertEqual(both, [], f"scenarios claimed twice: {both}")
        stale = sorted(set(DELEGATED) - set(titles))
        self.assertEqual(stale, [],
                         f"DELEGATED names scenarios the deltas do not: {stale}")
        stale_claims = sorted(claimed - set(titles))
        self.assertEqual(stale_claims, [],
                         f"docstrings claim scenarios the deltas do not: "
                         f"{stale_claims}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
