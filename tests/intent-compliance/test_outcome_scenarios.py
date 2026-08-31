from __future__ import annotations

import copy
from pathlib import Path

from scripts.intent_compliance.evidence_validation import decision_digest
from scripts.intent_compliance.model import (
    Record,
    RecordDocument,
    load_record_documents,
)
from scripts.intent_compliance.state_validation import canonical_digest
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _classifier(decision: Record, result: str) -> Record:
    classifier: Record = {
        "trigger": {
            "kind": "policy_sensitive_surface",
            "reference": "neutral.sensitive_surface",
            "digest": decision["vocabulary"]["vocabulary_digest"],
        },
        "model": {"model_id": "neutral.classifier", "version": "1"},
        "limits": {
            "invocations": 1,
            "turns": 1,
            "input_bytes": 64,
            "output_bytes": 64,
            "output_tokens": 16,
            "seconds": 1,
        },
        "actual": {
            "invocations": 1,
            "turns": 1,
            "input_bytes": 8,
            "output_bytes": 8,
            "output_tokens": 2,
            "seconds": 1,
        },
        "result": result,
        "result_digest": "sha256:" + "0" * 64,
    }
    classifier["result_digest"] = canonical_digest(classifier, "result_digest")
    return classifier


def _refresh_evidence(decision: Record) -> None:
    evidence = decision["deterministic_evidence"]
    assert isinstance(evidence, dict)
    evidence["finding_digests"] = sorted(
        canonical_digest(finding, "__absent_digest_field__")
        for finding in decision["findings"]
        if isinstance(finding, dict) and finding.get("layer") == "deterministic"
    )
    evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")
    authorization = decision.get("dispatch_authorization_evidence")
    if isinstance(authorization, dict):
        authorization["decision_digest"] = decision_digest(decision)
        authorization["evidence_digest"] = canonical_digest(
            authorization, "evidence_digest"
        )


