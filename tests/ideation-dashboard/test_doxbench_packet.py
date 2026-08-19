"""The BOUNDED CONTEXT PACKET, its rails, and the three-layer compression
stack (add-doxbench-editing-phase-b, design §3.1–§3.4, tasks 10.3, 10.4, 10.5,
10.7).

Every scenario of the delta's knowledge-service requirement that concerns the
PACKET is here, plus every scenario of its compression requirement that this
slice owns. What the file is careful about:

  * the RAIL ORDER is observed rather than asserted about — a recording
    boundary reports what it was handed and when, so "the confinement is
    computed before the provider is reached" is a fact about a call, not a
    comment;
  * a refusal is checked for what it does NOT say: no packet content reaches a
    bounds refusal, and nothing is truncated to make one go away;
  * the lifecycle-status read is cross-checked against the repository's own
    doc-health corpus reader over REAL documents, because the same rule living
    in two places is how two places drift; and
  * layer three is NOT implemented here, so the tests pin its absence and the
    fidelity vocabulary rather than pretending otherwise.

MIRRORING LANDS LATER. Nothing writes a turn into a sidecar until §11 (tasks
9.2/9.5 are "route unwired" by design), so the threads below are constructed
directly. That is exactly the seam §11 fills: the packet carries a thread when
one exists and DECLARES the absence when it does not, and both halves are
pinned here so the later slice has something to satisfy.
"""

from __future__ import annotations

import dataclasses

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_threads as dt  # noqa: E402
from ideation_dashboard.doxbench_scope import (  # noqa: E402
    ScopeKey, ScopeProjection,
)

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_packet.py")

TILE = "demo-topic"
OUTLINE = f"ideation/staging/{TILE}/{TILE}.md"
DOC_A = f"ideation/staging/{TILE}/alpha.md"
DOC_B = f"ideation/staging/{TILE}/beta.md"
DOC_C = f"ideation/staging/{TILE}/gamma.md"
DOC_D = f"ideation/staging/{TILE}/delta.md"
EVIDENCE_RATIFIED = f"ideation/staging/{TILE}/ratified-note.md"
EVIDENCE_DRAFT = f"ideation/staging/{TILE}/draft-note.md"
FOREIGN = "ideation/staging/other-topic/foreign.md"

RATIFIED_TEXT = ("Status: ratified\nKind: record\n\n"
                 "The packet assembler applies the exemption itself.\n")
DRAFT_TEXT = ("Status: draft\n\n"
              "A packet assembler proposal that is not yet ratified.\n")
FOREIGN_TEXT = "Status: ratified\n\nSECRET-FOREIGN-MATERIAL packet assembler.\n"

SCOPE = ScopeKey(repository="openxFactory", ref="main", tile_kind="staged",
                 tile_id=TILE)
OTHER_SCOPE = ScopeKey(repository="openxFactory", ref="main",
                       tile_kind="staged", tile_id="another-topic")

THREAD_SCOPE = dt.ThreadScope(repository="openxFactory", tile_kind="staged",
                              tile_id=TILE)


def _projection(context_paths=(OUTLINE, DOC_A, DOC_B, DOC_C, DOC_D,
                               EVIDENCE_RATIFIED, EVIDENCE_DRAFT)):
    return ScopeProjection(
        key=SCOPE, title="Demo topic", keywords=(), source_revision="r" * 40,
        sections=(), context_paths=tuple(context_paths),
        editable_paths=tuple(context_paths), outline_path=OUTLINE,
        active_document_candidates=())


def _thread(document: str, *, goal: str = "Decide the delta type",
            evidence=(EVIDENCE_RATIFIED,), turns=()) -> dt.DocumentThread:
    return dt.DocumentThread(
        document=document, scope=THREAD_SCOPE,
        state=dt.ThreadState(
            active_goal=goal,
            accepted_facts=(dt.AcceptedFact("The tile declares three claims.",
                                            evidence=EVIDENCE_RATIFIED),),
            open_questions=("Which capability owns the delta?",),
            decisions=(dt.ThreadDecision("Keep it staged", "claims unmapped"),),
            evidence_refs=tuple(evidence),
            pending_actions=("Draft the delta-type line.",)),
        turns=turns)


TURN = dt.ThreadTurn(turn_id="t1", model="opaque-local-id",
                     bound_buffer_key=DOC_A,
                     human="What is missing?", assistant="A delta type.")


class RecordingBoundary:
    """A knowledge boundary that RECORDS what it was handed.

    It exists so the rail order can be observed instead of described: the
    confinement it receives is the set the assembler computed, and the calls it
    logs happen after that computation and before any packet exists."""

    def __init__(self, *, sources=None, rogue: str | None = None) -> None:
        self.sources = dict(sources or {})
        self.rogue = rogue
        self.searches: list[dict] = []
        self.fetches: list[tuple[str, frozenset]] = []

    def profile(self):
        return kn.LOCAL_EMBEDDED_PROFILE

    def search(self, query, *, confined_to, limit, thread_signals=frozenset()):
        self.searches.append({"query": query, "confined_to": confined_to,
                              "limit": limit, "thread_signals": thread_signals})
        hits = [kn.RetrievalHit(ref=ref, score=1.0, lexical=1.0, vector=0.0,
                                thread=0.0)
                for ref in sorted(self.sources) if ref in confined_to]
        if self.rogue is not None:
            # A backend that answers OUTSIDE the confinement it was handed.
            hits.append(kn.RetrievalHit(ref=self.rogue, score=9.0, lexical=1.0,
                                        vector=0.0, thread=0.0))
        return tuple(hits[:limit])

    def get_source(self, ref, *, confined_to):
        self.fetches.append((ref, confined_to))
        text = self.sources.get(ref)
        return None if text is None else kn.IndexedSource(ref=ref, text=text)


