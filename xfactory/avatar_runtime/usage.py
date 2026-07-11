"""Usage metering + quota/duration outcomes (FR-032)."""

from __future__ import annotations

from typing import Optional

from .ports import UsagePort
from .values import OutcomeCode, PolicyBundle, UsageRecord


class UsageMeter:
    def __init__(self, usage: UsagePort) -> None:
        self._usage = usage

    def cap_outcome(
        self, bundle: PolicyBundle, tenant_ref: str, requested_duration: int = 0
    ) -> Optional[OutcomeCode]:
        """Return the canonical cap outcome, or None if within caps."""
        if self._usage.concurrency(tenant_ref) >= bundle.concurrency_cap:
            return OutcomeCode.QUOTA_EXCEEDED
        if requested_duration > bundle.duration_cap_ticks:
            return OutcomeCode.DURATION_EXCEEDED
        return None

    def record(
        self, tenant_ref: str, attempt_ref: str, outcome: OutcomeCode, clock_ts: int
    ) -> None:
        # Attributed, credential-free.
        self._usage.record(UsageRecord(tenant_ref, attempt_ref, outcome, clock_ts))
