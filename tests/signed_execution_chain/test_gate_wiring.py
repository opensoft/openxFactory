"""The short-chain gate's INVOCATION, pinned as a test rather than as a comment.

WHY THIS FILE EXISTS, and it is the same instrument
`tests/openxwallet_consumer_gate/test_gate_invocation.py` is. The reader runs its
whole-tree sweep only `if args.path is not None`, and it holds carried wallet
blocks to the SHIPPED shapes only when `--require-pinned-wallet-vocabulary` makes
an unreachable pin a refusal. A gate invoked with no argument, or without the
flag, goes green having checked strictly less than the check's name claims —
which is the vacuous-pass class, and a comment in the workflow protects nothing
against it. This module is collected by the REQUIRED `pytest-suite` job, so a
change to the invocation cannot land without a required check going red.

WHAT IS NOT PINNED HERE, deliberately: whether the check is REQUIRED. It is not,
and no test in this repository can make it so. That is `tasks.md` 4.5, an
OPERATOR act whose evidence is a live ruleset read — and until it happens this
capability confers and refuses nothing, which its own conformance declaration
states in the present tense.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "signed-execution-chain-gate.yml"

#: The token a branch ruleset would pin. It is the JOB ID, never the filename.
REQUIRED_JOB_ID = "signed-execution-chain-gate"

# THE INVOCATION IS PINNED BY THE ASSERTIONS BELOW AND BY NOTHING ELSE. An
# earlier draft also held it as a literal constant here, which Copilot flagged as
# dead code: it was never compared against anything, so it was a SECOND statement
# of the invocation that could drift from the first silently — which is precisely
# the defect this whole module exists to prevent, one level up. The assertions
# name the three parts that carry meaning (the script, the `.` target, the
# vocabulary flag) rather than a whole line whose shell continuation formatting is
# not itself a governed fact.


def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _steps():
    return _workflow()["jobs"][REQUIRED_JOB_ID]["steps"]


def _step_index(needle: str) -> int:
    """The index of the one step whose `run` contains `needle`.

    NOT `next(...)` WITHOUT A DEFAULT, which Copilot flagged: a bare `next` raises
    `StopIteration` when the workflow changes, and a test that dies with
    `StopIteration` says nothing about WHICH step went missing. This says it."""
    runs = [step.get("run", "") for step in _steps()]
    matches = [index for index, run in enumerate(runs) if needle in run]
    assert len(matches) == 1, (
        f"expected exactly one step whose `run` contains {needle!r}, found "
        f"{len(matches)}; the gate's ordering assertions cannot be evaluated "
        f"until that step exists exactly once")
    return matches[0]


def test_the_workflow_exists_and_declares_exactly_one_job():
    document = _workflow()
    assert list(document["jobs"]) == [REQUIRED_JOB_ID]


def test_the_job_carries_no_display_name():
    """The status check must surface as exactly the job id, because that is the
    literal token a ruleset pins. A `name:` on the job silently de-advises the
    gate — the same rule `openxwallet-consumer-gate.yml` and `pytest-suite.yml`
    each document for themselves."""
    assert "name" not in _workflow()["jobs"][REQUIRED_JOB_ID]


def test_the_gate_runs_on_pull_requests_to_main_and_on_main():
    """PULL REQUESTS ARE WHERE IT GATES; `main` is where its state is visible.
    The aggregation repository learned the second half the hard way: a check that
    runs on pull requests ONLY never reports on `main`, so a breakage surfaces on
    somebody else's pull request and gets blamed on their change."""
    # PyYAML resolves a bare `on:` key to the boolean True (the YAML 1.1 legacy),
    # so the trigger block is read under either spelling rather than assumed.
    document = _workflow()
    triggers = document.get("on", document.get(True))
    assert triggers["pull_request"]["branches"] == ["main"]
    assert triggers["push"]["branches"] == ["main"]


def test_the_reader_is_invoked_over_the_tree_with_the_pinned_vocabulary_required():
    steps = _steps()
    runs = [step.get("run", "") for step in steps]
    walk = [run for run in runs if "validate-signed-execution-chain.py" in run]
    assert len(walk) == 1, "exactly one step walks the chain"
    command = walk[0]
    assert "validate-signed-execution-chain.py ." in command, (
        "the argument must be PRESENT and equal to `.`: the reader runs its "
        "whole-tree sweep only when a path is given")
    assert "--require-pinned-wallet-vocabulary" in command, (
        "without the flag an unreachable pin degrades the carried-block check to "
        "the members this capability restricts, and the gate passes having "
        "validated less than its name claims")
    assert "tee chain-gate.log" in command, (
        "the anti-vacuity step greps this log; without the tee it reads nothing")


