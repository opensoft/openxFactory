from __future__ import annotations

from .index import load_index, validate_paths
from .models import (
    CaseId,
    CaseResult,
    ContractVersion,
    Execution,
    Finding,
    Report,
    Status,
)
from .validation import load_schema_validator, validate_case


def _expectation_finding(result: CaseResult, primary_finding: str | None) -> Finding | None:
    if result.actual_outcome != result.expected_outcome:
        return Finding(
            "CC-CASE-EXPECTATION", "error", "actual outcome does not match expected outcome",
            result.case_id,
        )
    if result.expected_outcome == "accept" and result.finding_codes:
        return Finding(
            "CC-CASE-EXPECTATION", "error", "accepted case produced findings", result.case_id,
        )
    if result.expected_outcome == "refuse" and result.finding_codes != (primary_finding,):
        return Finding(
            "CC-CASE-EXPECTATION", "error", "primary finding does not match expectation",
            result.case_id,
        )
    return None


def report_for_finding(finding: Finding, status: Status) -> Report:
    return Report(ContractVersion(1), status, (), (finding,))


def execute(case_id: str | None, strict: bool) -> Execution:
    index = load_index()
    path_findings = validate_paths(index)
    if path_findings:
        return Execution(Report(index.contract_version, "fail", (), path_findings), 1)
    selected = index.cases
    if case_id is not None:
        selected = tuple(case for case in index.cases if case.case_id == case_id)
        if not selected:
            finding = Finding(
                "CC-CASE-UNKNOWN", "error", "requested case_id is not indexed", CaseId(case_id),
            )
            return Execution(report_for_finding(finding, "error"), 2)
    validator = load_schema_validator()
    results: list[CaseResult] = []
    findings: list[Finding] = []
    entries_by_id = {entry.case_id: entry for entry in selected}
    for entry in selected:
        result = validate_case(entry, validator)
        results.append(result)
        expectation = _expectation_finding(result, entries_by_id[result.case_id].expected_primary_finding)
        if expectation is not None:
            findings.append(expectation)
    has_error = any(finding.severity == "error" for finding in findings)
    has_warning = any(finding.severity == "warning" for finding in findings)
    failed = has_error or (strict and has_warning)
    status: Status = "fail" if failed else "pass"
    return Execution(
        Report(index.contract_version, status, tuple(results), tuple(findings)),
        1 if failed else 0,
    )
