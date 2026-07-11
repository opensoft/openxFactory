"""Media-attempt lifecycle, fresh-resume replacement, one-leg (ARR-004-S03, FR-011/015)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import AttemptStatus, OutcomeCode, PreflightKind

from _support import make_request


def test_attempt_lifecycle_progresses(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    att = runtime.registry.get("s").pending_attempt
    assert att.status is AttemptStatus.ANSWER_HELD
    runtime.open_sideband("s")
    assert att.status is AttemptStatus.SIDEBAND_OPEN
    runtime.verify_sideband("s")
    assert att.status is AttemptStatus.SIDEBAND_VERIFIED


def test_fresh_resume_replaces_pending_leg(runtime, provider):
    runtime.preflight(make_request("r1", session_id="s", instance_id="A"))
    old = runtime.registry.get("s").pending_attempt
    res = runtime.preflight(
        make_request("r2", session_id="s", instance_id="A", resume_ref="r1")
    )
    assert res.kind is PreflightKind.GRANT
    assert old.is_terminal and old.terminal_result is OutcomeCode.ABANDONED
    # Exactly one pending leg — the replacement — and one extra provider call.
    assert runtime.registry.get("s").pending_attempt.request_id == "r2"
    assert provider.create_count == 2


def test_one_leg_without_resume_is_denied(runtime):
    runtime.preflight(make_request("r1", session_id="s", instance_id="A"))
    res = runtime.preflight(make_request("r2", session_id="s", instance_id="A"))
    assert res.kind is PreflightKind.DENIAL


def test_terminal_attempt_is_immutable(runtime):
    from xfactory.avatar_runtime.attempt import AttemptError

    runtime.preflight(make_request("r1", session_id="s"))
    att = runtime.registry.get("s").pending_attempt
    att.terminate(AttemptStatus.ABANDONED, OutcomeCode.ABANDONED)
    try:
        att.to(AttemptStatus.SIDEBAND_OPEN)
        assert False, "terminal attempt must reject mutation"
    except AttemptError:
        pass
