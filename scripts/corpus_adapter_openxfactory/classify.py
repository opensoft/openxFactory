"""Kind detection and the required-field answer, driven entirely by shape data.

WHY THIS IS NOT A NINTH HEADER READER. This repository has paid for header
readers that disagreed with each other: `align-status-reader-to-real-lines`
found ten Python spellings of "what is a line" over the same header window, and
the damage was FALSE FINDINGS — a correct document reported as lacking a header
it plainly carried. So the two readers here are faithful mirrors of the two the
corpus already trusts, they scan through the shared real-line rule
(`doc_health.lines.split_keepends`, CR/LF/CRLF only, never
`str.splitlines()`), and `tests/corpus-adapter/test_openxfactory_adapter.py`
pins each against its original over a sample of the real corpus. A divergence
fails closed rather than being discovered as a wrong answer.

THE TWO RULES DIFFER BY ONE SPACE, AND THAT IS FAITHFUL, NOT SLOPPY.
`doc_health.corpus.parse_kind` matches `"<field>: "` — WITH the trailing space —
while `ideation_dashboard.authoring.missing_required_headers` matches
`"<field>:"` and then requires a non-empty stripped value. A document written
with no space after the colon is therefore kind-less to the first reader and
field-complete to the second. That divergence is the CORPUS's, it predates this
module, and mirroring it is what makes both parity tests pass; collapsing it
here would silently move an answer the corpus's own tooling gives. If it is ever
repaired, it is repaired at the source and both mirrors follow.

RULING OQ-2 (2026-09-06, NO) BOUNDS THIS OPERATION. Classify answers KIND and
REQUIRED FIELDS — nothing else. The corpus carries two further classification
vocabularies over the same documents (`doc_health.pin_class`'s three axes, and
`doc_health.inventory.artifact_type_for`), and they stay checker internals,
never exposed through the adapter. Exposing them would create exactly what the
seam's fourth requirement forbids: an operation available to the home adapter
that a domain implementation cannot also declare.
"""

from __future__ import annotations

import sys
from pathlib import Path

from doc_health.lines import split_keepends

# #872 (RULED OQ-Q): pinned openDox copy, not the local replica — see
# `adapter.py`'s header for the reach and the manifest reason it stays in tree.
_OPENDOX_SRC = Path(__file__).resolve().parents[2] / "openDox" / "code" / "src"
if not (_OPENDOX_SRC / "opendox" / "corpus_adapter.py").is_file():
    raise ImportError(
        "corpus_adapter_openxfactory.classify: the pinned openDox corpus-adapter "
        f"interface is not at {_OPENDOX_SRC / 'opendox' / 'corpus_adapter.py'}. "
        "Run `git submodule update --init --recursive openDox` from the "
        "repository root.")
sys.path.insert(0, str(_OPENDOX_SRC))

from opendox.corpus_adapter import Classification, DocumentId

from .shape import CorpusShape


def _header_window(text: str, scan_lines: int) -> list[str]:
    """The first `scan_lines` REAL lines' bodies.

    Real lines, not `str.splitlines()` fragments: an exotic separator inside a
    header inflates the fragment count past the window and hides a header that
    is plainly there.
    """
    return [body for body, _ending in split_keepends(text)[:scan_lines]]


def kind_of(text: str, shape: CorpusShape) -> str | None:
    """The document's declared kind, or None where it carries none.

    Faithful mirror of `doc_health.corpus.parse_kind`, including the trailing
    space in the prefix and the strip-to-None on an empty value.
    """
    if not shape.kind_field:
        return None
    prefix = shape.kind_field + ": "
    for body in _header_window(text, shape.header_scan_lines):
        if body.startswith(prefix):
            return body[len(prefix):].strip() or None
    return None


def obliged_fields(document_key: str, kind: str | None,
                   shape: CorpusShape) -> tuple[str, ...]:
    """Which fields this document's kind obliges, here.

    Outside every declared obliged prefix the answer is `()` — this corpus
    carries no field contract over that part of itself, and reporting one would
    be a false finding rather than a strict one.
    """
    if shape.obliged_prefixes and not any(
            document_key.startswith(prefix) for prefix in shape.obliged_prefixes):
        return ()
    table = shape.required_fields_by_kind or {}
    if kind in table:
        return tuple(table[kind])
    return tuple(table.get(None, ()))


def absent_fields(text: str, fields: tuple[str, ...],
                  shape: CorpusShape) -> tuple[str, ...]:
    """Of `fields`, the ones this document does not carry a value for.

    Faithful mirror of `ideation_dashboard.authoring.missing_required_headers`:
    the prefix carries NO trailing space and the value must be non-empty after
    stripping, so a header line with no value is not a carried header.
    """
    window = _header_window(text, shape.header_scan_lines)
    present: set[str] = set()
    for body in window:
        for field in fields:
            prefix = field + ":"
            if body.startswith(prefix) and body[len(prefix):].strip():
                present.add(field)
    return tuple(field for field in fields if field not in present)


def classify_text(document: DocumentId, text: str,
                  shape: CorpusShape) -> Classification:
    """The whole operation: kind, obligation, absence, and — when the kind is
    absent — a named reason.

    NEVER OMITS. An unrecognized document comes back with `kind=None` and an
    `unclassifiable` reason that names it, and the caller's listing still holds
    it. That asymmetry is the interface's own: an unresolvable CORPUS refuses; an
    unrecognizable DOCUMENT is reported.
    """
    kind = kind_of(text, shape)
    required = obliged_fields(document.key, kind, shape)
    missing = absent_fields(text, required, shape)
    unclassifiable = None
    if kind is None and shape.kind_field:
        unclassifiable = (
            f"{document.key} carries no {shape.kind_field} header value, so its "
            f"declared shape is not recognizable to this reader")
    return Classification(id=document, kind=kind, required_fields=required,
                          missing_fields=missing, unclassifiable=unclassifiable)
