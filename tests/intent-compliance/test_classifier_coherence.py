from __future__ import annotations

from scripts.intent_compliance.classifier_validation import classifier_findings
from scripts.intent_compliance.decision_validation import _derived_outcome
from scripts.intent_compliance.model import Record


def _decision(result: str, invocations: int, turns: int) -> Record:
    return {
        "decision_id": "neutral.decision.classifier",
        "classifier": {
            "trigger": {
                "kind": "deterministic_ambiguity",
                "reference": "neutral.ambiguity",
                "digest": "sha256:" + "a" * 64,
            },
            "limits": {
                "invocations": 1,
                "turns": 1,
                "input_bytes": 64,
                "output_bytes": 64,
                "output_tokens": 16,
                "seconds": 1,
            },
            "actual": {
                "invocations": invocations,
                "turns": turns,
                "input_bytes": 0,
                "output_bytes": 0,
                "output_tokens": 0,
                "seconds": 0,
            },
            "result": result,
            "result_digest": "sha256:" + "b" * 64,
        },
    }


def test_classifier_when_no_signal_has_no_completed_turn_then_rejected() -> None:
    # Given
    decision = _decision("no_veto_signal", invocations=0, turns=0)

    # When
    findings = classifier_findings(decision, [], None)

    # Then
    assert "classifier-coherence" in {finding.code for finding in findings}


def test_classifier_when_error_has_turn_without_invocation_then_rejected() -> None:
    # Given
    decision = _decision("error", invocations=0, turns=1)

    # When
    findings = classifier_findings(decision, [], None)

    # Then
    assert "classifier-coherence" in {finding.code for finding in findings}


def test_classifier_when_actual_consumption_exceeds_cap_then_outcome_requires_review() -> None:
    decision = _decision("no_veto_signal", invocations=1, turns=1)
    classifier = decision["classifier"]
    assert isinstance(classifier, dict)
    actual = classifier["actual"]
    assert isinstance(actual, dict)
    actual["input_bytes"] = 65

    assert _derived_outcome(decision, [], {}) == "needs_human_review"
