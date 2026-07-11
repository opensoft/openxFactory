"""In-memory deterministic fakes for the injected ports (design D2/D6).

These live under the test tree only. They implement the port Protocols with a
fake provider (explicit create/sideband/hangup states) and fail-closed policy /
consent / operation / usage authorities.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

from xfactory.avatar_runtime.values import (
    ConfirmationDecision,
    ConsentBinding,
    PolicyBundle,
    UsageRecord,
)


class FakeProvider:
    """Explicit four-state media provider: create/sideband/verify/hangup.

    No network, no audio. ``hangup`` is idempotent.
    """

    def __init__(self) -> None:
        self._calls: dict[str, dict] = {}
        self._n = 0
        self.create_count = 0

    def create(self, offer_sdp: str) -> str:
        self._n += 1
        self.create_count += 1
        ref = f"call-{self._n:04d}"
        self._calls[ref] = {"sideband": "none", "live": True}
        return ref

    def open_sideband(self, call_ref: str) -> None:
        self._calls[call_ref]["sideband"] = "open"

    def verify_sideband(self, call_ref: str) -> None:
        # A test may verify only after open; enforce the two-step readiness.
        if self._calls[call_ref]["sideband"] not in ("open", "verified"):
            raise ValueError("sideband must be opened before verification")
        self._calls[call_ref]["sideband"] = "verified"

    def sideband_verified(self, call_ref: str) -> bool:
        return self._calls.get(call_ref, {}).get("sideband") == "verified"

    def hangup(self, call_ref: str) -> None:
        call = self._calls.get(call_ref)
        if call is not None:
            call["live"] = False  # idempotent

    def is_live(self, call_ref: str) -> bool:
        return self._calls.get(call_ref, {}).get("live", False)


class FakePolicy:
    """Fail-closed policy authority: unknown identity → None (deny)."""

    def __init__(self, bundles: Optional[dict[str, PolicyBundle]] = None) -> None:
        self._bundles = dict(bundles or {})
        self.available = True

    def resolve(self, identity_ref: str) -> Optional[PolicyBundle]:
        if not self.available:
            return None
        return self._bundles.get(identity_ref)


class FakeConsent:
    """Fail-closed consent authority: unknown subject → None (deny)."""

    def __init__(self, bindings: Optional[dict[str, ConsentBinding]] = None) -> None:
        self._bindings = dict(bindings or {})
        self.available = True

    def binding(self, subject_ref: str) -> Optional[ConsentBinding]:
        if not self.available:
            return None
        return self._bindings.get(subject_ref)

    def is_valid(self, binding: ConsentBinding) -> bool:
        return bool(binding.valid)

    def invalidate(self, subject_ref: str) -> None:
        b = self._bindings.get(subject_ref)
        if b is not None:
            self._bindings[subject_ref] = ConsentBinding(
                b.subject_ref, b.version, valid=False
            )


class FakeOperation:
    """Idempotent fixture operation handler under an external-operation key."""

    def __init__(self) -> None:
        self._done: dict[str, bool] = {}
        self.effects: list[str] = []

    def execute(
        self,
        external_operation_key: str,
        confirmation: ConfirmationDecision,
        now: int,
        effect: str,
    ) -> bool:
        # Fail-closed on a stale/superseded confirmation.
        if confirmation.superseded or now > confirmation.valid_until:
            return False
        if external_operation_key in self._done:
            return True  # idempotent — no repeated effect
        self._done[external_operation_key] = True
        self.effects.append(effect)
        return True


class FakeUsage:
    """In-memory append-only usage sink with a settable active-concurrency view."""

    def __init__(self) -> None:
        self.records: list[UsageRecord] = []
        self._active: dict[str, int] = defaultdict(int)

    def record(self, usage: UsageRecord) -> None:
        self.records.append(usage)

    def concurrency(self, tenant_ref: str) -> int:
        return self._active[tenant_ref]

    def set_active(self, tenant_ref: str, n: int) -> None:
        self._active[tenant_ref] = n


__all__ = [
    "FakeProvider",
    "FakePolicy",
    "FakeConsent",
    "FakeOperation",
    "FakeUsage",
]
