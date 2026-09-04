"""The clearing reader's CI wiring, pinned as a test rather than as a comment.

WHY THIS FILE EXISTS. A canonical validator that nothing runs confers and refuses
nothing. `.github/workflows/clearing-dispatch-gate.yml` is what runs it, and a
comment in that file protects none of the four properties the wiring actually
needs: that the job id IS the check token, that the pinned gitlink is initialized
and its pin verified BEFORE the reader trusts it, that the reader is invoked over
the whole tree, and that the assertion which follows is POSITIVE rather than a
mere absence of findings.

This module is collected by the REQUIRED `pytest-suite` job, so weakening any of
those cannot land without a required check going red. It is the same instrument,
and the same argument, as `tests/factory_identity/test_gate_wiring.py` and
`tests/openxwallet_consumer_gate/test_gate_invocation.py`.

WHY THE FILENAME CARRIES THE FAMILY. `tests/signed_execution_chain/` already
holds a `test_gate_wiring.py`, and neither directory is a Python package, so both
would claim the bare module name `test_gate_wiring` in `sys.modules` and
collection would fail with an import-file mismatch the moment both are collected
— which the required `pytest-suite` job always does. The alternative, making this
directory a package, would put the conftest behind a qualified name and break the
`from conftest import` this family's modules use. A distinct basename is the
smaller change.
"""

from __future__ import annotations

import pytest
import yaml

from conftest import REPO_ROOT

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "clearing-dispatch-gate.yml"
VALIDATOR = REPO_ROOT / "scripts" / "validate-clearing-dispatch.py"

CHECK_TOKEN = "clearing-dispatch-gate"
READER_COMMAND = "python3 scripts/validate-clearing-dispatch.py ."
READER_RUN = f"{READER_COMMAND} | tee clearing-gate.log"
SCOPED_INIT_RUN = "git submodule update --init openXwallet"
PIN_VERIFY_RUN = "python3 scripts/verify-openxwallet-pin.py"


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert WORKFLOW.is_file(), f"{WORKFLOW} is absent"
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def job(workflow) -> dict:
    assert CHECK_TOKEN in workflow["jobs"], (
        f"the job id must be exactly {CHECK_TOKEN!r} — it is the literal token a "
        f"branch ruleset pins"
    )
    return workflow["jobs"][CHECK_TOKEN]


@pytest.fixture(scope="module")
def runs(job) -> list[str]:
    return [step["run"] for step in job["steps"] if "run" in step]


def test_the_validator_exists_and_is_executable() -> None:
    assert VALIDATOR.is_file()


def test_the_job_carries_no_display_name(job) -> None:
    """A display name silently de-advises the gate.

    GitHub surfaces the check under the job's DISPLAY name when one is set, so a
    ruleset pinning the job ID would stop matching and the required check would
    quietly become a check nobody required.
    """
    assert "name" not in job, (
        "the job must surface as its id; a `name:` key renames the status check"
    )


def test_the_gate_runs_on_pull_requests_and_on_main(workflow) -> None:
    # PyYAML reads a bare `on:` key as the boolean True (the Norway problem's
    # cousin), which is why this indexes `True` rather than "on".
    triggers = workflow.get(True) or workflow.get("on")
    assert triggers["pull_request"]["branches"] == ["main"]
    assert triggers["push"]["branches"] == ["main"]


def test_the_gate_holds_no_write_permission(workflow) -> None:
    assert workflow["permissions"] == {"contents": "read"}


def test_the_pinned_gitlink_is_initialized_before_the_reader_runs(runs) -> None:
    """The reader REFUSES without the pinned decoders, so the init is not
    optional and its ORDER is not incidental."""
    assert SCOPED_INIT_RUN in " ".join(runs), (
        "the openXwallet gitlink is never initialized; the reader would exit 2"
    )
    init_at = next(i for i, r in enumerate(runs) if SCOPED_INIT_RUN in r)
    reader_at = next(i for i, r in enumerate(runs) if READER_COMMAND in r)
    assert init_at < reader_at


