# Data model: 029-chain-anchoring-durability-confirmation

Status: draft
Kind: design record

## Six new record kinds

| Kind | File | Digested substance | Its own digest subject |
| --- | --- | --- | --- |
| `xfactory_chain_anchoring_confirmation_profile` | `confirmation-profile.schema.yaml` | `terms` | `confirmation_profile_terms` |
| `xfactory_chain_anchoring_confirmation_profile_registry` | `confirmation-profile-registry.schema.yaml` | — (binds entries' digests) | — |
| `xfactory_chain_anchoring_daily_merkle_profile` | `daily-merkle-profile.schema.yaml` | `construction` | `daily_merkle_construction` |
| `xfactory_chain_anchoring_durability_eligibility_registry` | `durability-eligibility-registry.schema.yaml` | each entry's `terms` | `durability_eligibility_terms` |
| `xfactory_chain_anchoring_durability_batch_admission` | `durability-batch-admission.schema.yaml` | — | leaf: `durability_event_leaf` |
| `xfactory_chain_anchoring_durability_batch_manifest` | `durability-batch-manifest.schema.yaml` | `terms` | `anchor_material` (it IS the anchored material) |

## Eighteen shared definitions, declared once

`registry_standing`, `approval_record`, `activation_checkpoint`,
`effective_window_interval`, `registry_append_only_declaration`,
`witness_evidence_state`, `profile_as_of_token`, `profile_standing_report`,
`confirmation_profile_snapshot`, `eligibility_snapshot`,
`merkle_profile_snapshot`, `dedupe_rule`, `late_arrival_rule`,
`window_close_reason`, `leaf_class`, `daily_genesis_sentinel`,
`resolving_log_checkpoint`, `batch_membership_path`.

**EIGHTEEN, MEASURED RATHER THAN COUNTED BY HAND** — which is how the four
feature documents came to say "fourteen" in Copilot round 1 while listing
eighteen:

```
$ python3 -c "…set(now['\$defs']) - set(basis['\$defs'])…"
basis defs: 13   now: 31   ADDED: 18   removed: []
```

**Why one entry DISCIPLINE and two entry SHAPES.** Both registers bind a
version, a canonical digest, an approval, a predecessor, an activation
checkpoint, a half-open effective interval and a standing — so those are
`$defs` here and `$ref`s there. Their SUBSTANCE differs (which event kinds are
counted, versus what distinguishes submitted from confirmed), and a single entry
shape over both would make the two registers indistinguishable to anything that
compares them.

## The proof chain, node by node, as the amendment orders it

1. accepted event leaves + membership paths → `daily_batch_root`
   (`durability_event_leaf`, `daily_batch_node`, `daily_batch_root`)
2. canonical signed daily-manifest bytes = the manifest's `terms`
3. `material_digest` over exactly those bytes (`anchor_material`)
4. `anchored_digest` over `{material_digest, mint_time_configuration}`
   (`anchored_commitment`) — and the mint-time block now carries each configured
   witness's `confirmation_profile` snapshot, so swapping the confirmation RULE
   breaks every proof exactly as rewriting the witness set does
5. `aggregation_root == anchored_digest`: for this one-item daily profile the
   shared aggregation path is the IDENTITY path, enforced by
   `aggregation_root_not_identity_for_daily_item`
6. each per-chain entry's `commitment_derivation` begins at that SAME
   `source_aggregation_root`, then the four ratified per-chain elements

## Three shapes that can say the wrong thing on purpose

The family's carried rule: shapes it OWNS are made unrepresentable; restrictions
it imposes on a DECLARED value are refused BY NAME, because a shape that cannot
express the refused value cannot carry the negative example that proves the
refusal fires.

* `dedupe_rule.on_identical_replay` can say `assign_second_sequence`;
  `on_key_reuse_with_different_material` can say `admit_second_leaf`;
  `key_scope` can say `chain_visible`.
* `late_arrival_rule.window_selected_from` can say `owner_source_time`;
  `source_time_lateness_recorded` can say `on_chain`.
* `manifest.reopened_after_close`, `.presented_as_publicly_anchored`,
  `terms.selectivity_applied`, `terms.previous_daily_batch_root`,
  `admission.pre_closure_anchor_receipt_ref`,
  `admission.leaf_class: anchoring_control`,
  `approval_record.approved_by: implementer`,
  `registry_append_only_declaration.history_rewritten`,
  `commitment_derivation.proof_over: raw_daily_batch_root`,
  `pending_durability_proof.prior_transitions_retained: false`,
  `long_horizon_claim_admitted`.

## The verification result's rows are keyed by WITNESS, not by chain

Copilot round 1 found the ambiguity and it was real:
`configured_witnesses` carries no uniqueness constraint on `chain_id`, and the
per-chain entry's own `witness_id` exists precisely because a realization may
configure *"more than one witness against one chain"*. A
`confirmation_profiles_evaluated_under` row keyed on the chain alone would
collapse two such witnesses into one row, and a reader could not tell which
pairing was evaluated. `witness_id` is therefore REQUIRED on the row — the
shortfall arithmetic is already keyed by it, so this is the family's key and not
a new one — and the reader COMPARES it rather than trusting it: the named witness
must be in the referenced receipt's committed configured set, its chain must be
that witness's chain, the profile named must be the one the committed block
snapshotted for it, and two rows for one witness are refused.

## The per-witness state migration

| Old | New | Mechanical? |
| --- | --- | --- |
| `in_flight` | `pending` **or** `submitted` | **No** — and that is the measure of what the old value was hiding |
| `landed` | `confirmed` | Yes, plus the profile reference the new value requires |
| `terminally_failed` | `terminally_failed` | Unchanged |
| — | `invalid`, `unevaluable` | New; required by the amendment's own refusal scenario |

The durability witness additionally reports TWO LAYERS —
`upgrade_stage.aggregation_submission` and `.chain_confirmation` — because the
amendment requires the record to say *"OpenTimestamps submitted and Bitcoin
pending"*, which one field cannot express and which is the exact state in which
an unupgraded detached proof gets mistaken for durability.
