"""The doxBench STAGED-SET KNOWLEDGE SERVICE v1 — the tool boundary, the
assembly port, the local-hybrid backend, and the install-time declaration
(add-doxbench-editing-phase-b, design §3.3 / D10 / D11, tasks 10.1, 10.2,
10.5, 10.6).

The negatives are the point of this file, and each is asserted CONSTRUCTIVELY
rather than described:

  * `graph_query` EXISTS at the boundary and refuses with a fixed governance
    reason — it is not a missing name, and it is not a crash;
  * no graph engine, store, or index is reachable, importable, or spelled;
  * no runtime path selects a retrieval backend — the parameter that would
    carry a turn, a prompt, or a heuristic does not exist on the function that
    builds one, which is asserted against the SIGNATURE;
  * retrieval and source fetch are both confined to the caller's declared ref
    set, and a backend answering outside it has its answer dropped; and
  * `promote_finding` writes nothing anywhere.
"""

from __future__ import annotations

import dataclasses
import inspect

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_knowledge.py")

RATIFIED = ("Status: ratified\n\n"
            "The packet assembler runs its rails before any provider call.\n")
DRAFT = ("Status: draft\n\n"
         "A contract governs how the packet is bounded and expires.\n")
STANDARD = ("Status: standard\n\n"
            "Unrelated notes about brewing coffee in the morning.\n")

CORPUS = (
    kn.IndexedSource(ref="ideation/staging/t/rails.md", text=RATIFIED),
    kn.IndexedSource(ref="ideation/staging/t/contract.md", text=DRAFT),
    kn.IndexedSource(ref="ideation/staging/t/coffee.md", text=STANDARD),
)
ALL_REFS = frozenset(source.ref for source in CORPUS)

# A query that scores ZERO on both textual legs against this corpus: no shared
# token and no shared character n-gram. Worth naming, because "obviously
# unrelated" prose is NOT such a query — `zzzzz-nothing-matches` scores on the
# vector leg through the trigrams it shares with `morning`, which is the leg
# doing its job rather than a defect.
NULL_QUERY = "xqxqxq"


def _backend() -> kn.LocalHybridBackend:
    backend = kn.build_backend(kn.SELF_HOSTED_LOCAL_EMBEDDED)
    backend.index(CORPUS)
    return backend


def _boundary() -> kn.KnowledgeToolBoundary:
    return kn.KnowledgeToolBoundary(_backend())


# ===========================================================================
# THE ASSEMBLY PORT (task 10.1)
# ===========================================================================

# The spellings that would make the port a second boundary, a graph surface, or
# a credential carrier. Mirrors `test_doxbench_model.FORBIDDEN_PORT_MEMBERS`
# and exists for the same reason: a port grows a member the day nobody is
# asserting it did not.
FORBIDDEN_ASSEMBLY_PORT_MEMBERS = {
    "graph_query", "graph", "traverse", "neighbors", "subgraph", "edges",
    "promote", "promote_finding", "write", "store", "save", "commit",
    "credentials", "api_key", "endpoint", "client", "fetch", "request",
}


def test_the_assembly_port_declares_exactly_four_product_neutral_members():
    declared = kn.RetrievalAssemblyPort.__protocol_attrs__
    assert declared == set(kn.ASSEMBLY_PORT_MEMBERS)
    assert not (declared & FORBIDDEN_ASSEMBLY_PORT_MEMBERS)


def test_the_port_and_the_tool_boundary_are_two_different_vocabularies():
    """Design §3.3: the tool contract is what a CALLER sees and the port is
    what a PROVIDER implements. One vocabulary for both would make a backend
    swap look like a boundary change the first time they had to differ."""
    assert set(kn.ASSEMBLY_PORT_MEMBERS) != set(kn.IMPLEMENTED_TOOLS)


