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
the documented invocation succeeds and prints what its readers depend on. EVERY
behavioural test here goes through the subprocess, with no exception. The module
IS also loaded by path, once, for the constant assertions — the ratified refusal
vocabulary, the ruled manifest path, the ruled vocabularies, and the docstring's
record of the digest-field divergence — and the script's SOURCE is read once
more to assert that the closed vocabulary is COMPLETE: those are claims about
the file's contents rather than about a run.

CHECK 2 IS ANCESTRY, NOT IDENTITY (amended 2026-09-09, before the manifest was
authored), so most of what used to be one `carve-revision-mismatch` is now a
NAMED FILE. The tests below are shaped around that: a revision that merely
descends from the carve commit VERIFIES — that is a pull request's merge ref
and `main` after the manifest lands, the only two revisions this validator ever
actually runs at — while a surface file changed, deleted, chmod'd or added
since the carve refuses one by one. Each of those cases used to be answered by
the revision check before any file was read, and every test here that pins the
new answer was PROVEN to fail against `git show
origin/main:scripts/validate-carve-manifest.py` and to pass against this one.

THE REAL-REPOSITORY TEST IS THE § 8.2 SEAT AND IT DOES NOT SKIP.
`docs/opendox-carve-manifest.yaml` is authored by the § 6 ceremony at the
carve commit, AFTER this validator lands: before it the seat-holding branch
answered and the test asserted exit 0 with the `NO MANIFEST` line, and since it
landed the same test asserts exit 0 with the `OK` line instead — and from then
on a file that changes on `main` between the manifest and the move reds this
suite as a `carve-digest-mismatch`, which is the intended pressure of the
ceremony rather than a defect in it. It is a BRANCH and never a `pytest.skip`:
a skip reports as a green bar, which is indistinguishable from a pass to every
reader — and `pytest-suite.yml` pins the skip count exactly, so a conditional
skip here would red the required job.

THE TESTS THAT READ THE LANDED DOCUMENT NO LONGER BRANCH AT ALL (amended on a
Copilot finding, `#1030`, again on one in `#1032` — the retirement seat test was
authored beside that cleanup rather than after it and arrived carrying a SIXTH
copy of the idiom — and a third time on one in `#1043`, whose
`test_carved_reach_refuses_the_two_landed_retired_rows` was authored beside BOTH
and arrived carrying a SEVENTH. Three acts in a row is not three accidents: the
idiom is read off the neighbouring test that still legitimately branches, so
the cleanup has to be re-made by every act that adds a landed-document pin until
the seat test is the only branch left to copy). They had taken the seat too — `if not
manifest.is_file(): assert True; return` — and `assert True` REPORTS A PASS,
the same green bar the paragraph above refuses a skip for, so a checkout that
lost the file turned five pins on the landed document into five no-ops. They
read it through `the_landed_manifest()`, where the absence is a FAILURE: those
tests are about the document's contents, and there is no revision they can run
at without it. The seat test is the only absent-manifest arm left in this
module, and it must be — the absence is that test's own subject.

Hermetic: no network and no `nlm`/`gh`/`omp` (`tests/hermeticity.py`'s guarded
set); `git` is not guarded, and the environment it reads is PINNED rather than
inherited — `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a
repository-local identity, the same treatment and for the same reasons as
`tests/openxwallet_pin/test_verify_pin.py:32-40`: a CI runner has no ambient
git identity and a developer's global config can carry `core.hooksPath` or
`commit.gpgsign`, and the ambient installation must not change the answer.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
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
#
# `carve-unreadable` is IN the list. It used to be raised but excluded, so a
# caller branching on the code met a value the vocabulary said did not exist;
# `test_every_code_the_validator_can_emit_is_in_the_vocabulary` below now holds
# the tuple complete by scanning the script's own raise sites.
RATIFIED_CODES = (
    "carve-shape-invalid",
    "carve-revision-mismatch",
    "carve-digest-mismatch",
    "carve-path-absent",
    "carve-file-undeclared",
    "carve-file-duplicated",
    "carve-surface-vacuous",
    "carve-vocabulary-unknown",
    "carve-disposition-inconsistent",
    "carve-path-order-violation",
    "carve-shed-incomplete",
    # RULED Q6 (Brett Heap, 2026-09-12, `#656` comment `5648044785`) — the
    # `re_destined:` row form's three own findings. They keep the `carve-`
    # prefix the vocabulary's split with `arrival-*` depends on.
    "carve-re-destined-not-moved",
    "carve-re-destined-unruled",
    "carve-re-destined-chain",
    # RULED 5656343213 (Brett Heap, 2026-09-13, by interactive multi-choice, on
    # the question slice S8's author put in `#656` comment `5650335573` § 2) —
    # the `retired:` row form's three own findings, same prefix and same
    # reasoning as the Q6 trio above.
    "carve-retired-not-moved",
    "carve-retired-unruled",
    "carve-retired-surface-live",
    "carve-unreadable",
)

# RULING OQ-1's own list, verbatim. Three, not four.
RULED_EDIT_CLASSES = ["import rewrites", "path constants", "adapter calls"]

SURFACE = "scripts/pkg/"

# TWO REAL FILENAMES WHOSE BYTEWISE ORDER IS THE REVERSE OF THEIR CODE-POINT
# ORDER, which is what makes `path_order: bytewise_utf8` a claim with a
# consequence rather than a synonym for `sorted()`. `\xff` is not valid UTF-8
# and decodes (`surrogateescape`) to U+DCFF = 56575; `\xee\x80\x80` IS valid
# UTF-8 for U+E000 = 57344. So bytes put `\xee…` first (0xEE < 0xFF) and code
# points put `\udcff` first (56575 < 57344). A code-point sort would accept the
# reverse of this tuple; the validator must not.
PATHS_UTF8_CANNOT_HOLD = (b"scripts/pkg/\xee\x80\x80.py",
                          b"scripts/pkg/\xff.py")


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


def _git_bytes(root: Path, *args: str) -> bytes:
    """git, capturing BYTES — for `-z` output, whose records may hold a path
    that is not valid UTF-8 and which no text decoder may touch on the way in."""
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, check=False)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr!r}"
    return done.stdout


def _write(repo: Path, rel: str, text: str) -> None:
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _write_raw(repo: Path, rel: bytes, data: bytes) -> None:
    """Create a file whose NAME is bytes — the case `os.fsdecode` exists for.
    `Path` cannot hold `b"\\xff"` as text without a decoder, so the whole path
    is assembled and opened as bytes."""
    target = os.path.join(os.fsencode(repo), rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)


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
        the validator reads it — `-z`, `--full-tree`, `surrogateescape`, and a
        SEGMENT-AWARE prefix test.

        Copilot's second review was right that this used to claim that and not
        do it: without `-z`, git QUOTES a path it cannot print (`\\xff.py` comes
        back as `"scripts/pkg/\\377.py"`, quotes and octal included), so the
        bare `startswith` dropped exactly the filenames the ordering test needs
        — silently, since a dropped file just means no row is generated for it.
        The reading is duplicated rather than imported from the validator on
        purpose: a fixture that borrowed `in_surface` would agree with a broken
        `in_surface` too.
        """
        out: dict[str, str] = {}
        listing = _git_bytes(self.repo, "ls-tree", "-r", "-z", "--full-tree",
                             commit).decode("utf-8", "surrogateescape")
        prefix = SURFACE.rstrip("/")
        for record in listing.split("\0"):
            if not record:
                continue
            meta, _, path = record.partition("\t")
            mode, kind, _oid = meta.split(" ")
            if kind != "blob":
                continue
            if path == prefix or path.startswith(prefix + "/"):
                out[path] = mode
        return out

    def digest(self, commit: str, path: str) -> str:
        raw = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "blob",
             f"{commit}:{path}"], capture_output=True, check=True).stdout
        return hashlib.sha256(raw).hexdigest()


def add_paths_utf8_cannot_hold(scratch: Scratch) -> str:
    """Commit `PATHS_UTF8_CANNOT_HOLD` into the carve surface; return the sha.

    Two REAL files, not two strings in a document: the point of the ordering
    check is that git names files in bytes, so the fixture has to as well.
    """
    for rel in PATHS_UTF8_CANNOT_HOLD:
        _write_raw(scratch.repo, rel, b"X = 1\n")
    _git(scratch.repo, "add", "--", "scripts")
    _git(scratch.repo, "commit", "-q", "-m", "names Unicode cannot hold")
    return _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()


def commit_since_the_carve(scratch: Scratch, message: str,
                          *pathspecs: str) -> str:
    """`main` moves on after the manifest was cut; return the new sha.

    That is the situation this whole amendment is about, and every test below
    that builds one needs the same three lines. EXPLICIT PATHSPECS and never
    `git add -A`: the fixture writes the manifest into the scratch tree's
    `docs/` and it must stay UNTRACKED — a manifest committed into the
    repository it describes would change the tree it is being validated
    against. With no pathspecs the already-staged index is committed, which is
    how the `git rm` and `update-index --chmod` cases arrive here.
    """
    if pathspecs:
        _git(scratch.repo, "add", "--", *pathspecs)
    _git(scratch.repo, "commit", "-q", "-m", message)
    return _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()


def divergent_line(scratch: Scratch) -> str:
    """A commit that descends from `scratch.first` and NOT from `scratch.head`.

    The one revision the ancestry check must still refuse: a tree the carve
    commit is not in the history of, where a file-by-file comparison would be
    measuring two unrelated lines against each other.
    """
    _git(scratch.repo, "checkout", "-q", "-b", "divergent", scratch.first)
    _write(scratch.repo, "docs/divergent.md", "# a line the carve is not on\n")
    _git(scratch.repo, "add", "--", "docs/divergent.md")
    _git(scratch.repo, "commit", "-q", "-m", "a line the carve is not on")
    sha = _git(scratch.repo, "rev-parse", "HEAD").stdout.strip()
    _git(scratch.repo, "checkout", "-q", "main")
    return sha


# A 40-lowercase-hex string that passes check 1's grammar and names no object
# in any repository — the `carve_commit` a re-cut typo produces, and the one
# case ancestry cannot even ask about.
UNKNOWN_COMMIT = "deadbeef" * 5


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
    # `surrogateescape` on the encode, for the same reason the validator's sort
    # key uses it: a path is bytes, and a strict encode would raise out of the
    # GENERATOR for the filenames the ordering test is built on.
    for path in sorted(blobs,
                       key=lambda p: p.encode("utf-8", "surrogateescape")):
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


def test_every_code_the_validator_can_emit_is_in_the_vocabulary() -> None:
    """The closure, ASSERTED rather than documented.

    `REFUSAL_CODES` was referenced nowhere in the script, so nothing stopped a
    check raising a code outside it — and one already did: `carve-unreadable`
    was raised at five sites and excluded from the tuple by design, which left a
    caller that branches on the code (the stated reason the vocabulary is
    closed) meeting a value the vocabulary said did not exist. This scans the
    script's own raise sites, so the tuple cannot drift from them in either
    direction: no code raised but unlisted, and no code listed but never raised.

    THE SCAN IS `ast`, NOT A REGEX (Copilot review, PRRT_kwDOTAvnrs6guuUv,
    2026-09-09). The regex this replaced — `CarveRefusal\\(\\s*"([^"]+)"` —
    matched only a DOUBLE-quoted first argument, so a raise site written
    `CarveRefusal('carve-shape-invalid', ...)` — legal Python, and nothing in
    this file's own style forbids it — would silently miss the code it
    raises, which is exactly the blind spot this test exists to close: a code
    the validator can emit that never reaches the comparison below at all.
    Walking the parsed module for a `Call` to the bare name `CarveRefusal`
    whose first argument is a string constant reads the code the way Python
    itself does — single quotes, double quotes, and unusual whitespace inside
    the call are all one `ast.Constant` node — rather than the way one
    particular regex happens to expect it typed. A `CarveRefusal(...)` call
    whose first argument is NOT a string constant (a variable, an f-string)
    fails loudly rather than being silently skipped, so a future raise site
    that stopped being a literal could not go uncounted the same way.
    """
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SCRIPT))
    raised: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "CarveRefusal"):
            continue
        first = node.args[0] if node.args else None
        assert (isinstance(first, ast.Constant)
                and isinstance(first.value, str)), (
            f"{SCRIPT}:{node.lineno}: a CarveRefusal(...) call does not open "
            "with a string-literal code, so this scan cannot read it as "
            "evidence of anything")
        raised.add(first.value)
    ordered = sorted(raised)
    assert len(ordered) > 5, \
        f"the scan found only {ordered}, so it is not evidence of anything"
    assert [c for c in ordered if c not in MODULE.REFUSAL_CODES] == []
    assert sorted(MODULE.REFUSAL_CODES) == ordered


def test_the_module_records_the_digest_field_divergence() -> None:
    """The manifest's field is `sha256: <64 hex>` and the release-digest
    inventory it borrows its three consts from is `digest: sha256:<hex>`. The
    divergence originates in the memo, so it is recorded rather than corrected —
    and a reader of one document does NOT already know how to write the other,
    which is the sentence that has to be findable in the file."""
    doc = MODULE.__doc__ or ""
    assert "digest: sha256:<hex>" in doc, doc
    assert "memo § 1.2" in doc, doc


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


def test_a_named_manifest_that_does_not_exist_refuses(scratch: Scratch) -> None:
    """The seat-holding pass is for the DEFAULT path, and only for it.

    A caller that NAMED a manifest and got exit 0 because the path was wrong is
    the worst outcome this file can produce: the one branch here that is not
    fail-closed becomes the branch a typo selects, and a job verifying nothing
    reports green forever. `carve-unreadable`, because the environment could not
    hand the program a document at all.
    """
    missing = scratch.repo / "docs" / "not-the-carve-manifest.yaml"
    assert not missing.exists()
    done = run(scratch, "--manifest", str(missing))
    combined = done.stdout + done.stderr
    assert done.returncode == 2, combined
    assert ": carve-unreadable —" in combined, combined
    assert "Remediation:" in combined, combined
    assert "NO MANIFEST" not in combined, combined


def test_a_named_manifest_that_does_not_exist_refuses_in_json(
        scratch: Scratch) -> None:
    """`--json` says `refused` with the code, not `no-manifest`: a caller that
    branches on the field must not read a typo as `not written yet`."""
    done = run(scratch, "--manifest",
               str(scratch.repo / "docs" / "typo.yaml"), "--json")
    assert done.returncode == 2, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "refused"
    assert payload["code"] == "carve-unreadable"
    assert payload["code"] in RATIFIED_CODES


def test_a_relative_manifest_resolves_against_repo_not_cwd(
        scratch: Scratch, tmp_path: Path) -> None:
    """Copilot round 3: the help text says `--manifest`'s default is
    `<repo>/…`, but a RELATIVE override used to resolve against the caller's
    CWD instead — `--repo <other-tree> --manifest docs/….yaml` pointed at
    whatever sat under wherever the caller happened to be standing, the wrong
    file unless CWD and `--repo` coincide. `scratch.repo` carries the manifest;
    the subprocess is launched from `tmp_path`, its EMPTY parent, which holds
    no `docs/` at all — so the old resolution finds nothing there and the new
    one finds it under `--repo`."""
    scratch.write(clean_manifest(scratch))
    assert tmp_path != scratch.repo
    assert not (tmp_path / MODULE.MANIFEST_RELPATH).exists()
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(scratch.repo),
         "--manifest", MODULE.MANIFEST_RELPATH],
        cwd=tmp_path, capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "OK " in done.stdout, done.stdout
    # The resolved ABSOLUTE path is what the reader sees, not the relative
    # fragment the caller typed.
    assert str(scratch.repo / MODULE.MANIFEST_RELPATH) in done.stdout, \
        done.stdout


def test_at_verifies_an_earlier_carve_commit(scratch: Scratch) -> None:
    """The manifest is cut at the carve commit and `main` moves on; `--at`
    asks the question the manifest actually answers."""
    scratch.write(clean_manifest(scratch, scratch.first))
    done = run(scratch, "--at", scratch.first)
    assert done.returncode == 0, done.stdout + done.stderr
    assert scratch.first[:12] in done.stdout, done.stdout


def test_at_a_descendant_with_no_surface_change_verifies(
        scratch: Scratch) -> None:
    """`--at` A REVISION THE CARVE COMMIT IS AN ANCESTOR OF, with the surface
    untouched between them — the shape of every real run of this validator.

    Proven against `origin/main`'s validator, which required the tested
    revision to RESOLVE TO `carve_commit` and therefore refused this with
    `carve-revision-mismatch`: a pull request's merge ref is a commit no
    manifest can name, and `main` after the manifest lands is the manifest's
    own squash, so the landed check could not pass anywhere it would ever run.
    """
    doc = clean_manifest(scratch)
    _write(scratch.repo, "docs/later.md", "# outside the carve surface\n")
    later = commit_since_the_carve(scratch, "main moves on, off the surface",
                                   "docs/later.md")
    scratch.write(doc)
    done = run(scratch, "--at", later)
    assert done.returncode == 0, done.stdout + done.stderr
    # BOTH revisions named, because they differ.
    assert scratch.head[:12] in done.stdout, done.stdout
    assert f"verified at {later[:12]}" in done.stdout, done.stdout


def test_at_a_revision_the_carve_commit_does_not_reach_refuses(
        scratch: Scratch) -> None:
    """Ancestry is not "any two commits": a revision on a line the carve commit
    is not in the history of still refuses, because every comparison below it
    would be measuring two unrelated trees and reporting the difference as
    drift."""
    other = divergent_line(scratch)
    combined = refuses(scratch, clean_manifest(scratch),
                       "carve-revision-mismatch", "--at", other)
    assert "NOT AN ANCESTOR" in combined, combined
    assert other in combined, combined


def test_an_unresolvable_at_refuses(scratch: Scratch) -> None:
    refuses(scratch, clean_manifest(scratch), "carve-revision-mismatch",
            "--at", "no-such-revision")


# --------------------------------------------------------------------------
# check 1 — shape
# --------------------------------------------------------------------------

@pytest.mark.parametrize("version", [True, 1.0, "1", 1.5, None])
def test_a_schema_version_that_is_not_the_integer_one_refuses(
        scratch: Scratch, version: Any) -> None:
    """`true` and `1.0` are both EQUAL to 1 in Python, so a plain `!=` admitted
    them — `schema_version: true` verified a whole manifest. The first assertion
    of a fail-closed chain is the last place to be type-blind."""
    doc = clean_manifest(scratch)
    doc["schema_version"] = version
    refuses(scratch, doc, "carve-shape-invalid")


def test_an_unknown_top_level_key_refuses(scratch: Scratch) -> None:
    """The document grammar is closed too, not only the row's: an ignored
    `moved_path:` is a surface nobody declared, reported (if at all) as some
    other fault further down."""
    doc = clean_manifest(scratch)
    doc["moved_path"] = [SURFACE]
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "moved_path" in combined, combined


def test_the_optional_header_key_is_still_accepted(scratch: Scratch) -> None:
    """`header:` is where RULED OQ-E's convention break is recorded, so closing
    the top level must not close it out. The clean manifest carries one."""
    doc = clean_manifest(scratch)
    assert "header" in doc
    scratch.write(doc)
    assert run(scratch).returncode == 0


def test_an_unparseable_manifest_is_a_document_defect(scratch: Scratch) -> None:
    """A DOCUMENT defect, `carve-shape-invalid`, with the parser's position —
    not `carve-unreadable`. An empty manifest (parsing to `None`) and a manifest
    with one unclosed bracket are the same kind of fault to the same reader, and
    they used to answer with codes from two different vocabularies."""
    path = scratch.manifest_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("kind: opendox-carve-manifest\nrows: [unclosed\n",
                    encoding="utf-8")
    done = run(scratch)
    combined = done.stdout + done.stderr
    assert done.returncode == 2, combined
    assert ": carve-shape-invalid —" in combined, combined
    assert "not parseable YAML at line" in combined, combined
    assert "Traceback" not in done.stderr, done.stderr


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


@pytest.mark.parametrize("key,value", [("destination", "opendox_code"),
                                       ("destination_path", "src/x.py"),
                                       ("git_mode", "100644")])
def test_a_not_moved_row_carrying_a_destination_refuses(
        scratch: Scratch, key: str, value: str) -> None:
    """Symmetric with the digest it already refused, and for the same sentence:
    nothing arrives. Such a row used to PASS — and its `destination` was even
    validated against `destinations:` on the way — so it read at the destination
    as `this file goes there` over a disposition saying it does not. The memo's
    § 1.2 `not_moved` row is `source_path + disposition + reason + evidence`."""
    doc = clean_manifest(scratch)
    row_named(doc, "delta.py")[key] = value
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert key in combined, combined


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


def test_a_destination_entry_with_an_unknown_key_refuses(
        scratch: Scratch) -> None:
    """Copilot round 3: the module docstring claims `destinations.<key>` is a
    closed map like the rows, but an extra key inside one used to be admitted
    in silence — the closed-grammar guarantee the docstring states was true of
    the rows and not of the destinations beside them. A stray field here must
    refuse exactly as a stray field on a row does."""
    doc = clean_manifest(scratch)
    doc["destinations"]["opendox_code"]["branch"] = "main"
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "opendox_code" in combined, combined
    assert "branch" in combined, combined


def test_a_non_string_destination_key_refuses(scratch: Scratch) -> None:
    """Copilot round 4, PRRT_kwDOTAvnrs6guuUN: PyYAML parses an unquoted
    `destinations:` key such as `1:` as the int 1, not the label its author
    meant. That used to pass `check_shape()` in silence and reach
    `check_vocabularies`' `sorted(destinations)` the moment any row's
    (always-string) `destination` failed to match it — a document mixing
    that int key with a surviving string key raises a raw `TypeError` there,
    and the process exits 1: not one of the two exit codes this file's
    docstring promises, and a caller that only knows 0/2 reads it as a
    crash rather than a refusal.

    PROVED AGAINST THE PRE-FIX VALIDATOR — this round's base commit,
    `a25a3235`: the fixture below (an int key REPLACING `opendox_code`
    while every row that named it still does) written under `docs/` in a
    throwaway repo and run through `git show
    a25a3235:scripts/validate-carve-manifest.py` saved to a temp path,
    exits 1 with `TypeError: '<' not supported between instances of 'str'
    and 'int'` at `check_vocabularies`' `sorted(destinations)`. The fix
    exits 2 `carve-shape-invalid`, naming the offending key, before
    `check_vocabularies` — or any check after `check_shape` — ever runs.
    """
    doc = clean_manifest(scratch)
    doc["destinations"][1] = doc["destinations"].pop("opendox_code")
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "the key 1" in combined, combined
    assert "Traceback" not in combined, combined


# --------------------------------------------------------------------------
# check 2 — revision
# --------------------------------------------------------------------------

def test_a_head_that_has_moved_past_the_carve_commit_verifies(
        scratch: Scratch) -> None:
    """THE CASE THE AMENDMENT EXISTS FOR, at the documented invocation.

    The manifest is cut at the carve commit and `main` moves on — off the
    surface — and the plain `HEAD` run must pass. `origin/main`'s validator
    refused this as `carve-revision-mismatch`, which is why the manifest's own
    pull request could never have been green: CI checks out a merge ref, and
    after the manifest lands `HEAD` is its own squash. Neither is ever
    `carve_commit`, and neither ever will be.
    """
    doc = clean_manifest(scratch)
    _write(scratch.repo, "docs/later.md", "# outside the carve surface\n")
    later = commit_since_the_carve(scratch, "main moves on, off the surface",
                                   "docs/later.md")
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert f"verified at {later[:12]}" in done.stdout, done.stdout


def test_a_carve_commit_the_repository_does_not_carry_refuses(
        scratch: Scratch) -> None:
    """A referent nobody can resolve is a claim about nothing — and the
    reader has to be told THAT, not told that HEAD is some other sha. It is
    also the finding a checkout too shallow to reach the carve commit
    produces, which this validator cannot distinguish and does not pretend to.
    """
    doc = clean_manifest(scratch)
    doc["carve_commit"] = UNKNOWN_COMMIT
    combined = refuses(scratch, doc, "carve-revision-mismatch")
    assert "DOES NOT CARRY" in combined, combined
    assert UNKNOWN_COMMIT in combined, combined


def test_an_annotated_tags_object_id_used_as_the_referent_refuses(
        scratch: Scratch) -> None:
    """THE TAG IS A LABEL AND NEVER THE REFERENT — and an annotated tag's
    OBJECT ID is 40 lowercase hex, so it passes check 1's grammar exactly as a
    commit id does.

    Every git command below check 2 peels a tag silently: `merge-base`,
    `ls-tree` and `cat-file` would all have accepted it and verified the whole
    manifest against a referent the § 6 ceremony forbids. The landed identity
    check refused this as a SIDE EFFECT — a tag object id can never equal a
    `rev-parse HEAD^{commit}` — so ancestry has to refuse it deliberately.
    Copilot review `3972445078`, 2026-09-09.
    """
    _git(scratch.repo, "tag", "-a", "opendox-carve-0", "-m", "the label",
         scratch.head)
    tag_object = _git(scratch.repo, "rev-parse",
                      "opendox-carve-0").stdout.strip()
    assert tag_object != scratch.head, tag_object
    assert _git(scratch.repo, "cat-file", "-t",
                tag_object).stdout.strip() == "tag"
    doc = clean_manifest(scratch)
    doc["carve_commit"] = tag_object
    combined = refuses(scratch, doc, "carve-revision-mismatch")
    assert "PEELS to" in combined, combined
    assert scratch.head in combined, combined


def test_the_revision_check_runs_before_the_digests(scratch: Scratch) -> None:
    """A referent this repository cannot resolve is reported as ONE revision
    mismatch rather than as a pile of digest failures — the ordering is the
    finding, and the digests could not be recomputed at that commit anyway."""
    doc = clean_manifest(scratch)
    doc["carve_commit"] = UNKNOWN_COMMIT
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


def test_an_edit_line_past_the_end_of_the_blob_refuses(
        scratch: Scratch) -> None:
    """`beta.py` has three lines at the carve commit, so line 999999 is a claim
    nothing at the destination can check — which is the ONLY reason the line
    numbers are recorded. The blob is already read for the digest, so the bound
    is free; it was simply never applied."""
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["edits"][0]["lines"] = [1, 999999]
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "999999" in combined, combined
    assert "3 line(s)" in combined, combined


def test_an_edit_on_the_last_line_of_the_blob_passes(scratch: Scratch) -> None:
    """The bound is inclusive and off by nothing: the clean manifest's own
    `adapter calls` edit is on line 3 of a three-line file."""
    doc = clean_manifest(scratch)
    assert row_named(doc, "beta.py")["edits"][1]["lines"] == [3]
    scratch.write(doc)
    assert run(scratch).returncode == 0


# --------------------------------------------------------------------------
# check 3, pass 2 — the tree the carve would actually run against
# --------------------------------------------------------------------------

def test_a_surface_file_changed_since_the_carve_refuses(
        scratch: Scratch) -> None:
    """MEMO § 6 STEP 3, VERBATIM: "a file changed on main between the manifest
    and the move surfaces as `carve-digest-mismatch` on the next pull request".

    This is where that pressure lives now. `origin/main`'s validator answered
    the same fixture `carve-revision-mismatch` — the RIGHT outcome for the
    wrong reason, and one it would have given just as loudly for a revision on
    which nothing had changed at all.
    """
    doc = clean_manifest(scratch)
    _write(scratch.repo, "scripts/pkg/alpha.py", "ALPHA = 99\n")
    later = commit_since_the_carve(scratch, "alpha moves after the manifest",
                                   "scripts/pkg/alpha.py")
    combined = refuses(scratch, doc, "carve-digest-mismatch")
    assert "CHANGED SINCE THE CARVE" in combined, combined
    assert "scripts/pkg/alpha.py" in combined, combined
    # BOTH sides of the comparison are printed, and the second one is the real
    # sha256 at the tested revision rather than a restatement of the row.
    assert scratch.head[:12] in combined, combined
    assert later[:12] in combined, combined
    assert scratch.digest(later, "scripts/pkg/alpha.py") in combined, combined


def test_a_moved_row_whose_file_is_deleted_since_the_carve_refuses(
        scratch: Scratch) -> None:
    """A source the tree has dropped since the carve is a move nobody can
    review at the destination."""
    doc = clean_manifest(scratch)
    _git(scratch.repo, "rm", "-q", "--", "scripts/pkg/alpha.py")
    commit_since_the_carve(scratch, "alpha deleted after the manifest")
    combined = refuses(scratch, doc, "carve-path-absent")
    assert "DELETED SINCE THE CARVE" in combined, combined
    assert "scripts/pkg/alpha.py" in combined, combined


def test_a_mode_flip_since_the_carve_refuses(scratch: Scratch) -> None:
    """The mode is compared at BOTH revisions for the reason it is carried at
    all: a mode flip is the one change a blob digest cannot see, and one that
    lands after the carve would travel to the destination unnoticed.

    `update-index --chmod`, not `os.chmod`: the mode is staged directly, so the
    fixture does not depend on `core.fileMode` being honoured by the
    filesystem the tests happen to run on.
    """
    doc = clean_manifest(scratch)
    _git(scratch.repo, "update-index", "--chmod=+x", "scripts/pkg/alpha.py")
    commit_since_the_carve(scratch, "alpha becomes executable after the carve")
    combined = refuses(scratch, doc, "carve-digest-mismatch")
    assert "MODE DRIFT SINCE THE CARVE" in combined, combined
    assert "100755" in combined, combined


def test_a_lie_about_the_referent_outranks_a_change_since_the_carve(
        scratch: Scratch) -> None:
    """THE TWO-PASS ORDER, PINNED. A manifest that lies about its own referent
    is a DOCUMENT defect its author fixes by recomputing one digest; a file
    that moved on `main` afterwards is a TREE fact whose remedy is the § 6
    re-cut. The reader must be handed the first even when the second is also
    true — and `alpha.py` sorts BEFORE `gamma.py`, so a single row loop doing
    both comparisons would report the re-cut and choose the reader's remedy by
    filename.
    """
    doc = clean_manifest(scratch)
    row_named(doc, "gamma.py")["sha256"] = "0" * 64
    _write(scratch.repo, "scripts/pkg/alpha.py", "ALPHA = 99\n")
    commit_since_the_carve(scratch, "alpha moves after the manifest",
                           "scripts/pkg/alpha.py")
    combined = refuses(scratch, doc, "carve-digest-mismatch")
    assert "DIGEST DRIFT" in combined, combined
    assert "gamma.py" in combined, combined
    assert "CHANGED SINCE THE CARVE" not in combined, combined


# --------------------------------------------------------------------------
# check 4 — surface completeness
# --------------------------------------------------------------------------

def test_a_moved_paths_prefix_that_matches_nothing_refuses(
        scratch: Scratch) -> None:
    """The completeness check is only as good as the prefix list. A mistyped
    prefix contributes an EMPTY surface while looking like coverage in review,
    and the silent case — the typo and its rows dropped together — is exactly
    the hand-editing error a ~430-row manifest invites."""
    doc = clean_manifest(scratch)
    doc["moved_paths"] = [SURFACE, "scripts/ideation_dashbord"]
    combined = refuses(scratch, doc, "carve-surface-vacuous")
    assert "scripts/ideation_dashbord" in combined, combined


def test_two_rows_arriving_at_one_destination_path_refuse(
        scratch: Scratch) -> None:
    """`seen` guarantees uniqueness on the SOURCE side only. Two sources sent to
    one destination path means one overwrites the other at the destination, and
    the manifest — read as the carve's instruction sheet — does not say which."""
    doc = clean_manifest(scratch)
    alpha = row_named(doc, "alpha.py")
    gamma = row_named(doc, "gamma.py")
    gamma["destination"] = alpha["destination"]
    gamma["destination_path"] = alpha["destination_path"]
    combined = refuses(scratch, doc, "carve-file-duplicated")
    assert "DESTINATION" in combined, combined


