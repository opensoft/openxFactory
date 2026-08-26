#!/usr/bin/env python3
"""Red-proof harness for the trust-anchor negative corpus.

A green self-test proves the negatives fail. It does NOT prove they fail because
the rule they name is doing the work — a fixture can drift into tripping
something incidental while its own suite stays green.

This suppresses each expected finding code in turn and asserts the packaged
corpus goes RED. A code that can be neutered while the bar stays green has a
negative confirmation that proves nothing.

`schema` is the one code that cannot be neutered this way: several guarantees in
this family are expressed IN THE SHAPE, so suppressing `schema` also suppresses
every other document's schema findings and the run collapses into noise. Those
probes carry a `expected_failure_detail` pin instead, which is what keeps them
tied to the invariant they are named for.

Run from the repository root:

    python3 specs/009-trust-anchor-contracts/evidence/red-proof.py

Exit codes: 0 every code load-bearing, 1 one or more neuterable silently.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "validate-trust-anchor.py"


def load():
    spec = importlib.util.spec_from_file_location("validate_trust_anchor", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_with_code_suppressed(code: str) -> int:
    m = load()
    original = m.Findings.error

    def patched(self, c, msg, _c=code, _o=original):
        if c == _c:
            return  # neuter exactly this rule
        _o(self, c, msg)

    m.Findings.error = patched
    docs = m.load_schemas()
    ctx = m.Context(m.load_yaml(m.CUSTODY_REGISTRY_PATH),
                    m.load_yaml(m.OPENXWALLET_REGISTRY_PATH))
    for path in m.positive_paths():
        doc = m.load_yaml(path)
        if isinstance(doc, dict):
            ctx.index(doc)
    findings = m.Findings()
    with contextlib.redirect_stdout(io.StringIO()):
        m.self_test(findings, docs, ctx)
    return len(findings.errors)


def main() -> int:
    base = load()
    codes = sorted({base.expected_failure(p)[0] for p in base.negative_paths()}
                   - {"schema"})
    silent = []
    for code in codes:
        errors = run_with_code_suppressed(code)
        print(f"  {'RED  ' if errors else 'GREEN'}  neutered {code:46s} "
              f"-> {errors} error(s)")
        if not errors:
            silent.append(code)
    print()
    if silent:
        print(f"FAIL {len(silent)} code(s) neuterable without turning the bar "
              f"red: {silent}")
        return 1
    print(f"OK all {len(codes)} codes are load-bearing — neutering any one "
          f"turns the corpus red")
    return 0


if __name__ == "__main__":
    sys.exit(main())
