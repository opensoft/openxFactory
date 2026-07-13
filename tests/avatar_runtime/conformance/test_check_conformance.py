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


def test_pin_missing_required_scenarios_flagged():
    # A realized pin MUST carry the content-addressed required-set (FR-034a).
    pin = {
        "released_kernel": {
            "tag": "t", "commit": "c", "file_digests": {"f": "d"},
            "interface_lock_digest": "i", "acceptance_map_digest": "a",
        },
        "conformance": {
            "provisional_adapter_disabled": True,
            "canonical_matches_provisional": True,
        },
    }
    assert any("required_scenarios" in p for p in cc.validate_realization_pin(pin))


# --- pin-authoritative acceptance sourcing (FR-034a; fail-closed cross-check) --- #
import yaml  # noqa: E402
from pathlib import Path  # noqa: E402

from conformance import acceptance_source as asrc  # noqa: E402


def _write_map(root: Path, rel: str, ids: list[str]) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump({"requirements": [{"scenarios": [{"id": i} for i in ids]}]}))


def _pin(root: Path, arr, acr, archived=False, arr_digest=None):
    return {
        "required_scenarios": {"arr": list(arr), "acr": list(acr)},
        "conformance": {
            "sources_archived": archived,
            "acceptance_source_digests": {
                "arr": arr_digest or asrc.content_digest(asrc.ARR_MAP, root),
                "acr": asrc.content_digest(asrc.ACR_RELEASED_MAP, root),
            },
        },
    }


def test_pinned_required_scenarios_union():
    assert asrc.pinned_required_scenarios({}) == set()
    pin = {"required_scenarios": {"arr": ["ARR-1"], "acr": ["ACR-1", "ACR-2"]}}
    assert asrc.pinned_required_scenarios(pin) == {"ARR-1", "ACR-1", "ACR-2"}


def test_verify_sources_clean_pass(tmp_path):
    _write_map(tmp_path, asrc.ARR_MAP, ["ARR-1", "ARR-2"])
    _write_map(tmp_path, asrc.ACR_RELEASED_MAP, ["ACR-1"])
    pin = _pin(tmp_path, ["ARR-1", "ARR-2"], ["ACR-1"])
    assert asrc.verify_sources_against_pin(pin, root=tmp_path) == []


def test_verify_sources_digest_drift_only(tmp_path):
    _write_map(tmp_path, asrc.ARR_MAP, ["ARR-1"])
    _write_map(tmp_path, asrc.ACR_RELEASED_MAP, ["ACR-1"])
    pin = _pin(tmp_path, ["ARR-1"], ["ACR-1"])
    # same scenario set, different bytes -> only the digest leg fires
    (tmp_path / asrc.ARR_MAP).write_text(
        (tmp_path / asrc.ARR_MAP).read_text() + "\n# noise\n")
    probs = asrc.verify_sources_against_pin(pin, root=tmp_path)
    assert any(p.startswith("arr") and "digest drift" in p for p in probs)
    assert not any("set drift" in p for p in probs)


def test_verify_sources_set_drift_only(tmp_path):
    _write_map(tmp_path, asrc.ARR_MAP, ["ARR-1"])
    _write_map(tmp_path, asrc.ACR_RELEASED_MAP, ["ACR-1", "ACR-2"])
    # digests match the live files, but the pinned ACR set omits ACR-2 -> set drift only
    pin = _pin(tmp_path, ["ARR-1"], ["ACR-1"])
    probs = asrc.verify_sources_against_pin(pin, root=tmp_path)
    assert any(p.startswith("acr") and "set drift" in p for p in probs)
    assert not any("digest drift" in p for p in probs)


def test_verify_sources_absent_map_fails_closed(tmp_path):
    # ARR map absent, pin records an arr digest, sources_archived not set -> drift.
    _write_map(tmp_path, asrc.ACR_RELEASED_MAP, ["ACR-1"])
    pin = _pin(tmp_path, ["ARR-1"], ["ACR-1"], arr_digest="sha256:deadbeef")
    probs = asrc.verify_sources_against_pin(pin, root=tmp_path)
    assert any(p.startswith("arr") and "absent" in p for p in probs)


def test_verify_sources_absent_map_archived_skips(tmp_path):
    # Deliberate archival: absent ARR is permitted; present ACR still verified.
    _write_map(tmp_path, asrc.ACR_RELEASED_MAP, ["ACR-1"])
    pin = _pin(tmp_path, ["ARR-1"], ["ACR-1"], archived=True, arr_digest="sha256:x")
    assert asrc.verify_sources_against_pin(pin, root=tmp_path) == []


def test_verify_sources_null_conformance_no_crash():
    # conformance present but null must not raise (controlled behavior, not a traceback).
    pin = {"required_scenarios": {"arr": ["X"], "acr": ["Y"]}, "conformance": None}
    out = asrc.verify_sources_against_pin(pin, root=Path("/nonexistent-root-xyz"))
    assert isinstance(out, list)
