"""align-status-reader-to-real-lines, WIDE ruling (2026-08-19): `families.py`
converts too.

Adversarial-review finding C1, reproduced: `corpus.parse_status` already
counted real lines, but `families._header_line` still scanned
`text.splitlines()[:STATUS_SCAN_LINES]` — the SAME window constant, a
DIFFERENT rule. A ratified document whose header carries an exotic
line-boundary character (here, one real line littered with several) could get
`status == "ratified"` from `corpus` (correct) and then a false CRITICAL
`ratified-provenance` finding from `families` ("Ratified by: missing") even
though the real `Ratified by:` line sits plainly inside the real 15-line
window — it was only pushed past the OLD pseudo-line window. That is the
exact false-finding shape `align-status-reader-to-real-lines` exists to
close, now closed for `families` as well as `corpus`.

This module builds its `Context`/`Doc` directly rather than through
`conftest.make_ctx`'s fixture-directory mechanism: the defect is about exact
line-boundary placement, which is far more precisely controlled as a literal
string than as a checked-in fixture file.
"""

from __future__ import annotations

from datetime import date

from doc_health import CRITICAL
from doc_health import corpus
from doc_health.corpus import Doc
from doc_health.families import _header_line, fam_ratified_provenance
from doc_health.runner import Context

# The same exotic-separator alphabet the shared primitive's own tests use
# (CR/LF/CRLF are real lines; everything else here is not).
_EXOTIC_SEPARATORS = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)


def _exotic_noise() -> str:
    """One REAL line littered with every exotic pseudo-line separator, twice
    over — the pseudo-split of this single line already overruns
    `corpus.STATUS_SCAN_LINES` (15) on its own."""
    return "".join(f"seg{i}{c}" for i, c in enumerate(_EXOTIC_SEPARATORS * 2))


def _ratified_doc_with_exotic_header() -> Doc:
    text = (
        "# Ratified: a topic\n\n"
        "Status: ratified\n\n"
        f"{_exotic_noise()}tail\n"
        "Ratified by: fix-c1-demo\n\n"
        "## Why\n"
    )
    # Sanity: the fixture actually demonstrates the shape it claims to.
    real_line_count = len(corpus.split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= corpus.STATUS_SCAN_LINES, \
        "fixture is broken: Ratified by: must sit inside the REAL window"
    assert pseudo_line_count > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the pseudo-line count must overrun the window"
    return Doc("openxFactory", "docs/exotic-ratified.md", text,
               corpus.parse_status(text), corpus.parse_kind(text))


def _ctx(doc: Doc) -> Context:
    return Context(
        repo_paths={}, docs=[doc], capabilities={},
        change_ids={"openxFactory": {"fix-c1-demo"}},
        git=None, thresholds={}, as_of=date(2026, 8, 19), agg_root=None)


def test_the_fixture_status_is_ratified_through_the_real_line_reader():
    """Sanity check on the fixture itself: `corpus.parse_status` (already
    fixed) must read `ratified` here, or this fixture is not the C1 shape."""
    doc = _ratified_doc_with_exotic_header()
    assert doc.status == "ratified"


def test_header_line_finds_ratified_by_within_the_real_window():
    """`_header_line` directly: the real-line reader finds `Ratified by:`
    even though the OLD pseudo-line reader would have scanned past it."""
    doc = _ratified_doc_with_exotic_header()
    line = _header_line(doc, "Ratified by:")
    assert line == "Ratified by: fix-c1-demo"


def test_a_ratified_document_with_an_exotic_header_is_not_falsely_flagged():
    """C1's end-to-end shape: `fam_ratified_provenance` must NOT report this
    document, because its `Ratified by:` line is plainly there in real
    lines and resolves to a real change id."""
    doc = _ratified_doc_with_exotic_header()
    findings = fam_ratified_provenance(_ctx(doc))
    assert findings == [], (
        "false ratified-provenance finding on a document whose header "
        "plainly carries Ratified by: inside the real 15-line window")


def test_mutation_reverting_header_line_alone_reproduces_the_false_finding():
    """MUTATION CHECK (tasks.md 4.7): reverting `_header_line` alone to the
    pre-fix `str.splitlines()[:N]` idiom, with EVERYTHING ELSE (including
    `corpus.parse_status`) left as this change fixed it, must reproduce
    exactly the false CRITICAL finding C1 demonstrated — proving the tests
    above actually exercise the defect this change closes, not some other
    accident of the fixture.
    """
    doc = _ratified_doc_with_exotic_header()
    assert doc.status == "ratified"  # corpus's real-line fix still applies

    def _reverted_header_line(doc, prefix):
        for line in doc.text.splitlines()[:corpus.STATUS_SCAN_LINES]:
            if line.startswith(prefix):
                return line
        return None

    import doc_health.families as families_module
    original = families_module._header_line
    families_module._header_line = _reverted_header_line
    try:
        findings = fam_ratified_provenance(_ctx(doc))
    finally:
        families_module._header_line = original

    assert [(f.severity, f.family) for f in findings] == [
        (CRITICAL, "ratified-provenance")], (
        "reverting _header_line to splitlines() did not reproduce the false "
        "finding — the test above is not actually pinned to this defect")
