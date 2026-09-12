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
    "carve-shed-incomplete",
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


def test_the_real_manifest_carries_the_ruled_q_l7_amendment() -> None:
    """RULED Q-L7 (a) against the LANDED manifest, not a generated one.

    The two rows the ruling names, read out of the real document: a moved row
    that is ALSO replicated at `openxdox_code`, and a replica row declaring the
    one line its copies must differ on. A BRANCH and never a skip, on the
    module docstring's reasoning — before the § 6 ceremony there is no manifest
    to read.
    """
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        assert True
        return
    doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    rows = {row["source_path"]: row for row in doc["rows"]}

    moved = rows["tests/ideation-dashboard/session_fixtures.py"]
    assert moved["disposition"] == "moved_with_declared_edit", moved
    assert moved["destination"] == "opendox_code", moved
    assert moved["also_replicated_to"] == ["openxdox_code"], moved

    replica = rows["tests/ideation-dashboard/conftest.py"]
    assert replica["disposition"] == "not_moved", replica
    assert replica["reason"] == MODULE.REPLICA_REASON, replica
    assert [(edit["class"], edit["lines"]) for edit in replica["edits"]] == \
        [("path constants", [25])], replica

    # The ruling's own pairing: the replica IMPORTS the moved row's module
    # unconditionally, which is why one amendment carries both.
    assert "session_fixtures" in replica["evidence"], replica

    # And the counts this amendment moved, re-derived from the file rather than
    # transcribed: one more declared line than the 793 the runbook's § 2 table
    # carried before it, on one more row than the 146 that carried edits — and
    # then the Q-L1 ANNOTATIONS of 2026-09-10 (`#656` comment `5628560136`,
    # landed with the § 5.2 shed) moved both again, by 68 lines over seven rows,
    # three of which carried no `edits:` before. 794 + 68 = 862 on 147 + 3 = 150
    # rows. Then the ASK-7 DECLARED-EDIT WINDOW of 2026-09-11 (`#656` comment
    # `5635150678`, ASK-7 → 1) added 4 more declared lines to two rows that
    # ALREADY carried `edits:` — the cli.py and serve.py docstring/comment
    # lines — so `carrying` does not move: 862 + 4 = 866 on the same 150 rows.
    # Re-derived here for the same reason as before: a transcribed count is a
    # claim, a summed one is a measurement.
    lines = sum(len(edit["lines"]) for row in doc["rows"]
                for edit in row.get("edits") or [])
    carrying = sum(1 for row in doc["rows"] if row.get("edits"))
    assert (lines, carrying) == (866, 150), (lines, carrying)
    replicas = [row for row in doc["rows"]
                if row.get("reason") == MODULE.REPLICA_REASON]
    assert len(replicas) == 20, len(replicas)

    # THE ASK-7 WINDOW'S OWN FOUR LINES, PINNED BY ROW AND CLASS (Copilot
    # review, PR #995) — the aggregate `(866, 150)` above would still pass if
    # these four had landed on the wrong rows, under the wrong class, or as a
    # different four line numbers that happened to sum to the same total.
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

    The manifest's 862 line numbers were written in the numbering this
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
    would be a row whose declarations nobody has checked. A BRANCH and never a
    skip, on the module docstring's reasoning.
    """
    manifest = REPO_ROOT / MODULE.MANIFEST_RELPATH
    if not manifest.is_file():
        assert True
        return
    doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
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