def test_two_destination_aliases_sharing_a_body_still_refuse_a_duplicate_arrival(
        scratch: Scratch) -> None:
    """S8 (RE-VERIFICATION of `d97371d1`, 2026-09-09). The duplicate-arrival
    check used to key on the manifest's own `destination` ALIAS
    (`(destination, destination_path)`), not on the REAL arrival. Two KEYS of
    `destinations:` may declare an identical `{repository, leg}` body — the
    grammar does not forbid it — and two rows naming the two DIFFERENT keys
    with one shared `destination_path` used to pass silently: keyed on the
    alias they look like two different destinations, but they are one real
    file, and one of them overwrites the other exactly as
    `carve-file-duplicated` exists to refuse. Proved against the pre-fix
    validator: this fixture exits 0 under `git show
    HEAD:scripts/validate-carve-manifest.py` at the round-3 head `d97371d1`,
    and exit 2 `carve-file-duplicated` under the fix."""
    doc = clean_manifest(scratch)
    doc["destinations"]["opendox_code_alias"] = dict(
        doc["destinations"]["opendox_code"])
    alpha = row_named(doc, "alpha.py")
    gamma = row_named(doc, "gamma.py")
    assert gamma["destination"] == alpha["destination"] == "opendox_code"
    gamma["destination"] = "opendox_code_alias"
    gamma["destination_path"] = alpha["destination_path"]
    combined = refuses(scratch, doc, "carve-file-duplicated")
    assert "destination" in combined, combined


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


def test_a_file_added_under_the_surface_since_the_carve_refuses(
        scratch: Scratch) -> None:
    """The second half of memo § 6 step 3's pressure, and the half no digest
    can carry: a file ADDED under the surface after the carve is in no row, and
    a file in no row is an UNDECLARED MOVEMENT (RULING OQ-1). `origin/main`'s
    validator reached this fixture as `carve-revision-mismatch`, naming a sha
    instead of the file."""
    doc = clean_manifest(scratch)
    _write(scratch.repo, "scripts/pkg/epsilon.py", "EPSILON = 5\n")
    commit_since_the_carve(scratch, "a new module under the carve surface",
                           "scripts/pkg/epsilon.py")
    combined = refuses(scratch, doc, "carve-file-undeclared")
    assert "APPEARED" in combined, combined
    assert "scripts/pkg/epsilon.py" in combined, combined


def test_a_not_moved_row_whose_file_is_deleted_since_the_carve_refuses(
        scratch: Scratch) -> None:
    """The digest loop never reads a `not_moved` row, so check 3's pass 2
    cannot see this one — the surface walk at the tested revision is what
    catches it, exactly as the referent-side walk already catches a `not_moved`
    row for a path the carve commit never carried."""
    doc = clean_manifest(scratch)
    _git(scratch.repo, "rm", "-q", "--", "scripts/pkg/delta.py")
    commit_since_the_carve(scratch, "the adapter file deleted after the carve")
    combined = refuses(scratch, doc, "carve-path-absent")
    assert "DELETED SINCE THE CARVE" in combined, combined
    assert "scripts/pkg/delta.py" in combined, combined
    assert "not_moved" in combined, combined


def test_a_file_added_outside_the_surface_since_the_carve_does_not_refuse(
        scratch: Scratch) -> None:
    """The second walk is the SURFACE's, not the tree's. `main` growing a file
    the carve does not touch is not the carve's business, and a gate that could
    not tell the two apart would be the identity check again under another
    name."""
    doc = clean_manifest(scratch)
    _write(scratch.repo, "docs/unrelated.md",
           "# nothing to do with the carve\n")
    commit_since_the_carve(scratch, "an unrelated document",
                           "docs/unrelated.md")
    scratch.write(doc)
    assert run(scratch).returncode == 0


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
    """Under every reason but `replicated_at_destination` (RULED Q-L7 (a)).

    `delta.py` is the fixture's `stays_openxfactory_adapter` row, which is the
    shape that must keep refusing: it is RULING OQ-B's three
    `tests/notebooklm/*` rows, which STAY here and take their import rewrite in
    openxFactory, and whose evidence says in as many words that "a not_moved
    row cannot carry an edit". They have no replica for a declared line to be
    applied at, so nothing about the amendment reaches them.
    """
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
    # The revision the run was VERIFIED at, always carried — equal to the carve
    # commit here, because nothing has moved.
    assert payload["verified_at"] == scratch.head
    assert payload["rows"] == 4
    assert payload["digests_recomputed"] == 3
    assert payload["surface"] == 4
    assert payload["dispositions"]["not_moved"] == 1


def test_json_names_the_verified_revision_when_it_differs(
        scratch: Scratch) -> None:
    """A caller reading the JSON must be able to tell WHICH revision was
    verified — on a merge ref the two are never the same commit, and a summary
    that carried only `carve_commit` would say nothing about what was
    actually read."""
    doc = clean_manifest(scratch)
    _write(scratch.repo, "docs/later.md", "# outside the carve surface\n")
    later = commit_since_the_carve(scratch, "main moves on, off the surface",
                                   "docs/later.md")
    scratch.write(doc)
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["carve_commit"] == scratch.head
    assert payload["verified_at"] == later


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
# the exit-code contract holds for the inputs Unicode cannot hold
# --------------------------------------------------------------------------

def test_a_manifest_that_is_not_utf8_refuses_rather_than_crashing(
        scratch: Scratch) -> None:
    """`UnicodeDecodeError` is a `ValueError`, not an `OSError`, so it used to
    leave this process as a traceback and exit 1 — the exit code the module
    docstring says does not exist. It must arrive as the named refusal."""
    path = scratch.manifest_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"kind: opendox-carve-manifest\nheader: \xff\xfe\n")
    done = run(scratch)
    assert done.returncode == 2, done.stdout + done.stderr
    assert "carve-unreadable" in done.stdout + done.stderr
    assert "Traceback" not in done.stderr, done.stderr


def test_the_fixture_reads_the_tree_the_way_the_validator_does(
        scratch: Scratch) -> None:
    """Copilot's second review, pinned: without `-z` git QUOTES a path it cannot
    print, so `Scratch.blobs()` used to DROP the two filenames below — silently,
    because a dropped file simply produces no row. A fixture generator that
    cannot see a file cannot generate the case that file exists for."""
    commit = add_paths_utf8_cannot_hold(scratch)
    seen = scratch.blobs(commit)
    for raw in PATHS_UTF8_CANNOT_HOLD:
        assert os.fsdecode(raw) in seen, sorted(map(repr, seen))
    assert not [p for p in seen if p.startswith('"')], sorted(map(repr, seen))


def test_the_row_order_is_bytewise_and_not_by_code_point(
        scratch: Scratch) -> None:
    """`path_order: bytewise_utf8` DISTINGUISHES ITSELF from a code-point sort,
    and this is the fixture in which the two disagree.

    Both real files: `\\xff` is not valid UTF-8 and decodes to U+DCFF (56575),
    while `\\xee\\x80\\x80` is valid UTF-8 for U+E000 (57344) — so the bytes and
    the code points order them oppositely. The correct (bytewise) order passes;
    feeding the validator the code-point order, which a `sorted(paths)`
    implementation would have accepted, refuses.

    This replaces a test that called `check_disposition_consistency` in process,
    asserted nothing, and used two paths that agree under both orders — so the
    suite pinned `the encode does not raise` and nothing about the ordering.
    """
    commit = add_paths_utf8_cannot_hold(scratch)
    doc = clean_manifest(scratch, commit)
    paths = [row["source_path"] for row in doc["rows"]]
    bytewise = sorted(paths, key=lambda p: p.encode("utf-8", "surrogateescape"))
    by_code_point = sorted(paths)
    assert bytewise != by_code_point, \
        f"the fixture is not divergent, so it proves nothing: {paths!r}"
    assert paths == bytewise, f"the generator must emit bytewise: {paths!r}"

    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr

    order = {row["source_path"]: row for row in doc["rows"]}
    doc["rows"] = [order[path] for path in by_code_point]
    refuses(scratch, doc, "carve-path-order-violation")


# --------------------------------------------------------------------------
# RULED Q-L7 (a) — the two grammar extensions
#
# Brett Heap, 2026-09-10, verbatim "rule Q-L7 (a)" (`#656` comment
# `5618683833`), after carve leg 1 measured two facts the grammar could not
# hold: a row was either MOVED or REPLICATED, and a replica was byte-identical
# and declared no line. Both halves are exercised HERE against a generated
# manifest, and once against the real one in the § 8.2 seat below.
# --------------------------------------------------------------------------

def _as_replica(doc: dict[str, Any], name: str = "delta.py"
                ) -> dict[str, Any]:
    """Turn the fixture's `not_moved` row into a REPLICA row and return it.

    The fixture generates a `stays_openxfactory_adapter` row, which is the one
    reason under which `edits:` must keep refusing — so the positive cases have
    to move it to `replicated_at_destination` explicitly rather than inheriting
    it, and the two reasons stay visibly different in every test below.
    """
    row = row_named(doc, name)
    row["reason"] = "replicated_at_destination"
    row["evidence"] = ("a replica at each destination, retained here "
                       "(RULED OQ-A/OQ-C)")
    return row


def test_a_moved_row_may_also_be_replicated_at_another_destination(
        scratch: Scratch) -> None:
    """The first half of the ruling: `tests/…/session_fixtures.py` moves to
    `opendox_code` and is ALSO replicated at `openxdox_code`, because the
    replicated conftest imports it unconditionally at both legs."""
    doc = clean_manifest(scratch)
    row = row_named(doc, "beta.py")
    assert row["destination"] == "openxdox_code", row
    row["also_replicated_to"] = ["opendox_code"]
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout


def test_a_verbatim_row_may_also_be_replicated(scratch: Scratch) -> None:
    """`also_replicated_to:` is on BOTH moved dispositions. A verbatim row
    replicated elsewhere is coherent — the same bytes at both places — and
    refusing it would be a rule nothing in the ruling asks for."""
    doc = clean_manifest(scratch)
    row_named(doc, "alpha.py")["also_replicated_to"] = ["openxdox_code"]
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_an_also_replicated_destination_the_manifest_does_not_declare_refuses(
        scratch: Scratch) -> None:
    """The same membership test `destination` gets, for the same reason: one
    typo otherwise replicates a file to a repository nobody declared."""
    doc = clean_manifest(scratch)
    row_named(doc, "beta.py")["also_replicated_to"] = ["opendox_kode"]
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_a_row_may_not_be_also_replicated_at_its_own_destination(
        scratch: Scratch) -> None:
    """ALSO means somewhere else. A row replicating a file at the destination
    it already moves to would let `--replica-at` re-point an arrival the
    manifest declared, which is the one thing the manifest is for."""
    doc = clean_manifest(scratch)
    row = row_named(doc, "beta.py")
    row["also_replicated_to"] = [row["destination"]]
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "also_replicated_to" in combined, combined


def test_a_malformed_also_replicated_to_refuses(scratch: Scratch) -> None:
    """Shape, in check 1: a NON-EMPTY list of distinct non-empty labels.

    The empty list is refused rather than ignored on `moved_paths:`' own
    reasoning one level down — it declares no replica while reading in a diff
    like a row that declares one — and a repeated label is refused for the
    reason `--replica-at`'s repeated key is at the destination.
    """
    for value in ([], "opendox_code", [""], ["opendox_code", "opendox_code"],
                  [None], [["opendox_code"]]):
        doc = clean_manifest(scratch)
        row_named(doc, "beta.py")["also_replicated_to"] = value
        refuses(scratch, doc, "carve-shape-invalid")


def test_a_not_moved_row_may_not_carry_also_replicated_to(
        scratch: Scratch) -> None:
    """A `not_moved` row declares no destination, so it cannot declare an
    ADDITIONAL one — and the refusal is its own arm rather than the generic
    "nothing arrives" message, which is false of a replica row."""
    doc = clean_manifest(scratch)
    _as_replica(doc)["also_replicated_to"] = ["opendox_code"]
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "also_replicated_to" in combined, combined
    assert "cannot declare an additional one" in combined, combined


def test_a_replica_row_may_declare_edits(scratch: Scratch) -> None:
    """The second half of the ruling: the conftest replica's `:25`
    `REPO_ROOT = HERE.parent.parent`, which must read one level shallower at
    every replica because the copy lands one directory up."""
    doc = clean_manifest(scratch)
    _as_replica(doc)["edits"] = [
        {"class": "path constants", "lines": [1],
         "note": "the replica lands one directory shallower"}]
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout


def test_a_replica_rows_declared_line_past_the_end_of_the_blob_refuses(
        scratch: Scratch) -> None:
    """The line bound is the SOURCE BLOB at the carve commit, exactly as a
    moved row's is — and a replica carries no `sha256`, so nothing had read its
    blob before this check. `delta.py` is one line long."""
    doc = clean_manifest(scratch)
    _as_replica(doc)["edits"] = [{"class": "path constants", "lines": [2]}]
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "names line 2" in combined, combined


def test_a_replica_rows_edit_class_is_still_closed(scratch: Scratch) -> None:
    """An edit in no class is an UNDECLARED MOVEMENT wherever it is declared:
    the replica grammar widens the rows that may carry `edits:` and widens no
    vocabulary."""
    doc = clean_manifest(scratch)
    _as_replica(doc)["edits"] = [{"class": "depth arithmetic", "lines": [1]}]
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_a_replica_row_with_an_empty_edits_list_is_not_a_declaration(
        scratch: Scratch) -> None:
    """`edits: []` on a replica is the empty-list case check 1 owns for every
    row, and it stays that: a list is required to hold at least one entry
    before check 6 is asked whether the row may hold one at all."""
    doc = clean_manifest(scratch)
    _as_replica(doc)["edits"] = [{"class": "path constants", "lines": []}]
    refuses(scratch, doc, "carve-shape-invalid")


def test_the_grammar_extension_names_the_ruling_and_not_the_owed_field(
        scratch: Scratch) -> None:
    """The disclosure, asserted in the file that carries it.

    RULING OQ-K owes FLOOR PART 1 a field naming the REPOSITORIES a
    test-bearing replica's copies land in, for the multiplicity sum. This
    amendment does not author it — different subject, different consumer — and
    a reader must be able to find that said rather than infer it from silence.
    """
    doc = MODULE.__doc__ or ""
    assert "also_replicated_to" in doc, doc
    assert "RULED Q-L7 (a)" in doc, doc
    assert "FLOOR PART 2" in doc, doc
    assert MODULE.REPLICA_REASON == "replicated_at_destination"


# --------------------------------------------------------------------------
# RULED Q6 — the `re_destined:` row form
#
# Brett Heap, 2026-09-12, by interactive multi-choice (`#656` comment
# `5648044785`), adopting the RECOMMENDED answer of openDox-spec
# `docs/front-end-package-boundary.md` § 6 Q6 at `7d12428c`. The THIRD
# grammar extension and the FIRST about PLACEMENT: a moved row whose
# placement a ruling has corrected carries where it went, and the floor asks
# its arrival question there instead. Every case below is a generated
# manifest and a real tree; the landed manifest — which carried the form and
# used it NOWHERE as PR #1011 landed it, and carries FOUR re-destined rows
# since § 3.4 slice S5 (PR #1023) — is asserted separately in the § 8.2 seat.
# (Stated in the same shape as the retirement section below, on the same
# reading: this sentence said "uses it nowhere" in the PRESENT tense until
# slice S5 made it false, and it was found while sweeping for exactly that
# defect in THIS act's own vocabulary — openxFactory PR #1043.)
# --------------------------------------------------------------------------

RULING_CITATION = "`#656` comment 5648044785 (RULED Q6, Brett Heap 2026-09-12)"


def _re_destine(doc: dict[str, Any], name: str = "beta.py",
                to: str = "opendox_code",
                to_path: str = "src/opendox/beta.py",
                **override: Any) -> dict[str, Any]:
    """Re-destine a generated row, and return it.

    `from`/`from_path` are READ OFF THE ROW rather than typed, because that is
    what the form requires them to be — a fixture that spelled them out would
    go on agreeing with itself after the row moved and stop being evidence.
    `beta.py` by default: the `moved_with_declared_edit` row, so the cases
    below exercise a re-destination of a row that also carries `edits:`, which
    is S8's actual shape.
    """
    row = row_named(doc, name)
    block: dict[str, Any] = {
        "from": row["destination"],
        "from_path": row["destination_path"],
        "to": to,
        "to_path": to_path,
        "ruling": RULING_CITATION,
    }
    block.update(override)
    row["re_destined"] = block
    return row


def _summary(scratch: Scratch, doc: dict[str, Any]) -> dict[str, Any]:
    """Write `doc`, run with `--json`, and return the summary of a clean run."""
    scratch.write(doc)
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    return json.loads(done.stdout)


def test_a_moved_row_may_be_re_destined_by_a_ruling(scratch: Scratch) -> None:
    """The form itself: `beta.py` moved to `openxdox_code` at the carve and a
    ruling has since re-homed it at `opendox_code`, which is slice S8's shape
    in miniature (23 test files placed by RULED OQ-G's imports rule at a leg
    that cannot run them)."""
    doc = clean_manifest(scratch)
    _re_destine(doc)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout
    assert "1 row(s) RE-DESTINED by ruling" in done.stdout, done.stdout


def test_a_verbatim_row_may_be_re_destined_and_keeps_its_digest(
        scratch: Scratch) -> None:
    """The field is on BOTH moved dispositions, and it moves NO digest: the
    same number of blobs is recomputed with the re-destination as without it,
    because a `sha256` is a claim about the SOURCE blob at the carve commit and
    where the file now lives says nothing about it."""
    before = _summary(scratch, clean_manifest(scratch))
    doc = clean_manifest(scratch)
    row = _re_destine(doc, "alpha.py", to="openxdox_code",
                      to_path="src/openxdox/alpha.py")
    after = _summary(scratch, doc)
    assert row["disposition"] == "moved_verbatim", row
    assert after["digests_recomputed"] == before["digests_recomputed"], after
    assert after["dispositions"] == before["dispositions"], after
    assert after["carve_commit"] == before["carve_commit"], after


def test_the_summary_counts_the_re_destined_rows(scratch: Scratch) -> None:
    """Counted in `--json` and printed on the human line — and ZERO is a state
    the log records too, which is what the landed manifest reads as until S8
    uses the form."""
    clean = _summary(scratch, clean_manifest(scratch))
    assert clean["re_destined"] == 0, clean
    doc = clean_manifest(scratch)
    _re_destine(doc)
    _re_destine(doc, "gamma.py", to="openxdox_code",
                to_path="src/openxdox/gamma.py")
    assert _summary(scratch, doc)["re_destined"] == 2


def test_re_destined_on_a_not_moved_row_refuses(scratch: Scratch) -> None:
    """A row that placed nothing has no arrival to re-place — under EVERY
    `not_moved` reason, the replica one included: a replica's copies are
    placed by the leg and declared with `--replica-at` (RULED OQ-C), so
    re-destining one would re-point a placement this manifest never made."""
    for make_replica in (False, True):
        doc = clean_manifest(scratch)
        row = _as_replica(doc) if make_replica else row_named(doc, "delta.py")
        row["re_destined"] = {
            "from": "opendox_code", "from_path": "src/opendox/delta.py",
            "to": "openxdox_code", "to_path": "src/openxdox/delta.py",
            "ruling": RULING_CITATION,
        }
        combined = refuses(scratch, doc, "carve-re-destined-not-moved")
        assert "re_destined" in combined, combined


def test_a_re_destination_with_no_ruling_refuses(scratch: Scratch) -> None:
    """The ruling's own SCOPE answer, as running code: "require a `ruling:`
    field naming the comment that ordered it, validated present, so the form
    cannot become a quiet way to move a file after the carve is closed". Its
    own code, because an absent citation is a governance defect and not a
    typo."""
    for value in (None, "", "   ", 5648044785, ["#656"]):
        doc = clean_manifest(scratch)
        row = _re_destine(doc)
        if value is None:
            del row["re_destined"]["ruling"]
        else:
            row["re_destined"]["ruling"] = value
        refuses(scratch, doc, "carve-re-destined-unruled")


def test_the_citations_form_is_not_constrained(scratch: Scratch) -> None:
    """PRESENT is what the ruling asked for. A comment id, a `#656` reference
    and a pull request URL are all how this estate cites a ruling, and a
    pattern here would refuse a legitimate one and teach the author to write
    whatever the pattern wanted."""
    for citation in ("5648044785", "#656 comment 5648044785",
                     "https://github.com/opensoft/openxFactory/pull/1011"):
        doc = clean_manifest(scratch)
        _re_destine(doc, ruling=citation)
        scratch.write(doc)
        done = run(scratch)
        assert done.returncode == 0, done.stdout + done.stderr


def test_a_re_destination_to_the_destination_it_came_from_refuses(
        scratch: Scratch) -> None:
    """RULED Q6 makes `to` a `destinations:` key that is NOT `from`. A move
    that lands where it started declares nothing, and a file that changes only
    its PATH at one leg has not been re-homed at all — the row's own
    `destination_path:` is the field that says where it lands."""
    doc = clean_manifest(scratch)
    row = _re_destine(doc)
    row["re_destined"]["to"] = row["re_destined"]["from"]
    row["re_destined"]["to_path"] = "src/openxdox/moved.py"
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "re_destined" in combined, combined


def test_a_re_destination_between_two_aliases_of_one_leg_refuses(
        scratch: Scratch) -> None:
    """THE RESOLVED-IDENTITY READING of `to != from` (§ 3.4 slice S8; the
    follow-up REGISTERED at `#1011`'s landing, `opensoft/openxFactory#656`,
    lane `openxfactory-4-opendox-extraction`).

    `check_shape` deliberately ADMITS two `destinations:` keys sharing one
    `{repository, leg}` body — its own comment says why — and a key is a LABEL,
    never a referent. So `to != from` compared as STRINGS left exactly one
    hole in the check that is supposed to guarantee a re-destination MOVES the
    file: an ALIAS PAIR passed. The document that results is unsatisfiable at
    the destination, which is the point — `verify-carve-arrival.py` would
    require these bytes PRESENT (this row's arrival) and ABSENT (its vacation)
    at ONE real leg, and the leg would refuse `arrival-not-vacated` on a file
    the manifest still says it carries. Refused here, at the gate that runs
    first, in the same shape `check_surface`'s duplicate-arrival map already
    uses.
    """
    doc = clean_manifest(scratch)
    doc["destinations"]["openxdox_code_alias"] = dict(
        doc["destinations"]["openxdox_code"])
    row = _re_destine(doc, to="openxdox_code_alias",
                      to_path="src/openxdox/relocated.py")
    assert row["re_destined"]["from"] == "openxdox_code", row
    assert row["re_destined"]["to"] != row["re_destined"]["from"], row
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "openxdox_code_alias" in combined, combined
    assert "ONE REAL DESTINATION" in combined, combined
    assert "opensoft/openXdox-code" in combined, combined


def test_an_alias_that_is_a_DIFFERENT_leg_is_a_lawful_re_destination(
        scratch: Scratch) -> None:
    """The other side of the same reading, so the check is a discriminator and
    not a blanket refusal: two keys whose `{repository, leg}` bodies DIFFER are
    two destinations, and a re-destination between them moves the file. Only
    the resolved IDENTITY is compared — never the spelling of the key."""
    doc = clean_manifest(scratch)
    doc["destinations"]["opendox_root"] = {
        "repository": "opensoft/openDox-code", "leg": "assembly"}
    _re_destine(doc, to="opendox_root", to_path="src/opendox/beta.py")
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 row(s) RE-DESTINED by ruling" in done.stdout, done.stdout


def test_a_chain_spelled_across_two_aliases_of_one_leg_refuses(
        scratch: Scratch) -> None:
    """The chain check takes the same reading, for the same reason: the arrival
    one row CREATES is the arrival the other MOVES ON even where the two rows
    spell that one real leg with two different keys. A reader would still have
    to compose two hops to learn where one file is, and the two vacation
    questions would still contradict each other."""
    doc = clean_manifest(scratch)
    doc["destinations"]["opendox_code_alias"] = dict(
        doc["destinations"]["opendox_code"])
    _re_destine(doc, "beta.py", to="opendox_code",
                to_path="src/opendox/relay.py")
    alpha = row_named(doc, "alpha.py")
    alpha["re_destined"] = {
        "from": alpha["destination"], "from_path": alpha["destination_path"],
        "to": "openxdox_code", "to_path": "src/openxdox/alpha.py",
        "ruling": RULING_CITATION,
    }
    # `alpha.py` vacates `opendox_code:<its path>`; `beta.py` lands on it — but
    # spelled with the ALIAS, which the string comparison could not see.
    beta = row_named(doc, "beta.py")
    beta["re_destined"]["to"] = "opendox_code_alias"
    beta["re_destined"]["to_path"] = alpha["destination_path"]
    combined = refuses(scratch, doc, "carve-re-destined-chain")
    assert "AMENDED IN PLACE" in combined, combined


