"""`scripts/verify-openxwallet-pin.py`: the positive, and all six refusals.

Two things are proven here and they are different things.

THE POSITIVE IS ADJUDICATED AGAINST THE REAL REPOSITORY ROOT. `test_the_real_pin
_is_satisfied` runs `verify()` with no arguments, so it recomputes the eight
`sha256`s in the committed `contracts/openxwallet-pin.yaml` against the bytes of
the pinned `openXwallet` submodule and compares both the recorded gitlink and the
checked-out revision against `commit`. That is the assertion that makes the pin a
fact rather than a claim, and it is the one assertion in this file that CANNOT be
moved into a fixture: a fixture proves the mechanism, and the mechanism agreeing
with itself says nothing about whether the eight digests in the shipped pin are
the digests of the shipped submodule.

THE SIX REFUSALS ARE ADJUDICATED IN AN ISOLATED SCRATCH TREE. `_scratch` builds
a throwaway superproject under `tmp_path` holding a real nested git repository at
`openXwallet`, a `.git` POINTER FILE, a fabricated `160000` gitlink, and a pin
whose `commit` is the nested repository's actual HEAD — so the positive path is
reachable in the fixture and each negative is ONE mutation away from it.
`test_the_scratch_fixture_is_a_positive_before_it_is_mutated` runs first for
exactly that reason: a fixture that refuses for some incidental reason would let
every negative below pass while proving nothing about the code it names.

NOTHING IS SKIPPED, AND THAT IS A DESIGN CONSTRAINT RATHER THAN A PREFERENCE.
A `pytest.skip` reports as a green bar, which is indistinguishable from a pass
to every reader and every gate — and "a check that cannot be reached reports as
satisfied" is the entire class of defect the pin, the verifier and this suite
exist to close. Every case here is hermetic: no network, no ambient git identity,
no ambient git config, and no dependence on any object that is not created inside
`tmp_path`.

THE GIT ENVIRONMENT IS PINNED, NOT INHERITED (`_hermetic_git`). CI runners have
no ambient git identity, so a scratch `git commit` there dies with "Author
identity unknown" while passing on a developer's machine; and a developer's
GLOBAL config can carry `core.hooksPath` (husky, lefthook, `pre-commit`) or
`commit.gpgsign`, either of which runs or refuses inside our throwaway
repositories. Both directions are the same defect — the ambient installation
must not change the answer — so `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1` and a repository-LOCAL identity are set for every test.
The env vars go on `os.environ` through `monkeypatch` rather than into a private
`env=` dict because the VERIFIER shells out to `git` itself; an env the fixture
kept to itself would leave the calls under test reading the host's config.
"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFIER = REPO_ROOT / "scripts" / "verify-openxwallet-pin.py"

# The ratified vocabulary, restated here as a LITERAL rather than imported.
# Asserting `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology;
# spelling FR-003's list out is what makes a silent reorder or rename in the
# verifier a test failure, which is the point — other code refuses BY CODE.
RATIFIED_CODES = (
    "pin-submodule-uninitialized",
    "pin-gitlink-mismatch",
    "pin-checkout-mismatch",
    "pin-digest-mismatch",
    "pin-member-missing",
    "pin-tag-only",
)


def _load():
    """The verifier as a module.

    Loaded by path because `scripts/verify-openxwallet-pin.py` is a hyphenated
    file name and therefore not importable, which is the same reason
    `tests/trust-anchor/test_negative_corpus.py` loads its subject this way.
    This import must be SIDE-EFFECT-FREE beyond the module constants — the
    verifier is contracted that way because `scripts/validate-trust-anchor.py`
    loads it the same way at run time — so a regression that put I/O at import
    would surface here as a collection error.
    """
    spec = importlib.util.spec_from_file_location("verify_openxwallet_pin",
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
    """No global config, no system config, and a deterministic identity.

    See the module docstring. `GIT_*_NAME`/`GIT_*_EMAIL` are belt-and-braces
    beside the repository-local identity `_scratch` sets: the local config covers
    every call this file makes, and the env vars cover any call it does not.
    """
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "openxwallet-pin-test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "pin-test@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "openxwallet-pin-test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "pin-test@example.invalid")


def _git_raw(root: Path, *args: str) -> subprocess.CompletedProcess:
    """git, without asserting success — for the calls that are EXPECTED to fail."""
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    done = _git_raw(root, *args)
    assert done.returncode == 0, \
        f"git {' '.join(args)} in {root} failed: {done.stderr}"
    return done


def _identify(root: Path) -> None:
    """Repository-LOCAL identity, because the apply path may not carry `-c`."""
    _git(root, "config", "user.name", "openxwallet-pin-test")
    _git(root, "config", "user.email", "pin-test@example.invalid")


# --------------------------------------------------------------------------
# the scratch superproject
# --------------------------------------------------------------------------

class Scratch:
    """A throwaway superproject that satisfies the pin, ready to be broken.

    Its member layout is DERIVED FROM THE REAL PIN rather than invented, so the
    fixture is a faithful miniature: the same eight digested paths and the same
    six path-only members, with synthetic bytes and freshly computed digests. A
    hand-written member list would drift from the pin the day the pin changed
    and the negatives would keep passing against a shape production no longer
    has.
    """

    def __init__(self, root: Path, commit: str, parent_commit: str,
                 pin: dict) -> None:
        self.root = root
        self.sub = root / "openXwallet"
        self.commit = commit
        self.parent_commit = parent_commit
        self.pin = pin
        self.pin_path = root / "contracts" / "openxwallet-pin.yaml"

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
             "--cacheinfo", f"160000,{oid},openXwallet")
        if commit:
            _git(self.root, "commit", "-q", "--allow-empty",
                 "-m", f"record openXwallet at {oid}")

    def member(self, rel: str) -> Path:
        return self.sub / rel


def _scratch(tmp_path: Path, *, record: str = "head") -> Scratch:
    """Build the positive fixture. `record` is "head", "index" or "none".

    "head"  the gitlink is committed, so `git ls-tree HEAD` answers.
    "index" the gitlink is staged and never committed — the state of a fresh
            `git submodule add`, and the state in which the verifier must fall
            back to `git ls-files -s`.
    "none"  no gitlink anywhere, which must refuse rather than pass.
    """
    real_pin = MODULE.load_pin()
    digested = [entry["path"] for entry in real_pin["files"]]
    path_only = list(real_pin["pinned_by_commit_only"])

    root = tmp_path / "superproject"
    (root / "contracts").mkdir(parents=True)
    _git(root.parent, "init", "-q", "-b", "main", str(root))
    _identify(root)

    sub = root / "openXwallet"
    sub.mkdir()
    for rel in digested:
        target = sub / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# synthetic {rel}\n", encoding="utf-8")
    for rel in path_only:
        target = sub / rel
        if Path(rel).suffix:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# synthetic {rel}\n", encoding="utf-8")
        else:
            # A directory member. Given a file inside it, because git tracks no
            # empty directory and the fixture must survive a clone.
            target.mkdir(parents=True, exist_ok=True)
            (target / "keep.yaml").write_text("{}\n", encoding="utf-8")

    # The nested repository, with TWO commits. The second exists so
    # `pin-checkout-mismatch` is reproducible by pinning the FIRST while the
    # checkout sits at the second — a real advanced/stale checkout, with no
    # write through the `.git` pointer and no fabricated revision.
    _git(sub.parent, "init", "-q", "-b", "main", str(sub))
    _identify(sub)
    _git(sub, "add", "-A")
    _git(sub, "commit", "-q", "-m", "seed the wallet members")
    parent_commit = _git(sub, "rev-parse", "HEAD").stdout.strip()
    (sub / "docs").mkdir(exist_ok=True)
    (sub / "docs" / "pin-resync-runbook.md").write_text("runbook\n",
                                                        encoding="utf-8")
    _git(sub, "add", "-A")
    _git(sub, "commit", "-q", "-m", "add the runbook")
    commit = _git(sub, "rev-parse", "HEAD").stdout.strip()

    # Convert the nested `.git` DIRECTORY into the `gitdir:` POINTER FILE a real
    # submodule has. Every scratch test therefore also exercises the `.exists()`
    # rather than `.is_dir()` choice in check 1, which is the check that would
    # otherwise refuse every correctly initialized submodule in the world.
    modules = root / ".git" / "modules"
    modules.mkdir(parents=True, exist_ok=True)
    (sub / ".git").rename(modules / "openXwallet")
    (sub / ".git").write_text(f"gitdir: {modules / 'openXwallet'}\n",
                              encoding="utf-8")

    pin = {
        "schema_version": 1,
        "kind": "pinned_contract_manifest",
        "contract_bundle_tag": "wallet-scratch",
        "source_repository": "opensoft/openXwallet",
        "submodule_path": "openXwallet",
        "commit": commit,
        "revision_kind": "commit",
        "digest_algorithm": "sha256",
        "files": [
            {"path": rel,
             "sha256": hashlib.sha256((sub / rel).read_bytes()).hexdigest()}
            for rel in digested
        ],
        "pinned_by_commit_only": path_only,
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


def _consumer(tmp_path: Path, name: str, oid: str | None) -> Path:
    """A minimal aggregation-shaped checkout, with or without the gitlink."""
    root = tmp_path / name
    root.mkdir(parents=True)
    _git(root.parent, "init", "-q", "-b", "main", str(root))
    _identify(root)
    if oid is not None:
        _git(root, "update-index", "--add", "--replace",
             "--cacheinfo", f"160000,{oid},openXwallet")
        _git(root, "commit", "-q", "--allow-empty", "-m", "record openXwallet")
    return root


# --------------------------------------------------------------------------
# the vocabulary
# --------------------------------------------------------------------------

def test_refusal_codes_are_exactly_the_six_ratified_codes_in_order() -> None:
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES


def test_pin_unreadable_is_not_in_the_ratified_vocabulary() -> None:
    # The seventh code names an ENVIRONMENT in which no finding can be reached.
    # A consumer that enumerates the vocabulary must not be able to treat "we
    # could not ask the question" as one of the answers.
    assert "pin-unreadable" not in MODULE.REFUSAL_CODES
    assert len(MODULE.REFUSAL_CODES) == 6


def test_the_remediation_trailer_is_the_ratified_string() -> None:
    assert MODULE.REMEDIATION == (
        "Remediation: run `git submodule update --init openXwallet` (NOT "
        "--recursive; this wave's init is deliberately scoped). If the pin "
        "itself is stale, follow `openXwallet/docs/pin-resync-runbook.md`.")
    # `--recursive` must stay absent: this wave's init is scoped to one
    # submodule, and a remediation that recursed would pull the aggregation's
    # whole submodule tree into a job with business in exactly one of them.
    assert "--recursive;" in MODULE.REMEDIATION
    assert "update --init --recursive" not in MODULE.REMEDIATION


# --------------------------------------------------------------------------
# the positive, against the real repository
# --------------------------------------------------------------------------

def test_the_real_pin_is_satisfied() -> None:
    """The eight shipped digests are the digests of the shipped submodule."""
    pin = MODULE.verify()
    assert pin["revision_kind"] == "commit"
    assert len(pin["commit"]) == 40
    assert len(pin["files"]) == 8
    assert len(pin["pinned_by_commit_only"]) == 6


def test_the_real_submodule_dot_git_is_a_file_not_a_directory() -> None:
    """Check 1 must use `.exists()`; this is why.

    A submodule's `.git` is a FILE holding a `gitdir:` pointer, so `.is_dir()`
    is False for the shipped tree and an `.is_dir()` check would refuse the
    very state it exists to accept. Asserted against the real checkout so the
    claim is about the world and not about the fixture.
    """
    dot_git = REPO_ROOT / "openXwallet" / ".git"
    assert dot_git.exists()
    assert not dot_git.is_dir()
    assert MODULE.verify() is not None


def test_main_prints_one_success_line_and_returns_zero(capsys) -> None:
    assert MODULE.main([]) == 0
    out = capsys.readouterr()
    assert out.err == ""
    lines = [line for line in out.out.splitlines() if line.strip()]
    assert len(lines) == 1
    pin = MODULE.load_pin()
    assert pin["commit"] in lines[0]
    assert str(pin["contract_bundle_tag"]) in lines[0]
    assert "8 digest(s)" in lines[0]


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
    committed — the state of a fresh `git submodule add`. CI always reads a
    pushed commit; an author running the gate locally before the wave's first
    commit does not, and refusing there would train people to skip the gate.
    """
    scratch = _scratch(tmp_path, record="index")
    # HEAD answers NOTHING here — in this fixture it does not exist at all,
    # which is the state of a repository whose very first commit has not landed.
    # Either shape (a failing `ls-tree` or an empty one) must reach the index.
    head = _git_raw(scratch.root, "ls-tree", "HEAD", "--", "openXwallet")
    assert head.returncode != 0 or head.stdout.strip() == ""
    assert MODULE.verify(root=scratch.root, pin=scratch.pin) is scratch.pin
    oid, source = MODULE._recorded_gitlink(scratch.root, "openXwallet")
    assert oid == scratch.commit
    assert "index" in source


