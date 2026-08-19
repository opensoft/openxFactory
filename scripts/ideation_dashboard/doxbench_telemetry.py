"""CONTENT-FREE usage telemetry for doxBench turns and sessions
(add-doxbench-editing-phase-b task 10.8; `memory-gateway`'s
`Usage Metering Is Gateway-Owned`, which this surface declares PARTIAL).

The metering requirement asks a gateway to emit a usage event for every
governed memory operation "without storing memory content in billing or usage
records", recording operation, provider role, provider id, client, domain,
workflow, bill-to target, usage units, latency, and a content-free
customer-subject reference.

A self-hosted authoring console can honour the SHAPE and the content-free rule
exactly, and cannot honour four of the fields at all: it has no client, no
domain, no bill-to target, and no customer subject. This module therefore does
two things and refuses a third:

  1. it emits the event with the dimensions this surface really measures —
     exact UTF-8 byte counts and item counts, the same arithmetic every other
     doxBench bound uses, never an estimate dressed as a measurement;
  2. it DECLARES each absent field as an absence WITH ITS REASON
     (``DeclaredAbsence``), so a reader sees "no bill-to target exists on a
     self-hosted console" rather than an empty string, a zero, or a plausible
     placeholder; and
  3. it never carries text. Every field is a count, a closed-vocabulary label,
     a scope key, or a declared absence — a companion test asserts that no
     byte of any metered packet's content appears anywhere in an emitted
     record.

TOKENS, honestly. The requirement's "usage units" are token counts for a
provider that reports them. This surface measures BYTES exactly and has no
tokenizer of its own, so a token count is carried only when a provider
REPORTS one and is a declared absence otherwise. Multiplying bytes by a guessed
ratio would be a fabricated measurement in a billing record, which is the one
thing a metering surface may never do.

Stdlib only, pure, in-process, and bounded: the meter holds counts for at most
``MAX_METERED_SCOPES`` conversation scopes and evicts the oldest, so a long
serve cannot grow one.
"""

from __future__ import annotations

import dataclasses
import threading
from collections.abc import Mapping

from ideation_dashboard.doxbench_scope import ScopeKey

# ---------------------------------------------------------------------------
# the declared-absence shape
# ---------------------------------------------------------------------------


class TelemetryRefused(ValueError):
    """Raised when a record would carry content, an unknown operation, or a
    placeholder in a field this console cannot fill."""