def test_an_unknown_destination_key_still_falls_to_the_vocabulary_refusal(
        scratch: Scratch) -> None:
    """The resolver's own guard, asserted rather than assumed: a key
    `destinations:` does not carry resolves to a 1-TUPLE of the key itself — a
    shape that can never equal a resolved 2-tuple — so two unknown keys never
    compare equal to each other by accident, and `check_vocabulary` keeps its
    own refusal instead of having it pre-empted by a crash here."""
    doc = clean_manifest(scratch)
    row = _re_destine(doc)
    row["re_destined"]["to"] = "opendox_kode"
    row["re_destined"]["from"] = "openxdox_kode"
    row["destination"] = "openxdox_kode"
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_a_re_destination_must_name_the_placement_the_row_made(
        scratch: Scratch) -> None:
    """`from`/`from_path` ARE the row's own `destination`/`destination_path`,
    and the row keeps both unedited. A `from` naming some third leg would ask
    the vacation question of a leg this row never placed anything at."""
    doc = clean_manifest(scratch)
    _re_destine(doc)["re_destined"]["from"] = "opendox_code"
    refuses(scratch, doc, "carve-disposition-inconsistent")
    doc = clean_manifest(scratch)
    _re_destine(doc)["re_destined"]["from_path"] = "src/openxdox/elsewhere.py"
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "from_path" in combined, combined


def test_a_chain_of_re_destinations_refuses(scratch: Scratch) -> None:
    """RULED Q6, verbatim: "refuses a chain (a row already re-destined is
    AMENDED in place, never re-destined twice, so one row never needs two
    readings)". One row cannot carry two blocks, so a chain is two rows — the
    arrival one creates being the arrival the other moves on — and the pair
    also contradicts each other at that destination, one requiring the file
    present and the other requiring it absent."""
    doc = clean_manifest(scratch)
    _re_destine(doc, "beta.py", to="opendox_code",
                to_path="src/opendox/relay.py")
    alpha = row_named(doc, "alpha.py")
    alpha["re_destined"] = {
        "from": alpha["destination"], "from_path": alpha["destination_path"],
        "to": "openxdox_code", "to_path": "src/openxdox/alpha.py",
        "ruling": RULING_CITATION,
    }
    # `alpha.py` now vacates `opendox_code:src/opendox/alpha.py`; point
    # `beta.py`'s re-destination AT that vacated arrival to build the chain.
    row_named(doc, "beta.py")["re_destined"]["to_path"] = \
        alpha["destination_path"]
    combined = refuses(scratch, doc, "carve-re-destined-chain")
    assert "AMENDED IN PLACE" in combined, combined


def test_a_re_destination_to_a_destination_the_manifest_does_not_declare_refuses(
        scratch: Scratch) -> None:
    """The same membership test a row's own `destination` gets, at both ends:
    one typo otherwise re-homes a file to a repository nobody declared, and an
    unknown `from` is a vacation nobody can check."""
    for key in ("to", "from"):
        doc = clean_manifest(scratch)
        _re_destine(doc)["re_destined"][key] = "opendox_kode"
        refuses(scratch, doc, "carve-vocabulary-unknown")


def test_a_malformed_re_destined_refuses(scratch: Scratch) -> None:
    """Shape, in check 1: a CLOSED mapping of five required strings and one
    optional prose note. The two paths go through the same canonical-relative
    predicate `destination_path` does — `to_path` is joined onto a leg's mount
    and `from_path` is the path the arrival verifier requires ABSENT, and
    either question asked about a path outside the tree is a question about
    the wrong file."""
    cases: list[Any] = [
        "opendox_code",                      # not a mapping at all
        {"from": "openxdox_code", "from_path": "src/openxdox/beta.py",
         "to": "opendox_code", "to_path": "src/opendox/beta.py",
         "ruling": RULING_CITATION, "why": "an unknown key"},
    ]
    for value in cases:
        doc = clean_manifest(scratch)
        row_named(doc, "beta.py")["re_destined"] = value
        refuses(scratch, doc, "carve-shape-invalid")
    for key in ("from", "from_path", "to", "to_path"):
        for value in (None, "", 7, ["x"]):
            doc = clean_manifest(scratch)
            row = _re_destine(doc)
            if value is None:
                del row["re_destined"][key]
            else:
                row["re_destined"][key] = value
            refuses(scratch, doc, "carve-shape-invalid")
    for path in ("/etc/passwd", "../../escape.py", "src/./beta.py",
                 "src/../../beta.py", "src\\beta.py"):
        doc = clean_manifest(scratch)
        _re_destine(doc, to_path=path)
        refuses(scratch, doc, "carve-shape-invalid")
    doc = clean_manifest(scratch)
    _re_destine(doc, note="   ")
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_re_destination_may_carry_a_note(scratch: Scratch) -> None:
    """`note:` is the one optional key, prose, exactly as an `edits[]` entry's
    is — the place the reason for a re-homed file is written down beside the
    citation that ordered it."""
    doc = clean_manifest(scratch)
    _re_destine(doc, note="the census says this bundle file's tests belong at "
                          "the other leg (§ 1.2(d))")
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_another_row_may_move_into_the_path_a_re_destination_vacated(
        scratch: Scratch) -> None:
    """Check 4 keys the duplicate-arrival map on the EFFECTIVE arrival. Keyed
    on the original, a row re-destined AWAY from a path would go on reserving
    it and this lawful refill — one row leaving and another arriving, which is
    two rows agreeing — would refuse as a duplicate."""
    doc = clean_manifest(scratch)
    beta = row_named(doc, "beta.py")
    vacated = beta["destination_path"]
    _re_destine(doc)
    gamma = row_named(doc, "gamma.py")
    gamma["destination"] = "openxdox_code"
    gamma["destination_path"] = vacated
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_a_re_destination_onto_an_occupied_path_refuses(
        scratch: Scratch) -> None:
    """The other direction of the same keying: a re-destined row landing where
    another row already arrives is the overwrite `carve-file-duplicated`
    exists to refuse, and keyed on the original arrivals it would have passed
    in silence."""
    doc = clean_manifest(scratch)
    alpha = row_named(doc, "alpha.py")
    _re_destine(doc, to=alpha["destination"],
                to_path=alpha["destination_path"])
    refuses(scratch, doc, "carve-file-duplicated")


def test_a_re_destination_moves_no_source_path(scratch: Scratch) -> None:
    """The surface walk is untouched by the field. The row's `source_path` is
    still the file openxFactory carries, still in exactly one row, and still
    counted in the surface — a re-destination is a claim about the
    DESTINATION, and a floor that let it move a source path would let a file
    leave the surface by being re-addressed."""
    doc = clean_manifest(scratch)
    _re_destine(doc)
    summary = _summary(scratch, doc)
    assert summary["surface"] == _summary(scratch, clean_manifest(scratch))[
        "surface"], summary


def test_the_grammar_extension_names_the_ruling_and_why_not_a_re_cut(
        scratch: Scratch) -> None:
    """The disclosure, asserted in the file that carries it: the ruling, the
    field, and the argument that a post-shed manifest cannot be re-cut into
    one carrying moved rows at all — which is why a ruled mis-placement is
    DECLARED."""
    doc = MODULE.__doc__ or ""
    assert "re_destined" in doc, doc
    assert "RULED Q6" in doc, doc
    assert "5648044785" in doc, doc
    assert "WHY NOT A RE-CUT" in doc, doc
    assert MODULE.RE_DESTINED_KEYS == frozenset(
        {"from", "from_path", "to", "to_path", "ruling", "note"})


def test_the_human_readable_line_prints_the_zero_state_too(
        scratch: Scratch) -> None:
    """`test_the_summary_counts_the_re_destined_rows` already reads `0` from
    `--json`. The human line is a separate promise (the comment two lines
    above the print statement: "whether the number is 0 or 48") and had its
    own gap: a ternary printed the `RE-DESTINED by ruling` clause only when
    the count was truthy, so the landed manifest's own zero state — the one
    every reader hits first, until S8 lands a row — was the one count this
    line never showed (Copilot review, PR #1011)."""
    doc = clean_manifest(scratch)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "0 row(s) RE-DESTINED by ruling (RULED Q6)" in done.stdout, \
        done.stdout


def test_a_re_destined_row_may_not_be_also_replicated_at_its_new_destination(
        scratch: Scratch) -> None:
    """The same refusal `test_a_row_may_not_be_also_replicated_at_its_own_
    destination` proves, at the EFFECTIVE destination rather than the raw
    one: a row re-destined to `opendox_code` that also lists `opendox_code`
    in `also_replicated_to` used to pass here (the check compared against the
    row's own `destination`, still `openxdox_code`), and
    `verify-carve-arrival.py` would then silently drop the now-redundant
    replica at the one place the row actually arrives today — two tools
    reading one row two ways. Comparing against `effective_arrival(row)`
    refuses it at the gate that runs first (Copilot review, PR #1011)."""
    doc = clean_manifest(scratch)
    row = _re_destine(doc)  # beta.py, openxdox_code -> opendox_code
    row["also_replicated_to"] = ["opendox_code"]
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "also_replicated_to" in combined, combined


def test_a_re_destined_row_may_still_be_also_replicated_at_its_original_destination(
        scratch: Scratch) -> None:
    """The row's ORIGINAL `destination` is not a forbidden replica key merely
    because a ruling has since moved the row away from it — only the
    EFFECTIVE destination is. `beta.py` moves to `openxdox_code` at the carve
    and is re-destined to `opendox_code`; a replica declared at
    `openxdox_code` names a DIFFERENT destination than the one the row
    arrives at today, so it is not the self-replica the check refuses."""
    doc = clean_manifest(scratch)
    original_destination = row_named(doc, "beta.py")["destination"]
    row = _re_destine(doc)  # beta.py, openxdox_code -> opendox_code
    row["also_replicated_to"] = [original_destination]
    summary = _summary(scratch, doc)
    assert summary["re_destined"] == 1, summary


def test_a_row_may_not_be_also_replicated_at_an_ALIAS_of_its_own_destination(
        scratch: Scratch) -> None:
    """THE SAME RESOLVED-IDENTITY READING, ONE CHECK OVER (Copilot review of
    PR #1025, accurate).

    The self-replica refusal above compared `also_replicated_to`'s entries
    against `effective_arrival(row)` AS RAW LABELS, while this slice made
    `verify-carve-arrival.py::also_replicated_rows` resolve both sides. A row
    listing an ALIAS of the destination it arrives at therefore passed HERE and
    was DROPPED THERE — the manifest claiming a replica no run can verify and
    `--replica-at` cannot declare, which is the self-replica refusal bypassed by
    spelling. A `destinations:` key is a LABEL and `check_shape` admits two keys
    for one `{repository, leg}` body on purpose, so the two tools must agree on
    what "the same destination" means or the asymmetry is the finding.
    """
    doc = clean_manifest(scratch)
    doc["destinations"]["openxdox_code_alias"] = dict(
        doc["destinations"]["openxdox_code"])
    row = row_named(doc, "beta.py")
    assert row["destination"] == "openxdox_code", row
    row["also_replicated_to"] = ["openxdox_code_alias"]
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "also_replicated_to" in combined, combined
    assert "openxdox_code_alias" in combined, combined
    assert "ONE REAL DESTINATION" in combined, combined


def test_an_also_replicated_alias_naming_a_DIFFERENT_leg_stays_lawful(
        scratch: Scratch) -> None:
    """The discriminator, so the check above is not a blanket refusal of every
    alias: two keys whose `{repository, leg}` bodies DIFFER are two real
    destinations, and a replica declared at one of them is somewhere ELSE — the
    thing `also_replicated_to:` is for."""
    doc = clean_manifest(scratch)
    doc["destinations"]["openxdox_root"] = {
        "repository": "opensoft/openXdox-code", "leg": "assembly"}
    row = row_named(doc, "beta.py")
    assert row["destination"] == "openxdox_code", row
    row["also_replicated_to"] = ["openxdox_root"]
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


# --------------------------------------------------------------------------
# RULED 5656343213 — the `retired:` row form
#
# Brett Heap, 2026-09-13, by interactive multi-choice, on the question slice
# S8's author put in `#656` comment `5650335573` § 2. The FOURTH grammar
# extension and the SECOND about PLACEMENT — the one Q6 above could not be
# stretched to cover, because Q6 moves an arrival BETWEEN two legs and what S8
# measured has no leg to move it to. Every case below is a generated manifest
# and a real tree; the landed manifest — which carried the form and used it
# NOWHERE as PR #1032 landed it, and carries TWO retired rows since its first
# use (RULED 5656343213's own act, PR #1043) — is asserted separately in the
# § 8.2 seat.
# --------------------------------------------------------------------------

RETIREMENT_CITATION = ("`#656` comment 5656343213 (RULED, Brett Heap "
                       "2026-09-13)")

#: The fixture's one `not_moved` row, by `source_path`. A retirement's
#: `surface:` must be one, and the generator's `delta.py` is it — which is
#: also the shape of the real act: `views/intent-feed.js`, RULED OQ-F
#: `not_moved`, so the manifest's own declaration says it arrived nowhere.
RETIRED_SURFACE = "scripts/pkg/delta.py"


def _retire(doc: dict[str, Any], name: str = "beta.py",
            surface: str = RETIRED_SURFACE, **override: Any) -> dict[str, Any]:
    """Retire a generated row's EFFECTIVE arrival, and return the row.

    `at`/`at_path` are READ OFF THE ROW rather than typed, for `_re_destine`'s
    reason exactly — and read through `re_destined:` where one is present,
    because that is what "EFFECTIVE" means and a fixture that took the raw
    destination could not tell the composed case from the plain one.
    `beta.py` by default: the `moved_with_declared_edit` row, so the cases
    below retire a row that also carries `edits:` — which is the real act's
    shape, the three retired suites being test files with declared lines.
    """
    row = row_named(doc, name)
    re_destined = row.get("re_destined")
    if isinstance(re_destined, dict):
        at, at_path = re_destined["to"], re_destined["to_path"]
    else:
        at, at_path = row["destination"], row["destination_path"]
    block: dict[str, Any] = {
        "at": at,
        "at_path": at_path,
        "ruling": RETIREMENT_CITATION,
        "surface": surface,
    }
    block.update(override)
    row["retired"] = block
    return row


def test_a_moved_row_may_be_retired_by_a_ruling(scratch: Scratch) -> None:
    """The form itself: `beta.py` arrived at `openxdox_code` and a ruling has
    since DELETED that arrival, because the surface it needed is a `not_moved`
    row — which is the three intent-feed suites' shape in miniature."""
    doc = clean_manifest(scratch)
    _retire(doc)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout
    assert "1 row(s) RETIRED by ruling" in done.stdout, done.stdout


def test_a_verbatim_row_may_be_retired_and_keeps_every_source_side_answer(
        scratch: Scratch) -> None:
    """The field is on BOTH moved dispositions, and it moves NOTHING at the
    source: the same blobs are recomputed with the retirement as without it,
    the disposition counts are the same, and the surface is the same. A
    `sha256` is a claim about the SOURCE blob at the carve commit and a
    retirement is a fact about a DESTINATION."""
    before = _summary(scratch, clean_manifest(scratch))
    doc = clean_manifest(scratch)
    row = _retire(doc, "alpha.py")
    after = _summary(scratch, doc)
    assert row["disposition"] == "moved_verbatim", row
    assert after["digests_recomputed"] == before["digests_recomputed"], after
    assert after["dispositions"] == before["dispositions"], after
    assert after["surface"] == before["surface"], after
    assert after["carve_commit"] == before["carve_commit"], after


def test_a_retired_rows_digest_still_binds(scratch: Scratch) -> None:
    """"Every source-side question" as running code rather than as prose. A
    retirement deletes a file at a LEG; the row still says which openxFactory
    blob left, and a manifest that drifted from that blob still refuses."""
    doc = clean_manifest(scratch)
    row = _retire(doc)
    row["sha256"] = "0" * 64
    refuses(scratch, doc, "carve-digest-mismatch")


def test_the_summary_counts_the_retired_rows(scratch: Scratch) -> None:
    """Counted in `--json` and printed on the human line — and ZERO is a state
    the log records too, which is what a manifest carrying no retirement reads
    as. THE ZERO HERE IS THE FIXTURE'S, not the landed document's: since RULED
    5656343213's first use (PR #1043) the landed manifest reads 2, the two
    intent-feed suites, and it will never read 3: the ruling's third suite
    KEEPS ITS ROW — the file goes on arriving — and only the ending replay
    inside it is declared, as an ordinary edit on that row's `edits[]`. Both
    numbers matter, and this case is about the counter rather than about
    either one of them."""
    clean = _summary(scratch, clean_manifest(scratch))
    assert clean["retired"] == 0, clean
    doc = clean_manifest(scratch)
    _retire(doc)
    _retire(doc, "gamma.py")
    assert _summary(scratch, doc)["retired"] == 2


def test_a_retirement_is_counted_apart_from_a_re_destination(
        scratch: Scratch) -> None:
    """One row may be BOTH — re-destined by Q6, then retired — and folding
    either count into the other would report one row twice and hide the one
    fact about this document a reader cannot get anywhere else: how many
    arrivals the floor no longer asks for."""
    doc = clean_manifest(scratch)
    _re_destine(doc)                      # beta.py, openxdox_code -> opendox
    _retire(doc)                          # ... and then retired, at the NEW leg
    summary = _summary(scratch, doc)
    assert summary["re_destined"] == 1, summary
    assert summary["retired"] == 1, summary
    assert summary["dispositions"]["moved_with_declared_edit"] == 1, summary


def test_a_half_written_block_is_not_counted_as_a_retirement(
        scratch: Scratch) -> None:
    """The count is taken off `retired_at`, not off the raw key, so a block
    this file is about to REFUSE is never first reported as a retirement —
    and the refusal is the shape one, not a silent zero."""
    doc = clean_manifest(scratch)
    row = _retire(doc)
    del row["retired"]["at_path"]
    refuses(scratch, doc, "carve-shape-invalid")


def test_retired_on_a_not_moved_row_refuses(scratch: Scratch) -> None:
    """A row that placed nothing has no arrival to RETIRE — under EVERY
    `not_moved` reason, the replica one included: a replica's copies are
    placed by the leg (RULED OQ-C), so retiring one would un-place something
    this manifest never placed."""
    for make_replica in (False, True):
        doc = clean_manifest(scratch)
        row = _as_replica(doc) if make_replica else row_named(doc, "delta.py")
        row["retired"] = {
            "at": "opendox_code", "at_path": "src/opendox/delta.py",
            "ruling": RETIREMENT_CITATION, "surface": RETIRED_SURFACE,
        }
        combined = refuses(scratch, doc, "carve-retired-not-moved")
        assert "retired" in combined, combined


def test_a_retirement_with_no_ruling_refuses(scratch: Scratch) -> None:
    """Q6's scope answer, extended by 5656343213 to this form: the citation is
    the one absence that is a GOVERNANCE defect rather than a typo, so it gets
    its own code. Without it the field is a quiet way to delete an arrived
    file after the carve is closed, which is the one use the ruling refused."""
    for value in (None, "", "   ", 5656343213, ["#656"]):
        doc = clean_manifest(scratch)
        row = _retire(doc)
        if value is None:
            del row["retired"]["ruling"]
        else:
            row["retired"]["ruling"] = value
        refuses(scratch, doc, "carve-retired-unruled")


def test_the_retirement_citations_form_is_not_constrained(
        scratch: Scratch) -> None:
    """PRESENT is what the ruling asked for, on `re_destined:`' own reasoning:
    a pattern here would refuse a legitimate citation and teach the author to
    write whatever the pattern wanted."""
    for citation in ("5656343213", "#656 comment 5656343213",
                     "https://github.com/opensoft/openxFactory/pull/1011"):
        doc = clean_manifest(scratch)
        _retire(doc, ruling=citation)
        scratch.write(doc)
        done = run(scratch)
        assert done.returncode == 0, done.stdout + done.stderr


def test_a_retirement_must_name_the_arrival_the_row_made(
        scratch: Scratch) -> None:
    """`at`/`at_path` ARE the row's effective arrival, and the row keeps every
    placement field unedited. An `at` naming some third leg would ask a leg
    this row never placed anything at to prove an absence it was always going
    to have."""
    doc = clean_manifest(scratch)
    _retire(doc)["retired"]["at"] = "opendox_code"
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "retired.at" in combined, combined
    doc = clean_manifest(scratch)
    _retire(doc)["retired"]["at_path"] = "src/openxdox/elsewhere.py"
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "at_path" in combined, combined


def test_a_retirement_is_pinned_to_the_effective_arrival_and_not_the_raw_one(
        scratch: Scratch) -> None:
    """The two acts compose in ONE order — move, then retire — and this is the
    check that says so. A row re-destined by Q6 has its file at
    `re_destined.to:to_path`; a retirement pinned to the row's ORIGINAL
    `destination` would leave the real copy standing at the leg the ruling
    actually reached while the arrival verifier checked an absence at a leg
    that vacated the path long before."""
    doc = clean_manifest(scratch)
    row = _re_destine(doc)            # beta.py: openxdox_code -> opendox_code
    _retire(doc)                      # reads the re-destination: opendox_code
    assert row["retired"]["at"] == "opendox_code", row
    assert row["retired"]["at_path"] == row["re_destined"]["to_path"], row
    summary = _summary(scratch, doc)
    assert summary["retired"] == 1, summary

    doc = clean_manifest(scratch)
    row = _re_destine(doc)
    _retire(doc)
    row["retired"]["at"] = row["destination"]            # the RAW arrival
    row["retired"]["at_path"] = row["destination_path"]
    combined = refuses(scratch, doc, "carve-disposition-inconsistent")
    assert "EFFECTIVE arrival" in combined, combined


def test_a_retirement_at_a_destination_the_manifest_does_not_declare_refuses(
        scratch: Scratch) -> None:
    """The same membership test a row's own `destination` gets. A key nobody
    declared is a retirement nobody can check — every leg satisfies an absence
    at a repository that never existed."""
    doc = clean_manifest(scratch)
    _retire(doc)["retired"]["at"] = "openxdox_kode"
    refuses(scratch, doc, "carve-vocabulary-unknown")


def test_a_retirement_must_cite_a_surface_this_manifest_says_is_gone(
        scratch: Scratch) -> None:
    """The gate that makes the form a FLOOR rather than a licence to delete an
    arrived file, in TWO of its three arms and under one code.

    A surface that is a MOVED row is LIVE at a leg — a suite driving a surface
    that still exists is not retired for the reason this form serves. A
    surface in NO row is one this document says nothing about, and "this
    manifest cannot say" is not "gone" in a floor that refuses by default. The
    message names which arm was hit, so a reader is never left guessing. (The
    third arm — a `not_moved` row that is a REPLICA — is the test below.)
    """
    doc = clean_manifest(scratch)
    _retire(doc, surface="scripts/pkg/alpha.py")     # a MOVED row
    combined = refuses(scratch, doc, "carve-retired-surface-live")
    assert "LIVE at a" in combined, combined

    doc = clean_manifest(scratch)
    _retire(doc, surface="scripts/pkg/nowhere.py")   # no row at all
    combined = refuses(scratch, doc, "carve-retired-surface-live")
    assert "names no row of this manifest" in combined, combined


def test_a_replicated_surface_is_not_a_surface_this_manifest_says_is_gone(
        scratch: Scratch) -> None:
    """THE THIRD ARM, and the one a reading of the disposition alone misses
    (Copilot review of PR #1032, the one posted thread).

    `not_moved` is not one claim. Four of its five reasons say the file is
    ABSENT at the legs — it stayed here, or it is nowhere at all — and
    `replicated_at_destination` says the opposite: RULED OQ-C has EVERY
    destination place its own copy, `verify-carve-arrival.py` admits those
    copies through `--replica-at`, and RULED Q-L7 (a) even lets the row
    declare the `edits:` they carry. A retirement citing such a surface would
    rest its whole claim — "the surface this arrived file needed is at no leg"
    — on a row that says the surface is at every leg.

    Before the fix this document VALIDATED: the check tested
    `disposition == "not_moved"` and nothing else, so the one reason that
    contradicts the claim satisfied it. The assertion below is that it does
    not, and that the message says WHY rather than repeating the disposition.
    """
    doc = clean_manifest(scratch)
    _as_replica(doc)                                 # delta.py, the surface
    _retire(doc)                                     # cites delta.py
    combined = refuses(scratch, doc, "carve-retired-surface-live")
    assert "replicated_at_destination" in combined, combined
    assert "LIVE at every leg that placed one" in combined, combined

    # …and the SAME row under any other `not_moved` reason is still lawful, so
    # the exclusion is one reason and not a retreat from the whole form.
    doc = clean_manifest(scratch)
    _retire(doc)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 row(s) RETIRED by ruling" in done.stdout, done.stdout


def test_a_malformed_retired_refuses(scratch: Scratch) -> None:
    """Shape, in check 1: a CLOSED mapping of four required strings and one
    optional prose note. BOTH paths go through the same canonical-relative
    predicate `destination_path` does — `at_path` is the path the arrival
    verifier requires ABSENT, and `surface:` is looked up as a `source_path`
    of this manifest, so a value that could not be one is a typo worth naming
    here rather than a "no such row" two checks later."""
    cases: list[Any] = [
        "opendox_code",                      # not a mapping at all
        {"at": "openxdox_code", "at_path": "src/openxdox/beta.py",
         "ruling": RETIREMENT_CITATION, "surface": RETIRED_SURFACE,
         "why": "an unknown key"},
    ]
    for value in cases:
        doc = clean_manifest(scratch)
        row_named(doc, "beta.py")["retired"] = value
        refuses(scratch, doc, "carve-shape-invalid")
    for key in ("at", "at_path", "surface"):
        for value in (None, "", 7, ["x"]):
            doc = clean_manifest(scratch)
            row = _retire(doc)
            if value is None:
                del row["retired"][key]
            else:
                row["retired"][key] = value
            refuses(scratch, doc, "carve-shape-invalid")
    for path in ("/etc/passwd", "../../escape.py", "src/./beta.py",
                 "src/../../beta.py", "src\\beta.py"):
        for key in ("at_path", "surface"):
            doc = clean_manifest(scratch)
            _retire(doc)["retired"][key] = path
            refuses(scratch, doc, "carve-shape-invalid")
    doc = clean_manifest(scratch)
    _retire(doc, note="   ")
    refuses(scratch, doc, "carve-shape-invalid")


def test_a_retirement_may_carry_a_note(scratch: Scratch) -> None:
    """`note:` is the one optional key, prose, exactly as an `edits[]` entry's
    and a `re_destined:`' are — the place the reason a suite is retired is
    written down beside the citation that ordered it."""
    doc = clean_manifest(scratch)
    _retire(doc, note="RULED OQ-F kept the surface at openxFactory; S2 "
                      "replaced the one openDox has")
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_another_row_may_move_into_the_path_a_retirement_emptied(
        scratch: Scratch) -> None:
    """Check 4 stops RESERVING a retired row's arrival. That path is empty
    once the act lands, and another row may lawfully move into it — the same
    reading, and the same reason, that keyed the duplicate-arrival map on the
    EFFECTIVE arrival for Q6. Keyed on the retired row too, this lawful refill
    would refuse as a duplicate while the tree carries exactly one file."""
    doc = clean_manifest(scratch)
    beta = row_named(doc, "beta.py")
    emptied = beta["destination_path"]
    _retire(doc)
    gamma = row_named(doc, "gamma.py")
    gamma["destination"] = beta["destination"]
    gamma["destination_path"] = emptied
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr


def test_two_retired_rows_at_one_path_do_not_collide(
        scratch: Scratch) -> None:
    """Neither of them is there. Two rows retired at one path is not an
    overwrite, because the act each declares is a DELETION — and a map that
    still held both would refuse a document describing an empty path."""
    doc = clean_manifest(scratch)
    beta = row_named(doc, "beta.py")
    gamma = row_named(doc, "gamma.py")
    gamma["destination"] = beta["destination"]
    gamma["destination_path"] = beta["destination_path"]
    _retire(doc, "beta.py")
    _retire(doc, "gamma.py")
    summary = _summary(scratch, doc)
    assert summary["retired"] == 2, summary


def test_a_retirement_onto_a_live_duplicate_still_refuses(
        scratch: Scratch) -> None:
    """The other direction of the same keying, kept: a retired row stops
    reserving its path, but the rows that are NOT retired still collide there
    exactly as they always did. `carve-file-duplicated` is unweakened by this
    amendment."""
    doc = clean_manifest(scratch)
    alpha = row_named(doc, "alpha.py")
    gamma = row_named(doc, "gamma.py")
    gamma["destination"] = alpha["destination"]
    gamma["destination_path"] = alpha["destination_path"]
    _retire(doc, "beta.py")
    refuses(scratch, doc, "carve-file-duplicated")


def test_a_retirement_moves_no_source_path(scratch: Scratch) -> None:
    """The surface walk is untouched by the field, exactly as it is by
    `re_destined:`. The row's `source_path` is still the file openxFactory
    carries, still in exactly one row, and still counted — a floor that let a
    retirement move a source path would let a file leave the surface by being
    deleted somewhere else."""
    doc = clean_manifest(scratch)
    _retire(doc)
    summary = _summary(scratch, doc)
    assert summary["surface"] == _summary(scratch, clean_manifest(scratch))[
        "surface"], summary


