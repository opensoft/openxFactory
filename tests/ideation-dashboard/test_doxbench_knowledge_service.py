"""The staged-set knowledge service THROUGH THE REAL SERVE — the install-time
declaration, the degraded posture, the two capabilities' independence, and the
content-free telemetry (add-doxbench-editing-phase-b tasks 10.6, 10.7, 10.8;
design §3.4).

Why this file drives a real server rather than the assembler directly: the
things it pins are all WIRING claims. "The backend is an install-time
declaration" is a claim about where `build_server` reads it and about what the
route does NOT do; "the two capabilities are independent" is a claim about a
route that has one and not the other; and "the editors are unaffected" is a
claim about a request that still succeeds. Each of those passes trivially
against a stubbed assembler and can only fail against a serve.

The harness is IMPORTED from `test_doxbench_routes` rather than copied, for
the reason `test_doxbench_composition.py` records: a second harness is a
second set of behaviours to keep in step, and the two drifting is how a wiring
defect hides.
"""

from __future__ import annotations

import dataclasses
import shutil

import pytest

from conftest import BASE_REPO, REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_telemetry as tel  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402
from ideation_dashboard.doxbench_scope import ScopeKey  # noqa: E402

from test_doxbench_routes import (  # noqa: E402
    OUTLINE_PATH, _assert_refusal, _catalog, _CatalogOnlyPort, _port,
    _post_turn, _turn,
)

# The two brainstorm notes this fixture tile's scope contains beside its own
# outline. Named here because the evidence assertions below are about material
# the tile really has, not about a fixture invented for the occasion.
TILE_EVIDENCE = ("ideation/brainstorm/doc-health-checks.md",
                 "ideation/brainstorm/dtn-register.md")


def _packet_sections(port):
    """The packet's sections out of the ONE envelope the port was handed."""
    assert len(port.dispatched) == 1, port.calls
    envelope = port.dispatched[0]
    return {section.key: section.text for section in envelope.sections}


def _declaration(port) -> str:
    return _packet_sections(port)[pk.PACKET_SECTION_DECLARATION]


# ===========================================================================
# THE INSTALL-TIME DECLARATION (task 10.6)
# ===========================================================================


def test_a_server_built_with_no_declaration_has_no_knowledge_service(tmp_path):
    """The library default is ABSENCE, exactly as it is for the notebook
    adapter and the model port: `build_server` never reaches for a backend on
    a caller's behalf."""
    status, _payload, port = _post_turn(tmp_path, _turn())
    assert status == 200
    assert _declaration(port).splitlines()[3] == "posture: reduced"


def test_the_declared_local_embedded_backend_is_the_one_the_turn_uses(tmp_path):
    status, _payload, port = _post_turn(
        tmp_path, _turn(),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    declaration = _declaration(port)
    assert "posture: full" in declaration
    assert f"retrieval provider profile: {kn.PROFILE_LOCAL_EMBEDDED}" in declaration


def test_the_production_entrypoints_declare_the_self_hosted_profile():
    """An operator must be able to read what their install talks to, so the
    ENTRYPOINTS declare it — the same discipline `real_notebook_adapter`
    carries and asserted the same way, against the source that declares it."""
    serve_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "serve.py").read_text(encoding="utf-8")
    cli_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                  / "cli.py").read_text(encoding="utf-8")
    assert 'build_kwargs.setdefault("knowledge_declaration",' in serve_source
    assert "SELF_HOSTED_LOCAL_EMBEDDED" in serve_source
    assert "SELF_HOSTED_LOCAL_EMBEDDED" in cli_source


def test_the_route_reads_the_declaration_and_never_selects_a_backend(tmp_path):
    """"a backend MUST NOT be selected at runtime by a turn, a prompt, or a
    heuristic" — asserted against the ROUTE's own source, because that is the
    one place a per-turn choice could be introduced."""
    serve_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "serve.py").read_text(encoding="utf-8")
    assert "doxbench_knowledge.build_backend(declaration)" in serve_source
    for forbidden in ("build_backend(body", "build_backend(payload",
                      "build_backend(message", "backend_for_turn",
                      "backend_from_prompt", "choose_backend"):
        assert forbidden not in serve_source, forbidden


