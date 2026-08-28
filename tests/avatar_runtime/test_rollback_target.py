"""Rollback disables voice into text or human handoff (ALV-008-S03, task 6.3.4).

`gpt-realtime-2.1` is the FIRST qualified live profile, so no model fallback
exists and none may be implied in copy or in code. The last test in this file
greps the runtime package's own source for the copy that would let a reader
infer a hot-swap, because the constraint binds the WORDS as well as the branch.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from xfactory.avatar_runtime import rollback
from xfactory.avatar_runtime.values import (
    AttemptStatus,
    KillSwitchState,
    OutcomeCode,
    PreflightKind,
)

from _support import PROFILE, make_request

PKG = Path(__file__).resolve().parents[2] / "xfactory" / "avatar_runtime"


# --- the posture the session-creation path answers with -------------------- #
def test_rollback_disables_voice_and_offers_text_or_human_handoff(runtime):
    posture = runtime.rollback_posture()
    assert posture.voice_enabled is False
    # Both are members of the released `fallback-modes` registry.
    assert posture.offered_modes == ("text", "human_handoff")


def test_no_model_fallback_exists_and_none_is_offered(runtime):
    posture = runtime.rollback_posture()
    assert posture.model_fallback_exists is False
    assert rollback.MODEL_FALLBACK_EXISTS is False
    # Not "no fallback is enabled" — there is no other qualified profile at all.
    assert posture.qualified_profiles_remaining == ()
    assert posture.withdrawn_profile == rollback.CANDIDATE_PROFILE


def test_the_session_creation_path_refuses_and_carries_the_posture(runtime):
    decision = rollback.decide(
        rollback.RollbackClass.B,
        trigger="elevated_error_rate",
        profile=PROFILE,
    )
    outcome = runtime.apply_rollback(decision)

    refused = runtime.preflight(make_request("r1", profile=PROFILE))
    assert refused.kind is PreflightKind.TERMINAL
    assert refused.outcome is OutcomeCode.KILLED
    assert not refused.carries_credential()
    # ... and the answer the ring gives that refusal is text or human handoff.
    assert outcome.posture.voice_enabled is False
    assert outcome.posture.offered_modes == ("text", "human_handoff")
    assert outcome.posture.model_fallback_exists is False


def test_the_profile_switch_leaves_other_profiles_alone(runtime):
    decision = rollback.decide(
        rollback.RollbackClass.B, trigger="elevated_quota_condition", profile=PROFILE
    )
    runtime.apply_rollback(decision)
    assert decision.switch is rollback.KillSwitchId.PROFILE
    other = runtime.preflight(
        make_request("r2", session_id="s2", profile="profile-other")
    )
    assert other.kind is PreflightKind.GRANT


def test_a_condition_that_is_not_profile_specific_takes_the_wider_switch(runtime):
    decision = rollback.decide(
        rollback.RollbackClass.A,
        trigger="secret_scan_finding",
        profile=PROFILE,
        profile_specific=False,
    )
    assert decision.switch is rollback.KillSwitchId.ALL_NEW
    runtime.apply_rollback(decision)
    blocked = runtime.preflight(make_request("r3", session_id="s3", profile="anything"))
    assert blocked.outcome is OutcomeCode.KILLED


# --- the act is the EXISTING kill switch, with the ruled flags -------------- #
def test_the_act_is_the_existing_kill_switch_value():
    a = rollback.decide(rollback.RollbackClass.A, trigger="redaction_finding")
    state = a.kill_switch_state()
    assert isinstance(state, KillSwitchState)
    assert state.revoke_active_on_activate is True
    assert state.disabled_profiles == frozenset({rollback.CANDIDATE_PROFILE})
    assert state.all_session is False


def test_rollback_b_never_revokes_active_leases():
    """The mutation the policy's own validator is built to catch."""
    b = rollback.decide(
        rollback.RollbackClass.B, trigger="material_regression_on_a_gated_percentile"
    )
    assert b.revoke_active_leases is False
    assert b.kill_switch_state().revoke_active_on_activate is False
    assert rollback.CLASS_REVOKES_ACTIVE[rollback.RollbackClass.B] is False