def test_a_retired_row_is_still_shed_at_the_source_under_post_shed(
        scratch: Scratch) -> None:
    """The post-shed arm asks a retired row exactly what it asks every other
    moved row: the SOURCE path must be absent here. `shed()` is defined below
    this block — the call resolves at run time — and it is the right helper
    rather than a hand-written deletion because it derives the paths from the
    document, so a retired row that stopped being shed would show up here."""
    doc = clean_manifest(scratch)
    _retire(doc)
    doc["phase"] = MODULE.PHASE_POST_SHED
    shed(scratch, doc)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 row(s) RETIRED by ruling" in done.stdout, done.stdout
    assert "shed row(s) absent at source as declared" in done.stdout, \
        done.stdout


def test_the_grammar_extension_names_the_ruling_and_what_it_does_not_move(
        scratch: Scratch) -> None:
    """The disclosure, asserted in the file that carries it: the ruling, the
    field, and the sentence that separates this form from Q6's — a retirement
    is a DESTINATION-side fact and every source-side question is unmoved."""
    doc = MODULE.__doc__ or ""
    assert "retired" in doc, doc
    assert "5656343213" in doc, doc
    assert "EVERY\nSOURCE-SIDE QUESTION" in doc or \
        "SOURCE-SIDE QUESTION" in doc, doc
    assert MODULE.RETIRED_KEYS == frozenset(
        {"at", "at_path", "ruling", "surface", "note"})


def test_the_human_line_prints_the_retirement_zero_state_too(
        scratch: Scratch) -> None:
    """`test_the_summary_counts_the_retired_rows` already reads `0` from
    `--json`. The human line is a separate promise, and it is written
    UNCONDITIONAL from the start rather than repaired later: the `re_destined`
    clause had to be fixed in review on PR #1011 because a ternary suppressed
    it, making the landed manifest's own state the one count that line never
    showed. Zero is the state this form LANDED in (PR #1032); the landed
    document reads 2 since its first use (PR #1043), and this case asks the
    GENERATED one, where zero is the baseline every other case in this section
    starts from."""
    doc = clean_manifest(scratch)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "0 row(s) RETIRED by ruling (RULED 5656343213)" in done.stdout, \
        done.stdout


