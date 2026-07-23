#!/usr/bin/env python3
"""Validate the hermes-domain-overlay contract family (add-hermes-domain-overlay-contract).

The openxFactory-owned canonical validator for the two kinds
`hermes_domain_overlay` and `hermes_overlay_descriptor`
(`contracts/hermes-domain-overlay/*.schema.yaml`). Run from the pinned
openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-hermes-domain-overlay.py [DOMAIN_REPO_PATH]

Two layers run:

1. Packaged reference examples (`contracts/hermes-domain-overlay/examples/`):
   every `*.example.yaml` must pass; every file under `negative/` must fail
   for its INTENDED reason (declared in its `# expected_failure:` header) —
   the self-test fails closed if any negative stops failing for its reason
   or any positive example fails.
2. Optional real artifacts under DOMAIN_REPO_PATH: the overlay at the
   descriptor-declared path (or the documented convention
   `hermes/domain/overlay.yaml` when no descriptor exists) is validated;
   a descriptor, when present, is validated including path existence.

Deterministic checks the schema shape cannot express:
  - `authority_boundaries` carries exactly one domain-owned list named
    `<domain.id>_owns`, non-empty;
  - the no-overlap rule: no authority item appears in more than one
    boundary list;
  - descriptor role keys are limited to domain/client/customer, and every
    declared path exists when a repo path is supplied.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = REPO_ROOT / "contracts" / "hermes-domain-overlay"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
DESCRIPTOR_ROLES = {"domain", "client", "customer"}
CONVENTION_PATHS = {"domain": "hermes/domain/overlay.yaml"}
DESCRIPTOR_FILE = "hermes/overlay-descriptor.yaml"


def _fail(findings: list[str], message: str) -> None:
    findings.append(message)


def validate_overlay(doc: object, findings: list[str]) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "overlay document is not a mapping")
    if doc.get("kind") != "hermes_domain_overlay":
        return _fail(findings, "kind is not hermes_domain_overlay")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    domain = doc.get("domain")
    if not isinstance(domain, dict):
        return _fail(findings, "missing required block: domain")
    for field in ("id", "display_name"):
        if not isinstance(domain.get(field), str) or not domain.get(field):
            _fail(findings, f"missing or empty domain.{field}")
    for field in ("approval_scope_kinds", "required_approval_fields"):
        value = domain.get(field)
        if not isinstance(value, list) or not value:
            _fail(findings, f"missing or empty {field}")
        elif not all(isinstance(item, str) and item for item in value):
            _fail(findings, f"{field} entries must be non-empty strings")
    boundaries = domain.get("authority_boundaries")
    if not isinstance(boundaries, dict):
        return _fail(findings, "missing required block: authority_boundaries")
    for required_list in ("xfactory_owns", "repository_owns"):
        value = boundaries.get(required_list)
        if not isinstance(value, list) or not value:
            _fail(findings, f"missing or empty authority_boundaries.{required_list}")
    domain_id = domain.get("id")
    expected_key = f"{domain_id}_owns" if isinstance(domain_id, str) else None
    extra_keys = [k for k in boundaries if k not in ("xfactory_owns", "repository_owns")]
    if expected_key is None or expected_key not in boundaries:
        _fail(findings, f"missing domain-owned list: expected authority_boundaries.{expected_key}")
    elif not isinstance(boundaries[expected_key], list) or not boundaries[expected_key]:
        _fail(findings, f"domain-owned list {expected_key} must be a non-empty list")
    for key in extra_keys:
        if key != expected_key:
            _fail(findings, f"unexpected boundary list {key}: the domain-owned list must be named {expected_key}")
    # no-overlap rule across all boundary lists
    seen: dict[str, str] = {}
    for list_name, value in boundaries.items():
        if not isinstance(value, list):
            continue
        for item in value:
            if item in seen and seen[item] != list_name:
                _fail(findings, f"authority item in more than one boundary list: {item} ({seen[item]} and {list_name})")
            seen.setdefault(item, list_name)


def validate_descriptor(doc: object, findings: list[str], repo_path: Path | None) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "descriptor document is not a mapping")
    if doc.get("kind") != "hermes_overlay_descriptor":
        return _fail(findings, "kind is not hermes_overlay_descriptor")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    paths = doc.get("overlay_paths")
    if not isinstance(paths, dict) or not paths:
        return _fail(findings, "missing or empty overlay_paths")
    for role, path in paths.items():
        if role not in DESCRIPTOR_ROLES:
            _fail(findings, f"unknown role in overlay_paths: {role} (allowed: {sorted(DESCRIPTOR_ROLES)})")
        if not isinstance(path, str) or not path:
            _fail(findings, f"overlay_paths.{role} must be a non-empty path string")
        elif repo_path is not None and not (repo_path / path).is_file():
            _fail(findings, f"dangling declared path for role {role}: {path}")


def validate_document(path: Path, repo_path: Path | None) -> list[str]:
    findings: list[str] = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"unparseable YAML: {exc}"]
    kind = doc.get("kind") if isinstance(doc, dict) else None
    if kind == "hermes_domain_overlay":
        validate_overlay(doc, findings)
    elif kind == "hermes_overlay_descriptor":
        validate_descriptor(doc, findings, repo_path)
    else:
        findings.append(f"unknown kind: {kind}")
    return findings


def expected_failure(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            return line.split(":", 1)[1].strip()
    raise SystemExit(f"negative fixture missing '# expected_failure:' header: {path}")


def self_test() -> int:
    checked = 0
    for example in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        findings = validate_document(example, repo_path=None)
        if findings:
            print(f"FAIL positive example {example.name}: {findings}", file=sys.stderr)
            return 1
        print(f"example ok: {example.name}")
        checked += 1
    for negative in sorted(NEGATIVE_DIR.glob("*.yaml")):
        reason = expected_failure(negative)
        findings = validate_document(negative, repo_path=None)
        if not findings:
            print(f"FAIL negative fixture passed: {negative.name}", file=sys.stderr)
            return 1
        if not any(reason in finding for finding in findings):
            print(
                f"FAIL negative fixture {negative.name} failed for the wrong reason: "
                f"expected '{reason}', got {findings}",
                file=sys.stderr,
            )
            return 1
        print(f"negative ok ({reason}): {negative.name}")
        checked += 1
    print(f"self-test ok: {checked} fixture(s)")
    return 0


def validate_repo(repo_path: Path) -> int:
    descriptor_path = repo_path / DESCRIPTOR_FILE
    role_paths = dict(CONVENTION_PATHS)
    if descriptor_path.is_file():
        findings = validate_document(descriptor_path, repo_path)
        if findings:
            for finding in findings:
                print(f"FAIL {descriptor_path}: {finding}", file=sys.stderr)
            return 1
        print(f"descriptor ok: {DESCRIPTOR_FILE}")
        declared = yaml.safe_load(descriptor_path.read_text(encoding="utf-8"))["overlay_paths"]
        role_paths.update(declared)
    else:
        print(f"no descriptor at {DESCRIPTOR_FILE}; using documented convention")
    validated = 0
    for role, rel_path in sorted(role_paths.items()):
        overlay_path = repo_path / rel_path
        if not overlay_path.is_file():
            if role in CONVENTION_PATHS and not descriptor_path.is_file():
                print(f"note: no overlay at convention path for role {role}: {rel_path}")
                continue
            print(f"FAIL role {role}: declared overlay missing at {rel_path}", file=sys.stderr)
            return 1
        doc = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        kind = doc.get("kind") if isinstance(doc, dict) else None
        if kind != "hermes_domain_overlay":
            print(f"skip role {role}: {rel_path} carries kind {kind} (not a domain overlay)")
            continue
        findings = validate_document(overlay_path, repo_path)
        if findings:
            for finding in findings:
                print(f"FAIL {rel_path}: {finding}", file=sys.stderr)
            return 1
        print(f"overlay ok ({role}): {rel_path}")
        validated += 1
    print(f"repo validation ok: {validated} overlay(s) validated")
    return 0


def main() -> int:
    status = self_test()
    if status:
        return status
    if len(sys.argv) > 1:
        repo_path = Path(sys.argv[1]).resolve()
        if not repo_path.is_dir():
            print(f"not a directory: {repo_path}", file=sys.stderr)
            return 2
        return validate_repo(repo_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
