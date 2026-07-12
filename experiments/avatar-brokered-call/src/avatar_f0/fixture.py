"""Deterministic synthetic audio fixture (FR-002 / Clarifications Q7).

Generates ONE deterministic synthetic speech-plus-silence clip per harness revision:
a voiced (formant-like) segment followed by trailing silence long enough to exceed the
pinned ``server_vad`` 500 ms silence window and close the turn. Determinism is by pure
math (no RNG); regenerating with the same parameters reproduces the same bytes, so the
generated-byte digest can be pinned in run metadata. No binary audio is ever committed,
and no real-user recording is used.

Implementation note (analyze U2 / task T011): for a live run the voiced segment is
produced by a pinned offline TTS engine (engine + voice + version), whose identity is
folded into the candidate ``profile_digest``. The deterministic waveform below is the
harness's reproducible default and stand-in; swapping in a pinned TTS keeps the same
digest-pinning contract.
"""
from __future__ import annotations

import hashlib
import math
import struct
from dataclasses import dataclass, field
from typing import Dict

SAMPLE_RATE_HZ = 24_000  # OpenAI realtime PCM16 mono default
SPEECH_MS = 900          # voiced segment
SILENCE_MS = 800         # trailing silence > server_vad 500 ms window
FUNDAMENTAL_HZ = 130.0   # ~male speaking f0
FORMANTS_HZ = (700.0, 1220.0, 2600.0)  # formant-like partials


@dataclass(frozen=True)
class AudioFixture:
    pcm16: bytes
    sha256: str
    params: Dict[str, object] = field(default_factory=dict)

    @property
    def duration_ms(self) -> int:
        return int(round(1000 * (len(self.pcm16) // 2) / SAMPLE_RATE_HZ))


def _generator_params() -> Dict[str, object]:
    return {
        "kind": "deterministic_synthetic_waveform",
        "sample_rate_hz": SAMPLE_RATE_HZ,
        "speech_ms": SPEECH_MS,
        "silence_ms": SILENCE_MS,
        "fundamental_hz": FUNDAMENTAL_HZ,
        "formants_hz": list(FORMANTS_HZ),
        "encoding": "pcm16le_mono",
        # Live runs replace the voiced segment with a pinned TTS engine/voice/version
        # (recorded here and folded into the profile digest) — see module docstring.
        "tts_engine": None,
        "tts_voice": None,
        "tts_version": None,
    }


def generate_fixture() -> AudioFixture:
    """Deterministically generate the speech-plus-silence PCM16 fixture."""
    n_speech = int(SAMPLE_RATE_HZ * SPEECH_MS / 1000)
    n_silence = int(SAMPLE_RATE_HZ * SILENCE_MS / 1000)
    samples = bytearray()
    amp = 0.62  # peak amplitude fraction of full scale
    for i in range(n_speech):
        t = i / SAMPLE_RATE_HZ
        # Amplitude envelope: smooth attack/decay so the segment is clearly voiced.
        env = math.sin(math.pi * i / n_speech)  # 0..1..0
        # Glottal-like source: fundamental + formant partials, deterministic phases.
        val = 0.0
        val += 1.0 * math.sin(2 * math.pi * FUNDAMENTAL_HZ * t)
        for k, f in enumerate(FORMANTS_HZ, start=1):
            val += (0.6 / k) * math.sin(2 * math.pi * f * t)
        val = (val / (1.0 + sum(0.6 / k for k in range(1, len(FORMANTS_HZ) + 1)))) * env * amp
        s = int(max(-1.0, min(1.0, val)) * 32767)
        samples += struct.pack("<h", s)
    # Trailing silence closes the VAD turn.
    samples += b"\x00\x00" * n_silence
    pcm = bytes(samples)
    return AudioFixture(pcm16=pcm, sha256=hashlib.sha256(pcm).hexdigest(), params=_generator_params())
