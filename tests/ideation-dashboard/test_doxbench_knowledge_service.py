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

from conftest import (  # noqa: F401  (sys.path side effect)
    BASE_REPO, REPO_ROOT, serve_surface_source,
)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_telemetry as tel  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402
from ideation_dashboard.doxbench_scope import ScopeKey  # noqa: E402

from test_doxbench_routes import (  # noqa: E402
    CHAT_ROUTE, OUTLINE_PATH, _assert_refusal, _capabilities, _catalog,
    _CatalogOnlyPort, _console_headers, _port, _post_turn, _request, _serving,
    _turn, _turn_v2, _UNSET, released_only,
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
    # THE SERVE SURFACE, not one file of it (§ 2.4 PR 2 of 4 moved this
    # code to a sibling module; the scan widened rather than narrowed).
    serve_source = serve_surface_source()
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


def test_the_widened_record_keeps_the_same_shape_and_says_what_it_ran_on(
        tmp_path):
    """THE SAME CLAIM ON THE WIDENED LANE, and what contract-v1.40 changed
    about it.

    The clause above is unchanged and still holds: the two turns answer in the
    SAME envelope with the SAME keys, so nothing a consumer parses moves when
    the knowledge service disappears. What v1.40 adds is that the two records
    now DIFFER in what they say — one states `full`, the other `reduced` with
    its reason — which is the whole point of the release and is the difference
    that used to be invisible to every reader of the record.

    This is deliberately the STRONGER form of the sibling test above, not a
    relaxation of it: the key-set equality is asserted first, and the posture
    difference is asserted inside the one key whose job is to carry it."""
    without = _post_turn(tmp_path, _turn_v2())
    with_service = _post_turn(
        tmp_path, _turn_v2(),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert without[0] == with_service[0] == 200
    assert set(without[1]) == set(with_service[1])
    assert "context_packet" in without[1]
    assert without[1]["context_packet"] == {
        "posture": "reduced",
        "reduced_reason": pk.REDUCED_NO_KNOWLEDGE_SERVICE,
    }
    assert with_service[1]["context_packet"] == {"posture": "full"}


# ===========================================================================
# THE REDUCED POSTURE IS STATED ON THE RECORD (task 10.7, contract-v1.40)
#
# The ratified sentence ends "with the reduced posture STATED", and until this
# release the statement lived only inside the assembled packet — where the
# tests above read it, out of the prompt envelope the fake port was handed.
# That is a real statement and it was never readable by the CONSUMER of the
# turn or by the human who asked the question. These drive the REAL route and
# read the posture off the WIRE.
# ===========================================================================


def test_a_widened_turn_with_no_knowledge_service_records_the_reduced_posture(
        tmp_path):
    """The scenario, end to end: no knowledge service, a turn that SUCCEEDS,
    and a record that says what it ran on and why — including, in the reason's
    own words, that nothing unbounded was substituted and no rail was bypassed.

    The two halves are asserted TOGETHER on purpose: a success whose record
    hid the reduction, and a refusal, are the two failures this requirement is
    written against, and one assertion catches neither."""
    status, payload, port = _post_turn(tmp_path, _turn_v2())
    assert status == 200
    assert payload["kind"] == "workbench-chat-turn-v2-success"
    assert port.calls.count("dispatch") == 1
    assert payload["context_packet"] == {
        "posture": "reduced",
        "reduced_reason": pk.REDUCED_NO_KNOWLEDGE_SERVICE,
    }
    reason = payload["context_packet"]["reduced_reason"]
    assert "no unbounded context was substituted" in reason
    assert "no rail was bypassed" in reason


def test_a_widened_turn_with_a_live_knowledge_service_records_the_full_posture(
        tmp_path):
    """The inverse, which is what makes the reduced record MEAN anything: with
    the declared backend indexed and answering, the record states `full` — and
    carries NO reason, because a full packet has none to carry."""
    status, payload, _port = _post_turn(
        tmp_path, _turn_v2(),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    assert payload["context_packet"] == {"posture": "full"}
    assert "reduced_reason" not in payload["context_packet"]


def test_the_record_and_the_packets_own_declaration_state_the_same_posture(
        tmp_path):
    """ONE DERIVATION, proven rather than asserted in a comment. The packet
    writes its posture into the prompt's declaration section and the route
    writes it onto the wire; both come from the same `ContextPacket`, so a
    reader of the transcript and a reader of the record can never be told two
    different things about the same turn."""
    for declaration, posture in ((None, "reduced"),
                                 (kn.SELF_HOSTED_LOCAL_EMBEDDED, "full")):
        status, payload, port = _post_turn(
            tmp_path, _turn_v2(), knowledge_declaration=declaration)
        assert status == 200
        assert f"posture: {posture}" in _declaration(port)
        assert payload["context_packet"]["posture"] == posture


def test_a_backend_that_REFUSES_records_its_own_reason_not_the_absent_one(
        tmp_path, monkeypatch):
    """THE DERIVATION READS THE PACKET, and this is the case that proves it.

    There are TWO ways a turn reduces: no knowledge service was declared, and a
    declared one REFUSED the retrieval. A derivation written as "did this serve
    have a knowledge service?" would answer `full` here — a live backend was
    declared and built — and the record would state the exact opposite of what
    happened. Only the packet knows, so only the packet is read."""
    class _RefusingBackend(kn.LocalHybridBackend):
        def retrieve(self, query, *, confined_to, limit,
                     thread_signals=frozenset()):
            raise kn.RetrievalRefused("this backend declines")

    monkeypatch.setattr(kn, "build_backend", lambda declaration: _RefusingBackend())
    status, payload, port = _post_turn(
        tmp_path, _turn_v2(),
        knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED)
    assert status == 200
    assert port.calls.count("dispatch") == 1
    assert payload["context_packet"] == {
        "posture": "reduced",
        "reduced_reason": pk.REDUCED_RETRIEVAL_REFUSED,
    }
    # …and it is the OTHER reason, not the absent-service one. The two are
    # different facts and the record keeps them apart.
    assert payload["context_packet"]["reduced_reason"] != (
        pk.REDUCED_NO_KNOWLEDGE_SERVICE)


# `test_the_deprecated_v1_record_still_succeeds_and_still_cannot_say_so` stood
# here. It pinned contract-v1.40's RECORDED LIMITATION as a limitation rather
# than leaving it to prose: the deprecated v1 success envelope was CLOSED and
# that release deliberately did not widen it, so a v1 turn that ran reduced
# succeeded — the ratified "MUST NOT make the editors unusable" half — and
# carried no posture on the wire, with the reduction stated only inside the
# packet. It would have failed if a later release widened the v1 envelope, which
# was the point: that would have broken the deprecation's byte-identity promise.
#
# DELETED at contract-v3.0 (retire-doxbench-chat-turn-v1), because the
# limitation is gone with the envelope rather than fixed: there is no longer a
# turn this serve can answer whose record cannot state its posture. The
# byte-identity promise it also guarded expired at the same moment — the whole
# release IS the removal of those bytes. Every surviving turn states its posture
# on the wire, which the four tests above assert directly.


def test_every_shipped_reduction_reason_fits_the_released_bound(tmp_path):
    """THE AUTHORED CONSTANTS, held to the STRICTER unit — and the unit is the
    point (adversarial review S2 corrected this docstring, which used to call
    the released ceiling a "500-byte" one).

    The released bound is `maxLength: 500`, which JSON Schema counts in CODE
    POINTS. This test checks the shipped reasons in UTF-8 BYTES against that
    same number, which is STRICTER: bytes ≥ code points for every string, so a
    reason that passes here cannot fail the shape. That is deliberate and it is
    a rule about text THIS REPOSITORY AUTHORS, not a rule the wire imposes — a
    conformant producer elsewhere may ship 500 CJK characters at 1,500 bytes and
    this contract accepts it.

    What enforces the WIRE bound is not this test: it is
    `serve.doxbench_context_packet`, which refuses an over-long reason in code
    points before any provider is dispatched (see the route test below). This
    test is the belt on the constants; that is the braces on the record."""
    import yaml

    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "schemas"
         / "xfactory-workbench-chat-turn.schema.yaml").read_text(
             encoding="utf-8"))
    bound = schema["$defs"]["context_packet"]["properties"][
        "reduced_reason"]["maxLength"]
    reasons = [value for name, value in vars(pk).items()
               if name.startswith("REDUCED_") and isinstance(value, str)]
    assert reasons, "the reduction reasons moved; this guard found none"
    for reason in reasons:
        assert 0 < len(reason.encode("utf-8")) <= bound, reason[:60]


def test_the_construction_gate_and_the_derivation_agree_on_PRESENCE(tmp_path):
    """THE RELEASE CLAIMS THREE GATES ASSERT ONE RULE, and at the blank string
    they did not (Copilot review of PR #256, finding 1). The released shape
    forbids `reduced_reason`'s PRESENCE on a full posture; `ContextPacket` and
    `serve.doxbench_context_packet` both forbade only a TRUTHY one, so
    `{full, ""}` sailed through both and the record was emitted with the key
    silently dropped.

    Pinned here as the agreement it is supposed to be — and pinned in BOTH
    directions, because the fix must not have been a blanket tightening: the
    REDUCED arm still refuses a blank (there a blank is unusable, which is the
    shape's `minLength: 1`) and still accepts a real reason."""
    scope = ScopeKey(repository="fixture-repo", ref="main",
                     tile_kind="staged", tile_id="t")

    def _packet(posture, reason):
        return pk.ContextPacket(
            purpose=pk.PACKET_PURPOSE_CHAT_TURN, scope=scope, posture=posture,
            sources=(), issued_at=0.0, expires_at=1.0, reduced_reason=reason)

    class _Duck:
        def __init__(self, posture, reason):
            self.posture, self.reduced_reason = posture, reason

    # FULL: the key's presence is the refusal, whatever it holds.
    for blocked in ("", "a real reason"):
        with pytest.raises(pk.PacketError):
            _packet(pk.POSTURE_FULL, blocked)
        with pytest.raises(pk.PacketError):
            serve_mod.doxbench_context_packet(_Duck(pk.POSTURE_FULL, blocked))
    # …and absence is the only thing that passes.
    assert _packet(pk.POSTURE_FULL, None).posture == pk.POSTURE_FULL
    assert serve_mod.doxbench_context_packet(
        _Duck(pk.POSTURE_FULL, None)) == {"posture": "full"}

    # REDUCED: unweakened, and a reason must be a STRING (Codex review of
    # PR #256). `if not reason:` let any truthy value through and `str()` then
    # MANUFACTURED a reason from it — `123` became "123", and a bare `object()`
    # became "<object object at 0x…>", a heap address in a durable record on the
    # degraded path. Same silent-normalisation class as the presence findings.
    for blocked in (None, "", 123, ["a", "b"], {"why": "x"}, object()):
        with pytest.raises(pk.PacketError):
            _packet(pk.POSTURE_REDUCED, blocked)
        with pytest.raises(pk.PacketError):
            serve_mod.doxbench_context_packet(_Duck(pk.POSTURE_REDUCED, blocked))
    assert serve_mod.doxbench_context_packet(
        _Duck(pk.POSTURE_REDUCED, "why")) == {
            "posture": "reduced", "reduced_reason": "why"}


def test_the_serve_side_ceiling_is_pinned_to_the_RELEASED_maxLength():
    """`CONTEXT_REDUCED_REASON_MAX_LENGTH` is a literal in a module that does
    not parse the schema per turn. This is what makes it authoritative anyway —
    the same discipline `MAX_ROUTING_TARGETS` got at contract-v1.38: the bound
    is read out of the RELEASED BYTES here and pinned equal, so the guard and
    the shape cannot drift into two ceilings."""
    import yaml

    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "schemas"
         / "xfactory-workbench-chat-turn.schema.yaml").read_text(
             encoding="utf-8"))
    assert serve_mod.CONTEXT_REDUCED_REASON_MAX_LENGTH == schema["$defs"][
        "context_packet"]["properties"]["reduced_reason"]["maxLength"]


