from __future__ import annotations

from itertools import pairwise

from .model import Finding, Record, as_record, as_records
from .temporal import parse_timestamp

GATE_ORDER = ("approval", "dispatch", "admission")
VALID_GATE_PREFIXES = (
    ("approval",),
    ("approval", "dispatch"),
    GATE_ORDER,
)


def enforcement_findings(chains: dict[str, list[Record]]) -> list[Finding]:
    findings: list[Finding] = []
    for correlation, decisions in chains.items():
        gates = [str(decision.get("enforcement_point")) for decision in decisions]
        if len(gates) != len(set(gates)):
            findings.extend(
                (
                    Finding(
                        "enforcement-gate-set",
                        correlation,
                        "binding contains a duplicate enforcement point",
                    ),
                    Finding(
                        "enforcement-binding",
                        correlation,
                        "duplicate gate decisions do not form one sequence",
                    ),
                )
            )
        by_gate = {
            str(decision.get("enforcement_point")): decision for decision in decisions
        }
        ordered_gates = tuple(gate for gate in GATE_ORDER if gate in by_gate)
        if ordered_gates not in VALID_GATE_PREFIXES:
            findings.append(
                Finding(
                    "enforcement-gate-set",
                    correlation,
                    "binding decisions must form a completed gate prefix",
                )
            )
        reference_sets = {
            tuple(sorted(reference_keys(as_records(decision.get("allowance_references")))))
            for decision in decisions
        }
        bindings = {_decision_binding(decision) for decision in decisions}
        if len(reference_sets) > 1:
            findings.append(
                Finding(
                    "allowance-reference-substitution",
                    correlation,
                    "gate bindings changed",
                )
            )
        if len(bindings) > 1:
            findings.append(
                Finding(
                    "enforcement-binding",
                    correlation,
                    "content or policy binding changed",
                )
            )
        ordered = [by_gate[gate] for gate in ordered_gates]
        if any(
            parse_timestamp(later.get("evaluated_at"))
            <= parse_timestamp(earlier.get("evaluated_at"))
            for earlier, later in pairwise(ordered)
        ):
            findings.append(
                Finding(
                    "enforcement-sequence",
                    correlation,
                    "later enforcement point is not later in time",
                )
            )
        if any(earlier.get("outcome") != "allow" for earlier in ordered[:-1]):
            findings.append(
                Finding(
                    "enforcement-sequence",
                    correlation,
                    "a non-allow decision must terminate the gate sequence",
                )
            )
    return findings


def reference_keys(references: list[Record]) -> list[tuple[str, str]]:
    return [
        (str(item.get("registry_id")), str(item.get("allowance_id")))
        for item in references
    ]


def _decision_binding(decision: Record) -> tuple[str, ...]:
    vocabulary = as_record(decision.get("vocabulary")) or {}
    policy_source = as_record(decision.get("policy_source")) or {}
    ratification = as_record(policy_source.get("ratification_record")) or {}
    registry = as_record(decision.get("registry")) or {}
    return (
        str(decision.get("evaluated_content_digest")),
        str(policy_source.get("repository")),
        str(policy_source.get("path")),
        str(policy_source.get("revision")),
        str(policy_source.get("content_digest")),
        str(ratification.get("path")),
        str(ratification.get("content_digest")),
        str(vocabulary.get("vocabulary_id")),
        str(vocabulary.get("vocabulary_digest")),
        str(registry.get("registry_id")),
    )
