"""Rule (f) fails closed when the openxWallet pin does not hold.

The trust-anchor family's chain-custody set does not restate openxWallet's
custody model; it COMPOSES with it, reading
`openXwallet/contracts/openxwallet/openxwallet-custody.registry.yaml` at run
time. `split-openxwallet-repo` moved that parent set out of openxFactory and
behind a nested submodule pinned by `contracts/openxwallet-pin.yaml`, which
changes what the validator has to prove before it trusts the set. The old check
was `is_file()` — a question about PRESENCE, adequate while the bytes were owned
here and inadequate the moment they arrive across a gitlink, because a submodule
sitting on an unpinned commit is present, readable, and mapping-resolving, and
would move this family's answers without moving the pin.

So the two refusals that presence could never express are asserted here, BY THEIR
NAMED CODES:

  * `pin-submodule-uninitialized` — the shape of a clone taken without the
    scoped `git submodule update --init openXwallet`, which is the ordinary way
    for this to happen and therefore the one that must not degrade to a skip; and
  * `pin-digest-mismatch` — bytes inside an initialized submodule that no longer
    hash to what the pin recorded, with the recorded gitlink and the checked-out
    revision both still agreeing. Digest is the only check that catches it.

Both cases are built under `tmp_path` as a throwaway openxFactory-shaped tree
with a FABRICATED pin and its own scratch wallet repository. Nothing here touches
the real checkout: the conditions being tested are a broken submodule and
corrupted pinned bytes, and inducing either in the working tree would leave the
tree broken for whatever ran next — including the other suites in the same
session.

The remaining case, a verifier that cannot be loaded at all, is asserted through
its remediation string rather than by breaking the verifier: the point of that
path is that it refuses instead of falling back to "the registry file happens to
be there", and an operator who hits it still needs the way out.
"""

from __future__ import annotations

import functools
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-trust-anchor.py"
VERIFIER = REPO_ROOT / "scripts" / "verify-openxwallet-pin.py"
PIN_PATH = REPO_ROOT / "contracts" / "openxwallet-pin.yaml"

REGISTRY_MEMBER = "contracts/openxwallet/openxwallet-custody.registry.yaml"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None, path
    spec.loader.exec_module(module)
    return module


@functools.lru_cache(maxsize=1)
def _module():
    """`validate-trust-anchor.py`, loaded on first use.

    Not at module scope, and for the same reason the validator loads the verifier
    lazily: a load that fails at import scope becomes a COLLECTION error and
    takes the other cases in this file with it, so nothing left in the run can
    say which half broke."""
    return _load("validate_trust_anchor", VALIDATOR)


@functools.lru_cache(maxsize=1)
def _verifier():
    """`verify-openxwallet-pin.py`, loaded on first use — same reason."""
    return _load("verify_openxwallet_pin", VERIFIER)


@functools.lru_cache(maxsize=1)
def _real_pin() -> dict:
    return yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))


def _git(*args: str, cwd: Path) -> str:
    # `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` cut the operator's
    # own configuration out of the scratch repositories, and the identity is
    # declared rather than assumed because a CI runner has no ambient one and a
    # commit is how a gitlink gets recorded at all.
    env = dict(
        os.environ,
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="trust-anchor pin fixture",
        GIT_AUTHOR_EMAIL="trust-anchor-pin-fixture@openxfactory.invalid",
        GIT_COMMITTER_NAME="trust-anchor pin fixture",
        GIT_COMMITTER_EMAIL="trust-anchor-pin-fixture@openxfactory.invalid",
    )
    done = subprocess.run(("git", *args), cwd=str(cwd), env=env,
                          capture_output=True, text=True)
    assert done.returncode == 0, (
        f"git {' '.join(args)} in {cwd}: {done.stdout}{done.stderr}")
    return done.stdout.strip()


