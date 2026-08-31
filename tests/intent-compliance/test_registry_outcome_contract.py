from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.intent_compliance.canonical import canonical_digest
from scripts.intent_compliance.model import (
    Record,
    RecordDocument,
    load_record_documents,
)
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _approval(records: list[RecordDocument]) -> RecordDocument:
    return next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == "approval"
    )


def _refresh_deterministic_evidence(decision: Record) -> None:
    evidence = decision["deterministic_evidence"]
    assert isinstance(evidence, dict)
    findings = decision["findings"]
    assert isinstance(findings, list)
    evidence["finding_digests"] = sorted(
        canonical_digest(finding, "__absent_digest_field__")
        for finding in findings
        if isinstance(finding, dict) and finding.get("layer") == "deterministic"
    )
    evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")


def _set_registry_state(decision: Record, registry_state: Record) -> None:
    decision["registry"] = copy.deepcopy(registry_state)
    evidence = decision["deterministic_evidence"]
    assert isinstance(evidence, dict)
    evidence.pop("registry_id", None)
    evidence.pop("revision_digest", None)
    evidence["registry"] = copy.deepcopy(registry_state)


def _unresolved_decision(
    records: list[RecordDocument], reason_code: str
) -> RecordDocument:
    approval = _approval(records)
    decision = copy.deepcopy(approval.data)
    registry_state: Record = {
        "status": "unresolved",
        "registry_id": "neutral.registry",
        "reason_code": reason_code,
    }
    _set_registry_state(decision, registry_state)
    decision["outcome"] = "needs_human_review"
    decision["evaluated_at"] = "2026-07-01T00:00:02Z"
    decision["resolutions"] = [
        {
            "status": "unresolved",
            "class_id": "neutral.restricted_action",
            "allowance_reference": {
                "registry_id": "neutral.registry",
                "allowance_id": "neutral.allowance.1",
            },
            "reason_code": reason_code,
        }
    ]
    findings = decision["findings"]
    assert isinstance(findings, list)
    finding = findings[0]
    assert isinstance(finding, dict)
    finding["disposition"] = "needs_human_review"
    _refresh_deterministic_evidence(decision)
    return RecordDocument(approval.path, decision)


def _authority_without_decisions(records: list[RecordDocument]) -> list[RecordDocument]:
    return [
        record for record in records if record.data.get("kind") != "compliance_decision"
    ]


def _root_authority(records: list[RecordDocument]) -> list[RecordDocument]:
    return [
        record
        for record in _authority_without_decisions(records)
        if record.data.get("kind") != "policy_allowance_revocation"
        and not (
            record.data.get("kind") == "policy_allowance_registry"
            and record.data.get("revision_id") != "neutral.revision.1"
        )
    ]


def test_registry_when_no_current_head_then_not_found_is_valid() -> None:
    # Given
    records = _positive()
    decision = _unresolved_decision(records, "registry_not_found")
    authority = [
        record
        for record in _authority_without_decisions(records)
        if record.data.get("kind")
        not in {"policy_allowance_registry", "policy_allowance_revocation"}
    ]

    # When
    codes = _codes([*authority, decision])

    # Then
    assert codes == set()


def test_registry_when_multiple_current_heads_then_ambiguity_is_valid_but_fork_is_not() -> (
    None
):
    # Given
    records = _positive()
    decision = _unresolved_decision(records, "registry_head_ambiguous")
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    sibling = copy.deepcopy(latest.data)
    sibling["revision_id"] = "neutral.revision.sibling"
    sibling["revision_digest"] = canonical_digest(sibling, "revision_digest")

    # When
    codes = _codes(
        [
            *_authority_without_decisions(records),
            RecordDocument(latest.path, sibling),
            decision,
        ]
    )

    # Then
    assert codes == {"registry-chain-fork"}


