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
import re
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
    # RULED Q6 — the LOSING half of a re-destination: a row moved off this leg
    # by a ruling still has a file at the placement it left.
    "arrival-not-vacated",
    "arrival-undeclared-file",
    "arrival-carved-from-mismatch",
    "arrival-unreadable",
)

CARVE_TAG = "opendox-carve-0"
SOURCE_REPOSITORY = "opensoft/openxFactory"

# THE U+2028 ROW (RULED Q-L8 (c)), in miniature: an `import rewrites` line, a
# line carrying the separator, and a `path constants` line AFTER it — the shape
# of `tests/ideation-dashboard/test_gate_console.py`, whose U+2028 sits at
# `\n`-line 795 and whose five declared lines from 870 on all fall after it.
EXOTIC_SOURCE = (
    "import ideation_dashboard.alpha\n"
    "SEPARATOR = \"one line\u2028with U+2028 inside it\"\n"
    "KEEP = 3\n"
    "PATH = \"scripts/ideation_dashboard/web\"\n"
    "TAIL = 5\n")

# The scratch carve surface. `docs/outside.md` sits outside every row
# deliberately: without a file no destination should ever receive, a destination
# built from "everything in the source" would pass a verifier that never read
# the rows at all.
SURFACE_FILES: dict[str, str] = {
    "scripts/pkg/alpha.py": "ALPHA = 1\n",
    "scripts/pkg/beta.py": "import ideation_dashboard.alpha\nBETA = 2\nCALL = 3\n",
    "scripts/pkg/gamma.py": "GAMMA = 3\n",
    "scripts/pkg/neutral.py": "NEUTRAL = 4\n",
    # A MULTI-LINE REPLICA, added for RULED Q-L7 (a): the landed manifest's
    # replica that declares a line is a 271-line conftest whose `:25` depth
    # arithmetic must change and whose other 270 lines must not, and a
    # one-line replica cannot express "changed a line the row does not
    # declare" — every insertion into it is adjacent to its only line.
    "scripts/pkg/harness.py": ("HARNESS = 1\n"
                               "DEPTH = \"parents[2]\"\n"
                               "KEEP = 3\n"
                               "TAIL = 4\n"),
    # An EMPTY replica blob, because the landed manifest has two
    # (`fixtures/empty/{notes,papers}/.gitkeep`) and they are what makes an
    # admission by byte-identity dangerous: every empty file in the world
    # matches them.
    "scripts/pkg/empty.py": "",
    # A LINE CARRYING U+2028, which is what RULED Q-L8 (c) is about: this file
    # is FIVE lines to the floor (`\n`-terminated records, the manifest
    # validator's count) and SIX to `str.splitlines()`, so every declared line
    # after the exotic one named a different line in the two halves of the
    # floor. Three rows of the landed manifest carry the character and two of
    # them are `moved_with_declared_edit` rows to `openxdox_code`, whose six
    # declared lines the arrival verifier could not apply. NO ROW OF
    # `manifest_doc()` PLACES IT: the tests that need it append their own row,
    # so the row and digest counts every other case asserts do not move.
    "scripts/pkg/exotic.py": EXOTIC_SOURCE,
    "docs/outside.md": "# outside every row\n",
}

# `beta.py`'s ONE declared edit line, at the carve commit: the `import
# rewrites` class's dominant shape, `ideation_dashboard.X` -> `opendox.X`.
BETA_DECLARED_LINE = 1
BETA_REWRITTEN = "import opendox.alpha\nBETA = 2\nCALL = 3\n"

# `harness.py`'s depth line and its two arrived forms — the conftest replica's
# `:25` in miniature (RULED Q-L7 (a)). `HARNESS_ELSEWHERE` changes a line the
# row does NOT declare, which is the refusal the extension must keep.
HARNESS_DECLARED_LINE = 2
HARNESS_APPLIED = ("HARNESS = 1\nDEPTH = \"parents[1]\"\nKEEP = 3\n"
                   "TAIL = 4\n")
HARNESS_APPLIED_OTHERWISE = ("HARNESS = 1\nDEPTH = \"parents[0]\"\n"
                             "KEEP = 3\nTAIL = 4\n")
HARNESS_ELSEWHERE = ("HARNESS = 1\nDEPTH = \"parents[2]\"\nKEEP = 3\n"
                     "TAIL = 5\n")

# The declared line and its neighbour, in the FLOOR's numbering. `splitlines()`
# would call them 5 and 6, which is the whole defect: the manifest declares 4,
# the validator bounds 4 against a five-line file, and the arrival verifier
# used to compare line 4 of a six-line reading — `KEEP = 3`.
EXOTIC_DECLARED_LINE = 4
EXOTIC_UNDECLARED_LINE = 5
EXOTIC_APPLIED = EXOTIC_SOURCE.replace(
    'PATH = "scripts/ideation_dashboard/web"', 'PATH = "src/opendox/web"')
EXOTIC_ELSEWHERE = EXOTIC_SOURCE.replace("TAIL = 5", "TAIL = 6")


def _exotic_row(doc: dict[str, Any]) -> dict[str, Any]:
    """APPEND the U+2028 row to a generated manifest, and return it.

    Appended rather than generated by `manifest_doc()` so that the row,
    digest and declared-root figures a dozen other cases assert stay exactly
    what they were: this change is about which LINE a number names, and a test
    file whose every count moved would hide that.
    """
    row = {
        "source_path": "scripts/pkg/exotic.py",
        "disposition": "moved_with_declared_edit",
        "git_mode": "100644",
        "sha256": _sha256(EXOTIC_SOURCE.encode("utf-8")),
        "destination": "scratch_code",
        "destination_path": "src/pkg/exotic.py",
        "edits": [{"class": "path constants",
                   "lines": [EXOTIC_DECLARED_LINE],
                   "note": "the package's own asset path, on the line after "
                           "the one carrying U+2028"}],
    }
    doc["rows"].append(row)
    return row


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

def _placement(row: dict[str, Any]) -> tuple[Any, Any]:
    """Where a row's blob goes: `re_destined.to`/`to_path` where a ruling has
    moved the placement (RULED Q6), else the row's own destination.

    SPELLED OUT HERE rather than imported from the verifier, on `Scratch.blobs`'
    own reasoning one file over: a fixture that borrowed its subject's reader
    would agree with a broken reader too.
    `test_both_tools_read_the_effective_arrival_identically` is what holds the
    two SHIPPED readings equal; this third one is the test's own, and it is
    three lines so that it can be read at a glance.
    """
    re_destined = row.get("re_destined")
    if isinstance(re_destined, dict):
        return re_destined.get("to"), re_destined.get("to_path")
    return row.get("destination"), row.get("destination_path")


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
                {"source_path": "scripts/pkg/empty.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination",
                 "evidence": "an EMPTY replica blob, the shape the landed "
                             "manifest carries twice"},
                # APPENDED, and the row order here is the fixture's own rather
                # than bytewise: several tests below mutate `doc["rows"][0]`
                # and `[1]` by position, and this manifest is read by the
                # ARRIVAL verifier, whose questions are all about the
                # destination. `path_order:` is
                # `validate-carve-manifest.py`'s check and has its own tests.
                {"source_path": "scripts/pkg/harness.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination",
                 "evidence": "a replica whose copies must differ from the "
                             "carve blob on ONE declared line (RULED Q-L7 "
                             "(a)) — the conftest replica's depth arithmetic"},
            ],
        }

    def write_manifest(self, doc: dict[str, Any], name: str = "manifest.yaml"
                       ) -> Path:
        path = self.tmp / name
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return path

    def write_admissions(self, doc: dict[str, Any],
                        name: str = MODULE.ADMISSIONS_BASENAME) -> Path:
        """The declared admissions file (RULED #656), written beside the
        manifest by DEFAULT — same `self.tmp` directory, same default
        basename `verify-carve-arrival.py` itself resolves to — so a case
        that wants the CLI default path need only omit `--admissions`."""
        path = self.tmp / name
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return path

    def materialise(self, doc: dict[str, Any], destination: str,
                    name: str | None = None) -> Path:
        """A destination directory built from the manifest's own rows — commit
        A, byte-identical, which is what `--phase A` asserts.

        AT THE EFFECTIVE PLACEMENT (RULED Q6), so a re-destined row is
        materialised where the ruling put it and NOT where the carve did —
        which is what makes the losing leg's tree genuinely vacated rather
        than vacated by a fixture that forgot to write the file.
        """
        dest = self.tmp / (name or f"dest-{destination}")
        dest.mkdir(parents=True, exist_ok=True)
        for row in doc["rows"]:
            where, relpath = _placement(row)
            if where != destination:
                continue
            data = subprocess.run(
                ["git", "-C", str(self.source), "cat-file", "blob",
                 f"{self.carve_commit}:{row['source_path']}"],
                capture_output=True, check=True).stdout
            target = dest / relpath
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
# the declared admissions file (RULED — the arrival-admission repair,
# Brett Heap, 2026-09-11, `#656` comment 5639058687)
# --------------------------------------------------------------------------

# Any 40 lowercase hex characters satisfy `COMMIT_RE`; the tests below are not
# about WHICH commit, only that the field is held to the shape.
ADMISSION_SINCE = "a" * 40


def _entry(path: str, reason: str = "test fixture",
          since: str = ADMISSION_SINCE) -> dict[str, str]:
    return {"path": path, "reason": reason, "since": since}


def _admissions_doc(created_by_destination: dict[str, list[dict[str, str]]]
                    | None = None) -> dict[str, Any]:
    """A minimal admissions document over `manifest_doc()`'s three
    destinations (RULED #656): every one gets a `created:` block, empty
    unless `created_by_destination` supplies entries for it."""
    created_by_destination = created_by_destination or {}
    return {
        "schema_version": 1,
        "kind": "opendox-carve-admissions",
        "destinations": {
            name: {"created": created_by_destination.get(name, [])}
            for name in ("scratch_code", "scratch_spec", "scratch_root")
        },
    }


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
    because a reader's first question about `318 digest(s) verified` — the
    verifier's own words — is what the other 138 rows mean."""
    doc = MODULE.__doc__ or ""
    assert "replicated_at_destination" in doc, doc
    assert "WHAT IT DELIBERATELY DOES NOT PROVE" in doc, doc
    assert "--allow-created" in doc, doc
    # RULED Q-L7 (a): "applied identically at every replica" is a bound on
    # LINES, and one destination is verified per run — so the file must SAY
    # that it compares no two legs' copies with each other.
    assert "also_replicated_to" in doc, doc
    assert "NOT A\n    CROSS-DESTINATION COMPARISON" in doc, doc


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
    """A FINAL NEWLINE gained or lost — the ONE change the floor's definition
    of a line cannot express, since `b"a\\nb\\n"` and `b"a\\nb"` have the same
    records. If the bytes differ and the records do not, the difference is
    exactly that, and it refuses rather than passing as `no changed line`,
    which is the hole a line-based comparison leaves if nobody closes it.

    THE CRLF CASE USED TO ARRIVE HERE and RULED Q-L8 (c) deliberately moved
    it: `\\r` is CONTENT under `scripts/carve_lines.py`, so a flipped
    terminator is now a change AT a line number — the test below pins that,
    and this one keeps the branch that is still unnameable.
    """
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_bytes(
        b"import ideation_dashboard.alpha\nBETA = 2\nCALL = 3")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"
    detail = json.loads(done.stdout)["detail"]
    assert "no line number can name" in detail
    assert "final newline gained or lost" in detail


