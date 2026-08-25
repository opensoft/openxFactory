"""CONTENT-FREE usage telemetry — the shape, the declared absences, and the
bounded meter (add-doxbench-editing-phase-b task 10.8; `memory-gateway`'s
`Usage Metering Is Gateway-Owned`, declared PARTIAL by this surface).

The route-level proof that a real turn emits one of these lives in
`test_doxbench_knowledge_service.py`. What this file pins is the shape itself:
that there is NO field a caller could put text in, that the four fields a
self-hosted console cannot fill accept only a declared absence, that a token
count is carried only when a provider REPORTS one, and that the meter is
bounded so a long serve cannot grow one.
"""

from __future__ import annotations

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_telemetry as tel  # noqa: E402
from ideation_dashboard.doxbench_scope import ScopeKey  # noqa: E402

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_telemetry.py")


def _scope(tile: str = "demo-topic") -> ScopeKey:
    return ScopeKey(repository="openxFactory", ref="main", tile_kind="staged",
                    tile_id=tile)


def _usage(scope=None, **over):
    fields = {
        "operation": tel.OPERATION_CONTEXT_PACKET,
        "scope": scope or _scope(),
        "provider_role": tel.PROVIDER_ROLE_RETRIEVAL,
        "provider_id": "local-embedded",
        "packet_posture": "full",
        "source_count": 4,
        "exempt_source_count": 1,
        "packet_bytes": 2048,
        "prompt_bytes": 8192,
    }
    fields.update(over)
    return tel.TurnUsage(**fields)


# ===========================================================================
# CONTENT-FREEDOM, BY CONSTRUCTION
# ===========================================================================


def test_every_field_is_a_count_a_label_a_scope_or_a_declared_absence():
    import dataclasses

    kinds = {field.name: field.type
             for field in dataclasses.fields(tel.TurnUsage)}
    assert set(kinds) == {
        "operation", "scope", "provider_role", "provider_id", "packet_posture",
        "source_count", "exempt_source_count", "packet_bytes", "prompt_bytes",
        "provider_tokens", "client", "domain", "bill_to",
        "customer_subject_ref"}
    for name in ("operation", "provider_role", "provider_id", "packet_posture"):
        assert "str" in str(kinds[name])


def test_a_label_may_not_carry_a_body_of_text():
    with pytest.raises(tel.TelemetryRefused) as raised:
        _usage(provider_id="local\nand a whole paragraph of packet content")
    assert "one label, never a body of text" in str(raised.value)


def test_the_operation_vocabulary_is_closed():
    assert tel.OPERATIONS == ("context_packet_created", "turn_dispatched")
    with pytest.raises(tel.TelemetryRefused):
        _usage(operation="anything_else")


def test_a_measured_dimension_is_a_non_negative_integer():
    for field in ("source_count", "exempt_source_count", "packet_bytes",
                  "prompt_bytes"):
        with pytest.raises(tel.TelemetryRefused):
            _usage(**{field: -1})
        with pytest.raises(tel.TelemetryRefused):
            _usage(**{field: "8192"})


def test_more_sources_cannot_be_exempt_than_the_packet_carried():
    with pytest.raises(tel.TelemetryRefused) as raised:
        _usage(source_count=2, exempt_source_count=3)
    assert "more sources were exempt" in str(raised.value)


# ===========================================================================
# THE DECLARED ABSENCES
# ===========================================================================


def test_the_four_unfillable_fields_are_declared_absences_with_reasons():
    emitted = _usage().as_dict()
    for field in ("client", "domain", "bill_to", "customer_subject_ref"):
        assert emitted[field] == {"value": None, "declared_absent": True,
                                  "reason": emitted[field]["reason"]}
        assert len(emitted[field]["reason"].split()) >= 8, field


def test_a_declared_absence_is_not_a_bare_null():
    """A null in a usage record reads as "not supplied yet" and invites a
    later caller to fill it in; this value says the field has no value HERE
    and why."""
    absence = tel.ABSENT_BILL_TO.as_dict()
    assert absence["value"] is None
    assert absence["declared_absent"] is True
    assert "placeholder" in absence["reason"]


def test_a_declared_absence_must_name_its_field_and_its_reason():
    with pytest.raises(tel.TelemetryRefused):
        tel.DeclaredAbsence("bill_to", "   ")
    with pytest.raises(tel.TelemetryRefused):
        tel.DeclaredAbsence("", "a reason")


def test_a_token_count_is_carried_only_when_a_provider_reports_one():
    """Bytes are measured exactly; tokens are never estimated from them,
    because a guessed unit in a usage record is a fabricated measurement."""
    default = _usage().as_dict()["usage_units"]["provider_tokens"]
    assert default["declared_absent"] is True
    assert "fabricated measurement" in default["reason"]

    reported = _usage(provider_tokens=1234).as_dict()["usage_units"]
    assert reported["provider_tokens"] == 1234

    with pytest.raises(tel.TelemetryRefused) as raised:
        _usage(provider_tokens="about a thousand")
    assert "there is no third answer" in str(raised.value)


