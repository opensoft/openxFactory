"""Immutable pinned candidate profile + digest (FR-002).

The profile is fixed by the registered protocol/result schema: model ``gpt-realtime-2.1``,
voice ``marin``, interaction mode ``provider_vad``, ``server_vad`` turn detection. The
digest covers harness revision, dependency-lock digest, model/voice/turn settings, timeout
settings, and the generated-audio fixture digest.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict

REQUESTED_MODEL = "gpt-realtime-2.1"
VOICE = "marin"
INTERACTION_MODE = "provider_vad"
TURN_DETECTION = {
    "type": "server_vad",
    "threshold": 0.5,
    "prefix_padding_ms": 300,
    "silence_duration_ms": 500,
    "create_response": True,
    "interrupt_response": True,
}
READINESS_DEFAULT_MS = 3000
READINESS_CEILING_MS = 5000
REVOCATION_BOUND_MS = 5000


@dataclass(frozen=True)
class CandidateProfile:
    harness_revision: str
    dependency_lock_sha256: str
    fixture_bytes_sha256: str
    fixture_params: Dict[str, object] = field(default_factory=dict)
    requested_model: str = REQUESTED_MODEL
    voice: str = VOICE
    interaction_mode: str = INTERACTION_MODE
    turn_detection: Dict[str, object] = field(default_factory=lambda: dict(TURN_DETECTION))
    readiness_default_ms: int = READINESS_DEFAULT_MS
    readiness_ceiling_ms: int = READINESS_CEILING_MS

    def digest_source(self) -> Dict[str, object]:
        return {
            "harness_revision": self.harness_revision,
            "dependency_lock_sha256": self.dependency_lock_sha256,
            "requested_model": self.requested_model,
            "voice": self.voice,
            "interaction_mode": self.interaction_mode,
            "turn_detection": self.turn_detection,
            "readiness_default_ms": self.readiness_default_ms,
            "readiness_ceiling_ms": self.readiness_ceiling_ms,
            "fixture_bytes_sha256": self.fixture_bytes_sha256,
            "fixture_params": self.fixture_params,
        }

    @property
    def profile_digest(self) -> str:
        canonical = json.dumps(self.digest_source(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def dependency_lock_digest(lock_text: str) -> str:
    """Deterministic digest of the pinned dependency lock content (FR-002)."""
    return hashlib.sha256(lock_text.encode("utf-8")).hexdigest()
