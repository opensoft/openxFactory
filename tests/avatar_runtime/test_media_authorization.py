"""Two-channel media authorization, sideband timeout, hostile identity (ARR-005-S01/S02, FR-018/019/020)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode

from _support import ack_for, make_request


def test_both_channels_emit_media_authorized_exactly_once(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    runtime.open_sideband("s")
    runtime.verify_sideband("s")
    ev = runtime.submit_lease_ack("s", ack_for(runtime, "s"))
    assert ev is not None and ev.payload == "media_authorized"
    # A second ack does not emit again.
    assert runtime.submit_lease_ack("s", ack_for(runtime, "s")) is None
    log = runtime.event_log("s").records()
    assert sum(1 for e in log if e.payload == "media_authorized") == 1


def test_authorization_withheld_until_both_channels_ready(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    # Lease ack before sideband verification -> withheld (None).
    assert runtime.submit_lease_ack("s", ack_for(runtime, "s")) is None
    runtime.open_sideband("s")
    runtime.verify_sideband("s")
    assert runtime.submit_lease_ack("s", ack_for(runtime, "s")) is not None


def test_sideband_missing_at_readiness_times_out(runtime, clock, provider):
    runtime.preflight(make_request("r1", session_id="s"))
    runtime.open_sideband("s")  # opened but not verified
    clock.advance(runtime.READINESS_TTL + 1)
    term = runtime.check_readiness("s")
    assert term.outcome is OutcomeCode.READINESS_TIMEOUT
    call = runtime.registry.get("s").pending_attempt.provider_call_ref
    assert not provider.is_live(call)


def test_hostile_identity_ack_rejected(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    runtime.open_sideband("s")
    runtime.verify_sideband("s")
    ev = runtime.submit_lease_ack(
        "s", ack_for(runtime, "s", transport_identity="transport-EVIL")
    )
    assert ev is None
    att = runtime.registry.get("s").pending_attempt
    assert not att.media_authorized_emitted
