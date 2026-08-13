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

import re
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

# Semantic checks for add-dispatch-credential-contract: the dispatch-only
# least-privilege + serving-tier-separation and reference-delivery invariants
# the shape schema cannot express. Neutral — they read the record, not the
# domain's meaning of a scope, beyond the trigger-scope allowlist.
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples/credential-contracts"
DISPATCH_SCOPES = {"actions:write", "actions:read", "metadata:read"}
RAW_SECRET_MARKERS = ("-----BEGIN", "ghp_", "github_pat_", "gho_", "ghs_", "AKIA")
_B64ISH = re.compile(r"[A-Za-z0-9+/=]{40,}")
# each packaged negative must raise a finding whose code starts with this
NEGATIVE_EXPECTATIONS = {
    "dispatch-reuses-content-secret.yaml": "shared-secret-identity",
    "dispatch-grants-contents.yaml": "dispatch-scope-ceiling",
    "baked-secret-in-binding.yaml": "baked-secret",
}


def _looks_like_raw_secret(value: str) -> bool:
    v = value.strip()
    return any(m in v for m in RAW_SECRET_MARKERS) or bool(_B64ISH.fullmatch(v))


def _semantic_findings(doc: dict) -> list[str]:
    """Dispatch-credential invariants the shape schema cannot express. Returns
    `code: message` strings (empty when the record conforms)."""
    kind = doc.get("kind")
    out: list[str] = []
    if kind == "xfactory_credential_requirements":
        for req in doc.get("requirements") or []:
            if req.get("access_mode") != "dispatch_only":
                continue
            rid = req.get("id", "<?>")
            bad = [s for s in (req.get("minimum_scopes") or []) if s not in DISPATCH_SCOPES]
            if bad:
                out.append(f"dispatch-scope-ceiling: requirement {rid!r} is dispatch_only but "
                           f"requests non-trigger scope(s) {bad}; a dispatch credential carries no "
                           f"contents authority (allowed: {sorted(DISPATCH_SCOPES)})")
            if len(req.get("allowed_workflows") or []) > 1:
                out.append(f"dispatch-one-workflow: requirement {rid!r} is dispatch_only but names "
                           f">1 allowed_workflow; a dispatch credential triggers exactly one")
    elif kind == "xfactory_credential_binding_template":
        seen: dict[str, str] = {}
        for name, binding in (doc.get("credential_bindings") or {}).items():
            ref = binding.get("secret_ref") if isinstance(binding, dict) else None
            if not isinstance(ref, str):
                continue
            if _looks_like_raw_secret(ref):
                out.append(f"baked-secret: binding {name!r} secret_ref is a raw secret value, not a "
                           f"vault reference; credentials are delivered by reference, never baked")
            if ref in seen:
                out.append(f"shared-secret-identity: bindings {seen[ref]!r} and {name!r} share "
                           f"secret_ref {ref!r}; dispatch and content credentials must be distinct "
                           f"bindings so the serving tier holds no content-write key material")
            else:
                seen[ref] = name
    return out


def _self_test(validator: Draft202012Validator) -> int:
    """Packaged examples: positives are schema-valid with no semantic finding;
    each negative raises its intended semantic code. Returns the error count."""
    if not EXAMPLES_DIR.is_dir():
        print(f"ERROR self-test: {EXAMPLES_DIR} not found")
        return 1
    errs = 0
    positives = sorted(EXAMPLES_DIR.glob("*.example.yaml"))
    for path in positives:
        doc = yaml.safe_load(path.read_text())
        problems = [e.message for e in validator.iter_errors(doc)] + _semantic_findings(doc)
        if problems:
            print(f"ERROR self-test: positive {path.name} unexpectedly invalid: {problems}")
            errs += 1
    neg_dir = EXAMPLES_DIR / "negative"
    negatives = sorted(neg_dir.glob("*.yaml")) if neg_dir.is_dir() else []
    for path in negatives:
        want = NEGATIVE_EXPECTATIONS.get(path.name)
        findings = _semantic_findings(yaml.safe_load(path.read_text()))
        if not want:
            print(f"ERROR self-test: negative {path.name} has no registered expectation")
            errs += 1
        elif not any(f.startswith(want) for f in findings):
            print(f"ERROR self-test: negative {path.name} did not raise {want!r} (got {findings})")
            errs += 1
    if errs == 0:
        print(f"self-test: {len(positives)} positive + {len(negatives)} negative example(s) confirmed")
    return errs


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    repo = Path(sys.argv[1]).resolve()
    validator = Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))
    errors = _self_test(validator)
    skipped = checked = 0

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
        for msg in _semantic_findings(doc):
            print(f"ERROR {rel}: {msg}")
            errors += 1

    verdict = "PASS" if errors == 0 else "FAIL"
    print(f"\n{repo.name}: {checked} contract(s) checked, {skipped} skipped, "
          f"{errors} error(s) -> {verdict}")
    raise SystemExit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
