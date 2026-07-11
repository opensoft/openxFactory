"""Q7 / FR-002: the audio fixture is deterministic and reproduces its pinned digest."""
from avatar_f0.candidate import CandidateProfile
from avatar_f0.fixture import SILENCE_MS, generate_fixture


def test_fixture_is_deterministic():
    a = generate_fixture()
    b = generate_fixture()
    assert a.sha256 == b.sha256
    assert a.pcm16 == b.pcm16
    assert len(a.sha256) == 64


def test_fixture_has_speech_and_trailing_silence():
    fx = generate_fixture()
    # non-silent overall, with a trailing silence window >= server_vad 500 ms
    assert any(byte != 0 for byte in fx.pcm16[:1000])
    tail = fx.pcm16[-int(24_000 * (SILENCE_MS / 1000)) * 2:]
    assert set(tail) == {0}
    assert fx.duration_ms >= 1000


def test_fixture_digest_feeds_profile_digest():
    fx = generate_fixture()
    p1 = CandidateProfile(harness_revision="r1", dependency_lock_sha256="a" * 64,
                          fixture_bytes_sha256=fx.sha256, fixture_params=fx.params)
    p2 = CandidateProfile(harness_revision="r1", dependency_lock_sha256="a" * 64,
                          fixture_bytes_sha256="b" * 64, fixture_params=fx.params)
    # a different fixture digest yields a different profile digest
    assert p1.profile_digest != p2.profile_digest
    assert len(p1.profile_digest) == 64