# ===========================================================================
# THE BOUNDED METER
# ===========================================================================


def test_per_session_totals_sum_the_per_turn_dimensions():
    meter = tel.UsageMeter()
    scope = _scope()
    meter.record(_usage(scope=scope))
    meter.record(_usage(scope=scope, packet_bytes=1, prompt_bytes=2,
                        source_count=1, exempt_source_count=0))
    session = meter.session(scope)
    assert session.turn_count == 2
    assert session.packet_bytes == 2049
    assert session.prompt_bytes == 8194
    assert session.source_count == 5
    assert session.exempt_source_count == 1


def test_a_session_that_never_ran_has_no_row_rather_than_a_zeroed_one():
    assert tel.UsageMeter().session(_scope()) is None


def test_reported_tokens_accumulate_and_stay_absent_until_one_is_reported():
    meter = tel.UsageMeter()
    scope = _scope()
    meter.record(_usage(scope=scope))
    assert isinstance(meter.session(scope).reported_provider_tokens,
                      tel.DeclaredAbsence)
    meter.record(_usage(scope=scope, provider_tokens=10))
    meter.record(_usage(scope=scope, provider_tokens=5))
    assert meter.session(scope).reported_provider_tokens == 15


def test_the_meter_is_bounded_and_its_eviction_is_VISIBLE():
    """RE-PINNED (adversarial review, F9). This used to assert that an evicted
    scope answers `None` — the SAME answer as a scope that never ran, so five
    hundred metered turns and zero metered turns read identically. The bound
    stays (dropping the totals is what it is for); what changed is that the
    drop is now something a reader can see."""
    meter = tel.UsageMeter()
    for index in range(tel.MAX_METERED_SCOPES + 3):
        meter.record(_usage(scope=_scope(f"topic-{index:03d}")))
    assert len(meter.scopes()) == tel.MAX_METERED_SCOPES
    assert meter.eviction_count() == 3

    evicted = meter.session(_scope("topic-000"))
    assert isinstance(evicted, tel.EvictedSession)
    assert evicted.as_dict()["evicted"] is True
    assert "NOT the answer for a session that never ran" in (
        evicted.as_dict()["reason"])

    # a scope that never ran is still, distinctly, None
    assert meter.session(_scope("never-opened")) is None
    assert meter.session(_scope("topic-066")) is not None


def test_eviction_is_LEAST_RECENTLY_RECORDED_not_first_opened():
    """The busiest live conversation must not be dropped first merely because
    it was opened first: recording moves a scope to the end, exactly as the
    turn store tracks recency."""
    meter = tel.UsageMeter()
    busy = _scope("busy")
    meter.record(_usage(scope=busy))
    for index in range(tel.MAX_METERED_SCOPES - 1):
        meter.record(_usage(scope=_scope(f"other-{index:03d}")))
    meter.record(_usage(scope=busy))          # busy is now most recent
    meter.record(_usage(scope=_scope("new"))) # forces one eviction

    assert isinstance(meter.session(busy), tel.SessionUsage)
    assert meter.session(busy).turn_count == 2
    assert isinstance(meter.session(_scope("other-000")), tel.EvictedSession)


def test_a_scope_that_returns_after_eviction_stops_reading_as_evicted():
    meter = tel.UsageMeter()
    first = _scope("returning")
    meter.record(_usage(scope=first))
    for index in range(tel.MAX_METERED_SCOPES):
        meter.record(_usage(scope=_scope(f"filler-{index:03d}")))
    assert isinstance(meter.session(first), tel.EvictedSession)
    meter.record(_usage(scope=first))
    assert isinstance(meter.session(first), tel.SessionUsage)
    assert meter.session(first).turn_count == 1


def test_two_meters_share_no_state():
    one, two = tel.UsageMeter(), tel.UsageMeter()
    one.record(_usage())
    assert two.scopes() == ()


def test_the_meter_records_and_emits_nowhere_itself():
    """A meter that also wrote somewhere would be a second store, and the
    content-free argument depends on there being exactly one shape and one
    place it is built."""
    source = MODULE_PATH.read_text(encoding="utf-8")
    for needle in ("open(", "write_text", "import os", "urllib", "socket",
                   "logging", "print(", "sqlite3"):
        assert needle not in source, needle


def test_declared_absences_are_readable_as_the_auditable_half():
    absences = tel.declared_absences()
    assert set(absences) == {"client", "domain", "bill_to",
                             "customer_subject_ref"}
    for field, reason in absences.items():
        assert reason.strip(), field
