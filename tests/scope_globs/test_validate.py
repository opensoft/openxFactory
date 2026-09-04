"""Feature `scope-globs-validate` (add-structured-scope-substrate tasks 3.1-3.4):
dialect conformance + cross-consistency, wired into a house validator that the
pytest gate runs over the live corpus.

`openspec validate` (the external CLI) cannot be extended, so the house wiring is
`scripts/validate-scope-globs.py` plus `test_corpus_scope_globs_all_validate`
below, which runs it over every active change on every PR — the same enforcement
route the other `scripts/validate-*.py` contract validators use.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "scope_globs.py"
VALIDATOR = ROOT / "scripts" / "validate-scope-globs.py"


def _load():
    spec = importlib.util.spec_from_file_location("scope_globs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sg = _load()


# --- dialect conformance -----------------------------------------------------


def test_conformant_scope_validates():
    sg.validate_scope_globs(
        {"openxFactory": ["scripts/**", "openspec/specs/**", "docs/a?.md"]},
        code_surface_repos={"openxFactory"},
    )


@pytest.mark.parametrize("bad", ["**", "*", "**/*", "/**", "./**"])
def test_universal_patterns_are_rejected(bad):
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["scripts/**", bad]}, code_surface_repos={"R"})
    assert bad in str(exc.value)


def test_leading_slash_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["/scripts/**"]}, code_surface_repos={"R"})
    assert "/scripts/**" in str(exc.value)


def test_negation_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["!scripts/**"]}, code_surface_repos={"R"})
    assert "!scripts/**" in str(exc.value)


def test_complement_denylist_key_is_rejected():
    for key in ("path_denylist", "except_paths", "codeowners_complement"):
        with pytest.raises(sg.ScopeGlobsError) as exc:
            sg.validate_scope_globs({key: ["scripts/**"]}, code_surface_repos={key})
        assert key in str(exc.value)


# --- cross-consistency with code_surface -------------------------------------


def test_scope_repo_absent_from_code_surface_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs(
            {"codexFactory": ["scripts/**"]}, code_surface_repos={"openxFactory"}
        )
    assert "codexFactory" in str(exc.value)


def test_code_surface_repo_without_scope_is_fine():
    # code_surface may name a repo scope_globs omits; that repo is simply not
    # provenance-eligible. Not an error.
    sg.validate_scope_globs(
        {"openxFactory": ["scripts/**"]},
        code_surface_repos={"openxFactory", "codexFactory"},
    )


# --- floor-agnostic ----------------------------------------------------------


def test_validator_is_floor_agnostic_a_floor_named_glob_passes():
    # `.github/**` and `openspec/changes/**` are typical never-clearable floor
    # members; the neutral validator MUST still accept them (the floor override
    # is a check-time concern of the downstream verifier, never a validate error).
    sg.validate_scope_globs(
        {"R": [".github/**", "openspec/changes/**"]}, code_surface_repos={"R"}
    )


# --- house wiring: the validator runs green over the live corpus --------------


def test_corpus_scope_globs_all_validate():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_flags_a_malformed_change(tmp_path):
    change = tmp_path / "openspec" / "changes" / "bad-change"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        "---\ncode_surface: R\nscope_globs:\n  R:\n    - '**'\n---\n\n# bad\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "bad-change" in result.stdout
    assert "**" in result.stdout
