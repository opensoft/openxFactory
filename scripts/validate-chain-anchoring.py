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
 14. THE CONFORMANCE DECLARATION — closed over the capability's eleven obligations
     in BOTH directions (`obligation_not_declared`), with the structural residual
     `CA-R5-COMMITMENT-PATH` refused the word `satisfied`
     (`structural_residual_declared_satisfied`), and every realization POSTURE
     member adjudicated against its named refusal.

FIVE FINDINGS CARRY KEBAB-CASE CODES because the closed enumeration has no member
for them and inventing one would be a contract change made by a reader:
`ordering-only-correspondence` (a null header time under a time-bearing rule, or a
time under an ordering-only rule — the same defect pointing opposite ways),
`delay-check-arithmetic` (a bracket that is not a bracket, or a bound that is not
the difference it claims), `checkpoint-anchor-mismatch` (a checkpoint anchor
committing to a digest its own receipt does not carry), `record-digest-mismatch`
(a record digest that does not recompute) and `residual-not-declared` (the
declared-shortfall pattern's own arithmetic: a partial or cannot entry with no
residual, or a satisfied entry carrying one). Each has a packaged negative, on
the same rule as the closed codes — and each negative fixture's FILENAME IS THE
CODE IT PROVOKES, one file per code, so the tree listing is the index of the
refusal enumeration and the self-test refuses a misnamed fixture.

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
    # ADDED BY `amend-chain-anchoring-readiness-and-durability` (requirements 2
    # and 3): the durability profile's six shapes. Eighteen files, one family.
    "confirmation-profile.schema.yaml",
    "confirmation-profile-registry.schema.yaml",
    "daily-merkle-profile.schema.yaml",
    "durability-eligibility-registry.schema.yaml",
    "durability-batch-admission.schema.yaml",
    "durability-batch-manifest.schema.yaml",
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
    "xfactory_chain_anchoring_confirmation_profile":
        "confirmation-profile.schema.yaml",
    "xfactory_chain_anchoring_confirmation_profile_registry":
        "confirmation-profile-registry.schema.yaml",
    "xfactory_chain_anchoring_daily_merkle_profile":
        "daily-merkle-profile.schema.yaml",
    "xfactory_chain_anchoring_durability_eligibility_registry":
        "durability-eligibility-registry.schema.yaml",
    "xfactory_chain_anchoring_durability_batch_admission":
        "durability-batch-admission.schema.yaml",
    "xfactory_chain_anchoring_durability_batch_manifest":
        "durability-batch-manifest.schema.yaml",
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
    # ====================================================================
    # WIDENED BY `amend-chain-anchoring-readiness-and-durability`
    # (requirements 2 and 3) — the same forty-eight the contract's own
    # enumeration declares, in the same order. The two sets are compared
    # set for set at startup, so a code added to one alone is a finding.
    # ====================================================================
    # ---- Fixed UTC windows and the one atomic admission --------------------
    "durability_window_not_fixed_utc_midnight",
    "durability_window_selected_from_source_time",
    "durability_window_reopened_after_close",
    "durability_admission_not_atomic",
    "durability_sequence_inverts_acceptance_partition",
    "durability_event_assigned_to_two_windows",
    "durability_close_watermark_unproven",
    "durability_batch_omits_accepted_event",
    "durability_batch_summary_lowered_below_watermark",
    "durability_event_selectivity_applied",
    "anchoring_control_leaf_admitted_as_event",
    "dedupe_replay_consumed_a_second_sequence",
    "dedupe_key_reused_for_different_content",
    "dedupe_key_reachable_from_anchor",
    "source_time_lateness_recorded_on_chain",
    "empty_window_without_linked_checkpoint",
    "open_window_presented_as_anchored",
    "constituent_event_given_separate_receipt",
    # ---- The eligibility registry and its denominator ----------------------
    "eligibility_boundary_selection_ambiguous",
    "eligibility_activation_applied_to_open_window",
    "eligibility_snapshot_rolled_back",
    "eligibility_terms_substituted_under_version",
    # ---- The released Merkle construction and the continuity link ----------
    "merkle_profile_absent_or_substituted",
    "daily_batch_root_not_reproducible",
    "daily_continuity_link_unresolved",
    "daily_continuity_link_over_batch_root",
    "first_daily_manifest_without_genesis_sentinel",
    # ---- One item, one root, both witnesses --------------------------------
    "daily_item_witness_roots_differ",
    "aggregation_root_not_identity_for_daily_item",
    "witness_commitment_path_absent",
    "durability_witness_proof_over_raw_batch_root",
    "daily_manifest_configuration_substituted",
    # ---- The confirmation-profile registry ---------------------------------
    "confirmation_profile_unresolved",
    "confirmation_profile_not_operator_approved",
    "confirmation_profile_numeric_depth_uncited",
    "confirmation_profile_snapshot_rolled_back",
    "confirmation_profile_activation_applied_to_open_window",
    "confirmation_profile_terms_substituted_under_version",
    "confirmation_profile_retired_or_compromised_mints_receipt",
    "confirmation_profile_standing_rewrites_historical_receipt",
    "registry_history_rewritten",
    # ---- Submitted is not confirmed ----------------------------------------
    "witness_confirmed_without_profile_condition",
    "witness_confirmed_without_named_profile",
    "witness_pending_with_submission_evidence",
    "submission_evidence_offered_as_confirmed",
    "long_horizon_claim_on_unupgraded_durability_proof",
    "reorganized_witness_retains_confirmed_label",
    "state_transition_history_erased_on_upgrade",
})

# The capability's ELEVEN obligations, in the deltas' own order: nine from
# `add-chain-anchoring` and two from
# `amend-chain-anchoring-readiness-and-durability`, whose own `tasks.md` 3.2
# counts "all eleven promoted requirements". A declaration enumerating nine
# after the amendment ratified would be silent on two obligations, which is
# exactly what `obligation_not_declared` refuses.
OBLIGATIONS = ["CA-R1", "CA-R2", "CA-R3", "CA-R4", "CA-R5", "CA-R6",
               "CA-R7", "CA-R8", "CA-R9", "CA-R10", "CA-R11"]

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
    # THE CONFIRMATION PROFILE IS A RECEIPT-ONLY INPUT AND JOINS THIS SET BY THE
    # RULE, not by an enumeration chase — which is the rule the block's own
    # header says a future timing input joins by. What separates submitted from
    # confirmed is the profile's objective condition, so a verifier reads it,
    # so it lives inside the committed block and nowhere else.
    "confirmation_profile",
})

