"""`scripts/validate-carve-manifest.py` — every refusal code pinned by a test
that can only pass if that check runs.

WHY A THROWAWAY REPOSITORY AND NOT THIS ONE. Every refusal here is a
disagreement between a manifest and a git tree, and manufacturing one against
`openxFactory` would mean editing the repository under the test. So each case
builds a fresh git repository in `tmp_path`, commits a handful of files, and
generates a manifest FROM that tree — so the clean case is clean by
construction and every refusal is one deliberate mutation away from it. The
generator is the point: a hand-written fixture manifest would rot against the
validator, and a test that had to be edited whenever a digest changed would
stop being evidence.

THE SCRIPT IS RUN AS A SUBPROCESS, not imported, for the reason
`tests/manifest_digests/test_manifest_digest_sweep.py:26-45` gives: the
documented way to invoke it is `python3 scripts/validate-carve-manifest.py`,
and a test of the imported function proves the code executes rather than that
the documented invocation succeeds and prints what its readers depend on. The
module IS also loaded by path, once, for the two constant assertions — the
ratified refusal vocabulary and the ruled manifest path — because those are
claims about the file's contents rather than about a run.

THE REAL-REPOSITORY TEST IS THE § 8.2 SEAT AND IT DOES NOT SKIP.
`docs/opendox-carve-manifest.yaml` does not exist yet — the § 6 ceremony
authors it at the carve commit, AFTER this validator lands — so today the
validator's seat-holding branch answers and the test asserts exit 0 with the
`NO MANIFEST` line. The moment the manifest lands, the same test asserts exit 0
with the `OK` line instead, and from then on a file that changes on `main`
between the manifest and the move reds this suite as a `carve-digest-mismatch`,
which is the intended pressure of the ceremony rather than a defect in it. It
is a BRANCH and never a `pytest.skip`: a skip reports as a green bar, which is
indistinguishable from a pass to every reader — and `pytest-suite.yml` pins the
skip count exactly, so a conditional skip here would red the required job.

Hermetic: no network and no `nlm`/`gh`/`omp` (`tests/hermeticity.py`'s guarded
set); `git` is not guarded, and the environment it reads is PINNED rather than
inherited — `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a
repository-local identity, the same treatment and for the same reasons as
`tests/openxwallet_pin/test_verify_pin.py:32-40`: a CI runner has no ambient
git identity and a developer's global config can carry `core.hooksPath` or
`commit.gpgsign`, and the ambient installation must not change the answer.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "validate-carve-manifest.py"

# The vocabulary, restated as a LITERAL rather than imported. Asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology; spelling
# the list out is what makes a silent rename or reorder in the validator a test
# failure — which is the point, because other code branches BY CODE.
RATIFIED_CODES = (
    "carve-shape-invalid",
    "carve-revision-mismatch",
    "carve-digest-mismatch",
    "carve-path-absent",
    "carve-file-undeclared",
    "carve-file-duplicated",
    "carve-vocabulary-unknown",
    "carve-disposition-inconsistent",
    "carve-path-order-violation",
)

# RULING OQ-1's own list, verbatim. Three, not four.
RULED_EDIT_CLASSES = ["import rewrites", "path constants", "adapter calls"]

SURFACE = "scripts/pkg/"


def _load():
    """The validator as a module, loaded by path because
    `validate-carve-manifest.py` is hyphenated and therefore unimportable — the
    same reason `tests/openxwallet_pin/test_verify_pin.py` loads its subject
    this way. The import must be side-effect-free beyond module constants."""
    spec = importlib.util.spec_from_file_location("validate_carve_manifest",
                                                  SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load()


# --------------------------------------------------------------------------
# the hermetic git environment
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _hermetic_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "carve-manifest-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "carve-test@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "carve-manifest-test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "carve-test@example.invalid")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr}"
    return done


def _write(repo: Path, rel: str, text: str) -> None:
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


class Scratch:
    """A throwaway repository with two commits and a four-file carve surface.

    `docs/outside.md` sits OUTSIDE `moved_paths:` deliberately: without a file
    the surface must not swallow, the completeness check would pass for a
    validator that walked the whole tree.
    """

    def __init__(self, repo: Path, first: str, head: str) -> None:
        self.repo = repo
        self.first = first
        self.head = head

    def manifest_path(self) -> Path:
        return self.repo / MODULE.MANIFEST_RELPATH

    def write(self, doc: dict[str, Any]) -> Path:
        path = self.manifest_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return path

    def blobs(self, commit: str) -> dict[str, str]:
        """`{path: git_mode}` for the carve surface at `commit`, read the way
        the validator reads it."""
        listing = _git(self.repo, "ls-tree", "-r", "--full-tree", commit).stdout
        out: dict[str, str] = {}
        for line in listing.splitlines():
            meta, _, path = line.partition("\t")
            mode, kind, _oid = meta.split(" ")
            if kind == "blob" and path.startswith(SURFACE):
                out[path] = mode
        return out

    def digest(self, commit: str, path: str) -> str:
        raw = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "blob",
             f"{commit}:{path}"], capture_output=True, check=True).stdout
        return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def scratch(tmp_path: Path) -> Scratch:
    repo = tmp_path / "scratch"
    repo.mkdir()
    _git(tmp_path, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.name", "carve-manifest-test")
    _git(repo, "config", "user.email", "carve-test@example.invalid")
    _write(repo, "scripts/pkg/alpha.py", "ALPHA = 1\n")
    _write(repo, "scripts/pkg/beta.py", "import alpha\nBETA = 2\nCALL = 3\n")
    _write(repo, "scripts/pkg/gamma.py", "GAMMA = 3\n")
    _write(repo, "docs/outside.md", "# outside the carve surface\n")
    _git(repo, "add", "--", "scripts", "docs")
    _git(repo, "commit", "-q", "-m", "seed the carve surface")
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _write(repo, "scripts/pkg/delta.py", "DELTA = 4\n")
    _git(repo, "add", "--", "scripts")
    _git(repo, "commit", "-q", "-m", "the adapter file the carve keeps")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    return Scratch(repo, first, head)


# --------------------------------------------------------------------------
# the manifest generator
# --------------------------------------------------------------------------

def clean_manifest(scratch: Scratch, commit: str | None = None
                   ) -> dict[str, Any]:
    """A manifest that verifies, generated from the tree it describes.

    All three dispositions are exercised, so a mutation test starts from a
    document in which every branch of every check has already run.
    """
    commit = commit or scratch.head
    blobs = scratch.blobs(commit)
    rows: list[dict[str, Any]] = []
    for path in sorted(blobs, key=lambda p: p.encode("utf-8")):
        name = path.rsplit("/", 1)[-1]
        if name == "delta.py":
            rows.append({
                "source_path": path,
                "disposition": "not_moved",
                "reason": "stays_openxfactory_adapter",
                "evidence": "the adapter column keeps this reader (RULING DQ-1)",
            })
            continue
        row: dict[str, Any] = {
            "source_path": path,
            "git_mode": blobs[path],
            "sha256": scratch.digest(commit, path),
            "disposition": "moved_verbatim",
            "destination": "opendox_code",
            "destination_path": f"src/opendox/{name}",
        }
        if name == "beta.py":
            row["disposition"] = "moved_with_declared_edit"
            row["destination"] = "openxdox_code"
            row["destination_path"] = f"src/openxdox/{name}"
            row["edits"] = [
                {"class": "import rewrites", "lines": [1]},
                {"class": "adapter calls", "lines": [3],
                 "note": "the module's only openxFactory reach"},
            ]
        rows.append(row)
    return {
        "schema_version": 1,
        "kind": "opendox-carve-manifest",
        "header": ("the first machine-validated YAML under docs/ in this "
                   "repository (RULED OQ-E)"),
        "carve_commit": commit,
        "carve_tag": "opendox-carve-0",
        "source_repository": "opensoft/openxFactory",
        "digest_algorithm": "sha256",
        "digest_source": "raw_git_blob",
        "path_order": "bytewise_utf8",
        "destinations": {
            "opendox_code": {"repository": "opensoft/openDox-code",
                             "leg": "code"},
            "openxdox_code": {"repository": "opensoft/openXdox-code",
                              "leg": "code"},
        },
        "edit_classes": list(RULED_EDIT_CLASSES),
        "not_moved_reasons": ["stays_openxfactory_adapter",
                              "deleted_at_carve",
                              "replicated_at_destination"],
        "moved_paths": [SURFACE],
        "rows": rows,
    }


def row_named(doc: dict[str, Any], name: str) -> dict[str, Any]:
    for row in doc["rows"]:
        if row["source_path"].endswith("/" + name):
            return row
    raise AssertionError(f"no row for {name} in the generated manifest")


def run(scratch: Scratch, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(scratch.repo), *args],
        capture_output=True, text=True, check=False)


def refuses(scratch: Scratch, doc: dict[str, Any], code: str,
            *args: str) -> str:
    """Write `doc`, run the validator, and assert exactly `code`."""
    scratch.write(doc)
    done = run(scratch, *args)
    combined = done.stdout + done.stderr
    assert done.returncode == 2, combined
    assert f": {code} —" in combined, combined
    assert "Remediation:" in combined, combined
    return combined


# --------------------------------------------------------------------------
# the constants
# --------------------------------------------------------------------------

def test_the_refusal_vocabulary_is_the_ratified_list() -> None:
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES


def test_the_edit_class_list_is_the_rulings_own_verbatim() -> None:
    """Three, not four. The packet proposed `vocabulary parameterization` and
    the ruling does not carry it, so a parameterization edit is expressible as
    one of these three or it is not a carve edit at all."""
    assert list(MODULE.EDIT_CLASSES) == RULED_EDIT_CLASSES
    assert list(MODULE.DISPOSITIONS) == [
        "moved_verbatim", "moved_with_declared_edit", "not_moved"]


def test_the_manifest_path_is_the_ruled_one() -> None:
    """RULED OQ-E: the ruled path is honoured verbatim rather than moved to
    `contracts/` to match the convention."""
    assert MODULE.MANIFEST_RELPATH == "docs/opendox-carve-manifest.yaml"


def test_the_reason_vocabulary_is_the_ruled_five() -> None:
    assert sorted(MODULE.KNOWN_NOT_MOVED_REASONS) == sorted([
        "stays_openxfactory_adapter", "stays_openxfactory_governance",
        "deleted_at_carve", "superseded_by_split", "replicated_at_destination"])


# --------------------------------------------------------------------------
# the clean pass, the absent manifest, and --at
# --------------------------------------------------------------------------

def test_a_generated_manifest_verifies(scratch: Scratch) -> None:
    scratch.write(clean_manifest(scratch))
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "OK " in done.stdout, done.stdout
    assert "2 moved_verbatim, 1 moved_with_declared_edit, 1 not_moved" \
        in done.stdout, done.stdout
    assert "3 digest(s) recomputed" in done.stdout, done.stdout
    assert "4 file(s) in the declared surface with none undeclared" \
        in done.stdout, done.stdout


def test_an_absent_manifest_is_not_a_refusal(scratch: Scratch) -> None:
    """The seat-holding pass: this validator lands BEFORE its subject, and a
    red suite on every pull request until the carve would train the lane to
    ignore it."""
    assert not scratch.manifest_path().exists()
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "NO MANIFEST" in done.stdout, done.stdout
    assert "(nothing to validate)" in done.stdout, done.stdout


def test_at_verifies_an_earlier_carve_commit(scratch: Scratch) -> None:
    """The manifest is cut at the carve commit and `main` moves on; `--at`
    asks the question the manifest actually answers."""
    scratch.write(clean_manifest(scratch, scratch.first))
    done = run(scratch, "--at", scratch.first)
    assert done.returncode == 0, done.stdout + done.stderr
    assert scratch.first[:12] in done.stdout, done.stdout


def test_an_at_that_resolves_elsewhere_still_refuses(scratch: Scratch) -> None:
    refuses(scratch, clean_manifest(scratch, scratch.first),
            "carve-revision-mismatch", "--at", scratch.head)


def test_an_unresolvable_at_refuses(scratch: Scratch) -> None:
    refuses(scratch, clean_manifest(scratch), "carve-revision-mismatch",
            "--at", "no-such-revision")


# --------------------------------------------------------------------------
# check 1 — shape
# --------------------------------------------------------------------------

def test_a_wrong_kind_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["kind"] = "opendox-carve-map"
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_flipped_const_refuses(scratch: Scratch) -> None:
    """`digest_source` is a const of the row grammar, not a per-manifest
    choice: a manifest that digested working-tree bytes would verify against a
    tree it never read."""
    doc = clean_manifest(scratch)
    doc["digest_source"] = "working_tree"
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_abbreviated_carve_commit_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["carve_commit"] = scratch.head[:12]
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_uppercase_carve_commit_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["carve_commit"] = scratch.head.upper()
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_tag_used_as_the_referent_refuses(scratch: Scratch) -> None:
    """The tag is a LABEL beside the commit and never the referent."""
    doc = clean_manifest(scratch)
    doc["carve_commit"] = "opendox-carve-0"
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_moved_row_without_a_destination_path_refuses(
        scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    del row_named(doc, "alpha.py")["destination_path"]
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_unquoted_git_mode_refuses(scratch: Scratch) -> None:
    """`git_mode: 100644` unquoted parses as an int, and a mode flip is the one
    change a blob digest cannot see."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["git_mode"] = 100644
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_not_moved_row_carrying_a_digest_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "delta.py")["sha256"] = "0" * 64
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_not_moved_row_without_evidence_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    del row_named(doc, "delta.py")["evidence"]
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_moved_row_carrying_a_reason_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["reason"] = "deleted_at_carve"
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_declared_fourth_edit_class_refuses(scratch: Scratch) -> None:
    """The list is closed AND asserted equal to the ruling's own: a manifest
    that declared its own fourth class would otherwise validate against
    itself."""
    doc = clean_manifest(scratch)
    doc["edit_classes"] = RULED_EDIT_CLASSES + ["vocabulary parameterization"]
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_reordered_edit_class_list_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["edit_classes"] = list(reversed(RULED_EDIT_CLASSES))
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_not_moved_reason_the_validator_does_not_know_refuses(
        scratch: Scratch) -> None:
    """Declared AND known: the reason vocabulary is the memo's invention rather
    than the ruling's, so the file declares its own subset — but it may not
    widen the set by declaring it."""
    doc = clean_manifest(scratch)
    doc["not_moved_reasons"] = ["stays_openxfactory_adapter", "felt_right"]
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_row_outside_the_declared_surface_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["rows"].insert(0, {
        "source_path": "docs/outside.md",
        "git_mode": "100644",
        "sha256": scratch.digest(scratch.head, "docs/outside.md"),
        "disposition": "moved_verbatim",
        "destination": "opendox_code",
        "destination_path": "docs/outside.md",
    })
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_edit_with_no_line_numbers_refuses(scratch: Scratch) -> None:
    """Without line numbers `moved_with_declared_edit` is only a label — the
    numbers are what make the claim falsifiable at the destination."""
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["edits"] = [{"class": "import rewrites",
                                           "lines": []}]
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_edit_with_an_unknown_key_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["edits"][0]["rationale"] = "because"
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_row_with_an_unknown_key_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["destination_branch"] = "main"
    refuses(scratch, doc, "carve-shape-invalid")


