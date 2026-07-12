"""Sideband control channel.

Offline: ``SimulatedSideband`` with configurable attach delay and failure. Live:
``WssSideband`` (lazy ``websockets``), deferred to the lab run. ``open`` and ``verify``
are distinct steps so the harness records ``t_sideband_open`` vs ``t_sideband_verified``.
"""
from __future__ import annotations

from dataclasses import dataclass

# Substrings in a server error frame that indicate the call is gone (termination probe,
# F0-D). Deliberately conservative: confirm/extend against the exact provider error type
# observed for a hung-up call on the lab re-run. A generic error is NOT a termination.
TERMINATION_ERROR_MARKERS = (
    "not_found", "not found", "call_not_found", "call_ended", "session_expired",
    "no active session", "invalid_call", "closed",
)


def _is_connection_closed(exc: Exception) -> bool:
    """True if ``exc`` is a websockets connection-closed signal (the strong 'call gone' cue)."""
    return type(exc).__name__ in (
        "ConnectionClosed", "ConnectionClosedOK", "ConnectionClosedError",
    )


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
    confirms the session with an ACTIVE probe (send a client event, await the server
    response). This is the out-of-band control channel — distinct from the WebRTC media
    leg — so the harness can verify readiness while the provider answer is still held off
    the peer connection. ``open`` and ``verify`` are distinct so the harness records
    ``t_sideband_open`` vs ``t_sideband_verified``.

    Empirical provider variance (lab, 2026-07-12): the GA ``?call_id=`` attach sends NO
    unsolicited greeting event (no ``session.created``) in either the held or the
    connected state, but it answers a client ``session.update`` with ``session.updated``
    in well under the readiness deadline — including while the answer is held. A passive
    first-event wait therefore never verifies; the active probe does.
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
        """Probe the control channel; a non-error server response confirms the session.

        Sends a benign ``session.update`` and awaits the reply (the provider emits no
        unsolicited event to wait for — see class docstring). An ``error`` reply or a
        non-JSON frame counts as NOT verified: fail closed.
        """
        import asyncio
        import json

        if self._ws is None:
            raise SidebandError("sideband.verify called before open")
        try:
            await self._ws.send(
                json.dumps({"type": "session.update", "session": {"type": "realtime"}})
            )
            reply = await asyncio.wait_for(self._ws.recv(), timeout=timeout_s)
            self._verified = json.loads(reply).get("type", "error") != "error"
        except Exception:
            self._verified = False
        return self._verified

    async def probe_terminated(self, timeout_s: float) -> str:
        """Active termination probe — INVERTED polarity from ``verify`` (F0-D revocation).

        Passively watching the media leg cannot see teardown within the 5 s bound (the
        provider emits no prompt terminal signal; aiortc's ICE-consent teardown is ~30 s).
        So after hangup we probe the control channel instead. Returns exactly one of:

          "terminated"    the socket closed, OR the server errored with a call-gone marker
                          → revocation observed
          "alive"         the server acknowledged (``session.updated``) → the call is STILL
                          live → revocation FAILED (must become a FAIL, never ignored)
          "inconclusive"  timeout, or an error/frame we cannot attribute to termination

        SAFETY: only a POSITIVE termination signal returns "terminated". A generic error, a
        non-JSON frame, or a timeout is "inconclusive" — never a false "terminated", which
        would falsely PASS the one assertion that proves we can actually kill a live call.
        The exact provider close-code / error-type for a hung-up call is confirmed on the
        lab re-run; extend ``TERMINATION_ERROR_MARKERS`` there if the provider errors rather
        than closing.
        """
        import asyncio
        import json

        if self._ws is None:
            return "inconclusive"
        try:
            await self._ws.send(
                json.dumps({"type": "session.update", "session": {"type": "realtime"}})
            )
            reply = await asyncio.wait_for(self._ws.recv(), timeout=timeout_s)
        except asyncio.TimeoutError:
            return "inconclusive"
        except Exception as exc:
            # A closed connection is the strong, unambiguous termination signal; any other
            # transport failure is inconclusive (cannot attribute to termination).
            return "terminated" if _is_connection_closed(exc) else "inconclusive"
        try:
            msg = json.loads(reply)
        except Exception:
            return "inconclusive"
        typ = msg.get("type", "")
        if typ == "session.updated":
            return "alive"          # still processing → revocation FAILED
        if typ == "error":
            blob = json.dumps(msg).lower()
            if any(m in blob for m in TERMINATION_ERROR_MARKERS):
                return "terminated"
            return "inconclusive"   # generic error — do NOT assume termination
        return "inconclusive"

    async def close(self) -> None:
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass

    @property
    def verified(self) -> bool:
        return self._verified
