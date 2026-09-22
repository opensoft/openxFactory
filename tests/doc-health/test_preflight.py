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

This module is new with the bind (#1128 measured that nothing tested this file),
so it pins the surrounding contract as well as the bound: an ordinary validator
failure must still be the Finding it always was, because a fix that moved THAT
would be a worse defect than the one it repairs.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

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
    elapsed time: a shim that sleeps would prove only that the shim exited.

    It also pins the two halves the group kill needs (Copilot, PR #1142): the
    child is asked for its OWN session, and the group is taken down BEFORE the
    finding is recorded."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\nexit 0\n")
    waits, spawns, terminated = [], [], []

    class NeverReturns:
        """A `Popen` whose wait never finishes. Its `pid` is deliberately not a
        real one: `_terminate_group` is stubbed out below, so nothing here can
        signal a live process by accident."""

        def __init__(self, argv, **kwargs):
            self.args, self.pid, self.returncode = argv, -1, None
            spawns.append((list(argv), dict(kwargs)))

        def communicate(self, timeout=None):
            waits.append(timeout)
            raise subprocess.TimeoutExpired(cmd=self.args, timeout=timeout)

        def kill(self):
            pass

    monkeypatch.setattr(subprocess, "Popen", NeverReturns)
    monkeypatch.setattr(preflight, "_terminate_group",
                        lambda proc: terminated.append(proc))
    findings, log = preflight.run_preflight(paths)

    assert spawns, "the entrypoint must still be attempted"
    assert spawns[0][1].get("start_new_session") is True, (
        "the entrypoint must get its own session, or the timeout can only "
        "reach the wrapper and not the work it spawned")
    assert waits and waits[0] == preflight._ENTRYPOINT_TIMEOUT_SECONDS
    assert waits[0] == 120, (
        "the entrypoint bound is deliberately NOT the 30s the git readers "
        "bind — this is a whole repository's validator suite, and a bound "
        "tight enough to cut an honest slow validator would turn a green "
        f"nightly into an ERROR finding; saw {waits[0]!r}")
    assert terminated, (
        "the process group must be taken down before the finding is recorded")
    assert waits[1:] == [preflight._GROUP_REAP_SECONDS], (
        "the drain that follows the kill is itself bounded, so something that "
        "outlives SIGKILL cannot become the block the timeout exists to stop")

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


# --------------------------------------------------------------------------
# The DESCENDANTS of a timed-out entrypoint (Copilot, PR #1142)
#
# `subprocess.run(timeout=…)` kills and reaps its own child and no more, and
# every entrypoint discovered here is a WRAPPER — `bash validate-docs.sh`,
# `make validate`, a python validator that spawns git — so bounding only the
# parent left the actual work running after the finding was recorded. The
# entrypoint is therefore started in its own session and the whole group is
# killed. Proven by a real process that outlives its parent, not by a double.
# --------------------------------------------------------------------------

def _alive(pid: int) -> bool:
    """Whether `pid` is a process that is still RUNNING.

    `os.kill(pid, 0)` alone is not that question. A killed process whose parent
    is gone gets reparented, and where the new parent does not reap it — PID 1
    in an ordinary container, measured here — it stays in the process table as a
    zombie and `os.kill(pid, 0)` keeps succeeding for it. A zombie has already
    been killed, which is precisely the property under test, so `/proc` is
    consulted for the state where it exists and `os.kill` is the fallback."""
    stat = Path(f"/proc/{pid}/stat")
    if stat.exists():
        try:
            return stat.read_text().rsplit(") ", 1)[1].split()[0] != "Z"
        except (OSError, IndexError):
            pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:          # alive, just not ours
        return True
    return True


def _gone_within(pid: int, seconds: float = 5.0) -> bool:
    """Reaping is not instantaneous; poll rather than look exactly once."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not _alive(pid):
            return True
        time.sleep(0.05)
    return not _alive(pid)


@pytest.mark.skipif(os.name != "posix", reason="process groups are POSIX")
def test_a_timed_out_entrypoint_takes_its_grandchild_with_it(tmp_path,
                                                             monkeypatch):
    """The wrapper spawns a long-lived child and then waits on it, which is the
    shape of every real entrypoint here. When the bound fires, that GRANDCHILD
    must be gone: killing only `bash` would leave the validator's own `git` (and
    its network read) running, and a nightly that times out repeatedly would
    accumulate them.

    It fails against the parent-only shape this file carried one commit ago
    (66fe57a2), where the grandchild was measured still RUNNING after the
    bound fired, and against `origin/main`, which binds nothing at all.

    The elapsed assertion below is a guard rather than a reproduction: a
    grandchild holding the captured pipe COULD make the post-kill drain wait
    on it, and that did not happen in the measurement above, so it is pinned
    here rather than claimed anywhere as observed."""
    pidfile = tmp_path / "grandchild.pid"
    paths = _repo_with_validator(
        tmp_path,
        f"#!/bin/sh\nsleep 300 &\necho $! > {pidfile}\nwait\n")
    monkeypatch.setattr(preflight, "_ENTRYPOINT_TIMEOUT_SECONDS", 1)

    started = time.monotonic()
    findings, log = preflight.run_preflight(paths)
    elapsed = time.monotonic() - started

    pid = int(pidfile.read_text(encoding="utf-8").strip())
    try:
        assert _gone_within(pid), (
            f"the grandchild ({pid}) outlived the timeout — only the direct "
            "child was killed, so the validator's real work (and any network "
            "read it holds) keeps running after the finding is recorded")
        assert elapsed < 30, (
            f"run_preflight took {elapsed:.1f}s against a 1s bound: the drain "
            "waited on something that outlived the kill, which would make the "
            "bound wait on the very process it gave up on")
        assert len(findings) == 1 and findings[0].family == "preflight"
        assert findings[0].severity == ERROR
        assert "timed out after 1s" in findings[0].rule, findings[0].rule
        assert log[0][2] is False
    finally:
        if _alive(pid):               # never leave one behind on a failure
            try:
                os.kill(pid, 9)
            except OSError:
                pass


# --------------------------------------------------------------------------
# OSError coverage beside the timeout coverage (Copilot, PR #1142)
#
# `test_an_unrunnable_entrypoint_is_a_finding_rather_than_a_raised_OSError`
# above already proves the real-world route (an emptied PATH, so `bash` cannot
# be exec'd). This pins the OTHER half of the same `except` — that the arm is
# reached at all and reports the reason — without depending on how a particular
# host spells its spawn failure.
# --------------------------------------------------------------------------

def test_a_spawn_failure_reports_its_reason_rather_than_raising(tmp_path,
                                                                monkeypatch):
    """Any `OSError` out of the spawn — no interpreter, a permission denial, a
    text-file-busy — must reach the same finding, with the reason carried into
    the message where a reader can see WHICH failure it was."""
    paths = _repo_with_validator(tmp_path, "#!/bin/sh\nexit 0\n")

    def cannot_spawn(*args, **kwargs):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(subprocess, "Popen", cannot_spawn)
    findings, log = preflight.run_preflight(paths)

    assert len(findings) == 1, findings
    assert (findings[0].severity, findings[0].family) == (ERROR, "preflight")
    assert findings[0].path == "scripts/validate-docs.sh"
    assert "could not be run" in findings[0].rule
    assert "Permission denied" in findings[0].rule, findings[0].rule
    assert log == [("driftFactory", "bash scripts/validate-docs.sh", False,
                    log[0][3])] and "Permission denied" in log[0][3]
