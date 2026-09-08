"""The factory-identity reader's place in the REQUIRED check, pinned as a test.

WHY THIS FILE EXISTS. Task 2.6 of the ratified change `add-cpc-clearing-boundary`
requires the factory-identity register reader to run inside the REQUIRED
`wallet-validation` check "with a POSITIVE log conjunction — a green check that
never opened the register must be impossible". A comment in the workflow protects
neither half: not that the step exists, and not that its assertion is positive.
This module is collected by the REQUIRED `pytest-suite` job, so removing the
step, dropping its argument, or weakening its assertion to a mere
absence-of-findings cannot land without a second required check going red.

It is the same instrument, and the same argument, as
`tests/openxwallet_consumer_gate/test_gate_invocation.py`, which pins the intake
register's half of the same job.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "openxwallet-consumer-gate.yml"
VALIDATOR = REPO_ROOT / "scripts" / "validate-factory-identity.py"

REQUIRED_JOB_ID = "wallet-validation"
READER_COMMAND = "python3 scripts/validate-factory-identity.py ."
READER_RUN = f"{READER_COMMAND} | tee factory-identity-gate.log"
SCOPED_INIT_RUN = "git submodule update --init openXwallet"
PIN_VERIFY_RUN = "python3 scripts/verify-openxwallet-pin.py"


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert WORKFLOW.is_file()
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def runs(workflow: dict) -> list[str]:
    return [step["run"] for step in workflow["jobs"][REQUIRED_JOB_ID]["steps"]
            if "run" in step]


@pytest.fixture(scope="module")
def assertion(runs: list[str]) -> str:
    found = [r for r in runs
             if "factory-identity-gate.log" in r
             and "validate-factory-identity.py" not in r]
    assert len(found) == 1, (
        "the gate must carry exactly one factory-identity ASSERTION step "
        "reading the reader's log")
    # The step's body is a set of grep -E PATTERNS, so the literals it pins
    # carry regex escapes (`\(s\)`). Comparing against the escaped spelling
    # would make this test a pin on the escaping style rather than on the
    # sentence, so the backslashes are dropped and the SENTENCE is asserted.
    return found[0].replace("\\", "")


def test_the_reader_runs_inside_the_required_token(runs: list[str]) -> None:
    """`wallet-validation` is the REQUIRED token (org ruleset 21538893). A
    second, advisory workflow would leave the register's reader optional on the
    day it matters."""
    invocations = [r for r in runs if "validate-factory-identity.py" in r]
    assert len(invocations) == 1, (
        f"exactly one step may invoke the factory-identity reader; found "
        f"{invocations}")
    assert invocations[0] == READER_RUN, (
        f"the invocation must be exactly {READER_RUN!r} — the argument must be "
        f"PRESENT and equal to `.` (a run with no target reads no register), "
        f"and the `tee` is what feeds the assertion step. Found "
        f"{invocations[0]!r}")


def test_the_reader_step_runs_under_pipefail(workflow: dict) -> None:
    """Without pipefail, `tee` returns 0 over a refusing reader."""
    step = next(s for s in workflow["jobs"][REQUIRED_JOB_ID]["steps"]
                if "validate-factory-identity.py" in s.get("run", ""))
    assert step.get("shell") == "bash"


def test_the_reader_runs_after_the_pinned_gitlink_is_initialized(
        runs: list[str]) -> None:
    """ONE DERIVATION, ONE PLACE. The reader imports the pinned openXwallet
    decoders rather than copying them, and REFUSES when the gitlink is absent;
    running it before the init would refuse every time.
    """
    reader = next(i for i, r in enumerate(runs)
                  if "validate-factory-identity.py" in r)
    assert runs.index(SCOPED_INIT_RUN) < reader
    assert runs.index(PIN_VERIFY_RUN) < reader, (
        "the pin must be verified before a reader that imports from the pinned "
        "tree is trusted")


def test_the_assertion_is_positive_and_not_merely_an_absence(
        assertion: str) -> None:
    """On the happy path the reader emits no finding, so 'no factory-identity
    finding' alone is satisfied by never having opened the register. The
    conjunction is what proves it ran."""
    assert "factory-identity register read: "\
           "governance/factory-identity/register.yaml" in assertion
    assert "active origin row(s) over" in assertion
    assert "disjointness holds against governance/review-authority/" in assertion
    assert "0 shared" in assertion, (
        "the assertion must pin the count of SHARED identifiers at zero; "
        "asserting only that the disjointness note appeared would be satisfied "
        "by a note reporting an overlap")
    assert "[factory-identity-" in assertion, (
        "the assertion must also refuse any factory-identity-* finding code")


def test_the_assertion_pins_the_row_count_literally(assertion: str) -> None:
    """A wildcard would let a register that lost its only row pass the positive
    assertion and confer nothing. One originating repository is registered
    today; a second must be a deliberate edit here beside the register edit."""
    assert "1 active origin row(s) over 1 originating repository(ies)" \
        in assertion


def test_the_reader_derives_nothing_of_its_own() -> None:
    """The rule the whole design rests on, asserted over the source: no second
    base58 alphabet, no second fingerprint spelling, no `hashlib.sha256` used to
    MAKE a fingerprint rather than to compare one.

    The single encoder the reader does own (`b58encode`, for the mint helper) is
    permitted precisely because every value it produces is round-tripped through
    the PINNED decoder before it is printed — which the module docstring states
    and `test_derive_reproduces_a_known_minted_key` proves against a live key.
    """
    text = VALIDATOR.read_text(encoding="utf-8")
    assert "load_pinned_reader" in text
    assert 'pinned.decode_public_key_multibase' in text
    assert 'pinned.fingerprint_of_public_key' in text
    assert text.count('"sha256:" + hashlib') == 0, (
        "the fingerprint spelling must come from the pinned reader, never from "
        "a second implementation here")
    assert "raise SystemExit(" in text, (
        "the reader must REFUSE when the pinned reader is absent rather than "
        "fall back to arithmetic of its own")
