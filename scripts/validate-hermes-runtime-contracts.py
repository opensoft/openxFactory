#!/usr/bin/env python3
"""Deterministic command-line entrypoint for Hermes runtime contract checks."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import json
from pathlib import Path
import subprocess
from typing import Any

import yaml


def classify_exit_code(
    findings: Sequence[Mapping[str, Any]],
    *,
    strict: bool,
    dependency_error: bool = False,
) -> int:
    if dependency_error:
        return 2
    severities = {str(finding.get("severity", "error")) for finding in findings}
    if "error" in severities or (strict and "warning" in severities):
        return 1
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--case", dest="case_id")
    parser.add_argument("--phase", choices=("structural", "semantic", "all"), default="all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--require-candidate", action="store_true")
    parser.add_argument("--require-realization", action="store_true")
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--domain-repo", action="append", default=[], metavar="REPO=CHECKOUT")
    parser.add_argument("--domain-repo-root", type=Path)
    parser.add_argument("--handoff-receipt", type=Path)
    parser.add_argument("--consumer-repo", action="append", default=[], metavar="REPO=CHECKOUT")
    parser.add_argument("--consumer-repo-root", type=Path)
    return parser


def _finding(
    code: str, message: str, *, case_id: str = "", path: str = ""
) -> dict[str, str]:
    return {
        "code": code,
        "severity": "error",
        "case_id": case_id,
        "path": path,
        "message": message,
    }


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


def _indexed_case_ids(index_path: Path) -> set[str] | None:
    if not index_path.is_file():
        return None
    try:
        document = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return None
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list):
        return None
    return {
        case["case_id"]
        for case in document["cases"]
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    }


def _render(
    findings: list[dict[str, str]], *, mode: str, as_json: bool, exit_code: int
) -> None:
    findings.sort(key=lambda item: (item["case_id"], item["path"], item["code"]))
    if as_json:
        payload = {
            "findings": findings,
            "mode": mode,
            "status": "pass" if exit_code == 0 else "error",
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return
    if not findings:
        print("Hermes runtime contracts: pass")
        return
    for finding in findings:
        case = f" case={finding['case_id']}" if finding["case_id"] else ""
        path = f" path={finding['path']}" if finding["path"] else ""
        print(
            f"{finding['code']} {finding['severity']}{case}{path}: "
            f"{finding['message']}"
        )


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    mode = (
        "realization"
        if arguments.require_realization
        else "candidate" if arguments.require_candidate else "standard"
    )
    findings: list[dict[str, str]] = []
    dependency_error = False

    if arguments.require_candidate and arguments.require_realization:
        findings.append(
            _finding(
                "HRC-MODE-MUTUALLY-EXCLUSIVE",
                "candidate and realization modes are mutually exclusive",
                case_id=arguments.case_id or "",
            )
        )
        dependency_error = True
    else:
        requested_root = arguments.repo or Path(__file__).resolve().parents[1]
        repo_root = _git_root(requested_root)
        if repo_root is None:
            findings.append(
                _finding(
                    "HRC-REPO-NOT-AVAILABLE",
                    "the selected repository is not an available Git root",
                    case_id=arguments.case_id or "",
                )
            )
            dependency_error = True
        else:
            case_ids = _indexed_case_ids(
                repo_root / "contracts/hermes-runtime/fixtures/index.yaml"
            )
            if arguments.case_id and (
                case_ids is None or arguments.case_id not in case_ids
            ):
                findings.append(
                    _finding(
                        "HRC-CASE-NOT-INDEXED",
                        "the selected case is not present in the fixture index",
                        case_id=arguments.case_id,
                        path="contracts/hermes-runtime/fixtures/index.yaml",
                    )
                )
                dependency_error = True
            elif case_ids is None:
                findings.append(
                    _finding(
                        "HRC-HARNESS-INDEX-MISSING",
                        "the fixture index is missing or invalid",
                        path="contracts/hermes-runtime/fixtures/index.yaml",
                    )
                )
                dependency_error = True

    exit_code = classify_exit_code(
        findings, strict=arguments.strict, dependency_error=dependency_error
    )
    _render(findings, mode=mode, as_json=arguments.as_json, exit_code=exit_code)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
