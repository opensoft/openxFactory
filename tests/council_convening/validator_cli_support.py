from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Final, Protocol, TypedDict

import pytest

REPOSITORY_ROOT: Final = Path(__file__).resolve().parents[2]
VALIDATOR: Final = REPOSITORY_ROOT / "scripts" / "validate-council-convening.py"
VALIDATOR_PACKAGE: Final = REPOSITORY_ROOT / "scripts" / "council_convening_validation"
SCHEMA_PATH: Final = (
    REPOSITORY_ROOT
    / "contracts"
    / "council-convening"
    / "resolved-council-convening.schema.yaml"
)
INDEX_PATH: Final = (
    REPOSITORY_ROOT / "contracts" / "council-convening" / "fixtures" / "index.yaml"
)


class FindingJson(TypedDict):
    code: str
    severity: str
    case_id: str | None
    path: str | None
    message: str


class CaseResultJson(TypedDict):
    case_id: str
    expected_outcome: str
    actual_outcome: str
    finding_codes: list[str]
    evidence_id: str


class ReportJson(TypedDict):
    contract_version: int
    status: str
    cases: list[CaseResultJson]
    findings: list[FindingJson]


class ReportDecoder(Protocol):
    def __call__(self, s: str) -> ReportJson: ...


decode_report: ReportDecoder = json.loads


def run_cli(
    *arguments: str, validator: Path = VALIDATOR
) -> subprocess.CompletedProcess[str]:
    assert validator.is_file(), f"planned validator CLI is missing: {validator}"
    return subprocess.run(
        [sys.executable, validator, *arguments],
        cwd=validator.parents[1],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def json_output(result: subprocess.CompletedProcess[str]) -> ReportJson:
    assert result.stderr == "", result.stderr
    return decode_report(result.stdout)


def single_case_result(payload: ReportJson, case_id: str) -> CaseResultJson:
    assert len(payload["cases"]) == 1
    result = payload["cases"][0]
    assert result["case_id"] == case_id
    return result


def install_single_case(
    temporary_validator: Path, case_id: str, fixture_path: str
) -> Path:
    fixture_root = (
        temporary_validator.parents[1] / "contracts/council-convening/fixtures"
    )
    target = temporary_validator.parents[1] / fixture_path
    target.parent.mkdir(parents=True, exist_ok=True)
    _ = shutil.copy2(REPOSITORY_ROOT / fixture_path, target)
    index = fixture_root / "index.yaml"
    _ = index.write_text(
        f"""schema_version: 1
kind: council-convening-fixture-index
contract_version: 1
cases:
  - case_id: {case_id}
    class: positive
    path: {fixture_path}
    requirement_ids: [FR-TEST]
    scenario_ids: [SC-TEST]
    expected_outcome: accept
    expected_primary_finding: null
    evidence_id: TEST-{case_id.upper()}
""",
        encoding="utf-8",
    )
    return target


@pytest.fixture(name="temporary_validator")
def temporary_validator_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    scripts = root / "scripts"
    fixtures = root / "contracts" / "council-convening" / "fixtures"
    scripts.mkdir(parents=True)
    fixtures.mkdir(parents=True)
    _ = shutil.copy2(VALIDATOR, scripts / VALIDATOR.name)
    _ = shutil.copytree(VALIDATOR_PACKAGE, scripts / VALIDATOR_PACKAGE.name)
    _ = shutil.copy2(SCHEMA_PATH, fixtures.parent / SCHEMA_PATH.name)
    _ = shutil.copy2(INDEX_PATH, fixtures / "index.yaml")
    return scripts / VALIDATOR.name
