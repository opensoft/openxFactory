"""FLOOR PART 2 — every refusal pinned by a test that can only pass if that
check runs, plus the landed document's own figures.

`scripts/carve_test_mapping.py` and `scripts/verify-carve-test-mapping.py`
realize `split-opendox-two-layer-product` § 5.4 (design § D6 (2), RULED OQ-1,
RESTATED BY RULING OQ-K). This module is their evidence.

WHY A THROWAWAY REPOSITORY FOR THE REFUSALS. Every refusal here is a
disagreement between a manifest and a tree, and manufacturing one against
`openxFactory` would mean editing the repository under the test —
`tests/carve_manifest/test_carve_manifest.py`'s reason, unchanged. So the cases
below build a fresh git repository in `tmp_path` and generate a manifest FROM
it: the clean case is clean by construction and every refusal is one deliberate
mutation away from it.

THE FIXTURE IS A MINIATURE OF THE REAL CARVE, not an abstract one: its
`source_repository` is `opensoft/openxFactory`, its two destinations resolve to
`opensoft/openDox-code` and `opensoft/openXdox-code`, and its replica sits at
`tests/corpus-adapter/test_conformance.py`. That is deliberate. Clause (b)'s
declaration is keyed BY SOURCE PATH — until FLOOR PART 1's successor pull
request lands the manifest field, `DECLARED_REPLICA_SETS` is the enumeration
§ 5.4 says IS the declaration — so a fixture with invented paths could not
exercise a declared multiplicity at all, and the `(m − 1) × row_test_count`
term would be pinned only by prose.

THE SCRIPT IS RUN AS A SUBPROCESS for every behavioural case, on
`tests/carve_manifest`'s rule: the documented way to invoke it is
`python3 scripts/verify-carve-test-mapping.py`, and a test of an imported
function proves the code executes rather than that the documented invocation
succeeds and prints what its readers depend on. The MODULE is also imported —
it is not hyphenated, which is the point of it existing — for the constant
assertions, the predicate identities and the pure arithmetic.

THE TESTS THAT READ THE LANDED DOCUMENT DO NOT BRANCH.
`the_landed_manifest()` treats an absent manifest as a FAILURE, not a skip and
not an `assert True`: those tests are about the document's contents and there
is no revision they can run at without it. `tests/carve_manifest`'s docstring
records what the branching idiom cost when it was copied five times; this
module does not start a sixth.

NO TEST HERE SKIPS. `.github/workflows/pytest-suite.yml` pins `EXPECT_SKIPPED`
exactly, so a conditional skip in a new directory reds the required job for a
reason no reader would connect to this file.

Hermetic: no network, `git` only, and its environment PINNED rather than
inherited — `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a
repository-local identity, the same treatment
`tests/carve_manifest/test_carve_manifest.py` gives it and for the same
reasons: a CI runner has no ambient git identity and a developer's global
config can carry `core.hooksPath` or `commit.gpgsign`.
"""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify-carve-test-mapping.py"
MODULE_PATH = REPO_ROOT / "scripts" / "carve_test_mapping.py"
FLOOR_PART_1 = REPO_ROOT / "scripts" / "validate-carve-manifest.py"
RUNBOOK = REPO_ROOT / "docs" / "opendox-cutover-runbook.md"

# THE PACKET, resolved with its ARCHIVE FALLBACK — `openspec/changes/<id>/`
# while the change is live and `openspec/changes/archive/<date>-<id>/` after it
# archives, the shape `tests/avatar_client_validator/test_f0_archive_fallback.py`
# already pins for a pinned packet path. Clause (b)'s declaration lives in that
# file's prose until the manifest carries the field, so a test that could not
# find the packet after archiving would quietly stop checking the declaration
# at exactly the moment nobody is watching this floor any more.
PACKET_ID = "split-opendox-two-layer-product"


def the_packet_tasks() -> Path:
    live = REPO_ROOT / "openspec" / "changes" / PACKET_ID / "tasks.md"
    if live.is_file():
        return live
    archive = REPO_ROOT / "openspec" / "changes" / "archive"
    candidates = sorted(archive.glob(f"*-{PACKET_ID}/tasks.md"))
    assert candidates, (
        f"neither openspec/changes/{PACKET_ID}/tasks.md nor an archived "
        "copy of it exists, and clause (b)'s declaration lives there")
    return candidates[-1]


# The vocabulary, restated as a LITERAL rather than imported: asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology, and
# spelling it out is what makes a silent rename a test failure — other code
# branches BY CODE.
RATIFIED_CODES = (
    "test-home-missing",
    "test-home-deleted-at-carve",
    "replica-multiplicity-undeclared",
    "destination-test-shortfall",
    "test-mapping-unreadable",
)

# The three repositories RULING OQ-K enumerates, verbatim and in the box's own
# order — `openxFactory` (retained) first.
RULED_REPLICA_HOMES = ("opensoft/openxFactory", "opensoft/openDox-code",
                       "opensoft/openXdox-code")


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load(MODULE_PATH, "carve_test_mapping_under_test")
PART_1 = _load(FLOOR_PART_1, "validate_carve_manifest_for_parity")


# --------------------------------------------------------------------------
# the hermetic git environment
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _hermetic_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "carve-test-mapping-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "carve-test@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "carve-test-mapping-test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "carve-test@example.invalid")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr}"
    return done


# --------------------------------------------------------------------------
# the generated fixture — a miniature carve
# --------------------------------------------------------------------------

def _tests(n: int, name: str) -> str:
    body = "\n\n".join(f"def test_{name}_{i}():\n    assert True"
                       for i in range(n))
    return f'"""{name}."""\n\n{body}\n' if n else f'"""{name}, no tests."""\n'


SOURCE_FILES = {
    "scripts/pkg/mod.py": _tests(0, "mod"),
    "scripts/pkg/test_alpha.py": _tests(3, "alpha"),
    "scripts/pkg/test_beta.py": _tests(2, "beta"),
    "scripts/pkg/test_kept.py": _tests(4, "kept"),
    "scripts/pkg/gone.py": _tests(0, "gone"),
    "tests/corpus-adapter/test_conformance.py": _tests(5, "conformance"),
    # THE OTHER TWO DECLARED REPLICAS, carrying NO tests, and both are here
    # because the tool holds the declared key set and the manifest's replica
    # rows equal in BOTH directions (Copilot, second round on #1080): a
    # declared key naming no row at all is stale. Zero tests keeps every
    # arithmetic assertion below unmoved — a zero-test replica is outside
    # clause (b) by its own words and contributes `(m − 1) × 0` — while the
    # fixture stops being a manifest the declaration cannot describe.
    "tests/corpus-adapter/test_interface_closure.py": _tests(0, "closure"),
    "tests/corpus-adapter/test_no_home_vocabulary.py": _tests(0, "vocab"),
}


class Scratch:
    """A throwaway source repository plus the manifest generated from it."""

    def __init__(self, tmp_path: Path) -> None:
        self.root = tmp_path
        self.repo = tmp_path / "src"
        self.repo.mkdir()
        _git(self.repo, "init", "-q", "-b", "main")
        for relpath, text in SOURCE_FILES.items():
            target = self.repo / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-qm", "the carve commit")
        self.commit = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.manifest_path = tmp_path / "manifest.yaml"

    def clean(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "kind": "opendox-carve-manifest",
            "carve_commit": self.commit,
            "carve_tag": "miniature-carve-0",
            "source_repository": "opensoft/openxFactory",
            "destinations": {
                "dox_code": {"repository": "opensoft/openDox-code",
                             "leg": "code"},
                "xdox_code": {"repository": "opensoft/openXdox-code",
                              "leg": "code"},
            },
            "moved_paths": ["scripts/pkg/", "tests/corpus-adapter/"],
            "rows": [
                {"source_path": "scripts/pkg/mod.py",
                 "disposition": "moved_verbatim",
                 "destination": "dox_code",
                 "destination_path": "src/mod.py"},
                {"source_path": "scripts/pkg/test_alpha.py",
                 "disposition": "moved_verbatim",
                 "destination": "dox_code",
                 "destination_path": "tests/test_alpha.py"},
                {"source_path": "scripts/pkg/test_beta.py",
                 "disposition": "moved_verbatim",
                 "destination": "xdox_code",
                 "destination_path": "tests/test_beta.py"},
                {"source_path": "scripts/pkg/test_kept.py",
                 "disposition": "not_moved",
                 "reason": "stays_openxfactory_adapter"},
                {"source_path": "scripts/pkg/gone.py",
                 "disposition": "not_moved",
                 "reason": "deleted_at_carve"},
                {"source_path": "tests/corpus-adapter/test_conformance.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination"},
                {"source_path":
                    "tests/corpus-adapter/test_interface_closure.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination"},
                {"source_path":
                    "tests/corpus-adapter/test_no_home_vocabulary.py",
                 "disposition": "not_moved",
                 "reason": "replicated_at_destination"},
            ],
        }

    def write(self, doc: dict[str, Any]) -> Path:
        self.manifest_path.write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                           width=10 ** 6), encoding="utf-8")
        return self.manifest_path

    def row(self, doc: dict[str, Any], source_path: str) -> dict[str, Any]:
        for row in doc["rows"]:
            if row["source_path"] == source_path:
                return row
        raise AssertionError(f"no row for {source_path}")

    def destination(self, name: str, arrivals: dict[str, str]) -> Path:
        """A destination checkout carrying the arrivals it is given."""
        root = self.root / name
        for relpath, source_path in arrivals.items():
            target = root / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(SOURCE_FILES[source_path], encoding="utf-8")
        root.mkdir(parents=True, exist_ok=True)
        return root

    def run(self, doc: dict[str, Any] | None = None,
            *args: str) -> subprocess.CompletedProcess:
        manifest = self.write(self.clean() if doc is None else doc)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--manifest", str(manifest),
             "--repo", str(self.repo), "--json", *args],
            capture_output=True, text=True, check=False)


