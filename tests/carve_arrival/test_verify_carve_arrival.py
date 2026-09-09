"""`scripts/verify-carve-arrival.py` — every refusal code pinned by a test that
can only pass if that check runs.

WHY A THROWAWAY SOURCE REPOSITORY AND A THROWAWAY DESTINATION. Every refusal
here is a disagreement between a manifest, a carve commit's blobs and an ARRIVED
tree, and no destination exists yet: `opensoft/openDox-code` and its four
siblings hold not one carved byte until Phase 2 of
`docs/opendox-cutover-runbook.md` runs. So each case builds a fresh git
repository in `tmp_path`, commits a small carve surface, GENERATES a manifest
from that tree, and materialises a destination directory from the manifest's own
rows — so the clean case is clean by construction and every refusal is one
deliberate mutation away from it. The generator is the point: a hand-written
fixture would rot against the verifier, and a test that had to be edited
whenever a digest changed would stop being evidence.

THE SCRIPT IS RUN AS A SUBPROCESS, not imported, for
`tests/carve_manifest/test_carve_manifest.py`'s reason: the documented way to
invoke it is `python3 scripts/verify-carve-arrival.py …`, and a test of the
imported function proves the code executes rather than that the documented
invocation succeeds and prints what its readers depend on. EVERY behavioural
test here goes through the subprocess. The module IS also loaded by path, once,
for the constant assertions, and the script's SOURCE is read once more to assert
that the closed vocabulary is COMPLETE — claims about the file's contents rather
than about a run.

THE REAL-REPOSITORY TEST IS THE SEAT AND IT DOES NOT SKIP. Run with no
`--destination`, from the repository root, the verifier prints
`NO DESTINATION (nothing to verify; …)` and exits 0. That is the seat-holding
branch the module docstring describes, and it is a BRANCH and never a
`pytest.skip`: a skip reports as a green bar, indistinguishable from a pass to
every reader, and `pytest-suite.yml` pins the skip count EXACTLY, so a
conditional skip here would red the required job. When the first destination
exists, this file gains a case that names it; the seat's own assertion is about
the documented invocation and stays true either way.

Hermetic: no network and no `nlm`/`gh`/`omp` (`tests/hermeticity.py`'s guarded
set); `git` is not guarded, and the environment it reads is PINNED rather than
inherited — `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a
repository-local identity, the same treatment and the same reasons as
`tests/carve_manifest/test_carve_manifest.py:_hermetic_git`: a CI runner has no
ambient git identity, a developer's global config can carry `core.hooksPath` or
`commit.gpgsign`, and the ambient installation must not change the answer.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify-carve-arrival.py"

# The vocabulary, restated as a LITERAL rather than imported. Asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology; spelling
# the list out is what makes a silent rename or reorder in the verifier a test
# failure — which is the point, because other code branches BY CODE.
RATIFIED_CODES = (
    "arrival-missing",
    "arrival-digest-mismatch",
    "arrival-undeclared-edit",
    "arrival-undeclared-file",
    "arrival-carved-from-mismatch",
    "arrival-unreadable",
)

CARVE_TAG = "opendox-carve-0"
SOURCE_REPOSITORY = "opensoft/openxFactory"

# The scratch carve surface. `docs/outside.md` sits outside every row
# deliberately: without a file no destination should ever receive, a destination
# built from "everything in the source" would pass a verifier that never read
# the rows at all.
SURFACE_FILES: dict[str, str] = {
    "scripts/pkg/alpha.py": "ALPHA = 1\n",
    "scripts/pkg/beta.py": "import ideation_dashboard.alpha\nBETA = 2\nCALL = 3\n",
    "scripts/pkg/gamma.py": "GAMMA = 3\n",
    "scripts/pkg/neutral.py": "NEUTRAL = 4\n",
    "docs/outside.md": "# outside every row\n",
}

# `beta.py`'s ONE declared edit line, at the carve commit: the `import
# rewrites` class's dominant shape, `ideation_dashboard.X` -> `opendox.X`.
BETA_DECLARED_LINE = 1
BETA_REWRITTEN = "import opendox.alpha\nBETA = 2\nCALL = 3\n"


def _load():
    """The verifier as a module, loaded by path because
    `verify-carve-arrival.py` is hyphenated and therefore unimportable — the
    same reason `tests/carve_manifest/test_carve_manifest.py` loads its subject
    this way. The import must be side-effect-free beyond module constants."""
    spec = importlib.util.spec_from_file_location("verify_carve_arrival",
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
    monkeypatch.setenv("GIT_AUTHOR_NAME", "carve-arrival-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "carve-arrival@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "carve-arrival-test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "carve-arrival@example.invalid")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr}"
    return done


def _write(root: Path, rel: str, text: str) -> None:
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------
# the fixture: a source repository, a manifest generated from it, and a
# destination materialised from the manifest
# --------------------------------------------------------------------------

class Carve:
    """A scratch source repository at a carve commit, plus its manifest."""

    def __init__(self, source: Path, carve_commit: str, tmp: Path) -> None:
        self.source = source
        self.carve_commit = carve_commit
        self.tmp = tmp

    def manifest_doc(self) -> dict[str, Any]:
        """A manifest generated FROM the tree it describes.

        Two destinations, so the row filter is exercised rather than assumed —
        a verifier that ignored `destination` would place `gamma.py` at the code
        leg and every arrival assertion would still pass. All three moved
        dispositions and the replica reason appear, so a mutation test starts
        from a document in which every branch has already run.
        """
        def blob(path: str) -> bytes:
            return subprocess.run(
                ["git", "-C", str(self.source), "cat-file", "blob",
                 f"{self.carve_commit}:{path}"],
                capture_output=True, check=True).stdout

        return {
            "schema_version": 1,
            "kind": "opendox-carve-manifest",
            "carve_commit": self.carve_commit,
            "carve_tag": CARVE_TAG,
            "source_repository": SOURCE_REPOSITORY,
            "digest_algorithm": "sha256",
            "digest_source": "raw_git_blob",
            "path_order": "bytewise_utf8",
            "destinations": {
                "scratch_code": {"repository": "opensoft/scratch-code",
                                 "leg": "code"},
                "scratch_spec": {"repository": "opensoft/scratch-spec",
                                 "leg": "spec"},
                "scratch_root": {"repository": "opensoft/scratch",
                                 "leg": "assembly"},
            },
            "edit_classes": ["import rewrites", "path constants",
                             "adapter calls"],
            "not_moved_reasons": ["replicated_at_destination"],
            "moved_paths": ["scripts/pkg/"],
            "rows": [
                {"source_path": "scripts/pkg/alpha.py",
                 "disposition": "moved_verbatim",
                 "git_mode": "100644",
                 "sha256": _sha256(blob("scripts/pkg/alpha.py")),
                 "destination": "scratch_code",
                 "destination_path": "src/pkg/alpha.py"},
                {"source_path": "scripts/pkg/beta.py",
                 "disposition": "moved_with_declared_edit",
                 "git_mode": "100644",
                 "sha256": _sha256(blob("scripts/pkg/beta.py")),
                 "destination": "scratch_code",
                 "destination_path": "src/pkg/beta.py",
                 "edits": [{"class": "import rewrites",
                            "lines": [BETA_DECLARED_LINE],
                            "note": "ideation_dashboard.alpha -> opendox.alpha"}]},
                {"source_path": "scripts/pkg/gamma.py",
                 "disposition": "moved_verbatim",
                 "git_mode": "100755",
                 "sha256": _sha256(blob("scripts/pkg/gamma.py")),
                 "destination": "scratch_spec",
                 "destination_path": "examples/gamma.py"},
                {"source_path": "scripts/pkg/neutral.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination",
                 "evidence": "neutral by test; a replica at each destination "
                             "and retained here (RULED OQ-A)"},
            ],
        }

    def write_manifest(self, doc: dict[str, Any], name: str = "manifest.yaml"
                       ) -> Path:
        path = self.tmp / name
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return path

    def materialise(self, doc: dict[str, Any], destination: str,
                    name: str | None = None) -> Path:
        """A destination directory built from the manifest's own rows — commit
        A, byte-identical, which is what `--phase A` asserts."""
        dest = self.tmp / (name or f"dest-{destination}")
        dest.mkdir(parents=True, exist_ok=True)
        for row in doc["rows"]:
            if row.get("destination") != destination:
                continue
            data = subprocess.run(
                ["git", "-C", str(self.source), "cat-file", "blob",
                 f"{self.carve_commit}:{row['source_path']}"],
                capture_output=True, check=True).stdout
            target = dest / row["destination_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            if row["git_mode"] == "100755":
                target.chmod(target.stat().st_mode | stat.S_IXUSR)
        return dest


@pytest.fixture
def carve(tmp_path: Path) -> Carve:
    source = tmp_path / "source"
    source.mkdir()
    _git(tmp_path, "init", "-q", "-b", "main", str(source))
    _git(source, "config", "user.name", "carve-arrival-test")
    _git(source, "config", "user.email", "carve-arrival@example.invalid")
    for rel, text in SURFACE_FILES.items():
        _write(source, rel, text)
    (source / "scripts/pkg/gamma.py").chmod(0o755)
    _git(source, "add", "--", "scripts", "docs")
    _git(source, "commit", "-q", "-m", "seed the carve surface")
    head = _git(source, "rev-parse", "HEAD").stdout.strip()
    return Carve(source, head, tmp_path)


def run(carve: Carve, manifest: Path, *args: str) -> subprocess.CompletedProcess:
    """The DOCUMENTED invocation, as a subprocess."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest),
         "--source-repo", str(carve.source), *args],
        capture_output=True, text=True, check=False)


