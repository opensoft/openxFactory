"""`scripts/verify-openxdox-pin.py`: the positive, all five refusals, and the
one thing this verifier deliberately does NOT check.

Modelled on `tests/openxwallet_pin/test_verify_pin.py`, which is this
repository's standing shape for a pin verifier's suite, and departing from it
only where the artifact departs: five `openxdox-`prefixed codes instead of the
wallet's ratified six, ONE whole-tree `sorted-ls-tree-r-v1` digest instead of a
per-file loop, and no `--aggregation-root` mode.

THE POSITIVE IS ADJUDICATED AGAINST THE REAL REPOSITORY ROOT, and one assertion
here cannot be moved into a fixture. `test_the_shipped_digest_is_recomputed_by
_an_independent_implementation` re-derives `sorted-ls-tree-r-v1` from the
definition written in `contracts/openxdox-pin.yaml`'s own comment block —
locally, in this file, without calling `MODULE.tree_digest` — and compares the
result against the digest the shipped pin records. A fixture proves the
mechanism; the mechanism agreeing with itself says nothing about whether the
digest in the shipped pin is the digest of the shipped submodule, and a
verifier that recomputes a value with the same function that produced it would
pass on a pin computed by a subtly wrong algorithm.

THE FIVE REFUSALS ARE ADJUDICATED IN AN ISOLATED SCRATCH TREE. `_scratch`
builds a throwaway superproject under `tmp_path` holding a real nested git
repository at `openXdox` — including a nested `160000` gitlink of its own, so
the "a leg moving inside openXdox is drift too" claim is provable rather than
asserted — a `.git` POINTER FILE, a fabricated gitlink in the superproject, and
a pin whose `commit` and `tree_sha256` are the nested repository's actual HEAD
and actual digest. So the positive path is reachable in the fixture and every
negative is ONE mutation away from it.
`test_the_scratch_fixture_is_a_positive_before_it_is_mutated` runs first for
exactly that reason: a fixture that refused for some incidental reason would
let every negative below pass while proving nothing about the code it names.

NOTHING IS SKIPPED, AND THAT IS A DESIGN CONSTRAINT RATHER THAN A PREFERENCE.
A `pytest.skip` reports as a green bar, indistinguishable from a pass to every
reader and every gate — and "a check that cannot be reached reports as
satisfied" is the entire class of defect the pin, the verifier and this suite
exist to close. It is also arithmetic: `pytest-suite` pins `EXPECT_SKIPPED`
exactly, so a conditionally-skipped test here would red the required check on
every tree that skipped it. Every case is hermetic: no network, no ambient git
identity, no ambient git config, and no dependence on any object not created
inside `tmp_path` — except the handful of cases that deliberately read the real
repository, each named as doing so.

THE GIT ENVIRONMENT IS PINNED, NOT INHERITED (`_hermetic_git`), on the wallet
suite's reasoning unchanged: CI runners have no ambient git identity, so a
scratch `git commit` there dies with "Author identity unknown" while passing on
a developer's machine, and a developer's GLOBAL config can carry
`core.hooksPath` or `commit.gpgsign`, either of which runs or refuses inside a
throwaway repository. Both directions are the same defect — the ambient
installation must not change the answer. The env vars go on `os.environ`
through `monkeypatch` rather than into a private `env=` dict because the
VERIFIER shells out to `git` itself; an env this file kept to itself would
leave the calls under test reading the host's config.
"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFIER = REPO_ROOT / "scripts" / "verify-openxdox-pin.py"
PIN_PATH = REPO_ROOT / "contracts" / "openxdox-pin.yaml"

# The vocabulary, restated as a LITERAL rather than imported. Asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology; spelling
# the five out is what makes a silent reorder or rename a test failure. The
# codes are the thing a consumer gate branches on, and task 5.3 (Phase 5) is
# about to become that consumer, so they are fixed here BEFORE anything reads
# them rather than after.
OPENXDOX_CODES = (
    "openxdox-pin-tag-only",
    "openxdox-pin-submodule-uninitialized",
    "openxdox-pin-gitlink-mismatch",
    "openxdox-pin-checkout-mismatch",
    "openxdox-pin-digest-mismatch",
)


def _load():
    """The verifier as a module.

    Loaded by path because `scripts/verify-openxdox-pin.py` is a hyphenated file
    name and therefore not importable — the same reason
    `tests/openxwallet_pin/test_verify_pin.py` loads its own subject this way.
    The import must be SIDE-EFFECT-FREE beyond the module constants, so a
    regression that put I/O at import time surfaces here as a collection error.
    """
    spec = importlib.util.spec_from_file_location("verify_openxdox_pin",
                                                  VERIFIER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MODULE = _load()


# --------------------------------------------------------------------------
# the hermetic git environment
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _hermetic_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """No global config, no system config, and a deterministic identity."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "openxdox-pin-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "pin-test@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "openxdox-pin-test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "pin-test@example.invalid")


def _git_raw(root: Path, *args: str) -> subprocess.CompletedProcess:
    """git, without asserting success — for calls that are EXPECTED to fail."""
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    done = _git_raw(root, *args)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr}"
    return done


def _identify(root: Path) -> None:
    """Repository-LOCAL identity, because a call may not carry `-c`."""
    _git(root, "config", "user.name", "openxdox-pin-test")
    _git(root, "config", "user.email", "pin-test@example.invalid")


