"""Tests for the doxBench model-catalog types and narrow provider port
(010-doxbench-editor-chat T013/T020; data-model.md Section 6,
contracts/model-catalog.md, research.md R6/R9, plan.md Constraints).

Unlike test_doxbench_hash.py this suite has no shared cross-language vector
file: ``WorkbenchModelPort``, ``ModelCatalog``, and their fake are Python-only,
server-side types with no browser sibling in this slice (research R6). What
IS mirrored is the sentinel discipline -- several tests below read
``scripts/ideation_dashboard/doxbench_model.py``'s own source text to prove
it never grows a network import, a credential-shaped literal, or a quoted
wire-envelope field ahead of the schedule research.md/plan.md declare (R13,
"Contract Baseline and Merge Pin").

Sections below mirror the four required-coverage groups: catalog/descriptor,
provider port, output limit, and redaction/hermeticity sentinels.
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from carved_reach import source as carved_source

from opendox.doxbench_model import (
    CATALOG_WIRE_KIND,
    CATALOG_WIRE_SCHEMA_VERSION,
    MAX_ADAPTER_TIMEOUT_SECONDS,
    SERVER_MAX_INPUT_LIMIT_BYTES,
    SERVER_MAX_OUTPUT_LIMIT_BYTES,
    PUBLIC_ENTRY_FIELDS,
    WIRE_ENVELOPE_FIELDS,
    EMPTY_CATALOG,
    AdapterTimeoutError,
    DuplicateModelIdError,
    FakeWorkbenchModelPort,
    InvalidCatalogEntryError,
    InvalidRoutingRuleError,
    MAX_CATALOG_ENTRIES,
    MAX_ROUTING_TARGETS,
    MODEL_REFERENCE_MAX_LENGTH,
    MODEL_REFERENCE_PATTERN,
    CATALOG_MODALITIES,
    CAPABILITY_ENTRY_FIELDS,
    CatalogEntryCountError,
    DATA_HANDLING_MAX_LENGTH,
    LABEL_MAX_LENGTH,
    PROVIDER_CLASS_MAX_LENGTH,
    REQUIRED_MODALITY,
    DECLARABLE_ENTRY_FIELDS,
    ROUTING_ENTRY_FIELDS,
    ModelCatalog,
    ModelCatalogEntry,
    ModelCatalogError,
    WorkbenchModelPort,
    catalog_wire_envelope,
    effective_limit_bytes,
    validated_timeout_seconds,
)
from ideation_dashboard import doxbench_contracts
from opendox import doxbench_model
from opendox import serve

# POST-SHED (§ 5.2, RULED (a), `#656` comment `5625573095`). This module is a
# `moved_verbatim` row: its file left for the openDox-code leg and this test
# STAYED (`stays_openxfactory_adapter`). The manifest row says where it went, so
# the name below is the one it has always been and the path is DERIVED.
MODULE_PATH = carved_source("scripts/ideation_dashboard/doxbench_model.py")

# The exact success example from contracts/model-catalog.md -- reused as the
# base fixture for every entry-shaped test below.
CONTRACT_EXAMPLE = {
    "model_id": "opaque-local-id",
    "label": "Approved authoring model",
    "provider_class": "on-tenant",
    "available": True,
    "input_limit_bytes": 800_000,
    "output_limit_bytes": 900_000,
    "data_handling": "Processed in the approved tenant boundary",
}


def _entry(model_id: str, **overrides) -> ModelCatalogEntry:
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs["model_id"] = model_id
    kwargs.update(overrides)
    return ModelCatalogEntry(**kwargs)


# ---------------------------------------------------------------------------
# Catalog / descriptor (T013 "catalog")
# ---------------------------------------------------------------------------


def test_valid_entry_round_trips_the_contract_example_and_public_dict_order():
    entry = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    public = entry.as_public_dict()
    assert list(public) == list(PUBLIC_ENTRY_FIELDS)
    assert public == CONTRACT_EXAMPLE


def test_entry_is_frozen_and_new_attributes_cannot_be_added():
    entry = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.model_id = "changed"
    # The assignment to an attribute the dataclass never declared must be
    # refused; what matters is that it IS refused, not the exact exception
    # type. On CPython 3.12.3 this currently raises TypeError with the
    # message "super(type, obj): obj must be an instance or subtype of
    # type" -- an artifact of how slots=True regenerates the dataclass (the
    # generated __setattr__'s fallback branch calls super(cls, self) with
    # the pre-slots cls), not a documented language guarantee or a
    # deliberate detection branch. Both TypeError and AttributeError are
    # accepted here as evidence the assignment was refused.
    with pytest.raises((TypeError, AttributeError)):
        entry.brand_new_field = "nope"


@pytest.mark.parametrize("field", ["model_id", "label", "provider_class", "data_handling"])
@pytest.mark.parametrize("blank", ["", "   ", "\t\n"])
def test_blank_or_whitespace_only_string_fields_are_refused(field, blank):
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs[field] = blank
    with pytest.raises(InvalidCatalogEntryError, match="must not be blank"):
        ModelCatalogEntry(**kwargs)


@pytest.mark.parametrize("bad_available", [1, 0, "true", None, "yes"])
def test_non_bool_available_is_refused(bad_available):
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs["available"] = bad_available
    with pytest.raises(TypeError, match="available must be a bool"):
        ModelCatalogEntry(**kwargs)


@pytest.mark.parametrize("field", ["input_limit_bytes", "output_limit_bytes"])
def test_bool_passed_as_a_limit_field_is_refused(field):
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs[field] = True
    with pytest.raises(TypeError, match=f"{field} must be a non-bool int"):
        ModelCatalogEntry(**kwargs)


def test_input_limit_boundary_equality_is_accepted():
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs["input_limit_bytes"] = SERVER_MAX_INPUT_LIMIT_BYTES
    entry = ModelCatalogEntry(**kwargs)
    assert entry.input_limit_bytes == SERVER_MAX_INPUT_LIMIT_BYTES


def test_output_limit_boundary_equality_is_accepted():
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs["output_limit_bytes"] = SERVER_MAX_OUTPUT_LIMIT_BYTES
    entry = ModelCatalogEntry(**kwargs)
    assert entry.output_limit_bytes == SERVER_MAX_OUTPUT_LIMIT_BYTES


@pytest.mark.parametrize(
    "field,cap",
    [
        ("input_limit_bytes", SERVER_MAX_INPUT_LIMIT_BYTES),
        ("output_limit_bytes", SERVER_MAX_OUTPUT_LIMIT_BYTES),
    ],
)
def test_limit_fields_refuse_zero_negative_and_over_cap(field, cap):
    for bad in (0, -1, cap + 1):
        kwargs = dict(CONTRACT_EXAMPLE)
        kwargs[field] = bad
        with pytest.raises(InvalidCatalogEntryError):
            ModelCatalogEntry(**kwargs)


def test_empty_catalog_is_the_fr025_editor_only_posture():
    assert EMPTY_CATALOG.entries == ()
    assert EMPTY_CATALOG.available_entries() == ()
    assert EMPTY_CATALOG.as_public_dict() == {"models": []}


def test_from_entries_preserves_supplied_order_and_never_sorts():
    zeta = _entry("zeta-model", label="Zeta")
    alpha = _entry("alpha-model", label="Alpha")
    middle = _entry("middle-model", label="Middle")
    catalog = ModelCatalog.from_entries([zeta, alpha, middle])
    assert catalog.entries == (zeta, alpha, middle)
    assert [e.model_id for e in catalog.entries] == [
        "zeta-model",
        "alpha-model",
        "middle-model",
    ]


def test_duplicate_model_id_raises_and_produces_no_partial_catalog():
    one = _entry("dup-id")
    two = _entry("dup-id", label="Second label")
    with pytest.raises(DuplicateModelIdError, match="duplicate model_id"):
        ModelCatalog.from_entries([one, two])


def test_one_non_entry_element_refuses_the_whole_catalog_fail_closed():
    good_one = _entry("good-1")
    good_two = _entry("good-2")
    with pytest.raises(TypeError):
        ModelCatalog.from_entries([good_one, {"model_id": "bad"}, good_two])
    # Nothing was silently dropped or partially kept: retrying without the
    # bad element succeeds and both good entries are present, proving the
    # earlier failure left no partial/cached catalog behind.
    catalog = ModelCatalog.from_entries([good_one, good_two])
    assert catalog.entries == (good_one, good_two)


@pytest.mark.parametrize("bad_element", [{"model_id": "x"}, "not-an-entry", None])
def test_non_modelcatalogentry_elements_are_refused(bad_element):
    with pytest.raises(TypeError):
        ModelCatalog.from_entries([_entry("good"), bad_element])


def test_available_entries_filters_in_order_for_mixed_availability():
    a = _entry("a", available=True)
    b = _entry("b", available=False)
    c = _entry("c", available=True)
    catalog = ModelCatalog.from_entries([a, b, c])
    assert catalog.available_entries() == (a, c)


def test_available_entries_all_unavailable_and_all_available_postures():
    a = _entry("a", available=False)
    b = _entry("b", available=False)
    unavailable_catalog = ModelCatalog.from_entries([a, b])
    assert unavailable_catalog.available_entries() == ()

    c = _entry("c", available=True)
    d = _entry("d", available=True)
    available_catalog = ModelCatalog.from_entries([c, d])
    assert available_catalog.available_entries() == (c, d)


def test_entry_for_exact_match_absent_and_no_normalization():
    entry = _entry("Model-A")
    catalog = ModelCatalog.from_entries([entry])
    assert catalog.entry_for("Model-A") is entry
    assert catalog.entry_for("model-a") is None
    assert catalog.entry_for("missing") is None


def test_selectable_entry_for_available_unavailable_and_absent():
    available = _entry("avail", available=True)
    unavailable = _entry("unavail", available=False)
    catalog = ModelCatalog.from_entries([available, unavailable])
    assert catalog.selectable_entry_for("avail") is available
    assert catalog.selectable_entry_for("unavail") is None
    assert catalog.selectable_entry_for("missing") is None


def test_catalog_is_frozen_and_entries_tuple_is_independent_of_source_list():
    entries_list = [_entry("a"), _entry("b")]
    catalog = ModelCatalog.from_entries(entries_list)
    entries_list.append(_entry("c"))
    entries_list.clear()

    assert isinstance(catalog.entries, tuple)
    assert len(catalog.entries) == 2

    with pytest.raises(dataclasses.FrozenInstanceError):
        catalog.entries = ()


def test_populated_catalog_public_dict_has_exactly_one_key():
    catalog = ModelCatalog.from_entries([_entry("a"), _entry("b")])
    public = catalog.as_public_dict()
    assert list(public) == ["models"]
    assert len(public["models"]) == 2


# ---------------------------------------------------------------------------
# WIRE projection (T020 wire clause).
#
# The additive openxFactory catalog schema is now RELEASED and PINNED
# (`xfactory-workbench-model-catalog.schema.yaml` at contract-v1.27,
# `d09d5820de5b63b9528f6baea884a6dccde9b158`), so the version field and kind
# constant data-model.md Section 6 always described are no longer deferred.
# The projection is a PURE module-level function, not a port member and not a
# deployment adapter: T049 owns dispatch, T047/5.1 the adapters. This module
# still imports nothing from `serve.py` and no schema library -- the released
# schema is the AUTHORITY for this shape, and `doxbench_contracts` is where it
# is loaded and enforced (the constants below are pinned against that module's
# own released kind literal so the two cannot drift).
# ---------------------------------------------------------------------------


def test_wire_envelope_constants_match_the_released_schema_literals():
    assert CATALOG_WIRE_SCHEMA_VERSION == 1
    assert CATALOG_WIRE_KIND == "workbench-model-catalog"
    # No second spelling of the released kind: the loader's constant IS the pin.
    assert CATALOG_WIRE_KIND == doxbench_contracts.KIND_MODEL_CATALOG
    assert WIRE_ENVELOPE_FIELDS == ("schema_version", "kind", "models")


def test_wire_envelope_is_the_released_three_key_envelope_in_order():
    catalog = ModelCatalog.from_entries([_entry("a"), _entry("b")])
    envelope = catalog_wire_envelope(catalog)
    assert list(envelope) == list(WIRE_ENVELOPE_FIELDS)
    assert envelope["schema_version"] == CATALOG_WIRE_SCHEMA_VERSION
    assert envelope["kind"] == CATALOG_WIRE_KIND
    assert [entry["model_id"] for entry in envelope["models"]] == ["a", "b"]
    for entry in envelope["models"]:
        assert list(entry) == list(PUBLIC_ENTRY_FIELDS)


def test_empty_catalog_wire_envelope_is_the_editor_only_success_posture():
    # FR-025/SC-008: an empty `models` array is a SUCCESSFUL editor-only
    # posture in the released schema, never an error.
    envelope = catalog_wire_envelope(EMPTY_CATALOG)
    assert envelope == {"schema_version": 1, "kind": "workbench-model-catalog",
                        "models": []}


def test_wire_envelope_carries_the_public_allowlist_and_nothing_else():
    catalog = ModelCatalog.from_entries([ModelCatalogEntry(**CONTRACT_EXAMPLE)])
    envelope = catalog_wire_envelope(catalog)
    assert set(envelope) == set(WIRE_ENVELOPE_FIELDS)
    assert envelope["models"] == [ModelCatalogEntry(**CONTRACT_EXAMPLE).as_public_dict()]
    assert set(envelope["models"][0]) == set(PUBLIC_ENTRY_FIELDS)


def test_wire_envelope_is_pure_repeatable_and_shares_no_mutable_state():
    catalog = ModelCatalog.from_entries([_entry("a")])
    first = catalog_wire_envelope(catalog)
    second = catalog_wire_envelope(catalog)
    assert first == second
    assert first is not second
    assert first["models"] is not second["models"]
    first["models"].append({"model_id": "injected"})
    first["kind"] = "mutated"
    # A caller mutating one projection cannot reach the catalog or the next one.
    assert catalog_wire_envelope(catalog) == second
    assert [entry.model_id for entry in catalog.entries] == ["a"]


def test_wire_envelope_refuses_anything_that_is_not_a_model_catalog():
    for bad in ({"models": []}, [], None, ModelCatalogEntry(**CONTRACT_EXAMPLE)):
        with pytest.raises(TypeError):
            catalog_wire_envelope(bad)


def test_as_public_dict_stays_key_exact_and_envelope_free_alongside_the_wire_shape():
    # The internal projection is UNCHANGED by the wire clause: exactly one
    # key, no discriminators. Callers that need the released envelope call
    # `catalog_wire_envelope`; nothing was widened in place.
    catalog = ModelCatalog.from_entries([_entry("a")])
    assert list(catalog.as_public_dict()) == ["models"]
    assert "schema_version" not in catalog.as_public_dict()
    assert "kind" not in catalog.as_public_dict()
    assert "schema_version" not in catalog.as_public_dict()["models"][0]
    assert "kind" not in catalog.as_public_dict()["models"][0]


# ``ModelCatalog``'s fail-closed invariants (unique model_id, entries-only-
# ModelCatalogEntry, entries-is-a-tuple) are enforced by __post_init__, so
# they hold for direct construction too -- not just for from_entries. The
# tests below exercise ``ModelCatalog(entries=...)`` directly.


def test_direct_construction_with_a_list_coerces_to_tuple_and_preserves_order():
    zeta = _entry("zeta-model", label="Zeta")
    alpha = _entry("alpha-model", label="Alpha")
    catalog = ModelCatalog(entries=[zeta, alpha])
    assert isinstance(catalog.entries, tuple)
    assert catalog.entries == (zeta, alpha)


def test_direct_construction_with_a_duplicate_model_id_raises():
    one = _entry("dup-id")
    two = _entry("dup-id", label="Second label")
    with pytest.raises(DuplicateModelIdError, match="duplicate model_id"):
        ModelCatalog(entries=[one, two])


def test_direct_construction_with_a_non_modelcatalogentry_element_raises_type_error():
    with pytest.raises(TypeError):
        ModelCatalog(entries=[_entry("good"), "not-an-entry"])


def test_direct_construction_tuple_is_independent_of_the_mutated_source_list():
    source = [_entry("a"), _entry("b")]
    catalog = ModelCatalog(entries=source)
    source.append(_entry("c"))
    source.clear()

    assert isinstance(catalog.entries, tuple)
    assert len(catalog.entries) == 2
    assert [e.model_id for e in catalog.entries] == ["a", "b"]


def test_direct_construction_with_empty_tuple_and_empty_catalog_remain_valid():
    assert ModelCatalog(entries=()).entries == ()
    assert EMPTY_CATALOG.entries == ()


def test_direct_construction_entries_attribute_is_always_a_tuple():
    catalog = ModelCatalog(entries=[_entry("a")])
    assert isinstance(catalog.entries, tuple)


def test_generator_input_is_materialized_exactly_once_not_emptied_by_post_init():
    # Why this test exists: __post_init__ must coerce self.entries to a
    # tuple BEFORE it iterates for the duplicate/type checks. A generator is
    # single-use, so a rewrite that iterated first and materialized second
    # would silently consume the generator during validation and leave an
    # EMPTY tuple behind -- no exception, just a catalog that quietly lost
    # every entry. Asserting non-empty exact contents (not merely "no
    # exception") is what makes that regression fail loudly here.
    one = _entry("one")
    two = _entry("two")

    def gen():
        yield one
        yield two

    from_entries_catalog = ModelCatalog.from_entries(gen())
    assert isinstance(from_entries_catalog.entries, tuple)
    assert from_entries_catalog.entries == (one, two)
    assert len(from_entries_catalog.entries) == 2

    direct_catalog = ModelCatalog(entries=gen())
    assert isinstance(direct_catalog.entries, tuple)
    assert direct_catalog.entries == (one, two)
    assert len(direct_catalog.entries) == 2


def test_identity_aliased_duplicate_entry_is_still_a_duplicate():
    # The same object twice, not two equal-but-distinct objects: proves the
    # duplicate check keys on model_id, not object identity.
    entry = _entry("dup-id")
    with pytest.raises(DuplicateModelIdError, match="duplicate model_id"):
        ModelCatalog.from_entries([entry, entry])
    with pytest.raises(DuplicateModelIdError, match="duplicate model_id"):
        ModelCatalog(entries=[entry, entry])


def test_tuple_and_list_construction_are_equal_and_the_catalog_is_hashable():
    a = _entry("a")
    tuple_catalog = ModelCatalog(entries=(a,))
    list_catalog = ModelCatalog(entries=[a])
    assert tuple_catalog == list_catalog
    assert hash(tuple_catalog) == hash(list_catalog)
    assert {tuple_catalog, list_catalog} == {tuple_catalog}


# ---------------------------------------------------------------------------
# Provider port (T013 "provider-port")
# ---------------------------------------------------------------------------


def test_fake_port_satisfies_the_protocol_and_missing_members_do_not():
    fake = FakeWorkbenchModelPort()
    assert isinstance(fake, WorkbenchModelPort)

    class MissingCatalog:
        timeout_seconds = 10.0

    class MissingTimeout:
        def catalog(self):
            return EMPTY_CATALOG

    class MissingDispatch:
        timeout_seconds = 10.0

        def catalog(self):
            return EMPTY_CATALOG

    assert not isinstance(MissingCatalog(), WorkbenchModelPort)
    assert not isinstance(MissingTimeout(), WorkbenchModelPort)
    # PIN EVOLUTION (T049): a catalog-only adapter no longer satisfies the
    # protocol, because the protocol now DECLARES dispatch. That is not a
    # deployment claim: `serve.py` reaches the dispatch arm through a
    # `callable(getattr(port, "dispatch", None))` probe, never through
    # `isinstance`, so a catalog-only adapter keeps working and keeps the
    # refused-by-absence posture. This assertion pins the DECLARED surface.
    assert not isinstance(MissingDispatch(), WorkbenchModelPort)


# PIN EVOLUTION (T049). `dispatch` LEFT this set and joined the declared member
# set below. Every other spelling STAYS banned, and the ban is what makes the
# widening narrow: the port gained exactly ONE named capability (hand an opaque
# prompt envelope to an adapter and get its answer back), not a family of
# provider verbs. `generate`/`complete`/`chat`/`send` would be second spellings
# of the same capability; `assemble_prompt`/`prompt` would move prompt assembly
# (doxbench_turns.py) behind the seam; `validate`/`validate_response` would move
# response validation out of `dispatch_turn`, which is exactly where T049 puts
# it; `credentials`/`api_key`/`endpoint`/`client` would make the port a carrier
# for the material FR-020/FR-022 forbid.
FORBIDDEN_PORT_MEMBERS = {
    "generate",
    "complete",
    "chat",
    "send",
    "assemble_prompt",
    "prompt",
    "validate",
    "validate_response",
    "render",
    "save",
    "ensemble",
    "review",
    "credentials",
    "api_key",
    "endpoint",
    "client",
}


def test_the_protocol_declares_exactly_three_members_naming_dispatch_once():
    """PIN EVOLUTION (T049, sanctioned by research R6's own rationale). This
    test previously asserted the member set was EXACTLY
    `{timeout_seconds, catalog}` and that `dispatch` was absent -- the correct
    pin while the chat-turn contract was unreleased and no turn could be
    dispatched at all. The contract IS released and pinned (contract-v1.27,
    `d09d5820de5b63b9528f6baea884a6dccde9b158`) and T049 owns provider failure
    mapping, timeout enforcement, and response bounds, so the seam that carries
    a turn to an adapter has to exist somewhere. R6's argument was for a seam
    with ONE named capability per genuine need, not for two members forever.

    What the pin protects now is unchanged in kind: the member set is still an
    EQUALITY assertion, the widening is exactly ONE individually-named member,
    and every other provider-verb spelling stays banned above."""
    declared = WorkbenchModelPort.__protocol_attrs__
    # __protocol_attrs__ is an undocumented CPython `typing` internal --
    # pinned here deliberately (research R6) because no documented API
    # exposes a Protocol's declared member set. If a future Python version
    # renames or removes it, this assertion fails visibly rather than
    # silently losing the narrowness guarantee it exists to enforce.
    assert declared == {"timeout_seconds", "catalog", "dispatch"}
    assert not (declared & FORBIDDEN_PORT_MEMBERS)


def test_fake_catalog_calls_are_deterministic_and_recorded_in_order():
    catalog = ModelCatalog.from_entries([_entry("a")])
    fake = FakeWorkbenchModelPort(catalog)
    first = fake.catalog()
    second = fake.catalog()
    assert first is second
    assert first.as_public_dict() == second.as_public_dict()
    assert fake.calls == ["catalog", "catalog"]


def test_seeded_catalog_error_raises_deterministically_and_is_recorded():
    boom = ModelCatalogError("catalog assembly failed")
    fake = FakeWorkbenchModelPort(catalog_error=boom)
    with pytest.raises(ModelCatalogError):
        fake.catalog()
    with pytest.raises(ModelCatalogError):
        fake.catalog()
    assert fake.calls == ["catalog", "catalog"]


def test_default_constructed_fake_yields_the_empty_catalog_posture():
    fake = FakeWorkbenchModelPort()
    assert fake.catalog() is EMPTY_CATALOG


def test_validated_timeout_seconds_accepts_normal_value_and_the_boundary():
    assert validated_timeout_seconds(30) == 30.0
    assert validated_timeout_seconds(120) == 120.0


@pytest.mark.parametrize("bad", [0, -1, 121, float("nan"), True, None, "30"])
def test_validated_timeout_seconds_refuses_out_of_range_and_non_numeric(bad):
    with pytest.raises(AdapterTimeoutError, match="declared timeout"):
        validated_timeout_seconds(bad)


def test_fake_port_refuses_an_out_of_range_declared_timeout_at_construction():
    with pytest.raises(AdapterTimeoutError, match="declared timeout"):
        FakeWorkbenchModelPort(timeout_seconds=121)


def test_fake_port_refuses_a_non_modelcatalog_catalog_argument_at_construction():
    with pytest.raises(TypeError, match="catalog must be a ModelCatalog"):
        FakeWorkbenchModelPort(catalog="not-a-catalog")


def test_fake_port_accepts_a_valid_catalog_and_the_default_empty_catalog():
    catalog = ModelCatalog.from_entries([_entry("a")])
    fake = FakeWorkbenchModelPort(catalog)
    assert fake.catalog() is catalog

    default_fake = FakeWorkbenchModelPort()
    assert default_fake.catalog() is EMPTY_CATALOG


def test_fake_repr_exposes_only_entry_count_and_timeout():
    entry = ModelCatalogEntry(
        model_id="private-model-id",
        label="Private Label",
        provider_class="private-provider-class",
        available=True,
        input_limit_bytes=800_000,
        output_limit_bytes=900_000,
        data_handling="private-data-handling-badge",
    )
    catalog = ModelCatalog.from_entries([entry])
    fake = FakeWorkbenchModelPort(catalog, timeout_seconds=45.0)
    text = repr(fake)
    assert text == "FakeWorkbenchModelPort(entries=1, timeout_seconds=45.0)"
    for leaked in (
        "private-model-id",
        "Private Label",
        "private-data-handling-badge",
        "private-provider-class",
    ):
        assert leaked not in text


# ---------------------------------------------------------------------------
# Output limit (T013 "output-limit")
# ---------------------------------------------------------------------------


def test_effective_limit_bytes_returns_the_stricter_value_for_input_and_output():
    # input constant: entry equal, entry stricter, server stricter
    assert (
        effective_limit_bytes(
            server_maximum=SERVER_MAX_INPUT_LIMIT_BYTES,
            entry_limit=SERVER_MAX_INPUT_LIMIT_BYTES,
        )
        == SERVER_MAX_INPUT_LIMIT_BYTES
    )
    assert (
        effective_limit_bytes(server_maximum=SERVER_MAX_INPUT_LIMIT_BYTES, entry_limit=800_000)
        == 800_000
    )
    assert (
        effective_limit_bytes(server_maximum=500_000, entry_limit=SERVER_MAX_INPUT_LIMIT_BYTES)
        == 500_000
    )

    # output constant: entry equal, entry stricter, server stricter
    assert (
        effective_limit_bytes(
            server_maximum=SERVER_MAX_OUTPUT_LIMIT_BYTES,
            entry_limit=SERVER_MAX_OUTPUT_LIMIT_BYTES,
        )
        == SERVER_MAX_OUTPUT_LIMIT_BYTES
    )
    assert (
        effective_limit_bytes(server_maximum=SERVER_MAX_OUTPUT_LIMIT_BYTES, entry_limit=400_000)
        == 400_000
    )
    assert (
        effective_limit_bytes(server_maximum=300_000, entry_limit=SERVER_MAX_OUTPUT_LIMIT_BYTES)
        == 300_000
    )


@pytest.mark.parametrize("bad", [0, -1, True, False, 1.5, "100", None])
def test_effective_limit_bytes_refuses_non_positive_and_non_int_arguments(bad):
    with pytest.raises(ValueError):
        effective_limit_bytes(server_maximum=bad, entry_limit=100)
    with pytest.raises(ValueError):
        effective_limit_bytes(server_maximum=100, entry_limit=bad)


def test_server_max_input_limit_matches_serves_request_cap_no_drift():
    # DRIFT PIN (read-only against serve.py -- serve.py is not modified by
    # this task). Both constants encode plan.md's route-specific request
    # maximum; this assertion is what stops them from silently diverging.
    assert doxbench_model.SERVER_MAX_INPUT_LIMIT_BYTES == serve.DOXBENCH_MAX_REQUEST_BYTES
    assert SERVER_MAX_INPUT_LIMIT_BYTES == 1_048_576


def test_server_max_output_limit_and_adapter_timeout_constants_match_plan_md():
    # plan.md Constraints: "total validated response content is at most
    # 900,000 bytes."
    assert SERVER_MAX_OUTPUT_LIMIT_BYTES == 900_000
    # plan.md Constraints: "Provider calls have an adapter-declared timeout
    # no greater than 120 seconds."
    assert MAX_ADAPTER_TIMEOUT_SECONDS == 120


# ---------------------------------------------------------------------------
# Redaction / hermeticity sentinels (T013 "redaction", FR-021/FR-022,
# CHK001/CHK010)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("extra_kwarg", ["api_key", "endpoint", "deployment"])
def test_extra_keyword_argument_is_refused_the_seven_field_surface_is_closed(extra_kwarg):
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs[extra_kwarg] = "nope"
    with pytest.raises(TypeError):
        ModelCatalogEntry(**kwargs)


FORBIDDEN_VALUE_SUBSTRINGS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "credential",
    "password",
    "bearer",
    "endpoint",
    "http://",
    "https://",
    "deployment",
    "azure",
    "openai",
    "anthropic",
    "env",
    "template",
)


def test_public_dicts_contain_no_forbidden_substrings():
    entry = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    catalog = ModelCatalog.from_entries([entry])
    # The released WIRE envelope is scanned alongside the two internal
    # projections: the credential/endpoint/env-var needles are unaffected by
    # the contract release and must stay absent from every public shape this
    # module can produce (FR-020/FR-022).
    blob = (json.dumps(entry.as_public_dict())
            + json.dumps(catalog.as_public_dict())
            + json.dumps(catalog_wire_envelope(catalog))).lower()
    for forbidden in FORBIDDEN_VALUE_SUBSTRINGS:
        assert forbidden not in blob, forbidden


FORBIDDEN_SOURCE_SNIPPETS = (
    "import requests",
    "import httpx",
    "import socket",
    "import openai",
    "import anthropic",
    "boto3",
    "urllib",
    "subprocess",
    "os.environ",
    "os.getenv",
    "getenv(",
    "http://",
    "https://",
    "api_key",
    "apikey",
    "secret",
    "bearer",
    "jsonschema",
    "from ideation_dashboard.serve",
    "import serve",
)


def test_module_source_contains_no_network_or_provider_or_schema_markers():
    src = MODULE_PATH.read_text(encoding="utf-8")
    lowered = src.lower()
    for forbidden in FORBIDDEN_SOURCE_SNIPPETS:
        assert forbidden.lower() not in lowered, forbidden


def test_wire_envelope_literals_are_confined_to_the_released_catalog_projection():
    """PIN EVOLUTION (T020 wire clause). This test previously asserted that
    `"schema_version"`/`"kind"` appeared NOWHERE in the module source -- the
    correct pin while the additive openxFactory catalog schema was unreleased
    (its own docstring said "ahead of the schedule research.md/plan.md
    declare (R13)"). The schema IS now released and pinned (contract-v1.27,
    `d09d5820de5b63b9528f6baea884a6dccde9b158`), so the literals are exactly
    as legitimate here as they were forbidden before. What the pin protects
    now is CONFINEMENT: the two discriminators may appear only as the wire
    projection's own constants, they never leak into the ENTRY
    surface, and they never appear in the internal `as_public_dict`
    projections that predate the release."""
    src = MODULE_PATH.read_text(encoding="utf-8")
    for quoted in ("'schema_version'", "'kind'"):
        assert quoted not in src, quoted
    # Every source line mentioning either discriminator, exactly: the released
    # envelope's ordered field tuple, and the projection that emits it. Nowhere
    # else -- not on an entry, not on a port, not on the fake adapter.
    bearing = [line.strip() for line in src.splitlines()
               if '"schema_version"' in line or '"kind"' in line]
    assert bearing == [
        'WIRE_ENVELOPE_FIELDS: tuple[str, ...] = ("schema_version", "kind", "models")',
        '"schema_version": CATALOG_WIRE_SCHEMA_VERSION,',
        '"kind": CATALOG_WIRE_KIND,',
    ]

    entry = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    catalog = ModelCatalog.from_entries([entry])
    assert "schema_version" not in entry.as_public_dict()
    assert "kind" not in entry.as_public_dict()
    assert "schema_version" not in catalog.as_public_dict()
    assert "kind" not in catalog.as_public_dict()
    # And in the envelope they are the ONLY additions: a plain entry stays
    # exactly the seven required base fields (contract-v1.38's three routing
    # fields are disclosed only by an entry that declares itself a rule, and
    # contract-v2.2's `modalities` only by an entry that declares one).
    envelope = catalog_wire_envelope(catalog)
    assert set(envelope) - {"models"} == {"schema_version", "kind"}
    assert set(envelope["models"][0]) == set(PUBLIC_ENTRY_FIELDS)


def test_module_namespace_holds_no_bound_network_module():
    # Simplest acceptable form (per task spec): the source sentinel above
    # plus this direct namespace check, so a network module bound as a
    # module-level name (rather than a plain string match) is also caught.
    forbidden_names = ("requests", "httpx", "socket", "urllib", "subprocess", "os", "http")
    for name in forbidden_names:
        assert name not in vars(doxbench_model), name


# ---------------------------------------------------------------------------
# T046/T049: dispatch_turn -- provider failure mapping, timeout enforcement,
# response bounds, redacted diagnostics (research R6/R9/R14, plan.md
# Constraints, FR-020/FR-022). Every case below runs against the FAKE port
# only: no real adapter exists in this repository, and `dispatch_turn` takes
# an INJECTED monotonic `clock` callable precisely so timeout enforcement
# needs no real sleeping and no `time` import inside doxbench_model.py.
# New names are reached as `doxbench_model.<name>` attributes so this section
# could be authored red without breaking collection of the sections above.
# ---------------------------------------------------------------------------


def _list_clock(*readings: float):
    """A deterministic clock: yields `readings` in order, then repeats the
    final value forever. Also records how many times it was read, so a test
    can pin dispatch_turn's exact clock discipline."""
    state = {"reads": 0}
    values = list(readings)

    def clock() -> float:
        index = min(state["reads"], len(values) - 1)
        state["reads"] += 1
        return values[index]

    clock.reads = lambda: state["reads"]  # type: ignore[attr-defined]
    return clock


def _prose_payload(prose: str = "grounded answer") -> dict:
    return {"assistant_prose": prose, "proposals": []}


def _dispatch(fake, *, entry=None, payload_prose="grounded answer",
              clock=None, envelope="opaque-envelope"):
    """One dispatch_turn call with this section's defaults."""
    if entry is None:
        entry = _entry("m-live")
    if clock is None:
        clock = _list_clock(0.0, 1.0)
    return doxbench_model.dispatch_turn(
        fake, envelope, entry=entry, clock=clock)


def test_dispatch_turn_prose_only_success_round_trips_and_delegates_once():
    fake = FakeWorkbenchModelPort(
        ModelCatalog.from_entries([_entry("m-live")]),
        dispatch_result=_prose_payload("grounded answer"))
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchSuccess)
    assert outcome.assistant_prose == "grounded answer"
    assert outcome.proposals == ()
    # Delegation-only semantics: exactly ONE dispatch call, nothing else.
    assert fake.calls == ["dispatch"]


