"""The arrival gate's WORKFLOW, pinned as a test rather than as a comment.

WHY THIS FILE EXISTS, and it is the same instrument
`tests/signed_execution_chain/test_gate_wiring.py` and
`tests/clearing/test_clearing_gate_wiring.py` are. Every test in
`test_former_id_arrival.py` exercises the READER — the module and the CLI —
directly, over fixtures built in a `TemporaryDirectory`. None of them ever
reads `.github/workflows/former-id-arrival-gate.yml`, so a later `name:` on
the job, a missing `fetch-depth: 0`, a changed invocation, an added
`--base`/`--head`, or a removed `shell: bash` could silently de-advise or
vacuously pass the check without a single existing test noticing — the
CLI fixtures protect the reader's OWN behaviour, never the file that wires
it into CI. (Copilot, PR #1039.) This module is collected by the REQUIRED
`pytest-suite` job, so a drift in the wiring cannot land without a required
check going red.

WHAT IS NOT PINNED HERE, deliberately: whether the check is REQUIRED. That
is `tasks.md` § 4.5, an operator act in the organization ruleset, and no
test in this repository can assert or protect it — it lives in a ruleset,
not in the tree. What this module pins is the WIRING, so that once § 4.5 is
performed, the required check keeps checking what its name claims.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "former-id-arrival-gate.yml"

#: The token a branch ruleset would pin. It is the JOB ID, never the filename
#: and never the workflow-level `name:` (a cosmetic Actions-tab label this
#: file also carries, and which no ruleset ever reads).
REQUIRED_JOB_ID = "former-id-arrival-gate"


def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _steps():
    return _workflow()["jobs"][REQUIRED_JOB_ID]["steps"]


def _step_index(needle: str) -> int:
    """The index of the one step whose `run` contains `needle`.

    NOT `next(...)` without a default: a bare `next` raises `StopIteration`
    when the workflow changes, and a test that dies with `StopIteration`
    says nothing about WHICH step went missing. This says it.
    """
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
    """The status check must surface as exactly the job id, because that is
    the literal token a ruleset pins. A `name:` on the JOB silently
    de-advises the gate — the same rule `signed-execution-chain-gate.yml`,
    `release-tag-gate.yml`, `openxwallet-consumer-gate.yml` and
    `pytest-suite.yml` each document for themselves, and this workflow's own
    header names too. (The WORKFLOW-level `name:` at the top of the file is
    a different, cosmetic key — an Actions-tab label no ruleset reads — and
    is untouched by this assertion.)
    """
    assert "name" not in _workflow()["jobs"][REQUIRED_JOB_ID]


def test_the_gate_runs_on_pull_requests_to_main_only():
    """PULL REQUESTS ARE WHERE IT GATES, and `push: main` is deliberately
    absent: the gate judges the commits a PULL REQUEST carries, and on
    `main` there is no such range — re-adjudicating history that has
    already landed would red the branch for moves nobody can now repair in
    the commit that made them (the workflow's own header says so). This is
    the ONE required check in this repository's own gate family that does
    NOT also run on `push: main`, so the trigger block is pinned exactly
    rather than by a shape shared with the others.
    """
    # PyYAML resolves a bare `on:` key to the boolean True (the YAML 1.1
    # legacy), so the trigger block is read under either spelling rather
    # than assumed.
    document = _workflow()
    triggers = document.get("on", document.get(True))
    assert triggers == {"pull_request": {"branches": ["main"]}}


def test_the_checkout_step_fetches_full_history():
    """`fetch-depth: 0` IS LOAD-BEARING. On a `pull_request` run the
    checkout is the merge commit GitHub built, whose first parent is the
    base tip and whose second is the pull request head, so `HEAD^1..HEAD^2`
    is this pull request's own commits and nothing else — and a shallow
    checkout cannot resolve either. The reader REFUSES
    `former-id-arrival-unreadable` rather than passing blind when it
    cannot, so a shallow checkout is a silent de-advise and not a visible
    failure: this is the one property a red check cannot itself prove was
    ever wrong.
    """
    checkout = _steps()[0]
    assert checkout["uses"].startswith("actions/checkout@")
    assert checkout.get("with", {}).get("fetch-depth") == 0


def test_the_dependency_install_is_pinned_and_binary_only():
    """`--require-hashes` binds WHICH artifact may be installed, and
    `--only-binary :all:` binds WHAT KIND — the half a hash cannot
    express, so no sdist's `setup.py` runs during the install of a check
    that judges other people's landings. SonarCloud's `githubactions:S8544`
    and `githubactions:S8541` findings on an earlier draft, both taken.
    """
    install = _steps()[_step_index("pip install")]
    command = install["run"]
    assert "--require-hashes" in command
    assert "--only-binary :all:" in command
    assert "requirements/hermes-runtime-contracts.lock" in command


def test_the_reader_is_invoked_over_the_tree_with_no_bypass_flag():
    """`design.md` D3 and `tasks.md` name it: THERE IS NO BYPASS FLAG and
    there is not going to be one (#690). `--base`/`--head` exist so the
    test suite can name a range; CI passes neither, and the gate derives
    the range from the checkout's own event instead.
    """
    judge = _steps()[_step_index("validate-former-id-arrival.py")]
    command = judge["run"]
    assert "validate-former-id-arrival.py ." in command, (
        "the argument must be PRESENT and equal to `.`: without it the CLI "
        "defaults to the current directory too, but naming it here is what "
        "this test pins against a later argument change")
    assert "--base" not in command and "--head" not in command, (
        "CI must derive the range from the pull_request event, never from "
        "a named range — a flag would be the declaration nobody writes")
    assert "tee arrival-gate.log" in command, (
        "the anti-vacuity step greps this log; without the tee it reads "
        "nothing")


def test_the_judge_and_assert_steps_run_under_pipefail():
    """WITHOUT PIPEFAIL, `tee` RETURNS 0 OVER A FAILING READER.

    The judge step pipes the reader's verdict into `tee`, so without
    `shell: bash` (and the pipefail it carries) the job is green whatever
    the reader decided — the vacuous pass this whole module exists to
    prevent, by the one route the command-string assertions in the other
    tests here cannot see. The assert step's OWN `set -euo pipefail` needs
    `shell: bash` for the same reason, one level up: under the default
    shell its greps would still run but its `fail()` exits would not stop
    the step the way `set -e` promises.
    """
    judge = _steps()[_step_index("validate-former-id-arrival.py")]
    assert judge.get("shell") == "bash", (
        "the judge step must declare `shell: bash` so `| tee "
        "arrival-gate.log` masks nothing")
    assertion = _steps()[_step_index("set -euo pipefail")]
    assert assertion.get("shell") == "bash", (
        "the assertion step's own `set -euo pipefail` needs bash to behave "
        "as written")


def test_the_anti_vacuity_step_checks_all_four_conditions():
    """A green check that proves nothing was read is the class of defect
    this step exists to close (the workflow's own header says so). Four
    conditions, and each is named here so a later edit that drops one is
    caught by this test rather than by a corpus this repository is lucky
    enough not to have yet.
    """
    assertion = _steps()[_step_index("set -euo pipefail")]
    command = assertion["run"]
    for probe in (
            "commit\\(s\\) of ",
            "corpus sweep: [0-9]+ active and [0-9]+ archived",
            "0 active and 0 archived",
            "(FAILED|CANNOT RUN):",
    ):
        assert probe in command, probe


def test_the_gate_has_a_bounded_timeout():
    """A hung reader over a corpus this size should fail the job rather
    than run until the runner's own hour-long default does it instead."""
    job = _workflow()["jobs"][REQUIRED_JOB_ID]
    assert isinstance(job.get("timeout-minutes"), int)
    assert job["timeout-minutes"] <= 10
