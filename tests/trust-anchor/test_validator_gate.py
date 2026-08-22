"""The trust-anchor validator's own gate: invoke it, assert exit 0.

Matches the repo's validator-gating pattern (`tests/credential_contracts/`,
`tests/conformance-gate/`): run the script the way CI runs it and hold it to its
exit code and its own reported counts.

Why the counts are asserted rather than just the exit code: the self-test can
pass VACUOUSLY. A rename that drops the packaged corpus out of the glob leaves
zero positives and zero negatives, and `examples-missing` is the only thing
standing between that and a green bar — so the numbers the run reports are part
of what is being gated, and a change that moves them is a change a reader should
have to acknowledge.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-trust-anchor.py"
FAMILY = REPO_ROOT / "contracts" / "trust-anchor"

# The corpus as this suite expects to find it. Kept as one string so the
# assertion failure prints the note the run actually emitted beside it.
EXPECTED_NOTE = ("corpus: 34 positive example(s), 65 negative confirmation(s) "
                 "across 8/8 requirements")


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), *args],
                          capture_output=True, text=True, cwd=REPO_ROOT)


def test_self_test_is_green() -> None:
    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 error(s), 0 warning(s)" in result.stdout


def test_self_test_reports_the_expected_corpus() -> None:
    result = _run()
    assert EXPECTED_NOTE in result.stdout, result.stdout


def test_repo_scan_is_green_under_strict() -> None:
    # `--strict` is the mode the bar runs: it turns warnings into a nonzero exit,
    # which is what makes the two WARNING-level rules (a declaration whose
    # `cannot` set is broad, and a binding requiring a partially-satisfied
    # obligation) cost something in CI rather than only in a log.
    result = _run(str(REPO_ROOT), "--strict")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 error(s), 0 warning(s)" in result.stdout


def test_the_packaged_corpus_is_present() -> None:
    # Guards against a self-test that passes because the fixtures moved.
    assert (FAMILY / "trust-anchor-chain-custody.registry.yaml").is_file()
    positives = sorted((FAMILY / "examples").glob("*.example.yaml"))
    negatives = sorted((FAMILY / "examples" / "negative").glob("*.yaml"))
    assert len(positives) == 34, [p.name for p in positives]
    assert len(negatives) == 65, [p.name for p in negatives]


def test_the_review_hardening_fixtures_are_present() -> None:
    # The probes the adversarial review of 2026-08-21 contributed. Named
    # individually because each one is the only thing standing between a rule and
    # the bypass it was written for, and a deletion should read as a deletion.
    for name in (
        "conformance-declaration-family-operated-excusing-its-own-authority-key.yaml",
        "anchor-excusing-a-family-operated-authority-key.yaml",
        "certificate-reaching-holder-assurance-under-a-host-readable-root.yaml",
        "anchor-shortfall-cited-with-no-claim-moment.yaml",
        "authority-key-material-as-unarmored-pkcs8-der.yaml",
        "authority-key-material-as-hex-pkcs8-der.yaml",
        "authority-key-material-double-base64-encoded.yaml",
        "authority-key-material-with-the-armor-label-split-across-fields.yaml",
        "authority-key-material-as-der-labelled-qa-only.yaml",
        "issuance-at-the-floor-under-a-family-operated-authority.yaml",
        "issuance-asserting-a-level-above-the-declared-achievement.yaml",
        "certificate-superseded-with-no-renewal-record.yaml",
        "dependent-binding-current-at-a-superseded-generation.yaml",
        "certificate-revocation-not-reaching-its-dependent-authority.yaml",
        "propagation-evidenced-after-the-window-closed.yaml",
        "dependent-binding-declaring-no-required-obligations.yaml",
        "chain-custody-registry-claiming-the-canonical-registry-id.yaml",
        "certificate-citing-a-registry-it-does-not-derive-from.yaml",
        "custody-registry-variant-floor-above-its-own-weakest-member.yaml",
        "expired-certificate-recorded-as-trusted.yaml",
        "certificate-evaluated-after-its-validity-recorded-as-trusted.yaml",
        "conformance-declaration-with-a-duplicated-entry-id.yaml",
    ):
        assert (FAMILY / "examples" / "negative" / name).is_file(), name