def test_the_index_is_built_only_from_CONFINED_sources(tmp_path):
    """Codex review of PR #216, CODEX-A. The reindex that precedes the search
    is itself governed: `_indexed_sources` reads `projection.context_paths`,
    which IS the tile's staged set and is exactly what `confined_refs` computes
    the admissible set from — so the index is a SUBSET of the confinement by
    construction, not by filtering its answers afterwards.

    Asserted rather than argued, because "the provider is handed the rail"
    only means anything if what it was given to search was confined too."""
    from test_doxbench_routes import _handler_class, _serving

    with _serving(tmp_path,
                  knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                  ) as (httpd, _host, _port):
        handler = _handler_class(httpd)
        from ideation_dashboard.doxbench_scope import ScopeKey, resolve_scope
        from ideation_dashboard.generator import generate_snapshot
        from conftest import BASE_REPO, PINNED_REVISION, FakeGit

        snapshot = generate_snapshot(BASE_REPO, "fixture-repo",
                                     source_revision=PINNED_REVISION,
                                     git=FakeGit())
        key = ScopeKey(repository="fixture-repo", ref="main",
                       tile_kind="staged", tile_id="ideation-governance")
        projection = resolve_scope(snapshot, key, source_root=BASE_REPO)
        sources, _unreadable = handler._indexed_sources(handler, projection)

    indexed = {source.ref for source in sources}
    confined = pk.confined_refs(projection)
    assert indexed, "nothing was indexed; this proves nothing"
    assert indexed <= confined


def test_a_server_built_with_no_kwarg_binds_the_REAL_packet_assembler(tmp_path):
    """RE-VERIFY NF6. The `packet_assembler` seam carries the governance rails
    — the confinement, the lifecycle-status exemption and the bounds fit all
    live inside the assembler — so a swapped one bypasses all three while still
    passing the leash, which the reviewer proved by driving 560 KB of
    out-of-confinement text to a 200.

    A seam that powerful gets the same guard `knowledge_declaration` has: the
    default is asserted to be the real function, and neither production
    entrypoint is allowed to pass the argument at all. The injection stays
    available to tests, which is what makes the leash testable end to end, but
    nothing in a shipped path can reach it."""
    from test_doxbench_routes import _handler_class, _serving

    with _serving(tmp_path) as (httpd, _host, _port):
        bound = _handler_class(httpd).packet_assembler
    assert bound is pk.assemble_packet


def test_neither_entrypoint_passes_a_packet_assembler(tmp_path):
    """The production entrypoints declare the notebook adapter and the
    retrieval backend explicitly, and must NOT declare this: an install that
    could name its own packet assembler could name one that skips a rail."""
    import ast

    calls = 0
    for module in ("serve.py", "cli.py"):
        path = REPO_ROOT / "scripts" / "ideation_dashboard" / module
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            target = node.func
            name = (target.attr if isinstance(target, ast.Attribute)
                    else getattr(target, "id", None))
            if name != "build_server":
                continue
            calls += 1
            passed = {kw.arg for kw in node.keywords}
            assert "packet_assembler" not in passed, module
            # the retrieval backend, by contrast, MUST be declared here
            assert "knowledge_declaration" in passed or any(
                kw.arg is None for kw in node.keywords), module
    assert calls >= 2, "the entrypoint call sites moved; this guard found none"

    # and `build_server`'s own default is the real function, not an absence
    serve_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "serve.py").read_text(encoding="utf-8")
    assert "else doxbench_packet.assemble_packet)" in serve_source


def test_a_tile_that_cannot_be_indexed_degrades_rather_than_failing(tmp_path):
    """An unreadable corpus is the same POSTURE as an undeclared backend, not
    a turn failure: `_knowledge_service` answers None and the reduced packet
    rides."""
    class Unbuildable:
        installation = kn.INSTALL_TENANT
        profile_id = "vertex-hosted"
        networked = True
        credentialed = True
        declared_by = "a tenant install this release cannot serve"

    status, _payload, port = _post_turn(tmp_path, _turn(),
                                        knowledge_declaration=Unbuildable())
    assert status == 200
    assert "posture: reduced" in _declaration(port)


# ===========================================================================
# EVIDENCE COMES FROM THE TILE'S OWN STAGED SET (task 10.5)
# ===========================================================================