def test_dispatch_receives_the_prompt_envelope_opaquely_and_unmodified():
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload())
    marker = object()
    _dispatch(fake, envelope=marker)
    assert fake.dispatched == [marker]


def test_an_unavailable_entry_refuses_model_unavailable_before_any_dispatch():
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload())
    outcome = _dispatch(fake, entry=_entry("m-off", available=False))
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_MODEL_UNAVAILABLE
    assert fake.calls == []


def test_model_unavailable_spelling_matches_the_route_catalog_no_drift():
    assert (doxbench_model.DISPATCH_ERR_MODEL_UNAVAILABLE
            == serve.DOXBENCH_ERR_MODEL_UNAVAILABLE)


def test_a_turn_exceeding_the_declared_timeout_maps_to_model_timeout():
    fake = FakeWorkbenchModelPort(
        dispatch_result=_prose_payload("late but valid"),
        timeout_seconds=30.0)
    outcome = _dispatch(fake, clock=_list_clock(100.0, 130.5))
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_MODEL_TIMEOUT
    # The late result is DISCARDED unread: a failure carries no payload and
    # no prose-shaped attribute at all.
    assert not hasattr(outcome, "assistant_prose")
    assert not hasattr(outcome, "payload")


def test_a_turn_finishing_exactly_at_the_deadline_is_not_a_timeout():
    fake = FakeWorkbenchModelPort(
        dispatch_result=_prose_payload(), timeout_seconds=30.0)
    outcome = _dispatch(fake, clock=_list_clock(0.0, 30.0))
    assert isinstance(outcome, doxbench_model.TurnDispatchSuccess)


