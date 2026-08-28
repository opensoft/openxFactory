"""The auto-detection wiring behind the recorded rollback policy (task 6.3.3).

Two trips, and both of their fail-closed edges:

* The LATENCY trip fires ROLLBACK-B — auto-block-new, in-flight legs drain —
  only on a material regression against ALV-SLO-001, on a GATED cell, once the
  cell holds the declared n>=100. An under-sampled cell never trips
  (ALV-008-S02, ALV-005-S02).
* The SAFETY-EVAL trip fires ROLLBACK-A — auto-abort WITH active-lease
  revocation — only on a well-formed failing signal naming one of the eight
  recorded triggers. §6.2.1's corpus does not exist yet, so what is proved
  here is the input seam and its refusals: absent, malformed, foreign and
  unknown-trigger input NEVER trips (ALV-008-S01).
"""

from __future__ import annotations

import pytest

from xfactory.avatar_runtime import detection, rollback
from xfactory.avatar_runtime.detection import (
    CellVerdict,
    LatencySample,
    SafetyEvalSignal,
    SafetyVerdict,
)
from xfactory.avatar_runtime.values import AttemptStatus, OutcomeCode, PreflightKind

from _support import PROFILE, make_request

N = detection.DECLARED_SAMPLE_MINIMUM  # 100, declared before measuring


def _samples(classification, value_ms, *, count=N,
             platform="windows_desktop", network_class="nominal",
             interval="first_playable_after_authorized_ms", region=None):
    return [
        LatencySample(
            platform=platform,
            network_class=network_class,
            region=region,
            reference_classification=classification,
            interval=interval,
            value_ms=value_ms,
        )
        for _ in range(count)
    ]


def _cell(reference_ms, adapter_ms, *, count=N, **kw):
    return (
        _samples(detection.REFERENCE_CLASSIFICATION, reference_ms, count=count, **kw)
        + _samples(detection.ADAPTER_CLASSIFICATION, adapter_ms, count=count, **kw)
    )


# --- the ruled SLO ---------------------------------------------------------- #
def test_the_materiality_rule_is_the_greater_of_fifteen_percent_and_150ms():
    assert detection.RELATIVE_THRESHOLD_PCT == 15
    assert detection.ABSOLUTE_THRESHOLD_MS == 150
    # Fast interval: the 150 ms absolute floor dominates.
    assert detection.materiality_threshold_ms(400) == 400 + 150
    # Slow interval: 15% relative dominates.
    assert detection.materiality_threshold_ms(2_000) == 2_000 + 300


def test_a_material_regression_on_a_gated_cell_trips_rollback_b(runtime):
    evaluation, outcome = runtime.latency_detection(_cell(400, 600))

    assert evaluation.tripped
    assert all(c.verdict is CellVerdict.GATED_MATERIAL_REGRESSION for c in evaluation.trips)
    assert outcome is not None
    assert outcome.decision.rollback_class is rollback.RollbackClass.B
    assert outcome.decision.trigger == "material_regression_on_a_gated_percentile"
    # ROLLBACK-B blocks new sessions WITHOUT revoking active leases.
    assert outcome.decision.revoke_active_leases is False
    assert outcome.decision.mode is rollback.SwitchMode.BLOCK_NEW
    assert outcome.revoked_sessions == ()


def test_a_regression_inside_the_threshold_does_not_trip(runtime):
    evaluation, outcome = runtime.latency_detection(_cell(400, 549))
    assert not evaluation.tripped and outcome is None
    assert all(c.verdict is CellVerdict.GATED_PASS for c in evaluation.comparisons)


def test_both_gated_percentiles_are_evaluated(runtime):
    evaluation, _ = runtime.latency_detection(_cell(400, 420))
    assert {c.percentile for c in evaluation.comparisons} == {"p50", "p95"}