@pytest.fixture()
def scratch(tmp_path: Path) -> Scratch:
    return Scratch(tmp_path)


def verified(done: subprocess.CompletedProcess) -> dict[str, Any]:
    assert done.returncode == 0, f"expected exit 0: {done.stdout}{done.stderr}"
    return json.loads(done.stdout)


def refused(done: subprocess.CompletedProcess, code: str) -> dict[str, Any]:
    assert done.returncode == 2, \
        f"expected refusal {code}: rc={done.returncode} {done.stdout}{done.stderr}"
    payload = json.loads(done.stdout)
    assert payload["result"] == "refused"
    assert payload["code"] == code, payload
    return payload


# --------------------------------------------------------------------------
# the counting rule (DEFINITION)
# --------------------------------------------------------------------------

def test_the_counting_rule_is_declared_once_and_counts_raw_bytes() -> None:
    """`DEFINITION` is the floor's sentence and `count()` is its only
    implementation. Byte-level, because a carve blob is whatever git holds —
    `carve_lines.py` records the day two tools disagreed about what a LINE was,
    and a count of test functions is the same class of claim."""
    assert "def test_" in MODULE.DEFINITION
    assert "carve_commit" in MODULE.DEFINITION
    assert MODULE.count(b"") == 0
    assert MODULE.count(b"def test_one():\n    pass\n") == 1
    assert MODULE.count(b"    def test_nested(self):\n") == 1
    assert MODULE.count(b"# def test_in_a_comment()\n") == 1
    assert MODULE.count(b"def testing():\n") == 0
    assert MODULE.count(b"async def test_async():\n") == 1
    # NOT VALID UTF-8, and still answerable: the count is over bytes, so a file
    # no decoder can hold does not raise out of a floor question.
    assert MODULE.count(b"\xff\xfe def test_x():\n def test_y():\n") == 2


def test_the_vocabulary_is_closed_and_every_raise_site_is_in_it() -> None:
    """The list spelled out, and then held COMPLETE by scanning both files'
    own raise sites — the guard `tests/carve_manifest` learned to add after
    `carve-unreadable` was raised while the vocabulary said it did not exist."""
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES
    raised: set[str] = set()
    for path in (MODULE_PATH, SCRIPT):
        source = path.read_text(encoding="utf-8")
        raised |= set(re.findall(r'TestMappingRefusal\(\s*"([a-z-]+)"',
                                 source))
    assert raised, "no raise site found — the scan itself is broken"
    assert raised <= set(RATIFIED_CODES), sorted(raised - set(RATIFIED_CODES))


# --------------------------------------------------------------------------
# the predicates are IMPORTED, not copied
# --------------------------------------------------------------------------

def test_the_two_ruled_predicates_are_carved_reachs_own_objects() -> None:
    """IDENTITY, not equality. `validate-carve-manifest.py`,
    `verify-carve-arrival.py` and `carved_reach.py` hold three copies of
    `effective_arrival`/`retired_at` kept in step by a table test, because the
    first two are hyphenated and unimportable. `carve_test_mapping.py` is not
    hyphenated, so it takes the sharing `carve_lines.py`'s doctrine asks for —
    and a future copy-paste into that file fails HERE rather than passing
    review."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import carved_reach  # noqa: PLC0415

    assert MODULE.effective_arrival is carved_reach.effective_arrival
    assert MODULE.retired_at is carved_reach.retired_at


def test_the_surface_reading_matches_floor_part_1_over_the_landed_rows() -> None:
    """`under_surface` is the ONE predicate this floor copies, because FLOOR
    PART 1's `in_surface` lives in a hyphenated entry point. Compared over
    every row of the landed manifest and over the adversarial prefix the
    docstring of both names."""
    _text, doc = the_landed_manifest()
    moved_paths = doc["moved_paths"]
    for row in doc["rows"]:
        path = row["source_path"]
        assert MODULE.under_surface(path, moved_paths) is \
            PART_1.in_surface(path, moved_paths), path
    for probe in ("scripts/ideation_dashboard_old/x.py",
                  "scripts/ideation_dashboard/x.py",
                  "scripts/ideation_dashboard",
                  "docs/opendox-carve-manifest.yaml"):
        assert MODULE.under_surface(probe, moved_paths) is \
            PART_1.in_surface(probe, moved_paths), probe


# --------------------------------------------------------------------------
# the clean case
# --------------------------------------------------------------------------

def test_the_generated_miniature_verifies_and_prints_every_term(
        scratch: Scratch) -> None:
    """The baseline every refusal below is one mutation from.

    source = 3 + 2 + 4 + 5 = 14 (mod.py and gone.py carry none); the replica's
    5 have THREE homes, so the excess is (3 − 1) × 5 = 10; nothing is retired;
    Σ(destinations) = 24 = 14 + 10 − 0."""
    summary = verified(scratch.run())
    assert summary["source_count"] == 14
    assert summary["replica_excess"] == 10
    assert summary["also_replicated_excess"] == 0
    assert summary["retired_tests"] == 0
    assert summary["retired_excess"] == 0
    assert summary["destinations_sum"] == 24
    assert summary["identity_holds"] is True
    assert summary["per_repository"] == {
        "opensoft/openDox-code": 3 + 5,
        "opensoft/openXdox-code": 2 + 5,
        "opensoft/openxFactory": 4 + 5,
    }
    assert summary["test_bearing_rows"] == 4
    assert summary["homed_rows"] == 4
    assert summary["retired"] == []


def test_a_zero_test_replica_needs_no_declaration(scratch: Scratch) -> None:
    """Clause (b) binds TEST-BEARING replicated rows ONLY, in terms: a zero-test
    replica contributes `(m − 1) × 0 = 0` whatever its set, so it can neither
    move the sum nor make it uncomputable, and its replica set is FLOOR PART
    1's business. Fifteen of the landed manifest's replicas were in this class
    when OQ-K was measured and seventeen are today."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/mod.py")["disposition"] = "not_moved"
    scratch.row(doc, "scripts/pkg/mod.py").pop("destination")
    scratch.row(doc, "scripts/pkg/mod.py").pop("destination_path")
    scratch.row(doc, "scripts/pkg/mod.py")["reason"] = \
        "replicated_at_destination"
    summary = verified(scratch.run(doc))
    assert summary["source_count"] == 14
    assert summary["replica_excess"] == 10


# --------------------------------------------------------------------------
# clause (a) — a test with no home
# --------------------------------------------------------------------------

def test_a_moved_row_with_no_destination_is_a_lost_test(
        scratch: Scratch) -> None:
    """Clause (a)'s FIRST LIMB, verbatim: "its row names no home — no
    `destination`". FLOOR PART 1 refuses the same row `carve-shape-invalid`,
    and this floor still answers it by its own name, because the two tools run
    in different places and "validate the manifest first" is not an answer to
    "where did three tests go"."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row.pop("destination")
    row.pop("destination_path")
    payload = refused(scratch.run(doc), "test-home-missing")
    assert "scripts/pkg/test_alpha.py" in payload["detail"]
    assert "3 `def test_`" in payload["detail"]


def test_a_row_with_no_tests_and_no_destination_does_not_refuse(
        scratch: Scratch) -> None:
    """The clause is about TESTS. A homeless row carrying none is FLOOR PART
    1's shape question and not this floor's — and a floor that refused it would
    be answering a question it was not given, which is how a check earns the
    reputation that gets it ignored."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/mod.py")
    row.pop("destination")
    row.pop("destination_path")
    verified(scratch.run(doc))


