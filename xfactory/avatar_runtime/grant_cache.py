"""Process-memory-only, TTL-bounded grant retry cache (FR-013/016, SC-009).

Holds unconsumed grants for exact retries and a *credential-free* terminal
record for replay. Destroying the runtime discards it with no persistence, and
terminal replay never needs secret grant material.
"""

from __future__ import annotations

from typing import Optional

from .values import Grant, OutcomeCode


class GrantCache:
    def __init__(self) -> None:
        self._grants: dict[str, Grant] = {}
        self._fingerprints: dict[str, str] = {}
        self._terminals: dict[str, OutcomeCode] = {}

    def seen_fingerprint(self, request_id: str) -> Optional[str]:
        return self._fingerprints.get(request_id)

    def put(self, request_id: str, grant: Grant, fingerprint: str) -> None:
        self._grants[request_id] = grant
        self._fingerprints[request_id] = fingerprint

    def active_grant(self, request_id: str, now: int) -> Optional[Grant]:
        g = self._grants.get(request_id)
        if g is None:
            return None
        if now > g.expires_at:
            # Expired: destroy secret material, leave a credential-free terminal.
            self.invalidate(request_id, OutcomeCode.EXPIRED)
            return None
        return g

    def terminal(self, request_id: str) -> Optional[OutcomeCode]:
        return self._terminals.get(request_id)

    def invalidate(self, request_id: str, outcome: OutcomeCode) -> None:
        """Remove cached grant (answer + credential); keep credential-free terminal."""
        self._grants.pop(request_id, None)
        self._terminals[request_id] = outcome

    def has_secret(self, request_id: str) -> bool:
        return request_id in self._grants

    def clear(self) -> None:
        self._grants.clear()
        self._fingerprints.clear()
        self._terminals.clear()
