"""Round-trip on demote: the fragment refresh (`align-demote-to-round-trip-rule`).

PURE. Text in, text out — no paths, no I/O, no knowledge of a plan or a tree.
`gate_console.execute_demotion_plan` reads bytes, calls in here, writes bytes.
That split is design Decision 2: this is markdown surgery, it is the part most
worth testing without a tree, and gate_console.py is already ~1250 lines of
planning and recording.

WHAT THIS EXISTS TO FIX. The ratified rule "A demoted topic does not reset to its
aspirational text" was inverted by the mechanism: a demote routed the change
folder's pre-proposal SNAPSHOT of the topic's primary fragment back over the live
fragment, so everything learned while the change was in flight was discarded at
exactly the moment it was most valuable. The two operations below are the
correction — the provenance slots and the `xspec:candidate`-marked sections are
refreshed, and NOTHING ELSE IN THE DOCUMENT IS TOUCHED. That boundedness is what
makes it safe to refresh a fragment a human has been working in.

THREE PROPERTIES, each load-bearing and each tested:

* FENCE-AWARE. The canonical template ships as a copy-pasteable ```markdown
  skeleton whose body contains the provenance heading and every slot line. A
  fragment that merely QUOTES the skeleton has adopted nothing, and a fence-blind
  rewrite would edit somebody's example. The predicate below is byte-for-byte the
  one `doc_health.families` and `web/views/outline-model.js` already share; a
  companion test pins all three agreeing, because this is the corpus's THIRD
  implementation of one rule (design Decision 2's named hazard).
* BYTE-PRESERVING OUTSIDE THE EDIT. Every line keeps its own original line
  ending; only lines this module CREATES take the document's flavor. That is
  strictly stronger than detecting one flavor and rejoining with it, which would
  silently rewrite every ending in a mixed-EOL document — the defect class this
  corpus has already paid for twice (the doxBench base-lens fix, and the demote
  move's own `read_text`/`write_text` retranslation).
* IDEMPOTENT. Both operations are ADDRESSED rather than appending: the slots are
  overwritten in place, the fenced bodies replaced in place. Running twice with
  the same inputs therefore produces the same bytes, which the requirement demands
  and a test asserts.
"""

from __future__ import annotations

import re

# The skeleton's own heading, matched case-insensitively on its stable prefix so a
# fragment that spells the parenthetical differently is still found.
PROVENANCE_HEADING = "## Last proposal attempt (round-trip provenance)"
PROVENANCE_NEEDLE = "last proposal attempt"

# The five slots the skeleton carries, in its order. The ratified rule's prose
# enumerates four VALUES (change id, both dates, reason) and the skeleton adds
# `Status at demote`, whose own comment says to replace every field below it — so
# all five are filled. `Status at demote` is `active` for every reachable demote
# today, because `plan_demotion` refuses a change in any other state; it is filled
# anyway, because a slot still reading `n/a` after a real demote is worse than one
# reading a true constant.
SLOT_ORDER = (
    "Change ID",
    "Raised",
    "Status at demote",
    "Demoted",
    "Demote reason",
)

# What a slot says when the value genuinely could not be resolved. The
# requirement forbids both fabricating a value and leaving the slot reading as an
# unused placeholder, so this is neither a guess nor `n/a`.
UNAVAILABLE = "unavailable"

# `<!-- xspec:candidate ... -->` opens a proposal-element block; the matching
# `<!-- /xspec:candidate -->` closes it. The marker comments are the ADDRESSING
# KEY and are never rewritten — rewriting an addressing key mid-operation is how
# two sides stop agreeing about what they are addressing.
_XSPEC_OPEN = re.compile(r"<!--\s*xspec:candidate\b")
_XSPEC_CLOSE = re.compile(r"<!--\s*/\s*xspec:candidate\s*-->")

_EOL = re.compile(r"\r\n|\r|\n")


def _is_fence(line: str) -> bool:
    """The SHARED fence predicate, byte-for-byte.

    `doc_health.families._scan_lines` / `_template_gaps` use
    `line.lstrip().startswith("```")`; `outline-model.js`'s `isFence` uses
    `String(line).trimStart().startsWith("```")`. Same algorithm, deliberately
    naive (an opening fence with a language tag toggles, and so does its closer).
    Do not "improve" this one without the other two: a companion test pins all
    three on a shared fixture set.
    """
    return line.lstrip().startswith("```")


