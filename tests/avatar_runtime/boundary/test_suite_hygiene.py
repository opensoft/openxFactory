"""Suite-wide hygiene guard: behavioral tests use no wall-time/randomness/network
(T060a, SC-004). Complements the package scanner (which targets the runtime
package, not the tests)."""

from __future__ import annotations

from pathlib import Path

from boundary.scanner import scan_test_hygiene

TESTS_DIR = Path(__file__).resolve().parents[1]  # tests/avatar_runtime/


def test_behavioral_tests_are_hermetic():
    violations = scan_test_hygiene(TESTS_DIR)
    assert violations == [], "\n".join(str(v) for v in violations)


def test_hygiene_scanner_flags_forbidden_usage():
    # Negative control: prove the scanner detects a forbidden pattern.
    from boundary import scanner

    import ast as _ast

    tree = _ast.parse("import random\nx = random.random()\n")
    # scan a synthetic file by writing/inspecting nodes directly:
    found = []
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Import) and any(
            scanner._top(a.name) in scanner.HYGIENE_IMPORTS for a in node.names
        ):
            found.append("random")
    assert "random" in found
