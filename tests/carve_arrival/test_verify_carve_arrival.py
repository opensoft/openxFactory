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

THE SEVEN TESTS THAT READ THE LANDED MANIFEST DO NOT BRANCH ON IT (amended on
a Copilot finding, `#1030`, the round after the same finding closed in
`tests/carve_manifest/test_carve_manifest.py`; the COUNT re-read on round
eleven of the same review, which found this paragraph still saying FIVE two
tests later). They had taken the seat above for a DIFFERENT absence than the
one it describes — `if not manifest.is_file(): assert True; return` — and
`assert True` REPORTS A PASS, the same green bar the paragraph above refuses a
skip for, so a checkout that had lost `docs/opendox-carve-manifest.yaml`
turned four pins on the landed document into four no-ops and passed the fifth
— the five that existed then — on the verifier's apology line instead of its
answer. The § 6 ceremony has happened: the manifest is committed, and there is
no revision these seven can run at without it. They read it through
`the_landed_manifest()`, where the absence is a FAILURE, and the NUMBER above
is counted rather than transcribed:
`test_the_module_docstring_counts_the_tests_that_read_the_landed_manifest`
re-counts the call sites in this file and holds this paragraph to them,
because a paragraph that states its own coverage is a claim like any other.
The absent manifest is pinned where a claim about it belongs — hermetically,
on a path the test controls: `test_a_manifest_that_is_not_there_refuses` and
the `--json` seat's `destinations_unreadable`.

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
import shlex
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
    # RULED 5656343213 — the RETIREMENT's own finding: a row whose `retired:`
    # block says a ruling DELETED its arrival at this leg still has a file at
    # `retired.at_path`.
    "arrival-not-retired",
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