def split_keepends(text: str) -> list[tuple[str, str]]:
    """`text` as [(body, ending)] pairs, where ''.join(b + e) IS `text`.

    NOT `str.splitlines(keepends=True)`, which also breaks on \\x0b, \\x0c,
    \\x1c-\\x1e, \\x85, U+2028 and U+2029. A governance document containing one of
    those would be silently re-split and rejoined into different bytes. Only the
    three real line endings separate lines here, and the identity above is
    asserted in the tests.
    """
    rows: list[tuple[str, str]] = []
    at, size = 0, len(text)
    while at < size:
        match = _EOL.search(text, at)
        if match is None:
            rows.append((text[at:], ""))
            break
        rows.append((text[at:match.start()], match.group(0)))
        at = match.end()
    return rows


def join_rows(rows: list[tuple[str, str]]) -> str:
    return "".join(body + ending for body, ending in rows)


def document_eol(rows: list[tuple[str, str]]) -> str:
    """The flavor NEW lines take: the document's FIRST real ending.

    The first-break rule, not a majority vote — the same rule
    `doxbench-editor.js`'s `eolFlavorOf` applies to the same documents, so a
    fragment edited in the outline tab and a fragment refreshed by a demote agree
    about what its flavor is.
    """
    for _body, ending in rows:
        if ending:
            return ending
    return "\n"


def _heading_text(body: str) -> str | None:
    return body[3:].strip() if body.startswith("## ") else None


def _section_bounds(rows: list[tuple[str, str]]) -> list[tuple[int, str, int]]:
    """Every `## ` section OUTSIDE a fence, as (heading_row, title, end_row).

    `end_row` is exclusive — the index of the next such heading, or len(rows).
    """
    heads: list[tuple[int, str]] = []
    fenced = False
    for index, (body, _ending) in enumerate(rows):
        if _is_fence(body):
            fenced = not fenced
            continue
        if fenced:
            continue
        title = _heading_text(body)
        if title is not None:
            heads.append((index, title))
    out = []
    for position, (index, title) in enumerate(heads):
        end = heads[position + 1][0] if position + 1 < len(heads) else len(rows)
        out.append((index, title, end))
    return out


def _fenced_flags(rows: list[tuple[str, str]]) -> list[bool]:
    """Per-row "is inside a fence", with the fence lines themselves marked True.

    Matches `_scan_lines`, which yields True FOR the fence line: a fence delimiter
    is never content to be rewritten.
    """
    flags: list[bool] = []
    fenced = False
    for body, _ending in rows:
        if _is_fence(body):
            fenced = not fenced
            flags.append(True)
            continue
        flags.append(fenced)
    return flags


def find_provenance_section(rows: list[tuple[str, str]]) -> tuple[int, int] | None:
    """(heading_row, end_row) of the provenance section, or None. Fence-aware."""
    for index, title, end in _section_bounds(rows):
        if PROVENANCE_NEEDLE in title.lower():
            return index, end
    return None


def _slot_line(name: str, value: str, ending: str) -> tuple[str, str]:
    text = str(value) if str(value).strip() else UNAVAILABLE
    return (f"{name}: {text}", ending)


def fill_provenance_slots(text: str, values: dict[str, str]) -> str:
    """Fill the round-trip provenance slots, in place where they exist.

    A slot present in the section is REWRITTEN and keeps its own line ending (the
    `_flip_status` precedent — flipping a CRLF line must not be the one line that
    comes out LF). A slot the section lacks is appended to the slot block. A
    fragment with no provenance section at all — most of the corpus, since template
    conformance is opt-in — has the section INSERTED in the template's canonical
    position, ahead of the first `## ` section.

    Inserting a section a topic did not have is a real content change, and that is
    why it belongs to a demote rather than to doc-health: it happens because a
    human ran a gate verb, not because a checker looked at the file.
    """
    rows = split_keepends(text)
    eol = document_eol(rows)
    wanted = {name: values.get(name, UNAVAILABLE) for name in SLOT_ORDER}

    found = find_provenance_section(rows)
    if found is None:
        return join_rows(_insert_provenance_section(rows, wanted, eol))

    start, end = found
    flags = _fenced_flags(rows)
    seen: dict[str, int] = {}
    for index in range(start + 1, end):
        if flags[index]:
            continue
        body = rows[index][0]
        for name in SLOT_ORDER:
            if name in seen:
                continue
            if body.startswith(f"{name}:"):
                seen[name] = index
                break

    out = list(rows)
    for name, index in seen.items():
        out[index] = _slot_line(name, wanted[name], rows[index][1])

    missing = [name for name in SLOT_ORDER if name not in seen]
    if missing:
        # Appended after the LAST slot line present, so a partially-filled block
        # keeps its own order and grows at its end; with no block at all the slots
        # go directly under the heading.
        anchor = max(seen.values()) if seen else start
        block = [_slot_line(name, wanted[name], eol) for name in missing]
        if not seen:
            block = [("", eol)] + block
        out[anchor + 1:anchor + 1] = block
    return join_rows(out)


def _insert_provenance_section(
    rows: list[tuple[str, str]], wanted: dict[str, str], eol: str,
) -> list[tuple[str, str]]:
    """The whole section, ahead of the first `## ` section (canonical position).

    The skeleton's advisory HTML comment is deliberately NOT carried: it is an
    authoring aid, not part of the provenance contract, and a second copy of that
    prose in code would be one more thing to keep in step with the ratified doc.
    """
    block: list[tuple[str, str]] = [(PROVENANCE_HEADING, eol), ("", eol)]
    block += [_slot_line(name, wanted[name], eol) for name in SLOT_ORDER]

    sections = _section_bounds(rows)
    at = sections[0][0] if sections else len(rows)

    head = list(rows[:at])
    tail = list(rows[at:])
    while head and head[-1][0].strip() == "":
        head.pop()
    out = head
    if out:
        out = out + [("", eol)]
    out = out + block
    if tail:
        out = out + [("", eol)] + tail
    else:
        out = out + [("", eol)]
    # A document that ended without a trailing newline keeps ending without one
    # only if nothing was appended after it; when the block lands last it ends the
    # file properly.
    return out


def proposal_sections(text: str) -> dict[str, list[tuple[str, str]]]:
    """`## ` section bodies of a proposal, keyed by lowercased heading.

    Fence-aware, and the body is trimmed of leading/trailing blank lines so a
    refresh inserts the section's prose rather than its surrounding whitespace.
    """
    rows = split_keepends(text)
    out: dict[str, list[tuple[str, str]]] = {}
    for start, title, end in _section_bounds(rows):
        body = list(rows[start + 1:end])
        while body and body[0][0].strip() == "":
            body.pop(0)
        while body and body[-1][0].strip() == "":
            body.pop()
        out[title.strip().lower()] = body
    return out


def refresh_marked_sections(fragment_text: str, proposal_text: str) -> str:
    """Replace each marked section's fenced body with the proposal's own text.

    ONLY sections present in BOTH documents are rewritten. A section the proposal
    does not carry is left alone (never invented), and a section the proposal
    carries but the fragment does not mark is not added (the fragment's marked set
    is the human's declaration of which proposal elements this topic carries, and
    a demote is not the moment to widen it).

    An `xspec:candidate` block with no closing marker is left UNTOUCHED. An
    unterminated marker is malformed, and guessing where it ends would be a
    rewrite over an unknown span — refusing is the only safe answer.
    """
    if not proposal_text:
        return fragment_text
    incoming = proposal_sections(proposal_text)
    if not incoming:
        return fragment_text

    rows = split_keepends(fragment_text)
    eol = document_eol(rows)
    flags = _fenced_flags(rows)

    # Collected first, applied LAST-to-FIRST so earlier edits cannot shift the
    # indices of later ones.
    edits: list[tuple[int, int, list[tuple[str, str]]]] = []
    for start, title, end in _section_bounds(rows):
        body = incoming.get(title.strip().lower())
        if body is None:
            continue
        open_at = close_at = None
        for index in range(start + 1, end):
            if flags[index]:
                continue
            line = rows[index][0]
            if open_at is None:
                if _XSPEC_OPEN.search(line):
                    open_at = index
                continue
            if _XSPEC_CLOSE.search(line):
                close_at = index
                break
        if open_at is None or close_at is None:
            continue
        # The DESTINATION's flavor, never the proposal's. These lines are being
        # written into the fragment, so carrying the proposal's endings across
        # would make a CRLF fragment sprout LF lines in the middle — the
        # mixed-ending outcome the byte-preserving rule exists to prevent.
        replacement = [(text, eol) for text, _ending in body]
        edits.append((open_at + 1, close_at, replacement))

    out = list(rows)
    for begin, finish, replacement in reversed(edits):
        out[begin:finish] = replacement
    return join_rows(out)


def refresh_fragment(
    fragment_text: str, *, proposal_text: str | None, provenance: dict[str, str],
) -> str:
    """The whole refresh: provenance slots, then the marked sections.

    Slots first, deliberately: the slot fill may INSERT a section, and doing that
    after the section refresh would mean the section-index walk had run against a
    document the slot fill then moved.
    """
    filled = fill_provenance_slots(fragment_text, provenance)
    if not proposal_text:
        return filled
    return refresh_marked_sections(filled, proposal_text)
