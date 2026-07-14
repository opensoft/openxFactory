"""Negative + positive coverage for the successor-register deferral discharge
extension of ``scripts/validate-avatar-client.py`` (task 4.4, locked decision 7
of ``implement-avatar-client-lab``).

The validator is a hyphenated script, so it is loaded by file path with
``importlib``. Its collection/discharge functions read the module-level ``AVC``
and ``ROOT`` globals; each test monkeypatches those to a tmp contract tree so the
check functions can be exercised over synthetic successor registers without
touching the real repository tree.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts" / "validate-avatar-client.py"


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_avatar_client", ENTRYPOINT)
    assert spec and spec.loader, f"cannot load validator at {ENTRYPOINT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


@pytest.fixture
def avc_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A tmp ``contracts/avatar-client/`` tree with ROOT/AVC repointed at it."""
    avc = tmp_path / "contracts" / "avatar-client"
    avc.mkdir(parents=True)
    monkeypatch.setattr(VALIDATOR, "ROOT", tmp_path)
    monkeypatch.setattr(VALIDATOR, "AVC", avc)
    return avc


def _write_successor(avc: Path, change: str, entries: list, *,
                     change_id: str | None = "__match__",
                     schema_version: int | None = 1,
                     kind: str | None = "avatar-client-evidence-register") -> Path:
    doc: dict = {}
    if schema_version is not None:
        doc["schema_version"] = schema_version
    if kind is not None:
        doc["kind"] = kind
    if change_id is not None:
        doc["change_id"] = change if change_id == "__match__" else change_id
    doc["entries"] = entries
    path = avc / f"evidence-register.{change}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


DEFERRED_S05 = {
    "scenario_id": "SCO-001-S05",
    "evidence_type": "deferred",
    "status": "deferred",
    "owner_change": "implement-avatar-client-lab",
    "fail_closed_default": "stays in the owning adapter",
}


def _codes(findings) -> list[str]:
    return [line.split("]")[0].split("[")[1] for line in findings.errors]


# --------------------------------------------------------------------------
# Collection: the successor file can never be silently ignored.
# --------------------------------------------------------------------------

def test_successor_file_is_collected(avc_tree: Path) -> None:
    path = _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ])
    collected = VALIDATOR.successor_register_files()
    assert path in collected, "successor register must be collected by the glob"
    # And it joins the digested semantic surface (SEMANTIC_GLOBS) — silent-ignore
    # is impossible: the file is both discharge-checked and content-addressed.
    assert path in VALIDATOR.semantic_files()
    assert "evidence-register.*.yaml" in VALIDATOR.SEMANTIC_GLOBS
    # The released register itself is never mistaken for a successor.
    assert not VALIDATOR._is_successor_register("evidence-register.yaml")
    assert VALIDATOR._is_successor_register("evidence-register.implement-avatar-client-lab.yaml")


# --------------------------------------------------------------------------
# Green baseline + accepted discharges.
# --------------------------------------------------------------------------

def test_green_baseline_no_successor(avc_tree: Path) -> None:
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert f.errors == [], f.errors


def test_valid_planned_discharge_accepted(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "evidence_id": "TEST-SCO-001-S05",
         "discharges_deferred": True, "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    # A planned discharge is DECLARED, not yet effective: the evidence_id need not
    # resolve in the fixtures index yet (empty set below).
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert f.errors == [], f.errors


def test_valid_evidenced_discharge_accepted(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "evidenced", "evidence_id": "TEST-SCO-001-S05",
         "discharges_deferred": True, "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    # An EFFECTIVE (evidenced) discharge must name an evidence_id present in the
    # fixtures index.
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], {"TEST-SCO-001-S05"})
    assert f.errors == [], f.errors


def test_evidenced_discharge_unknown_evidence_id_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "evidenced", "evidence_id": "TEST-SCO-001-S05",
         "discharges_deferred": True, "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-evidence" in _codes(f), f.errors


# --------------------------------------------------------------------------
# Fail-closed negatives (task 4.4 required coverage).
# --------------------------------------------------------------------------

def test_mismatched_owner_change_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "some-other-change"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-owner-mismatch" in _codes(f), f.errors


def test_duplicate_discharge_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-dup" in _codes(f), f.errors


def test_nondischarging_entry_illegal(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-nondischarge" in _codes(f), f.errors


def test_change_id_filename_mismatch_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ], change_id="some-other-change")
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-change-id" in _codes(f), f.errors


def test_discharge_of_nondeferred_scenario_red(avc_tree: Path) -> None:
    released = {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
                "status": "evidenced", "evidence_id": "TEST-SCO-001-S05"}
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [released], set())
    assert "successor-target-not-deferred" in _codes(f), f.errors


def test_discharge_of_absent_scenario_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-999-S99", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ])
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-no-deferred" in _codes(f), f.errors


def test_missing_metadata_red(avc_tree: Path) -> None:
    _write_successor(avc_tree, "implement-avatar-client-lab", [
        {"scenario_id": "SCO-001-S05", "evidence_type": "automated",
         "status": "planned", "discharges_deferred": True,
         "owner_change": "implement-avatar-client-lab"},
    ], kind=None, schema_version=None)
    f = VALIDATOR.Findings()
    VALIDATOR.check_successor_discharge(f, [DEFERRED_S05], set())
    assert "successor-meta" in _codes(f), f.errors


# --------------------------------------------------------------------------
# The in-place deferred->evidenced flip stays illegal on the released register.
# --------------------------------------------------------------------------

def test_inplace_flip_still_illegal() -> None:
    # `deferred` is terminal in the transition graph: it can never reach
    # `evidenced`. That is what makes an in-place discharge (flipping a released
    # deferred entry to evidenced) illegal — the discharge must go to a successor.
    legal = VALIDATOR._legal_statuses_for("deferred")
    assert legal == {"planned", "deferred"}, legal
    assert "evidenced" not in legal
    assert VALIDATOR.EVID_STATUS_TRANSITIONS["deferred"] == set()
