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

TWO THINGS THIS SCRIPT DOES THE LONG WAY, BOTH ON COPILOT FINDINGS AGAINST ITS
FIRST DRAFT (`r4075847837`, `r4075847914` on `opensoft/openxFactory#1143`), and
both because a carriage proof that is approximately right proves nothing.

(1) IT READS BYTES AND REFUSES A CARRIAGE RETURN, rather than reading text.
`Path.read_text()` applies universal-newline conversion before any comparison
runs, so a promoted scenario whose line endings changed to CRLF would compare
EQUAL to a delta carrying LF — the script would report a byte-for-byte match
over bytes it had already normalized. Both files are therefore read as bytes,
decoded strictly, and refused outright if either contains `\r`: this corpus
writes LF, and an unexpected CR is a fact to report rather than to smooth.

(2) IT COMPARES PARSED SCENARIO BLOCKS, not a substring of the delta file. A
`carried in delta_text` search passes when the promoted bytes survive ANYWHERE
in the file — in explanatory prose, in a marker, or under a different
requirement — while the requirement's actual scenario blocks are replaced. That
is not a hypothetical here: this packet's `domain-mapping-declaration` delta
carries a promoted BODY unit verbatim inside a `Removed from canon by` marker,
exactly the kind of quotation a substring search would accept as carriage. So
each side is parsed into individual `#### Scenario:` blocks under the SAME
requirement title, and every promoted block must appear among the DELTA's
parsed blocks.
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


def read_lf_bytes(path: pathlib.Path) -> str:
    """The file's bytes, decoded strictly, with a carriage return REFUSED.

    Never `read_text()`: its universal-newline conversion would make a CRLF file
    compare equal to an LF one and turn this script's own claim into a
    tautology.
    """
    raw = path.read_bytes()
    if b"\r" in raw:
        raise SystemExit(
            f"{path}: contains a carriage return. This corpus writes LF, and a "
            f"byte-for-byte comparison across mixed line endings is not one — "
            f"reported rather than normalized away")
    return raw.decode("utf-8")


def scenario_blocks(text: str, title: str) -> list[str]:
    """Every `#### Scenario:` block under `title`, as separate strings.

    Blocks and not one region: the comparison must be per scenario, so that a
    promoted block surviving somewhere in the file cannot stand in for one that
    was replaced where it matters.
    """
    for part in re.split(r"(?m)^### Requirement: ", text)[1:]:
        head, _, body = part.partition("\n")
        if head.strip() != title:
            continue
        index = body.find("#### Scenario:")
        if index == -1:
            raise SystemExit(f"no scenarios under {title!r}")
        region = body[index:]
        # Stop at the next requirement or top-level section, if any follows.
        cut = re.search(r"(?m)^(?:### Requirement: |## )", region)
        if cut:
            region = region[:cut.start()]
        pieces = re.split(r"(?m)^(?=#### Scenario:)", region)
        return [piece.rstrip("\n") for piece in pieces if piece.strip()]
    raise SystemExit(f"requirement not found: {title!r}")


def main() -> int:
    failures = 0
    for capability, title, expected in PAIRS:
        promoted = read_lf_bytes(ROOT / "openspec/specs" / capability / "spec.md")
        delta = read_lf_bytes(PACKET / "specs" / capability / "spec.md")
        carried = scenario_blocks(promoted, title)
        mine = scenario_blocks(delta, title)
        if len(carried) != expected:
            print(f"FAIL {capability}: promoted requirement has {len(carried)} "
                  f"scenarios, this script expects {expected} — re-derive before "
                  f"trusting the compare")
            failures += 1
            continue
        missing = [block for block in carried if block not in mine]
        if missing:
            print(f"FAIL {capability}: {len(missing)} promoted scenario block(s) "
                  f"not carried byte-identically; first -> "
                  f"{missing[0].splitlines()[0]}")
            failures += 1
            continue
        print(f"OK {capability}: all {len(carried)} promoted scenario blocks "
              f"carried byte-identically among the delta's {len(mine)} parsed "
              f"blocks")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