def _boundary(**kwargs) -> RecordingBoundary:
    return RecordingBoundary(sources={EVIDENCE_RATIFIED: RATIFIED_TEXT,
                                      EVIDENCE_DRAFT: DRAFT_TEXT},
                             **kwargs)


def _clock(start: float = 1000.0):
    return lambda: start


# ===========================================================================
# THE PACKET (task 10.4) — purpose, sources with refs, scope, expiry
# ===========================================================================


def test_a_turn_with_four_documents_loaded_assembles_the_declared_packet():
    """The delta's `A turn is assembled` scenario, verbatim: the selected
    document's thread in full, the other three threads' state headers, and the
    evidence the service selected — with purpose, sources, scope and expiry
    declared."""
    threads = {key: _thread(key, turns=(TURN,))
               for key in (DOC_A, DOC_B, DOC_C, DOC_D)}
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B, DOC_C, DOC_D), query="packet assembler",
        threads=threads, knowledge=_boundary(), already_carried=(OUTLINE,),
        clock=_clock())

    selected = packet.of_kind(pk.SOURCE_SELECTED_THREAD)
    assert [source.ref for source in selected] == [DOC_A]
    assert TURN.human in selected[0].text  # IN FULL: the transcript rides along

    headers = packet.of_kind(pk.SOURCE_THREAD_STATE)
    assert [source.ref for source in headers] == [DOC_B, DOC_C, DOC_D]
    for header in headers:
        assert "## Thread state" in header.text
        assert TURN.human not in header.text  # headers only, no transcripts

    evidence = packet.of_kind(pk.SOURCE_EVIDENCE)
    assert [source.ref for source in evidence] == [EVIDENCE_DRAFT,
                                                   EVIDENCE_RATIFIED]

    assert packet.purpose == pk.PACKET_PURPOSE_CHAT_TURN
    assert packet.scope == SCOPE
    assert packet.expires_at == packet.issued_at + pk.PACKET_TTL_SECONDS
    assert packet.refs() == (DOC_A, DOC_B, DOC_C, DOC_D, EVIDENCE_DRAFT,
                             EVIDENCE_RATIFIED)
    assert packet.provider_id == kn.PROFILE_LOCAL_EMBEDDED


def test_the_packet_is_rejected_for_another_purpose():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    with pytest.raises(pk.PacketPurposeMismatch) as raised:
        pk.require_valid(packet, purpose="doxbench-share-session", scope=SCOPE,
                         now=1001.0)
    assert "request a new packet" in str(raised.value)


def test_the_packet_is_rejected_for_another_scope():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    with pytest.raises(pk.PacketScopeMismatch):
        pk.require_valid(packet, purpose=pk.PACKET_PURPOSE_CHAT_TURN,
                         scope=OTHER_SCOPE, now=1001.0)


def test_the_packet_is_rejected_after_it_expires():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    assert pk.require_valid(packet, purpose=pk.PACKET_PURPOSE_CHAT_TURN,
                            scope=SCOPE, now=1000.0 + pk.PACKET_TTL_SECONDS - 1)
    with pytest.raises(pk.PacketExpired) as raised:
        pk.require_valid(packet, purpose=pk.PACKET_PURPOSE_CHAT_TURN,
                         scope=SCOPE, now=1000.0 + pk.PACKET_TTL_SECONDS)
    assert "re-runs the rails" in str(raised.value)


def test_the_declaration_section_names_every_source_with_its_ref():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler",
        threads={DOC_A: _thread(DOC_A)}, knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    text = pk.declaration_text(packet)
    assert f"purpose: {pk.PACKET_PURPOSE_CHAT_TURN}" in text
    assert f"tile_id={TILE}" in text
    assert "expires: 300 seconds" in text
    for ref in packet.refs():
        assert ref in text


# ===========================================================================
# RAIL 1 — CONFINEMENT, before any provider (task 10.5)
# ===========================================================================


def test_the_confinement_is_computed_from_the_tiles_staged_set():
    projection = _projection()
    assert pk.confined_refs(projection) == frozenset(projection.context_paths)
    assert pk.confined_refs(projection, ("promoted/finding.md",)) == (
        frozenset(projection.context_paths) | {"promoted/finding.md"})


def test_the_provider_is_HANDED_the_confinement_rather_than_trusted_with_one():
    boundary = _boundary()
    pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    assert len(boundary.searches) == 1
    handed = boundary.searches[0]["confined_to"]
    # exactly the tile's staged set, minus what the prompt already carries
    assert handed == frozenset(_projection().context_paths) - {OUTLINE, DOC_A}
    assert FOREIGN not in handed