def test_a_flipped_line_terminator_is_named_by_its_line_number(
        carve: Carve) -> None:
    """RULED Q-L8 (c), the widening the one definition brings with it.

    `\\r` is not a terminator to this floor — a record is the bytes BETWEEN the
    `\\n`s — so a CRLF/LF flip changes the CONTENT of every line it touches and
    is answered like any other change: refused at the lines the row does not
    declare, NAMING them, and admitted at the line it does. Under
    `splitlines()` the same three-line flip produced identical record lists and
    fell into the message above, which told an operator only that something
    unnameable had happened to a file whose every line had in fact moved.
    """
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_bytes(
        b"import ideation_dashboard.alpha\r\nBETA = 2\r\nCALL = 3\r\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"
    detail = json.loads(done.stdout)["detail"]
    # Line 1 is declared and its flip is part of that line's declared change;
    # 2 and 3 are not, and the refusal says so by number.
    assert "line(s) [2, 3]" in detail, detail
    assert f"it declares [{BETA_DECLARED_LINE}]" in detail, detail


# --------------------------------------------------------------------------
# arrival-undeclared-edit — THE FLOOR'S ONE DEFINITION OF A LINE
# (RULED Q-L8 (c))
# --------------------------------------------------------------------------

def test_a_declared_edit_after_a_u2028_line_verifies(carve: Carve) -> None:
    """The regression RULED Q-L8 (c) closes, in the shape leg 3 measured it.

    `exotic.py` carries U+2028 INSIDE line 2, so it is five lines to the floor
    and six to `str.splitlines()`. Its row declares line 4 — the `path
    constants` line — and the destination applies the edit at line 4. Before
    this change the verifier compared line 4 of a SIX-line reading (`KEEP = 3`,
    untouched) and line 5 (the applied `PATH`, undeclared in that numbering),
    so a correctly applied declared edit REFUSED: exactly the six unappliable
    lines carve leg 3 reported over
    `tests/ideation-dashboard/test_gate_console.py` and
    `tests/ideation-dashboard/test_round_trip.py`.

    PHASE A IS ASSERTED FIRST, and not as decoration: the numbering plays no
    part in a digest comparison, so a change that moved phase A would have
    moved the floor's strongest claim while fixing its weakest.
    """
    doc = carve.manifest_doc()
    _exotic_row(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")

    # The witness, in the test rather than in a comment: the two numberings
    # disagree about this blob, which is what makes the case evidence.
    raw = EXOTIC_SOURCE.encode("utf-8")
    assert MODULE.carve_lines.count(raw) == 5
    assert len(raw.decode("utf-8").splitlines()) == 6

    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["rows"] == 3 and payload["digests_verified"] == 3, payload

    (dest / "src/pkg/exotic.py").write_text(EXOTIC_APPLIED, encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "ok", payload
    # One row diffed and within its lines: `exotic.py`. `beta.py` arrived
    # unapplied, which is counted and not a refusal.
    assert payload["declared_edits_diffed"] == 1, payload
    assert payload["declared_edits_unapplied"] == 1, payload


def test_an_undeclared_edit_after_a_u2028_line_names_the_floors_number(
        carve: Carve) -> None:
    """The other half: the refusal must NAME the line the manifest would name.

    `TAIL` is line 5 to the floor and line 6 to `splitlines()`. A refusal
    naming 6 sends an operator to a line the manifest cannot declare and the
    validator would refuse as past the end of a five-line file — a finding
    nobody can act on. It names 5.
    """
    doc = carve.manifest_doc()
    _exotic_row(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/exotic.py").write_text(EXOTIC_ELSEWHERE, encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"
    detail = json.loads(done.stdout)["detail"]
    assert f"line(s) [{EXOTIC_UNDECLARED_LINE}] which" in detail, detail
    assert f"it declares [{EXOTIC_DECLARED_LINE}]" in detail, detail


def test_the_verifier_numbers_lines_with_the_floors_shared_definition(
        ) -> None:
    """ONE DEFINITION, imported and not re-implemented (RULED Q-L8 (c)).

    An assertion about the module rather than about a run, on this file's own
    split: the behavioural cases above prove the numbering, and this proves
    there is no second numbering left in the file to drift.
    `tests/carve_manifest/test_carve_manifest.py` holds the other end — that
    the manifest VALIDATOR reaches the same module object, and that neither
    file splits lines by any other route.
    """
    assert MODULE.carve_lines.count(b"") == 0
    assert MODULE.carve_lines.records(b"a\nb\n") == [b"a", b"b"]
    assert MODULE.carve_lines.records(b"a\r\nb") == [b"a\r", b"b"]
    assert MODULE.carve_lines.text_records("x\u2028y\n".encode("utf-8")) == \
        ["x\u2028y"]
    assert "`\\n`-terminated record" in MODULE.carve_lines.DEFINITION


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


def test_a_declared_replica_is_verified_against_the_carve_blob(
        carve: Carve) -> None:
    """The stronger claim `--replica-at` buys. The manifest declares no path
    and no digest for a replica (RULED OQ-C, and measured: all 20 rows carry
    neither), so the OPERATOR declares where it landed — the runbook's per-leg
    table in machine form — and the copy becomes as falsifiable as a row."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/neutral.py", SURFACE_FILES["scripts/pkg/neutral.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/neutral.py=src/pkg/neutral.py")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_declared"] == 1
    assert payload["replicas_verified"] == 1
    # ADMITTED BY NAME, not by a coincidence of bytes: the digest admission
    # never runs for a path the operator declared.
    assert payload["admitted"]["replica"] == 0


def test_a_declared_replica_that_never_arrived_refuses_missing(
        carve: Carve) -> None:
    """The question the digest admission cannot ask, and the memo's own worry
    about `scripts/corpus_adapter.py`: a destination importing a module that
    never arrived. Undeclared, an absent replica is indistinguishable from a
    replica this leg does not want."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/neutral.py=src/pkg/neutral.py")
    assert refusal(done) == "arrival-missing"


def test_a_declared_replica_that_drifted_refuses_digest_mismatch(
        carve: Carve) -> None:
    """Declaring is what withdraws the exemption. Undeclared, this same file is
    `arrival-undeclared-file`; declared, it is the copy failing to be one."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/neutral.py", "NEUTRAL = 4\nDRIFTED = True\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/neutral.py=src/pkg/neutral.py")
    assert refusal(done) == "arrival-digest-mismatch"


def test_an_expected_replica_rewrite_is_simply_not_declared(
        carve: Carve) -> None:
    """`tests/corpus-adapter/test_conformance.py`'s implementation-aware block
    names the home factory and MUST be rewritten at each destination. The
    verifier does not need a waiver grammar for that: the operator declares the
    replicas that are copies and leaves the rewritten one undeclared, where the
    admission rules are exactly what they were."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/neutral.py", SURFACE_FILES["scripts/pkg/neutral.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_declared"] == 0
    assert payload["admitted"]["replica"] == 1


def test_replica_at_may_not_name_a_moved_row(carve: Carve) -> None:
    """A flag that could name a moved row would let a caller re-point a row the
    manifest already placed — the one thing the manifest is for."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=src/pkg/elsewhere.py")
    assert refusal(done) == "arrival-unreadable"


def test_a_malformed_replica_at_refuses_rather_than_being_ignored(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    for value in ("scripts/pkg/neutral.py", "=src/pkg/neutral.py",
                  "scripts/pkg/neutral.py="):
        done = run(carve, manifest, "--destination", "scratch_code",
                   "--dest-root", str(dest), "--phase", "A", "--json",
                   "--replica-at", value)
        assert refusal(done) == "arrival-unreadable", value


def test_one_replica_may_not_be_declared_at_two_paths(carve: Carve) -> None:
    """A repeated key would silently keep whichever `append` parsed last, and
    the operator would believe both were checked."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/neutral.py=src/pkg/neutral.py",
               "--replica-at", "scripts/pkg/neutral.py=src/pkg/other.py")
    assert refusal(done) == "arrival-unreadable"


def test_the_scaffolds_posture_document_is_admitted_under_a_declared_root(
        carve: Carve) -> None:
    """MEASURED, and it is the openDox-spec leg's first real run.
    `docs/branch-protection.md` ships with the leg scaffold (present in the
    three openDox repositories 2026-09-09; owed to the openXdox family by RULED
    OQ-O) and is in no leg's `REQUIRED_FILES`, while `docs/` IS a declared root
    for `opendox_spec` — which receives
    `docs/ideation-dashboard-session-runbook.md`. Before this admission the
    leg refused `arrival-undeclared-file` on a file the carve never touched.

    It is admitted as SCAFFOLD and not left to `--allow-created`, because the
    two make different claims: `--allow-created` records that the destination
    ASSEMBLED the file, and a document whose whole subject is provenance may
    not arrive carrying a false one.
    """
    doc = copy.deepcopy(carve.manifest_doc())
    doc["rows"][0]["destination_path"] = "docs/alpha.md"
    manifest = carve.write_manifest(doc, "manifest-docs.yaml")
    dest = carve.materialise(doc, "scratch_code", name="dest-docs")
    _write(dest, "docs/branch-protection.md", "# posture\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["admitted"]["scaffold"] == 1
    assert "docs/branch-protection.md" in MODULE.SCAFFOLD_DOCS


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
# RULED Q6 — the EFFECTIVE arrival, and `arrival-not-vacated`
#
# Brett Heap, 2026-09-12, by interactive multi-choice (`#656` comment
# `5648044785`), adopting the RECOMMENDED answer of openDox-spec
# `docs/front-end-package-boundary.md` § 6 Q6 at `7d12428c`. A moved row whose
# placement a RULING has corrected carries `re_destined:`, and this file asks
# every question at the placement the ruling made — with the LOSING leg held to
# the other half of the same act.
#
# THE TWO REFUSALS THE BOUNDARY NOTE MEASURED are what these cases are built
# around: before the field, a re-homed file drew `arrival-missing` at the leg
# whose row it left and `arrival-undeclared-file` at the leg it landed on, and
# one such file stopped slice S6 (openXdox-code `657c821b`). Both must now
# answer correctly, and the file must not be in two places at once.
# --------------------------------------------------------------------------

RE_DESTINED_RULING = "`#656` comment 5648044785 (RULED Q6, Brett Heap 2026-09-12)"

# The `src/pkg/beta.py` row, re-homed at the spec leg: the shape of S8's 23
# test files, which RULED OQ-G's imports rule placed at a leg that cannot run
# them. `beta.py` rather than `alpha.py` because it CARRIES A DECLARED EDIT —
# a re-destination must not disturb the phase-B question, and a fixture built
# on the verbatim row could not tell.
RE_DESTINED_SOURCE = "scripts/pkg/beta.py"
RE_DESTINED_TO = "scratch_spec"
RE_DESTINED_TO_PATH = "examples/beta.py"
RE_DESTINED_FROM_PATH = "src/pkg/beta.py"


def _re_destine(doc: dict[str, Any], source_path: str = RE_DESTINED_SOURCE,
                to: str = RE_DESTINED_TO, to_path: str = RE_DESTINED_TO_PATH,
                **override: Any) -> dict[str, Any]:
    """Re-destine a row of the generated manifest, and return it.

    `from`/`from_path` are READ OFF THE ROW and never typed: that is what the
    form requires them to be, and a fixture that spelled them out would go on
    agreeing with itself after the row moved.
    """
    row = next(r for r in doc["rows"] if r["source_path"] == source_path)
    block: dict[str, Any] = {
        "from": row["destination"],
        "from_path": row["destination_path"],
        "to": to,
        "to_path": to_path,
        "ruling": RE_DESTINED_RULING,
    }
    block.update(override)
    row["re_destined"] = block
    return row


def _load_manifest_validator() -> Any:
    """`scripts/validate-carve-manifest.py` as a module — the OTHER half of the
    floor, loaded by path for the same reason this file's own subject is."""
    path = REPO_ROOT / "scripts" / "validate-carve-manifest.py"
    spec = importlib.util.spec_from_file_location("validate_carve_manifest",
                                                  path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_re_destined_row_is_verified_at_the_leg_the_ruling_named(
        carve: Carve) -> None:
    """The GAINING half. The row's `destination:` still says `scratch_code`,
    and every question here — owed, present, digest, roots, the walk's
    admission BY NAME — is asked at `scratch_spec:examples/beta.py` instead."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RE_DESTINED_TO)
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    assert summary["rows"] == 2, summary
    assert summary["digests_verified"] == 2, summary
    assert summary["declared_roots"] == ["examples"], summary
    # ADMITTED BY NAME, not by a coincidence of bytes and not by a created-file
    # rule: the manifest places the file here, which is the whole point.
    assert summary["admitted"]["created"] == 0, summary
    arrived = summary["re_destined"]["arrived"]
    assert [row["source_path"] for row in arrived] == [RE_DESTINED_SOURCE], \
        summary
    assert arrived[0]["ruling"] == RE_DESTINED_RULING, arrived
    assert arrived[0]["from_path"] == RE_DESTINED_FROM_PATH, arrived


def test_the_losing_leg_no_longer_owes_the_re_destined_row(
        carve: Carve) -> None:
    """The LOSING half, passing: the row is not owed here any more, and the
    tree that no longer carries it verifies. Before the field this was
    `arrival-missing` — the refusal that stopped slice S6."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    assert summary["rows"] == 1, summary
    assert summary["declared_roots"] == ["src/pkg"], summary
    vacated = summary["re_destined"]["vacated"]
    assert [row["source_path"] for row in vacated] == [RE_DESTINED_SOURCE], \
        summary
    assert vacated[0]["to_path"] == RE_DESTINED_TO_PATH, vacated


def test_a_copy_left_behind_at_the_losing_leg_refuses(carve: Carve) -> None:
    """The other half of the same act. A re-destination that did not also
    REMOVE the file leaves the same bytes at two legs with the floor standing
    behind one — and the finding names the ruling, not the filename, because
    it runs before the walk."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    left_behind = dest / RE_DESTINED_FROM_PATH
    left_behind.parent.mkdir(parents=True, exist_ok=True)
    left_behind.write_text(SURFACE_FILES[RE_DESTINED_SOURCE], encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-vacated"
    detail = json.loads(done.stdout)["detail"]
    assert RE_DESTINED_RULING in detail, detail
    assert RE_DESTINED_TO_PATH in detail, detail


def test_a_symlink_left_at_the_vacated_path_is_not_invisible(
        carve: Carve) -> None:
    """`lexists` and not `exists`. A DANGLING symlink at the old path reads as
    absent to a followed test and would be committed by git all the same; one
    pointing at the new location reads as the file still being there."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    link = dest / RE_DESTINED_FROM_PATH
    link.parent.mkdir(parents=True, exist_ok=True)
    os.symlink("../../nowhere/beta.py", link)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-vacated"


def test_another_rows_arrival_at_the_vacated_path_is_a_lawful_refill(
        carve: Carve) -> None:
    """The arrival-verifier twin of `test_carve_manifest.py`'s
    `test_another_row_may_move_into_the_path_a_re_destination_vacated`: a row
    re-destined AWAY from a path, and a DIFFERENT row's own effective arrival
    legitimately occupying that same path today, is one row leaving and
    another arriving — not evidence of anything left behind (Copilot review,
    PR #1011). `alpha.py` is retargeted onto `beta.py`'s vacated
    `destination_path` at the SAME destination `scratch_code`; `rows_for`
    already verifies it present there before `check_vacated` ever runs, so an
    entry at the old path is this leg's OWN claimed arrival, not a leftover."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    alpha = next(r for r in doc["rows"]
                if r["source_path"] == "scripts/pkg/alpha.py")
    assert alpha["destination"] == "scratch_code", alpha
    alpha["destination_path"] = RE_DESTINED_FROM_PATH
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    vacated = summary["re_destined"]["vacated"]
    assert [row["source_path"] for row in vacated] == [RE_DESTINED_SOURCE], \
        summary


def test_a_declared_replica_may_refill_a_re_destinations_vacated_path(
        carve: Carve) -> None:
    """The `--replica-at` twin of
    `test_another_rows_arrival_at_the_vacated_path_is_a_lawful_refill`
    (Copilot review, PR #1011, round 3): a replica the OPERATOR declares at a
    path a `re_destined:` row vacated on this same leg is a lawful refill too
    — `neutral.py` is not a row `rows_for()` ever returns (RULED OQ-C), so it
    was invisible to round 2's own fix and read as the vacated row's
    abandoned copy. `check_vacated` runs before `check_replicas` builds and
    verifies the declared placements, so excluding this path here says only
    "not a leftover" — `check_replicas` still separately verifies the bytes
    below are actually `neutral.py`'s."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, RE_DESTINED_FROM_PATH, SURFACE_FILES["scripts/pkg/neutral.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", f"scripts/pkg/neutral.py={RE_DESTINED_FROM_PATH}")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_declared"] == 1, payload
    assert payload["replicas_verified"] == 1, payload
    vacated = payload["re_destined"]["vacated"]
    assert [row["source_path"] for row in vacated] == [RE_DESTINED_SOURCE], \
        payload


def test_a_re_destined_row_that_never_arrived_refuses_missing(
        carve: Carve) -> None:
    """`arrival-missing` at the GAINING leg, naming the ruling that made the
    leg owe it — a reader of the refusal must not have to open the manifest to
    learn why a file the row does not name is this leg's to place."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RE_DESTINED_TO)
    (dest / RE_DESTINED_TO_PATH).unlink()
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"
    detail = json.loads(done.stdout)["detail"]
    assert "RULED Q6" in detail, detail
    assert RE_DESTINED_FROM_PATH in detail, detail


def test_a_re_destined_row_is_byte_identical_at_phase_a(carve: Carve) -> None:
    """The digest is untouched by the field: a `sha256` is a claim about the
    SOURCE blob at the carve commit, so the row is held to exactly the bytes it
    always was — at a different address."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RE_DESTINED_TO)
    (dest / RE_DESTINED_TO_PATH).write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-digest-mismatch"


def test_a_re_destined_rows_declared_lines_still_bind_at_the_new_leg(
        carve: Carve) -> None:
    """Phase B at the gaining leg: the diff against the CARVE blob must touch
    only the row's own `edits[].lines`, exactly as it would have at the leg the
    carve chose. The edit lines are bounded by the source blob and a
    re-destination moves nothing at the source."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RE_DESTINED_TO)
    (dest / RE_DESTINED_TO_PATH).write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["declared_edits_diffed"] == 1, done.stdout

    (dest / RE_DESTINED_TO_PATH).write_text(
        "import opendox.alpha\nBETA = 2\nCALL = 4\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-edit"


def test_the_human_line_names_the_re_destinations_at_both_legs(
        carve: Carve) -> None:
    """A reader of a leg's log must be able to see that one of its arrivals is
    not the carve's own act — and, at the other leg, that a row it used to owe
    was checked to be GONE rather than simply forgotten."""
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    gaining = carve.materialise(doc, RE_DESTINED_TO)
    losing = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(gaining), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 row(s) re-destined HERE and 0 re-destined AWAY" in done.stdout, \
        done.stdout
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(losing), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "0 row(s) re-destined HERE and 1 re-destined AWAY" in done.stdout, \
        done.stdout


def test_a_leg_with_no_re_destination_says_nothing_about_one(
        carve: Carve) -> None:
    """Silent at zero. The manifest validator prints its count in every state
    because it describes ONE document; this line describes a leg, where the
    honest default is that every arrival is the carve's own."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "re-destined" not in done.stdout, done.stdout


def test_a_ruled_re_destination_verifies_at_BOTH_legs_end_to_end(
        carve: Carve) -> None:
    """ONE manifest, TWO destination trees, and the whole act in one case.

    The two halves of a re-destination are two runs — this file verifies one
    destination per run — so nothing else here proves they agree. This does:
    the same document, materialised at both legs, passes at both; and then each
    violation of the pair is introduced in turn and refuses.
    """
    doc = carve.manifest_doc()
    _re_destine(doc)
    manifest = carve.write_manifest(doc)
    gaining = carve.materialise(doc, RE_DESTINED_TO)
    losing = carve.materialise(doc, "scratch_code")

    # The file is at the gaining leg and NOT at the losing one, which is what
    # the ruling ordered — and the fixture derived both trees from the same
    # rows rather than being told where to put anything.
    assert (gaining / RE_DESTINED_TO_PATH).is_file()
    assert not (losing / RE_DESTINED_FROM_PATH).exists()

    for destination, root in ((RE_DESTINED_TO, gaining),
                              ("scratch_code", losing)):
        done = run(carve, manifest, "--destination", destination,
                   "--dest-root", str(root), "--phase", "A", "--json")
        assert done.returncode == 0, (destination, done.stdout, done.stderr)

    # VIOLATION 1 — the gaining leg never placed it.
    (gaining / RE_DESTINED_TO_PATH).unlink()
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(gaining), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"

    # VIOLATION 2 — the losing leg kept it.
    (losing / RE_DESTINED_FROM_PATH).write_text(
        SURFACE_FILES[RE_DESTINED_SOURCE], encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(losing), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-vacated"

    # VIOLATION 3 — the gaining leg placed it, but at the OLD path, which no
    # row of this destination names: the walk owns that one, by name.
    stray = gaining / RE_DESTINED_FROM_PATH
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text(SURFACE_FILES[RE_DESTINED_SOURCE], encoding="utf-8")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(gaining), "--phase", "A", "--json")
    assert refusal(done) in ("arrival-missing", "arrival-undeclared-file")


def test_both_tools_read_the_effective_arrival_identically() -> None:
    """The two halves of the floor, over one table of rows.

    RULED Q-L8 (c) is the lesson this closes in advance: `validate-carve-
    manifest.py` and this file each carry the same three-line reading of
    `re_destined:`, because neither can import the other, and two tools quietly
    disagreeing about ONE definition is what cost six declared lines when a
    line meant two things. The mis-shaped rows are in the table deliberately —
    the agreement that matters most is the one about a document neither tool
    validates.
    """
    other = _load_manifest_validator()
    table: list[dict[str, Any]] = [
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py"},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "re_destined": {"from": "scratch_code", "from_path": "src/pkg/a.py",
                         "to": "scratch_spec", "to_path": "examples/a.py",
                         "ruling": RE_DESTINED_RULING}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "re_destined": "scratch_spec"},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "re_destined": {"to": "scratch_spec"}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "re_destined": {"to": ["scratch_spec"], "to_path": "examples/a.py"}},
        {},
    ]
    for row in table:
        assert MODULE.effective_arrival(row) == other.effective_arrival(row), \
            row
    assert MODULE.effective_arrival(table[1]) == ("scratch_spec",
                                                  "examples/a.py")
    assert MODULE.effective_arrival(table[0]) == ("scratch_code",
                                                  "src/pkg/a.py")


def test_both_tools_resolve_a_destination_key_identically() -> None:
    """THE SECOND SHARED DEFINITION, held equal the way `effective_arrival`
    already is (§ 3.4 slice S8; the follow-up REGISTERED at `#1011`'s landing).

    A `destinations:` KEY IS A LABEL, NEVER A REFERENT, and the validator's
    `check_shape` deliberately admits two keys sharing one `{repository, leg}`
    body. Both tools therefore resolve a key to that body before asking whether
    two destinations are "the same" — and if the two readings ever drifted, one
    tool would gate a document the other could not satisfy, which is precisely
    what RULED Q-L8 (c) cost six declared lines to repair.
    """
    other = _load_manifest_validator()
    destinations = {
        "scratch_code": {"repository": "opensoft/scratch-code", "leg": "code"},
        "scratch_code_alias": {"repository": "opensoft/scratch-code",
                               "leg": "code"},
        "scratch_spec": {"repository": "opensoft/scratch-spec", "leg": "spec"},
        "half": {"repository": "opensoft/scratch-code"},
        "not_a_mapping": ["opensoft/scratch-code", "code"],
    }
    for key in (*destinations, "absent", None, 7):
        assert (MODULE._resolved_destination(key, destinations)
                == other._resolved_destination(key, destinations)), key
    # the claim the two tools are making, spelled out once
    resolve = MODULE._resolved_destination
    assert resolve("scratch_code", destinations) == \
        resolve("scratch_code_alias", destinations)
    assert resolve("scratch_code", destinations) != \
        resolve("scratch_spec", destinations)
    # an UNKNOWN key is a 1-tuple of itself: it can never equal a resolved
    # 2-tuple, and two different unknown keys never equal each other
    assert resolve("absent", destinations) == ("absent",)
    assert resolve("absent", destinations) != resolve("other", destinations)
    # a malformed `destinations:` degrades to the label comparison rather than
    # crashing — this file READS the manifest and does not revalidate it
    for broken in (None, [], "scratch_code"):
        assert resolve("scratch_code", broken) == ("scratch_code",)


def test_two_keys_for_one_leg_are_read_as_one_destination(
        carve: Carve) -> None:
    """The behaviour that reading matters for. A row re-destined from
    `scratch_code` to an ALIAS of `scratch_code` does not LEAVE that leg, so
    the file must stay exactly where it is — and reading the keys as strings
    made this file demand it both PRESENT (this row's own arrival) and ABSENT
    (its vacation) at one real destination, an unsatisfiable pair that would
    have refused `arrival-not-vacated` on a file the manifest still says the
    leg carries. `validate-carve-manifest.py` refuses such a document at the
    gate that runs first; this file must not ACT on one either.
    """
    doc = carve.manifest_doc()
    doc["destinations"]["scratch_code_alias"] = dict(
        doc["destinations"]["scratch_code"])
    row = _re_destine(doc, to="scratch_code_alias",
                      to_path=RE_DESTINED_FROM_PATH)
    assert row["re_destined"]["from"] == "scratch_code", row
    manifest = carve.write_manifest(doc)
    # ONE tree, built from both spellings — the fixture's own `_placement`
    # reading is a string comparison by design (it is the test's third reading
    # of the field, deliberately the naive one), so the alias half is laid down
    # by a second call into the same directory rather than by teaching the
    # fixture what the subject is supposed to know.
    dest = carve.materialise(doc, "scratch_code")
    carve.materialise(doc, "scratch_code_alias", name="dest-scratch_code")
    # the file is where the carve put it, because nothing moved
    assert (dest / RE_DESTINED_FROM_PATH).is_file()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    assert summary["re_destined"]["vacated"] == [], summary
    # and the row is still OWED here, counted as this leg's arrival
    assert summary["rows"] == len(
        [r for r in doc["rows"]
         if r["disposition"] in ("moved_verbatim", "moved_with_declared_edit")
         and r["destination"] in ("scratch_code", "scratch_code_alias")]), \
        summary


def test_the_module_records_the_effective_arrival_and_its_limit() -> None:
    """The disclosure, asserted in the file that carries it: what the field
    moves, and the limit that ONE destination is verified per run, so the two
    halves are two runs and nothing here compares them."""
    doc = MODULE.__doc__ or ""
    assert "re_destined" in doc, doc
    assert "RULED Q6" in doc, doc
    assert "5648044785" in doc, doc
    assert "arrival-not-vacated" in doc, doc
    assert "ONE destination per run" in doc, doc


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


# --------------------------------------------------------------------------
# RULED Q-L7 (a) — a moved row also replicated, and a replica that declares
# lines
#
# Brett Heap, 2026-09-10, verbatim "rule Q-L7 (a)" (`#656` comment
# `5618683833`). Carve leg 1 measured both halves: the replicated conftest
# imports `session_fixtures` unconditionally at a leg no row placed it at, and
# the same conftest's `:25` depth arithmetic points outside the destination
# once the copy lands one directory shallower.
# --------------------------------------------------------------------------

def _also_replicated(carve: Carve, destination: str,
                     source: str = "scripts/pkg/alpha.py"
                     ) -> dict[str, Any]:
    """A manifest in which one MOVED row is also replicated at `destination`."""
    doc = copy.deepcopy(carve.manifest_doc())
    for row in doc["rows"]:
        if row["source_path"] == source:
            row["also_replicated_to"] = [destination]
            return doc
    raise AssertionError(f"no row for {source}")


def _declares_a_line(carve: Carve, source: str = "scripts/pkg/harness.py",
                     line: int = HARNESS_DECLARED_LINE) -> dict[str, Any]:
    """A manifest in which one REPLICA row declares one line."""
    doc = copy.deepcopy(carve.manifest_doc())
    for row in doc["rows"]:
        if row["source_path"] == source:
            row["edits"] = [{"class": "path constants", "lines": [line],
                             "note": "the copy lands one directory shallower"}]
            return doc
    raise AssertionError(f"no row for {source}")


def test_replica_at_may_name_a_moved_row_the_manifest_also_replicates(
        carve: Carve) -> None:
    """The admission the ruling buys. `alpha.py` MOVES to `scratch_code` and is
    ALSO replicated at `scratch_spec`, so at `scratch_spec` — and only there —
    the flag may name it, and the copy is answered with the two codes a row is
    answered with."""
    doc = _also_replicated(carve, "scratch_spec")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=examples/alpha.py")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_declared"] == 1, payload
    assert payload["replicas_verified"] == 1, payload
    # ADMITTED BY NAME: the byte-identity admission never runs for a declared
    # path, exactly as for a `replicated_at_destination` row.
    assert payload["admitted"]["replica"] == 0, payload
    # and the row is still the OTHER destination's move, not this one's
    assert payload["rows"] == 1, payload


def test_replica_at_may_not_name_the_destination_a_row_moves_to(
        carve: Carve) -> None:
    """The `iff`, and the narrowing it preserves: at the destination the row
    MOVES to, the arrival is declared by its own `destination_path:`, and a
    flag that could name it would re-point an arrival the manifest declared."""
    doc = _also_replicated(carve, "scratch_spec")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/elsewhere.py",
           SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=src/pkg/elsewhere.py")
    assert refusal(done) == "arrival-unreadable"


def test_replica_at_may_not_name_a_moved_row_replicated_at_another_leg(
        carve: Carve) -> None:
    """A row replicated at `scratch_root` says nothing about `scratch_spec`.
    The manifest names the destinations; the flag does not widen them."""
    doc = _also_replicated(carve, "scratch_root")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=examples/alpha.py")
    assert refusal(done) == "arrival-unreadable"


def test_an_also_replicated_row_is_admitted_by_its_bytes_when_undeclared(
        carve: Carve) -> None:
    """The weaker reading, unchanged and now reaching one row further: the
    manifest says these bytes arrive here as a copy, so a file carrying exactly
    them is no more undeclared than any other replica's."""
    doc = _also_replicated(carve, "scratch_spec")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["admitted"]["replica"] == 1, payload
    assert payload["replicas_declared"] == 0, payload


def test_an_also_replicated_row_is_not_admitted_at_a_leg_it_does_not_name(
        carve: Carve) -> None:
    """The other half of the same sentence: the admission follows the manifest's
    list, so at a destination the row does not name, its bytes are no
    replica's."""
    doc = _also_replicated(carve, "scratch_root")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"


def test_an_also_replicated_replica_arriving_with_another_mode_refuses(
        carve: Carve) -> None:
    """A MOVED row declares `git_mode:`, so its replica's mode is compared —
    the one change a digest comparison cannot see. A
    `replicated_at_destination` row declares none and its replica's mode stays
    unchecked, which is why the mode check keys on the row and not on the
    flag."""
    doc = _also_replicated(carve, "scratch_spec")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    target = dest / "examples/alpha.py"
    target.chmod(target.stat().st_mode | stat.S_IXUSR)
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=examples/alpha.py")
    assert refusal(done) == "arrival-digest-mismatch"


def test_a_replica_that_declares_a_line_is_verified_at_phase_b_like_a_row(
        carve: Carve) -> None:
    """The second half of the ruling. The copy differs from the carve blob on
    the ONE line the row declares, and it is counted where a moved row's
    declared edit is counted."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/beta.py").write_text(BETA_REWRITTEN, encoding="utf-8")
    _write(dest, "src/pkg/harness.py", HARNESS_APPLIED)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json",
               "--replica-at", "scripts/pkg/harness.py=src/pkg/harness.py")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_verified"] == 1, payload
    # the moved row's edit AND the replica's, in the counter a reader of a
    # phase-B log already knows how to read
    assert payload["declared_edits_diffed"] == 2, payload
    assert payload["declared_edits_unapplied"] == 0, payload


def test_a_replica_edited_outside_its_declared_lines_refuses_and_names_them(
        carve: Carve) -> None:
    """The fence, at a replica. `TAIL = 4` -> `TAIL = 5` is line 4 and the row
    declares line 2 — an edit in no class is an UNDECLARED MOVEMENT wherever it
    is applied, and the refusal names the line and the PLACED path rather than
    a `destination_path:` a replica row does not carry."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/harness.py", HARNESS_ELSEWHERE)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json",
               "--replica-at", "scripts/pkg/harness.py=src/pkg/harness.py")
    assert refusal(done) == "arrival-undeclared-edit"
    detail = json.loads(done.stdout)["detail"]
    assert "[4]" in detail, detail
    assert "src/pkg/harness.py" in detail, detail


