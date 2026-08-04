"""THE ADVERTISED VALIDATION, ON THE DOCUMENTED HUMAN LAUNCH — T092 sweep defect 8.

`generate-and-open` advertises that the snapshot it serves is checked against the
pinned openxFactory validator (SC-002's fail-loud guardrail). On the launch the
runbook documents — no `--run-dir` — it never was:

  * `cmd_generate_and_open` defaults its run dir to `tempfile.mkdtemp()`;
  * `_validate` searched for the validator by walking UP from the OUTPUT file;
  * from /tmp no ancestor ever holds an aggregation checkout.

So every ordinary launch printed "validation SKIPPED — no reachable openxFactory
checkout" and served an UNVALIDATED snapshot — and the message blamed the one
thing that was demonstrably present, since `--repo-root` is by definition the
openxFactory checkout being rendered and carries the validator. The sweep's
controlled A/B is the clincher: same corpus, same command, only the run dir
differs → one launch SKIPPED, the other validated.

These tests build both halves of that A/B in a scratch tree with a STUB pinned
validator, so they assert the SEARCH rather than the real validator's verdict:
hermetic, deterministic, and independent of whether an aggregation checkout is
reachable from wherever the suite happens to be running (it is not, from a nested
worktree — which is precisely the shape that hid this).

SECOND HALF OF THE FILE — the regression that fix CAUSED. Reaching the validator
made a second conflation load-bearing: `ok = (returncode == 0)` cannot tell "your
snapshot is wrong" from "I could not run at all", and on a host whose python
lacks `jsonschema`/`referencing` the validator exits 2 saying so. Brett's launch
therefore printed `validation: ERROR jsonschema>=4.18 and referencing are
required` and exited 1 WITHOUT STARTING THE SERVER, mid-T092 acceptance, over a
corpus that was fine. PR #51 was verified only in a container that HAS those
libraries, which is exactly why the dependency gap is simulated here rather than
assumed: these stubs reproduce the missing-dependency exit without uninstalling
anything, so the suite proves the behaviour on a machine that cannot otherwise
show it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION

from ideation_dashboard import snapshot as snapshot_mod
from ideation_dashboard.cli import build_parser, cmd_generate_and_open

STUB_VALIDATOR = """import sys
print("stub-validator: 0 error(s), 0 warning(s)")
sys.exit(0)
"""

# Byte-for-byte what the pinned validator does when its dependencies are absent
# (`openxFactory/scripts/validate-ideation-dashboard-contracts.py`, the import
# guard at the top): the message on stderr, and exit 2 — the "harness error" code
# in the contract its own docstring publishes.
STUB_MISSING_DEPENDENCIES = """import sys
print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
sys.exit(2)
"""

# The OTHER environmental shape, to prove the classifier reads the exit code and
# not that one English sentence: the same harness code, a completely different
# cause and wording (the PyYAML guard three lines above it).
STUB_MISSING_YAML = """import sys
print("ERROR PyYAML is required", file=sys.stderr)
sys.exit(2)
"""

# A real verdict on the DATA: exit 1, the validator's findings code.
STUB_NON_CONFORMANT = """import sys
print("ERROR referential-integrity snapshot.json: cluster 'cl-x' has a dangling "
      "document_edge to 'doc-missing'")