def test_the_deadline_outcome_dominates_a_late_provider_error():
    fake = FakeWorkbenchModelPort(
        dispatch_error=RuntimeError("late provider explosion"),
        timeout_seconds=30.0)
    outcome = _dispatch(fake, clock=_list_clock(0.0, 31.0))
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_MODEL_TIMEOUT


def test_a_provider_exception_maps_to_model_failed_with_a_fixed_diagnostic():
    fake = FakeWorkbenchModelPort(
        dispatch_error=RuntimeError("secret-key-material-9x7 leaked detail"))
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_MODEL_FAILED
    assert fake.calls == ["dispatch"]


def test_provider_exception_text_never_reaches_the_failure_surface():
    """FR-020/FR-022 redaction: the diagnostic is one of the module's FIXED
    strings, and the exception's own text is absent from every attribute and
    from repr -- there is no field a caller could log that carries it."""
    fake = FakeWorkbenchModelPort(
        dispatch_error=RuntimeError("secret-key-material-9x7 leaked detail"))
    outcome = _dispatch(fake)
    assert outcome.diagnostic in doxbench_model.FIXED_DISPATCH_DIAGNOSTICS
    surface = repr(outcome) + json.dumps(dataclasses.asdict(outcome))
    assert "secret-key-material-9x7" not in surface
    assert "leaked detail" not in surface