def test_an_over_long_reason_refuses_BEFORE_a_provider_is_dispatched(tmp_path):
    """THE S2 DEFECT, closed and pinned. Before this guard the only thing
    between an over-long reason and the wire was the route's POST-dispatch
    self-validation, and the review reproduced the cost: 502 `response_invalid`
    with `dispatch` already counted — a provider call paid for, and the human's
    answer produced and then thrown away.

    Refused pre-dispatch now, on the route's existing packet boundary."""
    over = "x" * (serve_mod.CONTEXT_REDUCED_REASON_MAX_LENGTH + 1)
    status, payload, port = _post_turn(
        tmp_path, _turn_v2(),
        packet_assembler=_lying_packet_assembler(
            lambda p: object.__setattr__(p, "reduced_reason", over)))
    assert status == 400
    assert payload["error"] == serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST
    assert port.calls.count("dispatch") == 0


@released_only
def test_a_long_MULTIBYTE_reason_is_conformant_and_is_SERVED(tmp_path):
    """THE OTHER HALF OF THE UNIT QUESTION, and the reason the guard counts code
    points rather than bytes. 500 CJK characters is 1,500 UTF-8 bytes and is
    CONFORMANT under `maxLength: 500`; a byte-counting guard would have refused
    a record the released contract accepts, which is a worse defect than the one
    S2 found. The turn is served and the record carries the reason whole.

    DRIVEN THROUGH THE RELEASED VALIDATORS (adversarial review NEW-4), because
    otherwise it proves the wrong thing. The fixture schema declares
    `context_packet: {}` with no value rules, so under it this record would be
    accepted whatever the released bound said — "conformant" would be a claim
    about the fixture. Its sibling above needs no such treatment: the
    producer-side guard fires BEFORE any validator is consulted, so which
    validator is mounted cannot change that verdict."""
    cjk = "漢" * serve_mod.CONTEXT_REDUCED_REASON_MAX_LENGTH
    assert len(cjk.encode("utf-8")) == 1500
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  packet_assembler=_lying_packet_assembler(
                      lambda p: object.__setattr__(p, "reduced_reason", cjk)),
                  schema_validator_factory=_UNSET) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=_turn_v2(),
            headers=_console_headers(caps))
    assert status == 200, payload
    assert fake.calls.count("dispatch") == 1
    assert payload["context_packet"]["reduced_reason"] == cjk


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


