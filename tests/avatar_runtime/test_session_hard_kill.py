"""The §7.2 session hard-kill on the EXISTING terminal (ALV-006-S01, task 6.1.3).

Proves the three things the task asks for and one thing it forbids: a session
crossing any of the three ruled per-session ceilings terminates; it terminates
through the duration-or-quota outcome the kernel already models, with lease
revocation and the same act the kill switch performs; a COST-triggered kill
carries an auditable reason distinguishable from an ordinary duration or quota
terminal; and no new terminal outcome or attempt status is introduced anywhere.
"""

from __future__ import annotations

import pytest

from xfactory.avatar_runtime import spend
from xfactory.avatar_runtime.values import (
    AttemptStatus,
    OutcomeCode,
    PreflightKind,
)

from _support import TENANT, make_request


def _granted(runtime, session_id="s"):
    result = runtime.preflight(make_request("r1", session_id=session_id))
    assert result.kind is PreflightKind.GRANT
    return runtime.registry.get(session_id).pending_attempt


# --- the three ceilings ---------------------------------------------------- #
def test_billable_unit_ceiling_hard_kills_through_the_quota_terminal(runtime, provider):
    attempt = _granted(runtime)
    call_ref = attempt.provider_call_ref
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)

    result = runtime.enforce_session_ceilings("s")

    assert result is not None and result.kind is PreflightKind.TERMINAL
    # The EXISTING quota terminal — nothing new was invented.
    assert result.outcome is OutcomeCode.QUOTA_EXCEEDED
    assert attempt.terminal_result is OutcomeCode.QUOTA_EXCEEDED
    assert attempt.status is AttemptStatus.REVOKED
    # ... plus lease revocation and the idempotent provider hangup.
    assert not attempt.lease.active
    assert provider.is_live(call_ref) is False
    # ... and the credential-free terminal the kernel already replays.
    assert not runtime.grants.has_secret("r1")
    assert not result.carries_credential()


def test_the_three_hundred_unit_ceiling_is_three_dollars(runtime):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)
    verdict = runtime.session_spend_verdict("s")
    assert verdict.usd_cents == spend.SESSION_SPEND_CEILING_USD_CENTS == 300


def test_duration_ceiling_hard_kills_through_the_duration_terminal(runtime, clock):
    attempt = _granted(runtime)
    clock.advance(spend.SESSION_DURATION_CEILING_TICKS)

    result = runtime.enforce_session_ceilings("s")

    assert result.outcome is OutcomeCode.DURATION_EXCEEDED
    assert attempt.terminal_result is OutcomeCode.DURATION_EXCEEDED
    assert not attempt.lease.active


def test_uncountable_cost_refuses_rather_than_proceeding_blind(runtime):
    # `uncountable_is: exhausted` — a broker that cannot determine its
    # accumulated cost refuses the session rather than running on unmetered.
    attempt = _granted(runtime)
    runtime.mark_spend_uncountable("s")

    result = runtime.enforce_session_ceilings("s")

    assert result.outcome is OutcomeCode.QUOTA_EXCEEDED
    assert attempt.status is AttemptStatus.REVOKED
    record = runtime.spend.records[-1]
    assert record.reason is spend.KillReason.COST_UNCOUNTABLE
    assert record.countable is False
    assert record.cost_triggered is True


def test_a_negative_attribution_is_uncountable_not_cheaper(runtime):
    _granted(runtime)
    runtime.attribute_spend("s", 40)
    runtime.attribute_spend("s", -100)
    assert runtime.session_spend_verdict("s").reason is spend.KillReason.COST_UNCOUNTABLE


def test_a_session_inside_every_ceiling_is_not_killed(runtime, clock):
    attempt = _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING - 1)
    clock.advance(spend.SESSION_DURATION_CEILING_TICKS - 1)

    assert runtime.enforce_session_ceilings("s") is None
    assert not attempt.is_terminal
    assert attempt.lease.active


def test_enforcement_is_idempotent_on_an_already_terminal_leg(runtime):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)
    first = runtime.enforce_session_ceilings("s")
    second = runtime.enforce_session_ceilings("s")
    assert first is not None and second is None
    assert len(runtime.spend.records) == 1


