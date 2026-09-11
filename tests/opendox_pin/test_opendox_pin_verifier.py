"""`scripts/verify-opendox-pin.py`: the positive, all six refusals, and the
LOCKSTEP cross-check the sibling openXdox suite has no analogue of.

Modelled on `tests/openxdox_pin/test_openxdox_pin_verifier.py`, which this
file mirrors check-for-check for the first four checks and departs from only
where the artifact departs: `opendox-pin-*`-prefixed codes instead of
`openxdox-pin-*`, and a FIFTH check — LOCKSTEP against openXdox's own derived
reading of the same commit — with no analogue in that file at all.

THE POSITIVE IS ADJUDICATED AGAINST THE REAL REPOSITORY ROOT, on the same
reasoning as the sibling suite: `test_the_shipped_digest_is_recomputed_by_an_
independent_implementation` re-derives `sorted-ls-tree-r-v1` from the
definition written in `contracts/opendox-pin.yaml`'s own comment block —
locally, without calling `MODULE.tree_digest` — and compares the result
against the digest the shipped pin records.

THE SIX REFUSALS ARE ADJUDICATED IN AN ISOLATED SCRATCH TREE, and this
fixture is a THIRD REPOSITORY deeper than the sibling suite's: a throwaway
superproject under `tmp_path`, holding a real nested git repository at
`openDox` (with its own nested `160000` gitlink at `code`, so the "a leg
moving inside openDox is drift too" claim stays provable) AND a SECOND real
nested git repository at `openXdox`, holding nothing but the one committed
file check 5 reads: `contracts/opendox-pin.yaml`, declaring the `commit` this
pin's own LOCKSTEP check compares against. Both nested repositories' `.git`
directories are converted to `gitdir:` POINTER FILES, exactly as a real
submodule mount looks on disk, so both `.exists()`-rather-than-`.is_dir()`
choices (check 1's, and the LOCKSTEP prerequisite's own) are exercised against
the real shape rather than a directory that happens to also satisfy `.git`.

THE WORKING-TREE-READ DEFECT IS THE MOST IMPORTANT THING THIS FILE PROVES IS
FIXED. `test_editing_the_openxdox_working_tree_pin_does_not_fool_lockstep`
edits `openXdox/contracts/opendox-pin.yaml` ON DISK, inside the scratch
fixture, WITHOUT moving the `openXdox` gitlink or committing inside that
nested repository — the exact shape of the defect PR #932's review caught:
reading the submodule's mutable working tree lets an edit there satisfy or
defeat the LOCKSTEP check independently of what the superproject is actually
pinned to. `verify()` must still answer from the COMMITTED blob the gitlink
names, so this test asserts the on-disk edit changes nothing.

NOTHING IS SKIPPED, AND THAT IS A DESIGN CONSTRAINT RATHER THAN A PREFERENCE,
on the sibling suite's own reasoning: `pytest-suite` pins `EXPECT_SKIPPED`
exactly, so a conditionally-skipped test here would red the required check on
every tree that skipped it. Every case is hermetic: no network, no ambient
git identity, no ambient git config, and no dependence on any object not
created inside `tmp_path` — except the handful of cases that deliberately
read the real repository, each named as doing so.

THE GIT ENVIRONMENT IS PINNED, NOT INHERITED (`_hermetic_git`), on the
sibling suite's reasoning unchanged: CI runners have no ambient git identity,
so a scratch `git commit` there dies with "Author identity unknown" while
passing on a developer's machine, and a developer's GLOBAL config can carry
`core.hooksPath` or `commit.gpgsign`, either of which runs or refuses inside a
throwaway repository. The env vars go on `os.environ` through `monkeypatch`
rather than into a private `env=` dict because the VERIFIER shells out to
`git` itself; an env this file kept to itself would leave the calls under
test reading the host's config.
"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFIER = REPO_ROOT / "scripts" / "verify-opendox-pin.py"
PIN_PATH = REPO_ROOT / "contracts" / "opendox-pin.yaml"

# The vocabulary, restated as a LITERAL rather than imported — spelling the six
# out is what makes a silent reorder or rename a test failure, on the sibling
# suite's own reasoning.
OPENDOX_CODES = (
    "opendox-pin-tag-only",
    "opendox-pin-submodule-uninitialized",
    "opendox-pin-gitlink-mismatch",
    "opendox-pin-checkout-mismatch",
    "opendox-pin-digest-mismatch",
    "opendox-pin-lockstep-mismatch",
)


def _load():
    """The verifier as a module.

    Loaded by path because `scripts/verify-opendox-pin.py` is a hyphenated
    file name and therefore not importable — the same reason the sibling
    suite loads its own subject this way. The import must be SIDE-EFFECT-FREE
    beyond the module constants, so a regression that put I/O at import time
    surfaces here as a collection error.
    """
    spec = importlib.util.spec_from_file_location("verify_opendox_pin",
                                                  VERIFIER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MODULE = _load()


def _load_openxdox():
    spec = importlib.util.spec_from_file_location(
        "verify_openxdox_pin_probe",
        REPO_ROOT / "scripts" / "verify-openxdox-pin.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_wallet():
    spec = importlib.util.spec_from_file_location(
        "verify_openxwallet_pin_probe",
        REPO_ROOT / "scripts" / "verify-openxwallet-pin.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# the hermetic git environment
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _hermetic_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """No global config, no system config, and a deterministic identity."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "opendox-pin-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "pin-test@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "opendox-pin-test")
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


def _git_bytes_raw(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, check=False)