def _independent_tree_digest(repo: Path, revision: str) -> str:
    """`sorted-ls-tree-r-v1`, re-derived here from the pin's own prose.

    DELIBERATELY NOT `MODULE.tree_digest`. This is the second implementation
    that makes the shipped digest a measured fact rather than a self-consistent
    one; if the two ever disagree, one of them is wrong and the suite says so
    instead of both agreeing on the same mistake.

    The definition, quoted from `contracts/openxdox-pin.yaml`:
        records = `git ls-tree -r -z <commit>` split on NUL, empties dropped
        sort the records bytewise ascending
        digest  = sha256(b"".join(record + b"\\n" for record in records))
    """
    done = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z",
                           revision], capture_output=True, check=True)
    records = sorted(rec for rec in done.stdout.split(b"\x00") if rec)
    digest = hashlib.sha256()
    for record in records:
        digest.update(record)
        digest.update(b"\n")
    return digest.hexdigest()


# --------------------------------------------------------------------------
# the scratch superproject
# --------------------------------------------------------------------------

class Scratch:
    """A throwaway superproject that satisfies the pin, ready to be broken."""

    def __init__(self, root: Path, commit: str, parent_commit: str,
                 pin: dict) -> None:
        self.root = root
        self.sub = root / "openXdox"
        self.commit = commit
        self.parent_commit = parent_commit
        self.pin = pin
        self.pin_path = root / "contracts" / "openxdox-pin.yaml"

    def write_pin(self) -> None:
        self.pin_path.write_text(yaml.safe_dump(self.pin, sort_keys=False),
                                 encoding="utf-8")

    def record_gitlink(self, oid: str, *, commit: bool = True) -> None:
        """Fabricate the `160000` index entry, and optionally commit it.

        `--cacheinfo` writes the index entry without requiring the object to
        exist in this repository, which is what makes a disagreeing gitlink
        reproducible without a second real clone.
        """
        _git(self.root, "update-index", "--add", "--replace",
             "--cacheinfo", f"160000,{oid},openXdox")
        if commit:
            _git(self.root, "commit", "-q", "--allow-empty",
                 "-m", f"record openXdox at {oid}")

    def digest_at(self, revision: str) -> str:
        return _independent_tree_digest(self.sub, revision)


def _scratch(tmp_path: Path, *, record: str = "head") -> Scratch:
    """Build the positive fixture. `record` is "head", "index" or "none".

    "head"  the gitlink is committed, so `git ls-tree HEAD` answers.
    "index" the gitlink is staged and never committed — the state of a fresh
            `git submodule add`, in which the verifier must fall back to
            `git ls-files -s`.
    "none"  no gitlink anywhere, which must refuse rather than pass.

    THE NESTED REPOSITORY CARRIES A NESTED GITLINK OF ITS OWN, because openXdox
    is an assembly root whose `code` and `spec` legs are submodules and the pin
    file's central claim — that ONE digest covers a three-repository product
    without mounting the other two — is only checkable if the fixture has one.
    """
    root = tmp_path / "superproject"
    (root / "contracts").mkdir(parents=True)
    _git(root.parent, "init", "-q", "-b", "main", str(root))
    _identify(root)

    sub = root / "openXdox"
    sub.mkdir()
    _git(sub.parent, "init", "-q", "-b", "main", str(sub))
    _identify(sub)
    (sub / "contracts").mkdir()
    (sub / "README.md").write_text("# synthetic openXdox\n", encoding="utf-8")
    (sub / "contracts" / "manifest.yaml").write_text(
        "schema_version: 1\ncontract_bundle_version: none\nentries: []\n",
        encoding="utf-8")
    # The nested leg gitlink. `--cacheinfo` again: the leg's own object need
    # not exist for `ls-tree -r` to report the 160000 record, and reporting it
    # is the whole of what the digest consumes.
    _git(sub, "add", "-A")
    _git(sub, "update-index", "--add", "--cacheinfo",
         f"160000,{'a' * 40},code")
    _git(sub, "commit", "-q", "-m", "seed the assembly root and its leg")
    parent_commit = _git(sub, "rev-parse", "HEAD").stdout.strip()

    # A SECOND commit, so `openxdox-pin-checkout-mismatch` is reproducible by
    # pinning the FIRST while the checkout sits at the second — a real stale
    # checkout, with no write through the `.git` pointer and no fabricated
    # revision.
    (sub / "CHANGELOG.md").write_text("# changes\n", encoding="utf-8")
    _git(sub, "add", "-A")
    _git(sub, "commit", "-q", "-m", "add a changelog")
    commit = _git(sub, "rev-parse", "HEAD").stdout.strip()
    tree_sha256 = _independent_tree_digest(sub, commit)

    # Convert the nested `.git` DIRECTORY into the `gitdir:` POINTER FILE a real
    # submodule has. Every scratch test therefore also exercises the
    # `.exists()`-rather-than-`.is_dir()` choice in check 1, which is the check
    # that would otherwise refuse every correctly initialized submodule.
    modules = root / ".git" / "modules"
    modules.mkdir(parents=True, exist_ok=True)
    (sub / ".git").rename(modules / "openXdox")
    (sub / ".git").write_text(f"gitdir: {modules / 'openXdox'}\n",
                              encoding="utf-8")

    pin = {
        "schema_version": 1,
        "kind": "pinned_contract_manifest",
        "source_repository": "opensoft/openXdox",
        "submodule_path": "openXdox",
        "commit": commit,
        "revision_kind": "commit",
        "digest_algorithm": "sha256",
        "digest_definition": "sorted-ls-tree-r-v1",
        "digests": {"tree_sha256": tree_sha256},
        "carve_commit": "b" * 40,
        "resync_runbook": "openXdox/README.md#the-lockstep-invariant",
        "verify_pin": "scripts/verify-openxdox-pin.py",
    }

    scratch = Scratch(root, commit, parent_commit, pin)
    scratch.write_pin()
    if record == "head":
        scratch.record_gitlink(commit, commit=True)
    elif record == "index":
        scratch.record_gitlink(commit, commit=False)
    elif record != "none":  # pragma: no cover - fixture misuse
        raise AssertionError(f"unknown record mode {record!r}")
    return scratch


