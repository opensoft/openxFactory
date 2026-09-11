"""The neutral conformance suite — written against the INTERFACE, run over
several corpora, including one the home adapter does not own.

RULING OQ-3 (`opensoft/openxFactory` issue #656, 2026-09-06): **SEED HERE.**
Design D6 part 3 of `split-opendox-two-layer-product` makes "a neutral
conformance corpus every destination passes" one of the four parts of the floor
that replaces byte identity for the carve, and its words are "every
destination" — so openXdox's adapter implementation and openxFactory's own
adapter run it too, which is "the only mechanical proof that
`corpus-adapter-seam`'s no-privileged-route requirement holds for the home
corpus". `tasks.md` § 3.7 files the corpus on the openDox side, which does not
exist yet; `fixtures/neutral/` is the seed handed upstream when it does, and
`fixtures/README.md` says so.

HOW THIS FILE STAYS HANDABLE-OVER. Everything below the fence is written
against `corpus_adapter` alone and is parameterized by an adapter FACTORY. A
future openXdox or openDox implementation replaces the block ABOVE the fence —
its own factories, its own corpora — and every assertion here runs unchanged.
That is why the whole file is a move rather than a rewrite when § 3.7 comes due.

ZERO HOME BRANCHES BELOW THE FENCE, and it is worth stating as this file's own
invariant because a reviewer can check it by eye: there is no `if corpus is
home:` anywhere, and no assertion is conditioned on WHICH corpus is under test.
Where behaviour legitimately differs between corpora — a read-only corpus versus
one with a declared write path — the difference is read from what `resolve`
ITSELF reported, which is the interface's own answer and available to any
implementation. `test_no_home_vocabulary.py` catches the literal form of the
same cheat.

THE SUITE HAS TEETH, and the last test is where they are. Two deliberately
non-conformant adapters are defined in-file — one that returns an empty listing
for an absent checkout instead of refusing, and one whose write-back writes the
tree — and the suite's fail-closed checks are run against them and asserted to
FAIL. Without that, a green suite would prove only that the real implementation
happens to behave; with it, the suite is the thing enforcing requirements 2 and
3 rather than the implementation's goodwill.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

# #872 (RULED OQ-Q): the adapter under test now builds its dataclasses from the
# PINNED openDox copy, not the local `scripts/corpus_adapter.py` replica — this
# suite must construct/compare against the SAME copy, or every isinstance check
# below (a nominal check, since these are dataclasses and not the Protocol)
# reports a conformant adapter as foreign. See `adapter.py`'s header.
_OPENDOX_SRC = REPO_ROOT / "openDox" / "code" / "src"
if not (_OPENDOX_SRC / "opendox" / "corpus_adapter.py").is_file():
    raise ImportError(
        "test_conformance: the pinned openDox corpus-adapter interface is not "
        f"at {_OPENDOX_SRC / 'opendox' / 'corpus_adapter.py'}. Run `git "
        "submodule update --init --recursive openDox` from the repository "
        "root.")
sys.path.insert(0, str(_OPENDOX_SRC))

from opendox.corpus_adapter import (  # noqa: E402
    CORPUS_ABSENT,
    CORPUS_READ_ONLY,
    CORPUS_UNREADABLE,
    DOCUMENT_UNKNOWN,
    INTERFACE_PROVENANCE,
    WRITE_PATH_UNREACHABLE,
    REVISION_UNKNOWN,
    SCOPE_ALL,
    SCOPE_UNKNOWN,
    SEVERITIES,
    Classification,
    CorpusAdapter,
    CorpusRef,
    CorpusRefused,
    Document,
    DocumentId,
    ResolvedCorpus,
    WriteReceipt,
)

# ==========================================================================
# THE ONLY IMPLEMENTATION-AWARE BLOCK IN THIS FILE.
# Replace it to run this suite against another implementation; nothing below
# the fence names one.
# ==========================================================================

from corpus_adapter_openxfactory import (  # noqa: E402
    OpenxFactoryCorpusAdapter,
    home_corpus,
)
from corpus_adapter_openxfactory.home import home_shape  # noqa: E402
from corpus_adapter_openxfactory.shape import CorpusShape, Scope  # noqa: E402
from corpus_adapter_openxfactory.write_path import apply_lane_write_path  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"

#: The neutral corpus's own shape: two roots of its own, a two-field header
#: vocabulary of its own, no governed write path, and no verdict machinery.
#: Nothing here is derived from the home corpus, which is the point.
NEUTRAL_SHAPE = CorpusShape(
    scan_roots=("notes", "papers"),
    scopes={SCOPE_ALL: Scope(globs=("**/*.md",))},
    header_scan_lines=6,
    kind_field="Type",
    required_fields_by_kind={None: ("Type", "Title")},
)

#: A verdict over the whole home corpus is a two-minute run and this suite is a
#: per-pull-request gate, so the home factory narrows it to ONE check grouping.
#: Narrowing is a construction argument any implementation may offer over its
#: own corpus — it adds no operation and opens no route the interface does not
#: define — and the mapping itself is pinned in full by
#: `test_openxfactory_adapter.py`.
HOME_VERDICT_GROUPS = ("status-validity",)


def _neutral():
    return (OpenxFactoryCorpusAdapter(NEUTRAL_SHAPE),
            CorpusRef(name="neutral", location=str(FIXTURES / "neutral")))


def _empty():
    return (OpenxFactoryCorpusAdapter(NEUTRAL_SHAPE),
            CorpusRef(name="empty", location=str(FIXTURES / "empty")))


def _home():
    built = home_corpus(verdict_groups=HOME_VERDICT_GROUPS)
    return built.adapter, built.ref


#: Every request the dispatchable fixture's write path is handed. A LIST, not a
#: count, so a test can say what was dispatched as well as how often.
DISPATCH_LOG: list = []


def _dispatchable():
    """A corpus whose declared write path is genuinely REACHABLE.

    WHY THIS FIXTURE HAD TO EXIST. Every other corpus in this suite resolves
    against a write path that is either absent or unavailable, so the guard that
    refuses a MISMATCHED path name was never the guard that fired — the
    availability guard behind it caught everything first, and deleting the
    mismatch guard left the whole suite green. A conformance suite that cannot
    distinguish two guards is not testing either of them.

    The injected dispatcher RECORDS and does nothing: no workflow is invoked by
    this suite. What it buys is the one branch nothing else reaches — an adapter
    whose own path IS open, where a forged reference is the only thing standing
    between a caller and a real dispatch.
    """
    DISPATCH_LOG.clear()
    shape = replace(home_shape(verdict_groups=HOME_VERDICT_GROUPS),
                    write_path=apply_lane_write_path(
                        dispatch=lambda request, proposal: DISPATCH_LOG.append(request)))
    return OpenxFactoryCorpusAdapter(shape), home_corpus().ref


def dispatches_recorded(name: str) -> int | None:
    """How many dispatches this fixture's write path has taken, or None where
    the fixture instruments none.

    Implementation-supplied because only an implementation can instrument its
    own path. The assertions below read the COUNT and nothing else.
    """
    return len(DISPATCH_LOG) if name == DISPATCHABLE_ID else None


def adapter_for(location) -> CorpusAdapter:
    """A conformant adapter to point at an arbitrary location."""
    return OpenxFactoryCorpusAdapter(NEUTRAL_SHAPE)


#: (id, factory). Each factory returns `(adapter, ref)` for a RESOLVABLE corpus.
FACTORIES = (("neutral", _neutral), ("empty", _empty), ("home", _home),
             ("dispatchable", _dispatchable))

#: Which of them is the genuinely empty one — a fixture label, not a branch.
EMPTY_ID = "empty"

#: Which of them has a genuinely reachable write path — likewise a label.
DISPATCHABLE_ID = "dispatchable"

#: A path that exists and is not a directory.
NOT_A_DIRECTORY = FIXTURES / "not-a-directory"

# ==========================================================================
# END OF THE IMPLEMENTATION-AWARE BLOCK. Everything below is the standard.
# ==========================================================================

IDS = [name for name, _factory in FACTORIES]
#: How many documents a large corpus is sampled down to. Deterministic (the
#: first N of the sorted listing), so a failure is reproducible.
SAMPLE = 25


def refusal_kind(excinfo) -> str:
    return excinfo.value.refusal.kind


# -- the fail-closed checks, as functions, so the teeth can re-run them ------


def check_absent_corpus_refuses_and_names_it(adapter, location) -> None:
    """Requirement 2, scenario 1. `location` must not exist."""
    ref = CorpusRef(name="absent", location=str(location))
    try:
        resolved = adapter.resolve(ref)
    except CorpusRefused as refused:
        assert refused.refusal.kind == CORPUS_ABSENT, (
            f"an absent checkout must refuse {CORPUS_ABSENT}, got "
            f"{refused.refusal.kind}")
        assert str(location) in refused.refusal.subject, (
            "the refusal must NAME the corpus it could not resolve; got "
            f"{refused.refusal.subject!r}")
        return
    raise AssertionError(
        "an adapter pointed at an absent checkout must REFUSE and name it, not "
        f"degrade to a result — it returned {resolved!r}. An empty answer and "
        "an unreadable corpus must be distinguishable, or a projection built "
        "over the second is a lie with a timestamp")


def check_write_back_honours_what_resolve_declared(adapter, ref) -> None:
    """Requirement 3, all three scenarios, driven by the adapter's OWN report.

    A read-only corpus must have said so at resolution time; a declared path
    that cannot be reached must refuse BY NAME and leave the document exactly as
    it was; a reachable path must return a receipt naming it. Nothing here knows
    which case any particular corpus is in.
    """
    resolved = adapter.resolve(ref)
    listed = adapter.list_documents(resolved, SCOPE_ALL)
    if not listed:
        return
    document = listed[0]
    before = adapter.read(resolved, document).content
    on_disk = Path(resolved.location) / document.key
    bytes_before = on_disk.read_bytes() if on_disk.is_file() else None

    proposed = before + b"\nproposed by the conformance suite\n"
    try:
        receipt = adapter.write_back(
            resolved, document, proposed, actor="conformance-suite",
            basis_revision=resolved.revision or "0" * 40,
            reason="conformance")
    except CorpusRefused as refused:
        kind = refused.refusal.kind
        if resolved.write_path is None:
            assert kind == CORPUS_READ_ONLY, (
                "a corpus with no declared write path must refuse "
                f"{CORPUS_READ_ONLY}; got {kind}")
        else:
            assert kind == WRITE_PATH_UNREACHABLE, (
                "a corpus with a declared write path that will not carry this "
                f"write must refuse {WRITE_PATH_UNREACHABLE}; got {kind}")
            assert refused.refusal.subject == resolved.write_path, (
                "the refusal must NAME the declared path so an operator knows "
                f"what to go and look at; got {refused.refusal.subject!r}")
            # An UNAVAILABLE path refuses every document. An AVAILABLE one may
            # still refuse a particular document that has no target on it, and
            # that is not a contradiction — both refusals name the path.
    else:
        assert resolved.write_path_available, (
            "a write DISPATCHED through a path resolution had reported "
            "unavailable — the receipt and the resolution must agree")
        assert isinstance(receipt, WriteReceipt) and receipt.correlation_id, (
            "a dispatched write returns a correlation identifier")
        assert receipt.dispatched_to == resolved.write_path

    if bytes_before is not None:
        assert on_disk.read_bytes() == bytes_before, (
            f"{document.key} changed on disk. Write-back DISPATCHES through the "
            "declared governed write path and never writes the corpus tree — "
            "'refused even where it would produce the identical bytes, because "
            "the gate is the act of passing through the path and not the shape "
            "of the result'")


def check_a_forged_reference_cannot_open_the_write_path(adapter, ref,
                                                       witness=None) -> None:
    """Requirement 3, against a caller that did not come through `resolve`.

    `ResolvedCorpus` is PLAIN DATA. Nothing stops a caller — or a consumer that
    cached one, or a future route that reconstructs one from a request body —
    from handing an adapter a reference it never issued. An implementation that
    decides whether the governed write path is reachable by READING that
    reference has made the gate advisory: set one boolean and the write goes
    through, "even where it would produce the identical bytes, because the gate
    is the act of passing through the path and not the shape of the result".

    So both forgeries below must REFUSE. A `TypeError` is not a refusal and does
    not satisfy this check — it is what an implementation raises on its way to a
    dispatch it should never have reached, and it stops being raised at all the
    moment a real dispatcher is injected.

    `witness`, where a fixture supplies one, reports how many dispatches its
    write path has taken. A refusal that nonetheless moved that number is not a
    refusal, and on a fixture whose path is genuinely OPEN it is the only thing
    that tells a real refusal from one raised after the dispatch already
    happened.

    Forging AVAILABILITY is only a forgery on a corpus that reported itself
    unavailable; where the path is already open there is nothing to forge, and
    a write that succeeds there is correct rather than a defect. Which of the
    two applies is read from the adapter's own report, so this stays a statement
    about any implementation.
    """
    resolved = adapter.resolve(ref)
    listed = adapter.list_documents(resolved, SCOPE_ALL)
    if not listed:
        return

    # A SPREAD across the listing, not its head. An implementation may refuse
    # some documents for an unrelated reason — this one has no target on the
    # declared path, say — and if the sample happened to hold only those, every
    # forgery would meet that refusal instead and the check would pass over an
    # adapter that trusts the reference completely. Deterministic (a fixed
    # stride over a sorted listing), bounded, and it knows nothing about WHICH
    # documents an implementation treats how.
    stride = max(1, len(listed) // SAMPLE)
    sample = listed[::stride][:SAMPLE]
    before = {document.key: (Path(resolved.location) / document.key).read_bytes()
              for document in sample
              if (Path(resolved.location) / document.key).is_file()}

    dispatches_before = None if witness is None else witness()

    forgeries = [
        ("renamed", replace(resolved, write_path="a-path-this-adapter-never-declared",
                            write_path_available=True)),
    ]
    if not resolved.write_path_available:
        forgeries.insert(0, ("available",
                             replace(resolved, write_path_available=True)))
    for label, forged in forgeries:
        for document in sample:
            try:
                adapter.write_back(forged, document, b"forged\n", actor="forger",
                                   basis_revision=resolved.revision or "0" * 40)
            except CorpusRefused:
                continue
            except Exception as unexpected:        # noqa: BLE001 - that is the point
                raise AssertionError(
                    f"the {label} forgery over {document.key} raised "
                    f"{type(unexpected).__name__} rather than refusing: "
                    f"{unexpected}. Reachability must be the adapter's own "
                    "answer, so a forged reference meets a REFUSAL and not the "
                    "inside of a dispatch") from unexpected
            else:
                raise AssertionError(
                    f"the {label} forgery over {document.key} was accepted. A "
                    "reference the adapter did not issue must never open the "
                    "governed write path")
    for key, bytes_before in before.items():
        assert (Path(resolved.location) / key).read_bytes() == bytes_before, (
            f"a forged write changed {key} on disk")
    if witness is not None:
        assert witness() == dispatches_before, (
            "a forged reference reached the dispatcher. It refused afterwards, "
            "which is worse than not refusing at all: the governed path was "
            "already entered")


# -- the standard ----------------------------------------------------------


def test_the_interface_declares_itself_provisional():
    """RULING OQ-1 (2026-09-06, YES).

    The operation names, arguments and return shapes belong to openDox's own
    governance instance under RULING Q4 and are ratified there, while § 2.2
    requires them landed in-tree NOW — reconcilable only if what landed says it
    is provisional. The marker is machine-readable so it cannot be dropped in
    silence when the real ratification happens."""
    assert "provisional" in INTERFACE_PROVENANCE.lower()
    assert "openDox" in INTERFACE_PROVENANCE, (
        "the marker must name WHO ratifies the signatures; without that it is "
        "a disclaimer rather than a provenance statement")
    assert "openxFactory" in INTERFACE_PROVENANCE, (
        "and WHAT openxFactory authors instead — the terms of consumption")


@pytest.mark.parametrize("name", IDS)
def test_the_adapter_satisfies_the_interface(name):
    adapter, _ref = dict(FACTORIES)[name]()
    assert isinstance(adapter, CorpusAdapter), (
        "structural conformance is the whole point of the seam: an "
        "implementation authored in another repository must satisfy this "
        "without importing anything from openxFactory")


@pytest.mark.parametrize("name", IDS)
def test_resolve_answers_scopes_and_write_terms_up_front(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    assert isinstance(resolved, ResolvedCorpus)
    assert Path(resolved.location).is_absolute()
    assert SCOPE_ALL in resolved.scopes, (
        f"every implementation accepts {SCOPE_ALL!r}")
    assert len(set(resolved.scopes)) == len(resolved.scopes), (
        "a scope name announced twice would make a caller list twice")
    if resolved.write_path is None:
        assert resolved.write_path_available is False, (
            "a corpus with no declared path cannot have an available one")
    # A corpus that carries no revision notion resolves to None, and that is
    # legal — not every corpus is a git checkout.
    assert resolved.revision is None or isinstance(resolved.revision, str)


@pytest.mark.parametrize("name", IDS)
def test_an_absent_checkout_refuses_rather_than_listing_nothing(name, tmp_path):
    adapter, _ref = dict(FACTORIES)[name]()
    check_absent_corpus_refuses_and_names_it(adapter, tmp_path / "nowhere")


def test_a_path_that_is_not_a_directory_refuses_as_unreadable():
    """`corpus_root.corpus_scan_defect`'s second defect, reachable without
    `chmod` — which is unreliable when the suite runs as root on CI."""
    adapter = adapter_for(NOT_A_DIRECTORY)
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.resolve(CorpusRef(name="file", location=str(NOT_A_DIRECTORY)))
    assert refusal_kind(excinfo) == CORPUS_UNREADABLE
    assert str(NOT_A_DIRECTORY) in excinfo.value.refusal.subject


def test_an_empty_corpus_is_an_answer_and_not_a_refusal():
    """Requirement 2, scenario 3 — the distinction the whole requirement is
    about: "so that a consumer can tell 'nothing there' from 'could not look'"."""
    adapter, ref = dict(FACTORIES)[EMPTY_ID]()
    resolved = adapter.resolve(ref)          # reached WITHOUT an exception
    assert adapter.list_documents(resolved, SCOPE_ALL) == ()


@pytest.mark.parametrize("name", IDS)
def test_listings_are_sorted_unique_and_stable(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    first = adapter.list_documents(resolved, SCOPE_ALL)
    keys = [doc.key for doc in first]
    assert keys == sorted(keys), "a listing is sorted"
    assert len(set(keys)) == len(keys), "a document listed twice doubles every "\
        "finding it carries"
    assert all(doc.corpus == resolved.ref.name for doc in first), (
        "an identity names the corpus it belongs to")
    # Stability is asserted against a FRESH adapter, so an implementation that
    # merely remembers its own last answer cannot pass it.
    fresh, fresh_ref = dict(FACTORIES)[name]()
    assert adapter.list_documents(fresh.resolve(fresh_ref), SCOPE_ALL) == first


@pytest.mark.parametrize("name", IDS)
def test_an_undeclared_scope_refuses(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.list_documents(resolved, "no-such-scope")
    assert refusal_kind(excinfo) == SCOPE_UNKNOWN


@pytest.mark.parametrize("name", IDS)
def test_every_declared_scope_is_listable_and_contained_by_all(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    everything = {doc.key for doc in adapter.list_documents(resolved, SCOPE_ALL)}
    for scope in resolved.scopes:
        keys = {doc.key for doc in adapter.list_documents(resolved, scope)}
        assert keys <= everything, (
            f"scope {scope!r} returned documents {SCOPE_ALL!r} did not")


@pytest.mark.parametrize("name", IDS)
def test_read_round_trips_and_refuses_what_it_cannot_serve(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    listed = adapter.list_documents(resolved, SCOPE_ALL)
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.read(resolved,
                     DocumentId(corpus=resolved.ref.name, key="no/such/document"))
    assert refusal_kind(excinfo) == DOCUMENT_UNKNOWN
    if not listed:
        return
    document = adapter.read(resolved, listed[0])
    assert isinstance(document, Document)
    assert isinstance(document.content, bytes)
    assert document.revision == resolved.revision, (
        "a read reports the revision it was served at")
    assert document.content == (Path(resolved.location) / listed[0].key).read_bytes()
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.read(resolved, listed[0], revision="f" * 40)
    assert refusal_kind(excinfo) == REVISION_UNKNOWN, (
        "a revision the adapter cannot serve refuses; it never falls back "
        "silently to the one it has")


@pytest.mark.parametrize("name", IDS)
def test_classify_reports_an_unrecognizable_document_and_still_lists_it(name):
    """Requirement 2, scenario 2 — the asymmetry that catches readers out.

    An unresolvable CORPUS refuses. An unrecognizable DOCUMENT is REPORTED and
    stays in the listing: "it reports the document as unclassifiable and names
    it, rather than omitting it from the listing"."""
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    listed = adapter.list_documents(resolved, SCOPE_ALL)
    for document in listed[:SAMPLE]:
        result = adapter.classify(resolved, document)
        assert isinstance(result, Classification)
        assert result.id == document
        assert set(result.missing_fields) <= set(result.required_fields), (
            "a field can only be missing if it was required")
        if result.kind is None:
            assert result.unclassifiable, (
                f"{document.key} has no kind and no reason — one of the two "
                "must be present")
            assert document.key in result.unclassifiable, (
                "the reason must NAME the document")
            assert document in listed, "and the document stays listed"
        else:
            assert result.unclassifiable is None


