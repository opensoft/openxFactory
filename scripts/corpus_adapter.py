"""The corpus-adapter interface: six operations a reader over a governed
document corpus declares, and nothing else (`split-opendox-two-layer-product`
§ 2.2, design § D2).

PROVENANCE, AND IT IS PROVISIONAL. RULING Q4 (`opensoft/openxFactory` issue
#656, 2026-09-04T15:34Z) gives the INTERFACE to openDox: the operation names,
their arguments and their return shapes are ratified in openDox's own
governance instance, not here. § 2.2 nonetheless lands them in-tree NOW,
because "a repository created before the interface exists has its boundary
drawn by whatever `git filter-repo` happened to move". Those two are
reconcilable only if what lands is provisional, so it says so in one machine-
readable place -- `INTERFACE_PROVENANCE` below, asserted by the conformance
suite (RULING OQ-1, 2026-09-06, YES). openxFactory authors the terms of
consumption; openDox authors the standard.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
The same rule design § D2 states for the write guard, and for the same two
futures: BOTH of this repository's reader packages will consume it (§ 2.3,
§ 2.4), and it travels to openDox with the carve, where the checker package
does not exist. It therefore imports NOTHING from either package -- stdlib and
`typing` only -- and that is a property a test asserts by parsing, not an
accident of the current body (`tests/corpus-adapter/test_no_privileged_route.py`).

WHY A `runtime_checkable` `Protocol` AND NOT AN ABC, recorded because nothing
in the governing packet fixes the construct and the choice is load-bearing:

  * An ABC forces `class X(CorpusAdapter)`. This interface travels to openDox
    and is pinned back as an external product, and the seam's first rule is
    that no neutral product openxFactory pins imports openxFactory's own
    tooling. STRUCTURAL conformance lets an implementation authored elsewhere
    conform without importing anything from this repository -- which is the
    property the seam exists for. Nominal conformance would make the seam
    exactly the dependency it was drawn to remove.
  * A module of plain functions has nowhere to carry per-corpus construction
    data, so a home layout would have to sit in module-level literals -- which
    is the privileged route the seam's fourth rule forbids.
  * House precedent: `doxbench_model.WorkbenchModelPort`, a
    closed-member `runtime_checkable` Protocol guarded by a companion test that
    reads `__protocol_attrs__` so the surface cannot grow a verb by accident.
    `intent_compliance.allowance_resolution.AllowanceIndex` is the smaller
    sibling.

CLOSED MEMBERSHIP, AND ALL SIX MEMBERS ARE METHODS. `runtime_checkable`
protocols with non-method members support `isinstance()` but not
`issubclass()`, so every member here is a method, the conformance suite uses
`isinstance` only, and `OPERATIONS` is the closure the companion test reads
`__protocol_attrs__` against. A seventh member is a seam that leaks.

TWO FAILURE MODES, DELIBERATELY DIFFERENT, AND THIS IS THE ONE PLACE A READER
GOES WRONG. An unresolvable CORPUS refuses -- `CorpusRefused`, naming what it
could not resolve -- and never degrades to an empty result, a partial listing
or a skip; an empty corpus is a legal `()` and must stay distinguishable from
an unreadable one, because a projection built over the first is correct and a
projection over the second is a lie with a timestamp. An unrecognizable
DOCUMENT does the opposite: it is REPORTED, as a `Classification` carrying
`kind=None` and a named `unclassifiable` reason, and it stays in the listing.
Corpus -> refusal; document -> report.

WRITE-BACK IS A DISPATCH, NOT A WRITE. `write_back` hands a proposed document
body to the corpus's DECLARED governed write path and returns that path's
correlation identifier. It never touches the corpus tree -- an implementation
that does is refused even where the bytes would be identical, because the gate
is the act of passing through the path and not the shape of the result. A
corpus with no declared path is read-only, and `resolve` says so at resolution
time rather than letting the first write discover it.

NO REFUSALS LEDGER. The write guard keeps one because its refusals happen
inside batch writes and are otherwise invisible; an adapter call refuses ONE
call to a caller already holding it, and a public `refusals` attribute would
be surface the closure test then has to carve an exception for.

NO HOME VOCABULARY LIVES IN THIS FILE (RULING C2, 2026-09-04T17:47Z). Neither
the home corpus's header words nor its governance nouns appear here, in a
literal or in prose, and a test enforces it over the whole source text: a
clinician using a descendant of this interface must never meet an engineering
noun that arrived by way of the reader.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

#: RULING OQ-1 (2026-09-06, YES). Machine-readable, asserted by the
#: conformance suite, so the marker cannot be dropped silently when openDox
#: ratifies for real.
INTERFACE_PROVENANCE = (
    "provisional -- openDox's own governance instance ratifies these "
    "signatures (RULING Q4, opensoft/openxFactory#656); openxFactory authors "
    "the terms of consumption only"
)

#: The closed operation set. The companion test reads
#: `CorpusAdapter.__protocol_attrs__` against this tuple, so growing the
#: surface is a two-file act somebody has to mean.
OPERATIONS: tuple[str, ...] = (
    "resolve", "list_documents", "read", "classify", "check", "write_back",
)

#: Design § D2 names the four operations `list` / `read` / `write back` /
#: `check` and the two derived ones `classify` / `resolve`. `list` is a
#: builtin, hence `list_documents`; the mapping is DECLARED here rather than
#: left to be inferred, so a reader of the design table can find each row.
DESIGN_NAMES: dict[str, str] = {
    "resolve": "resolve",
    "list_documents": "list",
    "read": "read",
    "classify": "classify",
    "check": "check",
    "write_back": "write back",
}

#: The one scope name every implementation SHALL accept. An implementation may
#: declare further scope names; it announces them through
#: `ResolvedCorpus.scopes` rather than through a seventh operation.
SCOPE_ALL = "all"

#: Ordered, most severe first. Deliberately a small fixed vocabulary: a
#: consumer that cannot rank two findings cannot decide anything with them.
SEVERITIES: tuple[str, ...] = ("critical", "error", "warning", "info")

# --------------------------------------------------------------------------
# refusal kinds -- stable strings for reports, tests and any eventual surface
# --------------------------------------------------------------------------

CORPUS_ABSENT = "corpus-absent"                    #: the checkout is not there
CORPUS_UNREADABLE = "corpus-unreadable"            #: it is there and cannot be read
CORPUS_UNCLASSIFIABLE = "corpus-unclassifiable"    #: the CORPUS's shape, not a document's
REVISION_UNKNOWN = "revision-unknown"              #: a revision this reader cannot serve
SCOPE_UNKNOWN = "scope-unknown"                    #: a scope name this corpus does not declare
DOCUMENT_UNKNOWN = "document-unknown"              #: no such document identity here
CORPUS_READ_ONLY = "corpus-read-only"              #: no declared governed write path
WRITE_PATH_UNREACHABLE = "write-path-unreachable"  #: declared, and it cannot be reached

REFUSAL_KINDS: tuple[str, ...] = (
    CORPUS_ABSENT,
    CORPUS_UNREADABLE,
    CORPUS_UNCLASSIFIABLE,
    REVISION_UNKNOWN,
    SCOPE_UNKNOWN,
    DOCUMENT_UNKNOWN,
    CORPUS_READ_ONLY,
    WRITE_PATH_UNREACHABLE,
)


@dataclass(frozen=True)
class Refusal:
    """WHY an operation could not be performed, with WHAT it was about.

    `subject` is never optional and never generic: the failure this whole
    class exists to end is a reader that was pointed at the wrong tree and
    said nothing useful about which tree.
    """

    kind: str      #: one of REFUSAL_KINDS
    subject: str   #: what could not be resolved -- named, always
    detail: str    #: the human-readable why

    def report(self) -> str:
        return f"corpus refused {self.kind}: subject={self.subject!r} -- {self.detail}"


class CorpusRefused(Exception):
    """A refused adapter operation, carrying the structured `Refusal`.

    One exception for the whole interface. A consumer branches on
    `err.refusal.kind`, which is a stable string, rather than on an exception
    hierarchy that would have to travel across the seam intact.
    """

    def __init__(self, refusal: Refusal) -> None:
        self.refusal = refusal
        super().__init__(refusal.report())


# --------------------------------------------------------------------------
# plain data -- every type below is frozen, and none of it knows a home
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CorpusRef:
    """The caller's REQUEST for a corpus, before anything has been resolved."""

    name: str                    #: the caller's name for this corpus
    location: str                #: opaque here; the implementation interprets it
    revision: str | None = None  #: None means "whatever the location currently is"