def _bind_current_registry(decision: Record, records: list[RecordDocument]) -> None:
    current = next(
        record.data
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    decision["registry"] = {
        "status": "resolved",
        "registry_id": current["registry_id"],
        "revision_id": current["revision_id"],
        "revision_digest": current["revision_digest"],
    }
    decision["deterministic_evidence"]["registry"] = copy.deepcopy(decision["registry"])
    decision["evaluated_at"] = "2026-06-01T00:00:02Z"
    revocations = current["allowances"][0]["revocation_digests"]
    for resolution in decision["resolutions"]:
        if resolution.get("status") == "resolved":
            resolution["revocation_digests"] = copy.deepcopy(revocations)
    for finding in decision["findings"]:
        if finding.get("layer") == "deterministic":
            finding["disposition"] = "block"


def test_clean_content_when_no_veto_class_applies_then_allow_is_valid() -> None:
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if changed.get("kind") == "compliance_decision":
            changed["outcome"] = "allow"
            changed["allowance_references"] = []
            changed["resolutions"] = []
            changed["findings"] = []
            changed["rationale_codes"] = ["neutral.no_restricted_action"]
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_revoked_allowance_when_effective_then_block_is_valid() -> None:
    # Given
    records = _positive()
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
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if changed.get("kind") == "compliance_decision":
            if changed.get("enforcement_point") != "approval":
                continue
            changed["outcome"] = "block"
            offset = {"approval": 0, "dispatch": 1, "admission": 2}[
                str(changed["enforcement_point"])
            ]
            changed["evaluated_at"] = f"2026-07-01T00:00:0{offset}Z"
            changed["registry"] = {
                "status": "resolved",
                "registry_id": latest["registry_id"],
                "revision_id": latest["revision_id"],
                "revision_digest": latest["revision_digest"],
            }
            changed["resolutions"][0]["revocation_digests"] = [
                revocation["revocation_digest"]
            ]
            changed["findings"][0]["disposition"] = "block"
            evidence = changed["deterministic_evidence"]
            evidence["registry"] = copy.deepcopy(changed["registry"])
            changed.pop("dispatch_authorization_evidence", None)
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_unresolved_allowance_when_current_head_revokes_then_review_is_rejected() -> (
    None
):
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if (
            changed.get("kind") == "compliance_decision"
            and changed.get("enforcement_point") == "admission"
        ):
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
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == {"allowance-resolution"}


def test_unresolved_allowance_when_absent_then_review_is_valid() -> None:
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if (
            changed.get("kind") == "compliance_decision"
            and changed.get("enforcement_point") != "approval"
        ):
            continue
        if (
            changed.get("kind") == "compliance_decision"
            and changed.get("enforcement_point") == "approval"
        ):
            missing_reference = {
                "registry_id": "neutral.registry",
                "allowance_id": "neutral.allowance.missing",
            }
            changed["outcome"] = "needs_human_review"
            changed["allowance_references"] = [missing_reference]
            changed["resolutions"] = [
                {
                    "status": "unresolved",
                    "class_id": "neutral.restricted_action",
                    "allowance_reference": copy.deepcopy(missing_reference),
                    "reason_code": "allowance_not_found",
                }
            ]
            _bind_current_registry(changed, records)
            changed["findings"][0]["disposition"] = "needs_human_review"
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_classifier_when_no_veto_signal_then_allow_is_valid() -> None:
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if changed.get("kind") == "compliance_decision":
            changed["classifier"] = _classifier(changed, "no_veto_signal")
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_classifier_when_veto_signal_then_block_is_valid() -> None:
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if changed.get("kind") == "compliance_decision":
            if changed.get("enforcement_point") != "approval":
                continue
            changed["outcome"] = "block"
            changed["classifier"] = _classifier(changed, "veto_signal")
            changed["findings"].append(
                {
                    "layer": "classifier",
                    "class_id": "neutral.restricted_action",
                    "disposition": "block",
                    "evidence_digest": changed["classifier"]["result_digest"],
                }
            )
            _bind_current_registry(changed, records)
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == set()


def test_classifier_when_current_head_revokes_then_review_is_rejected() -> None:
    # Given
    records = _positive()
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        if (
            changed.get("kind") == "compliance_decision"
            and changed.get("enforcement_point") != "approval"
        ):
            continue
        if changed.get("kind") == "compliance_decision":
            changed["outcome"] = "needs_human_review"
            changed["classifier"] = _classifier(changed, "veto_signal")
            changed["findings"].append(
                {
                    "layer": "classifier",
                    "class_id": "neutral.restricted_action",
                    "disposition": "needs_human_review",
                    "evidence_digest": changed["classifier"]["result_digest"],
                }
            )
            changed.pop("dispatch_authorization_evidence", None)
            _bind_current_registry(changed, records)
            _refresh_evidence(changed)
        changed_records.append(RecordDocument(record.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert codes == {"composition-outcome"}


def test_decision_when_resolution_is_duplicated_then_reference_is_rejected() -> None:
    # Given
    records = _positive()
    approval = next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == "approval"
    )
    changed = copy.deepcopy(approval.data)
    changed["resolutions"].append(copy.deepcopy(changed["resolutions"][0]))
    changed_records = [
        record for record in records if record.data.get("kind") != "compliance_decision"
    ]
    changed_records.append(RecordDocument(approval.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert "allowance-reference-substitution" in codes


def test_decision_when_ambiguity_has_no_classifier_then_review_is_required() -> None:
    # Given
    records = _positive()
    approval = next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == "approval"
    )
    changed = copy.deepcopy(approval.data)
    evidence = changed["deterministic_evidence"]
    evidence["ambiguity_refs"] = ["neutral.ambiguous.surface"]
    evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")
    changed_records = [
        record for record in records if record.data.get("kind") != "compliance_decision"
    ]
    changed_records.append(RecordDocument(approval.path, changed))

    # When
    codes = _codes(changed_records)

    # Then
    assert "classifier-outcome" in codes
