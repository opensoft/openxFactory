"""In-process runtime assembly + orchestration (FR-001/FR-003).

Wires the injected ports and protocol managers into one deterministic facade.
Holds only in-memory state; ``destroy()`` discards everything with no
migration, durable-state cleanup, or recovery of secret grant material
(SC-009). This is deliberately NOT an application factory: it opens no socket
and loads no credential.
"""

from __future__ import annotations

from typing import Optional

from . import broker
from .authority import PolicyResolver
from .commands import CommandProcessor
from .consent import REVOCATION_BOUND_TICKS, ConsentGate
from .control import LeaseManager
from .events import EventLog
from .grant_cache import GrantCache
from .media_authz import MediaAuthorizer
from .ports import (
    ClockPort,
    ConsentPort,
    IdPort,
    OperationPort,
    PolicyPort,
    ProviderPort,
    UsagePort,
)
from .session import SessionRegistry
from .telemetry import TelemetrySink
from .usage import UsageMeter
from .values import (
    AttemptStatus,
    Command,
    CommandResult,
    EventKind,
    EventRecord,
    KillSwitchState,
    LeaseAck,
    OutcomeCode,
    PreflightResult,
    ProducerAuthority,
    Request,
)


class AvatarRuntime:
    # Deterministic fixture-configured bounds (injected-clock ticks).
    GRANT_TTL = 50
    READINESS_TTL = 10
    HEARTBEAT_TTL = 20
    LEASE_EXPIRY_TTL = 100

    def __init__(
        self,
        *,
        clock: ClockPort,
        ids: IdPort,
        provider: ProviderPort,
        policy: PolicyPort,
        consent: ConsentPort,
        operation: OperationPort,
        usage: UsagePort,
        kill_switch: Optional[KillSwitchState] = None,
        telemetry: Optional[TelemetrySink] = None,
    ) -> None:
        self.clock = clock
        self.ids = ids
        self.provider = provider
        self.policy = policy
        self.consent = consent
        self.operation = operation
        self.usage = usage
        self.kill_switch = kill_switch or KillSwitchState()
        self.telemetry = telemetry or TelemetrySink()

        # Protocol managers.
        self.registry = SessionRegistry()
        self.grants = GrantCache()
        self.lease_manager = LeaseManager()
        self.authorizer = MediaAuthorizer()
        self.policy_resolver = PolicyResolver(policy)
        self.consent_gate = ConsentGate(consent)
        self.usage_meter = UsageMeter(usage)

        # In-memory registries (no persistence).
        self.sessions = self.registry  # backward-compat alias
        self.attempts_by_request: dict = {}
        self._event_logs: dict[str, EventLog] = {}
        self._command_procs: dict[str, CommandProcessor] = {}
        self._destroyed = False

    # ------------------------------------------------------------------ #
    # Per-session helpers
    # ------------------------------------------------------------------ #
    def event_log(self, session_id: str) -> EventLog:
        return self._event_logs.setdefault(session_id, EventLog())

    def _commands(self, session_id: str) -> CommandProcessor:
        return self._command_procs.setdefault(session_id, CommandProcessor())

    def _pending(self, session_id: str):
        session = self.registry.get(session_id)
        return session.pending_attempt if session else None

    # ------------------------------------------------------------------ #
    # Broker
    # ------------------------------------------------------------------ #
    def preflight(self, request: Request) -> PreflightResult:
        return broker.preflight(self, request)

    def terminal_replay(self, request_id: str) -> Optional[PreflightResult]:
        term = self.grants.terminal(request_id)
        if term is None:
            return None
        return PreflightResult.of_terminal(request_id, term)

    # ------------------------------------------------------------------ #
    # Media flow
    # ------------------------------------------------------------------ #
    def open_sideband(self, session_id: str) -> None:
        attempt = self._pending(session_id)
        self.provider.open_sideband(attempt.provider_call_ref)
        attempt.to(AttemptStatus.SIDEBAND_OPEN)

    def verify_sideband(self, session_id: str) -> None:
        attempt = self._pending(session_id)
        self.provider.verify_sideband(attempt.provider_call_ref)
        attempt.to(AttemptStatus.SIDEBAND_VERIFIED)

    def submit_lease_ack(self, session_id: str, ack: LeaseAck) -> Optional[EventRecord]:
        attempt = self._pending(session_id)
        return self.authorizer.authorize(
            attempt,
            self.provider,
            attempt.lease,
            ack,
            self.lease_manager,
            self.event_log(session_id),
            self.clock.monotonic(),
        )

    def check_readiness(self, session_id: str) -> Optional[PreflightResult]:
        attempt = self._pending(session_id)
        if self.authorizer.check_readiness(attempt, self.provider, self.clock.monotonic()):
            self.grants.invalidate(attempt.request_id, OutcomeCode.READINESS_TIMEOUT)
            return PreflightResult.of_terminal(
                attempt.request_id, OutcomeCode.READINESS_TIMEOUT
            )
        return None

    def mark_connected(self, session_id: str) -> None:
        attempt = self._pending(session_id)
        attempt.to(AttemptStatus.CONNECTED)
        # Secret cache destroyed on connect; credential-free terminal remains.
        self.grants.invalidate(attempt.request_id, OutcomeCode.CONNECTED)

    # ------------------------------------------------------------------ #
    # Control lease
    # ------------------------------------------------------------------ #
    def check_lease(self, session_id: str) -> Optional[PreflightResult]:
        attempt = self._pending(session_id)
        if attempt is None or attempt.is_terminal:
            return None  # already handled (idempotent)
        lease = attempt.lease
        if self.lease_manager.is_expired(lease, self.clock.monotonic()):
            self.lease_manager.revoke(lease)
            self.provider.hangup(attempt.provider_call_ref)  # idempotent
            attempt.terminate(AttemptStatus.EXPIRED, OutcomeCode.LEASE_EXPIRED)
            self.grants.invalidate(attempt.request_id, OutcomeCode.LEASE_EXPIRED)
            return PreflightResult.of_terminal(
                attempt.request_id, OutcomeCode.LEASE_EXPIRED
            )
        return None

    def reconnect(self, session_id: str, *, epoch: int, credential: str) -> bool:
        attempt = self._pending(session_id)
        return self.lease_manager.reconnect(
            attempt.lease, self.ids, epoch=epoch, credential=credential
        )

    # ------------------------------------------------------------------ #
    # Consent revocation
    # ------------------------------------------------------------------ #
    def revoke_consent(self, session_id: str) -> dict:
        start = self.clock.monotonic()
        attempt = self._pending(session_id)
        lease = attempt.lease
        self.lease_manager.revoke(lease)
        self.provider.hangup(attempt.provider_call_ref)  # idempotent, synchronous
        attempt.terminate(AttemptStatus.REVOKED, OutcomeCode.CONSENT_REVOKED)
        self.grants.invalidate(attempt.request_id, OutcomeCode.CONSENT_REVOKED)
        completed = self.clock.monotonic()
        return {
            "revoked": True,
            "completed_at": completed,
            "deadline": start + REVOCATION_BOUND_TICKS,
            "provider_live": self.provider.is_live(attempt.provider_call_ref),
        }

    # ------------------------------------------------------------------ #
    # Kill switch
    # ------------------------------------------------------------------ #
    def activate_kill_switch(self, state: KillSwitchState) -> list[str]:
        """Apply a kill switch. New matching requests are denied at preflight;
        active leases are revoked ONLY when ``revoke_active_on_activate`` is set.
        """
        self.kill_switch = state
        revoked: list[str] = []
        if not state.revoke_active_on_activate:
            return revoked
        for session in self.registry.all():
            attempt = session.pending_attempt
            if attempt and attempt.lease and attempt.lease.active:
                self.lease_manager.revoke(attempt.lease)
                self.provider.hangup(attempt.provider_call_ref)
                attempt.terminate(AttemptStatus.REVOKED, OutcomeCode.KILLED)
                self.grants.invalidate(attempt.request_id, OutcomeCode.KILLED)
                revoked.append(session.session_id)
        return revoked

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #
    def submit_command(self, command: Command) -> CommandResult:
        session = self.registry.get_or_create(command.session_id)
        attempt = session.pending_attempt
        lease = attempt.lease if attempt else None
        return self._commands(command.session_id).submit(
            command,
            session=session,
            lease=lease,
            now=self.clock.monotonic(),
            lease_manager=self.lease_manager,
        )

    # ------------------------------------------------------------------ #
    # Event log
    # ------------------------------------------------------------------ #
    def append_observation(
        self,
        session_id: str,
        producer: ProducerAuthority,
        payload: str,
        *,
        authoritative: bool = False,
    ) -> EventRecord:
        kind = (
            EventKind.AUTHORITATIVE_RESULT if authoritative else EventKind.OBSERVATION
        )
        return self.event_log(session_id).append(
            kind, producer, payload, self.clock.monotonic()
        )

    # ------------------------------------------------------------------ #
    def destroy(self) -> None:
        """Discard all in-memory state — no durable state exists (FR-003)."""
        self.registry.clear()
        self.grants.clear()
        self.attempts_by_request.clear()
        self._event_logs.clear()
        self._command_procs.clear()
        self._destroyed = True

    @property
    def destroyed(self) -> bool:
        return self._destroyed
