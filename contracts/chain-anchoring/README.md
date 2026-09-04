# Chain Anchoring Contract Family (tranche three)

Status: ratified
Ratified by: add-chain-anchoring (ratified 2026-08-30 by Brett Heap, repository
owner, in session, ruling item 2 of six — *"2 yes with note"*; record
`openspec/changes/add-chain-anchoring/review/ratification-2026-08-30.md`, taken
after the §7.4 council sitting of 2026-08-30 whose sole disposition of record is
`review/disposition-2026-08-30.md`)
Kind: reference
Repository context: openxFactory owns this neutral contract. It is REALIZED and
**REGISTERED in `contracts/manifest.yaml`** — all twelve schemas below carry a
per-file `sha256` — performed at THIS REALIZATION rather than by the cutting
session, on the repository owner's word of 2026-09-04 (Brett Heap, verbatim:
*"register now"*) and on the TRANCHE-TWO PRECEDENT, where `add-chain-attestation`
added its eight rows in its realization (`518c670b`) and left only the number and
the changelog entry to the cut (`bbbbeda9`). `tasks.md` 4.11 reads *"at the
additive bundle cut"*; that TIMING is what the owner overruled, and only that.
**NO BUNDLE NUMBER IS TAKEN OR RESERVED HERE.** `contracts/CHANGELOG.md` — 4.11's
other named surface — and the `contract_bundle_version` bump remain the cutting
session's act, per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md), because a
proposed change MUST NOT reserve a minor number before merge order is known; the
number is fresh-counted at the tip the cut is taken from. The packaged corpus,
this README, the reader and its pytest wiring are content-addressed BY COMMIT, on
tranche one's and tranche two's precedent.
**AND NO CHECK REQUIRES THESE RECORDS YET.** Until a named reader runs as a
REQUIRED check on the repository that holds them, everything below confers and
refuses exactly nothing — the distinction tranche one's own README drew, and
which took it from realization on 2026-08-29 to a required check on 2026-08-31.
A merged workflow file is not evidence that a check is required; the live ruleset
state is. See § What this family does NOT carry for what else is outstanding.

## Amended once, and the amendment REPLACED an enumeration

**`amend-chain-anchoring-readiness-and-durability` requirements 2 and 3 are
ratified and realized here** (ratified 2026-09-04 by Brett Heap, repository
owner, in session, verbatim *"ratify 2 and 3"*; record
`../../openspec/changes/amend-chain-anchoring-readiness-and-durability/review/ratification-2026-09-04.md`.
Requirement 1 was WITHDRAWN — not refused — by his separate earlier ruling of
the same day). The family is EIGHTEEN files, not twelve; the capability has
ELEVEN obligations, not nine; the closed refusal enumeration carries 118 codes,
not 70; and the per-witness state vocabulary is SIX members where it was three.

**THE ENUMERATION CHANGE IS THE ONE THING HERE THAT IS NOT ADDITIVE, AND THE
WINDOW FOR IT IS WHY THIS LANDED WHEN IT DID.**
`anchor-state.schema.yaml`'s per-witness `status` was
`[in_flight, landed, terminally_failed]`. `in_flight` had ONE word for two facts
requirement 3 requires be distinct — a witness with NO accepted submission
evidence, and a witness whose submission an interface accepted while the
approved confirmation condition remains unmet — and one word for both is what
lets interface acceptance read as progress toward confirmation. So:

| Old value | Becomes | Why |
| --- | --- | --- |
| `in_flight` | `pending` **or** `submitted` | The split requirement 3 exists for. It CANNOT be done mechanically from the old value alone, which is the measure of how much the old value was hiding: `pending` means no accepted submission evidence, `submitted` means submission accepted and the condition unmet |
| `landed` | `confirmed` | Same meaning, bound now to a named profile's OBJECTIVE CONDITION rather than to a word; a `confirmed` row names the profile it was evaluated under |
| `terminally_failed` | `terminally_failed` | Carried unchanged, same meaning, same closed ground set |
| — | `invalid`, `unevaluable` | NEW, and obliged by the amendment's own refusal scenario: when confirmation is refused the verifier must report *"the actual submitted, pending, invalid, or unevaluable state"*, and a vocabulary with no word for the last two forces a wrong answer |

