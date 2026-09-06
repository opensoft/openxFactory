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


_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e",
}


def _init_change(tmp_path: Path, scope_block: str) -> Path:
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        f"---\ncode_surface: openxFactory\n{scope_block}---\n\n# Example\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified"],
                   check=True, env={**_os_environ(), **_ENV})
    return change


def _head(repo: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()


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


# --- the archive gate ACROSS THE ARCHIVE RENAME (issue #705) -----------------
#
# `--ratified-ref` names a commit BEFORE the archive rename, so the ratified-
# side `proposal.md` sits at the change's ACTIVE path there even when
# CHANGE_DIR — the gate's other argument — now names the ARCHIVED path. The
# gate must locate the ratified-side proposal BY CHANGE ID against the ref's
# own tree, never by reusing CHANGE_DIR's current path, or it asks git for an
# object that never existed at that ref and dies with a CalledProcessError
# traceback instead of reporting a finding. The same defect was fixed for the
# sibling `sequenced_after` gate in #638 (issue #633); this gate reuses that
# fix's resolution rather than re-implementing it.


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
                   check=True, env={**_os_environ(), **_ENV})
    return archive


def test_the_archive_gate_PASSES_across_the_archive_rename(tmp_path):
    # (a) ratified at ref R with a scope, then renamed into
    # archive/<date>-<id>/ in a LATER commit: the gate, given the ARCHIVED
    # directory and --ratified-ref R, still finds the ratified-side proposal
    # (at its ACTIVE path in R's tree) and passes.
    change = _init_change(tmp_path, _SCOPE)
    ratified_ref = _head(tmp_path)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    assert sg.scope_retention_at_archive(archive, ratified_ref) is None

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
    # (b) same shape, but the ARCHIVED proposal's scope was widened after the
    # rename: the gate still runs the comparison — it does not merely stop
    # crashing — and reports the existing retention finding.
    change = _init_change(tmp_path, _SCOPE)
    ratified_ref = _head(tmp_path)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    (archive / "proposal.md").write_text(
        "---\ncode_surface: openxFactory\n"
        "scope_globs:\n  openxFactory:\n    - scripts/**\n    - openspec/**\n"
        "---\n\n# Example\n",
        encoding="utf-8",
    )
    problem = sg.scope_retention_at_archive(archive, ratified_ref)
    assert problem is not None
    assert "contested" in problem

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(archive),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 1, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stderr, result.stderr
    assert "SCOPE-RETENTION" in result.stdout, result.stdout
    assert "FAILED (contested)" in result.stdout, result.stdout


def test_the_archive_gate_CLI_reports_a_ref_with_NO_PROPOSAL_as_a_finding_not_a_traceback(tmp_path):
    # (c) the id has no proposal.md at the ratified ref at all (e.g. a wrong or
    # mismatched --ratified-ref): a NAMED finding and exit 2, never a traceback.
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    other = repo / "openspec" / "changes" / "add-other"
    other.mkdir(parents=True)
    (other / "proposal.md").write_text(
        f"---\ncode_surface: openxFactory\n{_SCOPE}---\n\n# Other\n",
        encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified-other"],
                   check=True, env={**_os_environ(), **_ENV})
    ratified_ref = _head(repo)
    # "add-example" never existed at ratified_ref — created only afterward.
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        f"---\ncode_surface: openxFactory\n{_SCOPE}---\n\n# Example\n",
        encoding="utf-8")

    with pytest.raises(sg.ScopeGlobsError) as excinfo:
        sg.scope_retention_at_archive(change, ratified_ref)
    # The named subclass, so a caller can tell "could not run" from "malformed"
    # while still catching the module's one error class.
    assert isinstance(excinfo.value, sg.ScopeGlobsResolutionError)
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
    # Distinct from (a) and (b), where `ratified_ref` predates the rename (so
    # the ACTIVE-path lookup resolves it): here `ratified_ref` IS the archival
    # commit, so the active path never existed there and the resolution must go
    # through the archived-directory enumeration.
    change = _init_change(tmp_path, _SCOPE)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")
    ratified_ref = _head(tmp_path)
    assert subprocess.run(
        ["git", "-C", str(tmp_path), "cat-file", "-e",
         f"{ratified_ref}:openspec/changes/add-example/proposal.md"],
        capture_output=True, text=True).returncode != 0
    assert sg.scope_retention_at_archive(archive, ratified_ref) is None


