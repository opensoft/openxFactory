"""THE TWELVE ANCHORING LEAF KINDS, ADJUDICATED AGAINST THE SHIPPED SHAPE.

`add-chain-anchoring` tasks.md 5.3 settles twelve new leaf kinds INSIDE tranche
one's ratified leaf grammar, on its own ground: *"This packet adds no second
grammar and must not, so tranche one's grammar is where each event discriminator
and its required fields are settled."* What that settlement buys is only as good
as what the SHAPE refuses, and this module is where that is measured rather than
asserted — every case here validates a whole leaf record against
`transparency-log-leaf.schema.yaml` with a stock `Draft202012Validator`, so what
passes here passes in a consumer's validator too.

THE THREE COMMISSIONED MUTATION PROOFS are `test_an_anchoring_leaf_carrying_a_
verdict_is_refused`, `test_a_gate_verdict_leaf_carrying_an_anchor_event_is_
refused` and `test_a_horizon_breach_missing_its_witness_id_is_refused`. The rest
are the same measurement widened: one healthy record per kind (so a refusal is
never mistaken for a shape nothing can satisfy), the event/leaf-type disagreement
that the `allOf` makes UNREPRESENTABLE, and the fields each kind's requirement
mandates.

THE CONTROL IS THE POINT. Each refusal test asserts a HEALTHY sibling of the same
record validates, so a test that would pass against a schema refusing everything
is not counted as evidence.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONTRACTS = REPO_ROOT / "contracts" / "signed-execution-chain"
LEAF_SCHEMA_PATH = CONTRACTS / "transparency-log-leaf.schema.yaml"
DIGEST_SCHEMA_PATH = CONTRACTS / "digest-construction.schema.yaml"

# Synthetic throughout. No real chain, no real key, no real identifier.
SYNTHETIC_DIGEST = "sha256:" + "ab" * 32
SYNTHETIC_SIGNATURE = "A" * 86


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    """The leaf schema resolved against the digest construction it `$ref`s, the
    same way the reader and a consumer's stock validator both resolve it."""
    resources: list[tuple[str, Resource]] = []
    for path in (DIGEST_SCHEMA_PATH, LEAF_SCHEMA_PATH):
        doc = _load(path)
        resource = Resource.from_contents(doc, default_specification=DRAFT202012)
        resources.append((path.name, resource))
        resources.append((doc["$id"], resource))
    registry = Registry().with_resources(resources)
    return Draft202012Validator(_load(LEAF_SCHEMA_PATH), registry=registry)


def errors_of(validator: Draft202012Validator, doc: dict) -> list[str]:
    return [err.message for err in validator.iter_errors(doc)]


def leaf(leaf_type: str, **extra) -> dict:
    """A structurally complete leaf of the given type.

    The digests are synthetic and do NOT recompute — that is the canonical
    reader's check, over a real corpus, and not the shape's. What this record
    exercises is exactly what a stock validator can decide: which members a leaf
    of this type must, may and MUST NOT carry.
    """
    record = {
        "schema_version": 1,
        "kind": "xfactory_signed_execution_chain_log_leaf",
        "leaf_id": "example:leaf/0001",
        "leaf_index": 7,
        "tree_size": 8,
        "chain_ref": SYNTHETIC_DIGEST,
        "leaf_type": leaf_type,
        "recorded_at": "2026-08-31T00:00:00Z",
        "payload_ref": "example:payload/0001",
        "payload_digest": {
            "construction": "xfc-jcs-sha256-1",
            "subject": "anchor_event",
            "value": SYNTHETIC_DIGEST,
        },
        "leaf_digest": {
            "construction": "xfc-jcs-sha256-1",
            "subject": "transparency_log_leaf",
            "value": SYNTHETIC_DIGEST,
        },
        "leaf_signature": {
            "algorithm": "ed25519",
            "key_ref": "example:key/0001",
            "signed_over": "leaf_content",
            "signature": SYNTHETIC_SIGNATURE,
        },
    }
    record.update(extra)
    return record


