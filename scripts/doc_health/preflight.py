"""Per-repo validator preflight.

Each repo's own validators run before any family; a validator failure is a
finding (severity error), never a crash. Entrypoints are discovered, not
hardcoded per repo name, so new family repos join the preflight by
convention.
"""

from __future__ import annotations

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
                proc = subprocess.run(cmd, cwd=repo_path, capture_output=True,
                                      text=True,
                                      timeout=_ENTRYPOINT_TIMEOUT_SECONDS,
                                      env={**__import__("os").environ,
                                           "DOC_HEALTH_PREFLIGHT": "1"})
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
                # takes the same route: it was never caught here either.
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
