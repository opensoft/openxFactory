Lane: openxfactory-1d

Claim: https://github.com/opensoft/openxFactory/pull/548#issuecomment-5540796986

## The chain, in one line each

**#548 (`471d3361`, 2026-09-04)** ratified `amend-chain-anchoring-readiness-and-durability`
requirements 2 and 3 — Brett Heap, repository owner, in session, verbatim
*"ratify 2 and 3"*; requirement 1 WITHDRAWN, not refused, by his separate earlier
ruling of the same day. **Ratification promotes a spec delta and realizes
nothing**, and that packet's own `tasks.md` says so in its header.
**#629 (`11feff75`)** landed the basis: twelve schemas, a refusing reader, a
packaged corpus. **This PR** is the successor realization the ratification
created, authorized 2026-09-04 in session: *"build the successor realization on
629's schemas."*

## ⚠️ CUT ORDERING — THIS MUST LAND BEFORE #653, OR #653 MUST BE RE-DERIVED

**#653 (`chore/cut-contract-v3.4`) is open and publishes this exact family.**
Recorded on it: https://github.com/opensoft/openxFactory/pull/653#issuecomment-5542708415

One of this PR's changes is **not additive**: `anchor-state.schema.yaml`'s
closed per-witness `status` enumeration `[in_flight, landed, terminally_failed]`
is **REPLACED**. That is free before publication and a compatibility break after
it, and today it is free — **measured, not assumed**:

```
$ git tag --contains 11feff75
(empty)
$ grep -c chain-anchoring contracts/releases/contract-v3.3.digests.yaml
0
```

The `contract-v3.3` tag (`16b85614`) predates the basis realization by twenty
minutes, so the family is REGISTERED in `contracts/manifest.yaml` and UNSHIPPED
in every bundle. **#653 is precisely the act that ends that window.** If it lands
first, `contract-v3.4` publishes the retired spelling and this same edit becomes
a break against a published bundle — the amendment's `tasks.md` header says it
in its own words. #653's own additive argument rests on a grep
(*"returns zero matches"*) that is stale at this head, and its
`contracts/manifest.yaml` digest would need re-deriving either way.

## Why the enumeration had to be replaced rather than widened

`in_flight` carried ONE word for two facts requirement 3 requires be distinct: a
witness with **no accepted submission evidence**, and a witness whose submission
an interface **accepted while the approved confirmation condition remains
unmet**. One word for both is exactly what lets interface acceptance read as
progress toward confirmation — the defect requirement 3 exists to close.

| Old | Becomes | Mechanical? |
| --- | --- | --- |
| `in_flight` | `pending` **or** `submitted` | **No** — and that is the measure of what the old value was hiding |
| `landed` | `confirmed` | Yes, plus the profile reference the new value requires |
| `terminally_failed` | `terminally_failed` | Unchanged, same closed ground set |
| — | `invalid`, `unevaluable` | New; obliged by the amendment's own refusal scenario, which requires a verifier to report *"the actual submitted, pending, invalid, or unevaluable state"* |

Widening instead would have left `in_flight` and `landed` in the vocabulary as a
second, ambiguous spelling of the same states — the drift this family's
one-definition rule exists to prevent — and left every consumer free to keep
using the word that conflates the two facts. The migration is written into the
`witness_evidence_state` `$def` itself, with the pre-publication measurement
beside it, and into the family README's own table.

The durability witness additionally reports **two layers** —
`upgrade_stage.aggregation_submission` and `.chain_confirmation` — because the
amendment requires the record to say *"OpenTimestamps submitted and Bitcoin
pending"*, which one field cannot express and which is the exact state in which
an unupgraded detached proof gets mistaken for durability.

## What landed

**Six new record shapes** (the family is eighteen files, not twelve): the
operator-approved confirmation profile and its append-only signed register, the
released immutable daily-Merkle construction, the append-only eligibility
register that fixes the denominator, the one atomic admission of one event into
one fixed UTC window, and the canonical signed manifest of one closed window —
which is **the anchored item** of this profile.

