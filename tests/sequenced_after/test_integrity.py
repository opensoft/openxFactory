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

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
VALIDATOR = ROOT / "scripts" / "validate-sequenced-after.py"


def _load():
    # Loaded under a name that is NOT `sequenced_after`: THIS DIRECTORY is a
    # package by that name (see `__init__.py`), and registering the script module
    # under the package's own name would replace the package in `sys.modules` and
    # abort collection of every sibling test module.
    spec = importlib.util.spec_from_file_location("sequenced_after_substrate", MODULE)
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


# --- the archive gate ACROSS THE ARCHIVE RENAME (issue #633) -----------------
#
# `--ratified-ref` names a commit BEFORE the archive rename, so the ratified-
# side `proposal.md` sits at the change's ACTIVE path there even when
# CHANGE_DIR — the gate's other argument — now names the ARCHIVED path. The
# gate must locate the ratified-side proposal BY CHANGE ID against the ref's
# own tree, never by reusing CHANGE_DIR's current path, or it asks git for an
# object that never existed at that ref and dies with a traceback instead of
# a finding.


def _head(repo: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()


def _archive_move(repo: Path, change: Path, dated_name: str) -> Path:
    """Move `change` into `openspec/changes/archive/<dated_name>/` and commit
    the rename as a SEPARATE commit, so the ratified ref and the current
    (post-rename) commit are two distinct snapshots — the shape the real
    archival workflow produces."""
    archive = repo / "openspec" / "changes" / "archive" / dated_name
    archive.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(repo), "mv", str(change), str(archive)],
                   check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "archive"],
                   check=True, env={**os.environ, **_ENV})
    return archive


def test_the_archive_gate_PASSES_across_the_archive_rename(tmp_path):
    # (a) ratified at ref R with a declaration, then renamed into
    # archive/<date>-<id>/ in a LATER commit: the gate, given the ARCHIVED
    # directory and --ratified-ref R, still finds the ratified-side proposal
    # (at its ACTIVE path in R's tree) and passes.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    assert sa.retention_at_archive(archive, ratified_ref) is None

    # And the CLI reports the same pass, not a traceback.
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(archive),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Traceback" not in result.stderr, result.stderr
    assert "passed" in result.stdout, result.stdout


def test_the_archive_gate_FAILS_across_the_archive_rename_on_a_real_mutation(tmp_path):
    # (b) same shape, but the ARCHIVED proposal's declaration was altered
    # (here: dropped) after the rename: the gate still runs the comparison —
    # it does not merely stop crashing — and reports the existing retention
    # finding.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    (archive / "proposal.md").write_text(_front(None), encoding="utf-8")
    problem = sa.retention_at_archive(archive, ratified_ref)
    assert problem is not None
    assert "contested" in problem

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(archive),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "Traceback" not in result.stderr, result.stderr
    assert "PARENT-DECLARATION-RETENTION" in result.stdout


def test_the_archive_gate_CLI_reports_a_ref_with_NO_PROPOSAL_as_a_finding_not_a_traceback(tmp_path):
    # (c) the id has no proposal.md at the ratified ref at all (e.g. a wrong
    # or mismatched --ratified-ref): a NAMED finding and exit 2, never a
    # traceback.
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    other = repo / "openspec" / "changes" / "add-other"
    other.mkdir(parents=True)
    (other / "proposal.md").write_text(_front(None), encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified-other"],
                   check=True, env={**os.environ, **_ENV})
    ratified_ref = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    # "add-example" never existed at ratified_ref — created only afterward.
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(_front(None), encoding="utf-8")

    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, ratified_ref)
    assert "add-example" in str(excinfo.value)
    assert ratified_ref in str(excinfo.value)
    assert "openspec/changes/add-example/proposal.md" in str(excinfo.value)
    assert "openspec/changes/archive" in str(excinfo.value)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "add-example" in result.stdout, result.stdout
    assert "CANNOT RUN" in result.stdout, result.stdout