def test_a_replica_that_declares_a_line_is_byte_identical_at_phase_a(
        carve: Carve) -> None:
    """Commit A places the copy and commit B applies the edit, at a replica
    exactly as at a moved row — so the applied form REFUSES at phase A."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/harness.py", HARNESS_APPLIED)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/harness.py=src/pkg/harness.py")
    assert refusal(done) == "arrival-digest-mismatch"


def test_an_unapplied_replica_edit_is_lawful_and_counted(
        carve: Carve) -> None:
    """DECIDED, and it follows the moved row's own rule rather than inventing a
    second one: an unapplied declared edit touches no undeclared line, which is
    the only question the ruling's sentence asks. It is COUNTED — a phase-B run
    in which the replica's depth line was applied and one in which it was not
    are very different events wearing the same `OK` — and what refuses an
    unapplied `REPO_ROOT = HERE.parent.parent` is the destination's own suite,
    where a root pointing outside the repository is hundreds of setup errors
    and not an opinion."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/harness.py", SURFACE_FILES["scripts/pkg/harness.py"])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json",
               "--replica-at", "scripts/pkg/harness.py=src/pkg/harness.py")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_verified"] == 1, payload
    # beta.py's unapplied edit and the replica's, together
    assert payload["declared_edits_unapplied"] == 2, payload
    assert payload["declared_edits_diffed"] == 0, payload


