"""Single sequenced event log with producer-authority checks (FR-026)."""

from __future__ import annotations

from typing import Optional

from .values import EventKind, EventRecord, ProducerAuthority


class ProducerAuthorityError(Exception):
    """A non-runtime producer tried to append an authoritative result."""


class EventLog:
    def __init__(self) -> None:
        self._records: list[EventRecord] = []

    @property
    def last_sequence(self) -> int:
        return self._records[-1].sequence if self._records else 0

    def records(self) -> list[EventRecord]:
        return list(self._records)

    def append(
        self,
        kind: EventKind,
        producer: ProducerAuthority,
        payload: str,
        clock_ts: int,
    ) -> EventRecord:
        # Only the runtime authority may append an authoritative result;
        # a client/provider observation claiming authority is rejected.
        if kind is EventKind.AUTHORITATIVE_RESULT and producer is not ProducerAuthority.RUNTIME_AUTHORITY:
            raise ProducerAuthorityError(
                f"{producer.value} may not append an authoritative_result"
            )
        rec = EventRecord(
            sequence=self.last_sequence + 1,
            kind=kind,
            producer=producer,
            payload=payload,
            clock_ts=clock_ts,
        )
        self._records.append(rec)
        return rec

    def since(self, sequence: int) -> list[EventRecord]:
        return [r for r in self._records if r.sequence > sequence]
