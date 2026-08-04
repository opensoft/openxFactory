"""Shared deterministic fixtures + seed recording for the AVC runtime suite.

pytest's default (prepend) import mode puts this file's directory
(``tests/avatar_runtime/``) on ``sys.path``, so tests can ``import fakes``,
``from _support import ...``, ``import boundary.scanner``, etc.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# The STRUCTURAL hermeticity guard (`tests/hermeticity.py`) is registered here
# as well as in `tests/conftest.py`, because a pytest run that makes this
# directory the rootdir excludes the suite-wide conftest from collection
# (FR-043; hookup set pinned by tests/ideation-dashboard/test_hermeticity.py).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    hermetic_binary_path,
    hermetic_external_runners,
)

from xfactory.avatar_runtime import build_runtime
from xfactory.avatar_runtime.clocks import ManualClock
from xfactory.avatar_runtime.ids import QueuedIdSource
from xfactory.avatar_runtime.telemetry import TelemetrySink
from xfactory.avatar_runtime.values import ConsentBinding, KillSwitchState

from _support import PURPOSE, SUBJECT, default_bundle
from fakes import FakeConsent, FakeOperation, FakePolicy, FakeProvider, FakeUsage


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
def policy_bundle():
    return default_bundle()


@pytest.fixture
def policy(policy_bundle) -> FakePolicy:
    # Broker resolves policy by request.subject_id.
    return FakePolicy({SUBJECT: policy_bundle})


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
    seed = getattr(config.option, "randomly_seed", None)
    if seed is not None:
        return f"avatar-runtime randomly-seed: {seed}"
    return None
