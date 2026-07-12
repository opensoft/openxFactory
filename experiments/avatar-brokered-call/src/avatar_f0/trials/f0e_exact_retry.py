"""F0-E exact-retry runner (FR-010): at most one provider call, equivalent result."""
from __future__ import annotations

from .. import FAIL, PASS
from ..broker import SimulatedBroker
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..models import TrialResult
from .base import VirtualTimeline, _new_components, _run_handshake


def run(trial_id: str, deadline_ms: int = 3000, registry: CallRegistry | None = None) -> TrialResult:
    registry = registry or CallRegistry()
    clock = TrialClock()
    tl = VirtualTimeline()
    broker = SimulatedBroker()
    c = _new_components(broker=broker)
    request_id = f"req-{trial_id}"
    offer = f"offer-{trial_id}"
    hs = _run_handshake(clock, tl, broker, c["sideband"], c["media"], c["control"],
                        registry, request_id, offer, deadline_ms)
    # Simulate a lost response and retry the IDENTICAL request + offer.
    retry = broker.create_call(request_id, offer)
    ok = (broker.provider_calls_created == 1 and retry.duplicate
          and retry.call_id_hash == hs.call_id_hash)
    return TrialResult(
        trial_id=trial_id, group_id="F0-E",
        status=PASS if ok else FAIL,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=clock.offsets_ms(),
        assertion_ids=["F0-E-SINGLE_CALL"],
        note="" if ok else "exact retry created a duplicate provider call",
        provider_calls_created=broker.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