@pytest.mark.parametrize("raw", [
    None,
    "just a string",
    42,
    [],
    {},
    {"assistant_prose": "x"},
    {"proposals": []},
    {"assistant_prose": 5, "proposals": []},
    {"assistant_prose": "x", "proposals": "nope"},
    {"assistant_prose": "x", "proposals": [], "extra": 1},
])
def test_malformed_provider_output_maps_to_response_invalid(raw):
    fake = FakeWorkbenchModelPort(dispatch_result=raw)
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID
    assert outcome.diagnostic in doxbench_model.FIXED_DISPATCH_DIAGNOSTICS


def test_non_empty_proposals_are_refused_without_an_injected_validator():
    """PIN EVOLUTION (T061, exactly the widening the original docstring
    promised): typed-proposal validation now EXISTS
    (doxbench_turns.validate_assistant_response), and dispatch_turn reaches
    it only through an INJECTED `proposal_validator` (doxbench_turns imports
    this module, so the dependency cannot point back). The fail-closed rule
    is UNCHANGED in kind: with no validator injected — today's posture for
    any caller that has not opted in — a proposal-bearing response is still
    refused, never passed through unvalidated."""
    payload = {"assistant_prose": "x",
               "proposals": [{"target": "outline", "content": "# New"}]}
    fake = FakeWorkbenchModelPort(dispatch_result=payload)
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID


def test_an_injected_validator_passes_validated_proposals_through():
    proposal = {"target": "outline", "base_hash": "a" * 64,
                "summary": "Tighten the outline", "content": "# New"}
    payload = {"assistant_prose": "x", "proposals": [proposal]}
    fake = FakeWorkbenchModelPort(dispatch_result=payload)
    seen = []

    class _Validated:
        assistant_prose = "x"
        proposals = (proposal,)

    def validator(raw):
        seen.append(raw)
        return _Validated()

    outcome = doxbench_model.dispatch_turn(
        fake, "opaque", entry=_entry("m"), clock=_list_clock(0.0, 1.0),
        proposal_validator=validator)
    assert isinstance(outcome, doxbench_model.TurnDispatchSuccess)
    assert outcome.proposals == (proposal,)
    assert seen == [payload]


def test_a_refusing_validator_maps_to_response_invalid_redacted():
    def validator(raw):
        raise ValueError("secret-refusal-detail-77z")

    fake = FakeWorkbenchModelPort(dispatch_result={
        "assistant_prose": "x",
        "proposals": [{"target": "outline", "base_hash": "a" * 64,
                       "summary": "s", "content": "c"}]})
    outcome = doxbench_model.dispatch_turn(
        fake, "opaque", entry=_entry("m"), clock=_list_clock(0.0, 1.0),
        proposal_validator=validator)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID
    assert outcome.diagnostic in doxbench_model.FIXED_DISPATCH_DIAGNOSTICS
    assert "secret-refusal-detail-77z" not in repr(outcome)


def test_a_prose_only_response_never_consults_the_validator():
    calls = []
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload("ok"))
    outcome = doxbench_model.dispatch_turn(
        fake, "opaque", entry=_entry("m"), clock=_list_clock(0.0, 1.0),
        proposal_validator=lambda raw: calls.append(raw))
    assert isinstance(outcome, doxbench_model.TurnDispatchSuccess)
    assert outcome.proposals == ()
    assert calls == []


def test_prose_over_the_fixed_cap_maps_to_response_invalid():
    fake = FakeWorkbenchModelPort(
        dispatch_result=_prose_payload("a" * 65_537))
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID


def test_prose_at_the_exact_fixed_cap_is_accepted():
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload("a" * 65_536))
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchSuccess)


def test_prose_bounds_measure_utf8_bytes_never_code_points():
    # 21_846 three-byte characters is 65_538 bytes but only 21_846 code
    # points: a code-point measurer would accept it, the byte rule refuses.
    fake = FakeWorkbenchModelPort(
        dispatch_result=_prose_payload("€" * 21_846))
    outcome = _dispatch(fake)
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID


def test_the_entry_output_limit_is_the_stricter_response_bound():
    entry = _entry("m-small", output_limit_bytes=1_000)
    over = FakeWorkbenchModelPort(dispatch_result=_prose_payload("a" * 1_001))
    at = FakeWorkbenchModelPort(dispatch_result=_prose_payload("a" * 1_000))
    refused = _dispatch(over, entry=entry)
    accepted = _dispatch(at, entry=entry)
    assert isinstance(refused, doxbench_model.TurnDispatchFailure)
    assert refused.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID
    assert isinstance(accepted, doxbench_model.TurnDispatchSuccess)


def test_a_misdeclared_adapter_timeout_fails_closed_without_dispatch():
    class MisdeclaredPort:
        timeout_seconds = 200  # over MAX_ADAPTER_TIMEOUT_SECONDS

        def catalog(self):
            return EMPTY_CATALOG

        def dispatch(self, prompt_envelope):
            raise AssertionError("a misdeclared adapter must never dispatch")

    outcome = doxbench_model.dispatch_turn(
        MisdeclaredPort(), "opaque", entry=_entry("m"),
        clock=_list_clock(0.0, 1.0))
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_MODEL_FAILED
    assert outcome.diagnostic in doxbench_model.FIXED_DISPATCH_DIAGNOSTICS


def test_a_non_entry_argument_is_a_type_error_not_a_wire_failure():
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload())
    with pytest.raises(TypeError, match="entry must be a ModelCatalogEntry"):
        doxbench_model.dispatch_turn(
            fake, "opaque", entry={"model_id": "m"},
            clock=_list_clock(0.0, 1.0))


