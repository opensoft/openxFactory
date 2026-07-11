"""All-session / per-profile kill switches (ARR-007-S03, FR-031)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import KillSwitchState, OutcomeCode, PreflightKind

from _support import PROFILE, make_request


def test_all_session_kill_denies_new(runtime):
    runtime.kill_switch = KillSwitchState(all_session=True)
    res = runtime.preflight(make_request("r1"))
    assert res.kind is PreflightKind.TERMINAL
    assert res.outcome is OutcomeCode.KILLED


def test_profile_kill_denies_only_matching(runtime):
    runtime.kill_switch = KillSwitchState(disabled_profiles=frozenset({PROFILE}))
    blocked = runtime.preflight(make_request("r1", profile=PROFILE))
    assert blocked.outcome is OutcomeCode.KILLED
    allowed = runtime.preflight(
        make_request("r2", session_id="s2", profile="profile-other")
    )
    assert allowed.kind is PreflightKind.GRANT


def test_active_lease_revoked_only_when_policy_requests(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    att = runtime.registry.get("s").pending_attempt

    # Switch without revoke policy: active lease survives.
    runtime.activate_kill_switch(
        KillSwitchState(all_session=True, revoke_active_on_activate=False)
    )
    assert att.lease.active and not att.is_terminal

    # Switch with revoke policy: active lease revoked.
    revoked = runtime.activate_kill_switch(
        KillSwitchState(all_session=True, revoke_active_on_activate=True)
    )
    assert "s" in revoked
    assert not att.lease.active and att.terminal_result is OutcomeCode.KILLED
