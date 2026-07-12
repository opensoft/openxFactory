"""Brokered call creation + idempotent call registry.

Offline: ``SimulatedBroker`` drives the retry / single-call semantics deterministically.
Live: ``HttpBroker`` (lazy ``httpx``) POSTs the SDP offer to the GA brokered
``POST /v1/realtime/calls`` surface and reads the answer SDP + ``Location`` call id; it is
exercised only when a lab key is present (T058 live run).

The provider request ID and call id are only ever exposed as SHA-256 hashes; the raw
answer SDP is held in memory to gate onto the peer connection and is NEVER logged,
returned in evidence, or persisted.
"""
from __future__ import annotations

import hashlib
import json
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


@dataclass
class LiveBrokerResult:
    """Live create result. ``held_answer_sdp`` and ``call_id`` stay in memory only;
    evidence sees only the hashes / opaque token."""
    call_id_hash: str
    provider_request_id_hash: str
    answer_token: str          # opaque handle (sha256 of the call id); never the SDP
    duplicate: bool
    held_answer_sdp: str       # raw answer SDP — held, gated onto the peer, never logged
    call_id: str               # raw provider call id — kept for WSS attach + hangup


class BrokerHttpError(Exception):
    """A provider create/hangup returned a non-success status or an unexpected shape.

    Carries only the status code and a redacted marker — never the response body, which
    may contain SDP or provider detail. Surfaces as INCONCLUSIVE (API-shape) per FR-004.
    """

    def __init__(self, status: int, where: str) -> None:
        super().__init__(f"provider {where} returned HTTP {status}")
        self.status = status
        self.where = where


class HttpBroker:  # pragma: no cover - live path, exercised only with a lab key
    """Live brokered-call client (lazy httpx) for the GA ``/v1/realtime/calls`` surface.

    A harness-side idempotency cache (mirroring ``SimulatedBroker``) guarantees the retry
    invariants WITHOUT a second provider call: an exact retry returns the same held call
    and creates no new provider call; a changed retry raises ``IdempotencyConflict`` and
    discloses no prior answer. The provider itself is never asked to dedupe.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com",
                 timeout_s: float = 15.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s
        self.provider_calls_created = 0
        # request_id -> (offer_fingerprint, LiveBrokerResult)
        self._by_request: Dict[str, Tuple[str, "LiveBrokerResult"]] = {}

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._api_key}"}

    async def create_call(self, request_id: str, offer_fingerprint: str, offer_sdp: str,
                          session_config: dict) -> "LiveBrokerResult":
        """POST the offer SDP + session config; return the held answer (never applied here)."""
        import httpx  # lazy

        rid_hash = hash_request_id(request_id)
        if request_id in self._by_request:
            offer0, prior = self._by_request[request_id]
            if offer0 == offer_fingerprint:
                # Exact retry: same held call, no new billable provider call.
                return LiveBrokerResult(prior.call_id_hash, rid_hash, prior.answer_token,
                                        duplicate=True, held_answer_sdp=prior.held_answer_sdp,
                                        call_id=prior.call_id)
            # Changed retry: refuse; no second call, no prior answer disclosed.
            raise IdempotencyConflict("idempotency_conflict")

        url = f"{self._base_url}/v1/realtime/calls"
        async with httpx.AsyncClient(timeout=self._timeout_s) as client:
            resp = await client.post(
                url, headers=self._headers(),
                files={"sdp": (None, offer_sdp), "session": (None, json.dumps(session_config))},
            )
        if resp.status_code not in (200, 201):
            # Do NOT include resp.text (may carry SDP/provider detail). API-shape → INCONCLUSIVE.
            raise BrokerHttpError(resp.status_code, "create")
        answer_sdp = resp.text
        location = resp.headers.get("Location", "")
        call_id = location.rsplit("/", 1)[-1] if location else ""
        if not call_id or not answer_sdp:
            raise BrokerHttpError(resp.status_code, "create")
        cid_hash = hashlib.sha256(call_id.encode()).hexdigest()
        answer_token = hashlib.sha256(f"answer:{cid_hash}".encode()).hexdigest()[:32]
        result = LiveBrokerResult(cid_hash, rid_hash, answer_token, duplicate=False,
                                  held_answer_sdp=answer_sdp, call_id=call_id)
        self._by_request[request_id] = (offer_fingerprint, result)
        self.provider_calls_created += 1
        return result

    async def hangup(self, call_id: str) -> bool:
        """Ask the provider to terminate the call (POST …/{call_id}/hangup). 200 ⇒ accepted."""
        import httpx  # lazy

        if not call_id:
            return False
        url = f"{self._base_url}/v1/realtime/calls/{call_id}/hangup"
        try:
            async with httpx.AsyncClient(timeout=self._timeout_s) as client:
                resp = await client.post(url, headers=self._headers())
            return resp.status_code == 200
        except Exception:
            return False