def test_the_v1_backend_satisfies_the_port():
    backend = _backend()
    assert isinstance(backend, kn.RetrievalAssemblyPort)
    for member in kn.ASSEMBLY_PORT_MEMBERS:
        assert callable(getattr(backend, member))


def test_a_backend_missing_a_port_member_is_refused_at_the_boundary():
    class Partial:
        def profile(self):  # pragma: no cover - never reached
            return kn.LOCAL_EMBEDDED_PROFILE

    with pytest.raises(kn.KnowledgeError) as raised:
        kn.KnowledgeToolBoundary(Partial())
    assert "assembly port member" in str(raised.value)


# ===========================================================================
# NO GRAPH, ANYWHERE (design D10, §8)
# ===========================================================================


def test_the_v1_profile_declares_graph_false_rather_than_omitting_it():
    profile = kn.LOCAL_EMBEDDED_PROFILE
    assert profile.graph is False
    assert profile.signals == (kn.SIGNAL_LEXICAL, kn.SIGNAL_VECTOR,
                               kn.SIGNAL_THREAD_STATE)


def test_a_profile_declaring_a_graph_capability_is_refused():
    """The delta's `A graph engine is proposed for v1` scenario, expressed
    where a graph would have to be declared to exist at all."""
    with pytest.raises(kn.BackendDeclarationRefused) as raised:
        kn.ProviderProfile(profile_id="graphy", signals=("graph",), graph=True,
                           networked=False, credentialed=False, notes="n")
    assert "graduation trigger" in str(raised.value)


_FORBIDDEN_GRAPH_SPELLINGS = [
    "networkx", "neo4j", "cognee", "falkordb", "graphiti", "kuzu", "ladybug",
    "adjacency", "def traverse", "import sqlite3", "headroom",
]


@pytest.mark.parametrize("needle", _FORBIDDEN_GRAPH_SPELLINGS)
def test_no_graph_engine_or_watch_listed_candidate_is_spelled(needle):
    source = MODULE_PATH.read_text(encoding="utf-8").lower()
    assert needle not in source, needle


# ===========================================================================
# THE ONE TOOL BOUNDARY, AND THE RESERVED NAME (task 10.2)
# ===========================================================================


def test_the_boundary_declares_four_tools_and_one_reserved_name():
    boundary = _boundary()
    assert boundary.implemented_tools() == (
        "search", "get_source", "promote_finding", "reindex")
    assert boundary.reserved_tools() == ("graph_query",)
    assert boundary.declared_tools() == (
        "search", "get_source", "promote_finding", "reindex", "graph_query")


def test_the_reserved_name_is_declared_and_unimplemented_not_missing():
    """The reservation IS the point: a caller must get a governance answer, not
    a missing name and not a crash."""
    boundary = _boundary()
    assert "graph_query" in boundary.declared_tools()
    assert "graph_query" not in boundary.implemented_tools()
    assert not hasattr(boundary, "graph_query")
    with pytest.raises(kn.ReservedToolUnimplemented) as raised:
        boundary.call("graph_query", query="anything")
    message = str(raised.value)
    assert "RESERVED and unimplemented" in message
    assert "GRADUATION TRIGGER" in message
    assert "dependency traversal" in message
    # a fixed refusal: the same answer every time, whatever it is asked
    with pytest.raises(kn.ReservedToolUnimplemented) as again:
        boundary.call("graph_query")
    assert str(again.value) == message


def test_the_reserved_refusal_is_not_a_NotImplementedError():
    boundary = _boundary()
    with pytest.raises(kn.KnowledgeError) as raised:
        boundary.call("graph_query")
    assert not isinstance(raised.value, NotImplementedError)


def test_an_undeclared_name_is_a_different_verdict_from_a_reserved_one():
    boundary = _boundary()
    with pytest.raises(kn.UnknownTool):
        boundary.call("vector_query")
    assert not issubclass(kn.UnknownTool, kn.ReservedToolUnimplemented)
    assert not issubclass(kn.ReservedToolUnimplemented, kn.UnknownTool)


