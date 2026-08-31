from __future__ import annotations

import copy
from pathlib import Path

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


def _new_evidence_shape(records: list[RecordDocument]) -> list[RecordDocument]:
    changed_records: list[RecordDocument] = []
    for record in records:
        changed = copy.deepcopy(record.data)
        evidence = changed.get("deterministic_evidence")
        if isinstance(evidence, dict):
            evidence["ambiguity_refs"] = []
            evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")
        authorization = changed.pop("dispatch_authorization", None)
        if isinstance(authorization, dict):
            authorization["evidence_digest"] = authorization.pop("token_digest")
            authorization["evidence_digest"] = canonical_digest(
                authorization, "evidence_digest"
            )
            changed["dispatch_authorization_evidence"] = authorization
        changed_records.append(RecordDocument(record.path, changed))
    return changed_records


def test_dispatch_allow_when_static_evidence_is_bound_then_corpus_is_accepted() -> None:
    # Given
    records = _new_evidence_shape(_positive())

    # When
    codes = _codes(records)

    # Then
    assert "schema" not in codes
    assert "dispatch-authorization-evidence" not in codes


def test_classifier_when_policy_sensitive_trigger_is_not_in_vocabulary_then_rejected() -> None:
    # Given
    records = _new_evidence_shape(_positive())
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    changed["outcome"] = "needs_human_review"
    changed["classifier"] = {
        "trigger": {
            "kind": "policy_sensitive_surface",
            "reference": "neutral.fake_sensitive_surface",
            "digest": changed["vocabulary"]["vocabulary_digest"],
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
        "result": "indeterminate",
        "result_digest": "sha256:" + "0" * 64,
    }
    classifier = changed["classifier"]
    assert isinstance(classifier, dict)
    classifier["result_digest"] = canonical_digest(classifier, "result_digest")
    changed["findings"] = [
        {
            "layer": "classifier",
            "class_id": "neutral.restricted_action",
            "disposition": "needs_human_review",
            "evidence_digest": "sha256:" + "d" * 64,
        }
    ]
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    # When
    codes = _codes(changed_records)

    # Then
    assert "classifier-trigger" in codes


def test_classifier_when_ambiguity_trigger_is_not_in_evidence_then_rejected() -> None:
    # Given
    records = _new_evidence_shape(_positive())
    dispatch = _decision(records, "dispatch")
    changed = copy.deepcopy(dispatch.data)
    evidence = changed["deterministic_evidence"]
    assert isinstance(evidence, dict)
    evidence["ambiguity_refs"] = ["neutral.actual_ambiguity"]
    evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")
    changed["classifier"] = {
        "trigger": {
            "kind": "deterministic_ambiguity",
            "reference": "neutral.fake_ambiguity",
            "digest": evidence["evidence_digest"],
        },
        "model": {"model_id": "neutral.classifier", "version": "1"},
        "limits": {"invocations": 1, "turns": 1, "input_bytes": 64, "output_bytes": 64, "output_tokens": 16, "seconds": 1},
        "actual": {"invocations": 0, "turns": 0, "input_bytes": 0, "output_bytes": 0, "output_tokens": 0, "seconds": 0},
        "result": "error",
        "result_digest": "sha256:" + "0" * 64,
    }
    classifier = changed["classifier"]
    assert isinstance(classifier, dict)
    classifier["result_digest"] = canonical_digest(classifier, "result_digest")
    changed["outcome"] = "needs_human_review"
    changed["findings"] = [{"layer": "classifier", "class_id": "neutral.restricted_action", "disposition": "needs_human_review", "evidence_digest": "sha256:" + "d" * 64}]
    changed_records = [
        RecordDocument(record.path, changed) if record is dispatch else record
        for record in records
    ]

    # When
    codes = _codes(changed_records)

    # Then
    assert "classifier-trigger" in codes
