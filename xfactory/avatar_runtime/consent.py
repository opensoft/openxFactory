"""Versioned consent + revocation within the injected 5-second bound (FR-023/030).

The memory-gateway consent schema is NEVER treated as media authority (FR-030):
this gate consumes only the domain ConsentPort.
"""

from __future__ import annotations

from typing import Optional

from .ports import ConsentPort
from .values import ConsentBinding

#: Revocation must complete within this many injected-clock ticks (FR-023).
REVOCATION_BOUND_TICKS = 5


class ConsentGate:
    def __init__(self, consent: ConsentPort) -> None:
        self._consent = consent

    def check(self, subject_ref: str) -> Optional[ConsentBinding]:
        """Return a valid binding, or None if unavailable/unknown/invalid (fail closed)."""
        binding = self._consent.binding(subject_ref)
        if binding is None:
            return None
        if not self._consent.is_valid(binding):
            return None
        return binding

    def is_valid_now(self, subject_ref: str) -> bool:
        return self.check(subject_ref) is not None