def test_dispatch_cannot_reach_a_private_helper_by_naming_it():
    boundary = _boundary()
    with pytest.raises(kn.UnknownTool):
        boundary.call("_port")


def test_every_declared_tool_dispatches_through_call():
    boundary = _boundary()
    assert boundary.call("search", query="packet",
                         confined_to=ALL_REFS, limit=3)
    assert boundary.call("get_source", ref=CORPUS[0].ref,
                         confined_to=ALL_REFS).text == RATIFIED
    assert boundary.call("promote_finding", finding="settled",
                         provenance=(CORPUS[0].ref,)).act_verb
    assert boundary.call("reindex", sources=CORPUS).source_count == 3


# ===========================================================================
# PROMOTION IS GATE-ONLY (design §4.2)
# ===========================================================================


def test_promote_finding_returns_a_request_and_writes_nothing():
    boundary = _boundary()
    request = boundary.promote_finding(
        "the topic needs a delta type", provenance=("ideation/staging/t/t.md",))
    assert isinstance(request, kn.PromotionRequest)
    assert request.act_verb == "create-document"
    assert request.provenance == ("ideation/staging/t/t.md",)
    # the finding is NOT in the index afterwards: nothing was stored
    assert boundary.get_source("ideation/staging/t/t.md",
                               confined_to=frozenset({"ideation/staging/t/t.md"})) is None


def test_an_unattributed_finding_is_refused():
    boundary = _boundary()
    with pytest.raises(kn.KnowledgeError) as raised:
        boundary.promote_finding("a claim from nowhere", provenance=())
    assert "provenance" in str(raised.value)


# ===========================================================================
# THE INSTALL-TIME DECLARATION (task 10.6, design D11)
# ===========================================================================


def test_the_self_hosted_case_declares_the_local_embedded_profile():
    declaration = kn.SELF_HOSTED_LOCAL_EMBEDDED
    assert declaration.installation == kn.INSTALL_SELF_HOSTED
    assert declaration.profile_id == kn.PROFILE_LOCAL_EMBEDDED
    assert declaration.networked is False
    assert declaration.credentialed is False
    assert declaration.declared_by


def test_a_self_hosted_install_may_not_declare_a_hosted_backend():
    """The ratified two-case principle, enforced rather than described."""
    with pytest.raises(kn.BackendDeclarationRefused) as raised:
        kn.RetrievalBackendDeclaration(
            installation=kn.INSTALL_SELF_HOSTED, profile_id="vertex-hosted",
            networked=True, credentialed=True, declared_by="an operator")
    assert "only a tenant install may declare" in str(raised.value)


def test_a_tenant_may_declare_a_hosted_backend_that_this_release_does_not_ship():
    """The declaration MECHANISM must be the thing that names a hosted
    backend even though v1 ships only the local profile — and resolving one
    is an honest refusal rather than a silent local fallback."""
    declared = kn.RetrievalBackendDeclaration(
        installation=kn.INSTALL_TENANT, profile_id="vertex-hosted",
        networked=True, credentialed=True, declared_by="a tenant install")
    with pytest.raises(kn.BackendUnavailable) as raised:
        kn.build_backend(declared)
    assert "vertex-hosted" in str(raised.value)
    assert "ships only" in str(raised.value)
    assert "would hide which backend this install talks to" in str(raised.value)


def test_the_local_profile_may_never_be_declared_networked_or_credentialed():
    with pytest.raises(kn.BackendDeclarationRefused):
        kn.RetrievalBackendDeclaration(
            installation=kn.INSTALL_TENANT,
            profile_id=kn.PROFILE_LOCAL_EMBEDDED, networked=True,
            credentialed=False, declared_by="a tenant install")


