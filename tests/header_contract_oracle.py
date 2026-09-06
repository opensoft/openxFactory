"""The header-completeness answer this repository gave BEFORE § 2.3, frozen.

`split-opendox-two-layer-product` § 2.3 moved the ideation header contract from
a constant in `ideation_dashboard.authoring` to a `classify` RESPONSE from
openxFactory's own corpus adapter. Every parity that guards that move needs
something to measure against, and the one thing it must NOT measure against is
either side of the move: comparing `authoring.missing_required_headers` to
`classify` after the migration compares a function to itself, and a green
tautology is how a behaviour change gets shipped as a refactor.

So the pre-migration algorithm lives here, verbatim, with its own copy of the
field block and its own window. It is an ORACLE, not a second authority:

  * It is deliberately NOT derived. Importing `corpus.STATUS_SCAN_LINES` or the
    adapter's `HEADER_FIELDS` would make it follow a change in the thing it is
    supposed to detect a change in, which is the whole failure mode of a
    co-authoritative constant read backwards.
  * The ONE thing it does import is `doc_health.lines.split_keepends`, the
    shared real-line rule. That rule was settled by
    `align-status-reader-to-real-lines` and § 2.3 does not touch it; a private
    copy here would be an eleventh spelling of "what is a line", which is the
    exact defect that ruling exists to have ended.
  * If the contract legitimately changes, this file changes in the same commit
    and the parities re-measure against the new answer — deliberately, visibly,
    and with the diff naming both halves.

Two suites read it: `tests/ideation-dashboard/test_authoring_classify_derivation.py`
(the create gate's answer over the whole governed corpus) and
`tests/corpus-adapter/test_openxfactory_adapter.py` (the adapter's own
`classify` over a sample of it). One oracle, because hand-copying it into both
would reintroduce, inside the tests, the pattern the change removes from the
code. `tests/import_scan.py` and `tests/hermeticity.py` are the precedent for a
helper module at the `tests/` root; both consumers reach it with the
`sys.path` insert their own header already carries.
"""

from __future__ import annotations

from doc_health.lines import split_keepends

#: The six field names `ideation_dashboard.authoring` authored until § 2.3, in
#: the order it authored them (openxFactory `ideation/README.md`, "Ideation
#: Header Format").
FIELDS: tuple[str, ...] = (
    "Status", "Kind", "Summary", "Topics", "Repository context", "Captured",
)

#: The window that module scanned, which was `doc_health.corpus
#: .STATUS_SCAN_LINES` — the other half of the pair § 2.3 collapses. Frozen at
#: the value it held.
SCAN_LINES = 15


def missing_required_headers(text: str) -> list[str]:
    """The body `authoring.missing_required_headers` carried before § 2.3.

    Unchanged from the landed implementation apart from reading this module's
    frozen field block and window instead of the two constants it read: a
    header line whose value is empty after stripping is not a carried header,
    and the window is the first `SCAN_LINES` REAL lines.
    """
    present: set[str] = set()
    for body, _ending in split_keepends(text)[:SCAN_LINES]:
        for field in FIELDS:
            prefix = field + ":"
            if body.startswith(prefix) and body[len(prefix):].strip():
                present.add(field)
    return [field for field in FIELDS if field not in present]
