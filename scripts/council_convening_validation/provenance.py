from __future__ import annotations

from dataclasses import dataclass

from .models import (
    Finding,
    GovernedRule,
    HarnessError,
    RelativePath,
    ResolverInput,
    YamlValue,
)
from .yaml_io import mapping, string, string_tuple


@dataclass(frozen=True, slots=True)
class ProvenanceAccepted:
    rule: GovernedRule
    required_conditionals: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProvenanceRefused:
    finding_code: str


ProvenanceResult = ProvenanceAccepted | ProvenanceRefused


def _rule_identity(document: dict[str, YamlValue], path: RelativePath) -> tuple[str, ...]:
    return (
        string(document["repository"], "rule repository", path),
        string(document["path"], "rule path", path),
        string(document["revision"], "rule revision", path),
        string(document["matched_class"], "matched class", path),
    )


def _producer_evaluations(
    provenance: dict[str, YamlValue],
    path: RelativePath,
) -> tuple[dict[tuple[str, str], bool], bool]:
    resolution = mapping(provenance["resolution"], "resolution", path)
    values = resolution["conditional_seats"]
    if not isinstance(values, list):
        raise HarnessError(Finding(
            "CC-FIXTURE-SHAPE", "error", "conditional evaluations must be a list", path=path,
        ))
    evaluations: dict[tuple[str, str], bool] = {}
    duplicate_evaluation = False
    for value in values:
        evaluation = mapping(value, "conditional evaluation", path)
        required = evaluation["required"]
        if not isinstance(required, bool):
            raise HarnessError(Finding(
                "CC-FIXTURE-SHAPE", "error", "conditional required must be boolean", path=path,
            ))
        key = (
            string(evaluation["seat"], "seat", path),
            string(evaluation["condition_ref"], "condition_ref", path),
        )
        if key in evaluations:
            duplicate_evaluation = True
        evaluations[key] = required
    return evaluations, duplicate_evaluation


def evaluate_provenance(
    convening: dict[str, YamlValue],
    resolver: ResolverInput,
    path: RelativePath,
) -> ProvenanceResult:
    provenance = mapping(convening["required_seats_provenance"], "provenance", path)
    rule = resolver.governed_rule
    if rule is None:
        return ProvenanceRefused("rule_revision_unavailable")
    rule_reference = mapping(provenance["governed_rule"], "governed rule reference", path)
    resolved_identity = (rule.repository, rule.path, rule.revision, rule.matched_class)
    if _rule_identity(rule_reference, path) != resolved_identity:
        return ProvenanceRefused("rule_revision_unavailable")
    candidate = mapping(provenance["candidate"], "candidate", path)
    if string(candidate["head_revision"], "candidate head revision", path) != resolver.candidate_head:
        return ProvenanceRefused("candidate_head_stale")
    facts = mapping(provenance["normalized_facts"], "normalized facts", path)
    producer, duplicate_evaluation = _producer_evaluations(provenance, path)
    declared_evaluations = tuple(
        (conditional.seat, conditional.condition_ref)
        for conditional in rule.conditional_seats
    )
    duplicate_declaration = len(set(declared_evaluations)) != len(declared_evaluations)
    if duplicate_evaluation or duplicate_declaration or set(producer) != set(declared_evaluations):
        return ProvenanceRefused("condition_result_drift")
    recorded_standing = string_tuple(
        mapping(provenance["resolution"], "resolution", path)["standing_seats"],
        "standing_seats",
        path,
    )
    recorded_duplicate = len(set(recorded_standing)) != len(recorded_standing)
    authoritative_duplicate = len(set(rule.standing_seats)) != len(rule.standing_seats)
    if recorded_duplicate or authoritative_duplicate or set(recorded_standing) != set(rule.standing_seats):
        return ProvenanceRefused("standing_seat_drift")
    required_conditionals: list[str] = []
    for conditional in rule.conditional_seats:
        fact_value = facts.get(conditional.predicate.fact)
        if not isinstance(fact_value, bool):
            return ProvenanceRefused("fact_missing")
        independently_required = fact_value == conditional.predicate.expected
        producer_required = producer.get((conditional.seat, conditional.condition_ref))
        if producer_required is None or producer_required != independently_required:
            return ProvenanceRefused("condition_result_drift")
        if independently_required:
            required_conditionals.append(conditional.seat)
    return ProvenanceAccepted(rule, tuple(required_conditionals))
