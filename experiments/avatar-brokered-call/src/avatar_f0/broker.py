"""Brokered call creation + idempotent call registry.

Offline: ``SimulatedBroker`` drives the retry / single-call semantics deterministically.
Live: ``HttpBroker`` (lazy ``httpx``) POSTs to the brokered ``/v1/realtime/calls`` surface;
it is exercised only when a lab key is present (deferred live run, task T058).

The provider request ID is only ever exposed as a SHA-256 hash (never raw).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


class IdempotencyConflict(Exception):
    """Reused request ID with a changed offer fingerprint (FR-010 / F0-F)."""


class BrokerCreateFailed(Exception):
    pass


def hash_request_id(request_id: str) -> str:
    return hashlib.sha256(request_id.encode("utf-8")).hexdigest()


@dataclass
class BrokerResult:
    call_id_hash: str
    provider_request_id_hash: str
    answer_token: str          # opaque held-answer handle (never SDP)
    duplicate: bool            # True when an exact retry returned the same pending call


@dataclass
class SimulatedBroker:
    """Deterministic offline broker double.

    Enforces: an exact retry (same request_id + offer_fingerprint) returns the SAME
    pending call with NO new provider call; a changed retry (same request_id, different
    offer_fingerprint) raises ``IdempotencyConflict`` with NO second call and NO prior
    answer disclosed.
    """

    fail_create: bool = False
    create_ms: float = 40.0
    provider_calls_created: int = 0
    _by_request: Dict[str, Tuple[str, str, str]] = field(default_factory=dict)
    # request_id -> (offer_fingerprint, call_id_hash, answer_token)

    def create_call(self, request_id: str, offer_fingerprint: str) -> BrokerResult:
        if self.fail_create:
            raise BrokerCreateFailed("simulated provider create failure")
        rid_hash = hash_request_id(request_id)
        if request_id in self._by_request:
            offer0, cid_hash, token = self._by_request[request_id]
            if offer0 == offer_fingerprint:
                # Exact retry: same pending call, no new billable call.
                return BrokerResult(cid_hash, rid_hash, token, duplicate=True)
            # Changed retry: refuse; do not create a second call, do not disclose answer.
            raise IdempotencyConflict("idempotency_conflict")
        cid_hash = hashlib.sha256(f"{request_id}:{offer_fingerprint}".encode()).hexdigest()
        token = hashlib.sha256(f"answer:{cid_hash}".encode()).hexdigest()[:32]
        self._by_request[request_id] = (offer_fingerprint, cid_hash, token)
        self.provider_calls_created += 1
        return BrokerResult(cid_hash, rid_hash, token, duplicate=False)


@dataclass
class SimulatedTermination:
    """Configurable revocation/termination behavior for the offline double."""

    observable: bool = True
    terminal_ms: float = 900.0  # observed terminal offset after hangup

    def terminate(self, call_id_hash: str) -> bool:
        return self.observable


class HttpBroker:  # pragma: no cover - live path, exercised only with a lab key
    """Live brokered-call client (lazy httpx). Deferred to the live run (T058)."""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com") -> None:
        self._api_key = api_key
        self._base_url = base_url

    def create_call(self, request_id: str, offer_sdp: str):
        import httpx  # lazy

        raise NotImplementedError(
            "live brokered call creation is enabled during the lab run (T058); "
            "offline completion uses the simulated broker"
        )
