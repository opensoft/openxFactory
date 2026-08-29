from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from .canonical import canonical_digest
from .evidence_validation import (
    deterministic_evidence_findings,
    dispatch_evidence_findings,
)
from .model import Finding, Record, as_record, as_records, as_strings
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
    registry_ref = as_record(decision.get("registry")) or {}
    registry_id = str(registry_ref.get("registry_id"))
    revisions = index.registries.get(registry_id, [])
    all_predecessors = {
        str(item.get("predecessor_revision_digest"))
        for item in revisions
        if item.get("predecessor_revision_digest") is not None
    }
    current_heads = [
        item
        for item in revisions
        if str(item.get("revision_digest")) not in all_predecessors
    ]
    if len(current_heads) != 1:
        return [
            Finding(
                "current-registry",
                decision_id,
                "trusted snapshot has no unique current registry head",
            )
        ]
    evaluated_at = parse_timestamp(decision.get("evaluated_at"))
    applicable = [
        item
        for item in revisions
        if parse_timestamp(item.get("published_at")) <= evaluated_at
    ]
    applicable_digests = {str(item.get("revision_digest")) for item in applicable}
    referenced_predecessors = {
        str(item.get("predecessor_revision_digest"))
        for item in applicable
        if str(item.get("predecessor_revision_digest")) in applicable_digests
    }
    heads = [
        item
        for item in applicable
        if str(item.get("revision_digest")) not in referenced_predecessors
    ]
    if len(heads) != 1:
        return [
            Finding(
                "current-registry",
                decision_id,
                "evaluation time has no unique current registry head",
            )
        ]
    findings: list[Finding] = []
    if terminal and parse_timestamp(current_heads[0].get("published_at")) > evaluated_at:
        findings.append(
            Finding(
                "current-registry",
                decision_id,
                "current registry head postdates evaluation time",
            )
        )
    head = current_heads[0] if terminal else heads[0]
    if (
        registry_ref.get("revision_id") != head.get("revision_id")
        or registry_ref.get("revision_digest") != head.get("revision_digest")
    ):
        findings.append(
                Finding("current-registry", decision_id, "decision does not name current head")
        )
    entries = {
        str(item.get("allowance_id")): item
        for item in as_records(head.get("allowances"))
    }
    for resolution in as_records(decision.get("resolutions")):
        reference = as_record(resolution.get("allowance_reference")) or {}
        allowance_id = str(reference.get("allowance_id"))
        if reference.get("registry_id") != registry_id:
            findings.append(
                Finding("allowance-resolution", decision_id, "reference registry differs")
            )
            continue
        entry = entries.get(allowance_id)
        if resolution.get("status") == "unresolved":
            findings.extend(
                _unresolved_allowance_findings(
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
    findings.extend(deterministic_evidence_findings(decision, head))
    return findings


def _unresolved_allowance_findings(
    *,
    decision: Record,
    resolution: Record,
    registry_id: str,
    entry: Record | None,
    index: ResolutionIndex,
) -> list[Finding]:
    decision_id = str(decision.get("decision_id"))
    reference = as_record(resolution.get("allowance_reference")) or {}
    allowance_id = str(reference.get("allowance_id"))
    expected_reason: str | None = "allowance_not_found"
    if entry is not None:
        approval = index.approvals.get(
            (registry_id, allowance_id, str(entry.get("approval_digest")))
        )
        expected_reason = "approval_not_found"
        if approval is not None:
            evaluated_at = parse_timestamp(decision.get("evaluated_at"))
            active = parse_timestamp(approval.get("valid_from")) <= evaluated_at < parse_timestamp(
                approval.get("valid_until")
            )
            revocations = _applicable_revocation_digests(
                registry_id=registry_id,
                allowance_id=allowance_id,
                approval_digest=str(entry.get("approval_digest")),
                revocations=index.revocations,
                evaluated_at=evaluated_at,
            )
            expected_reason = "scope_indeterminate" if active and not revocations else None
    if resolution.get("reason_code") == expected_reason:
        return []
    return [
        Finding(
            "allowance-resolution",
            decision_id,
            "unresolved reason differs from current allowance state",
        )
    ]


def _applicable_revocation_digests(
    *,
    registry_id: str,
    allowance_id: str,
    approval_digest: str,
    revocations: dict[str, Record],
    evaluated_at: datetime,
) -> list[str]:
    target = (registry_id, allowance_id, approval_digest)
    return sorted(
        digest
        for digest, event in revocations.items()
        if (
            str(event.get("registry_id")),
            str(event.get("allowance_id")),
            str(event.get("approval_digest")),
        )
        == target
        and parse_timestamp(event.get("revoked_at")) <= evaluated_at
    )


def _resolved_allowance_findings(resolved: ResolvedAllowance) -> list[Finding]:
    decision_id = str(resolved.decision.get("decision_id"))
    evaluated_at = parse_timestamp(resolved.decision.get("evaluated_at"))
    reference = as_record(resolved.resolution.get("allowance_reference")) or {}
    expected_revocations = _applicable_revocation_digests(
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
    valid = parse_timestamp(resolved.approval.get("valid_from")) <= evaluated_at < parse_timestamp(
        resolved.approval.get("valid_until")
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
        finding.get("disposition") != expected_disposition for finding in matching_findings
    ):
        findings.append(
            Finding(
                "allowance-disposition",
                decision_id,
                "deterministic finding disposition differs from resolved allowance state",
            )
        )
    return findings