def test_the_walk_step_runs_under_pipefail():
    """WITHOUT PIPEFAIL, `tee` RETURNS 0 OVER A FAILING READER.

    The default shell for a `run` step does not set `-o pipefail`; declaring
    `shell: bash` does. This gate pipes the reader's verdict into `tee` so the
    next step can grep it, so without pipefail the job is green whatever the
    reader decided — the vacuous pass this whole module exists to prevent, by the
    one route the command-string assertions cannot see.

    Copilot raised it as a suppressed finding, and it was right that nothing
    pinned it: the workflow already declared `shell: bash`, and removing that line
    left all eight assertions here passing. The in-repo precedent is
    `tests/openxwallet_consumer_gate/test_gate_invocation.py`'s
    `test_the_validator_step_runs_under_pipefail`, which asserts exactly this for
    the wallet gate — so the omission was also a divergence from a rule this
    repository had already written down once."""
    walk = _steps()[_step_index("validate-signed-execution-chain.py")]
    assert walk.get("shell") == "bash", (
        "the walk step must declare `shell: bash` so it runs under `-o pipefail`; "
        "otherwise `| tee chain-gate.log` masks a non-zero reader exit and the "
        "gate passes having refused nothing")
    # `chain-gate.log` is NOT a usable needle here: it appears in the walk step's
    # `tee` and in the grep step's reads, so `_step_index` correctly refuses it as
    # ambiguous — which is the helper doing the job Copilot's other finding asked
    # for. `set -euo pipefail` belongs to the asserting step alone.
    grep = _steps()[_step_index("set -euo pipefail")]
    assert grep.get("shell") == "bash", (
        "the anti-vacuity step's own `set -euo pipefail` needs bash; under the "
        "default shell its greps would run but its `fail()` exits would not be "
        "reached the same way")


def test_the_gate_does_not_pass_strict():
    """`--strict` turns warnings into errors, and this reader emits a STANDING
    warning for as long as it is not itself a required check. Passing `--strict`
    would convert the capability's own honest self-report into a gate that can
    never go green."""
    for step in _steps():
        assert "--strict" not in step.get("run", "")


def test_the_pin_is_verified_before_the_pinned_vocabulary_is_trusted():
    """Order, not merely presence: a carried block validated against an
    UNVERIFIED pin is a check against bytes nobody vouched for. The same ordering
    `openxwallet-consumer-gate.yml` uses."""
    init = _step_index("submodule update --init openXwallet")
    verify = _step_index("verify-openxwallet-pin.py")
    walk = _step_index("validate-signed-execution-chain.py")
    assert init < verify, (
        "the pin verifier recomputes digests against the NESTED checkout, so "
        "running it before the init refuses for its environment rather than for a "
        "finding — the failure mode that trains people to skip a gate")
    assert verify < walk, (
        "the reader must not hold carried blocks to a pin nothing has verified")


def test_the_submodule_init_is_scoped_to_openxwallet():
    """A blanket init would also fetch `installs/omnigent-install`, which nothing
    in this gate reads."""
    runs = " ".join(step.get("run", "")
                    for step in _steps())
    assert "git submodule update --init openXwallet" in runs
    assert "--recursive" not in runs
    assert "submodules: true" not in WORKFLOW.read_text(encoding="utf-8")


def test_the_anti_vacuity_step_asserts_the_gate_actually_walked_something():
    """On the happy path the reader emits no finding, so the proof that it walked
    anything is the conjunction of notes it DOES produce. Each grep below
    corresponds to a note `test_chain_reader.py` proves the reader still emits;
    together they are what stops a green check from proving nothing."""
    runs = " ".join(step.get("run", "")
                    for step in _steps())
    for probe in ("pinned openXwallet vocabulary read from",
                  "self-test:",
                  "closed refusal codes red-proven",
                  "repo scan"):
        assert probe in runs, probe
    assert "ERROR \\[" in runs, (
        "the step must also fail on a refusal in the log, not only on a missing "
        "note")
