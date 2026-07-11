"""Two-channel media-authorization barrier (FR-018/020).

`media_authorized` is emitted exactly once, only when sideband verification AND
an identity-matched `lease_ack` agree for the same session/epoch/instance/
attempt/media-leg. Readiness timeout withholds authorization and terminates the
leg through the same idempotent provider port.
"""

from __future__ import annotations

from typing import Optional

from .attempt import MediaAttempt
from .control import ControlLease, LeaseManager
from .events import EventLog
from .ports import ProviderPort
from .values import (
    AttemptStatus,
    EventKind,
    EventRecord,
    LeaseAck,
    OutcomeCode,
    ProducerAuthority,
)


class MediaAuthorizer:
    def authorize(
        self,
        attempt: MediaAttempt,
        provider: ProviderPort,
        lease: ControlLease,
        ack: LeaseAck,
        lease_manager: LeaseManager,
        event_log: EventLog,
        now: int,
    ) -> Optional[EventRecord]:
        if attempt.is_terminal:
            return None
        # Channel 1: sideband verified?
        if not provider.sideband_verified(attempt.provider_call_ref):
            return None  # withhold
        # Channel 2: identity-matched lease_ack? (rejects hostile identity)
        if not lease_manager.verify_ack(lease, ack):
            return None
        if attempt.media_authorized_emitted:
            return None  # exactly once
        attempt.to(AttemptStatus.AUTHORIZED)
        ev = event_log.append(
            EventKind.AUTHORITATIVE_RESULT,
            ProducerAuthority.RUNTIME_AUTHORITY,
            "media_authorized",
            now,
        )
        attempt.media_authorized_emitted = True
        return ev

    def check_readiness(
        self, attempt: MediaAttempt, provider: ProviderPort, now: int
    ) -> bool:
        """If sideband missed the readiness deadline, withhold + terminate the leg."""
        if attempt.is_terminal:
            return False
        if provider.sideband_verified(attempt.provider_call_ref):
            return False
        if now > attempt.readiness_deadline:
            provider.hangup(attempt.provider_call_ref)  # idempotent
            attempt.terminate(AttemptStatus.TIMED_OUT, OutcomeCode.READINESS_TIMEOUT)
            return True
        return False
