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
            proc = subprocess.run(cmd, cwd=repo_path, capture_output=True,
                                  text=True,
                                  env={**__import__("os").environ,
                                       "DOC_HEALTH_PREFLIGHT": "1"})
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