# The one healthy `anchor_event` block per settled kind, carrying exactly the
# fields tasks.md 5.3 settles for it and nothing else.
HEALTHY_EVENTS: dict[str, dict] = {
    "anchor_pending_entry": {
        "event": "anchor_pending_entry",
        "item_ref": "example:item/0001",
        "configured_witnesses": ["example:witness/operational",
                                 "example:witness/durability"],
        "submission_time": "2026-08-31T00:00:00Z",
    },
    "horizon_breach": {
        "event": "horizon_breach",
        "item_ref": "example:item/0001",
        "witness_id": "example:witness/durability",
        "horizon_seconds": 86400,
        "horizon_base": {"kind": "chain_derived",
                         "value": "2026-08-31T00:00:00Z"},
    },
    "terminal_witness_failure": {
        "event": "terminal_witness_failure",
        "item_ref": "example:item/0001",
        "witness_id": "example:witness/operational",
        "failure_ground": "target_withdrawn",
    },
    "anchor_completion": {
        "event": "anchor_completion",
        "item_ref": "example:item/0001",
        "receipt_ref": "example:receipt/0001",
        "witnesses_landed": ["example:witness/operational",
                             "example:witness/durability"],
    },
    "item_anchor_refusal": {
        "event": "item_anchor_refusal",
        "material_ref": "example:material/0001",
        "ground": "the material has not passed its governing gate",
    },
    "correction_anchored_forward": {
        "event": "correction_anchored_forward",
        "superseded_material_ref": "example:material/0001",
        "correcting_material_ref": "example:material/0002",
        "ground": "the anchored material was found wrong and is corrected forward",
    },
    "verification": {
        "event": "verification",
        "subject_ref": "example:item/0001",
        "outcome": "anchor_complete",
        "verification_mode": "stateful",
    },
    "verification_failure": {
        "event": "verification_failure",
        "subject_ref": "example:item/0001",
        "outcome": "failed",
        "verification_mode": "receipt_only",
    },
    "permitted_access": {
        "event": "permitted_access",
        "served_party_ref": "example:party/0001",
        "reached_ref": "example:item/0001",
    },
    "refused_access": {
        "event": "refused_access",
        "requesting_party_ref": "example:party/0002",
        "ground": "the requesting party holds no current authorization",
    },
    "linkage_derivation_issuance": {
        "event": "linkage_derivation_issuance",
        "derivation_ref": "example:derivation/0001",
        "issuing_plane": "identity",
        "consent_checkpoint_ref": "example:checkpoint/0001",
        "analysis_ref": "example:analysis/0001",
    },
    "linkage_derivation_use": {
        "event": "linkage_derivation_use",
        "derivation_ref": "example:derivation/0001",
        "analysis_ref": "example:analysis/0001",
        "revocation_state_read": "current_not_revoked",
    },
}

TRANCHE_ONE_TYPES = ("wallet_presented_ratification", "chain_inception",
                     "traveling_contract_issued", "gate_verdict")

# Tranche two's seven (`add-chain-attestation`), which landed on `main` while this
# settlement was being authored. They sit BETWEEN tranche one's four and this
# packet's twelve in the shipped enumeration, so the slices below name all three
# groups by position rather than assuming the twelve start at index four.
TRANCHE_TWO_TYPES = ("setup_attestation", "commitment_extension",
                     "signed_chain_binding", "runner_attestation",
                     "pr_open_decision", "closure_record",
                     "remediation_declaration")

TRANCHE_TWO_SUBJECTS = ("setup_attestation", "commitment_extension",
                        "signed_chain_binding", "runner_attestation",
                        "signing_request", "pr_open_decision", "closure_record",
                        "remediation_declaration", "reviewed_subject",
                        "review_record", "governed_test_definition")

# A minimally complete gate verdict, so the tranche-one control is a record the
# shape actually accepts rather than one refused for an unrelated reason.
CHECK_NAMES = (
    "ratification_signature_verifies",
    "chain_identity_recomputes",
    "exercise_object_ref_is_content_digest",
    "inception_leaf_commits_to_chain_identity",
    "traveling_contract_carries_established_values",
    "actor_bound_to_signing_wallet",
    "proof_of_possession_supplied_and_verified",
    "standing_and_holder_class_at_exercise",
)
HEALTHY_VERDICT = {
    "outcome": "permitted",
    "scope": "links_1_3",
    "checks": [{"check": name, "outcome": "pass"} for name in CHECK_NAMES],
}