# --------------------------------------------------------------------------
# check 2 — revision
# --------------------------------------------------------------------------

def test_head_that_is_not_the_carve_commit_refuses(scratch: Scratch) -> None:
    """The manifest is the LAST thing on the carve tree, so anything merged
    after it goes red until it is re-cut. That is the ceremony's intended
    pressure."""
    doc = clean_manifest(scratch, scratch.first)
    combined = refuses(scratch, doc, "carve-revision-mismatch")
    assert scratch.head in combined, combined


def test_the_revision_check_runs_before_the_digests(scratch: Scratch) -> None:
    """A stale tree is reported as ONE revision mismatch rather than as a pile
    of digest failures — the ordering is the finding."""
    doc = clean_manifest(scratch, scratch.first)
    row_named(doc, "alpha.py")["sha256"] = "0" * 64
    refuses(scratch, doc, "carve-revision-mismatch")


# --------------------------------------------------------------------------
# check 3 — digests
# --------------------------------------------------------------------------

def test_a_drifted_digest_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["sha256"] = "0" * 64
    combined = refuses(scratch, doc, "carve-digest-mismatch")
    assert "DIGEST DRIFT" in combined, combined


def test_a_digest_taken_at_the_wrong_revision_refuses(
        scratch: Scratch) -> None:
    """Not a synthetic digest: the REAL sha256 of a real file, taken from the
    tree the manifest does not name."""
    doc = clean_manifest(scratch)
    _write(scratch.repo, "scripts/pkg/alpha.py", "ALPHA = 99\n")
    _git(scratch.repo, "add", "--", "scripts")
    _git(scratch.repo, "commit", "-q", "-m", "alpha moves after the manifest")
    moved = _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()
    doc["carve_commit"] = moved
    doc["rows"] = clean_manifest(scratch, moved)["rows"]
    row_named(doc, "alpha.py")["sha256"] = scratch.digest(
        scratch.head, "scripts/pkg/alpha.py")
    refuses(scratch, doc, "carve-digest-mismatch")