def test_no_runtime_selection_path_exists_asserted_against_the_signature():
    """"a backend MUST NOT be selected at runtime by a turn, a prompt, or a
    heuristic" — proven by the ABSENCE of the parameter that would carry one,
    rather than by a comment saying nobody passes it."""
    parameters = set(inspect.signature(kn.build_backend).parameters)
    assert parameters == {"declaration"}
    for forbidden in ("turn", "prompt", "message", "scope", "request",
                      "heuristic", "hint"):
        assert forbidden not in parameters


def test_the_module_exposes_no_selection_or_choice_callable():
    public = {name for name in vars(kn) if not name.startswith("_")}
    for name in public:
        lowered = name.lower()
        for forbidden in ("select_backend", "choose", "pick", "autodetect",
                          "detect_backend", "for_turn", "for_prompt"):
            assert forbidden not in lowered, name


_FORBIDDEN_MODULE_NEEDLES = [
    ("import os", "an os import"),
    ("open(", "a direct file open"),
    ("write_text", "a direct write"),
    ("subprocess", "a subprocess invocation"),
    ("urllib", "a network client"),
    ("socket", "a network socket"),
    ("http", "a network protocol"),
    ("api_key", "a credential field"),
    ("pickle", "an opaque store"),
    ("shelve", "an opaque store"),
]


@pytest.mark.parametrize("needle,label", _FORBIDDEN_MODULE_NEEDLES,
                         ids=[needle for needle, _ in _FORBIDDEN_MODULE_NEEDLES])
def test_the_knowledge_module_contains_no_forbidden_spelling(needle, label):
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert needle not in source, (
        f"doxbench_knowledge.py must not contain {label}: {needle!r}")


# ===========================================================================
# THE LOCAL-HYBRID RETRIEVAL (task 10.1)
# ===========================================================================


def test_the_three_signals_each_do_work():
    backend = _backend()
    # LEXICAL: an exact term match ranks its document first and reports a
    # lexical score.
    lexical = backend.retrieve("rails provider", confined_to=ALL_REFS, limit=3)
    assert lexical[0].ref == "ideation/staging/t/rails.md"
    assert lexical[0].lexical > 0

    # VECTOR: a morphological variant shares NO token with the corpus, so the
    # lexical leg scores zero and only the embedded vectors can select.
    vector = backend.retrieve("bounding expiries", confined_to=ALL_REFS, limit=3)
    assert vector, "the vector leg selected nothing"
    assert all(hit.lexical == 0 for hit in vector)
    assert any(hit.vector > 0 for hit in vector)

    # THREAD-STATE: a ref the session's threads already cite is selected even
    # with no textual signal at all. `NULL_QUERY` is chosen so BOTH textual
    # legs really are zero — a query that merely looked unrelated still scores
    # on the vector leg, because shared character n-grams are exactly what that
    # leg is for.
    thread = backend.retrieve(
        NULL_QUERY, confined_to=ALL_REFS, limit=3,
        thread_signals=frozenset({"ideation/staging/t/coffee.md"}))
    assert [hit.ref for hit in thread] == ["ideation/staging/t/coffee.md"]
    assert thread[0].thread == 1.0
    assert thread[0].lexical == 0 and thread[0].vector == 0


@pytest.mark.parametrize("token,expected", [
    ("ab", ["ab"]),                              # shorter than one n-gram
    ("the", ["the", "#the"]),                    # EXACTLY one n-gram
    ("abcd", ["abcd", "#abc", "#bcd"]),          # two
])
def test_every_character_ngram_inside_a_token_is_emitted(token, expected):
    """Copilot review of PR #216. `len(token) > CHARACTER_NGRAM` skipped the
    single n-gram of a token exactly that long, so every three-letter token
    contributed NO n-gram feature while four-letter tokens contributed two —
    contradicting `_features`' own docstring, and weakening the vector leg
    precisely for the short tokens the lexical leg generalizes over worst.

    Pinned on the feature ENUMERATION rather than on a score, so it states the
    rule directly and cannot drift with the hash."""
    assert list(kn._features((token,))) == expected


