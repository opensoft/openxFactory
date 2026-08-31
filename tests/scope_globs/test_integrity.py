"""Feature `scope-globs-integrity` (add-structured-scope-substrate tasks 4.1-4.2):
the archive-gate scope-retention FREEZE and the trust-root floor doctrine record.
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
DOCTRINE = ROOT / "docs" / "scope-globs-trust-root-floor.md"


def _load():
    spec = importlib.util.spec_from_file_location("scope_globs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sg = _load()


# --- pure retention comparison (task 4.1) ------------------------------------


def test_unchanged_scope_is_retained():
    scope = {"openxFactory": ["scripts/**"]}
    assert sg.scope_retention_problem(scope, dict(scope)) is None


def test_both_absent_is_retained():
    assert sg.scope_retention_problem(None, None) is None


def test_repo_key_reorder_is_retained():
    a = {"openxFactory": ["scripts/**"], "codexFactory": ["a/**"]}
    b = {"codexFactory": ["a/**"], "openxFactory": ["scripts/**"]}
    assert sg.scope_retention_problem(a, b) is None


def test_widening_after_ratification_is_a_contested_mutation():
    ratified = {"openxFactory": ["scripts/**"]}
    widened = {"openxFactory": ["scripts/**", "openspec/**"]}
    problem = sg.scope_retention_problem(ratified, widened)
    assert problem is not None
    assert "contested" in problem


def test_adding_scope_after_ratification_is_a_mutation():
    assert sg.scope_retention_problem(None, {"R": ["a/**"]}) is not None


def test_removing_scope_after_ratification_is_a_mutation():
    assert sg.scope_retention_problem({"R": ["a/**"]}, None) is not None


def test_glob_reorder_is_a_mutation():
    assert sg.scope_retention_problem(
        {"R": ["a/**", "b/**"]}, {"R": ["b/**", "a/**"]}
    ) is not None


# --- archive gate over a real git snapshot (task 4.1) ------------------------


def _init_change(tmp_path: Path, scope_block: str) -> Path:
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        f"---\ncode_surface: openxFactory\n{scope_block}---\n\n# Example\n",
        encoding="utf-8",
    )
    env = {
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e",
    }
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified"],
                   check=True, env={**_os_environ(), **env})
    return change


def _os_environ():
    import os
    return dict(os.environ)


_SCOPE = "scope_globs:\n  openxFactory:\n    - scripts/**\n"


def test_archive_gate_passes_when_scope_unchanged(tmp_path):
    change = _init_change(tmp_path, _SCOPE)
    assert sg.scope_retention_at_archive(change, "HEAD") is None


def test_archive_gate_rejects_a_post_ratification_mutation(tmp_path):
    change = _init_change(tmp_path, _SCOPE)
    # Widen the working-tree scope after the ratified commit.
    (change / "proposal.md").write_text(
        "---\ncode_surface: openxFactory\n"
        "scope_globs:\n  openxFactory:\n    - scripts/**\n    - openspec/**\n"
        "---\n\n# Example\n",
        encoding="utf-8",
    )
    problem = sg.scope_retention_at_archive(change, "HEAD")
    assert problem is not None
    assert "contested" in problem


def test_archive_gate_cli_rejects_a_mutation(tmp_path):
    change = _init_change(tmp_path, _SCOPE)
    (change / "proposal.md").write_text(
        "---\ncode_surface: openxFactory\n"
        "scope_globs:\n  openxFactory:\n    - openspec/**\n---\n\n# Example\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", "HEAD"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "SCOPE-RETENTION" in result.stdout


# --- trust-root floor doctrine record (task 4.2) -----------------------------


def test_doctrine_doc_exists_and_carries_the_four_properties():
    assert DOCTRINE.is_file()
    text = DOCTRINE.read_text(encoding="utf-8")
    flat = " ".join(text.split())  # collapse line-wraps for phrase matching
    assert "Status: ratified" in text
    assert "Ratified by: add-structured-scope-substrate" in text
    # The four trust-root properties (CRITICAL #1 (iv)).
    for phrase in ("Base-read", "Ratification-covered", "Non-author-mutable",
                   "Frozen after ratification"):
        assert phrase in text, phrase
    # The never-clearable-floor-of-every-enrolled-repo statement.
    assert "never-clearable floor member of EVERY repository" in flat
    assert "no autonomous provenance merge SHALL write" in flat
    assert "floor always wins" in flat.lower()


def test_doctrine_doc_is_linked_in_the_readme_index():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/scope-globs-trust-root-floor.md" in readme
