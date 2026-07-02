#!/usr/bin/env python3
"""Validate openxFactory pins in DomainxFactory stack.yaml files."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to validate stack.yaml files") from exc


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v[0-9]+\\.[0-9]+\\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


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