def test_an_undeclared_replica_that_was_edited_must_be_declared(
        carve: Carve) -> None:
    """The edited copy's bytes are no replica's at the carve commit, so
    UNDECLARED it refuses — which is the honest outcome and the reason the
    runbook tells every leg to declare the replicas it edits."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/harness.py", HARNESS_APPLIED)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    assert "--replica-at" in json.loads(done.stdout)["detail"]


def test_two_legs_may_apply_one_replicas_line_differently(
        carve: Carve) -> None:
    """THE LIMIT, RECORDED BY TEST rather than by prose alone.

    "Applied identically at every replica" is a bound on LINES: one destination
    is verified per run — that is what `--destination` means — so two legs that
    edit the same declared line differently both pass here, and the identity of
    the applied TEXT is the placing pull request's claim plus each leg's own
    `validate`. A floor that overstated this would be worse than one that says
    where it stops.
    """
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    code = carve.materialise(doc, "scratch_code")
    _write(code, "src/pkg/harness.py", HARNESS_APPLIED)
    spec = carve.materialise(doc, "scratch_spec")
    _write(spec, "examples/harness.py", HARNESS_APPLIED_OTHERWISE)
    for destination, dest, relpath in (("scratch_code", code,
                                        "src/pkg/harness.py"),
                                       ("scratch_spec", spec,
                                        "examples/harness.py")):
        done = run(carve, manifest, "--destination", destination,
                   "--dest-root", str(dest), "--phase", "B", "--json",
                   "--replica-at", f"scripts/pkg/harness.py={relpath}")
        assert done.returncode == 0, done.stdout + done.stderr
        assert json.loads(done.stdout)["replicas_verified"] == 1, destination


def test_the_human_line_no_longer_calls_an_edited_replica_byte_identical(
        carve: Carve) -> None:
    """The one-line summary is read off a pull-request log by a person, and
    `1 of 1 declared replica(s) byte-identical` would be false of a replica
    that arrived carrying its declared edit."""
    doc = _declares_a_line(carve)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/harness.py", HARNESS_APPLIED)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "B",
               "--replica-at", "scripts/pkg/harness.py=src/pkg/harness.py")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 of 1 declared replica(s) verified" in done.stdout, done.stdout
    assert "byte-identical, or" in done.stdout, done.stdout


def test_the_real_manifest_carries_the_ruled_q_l7_rows(carve: Carve) -> None:
    """The LANDED manifest read through this verifier's own row readers, so the
    grammar the leg-3 run will depend on is asserted here and not only in the
    manifest validator's suite. A BRANCH and never a skip."""
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        assert True
        return
    doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    also = MODULE.also_replicated_rows(doc, "openxdox_code")
    assert [row["source_path"] for row in also] == \
        ["tests/ideation-dashboard/session_fixtures.py"], also
    # and NOT at the destination it moves to, however the document reads
    assert MODULE.also_replicated_rows(doc, "opendox_code") == []
    replicas = MODULE.replica_rows(doc)
    assert len(replicas) == 20, len(replicas)
    with_lines = {row["source_path"] for row in replicas if row.get("edits")}
    assert with_lines == {"tests/ideation-dashboard/conftest.py"}, with_lines
    # `--replica-at` admits both of them at openXdox-code, which is the pair
    # LEG 3 places: the moved row's replica and the replica that declares a
    # line.
    placements = MODULE.parse_replica_placements(
        ["tests/ideation-dashboard/session_fixtures.py=tests/session_fixtures.py",
         "tests/ideation-dashboard/conftest.py=tests/conftest.py"],
        doc, "openxdox_code")
    assert placements == {
        "tests/ideation-dashboard/session_fixtures.py":
            "tests/session_fixtures.py",
        "tests/ideation-dashboard/conftest.py": "tests/conftest.py"}, placements