# --- the auditable, distinguishable reason --------------------------------- #
def test_cost_kill_reason_is_distinguishable_from_an_ordinary_quota_terminal(
    runtime, usage, telemetry
):
    """Same OutcomeCode, different reason — the distinction the spec requires."""
    # (1) An ORDINARY quota terminal: the policy bundle's concurrency cap.
    usage.set_active(TENANT, 2)  # concurrency_cap == 2
    ordinary = runtime.preflight(make_request("r-ordinary", session_id="s-ordinary"))
    assert ordinary.outcome is OutcomeCode.QUOTA_EXCEEDED
    ordinary_reason = telemetry.published[-1].reason

    # (2) A COST-triggered kill on the same outcome code.
    usage.set_active(TENANT, 0)
    _granted(runtime, "s-cost")
    runtime.attribute_spend("s-cost", spend.SESSION_BILLABLE_UNIT_CEILING)
    cost = runtime.enforce_session_ceilings("s-cost")
    assert cost.outcome is OutcomeCode.QUOTA_EXCEEDED
    cost_reason = telemetry.published[-1].reason

    assert cost_reason == spend.KillReason.COST_CEILING_EXCEEDED.value
    assert ordinary_reason == spend.KillReason.ORDINARY_QUOTA_EXCEEDED.value
    assert cost_reason != ordinary_reason
    # Both audit records survived redaction rather than being dropped.
    assert telemetry.dropped == 0
    assert {r.usage_outcome for r in telemetry.published} == {"quota_exceeded"}


def test_the_spend_record_carries_the_auditable_reason(runtime):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING + 5)
    runtime.enforce_session_ceilings("s")

    record = runtime.spend.records[-1]
    assert record.reason is spend.KillReason.COST_CEILING_EXCEEDED
    assert record.cost_triggered is True
    assert record.outcome is OutcomeCode.QUOTA_EXCEEDED
    assert record.tenant_ref == TENANT and record.session_id == "s"
    assert record.usd_cents == 305
    # Credential-free: no answer, no control descriptor, no SDP on the record.
    for forbidden in ("answer", "control_descriptor", "sdp_media", "held_answer"):
        assert not hasattr(record, forbidden)


def test_the_kill_leaves_an_attributed_credential_free_usage_record(runtime, usage):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)
    runtime.enforce_session_ceilings("s")

    record = usage.records[-1]
    assert record.tenant_ref == TENANT  # attributed
    assert record.attempt_ref == "r1"
    assert record.outcome is OutcomeCode.QUOTA_EXCEEDED
    assert not hasattr(record, "answer")  # credential-free


def test_a_duration_ceiling_kill_is_not_reported_as_cost_triggered(runtime, clock):
    _granted(runtime)
    clock.advance(spend.SESSION_DURATION_CEILING_TICKS)
    runtime.enforce_session_ceilings("s")

    record = runtime.spend.records[-1]
    assert record.reason is spend.KillReason.DURATION_CEILING_EXCEEDED
    assert record.cost_triggered is False
    assert runtime.spend.cost_triggered_kills() == []


def test_an_ordinary_terminal_is_not_reported_as_cost_triggered(runtime, consent):
    from _support import SUBJECT

    _granted(runtime)
    consent.invalidate(SUBJECT)
    runtime.revoke_consent("s")

    record = runtime.spend.records[-1]
    assert record.reason is spend.KillReason.NON_CEILING_TERMINAL
    assert record.cost_triggered is False
    assert record.outcome is OutcomeCode.CONSENT_REVOKED


# --- no new terminal, and the precedence is stated ------------------------- #
def test_every_ceiling_reason_terminates_through_an_existing_outcome():
    for reason, outcome in spend.REASON_OUTCOMES.items():
        assert isinstance(outcome, OutcomeCode)
        assert outcome in (OutcomeCode.QUOTA_EXCEEDED, OutcomeCode.DURATION_EXCEEDED)
        assert reason in spend.KillReason
    # `NON_CEILING_TERMINAL` is deliberately unmapped: it is not a ceiling trip.
    assert spend.KillReason.NON_CEILING_TERMINAL not in spend.REASON_OUTCOMES


def test_cost_outranks_duration_when_a_session_crosses_both(runtime, clock):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)
    clock.advance(spend.SESSION_DURATION_CEILING_TICKS)
    verdict = runtime.session_spend_verdict("s")
    # Stated precedence: the reason that carries an escalation is recorded.
    assert verdict.reason is spend.KillReason.COST_CEILING_EXCEEDED


def test_uncountable_outranks_a_counted_ceiling(runtime):
    _granted(runtime)
    runtime.attribute_spend("s", spend.SESSION_BILLABLE_UNIT_CEILING)
    runtime.mark_spend_uncountable("s")
    assert (
        runtime.session_spend_verdict("s").reason is spend.KillReason.COST_UNCOUNTABLE
    )


@pytest.mark.parametrize("session_id", ["never-opened", ""])
def test_enforcement_on_an_unknown_session_is_a_no_op(runtime, session_id):
    assert runtime.enforce_session_ceilings(session_id) is None
    assert runtime.spend.records == []
