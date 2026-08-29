from __future__ import annotations

import copy
from pathlib import Path

from .canonical import canonical_digest
from .model import (
    InputLimitError,
    JsonValue,
    Record,
    RecordDocument,
    as_record,
    as_records,
    bounded_yaml_text,
    load_single_mapping_text,
)
from .negative_state import (
    append_reused_allowance as _append_reused_allowance,
)
from .negative_state import (
    gate_document as _gate,
)
from .negative_state import (
    kind_document as _kind,
)
from .negative_state import (
    recompute_authority_state as _recompute_authority_state,
)
from .negative_state import (
    refresh_all_evidence as _refresh_all_evidence,
)
from .negative_state import (
    required_record as _required_record,
)


def _json_records(records: list[Record]) -> list[JsonValue]:
    values: list[JsonValue] = []
    values.extend(records)
    return values


def negative_case_documents(
    fixture_path: Path,
    baseline: list[RecordDocument],
    *,
    fixture_text: str | None = None,
) -> list[RecordDocument]:
    fixture = load_single_mapping_text(
        fixture_text if fixture_text is not None else bounded_yaml_text(fixture_path),
        fixture_path,
    )
    if fixture.get("schema_version") != 1:
        raise InputLimitError(fixture_path, "negative fixture schema_version must be 1")
    if fixture.get("kind") != "intent_compliance_negative_fixture":
        raise InputLimitError(
            fixture_path,
            "negative fixture kind must be intent_compliance_negative_fixture",
        )
    mutation = fixture.get("mutation")
    documents = copy.deepcopy(baseline)
    match mutation:
        case "duplicate_class_id":
            vocabulary = _kind(documents, "veto_class_vocabulary")
            classes = as_records(vocabulary.data.get("classes"))
            classes.append(copy.deepcopy(classes[0]))
            vocabulary.data["classes"] = _json_records(classes)
            _recompute_authority_state(documents)
        case "unauthorized_issuer":
            issuer = _required_record(
                as_record(_kind(documents, "policy_allowance").data.get("issuer")),
                "policy_allowance.issuer",
            )
            issuer["authority_role"] = "neutral.unauthorized_role"
            _recompute_authority_state(documents)
        case "unauthorized_revoker":
            revoker = _required_record(
                as_record(
                    _kind(documents, "policy_allowance_revocation").data.get(
                        "revoker"
                    )
                ),
                "policy_allowance_revocation.revoker",
            )
            revoker["authority_role"] = "neutral.unauthorized_role"
            _recompute_authority_state(documents)
        case "classifier_error_as_allow":
            decision = _gate(documents, "dispatch").data
            classifier = _classifier("error", decision)
            classifier["result_digest"] = canonical_digest(classifier, "result_digest")
            decision["classifier"] = classifier
            layer_findings = as_records(decision.get("findings"))
            layer_findings.append(
                {
                    "layer": "classifier",
                    "class_id": "neutral.classifier_signal",
                    "disposition": "needs_human_review",
                    "evidence_digest": "sha256:" + "c" * 64,
                }
            )
            decision["findings"] = _json_records(layer_findings)
        case "missing_classifier_limits":
            decision = _gate(documents, "dispatch").data
            classifier = _classifier("no_veto_signal", decision)
            del classifier["limits"]
            classifier["result_digest"] = canonical_digest(classifier, "result_digest")
            decision["classifier"] = classifier
        case "raw_intent_evidence":
            _gate(documents, "dispatch").data["raw_intent"] = "forbidden"
        case "indeterminate_scope_as_allow":
            decision = _gate(documents, "dispatch").data
            resolution = as_records(decision.get("resolutions"))[0]
            verdict = _required_record(
                as_record(resolution.get("scope_verdict")),
                "resolution.scope_verdict",
            )
            verdict["verdict"] = "indeterminate"
            verdict["verdict_digest"] = canonical_digest(verdict, "verdict_digest")
            finding = as_records(decision.get("findings"))[0]
            finding["disposition"] = "needs_human_review"
        case "approval_content_changed":
            decision = _gate(documents, "dispatch").data
            changed_digest = "sha256:" + "a" * 64
            decision["evaluated_content_digest"] = changed_digest
            resolution = as_records(decision.get("resolutions"))[0]
            verdict = _required_record(
                as_record(resolution.get("scope_verdict")),
                "resolution.scope_verdict",
            )
            deterministic = _required_record(
                as_record(decision.get("deterministic_evidence")),
                "decision.deterministic_evidence",
            )
            authorization = _required_record(
                as_record(decision.get("dispatch_authorization_evidence")),
                "decision.dispatch_authorization_evidence",
            )
            verdict["evaluated_content_digest"] = changed_digest
            verdict["verdict_digest"] = canonical_digest(verdict, "verdict_digest")
            deterministic["evaluated_content_digest"] = changed_digest
            deterministic["evidence_digest"] = canonical_digest(deterministic, "evidence_digest")
            authorization["evaluated_content_digest"] = changed_digest
            authorization["evidence_digest"] = canonical_digest(
                authorization, "evidence_digest"
            )
        case "allowance_reference_substitution":
            _gate(documents, "dispatch").data["allowance_references"] = [
                {"registry_id": "neutral.registry", "allowance_id": "neutral.allowance.other"}
            ]
        case "unclaimed_veto_as_allow":
            for decision_document in (
                item
                for item in documents
                if item.data.get("kind") == "compliance_decision"
            ):
                decision_document.data["allowance_references"] = []
                decision_document.data["resolutions"] = []
        case "hermes_review_as_allow":
            decision = _gate(documents, "dispatch").data
            layer_findings = as_records(decision.get("findings"))
            layer_findings.append(
                {
                    "layer": "hermes",
                    "class_id": "neutral.context_review",
                    "disposition": "needs_human_review",
                    "evidence_digest": "sha256:" + "f" * 64,
                }
            )
            decision["findings"] = _json_records(layer_findings)
        case "reused_allowance_id":
            _append_reused_allowance(documents)
            documents = [
                item
                for item in documents
                if item.data.get("kind") != "compliance_decision"
            ]
        case _:
            raise ValueError(f"unknown negative-corpus mutation: {mutation}")
    _refresh_all_evidence(documents)
    return documents


def _classifier(result: str, decision: Record) -> Record:
    vocabulary = _required_record(
        as_record(decision.get("vocabulary")), "decision.vocabulary"
    )
    actual: Record = {
        "invocations": 1,
        "turns": 1,
        "input_bytes": 100,
        "output_bytes": 50,
        "output_tokens": 10,
        "seconds": 1,
    }
    if result == "error":
        actual = {
            "invocations": 0,
            "turns": 0,
            "input_bytes": 0,
            "output_bytes": 0,
            "output_tokens": 0,
            "seconds": 0,
        }
    return {
        "trigger": {
            "kind": "policy_sensitive_surface",
            "reference": "neutral.sensitive_surface",
            "digest": vocabulary["vocabulary_digest"],
        },
        "model": {"model_id": "neutral.classifier", "version": "1"},
        "limits": {
            "invocations": 1,
            "turns": 1,
            "input_bytes": 1024,
            "output_bytes": 512,
            "output_tokens": 128,
            "seconds": 10,
        },
        "actual": actual,
        "result": result,
        "result_digest": "sha256:" + "0" * 64,
    }
