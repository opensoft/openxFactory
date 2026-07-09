#!/usr/bin/env python3
"""Validate a domain repo's credential contracts against the neutral schema.

Canonical validator for the credential-contracts capability
(promote-credential-contracts change; DTN-004). Run from the pinned
openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-credential-contracts.py <domain-repo-path>

Files under credentials/*.yaml|yml whose kind is one of the five contract
kinds validate against contracts/schemas/xfactory-credential-contracts.schema.yaml;
files with other kinds (e.g. domain policy records) are skipped with notice;
files with no kind envelope are errors.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / "contracts/schemas/xfactory-credential-contracts.schema.yaml"
KINDS = {
    "xfactory_credential_requirements",
    "xfactory_runtime_capability_grant_template",
    "xfactory_credential_binding_template",
    "xfactory_credential_broker_contract",
    "xfactory_credential_audit_policy",
}


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    repo = Path(sys.argv[1]).resolve()
    validator = Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))
    errors = skipped = checked = 0

    cred = repo / "credentials"
    files = sorted(cred.rglob("*.y*ml")) if cred.is_dir() else []
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
        if kind not in KINDS:
            print(f"skip  {rel}: kind {kind!r} is not a credential contract (out of scope)")
            skipped += 1
            continue
        checked += 1
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            # oneOf noise: report the sub-errors that are not kind mismatches
            if err.validator == "oneOf":
                msgs = sorted({e.message for e in err.context
                               if "const" not in e.message})
                for m in msgs[:3] or [err.message]:
                    print(f"ERROR {rel}: {loc}: {m}")
                    errors += 1
                continue
            print(f"ERROR {rel}: {loc}: {err.message}")
            errors += 1

    verdict = "PASS" if errors == 0 else "FAIL"
    print(f"\n{repo.name}: {checked} contract(s) checked, {skipped} skipped, "
          f"{errors} error(s) -> {verdict}")
    raise SystemExit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
