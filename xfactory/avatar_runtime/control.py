"""Leased control: epoch fencing, identity-checked lease_ack, expiry, reconnect.

`lease_ack` ≡ the spec's "control acknowledgement" (FR-019).
"""

from __future__ import annotations

from dataclasses import dataclass

from .ids import QueuedIdSource
from .values import LeaseAck


@dataclass
class ControlLease:
    lease_id: str
    session_id: str
    epoch: int
    instance_id: str
    attempt_id: str
    transport_identity: str
    heartbeat_deadline: int
    expiry_deadline: int
    reconnect_credential: str
    active: bool = True


class LeaseManager:
    def create(
        self,
        ids: QueuedIdSource,
        *,
        session_id: str,
        epoch: int,
        instance_id: str,
        attempt_id: str,
        transport_identity: str,
        now: int,
        heartbeat_ttl: int,
        expiry_ttl: int,
    ) -> ControlLease:
        return ControlLease(
            lease_id=ids.next("lease"),
            session_id=session_id,
            epoch=epoch,
            instance_id=instance_id,
            attempt_id=attempt_id,
            transport_identity=transport_identity,
            heartbeat_deadline=now + heartbeat_ttl,
            expiry_deadline=now + expiry_ttl,
            reconnect_credential=ids.next("cred"),
        )

    def verify_ack(self, lease: ControlLease, ack: LeaseAck) -> bool:
        """All five identity dimensions + transport identity must match (FR-019)."""
        return (
            lease.active
            and ack.lease_id == lease.lease_id
            and ack.session_id == lease.session_id
            and ack.epoch == lease.epoch
            and ack.instance_id == lease.instance_id
            and ack.attempt_id == lease.attempt_id
            and ack.transport_identity == lease.transport_identity
        )

    def is_expired(self, lease: ControlLease, now: int) -> bool:
        return now > lease.expiry_deadline

    def revoke(self, lease: ControlLease) -> None:
        lease.active = False

    def reconnect(
        self, lease: ControlLease, ids: QueuedIdSource, *, epoch: int, credential: str
    ) -> bool:
        """Accept only a current epoch + credential; rotate on success (FR-022)."""
        if epoch != lease.epoch or credential != lease.reconnect_credential:
            return False  # stale epoch / rotated credential -> reject, no state change
        lease.reconnect_credential = ids.next("cred")
        return True
