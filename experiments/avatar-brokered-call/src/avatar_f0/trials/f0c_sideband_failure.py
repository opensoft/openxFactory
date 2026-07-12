"""F0-C sideband-failure runner (FR-009) + readiness-timeout path (FR-012, US4).

Both variants must authorize NO media, apply NO answer, and terminate the call.
"""
from __future__ import annotations

from .. import FAIL, PASS
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..models import TrialResult
from .base import VirtualTimeline, _new_components, _run_handshake


def run(
    trial_id: str,
    deadline_ms: int = 3000,
    variant: str = "sideband_failure",
    registry: CallRegistry | None = None,
) -> TrialResult:
    registry = registry or CallRegistry()
    clock = TrialClock()
    tl = VirtualTimeline()
    if variant == "readiness_timeout":
        # Verification would succeed but lands past the deadline → timeout path.
        c = _new_components(sideband_extra_delay_ms=float(deadline_ms) + 1000.0)
        assertion = "F0-C-READINESS_TIMEOUT"
    else:
        c = _new_components(sideband_fail=True)
        assertion = "F0-C-NO_MEDIA"
    hs = _run_handshake(clock, tl, c["broker"], c["sideband"], c["media"], c["control"],
                        registry, f"req-{trial_id}", f"offer-{trial_id}", deadline_ms)
    ok = (not hs.authorized) and (not hs.answer_applied) and (not hs.first_output) and hs.terminated
    if variant == "readiness_timeout":
        ok = ok and hs.timed_out
    return TrialResult(
        trial_id=trial_id, group_id="F0-C",
        status=PASS if ok else FAIL,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=clock.offsets_ms(),
        assertion_ids=[assertion],
        note="" if ok else f"{variant}: media/answer leaked or call not terminated",
        provider_calls_created=hs.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