@dataclass(frozen=True)
class ResolvedCorpus:
    """A corpus an implementation has actually found, and its terms.

    `scopes` rides here as RETURN DATA rather than as a seventh operation --
    the surface stays six wide, and a caller that has resolved a corpus
    already holds everything it needs to list it.

    `write_path` / `write_path_available` are answered HERE, at resolution
    time, not at the first write: a read-only corpus is a fact about the
    corpus, and discovering it by attempting a write is how a caller ends up
    with a half-built edit and nowhere to put it.
    """

    ref: CorpusRef
    location: str                #: resolved, absolute
    revision: str | None         #: None where this corpus carries no revision notion -- legal
    scopes: tuple[str, ...]      #: the scope names `list_documents` accepts here; always holds SCOPE_ALL
    write_path: str | None       #: the DECLARED governed write path's name; None means read-only
    write_path_available: bool   #: False where it is declared and cannot be reached


@dataclass(frozen=True)
class DocumentId:
    """A stable identity for one document within one corpus.

    `key` is OPAQUE to this interface. An implementation may make it a
    relative path, an object id or a database row key; a consumer may compare
    it, sort it and hand it back, and may not parse it.
    """

    corpus: str
    key: str


@dataclass(frozen=True)
class Document:
    """The bytes of one document, plus the revision they were read at."""

    id: DocumentId
    content: bytes
    revision: str | None


