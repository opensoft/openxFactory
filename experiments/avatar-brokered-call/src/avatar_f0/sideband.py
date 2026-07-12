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


class SidebandError(Exception):
    pass


class WssSideband:  # pragma: no cover - live path, exercised only with a lab key
    """Live sideband WSS control channel for an existing call.

    Attaches to ``wss://api.openai.com/v1/realtime?call_id=<id>`` with the bearer key and
    treats the first server event as confirmation the session is live. This is the
    out-of-band control channel — distinct from the WebRTC media leg — so the harness can
    verify readiness while the provider answer is still held off the peer connection.
    ``open`` and ``verify`` are distinct so the harness records ``t_sideband_open`` vs
    ``t_sideband_verified``.
    """

    def __init__(self, call_id: str, api_key: str, base_url: str = "wss://api.openai.com") -> None:
        self._call_id = call_id
        self._api_key = api_key
        self._url = f"{base_url.rstrip('/')}/v1/realtime?call_id={call_id}"
        self._ws = None
        self._verified = False

    async def open(self) -> None:
        import websockets  # lazy

        # websockets 12.x legacy client uses ``extra_headers``.
        self._ws = await websockets.connect(
            self._url, extra_headers=[("Authorization", f"Bearer {self._api_key}")]
        )

    async def verify(self, timeout_s: float) -> bool:
        """Await the first control event; its arrival confirms the session is attachable."""
        import asyncio

        if self._ws is None:
            raise SidebandError("sideband.verify called before open")
        try:
            await asyncio.wait_for(self._ws.recv(), timeout=timeout_s)
            self._verified = True
        except Exception:
            self._verified = False
        return self._verified

    async def close(self) -> None:
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass

    @property
    def verified(self) -> bool:
        return self._verified