def test_a_deleted_at_carve_row_carrying_tests_refuses_under_its_own_name(
        scratch: Scratch) -> None:
    """The box: "A `deleted_at_carve` row carrying `def test_` is the same
    refusal under its own name: deleting tests is a decision to be RULED, never
    inferred from a disposition." Its own name is
    `test-home-deleted-at-carve`, so a reader of a CI log can tell a row that
    forgot its destination from a row whose disposition deletes it."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row.pop("destination")
    row.pop("destination_path")
    row["disposition"] = "not_moved"
    row["reason"] = "deleted_at_carve"
    payload = refused(scratch.run(doc), "test-home-deleted-at-carve")
    assert "RULED" in payload["detail"]


def test_the_landed_deleted_at_carve_row_carries_no_test(
        scratch: Scratch) -> None:
    """Measured at `carve_commit` and asserted rather than recited: the
    manifest's ONE `deleted_at_carve` row is
    `scripts/ideation_dashboard/profile_openxfactory.py` and it carries zero
    `def test_`, which is why the limb above does not fire on the real
    document."""
    _text, doc = the_landed_manifest()
    deleted = [row["source_path"] for row in doc["rows"]
               if row.get("reason") == "deleted_at_carve"]
    assert deleted == ["scripts/ideation_dashboard/profile_openxfactory.py"]
    counts = MODULE.tests_at_carve(REPO_ROOT, doc)
    assert counts[deleted[0]] == 0


# --------------------------------------------------------------------------
# clause (b) — declared multiplicity
# --------------------------------------------------------------------------

def test_a_test_bearing_replica_with_no_declared_set_refuses(
        scratch: Scratch) -> None:
    """An undeclared replica set makes `Σ over replicated rows of (m − 1) ×
    row_test_count` UNCOMPUTABLE, and an uncomputable check is never a pass.
    The mutation is a RENAME of the declared path, which is the shape the
    refusal actually has to catch: a NEW test-bearing replica, or an existing
    one that starts carrying tests."""
    doc = scratch.clean()
    row = scratch.row(doc, "tests/corpus-adapter/test_conformance.py")
    row["source_path"] = "tests/corpus-adapter/test_undeclared.py"
    (scratch.repo / "tests/corpus-adapter/test_undeclared.py").write_text(
        SOURCE_FILES["tests/corpus-adapter/test_conformance.py"],
        encoding="utf-8")
    _git(scratch.repo, "add", "-A")
    _git(scratch.repo, "commit", "-qm", "a second replica")
    doc["carve_commit"] = _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()
    payload = refused(scratch.run(doc), "replica-multiplicity-undeclared")
    assert "UNCOMPUTABLE" in payload["detail"]
    assert "5609526215" in payload["detail"], \
        "the refusal must cite the ruling that owes the declaration"


def test_the_declaration_names_repositories_and_not_destination_keys() -> None:
    """The manifest is explicit that the two vocabularies are different
    things: "`also_replicated_to:` names `destinations:` KEYS for arrival
    admission; the owed field names REPOSITORIES for an arithmetic. One row
    could carry both without either meaning the other." """
    for source_path, homes in MODULE.DECLARED_REPLICA_SETS.items():
        assert homes == RULED_REPLICA_HOMES, source_path
        assert len(homes) == 3, "RULING OQ-K's `m = 3`"
        for home in homes:
            assert "/" in home, f"{home} is not a repository"


def test_the_declaration_tables_keys_are_the_manifests_own_replicas() -> None:
    """THE KEY PIN. The table is a transcription of § 5.4's enumeration, so the
    one way it can rot is by disagreeing with the manifest it describes. Its
    keys must be EXACTLY the test-bearing `replicated_at_destination` rows —
    a new one is a REFUSAL until declared (above), and a stale key is a
    declaration about nothing."""
    _text, doc = the_landed_manifest()
    counts = MODULE.tests_at_carve(REPO_ROOT, doc)
    measured = {row["source_path"] for row in doc["rows"]
                if MODULE.is_replica(row) and counts[row["source_path"]]}
    assert measured == set(MODULE.DECLARED_REPLICA_SETS), (
        "the declared replica sets and the manifest's test-bearing replicas "
        "have diverged")
    assert measured == {"tests/corpus-adapter/test_conformance.py",
                        "tests/corpus-adapter/test_interface_closure.py",
                        "tests/corpus-adapter/test_no_home_vocabulary.py"}
    assert sum(counts[path] for path in measured) == 30, \
        "RULING OQ-K's 30 `def test_` across the three replicated modules"


def test_the_declaration_tables_values_are_the_packets_own_words() -> None:
    """THE VALUE PIN. § 5.4 says "until it lands the enumeration below IS the
    declaration", so the table's three repositories and its `m = 3` must be
    findable in the box itself. Whitespace-normalized, because a re-wrap of
    that paragraph is not a change to the declaration."""
    text = " ".join(the_packet_tasks().read_text(encoding="utf-8").split())
    # ANCHORED ON `FLOOR PART 2` ALONE and not on the box's full title. The
    # packet is amended often and by another actor, and a re-title is not a
    # change to the declaration — but if the phrase itself goes, the
    # declaration really has moved and a failing test is the right answer.
    start = text.find("FLOOR PART 2")
    assert start >= 0, "the packet no longer names FLOOR PART 2"
    box = text[start:start + 14000]
    assert "`m = 3`" in box
    assert "`openxFactory` (retained)" in box
    assert "`opensoft/openDox-code`" in box
    assert "`opensoft/openXdox-code`" in box
    assert "IS the declaration" in box
    assert "5609526215" in MODULE.MULTIPLICITY_DECLARATION


# --------------------------------------------------------------------------
# the retirement — a RULED deletion is admitted and NAMED
# --------------------------------------------------------------------------

RETIREMENT = {
    "at": "dox_code",
    "at_path": "tests/test_alpha.py",
    "ruling": "opensoft/openxFactory#656 comment 5656343213",
    "surface": "scripts/pkg/test_kept.py",
    "note": "the surface stayed at openxFactory and reached neither leg",
}


def test_a_retired_row_is_admitted_named_and_subtracted(
        scratch: Scratch) -> None:
    """RULED 5656343213's form, and the whole reason clause (c) has a fourth
    term. The row keeps its `destination:` unedited, so the box's literal
    condition ("no `destination`") is satisfied and nothing refuses — but the
    arrival is DELETED, so those tests are at no home and the destination's
    total must fall by exactly them. Admitted because the form REQUIRES a
    `ruling:`, which is the RULED decision clause (a) demands; NAMED because a
    deletion nobody prints is a deletion nobody re-reads."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_alpha.py")["retired"] = \
        copy.deepcopy(RETIREMENT)
    summary = verified(scratch.run(doc))
    assert summary["retired"] == [
        {"source_path": "scripts/pkg/test_alpha.py", "tests": 3,
         "ruling": RETIREMENT["ruling"],
         # EMPTY HERE AND NOT ABSENT: a plain retirement deletes the
         # row's only home, and a row that keeps `also_replicated_to:`
         # copies is the case
         # `test_a_retired_row_with_surviving_copies_is_counted_once`
         # holds. The report names them because they are the difference
         # between this row's negative term and that one's zero.
         "homes": []}]
    assert summary["retired_tests"] == 3
    assert summary["retired_excess"] == -3, \
        "a plain retired row has no home, so its `(0 − 1) × tests` IS the "\
        "subtraction — the fourth term is arithmetic, not a special case"
    assert summary["source_count"] == 14, "the source still carried them"
    assert summary["per_repository"]["opensoft/openDox-code"] == 5, \
        "the three retired tests leave the destination's declared total"
    assert summary["destinations_sum"] == 14 + 10 - 3
    assert summary["identity_holds"] is True
    assert summary["homed_rows"] == 3


def test_half_a_retirement_reads_as_no_retirement_and_the_row_owes_again(
        scratch: Scratch) -> None:
    """The reading guard, inherited whole from `carved_reach.retired_at`: a
    block missing any of its four required keys is NO retirement. It FAILS
    CLOSED — the row goes on owing its arrival — because reading half a block
    as a retirement would let `retired: {}` silence a required arrival at every
    leg. Here the missing key is `ruling:`, which is the one that makes the
    deletion RULED at all."""
    doc = scratch.clean()
    retirement = copy.deepcopy(RETIREMENT)
    retirement.pop("ruling")
    scratch.row(doc, "scripts/pkg/test_alpha.py")["retired"] = retirement
    summary = verified(scratch.run(doc))
    assert summary["retired"] == []
    assert summary["retired_tests"] == 0
    assert summary["per_repository"]["opensoft/openDox-code"] == 3 + 5


def test_a_retired_row_is_not_a_lost_test(scratch: Scratch) -> None:
    """Stated as its own case because the opposite reading was available and
    was rejected on measurement: treating a retired row as `test-home-missing`
    would refuse the real tree today, on a deletion Brett RULED and the row
    cites."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_alpha.py")["retired"] = \
        copy.deepcopy(RETIREMENT)
    done = scratch.run(doc)
    assert done.returncode == 0, done.stdout + done.stderr


# --------------------------------------------------------------------------
# the destination side — a silent drop
# --------------------------------------------------------------------------

ARRIVALS = {"tests/test_alpha.py": "scripts/pkg/test_alpha.py",
            "src/mod.py": "scripts/pkg/mod.py"}


