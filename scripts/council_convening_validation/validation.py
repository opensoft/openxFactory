from __future__ import annotations

from typing import Protocol

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .fixture import load_fixture
from .models import (
    CaseEntry,
    CaseResult,
    Finding,
    HarnessError,
    RelativePath,
    YamlValue,
)
from .paths import SCHEMA_PATH, SCHEMA_RELATIVE_PATH
from .provenance import ProvenanceAccepted, evaluate_provenance
from .yaml_io import load_yaml, mapping, string_tuple


class SchemaValidator(Protocol):
    def is_valid(self, instance: dict[str, YamlValue]) -> bool: ...


def load_schema_validator() -> SchemaValidator:
    path = RelativePath(SCHEMA_RELATIVE_PATH)
    schema = mapping(load_yaml(SCHEMA_PATH, path), "schema", path)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise HarnessError(Finding(
            "CC-SCHEMA-INVALID", "error", error.message, path=path,
        )) from error
    validator: SchemaValidator = Draft202012Validator(schema)
    return validator


def _schema_finding(
    convening: dict[str, YamlValue],
    validator: SchemaValidator,
) -> str | None:
    if "required_seats" not in convening:
        return "roster_absent"
    if "required_seats_provenance" not in convening:
        return "provenance_opaque"
    roster = convening["required_seats"]
    if isinstance(roster, list) and not roster:
        return "roster_empty"
    if isinstance(roster, list):
        strings = [seat for seat in roster if isinstance(seat, str)]
        if len(strings) == len(roster) and len(set(strings)) != len(strings):
            return "roster_duplicate"
    if not validator.is_valid(convening):
        return "roster_malformed"
    return None


def _roster_findings(
    convening: dict[str, YamlValue],
    provenance: ProvenanceAccepted,
    path: RelativePath,
) -> tuple[str, ...]:
    submitted = string_tuple(convening["required_seats"], "required_seats", path)
    conditional_seats = tuple(rule.seat for rule in provenance.rule.conditional_seats)
    declared = set(provenance.rule.standing_seats) | set(conditional_seats)
    if set(submitted) - declared:
        return ("roster_unknown_seat",)
    if set(provenance.rule.standing_seats) - set(submitted):
        return ("roster_standing_incomplete",)
    expected = set(provenance.rule.standing_seats) | set(provenance.required_conditionals)
    if set(submitted) != expected:
        return ("roster_mismatch",)
    return ()


def validate_case(entry: CaseEntry, validator: SchemaValidator) -> CaseResult:
    fixture = load_fixture(entry)
    schema_finding = _schema_finding(fixture.convening, validator)
    if schema_finding is not None:
        finding_codes = (schema_finding,)
    else:
        provenance = evaluate_provenance(fixture.convening, fixture.resolver, entry.path)
        if isinstance(provenance, ProvenanceAccepted):
            finding_codes = _roster_findings(fixture.convening, provenance, entry.path)
        else:
            finding_codes = (provenance.finding_code,)
    actual_outcome = "accept" if not finding_codes else "refuse"
    return CaseResult(
        case_id=entry.case_id,
        expected_outcome=entry.expected_outcome,
        actual_outcome=actual_outcome,
        finding_codes=finding_codes,
        evidence_id=entry.evidence_id,
    )