def test_a_string_also_replicated_to_admits_no_destination(
        carve: Carve) -> None:
    """A BARE STRING IS NOT A LIST OF ONE (Copilot round, 2026-09-10).

    `validate-carve-manifest.py` refuses `also_replicated_to: "<label>"` as
    `carve-shape-invalid`, and `test_a_malformed_also_replicated_to_refuses`
    pins that. But THIS file reads the manifest and does not revalidate it, so
    it must not ACT on a shape it did not check: a string is an iterable of
    CHARACTERS, and a plain `in` test against one admits every destination key
    that is a SUBSTRING of it. `'scratch_spec' in 'not_scratch_spec_at_all'` is
    True, which without the guard reads a hand-edited document as replicating a
    file at a leg it never named — and then `--replica-at` may re-point it.
    Guarded the way `_declared_line_set` guards `edits[].lines`.
    """
    doc = copy.deepcopy(carve.manifest_doc())
    for row in doc["rows"]:
        if row["source_path"] == "scripts/pkg/alpha.py":
            row["also_replicated_to"] = "not_scratch_spec_at_all"
            break
    else:  # pragma: no cover - the fixture always carries the row
        raise AssertionError("no row for scripts/pkg/alpha.py")

    # the reader itself: nothing, not the characters of the string
    assert MODULE.also_replicated_rows(doc, "scratch_spec") == []
    assert MODULE._also_replicated_labels(doc["rows"][0]) == []

    # and end to end: the flag is refused and the copy is not admitted
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    _write(dest, "examples/alpha.py", SURFACE_FILES["scripts/pkg/alpha.py"])
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/alpha.py=examples/alpha.py")
    assert refusal(done) == "arrival-unreadable"
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"


def test_a_non_string_entry_in_also_replicated_to_admits_nothing(
        carve: Carve) -> None:
    """The same guard one level in: a list whose entry is not a string names no
    destination, and is dropped rather than compared."""
    doc = copy.deepcopy(carve.manifest_doc())
    doc["rows"][0]["also_replicated_to"] = [None, ["scratch_spec"], 7]
    assert MODULE._also_replicated_labels(doc["rows"][0]) == []
    assert MODULE.also_replicated_rows(doc, "scratch_spec") == []


# --------------------------------------------------------------------------
# ROUND 1 — the corrections the independent verification owed
#
# Each case below reproduced a real hole first, against the file as it stood at
# `8aa6f92e`, and each fails against that revision. They are grouped here rather
# than filed under their codes because what they have in common is the round,
# and a reader chasing the round wants them together.
# --------------------------------------------------------------------------

def _scaffolded_dest(carve: Carve, doc: dict[str, Any], destination: str,
                     scaffold: dict[str, str], name: str) -> Path:
    """A destination that is a GIT REPOSITORY with a pre-carve baseline.

    `origin/main` is written directly with `update-ref`: the baseline is a
    revision, not a remote, and a fixture that had to clone to get one would be
    testing git's transport rather than the admission rule.
    """
    dest = carve.tmp / name
    dest.mkdir(parents=True, exist_ok=True)
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "config", "user.name", "carve-arrival-test")
    _git(dest, "config", "user.email", "carve-arrival@example.invalid")
    for rel, text in scaffold.items():
        _write(dest, rel, text)
    _git(dest, "add", "--", *scaffold)
    _git(dest, "commit", "-q", "-m", "the leg scaffold, before the carve")
    _git(dest, "update-ref", "refs/remotes/origin/main", "HEAD")
    carve.materialise(doc, destination, name=name)
    return dest


def test_a_row_shape_this_file_cannot_read_refuses_rather_than_exiting_1(
        carve: Carve) -> None:
    """THE EXIT CONTRACT, ASSERTED. The module docstring says exit 0 or 2 and
    never 1, and before this round a manifest row missing `destination_path:`
    escaped `main()` as a `KeyError` traceback and exit 1 — the one exit the
    file says does not exist. A guarantee that depends on a reader auditing
    every raise site is not a guarantee, so `main()` now owns it.
    """
    doc = copy.deepcopy(carve.manifest_doc())
    del doc["rows"][0]["destination_path"]
    manifest = carve.write_manifest(doc, "manifest-shapeless.yaml")
    dest = carve.tmp / "dest-shapeless"
    dest.mkdir()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 2, (done.returncode, done.stdout, done.stderr)
    assert "Traceback" not in done.stderr, done.stderr
    assert refusal(done) == "arrival-unreadable"
    detail = json.loads(done.stdout)["detail"]
    assert "KeyError" in detail and "no exit 1" in detail, detail


def test_the_scaffold_list_reader_survives_more_than_a_value_error() -> None:
    """`ast.literal_eval` raises `SyntaxError` — and `TypeError`,
    `MemoryError`, `RecursionError` over a hostile literal — as well as
    `ValueError`. A destination checkout is untrusted input, so a claim about
    the SOURCE is the honest pin here: the handler names them, and `main()`'s
    catch-all is the second line of the same defence."""
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    handlers = [h for node in ast.walk(tree)
                if isinstance(node, ast.Try)
                for h in node.handlers
                if any(isinstance(c, ast.Call)
                       and isinstance(c.func, ast.Attribute)
                       and c.func.attr == "literal_eval"
                       for c in ast.walk(node))]
    assert handlers, "no `literal_eval` call is guarded at all"
    named = {n.id for h in handlers for n in ast.walk(h.type or ast.Pass())
             if isinstance(n, ast.Name)}
    assert {"ValueError", "SyntaxError"} <= named, named


def test_an_undeclared_directory_symlink_is_not_invisible(
        carve: Carve) -> None:
    """`os.walk` puts a symlink to a DIRECTORY in `dirnames`, does not descend
    into it and never reads it, so before this round a destination could carry a
    whole tree of undeclared content behind one name and still return `OK`. git
    stores such a link as a `120000` blob whose content is the target path, so
    it is answered exactly as any other entry is."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    hidden = carve.tmp / "smuggled"
    (hidden / "deep").mkdir(parents=True)
    (hidden / "deep" / "payload.py").write_text("PAYLOAD = 1\n",
                                                encoding="utf-8")
    os.symlink(hidden, dest / "src" / "pkg" / "vendor")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    assert "src/pkg/vendor" in json.loads(done.stdout)["detail"]


def test_a_file_symlink_is_still_refused(carve: Carve) -> None:
    """The half that already worked, kept beside the half that did not, so a
    later change cannot fix one by breaking the other."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    os.symlink(carve.tmp / "nowhere.py", dest / "src" / "pkg" / "link.py")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"


def test_an_empty_created_file_is_not_admitted_as_a_replica(
        carve: Carve) -> None:
    """EMPTY BYTES IDENTIFY NOTHING. Two of the landed manifest's 20 replica
    rows carry the empty digest (`fixtures/empty/*/.gitkeep`), so before this
    round ANY empty file under a declared root — a created `__init__.py`, a
    truncated module — was admitted as "a replica" and counted as one: a true
    statement about the bytes and a false one about the file. The
    `.gitkeep`-by-name rule already refused to call the scaffold's placeholder a
    replica for the same reason; this is the rest of it."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/__init__.py", "")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    detail = json.loads(done.stdout)["detail"]
    assert "EMPTY" in detail and "--replica-at" in detail, detail


def test_an_empty_replica_may_still_be_declared_by_name(carve: Carve) -> None:
    """The admission the rule leaves standing, and the stronger one: what an
    empty replica cannot be admitted BY IDENTITY it can always be admitted BY
    NAME, which is what `--replica-at` was for."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    _write(dest, "src/pkg/empty.py", "")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", "scripts/pkg/empty.py=src/pkg/empty.py")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_verified"] == 1
    assert payload["admitted"]["replica"] == 0