# --------------------------------------------------------------------------
# the vocabulary
# --------------------------------------------------------------------------

def test_refusal_codes_are_exactly_the_five_openxdox_codes_in_order() -> None:
    assert MODULE.REFUSAL_CODES == OPENXDOX_CODES


def test_pin_unreadable_is_not_in_the_vocabulary() -> None:
    """The sixth spelling names an ENVIRONMENT in which no finding is reachable.

    A consumer that enumerates the vocabulary must not be able to treat "we
    could not ask the question" as one of the answers to it.
    """
    assert "pin-unreadable" not in MODULE.REFUSAL_CODES
    assert len(MODULE.REFUSAL_CODES) == 5


def test_every_code_is_prefixed_so_a_consumer_can_tell_the_products_apart(
) -> None:
    """The prefix is the whole reason these are not the wallet's six by import.

    `verify-openxwallet-pin.py`'s codes are a ratified vocabulary and other code
    refuses BY CODE against it. Reusing those tokens here would make an openXdox
    refusal indistinguishable from a wallet refusal to anything branching on the
    string.
    """
    assert all(code.startswith("openxdox-pin-")
               for code in MODULE.REFUSAL_CODES)
    wallet = _load_wallet()
    assert set(MODULE.REFUSAL_CODES) & set(wallet.REFUSAL_CODES) == set()


def _load_wallet():
    spec = importlib.util.spec_from_file_location(
        "verify_openxwallet_pin_probe",
        REPO_ROOT / "scripts" / "verify-openxwallet-pin.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_the_remediation_trailer_scopes_the_init_and_names_the_procedure(
) -> None:
    """`--recursive` must stay ABSENT, and the procedure must be nameable.

    openXdox's own `code`/`spec` legs are not consumed here, so a remediation
    that recursed would pull a three-repository tree into a job with business in
    exactly one of them — the same scoped-init discipline the wallet trailer
    states.
    """
    assert "git submodule update --init openXdox" in MODULE.REMEDIATION
    assert "NOT --recursive" in MODULE.REMEDIATION
    assert "update --init --recursive" not in MODULE.REMEDIATION
    assert "openXdox/README.md#the-lockstep-invariant" in MODULE.REMEDIATION


def test_the_digest_constants_are_the_family_spelling() -> None:
    """One definition, spelled the way the rest of the carve's pins spell it."""
    assert MODULE.DIGEST_DEFINITION == "sorted-ls-tree-r-v1"
    assert MODULE.DIGEST_ALGORITHM == "sha256"
    assert MODULE.GITLINK_MODE == "160000"


def test_there_is_no_aggregation_root_mode_and_the_absence_is_deliberate(
) -> None:
    """`opensoft/xFactory` records no openXdox gitlink, so the mode would refuse
    by construction. Asserted so the absence reads as a decision rather than an
    oversight, and so re-adding it is a deliberate act with a test to update."""
    assert not hasattr(MODULE, "verify_aggregation")
    with pytest.raises(SystemExit) as caught:
        MODULE.main(["--aggregation-root", "/nonexistent"])
    assert caught.value.code == 2


# --------------------------------------------------------------------------
# the positive, against the real repository
# --------------------------------------------------------------------------

def test_the_real_pin_is_satisfied() -> None:
    """The shipped pin is a fact about the shipped submodule, not a claim."""
    pin = MODULE.verify()
    assert pin["revision_kind"] == "commit"
    assert len(pin["commit"]) == 40
    assert pin["source_repository"] == "opensoft/openXdox"
    assert pin["submodule_path"] == "openXdox"
    assert pin["digest_definition"] == "sorted-ls-tree-r-v1"


def test_the_shipped_digest_is_recomputed_by_an_independent_implementation(
) -> None:
    """The one assertion in this file that cannot be moved into a fixture.

    Re-derives `sorted-ls-tree-r-v1` locally, from the definition written in the
    pin's own comment block, and compares against the digest the pin records —
    so a pin computed by a subtly wrong algorithm fails here even though the
    verifier, using that same wrong algorithm, would agree with itself.
    """
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    recomputed = _independent_tree_digest(REPO_ROOT / "openXdox",
                                          pin["commit"])
    assert recomputed == pin["digests"]["tree_sha256"]
    # ...and the verifier's own implementation agrees with the independent one.
    assert MODULE.tree_digest(REPO_ROOT / "openXdox",
                              pin["commit"]) == recomputed


def test_the_pinned_commit_is_a_real_object_in_the_submodule() -> None:
    """`docs/opendox-cutover-runbook.md` § 7's "the pin names a real object".

    git records a gitlink WITHOUT checking the object exists, so a wrong pin
    commits and pushes clean; only a `cat-file` in the submodule catches it.
    """
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    done = _git(REPO_ROOT / "openXdox", "cat-file", "-t", pin["commit"])
    assert done.stdout.strip() == "commit"


