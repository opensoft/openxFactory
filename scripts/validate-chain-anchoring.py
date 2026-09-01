#!/usr/bin/env python3
"""Validate the chain-anchoring contract family, and ADJUDICATE ITS RECORDS.

The openxFactory-owned canonical validator for the eleven kinds
`xfactory_chain_anchoring_receipt`, `xfactory_chain_anchoring_anchor_state`,
`xfactory_chain_anchoring_verification_result`,
`xfactory_chain_anchoring_anchor_bound_commitment`,
`xfactory_chain_anchoring_log_checkpoint_anchor`,
`xfactory_chain_anchoring_consent_checkpoint_commitment`,
`xfactory_chain_anchoring_plane_separation_declaration`,
`xfactory_chain_anchoring_linkage_derivation_issuance`,
`xfactory_chain_anchoring_linkage_derivation_use`,
`xfactory_chain_anchoring_analysis_result` and
`xfactory_chain_anchoring_conformance_declaration`
(`contracts/chain-anchoring/*.schema.yaml`). Run from the pinned openxFactory
checkout, never copied into a domain repo:

    python3 scripts/validate-chain-anchoring.py [REPO_PATH] [--strict]

THIS FILE IS THE NAMED READER. The capability's fifth requirement is that the
on-chain boundary is CONTRACT TEXT CARRYING A REFUSING VALIDATOR — prose about
where content may not go erodes, and a refusal holds — so this validator is not a
description of a control, it IS the control. IN THIS REPOSITORY IT IS NOT YET A
REQUIRED CHECK, and the packaged conformance declaration says so in the present
tense: until the reader runs as a required check on the repository holding these
records, every record this family defines confers and refuses nothing. A
declaration recording the reader unrequired earns the standing `reader-not-required`
warning on every run, and may not record its self-referential obligation satisfied.

Two layers run:

1. Packaged reference corpus (`contracts/chain-anchoring/examples/`): every
   `*.example.yaml` must pass schema conformance AND every semantic rule below;
   every file under `negative/` must FAIL for its INTENDED reason, declared in its
   own `# expected_failure:` header and pinned further by an
   `# expected_failure_detail:` substring, because a finding CODE alone is too
   coarse an anchor for a rule more than one fixture can provoke. THE NEGATIVES
   ARE EVALUATED IN THE POSITIVE CORPUS'S SCOPE, with the fixture added to it: a
   refusal here is frequently a property of a SET of records — a derivation reused
   under a second analysis, a receipt entry written for a witness another record
   says is still in flight, a key custody reference appearing under two planes —
   and a fixture adjudicated alone could not express one. A negative that draws
   further findings beyond the one it is named for is the rules working; the
   expected code and detail are what the self-test pins.
2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose top-level `kind`
   is one of the eleven family kinds is validated as one scope. Other kinds are
   skipped and counted; the packaged `examples/` tree is excluded, because the
   negatives there are deliberately invalid and layer 1 already asserts exactly
   how. ZERO REAL ARTIFACTS IS THE EXPECTED STATE UNTIL AN ANCHORING SUBSYSTEM
   RUNS — this realization anchors nothing, reaches no chain, and mints no receipt.

THE ORDERED CHECKS, each one reported under a CLOSED refusal code except where
noted, and each traceable to a scenario of the ratified delta:

  1. SHAPES — the library's job, against the shipped schemas, with `date-time`
     format checking enforced rather than annotated.
  2. THE RECEIPT'S ANCHORED DIGEST, RECOMPUTED over the two-member subject
     `{material_digest, mint_time_configuration}` under the one construction in
     force. A digest taken over the material ALONE is the configured set carried
     beside the proof rather than committed by it
     (`receipt_configuration_not_committed`); a digest matching neither is a block
     a holder has edited (`receipt_configuration_block_edited`). This is what
     makes a rewritten witness set or an extended horizon break the proofs.
  3. THE FOUR PER-CHAIN ELEMENTS, each refused BY NAME when absent, plus the
     CANONICALITY step the first three stop short of: a header absent from the
     linkage that would place it on the chain is refused
     (`receipt_header_not_canonical`), and a capture the SIZE OF A REFERENCE is a
     transaction deferred to verification time
     (`receipt_transaction_deferred_to_verification`).
  4. THE CLOSURE RULE — every value a receipt-only computation reads lives inside
     the committed block, so a member of that vocabulary found anywhere else on a
     receipt is refused by the RULE and not by an enumeration chase
     (`receipt_only_input_outside_committed_block`). The receipt holds proof
     material and never state, so a member of the state vocabulary found on one is
     refused by name (`receipt_carries_anchor_state`).
  5. THE TIMING MODEL, IN ITS DECLARED DIRECTION. A declared submission LATER than
     the earliest chain-accepted time by MORE than that chain's declared skew is
     provably false (`receipt_submission_after_earliest_chain_time`); WITHIN the
     skew it is ACCEPTED, and refusing it there is itself refused
     (`honest_receipt_refused_within_skew`). A receipt whose earliest chain time
     exceeds its declared submission by more than the declared maximum delay plus
     the declared tolerance documents its own breach
     (`receipt_self_inconsistent_delay`).
  6. THE WITNESS SHORTFALL ARITHMETIC — `missing` is exactly `configured` minus
     `present`, and a set of three lists that does not reconcile is refused rather
     than read as a partial answer (`witness_shortfall_miscomputed`).
  7. THE DISJOINT STATE MACHINE — three states, no aggregate boolean anywhere
     (`anchor_state_aggregate_boolean`), every transition carrying its leaf
     (`anchor_state_transition_without_leaf`), completion resting on a captured
     receipt with every configured witness landed
     (`anchor_state_complete_without_captured_receipt`), and pending never
     coexisting with a terminal failure (`anchor_state_pending_and_incomplete`).
  8. THE MODE DISCRIMINATORS — a verification result carries its mode or is
     refused (`verification_mode_absent`); a `receipt_only` result may not claim
     knowledge only the state record holds
     (`verification_result_claims_stateful_knowledge`); a determination reached on
     a minter-claimed base is refused
     (`determination_made_with_minter_claimed_base`); and NO MODE MAY CONCLUDE
     DELAY COMPLIANCE (`delay_check_read_as_compliance`).
  9. THE STRUCTURAL PAYLOAD SWEEP — any content-bearing member, at any depth, by
     THE SHAPE OF THE MEMBER and never by recognizing what the content is about.
     A validator that refused one domain's protected content by name would need
     that domain's semantics, which this capability is forbidden to carry; a
     validator that refuses EVERY payload needs none, and is stricter, because raw
     content, ENCRYPTED content and PLAIN-HASHED content are all outside the
     boundary and one structural refusal reaches all three
     (`payload_bearing_field`).
 10. THE COMMITMENT DECLARATION — construction declared
     (`commitment_construction_absent`), keyed AND salted
     (`commitment_not_keyed_and_salted`), both custody references resolving into
     the governed layer and nowhere the anchor can reach
     (`salt_custody_reference_reachable_from_anchor`,
     `key_custody_reference_reachable_from_anchor`), the salt's source and width
     declared (`salt_entropy_declaration_absent`), and the width AT OR ABOVE 128
     BITS, refused by name with the requirement's own ground rather than by a
     schema range error (`salt_width_below_floor`).
 11. THE PLANE SEPARATION — one commitment key under two planes is a join key
     whatever the salts do (`commitment_key_shared_across_planes`), a shared
     stable key or shared record digest is the refused key under another name
     (`cross_plane_join_key_shared`), and no anchored value serves as a join key
     (`anchored_commitment_used_as_join_key`).
 12. THE AUTHORIZED LINKAGE PATH — issued by the identity plane, under an anchored
     consent checkpoint, per-analysis and never stable, expiring and revocable,
     and used only against a revocation state that could actually be read.
 13. THE CLOSED DISCRIMINATORS — the analysis result's status, its refusal ground,
     and the de-identification hook that is a HOOK AND NEVER A STANDARD.
 14. THE CONFORMANCE DECLARATION — closed over the capability's nine obligations
     in BOTH directions (`obligation_not_declared`), with the structural residual
     `CA-R5-COMMITMENT-PATH` refused the word `satisfied`
     (`structural_residual_declared_satisfied`), and every realization POSTURE
     member adjudicated against its named refusal.

FOUR FINDINGS CARRY KEBAB-CASE CODES because the closed enumeration has no member
for them and inventing one would be a contract change made by a reader:
`ordering-only-correspondence` (a null header time under a time-bearing rule, or a
time under an ordering-only rule — the same defect pointing opposite ways),
`delay-check-arithmetic` (a bracket that is not a bracket, or a bound that is not
the difference it claims), `checkpoint-anchor-mismatch` (a checkpoint anchor
committing to a digest its own receipt does not carry) and `record-digest-mismatch`
(a record digest that does not recompute). Each has a packaged negative, on the
same rule as the closed codes.

WHAT THIS VALIDATOR DOES NOT DO, stated at its real strength:

  * IT CANNOT VERIFY A REAL CHAIN ANCHOR. It reaches no network, holds no key,
    parses no transaction and evaluates no consensus rule. It reads what a receipt
    DECLARES about its anchors and checks the declarations against each other; it
    never establishes that the transaction was mined, that the header is on any
    chain, or that the anchor exists at all.
  * IT CANNOT FETCH A CANONICAL HEADER SET. Canonicality is exactly the step the
    fourth per-chain element exists for, and the check here is STRUCTURAL — that
    the entry's own header is named by the linkage or acceptance path it offers.
    A self-consistent fabrication passes that check, which is why the trust root
    is a public chain THE VERIFIER OBTAINS FOR ITSELF and why a minter-supplied
    header source is refused outright.
  * IT CANNOT TELL A DECLARED SALTED KEYED COMMITMENT FROM A PLAIN DIGEST BY
    INSPECTION. Both are opaque values of the same width. This is requirement 5's
    OWN DECLARED RESIDUAL (`CA-R5-COMMITMENT-PATH`): the declaration and the
    custody references are enforceable today, and the step from "the record
    DECLARES a salted keyed commitment" to "the anchored value IS one" rests on
    the realization establishing that this path is the ONLY path that can mint an
    anchor-bound value. A declaration recording that residual `satisfied` is
    refused rather than believed.
  * IT ADJUDICATES RECORDS AND NOT A RUNNING ANCHORING SUBSYSTEM. Cadence,
    retention, capture-at-anchor-time and the durability calendar are read from
    what a realization DECLARES about itself. A declaration is not an observation.
  * IT MINTS NOTHING. No receipt, no commitment, no leaf, no anchor.

THE OPERATOR GATES THAT REMAIN OPEN, named so their absence is decided rather than
overlooked: the operational witness's ARCHIVAL NODE (tasks 4.5), INCLUSION-PROOF
CAPTURE AT ANCHOR TIME (4.6), INCLUSION-PROOF RETENTION proved against a pruned
chain (4.7), the durability witness's AGGREGATION PATH proved by a completed
upgrade on a real item (4.9), and the END-TO-END exercise of the both-witnesses
rule including its degraded paths (4.10). None of them is evidenced by a record
this reader can see, and none of them is claimed by the packaged declaration.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import base64
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# THE ONE DIGEST CONSTRUCTION, TAKEN FROM THE FAMILY THAT DECLARES IT. There is no
# second construction and this file writes none: `xfc-jcs-sha256-1` is
# `signed-execution-chain`'s, and this tranche added SUBJECTS to its enumeration
# rather than a rule beside it.
from scripts.signed_execution_chain import canonical  # noqa: E402

CONTRACT_DIR = ROOT / "contracts" / "chain-anchoring"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
SIBLING_DIR = ROOT / "contracts" / "signed-execution-chain"

SCHEMA_FILENAMES = [
    "anchoring-definitions.schema.yaml",
    "anchor-receipt.schema.yaml",
    "anchor-state.schema.yaml",
    "verification-result.schema.yaml",
    "anchor-bound-commitment.schema.yaml",
    "log-checkpoint-anchor.schema.yaml",
    "consent-checkpoint-commitment.schema.yaml",
    "plane-separation-declaration.schema.yaml",
    "linkage-derivation-issuance.schema.yaml",
    "linkage-derivation-use.schema.yaml",
    "analysis-result.schema.yaml",
    "conformance-declaration.schema.yaml",
]

# The sibling schema every file here `$ref`s for `identifier` and `digest`. It is
# LOADED INTO THE REGISTRY and never restated: a second copy of a shape this
# family consumes is the drift the reference exists to prevent.
SIBLING_SCHEMA_FILENAMES = ["digest-construction.schema.yaml"]

KIND_TO_SCHEMA = {
    "xfactory_chain_anchoring_receipt": "anchor-receipt.schema.yaml",
    "xfactory_chain_anchoring_anchor_state": "anchor-state.schema.yaml",
    "xfactory_chain_anchoring_verification_result": "verification-result.schema.yaml",
    "xfactory_chain_anchoring_anchor_bound_commitment":
        "anchor-bound-commitment.schema.yaml",
    "xfactory_chain_anchoring_log_checkpoint_anchor": "log-checkpoint-anchor.schema.yaml",
    "xfactory_chain_anchoring_consent_checkpoint_commitment":
        "consent-checkpoint-commitment.schema.yaml",
    "xfactory_chain_anchoring_plane_separation_declaration":
        "plane-separation-declaration.schema.yaml",
    "xfactory_chain_anchoring_linkage_derivation_issuance":
        "linkage-derivation-issuance.schema.yaml",
    "xfactory_chain_anchoring_linkage_derivation_use":
        "linkage-derivation-use.schema.yaml",
    "xfactory_chain_anchoring_analysis_result": "analysis-result.schema.yaml",
    "xfactory_chain_anchoring_conformance_declaration":
        "conformance-declaration.schema.yaml",
}

# THE CLOSED REFUSAL ENUMERATION, held here as the set the packaged corpus must
# probe. It is the same enumeration the definitions file's
# `#/$defs/refusal_code` declares — and the self-test compares the two set for
# set, so a code added to one and not the other is a finding rather than a
# silence; the self-test also refuses a code with no probe, so a refusal this
# validator can emit and no fixture ever provokes cannot ship.
REFUSAL_CODES = frozenset({
    # ---- Receipt and capture time ------------------------------------------
    "receipt_missing_transaction_bytes",
    "receipt_missing_inclusion_proof",
    "receipt_missing_block_header",
    "receipt_missing_chain_acceptance_evidence",
    "receipt_header_not_canonical",
    "receipt_transaction_deferred_to_verification",
    "receipt_missing_configured_witness_set",
    "receipt_configuration_not_committed",
    "receipt_configuration_block_edited",
    "receipt_only_input_outside_committed_block",
    "receipt_submission_after_earliest_chain_time",
    "receipt_self_inconsistent_delay",
    "receipt_entry_incomplete_for_pending_witness",
    "receipt_single_chain_shape",
    "receipt_carries_anchor_state",
    # ---- Verification ------------------------------------------------------
    "verification_header_source_is_minter_supplied",
    "verification_mode_absent",
    "verification_result_claims_stateful_knowledge",
    "horizon_base_from_minter_clock",
    "determination_made_with_minter_claimed_base",
    "breach_declared_within_tolerance",
    "honest_receipt_refused_within_skew",
    "delay_check_read_as_compliance",
    "witness_shortfall_miscomputed",
    # ---- Anchor state and witnesses ----------------------------------------
    "anchor_state_aggregate_boolean",
    "anchor_state_pending_and_incomplete",
    "anchor_state_transition_without_leaf",
    "anchor_state_complete_without_captured_receipt",
    "item_presented_as_anchored_with_missing_witness",
    "ten_year_claim_on_operational_witness",
    "claim_stands_on_operational_witness_alone",
    "witness_selectivity_rule",
    "third_anchor_target",
    "operational_anchor_without_retained_proof",
    "durability_proof_reanchored_rather_than_upgraded",
    # ---- Boundary and commitment -------------------------------------------
    "payload_bearing_field",
    "commitment_construction_absent",
    "commitment_not_keyed_and_salted",
    "salt_custody_reference_reachable_from_anchor",
    "key_custody_reference_reachable_from_anchor",
    "commitment_key_shared_across_planes",
    "salt_entropy_declaration_absent",
    "salt_width_below_floor",
    # ---- Consent plane and checkpoints -------------------------------------
    "consent_row_offered_for_anchoring",
    "consent_enforcement_as_on_chain_contract_code",
    "revocation_presented_as_recall",
    "checkpoint_inclusion_presented_as_validation",
    "checkpoint_anchor_missing_disclaimer",
    "item_anchor_over_ungated_material",
    "attempt_row_offered_for_direct_anchoring",
    "checkpoint_cadence_not_met",
    # ---- Served audit surface ----------------------------------------------
    "served_audit_logs_refusals_only",
    "reporting_obligation_on_independent_verifiers",
    "served_verification_event_unlogged",
    # ---- Planes, linkage and analysis --------------------------------------
    "direct_identifier_in_demographic_plane",
    "cross_plane_join_key_shared",
    "anchored_commitment_used_as_join_key",
    "linkage_derivation_reused_across_analyses",
    "linkage_derivation_not_issued_by_identity_plane",
    "linkage_derivation_without_anchored_consent_checkpoint",
    "linkage_derivation_not_expiring_or_revocable",
    "linkage_use_with_unreadable_revocation_state",
    "analysis_result_status_outside_enumeration",
    "analysis_result_refusal_ground_free_text",
    "analysis_result_silently_partial",
    "analysis_result_labelled_deidentified",
    # ---- Neutrality and declaration ----------------------------------------
    "domain_record_kind_in_neutral_family",
    "overlay_relaxes_neutral_refusal",
    "structural_residual_declared_satisfied",
    "obligation_not_declared",
})

# The capability's nine obligations, in the delta's own order.
OBLIGATIONS = ["CA-R1", "CA-R2", "CA-R3", "CA-R4", "CA-R5", "CA-R6",
               "CA-R7", "CA-R8", "CA-R9"]

# THE ONE OBLIGATION WHOSE RESIDUAL IS STRUCTURAL AT THIS REALIZATION. CA-R5 is
# the step from "the record DECLARES a salted keyed commitment" to "the anchored
# value IS one", which is not detectable from the record; it may not be recorded
# `satisfied`, and the declaration's own `structural_residual` token names it.
STRUCTURAL_RESIDUAL_OBLIGATIONS = {"CA-R5"}
STRUCTURAL_RESIDUAL_TOKENS = {"CA-R5-COMMITMENT-PATH": "CA-R5"}

# THE FLOOR IS 128 BITS AND IT IS ENFORCED HERE RATHER THAN BY `minimum: 128` IN
# THE SHAPE. The ground is the reading requirement 5 cites — EDPB Guidelines
# 02/2025 — that what makes a hash of a person's attributes reach them is that the
# INPUT SPACE CAN BE SEARCHED. An eight-bit salt satisfies every other check
# written here while leaving that search trivial, so a schema range error
# reporting a number out of bounds would say nothing about the attack the floor
# exists to answer. A domain overlay MAY raise this floor and SHALL NOT lower it.
SALT_WIDTH_FLOOR_BITS = 128

# A CAPTURE THE SIZE OF A REFERENCE IS A REFERENCE. A transaction identifier is
# thirty-two bytes on every chain this family contemplates and the smallest whole
# transaction any of them admits is larger, so a capture below this floor is a
# transaction DEFERRED to verification time rather than captured at anchor time.
# The test is on SIZE and never on structure: this reader parses no transaction,
# and it says so rather than implying it checked one.
TRANSACTION_CAPTURE_FLOOR_BYTES = 64

# THE VALUES A RECEIPT-ONLY COMPUTATION READS. Every one of them lives inside the
# mint-time configuration block and is therefore committed by the anchored digest;
# a member of this vocabulary found anywhere else on a receipt is refused BY THE
# RULE rather than after an enumeration chase, which is what three separate review
# rounds adding a field outside the block earned.
RECEIPT_ONLY_INPUT_NAMES = frozenset({
    "configured_witnesses",
    "submission_time",
    "max_submission_to_first_anchor_delay_seconds",
    "checkpoint_cadence_seconds",
    "completion_horizon_seconds",
    "chain_accepted_time_rule",
    "skew_seconds",
    "tolerance_seconds",
    "ordering_only",
})

# THE STATE VOCABULARY THE RECEIPT MAY NOT CARRY. The receipt holds proof material
# and never state; a witness still in flight is recorded in the anchor-state
# record, which is where every surface reads per-witness status.
ANCHOR_STATE_VOCABULARY = frozenset({
    "anchored", "anchor_status", "pending", "complete", "state", "status",
    "anchor_state", "witness_status", "landed", "in_flight",
})

# THE AGGREGATE BOOLEAN THAT EXISTS NOWHERE IN THIS CAPABILITY. Such a field can
# read TRUE while a configured witness is missing, which is how an outage becomes
# selectivity by accident. Per-witness status is what every surface reads instead.
AGGREGATE_BOOLEAN_NAMES = frozenset({
    "anchored", "is_anchored", "fully_anchored", "anchored_flag", "anchor_ok",
    "all_witnesses_landed", "anchor_complete_flag",
})

# THE CONTENT-BEARING SHAPE LIST, WHICH IS A LIST OF NAME TOKENS AND NOT A LIST OF
# SUBJECTS. The refusal is STRUCTURAL: it fires on the SHAPE of the member and
# never on recognizing what the content is about. A validator that refused one
# domain's protected content by name would need that domain's semantics, which
# this capability is forbidden to carry; a validator that refuses EVERY payload
# needs none, and refuses the protected ones without having to detect them. Raw
# content, ENCRYPTED content and PLAIN-HASHED content are all outside the boundary
# and one structural refusal reaches all three.
PAYLOAD_NAME_TOKENS = (
    "payload", "content", "ciphertext", "cleartext", "plaintext", "blob",
    "attachment", "encrypted", "body", "document", "dataset", "row_values",
)

# Members that legitimately carry captured CHAIN artifacts, exempt from the
# length half of the payload sweep by NAME. Both are declared shapes of this
# family, bounded by the contract, and neither is a doorway for record content.
PAYLOAD_LENGTH_EXEMPT_NAMES = frozenset({
    "anchor_transaction_bytes", "header_bytes",
})

# Any string member longer than this, outside the exempt names above, is a
# payload however it is spelled. The declared prose members of this family are all
# bounded well below it by their own `maxLength`, so this bound can only be
# reached by a member the shapes do not name.
PAYLOAD_LENGTH_CEILING_BYTES = 2048

# A PUBLIC CHAIN NEVER SEES A PER-SUBJECT CONSENT ROW. A row is publicly linkable
# to a person and a checkpoint is not, which is the whole reason consent is split
# from its own anchor.
CONSENT_ROW_NAME_TOKENS = (
    "subject_id", "subject_ref", "subject_reference", "consent_row", "row_id",
    "per_subject", "data_subject", "subject_entry",
)

# A DELAY CHECK PROVES A BREACH OR IT PROVES NOTHING, so a member asserting
# compliance is refused by name rather than reported as an unexpected property —
# the refusal has to say that a LOWER bound was read as an UPPER one.
COMPLIANCE_NAME_TOKENS = (
    "compliant", "compliance", "within_bound", "delay_ok", "not_breached",
)

ANALYSIS_STATUSES = frozenset({"complete", "correlation_refused",
                               "correlation_not_requested"})
ANALYSIS_REFUSAL_GROUNDS = frozenset({"revocation_state_unreadable",
                                      "consent_revoked", "derivation_refused"})
GOVERNED_CUSTODY = "governed_layer"
ANALYZED_PLANES = ("record", "demographic")

# date/date-time enforced, not merely annotated. jsonschema registers the
# date-time checker only when rfc3339-validator is importable, so a bare
# environment would silently accept malformed timestamps — fail closed instead of
# validating vacuously.
FORMAT_CHECKER = FormatChecker()
if not {"date", "date-time"} <= set(FORMAT_CHECKER.checkers):  # pragma: no cover
    print(
        "ERROR jsonschema is missing its date/date-time format checkers; install "
        "rfc3339-validator (see requirements/hermes-runtime-contracts.in) so "
        "`format: date` and `format: date-time` are enforced",
        file=sys.stderr,
    )
    sys.exit(2)

BASE64URL_RX = re.compile(r"^[A-Za-z0-9_-]+$")


# --------------------------- findings ---------------------------

@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_records(path: Path) -> list[Any]:
    """A fixture may carry MORE THAN ONE record, `---`-separated.

    Not a convenience: several of this capability's refusals are properties of a
    SET rather than of a document — a derivation reused under a second analysis, a
    receipt entry written for a witness another record says is still in flight, a
    key custody reference appearing under two planes — and a probe for one of them
    cannot be written at all if a fixture is one record. Single-document files
    load unchanged."""
    with path.open(encoding="utf-8") as handle:
        return [doc for doc in yaml.safe_load_all(handle) if doc is not None]


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline registry over this family's twelve schemas PLUS the sibling
    `digest-construction.schema.yaml` every one of them `$ref`s, so the cross-file
    references resolve without a network. Each schema is registered under BOTH its
    absolute `$id` and its filename, so the bundle resolves identically here and
    in a consumer's stock validator."""
    resources: list[tuple[str, Resource]] = []
    docs: dict[str, dict] = {}
    for directory, names, own in ((CONTRACT_DIR, SCHEMA_FILENAMES, True),
                                  (SIBLING_DIR, SIBLING_SCHEMA_FILENAMES, False)):
        for name in names:
            doc = load_yaml(directory / name)
            if own:
                docs[name] = doc
            resource = Resource.from_contents(doc, default_specification=DRAFT202012)
            resources.append((name, resource))
            if doc.get("$id"):
                resources.append((doc["$id"], resource))
    return Registry().with_resources(resources), docs


