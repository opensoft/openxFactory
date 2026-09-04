from __future__ import annotations

from .canonical import canonical_digest
from .model import Finding, Record, as_record, as_records, as_strings


def classifier_findings(
    decision: Record, layer_findings: list[Record], vocabulary: Record | None
) -> list[Finding]:
    classifier = as_record(decision.get("classifier"))
    if classifier is None:
        evidence = as_record(decision.get("deterministic_evidence")) or {}
        if as_strings(evidence.get("ambiguity_refs")):
            return [
                Finding(
                    "classifier-outcome",
                    str(decision.get("decision_id")),
                    "deterministic ambiguity lacks bounded classifier evidence",
                )
            ]
        return []
    decision_id = str(decision.get("decision_id"))
    findings: list[Finding] = []
    limits = as_record(classifier.get("limits")) or {}
    actual = as_record(classifier.get("actual")) or {}
    for key in (
        "invocations",
        "turns",
        "input_bytes",
        "output_bytes",
        "output_tokens",
        "seconds",
    ):
        limit = limits.get(key)
        consumed = actual.get(key)
        if isinstance(limit, int) and isinstance(consumed, int) and consumed > limit:
            findings.append(
                Finding("classifier-limits", decision_id, f"{key} cap exceeded")
            )
    result = classifier.get("result")
    classifier_layers = [
        item for item in layer_findings if item.get("layer") == "classifier"
    ]
    if result == "no_veto_signal" and classifier_layers:
        findings.append(
            Finding("classifier-outcome", decision_id, "no-veto result added a finding")
        )
    if result != "no_veto_signal" and not classifier_layers:
        findings.append(
            Finding("classifier-outcome", decision_id, "classifier finding is missing")
        )
    if result == "veto_signal" and not any(
        item.get("disposition") in {"block", "needs_human_review"}
        for item in classifier_layers
    ):
        findings.append(
            Finding(
                "classifier-outcome",
                decision_id,
                "veto signal lacks a blocking or review disposition",
            )
        )
    if classifier.get("result_digest") != canonical_digest(classifier, "result_digest"):
        findings.append(Finding("canonical-digest", decision_id, "classifier result"))
    findings.extend(_coherence_findings(decision_id, classifier, actual))
    findings.extend(_trigger_findings(decision, classifier, vocabulary))
    return findings


def classifier_caps_exceeded(classifier: Record) -> bool:
    limits = as_record(classifier.get("limits")) or {}
    actual = as_record(classifier.get("actual")) or {}
    for key in (
        "invocations",
        "turns",
        "input_bytes",
        "output_bytes",
        "output_tokens",
        "seconds",
    ):
        limit = limits.get(key)
        consumed = actual.get(key)
        if type(limit) is int and type(consumed) is int and consumed > limit:
            return True
    return False


def _coherence_findings(
    decision_id: str, classifier: Record, actual: Record
) -> list[Finding]:
    invocations = actual.get("invocations")
    turns = actual.get("turns")
    result = classifier.get("result")
    successful_results = {"no_veto_signal", "veto_signal", "indeterminate"}
    if result not in successful_results | {"error"}:
        return []
    coherent = (
        result in successful_results and invocations == 1 and turns == 1
    ) or (result == "error" and invocations in {0, 1} and turns == 0)
    if coherent:
        return []
    return [
        Finding(
            "classifier-coherence",
            decision_id,
            "result is inconsistent with invocation and turn counts",
        )
    ]


def _trigger_findings(
    decision: Record, classifier: Record, vocabulary: Record | None
) -> list[Finding]:
    trigger = as_record(classifier.get("trigger")) or {}
    reference = trigger.get("reference")
    digest = trigger.get("digest")
    decision_id = str(decision.get("decision_id"))
    sensitive_surfaces = {
        surface
        for class_record in as_records(
            vocabulary.get("classes") if vocabulary is not None else None
        )
        if (metadata := as_record(class_record.get("detection_metadata"))) is not None
        for surface in as_strings(metadata.get("sensitive_surface_ids"))
    }
    vocabulary_digest = (
        vocabulary.get("vocabulary_digest") if vocabulary is not None else None
    )
    evidence = as_record(decision.get("deterministic_evidence")) or {}
    valid_by_kind = {
        "policy_sensitive_surface": reference in sensitive_surfaces
        and digest == vocabulary_digest,
        "deterministic_ambiguity": reference in as_strings(
            evidence.get("ambiguity_refs")
        )
        and digest == evidence.get("evidence_digest"),
    }
    valid = valid_by_kind.get(str(trigger.get("kind")))
    if valid is None:
        return []
    if valid:
        return []
    return [
        Finding(
            "classifier-trigger",
            decision_id,
            "classifier trigger does not resolve to bound deterministic evidence",
        )
    ]
