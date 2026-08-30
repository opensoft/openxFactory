from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Final

import pytest

from tests.council_convening.validator_cli_support import (
    install_single_case,
    json_output,
    run_cli,
    single_case_result,
    temporary_validator_fixture,
)

IMPORTED_FIXTURES: Final = (temporary_validator_fixture,)


def test_help_lists_the_foundation_cli_surface() -> None:
    # Given the validator entrypoint
    # When help is requested
    # Then strict, case selection, and deterministic JSON modes are discoverable.
    result = run_cli("--help")

    assert result.returncode == 0
    assert {"--strict", "--case", "--json"} <= set(result.stdout.split())


def test_empty_index_is_a_deterministic_conformance_mismatch(
    temporary_validator: Path,
) -> None:
    # Given an index with no conformance cases
    index = (
        temporary_validator.parents[1]
        / "contracts/council-convening/fixtures/index.yaml"
    )
    index_text = """schema_version: 1
kind: council-convening-fixture-index
contract_version: 1
cases: []
"""
    _ = index.write_text(
        index_text,
        encoding="utf-8",
    )

    # When the complete corpus is requested twice
    # Then both runs refuse the vacuous corpus as a conformance mismatch.
    first = run_cli("--strict", "--json", validator=temporary_validator)
    second = run_cli("--strict", "--json", validator=temporary_validator)

    assert first.returncode == second.returncode == 1
    assert first.stdout == second.stdout
    payload = json_output(first)
    assert payload["status"] == "fail"
    assert payload["cases"] == []
    assert payload["findings"][0]["code"] == "CC-INDEX-EMPTY"


@pytest.mark.parametrize(
    "conditional_seats",
    [
        """conditional_seats:
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: false
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: true""",
        """conditional_seats:
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: true
          - seat: client-interest
            condition_ref: undeclared-condition
            required: false""",
    ],
)
def test_producer_conditional_evaluations_must_match_the_governed_rule(
    temporary_validator: Path,
    conditional_seats: str,
) -> None:
    fixture_path = (
        "contracts/council-convening/fixtures/positive/conditional-seat-required.yaml"
    )
    fixture = install_single_case(
        temporary_validator, "conditional-seat-required", fixture_path
    )
    text = fixture.read_text(encoding="utf-8")
    original = """conditional_seats:
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: true"""
    _ = fixture.write_text(
        text.replace(original, conditional_seats, 1), encoding="utf-8"
    )

    completed = run_cli("--strict", "--json", validator=temporary_validator)
    payload = json_output(completed)

    assert completed.returncode == 1
    case = single_case_result(payload, "conditional-seat-required")
    assert case["actual_outcome"] == "refuse"
    assert case["finding_codes"] == ["condition_result_drift"]


@pytest.mark.parametrize(
    ("case_id", "required"),
    [
        ("standing-roster", False),
        ("conditional-seat-required", True),
    ],
)
def test_producer_conditional_evaluations_reject_identical_duplicates(
    temporary_validator: Path,
    case_id: str,
    required: bool,
) -> None:
    fixture_path = f"contracts/council-convening/fixtures/positive/{case_id}.yaml"
    fixture = install_single_case(temporary_validator, case_id, fixture_path)
    text = fixture.read_text(encoding="utf-8")
    original = f"""conditional_seats:
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: {str(required).lower()}"""
    duplicate = f"""{original}
          - seat: company-policy
            condition_ref: pull-in-company-policy
            required: {str(required).lower()}"""
    _ = fixture.write_text(text.replace(original, duplicate, 1), encoding="utf-8")

    completed = run_cli("--strict", "--json", validator=temporary_validator)
    payload = json_output(completed)

    assert completed.returncode == 1
    case = single_case_result(payload, case_id)
    assert case["actual_outcome"] == "refuse"
    assert case["finding_codes"] == ["condition_result_drift"]


def test_recorded_standing_seats_must_match_the_governed_rule(
    temporary_validator: Path,
) -> None:
    fixture_path = "contracts/council-convening/fixtures/positive/standing-roster.yaml"
    fixture = install_single_case(temporary_validator, "standing-roster", fixture_path)
    text = fixture.read_text(encoding="utf-8")
    _ = fixture.write_text(
        text.replace(
            "standing_seats: [domain-policy, client-interest, customer-protection]",
            "standing_seats: [bogus-seat]",
            1,
        ),
        encoding="utf-8",
    )

    completed = run_cli("--strict", "--json", validator=temporary_validator)
    payload = json_output(completed)

    assert completed.returncode == 1
    case = single_case_result(payload, "standing-roster")
    assert case["actual_outcome"] == "refuse"
    assert case["finding_codes"] == ["standing_seat_drift"]


