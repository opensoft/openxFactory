from __future__ import annotations

import re
from typing import Final

from .decision_validation import decision_findings
from .model import (
    Finding,
    JsonValue,
    Record,
    RecordDocument,
    as_record,
    as_records,
    as_strings,
)
from .state_validation import state_findings

RAW_EVIDENCE_KEYS = {
    "full_prompt",
    "provider_payload",
    "raw_content",
    "raw_intent",
    "secret",
    "token",
}
RAW_EVIDENCE_PATTERNS: Final = (
    re.compile(r"sk(?:_|-)[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{16,}"),
    re.compile(r"(?i)bearer[ ]+[A-Za-z0-9._-]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{6,}"),
)


def semantic_findings(documents: list[RecordDocument]) -> list[Finding]:
    records = [document.data for document in documents]
    findings: list[Finding] = []
    findings.extend(_vocabulary_findings(records))
    findings.extend(_authority_findings(records))
    findings.extend(_identity_binding_findings(records))
    findings.extend(decision_findings(records))
    findings.extend(state_findings(records))
    return findings


def raw_evidence_findings(documents: list[RecordDocument]) -> list[Finding]:
    return list(
        dict.fromkeys(
            finding
            for document in documents
            for finding in _raw_evidence_findings(document.data, str(document.path))
        )
    )


def _class(
    records: list[Record], vocabulary_id: str, vocabulary_digest: str, class_id: str
) -> Record | None:
    vocabulary = next(
        (
            record
            for record in records
            if record.get("kind") == "veto_class_vocabulary"
            and record.get("vocabulary_id") == vocabulary_id
            and record.get("vocabulary_digest") == vocabulary_digest
        ),
        None,
    )
    if vocabulary is None:
        return None
    return next(
        (item for item in as_records(vocabulary.get("classes")) if item.get("class_id") == class_id),
        None,
    )


def _vocabulary_findings(records: list[Record]) -> list[Finding]:
    findings: list[Finding] = []
    for vocabulary in (
        record for record in records if record.get("kind") == "veto_class_vocabulary"
    ):
        class_ids = [
            class_id
            for item in as_records(vocabulary.get("classes"))
            if isinstance((class_id := item.get("class_id")), str)
        ]
        duplicates = {
            class_id for class_id in class_ids if class_ids.count(class_id) > 1
        }
        for class_id in sorted(str(item) for item in duplicates):
            findings.append(
                Finding(
                    "duplicate-class-id",
                    str(vocabulary.get("vocabulary_id")),
                    class_id,
                )
            )
    return findings


def _authority_findings(records: list[Record]) -> list[Finding]:
    findings: list[Finding] = []
    allowances = {
        (
            str(record.get("registry_id")),
            str(allowance_id),
            str(record.get("approval_digest")),
        ): record
        for record in records
        if record.get("kind") == "policy_allowance"
        and isinstance((allowance_id := record.get("allowance_id")), str)
    }
    for (_, allowance_id, _), allowance in allowances.items():
        vocabulary_ref = as_record(allowance.get("vocabulary")) or {}
        vocabulary_id = vocabulary_ref.get("vocabulary_id")
        vocabulary_digest = vocabulary_ref.get("vocabulary_digest")
        class_id = allowance.get("class_id")
        issuer = as_record(allowance.get("issuer")) or {}
        if all(
            isinstance(value, str)
            for value in (vocabulary_id, vocabulary_digest, class_id)
        ):
            class_record = _class(
                records,
                str(vocabulary_id),
                str(vocabulary_digest),
                str(class_id),
            )
            roles = as_strings(class_record.get("allowance_issuer_roles")) if class_record else []
            if issuer.get("authority_role") not in roles:
                findings.append(
                    Finding(
                        "authority-attribution",
                        allowance_id,
                        "issuer role does not resolve in the exact vocabulary identity",
                    )
                )
    for revocation in (record for record in records if record.get("kind") == "policy_allowance_revocation"):
        allowance_id = revocation.get("allowance_id")
        allowance = allowances.get(
            (
                str(revocation.get("registry_id")),
                str(allowance_id),
                str(revocation.get("approval_digest")),
            )
        )
        revoker = as_record(revocation.get("revoker")) or {}
        if allowance is None:
            continue
        vocabulary_ref = as_record(allowance.get("vocabulary")) or {}
        class_record = _class(
            records,
            str(vocabulary_ref.get("vocabulary_id")),
            str(vocabulary_ref.get("vocabulary_digest")),
            str(allowance.get("class_id")),
        )
        roles = as_strings(class_record.get("allowance_revoker_roles")) if class_record else []
        if revoker.get("authority_role") not in roles:
            findings.append(
                Finding(
                    "authority-attribution",
                    str(allowance_id),
                    "revoker role does not resolve in the exact vocabulary identity",
                )
            )
    return findings


