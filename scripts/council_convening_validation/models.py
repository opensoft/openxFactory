from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, NewType, TypeAlias, TypedDict, override

Scalar: TypeAlias = str | int | float | bool | None
RawYaml: TypeAlias = Scalar | list["RawYaml"] | dict[Scalar, "RawYaml"]
YamlValue: TypeAlias = Scalar | list["YamlValue"] | dict[str, "YamlValue"]
Severity: TypeAlias = Literal["error", "warning"]
Outcome: TypeAlias = Literal["accept", "refuse"]
Status: TypeAlias = Literal["pass", "fail", "error"]

CaseId = NewType("CaseId", str)
ContractVersion = NewType("ContractVersion", int)
RelativePath = NewType("RelativePath", str)


class FindingJson(TypedDict):
    code: str
    severity: Severity
    case_id: str | None
    path: str | None
    message: str


class CaseResultJson(TypedDict):
    case_id: str
    expected_outcome: Outcome
    actual_outcome: Outcome
    finding_codes: list[str]
    evidence_id: str


class ReportJson(TypedDict):
    contract_version: int
    status: Status
    cases: list[CaseResultJson]
    findings: list[FindingJson]


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: Severity
    message: str
    case_id: CaseId | None = None
    path: RelativePath | None = None

    def to_json(self) -> FindingJson:
        return FindingJson(
            code=self.code,
            severity=self.severity,
            case_id=self.case_id,
            path=self.path,
            message=self.message,
        )


@dataclass(frozen=True, slots=True)
class CaseEntry:
    case_id: CaseId
    case_class: Literal["positive", "negative"]
    path: RelativePath
    requirement_ids: tuple[str, ...]
    scenario_ids: tuple[str, ...]
    expected_outcome: Outcome
    expected_primary_finding: str | None
    evidence_id: str


@dataclass(frozen=True, slots=True)
class FixtureIndex:
    contract_version: ContractVersion
    cases: tuple[CaseEntry, ...]


@dataclass(frozen=True, slots=True)
class BooleanEqualsPredicate:
    fact: str
    expected: bool


@dataclass(frozen=True, slots=True)
class ConditionalRule:
    seat: str
    condition_ref: str
    predicate: BooleanEqualsPredicate


@dataclass(frozen=True, slots=True)
class GovernedRule:
    repository: str
    path: str
    revision: str
    matched_class: str
    standing_seats: tuple[str, ...]
    conditional_seats: tuple[ConditionalRule, ...]


@dataclass(frozen=True, slots=True)
class ResolverInput:
    candidate_head: str
    governed_rule: GovernedRule | None


@dataclass(frozen=True, slots=True)
class FixtureInput:
    convening: dict[str, YamlValue]
    resolver: ResolverInput


@dataclass(frozen=True, slots=True)
class CaseResult:
    case_id: CaseId
    expected_outcome: Outcome
    actual_outcome: Outcome
    finding_codes: tuple[str, ...]
    evidence_id: str

    def to_json(self) -> CaseResultJson:
        return CaseResultJson(
            case_id=self.case_id,
            expected_outcome=self.expected_outcome,
            actual_outcome=self.actual_outcome,
            finding_codes=list(self.finding_codes),
            evidence_id=self.evidence_id,
        )


@dataclass(frozen=True, slots=True)
class Report:
    contract_version: ContractVersion
    status: Status
    cases: tuple[CaseResult, ...]
    findings: tuple[Finding, ...]

    def to_json(self) -> ReportJson:
        ordered = sorted(
            self.findings,
            key=lambda item: (item.case_id or "", item.path or "", item.code, item.message),
        )
        return ReportJson(
            contract_version=self.contract_version,
            status=self.status,
            cases=[result.to_json() for result in self.cases],
            findings=[finding.to_json() for finding in ordered],
        )


@dataclass(frozen=True, slots=True)
class Execution:
    report: Report
    exit_code: int


@dataclass(frozen=True, slots=True)
class ContractViolation(Exception):
    finding: Finding

    @override
    def __str__(self) -> str:
        return self.finding.message


@dataclass(frozen=True, slots=True)
class HarnessError(Exception):
    finding: Finding

    @override
    def __str__(self) -> str:
        return self.finding.message
