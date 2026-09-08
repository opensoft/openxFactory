from __future__ import annotations

from pathlib import Path

from .model import Finding, RecordDocument, as_record
from .schema_validation import schema_findings, schema_validators
from .semantic_validation import raw_evidence_findings, semantic_findings


def validate_governed_documents(
    documents: list[RecordDocument], family_dir: Path
) -> list[Finding]:
    validators = schema_validators(family_dir)
    schema_results = [
        (document, schema_findings(document, validators)) for document in documents
    ]
    findings = [
        finding for _, document_findings in schema_results for finding in document_findings
    ]
    findings.extend(raw_evidence_findings(documents))
    findings.extend(
        Finding(
            "dispatch-authorization-evidence",
            str(document.data.get("decision_id")),
            "dispatch allow lacks static authorization evidence",
        )
        for document, _ in schema_results
        if document.data.get("kind") == "compliance_decision"
        and document.data.get("enforcement_point") == "dispatch"
        and document.data.get("outcome") == "allow"
        and as_record(document.data.get("dispatch_authorization_evidence")) is None
    )
    if any(finding.code == "schema" for finding in findings):
        return findings
    findings.extend(semantic_findings(documents))
    return findings
