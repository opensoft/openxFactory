"""Session-layer spend containment for the internal-live ring (task 6.1.3).

THE RULED CEILINGS ARE NOT INVENTED HERE. Every number below is read off
`contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`
(`rollback_policy.classes[ROLLBACK-B].trigger_thresholds.elevated_quota_condition`),
ruled 2026-08-27 as `qualify-avatar-live-voice` §7.2:

    per_session_duration_seconds_max: 900
    per_session_billable_units_max: 300
    billable_unit: one_us_cent_of_provider_attributed_spend   -> $3.00
    uncountable_is: exhausted

`tests/avatar_runtime/test_ruled_values_pinned.py` reads that YAML and fails if
this module and the contract ever disagree, so the constants here are a pinned
mirror rather than a second source.

WHAT THIS MODULE DOES NOT DO. It invents NO terminal. A session that crosses a
ceiling is terminated through the outcomes the kernel already models —
``OutcomeCode.QUOTA_EXCEEDED`` and ``OutcomeCode.DURATION_EXCEEDED`` — driven
by the runtime's single media-plane termination act (lease revocation, an
idempotent provider hangup, the attempt's terminal transition, and the
credential-free grant-cache terminal), which is the same act the kill switch
and the consent-withdraw path already perform.

THE AUDITABLE REASON. The spec requires "an auditable termination whose reason
distinguishes a cost-triggered kill from an ordinary duration or quota
terminal". The closed ``OutcomeCode`` registry has no reason slot and MUST NOT
be widened, so the reason rides the two shapes the runtime already has for it:
``TelemetryRecord.reason`` (``reason`` is an allowlisted stable telemetry key)
and the ``SessionSpendRecord`` this module appends to the journal. Both carry a
:class:`KillReason` value, and ``KillReason`` separates the cost trips from the
ordinary ones by construction — see :data:`COST_TRIGGERED_REASONS`.

SYNCHRONOUS BY RULING. The per-session ceilings are enforced "SYNCHRONOUSLY IN
THE BROKER". Only the per-TENANT metering is asynchronous, and that lives in
``metering`` — a module this one does not import and the dispatch path never
reaches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .values import OutcomeCode


# --------------------------------------------------------------------------- #
# The ruled per-session ceilings (§7.2)
# --------------------------------------------------------------------------- #
#: One injected-clock tick stands for one second of session wall duration. The
#: runtime's clock is a manually advanced integer tick source (FR-008), so the
#: ruled 900-SECOND ceiling is expressed as 900 ticks and the mapping is stated
#: rather than left for a reader to guess.
TICKS_PER_SECOND = 1

#: 15 minutes. RULED §7.2 — hard and broker-enforced.
SESSION_DURATION_CEILING_SECONDS = 900
SESSION_DURATION_CEILING_TICKS = SESSION_DURATION_CEILING_SECONDS * TICKS_PER_SECOND

#: 300 billable units. RULED §7.2 — hard and broker-enforced.
SESSION_BILLABLE_UNIT_CEILING = 300

#: One billable unit is one US cent of PROVIDER-ATTRIBUTED spend, read off the
#: provider's own usage block. The unit is cents and not tokens by ruling:
#: audio-output tokens cost 160x cached audio-input tokens, so a token count is
#: a bad cost proxy across modalities.
BILLABLE_UNIT_USD_CENTS = 1

#: $3.00 — the same ceiling as 300 units, stated in the other unit so a reader
#: never has to do the multiplication to check it.
SESSION_SPEND_CEILING_USD_CENTS = SESSION_BILLABLE_UNIT_CEILING * BILLABLE_UNIT_USD_CENTS


# --------------------------------------------------------------------------- #
# Closed reason registry — the auditable half of a ceiling termination
# --------------------------------------------------------------------------- #
class KillReason(Enum):
    """CLOSED registry of auditable termination reasons.

    The three ceiling reasons and the two ordinary ones are deliberately
    distinct VALUES rather than a boolean beside one value: a reader of an
    audit record must be able to tell a runaway-cost kill from a session that
    simply ran its allotted length, and a boolean loses which ceiling fired.
    """

    #: Crossed the 300-unit / $3.00 per-session spend ceiling.
    COST_CEILING_EXCEEDED = "cost_ceiling_exceeded"
    #: Crossed the 900-second per-session duration ceiling.
    DURATION_CEILING_EXCEEDED = "duration_ceiling_exceeded"
    #: `uncountable_is: exhausted` — the broker could not determine its
    #: accumulated cost, so it refuses the session rather than proceeding
    #: blind. This is a spend-containment act, not an ordinary quota terminal.
    COST_UNCOUNTABLE = "cost_uncountable"
    #: An ordinary quota terminal (the policy bundle's concurrency cap). This
    #: is the terminal the spec's "distinguishable from an ordinary duration or
    #: quota terminal" contrasts a cost kill against.
    ORDINARY_QUOTA_EXCEEDED = "ordinary_quota_exceeded"
    #: An ordinary duration terminal (the policy bundle's duration cap).
    ORDINARY_DURATION_EXCEEDED = "ordinary_duration_exceeded"
    #: The ledger closed on a terminal that was not a ceiling trip at all —
    #: consent withdrawal, lease expiry, a kill-switch act, a drained leg, or a
    #: natural completion. The record's `outcome` field says which. Naming one
    #: of the ceiling reasons here would put a cost story on a session that
    #: never had one, and the metering job pages a human off exactly that
    #: distinction.
    NON_CEILING_TERMINAL = "non_ceiling_terminal"


#: The reasons §7.4 means by "any cost-triggered session kill" — the set the
#: metering job pages a human on. `COST_UNCOUNTABLE` is a member: a broker that
#: refuses because it cannot count is containing spend, not enforcing a quota.
COST_TRIGGERED_REASONS = frozenset(
    {KillReason.COST_CEILING_EXCEEDED, KillReason.COST_UNCOUNTABLE}
)

#: Which of the kernel's two already-modelled terminal outcomes each CEILING
#: reason terminates through. NO NEW TERMINAL IS INTRODUCED — this map is the
#: whole of the relationship between the new reasons and the closed outcome
#: registry. ``NON_CEILING_TERMINAL`` is deliberately absent: it is not a
#: ceiling trip and has no outcome of its own to map to.
REASON_OUTCOMES: dict[KillReason, OutcomeCode] = {
    KillReason.COST_CEILING_EXCEEDED: OutcomeCode.QUOTA_EXCEEDED,
    KillReason.COST_UNCOUNTABLE: OutcomeCode.QUOTA_EXCEEDED,
    KillReason.DURATION_CEILING_EXCEEDED: OutcomeCode.DURATION_EXCEEDED,
    KillReason.ORDINARY_QUOTA_EXCEEDED: OutcomeCode.QUOTA_EXCEEDED,
    KillReason.ORDINARY_DURATION_EXCEEDED: OutcomeCode.DURATION_EXCEEDED,
}


def is_cost_triggered(reason: KillReason) -> bool:
    """True for the reasons §7.4's alert path and the audit trail must separate."""
    return reason in COST_TRIGGERED_REASONS


