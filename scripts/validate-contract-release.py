#!/usr/bin/env python3
"""Thin CLI over the release digest inventory verifier (T074).

Subcommands mirror the planning contract and quickstart:

    validate-contract-release.py build --tag <tag> --output <path>
    validate-contract-release.py verify-commit --commit <sha>
    validate-contract-release.py verify-promotion --commit <sha> --remote <name> --tag <tag>
    validate-contract-release.py verify-tag --remote <name> --tag <tag>

Exit codes: 0 pass, 1 findings, 2 dependency/harness (mirroring
``validate-hermes-runtime-contracts.py::classify_exit_code``).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

# ``python scripts/validate-contract-release.py`` otherwise places only the
# scripts directory on sys.path; add the repository root so this thin entrypoint
# reuses the importable validation package.
_ENTRYPOINT_REPO = Path(__file__).resolve().parents[1]
if str(_ENTRYPOINT_REPO) not in sys.path:
    sys.path.insert(0, str(_ENTRYPOINT_REPO))

from scripts.hermes_runtime_validation import release  # noqa: E402
from scripts.hermes_runtime_validation.content import (  # noqa: E402
    ContentResolutionError,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--tag", required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--json", action="store_true", dest="as_json")

    verify_commit = subparsers.add_parser("verify-commit")
    verify_commit.add_argument("--commit", required=True)
    verify_commit.add_argument("--json", action="store_true", dest="as_json")

    verify_promotion = subparsers.add_parser("verify-promotion")
    verify_promotion.add_argument("--commit", required=True)
    verify_promotion.add_argument("--remote", required=True)
    verify_promotion.add_argument("--tag", required=True)
    verify_promotion.add_argument("--json", action="store_true", dest="as_json")

    verify_tag = subparsers.add_parser("verify-tag")
    verify_tag.add_argument("--remote", required=True)
    verify_tag.add_argument("--tag", required=True)
    verify_tag.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _git_root(path: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def _render(
    findings: list[dict[str, str]],
    *,
    as_json: bool,
    exit_code: int,
    command: str,
    summary: dict[str, Any],
) -> None:
    findings = sorted(
        findings,
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )
    if as_json:
        payload = {
            "command": command,
            "exit_code": exit_code,
            "findings": findings,
            "status": "pass" if exit_code == 0 else "error",
            "summary": summary,
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return
    if exit_code == 0 and not findings:
        print(f"release {command}: pass")
        for key in sorted(summary):
            print(f"  {key}={summary[key]}")
        return
    for finding in findings:
        path = f" path={finding['path']}" if finding.get("path") else ""
        print(
            f"{finding['code']} {finding.get('severity', 'error')}{path}: "
            f"{finding['message']}"
        )


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    command = str(arguments.command)
    repo_root = _git_root(arguments.repo or _ENTRYPOINT_REPO)
    if repo_root is None:
        print(
            "validate-contract-release: repository is not an available Git root",
            file=sys.stderr,
        )
        return 2

    try:
        findings: list[dict[str, str]] = []
        summary: dict[str, Any] = {}
        if command == "build":
            inventory = release.build_release_inventory(
                repo_root, bundle_tag=arguments.tag
            )
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            arguments.output.write_text(
                release.dump_inventory(inventory), encoding="utf-8"
            )
            summary = {
                "bundle_tag": arguments.tag,
                "entries": len(inventory["entries"]),
                "output": str(arguments.output),
            }
        elif command == "verify-commit":
            committed = release.resolve_committed_inventory(repo_root, arguments.commit)
            if committed is None:
                findings = [
                    {
                        "code": "HGR-RELEASE-INVENTORY-MISSING",
                        "severity": "error",
                        "path": release.RELEASES_DIRECTORY,
                        "message": "the commit records no release digest inventory",
                    }
                ]
            else:
                findings = release.verify_inventory_against_commit(
                    repo_root, arguments.commit, committed[1]
                )
                summary = {"inventory": committed[0]}
        elif command == "verify-promotion":
            findings = release.verify_promotion(
                repo_root,
                commit=arguments.commit,
                remote=arguments.remote,
                tag=arguments.tag,
            )
        elif command == "verify-tag":
            findings = release.verify_tag(
                repo_root, remote=arguments.remote, tag=arguments.tag
            )
    except (release.ReleaseDependencyError, ContentResolutionError) as exc:
        print(f"validate-contract-release: {exc}", file=sys.stderr)
        return 2

    exit_code = 1 if findings else 0
    _render(
        findings,
        as_json=arguments.as_json,
        exit_code=exit_code,
        command=command,
        summary=summary,
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
