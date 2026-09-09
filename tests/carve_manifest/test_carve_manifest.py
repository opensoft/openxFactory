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


def test_an_at_that_resolves_elsewhere_still_refuses(scratch: Scratch) -> None:
    refuses(scratch, clean_manifest(scratch, scratch.first),
            "carve-revision-mismatch", "--at", scratch.head)


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