def test_a_destination_carrying_its_arrivals_verifies(
        scratch: Scratch) -> None:
    dest = scratch.destination("dox", ARRIVALS)
    summary = verified(scratch.run(None, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["declared"] == 3
    assert summary["collected"] == 3
    assert summary["below_declaration"] == []
    assert summary["absent"] == []
    assert summary["repository"] == "opensoft/openDox-code"


def test_one_dropped_test_function_at_a_destination_refuses(
        scratch: Scratch) -> None:
    """The case Brett named when he rejected snapshot-equivalence alone: *"a
    dropped module without test coverage go unnoticed"*. ONE function, not a
    module — the floor is a count, so the smallest real loss is the one that
    has to red."""
    dest = scratch.destination("dox", ARRIVALS)
    arrived = dest / "tests/test_alpha.py"
    arrived.write_text(arrived.read_text().replace("def test_alpha_0",
                                                   "def helper_alpha_0"),
                       encoding="utf-8")
    payload = refused(scratch.run(None, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "destination-test-shortfall")
    assert "1 short" in payload["detail"]
    assert "tests/test_alpha.py" in payload["detail"]


def test_an_absent_arrival_is_named_as_absent_not_as_zero(
        scratch: Scratch) -> None:
    """A file that never arrived and a file that arrived with no tests are the
    same number and different facts, so the refusal distinguishes them."""
    dest = scratch.destination("dox", {"src/mod.py": "scripts/pkg/mod.py"})
    payload = refused(scratch.run(None, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "destination-test-shortfall")
    assert "ABSENT" in payload["detail"]
    assert "tests/test_alpha.py" in payload["detail"]


def test_a_destinations_own_new_tests_do_not_raise_the_declaration(
        scratch: Scratch) -> None:
    """"A file CREATED at a destination gets no row at all: this manifest
    declares what LEAVES, not what the destination assembles" — so the leg's
    own suites are counted in the TREE figure and never in the floor. Measured
    on the real legs 2026-09-16, the two differ by 257 and 236 `def test_`; a
    floor resting on the larger number would drift with another repository's
    unrelated commits."""
    dest = scratch.destination("dox", ARRIVALS)
    (dest / "tests/test_the_legs_own.py").write_text(_tests(9, "own"),
                                                     encoding="utf-8")
    summary = verified(scratch.run(None, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["declared"] == 3
    assert summary["collected"] == 3
    assert summary["tree_tests"] == 12


def test_a_retired_arrival_is_not_owed_at_its_destination(
        scratch: Scratch) -> None:
    """The destination side reads the same retirement the source side does:
    once a RULING has deleted the arrival, the leg is not short for not having
    it. openDox-code would otherwise be 31 `def test_` short of the landed
    manifest from PR #1043's landing onward, forever."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_alpha.py")["retired"] = \
        copy.deepcopy(RETIREMENT)
    dest = scratch.destination("dox", {"src/mod.py": "scripts/pkg/mod.py"})
    summary = verified(scratch.run(doc, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["declared"] == 0
    assert summary["absent"] == []


def test_a_replica_joins_a_destinations_floor_only_when_it_is_declared(
        scratch: Scratch) -> None:
    """RULED OQ-C gives a replica no `destination_path`, so there is nothing to
    derive its arrival from and `verify-carve-arrival.py` makes the operator
    declare it. This floor follows, and has a second measured reason to: at
    2026-09-16 the three test-bearing replicas are at NEITHER leg (§ 3.7 is
    unticked), so a floor that counted them unasked would refuse both legs for
    work that has not been scheduled."""
    dest = scratch.destination("dox", ARRIVALS)
    silent = verified(scratch.run(None, "--destination", "dox_code",
                                  "--dest-root", str(dest)))
    assert silent["declared"] == 3
    assert silent["replicas_declared"] == 0
    payload = refused(
        scratch.run(None, "--destination", "dox_code", "--dest-root",
                    str(dest), "--replica-at",
                    "tests/corpus-adapter/test_conformance.py="
                    "tests/test_conformance.py"),
        "destination-test-shortfall")
    assert "5 short" in payload["detail"]
    (dest / "tests/test_conformance.py").write_text(
        SOURCE_FILES["tests/corpus-adapter/test_conformance.py"],
        encoding="utf-8")
    summary = verified(
        scratch.run(None, "--destination", "dox_code", "--dest-root",
                    str(dest), "--replica-at",
                    "tests/corpus-adapter/test_conformance.py="
                    "tests/test_conformance.py"))
    assert summary["declared"] == 8
    assert summary["collected"] == 8
    assert summary["replicas_declared"] == 1


def test_the_retained_column_needs_no_flag_for_its_replicas(
        scratch: Scratch) -> None:
    """Not an inconsistency with the case above: a `not_moved` row STAYS at
    `openxFactory` at its own `source_path`, and FLOOR PART 1 requires it
    present there in both phases. The flag exists for placements the manifest
    cannot name, and this one it names."""
    summary = verified(scratch.run(None, "--destination", "openxFactory",
                                   "--dest-root", str(scratch.repo)))
    assert summary["declared"] == 4 + 5
    assert summary["collected"] == 4 + 5
    assert summary["repository"] == "opensoft/openxFactory"


def test_replica_at_may_not_re_point_a_moved_row(scratch: Scratch) -> None:
    """`verify-carve-arrival.py`'s rule, kept: "a flag that could name any
    moved row would let a caller re-point an arrival the manifest declared,
    which is the one thing the manifest is for"."""
    dest = scratch.destination("dox", ARRIVALS)
    payload = refused(
        scratch.run(None, "--destination", "dox_code", "--dest-root",
                    str(dest), "--replica-at",
                    "scripts/pkg/test_beta.py=tests/test_beta.py"),
        "test-mapping-unreadable")
    assert "scripts/pkg/test_beta.py" in payload["detail"]


def test_an_unusable_invocation_refuses_rather_than_reporting_nothing(
        scratch: Scratch) -> None:
    """Every tool in this family carries one I/O refusal, because a question
    this floor cannot ask must never read as a pass."""
    dest = scratch.destination("dox", ARRIVALS)
    refused(scratch.run(None, "--destination", "not_a_key", "--dest-root",
                        str(dest)), "test-mapping-unreadable")
    refused(scratch.run(None, "--destination", "dox_code"),
            "test-mapping-unreadable")
    refused(scratch.run(None, "--dest-root", str(dest)),
            "test-mapping-unreadable")
    missing = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest",
         str(scratch.root / "absent.yaml"), "--repo", str(scratch.repo),
         "--json"], capture_output=True, text=True, check=False)
    refused(missing, "test-mapping-unreadable")


def test_a_source_path_carrying_a_line_terminator_refuses() -> None:
    """The one failure mode a floor must not have is a SILENT MIS-COUNT.

    `git cat-file --batch` is asked one path per line and answers in order, so
    a `source_path` holding a newline would desync the reply parse and start
    attributing blobs to the wrong rows — every count wrong, nothing refused.
    Git permits such a path and `tests/carve_manifest` already carries paths
    UTF-8 cannot hold, so the guard is a refusal rather than an assumption.

    Asserted IN PROCESS, the one case that is: the guard runs BEFORE git is
    invoked, and building the manifest through the CLI would mean writing a
    YAML document whose own reader is the thing under test rather than the
    guard.
    """
    doc = {"carve_commit": "0" * 40,
           "rows": [{"source_path": "scripts/pkg/te\nst.py"}]}
    with pytest.raises(MODULE.TestMappingRefusal) as raised:
        MODULE.tests_at_carve(REPO_ROOT, doc)
    assert raised.value.code == "test-mapping-unreadable"
    assert "line terminator" in raised.value.detail


def test_a_declared_home_outside_the_manifests_repositories_refuses(
        scratch: Scratch) -> None:
    """The two vocabularies are different — `DECLARED_REPLICA_SETS` spells
    REPOSITORIES and the manifest spells `destinations:` keys — and this is the
    one drift nothing else would catch: a repository renamed in one and not the
    other opens a SECOND per-repository column carrying the replica's tests.
    The identity still holds, every total is wrong, and the run prints an extra
    line nobody reads as an alarm."""
    doc = scratch.clean()
    doc["source_repository"] = "opensoft/openxFactory-renamed"
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "opensoft/openxFactory" in payload["detail"]
    assert "REPOSITORIES" in payload["detail"]


def test_the_tree_figure_skips_a_nested_checkout(scratch: Scratch) -> None:
    """The context figure counts the destination's OWN files and no others.

    Measured at openxFactory: the carve suites require `openDox/` and
    `openXdox/` materialized, so a naive walk counts two other repositories'
    suites into a number captioned "the tree carries". A directory holding a
    `.git` entry is another repository's root — a FILE for a submodule, which
    is why "`.git` in the path parts" was not enough."""
    dest = scratch.destination("dox", ARRIVALS)
    nested = dest / "vendored"
    nested.mkdir(parents=True, exist_ok=True)
    (nested / ".git").write_text("gitdir: ../.git/modules/vendored\n",
                                 encoding="utf-8")
    (nested / "test_someone_elses.py").write_text(_tests(11, "theirs"),
                                                  encoding="utf-8")
    summary = verified(scratch.run(None, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["collected"] == 3
    assert summary["tree_tests"] == 3, \
        "the nested checkout's eleven tests are not this destination's"


# --------------------------------------------------------------------------
# the Copilot round on #1080 — nine suppressed findings and six threads, each
# of them a hole in the reading rather than a matter of taste, and each closed
# with the case below.
# --------------------------------------------------------------------------

def test_a_retirement_that_names_another_placement_is_no_retirement(
        scratch: Scratch) -> None:
    """`retired_at` validates the block's SHAPE; it cannot ask whether the
    block retires THIS ROW'S arrival. Taking a shape-valid block that names
    somewhere else as a retirement would DELETE a live arrival from the
    mapping — the sum balances while a real leg quietly stops being asked for
    a real file. FLOOR PART 1 refuses that document
    (`carve-disposition-inconsistent`), but this floor runs at a leg and
    inside a consumer, where that validator never runs."""
    doc = scratch.clean()
    retirement = copy.deepcopy(RETIREMENT)
    retirement["at_path"] = "tests/somewhere_else.py"
    scratch.row(doc, "scripts/pkg/test_alpha.py")["retired"] = retirement
    summary = verified(scratch.run(doc))
    assert summary["retired"] == []
    assert summary["per_repository"]["opensoft/openDox-code"] == 3 + 5, \
        "the row goes on owing the arrival the manifest places"
    dest = scratch.destination("dox", {"src/mod.py": "scripts/pkg/mod.py"})
    payload = refused(scratch.run(doc, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "destination-test-shortfall")
    assert "tests/test_alpha.py" in payload["detail"]


def test_a_moved_row_with_no_destination_cannot_be_homed_by_a_replica(
        scratch: Scratch) -> None:
    """A malformed moved row could pass clause (a) merely by LISTING an
    `also_replicated_to:` destination. The row's own placement is the home the
    clause is about, and RULED Q-L7 (a)'s own sentence about that field is
    that it is "neither a fourth disposition and NEITHER OF THEM A
    PLACEMENT"."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row.pop("destination")
    row.pop("destination_path")
    row["also_replicated_to"] = ["xdox_code"]
    refused(scratch.run(doc), "test-home-missing")


def test_a_retired_row_that_also_replicates_keeps_its_replicas(
        scratch: Scratch) -> None:
    """The hole the fourth term opened when it was written as a whole-row
    subtraction: retirement deletes the row's own ARRIVAL, not the copies its
    `also_replicated_to:` places elsewhere. Subtracting the row's tests while
    still counting them at the surviving home made the printed identity false
    — and nothing refused, because the identity was computed and never
    enforced. One rule now computes every term: `(|homes| − 1) × tests`."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row["also_replicated_to"] = ["xdox_code"]
    row["retired"] = copy.deepcopy(RETIREMENT)
    summary = verified(scratch.run(doc))
    assert summary["identity_holds"] is True
    assert summary["retired_tests"] == 3
    assert summary["retired_excess"] == 0, \
        "one surviving home: (1 − 1) × 3 — nothing to subtract"
    assert summary["per_repository"]["opensoft/openXdox-code"] == 2 + 5 + 3
    assert summary["per_repository"]["opensoft/openDox-code"] == 5


def test_a_declaration_for_a_row_this_manifest_dispositions_otherwise_refuses(
        scratch: Scratch) -> None:
    """THE MACHINE HALF OF THE KEY PIN. The table's keys being exactly the
    manifest's test-bearing replicas is a pytest assertion, and a pytest
    assertion is not a check the runbook's invocation makes — so a row that
    stopped being a replica left the verifier green while its declaration went
    on describing nothing."""
    doc = scratch.clean()
    row = scratch.row(doc, "tests/corpus-adapter/test_conformance.py")
    row["disposition"] = "moved_verbatim"
    row.pop("reason")
    row["destination"] = "dox_code"
    row["destination_path"] = "tests/test_conformance.py"
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "declaration about nothing" in payload["detail"]


def test_two_destination_keys_for_one_leg_are_one_destination(
        scratch: Scratch) -> None:
    """A `destinations:` KEY IS A LABEL, NEVER A REFERENT, and FLOOR PART 1's
    `check_shape` deliberately ADMITS two keys sharing one `{repository, leg}`
    body — which is why `verify-carve-arrival.py` grew `_resolved_destination`
    in the first place. A string comparison here would skip every row written
    under the other alias and report a leg with no owed arrivals: a floor that
    passes by asking nothing."""
    doc = scratch.clean()
    doc["destinations"]["dox_code_alias"] = {
        "repository": "opensoft/openDox-code", "leg": "code"}
    scratch.row(doc, "scripts/pkg/test_alpha.py")["destination"] = \
        "dox_code_alias"
    dest = scratch.destination("dox", ARRIVALS)
    summary = verified(scratch.run(doc, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["declared"] == 3, \
        "the row under the alias is this destination's"
    assert summary["collected"] == 3


def test_one_file_may_not_answer_for_two_rows(scratch: Scratch) -> None:
    """Two declarations naming one destination path had that file's tests
    counted once per declaration — one physical suite satisfying two
    obligations, which is a MISSING ARRIVAL wearing a total that balances."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_beta.py")["destination"] = "dox_code"
    scratch.row(doc, "scripts/pkg/test_beta.py")["destination_path"] = \
        "tests/test_alpha.py"
    dest = scratch.destination("dox", ARRIVALS)
    payload = refused(scratch.run(doc, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "test-mapping-unreadable")
    assert "cannot answer for two rows" in payload["detail"]


def test_a_replica_may_not_be_placed_outside_its_declared_set(
        scratch: Scratch) -> None:
    """A declared set is a CLOSED list of homes, so a placement at a
    repository outside it is not a late arrival — it is a copy the
    multiplicity never counted, and admitting it would raise a destination's
    floor by tests no term of clause (c) carries."""
    doc = scratch.clean()
    doc["destinations"]["dox_spec"] = {"repository": "opensoft/openDox-spec",
                                       "leg": "spec"}
    dest = scratch.destination("spec", {})
    payload = refused(
        scratch.run(doc, "--destination", "dox_spec", "--dest-root",
                    str(dest), "--replica-at",
                    "tests/corpus-adapter/test_conformance.py="
                    "tests/test_conformance.py"),
        "test-mapping-unreadable")
    assert "declared replica set" in payload["detail"]


def test_replica_at_is_refused_at_the_retained_column_not_discarded(
        scratch: Scratch) -> None:
    """Silently ignoring the flag reported a passing retained summary for a
    question the operator thought they had asked."""
    payload = refused(
        scratch.run(None, "--destination", "openxFactory", "--dest-root",
                    str(scratch.repo), "--replica-at",
                    "tests/corpus-adapter/test_conformance.py=x.py"),
        "test-mapping-unreadable")
    assert "means nothing at the retained column" in payload["detail"]


@pytest.mark.parametrize("relpath", ["/etc/passwd", "../outside.py",
                                     "tests/./x.py"])
def test_a_destination_path_that_escapes_the_root_refuses(
        scratch: Scratch, relpath: str) -> None:
    """`Path("/dest") / "/etc/passwd"` is `/etc/passwd`: an absolute value
    REPLACES the root it is joined to and `..` walks out of it. On this floor
    that is not a wrong error message — it is a WRONG NUMBER in a passing
    report."""
    dest = scratch.destination("dox", ARRIVALS)
    refused(scratch.run(None, "--destination", "dox_code", "--dest-root",
                        str(dest), "--replica-at",
                        f"tests/corpus-adapter/test_conformance.py={relpath}"),
            "test-mapping-unreadable")


def test_a_manifest_that_is_not_utf8_refuses_instead_of_raising(
        scratch: Scratch) -> None:
    """`Path.read_text` raises `UnicodeDecodeError`, which is NOT an
    `OSError`, so it escaped the CLI's only catch as a traceback and exit 1 —
    the documented contract being a named refusal and exit 2, for exactly the
    input most likely to be a corrupted file."""
    scratch.manifest_path.write_bytes(b"carve_commit: \xff\xfe\n")
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(scratch.manifest_path),
         "--repo", str(scratch.repo), "--json"],
        capture_output=True, text=True, check=False)
    refused(done, "test-mapping-unreadable")


def test_a_yaml_valid_but_malformed_shape_refuses_instead_of_raising(
        scratch: Scratch) -> None:
    """`read_manifest` accepts many YAML-valid shapes FLOOR PART 1 refuses —
    a row that is not a mapping, a `destinations:` value that is not one — and
    those raised out as a traceback and exit 1, which is a shape no caller can
    branch on.

    A ROW IS NOW NAMED BY ITS INDEX (Copilot, round 6 on #1080) and the
    rest still fall to the generic refusal: every question this floor asks
    is keyed by `source_path:`, so a row without one is worth pointing at,
    while a malformed `destinations:` entry is answered where it is
    resolved. What the two have in common is the contract — a named
    refusal and exit 2, never a traceback."""
    doc = scratch.clean()
    doc["rows"].append("not a mapping at all")
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "source_path" in payload["detail"]
    assert f"rows[{len(doc['rows']) - 1}]" in payload["detail"]
    doc = scratch.clean()
    doc["destinations"]["dox_code"] = "not a mapping either"
    refused(scratch.run(doc), "test-mapping-unreadable")


def test_the_carve_blobs_are_read_in_the_named_repository_not_an_ambient_one(
        scratch: Scratch) -> None:
    """An ambient `GIT_DIR`, alternate object directory, indexed
    `GIT_CONFIG_KEY/VALUE_N` or replace-ref would let `cat-file` read a
    DIFFERENT object store than `--repo` names, and the counts would then be a
    claim about a tree nobody asked about. The scrub list is
    `carved_reach._sanitized_git_environment`'s, REUSED rather than copied a
    fourth time — `validate-carve-manifest.py` and
    `scripts/validate-contract-release.py` set that precedent."""
    manifest = scratch.write(scratch.clean())
    decoy = scratch.root / "decoy"
    decoy.mkdir()
    _git(decoy, "init", "-q", "-b", "main")
    (decoy / "README.md").write_text("no carve commit here\n",
                                     encoding="utf-8")
    _git(decoy, "add", "-A")
    _git(decoy, "commit", "-qm", "decoy")
    poisoned = dict(os.environ)
    poisoned["GIT_DIR"] = str(decoy / ".git")
    poisoned["GIT_WORK_TREE"] = str(decoy)
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest),
         "--repo", str(scratch.repo), "--json"],
        capture_output=True, text=True, check=False, env=poisoned)
    summary = verified(done)
    assert summary["source_count"] == 14, \
        "the ambient GIT_DIR must not decide which object store answers"


def test_a_symlink_may_not_stand_in_for_an_arrival(scratch: Scratch) -> None:
    """The floor's own evasion, and one no digest check at this level would
    notice: `read_bytes()` follows a link, so an arrival path that is a
    symlink to a test-bearing file elsewhere satisfied a row's declaration
    with a file that never arrived. `verify-carve-arrival.py` reads the
    destination with `lstat` and treats a link as a git link blob."""
    dest = scratch.destination("dox", {"src/mod.py": "scripts/pkg/mod.py"})
    elsewhere = dest / "vendored_alpha.py"
    elsewhere.write_text(SOURCE_FILES["scripts/pkg/test_alpha.py"],
                         encoding="utf-8")
    (dest / "tests").mkdir(parents=True, exist_ok=True)
    (dest / "tests/test_alpha.py").symlink_to(elsewhere)
    payload = refused(scratch.run(None, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "destination-test-shortfall")
    assert "ABSENT" in payload["detail"]
    assert "tests/test_alpha.py" in payload["detail"]


def test_a_symlinked_PARENT_may_not_stand_in_for_an_arrival_either(
        scratch: Scratch) -> None:
    """The half the first symlink fix did not cover, and which this lane's own
    reply to the finding got WRONG before measuring it: `lstat` does not
    follow only the FINAL component, so `tests/` being a link to a directory
    full of suites was still counted. Measured — `lstat` on a path whose
    PARENT is a link reports a regular file — so every component below
    `--dest-root` is checked, from the top down."""
    dest = scratch.destination("dox", {"src/mod.py": "scripts/pkg/mod.py"})
    elsewhere = dest / "vendored"
    elsewhere.mkdir(parents=True, exist_ok=True)
    (elsewhere / "test_alpha.py").write_text(
        SOURCE_FILES["scripts/pkg/test_alpha.py"], encoding="utf-8")
    (dest / "tests").symlink_to(elsewhere)
    payload = refused(scratch.run(None, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "destination-test-shortfall")
    assert "ABSENT" in payload["detail"]
    assert "tests/test_alpha.py" in payload["detail"]


def test_two_aliases_of_one_home_are_not_two_homes(scratch: Scratch) -> None:
    """The alias defect on the SOURCE side, and it is an arithmetic one rather
    than a naming one: two `destinations:` keys may share a `{repository,
    leg}` body — `check_shape` admits it — so a row listing two ALIASES of one
    home counted two homes and added an extra `(m − 1) × tests` term, while
    the destination verifier's own `any(...)` counted that physical home
    ONCE."""
    doc = scratch.clean()
    doc["destinations"]["xdox_alias"] = {
        "repository": "opensoft/openXdox-code", "leg": "code"}
    scratch.row(doc, "scripts/pkg/test_alpha.py")["also_replicated_to"] = \
        ["xdox_code", "xdox_alias"]
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "not distinct homes" in payload["detail"]


def test_a_row_is_not_also_replicated_where_it_already_moves(
        scratch: Scratch) -> None:
    """The same defect wearing the row's own placement: an
    `also_replicated_to:` entry that resolves to the row's OWN effective
    arrival would count that home twice."""
    doc = scratch.clean()
    doc["destinations"]["dox_alias"] = {
        "repository": "opensoft/openDox-code", "leg": "code"}
    scratch.row(doc, "scripts/pkg/test_alpha.py")["also_replicated_to"] = \
        ["dox_alias"]
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "already moves" in payload["detail"]


def test_an_absent_arrival_is_printed_even_when_the_total_balances(
        scratch: Scratch) -> None:
    """A MISSING FILE WAS THE SILENT ONE. `absent` was collected and never
    printed on a passing run, so a declared arrival that is NOT THERE could be
    hidden by another path carrying extra tests: `collected == declared`,
    exit 0, and the per-row delta the runbook promises by name was not shown.

    Built exactly that way: `tests/test_alpha.py` (3 declared) never arrives,
    and `src/mod.py` — declared 0 — carries 3 of the destination's own, so the
    totals match. The run passes, and it SAYS what is missing."""
    dest = scratch.destination("dox", {})
    (dest / "src").mkdir(parents=True, exist_ok=True)
    (dest / "src/mod.py").write_text(_tests(3, "the_legs_own"),
                                     encoding="utf-8")
    manifest = scratch.write(scratch.clean())
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest),
         "--repo", str(scratch.repo), "--destination", "dox_code",
         "--dest-root", str(dest)],
        capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "declared arrivals ABSENT: 1" in done.stdout, done.stdout
    assert "tests/test_alpha.py" in done.stdout
    assert "nothing regular at that path" in done.stdout


def test_a_declared_key_naming_no_row_at_all_refuses(
        scratch: Scratch) -> None:
    """The stale-key arm, on the runtime path rather than in a pytest
    assertion (Copilot, second round on #1080). The declaration is § 5.4's
    enumeration FOR THIS CARVE and a re-cut of it still carries these rows, so
    a key with no row means the table and the document have come apart —
    which is the drift the module said it refused and did not."""
    doc = scratch.clean()
    doc["rows"] = [row for row in doc["rows"]
                   if row["source_path"]
                   != "tests/corpus-adapter/test_no_home_vocabulary.py"]
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "no row for it at all" in payload["detail"] or \
        "no row for at all" in payload["detail"], payload["detail"]


@pytest.mark.parametrize("mutate,fragment", [
    (lambda doc: doc.__setitem__("rows", []), "EMPTY `rows:`"),
    (lambda doc: doc.__setitem__("moved_paths", []), "moved_paths"),
    (lambda doc: doc.__setitem__("moved_paths", "scripts/pkg/"), "moved_paths"),
    (lambda doc: doc.__setitem__("moved_paths", ["", "x/"]), "moved_paths"),
])
def test_a_floor_over_nothing_does_not_pass(scratch: Scratch, mutate, fragment
                                            ) -> None:
    """A CHECK THAT PASSES BY ASKING NOTHING is the shape this whole design
    refuses, and both spellings of it reached an `ok` report: with `rows: []`
    the mapping is empty and `totals()` computes `0 = 0`; with an empty or
    mistyped `moved_paths:` every row falls outside the declared surface and
    the mapping is empty again. Clause (a) is quantified over that surface, so
    an empty one makes the quantifier vacuous rather than satisfied."""
    doc = scratch.clean()
    mutate(doc)
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert fragment in payload["detail"], payload["detail"]


@pytest.mark.parametrize("key,value", [
    ("source_repository", ["opensoft/openxFactory"]),
    ("source_repository", ""),
    ("carve_commit", 12345),
    ("destinations", []),
    ("destinations", {}),
])
def test_the_scalars_are_typed_and_not_merely_present(
        scratch: Scratch, key: str, value) -> None:
    """A present key of the wrong TYPE reached the mapping. `repository_of`
    coerced a non-string `source_repository:` with `str()`, so a list arrived
    in the report as `"['opensoft/openxFactory']"` — measured to refuse
    downstream, because the declared homes then match nothing, which is a
    right answer by the wrong road and a message an operator has to decode.
    The presence checks are what this floor needs to COMPUTE; these are what
    it needs to compute the truth."""
    doc = scratch.clean()
    doc[key] = value
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert key in payload["detail"]


@pytest.mark.parametrize("value", ["dox_code", [], ["dox_code", "dox_code"],
                                   [""], [3]])
def test_a_present_also_replicated_to_is_read_or_refused_never_dropped(
        scratch: Scratch, value) -> None:
    """Treating every non-list — and `[]` — as "no replicas" let a malformed
    row UNDERCOUNT its own multiplicity while the sum went on balancing, which
    is the one failure shape this floor exists to make impossible. A field
    that is present and unreadable is not an absent one."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_alpha.py")["also_replicated_to"] = value
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "also_replicated_to" in payload["detail"]


def _names_the_table(node: ast.AST) -> bool:
    """Does this node READ `DECLARED_REPLICA_SETS`, under EITHER spelling?

    A bare `Name` inside the module, and `mapping.DECLARED_REPLICA_SETS` —
    an `Attribute` — from the verifier. The first version of this scan looked
    for the `Name` only and so passed over the verifier's own direct read,
    which was the very site the finding was about.
    """
    return ((isinstance(node, ast.Name)
             and node.id == "DECLARED_REPLICA_SETS")
            or (isinstance(node, ast.Attribute)
                and node.attr == "DECLARED_REPLICA_SETS"))


def test_every_read_of_the_declaration_goes_through_the_one_seam() -> None:
    """THE MIGRATION SEAM, ASSERTED RATHER THAN CLAIMED (Copilot, round 3 on
    #1080, accurate about a claim this module made and did not keep).
    `declared_replica_set` was called the single place FLOOR PART 1's
    successor pull request edits, while `refuse_stale_declarations` and the
    verifier's `--replica-at` admission read the table directly — so migrating
    the reader would have moved the SOURCE homes and left the stale check and
    the destination admission on the obsolete table, with nothing red.

    The scan is over the two SHIPPED files. `DECLARED_REPLICA_SETS` may appear
    only where it is defined and inside the two accessors; every other reader
    goes through `declared_homes()` or `declared_source_paths()`.
    """
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    seam = {"declared_source_paths", "declared_homes"}
    readers: dict[str, int] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for inner in ast.walk(node):
            if _names_the_table(inner):
                readers[node.name] = readers.get(node.name, 0) + 1
    assert set(readers) == seam, (
        "every read of the declaration must go through "
        f"{sorted(seam)}; these functions read it directly: {sorted(readers)}")
    verifier = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    assert not [n for n in ast.walk(verifier) if _names_the_table(n)], \
        "the verifier must reach the declaration through the accessors"
    assert MODULE.declared_source_paths() == \
        tuple(MODULE.DECLARED_REPLICA_SETS)
    assert MODULE.declared_homes("tests/corpus-adapter/test_conformance.py") \
        == RULED_REPLICA_HOMES
    assert MODULE.declared_homes("no/such/path.py") is None


def test_argparse_rejects_an_invocation_with_status_two_and_no_code(
        scratch: Scratch) -> None:
    """The docstring said argparse exits 1. It exits 2 — the same status a
    REFUSAL uses — so a caller classifying by status alone would file a usage
    error as a clean run, or a refusal as one. They are told apart by the
    OUTPUT: a refusal prints `FAIL <where>: <code>` (or a `{"result":
    "refused"}` object under `--json`) and argparse prints its own usage block
    with no code at all."""
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--no-such-flag"],
        capture_output=True, text=True, check=False)
    assert done.returncode == 2
    assert "usage:" in done.stderr
    assert "FAIL" not in done.stderr
    for code in RATIFIED_CODES:
        assert code not in done.stderr


# --------------------------------------------------------------------------
# Copilot rounds 5 and 6 — the key nobody resolved, the surface nobody
# bounded, the commit nobody shaped, and the row counted twice
# --------------------------------------------------------------------------

def test_a_retirement_may_not_be_at_a_destination_the_manifest_lacks(
        scratch: Scratch) -> None:
    """The retirement branch returned before `repository_of` was ever asked,
    so a moved row could name a FABRICATED `destinations:` key, point a
    shape-valid `retired:` block at that same fabricated placement, and have
    its tests SUBTRACTED from the identity as a RULED deletion. Measured on
    the landed manifest with one row mutated that way: `retired_tests` 31 →
    53 and exit 0.

    `retirement_of` already requires the block to retire the arrival the row
    ACTUALLY has, which is what makes the repair one line: the arrival's key
    is the same key the moved path resolves, so it is resolved before either
    branch."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row["destination"] = "made_up_leg"
    row["destination_path"] = "tests/test_alpha.py"
    retirement = copy.deepcopy(RETIREMENT)
    retirement["at"] = "made_up_leg"
    row["retired"] = retirement
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "made_up_leg" in payload["detail"]


def test_a_fabricated_retirement_does_not_silence_the_leg_that_owed_it(
        scratch: Scratch) -> None:
    """The same document at the leg, which is where it matters: the source
    side is not running there. Before the fix this run simply stopped asking
    for the file — on the landed manifest, 117 rows / 1,067 `def test_` became
    116 / 1,045 and the run exited 0, a leg passing because a live arrival had
    been deleted by a key naming nothing."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row["destination"] = "made_up_leg"
    row["destination_path"] = "tests/test_alpha.py"
    retirement = copy.deepcopy(RETIREMENT)
    retirement["at"] = "made_up_leg"
    row["retired"] = retirement
    dest = scratch.destination("dox", ARRIVALS)
    payload = refused(scratch.run(doc, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "test-mapping-unreadable")
    assert "made_up_leg" in payload["detail"]


def test_a_misspelled_destination_key_refuses_at_the_leg_and_not_only_at_source(
        scratch: Scratch) -> None:
    """`resolved_destination` degrades an unknown key to a 1-tuple that can
    never equal a resolved 2-tuple — which is right for TELLING THEM APART and
    was wrong as the only reading, because the row was then dropped as another
    leg's business. Only the source invocation called `repository_of`, and a
    leg does not run the source invocation."""
    doc = scratch.clean()
    scratch.row(doc, "scripts/pkg/test_alpha.py")["destination"] = "dox_kode"
    dest = scratch.destination("dox", ARRIVALS)
    payload = refused(scratch.run(doc, "--destination", "dox_code",
                                  "--dest-root", str(dest)),
                      "test-mapping-unreadable")
    assert "dox_kode" in payload["detail"]
    source = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "dox_kode" in source["detail"]


def test_an_absent_destination_stays_a_lost_test_and_is_not_a_leg_s_refusal(
        scratch: Scratch) -> None:
    """THE LINE THE FIX DRAWS, pinned so a later reading cannot move it
    quietly. `homes_of` draws it already: an absent or non-string
    `destination:` is NO HOME and the SOURCE side names it
    `test-home-missing`; a PRESENT key the manifest does not carry is a
    vocabulary error, and a leg is where that one is found. A leg refusing
    both would make every homeless row every destination's failure."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row.pop("destination")
    row.pop("destination_path")
    refused(scratch.run(doc), "test-home-missing")
    dest = scratch.destination("dox", ARRIVALS)
    summary = verified(scratch.run(doc, "--destination", "dox_code",
                                   "--dest-root", str(dest)))
    assert summary["rows_owed"] == 1, "src/mod.py alone; the homeless row is " \
        "not this leg's business"


def test_a_replica_outside_the_declared_surface_may_not_be_placed(
        scratch: Scratch) -> None:
    """`arrivals_for` filters its rows through `under_surface` and the two
    `--replica-at` admission sets did not, so a replica row OUTSIDE
    `moved_paths:` was admitted, counted from `tests_at_carve` and added to
    this destination's declared total — an obligation the SOURCE mapping does
    not carry, because `map_rows` skips exactly those rows. Measured on the
    landed manifest with one replica moved out of the surface: the
    openDox-code declaration rose 1,067 → 1,138 and the leg was refused a
    shortfall it did not have."""
    doc = scratch.clean()
    doc["moved_paths"] = ["scripts/pkg/"]
    dest = scratch.destination("dox", ARRIVALS)
    payload = refused(
        scratch.run(doc, "--destination", "dox_code", "--dest-root",
                    str(dest), "--replica-at",
                    "tests/corpus-adapter/test_conformance.py="
                    "tests/test_conformance.py"),
        "test-mapping-unreadable")
    assert "tests/corpus-adapter/test_conformance.py" in payload["detail"]
    assert verified(scratch.run(doc, "--destination", "dox_code",
                                "--dest-root", str(dest)))["declared"] == 3, \
        "and the same document without the flag is unchanged"


@pytest.mark.parametrize("value,fragment", [
    ("HEAD", "HEAD"),
    ("{commit}^{{tree}}", "^{tree}"),
    ("{commit}:scripts/pkg/mod.py\n{commit}", "\\n"),
    ("{COMMIT}", "40 lowercase hex"),
])
def test_the_carve_commit_is_a_commit_and_not_a_revision_expression(
        scratch: Scratch, value: str, fragment: str) -> None:
    """`carve_commit:` is interpolated into a newline-delimited `git cat-file
    --batch` request, so a TYPE is not enough: it is a REF INJECTION seat, the
    `source_path` newline defect this file already pins, wearing the other
    field.

    Measured on the landed manifest before the fix, no other mutation:
    `carve_commit: "<sha>:contracts/schemas/gate-intent.schema.yaml\n<sha>"`
    doubled every request line, the replies desynced, and the source side
    reported `source_count 0`, `Σ(destinations) 0`, `identity_holds true` and
    EXIT 0 over a surface carrying 4,411 `def test_`. A floor that reports
    zero and passes is the failure shape the whole design refuses."""
    doc = scratch.clean()
    doc["carve_commit"] = value.format(commit=scratch.commit,
                                       COMMIT=scratch.commit.upper())
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "40 lowercase hex" in payload["detail"]
    assert fragment in payload["detail"] or fragment == "40 lowercase hex"


def test_the_commit_shape_is_floor_part_1_s_own() -> None:
    """Two tools that disagreed about what a commit id IS would disagree about
    which documents are readable. FLOOR PART 1 owns the shape; this one is
    held equal to it here rather than by a comment claiming it."""
    assert MODULE.COMMIT_RE.pattern == PART_1.COMMIT_RE.pattern


def test_a_source_path_declared_twice_is_refused_not_counted_twice(
        scratch: Scratch) -> None:
    """`tests_at_carve` keys its counts BY PATH and collapses a duplicate,
    while `map_rows` emits one mapping per ROW — so both copies were counted
    and the identity went on balancing. Measured on the landed manifest with
    one 35-test row duplicated: `source_count` 4,411 → 4,446, `identity_holds`
    true, exit 0. FLOOR PART 1 calls the same document
    `carve-file-duplicated`; this tool runs where that validator does not."""
    doc = scratch.clean()
    doc["rows"].append(copy.deepcopy(
        scratch.row(doc, "scripts/pkg/test_alpha.py")))
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "scripts/pkg/test_alpha.py" in payload["detail"]
    assert "carve-file-duplicated" in payload["detail"]


@pytest.mark.parametrize("row", [
    {"disposition": "moved_verbatim", "destination": "dox_code",
     "destination_path": "tests/test_nameless.py"},
    {"source_path": "", "disposition": "not_moved",
     "reason": "deleted_at_carve"},
    {"source_path": ["scripts/pkg/test_alpha.py"],
     "disposition": "not_moved", "reason": "deleted_at_carve"},
    "a string where a row should be",
])
def test_a_row_without_a_usable_source_path_refuses_rather_than_raising(
        scratch: Scratch, row: Any) -> None:
    """Every question this floor asks is keyed by `source_path:`, and four
    readers subscripted it raw — a TRACEBACK and exit 1 against a documented
    contract of a named refusal and exit 2, for exactly the input most likely
    to be a hand-edited document."""
    doc = scratch.clean()
    doc["rows"].append(copy.deepcopy(row) if isinstance(row, dict) else row)
    done = scratch.run(doc)
    payload = refused(done, "test-mapping-unreadable")
    assert "source_path" in payload["detail"]
    assert "Traceback" not in done.stderr


def test_a_surface_that_selects_no_row_does_not_pass(
        scratch: Scratch) -> None:
    """Round 3 refused an EMPTY or mistyped `moved_paths:`; a well-formed one
    naming a prefix no row lies under is the same vacuum one step further on,
    and round 6 was right that the claim had been made and not kept. Measured
    on the landed manifest with `moved_paths: ["contracts/policies/"]`:
    `rows_in_surface 0`, `source_count 0`, exit 0. Clause (a) is a QUANTIFIER
    and a quantifier over the empty set is not a floor that holds."""
    doc = scratch.clean()
    doc["moved_paths"] = ["docs/", "openspec/changes/"]
    payload = refused(scratch.run(doc), "test-mapping-unreadable")
    assert "NOT ONE" in payload["detail"]
    doc["moved_paths"] = ["scripts/pkg/"]
    assert verified(scratch.run(doc))["rows_in_surface"] == 5, \
        "a surface that selects SOME rows is the operator's business, not " \
        "this refusal's"


def test_a_retired_row_with_surviving_copies_is_counted_once(
        scratch: Scratch) -> None:
    """`homed_rows` and `retired` are documented to add to
    `test_bearing_rows`, and a retired row KEEPS the homes its
    `also_replicated_to:` copies stand at — the identity `totals()` was
    corrected to compute two rounds ago — so such a row was counted in BOTH
    and the two summed to 147 of 146 on the landed manifest. The kinds
    partition the mapping; the homes do not."""
    doc = scratch.clean()
    row = scratch.row(doc, "scripts/pkg/test_alpha.py")
    row["also_replicated_to"] = ["xdox_code"]
    row["retired"] = copy.deepcopy(RETIREMENT)
    summary = verified(scratch.run(doc))
    assert summary["homed_rows"] + len(summary["retired"]) == \
        summary["test_bearing_rows"]
    assert summary["retired"][0]["homes"] == ["opensoft/openXdox-code"], \
        "and the copies the retirement did NOT delete are named in the report"


def test_the_arrival_reader_is_annotated_for_the_bytes_it_returns() -> None:
    """It said `int | None` while returning `read_bytes()`, so a type checker
    read the `mapping.count(blob)` at its one call site as an incompatible
    argument — a claim about its own signature, wrong in the direction that
    makes a reader distrust the checker rather than the code."""
    verifier = _load(SCRIPT, "verify_carve_test_mapping_under_test")
    assert verifier._tests_in.__annotations__["return"] == "bytes | None"


# --------------------------------------------------------------------------
# the landed document — the § 8.2 seat
# --------------------------------------------------------------------------

def the_landed_manifest() -> tuple[str, dict[str, Any]]:
    """The real document, REQUIRED. Absence is a failure and never a skip or
    an `assert True`: a green bar is indistinguishable from a pass to every
    reader, and `pytest-suite.yml` pins the skip count exactly."""
    path = REPO_ROOT / MODULE.MANIFEST_RELPATH
    assert path.is_file(), f"{path} is missing; FLOOR PART 2 has no subject"
    text = path.read_text(encoding="utf-8")
    return text, yaml.safe_load(text)


def test_the_real_repository_verifies_and_the_box_arithmetic_reproduces(
) -> None:
    """THE SEAT. `pytest-suite.yml` runs `tests/` whole, so this is FLOOR PART
    2's place in the required check — the seat `tests/carve_manifest` holds for
    FLOOR PART 1.

    The figures are § 5.4's own, re-derived rather than recited: source 4,411
    over 146 test-bearing rows, three test-bearing replicas carrying 30 at
    `m = 3`, and the destination columns the box states as 1,128 / 2,345 / 998.
    The FIRST of those three is 1,097 here and the difference is exactly the
    31 `def test_` of the two rows RULED 5656343213 retired at PR #1043 — the
    box was amended 2026-09-09 and the form was ruled 2026-09-13."""
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(REPO_ROOT), "--json"],
        capture_output=True, text=True, check=False)
    summary = verified(done)
    assert summary["rows"] == summary["rows_in_surface"], \
        "every row of the landed manifest is under its own declared surface"
    assert summary["test_bearing_rows"] == 146
    assert summary["source_count"] == 4411
    assert summary["replica_excess"] == 60
    assert summary["identity_holds"] is True
    assert summary["per_repository"]["opensoft/openXdox-code"] == 2345
    assert summary["per_repository"]["opensoft/openxFactory"] == 998
    assert summary["per_repository"]["opensoft/openDox-code"] + \
        summary["retired_tests"] == 1128
    assert [item["source_path"] for item in summary["retired"]] == [
        "tests/ideation-dashboard/test_intent_tray_dom.py",
        "tests/ideation-dashboard/test_wheel_verbs_dom.py"]
    assert summary["retired_tests"] == 31
    assert summary["retired_excess"] == -31
    for item in summary["retired"]:
        assert "5656343213" in item["ruling"]
    assert summary["destinations_sum"] == 4411 + 60 - 31


def test_no_row_of_the_landed_surface_is_a_lost_test() -> None:
    """Clause (a) over the real document, stated as its own assertion because
    it is the sentence the floor exists to make: *no test is lost*."""
    _text, doc = the_landed_manifest()
    counts = MODULE.tests_at_carve(REPO_ROOT, doc)
    mapped = MODULE.map_rows(doc, counts)
    homeless = [record.source_path for record in mapped
                if record.tests and not record.homes
                and record.kind != "retired"]
    assert homeless == []


def test_the_retained_column_stands_above_its_declaration_today() -> None:
    """The destination side over THIS repository, which is the one column a
    test can run against without a second checkout.

    IT IS A TOTAL AND NOT A PER-ROW EQUALITY, and the reason is in this
    assertion: `tests/ideation-dashboard/test_serve_column_split.py` declares 9
    `def test_` at the carve commit and carries 8, because § 3.4 slice S6
    (RULED Q4, `#656` comment `5642758731`) moved that test's SUBJECT to
    `opensoft/openDox-code`'s `tests/test_source_core_arm.py` and the file
    records the move in place. A per-row equality would go red on a RULED
    re-homing that lost nothing; the total holds with room."""
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(REPO_ROOT),
         "--destination", MODULE.RETAINED_TOKEN, "--json"],
        capture_output=True, text=True, check=False)
    summary = verified(done)
    assert summary["declared"] == 998
    assert summary["collected"] >= summary["declared"]
    assert summary["absent"] == []
    below = {item["source_path"]: (item["declared"], item["found"])
             for item in summary["below_declaration"]}
    assert below == {
        "tests/ideation-dashboard/test_serve_column_split.py": (9, 8)}, below


def test_the_runbook_carries_the_invocation_and_the_clause_d_blocker() -> None:
    """A floor nobody can run is prose. § 9 of the cutover runbook is where
    FLOOR PART 2 is described, so it is where the two invocations and the
    measured clause (d) finding belong."""
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "scripts/verify-carve-test-mapping.py" in text
    assert "--replica-at" in text
    assert "BUILD arc" in text
