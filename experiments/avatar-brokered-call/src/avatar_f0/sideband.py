"""Sideband control channel.

Offline: ``SimulatedSideband`` with configurable attach delay and failure. Live:
``WssSideband`` (lazy ``websockets``), deferred to the lab run. ``open`` and ``verify``
are distinct steps so the harness records ``t_sideband_open`` vs ``t_sideband_verified``.
"""
from __future__ import annotations

from dataclasses import dataclass

# EXACT provider error codes/types that mean the call is gone (termination probe, F0-D).
# Matched by exact equality against the error frame's code/type field ONLY — never substring
# over the serialized blob (a benign message containing e.g. "closed"/"disclosed" must not
# read as termination). Deliberately conservative and possibly INCOMPLETE: confirm/extend
# against the exact code observed for a hung-up call on the lab re-run.
TERMINATION_ERROR_CODES = frozenset({
    "call_not_found", "session_not_found", "unknown_call", "invalid_call_id",
    "call_ended", "session_ended", "session_expired",
})


def _error_code(msg: dict) -> str:
    """The error frame's code/type, lowercased — for EXACT matching against call-gone codes."""
    err = msg.get("error")
    if isinstance(err, dict):
        return str(err.get("code") or err.get("type") or "").strip().lower()
    return str(msg.get("code") or "").strip().lower()


def _close_verdict(exc: Exception) -> str:
    """Classify a raised exception during the probe.

    Only a CLEAN close (1000/1001) attributes to call termination; an abnormal close
    (1006/1011) or any other transport failure of the out-of-band control channel cannot be
    attributed to the media call's teardown → "inconclusive" (never a false "terminated").
    """
    if type(exc).__name__ not in ("ConnectionClosed", "ConnectionClosedOK", "ConnectionClosedError"):
        return "inconclusive"
    code = getattr(exc, "code", None)
    if code is None:
        rcvd = getattr(exc, "rcvd", None)
        code = getattr(rcvd, "code", None) if rcvd is not None else None
    return "terminated" if code in (1000, 1001) else "inconclusive"


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

          "terminated"    the socket CLEANLY closed (1000/1001), OR the server errored with a
                          confirmed call-gone code → revocation observed
          "alive"         the server acknowledged our update (``session.updated``) → the call
                          is STILL live → revocation FAILED (must become a FAIL, never ignored)
          "inconclusive"  deadline/timeout, an abnormal close, or no attributable signal

        The ``?call_id=`` socket is the ACTIVE session's server-event channel, so response.*/
        conversation.* events queued before the probe are read first — we DRAIN and ignore
        them, classifying only on a DEFINITIVE, correlated signal within the bound. Our
        ``session.update`` carries a unique ``event_id`` (no stale ``session.updated`` can
        exist after ``verify`` consumed its own ack), so a ``session.updated`` observed here
        is this probe's reply → the call is alive.

        SAFETY: only a POSITIVE termination signal returns "terminated" (exact-code match, or
        a CLEAN close) — never a substring, a generic/other error, an abnormal close, or a
        stale frame. Everything else drains or falls to "inconclusive"; a false "terminated"
        would wrongly PASS the assertion that proves we can actually kill a live call. The
        exact provider close-code / error-code for a hung-up call is confirmed on the lab
        re-run; extend ``TERMINATION_ERROR_CODES`` there if it errors rather than closing.
        """
        import asyncio
        import json

        if self._ws is None:
            return "inconclusive"
        event_id = f"f0-term-probe-{id(self):x}"
        try:
            await self._ws.send(json.dumps(
                {"type": "session.update", "event_id": event_id, "session": {"type": "realtime"}}
            ))
        except Exception as exc:
            return _close_verdict(exc)

        loop = asyncio.get_event_loop()
        end = loop.time() + max(0.0, timeout_s)
        while True:
            remaining = end - loop.time()
            if remaining <= 0:
                return "inconclusive"           # no definitive signal within the bound
            try:
                reply = await asyncio.wait_for(self._ws.recv(), timeout=remaining)
            except asyncio.TimeoutError:
                return "inconclusive"
            except Exception as exc:
                return _close_verdict(exc)
            try:
                msg = json.loads(reply)
            except Exception:
                continue                        # non-JSON frame → ignore, keep draining
            typ = msg.get("type", "")
            if typ == "session.updated":
                return "alive"                  # our update was acked → call still live
            if typ == "error" and _error_code(msg) in TERMINATION_ERROR_CODES:
                return "terminated"             # confirmed call-gone code
            # unrelated queued server event, or a non-call-gone error → drain and keep looking
            continue

    async def close(self) -> None:
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass

    @property
    def verified(self) -> bool:
        return self._verified
