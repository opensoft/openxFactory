from __future__ import annotations

import copy
from pathlib import Path

from scripts.intent_compliance import enforcement_validation
from scripts.intent_compliance.canonical import canonical_digest
from scripts.intent_compliance.model import RecordDocument, load_record_documents
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


def test_decision_when_tuple_references_only_share_colon_encoding_then_rejected() -> None:
    left = [
        {"registry_id": "neutral.registry:a", "allowance_id": "neutral.b"}
    ]
    right = [
        {"registry_id": "neutral.registry", "allowance_id": "a:neutral.b"}
    ]

    left_keys = enforcement_validation.reference_keys(left)
    right_keys = enforcement_validation.reference_keys(right)

    assert left_keys != right_keys


def test_decision_when_no_signal_requires_block_then_unsupported_block_is_rejected() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["outcome"] = "block"
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    codes = _codes(changed_records)

    assert "composition-outcome" in codes


def test_decision_when_no_signal_requires_review_then_unsupported_review_is_rejected() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["outcome"] = "needs_human_review"
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    codes = _codes(changed_records)

    assert "composition-outcome" in codes


def test_decision_when_allowance_lookup_is_unresolved_then_schema_accepts_bounded_reason() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["outcome"] = "needs_human_review"
    changed["resolutions"] = [
        {
            "status": "unresolved",
            "class_id": "neutral.restricted_action",
            "allowance_reference": {
                "registry_id": "neutral.registry",
                "allowance_id": "neutral.allowance.1",
            },
            "reason_code": "allowance_not_found",
        }
    ]
    changed["findings"][0]["disposition"] = "needs_human_review"
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    codes = _codes(changed_records)

    assert "schema" not in codes


def test_decision_when_deterministic_finding_is_unclaimed_then_outcome_must_block() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["allowance_references"] = []
    changed["resolutions"] = []
    changed["findings"][0]["disposition"] = "needs_human_review"
    changed["outcome"] = "needs_human_review"
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    codes = _codes(changed_records)

    assert "allowance-claim-closure" in codes
    assert "composition-outcome" in codes


def test_decision_when_resolution_has_no_deterministic_finding_then_rejected() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["findings"] = []
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    assert "allowance-claim-closure" in _codes(changed_records)


def test_decision_when_covering_allowance_is_reported_as_block_then_rejected() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["outcome"] = "block"
    findings = changed["findings"]
    assert isinstance(findings, list)
    deterministic = findings[0]
    assert isinstance(deterministic, dict)
    deterministic["disposition"] = "block"
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    assert "allowance-disposition" in _codes(changed_records)


def test_decision_when_noncovering_allowance_is_reported_satisfied_then_rejected() -> None:
    records = _positive()
    approval = _approval(records)
    changed = copy.deepcopy(approval.data)
    changed["outcome"] = "block"
    resolutions = changed["resolutions"]
    assert isinstance(resolutions, list)
    resolution = resolutions[0]
    assert isinstance(resolution, dict)
    verdict = resolution["scope_verdict"]
    assert isinstance(verdict, dict)
    verdict["verdict"] = "does_not_cover"
    verdict["verdict_digest"] = canonical_digest(verdict, "verdict_digest")
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    assert "allowance-disposition" in _codes(changed_records)
