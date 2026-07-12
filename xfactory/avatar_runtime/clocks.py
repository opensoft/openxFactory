"""Deterministic, manually advanced clock (FR-008).

The core evaluates every deadline against ``monotonic()``; identical
``advance()`` sequences yield identical results. ``wall()`` is for record
timing only and never drives a control decision.
"""

from __future__ import annotations


class ManualClock:
    def __init__(self, start: int = 0, wall_start: int = 1_000_000) -> None:
        self._t = int(start)
        self._wall = int(wall_start)

    def monotonic(self) -> int:
        return self._t

    def wall(self) -> int:
        return self._wall

    def advance(self, ticks: int) -> int:
        if ticks < 0:
            raise ValueError("clock only advances forward")
        self._t += int(ticks)
        self._wall += int(ticks)
        return self._t
