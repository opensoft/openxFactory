"""The seven injected ports — the runtime's only external dependency surface.

Every nondeterministic or authoritative dependency enters here as a narrow
``typing.Protocol`` (structural, stdlib-only). Deterministic in-memory
implementations are supplied by tests (FR-007).
"""

from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable

from .values import (
    ConfirmationDecision,
    ConsentBinding,
    PolicyBundle,
    UsageRecord,
)


@runtime_checkable
class ClockPort(Protocol):
    def monotonic(self) -> int: ...
    def wall(self) -> int: ...


@runtime_checkable
class IdPort(Protocol):
    def next(self, kind: str) -> str: ...


@runtime_checkable
class ProviderPort(Protocol):
    def create(self, offer_sdp: str) -> str: ...
    def open_sideband(self, call_ref: str) -> None: ...
    def verify_sideband(self, call_ref: str) -> None: ...
    def sideband_verified(self, call_ref: str) -> bool: ...
    def hangup(self, call_ref: str) -> None: ...
    def is_live(self, call_ref: str) -> bool: ...


@runtime_checkable
class PolicyPort(Protocol):
    def resolve(self, identity_ref: str) -> Optional[PolicyBundle]: ...


@runtime_checkable
class ConsentPort(Protocol):
    def binding(self, subject_ref: str) -> Optional[ConsentBinding]: ...
    def is_valid(self, binding: ConsentBinding) -> bool: ...


@runtime_checkable
class OperationPort(Protocol):
    def execute(
        self,
        external_operation_key: str,
        confirmation: ConfirmationDecision,
        now: int,
        effect: str,
    ) -> bool: ...


@runtime_checkable
class UsagePort(Protocol):
    def record(self, usage: UsageRecord) -> None: ...
    def concurrency(self, tenant_ref: str) -> int: ...
