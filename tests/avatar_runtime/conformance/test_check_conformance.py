"""Conformance-checker self-tests (ARR-008-S01, FR-034) + realization-pin + variance.

These drive the pure checker with synthetic inputs so they need no nested pytest
collection. They assert the checker FAILS on each failure class and that the
realization-pin validation catches a bare tag (ARR-002-S03) and canonical-vs-
provisional divergence (ARR-008-S03).
"""

from __future__ import annotations

from conformance import check_conformance as cc

REQUIRED = {"ARR-001-S01", "ARR-001-S02"}
COLLECTED = {"tests/avatar_runtime/test_x.py::test_a"}


def _mapped(sid, node):
    return {"scenario_id": sid, "disposition": "mapped", "test_node_ids": [node]}


def test_fully_mapped_passes():
    entries = [
        _mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::test_a"),
        {"scenario_id": "ARR-001-S02", "disposition": "non_applicable", "rationale": "n/a"},
    ]
    f = cc.check(REQUIRED, entries, COLLECTED)
    assert sum(len(v) for v in f.values()) == 0


def test_missing_required_scenario_fails():
    entries = [_mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::test_a")]
    f = cc.check(REQUIRED, entries, COLLECTED)
    assert f["missing"] == ["ARR-001-S02"]


def test_duplicate_entry_fails():
    entries = [
        _mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::test_a"),
        _mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::test_a"),
        {"scenario_id": "ARR-001-S02", "disposition": "non_applicable", "rationale": "n/a"},
    ]
    f = cc.check(REQUIRED, entries, COLLECTED)
    assert "ARR-001-S01" in f["duplicate"]


def test_dangling_node_fails():
    entries = [
        _mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::does_not_exist"),
        {"scenario_id": "ARR-001-S02", "disposition": "non_applicable", "rationale": "n/a"},
    ]
    f = cc.check(REQUIRED, entries, COLLECTED)
    assert f["dangling"]


def test_skipped_required_fails():
    node = "tests/avatar_runtime/test_x.py::test_a"
    entries = [
        _mapped("ARR-001-S01", node),
        {"scenario_id": "ARR-001-S02", "disposition": "non_applicable", "rationale": "n/a"},
    ]
    f = cc.check(REQUIRED, entries, COLLECTED, skipped={node})
    assert f["skipped_required"]


def test_unknown_scenario_fails():
    entries = [
        _mapped("ARR-001-S01", "tests/avatar_runtime/test_x.py::test_a"),
        {"scenario_id": "ARR-001-S02", "disposition": "non_applicable", "rationale": "n/a"},
        _mapped("ARR-999-S99", "tests/avatar_runtime/test_x.py::test_a"),
    ]
    f = cc.check(REQUIRED, entries, COLLECTED)
    assert "ARR-999-S99" in f["unknown"]


def test_bare_tag_fails_realization():
    # A tag without the exact commit + digests fails (ARR-002-S03).
    pin = {
        "released_kernel": {"tag": "contract-v1.0"},
        "conformance": {
            "provisional_adapter_disabled": True,
            "canonical_matches_provisional": True,
        },
    }
    problems = cc.validate_realization_pin(pin)
    assert any("commit" in p for p in problems)


def test_canonical_vs_provisional_divergence_fails():
    pin = {
        "released_kernel": {
            "tag": "t", "commit": "c", "file_digests": {"f": "d"},
            "interface_lock_digest": "i", "acceptance_map_digest": "a",
        },
        "conformance": {
            "provisional_adapter_disabled": True,
            "canonical_matches_provisional": False,  # divergence
        },
    }
    problems = cc.validate_realization_pin(pin)
    assert any("diverged" in p for p in problems)


def test_kernel_variance_reopens_only_mapped():
    from provisional import reopened_for_variance

    assert reopened_for_variance(["ARR-004-S01", "ARR-005-S03"]) == {
        "ARR-004-S01",
        "ARR-005-S03",
    }