def test_dispatch_turn_reads_the_clock_exactly_twice():
    clock = _list_clock(0.0, 1.0)
    fake = FakeWorkbenchModelPort(dispatch_result=_prose_payload())
    doxbench_model.dispatch_turn(fake, "opaque", entry=_entry("m"), clock=clock)
    assert clock.reads() == 2


def test_dispatch_failure_codes_are_fixed_closed_and_pattern_conformant():
    """The released failure envelope types `error` as
    `^[a-z][a-z0-9_]{2,63}$` (contract-v1.27). The module's dispatch codes
    are a CLOSED four-value surface; anything new must be added here loudly."""
    codes = doxbench_model.DISPATCH_FAILURE_CODES
    assert codes == (
        doxbench_model.DISPATCH_ERR_MODEL_UNAVAILABLE,
        doxbench_model.DISPATCH_ERR_MODEL_TIMEOUT,
        doxbench_model.DISPATCH_ERR_MODEL_FAILED,
        doxbench_model.DISPATCH_ERR_RESPONSE_INVALID,
    )
    for code in codes:
        assert 3 <= len(code) <= 64
        assert code[0].isalpha() and code[0].islower()
        assert all(c.isdigit() or c == "_" or (c.isalpha() and c.islower())
                   for c in code)


def test_dispatch_outcome_shapes_are_frozen_slotted_and_closed():
    success = doxbench_model.TurnDispatchSuccess(
        assistant_prose="x", proposals=())
    failure = doxbench_model.TurnDispatchFailure(
        error=doxbench_model.DISPATCH_ERR_MODEL_FAILED,
        diagnostic=next(iter(doxbench_model.FIXED_DISPATCH_DIAGNOSTICS)))
    for shape in (success, failure):
        with pytest.raises((AttributeError, TypeError)):
            shape.grown = "no"  # type: ignore[attr-defined]
    with pytest.raises(dataclasses.FrozenInstanceError):
        success.assistant_prose = "mutated"  # type: ignore[misc]


def test_fixed_diagnostics_are_a_closed_set_of_plain_fixed_strings():
    diagnostics = doxbench_model.FIXED_DISPATCH_DIAGNOSTICS
    assert isinstance(diagnostics, frozenset)
    assert diagnostics  # non-empty
    for text in diagnostics:
        assert isinstance(text, str)
        # Fixed prose only: no formatting slots a later edit could feed
        # request or provider data through.
        assert "{" not in text and "}" not in text and "%" not in text


def test_assistant_prose_cap_matches_doxbench_turns_no_drift():
    from opendox import doxbench_turns
    assert (doxbench_model.MAX_ASSISTANT_PROSE_BYTES
            == doxbench_turns.MAX_ASSISTANT_PROSE_BYTES == 65_536)


def test_fake_dispatch_error_is_recorded_and_deterministic():
    boom = RuntimeError("deterministic failure")
    fake = FakeWorkbenchModelPort(dispatch_error=boom)
    with pytest.raises(RuntimeError):
        fake.dispatch("opaque-1")
    with pytest.raises(RuntimeError):
        fake.dispatch("opaque-2")
    assert fake.calls == ["dispatch", "dispatch"]
    assert fake.dispatched == ["opaque-1", "opaque-2"]


# ---------------------------------------------------------------------------
# PR #63 review response (Codex P2, doxbench_model.py:565): the model entry's
# output limit bounds the WHOLE validated response — prose plus proposal
# content — not prose alone.
# ---------------------------------------------------------------------------


def test_the_entry_output_limit_bounds_prose_plus_proposal_content():
    entry = _entry("m-narrow", output_limit_bytes=1_000)
    proposal = {"target": "outline", "base_hash": "a" * 64,
                "summary": "s", "content": "c" * 900}

    class _Validated:
        assistant_prose = "p" * 200
        proposals = (proposal,)

    fake = FakeWorkbenchModelPort(dispatch_result={
        "assistant_prose": "p" * 200, "proposals": [proposal]})
    outcome = doxbench_model.dispatch_turn(
        fake, "opaque", entry=entry, clock=_list_clock(0.0, 1.0),
        proposal_validator=lambda raw: _Validated())
    # 200 + 900 = 1,100 > the entry's 1,000-byte output limit.
    assert isinstance(outcome, doxbench_model.TurnDispatchFailure)
    assert outcome.error == doxbench_model.DISPATCH_ERR_RESPONSE_INVALID

    within = {"target": "outline", "base_hash": "a" * 64,
              "summary": "s", "content": "c" * 700}

    class _ValidatedWithin:
        assistant_prose = "p" * 200
        proposals = (within,)

    fake2 = FakeWorkbenchModelPort(dispatch_result={
        "assistant_prose": "p" * 200, "proposals": [within]})
    ok = doxbench_model.dispatch_turn(
        fake2, "opaque", entry=entry, clock=_list_clock(0.0, 1.0),
        proposal_validator=lambda raw: _ValidatedWithin())
    assert isinstance(ok, doxbench_model.TurnDispatchSuccess)


# ===========================================================================
# THE ROUTING-RULE DECLARATION (contract-v1.38, add-doxbench-editing-phase-b
# task 11.7)
#
# The release makes an `auto` entry constructible: three OPTIONAL fields that
# travel together, defaulting to the plain-model posture. Every rule asserted
# here mirrors one the released schema or its delegated validator enforces on
# the wire -- the two are pinned to each other by the packaged
# `workbench-model-catalog-routing-rule.example.yaml`, which this suite's
# sibling (`test_doxbench_contracts.py`) validates against the real bytes.
# ===========================================================================


def _rule(model_id="auto", *, routes_to=("a", "b"), resolved="a",
          badge=None, **overrides):
    """A routing entry over `_entry("a")`/`_entry("b")`-shaped targets, whose
    badge carries the target badge by default so the covering rule holds."""
    kwargs = dict(CONTRACT_EXAMPLE)
    kwargs.update(
        model_id=model_id,
        provider_class="routing-rule",
        data_handling=badge if badge is not None else (
            "Routes by role. / " + CONTRACT_EXAMPLE["data_handling"]),
        routing_rule=True,
        routes_to=tuple(routes_to),
        resolved_model_id=resolved,
    )
    kwargs.update(overrides)
    return ModelCatalogEntry(**kwargs)


def test_the_routing_fields_are_declared_optional_and_default_to_a_plain_model():
    """THE ADDITIVE PROPERTY, at the type. A construction that names none of
    the three -- i.e. every construction written before this release -- means
    exactly what it always meant, and the public dict it projects is
    byte-identical to the pre-release one."""
    plain = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    assert plain.routing_rule is False
    assert plain.routes_to == ()
    assert plain.resolved_model_id is None
    assert plain.as_public_dict() == CONTRACT_EXAMPLE
    assert list(plain.as_public_dict()) == list(PUBLIC_ENTRY_FIELDS)


def test_the_field_tuples_are_the_base_seven_then_the_optional_groups():
    assert ROUTING_ENTRY_FIELDS == (
        "routing_rule", "routes_to", "resolved_model_id")
    assert CAPABILITY_ENTRY_FIELDS == ("modalities",)
    assert DECLARABLE_ENTRY_FIELDS == (
        PUBLIC_ENTRY_FIELDS + CAPABILITY_ENTRY_FIELDS + ROUTING_ENTRY_FIELDS)
    # The base seven are a PREFIX of the declarable set — the property callers
    # rely on. The capability group was INSERTED before the routing three
    # rather than appended after them, so the routing keys moved within this
    # tuple; nothing indexes it, and a plain entry's projection is unchanged.
    assert DECLARABLE_ENTRY_FIELDS[:len(PUBLIC_ENTRY_FIELDS)] == PUBLIC_ENTRY_FIELDS
    # No key appears twice, so the projection order is a total order.
    assert len(set(DECLARABLE_ENTRY_FIELDS)) == len(DECLARABLE_ENTRY_FIELDS)


def test_a_routing_entry_discloses_the_three_fields_after_the_base_seven():
    rule = _rule()
    public = rule.as_public_dict()
    # A rule that declares no modalities projects the base seven then the
    # routing three, and skips the capability group entirely — each optional
    # group is present ONLY when declared, which is why this is not simply
    # `DECLARABLE_ENTRY_FIELDS` (the entry declaring BOTH groups has its own
    # test, and that one is).
    assert list(public) == list(PUBLIC_ENTRY_FIELDS) + list(ROUTING_ENTRY_FIELDS)
    assert "modalities" not in public
    assert public["routing_rule"] is True
    assert public["routes_to"] == ["a", "b"]
    assert public["resolved_model_id"] == "a"
    # `routes_to` projects as a LIST (JSON has no tuple) and shares no state
    # with the frozen entry.
    public["routes_to"].append("smuggled")
    assert rule.routes_to == ("a", "b")


def test_the_wire_envelope_carries_a_routing_entry_and_leaves_plain_ones_alone():
    catalog = ModelCatalog.from_entries(
        [_rule(routes_to=("a",), resolved="a"), _entry("a")])
    envelope = catalog_wire_envelope(catalog)
    assert list(envelope) == list(WIRE_ENVELOPE_FIELDS)
    assert set(envelope["models"][0]) == set(PUBLIC_ENTRY_FIELDS) | set(
        ROUTING_ENTRY_FIELDS)
    assert set(envelope["models"][1]) == set(PUBLIC_ENTRY_FIELDS)


@pytest.mark.parametrize("overrides, match", [
    ({"routes_to": ()}, "must declare the models it may route to"),
    ({"resolved_model_id": None}, "must declare the model it currently resolves"),
    ({"routes_to": ("auto", "a"), "resolved": "a"}, "must not route to itself"),
    ({"resolved": "c"}, "is not among the models this rule declares"),
    ({"routes_to": ("a", "a")}, "must not repeat a model id"),
])
def test_an_inconsistent_routing_declaration_refuses_at_construction(overrides,
                                                                     match):
    kwargs = {k: v for k, v in overrides.items() if k != "resolved"}
    if "resolved" in overrides:
        kwargs["resolved"] = overrides["resolved"]
    with pytest.raises(InvalidCatalogEntryError, match=match):
        _rule(**kwargs)


# One SHARED badge across every target, so the rule's own badge stays one short
# segment. The first version of this helper gave each target its own badge and
# built a 901-byte rule badge — over `data_handling`'s 500 — which is half of why
# its "accepted" catalog was one the wire refuses (review N6).
_WIDE_BADGE = "Processed in the approved tenant boundary; no retention."

# rule + targets <= `models.maxItems: 64`, so 63 is the largest WIRE-CONFORMANT
# routable set even though `routes_to.maxItems` is 64. The helper defaults to the
# number a real catalog can actually hold.
MAX_WIRE_CONFORMANT_TARGETS = 63


def _wide_rule(n=MAX_WIRE_CONFORMANT_TARGETS):
    """A rule over `n` distinct targets, conformant on every other rule: unique
    ids, one shared badge carried as the rule's single routed segment, limits
    equal to the resolution's, and the resolution among them."""
    ids = tuple(f"t{i}" for i in range(n))
    badge = "Routes by role. / " + _WIDE_BADGE
    rule = ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "model_id": "auto",
                                "data_handling": badge, "routing_rule": True,
                                "routes_to": ids, "resolved_model_id": ids[0]})
    targets = [_entry(i, data_handling=_WIDE_BADGE) for i in ids]
    return rule, targets


