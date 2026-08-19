"""align-status-reader-to-real-lines: coverage gap closed (focused re-verify,
item 2).

`doc_health.inventory._header_value` and `doc_health.organizer_dispatch
._header_value` were converted to `doc_health.lines.split_keepends` in the
wide-scope conversion, but carried no dedicated test at all — the reviewer
reverted BOTH of them (together with two ideation_dashboard readers)
simultaneously and nothing in the suite failed. This module closes that gap
for the doc-health package's two conversions with one shared exotic-separator
fixture, checked against both functions, so each one has a test that fails
when IT ALONE is reverted.
"""

from __future__ import annotations

from doc_health import corpus
from doc_health import inventory
from doc_health import organizer_dispatch


_EXOTIC = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)


def _exotic_fixture() -> str:
    """One REAL line littered with every exotic pseudo-line separator, twice
    over, followed by the header line under test — so the pseudo-line
    window (`str.splitlines()[:N]`) overruns before ever reaching it, while
    the real-line window (CR/LF/CRLF only) does not."""
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(_EXOTIC * 2))
    text = f"# Doc\n\n{noise}tail\nHandling: internal-governance\n"
    real_line_count = len(corpus.split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the real-line count must fit the window"
    assert pseudo_line_count > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the pseudo-line count must overrun the window"
    return text


def test_inventory_header_value_finds_the_field_inside_the_real_window():
    text = _exotic_fixture()
    assert inventory._header_value(text, "Handling") == "internal-governance"


def test_organizer_dispatch_header_value_finds_the_field_inside_the_real_window():
    text = _exotic_fixture()
    assert organizer_dispatch._header_value(text, "Handling") == \
        "internal-governance"


def test_mutation_reverting_inventory_header_value_alone_reproduces_the_miss():
    """MUTATION CHECK: reverting `inventory._header_value` alone to
    `str.splitlines()[:N]` must miss the field on this fixture, proving the
    test above is pinned to THAT conversion specifically (not, say, to
    `organizer_dispatch`'s, or to the fixture being trivially findable
    regardless of which rule reads it)."""
    text = _exotic_fixture()

    def _reverted(text, name):
        prefix = f"{name}: "
        for line in text.splitlines()[:corpus.STATUS_SCAN_LINES]:
            if line.startswith(prefix):
                return line[len(prefix):].strip() or None
        return None

    original = inventory._header_value
    inventory._header_value = _reverted
    try:
        result = inventory._header_value(text, "Handling")
    finally:
        inventory._header_value = original

    assert result is None, (
        "reverting inventory._header_value to splitlines() still found the "
        "field — the fixture does not exercise this conversion")


def test_mutation_reverting_organizer_dispatch_header_value_alone_reproduces_the_miss():
    """MUTATION CHECK, the `organizer_dispatch` half: reverted alone, the
    SAME fixture must miss the field, independently of `inventory`'s own
    conversion (which stays fixed throughout this check)."""
    text = _exotic_fixture()

    def _reverted(text, name):
        prefix = f"{name}: "
        for line in text.splitlines()[:corpus.STATUS_SCAN_LINES]:
            if line.startswith(prefix):
                return line[len(prefix):].strip() or None
        return None

    original = organizer_dispatch._header_value
    organizer_dispatch._header_value = _reverted
    try:
        result = organizer_dispatch._header_value(text, "Handling")
    finally:
        organizer_dispatch._header_value = original

    assert result is None, (
        "reverting organizer_dispatch._header_value to splitlines() still "
        "found the field — the fixture does not exercise this conversion")
