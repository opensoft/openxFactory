from __future__ import annotations

from .models import (
    BooleanEqualsPredicate,
    CaseEntry,
    ConditionalRule,
    Finding,
    FixtureInput,
    GovernedRule,
    HarnessError,
    RelativePath,
    ResolverInput,
    YamlValue,
)
from .paths import ROOT
from .yaml_io import load_yaml, mapping, string, string_tuple


def _parse_predicate(value: YamlValue, path: RelativePath) -> BooleanEqualsPredicate:
    document = mapping(value, "predicate", path)
    if set(document) != {"kind", "fact", "expected"}:
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "predicate fields are invalid", path=path,
        ))
    if document["kind"] != "boolean_equals":
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "predicate kind is unsupported", path=path,
        ))
    expected = document["expected"]
    if not isinstance(expected, bool):
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "predicate expected must be boolean", path=path,
        ))
    return BooleanEqualsPredicate(
        fact=string(document["fact"], "predicate fact", path),
        expected=expected,
    )


def _parse_conditional_rules(value: YamlValue, path: RelativePath) -> tuple[ConditionalRule, ...]:
    if not isinstance(value, list):
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "conditional_seats must be a list", path=path,
        ))
    rules: list[ConditionalRule] = []
    for item in value:
        document = mapping(item, "conditional seat declaration", path)
        if set(document) != {"seat", "condition_ref", "predicate"}:
            raise HarnessError(Finding(
                "CC-FIXTURE-SHAPE", "error", "conditional declaration fields are invalid", path=path,
            ))
        rules.append(ConditionalRule(
            seat=string(document["seat"], "seat", path),
            condition_ref=string(document["condition_ref"], "condition_ref", path),
            predicate=_parse_predicate(document["predicate"], path),
        ))
    return tuple(rules)


def _parse_governed_rule(value: YamlValue, path: RelativePath) -> GovernedRule | None:
    if value is None:
        return None
    document = mapping(value, "governed_rule", path)
    expected_fields = {
        "repository", "path", "revision", "matched_class", "standing_seats", "conditional_seats",
    }
    if set(document) != expected_fields:
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "governed rule fields are invalid", path=path,
        ))
    return GovernedRule(
        repository=string(document["repository"], "rule repository", path),
        path=string(document["path"], "rule path", path),
        revision=string(document["revision"], "rule revision", path),
        matched_class=string(document["matched_class"], "matched class", path),
        standing_seats=string_tuple(document["standing_seats"], "standing_seats", path),
        conditional_seats=_parse_conditional_rules(document["conditional_seats"], path),
    )


def load_fixture(entry: CaseEntry) -> FixtureInput:
    path = entry.path
    document = mapping(load_yaml(ROOT / path, path), "fixture", path)
    if set(document) != {"schema_version", "kind", "input"}:
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "fixture fields are invalid", entry.case_id, path,
        ))
    if document["schema_version"] != 1 or document["kind"] != "council-convening-conformance-case":
        raise HarnessError(Finding(
            "CC-FIXTURE-METADATA", "error", "fixture metadata is invalid", entry.case_id, path,
        ))
    inputs = mapping(document["input"], "input", path)
    if set(inputs) != {"convening", "resolver"}:
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "fixture input fields are invalid", entry.case_id, path,
        ))
    resolver = mapping(inputs["resolver"], "resolver", path)
    if set(resolver) != {"candidate_head", "governed_rule"}:
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "resolver fields are invalid", entry.case_id, path,
        ))
    return FixtureInput(
        convening=mapping(inputs["convening"], "convening", path),
        resolver=ResolverInput(
            candidate_head=string(resolver["candidate_head"], "candidate_head", path),
            governed_rule=_parse_governed_rule(resolver["governed_rule"], path),
        ),
    )
