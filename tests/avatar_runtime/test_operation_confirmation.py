"""Confirmation supersession + idempotent operation (ARR-007-S02, FR-029)."""

from __future__ import annotations

from xfactory.avatar_runtime.operations import OperationRunner
from xfactory.avatar_runtime.values import ConfirmationDecision

from fakes import FakeOperation


def test_superseded_confirmation_blocks_operation():
    op = FakeOperation()
    runner = OperationRunner(op)
    stale = ConfirmationDecision(confirmation_version=1, valid_until=10, superseded=True)
    assert runner.run("op-1", stale, now=5, effect="charge") is False
    assert op.effects == []  # no effect recorded; fresh confirmation required


def test_expired_confirmation_blocks_operation():
    op = FakeOperation()
    runner = OperationRunner(op)
    expired = ConfirmationDecision(confirmation_version=1, valid_until=3)
    assert runner.run("op-1", expired, now=5, effect="charge") is False
    assert op.effects == []


def test_fresh_confirmation_executes_idempotently_under_key():
    op = FakeOperation()
    runner = OperationRunner(op)
    fresh = ConfirmationDecision(confirmation_version=2, valid_until=10)
    assert runner.run("op-1", fresh, now=5, effect="charge") is True
    # Same external-operation key -> idempotent, effect not repeated.
    assert runner.run("op-1", fresh, now=6, effect="charge") is True
    assert op.effects == ["charge"]