# THE STATE VOCABULARY THE RECEIPT MAY NOT CARRY. The receipt holds proof material
# and never state; a witness still in flight is recorded in the anchor-state
# record, which is where every surface reads per-witness status.
ANCHOR_STATE_VOCABULARY = frozenset({
    "anchored", "anchor_status", "pending", "complete", "state", "status",
    "anchor_state", "witness_status",
    # `landed` and `in_flight` were this list's words for the per-witness
    # states; `amend-chain-anchoring-readiness-and-durability` replaced that
    # enumeration, so the vocabulary the RECEIPT may not carry moves with it.
    # `confirmed_under_profile` and `commitment_derivation` are receipt members
    # by design and are not caught here, because this sweep is exact-match: it
    # refuses a member NAMED for a state, never one whose name contains a word.
    "submitted", "confirmed", "unevaluable",
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
    profiles: list[tuple[str, dict]] = field(default_factory=list)
    profile_registries: list[tuple[str, dict]] = field(default_factory=list)
    merkle_profiles: list[tuple[str, dict]] = field(default_factory=list)
    eligibility_registries: list[tuple[str, dict]] = field(default_factory=list)
    admissions: list[tuple[str, dict]] = field(default_factory=list)
    manifests: list[tuple[str, dict]] = field(default_factory=list)
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
    "xfactory_chain_anchoring_confirmation_profile": "profiles",
    "xfactory_chain_anchoring_confirmation_profile_registry": "profile_registries",
    "xfactory_chain_anchoring_daily_merkle_profile": "merkle_profiles",
    "xfactory_chain_anchoring_durability_eligibility_registry":
        "eligibility_registries",
    "xfactory_chain_anchoring_durability_batch_admission": "admissions",
    "xfactory_chain_anchoring_durability_batch_manifest": "manifests",
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
                        if row.get("status") != "confirmed"]
            if not doc.get("receipt_ref"):
                f.error("anchor_state_complete_without_captured_receipt",
                        f"{label}: state anchor_complete with no captured receipt "
                        f"referenced — completion is the captured multi-anchor "
                        f"receipt holding every configured witness's four "
                        f"elements, and nothing else is that")
            if unlanded:
                f.error("anchor_state_complete_without_captured_receipt",
                        f"{label}: state anchor_complete while witness(es) "
                        f"{unlanded} are not confirmed — a completeness claim over a "
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
            if row.get("status") in ("pending", "submitted") and facts is not None \
                    and (wid in facts.entry_witnesses
                         or row.get("chain_id") in facts.entry_chains):
                f.error("receipt_entry_incomplete_for_pending_witness",
                        f"{where}: this witness is recorded {row.get('status')!r} "
                        f"— no confirmation evidence yet — while "
                        f"the referenced receipt already carries a per-chain "
                        f"entry for it — a receipt entry exists only once the "
                        f"four elements are captured whole; a witness that is "
                        f"pending or merely submitted is a pending proof held "
                        f"HERE, and the later upgrade appends a whole entry")

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
                        f"capability's eleven obligations with exactly one entry "
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


# --------------------------- the durability profile ---------------------------

# THE FIVE THINGS THE ONE ATOMIC ADMISSION TRANSACTION DOES. Enumerated so a
# realization that performed four of them is refused FOR THE ONE IT SKIPPED,
# which is a more useful answer than "not atomic".
ADMISSION_STEPS = (
    "validate_eligibility",
    "apply_dedupe_rule",
    "record_acceptance_time",
    "select_window_from_acceptance_time",
    "assign_next_leaf_sequence",
)

# THE CONTRACT-DEFINED SENTINEL THE FIRST DAILY MANIFEST BINDS. Held here as the
# set the corpus must match, and compared against the contract's own `const` at
# startup, for the same reason the refusal enumeration is compared: a sentinel a
# reader and a contract spell differently is a first manifest neither can agree
# on.
DAILY_GENESIS_SENTINEL = "xfactory-chain-anchoring-daily-genesis-v1"

WINDOW_SECONDS = 86400

# THE CONSTRUCTION CHOICES THIS READER CAN MECHANICALLY RECOMPUTE UNDER. The
# amendment obliges the canonical validator to "resolve the pinned released
# profile and mechanically recompute every leaf, membership path, and
# `daily_batch_root`" — so a released profile whose declared ordering or shape
# this reader cannot reproduce DETERMINISTICALLY is refused rather than accepted
# on the strength of a root nobody can check. `acceptance_time_ascending` is
# refused for a stated reason and not for convenience: timestamps tie, a tie has
# no deterministic tiebreak, and a batch two builders can order differently is a
# batch whose root proves nothing.
RECOMPUTABLE_ORDERINGS = frozenset({"leaf_sequence_ascending"})
RECOMPUTABLE_SHAPES = frozenset({"binary_left_complete"})
RECOMPUTABLE_ODD_HANDLING = frozenset({"promote_unpaired_node",
                                       "duplicate_unpaired_node"})


def _midnight(value: Any) -> datetime | None:
    """The instant, only if it is a UTC midnight. The windows of this profile run
    from `00:00:00Z` inclusive to the next `00:00:00Z` exclusive, and a boundary
    that is not one of them is refused BY NAME rather than made unrepresentable
    by a pattern — a regex error saying a string did not match says nothing about
    which fixed window was meant."""
    moment = instant(value)
    if moment is None:
        return None
    if (moment.hour, moment.minute, moment.second, moment.microsecond) != (0, 0, 0, 0):
        return None
    return moment


def _leaf_node(construction: dict, leaf_value: Any) -> str:
    """One event leaf's tree node, domain-separated. The composition is under the
    estate's ONE digest construction — the separator travels INSIDE the canonical
    JSON — so this tranche mints no second hashing rule to reach a Merkle tree."""
    return canonical.digest({"domain": construction.get("leaf_domain_separator"),
                             "leaf": leaf_value})


def _internal_node(construction: dict, left: str, right: str) -> str:
    return canonical.digest({"domain": construction.get("node_domain_separator"),
                             "left": left, "right": right})


def _fold(construction: dict, level: list[str]) -> tuple[list[str], bool]:
    nxt = [_internal_node(construction, level[i], level[i + 1])
           for i in range(0, len(level) - 1, 2)]
    promoted = len(level) % 2 == 1
    if promoted:
        if construction.get("odd_node_handling") == "duplicate_unpaired_node":
            nxt.append(_internal_node(construction, level[-1], level[-1]))
            promoted = False
        else:
            nxt.append(level[-1])
    return nxt, promoted


def _batch_root(construction: dict, leaf_values: list[Any]) -> str | None:
    if not leaf_values:
        return digest_value(get(construction, "empty_root"))
    level = [_leaf_node(construction, v) for v in leaf_values]
    while len(level) > 1:
        level, _ = _fold(construction, level)
    return level[0]


def _membership_path(construction: dict, leaf_values: list[Any],
                     index: int) -> list[dict]:
    level = [_leaf_node(construction, v) for v in leaf_values]
    idx, path = index, []
    while len(level) > 1:
        nxt, promoted = _fold(construction, level)
        if idx == len(level) - 1 and promoted:
            idx = len(nxt) - 1
        else:
            sibling = idx + 1 if idx % 2 == 0 else idx - 1
            path.append({"position": "right" if idx % 2 == 0 else "left",
                         "value": level[sibling]})
            idx //= 2
        level = nxt
    return path


@dataclass
class DurabilityIndex:
    """What the durability records establish ABOUT EACH OTHER, derived once.

    Every cross-record rule of this profile is a property of a SET and not of a
    document — a denominator two admissions of one window disagree about, a
    registry version a snapshot rolled back to, a daily item whose predecessor
    is missing — so the comparisons are made here, over the whole scope, and
    never inferred from one record."""
    profile_terms: dict = field(default_factory=dict)      # (pid, ver) -> digest
    profile_entries: dict = field(default_factory=dict)    # (chain,pid,ver) -> entry
    active_profile: dict = field(default_factory=dict)     # chain -> entry
    registries: list = field(default_factory=list)
    merkle: dict = field(default_factory=dict)             # (pid, ver) -> record
    eligibility: dict = field(default_factory=dict)        # (rid, eid) -> entry
    active_eligibility: dict = field(default_factory=dict)  # rid -> entry
    admissions_by_window: dict = field(default_factory=dict)
    manifests: list = field(default_factory=list)


def _build_durability_index(scope: Scope) -> DurabilityIndex:
    idx = DurabilityIndex()
    for _, doc in scope.profiles:
        idx.profile_terms[(doc.get("profile_id"), doc.get("version"))] = doc
    for label, doc in scope.profile_registries:
        idx.registries.append((label, doc))
        for entry in (doc.get("entries") or []):
            if not isinstance(entry, dict):
                continue
            key = (entry.get("chain_id"), entry.get("profile_id"),
                   entry.get("version"))
            idx.profile_entries[key] = entry
            if entry.get("standing") == "active":
                chain = entry.get("chain_id")
                current = idx.active_profile.get(chain)
                seq = as_int(get(entry, "activation", "log_sequence")) or 0
                if current is None \
                        or seq > (as_int(get(current, "activation",
                                             "log_sequence")) or 0):
                    idx.active_profile[chain] = entry
    for _, doc in scope.merkle_profiles:
        idx.merkle[(doc.get("profile_id"), doc.get("version"))] = doc
    for _, doc in scope.eligibility_registries:
        rid = doc.get("registry_id")
        for entry in (doc.get("entries") or []):
            if not isinstance(entry, dict):
                continue
            idx.eligibility[(rid, entry.get("entry_id"))] = entry
            if entry.get("standing") == "active":
                current = idx.active_eligibility.get(rid)
                seq = as_int(get(entry, "activation", "log_sequence")) or 0
                if current is None \
                        or seq > (as_int(get(current, "activation",
                                             "log_sequence")) or 0):
                    idx.active_eligibility[rid] = entry
    for label, doc in scope.admissions:
        idx.admissions_by_window.setdefault(doc.get("window_open"), []) \
            .append((label, doc))
    idx.manifests = sorted(
        scope.manifests,
        key=lambda pair: str(get(pair[1], "terms", "window_open") or ""))
    return idx


def _check_window(f: Findings, label: str, open_value: Any, close_value: Any
                  ) -> tuple[datetime | None, datetime | None]:
    opened, closed = _midnight(open_value), _midnight(close_value)
    if opened is None or closed is None:
        f.error("durability_window_not_fixed_utc_midnight",
                f"{label}: window {open_value!r}..{close_value!r} is not a fixed "
                f"UTC window — the profile divides time into consecutive "
                f"non-overlapping windows from 00:00:00Z inclusive to the next "
                f"00:00:00Z exclusive, and a boundary chosen anywhere else is a "
                f"window an owner can move")
        return opened, closed
    if seconds_between(closed, opened) != WINDOW_SECONDS:
        f.error("durability_window_not_fixed_utc_midnight",
                f"{label}: window spans "
                f"{int(seconds_between(closed, opened))}s rather than "
                f"{WINDOW_SECONDS}s — consecutive fixed windows tile time exactly "
                f"once, and an interval of any other width either overlaps its "
                f"neighbour or leaves a gap no manifest accounts for")
    return opened, closed


def _resolve_merkle(f: Findings, label: str, snapshot: Any,
                    idx: DurabilityIndex) -> dict | None:
    """The released construction this record binds, resolved and digest-checked."""
    if not isinstance(snapshot, dict):
        f.error("merkle_profile_absent_or_substituted",
                f"{label}: no daily-Merkle profile reference — an admission or "
                f"manifest that names no construction has made no membership or "
                f"completeness claim a verifier can recompute")
        return None
    key = (snapshot.get("profile_id"), snapshot.get("version"))
    record = idx.merkle.get(key)
    if record is None:
        f.warn("merkle-profile-not-in-scope",
               f"{label}: daily-Merkle profile {key} is not among the records in "
               f"scope, so its construction could not be resolved; the digest it "
               f"binds is checked when the released profile travels with it")
        return None
    carried = digest_value(snapshot.get("canonical_digest"))
    recomputed = canonical.digest(record.get("construction"))
    if carried != recomputed:
        f.error("merkle_profile_absent_or_substituted",
                f"{label}: the bound daily-Merkle digest {carried} does not "
                f"recompute over the released construction of {key} "
                f"({recomputed}) — a substituted construction changes every leaf "
                f"and every path while leaving the root's shape untouched, which "
                f"is why the digest is checked BEFORE any membership claim")
        return None
    return record.get("construction")


def _resolve_eligibility(f: Findings, label: str, snapshot: Any,
                         idx: DurabilityIndex, window_open: datetime | None
                         ) -> None:
    if not isinstance(snapshot, dict):
        return
    key = (snapshot.get("registry_id"), snapshot.get("entry_id"))
    entry = idx.eligibility.get(key)
    if entry is None:
        f.warn("eligibility-entry-not-in-scope",
               f"{label}: eligibility entry {key} is not among the records in "
               f"scope; its digest and standing are checked when the register "
               f"travels with the records that snapshot it")
        return
    if digest_value(snapshot.get("canonical_digest")) \
            != digest_value(entry.get("canonical_digest")):
        f.error("eligibility_terms_substituted_under_version",
                f"{label}: the snapshotted eligibility digest disagrees with the "
                f"append-only register's entry {key} — supplying different terms "
                f"under an approved version is how a denominator is changed after "
                f"the counting started, and it is refused before the batch root "
                f"can be accepted")
    if snapshot.get("version") != entry.get("version") \
            or snapshot.get("standing") != entry.get("standing"):
        f.error("eligibility_terms_substituted_under_version",
                f"{label}: the snapshot declares version "
                f"{snapshot.get('version')!r}/standing "
                f"{snapshot.get('standing')!r} where the register's entry {key} "
                f"carries {entry.get('version')!r}/{entry.get('standing')!r} — "
                f"the register is the authority and a disagreement is refused "
                f"rather than either preferred")
    active = idx.active_eligibility.get(snapshot.get("registry_id"))
    if entry.get("standing") in ("retired", "compromised") and active is not None \
            and active.get("entry_id") != entry.get("entry_id"):
        f.error("eligibility_snapshot_rolled_back",
                f"{label}: the window snapshotted retired eligibility entry "
                f"{entry.get('entry_id')!r} while {active.get('entry_id')!r} "
                f"stands active with the greater activation checkpoint — a "
                f"rollback is exactly how a minter would shrink a denominator "
                f"after the fact, so window opening is refused as eligibility "
                f"rollback")
    if window_open is not None:
        effective = instant(get(entry, "effective_interval", "from_window_open"))
        if effective is not None and effective > window_open:
            f.error("eligibility_activation_applied_to_open_window",
                    f"{label}: eligibility entry {entry.get('entry_id')!r} takes "
                    f"effect at the window opening "
                    f"{effective.isoformat()} but is bound to the window that "
                    f"opened {window_open.isoformat()} — an activation during an "
                    f"open window applies to the NEXT window; a denominator that "
                    f"widens mid-count makes the count meaningless in both "
                    f"directions")
        until = instant(get(entry, "effective_interval", "until_window_open"))
        if until is not None and until <= window_open:
            f.error("eligibility_snapshot_rolled_back",
                    f"{label}: eligibility entry {entry.get('entry_id')!r} ceased "
                    f"to be effective at {until.isoformat()}, before this window "
                    f"opened at {window_open.isoformat()} — the interval is "
                    f"half-open, and a boundary outside it is not this entry's to "
                    f"answer for")


def check_confirmation_profiles(f: Findings, scope: Scope) -> None:
    """THE APPROVED TERMS, RECOMPUTED, AND THE DEPTH THAT MUST BE CITED."""
    for label, doc in scope.profiles:
        terms = doc.get("terms")
        carried = digest_value(doc.get("canonical_digest"))
        if isinstance(terms, dict) and carried:
            recomputed = canonical.digest(terms)
            if carried != recomputed:
                f.error("confirmation_profile_terms_substituted_under_version",
                        f"{label}: the profile's own canonical digest {carried} "
                        f"does not recompute over its `terms` ({recomputed}) — "
                        f"the digest a registry entry binds is over the TERMS and "
                        f"over nothing else, so a record whose two halves "
                        f"disagree is refused before any registry entry is "
                        f"consulted")
        confirmed = get(doc, "terms", "confirmed_condition") or {}
        if confirmed.get("numeric_depth") is not None \
                and not confirmed.get("numeric_depth_citation"):
            f.error("confirmation_profile_numeric_depth_uncited",
                    f"{label}: the confirmation condition names a numeric depth "
                    f"of {confirmed.get('numeric_depth')!r} with no citation — "
                    f"*\"This specification MUST NOT invent an unsupported "
                    f"numeric confirmation depth\"*, and a depth with nothing "
                    f"cited behind it is a number somebody chose about another "
                    f"chain's consensus rules")
        vectors = [v for v in (get(doc, "terms", "transition_vectors") or [])
                   if isinstance(v, dict)]
        expectations = {v.get("expectation") for v in vectors}
        if not {"accept", "refuse"} <= expectations:
            f.error("profile-transition-vectors-incomplete",
                    f"{label}: the approved terms carry expectations "
                    f"{sorted(x for x in expectations if x)} — the amendment "
                    f"requires POSITIVE AND REFUSAL vectors at the transition "
                    f"boundaries, and a profile with only one direction has never "
                    f"been shown to refuse anything")


def check_profile_registries(f: Findings, scope: Scope,
                             idx: DurabilityIndex) -> None:
    """APPEND-ONLY, AND DETERMINISTIC SELECTION OR NO WINDOW OPENS."""
    for label, doc in idx.registries:
        if get(doc, "append_only", "history_rewritten") is True \
                or get(doc, "append_only", "append_only") is False:
            f.error("registry_history_rewritten",
                    f"{label}: the register declares its history rewritten "
                    f"(append_only="
                    f"{get(doc, 'append_only', 'append_only')!r}, "
                    f"history_rewritten="
                    f"{get(doc, 'append_only', 'history_rewritten')!r}) — a "
                    f"register whose past can be edited cannot show that a "
                    f"rollback did not happen, which is the one thing it exists "
                    f"to show")
        entries = [e for e in (doc.get("entries") or []) if isinstance(e, dict)]
        for chain in (doc.get("configured_networks") or []):
            active = [e for e in entries
                      if e.get("chain_id") == chain and e.get("standing") == "active"]
            if not active:
                f.error("confirmation_profile_unresolved",
                        f"{label}: configured network {chain!r} has no entry with "
                        f"standing `active` — with either profile unresolved, "
                        f"schema and validator authoring stays BLOCKED rather "
                        f"than leaving finality to an implementer, and this "
                        f"register is where that is measured rather than assumed")
                continue
            if len(active) > 1:
                overlapping = sorted(e.get("entry_id") for e in active)
                f.error("confirmation_profile_unresolved",
                        f"{label}: configured network {chain!r} has "
                        f"{len(active)} active entries {overlapping} — selection "
                        f"at window open must be DETERMINISTIC, and a register "
                        f"that cannot name one version per witness leaves the "
                        f"window with no answer to give later about what it was "
                        f"measuring")
        by_profile: dict[Any, list[dict]] = {}
        for entry in entries:
            by_profile.setdefault((entry.get("chain_id"), entry.get("profile_id")),
                                  []).append(entry)
        for key, group in by_profile.items():
            ordered = sorted(group, key=lambda e: as_int(e.get("version")) or 0)
            for older, newer in zip(ordered, ordered[1:]):
                if not newer.get("predecessor_entry_id"):
                    f.error("registry-entry-predecessor-unresolved",
                            f"{label}: entry {newer.get('entry_id')!r} for {key} "
                            f"is version {newer.get('version')!r} and names no "
                            f"predecessor — a version chain with a hole in it "
                            f"cannot prove a rollback did not happen")
                if older.get("standing") == "active" \
                        and newer.get("standing") == "active":
                    f.error("confirmation_profile_unresolved",
                            f"{label}: entries {older.get('entry_id')!r} and "
                            f"{newer.get('entry_id')!r} are both active for "
                            f"{key} — activating a successor closes its "
                            f"predecessor's interval in the SAME act, so two "
                            f"active versions is a register that did not perform "
                            f"the activation it recorded")
            for entry in ordered:
                if entry.get("standing") in ("retired", "compromised") \
                        and not get(entry, "effective_interval",
                                    "until_window_open"):
                    f.warn("registry-retired-interval-open",
                           f"{label}: entry {entry.get('entry_id')!r} stands "
                           f"{entry.get('standing')!r} with an open effective "
                           f"interval; activating a successor closes the "
                           f"predecessor's interval, and an open one leaves the "
                           f"boundary readable two ways")
        for entry in entries:
            # THE APPROVAL IS A FACT ABOUT THE ENTRY AND NOT ABOUT THE PROFILE.
            # A profile record says what the rule IS; the register says who
            # approved it and when it applies, which is why the operator check
            # lives here. `implementer` and `unattributed` are writable in the
            # shared `approval_record` precisely so this refusal has a fixture:
            # an implementer-approved profile is finality left to an implementer
            # under a different name.
            if get(entry, "approval", "approved_by") != "operator":
                f.error("confirmation_profile_not_operator_approved",
                        f"{label}: entry {entry.get('entry_id')!r} records "
                        f"approval by "
                        f"{get(entry, 'approval', 'approved_by')!r} — the "
                        f"amendment requires the OPERATOR to approve what "
                        f"distinguishes submitted from confirmed before any "
                        f"schema or validator rests on it")
            record = idx.profile_terms.get((entry.get("profile_id"),
                                            entry.get("version")))
            if record is None:
                continue
            if digest_value(entry.get("canonical_digest")) \
                    != digest_value(record.get("canonical_digest")):
                f.error("confirmation_profile_terms_substituted_under_version",
                        f"{label}: entry {entry.get('entry_id')!r} binds a digest "
                        f"that is not the released profile's own — the terms were "
                        f"substituted under an approved id and version, and "
                        f"verification refuses the receipt rather than evaluating "
                        f"the substituted rule")


def check_merkle_profiles(f: Findings, scope: Scope) -> None:
    """THE CONSTRUCTION, DIGESTED, SEPARATED, AND RECOMPUTABLE."""
    for label, doc in scope.merkle_profiles:
        construction = doc.get("construction")
        carried = digest_value(doc.get("canonical_digest"))
        if isinstance(construction, dict) and carried:
            recomputed = canonical.digest(construction)
            if carried != recomputed:
                f.error("merkle_profile_absent_or_substituted",
                        f"{label}: the released profile's own digest {carried} "
                        f"does not recompute over its `construction` "
                        f"({recomputed}) — every admission and manifest binds "
                        f"this value, so a record whose halves disagree is a "
                        f"substitution nobody downstream could detect")
        if isinstance(construction, dict):
            if construction.get("leaf_domain_separator") \
                    == construction.get("node_domain_separator"):
                f.error("merkle-domain-separators-equal",
                        f"{label}: the leaf and internal-node domain separators "
                        f"are the same string — without separation a leaf digest "
                        f"can be presented as an internal node, and a "
                        f"second-preimage substitution becomes available inside a "
                        f"valid-looking membership path")
            if construction.get("ordering") not in RECOMPUTABLE_ORDERINGS \
                    or construction.get("tree_shape") not in RECOMPUTABLE_SHAPES \
                    or construction.get("odd_node_handling") \
                    not in RECOMPUTABLE_ODD_HANDLING:
                f.error("daily_batch_root_not_reproducible",
                        f"{label}: the released construction declares ordering "
                        f"{construction.get('ordering')!r}, shape "
                        f"{construction.get('tree_shape')!r} and odd-node "
                        f"handling {construction.get('odd_node_handling')!r}, "
                        f"which this canonical reader cannot reproduce "
                        f"deterministically — the amendment obliges the validator "
                        f"to recompute every leaf, path and root, and a root no "
                        f"validator can recompute is a number rather than a proof")
        if get(doc, "approval", "approved_by") != "operator":
            f.warn("merkle-profile-not-operator-approved",
                   f"{label}: the released construction records approval by "
                   f"{get(doc, 'approval', 'approved_by')!r}; the amendment asks "
                   f"the operator to release it before schema authoring rests on "
                   f"it")


def check_eligibility_registries(f: Findings, scope: Scope,
                                 idx: DurabilityIndex) -> None:
    """THE DENOMINATOR, APPEND-ONLY, AND CONTROL LEAVES OUTSIDE THE COUNT."""
    for label, doc in scope.eligibility_registries:
        if get(doc, "append_only", "history_rewritten") is True \
                or get(doc, "append_only", "append_only") is False:
            f.error("registry_history_rewritten",
                    f"{label}: the eligibility register declares its history "
                    f"rewritten — the denominator's whole authority is that it "
                    f"cannot be edited after the windows that counted against it")
        entries = [e for e in (doc.get("entries") or []) if isinstance(e, dict)]
        active = [e for e in entries if e.get("standing") == "active"]
        if len(active) != 1:
            f.error("eligibility_boundary_selection_ambiguous",
                    f"{label}: {len(active)} entries stand active — at each UTC "
                    f"window open exactly ONE entry with standing `active` whose "
                    f"effective interval contains the boundary is selected, and "
                    f"zero or several is refused: no event is admitted under an "
                    f"ambiguous denominator")
        for entry in entries:
            terms = entry.get("terms")
            carried = digest_value(entry.get("canonical_digest"))
            if isinstance(terms, dict) and carried:
                recomputed = canonical.digest(terms)
                if carried != recomputed:
                    f.error("eligibility_terms_substituted_under_version",
                            f"{label}: entry {entry.get('entry_id')!r} binds "
                            f"{carried} which does not recompute over its own "
                            f"terms ({recomputed})")
            excluded = get(entry, "terms", "excluded_leaf_classes") or []
            if "anchoring_control" not in excluded:
                f.error("anchoring_control_leaf_admitted_as_event",
                        f"{label}: entry {entry.get('entry_id')!r} does not "
                        f"exclude `anchoring_control` from the count — an "
                        f"eligibility set that counts its own control leaves "
                        f"produces a batch that must contain the manifest "
                        f"describing it, which is a regress rather than a fixed "
                        f"point, and it also makes a genuinely empty window "
                        f"impossible")
            if get(entry, "approval", "approved_by") != "operator":
                f.warn("eligibility-entry-not-operator-approved",
                       f"{label}: entry {entry.get('entry_id')!r} records "
                       f"approval by "
                       f"{get(entry, 'approval', 'approved_by')!r}")
        by_version = sorted(entries, key=lambda e: as_int(e.get("version")) or 0)
        for older, newer in zip(by_version, by_version[1:]):
            if older.get("standing") == "active" and newer.get("standing") == "active":
                f.error("eligibility_boundary_selection_ambiguous",
                        f"{label}: entries {older.get('entry_id')!r} and "
                        f"{newer.get('entry_id')!r} are both active — activating "
                        f"a successor closes its predecessor's interval and marks "
                        f"it retired in the same atomic act")


def check_admissions(f: Findings, scope: Scope, idx: DurabilityIndex) -> None:
    """ONE ATOMIC ADMISSION, ONE WINDOW, ONE SEQUENCE, EXACTLY ONCE."""
    seen_leaf: dict[Any, tuple[str, Any]] = {}
    dedupe_material: dict[Any, tuple[str, Any]] = {}
    ordered: list[tuple[str, dict, datetime, int]] = []

    for label, doc in scope.admissions:
        opened, closed = _check_window(f, label, doc.get("window_open"),
                                       doc.get("window_close"))
        accepted = instant(doc.get("trusted_acceptance_time"))
        source = instant(doc.get("owner_source_time"))
        rule = doc.get("late_arrival_rule") or {}

        if rule.get("window_selected_from") != "trusted_acceptance_time":
            f.error("durability_window_selected_from_source_time",
                    f"{label}: the declared rule selects the window from "
                    f"{rule.get('window_selected_from')!r} — owner source time is "
                    f"DESCRIPTIVE ONLY and must not select or reopen a window, "
                    f"because a window a source time can select is a window an "
                    f"owner can reopen by backdating")
        if rule.get("source_time_lateness_recorded") in ("on_chain",
                                                         "in_daily_manifest"):
            f.error("source_time_lateness_recorded_on_chain",
                    f"{label}: source-time lateness is recorded "
                    f"{rule.get('source_time_lateness_recorded')!r} — the "
                    f"amendment records lateness OFF CHAIN; a per-event lateness "
                    f"value that reaches a public chain leaks by metadata what "
                    f"the payload rules keep off it, and it does so permanently")

        if opened is not None and closed is not None and accepted is not None:
            if not (opened <= accepted < closed):
                if source is not None and opened <= source < closed:
                    f.error("durability_window_selected_from_source_time",
                            f"{label}: trusted acceptance "
                            f"{accepted.isoformat()} falls outside the declared "
                            f"window while the OWNER SOURCE TIME "
                            f"{source.isoformat()} falls inside it — the window "
                            f"was selected from the descriptive clock, which is "
                            f"the one clock that may never select one")
                else:
                    f.error("admission-window-acceptance-mismatch",
                            f"{label}: trusted acceptance "
                            f"{accepted.isoformat()} does not fall in the "
                            f"half-open declared window "
                            f"[{opened.isoformat()}, {closed.isoformat()}) — "
                            f"acceptance selects the window, so a record whose "
                            f"two halves disagree names no window at all")

        transaction = doc.get("admission_transaction") or {}
        steps = set(transaction.get("steps") or [])
        missing = [step for step in ADMISSION_STEPS if step not in steps]
        if transaction.get("atomic") is not True or missing:
            f.error("durability_admission_not_atomic",
                    f"{label}: the admission declares atomic="
                    f"{transaction.get('atomic')!r} and omits {missing or 'nothing'} "
                    f"from the one transaction — validation, the dedupe rule, the "
                    f"acceptance timestamp, the window selection and the sequence "
                    f"assignment are ONE transaction, and split into steps that "
                    f"can each succeed alone every interleaving is a way for an "
                    f"event to be counted twice or not at all")

        if doc.get("leaf_class") == "anchoring_control":
            f.error("anchoring_control_leaf_admitted_as_event",
                    f"{label}: an `anchoring_control` leaf is offered as a "
                    f"durability-eligible event — a witness submission, a "
                    f"confirmation, a batch manifest or a continuity checkpoint "
                    f"stays covered by the signed log and its checkpoint anchors "
                    f"and is OUTSIDE the event count; admitting one to the batch "
                    f"it produces is recursive")

        rule_d = doc.get("dedupe_rule") or {}
        if rule_d.get("on_identical_replay") == "assign_second_sequence":
            f.error("dedupe_replay_consumed_a_second_sequence",
                    f"{label}: the declared dedupe rule assigns a SECOND sequence "
                    f"on identical replay — replay of the same key with the same "
                    f"material returns the EXISTING leaf and sequence, because an "
                    f"idempotent producer replaying is normal and a second "
                    f"sequence for one event is exactly-once accounting lost")
        if rule_d.get("on_key_reuse_with_different_material") == "admit_second_leaf":
            f.error("dedupe_key_reused_for_different_content",
                    f"{label}: the declared dedupe rule admits a second leaf when "
                    f"a key is reused for DIFFERENT material — reuse with a "
                    f"different digest is REFUSED before sequence assignment, "
                    f"because a key replayed over different content is a "
                    f"different event wearing the same handle")
        custody = get(rule_d, "key_custody", "resolves_into")
        if custody is not None and custody != GOVERNED_CUSTODY:
            f.error("dedupe_key_reachable_from_anchor",
                    f"{label}: the dedupe key's custody resolves into "
                    f"{custody!r} — the key is owner-local and STABLE, which "
                    f"makes it a correlation handle the moment it is reachable "
                    f"from an anchor; the amendment keeps it off public chains")
        if rule_d.get("key_scope") in ("global_public", "chain_visible"):
            f.error("dedupe_key_reachable_from_anchor",
                    f"{label}: the dedupe key's scope is "
                    f"{rule_d.get('key_scope')!r} — a globally public or "
                    f"chain-visible dedupe key is the same reachability by a "
                    f"different route")

        if doc.get("admission_kind") == "replay_acknowledgement":
            replayed = as_int(doc.get("replay_of_leaf_sequence"))
            if replayed is None or replayed != as_int(doc.get("leaf_sequence")):
                f.error("dedupe_replay_consumed_a_second_sequence",
                        f"{label}: a replay acknowledgement returns sequence "
                        f"{doc.get('leaf_sequence')!r} while naming "
                        f"{doc.get('replay_of_leaf_sequence')!r} as the existing "
                        f"one — the acknowledgement returns the EXISTING leaf, so "
                        f"a record where the two differ is the second admission "
                        f"the dedupe rule was there to prevent")
        if doc.get("pre_closure_anchor_receipt_ref"):
            f.error("constituent_event_given_separate_receipt",
                    f"{label}: the admission carries a pre-closure anchor receipt "
                    f"{doc.get('pre_closure_anchor_receipt_ref')!r} — the anchored "
                    f"item is the CLOSED DAILY MANIFEST, constituent events are "
                    f"membership leaves, and an event with its own receipt is a "
                    f"second anchored item hiding inside the first")

        construction = _resolve_merkle(f, label, doc.get("merkle_profile"), idx)
        _resolve_eligibility(f, label, doc.get("eligibility_snapshot"), idx, opened)

        leaf = digest_value(doc.get("event_leaf_digest"))
        if doc.get("admission_kind") != "replay_acknowledgement" and leaf:
            prior = seen_leaf.get(leaf)
            if prior is not None and prior[1] != doc.get("window_open"):
                f.error("durability_event_assigned_to_two_windows",
                        f"{label}: event leaf {leaf} was already admitted in "
                        f"window {prior[1]!r} ({prior[0]}) and is admitted again "
                        f"in {doc.get('window_open')!r} — every accepted event "
                        f"appears in EXACTLY ONE window's batch, and an event on "
                        f"both sides of a boundary is counted twice")
            elif prior is not None:
                f.error("durability_event_assigned_to_two_windows",
                        f"{label}: event leaf {leaf} is admitted twice in window "
                        f"{doc.get('window_open')!r} (also {prior[0]}) — exactly "
                        f"once means once")
            else:
                seen_leaf[leaf] = (label, doc.get("window_open"))

        key = doc.get("dedupe_key_ref")
        material = digest_value(doc.get("material_digest"))
        if key is not None and material is not None:
            prior = dedupe_material.get(key)
            if prior is not None and prior[1] != material:
                f.error("dedupe_key_reused_for_different_content",
                        f"{label}: dedupe key {key!r} was accepted for material "
                        f"{prior[1]} ({prior[0]}) and is offered here for "
                        f"{material} — reuse of an accepted key with different "
                        f"content is REFUSED before a sequence is assigned, and "
                        f"this record already holds one")
            elif prior is None:
                dedupe_material[key] = (label, material)

        sequence = as_int(doc.get("leaf_sequence"))
        if accepted is not None and sequence is not None \
                and doc.get("admission_kind") != "replay_acknowledgement":
            ordered.append((label, doc, accepted, sequence))

    ordered.sort(key=lambda row: row[2])
    for (label_a, _, accepted_a, seq_a), (label_b, _, accepted_b, seq_b) \
            in zip(ordered, ordered[1:]):
        if accepted_a < accepted_b and seq_a > seq_b:
            f.error("durability_sequence_inverts_acceptance_partition",
                    f"{label_b}: sequence {seq_b} was assigned at "
                    f"{accepted_b.isoformat()} while {label_a} holds the greater "
                    f"sequence {seq_a} at the EARLIER {accepted_a.isoformat()} — "
                    f"acceptance time partitions the windows and the sequence "
                    f"orders events within one, so a sequence that inverts the "
                    f"partition breaks the completeness walk that relies on it")


def check_manifests(f: Findings, scope: Scope, idx: DurabilityIndex) -> None:
    """THE CLOSED WINDOW'S ACCOUNTING, RECONCILED AGAINST ITS OWN ADMISSIONS."""
    anchored_by_manifest: dict[Any, Any] = {}
    for _, receipt in scope.receipts:
        ref = get(receipt, "daily_item", "manifest_ref")
        if ref is not None:
            anchored_by_manifest[ref] = digest_value(receipt.get("anchored_digest"))

    previous: tuple[str, dict] | None = None
    for label, doc in idx.manifests:
        terms = doc.get("terms") or {}
        opened, closed = _check_window(f, label, terms.get("window_open"),
                                       terms.get("window_close"))

        carried = digest_value(doc.get("material_digest"))
        if carried and terms:
            recomputed = canonical.digest(terms)
            if carried != recomputed:
                f.error("daily_manifest_configuration_substituted",
                        f"{label}: the manifest's material digest {carried} does "
                        f"not recompute over its own canonical terms "
                        f"({recomputed}) — the receipt anchors THIS list of "
                        f"fields, and a manifest whose digest stands over "
                        f"different bytes has substituted the accounting under "
                        f"the proof")

        if terms.get("selectivity_applied") is True:
            f.error("durability_event_selectivity_applied",
                    f"{label}: the manifest declares per-event selectivity — "
                    f"every durability-eligible event accepted during the window "
                    f"appears exactly once with NO per-event selectivity, and "
                    f"selection after acceptance is the discretion this whole "
                    f"profile exists to remove")
        if doc.get("reopened_after_close") is True:
            f.error("durability_window_reopened_after_close",
                    f"{label}: the manifest records the window reopened after "
                    f"close — a closed window is not reopened or rewritten, "
                    f"because a window that can be reopened has no closing time "
                    f"anybody can rely on")
        if doc.get("window_closed") is False \
                and doc.get("presented_as_publicly_anchored") is True:
            f.error("open_window_presented_as_anchored",
                    f"{label}: an OPEN window is presented as already publicly "
                    f"anchored — the open window is evidenced by the signed "
                    f"owner-local log and by nothing on a chain, and presenting "
                    f"it otherwise claims a witness that has not seen it")

        watermark = as_int(terms.get("close_sequence_watermark"))
        tree_size = as_int(get(terms, "resolving_log_checkpoint", "tree_size"))
        if watermark is None or tree_size is None or tree_size <= watermark:
            f.error("durability_close_watermark_unproven",
                    f"{label}: close watermark {watermark!r} is not covered by "
                    f"the resolving checkpoint's tree size {tree_size!r} — the "
                    f"SAME atomic close transaction records the watermark AND a "
                    f"signed checkpoint whose tree covers every leaf through it; "
                    f"a serialization point nothing witnesses is a serialization "
                    f"point a minter can move")

        construction = _resolve_merkle(f, label, terms.get("merkle_profile"), idx)
        _resolve_eligibility(f, label, terms.get("eligibility_snapshot"), idx,
                             opened)

        admissions = [pair for pair in
                      idx.admissions_by_window.get(terms.get("window_open"), [])
                      if pair[1].get("admission_kind") != "replay_acknowledgement"]
        declared_count = as_int(terms.get("event_count"))
        if admissions:
            admissions.sort(key=lambda pair: as_int(pair[1].get("leaf_sequence")) or 0)
            sequences = [as_int(pair[1].get("leaf_sequence")) for pair in admissions]
            leaves = [digest_value(pair[1].get("event_leaf_digest"))
                      for pair in admissions]
            if declared_count is not None and declared_count != len(admissions):
                code = ("durability_batch_summary_lowered_below_watermark"
                        if declared_count < len(admissions)
                        else "durability_batch_omits_accepted_event")
                f.error(code,
                        f"{label}: the manifest declares event_count "
                        f"{declared_count} where the resolving checkpoint's own "
                        f"admissions through watermark {watermark!r} number "
                        f"{len(admissions)} ({sequences}) — first sequence, last "
                        f"sequence and event count are SUMMARIES of the "
                        f"checkpoint-derived set and not a denominator this "
                        f"record chose, and three self-consistent numbers over a "
                        f"retained prefix are exactly what checkpoint "
                        f"reconciliation exists to catch")
            declared_last = as_int(terms.get("last_leaf_sequence"))
            if declared_last is not None and sequences \
                    and declared_last < max(s for s in sequences if s is not None):
                f.error("durability_batch_summary_lowered_below_watermark",
                        f"{label}: last_leaf_sequence {declared_last} is below "
                        f"the greatest eligible admission "
                        f"{max(s for s in sequences if s is not None)} covered by "
                        f"the close watermark — the omitted suffix is detected by "
                        f"reconciliation and the batch is REFUSED before witness "
                        f"verification")
            declared_first = as_int(terms.get("first_leaf_sequence"))
            if declared_first is not None and sequences \
                    and declared_first > min(s for s in sequences if s is not None):
                f.error("durability_batch_omits_accepted_event",
                        f"{label}: first_leaf_sequence {declared_first} is above "
                        f"the earliest eligible admission "
                        f"{min(s for s in sequences if s is not None)} — an "
                        f"omitted PREFIX is refused on the same footing as an "
                        f"omitted suffix")
            if construction is not None and all(leaves):
                root = digest_value(terms.get("daily_batch_root"))
                recomputed = _batch_root(construction, leaves)
                if root != recomputed:
                    f.error("daily_batch_root_not_reproducible",
                            f"{label}: the declared daily_batch_root {root} does "
                            f"not reproduce from the window's ordered event "
                            f"leaves under the released construction "
                            f"({recomputed}) — canonical leaf encoding, domain "
                            f"separation, ordering, tree shape, odd-node handling "
                            f"and SHA-256 deterministically reproduce the root or "
                            f"verification is refused")
                for index, (adm_label, adm) in enumerate(admissions):
                    expected = _membership_path(construction, leaves, index)
                    supplied = [entry for entry in (adm.get("membership_path") or [])
                                if isinstance(entry, dict)]
                    if not supplied and len(leaves) > 1:
                        f.error("durability_batch_omits_accepted_event",
                                f"{adm_label}: an accepted sequence in a closed "
                                f"window with no membership path into "
                                f"{label}'s batch — the batch is refused as "
                                f"INCOMPLETE even where its root carries valid "
                                f"witness evidence")
                        continue
                    got = [(entry.get("position"),
                            digest_value(entry.get("sibling_digest")))
                           for entry in supplied]
                    want = [(step["position"], step["value"]) for step in expected]
                    if got != want:
                        f.error("daily_batch_root_not_reproducible",
                                f"{adm_label}: the supplied membership path does "
                                f"not recompute to {label}'s batch root under the "
                                f"released construction (supplied {got}, "
                                f"recomputed {want}) — a path a verifier cannot "
                                f"walk is an unfalsifiable claim rather than a "
                                f"strong one")
        elif declared_count == 0 and construction is not None:
            root = digest_value(terms.get("daily_batch_root"))
            empty = digest_value(get(construction, "empty_root"))
            if root != empty:
                f.error("daily_batch_root_not_reproducible",
                        f"{label}: a count-zero window binds {root} where the "
                        f"released construction declares the deterministic empty "
                        f"root {empty} — an empty tree must have a value both "
                        f"parties reach, which is why the profile declares one "
                        f"rather than leaving it to convention")
        elif declared_count:
            f.warn("manifest-admissions-not-in-scope",
                   f"{label}: declares event_count {declared_count} and no "
                   f"admission for window {terms.get('window_open')!r} travels "
                   f"with it, so the checkpoint-derived reconciliation could not "
                   f"be performed; this reader adjudicates the records it is "
                   f"given and says so rather than passing the claim")

        if terms.get("previous_daily_batch_root") is not None:
            f.error("daily_continuity_link_over_batch_root",
                    f"{label}: the continuity link is taken over the previous "
                    f"window's BATCH ROOT — two consecutive empty windows share "
                    f"the deterministic empty root on purpose, so a link over the "
                    f"root cannot tell a missing intermediate day from a present "
                    f"one; the link is over the previous item's "
                    f"configuration-bound anchored digest and commits to its "
                    f"identity, accounting, registry snapshots and configuration")
        link = digest_value(terms.get("previous_daily_anchored_digest"))
        sentinel = terms.get("genesis_sentinel")
        if link is None and sentinel is None:
            f.error("daily_continuity_link_unresolved",
                    f"{label}: the manifest binds neither a predecessor's "
                    f"anchored digest nor the contract-defined genesis sentinel — "
                    f"a daily item with no continuity link is an item that cannot "
                    f"show what came before it")
        if link is not None and sentinel is not None:
            f.error("daily_continuity_link_unresolved",
                    f"{label}: the manifest binds BOTH a predecessor's anchored "
                    f"digest and the genesis sentinel — exactly one is present on "
                    f"a conforming record, because there is exactly one first "
                    f"manifest per owner log")
        if previous is None:
            if sentinel is None:
                f.error("first_daily_manifest_without_genesis_sentinel",
                        f"{label}: the earliest daily manifest in scope binds no "
                        f"genesis sentinel — the first manifest binds ONE "
                        f"contract-defined sentinel, because a sentinel a "
                        f"realization chose would let a minter start a fresh "
                        f"chain of daily items anywhere and present it as the "
                        f"first")
            elif sentinel != DAILY_GENESIS_SENTINEL:
                f.error("first_daily_manifest_without_genesis_sentinel",
                        f"{label}: the genesis sentinel is {sentinel!r} and not "
                        f"the contract-defined {DAILY_GENESIS_SENTINEL!r}")
        else:
            prev_label, prev_doc = previous
            expected = anchored_by_manifest.get(prev_doc.get("manifest_id"))
            prev_close = instant(get(prev_doc, "terms", "window_close"))
            if opened is not None and prev_close is not None and opened != prev_close:
                f.error("empty_window_without_linked_checkpoint",
                        f"{label}: this window opens {opened.isoformat()} while "
                        f"{prev_label} closed {prev_close.isoformat()} — the "
                        f"windows in between emitted no signed, linked count-zero "
                        f"manifest, and a chain of daily items with holes in it "
                        f"proves nothing about the days in the holes")
            if expected is None:
                f.warn("continuity-predecessor-receipt-not-in-scope",
                       f"{label}: {prev_label}'s receipt does not travel with "
                       f"these records, so the continuity link could not be "
                       f"resolved to a configuration-bound anchored digest")
            elif link != expected:
                f.error("daily_continuity_link_unresolved",
                        f"{label}: the continuity link {link} does not resolve to "
                        f"the immediately preceding item's anchored digest "
                        f"{expected} ({prev_label}) — a missing, duplicated, "
                        f"reordered or substituted daily item breaks the next "
                        f"manifest's continuity proof, and that is the property "
                        f"the link is for")
            if sentinel is not None:
                f.error("daily_continuity_link_unresolved",
                        f"{label}: the genesis sentinel is bound on a manifest "
                        f"that HAS a predecessor ({prev_label}) — a second first "
                        f"manifest is a fresh chain of daily items presented as "
                        f"the original")
        previous = (label, doc)


def check_confirmation_bindings(f: Findings, scope: Scope,
                                idx: DurabilityIndex) -> None:
    """THE PROFILE BINDING ON RECEIPTS, STATES AND RESULTS.

    Requirement 3 is a rule about THREE records at once — the mint-time
    configuration block commits the snapshot, the state record reports the
    evidence state under it, and the verification result names the profile its
    answer was reached under — so the comparisons live in one place rather than
    three, and a receipt minted under a dead profile is refused wherever it is
    read from."""
    # ---------------- receipts: the committed snapshot ----------------
    for label, doc in scope.receipts:
        mtc = doc.get("mint_time_configuration") or {}
        snapshots: dict[Any, dict] = {}
        for witness in (mtc.get("configured_witnesses") or []):
            if not isinstance(witness, dict):
                continue
            snapshot = witness.get("confirmation_profile")
            if not isinstance(snapshot, dict):
                continue
            chain = snapshot.get("chain_id")
            snapshots[chain] = snapshot
            if chain != witness.get("chain_id"):
                f.error("confirmation_profile_terms_substituted_under_version",
                        f"{label}: configured witness "
                        f"{witness.get('witness_id')!r} anchors on chain "
                        f"{witness.get('chain_id')!r} while its committed "
                        f"confirmation profile names {chain!r} — a snapshot for "
                        f"another network is a confirmation rule swapped under a "
                        f"valid-looking proof")
            if snapshot.get("standing") in ("retired", "compromised"):
                f.error("confirmation_profile_retired_or_compromised_mints_receipt",
                        f"{label}: the committed snapshot for {chain!r} stands "
                        f"{snapshot.get('standing')!r} — a retired or compromised "
                        f"profile MUST NOT mint a new receipt or support a new "
                        f"long-horizon claim; its historical receipts keep their "
                        f"as-of evidence, and that is a different thing from "
                        f"minting a new one")
            key = (chain, snapshot.get("profile_id"), snapshot.get("version"))
            entry = idx.profile_entries.get(key)
            if entry is None:
                if idx.profile_entries:
                    f.warn("confirmation-profile-unregistered",
                           f"{label}: the committed snapshot {key} matches no "
                           f"entry in any append-only register in scope, so its "
                           f"digest and standing could not be compared")
                continue
            if digest_value(snapshot.get("canonical_digest")) \
                    != digest_value(entry.get("canonical_digest")):
                f.error("confirmation_profile_terms_substituted_under_version",
                        f"{label}: the committed snapshot's digest disagrees with "
                        f"register entry {entry.get('entry_id')!r} — verification "
                        f"REFUSES the receipt and does not evaluate the "
                        f"substituted confirmation rule")
            if entry.get("standing") in ("retired", "compromised"):
                f.error("confirmation_profile_retired_or_compromised_mints_receipt",
                        f"{label}: register entry {entry.get('entry_id')!r} stands "
                        f"{entry.get('standing')!r} in the append-only register "
                        f"while this receipt was minted under it")
            active = idx.active_profile.get(chain)
            if active is not None and entry.get("entry_id") != active.get("entry_id") \
                    and (as_int(get(active, "activation", "log_sequence")) or 0) \
                    > (as_int(get(entry, "activation", "log_sequence")) or 0):
                f.error("confirmation_profile_snapshot_rolled_back",
                        f"{label}: the snapshot selects version "
                        f"{snapshot.get('version')!r} for {chain!r} while "
                        f"{active.get('entry_id')!r} (version "
                        f"{active.get('version')!r}) had already activated at the "
                        f"greater checkpoint — minting is REFUSED before witness "
                        f"submission even though the older version was once "
                        f"approved")

        daily = doc.get("daily_item")
        roots = {digest_value(get(entry, "commitment_derivation",
                                  "source_aggregation_root"))
                 for entry in (doc.get("per_chain_anchors") or [])
                 if isinstance(entry, dict)}
        roots.discard(None)
        if len(roots) > 1:
            f.error("daily_item_witness_roots_differ",
                    f"{label}: per-chain entries derive their commitments from "
                    f"{len(roots)} different aggregation roots {sorted(roots)} — "
                    f"after closure the SAME aggregation root enters BOTH "
                    f"configured witnesses; different commitment PATHS are "
                    f"mandatory where encoding differs and a different SOURCE is "
                    f"refused, because a split root is two anchored items "
                    f"presented as one")
        if isinstance(daily, dict):
            anchored = digest_value(doc.get("anchored_digest"))
            if doc.get("aggregation_merkle_path"):
                f.error("aggregation_root_not_identity_for_daily_item",
                        f"{label}: a `daily_merkle` item carries a non-empty "
                        f"aggregation path — for this one-item daily profile the "
                        f"shared aggregation path is the IDENTITY path, so "
                        f"aggregation_root == anchored_digest, and a sibling here "
                        f"means the anchored item is not the one the manifest "
                        f"closed")
            for root in roots:
                if root != anchored:
                    f.error("aggregation_root_not_identity_for_daily_item",
                            f"{label}: a per-chain commitment derives from {root} "
                            f"where the configuration-bound anchored digest is "
                            f"{anchored} — the daily item's aggregation root IS "
                            f"its anchored digest, and a commitment over anything "
                            f"else commits to something this receipt does not "
                            f"name")

        for index, entry in enumerate(doc.get("per_chain_anchors") or []):
            if not isinstance(entry, dict):
                continue
            where = f"{label}: per_chain_anchors[{index}] ({entry.get('chain_id')!r})"
            derivation = entry.get("commitment_derivation") or {}
            if derivation.get("path_present") is False:
                f.error("witness_commitment_path_absent",
                        f"{where}: carries transaction and chain inclusion "
                        f"evidence but no proof that its transaction commitment "
                        f"derives from the aggregation root this receipt names — "
                        f"the entry is REFUSED even where the transaction itself "
                        f"is canonically accepted, because inclusion of a "
                        f"commitment to something else is not evidence about this "
                        f"item")
            if derivation.get("proof_over") == "raw_daily_batch_root":
                f.error("durability_witness_proof_over_raw_batch_root",
                        f"{where}: the proof is taken over the RAW daily batch "
                        f"root rather than the configuration-bound aggregation "
                        f"root — a proof over the bare root drops the manifest "
                        f"link, the accounting fields, the registry snapshots and "
                        f"the whole mint-time configuration from what was "
                        f"committed, and it is refused by the amendment by name")
            named = entry.get("confirmed_under_profile") or {}
            snapshot = snapshots.get(entry.get("chain_id"))
            if snapshot is None:
                continue
            if named.get("profile_id") != snapshot.get("profile_id") \
                    or named.get("version") != snapshot.get("version") \
                    or digest_value(named.get("canonical_digest")) \
                    != digest_value(snapshot.get("canonical_digest")):
                f.error("witness_confirmed_without_named_profile",
                        f"{where}: the entry says it was confirmed under "
                        f"{named.get('profile_id')!r} v{named.get('version')!r} "
                        f"while the committed block snapshotted "
                        f"{snapshot.get('profile_id')!r} "
                        f"v{snapshot.get('version')!r} — a confirmed entry names "
                        f"the profile it was ACTUALLY evaluated under, and a name "
                        f"that disagrees with the committed snapshot names a rule "
                        f"nobody applied")
            token = named.get("as_of_token")
            expected = (f"confirmed_under_v{snapshot.get('version')}_at_"
                        f"{get(snapshot, 'activation', 'checkpoint_ref')}")
            if token is not None and token != expected:
                f.error("confirmation_profile_standing_rewrites_historical_receipt",
                        f"{where}: the immutable as-of token is {token!r} where "
                        f"the committed snapshot's version and activation "
                        f"checkpoint give {expected!r} — the as-of token is what "
                        f"was proven, under which version, at which checkpoint, "
                        f"and it does not change when policy does")

    # ---------------- anchor states: submitted is not confirmed ----------------
    for label, doc in scope.states:
        rows = [row for row in (doc.get("per_witness") or []) if isinstance(row, dict)]
        for row in rows:
            where = f"{label}: per_witness[{row.get('witness_id')!r}]"
            status = row.get("status")
            submission = row.get("submission_evidence")
            confirmation = row.get("confirmation_evidence")
            stage = row.get("upgrade_stage") or {}
            snapshot = row.get("confirmation_profile") or {}

            if status == "pending" and isinstance(submission, dict):
                f.error("witness_pending_with_submission_evidence",
                        f"{where}: reports `pending` while carrying accepted "
                        f"submission evidence "
                        f"{submission.get('evidence_kinds')!r} — `pending` is "
                        f"RESERVED for a witness with no accepted submission "
                        f"evidence, and a row that under-reports is as wrong an "
                        f"answer as one that over-reports")
            if status == "confirmed" and not isinstance(confirmation, dict):
                f.error("submission_evidence_offered_as_confirmed",
                        f"{where}: reports `confirmed` with no confirmation "
                        f"evidence at all — interface acceptance, a detached "
                        f"timestamp proof, a transaction identifier and a prior "
                        f"status label are SUBMISSION evidence, and offering them "
                        f"as confirmation is the one substitution requirement 3 "
                        f"exists to refuse")
            if status == "confirmed" and isinstance(confirmation, dict):
                if confirmation.get("condition_satisfied") is not True:
                    f.error("witness_confirmed_without_profile_condition",
                            f"{where}: reports `confirmed` while its own "
                            f"confirmation evidence records "
                            f"condition_satisfied="
                            f"{confirmation.get('condition_satisfied')!r} — the "
                            f"witness deterministically remains `submitted` where "
                            f"the referenced profile's objective condition is not "
                            f"satisfied, and the validator refuses the confirmed "
                            f"state")
                record = idx.profile_terms.get((snapshot.get("profile_id"),
                                                snapshot.get("version")))
                required = set(get(record, "terms", "retained_proof_material") or []) \
                    if record is not None else set()
                retained = set(confirmation.get("retained_proof_material") or [])
                if required and not required <= retained:
                    f.error("witness_confirmed_without_profile_condition",
                            f"{where}: reports `confirmed` while retaining "
                            f"{sorted(retained)} where the named profile requires "
                            f"{sorted(required)} — the retained-proof requirement "
                            f"is part of the condition, and confirmation over "
                            f"material nobody kept cannot be re-checked")
            if row.get("role") == "durability" and status == "confirmed" \
                    and stage and stage.get("chain_confirmation") != "confirmed":
                f.error("submission_evidence_offered_as_confirmed",
                        f"{where}: the row reports `confirmed` while its chain "
                        f"layer reports {stage.get('chain_confirmation')!r} — an "
                        f"accepted and retained detached proof is OpenTimestamps "
                        f"submitted, and confirmation on the underlying chain "
                        f"requires the upgrade this row says has not happened")

            change = row.get("observation_change")
            if isinstance(change, dict):
                if change.get("state_after") == "confirmed":
                    f.error("reorganized_witness_retains_confirmed_label",
                            f"{where}: a {change.get('change_kind')!r} is recorded "
                            f"and the state after it is still `confirmed` — the "
                            f"profile's declared transition rule determines the "
                            f"state, the change is written as evidence, and a "
                            f"stale confirmed label is not retained by assertion")
                if change.get("evidence_written") is not True:
                    f.error("reorganized_witness_retains_confirmed_label",
                            f"{where}: a {change.get('change_kind')!r} is recorded "
                            f"with evidence_written="
                            f"{change.get('evidence_written')!r} — a state change "
                            f"nobody wrote down is a label edit, and the whole "
                            f"point of the rule is that the change becomes "
                            f"evidence")

            pending_proof = row.get("pending_durability_proof")
            if isinstance(pending_proof, dict) \
                    and pending_proof.get("prior_transitions_retained") is False:
                f.error("state_transition_history_erased_on_upgrade",
                        f"{where}: the durability upgrade did not retain the "
                        f"prior state transitions — an upgrade APPENDS the "
                        f"completed entry against the same anchored digest and "
                        f"erases nothing, because the transitions are the "
                        f"evidence that submitted and confirmed were ever "
                        f"distinct states")

        if doc.get("long_horizon_claim_admitted") is True:
            durable = [row for row in rows if row.get("role") == "durability"]
            confirmed = [row for row in durable
                         if get(row, "upgrade_stage", "chain_confirmation")
                         == "confirmed"
                         or (not row.get("upgrade_stage")
                             and row.get("status") == "confirmed")]
            if not confirmed:
                f.error("long_horizon_claim_on_unupgraded_durability_proof",
                        f"{label}: a long-horizon durability claim is admitted "
                        f"while no durability witness reports a confirmed chain "
                        f"layer ("
                        f"{[(r.get('witness_id'), r.get('status'), get(r, 'upgrade_stage', 'chain_confirmation')) for r in durable]}) "
                        f"— such a claim cites Bitcoin-confirmed evidence and "
                        f"MUST NOT cite an unupgraded OpenTimestamps submission "
                        f"or the operational witness alone; the valid operational "
                        f"result stays independently reportable")

    # ---------------- verification results: the profile is named ----------------
    for label, doc in scope.verifications:
        rows = [row for row in (doc.get("confirmation_profiles_evaluated_under") or [])
                if isinstance(row, dict)]
        if doc.get("status") == "anchor_complete" and not rows:
            f.error("witness_confirmed_without_named_profile",
                    f"{label}: reports `anchor_complete` and names no "
                    f"confirmation profile — every verification result names the "
                    f"profile under which it was evaluated, because a "
                    f"completeness answer whose confirmation rule is unstated "
                    f"cannot be re-checked by the party it is shown to")
        for row in rows:
            where = f"{label}: confirmation_profiles_evaluated_under[{row.get('chain_id')!r}]"
            token = row.get("as_of_token")
            if token and not token.startswith(f"confirmed_under_v{row.get('version')}_at_"):
                f.error("confirmation_profile_standing_rewrites_historical_receipt",
                        f"{where}: the as-of token {token!r} does not name the "
                        f"version {row.get('version')!r} this row was evaluated "
                        f"under — the token is immutable evidence about the past "
                        f"and current standing is reported BESIDE it, never over "
                        f"it")
            if row.get("current_standing") in ("profile_retired", "profile_compromised") \
                    and row.get("new_claim_admitted") is True:
                f.error("confirmation_profile_retired_or_compromised_mints_receipt",
                        f"{where}: a NEW claim is admitted while current registry "
                        f"standing is {row.get('current_standing')!r} — the "
                        f"historical as-of evidence remains immutable AND no new "
                        f"long-horizon claim is admitted from that profile; each "
                        f"of those is the other's overcorrection")
            key = (row.get("chain_id"), row.get("profile_id"), row.get("version"))
            entry = idx.profile_entries.get(key)
            if entry is None:
                continue
            if digest_value(row.get("canonical_digest")) \
                    != digest_value(entry.get("canonical_digest")):
                f.error("confirmation_profile_terms_substituted_under_version",
                        f"{where}: the digest named by this result disagrees with "
                        f"register entry {entry.get('entry_id')!r}")
            expected_standing = {"active": "profile_active",
                                 "retired": "profile_retired",
                                 "compromised": "profile_compromised"}.get(
                                     entry.get("standing"))
            if expected_standing is not None \
                    and row.get("current_standing") != expected_standing \
                    and row.get("current_standing") != "profile_digest_mismatch":
                f.error("confirmation_profile_standing_rewrites_historical_receipt",
                        f"{where}: reports current standing "
                        f"{row.get('current_standing')!r} where the append-only "
                        f"register carries {entry.get('standing')!r} — current "
                        f"verification reports CURRENT standing, and a result "
                        f"that reports a stale one is the historical answer "
                        f"overwriting the live one")


def check_manifest_window_profiles(f: Findings, scope: Scope,
                                   idx: DurabilityIndex) -> None:
    """THE WINDOW-OPEN SNAPSHOT, CHECKED AGAINST THE WINDOW IT OPENED.

    A profile that activates DURING an open window applies only to the next one.
    That comparison needs both a window and a snapshot, and only the manifest and
    its receipt hold both — so it lives here rather than on either alone."""
    receipts_by_manifest = {get(doc, "daily_item", "manifest_ref"): (label, doc)
                            for label, doc in scope.receipts
                            if get(doc, "daily_item", "manifest_ref") is not None}
    for label, doc in idx.manifests:
        opened = instant(get(doc, "terms", "window_open"))
        pair = receipts_by_manifest.get(doc.get("manifest_id"))
        if opened is None or pair is None:
            continue
        receipt_label, receipt = pair
        for witness in (get(receipt, "mint_time_configuration",
                            "configured_witnesses") or []):
            snapshot = witness.get("confirmation_profile") \
                if isinstance(witness, dict) else None
            if not isinstance(snapshot, dict):
                continue
            key = (snapshot.get("chain_id"), snapshot.get("profile_id"),
                   snapshot.get("version"))
            entry = idx.profile_entries.get(key)
            if entry is None:
                continue
            effective = instant(get(entry, "effective_interval", "from_window_open"))
            if effective is not None and effective > opened:
                f.error("confirmation_profile_activation_applied_to_open_window",
                        f"{receipt_label}: the snapshot for "
                        f"{snapshot.get('chain_id')!r} takes effect at the window "
                        f"opening {effective.isoformat()} while {label} closed the "
                        f"window that opened {opened.isoformat()} — a profile "
                        f"activation during an open window applies only to the "
                        f"NEXT window, and every event and the final item retain "
                        f"the window-open snapshot")
            until = instant(get(entry, "effective_interval", "until_window_open"))
            if until is not None and until <= opened:
                f.error("confirmation_profile_snapshot_rolled_back",
                        f"{receipt_label}: the snapshot for "
                        f"{snapshot.get('chain_id')!r} ceased to be effective at "
                        f"{until.isoformat()}, before {label}'s window opened at "
                        f"{opened.isoformat()} — a window that opens after a new "
                        f"activation checkpoint and selects an older version is "
                        f"refused as rollback")


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
    # THE DURABILITY PROFILE'S OWN LAYER, LAST, because every one of its rules is
    # a property of a SET: the index is built once over the whole scope and the
    # comparisons are made against it rather than inferred from any one record.
    durability = _build_durability_index(scope)
    check_confirmation_profiles(f, scope)
    check_profile_registries(f, scope, durability)
    check_merkle_profiles(f, scope)
    check_eligibility_registries(f, scope, durability)
    check_admissions(f, scope, durability)
    check_manifests(f, scope, durability)
    check_manifest_window_profiles(f, scope, durability)
    check_confirmation_bindings(f, scope, durability)
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

    # THE SENTINEL THE READER HOLDS AND THE ONE THE CONTRACT DEFINES ARE ONE
    # VALUE, for the same reason the refusal sets are one set: a first manifest
    # the two spell differently is a first manifest neither can agree on.
    contract_sentinel = get(docs.get("anchoring-definitions.schema.yaml", {}),
                            "$defs", "daily_genesis_sentinel", "const")
    if contract_sentinel is not None \
            and contract_sentinel != DAILY_GENESIS_SENTINEL:
        f.error("genesis-sentinel-drift",
                f"the validator holds {DAILY_GENESIS_SENTINEL!r} and the contract "
                f"defines {contract_sentinel!r} as the daily genesis sentinel")

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
