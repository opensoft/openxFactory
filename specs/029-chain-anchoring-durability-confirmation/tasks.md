# Tasks: 029-chain-anchoring-durability-confirmation

Status: draft
Kind: task list

## 1. Shapes

- [x] 1.1 Six new record shapes under `contracts/chain-anchoring/`.
- [x] 1.2 Fourteen shared `$defs` in `anchoring-definitions.schema.yaml`, one
      definition per concept, taken by `$ref` everywhere they are used.
- [x] 1.3 The closed refusal enumeration widened by 48, grouped and commented.
- [x] 1.4 `witness_evidence_state` REPLACES the per-witness `status`
      enumeration, with the migration and the pre-publication measurement
      written into the `$def`.
- [x] 1.5 `configured_witness` gains `confirmation_profile` INSIDE the committed
      mint-time block (a receipt-only input joins the block by the closure rule);
      `per_chain_anchor` gains `commitment_derivation` and
      `confirmed_under_profile`; the receipt gains a `daily_item` pointer that
      carries no accounting.
- [x] 1.6 The verification result names the profiles it was evaluated under,
      with the immutable as-of token beside current registry standing.
- [x] 1.7 The conformance declaration closes over ELEVEN obligations and gains
      the `durability_profile` and `confirmation_profile_resolution` posture
      blocks.
- [x] 1.8 Six subjects added to `digest-construction.schema.yaml` and mirrored
      in `canonical.py`; no second construction; no leaf-grammar widening.

## 2. Reader

- [x] 2.1 Eight new check layers, run last over a durability index built once
      across the whole scope.
- [x] 2.2 The released Merkle construction RESOLVED, and every leaf, membership
      path and batch root recomputed under it; a construction this reader cannot
      reproduce deterministically is refused.
- [x] 2.3 Manifests reconciled against their own window's admissions, so a
      lowered summary over a retained prefix is caught.
- [x] 2.4 Continuity resolved to the previous item's configuration-bound
      anchored digest; the link over a batch root and the gap between windows
      each refused.
- [x] 2.5 The confirmation-profile binding checked across receipt, state and
      result at once, with both overcorrections refused.
- [x] 2.6 The reader's docstring extended with checks 15-17, the eight
      kebab-case findings, and two further honest limits (it cannot approve a
      profile; it cannot see a signed log).

## 3. Corpus

- [x] 3.1 Fifteen new positive example files: three consecutive fixed-UTC
      windows with their admissions, manifests, receipts and states, plus the
      two registers and the released construction.
- [x] 3.2 Every batch root and membership path COMPUTED under the released
      construction rather than written by hand.
- [x] 3.3 The basis realization's sixty corpus files migrated uniformly, with
      anchored digests recomputed only where they already recomputed.
- [x] 3.4 Fifty-two single-fault negatives; 118/118 closed codes red-proven; 8
      further finding codes probed.
- [x] 3.5 No YAML anchors or aliases anywhere in the packaged corpus.

## 4. Registration and documentation

- [x] 4.1 Six manifest rows with per-file digests; six moved files re-pinned;
      187/187 verify; `contract_bundle_version` untouched and no bundle number
      reserved.
- [x] 4.2 The family README: eighteen files, the migration table, the
      pre-publication measurement, and what the operator still owes in the
      present tense.
- [x] 4.3 `signed-execution-chain/README.md` records the six further subjects
      and the deliberate absence of a leaf-grammar widening.

## 5. Tests and evidence

- [x] 5.1 One test per scenario, 34 of them, each named for its scenario.
- [x] 5.2 The existing reader suite updated for eleven obligations.
- [x] 5.3 Red-first measured: with the amendment's eight check layers disabled,
      52/52 of its negatives validate cleanly and the positive corpus reports
      zero errors.
- [x] 5.4 Every gate in the brief run and recorded with counts.

## 6. Not this feature's

- [ ] 6.1 **[OPERATOR]** Approve and publish the Kaspa and Bitcoin confirmation
      profiles (amendment task 1.3).
- [ ] 6.2 **[OPERATOR]** Approve and release the daily-Merkle construction
      (amendment task 1.4).
- [ ] 6.3 Archive `add-chain-anchoring`, then this amendment (amendment task
      3.2).
- [ ] 6.4 Cut the additive bundle minor and publish release evidence (amendment
      task 3.3). **This feature must be IN that cut.**