def test_evidence_is_drawn_from_the_tiles_staged_set_and_carries_its_status(
        tmp_path):
    status, _payload, port = _post_turn(
        tmp_path,
        _turn(message="Which doc health checks and DTN register notes apply?"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    sections = _packet_sections(port)
    evidence_keys = [key for key in sections
                     if key.startswith(pk.EVIDENCE_SECTION_PREFIX)]
    assert evidence_keys, "the tile's own staged set produced no evidence"
    for key in evidence_keys:
        ref = key[len(pk.EVIDENCE_SECTION_PREFIX):]
        assert ref in TILE_EVIDENCE
        assert "Status: " in sections[key]


def test_the_outline_and_the_loaded_buffers_are_not_carried_twice(tmp_path):
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="outline governance staging"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    sections = _packet_sections(port)
    assert (pk.EVIDENCE_SECTION_PREFIX + OUTLINE_PATH) not in sections
    assert "outline_buffer" in sections


def test_a_retrieved_document_does_not_become_a_buffer_section(tmp_path):
    """The state authority, at the route: the prompt's buffer sections are
    exactly the buffers the REQUEST supplied, whatever retrieval found."""
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    sections = _packet_sections(port)
    buffer_sections = [key for key in sections
                       if key.startswith("document_buffer:")]
    assert buffer_sections == ["document_buffer:document"]
    for ref in TILE_EVIDENCE:
        assert ("document_buffer:" + ref) not in sections


# ===========================================================================
# THE TWO CAPABILITIES ARE INDEPENDENT (task 10.7, design §3.4)
# ===========================================================================


def test_a_live_model_with_no_knowledge_service_is_a_reduced_packet_not_a_refusal(
        tmp_path):
    """Design §3.4's first independence claim, and the one that would be
    easiest to get wrong: a missing knowledge service must not fail a turn."""
    status, payload, port = _post_turn(tmp_path, _turn())
    assert status == 200
    assert payload["kind"]
    assert port.calls.count("dispatch") == 1
    declaration = _declaration(port)
    assert "posture: reduced" in declaration
    assert "no unbounded context was substituted" in declaration
    assert "no rail was bypassed" in declaration


def test_a_live_knowledge_service_with_no_model_leaves_the_editor_usable(
        tmp_path):
    """Design §3.4's second claim: a live knowledge service with no model is
    an editor with retrieval that nothing consumes yet. The route's existing
    refusal shape and gate order are UNCHANGED — the packet does not soften a
    model-capability refusal, and it does not leak into one either."""
    status, payload, _port = _post_turn(
        tmp_path, _turn(), port=_CatalogOnlyPort(_catalog()),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    _assert_refusal(status, payload,
                    serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    for key in payload:
        assert "packet" not in key
    for ref in TILE_EVIDENCE:
        assert ref not in str(payload)


def test_the_reduced_posture_does_not_change_the_turns_own_success_shape(
        tmp_path):
    """"MUST NOT ... make the editors unusable": the same request answers with
    the same released envelope whether or not a knowledge service exists."""
    without = _post_turn(tmp_path, _turn())
    with_service = _post_turn(
        tmp_path, _turn(), knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert without[0] == with_service[0] == 200
    assert set(without[1]) == set(with_service[1])
    assert without[1]["kind"] == with_service[1]["kind"]


# ===========================================================================
# THE LEASH, AT THE ROUTE (task 10.4; adversarial review F1)
# ===========================================================================

FOREIGN_SCOPE = ScopeKey(repository="some-other-repo", ref="main",
                         tile_kind="staged", tile_id="a-different-tile")


def _bad_packet_assembler(*, axis, good_after_first=False):
    """An assembler that hands the route a packet the leash must reject.

    This is the seam the review's own repro used by hand: `require_valid` can
    only be exercised end to end by a route that is GIVEN a stale or foreign
    packet, and no legitimate input produces one."""
    state = {"calls": 0}

    def _assemble(**kwargs):
        state["calls"] += 1
        good = state["calls"] > 1 and good_after_first
        packet = pk.assemble_packet(**{**kwargs, "knowledge": None})
        if good:
            return packet
        if axis == "scope":
            return dataclasses.replace(packet, scope=FOREIGN_SCOPE)
        if axis == "purpose":
            return dataclasses.replace(packet, purpose="doxbench-share-session")
        return dataclasses.replace(packet, issued_at=0.0, expires_at=1.0)

    _assemble.calls = state
    return _assemble


@pytest.mark.parametrize("axis", ["purpose", "scope", "expiry"])
def test_the_route_refuses_a_packet_that_fails_its_leash_on_any_axis(tmp_path,
                                                                     axis):
    assembler = _bad_packet_assembler(axis=axis)
    status, payload, port = _post_turn(tmp_path, _turn(),
                                       packet_assembler=assembler)
    _assert_refusal(status, payload,
                    serve_mod.DOXBENCH_ERR_CONTEXT_PACKET_INVALID)
    assert status == 500
    # nothing was dispatched: the leash is checked BEFORE any provider is
    # reached, so a foreign packet never becomes a prompt
    assert port.calls.count("dispatch") == 0
    # and the route asked for a NEW packet before giving up, exactly as the
    # delta's "reject it and request a new one" says
    assert assembler.calls["calls"] == 2


@pytest.mark.parametrize("axis", ["purpose", "scope", "expiry"])
def test_a_reissued_packet_is_accepted_and_the_turn_proceeds(tmp_path, axis):
    """"Request a new one" is a REQUEST, not a formality: when the reissued
    packet is valid the turn is served, and only a second failure refuses."""
    assembler = _bad_packet_assembler(axis=axis, good_after_first=True)
    status, _payload, port = _post_turn(tmp_path, _turn(),
                                        packet_assembler=assembler)
    assert status == 200
    assert port.calls.count("dispatch") == 1
    assert assembler.calls["calls"] == 2


def test_a_rejected_packet_leaks_nothing_into_the_refusal(tmp_path):
    assembler = _bad_packet_assembler(axis="scope")
    status, payload, _port = _post_turn(
        tmp_path, _turn(), packet_assembler=assembler)
    assert status == 500
    from test_doxbench_routes import _TURN_SENTINELS
    for sentinel in _TURN_SENTINELS:
        assert sentinel not in str(payload)
    assert "some-other-repo" not in str(payload)


# ===========================================================================
# THE BOUNDS RAIL'S TWO ARMS, AT THE ROUTE (task 10.3; adversarial review F2)
# ===========================================================================


def _fat_checkout(tmp_path):
    """A copy of the fixture checkout whose two brainstorm notes are each big
    enough to blow the packet bound on their own — the review's own repro,
    which a real corpus reproduces with documents it already holds."""
    root = tmp_path / "fat-checkout"
    if root.exists():
        # IDEMPOTENT: a caller that needs the same fat checkout for several
        # ceilings must not have to remember that building it twice explodes.
        return root
    shutil.copytree(BASE_REPO, root)
    for ref in TILE_EVIDENCE:
        path = root / ref
        path.write_text(
            path.read_text(encoding="utf-8") + "\n\n"
            + ("doc health dtn register staging governance " * 8000),
            encoding="utf-8")
    return root


def test_server_selected_evidence_over_the_bound_FITS_instead_of_refusing(
        tmp_path):
    """RE-PINNED BEHAVIOUR (F2). This turn used to answer HTTP 413
    `request_limit_exceeded` — blaming a few-hundred-byte request for hundreds
    of KB the SERVER selected, and refusing every turn on that tile forever."""
    status, payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
        checkout_root=_fat_checkout(tmp_path))
    assert status == 200, payload
    declaration = _declaration(port)
    assert "selected out to fit this packet's bound, best-ranked first" in declaration
    for ref in TILE_EVIDENCE:
        assert ref in declaration
    assert "one retrieval call away" in declaration
    assert "nothing was shortened" in declaration


def test_a_fitted_packet_carries_what_it_kept_WHOLE_and_drops_the_rest(tmp_path):
    """Fitting is selection, never truncation: what survives survives byte for
    byte. Built with ONE oversized document so the tile's other note is still
    small enough to be carried — otherwise this test would pass vacuously on a
    packet that carried no evidence at all."""
    root = tmp_path / "one-fat-checkout"
    shutil.copytree(BASE_REPO, root)
    fat, lean = TILE_EVIDENCE
    fat_path = root / fat
    fat_path.write_text(
        fat_path.read_text(encoding="utf-8") + "\n\n"
        + ("doc health dtn register staging governance " * 8000),
        encoding="utf-8")

    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
        checkout_root=root)
    assert status == 200
    sections = _packet_sections(port)
    carried = {key[len(pk.EVIDENCE_SECTION_PREFIX):]: text
               for key, text in sections.items()
               if key.startswith(pk.EVIDENCE_SECTION_PREFIX)}
    assert carried, "the fit dropped everything; this test would prove nothing"
    assert fat not in carried
    for ref, text in carried.items():
        assert (root / ref).read_text(encoding="utf-8") in text
    assert fat in _declaration(port)


def test_the_genuine_refusal_arm_answers_409_and_names_its_dimension(tmp_path):
    """The only refusal left: the session's own threads exceed the bound
    alone. It carries the measured dimension, and its message does NOT blame
    the request."""
    def _oversized_threads(**kwargs):
        packet = pk.assemble_packet(**{**kwargs, "knowledge": None})
        raise pk.PacketBoundExceeded(
            "context_packet_bytes", pk.MAX_PACKET_BYTES + 1,
            pk.MAX_PACKET_BYTES)

    status, payload, port = _post_turn(tmp_path, _turn(),
                                       packet_assembler=_oversized_threads)
    assert status == 409
    assert payload["error"] == serve_mod.DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED
    assert payload["limit"] == {"dimension": "context_packet_bytes",
                                "measured": pk.MAX_PACKET_BYTES + 1,
                                "maximum": pk.MAX_PACKET_BYTES}
    assert "request" not in payload["message"]
    assert "thread" in payload["message"]
    assert port.calls.count("dispatch") == 0


def test_FULL_coverage_is_stated_on_a_real_route(tmp_path):
    """RENAMED (re-verify NF3). This asserted the FULL-coverage sentence while
    claiming to be the shortfall test, so the shortfall branch had no route
    coverage at all — the branch that matters, because it is the one that
    contradicts the packet's own lossless note."""
    status, _payload, port = _post_turn(
        tmp_path, _turn(), knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    assert "the index covered all 3 documents" in _declaration(port)


def test_the_coverage_SHORTFALL_is_stated_on_a_real_route(tmp_path):
    """The branch itself, driven the way the reviewer's own repro drives it:
    squeeze the index bound on the live handler below the tile's staged-set
    size, so refs that ARE confined were never indexed."""
    from test_doxbench_routes import (
        _capabilities, _console_headers, _handler_class, _request, _serving,
        CHAT_ROUTE,
    )

    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                  ) as (httpd, host, port):
        _handler_class(httpd).MAX_INDEXED_SOURCES = 1
        caps = _capabilities(host, port)
        status, _payload, _headers, _raw = _request(
            host, port, "POST", CHAT_ROUTE,
            body=_turn(message="doc health checks"),
            headers=_console_headers(caps))

    assert status == 200
    declaration = _declaration(fake)
    assert "the index covered 1 of 3 documents" in declaration
    assert "2 were beyond the declared index bound" in declaration
    assert "not one retrieval call away either" in declaration


class _MissingFirst:
    """A projection whose FIRST staged-set entry does not exist on disk."""
    context_paths = ("ideation/staging/does-not-exist/GONE.md",) + TILE_EVIDENCE
    source_revision = "r" * 40


def test_an_unreadable_entry_does_not_consume_index_capacity(tmp_path):
    """Codex review of PR #216, CODEX-C, reproduced then fixed. Slicing
    `context_paths` before filtering let a missing file eat a slot, so a bound
    of 2 over three paths indexed ONE and never considered the readable
    document behind it — and the coverage line then blamed the index bound for
    an omission the bound had nothing to do with."""
    from test_doxbench_routes import _handler_class, _serving

    with _serving(tmp_path,
                  knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                  ) as (httpd, _host, _port):
        handler = _handler_class(httpd)
        handler.MAX_INDEXED_SOURCES = 2
        sources, unreadable = handler._indexed_sources(handler, _MissingFirst())

    # the bound is on what is INDEXED: both readable documents made it in
    assert [source.ref for source in sources] == list(TILE_EVIDENCE)
    assert unreadable == ("ideation/staging/does-not-exist/GONE.md",)


def test_the_route_states_unreadable_and_beyond_bound_apart(tmp_path):
    """The same fix, seen where a human reads it: the packet's own
    declaration."""
    from test_doxbench_routes import (
        _capabilities, _console_headers, _handler_class, _request, _serving,
        CHAT_ROUTE,
    )

    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                  ) as (httpd, host, port):
        handler = _handler_class(httpd)
        handler.MAX_INDEXED_SOURCES = 1
        original = handler._indexed_sources

        def _with_an_unreadable(self, projection):
            sources, _unreadable = original(self, projection)
            return sources, ("ideation/staging/topic/UNREADABLE.md",)

        handler._indexed_sources = _with_an_unreadable
        caps = _capabilities(host, port)
        status, _payload, _headers, _raw = _request(
            host, port, "POST", CHAT_ROUTE,
            body=_turn(message="doc health checks"),
            headers=_console_headers(caps))

    assert status == 200
    declaration = _declaration(fake)
    assert "could not be read at this revision" in declaration
    assert "beyond the declared index bound" in declaration


def test_the_evidence_revision_is_stated_on_a_real_route(tmp_path):
    """F5: evidence is the SERVED CHECKOUT's bytes, not the session's."""
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    declaration = _declaration(port)
    assert "evidence bytes are the served checkout at revision" in declaration
    assert "NOT this session's worktree" in declaration


# ===========================================================================
# THE PACKET COMPOSES WITH THE MODEL'S INPUT LIMIT (Codex review, CODEX-B)
# ===========================================================================


def _prompt_bytes(port) -> int:
    from ideation_dashboard.doxbench_hash import utf8_size

    return sum(utf8_size(section.text)
               for section in port.dispatched[0].sections)


def test_the_packet_is_FITTED_to_what_the_request_left_of_the_input_limit(
        tmp_path):
    """The request bytes are measured against the catalog's effective input
    limit BEFORE the packet exists, and the packet's sections are appended
    after — so without this composition an accepted turn could dispatch a
    prompt past the model's declared capacity and fail at the provider instead
    of at a measured bound.

    Fitted rather than refused, for the reason the bounds rework recorded:
    a refusal here would resurrect the un-actionable-refusal class."""
    narrow = _port(_catalog(input_limit_bytes=40_000))
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        port=narrow, knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
        checkout_root=_fat_checkout(tmp_path))
    assert status == 200
    assert _prompt_bytes(port) <= 40_000
    # it fitted by SELECTING less, and said so
    assert "selected out to fit this packet's bound" in _declaration(port)


def test_a_generous_ceiling_still_carries_evidence(tmp_path):
    """The composition must not starve a turn that has room: the same tile at
    the default ceiling still carries its evidence."""
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    sections = _packet_sections(port)
    assert [key for key in sections
            if key.startswith(pk.EVIDENCE_SECTION_PREFIX)]


def test_the_scaffold_reserve_is_MEASURED_adequate_not_asserted(tmp_path):
    """`PROMPT_SCAFFOLD_RESERVE_BYTES` is a declared allowance for what the
    prompt spends outside the packet and outside the measured request. Its
    adequacy is checked against a REAL rendered prompt rather than argued."""
    for ceiling in (40_000, 60_000, 200_000):
        narrow = _port(_catalog(input_limit_bytes=ceiling))
        status, _payload, port = _post_turn(
            tmp_path, _turn(message="doc health checks dtn register"),
            port=narrow, knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
            checkout_root=_fat_checkout(tmp_path))
        assert status == 200, ceiling
        assert _prompt_bytes(port) <= ceiling, ceiling


def test_a_budget_of_zero_carries_no_evidence_rather_than_refusing(tmp_path):
    """A turn with no room left for evidence is still a turn: the fit carries
    none, names what it dropped, and the editor keeps working."""
    assert pk.packet_budget_for(input_limit_bytes=1_000,
                                request_bytes=900) == 0
    status, _payload, port = _post_turn(
        tmp_path, _turn(message="doc health checks dtn register"),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
        packet_assembler=lambda **kw: pk.assemble_packet(
            **{**kw, "max_packet_bytes": 0}))
    assert status == 200
    sections = _packet_sections(port)
    assert not [key for key in sections
                if key.startswith(pk.EVIDENCE_SECTION_PREFIX)]


def test_non_evidence_over_the_remaining_budget_refuses_via_the_409_arm(
        tmp_path):
    """The genuinely-unfittable arm: what the packet must carry and nothing
    selected — the session's own threads — over the REMAINING budget refuses
    with the measured dimension, not with a provider failure."""
    def _threads_over_budget(**kwargs):
        return pk.assemble_packet(**{**kwargs, "max_packet_bytes": 10,
                                     "knowledge": None})

    from ideation_dashboard import doxbench_threads as dt

    def _with_a_big_thread(**kwargs):
        scope = kwargs["scope"]
        thread = dt.DocumentThread(
            document="ideation/staging/ideation-governance/README.md",
            scope=dt.ThreadScope(repository=scope.repository,
                                 tile_kind=scope.tile_kind,
                                 tile_id=scope.tile_id),
            state=dt.ThreadState(active_goal="g" * 500))
        return pk.assemble_packet(**{
            **kwargs, "max_packet_bytes": 10, "knowledge": None,
            "selected_key": "ideation/staging/ideation-governance/README.md",
            "threads": {"ideation/staging/ideation-governance/README.md": thread},
        })

    status, payload, port = _post_turn(tmp_path, _turn(),
                                       packet_assembler=_with_a_big_thread)
    assert status == 409
    assert payload["error"] == (
        serve_mod.DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED)
    assert payload["limit"]["dimension"] == "context_packet_bytes"
    assert payload["limit"]["maximum"] == 10
    assert port.calls.count("dispatch") == 0


# ===========================================================================
# TELEMETRY (task 10.8)
# ===========================================================================


def test_a_turn_records_one_content_free_usage_event(tmp_path):
    seen: dict = {}

    def _inspect(handler):
        seen["meter"] = handler.usage_meter

    status, _payload, port = _post_turn(
        tmp_path, _turn(), knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
        inspect_handler=_inspect)
    assert status == 200
    meter = seen["meter"]
    scopes = meter.scopes()
    assert len(scopes) == 1
    session = meter.session(scopes[0])
    assert session.turn_count == 1
    assert session.packet_bytes > 0
    assert session.prompt_bytes > session.packet_bytes

    emitted = session.as_dict()
    # CONTENT-FREE: no sentinel from the request survives anywhere in the
    # record, and the four fields this console cannot fill are DECLARED absent
    # rather than filled with something plausible.
    from test_doxbench_routes import _TURN_SENTINELS
    for sentinel in _TURN_SENTINELS:
        assert sentinel not in str(emitted)
    for field in ("client", "domain", "bill_to", "customer_subject_ref"):
        assert emitted[field]["value"] is None
        assert emitted[field]["declared_absent"] is True
        assert emitted[field]["reason"].strip()
    tokens = emitted["usage_units"]["provider_tokens"]
    assert tokens["declared_absent"] is True
    assert "fabricated measurement" in tokens["reason"]


def test_the_meter_is_bound_per_server_process(tmp_path):
    from test_doxbench_routes import _serving, _handler_class

    with _serving(tmp_path) as (first, _host, _port):
        with _serving(tmp_path) as (second, _host2, _port2):
            one = _handler_class(first).usage_meter
            two = _handler_class(second).usage_meter
    assert isinstance(one, tel.UsageMeter)
    assert one is not two


def test_a_usage_record_cannot_be_built_with_a_placeholder_metering_field():
    """The absence is structural: `client`, `domain`, `bill_to` and the
    subject reference accept ONLY a declared absence, so a later caller
    cannot quietly fill one in."""
    from ideation_dashboard.doxbench_scope import ScopeKey

    scope = ScopeKey(repository="fixture-repo", ref="main", tile_kind="staged",
                     tile_id="ideation-governance")
    for field in ("client", "domain", "bill_to", "customer_subject_ref"):
        with pytest.raises(tel.TelemetryRefused) as raised:
            tel.TurnUsage(operation=tel.OPERATION_CONTEXT_PACKET, scope=scope,
                          provider_role=tel.PROVIDER_ROLE_RETRIEVAL,
                          provider_id=kn.PROFILE_LOCAL_EMBEDDED,
                          packet_posture=pk.POSTURE_FULL, source_count=1,
                          exempt_source_count=0, packet_bytes=10,
                          prompt_bytes=20, **{field: "acme-corp"})
        assert "declared absence" in str(raised.value)