def test_a_backend_answering_outside_the_confinement_has_it_excluded():
    """The delta's `Evidence outside the staged set is requested` scenario, at
    the assembler: the answer is DROPPED, not trusted because the port
    returned it."""
    boundary = _boundary(rogue=FOREIGN)
    boundary.sources[FOREIGN] = FOREIGN_TEXT
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    assert FOREIGN not in packet.refs()
    for source in packet.sources:
        assert "SECRET-FOREIGN-MATERIAL" not in source.text
    # and it was never even fetched
    assert FOREIGN not in [ref for ref, _ in boundary.fetches]


def test_material_the_prompt_already_carries_is_not_carried_twice():
    boundary = _boundary()
    boundary.sources[DOC_A] = "Status: draft\n\npacket assembler\n"
    boundary.sources[OUTLINE] = "Status: draft\n\npacket assembler\n"
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    evidence_refs = [source.ref for source in packet.of_kind(pk.SOURCE_EVIDENCE)]
    assert DOC_A not in evidence_refs
    assert OUTLINE not in evidence_refs


def test_a_retrieved_document_never_becomes_a_loaded_buffer():
    """"a retrieved document NEVER joins the loaded set" — asserted through the
    STATE AUTHORITY (the turn's own buffer set), not only through the packet.

    On the server the loaded set IS the request's buffer keys, which the
    assembler neither receives as mutable state nor returns: evidence lands in
    evidence sections and nowhere else, and the buffer sections of the assembled
    prompt still enumerate exactly the buffers the request supplied."""
    from ideation_dashboard import doxbench_turns as dtu

    loaded = (DOC_A,)
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=loaded, query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.of_kind(pk.SOURCE_EVIDENCE)  # there IS evidence to confuse
    keys = dtu.prompt_section_keys(loaded, packet=packet)
    buffer_keys = [key for key in keys
                   if key.startswith(dtu.DOCUMENT_BUFFER_SECTION_PREFIX)]
    assert buffer_keys == [dtu.DOCUMENT_BUFFER_SECTION_PREFIX + DOC_A]
    for source in packet.of_kind(pk.SOURCE_EVIDENCE):
        assert (dtu.DOCUMENT_BUFFER_SECTION_PREFIX + source.ref) not in keys


def test_the_assembler_constructs_no_buffer_and_reaches_no_state_route():
    source = MODULE_PATH.read_text(encoding="utf-8")
    for needle in ("TurnBuffer", "doxbench_state", "loadDocument",
                   "setActiveBuffer", "replaceBuffer"):
        assert needle not in source, needle


# ===========================================================================
# RAIL 2 — SELECTION, and the honest absence of a thread
# ===========================================================================


def test_a_loaded_document_with_no_sidecar_is_declared_absent_not_invented():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B), query="packet assembler",
        threads={DOC_B: _thread(DOC_B)}, knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.of_kind(pk.SOURCE_SELECTED_THREAD) == ()
    assert packet.absent_threads == (DOC_A,)
    text = pk.declaration_text(packet)
    assert "no thread exists yet for: " + DOC_A in text
    assert "nothing has been mirrored into those sidecars" in text


def test_the_declaration_states_WHICH_BYTES_the_evidence_is(
):
    """The session's saves land in its WORKTREE; evidence is read from the
    SERVED CHECKOUT. A document saved (or created) in this session is therefore
    eligible evidence at its pre-session bytes, or not indexable at all — so
    the packet names the revision rather than letting a reader assume the
    evidence is the session's own work."""
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.source_revision == "r" * 40
    text = pk.declaration_text(packet)
    assert "evidence bytes are the served checkout at revision" in text
    assert "NOT this session's worktree" in text
    assert "pre-session bytes, or not at all" in text


def test_the_worktree_caveat_survives_a_projection_with_NO_revision():
    """RE-VERIFY NF4. The whole disclosure used to be gated on
    `packet.source_revision`, so a snapshot that declared no revision dropped
    the worktree warning entirely — it vanished exactly where the reader had
    least information about which bytes they were looking at.

    The caveat is now conditional on the packet standing on retrieved bytes at
    all, which is what it warns about; a missing revision is SAID."""
    revisionless = dataclasses.replace(_projection(), source_revision="")
    packet = pk.assemble_packet(
        projection=revisionless, scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.of_kind(pk.SOURCE_EVIDENCE), "no evidence, nothing to warn about"
    text = pk.declaration_text(packet)
    assert "evidence bytes are the served checkout at revision unknown" in text
    assert "NOT this session's worktree" in text


def test_the_caveat_survives_when_every_evidence_item_was_dropped():
    """Dropped refs are named as one-retrieval-call-away FROM THE SERVED
    CHECKOUT, so the caveat is owed there too."""
    boundary = _boundary()
    boundary.sources[EVIDENCE_DRAFT] = ("Status: draft\n\n"
                                        + "x" * (pk.MAX_PACKET_BYTES + 1))
    boundary.sources[EVIDENCE_RATIFIED] = ("Status: ratified\n\n"
                                           + "y" * (pk.MAX_PACKET_BYTES + 1))
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.of_kind(pk.SOURCE_EVIDENCE) == ()
    assert packet.dropped_evidence
    assert "NOT this session's worktree" in pk.declaration_text(packet)


def test_dropped_refs_are_named_BEST_ranked_first_as_they_were_dropped():
    """RE-VERIFY NF5. The line said "lowest-ranked first" while `bounds_rail`
    walks best-ranked first and appends what does not fit — so the first name
    printed is the HIGHEST-ranked item that was dropped, and the sentence was
    the exact opposite of the data beside it."""
    huge = "Status: draft\n\n" + "x" * (pk.MAX_PACKET_BYTES + 1)
    rows = (
        pk.PacketSource(ref="rank1.md", kind=pk.SOURCE_EVIDENCE, text=huge,
                        status=None, compression_exempt=False),
        pk.PacketSource(ref="rank2.md", kind=pk.SOURCE_EVIDENCE, text=huge,
                        status=None, compression_exempt=False),
    )
    _fitted, dropped = pk.bounds_rail(rows)
    assert dropped == ("rank1.md", "rank2.md")


def test_a_ratified_document_can_be_dropped_by_the_fit_and_is_named():
    """RE-VERIFY NF7, stated rather than left implicit: the exemption governs
    aggressive COMPRESSION, not selection, so canon can be selected out by byte
    size while a draft that fits is carried. The dropped ref is named."""
    boundary = _boundary()
    boundary.sources[EVIDENCE_RATIFIED] = ("Status: ratified\n\n"
                                           + "y" * (pk.MAX_PACKET_BYTES + 1))
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    assert EVIDENCE_RATIFIED in packet.dropped_evidence
    assert EVIDENCE_DRAFT in packet.refs()
    assert EVIDENCE_RATIFIED in pk.declaration_text(packet)


def test_a_packet_carrying_no_evidence_claims_no_revision():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    assert packet.source_revision is None
    assert "served checkout at revision" not in pk.declaration_text(packet)


def test_a_retrieval_coverage_shortfall_is_STATED_not_left_to_silence():
    """The index has a declared bound; the confinement does not. Refs past the
    bound are confined-but-unindexable, which the declaration must say — the
    lossless note's "one retrieval call away" is FALSE for them."""
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock(),
        corpus_coverage=pk.CorpusCoverage(indexed=200, unreadable=0, total=512))
    text = pk.declaration_text(packet)
    assert "the index covered 200 of 512 documents" in text
    assert "312 were beyond the declared index bound" in text
    assert "not one retrieval call away either" in text


def test_the_two_omission_classes_are_stated_apart_not_merged():
    """Codex review of PR #216, CODEX-C. An UNREADABLE document is absent at
    this revision and stays absent until it is fixed; a BEYOND-BOUND one exists
    and would be retrievable under a larger bound. Blaming the index bound for
    both told the reader the wrong thing about half of them."""
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock(),
        corpus_coverage=pk.CorpusCoverage(indexed=5, unreadable=2, total=9))
    text = pk.declaration_text(packet)
    assert "the index covered 5 of 9 documents" in text
    assert "2 could not be read at this revision" in text
    assert "2 were beyond the declared index bound" in text


def test_an_unreadable_only_shortfall_does_not_blame_the_bound():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock(),
        corpus_coverage=pk.CorpusCoverage(indexed=4, unreadable=2, total=6))
    text = pk.declaration_text(packet)
    assert "2 could not be read at this revision" in text
    assert "beyond the declared index bound" not in text


def test_coverage_that_accounts_for_more_than_the_tile_holds_is_refused():
    with pytest.raises(pk.PacketError):
        pk.CorpusCoverage(indexed=5, unreadable=5, total=6)


def test_full_coverage_is_stated_too_so_the_line_is_never_ambiguous():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock(),
        corpus_coverage=pk.CorpusCoverage(indexed=7, unreadable=0, total=7))
    assert "the index covered all 7 documents" in pk.declaration_text(packet)


def test_selection_is_lossless_by_reference_and_says_so():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    assert "lossless" in pk.declaration_text(packet).lower()
    assert "one retrieval call away" in pk.declaration_text(packet)


# ===========================================================================
# RAIL 3 — THE LIFECYCLE-STATUS EXEMPTION (task 10.3)
# ===========================================================================


def test_ratified_content_is_exempted_by_the_assembler_before_any_provider():
    """The delta's `Ratified content meets the compressor` scenario. The
    marking travels WITH the item, applied in the assembler, so it is upstream
    of a compressor that does not exist yet and cannot be delegated to one."""
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    by_ref = {source.ref: source for source in packet.sources}
    assert by_ref[EVIDENCE_RATIFIED].status == "ratified"
    assert by_ref[EVIDENCE_RATIFIED].compression_exempt is True
    assert by_ref[EVIDENCE_DRAFT].status == "draft"
    assert by_ref[EVIDENCE_DRAFT].compression_exempt is False
    assert packet.exempt_count == 1


