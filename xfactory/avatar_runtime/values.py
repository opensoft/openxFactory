"""Immutable typed values and closed (fail-closed) registries.

All registries here are CLOSED: an unrecognized value is rejected, never
coerced (constitution VII, FR-010). Values are frozen dataclasses.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------- #
# Closed registries
# --------------------------------------------------------------------------- #
class SessionState(Enum):
    ACTIVE = "active"
    TERMINATED = "terminated"


class AttemptStatus(Enum):
    CREATED = "created"
    PROVIDER_CALL_CREATED = "provider_call_created"
    ANSWER_HELD = "answer_held"
    SIDEBAND_OPEN = "sideband_open"
    SIDEBAND_VERIFIED = "sideband_verified"
    AUTHORIZED = "authorized"
    CONNECTED = "connected"
    ABANDONED = "abandoned"
    EXPIRED = "expired"
    REVOKED = "revoked"
    TIMED_OUT = "timed_out"
    TERMINATED = "terminated"


#: Attempt statuses that are terminal (immutable once entered).
TERMINAL_STATUSES = frozenset(
    {
        AttemptStatus.ABANDONED,
        AttemptStatus.EXPIRED,
        AttemptStatus.REVOKED,
        AttemptStatus.TIMED_OUT,
        AttemptStatus.TERMINATED,
    }
)

#: Allowed forward transitions of the media-attempt state machine (design D4).
ATTEMPT_TRANSITIONS: dict[AttemptStatus, frozenset[AttemptStatus]] = {
    AttemptStatus.CREATED: frozenset({AttemptStatus.PROVIDER_CALL_CREATED}),
    AttemptStatus.PROVIDER_CALL_CREATED: frozenset({AttemptStatus.ANSWER_HELD}),
    AttemptStatus.ANSWER_HELD: frozenset({AttemptStatus.SIDEBAND_OPEN}),
    AttemptStatus.SIDEBAND_OPEN: frozenset({AttemptStatus.SIDEBAND_VERIFIED}),
    AttemptStatus.SIDEBAND_VERIFIED: frozenset({AttemptStatus.AUTHORIZED}),
    AttemptStatus.AUTHORIZED: frozenset({AttemptStatus.CONNECTED}),
    AttemptStatus.CONNECTED: frozenset(),  # terminal transitions handled separately
}


class PreflightKind(Enum):
    GRANT = "grant"
    DENIAL = "denial"
    TERMINAL = "terminal"


class OutcomeCode(Enum):
    # Denial / terminal reason codes ...
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    SECOND_INSTANCE_DENIED = "second_instance_denied"
    READINESS_TIMEOUT = "readiness_timeout"
    LEASE_EXPIRED = "lease_expired"
    CONSENT_REVOKED = "consent_revoked"
    KILLED = "killed"
    QUOTA_EXCEEDED = "quota_exceeded"
    DURATION_EXCEEDED = "duration_exceeded"
    PURPOSE_UNMAPPED = "purpose_unmapped"
    AUTHORITY_UNAVAILABLE = "authority_unavailable"
    CONFIRMATION_STALE = "confirmation_stale"
    # ... and terminal-status echoes (D1: unified for now)
    CONNECTED = "connected"
    ABANDONED = "abandoned"
    EXPIRED = "expired"
    REVOKED = "revoked"


class EventKind(Enum):
    OBSERVATION = "observation"
    AUTHORITATIVE_RESULT = "authoritative_result"


class ProducerAuthority(Enum):
    CLIENT = "client"
    PROVIDER = "provider"
    RUNTIME_AUTHORITY = "runtime_authority"


class ReasonCode(Enum):
    OK = "ok"
    DENIED = "denied"
    TERMINATED = "terminated"
    REVOKED = "revoked"
    TIMED_OUT = "timed_out"
    RETRY_COALESCED = "retry_coalesced"


class DispositionKind(Enum):
    MAPPED = "mapped"
    NON_APPLICABLE = "non_applicable"
    GATE = "gate"


class ClosedRegistryError(ValueError):
    """Raised when an unrecognized value is offered to a closed registry."""


# --------------------------------------------------------------------------- #
# Idempotency: volatile vs non-volatile offer/request fields (U1, FR-014)
# --------------------------------------------------------------------------- #
#: Volatile request fields are EXCLUDED from the offer fingerprint (may differ
#: on an exact retry). Everything else is non-volatile (a change conflicts).
VOLATILE_REQUEST_FIELDS = frozenset(
    {"client_ts", "transport_nonce", "retry_count"}
)


@dataclass(frozen=True)
class Offer:
    """A media offer. ``sdp_media`` stands in for the SDP media description."""

    sdp_media: str
    model_profile: str


@dataclass(frozen=True)
class Request:
    request_id: str
    session_id: str
    subject_id: str
    instance_id: str
    epoch: int
    purposes: frozenset[str]
    offer: Offer
    tenant_ref: str
    resume_ref: Optional[str] = None
    # Volatile fields (excluded from the fingerprint):
    client_ts: int = 0
    transport_nonce: str = ""
    retry_count: int = 0

    def fingerprint(self) -> str:
        """Deterministic fingerprint over the NON-VOLATILE fields only."""
        parts = [
            self.subject_id,
            self.instance_id,
            str(self.epoch),
            "|".join(sorted(self.purposes)),
            self.offer.sdp_media,
            self.offer.model_profile,
            self.tenant_ref,
            self.resume_ref or "",
        ]
        return "sha256:" + hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


@dataclass(frozen=True)
class ControlDescriptor:
    """Scoped control credential — only ever carried by a grant."""

    lease_id: str
    scope_digest: str


@dataclass(frozen=True)
class Grant:
    request_id: str
    offer_fingerprint: str
    answer: str
    control: ControlDescriptor
    expires_at: int  # injected-clock tick


@dataclass(frozen=True)
class Denial:
    request_id: str
    outcome: OutcomeCode


@dataclass(frozen=True)
class Terminal:
    request_id: str
    outcome: OutcomeCode


@dataclass(frozen=True)
class PreflightResult:
    """Tagged union: exactly one of grant / denial / terminal (FR-012)."""

    kind: PreflightKind
    grant: Optional[Grant] = None
    denial: Optional[Denial] = None
    terminal: Optional[Terminal] = None

    @staticmethod
    def of_grant(g: Grant) -> "PreflightResult":
        return PreflightResult(PreflightKind.GRANT, grant=g)

    @staticmethod
    def of_denial(request_id: str, outcome: OutcomeCode) -> "PreflightResult":
        return PreflightResult(PreflightKind.DENIAL, denial=Denial(request_id, outcome))

    @staticmethod
    def of_terminal(request_id: str, outcome: OutcomeCode) -> "PreflightResult":
        return PreflightResult(
            PreflightKind.TERMINAL, terminal=Terminal(request_id, outcome)
        )

    @property
    def outcome(self) -> Optional[OutcomeCode]:
        if self.denial:
            return self.denial.outcome
        if self.terminal:
            return self.terminal.outcome
        return None

    def carries_credential(self) -> bool:
        return self.grant is not None


@dataclass(frozen=True)
class LeaseAck:
    """Control-path acknowledgement (spec 'control acknowledgement' ≡ lease_ack)."""

    lease_id: str
    session_id: str
    epoch: int
    instance_id: str
    attempt_id: str
    transport_identity: str


@dataclass(frozen=True)
class EventRecord:
    sequence: int
    kind: EventKind
    producer: ProducerAuthority
    payload: str
    clock_ts: int


@dataclass(frozen=True)
class Command:
    command_id: str
    session_id: str
    epoch: int
    verb: str
    payload: str = ""
    expected_revision: Optional[int] = None


@dataclass(frozen=True)
class CommandResult:
    command_id: str
    accepted: bool
    reason: ReasonCode
    revision: int


@dataclass(frozen=True)
class Snapshot:
    last_event_sequence: int
    projection_through_b: tuple  # AVC-12 projection through barrier B


@dataclass(frozen=True)
class UsageRecord:
    tenant_ref: str
    attempt_ref: str
    outcome: OutcomeCode
    clock_ts: int


@dataclass(frozen=True)
class ConsentBinding:
    subject_ref: str
    version: int
    valid: bool


@dataclass(frozen=True)
class ConfirmationDecision:
    confirmation_version: int
    valid_until: int  # injected-clock tick
    superseded: bool = False


@dataclass(frozen=True)
class PolicyBundle:
    identity_ref: str
    required_purposes: frozenset[str]
    speech_gate: str
    retention_ticks: int
    concurrency_cap: int
    duration_cap_ticks: int
    confirmation_required: bool


@dataclass(frozen=True)
class KillSwitchState:
    all_session: bool = False
    disabled_profiles: frozenset[str] = field(default_factory=frozenset)
    revoke_active_on_activate: bool = False


# Re-export replace for convenience in modules building successor states.
__all__ = [name for name in globals() if not name.startswith("_")]
