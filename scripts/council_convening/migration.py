"""Protocol selection, activation evidence and historical classification (Phase 6).

T061, per data-model E1 (the effects rows for `deprecated` and `historical_only`
live in `classification`), E11 and E12, and contracts/conformance-corpus.md.
Written from the data model's rules and nothing else (research R4). Three corpus
boundaries are registered here:

* `selection` (E11), in its order. Steps 1 to 3 run over every selection in the
  vector before the next step begins, the producer's, then the consumer's, then
  the later attempt's:
    1. `selection_malformed`: the record breaks its schema, or a record presented
       as one side's selection names the other side;
    2. `protocol_unknown`: the protocol names no registry entry;
    3. an `active` replacement selection while the replacement is not
       `admission_eligible`: `replacement_not_admission_eligible`; any legacy
       selection, in either mode, while the legacy entry is `historical_only`:
       `legacy_protocol_refused`;
    4. `pair_mismatched`, unless `mode`, `protocol`, `provider_commit`,
       `provider_bundle` and `corpus_index_sha256` are all equal;
    5. `rejected_without_fallback`: a later attempt that names any protocol other
       than the one a refusal was recorded under.
* `activation` (E12), in its order: `activation_evidence_malformed`;
  `activation_evidence_incomplete`; for an activation or resume, each
  `binding_refs` entry in order, `binding_unresolved` then
  `broker_capability_insufficient`; `pair_mismatched`; and
  `historical_reinterpretation_refused`.
* `historical`: a record classified by its recorded protocol, never
  reinterpreted, at any status. A legacy record is ROUTED, never passed; a
  replacement record goes on to the replacement rules.

BROKER CAPABILITY HAS ONE SOURCE OF TRUTH: each producer binding's `broker`
member, read through the activation's `binding_refs` against the consumer's
configured binding set. An activation record carries no broker state of its own.
Under Brett Heap's 025 ruling (A), "Per-seat environments (Recommended)", that set
is the commission binding plus one binding per seat.

THE BACKING REHEARSAL. `rehearsal_ref` is the raw SHA-256 of the exact UTF-8 text
of a rehearsal record. It is backed only by a rehearsal record that this order
itself accepts, whose `rehearsal.mode` is `matched` and `outcome` is `pass`, whose
`provider` is the activation's, and each of whose sides' selections equals the
activation's on every matched value but `mode`. `mode` is the one matched value a
rehearsal cannot share with its activation: a rehearsal runs its selections in
`mode: rehearsal`, an activation in `mode: active`. That reading is disclosed in
evidence.md § Phase 6.

NO STATUS IS READ BUT WHERE THE ORDER SAYS SO. Selection step 3 reads the status of
the entry a selection names, and records which, so the corpus can require that
vector's `registry_status` override. The activation and historical boundaries
read none. In production a selection's status is the registry's AT THE PIN THE
SELECTION NAMES: under Brett Heap's ruling of 2026-10-09T13:22:16Z, "Back to
Release A pins (Recommended)", a paired rollback after activation returns both
sides to their Release A pins, where legacy is still `deprecated` and selectable.

THE CORPUS HANDLERS are registered by `corpus` at its foot, as Phase 2's are, and
this module imports `corpus` only inside them, so no import cycle closes.
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping, Sequence

from . import classification, records

SELECTION_KIND = "xfactory_council_protocol_selection"
ACTIVATION_KIND = "xfactory_council_activation_evidence"
SELECTION_SCHEMA_ID = records.ID_BASE + "protocol-selection.schema.yaml"
ACTIVATION_SCHEMA_ID = records.ID_BASE + "activation-evidence.schema.yaml"
BINDING_KIND = "xfactory_council_producer_binding"

SIDES = ("producer", "consumer")

#: The five values a pair is matched on (E11 step 4).
MATCHED = ("mode", "protocol", "provider_commit", "provider_bundle", "corpus_index_sha256")
#: The matched values a backing rehearsal must share with its activation.
REHEARSAL_MATCHED = MATCHED[1:]

ACTIVATING_ACTS = ("activation", "resume")

#: Each act's required members, beside `schema_version`, `kind` and `act`
#: (data-model E12). A rehearsal whose `rehearsal.mode` is `matched` also needs
#: `intake`.
ACT_REQUIRED: dict[str, tuple[str, ...]] = {
    "pause": ("recorded_at", "provider", "owner_word"),
    "drain": ("recorded_at", "provider", "intake", "in_flight"),
    "switch": ("recorded_at", "provider", "owner_word", "intake", "producer", "consumer"),
    "rehearsal": ("recorded_at", "provider", "producer", "consumer", "rehearsal"),
    "activation": ("recorded_at", "provider", "owner_word", "intake", "producer",
                   "consumer", "rehearsal_ref", "binding_refs"),
    "rollback": ("recorded_at", "provider", "owner_word", "intake", "producer",
                 "consumer", "rollback"),
    "resume": ("recorded_at", "provider", "owner_word", "producer", "consumer",
               "rehearsal_ref", "binding_refs"),
}
ROLLBACK_REQUIRED = ("restored_producer", "restored_consumer", "new_records_retained",
                     "new_records_protocol")


class _Reads:
    """Registry status reads, recorded in the order they happen."""

    def __init__(self, registry: classification.Registry,
                 overrides: Mapping[str, str] | None):
        self.registry = registry
        self.overrides = overrides
        self.read: list[str] = []

    def __call__(self, protocol_id: str) -> str:
        if protocol_id not in self.read:
            self.read.append(protocol_id)
        return self.registry.status(protocol_id, self.overrides)

    def outcome(self, outcome: str, refusal: str | None = None) -> records.Outcome:
        return records.Outcome(outcome, refusal, status_read=bool(self.read),
                               statuses_read=tuple(self.read))


# --------------------------------------------------------------------------
# E11: selection.
# --------------------------------------------------------------------------

def _eligibility(selection: Mapping[str, Any], registry: classification.Registry,
                 reads: _Reads) -> str | None:
    """Step 3 for one well-formed, registered selection."""
    protocol = selection["protocol"]
    if protocol == registry.replacement_id:
        if selection["mode"] == "active" and reads(protocol) != "admission_eligible":
            return "replacement_not_admission_eligible"
    elif protocol == registry.legacy_id:
        if reads(protocol) == "historical_only":
            return "legacy_protocol_refused"
    return None


def select(entries: Sequence[tuple[str | None, Any]], registry: classification.Registry,
           schemas: records.SchemaSet, statuses: Mapping[str, str] | None = None, *,
           pair: tuple[Any, Any] | None = None,
           rejected_under: str | None = None,
           attempt: Any = None) -> records.Outcome:
    """The `selection` order over `entries`, `(role, record)` pairs in order.

    `role` is the side a record is presented for, or `None` where no side is
    implied (a later attempt, or one record checked alone). `pair`, when given,
    is the producer's and the consumer's record for step 4; `rejected_under`
    with `attempt` is step 5.
    """
    reads = _Reads(registry, statuses)
    for role, record in entries:
        if (not isinstance(record, Mapping) or schemas.errors(SELECTION_SCHEMA_ID, record)
                or (role is not None and record.get("side") != role)):
            return reads.outcome("refuse", "selection_malformed")
    for _role, record in entries:
        if record["protocol"] not in registry.entries:
            return reads.outcome("refuse", "protocol_unknown")
    for _role, record in entries:
        refusal = _eligibility(record, registry, reads)
        if refusal:
            return reads.outcome("refuse", refusal)
    if pair is not None and any(pair[0][m] != pair[1][m] for m in MATCHED):
        return reads.outcome("refuse", "pair_mismatched")
    if rejected_under is not None and attempt["protocol"] != rejected_under:
        return reads.outcome("refuse", "rejected_without_fallback")
    return reads.outcome("accept")


def select_pair(producer: Any, consumer: Any, registry: classification.Registry,
                schemas: records.SchemaSet, statuses: Mapping[str, str] | None = None, *,
                rejected_under: str | None = None, attempt: Any = None,
                with_attempt: bool = False) -> records.Outcome:
    entries: list[tuple[str | None, Any]] = [("producer", producer), ("consumer", consumer)]
    if with_attempt:
        entries.append((None, attempt))
    return select(entries, registry, schemas, statuses, pair=(producer, consumer),
                  rejected_under=rejected_under if with_attempt else None, attempt=attempt)


def selection_handler(vector: Mapping[str, Any], context: Any) -> records.Outcome:
    """The corpus handler for `selection`."""
    from . import corpus

    inputs = vector["inputs"]
    pair_members = ("selection_producer", "selection_consumer")
    fallback_members = pair_members + ("rejected_under", "selection_attempt")
    if not isinstance(inputs, dict) or set(inputs) not in (set(pair_members),
                                                           set(fallback_members)):
        raise corpus.VectorInputError(
            "inputs must be exactly {selection_producer, selection_consumer}, with "
            "rejected_under and selection_attempt together or not at all")
    with_attempt = "selection_attempt" in inputs
    if with_attempt and inputs["rejected_under"] not in context.registry.entries:
        raise corpus.VectorInputError("inputs.rejected_under names no registry entry")
    statuses = corpus._statuses(vector.get("environment", {}), context)
    joined = {key: corpus.join_parts(value) for key, value in inputs.items()}
    return select_pair(joined["selection_producer"], joined["selection_consumer"],
                       context.registry, context.schemas, statuses,
                       rejected_under=joined.get("rejected_under"),
                       attempt=joined.get("selection_attempt"), with_attempt=with_attempt)


# --------------------------------------------------------------------------
# E12: activation evidence.
# --------------------------------------------------------------------------

def _missing(record: Mapping[str, Any]) -> bool:
    act = record["act"]
    if any(member not in record for member in ACT_REQUIRED[act]):
        return True
    if act == "rehearsal" and record["rehearsal"]["mode"] == "matched" and "intake" not in record:
        return True
    if act == "rollback" and any(m not in record["rollback"] for m in ROLLBACK_REQUIRED):
        return True
    return False


def raw_sha256_of_text(text: str) -> str | None:
    """`sha256:` plus the hex SHA-256 of `text`'s UTF-8 bytes, or None for a text
    with no UTF-8 encoding (a lone surrogate)."""
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        return None
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _backed(record: Mapping[str, Any], rehearsal: Any, registry: classification.Registry,
            schemas: records.SchemaSet) -> bool:
    """Whether `rehearsal`, the text `inputs.rehearsal` supplies, is the passing
    matched rehearsal `record.rehearsal_ref` names, with the record's values."""
    from . import corpus

    if not isinstance(rehearsal, str) or raw_sha256_of_text(rehearsal) != record["rehearsal_ref"]:
        return False
    try:
        backing = corpus.loads_strict(rehearsal)
    except ValueError:
        return False
    if not isinstance(backing, dict) or backing.get("act") != "rehearsal":
        return False
    if activation(backing, registry, schemas).outcome != "accept":
        return False
    if (backing["rehearsal"]["mode"], backing["rehearsal"]["outcome"]) != ("matched", "pass"):
        return False
    if backing["provider"] != record["provider"]:
        return False
    return all(backing[side]["selection"][m] == record[side]["selection"][m]
               for side in SIDES for m in REHEARSAL_MATCHED)