**REPLACING A CLOSED ENUMERATION IS FREE BEFORE PUBLICATION AND A COMPATIBILITY
BREAK AFTER IT, AND THIS IS PRE-PUBLICATION — MEASURED, NOT ASSUMED.** At the
commit that realizes this, `git tag --contains 11feff75` (the basis
realization's squash) is **EMPTY**, and
[`../releases/contract-v3.3.digests.yaml`](../releases/contract-v3.3.digests.yaml)
carries **ZERO** rows for any path under `contracts/chain-anchoring/` — because
the `contract-v3.3` tag (`16b85614`) predates the basis realization by twenty
minutes. The family is REGISTERED in `contracts/manifest.yaml` and UNSHIPPED, so
this change is **additive to every bundle that has ever shipped** and there is no
consumer holding the retired spelling. **It therefore had to land BEFORE the next
cut**, and a cut taken from a tip that lacks it would have to be re-derived.

**WHAT THE OPERATOR STILL OWES, IN THE PRESENT TENSE.** The amendment obliges the
operator to APPROVE the two confirmation profiles and to RELEASE the daily-Merkle
construction before authoring rests on them
(`amend-chain-anchoring-readiness-and-durability` tasks 1.3 and 1.4, both still
open). What is built here is the VESSEL those approvals are published into and
the refusal that fires when a configured network has none
(`confirmation_profile_unresolved`) — so the BLOCK is mechanical rather than a
promise. **The packaged register carries EXAMPLE entries and no operator's act**,
the packaged declaration reports `operator_approval_outstanding` in the present
tense, and no record here claims otherwise.

## What this family is for

**Tranche one's log detects an edit inside a prefix somebody already watched,
and nothing else.** A store that deletes its newest leaves and presents an
earlier valid head shows a shorter log that verifies perfectly to a fresh
reader. That residual is DECLARED in tranche one's `SEC-R6` entry, and this is
the tranche that closes it: a head witnessed on a public chain is a head no
custodian can quietly shorten.

**The receipt is defined FIRST, and being chain-agnostic is the point of it.**
Anchor targets are a configuration this estate expects to change. If the receipt
were shaped around one chain's proof structure, changing targets would be a
rebuild and every already-captured receipt would be an object nobody could read.
So the format comes first, the targets go in a LIST inside it, and adding or
dropping one moves nothing else.

**What this family is NOT is a runtime.** Nothing here reaches a chain, runs a
node, batches an aggregation or fetches a header set. These are the record
shapes, the refusals, and the declaration a realization makes about itself.

## The eighteen files

| File | What it declares |
| --- | --- |
| [`anchoring-definitions.schema.yaml`](anchoring-definitions.schema.yaml) | **THE SHARED VOCABULARY**, declaring NO record kind: the two witness roles, the three plane names, the custody reference, the per-chain accepted-time rule, the integer-second duration, and **the closed refusal enumeration in one place**. Refuses a second spelling of any of them |
| [`anchor-receipt.schema.yaml`](anchor-receipt.schema.yaml) | The CHAIN-AGNOSTIC MULTI-ANCHOR RECEIPT — the material digest, the anchored digest, the committed MINT-TIME CONFIGURATION BLOCK, the aggregation path and a per-chain list whose entries carry all FOUR elements whole. Refuses a partial entry by shape, a deferred transaction, a missing configured set, a single-chain shape, and any state member |
| [`anchor-state.schema.yaml`](anchor-state.schema.yaml) | PER-WITNESS STATE for one anchored item, the three disjoint states, and the two explicit transitions out of pending. Refuses a transition with no leaf, a completeness claim with no captured receipt, and an aggregate `anchored` boolean |
| [`verification-result.schema.yaml`](verification-result.schema.yaml) | ONE VERIFICATION'S ANSWER with its MANDATORY VERIFICATION MODE, its horizon base, its witness shortfall and its delay check. Refuses a result with no mode, a `receipt_only` result claiming stateful knowledge, a determination made on a minter-claimed base, and a delay check read as compliance |
| [`anchor-bound-commitment.schema.yaml`](anchor-bound-commitment.schema.yaml) | THE ONLY KIND OF VALUE THIS CAPABILITY PUTS ON A CHAIN, with its DECLARED CONSTRUCTION and both custody references. Refuses a payload by shape, an absent or unkeyed-unsalted construction, a custody reference reachable from the anchor, a missing entropy declaration and a salt below the floor. Carries no free-text member at all |
| [`log-checkpoint-anchor.schema.yaml`](log-checkpoint-anchor.schema.yaml) | A CHECKPOINT ANCHOR and its `const` NEVER-READ-AS-VALIDATION DISCLAIMER. Refuses a record that omits or alters the disclaimer, and a realization presenting checkpoint inclusion as validation |
| [`consent-checkpoint-commitment.schema.yaml`](consent-checkpoint-commitment.schema.yaml) | A COMMITMENT TO A CONSENT LOG'S CHECKPOINT — the only thing of that log a chain sees. Refuses a per-subject row, enforcement as on-chain contract code, and revocation presented as recall |
| [`plane-separation-declaration.schema.yaml`](plane-separation-declaration.schema.yaml) | PER-PLANE KEYS UNDER PER-PLANE SALTS, the identifier policy, and the correlation mechanism. Refuses a key shared across planes, a direct identifier in the record or demographic plane, a shared cross-plane join key, and an anchored commitment used as one |
| [`linkage-derivation-issuance.schema.yaml`](linkage-derivation-issuance.schema.yaml) | THE ONE LAWFUL CROSS-PLANE CORRELATION PATH at issuance. Refuses a derivation minted outside the identity plane, one without an anchored consent checkpoint, one that neither expires nor is revocable, and a parameter reused across analyses |
| [`linkage-derivation-use.schema.yaml`](linkage-derivation-use.schema.yaml) | ONE USE of an issued derivation and the CURRENT revocation state it answered to. Refuses a correlation performed while that state is revoked or unreadable, and a use naming a different analysis |
| [`analysis-result.schema.yaml`](analysis-result.schema.yaml) | THE OUTCOME DISCRIMINATOR, the named omitted correlation with its enumerated ground, and the per-plane results carried distinctly. Refuses a status outside the enumeration, a free-text ground, a silently partial result, and a de-identified label with no named determination behind it |
| [`conformance-declaration.schema.yaml`](conformance-declaration.schema.yaml) | A realization's obligation-by-obligation declaration over `CA-R1 … CA-R9` on `add-trust-anchor`'s ratified declared-shortfall pattern, plus the POSTURE members a validator adjudicates. Refuses an undeclared obligation and a structural residual recorded as satisfied. **CA-R10 and CA-R11 are the amendment's two, and the set is eleven because the capability is** |
| [`confirmation-profile.schema.yaml`](confirmation-profile.schema.yaml) | ONE OPERATOR-APPROVED CONFIRMATION PROFILE for one witness network: the objective condition separating SUBMITTED from CONFIRMED, the proof material retained at confirmation, the reorganization and replacement rules, and positive and refusal vectors at every transition boundary. **It names no depth**, and a depth carried with no citation behind it is refused — a neutral contract naming one would be asserting a number about somebody else's consensus rules |
| [`confirmation-profile-registry.schema.yaml`](confirmation-profile-registry.schema.yaml) | THE APPEND-ONLY SIGNED REGISTER those approvals are published into, and the one place a UTC window resolves its version from. Refuses a configured network with no active entry (the amendment's BLOCKED state, MEASURED), a rewritten history, a rollback past an activation checkpoint, a non-operator approval, and a retired or compromised version minting a new receipt |
| [`daily-merkle-profile.schema.yaml`](daily-merkle-profile.schema.yaml) | THE RELEASED IMMUTABLE CONSTRUCTION a window's batch is built under: canonical leaf encoding, SHA-256, DISTINCT leaf and node domain separators, ordering, shape, odd-node handling, and the deterministic empty root. **A Merkle root without a construction is a number, not a proof**: two honest implementations that disagree about odd-node handling compute different roots over the same events and neither can show the other wrong |
| [`durability-eligibility-registry.schema.yaml`](durability-eligibility-registry.schema.yaml) | THE DENOMINATOR, append-only and snapshotted at window open. *"Every accepted event exactly once"* is a claim about a SET, and a completeness proof over a denominator its own author chose proves nothing. Every conforming entry excludes `anchoring_control` from the count, which is what permits genuine consecutive empty windows |
| [`durability-batch-admission.schema.yaml`](durability-batch-admission.schema.yaml) | ONE ATOMIC ADMISSION of one event into one fixed UTC window — the trusted acceptance time that SELECTS the window, the sequence that orders events within it, the dedupe rule and its off-chain key custody, the window's two snapshots, and the membership path. Refuses a non-fixed window, a window selected from source time, a non-atomic admission, a replay that spent a sequence, a key reused for different content, a control leaf offered as an event, and an event holding its own receipt |
| [`durability-batch-manifest.schema.yaml`](durability-batch-manifest.schema.yaml) | THE CANONICAL SIGNED MANIFEST of one closed window, and THE ANCHORED ITEM of this profile. Its summaries are DERIVED from the checkpoint-covered admission set, so a manifest that lowers its last sequence and count to match a retained prefix is refused even though its three numbers and its root are perfectly self-consistent. Continuity is over the previous item's CONFIGURATION-BOUND anchored digest and never over its batch root |

## The canonical reader and its packaged corpus

The reader is [`scripts/validate-chain-anchoring.py`](../../scripts/validate-chain-anchoring.py),
run from the openxFactory checkout:

```bash
python3 scripts/validate-chain-anchoring.py          # self-test only
python3 scripts/validate-chain-anchoring.py .        # plus whole-tree scan
```

**It is the named reader of requirement 5 — the refusing validator the on-chain
boundary consists of — and it is not yet a required check**, which is why the
packaged conformance declaration records `is_required_in_ruleset: false` in the
present tense and why every run carries the standing `reader-not-required`
warning (with a second honest warning, `archival-node-undeclared`, for the 4.5
operator gate). Beyond shape conformance it RECOMPUTES the receipt's anchored
digest over `{material_digest, mint_time_configuration}`, checks the four
per-chain elements and the structural half of canonicality, enforces the closure
rule and the state vocabulary as RULES (name sweeps at any depth), applies the
timing model in its declared direction — the future-dated mint refused beyond
the skew, its honest twin accepted within it, the breach margin one-directional,
the delay check never read as compliance — reconciles the witness shortfall
arithmetic against the committed set, walks the plane/linkage/consent refusals
across the WHOLE scope (a reused derivation parameter, one key under two planes
and a receipt entry for an in-flight witness are properties of a SET, not of a
record), and closes the conformance declaration over `CA-R1 … CA-R9` in both
directions. Its docstring carries the full ordered check list and — at equal
length — WHAT IT DOES NOT DO: it reaches no chain, fetches no header set,
cannot tell a declared salted keyed commitment from a plain digest by
inspection (`CA-R5-COMMITMENT-PATH`, the declared structural residual), and
adjudicates records rather than a running anchoring subsystem.

The packaged corpus under [`examples/`](examples/) is 41 positive records
validated as ONE coherent scope — the healthy dual-witness receipt, the
ordering-only chain with its `no_determination` verification, the honest twin
accepted within the skew, the sat-on minter exposed by the checkpoint bracket
(`breach_proven`), the served/local verification pair over one item, the
three-state anchor lifecycle, the correction anchored forward, the
declared-shortfall conformance declaration, and — from the amendment — the two
immutable profile versions with their retired predecessor kept in place, the
append-only register, the released construction, the versioned denominator, and
THREE CONSECUTIVE FIXED-UTC WINDOWS: a first day with the genesis sentinel, an
EMPTY second day whose count-zero item enters both witnesses, and a third
carrying both an acceptance at exactly `00:00:00Z` and a late-source-time event,
with their admissions (a replay acknowledgement that consumes no sequence among
them), their receipts on the identity aggregation path, and both anchor states —
both witnesses confirmed, and *"OpenTimestamps submitted and Bitcoin pending"* in
the amendment's own words. **Every batch root and membership path in the corpus
is COMPUTED under the released construction rather than written by hand**, so the
reader's recomputation has something real to disagree with — plus, under
[`examples/negative/`](examples/negative/), **one single-fault fixture per
refusal code, its FILENAME the code it provokes**: 118/118 closed codes
red-proven, plus eight finding codes outside the closed enumeration
(`ordering-only-correspondence`, `delay-check-arithmetic`,
`checkpoint-anchor-mismatch`, `record-digest-mismatch`,
`residual-not-declared`, `admission-window-acceptance-mismatch`,
`registry-entry-predecessor-unresolved`, `merkle-domain-separators-equal`,
`profile-transition-vectors-incomplete`) for the semantic rules whose codes the enumeration
does not carry, because inventing a member there would be a contract change
made by a reader. Negatives are adjudicated INSIDE the positive scope, with an
`# expected_failure:` code and an `# expected_failure_detail:` substring each,
and the self-test refuses a code with no probe, a misnamed fixture, and a
fixture that fails for the wrong reason. `tests/chain_anchoring/` holds two
pytest modules: `test_anchoring_reader.py` pins what the self-test cannot check
about itself — the direction pairs, the depth-blindness of the payload sweep,
the corpus's digests actually recomputing, and the exit codes a future gate
would grep for — and `test_durability_and_confirmation_scenarios.py` pins THE
RATIFIED DELTA, with **one test per scenario, thirty-four of them, each named
for the scenario it holds**.

## The timing model lives in one place, and so does its direction

Three consecutive rounds of adversarial review on this packet found DIRECTION
ERRORS — a bound asserted the wrong way round, a clock trusted from the wrong
party, an inequality read backwards — and a model spread across a dozen files is
exactly the object in which a direction error hides. So the model is stated ONCE,
in the receipt requirement, and this family's shapes carry it rather than
restating it:

- **Three clocks and only three.** The CHAIN-ACCEPTED TIME derived from a
  per-chain entry's own block header under that chain's declared rule; the
  CHECKPOINT ANCHOR TIME the log contributes, which is the only clock that bounds
  the submission; and the minter's DECLARED SUBMISSION TIME, which is an
  ASSERTION and not a clock. The receipt therefore offers no capture time, no
  observation time and no mint time — a fourth, uncheckable clock is a field this
  family declines to provide.
- **A header time NEVER upper-bounds the submission.** Consensus does not compare
  a header time to any submission's wall clock, so a valid accepting block may
  carry a time EARLIER than the material was submitted. *"Material cannot be
  anchored before it is submitted"* is true of the ACT and false of the
  TIMESTAMP. An honest receipt whose declared submission falls after its header
  time, within the declared skew, is ACCEPTED.
- **One declared skew serves both uses.** The same per-chain value feeds the
  horizon computation and the self-consistency refusal, so two margins cannot
  drift apart — and the margin is applied in ONE DIRECTION on purpose, because a
  FALSE breach raises the operator obligation on a sound item and turns the
  signal into noise, while a slightly LATE breach is still caught on its own
  transition leaf.
- **A delay check PROVES A BREACH and NEVER PROVES COMPLIANCE.** It rests on a
  lower bound from the containing checkpoint. *Not-provably-breached is not
  compliant*, the residual is exactly one cadence interval, and the bracket's
  width is reported rather than a bare pass.
- **The closure rule is why the model can be read as complete.** EVERY value the
  receipt-only computation reads lives in the MINT-TIME CONFIGURATION BLOCK and
  is therefore committed by the anchored digest; a realization carrying such a
  value anywhere else is REFUSED. The rule is stated rather than the fields
  enumerated, because three separate rounds added a field OUTSIDE the block and
  each had to be swept in afterwards: the failure was never in any one field, but
  in adding them singly. **A future timing input joins the block by the rule, not
  by an enumeration chase.**

## What was settled before these schemas were authored, and what was not

`tasks.md` §5 required four things to be fixed first. Two of them are contract
content and are settled here; two are realization decisions these contracts
deliberately do not fix, and saying which is which is the honest state.

**SETTLED — the twelve leaf kinds.** Requirements 3, 4, 7 and 8 each mandate
leaves and none of them defines a field, so the shapes are settled INSIDE tranche
one's leaf grammar,
[`../signed-execution-chain/transparency-log-leaf.schema.yaml`](../signed-execution-chain/transparency-log-leaf.schema.yaml),
and **this family adds no second grammar and defines no leaf**: every record here
references leaves by identifier only. The twelve are the `anchor-pending` entry,
the `horizon-breach` and `terminal-witness-failure` transitions, the
`anchor-completion`, the `item-anchor-refusal`, the `correction-anchored-forward`,
the `verification` and `verification-failure` pair, the `permitted-access` and
`refused-access` pair, and the `linkage-derivation-issuance` and
`linkage-derivation-use` pair. **One kind is deliberately excluded with its
ground stated**: requirement 4's validation-failure leaf is a GATE VERDICT, which
tranche one's ratified leaf set already carries, so settling it here would mint
the second grammar the task forbids.

**SETTLED — one digest construction, new subjects.** Every digest this capability
computes is `xfc-jcs-sha256-1` under
[`../signed-execution-chain/digest-construction.schema.yaml`](../signed-execution-chain/digest-construction.schema.yaml),
taken by `$ref` to its absolute identifier. A later tranche adds no second rule;
it adds SUBJECTS to that file's enumeration, on that file's own invitation. A
value another chain's consensus produced — a block hash, a foreign Merkle
sibling, a DAG acceptance path element — is NOT carried in that shape and takes
the definitions file's `chain_native_value` instead, because tagging a foreign
value as `xfc-jcs-sha256-1` would assert a construction that did not produce it.

**NOT SETTLED, AND NOT THIS FAMILY'S TO SETTLE — the anchored-item unit and the
timing numbers.** What exactly is anchored (a log checkpoint, a state root, or
both) and at what granularity the aggregation batches is `tasks.md` 5.1; the
declared horizons, `D_max`, the cadence, and each chain's skew and tolerance with
their cited consensus rules are 5.2. These shapes fix that all of them are
DECLARED, that they are integer seconds, and that every one of them sits inside
the committed block. **They name no numbers, and the fail-closed determination is
only as good as the numbers a realization declares.**

## What this family refuses, by name

**One hundred and eighteen closed refusal codes**, defined once at
`anchoring-definitions.schema.yaml#/$defs/refusal_code` and taken from there by
`$ref` wherever a record reports one. On tranche one's carried rule, the
canonical reader's self-test REFUSES a code with no negative example that
provokes it.

**Where a shape can refuse a thing, the shape refuses it.** A per-chain entry
short of any of its four elements, a mint-time configuration block grown a member
beside the ones it names, a subject member on a consent checkpoint, and a
free-text refusal ground are all UNREPRESENTABLE rather than refused.

**And where a refusal must NAME what was actually lacking, the value stays
writable.** A custody reference resolving onto a chain, a salt width below the
floor, a header source supplied by the minter, a third anchor target, a
`proves_compliance` delay reading — each of these is a value a record DECLARES,
so each is expressible and refused by name with its ground. A shape that cannot
say the wrong thing cannot carry the negative example that proves the refusal
fires, and a refusal nobody has provoked is a refusal nobody has tested.

## What this family does NOT carry, and why

- **No runtime, and nothing that reaches a chain.** The archival node for the
  operational witness, the aggregation-calendar client for the durability
  witness, and the batching scheduler are OPERATOR INFRASTRUCTURE commissioned at
  realization (`tasks.md` 4.5, 4.6, 4.7, 4.9) and gated there. Those boxes are
  UNTICKED, and no record here asserts a capability they would deliver.
- **No anchor target, endpoint, transaction identifier or block hash of any real
  chain.** The two-witness configuration is RULED and is declared by a
  realization in its conformance declaration; these contracts carry the roles and
  refuse a third target, and they name no chain.
- **No selection of a permissioned plane instance.** That is a realization
  decision (`tasks.md` 5.4) that this packet deliberately does not fix; naming
  one in a neutral contract would bind every consumer to an operational choice
  that answers to its own evidence.
- **No leaf grammar, the amendment's control leaves included.** The durability
  profile's control leaves — witness submissions, confirmations, batch
  manifests, continuity checkpoints — are referenced BY IDENTIFIER from the
  records that produce them, exactly as every other record here references a
  leaf, so the amendment needed no thirteenth anchoring discriminator and took
  none. It widened
  [`../signed-execution-chain/digest-construction.schema.yaml`](../signed-execution-chain/digest-construction.schema.yaml)'s
  subject enumeration by SIX on that file's own written invitation and touched
  nothing else in that family. A realization that wants those events
  discriminated IN THAT GRAMMAR is a successor act with its own evidence.
- **No leaf grammar.** The twelve mandated leaf kinds are settled in tranche
  one's
  [`../signed-execution-chain/transparency-log-leaf.schema.yaml`](../signed-execution-chain/transparency-log-leaf.schema.yaml)
  and nowhere else. Every record in this family references leaves by identifier;
  none of them defines one, because a second grammar is precisely what this
  tranche must not mint.
- **No second digest construction.** See above. One construction, new subjects,
  and a foreign chain's own values kept visibly distinct from both.
- **No domain semantics of any kind.** No domain's record kinds, no regulating
  body, no product surface, and **no de-identification standard**. The
  de-identification member on the analysis result is a REFERENCE HOOK to a
  determination made elsewhere and never a standard: this capability names none,
  presumes none, and stands in for none. Domain products instantiate this
  capability through DIGEST-PINNED overlays owned by their own repositories, and
  an overlay may ADD refusals and never remove one.
- **No claim that a receipt is self-sufficient against a forged history.** A
  receipt cannot carry a whole chain. What it delivers is that a receipt is
  CHECKABLE against a canonical header set the verifier obtains for itself — the
  trust root is a public chain the verifier can reach, never a header this
  capability handed it.
- **No claim that anything anchored can be withdrawn.** A correction is anchored
  FORWARD as new material. The only erasure property offered anywhere here is
  salt destruction, it belongs to the COMMITMENT rather than to the anchor, and
  it makes the handle PERMANENTLY UNVERIFIABLE by the same act that makes the
  residue anonymous.
- **No census of every verification of anchored material anywhere.** The
  completeness claim is over the SERVED surface and names which surface that is.
  A holder verifying a receipt on its own machine is invisible here BY
  CONSTRUCTION, that invisibility is the receipt's self-sufficiency working as
  designed, and closing it with a reporting obligation on independent verifiers
  is refused for what it would cost.