def _lying_packet_assembler(mutate):
    """An assembler whose packet CONTRADICTS ITSELF about its own posture.

    `ContextPacket.__post_init__` refuses every one of these at construction,
    so the mutation is applied AFTER it — through `object.__setattr__`, which
    a frozen slotted dataclass cannot stop. That is not a contrived attack: the
    packet assembler is an INJECTED, duck-typed seam
    (`build_server(packet_assembler=…)`), and a collaborator behind it is under
    no obligation to be a `ContextPacket` at all. What must hold is that a
    record never states a posture the packet does not support."""
    def _assemble(**kwargs):
        packet = pk.assemble_packet(**kwargs)
        mutate(packet)
        return packet
    return _assemble


@pytest.mark.parametrize("mutate, why", [
    (lambda p: object.__setattr__(p, "reduced_reason", None),
     "reduced, with its reason removed"),
    (lambda p: object.__setattr__(p, "posture", pk.POSTURE_FULL),
     "full, still carrying a reduction reason"),
    # PRESENCE, NOT TRUTHINESS (Copilot review of PR #256, finding 1). This is
    # the instance the derivation used to accept: `if reason:` let a BLANK
    # through, and the record shipped with the key quietly dropped instead of
    # the turn failing closed. The released shape refuses the key's presence on
    # a full posture whatever it holds, so this boundary must too.
    (lambda p: (object.__setattr__(p, "posture", pk.POSTURE_FULL),
                object.__setattr__(p, "reduced_reason", "")),
     "full, carrying a BLANK reduction reason"),
    (lambda p: object.__setattr__(p, "posture", "degraded"),
     "a posture outside the released vocabulary"),
    (lambda p: object.__delattr__(p, "posture"),
     "no posture at all"),
])
def test_a_packet_that_lies_about_its_posture_refuses_the_turn(
        tmp_path, mutate, why):
    """FAIL-CLOSED, never a guessed posture (contract-v1.40, task 10.7).

    The derivation could have defaulted — `getattr(packet, "posture", "full")`
    would have made every one of these turns succeed with a record claiming a
    full context. It refuses instead, on the route's EXISTING packet boundary,
    so the answer is the same fixed `invalid_turn_request` every other
    structural packet refusal gives and nothing about the failure is new
    surface. Nothing is dispatched, because the derivation runs before the
    provider does."""
    status, payload, port = _post_turn(
        tmp_path, _turn_v2(),
        packet_assembler=_lying_packet_assembler(mutate))
    assert status == 400, why
    assert payload["error"] == serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST, why
    assert port.calls.count("dispatch") == 0, why


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


