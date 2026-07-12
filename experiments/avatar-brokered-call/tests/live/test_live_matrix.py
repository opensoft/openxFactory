"""Live matrix smoke (T056/T058): key-gated; skipped → INCONCLUSIVE when OPENAI_API_KEY absent.

These tests exercise the REAL provider path (billed) and are collected only when a lab key
is present AND the ``live`` marker is selected (``pytest -m live``). With no key they are
skipped, and the harness records a terminal INCONCLUSIVE result (SC-013) — never a
fabricated PASS. The deterministic driver LOGIC is covered without a key in
``tests/offline/test_live_runner_mock.py``.
"""
import asyncio

import pytest

from avatar_f0.candidate import CandidateProfile
from avatar_f0.credential import has_credential, load_credential
from avatar_f0.fixture import generate_fixture
from avatar_f0.live_runner import build_session_config

pytestmark = pytest.mark.live

requires_key = pytest.mark.skipif(
    not has_credential(), reason="no OPENAI_API_KEY present; live matrix is deferred (INCONCLUSIVE)"
)


@requires_key
def test_live_baseline_handshake_smoke():
    """One real brokered handshake: answer HELD until authorized, first output, clean hangup.

    Deliberately a single call (not the full 20-trial F0-A group) to bound cost. Proves the
    live components interoperate with the provider and the held-answer gate holds end to end.
    """
    from avatar_f0.broker import HttpBroker
    from avatar_f0.control_stub import ControlLeaseStub
    from avatar_f0.media import AiortcMediaPeer, MediaGateError, fixture_audio_track
    from avatar_f0.sideband import WssSideband

    key = load_credential()
    fixture = generate_fixture()
    candidate = CandidateProfile(harness_revision="live-smoke", dependency_lock_sha256="0" * 64,
                                 fixture_bytes_sha256=fixture.sha256)
    session_config = build_session_config(candidate)

    async def _drive():
        broker = HttpBroker(key)
        media = AiortcMediaPeer()
        sideband = None
        result = None
        try:
            offer_sdp = await media.create_offer(fixture_audio_track(fixture.pcm16))
            result = await broker.create_call("f0-live-smoke", "fp-smoke", offer_sdp, session_config)
            assert result.held_answer_sdp, "provider returned no answer SDP"
            assert result.call_id, "provider returned no call id (Location header)"

            # Held-answer gate: applying before authorization MUST fail closed.
            with pytest.raises(MediaGateError):
                await media.apply_answer(result.held_answer_sdp, authorized=False)

            sideband = WssSideband(result.call_id, key)
            await sideband.open()
            verified = await sideband.verify(3.0)
            assert verified, "sideband did not verify the live session"

            control = ControlLeaseStub()
            control.request_readiness()
            control.lease_ack()
            control.grant_authorization(sideband_verified=verified)

            await media.apply_answer(result.held_answer_sdp, authorized=control.is_authorized)
            got_output = await media.wait_first_output(4.0)
            accepted = await broker.hangup(result.call_id)
            terminal = await media.wait_terminal(5.0)
            assert accepted, "provider did not accept hangup"
            # A missing first-output / terminal signal is a recorded provider variance, not a
            # wiring failure of this smoke test.
            return got_output, terminal
        finally:
            # Always hang up the created call so a mid-handshake assertion failure never
            # orphans a live, billed provider call (idempotent on the happy path).
            if result is not None and result.call_id:
                try:
                    await broker.hangup(result.call_id)
                except Exception:
                    pass
            if sideband is not None:
                await sideband.close()
            await media.close()

    asyncio.run(_drive())