def test_the_sequenced_after_sibling_is_NOT_imported_at_module_import_time():
    # THE DEFERRAL IS LOAD-BEARING, so it is pinned rather than left to a
    # comment. `scripts/scope_globs.py` is vendored byte-for-byte into
    # codexFactory's merge gate alongside only `frontmatter_strict.py`; a
    # module-level `sequenced_after` import would leave that vendored copy
    # unimportable for a function the merge gate never calls. A future
    # refactor that hoists the import fails HERE, in this repository, rather
    # than in the consumer.
    probe = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('scope_globs', {str(MODULE)!r})\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "sys.modules['scope_globs'] = module\n"
        "spec.loader.exec_module(module)\n"
        "print('sequenced_after_substrate' in sys.modules or "
        "'sequenced_after' in sys.modules)\n"
    )
    result = subprocess.run([sys.executable, "-c", probe],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "False", result.stdout


# --- the gate's OWN refusals are findings, never tracebacks ------------------
#
# #705 was an operator running the gate on a real archived directory and being
# handed a stack trace. Every OTHER way that same operator can hold the gate
# wrong — a cwd-relative CHANGE_DIR, a path outside any work tree, a ref that
# names nothing — must therefore land as a NAMED finding too, and the
# cwd-relative shapes must simply WORK, since they are how a person standing in
# the directory actually types it.


def test_the_archive_gate_RUNS_when_CHANGE_DIR_IS_DOT_from_inside_the_archived_dir(tmp_path):
    # `cd openspec/changes/archive/<date>-<id> && ... --archive-gate .` — the
    # change id is decided from the directory's own name and its PARENT's name,
    # so an UNRESOLVED '.' carries neither and the id would read as ''. The
    # directory is resolved before the id is read; this is the shape that
    # regressed when the by-id resolution was first adopted.
    change = _init_change(tmp_path, _SCOPE)
    ratified_ref = _head(tmp_path)
    archive = _archive_move(tmp_path, change, "2026-09-01-add-example")

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
    change = _init_change(tmp_path, _SCOPE)
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
    # converted here or it escapes as a raw `CalledProcessError`.
    change = _init_change(tmp_path, _SCOPE)
    ratified_ref = _head(tmp_path)
    missing = tmp_path / "no" / "such" / "add-example"

    with pytest.raises(sg.ScopeGlobsResolutionError) as excinfo:
        sg.scope_retention_at_archive(missing, ratified_ref)
    assert "git work tree" in str(excinfo.value)

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
    assert str(missing.parent) in result.stdout, result.stdout
    # Untouched: the change itself is fine, so this must not read as a mutation.
    assert "contested" not in result.stdout, result.stdout
    assert change.is_dir()


def test_an_UNRESOLVABLE_RATIFIED_REF_is_named_as_such_not_as_an_absent_change(tmp_path):
    # The by-id probes swallow git's exit status, so without a commit check a
    # bad ref is reported in the wording of a change that is absent at a good
    # one — pointing the operator at the wrong thing entirely.
    change = _init_change(tmp_path, _SCOPE)

    with pytest.raises(sg.ScopeGlobsResolutionError) as excinfo:
        sg.scope_retention_at_archive(change, "no-such-ref")
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
    change = _init_change(tmp_path, _SCOPE)
    blob = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse",
         "HEAD:openspec/changes/add-example/proposal.md"],
        capture_output=True, text=True, check=True).stdout.strip()

    with pytest.raises(sg.ScopeGlobsResolutionError) as excinfo:
        sg.scope_retention_at_archive(change, blob)
    assert "does not name a commit" in str(excinfo.value)


def test_a_MISSING_WORKING_TREE_PROPOSAL_is_a_CANNOT_RUN_finding_not_a_verdict(tmp_path):
    # Reading an ABSENT current-side proposal as "no scope declared" made the
    # gate answer a question it had never asked. With a scope ratified at REF it
    # reported a contested MUTATION — a removal nobody made; with nothing
    # ratified it reported RETAINED. Both are verdicts about a declaration the
    # gate never read, and the CLI's own contract already calls every failure to
    # READ the current front matter a named finding with exit 2.
    change = _init_change(tmp_path, _SCOPE)
    ratified_ref = _head(tmp_path)
    # The directory has to SURVIVE the deletion, so it carries a second file —
    # the shape a real change directory has (proposal.md beside tasks.md).
    (change / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m", "tasks"],
                   check=True, env={**_os_environ(), **_ENV})
    subprocess.run(["git", "-C", str(tmp_path), "rm", "-q",
                    str(change / "proposal.md")], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m", "drop"],
                   check=True, env={**_os_environ(), **_ENV})
    assert change.is_dir() and not (change / "proposal.md").exists()

    with pytest.raises(sg.ScopeGlobsResolutionError) as excinfo:
        sg.scope_retention_at_archive(change, ratified_ref)
    message = str(excinfo.value)
    assert "no proposal.md in the working tree" in message, message
    assert str(change.resolve()) in message, message

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--archive-gate", str(change),
         "--ratified-ref", ratified_ref],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "Traceback" not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "CANNOT RUN" in result.stdout, result.stdout
    # And NOT as the mutation the old reading mistook it for.
    assert "contested" not in result.stdout, result.stdout


def test_the_sibling_loader_REQUIRES_every_attribute_the_gate_uses(tmp_path):
    # The cache probe accepts a module under `sequenced_after_substrate` only
    # when it carries EVERY attribute this module calls: a partial module
    # reused from the cache would raise an AttributeError traceback at the call
    # site instead of the named finding the gate promises.
    module = sg._sequenced_after()
    for attr in ("change_id_of_dir", "proposal_path_at_ref", "SequencedAfterError"):
        assert hasattr(module, attr), attr
    # And the loaded module IS the sibling implementation, not the test package
    # that shares the bare name `sequenced_after`.
    assert Path(module.__file__).name == "sequenced_after.py"
    assert Path(module.__file__).parent.name == "scripts"


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