def _identify(root: Path) -> None:
    """Repository-LOCAL identity, because a call may not carry `-c`."""
    _git(root, "config", "user.name", "opendox-pin-test")
    _git(root, "config", "user.email", "pin-test@example.invalid")


def _independent_tree_digest(repo: Path, revision: str) -> str:
    """`sorted-ls-tree-r-v1`, re-derived here from the pin's own prose.

    DELIBERATELY NOT `MODULE.tree_digest`. This is the second implementation
    that makes the shipped digest a measured fact rather than a
    self-consistent one; if the two ever disagree, one of them is wrong and
    the suite says so instead of both agreeing on the same mistake.

    The definition, quoted from `contracts/opendox-pin.yaml`:
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
# the scratch superproject — TWO nested repositories deep
# --------------------------------------------------------------------------

def _to_pointer_file(root: Path, sub_name: str) -> None:
    """Convert `root/<sub_name>/.git` from a directory into the `gitdir:`
    POINTER FILE a real submodule mount has, so the `.exists()`-rather-than-
    `.is_dir()` choice is exercised against the real shape."""
    sub = root / sub_name
    modules = root / ".git" / "modules"
    modules.mkdir(parents=True, exist_ok=True)
    dest = modules / sub_name
    (sub / ".git").rename(dest)
    (sub / ".git").write_text(f"gitdir: {dest}\n", encoding="utf-8")


class Scratch:
    """A throwaway superproject that satisfies the pin, ready to be broken."""

    def __init__(self, root: Path, commit: str, parent_commit: str,
                 pin: dict, openxdox_head: str) -> None:
        self.root = root
        self.sub = root / "openDox"
        self.openxdox_sub = root / "openXdox"
        self.commit = commit
        self.parent_commit = parent_commit
        self.pin = pin
        self.pin_path = root / "contracts" / "opendox-pin.yaml"
        self.openxdox_head = openxdox_head

    def write_pin(self) -> None:
        self.pin_path.write_text(yaml.safe_dump(self.pin, sort_keys=False),
                                 encoding="utf-8")

    def record_gitlink(self, path: str, oid: str, *,
                       commit: bool = True) -> None:
        """Fabricate a `160000` index entry for `path`, and optionally commit
        it. `--cacheinfo` writes the index entry without requiring the object
        to exist in THIS repository, which is what makes a disagreeing or
        dangling gitlink reproducible without a second real clone."""
        _git(self.root, "update-index", "--add", "--replace",
             "--cacheinfo", f"160000,{oid},{path}")
        if commit:
            _git(self.root, "commit", "-q", "--allow-empty",
                 "-m", f"record {path} at {oid}")

    def digest_at(self, revision: str) -> str:
        return _independent_tree_digest(self.sub, revision)

    def write_openxdox_pin_raw(self, text: str) -> str:
        """Overwrite the openXdox nested repo's own `contracts/opendox-
        pin.yaml` with arbitrary TEXT, commit it, and return the new HEAD —
        the raw form used by the malformed-derived-pin cases."""
        path = self.openxdox_sub / "contracts" / "opendox-pin.yaml"
        path.write_text(text, encoding="utf-8")
        _git(self.openxdox_sub, "add", "-A")
        _git(self.openxdox_sub, "commit", "-q", "-m", "rewrite derived pin")
        return _git(self.openxdox_sub, "rev-parse", "HEAD").stdout.strip()

    def write_openxdox_pin_bytes(self, data: bytes) -> str:
        """As `write_openxdox_pin_raw`, but for content that is not valid
        UTF-8 text at all — the `UnicodeDecodeError` case."""
        path = self.openxdox_sub / "contracts" / "opendox-pin.yaml"
        path.write_bytes(data)
        _git(self.openxdox_sub, "add", "-A")
        _git(self.openxdox_sub, "commit", "-q", "-m", "rewrite derived pin")
        return _git(self.openxdox_sub, "rev-parse", "HEAD").stdout.strip()

    def write_openxdox_derived_commit(self, derived_commit: str) -> str:
        """Rewrite the openXdox nested repo's own pin to declare `commit:
        derived_commit`, commit it, and return the new HEAD."""
        body = {
            "schema_version": 1,
            "kind": "pinned_contract_manifest",
            "source_repository": "opensoft/openDox",
            "submodule_path": "openDox",
            "commit": derived_commit,
            "revision_kind": "commit",
            "digest_algorithm": "sha256",
            "digest_definition": "sorted-ls-tree-r-v1",
            "digests": {"tree_sha256": "0" * 64},
            "carve_commit": "b" * 40,
            "resync_runbook": "openDox/README.md#the-lockstep-invariant",
            "verify_pin": "scripts/verify-opendox-pin.py",
        }
        return self.write_openxdox_pin_raw(
            yaml.safe_dump(body, sort_keys=False))


def _scratch(tmp_path: Path, *, record: str = "head",
            openxdox_record: str = "head") -> Scratch:
    """Build the positive fixture. `record` governs the `openDox` gitlink,
    `openxdox_record` the `openXdox` one — each "head", "index" or "none",
    on `_scratch`'s own three meanings in the sibling suite.

    THE NESTED `openDox` REPOSITORY CARRIES A NESTED GITLINK OF ITS OWN
    (`code`), on the sibling fixture's own reasoning: openDox is an assembly
    root whose `code` and `spec` legs are submodules, and the pin file's
    central claim — that ONE digest covers a three-repository product without
    mounting the other two — is only checkable if the fixture has one.

    THE SECOND NESTED REPOSITORY, `openXdox`, EXISTS ONLY TO HOLD ONE FILE:
    its own `contracts/opendox-pin.yaml`, declaring `commit: <the openDox
    commit>` by default — the value check 5 reads. It carries no leg of its
    own; that claim belongs to the sibling suite's fixture, not this one's.
    """
    root = tmp_path / "superproject"
    (root / "contracts").mkdir(parents=True)
    _git(root.parent, "init", "-q", "-b", "main", str(root))
    _identify(root)

    # ---- the openDox nested repository, with its own nested leg -----------
    sub = root / "openDox"
    sub.mkdir()
    _git(sub.parent, "init", "-q", "-b", "main", str(sub))
    _identify(sub)
    (sub / "contracts").mkdir()
    (sub / "README.md").write_text("# synthetic openDox\n", encoding="utf-8")
    (sub / "contracts" / "manifest.yaml").write_text(
        "schema_version: 1\ncontract_bundle_version: none\nentries: []\n",
        encoding="utf-8")
    _git(sub, "add", "-A")
    _git(sub, "update-index", "--add", "--cacheinfo",
         f"160000,{'a' * 40},code")
    _git(sub, "commit", "-q", "-m", "seed the assembly root and its leg")
    parent_commit = _git(sub, "rev-parse", "HEAD").stdout.strip()

    # A SECOND commit, so `opendox-pin-checkout-mismatch` is reproducible by
    # pinning the FIRST while the checkout sits at the second.
    (sub / "CHANGELOG.md").write_text("# changes\n", encoding="utf-8")
    _git(sub, "add", "-A")
    _git(sub, "commit", "-q", "-m", "add a changelog")
    commit = _git(sub, "rev-parse", "HEAD").stdout.strip()
    tree_sha256 = _independent_tree_digest(sub, commit)
    _to_pointer_file(root, "openDox")

    # ---- the openXdox nested repository — one file, the derived pin -------
    openxdox_sub = root / "openXdox"
    openxdox_sub.mkdir()
    _git(openxdox_sub.parent, "init", "-q", "-b", "main", str(openxdox_sub))
    _identify(openxdox_sub)
    (openxdox_sub / "contracts").mkdir()
    (openxdox_sub / "contracts" / "opendox-pin.yaml").write_text(
        yaml.safe_dump({
            "schema_version": 1,
            "kind": "pinned_contract_manifest",
            "source_repository": "opensoft/openDox",
            "submodule_path": "openDox",
            "commit": commit,
            "revision_kind": "commit",
            "digest_algorithm": "sha256",
            "digest_definition": "sorted-ls-tree-r-v1",
            "digests": {"tree_sha256": tree_sha256},
            "carve_commit": "b" * 40,
            "resync_runbook": "openDox/README.md#the-lockstep-invariant",
            "verify_pin": "scripts/verify-opendox-pin.py",
        }, sort_keys=False), encoding="utf-8")
    _git(openxdox_sub, "add", "-A")
    _git(openxdox_sub, "commit", "-q", "-m", "seed the derived opendox pin")
    openxdox_head = _git(openxdox_sub, "rev-parse", "HEAD").stdout.strip()
    _to_pointer_file(root, "openXdox")

    pin = {
        "schema_version": 1,
        "kind": "pinned_contract_manifest",
        "source_repository": "opensoft/openDox",
        "submodule_path": "openDox",
        "commit": commit,
        "revision_kind": "commit",
        "digest_algorithm": "sha256",
        "digest_definition": "sorted-ls-tree-r-v1",
        "digests": {"tree_sha256": tree_sha256},
        "carve_commit": "b" * 40,
        "resync_runbook": "openDox/README.md#the-lockstep-invariant",
        "verify_pin": "scripts/verify-opendox-pin.py",
    }

    scratch = Scratch(root, commit, parent_commit, pin, openxdox_head)
    scratch.write_pin()

    # TWO PASSES, DELIBERATELY ORDERED: `git commit` commits the WHOLE index,
    # so a "head" entry processed after an "index" entry would sweep the
    # staged-but-uncommitted one into its own commit and silently upgrade it.
    # Every "head" entry commits FIRST, each in its own clean commit; every
    # "index" entry stages ONLY, last, so it is still staged-and-uncommitted
    # when this function returns rather than accidentally landed.
    entries = (("openDox", commit, record),
              ("openXdox", openxdox_head, openxdox_record))
    for path, oid, mode in entries:
        if mode == "head":
            scratch.record_gitlink(path, oid, commit=True)
        elif mode not in ("index", "none"):  # pragma: no cover - misuse
            raise AssertionError(f"unknown record mode {mode!r}")
    for path, oid, mode in entries:
        if mode == "index":
            scratch.record_gitlink(path, oid, commit=False)
    return scratch


# --------------------------------------------------------------------------
# the vocabulary
# --------------------------------------------------------------------------

def test_refusal_codes_are_exactly_the_six_opendox_codes_in_order() -> None:
    assert MODULE.REFUSAL_CODES == OPENDOX_CODES


def test_pin_unreadable_is_not_in_the_vocabulary() -> None:
    """The seventh spelling names an ENVIRONMENT in which no finding is
    reachable. A consumer that enumerates the vocabulary must not be able to
    treat "we could not ask the question" as one of the answers to it."""
    assert "pin-unreadable" not in MODULE.REFUSAL_CODES
    assert len(MODULE.REFUSAL_CODES) == 6


def test_every_code_is_prefixed_so_a_consumer_can_tell_the_products_apart(
) -> None:
    """The prefix is the whole reason these are not `openxdox-pin-*`'s codes
    by import, and not the wallet's six either: a shared vocabulary would make
    an openDox refusal indistinguishable from a sibling refusal to anything
    branching on the string."""
    assert all(code.startswith("opendox-pin-")
               for code in MODULE.REFUSAL_CODES)
    openxdox = _load_openxdox()
    wallet = _load_wallet()
    assert set(MODULE.REFUSAL_CODES) & set(openxdox.REFUSAL_CODES) == set()
    assert set(MODULE.REFUSAL_CODES) & set(wallet.REFUSAL_CODES) == set()


def test_the_remediation_trailer_names_both_gitlinks_and_the_procedures(
) -> None:
    """Both submodules are named, because check 5 needs `openXdox`
    initialized too — a caller who only ran `git submodule update --init
    openDox` would hit a SECOND environment failure immediately after fixing
    the first. `--recursive` must stay ABSENT: neither product's own
    `code`/`spec` legs are consumed here."""
    assert "git submodule update --init openDox openXdox" in MODULE.REMEDIATION
    assert "NOT --recursive" in MODULE.REMEDIATION
    assert "update --init --recursive" not in MODULE.REMEDIATION
    assert "openDox/README.md#the-lockstep-invariant" in MODULE.REMEDIATION
    assert "docs/opendox-cutover-runbook.md" in MODULE.REMEDIATION


def test_the_digest_constants_are_the_family_spelling() -> None:
    assert MODULE.DIGEST_DEFINITION == "sorted-ls-tree-r-v1"
    assert MODULE.DIGEST_ALGORITHM == "sha256"
    assert MODULE.GITLINK_MODE == "160000"


def test_there_is_no_aggregation_root_mode_and_the_absence_is_deliberate(
) -> None:
    """`opensoft/xFactory` records no openDox gitlink, so the mode would
    refuse by construction. Asserted so the absence reads as a decision
    rather than an oversight."""
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
    assert pin["source_repository"] == "opensoft/openDox"
    assert pin["submodule_path"] == "openDox"
    assert pin["digest_definition"] == "sorted-ls-tree-r-v1"


def test_the_shipped_digest_is_recomputed_by_an_independent_implementation(
) -> None:
    """The one assertion in this file that cannot be moved into a fixture."""
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    recomputed = _independent_tree_digest(REPO_ROOT / "openDox", pin["commit"])
    assert recomputed == pin["digests"]["tree_sha256"]
    assert MODULE.tree_digest(REPO_ROOT / "openDox",
                              pin["commit"]) == recomputed


def test_the_pinned_commit_is_a_real_object_in_the_submodule() -> None:
    """`docs/opendox-cutover-runbook.md` § 7's "the pin names a real object".

    git records a gitlink WITHOUT checking the object exists, so a wrong pin
    commits and pushes clean; only a `cat-file` in the submodule catches it.
    """
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    done = _git(REPO_ROOT / "openDox", "cat-file", "-t", pin["commit"])
    assert done.stdout.strip() == "commit"


def test_the_gitlink_the_tree_records_equals_the_pin() -> None:
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    recorded, source = MODULE._recorded_gitlink(REPO_ROOT, "openDox")
    assert recorded == pin["commit"]
    assert source == "HEAD"


def test_the_real_submodule_dot_git_is_a_file_not_a_directory() -> None:
    """Check 1 must use `.exists()`; this is why."""
    dot_git = REPO_ROOT / "openDox" / ".git"
    assert dot_git.exists()
    assert not dot_git.is_dir()


def test_the_real_pin_is_in_lockstep_with_openxdox_own_derived_reading(
) -> None:
    """Check 5, against the real repository — the fact PR #932 exists to
    establish: openxFactory's own DIRECT pin and openXdox's own DERIVED
    reading of the same commit agree. Reads the openXdox blob at the
    gitlinked commit, exactly as `MODULE._openxdox_derived_commit` does but
    as a second, independent implementation living in this test file."""
    pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
    openxdox_oid, source = MODULE._recorded_gitlink(REPO_ROOT, "openXdox")
    assert openxdox_oid is not None
    assert source == "HEAD"
    blob = _git(REPO_ROOT / "openXdox", "show",
               f"{openxdox_oid}:contracts/opendox-pin.yaml").stdout
    derived = yaml.safe_load(blob)
    assert derived["commit"] == pin["commit"]


def test_the_migration_block_is_present_and_lockstep_with_openxdox() -> None:
    """PR #952 review thread: the §4.2 `migration` block RULED ASK-1 (#656
    comment 5628886636) is not read by `verify()` — only the commit and tree
    digest are — so deleting or renaming it would still leave every other
    check in this file green. This is the positive assertion the thread
    asked for: the root pin carries `migration.range`, `.reversible`, and
    `.runbook` each at the `not_yet_deployed` sentinel, the in-file comment
    cites ASK-1, and openXdox's own derived copy — read as a git BLOB at the
    gitlinked commit, never the working tree, on the same reasoning as
    `test_the_real_pin_is_in_lockstep_with_openxdox_own_derived_reading`
    above — renders the identical three keys and cites the same ruling.

    Field-VALUE enforcement inside `verify()` itself (refusing a pin whose
    `migration.range` etc. are not `not_yet_deployed`, or requiring the keys
    at all) is a follow-up once `neutral-product-pin`'s spec pins the key
    names; this test only proves the shape is not silently deletable.
    """
    pin_text = PIN_PATH.read_text(encoding="utf-8")
    pin = yaml.safe_load(pin_text)
    migration = pin["migration"]
    assert migration["range"] == "not_yet_deployed"
    assert migration["reversible"] == "not_yet_deployed"
    assert migration["runbook"] == "not_yet_deployed"
    assert "ASK-1" in pin_text

    openxdox_oid, source = MODULE._recorded_gitlink(REPO_ROOT, "openXdox")
    assert openxdox_oid is not None
    assert source == "HEAD"
    blob = _git(REPO_ROOT / "openXdox", "show",
               f"{openxdox_oid}:contracts/opendox-pin.yaml").stdout
    derived = yaml.safe_load(blob)
    derived_migration = derived["migration"]
    assert derived_migration["range"] == "not_yet_deployed"
    assert derived_migration["reversible"] == "not_yet_deployed"
    assert derived_migration["runbook"] == "not_yet_deployed"
    assert "ASK-1" in blob


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
    assert "lockstep with openXdox confirmed" in lines[0]


def test_the_verifier_runs_as_a_subprocess_and_exits_zero() -> None:
    """The shebang path, end to end, from the repository root."""
    done = subprocess.run(["python3", str(VERIFIER)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("OK opendox-pin verified: ")


# --------------------------------------------------------------------------
# the fixture is a positive first
# --------------------------------------------------------------------------

def test_the_scratch_fixture_is_a_positive_before_it_is_mutated(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    loaded = MODULE.load_pin(scratch.pin_path)
    assert MODULE.verify(root=scratch.root, pin=loaded) is loaded


def test_a_staged_but_uncommitted_gitlink_falls_back_to_the_index(
        tmp_path: Path) -> None:
    """The pre-commit local run must be checkable, not silently unrunnable."""
    scratch = _scratch(tmp_path, record="index")
    head = _git_raw(scratch.root, "ls-tree", "HEAD", "--", "openDox")
    assert head.returncode != 0 or head.stdout.strip() == ""
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin
    oid, source = MODULE._recorded_gitlink(scratch.root, "openDox")
    assert oid == scratch.commit
    assert "index" in source


def test_a_committed_gitlink_is_read_from_head(tmp_path: Path) -> None:
    scratch = _scratch(tmp_path, record="head")
    oid, source = MODULE._recorded_gitlink(scratch.root, "openDox")
    assert oid == scratch.commit
    assert source == "HEAD"


def _assert_the_mutated_index_wins_over_stale_head(
        scratch: "Scratch", *, mutate, expected_oid: str | None) -> None:
    """Shared tail for the three PR #932 round-2 one-commit-resync
    regressions below. Each names a different way an ALREADY-COMMITTED
    `openDox` gitlink is mutated in the INDEX ONLY — replaced, staged for
    deletion, or replaced by a regular file — and each must make
    `_recorded_gitlink` answer from that mutated index, never from HEAD's
    now-stale oid, even where the index's own answer is `None`.

    `mutate` performs the scenario's own staging, plus whatever assertion
    that scenario makes about the state it just staged (each caller below
    defines a small nested function for this); this helper asserts the two
    ends every scenario shares: the gitlink is still, and only, HEAD BEFORE
    `mutate` runs, and the INDEX wins — disagreeing with `scratch.commit` —
    after it does.
    """
    head_oid, head_source = MODULE._recorded_gitlink(scratch.root, "openDox")
    assert head_oid == scratch.commit
    assert head_source == "HEAD"

    mutate()

    oid, source = MODULE._recorded_gitlink(scratch.root, "openDox")
    assert oid == expected_oid
    assert oid != scratch.commit
    assert "index" in source


def test_a_replaced_gitlink_is_read_from_the_index_not_stale_head(
        tmp_path: Path) -> None:
    """THE ONE-COMMIT RESYNC REGRESSION (PR #932 thread review). A HEAD-first
    read of an EXISTING, already-committed gitlink answers for the commit
    being REPLACED the moment a resync stages a new one: `ls-tree HEAD` still
    finds the OLD 160000 entry and a HEAD-first check returns it without ever
    consulting the index, so a caller mid-resync sees the commit it is
    leaving rather than the one it is moving to.

    Simulates `git -C openDox checkout <new>` then `git add openDox` on a
    submodule already committed at a DIFFERENT commit: HEAD still names
    `scratch.commit` (the committed gitlink), the index is re-staged to
    `scratch.parent_commit` (a second, real, already-existing commit in the
    same nested repository) WITHOUT a new commit, and `_recorded_gitlink`
    must answer with the INDEX's value — the one about to be committed — not
    HEAD's stale one.
    """
    scratch = _scratch(tmp_path, record="head")

    def _stage_the_resync() -> None:
        scratch.record_gitlink("openDox", scratch.parent_commit,
                               commit=False)
        # HEAD is unmoved: the resync is staged, not yet committed.
        still_head = _git_raw(scratch.root, "ls-tree", "HEAD", "--",
                              "openDox")
        assert MODULE._gitlink_from(still_head.stdout,
                                    "openDox") == scratch.commit

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_resync,
        expected_oid=scratch.parent_commit)


def test_a_gitlink_staged_for_deletion_is_not_read_from_stale_head(
        tmp_path: Path) -> None:
    """PR #932 round-2 review's first regression. `git update-index
    --force-remove` (what `git rm --cached openDox` does to the index) makes
    `git ls-files -s` stop reporting `openDox` at all — silent in exactly the
    way a path that was NEVER tracked is silent — but never indistinguishable
    from "nothing changed": HEAD still names a committed gitlink here.
    `_recorded_gitlink` must not paper over the staged removal by falling
    back to that stale HEAD oid; the pending commit no longer has a gitlink
    at this path, so the answer must be `None`, not the commit being removed.
    """
    scratch = _scratch(tmp_path, record="head")

    def _stage_the_deletion() -> None:
        _git(scratch.root, "update-index", "--force-remove", "openDox")
        index_after = _git(scratch.root, "ls-files", "-s", "--",
                           "openDox").stdout
        assert index_after.strip() == "", \
            "the index must show nothing at all"

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_deletion, expected_oid=None)


def test_a_gitlink_replaced_by_a_regular_file_in_the_index_is_not_read_from_stale_head(
        tmp_path: Path) -> None:
    """PR #932 round-2 review's first regression, the other half. Staging a
    REGULAR FILE over the same path (a `100644` entry, not `160000`) also
    makes `_gitlink_from` return nothing for the index — a different git
    state than a staged deletion, but the SAME non-answer from that helper —
    and must not fall back to HEAD's stale gitlink either.
    """
    scratch = _scratch(tmp_path, record="head")
    # git's own empty blob, always present
    empty_blob = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"

    def _stage_the_type_change() -> None:
        _git(scratch.root, "update-index", "--add", "--replace",
             "--cacheinfo", f"100644,{empty_blob},openDox")
        index_after = _git(scratch.root, "ls-files", "-s", "--",
                           "openDox").stdout
        assert "100644" in index_after
        assert "160000" not in index_after

    _assert_the_mutated_index_wins_over_stale_head(
        scratch, mutate=_stage_the_type_change, expected_oid=None)


def test_a_regular_file_at_the_submodule_path_does_not_satisfy_the_gitlink(
        tmp_path: Path) -> None:
    """The MODE is matched, not merely the path."""
    scratch = _scratch(tmp_path, record="head")
    line = f"100644 {'c' * 40} 0\topenDox"
    assert MODULE._gitlink_from(line, "openDox") is None
    good = f"160000 commit {scratch.commit}\topenDox"
    assert MODULE._gitlink_from(good, "openDox") == scratch.commit


# --------------------------------------------------------------------------
# the six refusals
# --------------------------------------------------------------------------

def _break_uninitialized(scratch: Scratch) -> None:
    (scratch.sub / ".git").unlink()


def _break_gitlink(scratch: Scratch) -> None:
    scratch.pin["commit"] = "0" * 39 + "1"


def _break_gitlink_recorded_nowhere(scratch: Scratch) -> None:
    assert _git(scratch.root, "ls-files", "-s", "--", "openDox").stdout \
        .strip() == ""


def _break_checkout(scratch: Scratch) -> None:
    scratch.pin["commit"] = scratch.parent_commit
    scratch.pin["digests"]["tree_sha256"] = \
        scratch.digest_at(scratch.parent_commit)
    scratch.record_gitlink("openDox", scratch.parent_commit)


def _break_digest(scratch: Scratch) -> None:
    scratch.pin["digests"]["tree_sha256"] = "0" * 64


def _break_recorded_digest_shape(scratch: Scratch) -> None:
    scratch.pin["digests"]["tree_sha256"] = "not-a-digest"


def _break_revision_kind(scratch: Scratch) -> None:
    scratch.pin["revision_kind"] = "tag"
    scratch.pin["commit"] = "dox-v1.0"


def _break_abbreviated_commit(scratch: Scratch) -> None:
    scratch.pin["commit"] = scratch.commit[:12]


def _break_lockstep(scratch: Scratch) -> None:
    # openXdox's own pin advances to a DIFFERENT commit, and its gitlink is
    # moved forward WITH it — a genuine disagreement between two point-in-
    # time-correct declarations, not an artifact of a stale openXdox gitlink.
    new_derived = "e" * 40
    new_head = scratch.write_openxdox_derived_commit(new_derived)
    scratch.record_gitlink("openXdox", new_head)


NEGATIVES = [
    ("uninitialized", _break_uninitialized, "head", "head",
     "opendox-pin-submodule-uninitialized", "openDox/.git does not exist"),
    ("gitlink-disagrees", _break_gitlink, "head", "head",
     "opendox-pin-gitlink-mismatch", "but the pin records"),
    ("gitlink-recorded-nowhere", _break_gitlink_recorded_nowhere, "none",
     "head", "opendox-pin-gitlink-mismatch", "recorded NOWHERE"),
    ("checkout-stale", _break_checkout, "head", "head",
     "opendox-pin-checkout-mismatch", "the working checkout is stale"),
    ("digest-drift", _break_digest, "head", "head",
     "opendox-pin-digest-mismatch", "TREE DIGEST DRIFT"),
    ("recorded-digest-not-hex", _break_recorded_digest_shape, "head", "head",
     "opendox-pin-digest-mismatch", "is not 64 hex characters"),
    ("revision-kind-is-a-tag", _break_revision_kind, "head", "head",
     "opendox-pin-tag-only", "not 'commit'"),
    ("commit-is-abbreviated", _break_abbreviated_commit, "head", "head",
     "opendox-pin-tag-only", "not exactly 40 hex characters"),
    ("lockstep-disagrees", _break_lockstep, "head", "head",
     "opendox-pin-lockstep-mismatch", "disagree"),
]


@pytest.mark.parametrize("name,mutate,record,openxdox_record,code,detail",
                         NEGATIVES, ids=[case[0] for case in NEGATIVES])
def test_each_refusal_fires_with_its_named_code_and_the_trailer(
        tmp_path: Path, name: str, mutate, record: str, openxdox_record: str,
        code: str, detail: str) -> None:
    """One mutation, one named code, and always the remediation trailer."""
    scratch = _scratch(tmp_path, record=record,
                       openxdox_record=openxdox_record)
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
    assert "git submodule update --init openDox openXdox" in rendered


def test_every_refusal_code_is_covered_by_at_least_one_negative() -> None:
    covered = {case[4] for case in NEGATIVES}
    assert covered == set(MODULE.REFUSAL_CODES)


def test_a_content_change_inside_the_submodule_is_digest_drift(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    (scratch.sub / "README.md").write_text("# edited\n", encoding="utf-8")
    _git(scratch.sub, "add", "-A")
    _git(scratch.sub, "commit", "-q", "-m", "edit the readme")
    moved = _git(scratch.sub, "rev-parse", "HEAD").stdout.strip()
    scratch.pin["commit"] = moved
    scratch.record_gitlink("openDox", moved)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-digest-mismatch"


def test_a_mode_change_alone_is_digest_drift(tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    before = scratch.digest_at(scratch.commit)
    _git(scratch.sub, "update-index", "--chmod=+x", "README.md")
    _git(scratch.sub, "commit", "-q", "-m", "make the readme executable")
    after = scratch.digest_at(
        _git(scratch.sub, "rev-parse", "HEAD").stdout.strip())
    assert after != before


def test_a_nested_leg_gitlink_moving_is_digest_drift(tmp_path: Path) -> None:
    """The claim that makes ONE digest cover a THREE-repository product."""
    scratch = _scratch(tmp_path)
    before = scratch.digest_at(scratch.commit)
    _git(scratch.sub, "update-index", "--add", "--replace", "--cacheinfo",
         f"160000,{'d' * 40},code")
    _git(scratch.sub, "commit", "-q", "-m", "re-point the code leg")
    moved = _git(scratch.sub, "rev-parse", "HEAD").stdout.strip()
    after = scratch.digest_at(moved)
    assert after != before
    scratch.pin["commit"] = moved
    scratch.record_gitlink("openDox", moved)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-digest-mismatch"


def test_a_working_tree_deletion_is_deliberately_not_drift(
        tmp_path: Path) -> None:
    """`tree_digest` reads the COMMIT'S tree object, so a file deleted under
    the mount after checkout leaves every check passing — the same narrowing
    the sibling suite pins for openXdox, proved here for openDox."""
    scratch = _scratch(tmp_path)
    (scratch.sub / "README.md").unlink()
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin
    assert "pin-member-missing" not in MODULE.REFUSAL_CODES


# --------------------------------------------------------------------------
# THE REGRESSION TEST: the working-tree-read defect PR #932's review caught
# --------------------------------------------------------------------------

def test_editing_the_openxdox_working_tree_pin_does_not_fool_lockstep(
        tmp_path: Path) -> None:
    """An operator can edit `openXdox/contracts/opendox-pin.yaml` ON DISK
    without moving the `openXdox` gitlink or committing inside that
    submodule. `verify()` must answer from the COMMITTED blob the gitlink
    names, so a dirty, unrepinned working-tree edit must change nothing about
    the result — proved here in both directions: the edit alone does not
    break a satisfied pin, and (implicitly, by the same read path) it could
    not have silently REPAIRED a broken one either.
    """
    scratch = _scratch(tmp_path)
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin

    derived_path = scratch.openxdox_sub / "contracts" / "opendox-pin.yaml"
    original = derived_path.read_text(encoding="utf-8")
    dirtied = original.replace(scratch.commit, "f" * 40)
    assert dirtied != original, "the fixture must actually contain the commit"
    derived_path.write_text(dirtied, encoding="utf-8")

    # Proof the mutation is real: openXdox's own working tree is now dirty,
    # and its HEAD has not moved.
    status = _git(scratch.openxdox_sub, "status", "--porcelain").stdout
    assert "contracts/opendox-pin.yaml" in status
    assert _git(scratch.openxdox_sub, "rev-parse", "HEAD").stdout.strip() \
        == scratch.openxdox_head

    # Still satisfied: the dirty working-tree file is never consulted.
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin


def test_a_committed_change_to_the_openxdox_pin_IS_seen(tmp_path: Path
                                                        ) -> None:
    """The complement of the test above: this is not a check that ignores
    openXdox altogether, only one that ignores its WORKING TREE. A real
    commit that moves openXdox's own derived reading, with the gitlink
    advanced to match, is exactly `_break_lockstep` above and is caught as
    `opendox-pin-lockstep-mismatch`; asserted again here, directly, so the
    two tests read as a deliberate pair rather than as one test that happens
    to pass."""
    scratch = _scratch(tmp_path)
    new_head = scratch.write_openxdox_derived_commit("e" * 40)
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-lockstep-mismatch"
    assert scratch.commit in caught.value.detail
    assert "e" * 40 in caught.value.detail


# --------------------------------------------------------------------------
# the order departures are themselves asserted
# --------------------------------------------------------------------------

def test_a_malformed_pin_refuses_tag_only_not_a_mismatch(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("openDox", "1" * 40)
    scratch.pin["revision_kind"] = "tag"
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-tag-only"


def test_an_uninitialized_submodule_outranks_a_disagreeing_gitlink(
        tmp_path: Path) -> None:
    """Check 1 first: an absent tree buries the one fact that matters."""
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("openDox", "1" * 40)
    (scratch.sub / ".git").unlink()
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-submodule-uninitialized"


def test_a_stale_checkout_outranks_the_digest_it_would_otherwise_drift(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    scratch.pin["commit"] = scratch.parent_commit
    scratch.record_gitlink("openDox", scratch.parent_commit)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-checkout-mismatch"


def test_a_digest_mismatch_outranks_a_lockstep_mismatch(
        tmp_path: Path) -> None:
    """Check 5 runs LAST, once checks 1-4 have already proved this pin an
    accurate description of the openDox bytes present. Broken here alongside
    a genuine lockstep disagreement, so the two are truly in contention and
    check 4's code is the one that must win."""
    scratch = _scratch(tmp_path)
    scratch.pin["digests"]["tree_sha256"] = "0" * 64
    new_head = scratch.write_openxdox_derived_commit("e" * 40)
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "opendox-pin-digest-mismatch"


# --------------------------------------------------------------------------
# `pin-unreadable`: the environment, not one of the six
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


def test_a_pin_file_with_invalid_utf8_bytes_is_pin_unreadable(
        tmp_path: Path) -> None:
    """`Path.read_text(encoding="utf-8")` can raise `UnicodeDecodeError`,
    which is not `OSError` and not `yaml.YAMLError` — the defect a Copilot
    review of PR #932 found. `load_pin` must translate it into the same
    fail-closed refusal, not let it propagate as a bare traceback."""
    bad = tmp_path / "invalid-utf8-pin.yaml"
    bad.write_bytes(b"commit: \"\xff\xfe not valid utf-8\"\n")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(bad)
    assert caught.value.code == "pin-unreadable"
    assert str(caught.value).endswith(MODULE.REMEDIATION)


def test_a_pin_that_is_not_a_mapping_is_pin_unreadable(tmp_path: Path) -> None:
    scalar = tmp_path / "scalar-pin.yaml"
    scalar.write_text("just a string\n", encoding="utf-8")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(scalar)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_with_no_submodule_path_is_pin_unreadable(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    del scratch.pin["submodule_path"]
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_an_unimplemented_digest_definition_is_unreadable_not_drift(
        tmp_path: Path) -> None:
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
    scratch = _scratch(tmp_path)
    scratch.pin["digests"] = None
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


# --------------------------------------------------------------------------
# `pin-unreadable`: the LOCKSTEP prerequisite, not one of the six either
# --------------------------------------------------------------------------

def test_an_uninitialized_openxdox_is_pin_unreadable_naming_the_init(
        tmp_path: Path) -> None:
    """The LOCKSTEP question cannot be asked without openXdox initialized —
    an environment fact, not a finding that the two commits disagree."""
    scratch = _scratch(tmp_path)
    (scratch.openxdox_sub / ".git").unlink()
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"
    assert "openXdox" in caught.value.detail
    assert "git submodule update --init openXdox" in caught.value.detail


def test_openxdox_gitlink_recorded_nowhere_is_pin_unreadable(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path, openxdox_record="none")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"
    assert "openXdox" in caught.value.detail


def test_an_openxdox_gitlink_naming_a_missing_object_is_pin_unreadable(
        tmp_path: Path) -> None:
    """The gitlink is recorded, but the commit it names was never committed
    inside the openXdox nested repository — `git show` fails, and that
    failure is `pin-unreadable` rather than a traceback."""
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("openXdox", "9" * 40)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"
    assert "9" * 40 in caught.value.detail


def test_a_derived_pin_blob_with_invalid_utf8_bytes_is_pin_unreadable(
        tmp_path: Path) -> None:
    """The second instance of the same `UnicodeDecodeError` defect: the blob
    `git show` returns is decoded by hand in `_openxdox_derived_commit`
    rather than through `Path.read_text`, and must fail closed the same way.
    """
    scratch = _scratch(tmp_path)
    new_head = scratch.write_openxdox_pin_bytes(
        b"commit: \"\xff\xfe not valid utf-8\"\n")
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_a_derived_pin_that_is_not_a_mapping_is_pin_unreadable(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    new_head = scratch.write_openxdox_pin_raw("just a string\n")
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_a_derived_pin_with_no_commit_field_is_pin_unreadable(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    new_head = scratch.write_openxdox_pin_raw(
        "schema_version: 1\nkind: pinned_contract_manifest\n")
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_a_derived_pin_with_an_abbreviated_commit_is_pin_unreadable(
        tmp_path: Path) -> None:
    """Not `opendox-pin-tag-only`: the malformed value is on openXdox's
    side of the comparison, not this pin's own, so none of the six would
    name the actual defect."""
    scratch = _scratch(tmp_path)
    new_head = scratch.write_openxdox_pin_raw(
        yaml.safe_dump({"commit": "abc123"}, sort_keys=False))
    scratch.record_gitlink("openXdox", new_head)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"
    assert "40 hex characters" in caught.value.detail


# --------------------------------------------------------------------------
# `main()`: every failure path is exit 2, on stderr
# --------------------------------------------------------------------------

def test_main_returns_two_and_writes_the_refusal_to_stderr(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """There is no exit 1. `load_pin` is patched rather than `MODULE.PIN_PATH`
    — `def load_pin(pin_path: Path = PIN_PATH)` binds the constant as a
    DEFAULT ARGUMENT at definition time, so rebinding the module attribute
    afterwards changes nothing."""
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
    """Fail-closure is two-valued, and the suite says so for every code."""
    for code in MODULE.REFUSAL_CODES:
        def _raise(*_args, **_kwargs):
            raise MODULE.PinRefusal(code, "synthetic")
        monkeypatch.setattr(MODULE, "verify", _raise)
        assert MODULE.main([]) == 2
