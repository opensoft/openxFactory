from __future__ import annotations

import copy
from dataclasses import dataclass

from .canonical import canonical_digest
from .evidence_validation import decision_digest
from .model import JsonValue, Record, RecordDocument, as_record, as_records


@dataclass(slots=True)
class NegativeCorpusError(Exception):
    field: str

    def __str__(self) -> str:
        return f"negative-corpus baseline lacks record field: {self.field}"


def required_record(value: Record | None, field: str) -> Record:
    if value is None:
        raise NegativeCorpusError(field)
    return value


def kind_document(documents: list[RecordDocument], kind: str) -> RecordDocument:
    return next(item for item in documents if item.data.get("kind") == kind)


def gate_document(documents: list[RecordDocument], gate: str) -> RecordDocument:
    return next(
        item
        for item in documents
        if item.data.get("kind") == "compliance_decision"
        and item.data.get("enforcement_point") == gate
    )


def recompute_authority_state(documents: list[RecordDocument]) -> None:
    vocabulary = kind_document(documents, "veto_class_vocabulary").data
    vocabulary["vocabulary_digest"] = canonical_digest(
        vocabulary, "vocabulary_digest"
    )
    allowance = kind_document(documents, "policy_allowance").data
    vocabulary_ref = required_record(
        as_record(allowance.get("vocabulary")), "policy_allowance.vocabulary"
    )
    vocabulary_ref["vocabulary_digest"] = vocabulary["vocabulary_digest"]
    allowance["approval_digest"] = canonical_digest(allowance, "approval_digest")
    registries = sorted(
        [
            item.data
            for item in documents
            if item.data.get("kind") == "policy_allowance_registry"
        ],
        key=lambda item: str(item.get("published_at")),
    )
    root = registries[0]
    as_records(root.get("allowances"))[0]["approval_digest"] = allowance[
        "approval_digest"
    ]
    root["revision_digest"] = canonical_digest(root, "revision_digest")
    revocation = kind_document(documents, "policy_allowance_revocation").data
    revocation["approval_digest"] = allowance["approval_digest"]
    revocation["predecessor_revision_digest"] = root["revision_digest"]
    revocation["revocation_digest"] = canonical_digest(
        revocation, "revocation_digest"
    )
    child = registries[1]
    child["predecessor_revision_digest"] = root["revision_digest"]
    child_entry = as_records(child.get("allowances"))[0]
    child_entry["approval_digest"] = allowance["approval_digest"]
    child_entry["revocation_digests"] = [revocation["revocation_digest"]]
    child["revision_digest"] = canonical_digest(child, "revision_digest")
    for decision_document in (
        item for item in documents if item.data.get("kind") == "compliance_decision"
    ):
        decision = decision_document.data
        decision["vocabulary"] = {
            "vocabulary_id": vocabulary["vocabulary_id"],
            "vocabulary_digest": vocabulary["vocabulary_digest"],
        }
        registry = required_record(
            as_record(decision.get("registry")), "decision.registry"
        )
        deterministic = required_record(
            as_record(decision.get("deterministic_evidence")),
            "decision.deterministic_evidence",
        )
        resolution = as_records(decision.get("resolutions"))[0]
        selected = child if decision.get("enforcement_point") == "admission" else root
        selected_entry = as_records(selected.get("allowances"))[0]
        registry["revision_id"] = selected["revision_id"]
        registry["revision_digest"] = selected["revision_digest"]
        resolution["approval_digest"] = allowance["approval_digest"]
        resolution["revocation_digests"] = selected_entry["revocation_digests"]
        deterministic["vocabulary_digest"] = vocabulary["vocabulary_digest"]
        deterministic["revision_digest"] = selected["revision_digest"]
        authorization = as_record(decision.get("dispatch_authorization_evidence"))
        if authorization is not None:
            authorization["conditioned_revision_digest"] = root["revision_digest"]


def refresh_all_evidence(documents: list[RecordDocument]) -> None:
    for document in documents:
        decision = document.data
        if decision.get("kind") != "compliance_decision":
            continue
        deterministic = required_record(
            as_record(decision.get("deterministic_evidence")),
            "decision.deterministic_evidence",
        )
        finding_digests = sorted(
            canonical_digest(finding, "__absent_digest_field__")
            for finding in as_records(decision.get("findings"))
            if finding.get("layer") == "deterministic"
        )
        digest_values: list[JsonValue] = []
        digest_values.extend(finding_digests)
        deterministic["finding_digests"] = digest_values
        deterministic["evidence_digest"] = canonical_digest(
            deterministic, "evidence_digest"
        )
        authorization = as_record(decision.get("dispatch_authorization_evidence"))
        if authorization is not None:
            authorization["decision_digest"] = decision_digest(decision)
            authorization["evidence_digest"] = canonical_digest(
                authorization, "evidence_digest"
            )


def append_reused_allowance(documents: list[RecordDocument]) -> None:
    original = kind_document(documents, "policy_allowance")
    reused = copy.deepcopy(original.data)
    scope = required_record(as_record(reused.get("scope")), "policy_allowance.scope")
    scope["scope_ref"] = "neutral.resource.2"
    scope["scope_digest"] = canonical_digest(scope, "scope_digest")
    reused["approval_digest"] = canonical_digest(reused, "approval_digest")
    documents.append(RecordDocument(original.path, reused))
    latest = max(
        (
            item
            for item in documents
            if item.data.get("kind") == "policy_allowance_registry"
        ),
        key=lambda item: str(item.data.get("published_at")),
    )
    child = copy.deepcopy(latest.data)
    child["revision_id"] = "neutral.revision.3"
    child["predecessor_revision_digest"] = latest.data["revision_digest"]
    child["published_at"] = "2026-06-01T00:00:02Z"
    entry = as_records(child.get("allowances"))[0]
    entry["approval_digest"] = reused["approval_digest"]
    entry["revocation_digests"] = []
    child["revision_digest"] = canonical_digest(child, "revision_digest")
    documents.append(RecordDocument(latest.path, child))
    admission = gate_document(documents, "admission").data
    registry = required_record(as_record(admission.get("registry")), "decision.registry")
    registry["revision_id"] = child["revision_id"]
    registry["revision_digest"] = child["revision_digest"]
    resolution = as_records(admission.get("resolutions"))[0]
    resolution["approval_digest"] = reused["approval_digest"]
    resolution["revocation_digests"] = []
    deterministic = required_record(
        as_record(admission.get("deterministic_evidence")),
        "decision.deterministic_evidence",
    )
    deterministic["revision_digest"] = child["revision_digest"]
