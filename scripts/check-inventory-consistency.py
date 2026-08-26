#!/usr/bin/env python3
"""Inventory consistency check (domain-conformance-checks capability).

Runs from the pinned openxFactory checkout against a DomainxFactory repo,
never copied into it (adopted from codexFactory's conformance-gate,
adopt-neutral-utility-pack). stack.yaml is the declared source of truth
for required artifacts. This check errors when:

- an entry in ``schemas.required`` or ``workflows.required`` has no file on
  disk;
- a shipped ``schemas/*.schema.{json,yaml}`` or ``workflows/*.md`` (with its
  required ``.yaml`` pair) is absent from the corresponding required list;
- the ``schemas/README.md`` table omits a shipped schema or lists one that
  does not exist.

Exit code 0 on agreement, 1 with one line per error otherwise.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


def load_stack(repo_root: Path) -> dict:
    with (repo_root / "stack.yaml").open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def shipped_schemas(repo_root: Path) -> set[str]:
    root = repo_root / "schemas"
    return {
        p.name
        for p in root.iterdir()
        if p.is_file() and (p.name.endswith(".schema.json") or p.name.endswith(".schema.yaml"))
    }


def shipped_workflows(repo_root: Path) -> set[str]:
    root = repo_root / "workflows"
    return {p.name for p in root.glob("*.md") if p.name != "README.md"}


def readme_schema_rows(repo_root: Path) -> set[str]:
    text = (repo_root / "schemas" / "README.md").read_text(encoding="utf-8")
    return set(re.findall(r"\[([^\]]+\.schema\.(?:json|yaml))\]", text))


def check(repo_root: Path) -> list[str]:
    errors: list[str] = []
    stack = load_stack(repo_root)

    required_schemas = set(stack.get("schemas", {}).get("required", []))
    required_workflows = set(stack.get("workflows", {}).get("required", []))

    for name in sorted(required_schemas):
        if not (repo_root / "schemas" / name).is_file():
            errors.append(f"stack.yaml schemas.required entry missing on disk: schemas/{name}")
    for name in sorted(required_workflows):
        if not (repo_root / "workflows" / name).is_file():
            errors.append(f"stack.yaml workflows.required entry missing on disk: workflows/{name}")

    for name in sorted(shipped_schemas(repo_root) - required_schemas):
        errors.append(f"shipped schema not listed in stack.yaml schemas.required: schemas/{name}")
    for name in sorted(shipped_workflows(repo_root) - required_workflows):
        errors.append(f"shipped workflow not listed in stack.yaml workflows.required: workflows/{name}")

    for name in sorted(shipped_workflows(repo_root)):
        pair = repo_root / "workflows" / name.replace(".md", ".yaml")
        if not pair.is_file():
            errors.append(f"workflow missing its .yaml gate contract pair: workflows/{pair.name}")

    rows = readme_schema_rows(repo_root)
    shipped = shipped_schemas(repo_root)
    for name in sorted(shipped - rows):
        errors.append(f"schemas/README.md table omits shipped schema: {name}")
    for name in sorted(rows - shipped):
        errors.append(f"schemas/README.md table lists nonexistent schema: {name}")

    return errors


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
    args = parser.parse_args()

    errors = check(args.repo_root)
    for line in errors:
        print(f"ERROR: {line}", file=sys.stderr)
    if errors:
        return 1
    print("inventory consistency ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