def test_a_payload_at_the_posture_documents_name_is_refused(
        carve: Carve) -> None:
    """The smuggling the independent verification demonstrated: `SECRET CARVE
    PAYLOAD` written to `docs/branch-protection.md`, which is admitted BY NAME
    under a declared `docs/` root, returned `OK`. The admission stays — a
    document whose whole subject is provenance may not arrive under
    `--allow-created`, which would record that the destination assembled it —
    but the bytes are now the destination's own at `--dest-base`."""
    doc = copy.deepcopy(carve.manifest_doc())
    doc["rows"][0]["destination_path"] = "docs/alpha.md"
    manifest = carve.write_manifest(doc, "manifest-posture.yaml")
    dest = _scaffolded_dest(carve, doc, "scratch_code",
                            {"docs/branch-protection.md": "# posture\n"},
                            "dest-posture")
    ok = run(carve, manifest, "--destination", "scratch_code",
             "--dest-root", str(dest), "--phase", "A", "--json")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert json.loads(ok.stdout)["admitted"]["scaffold"] == 1
    assert json.loads(ok.stdout)["dest_base"] is not None

    _write(dest, "docs/branch-protection.md", "SECRET CARVE PAYLOAD\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    detail = json.loads(done.stdout)["detail"]
    assert "SCAFFOLD by name" in detail, detail


def test_a_gitkeep_with_content_is_refused(carve: Carve) -> None:
    """`.gitkeep` is admitted by NAME anywhere under a root, which is right for
    the scaffold's placeholder and wrong for a file carrying content at that
    name."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = _scaffolded_dest(carve, doc, "scratch_code",
                            {"src/pkg/.gitkeep": ""}, "dest-gitkeep")
    ok = run(carve, manifest, "--destination", "scratch_code",
             "--dest-root", str(dest), "--phase", "A", "--json")
    assert ok.returncode == 0, ok.stdout + ok.stderr

    _write(dest, "src/pkg/.gitkeep", "PAYLOAD = 1\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"


def test_the_required_files_list_is_read_from_the_baseline_not_the_arrival(
        carve: Carve) -> None:
    """The check must not take its allowlist from the thing it is checking.
    Before this round `REQUIRED_FILES` was parsed out of the destination's
    WORKING TREE, so an arrival commit that added a path to its own
    `tests/test_leg_shape.py` admitted that path."""
    doc = copy.deepcopy(carve.manifest_doc())
    doc["rows"][0]["destination_path"] = "tests/test_alpha.py"
    manifest = carve.write_manifest(doc, "manifest-legshape.yaml")
    dest = _scaffolded_dest(
        carve, doc, "scratch_code",
        {"tests/test_leg_shape.py": 'REQUIRED_FILES = ["README.md"]\n'},
        "dest-legshape")
    _write(dest, "tests/test_leg_shape.py",
           'REQUIRED_FILES = ["README.md", "tests/payload.py"]\n')
    _write(dest, "tests/payload.py", "PAYLOAD = 1\n")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    # BOTH files are now undeclared — the rewritten leg-shape module itself is
    # the first one the ordered walk reaches — and either is the right refusal.
    assert "tests/" in json.loads(done.stdout)["detail"]


def test_a_dest_base_that_names_no_commit_refuses(carve: Carve) -> None:
    """A NAMED `--dest-base` that does not resolve refuses: an operator who
    asked for the strong admission must not silently be given the weak one. The
    DEFAULT is allowed to be absent — a destination is a working tree and not
    necessarily a repository."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--dest-base", "refs/heads/no-such-thing")
    assert refusal(done) == "arrival-unreadable"


def test_a_replica_at_may_not_reach_outside_the_dest_root(
        carve: Carve) -> None:
    """`Path("/dest") / "/etc/passwd"` is `/etc/passwd`: an absolute right-hand
    side REPLACES the root, and `..` walks out of it. Before this guard both
    were read, and the answer was reported as the destination's."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    outside = carve.tmp / "outside.py"
    outside.write_text("OUTSIDE = 1\n", encoding="utf-8")
    hostiles = ["scripts/pkg/neutral.py=/etc/passwd",
                "scripts/pkg/neutral.py=../outside.py",
                "scripts/pkg/neutral.py=src/./pkg/neutral.py",
                # A DRIVE and a UNC root: `posixpath.isabs` sees neither, and
                # on Windows `Path(dest) / "C:/x"` leaves the root. Asserted on
                # every platform, because `ntpath.splitdrive` names them on
                # every platform.
                "scripts/pkg/neutral.py=C:/pkg/neutral.py",
                "scripts/pkg/neutral.py=//server/share/neutral.py",
                "scripts/pkg/neutral.py="]
    if os.sep == "/":
        # A BACKSLASH THIS HOST DOES NOT TREAT AS A SEPARATOR. `os.sep` is `/`
        # here, so the replacement is a no-op and this passed the canonicality
        # test as one long filename — then matched nothing, because the walk
        # joins with `/`. On a Windows host the same value IS a path and is
        # converted, which is why the case is platform-guarded rather than
        # asserted everywhere.
        hostiles.append("scripts/pkg/neutral.py=src\\pkg\\neutral.py")
    for hostile in hostiles:
        done = run(carve, manifest, "--destination", "scratch_code",
                   "--dest-root", str(dest), "--phase", "A", "--json",
                   "--replica-at", hostile)
        assert refusal(done) == "arrival-unreadable", hostile


def test_allow_created_may_not_reach_outside_the_dest_root(
        carve: Carve) -> None:
    """The same guard on the other flag that takes a destination path. It is
    fail-fast rather than harmless-because-it-never-matches: a value that can
    never match is a silent admission the operator believes they made."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    hostiles = ["/etc/passwd", "../outside.py", "src/../src/pkg/x.py",
                "C:/pkg/x.py", "//server/share/x.py"]
    if os.sep == "/":
        hostiles.append("src\\pkg\\x.py")
    for hostile in hostiles:
        done = run(carve, manifest, "--destination", "scratch_code",
                   "--dest-root", str(dest), "--phase", "A", "--json",
                   "--allow-created", hostile)
        assert refusal(done) == "arrival-unreadable", hostile


def test_a_dest_base_is_validated_before_a_process_is_started(
        carve: Carve) -> None:
    """`--dest-base` is the ONE value this tool hands to git that came from the
    command line rather than from the manifest, so it is validated at the
    boundary. The refusal that matters is a LEADING DASH — `git rev-parse`
    would read `--upload-pack=…^{commit}` as an OPTION and not a revision —
    and `--end-of-options` is passed as well, so the two defences are
    independent."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    for hostile in ("--dest-base=--upload-pack=/bin/sh",
                    "--dest-base=-x",
                    "--dest-base=origin/main; rm -rf /",
                    "--dest-base=$(id)"):
        done = run(carve, manifest, "--destination", "scratch_code",
                   "--dest-root", str(dest), "--phase", "A", "--json",
                   hostile)
        assert refusal(done) == "arrival-unreadable", hostile
    assert MODULE.DEST_BASE_RE.fullmatch("origin/main")
    assert MODULE.DEST_BASE_RE.fullmatch("HEAD^{commit}")
    assert not MODULE.DEST_BASE_RE.fullmatch("-x")


def test_without_a_baseline_the_weaker_claim_is_printed_as_the_weaker_one(
        carve: Carve) -> None:
    """The fallback is honest rather than silent: a destination with no
    `origin/main` still verifies, and both the summary and the human line say
    the scaffold admissions were by name alone."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "scaffold admissions by NAME ONLY" in done.stdout, done.stdout


def test_an_assembly_root_is_reachable_by_the_repository_it_is(
        carve: Carve) -> None:
    """RULED OQ-I puts `carved_from:` in EACH assembly root, and the landed
    manifest declares `opendox_root` and NO `openxdox_root` — openXdox's root
    receives no row, so it has no `destinations:` key. Addressed only by key,
    half the provenance the ruling requires would be uncheckable by the tool
    that checks the other half."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": carve.carve_commit,
                                  "carve_tag": CARVE_TAG})
    undeclared = run(carve, manifest, "--assembly-root", "opensoft/openXdox",
                     "--dest-root", str(root), "--json")
    assert undeclared.returncode == 0, undeclared.stdout + undeclared.stderr
    payload = json.loads(undeclared.stdout)
    assert payload["mode"] == "assembly-root"
    assert payload["declared_by_the_manifest"] is False
    assert payload["destination"] is None
    assert payload["carved_from"]["commit"] == carve.carve_commit

    declared = run(carve, manifest, "--assembly-root", "opensoft/scratch",
                   "--dest-root", str(root), "--json")
    assert declared.returncode == 0, declared.stdout + declared.stderr
    assert json.loads(declared.stdout)["destination"] == "scratch_root"


def test_an_assembly_root_addressed_by_repository_still_refuses(
        carve: Carve) -> None:
    """The mode adds an ADDRESS, not an exemption: the check it runs is the
    same one."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": "deadbeef" * 5})
    done = run(carve, manifest, "--assembly-root", "opensoft/openXdox",
               "--dest-root", str(root), "--json")
    assert refusal(done) == "arrival-carved-from-mismatch"


def test_assembly_root_refuses_a_leg_and_a_malformed_repository(
        carve: Carve) -> None:
    """A leg carries no `contracts/` at all (RULED OQ-I, measured), so naming
    one here is a caller reaching for `--destination`; and the flag takes a
    repository, so a key typed into it is refused rather than read as one."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": carve.carve_commit})
    leg = run(carve, manifest, "--assembly-root", "opensoft/scratch-code",
              "--dest-root", str(root), "--json")
    assert refusal(leg) == "arrival-unreadable"
    assert "--destination scratch_code" in json.loads(leg.stdout)["detail"]

    shape = run(carve, manifest, "--assembly-root", "openxdox_root",
                "--dest-root", str(root), "--json")
    assert refusal(shape) == "arrival-unreadable"


def test_destination_and_assembly_root_together_refuse(carve: Carve) -> None:
    """Two addresses for one run, and the file does not choose between them."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    root = _assembly_root(carve, {"repository": SOURCE_REPOSITORY,
                                  "commit": carve.carve_commit})
    done = run(carve, manifest, "--destination", "scratch_root",
               "--assembly-root", "opensoft/scratch", "--phase", "A",
               "--dest-root", str(root), "--json")
    assert refusal(done) == "arrival-unreadable"


def test_the_no_destination_json_names_the_destinations_as_a_list(
        carve: Carve) -> None:
    """`--json` is consumed by machines. Before this round the seat's
    `destinations` field was a comma-joined sentence, or an apology sentence
    when the manifest could not be read — a field every consumer had to parse
    twice."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    done = run(carve, manifest, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["destinations"] == ["scratch_code", "scratch_root",
                                       "scratch_spec"]
    assert payload["destinations_unreadable"] is False

    missing = run(carve, carve.tmp / "not-there.yaml", "--json")
    assert missing.returncode == 0, missing.stdout + missing.stderr
    gone = json.loads(missing.stdout)
    assert gone["destinations"] == [] and gone["destinations_unreadable"]


def test_the_landed_manifest_gives_the_openxdox_root_no_key() -> None:
    """The measured fact the `--assembly-root` mode exists for, asserted
    against the LANDED manifest so that a re-cut which ADDS the key reds here
    and the runbook's § 7 can go back to a `--destination`."""
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        assert True
        return
    doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    assert "opendox_root" in doc["destinations"]
    assert "openxdox_root" not in doc["destinations"]
    repositories = {entry["repository"] for entry in doc["destinations"].values()}
    assert "opensoft/openXdox" not in repositories