def _retirement(row: dict[str, Any]) -> tuple[Any, Any]:
    """Where a RULING has DELETED this row's arrival (RULED 5656343213), or
    `(None, None)`.

    SPELLED OUT HERE for `_placement`'s reason one function up, and used by
    `Carve.materialise` so a retired row is written NOWHERE — which is what
    makes a retiring leg's tree genuinely empty at that path rather than empty
    because a fixture forgot to write the file.
    """
    retired = row.get("retired")
    if isinstance(retired, dict):
        return retired.get("at"), retired.get("at_path")
    return None, None


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
        than vacated by a fixture that forgot to write the file. AND NOT AT
        ALL where a ruling has RETIRED the arrival (RULED 5656343213), for
        the same reason read one step further on.
        """
        dest = self.tmp / (name or f"dest-{destination}")
        dest.mkdir(parents=True, exist_ok=True)
        for row in doc["rows"]:
            # A RETIRED row is materialised nowhere (RULED 5656343213): the
            # ruling DELETED the arrival, so the tree this builds is the tree
            # the act leaves behind.
            if _retirement(row)[1] is not None:
                continue
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
    """The three copies of the floor, over one table of rows.

    RULED Q-L8 (c) is the lesson this closes in advance: `validate-carve-
    manifest.py`, this file and `scripts/carved_reach.py` each carry the same
    three-line reading of `re_destined:`, because none of the three can import
    either of the others, and two tools quietly disagreeing about ONE
    definition is what cost six declared lines when a line meant two things.
    `carved_reach.py` joined the comparison at `PRRT_kwDOTAvnrs6h1nYE`: its
    `source()` (and `sources_under()`/`shed_destination()` through it) used to
    read a row's raw `destination`/`destination_path` even when a
    `re_destined:` block said a ruling had moved the placement, which is
    exactly the disagreement this test exists to catch — now for three readers
    instead of two. The mis-shaped rows are in the table deliberately — the
    agreement that matters most is the one about a document none of the three
    tools validates.
    """
    other = _load_manifest_validator()
    import carved_reach  # noqa: E402 — local: only this test needs it here
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
        assert MODULE.effective_arrival(row) == carved_reach.effective_arrival(row), \
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
# RULED 5656343213 — the RETIREMENT, and `arrival-not-retired`
#
# Brett Heap, 2026-09-13, by interactive multi-choice, on the question slice
# S8's author put in `#656` comment `5650335573` § 2. A moved row may carry
# `retired: {at, at_path, ruling, surface, note}` saying that a RULING has
# DELETED the arrival itself — not moved it, as Q6 does, because the surface
# the arrived file needed is at NO leg to move it to. This file then asks the
# INVERSE of its usual question at that leg: the row is not owed, and the path
# must be empty.
#
# THE FAILURE MODE THESE CASES ARE BUILT AROUND is the one a half-built form
# would have: a `retired:` that only stopped ASKING for the file would leave
# the arrived copy standing under a declared root with nothing left to declare
# it — `rows_for()` having dropped the row, nothing else here would ever
# mention it again. `check_retired` is what closes that, and it runs BEFORE
# the walk so the finding names the RULING rather than the filename.
# --------------------------------------------------------------------------

RETIREMENT_RULING = ("`#656` comment 5656343213 (RULED, Brett Heap "
                     "2026-09-13)")

#: The manifest's own `not_moved` row, which is what `retired.surface` must be
#: — `validate-carve-manifest.py` holds it, and this file reads the block
#: without revalidating it, so the value here is the one a valid document
#: carries.
RETIRED_SURFACE = "scripts/pkg/neutral.py"

RETIRED_SOURCE = "scripts/pkg/beta.py"
RETIRED_AT = "scratch_code"
RETIRED_AT_PATH = "src/pkg/beta.py"


def _retire(doc: dict[str, Any], source_path: str = RETIRED_SOURCE,
            surface: str = RETIRED_SURFACE, **override: Any) -> dict[str, Any]:
    """Retire a row of the generated manifest at its EFFECTIVE arrival.

    `at`/`at_path` are READ OFF THE ROW and never typed — through
    `re_destined:` where one is present, because that is what EFFECTIVE means
    and a fixture that took the raw destination could not tell the composed
    case from the plain one. `beta.py` by default: the row that CARRIES A
    DECLARED EDIT, so these cases prove that a retirement stops the phase-B
    question being asked rather than merely passing it.
    """
    row = next(r for r in doc["rows"] if r["source_path"] == source_path)
    at, at_path = _placement(row)
    block: dict[str, Any] = {
        "at": at,
        "at_path": at_path,
        "ruling": RETIREMENT_RULING,
        "surface": surface,
    }
    block.update(override)
    row["retired"] = block
    return row


def test_a_retirement_is_asked_at_THE_LEG_and_not_only_at_the_spelling(
        carve: Carve) -> None:
    """A `destinations:` KEY IS A LABEL and the retirement is about a LEG
    (Copilot review of PR #1032, round 9).

    `check_shape` deliberately admits two keys sharing one
    `{repository, leg}` body, and `--destination` names a key. `retired_rows()`
    compared that key as a STRING, so a run invoked with the other spelling of
    the very leg the block names skipped the retirement: the absence was never
    required at all.

    AND THE FAILURE IS NOT SILENCE — IT IS THE WRONG REMEDY, which is worse. A
    file left at the retired path is not claimed by any row, so the walk finds
    it and refuses `arrival-undeclared-file`, whose sentence tells the operator
    to DECLARE it. A ruling said to DELETE it. This test pins the CODE and not
    merely the exit status, because the two codes send an operator in opposite
    directions.

    The manifest here is one the validator ACCEPTS: `retired.at` is the row's
    own `destination` spelling, verbatim, because `_check_retired_consistency`
    compares those two as strings and refuses any document that spells them
    differently. So the alias never enters the document — it enters on the
    COMMAND LINE, which is exactly where nothing had checked it.
    """
    doc = carve.manifest_doc()
    doc["destinations"]["scratch_code_alias"] = dict(
        doc["destinations"][RETIRED_AT])
    row = _retire(doc)
    assert row["retired"]["at"] == RETIRED_AT, row
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    # The act's OTHER half, not done: the leg still has the file.
    _write(dest, RETIRED_AT_PATH, "STILL HERE\n")

    # THE LEG'S OWN SPELLING answers correctly, and always did.
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-not-retired", done.stdout
    assert "5656343213" in json.loads(done.stdout)["detail"], done.stdout

    # THE ALIAS must reach the same finding. Before round 9 it reached
    # `arrival-undeclared-file` instead — same exit code, opposite instruction.
    aliased = run(carve, manifest, "--destination", "scratch_code_alias",
                  "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(aliased) == "arrival-not-retired", aliased.stdout
    detail = json.loads(aliased.stdout)["detail"]
    assert "5656343213" in detail, detail
    assert RETIRED_AT_PATH in detail, detail


def test_a_retirement_reached_through_an_alias_reports_its_refill(
        carve: Carve) -> None:
    """The passing half of round 9's finding, and the half that shows the two
    selectors now agree.

    With the retired path lawfully refilled by a declared `--replica-at`
    replica, the run must REPORT the retirement as `absence: refilled` — not
    omit it. Under the alias spelling the row was not selected at all, so the
    `retired` list came back EMPTY and a reader was told nothing about a
    retirement this leg owes: the silent direction of the same defect.
    """
    doc = carve.manifest_doc()
    doc["destinations"]["scratch_code_alias"] = dict(
        doc["destinations"][RETIRED_AT])
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    _write(dest, RETIRED_AT_PATH, SURFACE_FILES["scripts/pkg/neutral.py"])

    for spelling in (RETIRED_AT, "scratch_code_alias"):
        done = run(carve, manifest, "--destination", spelling,
                   "--dest-root", str(dest), "--phase", "B", "--json",
                   "--replica-at", f"scripts/pkg/neutral.py={RETIRED_AT_PATH}")
        assert done.returncode == 0, (spelling, done.stdout + done.stderr)
        retired = json.loads(done.stdout)["retired"]
        assert [r["source_path"] for r in retired] == [RETIRED_SOURCE], \
            (spelling, retired)
        assert retired[0]["absence"] == "refilled", (spelling, retired)
        assert retired[0]["refilled_by"], (spelling, retired)


def test_the_leg_no_longer_owes_a_retired_row(carve: Carve) -> None:
    """The whole act, passing: the row is not owed here any more, the tree
    that no longer carries it verifies, and the retirement is REPORTED rather
    than merely tolerated — with the surface and the citation, because an
    absence cannot tell a reader why by itself."""
    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    assert not (dest / RETIRED_AT_PATH).exists()
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    assert summary["rows"] == 1, summary          # alpha.py only
    retired = summary["retired"]
    assert [row["source_path"] for row in retired] == [RETIRED_SOURCE], summary
    assert retired[0]["at_path"] == RETIRED_AT_PATH, retired
    assert retired[0]["surface"] == RETIRED_SURFACE, retired
    assert retired[0]["ruling"] == RETIREMENT_RULING, retired


def test_a_retired_row_is_neither_digested_nor_diffed(carve: Carve) -> None:
    """`rows_for()` drops it, so nothing downstream asks it anything.

    Measured in BOTH phases against the same document un-retired, because the
    two phases ask a `moved_with_declared_edit` row two different questions:
    phase A digests it, phase B diffs it against its declared lines. Retired,
    it is in neither count and in neither row total — which is the difference
    between a row this leg no longer owes and a row it owes and cannot find.
    """
    plain = carve.manifest_doc()
    plain_manifest = carve.write_manifest(plain, name="plain.yaml")
    plain_dest = carve.materialise(plain, RETIRED_AT, name="dest-plain")

    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT, name="dest-retired")
    assert not (dest / RETIRED_AT_PATH).exists()

    # PHASE A — the digest question. `beta.py` is digested un-retired and is
    # not digested retired.
    done = run(carve, plain_manifest, "--destination", RETIRED_AT,
               "--dest-root", str(plain_dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    before = json.loads(done.stdout)
    assert before["rows"] == 2 and before["digests_verified"] == 2, before

    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    after = json.loads(done.stdout)
    assert after["rows"] == 1 and after["digests_verified"] == 1, after

    # PHASE B — the declared-lines question, on trees carrying the edit.
    (plain_dest / RETIRED_AT_PATH).write_text(BETA_REWRITTEN, encoding="utf-8")
    done = run(carve, plain_manifest, "--destination", RETIRED_AT,
               "--dest-root", str(plain_dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["declared_edits_diffed"] == 1, done.stdout

    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["declared_edits_diffed"] == 0, done.stdout


def test_a_copy_left_at_a_retired_arrival_refuses(carve: Carve) -> None:
    """The half a reader should check. A retirement that did not also DELETE
    the file leaves an arrival the floor no longer stands behind and no row
    declares — and the finding names the RULING and the SURFACE, not the
    filename, because it runs before the walk."""
    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    left_behind = dest / RETIRED_AT_PATH
    left_behind.parent.mkdir(parents=True, exist_ok=True)
    left_behind.write_text(SURFACE_FILES[RETIRED_SOURCE], encoding="utf-8")
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-retired"
    detail = json.loads(done.stdout)["detail"]
    assert RETIREMENT_RULING in detail, detail
    assert RETIRED_SURFACE in detail, detail


def test_the_leftover_is_not_left_to_the_walk_to_find(carve: Carve) -> None:
    """WHY `check_retired` EXISTS AT ALL, as running code.

    Left to `check_undeclared_files`, an un-deleted file would refuse as
    `arrival-undeclared-file` — true, and useless: it would send a reader
    looking for an admission rule for a file whose whole story is the
    `retired:` block in its own row. `check_retired` answers FIRST and names
    the ruling, which is the difference between a refusal an operator can act
    on and one that starts a hunt.

    AND THE WALK DOES LOOK, SINCE ROUND 6. This case is the destination where
    the retired row is the ONLY row under `examples`, and the roots used to be
    computed from the list the retirement had already been dropped from — so
    that directory left the walk altogether and anything ELSE added there
    passed in silence (`test_a_retired_rows_directory_stays_in_the_walk`
    above is that hole, measured). The roots now keep a retired row's
    directory while `placed` still excludes its path, so the two checks divide
    the question properly: the retired path is `check_retired`'s, and every
    other file under the same root is the walk's.
    """
    doc = carve.manifest_doc()
    _retire(doc, "scripts/pkg/gamma.py")     # the only `scratch_spec` row
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    stray = dest / "examples/gamma.py"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text(SURFACE_FILES["scripts/pkg/gamma.py"], encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-retired"
    # The root really is gone — which is what makes the paragraph above a
    # measurement rather than a worry.
    doc = carve.manifest_doc()
    _retire(doc, "scripts/pkg/gamma.py")
    manifest = carve.write_manifest(doc)
    clean = carve.materialise(doc, "scratch_spec", name="dest-spec-clean")
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(clean), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    # THE ROOT SURVIVES THE RETIREMENT and the row does not: `rows: 0` with
    # `declared_roots: ["examples"]` is the whole of round 6's repair in two
    # fields — nothing is owed at that path any more, and the directory is
    # still read.
    clean_summary = json.loads(done.stdout)
    assert clean_summary["declared_roots"] == ["examples"], done.stdout
    assert clean_summary["rows"] == 0, done.stdout
    assert clean_summary["files_walked"] == 0, done.stdout


def test_a_symlink_left_at_the_retired_path_is_not_invisible(
        carve: Carve) -> None:
    """`lexists` and not `exists`, on `check_vacated`'s reasoning verbatim: a
    DANGLING symlink reads as absent to a followed test and git would commit
    it all the same."""
    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    link = dest / RETIRED_AT_PATH
    link.parent.mkdir(parents=True, exist_ok=True)
    os.symlink("../../nowhere/beta.py", link)
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-retired"


def test_another_rows_arrival_at_the_retired_path_is_a_lawful_refill(
        carve: Carve) -> None:
    """A retirement EMPTIES a path; another row's own effective arrival may
    lawfully occupy it, and an entry there is then that row's — verified by
    `check_arrivals` on its own terms — not the retired row's leftover. Built
    in from the first line of `check_retired` rather than found in review,
    which is what PR #1011 cost `check_vacated` to learn.

    AND THE RECORD SAYS SO (Copilot round 5): the exclusion is a decision not
    to ASK the absence question here, so this retirement is reported
    `absence: refilled`, naming the arrival that occupies the path, and not as
    an absence this run verified. The assertion is AMENDED rather than joined
    by a second case, because the defect was in what THIS run already said."""
    doc = carve.manifest_doc()
    _retire(doc)
    alpha = next(r for r in doc["rows"]
                 if r["source_path"] == "scripts/pkg/alpha.py")
    assert alpha["destination"] == RETIRED_AT, alpha
    alpha["destination_path"] = RETIRED_AT_PATH
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    summary = json.loads(done.stdout)
    assert [row["source_path"] for row in summary["retired"]] == \
        [RETIRED_SOURCE], summary
    assert summary["retired"][0]["absence"] == "refilled", summary
    assert summary["retired"][0]["refilled_by"] == \
        "the arrival of scripts/pkg/alpha.py", summary


def test_a_declared_replica_may_refill_a_retired_path(carve: Carve) -> None:
    """The `--replica-at` twin of the case above, and it is a SEPARATE one
    for the reason PR #1011's round 3 found the hard way: a replica is not a
    row `rows_for()` ever returns (RULED OQ-C), so a fix that only excluded
    other rows' arrivals would still read a declared replica's file as the
    retired row's abandoned copy.

    ITS RECORD NAMES THE OTHER REFILLER (Copilot round 5). `--replica-at` is
    declared on the COMMAND LINE and not in the manifest, so a reader of this
    run's output has no row to look the occupant up in — which is the reason
    the refiller is named in the record rather than left as a bare
    `absence: refilled`."""
    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    _write(dest, RETIRED_AT_PATH, SURFACE_FILES[RETIRED_SURFACE])
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json",
               "--replica-at", f"{RETIRED_SURFACE}={RETIRED_AT_PATH}")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["replicas_verified"] == 1, payload
    assert [row["source_path"] for row in payload["retired"]] == \
        [RETIRED_SOURCE], payload
    assert payload["retired"][0]["absence"] == "refilled", payload
    assert payload["retired"][0]["refilled_by"] == \
        "a declared --replica-at replica", payload


def test_a_row_re_destined_and_then_retired_is_retired_at_the_leg_it_reached(
        carve: Carve) -> None:
    """THE TWO ACTS COMPOSE IN ONE ORDER — move, then retire — and this is the
    case that proves the pair at both legs.

    `beta.py` is re-destined from `scratch_code` to `scratch_spec` by RULED
    Q6 and retired there by RULED 5656343213. The GAINING leg must be empty at
    `examples/beta.py` and report the retirement; the LOSING leg must still be
    VACATED at `src/pkg/beta.py`, because a retirement says nothing about the
    other half of a re-destination — those are two absences at two legs, and
    `check_vacated` goes on asking its own.
    """
    doc = carve.manifest_doc()
    _re_destine(doc)                       # -> scratch_spec:examples/beta.py
    row = _retire(doc)                     # ... retired AT that arrival
    assert row["retired"]["at"] == RE_DESTINED_TO, row
    assert row["retired"]["at_path"] == RE_DESTINED_TO_PATH, row
    manifest = carve.write_manifest(doc)

    gaining = carve.materialise(doc, RE_DESTINED_TO)
    losing = carve.materialise(doc, "scratch_code")
    assert not (gaining / RE_DESTINED_TO_PATH).exists()
    assert not (losing / RE_DESTINED_FROM_PATH).exists()

    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(gaining), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    gaining_summary = json.loads(done.stdout)
    assert [r["source_path"] for r in gaining_summary["retired"]] == \
        [RE_DESTINED_SOURCE], gaining_summary
    assert gaining_summary["re_destined"]["arrived"] == [], gaining_summary

    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(losing), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    losing_summary = json.loads(done.stdout)
    assert losing_summary["retired"] == [], losing_summary
    assert [r["source_path"] for r in losing_summary["re_destined"]["vacated"]] \
        == [RE_DESTINED_SOURCE], losing_summary

    # And each half still refuses on its own: the gaining leg for the file the
    # retirement deleted, the losing leg for the file the move left behind.
    _write(gaining, RE_DESTINED_TO_PATH, SURFACE_FILES[RE_DESTINED_SOURCE])
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(gaining), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-retired"
    _write(losing, RE_DESTINED_FROM_PATH, SURFACE_FILES[RE_DESTINED_SOURCE])
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(losing), "--phase", "A", "--json")
    assert refusal(done) == "arrival-not-vacated"


def test_a_retirement_at_one_leg_says_nothing_about_another(
        carve: Carve) -> None:
    """ONE destination per run. `gamma.py` is retired at `scratch_spec`; the
    `scratch_code` run neither reports it nor asks anything about it, and the
    two absences are two questions about two legs."""
    doc = carve.manifest_doc()
    _retire(doc, "scripts/pkg/gamma.py")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["retired"] == [], done.stdout


# --------------------------------------------------------------------------
# THE PLACEMENT A BLOCK NAMES vs THE PLACEMENT ITS ROW MAKES (Copilot review of
# PR #1032, round 3)
#
# `rows_for()` and `retired_rows()` are deliberately ASYMMETRIC: the first
# reads the ROW's effective arrival, the second reads the BLOCK's `at`. That
# is the right pair of questions, and it left a hole the moment the two
# disagreed — the row was dropped THERE for carrying a readable retirement and
# declined HERE for naming another leg, so it was checked as neither an
# arrival nor a retirement and its absent file passed silently. These cases
# are that hole, from both sides, and they are end-to-end runs of the shipped
# script rather than unit calls, because "passes silently" is a property of
# the exit code and not of a predicate.
#
# `validate-carve-manifest.py`'s check 6 refuses such a document as
# `carve-disposition-inconsistent`. It is not a defence here: this file is run
# AT A LEG on a manifest `read_manifest()` deliberately does not revalidate,
# which is the whole reason `effective_arrival`, `retired_at` and
# `_also_replicated_labels` each guard their own reading rather than trusting
# the other tool to have run.
# --------------------------------------------------------------------------


def test_a_retirement_naming_another_leg_leaves_this_one_owed_the_file(
        carve: Carve) -> None:
    """The block says `scratch_spec`; the row arrives at `scratch_code`. The
    `scratch_code` run must still ASK for `src/pkg/beta.py` — and refuse its
    absence — because nothing in this document retires the placement that leg
    makes.

    The tree is the one the fixture builds for an author who acted on the bad
    block: `Carve.materialise` writes a retired row nowhere, so the file is
    genuinely gone. Before the `retired_arrival` split this run exited 0."""
    doc = carve.manifest_doc()
    row = _retire(doc)
    row["retired"]["at"] = RE_DESTINED_TO
    row["retired"]["at_path"] = RE_DESTINED_TO_PATH
    manifest = carve.write_manifest(doc)

    dest = carve.materialise(doc, RETIRED_AT)
    assert not (dest / RETIRED_AT_PATH).exists()
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"

    # AND AT THE LEG THE BLOCK NAMES IT IS REFUSED — round 4's half of the
    # same finding. `retired_rows()` still SELECTS it there, because where a
    # row is CHECKED is a selection's question, but `check_retired` reads the
    # block before joining its path and a retirement of a placement this row
    # does not make retires nothing anywhere. Until then this run exited 0 and
    # REPORTED the retirement: a path proved empty that no ruling emptied.
    named = carve.materialise(doc, RE_DESTINED_TO)
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(named), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    assert "carve-disposition-inconsistent" in json.loads(done.stdout)["detail"]


def test_a_retirement_naming_another_path_here_leaves_the_arrival_owed(
        carve: Carve) -> None:
    """The narrower half of the same hole, and the one a leg is likeliest to
    hand-write: the right `at`, the wrong `at_path`.

    `retired_rows()` selects the row here and proves the path the BLOCK named
    empty — which it always was — while the placement the ROW makes goes
    unasked. Nothing else in the file would mention `src/pkg/beta.py` again."""
    doc = carve.manifest_doc()
    row = _retire(doc)
    row["retired"]["at_path"] = "src/pkg/beta-under-another-name.py"
    manifest = carve.write_manifest(doc)

    dest = carve.materialise(doc, RETIRED_AT)
    assert not (dest / RETIRED_AT_PATH).exists()
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"


def test_the_placement_question_is_this_files_own_and_the_shared_one_is_not(
        ) -> None:
    """`retired_at` is the predicate the THREE tools mirror and it is
    unchanged; `retired_arrival` is the fourth question only this file can
    ask, because only this file is run against a destination.

    Called directly, over one row read three ways, so the two selections'
    pairing is visible as arithmetic rather than inferred from an exit code:
    every row must be in exactly one of `rows_for` and `retired_rows` at the
    leg it belongs to, and in `rows_for` wherever the block does not name the
    row's own placement."""
    row: dict[str, Any] = {
        "source_path": "scripts/pkg/beta.py",
        "disposition": "moved_verbatim",
        "destination": "scratch_code",
        "destination_path": "src/pkg/beta.py",
        "retired": {"at": RE_DESTINED_TO, "at_path": RE_DESTINED_TO_PATH,
                    "ruling": RETIREMENT_RULING, "surface": RETIRED_SURFACE},
    }
    doc: dict[str, Any] = {"rows": [row]}

    # MIS-PLACED: readable, and about no placement this row makes.
    assert MODULE.retired_at(row) == (RE_DESTINED_TO, RE_DESTINED_TO_PATH), row
    assert MODULE.retired_arrival(row) == (None, None), row
    assert MODULE.rows_for(doc, "scratch_code") == [row], doc
    assert MODULE.retired_rows(doc, "scratch_code") == [], doc
    assert MODULE.retired_rows(doc, RE_DESTINED_TO) == [row], doc

    # WELL PLACED: the row's own arrival, and the pair swaps over.
    row["retired"]["at"] = "scratch_code"
    row["retired"]["at_path"] = "src/pkg/beta.py"
    assert MODULE.retired_arrival(row) == ("scratch_code", "src/pkg/beta.py")
    assert MODULE.rows_for(doc, "scratch_code") == [], doc
    assert MODULE.retired_rows(doc, "scratch_code") == [row], doc

    # COMPOSED (RULED Q6 then RULED 5656343213): the EFFECTIVE arrival is what
    # `retired_arrival` compares against, so the pair swaps at the leg the file
    # actually reached and the row is owed at neither.
    row["re_destined"] = {"to": RE_DESTINED_TO, "to_path": RE_DESTINED_TO_PATH,
                          "from": "scratch_code",
                          "from_path": "src/pkg/beta.py",
                          "ruling": RE_DESTINED_RULING}
    assert MODULE.retired_arrival(row) == (None, None), row
    assert MODULE.rows_for(doc, RE_DESTINED_TO) == [row], doc
    row["retired"]["at"] = RE_DESTINED_TO
    row["retired"]["at_path"] = RE_DESTINED_TO_PATH
    assert MODULE.retired_arrival(row) == (RE_DESTINED_TO, RE_DESTINED_TO_PATH)
    assert MODULE.rows_for(doc, RE_DESTINED_TO) == [], doc
    assert MODULE.rows_for(doc, "scratch_code") == [], doc
    assert MODULE.retired_rows(doc, RE_DESTINED_TO) == [row], doc


# --------------------------------------------------------------------------
# THE BLOCK IS READ BEFORE ITS PATH IS JOINED (Copilot review of PR #1032,
# round 4)
#
# Round 3 asked the PLACEMENT question on `rows_for`'s side, where a deleted
# file was passing silently. It left the other side unasked: `retired_rows()`
# selects on `retired.at` — ONE field of five — so at the leg the BLOCK names,
# nothing about the block had been read at all when its `at_path` was joined
# to `--dest-root` and asserted ABSENT. Every reading a check like that fails
# to make answers its question "yes".
#
# Three consequences, all measured below against the previous commit: a
# malformed block passed BOTH destination runs whenever nobody had acted on it
# yet; a run reported and counted a retirement whose emptied path no ruling
# emptied; and where a live file sat at the named path the run refused
# `arrival-not-retired`, a finding whose own sentence tells the reader to
# DELETE it. `retired_placement` answers both readings in one place, as
# `arrival-unreadable` naming `validate-carve-manifest.py` — which owns each
# defect (`_require_closed_relative_path`, and check 6's
# `carve-disposition-inconsistent`) for a document anyone ran it over. What is
# refused here is not the document: it is the answer this run would otherwise
# print about a leg.
# --------------------------------------------------------------------------


def test_a_misplaced_block_is_refused_before_anything_is_deleted(
        carve: Carve) -> None:
    """The case round 3 did not reach: nobody acted on the bad block.

    The file is still at the placement the ROW makes, so `check_arrivals`
    verifies it normally; the path the BLOCK names is empty, as it always was,
    so the retirement "verified" too. Both destination runs exited 0 on a
    document in which one row's retirement is about a file it is not about."""
    doc = carve.manifest_doc()
    row = _retire(doc)
    row["retired"]["at_path"] = "src/pkg/beta-under-another-name.py"
    manifest = carve.write_manifest(doc)

    # `Carve.materialise` writes a retired row nowhere, so the arrival is put
    # back by hand: this is the tree of a leg where the act has NOT happened.
    dest = carve.materialise(doc, RETIRED_AT)
    _write(dest, RETIRED_AT_PATH, SURFACE_FILES[RETIRED_SOURCE])
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    detail = json.loads(done.stdout)["detail"]
    assert "src/pkg/beta-under-another-name.py" in detail, detail
    assert "carve-disposition-inconsistent" in detail, detail


def test_a_misplaced_block_can_neither_order_a_deletion_nor_hide_in_a_refill(
        carve: Carve) -> None:
    """The two shapes the un-read block took at the leg it named.

    (a) A LIVE FILE AT THE NAMED PATH drew `arrival-not-retired`, whose text
    reads "Delete it in the commit that lands the `retired:` block" — an
    instruction to delete a file no ruling touched, issued on the strength of
    a block that names another row's placement. A wrong finding that asks for
    a deletion is worse than a missed one.

    (b) THE NAMED PATH IS ANOTHER ROW'S OWN ARRIVAL, the `claimed` exclusion a
    lawful refill needs (PR #1011). It must not swallow the defect, which is
    why `check_retired` reads the block BEFORE it: a refill is a reason not to
    ask the ABSENCE question, never a reason to stop reading the block that
    asked it. Here the exclusion hid it completely and the run exited 0."""
    doc = carve.manifest_doc()
    row = _retire(doc)
    row["retired"]["at"] = RE_DESTINED_TO
    row["retired"]["at_path"] = "examples/unrelated.py"
    manifest = carve.write_manifest(doc)

    named = carve.materialise(doc, RE_DESTINED_TO)
    _write(named, "examples/unrelated.py", "UNRELATED = 1\n")
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(named), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    # The refusal EXPLAINS the harm and never issues it: `arrival-not-retired`'s
    # instruction — the sentence that would have a reader remove that file — is
    # the one string this detail must not carry.
    assert "Delete it in the commit" not in json.loads(done.stdout)["detail"]

    # (b) — `examples/gamma.py` is the `scratch_spec` row's own arrival, so it
    # is `claimed` and the absence question is skipped for it.
    row["retired"]["at_path"] = "examples/gamma.py"
    manifest = carve.write_manifest(doc)
    done = run(carve, manifest, "--destination", RE_DESTINED_TO,
               "--dest-root", str(named), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"


def test_a_retirement_path_this_leg_cannot_join_is_not_an_empty_path(
        carve: Carve) -> None:
    """`read_manifest()` does not revalidate the document, so
    `retired.at_path: ../elsewhere` reaches the join exactly as a malformed
    `destination_path:` would — and here the join is the whole check.

    The fixture's destination roots are siblings, which is the hazard drawn to
    scale: `../dest-scratch_spec/examples/gamma.py` at the CODE leg is the
    SPEC leg's live arrived file. Before this commit the run refused
    `arrival-not-retired` about it — another repository's verified arrival,
    reported as this leg's un-deleted retirement — and with nothing at the
    other end of the `..` it exited 0, having proved a path outside the tree
    empty and called that a retirement.

    The row's own `destination_path` is moved with the block, because
    `rows_for()` drops the row only where the block names the placement the
    row makes: the document that reaches this join is malformed in both
    fields, which is exactly what `_require_closed_relative_path` refuses in
    `validate-carve-manifest.py` and what this leg cannot assume anyone ran."""
    doc = carve.manifest_doc()
    escape = "../dest-scratch_spec/examples/gamma.py"
    row = _retire(doc)
    row["destination_path"] = escape
    row["retired"]["at_path"] = escape
    manifest = carve.write_manifest(doc)

    spec = carve.materialise(doc, RE_DESTINED_TO, name="dest-scratch_spec")
    assert (spec / "examples/gamma.py").is_file(), spec
    dest = carve.materialise(doc, RETIRED_AT, name="dest-scratch_code")
    assert (dest / ".." / "dest-scratch_spec/examples/gamma.py").is_file()

    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    detail = json.loads(done.stdout)["detail"]
    assert "plain path inside --dest-root" in detail, detail
    assert "_require_closed_relative_path" in detail, detail


def test_the_block_is_read_before_its_path_is_joined(carve: Carve) -> None:
    """`retired_placement` called directly, over one row read three ways —
    the pairing `test_the_placement_question_is_this_files_own_and_the_shared_one_is_not`
    states for the SELECTIONS, stated here for the READING each one's caller
    is left owing. A well-placed block answers with the path; each defect
    refuses by name, and names the tool whose finding the document defect is."""
    doc = carve.manifest_doc()
    row = _retire(doc)
    assert MODULE.retired_placement(row) == RETIRED_AT_PATH, row

    row["retired"]["at_path"] = "../outside.py"
    with pytest.raises(MODULE.ArrivalRefusal) as unreadable:
        MODULE.retired_placement(row)
    assert unreadable.value.code == "arrival-unreadable"
    assert "_require_closed_relative_path" in unreadable.value.detail

    row["retired"]["at_path"] = "src/pkg/somewhere-else.py"
    with pytest.raises(MODULE.ArrivalRefusal) as inconsistent:
        MODULE.retired_placement(row)
    assert inconsistent.value.code == "arrival-unreadable"
    assert "carve-disposition-inconsistent" in inconsistent.value.detail

    # AND THE RE-DESTINED CASE (RULED Q6 then RULED 5656343213): the placement
    # a block must name is the EFFECTIVE one, so the same pair of readings is
    # made against the leg the file actually reached.
    row["re_destined"] = {"to": RE_DESTINED_TO, "to_path": RE_DESTINED_TO_PATH,
                          "from": RETIRED_AT, "from_path": RETIRED_AT_PATH,
                          "ruling": RE_DESTINED_RULING}
    row["retired"]["at"] = RE_DESTINED_TO
    row["retired"]["at_path"] = RE_DESTINED_TO_PATH
    assert MODULE.retired_placement(row) == RE_DESTINED_TO_PATH, row


def test_the_human_line_names_the_retirements_at_this_leg(
        carve: Carve) -> None:
    """A reader of a leg's log must be able to see that a row it used to owe
    was checked to be GONE by a ruling rather than simply forgotten."""
    doc = carve.manifest_doc()
    _retire(doc)
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert ("1 row(s) RETIRED here by ruling and verified absent "
            "(RULED 5656343213)") in done.stdout, done.stdout


def test_a_refilled_retirement_is_not_printed_as_a_verified_absence(
        carve: Carve) -> None:
    """THE RUN MAY NOT CLAIM THE ONE READING IT DELIBERATELY SKIPPED (Copilot
    review of PR #1032, round 5).

    `check_retired` EXCLUDES a path another row's arrival or a declared replica
    lawfully occupies — rightly: the entry there is the refiller's and is
    verified on the refiller's own terms. But the summary then reported every
    retirement as "verified absent", which made this line's only false case the
    one case where a file really is sitting at the retired path — the case a
    reader would most want it honest about, and the one an operator would act
    on. TWO retirements here rather than one, so the arithmetic is visible:
    the counts must SPLIT, not switch.

    The second run is the control, on the same manifest: take the refill away
    and the original sentence returns unchanged, so what moved is the report of
    a refill and not the report of a retirement."""
    doc = carve.manifest_doc()
    _retire(doc)
    _retire(doc, source_path="scripts/pkg/alpha.py")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    _write(dest, RETIRED_AT_PATH, SURFACE_FILES[RETIRED_SURFACE])
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A",
               "--replica-at", f"{RETIRED_SURFACE}={RETIRED_AT_PATH}")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "RETIRED here by ruling and verified absent" not in done.stdout, \
        done.stdout
    assert ("2 row(s) RETIRED here by ruling (RULED 5656343213), 1 verified "
            "absent and 1 at a path a LAWFUL REFILL occupies — not asked, not "
            "owed absent: src/pkg/beta.py now holds a declared --replica-at "
            "replica") in done.stdout, done.stdout

    control_dest = carve.materialise(doc, RETIRED_AT, name="dest-no-refill")
    control = run(carve, manifest, "--destination", RETIRED_AT,
                  "--dest-root", str(control_dest), "--phase", "A")
    assert control.returncode == 0, control.stdout + control.stderr
    assert ("2 row(s) RETIRED here by ruling and verified absent "
            "(RULED 5656343213)") in control.stdout, control.stdout


def test_a_leg_with_no_retirement_says_nothing_about_one(
        carve: Carve) -> None:
    """Silent at zero, on the re-destination clause's own reasoning: the
    MANIFEST validator's count is unconditional because it describes ONE
    document whose state a reader must be able to read off any run; this line
    describes a LEG, where the honest default is that every arrival here is
    the carve's own."""
    doc = carve.manifest_doc()
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "RETIRED" not in done.stdout, done.stdout


def test_all_three_tools_read_the_retirement_identically() -> None:
    """The three copies of the predicate, over one table of rows.

    `validate-carve-manifest.py`, this file and `scripts/carved_reach.py` each
    carry the same reading of `retired:`, because none of the three can import
    either of the others — the same duplication, and the same risk, that
    `test_both_tools_read_the_effective_arrival_identically` closes for
    `effective_arrival`. The mis-shaped rows are in the table deliberately, and
    they are the half that matters MOST here: this guard fails closed in the
    OTHER direction from `effective_arrival`'s. Half a re-destination reading
    as no re-destination leaves a row owed at its original leg; half a
    RETIREMENT reading as one would SILENCE this leg's arrival check for that
    row, so `retired: {}` and a block whose `at_path` is a list must both read
    as NO retirement in all three.

    THE LAST FIVE ROWS ARE THE HALF-WRITTEN BLOCKS (Copilot review of PR
    #1032, round 2): `at` and `at_path` present and well-formed, `ruling` or
    `surface` missing, empty, blank or not a string. Each is a placement a
    reader COULD act on and a retirement this floor has not ruled, and the
    guard's four required keys are what keep the two apart.
    """
    other = _load_manifest_validator()
    import carved_reach  # noqa: E402 — local: only this test needs it here
    table: list[dict[str, Any]] = [
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py"},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING,
                     "surface": RETIRED_SURFACE}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": "scratch_code"},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code"}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": ["src/pkg/a.py"]}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": ["scratch_code"], "at_path": "src/pkg/a.py"}},
        # …and the four-key half-blocks: a usable PLACEMENT, no ruled
        # RETIREMENT (Copilot review of PR #1032, round 2).
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py"}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "surface": RETIRED_SURFACE}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING, "surface": "   "}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": {"comment": 5656343213},
                     "surface": RETIRED_SURFACE}},
        # …and the CLOSED KEY SET, which the docstrings of all three copies
        # already claimed and none of them enforced (Copilot review of PR
        # #1032, round 6): a block carrying a key outside
        # {at, at_path, ruling, surface, note} — a misspelled `notes:`, a
        # field somebody invented — is a document the manifest validator
        # refuses (`carve-shape-invalid`), and these three tools run without
        # it. A `note` that is not a string is the same defect in the one
        # OPTIONAL key.
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING,
                     "surface": RETIRED_SURFACE, "notes": "misspelled"}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING,
                     "surface": RETIRED_SURFACE, "note": ["not a string"]}},
        # …and the OPTIONAL key's own grammar (Copilot review of PR #1032,
        # round 7). `_check_retired_shape` writes it as "a note is prose or it
        # is absent" and refuses a PRESENT blank one; the predicate asked only
        # `isinstance`, so these two blocks read as usable retirements in the
        # three tools and as `carve-shape-invalid` in the grammar. A key the
        # form makes optional is not a key it makes empty.
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING,
                     "surface": RETIRED_SURFACE, "note": ""}},
        {"destination": "scratch_code", "destination_path": "src/pkg/a.py",
         "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                     "ruling": RETIREMENT_RULING,
                     "surface": RETIRED_SURFACE, "note": "   "}},
        {},
    ]
    for row in table:
        assert MODULE.retired_at(row) == other.retired_at(row), row
        assert MODULE.retired_at(row) == carved_reach.retired_at(row), row
    assert MODULE.retired_at(table[1]) == ("scratch_code", "src/pkg/a.py")
    for row in table[2:]:
        assert MODULE.retired_at(row) == (None, None), row

    # AND THE OPTIONAL KEY IS STILL ADMITTED, in all three — the guard closes
    # the SET, it does not close the form. Without this control the two rows
    # above would also pass against a predicate that had simply dropped
    # `note:` from the grammar.
    with_note = {"destination": "scratch_code",
                 "destination_path": "src/pkg/a.py",
                 "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                             "ruling": RETIREMENT_RULING,
                             "surface": RETIRED_SURFACE,
                             "note": "23 tests of a surface at neither leg"}}
    assert MODULE.retired_at(with_note) == ("scratch_code", "src/pkg/a.py")
    assert other.retired_at(with_note) == MODULE.retired_at(with_note)
    assert carved_reach.retired_at(with_note) == MODULE.retired_at(with_note)


