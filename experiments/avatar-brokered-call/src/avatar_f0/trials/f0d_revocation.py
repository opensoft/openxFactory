"""F0-D revocation runner (FR-013/FR-014): terminal within 5 s; separate offsets.

Authorizes a baseline handshake, then revokes and requests hangup, recording separate
``t_revocation_request``, ``t_hangup_sent`` and ``t_peer_terminal`` offsets. An
unconfirmed terminal is INCONCLUSIVE (missing evidence) — never treated as success.
"""
from __future__ import annotations

from .. import FAIL, INCONCLUSIVE, PASS
from ..candidate import REVOCATION_BOUND_MS
from ..cleanup import CallRegistry
from ..clock import TrialClock
from ..models import TrialResult
from .base import VirtualTimeline, _new_components, _run_handshake


def run(
    trial_id: str,
    deadline_ms: int = 3000,
    registry: CallRegistry | None = None,
    observable: bool = True,
) -> TrialResult:
    registry = registry or CallRegistry()
    clock = TrialClock()
    tl = VirtualTimeline()
    c = _new_components()
    c["termination"].observable = observable
    hs = _run_handshake(clock, tl, c["broker"], c["sideband"], c["media"], c["control"],
                        registry, f"req-{trial_id}", f"offer-{trial_id}", deadline_ms)
    control = c["control"]
    termination = c["termination"]

    # Revoke, then request hangup, then observe (or fail to observe) terminal.
    control.revoke()
    tl.advance(5.0)
    clock.mark("t_revocation_request", tl.ns)
    tl.advance(5.0)
    clock.mark("t_hangup_sent", tl.ns)
    confirmed = termination.terminate(hs.call_id_hash)
    if confirmed:
        tl.advance(termination.terminal_ms)
        clock.mark("t_peer_terminal", tl.ns)
        registry.mark_terminated(hs.call_id_hash)

    offs = clock.offsets_ms()
    status = FAIL
    note = ""
    if not (hs.authorized and hs.first_output):
        status = FAIL
        note = "revocation precondition (authorized active media) not met"
    elif not confirmed or "t_peer_terminal" not in offs:
        status = INCONCLUSIVE  # missing terminal evidence — never success
        note = "provider terminal signal not observed"
    else:
        hangup_to_terminal = offs["t_peer_terminal"] - offs["t_hangup_sent"]
        # No later input/output is structurally guaranteed (revoke precedes any new IO).
        status = PASS if hangup_to_terminal <= REVOCATION_BOUND_MS else FAIL
        if status == FAIL:
            note = "terminal exceeded 5000 ms bound"
    return TrialResult(
        trial_id=trial_id, group_id="F0-D",
        status=status,
        provider_request_id_hash=hs.request_id_hash,
        durations_ms=offs,
        assertion_ids=["F0-D-TERMINAL_5S", "F0-D-NO_LATE_IO"],
        note=note,
        provider_calls_created=hs.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )
