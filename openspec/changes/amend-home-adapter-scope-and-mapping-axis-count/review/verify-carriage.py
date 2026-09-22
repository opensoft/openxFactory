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

FOUR THINGS THIS SCRIPT DOES THE LONG WAY, EVERY ONE ON A COPILOT FINDING
AGAINST AN EARLIER DRAFT OF IT, ACROSS THREE ROUNDS ON `opensoft/openxFactory#1143`
(`r4075847837` and `r4075847914` against the first draft; the terminator finding
of round 5, and the ordering gap found while fixing it) — and every one for the
same reason: **a carriage proof that is approximately right proves nothing.**
Items (1) and (2) are what the first draft got wrong about WHAT IT READ; items
(3) and (4) are what the next drafts got wrong about WHAT IT COMPARED.

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

(3) IT SAYS WHAT A BLOCK IS, AND STOPS CLAIMING MORE THAN IT COMPARES
(`r4076204332`'s successor finding on `opensoft/openxFactory#1143`). The earlier
drafts said BYTE-FOR-BYTE while `rstrip("\n")` normalized each block's trailing
newlines, so a change in the number of blank lines between blocks passed as
identical and the claim was wider than the comparison. **THE CANONICAL BLOCK IS
DEFINED HERE RATHER THAN LEFT TO A STRIP CALL**: a block runs from its
`#### Scenario:` line through its LAST NON-BLANK line, and every byte inside
that span — every bullet, every space, every internal blank line — must match
exactly. Blank lines BETWEEN blocks are outside every block by that definition
and are deliberately not compared: they carry no requirement text, the OpenSpec
parser does not read them, and a check that reddened on a cosmetic reflow would
be one nobody ran. The script reports the definition with its verdict, so the
claim and the comparison are the same sentence.

(4) IT COMPARES IN ORDER, not as a set. Membership alone would pass a delta that
carried every promoted scenario in a different sequence — a reordering of the
requirement that no reader asked for and this script was meant to catch. The
promoted blocks must appear among the delta's in their PROMOTED ORDER.
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

    A BLOCK RUNS FROM ITS `#### Scenario:` LINE THROUGH ITS LAST NON-BLANK LINE.
    That boundary is the definition, not a convenience: every byte inside the
    span is compared exactly, and the blank lines BETWEEN blocks fall outside
    every block and are not compared at all. They carry no requirement text, the
    OpenSpec parser does not read them, and a check that reddened on a cosmetic
    reflow is a check nobody runs. What the earlier draft did by `rstrip` and
    called byte-for-byte, this does by definition and says so.
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
        # The canonical boundary: keep every byte up to and including the last
        # NON-BLANK line, so internal blank lines survive the comparison and only
        # the run of blank lines separating one block from the next is dropped.
        blocks = []
        for piece in pieces:
            if not piece.strip():
                continue
            lines = piece.split("\n")
            while lines and not lines[-1].strip():
                lines.pop()
            blocks.append("\n".join(lines))
        return blocks
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
        # IN ORDER, not merely present. Membership alone would pass a delta that
        # carried every promoted scenario in a different sequence.
        positions = [mine.index(block) for block in carried]
        if positions != sorted(positions):
            out_of_order = [carried[i].splitlines()[0]
                            for i in range(1, len(positions))
                            if positions[i] < positions[i - 1]]
            print(f"FAIL {capability}: the promoted scenario blocks are all "
                  f"present but REORDERED; first out of sequence -> "
                  f"{out_of_order[0]}")
            failures += 1
            continue
        print(f"OK {capability}: all {len(carried)} promoted scenario blocks "
              f"carried exactly and in order among the delta's {len(mine)} "
              f"parsed blocks (a block is its heading through its last "
              f"non-blank line; blank lines between blocks are outside every "
              f"block and are not compared)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
