#!/usr/bin/env python3
"""Validate a domain repo's workflow contracts against the neutral schema.

Canonical validator for the workflow-gate-contract capability
(promote-workflow-gate-contract change; DTN-001/DTN-002). Run from the
pinned openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-workflow-contracts.py <domain-repo-path>

Rules (per the capability):
- files under workflows/*.yaml|yml whose kind matches
  ``<domain>_workflow_contract`` validate against
  contracts/schemas/xfactory-workflow.schema.yaml (errors on failure);
- files with NO kind envelope are errors (missing envelope);
- files with a non-matching kind (e.g. opsx_workflow) are skipped with
  notice — out of this contract's scope;
- gate/workflow owner_layer values not among canonical roles or the
  domain stack's declared layer ids are warnings.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / "contracts/schemas/xfactory-workflow.schema.yaml"
KIND_RE = re.compile(r"^[a-z][a-z0-9]*_workflow_contract$")
CANONICAL = {"customer", "client", "domain", "xfactory"}


def declared_layers(repo: Path) -> set[str]:
    layers = set(CANONICAL)
    stack = repo / "stack.yaml"
    if stack.exists():
        data = yaml.safe_load(stack.read_text()) or {}
        for layer in (data.get("hermes") or {}).get("layers") or []:
            if isinstance(layer, dict):
                for key in ("id", "role"):
                    if layer.get(key):
                        layers.add(str(layer[key]))
        dom = (data.get("domain") or {}).get("id")
        if dom:
            layers.add(f"{dom}_omnigent")
            layers.add(f"{dom}_domain_hermes")
    return layers


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    repo = Path(sys.argv[1]).resolve()
    validator = Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))
    layers = declared_layers(repo)
    errors = warnings = skipped = checked = 0

    files = sorted((repo / "workflows").glob("*.y*ml")) if (repo / "workflows").is_dir() else []
    for f in files:
        rel = f.relative_to(repo)
        try:
            doc = yaml.safe_load(f.read_text())
        except yaml.YAMLError as exc:
            print(f"ERROR {rel}: YAML parse failure: {exc}")
            errors += 1
            continue
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if kind is None:
            print(f"ERROR {rel}: missing schema_version/kind envelope")
            errors += 1
            continue
        if not KIND_RE.match(str(kind)):
            print(f"skip  {rel}: kind {kind!r} is not a workflow contract (out of scope)")
            skipped += 1
            continue
        checked += 1
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            print(f"ERROR {rel}: {loc}: {err.message}")
            errors += 1
        wf = doc.get("workflow") or {}
        owners = [("workflow", wf.get("owner_layer"))]
        owners += [(f"gate {g.get('id')}", g.get("owner_layer"))
                   for g in wf.get("gates") or [] if isinstance(g, dict)]
        for where, owner in owners:
            if owner and str(owner) not in layers:
                print(f"WARN  {rel}: {where}: owner_layer {owner!r} not canonical or declared in stack.yaml")
                warnings += 1

    verdict = "PASS" if errors == 0 else "FAIL"
    print(f"\n{repo.name}: {checked} contract(s) checked, {skipped} skipped, "
          f"{errors} error(s), {warnings} warning(s) -> {verdict}")
    raise SystemExit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
