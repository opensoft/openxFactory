"""Shared deterministic test support (constants, request/ack builders, factory).

Imported by ``conftest.py`` (for fixtures) and by test modules directly.
"""

from __future__ import annotations

from xfactory.avatar_runtime import build_runtime
from xfactory.avatar_runtime.clocks import ManualClock
from xfactory.avatar_runtime.ids import QueuedIdSource
from xfactory.avatar_runtime.telemetry import TelemetrySink
from xfactory.avatar_runtime.values import (
    ConsentBinding,
    KillSwitchState,
    LeaseAck,
    Offer,
    PolicyBundle,
    Request,
)

from fakes import FakeConsent, FakeOperation, FakePolicy, FakeProvider, FakeUsage

SUBJECT = "subject-1"
IDENTITY = "identity-1"
TENANT = "tenant-1"
PROFILE = "profile-standard"
PURPOSE = "avatar.voice"


def default_bundle() -> PolicyBundle:
    return PolicyBundle(
        identity_ref=IDENTITY,
        required_purposes=frozenset({PURPOSE}),
        speech_gate="gate-default",
        retention_ticks=100,
        concurrency_cap=2,
        duration_cap_ticks=1000,
        confirmation_required=True,
    )


def make_request(
    request_id: str = "req-1",
    *,
    session_id: str = "sess-1",
    instance_id: str = "inst-1",
    epoch: int = 0,
    subject_id: str = SUBJECT,
    purposes=frozenset({PURPOSE}),
    sdp: str = "m=audio 9 UDP",
    profile: str = PROFILE,
    tenant: str = TENANT,
    resume_ref=None,
    client_ts: int = 0,
    transport_nonce: str = "",
    retry_count: int = 0,
) -> Request:
    return Request(
        request_id=request_id,
        session_id=session_id,
        subject_id=subject_id,
        instance_id=instance_id,
        epoch=epoch,
        purposes=purposes,
        offer=Offer(sdp_media=sdp, model_profile=profile),
        tenant_ref=tenant,
        resume_ref=resume_ref,
        client_ts=client_ts,
        transport_nonce=transport_nonce,
        retry_count=retry_count,
    )


def ack_for(runtime, session_id: str, *, transport_identity=None) -> LeaseAck:
    lease = runtime.registry.get(session_id).pending_attempt.lease
    return LeaseAck(
        lease_id=lease.lease_id,
        session_id=lease.session_id,
        epoch=lease.epoch,
        instance_id=lease.instance_id,
        attempt_id=lease.attempt_id,
        transport_identity=transport_identity or lease.transport_identity,
    )


def authorize(runtime, session_id: str):
    """Drive a granted attempt through both control channels to authorization."""
    runtime.open_sideband(session_id)
    runtime.verify_sideband(session_id)
    return runtime.submit_lease_ack(session_id, ack_for(runtime, session_id))


def build_fresh_runtime():
    """A brand-new runtime with fresh deterministic fakes (for determinism tests)."""
    return build_runtime(
        clock=ManualClock(),
        ids=QueuedIdSource(),
        provider=FakeProvider(),
        policy=FakePolicy({SUBJECT: default_bundle()}),
        consent=FakeConsent({SUBJECT: ConsentBinding(SUBJECT, 1, True)}),
        operation=FakeOperation(),
        usage=FakeUsage(),
        kill_switch=KillSwitchState(),
        telemetry=TelemetrySink(),
    )