def test_the_gitlink_the_tree_records_equals_the_pin() -> None:
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    recorded, source = MODULE._recorded_gitlink(REPO_ROOT, "openXdox")
    assert recorded == pin["commit"]
    assert source == "HEAD"


def test_the_real_submodule_dot_git_is_a_file_not_a_directory() -> None:
    """Check 1 must use `.exists()`; this is why.

    A submodule's `.git` is a FILE holding a `gitdir:` pointer, so `.is_dir()`
    is False for the shipped tree and an `.is_dir()` check would refuse the very
    state it exists to accept. Asserted against the real checkout so the claim
    is about the world and not about the fixture.
    """
    dot_git = REPO_ROOT / "openXdox" / ".git"
    assert dot_git.exists()
    assert not dot_git.is_dir()


def test_ruling_q7_two_direct_upstreams_in_lockstep() -> None:
    """RULING F, SUPERSEDED FOR OPENDOX ONLY BY RULED Q7 — as a test.

    This test used to be `test_ruling_f_is_checkable_no_opendox_pin_and_no_
    second_gitlink`, asserting RULING F (Brett Heap, `opensoft/openxFactory
    #656`, 2026-09-05, "rule F openXdox only"): that openxFactory pinned
    openXdox and NOTHING ELSE, carrying no `contracts/opendox-pin.yaml` and no
    second gitlink, with openDox's commit read only as a value DERIVED through
    openXdox's own pin. Brett Heap's Q7 ruling (`#656` comment `5626248666`,
    2026-09-10) supersedes that sentence FOR OPENDOX ONLY, verbatim: *"RULED
    (i): SECOND SUBMODULE — openxFactory mounts the openDox assembly root
    (gitlink → opensoft/openDox main `49a99df2…` + `contracts/opendox-
    pin.yaml`, mirroring the openXdox pin of #917) … openxFactory then
    declares two direct upstreams (openDox, openXdox)."* Landed as its own
    pull request (#932; placement ruled by `#656` comment `5626260214`,
    "OWN PR FIRST, MERGE WHEN GREEN").

    `contracts/openxdox-pin.yaml` and `scripts/verify-openxdox-pin.py` (this
    file's own MODULE) are UNCHANGED by that ruling — RULING F still governs
    THIS pin, openXdox pins openXdox and nothing about openDox, and this test
    moves accordingly: from "no second declaration exists" to "the two
    declarations exist and agree". It asserts the Q7 SHAPE: exactly TWO
    product gitlinks in `.gitmodules` (`openDox`, `openXdox`, never a leg of
    either), and the LOCKSTEP equality between `contracts/opendox-pin.yaml`'s
    own `commit` and the commit `openXdox/contracts/opendox-pin.yaml` names —
    read as a git BLOB at the commit the `openXdox` gitlink itself records,
    never the openXdox WORKING TREE, on `scripts/verify-opendox-pin.py`'s own
    lockstep reasoning (PR #932 thread review, 2026-09-10): an on-disk edit to
    that file which does not move the gitlink must not be able to satisfy this
    assertion, so this test reads the same way the shipped verifier's fifth
    check does rather than through `Path.read_text` on the submodule mount.
    """
    gitmodules = (REPO_ROOT / ".gitmodules").read_text(encoding="utf-8")
    paths = [line.split("=", 1)[1].strip()
             for line in gitmodules.splitlines()
             if line.strip().startswith("path")]
    assert sorted(p for p in paths if p in ("openDox", "openXdox")) == \
        ["openDox", "openXdox"]
    for forbidden in ("openDox-code", "openDox-spec",
                      "openXdox-code", "openXdox-spec"):
        assert forbidden not in paths

    opendox_pin = yaml.safe_load(
        (REPO_ROOT / "contracts" / "opendox-pin.yaml").read_text(
            encoding="utf-8"))

    # A SECOND, INDEPENDENT implementation of the lockstep read — this test
    # does not import `scripts/verify-opendox-pin.py` at all, on the same
    # "a mechanism proving itself against itself proves nothing" reasoning as
    # `test_the_shipped_digest_is_recomputed_by_an_independent_implementation`
    # above. `MODULE` here is `verify-openxdox-pin.py`, which already exposes
    # `_recorded_gitlink` (reused by `test_the_gitlink_the_tree_records_
    # equals_the_pin` above); the blob read is plain `git show`.
    openxdox_oid, source = MODULE._recorded_gitlink(REPO_ROOT, "openXdox")
    assert openxdox_oid is not None, "the openXdox gitlink must be recorded"
    assert source == "HEAD"
    derived_blob = _git(REPO_ROOT / "openXdox", "show",
                        f"{openxdox_oid}:contracts/opendox-pin.yaml").stdout
    derived_pin = yaml.safe_load(derived_blob)

    assert opendox_pin["commit"] == derived_pin["commit"]
    assert opendox_pin["commit"] == "8ec3036ce496a90a3c92a89c4907e57941901b51"


def test_main_prints_one_success_line_and_returns_zero(capsys) -> None:
    assert MODULE.main([]) == 0
    out = capsys.readouterr()
    assert out.err == ""
    lines = [line for line in out.out.splitlines() if line.strip()]
    assert len(lines) == 1
    pin = MODULE.load_pin()
    assert pin["commit"] in lines[0]
    assert pin["digests"]["tree_sha256"] in lines[0]
    assert "sorted-ls-tree-r-v1" in lines[0]