def test_the_largest_wire_conformant_routable_set_constructs_and_SERVES():
    """CODEX REVIEW OF PR #244, P2, CORRECTED BY THE FINAL REVIEW (N6).

    The accepted case must be a catalog the WIRE accepts, or a two-sided
    boundary claim is only one-sided. The first version built 64 targets plus the
    rule — 65 models, over `models.maxItems: 64` — with a 901-byte rule badge,
    over `data_handling`'s 500: the catalog it ACCEPTED was one the wire refused
    on two grounds.

    So the accepted case is now the largest set a conformant catalog can express
    — 63 targets plus the rule, exactly 64 models — and it is checked THROUGH the
    projection against the released schema, which is the only way this assertion
    means what it says."""
    rule, targets = _wide_rule()
    catalog = ModelCatalog.from_entries([rule] + targets)
    assert len(catalog.entries[0].routes_to) == MAX_WIRE_CONFORMANT_TARGETS == 63
    assert len(catalog.entries) == 64

    envelope = catalog_wire_envelope(catalog)
    assert doxbench_contracts.validate_instance(
        envelope, doxbench_contracts.REPO_ROOT) == [], (
            "the accepted case must be one the released schema serves")


def test_routes_to_above_the_released_cap_is_refused_by_the_type():
    """The refusal half. 65 targets is over `routes_to.maxItems`, and the type
    used to accept it while the wire refused — the F2 divergence in the other
    direction, with the concrete consequence Codex named: such a rule constructs,
    the turn route (which checks only `isinstance(catalog, ModelCatalog)`) could
    dispatch it, and `GET /workbench/model-catalog` refuses to serve the catalog
    holding it.

    The 64/65 BOUNDARY itself is asserted where it is actually true — against the
    entry subschema — in `test_doxbench_contracts.py`; a whole catalog cannot
    reach 64 targets and stay conformant."""
    with pytest.raises(InvalidCatalogEntryError,
                       match=r"declares 65 models, above the 64"):
        _wide_rule(MAX_ROUTING_TARGETS + 1)
    assert MAX_ROUTING_TARGETS == 64
    # …and the operative maximum is one less, because the rule needs a slot too.
    assert MAX_WIRE_CONFORMANT_TARGETS == MAX_ROUTING_TARGETS - 1


# ONE table, driven through all three id-bearing fields. `model_id` joined the
# other two at contract-v2.2, and reusing the table rather than writing a fourth
# set of boundary values is what makes "one spelling holds all three" checkable.
MODEL_REFERENCE_CASES = [
    ("m", True, "one character is the shortest legal id"),
    ("ok.id-1_2", True, "dot, hyphen and underscore are all legal after the head"),
    ("9starts-with-a-digit", True, "the head may be a digit"),
    ("x" * MODEL_REFERENCE_MAX_LENGTH, True, "exactly at maxLength"),
    ("x" * (MODEL_REFERENCE_MAX_LENGTH + 1), False, "one over maxLength"),
    ("has spaces!", False, "space and bang are outside the pattern"),
    ("_leading", False, "the head must be alphanumeric"),
    (".leading", False, "the head must be alphanumeric"),
    ("-leading", False, "the head must be alphanumeric"),
    ("tráiling", False, "non-ASCII is refused though str.isalnum() accepts it"),
    ("has/slash", False, "the badge separator's character is not an id character"),
]


@pytest.mark.parametrize("reference, valid, why", MODEL_REFERENCE_CASES)
def test_the_two_NEW_id_bearing_fields_are_held_to_the_schemas_item_bounds(
        reference, valid, why):
    """FINAL REVIEW N7. The type learned `routes_to`'s `maxItems` and stopped
    there: its `items.maxLength`/`items.pattern` and the identical pair on
    `resolved_model_id` still escaped, so the same type-weaker-than-wire
    divergence survived on the two fields THIS release introduced.

    The non-ASCII row is the one worth reading: `"tráiling".isalnum()` is True,
    so a naive check passes it while the released pattern refuses it. That is
    why the predicate guards on `isascii()` — see
    `_is_conformant_model_reference`, which evaluates the pattern without
    importing `re`."""
    def build():
        return ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "model_id": "auto",
                                    "data_handling": "Routes. / " + CONTRACT_EXAMPLE[
                                        "data_handling"],
                                    "routing_rule": True,
                                    "routes_to": (reference,),
                                    "resolved_model_id": reference})
    if valid:
        assert build().resolved_model_id == reference, why
    else:
        with pytest.raises(InvalidCatalogEntryError):
            build()


@pytest.mark.parametrize("reference, valid, why", MODEL_REFERENCE_CASES)
def test_model_id_itself_is_now_held_to_the_SAME_released_bounds(reference,
                                                                 valid, why):
    """N7 CLOSED (contract-v2.2, Brett's ALL-FIVE ruling of 2026-08-24).

    This test is the rewrite its predecessor asked for. It used to pin
    `model_id`'s laxity as a recorded decision — the deferral reason being that
    tightening it "would be a behaviour change belonging to no release" — and
    said in as many words that if a future release closed the gap, this is the
    test that should fail and be rewritten. That release arrived, so it did.

    The cases are the SAME table the reference fields are driven through, which
    is the point: one spelling, three fields, no fourth set of boundary
    values."""
    build = lambda: ModelCatalogEntry(  # noqa: E731
        **{**CONTRACT_EXAMPLE, "model_id": reference})
    if valid:
        assert build().model_id == reference, why
    else:
        with pytest.raises(InvalidCatalogEntryError):
            build()


def test_the_model_id_refusal_names_the_measured_length_and_the_released_bound():
    with pytest.raises(InvalidCatalogEntryError) as caught:
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "model_id": "m" * 500})
    assert "500 characters" in str(caught.value)
    assert str(MODEL_REFERENCE_MAX_LENGTH) in str(caught.value)


# ---------------------------------------------------------------------------
# contract-v2.2 — THE THREE DESCRIPTIVE STRING BOUNDS
#
# `label`, `provider_class` and `data_handling` were checked type-side for
# blankness alone; the released schema bounds all three by length. Brett's
# ALL-FIVE ruling (2026-08-24) closed them in the same release as `model_id`, so
# that after it EVERY string bound the schema declares is enforced at
# construction with no residue. The schema-DRIVEN proof of "no residue" lives in
# `test_doxbench_contracts.py`, which walks the released bytes rather than this
# list of three names; these are the boundary cases and the message contract.
# ---------------------------------------------------------------------------

DESCRIPTIVE_BOUNDS = [
    ("label", LABEL_MAX_LENGTH),
    ("provider_class", PROVIDER_CLASS_MAX_LENGTH),
    ("data_handling", DATA_HANDLING_MAX_LENGTH),
]


@pytest.mark.parametrize("field, maximum", DESCRIPTIVE_BOUNDS)
def test_a_descriptive_field_exactly_at_its_released_maximum_constructs(field,
                                                                        maximum):
    entry = ModelCatalogEntry(**{**CONTRACT_EXAMPLE, field: "a" * maximum})
    assert len(getattr(entry, field)) == maximum


@pytest.mark.parametrize("field, maximum", DESCRIPTIVE_BOUNDS)
def test_a_descriptive_field_one_over_its_released_maximum_is_refused(field,
                                                                      maximum):
    """Reproduced before the ruling and closed by it: 201, 65 and 501
    characters respectively all constructed cleanly while
    `GET /workbench/model-catalog` refused to serve the catalog holding them."""
    with pytest.raises(InvalidCatalogEntryError) as caught:
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, field: "a" * (maximum + 1)})
    message = str(caught.value)
    # The ratified scenario asks the refusal to name the measured length AND the
    # released maximum for that field.
    assert field in message
    assert str(maximum + 1) in message
    assert str(maximum) in message


@pytest.mark.parametrize("field, _maximum", DESCRIPTIVE_BOUNDS)
def test_a_descriptive_field_keeps_its_pre_existing_blankness_refusal(field,
                                                                      _maximum):
    """The length bound is ADDED to the blankness check, never substituted for
    it — a bound that silently replaced the older refusal would be a regression
    dressed as a tightening."""
    with pytest.raises(InvalidCatalogEntryError, match="must not be blank"):
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, field: "   "})


# ---------------------------------------------------------------------------
# contract-v2.2 — THE CATALOG-LEVEL ENTRY CAP
# ---------------------------------------------------------------------------


def _n_entries(count):
    return tuple(_entry(f"m{i}") for i in range(count))


def test_a_catalog_exactly_at_the_released_entry_maximum_constructs():
    assert len(ModelCatalog(_n_entries(MAX_CATALOG_ENTRIES)).entries) == \
        MAX_CATALOG_ENTRIES


def test_a_catalog_over_the_released_entry_maximum_is_refused_at_construction():
    """Reproduced before the release: a 65-entry catalog constructed cleanly and
    could be dispatched by the turn route, while the catalog route refused to
    serve the very catalog holding it."""
    with pytest.raises(CatalogEntryCountError) as caught:
        ModelCatalog(_n_entries(MAX_CATALOG_ENTRIES + 1))
    message = str(caught.value)
    assert str(MAX_CATALOG_ENTRIES + 1) in message
    assert str(MAX_CATALOG_ENTRIES) in message


def test_the_entry_cap_is_a_WHOLE_CATALOG_refusal_and_says_so_in_its_class():
    """Which exception, and why. No single entry is wrong, so
    `InvalidCatalogEntryError` — whose docstring says a single field failed —
    would be a false statement about what happened; and an over-large catalog of
    plain entries is not a routing inconsistency, so `InvalidRoutingRuleError`
    is wrong for the opposite reason. Its own class, exactly as
    `DuplicateModelIdError` has one for its own whole-catalog condition."""
    assert issubclass(CatalogEntryCountError, ModelCatalogError)
    assert not issubclass(CatalogEntryCountError, InvalidCatalogEntryError)
    assert not issubclass(CatalogEntryCountError, InvalidRoutingRuleError)
    assert not issubclass(CatalogEntryCountError, DuplicateModelIdError)


def test_from_entries_and_the_direct_constructor_both_enforce_the_cap():
    for build in (ModelCatalog, ModelCatalog.from_entries):
        with pytest.raises(CatalogEntryCountError):
            build(_n_entries(MAX_CATALOG_ENTRIES + 1))


def test_the_pre_existing_duplicate_refusal_still_wins_on_an_oversize_catalog():
    """Ordering, pinned: the element-type and duplicate scans run first, so
    every catalog that had one of those refusals keeps exactly it."""
    entries = _n_entries(MAX_CATALOG_ENTRIES) + (_entry("m0"),)
    with pytest.raises(DuplicateModelIdError):
        ModelCatalog(entries)