@dataclass(frozen=True)
class Classification:
    """What KIND of document this is, and which fields its kind obliges.

    `kind` is None ONLY when `unclassifiable` is set, and an unclassifiable
    document is REPORTED rather than omitted -- the reason names the document
    so a human can go look at it.
    """

    id: DocumentId
    kind: str | None
    required_fields: tuple[str, ...]    #: what this kind obliges
    missing_fields: tuple[str, ...]     #: of those, the ones absent
    unclassifiable: str | None = None   #: the reason, naming the document


@dataclass(frozen=True)
class Finding:
    """The corpus's own verdict on one subject.

    `code` is implementation-declared and OPAQUE here. This interface must not
    know the home corpus's check groupings, its thresholds or its taxonomy;
    an implementation is free to put its own grouping and rule ids inside this
    string, and a consumer may display it, group by it, and not parse it.
    """

    severity: str    #: one of SEVERITIES
    subject: str     #: a `DocumentId.key`, or the corpus name for a corpus-wide verdict
    code: str        #: implementation-declared, opaque
    message: str


@dataclass(frozen=True)
class WriteReceipt:
    """The correlation identifier a dispatched write comes back with.

    NOT a commit, not a diff and not a path: the proof that a proposed edit
    entered the declared governed write path, and the handle the eventual
    durable record is reachable from.
    """

    correlation_id: str
    dispatched_to: str   #: the declared write path's name


