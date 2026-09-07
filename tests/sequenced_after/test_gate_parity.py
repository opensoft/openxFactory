"""THE TWO ARCHIVE FREEZE GATES, PINNED TO EACH OTHER (issue #749).

`scripts/validate-sequenced-after.py --archive-gate` and
`scripts/validate-scope-globs.py --archive-gate` are two realizations of ONE
gate shape: given a change directory and the ratified ref, locate the
ratified-side `proposal.md` BY CHANGE ID at that ref, read the current side
from the working tree, and report a post-ratification mutation of a frozen
front-matter field. They read the SAME corpus over the SAME trees, and an
operator archiving a change runs BOTH. When they disagree about which inputs
they can even be RUN on, the operator learns the difference the hard way — one
gate hands back a finding and the other a stack trace, on the same directory.

That is not hypothetical: it is the history. #705 was the scope-globs gate
crashing on an archived directory; #723 fixed it and grew four refusal arms
there; #734 mirrored ONE of them back (a missing working-tree proposal); #749 —
this change — mirrored the other three. Each round was a divergence discovered
by running one gate and not the other.

SO THE PARITY IS ASSERTED, NOT NARRATED. Every arm below builds ONE git
fixture whose `proposal.md` carries BOTH frozen fields, runs BOTH CLIs over it,
and asserts they agree on the exit code — and, on every refusal arm, that both
name the refusal "CANNOT RUN" rather than tracing back. A future arm added to
one gate and not the other reds this file.

NEITHER MODULE IS IMPORTED HERE, deliberately: the two substrates are pinned
THROUGH THEIR CLIs, which is the surface the operator and the archival workflow
actually touch, and importing both into one process would let a shared helper
mask exactly the divergence this file exists to catch. (`scope_globs` does load
`sequenced_after` for the by-id resolution — that is one implementation of the
rename lookup on purpose, per #723 — but the refusal arms live in each gate's
own code, and only a run can tell whether both reach them.)
"""
from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SEQUENCED_AFTER_CLI = ROOT / "scripts" / "validate-sequenced-after.py"
SCOPE_GLOBS_CLI = ROOT / "scripts" / "validate-scope-globs.py"

#: Both gates, by the name used in failure output, so a mismatch says WHICH.
GATES = {
    "sequenced_after": SEQUENCED_AFTER_CLI,
    "scope_globs": SCOPE_GLOBS_CLI,
}

_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e",
}


def _front(sequenced_after: str, scope_globs_paths: str) -> str:
    """A proposal declaring BOTH frozen fields, so BOTH gates have something
    real to compare rather than trivially retaining absence on both sides."""
    return (
        "---\n"
        "code_surface: openxFactory\n"
        f"sequenced_after: {sequenced_after}\n"
        "scope_globs:\n"
        "  openxFactory:\n"
        f"{scope_globs_paths}"
        "---\n\n# Example\n"
    )


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True,
                          env={**os.environ, **_ENV})