def activation(record: Any, registry: classification.Registry, schemas: records.SchemaSet,
               bindings: Sequence[Mapping[str, Any]] | None = None,
               rehearsal: Any = None, *, offline: bool = False) -> records.Outcome:
    """The `activation` order over one E12 record.

    For an activation or resume, `bindings` is the consumer's configured binding
    set and `rehearsal` the backing rehearsal's exact text. With `offline` they
    are not consulted: the rehearsal and the binding-set rules are skipped, and
    the caller reports them as not checkable offline.
    """
    if not isinstance(record, Mapping) or schemas.errors(ACTIVATION_SCHEMA_ID, record):
        return records.Outcome("refuse", "activation_evidence_malformed")
    act = record["act"]
    if _missing(record):
        return records.Outcome("refuse", "activation_evidence_incomplete")
    if act == "rollback" and record["rollback"]["new_records_retained"] is not True:
        return records.Outcome("refuse", "activation_evidence_incomplete")
    if act in ACTIVATING_ACTS and not offline:
        if not _backed(record, rehearsal, registry, schemas):
            return records.Outcome("refuse", "activation_evidence_incomplete")
        configured = {binding["binding_id"]: binding for binding in bindings}
        if set(configured) - set(record["binding_refs"]):
            return records.Outcome("refuse", "activation_evidence_incomplete")
        for ref in record["binding_refs"]:
            if ref not in configured:
                return records.Outcome("refuse", "binding_unresolved")
            broker = configured[ref]["broker"]
            if broker.get("capability_verified") is not True or broker.get("evidence_ref") is None:
                return records.Outcome("refuse", "broker_capability_insufficient")
    if "producer" in record and any(
            record["producer"]["selection"][m] != record["consumer"]["selection"][m]
            for m in MATCHED):
        return records.Outcome("refuse", "pair_mismatched")
    if act == "rollback" and record["rollback"]["new_records_protocol"] != registry.replacement_id:
        return records.Outcome("refuse", "historical_reinterpretation_refused")
    return records.Outcome("accept")


