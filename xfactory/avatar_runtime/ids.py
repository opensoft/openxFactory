"""Deterministic id source (FR-007) — no randomness, no UUID.

Ids are a stable, monotonically increasing per-kind sequence so tests are
reproducible. An optional pre-seeded queue lets a test force exact ids.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Optional


class QueuedIdSource:
    def __init__(self, queued: Optional[dict[str, list[str]]] = None) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._queues: dict[str, Deque[str]] = {
            kind: deque(vals) for kind, vals in (queued or {}).items()
        }

    def next(self, kind: str) -> str:
        q = self._queues.get(kind)
        if q:
            return q.popleft()
        self._counters[kind] += 1
        return f"{kind}-{self._counters[kind]:04d}"