def test_unindexed_fixture_is_a_deterministic_conformance_mismatch(
    temporary_validator: Path,
) -> None:
    # Given a fixture YAML file absent from the index
    orphan = (
        temporary_validator.parents[1]
        / "contracts/council-convening/fixtures/orphan.yaml"
    )
    _ = orphan.write_text("schema_version: 1\nkind: test-orphan\n", encoding="utf-8")

    # When strict machine validation runs twice
    first = run_cli("--strict", "--json", validator=temporary_validator)
    second = run_cli("--strict", "--json", validator=temporary_validator)

    # Then both runs fail as conformance, with path-safe deterministic findings.
    assert first.returncode == second.returncode == 1
    assert first.stdout == second.stdout
    payload = json_output(first)
    assert payload["findings"][0]["code"] == "CC-INDEX-PARITY"
    assert str(temporary_validator.parents[1]) not in first.stdout


def test_unknown_case_is_a_deterministic_invocation_error() -> None:
    # Given a case identifier absent from the index
    arguments = ("--case", "not-indexed", "--json")

    # When it is selected twice
    first = run_cli(*arguments)
    second = run_cli(*arguments)

    # Then both runs return the stable harness-error protocol.
    assert first.returncode == second.returncode == 2
    assert first.stdout == second.stdout
    payload = json_output(first)
    assert payload["status"] == "error"
    assert payload["findings"][0]["code"] == "CC-CASE-UNKNOWN"
    assert payload["findings"][0]["case_id"] == "not-indexed"


def test_complete_indexed_corpus_finishes_under_thirty_seconds() -> None:
    # Given the complete indexed foundation corpus
    started = monotonic()

    # When strict validation runs through the real CLI
    result = run_cli("--strict")
    elapsed = monotonic() - started

    # Then expectations match and the performance contract is met.
    assert result.returncode == 0, result.stdout + result.stderr
    assert elapsed < 30


@pytest.mark.parametrize("case_id", ["standing-roster", "conditional-seat-required"])
def test_positive_roster_case_accepts_with_exact_set_arithmetic(case_id: str) -> None:
    # Given an indexed standing-only or condition-triggered roster case
    # When that exact case is validated through the strict machine interface
    completed = run_cli("--strict", "--case", case_id, "--json")
    payload = json_output(completed)

    # Then its independently reproduced roster accepts with no findings.
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert payload["status"] == "pass"
    assert payload["findings"] == []
    case = single_case_result(payload, case_id)
    assert case["expected_outcome"] == case["actual_outcome"] == "accept"
    assert case["finding_codes"] == []


@pytest.mark.parametrize(
    ("case_id", "primary_finding"),
    [
        ("roster-absent", "roster_absent"),
        ("roster-empty", "roster_empty"),
        ("roster-malformed", "roster_malformed"),
        ("roster-duplicate", "roster_duplicate"),
        ("roster-unknown-seat", "roster_unknown_seat"),
        ("roster-standing-incomplete", "roster_standing_incomplete"),
        ("roster-mismatch", "roster_mismatch"),
    ],
)
def test_negative_roster_case_refuses_for_exact_primary_finding(
    case_id: str,
    primary_finding: str,
) -> None:
    # Given an indexed invalid-roster case with one declared primary finding
    # When that exact case is validated through the strict machine interface
    completed = run_cli("--strict", "--case", case_id, "--json")
    payload = json_output(completed)

    # Then matching the expected refusal is a successful conformance result.
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert payload["status"] == "pass"
    case = single_case_result(payload, case_id)
    assert case["expected_outcome"] == case["actual_outcome"] == "refuse"
    assert case["finding_codes"] == [primary_finding]


@pytest.mark.parametrize(
    ("case_id", "primary_finding"),
    [
        ("provenance-opaque", "provenance_opaque"),
        ("rule-revision-unavailable", "rule_revision_unavailable"),
        ("fact-missing", "fact_missing"),
        ("condition-result-drift", "condition_result_drift"),
        ("candidate-head-stale", "candidate_head_stale"),
    ],
)
def test_resolver_provenance_case_refuses_for_exact_primary_finding(
    case_id: str,
    primary_finding: str,
) -> None:
    # Given an indexed resolver case covering exact identity, facts, evaluation, or head drift
    # When that exact case is validated through the strict machine interface
    completed = run_cli("--strict", "--case", case_id, "--json")
    payload = json_output(completed)

    # Then matching its one stable provenance refusal is a successful conformance result.
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert payload["status"] == "pass"
    case = single_case_result(payload, case_id)
    assert case["expected_outcome"] == case["actual_outcome"] == "refuse"
    assert case["finding_codes"] == [primary_finding]