def test_carved_reach_refuses_a_retired_row_by_name(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """The THIRD reader of the form, and the one whose failure would be
    silent. `carved_reach.source()` can compute a perfectly well-formed path
    for a retired row — the row keeps every field the carve wrote — and that
    path names a file `verify-carve-arrival.py` has just finished proving
    ABSENT. It refuses instead, with `CarveRowRetired`; `module()` and
    `shed_relpath()` refuse through it; and `sources_under()` OMITS the row,
    because one row that is nowhere must not take a whole compositor sweep
    down with it.

    The rows are a STUB rather than the landed manifest, for the reason every
    other case in this file builds its own document: this case needs BOTH arms
    in ONE sweep — a live row and a retired one — and control over which is
    which, which no real document owes it. Since RULED 5656343213's first use
    (PR #1043) the landed manifest DOES carry two retired rows, and they are
    driven through this same reader by
    `test_carved_reach_refuses_the_two_landed_retired_rows` in the § 8.2 seat:
    this case holds the shape, that one holds the act.
    """
    import carved_reach

    rows = {
        "scripts/pkg/live.py": {
            "source_path": "scripts/pkg/live.py",
            "disposition": "moved_verbatim",
            "destination": "opendox_code",
            "destination_path": "src/opendox/live.py"},
        "scripts/pkg/retired.py": {
            "source_path": "scripts/pkg/retired.py",
            "disposition": "moved_with_declared_edit",
            "destination": "opendox_code",
            "destination_path": "src/opendox/retired.py",
            "retired": {"at": "opendox_code",
                        "at_path": "src/opendox/retired.py",
                        "ruling": RETIREMENT_CITATION,
                        "surface": RETIRED_SURFACE}},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)

    with pytest.raises(carved_reach.CarveRowRetired) as caught:
        carved_reach.source("scripts/pkg/retired.py")
    assert "5656343213" in str(caught.value), caught.value
    assert RETIRED_SURFACE in str(caught.value), caught.value
    # A SUBCLASS, so a caller that already handles "at no destination" needs
    # no change the day a row is first retired.
    assert isinstance(caught.value, carved_reach.ShedModuleHasNoDestination)

    for call in (carved_reach.module, carved_reach.shed_relpath):
        with pytest.raises(carved_reach.CarveRowRetired):
            call("scripts/pkg/retired.py")

    swept = carved_reach.sources_under("scripts/pkg/")
    assert list(swept) == ["scripts/pkg/live.py"], swept


def test_a_retirement_on_a_not_moved_row_hides_nothing_from_a_sweep(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """A SWEEP AND `source()` MUST AGREE ABOUT THE SAME ROW (Copilot review of
    PR #1032, round 6).

    `retired:` on a `not_moved` row is a document `validate-carve-manifest.py`
    refuses — `carve-retired-not-moved`, because a row that placed nothing has
    no arrival to retire — and `carved_reach` is imported by consumers that
    never run that validator. `source()` has always read a `not_moved` row
    correctly: it resolves HERE, unconditionally, before any retirement is
    read. `sources_under()` omitted on the retirement alone, so for one
    malformed row the two disagreed, and the sweep silently dropped a file
    that is RETAINED in this tree — the one direction a fail-closed reader
    must never fail in, since a caller walking a tree cannot see what it was
    not given.

    The moved row beside it is the control: its retirement IS honoured, so
    what the assertion below measures is the disposition test and not a
    disabled omission.
    """
    import carved_reach

    rows = {
        "scripts/pkg/stays.py": {
            "source_path": "scripts/pkg/stays.py",
            "disposition": "not_moved",
            "reason": "replicated_at_destination",
            "retired": {"at": "opendox_code",
                        "at_path": "src/opendox/stays.py",
                        "ruling": RETIREMENT_CITATION,
                        "surface": RETIRED_SURFACE}},
        "scripts/pkg/gone.py": {
            "source_path": "scripts/pkg/gone.py",
            "disposition": "moved_with_declared_edit",
            "destination": "opendox_code",
            "destination_path": "src/opendox/gone.py",
            "retired": {"at": "opendox_code",
                        "at_path": "src/opendox/gone.py",
                        "ruling": RETIREMENT_CITATION,
                        "surface": RETIRED_SURFACE}},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)

    swept = carved_reach.sources_under("scripts/pkg/")
    assert list(swept) == ["scripts/pkg/stays.py"], swept
    assert swept["scripts/pkg/stays.py"] == (
        carved_reach.REPO_ROOT / "scripts/pkg/stays.py")
    # …and it is the SAME answer `source()` gives, which is the agreement this
    # case exists to hold.
    assert carved_reach.source("scripts/pkg/stays.py") == \
        swept["scripts/pkg/stays.py"]
    with pytest.raises(carved_reach.CarveRowRetired):
        carved_reach.source("scripts/pkg/gone.py")


def test_the_exact_commit_resolver_answers_for_a_retired_row_on_purpose(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`shed_commit_object()` does NOT refuse a retired row, and the
    divergence from `source()` is a decision this test holds (Copilot review
    of PR #1032 asked for the guard; the answer is here rather than in a
    comment nobody runs).

    The two functions answer two different questions. `source()` asks where a
    file is in THE WORKING TREE — one tree, the one that exists now — so a row
    a ruling has deleted has no answer and refusing is the only honest one.
    This one asks where a row's bytes are AT A NAMED COMMIT, through the leg
    THAT COMMIT pins, and a retirement is an EVENT: every commit from before
    the leg's deletion pins a leg that still carries the file, and the
    `retired:` block is read from the WORKING TREE's manifest and says nothing
    about when the deletion landed. A guard here would apply today's
    retirement to every commit ever asked about and would break the property
    `hermes_runtime_validation/release.py` is built on — verifying an older
    commit reads the leg that commit pinned.

    At a commit whose pinned leg no longer has the file, the answer is a path
    with no blob, and the CALLER's own absence finding stands: the release
    inventory reports the member VANISHED, `resolve_git_object` raises. That
    is why reporting, not deciding, is this resolver's job.
    """
    import carved_reach

    leg = tmp_path / "openDox" / "code"
    # An object store at EVERY level of the mount: the walk is one
    # `rev-parse <revision>:<segment>` per gitlink (`openDox`, then `code`),
    # and it refuses `CarveReachUnavailable` at the first level that is not
    # materialized — which is one of the THREE refusals this function keeps
    # (`#1048` added the other two) and this case must not be mistaken for.
    (leg / ".git").mkdir(parents=True)
    (tmp_path / "openDox" / ".git").mkdir(exist_ok=True)
    rows = {
        "scripts/pkg/retired.py": {
            "source_path": "scripts/pkg/retired.py",
            "disposition": "moved_verbatim",
            "destination": "opendox_code",
            "destination_path": "src/opendox/retired.py",
            "retired": {"at": "opendox_code",
                        "at_path": "src/opendox/retired.py",
                        "ruling": RETIREMENT_CITATION,
                        "surface": RETIRED_SURFACE}},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    monkeypatch.setattr(carved_reach, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        dict(carved_reach.MOUNTS, opendox_code=leg))
    pinned = "b" * 40
    monkeypatch.setattr(carved_reach, "_git_object_id",
                        lambda repo, revision, path: pinned)
    # …and the STORE-COMPLETENESS probe `#1048` added beside it. The two
    # `.git` entries above are bare directories, not repositories, so the real
    # `cat-file -e <gitlink>^{commit}` answers no and the walk would refuse
    # `CarveReachUnavailable` for an INCOMPLETE STORE — one more thing this
    # case must not be mistaken for. `#1048`'s OTHER new refusal, "the tree
    # this gitlink would be recorded in could not be READ", is already out of
    # the walk's way and needs no stub of its own: it is reached only where
    # `_git_object_id` answers `None`, and the stub above never does.
    # Stubbed for exactly the reason `_git_object_id` above is: what this case
    # measures is the DISPOSITION, and git is not the question.
    monkeypatch.setattr(carved_reach, "_git_ok",
                        lambda repo, *arguments: True)

    located = carved_reach.shed_commit_object("a" * 40,
                                              "scripts/pkg/retired.py")
    assert located == (leg, pinned, "src/opendox/retired.py"), located

    # …while the WORKING-TREE resolver refuses the same row at the same
    # moment, which is the pair this test exists to hold apart.
    with pytest.raises(carved_reach.CarveRowRetired):
        carved_reach.source("scripts/pkg/retired.py")


def test_the_exact_commit_resolver_reads_the_effective_arrival_of_a_re_destined_row(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression, `#1062`. `shed_commit_object()` walked the gitlink chain
    through `MOUNTS[row["destination"]]` and returned `row["destination_path"]`
    — the row's ORIGINAL arrival — instead of `effective_arrival(row)`, the
    same three-line predicate `source()` already reads at line 616. Latent
    while no `re_destined` row named a shed member; this fixture gives it one.

    The row below carved to `openxdox_code` and a ruling (RULED Q6) has since
    re-destined it to `opendox_code` — a DIFFERENT leg entirely, not merely a
    different path at the same one, so a resolver reading the raw
    `destination` walks the WRONG gitlink chain end to end and returns a
    perfectly well-formed answer at a leg the row no longer names, rather than
    raising: the ORIGINAL leg is left materialized here on purpose, so the bug
    does not merely fail loudly, it silently answers wrong.
    """
    import carved_reach

    original_leg = tmp_path / "openXdox" / "code"
    effective_leg = tmp_path / "openDox" / "code"
    for leg in (original_leg, effective_leg):
        (leg / ".git").mkdir(parents=True)
    (tmp_path / "openXdox" / ".git").mkdir()
    (tmp_path / "openDox" / ".git").mkdir()

    rows = {
        "scripts/pkg/moved.py": {
            "source_path": "scripts/pkg/moved.py",
            "disposition": "moved_verbatim",
            "destination": "openxdox_code",
            "destination_path": "src/openxdox/moved.py",
            "re_destined": {
                "from": "openxdox_code",
                "from_path": "src/openxdox/moved.py",
                "to": "opendox_code",
                "to_path": "src/opendox/moved.py",
                "ruling": RULING_CITATION,
            }},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    monkeypatch.setattr(carved_reach, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        dict(carved_reach.MOUNTS,
                             openxdox_code=original_leg,
                             opendox_code=effective_leg))
    pinned = "c" * 40
    monkeypatch.setattr(carved_reach, "_git_object_id",
                        lambda repo, revision, path: pinned)
    # …and the STORE-COMPLETENESS probe `#1048` added beside it, stubbed for
    # exactly the reason `_git_object_id` above is: the four `.git` entries
    # this fixture makes are bare directories and not repositories, so the real
    # `cat-file -e <gitlink>^{commit}` answers no and the walk would refuse
    # `CarveReachUnavailable` for an INCOMPLETE STORE at `openDox` — the WRONG
    # answer to measure a case whose whole question is WHICH LEG the walk
    # reaches, and which leaves the ORIGINAL leg materialized on purpose so
    # that a resolver reading the raw `destination` answers rather than
    # raising. Git is not the question here; the effective arrival is.
    monkeypatch.setattr(carved_reach, "_git_ok",
                        lambda repo, *arguments: True)

    located = carved_reach.shed_commit_object("a" * 40, "scripts/pkg/moved.py")
    assert located == (effective_leg, pinned, "src/opendox/moved.py"), located


def test_a_probe_that_times_out_is_UNAVAILABLE_never_absent(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Round 5 (`#1048`, Copilot on PR #1051, `carved_reach.py:826`): the
    `cat-file`/`ls-tree` probes below `_git_run` are also the paths a partial
    clone or an unreachable promisor remote can HANG rather than fail, and the
    pre-round-5 `_git_run` had no timeout to turn a hang into an answer.
    `scripts/hermes_runtime_validation/content.py:103-116` already bounds its
    own equivalent read at `timeout=30`; this pins the same bound here, and
    that a timeout is read as UNANSWERED — never as the tree's own "no such
    entry", the phantom-absence thesis this whole file exists to refuse, one
    layer lower than every other case in this section.

    `subprocess.run` is mocked to RAISE `subprocess.TimeoutExpired` rather than
    built as a slow real git call: the property under test is that `_git_run`
    catches the timeout and answers `None`, and that the READER built on it
    raises `CarveReachUnavailable` rather than returning `None` as if the tree
    had answered — not that git itself can be made to hang inside a test's own
    time budget. No leg is materialized here at all: the timeout fires on the
    very FIRST probe, the gitlink lookup, which is the earliest a real hang
    could reach.
    """
    import carved_reach

    def timed_out(argv, **kwargs):
        assert kwargs.get("timeout") == 30, (
            "the probe must be bounded at the same 30s "
            "scripts/hermes_runtime_validation/content.py uses")
        raise subprocess.TimeoutExpired(cmd=argv, timeout=30)

    monkeypatch.setattr(subprocess, "run", timed_out)

    # `_git_run` ITSELF: the same failed-probe result an unrunnable git
    # already answers with, so every existing `is None` check above it goes on
    # working unchanged.
    assert carved_reach._git_run(tmp_path, "cat-file", "-e",
                                 "deadbeef^{commit}") is None

    # ...and the READER built on it. `_git_object_id` answers `None` (the
    # mocked `_git_run` behind it timed out), which sends the walk to
    # `_tree_entry_absent` — ALSO built on the timed-out `_git_run` — and ITS
    # `(False, ...)` answer must raise rather than let the walk read a `None`
    # gitlink as "this tree has no such entry".
    rows = {
        "scripts/pkg/timed_out.py": {
            "source_path": "scripts/pkg/timed_out.py",
            "disposition": "moved_verbatim",
            "destination": "opendox_code",
            "destination_path": "src/opendox/timed_out.py"},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    monkeypatch.setattr(carved_reach, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        dict(carved_reach.MOUNTS,
                             opendox_code=tmp_path / "leg"))

    with pytest.raises(carved_reach.CarveReachUnavailable) as caught:
        carved_reach.shed_commit_object("a" * 40, "scripts/pkg/timed_out.py")
    assert "30s" in str(caught.value), (
        "the raised message must name the timeout where it surfaces git's "
        f"own stderr — got {caught.value}")


def test_the_module_loader_reads_the_effective_arrival_of_a_re_destined_row(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression, `#1079`. `module()` read `row["destination_path"]` directly
    — the row's ORIGINAL arrival — instead of `effective_arrival(row)`, the
    same three-line predicate `source()` reads at line 616 and
    `shed_commit_object()` was fixed to read by `#1077`. Latent while no
    `re_destined` row named a module-importable file; this fixture gives it
    one.

    The row below carved to `openxdox_code` and a ruling (RULED Q6) has since
    re-destined it to `opendox_code` — a DIFFERENT leg entirely, so a resolver
    reading the raw `destination_path` derives the dotted name the ORIGINAL
    leg would have made importable (`openxdox.moved`) rather than the one the
    EFFECTIVE leg makes importable (`opendox.moved`). `install()` and the real
    `importlib.import_module` are both stood down here — what this function
    is answerable for is which dotted name it ASKS for, not whether either
    leg is materialized in this checkout.
    """
    import carved_reach

    rows = {
        "scripts/pkg/moved.py": {
            "source_path": "scripts/pkg/moved.py",
            "disposition": "moved_verbatim",
            "destination": "openxdox_code",
            "destination_path": "src/openxdox/moved.py",
            "re_destined": {
                "from": "openxdox_code",
                "from_path": "src/openxdox/moved.py",
                "to": "opendox_code",
                "to_path": "src/opendox/moved.py",
                "ruling": RULING_CITATION,
            }},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    monkeypatch.setattr(carved_reach, "install", lambda **kwargs: None)
    asked: list[str] = []
    sentinel = object()
    monkeypatch.setattr(importlib, "import_module",
                        lambda name: asked.append(name) or sentinel)

    result = carved_reach.module("scripts/pkg/moved.py")
    assert result is sentinel
    assert asked == ["opendox.moved"], asked


def test_the_relative_path_reader_reads_the_effective_arrival_of_a_re_destined_row(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression, `#1079`. `shed_relpath()` walked
    `MOUNTS[row["destination"]]` and returned `row["destination_path"]` — the
    row's ORIGINAL arrival — instead of `effective_arrival(row)`, on the same
    defect `#1077` fixed in `shed_commit_object()`. Latent while no
    `re_destined` row named a file a marker asks the relative path of; this
    fixture gives it one.

    The row below carved to `openxdox_code` and a ruling (RULED Q6) has since
    re-destined it to `opendox_code` — a DIFFERENT leg entirely, not merely a
    different path at the same one, so a resolver reading the raw
    `destination` answers a well-formed relative path under the mount the row
    no longer names, which a marker's `exists()` check against the CORRECT leg
    reads as absent rather than present — the same silent-wrong-answer shape
    `#1077`'s own regression named for `shed_commit_object()`.
    """
    import carved_reach

    original_leg = tmp_path / "openXdox" / "code"
    effective_leg = tmp_path / "openDox" / "code"

    rows = {
        "scripts/pkg/moved.py": {
            "source_path": "scripts/pkg/moved.py",
            "disposition": "moved_verbatim",
            "destination": "openxdox_code",
            "destination_path": "src/openxdox/moved.py",
            "re_destined": {
                "from": "openxdox_code",
                "from_path": "src/openxdox/moved.py",
                "to": "opendox_code",
                "to_path": "src/opendox/moved.py",
                "ruling": RULING_CITATION,
            }},
    }
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    monkeypatch.setattr(carved_reach, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        dict(carved_reach.MOUNTS,
                             openxdox_code=original_leg,
                             opendox_code=effective_leg))

    relpath = carved_reach.shed_relpath("scripts/pkg/moved.py")
    assert relpath == "openDox/code/src/opendox/moved.py", relpath


def _cross_reference_validator():
    """`scripts/validate-ideation-cross-reference.py` as a module, by path."""
    return _load_by_path("validate-ideation-cross-reference.py",
                         "validate_ideation_cross_reference")


def _load_by_path(filename: str, module_name: str):
    """A hyphenated `scripts/` entry point as a module, by path."""
    spec = importlib.util.spec_from_file_location(
        module_name, REPO_ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_retirement_refusal_reaches_its_callers_as_their_own_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The five RETAINED-CONSUMER call sites translate `CarveRowRetired`
    instead of letting it out as a traceback (Copilot review of PR #1032,
    rounds 1 and 2 — round 1 found three, round 2 found the two that resolve
    a path through a ROOT rather than by name).

    `shed_destination()` is how a consumer of a file the § 5.2 shed MOVED
    reads it from the pinned leg (RULED (a), `#656` comment `5625573095`). It
    resolves through `source()`, so the day a row is first retired it raises —
    and each of its three callers guards only the lazy IMPORT with
    `except ImportError`, not the CALL. `CarveRowRetired` IS an `ImportError`
    subclass, which is what makes the omission easy to miss and its
    consequence bad: the refusal would have arrived as an uncaught traceback
    in three validators that otherwise report every failure as a finding.

    Each now answers in its own vocabulary — a `FAIL` line and a non-zero exit
    for the digest sweep, `CatalogError` (HRC-CATALOG-INVALID) for the Hermes
    family catalog, a named `RetiredSchema` finding for the cross-reference
    validator whose `main()` would otherwise label it `harness failure`, which
    is the one thing it is not, `ContractPinError` for the doxbench contract
    pin — the refusal that function already raises for a pinned schema the
    checkout does not have — and `ReleaseDependencyError` for the release
    source, whose `exists()` would otherwise answer a plain FALSE for a file
    that is not absent but DELETED BY RULING.

    `scripts/sync-notebooklm-books.py` is deliberately NOT in this list, and
    the reason is a MEASUREMENT rather than a reading of its docstring
    (Copilot review of PR #1032, round 8, which was right to ask). Its
    `_dashboard_module()` asks `module()` for exactly three names, every one of
    them a MOVED row no ruling has retired, so the refusal is unreachable
    there — not caught, unreachable. That is worth less than the five
    translations above, because it is a property of the manifest and not of the
    code, so it is PINNED:
    `test_no_module_the_notebook_sync_asks_for_is_retired` derives the names
    from the source with `ast` and fails the day a retirement reaches one of
    them. The measurement behind the pin: of the sixteen `_dashboard_module()`
    call sites, FIFTEEN sit under no `try` at all — the one exception is the
    orphan sweep, which is the site the review named, and which is inside
    `except Exception`. So the answer to "is it handled" is no; the answer to
    "can it happen" is no, and the pin is what keeps the second answer honest.
    """
    import carved_reach

    # IMPORTED BEFORE THE PATCH, every one of them: two of these modules read
    # the manifest AT IMPORT TIME (`doxbench_contracts.VALIDATOR_IN_CHECKOUT`
    # is computed from a row), and importing them under the stub rows below
    # would cache an answer derived from a fixture for the rest of the
    # session.
    digests = _load_by_path("validate-manifest-digests.py",
                            "validate_manifest_digests")
    cross = _load_by_path("validate-ideation-cross-reference.py",
                          "validate_ideation_cross_reference")
    catalog = importlib.import_module("scripts.hermes_runtime_validation.catalog")
    release = importlib.import_module("scripts.hermes_runtime_validation.release")
    doxbench = importlib.import_module("ideation_dashboard.doxbench_contracts")

    key = "scripts/ideation_dashboard/retired_reader.py"
    rows = {key: {
        "source_path": key,
        "disposition": "moved_verbatim",
        "destination": "opendox_code",
        "destination_path": "src/opendox/retired_reader.py",
        "retired": {"at": "opendox_code",
                    "at_path": "src/opendox/retired_reader.py",
                    "ruling": RETIREMENT_CITATION,
                    "surface": RETIRED_SURFACE}}}
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)
    # A STAND-IN LEG, so the tail below measures the retirement and not
    # whether this checkout happens to have its submodules materialized.
    leg = tmp_path / "openDox" / "code"
    (leg / ".git").mkdir(parents=True)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        dict(carved_reach.MOUNTS, opendox_code=leg))
    target = carved_reach.REPO_ROOT / key

    with pytest.raises(digests.RetiredMember) as caught:
        digests.shed_aware(target)
    assert "5656343213" in str(caught.value), caught.value

    with pytest.raises(cross.RetiredSchema) as raised:
        cross.shed_aware(target)
    assert "RETIRED" in str(raised.value), raised.value
    assert not isinstance(raised.value, ImportError), (
        "the whole point is that it stops being an ImportError at the caller")

    with pytest.raises(catalog.CatalogError) as refused:
        catalog._shed_destination(target, "contracts[0]")
    assert "contracts[0]" in str(refused.value), refused.value
    assert "5656343213" in str(refused.value), refused.value

    with pytest.raises(release.ReleaseDependencyError) as owed:
        release._shed_aware(target)
    assert "RETIRED" in str(owed.value), owed.value
    assert "5656343213" in str(owed.value), owed.value

    with pytest.raises(doxbench.ContractPinError) as pinned:
        doxbench._shed_aware(target)
    assert "RETIRED" in str(pinned.value), pinned.value
    assert "5656343213" in str(pinned.value), pinned.value

    # …and with NO retirement on the row the five answer exactly as before.
    rows[key].pop("retired")
    assert digests.shed_aware(target) == carved_reach.source(key)
    assert cross.shed_aware(target) == carved_reach.source(key)
    assert catalog._shed_destination(target, "contracts[0]") \
        == carved_reach.source(key)
    assert release._shed_aware(target) == carved_reach.source(key)
    assert doxbench._shed_aware(target) == carved_reach.source(key)


def test_no_module_the_notebook_sync_asks_for_is_retired() -> None:
    """THE EIGHTH CALL SITE, kept safe by the manifest rather than by a handler
    (Copilot review of PR #1032, round 8).

    `scripts/sync-notebooklm-books.py::_dashboard_module()` calls
    `carved_reach.module()` and translates nothing, so a `CarveRowRetired` out
    of it would arrive as an uncaught traceback at fifteen of its sixteen call
    sites — measured with `ast`, and the sixteenth is the orphan sweep, which
    is inside `except Exception`. The review asked for a translation there.
    This act does not write one, and this test is the reason it does not have
    to: THE REFUSAL IS UNREACHABLE AT THAT CONSUMER, because every name it can
    ask for is a MOVED row that no ruling has retired.

    "Unreachable" is a claim about the MANIFEST, not about the code, and a
    claim about the manifest can stop being true in somebody else's pull
    request without anyone re-reading this one. So it is asserted here, and the
    names are DERIVED FROM THE SOURCE rather than typed: the day an act retires
    a row the notebook sync reads, this test fails and names it, which is the
    moment to write the translation the review asked for — at that act, where
    the vocabulary to translate INTO is known.

    THE COLLECTOR MUST NOT UNDER-REPORT, which is the one way a test like this
    passes while being wrong: a call whose argument is not a string literal
    would be invisible to it and the row behind it unchecked. Every argument is
    required to be a literal, and the set is required to be non-empty, so a
    renamed helper or a computed name fails here rather than quietly narrowing
    what is asked.
    """
    source = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))

    names: set[str] = set()
    calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "_dashboard_module"):
            continue
        calls += 1
        assert len(node.args) == 1 and not node.keywords, ast.dump(node)
        arg = node.args[0]
        assert isinstance(arg, ast.Constant) and isinstance(arg.value, str), (
            f"{source.name}:{node.lineno} asks _dashboard_module() for "
            f"{ast.unparse(arg)}, which this test cannot resolve — either make "
            "it a literal or check the row it names by hand")
        names.add(arg.value)
    assert calls, "no _dashboard_module() call sites found — has it been renamed?"
    assert names, "call sites found but no names — the collector is wrong"

    # THE SPELLING THE LOADER BUILDS, read off the loader and not assumed: it
    # asks for `scripts/ideation_dashboard/<name>.py`, which is a manifest
    # `source_path`.
    loader = source.read_text(encoding="utf-8")
    assert 'carved_module(f"scripts/ideation_dashboard/{name}.py")' in loader, (
        "the loader no longer builds the path this test checks rows for")

    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    rows = {row["source_path"]: row
            for row in yaml.safe_load(manifest.read_text(encoding="utf-8"))["rows"]}
    for name in sorted(names):
        key = f"scripts/ideation_dashboard/{name}.py"
        row = rows.get(key)
        assert row is not None, f"{key} is asked for and is in no manifest row"
        assert MODULE.retired_at(row) == (None, None), (
            f"{key} carries a retirement and `_dashboard_module()` translates "
            "nothing — write the translation Copilot round 8 on PR #1032 asked "
            "for, in the act that retires it")
        # …and the OTHER branch of `module()` that refuses, so this test is
        # about "the loader answers" and not only about retirement.
        assert row["disposition"] != "not_moved" \
            or row.get("reason") != "deleted_at_carve", row


def test_the_two_marker_call_sites_answer_a_retired_row_instead_of_raising(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The SIXTH and SEVENTH call sites, and the only two that must NOT
    translate the refusal into a finding (Copilot review of PR #1032, round
    4): they ask `shed_relpath()` for a NAME, and one of them asks it at
    IMPORT TIME.

    `doxbench_contracts._validator_in_checkout()` is evaluated into the
    module constant `VALIDATOR_IN_CHECKOUT`, which is one of
    `PUBLISHER_MARKERS`, so a `CarveRowRetired` out of it would not be a
    finding at all — it would take down the import of the module whose whole
    job is to answer `ContractPinError`-or-absence, for every consumer, on
    the day the validator row was retired. `_composed_validator()` asks the
    same question about the same row to decide whether there is anything to
    compose. Both `except ImportError` blocks guard the lazy IMPORT and not
    the CALL, exactly as the five in
    `test_the_retirement_refusal_reaches_its_callers_as_their_own_error` did.

    THE ANSWER IS THE MODULE'S OWN CONTROLLED ABSENCE, not a softer refusal:
    a retirement means the file is at NO checkout, so the honest marker is
    one that is not there — the pre-shed spelling, whose `exists()` answers
    False and stops this tree reading as a publisher of a file a ruling
    deleted. That is what a manifest-less consumer copy already gets, reached
    by a different road. The composer answers with the validator it was
    handed, which is its `moved is None` answer for the same reason.
    """
    import carved_reach
    doxbench = importlib.import_module("ideation_dashboard.doxbench_contracts")

    key = "scripts/validate-ideation-dashboard-contracts.py"
    pre_shed = Path("scripts") / "validate-ideation-dashboard-contracts.py"
    rows = {key: {
        "source_path": key,
        "disposition": "moved_with_declared_edit",
        "destination": "openxdox_code",
        "destination_path": key,
        "retired": {"at": "openxdox_code",
                    "at_path": key,
                    "ruling": RETIREMENT_CITATION,
                    "surface": RETIRED_SURFACE}}}
    monkeypatch.setattr(carved_reach, "_rows", lambda: rows)

    assert doxbench._validator_in_checkout() == pre_shed

    # A REAL FILE, because the composer returns before it asks anything of a
    # path that is not one — and a fresh one per call, because the function is
    # `lru_cache`d on its argument.
    retired_validator = tmp_path / "retired" / pre_shed.name
    retired_validator.parent.mkdir()
    retired_validator.write_text("# a stand-in validator\n", encoding="utf-8")
    assert doxbench._composed_validator(retired_validator) == retired_validator

    # …and with the retirement off the row, the same two calls resolve through
    # the row exactly as they always did, which is what makes the two answers
    # above the RETIREMENT's and not the stub's.
    rows[key].pop("retired")
    moved = carved_reach.shed_relpath(key)
    assert moved is not None and moved.endswith(key), moved
    assert doxbench._validator_in_checkout() == Path(moved)
    live_validator = tmp_path / "live" / pre_shed.name
    live_validator.parent.mkdir()
    live_validator.write_text("# a stand-in validator\n", encoding="utf-8")
    assert doxbench._composed_validator(live_validator) == live_validator


# --------------------------------------------------------------------------
# `phase: post-shed` — the § 5.2 shed, declared IN the manifest
#
# The shed deletes every MOVED row's source path and the one
# `deleted_at_carve` row. Under the default phase that refuses twice by name
# (check 3 pass 2, then check 4's `vanished` arm) and it is right to; under
# `post-shed` it is the declared outcome. Every case below is built the same
# way as every other case in this file — a real tree, a real deletion, and
# the validator run as a subprocess — so nothing here is a claim about a
# branch that was never taken.
# --------------------------------------------------------------------------

def shed(scratch: Scratch, doc: dict[str, Any], *extra: str) -> str:
    """Delete every path the manifest's own rows say the shed removes.

    DERIVED FROM THE DOCUMENT, never from a hand-written list — the same rule
    the validator's own `shed_set` follows, and the reason a test that
    listed the paths would stop being evidence the moment a row changed
    disposition. Returns the deleting commit's sha.
    """
    paths = [row["source_path"] for row in doc["rows"]
             if row["disposition"] in MODULE.MOVED_DISPOSITIONS
             or row.get("reason") == "deleted_at_carve"]
    assert paths, "the fixture manifest declares nothing the shed would remove"
    _git(scratch.repo, "rm", "-q", "--", *paths, *extra)
    return commit_since_the_carve(scratch, "the shed")


def test_the_shed_refuses_under_the_default_phase(scratch: Scratch) -> None:
    """The finding this whole phase exists to answer, pinned FIRST.

    A manifest that says nothing about a phase is the file as landed, and over
    a shed tree it refuses at check 3 pass 2 — `carve-path-absent`, naming
    rows[0]. That is the measured behaviour the post-shed mode is a deliberate
    departure from, and it must stay true or the departure is from nothing.
    """
    doc = clean_manifest(scratch)
    assert "phase" not in doc
    shed(scratch, doc)
    combined = refuses(scratch, doc, "carve-path-absent")
    assert "DELETED SINCE THE CARVE" in combined, combined


def test_a_post_shed_manifest_verifies_over_a_shed_tree(
        scratch: Scratch) -> None:
    """The whole of exit (a) in one case: the same document, the same carve
    commit, the same digests — one declared word — over the tree § 5.2
    leaves."""
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    doc["rows"] = [dict(row) for row in doc["rows"]]
    # One `deleted_at_carve` row, as the real manifest has: the shed takes it
    # too, and check 4 rather than check 3 is what reads it.
    gamma = row_named(doc, "gamma.py")
    for key in ("git_mode", "sha256", "destination", "destination_path"):
        gamma.pop(key, None)
    gamma["disposition"] = "not_moved"
    gamma["reason"] = "deleted_at_carve"
    gamma["evidence"] = "the profile module openXdox declares for itself"

    head = shed(scratch, doc)
    scratch.write(doc)
    done = run(scratch)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "phase post-shed," in done.stdout, done.stdout
    # 2 moved rows + the one `deleted_at_carve` row.
    assert "3 shed row(s) absent at source as declared" in done.stdout, \
        done.stdout
    # PASS 1 IS UNTOUCHED: both moved rows' digests are still recomputed from
    # the referent's real bytes, which the shed does not reach.
    assert "2 digest(s) recomputed" in done.stdout, done.stdout
    assert f"verified at {head[:12]}" in done.stdout, done.stdout


def test_a_post_shed_manifest_over_an_unshed_tree_refuses(
        scratch: Scratch) -> None:
    """THE SYMMETRY, and the reason this is a floor and not a mute.

    Flipping the phase ahead of the deletions would buy silence for all 319
    rows at once. It refuses instead, at check 3, naming the first moved row
    the tree still carries.
    """
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    combined = refuses(scratch, doc, "carve-shed-incomplete")
    assert "STILL PRESENT UNDER A POST-SHED MANIFEST" in combined, combined


def test_a_post_shed_deleted_at_carve_row_still_present_refuses(
        scratch: Scratch) -> None:
    """The mirror arm's own case — a `not_moved` row, which the digest loop
    never reads, so only check 4 can report it."""
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    doc["rows"] = [dict(row) for row in doc["rows"]]
    gamma = row_named(doc, "gamma.py")
    for key in ("git_mode", "sha256", "destination", "destination_path"):
        gamma.pop(key, None)
    gamma["disposition"] = "not_moved"
    gamma["reason"] = "deleted_at_carve"
    gamma["evidence"] = "the profile module openXdox declares for itself"
    # The MOVED rows are shed; the `deleted_at_carve` row is left behind, so
    # check 3's arm passes and check 4's is the one that must speak.
    moved = [row["source_path"] for row in doc["rows"]
             if row["disposition"] in MODULE.MOVED_DISPOSITIONS]
    _git(scratch.repo, "rm", "-q", "--", *moved)
    commit_since_the_carve(scratch, "a half shed")
    combined = refuses(scratch, doc, "carve-shed-incomplete")
    assert "gamma.py" in combined, combined
    assert "the phase and the deletions are one act" in combined.lower(), \
        combined


def test_a_row_that_stays_may_not_be_deleted_by_the_shed(
        scratch: Scratch) -> None:
    """`stays_openxfactory_adapter` is NOT in the shed set, so its deletion is
    still the `carve-path-absent` it always was — the guarantee post-shed mode
    must not quietly widen."""
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    combined_paths = [row["source_path"] for row in doc["rows"]
                      if row["disposition"] in MODULE.MOVED_DISPOSITIONS]
    _git(scratch.repo, "rm", "-q", "--", *combined_paths,
         "scripts/pkg/delta.py")
    commit_since_the_carve(scratch, "the shed, plus one row that stays")
    combined = refuses(scratch, doc, "carve-path-absent")
    assert "delta.py" in combined, combined
    assert "every row named above is a row that STAYS" in combined, combined


def test_a_file_appearing_under_the_surface_still_refuses_post_shed(
        scratch: Scratch) -> None:
    """Post-shed does not open the surface. A new file under a shed prefix is
    still an UNDECLARED MOVEMENT — the constraint pre-dates the shed and the
    phase does not touch it."""
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    shed(scratch, doc)
    _write(scratch.repo, "scripts/pkg/epsilon.py", "EPSILON = 5\n")
    commit_since_the_carve(scratch, "a new file under the surface",
                           "scripts/pkg/epsilon.py")
    combined = refuses(scratch, doc, "carve-file-undeclared")
    assert "epsilon.py" in combined, combined


def test_the_carve_commits_own_line_refuses_under_a_post_shed_manifest(
        scratch: Scratch) -> None:
    """`--at <carve_commit>` STOPS ANSWERING once the phase flips, and this
    pins that cost rather than hiding it.

    At the carve commit every source path IS present, which is exactly what a
    post-shed manifest refuses — so the ceremony's own documented second
    invocation refuses `carve-shed-incomplete` from the shed commit onward.
    It is deliberately NOT special-cased: a phase that could be satisfied two
    ways is a phase that says less, and admitting `--at` at a pre-shed
    revision would be the one hole through which the symmetry above leaks.
    The cost is documented instead, in the manifest's own header block and in
    runbook § 0.4, both of which name the two remaining ways to ask about the
    carve's own line — check out a pre-shed revision, or read the digests
    straight out of git.
    """
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    shed(scratch, doc)
    scratch.write(doc)
    done = run(scratch, "--at", scratch.head)
    assert done.returncode == 2, done.stdout + done.stderr
    assert "carve-shed-incomplete" in done.stdout + done.stderr, \
        done.stdout + done.stderr


def test_an_unknown_phase_refuses(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["phase"] = "shed"
    combined = refuses(scratch, doc, "carve-shape-invalid")
    assert "'shed'" in combined, combined


def test_an_absent_phase_is_the_carve_phase(scratch: Scratch) -> None:
    """Backward compatibility, ASSERTED. A manifest that never mentions the
    key must read exactly as it did before the key existed — including in the
    JSON, where a consumer reads the phase rather than inferring it."""
    doc = clean_manifest(scratch)
    assert "phase" not in doc
    scratch.write(doc)
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["phase"] == "carve"
    assert payload["shed_rows"] == 0


def test_json_reports_the_post_shed_phase(scratch: Scratch) -> None:
    doc = clean_manifest(scratch)
    doc["phase"] = "post-shed"
    shed(scratch, doc)
    scratch.write(doc)
    done = run(scratch, "--json")
    assert done.returncode == 0, done.stdout + done.stderr
    payload = json.loads(done.stdout)
    assert payload["phase"] == "post-shed"
    # The fixture's three MOVED rows; all three digests are still recomputed
    # at the referent, which is pass 1 surviving the shed intact.
    assert payload["shed_rows"] == 3
    assert payload["digests_recomputed"] == 3


def test_the_phase_is_the_manifests_and_not_a_command_line_flag() -> None:
    """No `--phase`. A tree that verifies or refuses depending on which job
    invoked the tool is the one property a floor may not have, and the flag
    would also let the shed land in one commit and the declaration in
    another."""
    done = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "--phase" not in done.stdout, done.stdout


# --------------------------------------------------------------------------
# the real repository — the § 8.2 seat
# --------------------------------------------------------------------------

def the_landed_manifest() -> tuple[str, dict[str, Any]]:
    """The committed manifest's TEXT and document — and a failure if it is gone.

    THE SEAT-HOLDING BRANCH HAS OUTLIVED ITS REASON (Copilot review, this pull
    request). The module docstring's `if not manifest.is_file()` was written
    while `docs/opendox-carve-manifest.yaml` did not exist — the § 6 ceremony
    authors it at the carve commit, AFTER the validator lands — so every
    assertion about its contents had to hold a seat until then. The ceremony
    has happened: the manifest is committed, and there is no revision these
    tests can run at where it is absent. What the seat had degraded into is
    `assert True`, which REPORTS A PASS, so a checkout that lost the file
    turned five pins on the landed document into five green no-ops. A green
    bar that means "the check did not run" is the one thing this floor exists
    to refuse, and these five are the tests that read the real document.

    `test_the_real_repository_answers_at_the_ruled_path` below still branches,
    and must: the absence is that test's own subject, and it answers it by
    asserting the validator's `NO MANIFEST` line rather than by asserting
    nothing.
    """
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    assert manifest.is_file(), (
        f"{MODULE.MANIFEST_RELPATH} is not in this checkout. It landed at the "
        "carve commit, and every assertion in this test is about its "
        "contents: its absence is a FAILURE, not a seat to hold.")
    text = manifest.read_text(encoding="utf-8")
    return text, yaml.safe_load(text)


def dict_literal_keys(path: Path, name: str) -> list[str]:
    """Every key of the module-level dict literal `name`, in source order and
    WITH ITS DUPLICATES, which the imported object can no longer report — a
    dict literal collapses a repeated key at import and keeps the last value.
    Read with `ast`, the same way `test_every_code_the_validator_can_emit_is_
    in_the_vocabulary` reads the validator's own source.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign):
            target = node.target
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        else:
            continue
        if not (isinstance(target, ast.Name) and target.id == name):
            continue
        assert isinstance(node.value, ast.Dict), ast.dump(node.value)
        keys = [key.value for key in node.value.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)]
        # `**other` and a computed key both arrive as a key node this walk
        # cannot read, and either one would let entries escape the count.
        assert len(keys) == len(node.value.keys), (name, len(node.value.keys))
        return keys
    raise AssertionError(f"{name} is not a module-level assignment in {path}")


def test_the_real_repository_answers_at_the_ruled_path() -> None:
    """The documented invocation, from the repository root, with no arguments.

    A BRANCH and never a skip: see the module docstring. The § 6 ceremony has
    landed the manifest at the carve commit, so the call prints `OK` today and
    the seat-holding line is what answered before it. This is the ONE
    absent-manifest arm left in this module; everywhere else the absence is a
    failure (`the_landed_manifest()`).
    """
    done = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        assert done.stdout.startswith("NO MANIFEST "), done.stdout
        assert "(nothing to validate)" in done.stdout, done.stdout
        return

    assert done.stdout.startswith("OK "), done.stdout

    # AND THE SEAT NAMES THE PHASE, in BOTH phases. Exit 0 alone cannot tell
    # "the tree still carries every source path" from "the shed has run and
    # the manifest declares it": those are two different floors, and after
    # § 5.2 the difference is the whole question. The declared phase is read
    # out of the file and required to be the phase the run REPORTS, so the
    # seat can only pass if the validator took the branch the document asks
    # for — a phase-blind run, or a run that silently fell back to the
    # default, fails here rather than reading as green.
    declared = yaml.safe_load(manifest.read_text(encoding="utf-8")).get(
        "phase", MODULE.PHASE_CARVE)
    assert declared in MODULE.PHASES, declared
    assert f"phase {declared}," in done.stdout, done.stdout

    # The two phases owe DIFFERENT evidence on the same line, and neither
    # sentence is producible by the other's code path.
    if declared == MODULE.PHASE_POST_SHED:
        # A shed count is only printed after check 3's post-shed arm has
        # proved every one of those rows ABSENT, so the number is a claim
        # about the tree and not a row count copied out of the document.
        assert "shed row(s) absent at source as declared" in done.stdout, \
            done.stdout
    else:
        assert "shed row(s)" not in done.stdout, done.stdout


# ---------------------------------------------------------------------------
# THE § 3.4 SLICE-S7 DECLARED-EDIT WINDOW, BY ROW AND CLASS
#
# "Parameterize class C — every governance word in the fourteen class-C files
# and the four declared class-A tails becomes a read of the registered domain's
# DISPLAY facet BY ROLE" (openDox-spec `docs/front-end-package-boundary.md` § 5
# row S7 and § 4.3 @ `7d12428c`; RULED Q1/Q2/Q7, `#656` comment `5648049748`,
# Brett Heap 2026-09-12; the FORM is RULED Q-L1's, `5628560136`).
#
# WHY THE WHOLE WINDOW IS HERE AND NOT A SAMPLE. The aggregate assertion
# `(2621, 176)` would still pass if any of these 782 lines had landed on the
# wrong row, under the wrong class, or as a different set summing to the same
# total — which is the reason every slice since ASK-7 has pinned its own window
# by row and class. S7 edits 33 rows where S5 edited 11, so the pins are a TABLE
# rather than a run of hand-written asserts; it is the same claim, made once per
# row instead of once per slice. The entries are the LAST ones on each row,
# because an annotation appends to whatever the row already carried, and the
# assertion below reads them that way rather than by matching prose.
S7_WINDOW: dict[str, list[tuple[str, list[int]]]] = {
    "scripts/ideation_dashboard/canvas_drafts.py": [
        ("adapter calls", [56, 57, 146, 189]),
    ],
    "scripts/ideation_dashboard/web/app.js": [
        ("adapter calls", [473, 819, 867, 1050, 1095]),
    ],
    "scripts/ideation_dashboard/web/index.html": [
        ("adapter calls", [
            28, 29, 54, 56, 57, 58, 59, 60, 61, 62, 98, 99, 100, 101
        ]),
    ],
    "scripts/ideation_dashboard/web/styles.css": [
        ("adapter calls", [
            18, 19, 20, 21, 30, 55, 56, 57, 58, 79, 80, 81, 82, 99, 100,
            101, 102, 256, 260, 261, 270, 277, 281, 287, 305, 306, 311,
            326, 331, 352, 353, 354, 355, 366, 367, 368, 369, 370, 371,
            372, 373, 374, 375, 376, 377, 393, 398, 426, 437, 451, 491,
            492, 493, 505, 551, 568, 586, 604, 621, 630, 637, 638, 642,
            645, 646, 709, 713, 714, 720, 721, 772, 773, 776, 791, 800,
            814, 815, 831, 841, 844, 851, 858, 869, 877, 879, 900, 920,
            921, 922, 927, 929, 993, 996, 1016, 1032, 1035, 1042, 1049,
            1050, 1075, 1125, 1126, 1128, 1149, 1150, 1151, 1164, 1167,
            1194, 1204, 1213, 1225, 1229, 1242, 1245, 1273, 1291, 1306,
            1324, 1327, 1333, 1335, 1347, 1371, 1372, 1386, 1446, 1458,
            1474, 1475, 1481, 1482, 1492, 1504, 1528, 1544, 1582, 1584,
            1591, 1601, 1603, 1682, 1692, 1704, 1715, 1726, 2128, 2155,
            2158, 2159, 2168, 2519
        ]),
    ],
    "scripts/ideation_dashboard/web/views/board.js": [
        ("import rewrites", [16]),
        ("adapter calls", [
            18, 59, 87, 105, 106, 117, 118, 125, 126, 141, 142, 145, 147,
            154, 155, 156, 157, 168, 169, 194, 202, 203, 204, 217, 219,
            220, 222, 223, 225, 226, 228, 234
        ]),
    ],
    "scripts/ideation_dashboard/web/views/canvas-model.js": [
        ("import rewrites", [1]),
        ("adapter calls", [
            35, 36, 37, 60, 63, 77, 127, 142, 145, 175, 176, 182, 187, 189,
            196, 197, 209, 213
        ]),
    ],
    "scripts/ideation_dashboard/web/views/canvas.js": [
        ("import rewrites", [28]),
        ("adapter calls", [
            52, 66, 69, 112, 115, 117, 119, 128, 129, 133, 134, 135, 137,
            138, 156, 164, 167, 170, 178, 185, 194, 239, 263, 269, 273,
            286, 289, 292, 304, 306, 307, 357, 358, 359, 361, 376, 381
        ]),
    ],
    "scripts/ideation_dashboard/web/views/doc-wheel.js": [
        ("import rewrites", [45]),
        ("adapter calls", [52, 98, 100, 124, 129, 162]),
    ],
    "scripts/ideation_dashboard/web/views/docs.js": [
        ("import rewrites", [14]),
        ("adapter calls", [
            16, 17, 18, 20, 21, 22, 23, 24, 76, 116, 126, 134, 146, 152,
            177
        ]),
    ],
    "scripts/ideation_dashboard/web/views/explorer.js": [
        ("import rewrites", [1]),
        ("adapter calls", [
            44, 46, 47, 48, 49, 50, 51, 54, 80, 82, 89, 91, 94, 99, 103,
            108, 119, 124, 148, 221, 239, 272
        ]),
    ],
    "scripts/ideation_dashboard/web/views/funnel.js": [
        ("import rewrites", [24]),
        ("adapter calls", [
            26, 42, 44, 45, 75, 78, 109, 116, 121, 122, 126, 127, 128, 133,
            135, 162, 163, 174, 176, 191, 194, 196, 197, 198, 199, 213,
            248, 249, 250, 269, 271, 293, 328, 331, 425, 429, 437, 441,
            510
        ]),
    ],
    "scripts/ideation_dashboard/web/views/grouping.js": [
        ("import rewrites", [24]),
        ("adapter calls", [
            34, 35, 36, 37, 38, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52,
            53, 58, 64, 69, 209
        ]),
    ],
    "scripts/ideation_dashboard/web/views/helpers.js": [
        ("adapter calls", [15, 16]),
    ],
    "scripts/ideation_dashboard/web/views/lineage.js": [
        ("import rewrites", [13]),
        ("adapter calls", [
            41, 47, 52, 62, 63, 64, 65, 76, 77, 78, 79, 80, 81, 82, 83,
            104, 115, 116, 117, 124, 129, 130, 138
        ]),
    ],
    "scripts/ideation_dashboard/web/views/model.js": [
        ("adapter calls", [
            1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 35, 37, 38, 39, 40,
            41, 56, 57, 58, 59, 61, 62, 63, 64, 65, 67, 68, 80, 81, 83, 86,
            87, 89, 92, 93, 95, 97, 98, 100, 103, 104, 105, 106, 107, 108,
            109, 110, 115, 116, 117, 119
        ]),
    ],
    "scripts/ideation_dashboard/web/views/outline-model.js": [
        ("import rewrites", [1]),
        ("adapter calls", [
            92, 152, 153, 154, 155, 158, 160, 316, 340, 343, 361, 366
        ]),
    ],
    "scripts/ideation_dashboard/web/views/repo-selector-model.js": [
        ("import rewrites", [1]),
        ("adapter calls", [
            517, 518, 519, 520, 521, 522, 523, 525, 527, 531, 532
        ]),
    ],
    "scripts/ideation_dashboard/web/views/staging-workbench-model.js": [
        ("import rewrites", [29]),
        ("adapter calls", [
            31, 54, 56, 57, 64, 65, 69, 70, 74, 75, 85, 86, 89, 91, 138,
            269, 281, 304, 337, 539, 540, 541, 542, 551, 552, 554, 612,
            626, 634, 635, 636, 637, 638, 726, 731, 1042, 1043, 1044, 1045,
            1046, 1050, 1104, 1108, 1112, 1238, 1247, 1251, 1255, 1433,
            1446, 1447
        ]),
    ],
    "scripts/ideation_dashboard/web/views/staging-workbench.js": [
        ("adapter calls", [
            83, 113, 114, 115, 116, 119, 126, 131, 132, 133, 134, 135, 434,
            520, 1086, 1130, 1131, 1132, 1137, 1139, 1391, 1392, 1393,
            1576, 1617, 1677, 1684, 1701, 1928, 1955, 2434, 2905, 2912,
            2952, 2987, 3159, 3279
        ]),
    ],
    "scripts/ideation_dashboard/web/views/wheel-model.js": [
        ("adapter calls", [
            20, 21, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 55, 63, 64,
            71, 74, 86, 88, 91, 93, 95, 97, 100, 104, 105, 106, 107, 108,
            109, 114, 122, 123, 125, 128, 129, 132, 135, 136, 137, 139,
            141, 142, 144, 147, 150, 179, 181, 182, 183, 184, 185, 187,
            188, 190, 191, 193, 200, 201, 203, 207, 593, 594, 630, 632,
            636, 643, 644, 655, 660, 661, 662, 669, 670, 673, 678, 685,
            686, 705, 706, 722, 723, 729, 760, 764, 1088, 1096, 1101, 1105,
            1107, 1108
        ]),
    ],
    "scripts/ideation_dashboard/web/views/wheel.js": [
        ("import rewrites", [71]),
        ("adapter calls", [
            67, 139, 141, 143, 145, 155, 167, 174, 179, 184, 207, 214, 218,
            229, 236, 263, 375, 521, 601, 603, 789, 792, 831, 857, 1168,
            1169, 1170, 1199, 1255, 1344, 1481, 1483, 1499, 1632
        ]),
    ],
    "tests/ideation-dashboard/test_bullseye_widget.py": [
        ("path constants", [1988, 1989, 1990, 1991]),
        ("adapter calls", [
            45, 1277, 1318, 1319, 1751, 1752, 1756, 1757, 1758, 1759, 1977,
            2071, 2073, 2074, 2075
        ]),
    ],
    "tests/ideation-dashboard/test_doc_surfaces.py": [
        ("adapter calls", [
            90, 161, 202, 291, 298, 300, 301, 312, 321, 323, 327, 337, 339,
            340
        ]),
    ],
    "tests/ideation-dashboard/test_doc_wheel.py": [
        ("adapter calls", [135]),
    ],
    "tests/ideation-dashboard/test_doxbench_abstract_pane.py": [
        ("adapter calls", [152]),
    ],
    "tests/ideation-dashboard/test_doxbench_accessibility.py": [
        ("adapter calls", [309]),
    ],
    "tests/ideation-dashboard/test_doxbench_context_panes.py": [
        ("adapter calls", [117]),
    ],
    "tests/ideation-dashboard/test_doxbench_tile_verbs.py": [
        ("import rewrites", [25]),
        ("adapter calls", [36, 288, 333]),
    ],
    "tests/ideation-dashboard/test_doxbench_view.py": [
        ("adapter calls", [
            2874, 2877, 2880, 4128, 4223, 4225, 4335, 4337, 4380, 4381,
            4382, 4383, 4384, 4385, 4386, 4387, 4388, 4389, 4390, 4391,
            4392, 4393, 4394, 4395, 4396, 4398, 4399, 4412, 4414, 4562,
            4563, 4564, 4567, 4568, 4569, 4571, 4938, 5004, 5006
        ]),
    ],
    "tests/ideation-dashboard/test_outline_model.py": [
        ("adapter calls", [208, 212]),
    ],
    "tests/ideation-dashboard/test_outline_tab.py": [
        ("adapter calls", [785, 864, 865, 866]),
    ],
    "tests/ideation-dashboard/test_wheel_paint_and_reach.py": [
        ("adapter calls", [132]),
    ],
    "tests/ideation-dashboard/test_wheel_verbs_dom.py": [
        ("adapter calls", [310]),
    ],
}

# The seventeen rows this act converts `moved_verbatim` -> declared. Named,
# because a conversion is the one edit that moves BOTH disposition counts and
# the carrier count at once, and an act that converted a row it did not mean to
# would still sum correctly.
S7_CONVERTED = [
    "scripts/ideation_dashboard/canvas_drafts.py",
    "scripts/ideation_dashboard/web/index.html",
    "scripts/ideation_dashboard/web/styles.css",
    "scripts/ideation_dashboard/web/views/board.js",
    "scripts/ideation_dashboard/web/views/canvas-model.js",
    "scripts/ideation_dashboard/web/views/canvas.js",
    "scripts/ideation_dashboard/web/views/doc-wheel.js",
    "scripts/ideation_dashboard/web/views/docs.js",
    "scripts/ideation_dashboard/web/views/explorer.js",
    "scripts/ideation_dashboard/web/views/funnel.js",
    "scripts/ideation_dashboard/web/views/grouping.js",
    "scripts/ideation_dashboard/web/views/helpers.js",
    "scripts/ideation_dashboard/web/views/lineage.js",
    "scripts/ideation_dashboard/web/views/model.js",
    "scripts/ideation_dashboard/web/views/outline-model.js",
    "scripts/ideation_dashboard/web/views/repo-selector-model.js",
    "scripts/ideation_dashboard/web/views/wheel-model.js",
]


# THE THREE S7 ENTRIES THE EARLIER SLICES' ASSERTIONS FILTER OUT, read off the
# table above so there is ONE declaration of them — each earlier slice's
# assertion stays exactly its own (the idiom this file has used since S4
# filtered S3's, and S5 filtered S4's), and nothing is excluded that the
# S7 assertion does not itself pin.
WHEEL_S7_ADAPTER_CALLS = dict(
    S7_WINDOW["scripts/ideation_dashboard/web/views/wheel.js"])["adapter calls"]
APP_JS_S7_ADAPTER_CALLS = dict(
    S7_WINDOW["scripts/ideation_dashboard/web/app.js"])["adapter calls"]
SWB_MODEL_S7_ADAPTER_CALLS = dict(S7_WINDOW[
    "scripts/ideation_dashboard/web/views/staging-workbench-model.js"])[
        "adapter calls"]


def test_the_real_manifest_carries_the_ruled_q_l7_amendment() -> None:
    """RULED Q-L7 (a) against the LANDED manifest, not a generated one.

    The two rows the ruling names, read out of the real document: a moved row
    that is ALSO replicated at `openxdox_code`, and a replica row declaring the
    lines its copies may differ on. That replica row declares TWO since the
    pre-existing `openxdox_code` annotation (`#656` CLAIM `5656688910`) — Q-L7
    (a)'s own `:25` depth constant and openXdox-code#14's `:271` § 4.4 fixture
    — and the assertion below pins both, in order, with their classes: `edits:`
    is a field of a ROW, so each is permitted at EVERY replica of this file and
    obligatory at none. The manifest is REQUIRED and not branched on: see
    `the_landed_manifest()`.

    Also carries RULED Q-L1's own per-row contract for the two rows S2 (RULED
    Q5, `#656` comment 5642758731) annotated, added on Copilot review of PR
    #1002: the AGGREGATE (lines, carrying) count below would stay green even
    if those three lines had landed on the wrong row or under the wrong edit
    class, so the exact row/disposition/class/lines are pinned here too.
    """
    _text, doc = the_landed_manifest()
    rows = {row["source_path"]: row for row in doc["rows"]}

    moved = rows["tests/ideation-dashboard/session_fixtures.py"]
    assert moved["disposition"] == "moved_with_declared_edit", moved
    assert moved["destination"] == "opendox_code", moved
    assert moved["also_replicated_to"] == ["openxdox_code"], moved

    replica = rows["tests/ideation-dashboard/conftest.py"]
    assert replica["disposition"] == "not_moved", replica
    assert replica["reason"] == MODULE.REPLICA_REASON, replica
    # The SECOND entry comes from the pre-existing `openxdox_code` annotation
    # (`#656` CLAIM `5656688910`): openXdox-code#14 appends a 27-line § 4.4
    # pytest fixture beside this file's LAST carve line, and an insertion at
    # the end of a file has ONE neighbour. A replica has no row of its own, so the
    # declaration is row-wide and openDox-code's copy simply does not take it
    # (measured at `05bbde80`: 271 lines, the `:25` depth fix and nothing
    # else) — a permission, never an obligation.
    assert [(edit["class"], edit["lines"]) for edit in replica["edits"]] == \
        [("path constants", [25]), ("adapter calls", [271])], replica

    # The ruling's own pairing: the replica IMPORTS the moved row's module
    # unconditionally, which is why one amendment carries both.
    assert "session_fixtures" in replica["evidence"], replica

    # RULED Q5 (`#656` comment 5642758731, split-opendox § 3.4 slice S2): the
    # exact row/disposition/class/lines the aggregate count below cannot tell
    # apart from a same-sized drift elsewhere (Copilot review, PR #1002).
    dispose = rows["scripts/ideation_dashboard/web/views/dispose.js"]
    assert dispose["disposition"] == "moved_with_declared_edit", dispose
    assert dispose["destination"] == "opendox_code", dispose
    assert [(edit["class"], edit["lines"]) for edit in dispose["edits"]] == [
        ("import rewrites", [26]),
        # § 3.4 SLICE S5: RULED Q12's four literal `/actions/gate/<verb>`
        # routes replacing the concatenation, RULED Q8's `page-overlay` mount
        # replacing the append to `document.body`, and RULED counterpart Q6's
        # `ctx.intent.emit` / `ctx.intent.renderChips`.
        ("adapter calls",
         [29, 30, 51, 53, 54, 55, 69, 184, 212, 213, 396]),
    ], dispose

    wheel = rows["scripts/ideation_dashboard/web/views/wheel.js"]
    assert wheel["disposition"] == "moved_with_declared_edit", wheel
    assert wheel["destination"] == "opendox_code", wheel
    # § 3.4 SLICE S7 adds this row's fourth and fifth entries (the one sibling
    # import, and every per-wheel map keyed by STAGE ROLE), so they are filtered
    # out here exactly as S5's were filtered out of S4's assertions — this
    # assertion is slices S1–S5's and stays theirs. S7's own entries are pinned
    # by row and class in `test_the_real_manifest_carries_the_s7_display_facet_
    # declared_edits` below.
    s7_wheel_lines = ([71], WHEEL_S7_ADAPTER_CALLS)
    through_s5_wheel = [(edit["class"], edit["lines"]) for edit in wheel["edits"]
                        if edit["lines"] not in s7_wheel_lines]
    assert through_s5_wheel == [
        ("import rewrites", [75, 76]),
        # § 3.4 SLICE S5: the two-line `from "./dispose.js"` import of eight
        # names — one of § 4.5 assertion 3's four breaches — is gone, and the
        # call sites read the DECLARED namespace the shell resolved.
        ("import rewrites", [73, 74]),
        ("adapter calls",
         [136, 140, 142, 144, 146, 358, 359, 427, 1174, 1185, 1195, 1196,
          1223, 1224, 1428, 1498, 1500, 1505, 1506, 1509, 1510]),
    ], wheel

    # And the counts this amendment moved, re-derived from the file rather than
    # transcribed: one more declared line than the 793 the runbook's § 2 table
    # carried before it, on one more row than the 146 that carried edits — and
    # then the Q-L1 ANNOTATIONS of 2026-09-10 (`#656` comment `5628560136`,
    # landed with the § 5.2 shed) moved both again, by 68 lines over seven rows,
    # three of which carried no `edits:` before. 794 + 68 = 862 on 147 + 3 = 150
    # rows. Then the ASK-7 DECLARED-EDIT WINDOW of 2026-09-11 (`#656`
    # comment `5635150678`, ASK-7 → 1) added 4 more declared lines to two
    # rows that ALREADY carried `edits:` — the cli.py and serve.py
    # docstring/comment lines — so `carrying` does not move: 862 + 4 = 866
    # on the same 150 rows. Then the Q-L1 ANNOTATION of 2026-09-11 (RULED
    # Q5, `#656` comment `5642758731`, split-opendox § 3.4 slice S2) moved
    # both again, by 3 lines over two rows (`dispose.js` line 26, `wheel.js`
    # lines 75-76), neither of which carried `edits:` before. 866 + 3 = 869
    # on 150 + 2 = 152 rows. AND THEN THE § 3.4 SLICE-S3 ANNOTATION of
    # 2026-09-12 (`#656` comment `5642758731`, whose Q-L1 paragraph binds
    # every § 3.4 slice) moved both once more: the view registry edits ONE
    # arrived file, `scripts/ideation_dashboard/web/app.js`, which converts
    # `moved_verbatim` -> `moved_with_declared_edit` and takes 37 lines in
    # two classes (`import rewrites` 1, `adapter calls` 36) on a row that
    # carried no `edits:` before, AND three more `adapter calls` lines on
    # `tests/ideation-dashboard/test_bullseye_widget.py`, which already
    # carried an edit: that suite asserts `app.js`'s shape by quoting its
    # lines back, so the three quotations of the tab router's field names
    # are invalidated by the `app.js` edit and are migrated in the same act.
    # 869 + 37 + 3 = 909 on 152 + 1 = 153 rows — the second row is not a new
    # carrier. AND THEN THE OPENDOX-CODE #14 FIX ROUND'S CATCH-UP (openxFactory
    # #1001, extended after landing) moved `lines` once more: running
    # `verify-carve-arrival.py --destination opendox_code --phase B` against
    # openDox-code's post-Copilot-re-review head
    # (`e176947dd3691fa96b285575910989ed77e09181`) found one more undeclared
    # edit — `test_the_doc_tab_is_wired_to_the_one_cross_view_jump` in
    # `tests/ideation-dashboard/test_doc_surfaces.py` quoted `app.js`'s pre-S3
    # `{ tab: "tab-docs"` shape and was migrated to the registry shape in that
    # same fix round (Copilot finding "docs-tab migration"), the same
    # one-token-class migration `test_bullseye_widget.py` already took; the
    # `app.js` row itself needed no new declaration (the fix round's other two
    # findings — the gate bar's declared-entry mount and a view-registry
    # isolation fixture — both fall inside lines already declared on that row
    # or outside any arrived file). `test_doc_surfaces.py` already carried an
    # edit, so it is not a new carrier. 909 + 1 = 910 on the same 153 rows.
    #
    # AND THEN THE § 3.4 SLICE-S6 ANNOTATION (`#656` comment `5642758731`,
    # whose Q-L1 paragraph binds every § 3.4 slice, same as S2/S3 above)
    # moved `lines` once more, on ZERO new rows: RULED Q4's read-only
    # `/source` pass-through returns from a CONTRIBUTED binding
    # (`openxdox_code`'s `serve_projection.py`) to a FIXED core arm
    # (`opendox_code`'s `serve.py`) of the neutral product. Both rows were
    # ALREADY `moved_with_declared_edit`, so this act adds one `adapter
    # calls` entry to each and carries no new row into `carrying`: 10 lines
    # on `serve.py` (five insertions — the registration-modes record, the
    # two route constants, the containment entry point, the two `_route`
    # arms and the three handler methods) and 122 on `serve_projection.py`
    # (the matching deletions — the module docstring's opening, the "PAIR
    # MOVES TOGETHER" paragraph, the two constants, `resolve_source_path`,
    # the three handler methods and `ProjectionRoutesExtension`'s two
    # `/source` bindings). 910 + 10 + 122 = 1042 on the same 153 rows.
    #
    # AND THEN THE § 3.4 SLICE-S4 ANNOTATION (`#656` comment `5642758731`,
    # RULED Q3: "a route constant travels with the binding that calls it,
    # never with the model that happens to declare it") moved both again.
    # Seven ARRIVED rows are edited: `app.js` (already a carrier, gains one
    # `adapter calls` entry, 4 lines — the two new gate bindings' `routes:`
    # declarations); `lens-model.js`, `lens.js`, `repo-selector.js`,
    # `swb-create.js` and `swb-session.js` (five NEW carriers, `moved_verbatim`
    # -> `moved_with_declared_edit`); and `staging-workbench-model.js`
    # (already a carrier, gains two entries). 1042 + 380 = 1422 on 153 + 5 =
    # 158 rows. Four new files are admitted at `opendox_code`:
    # `views/gate-lens.js`, `views/gate-projects.js`,
    # `views/projection-index.js` and `tests/test_split_route_tails.py`.
    #
    # THIS ASSERTION IS WHERE THE ABSOLUTES LIVE, and deliberately so: the
    # document itself states each act as a DELTA (see the manifest's own
    # comment on why two acts restating one set of absolutes is how a count
    # becomes wrong in a merge), and the one place that sums them is this test,
    # which re-derives rather than transcribes. A transcribed count is a claim,
    # a summed one is a measurement.
    lines = sum(len(edit["lines"]) for row in doc["rows"]
                for edit in row.get("edits") or [])
    carrying = sum(1 for row in doc["rows"] if row.get("edits"))
    # AND THE SUM COUNTS LIST ENTRIES, SO THE ENTRIES MUST BE DISTINCT PER ROW
    # (Copilot review, `#1030`). Neither tool refuses a line declared twice on
    # one row — `validate-carve-manifest.py` bounds each number against the
    # blob and says nothing about repetition, and `verify-carve-arrival.py`
    # reads the row's declarations as a SET — so a duplicate raises this figure
    # by one while leaving one genuinely edited line undeclared, and the act
    # that did it would pass its own window pin, its own per-class figures and
    # this aggregate together. Measured over the whole document, because this
    # is the figure that is a MEASUREMENT of it.
    for row in doc["rows"]:
        flat = [number for edit in row.get("edits") or []
                for number in edit["lines"]]
        assert len(set(flat)) == len(flat), (row["source_path"], sorted(
            number for number in flat if flat.count(number) > 1))
    # AND THEN THE § 3.4 SLICE-S5 ANNOTATION (`#656` comments `5648044785` /
    # `5648049748` / `5648065587`, whose Q-L1 obligation binds every § 3.4
    # slice, same as S2/S3/S4/S6 above) moved both once more: "contribute the
    # gate loop" edits ELEVEN arrived rows (five at `opendox_code` — `serve.py`,
    # `app.js`, `wheel.js`, `staging-workbench.js`,
    # `test_bullseye_widget.py` — and six at `openxdox_code` — `gate.js`,
    # `dispose.js`, `swb-create.js`, `swb-session.js`,
    # `test_session_confinement.py`, `test_staging_workbench.py`) and converts
    # ONE of them — `views/staging-workbench.js`, `moved_verbatim` until this
    # slice — into a carrier. 1422 + 162 = 1584 on 158 + 1 = 159 rows. It is
    # also the FIRST act to use RULED Q6's `re_destined:` field, on four rows;
    # a re-destination is not an edit and moves neither figure, which the next
    # test measures.
    #
    # AND THEN THE § 3.4 SLICE-S7 ANNOTATION (RULED Q1/Q2/Q7, `#656` comment
    # `5648049748`, whose Q-L1 obligation binds every § 3.4 slice, same as
    # S2/S3/S4/S5/S6 above) moved both by the largest margin of any act so far:
    # "parameterize class C" edits THIRTY-THREE arrived rows, all at
    # `opendox_code`, and converts SEVENTEEN of them from `moved_verbatim`.
    # Every file in the served bundle is edited because every file in it
    # rendered a word. 1584 + 782 = 2366 on 159 + 17 = 176 rows.
    #
    # AND THEN THE § 3.4 SLICE-S8 ANNOTATION (`#656` comment `5642758731`,
    # whose Q-L1 paragraph binds every § 3.4 slice; S8 CLAIM `#656` comment
    # `5649985838`) moved `lines` once more, on ZERO new rows. S8 is "re-home
    # the 48 test files and un-narrow `validate`", and it carries NO
    # `re_destined:` row: measured at both leg heads, not one of the 48 may
    # lawfully change leg, because every one of the 23 at `openxdox_code`
    # imports a real `openxdox` module and RULED OQ-G's TEST HOMES rule places
    # a mixed file there for exactly that reason. The defect is the PATH
    # CONSTANT, which is § 1.2(d)'s own sentence — and that reading is now
    # RULED: `#656` comment `5656343213`, Brett Heap, 2026-09-13, by
    # interactive multi-choice, "the path constant moves, the file does
    # not", with boundary-note amendment #3 rewriting § 5's S8 row and
    # § 1.2(d) to it (48 re-measured to 43). THIRTEEN rows gain a
    # `path constants` entry — one each, and TWO for
    # `test_doxbench_mutation_boundary.py`, whose first entry the same slice
    # corrects — and every one of the thirteen was ALREADY a carrier, so
    # `carrying` does not move: six at `opendox_code` (`test_outline_model.py`
    # 1, `test_doxbench_view.py` 3, `test_doxbench_knowledge.py` 2,
    # `test_doxbench_document_abstract.py` 2, `test_doxbench_memory_gateway.py`
    # 2, `test_bullseye_widget.py` 1 = 11) and seven at `openxdox_code`
    # (`test_doxbench_mutation_boundary.py` 2 + 10, `test_doxbench_save.py` 5,
    # `test_doxbench_scope.py` 2, `test_renderer.py` 2,
    # `test_doxbench_abstract_store.py` 3, `test_doxbench_telemetry.py` 3,
    # `test_doxbench_turns.py` 2 = 29). The other edited sites across the two
    # legs needed no new line: the carve's own `import rewrites` pass already
    # declared the roots it rewrote, and an import inserted beside an
    # already-declared import line is declared by its neighbour
    # (`_check_declared_lines`' insertion rule). 2366 + 40 = 2406 on the same
    # 176 rows. One new file is admitted at `openxdox_code`:
    # `tests/opendox_bundle.py`.
    #
    # TEN OF THE FORTY ARE A CORRECTION TO THIS SLICE'S OWN FIRST PUSH, and
    # they are why the second push re-ran `_check_declared_lines` file-by-file
    # against both leg heads instead of reading the sweep's diff:
    # `test_doxbench_mutation_boundary.py` and `test_renderer.py` were short,
    # and nothing would have said so until a phase-B run at a tree carrying
    # every other slice's declarations too.
    #
    # AND THEN THE PRE-EXISTING `openxdox_code` ANNOTATION (`#656` CLAIM
    # `5656688910`) moved the LINE figure alone. It is not a § 3.4 slice's
    # annotation, and not the FIRST act on this document that is not one —
    # the ASK-7 declared-edit window (`#656` comment `5635150678`, PR #995) is
    # earlier, and the runbook's § 2 history records it. It differs from that
    # one in what it declares: ASK-7's four lines were RULED to be left and
    # fixed "at the next declared-edit window", so they were owed to someone
    # from the day of the ruling; these were scheduled by no ruling at all:
    # openXdox-code#14 (`3840c167`) and #16
    # (`17384c07`) landed RULING C2's § 4.4 work at the destination BEFORE
    # Q-L1's pairing became general (`#656` comment `5642758731`,
    # 2026-09-12 02:07Z), so no slice ever owned their edits, and openxFactory
    # #1023 § 5 listed them as `openxdox_code`'s remaining refusals rather than
    # absorbing them. Four rows are declared — `gate_console.py` (26 lines),
    # `generator.py` (17, split into the two acts that made them),
    # `test_generator.py` (4) and the conftest REPLICA (:271, the fourth and
    # the one #1023 could not see, because `--allow-created` had been used
    # where the runbook's `--replica-at` belongs and that suppresses the
    # replica's own line check). All four carried `edits:` already, so the
    # carrier count does not move: 2406 + 48 = 2454 on the same 176 rows.
    #
    # AND THEN THE RETIREMENT ACT (RULED 5656343213, Brett Heap 2026-09-13,
    # `#656` CLAIM `5656690570`) moved `lines` once more and `carrying` not at
    # all. The ruling retires three suites, and the third one's ROW is not
    # retired at all — the file goes on arriving, and what is declared is the
    # block removed from inside it: the ENDING REPLAY inside
    # `tests/ideation-dashboard/test_staging_workbench.py` — `_DOM_SHIM`,
    # `_ENDING_REPLAY_HARNESS`, `_run_ending_replay()` and
    # `test_the_ending_report_really_reaches_the_slot_the_re_render_rebuilt`,
    # carve lines 1833-2006, plus the docstring tail at 2028-2030 that named
    # the removed probe as the behaviour's owner — declared under `adapter
    # calls`, the class slice S5 already gave ten of those lines and the class
    # RULED OQ-1's CLOSED vocabulary leaves for a removal. That row has carried
    # `edits:` since S5, so `carrying` does not move: 2454 + 167 = 2621 on
    # the same 176 rows. The removed block spans 177 carve lines, but TEN of them
    # are slice S5's own declaration on this row and a line is declared once
    # per row — this sum counts line ENTRIES, and the pin below this comment
    # refuses a repeat for exactly that reason — so the entry carries 167 and
    # the row declares 196 distinct lines. The OTHER TWO suites are RETIRED rows and move neither
    # figure — `retired:` touches no `edits[]`, a retirement is a fact about a
    # DESTINATION, and the first-use pin below measures them.
    assert (lines, carrying) == (2621, 176), (lines, carrying)
    replicas = [row for row in doc["rows"]
                if row.get("reason") == MODULE.REPLICA_REASON]
    assert len(replicas) == 20, len(replicas)

    # THE ASK-7 WINDOW'S OWN FOUR LINES, PINNED BY ROW AND CLASS (Copilot
    # review, PR #995) — the aggregate above, `(1422, 158)` on the day this pin
    # was written, `(1761, 159)` at the RULED Q-L7 (a) amendment and
    # `(2621, 176)` today, would still pass if these four had
    # landed on the wrong rows, under the wrong class, or as a different four
    # line numbers that happened to sum to the same total. The dated figures are
    # kept beside the current one because the REASON this pin exists is what
    # that aggregate could not tell apart, and that reason is the same at
    # either total.
    # Named individually, on the same `(class, lines)` idiom the replica row's
    # check above already uses.
    cli_row = rows["scripts/ideation_dashboard/cli.py"]
    ask7_cli = [(edit["class"], edit["lines"]) for edit in cli_row["edits"]
                if edit["lines"] == [834]]
    assert ask7_cli == [("path constants", [834])], cli_row

    serve_row = rows["scripts/ideation_dashboard/serve.py"]
    ask7_serve = [(edit["class"], edit["lines"]) for edit in serve_row["edits"]
                  if edit["lines"] == [155, 725, 1338]]
    assert ask7_serve == [("path constants", [155, 725, 1338])], serve_row

    # THE § 3.4 SLICE-S8 ANNOTATION'S OWN FOURTEEN ENTRIES, PINNED BY ROW,
    # CLASS AND EXACT LINES — on the same reasoning as the ASK-7 and S3 pins:
    # the aggregate `(2621, 176)` would still pass if these forty lines had
    # landed on the wrong rows, under the wrong class, or as a different forty
    # that summed the same. Every one is `path constants` (a path literal
    # naming a location the destination does not have — this manifest's own
    # reading), and every one of the thirteen rows already carried an unrelated
    # edit, so each new entry is picked out by its lines exactly as
    # `test_bullseye_widget.py`'s S3 entry is.
    for source_path, expected in (
            ("tests/ideation-dashboard/test_outline_model.py", [22]),
            ("tests/ideation-dashboard/test_doxbench_view.py", [302, 303, 306]),
            ("tests/ideation-dashboard/test_doxbench_knowledge.py", [31, 32]),
            ("tests/ideation-dashboard/test_doxbench_document_abstract.py",
             [44, 45]),
            ("tests/ideation-dashboard/test_doxbench_memory_gateway.py",
             [32, 33]),
            ("tests/ideation-dashboard/test_bullseye_widget.py", [1674]),
            ("tests/ideation-dashboard/test_doxbench_mutation_boundary.py",
             [45, 46]),
            ("tests/ideation-dashboard/test_doxbench_save.py",
             [524, 525, 526, 1075, 1077]),
            ("tests/ideation-dashboard/test_doxbench_scope.py", [27, 28]),
            # The second push's five, four of them new sites and the first a
            # CORRECTION to the `mutation_boundary` entry above: re-running
            # `_check_declared_lines` against the leg head found the four
            # `Path` expressions REPLACED and not merely re-rooted.
            ("tests/ideation-dashboard/test_doxbench_mutation_boundary.py",
             [47, 48, 49, 51, 52, 55, 56, 57, 59, 60]),
            ("tests/ideation-dashboard/test_renderer.py", [610, 1078]),
            ("tests/ideation-dashboard/test_doxbench_abstract_store.py",
             [36, 46, 47]),
            ("tests/ideation-dashboard/test_doxbench_telemetry.py",
             [15, 22, 23]),
            ("tests/ideation-dashboard/test_doxbench_turns.py", [35, 103])):
        row = rows[source_path]
        assert row["disposition"] == "moved_with_declared_edit", row
        s8 = [(edit["class"], edit["lines"]) for edit in row["edits"]
              if edit["lines"] == expected]
        assert s8 == [("path constants", expected)], (source_path, row)
        note = s8 and [edit["note"] for edit in row["edits"]
                       if edit["lines"] == expected][0]
        assert "SLICE S8" in note, (source_path, note)
        assert "5649985838" in note, (source_path, note)

    # AND THE SLICE CARRIES NO RE-DESTINATION, asserted rather than left to the
    # summary line: S8 is the act RULED Q6 was built for, and it measured that
    # the move the note infers is unlawful for every one of the 48 files —
    # RULED on that measurement, `#656` comment `5656343213` (Brett Heap,
    # 2026-09-13, by interactive multi-choice): "the path constant moves, the
    # file does not". The S5 annotation's four rows therefore stay this
    # document's only uses of the field.
    re_destined = [row["source_path"] for row in doc["rows"]
                   if isinstance(row.get("re_destined"), dict)]
    assert all(path.startswith("scripts/ideation_dashboard/web/views/")
               for path in re_destined), re_destined

    # THE § 3.4 SLICE-S3 ANNOTATION'S OWN ROWS, PINNED BY DISPOSITION, CLASS
    # AND EXACT LINES (Copilot review, openxFactory PR #1001) — on the same
    # reasoning as the ASK-7 pin above: the aggregate assertion would still
    # pass if the `app.js` row's conversion, or either of its two edits,
    # landed on the wrong row, under the wrong class, or as different line
    # numbers that happened to sum to 37 — and likewise for the three-line
    # `test_bullseye_widget.py` addition. `app.js` carried no `edits:` at all
    # before THIS act, so its two entries are asserted exactly by picking
    # them out of the row's full list — the same idiom the ASK-7 checks
    # below use for `serve.py`, needed here too now that § 3.4 SLICE S4
    # (below) adds this row's third entry; `test_bullseye_widget.py` already
    # carried an unrelated `path constants` edit, so its new entry is picked
    # out by its lines the same way.
    app_js_row = rows["scripts/ideation_dashboard/web/app.js"]
    assert app_js_row["disposition"] == "moved_with_declared_edit", app_js_row
    # § 3.4 SLICE S5 adds this row's fourth and fifth entries (RULED Q10's
    # `firstEditTransport` through the registry, RULED counterpart Q6's two
    # model namespaces, and the call sites of RULED Q1/Q2/Q8/Q11), so they are
    # filtered out here the same way S4's were — this assertion is slice S3's.
    # § 3.4 SLICE S7 adds this row's sixth entry (RULED Q1/Q2/Q7's hop: the
    # facet read once per render and handed down as `ctx.display`), filtered out
    # the same way S4's and S5's are.
    s3_app_js = [(edit["class"], edit["lines"]) for edit in app_js_row["edits"]
                 if edit["lines"] not in ([514, 515, 1137, 1138],
                                          [45, 47, 48],
                                          APP_JS_S7_ADAPTER_CALLS)
                 and 749 not in edit["lines"]]
    assert s3_app_js == [
        ("import rewrites", [43]),
        ("adapter calls", [470, 471, 472, 475, 476, 480, 481, 482, 483, 484,
                            489, 521, 522, 523, 574, 579, 585, 587, 590, 599,
                            600, 602, 603, 604, 605, 606, 631, 640, 842, 843,
                            844, 865, 866, 876, 1102, 1103]),
    ], app_js_row

    bullseye_row = rows["tests/ideation-dashboard/test_bullseye_widget.py"]
    s3_bullseye = [(edit["class"], edit["lines"])
                   for edit in bullseye_row["edits"]
                   if edit["lines"] == [900, 1781, 1785]]
    assert s3_bullseye == [("adapter calls", [900, 1781, 1785])], bullseye_row

    # THE OPENDOX-CODE #14 FIX ROUND'S CATCH-UP, PINNED THE SAME WAY (openxFactory
    # #1001, extended after landing) — on the same reasoning as the two pins
    # above: the aggregate assertion would still pass if this line had landed
    # on the wrong row or under the wrong class. `test_doc_surfaces.py`
    # already carried an unrelated `path constants` edit (line 39), so its new
    # entry is picked out by its lines, the same idiom `test_bullseye_widget.py`
    # and `serve.py` use above.
    doc_surfaces_row = rows["tests/ideation-dashboard/test_doc_surfaces.py"]
    s3_doc_surfaces = [(edit["class"], edit["lines"])
                        for edit in doc_surfaces_row["edits"]
                        if edit["lines"] == [290]]
    assert s3_doc_surfaces == [("adapter calls", [290])], doc_surfaces_row

    # THE § 3.4 SLICE-S6 ANNOTATION, PINNED THE SAME WAY (RULED Q4, `#656`
    # comment `5642758731`) — on the same reasoning as the pins above: the
    # aggregate assertion would still pass if these lines had landed on the
    # wrong row, under the wrong class, or split across a different pair of
    # line counts that happened to sum to 132. Both rows already carried
    # `edits:` before this act, so each new entry is picked out by its exact
    # lines, the same idiom the ASK-7 and S3-catch-up pins above use.
    s6_serve = [(edit["class"], edit["lines"]) for edit in serve_row["edits"]
                if edit["lines"] == [161, 162, 304, 305, 515, 516, 921, 922,
                                      949, 950]]
    assert s6_serve == [("adapter calls",
                          [161, 162, 304, 305, 515, 516, 921, 922, 949,
                           950])], serve_row

    # THE RETIREMENT ACT'S ONE DECLARED EDIT, PINNED BY ROW, CLASS AND EXACT
    # LINES (RULED 5656343213) — on the same reasoning as every pin above, and
    # with one more: this entry is a REMOVAL filed under `adapter calls`
    # because the closed vocabulary has no class for one, so the row, the
    # class and the extent are the only record of what was taken out. The row
    # already carried three entries before this act.
    #
    # AND THE EXTENT IS PINNED IN TWO PIECES, BECAUSE A LINE IS DECLARED ONCE
    # PER ROW. The removed block spans 177 carve lines, and slice S5's ten
    # `adapter calls` lines sit INSIDE it on a row that already declared them.
    # The aggregate above SUMS LINE ENTRIES, so re-declaring the ten would
    # publish ten lines this act does not add while the row's declared SET
    # stayed the same -- the defect this very test's duplicate check refuses,
    # added by `#1030`'s review after this act was written and red at the
    # merge-forward. So this act's entry carries the other 167, and what the
    # LEG is held to is the UNION: `verify-carve-arrival.py` reads a row's
    # declarations as a set. Both halves and the union are asserted here, so
    # the record of what was taken out is no weaker for being in two entries.
    swb_test_row = rows["tests/ideation-dashboard/test_staging_workbench.py"]
    assert swb_test_row["disposition"] == "moved_with_declared_edit", \
        swb_test_row
    assert swb_test_row["destination"] == "openxdox_code", swb_test_row
    ending_replay = list(range(1833, 2007)) + [2028, 2029, 2030]
    assert len(ending_replay) == 177, len(ending_replay)
    s5_inside = [1895, 1896, 1897, 1898, 1900, 1906, 1907, 1918, 1926, 1928]
    this_act = [line for line in ending_replay if line not in set(s5_inside)]
    assert len(this_act) == 167, len(this_act)
    retirement_entry = [(edit["class"], edit["lines"])
                        for edit in swb_test_row["edits"]
                        if edit["lines"] == this_act]
    assert retirement_entry == [("adapter calls", this_act)], swb_test_row
    s5_entry = [(edit["class"], edit["lines"])
                for edit in swb_test_row["edits"]
                if edit["lines"] == s5_inside]
    assert s5_entry == [("adapter calls", s5_inside)], swb_test_row
    declared = {line for edit in swb_test_row["edits"]
                for line in edit["lines"]}
    assert set(ending_replay) <= declared, \
        sorted(set(ending_replay) - declared)

    serve_projection_row = rows[
        "scripts/ideation_dashboard/serve_projection.py"]
    s6_serve_projection_lines = [
        6, 7, 9, 12, 13, 14, 15, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
        60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
        77, 78, 79, 297, 298, 299, 300, 301, 302, 304, 305, 306, 307, 308,
        309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321,
        322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334,
        335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347,
        348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360,
        361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373,
        374, 375, 382, 383, 384, 385, 386, 387, 388]
    assert len(s6_serve_projection_lines) == 122, s6_serve_projection_lines
    s6_serve_projection = [
        (edit["class"], edit["lines"])
        for edit in serve_projection_row["edits"]
        if edit["lines"] == s6_serve_projection_lines]
    assert s6_serve_projection == [
        ("adapter calls", s6_serve_projection_lines)], serve_projection_row

    # THE § 3.4 SLICE-S4 ANNOTATION, PINNED THE SAME WAY (RULED Q3, `#656`
    # comment `5642758731`) — on the same reasoning as the pins above: the
    # aggregate assertion would still pass if these lines had landed on the
    # wrong row, under the wrong class, or split across a different set of
    # line counts that happened to sum to 380 over 5 new carriers.
    s4_app_js = [(edit["class"], edit["lines"]) for edit in app_js_row["edits"]
                 if edit["lines"] == [514, 515, 1137, 1138]]
    assert s4_app_js == [("adapter calls", [514, 515, 1137, 1138])], app_js_row

    lens_model_row = rows["scripts/ideation_dashboard/web/views/lens-model.js"]
    assert lens_model_row["disposition"] == "moved_with_declared_edit", \
        lens_model_row
    assert [(edit["class"], edit["lines"]) for edit in lens_model_row["edits"]] == [
        ("path constants", [1033, 1034, 1035, 1036, 1037]),
    ], lens_model_row

    lens_row = rows["scripts/ideation_dashboard/web/views/lens.js"]
    assert lens_row["disposition"] == "moved_with_declared_edit", lens_row
    lens_adapter_calls = (
        list(range(176, 183)) + list(range(211, 320)) + [1106, 1107, 1472, 1479])
    assert len(lens_adapter_calls) == 120, lens_adapter_calls
    assert [(edit["class"], edit["lines"]) for edit in lens_row["edits"]] == [
        ("import rewrites", [30]),
        ("adapter calls", lens_adapter_calls),
    ], lens_row

    repo_selector_row = rows[
        "scripts/ideation_dashboard/web/views/repo-selector.js"]
    assert repo_selector_row["disposition"] == "moved_with_declared_edit", \
        repo_selector_row
    repo_selector_path_constants = [6, 7, 8, 9, 10, 33, 36, 37, 39, 40, 41,
                                     42, 43, 44, 45, 46]
    repo_selector_adapter_calls = (
        [64, 65, 66, 67] + list(range(69, 78)) + list(range(189, 301))
        + [318] + list(range(357, 384))
        + [409, 577, 608, 609, 671, 672, 681, 682, 719]
        + list(range(779, 819)))
    assert len(repo_selector_path_constants) == 16, repo_selector_path_constants
    assert len(repo_selector_adapter_calls) == 202, repo_selector_adapter_calls
    assert [(edit["class"], edit["lines"]) for edit in repo_selector_row["edits"]] == [
        ("path constants", repo_selector_path_constants),
        ("adapter calls", repo_selector_adapter_calls),
    ], repo_selector_row

    staging_row = rows[
        "scripts/ideation_dashboard/web/views/staging-workbench-model.js"]
    # § 3.4 SLICE S7 adds this row's two last entries (the one sibling import,
    # and the whole class-A TAIL § 3.2 names — `SECTION_META`, the three scope
    # dispatches, and the corpus-area constants), filtered out the same way.
    s4_staging = [(edit["class"], edit["lines"])
                  for edit in staging_row["edits"]
                  if edit["lines"] != [544]
                  and edit["lines"] not in ([29], SWB_MODEL_S7_ADAPTER_CALLS)]
    staging_path_constants = [543] + list(range(814, 827))
    staging_adapter_calls = list(range(956, 964)) + list(range(985, 989))
    assert len(staging_path_constants) == 14, staging_path_constants
    assert len(staging_adapter_calls) == 12, staging_adapter_calls
    assert s4_staging == [
        ("path constants", staging_path_constants),
        ("adapter calls", staging_adapter_calls),
    ], staging_row

    swb_create_row = rows["scripts/ideation_dashboard/web/views/swb-create.js"]
    assert swb_create_row["disposition"] == "moved_with_declared_edit", \
        swb_create_row
    assert [(edit["class"], edit["lines"]) for edit in swb_create_row["edits"]] == [
        ("import rewrites", [32, 34]),
        ("path constants", [35]),
        # § 3.4 SLICE S5: RULED counterpart Q6 closes this contributed module's
        # reach into openDox's bundle to `./views/helpers.js`, and RULED Q3
        # gives it the one `mount(host, snapshot, ctx)` signature.
        ("import rewrites", [29, 30, 31, 33]),
        ("adapter calls", [162, 345, 346, 367, 368, 369, 370]),
    ], swb_create_row

    swb_session_row = rows[
        "scripts/ideation_dashboard/web/views/swb-session.js"]
    assert swb_session_row["disposition"] == "moved_with_declared_edit", \
        swb_session_row
    assert [(edit["class"], edit["lines"]) for edit in swb_session_row["edits"]] == [
        ("import rewrites", [76, 78]),
        ("path constants", [79]),
        # § 3.4 SLICE S5: RULED counterpart Q6 (the eighteen-name model import
        # goes, the nine functions arrive as `ctx.model`), RULED Q3's mount
        # signature, and RULED Q10's `firstEditTransport` reached through the
        # registry with the model the caller validated.
        ("import rewrites", [69, 70, 71, 72, 73, 74, 75, 77]),
        ("adapter calls",
         [161, 162, 163, 168, 177, 190, 191, 194, 195, 573, 574, 579, 582,
          596, 601, 609]),
    ], swb_session_row

    # THE PRE-EXISTING `openxdox_code` ANNOTATION, PINNED THE SAME WAY (`#656`
    # CLAIM `5656688910`) — on the same reasoning as every pin above: the
    # aggregate would still pass if these 48 lines had landed on the wrong
    # rows, under the wrong class, or split across a different set of counts
    # summing to 48. Each row carried `edits:` before this act, so every new
    # entry is picked out by its exact lines, the idiom the S3/S4/S6 pins use.
    # The conftest replica's entry is pinned with the rest of its row above.
    gate_console_row = rows["scripts/ideation_dashboard/gate_console.py"]
    # DISPOSITION AND DESTINATION PINNED TOO, on all three rows (Copilot
    # review, round 8). The `(class, lines)` assertions below would stay green
    # through a re-destination: `destination:` is the field
    # `verify-carve-arrival.py --destination openxdox_code` reads to decide
    # whether a row is its business at all, so a row re-destined to
    # `opendox_code` would carry these declarations to the OTHER leg with
    # every line still where this test looks for it — and `disposition:`
    # is what makes `edits:` legal on the row in the first place. Same form
    # as the S2 pins (`dispose.js`, `wheel.js`) above.
    assert gate_console_row["disposition"] == "moved_with_declared_edit", \
        gate_console_row
    assert gate_console_row["destination"] == "openxdox_code", gate_console_row
    preexisting_gate_console_adapters = [
        167, 168, 169, 170, 171, 826, 903, 968, 1012, 1135, 1150, 1151, 1154,
        1155, 1157, 1339, 1351, 1374, 1487, 1550, 1551, 1569, 1651, 2241]
    assert len(preexisting_gate_console_adapters) == 24, \
        preexisting_gate_console_adapters
    preexisting_gate_console = [
        (edit["class"], edit["lines"]) for edit in gate_console_row["edits"]
        if edit["lines"] in ([64, 65], preexisting_gate_console_adapters)]
    assert preexisting_gate_console == [
        # `from . import domain_profile`, inserted between :64 and :65 — BOTH
        # neighbours named, which is the form every insertion slice S5
        # declared at this destination already takes.
        ("import rewrites", [64, 65]),
        ("adapter calls", preexisting_gate_console_adapters),
    ], gate_console_row

    generator_row = rows["scripts/ideation_dashboard/generator.py"]
    assert generator_row["disposition"] == "moved_with_declared_edit", \
        generator_row
    assert generator_row["destination"] == "openxdox_code", generator_row
    preexisting_generator = [
        (edit["class"], edit["lines"]) for edit in generator_row["edits"]
        if edit["lines"] in ([326, 327, 348, 366, 891, 892, 893],
                             [76, 77, 78, 79, 80, 81, 438, 439, 456, 459])]
    assert preexisting_generator == [
        # TWO entries on one row, because they are two acts by two pull
        # requests: openXdox-code#14's two resolvers and their three call
        # sites, then #16's exclusion-check vocabulary. One entry, one commit.
        ("adapter calls", [326, 327, 348, 366, 891, 892, 893]),
        ("adapter calls", [76, 77, 78, 79, 80, 81, 438, 439, 456, 459]),
    ], generator_row

    test_generator_row = rows["tests/ideation-dashboard/test_generator.py"]
    assert test_generator_row["disposition"] == "moved_with_declared_edit", \
        test_generator_row
    assert test_generator_row["destination"] == "openxdox_code", \
        test_generator_row
    preexisting_test_generator = [
        (edit["class"], edit["lines"]) for edit in test_generator_row["edits"]
        if edit["lines"] in ([7, 8], [352, 353])]
    assert preexisting_test_generator == [
        # `from types import SimpleNamespace` is an insertion of NOTHING BUT an
        # import statement; the 76-line block beside :352/:353 is the new
        # tests, four of whose lines are function-local imports — the class of
        # an insertion is what the insertion IS.
        ("import rewrites", [7, 8]),
        ("adapter calls", [352, 353]),
    ], test_generator_row


def test_the_real_manifest_carries_the_s7_display_facet_declared_edits() -> None:
    """The § 3.4 slice-S7 window against the LANDED manifest, row by row.

    `test_the_real_manifest_carries_the_ruled_q_l7_amendment` above asserts the
    AGGREGATE `(2621, 176)`, and that pair would stay green if any of these 782
    lines had landed on the wrong row, under the wrong one of RULING OQ-1's
    three classes, or as a different set summing to the same total — which is
    why every slice since ASK-7 pins its own window. S7 edits THIRTY-THREE rows
    where S5 edited eleven, so the window is the `S7_WINDOW` table above rather
    than a run of hand-written asserts; it is the same claim, made once per row.

    THE ENTRIES ARE A CONTIGUOUS RUN, AND WERE EACH ROW'S LAST WHEN SLICE S7
    LANDED (amended by slice S8 in the merge that brought the two acts
    together — see § 1), because an annotation APPENDS to whatever the row
    already carried — sixteen of these rows were already
    `moved_with_declared_edit` from S1-S6 and seventeen are converted here — and
    a tail read positionally is a claim about ORDER too, which matching on prose
    would not be. The manifest is REQUIRED and not branched on: see
    `the_landed_manifest()`.
    """
    _text, doc = the_landed_manifest()
    rows = {row["source_path"]: row for row in doc["rows"]}

    # 1. EVERY ROW IN THE WINDOW, by disposition, destination and contiguous run.
    #
    # THE COUNT IS READ OFF THE TABLE'S OWN SOURCE FIRST, because `S7_WINDOW`
    # is a dict LITERAL and a dict literal collapses a repeated key at import,
    # keeping the last value (Copilot review, this pull request). A second
    # entry for a path already in the table is therefore invisible to every
    # assertion below — the imported object is byte-identical to the table the
    # author meant — and `len(S7_WINDOW) == 33` counts the SURVIVORS, so it is
    # a claim about the collapsed dict rather than about the 33 rows this act
    # declares. The duplicate survives in exactly one place, the text of the
    # literal, which is where it is now read: 33 key nodes, all distinct, and
    # the same set the imported table carries. That last line is what makes
    # the source read evidence about THIS table rather than about a copy of it
    # — a separately typed list of the same 33 paths would be a second
    # transcription, changed by the same hand in the same commit.
    #
    # `S7_CONVERTED` needs no such read and gets none: a LIST keeps its
    # duplicates, so § 2's `len(set(...)) == 17` sees them at run time.
    declared = dict_literal_keys(Path(__file__).resolve(), "S7_WINDOW")
    assert len(set(declared)) == len(declared), sorted(
        path for path in declared if declared.count(path) > 1)
    assert len(declared) == 33, len(declared)
    assert set(declared) == set(S7_WINDOW), \
        set(declared) ^ set(S7_WINDOW)
    for source_path, entries in S7_WINDOW.items():
        row = rows[source_path]
        assert row["disposition"] == "moved_with_declared_edit", row
        # Slice S7 is a ONE-LEG act: "parameterize class C" edits the served
        # bundle, and every file of it arrives at openDox-code. A window entry
        # landing on an `openxdox_code` row would be a different slice.
        assert row["destination"] == "opendox_code", row
        landed = [(edit["class"], edit["lines"]) for edit in row["edits"]]
        # AMENDED BY SLICE S8 IN THE MERGE THAT BROUGHT THE TWO ACTS TOGETHER
        # (openxFactory #1025, `#656` comment `5649985838`). This read
        # `landed[-len(entries):] == entries` — a TAIL — and a tail is only S7's
        # claim for as long as S7 is the newest act on all thirty-three rows.
        # It is not: this document is APPENDED TO IN LANDING ORDER (this
        # docstring says so), S7 lands first and S8 second, and S8 annotates
        # THREE of these rows — `test_bullseye_widget.py`,
        # `test_doxbench_view.py`, `test_outline_model.py` — so on those three a
        # tail read fails on a manifest in which nothing whatever is wrong.
        # Pinned as a CONTIGUOUS RUN OCCURRING EXACTLY ONCE, which keeps every
        # claim the tail made — these entries, under these classes, in this
        # order, adjacent, and not duplicated elsewhere on the row — and drops
        # only the accident of being last, which belongs to whichever slice
        # annotated the row most recently and to no slice permanently.
        runs = [i for i in range(len(landed) - len(entries) + 1)
                if landed[i:i + len(entries)] == entries]
        assert len(runs) == 1, (source_path, landed, entries)
        # AND THE ROW'S DECLARED LINES ARE DISTINCT (Copilot review, this pull
        # request). § 3 below sums `len(nums)` — LIST ENTRIES — and nothing
        # under this act refuses a repeated line number: the validator's
        # `edits[].lines` check requires a non-empty list of positive integers
        # and says nothing about repetition, and the arrival verifier reads a
        # row's declarations as a SET (`_declared_line_set`), so the duplicate
        # vanishes exactly where it would otherwise be caught. An entry naming
        # one line TWICE in place of naming two would therefore keep the 782,
        # keep the equality above and keep every per-class figure, while one
        # really edited line went undeclared — and an undeclared edit is
        # refused at the DESTINATION, an act later, as `arrival-undeclared-
        # edit`. The claim is made over the WHOLE row rather than over S7's
        # tail alone: a line this act declares that an earlier act already
        # declared on the same row is the same double count, one act apart.
        flat = [number for edit in row["edits"] for number in edit["lines"]]
        assert len(set(flat)) == len(flat), (source_path, sorted(
            number for number in flat if flat.count(number) > 1))

    # 2. THE SEVENTEEN CONVERSIONS, named. A conversion moves BOTH disposition
    # counts and the carrier count at once, so an act that converted a row it
    # did not mean to would still sum correctly; and a converted row carried no
    # `edits:` before this act, so S7's entries are its ONLY entries.
    assert len(S7_CONVERTED) == 17, len(S7_CONVERTED)
    # SEVENTEEN DISTINCT ROWS, not merely a list seventeen long (Copilot
    # review, this PR): a DUPLICATED path could stand in for an OMITTED
    # conversion, and the length above, the subset check below and the
    # per-row loop after it would every one of them still pass — while § 3's
    # `159 + len(S7_CONVERTED) == 176` counted the same row twice and the
    # omitted row's conversion went unasserted. Uniqueness is what makes the
    # count a claim about rows rather than about list length.
    assert len(set(S7_CONVERTED)) == 17, sorted(
        path for path in S7_CONVERTED if S7_CONVERTED.count(path) > 1)
    assert set(S7_CONVERTED) <= set(S7_WINDOW), \
        set(S7_CONVERTED) - set(S7_WINDOW)
    for source_path in S7_CONVERTED:
        row = rows[source_path]
        assert [(edit["class"], edit["lines"]) for edit in row["edits"]] == \
            S7_WINDOW[source_path], row

    # 3. THE WINDOW'S OWN TOTALS, summed rather than transcribed — the figures
    # the runbook's § 2 paragraph and this pull request's body both state.
    lines = sum(len(nums) for entries in S7_WINDOW.values()
                for _class, nums in entries)
    entries_count = sum(len(entries) for entries in S7_WINDOW.values())
    by_class: dict[str, int] = {}
    for entries in S7_WINDOW.values():
        for edit_class, nums in entries:
            by_class[edit_class] = by_class.get(edit_class, 0) + len(nums)
    assert (lines, entries_count) == (782, 48), (lines, entries_count)
    assert by_class == {"import rewrites": 14, "path constants": 4,
                        "adapter calls": 764}, by_class
    # 1584 + 782 = 2366 and 159 + 17 = 176 — THE AGGREGATE AS SLICE S7 LANDED
    # IT, which is what a window total is: a DELTA against the document the
    # act found, and so a figure a later slice cannot move. The carrying half
    # is still the amendment test's own figure, because neither slice S8
    # (openxFactory #1025) nor the pre-existing `openxdox_code` annotation
    # (#1031) added a carrier; the line half is not — S8's forty carry it to
    # 2406, that annotation's forty-eight to the figure that test asserts and
    # the retirement act's one hundred and sixty-seven to this one, and that
    # test re-derives it rather than reading it here.
    assert 1584 + lines == 2366, lines
    assert 159 + len(S7_CONVERTED) == 176, len(S7_CONVERTED)

    # 4. THE FOUR ARRIVED SUITES NOBODY HAD RUN SINCE THE CARVE (`#656` comment
    # `5650335573` § 4), which slice S7 repaired in the same leg commit that
    # this window declares. They are named because a suite repaired but NOT
    # declared is the undeclared movement the floor exists to refuse, and the
    # three classes cannot tell a test file from a product file.
    for source_path in ("tests/ideation-dashboard/test_doc_surfaces.py",
                        "tests/ideation-dashboard/test_doxbench_tile_verbs.py",
                        "tests/ideation-dashboard/test_doxbench_view.py",
                        "tests/ideation-dashboard/test_bullseye_widget.py"):
        assert source_path in S7_WINDOW, source_path


def test_the_real_manifest_carries_the_q6_form_and_the_four_rows_s5_re_destines() -> None:
    """RULED Q6 against the LANDED manifest: the FORM, documented, and the
    FOUR ROWS § 3.4 slice S5 uses it for.

    AS FIRST LANDED this amendment re-destined nothing on purpose, on the
    expectation that slice S8 of the front-end boundary note would be the
    first act to use it, under its own claim and its own pull request. § 3.4
    slice S5 (`#656` CLAIM `5648073924`) used it FIRST instead, so this is now
    the assertion that the floor's gate holds FOUR re-destined rows, not zero,
    and that `test_the_real_manifest_carries_the_ruled_q_l7_amendment` above
    still reads the aggregate correctly around them — a re-destination is not
    an edit and moves neither of that test's two figures.

    THE HEADER IS ASSERTED TOO, because a form nobody can find in the document
    that carries it is a form the next author re-invents: the ruling, the field
    and the citation requirement are all read out of the manifest's own prose.
    The manifest is REQUIRED and not branched on: see `the_landed_manifest()`.
    """
    text, doc = the_landed_manifest()

    re_destined = [row for row in doc["rows"] if "re_destined" in row]
    assert [row["source_path"] for row in re_destined] == [
        "scripts/ideation_dashboard/web/views/dispose.js",
        "scripts/ideation_dashboard/web/views/gate.js",
        "scripts/ideation_dashboard/web/views/swb-create.js",
        "scripts/ideation_dashboard/web/views/swb-session.js",
    ], [row["source_path"] for row in re_destined]

    # EVERY ONE OF THE FOUR SAYS THE SAME THING, which is what makes the field a
    # form rather than four hand-written paragraphs: the carve placed a class-B
    # module in the shell, and RULED Q5 makes the gate loop a CONTRIBUTED column
    # whose bytes live at openXdox-code. The row keeps its own `destination` and
    # `destination_path` untouched — that is the whole reason the ruling made
    # this a FIELD instead of an edit — and the EFFECTIVE destination is what
    # the arrival verifier reads.
    for row in re_destined:
        name = row["source_path"].rsplit("/", 1)[1]
        assert row["destination"] == "opendox_code", row
        assert row["destination_path"] == f"src/opendox/web/views/{name}", row
        moved = row["re_destined"]
        assert moved["from"] == "opendox_code", row
        assert moved["from_path"] == f"src/opendox/web/views/{name}", row
        assert moved["to"] == "openxdox_code", row
        assert moved["to_path"] == f"src/openxdox/web/views/{name}", row
        assert "5648044785" in moved["ruling"], row
        assert "5648073924" in moved["ruling"], row   # the S5 CLAIM comment
        assert moved["note"].strip(), row

    assert "re_destined:" in text, "the header does not document the form"
    assert "RULED Q6" in text, text[:200]
    assert "5648044785" in text, "the header does not cite the ruling"

    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["re_destined"] == 4, done.stdout


def test_carved_reach_resolves_the_four_re_destined_rows_at_their_arrival() -> None:
    """`PRRT_kwDOTAvnrs6h1nYE`, pinned against the same four LANDED rows.

    `carved_reach.source()` used to resolve every MOVED row — re-destined or
    not — at its raw `destination`/`destination_path`. For the four rows the
    test above pins, that raw pair names `opendox_code`, the leg RULED Q6's
    form says the ruling VACATES; the effective arrival (`#656` comment
    `5648044785`) is `openxdox_code`. `sources_under()` builds every one of
    its answers on `source()`, so the dashboard compositor's sweep of
    `scripts/ideation_dashboard/web/views/` inherited the same defect — a link
    to a file the paired leg no longer carries, for all four rows.

    Both legs are required, materialized, for the reason every other test here
    that reads a MOVED row's real destination is: this asks about rows that
    moved, and only the legs a ruling actually moved them between can answer
    what `source()` names now.
    """
    _text, doc = the_landed_manifest()
    re_destined = [row for row in doc["rows"] if "re_destined" in row]
    assert len(re_destined) == 4, re_destined  # the same four, guarded again

    import carved_reach as carved_reach_direct

    carved_reach_direct.require()
    swept = carved_reach_direct.sources_under(
        "scripts/ideation_dashboard/web/views/")
    for row in re_destined:
        key = row["source_path"]
        moved = row["re_destined"]
        vacated = (carved_reach_direct.MOUNTS[row["destination"]]
                   / row["destination_path"])
        arrived = (carved_reach_direct.MOUNTS[moved["to"]] / moved["to_path"])
        assert arrived != vacated, row  # or the assertions below prove nothing

        resolved = carved_reach_direct.source(key)
        assert resolved == arrived, (
            f"{key}: source() must resolve re_destined.to/to_path (RULED Q6), "
            f"not the row's own vacated destination — got {resolved}")

        assert swept[key] == arrived, (
            f"{key}: sources_under() delegates to source(); a dashboard "
            f"compositor sweep must not link the vacated path either")


def test_a_retired_schema_is_a_finding_and_not_a_harness_failure(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """WHERE the cross-reference validator's retirement lands (Copilot review
    of PR #1032, round 2).

    Round 1 gave the refusal a name so it would stop being an `ImportError`
    at the caller. It was still a bare `RuntimeError`, and `main()` catches
    every `Exception` and prints `ERROR harness failure: …` with exit 2 —
    which says the tool broke. The tool did not break: it read the manifest,
    found that a ruling had DELETED the schema it validates against, and said
    so. That is a FINDING about the document set, so it is reported as one,
    through the same `Findings`/`report` pair as every other error, with the
    validator's own exit code 1 — and the two orchestrators are where it is
    caught, because `main()` has no `Findings` to put it in.
    """
    cross = _cross_reference_validator()
    message = ("a RULING has RETIRED the schema scratch.schema.yaml at its "
               "leg (RULED 5656343213)")

    def retired() -> None:
        raise cross.RetiredSchema(message)

    monkeypatch.setattr(cross, "build_registry", retired)

    for run_one in (lambda: cross.run_default(REPO_ROOT, False),
                    lambda: cross.run_path(REPO_ROOT / "ideation",
                                           REPO_ROOT, False)):
        capsys.readouterr()
        assert run_one() == 1
        printed = capsys.readouterr()
        assert "ERROR [schema-retired]" in printed.out, printed
        assert message in printed.out, printed
        assert "harness failure" not in printed.out + printed.err, printed


def test_the_real_manifest_carries_the_retirement_form_and_the_two_rows_it_retires() -> None:
    """RULED 5656343213 against the LANDED manifest: the FORM, documented, and
    the TWO ROWS its first use retires.

    AS FIRST LANDED (PR #1032) this amendment retired NOTHING, and the ZERO was
    the assertion — the precedent is RULED Q6 itself, which landed at PR #1011
    with the grammar, the gates and no re-destined row, and was used first by
    an act with its own claim and its own pull request. A floor amendment that
    landed WITH its first use could not be reviewed apart from it, and this
    test is what stopped the two from being quietly merged: the day a row
    carried `retired:`, the assertion failed and the author had to come here
    and say which act did it.

    THAT DAY IS THIS ACT (openxFactory PR #1043, `#656` CLAIM `5656690570`),
    so the assertion MOVED rather than being deleted — it now names the two
    rows, exactly as
    `test_the_real_manifest_carries_the_q6_form_and_the_four_rows_s5_re_destines`
    names S5's four, and the next author who retires a row comes here for the
    same reason.

    THE RULING'S THIRD SUITE IS ASSERTED ABSENT FROM THE FORM. RULED
    5656343213 retires three, and only the ENDING REPLAY inside
    `tests/ideation-dashboard/test_staging_workbench.py` goes from that third
    file — a PART of a file whose other tests drive surfaces `openxdox_code`
    has, so its row goes on arriving and carries no block. It is an ordinary
    declared edit instead, pinned by
    `test_the_real_manifest_carries_the_ruled_q_l7_amendment` above; here the
    assertion is that nobody later stretched `retired:` over it.

    THE HEADER IS ASSERTED TOO, because a form nobody can find in the document
    that carries it is a form the next author re-invents.

    THE MANIFEST IS REQUIRED AND NOT BRANCHED ON (Copilot review, this pull
    request). This test was written with `if not manifest.is_file(): assert
    True; return` -- a SIXTH copy of the seat idiom that `#1030`'s review had
    just removed from five tests in this module, reintroduced by an act written
    beside that cleanup rather than after it. `assert True` REPORTS A PASS, so
    a checkout that lost the file would turn this pin into a green no-op, and
    the pin's whole job is to fail the day a row carries `retired:`. It reads
    the document through `the_landed_manifest()`, where the absence is a
    FAILURE with a message naming the ceremony that authored the file -- the
    same seat `test_the_real_repository_answers_at_the_ruled_path` still holds,
    and must, because there the absence IS the subject.
    """
    text, doc = the_landed_manifest()
    rows = {row["source_path"]: row for row in doc["rows"]}

    surface = "scripts/ideation_dashboard/web/views/intent-feed.js"
    retired = [row for row in doc["rows"] if "retired" in row]
    assert [row["source_path"] for row in retired] == [
        "tests/ideation-dashboard/test_intent_tray_dom.py",
        "tests/ideation-dashboard/test_wheel_verbs_dom.py",
    ], [row["source_path"] for row in retired]

    # BOTH SAY THE SAME THING, which is what makes this a form rather than two
    # hand-written paragraphs: the suite ARRIVED at openDox-code, the surface
    # it NEEDED is `views/intent-feed.js` — the tray suite drove that module
    # and the wheel suite only loads it, which is why the grammar says NEEDED
    # (Copilot review, this pull request) — and a RULING deleted the arrival. The
    # row keeps every placement field and its own `edits[]` — that is the whole
    # reason the ruling made this a FIELD — and `at`/`at_path` are the row's
    # EFFECTIVE arrival, which for these two is their own destination pair
    # because RULED Q6 never moved them.
    #
    # AND EACH ROW'S EXISTING DECLARATION, by class and exact lines, because
    # "untouched" is the claim and a non-empty `edits:` is not that claim: a
    # later act could rewrite either entry and a truthiness check would go on
    # passing. These two are the lines the LEG rewrote while the file was
    # there, and a retirement does not reach them.
    untouched = {
        "tests/ideation-dashboard/test_intent_tray_dom.py":
            [("path constants", [30])],
        # TWO entries on this row, and the second is SLICE S7's (openxFactory
        # #1030 -> `b3a75537`, `adapter calls` at carve line 310), landed while
        # this act was open. The pin FAILED at the merge-forward and that is
        # the pin working: a truthiness check would have gone on passing. It is
        # updated and told which act moved it, never weakened. Lawful beside a
        # retirement, because `rows_for()` drops a retired row before the
        # destination is asked anything — the declaration is CARRIED, not
        # applied, which is exactly what "the row keeps its own `edits[]`" is
        # for.
        "tests/ideation-dashboard/test_wheel_verbs_dom.py":
            [("path constants", [26]), ("adapter calls", [310])],
    }
    for row in retired:
        name = row["source_path"].rsplit("/", 1)[1]
        assert row["disposition"] == "moved_with_declared_edit", row
        assert row["destination"] == "opendox_code", row
        assert row["destination_path"] == f"tests/{name}", row
        assert "re_destined" not in row, row
        block = row["retired"]
        assert block["at"] == row["destination"], row
        assert block["at_path"] == row["destination_path"], row
        assert "5656343213" in block["ruling"], row
        assert block["surface"] == surface, row
        assert block["note"].strip(), row
        assert [(edit["class"], edit["lines"]) for edit in row["edits"]] == \
            untouched[row["source_path"]], row

    # THE CLAIM THE WHOLE FORM RESTS ON, read out of the document rather than
    # trusted: the surface both rows cite is `not_moved` HERE, and under a
    # reason that means ABSENT AT THE LEGS rather than
    # `replicated_at_destination`, whose copies each leg places itself. This is
    # `carve-retired-surface-live`'s question, asked of the landed rows.
    surface_row = rows[surface]
    assert surface_row["disposition"] == "not_moved", surface_row
    assert surface_row["reason"] != MODULE.REPLICA_REASON, surface_row

    # THE THIRD SUITE: a part of a file is not a row, and carries no block.
    swb_test_row = rows["tests/ideation-dashboard/test_staging_workbench.py"]
    assert "retired" not in swb_test_row, swb_test_row

    assert "retired:" in text, "the header does not document the form"
    assert "5656343213" in text, "the header does not cite the ruling"
    assert "A FOURTH GRAMMAR EXTENSION" in text, text[:200]
    assert "TWO ROWS BELOW CARRY THE FIELD" in text, \
        "the header does not record the act that used the form"

    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["retired"] == 2, done.stdout


def test_carved_reach_refuses_the_two_landed_retired_rows() -> None:
    """The THIRD reader of the form, against the LANDED rows this act retires.

    The companion for RULED Q6 is
    `test_carved_reach_resolves_the_four_re_destined_rows_at_their_arrival`
    above; this is the retirement's, and the two are not the same assertion —
    a re-destination moves an answer, a retirement REFUSES one, and the
    failure this guards would be SILENT: `source()` can compute a perfectly
    well-formed path for a retired row, because the row keeps every field the
    carve wrote, and that path names a file the arrival verifier has just
    finished proving absent.

    THE REFUSAL HALF NEEDS NO MATERIALIZED LEG, and that is relied on rather
    than described. MEASURED at this revision in a checkout whose `openDox`
    and `openXdox` directories are EMPTY: all three callers driven below raise
    `CarveRowRetired` for both rows, while a non-retired moved row's
    `source()` raises `CarveReachUnavailable` in that same checkout. THE ORDER
    IS NOT THE SAME IN ALL THREE, and an earlier wording here said it was
    (Copilot review, this pull request, reading the claim through `module()`):
    `source()` refuses the retirement before it resolves a mount at all and
    `shed_relpath()` reads the row and stops, but `module()` calls `install()`
    FIRST and `install()` DOES probe both legs — it records a missing one on
    `sys.meta_path` rather than raising, deferring that error to an import of
    a name inside it, so the retirement is still the refusal a caller gets.
    What all three share is the OUTCOME, which is the property this case
    relies on: the refusal holds in a checkout whose submodules were never
    initialized — the state a retained consumer is most likely to be read in.
    SO NO PART OF IT RESOLVES A ROW IT IS NOT ABOUT. The sweep assertion this
    case first carried called `sources_under()`, which resolves every OTHER
    row under the prefix and therefore needs both legs materialized — the very
    dependency the paragraph above says this case does not have (Copilot
    review, this pull request). What it asserts now is the PREDICATE that
    sweep filters on, asked of these two rows; the sweep's own end-to-end
    behaviour is driven on controlled rows in
    `test_carved_reach_refuses_a_retired_row_by_name` above, where both arms
    can be controlled. That stub drives the same three callers on a generated
    document; this one asks the real rows.

    AND IT DOES NOT BRANCH ON THE MANIFEST'S ABSENCE — a SEVENTH copy of that
    idiom, caught one act after the sixth (Copilot review, this pull request).
    `#1030`'s review took `if not manifest.is_file(): assert True; return` out
    of five tests that read the landed document; `#1032`'s round 10 took it out
    of a sixth, the retirement seat, which had been authored beside that
    cleanup rather than after it; and this test — authored beside BOTH — arrived
    carrying it a seventh time. `assert True` REPORTS A PASS, so a checkout
    without the document would have turned the FIRST USE of the whole form into
    a green bar meaning "the check did not run". It reads through
    `the_landed_manifest()`, where the absence is a FAILURE.
    """
    import carved_reach as carved_reach_direct

    _text, doc = the_landed_manifest()
    retired = [row for row in doc["rows"] if "retired" in row]
    assert len(retired) == 2, [row["source_path"] for row in retired]

    for row in retired:
        key = row["source_path"]
        with pytest.raises(carved_reach_direct.CarveRowRetired) as caught:
            carved_reach_direct.source(key)
        # The sentence names the RULING and the SURFACE rather than the
        # filename, because a caller reading it needs to know what replaced
        # the thing it asked for, not that a path is missing.
        assert "5656343213" in str(caught.value), caught.value
        assert row["retired"]["surface"] in str(caught.value), caught.value
        # A SUBCLASS: a caller that already handles "at no destination" needs
        # no change on the day a row is first retired — which is today.
        assert isinstance(caught.value,
                          carved_reach_direct.ShedModuleHasNoDestination)
        for call in (carved_reach_direct.module,
                     carved_reach_direct.shed_relpath):
            with pytest.raises(carved_reach_direct.CarveRowRetired):
                call(key)

    # AND A SWEEP DOES NOT GO DOWN WITH THEM — asserted through the PREDICATE
    # the sweep filters on rather than by running one. `sources_under()` skips
    # a row where `retired_at(row)[1] is not None` and RESOLVES every other row
    # under the prefix, so a real sweep of `tests/ideation-dashboard/` would
    # drag a hundred moved rows, and their mounts, into a case that is about
    # two rows and deliberately needs no mount at all (Copilot review, this
    # pull request). The sweep's own behaviour is driven end-to-end on
    # controlled rows in `test_carved_reach_refuses_a_retired_row_by_name`
    # above; what the landed document owes is that these two rows answer the
    # question that sweep asks.
    for row in retired:
        assert carved_reach_direct.retired_at(row)[1] is not None, row
        assert carved_reach_direct.retired_at(row) == (
            row["retired"]["at"], row["retired"]["at_path"]), row


# --------------------------------------------------------------------------
# ONE DEFINITION OF A LINE, SHARED WITH THE ARRIVAL VERIFIER
# (RULED Q-L8 (c), Brett Heap 2026-09-10)
# --------------------------------------------------------------------------

ARRIVAL_SCRIPT = REPO_ROOT / "scripts" / "verify-carve-arrival.py"
SHARED_LINES = REPO_ROOT / "scripts" / "carve_lines.py"

# A line carrying U+2028 — FIVE lines to the floor, SIX to `str.splitlines()`.
# The shape of the two landed `openxdox_code` rows the ruling is about, in
# miniature; `tests/carve_arrival/test_verify_carve_arrival.py` drives the same
# shape through the arrival half of the floor.
EXOTIC_SOURCE = (
    "import alpha\n"
    "SEPARATOR = \"one line\u2028with U+2028 inside it\"\n"
    "KEEP = 3\n"
    "PATH = \"scripts/pkg/web\"\n"
    "TAIL = 5\n")

# Every byte string whose line count the two spellings must agree on, INCLUDING
# each separator `splitlines()` adds. `\r\n` and a lone `\r` are here because
# `\r` is CONTENT to this floor and a terminator to `splitlines()`, and the
# empty blob is here because the validator's old expression guarded it by hand.
LINE_COUNT_CORPUS = (
    b"", b"\n", b"\n\n", b"a", b"a\n", b"a\nb", b"a\nb\n",
    b"a\r\nb\r\n", b"a\rb", b"a\rb\n",
    "x\u2028y\n".encode("utf-8"), "x\u2028y".encode("utf-8"),
    b"x\x0by\n", b"x\x0cy\n", b"x\x1cy\n", b"x\x1dy\n", b"x\x1ey\n",
    "x\x85y\n".encode("utf-8"), "x\u2029y\n".encode("utf-8"),
    b"\xff\xfe not utf-8 at all\n",
    EXOTIC_SOURCE.encode("utf-8"),
)


def _load_arrival():
    """The ARRIVAL verifier as a module, by path, for the agreement tests.

    Loaded inside the cases that need it and not at import: this file's subject
    is the manifest validator, and the other tool is read only by the four
    cases below that are ABOUT the two agreeing.
    """
    spec = importlib.util.spec_from_file_location("verify_carve_arrival",
                                                  ARRIVAL_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _u2028_manifest(scratch: Scratch) -> tuple[dict[str, Any], str]:
    """Commit `exotic.py` into the carve surface; generate a manifest at it."""
    _write(scratch.repo, "scripts/pkg/exotic.py", EXOTIC_SOURCE)
    commit = commit_since_the_carve(scratch, "a line carrying U+2028",
                                    "scripts")
    doc = clean_manifest(scratch, commit)
    row = row_named(doc, "exotic.py")
    row["disposition"] = "moved_with_declared_edit"
    row["destination"] = "openxdox_code"
    row["destination_path"] = "src/openxdox/exotic.py"
    return doc, commit


def test_the_line_count_is_exactly_the_expression_the_validator_carried(
        ) -> None:
    """THE COUNT DOES NOT MOVE (RULED Q-L8 (c)).

    The manifest's 1422 line numbers AT THAT RULING — 1761 at the RULED
    Q-L7 (a) amendment, 2621 today, and every
    one of them still in this numbering — were written in the numbering this
    validator already used — `content.count(b"\\n")`, plus one for a file with
    no final newline — so the shared module had to adopt THAT definition rather
    than invent a third, or every declared line in the landed document would
    have needed re-declaring. The old expression is pinned here verbatim
    against the module, over a corpus that includes every separator
    `splitlines()` would have added, which is what makes "the numbering is
    unchanged" a measurement instead of a claim.
    """
    for content in LINE_COUNT_CORPUS:
        expected = (content.count(b"\n")
                    + (0 if not content or content.endswith(b"\n") else 1))
        assert MODULE.carve_lines.count(content) == expected, content
        assert len(MODULE.carve_lines.records(content)) == expected, content


def test_both_tools_reach_one_definition_of_a_line() -> None:
    """ONE MODULE OBJECT, not two implementations that agree today.

    The defect RULED Q-L8 (c) closes was not a disagreement anybody could see
    in review — `content.count(b"\\n")` and `str.splitlines()` both look
    correct in isolation and disagree only on files nobody reads by eye. So the
    fix is not "the two spellings now match", which the next edit undoes; it is
    that there is ONE implementation and both tools import it.
    """
    arrival = _load_arrival()
    assert MODULE.carve_lines is arrival.carve_lines
    assert MODULE.carve_lines.__name__ == "carve_lines"
    assert MODULE.carve_lines.count(EXOTIC_SOURCE.encode("utf-8")) == 5
    assert "`\\n`-terminated record" in MODULE.carve_lines.DEFINITION


def test_neither_tool_splits_lines_by_any_other_route() -> None:
    """The drift guard, read as SYNTAX and not as text.

    A second numbering added later — a `splitlines()` in a new refusal message,
    a `count(b"\\n")` in a new bound — is the defect coming back, and it would
    come back GREEN: every test above would still pass while the new site
    answered a different question. So both scripts are walked for any call that
    splits or counts lines, and the only file allowed to hold one is
    `scripts/carve_lines.py`. An AST walk and not a `grep`, on this file's own
    precedent for the refusal vocabulary: both docstrings NAME `splitlines()` —
    they must, because they explain what was wrong with it — and a text scan
    cannot tell prose from a call.
    """
    def line_splitters(path):
        found = []
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"),
                                       filename=str(path))):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute):
                continue
            first = node.args[0] if node.args else None
            literal = first.value if isinstance(first, ast.Constant) else None
            if func.attr == "splitlines":
                found.append(f"{path.name}:{node.lineno} .splitlines()")
            elif (func.attr in ("split", "rsplit", "count")
                  and literal in ("\n", b"\n", "\r\n", b"\r\n")):
                found.append(f"{path.name}:{node.lineno} "
                             f".{func.attr}({literal!r})")
        return found

    assert line_splitters(SCRIPT) == [], \
        "the manifest validator splits or counts lines outside carve_lines.py"
    assert line_splitters(ARRIVAL_SCRIPT) == [], \
        "the arrival verifier splits or counts lines outside carve_lines.py"
    # NON-VACUITY: the walk must see the definition where it IS.
    assert [entry.split(" ", 1)[1] for entry in line_splitters(SHARED_LINES)] \
        == [".split(b'\\n')"], line_splitters(SHARED_LINES)
    # And both tools must IMPORT it, rather than each having grown a private
    # helper spelled some way this walk would not object to.
    for path in (SCRIPT, ARRIVAL_SCRIPT):
        imported = {alias.name
                    for node in ast.walk(ast.parse(
                        path.read_text(encoding="utf-8")))
                    if isinstance(node, ast.Import)
                    for alias in node.names}
        assert "carve_lines" in imported, path


def test_the_bound_is_the_floors_line_count_on_a_u2028_bearing_blob(
        scratch: Scratch) -> None:
    """The validator's END of the agreement, through the documented invocation.

    `exotic.py` is five lines to the floor and six to `splitlines()`. A row
    declaring line 5 verifies; a row declaring line 6 — the number a
    `splitlines()`-numbered author would have written for `TAIL` — refuses as
    past the end of the file, NAMING the count. That refusal is what keeps the
    document and the destination in one numbering: a line the floor cannot
    express never reaches a leg as a declaration.
    """
    doc, commit = _u2028_manifest(scratch)
    row_named(doc, "exotic.py")["edits"] = [
        {"class": "path constants", "lines": [5],
         "note": "TAIL, the last line of a five-line file"}]
    scratch.write(doc)
    done = run(scratch, "--at", commit)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("OK "), done.stdout

    row_named(doc, "exotic.py")["edits"] = [
        {"class": "path constants", "lines": [6],
         "note": "what `splitlines()` calls TAIL"}]
    combined = refuses(scratch, doc, "carve-shape-invalid", "--at", commit)
    assert "names line 6" in combined, combined
    assert "carries 5 line(s)" in combined, combined


def test_the_two_tools_number_a_u2028_bearing_blob_identically(
        ) -> None:
    """THE AGREEMENT, asserted line by line on one blob.

    For every 1-based line of a U+2028-bearing file the arrival verifier's
    record N is the text between the Nth pair of `\\n`s and the validator's
    bound is the same N. The last two assertions are the NON-VACUITY: an
    agreement test on a file the two spellings already agreed about would pass
    against the very defect it exists to catch.
    """
    arrival = _load_arrival()
    raw = EXOTIC_SOURCE.encode("utf-8")
    records = arrival.carve_lines.text_records(raw)
    assert len(records) == MODULE.carve_lines.count(raw) == 5
    assert records == [
        "import alpha",
        "SEPARATOR = \"one line\u2028with U+2028 inside it\"",
        "KEEP = 3",
        "PATH = \"scripts/pkg/web\"",
        "TAIL = 5",
    ]
    # The reading the verifier used to take, and what it did to line 4.
    old = EXOTIC_SOURCE.splitlines()
    assert len(old) == 6
    assert old[3] == "KEEP = 3"
    assert records[3] == "PATH = \"scripts/pkg/web\""


def test_the_real_manifests_declared_lines_are_the_floors_lines() -> None:
    """RULED Q-L8 (c) against the LANDED manifest: NO ROW NEEDED RE-DECLARING.

    The ruling allows for the two U+2028 rows being "re-declared so their 6
    lines are appliable", and the measurement says they do not need to be:
    every declared line of both rows names, under the floor's definition,
    exactly the `import rewrites` or `path constants` text its class describes
    at `carve_commit`. It was the `splitlines()` reading that named unrelated
    text — so the numbering moved and the document did not.

    Read as a CENSUS and not as two spot checks: every row is measured, and the
    set whose two numberings disagree must be exactly the three the leg-3 memo
    names — one of which declares no line and so owed no leg anything. A fourth
    would be a row whose declarations nobody has checked. The manifest is
    REQUIRED and not branched on: see `the_landed_manifest()`.
    """
    _text, doc = the_landed_manifest()
    commit = doc["carve_commit"]

    def blob(path: str) -> bytes:
        done = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "cat-file", "blob",
             f"{commit}:{path}"], capture_output=True, check=False)
        assert done.returncode == 0, \
            f"{path} is not readable at {commit[:12]}: {done.stderr!r}"
        return done.stdout

    disagreeing = {}
    for row in doc["rows"]:
        raw = blob(row["source_path"])
        floor = MODULE.carve_lines.count(raw)
        unicode_reading = len(raw.decode("utf-8", "surrogateescape")
                              .splitlines())
        if floor != unicode_reading:
            disagreeing[row["source_path"]] = (floor, unicode_reading)
    assert disagreeing == {
        # `not_moved / stays_openxfactory_adapter` — declares no line, so no
        # leg ever asked it a line-numbered question.
        "tests/corpus-adapter/test_openxfactory_adapter.py": (521, 522),
        # The two `openxdox_code` rows carve leg 3 measured.
        "tests/ideation-dashboard/test_gate_console.py": (2364, 2367),
        "tests/ideation-dashboard/test_round_trip.py": (734, 738),
    }, disagreeing

    # The six lines, one by one: the class the row declares them under, and the
    # text at that line number under the floor's definition.
    expected = {
        ("tests/ideation-dashboard/test_gate_console.py", 870):
            ("import rewrites", "from ideation_dashboard import cli"),
        ("tests/ideation-dashboard/test_gate_console.py", 1627):
            ("path constants", "scripts/ideation_dashboard/cli.py gate"),
        ("tests/ideation-dashboard/test_gate_console.py", 1785):
            ("path constants", "scripts/ideation_dashboard/cli.py"),
        ("tests/ideation-dashboard/test_gate_console.py", 1786):
            ("path constants", "scripts/ideation_dashboard/cli.py"),
        ("tests/ideation-dashboard/test_gate_console.py", 1810):
            ("import rewrites", "from ideation_dashboard import cli"),
        ("tests/ideation-dashboard/test_round_trip.py", 728):
            ("path constants", "scripts/ideation_dashboard/round_trip.py"),
    }
    rows = {row["source_path"]: row for row in doc["rows"]}
    for (path, line), (edit_class, text) in expected.items():
        row = rows[path]
        classes = [edit["class"] for edit in row["edits"]
                   if line in edit["lines"]]
        assert classes == [edit_class], (path, line, classes)
        records = MODULE.carve_lines.text_records(blob(path))
        assert text in records[line - 1], (path, line, records[line - 1])
        # And the reading that used to be the destination's: a different line.
        old = blob(path).decode("utf-8", "surrogateescape").splitlines()
        assert text not in old[line - 1], (path, line, old[line - 1])


