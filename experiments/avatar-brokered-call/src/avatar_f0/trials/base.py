"""Shared trial-runner scaffold + deterministic per-group orchestration (FR-006/FR-007).

A trial runs on a deterministic virtual timeline so offline evidence is reproducible.
The provider answer is held until BOTH sideband verification and control authorization
complete; media authorization is granted only after sideband verification. All timings
are monotonic offsets from ``t_provider_create_accepted`` (t=0).

Trial-ID / count orchestration (FR-006): exactly six groups run their planned counts
(F0-A=20; F0-B–F0-F=10; 70 total) via :func:`iter_trial_ids`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional

from .. import FAIL, INCONCLUSIVE, PASS, GROUP_PLANNED
from ..broker import BrokerCreateFailed, IdempotencyConflict, SimulatedBroker, SimulatedTermination
from ..candidate import REVOCATION_BOUND_MS
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..control_stub import ControlLeaseStub
from ..media import SimulatedMediaPeer
from ..models import TrialResult
from ..sideband import SimulatedSideband

# The ordering invariant (baseline/delayed): each marker must be <= the next.
ORDER = (
    "t_sideband_verified",
    "t_answer_released",
    "t_lease_ack",
    "t_media_authorized",
    "t_answer_applied",
    "t_first_input_sent",
)


def iter_trial_ids(group_id: str) -> Iterator[str]:
    """Yield the deterministic trial IDs for a group at its planned count (FR-006)."""
    planned = GROUP_PLANNED[group_id]
    for i in range(1, planned + 1):
        yield f"{group_id}-{i:02d}"


class VirtualTimeline:
    """A monotonic virtual clock (nanoseconds) advanced in milliseconds."""

    def __init__(self) -> None:
        self.ns = 0

    def advance(self, ms: float) -> None:
        self.ns += int(round(ms * 1_000_000))


@dataclass
class Handshake:
    request_id_hash: Optional[str] = None
    call_id_hash: Optional[str] = None
    verified: bool = False
    authorized: bool = False
    answer_applied: bool = False
    first_input: bool = False
    first_output: bool = False
    timed_out: bool = False
    terminated: bool = False
    duplicate: bool = False
    provider_calls_created: int = 0


def _run_handshake(
    clock: TrialClock,
    tl: VirtualTimeline,
    broker: SimulatedBroker,
    sideband: SimulatedSideband,
    media: SimulatedMediaPeer,
    control: ControlLeaseStub,
    registry: CallRegistry,
    request_id: str,
    offer_fingerprint: str,
    deadline_ms: int,
) -> Handshake:
    """Drive one brokered handshake to first media, enforcing ordering + the deadline."""
    hs = Handshake()
    clock.mark("t_offer_ready", tl.ns)
    tl.advance(5.0)
    clock.mark("t_provider_create_sent", tl.ns)
    tl.advance(broker.create_ms)
    result = broker.create_call(request_id, offer_fingerprint)
    clock.mark("t_provider_create_accepted", tl.ns)  # t=0 origin
    origin_ns = tl.ns
    hs.request_id_hash = result.provider_request_id_hash
    hs.call_id_hash = result.call_id_hash
    hs.duplicate = result.duplicate
    hs.provider_calls_created = broker.provider_calls_created
    registry.register(result.call_id_hash)

    sideband.open()
    tl.advance(sideband.open_ms)
    clock.mark("t_sideband_open", tl.ns)
    verified = sideband.verify()
    tl.advance(sideband.total_verify_ms)
    hs.verified = verified

    # Readiness deadline: sideband verification must land within the selected deadline,
    # measured as a monotonic offset from t_provider_create_accepted (t=0).
    sideband_ready_ms = (tl.ns - origin_ns) / 1_000_000.0
    over_deadline = sideband_ready_ms > deadline_ms

    if not verified or over_deadline:
        # Fail-closed: no answer released, no authorization, terminate the call.
        hs.timed_out = over_deadline and verified
        control.revoke()
        tl.advance(10.0)
        clock.mark("t_hangup_sent", tl.ns)
        registry.mark_terminated(result.call_id_hash)
        hs.terminated = True
        return hs

    clock.mark("t_sideband_verified", tl.ns)
    tl.advance(2.0)
    clock.mark("t_answer_released", tl.ns)
    control.request_readiness()
    control.lease_ack()
    tl.advance(3.0)
    clock.mark("t_lease_ack", tl.ns)
    control.grant_authorization(sideband_verified=hs.verified)
    tl.advance(2.0)
    clock.mark("t_media_authorized", tl.ns)
    hs.authorized = control.is_authorized

    media.apply_answer(result.answer_token, authorized=hs.authorized)
    tl.advance(media.apply_ms)
    clock.mark("t_answer_applied", tl.ns)
    hs.answer_applied = media.answer_applied

    media.send_first_input()
    tl.advance(media.first_input_ms)
    clock.mark("t_first_input_sent", tl.ns)
    hs.first_input = True

    if media.first_output_playable():
        tl.advance(media.first_output_ms)
        clock.mark("t_first_output_playable", tl.ns)
        hs.first_output = True
    return hs


def _ordering_ok(clock: TrialClock) -> bool:
    offs = clock.offsets_ms()
    seq = [offs[m] for m in ORDER if m in offs]
    return all(seq[i] <= seq[i + 1] + 1e-9 for i in range(len(seq) - 1)) and len(seq) == len(ORDER)


def _new_components(
    *,
    sideband_fail: bool = False,
    sideband_extra_delay_ms: float = 0.0,
    no_response: bool = False,
    broker: Optional[SimulatedBroker] = None,
    termination: Optional[SimulatedTermination] = None,
):
    return {
        "broker": broker or SimulatedBroker(),
        "sideband": SimulatedSideband(fail=sideband_fail, extra_delay_ms=sideband_extra_delay_ms),
        "media": SimulatedMediaPeer(no_response=no_response),
        "control": ControlLeaseStub(),
        "termination": termination or SimulatedTermination(),
    }
