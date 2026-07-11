"""Parallel work uses the provisional seam without claiming canon (ARR-002-S01, FR-004)."""

from __future__ import annotations

import provisional


def test_parallel_uses_provisional_without_canonical_contract():
    # Applicable ACR ids are readable from the provisional baseline...
    ids = provisional.baseline_acr_ids()
    assert ids and all(i.startswith(("ACR-", "RBG-", "SCO-")) for i in ids)
    # ...but nothing here writes or claims a canonical contract.
    assert provisional.claims_canonical_contract() is False


def test_variance_reopens_only_named_ids():
    assert provisional.reopened_for_variance(["ACR-003-S01"]) == {"ACR-003-S01"}
