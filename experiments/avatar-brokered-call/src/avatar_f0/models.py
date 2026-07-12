"""Shared result dataclasses (mirror the registered result schema)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TrialResult:
    trial_id: str
    group_id: str
    status: str  # PASS / FAIL / INCONCLUSIVE
    provider_request_id_hash: Optional[str]
    durations_ms: Dict[str, float] = field(default_factory=dict)
    assertion_ids: List[str] = field(default_factory=list)
    note: str = ""
    # Internal bookkeeping (not serialized verbatim):
    provider_calls_created: int = 0
    media_authorized: bool = False
    answer_applied: bool = False


@dataclass
class AssertionResult:
    id: str
    status: str
    passed_trials: int = 0
    failed_trials: int = 0
    note: str = ""


@dataclass
class GroupResult:
    id: str
    planned: int
    completed: int = 0
    passed: int = 0
    failed: int = 0