# ---------------------------------------------------------------------------
# contract-v2.2 — THE CLOSED INPUT-MODALITY VOCABULARY
# ---------------------------------------------------------------------------


def test_the_vocabulary_is_exactly_text_and_image():
    assert CATALOG_MODALITIES == ("text", "image")
    assert REQUIRED_MODALITY == "text"
    assert REQUIRED_MODALITY in CATALOG_MODALITIES


def test_an_entry_may_declare_that_it_accepts_images():
    entry = ModelCatalogEntry(**{**CONTRACT_EXAMPLE,
                                 "modalities": ["text", "image"]})
    assert entry.modalities == ("text", "image")
    assert entry.declares_modalities is True
    assert entry.routing_modalities == ("text", "image")


def test_a_text_only_declaration_is_a_declaration():
    entry = ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": ["text"]})
    assert entry.declares_modalities is True
    assert entry.routing_modalities == ("text",)
    # …and it is DISTINGUISHABLE from silence, which is the whole point of the
    # absence rule: the same routing set, a different recorded fact.
    silent = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    assert silent.routing_modalities == entry.routing_modalities
    assert silent.declares_modalities is False


def test_an_entry_that_declares_nothing_is_valid_and_makes_no_claim():
    """THE ADDITIVE PROPERTY, at the type. Absence is not "this model rejects
    images"; it is "this producer predates the field". The reader gets the safe
    reading for routing AND the fact that nothing was declared."""
    plain = ModelCatalogEntry(**CONTRACT_EXAMPLE)
    assert plain.modalities is None
    assert plain.declares_modalities is False
    assert plain.routing_modalities == (REQUIRED_MODALITY,)
    assert plain.as_public_dict() == CONTRACT_EXAMPLE


def test_absence_and_the_empty_set_are_DIFFERENT_values():
    """`None` and `()` are not synonyms here, exactly as they are not on the
    wire: the released schema has no key for the first and `minItems: 1` for
    the second. A default of `()` would have made a producer's empty
    declaration indistinguishable from silence."""
    assert ModelCatalogEntry(**CONTRACT_EXAMPLE).modalities is None
    with pytest.raises(InvalidCatalogEntryError, match="must not be empty"):
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": []})


@pytest.mark.parametrize("declared, match", [
    (["text", "audio"], "outside the closed vocabulary"),
    (["audio"], "outside the closed vocabulary"),
    (["Text"], "outside the closed vocabulary"),
    (["image"], "must contain 'text'"),
    (["text", "text"], "must not repeat a member"),
    ([], "must not be empty"),
])
def test_a_nonconforming_modality_declaration_is_refused_at_construction(
        declared, match):
    with pytest.raises(InvalidCatalogEntryError, match=match):
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": declared})


def test_the_out_of_vocabulary_refusal_names_the_closed_set_and_its_remedy():
    """The ratified scenario's THEN: the refusal names the closed vocabulary,
    and the remedy is the change that governs the new modality — never a wider
    field."""
    with pytest.raises(InvalidCatalogEntryError) as caught:
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": ["text", "audio"]})
    message = str(caught.value)
    assert "text" in message and "image" in message
    assert "change that governs" in message


@pytest.mark.parametrize("bad", ["text", b"text", 7, object()])
def test_modalities_that_is_not_an_iterable_of_names_is_a_TypeError(bad):
    """A bare string is the trap worth naming: it IS iterable, and iterating it
    would silently declare four single-character modalities."""
    with pytest.raises(TypeError):
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": bad})


def test_a_non_string_modality_member_is_a_TypeError():
    with pytest.raises(TypeError):
        ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": ["text", 7]})


def test_a_declared_set_is_materialized_to_a_tuple_the_caller_cannot_mutate():
    source = ["text", "image"]
    entry = ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "modalities": source})
    source.append("audio")
    assert entry.modalities == ("text", "image")


def test_a_declared_set_reaches_the_public_dict_after_the_base_seven():
    """THE WIRE GAP THE BOT ROUND FOUND. `as_public_dict` emits an explicit key
    list rather than serializing the dataclass, so without a deliberate
    projection a declared set would have been validated in process and then
    silently dropped — leaving consumers and the routing successor with nothing
    to read, which is the entire purpose of the field."""
    entry = ModelCatalogEntry(**{**CONTRACT_EXAMPLE,
                                 "modalities": ["text", "image"]})
    public = entry.as_public_dict()
    assert list(public) == list(PUBLIC_ENTRY_FIELDS) + ["modalities"]
    assert public["modalities"] == ["text", "image"]
    # A LIST (JSON has no tuple), sharing no state with the frozen entry.
    public["modalities"].append("smuggled")
    assert entry.modalities == ("text", "image")


def test_an_undeclared_entrys_public_dict_is_byte_identical_across_the_release():
    """The additive property at the wire: an entry that declares nothing emits
    no key, so its bytes are exactly the bytes it emitted before this release."""
    plain = ModelCatalogEntry(**CONTRACT_EXAMPLE).as_public_dict()
    assert "modalities" not in plain
    assert list(plain) == list(PUBLIC_ENTRY_FIELDS)


def test_a_routing_rule_may_also_declare_modalities_and_the_order_is_fixed():
    """Both optional groups on one entry: the capability field sits between the
    base seven and the routing three, which is what `DECLARABLE_ENTRY_FIELDS`
    declares and what makes each group an append."""
    rule = _rule(modalities=["text", "image"])
    public = rule.as_public_dict()
    assert list(public) == list(DECLARABLE_ENTRY_FIELDS)


def test_the_wire_envelope_carries_a_declared_set_and_leaves_silent_entries_alone():
    catalog = ModelCatalog.from_entries([
        _entry("declaring", modalities=["text", "image"]),
        _entry("silent"),
    ])
    envelope = catalog_wire_envelope(catalog)
    assert envelope["models"][0]["modalities"] == ["text", "image"]
    assert "modalities" not in envelope["models"][1]


def test_the_pattern_predicate_needs_no_regex_import():
    """`_is_conformant_model_reference` exists so this module's import list stays
    `dataclasses` and `typing`, which its own docstring promises."""
    src = MODULE_PATH.read_text(encoding="utf-8")
    assert "import re" not in src
    assert MODEL_REFERENCE_PATTERN == "^[A-Za-z0-9][A-Za-z0-9._-]*$"


def test_the_target_cap_is_an_ENTRY_refusal_not_a_catalog_one():
    """Which exception, and why — the split this release documents is by how
    much context a refusal needs, not by which field it names. The cap is
    visible with no catalog at all, so it is `InvalidCatalogEntryError`, like
    every other over-cap value. Codex suggested `InvalidRoutingRuleError`;
    declined, because that class's own docstring says every member of it needs a
    second entry to see."""
    with pytest.raises(InvalidCatalogEntryError):
        _wide_rule(MAX_ROUTING_TARGETS + 1)
    # …and it is raised by the ENTRY, before any catalog exists.
    assert not issubclass(InvalidRoutingRuleError, InvalidCatalogEntryError)
    assert not issubclass(InvalidCatalogEntryError, InvalidRoutingRuleError)


def test_a_plain_entry_may_not_carry_a_routing_only_field():
    """The other direction of the schema's `dependentRequired`: a directly
    answering model that resolves elsewhere is the hidden routing decision the
    ratified requirement forbids."""
    for field, value in (("routes_to", ("a",)), ("resolved_model_id", "a")):
        with pytest.raises(InvalidCatalogEntryError,
                           match="must declare neither"):
            ModelCatalogEntry(**{**CONTRACT_EXAMPLE, field: value})


def test_routing_field_types_are_refused_with_TypeError_not_a_value_error():
    """The module's existing split, extended: a wrong PYTHON TYPE is a caller
    programming error, a wrong VALUE is a catalog refusal."""
    def _raw(**overrides):
        # The DIRECT constructor, not the `_rule` helper: that helper coerces
        # `routes_to` with `tuple(...)`, which would turn a bare string into a
        # one-member tuple and hide the exact case under test.
        return ModelCatalogEntry(**{**CONTRACT_EXAMPLE, "routing_rule": True,
                                    "routes_to": ("a",),
                                    "resolved_model_id": "a", **overrides})

    with pytest.raises(TypeError, match="routing_rule must be a bool"):
        _raw(routing_rule="yes")
    with pytest.raises(TypeError, match="not a single str"):
        _raw(routes_to="a")
    with pytest.raises(TypeError, match="not a single bytes"):
        _raw(routes_to=b"a")
    with pytest.raises(TypeError, match="routes_to must be an iterable"):
        _raw(routes_to=7)
    with pytest.raises(TypeError, match="routes_to member must be a str"):
        _raw(routes_to=(7,))
    with pytest.raises(TypeError, match="resolved_model_id must be a str"):
        _raw(resolved_model_id=7)


@pytest.mark.parametrize("entries_factory, match", [
    # 1. no dangling target
    (lambda: [_rule(routes_to=("ghost",), resolved="ghost"), _entry("a")],
     "which is not in this catalog"),
    # 2. no chained rule
    (lambda: [
        _rule("outer", routes_to=("inner",), resolved="inner",
              badge="Routes by role (outer). / Routes by role (inner). / "
                    + CONTRACT_EXAMPLE["data_handling"]),
        _rule("inner", routes_to=("a",), resolved="a"),
        _entry("a")],
     "which is itself a routing rule"),
    # 3. the badge covering
    (lambda: [_rule(routes_to=("a", "b"), resolved="a",
                    badge=CONTRACT_EXAMPLE["data_handling"]),
              _entry("a"), _entry("b", data_handling="a different posture")],
     "does not carry the data-handling badge"),
    # 4. an available rule resolving to an unavailable model
    (lambda: [_rule(routes_to=("a",), resolved="a"),
              _entry("a", available=False)],
     "is available but resolves to"),
    # 5'. a rule wider than THE MODEL IT RESOLVES TO (Brett's ruling)
    (lambda: [_rule(routes_to=("a",), resolved="a", input_limit_bytes=800_000),
              _entry("a", input_limit_bytes=2048)],
     "above the 2048 of 'a', the model it resolves to"),
])
def test_a_catalog_refuses_a_routing_rule_it_cannot_honestly_offer(
        entries_factory, match):
    """The five CROSS-ENTRY rules. The catalog refuses AS A WHOLE, exactly as a
    duplicated model_id does: dropping the offending entry would leave the
    operator's declaration silently unserved."""
    with pytest.raises(InvalidRoutingRuleError, match=match):
        ModelCatalog.from_entries(entries_factory())
    # And the same refusal through the direct constructor, not only the
    # intention-revealing wrapper.
    with pytest.raises(InvalidRoutingRuleError, match=match):
        ModelCatalog(entries=tuple(entries_factory()))