def test_an_unrecorded_trigger_is_refused():
    with pytest.raises(rollback.RollbackPolicyError):
        rollback.decide(rollback.RollbackClass.A, trigger="looked_slow")
    # ... including a trigger that belongs to a DIFFERENT class.
    with pytest.raises(rollback.RollbackPolicyError):
        rollback.decide(rollback.RollbackClass.B, trigger="secret_scan_finding")


def test_operator_class_requires_the_operator_to_choose():
    with pytest.raises(rollback.RollbackPolicyError):
        rollback.decide(rollback.RollbackClass.C, trigger="cost_concern")
    revoking = rollback.decide(
        rollback.RollbackClass.C, trigger="cost_concern", operator_revokes_active=True
    )
    assert revoking.session_outcome == "revoked"
    blocking = rollback.decide(
        rollback.RollbackClass.C, trigger="quality_concern", operator_revokes_active=False
    )
    assert blocking.session_outcome == "abandoned"


def test_a_ruled_class_refuses_an_operator_override():
    with pytest.raises(rollback.RollbackPolicyError):
        rollback.decide(
            rollback.RollbackClass.B,
            trigger="elevated_error_rate",
            operator_revokes_active=True,
        )


# --- the outcome tokens are released registry members ---------------------- #
def test_every_declared_outcome_token_is_a_released_registry_member():
    released = {
        "granted", "denied", "completed", "abandoned", "expired", "revoked",
        "session_limit_reached",
    }
    declared = {
        v for v in rollback.CLASS_SESSION_OUTCOME.values() if v is not None
    } | set(rollback.DRAINED_LEG_ALSO_PERMITTED)
    assert declared <= released


def test_the_terminal_to_token_map_refuses_rather_than_guessing():
    assert rollback.session_outcome_token(AttemptStatus.REVOKED) == "revoked"
    assert rollback.session_outcome_token(AttemptStatus.ABANDONED) == "abandoned"
    assert rollback.session_outcome_token(AttemptStatus.EXPIRED) == "expired"
    assert (
        rollback.session_outcome_token(AttemptStatus.TERMINATED, OutcomeCode.CONNECTED)
        == "completed"
    )
    # Unbound terminals get None, not an inferred token.
    assert rollback.session_outcome_token(AttemptStatus.TIMED_OUT) is None
    assert rollback.session_outcome_token(AttemptStatus.TERMINATED) is None


# --- the copy constraint, checked against the package's own source --------- #
def test_no_source_in_the_package_implies_a_model_hot_swap():
    """6.3.4 binds the copy: nothing here may let a reader expect a swap."""
    forbidden = re.compile(
        r"fall\s*back\s+to\s+(?:another|a\s+(?:different|previous|prior|second))\s+model"
        r"|fall\s*back\s+to\s+(?:gpt|the\s+previous\s+profile)"
        r"|model[_\s-]?fallback\s*[:=]\s*(?:True|true|yes)"
        r"|hot[\s-]?swap"
        r"|swap\s+(?:to|in)\s+(?:another|a\s+different|the\s+previous)\s+(?:model|profile)"
        r"|previously\s+qualified\s+profile"
        r"|degrade\s+to\s+(?:another|a\s+different)\s+model",
        re.IGNORECASE,
    )
    offenders = []
    for path in sorted(PKG.rglob("*.py")):
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            if forbidden.search(line):
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert offenders == [], "\n".join(offenders)


def test_the_rollback_statement_says_there_is_nothing_to_swap_to():
    statement = rollback.ROLLBACK_TARGET_STATEMENT
    assert "no model fallback exists" in statement
    assert "no other qualified profile" in statement
    assert "text or human handoff" in statement.lower()