@pytest.mark.parametrize("status,exempt", [
    ("ratified", True), ("standard", True), ("approved", True),
    ("draft", False), ("staged", False), ("brainstorm", False),
    ("superseded", False), ("retired", False), ("record", False),
])
def test_the_exempt_status_set_is_the_approved_end_of_the_lifecycle(status,
                                                                    exempt):
    assert pk.is_compression_exempt(f"Status: {status}\n\nbody\n") is exempt


@pytest.mark.parametrize("raw,word,exempt", [
    ("ratified", "ratified", True),
    ("ratified (2026-08-01)", "ratified", True),
    ("standard · promoted 2026-07-24", "standard", True),
    ("record · 2026-08-01T01:21Z (session of 2026-07-31)", "record", False),
    ("record (in progress — accumulating)", "record", False),
    ("brainstorm | staged", "brainstorm", False),
    ("superseded by add-x", "superseded", False),
])
def test_a_DECORATED_status_keeps_its_status_word(raw, word, exempt):
    """This corpus already carries decorated statuses (`record · …`,
    `record (in progress — …)`), so a decorated `ratified (…)` would otherwise
    lose its exemption SILENTLY — the exact failure this rail prevents.

    `lifecycle_status` still returns the RAW value, so the agreement with the
    repository's own corpus reader is untouched."""
    text = f"Status: {raw}\n\nbody\n"
    assert pk.lifecycle_status(text) == raw
    assert pk.status_word(raw) == word
    assert pk.is_compression_exempt(text) is exempt


def test_a_document_with_no_status_header_is_not_exempt():
    assert pk.lifecycle_status("no header here\n") is None
    assert pk.is_compression_exempt("no header here\n") is False


def test_a_thread_is_never_exempt_because_a_summary_is_not_canon():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler",
        threads={DOC_A: _thread(DOC_A)}, knowledge=None, clock=_clock())
    for source in packet.sources:
        assert source.compression_exempt is False
        assert source.status is None


