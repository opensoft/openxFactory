"""Usage quota/duration outcomes + attributed credential-free records (ARR-007-S05, FR-032)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode, PreflightKind

from _support import TENANT, make_request


def test_concurrency_cap_emits_quota_and_records(runtime, usage):
    usage.set_active(TENANT, 2)  # concurrency_cap == 2
    res = runtime.preflight(make_request("r1"))
    assert res.kind is PreflightKind.TERMINAL
    assert res.outcome is OutcomeCode.QUOTA_EXCEEDED
    assert usage.records[-1].outcome is OutcomeCode.QUOTA_EXCEEDED
    assert usage.records[-1].tenant_ref == TENANT  # attributed
    # No answer/credential fields on a usage record (credential-free).
    assert not hasattr(usage.records[-1], "answer")


def test_duration_cap_outcome(runtime, policy_bundle):
    out = runtime.usage_meter.cap_outcome(
        policy_bundle, TENANT, requested_duration=policy_bundle.duration_cap_ticks + 1
    )
    assert out is OutcomeCode.DURATION_EXCEEDED


def test_within_caps_grants(runtime, usage):
    usage.set_active(TENANT, 0)
    res = runtime.preflight(make_request("r1"))
    assert res.kind is PreflightKind.GRANT
