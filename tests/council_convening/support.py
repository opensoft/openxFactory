from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeAlias

from jsonschema import Draft202012Validator

from scripts.council_convening_validation.models import RelativePath, YamlValue
from scripts.council_convening_validation.yaml_io import (
    load_yaml,
    mapping,
    string,
    string_tuple,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FAMILY_ROOT = REPOSITORY_ROOT / "contracts" / "council-convening"
FIXTURE_ROOT = FAMILY_ROOT / "fixtures"
INDEX_PATH = FIXTURE_ROOT / "index.yaml"
SCHEMA_PATH = FAMILY_ROOT / "resolved-council-convening.schema.yaml"
FEATURE_ROOT = REPOSITORY_ROOT / "specs" / "026-add-resolved-council-seats"
FEATURE_SPEC_PATH = FEATURE_ROOT / "spec.md"
ACCEPTANCE_MAP_PATH = FEATURE_ROOT / "contracts" / "acceptance-map.yaml"
OPENSPEC_SPEC_PATH = (
    REPOSITORY_ROOT
    / "openspec"
    / "changes"
    / "add-resolved-council-seats"
    / "specs"
    / "roles-authority-model"
    / "spec.md"
)

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class CaseEntry:
    case_id: str
    path: str
    case_class: str
    expected_outcome: str
    expected_primary_finding: str | None


@dataclass(frozen=True, slots=True)
class FoundationIndex:
    schema_version: int
    kind: str
    contract_version: int
    cases: tuple[CaseEntry, ...]


@dataclass(frozen=True, slots=True)
class ParityEntry:
    requirement_id: str
    scenario_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StoryEntry:
    requirements: tuple[str, ...]
    outcomes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GateEntry:
    gate_id: str
    owner: str
    external: bool
    blocks_on_failure: bool
    requirement_ids: tuple[str, ...]
    outcome_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AcceptanceMap:
    expected_openspec_requirement_count: int
    expected_openspec_scenario_count: int
    openspec_parity: tuple[ParityEntry, ...]
    stories: tuple[StoryEntry, ...]
    gates: tuple[GateEntry, ...]


class ValidationIssue(Protocol):
    validator: str


class SchemaValidator(Protocol):
    def iter_errors(self, instance: JsonValue) -> Iterable[ValidationIssue]: ...


def _integer(value: YamlValue) -> int:
    assert isinstance(value, int) and not isinstance(value, bool)
    return value


def _optional_string(value: YamlValue) -> str | None:
    assert value is None or isinstance(value, str)
    return value


def _boolean(value: YamlValue) -> bool:
    assert isinstance(value, bool)
    return value


def _optional_string_tuple(
    value: YamlValue | None,
    label: str,
    path: RelativePath,
) -> tuple[str, ...]:
    if value is None:
        return ()
    return string_tuple(value, label, path)


def load_index() -> FoundationIndex:
    relative_path = RelativePath(INDEX_PATH.relative_to(REPOSITORY_ROOT).as_posix())
    document = mapping(load_yaml(INDEX_PATH, relative_path), "fixture index", relative_path)
    raw_cases = document["cases"]
    assert isinstance(raw_cases, list)
    cases: list[CaseEntry] = []
    for raw_case in raw_cases:
        case = mapping(raw_case, "fixture index case", relative_path)
        cases.append(CaseEntry(
            case_id=string(case["case_id"], "case_id", relative_path),
            path=string(case["path"], "path", relative_path),
            case_class=string(case["class"], "class", relative_path),
            expected_outcome=string(case["expected_outcome"], "expected_outcome", relative_path),
            expected_primary_finding=_optional_string(case["expected_primary_finding"]),
        ))
    return FoundationIndex(
        schema_version=_integer(document["schema_version"]),
        kind=string(document["kind"], "kind", relative_path),
        contract_version=_integer(document["contract_version"]),
        cases=tuple(cases),
    )


def indexed_paths(document: FoundationIndex) -> tuple[Path, ...]:
    return tuple(Path(case.path) for case in document.cases)


def load_schema() -> JsonObject:
    assert SCHEMA_PATH.is_file(), f"planned Draft 2020-12 schema is missing: {SCHEMA_PATH}"
    relative_path = RelativePath(SCHEMA_PATH.relative_to(REPOSITORY_ROOT).as_posix())
    return mapping(load_yaml(SCHEMA_PATH, relative_path), "schema", relative_path)


def valid_convening() -> JsonObject:
    return {
        "schema_version": 1,
        "kind": "resolved-council-convening",
        "convening_id": "candidate-123-council",
        "required_seats": ["domain-policy", "client-interest"],
        "required_seats_provenance": {
            "candidate": {
                "repository": "example/candidates",
                "pull_request": 123,
                "head_revision": "0123456789abcdef0123456789abcdef01234567",
            },
            "governed_rule": {
                "repository": "example/governed-rules",
                "path": "candidate-classes/ordinary.yaml",
                "revision": "89abcdef0123456789abcdef0123456789abcdef",
                "matched_class": "ordinary-change",
            },
            "normalized_facts": {"touches_company_policy": False},
            "resolution": {
                "standing_seats": ["domain-policy", "client-interest"],
                "conditional_seats": [{
                    "seat": "company-policy",
                    "condition_ref": "pull-in-company-policy",
                    "required": False,
                }],
            },
        },
    }


def mapping_at(document: JsonObject, *path: str) -> JsonObject:
    current: JsonValue = document
    for segment in path:
        assert isinstance(current, dict)
        current = current[segment]
    assert isinstance(current, dict)
    return current


def validation_keywords(document: JsonObject) -> set[str]:
    validator = _schema_validator()
    return {error.validator for error in validator.iter_errors(document)}


def _schema_validator() -> SchemaValidator:
    return Draft202012Validator(load_schema())


def load_acceptance_map() -> AcceptanceMap:
    relative_path = RelativePath(ACCEPTANCE_MAP_PATH.relative_to(REPOSITORY_ROOT).as_posix())
    document = mapping(load_yaml(ACCEPTANCE_MAP_PATH, relative_path), "acceptance map", relative_path)
    raw_parity = document["openspec_parity"]
    raw_stories = document["stories"]
    raw_gates = document["gates"]
    assert isinstance(raw_parity, list)
    assert isinstance(raw_stories, list)
    assert isinstance(raw_gates, list)
    parity: list[ParityEntry] = []
    for raw_entry in raw_parity:
        entry = mapping(raw_entry, "OpenSpec parity entry", relative_path)
        parity.append(ParityEntry(
            requirement_id=string(entry["id"], "id", relative_path),
            scenario_ids=string_tuple(entry["scenario_ids"], "scenario_ids", relative_path),
        ))
    stories: list[StoryEntry] = []
    for raw_story in raw_stories:
        story = mapping(raw_story, "story entry", relative_path)
        stories.append(StoryEntry(
            requirements=string_tuple(story["requirements"], "requirements", relative_path),
            outcomes=string_tuple(story["outcomes"], "outcomes", relative_path),
        ))
    gates: list[GateEntry] = []
    for raw_gate in raw_gates:
        gate = mapping(raw_gate, "gate entry", relative_path)
        gates.append(GateEntry(
            gate_id=string(gate["gate_id"], "gate_id", relative_path),
            owner=string(gate["owner"], "owner", relative_path),
            external=_boolean(gate.get("external", False)),
            blocks_on_failure=_boolean(gate["blocks_on_failure"]),
            requirement_ids=_optional_string_tuple(
                gate.get("requirement_ids"), "requirement_ids", relative_path,
            ),
            outcome_ids=_optional_string_tuple(
                gate.get("outcome_ids"), "outcome_ids", relative_path,
            ),
        ))
    return AcceptanceMap(
        expected_openspec_requirement_count=_integer(document["expected_openspec_requirement_count"]),
        expected_openspec_scenario_count=_integer(document["expected_openspec_scenario_count"]),
        openspec_parity=tuple(parity),
        stories=tuple(stories),
        gates=tuple(gates),
    )


def markdown_ids(path: Path, pattern: str) -> set[str]:
    return set(re.findall(pattern, path.read_text(encoding="utf-8"), flags=re.MULTILINE))
