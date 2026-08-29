from __future__ import annotations

from datetime import datetime
from typing import Protocol

from .model import Finding, Record, as_record
from .temporal import parse_timestamp


class AllowanceIndex(Protocol):
    approvals: dict[tuple[str, str, str], Record]
    revocations: dict[str, Record]


def unresolved_allowance_findings(
    *,
    decision: Record,
    resolution: Record,
    registry_id: str,
    entry: Record | None,
    index: AllowanceIndex,
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
            active = (
                parse_timestamp(approval.get("valid_from"))
                <= evaluated_at
                < parse_timestamp(approval.get("valid_until"))
            )
            revocations = applicable_revocation_digests(
                registry_id=registry_id,
                allowance_id=allowance_id,
                approval_digest=str(entry.get("approval_digest")),
                revocations=index.revocations,
                evaluated_at=evaluated_at,
            )
            expected_reason = (
                "scope_indeterminate" if active and not revocations else None
            )
    if resolution.get("reason_code") == expected_reason:
        return []
    return [
        Finding(
            "allowance-resolution",
            decision_id,
            "unresolved reason differs from current allowance state",
        )
    ]


def applicable_revocation_digests(
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
