"""THE ABSENCE OF GIT RE-DERIVATION IS PINNED, BECAUSE AN ABSENCE ROTS SILENTLY.

`add-consent-custody-rederivation-record` design C-7 splits the custody-currency
obligation: `scripts/validate-consent-instruments.py` takes only the legs
derivable from the RECORD'S OWN BYTES, and the git re-derivation runs in the
CONSUMING repository where the target's bytes and history are. openxFactory
holds no consent instruments at all, so a re-derivation harness here would need
a consumer checkout, a network, or a vendored copy of another repository's
history — all three refused by this validator family's posture.

Nothing enforces that split except this file. Task 3.3 asks for the absence to
be asserted so "a helpful later edit fails on the developer's machine first",
and a later reader adding `subprocess.run(["git", "show", ...])` to close what
looks like an obvious gap is exactly the edit meant.

BOTH ASSERTIONS ARE ARGUMENT-SCOPED, and the naive forms do not work:

* A bare "the module contains no `git` token" ban reds forever on
  `SKIP_DIR_NAMES`' `".git"` entry, which is a DIRECTORY-NAME EXCLUSION making
  the tree walk skip a git directory — the opposite of reading one. That exact
  token is allowlisted.
* A bare "the module opens no file" ban is false of a validator whose whole job
  is reading its own schemas and corpus. What must not happen is an open
  ESCAPING the corpus root: a `custody.locator` names a file in another
  repository, so any path resolving outside the root is the forbidden read.
"""

from __future__ import annotations

import builtins
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-consent-instruments.py"
EXAMPLES = ROOT / "examples" / "consent-instrument"

#: `SKIP_DIR_NAMES`' directory-name exclusion. Allowlisted BY EXACT TOKEN, never
#: by substring: `".git"` in a skip set is the opposite of reading a repository.
ALLOWED_GIT_TOKENS = {'".git"'}

#: The three buckets. The withheld one is included deliberately — it is the leg
#: most likely to tempt a later editor into opening a repository, because it is
#: the one whose verdict a reader most wants confirmed.
BUCKETS = ("positive", "negative", "withheld")


def _source() -> str:
    return VALIDATOR.read_text(encoding="utf-8")


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_consent_instruments_under_test", VALIDATOR
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_the_module_does_not_import_subprocess() -> None:
    source = _source()
    assert not re.search(r"^\s*import subprocess\b", source, re.M), (
        "validate-consent-instruments.py imports subprocess — the neutral "
        "validator performs no git re-derivation (design C-7); the legs that "
        "need a repository belong to the consuming repository's custody-digest "
        "check"
    )
    assert not re.search(r"^\s*from subprocess\b", source, re.M)


@pytest.mark.parametrize("call", ["subprocess.", "os.system", "os.popen"])
def test_the_module_shells_out_to_nothing(call: str) -> None:
    assert call not in _source(), (
        f"validate-consent-instruments.py calls {call} — this validator is "
        f"network-free and reads ONE repository, and shelling out is how a "
        f"re-derivation leg would arrive by the back door"
    )


def test_the_only_git_token_is_the_skip_set_entry() -> None:
    """A `git` token is banned; the skip-set directory name is allowlisted.

    Allowlisting is BY EXACT TOKEN. A substring allowance would also admit
    ``"git", "show"`` and defeat the ban it exists to keep implementable.
    """
    found = {match.group(0) for match in re.finditer(r'"[^"\n]*git[^"\n]*"',
                                                     _source())}
    unexpected = found - ALLOWED_GIT_TOKENS
    assert not unexpected, (
        f"validate-consent-instruments.py carries git token(s) {sorted(unexpected)} "
        f"beyond the allowlisted SKIP_DIR_NAMES entry — a re-derivation leg has "
        f"crossed the C-7 line into the neutral validator"
    )


@pytest.mark.parametrize("bucket", BUCKETS)
def test_no_subprocess_is_launched_over_any_bucket(bucket: str, monkeypatch) -> None:
    """Runtime half, part one: nothing is executed, over all three buckets."""
    module = _load_validator()

    def refuse(*args, **kwargs):  # pragma: no cover - the point is not reaching it
        raise AssertionError(
            f"the validator launched a subprocess while checking the {bucket} "
            f"bucket: {args!r} — the git legs are the consuming repository's"
        )

    for name in ("run", "Popen", "check_output", "call", "check_call"):
        monkeypatch.setattr(subprocess, name, refuse, raising=False)

    findings = module.Findings()
    module.self_test(findings, module.load_schemas())
    assert not findings.errors, findings.errors


@pytest.mark.parametrize("bucket", BUCKETS)
def test_every_opened_path_stays_under_the_corpus_root(bucket: str, monkeypatch) -> None:
    """Runtime half, part two: no read ESCAPES the repository.

    This is the checkable form of "reads no file named by a locator". A
    `custody.locator` points into the CONSUMING repository, so any open
    resolving outside this root would be the forbidden read — while the
    validator's own schemas and corpus, which it must read, stay inside it.
    """
    module = _load_validator()
    escapes: list[str] = []
    real_open = builtins.open
    real_path_open = Path.open

    def _record(path) -> None:
        try:
            resolved = Path(path).resolve()
        except (OSError, TypeError, ValueError):
            return
        if ROOT not in resolved.parents and resolved != ROOT:
            escapes.append(str(resolved))

    def guarded_open(file, *args, **kwargs):
        _record(file)
        return real_open(file, *args, **kwargs)

    def guarded_path_open(self, *args, **kwargs):
        _record(self)
        return real_path_open(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(Path, "open", guarded_path_open)

    findings = module.Findings()
    module.self_test(findings, module.load_schemas())

    monkeypatch.undo()
    assert not escapes, (
        f"while checking the {bucket} bucket the validator opened path(s) "
        f"outside the repository root: {escapes} — a locator target lives in a "
        f"CONSUMING repository, and reading one here would cross the C-7 line"
    )
    assert not findings.errors, findings.errors
