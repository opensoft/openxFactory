#!/usr/bin/env python3
"""Syntax gate over the openxWallet family's YAML surfaces (feature
010-wallet-validator-ci).

Convener-authorized hardening, 2026-08-23, per
`specs/010-wallet-validator-ci/research.md` R7. QA proved a fail-open in the
canonical validator's layer 2: `validate-openxwallet.py` skips a file whose
YAML does not parse as "another kind" (`repo_scan`, the
`except yaml.YAMLError: skipped += 1` arm) — so a live grant with one broken
syntax error escapes the whole check while its well-formed siblings are
adjudicated. That skip is right for a whole-checkout sweep that must not
refuse unrelated YAML; this gate is the complement that closes the hole for
the files that claim to be ours.

The gate is deliberately SYNTAX-ONLY and narrower than the validator:

1. It loads `KIND_TO_SCHEMA` from the sibling validator module by importlib
   path-load — the hyphenated filename blocks a plain `import` — so there is
   no second copy of the kind vocabulary to drift, and kinds added upstream
   are covered here with no edit.
2. A file whose RAW TEXT carries none of those kind strings is not our
   business and is skipped without parsing: a whole-tree sweep stays free of
   false failures on the ~1500 unrelated documents it walks past.
3. Everything else is parsed with `yaml.safe_load_all` (the family writes
   multi-document streams). Any parse exception on any document is a finding:
   `ERROR <relative-file>: <yaml error>`. A file that cannot be decoded as
   UTF-8 text at all cannot be proven free of a family kind inside it, so it
   fails closed under the same prefix.

This gate proves PARSEABILITY only. Schema conformance, cross-record rules,
and every custody/authority invariant remain the validator's job, which runs
after this step in the same workflow. A file can pass here and still fail
there; a file that fails here never reaches a sweep that would skip it.

Exit codes: 0 ok, 1 findings, 2 harness error (fail-closed — including an
unloadable validator module, since without `KIND_TO_SCHEMA` the gate could
not tell our files from anyone else's).
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

VALIDATOR_PATH = Path(__file__).resolve().parent / "validate-openxwallet.py"


def load_kind_vocabulary() -> dict[str, str]:
    """KIND_TO_SCHEMA, read out of the canonical validator module rather than
    restated. Restating it would recreate exactly the parallel vocabulary the
    validator refuses elsewhere, and a future kind would then be validated
    there but unguarded here."""
    spec = importlib.util.spec_from_file_location(
        "validate_openxwallet", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"no importable spec for {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(module.KIND_TO_SCHEMA)


def scan(target: Path, kinds: dict[str, str]) -> int:
    """Walk `target` recursively; exit 1 if any kind-bearing file does not
    parse. Findings print as they are found, in sorted-path order."""
    if target.is_dir():
        files = sorted(p for p in target.rglob("*.y*ml")
                       if ".git" not in p.parts and p.is_file())
        root = target
    else:
        files, root = [target], target.parent

    findings = 0
    for path in files:
        label = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            findings += 1
            print(f"ERROR {label}: {exc}")
            continue
        if not any(kind in text for kind in kinds):
            continue
        try:
            for _doc in yaml.safe_load_all(text):
                pass
        except yaml.YAMLError as exc:
            findings += 1
            print(f"ERROR {label}: {exc}")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".",
                    help="directory (or single file) to syntax-gate; "
                         "defaults to the current directory")
    args = ap.parse_args()

    try:
        kinds = load_kind_vocabulary()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR cannot load {VALIDATOR_PATH.name}: {exc}", file=sys.stderr)
        return 2

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR path {target} not found", file=sys.stderr)
        return 2
    return scan(target.resolve(), kinds)


if __name__ == "__main__":
    sys.exit(main())
