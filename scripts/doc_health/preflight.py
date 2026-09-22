"""Per-repo validator preflight.

Each repo's own validators run before any family; a validator failure is a
finding (severity error), never a crash. Entrypoints are discovered, not
hardcoded per repo name, so new family repos join the preflight by
convention.
"""

from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path

from . import ERROR, Finding

# openxFactory's validators that run without arguments; the pin validator
# needs domain paths, so the suite invokes it separately with every domain.
_OPENX_NOARG = (
    "scripts/validate-avatar-first-ui.py",
    "scripts/validate-installation-templates.py",
    "scripts/validate-intake-templates.py",
    "scripts/validate-memory-gateway.py",
)

# The bound on ONE entrypoint (#1128). It is DELIBERATELY not the 30 s the git
# readers in this package bind (`corpus.RealGit`, `pin_class._git`): those are
# single git plumbing calls, and an entrypoint here is a whole repository's
# validator suite — `bash scripts/validate-docs.sh`, `make validate`, or a
# python validator that spawns git subprocesses of its own
# (`validate-domain-openxfactory-pins.py` does). A bound tight enough to cut a
# HONEST slow validator would convert a green nightly into an ERROR finding,
# which is a defect this fix would have introduced rather than removed.
#
# 120 s is measured, not picked: the slowest entrypoint this repository can run
# is `scripts/validate-memory-gateway.py` at 3.26 s (2026-09-21, the four
# openxFactory no-arg validators measured at 0.12/0.49/0.77/3.26 s), so the
# bound carries ~37x headroom over the slowest thing actually observed. It is
# also small enough that the WHOLE preflight still fits inside its own job:
# `.github/workflows/doc-health-reusable.yml` bounds the job at
# `timeout-minutes: 45`, and even if every one of the ~13 entrypoints an
# aggregation run discovers timed out, 13 x 120 s = 26 min, so the timeouts
# surface as the Findings below rather than as a killed job with no report at
# all — which is the outcome an unbounded call, or a far larger bound, gives.
_ENTRYPOINT_TIMEOUT_SECONDS = 120

# How long the group kill itself is given to drain the pipes before the finding
# is recorded anyway. Something that outlives SIGKILL (an uninterruptible wait,
# a namespace this process may not signal) must not become the very block the
# bound above exists to prevent.
_GROUP_REAP_SECONDS = 5


def _terminate_group(proc: subprocess.Popen) -> None:
    """SIGKILL the whole session the child was given, not just the child.

    `subprocess.run(timeout=…)` kills and reaps the DIRECT child only, and
    every entrypoint here is a wrapper whose real work is done by children of
    its own: `bash scripts/validate-docs.sh`, `make validate`, or a python
    validator that spawns git (`validate-domain-openxfactory-pins.py` has its
    own `_git`). Killing only the wrapper would leave that work — including a
    network read — running after the finding is recorded, and a nightly that
    times out repeatedly would accumulate them (Copilot, PR #1142).

    MEASURED, not argued: with the parent-only kill this file carried one
    commit ago, a `bash` wrapper's backgrounded child was still RUNNING (not
    even a zombie) after the bound fired. With the group kill it is dead
    before the finding is recorded.

    A surviving grandchild can ALSO hold the inherited stdout/stderr pipe
    open, which would make the drain after a kill wait on the very process
    the bound just gave up on. That did NOT reproduce in the measurement
    above — the drain returned at once — so it is named here as the reason
    the drain below is itself bounded, not as a defect anyone observed.

    POSIX only, and guarded rather than assumed: where there are no process
    groups the direct child is all there is to kill, which is exactly the
    behaviour `subprocess.run` already had.

    THE GROUP ID IS `proc.pid`, NOT A LOOKUP OF IT (Copilot, PR #1142).
    `_run_entrypoint` spawns with `start_new_session=True` on exactly this
    branch, so the child calls `setsid()` and IS the session and process-group
    leader: the group id EQUALS the child pid by construction. `os.getpgid`
    was therefore asking the kernel for a number this function already had —
    and asking can FAIL where the answer stays valid. If the leader has exited
    and been reaped while a descendant still holds the group (and the inherited
    stdout/stderr pipe, which is what made `communicate` block into the timeout
    in the first place), the lookup raises `ProcessLookupError`, cleanup falls
    to `_kill_direct`, and `proc.kill()` on an already-gone leader is a no-op.
    THE DESCENDANT THEN SURVIVES while the timeout finding is recorded — which
    is precisely the accumulation this function exists to prevent, arriving by
    the one route the lookup opened. Signalling the group directly cannot meet
    that failure, because a process group outlives its leader as long as any
    member remains.

    PID REUSE IS NOT A RISK HERE, and the ordering is what makes that true
    rather than luck: `_terminate_group` runs BEFORE the reaping
    `communicate()` in every caller, so the direct child is at worst a ZOMBIE
    still holding its pid. An unreaped pid cannot be recycled, so `proc.pid` is
    still this group's number and no other's. A kill-after-reap would be a
    different function, and it is not this one."""
    if os.name != "posix" or not hasattr(os, "killpg"):
        _kill_direct(proc)
        return
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except OSError:
        # `ProcessLookupError` (the whole group is already gone) and
        # `PermissionError` (not ours to signal) are the two expected shapes,
        # and both are `OSError`; the direct child is still ours either way.
        _kill_direct(proc)


