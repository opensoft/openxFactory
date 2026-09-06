"""openxFactory's own conformant implementation of the corpus-adapter
interface — ONE implementation among others, with no private door.

`split-opendox-two-layer-product` § 2.2a, under RULING DQ-1 (2026-09-04T22:14Z):
"doc-health and OpenSpec stay in openxFactory, and a small adapter package
beside them implements the corpus-adapter seam". That ruling makes this
repository permanently both the owner of a corpus and the author of a reader
over it — "exactly the position in which a private door gets built" — so the
seam's fourth requirement is this class's governing constraint, not a
formality.

HOW THE ABSENCE OF A PRIVATE DOOR IS MADE MECHANICAL, rather than asserted:

  1. SIX PUBLIC METHODS, and they are the interface's six. A companion test
     parses this file and compares the public method names against
     `corpus_adapter.OPERATIONS`, so a seventh — a home-only convenience — is a
     red test, which is the requirement's "an operation exists only for the home
     corpus" scenario made into a gate.
  2. NO PATH LITERAL AND NO HOME BRANCH. Everything this class knows about a
     corpus arrives as a `CorpusShape` at construction. There is no `if home:`
     anywhere in this module, and the neutral conformance corpus — no
     `openspec/`, no `contracts/`, no lifecycle headers — is served by this same
     class with the same code path, which design D6 part 3 calls the only
     mechanical proof the requirement holds.
  3. NOTHING HERE WRITES. `write_back` dispatches through the shape's declared
     write path and returns its receipt; no method in this module opens a file
     for writing, and the conformance suite asserts the target's bytes are
     unchanged after a refused write.

FAIL CLOSED, TWO DIFFERENT WAYS, AND THE DIFFERENCE IS THE SEAM'S SECOND
REQUIREMENT. An unresolvable CORPUS refuses and names what it could not
resolve; a genuinely empty corpus returns an empty listing, which is a
different answer — "a projection built over the first is correct and a
projection built over the second is a lie with a timestamp". That is the T092
lesson this repository already wrote down once, in
`ideation_dashboard.corpus_root`, after a `--repo-root` from another filesystem
namespace produced a written, exit-0, entirely empty snapshot. An unrecognizable
DOCUMENT does the opposite and is reported, never omitted.

WHY `resolve` DOES NOT IMPORT `corpus_root` (RULING OQ-4, 2026-09-06:
ADAPTER'S OWN). Its `corpus_scan_defect` is the same four-way structural test
this class applies, and this repository is unusually intolerant of
co-authoritative constants — § 2.3 exists to kill one. But importing it would
make this permanent adapter depend on a package whose destiny is unsettled
(`corpus_root` is not among design D3's third-column modules), while repointing
`corpus_root` at this class reaches `cli.py`'s `--repo-root` and `serve.py`'s
`--checkout-root`, which is § 2.4's critical path. So the adapter carries its own
shape-driven resolution, `corpus_root` is untouched, and a parity test pins
`HOME_SHAPE.scan_roots == corpus_root.SCANNED_ROOTS` so the duplication fails
closed instead of drifting. The collapse is filed to § 2.4.
"""

from __future__ import annotations

from pathlib import Path

from doc_health.corpus import RealGit

from corpus_adapter import (
    CORPUS_ABSENT,
    CORPUS_READ_ONLY,
    CORPUS_UNCLASSIFIABLE,
    CORPUS_UNREADABLE,
    DOCUMENT_UNKNOWN,
    REVISION_UNKNOWN,
    SCOPE_ALL,
    SCOPE_UNKNOWN,
    WRITE_PATH_UNREACHABLE,
    Classification,
    CorpusRef,
    CorpusRefused,
    Document,
    DocumentId,
    Finding,
    Refusal,
    ResolvedCorpus,
    WriteReceipt,
)

from .classify import classify_text
from .shape import CorpusShape, Scope, WriteProposal

#: The marker a versioned corpus root carries. A checkout has it as a
#: directory, a worktree as a file, and a plain tree of documents has neither —
#: in which case this corpus has no revision notion at all, which the interface
#: declares legal. Asking git about a directory that merely SITS INSIDE a
#: checkout would answer with the enclosing repository's revision, which is a
#: different corpus's answer.
VERSION_MARKER = ".git"

#: The reference a corpus resolves to when the caller names none.
DEFAULT_REF = "HEAD"


def _refuse(kind: str, subject: str, detail: str) -> CorpusRefused:
    return CorpusRefused(Refusal(kind=kind, subject=subject, detail=detail))