def anchoring_leaf(leaf_type: str) -> dict:
    record = leaf(leaf_type)
    record["anchor_event"] = copy.deepcopy(HEALTHY_EVENTS[leaf_type])
    return record


def gate_verdict_leaf() -> dict:
    record = leaf("gate_verdict")
    record["payload_digest"]["subject"] = "gate_verdict"
    record["verdict"] = copy.deepcopy(HEALTHY_VERDICT)
    return record


# --------------------------------------------------------------------------
# The controls. A refusal below is evidence only if the healthy record passes.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("leaf_type", sorted(HEALTHY_EVENTS))
def test_a_healthy_leaf_of_every_settled_kind_validates(validator, leaf_type):
    assert errors_of(validator, anchoring_leaf(leaf_type)) == []


def test_a_healthy_gate_verdict_leaf_validates(validator):
    assert errors_of(validator, gate_verdict_leaf()) == []


def test_the_settled_kinds_are_exactly_the_twelve_the_shape_enumerates(validator):
    """The settlement is TWELVE plus ONE DELIBERATE EXCLUSION, and the exclusion
    is checked here as an absence with a name.

    Requirement 4 of `add-chain-anchoring` also mandates a leaf for a VALIDATION
    FAILURE. No thirteenth member exists for it, because a validation failure is
    a GATE VERDICT that tranche one's ratified set already carries; settling it
    again would mint the second grammar 5.3 forbids. A member named for it
    appearing in this enumeration is that mistake, and this assertion is what
    would catch it.
    """
    declared = _load(LEAF_SCHEMA_PATH)["properties"]["leaf_type"]["enum"]
    assert declared[:4] == list(TRANCHE_ONE_TYPES)
    assert declared[4:11] == list(TRANCHE_TWO_TYPES)
    assert declared[11:] == [
        "anchor_pending_entry", "horizon_breach", "terminal_witness_failure",
        "anchor_completion", "item_anchor_refusal",
        "correction_anchored_forward", "verification", "verification_failure",
        "permitted_access", "refused_access", "linkage_derivation_issuance",
        "linkage_derivation_use",
    ]
    assert set(declared[11:]) == set(HEALTHY_EVENTS)
    assert not any("validation_failure" in name for name in declared), (
        "requirement 4's validation-failure leaf is a gate verdict and is "
        "DELIBERATELY excluded; a member for it is the second grammar 5.3 "
        "forbids")


# --------------------------------------------------------------------------
# MUTATION PROOF 1 — an anchoring leaf carrying a `verdict` is refused.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("leaf_type", sorted(HEALTHY_EVENTS))
def test_an_anchoring_leaf_carrying_a_verdict_is_refused(validator, leaf_type):
    """A verdict belongs to a gate leaf and to nothing else.

    Tranche one left this pairing to the canonical validator; for the twelve the
    SHAPE refuses it, which is this family's own stated preference — *"where a
    shape can refuse a thing, the shape refuses it"* — and it holds wherever the
    schema is read, not only where the reader runs.
    """
    healthy = anchoring_leaf(leaf_type)
    assert errors_of(validator, healthy) == []

    mutated = copy.deepcopy(healthy)
    mutated["verdict"] = copy.deepcopy(HEALTHY_VERDICT)
    assert errors_of(validator, mutated) != [], (
        f"a {leaf_type} leaf carrying a gate verdict must be refused by the "
        f"shape")


