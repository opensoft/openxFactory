"""Overall PASS/FAIL/INCONCLUSIVE derivation (FR-016).

- PASS  iff every mandatory trial ran, every assertion passed, all metric bounds held,
        and redaction passed.
- FAIL  iff any reproduced contrary observation (trial/assertion FAIL, metric-bound miss,
        or redaction finding).
- INCONCLUSIVE iff a mandatory trial did not run / lacked evidence (never PASS).

A p95/hard-ceiling miss is checked against p95/max directly — it can never be averaged
away.
"""
from __future__ import annotations

from typing import Dict, List

from . import FAIL, INCONCLUSIVE, PASS
from .models import AssertionResult, GroupResult, TrialResult

# PASS metric bounds (SC-002/SC-003/SC-005).
BOUNDS = {
    "sideband_ready_ms": {"p95": 3000.0, "max": 5000.0},
    "first_playable_after_authorized_ms": {"p95": 2000.0},
    "hangup_to_terminal_ms": {"max": 5000.0},
}


def metric_bound_failures(metrics: Dict[str, Dict[str, float]]) -> List[str]:
    fails: List[str] = []
    for name, bound in BOUNDS.items():
        summary = metrics.get(name, {})
        if summary.get("count", 0) == 0:
            continue  # no samples → handled by trial/group completeness, not a bound fail
        for stat, limit in bound.items():
            if summary.get(stat, 0.0) > limit:
                fails.append(f"{name}.{stat}>{limit}")
    return fails


def classify_overall(
    groups: List[GroupResult],
    trials: List[TrialResult],
    assertions: List[AssertionResult],
    metrics: Dict[str, Dict[str, float]],
    redaction_status: str,
    environment_inconclusive: bool = False,
) -> str:
    # Fail-closed: any reproduced contrary observation ⇒ FAIL.
    if redaction_status == FAIL:
        return FAIL
    if any(t.status == FAIL for t in trials):
        return FAIL
    if any(a.status == FAIL for a in assertions):
        return FAIL
    if metric_bound_failures(metrics):
        return FAIL

    # Missing / insufficient evidence ⇒ INCONCLUSIVE (never PASS).
    if environment_inconclusive or redaction_status == INCONCLUSIVE:
        return INCONCLUSIVE
    for g in groups:
        if g.completed != g.planned or g.passed != g.planned:
            return INCONCLUSIVE
    if any(t.status == INCONCLUSIVE for t in trials):
        return INCONCLUSIVE
    if any(a.status == INCONCLUSIVE for a in assertions):
        return INCONCLUSIVE
    return PASS
