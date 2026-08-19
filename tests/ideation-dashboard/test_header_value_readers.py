"""align-status-reader-to-real-lines: coverage gap closed (focused re-verify,
item 2).

`ideation_dashboard.generator._header_value` and `ideation_dashboard
.authoring.missing_required_headers` were converted to
`doc_health.lines.split_keepends` in the wide-scope conversion, but carried
no dedicated test that would fail if EITHER conversion alone regressed — the
reviewer reverted BOTH of them (together with two doc_health readers)
simultaneously and nothing in the suite failed. This module closes that gap
for the ideation-dashboard package's two conversions with one shared
exotic-separator fixture, checked against both functions, so each one has a
test that fails when IT ALONE is reverted.
"""

from __future__ import annotations

from doc_health import corpus
from ideation_dashboard import authoring
from ideation_dashboard import generator


_EXOTIC = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)


def _exotic_header_fixture() -> str:
    """One REAL line littered with every exotic pseudo-line separator, twice
    over, ahead of a complete six-field ideation header — so the pseudo-line
    window overruns before reaching ANY of the six fields, while the
    real-line window (CR/LF/CRLF only) does not."""
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(_EXOTIC * 2))
    text = (
        "# Staged: x\n"
        f"{noise}tail\n"
        "Status: staged\n"
        "Kind: policy\n"
        "Summary: a summary\n"
        "Topics: x\n"
        "Repository context: none\n"
        "Captured: 2026-08-19\n"
    )
    real_line_count = len(corpus.split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the real-line count must fit the window"
    assert pseudo_line_count > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the pseudo-line count must overrun the window"
    return text


def test_generator_header_value_finds_status_inside_the_real_window():
    text = _exotic_header_fixture()
    assert generator._header_value(text, "Status") == "staged"


def test_authoring_missing_required_headers_reports_none_missing():
    text = _exotic_header_fixture()
    assert authoring.missing_required_headers(text) == []


def test_mutation_reverting_generator_header_value_alone_reproduces_the_miss():
    """MUTATION CHECK: reverting `generator._header_value` alone to
    `str.splitlines()[:N]` must miss `Status:` on this fixture, proving the
    test above is pinned to THAT conversion specifically."""
    text = _exotic_header_fixture()

    def _reverted(text, name):
        prefix = name + ":"
        for line in text.splitlines()[:generator.HEADER_SCAN_LINES]:
            if line.startswith(prefix):
                return line[len(prefix):].strip() or None
        return None

    original = generator._header_value
    generator._header_value = _reverted
    try:
        result = generator._header_value(text, "Status")
    finally:
        generator._header_value = original

    assert result is None, (
        "reverting generator._header_value to splitlines() still found "
        "Status: — the fixture does not exercise this conversion")


def test_mutation_reverting_missing_required_headers_alone_reproduces_the_miss():
    """MUTATION CHECK, the `authoring` half: reverted alone, the SAME
    fixture must report every field missing, independently of
    `generator`'s own conversion (which stays fixed throughout this
    check)."""
    text = _exotic_header_fixture()

    def _reverted(text):
        lines = text.splitlines()[:corpus.STATUS_SCAN_LINES]
        present: set[str] = set()
        for line in lines:
            for field in authoring.REQUIRED_HEADER_FIELDS:
                prefix = field + ":"
                if line.startswith(prefix) and line[len(prefix):].strip():
                    present.add(field)
        return [f for f in authoring.REQUIRED_HEADER_FIELDS if f not in present]

    original = authoring.missing_required_headers
    authoring.missing_required_headers = _reverted
    try:
        result = authoring.missing_required_headers(text)
    finally:
        authoring.missing_required_headers = original

    assert result == list(authoring.REQUIRED_HEADER_FIELDS), (
        "reverting missing_required_headers to splitlines() did not report "
        "every field missing — the fixture does not exercise this conversion")