def _identity_binding_findings(records: list[Record]) -> list[Finding]:
    vocabularies = {
        (str(item.get("vocabulary_id")), str(item.get("vocabulary_digest"))): item
        for item in records
        if item.get("kind") == "veto_class_vocabulary"
    }
    findings: list[Finding] = []
    allowances = [item for item in records if item.get("kind") == "policy_allowance"]
    for allowance in allowances:
        vocabulary_ref = as_record(allowance.get("vocabulary")) or {}
        vocabulary_key = (
            str(vocabulary_ref.get("vocabulary_id")),
            str(vocabulary_ref.get("vocabulary_digest")),
        )
        if vocabulary_key not in vocabularies:
            findings.append(
                Finding(
                    "vocabulary-binding",
                    str(allowance.get("allowance_id")),
                    "complete vocabulary identity does not resolve",
                )
            )
    for decision in (item for item in records if item.get("kind") == "compliance_decision"):
        decision_id = str(decision.get("decision_id"))
        vocabulary_ref = as_record(decision.get("vocabulary")) or {}
        vocabulary_key = (
            str(vocabulary_ref.get("vocabulary_id")),
            str(vocabulary_ref.get("vocabulary_digest")),
        )
        vocabulary = vocabularies.get(vocabulary_key)
        if vocabulary is None:
            findings.append(Finding("vocabulary-binding", decision_id, "complete vocabulary identity does not resolve"))
            continue
        if decision.get("policy_source") != vocabulary.get("policy_source"):
            findings.append(Finding("policy-source-binding", decision_id, "policy source identity differs from vocabulary"))
        allowance_by_identity = {
            (
                str(item.get("registry_id")),
                str(item.get("allowance_id")),
                str(item.get("approval_digest")),
            ): item
            for item in allowances
        }
        for resolution in as_records(decision.get("resolutions")):
            reference = as_record(resolution.get("allowance_reference")) or {}
            identity = (
                str(reference.get("registry_id")),
                str(reference.get("allowance_id")),
                str(resolution.get("approval_digest")),
            )
            allowance = allowance_by_identity.get(identity)
            if allowance is None:
                continue
            if allowance.get("vocabulary") != vocabulary_ref:
                findings.append(Finding("vocabulary-binding", decision_id, "allowance vocabulary differs"))
            if allowance.get("class_id") != resolution.get("class_id"):
                findings.append(Finding("allowance-resolution", decision_id, "resolved class differs"))
    return findings


def _raw_evidence_findings(
    value: JsonValue, source: str, path: str = ""
) -> list[Finding]:
    findings: list[Finding] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.[field]" if path else "[field]"
            if key.lower() in RAW_EVIDENCE_KEYS or _credential_shaped(key):
                findings.append(Finding("raw-evidence", source, child_path))
            findings.extend(_raw_evidence_findings(child, source, child_path))
    elif isinstance(value, list):
        for child in value:
            findings.extend(_raw_evidence_findings(child, source, f"{path}[]"))
    elif isinstance(value, str) and _credential_shaped(value):
        findings.append(Finding("raw-evidence", source, path or "<root>"))
    return findings


def _credential_shaped(value: str) -> bool:
    return any(pattern.search(value) for pattern in RAW_EVIDENCE_PATTERNS)
