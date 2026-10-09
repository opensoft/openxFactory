"""T011: the `council-convening-gate` workflow's wiring, pinned as a test.

A validator that nothing runs confers and refuses nothing, and a comment in a
workflow protects none of the properties the wiring needs. This module is
collected by the required `pytest-suite` job, so weakening the gate cannot land
without a required check going red. It is the instrument
`tests/clearing/test_clearing_gate_wiring.py` is for its gate.

The strongest pin is the last one: the assertion step's own `grep -qE`
patterns are read out of the workflow and applied to the validator's REAL
output, so a note the validator stops printing, or a grep that stops matching
what it prints, fails here first.
"""

from __future__ import annotations

import re

import pytest
import yaml

from .conftest import REPO_ROOT, WORKFLOW, run_validator

CHECK_TOKEN = "council-convening-gate"
LOCK_INSTALL = ("pip install --require-hashes --only-binary :all: "
                "-r requirements/hermes-runtime-contracts.lock")
VALIDATOR_RUN = "python3 scripts/validate-council-convening.py"
LOG = "council-convening-gate.log"

PHASE_1_NOTE_PREFIXES = [
    "schemas loaded:",
    "protocol registry closed:",
    "corpus index:",
    "vectors adjudicated:",
    "refusal codes probed:",
    "finding codes probed:",
    "requirements probed:",
    "generator reproduced corpus byte-for-byte",
]


@pytest.fixture(scope="module")
def text() -> str:
    assert WORKFLOW.is_file(), f"{WORKFLOW} is absent"
    return WORKFLOW.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def workflow(text) -> dict:
    return yaml.safe_load(text)


@pytest.fixture(scope="module")
def job(workflow) -> dict:
    assert CHECK_TOKEN in workflow["jobs"], (
        f"the job id must be exactly {CHECK_TOKEN!r}: it is the literal token a "
        f"branch ruleset would pin")
    return workflow["jobs"][CHECK_TOKEN]


@pytest.fixture(scope="module")
def runs(job) -> list[str]:
    return [step["run"] for step in job["steps"] if "run" in step]


@pytest.fixture(scope="module")
def assertion(runs) -> str:
    step = next((r for r in runs if LOG in r and "grep" in r), None)
    assert step is not None, "no assertion step reads the gate log"
    return step


def test_the_job_carries_no_display_name(job):
    assert "name" not in job, "a `name:` key renames the status check"


def test_the_gate_runs_on_pull_requests_and_on_main(workflow):
    # PyYAML reads a bare `on:` key as the boolean True.
    triggers = workflow.get(True) or workflow.get("on")
    assert triggers["pull_request"]["branches"] == ["main"]
    assert triggers["push"]["branches"] == ["main"]


def test_the_gate_holds_no_write_permission_and_no_identity(workflow, job, text):
    assert workflow["permissions"] == {"contents": "read"}
    assert "permissions" not in job
    assert "id-token" not in text, "the gate needs no OIDC token"
    assert "secrets." not in text and "secrets[" not in text, (
        "the gate reads no secret")


def _joined(run: str) -> str:
    """A run script with its backslash continuations joined, whitespace folded."""
    return " ".join(run.replace("\\\n", " ").split())


def test_the_gate_installs_the_hash_locked_inputs_as_wheels_only(runs):
    """`--require-hashes` binds WHICH artifact may be installed; `--only-binary
    :all:` binds WHAT KIND, so no sdist's setup script runs in a gate (Sonar
    `githubactions:S8541`; `former-id-arrival-gate.yml`'s rule). Measured: the
    lock resolves to 17 wheels and 0 sdists on Python 3.12."""
    joined = [_joined(r) for r in runs]
    assert any(LOCK_INSTALL in r for r in joined), (
        "the gate must install the ratified validator inputs with --require-hashes "
        "and --only-binary :all:")
    install_at = next(i for i, r in enumerate(joined) if LOCK_INSTALL in r)
    run_at = next(i for i, r in enumerate(joined) if VALIDATOR_RUN in r)
    assert install_at < run_at
    installs = [r for r in joined if "pip install" in r]
    assert installs == [LOCK_INSTALL], installs


def test_the_gate_runs_the_self_test_and_keeps_its_log(runs):
    step = next((r for r in runs if VALIDATOR_RUN in r and f"tee {LOG}" in r), None)
    assert step is not None, f"no step runs {VALIDATOR_RUN!r} teed to {LOG}"
    invocation = step.split(VALIDATOR_RUN, 1)[1].split("|", 1)[0].strip()
    assert invocation == "", (
        "the gate runs the SELF-TEST, with no subcommand; a `check` or `corpus` "
        "run would adjudicate nothing")


def test_the_assertion_step_requires_every_phase_1_note(assertion):
    for prefix in PHASE_1_NOTE_PREFIXES:
        assert f"^note  {prefix}" in assertion.replace("\\(", "(").replace("\\)", ")"), (
            f"the assertion never proves {prefix!r}")
    assert "! grep -qE '^ERROR \\['" in assertion


#: The proof-of-work note Phase 2 adds (T032), asserted with its literal counts.
PHASE_2_NOTES = [
    "^note  predicate registry closed: 2 predicates, 2 input contracts$",
]


def test_the_assertion_step_requires_the_phase_2_note(assertion):
    for pattern in PHASE_2_NOTES:
        assert f"grep -qE '{pattern}' {LOG}" in assertion, (
            f"the assertion never proves {pattern!r}")


def test_the_requirements_assertion_names_the_coverage_floor(assertion):
    """The floor is written into the grep, so raising it cannot pass silently."""
    from scripts.council_convening import generate

    floor = ", ".join(generate.COVERAGE_FLOOR)
    assert f"requirements probed: ([1-9][0-9]*)/\\1 \\({floor}\\)$" in assertion


def test_the_assertion_step_requires_the_full_coverage_note(assertion):
    """Phase 6 (T058, T059): the floor is the full FR-001 to FR-012 and SC-001 to
    SC-003, and the gate proves the validator said so."""
    pattern = "^note  coverage floor full: FR-001 to FR-012, SC-001 to SC-003$"
    assert f"grep -qE '{pattern}' {LOG}" in assertion, (
        "the assertion never proves the full coverage floor")


def test_the_coverage_assertions_demand_all_of_them(assertion):
    """`N/N` via a backreference: `[0-9]+/[0-9]+` would pass 3/24, and
    `([0-9]+)/\\1` would pass `0/0`, a run that walked nothing."""
    for label in ("vectors adjudicated", "refusal codes probed",
                  "finding codes probed", "requirements probed"):
        assert f"{label}: ([1-9][0-9]*)/\\1" in assertion, label
    patterns = re.findall(r"grep -qE '([^']+/\\1[^']*)'", assertion)
    assert len(patterns) == 4, patterns
    for pattern in patterns:
        label = pattern.split(":")[0].lstrip("^")
        assert not re.search(pattern, f"{label}: 0/0"), pattern
        assert not re.search(pattern, f"{label}: 3/24"), pattern
        assert not re.search(pattern, f"{label}: 07/07"), pattern


def test_every_required_grep_is_followed_by_fail(assertion):
    """A grep whose miss is not turned into `fail` would let `set -e` decide,
    and a negated one would not stop the step at all."""
    joined = assertion.replace("\\\n", " ")
    greps = re.findall(r"(?:!\s+)?grep -qE '[^']+' " + re.escape(LOG) + r"\s*(\S+)", joined)
    assert len(greps) >= len(PHASE_1_NOTE_PREFIXES) + 1, greps
    assert set(greps) == {"||"}, greps
    tails = re.findall(re.escape(LOG) + r"\s*\|\|\s*(\S+)", joined)
    assert set(tails) == {"fail"}, tails
    assert "set -euo pipefail" in assertion
    assert "fail() {" in assertion


def test_the_run_steps_use_bash(job):
    """`shell: bash` is what gives the tee pipeline `-o pipefail` on GitHub, so a
    validator that exits non-zero fails its step instead of hiding behind tee."""
    for step in job["steps"]:
        if "run" in step and (VALIDATOR_RUN in step["run"] or LOG in step["run"]):
            assert step.get("shell") == "bash", step.get("name")


def test_the_assertion_greps_match_the_validators_real_output(assertion):
    greps = re.findall(r"(!\s+)?grep -qE '([^']+)' " + re.escape(LOG), assertion)
    required = [pattern for negated, pattern in greps if not negated]
    forbidden = [pattern for negated, pattern in greps if negated]
    assert len(required) >= len(PHASE_1_NOTE_PREFIXES), required
    assert forbidden == ["^ERROR \\["], forbidden
    output = run_validator().stdout
    for pattern in required:
        assert re.search(pattern, output, re.M), (
            f"the gate's grep {pattern!r} does not match the validator's output")
    for pattern in forbidden:
        assert not re.search(pattern, output, re.M), (
            f"the validator's output matches the gate's forbidden grep {pattern!r}")


def test_the_pytest_suite_collects_this_family():
    """The family's tests need no workflow of their own: the required
    `pytest-suite` runs the whole `tests/` tree from the same lock."""
    suite = (REPO_ROOT / ".github" / "workflows" / "pytest-suite.yml").read_text(
        encoding="utf-8")
    assert "python3 -m pytest tests/" in suite
    # The SAME lock, whatever flags beside it: `pytest-suite.yml` still carries
    # the older form without `--only-binary :all:`, and a divergence in a flag
    # is not a divergence in the dependency set.
    assert "pip install --require-hashes -r requirements/hermes-runtime-contracts.lock" in suite
