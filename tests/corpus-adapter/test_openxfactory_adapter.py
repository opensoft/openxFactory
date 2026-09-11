"""The home adapter's parities — deliberately OUTSIDE the neutral suite.

`test_conformance.py` proves the adapter obeys the interface over corpora it
does not own. This file proves the other half: that what it says about THIS
corpus is the same thing this corpus's own tooling says. Every test here is a
PARITY, and each one exists because the alternative was a co-authoritative
constant — the pattern this repository spends real effort killing (`tasks.md`
§ 2.3 exists to kill one, and `contracts/avatar-client/interface-lock.yaml`
records the same fix for a hand-mirrored file: "the hand-mirroring that made
this file drift-prone now fails closed").

It is a separate file because these assertions are NOT part of the standard and
must not travel with it. Handing `test_conformance.py` to openDox at § 3.7 is a
move; this file stays here with the adapter it pins.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

# #872 (RULED OQ-Q): same reason as `test_conformance.py` — the adapter's
# dataclasses now come from the pinned openDox copy, so this file's parities
# must import the same copy.
_OPENDOX_SRC = REPO_ROOT / "openDox" / "code" / "src"
if not (_OPENDOX_SRC / "opendox" / "corpus_adapter.py").is_file():
    raise ImportError(
        "test_openxfactory_adapter: the pinned openDox corpus-adapter interface "
        f"is not at {_OPENDOX_SRC / 'opendox' / 'corpus_adapter.py'}. Run `git "
        "submodule update --init --recursive openDox` from the repository "
        "root.")
sys.path.insert(0, str(_OPENDOX_SRC))

from opendox.corpus_adapter import (  # noqa: E402
    REVISION_UNKNOWN,
    SCOPE_ALL,
    WRITE_PATH_UNREACHABLE,
    CorpusRef,
    CorpusRefused,
    DocumentId,
    Finding,
)
from corpus_adapter_openxfactory import OpenxFactoryCorpusAdapter, home_corpus  # noqa: E402
from corpus_adapter_openxfactory.check import doc_health_verdict  # noqa: E402
from corpus_adapter_openxfactory.home import (  # noqa: E402
    DOCUMENTS,
    HOME_SHAPE,
    LIFECYCLE,
    home_shape,
)
from corpus_adapter_openxfactory.shape import WriteProposal  # noqa: E402
from corpus_adapter_openxfactory.write_path import (  # noqa: E402
    APPLY_LANE_NAME,
    apply_lane_write_path,
    build_gate_intent,
    packet_target,
)

from doc_health import DEFAULT_THRESHOLDS, corpus  # noqa: E402
from doc_health.families import FAMILIES  # noqa: E402
from doc_health.runner import Context, run_suite  # noqa: E402
from opendox import authoring  # noqa: E402
from openxdox import corpus_root  # noqa: E402
from ideation_dashboard.intent_apply_lane import (  # noqa: E402
    LANE_DEFERRED_VERBS,
    request_digest,
    shape_error,
)

import header_contract_oracle as oracle  # noqa: E402
from import_scan import imported_modules  # noqa: E402

PACKAGE = REPO_ROOT / "scripts" / "corpus_adapter_openxfactory"
#: The check grouping the mapping test uses: it reads documents and the
#: lifecycle scan set and nothing else, so a fixture repo needs no git.
HEADER_GROUP = "status-validity"


@pytest.fixture(scope="module")
def home():
    built = home_corpus()
    return built.adapter, built.adapter.resolve(built.ref)


# -- the shape is the same shape the corpus's own readers use ---------------


def test_the_scan_roots_are_the_roots_a_projection_is_built_from(home):
    """RULING OQ-4's mitigation, and the reason the duplication is tolerable.

    The adapter carries its own structural resolution rather than importing
    `corpus_root.corpus_scan_defect` — importing it would make this permanent
    adapter depend on a package whose destiny is unsettled, and repointing
    `corpus_root` at the adapter reaches `cli.py`'s `--repo-root` and
    `serve.py`'s `--checkout-root`, which is § 2.4's critical path. The price is
    two definitions of one predicate, for now; this assertion is what makes that
    price a DECLARED debt rather than a silent divergence. The collapse is filed
    to § 2.4."""
    assert HOME_SHAPE.scan_roots == corpus_root.SCANNED_ROOTS, (
        "the adapter and the entrypoint guard must agree on what makes a tree "
        "this corpus. They are two definitions of one predicate until § 2.4 "
        f"collapses them: adapter={HOME_SHAPE.scan_roots} "
        f"corpus_root={corpus_root.SCANNED_ROOTS}")


def test_the_two_scopes_are_the_two_sets_their_owning_functions_return(home):
    """Byte-for-byte parity with `iter_doc_paths` and `iter_lifecycle_paths`.

    Not a re-derivation of the membership rules: the same rules, read through a
    `CorpusShape`, asserted equal to what the functions that own them return.
    Anything that changes there and not here goes red."""
    adapter, resolved = home
    location = Path(resolved.location)
    documents = {doc.key for doc in adapter.list_documents(resolved, DOCUMENTS)}
    lifecycle = {doc.key for doc in adapter.list_documents(resolved, LIFECYCLE)}
    assert documents == {p.as_posix() for p in corpus.iter_doc_paths(location)}
    assert lifecycle == {p.as_posix()
                         for p in corpus.iter_lifecycle_paths(location)}


def test_the_two_scopes_are_distinct_and_are_never_merged(home):
    """`govern-openspec-corpus-membership` OQ-2, ruled 2026-08-23.

    The lifecycle scan set is an EXPLICIT PATTERN SET, not a directory rule: a
    directory rule "would have swept in `tasks.md`, `design.md`, the spec
    deltas, `supporting-docs/` and `evidence/`" — 488 of the 536 fires the
    full-membership option measured — and whether those are governance documents
    the ruling explicitly left open. Two scopes, never a union."""
    adapter, resolved = home
    documents = {doc.key for doc in adapter.list_documents(resolved, DOCUMENTS)}
    lifecycle = {doc.key for doc in adapter.list_documents(resolved, LIFECYCLE)}
    assert lifecycle - documents, (
        "the lifecycle scan set must reach documents the governed corpus does "
        "not, or the two scopes have collapsed into one")
    assert not any(key.startswith("openspec/") for key in documents), (
        "the governed corpus does not walk the packet root; only the lifecycle "
        "scan set's two ruled globs reach into it")
    assert set(resolved.scopes) == {SCOPE_ALL, DOCUMENTS, LIFECYCLE}


def test_all_is_the_union_of_the_declared_scopes(home):
    adapter, resolved = home
    everything = {doc.key for doc in adapter.list_documents(resolved, SCOPE_ALL)}
    documents = {doc.key for doc in adapter.list_documents(resolved, DOCUMENTS)}
    lifecycle = {doc.key for doc in adapter.list_documents(resolved, LIFECYCLE)}
    assert everything == documents | lifecycle


# -- classify says what the corpus's own header readers say -----------------


def test_the_required_field_table_is_the_contract_it_always_was():
    """§ 2.3, LANDED: the table is the authority now, and it is unchanged.

    Until § 2.3 this assertion read the other way round — the table MIRRORED
    `authoring.REQUIRED_HEADER_FIELDS`, which was the constant. The migration
    inverted it: the field block is a fact about this corpus's shape, the create
    gate asks `classify` for it, and deriving the table from the gate would now
    be a cycle rather than a derivation. Two things must therefore hold, and
    they are different things:

      * the contract did not CHANGE while its authorship moved — measured
        against the frozen pre-migration answer, not against the consumer, which
        would be a tautology now that the consumer's answer comes from here;
      * the two things that could not be derived either way still agree with the
        readers that own them: the tree the create path writes into, and the
        window the corpus's own header readers scan.
    """
    assert HOME_SHAPE.required_fields_by_kind[None] == oracle.FIELDS, (
        "the header block this corpus obliges is not the block it obliged "
        "before § 2.3 — the migration was a re-derivation of one contract, not "
        "a change to it")
    assert HOME_SHAPE.obliged_prefixes == (authoring.IDEATION_PREFIX,), (
        "the header block governs the tree the create path enforces it over, "
        "and reporting a document outside it as field-incomplete would be a "
        "false finding. Two definitions of one tree, pinned here because the "
        "import that used to make them one would now be a cycle")
    assert HOME_SHAPE.header_scan_lines == corpus.STATUS_SCAN_LINES


def test_the_authoring_gate_now_answers_out_of_this_table():
    """The other end of § 2.3, asserted where the table lives.

    `tests/ideation-dashboard/test_authoring_classify_derivation.py` proves the
    direction (no assignment survives, and a different table changes the gate's
    answer). This is the cheap standing check that the two ends are wired to
    each other at all — a broken wiring would otherwise show up only as a gate
    that quietly stopped following the corpus."""
    assert tuple(authoring.REQUIRED_HEADER_FIELDS) == \
        HOME_SHAPE.required_fields_by_kind[None]


def test_classify_agrees_with_the_corpus_own_header_readers(home):
    """The nine-reader problem, not made ten.

    `align-status-reader-to-real-lines` found ten Python spellings of "what is
    a line" over this header window, disagreeing with each other, and the damage
    was FALSE FINDINGS. So `classify` is asserted against `parse_kind` and the
    field reader over real documents rather than merely written to look like
    them.

    THE FIELD HALF MEASURES AGAINST THE FROZEN ORACLE, NOT AGAINST THE CALLER.
    It used to compare with `authoring.missing_required_headers`; since § 2.3
    that function IS this call, so the comparison would be a function against
    itself. `tests/header_contract_oracle.py` holds the answer that reader gave
    before the migration, so the parity keeps measuring the same thing it always
    did: this reader against the one the corpus trusted."""
    adapter, resolved = home
    location = Path(resolved.location)
    sample = [doc for doc in adapter.list_documents(resolved, DOCUMENTS)
              if doc.key.startswith(authoring.IDEATION_PREFIX)][:40]
    assert len(sample) >= 20, (
        f"only {len(sample)} documents sampled — the parity is not being "
        "measured over a real population")
    for document in sample:
        text = (location / document.key).read_text(encoding="utf-8",
                                                   errors="replace")
        result = adapter.classify(resolved, document)
        assert result.kind == corpus.parse_kind(text), document.key
        assert result.missing_fields == \
            tuple(oracle.missing_required_headers(text)), document.key
        # `Status` is one of the required fields, so the field reader and the
        # status reader must agree about its presence too.
        assert ("Status" in result.missing_fields) is \
            (corpus.parse_status(text) is None), document.key


def test_classify_finds_a_header_on_the_last_real_line_of_the_window(tmp_path):
    """The `align-status-reader-to-real-lines` invariant, as a fixture.

    A document whose header carries an exotic separator (U+2028) has MORE
    `str.splitlines()` fragments than real lines, so a naive reader's fifteen-
    line window ends before a `Status:` that is plainly on real line fifteen —
    and reports a correct document as lacking a header it carries. That is a
    false finding, which "costs more trust than a crash". The adapter scans real
    lines (CR/LF/CRLF only) through the shared rule, so it sees it."""
    topic = tmp_path / authoring.IDEATION_PREFIX / "staging" / "topic"
    topic.mkdir(parents=True)
    body = [
        "# Late Header — Brainstorm",
        "",
        "Kind: note",
        "Summary: one sentence with an exotic separator inside it",
        "Topics: parity",
        "Repository context: openxFactory",
        "Captured: 2026-09-06",
        "", "", "", "", "", "", "",
        "Status: staged",
    ]
    assert len(body) == corpus.STATUS_SCAN_LINES, (
        "the fixture must place the header on the LAST real line of the window")
    text = "\n".join(body) + "\n"
    document = topic / "late-header.md"
    document.write_text(text, encoding="utf-8")
    assert len(text.splitlines()) > corpus.STATUS_SCAN_LINES, (
        "the fixture must be one a naive splitter would mis-window, or it "
        "proves nothing")

    adapter = OpenxFactoryCorpusAdapter(HOME_SHAPE)
    resolved = adapter.resolve(CorpusRef(name="fixture", location=str(tmp_path)))
    key = document.relative_to(tmp_path).as_posix()
    result = adapter.classify(resolved, DocumentId(corpus="fixture", key=key))
    assert result.kind == "note"
    assert result.missing_fields == (), (
        f"the header is complete on real lines; the reader reported "
        f"{result.missing_fields} missing")
    assert corpus.parse_status(text) == "staged"


def test_a_document_with_no_kind_header_is_reported_not_omitted(tmp_path):
    topic = tmp_path / authoring.IDEATION_PREFIX / "staging" / "topic"
    topic.mkdir(parents=True)
    (topic / "kindless.md").write_text("Status: staged\n\n# Kindless\n",
                                       encoding="utf-8")
    adapter = OpenxFactoryCorpusAdapter(HOME_SHAPE)
    resolved = adapter.resolve(CorpusRef(name="fixture", location=str(tmp_path)))
    listed = adapter.list_documents(resolved, SCOPE_ALL)
    key = "ideation/staging/topic/kindless.md"
    assert [doc.key for doc in listed] == [key], "it stays in the listing"
    result = adapter.classify(resolved, listed[0])
    assert result.kind is None and result.unclassifiable
    assert key in result.unclassifiable, "the reason names the document"
    assert "Kind" in result.missing_fields, (
        "and the absent kind header is also an absent required field, which is "
        "why the default row of the table covers an unclassifiable document too")


# -- resolving a revision ---------------------------------------------------


def test_an_unversioned_tree_has_no_revision_and_that_is_legal(tmp_path):
    """`None` is a legitimate answer, and this is the ONLY thing it may mean."""
    (tmp_path / authoring.IDEATION_PREFIX).mkdir(parents=True)
    adapter = OpenxFactoryCorpusAdapter(HOME_SHAPE)
    resolved = adapter.resolve(CorpusRef(name="plain", location=str(tmp_path)))
    assert resolved.revision is None
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.resolve(CorpusRef(name="plain", location=str(tmp_path),
                                  revision="a" * 40))
    assert excinfo.value.refusal.kind == REVISION_UNKNOWN, (
        "a tree with no revisions refuses a caller who names one, rather than "
        "serving the bytes of something else")


def test_a_versioned_tree_whose_ref_will_not_resolve_refuses(tmp_path):
    """An UNBORN HEAD: initialized, nothing committed. Seam requirement 2.

    The marker is present, so this corpus HAS a revision notion; `HEAD` simply
    resolves to nothing yet. Answering `None` here would be a degradation
    wearing a legitimate answer's clothes — indistinguishable from the plain
    directory tree in the test above, and every subsequent `read` would stamp
    its bytes with a revision of `None`. An unresolvable corpus refuses, and it
    names the ref it could not resolve."""
    (tmp_path / authoring.IDEATION_PREFIX).mkdir(parents=True)
    initialized = subprocess.run(["git", "init", "-q", str(tmp_path)],
                                 capture_output=True, text=True)
    assert initialized.returncode == 0, initialized.stderr
    assert (tmp_path / ".git").exists(), "the fixture must carry a version marker"
    assert corpus.RealGit().resolve_ref(tmp_path, "HEAD") is None, (
        "the fixture must have an UNBORN HEAD, or it proves nothing")

    adapter = OpenxFactoryCorpusAdapter(HOME_SHAPE)
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.resolve(CorpusRef(name="unborn", location=str(tmp_path)))
    assert excinfo.value.refusal.kind == REVISION_UNKNOWN
    assert excinfo.value.refusal.subject == "HEAD", (
        "the DEFAULT ref is refused by name for the same reason a requested one "
        f"is; got {excinfo.value.refusal.subject!r}")


# -- the verdict mapping ----------------------------------------------------


def test_findings_map_one_to_one_onto_the_neutral_shape(tmp_path):
    """`doc_health.Finding` -> `corpus_adapter.Finding`, over a fixture repo.

    Compared against `run_suite`'s own output rather than against a hand-written
    expectation, so the mapping is pinned and the CONTENT of the findings is
    whatever this corpus's checker says it is."""
    root = tmp_path / "fixture-repo"
    (root / "ideation" / "staging" / "topic").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "ideation" / "staging" / "topic" / "no-status.md").write_text(
        "# No Status — Brainstorm\n\nKind: note\n", encoding="utf-8")
    (root / "docs" / "fine.md").write_text(
        "Status: standard\nKind: reference\n\n# Fine\n", encoding="utf-8")

    name = root.name
    expected = run_suite(Context(
        repo_paths={name: root},
        docs=corpus.load_docs(name, root),
        capabilities={name: corpus.spec_capabilities(root)},
        change_ids={name: corpus.change_ids(root)},
        git=corpus.RealGit(),
        thresholds=dict(DEFAULT_THRESHOLDS),
        as_of=date.today(),
        agg_root=None,
        lifecycle_docs=corpus.load_lifecycle_docs(name, root),
    ), HEADER_GROUP, set()).findings

    adapter = OpenxFactoryCorpusAdapter(home_shape(verdict_groups=(HEADER_GROUP,)))
    resolved = adapter.resolve(CorpusRef(name=name, location=str(root)))
    known = {doc.key for doc in adapter.list_documents(resolved, SCOPE_ALL)}
    mapped = adapter.check(resolved)

    assert expected, "the fixture must actually provoke a finding"
    assert len(mapped) == len(expected), (
        f"{len(expected)} findings became {len(mapped)} — the mapping is 1:1")
    for neutral, original in zip(mapped, expected):
        assert isinstance(neutral, Finding)
        assert neutral.severity == original.severity, "severities pass through"
        assert neutral.code == f"{original.family}/{original.rule}", (
            "the grouping and the rule ride inside the OPAQUE code, which is "
            "how the interface stays ignorant of this corpus's taxonomy")
        if original.path in known:
            assert neutral.subject == original.path
            assert neutral.message == original.action
        else:
            assert neutral.subject == name, (
                "a finding about something the listing does not hold is a "
                "corpus-wide finding")
            assert original.path in neutral.message, "and its path is not lost"