def test_the_verifier_runs_as_a_subprocess_and_exits_zero() -> None:
    """The shebang path, end to end, from the repository root."""
    done = subprocess.run(["python3", str(VERIFIER)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("OK openxdox-pin verified: ")


# --------------------------------------------------------------------------
# the fixture is a positive first
# --------------------------------------------------------------------------

def test_the_scratch_fixture_is_a_positive_before_it_is_mutated(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    # Through `load_pin`, so the YAML the fixture writes is exercised too.
    loaded = MODULE.load_pin(scratch.pin_path)
    assert MODULE.verify(root=scratch.root, pin=loaded) is loaded


def test_a_staged_but_uncommitted_gitlink_falls_back_to_the_index(
        tmp_path: Path) -> None:
    """The pre-commit local run must be checkable, not silently unrunnable.

    `git ls-tree HEAD` yields nothing for a gitlink that is staged and never
    committed — the state of a fresh `git submodule add`, and therefore the
    normal state of the very tree this pin was authored in. Refusing there would
    make the tool unrunnable at the moment its author most needs it, and
    "unrunnable" is the failure mode that trains people to skip a gate.
    """
    scratch = _scratch(tmp_path, record="index")
    head = _git_raw(scratch.root, "ls-tree", "HEAD", "--", "openXdox")
    assert head.returncode != 0 or head.stdout.strip() == ""
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin
    oid, source = MODULE._recorded_gitlink(scratch.root, "openXdox")
    assert oid == scratch.commit
    assert "index" in source


def test_a_committed_gitlink_is_read_from_head(tmp_path: Path) -> None:
    scratch = _scratch(tmp_path, record="head")
    oid, source = MODULE._recorded_gitlink(scratch.root, "openXdox")
    assert oid == scratch.commit
    assert source == "HEAD"


def _assert_the_mutated_index_wins_over_stale_head(
        scratch: "Scratch", *, mutate, expected_oid: str | None) -> None:
    """Shared tail for the three PR #932 round-2 one-commit-resync
    regressions below (ported from `verify-opendox-pin.py`'s own suite, on
    the shared owed follow-up: `#656` comment `5628145815`). Each names a
    different way an ALREADY-COMMITTED `openXdox` gitlink is mutated in the
    INDEX ONLY — replaced, staged for deletion, or replaced by a regular
    file — and each must make `_recorded_gitlink` answer from that mutated
    index, never from HEAD's now-stale oid, even where the index's own
    answer is `None`.

    `mutate` performs the scenario's own staging, plus whatever assertion
    that scenario makes about the state it just staged (each caller below
    defines a small nested function for this); this helper asserts the two
    ends every scenario shares: the gitlink is still, and only, HEAD BEFORE
    `mutate` runs, and the INDEX wins — disagreeing with `scratch.commit` —
    after it does.
    """
    head_oid, head_source = MODULE._recorded_gitlink(scratch.root, "openXdox")
    assert head_oid == scratch.commit
    assert head_source == "HEAD"

    mutate()

    oid, source = MODULE._recorded_gitlink(scratch.root, "openXdox")
    assert oid == expected_oid
    assert oid != scratch.commit
    assert "index" in source


def test_a_replaced_gitlink_is_read_from_the_index_not_stale_head(
        tmp_path: Path) -> None:
    """THE ONE-COMMIT RESYNC REGRESSION (mirrors `tests/opendox_pin/test_
    opendox_pin_verifier.py`'s own regression, PR #932 thread review). A
    HEAD-first read of an EXISTING, already-committed gitlink answers for
    the commit being REPLACED the moment a resync stages a new one:
    `ls-tree HEAD` still finds the OLD 160000 entry and a HEAD-first check
    returns it without ever consulting the index, so a caller mid-resync
    sees the commit it is leaving rather than the one it is moving to.

    Simulates `git -C openXdox checkout <new>` then `git add openXdox` on a
    submodule already committed at a DIFFERENT commit: HEAD still names
    `scratch.commit` (the committed gitlink), the index is re-staged to
    `scratch.parent_commit` (a second, real, already-existing commit in the
    same nested repository) WITHOUT a new commit, and `_recorded_gitlink`
    must answer with the INDEX's value — the one about to be committed — not
    HEAD's stale one.
    """
    scratch = _scratch(tmp_path, record="head")

    def _stage_the_resync() -> None:
        scratch.record_gitlink(scratch.parent_commit, commit=False)
        # HEAD is unmoved: the resync is staged, not yet committed.
        still_head = _git_raw(scratch.root, "ls-tree", "HEAD", "--",
                              "openXdox")
        assert MODULE._gitlink_from(still_head.stdout,
                                    "openXdox") == scratch.commit

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_resync,
        expected_oid=scratch.parent_commit)


def test_a_gitlink_staged_for_deletion_is_not_read_from_stale_head(
        tmp_path: Path) -> None:
    """Mirrors `tests/opendox_pin/test_opendox_pin_verifier.py`'s own
    regression, PR #932 round-2 review's first finding. `git update-index
    --force-remove` (what `git rm --cached openXdox` does to the index)
    makes `git ls-files -s` stop reporting `openXdox` at all — silent in
    exactly the way a path that was NEVER tracked is silent — but never
    indistinguishable from "nothing changed": HEAD still names a committed
    gitlink here. `_recorded_gitlink` must not paper over the staged removal
    by falling back to that stale HEAD oid; the pending commit no longer has
    a gitlink at this path, so the answer must be `None`, not the commit
    being removed.
    """
    scratch = _scratch(tmp_path, record="head")

    def _stage_the_deletion() -> None:
        _git(scratch.root, "update-index", "--force-remove", "openXdox")
        index_after = _git(scratch.root, "ls-files", "-s", "--",
                           "openXdox").stdout
        assert index_after.strip() == "", \
            "the index must show nothing at all"

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_deletion, expected_oid=None)


def test_a_gitlink_replaced_by_a_regular_file_in_the_index_is_not_read_from_stale_head(
        tmp_path: Path) -> None:
    """Mirrors `tests/opendox_pin/test_opendox_pin_verifier.py`'s own
    regression, PR #932 round-2 review's first finding, the other half.
    Staging a REGULAR FILE over the same path (a `100644` entry, not
    `160000`) also makes `_gitlink_from` return nothing for the index — a
    different git state than a staged deletion, but the SAME non-answer
    from that helper — and must not fall back to HEAD's stale gitlink
    either.
    """
    scratch = _scratch(tmp_path, record="head")
    # git's own empty blob, always present
    empty_blob = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"

    def _stage_the_type_change() -> None:
        _git(scratch.root, "update-index", "--add", "--replace",
             "--cacheinfo", f"100644,{empty_blob},openXdox")
        index_after = _git(scratch.root, "ls-files", "-s", "--",
                           "openXdox").stdout
        assert "100644" in index_after
        assert "160000" not in index_after

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_type_change, expected_oid=None)


