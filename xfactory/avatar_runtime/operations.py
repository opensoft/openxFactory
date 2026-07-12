"""Fixture operation execution — idempotent, confirmation-bound (FR-029)."""

from __future__ import annotations

from .ports import OperationPort
from .values import ConfirmationDecision


class OperationRunner:
    def __init__(self, operation: OperationPort) -> None:
        self._operation = operation

    def run(
        self,
        external_operation_key: str,
        confirmation: ConfirmationDecision,
        now: int,
        effect: str,
    ) -> bool:
        """Execute only on a valid, unexpired confirmation; idempotent by key.

        Returns False on a stale/superseded confirmation (a fresh one is
        required) — no effect is recorded.
        """
        return self._operation.execute(external_operation_key, confirmation, now, effect)
