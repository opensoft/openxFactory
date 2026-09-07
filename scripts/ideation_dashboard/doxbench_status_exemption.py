"""The `Status:`-header LIFECYCLE-EXEMPTION rail, carved out of the packet
assembler (`split-opendox-two-layer-product` § 2.4, OQ-1 as ruled).

WHAT THIS MODULE IS FOR, AND WHY IT IS NOT IN `doxbench_packet.py` ANY MORE.
`design.md` § D3 files the whole of `doxbench_packet.py` under the
openxFactory-adapter column, yet the packet assembler is the primitive
openDox's own chat-turn route calls — so moving the file wholesale would leave
openDox's kept-in-tree route depending on an openxFactory-only module, which is
the fork-vs-profile problem `domain-descendant-boundary` forbids one level down.
OQ-1 was ruled as recommended: the file splits along the same line it straddles.
Everything generic — confinement, selection, bounds, assembly, the packet type
itself — stays in `doxbench_packet.py` and travels with **openDox**. The four
constants and three functions below are the part that reads THIS corpus's
`Status:` header against THIS corpus's lifecycle vocabulary, so they are the
part that stays in the **openxFactory-adapter column** at the carve.

THE COLUMN ASSIGNMENT IS THE WHOLE POINT, AND IT IS WHY THE `doc_health`
IMPORT MOVED FILE RATHER THAN TARGET. `doxbench_packet.py` no longer imports
`doc_health` at all — a neutrality scan asserts it, the same way
`tests/corpus-adapter/test_no_privileged_route.py` asserts it of
`scripts/corpus_adapter.py` — and the import that used to sit there sits here
instead, on the openxFactory side of the line where a `doc_health` dependency
is unremarkable.

WHY IT STILL IMPORTS `doc_health` DIRECTLY RATHER THAN ASKING `classify()`,
RECORDED BECAUSE THE RULING'S PREFERRED ROUTE TURNED OUT NOT TO EXIST. OQ-1's
recommendation was that this rail reach what it needs through the corpus
adapter's already-landed `classify()` operation. It cannot, for two independent
reasons, and neither is repairable inside § 2.4:

  1. `corpus_adapter.Classification` carries `kind`, `required_fields`,
     `missing_fields` and `unclassifiable`. It never carries a status VALUE, and
     this rail needs the value — `PacketSource.status` is rendered verbatim into
     the packet's own evidence sections, and the exemption is keyed on the
     leading status WORD. `classify()` can say only whether a `Status` header is
     PRESENT. Carrying the value would mean a new `Classification` field, which
     is exactly what RULING OQ-2 (2026-09-06, NO) already refused in
     `corpus_adapter_openxfactory/classify.py`: "Classify answers KIND and
     REQUIRED FIELDS — nothing else." The `OPERATIONS` tuple is closed and
     `tests/corpus-adapter/test_interface_closure.py` guards it.
  2. `classify(corpus, document)` answers about a document a corpus HOLDS. This
     rail runs over `PacketSource.text` — in-memory strings from the retrieval
     provider, once per evidence item per chat turn. The only in-tree way to
     classify a loose body is `authoring._classify_proposal`'s corpus-of-one,
     which stages the body in a temporary directory and resolves it; that is a
     filesystem round trip per evidence item per turn, and the assembler's own
     negative-space test fails the build on any filesystem or process spelling
     appearing in it at all.

So the split lands as § 2.4's task text directs when the `classify()` route is
unavailable: the rail moves COLUMN, keeping its direct `doc_health` import, and
the gap is reported rather than closed by extending a closed Protocol.

PURE, STDLIB PLUS ONE SHARED PRIMITIVE, AND NO I/O — the same property the
assembler it came from declares, so nothing about the packet pipeline's "the
rails run before any provider is reached" claim changes by this move.
"""

from __future__ import annotations

import re

from doc_health.lines import split_keepends

# ---------------------------------------------------------------------------
# the lifecycle-status read (task 10.3) — the assembler's own, never delegated
# ---------------------------------------------------------------------------

# The SAME rule the repository's doc-health corpus reader uses: a `Status:`
# line inside the document's own header block, found by scanning the SAME
# shared real-line primitive corpus.parse_status scans through
# (`doc_health.lines.split_keepends` — CR/LF/CRLF only, so an exotic
# separator cannot inflate this window past a line that is plainly there).
# The window/regex/loop are still spelled out here rather than calling
# `corpus.parse_status` itself, because the exemption is the ASSEMBLER'S to
# apply and this is the read it applies it from; a companion test asserts
# the two readers agree, including on a synthetic exotic-separator fixture
# rather than real corpus documents alone (the corpus carries none today —
# measured zero across 1227 governed aggregation files — so an agreement
# check limited to it would pass vacuously).
_STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$")
STATUS_SCAN_LINES = 15

# The statuses whose content is EXEMPT from aggressive compression.
#
# The delta names "approved or ratified". This repository's own lifecycle
# vocabulary spells the approved end `ratified` (a change has ratified it) and
# `standard` (it has been promoted to canon), and the source-ranking hierarchy
# this same change ratified ranks "ratified or standard canon" TOGETHER at the
# top. Exempting `ratified` while compressing `standard` would therefore
# compress the most authoritative material this surface has, which is the
# opposite of what the exemption is for.
#
# `approved` is FOREIGN-CORPUS TOLERANCE, not a fourth local status: the delta
# names it, this repository's lifecycle vocabulary does not contain it, and a
# corpus-wide grep finds ZERO documents carrying it. It is honoured so a corpus
# that does use the word is not silently compressed, and it is recorded here as
# tolerance so no reader mistakes it for a status this repository issues.
EXEMPT_STATUSES: frozenset[str] = frozenset({"approved", "ratified", "standard"})

# A `Status:` value may carry a DECORATION after the status word — this corpus
# already holds `record · 2026-08-01T01:21Z (session of …)` and
# `record (in progress — …)` — so the exemption reads the leading status WORD
# and ignores what follows. Without this, a decorated `Status: ratified (…)`
# would silently lose its exemption, which is the exact failure this rail
# exists to prevent. `lifecycle_status` still returns the RAW value, so it goes
# on agreeing byte for byte with the repository's own corpus reader.
_STATUS_DECORATORS = "(·|,"


def lifecycle_status(text: str) -> str | None:
    """The document's own declared `Status:`, or None when it declares none."""
    if not isinstance(text, str):
        return None
    for body, _ending in split_keepends(text)[:STATUS_SCAN_LINES]:
        match = _STATUS_RE.match(body)
        if match:
            return match.group(1)
    return None


def status_word(status: str | None) -> str | None:
    """The leading status WORD of a possibly-decorated `Status:` value."""
    if status is None:
        return None
    value = status.strip().lower()
    for decorator in _STATUS_DECORATORS:
        value = value.split(decorator, 1)[0]
    parts = value.split()
    return parts[0] if parts else None


def is_compression_exempt(text: str) -> bool:
    """Whether this content is exempt from aggressive compression, read from
    its OWN lifecycle status header."""
    return status_word(lifecycle_status(text)) in EXEMPT_STATUSES
