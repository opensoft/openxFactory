"""The credential-contracts validator's dispatch-credential self-test gates the
packaged examples (add-dispatch-credential-contract task 2.2): the positives are
schema-valid with no semantic finding, and each negative raises its intended
code — dispatch-scope-ceiling, shared-secret-identity, baked-secret.

Matches the repo's validator-gating pattern: invoke the script, assert exit 0.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-credential-contracts.py"
EXAMPLES = ROOT / "examples" / "credential-contracts"


def _run() -> subprocess.CompletedProcess[str]:
    # the validator runs its self-test on every invocation; the positional arg
    # is the (here empty) domain-repo scan target.
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True,
        text=True,
    )


def test_selftest_passes_on_the_packaged_examples() -> None:
    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test: 2 positive + 3 negative example(s) confirmed" in result.stdout


def test_the_example_files_are_present() -> None:
    # guards against a self-test that passes vacuously because a rename dropped
    # the fixtures out of the glob.
    assert (EXAMPLES / "openxdox-dispatch.requirements.example.yaml").is_file()
    assert (EXAMPLES / "openxdox-dispatch.binding-template.example.yaml").is_file()
    for neg in (
        "dispatch-reuses-content-secret.yaml",
        "dispatch-grants-contents.yaml",
        "baked-secret-in-binding.yaml",
    ):
        assert (EXAMPLES / "negative" / neg).is_file(), neg
