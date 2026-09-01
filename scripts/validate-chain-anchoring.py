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