def test_the_fused_weights_are_declared_and_sum_to_one():
    assert (kn.WEIGHT_LEXICAL + kn.WEIGHT_VECTOR
            + kn.WEIGHT_THREAD) == pytest.approx(1.0)


def test_retrieval_is_deterministic_across_processes_not_just_within_one():
    """`hashlib.blake2b`, never the randomized `hash()`: two independently
    built indexes rank identically, which is what makes this testable at all."""
    first = _backend().retrieve("packet contract", confined_to=ALL_REFS, limit=3)
    second = _backend().retrieve("packet contract", confined_to=ALL_REFS, limit=3)
    assert first == second


def test_ties_break_on_the_ref_so_ordering_never_depends_on_dict_iteration():
    backend = kn.build_backend(kn.SELF_HOSTED_LOCAL_EMBEDDED)
    backend.index((kn.IndexedSource(ref="b.md", text="same text here"),
                   kn.IndexedSource(ref="a.md", text="same text here")))
    hits = backend.retrieve("same text", confined_to=frozenset({"a.md", "b.md"}),
                            limit=2)
    assert [hit.ref for hit in hits] == ["a.md", "b.md"]
    assert hits[0].score == hits[1].score


def test_an_unselected_document_is_left_out_rather_than_carried_at_zero():
    backend = _backend()
    hits = backend.retrieve(NULL_QUERY, confined_to=ALL_REFS, limit=3)
    assert hits == ()


def test_the_index_is_a_derived_projection_rebuilt_from_its_sources():
    backend = _backend()
    assert backend.index(CORPUS[:1]).source_count == 1
    assert backend.source(CORPUS[1].ref) is None
    assert backend.index(CORPUS).source_count == 3


def test_the_indexed_source_carries_no_cached_lifecycle_status():
    """The exemption is the ASSEMBLER'S to apply from the item's own header; a
    status cached here would be a second copy for it to trust instead."""
    fields = {field.name for field in dataclasses.fields(kn.IndexedSource)}
    assert fields == {"ref", "text"}


# ===========================================================================
# CONFINEMENT (task 10.5)
# ===========================================================================


def test_retrieval_never_returns_a_ref_outside_the_confined_set():
    backend = _backend()
    confined = frozenset({"ideation/staging/t/contract.md"})
    hits = backend.retrieve("packet contract rails coffee",
                            confined_to=confined, limit=5)
    assert {hit.ref for hit in hits} <= confined


def test_a_source_fetch_outside_the_confined_set_is_refused():
    """A confinement that governed search but not fetch would be no
    confinement: a caller would search inside the set and fetch outside it."""
    boundary = _boundary()
    with pytest.raises(kn.RetrievalRefused) as raised:
        boundary.get_source("ideation/staging/t/coffee.md",
                            confined_to=frozenset({"ideation/staging/t/rails.md"}))
    assert "outside this tile's staged set" in str(raised.value)


def test_an_unconfined_retrieval_is_refused_rather_than_defaulted():
    backend = _backend()
    with pytest.raises(kn.RetrievalRefused) as raised:
        backend.retrieve("packet", confined_to=None, limit=3)
    assert "unconfined retrieval is the failure" in str(raised.value)


def test_the_retrieval_limit_is_bounded():
    backend = _backend()
    with pytest.raises(kn.RetrievalRefused):
        backend.retrieve("packet", confined_to=ALL_REFS, limit=0)
    with pytest.raises(kn.RetrievalRefused) as raised:
        backend.retrieve("packet", confined_to=ALL_REFS,
                         limit=kn.MAX_RETRIEVAL_LIMIT + 1)
    assert str(kn.MAX_RETRIEVAL_LIMIT) in str(raised.value)


def test_an_empty_confinement_yields_nothing_and_is_not_an_error():
    backend = _backend()
    assert backend.retrieve("packet", confined_to=frozenset(), limit=3) == ()
