"""Bounded cleanup registry and routine (FR-005).

Every created provider call ID is registered the moment it is known so that cleanup can
attempt termination for every known call — including on interruption. Cleanup records a
per-call outcome and never treats missing confirmation as success.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class CleanupOutcome:
    call_id_hash: str
    terminated: bool
    reason: str  # bounded reason code, never raw provider content


@dataclass
class CallRegistry:
    """Tracks known provider call-ID hashes and their terminal state."""

    _open: Dict[str, bool] = field(default_factory=dict)  # id_hash -> confirmed_terminated

    def register(self, call_id_hash: str) -> None:
        self._open.setdefault(call_id_hash, False)

    def mark_terminated(self, call_id_hash: str) -> None:
        if call_id_hash in self._open:
            self._open[call_id_hash] = True

    def open_calls(self) -> List[str]:
        return [cid for cid, done in self._open.items() if not done]

    def all_calls(self) -> List[str]:
        return list(self._open.keys())


def run_cleanup(
    registry: CallRegistry,
    terminate: Optional[Callable[[str], bool]] = None,
) -> List[CleanupOutcome]:
    """Attempt bounded termination for every known open call.

    ``terminate`` returns True when termination is confirmed. Absent a terminator
    (offline / no live handle) the outcome is recorded as unconfirmed, never success.
    """
    outcomes: List[CleanupOutcome] = []
    for cid in list(registry.all_calls()):
        if terminate is None:
            outcomes.append(CleanupOutcome(cid, terminated=False, reason="no_terminator"))
            continue
        try:
            ok = bool(terminate(cid))
        except Exception:  # pragma: no cover - defensive; never raise out of cleanup
            ok = False
        if ok:
            registry.mark_terminated(cid)
            outcomes.append(CleanupOutcome(cid, terminated=True, reason="terminated"))
        else:
            outcomes.append(CleanupOutcome(cid, terminated=False, reason="termination_unconfirmed"))
    return outcomes