@pytest.mark.parametrize(
    ("derived_reason", "reported_reason"),
    [
        ("registry_not_found", "registry_head_ambiguous"),
        ("registry_head_ambiguous", "registry_not_found"),
    ],
)
def test_registry_when_unresolved_reason_differs_from_derived_state_then_rejected(
    derived_reason: str, reported_reason: str
) -> None:
    # Given
    records = _positive()
    decision = _unresolved_decision(records, reported_reason)
    authority = _authority_without_decisions(records)
    if derived_reason == "registry_not_found":
        authority = [
            record
            for record in authority
            if record.data.get("kind")
            not in {"policy_allowance_registry", "policy_allowance_revocation"}
        ]
    else:
        latest = next(
            record
            for record in records
            if record.data.get("kind") == "policy_allowance_registry"
            and record.data.get("revision_id") == "neutral.revision.2"
        )
        sibling = copy.deepcopy(latest.data)
        sibling["revision_id"] = "neutral.revision.sibling"
        sibling["revision_digest"] = canonical_digest(sibling, "revision_digest")
        authority.append(RecordDocument(latest.path, sibling))

    # When
    codes = _codes([*authority, decision])

    # Then
    assert "current-registry" in codes
    assert "schema" not in codes


def test_registry_when_allowance_reason_differs_from_registry_state_then_rejected() -> (
    None
):
    # Given
    records = _positive()
    decision = _unresolved_decision(records, "registry_not_found")
    resolution = decision.data["resolutions"][0]
    assert isinstance(resolution, dict)
    resolution["reason_code"] = "registry_head_ambiguous"
    authority = [
        record
        for record in _authority_without_decisions(records)
        if record.data.get("kind")
        not in {"policy_allowance_registry", "policy_allowance_revocation"}
    ]

    # When
    codes = _codes([*authority, decision])

    # Then
    assert "allowance-resolution" in codes
    assert "current-registry" not in codes


def test_registry_when_unresolved_state_invents_revision_identity_then_schema_rejects() -> (
    None
):
    # Given
    records = _positive()
    decision = _unresolved_decision(records, "registry_not_found")
    registry = decision.data["registry"]
    assert isinstance(registry, dict)
    registry["revision_id"] = "neutral.revision.invented"

    # When
    codes = _codes([decision])

    # Then
    assert "schema" in codes


def test_registry_when_resolved_revision_identity_is_not_exact_then_rejected() -> None:
    # Given
    records = _positive()
    approval = _approval(records)
    decision = copy.deepcopy(approval.data)
    root = next(
        record.data
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.1"
    )
    registry_state: Record = {
        "status": "resolved",
        "registry_id": root["registry_id"],
        "revision_id": "neutral.revision.substituted",
        "revision_digest": root["revision_digest"],
    }
    _set_registry_state(decision, registry_state)
    _refresh_deterministic_evidence(decision)
    authority = _root_authority(records)

    # When
    codes = _codes([*authority, RecordDocument(approval.path, decision)])

    # Then
    assert "current-registry" in codes
    assert "schema" not in codes


def test_deterministic_veto_when_no_allowance_is_claimed_then_block_is_valid() -> None:
    # Given
    records = _positive()
    approval = _approval(records)
    decision = copy.deepcopy(approval.data)
    decision["outcome"] = "block"
    decision["allowance_references"] = []
    decision["resolutions"] = []
    findings = decision["findings"]
    assert isinstance(findings, list)
    finding = findings[0]
    assert isinstance(finding, dict)
    finding["disposition"] = "block"
    _refresh_deterministic_evidence(decision)
    changed_records = [
        *_root_authority(records),
        RecordDocument(approval.path, decision),
    ]

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_satisfied_finding_when_allowance_resolution_is_missing_then_rejected() -> None:
    # Given
    records = _positive()
    approval = _approval(records)
    decision = copy.deepcopy(approval.data)
    decision["allowance_references"] = []
    decision["resolutions"] = []
    _refresh_deterministic_evidence(decision)
    changed_records = [
        *_root_authority(records),
        RecordDocument(approval.path, decision),
    ]

    # When
    codes = _codes(changed_records)

    # Then
    assert "allowance-claim-closure" in codes