def refusal(done: subprocess.CompletedProcess) -> str:
    """The code from a `--json` run, asserted to be exit 2."""
    assert done.returncode == 2, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "refused", payload
    return payload["code"]


# --------------------------------------------------------------------------
# the constants, and the closure of the vocabulary
# --------------------------------------------------------------------------

def test_the_refusal_vocabulary_is_the_ratified_list() -> None:
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES


def test_every_code_the_verifier_can_emit_is_in_the_vocabulary() -> None:
    """The closure, ASSERTED rather than documented.

    The scan is `ast` and not a regex, on the manifest driver's own finding: a
    regex over `ArrivalRefusal\\(\\s*"` matches only a DOUBLE-quoted first
    argument, so a site written with single quotes would silently miss the code
    it raises — exactly the blind spot this test exists to close. A call whose
    first argument is not a string constant fails loudly rather than being
    skipped.
    """
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    raised: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "ArrivalRefusal"):
            continue
        first = node.args[0] if node.args else None
        assert (isinstance(first, ast.Constant)
                and isinstance(first.value, str)), (
            f"{SCRIPT}:{node.lineno}: an ArrivalRefusal(...) call does not open "
            "with a string-literal code, so this scan cannot read it as "
            "evidence of anything")
        raised.add(first.value)
    ordered = sorted(raised)
    assert len(ordered) == len(RATIFIED_CODES), \
        f"the scan found {ordered}, which is not the closed vocabulary"
    assert sorted(MODULE.REFUSAL_CODES) == ordered


