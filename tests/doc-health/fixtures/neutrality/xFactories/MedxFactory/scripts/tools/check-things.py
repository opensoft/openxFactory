#!/usr/bin/env python3
"""Fixture: a generic tree checker with zero domain vocabulary.

Planted for the neutrality-drift tests: it must trip
uninventoried_tooling (absent from stack.yaml's required-artifact
surface), lexicon_absence (no domain terms anywhere), and
cross_repo_consumer (another fixture repo references its path).
"""

import sys
from pathlib import Path


def count_files(root: Path) -> int:
    return sum(1 for p in root.rglob("*") if p.is_file())


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(f"files: {count_files(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