class OpenxFactoryCorpusAdapter:
    """Six operations over one corpus, built from one `CorpusShape`."""

    def __init__(self, shape: CorpusShape) -> None:
        self._shape = shape
        # One listing per (location, revision, scope), remembered for this
        # INSTANCE only. Not an optimization for its own sake: `read` decides
        # membership by asking the listing — the one definition, so no second
        # membership rule can disagree with the first — and re-walking the tree
        # per read would make classifying a corpus quadratic in its own size.
        # The instance is bound to the revision it resolved, so the cache can
        # only be stale for a caller who changed the tree underneath it; such a
        # caller resolves again, which is the same thing it would have to do to
        # get a new revision anyway.
        self._listings: dict[tuple[str, str | None, str], tuple[str, ...]] = {}

    # -- the six -----------------------------------------------------------

    def resolve(self, ref: CorpusRef) -> ResolvedCorpus:
        """Which checkout, which revision, which scopes, which write path.

        The structural test is the shape's `scan_roots`: a tree holding none of
        them cannot be this corpus, and saying so is different from saying it is
        empty. A tree that IS this corpus and happens to hold no documents
        resolves fine and lists nothing — the one distinction the whole
        requirement is about.
        """
        location = Path(ref.location)
        try:
            if not location.exists():
                raise _refuse(CORPUS_ABSENT, str(location),
                              "the path does not exist")
            if not location.is_dir():
                raise _refuse(CORPUS_UNREADABLE, str(location),
                              "the path is not a directory")
            if not any((location / root).is_dir()
                       for root in self._shape.scan_roots):
                raise _refuse(
                    CORPUS_UNCLASSIFIABLE, str(location),
                    "the directory holds none of the roots this corpus is "
                    f"declared over ({', '.join(self._shape.scan_roots)})")
        except OSError as exc:   # an unreadable path is not this corpus either
            raise _refuse(CORPUS_UNREADABLE, str(location),
                          f"the path could not be read ({exc.strerror or exc})") from exc

        resolved = location.resolve()
        revision = self._revision(resolved, ref.revision)
        write_path = self._shape.write_path
        return ResolvedCorpus(
            ref=ref,
            location=str(resolved),
            revision=revision,
            # De-duplicated: a corpus MAY declare a scope named `all` and
            # nothing else, which is the smallest conformant shape there is.
            scopes=tuple(dict.fromkeys((SCOPE_ALL, *sorted(self._shape.scopes)))),
            write_path=None if write_path is None else write_path.name,
            write_path_available=bool(write_path and write_path.available),
        )

    def list_documents(self, corpus: ResolvedCorpus,
                       scope: str = SCOPE_ALL) -> tuple[DocumentId, ...]:
        """Every document identity under one declared scope, sorted and unique.

        A scope this corpus does not declare REFUSES rather than quietly
        widening to everything: a silent widening is indistinguishable from a
        correct answer, and this corpus in particular keeps two scopes whose
        membership rules were deliberately ruled DISTINCT
        (`govern-openspec-corpus-membership`, 2026-08-23) — merging them would
        sweep in documents a ruling explicitly left out.
        """
        if scope != SCOPE_ALL and scope not in self._shape.scopes:
            raise _refuse(
                SCOPE_UNKNOWN, scope,
                f"{corpus.ref.name} declares "
                f"{', '.join((SCOPE_ALL, *sorted(self._shape.scopes)))}")
        return tuple(DocumentId(corpus=corpus.ref.name, key=key)
                     for key in self._keys(corpus, scope))

    def read(self, corpus: ResolvedCorpus, document: DocumentId,
             revision: str | None = None) -> Document:
        """The bytes of one listed document, at the revision this corpus was
        resolved at.

        Reading arbitrary history is deliberately OUT: this adapter reads the
        checkout it is pointed at, and any other revision refuses rather than
        silently answering from the one it has. A caller that wants another
        revision resolves another corpus.
        """
        if revision is not None and revision != corpus.revision:
            raise _refuse(
                REVISION_UNKNOWN, revision,
                f"{corpus.ref.name} is resolved at {corpus.revision!r} and this "
                "reader serves the checkout it is pointed at, never another "
                "revision from it")
        self._require_listed(corpus, (document.key,))
        path = Path(corpus.location) / document.key
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise _refuse(CORPUS_UNREADABLE, document.key,
                          f"the document could not be read ({exc.strerror or exc})") from exc
        return Document(id=document, content=content, revision=corpus.revision)

    def classify(self, corpus: ResolvedCorpus,
                 document: DocumentId) -> Classification:
        """This document's kind and the fields its kind obliges.

        Reads through `read`, so an unknown identity refuses exactly as it does
        there and no second membership rule exists to disagree with the first.
        Decoding mirrors the corpus loader's own (`errors="replace"`), because a
        reader stricter than the loader would report a document the corpus reads
        happily as unreadable.
        """
        text = self.read(corpus, document).content.decode("utf-8", errors="replace")
        return classify_text(document, text, self._shape)

    def check(self, corpus: ResolvedCorpus,
              subjects: tuple[DocumentId, ...] | None = None) -> tuple[Finding, ...]:
        """This corpus's own verdict, mapped onto neutral findings.

        A corpus whose shape declares no verdict machinery honestly returns an
        empty result — an answer, not a refusal, and not a claim of cleanliness.
        A named subject this corpus does not list refuses rather than being
        silently dropped: a verdict that quietly checked less than it was asked
        to is a false green.
        """
        known = frozenset(self._keys(corpus, SCOPE_ALL))
        wanted = None
        if subjects is not None:
            wanted = tuple(doc.key for doc in subjects)
            self._require_listed(corpus, wanted, known=known)
        verdict = self._shape.verdict
        if verdict is None:
            return ()
        return tuple(verdict(corpus, known, wanted))

    def write_back(self, corpus: ResolvedCorpus, document: DocumentId,
                   content: bytes, *, actor: str, basis_revision: str,
                   reason: str = "") -> WriteReceipt:
        """DISPATCH a proposed body through the declared governed write path.

        Nothing in this method writes, and the order of its guards is part of
        that: read-only and unreachable are answered BEFORE any request artifact
        is built, so a refusal cannot have produced a side effect on the way to
        being raised.

        Today every call on this repository's own corpus reaches the second
        guard — the declared path does not yet carry this verb. That is the
        conformant answer, not a gap: the requirement's own third scenario is a
        declared path that cannot be reached, and it says the write refuses,
        names the path, and the document remains unsaved rather than being
        written by a fallback.
        """
        write_path = self._shape.write_path
        if write_path is None or corpus.write_path is None:
            raise _refuse(
                CORPUS_READ_ONLY, corpus.ref.name,
                "this corpus declares no governed write path, and resolution "
                "already reported it as read-only")
        if not corpus.write_path_available:
            raise _refuse(WRITE_PATH_UNREACHABLE, write_path.name,
                          write_path.unavailable_reason
                          or "the declared write path cannot be reached")
        target = write_path.routes(document.key)
        if target is None:
            raise _refuse(
                WRITE_PATH_UNREACHABLE, write_path.name,
                f"{document.key} has no target on the declared write path, so "
                "there is nothing to dispatch through it and the document "
                "remains unsaved")
        proposal = WriteProposal(document_key=document.key, content=content,
                                 actor=actor, basis_revision=basis_revision,
                                 reason=reason)
        request = write_path.build_request(proposal)
        correlation_id = write_path.correlation_id(request)
        write_path.dispatch(request, proposal)
        return WriteReceipt(correlation_id=correlation_id,
                            dispatched_to=write_path.name)

    # -- private -----------------------------------------------------------

    def _revision(self, location: Path, requested: str | None) -> str | None:
        """The commit this corpus is read at, or None where it carries none.

        A tree with no version marker at its ROOT is a corpus with no revision
        notion, which the interface declares legal — and a caller that named a
        revision anyway is refused rather than served the bytes of a different
        one.
        """
        versioned = (location / VERSION_MARKER).exists()
        if not versioned:
            if requested is not None:
                raise _refuse(REVISION_UNKNOWN, requested,
                              f"{location} carries no revisions to resolve against")
            return None
        resolved = RealGit().resolve_ref(location, requested or DEFAULT_REF)
        if resolved is None:
            if requested is not None:
                raise _refuse(REVISION_UNKNOWN, requested,
                              f"{location} does not carry that revision")
            return None
        return resolved

    def _keys(self, corpus: ResolvedCorpus, scope: str) -> tuple[str, ...]:
        cached = self._listings.get((corpus.location, corpus.revision, scope))
        if cached is not None:
            return cached
        location = Path(corpus.location)
        names = sorted(self._shape.scopes) if scope == SCOPE_ALL else [scope]
        keys: set[str] = set()
        for name in names:
            keys.update(self._scope_keys(location, self._shape.scopes[name]))
        listed = tuple(sorted(keys))
        self._listings[(corpus.location, corpus.revision, scope)] = listed
        return listed

    def _scope_keys(self, location: Path, scope: Scope) -> set[str]:
        keys: set[str] = set()
        for pattern in scope.globs:
            for match in location.glob(pattern):
                if not match.is_file():
                    continue
                rel = match.relative_to(location)
                if any(part in scope.excluded_parts for part in rel.parts):
                    continue
                keys.add(rel.as_posix())
        return keys

    def _require_listed(self, corpus: ResolvedCorpus, keys: tuple[str, ...],
                        known: frozenset | None = None) -> None:
        if known is None:
            known = frozenset(self._keys(corpus, SCOPE_ALL))
        for key in keys:
            if key not in known:
                raise _refuse(DOCUMENT_UNKNOWN, key,
                              f"{corpus.ref.name} lists no such document")