**Eighteen shared `$defs`** in `anchoring-definitions.schema.yaml`, because the
two requirements share a registry discipline and a window model and two
spellings of either is the drift that file exists to prevent. The two registers
share an entry DISCIPLINE and not an entry SHAPE: a single shape over both would
make them indistinguishable to anything that compares them.

**Forty-eight further closed refusal codes**, and **the reader recomputes rather
than believes**. The released construction is RESOLVED and every leaf, membership
path and batch root is recomputed under it. The composition runs under the
estate's ONE digest construction, with the domain separators travelling inside
the canonical JSON, so **no second hashing rule is minted to reach a Merkle
tree** — and a construction whose declared ordering or shape cannot be reproduced
deterministically is refused rather than trusted (`acceptance_time_ascending` is
refused for a stated reason: timestamps tie, a tie has no deterministic
tiebreak).

**Manifests are reconciled against their own window's admissions.** A manifest
that lowers its last sequence and count to match a retained prefix is caught even
though its three summary numbers and its root are perfectly self-consistent —
which is the one attack a self-consistent summary cannot detect. Continuity
resolves to the immediately preceding item's configuration-bound anchored digest;
a link over the previous BATCH ROOT is refused because two consecutive empty
windows share that root on purpose, and a gap between consecutive windows is
refused because a chain of daily items with holes proves nothing about the days
in the holes.

**Six `digest_subject` members** added on `digest-construction.schema.yaml`'s own
written invitation, with `canonical.py`'s frozen mirror moved with it. **No
second construction. No leaf-grammar widening** — the durability profile's
control leaves are referenced BY IDENTIFIER, as every other record here
references a leaf, so no thirteenth anchoring discriminator was needed or taken.
**No bundle number**: `contract_bundle_version` is untouched and
`contracts/CHANGELOG.md` is the cutting session's, on the #556/#629 precedent.

## WHAT THE OPERATOR STILL OWES, IN THE PRESENT TENSE

Amendment tasks **1.3** and **1.4** stay OPEN and are marked `[OPERATOR]`. They
ask the operator to APPROVE the two confirmation profiles and to RELEASE the
daily-Merkle construction *before* authoring rests on them. **This PR does not
discharge them and does not report them discharged.** What it builds is the
VESSEL those approvals are published into, plus the REFUSALS that make the
amendment's BLOCKED state mechanical rather than a promise —
`confirmation_profile_unresolved` (a configured network with no active entry),
`confirmation_profile_not_operator_approved`,
`confirmation_profile_numeric_depth_uncited`,
`profile-transition-vectors-incomplete`,
`merkle_profile_absent_or_substituted`, `merkle-domain-separators-equal` — each
red-proven by a packaged negative. **The packaged register carries EXAMPLE entries
and no operator's act**, the packaged declaration reports
`operator_approval_outstanding`, and the reader's own docstring says at equal
length that **it cannot approve a profile** and **cannot see a signed log**.

## Files

| Area | Change |
| --- | --- |
| `contracts/chain-anchoring/` | **+6 schemas** (confirmation-profile, confirmation-profile-registry, daily-merkle-profile, durability-eligibility-registry, durability-batch-admission, durability-batch-manifest); **M** anchoring-definitions (18 `$defs`, +48 codes, the replaced enum), anchor-receipt, anchor-state, verification-result, conformance-declaration (nine → **eleven** obligations), README |
| `contracts/chain-anchoring/examples/` | **+15 positive files** (41 records, was 21); 60 existing files migrated; **+52 negatives** (127, was 75) |
| `contracts/signed-execution-chain/` | **M** digest-construction (+6 subjects), README |
| `contracts/manifest.yaml` | **+6 rows**, 6 re-pinned; 187/187 verify; `contract_bundle_version` UNTOUCHED |
| `scripts/` | **M** validate-chain-anchoring.py (+8 check layers, checks 15–17, 9 kebab findings, two further honest limits), signed_execution_chain/canonical.py |
| `tests/chain_anchoring/` | **+34 scenario tests**; 1 obligation pin 9 → 11 |
| `tests/signed_execution_chain/` | 1 subject pin 28 → **34** |
| `openspec/changes/amend-…/tasks.md` | 1.6, 2.2, 2.3, 2.4, 2.5 ticked with evidence; 3.1's tick gains the successor's run; **1.3 and 1.4 left open, `[OPERATOR]`** |
| `specs/029-chain-anchoring-durability-confirmation/` | the Speckit feature and its evidence |