def _mid_checkout(tmp_path):
    """A checkout whose tile documents are ~60 KB each — big enough that a
    NARROWED model ceiling cannot afford them, small enough that the packet's
    OWN 256 KB bound easily can.

    That gap is the whole point: `_fat_checkout`'s ~344 KB documents exceed the
    packet bound by themselves, so they drop with or without the input-limit
    composition and a test built on them proves nothing about it. Found by
    revert-testing this very pin."""
    root = tmp_path / "mid-checkout"
    if root.exists():
        return root
    shutil.copytree(BASE_REPO, root)
    for ref in TILE_EVIDENCE:
        path = root / ref
        path.write_text(
            path.read_text(encoding="utf-8") + "\n\n"
            + ("doc health dtn register staging governance " * 1400),
            encoding="utf-8")
        assert 40_000 < path.stat().st_size < pk.MAX_PACKET_BYTES
    return root


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
        checkout_root=_mid_checkout(tmp_path))
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
    adequacy is checked against a REAL rendered prompt rather than argued.

    THE SHAPE MEASURED HERE CARRIES EVIDENCE AND NO THREADS, which is what §10
    ships: nothing wrote a sidecar at this point in the change's history, so the
    route supplied none. §11's obligation (tasks.md 11.5) is that the same
    measurement must hold once the route DOES carry threads, and the extension
    lives with the thread wiring it measures —
    `test_doxbench_thread_wiring.py::test_the_rendered_prompt_stays_inside_the_ceiling_WITH_threads`
    renders at three narrowed ceilings with a thread mirrored and evidence
    carried, sums `utf8_size(section.text)` across the assembled envelope, and
    compares it to the entry's effective input limit. This test stays as the
    evidence-only leg of the same measurement."""
    carried = []
    for ceiling in (40_000, 60_000, 200_000):
        narrow = _port(_catalog(input_limit_bytes=ceiling))
        status, _payload, port = _post_turn(
            tmp_path, _turn(message="doc health checks dtn register"),
            port=narrow, knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED,
            checkout_root=_mid_checkout(tmp_path))
        assert status == 200, ceiling
        assert _prompt_bytes(port) <= ceiling, ceiling
        carried.append(any(key.startswith(pk.EVIDENCE_SECTION_PREFIX)
                           for key in _packet_sections(port)))
    # the generous ceiling MUST carry evidence, or the reserve is being
    # "proved adequate" by a packet that spends nothing
    assert carried[-1] is True


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
