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


class AiortcMediaPeer:  # pragma: no cover - live path, exercised only with a lab key
    """Live WebRTC peer with the held-answer gate (FR-007).

    The provider answer SDP is applied to the peer connection ONLY via ``apply_answer``,
    and only when ``authorized`` is true — so the runner enforces "no media before both
    control channels verify + control authorizes." First inbound audio frame ⇒ first
    playable output. SDP is never logged. Constructed lazily so ``aiortc`` is imported
    only on the live path.
    """

    def __init__(self) -> None:
        import asyncio

        from aiortc import RTCPeerConnection  # lazy

        self._pc = RTCPeerConnection()
        self._answer_applied = False
        self._first_output = asyncio.Event()
        self._terminal = asyncio.Event()
        self._watch_late = False        # armed at revoke; a frame after that is "late I/O"
        self._late_io = False

        @self._pc.on("track")
        def _on_track(track):  # noqa: ANN001
            if track.kind != "audio":
                return

            async def _drain():
                try:
                    await track.recv()          # first inbound frame = first playable output
                    self._first_output.set()
                    while True:
                        await track.recv()       # keep draining so the leg stays alive
                        if self._watch_late:     # a frame after revoke = late media I/O
                            self._late_io = True
                except Exception:
                    return

            asyncio.ensure_future(_drain())

        @self._pc.on("connectionstatechange")
        async def _on_state():
            if self._pc.connectionState in ("failed", "closed", "disconnected"):
                self._terminal.set()

    async def create_offer(self, fixture_track) -> str:
        """Attach the fixture track, create the offer, wait ICE gather, return offer SDP."""
        import asyncio

        from aiortc import RTCSessionDescription  # noqa: F401  (kept explicit for parity)

        self._pc.addTrack(fixture_track)
        offer = await self._pc.createOffer()
        await self._pc.setLocalDescription(offer)
        # Non-trickle: the full SDP (with candidates) is POSTed, so wait for gathering.
        while self._pc.iceGatheringState != "complete":
            await asyncio.sleep(0.02)
        return self._pc.localDescription.sdp

    async def apply_answer(self, answer_sdp: str, *, authorized: bool) -> None:
        from aiortc import RTCSessionDescription

        if not authorized:
            raise MediaGateError("refusing to apply answer before media authorization")
        if not answer_sdp:
            raise MediaGateError("no answer sdp")
        await self._pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
        self._answer_applied = True

    async def wait_first_output(self, timeout_s: float) -> bool:
        import asyncio

        try:
            await asyncio.wait_for(self._first_output.wait(), timeout=timeout_s)
            return True
        except Exception:
            return False

    def arm_terminal(self) -> None:
        """Reset terminal watching so a transient earlier ICE blip cannot pre-latch it.

        Called at revocation, so ``wait_terminal`` only reports a transition observed AFTER
        the hangup was requested — never a stale terminal state from during the handshake.
        """
        import asyncio

        if not self._terminal.is_set():
            return
        # Recreate the event; the connectionstatechange handler resolves self._terminal
        # dynamically, so a fresh event only fires on the NEXT terminal transition.
        self._terminal = asyncio.Event()

    def arm_no_late_io(self) -> None:
        """Start watching for late media I/O: any inbound frame after this point is 'late'.

        Called at revoke, immediately before the client-side stop (``close``), so
        ``late_io_observed`` proves whether media kept flowing after the client stopped
        (F0-D-NO_LATE_IO under client-enforced revocation).
        """
        self._late_io = False
        self._watch_late = True

    @property
    def late_io_observed(self) -> bool:
        return self._late_io

    async def wait_terminal(self, timeout_s: float) -> bool:
        import asyncio

        try:
            await asyncio.wait_for(self._terminal.wait(), timeout=timeout_s)
            return True
        except Exception:
            return False

    @property
    def answer_applied(self) -> bool:
        return self._answer_applied

    async def close(self) -> None:
        try:
            await self._pc.close()
        except Exception:
            pass


def fixture_audio_track(pcm16: bytes, sample_rate_hz: int = 24_000):  # pragma: no cover - live path
    """A ``MediaStreamTrack`` that plays the deterministic PCM16 fixture, then silence.

    Frames are 20 ms of s16 mono at ``sample_rate_hz``; aiortc resamples/encodes to Opus.
    After the fixture is exhausted the track yields silence so the leg stays open long
    enough to observe the model's response (feeding the first-playable metric).
    """
    import asyncio
    import fractions

    import av
    from aiortc import MediaStreamTrack

    class _FixtureTrack(MediaStreamTrack):
        kind = "audio"

        def __init__(self) -> None:
            super().__init__()
            self._samples_per_frame = sample_rate_hz // 50  # 20 ms
            self._bytes_per_frame = self._samples_per_frame * 2
            self._pcm = pcm16
            self._pos = 0
            self._pts = 0

        async def recv(self):
            frame_bytes = self._pcm[self._pos:self._pos + self._bytes_per_frame]
            self._pos += self._bytes_per_frame
            if len(frame_bytes) < self._bytes_per_frame:
                frame_bytes = frame_bytes + b"\x00" * (self._bytes_per_frame - len(frame_bytes))
            frame = av.AudioFrame(format="s16", layout="mono", samples=self._samples_per_frame)
            frame.planes[0].update(frame_bytes)
            frame.sample_rate = sample_rate_hz
            frame.pts = self._pts
            frame.time_base = fractions.Fraction(1, sample_rate_hz)
            self._pts += self._samples_per_frame
            await asyncio.sleep(0.02)  # pace at real time (20 ms)
            return frame

    return _FixtureTrack()
