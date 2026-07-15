"""Positive + fail-closed negative coverage for the avatar-state derivation-table
check (task 4.3 / P1 of ``adopt-avatar-client-lab-candidates``, design D3) in
``scripts/validate-avatar-client.py::check_avatar_state_derivation_table``.

The validator is a hyphenated script, so it is loaded by file path with
``importlib``. The check reads the module-level ``ROOT``, ``DERIV_TABLE_YAML`` and
``DERIV_SEEDS_DIR`` globals; each test monkeypatches those to a tmp tree so the check
runs over a synthetic table + synthetic deterministic seeds, without touching the real
repository tree.

Required negative coverage (task 4.3): a green baseline, a wrong output set, a missing
media state, a seed-resolution mismatch, a reachability-set drift, an
invariant-contradiction row, and malformed YAML.
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


def _codes(findings) -> list[str]:
    return [line.split("]")[0].split("[")[1] for line in findings.errors]


TEN = [
    "permission", "capture_authorized", "capture_pending", "capture_active",
    "listening", "speaking", "control_degraded", "control_lost",
    "governed_action_pending", "retention_active",
]
TERMINALS = ["denied", "revoked", "abandoned", "expired", "completed", "session_limit_reached"]


def _valid_table() -> dict:
    return {
        "schema_version": 1,
        "kind": "avatar-client-registry",
        "registry_id": "avatar-state-derivation-table",
        "registry_version": 1,
        "inputs": {"media_states": list(TEN)},
        "outputs": ["listening", "thinking", "speaking", "interrupted", "blocked", "handoff"],
        "precedence": [
            {"id": "R0", "output": "blocked"},
            {"id": "R1", "output": "blocked"},
            {"id": "R2", "output": "handoff"},
            {"id": "R3", "output": "listening"},
            {"id": "R4", "output": "interrupted"},
            {"id": "R5", "output": "per media_state_map"},
            {"id": "R6", "output": "blocked"},
        ],
        "media_state_map": {
            "speaking": "speaking",
            "governed_action_pending": "listening",
            "permission": "listening",
            "capture_pending": "listening",
            "capture_authorized": "listening",
            "capture_active": "listening",
            "listening": "listening",
            "retention_active": "listening",
            "control_degraded": "blocked",
            "control_lost": "blocked",
        },
        "reachability_named_combinations": [
            {"axis": "control_health", "value": "lost", "evidences_media_state": "control_lost"},
            {"axis": "control_health", "value": "degraded", "evidences_media_state": "control_degraded"},
            {"axis": "media_state", "note": "eight non-control media.states"},
            {"axis": "session_outcome", "values": list(TERMINALS)},
        ],
        "landed_seed_crosscheck": [
            {"seed": "seed-listening.yaml", "derived": "listening"},
        ],
    }


def _seed(media_state, control_state="healthy", session_outcome=None, workflow_projection="intake") -> dict:
    view_state = {"media_state": media_state, "control_state": control_state,
                  "workflow_projection": workflow_projection}
    snapshot: dict = {}
    if session_outcome is not None:
        snapshot["session_outcome"] = session_outcome
    return {"expected": {"view_state": view_state}, "canonical": {"snapshot": snapshot}}


def _green_seeds() -> dict:
    return {
        # In the crosscheck (declares `listening`); resolves via R5 map.
        "seed-listening.yaml": _seed("capture_authorized"),
        # Declares an avatar state directly via media_state ∈ the six.
        "seed-speaking.yaml": _seed("speaking"),
        # R1 control-loss => blocked; declares blocked.
        "seed-blocked.yaml": _seed("blocked", control_state="lost"),
        # R2 handoff signal => handoff; declares handoff.
        "seed-handoff.yaml": _seed("handoff", workflow_projection="handoff"),
        # R4 interruption => interrupted; declares interrupted.
        "seed-interrupted.yaml": _seed("interrupted"),
        # Does NOT declare an avatar state (media.state is a denominator member) — resolves to
        # listening under OQ-5, checked only for totality.
        "seed-gap.yaml": _seed("governed_action_pending", session_outcome="granted"),
        # R3 terminal => listening (does not declare an avatar state).
        "seed-terminal.yaml": _seed("idle", session_outcome="denied"),
    }


@pytest.fixture
def tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A tmp repo tree with ROOT / DERIV_TABLE_YAML / DERIV_SEEDS_DIR repointed.

    Returns ``write(table_dict, seed_map=..., raw=...)`` which persists the table (or a
    ``raw`` string for the malformed case) plus each seed, and returns the tmp root.
    """
    lab = tmp_path / "contracts" / "avatar-client-lab"
    seeds = tmp_path / "examples" / "avatar-first-ui" / "fixtures" / "deterministic"
    lab.mkdir(parents=True)
    seeds.mkdir(parents=True)
    table = lab / "avatar-state-derivation-table.yaml"
    monkeypatch.setattr(VALIDATOR, "ROOT", tmp_path)
    monkeypatch.setattr(VALIDATOR, "DERIV_TABLE_YAML", table)
    monkeypatch.setattr(VALIDATOR, "DERIV_SEEDS_DIR", seeds)

    _DEFAULT = object()

    def write(doc, seed_map=_DEFAULT, *, raw=None) -> Path:
        if raw is not None:
            table.write_text(raw, encoding="utf-8")
        else:
            table.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        if seed_map is _DEFAULT:
            seed_map = _green_seeds()
        for name, sd in (seed_map or {}).items():
            (seeds / name).write_text(yaml.safe_dump(sd, sort_keys=False), encoding="utf-8")
        return tmp_path

    return write


