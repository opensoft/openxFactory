"""Timing metric summaries (SC-002/SC-003/SC-005).

Produces the three ``duration_summary`` metrics the result schema requires. A p95/max
miss is never averaged away — the bounds are checked against p95/max directly in
classification.
"""
from __future__ import annotations

import math
from typing import Dict, List

from .models import TrialResult


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    rank = (p / 100.0) * (len(s) - 1)
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return s[int(rank)]
    return s[lo] + (s[hi] - s[lo]) * (rank - lo)


def duration_summary(values: List[float]) -> Dict[str, float]:
    return {
        "count": len(values),
        "p50": round(percentile(values, 50), 3),
        "p95": round(percentile(values, 95), 3),
        "max": round(max(values), 3) if values else 0.0,
    }


def build_metrics(trials: List[TrialResult]) -> Dict[str, Dict[str, float]]:
    sideband_ready: List[float] = []
    first_playable: List[float] = []
    hangup_terminal: List[float] = []
    for t in trials:
        if t.status != "PASS":
            continue
        d = t.durations_ms
        if t.group_id in ("F0-A", "F0-B") and "t_sideband_verified" in d:
            sideband_ready.append(d["t_sideband_verified"])
        if "t_first_output_playable" in d and "t_media_authorized" in d:
            first_playable.append(d["t_first_output_playable"] - d["t_media_authorized"])
        if t.group_id == "F0-D" and "t_peer_terminal" in d and "t_hangup_sent" in d:
            hangup_terminal.append(d["t_peer_terminal"] - d["t_hangup_sent"])
    return {
        "sideband_ready_ms": duration_summary(sideband_ready),
        "first_playable_after_authorized_ms": duration_summary(first_playable),
        "hangup_to_terminal_ms": duration_summary(hangup_terminal),
    }
