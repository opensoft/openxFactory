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

THE LINE RULE IS SHARED, NOT REIMPLEMENTED PER READER. This is the corpus's
fourth attempt at "what is a line" (after `doc_health.families`,
`web/views/outline-model.js`, and the private copy `round_trip.py` used to
carry) — a dedicated, named home is how a fifth implementation gets prevented
instead of discovered. `ideation_dashboard.round_trip` imports this module
rather than defining its own copy; `doc_health.corpus.parse_status` and
`parse_kind` scan through it directly. The JavaScript side
(`web/views/outline-model.js`) cannot import a Python module, so it remains a
separate implementation of the fence/line rules — that divergence is not
fixable here and is held by an explicit three-way agreement test instead of by
convention (see `tests/ideation-dashboard/test_round_trip.py`).
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
