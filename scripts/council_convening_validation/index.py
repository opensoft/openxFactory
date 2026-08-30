from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from .models import (
    CaseEntry,
    CaseId,
    ContractVersion,
    ContractViolation,
    Finding,
    FixtureIndex,
    Outcome,
    RelativePath,
    YamlValue,
)
from .paths import FIXTURE_ROOT, INDEX_PATH, INDEX_RELATIVE_PATH, ROOT
from .yaml_io import load_yaml, mapping, string, string_tuple

EXPECTED_INDEX_KEYS: Final = {"schema_version", "kind", "contract_version", "cases"}
EXPECTED_CASE_KEYS: Final = {
    "case_id", "class", "path", "requirement_ids", "scenario_ids",
    "expected_outcome", "expected_primary_finding", "evidence_id",
}


def _case_class(value: YamlValue, case_id: CaseId) -> Literal["positive", "negative"]:
    if value == "positive":
        return "positive"
    if value == "negative":
        return "negative"
    raise ContractViolation(Finding(
        "CC-INDEX-SHAPE", "error", "class must be positive or negative", case_id,
        RelativePath(INDEX_RELATIVE_PATH),
    ))


def _outcome(value: YamlValue, case_id: CaseId) -> Outcome:
    if value == "accept":
        return "accept"
    if value == "refuse":
        return "refuse"
    raise ContractViolation(Finding(
        "CC-INDEX-SHAPE", "error", "expected_outcome must be accept or refuse", case_id,
        RelativePath(INDEX_RELATIVE_PATH),
    ))


def _parse_case(value: YamlValue) -> CaseEntry:
    path = RelativePath(INDEX_RELATIVE_PATH)
    document = mapping(value, "case", path)
    case_id = CaseId(string(document.get("case_id"), "case_id", path))
    if set(document) != EXPECTED_CASE_KEYS:
        raise ContractViolation(Finding(
            "CC-INDEX-SHAPE", "error", "case fields do not match the index contract", case_id, path,
        ))
    outcome = _outcome(document["expected_outcome"], case_id)
    primary = document["expected_primary_finding"]
    expectation_valid = outcome == "accept" and primary is None
    expectation_valid = expectation_valid or (
        outcome == "refuse" and isinstance(primary, str) and bool(primary)
    )
    if not expectation_valid:
        raise ContractViolation(Finding(
            "CC-INDEX-EXPECTATION", "error", "primary finding does not match outcome", case_id, path,
        ))
    return CaseEntry(
        case_id=case_id,
        case_class=_case_class(document["class"], case_id),
        path=RelativePath(string(document["path"], "path", path)),
        requirement_ids=string_tuple(document["requirement_ids"], "requirement_ids", path),
        scenario_ids=string_tuple(document["scenario_ids"], "scenario_ids", path),
        expected_outcome=outcome,
        expected_primary_finding=primary if isinstance(primary, str) else None,
        evidence_id=string(document["evidence_id"], "evidence_id", path),
    )


def load_index() -> FixtureIndex:
    path = RelativePath(INDEX_RELATIVE_PATH)
    document = mapping(load_yaml(INDEX_PATH, path), "fixture index", path)
    if set(document) != EXPECTED_INDEX_KEYS:
        raise ContractViolation(Finding(
            "CC-INDEX-SHAPE", "error", "index fields do not match the contract", path=path,
        ))
    if document["schema_version"] != 1 or document["contract_version"] != 1:
        raise ContractViolation(Finding(
            "CC-INDEX-METADATA", "error", "schema_version and contract_version must be 1", path=path,
        ))
    if document["kind"] != "council-convening-fixture-index":
        raise ContractViolation(Finding(
            "CC-INDEX-METADATA", "error", "fixture index kind is not supported", path=path,
        ))
    values = document["cases"]
    if not isinstance(values, list):
        raise ContractViolation(Finding("CC-INDEX-SHAPE", "error", "cases must be a list", path=path))
    cases = tuple(_parse_case(value) for value in values)
    if not cases:
        raise ContractViolation(Finding(
            "CC-INDEX-EMPTY", "error", "fixture index must contain at least one case", path=path,
        ))
    if [case.case_id for case in cases] != sorted(case.case_id for case in cases):
        raise ContractViolation(Finding("CC-INDEX-ORDER", "error", "cases must be ordered", path=path))
    if len({case.case_id for case in cases}) != len(cases):
        raise ContractViolation(Finding("CC-INDEX-DUPLICATE-CASE", "error", "case IDs must be unique", path=path))
    if len({case.path for case in cases}) != len(cases):
        raise ContractViolation(Finding("CC-INDEX-DUPLICATE-PATH", "error", "paths must be unique", path=path))
    return FixtureIndex(ContractVersion(1), cases)


def validate_paths(index: FixtureIndex) -> tuple[Finding, ...]:
    fixture_root = FIXTURE_ROOT.resolve()
    for case in index.cases:
        candidate = Path(case.path)
        if candidate.is_absolute() or ".." in candidate.parts or not (ROOT / candidate).resolve().is_relative_to(fixture_root):
            raise ContractViolation(Finding(
                "CC-INDEX-PATH", "error", "fixture path escapes the fixture directory",
                case.case_id, case.path,
            ))
    indexed = {Path(case.path) for case in index.cases}
    packaged = {path.relative_to(ROOT) for path in FIXTURE_ROOT.rglob("*.yaml") if path != INDEX_PATH}
    findings: list[Finding] = []
    for path in sorted(indexed - packaged):
        findings.append(Finding(
            "CC-INDEX-PARITY", "error", "indexed fixture file is missing",
            path=RelativePath(path.as_posix()),
        ))
    for path in sorted(packaged - indexed):
        findings.append(Finding(
            "CC-INDEX-PARITY", "error", "fixture YAML file is not indexed",
            path=RelativePath(path.as_posix()),
        ))
    return tuple(findings)