def _pinned_paths(pin: dict) -> list[str]:
    return ([entry["path"] for entry in pin["files"]]
            + list(pin["pinned_by_commit_only"]))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _scratch_tree(tmp_path: Path) -> tuple[Path, Path, dict]:
    """An openxFactory-shaped tree whose pin HOLDS, ready to be broken one way.

    Built from the real pin's own member lists rather than from a hard-coded
    inventory, so the fixture cannot fall behind the pin it is imitating. The
    digests are recomputed from the scratch copies, and `commit:` is the scratch
    wallet's own — a fabricated pin over fabricated bytes, self-consistent, which
    is what makes each test's single mutation the whole cause of the refusal.
    """
    pin = _real_pin()
    submodule = pin["submodule_path"]
    root = tmp_path / "scratch-openxfactory"
    (root / "scripts").mkdir(parents=True)
    # `FAMILY_DIR.is_dir()` is checked ahead of the pin, and an empty directory
    # satisfies it: the pin refusal has to be what ends the run, not a missing
    # corpus behind it.
    (root / "contracts" / "trust-anchor").mkdir(parents=True)
    shutil.copy2(VALIDATOR, root / "scripts" / VALIDATOR.name)
    shutil.copy2(VERIFIER, root / "scripts" / VERIFIER.name)

    wallet = root / submodule
    for relative in _pinned_paths(pin):
        source = REPO_ROOT / submodule / relative
        assert source.exists(), (
            f"{submodule}/{relative} is named by the pin but absent from the "
            f"checkout; initialize the submodule "
            f"(`git submodule update --init {submodule}`)")
        target = wallet / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)

    _git("init", "-q", "-b", "main", ".", cwd=wallet)
    _git("add", "-A", cwd=wallet)
    _git("commit", "-qm", "scratch openXwallet", cwd=wallet)
    revision = _git("rev-parse", "HEAD", cwd=wallet)

    scratch_pin = dict(pin)
    scratch_pin["commit"] = revision
    scratch_pin["files"] = [{"path": entry["path"],
                             "sha256": _sha256(wallet / entry["path"])}
                            for entry in pin["files"]]
    pin_file = root / "contracts" / "openxwallet-pin.yaml"
    pin_file.write_text(yaml.safe_dump(scratch_pin, sort_keys=False),
                        encoding="utf-8")

    _git("init", "-q", "-b", "main", ".", cwd=root)
    # `advice.addEmbeddedRepo` off because the embedded repository IS the point:
    # the gitlink is what checks (2) and (3) read.
    _git("-c", "advice.addEmbeddedRepo=false", "add", "--",
         "contracts", "scripts", submodule, cwd=root)
    _git("commit", "-qm", "scratch openxFactory", cwd=root)
    assert _git("ls-tree", "HEAD", "--", submodule, cwd=root).split()[2] == \
        revision, "the fixture failed to record the gitlink it is testing"

    return root, wallet, scratch_pin


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    # No path argument: the repo scan is irrelevant here, and the pin refusal
    # comes before any of it.
    return subprocess.run(
        [sys.executable, str(root / "scripts" / VALIDATOR.name)],
        capture_output=True, text=True, cwd=str(root))


def _assert_refused(result: subprocess.CompletedProcess[str],
                    code: str) -> None:
    combined = result.stdout + result.stderr
    assert result.returncode == 2, combined
    assert code in _verifier().REFUSAL_CODES, (
        f"{code!r} is not in the verifier's refusal vocabulary "
        f"{_verifier().REFUSAL_CODES}")
    assert code in result.stderr, combined
    assert _verifier().REMEDIATION in result.stderr, (
        f"the refusal carries no remediation trailer: {combined}")
    # The composition context the old presence check carried, which is WHY an
    # unavailable parent set is fatal rather than skippable, survives the move to
    # the verifier.
    assert "openXwallet/contracts/openxwallet/openxwallet-custody.registry.yaml" \
        in result.stderr, combined
    # And the run stopped: `report()`'s summary line is the proof that a
    # refusal short-circuited rather than merely warning on the way through.
    assert "validate-trust-anchor:" not in result.stdout, combined


def test_an_uninitialized_submodule_refuses_by_name(tmp_path: Path) -> None:
    root, wallet, _ = _scratch_tree(tmp_path)
    # A clone taken without the scoped init: the gitlink is recorded, the
    # directory exists, and it is empty. `.git` is what is missing, and the check
    # tests for its EXISTENCE rather than `is_dir()` because a real submodule's
    # `.git` is a file.
    shutil.rmtree(wallet)
    wallet.mkdir()
    assert not (wallet / ".git").exists()

    _assert_refused(_run(root), "pin-submodule-uninitialized")