def test_a_regular_file_at_the_submodule_path_does_not_satisfy_the_gitlink(
        tmp_path: Path) -> None:
    """The MODE is matched, not merely the path.

    `ls-files -s` will happily report a regular file at the same path with mode
    100644, and accepting that entry would let a directory-turned-file satisfy a
    gitlink check.
    """
    scratch = _scratch(tmp_path, record="head")
    line = f"100644 {'c' * 40} 0\topenXdox"
    assert MODULE._gitlink_from(line, "openXdox") is None
    good = f"160000 commit {scratch.commit}\topenXdox"
    assert MODULE._gitlink_from(good, "openXdox") == scratch.commit


# --------------------------------------------------------------------------
# the five refusals
# --------------------------------------------------------------------------

def _break_uninitialized(scratch: Scratch) -> None:
    (scratch.sub / ".git").unlink()


def _break_gitlink(scratch: Scratch) -> None:
    # The tree records one revision and the pin records another. Reproduced by
    # moving the PIN, so the gitlink stays a real object and the disagreement is
    # the only difference.
    scratch.pin["commit"] = "0" * 39 + "1"


def _break_gitlink_recorded_nowhere(scratch: Scratch) -> None:
    # Nothing to do: the fixture was built with `record="none"`.
    assert _git(scratch.root, "ls-files", "-s", "--", "openXdox").stdout \
        .strip() == ""


def _break_checkout(scratch: Scratch) -> None:
    # Gitlink and pin AGREE, at the nested repository's FIRST commit, while the
    # checkout sits at its second. Only the checkout comparison catches this,
    # which is why checks 2 and 3 are both required. The digest is moved to the
    # first commit's too, so the fixture is not also digest-drifted and the
    # ordering claim is genuinely tested.
    scratch.pin["commit"] = scratch.parent_commit
    scratch.pin["digests"]["tree_sha256"] = \
        scratch.digest_at(scratch.parent_commit)
    scratch.record_gitlink(scratch.parent_commit)


def _break_digest(scratch: Scratch) -> None:
    scratch.pin["digests"]["tree_sha256"] = "0" * 64


def _break_recorded_digest_shape(scratch: Scratch) -> None:
    # A recomputed digest can never equal a digest that is not one, so an
    # unverifiable value is drift rather than a shape complaint.
    scratch.pin["digests"]["tree_sha256"] = "not-a-digest"


def _break_revision_kind(scratch: Scratch) -> None:
    scratch.pin["revision_kind"] = "tag"
    scratch.pin["commit"] = "xdox-v1.0"


def _break_abbreviated_commit(scratch: Scratch) -> None:
    scratch.pin["commit"] = scratch.commit[:12]


NEGATIVES = [
    ("uninitialized", _break_uninitialized, "head",
     "openxdox-pin-submodule-uninitialized", "openXdox/.git does not exist"),
    ("gitlink-disagrees", _break_gitlink, "head",
     "openxdox-pin-gitlink-mismatch", "but the pin records"),
    ("gitlink-recorded-nowhere", _break_gitlink_recorded_nowhere, "none",
     "openxdox-pin-gitlink-mismatch", "recorded NOWHERE"),
    ("checkout-stale", _break_checkout, "head",
     "openxdox-pin-checkout-mismatch", "the working checkout is stale"),
    ("digest-drift", _break_digest, "head",
     "openxdox-pin-digest-mismatch", "TREE DIGEST DRIFT"),
    ("recorded-digest-not-hex", _break_recorded_digest_shape, "head",
     "openxdox-pin-digest-mismatch", "is not 64 hex characters"),
    ("revision-kind-is-a-tag", _break_revision_kind, "head",
     "openxdox-pin-tag-only", "not 'commit'"),
    ("commit-is-abbreviated", _break_abbreviated_commit, "head",
     "openxdox-pin-tag-only", "not exactly 40 hex characters"),
]