def _init_repo(tmp_path: Path) -> tuple[Path, Path, str]:
    """A repo with one ratified change, returning (repo, change_dir, ratified_ref)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        _front("[add-parent]", "    - scripts/**\n"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "ratified")
    ratified_ref = _git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, change, ratified_ref


def _archive_move(repo: Path, change: Path, dated_name: str) -> Path:
    """The rename committed SEPARATELY, so the ratified ref and the current
    tree are two snapshots — the shape the real archival workflow produces."""
    archive = repo / "openspec" / "changes" / "archive" / dated_name
    archive.parent.mkdir(parents=True, exist_ok=True)
    _git(repo, "mv", str(change), str(archive))
    _git(repo, "commit", "-q", "-m", "archive")
    return archive


def _run(cli: Path, change_dir: str, ratified_ref: str,
         cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(cli), "--archive-gate", change_dir,
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True, cwd=None if cwd is None else str(cwd),
    )


# --- the arms ----------------------------------------------------------------
#
# Each builder returns (change_dir_argument, ratified_ref, cwd) for ONE fixture,
# and the parametrization carries the exit code BOTH gates must return on it.


def _arm_across_the_rename(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    archive = _archive_move(repo, change, "2026-09-01-add-example")
    return str(archive), ratified_ref, None


def _arm_relative_dot_inside_the_archived_dir(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    archive = _archive_move(repo, change, "2026-09-01-add-example")
    return ".", ratified_ref, archive


def _arm_relative_dated_name_inside_archive(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    archive = _archive_move(repo, change, "2026-09-01-add-example")
    return archive.name, ratified_ref, archive.parent


def _arm_a_real_mutation(tmp_path: Path):
    """BOTH fields mutated after ratification: the gates must agree on the
    MUTATION verdict too, not merely on their refusals — a parity file that
    only exercised refusals would pass with both gates permanently broken."""
    repo, change, ratified_ref = _init_repo(tmp_path)
    (change / "proposal.md").write_text(
        _front("[add-other]", "    - scripts/**\n    - openspec/**\n"),
        encoding="utf-8")
    return str(change), ratified_ref, None


def _arm_missing_working_tree_proposal(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    # The directory has to SURVIVE the deletion, so it carries a second file —
    # the shape a real change directory has (proposal.md beside tasks.md).
    (change / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "tasks")
    _git(repo, "rm", "-q", str(change / "proposal.md"))
    _git(repo, "commit", "-q", "-m", "drop")
    assert change.is_dir() and not (change / "proposal.md").exists()
    return str(change), ratified_ref, None


def _arm_unresolvable_ratified_ref(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    return str(change), "no-such-ref", None


def _arm_ratified_ref_naming_a_non_commit_object(tmp_path: Path):
    repo, change, ratified_ref = _init_repo(tmp_path)
    blob = _git(repo, "rev-parse",
                "HEAD:openspec/changes/add-example/proposal.md").stdout.strip()
    return str(change), blob, None


def _arm_change_dir_outside_any_work_tree(tmp_path: Path):
    """A real directory carrying a real proposal, in no repository at all —
    the mistyped-path shape, which used to die as a `CalledProcessError`."""
    repo, change, ratified_ref = _init_repo(tmp_path)
    outside = tmp_path / "outside" / "add-example"
    outside.mkdir(parents=True)
    (outside / "proposal.md").write_text(
        _front("[add-parent]", "    - scripts/**\n"), encoding="utf-8")
    assert subprocess.run(
        ["git", "-C", str(outside), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True).returncode != 0, (
            "the fixture must stand outside any work tree")
    return str(outside), ratified_ref, None


PASSING_ARMS = [
    ("across_the_rename", _arm_across_the_rename),
    ("relative_dot_inside_the_archived_dir", _arm_relative_dot_inside_the_archived_dir),
    ("relative_dated_name_inside_archive", _arm_relative_dated_name_inside_archive),
]

#: (arm, builder, THE PHRASE BOTH GATES MUST USE). The exit code alone is too
#: coarse to hold the parity: a gate that reaches exit 2 by the WRONG route —
#: reporting an unresolvable ref in the wording of a change absent at a good one,
#: which is precisely what this gate did before #749 — agrees on the number while
#: sending the operator to the wrong repair. Each arm therefore also pins the
#: shared phrase that names the fact.
REFUSING_ARMS = [
    ("missing_working_tree_proposal", _arm_missing_working_tree_proposal,
     "no proposal.md in the working tree"),
    ("unresolvable_ratified_ref", _arm_unresolvable_ratified_ref,
     "does not name a commit"),
    ("ratified_ref_naming_a_non_commit_object",
     _arm_ratified_ref_naming_a_non_commit_object,
     "does not name a commit"),
    ("change_dir_outside_any_work_tree", _arm_change_dir_outside_any_work_tree,
     "is not inside a git work tree"),
]


def _both(tmp_path: Path, builder) -> dict[str, subprocess.CompletedProcess]:
    """Run BOTH gates over ONE fixture built by `builder`.

    The fixture is built ONCE and handed to both CLIs — building it twice would
    let the two gates be measured against two different trees, which is exactly
    the confound this file exists to remove.
    """
    change_dir, ratified_ref, cwd = builder(tmp_path)
    return {name: _run(cli, change_dir, ratified_ref, cwd)
            for name, cli in GATES.items()}


@pytest.mark.parametrize("name,builder", PASSING_ARMS, ids=[n for n, _ in PASSING_ARMS])
def test_BOTH_GATES_PASS_the_same_runnable_inputs(name, builder, tmp_path):
    runs = _both(tmp_path, builder)
    for gate, result in runs.items():
        assert result.returncode == 0, (
            gate, name, result.returncode, result.stdout, result.stderr)
        assert "Traceback" not in result.stderr, (gate, name, result.stderr)
        assert "passed" in result.stdout, (gate, name, result.stdout)
    assert (runs["sequenced_after"].returncode
            == runs["scope_globs"].returncode == 0)


def test_BOTH_GATES_REPORT_THE_SAME_MUTATION_VERDICT(tmp_path):
    runs = _both(tmp_path, _arm_a_real_mutation)
    for gate, result in runs.items():
        assert result.returncode == 1, (
            gate, result.returncode, result.stdout, result.stderr)
        assert "FAILED (contested)" in result.stdout, (gate, result.stdout)
        assert "Traceback" not in result.stderr, (gate, result.stderr)


@pytest.mark.parametrize("name,builder,phrase", REFUSING_ARMS,
                         ids=[n for n, _, _ in REFUSING_ARMS])
def test_BOTH_GATES_REFUSE_THE_SAME_UNRUNNABLE_INPUTS_AS_CANNOT_RUN(
        name, builder, phrase, tmp_path):
    runs = _both(tmp_path, builder)
    for gate, result in runs.items():
        # EXIT 2, NOT 1: "the gate could not run" is a different fact from "the
        # gate ran and found a mutation", and the two want different repairs.
        assert result.returncode == 2, (
            gate, name, result.returncode, result.stdout, result.stderr)
        assert "CANNOT RUN" in result.stdout, (gate, name, result.stdout)
        # THE SAME FACT, NAMED THE SAME WAY — not merely the same exit code.
        assert phrase in result.stdout, (gate, name, phrase, result.stdout)
        assert "Traceback" not in result.stdout, (gate, name, result.stdout)
        assert "Traceback" not in result.stderr, (gate, name, result.stderr)
        # And never as the mutation the crashing or comparing readings mistook
        # these for.
        assert "contested" not in result.stdout, (gate, name, result.stdout)
    assert (runs["sequenced_after"].returncode
            == runs["scope_globs"].returncode == 2)


def test_the_two_gates_are_TWO_DISTINCT_CLIs_and_this_file_imports_NEITHER():
    # Guards the parity claim itself: if these ever became one script, or this
    # file started importing a module, the parity assertion above would stop
    # measuring two independent implementations.
    assert SEQUENCED_AFTER_CLI != SCOPE_GLOBS_CLI
    assert SEQUENCED_AFTER_CLI.is_file() and SCOPE_GLOBS_CLI.is_file()
    # Read from the FILE'S OWN IMPORT STATEMENTS, via the parse tree rather than
    # a substring scan: a scan of the source text matches this very assertion
    # and can only ever fail on itself.
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for forbidden in ("sequenced_after", "sequenced_after_substrate",
                      "scope_globs", "importlib"):
        assert forbidden not in imported, (forbidden, sorted(imported))
