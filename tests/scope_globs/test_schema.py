"""Feature `scope-globs-schema` (add-structured-scope-substrate tasks 2.1-2.3):
the `scope_globs` schema + front-matter parser.

Loaded as a hyphen-free importable module directly from `scripts/scope_globs.py`.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "scope_globs.py"


def _load():
    spec = importlib.util.spec_from_file_location("scope_globs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # dataclass field resolution needs this
    spec.loader.exec_module(module)
    return module


sg = _load()


def _proposal(front_matter: str) -> str:
    return f"---\n{front_matter}\n---\n\n# Proposal\n\nbody\n"


# --- front-matter reading ----------------------------------------------------


def test_reads_scope_globs_mapping_from_front_matter():
    text = _proposal(
        "code_surface: openxFactory\n"
        "scope_globs:\n"
        "  openxFactory:\n"
        "    - scripts/**\n"
        "    - openspec/specs/**\n"
    )
    scope = sg.read_scope_globs(text)
    assert scope == {"openxFactory": ["scripts/**", "openspec/specs/**"]}


def test_absent_field_reads_as_none():
    text = _proposal("code_surface: openxFactory\ntarget_release: implemented")
    assert sg.read_scope_globs(text) is None


def test_document_without_front_matter_reads_as_empty():
    assert sg.read_front_matter("# no front matter\n\nbody") == {}
    assert sg.read_scope_globs("# no front matter\n") is None


def test_reads_from_a_path(tmp_path):
    p = tmp_path / "proposal.md"
    p.write_text(_proposal("scope_globs:\n  Repo:\n    - a/**\n"), encoding="utf-8")
    assert sg.read_scope_globs(p) == {"Repo": ["a/**"]}


def test_malformed_front_matter_yaml_is_rejected():
    text = "---\nscope_globs:\n  - : :bad\n  nested: [unterminated\n---\nbody"
    with pytest.raises(sg.ScopeGlobsError):
        sg.read_front_matter(text)


# --- shape validation --------------------------------------------------------


def test_valid_map_validates_and_exposes_globs():
    scope = sg.validate_shape({"openxFactory": ["scripts/**", "openspec/**"]})
    assert scope.repositories() == ("openxFactory",)
    assert scope.globs_for("openxFactory") == ("scripts/**", "openspec/**")


def test_absent_repo_entry_returns_empty_tuple_not_all_paths():
    scope = sg.validate_shape({"openxFactory": ["scripts/**"]})
    # A repository with no entry is not provenance-eligible — never "all paths".
    assert scope.globs_for("codexFactory") == ()


def test_non_mapping_is_rejected():
    for bad in (["scripts/**"], "scripts/**", 7, None):
        with pytest.raises(sg.ScopeGlobsError):
            sg.validate_shape(bad)


def test_empty_map_is_rejected():
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_shape({})


def test_empty_list_is_rejected():
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_shape({"openxFactory": []})


def test_non_string_or_empty_repo_key_is_rejected():
    for bad_key in ("", 3):
        with pytest.raises(sg.ScopeGlobsError):
            sg.validate_shape({bad_key: ["a/**"]})


def test_non_string_or_empty_glob_value_is_rejected():
    for bad in ("", 3, None):
        with pytest.raises(sg.ScopeGlobsError):
            sg.validate_shape({"openxFactory": [bad]})


def test_duplicate_globs_are_rejected():
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_shape({"openxFactory": ["scripts/**", "scripts/**"]})
