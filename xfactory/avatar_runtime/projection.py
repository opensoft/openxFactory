"""The AUTHORITY-OWNED workflow projection and the policy-required records.

WHAT THIS EXISTS TO MAKE CHECKABLE (task 6.3.5, ALV-008-S04). The policy's
`abort_scope` says an abort ENDS THE MEDIA PLANE ONLY, and that the
authority-owned workflow projection and the policy-required structured records
SURVIVE it. That is a claim about two different planes, and until the two are
separately addressable a reader can only take it on trust. These two values
are the addressable form: both serialize deterministically and both carry a
digest, so "survives an abort" becomes "the bytes are identical before and
after", which a test can assert and a mutation can break.

WHY THE PROJECTION CANNOT MOVE ON AN ABORT — structurally, not by promise. The
projection is built from the LOGICAL SESSION (its epoch, its policy and consent
versions, its state and revision) and from the AUTHORITATIVE_RESULT records in
the event log, which only the runtime authority may append. The media-plane
termination act touches none of those: it revokes a lease, hangs up an
idempotent provider call, drives the media ATTEMPT to a terminal status, and
invalidates the grant cache. There is no path from that act to this value, and
`tests/avatar_runtime/test_abort_scope.py` proves it by digest across a real
ROLLBACK-A abort.

THE RECORDS THAT SURVIVE are the ones policy requires be retained on every
terminal: the authoritative event records, the credential-free terminal
records (which never held secret material), and the closed session spend
records. Retention is APPEND-ONLY across an abort — an abort adds this leg's
terminal and its spend record, and removes nothing — so the test asserts the
pre-abort set is a subset of the post-abort set as well as asserting the
projection is byte-identical.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Optional

from .events import EventLog
from .session import LogicalSession
from .values import EventKind

_FIELD_SEPARATOR = "\x1f"
_RECORD_SEPARATOR = "\x1e"


def _digest(serialized: str) -> str:
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class WorkflowProjection:
    """The authority-owned projection of a logical session. Orthogonal to media."""

    session_id: str
    epoch: int
    policy_version: int
    consent_version: int
    state: str
    state_revision: int
    authoritative_events: tuple[tuple[int, str, str], ...]

    def serialize(self) -> str:
        head = _FIELD_SEPARATOR.join(
            [
                self.session_id,
                str(self.epoch),
                str(self.policy_version),
                str(self.consent_version),
                self.state,
                str(self.state_revision),
            ]
        )
        events = _RECORD_SEPARATOR.join(
            _FIELD_SEPARATOR.join([str(seq), producer, payload])
            for seq, producer, payload in self.authoritative_events
        )
        return head + _RECORD_SEPARATOR + events

    def digest(self) -> str:
        return _digest(self.serialize())


@dataclass(frozen=True)
class PolicyRequiredRecords:
    """The structured records retained on every terminal. Append-only."""

    session_id: str
    authoritative_events: tuple[tuple[int, str, str], ...]
    credential_free_terminals: tuple[tuple[str, str], ...]
    spend_records: tuple[tuple[str, str, str, int, int, str, str], ...]

    def serialize(self) -> str:
        parts = [self.session_id]
        parts += [
            _FIELD_SEPARATOR.join([str(seq), producer, payload])
            for seq, producer, payload in self.authoritative_events
        ]
        parts += [_FIELD_SEPARATOR.join(item) for item in self.credential_free_terminals]
        parts += [
            _FIELD_SEPARATOR.join(str(field) for field in record)
            for record in self.spend_records
        ]
        return _RECORD_SEPARATOR.join(parts)

    def digest(self) -> str:
        return _digest(self.serialize())


def _authoritative_events(log: Optional[EventLog]) -> tuple[tuple[int, str, str], ...]:
    if log is None:
        return ()
    return tuple(
        (record.sequence, record.producer.value, record.payload)
        for record in log.records()
        if record.kind is EventKind.AUTHORITATIVE_RESULT
    )


def project(session: LogicalSession, log: Optional[EventLog]) -> WorkflowProjection:
    """Build the authority-owned projection of one logical session."""
    return WorkflowProjection(
        session_id=session.session_id,
        epoch=session.epoch,
        policy_version=session.policy_version,
        consent_version=session.consent_version,
        state=session.state.value,
        state_revision=session.state_revision,
        authoritative_events=_authoritative_events(log),
    )


def policy_required_records(
    session: LogicalSession,
    log: Optional[EventLog],
    terminals: tuple[tuple[str, str], ...],
    spend_records: tuple,
) -> PolicyRequiredRecords:
    """Collect the records policy requires be retained on every terminal."""
    return PolicyRequiredRecords(
        session_id=session.session_id,
        authoritative_events=_authoritative_events(log),
        credential_free_terminals=tuple(sorted(terminals)),
        spend_records=tuple(
            (
                record.session_id,
                record.tenant_ref,
                record.attempt_ref,
                record.billable_units,
                record.usd_cents,
                record.outcome.value,
                record.reason.value,
            )
            for record in spend_records
        ),
    )
