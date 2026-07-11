"""In-harness simulated control / lease authorization stub (FR-007 / Clarifications Q6).

Models the ``lease_ack`` -> ``media_authorized`` ordering only. It has NO Hermes or
external control-plane dependency and is not reusable production broker code. Media
authorization is authoritative and may be granted only after sideband verification.
"""
from __future__ import annotations

from enum import Enum


class LeaseState(str, Enum):
    IDLE = "idle"
    READINESS_REQUESTED = "readiness_requested"
    LEASE_ACKED = "lease_acked"
    AUTHORIZED = "authorized"
    REVOKED = "revoked"


class ControlError(Exception):
    pass


class ControlLeaseStub:
    """Local authorization state machine (authoritative for media authorization)."""

    def __init__(self) -> None:
        self.state = LeaseState.IDLE

    def request_readiness(self) -> None:
        if self.state is not LeaseState.IDLE:
            raise ControlError(f"cannot request readiness from {self.state}")
        self.state = LeaseState.READINESS_REQUESTED

    def lease_ack(self) -> None:
        if self.state is not LeaseState.READINESS_REQUESTED:
            raise ControlError(f"cannot ack lease from {self.state}")
        self.state = LeaseState.LEASE_ACKED

    def grant_authorization(self, *, sideband_verified: bool) -> None:
        """Authorize media — permitted only after sideband verification (fail-closed)."""
        if not sideband_verified:
            raise ControlError("refusing media authorization: sideband not verified")
        if self.state is not LeaseState.LEASE_ACKED:
            raise ControlError(f"cannot authorize from {self.state}")
        self.state = LeaseState.AUTHORIZED

    def revoke(self) -> None:
        self.state = LeaseState.REVOKED

    @property
    def is_authorized(self) -> bool:
        return self.state is LeaseState.AUTHORIZED
