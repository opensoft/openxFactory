"""WebRTC media peer + held-answer gate (FR-007).

Offline: ``SimulatedMediaPeer`` records the ordered steps and models first-output timing.
Live: ``AiortcMediaPeer`` (lazy ``aiortc``), deferred to the lab run. The provider answer
is applied ONLY after media authorization; the runner enforces that ordering and this
peer records the fact that it happened.
"""
from __future__ import annotations

from dataclasses import dataclass


class MediaGateError(Exception):
    pass


@dataclass
class SimulatedMediaPeer:
    """Offline media double with a held-answer gate."""

    apply_ms: float = 30.0
    first_input_ms: float = 25.0
    first_output_ms: float = 400.0   # after first input; feeds first_playable metric
    no_response: bool = False        # provider produced no playable output
    _answer_applied: bool = False
    _first_input_sent: bool = False

    def apply_answer(self, answer_token: str, *, authorized: bool) -> None:
        if not authorized:
            raise MediaGateError("refusing to apply answer before media authorization")
        if not answer_token:
            raise MediaGateError("no answer token")
        self._answer_applied = True

    def send_first_input(self) -> None:
        if not self._answer_applied:
            raise MediaGateError("cannot send input before answer applied")
        self._first_input_sent = True

    def first_output_playable(self) -> bool:
        return self._first_input_sent and not self.no_response

    @property
    def answer_applied(self) -> bool:
        return self._answer_applied


class AiortcMediaPeer:  # pragma: no cover - live path
    """Live WebRTC peer (lazy aiortc). Deferred to the lab run (T058)."""

    def __init__(self) -> None:
        self._pc = None

    def create_offer(self):
        import aiortc  # lazy

        raise NotImplementedError("live media peer is enabled during the lab run (T058)")
