"""Snapshot barrier B, ordered drain, overflow restart (ARR-006-S03/S04, FR-027)."""

from __future__ import annotations

import pytest

from xfactory.avatar_runtime.events import EventLog
from xfactory.avatar_runtime.snapshots import RecoveryOverflow, SnapshotRecovery
from xfactory.avatar_runtime.values import EventKind, ProducerAuthority


def _obs(log: EventLog, payload: str, ts: int):
    return log.append(EventKind.OBSERVATION, ProducerAuthority.CLIENT, payload, ts)


def test_event_during_projection_ordered_after_barrier():
    log = EventLog()
    _obs(log, "e1", 1)
    _obs(log, "e2", 2)
    rec = SnapshotRecovery(log)
    barrier = rec.begin()  # B = 2
    e3 = _obs(log, "e3", 3)  # arrives after barrier, before snapshot applied
    rec.observe(e3)
    snap = rec.snapshot()
    assert barrier == 2 and snap.last_event_sequence == 2
    assert snap.projection_through_b == ("e1", "e2")
    drained = rec.drain()
    assert [r.payload for r in drained] == ["e3"]


def test_buffer_overflow_aborts_and_restarts():
    log = EventLog()
    rec = SnapshotRecovery(log, buffer_bound=2)
    rec.begin()
    with pytest.raises(RecoveryOverflow):
        for i in range(5):
            rec.observe(_obs(log, f"e{i}", i + 1))
    rec.restart()  # fresh snapshot, no partial replay
    assert rec.restarts == 1


def test_no_historical_replay_endpoint():
    # There is no method to replay historical events; the API exposes only
    # snapshot + bounded drain.
    assert not hasattr(SnapshotRecovery, "replay_history")