@pytest.mark.parametrize("name,mutate,record,code,detail",
                         NEGATIVES, ids=[case[0] for case in NEGATIVES])
def test_each_refusal_fires_with_its_named_code_and_the_trailer(
        tmp_path: Path, name: str, mutate, record: str, code: str,
        detail: str) -> None:
    """One mutation, one named code, and always the remediation trailer."""
    scratch = _scratch(tmp_path, record=record)
    mutate(scratch)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    exc = caught.value
    assert exc.code == code, f"{name} refused {exc.code}: {exc.detail}"
    assert code in MODULE.REFUSAL_CODES
    assert detail in exc.detail
    rendered = str(exc)
    assert rendered.startswith(f"REFUSE {code}: ")
    assert rendered.endswith(MODULE.REMEDIATION)
    # The trailer is part of the refusal, not an addition a caller remembers to
    # make: a refusal naming what is wrong without naming what to run puts the
    # exit in tribal memory instead of in the message.
    assert "git submodule update --init openXdox" in rendered


def test_every_refusal_code_is_covered_by_at_least_one_negative() -> None:
    """Coverage closed in the direction that rots quietly.

    Without this, a code could lose its only probe — or be added to the
    vocabulary with none — and the suite would stay green.
    """
    covered = {case[3] for case in NEGATIVES}
    assert covered == set(MODULE.REFUSAL_CODES)


def test_a_content_change_inside_the_submodule_is_digest_drift(
        tmp_path: Path) -> None:
    """The digest is over the COMMIT, so drift is proved by moving the commit.

    A third commit in the nested repository, with the gitlink and `commit:`
    advanced to it but the recorded digest left at the second's, is exactly the
    state a hand-edited pin produces — and the one the digest exists to catch.
    """
    scratch = _scratch(tmp_path)
    (scratch.sub / "README.md").write_text("# edited\n", encoding="utf-8")
    _git(scratch.sub, "add", "-A")
    _git(scratch.sub, "commit", "-q", "-m", "edit the readme")
    moved = _git(scratch.sub, "rev-parse", "HEAD").stdout.strip()
    scratch.pin["commit"] = moved
    scratch.record_gitlink(moved)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "openxdox-pin-digest-mismatch"


def test_a_mode_change_alone_is_digest_drift(tmp_path: Path) -> None:
    """`<mode>` is the first field of every record, so a chmod is drift.

    The pin file states this in as many words. Proved rather than asserted,
    because a digest that silently ignored mode would still pass every other
    test in this file.
    """
    scratch = _scratch(tmp_path)
    before = scratch.digest_at(scratch.commit)
    _git(scratch.sub, "update-index", "--chmod=+x", "README.md")
    _git(scratch.sub, "commit", "-q", "-m", "make the readme executable")
    after = scratch.digest_at(
        _git(scratch.sub, "rev-parse", "HEAD").stdout.strip())
    assert after != before


def test_a_nested_leg_gitlink_moving_is_digest_drift(tmp_path: Path) -> None:
    """The claim that makes ONE digest cover a THREE-repository product.

    openxFactory mounts openXdox and not its `code`/`spec` legs. `ls-tree -r`
    reports a nested submodule as an opaque `160000 commit <oid>` record and
    never reads through it — so the leg's oid is IN the digest, and openXdox's
    own pin moving is drift here without any nested materialization. If this
    were false, openXdox could re-point a leg under a digest that never moved.
    """
    scratch = _scratch(tmp_path)
    before = scratch.digest_at(scratch.commit)
    _git(scratch.sub, "update-index", "--add", "--replace", "--cacheinfo",
         f"160000,{'d' * 40},code")
    _git(scratch.sub, "commit", "-q", "-m", "re-point the code leg")
    moved = _git(scratch.sub, "rev-parse", "HEAD").stdout.strip()
    after = scratch.digest_at(moved)
    assert after != before
    # ...and the verifier reports it as drift rather than passing.
    scratch.pin["commit"] = moved
    scratch.record_gitlink(moved)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "openxdox-pin-digest-mismatch"


def test_a_working_tree_deletion_is_deliberately_not_drift(
        tmp_path: Path) -> None:
    """THE NARROWING, PINNED SO IT CANNOT ROT BACK INTO AN OVERCLAIM.

    `tree_digest` reads `git ls-tree -r -z <commit>` — the COMMIT'S TREE OBJECT
    — so a file deleted or edited under the mount after checkout leaves every
    check passing. This verifier answers "does the consumed commit contain the
    bytes the pin says", not "is the working tree still those bytes", and that
    is a REAL narrowing against `verify-openxwallet-pin.py`, whose
    `pin-member-missing` does catch a working-tree deletion.

    Asserted rather than argued because the module docstring once claimed the
    opposite. Whether the consumer gate wired in task 5.3 (Phase 5) also needs a
    dirty-checkout refusal is that task's call; this test is the input to it,
    and it will fail loudly the day someone changes the answer.
    """
    scratch = _scratch(tmp_path)
    (scratch.sub / "README.md").unlink()
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin
    assert "pin-member-missing" not in MODULE.REFUSAL_CODES


# --------------------------------------------------------------------------
# the order departures are themselves asserted
# --------------------------------------------------------------------------

