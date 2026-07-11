"""Sideband control channel.

Offline: ``SimulatedSideband`` with configurable attach delay and failure. Live:
``WssSideband`` (lazy ``websockets``), deferred to the lab run. ``open`` and ``verify``
are distinct steps so the harness records ``t_sideband_open`` vs ``t_sideband_verified``.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulatedSideband:
    """Offline sideband double.

    ``open_ms`` / ``verify_ms`` feed the deterministic virtual timeline. ``fail`` models
    an attach/verification failure (F0-C). ``extra_delay_ms`` models an injected delay
    (F0-B) added before verification completes.
    """

    open_ms: float = 20.0
    verify_ms: float = 60.0
    extra_delay_ms: float = 0.0
    fail: bool = False
    _opened: bool = False
    _verified: bool = False

    def open(self) -> None:
        self._opened = True

    def verify(self) -> bool:
        if not self._opened:
            raise RuntimeError("sideband.verify called before open")
        self._verified = not self.fail
        return self._verified

    @property
    def total_verify_ms(self) -> float:
        return self.verify_ms + self.extra_delay_ms

    @property
    def verified(self) -> bool:
        return self._verified


class WssSideband:  # pragma: no cover - live path
    """Live sideband WSS client (lazy websockets). Deferred to the lab run (T058)."""

    def __init__(self, url: str, api_key: str) -> None:
        self._url = url
        self._api_key = api_key

    def open(self):
        import websockets  # lazy

        raise NotImplementedError("live sideband is enabled during the lab run (T058)")
