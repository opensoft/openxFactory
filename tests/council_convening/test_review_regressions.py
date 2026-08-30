from __future__ import annotations

from pathlib import Path
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


@pytest.mark.parametrize(
    ("original", "replacement"),
    [
        ("repository: example/candidates", "repository: example/other-candidates"),
        ("pull_request: 101", "pull_request: 999"),
    ],
)
def test_authoritative_head_is_bound_to_candidate_identity(
    temporary_validator: Path,
    original: str,
    replacement: str,
) -> None:
    fixture_path = "contracts/council-convening/fixtures/positive/standing-roster.yaml"
    fixture = install_single_case(temporary_validator, "standing-roster", fixture_path)
    text = fixture.read_text(encoding="utf-8")
    _ = fixture.write_text(text.replace(original, replacement, 1), encoding="utf-8")

    completed = run_cli("--strict", "--json", validator=temporary_validator)
    payload = json_output(completed)

    assert completed.returncode == 1
    result = single_case_result(payload, "standing-roster")
    assert result["actual_outcome"] == "refuse"
    assert result["finding_codes"] == ["candidate_head_stale"]


def test_fixture_class_must_match_expected_outcome(
    temporary_validator: Path,
) -> None:
    fixture_path = "contracts/council-convening/fixtures/positive/standing-roster.yaml"
    _ = install_single_case(temporary_validator, "standing-roster", fixture_path)
    index = (
        temporary_validator.parents[1]
        / "contracts/council-convening/fixtures/index.yaml"
    )
    text = index.read_text(encoding="utf-8")
    _ = index.write_text(
        text.replace("class: positive", "class: negative", 1),
        encoding="utf-8",
    )

    completed = run_cli("--strict", "--json", validator=temporary_validator)
    payload = json_output(completed)

    assert completed.returncode == 1
    assert payload["status"] == "fail"
    assert payload["findings"][0]["code"] == "CC-INDEX-EXPECTATION"