def test_in_flight_legs_are_left_to_drain_when_the_latency_trip_fires(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    attempt = runtime.registry.get("s").pending_attempt

    _, outcome = runtime.latency_detection(_cell(400, 900), profile=PROFILE)

    assert outcome is not None
    # The in-flight leg is untouched: not terminal, lease still active.
    assert not attempt.is_terminal and attempt.lease.active
    # New sessions on the profile are refused.
    blocked = runtime.preflight(make_request("r2", session_id="s2", profile=PROFILE))
    assert blocked.kind is PreflightKind.TERMINAL
    assert blocked.outcome is OutcomeCode.KILLED


# --- the n>=100 floor: an under-sampled cell NEVER trips -------------------- #
@pytest.mark.parametrize("count", [1, 30, N - 1])
def test_an_under_sampled_cell_never_trips(runtime, count):
    """At n=30 a p95 estimate is a maximum wearing a percentile's name."""
    evaluation, outcome = runtime.latency_detection(_cell(400, 5_000, count=count))

    assert not evaluation.tripped
    assert outcome is None
    assert all(
        c.verdict is CellVerdict.RECORDED_NOT_GATED_UNDER_MINIMUM
        for c in evaluation.comparisons
    )
    # Recorded, not gated: the numbers are still carried for a reader.
    assert all(c.adapter_ms == 5_000 for c in evaluation.comparisons)


def test_the_floor_applies_to_each_side_of_the_comparison(runtime):
    samples = (
        _samples(detection.REFERENCE_CLASSIFICATION, 400, count=N)
        + _samples(detection.ADAPTER_CLASSIFICATION, 5_000, count=N - 1)
    )
    evaluation, outcome = runtime.latency_detection(samples)
    assert not evaluation.tripped and outcome is None


def test_the_declared_minimum_is_one_hundred():
    assert detection.DECLARED_SAMPLE_MINIMUM == 100


# --- the gated set: nothing outside it may claim the gated tier ------------ #
@pytest.mark.parametrize(
    "kw",
    [
        {"platform": "android_handset"},          # not a gated platform
        {"network_class": "degraded"},            # recorded-not-gated tier
        {"network_class": "jittered"},
        {"interval": "teardown_to_terminal_ms"},  # recorded-not-gated interval
        {"interval": "speech_to_first_audio_ms"},
    ],
)
def test_a_cell_outside_the_gated_set_never_trips(runtime, kw):
    evaluation, outcome = runtime.latency_detection(_cell(400, 9_000, **kw))
    assert not evaluation.tripped and outcome is None
    assert all(
        c.verdict is CellVerdict.REFUSED_NOT_A_GATED_CELL for c in evaluation.comparisons
    )


def test_a_comparison_across_two_regions_is_refused_not_pooled(runtime):
    samples = (
        _samples(detection.REFERENCE_CLASSIFICATION, 400, region="eu")
        + _samples(detection.ADAPTER_CLASSIFICATION, 9_000, region="us")
    )
    evaluation, outcome = runtime.latency_detection(samples)
    assert not evaluation.tripped and outcome is None
    assert all(
        c.verdict is CellVerdict.REFUSED_INCOMPLETE_COMPARISON
        for c in evaluation.comparisons
    )


def test_a_one_sided_cell_is_refused(runtime):
    evaluation, outcome = runtime.latency_detection(
        _samples(detection.ADAPTER_CLASSIFICATION, 9_000)
    )
    assert not evaluation.tripped and outcome is None


# --- malformed latency input fails closed ---------------------------------- #
def test_malformed_samples_are_dropped_and_never_trip(runtime):
    class Foreign:
        platform = "windows_desktop"

    bad = [
        None,
        Foreign(),
        LatencySample("windows_desktop", "nominal", None,
                      detection.ADAPTER_CLASSIFICATION,
                      "first_playable_after_authorized_ms", -1),
        LatencySample("", "nominal", None, detection.ADAPTER_CLASSIFICATION,
                      "first_playable_after_authorized_ms", 9_000),
        LatencySample("windows_desktop", "nominal", None, "made_up_classification",
                      "first_playable_after_authorized_ms", 9_000),
    ]
    evaluation, outcome = runtime.latency_detection(bad)
    assert evaluation.malformed_samples == len(bad)
    assert not evaluation.tripped and outcome is None


def test_no_samples_at_all_never_trips(runtime):
    evaluation, outcome = runtime.latency_detection([])
    assert evaluation.comparisons == () and not evaluation.tripped
    assert outcome is None


# --- the safety-eval trip: ROLLBACK-A with active-lease revocation ---------- #
def _signal(trigger="failed_consent_evaluation", verdict="fail"):
    return SafetyEvalSignal(
        run_id="safety-run-1",
        corpus_ref="fixture:synthetic-evaluation-corpus",
        scenario_class="consent",
        trigger=trigger,
        verdict=verdict,
    )


def test_the_seam_names_its_unbuilt_corpus_owner():
    # §6.2.1 is unticked; the seam says so rather than implying a corpus exists.
    assert detection.SAFETY_CORPUS_OWNER == "qualify-avatar-live-voice 6.2.1"


def test_the_eight_recorded_triggers_are_the_whole_set():
    assert detection.SAFETY_TRIGGERS == frozenset(
        {
            "revocation_bound_violation",
            "failed_blocked_state_evaluation",
            "failed_exact_value_evaluation",
            "failed_consent_evaluation",
            "failed_handoff_evaluation",
            "redaction_finding",
            "secret_scan_finding",
            "media_authorization_ordering_violation",
        }
    )


@pytest.mark.parametrize("trigger", sorted(detection.SAFETY_TRIGGERS))
def test_every_recorded_trigger_aborts_with_lease_revocation(runtime, provider, trigger):
    runtime.preflight(make_request("r1", session_id="s"))
    attempt = runtime.registry.get("s").pending_attempt
    call_ref = attempt.provider_call_ref

    decision, outcome = runtime.safety_detection(_signal(trigger))

    assert decision.verdict is SafetyVerdict.TRIPPED
    assert outcome is not None
    assert outcome.decision.rollback_class is rollback.RollbackClass.A
    assert outcome.decision.revoke_active_leases is True
    assert outcome.decision.mode is rollback.SwitchMode.REVOKE_ACTIVE
    # The landed consent-withdraw terminal path, exactly: media revoked,
    # capture stopped, credential-free terminal, control channel healthy.
    assert "s" in outcome.revoked_sessions
    assert attempt.status is AttemptStatus.REVOKED
    assert not attempt.lease.active
    assert provider.is_live(call_ref) is False
    assert not runtime.grants.has_secret("r1")
    assert runtime.session_outcome("s") == "revoked"


@pytest.mark.parametrize(
    "signal,expected",
    [
        (None, SafetyVerdict.REFUSED_ABSENT),
        (object(), SafetyVerdict.REFUSED_MALFORMED),
        ("failed_consent_evaluation", SafetyVerdict.REFUSED_MALFORMED),
        (_signal(verdict="maybe"), SafetyVerdict.REFUSED_MALFORMED),
        (_signal(trigger="slow_response"), SafetyVerdict.REFUSED_UNKNOWN_TRIGGER),
        (_signal(verdict="pass"), SafetyVerdict.NO_TRIP_PASSED),
    ],
)
def test_an_absent_or_malformed_safety_signal_never_trips(runtime, signal, expected):
    """FAIL CLOSED IN THE DETECTOR'S DIRECTION: garbage must not revoke leases."""
    runtime.preflight(make_request("r1", session_id="s"))
    attempt = runtime.registry.get("s").pending_attempt

    decision, outcome = runtime.safety_detection(signal)

    assert decision.verdict is expected
    assert decision.trips is False
    assert outcome is None
    # No lease was revoked and no new session was blocked.
    assert not attempt.is_terminal and attempt.lease.active
    assert runtime.preflight(make_request("r2", session_id="s2")).kind is PreflightKind.GRANT


def test_an_empty_corpus_reference_is_malformed(runtime):
    signal = SafetyEvalSignal(
        run_id="run-1", corpus_ref="   ", scenario_class="consent",
        trigger="failed_consent_evaluation", verdict="fail",
    )
    decision, outcome = runtime.safety_detection(signal)
    assert decision.verdict is SafetyVerdict.REFUSED_MALFORMED
    assert outcome is None


def test_absence_is_reported_distinctly_from_a_pass(runtime):
    """"No evaluation arrived" is a gate condition, not a green light."""
    absent, _ = runtime.safety_detection(None)
    passed, _ = runtime.safety_detection(_signal(verdict="pass"))
    assert absent.verdict is not passed.verdict
    assert absent.verdict is SafetyVerdict.REFUSED_ABSENT
    assert "absence is not a pass" in absent.detail


def test_neither_detector_raises_on_foreign_input():
    """A detector that raises is a detector that has stopped detecting."""
    for value in (0, [], {}, b"bytes", 3.5, True):
        assert detection.evaluate_safety_signal(value).trips is False
    foreign = [0, "sample", b"", 3.5, {"value_ms": 9_000}]
    evaluation = detection.evaluate_latency(foreign)
    assert evaluation.tripped is False
    assert evaluation.malformed_samples == len(foreign)
