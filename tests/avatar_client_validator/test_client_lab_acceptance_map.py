"""Positive + fail-closed negative coverage for the client-lab acceptance-map
check (task 4.2 of ``implement-avatar-client-lab``) in
``scripts/validate-avatar-client.py::check_client_lab_acceptance_map``.

The validator is a hyphenated script, so it is loaded by file path with
``importlib``. The check reads the module-level ``ROOT``, ``AVC``,
``CLIENT_LAB_MAP`` and ``AFU_ACCEPTANCE_MAP`` globals; each test monkeypatches
those to a tmp tree so the check can run over a synthetic client-lab map + the two
synthetic released acceptance maps it inherits from, without touching the real
repository tree.
"""

from __future__ import annotations

import copy
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

NINE_GATES = sorted(VALIDATOR.CLIENT_LAB_GATES)
ELEVEN_A11Y = sorted(VALIDATOR.CLIENT_LAB_A11Y)


def _codes(findings) -> list[str]:
    return [line.split("]")[0].split("[")[1] for line in findings.errors]


def _released_avc_map() -> dict:
    return {
        "schema_version": 1,
        "kind": "avatar-client-acceptance-map",
        "requirements": [
            {"id": "ACR-004", "title": "Single-log command, event, and snapshot authority",
             "owner_changes": ["implement-avatar-reference-runtime", "implement-avatar-client-lab"],
             "scenarios": [
                 {"id": "ACR-004-S01", "title": "Client submits a valid command"},
                 {"id": "ACR-004-S02", "title": "Command is retried"},
             ]},
            # A requirement that does NOT name the change — listing it is overclaiming.
            {"id": "ACR-002", "title": "Authenticated, purpose-bound session results",
             "owner_changes": ["implement-avatar-reference-runtime"],
             "scenarios": [{"id": "ACR-002-S01", "title": "Authorized session is granted"}]},
        ],
    }


def _released_afu_map() -> dict:
    return {
        "schema_version": 1,
        "requirements": [
            {"id": "AFU-008", "title": "Deterministic UI acceptance",
             "owner_changes": ["implement-avatar-client-lab"],
             "scenarios": [{"id": "AFU-008-S01", "title": "Offline acceptance is replayed"}]},
        ],
    }


def _valid_client_map() -> dict:
    return {
        "schema_version": 1,
        "kind": "avatar-client-lab-acceptance-map",
        "change_id": "implement-avatar-client-lab",
        "acceptance_foci": [{"id": x} for x in ("M0", "F1", "F2", "F3", "F4", "cross_cutting")],
        "gates": [{"id": g} for g in NINE_GATES],
        "accessibility_baseline": {"capabilities": list(ELEVEN_A11Y)},
        "expected_requirement_count": 2,
        "expected_scenario_count": 3,
        "inherited_scenarios": [
            {"requirement": "ACR-004", "source_map": "avatar-client",
             "title": "Single-log command, event, and snapshot authority", "focus": "F2",
             "scenarios": [
                 {"id": "ACR-004-S01", "title": "Client submits a valid command",
                  "client_evidence_class": "fixture", "gate": "replay_determinism"},
                 {"id": "ACR-004-S02", "title": "Command is retried",
                  "client_evidence_class": "fixture", "gate": "replay_determinism"},
             ]},
            {"requirement": "AFU-008", "source_map": "avatar-first-ui",
             "title": "Deterministic UI acceptance", "focus": "F4",
             "scenarios": [
                 {"id": "AFU-008-S01", "title": "Offline acceptance is replayed",
                  "client_evidence_class": "fixture", "gate": "replay_determinism"},
             ]},
        ],
    }