def test_the_status_read_agrees_with_the_repositorys_own_corpus_reader():
    """The rule lives in two places by necessity — the assembler must read the
    header ITSELF — so the two spellings are asserted to agree over REAL
    documents rather than assumed to."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health.corpus import parse_status  # noqa: E402

    assert pk.STATUS_SCAN_LINES == 15
    checked = 0
    for path in sorted((REPO_ROOT / "docs").rglob("*.md"))[:80]:
        text = path.read_text(encoding="utf-8", errors="replace")
        assert pk.lifecycle_status(text) == parse_status(text), path
        checked += 1
    assert checked > 10, "the drift check needs real documents to be a check"


# ===========================================================================
# RAIL 4 — THE BOUNDS CHECK (task 10.3)
# ===========================================================================


def _oversized_thread() -> dt.DocumentThread:
    """A thread whose state header alone blows the packet bound. Nothing
    SELECTED it, so there is nothing to select less of."""
    return _thread(DOC_A, goal="g" * (pk.MAX_PACKET_BYTES + 1))


def test_oversized_evidence_is_SELECTED_OUT_rather_than_refusing_the_turn():
    """RE-PINNED (adversarial review, F2). This test used to assert that
    server-selected evidence over the bound REFUSED the turn — which made every
    turn on a tile holding one big document fail forever, with an HTTP 413
    blaming a ~700-byte request for 293 KB the server itself chose.

    Selection is layer one, and layer one's contract is LOSSLESS BY REFERENCE:
    carrying less of what retrieval selected is selection, not truncation. So
    the packet FITS by selecting less and NAMES what it dropped."""
    oversized = "x" * (pk.MAX_PACKET_BYTES + 1)
    boundary = _boundary()
    boundary.sources[EVIDENCE_DRAFT] = "Status: draft\n\n" + oversized
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    assert packet.byte_count <= pk.MAX_PACKET_BYTES
    assert EVIDENCE_DRAFT in packet.dropped_evidence
    assert EVIDENCE_DRAFT not in packet.refs()
    # the one that fits is still carried: a fit is not an all-or-nothing drop
    assert EVIDENCE_RATIFIED in packet.refs()


def test_every_dropped_ref_is_NAMED_in_the_declaration():
    """"Lossless by reference" is only true if the packet says which
    references it is standing on."""
    boundary = _boundary()
    boundary.sources[EVIDENCE_DRAFT] = ("Status: draft\n\n"
                                        + "x" * (pk.MAX_PACKET_BYTES + 1))
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    text = pk.declaration_text(packet)
    assert "selected out to fit this packet's bound, best-ranked first" in text
    for ref in packet.dropped_evidence:
        assert ref in text
    assert "one retrieval call away" in text
    assert "nothing was shortened" in text


def test_the_fit_keeps_the_best_ranked_items_that_FIT_not_a_prefix():
    """Dropping strictly from the tail was the obvious alternative and is
    worse: one oversized TOP hit would evict every smaller item behind it and
    the packet would carry nothing. The fit is greedy BY RANK."""
    huge = "Status: draft\n\n" + "x" * (pk.MAX_PACKET_BYTES + 1)
    rows = (
        pk.PacketSource(ref="rank1-huge.md", kind=pk.SOURCE_EVIDENCE, text=huge,
                        status=None, compression_exempt=False),
        pk.PacketSource(ref="rank2-small.md", kind=pk.SOURCE_EVIDENCE,
                        text="small", status=None, compression_exempt=False),
    )
    fitted, dropped = pk.bounds_rail(rows)
    assert [source.ref for source in fitted] == ["rank2-small.md"]
    assert dropped == ("rank1-huge.md",)


def test_the_source_count_bound_is_fitted_by_dropping_too():
    rows = tuple(
        pk.PacketSource(ref=f"r{index:03d}.md", kind=pk.SOURCE_EVIDENCE,
                        text="x", status=None, compression_exempt=False)
        for index in range(pk.MAX_PACKET_SOURCES + 3))
    fitted, dropped = pk.bounds_rail(rows)
    assert len(fitted) == pk.MAX_PACKET_SOURCES
    assert len(dropped) == 3
    # rank order preserved: the three dropped are the last three
    assert dropped == ("r048.md", "r049.md", "r050.md")


def test_threads_alone_over_the_bound_REFUSE_with_the_measured_dimension():
    """The genuine refusal arm, and the only one left: the threads are not
    SELECTED — the packet is the only place they appear — so there is nothing
    to select less of. The refusal is actionable, because layer two exists to
    compact a thread back inside a bound."""
    with pytest.raises(pk.PacketBoundExceeded) as raised:
        pk.assemble_packet(
            projection=_projection(), scope=SCOPE, selected_key=DOC_A,
            loaded_keys=(DOC_A,), query="packet assembler", knowledge=None,
            threads={DOC_A: _oversized_thread()}, clock=_clock())
    assert raised.value.limit["dimension"] == "context_packet_bytes"
    assert raised.value.limit["measured"] > pk.MAX_PACKET_BYTES
    assert raised.value.limit["maximum"] == pk.MAX_PACKET_BYTES


def test_the_source_count_refusal_arm_names_its_own_dimension():
    rows = tuple(
        pk.PacketSource(ref=f"t{index:03d}.md", kind=pk.SOURCE_THREAD_STATE,
                        text="x", status=None, compression_exempt=False)
        for index in range(pk.MAX_PACKET_SOURCES + 1))
    with pytest.raises(pk.PacketBoundExceeded) as raised:
        pk.bounds_rail(rows)
    assert raised.value.limit["dimension"] == "context_packet_sources"


def test_a_bounds_refusal_discloses_no_packet_content():
    sentinel = "SENTINEL-PACKET-CONTENT-" + "y" * pk.MAX_PACKET_BYTES
    with pytest.raises(pk.PacketBoundExceeded) as raised:
        pk.assemble_packet(
            projection=_projection(), scope=SCOPE, selected_key=DOC_A,
            loaded_keys=(DOC_A,), query="packet assembler", knowledge=None,
            threads={DOC_A: _thread(DOC_A, goal=sentinel)}, clock=_clock())
    assert "SENTINEL-PACKET-CONTENT" not in str(raised.value)
    assert "SENTINEL-PACKET-CONTENT" not in repr(raised.value)
    assert "SENTINEL-PACKET-CONTENT" not in repr(raised.value.limit)
    # and no ref either -- the refusal is dimensions and integers
    assert DOC_A not in str(raised.value)


def test_nothing_is_truncated_to_fit_a_bound():
    """The house rule is refuse-and-say-the-number, and the other rule — a
    packet source carries its EXACT text — is what makes truncation
    impossible rather than merely discouraged."""
    long_text = "Status: draft\n\n" + ("z" * 5000)
    boundary = _boundary()
    boundary.sources[EVIDENCE_DRAFT] = long_text
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=boundary,
        already_carried=(OUTLINE,), clock=_clock())
    carried = {source.ref: source.text for source in packet.sources}
    assert carried[EVIDENCE_DRAFT] == long_text


# ===========================================================================
# THE DEGRADED POSTURE (task 10.7)
# ===========================================================================


def test_no_knowledge_service_yields_the_declared_reduced_packet():
    """The delta's `The knowledge service is unavailable` scenario: the turn
    degrades, states the reduction, substitutes nothing, and bypasses nothing."""
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B), query="packet assembler",
        threads={DOC_A: _thread(DOC_A), DOC_B: _thread(DOC_B)},
        knowledge=None, clock=_clock())
    assert packet.posture == pk.POSTURE_REDUCED
    assert packet.reduced_reason == pk.REDUCED_NO_KNOWLEDGE_SERVICE
    assert packet.of_kind(pk.SOURCE_EVIDENCE) == ()
    # the selected thread and the loaded buffers' threads still ride
    assert [s.ref for s in packet.of_kind(pk.SOURCE_SELECTED_THREAD)] == [DOC_A]
    assert [s.ref for s in packet.of_kind(pk.SOURCE_THREAD_STATE)] == [DOC_B]
    assert packet.provider_id == pk.PROVIDER_NONE


def test_the_reduced_posture_is_STATED_in_the_assembled_context():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    declaration = dict(pk.packet_sections(packet))[
        pk.PACKET_SECTION_DECLARATION]
    assert "posture: reduced" in declaration
    assert "reduced because:" in declaration
    assert "no unbounded context was substituted" in declaration
    assert "no rail was bypassed" in declaration


def test_the_reduced_packet_runs_the_SAME_rails_rather_than_skipping_them():
    """The reduction is one absent input, not a second pipeline: the bounds
    rail still refuses and the exemption rail still marks."""
    with pytest.raises(pk.PacketBoundExceeded):
        pk.assemble_packet(
            projection=_projection(), scope=SCOPE, selected_key=DOC_A,
            loaded_keys=(DOC_A,), query="", knowledge=None,
            threads={DOC_A: _thread(
                DOC_A, goal="x" * (pk.MAX_PACKET_BYTES + 1))},
            clock=_clock())


def test_a_retrieval_that_REFUSES_degrades_instead_of_killing_the_turn():
    """"The knowledge service cannot answer" is a case the delta already rules
    on. v1's in-process backend cannot realistically refuse, but the port
    exists so another backend can sit behind it, and an unhandled refusal there
    would have dropped the connection mid-turn."""
    class RefusingBoundary(RecordingBoundary):
        def search(self, query, *, confined_to, limit,
                   thread_signals=frozenset()):
            raise kn.RetrievalRefused("this backend declines")

    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler",
        knowledge=RefusingBoundary(), already_carried=(OUTLINE,),
        clock=_clock())
    assert packet.posture == pk.POSTURE_REDUCED
    assert packet.reduced_reason == pk.REDUCED_RETRIEVAL_REFUSED
    assert packet.of_kind(pk.SOURCE_EVIDENCE) == ()
    assert packet.provider_id == pk.PROVIDER_NONE


def test_evidence_gathered_before_a_refusal_is_discarded_not_half_carried():
    class HalfwayBoundary(RecordingBoundary):
        def get_source(self, ref, *, confined_to):
            self.fetches.append((ref, confined_to))
            if ref == EVIDENCE_DRAFT:
                return kn.IndexedSource(ref=ref, text=DRAFT_TEXT)
            raise kn.RetrievalRefused("this backend declines mid-answer")

    halfway = HalfwayBoundary(sources={EVIDENCE_RATIFIED: RATIFIED_TEXT,
                                       EVIDENCE_DRAFT: DRAFT_TEXT})
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler",
        knowledge=halfway, already_carried=(OUTLINE,), clock=_clock())
    assert halfway.fetches, "the test never reached the failing fetch"
    assert packet.posture == pk.POSTURE_REDUCED
    assert packet.of_kind(pk.SOURCE_EVIDENCE) == ()


def test_a_reduced_packet_must_state_its_reason():
    with pytest.raises(pk.PacketError) as raised:
        pk.ContextPacket(purpose=pk.PACKET_PURPOSE_CHAT_TURN, scope=SCOPE,
                         posture=pk.POSTURE_REDUCED, sources=(),
                         issued_at=1.0, expires_at=2.0)
    assert "a reduction nobody can read is a silent degradation" in str(
        raised.value)


def test_a_full_packet_may_not_carry_a_reduction_reason():
    with pytest.raises(pk.PacketError):
        pk.ContextPacket(purpose=pk.PACKET_PURPOSE_CHAT_TURN, scope=SCOPE,
                         posture=pk.POSTURE_FULL, sources=(), issued_at=1.0,
                         expires_at=2.0, reduced_reason="because")


# ===========================================================================
# THE THREE-LAYER COMPRESSION STACK — the fidelity pins
# ===========================================================================


def test_the_three_layers_declare_three_different_fidelity_contracts():
    fidelities = [row.fidelity for row in pk.COMPRESSION_LAYERS]
    assert fidelities == [pk.FIDELITY_LOSSLESS_BY_REFERENCE,
                          pk.FIDELITY_LOSSY_BY_DESIGN,
                          pk.FIDELITY_MECHANICAL_REVERSIBLE]
    assert len(set(fidelities)) == 3


@pytest.mark.parametrize("number,claimed", [
    (1, pk.FIDELITY_LOSSY_BY_DESIGN),          # selection is not lossy
    (2, pk.FIDELITY_LOSSLESS_BY_REFERENCE),    # compaction is not lossless
    (3, pk.FIDELITY_LOSSY_BY_DESIGN),          # offload is not a summary
])
def test_a_layer_claiming_anothers_fidelity_is_refused(number, claimed):
    """The delta's `A layer claims another's fidelity` scenario, executable."""
    with pytest.raises(pk.FidelityClaimRefused) as raised:
        pk.assert_fidelity(number, claimed)
    assert "what make the stack readable" in str(raised.value)


def test_each_layer_names_its_real_owner():
    assert pk.layer(2).owner == "doxbench_threads.compact_thread"
    assert callable(dt.compact_thread)
    assert pk.layer(1).realized is True
    assert pk.layer(2).realized is True
    # LAYER THREE IS NOT REALIZED HERE, and says so rather than being absent.
    assert pk.layer(3).realized is False
    assert "§11" in pk.layer(3).owner


def test_the_exemption_sits_upstream_of_where_layer_three_will_run():
    note = pk.layer(3).note
    assert "upstream" in note
    assert "no caller-metadata surface is disqualified" in note
    # and it really is upstream: the marking is on the packet BEFORE any
    # compressor could exist to receive it
    marked = pk.exemption_rail((pk.PacketSource(
        ref=EVIDENCE_RATIFIED, kind=pk.SOURCE_EVIDENCE, text=RATIFIED_TEXT,
        status=None, compression_exempt=False),))
    assert marked[0].compression_exempt is True


def test_the_watch_listed_candidate_is_recorded_with_gates_and_not_adopted():
    assert pk.WATCH_LISTED_CANDIDATES
    for candidate in pk.WATCH_LISTED_CANDIDATES:
        assert candidate.adopted is False
        assert len(candidate.gates) >= 4
    with pytest.raises(pk.PacketError) as raised:
        pk.WatchListedCandidate(name="Headroom", layer=3, gates=("none",),
                                adopted=True)
    assert "sandboxed trial" in str(raised.value)


def test_no_watch_listed_candidate_is_depended_on_anywhere_in_this_slice():
    for module in ("doxbench_packet.py", "doxbench_knowledge.py",
                   "doxbench_telemetry.py", "doxbench_memory_gateway.py"):
        source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                  / module).read_text(encoding="utf-8").lower()
        assert "import headroom" not in source, module
        assert "headroomlabs" not in source, module


# ===========================================================================
# THE PACKET'S PROMPT SECTIONS (task 5.4's packet half)
# ===========================================================================


def test_the_expanded_keys_and_the_rendered_sections_cannot_disagree():
    threads = {key: _thread(key, turns=(TURN,)) for key in (DOC_A, DOC_B)}
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B), query="packet assembler", threads=threads,
        knowledge=_boundary(), already_carried=(OUTLINE,), clock=_clock())
    expanded = []
    for group in pk.PACKET_SECTION_GROUPS:
        expanded.extend(pk.expand_group(group, packet))
    assert [key for key, _ in pk.packet_sections(packet)] == expanded


def test_a_group_with_nothing_contributes_no_section_at_all():
    packet = pk.reduced_packet(projection=_projection(), scope=SCOPE,
                               selected_key=DOC_A, loaded_keys=(DOC_A,),
                               clock=_clock())
    assert pk.expand_group(pk.PACKET_SECTION_EVIDENCE, packet) == ()
    assert pk.expand_group(pk.PACKET_SECTION_SELECTED_THREAD, packet) == ()
    keys = [key for key, _ in pk.packet_sections(packet)]
    assert keys == [pk.PACKET_SECTION_DECLARATION]


def test_no_packet_contributes_no_sections():
    for group in pk.PACKET_SECTION_GROUPS:
        assert pk.expand_group(group, None) == ()
    assert pk.packet_sections(None) == ()


def test_thread_sections_carry_the_non_authoritative_declaration():
    threads = {key: _thread(key, turns=(TURN,)) for key in (DOC_A, DOC_B)}
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B), query="packet assembler", threads=threads,
        knowledge=None, clock=_clock())
    sections = dict(pk.packet_sections(packet))
    assert "NON-AUTHORITATIVE" in sections[pk.PACKET_SECTION_SELECTED_THREAD]
    header = sections[pk.THREAD_STATE_SECTION_PREFIX + DOC_B]
    assert "NON-AUTHORITATIVE" in header
    assert "the transcript it summarizes is not carried here" in header


def test_evidence_sections_carry_the_ref_and_the_exemption_verdict():
    packet = pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A,), query="packet assembler", knowledge=_boundary(),
        already_carried=(OUTLINE,), clock=_clock())
    sections = dict(pk.packet_sections(packet))
    ratified = sections[pk.EVIDENCE_SECTION_PREFIX + EVIDENCE_RATIFIED]
    assert EVIDENCE_RATIFIED in ratified
    assert "Status: ratified" in ratified
    assert "EXEMPT from aggressive compression" in ratified
    draft = sections[pk.EVIDENCE_SECTION_PREFIX + EVIDENCE_DRAFT]
    assert "ordinary compression" in draft


# ===========================================================================
# NEGATIVE SPACE
# ===========================================================================

_FORBIDDEN_MODULE_NEEDLES = [
    ("import os", "an os import"),
    ("open(", "a direct file open"),
    ("write_text", "a direct write"),
    ("subprocess", "a subprocess invocation"),
    ("urllib", "a network client"),
    ("socket", "a network socket"),
    # `truncate` and `shorten` DO appear in this module — inside the sentences
    # that say it never happens. The negative that matters is the CODE, so the
    # needles below are the shapes a truncation would actually take.
    ("[:MAX_PACKET_BYTES", "a silent shortening by bytes"),
    ("[:MAX_PACKET_SOURCES", "a silent shortening by source count"),
    ("textwrap", "a reflow"),
    ("sqlite3", "a second store"),
    ("def promote", "a promotion path"),
]


@pytest.mark.parametrize("needle,label", _FORBIDDEN_MODULE_NEEDLES,
                         ids=[needle for needle, _ in _FORBIDDEN_MODULE_NEEDLES])
def test_the_packet_module_contains_no_forbidden_spelling(needle, label):
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert needle not in source, (
        f"doxbench_packet.py must not contain {label}: {needle!r}")
