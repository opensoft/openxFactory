"""An abort ends the MEDIA PLANE ONLY (ALV-008-S04, task 6.3.5).

THE PROOF, not the assertion. A session is driven to authorization, given a
governed command so its projection carries real state, then aborted under
ROLLBACK-A. The authority-owned workflow projection is compared BYTE FOR BYTE
across the abort, the policy-required records are shown to be retained
(append-only, nothing removed), and the media leg is shown to have terminated
with the released `revoked` token through the landed consent-withdraw path.

The ROLLBACK-B half proves the other ruled mapping: a drained leg is
`abandoned`, unless it reached its own natural terminal inside the drain, in
which case it is an ordinary `completed`.
"""

from __future__ import annotations

from xfactory.avatar_runtime import rollback
from xfactory.avatar_runtime.values import (
    AttemptStatus,
    Command,
    KillSwitchState,
    OutcomeCode,
    PreflightKind,
    ProducerAuthority,
    SessionState,
)

from _support import PROFILE, authorize, make_request


def _live_session(runtime, session_id="s", request_id="r1"):
    """A granted, authorized session carrying a real projection."""
    result = runtime.preflight(
        make_request(request_id, session_id=session_id, profile=PROFILE)
    )
    assert result.kind is PreflightKind.GRANT
    authorize(runtime, session_id)  # appends the authoritative `media_authorized`
    accepted = runtime.submit_command(
        Command(command_id="c1", session_id=session_id, epoch=0, verb="speak")
    )
    assert accepted.accepted is True
    return runtime.registry.get(session_id).pending_attempt


# --- ROLLBACK-A: the abort ends media, and only media ---------------------- #
def test_rollback_a_abort_ends_the_media_plane_only(runtime, provider):
    attempt = _live_session(runtime)
    call_ref = attempt.provider_call_ref

    projection_before = runtime.workflow_projection("s")
    records_before = runtime.policy_required_records("s")
    assert projection_before.authoritative_events  # non-empty: real content
    assert projection_before.state_revision == 1

    decision = rollback.decide(
        rollback.RollbackClass.A,
        trigger="failed_consent_evaluation",
        profile=PROFILE,
    )
    outcome = runtime.apply_rollback(decision)
    assert "s" in outcome.revoked_sessions

    # (1) THE MEDIA LEG TERMINATED, with the released `revoked` token, through
    #     the same path consent withdrawal takes.
    assert attempt.status is AttemptStatus.REVOKED
    assert attempt.terminal_result is OutcomeCode.KILLED
    assert runtime.session_outcome("s") == "revoked"
    assert decision.session_outcome == "revoked"
    assert decision.session_outcome_path == "force_terminated_leg"
    assert not attempt.lease.active               # lease revoked
    assert provider.is_live(call_ref) is False    # capture stopped
    assert not runtime.grants.has_secret("r1")    # credential-free terminal
    assert attempt.held_answer is None and attempt.control_descriptor is None

    # (2) THE AUTHORITY-OWNED WORKFLOW PROJECTION IS BYTE-INTACT.
    projection_after = runtime.workflow_projection("s")
    assert projection_after == projection_before
    assert projection_after.serialize() == projection_before.serialize()
    assert projection_after.digest() == projection_before.digest()
    assert projection_after.authoritative_events == projection_before.authoritative_events

    # (3) THE LOGICAL SESSION SURVIVES. Revoking a leg ends media, never the
    #     governed record.
    session = runtime.registry.get("s")
    assert session is not None
    assert session.state is SessionState.ACTIVE
    assert session.epoch == 0 and session.state_revision == 1
    assert session.consent_version == 1 and session.policy_version == 1

    # (4) THE POLICY-REQUIRED RECORDS ARE RETAINED. Append-only across the
    #     abort: the authoritative events are unchanged and nothing that
    #     existed before is gone.
    records_after = runtime.policy_required_records("s")
    assert records_after.authoritative_events == records_before.authoritative_events
    assert set(records_before.credential_free_terminals) <= set(
        records_after.credential_free_terminals
    )
    assert set(records_before.spend_records) <= set(records_after.spend_records)
    assert len(records_after.credential_free_terminals) > len(
        records_before.credential_free_terminals
    )


def test_the_projection_digest_would_notice_a_change(runtime):
    """A negative control: the byte-intactness assertion is not vacuous."""
    _live_session(runtime)
    before = runtime.workflow_projection("s")
    runtime.append_observation(
        "s",
        ProducerAuthority.RUNTIME_AUTHORITY,
        "policy_decision_recorded",
        authoritative=True,
    )
    after = runtime.workflow_projection("s")
    assert after.digest() != before.digest()
    assert after.serialize() != before.serialize()