@runtime_checkable
class CorpusAdapter(Protocol):
    """Six methods. Nothing else, ever -- see `OPERATIONS`.

    Every method may raise `CorpusRefused`; the kinds each one can raise are
    named per method below, and an implementation raising a kind outside its
    row is a defect the conformance suite is entitled to catch.
    """

    def resolve(self, ref: CorpusRef) -> ResolvedCorpus:
        """Which checkout, which revision, which scopes, which write path.

        Design § D2's second derived operation: "given a corpus reference,
        which checkout and which revision". Also the operation that answers
        read-only-ness, BEFORE a caller builds an edit it cannot dispatch.

        Refuses CORPUS_ABSENT, CORPUS_UNREADABLE, CORPUS_UNCLASSIFIABLE or
        REVISION_UNKNOWN. It never degrades to an empty result: an absent
        corpus and an empty corpus are different answers.
        """

    def list_documents(self, corpus: ResolvedCorpus,
                       scope: str = SCOPE_ALL) -> tuple[DocumentId, ...]:
        """Which documents this corpus holds under a declared scope.

        Sorted, stable across calls, no duplicates. A genuinely empty corpus
        returns `()` and that is NOT a refusal. A scope name outside
        `corpus.scopes` refuses SCOPE_UNKNOWN rather than quietly listing
        everything, because a silent widening is indistinguishable from a
        correct answer.
        """

    def read(self, corpus: ResolvedCorpus, document: DocumentId,
             revision: str | None = None) -> Document:
        """The bytes of one document at a declared revision.

        `revision=None` means the revision `corpus` was resolved at. A
        revision this implementation cannot serve refuses REVISION_UNKNOWN and
        NEVER falls back to another one -- a silent fallback returns bytes
        that answer a question nobody asked. An unknown identity refuses
        DOCUMENT_UNKNOWN.
        """

    def classify(self, corpus: ResolvedCorpus,
                 document: DocumentId) -> Classification:
        """What kind this document is, and which fields its kind obliges.

        Never omits. A shape this implementation does not recognize comes back
        as `kind=None` with `unclassifiable` set to a reason that names the
        document, and the same document still appears in `list_documents`.
        """

    def check(self, corpus: ResolvedCorpus,
              subjects: tuple[DocumentId, ...] | None = None) -> tuple[Finding, ...]:
        """The corpus's own verdict on a document, a set of them, or all.

        `subjects=None` means the whole corpus. A corpus with no verdict
        machinery of its own honestly returns `()`; that is an answer, not a
        refusal, and a consumer must not read it as "clean" without asking
        whether the corpus judges at all.
        """

    def write_back(self, corpus: ResolvedCorpus, document: DocumentId,
                   content: bytes, *, actor: str, basis_revision: str,
                   reason: str = "") -> WriteReceipt:
        """DISPATCH a proposed document body through the declared write path.

        `content` is what the document should become and `basis_revision` is
        the revision the proposer was looking at -- together the whole of
        what is proposed, and the second is what any governed path needs in
        order to refuse a stale one.

        Refuses CORPUS_READ_ONLY where `corpus.write_path` is None (and
        `resolve` already said so), and WRITE_PATH_UNREACHABLE naming the path
        where it is declared and cannot be reached -- and in that case the
        document remains unsaved rather than being written by a fallback.

        An implementation that writes the corpus tree here is not conformant,
        even where it would produce identical bytes.
        """


# NOTE (#872, RULED OQ-Q): openxFactory's executable readers of this module now
# import the pinned copy at `openDox/code/src/opendox/corpus_adapter.py` once
# that submodule is initialized (see `corpus_adapter_openxfactory/adapter.py`'s
# header). This file stays in tree because the carve manifest's row for this
# path is `not_moved / replicated_at_destination`, and deleting a retained
# row's path is refused by `validate-carve-manifest.py` (`carve-path-absent`):
# only flipping that row's disposition (Brett Heap's act) or folding this path
# into a follow-up shed PR makes removal lawful.
#
# NO APPLICATION CONSUMER reads this copy any more -- every executable reader
# of the interface's dataclasses was re-pointed above. What still reads this
# exact path, by design, is structural test tooling comparing shapes or
# refusals rather than nominal class identity, for which a second,
# separately-loaded copy of the interface is the point, not a defect:
#   - by import: `scripts/carve_conformance.py`,
#     `tests/carve_conformance/home_factory.py` and
#     `tests/carve_conformance/test_verify_carve_conformance.py` (see that
#     file's own docstring on why a distinct class object here must PASS),
#     `tests/corpus-adapter/test_interface_closure.py`, and two dashboard
#     test modules, `test_authoring_classify_derivation.py` and
#     `test_doxbench_status_exemption.py`
#   - by path, never imported: the two neutrality scans named above