def test_a_mode_flip_refuses(scratch: Scratch) -> None:
    """The mode is carried because a mode flip is what a blob digest does not
    see."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["git_mode"] = "100755"
    combined = refuses(scratch, doc, "carve-digest-mismatch")
    assert "MODE DRIFT" in combined, combined


def test_a_moved_row_for_a_path_the_commit_does_not_carry_refuses(
        scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["rows"].append({
        "source_path": "scripts/pkg/zeta.py",
        "git_mode": "100644",
        "sha256": "0" * 64,
        "disposition": "moved_verbatim",
        "destination": "opendox_code",
        "destination_path": "src/opendox/zeta.py",
    })
    refuses(scratch, doc, "carve-path-absent")


def test_a_not_moved_row_for_an_absent_path_refuses(scratch: Scratch) -> None:
    """The digest loop never reads a `not_moved` row, so the surface check is
    what catches a row for a file that is not there."""
    doc = clean_manifest(scratch)
    doc["rows"].append({
        "source_path": "scripts/pkg/zeta.py",
        "disposition": "not_moved",
        "reason": "deleted_at_carve",
        "evidence": "its own docstring says the carve deletes it",
    })
    refuses(scratch, doc, "carve-path-absent")


# --------------------------------------------------------------------------
# check 4 — surface completeness
# --------------------------------------------------------------------------

def test_a_file_in_no_row_refuses(scratch: Scratch) -> None:
    """RULING OQ-1's own sentence as running code: a file in no row is an
    UNDECLARED MOVEMENT and the carve refuses."""
    doc = clean_manifest(scratch)
    doc["rows"] = [r for r in doc["rows"]
                   if not r["source_path"].endswith("/gamma.py")]
    combined = refuses(scratch, doc, "carve-file-undeclared")
    assert "scripts/pkg/gamma.py" in combined, combined


def test_a_file_in_two_rows_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["rows"].insert(1, copy.deepcopy(row_named(doc, "alpha.py")))
    refuses(scratch, doc, "carve-file-duplicated")


def test_a_file_outside_the_surface_is_not_undeclared(
        scratch: Scratch) -> None:
    """`docs/outside.md` needs no row: the completeness check walks the
    declared prefixes, not the whole tree."""
    scratch.write(clean_manifest(scratch))
    assert run(scratch).returncode == 0


def test_a_sibling_directory_is_not_swallowed_by_the_prefix(
        scratch: Scratch) -> None:
    """`scripts/pkg` must not swallow `scripts/pkg_old/`, which a bare
    `startswith` would."""
    _write(scratch.repo, "scripts/pkg_old/legacy.py", "LEGACY = 1\n")
    _git(scratch.repo, "add", "--", "scripts")
    _git(scratch.repo, "commit", "-q", "-m", "a sibling the surface excludes")
    doc = clean_manifest(scratch)
    doc["carve_commit"] = _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()
    doc["moved_paths"] = ["scripts/pkg"]
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_digest_check_runs_before_the_surface_check(
        scratch: Scratch) -> None:
    """Ordering pinned: a manifest wrong in both ways reports the digest."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["sha256"] = "0" * 64
    doc["rows"] = [r for r in doc["rows"]
                   if not r["source_path"].endswith("/gamma.py")]
    refuses(scratch, doc, "carve-digest-mismatch")


