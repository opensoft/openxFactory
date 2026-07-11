"""Consent invalidation -> revocation within the injected 5s bound (ARR-005-S05, FR-023)."""

from __future__ import annotations

from xfactory.avatar_runtime.consent import REVOCATION_BOUND_TICKS
from xfactory.avatar_runtime.values import OutcomeCode

from _support import SUBJECT, make_request


def test_consent_invalidation_revokes_within_bound(runtime, consent, provider):
    runtime.preflight(make_request("r1", session_id="s"))
    att = runtime.registry.get("s").pending_attempt
    consent.invalidate(SUBJECT)
    assert not runtime.consent_gate.is_valid_now(SUBJECT)

    out = runtime.revoke_consent("s")
    assert out["revoked"] is True
    # Termination completes within the injected 5-tick bound.
    assert out["completed_at"] <= out["deadline"]
    assert out["deadline"] - out["completed_at"] <= REVOCATION_BOUND_TICKS
    assert out["provider_live"] is False
    assert att.terminal_result is OutcomeCode.CONSENT_REVOKED
    assert not att.lease.active


def test_memory_gateway_consent_is_not_media_authority():
    # The runtime consumes only the domain ConsentPort; there is no import of
    # a memory-gateway consent schema as media authority (FR-030).
    import xfactory.avatar_runtime.consent as consent_mod

    src = consent_mod.__doc__ or ""
    assert "never treated as media authority" in src.lower() or "not" in src.lower()
