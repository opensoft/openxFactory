"""F0-B delayed-sideband runner (FR-006/FR-008): injected 1500-2500 ms delay, still ordered."""
from __future__ import annotations

from .. import FAIL, PASS
from ..candidate import READINESS_CEILING_MS
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..models import TrialResult
from .base import VirtualTimeline, _new_components, _ordering_ok, _run_handshake


def run(trial_id: str, deadline_ms: int = 3000, registry: CallRegistry | None = None) -> TrialResult:
    registry = registry or CallRegistry()
    clock = TrialClock()
    tl = VirtualTimeline()
    # Deterministic injected delay in [1500, 2500] ms varied by the trial index.
    idx = int(trial_id.rsplit("-", 1)[-1])
    extra = 1500.0 + (idx % 11) * 100.0
    c = _new_components(sideband_extra_delay_ms=extra)
    hs = _run_handshake(clock, tl, c["broker"], c["sideband"], c["media"], c["control"],
                        registry, f"req-{trial_id}", f"offer-{trial_id}", deadline_ms)
    offs = clock.offsets_ms()
    sideband_ready = offs.get("t_sideband_verified", float("inf"))
    ok = (hs.verified and hs.authorized and hs.answer_applied and hs.first_output
          and _ordering_ok(clock) and sideband_ready <= READINESS_CEILING_MS
          and sideband_ready <= deadline_ms and hs.provider_calls_created == 1)
    return TrialResult(
        trial_id=trial_id, group_id="F0-B",
        status=PASS if ok else FAIL,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=offs,
        assertion_ids=["F0-B-ORDERING", "F0-B-WITHIN_CEILING"],
        note="" if ok else "delayed-sideband trial missed ordering/ceiling",
        provider_calls_created=hs.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
