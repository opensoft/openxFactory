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

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_telemetry as tel  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402

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
