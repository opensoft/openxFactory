"""The shared line rule: what a line is in a governed document.

WHAT THIS EXISTS TO FIX. `str.splitlines(keepends=True)` breaks not only on the
three real line endings but also on `\\x0b`, `\\x0c`, `\\x1c`-`\\x1e`, `\\x85`,
U+2028 and U+2029. A governance document containing one of those would be
silently re-split and rejoined into different bytes by anything using it, and a
15-line header window counted that way is a window over fifteen FRAGMENTS of the
document rather than fifteen of its lines.

Two damages followed from that, both demonstrated against the writer this module
now serves (`ideation_dashboard.gate_console._flip_status`), before the fix moved
here:

* `Status: draft\\x0crest of the line` was seen as TWO pseudo-lines, so the first
  was replaced with no ending and the remainder was GLUED onto the new value:
  `Status: stagedrest of the line`. A line boundary the file does not contain was
  invented, and text moved across it.
* A header carrying U+2028s inflates the pseudo-line count past the header
  window, so a real `Status:` inside it is never found and a flip silently does
  nothing.

The same blindness reaches the READER side too:
`doc_health.corpus.parse_status` / `parse_kind` scanned
`text.splitlines()[:STATUS_SCAN_LINES]`, so a document whose header carries an
exotic separator can have a `Status:` line the writer wrote correctly but the
reader never sees — reporting a correct document as lacking a status it plainly
has. That is a FALSE FINDING, which costs more trust than a crash: it accuses a
correct document and leaves the operator no recourse but to disbelieve the
checker.

Only the three real line endings separate lines here: CR, LF, and CRLF. The
`join(split(t)) == t` identity is the property every "these bytes survive"
guarantee in this corpus is stated in terms of, and it is asserted in the tests
for exactly that reason — get it wrong and every caller's guarantee is void.

THE LINE RULE IS SHARED, NOT REIMPLEMENTED PER READER — EVERY PYTHON READER,
not just `corpus.parse_status`/`parse_kind`. Before this module existed (and,
for six of these, before this change's wide ruling), the corpus carried
FOUR separate Python spellings of "what is a line": the private copy
`round_trip.py` used to define; `doc_health.families`'s own unbounded
`text.splitlines()` scan (`_scan_lines`); and the `text.splitlines()[:N]`
window idiom independently repeated in `corpus.parse_status`/`parse_kind`,
`doc_health.families._header_line`, `doc_health.inventory._header_value`,
`doc_health.organizer_dispatch._header_value`,
`ideation_dashboard.doxbench_packet.lifecycle_status`,
`ideation_dashboard.authoring.missing_required_headers`, and
`ideation_dashboard.generator._header_value` — none of them agreeing with
each other, or with this module's rule, on CR/LF/CRLF-only lines.

Brett's same-day ruling on `align-status-reader-to-real-lines` (in-session
multiple choice, recommended option adopted, 2026-08-19) converts ALL of
them: the delta's "SHALL hold for every reader of that header" governs over
the change's initially narrower `code_surface:` enumeration, measured at zero
baseline cost (1227 governed aggregation files, zero exotic separators, zero
window differences, zero value changes). Every one of the readers named above
now scans through THIS module. `web/views/outline-model.js` cannot import a
Python module, so it remains the ONE separate implementation of this line
rule — that divergence is not fixable here and is held by an explicit
agreement test instead of by convention (see
`tests/ideation-dashboard/test_round_trip.py`). The naive ``` fence-toggle
PREDICATE itself is a separate, narrower rule from this one (three textually
independent spellings — `round_trip.py`, `families.py`, `outline-model.js` —
pinned by that same test module's `test_the_shared_predicate_is_spelled_the_same_in_all_three`)
and is not converted here: this module owns line-splitting, not fence
detection.
"""

from __future__ import annotations

import re

_EOL = re.compile(r"\r\n|\r|\n")


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
