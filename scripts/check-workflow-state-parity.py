#!/usr/bin/env python3
"""Workflow md/yaml state-parity check (domain-conformance-checks capability).

Runs from the pinned openxFactory checkout against a DomainxFactory repo's
``workflows/`` directory, never copied into it (adopted from codexFactory's
conformance-gate, adopt-neutral-utility-pack).

The ``.md`` states/transitions tables are the authoritative state machine;
the paired ``.yaml`` gate contract is a machine projection (see the domain
repo's workflows/README.md, Contract Authority). For every workflow pair, the set
of states in the ``.yaml`` gates' ``produces[]`` lists must equal the set of
transition-target states in the ``.md`` — with one convention: ``blocked``
is expressed in the ``.yaml`` via ``blocks_when[]`` conditions and is
therefore excluded from the comparison.

Exit code 0 on parity, 1 with one line per divergent workflow otherwise.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

BLOCKED = "blocked"


def md_transition_targets(md_text: str) -> set[str]:
    section = re.search(r"## Transitions(.*?)(\n## |\Z)", md_text, re.S)
    if not section:
        return set()
    targets: set[str] = set()
    for row in re.finditer(r"^\|([^|]+)\|([^|]+)\|", section.group(1), re.M):
        target = row.group(2).strip().strip("`")
        if not target or target.lower() == "to" or set(target) <= set("-: "):
            continue
        targets.add(target)
    return targets


def yaml_produced_states(yaml_text: str) -> set[str]:
    data = yaml.safe_load(yaml_text)
    produced: set[str] = set()
    for gate in (data.get("workflow", {}) or {}).get("gates", []) or []:
        produced.update(gate.get("produces", []) or [])
    return produced


def check_pair(md_path: Path, yaml_path: Path) -> str | None:
    targets = md_transition_targets(md_path.read_text(encoding="utf-8")) - {BLOCKED}
    produced = yaml_produced_states(yaml_path.read_text(encoding="utf-8")) - {BLOCKED}
    if targets == produced:
        return None
    yaml_only = sorted(produced - targets)
    md_only = sorted(targets - produced)
    parts = [f"workflow {md_path.stem}: state parity violation"]
    if yaml_only:
        parts.append(f"yaml-only produces: {yaml_only}")
    if md_only:
        parts.append(f"md transition targets missing from yaml produces: {md_only}")
    return "; ".join(parts)


def check(workflows_dir: Path) -> list[str]:
    errors: list[str] = []
    for md_path in sorted(workflows_dir.glob("*.md")):
        if md_path.name == "README.md":
            continue
        yaml_path = md_path.with_suffix(".yaml")
        if not yaml_path.is_file():
            errors.append(f"workflow {md_path.stem}: missing .yaml gate contract pair")
            continue
        error = check_pair(md_path, yaml_path)
        if error:
            errors.append(error)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # Required on purpose: this script's own repo (openxFactory, the
    # publisher) has no domain workflows/ tree, so a self-repo default
    # would be a wrong-target default. The known consumers pass the path.
    parser.add_argument(
        "workflows_dir",
        type=Path,
        help="domain repo workflows directory to check",
    )
    args = parser.parse_args()

    errors = check(args.workflows_dir)
    for line in errors:
        print(f"ERROR: {line}", file=sys.stderr)
    if errors:
        return 1
    print("workflow state parity ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