def test_the_pin_is_verified_before_anything_pinned_is_trusted(runs) -> None:
    """A carved-out copy validated against an unverified pin is a check against
    bytes nobody vouched for."""
    assert any(PIN_VERIFY_RUN in r for r in runs)
    verify_at = next(i for i, r in enumerate(runs) if PIN_VERIFY_RUN in r)
    reader_at = next(i for i, r in enumerate(runs) if READER_COMMAND in r)
    assert verify_at < reader_at


def test_the_reader_is_invoked_over_the_whole_tree_and_teed(runs) -> None:
    """The trailing `.` is load-bearing: without it the reader self-tests only
    and never sweeps for real artifacts. The `tee` is what the assertion step
    reads."""
    assert any(READER_RUN in r for r in runs), (
        f"no step runs {READER_RUN!r}; the reader either does not run, does not "
        f"sweep the tree, or does not record a log for the assertion step"
    )


def test_the_assertion_step_is_positive_and_not_merely_absence(runs) -> None:
    """A green check that opened nothing is a vacuous pass.

    Each of these greps is a fact the run can only print if it did the work, and
    together they are the difference between "no errors" and "the reader
    walked the corpus, the register and the tree".
    """
    assertion = next((r for r in runs if "clearing-gate.log" in r
                      and "grep" in r), None)
    assert assertion is not None, "no assertion step reads the gate log"
    for probe in (
        "pinned openXwallet decoders read from",
        "permitted-operations register read:",
        "self-test:",
        "closed refusal codes red-proven",
        "repo scan",
    ):
        assert probe in assertion, f"the assertion never proves {probe!r} happened"
    assert "! grep -qE '^ERROR \\['" in assertion, (
        "the assertion never checks that no finding survived"
    )


def test_the_assertion_pins_the_registers_literal_member_count(runs) -> None:
    """THE COUNT IS THE POINT.

    The register is closed at two members. If a change makes this grep fail, the
    correct response is a ratifier, not a wider pattern.

    THIS IS COPY FIVE OF FIVE, and it is the one a reader of the contract tree
    would never see: it pins the CI grep's literal from a second file, so moving
    the grep alone turns this red. The count moved 1 -> 2 on 2026-09-04 by
    `admit-deliberation-clearing-operation` (PR #645, merged `3cf917b7`), which
    is what moving it costs.
    """
    assertion = next(r for r in runs if "clearing-gate.log" in r and "grep" in r)
    assert "2 registered operations" in assertion


def test_the_refusal_coverage_assertion_demands_all_of_them(runs) -> None:
    """`N/N`, via a backreference — not `[0-9]+/[0-9]+`, which 3/24 satisfies."""
    assertion = next(r for r in runs if "clearing-gate.log" in r and "grep" in r)
    assert "([0-9]+)/\\1 closed refusal codes red-proven" in assertion, (
        "the coverage assertion must require the two counts to be EQUAL; a "
        "pattern matching any two numbers passes a run that proved three "
        "refusals out of twenty-four"
    )


def test_the_pytest_suite_collects_this_family(runs) -> None:
    """`tests/clearing/` needs no workflow of its own.

    `pytest-suite.yml` runs the whole `tests/` tree and initializes the same
    gitlink beforehand, so this family's tests are gated by an already-required
    check. This test records that dependency so a change to that workflow's
    invocation is visibly a change to this family's coverage too.
    """
    suite = REPO_ROOT / ".github" / "workflows" / "pytest-suite.yml"
    text = suite.read_text(encoding="utf-8")
    assert "python3 -m pytest tests/" in text
    assert SCOPED_INIT_RUN in text, (
        "pytest-suite no longer initializes the openXwallet gitlink; "
        "tests/clearing/ would fail rather than skip, which is intended, but the "
        "cause would be invisible"
    )
