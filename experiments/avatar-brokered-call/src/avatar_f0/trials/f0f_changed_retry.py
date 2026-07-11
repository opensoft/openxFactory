"""F0-F changed-retry runner (FR-010): idempotency conflict; no 2nd call, no old answer."""
from __future__ import annotations

from .. import FAIL, PASS
from ..broker import IdempotencyConflict, SimulatedBroker
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
    hs = _run_handshake(clock, tl, broker, c["sideband"], c["media"], c["control"],
                        registry, request_id, f"offer-{trial_id}-A", deadline_ms)
    # Reuse the request ID with a CHANGED offer fingerprint.
    conflict = False
    disclosed_answer = None
    try:
        r = broker.create_call(request_id, f"offer-{trial_id}-B")
        disclosed_answer = r.answer_token
    except IdempotencyConflict:
        conflict = True
    ok = (conflict and broker.provider_calls_created == 1 and disclosed_answer is None)
    return TrialResult(
        trial_id=trial_id, group_id="F0-F",
        status=PASS if ok else FAIL,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=clock.offsets_ms(),
        assertion_ids=["F0-F-IDEMPOTENCY"],
        note="" if ok else "changed retry created a 2nd call or disclosed a prior answer",
        provider_calls_created=broker.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
