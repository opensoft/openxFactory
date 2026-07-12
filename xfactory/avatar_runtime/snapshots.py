"""Atomic snapshot barrier + bounded post-barrier recovery (FR-027).

Recovery fixes a barrier B, projects through B, buffers post-B events, sends the
snapshot with ``last_event_sequence = B``, then drains the buffer once in order.
Buffer overflow aborts and restarts from a fresh snapshot; there is no
historical-replay endpoint.
"""

from __future__ import annotations

from typing import Optional

from .events import EventLog
from .values import EventRecord, Snapshot


class RecoveryOverflow(Exception):
    """Post-barrier buffer exceeded its bound — recovery must restart."""


class SnapshotRecovery:
    def __init__(self, event_log: EventLog, buffer_bound: int = 8) -> None:
        self._log = event_log
        self._bound = buffer_bound
        self._barrier: Optional[int] = None
        self._buffer: list[EventRecord] = []
        self.restarts = 0

    def begin(self) -> int:
        """Fix barrier B at the current last sequence and start buffering."""
        self._barrier = self._log.last_sequence
        self._buffer = []
        return self._barrier

    def observe(self, record: EventRecord) -> None:
        """Buffer an event that arrived after the barrier during projection."""
        if self._barrier is None:
            return
        if record.sequence <= self._barrier:
            return
        self._buffer.append(record)
        if len(self._buffer) > self._bound:
            raise RecoveryOverflow(f"post-barrier buffer exceeded {self._bound}")

    def snapshot(self) -> Snapshot:
        assert self._barrier is not None, "call begin() first"
        through_b = tuple(
            r.payload for r in self._log.records() if r.sequence <= self._barrier
        )
        return Snapshot(last_event_sequence=self._barrier, projection_through_b=through_b)

    def drain(self) -> list[EventRecord]:
        """Deliver buffered post-barrier events exactly once, in order."""
        drained = sorted(self._buffer, key=lambda r: r.sequence)
        self._buffer = []
        return drained

    def restart(self) -> int:
        """Abort and restart from a fresh snapshot (no partial replay)."""
        self.restarts += 1
        return self.begin()