def test_an_unknown_check_grouping_is_refused_at_construction():
    with pytest.raises(ValueError) as excinfo:
        doc_health_verdict(groups=("no-such-grouping",))
    assert "no-such-grouping" in str(excinfo.value)
    assert sorted(FAMILIES)[0] in str(excinfo.value), (
        "the refusal lists what it does know, so an operator can fix it")


def test_ruling_oq2_holds_the_other_classification_vocabularies_out():
    """RULING OQ-2 (2026-09-06, NO).

    The corpus carries two further classification vocabularies over the same
    documents — `doc_health.pin_class`'s three axes and
    `inventory.artifact_type_for`'s two artifact types. Design D2 commits
    `classify` to kind + required fields only, and requirement 4 forbids keeping
    them as home-only extensions if they ARE adapter operations. The ruling is
    that they are OUT and stay checker internals, so the adapter must not even
    reach for them."""
    forbidden = {"doc_health.pin_class", "doc_health.inventory",
                 "doc_health.pin_sentinels"}
    offenders = [
        f"{path.name}:{line} imports {module!r}"
        for path in sorted(PACKAGE.glob("*.py"))
        for module, line in imported_modules(path)
        if module in forbidden
    ]
    assert offenders == [], (
        "the adapter exposes kind + required fields and nothing else; the "
        f"corpus's other classification vocabularies stay internal: {offenders}")


# -- the declared write path ------------------------------------------------


def test_the_declared_write_path_is_named_and_unreachable(home):
    """§ 2.5 made visible in code rather than only in the packet.

    RULING Q1 promotes the apply lane to the only governed write path; the lane
    lists this verb in `LANE_DEFERRED_VERBS` — "the routes layer cannot yet
    execute" them. The conformant answer is requirement 3's own third scenario:
    the write refuses, NAMES the path, and the document remains unsaved."""
    adapter, resolved = home
    assert resolved.write_path == APPLY_LANE_NAME
    assert resolved.write_path_available is False
    assert "edit-apply" in LANE_DEFERRED_VERBS, (
        "if the lane has learned the verb, this adapter's declaration is stale "
        "— flip `apply_lane_write_path(dispatch=...)` and move this test with it")

    document = adapter.list_documents(resolved, SCOPE_ALL)[0]
    on_disk = Path(resolved.location) / document.key
    before = on_disk.read_bytes()
    with pytest.raises(CorpusRefused) as excinfo:
        adapter.write_back(resolved, document, b"proposed",
                           actor="test", basis_revision=resolved.revision)
    assert excinfo.value.refusal.kind == WRITE_PATH_UNREACHABLE
    assert excinfo.value.refusal.subject == APPLY_LANE_NAME
    assert "edit-apply" in excinfo.value.refusal.detail, (
        "the refusal says WHY, naming the verb the lane cannot yet carry")
    assert on_disk.read_bytes() == before, "and nothing was written"


def test_only_a_packet_document_has_a_target_on_the_declared_path():
    """The lane's `edit-apply` verb targets a packet id, so a document outside a
    packet has no target on this path at all. Answering None rather than
    inventing an id is what keeps the refusal honest."""
    assert packet_target("openspec/changes/some-change/proposal.md") == \
        "some-change"
    assert packet_target(
        "openspec/changes/archive/2026-09-01-some-change/proposal.md") == \
        "2026-09-01-some-change"
    assert packet_target("docs/document-lifecycle.md") is None
    assert packet_target("openspec/changes/some-change") is None, (
        "a packet directory is not a document in it")
    assert packet_target("openspec/changes/../escape/proposal.md") is None, (
        "a target that is not one safe segment is refused before a request is "
        "built, exactly as the lane would refuse it on arrival")


def test_hardening_the_lane_is_one_construction_argument(home):
    """§ 2.5's flip, proven WITHOUT dispatching anything.

    The injected dispatcher RECORDS and does nothing: no workflow is invoked by
    this change or its tests. What is proven is that the refusal above is a
    property of the declared path's availability and not of the adapter — flip
    the argument and the same call returns a receipt, over a request the lane's
    own `shape_error` accepts, carrying the lane's own `request_digest` as the
    correlation identifier."""
    adapter, resolved = home
    packet_documents = [doc for doc in adapter.list_documents(resolved, SCOPE_ALL)
                        if packet_target(doc.key)]
    assert packet_documents, "the corpus must hold at least one packet document"
    document = packet_documents[0]
    on_disk = Path(resolved.location) / document.key
    before = on_disk.read_bytes()

    dispatched = []
    # THE FLIP: one construction argument. Nothing in the adapter changes, and
    # the dispatcher below records rather than dispatching — no workflow is
    # invoked by this change or its tests.
    hardened = replace(home_shape(), write_path=apply_lane_write_path(
        dispatch=lambda request, proposal: dispatched.append(request)))
    flipped = OpenxFactoryCorpusAdapter(hardened)
    reresolved = flipped.resolve(CorpusRef(name=resolved.ref.name,
                                           location=resolved.location))
    assert reresolved.write_path_available is True

    receipt = flipped.write_back(reresolved, document, b"a proposed body\n",
                                 actor="test-actor",
                                 basis_revision=reresolved.revision,
                                 reason="the flip")
    assert len(dispatched) == 1
    request = dispatched[0]
    assert shape_error(request) is None, (
        "the request this repository builds must be one the lane would accept")
    assert request["verb"] == "edit-apply"
    assert request["target"] == {"change_id": packet_target(document.key)}
    assert request["args"]["document"] == document.key
    assert receipt.dispatched_to == APPLY_LANE_NAME
    assert receipt.correlation_id == request_digest(dict(request)), (
        "the correlation identifier is the lane's OWN request identity, not a "
        "second one invented here")
    assert on_disk.read_bytes() == before, (
        "a DISPATCHED write still never touches the corpus tree")


def test_a_request_the_lane_would_refuse_is_never_built():
    with pytest.raises(ValueError):
        build_gate_intent(WriteProposal(
            document_key="docs/document-lifecycle.md", content=b"x",
            actor="test", basis_revision="0" * 40))


def test_undecodable_bytes_travel_as_base64_rather_than_being_dropped():
    request = build_gate_intent(WriteProposal(
        document_key="openspec/changes/some-change/proposal.md",
        content=b"\xff\xfe not utf-8", actor="test",
        basis_revision="a" * 40, reason="binary"))
    assert "content" not in request["args"]
    assert request["args"]["content_base64"]
    assert request["args"]["content_sha256"]
    assert shape_error(request) is None
