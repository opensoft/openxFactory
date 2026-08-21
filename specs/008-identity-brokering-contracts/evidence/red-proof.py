#!/usr/bin/env python3
"""Red-proof harness for the identity-brokering negative corpus.

A green self-test proves the negatives fail. It does NOT prove they fail
because the rule they name is doing the work — a fixture can drift into
tripping something incidental (a generic `schema` finding, most often) while
its own suite stays green.

This suppresses each expected finding code in turn and asserts the packaged
corpus goes RED. A code that can be neutered while the bar stays green has a
negative confirmation that proves nothing.

THE CODE SET IS DERIVED, NOT LISTED. `main()` reads it from the `#
expected_failure:` header of every file under `examples/negative/`, so a fixture
introducing a new code is covered the moment it lands and a code losing its last
fixture disappears from the proof rather than passing vacuously. That is why the
2026-08-21 review hardening needed no edit here: adding fourteen fixtures took
the proof from nineteen codes to twenty-two by itself.

Two of those codes are bound in the SCHEMA as well as reported by a rule
(`write-action-without-resolved-authorization` for a named-but-unoffered write
action, `isolation-restriction-unrecorded` for a co-residence answer with
nothing referenced). Those always fire beside a `schema` finding, on purpose —
the same convention rule (h) uses for a second governed-record pointer: the
shape carries the bound, and the code makes the refusal name the rule. Their
red proof is still meaningful, because suppressing the code removes the message
a reader would act on.

Run from the repository root:

    python3 specs/008-identity-brokering-contracts/evidence/red-proof.py

Exit codes: 0 every code load-bearing, 1 one or more neuterable silently.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "validate-identity-brokering.py"


def load():
    spec = importlib.util.spec_from_file_location(
        "validate_identity_brokering", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fresh_context(m):
    """The same context main() builds — every runtime-read vocabulary included.
    A vocabulary missing here reads as an empty legal set, which makes the
    POSITIVES fail and inflates every neutered run's error count by a constant:
    the harness would still report RED everywhere while measuring its own
    misconfiguration rather than the rule under test."""
    canonical, reserved = m.layer_vocabulary()
    docs = m.load_schemas()
    ctx = m.Context(
        canonical, reserved,
        m.schema_enum(docs, "identity-link-record.schema.yaml",
                      "properties", "basis"),
        m.schema_enum(docs, "surface-adoption.schema.yaml", "properties",
                      "resolved_authorization", "properties", "resolves_in"),
        m.schema_enum(docs, "broker-organization.schema.yaml", "properties",
                      "governed_record_refs", "items", "properties",
                      "resolves_in"),
    )
    for path in m.positive_paths():
        ctx.index(m.load_yaml(path))
    return docs, ctx


def run_with_code_suppressed(code: str) -> int:
    m = load()
    original = m.Findings.error

    def patched(self, c, msg, _c=code, _o=original):
        if c == _c:
            return  # neuter exactly this rule
        _o(self, c, msg)

    m.Findings.error = patched
    docs, ctx = fresh_context(m)
    findings = m.Findings()
    with contextlib.redirect_stdout(io.StringIO()):
        m.self_test(findings, docs, ctx)
    return len(findings.errors)


def main() -> int:
    base = load()
    codes = sorted({base.expected_failure(p)[0]
                    for p in base.negative_paths()})
    silent = []
    for code in codes:
        errors = run_with_code_suppressed(code)
        print(f"  {'RED  ' if errors else 'GREEN'}  neutered {code:44s} "
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