# --------------------------------------------------------------------------
# MUTATION PROOF 2 — a `gate_verdict` leaf carrying an `anchor_event` is refused.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("leaf_type", sorted(TRANCHE_ONE_TYPES))
def test_a_tranche_one_leaf_carrying_an_anchor_event_is_refused(validator,
                                                                leaf_type):
    """The four acts of THIS capability are complete as they were ratified.

    A tranche-one leaf that grew an anchoring block would be a tranche-one record
    making a tranche-three claim, and the shape refuses it for all four types —
    `gate_verdict` among them, which is the commissioned case.
    """
    healthy = gate_verdict_leaf() if leaf_type == "gate_verdict" else leaf(
        leaf_type, payload_digest={"construction": "xfc-jcs-sha256-1",
                                   "subject": "ratified_subject",
                                   "value": SYNTHETIC_DIGEST})
    assert errors_of(validator, healthy) == []

    mutated = copy.deepcopy(healthy)
    mutated["anchor_event"] = copy.deepcopy(HEALTHY_EVENTS["anchor_completion"])
    assert errors_of(validator, mutated) != [], (
        f"a {leaf_type} leaf carrying an anchor_event must be refused by the "
        f"shape")


# --------------------------------------------------------------------------
# MUTATION PROOF 3 — a `horizon_breach` whose event omits `witness_id`.
# --------------------------------------------------------------------------

def test_a_horizon_breach_missing_its_witness_id_is_refused(validator):
    """Requirement 3 has exactly two transitions out of `anchor_pending`, and a
    horizon breach *"is written as a leaf"* NAMING THAT WITNESS. A breach leaf
    that names no witness records that something went wrong and not what, which
    is the half of the state machine 5.3 says a realization will otherwise omit.
    """
    healthy = anchoring_leaf("horizon_breach")
    assert errors_of(validator, healthy) == []

    mutated = copy.deepcopy(healthy)
    del mutated["anchor_event"]["witness_id"]
    messages = errors_of(validator, mutated)
    assert messages != []
    assert any("witness_id" in message for message in messages), messages


@pytest.mark.parametrize("leaf_type,field", sorted(
    (leaf_type, field)
    for leaf_type, event in HEALTHY_EVENTS.items()
    for field in event if field != "event"))
def test_every_settled_field_is_required_by_the_shape(validator, leaf_type,
                                                      field):
    """5.3 settles the required fields, and a field settled but not REQUIRED is a
    settlement a realization can decline to honour."""
    mutated = anchoring_leaf(leaf_type)
    del mutated["anchor_event"][field]
    messages = errors_of(validator, mutated)
    assert messages != [], f"{leaf_type}.{field} must be required"
    assert any(field in message for message in messages), messages


# --------------------------------------------------------------------------
# The event discriminator and the leaf type cannot disagree.
# --------------------------------------------------------------------------

def test_an_event_block_from_another_kind_is_unrepresentable(validator):
    """5.3 asked that a validator assert `anchor_event.event == leaf_type`. The
    `allOf` routes by `leaf_type` to a shape whose `event` is a `const`, so the
    disagreement is refused by the SHAPE and never reaches a reader — the
    stronger discharge of the same obligation.
    """
    mutated = leaf("horizon_breach")
    mutated["anchor_event"] = copy.deepcopy(HEALTHY_EVENTS["anchor_completion"])
    assert errors_of(validator, mutated) != []


def test_an_anchor_event_with_an_unknown_member_is_refused(validator):
    """Every per-kind shape closes itself, which is where requirement 7's
    boundary is kept: there is no member into which material could be placed.
    """
    mutated = anchoring_leaf("permitted_access")
    mutated["anchor_event"]["disclosed_material"] = "content that must never be here"
    assert errors_of(validator, mutated) != []


def test_a_correction_cannot_claim_the_original_anchor_is_withdrawn(validator):
    """Requirement 4: *"no claim is made that the original anchor is withdrawn,
    because nothing on a chain can be un-published."* The shape keeps that
    promise by leaving no member in which the claim could be written.
    """
    for claim in ("withdrawn", "retracted", "void", "erased"):
        mutated = anchoring_leaf("correction_anchored_forward")
        mutated["anchor_event"][claim] = True
        assert errors_of(validator, mutated) != [], claim


def test_a_verification_leaf_cannot_report_failed_and_a_failure_cannot_report_a_state(
        validator):
    """The two verification kinds are decidable apart BY THE RECORD, so a failure
    cannot be filed as a success wearing a softer outcome.
    """
    verification = anchoring_leaf("verification")
    verification["anchor_event"]["outcome"] = "failed"
    assert errors_of(validator, verification) != []

    failure = anchoring_leaf("verification_failure")
    failure["anchor_event"]["outcome"] = "anchor_complete"
    assert errors_of(validator, failure) != []


