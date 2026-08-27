"""The consumer gate's invocation, pinned as a test rather than as a comment.

WHY THIS FILE EXISTS. `scripts/validate-openxwallet.py` runs `repo_scan` — and
hence `check_register`, which is where review authority is adjudicated at all —
only ``if args.path is not None``, and `repo_scan` reads the intake register only
``if sweep``, where ``sweep = target.is_dir()``. So a REQUIRED check invoked with
no argument, or with a FILE-valued argument, goes green having opened no
register. That is the vacuous-pass class: a gate whose passing proves nothing.
Before this file, no test in `tests/` referenced any workflow at all.

WHAT IS PINNED, AND WHY IT IS PINNED HERE RATHER THAN IN THE WORKFLOW'S OWN
COMMENT. This module is collected by the REQUIRED `pytest-suite` job, so a change
to the gate's invocation cannot land without a second required check going red.
A comment in the workflow protects nothing.

ON THE TWO RATIFIED SENTENCES ABOUT THE INVOCATION STRING. `tasks.md` 7.13 fixes
the step as ``python3 openXwallet/scripts/validate-openxwallet.py . | tee
wallet-gate.log`` — the `tee` is what the register assertion in the next step
reads. `tasks.md` 7.14 requires one step's ``run`` to be EXACTLY ``python3
openXwallet/scripts/validate-openxwallet.py .``, for the stated reason that the
argument must be "present AND equal to `.`". Both are honoured by pinning the
whole line exactly AND the command half exactly: the assertions below are
strictly stronger than either sentence alone, and neither is weakened.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "openxwallet-consumer-gate.yml"

#: The ratified token the org ruleset pins. It is the JOB ID, never the filename.
REQUIRED_JOB_ID = "wallet-validation"

#: The command half. The argument is present and is exactly `.`.
VALIDATOR_COMMAND = "python3 openXwallet/scripts/validate-openxwallet.py ."

#: The whole ratified line, `tee` included.
VALIDATOR_RUN = f"{VALIDATOR_COMMAND} | tee wallet-gate.log"

PIN_VERIFY_RUN = "python3 scripts/verify-openxwallet-pin.py"
SYNTAX_GATE_RUN = "python3 openXwallet/scripts/wallet-yaml-syntax-gate.py ."
SCOPED_INIT_RUN = "git submodule update --init openXwallet"


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert WORKFLOW.is_file(), (
        f"{WORKFLOW} is missing; the REQUIRED `wallet-validation` token has no "
        f"workflow to report from")
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def gate_job(workflow: dict) -> dict:
    return workflow["jobs"][REQUIRED_JOB_ID]


@pytest.fixture(scope="module")
def runs(gate_job: dict) -> list[str]:
    return [step["run"] for step in gate_job["steps"] if "run" in step]


def test_the_required_token_survives_the_file_rename(workflow: dict) -> None:
    """The ruleset pins a JOB ID. The file moved; the job key did not."""
    assert REQUIRED_JOB_ID in workflow["jobs"], (
        f"`jobs:` must contain the key {REQUIRED_JOB_ID!r} verbatim — org "
        f"ruleset 21538893 requires that token on main and it is the job id, "
        f"not the filename. Found: {sorted(workflow['jobs'])}")


def test_the_gate_job_carries_no_display_name(gate_job: dict) -> None:
    """A display name replaces the token in the check list and de-advises it."""
    assert "name" not in gate_job, (
        "the gate job must carry no `name:` — the status check has to surface "
        "as exactly `wallet-validation`, and a display name silently renames it")


def test_the_gate_runs_on_pull_requests_to_main(workflow: dict) -> None:
    triggers = workflow[True] if True in workflow else workflow["on"]
    assert "pull_request" in triggers
    assert triggers["pull_request"]["branches"] == ["main"]


def test_the_validator_is_invoked_with_the_repository_root_as_its_target(
        runs: list[str]) -> None:
    """The argument is PRESENT and equal to `.`, and the line is pinned whole."""
    invocations = [r for r in runs if "validate-openxwallet.py" in r]
    assert len(invocations) == 1, (
        f"exactly one step may invoke the pinned validator; found "
        f"{len(invocations)}: {invocations}")
    assert invocations[0] == VALIDATOR_RUN, (
        f"the pinned validator's invocation must be exactly {VALIDATOR_RUN!r} — "
        f"the `tee` feeds the register assertion and the `.` is what makes "
        f"`repo_scan` and therefore `check_register` run at all. Found: "
        f"{invocations[0]!r}")
    command = invocations[0].split("|", 1)[0].strip()
    assert command == VALIDATOR_COMMAND, (
        f"the command half must be exactly {VALIDATOR_COMMAND!r}; found "
        f"{command!r}")


def test_the_validator_is_not_invoked_with_strict(runs: list[str]) -> None:
    """Unchanged from `wallet-validation.yml:34`.

    `report()` reds a `--strict` run on WARNINGS, and this gate must red on
    errors only; LedgerxFactory is the consumer that runs `--strict`.
    """
    invocation = next(r for r in runs if "validate-openxwallet.py" in r)
    assert "--strict" not in invocation


def test_the_validator_step_runs_under_pipefail(gate_job: dict) -> None:
    """Without pipefail, `tee` returns 0 over a failing validator.

    The default shell for a `run` step does not set `-o pipefail`; declaring
    `shell: bash` does. A gate that pipes its verdict into `tee` without pipefail
    is green whatever the validator decided.
    """
    step = next(s for s in gate_job["steps"]
                if "validate-openxwallet.py" in s.get("run", ""))
    assert step.get("shell") == "bash", (
        "the validator step must declare `shell: bash` so it runs under "
        "`-o pipefail`; otherwise `| tee` masks a non-zero validator exit")


def test_the_pin_is_verified_before_anything_pinned_is_trusted(
        runs: list[str]) -> None:
    assert PIN_VERIFY_RUN in runs, (
        f"the gate must run {PIN_VERIFY_RUN!r}; without it the pinned reader is "
        f"trusted on the strength of the checkout having succeeded")
    assert runs.index(PIN_VERIFY_RUN) < runs.index(SYNTAX_GATE_RUN)
    assert runs.index(PIN_VERIFY_RUN) < runs.index(VALIDATOR_RUN)


def test_the_syntax_gate_runs_from_the_pin_too(runs: list[str]) -> None:
    """Both readers come from the gitlink; neither is an openxFactory file."""
    assert SYNTAX_GATE_RUN in runs
    assert runs.index(SYNTAX_GATE_RUN) < runs.index(VALIDATOR_RUN)


def test_the_submodule_init_is_scoped_and_not_recursive(runs: list[str]) -> None:
    """`--recursive` would pull every nested submodule of every consumer."""
    inits = [r for r in runs if "submodule update" in r]
    assert inits == [SCOPED_INIT_RUN], (
        f"the gate must init exactly the openXwallet gitlink; found {inits}")
    assert "--recursive" not in " ".join(inits)


def test_the_checkout_does_not_use_a_blanket_submodule_init(
        gate_job: dict) -> None:
    """`submodules: true` would also fetch `installs/omnigent-install`."""
    for step in gate_job["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout"):
            assert not step.get("with", {}).get("submodules"), (
                "the checkout must not declare `submodules:`; the init is a "
                "separate, scoped step")


def test_the_ssh_url_is_rewritten_before_checkout(gate_job: dict) -> None:
    """`insteadOf` after checkout is `insteadOf` too late for a nested clone."""
    steps = gate_job["steps"]
    rewrite = next(i for i, s in enumerate(steps)
                   if "insteadOf" in s.get("run", ""))
    checkout = next(i for i, s in enumerate(steps)
                    if str(s.get("uses", "")).startswith("actions/checkout"))
    assert rewrite < checkout
    token_step = next(i for i, s in enumerate(steps)
                      if s.get("id") == "app-token")
    assert token_step < rewrite


def test_the_register_assertion_is_positive(runs: list[str]) -> None:
    """The conjunction, not merely the absence of a failure.

    `check_register` emits nothing on the happy path, so "no register finding"
    alone is satisfied by never having opened the register.
    """
    assertion = next((r for r in runs if "wallet-gate.log" in r
                      and "validate-openxwallet.py" not in r), None)
    assert assertion is not None, "the gate has no register-assertion step"
    assert "repo scan:" in assertion
    assert "intake register read: governance/review-authority/register.yaml" \
        in assertion
    assert "no intake register at this tree" in assertion
    assert "register-" in assertion


def test_the_retired_workflow_file_is_gone(runs: list[str]) -> None:
    """The rename is a replacement, not an addition.

    Two workflows both declaring `jobs: wallet-validation:` would report the
    same required token twice and the ruleset could be satisfied by whichever
    ran the weaker gate.
    """
    assert not (REPO_ROOT / ".github" / "workflows"
                / "wallet-validation.yml").exists(), (
        "`.github/workflows/wallet-validation.yml` must not survive alongside "
        "`openxwallet-consumer-gate.yml`; both declare the job id the ruleset "
        "pins")


def test_no_openxfactory_owned_wallet_reader_remains(runs: list[str]) -> None:
    """The readers left the repository; only the pinned ones may be invoked."""
    for run in runs:
        assert "scripts/validate-openxwallet.py" not in run.replace(
            "openXwallet/scripts/validate-openxwallet.py", "")
        assert "scripts/wallet-yaml-syntax-gate.py" not in run.replace(
            "openXwallet/scripts/wallet-yaml-syntax-gate.py", "")
    assert not (REPO_ROOT / "scripts" / "validate-openxwallet.py").exists()
    assert not (REPO_ROOT / "scripts" / "wallet-yaml-syntax-gate.py").exists()