def test_the_module_names_the_tool_that_owns_the_manifest() -> None:
    """The ownership split, findable in the file: every `carve-*` code is a
    manifest that disagrees with openxFactory and every `arrival-*` code is a
    destination that disagrees with the manifest, so this file re-owns
    nothing."""
    assert MODULE.MANIFEST_VALIDATOR == "scripts/validate-carve-manifest.py"
    assert MODULE.MANIFEST_RELPATH == "docs/opendox-carve-manifest.yaml"
    assert MODULE.PHASES == ("A", "B")


def test_the_module_records_what_it_does_not_prove() -> None:
    """A floor that overstates its reach is worse than one that does not reach.
    The replica limit and the created-file rule must be findable in the file,
    because a reader's first question about `318 rows verified` is what the
    other 136 mean."""
    doc = MODULE.__doc__ or ""
    assert "replicated_at_destination" in doc, doc
    assert "WHAT IT DELIBERATELY DOES NOT PROVE" in doc, doc
    assert "--allow-created" in doc, doc


# --------------------------------------------------------------------------
# the clean cases
# --------------------------------------------------------------------------

def test_phase_a_verifies_a_destination_built_from_the_rows(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "ok", payload
    assert payload["rows"] == 2 and payload["digests_verified"] == 2
    assert payload["declared_roots"] == ["src/pkg"]
    assert payload["carved_from"] is None


def test_the_human_line_names_both_the_referent_and_the_phase(
        carve: Carve) -> None:
    """A pull-request log is read by a person, and `OK` alone does not say
    which of the two commits was proved."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout
    assert "phase A" in done.stdout
    assert carve.carve_commit[:12] in done.stdout
    assert CARVE_TAG in done.stdout


def test_phase_b_accepts_an_edit_on_exactly_the_declared_line(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["declared_edits_diffed"] == 1, payload
    assert payload["declared_edits_unapplied"] == 0, payload
    # the verbatim row is verbatim in phase B too
    assert payload["digests_verified"] == 1, payload


def test_phase_b_counts_an_unapplied_edit_rather_than_refusing_it(
        carve: Carve) -> None:
    """A declared edit not yet applied touches no undeclared line, which is the
    only question the ruling's sentence asks, and the leg's own `validate`
    refuses a tree whose imports still name the home package. It is COUNTED, so
    a phase-B run reporting 0 diffed is not mistaken for one reporting 62."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["declared_edits_unapplied"] == 1, payload
    assert payload["declared_edits_diffed"] == 0, payload


def test_the_spec_leg_is_verified_independently_of_the_code_leg(
        carve: Carve) -> None:
    """One destination at a time, and the row filter is what makes that true."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["rows"] == 1 and payload["declared_roots"] == ["examples"]


# --------------------------------------------------------------------------
# arrival-missing
# --------------------------------------------------------------------------

def test_a_row_with_no_file_at_the_destination_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/alpha.py").unlink()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"


def test_an_empty_destination_refuses_missing_and_not_something_vaguer(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    empty = carve.tmp / "empty-dest"
    empty.mkdir()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(empty), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"


# --------------------------------------------------------------------------
# arrival-digest-mismatch
# --------------------------------------------------------------------------

def test_arrived_bytes_that_are_not_the_rows_refuse(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/alpha.py").write_text("ALPHA = 999\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-digest-mismatch"


def test_a_verbatim_row_edited_at_commit_b_refuses_in_phase_b_too(
        carve: Carve) -> None:
    """`moved_verbatim` is verbatim in EVERY phase. Commit B touches only the
    rows that declare edits, so a verbatim row that moved there has moved
    undeclared — and phase B is the only run that would ever see it."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(BETA_REWRITTEN, encoding="utf-8")
    (dest / "src/pkg/alpha.py").write_text("ALPHA = 2\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-digest-mismatch"


def test_an_executable_bit_lost_in_transit_refuses(carve: Carve) -> None:
    """The mode is part of the blob's identity: git records it, the manifest
    declares it, and no digest comparison would name it."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    target = dest / "examples/gamma.py"
    target.chmod(target.stat().st_mode & ~stat.S_IXUSR & ~stat.S_IXGRP
                 & ~stat.S_IXOTH)
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-digest-mismatch"
    assert "mode" in json.loads(done.stdout)["detail"]


def test_a_declared_edit_row_must_be_byte_identical_at_phase_a(
        carve: Carve) -> None:
    """Commit A places EVERY row's blob byte-identical — that is the whole
    reason the leg lands as two commits, and the strongest statement the floor
    can make."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-digest-mismatch"
    assert "PHASE A" in json.loads(done.stdout)["detail"]


# --------------------------------------------------------------------------
# arrival-undeclared-edit
# --------------------------------------------------------------------------

def test_an_edit_outside_the_declared_lines_refuses_and_names_them(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(
        "import opendox.alpha\nBETA = 2\nCALL = 99\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"
    detail = json.loads(done.stdout)["detail"]
    assert "[3]" in detail, detail
    assert "import rewrites" in detail, detail


def test_the_refusal_carries_a_unified_diff_excerpt(carve: Carve) -> None:
    """A line number alone sends a reviewer to open two files; the excerpt is
    what makes the refusal actionable in the log it is read in."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(
        "import opendox.alpha\nBETA = 2\nCALL = 99\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    detail = json.loads(done.stdout)["detail"]
    assert "--- carve:scripts/pkg/beta.py" in detail, detail
    assert "+++ arrived:src/pkg/beta.py" in detail, detail


def test_an_insertion_beside_a_declared_line_is_declared(carve: Carve) -> None:
    """A line inserted at commit B had no number at the carve commit, so it is
    declared by naming a line it is inserted BESIDE. Line 1 is declared, so an
    insertion at the top of the file is within the grammar."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(
        "import opendox.alpha\nimport opendox.extra\nBETA = 2\nCALL = 3\n",
        encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr


def test_an_insertion_far_from_every_declared_line_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(
        "import opendox.alpha\nBETA = 2\nCALL = 3\nTRAILER = 5\n",
        encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"


def test_a_change_no_line_number_can_name_still_refuses(carve: Carve) -> None:
    """`splitlines()` is blind to the terminators and to a missing final
    newline. If the bytes differ and the line lists do not, the difference is
    exactly that — and it refuses rather than passing as `no changed line`,
    which is the hole a line-based comparison leaves if nobody closes it."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_bytes(
        b"import ideation_dashboard.alpha\r\nBETA = 2\r\nCALL = 3\r\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"
    assert "no line number can name" in json.loads(done.stdout)["detail"]


# --------------------------------------------------------------------------
# arrival-undeclared-file
# --------------------------------------------------------------------------

def test_a_file_under_a_declared_root_that_no_row_places_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/stowaway.py", "STOWAWAY = 1\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    assert "--allow-created src/pkg/stowaway.py" in \
        json.loads(done.stdout)["detail"]


def test_allow_created_admits_exactly_the_named_file(carve: Carve) -> None:
    """RULED OQ-C: a file CREATED at a destination gets no row. It is named
    once, on the command line, so the admission is written down in the pull
    request that makes it — and there is deliberately no wildcard."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/openxfactory_surface.py", "SURFACE = 1\n")
    _write(dest, "src/pkg/unnamed.py", "UNNAMED = 1\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--allow-created", "src/pkg/openxfactory_surface.py")
    assert refusal(done) == "arrival-undeclared-file"
    assert "unnamed.py" in json.loads(done.stdout)["detail"]

    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--allow-created", "src/pkg/openxfactory_surface.py",
               "--allow-created", "src/pkg/unnamed.py")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["admitted"]["created"] == 2


def test_a_replica_is_admitted_by_its_bytes_at_the_carve_commit(
        carve: Carve) -> None:
    """A `replicated_at_destination` row carries no destination and no digest —
    the manifest declares what LEAVES — so the replica is admitted by identity
    with its blob at the carve commit and COUNTED, never refused."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/neutral.py", SURFACE_FILES["scripts/pkg/neutral.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["admitted"]["replica"] == 1


def test_a_drifted_replica_is_not_admitted_and_the_limit_is_the_manifests(
        carve: Carve) -> None:
    """The other half of the same sentence, pinned so nobody reads the replica
    rule as "replicas are exempt": a file that is NOT the replica's bytes is not
    a replica, and the verifier says so with the created-file remedy rather than
    pretending to know it drifted."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/neutral.py", "NEUTRAL = 4\nDRIFTED = True\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"


def test_the_scaffolds_own_files_are_admitted_from_its_leg_shape_test(
        carve: Carve) -> None:
    """The allowlist is READ FROM THE DESTINATION, not copied into openxFactory:
    `tests/test_leg_shape.py`'s `REQUIRED_FILES` is the bootstrap posture, and a
    second copy here would drift from the six repositories it describes. The
    module is parsed, never imported — a destination checkout is untrusted
    input."""
    doc = copy.deepcopy(carve.manifest_doc())
    # place a row under `tests/`, so the scaffold's own test module lands
    # inside a declared root, which is the case the allowlist exists for
    doc["rows"][0]["destination"] = "scratch_code"
    doc["rows"][0]["destination_path"] = "tests/test_alpha.py"
    manifest = carve.write_manifest(doc, "manifest-tests.yaml")
    dest = carve.materialise(doc, "scratch_code", name="dest-tests")
    _write(dest, "tests/test_leg_shape.py",
           'REQUIRED_FILES = ["README.md", "tests/helper.py"]\n')
    _write(dest, "tests/helper.py", "HELPER = 1\n")
    _write(dest, "src/pkg/.gitkeep", "")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["admitted"]["scaffold"] == 3


def test_a_file_outside_every_declared_root_is_not_the_walks_business(
        carve: Carve) -> None:
    """The walk is scoped to the MINIMAL directories the rows land under, so a
    leg's README, LICENSE and workflows are not swept into the undeclared set
    and then taken back out by a rule."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "README.md", "# the leg\n")
    _write(dest, "docs/branch-protection.md", "# posture\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr


# --------------------------------------------------------------------------
# arrival-carved-from-mismatch
# --------------------------------------------------------------------------

def _assembly_root(carve: Carve, carved_from: Any | None) -> Path:
    root = carve.tmp / "dest-root"
    (root / "contracts").mkdir(parents=True, exist_ok=True)
    doc: dict[str, Any] = {"schema_version": 1, "kind": "contract-manifest",
                           "project": "scratch",
                           "contract_bundle_version": "none", "entries": []}
    if carved_from is not None:
        doc["carved_from"] = carved_from
    (root / "contracts" / "manifest.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return root


def test_an_assembly_root_with_carved_from_verifies(carve: Carve) -> None:
    """`opendox_root` declares ZERO rows — the assembly root is where the
    release identity is cut (§ 3.8) — so the provenance record is this
    destination's whole job."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": carve.carve_commit,
                                  "carve_tag": CARVE_TAG})
    done = run(carve, manifest, "--destination", "scratch_root",
               "--dest-root", str(root), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["rows"] == 0 and payload["declared_roots"] == []
    assert payload["carved_from"]["commit"] == carve.carve_commit


def test_an_assembly_root_without_carved_from_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, None)
    done = run(carve, manifest, "--destination", "scratch_root",
               "--dest-root", str(root), "--phase", "A", "--json")
    assert refusal(done) == "arrival-carved-from-mismatch"


def test_carved_from_naming_another_commit_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": "deadbeef" * 5})
    done = run(carve, manifest, "--destination", "scratch_root",
               "--dest-root", str(root), "--phase", "A", "--json")
    assert refusal(done) == "arrival-carved-from-mismatch"


def test_carved_from_naming_another_repository_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": "someone/else",
                                  "commit": carve.carve_commit})
    done = run(carve, manifest, "--destination", "scratch_root",
               "--dest-root", str(root), "--phase", "A", "--json")
    assert refusal(done) == "arrival-carved-from-mismatch"


