"""In-process runtime assembly + orchestration (FR-001/FR-003).

Wires the injected ports and protocol managers into one deterministic facade.
Holds only in-memory state; ``destroy()`` discards everything with no
migration, durable-state cleanup, or recovery of secret grant material
(SC-009). This is deliberately NOT an application factory: it opens no socket
and loads no credential.
"""

from __future__ import annotations

from typing import Optional

from . import broker, detection, projection, rollback
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
from .spend import KillReason, SessionCeilings, SpendJournal, SpendVerdict
from .telemetry import INTERNAL_LIVE_SCOPE, TelemetryRecord, TelemetrySink
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
        ceilings: Optional[SessionCeilings] = None,
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
        # Per-session spend containment (§7.2), enforced SYNCHRONOUSLY in the
        # broker. The per-TENANT metering that reads this journal's closed
        # records is asynchronous and lives in `metering`, which neither this
        # module nor `broker` imports.
        self.spend = SpendJournal(ceilings)

        # In-memory registries (no persistence).
        self.sessions = self.registry  # backward-compat alias
        self.attempts_by_request: dict = {}
        # Which media legs belong to which logical session, in creation order.
        # The grant cache is keyed by request id across the WHOLE runtime, so
        # this is what lets a per-session record be scoped to its own legs
        # instead of carrying every session's terminals. It is media-plane
        # bookkeeping and deliberately NOT a field of `LogicalSession`, whose
        # fields are the authority-owned projection.
        self._session_legs: dict[str, list[str]] = {}
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

    def record_leg(self, session_id: str, request_id: str) -> None:
        """Register a fresh media leg against its logical session."""
        legs = self._session_legs.setdefault(session_id, [])
        if request_id not in legs:
            legs.append(request_id)

    def session_legs(self, session_id: str) -> tuple[str, ...]:
        """Every media leg this logical session has had, in creation order."""
        return tuple(self._session_legs.get(session_id, ()))

    # ------------------------------------------------------------------ #
    # THE media-plane termination act — one act, four callers
    # ------------------------------------------------------------------ #
    def _terminate_media_leg(
        self,
        session_id: str,
        attempt,
        *,
        status: AttemptStatus,
        outcome: OutcomeCode,
        reason: KillReason,
    ) -> bool:
        """Revoke the lease, hang up, drive the leg terminal, drop the secret.

        This is the landed consent-withdraw-mid-speech path, factored out so
        the kill switch, the lease-expiry terminal, the §7.2 ceiling hard-kill
        and ROLLBACK-A all perform the SAME act rather than four lookalikes.
        No new terminal is introduced by any of them: `status` and `outcome`
        are both drawn from the closed registries in ``values``.

        It touches media state only. It appends nothing to the event log and
        mutates no field of the logical session, which is why the
        authority-owned workflow projection is byte-identical across it
        (`abort_scope.ends: media_plane_only`).

        Returns True when this call performed the termination, False when the
        leg was already terminal (idempotent).
        """
        if attempt is None:
            return False
        lease = getattr(attempt, "lease", None)
        if lease is not None:
            self.lease_manager.revoke(lease)
        if attempt.provider_call_ref:
            self.provider.hangup(attempt.provider_call_ref)  # idempotent
        terminated = attempt.terminate(status, outcome)
        self.grants.invalidate(attempt.request_id, outcome)
        self.spend.close(
            session_id, outcome=outcome, reason=reason, now=self.clock.monotonic()
        )
        return terminated

    def _publish_termination_audit(
        self, before: AttemptStatus, after: AttemptStatus,
        outcome: OutcomeCode, reason: KillReason,
    ) -> None:
        """The auditable half of a termination, on the existing telemetry shape.

        ``TelemetryRecord.reason`` is the runtime's audit-reason slot — the
        closed ``OutcomeCode`` registry has none, and widening it to carry a
        reason would mean widening a closed registry to say something the
        registry is not for. Every field used here is on the telemetry
        allowlist, so the record passes redaction and is published rather than
        dropped.
        """
        self.telemetry.publish(
            TelemetryRecord(
                test_id=INTERNAL_LIVE_SCOPE,
                transition=f"{before.value}->{after.value}",
                clock_ts=self.clock.monotonic(),
                reason=reason.value,
                usage_outcome=outcome.value,
            )
        )

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
            # The authorizer owns this leg's terminal transition; the ledger is
            # closed here so no session leaves the journal open behind it.
            self.spend.close(
                session_id,
                outcome=OutcomeCode.READINESS_TIMEOUT,
                reason=KillReason.NON_CEILING_TERMINAL,
                now=self.clock.monotonic(),
            )
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
            self._terminate_media_leg(
                session_id,
                attempt,
                status=AttemptStatus.EXPIRED,
                outcome=OutcomeCode.LEASE_EXPIRED,
                reason=KillReason.NON_CEILING_TERMINAL,
            )
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
        self._terminate_media_leg(
            session_id,
            attempt,
            status=AttemptStatus.REVOKED,
            outcome=OutcomeCode.CONSENT_REVOKED,
            reason=KillReason.NON_CEILING_TERMINAL,
        )
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
                self._terminate_media_leg(
                    session.session_id,
                    attempt,
                    status=AttemptStatus.REVOKED,
                    outcome=OutcomeCode.KILLED,
                    reason=KillReason.NON_CEILING_TERMINAL,
                )
                revoked.append(session.session_id)
        return revoked

    # ------------------------------------------------------------------ #
    # Session-layer spend containment (task 6.1.3)
    # ------------------------------------------------------------------ #
    def attribute_spend(self, session_id: str, units: int) -> None:
        """Accrue provider-attributed billable units onto the session's ledger.

        One unit is one US cent of PROVIDER-ATTRIBUTED spend read off the
        provider's own usage block, so this is accumulated ACTUAL cost rather
        than an estimate (§7.2).
        """
        self.spend.attribute(session_id, units)

    def mark_spend_uncountable(self, session_id: str) -> None:
        """`uncountable_is: exhausted` — the broker could not determine its cost."""
        self.spend.mark_uncountable(session_id)

    def enforce_session_ceilings(self, session_id: str) -> Optional[PreflightResult]:
        """The §7.2 hard-kill. Synchronous, in the broker, no new terminal.

        Returns the credential-free terminal when a ceiling was crossed, or
        None while the session is inside all three. A crossed ceiling
        terminates through the EXISTING duration-or-quota terminal outcome,
        with the SAME lease-revoking act the kill switch performs, and leaves
        an auditable reason that separates a cost-triggered kill from an
        ordinary duration or quota terminal — see :meth:`_publish_termination_audit`
        and the ``SessionSpendRecord`` the journal appends.
        """
        attempt = self._pending(session_id)
        if attempt is None or attempt.is_terminal:
            return None  # already handled (idempotent)
        verdict = self.spend.verdict(session_id, self.clock.monotonic())
        if verdict is None:
            return None
        before = attempt.status
        self._terminate_media_leg(
            session_id,
            attempt,
            status=AttemptStatus.REVOKED,
            outcome=verdict.outcome,
            reason=verdict.reason,
        )
        self._publish_termination_audit(
            before, attempt.status, verdict.outcome, verdict.reason
        )
        # Attributed, credential-free usage record on the existing meter.
        self.usage_meter.record(
            self.spend_tenant(session_id) or "",
            attempt.request_id,
            verdict.outcome,
            self.clock.wall(),
        )
        return PreflightResult.of_terminal(attempt.request_id, verdict.outcome)

    def spend_tenant(self, session_id: str) -> Optional[str]:
        """The tenant a session's spend is attributed to, open or closed."""
        ledger = self.spend.ledger(session_id)
        if ledger is not None:
            return ledger.tenant_ref
        for record in self.spend.records:
            if record.session_id == session_id:
                return record.tenant_ref
        return None

    def session_spend_verdict(self, session_id: str) -> Optional[SpendVerdict]:
        """Peek at the ceiling verdict without acting on it."""
        return self.spend.verdict(session_id, self.clock.monotonic())

    # ------------------------------------------------------------------ #
    # Rollback acts and the auto-detection wiring (tasks 6.3.3-6.3.5)
    # ------------------------------------------------------------------ #
    def apply_rollback(
        self, decision: rollback.RollbackDecision
    ) -> rollback.RollbackOutcome:
        """Execute a recorded rollback act through the EXISTING kill switch.

        ROLLBACK-A's ``revoke_active_leases: true`` becomes the switch's
        ``revoke_active_on_activate`` path, which is the landed
        consent-withdraw-mid-speech termination. ROLLBACK-B's ``false`` leaves
        in-flight legs alone to drain. Nothing new is invented at either end.
        """
        revoked = self.activate_kill_switch(decision.kill_switch_state())
        return rollback.RollbackOutcome(
            decision=decision,
            revoked_sessions=tuple(revoked),
            blocked_profile=decision.profile,
            posture=rollback.rollback_posture(decision.profile),
        )

    def rollback_posture(
        self, profile: str = rollback.CANDIDATE_PROFILE
    ) -> rollback.RollbackPosture:
        """What the session-creation path answers with once voice is withdrawn."""
        return rollback.rollback_posture(profile)

    def latency_detection(
        self,
        samples,
        *,
        profile: str = rollback.CANDIDATE_PROFILE,
        minimum: int = detection.DECLARED_SAMPLE_MINIMUM,
    ) -> tuple[detection.LatencyEvaluation, Optional[rollback.RollbackOutcome]]:
        """The latency trip: evaluate AVC-10 samples, fire ROLLBACK-B on a trip.

        An under-sampled, non-gated, incomplete or malformed cell yields a
        non-tripping verdict, so it cannot reach the act at all.
        """
        evaluation = detection.evaluate_latency(samples, minimum=minimum)
        if not evaluation.tripped:
            return evaluation, None
        decision = rollback.decide(
            rollback.RollbackClass.B,
            trigger="material_regression_on_a_gated_percentile",
            profile=profile,
        )
        return evaluation, self.apply_rollback(decision)

    def safety_detection(
        self, signal, *, profile: str = rollback.CANDIDATE_PROFILE
    ) -> tuple[detection.SafetyDecision, Optional[rollback.RollbackOutcome]]:
        """The safety-eval trip: fire ROLLBACK-A, WITH active-lease revocation.

        Absent, malformed, foreign or unknown-trigger input never reaches the
        act — :func:`detection.evaluate_safety_signal` returns a non-tripping
        verdict for each of those, and this method acts only on ``trips``.
        """
        decision = detection.evaluate_safety_signal(signal)
        if not decision.trips:
            return decision, None
        act = rollback.decide(
            rollback.RollbackClass.A, trigger=decision.trigger, profile=profile
        )
        return decision, self.apply_rollback(act)

    def close_drain_window(self, session_id: str) -> Optional[str]:
        """Close a ROLLBACK-B drain window on a leg that is still in flight.

        A leg still draining when the window closes was GIVEN UP, not
        completed and not revoked, so it terminates `abandoned` — the token
        §7.8 binds to ``drained_leg_after_block_new``. A leg that already
        reached its own terminal inside the drain is left exactly as it is.
        """
        attempt = self._pending(session_id)
        if attempt is None:
            return None
        if attempt.is_terminal:
            return rollback.session_outcome_token(attempt.status, attempt.terminal_result)
        self._terminate_media_leg(
            session_id,
            attempt,
            status=AttemptStatus.ABANDONED,
            outcome=OutcomeCode.ABANDONED,
            reason=KillReason.NON_CEILING_TERMINAL,
        )
        return rollback.session_outcome_token(attempt.status, attempt.terminal_result)

    def complete_leg(self, session_id: str) -> Optional[str]:
        """Drive a leg to its OWN natural terminal — the `completed` token.

        §7.8's `also_permitted`: a leg that reached its natural end inside a
        drain window is a completed session that happened to be in flight when
        new work was blocked, and recording it as `abandoned` would be false.
        """
        attempt = self._pending(session_id)
        if attempt is None or attempt.is_terminal:
            return None
        self._terminate_media_leg(
            session_id,
            attempt,
            status=AttemptStatus.TERMINATED,
            outcome=OutcomeCode.CONNECTED,
            reason=KillReason.NON_CEILING_TERMINAL,
        )
        return rollback.session_outcome_token(attempt.status, attempt.terminal_result)

    def session_outcome(self, session_id: str) -> Optional[str]:
        """The released `session-outcomes` token this session's leg emitted."""
        attempt = self._pending(session_id)
        if attempt is None:
            return None
        return rollback.session_outcome_token(attempt.status, attempt.terminal_result)

    # ------------------------------------------------------------------ #
    # The authority-owned plane (task 6.3.5)
    # ------------------------------------------------------------------ #
    def workflow_projection(
        self, session_id: str
    ) -> Optional[projection.WorkflowProjection]:
        """The authority-owned projection — orthogonal to the media leg."""
        session = self.registry.get(session_id)
        if session is None:
            return None
        return projection.project(session, self._event_logs.get(session_id))

    def policy_required_records(
        self, session_id: str
    ) -> Optional[projection.PolicyRequiredRecords]:
        """The structured records policy requires be retained on every terminal."""
        session = self.registry.get(session_id)
        if session is None:
            return None
        # SCOPED to this session's own legs. The grant cache is keyed by
        # request id across the whole runtime, so an unscoped read would give
        # this record every other session's terminals too — a record naming one
        # session while carrying another's evidence, and a digest that moved
        # whenever an unrelated leg terminated.
        return projection.policy_required_records(
            session,
            self._event_logs.get(session_id),
            self.grants.terminal_items(self.session_legs(session_id)),
            tuple(r for r in self.spend.records if r.session_id == session_id),
        )

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
        self._session_legs.clear()
        self._event_logs.clear()
        self._command_procs.clear()
        self.spend.clear()
        self._destroyed = True

    @property
    def destroyed(self) -> bool:
        return self._destroyed
