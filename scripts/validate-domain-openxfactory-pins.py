#!/usr/bin/env python3
"""Validate openxFactory pins in DomainxFactory stack.yaml files.

Beyond pin shape, this also resolves the pinned ref against the local
openxFactory checkout and verifies every `openxFactory/...` path the stack
references (contracts, profile refs) actually exists at that ref — a pin that
predates a contract surface it consumes is an error, not just stale.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to validate stack.yaml files") from exc


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")

OPENX_ROOT = Path(__file__).resolve().parent.parent
REF_PREFIX = "openxFactory/"


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(OPENX_ROOT), *args],
        capture_output=True, text=True, check=False,
    )


def collect_openx_refs(node) -> set[str]:
    """Every string anywhere in the stack that references an openxFactory path."""
    refs: set[str] = set()
    if isinstance(node, str):
        if node.startswith(REF_PREFIX):
            refs.add(node[len(REF_PREFIX):])
    elif isinstance(node, dict):
        for value in node.values():
            refs.update(collect_openx_refs(value))
    elif isinstance(node, list):
        for item in node:
            refs.update(collect_openx_refs(item))
    return refs


def validate_pin_content(path: Path, data: dict, xfactory: dict) -> list[str]:
    """Check the pinned ref exists locally and contains every referenced path."""
    if _git("rev-parse", "--is-inside-work-tree").returncode != 0:
        print(f"note: {OPENX_ROOT} is not a git checkout; "
              "skipping pinned-ref content checks")
        return []
    ref = xfactory.get("contract_ref")
    if not isinstance(ref, str) or not ref:
        return []  # shape errors already reported
    if _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode != 0:
        return [f"{path}: pinned ref {ref} not found in openxFactory history"]
    errors = []
    for rel in sorted(collect_openx_refs(data)):
        if _git("cat-file", "-e", f"{ref}:{rel}").returncode != 0:
            errors.append(
                f"{path}: references openxFactory/{rel}, "
                f"which does not exist at pinned ref {ref[:12]}"
            )
    return errors


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return data


def validate_stack(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []
    xfactory = data.get("xfactory")
    if not isinstance(xfactory, dict):
        return [f"{path}: missing xfactory mapping"]

    expected = {
        "contract_repo": "github.com/opensoft/openxFactory",
        "contract_name": "openxFactory",
        "contract_schema_version": 1,
    }
    for key, value in expected.items():
        if xfactory.get(key) != value:
            errors.append(f"{path}: xfactory.{key} must be {value!r}")

    ref_type = xfactory.get("contract_ref_type")
    ref = xfactory.get("contract_ref")
    if ref_type not in {"commit", "tag"}:
        errors.append(f"{path}: xfactory.contract_ref_type must be 'commit' or 'tag'")
    if not isinstance(ref, str) or not ref:
        errors.append(f"{path}: xfactory.contract_ref is required")
    elif ref_type == "commit" and not SHA_RE.match(ref):
        errors.append(f"{path}: commit ref must be a 40-character lowercase SHA")
    elif ref_type == "tag" and not TAG_RE.match(ref):
        errors.append(f"{path}: tag ref must match vX.Y.Z")

    if not xfactory.get("contract_declared_at"):
        errors.append(f"{path}: xfactory.contract_declared_at is required")
    if not xfactory.get("contract_source"):
        errors.append(f"{path}: xfactory.contract_source is required")

    errors.extend(validate_pin_content(path, data, xfactory))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", nargs="+", help="Domain repo directories or stack.yaml paths")
    args = parser.parse_args()

    all_errors: list[str] = []
    for domain in args.domains:
        path = Path(domain)
        stack_path = path if path.name == "stack.yaml" else path / "stack.yaml"
        all_errors.extend(validate_stack(stack_path))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1
    print("DomainxFactory openxFactory pins are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