def _binding_problem(binding: Any, schemas: records.SchemaSet) -> bool:
    """Whether `binding` is not a live producer binding as far as the activation
    order reads one: its kind, its `binding_id` and its `broker` member, and no
    `.template.yaml` stub marker. The binding's other members are judged at the
    `binding`, `admission` and `registration` boundaries (E10)."""
    if not isinstance(binding, dict) or binding.get("kind") != BINDING_KIND:
        return True
    if "instantiation_stub" in binding:
        return True
    opaque = records.SHARED_DEFINITIONS_ID + "#/$defs/opaque_id"
    if schemas.errors(opaque, binding.get("binding_id")):
        return True
    broker = binding.get("broker")
    if not isinstance(broker, dict) or set(broker) != {"broker_ref", "capability_verified",
                                                        "evidence_ref"}:
        return True
    if schemas.errors(opaque, broker["broker_ref"]) or not isinstance(
            broker["capability_verified"], bool):
        return True
    return broker["evidence_ref"] is not None and bool(schemas.errors(
        opaque, broker["evidence_ref"]))


def activation_handler(vector: Mapping[str, Any], context: Any) -> records.Outcome:
    """The corpus handler for `activation`."""
    from . import corpus

    inputs = vector["inputs"]
    record = corpus.join_parts(inputs.get("record")) if isinstance(inputs, dict) else None
    act = record.get("act") if isinstance(record, dict) else None
    activating = isinstance(act, str) and act in ACTIVATING_ACTS
    members = ("record", "bindings", "rehearsal") if activating else ("record",)
    corpus._closed_inputs(inputs, members)
    if not activating:
        return activation(record, context.registry, context.schemas)
    bindings = corpus.join_parts(inputs["bindings"])
    if not isinstance(bindings, list) or not bindings:
        raise corpus.VectorInputError("inputs.bindings is not a non-empty list of bindings")
    for binding in bindings:
        if _binding_problem(binding, context.schemas):
            raise corpus.VectorInputError("inputs.bindings holds a value that is not a live "
                                          "producer binding")
    ids = [binding["binding_id"] for binding in bindings]
    if len(set(ids)) != len(ids):
        raise corpus.VectorInputError("inputs.bindings repeats a binding_id")
    rehearsal = inputs["rehearsal"]
    if not isinstance(rehearsal, str):
        raise corpus.VectorInputError("inputs.rehearsal is not a string")
    return activation(record, context.registry, context.schemas, bindings, rehearsal)


