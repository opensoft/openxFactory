"""Live matrix (T056/T058): key-gated; skipped → INCONCLUSIVE when OPENAI_API_KEY absent.

These tests exercise the real provider path and are collected only when a lab key is
present. With no key they are skipped, and the harness records a terminal INCONCLUSIVE
result (SC-013) — never a fabricated PASS.
"""
import os

import pytest

from avatar_f0.credential import has_credential

pytestmark = pytest.mark.live

requires_key = pytest.mark.skipif(
    not has_credential(), reason="no OPENAI_API_KEY present; live matrix is deferred (INCONCLUSIVE)"
)


@requires_key
def test_live_baseline_handshake():
    # Implemented during the lab run (T058): drive the real broker/sideband/media path
    # for F0-A and assert the ordering invariant against live provider behavior.
    pytest.skip("live provider execution is performed during the supervised lab run")
