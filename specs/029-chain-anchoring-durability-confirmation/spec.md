# Feature: chain-anchoring durability batches and distinct witness evidence states

Status: draft
Kind: feature specification
Feature: 029-chain-anchoring-durability-confirmation
Realizes: `amend-chain-anchoring-readiness-and-durability` requirements 2 and 3
Basis: `add-chain-anchoring`, realized at PR #629 (squash `11feff75`)
Ratification: PR #548 (squash `471d3361`), 2026-09-04, Brett Heap, repository
owner, in session, verbatim *"ratify 2 and 3"* — record
`openspec/changes/amend-chain-anchoring-readiness-and-durability/review/ratification-2026-09-04.md`
Owner's authorization for this feature: Brett Heap, 2026-09-04, in session,
verbatim *"build the successor realization on 629's schemas"*

## What this feature is, and what it deliberately is not

**IT IS A CONTRACT REALIZATION.** Six new record shapes, fourteen shared
definitions, forty-eight further closed refusal codes, one REPLACED closed
enumeration, a canonical reader that recomputes rather than believes, a packaged
corpus in which every refusal has been seen to fire, and six manifest rows with
per-file digests.

**IT IS NOT A RUNTIME AND IT IS NOT AN OPERATOR APPROVAL.** Nothing here reaches
a chain, runs a node, batches an aggregation or fetches a header set. And the
amendment's two OPERATOR gates — approving the Kaspa and Bitcoin confirmation
profiles (tasks 1.3) and releasing the daily-Merkle construction (1.4) — are NOT
discharged by this feature and are not reported discharged. What this feature
builds is the VESSEL those approvals are published into, plus the REFUSAL that
fires when a configured network has none, so the amendment's BLOCKED state is
mechanical rather than a promise.

## The one non-additive change, and why it is safe here

`contracts/chain-anchoring/anchor-state.schema.yaml`'s per-witness `status`
enumeration was `[in_flight, landed, terminally_failed]`. It is REPLACED by
`[pending, submitted, confirmed, invalid, unevaluable, terminally_failed]`.

`in_flight` carried ONE word for two facts requirement 3 requires be distinct: a
witness with no accepted submission evidence, and a witness whose submission an
interface accepted while the approved confirmation condition remains unmet. One
word for both is precisely what lets interface acceptance read as progress
toward confirmation.

**Replacing a closed enumeration is free before publication and a compatibility
break after it, and this is pre-publication — measured, not assumed:**
`git tag --contains 11feff75` is EMPTY, and
`contracts/releases/contract-v3.3.digests.yaml` carries ZERO rows for any path
under `contracts/chain-anchoring/`, because the `contract-v3.3` tag
(`16b85614`) predates the basis realization by twenty minutes.

**THEREFORE THIS FEATURE IS ORDERED BEFORE THE NEXT BUNDLE CUT.** A cut taken
from a tip that lacks it would have to be re-derived.

## The thirty-four scenarios, and where each one lives

Every scenario of the ratified delta maps to (a) the record shape that makes it
expressible, (b) the reader rule that adjudicates it, and (c) the test named for
it in
`tests/chain_anchoring/test_durability_and_confirmation_scenarios.py`. Twelve of
them are ACCEPTING scenarios and are held by packaged POSITIVE records; the rest
are refusals, each with a single-fault packaged negative whose filename is the
code.

### Requirement 2 — fixed UTC durability batches account for every accepted event exactly once

| # | Scenario | Adjudicated by | Test |
| --- | --- | --- | --- |
| 1 | A non-empty UTC window closes | positive: `durability-batch-manifest-1`, `anchor-receipt-5`; root and paths recomputed | `test_a_non_empty_utc_window_closes` |
| 2 | An empty UTC window closes | positive: `durability-batch-manifest-2`, `anchor-receipt-6`; declared empty root | `test_an_empty_utc_window_closes` |
| 3 | A source-time event arrives after its earlier day closed | positive: `durability-batch-admission-2` | `test_a_source_time_event_arrives_after_its_earlier_day_closed` |
| 4 | Acceptance occurs exactly at UTC midnight | positive: `dba-example-0005`; `admission-window-acceptance-mismatch` the other way | `test_acceptance_occurs_exactly_at_utc_midnight` |
| 5 | Admission races the midnight close | `durability_admission_not_atomic`, `durability_event_assigned_to_two_windows`, `durability_sequence_inverts_acceptance_partition` | `test_admission_races_the_midnight_close` |
| 6 | A minter omits the final eligible admissions | `durability_batch_summary_lowered_below_watermark` | `test_a_minter_omits_the_final_eligible_admissions` |
| 7 | An identical dedupe key and digest are replayed | positive: `dba-example-0003`; `dedupe_replay_consumed_a_second_sequence`, `constituent_event_given_separate_receipt` | `test_an_identical_dedupe_key_and_digest_are_replayed` |
| 8 | A dedupe key is reused for different content | `dedupe_key_reused_for_different_content`, `dedupe_key_reachable_from_anchor` | `test_a_dedupe_key_is_reused_for_different_content` |
| 9 | An accepted event is omitted from the daily root | `durability_batch_omits_accepted_event` | `test_an_accepted_event_is_omitted_from_the_daily_root` |
| 10 | Eligibility changes during an open window | `eligibility_activation_applied_to_open_window` | `test_eligibility_changes_during_an_open_window` |
| 11 | Two eligibility entries claim the same boundary | `eligibility_boundary_selection_ambiguous` (zero and several) | `test_two_eligibility_entries_claim_the_same_boundary` |
| 12 | An older eligibility version is offered after successor activation | `eligibility_snapshot_rolled_back` | `test_an_older_eligibility_version_is_offered_after_successor_activation` |
| 13 | Eligibility content is substituted under the same version | `eligibility_terms_substituted_under_version` | `test_eligibility_content_is_substituted_under_the_same_version` |
| 14 | Merkle construction profile is missing or substituted | `merkle_profile_absent_or_substituted` | `test_merkle_construction_profile_is_missing_or_substituted` |
| 15 | Independent validator recomputes a non-empty root | reader recomputes every leaf, path and root | `test_independent_validator_recomputes_a_non_empty_root` |
| 16 | An intermediate empty day is omitted | `daily_continuity_link_unresolved`, `empty_window_without_linked_checkpoint`, `daily_continuity_link_over_batch_root`, `first_daily_manifest_without_genesis_sentinel` | `test_an_intermediate_empty_day_is_omitted` |
| 17 | An anchoring control leaf is offered as a source event in its own batch | `anchoring_control_leaf_admitted_as_event` | `test_an_anchoring_control_leaf_is_offered_as_a_source_event_in_its_own_batch` |
| 18 | Different roots are proposed for the two configured witnesses | `daily_item_witness_roots_differ` | `test_different_roots_are_proposed_for_the_two_configured_witnesses` |
| 19 | A witness-specific commitment path is omitted | `witness_commitment_path_absent`, `durability_witness_proof_over_raw_batch_root` | `test_a_witness_specific_commitment_path_is_omitted` |
| 20 | Batch root or mint-time configuration is substituted | `daily_manifest_configuration_substituted`, `receipt_configuration_block_edited`, `durability_close_watermark_unproven`, plus the reopened/selective/open-window/non-fixed/source-time/lateness refusals | `test_batch_root_or_mint_time_configuration_is_substituted` |

