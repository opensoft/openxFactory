"""Media-attempt state machine (design D4). Rejects illegal/terminal transitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .values import (
    ATTEMPT_TRANSITIONS,
    TERMINAL_STATUSES,
    AttemptStatus,
    ControlDescriptor,
    OutcomeCode,
)


class AttemptError(Exception):
    """Illegal predecessor or attempted mutation of a terminal attempt."""


@dataclass
class MediaAttempt:
    request_id: str
    offer_fingerprint: str
    instance_id: str
    epoch: int
    status: AttemptStatus = AttemptStatus.CREATED
    provider_call_ref: Optional[str] = None
    held_answer: Optional[str] = None
    control_descriptor: Optional[ControlDescriptor] = None
    readiness_deadline: int = 0
    lease: Optional[object] = None
    terminal_result: Optional[OutcomeCode] = None
    media_authorized_emitted: bool = False

    def to(self, new: AttemptStatus) -> None:
        if self.status in TERMINAL_STATUSES:
            raise AttemptError(f"attempt {self.status.value} is terminal; cannot mutate")
        allowed = ATTEMPT_TRANSITIONS.get(self.status, frozenset())
        if new not in allowed:
            raise AttemptError(f"illegal transition {self.status.value} -> {new.value}")
        self.status = new

    def terminate(self, status: AttemptStatus, outcome: OutcomeCode) -> bool:
        """Idempotently drive to a terminal status; erase secret material.

        Returns True if this call performed the termination, False if the
        attempt was already terminal (idempotent).
        """
        if status not in TERMINAL_STATUSES:
            raise AttemptError(f"{status.value} is not a terminal status")
        if self.status in TERMINAL_STATUSES:
            return False
        self.status = status
        self.terminal_result = outcome
        # Erase cached answer + scoped credential material (FR-016).
        self.held_answer = None
        self.control_descriptor = None
        return True

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES
