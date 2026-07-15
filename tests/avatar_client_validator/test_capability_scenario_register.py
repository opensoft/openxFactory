"""Positive + fail-closed negative coverage for the capability-scenario register
check (task 3.2 / P10 of ``adopt-avatar-client-lab-candidates``, design D2) in
``scripts/validate-avatar-client.py::check_capability_scenario_register``.

The validator is a hyphenated script, so it is loaded by file path with
``importlib``. The check reads the module-level ``ROOT``, ``CAP_REGISTER``,
``CAP_SPEC_PROMOTED`` and ``CAP_SPEC_DELTA`` globals; each test monkeypatches those
to a tmp tree so the check runs over a synthetic register + a synthetic capability
spec (promoted and/or change-delta), without touching the real repository tree.

Required negative coverage (task 3.2): a renamed title, a dropped scenario, and a
reordered entry each fail; the baseline is green. Also exercises the promoted-vs-
change-delta source fallback (design D2's re-verify-at-promotion pin).
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


# Synthetic capability spec: 2 requirements / 3 scenarios in document order.
SPEC_REQS = [
    ("Req One", ["Scen A1", "Scen A2"]),
    ("Req Two", ["Scen B1"]),
]


def _spec_md(reqs=SPEC_REQS) -> str:
    lines = ["## ADDED Requirements", ""]
    for rt, scens in reqs:
        lines += [f"### Requirement: {rt}", "The requirement SHALL hold.", ""]
        for st in scens:
            lines += [f"#### Scenario: {st}", "- **WHEN** x", "- **THEN** y", ""]
    return "\n".join(lines) + "\n"


def _valid_register() -> dict:
    return {
        "schema_version": 1,
        "kind": "avatar-client-lab-capability-scenario-register",
        "change_id": "implement-avatar-client-lab",
        "capability": "avatar-client-lab",
        "expected_requirement_count": 2,
        "expected_scenario_count": 3,
        "requirements": [
            {"id": "ACL-001", "capability": "avatar-client-lab", "title": "Req One",
             "scenarios": [
                 {"id": "ACL-001-S01", "title": "Scen A1"},
                 {"id": "ACL-001-S02", "title": "Scen A2"},
             ]},
            {"id": "ACL-002", "capability": "avatar-client-lab", "title": "Req Two",
             "scenarios": [
                 {"id": "ACL-002-S01", "title": "Scen B1"},
             ]},
        ],
    }


@pytest.fixture
def tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A tmp repo tree with ROOT/CAP_REGISTER/CAP_SPEC_* repointed.

    Returns ``write(register_dict, *, promoted=None, delta=_spec_md())`` which
    persists the register and the requested spec source(s) and returns the tmp root.
    Pass ``delta=None`` / ``promoted=None`` to omit that source file.
    """
    lab = tmp_path / "contracts" / "avatar-client-lab"
    promoted = tmp_path / "openspec" / "specs" / "avatar-client-lab" / "spec.md"
    delta = (tmp_path / "openspec" / "changes" / "implement-avatar-client-lab"
             / "specs" / "avatar-client-lab" / "spec.md")
    lab.mkdir(parents=True)
    register = lab / "capability-scenario-register.yaml"
    monkeypatch.setattr(VALIDATOR, "ROOT", tmp_path)
    monkeypatch.setattr(VALIDATOR, "CAP_REGISTER", register)
    monkeypatch.setattr(VALIDATOR, "CAP_SPEC_PROMOTED", promoted)
    monkeypatch.setattr(VALIDATOR, "CAP_SPEC_DELTA", delta)

    _DEFAULT = object()

    def write(doc: dict, *, promoted_md=None, delta_md=_DEFAULT) -> Path:
        register.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        if delta_md is _DEFAULT:
            delta_md = _spec_md()
        if delta_md is not None:
            delta.parent.mkdir(parents=True, exist_ok=True)
            delta.write_text(delta_md, encoding="utf-8")
        if promoted_md is not None:
            promoted.parent.mkdir(parents=True, exist_ok=True)
            promoted.write_text(promoted_md, encoding="utf-8")
        return tmp_path

    return write


def _run(tree, doc, **kw):
    tree(doc, **kw)
    f = VALIDATOR.Findings()
    VALIDATOR.check_capability_scenario_register(f)
    return f


# --------------------------------------------------------------------------
# Guard + green baseline.
# --------------------------------------------------------------------------

