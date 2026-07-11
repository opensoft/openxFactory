"""FR-018 / Q3: digest-verified acceptance-map gate; absent/mismatch → INCONCLUSIVE."""
import hashlib
from pathlib import Path

import pytest

from avatar_f0.acceptance_map import AcceptanceMapError, F0_RELEVANT_ACR, load_acceptance_map

REPO_ROOT = Path(__file__).resolve().parents[4]
MAP = REPO_ROOT / "openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml"


def test_loads_real_map_and_exposes_f0_relevant_acr_ids():
    ref = load_acceptance_map(str(MAP))
    assert ref.interface_baseline == "avatar-client-parallel-v1"
    assert len(ref.content_sha256) == 64
    assert set(ref.f0_relevant()) == set(F0_RELEVANT_ACR)
    assert "ACR-003" in ref.known_acr_ids


def test_matching_expected_digest_passes():
    digest = hashlib.sha256(MAP.read_bytes()).hexdigest()
    ref = load_acceptance_map(str(MAP), expected_sha256=digest)
    assert ref.content_sha256 == digest


def test_digest_mismatch_fails_closed():
    with pytest.raises(AcceptanceMapError) as exc:
        load_acceptance_map(str(MAP), expected_sha256="0" * 64)
    assert exc.value.reason == "acceptance_map_digest_mismatch"


def test_absent_map_fails_closed():
    with pytest.raises(AcceptanceMapError) as exc:
        load_acceptance_map(str(MAP.parent / "does-not-exist.yaml"))
    assert exc.value.reason == "acceptance_map_absent"


def test_no_placeholder_ids_are_ever_minted():
    ref = load_acceptance_map(str(MAP))
    assert all(a.startswith("ACR-") and "TBD" not in a for a in ref.known_acr_ids)