def test_the_archive_gate_resolves_a_ratified_ref_that_is_ITSELF_ALREADY_ARCHIVED(tmp_path):
    # Distinct from the fixtures above, which all have `ratified_ref` predate
    # the rename (so the ACTIVE-path lookup resolves it): here `ratified_ref`
    # is the archival commit itself, so the active path never existed there
    # and `proposal_path_at_ref` MUST resolve it via the archived-directory
    # enumeration (`_archive_dir_names_at_ref`) rather than the active-path
    # shortcut — the branch a reviewer flagged as possibly under-tested.
    change = _init_change(tmp_path, "[add-parent]")
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    ratified_ref = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    # Sanity: the active path is genuinely gone at this ref, so a pass here
    # can only come from the archived-directory branch.
    assert not sa._blob_exists_at_ref(
        tmp_path, ratified_ref, "openspec/changes/add-example/proposal.md")
    assert sa.retention_at_archive(archive, ratified_ref) is None


# --- a MISSING WORKING-TREE proposal is "cannot run" (parity with #723) ------
#
# The sibling gate `scope_globs.scope_retention_at_archive` refuses this case
# outright (#723, fixing #705); this gate used to read it as `ABSENT` and
# compare on, which is a verdict about a declaration it never read. The two
# archive gates read the same corpus over the same trees, so they answer this
# the same way: a named finding and exit 2.


def test_a_MISSING_WORKING_TREE_PROPOSAL_is_a_CANNOT_RUN_finding_not_a_verdict(tmp_path):
    # Reading an ABSENT current-side proposal as "no declaration made" made the
    # gate answer a question it had never asked. With a declaration ratified at
    # REF it reported a contested MUTATION — a removal nobody made; with nothing
    # ratified it reported RETAINED. Both are verdicts about a declaration the
    # gate never read, and `ABSENT` means "no declaration was made", never "the
    # proposal is missing".
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    # The directory has to SURVIVE the deletion, so it carries a second file —
    # the shape a real change directory has (proposal.md beside tasks.md).
    (change / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m", "tasks"],
                   check=True, env={**os.environ, **_ENV})
    subprocess.run(["git", "-C", str(tmp_path), "rm", "-q",
                    str(change / "proposal.md")], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m", "drop"],
                   check=True, env={**os.environ, **_ENV})
    assert change.is_dir() and not (change / "proposal.md").exists()

    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, ratified_ref)
    message = str(excinfo.value)
    assert "no proposal.md in the working tree" in message, message
    assert str(change) in message, message
    # THE MISSING FILE ITSELF, not merely its directory: the diagnostic's whole
    # job is to tell an operator which path the gate went looking for, and a
    # directory-only assertion would still pass if that half were dropped.
    assert str(change / "proposal.md") in message, message

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "CANNOT RUN" in result.stdout, result.stdout
    assert str(change) in result.stdout, result.stdout
    assert str(change / "proposal.md") in result.stdout, result.stdout
    # And NOT as the mutation the old reading mistook it for.
    assert "contested" not in result.stdout, result.stdout


# --- the gate's OWN refusals are findings, never tracebacks (issue #749) -----
#
# The three arms `scope_globs.scope_retention_at_archive` gained in #723 and
# this gate did not. #705 was an operator running the SIBLING gate on a real
# archived directory and being handed a stack trace; every OTHER way that same
# operator can hold THIS gate wrong — a cwd-relative CHANGE_DIR, a path outside
# any work tree, a ref that names nothing — must land as a NAMED finding too,
# and the cwd-relative shapes must simply WORK, since they are how a person
# standing in the directory actually types it. The two archive gates read the
# same corpus over the same trees, so they refuse the same inputs alike.


def test_the_archive_gate_RUNS_when_CHANGE_DIR_IS_DOT_from_inside_the_archived_dir(tmp_path):
    # `cd openspec/changes/archive/<date>-<id> && ... --archive-gate .` — the
    # change id is decided from the directory's own name and its PARENT's name,
    # so an UNRESOLVED '.' carries neither and the id would read as ''. The
    # directory is resolved before the id is read.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = _head(tmp_path)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")

    # Driven through the CLI, not in-process: `.` only means the archived
    # directory when the PROCESS stands in it, and the resolution under test is
    # exactly what turns that into an id.
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", ".",
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True, cwd=str(archive),
    )
    assert result.returncode == 0, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stderr, result.stderr
    assert "passed" in result.stdout, result.stdout


def test_the_archive_gate_RUNS_on_a_RELATIVE_dated_dir_name_from_inside_archive(tmp_path):
    # `cd openspec/changes/archive && ... --archive-gate <date>-<id>` — here the
    # relative path DOES carry the directory's own name but not its parent's,
    # so unresolved it reads as an id that still carries the date prefix.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = _head(tmp_path)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", archive.name,
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True, cwd=str(archive.parent),
    )
    assert result.returncode == 0, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stderr, result.stderr
    assert "passed" in result.stdout, result.stdout