def test_the_suite_actually_meets_an_unclassifiable_document():
    """Non-vacuity for the test above: a suite whose corpora were all perfectly
    classifiable would assert nothing about the scenario it names."""
    seen = 0
    for name, factory in FACTORIES:
        adapter, ref = factory()
        resolved = adapter.resolve(ref)
        for document in adapter.list_documents(resolved, SCOPE_ALL)[:SAMPLE]:
            if adapter.classify(resolved, document).kind is None:
                seen += 1
    assert seen, (
        "no corpus in this suite holds a document its reader cannot classify, "
        "so the report-rather-than-omit rule is untested. The neutral corpus "
        "carries one deliberately")


@pytest.mark.parametrize("name", IDS)
def test_check_answers_with_findings_the_interface_can_carry(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    known = {doc.key for doc in adapter.list_documents(resolved, SCOPE_ALL)}
    findings = adapter.check(resolved)
    assert isinstance(findings, tuple), (
        "a corpus with no verdict machinery returns an empty result — an "
        "ANSWER, not a refusal, and not a claim of cleanliness")
    for finding in findings:
        assert finding.severity in SEVERITIES, (
            f"{finding.severity!r} is outside the interface's severity "
            f"vocabulary {SEVERITIES}")
        assert finding.subject in known or finding.subject == resolved.ref.name, (
            f"a finding's subject is a listed document or the corpus itself; "
            f"got {finding.subject!r}")
        assert finding.code and finding.message


@pytest.mark.parametrize("name", IDS)
def test_check_refuses_a_subject_the_corpus_does_not_list(name):
    adapter, ref = dict(FACTORIES)[name]()
    resolved = adapter.resolve(ref)
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.check(resolved, (DocumentId(corpus=resolved.ref.name,
                                            key="no/such/document"),))
    assert refusal_kind(excinfo) == DOCUMENT_UNKNOWN, (
        "a verdict that quietly checked less than it was asked to is a false "
        "green")


@pytest.mark.parametrize("name", IDS)
def test_write_back_never_writes_the_corpus_tree(name):
    adapter, ref = dict(FACTORIES)[name]()
    check_write_back_honours_what_resolve_declared(adapter, ref)


@pytest.mark.parametrize("name", IDS)
def test_a_forged_reference_cannot_open_the_write_path(name):
    adapter, ref = dict(FACTORIES)[name]()
    check_a_forged_reference_cannot_open_the_write_path(
        adapter, ref, witness=lambda: dispatches_recorded(name))


def test_a_reachable_write_path_dispatches_once_and_only_for_its_own_name():
    """The branch every other fixture leaves untested: the path is OPEN.

    Both sides of the same fixture, in order, because each is the other's
    control. FIRST a legitimate `resolve()` + `write_back` must actually
    dispatch — otherwise "it refused" proves nothing, since a corpus that
    refuses everything would pass every assertion about refusing. THEN the SAME
    document under a reference naming a path this adapter does not serve must
    refuse, and the dispatcher must not move.

    Without this, a mismatched path name is caught only by the availability
    guard sitting behind it, and deleting the mismatch check leaves a green
    suite — measured, which is why this test exists.
    """
    adapter, ref = dict(FACTORIES)[DISPATCHABLE_ID]()
    resolved = adapter.resolve(ref)
    assert resolved.write_path is not None and resolved.write_path_available, (
        "this fixture's whole purpose is a write path that is genuinely open")

    listed = adapter.list_documents(resolved, SCOPE_ALL)
    stride = max(1, len(listed) // SAMPLE)
    sample = listed[::stride][:SAMPLE]
    baseline = dispatches_recorded(DISPATCHABLE_ID)
    assert baseline == 0

    # 1. a legitimate write DISPATCHES.
    accepted, receipt = None, None
    for document in sample:
        try:
            receipt = adapter.write_back(
                resolved, document, b"a proposed body\n", actor="conformance-suite",
                basis_revision=resolved.revision or "0" * 40, reason="conformance")
        except CorpusRefused:
            continue                      # no target on this path; try the next
        accepted = document
        break
    assert accepted is not None, (
        "the fixture must hold at least one document its own write path "
        "accepts, or the refusal in step 2 proves nothing")
    assert receipt.dispatched_to == resolved.write_path
    assert receipt.correlation_id
    assert dispatches_recorded(DISPATCHABLE_ID) == baseline + 1, (
        "a receipt was returned without the path being entered")

    on_disk = Path(resolved.location) / accepted.key
    bytes_after_dispatch = on_disk.read_bytes()

    # 2. the SAME document, under a reference naming another path, must refuse
    #    — and must not reach the dispatcher on its way there.
    forged = replace(resolved, write_path="a-path-this-adapter-never-declared")
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.write_back(forged, accepted, b"forged\n", actor="forger",
                           basis_revision=resolved.revision or "0" * 40)
    assert excinfo.value.refusal.kind == WRITE_PATH_UNREACHABLE
    assert dispatches_recorded(DISPATCHABLE_ID) == baseline + 1, (
        "the forged name reached the dispatcher: a reference naming a path this "
        "adapter does not serve was dispatched through the one it holds")
    assert on_disk.read_bytes() == bytes_after_dispatch, (
        "and a DISPATCHED write still never touches the corpus tree")


# -- the teeth --------------------------------------------------------------


class ForgivingAdapter:
    """DELIBERATELY NON-CONFORMANT: it degrades instead of refusing.

    This is the failure the second requirement was written from — every scan in
    the projection individually forgiving, so a wrong path produced a written,
    exit-0, entirely empty snapshot and nothing downstream could tell an empty
    corpus from a wrong one (T092)."""

    def resolve(self, ref):
        return ResolvedCorpus(ref=ref, location=ref.location, revision=None,
                              scopes=(SCOPE_ALL,), write_path=None,
                              write_path_available=False)

    def list_documents(self, corpus, scope=SCOPE_ALL):
        return ()

    def read(self, corpus, document, revision=None):
        return Document(id=document, content=b"", revision=None)

    def classify(self, corpus, document):
        return Classification(id=document, kind=None, required_fields=(),
                              missing_fields=())

    def check(self, corpus, subjects=None):
        return ()

    def write_back(self, corpus, document, content, *, actor, basis_revision,
                   reason=""):
        return WriteReceipt(correlation_id="", dispatched_to="")


class TreeWritingAdapter(ForgivingAdapter):
    """DELIBERATELY NON-CONFORMANT: its write-back writes the corpus tree.

    The identical-bytes case is the one the requirement calls out by name, so
    this one writes bytes a caller genuinely proposed — and it must still fail."""

    def __init__(self, location, key):
        self._location, self._key = Path(location), key

    def resolve(self, ref):
        return ResolvedCorpus(ref=ref, location=str(self._location),
                              revision=None, scopes=(SCOPE_ALL,),
                              write_path=None, write_path_available=False)

    def list_documents(self, corpus, scope=SCOPE_ALL):
        return (DocumentId(corpus=corpus.ref.name, key=self._key),)

    def read(self, corpus, document, revision=None):
        return Document(id=document,
                        content=(self._location / document.key).read_bytes(),
                        revision=None)

    def write_back(self, corpus, document, content, *, actor, basis_revision,
                   reason=""):
        (self._location / document.key).write_bytes(content)
        return WriteReceipt(correlation_id="written", dispatched_to="the tree")


def test_the_suite_fails_an_adapter_that_forgives_an_absent_corpus(tmp_path):
    """The strongest negative control there is: run the suite's own fail-closed
    check against an adapter built to break it, and require the FAILURE."""
    with pytest.raises(AssertionError):
        check_absent_corpus_refuses_and_names_it(
            ForgivingAdapter(), tmp_path / "nowhere")


def test_the_suite_fails_an_adapter_that_writes_the_corpus_tree(tmp_path):
    (tmp_path / "notes").mkdir()
    target = tmp_path / "notes" / "alpha.md"
    target.write_bytes(b"Type: note\nTitle: Alpha\n")
    adapter = TreeWritingAdapter(tmp_path, "notes/alpha.md")
    with pytest.raises(AssertionError):
        check_write_back_honours_what_resolve_declared(
            adapter, CorpusRef(name="written-over", location=str(tmp_path)))


def test_the_two_counterexamples_would_otherwise_look_conformant():
    """Both satisfy the Protocol. That is the point: structural conformance is
    a shape check, and the suite is what makes it a behaviour check."""
    assert isinstance(ForgivingAdapter(), CorpusAdapter)
    assert isinstance(TreeWritingAdapter(".", "x"), CorpusAdapter)
