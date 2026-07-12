"""Monotonic instrumentation (FR-011).

All trial offsets are measured from ``t_provider_create_accepted`` (t=0) with a
monotonic clock. Wall-clock is coarse run metadata only.
"""
from __future__ import annotations

import time
from typing import Callable, Dict, Optional

# The protocol timing points (offsets recorded from provider-create acceptance).
MARKERS = (
    "t_offer_ready",
    "t_provider_create_sent",
    "t_provider_create_accepted",  # t=0 origin
    "t_sideband_open",
    "t_sideband_verified",
    "t_answer_released",
    "t_lease_ack",
    "t_media_authorized",
    "t_answer_applied",
    "t_first_input_sent",
    "t_first_output_playable",
    "t_revocation_request",
    "t_hangup_sent",
    "t_peer_terminal",
)


class TrialClock:
    """Records monotonic markers and exposes millisecond offsets from t=0.

    ``now_ns`` is injectable so tests can drive deterministic timings.
    """

    def __init__(self, now_ns: Optional[Callable[[], int]] = None) -> None:
        self._now_ns = now_ns or time.monotonic_ns
        self._marks_ns: Dict[str, int] = {}
        self._origin_ns: Optional[int] = None

    def mark(self, name: str, at_ns: Optional[int] = None) -> None:
        if name not in MARKERS:
            raise ValueError(f"unknown marker: {name}")
        ns = at_ns if at_ns is not None else self._now_ns()
        self._marks_ns[name] = ns
        if name == "t_provider_create_accepted":
            self._origin_ns = ns

    def has(self, name: str) -> bool:
        return name in self._marks_ns

    def offsets_ms(self) -> Dict[str, float]:
        """Return millisecond offsets from t=0 for every recorded marker except origin.

        Requires the origin marker to have been recorded.
        """
        if self._origin_ns is None:
            raise RuntimeError("t_provider_create_accepted not recorded; no timing origin")
        out: Dict[str, float] = {}
        for name, ns in self._marks_ns.items():
            if name == "t_provider_create_accepted":
                continue
            out[name] = max(0.0, (ns - self._origin_ns) / 1_000_000.0)
        return out

    def offset_ms(self, name: str) -> float:
        return self.offsets_ms()[name]
