"""The aggregation root-gitlink parity check's INVOCATION, pinned as a test.

WHY THIS FILE EXISTS (`split-openxwallet-repo` task 9.4, design D11). The
invariant is root-gitlink-equals-nested-gitlink: the openXwallet revision the
xFactory aggregation records must be the revision openxFactory consumes.
openxFactory's own consumer gate cannot check it — it never sees the
aggregation's root gitlink — so the check runs from the aggregation's doc-health
lane, whose `prepare` job is the ONLY CI that initializes both gitlinks. But the
lane is a REUSABLE workflow living here, in openxFactory, while its caller lives
in `opensoft/xFactory`; nothing in that caller's repository can hold this file,
and nothing in this repository runs the lane. A comment would protect neither.

This module is collected by the REQUIRED `pytest-suite` job, so removing the
step, dropping `--aggregation-root`, or moving the invocation ahead of the
submodule init cannot land without a required check going red. It is the same
instrument, and the same argument, as
`tests/openxwallet_consumer_gate/test_gate_invocation.py`: a governed invocation
is pinned where a required check reads it.

WHAT IS PINNED, AND WHY EACH PART:

  * the COMMAND, exactly — one implementation and one refusal vocabulary. D11
    rejected a second script in xFactory, which has no validator convention of
    its own and would drift a duplicate refusal set. `--aggregation-root` is a
    MODE of this repository's verifier, and the flag's absence would silently
    reduce the step to the nested-only check the consumer gate already runs.

  * the ORDER — after "Init governed submodules only". `verify()` runs first
    inside the tool and recomputes the eight digests against the NESTED
    checkout; invoked before the init it would refuse
    `pin-submodule-uninitialized` on every nightly, which is a gate that fails
    for its environment rather than for a finding, and the failure mode that
    trains people to skip a gate.

  * the GUARD — the aggregation's openxFactory pin bump and its own root gitlink
    land in ONE pull request (P4, after P3). Before that bump openxFactory
    declares no `openXwallet` gitlink at the pinned revision and there is
    nothing to compare, so the step must skip rather than fail the nightly for a
    deploy ordering. AFTER the bump the guard is satisfied and the check is
    fail-closed: an aggregation that records no root gitlink refuses as
    `pin-member-missing`.

  * that it is in `prepare` and NOT in `finalize` — prepare runs first and its
    failure fails the whole reusable call, so a second invocation would only add
    a second place for the guard to drift.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LANE = REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml"

STEP_NAME = "Verify openXwallet root-gitlink parity"
INIT_STEP_NAME = "Init governed submodules only"

#: The command half. `--aggregation-root .` is the mode, and `.` is the
#: aggregation checkout the reusable workflow runs in.
PARITY_COMMAND = ("python3 openxFactory/scripts/verify-openxwallet-pin.py "
                  "--aggregation-root .")

#: The ordering guard, byte for byte the one the nested init already uses.
GUARD = ("git -C openxFactory config --file .gitmodules "
         "--get submodule.openXwallet.path")


@pytest.fixture(scope="module")
def lane() -> dict:
    assert LANE.is_file(), f"{LANE} is missing"
    return yaml.safe_load(LANE.read_text(encoding="utf-8"))


def _steps(lane: dict, job: str) -> list[dict]:
    return lane["jobs"][job]["steps"]


def _named(lane: dict, job: str, name: str) -> dict:
    for step in _steps(lane, job):
        if step.get("name") == name:
            return step
    raise AssertionError(f"{job} has no step named {name!r}")


def _flat(run: str) -> str:
    """`run` with YAML line continuations and indentation collapsed, so a
    reflowed multi-line command still matches the command it is."""
    return " ".join(run.replace("\\\n", " ").split())


def test_the_parity_step_exists_in_prepare(lane):
    step = _named(lane, "prepare", STEP_NAME)
    assert "run" in step, "the parity check is a run step, not an action"


def test_the_parity_step_invokes_the_verifier_in_aggregation_root_mode(lane):
    run = _flat(_named(lane, "prepare", STEP_NAME)["run"])
    assert PARITY_COMMAND in run, (
        f"the parity step no longer runs {PARITY_COMMAND!r}; a missing "
        "--aggregation-root silently reduces it to the nested-only check the "
        "consumer gate already runs")


def test_the_parity_step_is_guarded_on_the_nested_declaration(lane):
    run = _flat(_named(lane, "prepare", STEP_NAME)["run"])
    assert GUARD in run, (
        "the parity step lost its ordering guard; before the aggregation bumps "
        "its openxFactory pin there is no nested gitlink to compare and an "
        "unguarded invocation fails the nightly for a deploy ordering")
    assert "skipping the root-gitlink parity check" in run, (
        "the skip arm must SAY it skipped — a silent skip is indistinguishable "
        "from a pass")


def test_the_parity_step_runs_after_the_submodule_init(lane):
    names = [s.get("name") or s.get("uses") for s in _steps(lane, "prepare")]
    assert names.index(STEP_NAME) > names.index(INIT_STEP_NAME), (
        "verify() recomputes the eight digests against the NESTED checkout; "
        "invoked before the init it refuses pin-submodule-uninitialized on "
        "every nightly")


def test_the_parity_step_is_unconditional_within_prepare(lane):
    step = _named(lane, "prepare", STEP_NAME)
    assert "if" not in step, (
        "the parity check is offline and instant, and a governance gate that "
        "readiness-only mode switches off is a gate with a hole in it; the "
        "P3/P4 ordering is handled by the in-step guard, not by a job condition")


def test_the_parity_step_is_not_duplicated_in_finalize(lane):
    names = [s.get("name") for s in _steps(lane, "finalize")]
    assert STEP_NAME not in names, (
        "prepare runs first and its failure fails the whole reusable call; a "
        "second invocation only adds a second place for the guard to drift")


def test_the_verifier_supports_the_mode_the_lane_invokes():
    """The other half of the wiring: the flag the workflow passes is a flag the
    script has. A pinned invocation of an option that was renamed away is a
    green test over a red gate."""
    script = (REPO_ROOT / "scripts" / "verify-openxwallet-pin.py").read_text(
        encoding="utf-8")
    assert '"--aggregation-root"' in script
    assert "def verify_aggregation(" in script