def test_loading_either_tool_by_path_twice_does_not_grow_sys_path() -> None:
    """The shared-module import is GUARDED, and stays guarded (#907 review).

    Both tools are hyphenated entry points, so both are loaded by
    `spec_from_file_location` rather than imported — this file loads the
    validator at import and the arrival verifier in four cases, and
    `tests/carve_arrival/` loads the verifier again. An unguarded
    `sys.path.insert(0, <scripts>)` prepends one entry PER LOAD, and a
    duplicated leading entry moves import precedence for everything that runs
    after it in the session. The fix is one `if`; this is the assertion that
    keeps it, on `scripts/proposal-support.py`'s idiom.
    """
    scripts_dir = str((REPO_ROOT / "scripts").resolve())
    before = sys.path.count(scripts_dir)
    assert before >= 1, "loading the validator should have put scripts/ on the path"
    _load()
    _load_arrival()
    _load()
    assert sys.path.count(scripts_dir) == before, sys.path[:5]


# --------------------------------------------------------------------------
# `_git()`'s sanitized environment and `--no-replace-objects` (register item,
# `#656` comment `5638315691`)
# --------------------------------------------------------------------------
#
# The three tests below are the one deliberate exception to "EVERY
# behavioural test here goes through the subprocess" in the module docstring:
# they are white-box tests of `_git()`'s own wiring — not of the CLI's
# declared exit-code/output contract — the same shape as
# `tests/hermes_runtime_contracts/test_content_resolution.py::
# test_sanitized_git_environment_removes_redirects_and_command_scope_config`,
# which pins the sibling copy in `scripts/hermes_runtime_validation/
# content.py`. `resolve_revision`, `tree_at` and the `cat-file blob`/
# `merge-base --is-ancestor` reads all go through this one helper, so hardening
# it once covers every git read the validator makes.

