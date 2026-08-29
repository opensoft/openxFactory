from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import assert_never

from .allowance_resolution import (
    applicable_revocation_digests,
    unresolved_allowance_findings,
)
from .canonical import canonical_digest
from .evidence_validation import (
    dispatch_evidence_findings,
)
from .model import Finding, Record, as_record, as_records, as_strings
from .registry_state import select_registry_state
from .registry_validation import (
    ResolvedRegistryState,
    UnresolvedRegistryState,
)
from .temporal import parse_timestamp


@dataclass(frozen=True, slots=True)
class ResolutionIndex:
    registries: dict[str, list[Record]]
    approvals: dict[tuple[str, str, str], Record]
    revocations: dict[str, Record]


@dataclass(frozen=True, slots=True)
class ResolvedAllowance:
    decision: Record
    resolution: Record
    approval: Record
    entry: Record
    revocations: dict[str, Record]


def resolution_findings(records: list[Record]) -> list[Finding]:
    registries: dict[str, list[Record]] = defaultdict(list)
    decision_chains: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        if record.get("kind") == "policy_allowance_registry":
            registries[str(record.get("registry_id"))].append(record)
        if record.get("kind") == "compliance_decision":
            decision_chains[str(record.get("governed_binding_id"))].append(record)
    terminal_decisions = {
        id(max(chain, key=lambda item: parse_timestamp(item.get("evaluated_at"))))
        for chain in decision_chains.values()
    }
    index = ResolutionIndex(
        registries=registries,
        approvals={
            (
                str(item.get("registry_id")),
                str(item.get("allowance_id")),
                str(item.get("approval_digest")),
            ): item
            for item in records
            if item.get("kind") == "policy_allowance"
        },
        revocations={
            str(item.get("revocation_digest")): item
            for item in records
            if item.get("kind") == "policy_allowance_revocation"
        },
    )
    return [
        finding
        for decision in records
        if decision.get("kind") == "compliance_decision"
        for finding in _decision_resolution_findings(
            decision, index, terminal=id(decision) in terminal_decisions
        )
    ]


def _decision_resolution_findings(
    decision: Record, index: ResolutionIndex, *, terminal: bool
) -> list[Finding]:
    decision_id = str(decision.get("decision_id"))
    registry_state, findings = select_registry_state(
        decision, index.registries, terminal=terminal
    )
    match registry_state:
        case UnresolvedRegistryState():
            return findings
        case ResolvedRegistryState(registry_id=registry_id, head=head):
            pass
        case unreachable:
            assert_never(unreachable)
    entries = {
        str(item.get("allowance_id")): item
        for item in as_records(head.get("allowances"))
    }
    for resolution in as_records(decision.get("resolutions")):
        reference = as_record(resolution.get("allowance_reference")) or {}
        allowance_id = str(reference.get("allowance_id"))
        if reference.get("registry_id") != registry_id:
            findings.append(
                Finding(
                    "allowance-resolution", decision_id, "reference registry differs"
                )
            )
            continue
        entry = entries.get(allowance_id)
        if resolution.get("status") == "unresolved":
            findings.extend(
                unresolved_allowance_findings(
                    decision=decision,
                    resolution=resolution,
                    registry_id=registry_id,
                    entry=entry,
                    index=index,
                )
            )
            continue
        if resolution.get("status") != "resolved":
            continue
        if entry is None or resolution.get("approval_digest") != entry.get(
            "approval_digest"
        ):
            findings.append(
                Finding(
                    "allowance-resolution",
                    decision_id,
                    "complete approval identity does not resolve",
                )
            )
            continue
        approval = index.approvals.get(
            (registry_id, allowance_id, str(entry.get("approval_digest")))
        )
        if approval is None:
            findings.append(
                Finding("registry-approval", allowance_id, "approval record is absent")
            )
            continue
        findings.extend(
            _resolved_allowance_findings(
                ResolvedAllowance(
                    decision=decision,
                    resolution=resolution,
                    approval=approval,
                    entry=entry,
                    revocations=index.revocations,
                )
            )
        )
    findings.extend(dispatch_evidence_findings(decision, head))
    return findings


def _resolved_allowance_findings(resolved: ResolvedAllowance) -> list[Finding]:
    decision_id = str(resolved.decision.get("decision_id"))
    evaluated_at = parse_timestamp(resolved.decision.get("evaluated_at"))
    reference = as_record(resolved.resolution.get("allowance_reference")) or {}
    expected_revocations = applicable_revocation_digests(
        registry_id=str(reference.get("registry_id")),
        allowance_id=str(reference.get("allowance_id")),
        approval_digest=str(resolved.resolution.get("approval_digest")),
        revocations=resolved.revocations,
        evaluated_at=evaluated_at,
    )
    findings: list[Finding] = []
    if set(as_strings(resolved.resolution.get("revocation_digests"))) != set(
        expected_revocations
    ):
        findings.append(
            Finding(
                "allowance-resolution", decision_id, "revocation identity set differs"
            )
        )
    valid = (
        parse_timestamp(resolved.approval.get("valid_from"))
        <= evaluated_at
        < parse_timestamp(resolved.approval.get("valid_until"))
    )
    if resolved.decision.get("outcome") == "allow" and (
        expected_revocations or not valid
    ):
        findings.append(
            Finding(
                "allowance-state",
                decision_id,
                "revoked or inactive allowance authorized allow",
            )
        )
    scope = as_record(resolved.resolution.get("scope")) or {}
    approval_scope = as_record(resolved.approval.get("scope")) or {}
    if scope != approval_scope:
        findings.append(
            Finding("scope-binding", decision_id, "complete scope identity differs")
        )
    verdict = as_record(resolved.resolution.get("scope_verdict")) or {}
    if verdict.get("scope_digest") != approval_scope.get("scope_digest"):
        findings.append(Finding("scope-binding", decision_id, "scope digest differs"))
    if verdict.get("evaluated_content_digest") != resolved.decision.get(
        "evaluated_content_digest"
    ):
        findings.append(Finding("scope-binding", decision_id, "content digest differs"))
    if verdict.get("verdict_digest") != canonical_digest(verdict, "verdict_digest"):
        findings.append(Finding("canonical-digest", decision_id, "scope verdict"))
    expected_disposition = "block"
    if valid and not expected_revocations:
        match verdict.get("verdict"):
            case "covers":
                expected_disposition = "satisfied"
            case "indeterminate":
                expected_disposition = "needs_human_review"
            case _:
                expected_disposition = "block"
    matching_findings = [
        finding
        for finding in as_records(resolved.decision.get("findings"))
        if finding.get("layer") == "deterministic"
        and finding.get("class_id") == resolved.resolution.get("class_id")
    ]
    if any(
        finding.get("disposition") != expected_disposition
        for finding in matching_findings
    ):
        findings.append(
            Finding(
                "allowance-disposition",
                decision_id,
                "deterministic finding disposition differs from resolved allowance state",
            )
        )
    return findings
