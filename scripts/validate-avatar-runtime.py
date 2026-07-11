#!/usr/bin/env python3
"""Standalone execution-free boundary gate for the AVC reference runtime.

Declared narrow governance exception (FR-036, SC-008): the ONLY out-of-tree
artifact this feature writes, alongside its single README validator-index line.
It statically scans ``xfactory/avatar_runtime/`` — imports, exports, entrypoints,
and file surfaces — WITHOUT importing or executing runtime code, and fails if it
finds any listener, application factory, deployment file, persistence adapter,
provider/network SDK, credential loading, provisional-test import, or forbidden
entrypoint (FR-001/FR-004a, SC-005/010).

Usage:  python scripts/validate-avatar-runtime.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "xfactory" / "avatar_runtime"

# Reuse the same scanner the in-suite boundary test uses (identical rules).
sys.path.insert(0, str(ROOT / "tests" / "avatar_runtime"))
from boundary.scanner import scan_package, scan_test_hygiene  # noqa: E402


def main() -> int:
    violations = scan_package(PKG)
    hygiene = scan_test_hygiene(ROOT / "tests" / "avatar_runtime")

    print(f"validate-avatar-runtime: scanned {PKG.relative_to(ROOT)} (stdlib-only reference package)")
    if not violations:
        print("  boundary: OK — no deployment surface, third-party, provider SDK, or provisional import")
    else:
        for v in violations:
            print(f"  BOUNDARY VIOLATION {v}")
    if hygiene:
        for v in hygiene:
            print(f"  TEST-HYGIENE {v}")
    else:
        print("  test hygiene: OK — no wall-time/randomness/network usage in behavioral tests")

    total = len(violations) + len(hygiene)
    if total:
        print(f"FAIL: {total} boundary/hygiene violation(s)")
        return 1
    print("OK: reference package is non-deployable and stdlib-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