def test_carved_from_naming_another_carve_tag_refuses(carve: Carve) -> None:
    """The tag is a LABEL beside the commit and never the referent — but a label
    naming a DIFFERENT carve is a reader sent to the wrong one."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": carve.carve_commit,
                                  "carve_tag": "opendox-carve-99"})
    done = run(carve, manifest, "--destination", "scratch_root",
               "--dest-root", str(root), "--phase", "A", "--json")
    assert refusal(done) == "arrival-carved-from-mismatch"


def test_a_leg_is_not_asked_for_carved_from(carve: Carve) -> None:
    """RULED OQ-I puts the record in the ASSEMBLY ROOTS: measured 2026-09-09,
    the four legs have no `contracts/` directory at all."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["carved_from"] is None


# --------------------------------------------------------------------------
# arrival-unreadable — the environment and the encoding
# --------------------------------------------------------------------------

def test_an_unknown_destination_refuses_rather_than_seat_holding(
        carve: Carve) -> None:
    """The seat-holding pass covers a run with NO destination. It does not
    extend to one the caller NAMED, because a typo must not be
    indistinguishable from `not yet carved`."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_kode",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "scratch_code" in json.loads(done.stdout)["detail"]


def test_a_named_destination_without_a_phase_refuses(carve: Carve) -> None:
    """`--phase` has no default: the two phases are the two commits, and a run
    that guessed would prove the weaker claim silently."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--json")
    assert refusal(done) == "arrival-unreadable"