print("")
print("validate-ideation-dashboard-contracts: 1 error(s), 0 warning(s)")
sys.exit(1)
"""


def _corpus_with_a_reachable_validator(tmp_path: Path,
                                       body: str = STUB_VALIDATOR) -> Path:
    """A copy of the fixture corpus at `<aggregation>/openxFactory/`, with the
    pinned validator where `find_validator` expects it — i.e. exactly the shape
    of the real workspace, and the shape `--repo-root` names."""
    import shutil

    aggregation = tmp_path / "aggregation"
    repo_root = aggregation / "openxFactory"
    shutil.copytree(BASE_REPO, repo_root)
    validator = aggregation / snapshot_mod.VALIDATOR_RELPATH
    validator.parent.mkdir(parents=True, exist_ok=True)
    validator.write_text(body, encoding="utf-8")
    return repo_root


def _launch(repo_root: Path, run_dir: Path, *extra: str):
    args = build_parser().parse_args([
        "generate-and-open", "--repo-root", str(repo_root),
        "--repository", "fixture-repo", "--source-revision", PINNED_REVISION,
        "--run-dir", str(run_dir), "--no-open", "--no-serve", *extra,
    ])
    return cmd_generate_and_open(args, opener=lambda url: None)


def _served(captured) -> bool:
    """`--no-serve` still builds the server and prints its URL before closing
    it, so this line is the observable proof that `build_server` was reached —
    the exact step the regression returned before."""
    return "  serving http://" in captured.out


def test_the_default_shaped_launch_validates_from_the_repo_root(tmp_path, capsys):
    """THE DEFECT: the run dir is OUTSIDE any aggregation checkout — the shape
    `tempfile.mkdtemp()` always produces — and the snapshot is validated anyway,
    because `--repo-root` is a checkout and the validator lives in it.

    A real temp dir is not used, because a test that wrote to /tmp/<random> would
    be asserting the same thing with less control; what matters is that the run
    dir has NO aggregation ancestor, which `tmp_path/run` also has not."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path)
    run_dir = tmp_path / "outside" / "run"          # no validator above it
    assert snapshot_mod.find_validator(run_dir.parent) is None

    rc = _launch(repo_root, run_dir)
    captured = capsys.readouterr()

    assert rc == 0
    # the skip line goes to stderr, so BOTH streams have to be clean of it
    assert "validation SKIPPED" not in captured.out + captured.err, captured
    assert "validation: stub-validator: 0 error(s), 0 warning(s)" in captured.out
    assert (run_dir / "snapshot.json").is_file()


def test_a_run_dir_beside_a_checkout_still_uses_that_one_first(tmp_path, capsys):
    """The output path keeps PRIORITY: a run dir deliberately placed inside an
    aggregation checkout is validated by THAT checkout's validator, as before.
    `--repo-root` is the fallback that makes the ordinary launch validate, not a
    replacement for the search that already worked."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path)
    beside = tmp_path / "other-aggregation"
    marker = beside / snapshot_mod.VALIDATOR_RELPATH
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text('print("beside-validator: 0 error(s), 0 warning(s)")\n',
                      encoding="utf-8")
    run_dir = beside / "run"

    rc = _launch(repo_root, run_dir)
    out = capsys.readouterr().out

    assert rc == 0
    assert "beside-validator" in out, out


def test_when_neither_root_reaches_a_validator_the_message_names_both(
        tmp_path, capsys):
    """A skip is still legal — a checkout with no validator in it is a real
    state — but the line must not blame a checkout that is present. It names the
    two directories that were searched, so the human can see which one to fix.

    On stderr, and leading with the consequence rather than the cause (the
    wording PR #50 landed for the same line): a diagnostic that says "this
    snapshot was NOT checked" must not be mistakable for the routine stdout
    progress the surrounding `wrote …` lines are."""
    corpus = tmp_path / "corpus"
    import shutil
    shutil.copytree(BASE_REPO, corpus)
    run_dir = tmp_path / "run"

    rc = _launch(corpus, run_dir)
    captured = capsys.readouterr()

    assert rc == 0
    assert "validation SKIPPED" in captured.err
    assert str(run_dir) in captured.err and str(corpus) in captured.err, captured.err
    assert "NOT checked against the pinned schema" in captured.err
    assert "validation SKIPPED" not in captured.out, captured.out


# ---------------------------------------------------------------------------
# A MISSING TOOLING DEPENDENCY IS NOT A BAD SNAPSHOT
# ---------------------------------------------------------------------------

def test_missing_validator_dependencies_warn_and_the_server_still_starts(
        tmp_path, capsys):
    """THE REGRESSION, in the shape Brett hit it: the validator is reachable, it
    runs, and it exits non-zero because the interpreter running it has no
    `jsonschema`. Nothing is known about the snapshot — which is not the same as
    knowing it is bad, and only the second of those justifies withholding the
    dashboard from the human who asked for it."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path,
                                                   STUB_MISSING_DEPENDENCIES)
    rc = _launch(repo_root, tmp_path / "run")
    captured = capsys.readouterr()

    assert rc == 0, captured.err
    assert _served(captured), captured.out
    assert "NOT checked against the pinned schema" in captured.err


