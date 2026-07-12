"""Assertion aggregation (FR-006/FR-008/FR-009/FR-010).

Aggregates per-trial pass/fail into the schema's ``assertions`` array. A trial contributes
to each assertion it carries: PASS trials count as passed, FAIL as failed, INCONCLUSIVE as
neither (missing evidence). This module ONLY aggregates trial-derived assertions; bounded
cleanup lives in :mod:`avatar_f0.cleanup` and redaction scanning in
:mod:`avatar_f0.redaction` (wired from the run/evidence paths, not here).
"""
from __future__ import annotations

from typing import Dict, List

from . import FAIL, INCONCLUSIVE, PASS
from .models import AssertionResult, TrialResult


def aggregate_assertions(trials: List[TrialResult]) -> List[AssertionResult]:
    acc: Dict[str, Dict[str, int]] = {}
    order: List[str] = []
    for t in trials:
        for aid in t.assertion_ids:
            if aid not in acc:
                acc[aid] = {"passed": 0, "failed": 0, "incon": 0}
                order.append(aid)
            if t.status == PASS:
                acc[aid]["passed"] += 1
            elif t.status == FAIL:
                acc[aid]["failed"] += 1
            else:
                acc[aid]["incon"] += 1
    out: List[AssertionResult] = []
    for aid in order:
        c = acc[aid]
        if c["failed"] > 0:
            status = FAIL
        elif c["passed"] > 0 and c["incon"] == 0:
            status = PASS
        else:
            status = INCONCLUSIVE
        out.append(AssertionResult(id=aid, status=status,
                                   passed_trials=c["passed"], failed_trials=c["failed"]))
    return out
