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

THE LINE RULE IS SHARED, NOT REIMPLEMENTED PER READER — EVERY READER OF A
LIFECYCLE HEADER, not just `corpus.parse_status`/`parse_kind`. Before this
module existed (and, for most of these, before this change's wide ruling),
the corpus carried FOUR separate Python spellings of "what is a line": the
private copy `round_trip.py` used to define; `doc_health.families`'s own
unbounded `text.splitlines()` scan (`_scan_lines`); the `text.splitlines()
[:N]` window idiom independently repeated in `corpus.parse_status`/
`parse_kind`, `doc_health.families._header_line`,
`doc_health.inventory._header_value`,
`doc_health.organizer_dispatch._header_value`,
`ideation_dashboard.doxbench_status_exemption.lifecycle_status`,
`ideation_dashboard.authoring.missing_required_headers`,
`ideation_dashboard.generator._header_value`, and
`doc_health.ideation_readiness._parse_header`; and
`ideation_dashboard.completeness._Prepared.lines`, an assignment-then-slice
variant of the same window idiom that a grep for the literal idiom's two
tokens adjacent could not find (finding F4) — none of them agreeing with
each other, or with this module's rule, on CR/LF/CRLF-only lines. A further
sweep (finding F5, a second focused re-verify) found the SAME divergence
class reaching `_parse_header`'s standalone twin,
`scripts/bootstrap-ideation-cross-reference.py`'s `parse_header` — a
separate script, not a package, but able to import this module (verified,
not assumed) since both live directly under `scripts/`.

Brett's same-day ruling on `align-status-reader-to-real-lines` (in-session
multiple choice, recommended option adopted, 2026-08-19) converts ALL
readers of a lifecycle header: the delta's "SHALL hold for every reader of
that header" governs over the change's initially narrower `code_surface:`
enumeration, measured at zero baseline cost (1227 governed aggregation
files, zero exotic separators, zero window differences, zero value
changes). Every one of the readers named above now scans through THIS
module — verified true by a corrected, wider sweep (bare `splitlines()`
over document text, not just the `[:N]`-windowed idiom) each time a
narrower sweep pattern let one through, not asserted once and left stale.

NOT EVERY PYTHON LINE-SPLIT IN THIS CORPUS CONVERGED HERE, and this
docstring does not claim it did. Two further unbounded `text.splitlines()`
scanners share this rule's divergence class but are deliberately outside
this change's scope (recorded, with reasoning, in `tasks.md` §7): NEITHER
is a lifecycle-header reader, so the delta's every-*header*-reader clause
does not reach either, and the measured baseline carries no document where
either diverges from a real-line reading (0 of 1227 files).
`doc_health.families._template_gaps` scans `## `/`### Q` TEMPLATE headings
for conformance checking; `doc_health.ideation_routing._scan_lines`
(finding F6) is an unconverted byte-for-byte copy of
`families._scan_lines` as it existed BEFORE this change, scanning for
markdown provenance references and fence state.

So, for the NARROWER question of "where is a `##`/```` ``` ```` boundary"
(as opposed to "where is a lifecycle header", which this module answers
once, for everyone) — a question this module does not itself answer, since
it owns line-splitting, not heading or fence detection — the corpus holds
THREE Python rules (this module's, shared by `round_trip.py` and
`families._scan_lines`; `_template_gaps`'s own; `ideation_routing
._scan_lines`'s own) and, inside `web/views/outline-model.js`, TWO JS rules
(`outlineSections`'s LF-only `text.split("\n")` at outline-model.js:46;
`endsInsideFence`/`insertSection`'s real-line regex
`text.split(/\r\n|\r|\n/)` at outline-model.js:273/319 — finding F1). That
divergence, where it is exercised at all, is held by an explicit agreement
test rather than by convention (see
`tests/ideation-dashboard/test_round_trip.py`). The naive ``` fence-toggle
PREDICATE itself is a separate, narrower rule from any line-split (three
textually independent spellings — `round_trip.py`, `families.py`,
`outline-model.js` — pinned by that same test module's
`test_the_shared_predicate_is_spelled_the_same_in_all_three`) and is not
converted here: this module owns line-splitting, not fence detection.
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