@dataclasses.dataclass(frozen=True, slots=True)
class DeclaredAbsence:
    """A field this surface cannot fill, stated as an absence with its reason.

    Deliberately NOT ``None``: a null in a usage record reads as "not supplied
    yet" and invites a later caller to fill it in with something plausible.
    This value says the field has no value HERE and why, and it renders that
    way in ``as_dict``."""

    field: str
    reason: str

    def __post_init__(self) -> None:
        for name in ("field", "reason"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise TelemetryRefused(f"a declared absence names its {name}")

    def as_dict(self) -> dict[str, object]:
        return {"value": None, "declared_absent": True, "reason": self.reason}


_SELF_HOSTED = (
    "a self-hosted authoring console has no {what}: this is a human editing "
    "their own repository, not a tenant workload, so the field is declared "
    "absent rather than filled with a placeholder")

ABSENT_CLIENT = DeclaredAbsence("client", _SELF_HOSTED.format(what="client"))
ABSENT_DOMAIN = DeclaredAbsence("domain", _SELF_HOSTED.format(what="domain"))
ABSENT_BILL_TO = DeclaredAbsence(
    "bill_to", _SELF_HOSTED.format(what="bill-to target"))
ABSENT_SUBJECT = DeclaredAbsence(
    "customer_subject_ref",
    "no customer subject exists anywhere on this surface; there is no "
    "reference to make content-free because there is no subject")
ABSENT_PROVIDER_TOKENS = DeclaredAbsence(
    "provider_tokens",
    "no provider reported a token count for this operation, and this surface "
    "measures exact UTF-8 bytes rather than estimating tokens from them — a "
    "guessed unit in a usage record is a fabricated measurement")

# The metering fields a self-hosted console cannot fill, declared once so the
# emitting sites cannot each invent their own spelling of the same absence.
DECLARED_ABSENCES: tuple[DeclaredAbsence, ...] = (
    ABSENT_CLIENT, ABSENT_DOMAIN, ABSENT_BILL_TO, ABSENT_SUBJECT,
)

# ---------------------------------------------------------------------------
# the events
# ---------------------------------------------------------------------------

# The closed operation vocabulary. Two operations exist because the metering
# requirement meters PACKET CREATION and this surface additionally wants the
# dispatch it feeds; a third spelling would be a third thing to keep honest.
OPERATION_CONTEXT_PACKET = "context_packet_created"
OPERATION_TURN_DISPATCHED = "turn_dispatched"
OPERATIONS: tuple[str, ...] = (OPERATION_CONTEXT_PACKET,
                               OPERATION_TURN_DISPATCHED)

# The provider role this surface's retrieval fills, in the gateway's own
# vocabulary. `local` because that is what it is: an in-process index.
PROVIDER_ROLE_RETRIEVAL = "retrieval"


@dataclasses.dataclass(frozen=True, slots=True)
class TurnUsage:
    """One content-free usage event.

    Every field is a count, a closed-vocabulary label, the conversation's own
    scope key, or a declared absence. There is no field a caller could put text
    in, which is how the content-free rule is kept by construction rather than
    by review."""

    operation: str
    scope: ScopeKey
    provider_role: str
    provider_id: str
    packet_posture: str
    source_count: int
    exempt_source_count: int
    packet_bytes: int
    prompt_bytes: int
    provider_tokens: int | DeclaredAbsence = ABSENT_PROVIDER_TOKENS
    client: DeclaredAbsence = ABSENT_CLIENT
    domain: DeclaredAbsence = ABSENT_DOMAIN
    bill_to: DeclaredAbsence = ABSENT_BILL_TO
    customer_subject_ref: DeclaredAbsence = ABSENT_SUBJECT

    def __post_init__(self) -> None:
        if self.operation not in OPERATIONS:
            raise TelemetryRefused(
                f"{self.operation!r} is not one of {OPERATIONS}")
        if not isinstance(self.scope, ScopeKey):
            raise TelemetryRefused("a usage event is scoped by a ScopeKey")
        for name in ("provider_role", "provider_id", "packet_posture"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise TelemetryRefused(f"{name} is a declared label")
            if "\n" in value:
                raise TelemetryRefused(
                    f"{name} carries one label, never a body of text")
        for name in ("source_count", "exempt_source_count", "packet_bytes",
                     "prompt_bytes"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TelemetryRefused(f"{name} is a measured integer")
            if value < 0:
                raise TelemetryRefused(f"{name} cannot be negative")
        if self.exempt_source_count > self.source_count:
            raise TelemetryRefused(
                "more sources were exempt than the packet carried")
        tokens = self.provider_tokens
        if not isinstance(tokens, DeclaredAbsence):
            if isinstance(tokens, bool) or not isinstance(tokens, int):
                raise TelemetryRefused(
                    "provider_tokens is a REPORTED integer or a declared "
                    "absence; there is no third answer")
            if tokens < 0:
                raise TelemetryRefused("provider_tokens cannot be negative")
        for name in ("client", "domain", "bill_to", "customer_subject_ref"):
            if not isinstance(getattr(self, name), DeclaredAbsence):
                raise TelemetryRefused(
                    f"{name} has no value on a self-hosted console and MUST "
                    "stay a declared absence: filling it would be a "
                    "placeholder in a usage record")

    def as_dict(self) -> dict[str, object]:
        tokens = self.provider_tokens
        return {
            "operation": self.operation,
            "workflow": self.scope.as_dict(),
            "provider_role": self.provider_role,
            "provider_id": self.provider_id,
            "packet_posture": self.packet_posture,
            "usage_units": {
                "source_count": self.source_count,
                "exempt_source_count": self.exempt_source_count,
                "packet_bytes": self.packet_bytes,
                "prompt_bytes": self.prompt_bytes,
                "provider_tokens": (tokens.as_dict()
                                    if isinstance(tokens, DeclaredAbsence)
                                    else tokens),
            },
            "client": self.client.as_dict(),
            "domain": self.domain.as_dict(),
            "bill_to": self.bill_to.as_dict(),
            "customer_subject_ref": self.customer_subject_ref.as_dict(),
        }


@dataclasses.dataclass(frozen=True, slots=True)
class SessionUsage:
    """The per-session totals: the same dimensions, summed over the scope's own
    turns. Per-session as well as per-turn because task 10.8 asks for both, and
    because a total nobody keeps is a total nobody can act on."""

    scope: ScopeKey
    turn_count: int
    source_count: int
    exempt_source_count: int
    packet_bytes: int
    prompt_bytes: int
    reported_provider_tokens: int | DeclaredAbsence

    def as_dict(self) -> dict[str, object]:
        tokens = self.reported_provider_tokens
        return {
            "workflow": self.scope.as_dict(),
            "turn_count": self.turn_count,
            "usage_units": {
                "source_count": self.source_count,
                "exempt_source_count": self.exempt_source_count,
                "packet_bytes": self.packet_bytes,
                "prompt_bytes": self.prompt_bytes,
                "provider_tokens": (tokens.as_dict()
                                    if isinstance(tokens, DeclaredAbsence)
                                    else tokens),
            },
            "client": ABSENT_CLIENT.as_dict(),
            "domain": ABSENT_DOMAIN.as_dict(),
            "bill_to": ABSENT_BILL_TO.as_dict(),
            "customer_subject_ref": ABSENT_SUBJECT.as_dict(),
        }


# ---------------------------------------------------------------------------
# the bounded in-process meter
# ---------------------------------------------------------------------------

MAX_METERED_SCOPES = 64


@dataclasses.dataclass(frozen=True, slots=True)
class EvictedSession:
    """What a meter answers for a scope whose totals it DROPPED to stay
    bounded.

    A distinct answer from ``None``, and that distinction is the point
    (adversarial review, F9): the meter used to return ``None`` for an evicted
    scope, which is byte-identical to the answer for a session that never ran —
    so a conversation with five hundred metered turns and one with none read
    the same. The totals are genuinely gone (dropping them is what the bound is
    for), so what is retained is the FACT that they existed and were dropped."""

    scope: ScopeKey

    def as_dict(self) -> dict[str, object]:
        return {"workflow": self.scope.as_dict(), "evicted": True,
                "reason": ("this scope's totals were dropped to keep the "
                           "in-process meter bounded; they are gone, and this "
                           "is NOT the answer for a session that never ran")}


class UsageMeter:
    """A bounded, thread-safe, per-instance meter.

    One per served process, held beside the turn store and never shared between
    two servers. It accumulates per-scope totals for at most
    ``MAX_METERED_SCOPES`` conversation scopes and evicts the oldest scope when
    a new one arrives, because an unbounded counter in a long-lived serve is a
    leak with a friendly name.

    It emits nowhere by itself: ``record`` returns the event it accumulated so
    the caller decides what to do with it. A meter that also wrote somewhere
    would be a second store, and the whole content-free argument depends on
    there being exactly one shape and one place it is built."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._totals: dict[ScopeKey, dict[str, int]] = {}
        self._reported_tokens: dict[ScopeKey, int | None] = {}
        # Which scopes were dropped, and how many times a drop happened. The
        # evicted ROSTER is itself bounded (it would otherwise be the leak the
        # bound exists to prevent), so the COUNTER is what survives when even
        # the roster rolls over — a reader can always tell that dropping is
        # happening, even where it can no longer tell which scope.
        self._evicted: dict[ScopeKey, None] = {}
        self._eviction_count = 0

    def record(self, usage: TurnUsage) -> TurnUsage:
        if not isinstance(usage, TurnUsage):
            raise TelemetryRefused("a meter records a TurnUsage")
        with self._lock:
            totals = self._totals.get(usage.scope)
            if totals is not None:
                # LEAST-RECENTLY-RECORDED eviction, not first-opened: the
                # busiest live conversation must not be the first one dropped
                # merely because it was opened first. Recording moves a scope
                # to the end, exactly as the turn store tracks recency.
                self._totals[usage.scope] = self._totals.pop(usage.scope)
            if totals is None:
                self._evicted.pop(usage.scope, None)
                if len(self._totals) >= MAX_METERED_SCOPES:
                    oldest = next(iter(self._totals))
                    self._totals.pop(oldest, None)
                    self._reported_tokens.pop(oldest, None)
                    self._eviction_count += 1
                    self._evicted[oldest] = None
                    while len(self._evicted) > MAX_METERED_SCOPES:
                        self._evicted.pop(next(iter(self._evicted)), None)
                totals = {"turn_count": 0, "source_count": 0,
                          "exempt_source_count": 0, "packet_bytes": 0,
                          "prompt_bytes": 0}
                self._totals[usage.scope] = totals
                self._reported_tokens[usage.scope] = None
            totals["turn_count"] += 1
            totals["source_count"] += usage.source_count
            totals["exempt_source_count"] += usage.exempt_source_count
            totals["packet_bytes"] += usage.packet_bytes
            totals["prompt_bytes"] += usage.prompt_bytes
            if isinstance(usage.provider_tokens, int):
                current = self._reported_tokens.get(usage.scope) or 0
                self._reported_tokens[usage.scope] = (
                    current + usage.provider_tokens)
        return usage

    def session(self, scope: ScopeKey) -> "SessionUsage | EvictedSession | None":
        """The totals for one conversation scope.

        THREE distinct answers, and the third is why this reads the way it does
        (adversarial review, F9): ``SessionUsage`` when the totals are held,
        ``EvictedSession`` when this scope WAS metered and its totals were
        dropped to keep the meter bounded, and ``None`` only when nothing was
        ever recorded for it. None rather than a zeroed row for the last case,
        for the same reason: a session that never ran is not a session that
        used nothing — and neither is one whose numbers were thrown away."""

        with self._lock:
            totals = self._totals.get(scope)
            if totals is None:
                if scope in self._evicted:
                    return EvictedSession(scope=scope)
                return None
            reported = self._reported_tokens.get(scope)
            snapshot = dict(totals)
        return SessionUsage(
            scope=scope,
            turn_count=snapshot["turn_count"],
            source_count=snapshot["source_count"],
            exempt_source_count=snapshot["exempt_source_count"],
            packet_bytes=snapshot["packet_bytes"],
            prompt_bytes=snapshot["prompt_bytes"],
            reported_provider_tokens=(ABSENT_PROVIDER_TOKENS
                                      if reported is None else reported),
        )

    def scopes(self) -> tuple[ScopeKey, ...]:
        with self._lock:
            return tuple(self._totals)

    def eviction_count(self) -> int:
        """How many scopes this meter has dropped. The one number that always
        survives, including after the evicted roster itself rolls over."""
        with self._lock:
            return self._eviction_count


def declared_absences() -> Mapping[str, str]:
    """Every metering field this console declares absent, with its reason —
    the auditable half of the PARTIAL conformance the memory-gateway
    declaration records for `Usage Metering Is Gateway-Owned`."""

    return {absence.field: absence.reason for absence in DECLARED_ABSENCES}