def test_a_committed_gitlink_is_read_from_head(tmp_path: Path) -> None:
    scratch = _scratch(tmp_path, record="head")
    oid, source = MODULE._recorded_gitlink(scratch.root, "openXwallet")
    assert oid == scratch.commit
    assert source == "HEAD"


# --------------------------------------------------------------------------
# the six refusals
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
    assert _git(scratch.root, "ls-files", "-s", "--", "openXwallet").stdout \
        .strip() == ""


def _break_checkout(scratch: Scratch) -> None:
    # Gitlink and pin AGREE, at the nested repository's first commit, while the
    # checkout sits at its second. Only the checkout comparison catches this,
    # which is why checks 2 and 3 are both required.
    scratch.pin["commit"] = scratch.parent_commit
    scratch.record_gitlink(scratch.parent_commit)


def _break_digest(scratch: Scratch) -> None:
    target = scratch.member(scratch.pin["files"][3]["path"])
    target.write_bytes(target.read_bytes() + b"# one appended byte\n")


def _break_recorded_digest_shape(scratch: Scratch) -> None:
    # A recomputed digest can never equal a digest that is not one, so an
    # unverifiable member is drift rather than a shape complaint.
    scratch.pin["files"][1]["sha256"] = "not-a-digest"


def _break_digested_member_missing(scratch: Scratch) -> None:
    scratch.member(scratch.pin["files"][0]["path"]).unlink()


