"""SC-011 / FR-021: a run writes nothing outside the two owned locations."""
from pathlib import Path

import pytest

from avatar_f0.evidence import WritePathError, assert_write_allowed


def test_allows_the_two_owned_locations(tmp_path):
    root = tmp_path
    ok1 = root / "experiments/avatar-brokered-call/schemas/x.yaml"
    ok2 = root / "openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.json"
    assert_write_allowed(ok1, root)   # no raise
    assert_write_allowed(ok2, root)   # no raise


@pytest.mark.parametrize("rel", [
    "contracts/avatar-client/kernel.yaml",
    "openspec/changes/qualify-avatar-brokered-call-feasibility/supporting-docs/f0-results.schema.yaml",
    "openspec/changes/define-avatar-client-contract-kernel/supporting-docs/x.yaml",
    "xfactory/avatar_runtime/broker.py",
    "specs/002-avc-f0-feasibility/spec.md",
])
def test_rejects_everything_outside_owned_surface(tmp_path, rel):
    with pytest.raises(WritePathError):
        assert_write_allowed(tmp_path / rel, tmp_path)