def schema_errors(doc: Any, schema: dict, registry: Registry | None = None
                  ) -> list[str]:
    validator = Draft202012Validator(
        schema, registry=registry, format_checker=FORMAT_CHECKER) \
        if registry is not None else \
        Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    return [f"{'/'.join(str(part) for part in err.path) or '<root>'}: {err.message}"
            for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))]


# --------------------------- the scope ---------------------------

def get(doc: Any, *path: str) -> Any:
    node = doc
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def digest_value(node: Any) -> Any:
    return node.get("value") if isinstance(node, dict) else None


def walk_members(node: Any, path: str = "") -> Iterator[tuple[str, str, Any]]:
    """Every member of a record, AT ANY DEPTH, as (path, name, value).

    The structural sweeps are depth-blind on purpose: a payload nested three
    levels down is a payload, and a sweep that only read the top level would be a
    control that reads as though it covered the record."""
    if isinstance(node, dict):
        for name, value in node.items():
            here = f"{path}/{name}" if path else str(name)
            yield here, str(name), value
            yield from walk_members(value, here)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from walk_members(item, f"{path}[{index}]")


def instant(value: Any) -> datetime | None:
    """An RFC 3339 timestamp as an aware instant, or None.

    A naive value is read as UTC rather than compared against an aware one: a
    `TypeError` escaping into a timing rule would surface as a harness failure
    where a finding belongs."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def seconds_between(later: datetime, earlier: datetime) -> float:
    return (later - earlier).total_seconds()


def as_int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


@dataclass
class ReceiptFacts:
    """What one receipt establishes ABOUT ITSELF, derived once and read by every
    record that names it. Derived rather than believed: the anchor-state record
    and the verification result each carry values a holder could edit, and the
    committed block is the one they are compared against."""
    label: str
    doc: dict
    receipt_id: Any = None
    material_value: Any = None
    submission: datetime | None = None
    a_min: datetime | None = None
    a_min_skew: int = 0
    a_min_tolerance: int = 0
    d_max: int | None = None
    header_times: set[str] = field(default_factory=set)
    configured: list[Any] = field(default_factory=list)
    present: list[Any] = field(default_factory=list)
    entry_chains: set[Any] = field(default_factory=set)
    entry_witnesses: set[Any] = field(default_factory=set)
    submission_refusable: bool = False
    minter_supplied_source: bool = False
    header_source_id: Any = None


@dataclass
class Scope:
    records: list[tuple[str, dict]]
    receipts: list[tuple[str, dict]] = field(default_factory=list)
    states: list[tuple[str, dict]] = field(default_factory=list)
    verifications: list[tuple[str, dict]] = field(default_factory=list)
    commitments: list[tuple[str, dict]] = field(default_factory=list)
    checkpoints: list[tuple[str, dict]] = field(default_factory=list)
    consents: list[tuple[str, dict]] = field(default_factory=list)
    planes: list[tuple[str, dict]] = field(default_factory=list)
    issuances: list[tuple[str, dict]] = field(default_factory=list)
    uses: list[tuple[str, dict]] = field(default_factory=list)
    analyses: list[tuple[str, dict]] = field(default_factory=list)
    declarations: list[tuple[str, dict]] = field(default_factory=list)
    facts: dict[Any, ReceiptFacts] = field(default_factory=dict)


_KIND_BUCKET = {
    "xfactory_chain_anchoring_receipt": "receipts",
    "xfactory_chain_anchoring_anchor_state": "states",
    "xfactory_chain_anchoring_verification_result": "verifications",
    "xfactory_chain_anchoring_anchor_bound_commitment": "commitments",
    "xfactory_chain_anchoring_log_checkpoint_anchor": "checkpoints",
    "xfactory_chain_anchoring_consent_checkpoint_commitment": "consents",
    "xfactory_chain_anchoring_plane_separation_declaration": "planes",
    "xfactory_chain_anchoring_linkage_derivation_issuance": "issuances",
    "xfactory_chain_anchoring_linkage_derivation_use": "uses",
    "xfactory_chain_anchoring_analysis_result": "analyses",
    "xfactory_chain_anchoring_conformance_declaration": "declarations",
}


def build_scope(records: Iterable[tuple[str, dict]]) -> Scope:
    scope = Scope(records=list(records))
    for label, doc in scope.records:
        if not isinstance(doc, dict):
            continue
        bucket = _KIND_BUCKET.get(doc.get("kind"))
        if bucket is not None:
            getattr(scope, bucket).append((label, doc))
    return scope


# --------------------------- layer 0: shapes ---------------------------

def check_shapes(f: Findings, scope: Scope, registry: Registry,
                 docs: dict[str, dict]) -> None:
    for label, doc in scope.records:
        if not isinstance(doc, dict):
            f.error("schema", f"{label}: not a mapping")
            continue
        schema_name = KIND_TO_SCHEMA.get(doc.get("kind"))
        if schema_name is None:
            f.error("schema",
                    f"{label}: kind {doc.get('kind')!r} is not a chain-anchoring "
                    f"record kind")
            continue
        for err in schema_errors(doc, docs[schema_name], registry):
            f.error("schema", f"{label}: {err}")


# --------------------------- structural sweeps ---------------------------

def check_payload_sweep(f: Findings, scope: Scope) -> None:
    """THE STRUCTURAL PAYLOAD REFUSAL, over EVERY record of the family.

    The commitment record is the one whose value reaches a chain, but the sweep
    runs family-wide because every record here is either anchor-bound or feeds
    something that is — and a payload that is refused on one record kind and
    tolerated on another has a home. Name tokens catch a payload however small;
    the length ceiling catches one however named. Both fire on the SHAPE of the
    member, never on recognizing what the content is about."""
    for label, doc in scope.records:
        if not isinstance(doc, dict):
            continue
        for path, name, value in walk_members(doc):
            lowered = name.lower()
            if any(token in lowered for token in PAYLOAD_NAME_TOKENS):
                f.error("payload_bearing_field",
                        f"{label}: member {path!r} is content-bearing by the shape "
                        f"of its name. Raw content, encrypted content and "
                        f"plain-hashed content are all outside the on-chain "
                        f"boundary; this family carries digests, commitments and "
                        f"references, never the material itself — and ciphertext "
                        f"is refused on its own ground, because a public chain is "
                        f"permanent and key management would become the only thing "
                        f"standing between a subject and irreversible disclosure")
            elif (isinstance(value, str) and name not in PAYLOAD_LENGTH_EXEMPT_NAMES
                  and len(value.encode("utf-8")) > PAYLOAD_LENGTH_CEILING_BYTES):
                f.error("payload_bearing_field",
                        f"{label}: member {path!r} holds "
                        f"{len(value.encode('utf-8'))} bytes, over the "
                        f"{PAYLOAD_LENGTH_CEILING_BYTES}-byte ceiling for any "
                        f"member this family's shapes do not name as a captured "
                        f"chain artifact — a payload is a payload however it is "
                        f"spelled")


# --------------------------- receipts ---------------------------

def _decoded_length(value: Any) -> int | None:
    if not isinstance(value, str) or not BASE64URL_RX.match(value):
        return None
    padded = value + "=" * (-len(value) % 4)
    try:
        return len(base64.urlsafe_b64decode(padded))
    except (ValueError, TypeError):
        return None


def _witness_rules(mtc: Any) -> tuple[dict[Any, dict], dict[Any, dict]]:
    """Configured witnesses indexed by witness_id and by chain_id."""
    by_witness: dict[Any, dict] = {}
    by_chain: dict[Any, dict] = {}
    for witness in (get(mtc, "configured_witnesses") or []):
        if isinstance(witness, dict):
            if witness.get("witness_id") is not None:
                by_witness[witness["witness_id"]] = witness
            if witness.get("chain_id") is not None:
                by_chain.setdefault(witness["chain_id"], witness)
    return by_witness, by_chain


def _entry_rule(entry: dict, by_witness: dict, by_chain: dict) -> dict | None:
    if entry.get("witness_id") in by_witness:
        return by_witness[entry["witness_id"]]
    return by_chain.get(entry.get("chain_id"))


def _is_ordering_only(witness: dict) -> bool:
    return get(witness, "chain_accepted_time_rule", "basis") \
        == "ordering_and_inclusion_only"


def check_receipts(f: Findings, scope: Scope) -> None:
    for label, doc in scope.receipts:
        facts = ReceiptFacts(label=label, doc=doc, receipt_id=doc.get("receipt_id"))
        if facts.receipt_id is not None:
            scope.facts[facts.receipt_id] = facts
        mtc = doc.get("mint_time_configuration")
        witnesses = get(mtc, "configured_witnesses")

        # THE CONFIGURED SET, refused by name when absent: without it a one-entry
        # receipt is byte-indistinguishable from a receipt minted under a
        # one-witness configuration.
        if not isinstance(witnesses, list) or not witnesses:
            f.error("receipt_missing_configured_witness_set",
                    f"{label}: no configured witness set in the mint-time "
                    f"configuration block — a holder who cannot reach the minter "
                    f"cannot tell 'one witness because the other was unreachable' "
                    f"from 'one witness by design', so the receipt is refused at "
                    f"capture time on the same footing as a missing inclusion "
                    f"proof")
            witnesses = []
        facts.configured = [w.get("witness_id") for w in witnesses
                            if isinstance(w, dict)]
        if len(witnesses) > 2:
            f.error("third_anchor_target",
                    f"{label}: {len(witnesses)} configured witnesses — the ruled "
                    f"configuration names exactly two anchor targets, and a third "
                    f"adopted by a realization, an operator or a later author "
                    f"acting alone is refused; a different witness set is a ruling "
                    f"with its own evidence, not a configuration edit")

        # THE ANCHORED DIGEST, RECOMPUTED over the two-member subject.
        material = doc.get("material_digest")
        carried = digest_value(doc.get("anchored_digest"))
        if isinstance(material, dict) and isinstance(mtc, dict) and carried:
            try:
                over_both = canonical.digest(
                    {"material_digest": material, "mint_time_configuration": mtc})
                not_committed = {digest_value(material), canonical.digest(material),
                                 canonical.digest({"material_digest": material})}
            except canonical.ConstructionError as exc:
                f.error("receipt_configuration_block_edited",
                        f"{label}: the anchored digest cannot be recomputed at "
                        f"all: {exc}")
            else:
                if carried == over_both:
                    pass
                elif carried in not_committed:
                    f.error("receipt_configuration_not_committed",
                            f"{label}: the anchored digest was taken over the "
                            f"material alone, so the mint-time configuration "
                            f"block is CARRIED BESIDE the proof rather than "
                            f"committed by it — a set a holder can edit without "
                            f"breaking a proof is a decoration, not a "
                            f"completeness signal")
                else:
                    f.error("receipt_configuration_block_edited",
                            f"{label}: the anchored digest does not recompute "
                            f"over {{material_digest, mint_time_configuration}} "
                            f"(carried {carried}, recomputed {over_both}) — a "
                            f"rewritten witness set or an extended horizon is "
                            f"exactly the edit this commitment exists to break")
        if isinstance(material, dict):
            facts.material_value = digest_value(material)

        # THE CLOSURE RULE: every receipt-only input lives inside the committed
        # block, so the sweep runs over everything except that block.
        for top_name, top_value in doc.items():
            if top_name == "mint_time_configuration":
                continue
            for path, name, _ in walk_members({top_name: top_value}):
                if name in RECEIPT_ONLY_INPUT_NAMES:
                    f.error("receipt_only_input_outside_committed_block",
                            f"{label}: member {path!r} is a receipt-only "
                            f"verification input sitting OUTSIDE the committed "
                            f"mint-time configuration block — outside the block "
                            f"it is outside the anchored digest, and a value a "
                            f"holder can edit is not an input to a fail-closed "
                            f"decision. The rule is stated as a rule: a future "
                            f"timing input joins the block by the rule and not "
                            f"by an enumeration chase")

        # THE STATE VOCABULARY: the receipt holds proof material and never state.
        for path, name, _ in walk_members(doc):
            if name in ANCHOR_STATE_VOCABULARY:
                f.error("receipt_carries_anchor_state",
                        f"{label}: member {path!r} is anchor-state vocabulary on "
                        f"a receipt — a witness still in flight is recorded in "
                        f"the anchor-state record, which is where every surface "
                        f"reads per-witness status; the receipt gains a per-chain "
                        f"entry when the four elements are captured whole and "
                        f"carries no field describing what has not happened yet")

        # THE HEADER SOURCE: minter-supplied proves self-consistency only.
        source = doc.get("declared_header_source")
        if isinstance(source, dict):
            facts.header_source_id = source.get("source_id")
            if source.get("supplied_by_minter") is True \
                    or source.get("obtainable_independently") is False:
                facts.minter_supplied_source = True
                f.error("verification_header_source_is_minter_supplied",
                        f"{label}: the declared header source is supplied by the "
                        f"minter (supplied_by_minter="
                        f"{source.get('supplied_by_minter')}, "
                        f"obtainable_independently="
                        f"{source.get('obtainable_independently')}) — a "
                        f"verification against it establishes SELF-CONSISTENCY "
                        f"and not canonicality; the trust root is a public chain "
                        f"the verifier obtains for itself")

        by_witness, by_chain = _witness_rules(mtc)
        eligible: list[tuple[datetime, dict]] = []
        for index, entry in enumerate(doc.get("per_chain_anchors") or []):
            if not isinstance(entry, dict):
                continue
            where = f"{label}: per_chain_anchors[{index}]"
            facts.entry_chains.add(entry.get("chain_id"))
            if entry.get("witness_id") is not None:
                facts.entry_witnesses.add(entry["witness_id"])

            # THE FOUR ELEMENTS, each refused BY NAME — the shape already
            # requires them, and the refusal still says what was actually
            # lacking, because "property missing" does not.
            tx = entry.get("anchor_transaction_bytes")
            if not tx:
                f.error("receipt_missing_transaction_bytes",
                        f"{where}: no anchor_transaction_bytes — a transaction "
                        f"reference plus a header is not a proof, and a receipt "
                        f"is captured once; the missing material cannot be "
                        f"recovered after the chain prunes")
            else:
                decoded = _decoded_length(tx)
                if decoded is not None and decoded < TRANSACTION_CAPTURE_FLOOR_BYTES:
                    f.error("receipt_transaction_deferred_to_verification",
                            f"{where}: anchor_transaction_bytes decodes to "
                            f"{decoded} bytes, which is a capture the size of a "
                            f"transaction IDENTIFIER rather than a transaction — "
                            f"a receipt that expects the transaction to be "
                            f"re-fetched at verification time is refused, because "
                            f"a chain that prunes will not have it to return")
            if not entry.get("inclusion_proof"):
                f.error("receipt_missing_inclusion_proof",
                        f"{where}: no inclusion_proof — without it nothing places "
                        f"the captured transaction under the supplied header's "
                        f"transaction root, and the entry proves possession of "
                        f"bytes rather than an anchor")
            header = entry.get("block_header")
            if not header:
                f.error("receipt_missing_block_header",
                        f"{where}: no block_header — the header is what the "
                        f"chain-accepted time is read from and what the inclusion "
                        f"proof terminates in; an entry without one has no "
                        f"instant and no root")
            evidence = entry.get("chain_acceptance_evidence")
            if not evidence:
                f.error("receipt_missing_chain_acceptance_evidence",
                        f"{where}: no chain_acceptance_evidence — the first three "
                        f"elements stop one step short: a fabricated header "
                        f"satisfies all of them and proves nothing about either "
                        f"witness")

            # CANONICALITY, structurally: the evidence must NAME the entry's own
            # header. This is the check's honest strength — a self-consistent
            # fabrication passes it, which is why the trust root is a header set
            # the verifier obtains independently.
            header_digest = get(header, "header_digest") if isinstance(header, dict) else None
            if isinstance(evidence, dict) and header_digest:
                kind = evidence.get("evidence_kind")
                if kind == "linear_chain":
                    linkage = get(evidence, "linear", "header_chain_linkage") or []
                    if header_digest not in linkage:
                        f.error("receipt_header_not_canonical",
                                f"{where}: the entry's own header digest "
                                f"{header_digest} is absent from the "
                                f"header-chain linkage offered as its "
                                f"canonicality evidence — evidence that never "
                                f"names the header it is for establishes nothing "
                                f"about it")
                elif kind == "dag":
                    accepting = get(evidence, "dag", "accepting_block_value")
                    if accepting != header_digest:
                        f.error("receipt_header_not_canonical",
                                f"{where}: the DAG acceptance proof names "
                                f"accepting block {accepting} while the entry "
                                f"carries the header of {header_digest} — the "
                                f"accepting block IS the block whose header the "
                                f"accepted-time rule reads, so a proof about a "
                                f"different block is a proof about a different "
                                f"anchor")

            # THE ORDERING-ONLY CORRESPONDENCE, both directions: a null time
            # under a time-bearing rule and a time under an ordering-only rule
            # are the same defect pointing opposite ways.
            witness = _entry_rule(entry, by_witness, by_chain)
            time_field = get(header, "time_field") if isinstance(header, dict) else None
            if witness is not None:
                rule = witness.get("chain_accepted_time_rule") or {}
                ordering = _is_ordering_only(witness)
                declared_flag = rule.get("ordering_only") if isinstance(rule, dict) else None
                if declared_flag is not None and bool(declared_flag) != ordering:
                    f.error("ordering-only-correspondence",
                            f"{where}: the configured rule declares basis "
                            f"{get(witness, 'chain_accepted_time_rule', 'basis')!r} "
                            f"and ordering_only={declared_flag} — the two members "
                            f"are the same fact in two spellings and the "
                            f"equivalence is enforced in both directions rather "
                            f"than trusting either alone")
                if ordering and time_field is not None:
                    f.error("ordering-only-correspondence",
                            f"{where}: a header time under an ordering-only rule "
                            f"— the honest answer for a chain whose header "
                            f"carries no usable time field is null, because a "
                            f"timestamp invented for it would rest a fail-closed "
                            f"decision on a number nothing can check")
                if not ordering and header is not None and time_field is None:
                    f.error("ordering-only-correspondence",
                            f"{where}: a null header time under a time-bearing "
                            f"rule ({get(witness, 'chain_accepted_time_rule', 'basis')!r}) "
                            f"— the same defect as a time under an ordering-only "
                            f"rule, pointing the other way")
                if not ordering:
                    parsed = instant(time_field)
                    if parsed is not None:
                        eligible.append((parsed, witness))
            parsed_any = instant(time_field)
            if parsed_any is not None:
                facts.header_times.add(parsed_any.isoformat())

        # THE TIMING MODEL, IN ITS DECLARED DIRECTION.
        facts.d_max = as_int(get(mtc, "max_submission_to_first_anchor_delay_seconds"))
        facts.submission = instant(get(mtc, "submission_time"))
        if eligible:
            a_min, a_rule = min(eligible, key=lambda pair: pair[0])
            facts.a_min = a_min
            rule = a_rule.get("chain_accepted_time_rule") or {}
            facts.a_min_skew = as_int(rule.get("skew_seconds")) or 0
            facts.a_min_tolerance = as_int(rule.get("tolerance_seconds")) or 0
            if facts.submission is not None:
                late_by = seconds_between(facts.submission, a_min)
                if late_by > facts.a_min_skew:
                    facts.submission_refusable = True
                    f.error("receipt_submission_after_earliest_chain_time",
                            f"{label}: the declared submission is "
                            f"{int(late_by)}s LATER than the earliest "
                            f"chain-accepted time, beyond that chain's declared "
                            f"backward skew of {facts.a_min_skew}s — provably "
                            f"false, since no witness can accept material before "
                            f"it exists by more than the consensus rule's worst "
                            f"legal case. WITHIN the skew the same receipt is "
                            f"accepted: a header time is a reference with a "
                            f"width, never an upper bound on submission")
                if facts.d_max is not None:
                    early_by = seconds_between(a_min, facts.submission)
                    margin = facts.d_max + facts.a_min_tolerance
                    if early_by > margin:
                        f.error("receipt_self_inconsistent_delay",
                                f"{label}: the earliest chain-accepted time "
                                f"exceeds the declared submission by "
                                f"{int(early_by)}s, over the declared maximum "
                                f"delay plus tolerance ({margin}s) — the receipt "
                                f"documents its own breach, and it is refused at "
                                f"capture time and receipt-only alike, so a "
                                f"minter cannot mint a clean receipt over a "
                                f"delay it already exceeded")


# --------------------------- anchor state ---------------------------

def check_anchor_states(f: Findings, scope: Scope) -> None:
    for label, doc in scope.states:
        facts = scope.facts.get(doc.get("receipt_ref"))
        state = doc.get("state")
        rows = [row for row in (doc.get("per_witness") or []) if isinstance(row, dict)]
        transitions = [entry for entry in (doc.get("transitions") or [])
                       if isinstance(entry, dict)]

        # NO AGGREGATE BOOLEAN ANYWHERE: such a field can read true while a
        # configured witness is missing, which is how an outage becomes
        # selectivity by accident.
        for path, name, _ in walk_members(doc):
            if name in AGGREGATE_BOOLEAN_NAMES:
                f.error("anchor_state_aggregate_boolean",
                        f"{label}: member {path!r} is an aggregate anchored "
                        f"boolean — there is none anywhere in this capability; "
                        f"per-witness status is what every surface reads instead")

        # EVERY TRANSITION CARRIES ITS LEAF: the move between states is evidence,
        # not a derived opinion.
        for index, entry in enumerate(transitions):
            if not entry.get("leaf_ref"):
                f.error("anchor_state_transition_without_leaf",
                        f"{label}: transitions[{index}] "
                        f"({entry.get('transition')!r}) carries no leaf_ref — a "
                        f"transition claimed without a leaf is an opinion about "
                        f"a state machine rather than a record of it, and the "
                        f"incompleteness is evidence: a silent gap is what the "
                        f"leaf makes impossible")
            if entry.get("transition") == "terminal_witness_failure" \
                    and not entry.get("ground"):
                f.warn("transition-ground-unnamed",
                       f"{label}: transitions[{index}] records a terminal witness "
                       f"failure with no named ground; the closed grounds exist "
                       f"so the record and its leaf can be compared")

        # COMPLETION RESTS ON A CAPTURED RECEIPT WITH EVERY WITNESS LANDED —
        # the anchoring subsystem marks an item complete by no other path.
        if state == "anchor_complete":
            unlanded = [row.get("witness_id") for row in rows
                        if row.get("status") != "landed"]
            if not doc.get("receipt_ref"):
                f.error("anchor_state_complete_without_captured_receipt",
                        f"{label}: state anchor_complete with no captured receipt "
                        f"referenced — completion is the captured multi-anchor "
                        f"receipt holding every configured witness's four "
                        f"elements, and nothing else is that")
            if unlanded:
                f.error("anchor_state_complete_without_captured_receipt",
                        f"{label}: state anchor_complete while witness(es) "
                        f"{unlanded} are not landed — a completeness claim over a "
                        f"missing witness is the aggregate boolean's defect "
                        f"wearing the state machine's clothes")

        # THE STATES ARE DISJOINT: pending says nothing has gone wrong YET, so a
        # recorded terminal failure or breach contradicts it.
        if state == "anchor_pending":
            failed = [row.get("witness_id") for row in rows
                      if row.get("status") == "terminally_failed"]
            if failed:
                f.error("anchor_state_pending_and_incomplete",
                        f"{label}: state anchor_pending while witness(es) "
                        f"{failed} stand terminally failed — a terminal failure "
                        f"moves an item out of anchor_pending immediately rather "
                        f"than waiting out a horizon that cannot now be met")
            contradicting = [entry.get("transition") for entry in transitions
                             if entry.get("transition") in
                             ("horizon_breach", "terminal_witness_failure")]
            if contradicting:
                f.error("anchor_state_pending_and_incomplete",
                        f"{label}: state anchor_pending with {contradicting} "
                        f"transition(s) recorded — the record carries the "
                        f"evidence of its own incompleteness and reports the "
                        f"state it moved out of")

        # THE COUNT AGREES WITH THE COMMITTED BLOCK, which is the one a holder
        # cannot edit; a disagreement is refused rather than either preferred.
        declared_count = as_int(doc.get("configured_witness_count"))
        if facts is not None and declared_count is not None \
                and facts.configured and declared_count != len(facts.configured):
            f.error("witness_shortfall_miscomputed",
                    f"{label}: configured_witness_count={declared_count} "
                    f"disagrees with the {len(facts.configured)} configured "
                    f"witnesses of the receipt's committed mint-time "
                    f"configuration block — the shortfall is arithmetic over the "
                    f"committed set, and arithmetic over a different set is a "
                    f"different answer")

        horizons_by_witness: dict[Any, dict] = {}
        if facts is not None:
            by_witness, _ = _witness_rules(get(facts.doc, "mint_time_configuration"))
            horizons_by_witness = by_witness

        for row in rows:
            wid = row.get("witness_id")
            where = f"{label}: per_witness[{wid}]"

            # A RECEIPT ENTRY FOR A WITNESS STILL IN FLIGHT: the receipt gains an
            # entry when the four elements are captured whole, never before.
            if row.get("status") == "in_flight" and facts is not None \
                    and (wid in facts.entry_witnesses
                         or row.get("chain_id") in facts.entry_chains):
                f.error("receipt_entry_incomplete_for_pending_witness",
                        f"{where}: this witness is recorded still in flight while "
                        f"the referenced receipt already carries a per-chain "
                        f"entry for it — a receipt entry exists only once the "
                        f"four elements are captured whole; a witness in flight "
                        f"is a pending proof held HERE, and the later upgrade "
                        f"appends a whole entry")

            # THE OPERATIONAL WITNESS'S CAPTURE CONDITION, per item.
            if row.get("role") == "operational" \
                    and row.get("inclusion_proof_captured_at_anchor_time") is False:
                f.error("operational_anchor_without_retained_proof",
                        f"{where}: an operational-witness anchor captured without "
                        f"retaining its inclusion proof at anchor time — the item "
                        f"is NOT credited with that witness, and a plan to "
                        f"re-derive the proof later is not accepted, because the "
                        f"chain will have pruned the material the derivation "
                        f"needs")

            # AN AGGREGATION PROOF COMPLETES BY UPGRADE, NOT BY A SECOND ANCHOR.
            if get(row, "pending_durability_proof", "reanchored") is True:
                f.error("durability_proof_reanchored_rather_than_upgraded",
                        f"{where}: the pending durability proof was re-anchored "
                        f"rather than upgraded — a second transaction for the "
                        f"same digest leaves two proofs to keep where one was "
                        f"owed; the pending proof is held in this record and "
                        f"APPENDED to the receipt when the calendar returns")

            # THE HORIZON BASE IS A HEADER TIME OR IT IS NOT A BASE.
            base = row.get("horizon_base")
            if isinstance(base, dict) and base.get("kind") == "chain_derived":
                value = instant(base.get("value"))
                if value is not None and facts is not None and facts.header_times \
                        and value.isoformat() not in facts.header_times:
                    if facts.submission is not None and value == facts.submission:
                        f.error("horizon_base_from_minter_clock",
                                f"{where}: the chain-derived horizon base equals "
                                f"the receipt's DECLARED SUBMISSION TIME, which "
                                f"is the minter's assertion and not a clock — "
                                f"binding it makes it tamper-evident, not true")
                    else:
                        f.error("horizon_base_from_minter_clock",
                                f"{where}: horizon base {base.get('value')} is "
                                f"declared chain-derived but matches no block "
                                f"header time in the referenced receipt's own "
                                f"per-chain list — a base the artifact cannot be "
                                f"checked against is a minter's clock wearing "
                                f"the wrong kind")

            if row.get("status") == "terminally_failed" \
                    and not row.get("terminal_failure_ground"):
                f.warn("terminal-ground-unnamed",
                       f"{where}: terminally failed with no named ground from "
                       f"the closed set; a ground a validator cannot compare is "
                       f"a ground it cannot check")
            if facts is not None and wid in horizons_by_witness:
                committed = horizons_by_witness[wid].get("completion_horizon_seconds")
                declared = row.get("completion_horizon_seconds")
                if committed is not None and declared is not None \
                        and committed != declared:
                    f.warn("horizon-disagrees-with-committed-block",
                           f"{where}: declares horizon {declared}s where the "
                           f"receipt's committed block declares {committed}s — "
                           f"the committed block governs, being the one a holder "
                           f"cannot edit")

        # A BREACH DECLARED INSIDE THE MARGIN: the margin is applied in one
        # direction only, and a false breach turns the operator signal into
        # noise on a sound item.
        for index, entry in enumerate(transitions):
            if entry.get("transition") != "horizon_breach":
                continue
            occurred = instant(entry.get("occurred_at"))
            row = next((r for r in rows
                        if r.get("witness_id") == entry.get("witness_id")), None)
            if occurred is None or row is None or facts is None:
                continue
            base = instant(get(row, "horizon_base", "value")) \
                if get(row, "horizon_base", "kind") == "chain_derived" else None
            horizon = as_int(row.get("completion_horizon_seconds"))
            if base is None or horizon is None:
                continue
            margin = horizon + facts.a_min_skew + facts.a_min_tolerance
            elapsed = seconds_between(occurred, base)
            if elapsed <= margin:
                f.error("breach_declared_within_tolerance",
                        f"{label}: transitions[{index}] declares a horizon "
                        f"breach for {entry.get('witness_id')!r} after "
                        f"{int(elapsed)}s, within the declared margin of "
                        f"{margin}s (horizon + skew + tolerance) — a horizon "
                        f"exceeded by less than the margin is NOT a breach; the "
                        f"harm is asymmetric, and a false breach raises the "
                        f"operator obligation on a sound item")


# --------------------------- verification results ---------------------------

def check_verifications(f: Findings, scope: Scope) -> None:
    minter_sources = {facts.header_source_id
                      for facts in scope.facts.values()
                      if facts.minter_supplied_source
                      and facts.header_source_id is not None}
    for label, doc in scope.verifications:
        mode = doc.get("verification_mode")
        status = doc.get("status")
        facts = scope.facts.get(doc.get("receipt_ref"))
        base = doc.get("horizon_base") if isinstance(doc.get("horizon_base"), dict) \
            else None

        if not mode:
            f.error("verification_mode_absent",
                    f"{label}: no verification_mode — receipt_only and stateful "
                    f"carry genuinely different knowledge behind the same status "
                    f"value, and a caller that cannot read which one it holds is "
                    f"consuming the weaker answer as the stronger")

        # A RECEIPT-ONLY RESULT MAY NOT CLAIM STATEFUL KNOWLEDGE: a terminal
        # failure arises after the receipt was minted and leaves no mark on it.
        if mode == "receipt_only":
            if doc.get("terminal_failure_distinguished") is True:
                f.error("verification_result_claims_stateful_knowledge",
                        f"{label}: a receipt_only result declares "
                        f"terminal_failure_distinguished: true — structurally "
                        f"impossible, since a terminally failed item's receipt "
                        f"is byte-identical to a sound one's")
            if doc.get("anchor_state_ref"):
                f.error("verification_result_claims_stateful_knowledge",
                        f"{label}: a receipt_only result names an "
                        f"anchor_state_ref — it has read something its own mode "
                        f"says it did not")
            if doc.get("delay_check"):
                f.error("verification_result_claims_stateful_knowledge",
                        f"{label}: a receipt_only result carries a delay_check — "
                        f"only stateful can prove a delay breach, because the "
                        f"bracket is read from the log and not from the receipt")
            if doc.get("incomplete_cause") == "terminal_witness_failure":
                f.error("verification_result_claims_stateful_knowledge",
                        f"{label}: a receipt_only result attributes its "
                        f"incomplete to a terminal witness failure — the honest "
                        f"receipt-only value is undistinguished_receipt_only, "
                        f"which says so instead of omitting the field silently")

        # NO DETERMINATION ON A MINTER-CLAIMED BASE, in either mode: a claim the
        # artifact cannot check is not a basis for a fail-closed answer.
        determined = status in ("anchor_pending", "anchor_incomplete",
                                "anchor_complete")
        if determined and (base is None or base.get("kind") in
                           ("minter_claimed", "none")):
            f.error("determination_made_with_minter_claimed_base",
                    f"{label}: status {status!r} was determined on a "
                    f"{get(base, 'kind') if base else 'missing'} horizon base — "
                    f"where no landed witness is eligible as a base, the honest "
                    f"result is no_determination, a first-class answer rather "
                    f"than a gap")

        # THE BASE IS A HEADER TIME OF THE RECEIPT'S OWN PER-CHAIN LIST.
        if base is not None and base.get("kind") == "chain_derived" \
                and facts is not None and facts.header_times:
            value = instant(base.get("chain_accepted_time"))
            if value is not None and value.isoformat() not in facts.header_times:
                if facts.submission is not None and value == facts.submission:
                    f.error("horizon_base_from_minter_clock",
                            f"{label}: the horizon base equals the receipt's "
                            f"DECLARED SUBMISSION TIME — the minter's assertion, "
                            f"not a clock; every horizon determination runs from "
                            f"the earliest chain-accepted time and never from "
                            f"the declared submission, which is why a "
                            f"future-dated submission is exposed rather than "
                            f"obeyed")
                else:
                    f.error("horizon_base_from_minter_clock",
                            f"{label}: horizon base "
                            f"{base.get('chain_accepted_time')} is declared "
                            f"chain-derived but matches no block header time in "
                            f"the referenced receipt")

        # THE SHORTFALL IS ARITHMETIC AND THE ARITHMETIC IS CHECKED.
        shortfall = doc.get("witness_shortfall")
        missing: list = []
        if isinstance(shortfall, dict):
            configured = shortfall.get("configured") or []
            present = shortfall.get("present") or []
            missing = shortfall.get("missing") or []
            if set(missing) != set(configured) - set(present) \
                    or not set(present) <= set(configured):
                f.error("witness_shortfall_miscomputed",
                        f"{label}: the three lists do not reconcile — missing "
                        f"must be exactly configured minus present "
                        f"(configured={sorted(configured)}, "
                        f"present={sorted(present)}, missing={sorted(missing)}); "
                        f"a record that does not reconcile is refused rather "
                        f"than read as a partial answer")
            if facts is not None and facts.configured \
                    and set(configured) != set(facts.configured):
                f.error("witness_shortfall_miscomputed",
                        f"{label}: the configured list {sorted(configured)} "
                        f"disagrees with the receipt's committed witness set "
                        f"{sorted(facts.configured)} — the shortfall is "
                        f"established from the receipt alone, and the committed "
                        f"block is the set it is established against")
            elif facts is not None and facts.entry_witnesses \
                    and not set(present) <= facts.entry_witnesses:
                f.error("witness_shortfall_miscomputed",
                        f"{label}: present list {sorted(present)} credits a "
                        f"witness the receipt's per-chain list carries no entry "
                        f"for — presence is a per-chain entry with its four "
                        f"elements, not an assertion")

        # AN ITEM IS NEVER PRESENTED AS ANCHORED WITH A WITNESS MISSING.
        if status == "anchor_complete" and missing:
            f.error("item_presented_as_anchored_with_missing_witness",
                    f"{label}: status anchor_complete while the shortfall names "
                    f"missing witness(es) {sorted(missing)} — while an item is "
                    f"incomplete a verification returns anchor_incomplete naming "
                    f"the missing witnesses, never a bare pass and never a bare "
                    f"fail, because the record supports neither answer")

        # A BREACH DECLARED INSIDE THE MARGIN, on the result's own numbers.
        if status == "anchor_incomplete" \
                and doc.get("incomplete_cause") != "terminal_witness_failure" \
                and facts is not None and missing:
            evaluated = instant(doc.get("evaluated_at"))
            base_time = instant(get(base, "chain_accepted_time")) \
                if base and base.get("kind") == "chain_derived" else facts.a_min
            if evaluated is not None and base_time is not None:
                by_witness, _ = _witness_rules(
                    get(facts.doc, "mint_time_configuration"))
                margins = [as_int(by_witness[wid].get("completion_horizon_seconds"))
                           for wid in missing if wid in by_witness]
                margins = [h + facts.a_min_skew + facts.a_min_tolerance
                           for h in margins if h is not None]
                elapsed = seconds_between(evaluated, base_time)
                if margins and all(elapsed <= margin for margin in margins):
                    f.error("breach_declared_within_tolerance",
                            f"{label}: anchor_incomplete declared after "
                            f"{int(elapsed)}s, within every missing witness's "
                            f"declared margin (horizon + skew + tolerance, "
                            f"largest {max(margins)}s) — the margin is applied "
                            f"in one direction only, and a horizon exceeded by "
                            f"less than it is not a breach")

        # THE HONEST TWIN IS ACCEPTED, AND REFUSING IT IS ITSELF REFUSED: the
        # direction error this family had to fix three times, pinned as a check.
        refusal = doc.get("refusal") if isinstance(doc.get("refusal"), dict) else None
        if status == "refused" and refusal is None:
            f.warn("refusal-unnamed",
                   f"{label}: status refused with no refusal member — a refusal "
                   f"is an outcome of this record, and it names what was "
                   f"actually lacking")
        if refusal is not None \
                and refusal.get("code") == "receipt_submission_after_earliest_chain_time" \
                and facts is not None and not facts.submission_refusable:
            f.error("honest_receipt_refused_within_skew",
                    f"{label}: refuses receipt {doc.get('receipt_ref')!r} for a "
                    f"submission after the earliest chain time, but that "
                    f"receipt's declared submission falls WITHIN the declared "
                    f"backward skew — an honest receipt's declared submission "
                    f"may legitimately fall after its header time, because a "
                    f"header time is a reference with a width and never an "
                    f"upper bound on submission")

        # THE DELAY CHECK PROVES A BREACH OR IT PROVES NOTHING.
        for path, name, _ in walk_members(doc):
            lowered = name.lower()
            if any(token in lowered for token in COMPLIANCE_NAME_TOKENS):
                f.error("delay_check_read_as_compliance",
                        f"{label}: member {path!r} asserts delay COMPLIANCE — "
                        f"the check rests on a LOWER bound on the true delay: "
                        f"exceeding the declared maximum proves a breach, and "
                        f"falling under it leaves the true delay unknown. "
                        f"Not-provably-breached is not compliant, and the "
                        f"residual is exactly one cadence interval")
        delay = doc.get("delay_check")
        if isinstance(delay, dict) and mode == "stateful":
            cp_in = instant(delay.get("cp_in"))
            cp_out = instant(delay.get("cp_out"))
            a_first = instant(delay.get("a_first"))
            bound = as_int(delay.get("bound_seconds"))
            if cp_in is not None and cp_out is not None and cp_out >= cp_in:
                f.error("delay-check-arithmetic",
                        f"{label}: delay_check bracket is not a bracket — cp_out "
                        f"(latest checkpoint NOT containing the submission leaf) "
                        f"must precede cp_in (earliest containing it)")
            if cp_in is not None and a_first is not None and bound is not None \
                    and bound != int(seconds_between(a_first, cp_in)):
                f.error("delay-check-arithmetic",
                        f"{label}: bound_seconds={bound} is not a_first - cp_in "
                        f"({int(seconds_between(a_first, cp_in))}s) — the bound "
                        f"is the difference it claims to be or it is a number "
                        f"beside two timestamps")
            if facts is not None and facts.d_max is not None and bound is not None:
                threshold = facts.d_max + facts.a_min_tolerance
                if delay.get("outcome") == "breach_proven" and bound <= threshold:
                    f.error("breach_declared_within_tolerance",
                            f"{label}: delay_check claims breach_proven on a "
                            f"lower bound of {bound}s, within the declared "
                            f"maximum delay plus tolerance ({threshold}s) — a "
                            f"breach is proven by exceeding the declared "
                            f"maximum, not by approaching it")
                if delay.get("outcome") == "not_proven" and bound > threshold:
                    f.warn("delay-breach-understated",
                           f"{label}: delay_check reports not_proven while its "
                           f"own lower bound ({bound}s) exceeds the declared "
                           f"maximum plus tolerance ({threshold}s)")

        # THE HEADER SOURCE, cross-checked where the reference resolves.
        if doc.get("header_source_ref") in minter_sources:
            f.error("verification_header_source_is_minter_supplied",
                    f"{label}: this verification ran against header source "
                    f"{doc.get('header_source_ref')!r}, which a receipt in scope "
                    f"declares minter-supplied — the verification establishes "
                    f"self-consistency and not canonicality")


# --------------------------- commitments and custody ---------------------------

def _custody_check(f: Findings, label: str, member: str, node: Any,
                   code: str) -> None:
    if not isinstance(node, dict):
        return
    resolves = node.get("resolves_into")
    if resolves is not None and resolves != GOVERNED_CUSTODY:
        secret = "salt" if code.startswith("salt") else "key"
        f.error(code,
                f"{label}: {member} resolves into {resolves!r} — a {secret} "
                f"reachable from the anchor destroys the erasure property the "
                f"construction exists to provide; both secrets resolve into the "
                f"governed layer and nowhere the anchor can reach")


def check_commitments(f: Findings, scope: Scope) -> None:
    for label, doc in scope.commitments:
        construction = doc.get("declared_construction")
        if not isinstance(construction, dict):
            f.error("commitment_construction_absent",
                    f"{label}: no declared construction — a salted keyed "
                    f"commitment and a plain digest of the same material are "
                    f"indistinguishable by inspection, so the construction is "
                    f"declared beside the value and never inferred from it")
            construction = {}

        # AN HONESTLY DECLARED PLAIN DIGEST IS REFUSED TOO: the boundary refuses
        # the CONSTRUCTION and not the disclosure.
        if construction and (construction.get("keyed") is not True
                             or construction.get("salted") is not True):
            f.error("commitment_not_keyed_and_salted",
                    f"{label}: declared construction has "
                    f"keyed={construction.get('keyed')}, "
                    f"salted={construction.get('salted')} — every anchor-bound "
                    f"commitment is keyed AND salted, and honesty about a plain "
                    f"digest is not accepted as a defence, because a plain "
                    f"digest of a record looks like exactly the right thing to "
                    f"anchor and is exactly the wrong one")

        _custody_check(f, label, "salt_custody", construction.get("salt_custody"),
                       "salt_custody_reference_reachable_from_anchor")
        _custody_check(f, label, "key_custody", construction.get("key_custody"),
                       "key_custody_reference_reachable_from_anchor")

        # "SALTED" WITHOUT A DECLARED SOURCE AND WIDTH IS NOT A PROPERTY.
        if construction.get("salted") is True:
            source = construction.get("salt_source")
            width = as_int(construction.get("salt_width_bits"))
            if source is None or width is None:
                f.error("salt_entropy_declaration_absent",
                        f"{label}: the construction declares it is salted and "
                        f"names {'no source' if source is None else 'no width'} "
                        f"— 'salted' without a declared source and width in bits "
                        f"is not a property a validator or a reader can judge")
            if source in ("unspecified", "non_cryptographic"):
                f.error("salt_entropy_declaration_absent",
                        f"{label}: salt_source={source!r} — a salt from a "
                        f"non-cryptographic or unspecified source declares "
                        f"entropy nobody measured")
            if width is not None and width < SALT_WIDTH_FLOOR_BITS:
                f.error("salt_width_below_floor",
                        f"{label}: salt_width_bits={width}, below the "
                        f"{SALT_WIDTH_FLOOR_BITS}-bit floor. The ground is the "
                        f"reading requirement 5 cites — EDPB Guidelines 02/2025 "
                        f"— that what makes a hash of a person's attributes "
                        f"reach that person is that the INPUT SPACE CAN BE "
                        f"SEARCHED: a narrow salt satisfies every other check "
                        f"here while leaving that search trivial. An overlay "
                        f"may raise this floor and SHALL NOT lower it")
            if construction.get("salt_scope") == "shared":
                f.warn("salt-scope-shared",
                       f"{label}: salt_scope=shared — a salt shared across "
                       f"records restores the correlation the per-record salt "
                       f"exists to break")

        # ONLY GATE-PASSED MATERIAL GETS AN ITEM ANCHOR, and no urgency argument
        # admits unvalidated material: the resulting anchor would be permanent.
        if doc.get("receipt_ref") and not doc.get("named_gate_ref"):
            f.error("item_anchor_over_ungated_material",
                    f"{label}: anchored as an item (receipt_ref present) with no "
                    f"named gate reference — only gate-passed material gets an "
                    f"item anchor; a broken chain is a fraud signal, and a false "
                    f"attestation that reaches a chain is permanent")

        record_digest_check(f, label, doc, "commitment_digest")


def record_digest_check(f: Findings, label: str, doc: dict, member: str) -> None:
    node = doc.get(member)
    if not isinstance(node, dict):
        return
    body = {name: value for name, value in doc.items() if name != member}
    try:
        recomputed = canonical.digest(body)
    except canonical.ConstructionError as exc:
        f.error("record-digest-mismatch",
                f"{label}: {member} cannot be recomputed: {exc}")
        return
    if node.get("value") != recomputed:
        f.error("record-digest-mismatch",
                f"{label}: {member} does not recompute over this record's own "
                f"members under the one construction in force (carried "
                f"{node.get('value')}, recomputed {recomputed}) — the digest a "
                f"leaf commits to is the record, so a value that does not "
                f"recompute names a different record")


# --------------------------- checkpoint anchors and consent ---------------------------

def check_checkpoint_anchors(f: Findings, scope: Scope,
                             docs: dict[str, dict]) -> None:
    disclaimer = get(docs.get("log-checkpoint-anchor.schema.yaml", {}),
                     "properties", "validation_disclaimer", "const")
    for label, doc in scope.checkpoints:
        carried = doc.get("validation_disclaimer")
        if disclaimer is not None and carried != disclaimer:
            f.error("checkpoint_anchor_missing_disclaimer",
                    f"{label}: the validation disclaimer is "
                    f"{'absent' if carried is None else 'reworded'} — a "
                    f"disclaimer a realization can reword is a disclaimer a "
                    f"realization can weaken, and this is the one sentence whose "
                    f"weakening would turn an integrity witness into a validity "
                    f"claim")
        if doc.get("presented_as_validation") is True:
            f.error("checkpoint_inclusion_presented_as_validation",
                    f"{label}: checkpoint inclusion presented as validation — an "
                    f"anchored checkpoint witnesses that the log said something "
                    f"at a time; it proves the log's integrity and ordering and "
                    f"NOTHING about any leaf inside it, refusals and "
                    f"later-invalidated events included")

        # THE ANCHOR COMMITS TO WHAT IT SAYS IT DOES: the record and its receipt
        # are compared rather than assumed to agree.
        facts = scope.facts.get(doc.get("receipt_ref"))
        carried_digest = digest_value(doc.get("checkpoint_digest"))
        if facts is not None and facts.material_value is not None \
                and carried_digest is not None \
                and carried_digest != facts.material_value:
            f.error("checkpoint-anchor-mismatch",
                    f"{label}: checkpoint_digest {carried_digest} is not the "
                    f"material_digest of the referenced receipt "
                    f"({facts.material_value}) — without that equality the "
                    f"record names an anchor of nothing in particular")

        # THE CLOSURE RULE REACHES THIS RECORD TOO: the cadence obligation is
        # checked over the two anchors' own receipts, so an interval asserted
        # here would be a minter-written timing value outside the committed
        # block.
        for path, name, _ in walk_members(doc):
            if name in RECEIPT_ONLY_INPUT_NAMES:
                f.error("receipt_only_input_outside_committed_block",
                        f"{label}: member {path!r} is a receipt-only timing "
                        f"input asserted on a checkpoint anchor — this record "
                        f"carries the pointer to the previous anchor and never "
                        f"the number; the interval is derived from the two "
                        f"receipts' own chain-accepted times")


def check_consents(f: Findings, scope: Scope) -> None:
    for label, doc in scope.consents:
        # A PUBLIC CHAIN NEVER SEES A PER-SUBJECT CONSENT ROW: a row is publicly
        # linkable to a person and a checkpoint is not.
        for path, name, _ in walk_members(doc):
            lowered = name.lower()
            if any(token in lowered for token in CONSENT_ROW_NAME_TOKENS):
                f.error("consent_row_offered_for_anchoring",
                        f"{label}: member {path!r} names a per-subject consent "
                        f"row on a record whose value reaches a chain — what is "
                        f"anchored is the consent log's CHECKPOINT, which "
                        f"discloses that the log said something at a time and "
                        f"nothing about any decision inside it")
        if doc.get("enforcement_site") == "anchoring_chain_contract_code":
            f.error("consent_enforcement_as_on_chain_contract_code",
                    f"{label}: consent enforcement declared as contract code on "
                    f"the anchoring chain — consent, enrollment and access "
                    f"policy are authority questions, and this capability "
                    f"places none of them on any anchoring chain and deploys no "
                    f"contract code on one. The refusal states no permanent bar "
                    f"and names no trigger condition; a later change answers to "
                    f"its own evidence")
        if doc.get("recall_claimed") is True:
            f.error("revocation_presented_as_recall",
                    f"{label}: recall claimed — a revocation supersedes forward "
                    f"from the moment it is recorded and anchored; it does not "
                    f"reach a copy already disclosed, and nothing on a chain "
                    f"can be un-published")
        semantics = doc.get("revocation_semantics")
        if semantics is not None and semantics != "supersedes_forward_only":
            f.error("revocation_presented_as_recall",
                    f"{label}: revocation_semantics={semantics!r} — forward "
                    f"supersession is what a revocation delivers; recall is "
                    f"what nothing on a chain can deliver")
        if doc.get("plane_unreachable_refuses") is False:
            f.warn("plane-unreachable-read-as-permission",
                   f"{label}: declares that a consent-dependent act proceeds "
                   f"when the permissioned plane cannot be reached — an "
                   f"unevaluable answer read as permission, against the "
                   f"family's fail-closed doctrine")


# --------------------------- planes and linkage ---------------------------

def check_planes(f: Findings, scope: Scope) -> None:
    # ONE KEY UNDER TWO PLANES IS A JOIN KEY WHATEVER THE SALTS DO. The map is
    # built across plane declarations AND anchor-bound commitments, because the
    # sharing this refusal exists for is exactly the kind that spans records.
    key_planes: dict[Any, dict[Any, str]] = {}
    for label, doc in scope.planes:
        for entry in (doc.get("per_plane_keys") or []):
            if isinstance(entry, dict):
                ref = get(entry, "key_custody", "reference_id")
                if ref is not None:
                    key_planes.setdefault(ref, {})[entry.get("plane")] = label
                _custody_check(f, label, f"per_plane_keys[{entry.get('plane')}]",
                               entry.get("key_custody"),
                               "key_custody_reference_reachable_from_anchor")
    for label, doc in scope.commitments:
        ref = get(doc, "declared_construction", "key_custody", "reference_id")
        if ref is not None and doc.get("plane") is not None:
            key_planes.setdefault(ref, {})[doc.get("plane")] = label
    for ref, planes in sorted(key_planes.items(), key=lambda pair: str(pair[0])):
        if len(planes) > 1:
            f.error("commitment_key_shared_across_planes",
                    f"{'; '.join(sorted(set(planes.values())))}: key custody "
                    f"reference {ref!r} appears under planes "
                    f"{sorted(str(p) for p in planes)} — a key common to two "
                    f"planes is a join key whatever their salts do, and the "
                    f"segregation is only structural if the keys are")

    salt_planes: dict[Any, dict[Any, str]] = {}
    for label, doc in scope.planes:
        for entry in (doc.get("per_plane_salts") or []):
            if isinstance(entry, dict):
                ref = get(entry, "salt_custody", "reference_id")
                if ref is not None:
                    salt_planes.setdefault(ref, {})[entry.get("plane")] = label
                _custody_check(f, label, f"per_plane_salts[{entry.get('plane')}]",
                               entry.get("salt_custody"),
                               "salt_custody_reference_reachable_from_anchor")

    for ref, planes in sorted(salt_planes.items(), key=lambda pair: str(pair[0])):
        if len(planes) > 1:
            f.error("cross_plane_join_key_shared",
                    f"{'; '.join(sorted(set(planes.values())))}: salt custody "
                    f"reference {ref!r} appears under planes "
                    f"{sorted(str(p) for p in planes)} — per-plane salts under "
                    f"per-plane keys are what make the segregation structural; "
                    f"either one shared leaves a join available")

    for label, doc in scope.planes:
        for entry in (doc.get("identifier_policy") or []):
            if isinstance(entry, dict) \
                    and entry.get("plane") in ANALYZED_PLANES \
                    and entry.get("direct_identifier_present") is True:
                f.error("direct_identifier_in_demographic_plane",
                        f"{label}: the {entry.get('plane')} plane declares a "
                        f"direct person-resolving identifier — the linkage that "
                        f"resolves a person exists only inside the governed "
                        f"identity plane, so that no direct identifier is "
                        f"exposed because there is none to expose, not because "
                        f"a query was written carefully")
        mechanism = get(doc, "cross_plane_correlation", "mechanism")
        if mechanism in ("shared_stable_key", "shared_record_digest"):
            f.error("cross_plane_join_key_shared",
                    f"{label}: cross-plane correlation mechanism {mechanism!r} — "
                    f"anyone holding two rows can link them without either "
                    f"plane's permission; a shared stable key and a shared "
                    f"record digest are the same key wearing a different name. "
                    f"The lawful mechanism is the authorized, scoped linkage "
                    f"derivation")
        issuer = get(doc, "cross_plane_correlation", "derivation_issuer_plane")
        if mechanism == "authorized_scoped_derivation" and issuer is not None \
                and issuer != "identity":
            f.error("linkage_derivation_not_issued_by_identity_plane",
                    f"{label}: derivations declared issued by the {issuer!r} "
                    f"plane — linkage lives only in the identity plane, and an "
                    f"unauthorized derivation is a join key minted by whoever "
                    f"wanted one")
        if doc.get("anchored_commitment_usable_as_join_key") is True:
            f.error("anchored_commitment_used_as_join_key",
                    f"{label}: declares the anchored commitment usable as a "
                    f"cross-plane join key — the commitment is derived under "
                    f"the record plane's own salt held in the governed layer, "
                    f"and no plane's key is derivable from it; a declaration "
                    f"that it joins planes is a declaration that the "
                    f"segregation was not built")
        if doc.get("deidentification_claimed_from_separation") is True:
            f.error("analysis_result_labelled_deidentified",
                    f"{label}: de-identification claimed from plane separation "
                    f"alone — not querying the identity plane removes the "
                    f"direct linkage and not the identifying power of the "
                    f"attributes that remain; the label is carried by a NAMED "
                    f"determination made elsewhere, and this capability names "
                    f"no standard for it and stands in for none")
        if doc.get("identity_plane_read_by_analysis") is True:
            f.warn("identity-plane-read-by-analysis",
                   f"{label}: declares the identity plane read during analysis "
                   f"— correlation is authorized in advance by a derivation "
                   f"rather than resolved during a run")


def check_linkage(f: Findings, scope: Scope) -> None:
    issuance_by_id: dict[Any, tuple[str, dict]] = {}
    parameter_analyses: dict[str, dict[Any, str]] = {}
    for label, doc in scope.issuances:
        if doc.get("derivation_id") is not None:
            issuance_by_id[doc["derivation_id"]] = (label, doc)
        plane = doc.get("issuing_plane")
        if plane is not None and plane != "identity":
            f.error("linkage_derivation_not_issued_by_identity_plane",
                    f"{label}: issued by the {plane!r} plane — the identity "
                    f"plane is the only place linkage is permitted to live, and "
                    f"a derivation minted anywhere else is a join key minted by "
                    f"whoever wanted one")
        if doc.get("consent_checkpoint_anchored") is not True:
            f.error("linkage_derivation_without_anchored_consent_checkpoint",
                    f"{label}: issued without an ANCHORED consent checkpoint "
                    f"(consent_checkpoint_anchored="
                    f"{doc.get('consent_checkpoint_anchored')}) — an "
                    f"authorization resting on a checkpoint nobody witnessed "
                    f"rests on the issuer's own word, which is the thing the "
                    f"anchoring exists to replace")
        if not doc.get("expires_at") or not doc.get("revocation_surface_ref"):
            f.error("linkage_derivation_not_expiring_or_revocable",
                    f"{label}: no {'expires_at' if not doc.get('expires_at') else 'revocation_surface_ref'} "
                    f"— a derivation that neither expires nor can be revoked is "
                    f"an authorization that never ends, and an authorization "
                    f"that ends must actually end")
        parameter = doc.get("per_analysis_parameter")
        if isinstance(parameter, str):
            parameter_analyses.setdefault(parameter, {})[
                doc.get("analysis_ref")] = label
        record_digest_check(f, label, doc, "derivation_digest")

    # PER-ANALYSIS AND NEVER STABLE: a parameter repeated under a second
    # analysis is the shared cross-plane key under another name, however the
    # value was computed — the defect is the missing authorization, not the
    # arithmetic.
    for parameter, analyses in sorted(parameter_analyses.items()):
        if len(analyses) > 1:
            f.error("linkage_derivation_reused_across_analyses",
                    f"{'; '.join(sorted(set(analyses.values())))}: "
                    f"per-analysis parameter reused across analyses "
                    f"{sorted(str(a) for a in analyses)} — two analyses' "
                    f"derivations must correlate neither with each other nor "
                    f"with anything outside them")

    for label, doc in scope.uses:
        issued = issuance_by_id.get(doc.get("derivation_ref"))
        if issued is not None:
            issued_label, issued_doc = issued
            if doc.get("analysis_ref") != issued_doc.get("analysis_ref"):
                f.error("linkage_derivation_reused_across_analyses",
                        f"{label}: exercises derivation "
                        f"{doc.get('derivation_ref')!r} under analysis "
                        f"{doc.get('analysis_ref')!r}, but {issued_label} issued "
                        f"it for {issued_doc.get('analysis_ref')!r} — carrying a "
                        f"derivation into a second analysis and deriving two "
                        f"that agree are the same defect reached two ways")
        # AN UNREADABLE REVOCATION STATE REFUSES THE CORRELATION: an unevaluable
        # answer never reads as permission, and a revoked one refuses on its own
        # terms.
        if doc.get("revocation_state_read") in ("revoked", "unreadable") \
                and doc.get("correlation_performed") is True:
            f.error("linkage_use_with_unreadable_revocation_state",
                    f"{label}: correlation performed against revocation state "
                    f"{doc.get('revocation_state_read')!r} — issuance authorizes "
                    f"and does not immunize; every use answers to the CURRENT "
                    f"revocation state, and a pre-issued derivation is never "
                    f"self-authorizing offline, because that is how a revoked "
                    f"authorization keeps working")


def check_analyses(f: Findings, scope: Scope) -> None:
    correlations_attempted = {doc.get("analysis_ref")
                              for _, doc in scope.uses
                              if doc.get("correlation_performed") is True}
    for label, doc in scope.analyses:
        status = doc.get("status")
        if status is not None and status not in ANALYSIS_STATUSES:
            f.error("analysis_result_status_outside_enumeration",
                    f"{label}: status {status!r} is outside the closed "
                    f"enumeration {sorted(ANALYSIS_STATUSES)} — a status a "
                    f"consumer cannot branch on is a caveat in prose, and a "
                    f"caller branches on a value and never on a paragraph")
        omitted = doc.get("omitted_correlation")
        if status == "correlation_refused":
            if not isinstance(omitted, dict):
                f.error("analysis_result_silently_partial",
                        f"{label}: correlation refused and the result names no "
                        f"omitted correlation — a consumer reads the value it "
                        f"is given and not the circumstance behind it, so a "
                        f"result that merely omits what it could not do will be "
                        f"consumed as a result that had nothing to add")
            else:
                ground = omitted.get("ground")
                if ground is not None and ground not in ANALYSIS_REFUSAL_GROUNDS:
                    f.error("analysis_result_refusal_ground_free_text",
                            f"{label}: omitted correlation ground {ground!r} is "
                            f"not one of {sorted(ANALYSIS_REFUSAL_GROUNDS)} — a "
                            f"ground a validator cannot compare is a ground it "
                            f"cannot check")
        if status == "complete" and not doc.get("correlated_output") \
                and doc.get("analysis_ref") in correlations_attempted:
            f.error("analysis_result_silently_partial",
                    f"{label}: status complete with no correlated output while "
                    f"the corpus records a performed correlation for "
                    f"{doc.get('analysis_ref')!r} — the silently-partial case: "
                    f"the three shapes are decidable apart by the result itself")

        # THE HOOK, NEVER THE STANDARD.
        deid = doc.get("deidentification")
        if isinstance(deid, dict):
            named = deid.get("named_determination_ref")
            if deid.get("claimed") is True and named is None:
                f.error("analysis_result_labelled_deidentified",
                        f"{label}: de-identification claimed with no named "
                        f"determination referenced — plane separation alone "
                        f"does not make one: the attributes that remain can "
                        f"single out a person in combination, and absent the "
                        f"named determination the result remains governed "
                        f"under the same custody as the planes it came from")
            if named is None \
                    and deid.get("remains_governed_personal_data") is False:
                f.error("analysis_result_labelled_deidentified",
                        f"{label}: declares the result no longer governed with "
                        f"no named determination referenced — treating the "
                        f"output as reusable BECAUSE the identity plane was not "
                        f"queried is the same claim as the label, made without "
                        f"the word")
        record_digest_check(f, label, doc, "result_digest")


# --------------------------- conformance declarations ---------------------------

def check_declarations(f: Findings, scope: Scope) -> None:
    for label, doc in scope.declarations:
        reader = get(doc, "realization", "reader_required_check") or {}
        reader_required = reader.get("is_required_in_ruleset") is True
        if not reader_required:
            f.warn("reader-not-required",
                   f"{label}: the canonical reader is not a required check on "
                   f"the repository holding these records "
                   f"(is_required_in_ruleset="
                   f"{reader.get('is_required_in_ruleset')}) — until it is, "
                   f"every record this family defines confers and refuses "
                   f"nothing, and this declaration must keep saying so in the "
                   f"present tense")

        # COVERAGE IN BOTH DIRECTIONS: exactly one entry per obligation, no
        # entry for an obligation this capability does not have.
        entries = [entry for entry in (doc.get("obligations") or [])
                   if isinstance(entry, dict)]
        named = [entry.get("obligation") for entry in entries]
        for obligation in OBLIGATIONS:
            count = named.count(obligation)
            if count != 1:
                f.error("obligation_not_declared",
                        f"{label}: obligation {obligation} is declared {count} "
                        f"time(s); the declaration is closed over the "
                        f"capability's nine obligations with exactly one entry "
                        f"each — a declaration that can quietly omit an "
                        f"obligation is how a silent gap gets recorded as "
                        f"conformance")
        for value in named:
            if value not in OBLIGATIONS:
                f.error("obligation_not_declared",
                        f"{label}: entry names {value!r}, which is not an "
                        f"obligation of this capability")

        for entry in entries:
            obligation = entry.get("obligation")
            satisfaction = entry.get("satisfaction")
            token = entry.get("structural_residual")
            if token is not None \
                    and STRUCTURAL_RESIDUAL_TOKENS.get(token) != obligation:
                f.warn("structural-residual-misfiled",
                       f"{label}: {obligation} carries structural residual "
                       f"{token!r}, which belongs to "
                       f"{STRUCTURAL_RESIDUAL_TOKENS.get(token)}")
            # THE STRUCTURAL RESIDUAL MAY NOT BE RECORDED AS SATISFIED: the step
            # from "declares a salted keyed commitment" to "the anchored value
            # IS one" is not detectable from the record, and it stays open
            # until the realization makes this path the ONLY path that can mint
            # an anchor-bound value.
            if satisfaction == "satisfied" \
                    and (obligation in STRUCTURAL_RESIDUAL_OBLIGATIONS
                         or token is not None):
                f.error("structural_residual_declared_satisfied",
                        f"{label}: {obligation} recorded satisfied over the "
                        f"structural residual "
                        f"{token or 'CA-R5-COMMITMENT-PATH'} — a record "
                        f"declaring a salted keyed construction while anchoring "
                        f"a plain digest is not detectable from the record, and "
                        f"a declaration claiming otherwise is claiming to have "
                        f"read what the bytes cannot say. The residual closes "
                        f"when an undeclared construction is UNREACHABLE, not "
                        f"merely refused")
            elif satisfaction == "satisfied" and obligation == "CA-R5" \
                    and not reader_required:
                f.error("structural_residual_declared_satisfied",
                        f"{label}: CA-R5 recorded satisfied while the refusing "
                        f"validator is not a required check — a boundary whose "
                        f"reader nothing runs is prose, and prose erodes")
            # THE DECLARED-SHORTFALL PATTERN'S OWN ARITHMETIC.
            if satisfaction == "satisfied" and entry.get("declared_residual"):
                f.error("residual-not-declared",
                        f"{label}: {obligation} is recorded satisfied AND "
                        f"carries a declared residual — a residual on a "
                        f"satisfied obligation is a contradiction, and the "
                        f"validator refuses it rather than reading past it")
            if satisfaction in ("partial", "cannot") \
                    and not entry.get("declared_residual"):
                f.error("residual-not-declared",
                        f"{label}: {obligation} is recorded {satisfaction} with "
                        f"no declared residual naming the shortfall and its "
                        f"closing successor — an undeclared shortfall is "
                        f"non-conformance even where the identical shortfall, "
                        f"declared, would be conformant")

        posture = doc.get("realization_posture") or {}

        witnesses = [w for w in (posture.get("witness_configuration") or [])
                     if isinstance(w, dict)]
        if len(witnesses) > 2:
            f.error("third_anchor_target",
                    f"{label}: witness configuration declares {len(witnesses)} "
                    f"anchor targets — the ruled configuration names exactly "
                    f"two, and a third adopted by a realization, an operator or "
                    f"a later author acting alone is refused; no condition is "
                    f"written here under which one would become admissible, "
                    f"since a later ruling answers to its own evidence")
        roles = sorted(str(w.get("role")) for w in witnesses)
        if len(witnesses) == 2 and roles != ["durability", "operational"]:
            f.warn("witness-roles-unbalanced",
                   f"{label}: two witnesses declared with roles {roles}; the "
                   f"ruled pair is one operational and one durability witness")

        if posture.get("per_item_witness_selection") is True:
            f.error("witness_selectivity_rule",
                    f"{label}: per-item witness selection declared — a rule "
                    f"that decides per item which witness that item is worth "
                    f"will eventually decide wrong about the item that matters; "
                    f"the cost argument is answered by aggregation, not by "
                    f"selection")

        claim = posture.get("ten_year_claim_witness") or {}
        role_by_witness = {w.get("witness_id"): w.get("role") for w in witnesses}
        claim_role = claim.get("role") \
            if claim.get("role") is not None \
            else role_by_witness.get(claim.get("witness_id"))
        if claim and claim_role != "durability":
            f.error("ten_year_claim_on_operational_witness",
                    f"{label}: the ten-year claim cites witness "
                    f"{claim.get('witness_id')!r} in role {claim_role!r} — "
                    f"every ten-year claim cites the durability witness; the "
                    f"operational witness's anchor remains valid corroboration "
                    f"of the same fact at a shorter horizon, because 'primary' "
                    f"is order of arrival and never evidentiary weight")

        conditions = posture.get("operational_witness_conditions") or {}
        if conditions.get("inclusion_proof_captured_at_anchor_time") is False:
            f.error("operational_anchor_without_retained_proof",
                    f"{label}: the realization declares operational-witness "
                    f"inclusion proofs are NOT captured at anchor time — the "
                    f"chain prunes its transaction data within days, so a plan "
                    f"to re-derive the proof later is a plan to hold nothing")
        if conditions.get("corroborating_only") is False:
            f.error("claim_stands_on_operational_witness_alone",
                    f"{label}: the operational witness is declared sufficient "
                    f"to stand alone — it is corroborating and never sole, and "
                    f"the promotion in ordering does not soften the pruning "
                    f"finding")
        if conditions.get("archival_node_declared") is False:
            f.warn("archival-node-undeclared",
                   f"{label}: no archival node declared for the operational "
                   f"witness — an adoption condition is a node RUN by the "
                   f"realization, not a plan to run one")

        audit = posture.get("audit_surface") or {}
        if audit.get("logs_permitted_access") is False:
            f.error("served_audit_logs_refusals_only",
                    f"{label}: the served surface logs refusals only — a record "
                    f"of refusals alone answers who was turned away and NOT who "
                    f"actually read, and the question an audit asks first is "
                    f"the second one")
        if audit.get("logs_served_verifications") is False:
            f.error("served_verification_event_unlogged",
                    f"{label}: served verifications are not written as leaves — "
                    f"a served verification, successful or failed, is a logged "
                    f"event, and a failure is recorded as a failure rather than "
                    f"as an absent event")
        if audit.get("independent_verifier_reporting_obligation") is True:
            f.error("reporting_obligation_on_independent_verifiers",
                    f"{label}: a reporting obligation is imposed on independent "
                    f"verifiers — an authenticated call-home trades the "
                    f"receipt's self-sufficiency for a telemetry channel, makes "
                    f"the minter's reachability a precondition of verification "
                    f"again, and turns the who-verified-what trail off a public "
                    f"chain into a trail the minter collects instead. An "
                    f"unobservable verification is the correct outcome, not a "
                    f"defect to instrument away")
        if audit.get("logs_refused_access") is False:
            f.warn("refused-access-unlogged",
                   f"{label}: refused access is not logged on the served "
                   f"surface; the completeness claim is over BOTH answers")

        cadence = posture.get("checkpoint_cadence") or {}
        declared = as_int(cadence.get("declared_seconds"))
        observed = as_int(cadence.get("observed_max_interval_seconds"))
        if declared is not None and observed is not None and observed > declared:
            f.error("checkpoint_cadence_not_met",
                    f"{label}: observed maximum checkpoint interval {observed}s "
                    f"exceeds the declared cadence of {declared}s — anchoring "
                    f"checkpoints less often widens the bracket in which a "
                    f"submission-to-anchor delay could hide, and that is a "
                    f"breach in its own right with its own leaf, so the evasion "
                    f"is a second, independent finding rather than the way out "
                    f"of the delay check")

        if posture.get("delay_check_reading") == "proves_compliance":
            f.error("delay_check_read_as_compliance",
                    f"{label}: the delay check is read as proving compliance — "
                    f"it rests on a LOWER bound: exceeding the declared maximum "
                    f"proves a breach, and falling under it leaves the true "
                    f"delay unknown. Not-provably-breached is not compliant, "
                    f"and the residual is exactly one cadence interval")

        if posture.get("receipt_format") == "single_chain_shaped":
            f.error("receipt_single_chain_shape",
                    f"{label}: the receipt format is declared single-chain "
                    f"shaped — a one-way door, whatever convenience proposes "
                    f"it: anchor targets are added and dropped by changing the "
                    f"per-chain LIST and never the FORMAT")

        if get(posture, "item_anchor_gate", "only_gate_passed_material") is False:
            f.error("item_anchor_over_ungated_material",
                    f"{label}: the item-anchor path admits material no gate "
                    f"passed — the latency saved by anchoring on submission is "
                    f"one aggregation interval and the risk taken is permanent, "
                    f"because a false attestation that reaches a chain cannot "
                    f"be withdrawn")

        if posture.get("attempt_rows_anchored_directly") is True:
            f.error("attempt_row_offered_for_direct_anchoring",
                    f"{label}: per-attempt rows are anchored directly — a "
                    f"per-attempt public trail leaks BY METADATA what the "
                    f"payload rules keep off a chain; batched checkpoints over "
                    f"the attempt leaves are anchored instead")

        neutrality = posture.get("neutrality") or {}
        for record_kind in (neutrality.get("domain_record_kinds") or []):
            f.error("domain_record_kind_in_neutral_family",
                    f"{label}: domain record kind {record_kind!r} declared "
                    f"inside the neutral family — a domain-specific record kind "
                    f"lands in that domain's digest-pinned overlay, and the "
                    f"neutral capability gains no field, code or vocabulary "
                    f"naming the domain")
        for relaxation in (neutrality.get("overlay_relaxations") or []):
            f.error("overlay_relaxes_neutral_refusal",
                    f"{label}: overlay relaxation {relaxation!r} declared — an "
                    f"overlay may ADD refusals and never remove them, which is "
                    f"what the digest pin is for")


# --------------------------- the scope, adjudicated ---------------------------

def validate_scope(f: Findings, records: list[tuple[str, dict]],
                   registry: Registry, docs: dict[str, dict]) -> Scope:
    scope = build_scope(records)
    check_shapes(f, scope, registry, docs)
    check_payload_sweep(f, scope)
    check_receipts(f, scope)
    check_anchor_states(f, scope)
    check_verifications(f, scope)
    check_commitments(f, scope)
    check_checkpoint_anchors(f, scope, docs)
    check_consents(f, scope)
    check_planes(f, scope)
    check_linkage(f, scope)
    check_analyses(f, scope)
    check_declarations(f, scope)
    return scope


# --------------------------- layer 1: packaged corpus ---------------------------

def expected_failure(path: Path) -> tuple[str, str | None]:
    """A negative fixture declares the finding CODE it exists to provoke and MAY
    pin it further with a substring. The detail matters: `schema` is satisfied by
    any schema error whatsoever, so without it a fixture can be mutated into
    testing nothing while its self-test stays green."""
    code = detail = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            code = line.split(":", 1)[1].strip()
        elif line.startswith("# expected_failure_detail:"):
            detail = line.split(":", 1)[1].strip()
    if code is None:
        raise SystemExit(
            f"negative fixture missing '# expected_failure:' header: {path}")
    return code, detail


def codes_of(findings: list[str]) -> set[str]:
    return {match.group(1) for match in
            (re.match(r"ERROR \[([^]]+)]", line) for line in findings) if match}


def lines_for(findings: list[str], code: str) -> list[str]:
    return [line for line in findings if line.startswith(f"ERROR [{code}]")]


def labelled(prefix: str, path: Path) -> list[tuple[str, dict]]:
    records = load_records(path)
    if len(records) == 1:
        return [(f"{prefix}/{path.name}", records[0])]
    return [(f"{prefix}/{path.name}#{index}", doc)
            for index, doc in enumerate(records)]


def positive_records() -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        out.extend(labelled("examples", path))
    return out


def self_test(f: Findings, registry: Registry, docs: dict[str, dict]) -> None:
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return
    base = positive_records()
    if not base:
        f.error("examples-missing", "no packaged positive examples found")
        return
    covered_kinds = {doc.get("kind") for _, doc in base if isinstance(doc, dict)}
    for kind in sorted(set(KIND_TO_SCHEMA) - covered_kinds):
        f.error("examples-missing",
                f"no packaged positive example of kind {kind!r} — a record kind "
                f"no example exercises is a shape nobody has seen conform")
    local = Findings()
    validate_scope(local, base, registry, docs)
    f.errors.extend(f"{line} [expected a valid corpus]" for line in local.errors)
    f.warnings.extend(local.warnings)

    probed: set[str] = set()
    neg_ok = 0
    if not NEGATIVE_DIR.is_dir():
        f.error("examples-missing", f"{NEGATIVE_DIR} not found")
    else:
        for path in sorted(NEGATIVE_DIR.glob("*.yaml")):
            code, detail = expected_failure(path)
            # THE FILENAME IS THE CODE IT TRIGGERS — one fixture per refusal, and
            # the name is the index. A fixture whose name and header disagree is
            # a fixture whose intent nobody can read off the tree listing.
            if path.stem != code:
                f.error("negative-misnamed",
                        f"negative/{path.name}: filename must equal the declared "
                        f"expected_failure code ({code!r})")
            probe = Findings()
            validate_scope(probe, base + labelled("examples/negative", path),
                           registry, docs)
            found = codes_of(probe.errors)
            if not probe.errors:
                f.error("negative-should-fail",
                        f"negative/{path.name}: expected invalid, validated "
                        f"cleanly")
            elif code not in found:
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: expected finding {code!r}, got "
                        f"{sorted(found)}")
            elif detail and not any(detail in line
                                    for line in lines_for(probe.errors, code)):
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: finding {code!r} fired but not "
                        f"for {detail!r} — the fixture no longer tests the "
                        f"invariant it is named for: "
                        f"{lines_for(probe.errors, code)}")
            else:
                neg_ok += 1
                probed.add(code)
    unprobed = sorted(REFUSAL_CODES - probed)
    if unprobed:
        f.error("refusal-code-without-probe",
                f"the closed refusal enumeration declares {unprobed} and no "
                f"packaged negative provokes them. A refusal this reader can "
                f"emit and no fixture ever exercises is a refusal nobody has "
                f"seen work")
    f.note(f"self-test: {len(base)} packaged record(s) validated as ONE coherent "
           f"corpus, {neg_ok} negative fixture(s) confirmed invalid for their "
           f"intended reason, {len(probed & REFUSAL_CODES)}/{len(REFUSAL_CODES)} "
           f"closed refusal codes red-proven "
           f"({len(probed - REFUSAL_CODES)} further finding code(s) probed, for "
           f"the semantic rules whose codes live outside the closed enumeration "
           f"because inventing a member there would be a contract change made "
           f"by a reader)")


# --------------------------- layer 2: real artifacts ---------------------------

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}


def repo_scan(f: Findings, target: Path, registry: Registry,
              docs: dict[str, dict]) -> None:
    sweep = target.is_dir()
    files = sorted(list(target.rglob("*.yaml")) + list(target.rglob("*.yml"))) \
        if sweep else [target]
    records: list[tuple[str, dict]] = []
    checked = skipped = 0
    for path in files:
        if set(path.parts) & SKIP_DIR_NAMES:
            continue
        # Exclude ANY packaged corpus, not only this checkout's: a domain repo
        # that vendors openxFactory scans a COPY, and matching this checkout's
        # absolute paths would re-adjudicate every vendored negative as a live
        # record.
        if "examples" in path.parts and "chain-anchoring" in path.parts:
            continue
        try:
            documents = load_records(path)
        except yaml.YAMLError as exc:
            # A whole-checkout sweep is not the place to adjudicate unrelated
            # YAML: a file that does not parse cannot carry a family kind. An
            # explicitly named file is a different matter.
            if sweep:
                skipped += 1
                continue
            f.error("yaml", f"{path}: parse failure: {exc}")
            continue
        name = str(path.relative_to(target) if sweep else path)
        for index, doc in enumerate(documents):
            if not isinstance(doc, dict) or doc.get("kind") not in KIND_TO_SCHEMA:
                skipped += 1
                continue
            checked += 1
            records.append(
                (name if len(documents) == 1 else f"{name}#{index}", doc))
    if records:
        validate_scope(f, records, registry, docs)
    f.note(f"repo scan ({target}): {checked} artifact(s) checked, {skipped} "
           f"skipped (not a chain-anchoring kind); packaged examples/ excluded "
           f"(layer 1 owns them). ZERO real artifacts is the expected state "
           f"until an anchoring subsystem runs — this realization anchors "
           f"nothing, reaches no chain, and mints no receipt")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-chain-anchoring: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", default=None,
                        help="repo checkout (or single file) to scan for real "
                             "chain-anchoring artifacts; omit to self-test only")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    args = parser.parse_args()

    if not CONTRACT_DIR.is_dir():
        print(f"ERROR {CONTRACT_DIR} not found", file=sys.stderr)
        return 2
    try:
        registry, docs = build_registry()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2

    f = Findings()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")
        if not doc.get("$schema") or not doc.get("$id"):
            f.error("schema-identity-missing",
                    f"{name}: every schema in this family declares its dialect "
                    f"($schema) and an absolute $id, so a consumer's stock "
                    f"validator resolves the bundle the same way this one does")

    # THE FROZEN SET AND THE CONTRACT'S ENUMERATION ARE ONE SET. A code added to
    # either alone is a refusal one of the two readers cannot see, which is the
    # drift a closed enumeration exists to prevent.
    declared = set(get(docs.get("anchoring-definitions.schema.yaml", {}),
                       "$defs", "refusal_code", "enum") or [])
    if declared and declared != REFUSAL_CODES:
        f.error("refusal-enumeration-drift",
                f"the validator's frozen refusal set and the contract's "
                f"enumeration disagree: only in contract "
                f"{sorted(declared - REFUSAL_CODES)}, only in validator "
                f"{sorted(REFUSAL_CODES - declared)}")

    try:
        self_test(f, registry, docs)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, registry, docs)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