@dataclass(frozen=True)
class SessionCeilings:
    """The three ruled per-session ceilings, as one injectable value."""

    duration_ticks: int = SESSION_DURATION_CEILING_TICKS
    billable_units: int = SESSION_BILLABLE_UNIT_CEILING
    unit_usd_cents: int = BILLABLE_UNIT_USD_CENTS

    @property
    def spend_usd_cents(self) -> int:
        return self.billable_units * self.unit_usd_cents


@dataclass(frozen=True)
class SpendVerdict:
    """A crossed ceiling, with the auditable reason and the existing outcome."""

    reason: KillReason
    outcome: OutcomeCode
    elapsed_ticks: int
    billable_units: int
    usd_cents: int

    @property
    def cost_triggered(self) -> bool:
        return is_cost_triggered(self.reason)

    def audit_line(self) -> str:
        """One low-cardinality, credential-free line for an alert body."""
        return (
            f"{self.reason.value} outcome={self.outcome.value} "
            f"elapsed_ticks={self.elapsed_ticks} units={self.billable_units} "
            f"usd_cents={self.usd_cents}"
        )


@dataclass(frozen=True)
class SessionSpendRecord:
    """One closed session's attributed spend — the METERING JOB'S ONLY INPUT.

    Frozen, credential-free and low-cardinality by construction: it carries no
    answer, no control descriptor, no SDP and no provider payload. The
    asynchronous per-tenant counters in ``metering`` are aggregated off a list
    of these and off nothing else, which is what keeps metering out of the
    dispatch path.
    """

    session_id: str
    tenant_ref: str
    attempt_ref: str
    billable_units: int
    usd_cents: int
    outcome: OutcomeCode
    reason: KillReason
    cost_triggered: bool
    countable: bool
    opened_at: int
    closed_at: int


