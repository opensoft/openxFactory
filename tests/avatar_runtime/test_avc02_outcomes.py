"""AVC-02 idempotency, changed-offer conflict (ARR-004-S01/S02, FR-013/014)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode, PreflightKind

from _support import make_request


def test_exact_offer_retry_coalesces_to_same_grant(runtime, provider):
    a = runtime.preflight(make_request("r1"))
    # Volatile fields differ; must still coalesce with no new provider call.
    b = runtime.preflight(
        make_request("r1", client_ts=999, transport_nonce="z", retry_count=3)
    )
    assert a.kind is b.kind is PreflightKind.GRANT
    assert a.grant.answer == b.grant.answer
    assert provider.create_count == 1


def test_changed_non_volatile_field_conflicts(runtime, provider):
    runtime.preflight(make_request("r1"))
    b = runtime.preflight(make_request("r1", sdp="m=video 9 UDP"))
    assert b.kind is PreflightKind.DENIAL
    assert b.outcome is OutcomeCode.IDEMPOTENCY_CONFLICT
    assert not b.carries_credential()
    assert provider.create_count == 1  # no second call


def test_changed_purposes_conflicts(runtime):
    runtime.preflight(make_request("r1"))
    b = runtime.preflight(make_request("r1", purposes=frozenset({"avatar.voice", "avatar.extra"})))
    assert b.outcome is OutcomeCode.IDEMPOTENCY_CONFLICT
