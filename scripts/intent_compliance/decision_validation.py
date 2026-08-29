from __future__ import annotations

from .classifier_validation import classifier_caps_exceeded, classifier_findings
from .enforcement_validation import enforcement_findings, reference_keys
from .model import Finding, Record, as_record, as_records
from .temporal import parse_timestamp


def decision_findings(records: list[Record]) -> list[Finding]:
    findings: list[Finding] = []
    chains: dict[str, list[Record]] = {}
    vocabularies = {
        (str(record.get("vocabulary_id")), str(record.get("vocabulary_digest"))): record
        for record in records
        if record.get("kind") == "veto_class_vocabulary"
    }
    approvals = {
        (
            str(record.get("registry_id")),
            str(record.get("allowance_id")),
            str(record.get("approval_digest")),
        ): record
        for record in records
        if record.get("kind") == "policy_allowance"
    }
    for decision in (
        record for record in records if record.get("kind") == "compliance_decision"
    ):
        decision_id = str(decision.get("decision_id"))
        references = reference_keys(as_records(decision.get("allowance_references")))
        resolutions = [
            as_record(item.get("allowance_reference")) or {}
            for item in as_records(decision.get("resolutions"))
        ]
        resolution_keys = reference_keys(resolutions)
        if (
            len(references) != len(set(references))
            or len(resolution_keys) != len(set(resolution_keys))
            or set(references) != set(resolution_keys)
        ):
            findings.append(
                Finding(
                    "allowance-reference-substitution",
                    decision_id,
                    "reference sets differ",
                )
            )
        deterministic_classes = [
            str(item.get("class_id"))
            for item in as_records(decision.get("findings"))
            if item.get("layer") == "deterministic"
        ]
        resolution_classes = [
            str(item.get("class_id"))
            for item in as_records(decision.get("resolutions"))
        ]
        if (
            len(deterministic_classes) != len(set(deterministic_classes))
            or len(resolution_classes) != len(set(resolution_classes))
            or set(deterministic_classes) != set(resolution_classes)
        ):
            findings.append(
                Finding(
                    "allowance-claim-closure",
                    decision_id,
                    "deterministic finding and resolution classes differ",
                )
            )
        vocabulary_ref = as_record(decision.get("vocabulary")) or {}
        vocabulary = vocabularies.get(
            (
                str(vocabulary_ref.get("vocabulary_id")),
                str(vocabulary_ref.get("vocabulary_digest")),
            )
        )
        findings.extend(_outcome_findings(decision, vocabulary, approvals))
        binding_id = str(decision.get("governed_binding_id"))
        chains.setdefault(binding_id, []).append(decision)
    findings.extend(enforcement_findings(chains))
    return findings

def _outcome_findings(
    decision: Record,
    vocabulary: Record | None,
    approvals: dict[tuple[str, str, str], Record],
) -> list[Finding]:
    decision_id = str(decision.get("decision_id"))
    findings: list[Finding] = []
    classifier = as_record(decision.get("classifier"))
    if (
        decision.get("outcome") == "allow"
        and classifier is not None
        and classifier.get("result") != "no_veto_signal"
    ):
        findings.append(
            Finding(
                "classifier-outcome",
                decision_id,
                "non-no classifier result allowed",
            )
        )
    layer_findings = as_records(decision.get("findings"))
    expected_outcome = _derived_outcome(decision, layer_findings, approvals)
    if decision.get("outcome") != expected_outcome:
        findings.append(
            Finding(
                "composition-outcome",
                decision_id,
                f"outcome must be exactly {expected_outcome}",
            )
        )
    findings.extend(classifier_findings(decision, layer_findings, vocabulary))
    findings.extend(_scope_findings(decision))
    findings.extend(_derived_composition_findings(decision, layer_findings))
    return findings


def _derived_outcome(
    decision: Record,
    layer_findings: list[Record],
    approvals: dict[tuple[str, str, str], Record],
) -> str:
    dispositions = {str(item.get("disposition")) for item in layer_findings}
    resolutions = as_records(decision.get("resolutions"))
    scope_verdicts = {
        str(scope.get("verdict"))
        for resolution in resolutions
        if (scope := as_record(resolution.get("scope_verdict"))) is not None
    }
    classifier = as_record(decision.get("classifier"))
    classifier_result = None if classifier is None else classifier.get("result")
    has_revocation = any(
        resolution.get("status") == "resolved"
        and bool(resolution.get("revocation_digests"))
        for resolution in resolutions
    )
    resolution_classes = {
        str(resolution.get("class_id")) for resolution in resolutions
    }
    has_unclaimed_deterministic_finding = any(
        finding.get("layer") == "deterministic"
        and str(finding.get("class_id")) not in resolution_classes
        for finding in layer_findings
    )
    evaluated_at = parse_timestamp(decision.get("evaluated_at"))
    has_inactive_allowance = any(
        resolution.get("status") == "resolved"
        and (
            approval := approvals.get(
                (
                    str((as_record(resolution.get("allowance_reference")) or {}).get("registry_id")),
                    str((as_record(resolution.get("allowance_reference")) or {}).get("allowance_id")),
                    str(resolution.get("approval_digest")),
                )
            )
        )
        is not None
        and not (
            parse_timestamp(approval.get("valid_from"))
            <= evaluated_at
            < parse_timestamp(approval.get("valid_until"))
        )
        for resolution in resolutions
    )
    if (
        "block" in dispositions
        or "does_not_cover" in scope_verdicts
        or has_revocation
        or has_inactive_allowance
        or has_unclaimed_deterministic_finding
    ):
        return "block"
    if (
        "needs_human_review" in dispositions
        or "indeterminate" in scope_verdicts
        or classifier_result in {"veto_signal", "indeterminate", "error"}
        or (classifier is not None and classifier_caps_exceeded(classifier))
        or any(resolution.get("status") == "unresolved" for resolution in resolutions)
    ):
        return "needs_human_review"
    return "allow"


def _derived_composition_findings(
    decision: Record, layer_findings: list[Record]
) -> list[Finding]:
    if decision.get("outcome") != "allow":
        return []
    covered_classes = {
        str(resolution.get("class_id"))
        for resolution in as_records(decision.get("resolutions"))
        if resolution.get("status") == "resolved"
        and (scope := as_record(resolution.get("scope_verdict"))) is not None
        and scope.get("verdict") == "covers"
    }
    unsatisfied = [
        str(finding.get("class_id"))
        for finding in layer_findings
        if finding.get("layer") == "deterministic"
        and finding.get("disposition") == "satisfied"
        and str(finding.get("class_id")) not in covered_classes
    ]
    if unsatisfied:
        return [
            Finding(
                "composition-outcome",
                str(decision.get("decision_id")),
                f"satisfied deterministic classes lack covering authority: {sorted(unsatisfied)}",
            )
        ]
    return []


def _scope_findings(decision: Record) -> list[Finding]:
    decision_id = str(decision.get("decision_id"))
    findings: list[Finding] = []
    for resolution in as_records(decision.get("resolutions")):
        scope = as_record(resolution.get("scope_verdict")) or {}
        verdict = scope.get("verdict")
        if verdict == "does_not_cover" and decision.get("outcome") != "block":
            findings.append(
                Finding(
                    "scope-outcome", decision_id, "non-covering scope did not block"
                )
            )
        if verdict == "indeterminate" and decision.get("outcome") == "allow":
            findings.append(
                Finding("scope-outcome", decision_id, "indeterminate scope allowed")
            )
    return findings