@dataclass
class SessionSpendLedger:
    """Per-session accumulated provider-attributed spend, evaluated in-broker."""

    session_id: str
    tenant_ref: str
    attempt_ref: str
    opened_at: int
    ceilings: SessionCeilings = field(default_factory=SessionCeilings)
    billable_units: int = 0
    countable: bool = True
    closed: bool = False

    @property
    def usd_cents(self) -> int:
        return self.billable_units * self.ceilings.unit_usd_cents

    def attribute(self, units: int) -> None:
        """Accrue provider-attributed billable units (accumulated ACTUAL cost).

        A negative or non-integer attribution is not a cheaper session, it is
        an uncountable one: the ledger fails closed rather than subtracting.
        """
        if isinstance(units, bool) or not isinstance(units, int) or units < 0:
            self.countable = False
            return
        self.billable_units += units

    def mark_uncountable(self) -> None:
        """The provider usage block was absent or unreadable (`uncountable_is: exhausted`)."""
        self.countable = False

    def elapsed(self, now: int) -> int:
        return max(0, now - self.opened_at)

    def verdict(self, now: int) -> Optional[SpendVerdict]:
        """The crossed ceiling, or None while the session is inside all three.

        PRECEDENCE, stated rather than left to evaluation order: uncountable
        first (a broker that cannot count must not then reason about what it
        counted), then the cost ceiling, then the duration ceiling. Cost
        outranks duration when a session crosses both in the same tick because
        cost is the reason that carries an escalation (§7.4), and recording
        the escalating reason is the more useful of two true facts.
        """
        elapsed = self.elapsed(now)
        if not self.countable:
            return self._verdict(KillReason.COST_UNCOUNTABLE, elapsed)
        if self.billable_units >= self.ceilings.billable_units:
            return self._verdict(KillReason.COST_CEILING_EXCEEDED, elapsed)
        if elapsed >= self.ceilings.duration_ticks:
            return self._verdict(KillReason.DURATION_CEILING_EXCEEDED, elapsed)
        return None

    def _verdict(self, reason: KillReason, elapsed: int) -> SpendVerdict:
        return SpendVerdict(
            reason=reason,
            outcome=REASON_OUTCOMES[reason],
            elapsed_ticks=elapsed,
            billable_units=self.billable_units,
            usd_cents=self.usd_cents,
        )


class SpendJournal:
    """In-memory, append-only journal of open ledgers and closed session records.

    Holds no durable state: ``clear()`` discards everything, exactly like the
    grant cache and the session registry (FR-003, SC-009).
    """

    def __init__(self, ceilings: Optional[SessionCeilings] = None) -> None:
        self.ceilings = ceilings or SessionCeilings()
        self._open: dict[str, SessionSpendLedger] = {}
        self.records: list[SessionSpendRecord] = []

    # -- open side (synchronous, in the broker) ----------------------------- #
    def open_ledger(
        self, session_id: str, tenant_ref: str, attempt_ref: str, now: int
    ) -> SessionSpendLedger:
        ledger = SessionSpendLedger(
            session_id=session_id,
            tenant_ref=tenant_ref,
            attempt_ref=attempt_ref,
            opened_at=now,
            ceilings=self.ceilings,
        )
        self._open[session_id] = ledger
        return ledger

    def ledger(self, session_id: str) -> Optional[SessionSpendLedger]:
        return self._open.get(session_id)

    def attribute(self, session_id: str, units: int) -> Optional[SessionSpendLedger]:
        ledger = self._open.get(session_id)
        if ledger is None:
            return None
        ledger.attribute(units)
        return ledger

    def mark_uncountable(self, session_id: str) -> Optional[SessionSpendLedger]:
        ledger = self._open.get(session_id)
        if ledger is None:
            return None
        ledger.mark_uncountable()
        return ledger

    def verdict(self, session_id: str, now: int) -> Optional[SpendVerdict]:
        ledger = self._open.get(session_id)
        if ledger is None:
            return None
        return ledger.verdict(now)

    # -- close side (feeds the asynchronous meter) --------------------------- #
    def close(
        self,
        session_id: str,
        *,
        outcome: OutcomeCode,
        reason: KillReason,
        now: int,
    ) -> Optional[SessionSpendRecord]:
        """Close a session's ledger exactly once and append its spend record.

        Idempotent: closing an unknown or already-closed session is a no-op
        returning None, so every terminal path in the runtime may call this
        without first asking whether some other path got there first.
        """
        ledger = self._open.pop(session_id, None)
        if ledger is None or ledger.closed:
            return None
        ledger.closed = True
        record = SessionSpendRecord(
            session_id=ledger.session_id,
            tenant_ref=ledger.tenant_ref,
            attempt_ref=ledger.attempt_ref,
            billable_units=ledger.billable_units,
            usd_cents=ledger.usd_cents,
            outcome=outcome,
            reason=reason,
            cost_triggered=is_cost_triggered(reason),
            countable=ledger.countable,
            opened_at=ledger.opened_at,
            closed_at=now,
        )
        self.records.append(record)
        return record

    def cost_triggered_kills(self) -> list[SessionSpendRecord]:
        """The records §7.4 pages a human on."""
        return [r for r in self.records if r.cost_triggered]

    def clear(self) -> None:
        self._open.clear()
        self.records.clear()
