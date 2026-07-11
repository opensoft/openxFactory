"""Shared deterministic fixtures + seed recording for the AVC runtime suite.

pytest's default (prepend) import mode puts this file's directory
(``tests/avatar_runtime/``) on ``sys.path``, so tests can ``import fakes``,
``import boundary.scanner``, ``import conformance.check_conformance``, etc.
"""

from __future__ import annotations

import pytest

from xfactory.avatar_runtime import build_runtime
from xfactory.avatar_runtime.clocks import ManualClock
from xfactory.avatar_runtime.ids import QueuedIdSource
from xfactory.avatar_runtime.telemetry import TelemetrySink
from xfactory.avatar_runtime.values import (
    ConsentBinding,
    KillSwitchState,
    PolicyBundle,
)

from fakes import FakeConsent, FakeOperation, FakePolicy, FakeProvider, FakeUsage

SUBJECT = "subject-1"
IDENTITY = "identity-1"
TENANT = "tenant-1"
PROFILE = "profile-standard"
PURPOSE = "avatar.voice"


@pytest.fixture
def clock() -> ManualClock:
    return ManualClock()


@pytest.fixture
def ids() -> QueuedIdSource:
    return QueuedIdSource()


@pytest.fixture
def provider() -> FakeProvider:
    return FakeProvider()


@pytest.fixture
def policy_bundle() -> PolicyBundle:
    return PolicyBundle(
        identity_ref=IDENTITY,
        required_purposes=frozenset({PURPOSE}),
        speech_gate="gate-default",
        retention_ticks=100,
        concurrency_cap=2,
        duration_cap_ticks=1000,
        confirmation_required=True,
    )


@pytest.fixture
def policy(policy_bundle: PolicyBundle) -> FakePolicy:
    return FakePolicy({IDENTITY: policy_bundle})


@pytest.fixture
def consent() -> FakeConsent:
    return FakeConsent({SUBJECT: ConsentBinding(SUBJECT, version=1, valid=True)})


@pytest.fixture
def operation() -> FakeOperation:
    return FakeOperation()


@pytest.fixture
def usage() -> FakeUsage:
    return FakeUsage()


@pytest.fixture
def telemetry() -> TelemetrySink:
    return TelemetrySink()


@pytest.fixture
def runtime(clock, ids, provider, policy, consent, operation, usage, telemetry):
    return build_runtime(
        clock=clock,
        ids=ids,
        provider=provider,
        policy=policy,
        consent=consent,
        operation=operation,
        usage=usage,
        kill_switch=KillSwitchState(),
        telemetry=telemetry,
    )


# --- Seed recording (SC-003) --------------------------------------------- #
def pytest_report_header(config):
    """Surface the pytest-randomly seed so a failing run is reproducible."""
    seed = getattr(config.option, "randomly_seed", None)
    if seed is not None:
        return f"avatar-runtime randomly-seed: {seed}"
    return None
