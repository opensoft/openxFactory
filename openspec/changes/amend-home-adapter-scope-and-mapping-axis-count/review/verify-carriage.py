#!/usr/bin/env python3
"""Re-prove that this packet's two `## MODIFIED` blocks carry EVERY scenario the
promoted requirements have, exactly and in order, and that live canon has not
moved under them.

A `## MODIFIED Requirements` block REPLACES the requirement it names, so a
scenario retyped with one character changed, or silently dropped, is a
requirement quietly narrowed at promotion. The blocks were built by extracting
the promoted scenarios programmatically rather than by retyping them. THIS
SCRIPT RE-EXTRACTS THEM FROM THE IMMUTABLE BASIS, NOT FROM `openspec/specs/`:
`BASIS` below is the archived packet that PROMOTED both requirements,
`openspec/changes/archive/2026-09-22-split-opendox-two-layer-product/specs/`,
whose files never move, while `openspec/specs/` is the mutable current state
this very amendment rewrites when it archives. Live canon is read for ONE thing,
the currency check in `canon_state`, which passes only while canon states either
that basis or this packet's block. So the proof survives every later edit to the
packet, and the packet's own archive.

    python3 openspec/changes/amend-home-adapter-scope-and-mapping-axis-count/review/verify-carriage.py

That is the path while the change is active; once it archives, the same file
sits under `openspec/changes/archive/<date>-amend-home-adapter-scope-and-mapping-axis-count/review/`.
The root is found by marker from the script's own location, so the working
directory does not change what it reads.

Exit 0 with one `OK` line per capability. Exit 1 with one `FAIL` line for each
capability that fails — a promoted scenario count other than the one `PAIRS`
expects, the first promoted scenario not carried exactly, the first carried out
of order, or a canon state that must stop a reader — or at once, with a message
naming the path and the reason, when an input is missing, is not valid UTF-8,
carries a carriage return, or lacks the requirement it must hold.

SEVEN THINGS THIS SCRIPT DOES THE LONG WAY, and every one for the same reason:
**a carriage proof that is approximately right proves nothing.** Each was forced
by a defect in an earlier draft of it. Every one but (4) was found by Copilot
review on `opensoft/openxFactory#1143`; (4) was found by the author while fixing
(3). The record, with the control that proved each, is `design.md` D4b and D4d
through D4f.

(1) IT READS BYTES AND REFUSES A CARRIAGE RETURN, rather than reading text —
and it refuses a missing file or invalid UTF-8 by name as well, rather than
raising (Copilot `r4077737673`, against the docstring's own promise).
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
(Copilot `r4076352166` on `opensoft/openxFactory#1143`). The earlier
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

(5) IT READS THE IMMUTABLE BASIS, NOT CANON (Copilot `r4076557378`). An earlier
draft re-extracted from `openspec/specs/`, which this amendment rewrites when it
archives: it would then have found six and four scenarios where `PAIRS` expects
three, and reported FAIL from inside its own archived packet for having
succeeded. See `BASIS`.

(6) IT CHECKS CANON AGAINST FOUR STATES, OVER THE WHOLE REQUIREMENT (Copilot
`r4076675504`, and the item review `5284063015` listed as previously missed).
Canon ABSENT is a failure, not a pass; and the comparison covers the normative
body as well as the scenarios, because a body-only edit is exactly the kind that
could move canon unseen. See `canon_state` and `requirement_section`.

(7) IT FINDS THE ROOT BY MARKER, NOT BY DEPTH (Copilot `r4076754060`). Archiving
moves this file one directory deeper, where a `parent.parent.parent` root would
resolve to `<repo>/openspec`. See `_repo_root`.
"""
from __future__ import annotations

import pathlib
import re
import sys

PACKET = pathlib.Path(__file__).resolve().parent.parent


def _repo_root(start: pathlib.Path) -> pathlib.Path:
    """The repository root, found by MARKER and never by counting directories.

    A depth calculation (`parent.parent.parent`) is correct exactly once: today,
    with this packet at `openspec/changes/<id>/review/`. Archiving moves it one
    level deeper to `openspec/changes/archive/<date>-<id>/review/`, and the same
    expression then answers `<repo>/openspec` — so `BASIS` and canon both resolve
    under `<repo>/openspec/openspec/...` and the post-archive run this script
    promises fails on a path error. Walking up to the directory that actually
    holds `openspec/specs` and `openspec/changes` is depth-independent, which is
    the property the promise needs.
    """
    for candidate in (start, *start.parents):
        if (candidate / "openspec" / "specs").is_dir() and \
                (candidate / "openspec" / "changes").is_dir():
            return candidate
    raise SystemExit(
        f"no repository root above {start}: looked for a directory holding both "
        f"`openspec/specs` and `openspec/changes`")


ROOT = _repo_root(PACKET)

#: THE IMMUTABLE BASIS, and it is NOT `openspec/specs/`. Canon is the mutable
#: current state: the moment this amendment archives, `openspec/specs/` carries
#: the AMENDED requirements and a script expecting the pre-amendment scenario
#: counts would fail from inside its own archived packet — a committed proof that
#: reports FAIL for having succeeded. The reference is therefore the archived
#: packet that PROMOTED these requirements, whose delta files never move; and the
#: two were measured byte-identical block for block when this was written, so
#: nothing is weakened by reading the stable one.
BASIS = ROOT / "openspec/changes/archive/2026-09-22-split-opendox-two-layer-product/specs"