def _break_path_only_member_missing(scratch: Scratch) -> None:
    # A README the pin declares content-addressed by commit, deleted from the
    # WORKING TREE after checkout — the one thing the commit cannot catch, and
    # therefore what check 5's presence test is for.
    victim = next(rel for rel in scratch.pin["pinned_by_commit_only"]
                  if rel.endswith("README.md"))
    scratch.member(victim).unlink()


def _break_revision_kind(scratch: Scratch) -> None:
    scratch.pin["revision_kind"] = "tag"
    scratch.pin["commit"] = "wallet-v1.1"


def _break_abbreviated_commit(scratch: Scratch) -> None:
    scratch.pin["commit"] = scratch.commit[:12]


NEGATIVES = [
    ("uninitialized", _break_uninitialized, "head",
     "pin-submodule-uninitialized", "openXwallet/.git does not exist"),
    ("gitlink-disagrees", _break_gitlink, "head",
     "pin-gitlink-mismatch", "but the pin records"),
    ("gitlink-recorded-nowhere", _break_gitlink_recorded_nowhere, "none",
     "pin-gitlink-mismatch", "recorded NOWHERE"),
    ("checkout-stale", _break_checkout, "head",
     "pin-checkout-mismatch", "the working checkout is stale"),
    ("digest-drift", _break_digest, "head",
     "pin-digest-mismatch", "DIGEST DRIFT"),
    ("recorded-digest-not-hex", _break_recorded_digest_shape, "head",
     "pin-digest-mismatch", "is not 64 hex characters"),
    ("digested-member-missing", _break_digested_member_missing, "head",
     "pin-member-missing", "is MISSING from the checkout"),
    ("path-only-member-missing", _break_path_only_member_missing, "head",
     "pin-member-missing", "content-addressed by anything"),
    ("revision-kind-is-a-tag", _break_revision_kind, "head",
     "pin-tag-only", "not 'commit'"),
    ("commit-is-abbreviated", _break_abbreviated_commit, "head",
     "pin-tag-only", "not exactly 40 hex characters"),
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
    assert "git submodule update --init openXwallet" in rendered
    assert "openXwallet/docs/pin-resync-runbook.md" in rendered


def test_every_ratified_code_is_covered_by_at_least_one_negative() -> None:
    """Coverage closed in the direction that rots quietly.

    Without this, a code could lose its only probe — or be added to the
    vocabulary with none — and the suite would stay green.
    """
    covered = {case[3] for case in NEGATIVES}
    assert covered == set(MODULE.REFUSAL_CODES)


# --------------------------------------------------------------------------
# the order departure is itself asserted
# --------------------------------------------------------------------------

def test_a_malformed_pin_refuses_pin_tag_only_not_a_mismatch(
        tmp_path: Path) -> None:
    """The shape guard runs BEFORE the comparisons that use its value.

    `pin-tag-only` is SIXTH in the ratified order, but the second and third
    ratified checks both compare against `commit`. Evaluated in sixth place, a
    pin declaring `revision_kind: tag` would be reported as
    `pin-gitlink-mismatch` — a code that blames the TREE for a defect in the
    PIN, and that sends a reviewer to `git submodule update` instead of to the
    pin. This asserts the earlier evaluation, with a tree that WOULD also fail
    the gitlink comparison so the two are genuinely in contention.
    """
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("1" * 40)
    scratch.pin["revision_kind"] = "tag"
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-tag-only"


def test_an_uninitialized_submodule_outranks_a_disagreeing_gitlink(
        tmp_path: Path) -> None:
    """Check 1 first: eight missing files bury the one fact that matters."""
    scratch = _scratch(tmp_path)
    scratch.record_gitlink("1" * 40)
    (scratch.sub / ".git").unlink()
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-submodule-uninitialized"


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


def test_a_pin_that_is_not_a_mapping_is_pin_unreadable(tmp_path: Path) -> None:
    scalar = tmp_path / "scalar-pin.yaml"
    scalar.write_text("just a string\n", encoding="utf-8")
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.load_pin(scalar)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_with_no_submodule_path_is_pin_unreadable(
        tmp_path: Path) -> None:
    # A pin with no path cannot be compared against any gitlink, so the TREE is
    # not what is wrong and none of the six would name the defect.
    scratch = _scratch(tmp_path)
    del scratch.pin["submodule_path"]
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


def test_a_pin_with_no_files_members_is_pin_unreadable(tmp_path: Path) -> None:
    # An empty claim is not a satisfied claim.
    scratch = _scratch(tmp_path)
    scratch.pin["files"] = []
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify(root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-unreadable"


# --------------------------------------------------------------------------
# aggregation mode
# --------------------------------------------------------------------------

def test_an_agreeing_aggregation_root_passes(tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    agg = _consumer(tmp_path, "aggregation-agrees", scratch.commit)
    assert MODULE.verify_aggregation(agg, root=scratch.root,
                                     pin=scratch.pin) is None


def test_a_disagreeing_aggregation_root_refuses_gitlink_mismatch(
        tmp_path: Path) -> None:
    scratch = _scratch(tmp_path)
    agg = _consumer(tmp_path, "aggregation-disagrees", "2" * 40)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify_aggregation(agg, root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-gitlink-mismatch"
    assert str(agg) in caught.value.detail
    assert str(caught.value).endswith(MODULE.REMEDIATION)


def test_an_aggregation_root_with_no_gitlink_refuses_member_missing(
        tmp_path: Path) -> None:
    """An absent pin in a consumer that is supposed to carry one is not a pass.

    Treating "no gitlink to disagree with" as agreement would make the whole
    aggregation check opt-out by omission — the failure mode it exists to catch.
    """
    scratch = _scratch(tmp_path)
    agg = _consumer(tmp_path, "aggregation-silent", None)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify_aggregation(agg, root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-member-missing"
    assert str(agg) in caught.value.detail


def test_aggregation_mode_validates_the_pin_shape_standalone(
        tmp_path: Path) -> None:
    """Safe called without `verify()` first: it cannot compare against a tag."""
    scratch = _scratch(tmp_path)
    scratch.pin["revision_kind"] = "tag"
    agg = _consumer(tmp_path, "aggregation-shape", scratch.commit)
    with pytest.raises(MODULE.PinRefusal) as caught:
        MODULE.verify_aggregation(agg, root=scratch.root, pin=scratch.pin)
    assert caught.value.code == "pin-tag-only"


def test_a_staged_aggregation_gitlink_is_read_from_the_index(
        tmp_path: Path) -> None:
    """One implementation, one vocabulary: the fallback applies here too."""
    scratch = _scratch(tmp_path)
    agg = tmp_path / "aggregation-staged"
    agg.mkdir()
    _git(agg.parent, "init", "-q", "-b", "main", str(agg))
    _identify(agg)
    _git(agg, "update-index", "--add", "--cacheinfo",
         f"160000,{scratch.commit},openXwallet")
    assert MODULE.verify_aggregation(agg, root=scratch.root,
                                    pin=scratch.pin) is None


# --------------------------------------------------------------------------
# `main()`: every failure path is exit 2, on stderr
# --------------------------------------------------------------------------

def test_main_returns_two_and_writes_the_refusal_to_stderr(
        tmp_path: Path, capsys) -> None:
    """There is no exit 1.

    The consumer gate's only question is "may this pull request proceed", whose
    answer is identical for a stale pin and an uninitialized submodule; a
    two-valued failure invites a workflow that treats one of them as a warning.
    """
    agg = _consumer(tmp_path, "aggregation-empty", None)
    code = MODULE.main(["--aggregation-root", str(agg)])
    assert code == 2
    out = capsys.readouterr()
    assert out.out == ""
    assert out.err.startswith("REFUSE pin-member-missing: ")
    assert out.err.rstrip("\n").endswith(MODULE.REMEDIATION)


def test_main_notes_the_aggregation_root_when_it_agrees(capsys) -> None:
    """The real repository plus itself as the aggregation: the gitlink agrees.

    `verify_aggregation` reads the same gitlink `verify()` just checked, so this
    exercises the argument-handling and the success note without needing an
    aggregation that P4 has not yet repointed.
    """
    assert MODULE.main(["--aggregation-root", str(REPO_ROOT)]) == 0
    out = capsys.readouterr()
    assert "aggregation root" in out.out
    assert "agrees" in out.out


def test_the_verifier_runs_as_a_subprocess_and_exits_zero() -> None:
    """The shebang path, end to end, from the repository root."""
    done = subprocess.run(["python3", str(VERIFIER)], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("OK openxwallet-pin verified: ")