def test_a_verification_leaf_offered_without_a_mode_is_refused(validator):
    """Requirement 3: *"Every verification result SHALL carry its VERIFICATION
    MODE, and a result offered without one is REFUSED"* — because a caller
    branches on a value and never on a paragraph.
    """
    for leaf_type in ("verification", "verification_failure"):
        mutated = anchoring_leaf(leaf_type)
        del mutated["anchor_event"]["verification_mode"]
        assert errors_of(validator, mutated) != [], leaf_type


def test_the_wrong_values_stay_representable_so_a_negative_can_exist(validator):
    """THIS FAMILY'S STANDING RULE, measured rather than restated: a restriction
    on a value a record DECLARES is refused BY NAME by the reader that owns the
    rule, not made unrepresentable by the shape — because a value a record cannot
    state is a refusal no negative example can ever probe.

    So a horizon base of `minter_claimed`, a linkage derivation issued by the
    `record` plane, and a use recorded against an `unreadable` revocation state
    are all SCHEMA-VALID here. Each is refused by name in the chain-anchoring
    family; none is refused here, and that is the design working.
    """
    breach = anchoring_leaf("horizon_breach")
    breach["anchor_event"]["horizon_base"] = {"kind": "minter_claimed"}
    assert errors_of(validator, breach) == []

    issuance = anchoring_leaf("linkage_derivation_issuance")
    issuance["anchor_event"]["issuing_plane"] = "record"
    assert errors_of(validator, issuance) == []

    use = anchoring_leaf("linkage_derivation_use")
    use["anchor_event"]["revocation_state_read"] = "unreadable"
    assert errors_of(validator, use) == []


# --------------------------------------------------------------------------
# The digest-construction enumeration moved with the grammar.
# --------------------------------------------------------------------------

def test_the_eleven_anchoring_digest_subjects_are_enumerated_once():
    """`digest-construction.schema.yaml` invites exactly this: *"Any digest a
    later tranche introduces is computed under this construction, with its
    subject added to the enumeration below."* Eleven were added, in one place,
    under the one construction — no second construction name exists.

    UPDATED BY THE CATCH-UP MERGE TO MAIN (contract-v3.3): `add-cpc-clearing-
    boundary` landed on main while this branch carried the eleven above, and
    widened the SAME enumeration by one further subject
    (`sealed_bundle_manifest`), under the same construction, per this file's
    own tranche-widening invitation. The count pin below moves from 27 to 28
    to match — a union of subjects, never a second construction.
    """
    doc = _load(DIGEST_SCHEMA_PATH)
    subjects = doc["$defs"]["digest_subject"]["enum"]
    assert subjects[:5] == ["ratified_subject", "signed_ratification",
                            "transparency_log_leaf", "traveling_contract",
                            "gate_verdict"]
    assert subjects[5:16] == list(TRANCHE_TWO_SUBJECTS)
    assert subjects[16:27] == [
        "anchor_material", "anchored_commitment", "anchor_receipt",
        "anchor_state", "anchor_bound_commitment", "consent_checkpoint",
        "log_checkpoint", "linkage_derivation", "analysis_result",
        "verification_result", "anchor_event",
    ]
    assert subjects[27:] == ["sealed_bundle_manifest"]
    assert len(subjects) == len(set(subjects)) == 28
    assert doc["$defs"]["construction_name"]["const"] == "xfc-jcs-sha256-1"


def test_an_anchoring_leaf_commits_over_its_event_block(validator):
    """`payload_digest.subject` for the twelve is `anchor_event` — one new
    subject, not twelve. A leaf naming another subject is refused by the reader
    by name; the shape's part is that the subject is a member of the ONE closed
    enumeration, so a subject nobody declared cannot be written at all.
    """
    mutated = anchoring_leaf("anchor_completion")
    mutated["payload_digest"]["subject"] = "anchor_receipt_but_invented"
    assert errors_of(validator, mutated) != []