def _kill_direct(proc: subprocess.Popen) -> None:
    """`proc.kill()`, and an already-gone child is not an error.

    THE FALLBACK MUST NOT RAISE THE RACE IT IS THE FALLBACK FOR (Copilot,
    PR #1142). Every caller of `_terminate_group` is inside
    `_run_entrypoint`'s `except subprocess.TimeoutExpired` handler, whose whole
    job is to RE-RAISE that timeout so `run_preflight` can turn it into a
    finding. If the child exits between `communicate()` timing out and this
    cleanup, the group signal above raises `ProcessLookupError` — which is why
    this fallback is reached at all — and a bare `proc.kill()` can then raise
    the SAME `ProcessLookupError` from inside the `except` that was handling
    it. That second exception REPLACES the `TimeoutExpired`, escapes
    `run_preflight`'s handler, and takes the run down at precisely the moment
    an entrypoint was supposed to become an ordinary preflight finding.

    So the direct kill swallows `OSError` and nothing else: a child that is
    already gone needs no killing, and a signal we are not permitted to send
    is not a reason to lose the timeout. Every other exception still
    propagates."""
    try:
        proc.kill()
    except OSError:
        pass


def _run_entrypoint(cmd: list[str], cwd: Path,
                    env: dict) -> subprocess.CompletedProcess:
    """`subprocess.run(capture_output=True, text=True, timeout=…)`, except
    that a timeout takes the entrypoint's DESCENDANTS down with it.

    `run()` cannot do this itself — on timeout it kills its own child and
    re-raises, and by then the `Popen` it built is out of reach — so the one
    site that spawns wrappers builds the `Popen` here instead. Every other
    semantic `run()` gave is kept: captured text output, the same
    `CompletedProcess` on success, the same `OSError` when the command cannot
    be spawned at all, and the same `subprocess.TimeoutExpired` re-raised to
    the caller after the group is gone."""
    proc = subprocess.Popen(
        cmd, cwd=cwd, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=(os.name == "posix"))
    try:
        out, err = proc.communicate(timeout=_ENTRYPOINT_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        _terminate_group(proc)
        try:
            proc.communicate(timeout=_GROUP_REAP_SECONDS)
        except subprocess.TimeoutExpired:
            pass                      # see _GROUP_REAP_SECONDS
        raise                         # the ORIGINAL timeout, for the caller
    except BaseException:
        # A KeyboardInterrupt or anything else out of the wait must not strand
        # the session this function created.
        _terminate_group(proc)
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def _entrypoints(repo: str, repo_path: Path,
                 domain_paths: list[Path]) -> list[list[str]]:
    cmds: list[list[str]] = []
    if repo == "openxFactory":
        for rel in _OPENX_NOARG:
            if (repo_path / rel).is_file():
                cmds.append(["python3", rel])
        if (repo_path / "scripts/validate-domain-openxfactory-pins.py").is_file() and domain_paths:
            cmds.append(["python3", "scripts/validate-domain-openxfactory-pins.py",
                         *[str(p) for p in domain_paths]])
        return cmds
    if (repo_path / "scripts/validate-docs.sh").is_file():
        cmds.append(["bash", "scripts/validate-docs.sh"])
    elif (repo_path / "Makefile").is_file() and \
            "validate:" in (repo_path / "Makefile").read_text(encoding="utf-8"):
        cmds.append(["make", "validate"])
    return cmds


def run_preflight(repo_paths: dict[str, Path]):
    """Returns (findings, log) where log is (repo, cmd, ok, tail)."""
    findings, log = [], []
    domain_paths = [p for n, p in sorted(repo_paths.items())
                    if n != "openxFactory" and (p / "stack.yaml").is_file()]
    for repo in sorted(repo_paths):
        repo_path = repo_paths[repo]
        cmds = _entrypoints(repo, repo_path, domain_paths)
        if not cmds:
            log.append((repo, "(none)", True, "no validator entrypoint found"))
            continue
        for cmd in cmds:
            try:
                proc = _run_entrypoint(
                    cmd, repo_path,
                    {**os.environ, "DOC_HEALTH_PREFLIGHT": "1"})
            except (OSError, subprocess.TimeoutExpired) as exc:
                # #1128: an entrypoint that never returns used to block
                # `run_suite` (runner.py:227) before a single family ran — it
                # is the FIRST thing the suite does whenever no `--family` is
                # passed, which is how the nightly invokes it. A bounded
                # failure becomes the SAME Finding an ordinary validator
                # failure already produces two branches below, same family and
                # same path so regression matching is unchanged, with the
                # reason standing in for the output tail there is none of. An
                # unrunnable entrypoint (`OSError` — no `bash`, no `make`)
                # takes the same route: it was never caught here either. The
                # timeout has already taken the whole process group with it by
                # the time this runs — see `_terminate_group`.
                reason = (
                    f"timed out after {_ENTRYPOINT_TIMEOUT_SECONDS}s"
                    if isinstance(exc, subprocess.TimeoutExpired)
                    else f"could not be run: {exc}")
                log.append((repo, " ".join(cmd), False, reason))
                findings.append(Finding(
                    ERROR, "preflight", repo,
                    cmd[1] if len(cmd) > 1 else cmd[0],
                    f"preflight validator {reason}: {' '.join(cmd)}",
                    "fix the repo's own validator failures first"))
                continue
            ok = proc.returncode == 0
            tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
            log.append((repo, " ".join(cmd), ok, " / ".join(tail)))
            if not ok:
                # "preflight" is a reporting section, not a contract family;
                # regression matching (family + path) still applies to it.
                findings.append(Finding(
                    ERROR, "preflight", repo,
                    cmd[1] if len(cmd) > 1 else cmd[0],
                    f"preflight validator failed: {' '.join(cmd)}",
                    "fix the repo's own validator failures first"))
    return findings, log