def test_a_malformed_pin_refuses_tag_only_not_a_mismatch(
        tmp_path: Path) -> None:
    """The shape guard runs BEFORE the comparisons that use its value.

    Evaluated after them, a pin declaring `revision_kind: tag` would be reported
    as `openxdox-pin-gitlink-mismatch` — a code that blames the TREE for a
    defect in the PIN, and that sends a reviewer to `git submodule update`
    instead of to the pin. Asserted with a tree that WOULD also fail the gitlink
    comparison, so the two are genuinely in contention.
    """
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("1" * 40)
    scratch.pin["revision_kind"] = "tag"
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "openxdox-pin-tag-only"


def test_an_uninitialized_submodule_outranks_a_disagreeing_gitlink(
        tmp_path: Path) -> None:
    """Check 1 first: an absent tree buries the one fact that matters."""
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("1" * 40)
    (scratch.sub / ".git").unlink()
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "openxdox-pin-submodule-uninitialized"


def test_a_stale_checkout_outranks_the_digest_it_would_otherwise_drift(
        tmp_path: Path) -> None:
    """Check 3 before check 4, and the reason is the report a reader gets.

    Check 4 recomputes against the CHECKOUT. Without check 3, a wrong revision
    on disk would be reported as CONTENT DRIFT — sending a reviewer to look for
    a changed byte when the actual defect is a `git submodule update` never run.
    """
    scratch = _scratch(tmp_path)
    scratch.pin["commit"] = scratch.parent_commit
    scratch.record_gitlink(scratch.parent_commit)
    # The digest still names the SECOND commit's tree, so check 4 would also
    # fire; check 3 must win.
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "openxdox-pin-checkout-mismatch"


# --------------------------------------------------------------------------
# `pin-unreadable`: the environment, not one of the five
# --------------------------------------------------------------------------

def test_an_absent_pin_file_is_pin_unreadable(tmp_path: Path) -> None:
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(tmp_path / "no-such-pin.yaml")
    assert caught.value.code == "pin-unreadable"
    assert str(caught.value).endswith(MODULE.REMEDIATION)


def test_an_unparseable_pin_file_is_pin_unreadable(tmp_path: Path) -> None:
    bad = tmp_path / "broken-pin.yaml"
    bad.write_text("commit: [unclosed\n", encoding="utf-8")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(bad)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_that_is_not_a_mapping_is_pin_unreadable(tmp_path: Path) -> None:
    scalar = tmp_path / "scalar-pin.yaml"
    scalar.write_text("just a string\n", encoding="utf-8")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(scalar)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_with_no_submodule_path_is_pin_unreadable(
        tmp_path: Path) -> None:
    """A pin with no path cannot be compared against any gitlink, so the TREE is
    not what is wrong and none of the five would name the defect."""
    scratch = _scratch(tmp_path)
    del scratch.pin["submodule_path"]
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_an_unimplemented_digest_definition_is_unreadable_not_drift(
        tmp_path: Path) -> None:
    """The question cannot be ASKED, so the tree is not what is wrong.

    Reporting it as drift would send a reviewer looking for a changed byte that
    is not there.
    """
    scratch = _scratch(tmp_path)
    scratch.pin["digest_definition"] = "some-other-definition-v9"
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"
    assert "sorted-ls-tree-r-v1" in caught.value.detail


def test_an_unimplemented_digest_algorithm_is_unreadable_not_drift(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    scratch.pin["digest_algorithm"] = "sha512"
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_with_no_digests_mapping_is_pin_unreadable(
        tmp_path: Path) -> None:
    """A pin that records no tree digest pins no bytes; an empty claim is not a
    satisfied claim."""
    scratch = _scratch(tmp_path)
    scratch.pin["digests"] = None
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


# --------------------------------------------------------------------------
# `main()`: every failure path is exit 2, on stderr
# --------------------------------------------------------------------------

def test_main_returns_two_and_writes_the_refusal_to_stderr(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """There is no exit 1.

    The consumer gate's only question is "may this pull request proceed", whose
    answer is identical for a stale pin and an uninitialized submodule; a
    two-valued failure invites a workflow that treats one of them as a warning.

    `load_pin` is patched rather than `MODULE.PIN_PATH`, and the difference is
    not cosmetic: `def load_pin(pin_path: Path = PIN_PATH)` binds the constant
    as a DEFAULT ARGUMENT at definition time, so rebinding the module attribute
    afterwards changes nothing and a test that tried it would pass the real
    pin and assert against a green run. Found by writing it the other way
    first.
    """
    absent = tmp_path / "no-such-pin.yaml"
    real_load_pin = MODULE.load_pin
    monkeypatch.setattr(MODULE, "load_pin",
                        lambda *_a, **_k: real_load_pin(absent))
    code = MODULE.main([])
    assert code == 2
    out = capsys.readouterr()
    assert out.out == ""
    assert out.err.startswith("REFUSE pin-unreadable: ")
    assert out.err.rstrip("\n").endswith(MODULE.REMEDIATION)


def test_main_never_returns_one_on_any_reachable_refusal(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail-closure is two-valued, and the suite says so for every code.

    Driven through `verify()` rather than through eight fixtures, because the
    claim is about `main()`'s translation of a refusal into an exit status and
    not about which refusal was raised.
    """
    for code in MODULE.REFUSAL_CODES:
        def _raise(*_args, **_kwargs):
            raise MODULE.PinRefusal(code, "synthetic")
        monkeypatch.setattr(MODULE, "verify", _raise)
        assert MODULE.main([]) == 2
