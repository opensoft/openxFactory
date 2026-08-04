#!/usr/bin/env python3
"""openxFactory pin reconciliation check (domain-conformance-checks capability).

Runs from the pinned openxFactory checkout against a DomainxFactory repo,
never copied into it (adopted from codexFactory's conformance-gate,
adopt-neutral-utility-pack; the overlap with
``validate-domain-openxfactory-pins.py`` is a deliberately deferred merge —
design D3 of that change).

Aggregation-scope only: compares stack.yaml ``xfactory.contract_ref``
against the aggregation repository's recorded openxFactory submodule
pointer.

- ERROR when the pin is not an ancestor of the submodule pointer
  (divergent — the declared contract is off the submodule's history);
- WARN when the pin is a proper ancestor (stale-behind — legal, the
  aggregation pointer may deliberately track ahead, but it must be
  visible); the warning includes the refresh instruction;
- PASS on equality;
- SKIP with notice outside an aggregation checkout.

Tenant records are exempt by design: per-tenant openxFactory pinning is
legitimate by contract and is not inspected here.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

PASS, WARN, ERROR, SKIP = "PASS", "WARN", "ERROR", "SKIP"


def classify(pin: str, pointer: str, is_ancestor) -> tuple[str, str]:
    """Pure decision: (verdict, message). ``is_ancestor(a, b)`` -> bool."""
    if pin == pointer:
        return PASS, f"stack pin matches aggregation submodule pointer ({pin[:12]})"
    if is_ancestor(pin, pointer):
        return WARN, (
            f"stack pin {pin[:12]} is stale-behind the aggregation submodule "
            f"pointer {pointer[:12]}; refresh with: update stack.yaml "
            f"xfactory.contract_ref to {pointer} and contract_declared_at to today"
        )
    return ERROR, (
        f"stack pin {pin[:12]} is not an ancestor of the aggregation submodule "
        f"pointer {pointer[:12]}: the declared contract is off the submodule's history"
    )


def find_aggregation_root(repo_root: Path) -> Path | None:
    candidate = repo_root.parent.parent
    gitmodules = candidate / ".gitmodules"
    if gitmodules.is_file() and "openxFactory" in gitmodules.read_text(encoding="utf-8"):
        return candidate
    return None


def _git_dir_arg(root: Path) -> str:
    """Absolute form of a directory handed to ``git -C``.

    Both roots can come from the command line, and a relative path that began
    with a dash would be read by git as an option rather than a directory.
    Resolving first removes that shape entirely.
    """
    return str(Path(root).resolve())


def recorded_pointer(aggregation_root: Path) -> str:
    out = subprocess.run(
        ["git", "-C", _git_dir_arg(aggregation_root), "ls-tree", "HEAD", "openxFactory"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return out[2]


def git_is_ancestor(openx_root: Path):
    root_arg = _git_dir_arg(openx_root)

    def _is_ancestor(ancestor: str, descendant: str) -> bool:
        return subprocess.run(
            ["git", "-C", root_arg, "merge-base", "--is-ancestor", ancestor, descendant],
            capture_output=True,
        ).returncode == 0
    return _is_ancestor


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # Required on purpose: this script's own repo (openxFactory, the
    # publisher) is not a domain repo, so a self-repo default would be a
    # wrong-target default. The known consumers already pass the path.
    parser.add_argument(
        "repo_root",
        type=Path,
        help="domain repo root to check",
    )
    parser.add_argument(
        "--aggregation-root",
        type=Path,
        default=None,
        help="aggregation repo root override (default: repo_root/../..)",
    )
    args = parser.parse_args()

    aggregation_root = args.aggregation_root or find_aggregation_root(args.repo_root)
    if aggregation_root is None:
        print("SKIP: pin reconciliation skipped (not an aggregation checkout)")
        return 0

    with (args.repo_root / "stack.yaml").open(encoding="utf-8") as handle:
        pin = yaml.safe_load(handle)["xfactory"]["contract_ref"]
    pointer = recorded_pointer(aggregation_root)

    verdict, message = classify(pin, pointer, git_is_ancestor(aggregation_root / "openxFactory"))
    print(f"{verdict}: {message}", file=sys.stderr if verdict == ERROR else sys.stdout)
    return 1 if verdict == ERROR else 0


if __name__ == "__main__":
    raise SystemExit(main())
