"""Broker preflight — grant|denial|terminal totality, second-instance (ARR-004-S05, FR-012/017)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode, PreflightKind

from _support import make_request


def test_preflight_returns_exactly_one_grant(runtime, provider):
    res = runtime.preflight(make_request("req-1"))
    assert res.kind is PreflightKind.GRANT
    assert res.grant is not None and res.denial is None and res.terminal is None
    assert res.carries_credential()
    assert provider.create_count == 1


def test_only_grant_carries_credential(runtime, provider):
    res = runtime.preflight(make_request("req-x", subject_id="unknown-subject"))
    assert res.kind is PreflightKind.DENIAL
    assert res.outcome is OutcomeCode.AUTHORITY_UNAVAILABLE
    assert not res.carries_credential()
    assert provider.create_count == 0


def test_second_instance_denied_without_revoking_active(runtime):
    a = runtime.preflight(make_request("req-a", session_id="s", instance_id="A"))
    assert a.kind is PreflightKind.GRANT
    b = runtime.preflight(make_request("req-b", session_id="s", instance_id="B"))
    assert b.kind is PreflightKind.DENIAL
    assert b.outcome is OutcomeCode.SECOND_INSTANCE_DENIED
    session = runtime.registry.get("s")
    assert session.active_instance_id == "A"
    assert session.pending_attempt.lease.active
