"""Static validation of openxFactory's advisory Merge Master review lane.

Nothing here executes the workflow. It parses the YAML, checks the embedded
shell with `bash -n`, and asserts the properties this lane's whole value rests
on — that the pinned decision core cannot drift silently, and that the lane
CANNOT approve anything.

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

# READ-ONLY, stated exactly. Any scope beyond these two is a scope that could
# begin to approve, merge, or annotate.
EXPECTED_PERMISSIONS = {"contents": "read", "pull-requests": "read"}

PINNED_REPOSITORY = "opensoft/codexFactory"
FLOOR_REPOSITORY = "opensoft/openxFactory"

SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
CORE_COMMIT_RE = re.compile(
    r'^core_commit:[ \t]*"?([0-9a-f]{40})"?[ \t]*$', re.MULTILINE)

# THE APPROVAL DENYLIST. Every string here is a way this workflow could acquire
# the authority it is specified NOT to have. The spec says the absence is
# STRUCTURAL — these steps are absent, not disabled by a condition — and a
# condition is exactly what a later edit would reach for first, so the check is
# over the file TEXT rather than over the parsed graph.
APPROVAL_SHAPED = (
    "MERGE_MASTER_APP_ID",
    "MERGE_MASTER_APP_KEY",
    "gh pr review",
    "gh pr merge",
    "gh api --method POST",
    "/reviews",
    "enablePullRequestAutoMerge",
    "--auto",
    "event=APPROVE",
    '"event": "APPROVE"',
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
            "scripts/merge_master/openxfactory-review-authority-floor.yaml",
            paths,
            "the pin must name the floor document, so a re-point ceremony "
            "knows what to re-verify")

    def test_the_pin_records_its_divergence_from_the_aggregation_pin(self) -> None:
        """A forced divergence is still a divergence, and must be declared."""
        pin = yaml.safe_load(self.pin_text)
        lockstep = pin.get("lockstep") or {}
        self.assertEqual(lockstep.get("status"), "diverged")
        self.assertTrue(str(lockstep.get("reason") or "").strip(),
                        "a diverged pin must state WHY")
        self.assertTrue(str(lockstep.get("obligation") or "").strip(),
                        "a diverged pin must state the convergence obligation")
        self.assertEqual(len(lockstep.get("diverged_from") or []), 2,
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

    def test_the_caller_contains_no_approval_shaped_step(self) -> None:
        """FR-007: the absence is structural, so it is checked over the text."""
        for needle in APPROVAL_SHAPED:
            self.assertNotIn(
                needle, self.caller_text,
                "%r appears in the advisory caller. This lane must be unable "
                "to approve, merge, or enable auto-merge — the steps are "
                "absent, not disabled." % needle)

    def test_the_caller_ships_no_envelope_instance(self) -> None:
        """No enrolled candidate class means no envelope config, at all."""
        envelope = REPO_ROOT / ".github/merge-approval-envelope.yml"
        self.assertFalse(
            envelope.exists(),
            "an envelope instance implies an enrolled candidate class. The "
            "schema requires a non-empty `candidates` list and the "
            "gate_rules_council has defined no OPERABLE class for this "
            "repository — a record exists (2026-08-28) and REFUSED the class "
            "put to it, so add-substantive-review-lane task 3.2 stays OPEN.")

    def test_the_caller_evaluates_this_repositorys_floor(self) -> None:
        self.assertIn(
            FLOOR_REPOSITORY, self.caller_text,
            "the caller must name the repository whose gate floor it evaluates")
        self.assertIn("repository_floor", self.caller_text)

    def test_the_caller_opts_into_the_floor_reachability_check(self) -> None:
        """`tree_paths` is opt-in; a floor matching nothing must not be silent."""
        self.assertIn(
            "tree_paths=tree", self.caller_text,
            "the core's reachability check is opt-in precisely because a floor "
            "usually names another repository's paths. Here we ARE that "
            "repository, so an unreachable floor path must be a named failure.")

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
        cls.caller_text = CALLER.read_text(encoding="utf-8")
        cls.pin_text = PIN.read_text(encoding="utf-8")

    def test_the_unmutated_pair_is_a_positive_first(self) -> None:
        """Ordering guard: a fixture that never passes proves nothing."""
        document = caller_document(self.caller_text)
        self.assertEqual(pinned_ref(document),
                         declared_core_commit(self.pin_text))

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

    def test_an_approval_shaped_addition_is_visible(self) -> None:
        mutated = self.caller_text + "\n# gh pr review --approve\n"
        hits = [needle for needle in APPROVAL_SHAPED if needle in mutated]
        self.assertIn("gh pr review", hits,
                      "the approval denylist must catch a review submission")

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
