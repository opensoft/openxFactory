#!/usr/bin/env python3
"""Set the openxFactory contract pin in DomainxFactory stack.yaml files.

This updater is intentionally text-preserving. It replaces only the top-level
`xfactory:` block so existing YAML layout elsewhere in the file does not churn.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v[0-9]+\\.[0-9]+\\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
TOP_LEVEL_RE = re.compile(r"^[A-Za-z0-9_]+:\s*$")


def infer_ref_type(ref: str) -> str:
    if SHA_RE.match(ref):
        return "commit"
    if TAG_RE.match(ref):
        return "tag"
    raise ValueError("openxFactory ref must be a 40-character SHA or vX.Y.Z tag")


def find_block(lines: list[str], key: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        if line == f"{key}:\n" or line == f"{key}:":
            start = index
            break
    if start is None:
        raise ValueError(f"missing top-level {key}: block")

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line.startswith((" ", "\t")) and TOP_LEVEL_RE.match(line):
            end = index
            break
    return start, end


def update_stack(path: Path, ref: str, ref_type: str, declared_at: str, source: str) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    start, end = find_block(lines, "xfactory")

    replacement = [
        "xfactory:\n",
        "  contract_repo: github.com/opensoft/openxFactory\n",
        "  contract_name: openxFactory\n",
        f"  contract_ref_type: {ref_type}\n",
        f"  contract_ref: {ref}\n",
        "  contract_schema_version: 1\n",
        f"  contract_declared_at: \"{declared_at}\"\n",
        f"  contract_source: {source}\n",
    ]
    updated = "".join(lines[:start] + replacement + lines[end:])
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openxfactory-ref", required=True)
    parser.add_argument("--declared-at", default=date.today().isoformat())
    parser.add_argument("--source", default="xFactory-submodule-pin")
    parser.add_argument("domains", nargs="+", help="Domain repo directories or stack.yaml paths")
    args = parser.parse_args()

    ref_type = infer_ref_type(args.openxfactory_ref)
    for domain in args.domains:
        path = Path(domain)
        stack_path = path if path.name == "stack.yaml" else path / "stack.yaml"
        if not stack_path.exists():
            raise FileNotFoundError(stack_path)
        if update_stack(stack_path, args.openxfactory_ref, ref_type, args.declared_at, args.source):
            print(f"updated {stack_path}")
        else:
            print(f"ok {stack_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
