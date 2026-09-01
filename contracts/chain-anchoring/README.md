# Chain Anchoring Contract Family (tranche three)

Status: ratified
Ratified by: add-chain-anchoring (ratified 2026-08-30 by Brett Heap, repository
owner, in session, ruling item 2 of six — *"2 yes with note"*; record
`openspec/changes/add-chain-anchoring/review/ratification-2026-08-30.md`, taken
after the §7.4 council sitting of 2026-08-30 whose sole disposition of record is
`review/disposition-2026-08-30.md`)
Kind: reference
Repository context: openxFactory owns this neutral contract. It is **NOT YET
REGISTERED** in `contracts/manifest.yaml` or `contracts/CHANGELOG.md` — that is
`tasks.md` 4.11, performed by the cutting session at the next additive bundle cut
rather than by this realization, per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md), because a
proposed change MUST NOT reserve a minor number before merge order is known.
**AND NO CHECK REQUIRES THESE RECORDS YET.** Until a named reader runs as a
REQUIRED check on the repository that holds them, everything below confers and
refuses exactly nothing — the distinction tranche one's own README drew, and
which took it from realization on 2026-08-29 to a required check on 2026-08-31.
A merged workflow file is not evidence that a check is required; the live ruleset
state is. See § What this family does NOT carry for what else is outstanding.

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

## The twelve files

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
| [`conformance-declaration.schema.yaml`](conformance-declaration.schema.yaml) | A realization's obligation-by-obligation declaration over `CA-R1 … CA-R9` on `add-trust-anchor`'s ratified declared-shortfall pattern, plus the POSTURE members a validator adjudicates. Refuses an undeclared obligation and a structural residual recorded as satisfied |

The canonical reader is `scripts/validate-chain-anchoring.py`, self-testing over
the packaged corpus in `examples/` and `examples/negative/`.

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

**Seventy closed refusal codes**, defined once at
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