def _run(tree, doc, **kw):
    tree(doc, **kw)
    f = VALIDATOR.Findings()
    VALIDATOR.check_avatar_state_derivation_table(f)
    return f


# --------------------------------------------------------------------------
# Guard + green baseline.
# --------------------------------------------------------------------------

def test_absent_table_is_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(VALIDATOR, "DERIV_TABLE_YAML", tmp_path / "nope.yaml")
    f = VALIDATOR.Findings()
    VALIDATOR.check_avatar_state_derivation_table(f)
    assert f.errors == [], f.errors


def test_green_baseline(tree):
    f = _run(tree, _valid_table())
    assert f.errors == [], f.errors


# --------------------------------------------------------------------------
# Required negatives.
# --------------------------------------------------------------------------

def test_wrong_output_set_red(tree):
    doc = _valid_table()
    doc["outputs"] = ["listening", "thinking", "speaking", "interrupted", "blocked"]  # drop handoff
    assert "derivation-outputs" in _codes(_run(tree, doc))


def test_extra_output_red(tree):
    doc = _valid_table()
    doc["outputs"].append("ended")  # a seventh state (kernel vocabulary change) is illegal
    assert "derivation-outputs" in _codes(_run(tree, doc))


def test_missing_media_state_red(tree):
    doc = _valid_table()
    doc["inputs"]["media_states"] = [m for m in TEN if m != "retention_active"]  # nine, not ten
    assert "derivation-media-states" in _codes(_run(tree, doc))


def test_seed_resolution_mismatch_red(tree):
    doc = _valid_table()
    seeds = _green_seeds()
    # A seed that DECLARES `speaking` (media_state ∈ six) but whose control is lost, so the
    # precedence derives `blocked` (R1) — a genuine derivation mismatch.
    seeds["seed-mismatch.yaml"] = _seed("speaking", control_state="lost")
    codes = _codes(_run(tree, doc, seed_map=seeds))
    assert "derivation-seed" in codes, codes


def test_crosscheck_mismatch_red(tree):
    doc = _valid_table()
    # The crosscheck claims seed-listening derives `speaking`, but the precedence derives listening.
    doc["landed_seed_crosscheck"] = [{"seed": "seed-listening.yaml", "derived": "speaking"}]
    assert "derivation-seed" in _codes(_run(tree, doc))


def test_reachability_set_drift_red(tree):
    doc = _valid_table()
    doc["reachability_named_combinations"][3]["values"] = TERMINALS[:-1]  # drop one terminal
    assert "derivation-reachability" in _codes(_run(tree, doc))


def test_reachability_missing_control_combo_red(tree):
    doc = _valid_table()
    doc["reachability_named_combinations"] = doc["reachability_named_combinations"][1:]  # drop lost
    assert "derivation-reachability" in _codes(_run(tree, doc))


def test_invariant_contradiction_row_red(tree):
    doc = _valid_table()
    doc["media_state_map"]["control_lost"] = "speaking"  # control loss must map to blocked (INV-1)
    assert "derivation-invariant" in _codes(_run(tree, doc))


def test_invariant_contradiction_r1_output_red(tree):
    doc = _valid_table()
    for p in doc["precedence"]:
        if p["id"] == "R1":
            p["output"] = "speaking"  # R1 control-health trip must output blocked
    assert "derivation-invariant" in _codes(_run(tree, doc))


def test_malformed_yaml_red(tree):
    f = _run(tree, {}, raw="outputs: [listening, thinking\n  broken: :\n")
    assert "derivation-malformed" in _codes(f)


def test_non_mapping_top_level_red(tree):
    f = _run(tree, {}, raw="- just\n- a\n- list\n")
    assert "derivation-malformed" in _codes(f)


# --------------------------------------------------------------------------
# Metadata negatives.
# --------------------------------------------------------------------------

def test_bad_kind_red(tree):
    doc = _valid_table()
    doc["kind"] = "something-else"
    assert "derivation-meta" in _codes(_run(tree, doc))


def test_missing_schema_version_red(tree):
    doc = _valid_table()
    del doc["schema_version"]
    assert "derivation-meta" in _codes(_run(tree, doc))
