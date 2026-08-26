#!/usr/bin/env python3
"""Verify every per-file sha256 recorded in contracts/manifest.yaml.

The consumption contract (release-review finding N7): contracts/manifest.yaml
is what cross-repo consumers read to verify the bytes they pin, yet nothing
checked ITS digests — a stale entry (content-manifest.schema.yaml, stale
since 403c2b5) rode through three bundle cuts undetected. This checker walks
every artifact entry carrying a `sha256` field, recomputes the digest of the
file at `path`, and fails closed on any mismatch or missing file. Entries
without a sha256 field (directory registrations, content-addressed-by-commit
families) are out of scope by design.

Run: python3 scripts/validate-manifest-digests.py
Exit codes: 0 all digests verify, 1 mismatches, 2 harness error.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts" / "manifest.yaml"


def iter_entries(node):
    if isinstance(node, dict):
        if "sha256" in node and "path" in node:
            yield node
        for value in node.values():
            yield from iter_entries(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_entries(item)


def main() -> int:
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    failures = 0
    checked = 0
    for entry in iter_entries(doc):
        path = ROOT / str(entry["path"])
        recorded = str(entry["sha256"])
        checked += 1
        if not path.is_file():
            print(f"FAIL {entry['path']}: recorded in the manifest but missing on disk")
            failures += 1
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != recorded:
            print(f"FAIL {entry['path']}: manifest records {recorded[:12]}… "
                  f"but the bytes hash to {actual[:12]}…")
            failures += 1
    if failures:
        print(f"FAIL {failures}/{checked} manifest digest(s) do not verify")
        return 1
    print(f"OK contracts/manifest.yaml: {checked} per-file digest(s) verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