## Scenario → test, all thirty-four

Requirement 2 — *fixed UTC durability batches account for every accepted event exactly once*:

| # | Scenario | Test |
| --- | --- | --- |
| 1 | A non-empty UTC window closes | `test_a_non_empty_utc_window_closes` |
| 2 | An empty UTC window closes | `test_an_empty_utc_window_closes` |
| 3 | A source-time event arrives after its earlier day closed | `test_a_source_time_event_arrives_after_its_earlier_day_closed` |
| 4 | Acceptance occurs exactly at UTC midnight | `test_acceptance_occurs_exactly_at_utc_midnight` |
| 5 | Admission races the midnight close | `test_admission_races_the_midnight_close` |
| 6 | A minter omits the final eligible admissions | `test_a_minter_omits_the_final_eligible_admissions` |
| 7 | An identical dedupe key and digest are replayed | `test_an_identical_dedupe_key_and_digest_are_replayed` |
| 8 | A dedupe key is reused for different content | `test_a_dedupe_key_is_reused_for_different_content` |
| 9 | An accepted event is omitted from the daily root | `test_an_accepted_event_is_omitted_from_the_daily_root` |
| 10 | Eligibility changes during an open window | `test_eligibility_changes_during_an_open_window` |
| 11 | Two eligibility entries claim the same boundary | `test_two_eligibility_entries_claim_the_same_boundary` |
| 12 | An older eligibility version is offered after successor activation | `test_an_older_eligibility_version_is_offered_after_successor_activation` |
| 13 | Eligibility content is substituted under the same version | `test_eligibility_content_is_substituted_under_the_same_version` |
| 14 | Merkle construction profile is missing or substituted | `test_merkle_construction_profile_is_missing_or_substituted` |
| 15 | Independent validator recomputes a non-empty root | `test_independent_validator_recomputes_a_non_empty_root` |
| 16 | An intermediate empty day is omitted | `test_an_intermediate_empty_day_is_omitted` |
| 17 | An anchoring control leaf is offered as a source event in its own batch | `test_an_anchoring_control_leaf_is_offered_as_a_source_event_in_its_own_batch` |
| 18 | Different roots are proposed for the two configured witnesses | `test_different_roots_are_proposed_for_the_two_configured_witnesses` |
| 19 | A witness-specific commitment path is omitted | `test_a_witness_specific_commitment_path_is_omitted` |
| 20 | Batch root or mint-time configuration is substituted | `test_batch_root_or_mint_time_configuration_is_substituted` |

Requirement 3 — *witness submission and confirmation remain distinct evidence states*:

| # | Scenario | Test |
| --- | --- | --- |
| 21 | Kaspa accepts a transaction for processing | `test_the_operational_interface_accepts_a_transaction_for_processing` |
| 22 | Kaspa confirmation evidence becomes complete | `test_operational_confirmation_evidence_becomes_complete` |
| 23 | Schema authoring starts without approved confirmation profiles | `test_schema_authoring_starts_without_approved_confirmation_profiles` |
| 24 | A submitted proof is below its approved confirmation condition | `test_a_submitted_proof_is_below_its_approved_confirmation_condition` |
| 25 | A profile handles a reorganization or replacement | `test_a_profile_handles_a_reorganization_or_replacement` |
| 26 | An operator approves a new profile version | `test_an_operator_approves_a_new_profile_version` |
| 27 | A minter rolls back after a newer profile activates | `test_a_minter_rolls_back_after_a_newer_profile_activates` |
| 28 | A profile activates during an open window | `test_a_profile_activates_during_an_open_window` |
| 29 | Profile content is substituted under an approved id and version | `test_profile_content_is_substituted_under_an_approved_id_and_version` |
| 30 | A profile is retired or compromised after historical confirmation | `test_a_profile_is_retired_or_compromised_after_historical_confirmation` |
| 31 | OpenTimestamps proof is submitted but not upgraded | `test_a_durability_proof_is_submitted_but_not_upgraded` |
| 32 | Bitcoin upgrade verifies | `test_the_durability_upgrade_verifies` |
| 33 | Pending evidence is offered as confirmed | `test_pending_evidence_is_offered_as_confirmed` |
| 34 | Kaspa alone is offered for a long-horizon claim | `test_the_operational_witness_alone_is_offered_for_a_long_horizon_claim` |

**34/34.** Twelve are ACCEPTING scenarios and assert the positive half rather than
only a refusal. The delta names Kaspa and Bitcoin; **this family names no chain**,
so the records carry the `operational` and `durability` ROLES and the tests read
those.

## Red-first, measured

With the amendment's eight check layers replaced by no-ops:

```
with the amendment's checks DISABLED: 52/52 of its negatives validate cleanly
positive corpus with the checks disabled: 0 error(s)
```

**Every one of the fifty-two is red BECAUSE OF the new rule** — not a shape, not
the payload sweep, not the closure rule, not the timing model. Turn the new
layers off and the whole set goes green.

## Gates, at this head (`0115f346`, merged with `origin/main` `bc1bd4ee` — clean, no conflicts)

| Gate | Result |
| --- | --- |
| `validate-chain-anchoring.py .` | **0 errors, 2 warnings**; self-test **41** positives / **127** negatives / **118 of 118** closed codes red-proven / 9 further findings probed; repo scan 0 artifacts |
| `validate-signed-execution-chain.py . --require-pinned-wallet-vocabulary` | **0 / 0** |
| `validate-manifest-digests.py .` | **187/187 verify** |
| `pytest tests/chain_anchoring tests/signed_execution_chain tests/manifest_digests` | **237 passed** (195s) |
| `pytest tests/doc-health -q -p no:cacheprovider` | **1552 passed** (354s) |
| `openspec validate --all --strict` | **89 passed, 0 failed** |
| `proposal-support.py . verify amend-chain-anchoring-readiness-and-durability` | **ok** |
| `validate-sequenced-after.py . --ledger-diff` | **ledger consistent (165 rows)** |
| `doc-health.py --single-repo` | 6 critical / 4 error / 27 warning / 14 info — **identical finding SET to `origin/main`, zero delta**, re-taken after `main` moved 23 commits |

The two warnings are the standing honest pair, unchanged from the basis:
`reader-not-required` and `archival-node-undeclared`. Neither is this PR's to
close.

**`validate-contract-release.py verify-commit --commit HEAD`** reports exactly one
mismatch, `contracts/manifest.yaml` — and **a detached worktree at
`origin/main` reports the identical single mismatch on the identical path.** No
other path differs.

## What is deliberately NOT reopened

The two-witness configuration (the `third_anchor_target` refusal and its fixture
stand unchanged); `witness_role`, still exactly `[operational, durability]`; the
timing model and every direction in it; the one digest construction; and the leaf
grammar. No chain is named anywhere. No runtime is commissioned — no signed-log
instance identity, signer chain, custody owner, reachable interface or current
checkpoint is claimed, and the repo scan reports **0 real artifacts**, which is
the expected state until an anchoring subsystem runs.

Refs #548. Do not merge on my word — the cut ordering against #653 is the
repository owner's call.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
