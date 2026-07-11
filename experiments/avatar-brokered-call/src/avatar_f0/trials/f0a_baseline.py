"""F0-A baseline runner (FR-006/FR-008): held answer, ordered authorization, single call."""
from __future__ import annotations

from .. import FAIL, PASS
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..models import TrialResult
from .base import VirtualTimeline, _new_components, _ordering_ok, _run_handshake


def run(trial_id: str, deadline_ms: int = 3000, registry: CallRegistry | None = None) -> TrialResult:
    registry = registry or CallRegistry()
    clock = TrialClock()
    tl = VirtualTimeline()
    c = _new_components()
    request_id = f"req-{trial_id}"
    offer = f"offer-{trial_id}"
    hs = _run_handshake(clock, tl, c["broker"], c["sideband"], c["media"], c["control"],
                        registry, request_id, offer, deadline_ms)
    ok = (hs.verified and hs.authorized and hs.answer_applied and hs.first_output
          and _ordering_ok(clock) and hs.provider_calls_created == 1)
    return TrialResult(
        trial_id=trial_id, group_id="F0-A",
        status=PASS if ok else FAIL,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=clock.offsets_ms(),
        assertion_ids=["F0-A-ORDERING", "F0-A-SINGLE_CALL"],
        note="" if ok else "baseline handshake did not satisfy ordering/single-call",
        provider_calls_created=hs.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