@pytest.fixture
def tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A tmp repo tree with ROOT/AVC/CLIENT_LAB_MAP/AFU_ACCEPTANCE_MAP repointed.

    Returns a writer ``write(client_map_dict)`` that persists the client-lab map
    and returns the tmp root so tests can drop extra files (fixtures, registers).
    """
    avc = tmp_path / "contracts" / "avatar-client"
    lab = tmp_path / "contracts" / "avatar-client-lab"
    afu = tmp_path / "examples" / "avatar-first-ui"
    for d in (avc, lab, afu):
        d.mkdir(parents=True)
    (avc / "acceptance-map.yaml").write_text(yaml.safe_dump(_released_avc_map()), encoding="utf-8")
    (afu / "avatar-first-ui-acceptance-map.yaml").write_text(
        yaml.safe_dump(_released_afu_map()), encoding="utf-8")
    client_map = lab / "client-acceptance-map.yaml"
    monkeypatch.setattr(VALIDATOR, "ROOT", tmp_path)
    monkeypatch.setattr(VALIDATOR, "AVC", avc)
    monkeypatch.setattr(VALIDATOR, "CLIENT_LAB_MAP", client_map)
    monkeypatch.setattr(VALIDATOR, "AFU_ACCEPTANCE_MAP", afu / "avatar-first-ui-acceptance-map.yaml")

    def write(doc: dict) -> Path:
        client_map.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return tmp_path

    return write


def _run(tree, doc):
    tree(doc)
    f = VALIDATOR.Findings()
    VALIDATOR.check_client_lab_acceptance_map(f)
    return f


# --------------------------------------------------------------------------
# Guard + green baseline.
# --------------------------------------------------------------------------

def test_absent_map_is_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(VALIDATOR, "CLIENT_LAB_MAP", tmp_path / "nope.yaml")
    f = VALIDATOR.Findings()
    VALIDATOR.check_client_lab_acceptance_map(f)
    assert f.errors == [], f.errors


def test_green_baseline(tree):
    f = _run(tree, _valid_client_map())
    assert f.errors == [], f.errors


# --------------------------------------------------------------------------
# Metadata / gating-frame negatives.
# --------------------------------------------------------------------------

def test_bad_kind_red(tree):
    doc = _valid_client_map(); doc["kind"] = "something-else"
    assert "client-lab-meta" in _codes(_run(tree, doc))


def test_bad_change_id_red(tree):
    doc = _valid_client_map(); doc["change_id"] = "other-change"
    assert "client-lab-meta" in _codes(_run(tree, doc))


def test_missing_gate_red(tree):
    doc = _valid_client_map(); doc["gates"] = doc["gates"][:-1]  # eight gates
    assert "client-lab-gates" in _codes(_run(tree, doc))


def test_missing_a11y_capability_red(tree):
    doc = _valid_client_map()
    doc["accessibility_baseline"]["capabilities"] = ELEVEN_A11Y[:-1]  # ten caps
    assert "client-lab-a11y" in _codes(_run(tree, doc))


def test_missing_focus_red(tree):
    doc = _valid_client_map()
    doc["acceptance_foci"] = [x for x in doc["acceptance_foci"] if x["id"] != "F3"]
    assert "client-lab-foci" in _codes(_run(tree, doc))


# --------------------------------------------------------------------------
# Parity / completeness / overclaim negatives.
# --------------------------------------------------------------------------

def test_renamed_scenario_title_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][0]["title"] = "Client submits a bogus command"
    assert "client-lab-parity" in _codes(_run(tree, doc))


def test_fabricated_scenario_id_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][0]["id"] = "ACR-004-S99"
    assert "client-lab-parity" in _codes(_run(tree, doc))


def test_overclaimed_requirement_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"].append(
        {"requirement": "ACR-002", "source_map": "avatar-client",
         "title": "Authenticated, purpose-bound session results", "focus": "F2",
         "scenarios": [{"id": "ACR-002-S01", "title": "Authorized session is granted",
                        "client_evidence_class": "fixture", "gate": "replay_determinism"}]})
    doc["expected_requirement_count"] = 3
    doc["expected_scenario_count"] = 4
    assert "client-lab-owner" in _codes(_run(tree, doc))


def test_dropped_inherited_requirement_red(tree):
    doc = _valid_client_map()
    # Drop AFU-008 (an owed requirement) and align counts so ONLY completeness fires.
    doc["inherited_scenarios"] = [b for b in doc["inherited_scenarios"]
                                  if b["requirement"] != "AFU-008"]
    doc["expected_requirement_count"] = 1
    doc["expected_scenario_count"] = 2
    codes = _codes(_run(tree, doc))
    assert "client-lab-incomplete" in codes, codes


def test_bad_evidence_class_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][0]["client_evidence_class"] = "schema_reproof"
    assert "client-lab-class" in _codes(_run(tree, doc))


def test_bad_gate_ref_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][0]["gate"] = "not_a_gate"
    assert "client-lab-gates" in _codes(_run(tree, doc))


def test_missing_fixture_path_red(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][0]["fixture"] = "examples/does/not/exist.yaml"
    assert "client-lab-fixture" in _codes(_run(tree, doc))


def test_count_mismatch_red(tree):
    doc = _valid_client_map(); doc["expected_scenario_count"] = 99
    assert "client-lab-count" in _codes(_run(tree, doc))


def test_duplicate_scenario_id_red(tree):
    doc = _valid_client_map()
    dup = copy.deepcopy(doc["inherited_scenarios"][0]["scenarios"][0])
    doc["inherited_scenarios"][0]["scenarios"].append(dup)
    doc["expected_scenario_count"] = 4
    assert "client-lab-dup" in _codes(_run(tree, doc))


# --------------------------------------------------------------------------
# discharge_via must be consistent with the successor register (decision 7).
# --------------------------------------------------------------------------

def test_discharge_via_inconsistent_red(tree):
    doc = _valid_client_map()
    # Point ACR-004-S02 at a successor register that does NOT discharge it.
    doc["inherited_scenarios"][0]["scenarios"][1]["client_evidence_class"] = "successor"
    doc["inherited_scenarios"][0]["scenarios"][1]["discharge_via"] = \
        "contracts/avatar-client/evidence-register.some-change.yaml"
    root = tree(doc)
    reg = root / "contracts" / "avatar-client" / "evidence-register.some-change.yaml"
    reg.write_text(yaml.safe_dump({
        "schema_version": 1, "kind": "avatar-client-evidence-register",
        "change_id": "some-change",
        "entries": [{"scenario_id": "SOMETHING-ELSE", "discharges_deferred": True}],
    }), encoding="utf-8")
    f = VALIDATOR.Findings()
    VALIDATOR.check_client_lab_acceptance_map(f)
    assert "client-lab-discharge" in _codes(f), f.errors


def test_discharge_via_consistent_ok(tree):
    doc = _valid_client_map()
    doc["inherited_scenarios"][0]["scenarios"][1]["client_evidence_class"] = "successor"
    doc["inherited_scenarios"][0]["scenarios"][1]["discharge_via"] = \
        "contracts/avatar-client/evidence-register.some-change.yaml"
    root = tree(doc)
    reg = root / "contracts" / "avatar-client" / "evidence-register.some-change.yaml"
    reg.write_text(yaml.safe_dump({
        "schema_version": 1, "kind": "avatar-client-evidence-register",
        "change_id": "some-change",
        "entries": [{"scenario_id": "ACR-004-S02", "discharges_deferred": True}],
    }), encoding="utf-8")
    f = VALIDATOR.Findings()
    VALIDATOR.check_client_lab_acceptance_map(f)
    assert f.errors == [], f.errors