def test_the_note_is_prose_or_absent_in_the_grammar_and_in_all_three_readers(
) -> None:
    """The GRAMMAR and the three READERS, asked about the same `note:` (Copilot
    review of PR #1032, round 7).

    The identity test holds the three copies of `retired_at` equal TO EACH
    OTHER; three copies can agree and all three be wrong about the document
    they read. This one holds them to `_check_retired_shape`, which is where
    the form is actually written — *a note is prose or it is absent* — over the
    one key the form makes optional.

    THE DIRECTION IS WHY IT MATTERS. A block the validator refuses and the
    readers accept is not a disagreement about style: `rows_for()` DROPS the
    row, `check_retired` then asks for the file to be ABSENT, and
    `carved_reach` raises `CarveRowRetired` at every retained consumer — a
    required arrival silenced by a key nobody was required to write. The
    grammar is the authority and the readers follow it, in both answers: a
    present blank note is no retirement anywhere, and real prose is a
    retirement everywhere.
    """
    other = _load_manifest_validator()
    import carved_reach  # noqa: E402 — local: only this test needs it here

    def block(**extra: Any) -> dict[str, Any]:
        return {"destination": "scratch_code",
                "destination_path": "src/pkg/a.py",
                "retired": {"at": "scratch_code", "at_path": "src/pkg/a.py",
                            "ruling": RETIREMENT_RULING,
                            "surface": RETIRED_SURFACE, **extra}}

    for note in ("", "   ", "\t\n"):
        row = block(note=note)
        with pytest.raises(other.CarveRefusal) as refusal:
            other._check_retired_shape("row 0", "src/pkg/a.py",
                                       row["retired"])
        assert refusal.value.code == "carve-shape-invalid"
        assert "a note is prose or it is absent" in str(refusal.value)
        assert MODULE.retired_at(row) == (None, None), note
        assert other.retired_at(row) == (None, None), note
        assert carved_reach.retired_at(row) == (None, None), note

    # AND THE OTHER ANSWER, in the same shape: prose the grammar admits is a
    # retirement in all three readers. Without this the loop above would also
    # pass against a predicate that had dropped `note:` from the form.
    told = block(note="23 tests of a surface at neither leg (RULED OQ-F)")
    other._check_retired_shape("row 0", "src/pkg/a.py", told["retired"])
    for reader in (MODULE, other, carved_reach):
        assert reader.retired_at(told) == ("scratch_code", "src/pkg/a.py")

    # …and ABSENT is the third answer the grammar names, admitted by all three.
    bare = block()
    other._check_retired_shape("row 0", "src/pkg/a.py", bare["retired"])
    for reader in (MODULE, other, carved_reach):
        assert reader.retired_at(bare) == ("scratch_code", "src/pkg/a.py")