PAIRS = (
    ("corpus-adapter-seam",
     "The corpus reader is an external pinned product and the dependency points one way", 3),
    ("domain-mapping-declaration",
     "A domain descendant declares its mapping, and the neutral layer ships no domain's vocabulary", 3),
)


def read_lf_bytes(path: pathlib.Path) -> str:
    """The file's bytes, decoded strictly, with a carriage return REFUSED — and a
    missing file or invalid UTF-8 refused BY NAME, never raised as a traceback.

    Never `read_text()`: its universal-newline conversion would make a CRLF file
    compare equal to an LF one and turn this script's own claim into a
    tautology. And never a bare `read_bytes()`: the module docstring promises
    that an unreadable input exits at once WITH THE REASON (Copilot
    `r4077737673`), and a `FileNotFoundError` traceback is the reason buried in
    a stack rather than stated.
    """
    if not path.is_file():
        raise SystemExit(
            f"{path}: not found. This proof reads it and it is missing — "
            f"reported by name rather than raised")
    raw = path.read_bytes()
    if b"\r" in raw:
        raise SystemExit(
            f"{path}: contains a carriage return. This corpus writes LF, and a "
            f"byte-for-byte comparison across mixed line endings is not one — "
            f"reported rather than normalized away")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SystemExit(
            f"{path}: not valid UTF-8 ({error.reason} at byte {error.start}) — "
            f"reported by name rather than raised") from None


def requirement_section(text: str, title: str) -> str:
    """The whole requirement under `title` — normative body AND scenarios.

    `scenario_blocks` alone is the wrong unit for the currency check: a canon
    requirement whose scenarios are untouched but whose BODY changed would
    compare equal and pass, so a concurrent body-only edit — exactly the kind
    this amendment itself makes — could move canon under this block unnoticed.
    The carriage proof is per scenario because that is what a `## MODIFIED` block
    must carry; the CURRENCY check is over the whole requirement because that is
    what could move.
    """
    for part in re.split(r"(?m)^### Requirement: ", text)[1:]:
        head, _, body = part.partition("\n")
        if head.strip() != title:
            continue
        cut = re.search(r"(?m)^(?:### Requirement: |## )", body)
        return (body[:cut.start()] if cut else body).rstrip("\n")
    raise SystemExit(f"requirement not found: {title!r}")


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


def canon_state(capability: str, title: str,
                basis: str, mine: str) -> tuple[bool, str]:
    """Where live canon stands relative to the basis this block was written over.

    FOUR STATES AND TWO ARE FAILURES. Canon equal to the basis is the review-time
    state: nothing has moved under this block. Canon equal to THIS BLOCK is the
    post-archive state: the amendment has been applied and the proof above is
    historical and still true. Canon matching neither means something else moved
    it, and canon ABSENT means the capability the basis promoted was deleted —
    both are cases a reader must be stopped on.

    COMPARED OVER THE WHOLE REQUIREMENT, body and scenarios together, and not
    over the scenario blocks alone: a canon requirement whose scenarios are
    untouched but whose normative body changed would otherwise compare equal and
    pass. The carriage proof above is per scenario because that is what a
    `## MODIFIED` block must carry; this check is over the whole requirement
    because that is what could move.
    """
    canon_path = ROOT / "openspec/specs" / capability / "spec.md"
    if not canon_path.is_file():
        # NOT a valid state, and not a pass. `BASIS` is the archived packet that
        # ALREADY promoted this capability, so canon existed when this was
        # written; its absence means the capability was deleted rather than
        # amended — which is the failure mode this corpus has actually met, and
        # a check that shrugged at it would let a deleted spec pass as carriage.
        return False, f"canon absent at {canon_path}: the capability the basis promoted is gone"
    canon = requirement_section(read_lf_bytes(canon_path), title)
    if canon == basis:
        return True, ("canon still states the basis, body and scenarios both — "
                      "nothing moved under this block")
    if canon == mine:
        return True, ("canon now states THIS BLOCK, body and scenarios both — "
                      "the amendment has been applied and the proof above is "
                      "historical")
    return False, ("canon matches NEITHER the basis nor this block over the "
                   "requirement's full text: something else moved it")


def main() -> int:
    failures = 0
    for capability, title, expected in PAIRS:
        promoted = read_lf_bytes(BASIS / capability / "spec.md")
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
        ok, note = canon_state(
            capability, title,
            requirement_section(promoted, title),
            requirement_section(delta, title))
        if not ok:
            print(f"FAIL {capability}: {note}")
            failures += 1
            continue
        print(f"OK {capability}: all {len(carried)} promoted scenario blocks "
              f"carried exactly and in order among the delta's {len(mine)} "
              f"parsed blocks (a block is its heading through its last "
              f"non-blank line; blank lines between blocks are outside every "
              f"block and are not compared); {note}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
