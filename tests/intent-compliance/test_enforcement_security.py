from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.intent_compliance.model import RecordDocument, load_record_documents
from scripts.intent_compliance.state_validation import canonical_digest
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _decision(records: list[RecordDocument], gate: str) -> RecordDocument:
    return next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == gate
    )


def test_allowance_when_revocation_is_effective_at_admission_then_allow_is_rejected() -> (
    None
):
    records = _positive()
    admission = _decision(records, "admission")
    latest = next(
        record.data
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    revocation = next(
        record.data
        for record in records
        if record.data.get("kind") == "policy_allowance_revocation"
    )
    changed = copy.deepcopy(admission.data)
    changed["outcome"] = "allow"
    changed["findings"][0]["disposition"] = "satisfied"
    changed["evaluated_at"] = "2026-07-01T00:00:00Z"
    changed["registry"] = {
        "status": "resolved",
        "registry_id": latest["registry_id"],
        "revision_id": latest["revision_id"],
        "revision_digest": latest["revision_digest"],
    }
    resolution = changed["resolutions"][0]
    resolution["revocation_digests"] = [revocation["revocation_digest"]]
    deterministic = changed["deterministic_evidence"]
    deterministic["registry"] = copy.deepcopy(changed["registry"])
    deterministic["evidence_digest"] = canonical_digest(
        deterministic, "evidence_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed) if record is admission else record
        for record in records
    ]

    assert "allowance-state" in _codes(changed_records)


def test_allowance_when_revoked_before_registry_update_then_allow_is_rejected() -> None:
    records = _positive()
    approval = _decision(records, "approval")
    changed = copy.deepcopy(approval.data)
    changed["evaluated_at"] = "2026-06-01T00:00:02Z"
    changed_records = [
        record for record in records if record.data.get("kind") != "compliance_decision"
    ]
    changed_records.append(RecordDocument(approval.path, changed))

    assert "allowance-state" in _codes(changed_records)


def test_decisions_when_only_completed_gates_are_present_then_corpus_is_accepted() -> (
    None
):
    records = _positive()
    without_admission = [
        record
        for record in records
        if not (
            record.data.get("kind") == "compliance_decision"
            and record.data.get("enforcement_point") == "admission"
        )
    ]

    assert "enforcement-gate-set" not in _codes(without_admission)


@pytest.mark.parametrize("gate", ["dispatch", "admission"])
def test_decisions_when_prefix_is_missing_then_gate_set_is_rejected(gate: str) -> None:
    records = _positive()
    selected = _decision(records, gate)
    changed_records = [
        record for record in records if record.data.get("kind") != "compliance_decision"
    ]
    changed_records.append(selected)

    assert "enforcement-gate-set" in _codes(changed_records)


def test_decision_when_reference_order_differs_then_set_still_matches() -> None:
    records = _positive()
    second_reference = {
        "registry_id": "neutral.registry",
        "allowance_id": "neutral.allowance.2",
    }
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if changed.get("kind") == "compliance_decision":
            changed["allowance_references"] = [
                second_reference,
                copy.deepcopy(changed["allowance_references"][0]),
            ]
            changed["resolutions"].append(
                {
                    "status": "unresolved",
                    "class_id": "neutral.restricted_action",
                    "allowance_reference": second_reference,
                    "reason_code": "allowance_not_found",
                }
            )
        changed_records.append(RecordDocument(record.path, changed))

    assert "allowance-reference-substitution" not in _codes(changed_records)


def test_decisions_when_later_gate_is_not_later_in_time_then_rejected() -> None:
    records = _positive()
    admission = _decision(records, "admission")
    changed = copy.deepcopy(admission.data)
    changed["evaluated_at"] = "2026-02-01T00:00:01Z"
    changed_records = [
        RecordDocument(record.path, changed) if record is admission else record
        for record in records
    ]

    assert "enforcement-sequence" in _codes(changed_records)


def test_allowance_when_expired_then_allow_outcome_is_rejected() -> None:
    records = _positive()
    allowance = next(
        record for record in records if record.data.get("kind") == "policy_allowance"
    )
    changed = copy.deepcopy(allowance.data)
    changed["valid_until"] = "2026-01-15T00:00:00Z"
    changed_records = [
        RecordDocument(record.path, changed) if record is allowance else record
        for record in records
    ]

    assert "composition-outcome" in _codes(changed_records)


def test_decisions_when_only_correlation_matches_then_it_does_not_supply_governance() -> (
    None
):
    records = _positive()
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    changed["governed_binding_id"] = "neutral.binding.substituted"
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    assert "dispatch-authorization-evidence-binding" in _codes(changed_records)


def test_decision_when_deterministic_evidence_is_missing_then_schema_rejects_it() -> (
    None
):
    records = _positive()
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    del changed["deterministic_evidence"]
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    assert "schema" in _codes(changed_records)


def test_dispatch_allow_when_evidence_is_missing_then_schema_rejects_it() -> None:
    records = _positive()
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    del changed["dispatch_authorization_evidence"]
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    assert "dispatch-authorization-evidence" in _codes(changed_records)


def test_dispatch_evidence_when_decision_binding_differs_then_rejected() -> None:
    records = _positive()
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    authorization = changed["dispatch_authorization_evidence"]
    assert isinstance(authorization, dict)
    authorization["decision_id"] = "neutral.decision.other"
    authorization["evidence_digest"] = canonical_digest(
        authorization, "evidence_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    assert "dispatch-authorization-evidence-binding" in _codes(changed_records)


def test_decision_when_redacted_detail_is_free_form_then_schema_rejects_it() -> None:
    records = _positive()
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    changed["redacted_detail"] = "raw free-form detail"
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    assert "schema" in _codes(changed_records)