def test_the_dependency_warning_carries_the_pip_remedy_and_clears_the_corpus(
        tmp_path, capsys):
    """A warning that does not say what to type is a warning that gets ignored.
    It must also relay the validator's OWN diagnosis (it is the thing that knows
    which library it wanted) and state plainly that the corpus is not the
    accused — the wrong half of that sentence is what a stopped human reads
    first."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path,
                                                   STUB_MISSING_DEPENDENCIES)
    _launch(repo_root, tmp_path / "run")
    err = capsys.readouterr().err

    assert "pip install 'jsonschema>=4.18' referencing" in err, err
    assert "ERROR jsonschema>=4.18 and referencing are required" in err, err
    assert "the ENVIRONMENT, not the snapshot" in err, err
    assert "SERVES this unchecked snapshot" in err, err


def test_a_non_conformant_snapshot_still_blocks_and_blames_the_snapshot(
        tmp_path, capsys):
    """The other half of the distinction, and the one the fix must not spend: a
    validator that RAN and rejected the data still stops the serve. The message
    is about the snapshot, and it must not offer the dependency remedy — sending
    someone to `pip install` over a dangling document edge is the same defect
    pointing the other way."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path,
                                                   STUB_NON_CONFORMANT)
    rc = _launch(repo_root, tmp_path / "run")
    captured = capsys.readouterr()

    assert rc == 1
    assert not _served(captured), captured.out
    assert "REJECTED" in captured.err and "dangling document_edge" in captured.err
    assert "pip install" not in captured.err, captured.err
    assert "jsonschema" not in captured.err, captured.err


def test_strict_makes_an_unrunnable_validator_fatal(tmp_path, capsys):
    """`--strict` is a demand for certainty, so "we could not check" is a
    failure under it — otherwise the flag would quietly mean less than it
    says."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path,
                                                   STUB_MISSING_DEPENDENCIES)
    rc = _launch(repo_root, tmp_path / "run", "--strict")
    captured = capsys.readouterr()

    assert rc == 1
    assert not _served(captured), captured.out
    assert "--strict was given" in captured.err
    # and it must not also claim the run continues
    assert "SERVES this unchecked snapshot" not in captured.err, captured.err


def test_strict_is_fatal_when_no_validator_is_reachable_either(tmp_path, capsys):
    """The same rule for the other unavailable sub-case. A `--strict` run that
    found no validator at all learned exactly as much as one whose validator
    would not start."""
    import shutil

    corpus = tmp_path / "corpus"
    shutil.copytree(BASE_REPO, corpus)

    assert _launch(corpus, tmp_path / "run") == 0             # warns, serves
    capsys.readouterr()
    assert _launch(corpus, tmp_path / "run2", "--strict") == 1
    assert "--strict was given" in capsys.readouterr().err


def test_the_classifier_reads_the_exit_code_not_the_dependency_sentence(
        tmp_path, capsys):
    """The guard against fixing this brittlely. A different environmental
    failure, with different words and no mention of jsonschema, is classified
    the same way — because the signal is the validator's documented exit code
    (2 = harness error), not a phrase that a future edit could reword."""
    repo_root = _corpus_with_a_reachable_validator(tmp_path, STUB_MISSING_YAML)
    rc = _launch(repo_root, tmp_path / "run")
    captured = capsys.readouterr()

    assert rc == 0, captured.err
    assert _served(captured), captured.out
    assert "ERROR PyYAML is required" in captured.err
    assert "NOT checked against the pinned schema" in captured.err
