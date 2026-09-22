#!/usr/bin/env python3
"""Re-prove that this packet's two `## MODIFIED` blocks carry EVERY scenario the
promoted requirements have, byte for byte.

A `## MODIFIED Requirements` block REPLACES the requirement it names, so a
scenario retyped with one character changed, or silently dropped, is a
requirement quietly narrowed at promotion. The blocks were built by extracting
the promoted scenarios programmatically rather than by retyping them; this
script re-extracts from `openspec/specs/` and compares, so the proof survives
every later edit to the packet.

    python3 openspec/changes/amend-home-adapter-scope-and-mapping-axis-count/review/verify-carriage.py

Exit 0 and one line per capability, or exit 1 naming the first scenario that
does not match. Run from the openxFactory root.
"""
from __future__ import annotations

import pathlib
import re
import sys

PACKET = pathlib.Path(__file__).resolve().parent.parent
ROOT = PACKET.parent.parent.parent

PAIRS = (
    ("corpus-adapter-seam",
     "The corpus reader is an external pinned product and the dependency points one way", 3),
    ("domain-mapping-declaration",
     "A domain descendant declares its mapping, and the neutral layer ships no domain's vocabulary", 3),
)


def scenarios_of(text: str, title: str) -> str:
    for part in re.split(r"(?m)^### Requirement: ", text)[1:]:
        if part.split("\n", 1)[0].strip() == title:
            body = part.split("\n", 1)[1]
            index = body.find("#### Scenario:")
            if index == -1:
                raise SystemExit(f"no scenarios under {title!r}")
            return body[index:].rstrip("\n")
    raise SystemExit(f"requirement not found: {title!r}")


def main() -> int:
    failures = 0
    for capability, title, expected in PAIRS:
        promoted = (ROOT / "openspec/specs" / capability / "spec.md").read_text()
        delta = (PACKET / "specs" / capability / "spec.md").read_text()
        carried = scenarios_of(promoted, title)
        count = carried.count("#### Scenario:")
        if count != expected:
            print(f"FAIL {capability}: promoted requirement has {count} scenarios, "
                  f"this script expects {expected} — re-derive before trusting the compare")
            failures += 1
            continue
        if carried not in delta:
            for block in carried.split("\n\n"):
                if block.strip() and block not in delta:
                    print(f"FAIL {capability}: not carried byte-identically -> "
                          f"{block.splitlines()[0]}")
                    break
            failures += 1
            continue
        print(f"OK {capability}: all {count} promoted scenarios carried byte-identically; "
              f"block carries {delta.count('#### Scenario:')} in total")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