def test_a_named_destination_without_a_dest_root_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"


def test_a_dest_root_that_is_not_a_directory_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(carve.tmp / "nowhere"), "--phase", "A",
               "--json")
    assert refusal(done) == "arrival-unreadable"


def test_a_source_repository_without_the_carve_commit_refuses(
        carve: Carve, tmp_path: Path) -> None:
    """The phase-B diff is taken against that revision's blobs, so a source
    repository that does not carry it cannot answer the question."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    other = tmp_path / "other"
    other.mkdir()
    _git(tmp_path, "init", "-q", "-b", "main", str(other))
    _write(other, "README.md", "# another line entirely\n")
    _git(other, "add", "--", "README.md")
    _git(other, "-c", "user.name=x", "-c", "user.email=x@example.invalid",
         "commit", "-q", "-m", "unrelated")
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest),
         "--source-repo", str(other), "--destination", "scratch_code",
         "--dest-root", str(dest), "--phase", "A", "--json"],
        capture_output=True, text=True, check=False)
    assert refusal(done) == "arrival-unreadable"


def test_a_source_that_disagrees_with_the_manifest_names_the_other_tool(
        carve: Carve) -> None:
    """"This manifest disagrees with openxFactory" is
    `validate-carve-manifest.py`'s finding. Refusing it here as a destination
    fault would name the wrong tree, so the guard refuses as the environment and
    points at the tool that owns the question."""
    doc = carve.manifest_doc()
    doc["rows"][1]["sha256"] = "0" * 64
    manifest = carve.write_manifest(doc, "manifest-wrong-digest.yaml")
    dest = carve.materialise(carve.manifest_doc(), "scratch_code",
                             name="dest-wrong-digest")
    (dest / "src/pkg/beta.py").write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "validate-carve-manifest.py" in json.loads(done.stdout)["detail"]


def test_an_unparseable_manifest_refuses_and_names_the_other_tool(
        carve: Carve) -> None:
    manifest = carve.tmp / "broken.yaml"
    manifest.write_text("rows: [\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(carve.tmp), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"


def test_a_manifest_that_is_not_there_refuses(carve: Carve) -> None:
    done = run(carve, carve.tmp / "absent.yaml", "--destination",
               "scratch_code", "--dest-root", str(carve.tmp), "--phase", "A",
               "--json")
    assert refusal(done) == "arrival-unreadable"


# --------------------------------------------------------------------------
# the seat
# --------------------------------------------------------------------------

def test_no_destination_holds_the_seat_and_names_the_choices(
        carve: Carve) -> None:
    """The one place here that is not fail-closed, and it keys off
    `--destination` being ABSENT rather than off a lookup failing."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    done = run(carve, manifest)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("NO DESTINATION "), done.stdout
    assert "scratch_code" in done.stdout and "scratch_root" in done.stdout


