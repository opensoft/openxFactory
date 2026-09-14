"""The neutral conformance corpus, as CHECKS a reader either passes or does
not (`split-opendox-two-layer-product` § 3.7, design § D6 part 3, RULED OQ-1).

WHAT THIS FILE IS. Design § D6's third part of the floor is "A NEUTRAL
CONFORMANCE CORPUS EVERY DESTINATION PASSES ... on the wallet extraction's own
pattern of positives plus negative confirmations". The documents of that corpus
already exist and are RULED OQ-3's seed. What did not exist is the corpus as a
RUNNABLE OBJECT — a closed set of positives and negative confirmations that any
reader can be put through, wherever it was authored and whatever it is called.
This module is that object, and `verify-carve-conformance.py` is the operator's
way in.

WHY IT IMPORTS THE INTERFACE AND NOTHING ELSE. Every destination runs this,
including two that have no reason to hold anything of this repository's. It
therefore reaches for `corpus_adapter` — the one module RULING Q4 gives to
openDox and that travels with the carve — plus the standard library, and it
names no reader, no home layout and no home vocabulary anywhere in its source
text. That last is the same bar the interface itself is held to, and the same
test reads both.

HOW A READER IS SUPPLIED, AND WHY IT IS A FACTORY. The negative confirmations
have to point a reader at four DIFFERENT locations — a populated corpus, an
empty one, a path that is not a directory, and a path that is not there at all
— so a single constructed object would not do: three of the four cases are
about what happens at resolution time. A caller therefore hands in a callable
of `(name, location) -> reader`, which is the smallest thing that lets this
module do the pointing. A caller declares its own; nothing here knows one.

WHAT THE POSITIVES ASSERT, AND WHY NOT BY NAME. A document identity is OPAQUE
to the interface — "a consumer may compare it, sort it and hand it back, and
may not parse it" — so no check here reads a key to decide which document it is
holding. The populated corpus is instead described by the SHAPE of its answers:
how many documents it holds, how many of them classify completely, how many
classify with a field absent, and how many cannot be classified at all. That is
a property of the corpus rather than of its path spelling, it survives a
destination laying the same documents out differently, and it is strictly
harder to satisfy by accident than a name lookup is.

THE NEGATIVE CONFIRMATIONS ARE THE HALF WITH TEETH, and each one is a way a
reader can be wrong while looking right. An absent corpus that answers with an
empty listing, a scope nobody declared that quietly widens to everything, a
revision this reader cannot serve that silently falls back to one it can, a
write dispatched at a read-only corpus that lands in the tree anyway: all four
produce a plausible result and all four are lies. A reader passes here only by
REFUSING each of them, with the named refusal and not merely with an error.

THE VERDICT IS PER CHECK AND THE RUN NEVER STOPS EARLY. One failing check does
not hide the state of the others: an operator standing in front of a reader
that is new wants the whole list, and a run that halted on the first would turn
a survey into a bisection.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from corpus_adapter import (
    CORPUS_ABSENT,
    CORPUS_READ_ONLY,
    CORPUS_UNREADABLE,
    DOCUMENT_UNKNOWN,
    REVISION_UNKNOWN,
    SCOPE_ALL,
    SCOPE_UNKNOWN,
    SEVERITIES,
    CorpusAdapter,
    CorpusRef,
    DocumentId,
)

#: A callable a caller declares: given a name and a location, hand back a
#: reader pointed at it. The location is the interface's own opaque string.
Factory = Callable[[str, str], object]

#: The closed check set, in run order. Positives first, then the negative
#: confirmations, then the two that are about the corpus and not about one
#: answer. A caller reads a verdict against this tuple, so a check cannot be
#: added or dropped silently -- the companion test holds the two in step.
CHECKS: tuple[str, ...] = (
    "structural-conformance",
    "resolve-populated",
    "list-population",
    "list-stable",
    "read-round-trip",
    "classify-population",
    "classify-reports-unrecognizable",
    "check-severities",
    "empty-is-an-answer",
    "read-only-declared-at-resolution",
    "absent-refuses",
    "unreadable-refuses",
    "unknown-scope-refuses",
    "unknown-document-refuses",
    "unknown-revision-refuses",
    "write-back-refuses-read-only",
    "write-back-leaves-the-tree",
)


@dataclass(frozen=True)
class CorpusExpectation:
    """The SHAPE of the populated corpus's answers, as data.

    Not the documents' names and not their bytes: the counts a reader over
    this corpus must report. A destination holding the same documents at
    different paths satisfies the identical object.
    """

    documents: int              #: how many the populated corpus holds
    classified_complete: int    #: a kind, and no field absent
    classified_incomplete: int  #: a kind, and at least one field absent
    unrecognizable: int         #: no kind, and a reason naming the document


#: The seed corpus's own shape (RULED OQ-3): three documents in two roots, one
#: of each outcome. Stated once, here, so a caller does not restate it.
SEED_EXPECTATION = CorpusExpectation(
    documents=3,
    classified_complete=1,
    classified_incomplete=1,
    unrecognizable=1,
)

#: A revision no reader can serve, and it is deliberately not a plausible one:
#: a hexadecimal-looking value might BE a revision somewhere, and a check that
#: passed only because the value happened to be unknown would pass for the
#: wrong reason.
IMPOSSIBLE_REVISION = "no-such-revision-this-reader-can-serve"

#: A scope name no corpus declares, on the same reasoning.
UNDECLARED_SCOPE = "no-such-scope-this-corpus-declares"


@dataclass(frozen=True)
class Outcome:
    """One check's verdict. `detail` is written for a human either way -- a
    passing check that cannot say what it saw is a check nobody will trust the
    first time it fails."""

    check: str
    passed: bool
    detail: str


def _digest_tree(root: Path) -> str:
    """A digest over a directory's whole content, path and bytes together.

    Used by exactly one check, and it has to be sensitive to a file being
    ADDED as well as to bytes being rewritten: dispatching a write that
    quietly deposits a new file beside the document is the same defect as
    overwriting the document.
    """
    entries: list[tuple[str, bytes]] = []
    for base, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            try:
                entries.append((rel, path.read_bytes()))
            except OSError as exc:  # pragma: no cover - defensive
                entries.append((rel, repr(exc).encode("utf-8")))
    digest = hashlib.sha256()
    for rel, data in entries:
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _refusal_of(exc: BaseException) -> str | None:
    """The refusal kind an exception carries, read STRUCTURALLY.

    THIS IS NOT `isinstance`, AND THE REASON IS THE WHOLE POINT OF THE SEAM. A
    reader authored elsewhere holds its OWN copy of the interface module --
    the carve places one at each destination -- so the exception class it
    raises is a different object from this caller's, and an `isinstance` test
    against the local one would report a perfectly conformant reader as having
    raised something unrelated. The interface is structural everywhere else;
    its failure mode is read structurally too. What identifies a refusal is
    that it carries a `refusal` with a `kind`, which is the contract, rather
    than which module happened to define the class.
    """
    refusal = getattr(exc, "refusal", None)
    kind = getattr(refusal, "kind", None)
    return kind if isinstance(kind, str) else None


def _expect_refusal(fn: Callable[[], object], kind: str,
                    what: str) -> tuple[bool, str]:
    """Run `fn` and hold it to ONE named refusal.

    Three ways to be wrong, and they are reported differently on purpose: a
    call that RETURNED is the degradation the seam exists to forbid, a call
    that raised the wrong refusal is a reader answering a question nobody
    asked, and a call that raised something else entirely has not reached the
    interface's own failure mode at all.
    """
    try:
        got = fn()
    except Exception as exc:  # noqa: BLE001 - the kind is read structurally
        actual = _refusal_of(exc)
        if actual == kind:
            return True, f"{what} refused {kind}"
        if actual is not None:
            return False, (f"{what} refused {actual!r}, and this corpus holds "
                           f"it to {kind!r}")
        return False, (f"{what} raised {type(exc).__name__}: {exc}. The "
                       f"interface's one failure mode is a refusal carrying "
                       f"{kind!r}")
    return False, (f"{what} RETURNED {got!r} where it owes a {kind!r} "
                   f"refusal. Degrading to a result is the one thing a reader "
                   f"over a corpus it does not own must never do")


def _classification_shape(reader, corpus, documents: Iterable) -> tuple[
        int, int, int, list[str]]:
    complete = incomplete = unrecognizable = 0
    problems: list[str] = []
    for document in documents:
        answer = reader.classify(corpus, document)
        if answer.kind is None:
            if not answer.unclassifiable:
                problems.append(
                    "a document came back with no kind and no reason; a "
                    "reader owes a reason that names the document")
                continue
            unrecognizable += 1
        elif answer.missing_fields:
            incomplete += 1
        else:
            complete += 1
    return complete, incomplete, unrecognizable, problems


def run(factory: Factory, *, populated: str, empty: str, unreadable: str,
        absent: str,
        expectation: CorpusExpectation = SEED_EXPECTATION) -> tuple[
            Outcome, ...]:
    """Put one reader through the whole corpus and hand back every verdict.

    The four locations are the corpus's four states, and a caller supplies
    them because only a caller knows where it laid the documents down.
    """
    outcomes: list[Outcome] = []

    def record(check: str, passed: bool, detail: str) -> None:
        outcomes.append(Outcome(check=check, passed=passed, detail=detail))

    reader = factory("populated", populated)

    record("structural-conformance", isinstance(reader, CorpusAdapter),
           (f"{type(reader).__name__} "
            f"{'satisfies' if isinstance(reader, CorpusAdapter) else 'does not satisfy'}"
            " the interface's six operations"))

    # ---- the positives, over the populated corpus -------------------------
    corpus = None
    try:
        corpus = reader.resolve(CorpusRef(name="populated",
                                          location=populated))
        ok = SCOPE_ALL in corpus.scopes
        record("resolve-populated", ok,
               (f"resolved at {corpus.location!r}; declared scopes "
                f"{corpus.scopes!r}"
                + ("" if ok else f"; every corpus owes {SCOPE_ALL!r}")))
    except Exception as exc:  # noqa: BLE001
        record("resolve-populated", False,
               f"resolving the populated corpus raised "
               f"{type(exc).__name__}: {exc}")

    if corpus is None:
        # Everything below reads a resolved corpus. Report the rest as not
        # reached rather than as passing, and never as failing for a cause
        # that is already on the list once.
        for check in CHECKS:
            if check in {c.check for c in outcomes}:
                continue
            record(check, False, "not reached: the populated corpus did not "
                                 "resolve")
        return tuple(outcomes)

    documents: tuple = ()
    try:
        documents = reader.list_documents(corpus)
        ok = len(documents) == expectation.documents
        record("list-population", ok,
               f"listed {len(documents)} document(s); this corpus holds "
               f"{expectation.documents}")
    except Exception as exc:  # noqa: BLE001
        record("list-population", False,
               f"listing raised {type(exc).__name__}: {exc}")

    try:
        again = reader.list_documents(corpus)
        sorted_ok = list(documents) == sorted(documents, key=lambda d: d.key)
        unique = len({d.key for d in documents}) == len(documents)
        stable = list(again) == list(documents)
        ok = sorted_ok and unique and stable
        record("list-stable", ok,
               f"sorted={sorted_ok} unique={unique} stable-across-calls="
               f"{stable}")
    except Exception as exc:  # noqa: BLE001
        record("list-stable", False,
               f"the second listing raised {type(exc).__name__}: {exc}")

    if documents:
        try:
            first = documents[0]
            got = reader.read(corpus, first)
            ok = got.id == first and isinstance(got.content, bytes)
            record("read-round-trip", ok,
                   f"read {len(got.content)} byte(s); identity round-tripped="
                   f"{got.id == first}")
        except Exception as exc:  # noqa: BLE001
            record("read-round-trip", False,
                   f"reading raised {type(exc).__name__}: {exc}")
    else:
        record("read-round-trip", False,
               "not reached: the listing was empty")

    try:
        complete, incomplete, unrecognizable, problems = _classification_shape(
            reader, corpus, documents)
        ok = (not problems
              and complete == expectation.classified_complete
              and incomplete == expectation.classified_incomplete
              and unrecognizable == expectation.unrecognizable)
        record("classify-population", ok,
               (f"complete={complete} field-absent={incomplete} "
                f"unrecognizable={unrecognizable}; this corpus holds "
                f"{expectation.classified_complete}/"
                f"{expectation.classified_incomplete}/"
                f"{expectation.unrecognizable}"
                + ("; " + "; ".join(problems) if problems else "")))
        # The one clause design § D2 states twice: an unrecognizable document
        # is REPORTED and STAYS LISTED. The count above proves the report; the
        # listing it was drawn from proves it stayed.
        listed = unrecognizable > 0 and len(documents) == expectation.documents
        record("classify-reports-unrecognizable", listed,
               (f"{unrecognizable} unrecognizable document(s), and the "
                f"listing still holds {len(documents)}"
                if listed else
                "an unrecognizable document was omitted from the listing, or "
                "none was reported at all"))
    except Exception as exc:  # noqa: BLE001
        record("classify-population", False,
               f"classifying raised {type(exc).__name__}: {exc}")
        record("classify-reports-unrecognizable", False,
               "not reached: classifying raised")

    try:
        findings = reader.check(corpus)
        bad = [f.severity for f in findings if f.severity not in SEVERITIES]
        ok = not bad
        record("check-severities", ok,
               (f"{len(findings)} finding(s), every severity within the "
                f"declared vocabulary"
                if ok else
                f"{len(findings)} finding(s), and these severities are "
                f"outside the declared vocabulary: {sorted(set(bad))}"))
    except Exception as exc:  # noqa: BLE001
        record("check-severities", False,
               f"the verdict raised {type(exc).__name__}: {exc}")

    # ---- the empty corpus is an ANSWER ------------------------------------
    try:
        empty_reader = factory("empty", empty)
        empty_corpus = empty_reader.resolve(CorpusRef(name="empty",
                                                      location=empty))
        listing = empty_reader.list_documents(empty_corpus)
        ok = listing == ()
        record("empty-is-an-answer", ok,
               (f"an empty corpus resolved and listed {listing!r}"
                if ok else
                f"an empty corpus listed {len(listing)} document(s), so it is "
                f"not empty and this location is the wrong one"))
    except Exception as exc:  # noqa: BLE001 - the kind is read structurally
        refused = _refusal_of(exc)
        record("empty-is-an-answer", False,
               (f"an empty corpus REFUSED {refused!r}. An empty corpus and an "
                f"unreadable one are different answers, and a reader that "
                f"conflates them makes a projection over nothing "
                f"indistinguishable from one over a tree it could not open"
                if refused is not None else
                f"the empty corpus raised {type(exc).__name__}: {exc}"))

    # ---- read-only is answered at RESOLUTION, not at the first write ------
    ok = corpus.write_path is None
    record("read-only-declared-at-resolution", ok,
           ("resolution reported no declared write path, so this corpus is "
            "read-only before a caller builds an edit"
            if ok else
            f"resolution reported the write path {corpus.write_path!r}; this "
            f"corpus declares none, so a reader is inventing one"))

    # ---- the negative confirmations ---------------------------------------
    absent_reader = factory("absent", absent)
    passed, detail = _expect_refusal(
        lambda: absent_reader.resolve(CorpusRef(name="absent",
                                                location=absent)),
        CORPUS_ABSENT, "resolving a corpus that is not there")
    record("absent-refuses", passed, detail)

    unreadable_reader = factory("unreadable", unreadable)
    passed, detail = _expect_refusal(
        lambda: unreadable_reader.resolve(CorpusRef(name="unreadable",
                                                    location=unreadable)),
        CORPUS_UNREADABLE, "resolving a corpus that is not a directory")
    record("unreadable-refuses", passed, detail)

    passed, detail = _expect_refusal(
        lambda: reader.list_documents(corpus, UNDECLARED_SCOPE),
        SCOPE_UNKNOWN, "listing under a scope this corpus does not declare")
    record("unknown-scope-refuses", passed, detail)

    unknown = _unknown_document(documents, corpus)
    passed, detail = _expect_refusal(
        lambda: reader.read(corpus, unknown),
        DOCUMENT_UNKNOWN, "reading an identity this corpus does not hold")
    record("unknown-document-refuses", passed, detail)

    if documents:
        passed, detail = _expect_refusal(
            lambda: reader.read(corpus, documents[0], IMPOSSIBLE_REVISION),
            REVISION_UNKNOWN,
            "reading at a revision this reader cannot serve")
    else:
        passed, detail = False, "not reached: the listing was empty"
    record("unknown-revision-refuses", passed, detail)

    if documents:
        before = _digest_tree(Path(populated))
        passed, detail = _expect_refusal(
            lambda: reader.write_back(corpus, documents[0], b"rewritten",
                                      actor="the conformance corpus",
                                      basis_revision=str(corpus.revision)),
            CORPUS_READ_ONLY,
            "dispatching a write at a corpus that declares no write path")
        record("write-back-refuses-read-only", passed, detail)
        after = _digest_tree(Path(populated))
        record("write-back-leaves-the-tree", before == after,
               ("the corpus tree is byte-for-byte what it was before the "
                "refused write"
                if before == after else
                "the corpus tree MOVED under a write that was refused. A "
                "reader must not touch the tree, and least of all on a path "
                "it has already declined"))
    else:
        record("write-back-refuses-read-only", False,
               "not reached: the listing was empty")
        record("write-back-leaves-the-tree", False,
               "not reached: the listing was empty")

    return tuple(outcomes)


def _unknown_document(documents, corpus):
    """An identity this corpus does not hold, built without parsing one.

    The key is opaque, so the only lawful way to make a value that is
    certainly absent is to take one that is certainly present and extend it --
    a longer string cannot equal a shorter one, whatever the encoding.
    """
    seed = documents[0].key if documents else "seed"
    return DocumentId(corpus=corpus.ref.name,
                      key=seed + "/this-identity-is-not-in-this-corpus")


def verdict(outcomes: Iterable[Outcome]) -> tuple[int, int, tuple[str, ...]]:
    """`(passed, total, the checks that did not pass)`."""
    collected = tuple(outcomes)
    failed = tuple(o.check for o in collected if not o.passed)
    return len(collected) - len(failed), len(collected), failed
