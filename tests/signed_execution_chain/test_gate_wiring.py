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

#: The reader, its target, and the flag that stops it degrading in silence.
INVOCATION = ("python3 scripts/validate-signed-execution-chain.py . \\\n"
              "  --require-pinned-wallet-vocabulary")


def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


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
    steps = _workflow()["jobs"][REQUIRED_JOB_ID]["steps"]
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


def test_the_gate_does_not_pass_strict():
    """`--strict` turns warnings into errors, and this reader emits a STANDING
    warning for as long as it is not itself a required check. Passing `--strict`
    would convert the capability's own honest self-report into a gate that can
    never go green."""
    for step in _workflow()["jobs"][REQUIRED_JOB_ID]["steps"]:
        assert "--strict" not in step.get("run", "")


def test_the_pin_is_verified_before_the_pinned_vocabulary_is_trusted():
    """Order, not merely presence: a carried block validated against an
    UNVERIFIED pin is a check against bytes nobody vouched for. The same ordering
    `openxwallet-consumer-gate.yml` uses."""
    runs = [step.get("run", "")
            for step in _workflow()["jobs"][REQUIRED_JOB_ID]["steps"]]
    verify = next(index for index, run in enumerate(runs)
                  if "verify-openxwallet-pin.py" in run)
    init = next(index for index, run in enumerate(runs)
                if "submodule update --init openXwallet" in run)
    walk = next(index for index, run in enumerate(runs)
                if "validate-signed-execution-chain.py" in run)
    assert init < verify < walk


def test_the_submodule_init_is_scoped_to_openxwallet():
    """A blanket init would also fetch `installs/omnigent-install`, which nothing
    in this gate reads."""
    runs = " ".join(step.get("run", "")
                    for step in _workflow()["jobs"][REQUIRED_JOB_ID]["steps"])
    assert "git submodule update --init openXwallet" in runs
    assert "--recursive" not in runs
    assert "submodules: true" not in WORKFLOW.read_text(encoding="utf-8")


def test_the_anti_vacuity_step_asserts_the_gate_actually_walked_something():
    """On the happy path the reader emits no finding, so the proof that it walked
    anything is the conjunction of notes it DOES produce. Each grep below
    corresponds to a note `test_chain_reader.py` proves the reader still emits;
    together they are what stops a green check from proving nothing."""
    runs = " ".join(step.get("run", "")
                    for step in _workflow()["jobs"][REQUIRED_JOB_ID]["steps"])
    for probe in ("pinned openXwallet vocabulary read from",
                  "self-test:",
                  "closed refusal codes red-proven",
                  "repo scan"):
        assert probe in runs, probe
    assert "ERROR \\[" in runs, (
        "the step must also fail on a refusal in the log, not only on a missing "
        "note")