def test_a_digest_disagreeing_with_the_pin_refuses_by_name(
        tmp_path: Path) -> None:
    root, wallet, pin = _scratch_tree(tmp_path)
    # The custody registry itself, because it is the member rule (f) reads: the
    # bytes change in the WORKING TREE while the commit does not, so the recorded
    # gitlink and the checked-out revision both still equal `commit:` and the
    # digest is the only check left standing between this and a green run.
    member = wallet / REGISTRY_MEMBER
    member.write_text(member.read_text(encoding="utf-8")
                      + "\n# not the pinned bytes\n", encoding="utf-8")
    assert _sha256(member) != next(entry["sha256"] for entry in pin["files"]
                                  if entry["path"] == REGISTRY_MEMBER)
    assert _git("rev-parse", "HEAD", cwd=wallet) == pin["commit"], (
        "mutating the working tree must not move the revision, or this case "
        "would be caught by `pin-checkout-mismatch` instead")

    _assert_refused(_run(root), "pin-digest-mismatch")


def test_a_verifier_that_will_not_load_refuses_rather_than_falling_back(
        tmp_path: Path) -> None:
    root, wallet, _ = _scratch_tree(tmp_path)
    # The tree is otherwise SOUND and the custody registry is right where the old
    # `is_file()` check looked for it — which is the whole point: presence used to
    # be the entire question, and a validator that answered it when the verifier
    # was unavailable would be reporting a pin it never checked. The refusal has
    # to survive the loss of the thing that does the checking.
    (root / "scripts" / VERIFIER.name).unlink()
    assert (wallet / REGISTRY_MEMBER).is_file()

    result = _run(root)
    combined = result.stdout + result.stderr
    assert result.returncode == 2, combined
    assert "openxwallet-pin-unverifiable" in result.stderr, combined
    # The trailer still reaches the operator, from the validator's own held-equal
    # copy — the canonical constant is inside the module that would not load.
    assert _module().OPENXWALLET_REMEDIATION_FALLBACK in result.stderr, combined
    assert "validate-trust-anchor:" not in result.stdout, combined


def test_the_registry_literal_agrees_with_the_pins_submodule_path() -> None:
    # `OPENXWALLET_REGISTRY_PATH` writes `openXwallet` as a literal so that
    # resolving it cannot fail at import (a missing pin would otherwise take
    # every trust-anchor test down at collection). That literal duplicates
    # `submodule_path:`, and this is the check that keeps the duplication honest
    # — the one failure mode the design accepted in exchange for a constant that
    # cannot raise.
    module = _module()
    relative = module.OPENXWALLET_REGISTRY_PATH.relative_to(module.ROOT)
    assert relative.parts[0] == _real_pin()["submodule_path"], relative
    assert relative.as_posix() == \
        f"{_real_pin()['submodule_path']}/{REGISTRY_MEMBER}", relative


def test_the_registry_path_resolves_with_nothing_on_disk(
        tmp_path: Path) -> None:
    # The import-scope guarantee, proven rather than asserted about the source:
    # in a tree with no submodule, no pin and no corpus, importing the validator
    # still succeeds and the constant still resolves. Any pin read at import
    # would fail here — and would fail identically in
    # `test_negative_corpus.py`'s and `test_declaration_perimeter.py`'s
    # collection, where it would be an error rather than a refusal.
    root = tmp_path / "bare"
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(VALIDATOR, root / "scripts" / VALIDATOR.name)
    probe = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('v', {str(root / 'scripts' / VALIDATOR.name)!r})\n"
        "m = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(m)\n"
        "print(m.OPENXWALLET_REGISTRY_PATH.relative_to(m.ROOT).as_posix())\n")
    done = subprocess.run([sys.executable, "-c", probe],
                          capture_output=True, text=True, cwd=str(root))
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.strip() == \
        f"{_real_pin()['submodule_path']}/{REGISTRY_MEMBER}", done.stdout


def test_the_unverifiable_fallback_matches_the_canonical_remediation() -> None:
    # The validator keeps ONE copy of the trailer, for the case where the
    # verifier will not load and its constant therefore cannot be read. A copy is
    # what the design refused — three strings that drift — so it is held equal to
    # the canonical one here. Delete this test and the copy becomes the drift.
    assert _module().OPENXWALLET_REMEDIATION_FALLBACK == \
        _verifier().REMEDIATION