def test_the_abort_does_not_touch_the_event_log(runtime):
    attempt = _live_session(runtime)
    sequence_before = runtime.event_log("s").last_sequence
    records_before = runtime.event_log("s").records()

    runtime.apply_rollback(
        rollback.decide(
            rollback.RollbackClass.A, trigger="redaction_finding", profile=PROFILE
        )
    )

    assert runtime.event_log("s").last_sequence == sequence_before
    assert runtime.event_log("s").records() == records_before
    assert attempt.is_terminal


def test_a_second_session_projection_is_untouched_by_another_leg_abort(runtime):
    _live_session(runtime, "s1", "r1")
    _live_session(runtime, "s2", "r2")
    before = runtime.workflow_projection("s2")

    runtime.apply_rollback(
        rollback.decide(
            rollback.RollbackClass.A,
            trigger="media_authorization_ordering_violation",
            profile=PROFILE,
        )
    )

    # Both legs were revoked (the switch is ring-wide), and BOTH projections
    # are byte-intact.
    assert runtime.session_outcome("s1") == "revoked"
    assert runtime.session_outcome("s2") == "revoked"
    assert runtime.workflow_projection("s2").serialize() == before.serialize()


# --- ROLLBACK-B: the drained leg, and its two ruled tokens ----------------- #
def test_rollback_b_drain_ends_abandoned_when_the_window_closes(runtime, provider):
    attempt = _live_session(runtime)
    call_ref = attempt.provider_call_ref
    projection_before = runtime.workflow_projection("s")

    decision = rollback.decide(
        rollback.RollbackClass.B,
        trigger="material_regression_on_a_gated_percentile",
        profile=PROFILE,
    )
    outcome = runtime.apply_rollback(decision)

    # Nothing was revoked; the leg is left in flight to drain.
    assert outcome.revoked_sessions == ()
    assert not attempt.is_terminal and attempt.lease.active
    assert provider.is_live(call_ref) is True
    # New work is refused meanwhile.
    assert runtime.preflight(
        make_request("r-new", session_id="s-new", profile=PROFILE)
    ).outcome is OutcomeCode.KILLED

    # The drain window closes with the leg still in flight -> `abandoned`.
    assert runtime.close_drain_window("s") == "abandoned"
    assert attempt.status is AttemptStatus.ABANDONED
    assert decision.session_outcome == "abandoned"
    assert decision.session_outcome_path == "drained_leg_after_block_new"
    # `revoked` is refused for this path outright.
    assert runtime.session_outcome("s") != "revoked"
    # The projection is byte-intact across the drain too.
    assert runtime.workflow_projection("s").serialize() == projection_before.serialize()


def test_a_leg_that_reaches_its_natural_terminal_inside_the_drain_is_completed(runtime):
    attempt = _live_session(runtime)
    runtime.apply_rollback(
        rollback.decide(
            rollback.RollbackClass.B, trigger="elevated_error_rate", profile=PROFILE
        )
    )

    # The leg finished on its own before the window closed.
    assert runtime.complete_leg("s") == "completed"
    assert attempt.status is AttemptStatus.TERMINATED
    assert "completed" in rollback.DRAINED_LEG_ALSO_PERMITTED
    # Closing the window afterwards does not relabel a finished leg.
    assert runtime.close_drain_window("s") == "completed"


def test_the_records_survive_both_rollback_paths(runtime):
    for session_id, request_id, klass, trigger in (
        ("sa", "ra", rollback.RollbackClass.A, "failed_handoff_evaluation"),
        ("sb", "rb", rollback.RollbackClass.B, "elevated_quota_condition"),
    ):
        assert runtime.registry.get(session_id) is None
        # Clearing a switch is a SEPARATE decision with its own record (SOP
        # step 7); the second path is exercised from a cleared ring, not from
        # the first path's leftovers.
        runtime.kill_switch = KillSwitchState()
        _live_session(runtime, session_id, request_id)
        before = runtime.policy_required_records(session_id)
        runtime.apply_rollback(
            rollback.decide(klass, trigger=trigger, profile=PROFILE)
        )
        if klass is rollback.RollbackClass.B:
            runtime.close_drain_window(session_id)
        after = runtime.policy_required_records(session_id)
        assert after.authoritative_events == before.authoritative_events
        assert set(before.spend_records) <= set(after.spend_records)
        assert runtime.workflow_projection(session_id) is not None