def test_a_CHANGE_DIR_OUTSIDE_A_WORK_TREE_is_a_finding_not_a_CalledProcessError(tmp_path):
    # A mistyped CHANGE_DIR is the same class of operator error #705 filed. The
    # work-tree probe runs BEFORE any by-id resolution, so its failure has to be
    # converted in `_git_toplevel` or it escapes as a raw `CalledProcessError`.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = _head(tmp_path)
    missing = tmp_path / "no" / "such" / "add-example"

    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(missing, ratified_ref)
    assert "git work tree" in str(excinfo.value), str(excinfo.value)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(missing),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "CANNOT RUN" in result.stdout, result.stdout
    # The change dir the operator actually typed is named back to them.
    assert str(missing.parent.resolve()) in result.stdout, result.stdout
    # Untouched: the change itself is fine, so this must not read as a mutation.
    assert "contested" not in result.stdout, result.stdout
    assert change.is_dir()


# --- undocumented OS-level failures are ALSO "cannot run" (codeXfactory/codexFactory#333) -
#
# Neither `ValueError`/`OSError` from `Path.resolve()` nor `OSError` from
# `subprocess.run` itself (as opposed to a nonzero exit code it captures and
# reports as a finding already) was documented anywhere above as a reason this
# gate cannot run — yet both are real ways the process can fail before the
# gate ever gets to read a proposal: a broken/looping symlink, or an
# environment where `git` is not on PATH at all. Monkeypatched rather than
# fixture-driven, because there is no portable way to make a real filesystem
# or a real `git` binary fail this way on demand. Mirrors the sibling gate's
# hardening (`scope_globs.scope_retention_at_archive`).


def test_a_PATH_RESOLVE_FAILURE_is_a_finding_not_a_traceback(tmp_path, monkeypatch):
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = _head(tmp_path)

    def _boom(self, *a, **k):
        raise OSError("simulated: too many levels of symbolic links")

    monkeypatch.setattr(Path, "resolve", _boom)
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, ratified_ref)
    message = str(excinfo.value)
    assert "simulated: too many levels of symbolic links" in message, message
    assert str(change) in message, message


def test_a_GIT_TOPLEVEL_LAUNCH_FAILURE_is_a_finding_not_a_traceback(tmp_path, monkeypatch):
    # `subprocess.run` itself can fail before ever producing a
    # `CompletedProcess` (the realistic case: `git` missing from PATH raises
    # `FileNotFoundError`, an `OSError` subclass) — distinct from the
    # already-tested case of git running and reporting a non-zero exit.
    change = _init_change(tmp_path, "[add-parent]")
    ratified_ref = _head(tmp_path)

    def _boom(*a, **k):
        raise FileNotFoundError("simulated: git not found on PATH")

    monkeypatch.setattr(sa.subprocess, "run", _boom)
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, ratified_ref)
    assert "simulated: git not found on PATH" in str(excinfo.value)


def test_an_UNRESOLVABLE_RATIFIED_REF_is_named_as_such_not_as_an_absent_change(tmp_path):
    # The by-id probes swallow git's exit status, so without a commit check a
    # bad ref is reported in the wording of a change that is absent at a good
    # one — pointing the operator at the wrong thing entirely.
    change = _init_change(tmp_path, "[add-parent]")

    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, "no-such-ref")
    message = str(excinfo.value)
    assert "does not name a commit" in message, message
    assert "no-such-ref" in message, message
    assert "has no proposal.md" not in message, message

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", "no-such-ref"],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stderr, result.stderr
    assert "CANNOT RUN" in result.stdout, result.stdout
    assert "does not name a commit" in result.stdout, result.stdout


def test_a_ref_naming_a_NON_COMMIT_OBJECT_is_refused_as_an_unresolvable_ref(tmp_path):
    # A blob sha resolves as an object but is not a commit; `<sha>^{commit}`
    # fails, so it lands in the same named refusal rather than being reported
    # as "the change is not there".
    change = _init_change(tmp_path, "[add-parent]")
    blob = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse",
         "HEAD:openspec/changes/add-example/proposal.md"],
        capture_output=True, text=True, check=True).stdout.strip()

    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.retention_at_archive(change, blob)
    assert "does not name a commit" in str(excinfo.value), str(excinfo.value)


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
