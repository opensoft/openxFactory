"""Static validation of openxFactory's Merge Master review lane.

Nothing here executes the workflow. It parses the YAML, checks the embedded
shell with `bash -n`, and asserts the properties this lane's whole value rests
on — that the pinned decision core cannot drift silently, and that the ONE
thing the lane can now approve is exactly the one thing it was granted.

WHAT THIS MODULE USED TO ASSERT, AND WHY IT CHANGED. Until 2026-09-06 it
asserted an ABSENCE: no merge-master App token, no review submission, no
`.github/merge-approval-envelope.yml` at all. THE REASON FOR THAT ABSENCE IS
KEPT HERE RATHER THAN DELETED, because it is still in force for the class it
covers — the Gate-Rules Council convened on 2026-08-28 and REFUSED,
UNANIMOUSLY, the candidate class put to it: a class over `openspec/changes/**`,
refused because its admitted surface lies wholly inside the canonical
GATE_INTEGRITY_FLOOR and so can never convene. A class that can never convene
is not an operable class, so that record defines none, and
`add-substantive-review-lane` task 3.2 — the council's general grant of an
operable candidate class for this repository — STAYS OPEN.

WHAT CHANGED IS A DIFFERENT, NARROWER THING. Act A4 on openxFactory #656
(Brett Heap, 2026-09-06: *"author the envelope PR now as a narrow first
candidate"*) enrolls ONE candidate class, `intent-rolling-custody`, over the
ideation dashboard's own intent and gate-action record trees. His merge word on
that pull request is the grant, for that class and nothing else. So this module
no longer asserts that no approval exists; it asserts that the approval exists
BEHIND EXACTLY ONE DOOR and that the door is this narrow. Specifically:

  * the envelope declares EXACTLY ONE candidate, with that author, that head
    ref, those two path prefixes, and `require_all_checks: true`;
  * the enrolled surface admits no `openspec/` path, so the refused class is
    not smuggled back in under a different name;
  * every approval-shaped step is gated on `steps.envelope.outputs.decision ==
    'approve'`, a value written by nothing but the pinned core's exit code;
  * the workflow's own token still holds NO write scope, so the only write
    authority in the lane is a separately minted, per-repository App token;
  * the lane still cannot merge or enable auto-merge, and that absence is still
    structural.

WHY A TEST IS THE PIN'S TIE HERE. xFactory VENDORS codexFactory as a submodule,
so its `tests/test_review_lane_workflow.py` can assert the workflow's pin equals
the gitlink — the gitlink is the recorded value. openxFactory has no such
gitlink and will not acquire one, so `contracts/review-lane-pin.yaml` is the
recorded value and this module is the tie. Delete this module and the pin
becomes a comment.

NOTHING IS SKIPPED, and that is a design constraint rather than an accident.
A `pytest.skip` reports as a green bar, indistinguishable from a pass to every
reader and every gate — and this repository's CI gate pins the suite's skipped
count EXACTLY, so a skip here is a red gate elsewhere. Every check below either
passes or fails.

TWO TIERS, following `tests/openxwallet_pin/test_verify_pin.py`:
  1. THE REAL FILES, un-fixtured. A fixture proves the mechanism, and the
     mechanism agreeing with itself says nothing about whether the commit in the
     shipped workflow is the commit in the shipped pin.
  2. NEGATIVE CONTROLS over mutated copies, each ONE mutation away from a
     positive, so a check that has quietly stopped checking is visible.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import subprocess
import sys
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CALLER = REPO_ROOT / ".github/workflows/merge-master-approval.yml"
PIN = REPO_ROOT / "contracts/review-lane-pin.yaml"
PIN_CLASS_SOURCE = REPO_ROOT / "scripts/doc_health/pin_class.py"
CODEOWNERS = REPO_ROOT / ".github/CODEOWNERS"

# The check-run name a future ruleset would require, and the substring
# codexFactory's own `.github/merge-approval-envelope.yml` excludes to avoid a
# self-reference deadlock. Restated as a LITERAL rather than read from the file
# under test: asserting the file equals itself would be a tautology.
REQUIRED_JOB_ID = "merge-master-approval"

# The trigger set, stated exactly. `pull_request` is deliberately NOT here: it
# would run this file from the pull-request head with the App credential that
# reads a PRIVATE repository in scope.
EXPECTED_TRIGGERS = {"pull_request_target", "workflow_dispatch"}

# READ-ONLY, stated exactly, and STILL read-only after act A4. `checks` and
# `statuses` were added because the envelope's all-checks-green condition
# quantifies over both listings and a declared `permissions:` block sets every
# undeclared scope to `none`. ANY WRITE SCOPE HERE IS A FAILURE: the approval
# and its comment are written with a separately minted App token, scoped to
# `pull-requests: write` on this repository alone, and nothing else in the job
# can reach it.
EXPECTED_PERMISSIONS = {"contents": "read", "pull-requests": "read",
                        "checks": "read", "statuses": "read"}

ENVELOPE = REPO_ROOT / ".github/merge-approval-envelope.yml"

# THE GRANT, RESTATED AS LITERALS. Read from this module rather than from the
# file under test: asserting the file equals itself would be a tautology, and
# the whole point of a narrow grant is that widening it must break a test
# somebody has to justify changing.
ENROLLED_CANDIDATE_ID = "intent-rolling-custody"
ENROLLED_AUTHOR = "openxfactory[bot]"
ENROLLED_HEAD_REF = "intents/rolling"
ENROLLED_BASE_REF = "main"
ENROLLED_PATHS = ["ideation/dashboard/intents/**",
                  "ideation/dashboard/gate-records/**"]

# THE ONE DOOR. The literal `if:` fragment every approval-shaped step must
# carry. `steps.envelope.outputs.decision` is written by nothing but the pinned
# core's exit code, through the guarded emitter in the envelope step.
APPROVAL_GATE = "steps.envelope.outputs.decision == 'approve'"
ENVELOPE_DECISION = "steps.envelope.outputs.decision"

# A step SUBMITS A REVIEW when its shell carries both of these. Two markers, not
# one, so a step that merely READS the reviews listing (the idempotence check
# does exactly that) is not mistaken for one that writes.
REVIEW_SUBMISSION_MARKERS = ("/reviews", "event=APPROVE")

# The merge-master credential, in every EXPRESSION that reaches the approver
# identity. Every step wiring one of these into its `with:` or `env:` must be
# gated on the envelope decision.
#
# Matched over `with`/`env` only, never over `run` prose: the envelope step's
# job summary NAMES `MERGE_MASTER_APP_ID` when the App is unconfigured, so it
# can tell an operator what to grant, and a check that could not tell an
# explanation from a use would have to be weakened until it caught neither.
APPROVER_CREDENTIAL = ("secrets.MERGE_MASTER_APP_KEY",
                       "secrets.MERGE_MASTER_APP_ID",
                       "vars.MERGE_MASTER_APP_ID",
                       "steps.mm-token.outputs.token")

PINNED_REPOSITORY = "opensoft/codexFactory"
FLOOR_REPOSITORY = "opensoft/openxFactory"

SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
CORE_COMMIT_RE = re.compile(
    r'^core_commit:[ \t]*"?([0-9a-f]{40})"?[ \t]*$', re.MULTILINE)

# THE MERGE DENYLIST. Act A4 granted this lane the authority to APPROVE one
# candidate class. It granted nothing about LANDING one, and the aggregation's
# own intent-apply lane already arms GitHub's auto-merge on its side (ruling
# D-3 on #656), so a merge call here would be a second, ungranted authority
# over the same pull request. The absence is STRUCTURAL — these steps are
# absent, not disabled by a condition, and a condition is exactly what a later
# edit would reach for first — so the check is over the file TEXT rather than
# over the parsed graph.
#
# Every string is chosen to be unreachable from PROSE: the file's comments say
# "auto-merge" and "no merge call" repeatedly, and a denylist that tripped on
# its own explanation would have to be weakened until it caught nothing.
MERGE_SHAPED = (
    "gh pr merge",
    "enablePullRequestAutoMerge",
    "--auto ",
    "/auto-merge",
    "merge_method",
    "gh pr review",
)


def _load_pin_class():
    """Load `scripts/doc_health/pin_class.py` by path.

    By path, under a private module name, rather than by adding
    `<repo>/scripts` to `sys.path`: the doc-health subtree's own conftest does
    that insert for its own directory, and duplicating it from a second
    directory makes this module's behaviour depend on collection order. The
    module is stdlib-only and side-effect-free at import, so a regression in
    that surfaces here as a collection error, which is the right place for it.
    """
    name = "_review_lane_pin_class_probe"
    spec = importlib.util.spec_from_file_location(name, PIN_CLASS_SOURCE)
    module = importlib.util.module_from_spec(spec)
    # REGISTERED BEFORE EXEC, and not as a convenience: `@dataclass` resolves a
    # field's annotation through `sys.modules[cls.__module__].__dict__`, so an
    # unregistered module raises `AttributeError: 'NoneType' object has no
    # attribute '__dict__'` on its first dataclass. Measured, not anticipated.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def caller_document(text: str) -> dict:
    """Parse a caller workflow, normalizing YAML 1.1's `on` -> True.

    PyYAML resolves the bare key `on` to the BOOLEAN True (YAML 1.1 truthy
    words), so `doc["on"]` is a KeyError on every valid GitHub workflow. A test
    that reached for `doc["on"]` and caught the KeyError would report "no
    triggers declared" for a file that declares them, which is a false negative
    in the direction that matters.
    """
    document = yaml.safe_load(text)
    if not isinstance(document, dict):
        raise AssertionError("the caller workflow is not a YAML mapping")
    if True in document and "on" not in document:
        document["on"] = document.pop(True)
    return document


def triggers(document: dict) -> set:
    on = document.get("on")
    if isinstance(on, dict):
        return set(on)
    if isinstance(on, list):
        return set(on)
    if isinstance(on, str):
        return {on}
    raise AssertionError("the caller workflow declares no usable trigger block")


def pinned_ref(document: dict) -> str:
    """The literal `ref:` of the step that checks out the decision core."""
    jobs = document.get("jobs") or {}
    found = []
    for job in jobs.values():
        for step in (job or {}).get("steps") or []:
            with_block = (step or {}).get("with") or {}
            if with_block.get("repository") == PINNED_REPOSITORY:
                found.append(with_block.get("ref"))
    if len(found) != 1:
        raise AssertionError(
            "expected exactly one checkout of %s in the caller, found %d"
            % (PINNED_REPOSITORY, len(found)))
    ref = found[0]
    if not isinstance(ref, str) or not re.fullmatch(r"[0-9a-f]{40}", ref):
        raise AssertionError(
            "the decision-core checkout must pin a literal 40-lowercase-hex "
            "commit, not %r — a movable ref is not a pin" % (ref,))
    return ref


def declared_core_commit(text: str) -> str:
    """The `core_commit` a pin file declares, read strictly."""
    matches = CORE_COMMIT_RE.findall(text)
    if len(matches) != 1:
        raise AssertionError(
            "the pin must declare exactly one readable 40-hex `core_commit`, "
            "found %d" % len(matches))
    return matches[0]


def env_pinned_commit(document: dict) -> str:
    job = (document.get("jobs") or {}).get(REQUIRED_JOB_ID) or {}
    value = (job.get("env") or {}).get("PINNED_CORE_COMMIT")
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise AssertionError(
            "the job must restate the pin as a 40-hex PINNED_CORE_COMMIT so "
            "the shell can compare it against the commit that landed, got %r"
            % (value,))
    return value


def envelope_document() -> dict:
    """The enrolled envelope, parsed, or a named failure."""
    document = yaml.safe_load(ENVELOPE.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise AssertionError("the merge-approval envelope is not a YAML mapping")
    return document


def sole_candidate(envelope: dict) -> dict:
    """The ONE enrolled candidate, refusing anything but exactly one."""
    candidates = envelope.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 1:
        raise AssertionError(
            "the envelope must enrol EXACTLY ONE candidate class — Brett "
            "Heap's word of 2026-09-06 on #656 grants one and no other, and a "
            "second entry is a NEW GRANT rather than a configuration change. "
            "Found: %r" % (candidates,))
    candidate = candidates[0]
    if not isinstance(candidate, dict):
        raise AssertionError("the enrolled candidate is not a mapping")
    return candidate


def steps_of(document: dict) -> list:
    return (document.get("jobs") or {}).get(REQUIRED_JOB_ID, {}).get("steps") or []


def step_condition(step: dict) -> str:
    return str((step or {}).get("if") or "")


def review_submitting_steps(document: dict) -> list:
    """Steps whose shell actually POSTS an approving review."""
    found = []
    for step in steps_of(document):
        script = (step or {}).get("run") or ""
        if all(marker in script for marker in REVIEW_SUBMISSION_MARKERS):
            found.append(step)
    return found


def approver_credential_steps(document: dict) -> list:
    """Every step that WIRES the merge-master credential into its inputs."""
    found = []
    for step in steps_of(document):
        wiring = yaml.safe_dump({"with": (step or {}).get("with"),
                                 "env": (step or {}).get("env")})
        if any(name in wiring for name in APPROVER_CREDENTIAL):
            found.append(step)
    return found


def shell_blocks(document: dict) -> list:
    blocks = []
    for job in (document.get("jobs") or {}).values():
        for step in (job or {}).get("steps") or []:
            script = (step or {}).get("run")
            if isinstance(script, str) and script.strip():
                blocks.append(((step or {}).get("name") or "<unnamed>", script))
    return blocks


class TheRealFiles(unittest.TestCase):
    """Tier 1 — the shipped bytes, not a fixture."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.caller_text = CALLER.read_text(encoding="utf-8")
        cls.pin_text = PIN.read_text(encoding="utf-8")
        cls.document = caller_document(cls.caller_text)

    def gather_script(self) -> str:
        for name, script in shell_blocks(self.document):
            if "changed paths" in name.lower():
                return script
        raise AssertionError(
            "no step named for the changed-path gather was found; the "
            "masking check below would otherwise check nothing")

    def test_the_caller_and_the_pin_exist(self) -> None:
        self.assertTrue(CALLER.is_file(), f"missing caller: {CALLER}")
        self.assertTrue(PIN.is_file(), f"missing pin: {PIN}")

    def test_the_workflow_and_the_pin_name_the_same_commit(self) -> None:
        """THE POINT OF THIS MODULE."""
        workflow_ref = pinned_ref(self.document)
        pin_commit = declared_core_commit(self.pin_text)
        self.assertEqual(
            workflow_ref, pin_commit,
            "PIN DRIFT: %s checks out %s@%s but %s declares core_commit %s. "
            "Change BOTH in one reviewed diff — the pin is the recorded "
            "referent and the workflow is what actually runs."
            % (CALLER.relative_to(REPO_ROOT), PINNED_REPOSITORY, workflow_ref,
               PIN.relative_to(REPO_ROOT), pin_commit))

    def test_the_job_env_restates_the_same_commit(self) -> None:
        """A third witness, because the shell compares against the env value."""
        self.assertEqual(env_pinned_commit(self.document),
                         pinned_ref(self.document),
                         "the job's PINNED_CORE_COMMIT must be byte-identical "
                         "to the checkout `ref:`; the run-time pin assertion "
                         "compares against it")

    def test_the_pin_declares_the_ratified_shape(self) -> None:
        pin = yaml.safe_load(self.pin_text)
        self.assertIsInstance(pin, dict, "the pin is not a YAML mapping")
        self.assertEqual(pin.get("schema_version"), 1)
        self.assertEqual(pin.get("kind"), "pinned_workflow")
        self.assertEqual(pin.get("repository"), PINNED_REPOSITORY)
        self.assertEqual(
            pin.get("revision_kind"), "commit",
            "a tag or branch pin is refused: a movable ref is not a pin")
        self.assertRegex(str(pin.get("declared_at")), r"^\d{4}-\d{2}-\d{2}$")
        self.assertIn(
            ".github/workflows/merge-master-approval.yml",
            pin.get("governs") or [],
            "the pin must name the caller it governs")

    def test_the_pin_names_the_members_the_caller_actually_reads(self) -> None:
        pin = yaml.safe_load(self.pin_text)
        paths = {member.get("path")
                 for member in (pin.get("pinned_members") or [])}
        self.assertIn("scripts/merge_master/repository_floor.py", paths)
        self.assertIn(
            "scripts/merge_master/repository_floor_drift.py", paths,
            "the drift module became load-bearing at the 2026-09-01 (b′) "
            "advance — `post_merge_tree_paths` and `candidate_floor_drift` are "
            "re-exported through `repository_floor`, so the import site does "
            "not name it and a re-point ceremony would not know to re-verify it")
        self.assertIn(
            "scripts/merge_master/openxfactory-review-authority-floor.yaml",
            paths,
            "the pin must name the floor document, so a re-point ceremony "
            "knows what to re-verify")

    def test_the_pin_records_its_lockstep_state_with_the_aggregation_pin(self) -> None:
        """Diverged or converged, the state must be declared — never implied.

        Diverged since declaration; CONVERGED at the 2026-08-28 re-point
        ceremony (this repository's PR #483 paired with xFactory eae4dc6);
        DIVERGED AGAIN on 2026-09-01, when the (b′) activation advanced this
        pin alone. xFactory's two surfaces still name `f4702f64`, where the
        floor carries four entries and the three functions this caller now
        calls do not exist — so the converged commit cannot evaluate the object
        the advance exists to make operative. The divergence is forced by the
        feature for the second time, and the obligation to re-converge stands.
        """
        pin = yaml.safe_load(self.pin_text)
        lockstep = pin.get("lockstep") or {}
        self.assertEqual(lockstep.get("status"), "diverged")
        self.assertTrue(str(lockstep.get("reason") or "").strip(),
                        "the lockstep state must state WHY")
        self.assertTrue(str(lockstep.get("obligation") or "").strip(),
                        "the standing rule for future advances must remain: "
                        "advance only at a ceremony converging all three "
                        "surfaces")
        self.assertEqual(len(lockstep.get("converged_with") or []), 2,
                         "both xFactory merge-master surfaces must be named")

    def test_the_pin_declares_advisory_scope_and_the_never_performs_set(self) -> None:
        pin = yaml.safe_load(self.pin_text)
        scope = pin.get("scope") or {}
        self.assertIs(scope.get("advisory_only"), True)
        never = set(scope.get("never_performs") or [])
        for act in ("submitting a review", "calling merge",
                    "enabling auto-merge"):
            self.assertIn(act, never)

    def test_the_pin_carries_exactly_one_commit_shaped_value(self) -> None:
        """One value, one declared derivation-pin-class member.

        A second commit-shaped value in this file would be a second pin site
        needing its own declared member; the diverging xFactory pin is named in
        the caller's header instead, and `.github/` is outside the sweep roots.
        """
        found = set(SHA_RE.findall(self.pin_text))
        self.assertEqual(
            len(found), 1,
            "the pin must carry exactly one 40-hex value, found %d: %s"
            % (len(found), sorted(found)))

    def test_the_pin_is_a_declared_derivation_pin_class_member(self) -> None:
        module = _load_pin_class()
        members = [member for member in module.PIN_CLASS
                   if "contracts/review-lane-pin.yaml" in member.paths]
        self.assertEqual(
            len(members), 1,
            "exactly one PIN_CLASS member must cover the pin, found %d"
            % len(members))
        member = members[0]
        self.assertEqual(member.key, "core_commit")
        self.assertEqual(member.key_form, "field")
        self.assertEqual(
            member.locality, module.CROSS_REPOSITORY,
            "a codexFactory commit must never be expected to resolve here")
        self.assertEqual(member.presence, module.CURRENT)
        self.assertIn(
            "core_commit", module.PIN_KEY_VOCABULARY,
            "declaring the member is what teaches the sweep vocabulary the key")

    def test_the_caller_declares_exactly_one_job_with_the_required_id(self) -> None:
        jobs = self.document.get("jobs") or {}
        self.assertEqual(
            sorted(jobs), [REQUIRED_JOB_ID],
            "the check-run name is the job id. A second job would produce a "
            "check-run whose name codexFactory's envelope self-exclusion does "
            "not match, and a different id would not match a future ruleset.")

    def test_the_caller_declares_exactly_the_intended_triggers(self) -> None:
        self.assertEqual(triggers(self.document), EXPECTED_TRIGGERS)

    def test_the_head_executing_trigger_is_absent(self) -> None:
        """`pull_request` runs THIS FILE from the head, with the secrets."""
        self.assertNotIn(
            "pull_request", triggers(self.document),
            "a plain `pull_request` trigger would run the head's copy of this "
            "file with the App credential that reads a private repository in "
            "scope — the exfiltration shape the base-branch rule prevents")

    def test_the_caller_holds_only_read_permissions(self) -> None:
        self.assertEqual(self.document.get("permissions"),
                         EXPECTED_PERMISSIONS)

    def test_no_checkout_takes_the_pull_request_head(self) -> None:
        job = (self.document.get("jobs") or {})[REQUIRED_JOB_ID]
        for step in job.get("steps") or []:
            with_block = (step or {}).get("with") or {}
            ref = str(with_block.get("ref") or "")
            self.assertNotIn(
                "github.event.pull_request.head", ref,
                "no checkout may take the candidate's head: rules must come "
                "from the base branch (step %r)" % ((step or {}).get("name"),))

    def test_the_caller_contains_no_merge_shaped_step(self) -> None:
        """Act A4 granted approval, never landing. The absence is structural."""
        for needle in MERGE_SHAPED:
            self.assertNotIn(
                needle, self.caller_text,
                "%r appears in the caller. This lane may approve the one "
                "enrolled candidate class and nothing more: it must remain "
                "unable to merge or to enable auto-merge, and the steps are "
                "absent rather than disabled. The aggregation's intent-apply "
                "lane arms auto-merge on its own side (ruling D-3 on #656)."
                % needle)

    # ---- THE NARROW GRANT ------------------------------------------------
    #
    # Everything from here to the end of the class replaces what used to be a
    # single assertion that no envelope existed. The reason that assertion
    # existed is recorded in this module's docstring and is STILL IN FORCE for
    # the class it covers: the Gate-Rules Council's 2026-08-28 unanimous
    # refusal of a class over `openspec/changes/**`, and
    # `add-substantive-review-lane` task 3.2, which stays OPEN.

    def test_the_caller_ships_the_enrolled_envelope(self) -> None:
        self.assertTrue(
            ENVELOPE.is_file(),
            "act A4 enrols one candidate class, and the class lives in "
            "%s. Without the file the lane is advisory again and the "
            "approval steps below can never fire." % ENVELOPE)

    def test_the_envelope_declares_the_ratified_shape(self) -> None:
        envelope = envelope_document()
        self.assertEqual(envelope.get("schema_version"), 1)
        self.assertEqual(envelope.get("kind"), "merge_approval_envelope")
        self.assertEqual(
            envelope.get("org"), "opensoft",
            "this mechanism governs Opensoft's own vendor build org only, "
            "never a client tenant")
        self.assertTrue(str(envelope.get("id") or "").strip(),
                        "the envelope must carry an id")

    def test_the_envelope_enrols_exactly_one_candidate(self) -> None:
        """THE POINT OF THE GRANT. One class, on one man's word, for one lane.

        A second entry is not a configuration change: it is a new grant,
        needing its own word or its own council record. Widening it must break
        a test somebody has to justify changing.
        """
        candidate = sole_candidate(envelope_document())
        self.assertEqual(candidate.get("id"), ENROLLED_CANDIDATE_ID)

    def test_the_enrolled_candidate_is_the_narrow_one(self) -> None:
        candidate = sole_candidate(envelope_document())
        self.assertEqual(
            candidate.get("target_repos"), ["opensoft/openxFactory"],
            "the class exists on this repository and nowhere else")
        self.assertEqual(
            candidate.get("expected_author"), ENROLLED_AUTHOR,
            "the exact REST bot login of the content App that authors the "
            "custody pull request — a DISTINCT identity from the merge-master "
            "approver, or GitHub's author-cannot-approve rule voids the "
            "approval. Verified against the standing candidate #176.")
        self.assertEqual(
            candidate.get("expected_head_ref"), ENROLLED_HEAD_REF,
            "an EXACT same-repository head ref, never a pattern: it is half of "
            "the fork defence, and a fork cannot present it")
        self.assertEqual(candidate.get("expected_base_ref"), ENROLLED_BASE_REF)
        self.assertEqual(
            candidate.get("path_allowlist"), ENROLLED_PATHS,
            "the admitted surface is the two record trees "
            "`scripts/ideation_dashboard/intent_apply_lane.py` actually writes "
            "(`DEFAULT_INTENTS_DIR` and `gate_console.DEFAULT_RECORDS_DIR`) "
            "and nothing else. The lane commits with `git add -A`, so a "
            "delivery that touches anything beyond them falls outside this "
            "list and PARKS — which is what makes this a narrow first "
            "candidate rather than a general grant.")
        self.assertIs(
            candidate.get("require_all_checks"), True,
            "stated explicitly rather than left to the schema default: a "
            "conservative superset of 'all required checks green', which can "
            "only ever park more often than the merge gate would block")
        self.assertIn(
            REQUIRED_JOB_ID, candidate.get("check_exclusions") or [],
            "the approval workflow's own check-run must be excluded or the "
            "candidate self-deadlocks: GitHub names the check-run after the "
            "job id, and the run is still in progress while it evaluates")

    def test_the_enrolled_candidate_declares_no_open_finding_keys(self) -> None:
        """The candidate's KEY SET is pinned, not merely the values above.

        xFactory's `doc-health-nightly` candidate carries
        `open_finding_title_prefixes` and `open_finding_labels: []` because
        that candidate IS the doc-health report and such a finding is ABOUT
        the very tree it delivers (see that repository's own envelope). No
        finding class here ties to the intent record trees — the envelope's
        own header records that reasoning — so neither key may reappear on
        this candidate. A key silently added back would hand the pinned
        core's open-finding condition something to quantify over that no
        value-level assertion above would ever see, since both keys are
        absent today rather than present-and-empty.
        """
        candidate = sole_candidate(envelope_document())
        self.assertNotIn(
            "open_finding_title_prefixes", candidate,
            "no finding class in this repository is about the intent record "
            "trees; adding this key is a new grant, not a config tweak")
        self.assertNotIn(
            "open_finding_labels", candidate,
            "no finding class in this repository is about the intent record "
            "trees; adding this key is a new grant, not a config tweak")

    def test_the_enrolled_surface_admits_no_refused_path(self) -> None:
        """The 2026-08-28 refusal, asserted rather than merely remembered.

        The council refused a class over `openspec/changes/**` because its
        admitted surface lies wholly inside the canonical GATE_INTEGRITY_FLOOR.
        A later widening that reached any governed surface would re-enrol by
        accident exactly what was refused on purpose, so the refused ground is
        named here as a standing floor under the allowlist.
        """
        candidate = sole_candidate(envelope_document())
        refused_ground = ("openspec/", "contracts/", "governance/", ".github/",
                          "scripts/", "health/", "openXwallet")
        for pattern in candidate.get("path_allowlist") or []:
            for ground in refused_ground:
                self.assertFalse(
                    pattern.startswith(ground),
                    "path_allowlist entry %r reaches %r — refused ground. The "
                    "Gate-Rules Council's 2026-08-28 refusal stands and "
                    "add-substantive-review-lane task 3.2 is still OPEN; "
                    "widening onto it needs a council record, not an edit."
                    % (pattern, ground))
        self.assertNotIn(
            "**", [p.strip() for p in candidate.get("path_allowlist") or []],
            "a universal pattern is an allowlist that admits everything")

    def test_the_envelope_records_the_grant_and_the_standing_refusal(self) -> None:
        """A grant a reader cannot find is a grant nobody can audit."""
        text = ENVELOPE.read_text(encoding="utf-8")
        for phrase in ("Brett Heap", "2026-09-06", "#656", "2026-08-28",
                       "task 3.2"):
            self.assertIn(
                phrase, text,
                "the envelope's header must record the grant (who, when, on "
                "what issue) AND that the council's refusal still stands for "
                "the class it refused; %r is missing" % phrase)

    def test_the_envelope_is_routed_to_a_code_owner(self) -> None:
        """Widening the grant must be a reviewed human act.

        xFactory's envelope leans on `.github/` being code-owned wholesale.
        Here only `.github/workflows/` is, so the envelope needs its own line
        or the one file that decides what may be autonomously approved is the
        one file nobody is required to look at.
        """
        owners = CODEOWNERS.read_text(encoding="utf-8")
        self.assertRegex(
            owners,
            r"(?m)^/\.github/merge-approval-envelope\.yml\s+@\S+",
            "route the envelope to a human owner: `.github/workflows/` is "
            "owned but `.github/merge-approval-envelope.yml` is not covered "
            "by that entry")

    # ---- THE ONE DOOR ------------------------------------------------------

    def test_exactly_one_step_submits_a_review(self) -> None:
        found = review_submitting_steps(self.document)
        self.assertEqual(
            len(found), 1,
            "exactly one step may submit a review, found %d: %r. Two doors is "
            "two things to keep gated, and the second is the one that gets "
            "forgotten." % (len(found), [s.get("name") for s in found]))

    def test_the_review_submission_is_gated_on_the_envelope_decision(self) -> None:
        """THE POINT OF THIS MODULE, SINCE ACT A4.

        `steps.envelope.outputs.decision` is written by nothing but the pinned
        core's exit code, through the guarded emitter, so this one `if:` is the
        whole authority chain: envelope config (base branch) -> pinned core ->
        this literal -> one APPROVE review.
        """
        step = review_submitting_steps(self.document)[0]
        self.assertIn(
            APPROVAL_GATE, step_condition(step),
            "the review-submitting step %r must carry %r in its `if:` — an "
            "approval reachable any other way is an approval the envelope did "
            "not authorise" % (step.get("name"), APPROVAL_GATE))

    def test_every_step_touching_the_approver_credential_is_gated(self) -> None:
        found = approver_credential_steps(self.document)
        self.assertGreaterEqual(
            len(found), 2,
            "expected at least the mint and the submit to name the "
            "merge-master credential; found %r"
            % [s.get("name") for s in found])
        for step in found:
            with self.subTest(step=step.get("name")):
                self.assertIn(
                    ENVELOPE_DECISION, step_condition(step),
                    "step %r reaches the approver credential without "
                    "consulting the envelope decision" % (step.get("name"),))

    def test_the_app_token_mint_is_scoped_to_pull_requests_only(self) -> None:
        """`pull-requests: write` alone — and NOTHING wider, `issues` included.

        The live installation (App ID 4312542, installation 159938946 on
        `opensoft`) grants the merge-master App exactly
        `checks: write, contents: write, metadata: read, pull_requests:
        write` — no `issues` permission at all. Requesting
        `permission-issues: write` on the mint does not merely ask for an
        unused scope: `create-github-app-token` REFUSES THE MINT OUTRIGHT
        when a requested permission is not granted to the installation,
        failing this lane before any review or comment is attempted. The
        installation needs `contents: write` for the approval to COUNT (that
        is the installation's OWN grant, not the token's). The TOKEN this
        step mints needs none of that: it submits one review AND posts one
        sticky comment, both under `pull-requests: write` alone — "Record
        the envelope outcome" posts and patches through the Issues Comments
        API, but GitHub accepts EITHER `issues: write` OR `pull_requests:
        write` on that endpoint when the target is a pull request, so
        `pull-requests: write` alone covers both writes. xFactory's own
        production caller mints with `permission-pull-requests: write` only
        and posts its sticky comment through the same endpoint, proven live.
        """
        mints = [step for step in steps_of(self.document)
                 if str((step or {}).get("uses") or "").startswith(
                     "actions/create-github-app-token")
                 and "MERGE_MASTER_APP_KEY" in yaml.safe_dump(step)]
        self.assertEqual(len(mints), 1,
                         "exactly one merge-master token mint, found %d"
                         % len(mints))
        with_block = (mints[0].get("with") or {})
        self.assertEqual(
            with_block.get("permission-pull-requests"), "write",
            "the mint must narrow the token to `pull-requests: write` — "
            "needed to submit the APPROVE review and post the sticky "
            "comment")
        self.assertNotIn(
            "permission-issues", with_block,
            "the mint must NOT request `permission-issues` — the live "
            "installation (App ID 4312542, installation 159938946) holds no "
            "`issues` permission, and requesting it refuses the mint "
            "outright rather than merely granting an unused scope")
        for scope in with_block:
            self.assertNotIn(
                scope, ("permission-contents", "permission-administration",
                        "permission-actions", "permission-workflows"),
                "the mint requests %r, which nothing in this lane writes"
                % scope)

    def test_the_workflow_token_holds_no_write_scope(self) -> None:
        """Stricter than xFactory's caller, and deliberately so."""
        for scope, level in (self.document.get("permissions") or {}).items():
            with self.subTest(scope=scope):
                self.assertEqual(
                    level, "read",
                    "`%s: %s` — the workflow's own GITHUB_TOKEN must stay "
                    "read-only on a `pull_request_target` lane. The approval "
                    "and its comment are written with the separately minted "
                    "App token." % (scope, level))

    def test_the_envelope_decision_output_carries_a_closed_world_shape(self) -> None:
        """A `reason` with one newline must never become `decision=approve`.

        `$GITHUB_OUTPUT` is a newline-delimited `key=value` file and the LAST
        write of a key wins; `reason` comes out of the pinned core carrying
        externally-supplied check-run and status NAMES. So the emitter refuses
        an unrenderable value outright rather than escaping it, and `decision`
        is one of four literals rather than interpolated text.
        """
        self.assertIn(
            r'"decision": re.compile(r"\A(approve|already|skip|park)\Z")',
            self.caller_text,
            "the emitter must pin `decision` to a closed world of literals")
        self.assertNotIn(
            'echo "decision=', self.caller_text,
            "`decision` may be written only by the guarded emitter — an "
            "unguarded `echo` is exactly the line a hostile reason overwrites")

    def test_the_floor_is_composed_over_the_envelope(self) -> None:
        """A never-clearable path is never approvable, whatever the envelope says.

        The enrolled allowlist and the floor are disjoint today, so this gate
        can only fire on a future widening — which is precisely when nobody
        would remember to add it.
        """
        self.assertIn(
            "FLOOR_MATCHED: ${{ steps.floor.outputs.matched }}",
            self.caller_text,
            "the envelope step must read the floor verdict")
        self.assertIn(
            'if [ "${FLOOR_MATCHED:-}" != "0" ]; then', self.caller_text,
            "anything but a literal 0 — including the EMPTY value a skipped "
            "or failed floor step leaves — must refuse")

    def test_the_envelope_is_read_from_the_base_branch(self) -> None:
        """A pull request may never alter the rules governing its own approval."""
        self.assertIn(
            "CONFIG: .github/merge-approval-envelope.yml", self.caller_text,
            "the envelope path must be a repository-relative literal resolved "
            "against the BASE checkout, never a URL and never a head path")
        job = (self.document.get("jobs") or {})[REQUIRED_JOB_ID]
        for step in job.get("steps") or []:
            env = (step or {}).get("env") or {}
            config = str(env.get("CONFIG") or "")
            if not config:
                continue
            with self.subTest(step=(step or {}).get("name")):
                self.assertFalse(
                    config.startswith("/") or ".." in config
                    or config.startswith("http"),
                    "the envelope config must be read from the base checkout, "
                    "got %r" % config)

    def test_the_caller_evaluates_this_repositorys_floor(self) -> None:
        self.assertIn(
            FLOOR_REPOSITORY, self.caller_text,
            "the caller must name the repository whose gate floor it evaluates")
        self.assertIn("repository_floor", self.caller_text)

    def test_the_caller_opts_into_the_floor_reachability_check(self) -> None:
        """`tree_paths` is opt-in; a floor matching nothing must not be silent.

        SINCE THE (b′) ADVANCE THE TREE IS THE POST-MERGE ONE. Against the base
        tree alone the pull request that DELETES a floored path is green and the
        next, innocent one is red — which is the inversion LA-A2 filed and
        CPL-C1 measured. CPL-C1's first sufficient discharge, verbatim: *"the
        base tree adjusted by the candidate's own changed paths"*.
        """
        self.assertIn(
            "tree_paths=post_merge", self.caller_text,
            "the core's reachability check is opt-in precisely because a floor "
            "usually names another repository's paths. Here we ARE that "
            "repository, so an unreachable floor path must be a named failure "
            "— and it must be named on the pull request that CAUSED it, which "
            "means parsing against the post-merge path set.")
        self.assertNotIn(
            "parse_repository_floor(document, tree_paths=tree)",
            self.caller_text,
            "parsing against the BASE tree alone is the pre-(b′) behaviour "
            "LA-A2 and CPL-C1 both refuse: it fails the next pull request "
            "rather than the deleting one. (Matched on the whole call, not on "
            "`tree_paths=tree`: the drift call's own `base_tree_paths=tree` "
            "carries that substring and IS the base tree, correctly.)")

    def test_the_caller_calls_the_three_amended_core_functions(self) -> None:
        """Each name is one BLOCKING amendment's mechanism, wired here.

        The mechanisms landed in codexFactory PR #162 and are INERT until a
        caller invokes them; the record calls the two pull requests one landing.
        Asserted over the caller text so a refactor that quietly drops one is a
        red test rather than a silently weaker lane.

        `candidate_floor_drift` NAMED THIS FUNCTION UNTIL
        `mirror-floor-addition-grace` (task 3.1): LA-A2's attribution
        (`caused_by_candidate` / `already_unreachable`) is now read off the
        SAME `evaluate_floor_completeness` call LQ-A7's completeness direction
        already needs for the addition grace, rather than from a second,
        separately-called function — both partitions come from the pinned
        core's own `_drift_between`, so this is one call reading two facts off
        it rather than two callers of the same underlying rule. See
        `test_the_caller_asserts_the_floors_completeness_and_grace` for the
        grace's own assertions.
        """
        for function, amendment in (
                ("post_merge_tree_paths", "LA-A2 / CPL-C1 (deletions)"),
                ("evaluate_floor_completeness",
                 "LA-A2 (attribution) and LQ-A7 (completeness), ONE call since "
                 "mirror-floor-addition-grace"),
                ("parse_repository_floor_reporting", "LS-A1 (report before you refuse)")):
            self.assertIn(
                function, self.caller_text,
                "%s is the mechanism of %s and the caller does not call it"
                % (function, amendment))

    def test_the_gather_collects_the_status_the_drift_check_needs(self) -> None:
        """LA-A2's amendment, in one word: *"add `status`"*.

        Without it the core's `post_merge_tree_paths` cannot tell a deletion
        from an addition, and it refuses rather than guessing — so a gather that
        stopped collecting `status` would turn every run into a refusal at
        `changed_entries_unusable` rather than into a silent pass. This asserts
        the healthy shape rather than relying on that refusal.
        """
        gather = self.gather_script()
        self.assertIn(
            ".status", gather,
            "the changed-file gather must prove a string `status` on every "
            "entry: the post-merge tree cannot be reconstructed from "
            "incomplete facts without risking either a silent deletion or a "
            "false accusation")
        self.assertIn(
            "changed_entries.json", gather,
            "the gather must emit the changed ENTRIES (filename + status + "
            "previous_filename), not only the flattened path list")

    def test_the_caller_asserts_the_floors_completeness_and_grace(self) -> None:
        """LQ-A7 (BLOCKING), homed here by the seat and by the ruling.

        LQ: a check that *"fails when a tracked `openspec/specs/**` path is
        absent from `floor.never_clearable_paths`"*, in
        `merge-master-approval.yml`, *"which already produces `tree_paths.txt`,
        so the assertion is a set difference over data on hand"*. Ruled BOTH,
        LAYERED at record §6.1 — this half here, the required-check half in
        `pytest-suite` (see `test_floor_snapshot.py`).

        EXTENDED by `mirror-floor-addition-grace`: the completeness direction
        is no longer a bare set difference, and this asserts the grace's own
        wiring — the imported measurement function, the reported stage, the
        `pending_floor_extension` key, and the base checkout's `fetch-depth`
        the pin window needs (requirement 5 / decision C).
        """
        self.assertIn(
            "FLOORED_PREFIX: openspec/specs", self.caller_text,
            "the enumerated surface must be a CODE CONSTANT in the caller. The "
            "generated block declares its prefix in a COMMENT, which is not "
            "data: a prefix read out of prose narrows silently when the prose "
            "changes.")
        self.assertIn(
            "uncovered_paths", self.caller_text,
            "the completeness result must be reported by name, so a reader of "
            "a red run learns WHICH paths are off the floor")
        self.assertIn(
            "floor_incomplete", self.caller_text,
            "the completeness failure needs its own stage: it is a different "
            "defect from an unreachable floor and the repair is the reverse")
        self.assertIn(
            "pin_window_for_document", self.caller_text,
            "B1's window must be measured through the pinned core's own "
            "function, not re-derived, so the two floor lanes cannot disagree "
            "about what it means for a pin to be an ancestor of the base")
        self.assertIn(
            "pending_floor_extension", self.caller_text,
            "the graced stage must be reported by name, distinct from "
            "floor_incomplete, so a reader or a machine consumer keying on "
            "the stage cannot mistake a graced path for a floored one")

    def test_the_base_checkout_carries_the_history_the_pin_window_needs(self) -> None:
        """Decision C: `fetch-depth: 0` on THIS repository's base checkout.

        Measured 2026-09-05 (design.md §4): 2,025 commits, 29.6 MiB packed —
        the declared cost of a full-history checkout on a step that fetched
        one commit before this change. A shallow checkout cannot resolve the
        floor snapshot's declared `generated_at`, so B1's pin window would be
        permanently fail-safed off in this lane while it worked in
        `pytest-suite` (already full history) — the disagreement requirement 6
        of the core packet forbids between the two lanes.
        """
        job = (self.document.get("jobs") or {})[REQUIRED_JOB_ID]
        base_checkout = None
        for step in job.get("steps") or []:
            if (step or {}).get("name") == "Checkout base (this repository)":
                base_checkout = step
                break
        self.assertIsNotNone(
            base_checkout,
            "the 'Checkout base (this repository)' step is gone or renamed")
        with_block = (base_checkout or {}).get("with") or {}
        self.assertEqual(
            with_block.get("fetch-depth"), 0,
            "the base checkout must declare fetch-depth: 0, or B1's pin "
            "window is unmeasurable on every run of this lane")
        self.assertIsNone(
            with_block.get("ref"),
            "the base checkout must take the BASE branch tip — no ref: — "
            "never the candidate's head")

    def test_the_changed_path_gather_masks_no_failure(self) -> None:
        """A `|| echo '[]'` turns a rate-limited read into a false clean set.

        Scoped to the GATHER step, which is the only place masking produces a
        false CLEAN verdict. `gh api` writes its error body to stdout and exits
        non-zero, so a fallback there converts a failed or rate-limited query
        into an apparently-complete empty set — and the floor is exact set
        membership over that set.
        """
        gather = self.gather_script()
        for masking in ("|| echo '[]'", '|| echo "[]"', "|| true", "|| :",
                        "continue-on-error"):
            self.assertNotIn(
                masking, gather,
                "%r in the changed-path gather would convert a failed API read "
                "into a clean, empty, apparently-complete fact set, and the "
                "floor is exact set membership over that set" % masking)

    def test_the_gather_proves_completeness_and_rechecks_the_head(self) -> None:
        for marker in ("changed_files", "--paginate", "previous_filename",
                       "HEAD_SHA_AFTER"):
            self.assertIn(
                marker, self.caller_text,
                "the gather must prove completeness against the authoritative "
                "total, paginate, fold in renames, and recheck the head; %r "
                "is missing" % marker)

    def test_every_embedded_shell_block_parses(self) -> None:
        blocks = shell_blocks(self.document)
        self.assertGreater(len(blocks), 0, "the caller runs no shell at all")
        for name, script in blocks:
            with self.subTest(step=name):
                result = subprocess.run(
                    ["bash", "-n"], input=script, text=True,
                    capture_output=True, check=False)
                self.assertEqual(
                    result.returncode, 0,
                    "embedded shell in step %r does not parse:\n%s"
                    % (name, result.stderr))

    def test_every_embedded_shell_block_is_strict(self) -> None:
        for name, script in shell_blocks(self.document):
            with self.subTest(step=name):
                self.assertIn(
                    "set -euo pipefail", script,
                    "step %r runs shell without strict mode; an unset variable "
                    "or a failed pipe stage would pass silently" % name)

    def test_the_pin_is_routed_to_a_code_owner(self) -> None:
        owners = CODEOWNERS.read_text(encoding="utf-8")
        self.assertRegex(
            owners,
            r"(?m)^/contracts/review-lane-pin\.yaml\s+@\S+",
            "the pin decides WHICH code a governance surface executes, so it "
            "must be routed to a human owner like contracts/openxwallet-pin.yaml")

    def test_the_caller_workflow_directory_is_already_code_owned(self) -> None:
        owners = CODEOWNERS.read_text(encoding="utf-8")
        self.assertRegex(owners, r"(?m)^\.github/workflows/\s+@\S+")


