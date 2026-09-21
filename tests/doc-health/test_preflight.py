"""The per-repo validator preflight, and the bound on ONE entrypoint (#1128).

`run_preflight` is the FIRST thing `run_suite` does whenever no `--family` is
passed (`runner.py:227`), which is exactly how the nightly invokes doc-health
(`.github/workflows/doc-health-reusable.yml` passes no `--family` at several
steps, and `skip-families` defaults to `notebook-projection-drift` only, so
preflight is never skipped). Its `subprocess.run` carried no `timeout=` and the
file carried no `try`/`except` at all, so ONE entrypoint that never returned
blocked the whole suite before a single family ran — and the entrypoint is not
fixed to `git`: `_entrypoints` builds `python3 <validator>`, `bash
scripts/validate-docs.sh` or `make validate` per discovered repository, so the
exposure was the slowest thing any domain repo's own validator does.

This module is new with the fix (#1128 measured that nothing tested this file),
so it pins the surrounding contract as well as the bound: an ordinary validator
failure must still be the Finding it always was, because a fix that moved THAT
would be a worse defect than the one it repairs.
"""

from __future__ import annotations

import subprocess

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from doc_health import ERROR, preflight


def _repo_with_validator(tmp_path, body: str, *, name: str = "driftFactory"):
    """A discovered repository whose entrypoint is `bash scripts/validate-docs.sh`
    — the ordinary domain-repo shape `_entrypoints` finds by convention."""
    repo = tmp_path / name
    (repo / "scripts").mkdir(parents=True)
    script = repo / "scripts" / "validate-docs.sh"
    script.write_text(body, encoding="utf-8")
    script.chmod(0o755)
    return {name: repo}


def test_a_validator_failure_is_still_the_finding_it_always_was(tmp_path):
    """The baseline the bound must not move: a real entrypoint that exits
    non-zero is one ERROR finding in the `preflight` section, keyed by the
    script path, with the tail of its own output in the log row."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\necho 'a real finding'\n"
                                           "exit 1\n")
    findings, log = preflight.run_preflight(paths)

    assert len(findings) == 1, findings
    finding = findings[0]
    assert (finding.severity, finding.family) == (ERROR, "preflight")
    assert finding.repo == "driftFactory"
    assert finding.path == "scripts/validate-docs.sh"
    assert "preflight validator failed" in finding.rule
    assert log == [("driftFactory", "bash scripts/validate-docs.sh", False,
                    "a real finding")]


def test_an_entrypoint_that_never_returns_times_out_into_that_same_finding(
        tmp_path, monkeypatch):
    """#1128: bounded, an entrypoint that will not return becomes the SAME
    `Finding(ERROR, "preflight", ...)` an ordinary validator failure produces —
    same family and same path, so regression matching between two reports is
    unchanged — with the timeout named in the message in place of the output
    tail there is none of. Asserted on the bound the call carries, not on
    elapsed time: a shim that sleeps would prove only that the shim exited."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\nexit 0\n")
    calls = []

    def never_returns(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        raise subprocess.TimeoutExpired(cmd=list(argv),
                                        timeout=kwargs.get("timeout"))

    monkeypatch.setattr(subprocess, "run", never_returns)
    findings, log = preflight.run_preflight(paths)

    assert calls, "the entrypoint must still be attempted"
    assert calls[0][1].get("timeout") == preflight._ENTRYPOINT_TIMEOUT_SECONDS
    assert calls[0][1]["timeout"] == 120, (
        "the entrypoint bound is deliberately NOT the 30s the git readers "
        "bind — this is a whole repository's validator suite, and a bound "
        "tight enough to cut an honest slow validator would turn a green "
        f"nightly into an ERROR finding; saw {calls[0][1]['timeout']!r}")

    assert len(findings) == 1, findings
    finding = findings[0]
    assert (finding.severity, finding.family) == (ERROR, "preflight"), (
        "a timeout must reach the finding-producing path, which a hang never "
        "could: it blocked run_suite before any family ran at all")
    assert finding.repo == "driftFactory"
    assert finding.path == "scripts/validate-docs.sh", (
        "same key as an ordinary failure, or regression matching between two "
        "reports would see a different finding")
    assert "timed out after 120s" in finding.rule, finding.rule
    assert log == [("driftFactory", "bash scripts/validate-docs.sh", False,
                    "timed out after 120s")]


def test_an_unrunnable_entrypoint_is_a_finding_rather_than_a_raised_OSError(
        tmp_path, monkeypatch):
    """The second half of the same two-part gap #1098 measured in `corpus.py`
    and #1128 measured here: the file caught NOTHING, so an entrypoint that
    could not be spawned at all raised `OSError` straight out of `run_suite`
    before any family ran. Proven against a real unrunnable command rather
    than a raised double — an emptied `PATH` leaves no `bash` to exec."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\nexit 0\n")
    empty_bin = tmp_path / "empty-bin"
    empty_bin.mkdir()
    monkeypatch.setenv("PATH", str(empty_bin))

    findings, log = preflight.run_preflight(paths)

    assert len(findings) == 1, findings
    assert (findings[0].severity, findings[0].family) == (ERROR, "preflight")
    assert findings[0].path == "scripts/validate-docs.sh"
    assert "could not be run" in findings[0].rule, findings[0].rule
    assert log and log[0][2] is False


def test_a_clean_validator_reports_no_finding(tmp_path):
    """The passing path, pinned beside the failing ones so the bound cannot be
    shown to work by making everything a finding."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\nexit 0\n")
    findings, log = preflight.run_preflight(paths)

    assert findings == []
    assert log == [("driftFactory", "bash scripts/validate-docs.sh", True, "")]
