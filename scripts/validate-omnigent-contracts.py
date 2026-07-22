#!/usr/bin/env python3
"""Validate the omnigent contract family (add-omnigent-domain-overlay).

Checks, fail-closed:
  1. Both schemas under contracts/omnigent/ parse and are valid
     Draft 2020-12 JSON Schemas.
  2. Positive examples validate against their schema.
  3. Every negative fixture FAILS validation, and at least one reported
     violation matches the fixture's leading ``# expect: <substring>``
     marker (matched against the error message plus its JSON path).
  4. Semantic invariants the schema cannot express:
     - credential tier disjointness: no family listed in
       ``never_assignable`` may appear in ``all_classes``, ``by_class``,
       or ``unassigned_by_default``;
     - worker ids are unique;
     - canonical vocabulary lint: no mapping key in an instance document
       contains a ``customer`` or ``client`` word segment (legacy layer
       vocabulary; the pinned upstream Hermes runtime manifest is outside
       these documents).

Exit code 0 only if every check passes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = ROOT / "contracts" / "omnigent"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "fixtures" / "negative"

SCHEMA_FILES = {
    "omnigent_domain_overlay": CONTRACT_DIR / "omnigent-domain-overlay.schema.yaml",
    "omnigent_install_manifest": CONTRACT_DIR / "omnigent-install-manifest.schema.yaml",
}
POSITIVE_EXAMPLES = {
    "omnigent_domain_overlay": EXAMPLES_DIR / "omnigent-domain-overlay.example.yaml",
    "omnigent_install_manifest": EXAMPLES_DIR / "omnigent-install-manifest.example.yaml",
}

LEGACY_KEY_SEGMENT = re.compile(r"(^|_)(customer|client)(_|$)")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)
    print(f"FAIL {message}")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def schema_kind_for(path: Path) -> str:
    return "omnigent_domain_overlay" if path.name.startswith("overlay-") else "omnigent_install_manifest"


def iter_keys(node, prefix="$"):
    if isinstance(node, dict):
        for key, value in node.items():
            yield f"{prefix}.{key}", key
            yield from iter_keys(value, f"{prefix}.{key}")
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from iter_keys(item, f"{prefix}[{index}]")


def semantic_errors(kind: str, doc) -> list[str]:
    errors: list[str] = []
    for path, key in iter_keys(doc):
        if LEGACY_KEY_SEGMENT.search(key):
            errors.append(f"{path}: legacy vocabulary key '{key}' (use subject/tenant/domain spellings)")
    if kind == "omnigent_domain_overlay" and isinstance(doc, dict):
        workers = doc.get("workers") or []
        ids = [w.get("id") for w in workers if isinstance(w, dict)]
        for worker_id in {i for i in ids if ids.count(i) > 1}:
            errors.append(f"$.workers: duplicate worker id '{worker_id}'")
        creds = doc.get("credential_requirements") or {}
        never = set(creds.get("never_assignable") or [])
        assignable: set[str] = set(creds.get("all_classes") or [])
        assignable.update(creds.get("unassigned_by_default") or [])
        for families in (creds.get("by_class") or {}).values():
            assignable.update(families or [])
        for family in sorted(never & assignable):
            errors.append(
                f"$.credential_requirements: never_assignable family '{family}' "
                "is also declared grantable (no approval path may override never_assignable)"
            )
    return errors


def all_violations(validator: Draft202012Validator, kind: str, doc) -> list[str]:
    violations = [
        f"{error.json_path}: {error.message}"
        for error in validator.iter_errors(doc)
    ]
    violations.extend(semantic_errors(kind, doc))
    return violations


def main() -> int:
    validators: dict[str, Draft202012Validator] = {}
    for kind, path in SCHEMA_FILES.items():
        schema = load_yaml(path)
        Draft202012Validator.check_schema(schema)
        validators[kind] = Draft202012Validator(schema)
        print(f"ok   schema parses and is valid: {path.relative_to(ROOT)}")

    for kind, path in POSITIVE_EXAMPLES.items():
        violations = all_violations(validators[kind], kind, load_yaml(path))
        if violations:
            fail(f"positive example rejected: {path.relative_to(ROOT)}")
            for violation in violations:
                print(f"       {violation}")
        else:
            print(f"ok   positive example validates: {path.relative_to(ROOT)}")

    negative_fixtures = sorted(NEGATIVE_DIR.glob("*.yaml"))
    if not negative_fixtures:
        fail(f"no negative fixtures found under {NEGATIVE_DIR.relative_to(ROOT)}")
    for path in negative_fixtures:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        marker = re.match(r"#\s*expect:\s*(\S+)", first_line)
        if not marker:
            fail(f"negative fixture missing '# expect:' marker: {path.relative_to(ROOT)}")
            continue
        expected = marker.group(1)
        kind = schema_kind_for(path)
        violations = all_violations(validators[kind], kind, load_yaml(path))
        if not violations:
            fail(f"negative fixture unexpectedly validates: {path.relative_to(ROOT)}")
        elif not any(expected in violation for violation in violations):
            fail(
                f"negative fixture failed for the wrong reason: {path.relative_to(ROOT)} "
                f"(expected a violation mentioning '{expected}')"
            )
            for violation in violations:
                print(f"       {violation}")
        else:
            print(f"ok   negative fixture rejected as expected ({expected}): {path.relative_to(ROOT)}")

    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nAll omnigent contract checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