class NegativeControls(unittest.TestCase):
    """Tier 2 — each positive above is one mutation from failing.

    A check that has quietly stopped checking passes tier 1 exactly as a healthy
    one does. These mutate the real text in memory and require the refusal.
    """

    @classmethod
    def setUpClass(cls) -> None:
        # A clear assertion, not a bare `FileNotFoundError`. `TheRealFiles`
        # already asserts each of these exists with an explanatory message,
        # but unittest gives no ordering guarantee between classes, so a
        # reader who runs `NegativeControls` alone (or watches it fail first)
        # must not be left with a raw traceback pointing at `read_text`.
        for label, path in (("caller", CALLER), ("pin", PIN),
                            ("envelope", ENVELOPE)):
            if not path.is_file():
                raise AssertionError(
                    "NegativeControls mutates the real %s file and cannot "
                    "run without it: missing %s. See TheRealFiles for the "
                    "assertion that normally catches this." % (label, path))
        cls.caller_text = CALLER.read_text(encoding="utf-8")
        cls.pin_text = PIN.read_text(encoding="utf-8")
        cls.envelope_text = ENVELOPE.read_text(encoding="utf-8")

    def test_the_unmutated_pair_is_a_positive_first(self) -> None:
        """Ordering guard: a fixture that never passes proves nothing."""
        document = caller_document(self.caller_text)
        self.assertEqual(pinned_ref(document),
                         declared_core_commit(self.pin_text))

    def test_a_missing_source_file_fails_with_a_clear_message(self) -> None:
        """`setUpClass` must name the missing file, not leak a bare traceback."""
        import unittest.mock as mock

        missing = ENVELOPE.parent / "does-not-exist-merge-approval-envelope.yml"
        with mock.patch(__name__ + ".ENVELOPE", missing):
            with self.assertRaises(AssertionError) as ctx:
                NegativeControls.setUpClass()
        self.assertIn("envelope", str(ctx.exception))
        self.assertIn(str(missing), str(ctx.exception))

    def test_a_drifted_workflow_ref_is_refused(self) -> None:
        real = declared_core_commit(self.pin_text)
        # Hex but NOT all-digits, deliberately: `"0" * 40` is resolved by
        # YAML 1.1 to the integer 0, which makes the mutation a type error
        # rather than a drifted commit. (The real pin values are quoted in both
        # files for the same reason.)
        drifted = "deadbeef" * 5
        self.assertNotEqual(drifted, real)
        mutated = self.caller_text.replace(real, drifted)
        self.assertNotEqual(mutated, self.caller_text, "mutation did not apply")
        document = caller_document(mutated)
        self.assertNotEqual(pinned_ref(document),
                            declared_core_commit(self.pin_text))

    def test_a_pin_with_no_core_commit_is_refused(self) -> None:
        mutated = CORE_COMMIT_RE.sub("core_commit: not-a-commit", self.pin_text)
        with self.assertRaises(AssertionError):
            declared_core_commit(mutated)

    def test_a_pin_with_two_core_commits_is_refused(self) -> None:
        mutated = self.pin_text + "\ncore_commit: %s\n" % ("a" * 40)
        with self.assertRaises(AssertionError):
            declared_core_commit(mutated)

    def test_a_branch_pin_in_the_workflow_is_refused(self) -> None:
        real = declared_core_commit(self.pin_text)
        # The real values are QUOTED in both files (an all-digit 40-char sha
        # would otherwise be resolved by YAML 1.1 to an integer), so the
        # mutation must replace the quoted form.
        mutated = self.caller_text.replace('ref: "%s"' % real, "ref: main")
        self.assertNotEqual(mutated, self.caller_text, "mutation did not apply")
        with self.assertRaises(AssertionError):
            pinned_ref(caller_document(mutated))

    def test_a_second_job_is_refused(self) -> None:
        mutated = self.caller_text + (
            "\n  a-second-job:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: 'true'\n")
        document = caller_document(mutated)
        self.assertNotEqual(sorted(document.get("jobs") or {}),
                            [REQUIRED_JOB_ID],
                            "a second job must be visible to the job-id check")

    def test_an_added_write_permission_is_visible(self) -> None:
        mutated = self.caller_text.replace(
            "  pull-requests: read # candidate metadata",
            "  pull-requests: write # candidate metadata")
        self.assertNotEqual(mutated, self.caller_text, "mutation did not apply")
        self.assertNotEqual(caller_document(mutated).get("permissions"),
                            EXPECTED_PERMISSIONS)

    def test_a_merge_shaped_addition_is_visible(self) -> None:
        mutated = self.caller_text + "\n          gh pr merge --auto \n"
        hits = [needle for needle in MERGE_SHAPED if needle in mutated]
        self.assertIn("gh pr merge", hits,
                      "the merge denylist must catch a landing call")
        self.assertIn("--auto ", hits,
                      "the merge denylist must catch auto-merge enablement")

    def test_the_unmutated_envelope_is_a_positive_first(self) -> None:
        """Ordering guard: a fixture that never passes proves nothing."""
        candidate = sole_candidate(yaml.safe_load(self.envelope_text))
        self.assertEqual(candidate.get("id"), ENROLLED_CANDIDATE_ID)

    def test_a_second_enrolled_candidate_is_refused(self) -> None:
        """A second class is a NEW GRANT, and must fail loudly, not quietly."""
        mutated = yaml.safe_load(self.envelope_text)
        mutated["candidates"].append({
            "id": "something-else",
            "target_repos": ["opensoft/openxFactory"],
            "expected_author": "openxfactory[bot]",
            "expected_head_ref": "other/branch",
            "path_allowlist": ["health/**"],
        })
        with self.assertRaises(AssertionError):
            sole_candidate(mutated)

    def test_a_widened_allowlist_is_visible(self) -> None:
        mutated = yaml.safe_load(self.envelope_text)
        mutated["candidates"][0]["path_allowlist"] = ENROLLED_PATHS + [
            "openspec/changes/**"]
        candidate = sole_candidate(mutated)
        self.assertNotEqual(
            candidate.get("path_allowlist"), ENROLLED_PATHS,
            "the exact-allowlist assertion must see a widening")
        reached = [pattern for pattern in candidate["path_allowlist"]
                   if pattern.startswith("openspec/")]
        self.assertTrue(
            reached,
            "the refused-ground assertion must see a path_allowlist that "
            "reaches the surface the 2026-08-28 council refusal covers")

    def test_a_disabled_check_gate_is_visible(self) -> None:
        mutated = yaml.safe_load(self.envelope_text)
        mutated["candidates"][0]["require_all_checks"] = False
        self.assertIsNot(
            sole_candidate(mutated).get("require_all_checks"), True,
            "`require_all_checks: false` disables the greenness condition "
            "entirely and must be visible to the assertion")

    def test_an_ungated_review_submission_is_visible(self) -> None:
        """Drop the one door and the door-check must fail, not shrug."""
        mutated = self.caller_text.replace(
            "if: env.HAS_MERGE_MASTER_APP == 'true' && "
            + APPROVAL_GATE,
            "if: env.HAS_MERGE_MASTER_APP == 'true'")
        self.assertNotEqual(mutated, self.caller_text, "mutation did not apply")
        document = caller_document(mutated)
        submitters = review_submitting_steps(document)
        self.assertEqual(len(submitters), 1)
        self.assertNotIn(APPROVAL_GATE, step_condition(submitters[0]))

    def test_a_widened_workflow_permission_is_visible(self) -> None:
        mutated = self.caller_text.replace(
            "  checks: read # head check-runs",
            "  checks: write # head check-runs")
        self.assertNotEqual(mutated, self.caller_text, "mutation did not apply")
        levels = set((caller_document(mutated).get("permissions") or {}).values())
        self.assertIn("write", levels,
                      "a write scope on the workflow token must be visible")

    def test_a_broken_shell_block_is_caught(self) -> None:
        result = subprocess.run(
            ["bash", "-n"], input="if [ 1 -eq 1 ]; then\n", text=True,
            capture_output=True, check=False)
        self.assertNotEqual(
            result.returncode, 0,
            "`bash -n` must reject an unterminated block, or the shell check "
            "below it is checking nothing")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
