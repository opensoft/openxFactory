from __future__ import annotations

from .canonical import CanonicalizationError, canonical_digest
from .model import Finding, Record, as_record
from .registry_validation import registry_chain_findings
from .resolution_validation import resolution_findings
from .temporal import parse_timestamp

__all__ = [
    "CanonicalizationError",
    "canonical_digest",
    "state_findings",
]


def state_findings(records: list[Record]) -> list[Finding]:
    return [
        *_digest_findings(records),
        *_identity_findings(records),
        *registry_chain_findings(records),
        *resolution_findings(records),
    ]


def _digest_findings(records: list[Record]) -> list[Finding]:
    digest_fields = {
        "veto_class_vocabulary": "vocabulary_digest",
        "policy_allowance": "approval_digest",
        "policy_allowance_revocation": "revocation_digest",
        "policy_allowance_registry": "revision_digest",
    }
    findings: list[Finding] = []
    for record in records:
        kind = str(record.get("kind"))
        digest_field = digest_fields.get(kind)
        if digest_field and record.get(digest_field) != canonical_digest(
            record, digest_field
        ):
            findings.append(
                Finding("canonical-digest", str(record.get(digest_field)), kind)
            )
        if kind == "policy_allowance":
            scope = as_record(record.get("scope"))
            if scope is not None and scope.get("scope_digest") != canonical_digest(
                scope, "scope_digest"
            ):
                findings.append(
                    Finding(
                        "canonical-digest", str(record.get("allowance_id")), "scope"
                    )
                )
            if not _ordered_times(record):
                findings.append(
                    Finding(
                        "allowance-validity",
                        str(record.get("allowance_id")),
                        "invalid validity bounds",
                    )
                )
    return findings


def _identity_findings(records: list[Record]) -> list[Finding]:
    identity_fields = {
        "veto_class_vocabulary": ("vocabulary_id", "vocabulary_digest"),
        "policy_allowance": ("registry_id", "allowance_id", "approval_digest"),
        "policy_allowance_revocation": (
            "registry_id",
            "allowance_id",
            "approval_digest",
            "revocation_digest",
        ),
        "policy_allowance_registry": (
            "registry_id",
            "revision_id",
            "revision_digest",
        ),
        "compliance_decision": (
            "governed_binding_id",
            "enforcement_point",
            "decision_id",
        ),
    }
    seen: set[tuple[str, ...]] = set()
    findings: list[Finding] = []
    for record in records:
        kind = str(record.get("kind"))
        fields = identity_fields.get(kind)
        if fields is None:
            continue
        identity = (kind, *(str(record.get(field)) for field in fields))
        if identity in seen:
            findings.append(
                Finding(
                    "duplicate-record-identity", kind, ":".join(identity[1:])
                )
            )
        seen.add(identity)
    return findings


def _ordered_times(allowance: Record) -> bool:
    return parse_timestamp(allowance.get("approved_at")) <= parse_timestamp(
        allowance.get("valid_from")
    ) < parse_timestamp(allowance.get("valid_until"))