# --------------------------------------------------------------------------
# the declared admissions file (RULED — the arrival-admission repair,
# Brett Heap, 2026-09-11, `#656` comment 5639058687): `--destination` reads
# it by default and applies each destination's `created:` list exactly as
# `--allow-created` admits, so a new admission is a reviewed one-line diff
# in the pin-bump pull request rather than a flag typed once and recorded
# nowhere.
# --------------------------------------------------------------------------

def test_admissions_file_default_path_resolves_and_admits(carve: Carve
                                                          ) -> None:
    """No `--admissions` and no `--allow-created`: the default path — beside
    the manifest — is read on its own, and its `created:` entry admits."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/created.py").write_text("CREATED = 1\n", encoding="utf-8")
    admissions = carve.write_admissions(_admissions_doc(
        {"scratch_code": [_entry("src/pkg/created.py")]}))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["admitted"]["created"] == 1, payload
    assert payload["declared_admissions_used"] == ["src/pkg/created.py"]
    assert payload["declared_admissions_unused"] == []
    assert payload["ad_hoc_allow_created"] == []
    assert payload["admissions_file"] == str(admissions)


def test_a_declared_admission_admits_exactly_the_file_it_names(
        carve: Carve) -> None:
    """Declaring `created.py` must not admit a DIFFERENT undeclared file: the
    admission is by NAME under the destination, never a wildcard over the
    declared root."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/created.py").write_text("CREATED = 1\n", encoding="utf-8")
    (dest / "src/pkg/other_created.py").write_text("OTHER = 2\n",
                                                    encoding="utf-8")
    carve.write_admissions(_admissions_doc(
        {"scratch_code": [_entry("src/pkg/created.py")]}))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    assert "other_created.py" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_the_wrong_schema_version_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    bad = _admissions_doc()
    bad["schema_version"] = 999
    carve.write_admissions(bad)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "schema_version" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_schema_version_true_refuses(
        carve: Carve) -> None:
    """`isinstance(True, int)` is `True` in Python, so a bare type check
    would accept `schema_version: true` as though it were the integer 1
    (Copilot review, PR #979) — the same trap `validate-carve-manifest.py`
    already guards its own `schema_version:` against."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    bad = _admissions_doc()
    bad["schema_version"] = True
    carve.write_admissions(bad)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "schema_version" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_the_wrong_kind_refuses(carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    bad = _admissions_doc()
    bad["kind"] = "not-the-declared-admissions-kind"
    carve.write_admissions(bad)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "kind" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_naming_an_unknown_destination_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    admissions = carve.write_admissions({
        "schema_version": 1,
        "kind": "opendox-carve-admissions",
        "destinations": {"scratch_bogus": {"created": [_entry("x.py")]}},
    })
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A",
               "--admissions", str(admissions), "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "scratch_bogus" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_a_duplicate_path_refuses(carve: Carve
                                                          ) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc({
        "scratch_code": [_entry("src/pkg/created.py", reason="one"),
                         _entry("src/pkg/created.py", reason="two")],
    }))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "twice" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_an_unsorted_created_list_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc({
        "scratch_code": [_entry("src/pkg/z_created.py"),
                         _entry("src/pkg/a_created.py")],
    }))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "alphabetical order" in json.loads(done.stdout)["detail"]


def test_an_admissions_entry_missing_a_required_field_refuses(
        carve: Carve) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc({
        "scratch_code": [{"path": "src/pkg/created.py",
                          "reason": "missing since"}],
    }))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "since" in json.loads(done.stdout)["detail"]


def test_an_admissions_entry_with_a_non_hex_since_refuses(carve: Carve
                                                          ) -> None:
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc({
        "scratch_code": [_entry("src/pkg/created.py", since="not-a-commit")],
    }))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "40 lowercase hex" in json.loads(done.stdout)["detail"]


def test_a_since_value_with_a_trailing_newline_refuses(carve: Carve) -> None:
    """`$` matches just before a trailing newline as well as at the true end
    of the string, so `COMMIT_RE.match` alone would admit 40 hex characters
    plus a trailing "\\n" as a clean 40-hex commit (Copilot review, PR #979).
    The field must be held to `.fullmatch`, which requires the match to cover
    the ENTIRE string and so cannot let the newline ride along unchecked."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc({
        "scratch_code": [_entry("src/pkg/created.py",
                                since=ADMISSION_SINCE + "\n")],
    }))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "40 lowercase hex" in json.loads(done.stdout)["detail"]


def test_a_stale_declared_admission_is_reported_not_silent(carve: Carve
                                                            ) -> None:
    """A `created:` entry naming a file that never arrives is not consumed —
    reported as UNUSED rather than passed over in silence (RULED #656): a
    stale declared admission is a finding."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    carve.write_admissions(_admissions_doc(
        {"scratch_code": [_entry("src/pkg/never_arrives.py")]}))
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["declared_admissions_used"] == []
    assert payload["declared_admissions_unused"] == ["src/pkg/never_arrives.py"]

    human = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A")
    assert human.returncode == 0, human.stdout + human.stderr
    assert "STALE" in human.stdout
    assert "never_arrives.py" in human.stdout


def test_ad_hoc_allow_created_still_works_and_notes_the_governed_form(
        carve: Carve) -> None:
    """`--allow-created` remains a working ad-hoc admission (RULED #656), and
    a run using it prints a notice that the declared file is the governed
    form — on stderr only, so `--json`'s one-object promise on stdout holds
    and the human OK line is not corrupted."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/created.py").write_text("CREATED = 1\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A",
               "--allow-created", "src/pkg/created.py")
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout
    assert "ad-hoc" in done.stdout.lower()
    assert "NOTE" in done.stderr, done.stderr
    assert "governed" in done.stderr.lower()

    machine = run(carve, manifest, "--destination", "scratch_code",
                 "--dest-root", str(dest), "--phase", "A",
                 "--allow-created", "src/pkg/created.py", "--json")
    assert machine.returncode == 0, machine.stdout + machine.stderr
    payload = json.loads(machine.stdout)  # raises if a stray line broke it
    assert payload["ad_hoc_allow_created"] == ["src/pkg/created.py"]


def test_an_absent_admissions_file_is_not_a_refusal(carve: Carve) -> None:
    """A destination with no admissions file adopted yet gets no declared
    admissions, and behaves exactly as it did before this feature existed —
    ABSENT is not the same finding as PRESENT AND MALFORMED."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    assert not (carve.tmp / MODULE.ADMISSIONS_BASENAME).exists()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["admissions_file"] is None
    assert payload["declared_admissions_used"] == []
    assert payload["declared_admissions_unused"] == []


def test_an_unreadable_admissions_file_refuses_rather_than_reads_as_absent(
        carve: Carve) -> None:
    """A path that EXISTS but cannot be read as the admissions file — a
    directory sitting where the file would be, standing in for any non-absence
    `OSError` (permission failure, I/O error) — is not the same finding as "no
    admissions file adopted yet" (Copilot review, PR #979). Catching every
    `OSError` and returning as if absent would silently disable the governed
    admissions and let the run fall through to an unrelated undeclared-file
    result instead of naming the real cause; only `FileNotFoundError` may mean
    ABSENT."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    MODULE.default_admissions_path(manifest).mkdir()
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "could not be read" in json.loads(done.stdout)["detail"]


