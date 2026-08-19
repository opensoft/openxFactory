"""align-status-reader-to-real-lines: the reader counts real lines.

`corpus.parse_status` / `parse_kind` used to scan
`text.splitlines()[:STATUS_SCAN_LINES]`, which also breaks on `\\x0b`, `\\x0c`,
`\\x1c`-`\\x1e`, `\\x85`, U+2028 and U+2029 — the same blindness
`align-demote-to-round-trip-rule` closed on the WRITER side
(`ideation_dashboard.gate_console._flip_status`, see
`tests/ideation-dashboard/test_gate_console.py`'s "review F1" section). A
header carrying one of those characters can inflate the pseudo-line count
past a `Status:` line that is plainly there within the real 15-line window,
producing a FALSE FINDING: a correct document reported as lacking a status it
carries. These tests pin the fix from both sides — the false-finding shape
itself (4.1), the window-counting rule that closes it (4.2), the same
coverage for `parse_kind` (4.3), and the shared primitive's lossless
round-trip travelling to its new home (4.4).
"""

from __future__ import annotations

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import corpus
from doc_health.lines import join_rows, split_keepends

# ---- 4.1: the false-finding shape this change exists to fix ------------------


def test_a_u2028_bearing_header_parses_status_and_is_not_reported_missing():
    """The spec's own scenario ("A header carrying an exotic separator is
    read"): a header region containing characters a wider splitting rule
    would treat as line breaks must still yield the status that is plainly
    there, in real lines."""
    noise = chr(0x2028).join(["filler"] * 20)  # one REAL line, 20 embedded U+2028s
    text = f"# Doc\n\n{noise}\nStatus: staged\n"
    # Sanity: the separator really does inflate str.splitlines() past the
    # window the OLD implementation scanned — otherwise this fixture pins
    # nothing.
    assert len(text.splitlines()) > corpus.STATUS_SCAN_LINES
    assert corpus.parse_status(text) == "staged"


def test_a_u2028_bearing_header_parses_kind_and_is_not_reported_missing():
    """4.3: `parse_kind` gets the same false-finding coverage as
    `parse_status`, since it shared the exact same blindness before this
    change (task 2.2)."""
    noise = chr(0x2028).join(["filler"] * 20)
    text = f"# Doc\n\n{noise}\nKind: policy\n"
    assert len(text.splitlines()) > corpus.STATUS_SCAN_LINES
    assert corpus.parse_kind(text) == "policy"


# ---- 4.2: the window counts real lines, measured both ways -------------------

_EXOTIC_SEPARATORS = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)


def _exotic_noise() -> str:
    """One REAL line littered with every exotic pseudo-line separator, twice
    over, so the pseudo-split of this single line already overruns the
    header window on its own."""
    return "".join(f"seg{i}{c}" for i, c in enumerate(_EXOTIC_SEPARATORS * 2))


def test_the_header_window_counts_real_lines_not_pseudo_line_fragments():
    """The spec's own scenario ("The header window is counted"): construct a
    document whose PSEUDO-line count (`str.splitlines()`) exceeds
    `STATUS_SCAN_LINES` while its REAL-line count (CR/LF/CRLF only) does not,
    and show the `Status:` header within the real window is still found."""
    text = f"# Title\n\n{_exotic_noise()}tail\nStatus: staged\n"
    real_line_count = len(split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the real-line count must fit the window"
    assert pseudo_line_count > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the pseudo-line count must overrun the window"
    assert corpus.parse_status(text) == "staged"


def test_the_kind_header_window_also_counts_real_lines():
    """4.3 again, for the window-counting shape rather than the U+2028
    shape."""
    text = f"# Title\n\n{_exotic_noise()}tail\nKind: policy\n"
    real_line_count = len(split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= corpus.STATUS_SCAN_LINES
    assert pseudo_line_count > corpus.STATUS_SCAN_LINES
    assert corpus.parse_kind(text) == "policy"


def test_a_status_genuinely_past_the_real_window_is_still_not_found():
    """The window is real, not removed. Not in scope (`proposal.md`):
    widening `STATUS_SCAN_LINES` itself or what a valid status value is —
    this only asserts the bound still bounds, counted correctly."""
    filler = "".join(f"line{i}\n" for i in range(corpus.STATUS_SCAN_LINES + 2))
    text = filler + "Status: staged\n"
    assert corpus.parse_status(text) is None


# ---- the reader and the writer are compared -----------------------------------


def test_the_reader_finds_what_the_writer_just_wrote_through_an_exotic_header():
    """Spec scenario "The reader and the writer are compared": a lifecycle
    header WRITTEN by a governed action (`gate_console._flip_status`) and
    then READ by the deterministic pass (`corpus.parse_status`) must agree on
    where the document's lines begin and end.

    The same U+2028-bearing fixture
    `tests/ideation-dashboard/test_gate_console.py`'s
    `test_a_unicode_line_separator_in_the_header_does_not_hide_the_status`
    uses for the writer: before this change, the writer (already fixed by
    `align-demote-to-round-trip-rule`) found and flipped the real `Status:`
    line here while the reader (`corpus.parse_status`, unfixed until this
    change) would have scanned past it and reported the correct, just-written
    document as lacking a status entirely -- the exact false finding this
    change closes.

    Lazy import, matching this package's existing back-reference convention
    (`# lazy: house guard` in `ideation_readiness.py` / `derive_possibles.py`):
    `doc_health` reaches into `ideation_dashboard` only inside a function, never
    at module level.
    """
    from ideation_dashboard import gate_console as gc  # lazy: house guard

    header = "".join(f"Field{i}: v {chr(0x2028)}\n" for i in range(9))
    src = "# Staged: t\n" + header + "Status: draft\n\n## Why\n"
    assert len(src.splitlines(keepends=True)) > gc.HEADER_SCAN_LINES
    written = gc._flip_status(src, "staged")
    assert corpus.parse_status(written) == "staged"


# ---- 4.4: the join/split property travels with the primitive -----------------


@pytest.mark.parametrize("text", [
    "",
    "one line, no ending",
    "lf\nlf\n",
    "crlf\r\ncrlf\r\n",
    "cr\rcr\r",
    "mixed\r\nlf\ncr\rtail",
    "\n\n\n",
    "trailing\nno newline",
])
def test_split_and_join_are_exactly_inverse(text):
    """`join_rows(split_keepends(t)) == t` for every ending shape asserted on
    today in `tests/ideation-dashboard/test_round_trip.py` — the same shapes,
    now pinned at the primitive's new home (`doc_health.lines`) as well as at
    its writer call site. Every "these bytes survive" guarantee in both the
    reader and the writer rests on this identity."""
    assert join_rows(split_keepends(text)) == text


def test_the_split_does_not_break_on_exotic_line_boundaries():
    """`str.splitlines(keepends=True)` also breaks on `\\x0c`, `\\x85`,
    U+2028 and friends; this primitive's own split does not."""
    text = "a\x0cb\x85c d\n"
    assert len(text.splitlines(keepends=True)) > 1      # the stdlib would split
    assert [body for body, _ in split_keepends(text)] == ["a\x0cb\x85c d"]
    assert join_rows(split_keepends(text)) == text