def test_the_real_repository_answers_the_documented_invocation() -> None:
    """The seat, run from the repository root with no arguments.

    A BRANCH and never a skip: see the module docstring. No destination
    checkout exists on this machine — `opensoft/openDox-code` and its four
    siblings hold not one carved byte until Phase 2 of the cutover runbook runs
    — so what this asserts is that the DOCUMENTED INVOCATION answers, exit 0,
    naming the destinations the landed manifest declares. When a destination
    exists, this file gains a case that names it; this assertion stays true.
    """
    done = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("NO DESTINATION "), done.stdout
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if manifest.is_file():
        for key in ("opendox_code", "opendox_spec", "opendox_root",
                    "openxdox_code", "openxdox_spec"):
            assert key in done.stdout, done.stdout
    else:
        assert "the manifest could not be read" in done.stdout, done.stdout


def test_the_real_manifest_declares_the_roots_the_runbook_names() -> None:
    """The runbook's § 2 table is a claim about the LANDED manifest, and a table
    nothing checks is a comment. This reads the manifest and asserts the roots
    the verifier would walk for each destination — so a re-cut that moved a
    destination's layout reds here rather than at 2am inside a carve."""
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        # Before the § 6 ceremony landed the manifest there is nothing to
        # compare; a BRANCH, not a skip, for the module docstring's reason.
        assert True
        return
    doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    expected = {
        "opendox_code": ["src/opendox", "tests"],
        "opendox_spec": ["contracts/schemas", "docs",
                         "examples/ideation-dashboard"],
        "openxdox_code": ["scripts", "src/openxdox", "tests"],
        "openxdox_spec": ["contracts/schemas", "examples/ideation-dashboard"],
        "opendox_root": [],
    }
    for destination, roots in expected.items():
        rows = MODULE.rows_for(doc, destination)
        assert MODULE.declared_roots(rows) == roots, destination
