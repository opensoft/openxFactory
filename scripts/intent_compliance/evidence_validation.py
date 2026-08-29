from __future__ import annotations

from .canonical import canonical_digest
from .model import Finding, Record, as_record, as_records
from .temporal import parse_timestamp


def dispatch_evidence_findings(decision: Record, head: Record) -> list[Finding]:
    evidence = as_record(decision.get("dispatch_authorization_evidence"))
    decision_id = str(decision.get("decision_id"))
    if (
        decision.get("enforcement_point") == "dispatch"
        and decision.get("outcome") == "allow"
        and evidence is None
    ):
        return [
            Finding(
                "dispatch-authorization-evidence",
                decision_id,
                "dispatch allow lacks static evidence",
            )
        ]
    if evidence is None:
        return []
    evaluator = as_record(decision.get("evaluator")) or {}
    expected = {
        "decision_id": decision.get("decision_id"),
        "evaluated_content_digest": decision.get("evaluated_content_digest"),
        "registry_id": head.get("registry_id"),
        "conditioned_revision_digest": head.get("revision_digest"),
        "evaluator_id": evaluator.get("evaluator_id"),
        "evaluator_version": evaluator.get("version"),
        "decision_digest": decision_digest(decision),
    }
    if any(evidence.get(key) != value for key, value in expected.items()):
        return [
            Finding(
                "dispatch-authorization-evidence-binding",
                decision_id,
                "evidence fields differ from decision",
            )
        ]
    if evidence.get("evidence_digest") != canonical_digest(
        evidence, "evidence_digest"
    ):
        return [Finding("canonical-digest", decision_id, "dispatch evidence")]
    if parse_timestamp(evidence.get("expires_at")) <= parse_timestamp(
        decision.get("evaluated_at")
    ):
        return [
            Finding(
                "dispatch-authorization-evidence-binding",
                decision_id,
                "evidence validity ended before evaluation",
            )
        ]
    return []


def deterministic_evidence_findings(
    decision: Record, head: Record
) -> list[Finding]:
    evidence = as_record(decision.get("deterministic_evidence"))
    if evidence is None:
        return []
    vocabulary = as_record(decision.get("vocabulary")) or {}
    evaluator = as_record(decision.get("evaluator")) or {}
    expected = {
        "evaluated_content_digest": decision.get("evaluated_content_digest"),
        "vocabulary_id": vocabulary.get("vocabulary_id"),
        "vocabulary_digest": vocabulary.get("vocabulary_digest"),
        "registry_id": head.get("registry_id"),
        "revision_digest": head.get("revision_digest"),
        "evaluator_id": evaluator.get("evaluator_id"),
        "evaluator_version": evaluator.get("version"),
        "finding_digests": sorted(
            canonical_digest(finding, "__absent_digest_field__")
            for finding in as_records(decision.get("findings"))
            if finding.get("layer") == "deterministic"
        ),
    }
    decision_id = str(decision.get("decision_id"))
    findings: list[Finding] = []
    if any(evidence.get(key) != value for key, value in expected.items()):
        findings.append(
            Finding(
                "deterministic-evidence-binding",
                decision_id,
                "evidence identity differs",
            )
        )
    if evidence.get("evidence_digest") != canonical_digest(evidence, "evidence_digest"):
        findings.append(
            Finding("canonical-digest", decision_id, "deterministic evidence")
        )
    return findings


def decision_digest(decision: Record) -> str:
    content = {
        key: value
        for key, value in decision.items()
        if key != "dispatch_authorization_evidence"
    }
    return canonical_digest(content, "__absent_digest_field__")
