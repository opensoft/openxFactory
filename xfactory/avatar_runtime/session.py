"""Logical-session state (FR-011). One instance and one media leg per session."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .values import SessionState


@dataclass
class LogicalSession:
    session_id: str
    epoch: int = 0
    active_instance_id: Optional[str] = None
    policy_version: int = 1
    consent_version: int = 1
    state_revision: int = 0
    state: SessionState = SessionState.ACTIVE
    pending_attempt: Optional[object] = None  # MediaAttempt or None (≤1 leg)


class SessionRegistry:
    def __init__(self) -> None:
        self._sessions: dict[str, LogicalSession] = {}

    def get_or_create(self, session_id: str) -> LogicalSession:
        s = self._sessions.get(session_id)
        if s is None:
            s = LogicalSession(session_id)
            self._sessions[session_id] = s
        return s

    def get(self, session_id: str) -> Optional[LogicalSession]:
        return self._sessions.get(session_id)

    def all(self) -> list[LogicalSession]:
        return list(self._sessions.values())

    def clear(self) -> None:
        self._sessions.clear()