def test_git_helper_runs_with_no_replace_objects_and_a_sanitized_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Hostile values mirror `test_content_resolution.py`'s sanitized-
    environment test exactly, because both pin the same scrub list."""
    hostile = {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": "hostile-alternates",
        "GIT_COMMON_DIR": "hostile-common-dir",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_PARAMETERS": "'core.bare=true'",
        "GIT_DIR": "hostile-git-dir",
        "GIT_INDEX_FILE": "hostile-index",
        "GIT_OBJECT_DIRECTORY": "hostile-objects",
        "GIT_REPLACE_REF_BASE": "refs/hostile/replace/",
        "GIT_WORK_TREE": "hostile-work-tree",
        "GIT_CONFIG_KEY_0": "core.bare",
        "GIT_CONFIG_VALUE_0": "true",
        "GIT_CONFIG_KEY_37": "core.worktree",
        "GIT_CONFIG_VALUE_37": "hostile-work-tree",
    }
    for name, value in hostile.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "hostile-global-config")
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", "hostile-system-config")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "0")

    captured: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        captured["argv"] = argv
        captured["env"] = kwargs.get("env")
        return subprocess.CompletedProcess(argv, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(subprocess, "run", fake_run)

    MODULE._git(tmp_path, "rev-parse", "--verify", "--quiet", "HEAD")

    assert captured["argv"] == [
        "git", "--no-replace-objects", "-C", str(tmp_path),
        "rev-parse", "--verify", "--quiet", "HEAD",
    ], "--no-replace-objects must precede the subcommand, not follow it"

    env = captured["env"]
    assert env is not None, "_git must pass an explicit env, not inherit one"
    assert hostile.keys().isdisjoint(env)
    assert env["GIT_CONFIG_GLOBAL"] == os.devnull
    assert env["GIT_CONFIG_SYSTEM"] == os.devnull
    assert env["GIT_CONFIG_NOSYSTEM"] == "1"
    assert env["GIT_NO_REPLACE_OBJECTS"] == "1"


def test_git_helper_delegates_to_carved_reachs_sanitized_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Proof of DELEGATION, not agreement-by-coincidence: stub
    `carved_reach._sanitized_git_environment` to return a distinctive
    sentinel and show `MODULE._git` hands that exact object to
    `subprocess.run` as `env=`. `MODULE.carved_reach` is asserted to be the
    SAME module object a plain `import carved_reach` gives everywhere else in
    this repository (`tests/conftest.py` among them), which pins that the
    validator did not vendor a private copy of the module."""
    import carved_reach as carved_reach_direct

    assert MODULE.carved_reach is carved_reach_direct, (
        "the validator must import the real carved_reach module, not a copy")

    sentinel_env = {"SENTINEL_MARKER": "carved-reach-sanitized-env"}
    monkeypatch.setattr(carved_reach_direct, "_sanitized_git_environment",
                        lambda: sentinel_env)

    captured: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        captured["env"] = kwargs.get("env")
        return subprocess.CompletedProcess(argv, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(subprocess, "run", fake_run)

    MODULE._git(tmp_path, "rev-parse", "HEAD")

    assert captured["env"] is sentinel_env


def test_the_git_environment_scrub_list_agrees_across_content_and_carved_reach() -> None:
    """`scripts/carved_reach.py` and `scripts/hermes_runtime_validation/
    content.py` each carry their OWN copy of the ambient-git-environment scrub
    list — `carved_reach`'s own comment says to "keep the two lists equal if
    either changes", duplicated rather than imported because `content` is
    loaded dotted and `carved_reach` bare, at a call site where the dotted
    import would fail. Nothing enforced that agreement before this test. This
    validator does not add a THIRD copy — it delegates to `carved_reach`
    (pinned by the test above) — so what remains to pin here is that the two
    sites which DO still hand-carry the list have not drifted apart."""
    content = importlib.import_module("scripts.hermes_runtime_validation.content")
    import carved_reach as carved_reach_direct

    assert (carved_reach_direct._SCRUBBED_GIT_ENVIRONMENT
            == content._SCRUBBED_GIT_ENVIRONMENT)
    assert (carved_reach_direct._INDEXED_GIT_CONFIG_ENVIRONMENT.pattern
            == content._INDEXED_GIT_CONFIG_ENVIRONMENT.pattern)
