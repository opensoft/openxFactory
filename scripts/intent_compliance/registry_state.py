from __future__ import annotations

from typing import assert_never

from .evidence_validation import deterministic_evidence_findings
from .model import Finding, Record, as_record, as_records
from .registry_validation import (
    RegistryState,
    ResolvedRegistryState,
    UnresolvedRegistryState,
    derive_registry_state,
)
from .temporal import parse_timestamp


def select_registry_state(
    decision: Record,
    registries: dict[str, list[Record]],
    *,
    terminal: bool,
) -> tuple[RegistryState, list[Finding]]:
    registry_ref = as_record(decision.get("registry")) or {}
    registry_id = str(registry_ref.get("registry_id"))
    revisions = registries.get(registry_id, [])
    current_state = derive_registry_state(registry_id, revisions)
    match current_state:
        case UnresolvedRegistryState():
            return current_state, _unresolved_state_findings(decision, current_state)
        case ResolvedRegistryState(head=current_head):
            pass
        case unreachable:
            assert_never(unreachable)
    evaluated_at = parse_timestamp(decision.get("evaluated_at"))
    applicable_state = derive_registry_state(
        registry_id,
        [
            revision
            for revision in revisions
            if parse_timestamp(revision.get("published_at")) <= evaluated_at
        ],
    )
    if terminal:
        selected_state: RegistryState = current_state
    else:
        selected_state = applicable_state
    match selected_state:
        case UnresolvedRegistryState():
            return selected_state, _unresolved_state_findings(decision, selected_state)
        case ResolvedRegistryState():
            findings = _binding_findings(decision, selected_state)
        case unreachable:
            assert_never(unreachable)
    if terminal and parse_timestamp(current_head.get("published_at")) > evaluated_at:
        findings.append(
            Finding(
                "current-registry",
                str(decision.get("decision_id")),
                "current registry head postdates evaluation time",
            )
        )
    return selected_state, findings


def _binding_findings(decision: Record, registry_state: RegistryState) -> list[Finding]:
    expected = registry_state.as_record()
    findings = deterministic_evidence_findings(decision, expected)
    if as_record(decision.get("registry")) != expected:
        findings.append(
            Finding(
                "current-registry",
                str(decision.get("decision_id")),
                "declared registry state differs from the derived current state",
            )
        )
    return findings


def _unresolved_state_findings(
    decision: Record, registry_state: UnresolvedRegistryState
) -> list[Finding]:
    findings = _binding_findings(decision, registry_state)
    for resolution in as_records(decision.get("resolutions")):
        if (
            resolution.get("status") != "unresolved"
            or resolution.get("reason_code") != registry_state.reason_code
        ):
            findings.append(
                Finding(
                    "allowance-resolution",
                    str(decision.get("decision_id")),
                    "allowance resolution differs from unresolved registry state",
                )
            )
    return findings