# --------------------------------------------------------------------------
# Historical classification.
# --------------------------------------------------------------------------

def historical(record: Any, registry: classification.Registry) -> records.Outcome:
    """Classify by the recorded protocol, at any status, and never reinterpret."""
    try:
        kind = classification.classify(record, registry)
    except records.Refused as refused:
        return records.Outcome("refuse", refused.code)
    if kind == "legacy":
        return records.Outcome("route", None, (classification.ROUTE_FINDING,),
                               {"classification": "legacy"})
    return records.Outcome("accept", derived={"classification": "replacement"})


def historical_handler(vector: Mapping[str, Any], context: Any) -> records.Outcome:
    """The corpus handler for `historical`."""
    from . import corpus

    inputs = corpus._closed_inputs(vector["inputs"], ("record",))
    record = corpus.join_parts(inputs["record"])
    if not isinstance(record, dict):
        raise corpus.VectorInputError("inputs.record is not an object")
    if record.get("kind") in classification.JUDGED_BY_KIND_KINDS:
        raise corpus.VectorInputError(
            "inputs.record is a kind judged by kind, which is never classified")
    corpus._statuses(vector.get("environment", {}), context)  # validated; never read
    return historical(record, context.registry)



#: The oracles each boundary's vectors may carry.
SELECTION_ORACLES = ("registry_status",)
ACTIVATION_ORACLES: tuple[str, ...] = ()
HISTORICAL_ORACLES = ("registry_status",)
