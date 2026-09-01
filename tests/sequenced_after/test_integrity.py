"""Feature `sequenced-after-integrity` (add-sequenced-after-substrate tasks
5.1-5.2): the archive-gate PARENT-DECLARATION RETENTION freeze, and the assertion
that archival does not REWRITE a declaration.

The freeze realizes the FROZEN-AFTER-RATIFICATION property of the trust-root
integrity requirement: a ratified chain position is auditable and immutable, so a
change cannot silently re-parent itself — or PROMOTE ITSELF TO A ROOT — between
ratification and archive, which under any narrowing composition would be a
widening. Contested class: reversing it reverses a gate decision.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
VALIDATOR = ROOT / "scripts" / "validate-sequenced-after.py"


def _load():
    spec = importlib.util.spec_from_file_location("sequenced_after", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sa = _load()


# --- the pure retention comparison (task 5.1) --------------------------------


def test_an_unchanged_declaration_is_retained():
    assert sa.retention_problem(["add-parent"], ["add-parent"]) is None


def test_both_ABSENT_is_retained():
    assert sa.retention_problem(sa.ABSENT, sa.ABSENT) is None


def test_both_an_empty_root_claim_is_retained():
    assert sa.retention_problem([], []) is None


def test_PROMOTING_ONESELF_TO_A_ROOT_after_ratification_is_a_mutation():
    # The one the whole freeze exists for: absence -> `[]` and parent -> `[]` are
    # both a change from "no root claim" to "a root claim", which under a
    # narrowing composition is a WIDENING of what the change can authorize.
    assert sa.retention_problem(sa.ABSENT, []) is not None
    assert sa.retention_problem(["add-parent"], []) is not None


def test_ABSENCE_and_an_EMPTY_DECLARATION_are_not_interchangeable():
    assert sa.retention_problem(sa.ABSENT, []) is not None
    assert sa.retention_problem([], sa.ABSENT) is not None


def test_a_NULL_declaration_is_distinguishable_from_both():
    assert sa.retention_problem(None, []) is not None
    assert sa.retention_problem(None, sa.ABSENT) is not None
    assert sa.retention_problem(None, None) is None


def test_RE_PARENTING_after_ratification_is_a_contested_mutation():
    problem = sa.retention_problem(["add-parent"], ["add-other-parent"])
    assert problem is not None
    assert "contested" in problem
    assert "re-parent" in problem


def test_ADDING_a_parent_after_ratification_is_a_mutation():
    assert sa.retention_problem(["add-parent"],
                               ["add-parent", "add-second"]) is not None


def test_REMOVING_a_declaration_after_ratification_is_a_mutation():
    assert sa.retention_problem(["add-parent"], sa.ABSENT) is not None


def test_ENTRY_REORDER_is_a_mutation():
    # The frozen declaration is compared AS AUTHORED.
    assert sa.retention_problem(["a-parent", "b-parent"],
                               ["b-parent", "a-parent"]) is not None


def test_a_SELF_QUALIFIED_RESPELLING_is_NOT_a_mutation():
    # Normalization is part of the reference's MEANING, so re-spelling the same
    # reference is not a change to the chain — while a different reference is.
    assert sa.retention_problem(["add-parent"],
                               ["openxFactory:add-parent"]) is None
    assert sa.retention_problem(["add-parent"],
                               ["codexFactory:add-parent"]) is not None


def test_a_mutation_INTO_MALFORMED_shape_registers_rather_than_crashing():
    assert sa.retention_problem(["add-parent"], {"not": "a sequence"}) is not None
    assert sa.retention_problem(["add-parent"], "add-parent") is not None


# --- the archive gate over a real git snapshot (task 5.1) --------------------


_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e",
}


def _front(declaration: str | None) -> str:
    front = "code_surface: openxFactory"
    if declaration is not None:
        front += f"\nsequenced_after: {declaration}"
    return f"---\n{front}\n---\n\n# Example\n"


def _init_change(tmp_path: Path, declaration: str | None) -> Path:
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(_front(declaration), encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified"],
                   check=True, env={**os.environ, **_ENV})
    return change


def test_the_archive_gate_passes_when_the_declaration_is_unchanged(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    assert sa.retention_at_archive(change, "HEAD") is None


def test_the_archive_gate_passes_when_no_declaration_was_ever_made(tmp_path):
    change = _init_change(tmp_path, None)
    assert sa.retention_at_archive(change, "HEAD") is None


def test_the_archive_gate_rejects_a_post_ratification_re_parent(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    (change / "proposal.md").write_text(_front("[add-other]"), encoding="utf-8")
    problem = sa.retention_at_archive(change, "HEAD")
    assert problem is not None
    assert "contested" in problem


def test_the_archive_gate_rejects_a_post_ratification_ROOT_PROMOTION(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    (change / "proposal.md").write_text(_front("[]"), encoding="utf-8")
    assert sa.retention_at_archive(change, "HEAD") is not None


def test_the_archive_gate_rejects_a_declaration_ADDED_after_ratification(tmp_path):
    change = _init_change(tmp_path, None)
    (change / "proposal.md").write_text(_front("[]"), encoding="utf-8")
    assert sa.retention_at_archive(change, "HEAD") is not None


def test_the_archive_gate_CLI_rejects_a_mutation(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    (change / "proposal.md").write_text(_front("[add-other]"), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", "HEAD"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "PARENT-DECLARATION-RETENTION" in result.stdout


def test_the_archive_gate_CLI_passes_an_unchanged_declaration(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", "HEAD"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout


def test_the_archive_gate_CLI_requires_a_ratified_ref(tmp_path):
    change = _init_change(tmp_path, "[add-parent]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "--ratified-ref" in result.stderr


# --- ARCHIVAL DOES NOT REWRITE DECLARATIONS (task 5.2) ----------------------


def test_archiving_carries_the_entries_through_BYTE_UNCHANGED(tmp_path):
    """No date-prefixing, no re-pointing, no normalization on archival.

    The declaration's shape at ratification is the shape it still has years
    later — which is what makes a chain auditable after its root has archived.
    """
    change = _init_change(tmp_path, "[add-parent, codexFactory:add-foreign]")
    before = (change / "proposal.md").read_bytes()
    # The retention gate is a PRE-archive check: it runs while the change still
    # sits at its active path, and it passes.
    assert sa.retention_at_archive(change, "HEAD") is None
    # Now perform the archival move the gate guards.
    archive = tmp_path / "openspec" / "changes" / "archive" / "2026-09-01-add-example"
    archive.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(tmp_path), "mv", str(change), str(archive)],
                   check=True)
    after = (archive / "proposal.md").read_bytes()
    assert after == before, "archival rewrote the proposal bytes"
    declaration = sa.declaration_of(archive)
    assert declaration == ["add-parent", "codexFactory:add-foreign"], (
        "the entries were rewritten, re-pointed or normalized on archival")
    # And the archived hop resolves by its bare id, from the archived directory.
    assert sa.resolve(tmp_path, "add-example") == archive
