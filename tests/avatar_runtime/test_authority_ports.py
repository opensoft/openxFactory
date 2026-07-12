"""Fail-closed policy/consent + purpose mapping (ARR-003-S03/ARR-007-S01, FR-010/028)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode, PreflightKind

from _support import make_request


def test_policy_unavailable_denies_fail_closed(runtime, policy, provider):
    policy.available = False
    res = runtime.preflight(make_request("r1"))
    assert res.kind is PreflightKind.DENIAL
    assert res.outcome is OutcomeCode.AUTHORITY_UNAVAILABLE
    assert provider.create_count == 0


def test_consent_unavailable_denies_fail_closed(runtime, consent, provider):
    consent.available = False
    res = runtime.preflight(make_request("r1"))
    assert res.kind is PreflightKind.DENIAL
    assert res.outcome is OutcomeCode.CONSENT_REVOKED
    assert provider.create_count == 0


def test_purpose_mapping_absent_denies(runtime, provider):
    res = runtime.preflight(make_request("r1", purposes=frozenset({"avatar.unmapped"})))
    assert res.outcome is OutcomeCode.PURPOSE_UNMAPPED
    # Denied BEFORE any fake provider creation (FR-028).
    assert provider.create_count == 0


def test_unknown_registry_value_is_rejected():
    # Closed registries reject unknown values (constitution VII).
    import pytest

    from xfactory.avatar_runtime.values import OutcomeCode as OC

    with pytest.raises(ValueError):
        OC("not-a-real-outcome")