def test_a_rule_MAY_be_wider_than_a_non_resolved_member__rule_5_prime():
    """RULE 5' — BRETT'S RULING, 2026-08-21 ("Swap to rule 5'"), pinned here
    because it is the case the FIRST form of the rule got wrong.

    The rule declares 800,000 bytes while `narrow` — a model it MAY route to —
    accepts 2,048. That is LAWFUL, because the bound is the model it RESOLVES
    to (`wide`, which accepts 800,000). The first shipped form min-capped
    against every member of `routes_to` and would have refused this catalog.

    Three reasons the ruling gives, and the third is why this test is named for
    it rather than folded into the rule-5 table: min-capping would BAKE IN
    semantics that contradict the sanctioned per-turn fit-aware router staged as
    `ideation/staging/doxchat-auto-fit-routing/`, under which a rule's declared
    ceiling is the WIDEST thing it can serve and the router picks a destination
    that fits each turn. A min-cap would have had to be undone to get there."""
    catalog = ModelCatalog.from_entries([
        _rule(routes_to=("wide", "narrow"), resolved="wide",
              input_limit_bytes=800_000, output_limit_bytes=900_000,
              badge="Routes by role. / " + CONTRACT_EXAMPLE["data_handling"]
                    + " / a narrower posture"),
        _entry("wide", input_limit_bytes=800_000, output_limit_bytes=900_000),
        _entry("narrow", input_limit_bytes=2048, output_limit_bytes=8192,
               data_handling="a narrower posture")])
    rule = catalog.entries[0]
    assert rule.input_limit_bytes == 800_000
    # …and the discriminator, stated: the rule IS wider than a routable member.
    assert rule.input_limit_bytes > catalog.entry_for("narrow").input_limit_bytes
    assert rule.input_limit_bytes == catalog.entry_for("wide").input_limit_bytes

    # The other side of the ruling, so it is a bound and not an absence: wider
    # than the RESOLUTION is still refused.
    with pytest.raises(InvalidRoutingRuleError,
                       match="the model it resolves to"):
        ModelCatalog.from_entries([
            _rule(routes_to=("wide", "narrow"), resolved="narrow",
                  input_limit_bytes=800_000, output_limit_bytes=8192,
                  badge="Routes by role. / " + CONTRACT_EXAMPLE["data_handling"]
                        + " / a narrower posture"),
            _entry("wide", input_limit_bytes=800_000, output_limit_bytes=900_000),
            _entry("narrow", input_limit_bytes=2048, output_limit_bytes=8192,
                   data_handling="a narrower posture")])


def test_an_unavailable_rule_may_resolve_to_an_unavailable_model():
    """The availability rule's own boundary, and the reason the degraded-bridge
    path still constructs: `OmpHarnessBridge.catalog()` marks EVERY entry
    unavailable after a child dies, which would be unbuildable if the rule
    applied to an unselectable rule."""
    catalog = ModelCatalog.from_entries([
        _rule(routes_to=("a",), resolved="a", available=False),
        _entry("a", available=False)])
    assert catalog.entries[0].routing_rule is True
    # And that is exactly what the bridge's degraded projection produces.
    degraded = ModelCatalog.from_entries(
        dataclasses.replace(entry, available=False)
        for entry in ModelCatalog.from_entries(
            [_rule(routes_to=("a",), resolved="a"), _entry("a")]).entries)
    assert degraded.entries[0].routes_to == ("a",)
    assert all(entry.available is False for entry in degraded.entries)


def test_a_routing_rule_is_selectable_and_looked_up_like_any_other_entry():
    """No new lookup path: the rule is an entry, so the route's existing
    step-7 revalidation (`selectable_entry_for`) governs it unchanged."""
    catalog = ModelCatalog.from_entries(
        [_rule(routes_to=("a",), resolved="a"), _entry("a")])
    rule = catalog.selectable_entry_for("auto")
    assert rule is not None and rule.resolved_model_id == "a"
    assert catalog.entry_for("a").routing_rule is False
    assert [entry.model_id for entry in catalog.available_entries()] == ["auto", "a"]


# ---------------------------------------------------------------------------
# THE TWO GATES SHARE ONE GRAMMAR (contract-v1.38; adversarial review round 1
# F1/F2)
#
# The delegated validator is a standalone script that imports nothing from this
# package, so the separator and the normalizer are RESTATED there. Two copies of
# a rule drift apart invisibly because both copies keep passing — the same
# hazard §12.2 recorded for its no-implicit-push list — so the copies are pinned
# equal here, and the PARITY of the two gates is asserted over the packaged
# negatives rather than merely claimed in a docstring (which is precisely the
# claim review round 1 found untrue).
# ---------------------------------------------------------------------------

_VALIDATOR_PATH = carved_source(
    "scripts/validate-ideation-dashboard-contracts.py")


@pytest.fixture(scope="module")
def delegated_validator():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vidc_badge_parity", _VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_badge_grammar_is_one_spelling_in_both_gates(delegated_validator):
    assert (delegated_validator.ROUTING_BADGE_SEPARATOR
            == doxbench_model.ROUTING_BADGE_SEPARATOR == " / ")
    assert (delegated_validator.ROUTING_BADGE_TRAILING_PUNCTUATION
            == doxbench_model.ROUTING_BADGE_TRAILING_PUNCTUATION == ".;,")


@pytest.mark.parametrize("text", [
    "Processed in the approved tenant boundary; no retention.",
    "  leading and trailing  ",
    "collapsed\n   across a\twrap",
    "ON-TENANT",
    "trailing punctuation.;,",
    "",
    " / ",
])
def test_the_two_gates_normalize_a_segment_identically(delegated_validator, text):
    assert (delegated_validator.normalized_badge_segment(text)
            == doxbench_model.normalized_badge_segment(text))
    assert (delegated_validator.badge_segments(text)
            == doxbench_model.badge_segments(text))


def test_the_normalizer_forgives_only_what_cannot_flip_a_posture():
    """The three normalizations, and the one thing that must NEVER normalize.

    `on-tenant` vs `non-tenant` is the pair the reviewer used to break substring
    containment, so it is the pair pinned here: no amount of case, whitespace or
    trailing-punctuation forgiveness may make them equal."""
    n = doxbench_model.normalized_badge_segment
    # forgiven, because none of these is a different posture
    assert n("On-Tenant") == n("on-tenant") == n("  on-tenant  ") == n("on-tenant.")
    assert n("no  retention") == n("no retention")
    assert n("no retention;") == n("no retention,") == n("no retention")
    # NOT forgiven
    assert n("on-tenant") != n("non-tenant")
    assert n("retain") != n("retain nothing")
    assert n("zero retention") != n("no retention")


@pytest.mark.parametrize("rule_badge, target_badge, why", [
    ("Routes to a non-tenant endpoint.", "on-tenant",
     "review instance A: the rule states the INVERSE of the target's posture, "
     "and `'on-tenant' in 'non-tenant'` is True"),
    ("All routed models are on approved tenant infrastructure and retain nothing.",
     "retain",
     "review instance D: the target's whole badge is a common word the rule's "
     "prose contains by accident"),
    ("Processed in the approved tenant boundary; no retention. and more",
     "Processed in the approved tenant boundary; no retention.",
     "a badge swallowed into a longer sentence is not a segment"),
])
def test_the_covering_refuses_what_raw_substring_containment_accepted(
        rule_badge, target_badge, why):
    """THE DIRECT PIN on the type's own predicate (adversarial review round 1
    F1). Each row is a case the OLD `in` test accepted; each must now refuse,
    and refuse HERE rather than only through the packaged-corpus parity test —
    a rule that lives in only one gate's test is a rule the other gate can
    lose."""
    with pytest.raises(InvalidRoutingRuleError,
                       match="as a segment of its own badge"):
        ModelCatalog.from_entries([
            _rule(routes_to=("a",), resolved="a", badge=rule_badge),
            _entry("a", data_handling=target_badge)])


def test_the_covering_accepts_a_badge_that_IS_a_segment():
    """The other direction, so the predicate cannot have become a blanket
    refusal: the same target badge, carried as a real segment, is accepted —
    including across the three forgiven normalizations."""
    badge = "Processed in the approved tenant boundary; no retention."
    for rule_badge in (
            "Routes by role. / " + badge,
            badge + " / Routes by role.",
            "Routes by role. / " + badge.upper(),
            "Routes by role. /   " + badge.rstrip(".") + "   ",
    ):
        catalog = ModelCatalog.from_entries([
            _rule(routes_to=("a",), resolved="a", badge=rule_badge),
            _entry("a", data_handling=badge)])
        assert catalog.entries[0].routing_rule is True


@pytest.mark.parametrize("badge", [
    "Read / write access.",          # holds the separator literally
    "Read /  write access.",         # collapses onto it (doubled space)
    "Read /\nwrite access.",         # collapses onto it (line wrap)
])
def test_a_target_badge_that_holds_the_separator_is_refused_as_ill_formed(badge):
    """The grammar's own residual collision, closed rather than hoped away: a
    badge containing " / " could never BE one segment, so the catalog refuses
    instead of silently splitting the badge in half and matching a fragment.

    THE COLLAPSING FORMS ARE THE POINT (review re-verify N3). The arm used to
    test the RAW badge, so `"Read /\nwrite access."` — which holds no literal
    " / " — slipped it AND THEN PASSED THE COVERING CHECK, because the rule's
    own badge normalizes to exactly that segment. That was a full ACCEPT of an
    ill-formed badge, not a misdirected message, which is why all three forms
    are pinned and why the message is matched rather than just the refusal."""
    with pytest.raises(InvalidRoutingRuleError,
                       match="contains ' / ', the routing badge's own"):
        ModelCatalog.from_entries([
            _rule(routes_to=("a",), resolved="a",
                  badge="Routes by role. / " + badge),
            _entry("a", data_handling=badge)])


def test_the_resolved_models_badge_is_covered_because_it_must_be_a_member():
    """F2's note, asserted rather than assumed: `resolved_model_id ∈ routes_to`
    plus the covering loop over `routes_to` means the ANSWERING model's badge is
    necessarily carried. The construction below is the one the reviewer walked
    past the file gate — a rule badged safe resolving to a model badged for
    vendor training — and it is refused for the membership reason BEFORE any
    covering question is asked."""
    safe = CONTRACT_EXAMPLE["data_handling"]
    leaky = "Content is retained and used for vendor model training."
    with pytest.raises(InvalidCatalogEntryError,
                       match="is not among the models this rule declares"):
        _rule(routes_to=("safe",), resolved="leaky")
    # And with membership held, the resolved model's badge IS one of the
    # segments the covering rule just checked.
    catalog = ModelCatalog.from_entries([
        _rule(routes_to=("safe", "leaky"), resolved="leaky",
              badge="Routes by role. / " + safe + " / " + leaky),
        _entry("safe", data_handling=safe),
        _entry("leaky", data_handling=leaky)])
    rule = catalog.entries[0]
    resolved = catalog.entry_for(rule.resolved_model_id)
    assert rule.resolved_model_id in rule.routes_to
    assert (doxbench_model.normalized_badge_segment(resolved.data_handling)
            in doxbench_model.badge_segments(rule.data_handling))