def test_absent_register_is_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(VALIDATOR, "CAP_REGISTER", tmp_path / "nope.yaml")
    f = VALIDATOR.Findings()
    VALIDATOR.check_capability_scenario_register(f)
    assert f.errors == [], f.errors


def test_green_baseline(tree):
    f = _run(tree, _valid_register())
    assert f.errors == [], f.errors


# --------------------------------------------------------------------------
# Required negatives: renamed title, dropped scenario, reordered entry.
# --------------------------------------------------------------------------

def test_renamed_scenario_title_red(tree):
    doc = _valid_register()
    doc["requirements"][0]["scenarios"][0]["title"] = "Scen A1 BOGUS"
    assert "cap-register-parity" in _codes(_run(tree, doc))


def test_renamed_requirement_title_red(tree):
    doc = _valid_register()
    doc["requirements"][1]["title"] = "Req Two RENAMED"
    assert "cap-register-parity" in _codes(_run(tree, doc))


def test_dropped_scenario_red(tree):
    doc = _valid_register()
    # Drop the last scenario and align the count so ONLY the ordered parity fires.
    doc["requirements"][1]["scenarios"] = []
    doc["expected_scenario_count"] = 2
    codes = _codes(_run(tree, doc))
    assert "cap-register-parity" in codes, codes
    assert "cap-register-count" not in codes, codes


def test_reordered_scenario_red(tree):
    doc = _valid_register()
    # Same set, swapped order within ACL-001 -> ordered element-wise compare fails.
    scens = doc["requirements"][0]["scenarios"]
    scens[0], scens[1] = scens[1], scens[0]
    codes = _codes(_run(tree, doc))
    assert "cap-register-parity" in codes, codes
    assert "cap-register-count" not in codes, codes


def test_fabricated_scenario_red(tree):
    doc = _valid_register()
    doc["requirements"][1]["scenarios"].append({"id": "ACL-002-S02", "title": "Scen fabricated"})
    doc["expected_scenario_count"] = 4
    assert "cap-register-parity" in _codes(_run(tree, doc))


# --------------------------------------------------------------------------
# Metadata / count / id negatives.
# --------------------------------------------------------------------------

def test_bad_kind_red(tree):
    doc = _valid_register(); doc["kind"] = "something-else"
    assert "cap-register-meta" in _codes(_run(tree, doc))


def test_count_mismatch_red(tree):
    doc = _valid_register(); doc["expected_scenario_count"] = 99
    assert "cap-register-count" in _codes(_run(tree, doc))


def test_bad_scenario_id_red(tree):
    doc = _valid_register()
    doc["requirements"][0]["scenarios"][0]["id"] = "ACR-004-S01"  # wrong prefix/pattern
    assert "cap-register-id" in _codes(_run(tree, doc))


def test_duplicate_id_red(tree):
    doc = _valid_register()
    doc["requirements"][1]["scenarios"][0]["id"] = "ACL-001-S01"  # collides with the first
    assert "cap-register-dup" in _codes(_run(tree, doc))


# --------------------------------------------------------------------------
# Source path: promoted-over-delta fallback + fail-closed when neither exists.
# --------------------------------------------------------------------------

def test_source_missing_is_fail_closed(tree):
    # Neither promoted nor change-delta spec present -> cap-register-source.
    doc = _valid_register()
    assert "cap-register-source" in _codes(_run(tree, doc, delta_md=None))


def test_promoted_path_is_preferred_over_delta(tree):
    # The promoted spec (present) is authoritative; a diverging delta must NOT be used.
    doc = _valid_register()
    diverging_delta = _spec_md([("Req One", ["Scen A1", "Scen A2"]),
                                ("Req Two", ["Scen B1 WRONG"])])
    f = _run(tree, doc, promoted_md=_spec_md(), delta_md=diverging_delta)
    assert f.errors == [], f.errors  # matches promoted -> green despite the bad delta


def test_promoted_divergence_fails_even_if_delta_matches(tree):
    # Register matches the delta but the PROMOTED spec (which wins) diverged -> fail.
    doc = _valid_register()
    diverging_promoted = _spec_md([("Req One", ["Scen A1", "Scen A2"]),
                                   ("Req Two", ["Scen B1 PROMOTED-CHANGED"])])
    f = _run(tree, doc, promoted_md=diverging_promoted, delta_md=_spec_md())
    assert "cap-register-parity" in _codes(f), f.errors
