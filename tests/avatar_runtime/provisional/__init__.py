"""Test-only ``avatar-client-parallel-v1`` provisional adapter (FR-004, ARR-002).

This module lives ONLY under the test tree and MUST be unreachable from the
runtime package (`xfactory/avatar_runtime/`) — enforced by the boundary scanner.
It represents the provisional interface baseline and stable acceptance IDs so
implementation can proceed before the kernel releases; it writes/claims no
canonical contract. Final conformance disables it.

Kernel-variance handling (FR-006, ARR-002-S04): when the contract-kernel owner
accepts a baseline variance naming affected acceptance IDs, only the mapped
tests/adapters reopen — see :func:`reopened_for_variance`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

# Provisional baseline acceptance source (read-only, sibling-owned).
_BASELINE = (
    Path(__file__).resolve().parents[3]
    / "openspec/changes/define-avatar-client-contract-kernel"
    / "supporting-docs/avatar-client-acceptance-map.yaml"
)

ENABLED = False  # disabled at contract-v1.7 realization (final conformance uses the released map)


def baseline_acr_ids() -> set[str]:
    """Applicable ACR scenario ids from the provisional baseline (no canonical claim)."""
    doc = yaml.safe_load(_BASELINE.read_text())
    return {
        s["id"]
        for req in doc.get("requirements", [])
        for s in req.get("scenarios", [])
    }


def claims_canonical_contract() -> bool:
    """The provisional adapter never writes or claims a canonical contract."""
    return False


def reopened_for_variance(affected_ids: list[str]) -> set[str]:
    """Given accepted-variance acceptance IDs, return exactly the ids to reopen.

    Only the named ids reopen; no kernel or unrelated sibling file is edited.
    """
    return set(affected_ids)