### Requirement 3 — witness submission and confirmation remain distinct evidence states

| # | Scenario | Adjudicated by | Test |
| --- | --- | --- | --- |
| 21 | Kaspa accepts a transaction for processing | positive: `anchor-state-6`, `anchor-receipt-7` | `test_the_operational_interface_accepts_a_transaction_for_processing` |
| 22 | Kaspa confirmation evidence becomes complete | positive: `anchor-state-5`, `anchor-receipt-5` | `test_operational_confirmation_evidence_becomes_complete` |
| 23 | Schema authoring starts without approved confirmation profiles | `confirmation_profile_unresolved`, `confirmation_profile_not_operator_approved`, `confirmation_profile_numeric_depth_uncited`, `profile-transition-vectors-incomplete` | `test_schema_authoring_starts_without_approved_confirmation_profiles` |
| 24 | A submitted proof is below its approved confirmation condition | `witness_confirmed_without_profile_condition`, `witness_pending_with_submission_evidence` | `test_a_submitted_proof_is_below_its_approved_confirmation_condition` |
| 25 | A profile handles a reorganization or replacement | `reorganized_witness_retains_confirmed_label`, plus the accepting twin | `test_a_profile_handles_a_reorganization_or_replacement` |
| 26 | An operator approves a new profile version | positive: `confirmation-profile-registry-1` (v1 retired, v2 active, interval closed in the same act) | `test_an_operator_approves_a_new_profile_version` |
| 27 | A minter rolls back after a newer profile activates | `confirmation_profile_snapshot_rolled_back` | `test_a_minter_rolls_back_after_a_newer_profile_activates` |
| 28 | A profile activates during an open window | `confirmation_profile_activation_applied_to_open_window` | `test_a_profile_activates_during_an_open_window` |
| 29 | Profile content is substituted under an approved id and version | `confirmation_profile_terms_substituted_under_version` | `test_profile_content_is_substituted_under_an_approved_id_and_version` |
| 30 | A profile is retired or compromised after historical confirmation | `confirmation_profile_retired_or_compromised_mints_receipt`, `confirmation_profile_standing_rewrites_historical_receipt`, plus the accepting twin | `test_a_profile_is_retired_or_compromised_after_historical_confirmation` |
| 31 | OpenTimestamps proof is submitted but not upgraded | positive: `anchor-state-6` `upgrade_stage` = submitted / pending | `test_a_durability_proof_is_submitted_but_not_upgraded` |
| 32 | Bitcoin upgrade verifies | positive: `anchor-state-5`; `state_transition_history_erased_on_upgrade`, `durability_proof_reanchored_rather_than_upgraded` | `test_the_durability_upgrade_verifies` |
| 33 | Pending evidence is offered as confirmed | `submission_evidence_offered_as_confirmed`, `witness_confirmed_without_named_profile` | `test_pending_evidence_is_offered_as_confirmed` |
| 34 | Kaspa alone is offered for a long-horizon claim | `long_horizon_claim_on_unupgraded_durability_proof`; the operational result stays reportable | `test_the_operational_witness_alone_is_offered_for_a_long_horizon_claim` |

## What is NOT reopened

The two-witness configuration (the `third_anchor_target` refusal and its fixture
stand unchanged); the `witness_role` enumeration, still exactly `[operational,
durability]`; the timing model and every direction in it; the one digest
construction (six SUBJECTS were added to its enumeration on that file's own
written invitation, and no second construction); and the leaf grammar, which
this family still does not touch — the durability profile's control leaves are
referenced BY IDENTIFIER, as every other record here references a leaf. No chain
is named anywhere.
