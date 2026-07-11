"""Control lease: expiry, reconnect credential rotation (ARR-005-S03/S04, FR-021/022)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import Command, OutcomeCode

from _support import make_request


def test_lease_expiry_stops_commands_and_terminates_idempotently(runtime, clock, provider):
    runtime.preflight(make_request("r1", session_id="s"))
    att = runtime.registry.get("s").pending_attempt
    call = att.provider_call_ref
    clock.advance(runtime.LEASE_EXPIRY_TTL + 1)
    term = runtime.check_lease("s")
    assert term.outcome is OutcomeCode.LEASE_EXPIRED
    assert not provider.is_live(call)
    # Idempotent: a second check does not error and the leg stays terminal.
    assert runtime.check_lease("s") is None
    # Governed commands now stop (lease revoked).
    res = runtime.submit_command(Command("c1", "s", 0, "speak"))
    assert not res.accepted


def test_stale_epoch_reconnect_rejected_without_state_change(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    lease = runtime.registry.get("s").pending_attempt.lease
    ok = runtime.reconnect("s", epoch=lease.epoch + 5, credential=lease.reconnect_credential)
    assert ok is False and lease.active


def test_rotated_credential_reconnect_rejected(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    lease = runtime.registry.get("s").pending_attempt.lease
    ok = runtime.reconnect("s", epoch=lease.epoch, credential="stale-credential")
    assert ok is False


def test_valid_reconnect_rotates_credential(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    lease = runtime.registry.get("s").pending_attempt.lease
    old = lease.reconnect_credential
    ok = runtime.reconnect("s", epoch=lease.epoch, credential=old)
    assert ok is True and lease.reconnect_credential != old