def test_a_half_written_retirement_leaves_the_arrival_owed(
        carve: Carve) -> None:
    """WHAT THE FOUR-KEY GUARD BUYS, at the tool that would have paid for its
    absence (Copilot review of PR #1032, round 2).

    A leg acting on a `retired:` block DELETES the file, and this fixture's
    own reader is deliberately loose about the rest of the block — so the tree
    below is exactly the tree that act leaves behind, and the only question
    left is whether the floor accepts it. It must not: `retired:` with a
    well-formed `at`/`at_path` but no `ruling` and no `surface` is a placement
    a reader could act on and a retirement NOBODY RULED, and the row is still
    owed here. The refusal is the ordinary one for a file the manifest says
    arrived and the tree does not have.

    `validate-carve-manifest.py` refuses the same document as
    `carve-shape-invalid` — but that is a DIFFERENT tool, run at a different
    moment, against the manifest rather than against a leg. This one runs at
    the leg with `--dest-root`, routinely before anyone has validated the
    document, and this test is what says the absence is not licensed in the
    meantime.
    """
    doc = carve.manifest_doc()
    row = _retire(doc)
    del row["retired"]["ruling"]
    del row["retired"]["surface"]
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, RETIRED_AT)
    assert not (dest / RETIRED_AT_PATH).exists()
    done = run(carve, manifest, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-missing"
    assert RETIRED_AT_PATH in json.loads(done.stdout)["detail"], done.stdout

    # …and the COMPLETE block over the SAME tree verifies, so what the
    # refusal above measures is the two missing keys and not the tree.
    whole_doc = carve.manifest_doc()
    _retire(whole_doc)
    whole = carve.write_manifest(whole_doc, name="manifest-whole.yaml")
    done = run(carve, whole, "--destination", RETIRED_AT,
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert done.returncode == 0, done.stdout + done.stderr


def test_a_retired_rows_directory_stays_in_the_walk(carve: Carve) -> None:
    """RETIREMENT SUPPRESSES ONE ARRIVAL, NEVER THE REST OF THE TREE (Copilot
    review of PR #1032, round 6).

    `rows_for()` drops a retired row so the arrived copy cannot ride into the
    walk's `placed` set — that is the point of the drop, and
    `test_the_leg_no_longer_owes_a_retired_row` is where it is asserted. But
    the walk's ROOTS were computed from the same list, so a directory whose
    LAST arrival was retired left the walk altogether: `check_retired()` asked
    about that one path, `check_undeclared_files()` walked nothing, and any
    other file in that directory passed as a clean destination.

    `scratch_spec` is the destination that can say so: exactly one row lands
    there, `examples/gamma.py`, so retiring it empties `examples/` of
    declarations while leaving the directory in the tree for anything else to
    be added to. The stray file below is what an operator would most want the
    floor to catch — something added where a retirement had just made room.
    """
    doc = carve.manifest_doc()
    _retire(doc, "scripts/pkg/gamma.py")
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_spec")
    assert not (dest / "examples" / "gamma.py").exists()

    # The control FIRST, on the same tree: with the directory empty the run is
    # clean, so what the refusal below measures is the stray file and not the
    # retirement.
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert done.returncode == 0, done.stdout + done.stderr

    stray = dest / "examples" / "stray.py"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text("# added after a retirement emptied this directory\n",
                     encoding="utf-8")
    done = run(carve, manifest, "--destination", "scratch_spec",
               "--dest-root", str(dest), "--phase", "B", "--json")
    assert refusal(done) == "arrival-undeclared-file"
    assert "examples/stray.py" in json.loads(done.stdout)["detail"], done.stdout


def test_the_module_records_the_retirement_and_what_it_does_not_prove(
        ) -> None:
    """The disclosure, asserted in the file that carries it: the ruling, the
    finding, and the two limits — nothing here reads the SURFACE the block
    cites, and one destination is verified per run."""
    doc = MODULE.__doc__ or ""
    assert "retired" in doc, doc
    assert "5656343213" in doc, doc
    assert "arrival-not-retired" in doc, doc
    assert "carve-retired-surface-live" in doc, doc


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


def the_landed_manifest() -> tuple[str, dict[str, Any]]:
    """The committed manifest's TEXT and document — and a failure if it is gone.

    THE SEAT-HOLDING BRANCH HAD OUTLIVED ITS REASON HERE TOO (Copilot review,
    `#1030`). `docs/opendox-carve-manifest.yaml` is authored by the § 6
    ceremony at the carve commit, AFTER both scripts land, so every assertion
    about its contents held a seat until then. The ceremony has happened and
    the seat has nothing left to hold, while what it had degraded into —
    `assert True` — REPORTS A PASS. Absence is a FAILURE here, named, for the
    module docstring's reason.

    THE SEAT THE MODULE DOCSTRING DESCRIBES IS A DIFFERENT ABSENCE and it
    stays: no destination CHECKOUT exists on this machine, so the documented
    invocation is the one with no `--destination`, and `NO DESTINATION` is the
    verifier's ANSWER to that — asserted rather than skipped, and true whether
    or not a destination ever exists.
    """
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    assert manifest.is_file(), (
        f"{MODULE.MANIFEST_RELPATH} is not in this checkout. It landed at the "
        "carve commit, and every assertion in the test that asked for it is "
        "about its contents: its absence is a FAILURE, not a seat to hold.")
    text = manifest.read_text(encoding="utf-8")
    return text, yaml.safe_load(text)


# The word this file's own docstring uses for the number below. A map and not
# an f-string of the digit, because the paragraph is PROSE and says "THE SEVEN
# TESTS"; a count with no word here is a FAILURE that asks for one, never a
# check that quietly stops looking.
MANIFEST_READER_WORDS = {4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN",
                         8: "EIGHT", 9: "NINE", 10: "TEN", 11: "ELEVEN",
                         12: "TWELVE"}


def test_the_module_docstring_counts_the_tests_that_read_the_landed_manifest(
        ) -> None:
    """The docstring's own coverage claim, COUNTED from this file.

    "THE FIVE TESTS THAT READ THE LANDED MANIFEST" was true when it was written
    and stopped being true twice without anyone noticing (Copilot review, round
    eleven on `#1030`): the per-destination table test and § 5.5's phase-example
    test joined the five and the paragraph still said FIVE, while the sentence
    under it — "there is no revision these five can run at without it" — named
    a set two smaller than the one it describes.

    IT IS THE FILE'S OWN SUBJECT, ONE LEVEL UP. Every test in the § 2 and § 5.5
    group exists because a document stated a number nothing re-derived; a module
    docstring that states its own coverage is the same claim in the same shape,
    so it is re-counted here from the CALL SITES rather than maintained by hand.
    """
    source = Path(__file__).read_text(encoding="utf-8")
    readers = sorted(
        node.name for node in ast.parse(source, filename=__file__).body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        and any(isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == the_landed_manifest.__name__
                for call in ast.walk(node)))
    word = MANIFEST_READER_WORDS.get(len(readers))
    assert word is not None, (
        f"{len(readers)} tests in this file read the landed manifest and this "
        "check has no word for that many: extend MANIFEST_READER_WORDS rather "
        f"than leaving the paragraph unchecked. {readers}")
    # The module's docstring, named through `sys.modules` rather than the bare
    # `__doc__` global, so a reader does not have to know which `__doc__` a
    # name inside a function resolves to.
    docstring = " ".join((sys.modules[__name__].__doc__ or "").split())
    for sentence in (f"THE {word} TESTS THAT READ THE LANDED MANIFEST",
                     f"no revision these {word.lower()} can run at without"):
        assert sentence in docstring, (
            f"the module docstring does not say {sentence!r}, and "
            f"{len(readers)} tests in this file read the landed manifest: "
            f"{readers}. The paragraph states its own coverage, so it moves "
            "with the tests it describes or it is a transcription like any "
            "other")


def test_the_real_repository_answers_the_documented_invocation() -> None:
    """The seat, run from the repository root with no arguments.

    A BRANCH and never a skip: see the module docstring. No destination
    checkout exists on this machine — `opensoft/openDox-code` and its four
    siblings hold not one carved byte until Phase 2 of the cutover runbook runs
    — so what this asserts is that the DOCUMENTED INVOCATION answers, exit 0,
    naming the destinations the landed manifest declares. When a destination
    exists, this file gains a case that names it; this assertion stays true.

    THE MANIFEST, THOUGH, IS REQUIRED AND NOT BRANCHED ON: see
    `the_landed_manifest()`. The two absences are not the same absence.
    """
    done = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("NO DESTINATION "), done.stdout
    # THE `else` ARM ASSERTED THE APOLOGY INSTEAD OF THE ANSWER (Copilot
    # review, `#1030`): on a checkout that had lost the landed manifest this
    # test passed on the verifier's "the manifest could not be read" sentence,
    # which is the one state where the five destination keys — the thing the
    # documented invocation is being asserted to name — go unchecked. That
    # sentence is pinned hermetically instead, on a manifest path the test
    # controls (`test_a_manifest_that_is_not_there_refuses`, and the `--json`
    # seat's `destinations_unreadable`), which is the only way to assert it
    # without making this test green on it.
    the_landed_manifest()
    for key in ("opendox_code", "opendox_spec", "opendox_root",
                "openxdox_code", "openxdox_spec"):
        assert key in done.stdout, done.stdout


def test_the_real_manifest_declares_the_roots_the_runbook_names() -> None:
    """The runbook's § 2 table is a claim about the LANDED manifest, and a table
    nothing checks is a comment. This reads the manifest and asserts the roots
    the verifier would walk for each destination — so a re-cut that moved a
    destination's layout reds here rather than at 2am inside a carve. The
    manifest is REQUIRED and not branched on: see `the_landed_manifest()`."""
    _text, doc = the_landed_manifest()
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


def test_the_runbook_per_destination_table_is_the_manifests_own_sum() -> None:
    """§ 2's per-destination table, checked rather than described — EVERY cell
    of it, read from the table itself.

    The paragraph beneath that table says the figures are "summed over the rows
    whose `destination:` names that leg, re-derived here rather than carried
    forward". NOTHING CHECKED THAT until this test, and the four numeric columns
    rotted silently through two acts — `opendox_code` and `openxdox_code` were
    both left at their `880c821c` values while the § 3.4 slice-S5 annotation
    moved both, and the slice-S7 annotation found it. A stale cell here is worse
    than a missing one, because § 2's own sentence tells the operator to read
    the verifier's summary line and compare it with this table.

    THE ROOTS COLUMN HAD ONLY LOOKED CHECKED (Copilot review, this PR).
    `test_the_real_manifest_declares_the_roots_the_runbook_names` compares the
    manifest with a list hard-coded IN THE TEST: it holds the manifest to the
    roots that test names and never opens the runbook, so a roots cell that went
    stale or malformed passed it while this test's own docstring — and § 2's
    paragraph — said the table was checked. So the fifth column is parsed and
    compared here too, and the claim is true of every column it makes. The
    hard-coded test stays: two pins on one fact, one either side of the runbook.

    AND THE PARSER IS PART OF THE CHECK, not a way into it (Copilot review,
    round two on this PR for the duplicate key, round three for the roots cell,
    round four for the rest, round five for the block's own extent): the header
    and ruler are pinned, every remaining line of the block must `fullmatch`
    the record — so a key outside the character class, a sixth column or a
    reshaped cell is a FAILURE and not a skipped line — the roots cell must be
    exactly a comma-separated sequence of backticked paths (or the one
    empty-root marker, pinned WHOLE rather than by its first word), a missing
    runbook — and, round eight, a missing
    MANIFEST — is a failure rather than a branch, the key grammar is the
    VALIDATOR's own `^[a-z][a-z0-9_]*$` rather than a narrower one that would
    refuse a destination the manifest accepts,
    and the BLOCK is bounded by § 2's own two sentences rather than by any
    heuristic for where a table ends — so an interior blank line and a
    malformed row are both failures instead of ways to move the boundary. Each
    of those is a way a table could stop stating what this test says it states
    while the test stayed green.

    THE TWO HALVES OF A ROW ARE READ ON TWO BASES, each the one its column
    claims. The NUMERIC columns are summed by the RAW `destination:` field and
    not by `rows_for()`, which resolves the EFFECTIVE arrival (RULED Q6): the
    table counts a re-destined row at the leg its row still names, which is
    precisely what the paragraph beneath it explains, and reading it the other
    way would make the table disagree with itself. The ROOTS column is the walk
    the verifier performs, which IS `declared_roots(rows_for(...))` — effective,
    because a re-destined row lands in the gaining leg's tree and the walk that
    reads that tree must cover it. NEITHER DOCUMENT IS BRANCHED ON: both are
    required, and this test compares them.
    """
    runbook = REPO_ROOT / "docs" / "opendox-cutover-runbook.md"
    # NEITHER A MISSING RUNBOOK NOR A MISSING MANIFEST IS A BRANCH (Copilot
    # review, this PR: the runbook half in round six, the manifest half in
    # round eight). Branching on either made this invariant VACUOUS exactly
    # when the document it compares disappeared — the check went green on a
    # repository that had lost one of the two things it reads, which is the one
    # state it must not pass. The manifest's absence is a named failure in
    # `the_landed_manifest()`.
    assert runbook.is_file(), (
        f"{runbook} is absent while the manifest is present: § 2's "
        "per-destination table is the operator's comparison for every leg's "
        "arrival run, and a missing table is not a table that agrees")
    _text, doc = the_landed_manifest()
    text = runbook.read_text(encoding="utf-8")

    # THE MARKER SPANS TWO LINES OF THE RUNBOOK and is pinned with its own
    # newline (Copilot review, round eleven on this PR). The sentence it
    # replaced — "these are the numbers each leg's arrival run must report" —
    # was false of the two legs RULED Q6 touches: this table counts a
    # re-destined row at the `destination:` it still names — and a RETIRED one
    # too, which is why the marker sentence names BOTH rulings and this constant
    # moves with it (Copilot review, this pull request): the qualifier said only
    # RULED Q6 while the paragraph below the table had already grown a second
    # subtraction — so `opendox_code`'s run reports 117 arrived where the table says 123
    # (four re-destined away under RULED Q6 and two retired under RULED
    # 5656343213) and `openxdox_code`'s reports 96 where it says 92. A floor that overstated that would be worse
    # than one that says where it stops, which is the rule
    # `test_two_legs_may_apply_one_replicas_line_differently` is written under.
    # A re-wrap of the sentence breaks this anchor LOUDLY, by the count below,
    # rather than quietly moving the block's boundary.
    marker = ("Per destination, counted at the `destination:` each row names "
              "— which is what\neach leg's arrival run reports, save where "
              "RULED Q6 re-destined a row or RULED\n5656343213 retired one "
              "(below):")
    # THE BLOCK IS BOUNDED BY TWO FIXED SENTENCES, not by anything about where
    # a table LOOKS like it ends (Copilot review, rounds five and six on this
    # PR). Round five's extent walked forward across a blank line for as long
    # as anything table-shaped resumed after it, which still let a row that had
    # LOST ITS LEADING `|` end the block: that row was what resumed, it did not
    # look table-shaped, the block stopped above it, and — every destination
    # having appeared before the blank — the key-set check passed while the
    # malformed row went unread. EVERY heuristic for "where the table ends" has
    # that shape, so the boundary stops being a heuristic here. The block is
    # everything BETWEEN § 2's own two sentences — the one that introduces the
    # table and the one that states what its numeric columns mean — each
    # required to appear exactly once and in that order. Only the blank lines
    # that separate the table from those two sentences are trimmed; every line
    # that remains must be the header, the ruler or a record, so an interior
    # blank line and a malformed row are both FAILURES and neither of them can
    # move the boundary.
    terminator = ("The numeric columns are summed over the rows whose "
                  "`destination:` names that")
    assert text.count(marker) == 1, marker
    assert text.count(terminator) == 1, terminator
    start = text.index(marker) + len(marker)
    stop = text.index(terminator)
    assert stop > start, (
        "§ 2 states what the per-destination table's numeric columns mean "
        "BEFORE it introduces the table; the two sentences bound the block, so "
        "their order is part of the bound")
    block = text[start:stop].splitlines()
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    # EVERY LINE OF THE BLOCK IS READ, AND A LINE THAT DOES NOT PARSE IS A
    # FAILURE (Copilot review, this PR). A `match()` that skipped what it could
    # not read let a malformed row — a key outside the character class, a sixth
    # column, a cell in the wrong shape — sit in the table saying something
    # while this test asserted nothing about it, which is the same hole as the
    # duplicate key below one level down: the parser deciding what the check
    # covers. So the header and its ruler are pinned, and every remaining line
    # must `fullmatch` the record.
    header = ("| destination | rows | verbatim / edited | declared edit lines "
              "| declared roots |")
    ruler = "| --- | ---: | ---: | ---: | --- |"
    record = re.compile(
        # The key grammar is the VALIDATOR's, `DESTINATION_KEY_RE =
        # ^[a-z][a-z0-9_]*$` (Copilot review, round six on this PR). A narrower
        # one here refuses a destination the manifest accepts — `code2` would
        # fail this consistency check while the runbook and the manifest agreed
        # perfectly — which makes the test disagree with the floor it checks.
        r"\| `(?P<key>[a-z][a-z0-9_]*)` \| (?P<rows>\d+) \| "
        r"(?:(?P<verbatim>\d+) / (?P<edited>\d+)|—) \| "
        r"(?:(?P<lines>\d+)|—) \| (?P<roots>[^|]*) \|")
    # The roots cell is EXACTLY a comma-separated sequence of backticked paths,
    # or THE one empty-root marker. Anything else — a path that lost its
    # backticks, a word appended after the list — is refused rather than
    # quietly dropped by the `findall` that follows.
    #
    # THE MARKER IS PINNED WHOLE AND NOT BY ITS FIRST WORD (Copilot review,
    # round nine on this PR). `startswith("none")` read one word and let the
    # rest of the cell say anything: `none — stale`, or a sentence that had
    # stopped being true, still produced the EMPTY walk, still matched
    # `declared_roots(...) == []` and still passed every numeric check — so the
    # one cell whose shape this test could not check was the only cell it
    # claims to check as PROSE. The header and the ruler above are pinned
    # exactly for the same reason. When § 3.8 is renumbered this literal moves
    # in the same commit, which is what a marker is for.
    empty_roots = "none — the release identity only (§ 3.8)"
    roots_list = re.compile(r"`[^`]+`(?:, `[^`]+`)*")
    lines = [line.rstrip() for line in block]
    assert lines[0] == header, lines[0]
    assert lines[1] == ruler, lines[1]
    stated: dict[str, tuple[int, int, int, int]] = {}
    roots_stated: dict[str, list[str]] = {}
    for line in lines[2:]:
        found = record.fullmatch(line)
        assert found is not None, (
            "§ 2's per-destination table carries a line this check cannot "
            f"read: {line!r}. A row that does not parse is a row nothing "
            "asserts, so the table's own shape is refused here, not skipped — "
            "and an EMPTY line here is a blank inside the table with rows "
            "still below it, which would otherwise end the block and hide "
            "every one of them")
        # ONE AUTHORITATIVE ROW PER DESTINATION, refused HERE rather than
        # silently resolved (Copilot review, this PR). Assigning straight into
        # `stated` lets a later CORRECT row overwrite an earlier STALE
        # duplicate, so a table that has stopped having one entry per leg
        # still passes every numeric check below — the defect this test exists
        # to catch, hidden by the parser that feeds it. The table's SHAPE is
        # part of what the table states.
        assert found["key"] not in stated, (
            f"the runbook's per-destination table names {found['key']!r} more "
            "than once; a duplicate row is a stale figure standing behind a "
            "fresh one, and the sums below read only the last of them")
        stated[found["key"]] = (
            int(found["rows"]),
            int(found["verbatim"] or 0),
            int(found["edited"] or 0),
            int(found["lines"] or 0),
        )
        # THE FIFTH COLUMN IS A CLAIM TOO: every backticked path in the cell,
        # in the order the cell states them. A cell that names no path at all
        # (`opendox_root`'s "none — the release identity only") claims the
        # EMPTY walk, and it is the only cell allowed to be prose — that one
        # prose cell being pinned whole, above.
        roots_cell = found["roots"]
        if "`" in roots_cell:
            assert roots_list.fullmatch(roots_cell), (
                f"the roots cell for {found['key']!r} is not a comma-separated "
                f"sequence of backticked paths: {roots_cell!r}. An unbackticked "
                "path reads as a declared root to an operator and as nothing to "
                "the comparison below")
            roots_stated[found["key"]] = re.findall(r"`([^`]+)`", roots_cell)
        else:
            assert roots_cell == empty_roots, (
                f"the roots cell for {found['key']!r} names no path and is "
                f"not the empty-root marker {empty_roots!r}: {roots_cell!r}. "
                "A cell that begins 'none' and then says something else is a "
                "cell this check would read as the empty walk while the "
                "sentence beside it went unread")
            roots_stated[found["key"]] = []
    assert set(stated) == set(doc["destinations"]), sorted(stated)

    for key, claimed_roots in roots_stated.items():
        # The walk this destination's arrival run performs, computed from the
        # manifest exactly as `verify-carve-arrival.py` computes it.
        walked = MODULE.declared_roots(MODULE.rows_for(doc, key))
        assert claimed_roots == walked, (key, claimed_roots, walked)

    for key, claimed in stated.items():
        rows = [row for row in doc["rows"] if row.get("destination") == key]
        summed = (
            len(rows),
            sum(1 for row in rows if row["disposition"] == "moved_verbatim"),
            sum(1 for row in rows
                if row["disposition"] == "moved_with_declared_edit"),
            sum(len(edit["lines"]) for row in rows
                for edit in row.get("edits") or []),
        )
        assert claimed == summed, (key, claimed, summed)

    # AND THE ONE INVARIANT THAT TIES THE TABLE TO THE AGGREGATE ABOVE IT: a
    # replica row names no destination at all, so the per-leg figures sum to
    # the manifest's declared-line total MINUS the lines such rows declare
    # (RULED Q-L7 (a), § 2's own "the two replica lines belong to no
    # destination column below").
    #
    # THE SUBTRAHEND IS RE-DERIVED AND USED TO BE THE CONSTANT `1` (the
    # pre-existing `openxdox_code` annotation, `#656` CLAIM `5656688910`). The
    # replica row declared exactly one line from RULED Q-L7 (a) until that act
    # declared openXdox-code#14's `:271` beside it, and the constant would have
    # refused a lawful document for the one thing the grammar explicitly
    # permits: `edits:` is a field of a ROW, so a replica row may declare as
    # many lines as its copies differ on, and Q-L7 (a) bounds the LINE and
    # never the count. What must hold is that the columns exhaust exactly the
    # rows that HAVE a destination — which is what this now states, and what
    # the sentence beneath the table says in words.
    total = sum(len(edit["lines"]) for row in doc["rows"]
                for edit in row.get("edits") or [])
    no_destination = sum(len(edit["lines"]) for row in doc["rows"]
                         if not row.get("destination")
                         for edit in row.get("edits") or [])
    assert sum(claimed[3] for claimed in stated.values()) == (
        total - no_destination), (stated, total, no_destination)


# --------------------------------------------------------------------------
# § 2's FIRST table and the sentence beneath it — the same measurement the
# per-destination table states, stated over the WHOLE document
# --------------------------------------------------------------------------

# § 2's own two sentences bound the block, for the per-destination parser's
# reason: every heuristic for "where the block ends" is a boundary the document
# can move without anyone noticing it moved.
# § 2 spells small counts as WORDS, so the check that the cell states the
# current one has to spell it the same way. Beyond this table the digits are
# compared instead — a runbook that reaches eleven declared lines on one
# replica row has a bigger problem than its spelling.
NUMBER_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}

DISPOSITION_MARKER = "mapping manifest. Measured in the landed file:"
DISPOSITION_TERMINATOR = "**AND A MOVED ROW MAY CARRY `re_destined:`"
DISPOSITION_HEADER = ("| disposition | rows | the proof owed at the "
                      "destination |")
DISPOSITION_RULER = "| --- | ---: | --- |"
DISPOSITION_RECORD = re.compile(
    r"\| `(?P<disposition>[a-z][a-z0-9_]*)` \| \*\*(?P<rows>\d+)\*\* \| "
    r"(?P<proof>[^|]*) \|")
# The totals sentence, whitespace-normalised: four numbers and the class list,
# each of which is a sum over the landed manifest.
TOTALS = re.compile(
    r"\*\*(?P<moved>\d+) rows move\. (?P<lines>\d+) declared edit lines\*\*: "
    r"(?P<classes>[^.]+)\. \*\*(?P<carriers>\d+) rows carry `edits:`\*\* — "
    r"the (?P<edited>\d+) `moved_with_declared_edit` rows and, since RULED "
    r"Q-L7 \(a\), one replica row\.")
MOVED_DISPOSITIONS = ("moved_verbatim", "moved_with_declared_edit")


def test_the_runbook_disposition_table_and_totals_are_the_manifests_own(
        ) -> None:
    """§ 2's FIRST table and the totals sentence under it, re-derived — the pin
    the paragraph below them already claims to be.

    § 2 says of these figures that they are "the same measurement
    `scripts/validate-carve-manifest.py` prints and
    `tests/carve_manifest/test_carve_manifest.py::test_the_real_manifest_carries_the_ruled_q_l7_amendment`
    pins ... a transcribed count is a claim, a summed one is a measurement".
    THAT TEST NEVER OPENS THIS DOCUMENT (Copilot review, round eleven on this
    PR). It pins the MANIFEST's own aggregate — `(2621, 176)` and the 20
    replica rows — which is a claim about the file and not about the sentence
    that transcribes it. So every cell here (three disposition counts, the
    replica count, the three per-class totals, the moved-row total, the carrier
    total) was a transcription nothing compared with the thing transcribed,
    which is exactly how the per-destination table below rotted through two
    acts while its own paragraph said it was re-derived.

    THE BLOCK IS BOUNDED BY § 2'S OWN TWO SENTENCES and split into EXACTLY TWO
    paragraphs, the table and the totals. A third paragraph between them, a
    blank line inside the table, or a row that does not parse is a FAILURE here
    rather than a way to move the bound — the per-destination parser's rule,
    and for the reason its docstring gives.

    WHAT IT DELIBERATELY DOES NOT PIN: the two DELTA sentences that follow
    ("+162 declared lines", "+782 declared lines over 33 `opendox_code` rows,
    17 of them converted"). A delta is a claim about the PREVIOUS state of the
    file, which the landed manifest does not carry; those are pinned where the
    previous state is known, in `tests/carve_manifest/test_carve_manifest.py`'s
    slice window (`1584 + 782 == 2366`, `159 + 17 == 176`).
    """
    runbook = REPO_ROOT / "docs" / "opendox-cutover-runbook.md"
    assert runbook.is_file(), (
        f"{runbook} is absent while the manifest is present: § 2's first table "
        "is the floor's own summary, and a missing table is not a table that "
        "agrees")
    _text, doc = the_landed_manifest()
    text = runbook.read_text(encoding="utf-8")
    validator = _load_manifest_validator()

    assert text.count(DISPOSITION_MARKER) == 1, (
        f"§ 2's disposition table is bounded by {DISPOSITION_MARKER!r}, which "
        f"this runbook states {text.count(DISPOSITION_MARKER)} times")
    assert text.count(DISPOSITION_TERMINATOR) == 1, (
        f"§ 2's totals paragraph is bounded by {DISPOSITION_TERMINATOR!r}, "
        f"which this runbook states {text.count(DISPOSITION_TERMINATOR)} times")
    start = text.index(DISPOSITION_MARKER) + len(DISPOSITION_MARKER)
    stop = text.index(DISPOSITION_TERMINATOR)
    assert stop > start, (
        "§ 2 states the `re_destined:` grammar BEFORE it introduces the "
        "disposition table; the two sentences bound the block, so their order "
        "is part of the bound")
    blocks = [block for block in text[start:stop].split("\n\n")
              if block.strip()]
    assert len(blocks) == 2, (
        "§ 2's opening two sentences bound "
        f"{len(blocks)} paragraphs and this check reads exactly two — the "
        "disposition table and the totals sentence. A third paragraph between "
        "them is a claim nothing here asserts, and a blank line inside the "
        "table would end it early and hide every row below")

    table = [line.rstrip() for line in blocks[0].strip("\n").split("\n")]
    assert table[0] == DISPOSITION_HEADER, table[0]
    assert table[1] == DISPOSITION_RULER, table[1]
    stated: list[tuple[str, int]] = []
    proofs: dict[str, str] = {}
    for line in table[2:]:
        found = DISPOSITION_RECORD.fullmatch(line)
        assert found is not None, (
            "§ 2's disposition table carries a line this check cannot read: "
            f"{line!r}. A row that does not parse is a row nothing asserts, so "
            "the table's own shape is refused here and not skipped")
        assert found["disposition"] not in proofs, (
            f"§ 2's disposition table names {found['disposition']!r} more than "
            "once; a duplicate row is a stale figure standing behind a fresh "
            "one")
        stated.append((found["disposition"], int(found["rows"])))
        proofs[found["disposition"]] = found["proof"]
    # THE VOCABULARY IS THE VALIDATOR'S, verbatim AND IN ORDER (RULED OQ-1's
    # own "three, not four"): a disposition the manifest can carry and this
    # table does not state is a row class with no proof owed against it.
    assert [name for name, _ in stated] == list(validator.DISPOSITIONS), (
        [name for name, _ in stated], list(validator.DISPOSITIONS))

    for name, claimed in stated:
        summed = sum(1 for row in doc["rows"] if row["disposition"] == name)
        assert claimed == summed, (name, claimed, summed)
    assert sum(claimed for _, claimed in stated) == len(doc["rows"]), (
        "§ 2's three disposition counts do not sum to the manifest's row "
        f"count ({len(doc['rows'])}): the table claims to exhaust the "
        "document, so a row in no stated class is a row nothing owes a proof "
        "for")

    # THE REPLICA CLAUSE inside the `not_moved` cell. All three halves are the
    # manifest's: how many replica rows there are, that exactly ONE of them
    # declares lines (RULED Q-L7 (a)) — the second replica to declare any makes
    # this sentence false, and says so here — and HOW MANY that one declares,
    # which moved from one to two at the pre-existing `openxdox_code`
    # annotation (`#656` CLAIM `5656688910`) and is pinned rather than reworded.
    replicas = [row for row in doc["rows"]
                if row.get("reason") == MODULE.REPLICA_REASON]
    cell = proofs["not_moved"]
    assert f"**{len(replicas)}** `{MODULE.REPLICA_REASON}` rows" in cell, (
        f"§ 2's `not_moved` cell does not state the manifest's "
        f"{len(replicas)} `{MODULE.REPLICA_REASON}` rows: {cell!r}")
    declaring = [row for row in replicas if row.get("edits")]
    assert len(declaring) == 1, (
        "§ 2's `not_moved` cell says ONE replica row declares lines and the "
        f"landed manifest has {len(declaring)}: "
        f"{[row['source_path'] for row in declaring]}. The sentence is the "
        "reason the human summary line reads `verified (byte-identical, or …)`")
    assert "**one of them declares lines**" in cell, cell
    declared_on_it = sum(len(edit["lines"]) for edit in declaring[0]["edits"])
    spelled = NUMBER_WORDS.get(declared_on_it, str(declared_on_it))
    assert f"one line at that ruling, {spelled} today" in cell, (
        f"§ 2's `not_moved` cell does not state the {declared_on_it} line(s) "
        f"the one declaring replica row carries today: {cell!r}")

    # THE TOTALS SENTENCE — four numbers and a class list, each a sum.
    prose = " ".join(blocks[1].split())
    found = TOTALS.match(prose)
    assert found is not None, (
        "§ 2's totals sentence is not in the shape this check reads: "
        f"{prose[:240]!r}. It states the document's four aggregate figures, so "
        "a reshaped sentence is a claim nothing here compares with the "
        "manifest")
    lines_total = sum(len(edit["lines"]) for row in doc["rows"]
                      for edit in row.get("edits") or [])
    # THE CLASSES ARE THE LANDED MANIFEST'S OWN `edit_classes:` LIST, in its
    # order — the list `validate-carve-manifest.py` asserts EQUAL to RULED
    # OQ-1's three. A class with lines and no place in this sentence would
    # otherwise be invisible here and visible in the total, which is the next
    # assertion.
    per_class = [
        (name, sum(len(edit["lines"]) for row in doc["rows"]
                   for edit in row.get("edits") or []
                   if edit["class"] == name))
        for name in doc["edit_classes"]]
    assert found["classes"] == ", ".join(
        f"`{name}` {total}" for name, total in per_class), (
        found["classes"], per_class)
    assert sum(total for _, total in per_class) == lines_total, (
        per_class, lines_total)
    assert int(found["lines"]) == lines_total, (found["lines"], lines_total)
    moved = sum(1 for row in doc["rows"]
                if row["disposition"] in MOVED_DISPOSITIONS)
    assert int(found["moved"]) == moved, (found["moved"], moved)
    carriers = sum(1 for row in doc["rows"] if row.get("edits"))
    assert int(found["carriers"]) == carriers, (found["carriers"], carriers)
    edited = sum(1 for row in doc["rows"]
                 if row["disposition"] == "moved_with_declared_edit")
    assert int(found["edited"]) == edited, (found["edited"], edited)
    # AND THE SENTENCE'S OWN ARITHMETIC: the carriers are the edited rows plus
    # the replica rows that declare lines, which is what makes 176 one more
    # than 175 and the one figure a reader is most likely to "correct".
    assert carriers == edited + len(declaring), (carriers, edited, declaring)


# --------------------------------------------------------------------------
# § 5.5's worked example — the invocation an operator copies, and the line the
# runbook tells that operator to expect back
# --------------------------------------------------------------------------

# Each example is the ```sh block that FOLLOWS one of § 5.5's own sentences.
# The sentence is the bound, for the § 2 table test's reason: a heuristic for
# "the block near here" is a boundary the document can move without anyone
# noticing it moved.
PHASE_A_MARKER = "`arrival-unreadable` rather than holding a seat:"
PHASE_B_MARKER = ("**Only then** apply the declared edits as commit B, "
                  "and re-verify at phase B:")
# `…` elides, `<name>` stands for a value the operator supplies (`<origin/main>`
# is a ref, and the verifier prints the sha it resolved to). Everything BETWEEN
# them is the tool's own words and is compared with them.
ELISION = re.compile(r"…|<[^>]+>")


def _runbook_example(text: str, marker: str) -> tuple[list[str], str]:
    """The fenced example after `marker`, as (argv, the quoted expectation).

    FAIL-CLOSED AT EVERY STEP, because each way of being lenient here is a way
    for the check to stop reading what it says it reads: the marker appears
    exactly once, the fence opens immediately beneath it, the `# ` quotation is
    a CONTIGUOUS run at the END of the block — a comment among the command's
    own lines is a shape this parser refuses rather than silently drops — and
    both halves are non-empty.
    """
    assert text.count(marker) == 1, (
        f"§ 5.5's example is bounded by {marker!r}, which this runbook states "
        f"{text.count(marker)} times")
    rest = text[text.index(marker) + len(marker):]
    opening = "\n\n```sh\n"
    assert rest.startswith(opening), (
        f"the fenced invocation does not open immediately under {marker!r}: "
        f"{rest[:60]!r}")
    body = rest[len(opening):]
    closing = body.find("\n```\n")
    assert closing != -1, f"the invocation under {marker!r} is never closed"
    lines = body[:closing].split("\n")
    quoted: list[str] = []
    while lines and lines[-1].startswith("#"):
        quoted.insert(0, lines.pop()[1:].strip())
    assert lines, f"the block under {marker!r} is all comment and no command"
    assert quoted, (
        f"the block under {marker!r} states no `# expect exit 0:` line; an "
        "example with no expectation is an invocation nobody can check a run "
        "against")
    assert not any(line.lstrip().startswith("#") for line in lines), (
        f"the invocation under {marker!r} carries a comment among its own "
        "lines; this check reads the trailing run as the expectation, so a "
        "comment above the command would be read as part of it")
    argv = shlex.split(" ".join(line.rstrip("\\ ") for line in lines))
    return argv, " ".join(quoted)


def _flag(argv: list[str], flag: str) -> list[str]:
    """Every value given to `flag`, in the order the invocation gives them."""
    return [argv[i + 1] for i, word in enumerate(argv)
            if word == flag and i + 1 < len(argv)]


def _composed(summary: dict[str, Any],
              capsys: pytest.CaptureFixture[str]) -> str:
    """The verifier's own summary line for `summary` — the tool's words."""
    MODULE._print_ok(summary, False)
    return capsys.readouterr().out.strip()


def _summary(doc: dict[str, Any], destination: str, phase: str, *,
             rows: int, digests: int, diffed: int, unapplied: int,
             replicas: int) -> dict[str, Any]:
    """A summary the verifier would build for a run of § 5.5's example.

    Only the counted fields are asserted on; the rest are this destination's
    own identity, so the composed line is the one this leg prints and not a
    shape assembled out of nothing.
    """
    return {
        "result": "ok",
        "mode": "destination",
        "destination": destination,
        "repository": (doc["destinations"].get(destination) or {}).get(
            "repository"),
        "leg": None,
        "dest_root": "../dest-openDox-code",
        "phase": phase,
        # A run that PRINTS the strong scaffold sentence is the one § 5.5's
        # phase-A comment quotes; `None` here prints the weaker `by NAME ONLY`
        # alternative, which is a different claim and a different line.
        "dest_base": "0" * 40,
        "carve_commit": doc["carve_commit"],
        "carve_tag": doc.get("carve_tag"),
        "source_repository": doc["source_repository"],
        "rows": rows,
        "digests_verified": digests,
        "declared_edits_diffed": diffed,
        "declared_edits_unapplied": unapplied,
        "replicas_declared": replicas,
        "replicas_verified": replicas,
        "re_destined": {"arrived": [], "vacated": []},
        "declared_roots": MODULE.declared_roots(
            MODULE.rows_for(doc, destination)),
        "files_walked": 0,
        "admitted": {"scaffold": 0, "replica": 0, "created": 0},
        "carved_from": None,
        "admissions_file": None,
        "declared_admissions_used": [],
        "declared_admissions_unused": [],
        "ad_hoc_allow_created": [],
    }


def _declared_replica_row(doc: dict[str, Any], value: str,
                          destination: str) -> dict[str, Any]:
    """The manifest row `--replica-at VALUE` names, refused where there is none.

    `parse_replica_placements` admits a left side that is a
    `replicated_at_destination` row's `source_path` or — RULED Q-L7 (a) — a
    moved row's where the manifest replicates it HERE, and refuses
    `arrival-unreadable` for anything else: an example that named something
    else would not run at all. The ROW is also what decides the figure below,
    because a replica whose row declares lines is counted with the moved rows'
    declared edits at phase B (`check_replicas` -> `counts["diffed"]`).
    """
    source_path = value.partition("=")[0]
    admissible = {row["source_path"] for row in MODULE.replica_rows(doc)}
    admissible |= {row["source_path"]
                   for row in MODULE.also_replicated_rows(doc, destination)}
    assert source_path in admissible, (
        f"§ 5.5's example declares `--replica-at {value}`, and at "
        f"{destination!r} that left side is neither a replica row of the "
        "landed manifest nor a moved row it also replicates here. The "
        "verifier refuses `arrival-unreadable` for exactly that, so the "
        "invocation an operator copies would not run")
    rows = [row for row in doc["rows"]
            if row.get("source_path") == source_path]
    assert len(rows) == 1, (source_path, len(rows))
    return rows[0]


def test_the_runbook_phase_examples_are_the_arrival_the_manifest_produces(
        capsys: pytest.CaptureFixture[str]) -> None:
    """§ 5.5's two worked invocations, held to the landed manifest AND to the
    line this verifier composes — § 2's pin, one section down.

    § 2's per-destination table rotted through two acts because nothing read
    it. THESE TWO COMMENTS HAD ROTTED FURTHER (Copilot review, round ten on
    this PR): they were written when the runbook landed (`a970fd9d`) and never
    touched again, so phase A still told an operator to expect `123 row(s)
    arrived` after RULED Q6 re-destined four of `opendox_code`'s rows away,
    and phase B still expected `62 edited row(s), declared-lines-only` —
    a figure six annotation acts out of date, in words this verifier does not
    print at all. An expectation the tool would never produce cannot be
    compared with a run, so it fails silently forever: the operator reads the
    difference as their own mistake, or does not read it.

    SO THE EXPECTATION IS COMPOSED RATHER THAN MATCHED. The numbers come from
    the landed manifest through `rows_for()` — the EFFECTIVE arrival, which is
    what a run places and therefore what a run reports — and the WORDS come
    from `_print_ok`, the verifier's own summary line, with the runbook's `…`
    elisions and its one `<origin/main>` placeholder as the only wildcards.
    Each remaining fragment must appear, in order, in that line. A wording
    change in the tool, a figure moved by an annotation act, and a comment
    edited to say something the tool does not say are all the same failure.

    AND THE EXAMPLE'S OWN REPLICA FLAGS ARE PART OF THE ARITHMETIC (Copilot
    review, round eleven). A `--replica-at` whose ROW declares lines is a
    declared-edit row at phase B, counted with the moved rows' edits, so the
    phase-B figure is this leg's EFFECTIVE `moved_with_declared_edit` count PLUS
    one per such flag — derived from the invocation and from the manifest rather
    than carried, which is what let the fourth flag land in the same commit as the
    figure it produces, `85` then and `83` since RULED 5656343213 retired two of
    this leg's edited rows. A derivation is what makes a figure survive an act
    nobody was thinking about when the example was written.

    THE MODULE IS IMPORTED HERE, against this file's subprocess rule, for the
    reason the docstring gives for the constant assertions: the claim is about
    the LINE THE TOOL COMPOSES, not about a run. Every behavioural claim about
    a real destination stays where it is — no destination checkout exists on
    this machine, which is the seat the module docstring describes.

    AND THE AD-HOC `--allow-created` FLAGS ARE READ AGAINST THE ADMISSIONS
    FILE. § 5.5's note says in prose that those two flags are correct only
    while `opendox_code` declares neither path — and the sentence under it
    predicts its own expiry. That prediction is checked here, so the day a PR
    declares `pytest.ini` or `conftest.py` is a red test rather than a note
    nobody re-reads. (The note's OTHER premise had already expired unread: it
    said the block was `created: []` long after BUILD slice 2 began filling
    it.)
    """
    runbook = REPO_ROOT / "docs" / "opendox-cutover-runbook.md"
    assert runbook.is_file(), (
        f"{runbook} is absent: § 5.5 is the procedure every leg runs, and a "
        "missing procedure is not a procedure that agrees with the manifest")
    _text, doc = the_landed_manifest()
    text = runbook.read_text(encoding="utf-8")

    destination = "opendox_code"
    rows = MODULE.rows_for(doc, destination)
    verbatim = sum(1 for row in rows
                   if row["disposition"] == "moved_verbatim")
    edited = sum(1 for row in rows
                 if row["disposition"] == "moved_with_declared_edit")
    assert len(rows) == verbatim + edited, (
        "every row `rows_for` returns is a MOVED row, so the two dispositions "
        "exhaust it; a third here would mean the arrival counts below no "
        "longer sum to the rows the run walks")

    for marker, phase, expected in (
            # Phase A checks EVERY arrived row's digest, so its two figures
            # are one figure twice. Phase B checks the verbatim rows' digests
            # and diffs the declared-edit rows within their lines; `0
            # unapplied` is the standard for a complete commit B, not a
            # manifest figure.
            (PHASE_A_MARKER, "A", (len(rows), len(rows), 0, 0)),
            (PHASE_B_MARKER, "B", (len(rows), verbatim, edited, 0))):
        argv, quotation = _runbook_example(text, marker)
        assert _flag(argv, "--destination") == [destination], (
            f"§ 5.5's phase-{phase} example does not run {destination!r}; the "
            "figures below are that leg's and no other's")
        assert _flag(argv, "--phase") == [phase], (
            f"the example under {marker!r} does not run phase {phase}")
        prefix = "expect exit 0: "
        assert quotation.startswith(prefix), (
            f"§ 5.5's phase-{phase} expectation does not begin {prefix!r}: "
            f"{quotation!r}")
        # THE EXAMPLE'S OWN `--replica-at` FLAGS MOVE ITS FIGURES (Copilot
        # review, round eleven on this PR). A declared replica whose ROW
        # declares lines is a DECLARED-EDIT ROW at phase B — `check_replicas`
        # adds it to the same counter the moved rows use — so the phase-B
        # expectation is one above this leg's `moved_with_declared_edit` count
        # for each such flag. Held here rather than transcribed: the round that
        # added the Q-L7 conftest flag to the phase-B example moved `84` to
        # `85` and `3 of 3` to `4 of 4`, and a test whose expectation did not
        # move with the example's own command line could not have checked
        # either figure. BOTH LINE FIGURES HAVE SINCE FALLEN BY TWO — `82` + 1
        # = `83` — because RULED 5656343213 retired two of this leg's edited
        # rows; the replica arithmetic is untouched, which is the whole point
        # of deriving it. At phase A the copies are not placed yet (§ 5.5's
        # phase-A paragraph, measured at this leg's commit A), so a flag there
        # would refuse `arrival-missing` and the arithmetic stays the rows'.
        placements = _flag(argv, "--replica-at")
        declaring = sum(
            1 for value in placements
            if _declared_replica_row(doc, value, destination).get("edits"))
        # AND EVERY REPLICA ROW THAT DECLARES LINES IS DECLARED BY THE PHASE-B
        # EXAMPLE (§ 5.6's "the two RULED Q-L7 (a) placements, which BOTH
        # `-code` legs owe"; RULED Q-L7 (a)'s "applied identically at every
        # replica"). This is the defect the round-eleven finding names, and it
        # is not one the composition above can see: with the flag absent AND
        # the figures matching, the composed line agreed with the runbook while
        # the invocation itself had stopped running. Once a leg applies the
        # declared line — `opendox_code` did, at `3954d78` (#19) — the copy's
        # bytes are no blob at the carve commit, so an UNDECLARED copy is
        # `arrival-undeclared-file` and the example refuses at the destination
        # it is written for. A later line-declaring replica that this leg does
        # NOT place makes this assertion the re-read it should be: § 5.6 names
        # who owes which placement, and the example follows it.
        if phase == "B":
            declared_here = {value.partition("=")[0] for value in placements}
            owed = {row["source_path"] for row in MODULE.replica_rows(doc)
                    if row.get("edits")}
            assert owed <= declared_here, (
                "§ 5.5's phase-B example declares no `--replica-at` for "
                f"{sorted(owed - declared_here)}, whose row(s) DECLARE LINES "
                "(RULED Q-L7 (a)) and which § 5.6 says both `-code` legs "
                "place. A copy carrying its declared line and left undeclared "
                "is `arrival-undeclared-file`, so this example would refuse at "
                "the leg it is written for")
        line = _composed(_summary(
            doc, destination, phase,
            rows=expected[0], digests=expected[1],
            diffed=expected[2] + (declaring if phase == "B" else 0),
            unapplied=expected[3],
            replicas=len(placements)), capsys)
        position = 0
        for fragment in ELISION.split(quotation[len(prefix):]):
            fragment = fragment.strip()
            if not fragment:
                continue
            found = line.find(fragment, position)
            assert found != -1, (
                f"§ 5.5's phase-{phase} example says a run reports "
                f"{fragment!r}, and the line this verifier composes for that "
                f"run — from the LANDED manifest — is {line!r}. The runbook "
                "states what an operator compares their own run against, so "
                "a figure or a phrase it states and this tool does not print "
                "is an expectation no run can meet")
            position = found + len(fragment)

    # THE AD-HOC ADMISSION FLAGS, against the file that would replace them.
    admissions = REPO_ROOT / "docs" / MODULE.ADMISSIONS_BASENAME
    assert admissions.is_file(), (
        f"{admissions} is absent while § 5.5 names it: the note under the "
        "phase-B example is a claim about that file's contents")
    declared = {
        entry["path"] for entry in
        ((yaml.safe_load(admissions.read_text(encoding="utf-8"))
          ["destinations"].get(destination) or {}).get("created") or [])}
    argv, _quotation = _runbook_example(text, PHASE_B_MARKER)
    for path in _flag(argv, "--allow-created"):
        assert path not in declared, (
            f"§ 5.5's phase-B example still passes `--allow-created {path}` "
            f"while {MODULE.ADMISSIONS_BASENAME} declares that path for "
            f"{destination}. The note beneath the example says this is the "
            "moment the flag should be dropped and the note deleted with it")


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
    manifest validator's suite. The manifest is REQUIRED and not branched on:
    see `the_landed_manifest()`."""
    _text, doc = the_landed_manifest()
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
    and the runbook's § 7 can go back to a `--destination`. The manifest is
    REQUIRED and not branched on: see `the_landed_manifest()`."""
    _text, doc = the_landed_manifest()
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


def test_an_admission_declared_under_an_ALIAS_of_the_destination_admits(
        carve: Carve) -> None:
    """THE GOVERNED ADMISSIONS PATH READS THE REAL DESTINATION, not the CLI
    label (Copilot review, PR #1025, accurate).

    `check_shape` admits two `destinations:` keys sharing one
    `{repository, leg}` body on purpose, and every other reader in the tool
    resolves a key to that body. The admissions selection did not: it was
    `.get(args.destination)`, so a `created:` entry filed under one alias made
    the SAME CHECKOUT pass through that key and refuse
    `arrival-undeclared-file` through the other. A verdict that depends on
    which name the caller typed is not a verdict about the tree."""
    doc = carve.manifest_doc()
    doc["destinations"]["scratch_code_alias"] = dict(
        doc["destinations"]["scratch_code"])
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/created.py").write_text("CREATED = 1\n", encoding="utf-8")
    admissions = _admissions_doc({"scratch_code": []})
    admissions["destinations"]["scratch_code_alias"] = {
        "created": [_entry("src/pkg/created.py")]}
    carve.write_admissions(admissions)
    for key in ("scratch_code", "scratch_code_alias"):
        done = run(carve, manifest, "--destination", key,
                   "--dest-root", str(dest), "--phase", "A", "--json")
        assert done.returncode == 0, (key, done.stdout + done.stderr)
        payload = json.loads(done.stdout)
        assert payload["declared_admissions_used"] == [
            "src/pkg/created.py"], (key, payload)


def test_one_path_admitted_under_TWO_aliases_of_one_leg_refuses(
        carve: Carve) -> None:
    """The explicit duplicate rule the union needs. `read_admissions` already
    refuses a repeat WITHIN one destination's list because a file cannot have
    two provenances; the same claim spelled under an alias is the same claim
    about the same leg, with two `since` values and no rule saying which is the
    file's. Refused rather than silently collapsed — two entries are two review
    decisions, and this file's whole design is that an admission is a one-line
    diff somebody read."""
    doc = carve.manifest_doc()
    doc["destinations"]["scratch_code_alias"] = dict(
        doc["destinations"]["scratch_code"])
    manifest = carve.write_manifest(doc)
    dest = carve.materialise(doc, "scratch_code")
    (dest / "src/pkg/created.py").write_text("CREATED = 1\n", encoding="utf-8")
    admissions = _admissions_doc(
        {"scratch_code": [_entry("src/pkg/created.py")]})
    admissions["destinations"]["scratch_code_alias"] = {
        "created": [_entry("src/pkg/created.py", reason="the alias's copy")]}
    carve.write_admissions(admissions)
    done = run(carve, manifest, "--destination", "scratch_code",
               "--dest-root", str(dest), "--phase", "A", "--json")
    assert refusal(done) == "arrival-unreadable"
    detail = json.loads(done.stdout)["detail"]
    assert "scratch_code_alias" in detail, detail
    assert "twice for one real destination" in detail, detail


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

    AMENDED A SIXTH TIME by § 3.4 SLICE S7's own annotation PR (RULED
    Q1/Q2/Q7, `#656` comment 5648049748; S7 CLAIM `#656` comment 5649148461):
    three more `opendox_code` files — the DISPLAY facet's two halves
    (`src/opendox/display_profile.py`, `src/opendox/web/views/display.js`,
    introduced together) and the suite that holds one against the other
    (`tests/test_display_facet.py`) — admitted the governed way on the same
    Q-L1 footing as every bump above (the leg PR, opensoft/openDox-code#21,
    pairs with — and lands after — this annotation PR). Same footing again:
    checked by presence, not equality. It is pinned here at all because
    Copilot's review of the annotation PR observed that these three were the
    FIRST bump to arrive carrying only the generic shape/sort checks below:
    without an exact path+`since` pin, swapping one for another well-formed
    entry, or dropping one while adding another, passes every local test and
    lets the governed admission claim drift silently.
    AMENDED A SEVENTH TIME by § 3.4 SLICE S8's own annotation PR (`#656`
    comment `5649985838`): one more `openxdox_code` file,
    `tests/opendox_bundle.py` — the module through which that leg's 31
    mis-pointed suites read the PINNED openDox bundle (§ 1.2(d)'s measured
    defect: they resolved `REPO_ROOT / "src" / "openxdox" / "web"`, a
    directory openXdox-code does not have), and which builds RULED Q5's
    COMPOSED root for the four suites asserting across the seam. Admitted the
    governed way because the leg PR that lands it (opensoft/openXdox-code#19)
    pairs with — and lands after — this annotation PR. Checked by PRESENCE and
    by its own `since`, the same footing as every bump above; added to these
    durable assertions in the same act that declared it, on Copilot's review of
    PR #1025 (accurate: the generic shape checks below admit any well-formed
    entry, so this path and its provenance commit could have been changed or
    dropped without a failure).

    What is durable is asserted in place of the frozen content: the two
    RULED openxdox_code seed entries (the measured defect this file repairs,
    `#656` comment 5639058687), the three RULED Q5 opendox_code entries, the
    five PR #1001 opendox_code entries, the one § 3.4 SLICE S6 entry, the
    four § 3.4 SLICE S4 entries, and the three § 3.4 SLICE S7 entries are
    still declared with their own
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
    # THE SEVENTH BUMP: § 3.4 SLICE S8's own `openxdox_code` file (`#656`
    # comment `5649985838`), admitted the GOVERNED way on the same Q-L1
    # footing as every bump below (the leg PR, opensoft/openXdox-code#19,
    # pairs with — and lands after — this annotation PR). `since` is the
    # file's OWN introducing commit (`git log --diff-filter=A`), not the leg
    # branch's later tip — the provenance contract the FOURTH and FIFTH bumps
    # below state.
    assert "tests/opendox_bundle.py" in seed, (
        "tests/opendox_bundle.py is § 3.4 SLICE S8's own new file (`#656` "
        "comment 5649985838) and is no longer declared for openxdox_code")
    assert seed["tests/opendox_bundle.py"]["since"] == (
        "c8e4a59bd8eab231e5903e26b2a9b08e9e527fba")
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
    # TWO OF S4's THREE MOVED ON AT § 3.4 SLICE S5. `views/gate-lens.js` and
    # `views/gate-projects.js` are CREATED files with no manifest row (RULED
    # OQ-C), so the gate loop's re-destination cannot carry them in a
    # `re_destined:` field — that field belongs to a ROW. They move by
    # ADMISSION instead: removed from `opendox_code`'s list and added to
    # `openxdox_code`'s in the same diff, which is the whole of what "this file
    # moved legs" can mean for a file the manifest never described. Asserted
    # BOTH WAYS here, because a one-sided move is exactly the drift that
    # produces a STALE admission the verifier reports and nobody reads.
    for path in ("src/opendox/web/views/gate-lens.js",
                 "src/opendox/web/views/gate-projects.js"):
        assert path not in opendox_seed, (
            f"{path} left opendox_code at § 3.4 SLICE S5 (`#656` comment "
            "5648044785, RULED Q5) and its admission there is STALE")
        openxdox_path = path.replace("src/opendox/", "src/openxdox/")
        assert openxdox_path in seed, (
            f"{openxdox_path} is one of the two CREATED class-B modules § 3.4 "
            "SLICE S5 re-homes by admission and is not declared for "
            "openxdox_code")
        assert seed[openxdox_path]["since"] == (
            "8a3355889fcc9cd40efa03ee9d007dedc5d14f2a")
    assert "src/opendox/web/views/projection-index.js" in opendox_seed, (
        "src/opendox/web/views/projection-index.js is § 3.4 SLICE S4's own "
        "snapshot-index module (`#656` comment 5642758731), which S5 does NOT "
        "move — it is not a ViewBinding (§ 4.2) — and is no longer declared "
        "for opendox_code")
    assert opendox_seed["src/opendox/web/views/projection-index.js"]["since"] == (
        "031edc9b4268d9898c296b2e9bb3951a78642fb6")
    # § 3.4 SLICE S5's own created files, both legs, on the same footing.
    for path, since in (
            ("src/openxdox/serve_views.py",
             "01b06c940fa9f62c9b10f369b0843c4088690d49"),
            ("src/openxdox/view_extensions.py",
             "01b06c940fa9f62c9b10f369b0843c4088690d49"),
            ("src/openxdox/web_assets.py",
             "01b06c940fa9f62c9b10f369b0843c4088690d49"),
            ("tests/test_gate_loop_probes.py",
             "b009196345088e27abe87db0b99f7d132b2e41c4"),
            ("tests/test_gate_loop_views.py",
             "01b06c940fa9f62c9b10f369b0843c4088690d49")):
        assert path in seed, (
            f"{path} is § 3.4 SLICE S5's own created file at openxdox_code "
            "(`#656` comments 5648044785 / 5648049748 / 5648065587) and is no "
            "longer declared")
        assert seed[path]["since"] == since, seed[path]
    assert "tests/test_gate_loop_contributed.py" in opendox_seed, (
        "tests/test_gate_loop_contributed.py is § 3.4 SLICE S5's own test file "
        "at opendox_code and is no longer declared")
    assert opendox_seed["tests/test_gate_loop_contributed.py"]["since"] == (
        "fd7160d71813874033c21d6f2a8daa5ebf2350e4")
    assert "tests/test_split_route_tails.py" in opendox_seed, (
        "tests/test_split_route_tails.py is § 3.4 SLICE S4's own test file "
        "(`#656` comment 5642758731) and is no longer declared for "
        "opendox_code")
    assert opendox_seed["tests/test_split_route_tails.py"]["since"] == (
        "2e842178b2bceaee9a45441b7d70d797fe1205cf")
    # THE SIXTH BUMP: three more `opendox_code` files, RULED into this file by
    # § 3.4 SLICE S7 (RULED Q1/Q2/Q7, `#656` comment 5648049748; S7 CLAIM
    # `#656` comment 5649148461) — the DISPLAY facet's SERVER half
    # (`display_profile.py`, what `/capabilities` publishes) and CLIENT half
    # (`views/display.js`, the module every class-C file in the bundle resolves
    # its vocabulary through), introduced by ONE commit because neither half
    # means anything without the other, plus the suite that holds the two
    # against each other (`tests/test_display_facet.py`). None of the three
    # carries a manifest row (RULED OQ-C: a CREATED file has none), so the
    # admission is the ONLY governed record that they may be at the
    # destination at all — which is exactly why each is pinned to its own
    # introducing commit (`git log --diff-filter=A`, not the leg branch's
    # tip) rather than left to the generic shape checks below. Admitted on the
    # same Q-L1 footing as every bump above: the leg PR,
    # opensoft/openDox-code#21, pairs with — and lands after — this annotation
    # PR. Checked by PRESENCE for the same reason as the seeds above.
    for path, since in (
            ("src/opendox/display_profile.py",
             "80b1f3bc60499ebbd84e69aaba40ef243c24a54a"),
            ("src/opendox/web/views/display.js",
             "80b1f3bc60499ebbd84e69aaba40ef243c24a54a"),
            ("tests/test_display_facet.py",
             "372a04da2a14c2a4c547b78e9500d65f63899aac")):
        assert path in opendox_seed, (
            f"{path} is one of § 3.4 SLICE S7's three created files (`#656` "
            "comment 5648049748, RULED Q1/Q2/Q7) and is no longer declared "
            "for opendox_code")
        assert opendox_seed[path]["since"] == since, (
            f"{path} declares since={opendox_seed[path]['since']!r}; § 3.4 "
            f"SLICE S7 introduced it at {since} (`git log --diff-filter=A` on "
            "opensoft/openDox-code `build/s7-parameterize-class-c`), and an "
            "admission whose `since` is not the introducing commit is not a "
            "falsifiable claim")
    # THE TWO HALVES ARE ONE ADMISSION, and the pin says so: `display.js` is
    # unreadable without the payload `display_profile.py` publishes, so a
    # future act that re-homes one must move the other or state why not.
    assert (opendox_seed["src/opendox/display_profile.py"]["since"]
            == opendox_seed["src/opendox/web/views/display.js"]["since"]), (
        "§ 3.4 SLICE S7's two DISPLAY-facet halves were introduced by one "
        "commit and no longer declare the same `since`")
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
