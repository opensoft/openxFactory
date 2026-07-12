"""Fail-closed policy resolution + purpose mapping (FR-010/028)."""

from __future__ import annotations

from typing import Optional

from .ports import PolicyPort
from .values import PolicyBundle


class PolicyResolver:
    def __init__(self, policy: PolicyPort) -> None:
        self._policy = policy

    def resolve(self, identity_ref: str) -> Optional[PolicyBundle]:
        # Unknown / unavailable -> None (caller fails closed).
        return self._policy.resolve(identity_ref)

    @staticmethod
    def purposes_mapped(bundle: PolicyBundle, requested: frozenset[str]) -> bool:
        """A profile must map every requested neutral purpose (FR-028)."""
        return requested <= bundle.required_purposes