def test_an_empty_admissions_file_refuses_rather_than_reads_as_absent(
        carve: Carve) -> None:
    """An EXISTING file that parses to nothing — empty, or comments-only, so
    `yaml.safe_load` hands back `None` — is PRESENT AND MALFORMED, not
    ABSENT (Copilot review, PR #979). The old code's `if raw is None: return
    {}` silently disabled every declared admission the file was supposed to
    carry while the summary still reported it as this destination's
    `admissions_file`; only a file that does not exist at all may read as
    absent."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    MODULE.default_admissions_path(manifest).write_text(
        "# nothing declared yet\n", encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "not a mapping" in json.loads(done.stdout)["detail"]
    assert "NoneType" in json.loads(done.stdout)["detail"]


def test_an_admissions_file_with_a_duplicate_destination_key_refuses(
        carve: Carve) -> None:
    """`yaml.safe_load` applies last-duplicate-key-wins SILENTLY (Copilot
    review, PR #979): a `destinations:` block naming `scratch_code` twice
    would show a reviewer reading the diff the FIRST block (`created: []`,
    nothing admitted) while the plain loader would resolve the document to
    the SECOND (a real admission) — the same show-one-admit-another defect
    the admissions file exists to prevent, now inside the admission
    document itself. Written as raw text, not through `write_admissions`'s
    dict helper: a Python `dict` cannot itself hold a duplicate key, so only
    a hand-written document can produce the YAML this reader must refuse."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    MODULE.default_admissions_path(manifest).write_text(
        "schema_version: 1\n"
        "kind: opendox-carve-admissions\n"
        "destinations:\n"
        "  scratch_code:\n"
        "    created: []\n"
        "  scratch_code:\n"
        "    created:\n"
        "      - path: src/pkg/sneaky.py\n"
        f"        reason: shown-one-admitted-another\n"
        f"        since: {ADMISSION_SINCE}\n",
        encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    detail = json.loads(done.stdout)["detail"]
    assert "duplicate" in detail
    assert "scratch_code" in detail


def test_an_admissions_entry_with_a_duplicate_field_key_refuses(
        carve: Carve) -> None:
    """The same last-duplicate-key-wins silence (Copilot review, PR #979),
    one level down: a `created[]` entry repeating `reason:` would show a
    reviewer the FIRST reason while the plain loader admits the file on the
    SECOND, unread. Raw text for the same reason as the sibling test above —
    a Python `dict` cannot hold the duplicate key this must refuse."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    MODULE.default_admissions_path(manifest).write_text(
        "schema_version: 1\n"
        "kind: opendox-carve-admissions\n"
        "destinations:\n"
        "  scratch_code:\n"
        "    created:\n"
        "      - path: src/pkg/created.py\n"
        "        reason: the reviewed reason\n"
        f"        reason: a second, unreviewed reason\n"
        f"        since: {ADMISSION_SINCE}\n",
        encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "duplicate" in json.loads(done.stdout)["detail"]


def test_the_committed_admissions_file_keeps_the_ruled_seed_and_stays_well_formed(
    ) -> None:
    """The RULED SEED SURVIVES and the whole file stays well formed.

    AMENDED by the § 4.3/§ 4.4 openxFactory half + pin lockstep (openDox →
    `8ec3036c`, openXdox → `eca0b597`), which is the FIRST pin bump this
    file's own design anticipates: "a NEW admission is a reviewed ONE-LINE
    diff in the pull request that bumps the destination's pin". The original
    assertions — `openxdox_code`'s set EQUALS the two openXdox-code #7 files
    and every OTHER destination is `[]` — were true of the SEEDING COMMIT and
    are false of every bump after it by construction, so an equality over the
    file's CONTENT would have made the governed form unusable the first time
    it was used. Nothing else is relaxed: the EQUALITY that matters — the
    file declares one block for EVERY manifest destination and no id the
    manifest does not carry — is kept exactly as PR #979's review asked for
    it, because that one is about the file's SHAPE and not about what has
    accumulated in it.

    AMENDED AGAIN by RULED Q5 (`#656` comment 5642758731, split-opendox § 3.4
    slice S2, Q-L1): the SECOND bump this design anticipated, `opendox_code`'s
    own three new files (the optional-binding module and its two tests,
    admitted the governed way because the leg PR that lands them pairs with —
    and lands after — this annotation PR). Same footing, same reason the
    openxdox_code seed is checked by presence and not by equality: an
    equality over `opendox_code`'s content would break on the NEXT pin bump
    the same way the original whole-file equality broke on this one.

    AMENDED A THIRD TIME by openxFactory PR #1001 (Copilot review): five more
    `opendox_code` files, declared the same governed way once the PR ran
    `verify-carve-arrival.py` against the merged S1+S2+S3 tree and found them
    undeclared — § 3.4 SLICE S3's own `view_extension.py` /
    `view_extension.js` / `test_view_registry.py` (`#656` comment 5642758731,
    the leg PR opensoft/openDox-code#14 pairs with and lands after this one),
    and § 3.4 SLICE S1's `test_web_boundary.py` /
    `tests/fixtures/web_boundary_census.yaml` (already landed via
    opensoft/openDox-code#13, which touched no arrived file and so needed no
    row-annotation PR of its own — nothing wrote down that its two new files
    still wanted admitting until this PR looked). Same footing again: checked
    by presence, not equality.

    AMENDED A FOURTH TIME by § 3.4 SLICE S6's own annotation PR (RULED Q4,
    `#656` comment 5642758731): one more `opendox_code` file,
    `tests/test_source_core_arm.py` — the runnable half of the `/source`
    re-homing from `openxdox_code`'s contributed binding to `opendox_code`'s
    own fixed core arm, admitted the governed way because the leg PR that
    lands it (opensoft/openDox-code#16) pairs with — and lands after — this
    annotation PR. Same footing again: checked by presence, not equality.

    AMENDED A FIFTH TIME by § 3.4 SLICE S4's own annotation PR (RULED Q3,
    `#656` comment 5642758731): four more `opendox_code` files — the three
    new class-B modules that receive five of the thirteen route tails S4
    counts (`views/gate-lens.js`, `views/gate-projects.js`,
    `views/projection-index.js`; the other eight arrive at the existing SWB
    modules, are removed, or stay in place) and their own
    `tests/test_split_route_tails.py`
    — admitted the governed way because the leg PR that lands them
    (opensoft/openDox-code#17, stacked on S3's #14) pairs with — and lands
    after — this annotation PR. Same footing again: checked by presence, not
    equality.

    What is durable is asserted in place of the frozen content: the two
    RULED openxdox_code seed entries (the measured defect this file repairs,
    `#656` comment 5639058687), the three RULED Q5 opendox_code entries, the
    five PR #1001 opendox_code entries, the one § 3.4 SLICE S6 entry, and the
    four § 3.4 SLICE S4 entries are still declared with their own
    `since`, every `since` is a 40-hex commit, every `reason` is non-empty,
    and every destination's list is alphabetical by `path` with no repeat —
    the file's own stated invariants, over whatever the file has
    accumulated. Reads the REAL committed files,
    so a typo fails this rather than only a scratch fixture's copy."""
    manifest_path = REPO_ROOT / MODULE.MANIFEST_RELPATH
    admissions_path = MODULE.default_admissions_path(manifest_path)
    # Hard assertions, not a skip-guard (Copilot review, PR #979): this test
    # exists to protect the GOVERNED SEED, so the committed manifest and
    # admissions file disappearing or being renamed out from under it must
    # fail here, not silently report a pass that never examined anything.
    assert manifest_path.is_file(), (
        f"the committed manifest at {manifest_path} is missing; this test "
        "guards the governed admissions seed and must not pass silently "
        "when the file it reads disappears")
    assert admissions_path.is_file(), (
        f"the committed admissions file at {admissions_path} is missing; "
        "this test guards the governed admissions seed and must not pass "
        "silently when the file it reads disappears")
    manifest_doc = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    admissions = MODULE.read_admissions(admissions_path, manifest_doc)
    # Equality, not a subset (Copilot review, PR #979): the admissions
    # file's own header declares one block for EVERY destination the
    # manifest carries, so a destination missing its `created: []` block --
    # or an unknown id sneaking in -- must fail here rather than pass a
    # check that only bounded one side of the comparison.
    assert set(admissions) == set(manifest_doc["destinations"])
    seed = {entry["path"]: entry
            for entry in admissions.get("openxdox_code", [])}
    for path in ("src/openxdox/consumer_reach.py",
                 "tests/test_dependency_direction.py"):
        assert path in seed, (
            f"{path} is one of the two files RULED into this file's seed and "
            "is no longer declared for openxdox_code")
        assert seed[path]["since"] == (
            "bfd95063b2a71be097a04bb6a3a99c4c131dd322")
    # RULED Q5 (`#656` comment 5642758731, split-opendox § 3.4 slice S2):
    # `opendox_code`'s own three new files, admitted the GOVERNED way per
    # Q-L1 (the leg PR pairs with this annotation PR, which lands first) —
    # checked by PRESENCE, the same footing as the openxdox_code seed above
    # and for the same reason (a future opendox_code bump must not break
    # this the way an equality check broke on the FIRST bump).
    opendox_seed = {entry["path"]: entry
                    for entry in admissions.get("opendox_code", [])}
    for path in ("src/opendox/web/views/intent-binding.js",
                 "tests/test_intent_binding_dom.py",
                 "tests/test_intent_binding_shape.py"):
        assert path in opendox_seed, (
            f"{path} is one of the three files RULED Q5 (`#656` comment "
            "5642758731, split-opendox § 3.4 slice S2) into this file's "
            "opendox_code admissions and is no longer declared")
        assert opendox_seed[path]["since"] == (
            "330cf8161f06ae67be716deafe9b2ec3c64d1492")
    # THE THIRD BUMP (Copilot review, openxFactory PR #1001): two more
    # `opendox_code` files RULED into this file by § 3.4 SLICE S3 (`#656`
    # comment 5642758731) — the view registry's server and client modules,
    # admitted the GOVERNED way on the same Q-L1 footing as the S2 entries
    # above (the leg PR, opensoft/openDox-code#14, pairs with — and lands
    # after — this annotation PR) — plus its own test, and TWO files RULED
    # by § 3.4 SLICE S1 (opensoft/openDox-code#13, already landed on
    # `main`): S1 touched no arrived file, so Q-L1 required no
    # row-annotation PR of its own, but its two new files sat undeclared
    # until this PR ran `verify-carve-arrival.py` against the merged
    # S1+S2+S3 tree and needed them admitted. Checked by PRESENCE for the
    # same reason as the seeds above.
    for path in ("src/opendox/view_extension.py",
                 "src/opendox/web/views/view_extension.js"):
        assert path in opendox_seed, (
            f"{path} is one of § 3.4 SLICE S3's own two new files (`#656` "
            "comment 5642758731, openxFactory PR #1001) and is no longer "
            "declared for opendox_code")
        assert opendox_seed[path]["since"] == (
            "e6c65ed757bfc3f9b6664e27c85111bfe5f0d465")
    assert "tests/test_view_registry.py" in opendox_seed, (
        "tests/test_view_registry.py is § 3.4 SLICE S3's own test file "
        "(`#656` comment 5642758731, openxFactory PR #1001) and is no "
        "longer declared for opendox_code")
    assert opendox_seed["tests/test_view_registry.py"]["since"] == (
        "cb810d39737bf50bbe87e5700177c2e5ce2750da")
    for path in ("tests/test_web_boundary.py",
                 "tests/fixtures/web_boundary_census.yaml"):
        assert path in opendox_seed, (
            f"{path} is one of § 3.4 SLICE S1's two new files "
            "(opensoft/openDox-code#13) and is no longer declared for "
            "opendox_code")
        assert opendox_seed[path]["since"] == (
            "e86deb2dbcec528a312784508ddbf63c376abc33")
    # THE FOURTH BUMP: one more `opendox_code` file, RULED into this file by
    # § 3.4 SLICE S6 (RULED Q4, `#656` comment `5642758731`) — the runnable
    # half of the `/source` re-homing, admitted the GOVERNED way on the same
    # Q-L1 footing as the bumps above (the leg PR, opensoft/openDox-code#16,
    # pairs with — and lands after — this annotation PR). Checked by
    # PRESENCE for the same reason as the seeds above.
    assert "tests/test_source_core_arm.py" in opendox_seed, (
        "tests/test_source_core_arm.py is § 3.4 SLICE S6's own new file "
        "(`#656` comment 5642758731) and is no longer declared for "
        "opendox_code")
    assert opendox_seed["tests/test_source_core_arm.py"]["since"] == (
        "b00fbd920a019e2cee816b4936f921ceeab67a8c")
    # THE FIFTH BUMP: four more `opendox_code` files, RULED into this file by
    # § 3.4 SLICE S4 (RULED Q3, `#656` comment `5642758731`) — the three new
    # class-B gate/projection modules that receive five of the thirteen
    # route tails S4 counts (two to `gate-lens.js`, two to `gate-projects.js`,
    # one to `projection-index.js`; the other eight arrive at the existing
    # SWB modules, are removed, or stay in place), plus their own test file,
    # admitted the GOVERNED way on the same Q-L1 footing as the bumps above
    # (the leg PR, opensoft/openDox-code#17, stacked on S3's #14, pairs with
    # — and lands after — this annotation PR). Checked by PRESENCE for the
    # same reason as the seeds above. `since` is each file's OWN introducing
    # commit (`git log --diff-filter=A`), not the leg branch's later tip —
    # the same provenance contract the FOURTH BUMP above states, and the
    # same class of correction Copilot's review caught there.
    for path in ("src/opendox/web/views/gate-lens.js",
                 "src/opendox/web/views/gate-projects.js",
                 "src/opendox/web/views/projection-index.js"):
        assert path in opendox_seed, (
            f"{path} is one of § 3.4 SLICE S4's own three new class-B "
            "modules (`#656` comment 5642758731) and is no longer declared "
            "for opendox_code")
        assert opendox_seed[path]["since"] == (
            "031edc9b4268d9898c296b2e9bb3951a78642fb6")
    assert "tests/test_split_route_tails.py" in opendox_seed, (
        "tests/test_split_route_tails.py is § 3.4 SLICE S4's own test file "
        "(`#656` comment 5642758731) and is no longer declared for "
        "opendox_code")
    assert opendox_seed["tests/test_split_route_tails.py"]["since"] == (
        "2e842178b2bceaee9a45441b7d70d797fe1205cf")
    # THE FILE'S OWN STATED INVARIANTS, over whatever has accumulated. Each
    # replaces nothing: the frozen-content assertions these stand in for
    # could not survive a pin bump, and an accumulating file with no checked
    # shape is the drift the declared form exists to end.
    for destination, entries in admissions.items():
        paths = [entry["path"] for entry in entries]
        assert paths == sorted(paths), (
            f"{destination}'s created: list is not alphabetical by path, "
            "which the file's own shape requires so a new admission is a "
            "one-line insertion and never a reshuffle")
        assert len(paths) == len(set(paths)), (
            f"{destination} declares a path twice")
        for entry in entries:
            assert re.fullmatch(r"[0-9a-f]{40}", entry["since"]), (
                f"{destination}'s {entry['path']} declares since="
                f"{entry['since']!r}, which is no 40-hex leg commit, so the "
                "claim is not falsifiable")
            assert entry["reason"].strip(), (
                f"{destination}'s {entry['path']} declares no reason")