# --------------------------------------------------------------------------
# check 5 — the closed vocabularies
# --------------------------------------------------------------------------

def test_a_fourth_disposition_refuses(scratch: Scratch) -> None:
    """RULED OQ-C: the disposition list stays three, and the `not_moved` reason
    carries the nuance the three cannot express."""
    doc = clean_manifest(scratch)
    row_named(doc, "delta.py")["disposition"] = "replicated"
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_an_undeclared_destination_key_refuses(scratch: Scratch) -> None:
    """One typo otherwise ships a file to a repository nobody declared."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["destination"] = "opendox_kode"
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_an_edit_class_outside_the_closed_list_refuses(
        scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["edits"][0]["class"] = "vocabulary parameterization"
    combined = refuses(scratch, doc, "carve-vocabulary-unknown")
    assert "UNDECLARED MOVEMENT" in combined, combined


def test_a_reason_the_manifest_does_not_declare_refuses(
        scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "delta.py")["reason"] = "superseded_by_split"
    refuses(scratch, doc, "carve-vocabulary-unknown")


# --------------------------------------------------------------------------
# check 6 — disposition consistency, then the path order
# --------------------------------------------------------------------------

def test_a_declared_edit_with_no_edits_refuses(scratch: Scratch) -> None:
    """`moved_with_declared_edit` with an empty `edits:` is `moved_verbatim`
    mislabelled."""
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["edits"] = []
    refuses(scratch, doc, "carve-disposition-inconsistent")


def test_a_declared_edit_with_no_edits_key_at_all_refuses(
        scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    del row_named(doc, "beta.py")["edits"]
    refuses(scratch, doc, "carve-disposition-inconsistent")


def test_verbatim_with_edits_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["edits"] = [{"class": "import rewrites",
                                            "lines": [1]}]
    refuses(scratch, doc, "carve-disposition-inconsistent")


def test_not_moved_with_edits_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    row_named(doc, "delta.py")["edits"] = [{"class": "adapter calls",
                                            "lines": [1]}]
    refuses(scratch, doc, "carve-disposition-inconsistent")


def test_rows_out_of_bytewise_order_refuse(scratch: Scratch) -> None:
    """A ~430-row manifest is reviewed by diff, and a diff of an unsorted file
    hides a moved row inside a reordering."""
    doc = clean_manifest(scratch)
    doc["rows"] = list(reversed(doc["rows"]))
    refuses(scratch, doc, "carve-path-order-violation")


# --------------------------------------------------------------------------
# --json
# --------------------------------------------------------------------------

def test_json_reports_the_summary(scratch: Scratch) -> None:
    scratch.write(clean_manifest(scratch))
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "ok"
    assert payload["carve_commit"] == scratch.head
    assert payload["rows"] == 4
    assert payload["digests_recomputed"] == 3
    assert payload["surface"] == 4
    assert payload["dispositions"]["not_moved"] == 1


def test_json_reports_the_refusal_code(scratch: Scratch) -> None:
    """The code is carried as a FIELD, so a caller branches on it without
    parsing prose."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["sha256"] = "0" * 64
    scratch.write(doc)
    done = run(scratch, "--json")
    assert done.returncode == 2, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "refused"
    assert payload["code"] == "carve-digest-mismatch"
    assert payload["code"] in RATIFIED_CODES


def test_json_reports_the_absent_manifest(scratch: Scratch) -> None:
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["result"] == "no-manifest"


# --------------------------------------------------------------------------
# the real repository — the § 8.2 seat
# --------------------------------------------------------------------------

def test_the_real_repository_answers_at_the_ruled_path() -> None:
    """The documented invocation, from the repository root, with no arguments.

    A BRANCH and never a skip: see the module docstring. Today the manifest
    does not exist and the seat-holding line answers; once the § 6 ceremony
    lands it at the carve commit, the same call must print `OK`.
    """
    done = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if manifest.is_file():
        assert done.stdout.startswith("OK "), done.stdout
    else:
        assert done.stdout.startswith("NO MANIFEST "), done.stdout
        assert "(nothing to validate)" in done.stdout, done.stdout
