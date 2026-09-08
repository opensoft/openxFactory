## Context

`add-chain-anchoring` is the ratified tranche-three packet and the sole surviving
anchoring capability. The repository owner rejected the stale competing
`add-signed-execution-chain-anchoring` draft as superseded. A requirement-by-
requirement comparison found that the survivor already covers or strengthens
the competing packet's receipt integrity, configured-witness binding,
permissioned consent seam, keyed commitments, pruning-resistant proof capture,
claim-level witness failure, programmable-chain boundary, and neutral ownership.

Three useful obligations were originally found unique. First, the survivor
records the PKI prerequisite in design/tasks but not in normative contract
text. Second, it requires Bitcoin-via-OpenTimestamps on every anchored item but
does not define deterministic daily membership, replay, lateness, or
empty-window continuity. Third, it has a strong receipt/state split but does
not state the network-facing submitted-versus-confirmed distinction that
prevents interface acceptance or a detached timestamp proof from being
consumed as completed witness evidence.

**Update, 2026-09-04 (owner's ruling on PR #548): the first of the three —
the PKI-prerequisite realization gate (D2 below) — is DROPPED.**
`add-chain-anchoring` has since realized (PR #629, squash `11feff75`) without
it. Only the second and third obligations (D3, D4) remain part of this
amendment; D2 is retained below as the historical record of a decision this
amendment no longer makes, not as current scope.

## Goals / Non-Goals

**Goals:**

- Preserve the single `chain-anchoring` capability identity.
- Define one deterministic fixed-UTC durability batch for every accepted event.
- Preserve immutable membership under replay and late source-time arrival.
- Make submitted and confirmed witness evidence mechanically distinguishable.
- Reuse the survivor's receipt, anchor-state, timing, and proof-capture model.

**Non-Goals:**

(The goal of making the PKI realization dependency normative and fail
closed is DROPPED along with D2 and requirement 1 — see "Update,
2026-09-04" in Context above.)

- Reopen the two-witness configuration, its ordering, or its no-selectivity rule.
- Reintroduce `signed-execution-chain-anchoring` as an alias or second profile.
- Define or operate a provider-neutral policy gateway, PKI service, chain client,
  scheduler, retry worker, or evidence store.
- Move domain authorization, medical policy, credentials, or payloads into
  openxFactory or onto a public chain.
- Claim a released contract or participating runtime before realization.

## Decisions

### D1 — Preserve only semantic gaps, not the superseded packet's identity

The follow-up modifies `chain-anchoring`; it creates no alias and no second
capability. Requirements already covered by the survivor are not copied. The
provider-neutral gateway text is deliberately excluded because anchoring is an
evidence capability and the survivor correctly keeps protected-operation
enforcement with the consumer/runtime owner.

**Alternative rejected:** copy the superseded packet wholesale. That would
recreate the duplicate canon, weaken stronger survivor text, and bind unrelated
consumer enforcement to a witness contract.

### D2 — The PKI dependency becomes a normative realization gate [DROPPED]

**DROPPED, owner's ruling 2026-09-04 on PR #548 ("bring 548 forward after 629
lands, drop requirement 1"): no longer part of this amendment.** This decision
backed requirement 1, which is removed from `specs/chain-anchoring/spec.md`.
`add-chain-anchoring` has since realized (PR #629, squash `11feff75`) without
this gate, on the owner's own separate ruling on #629 ("merge 629, register
now"); ratifying D2 now would retroactively call that landed realization
illegitimate. See `proposal.md`'s "Requirement 1 removed" for the full
reasoning. The original decision text is kept below, unedited, as the record
of what was decided and then superseded — not as current scope.

<details>
<summary>Original D2 text (superseded 2026-09-04, kept for the record)</summary>

Tranche-one signed-execution-chain contracts are now realized at
`contract-v2.5`, but its own archive record leaves the live branch-ruleset act
and broken-chain canary open at issue #534. A workflow file or a reader
declaration with `is_required_in_ruleset: false` confers no permission. The gate
therefore requires the live `signed-execution-chain-gate` token to be REQUIRED
and its broken-chain canary to fail before anchoring realization begins. The
other surviving live gate is the operational PKI plane: governed issuance,
verification, revocation handling, and chain custody under released
`trust-anchor` contracts. Repository seeds, topology plans, workflow files, or
contract pins alone do not establish that plane.

The contract gate blocks realization, not authorship or ratification of this
amendment, and requires released signed-log contract/validator artifacts rather
than pretending a service exists. Runtime commissioning has a second gate: a
named operational log instance with signer chain, custody owner, reachable
interface, current checkpoint, and successful validator result. This preserves
the distinction between governing a contract and falsely claiming its runtime
dependencies already operate.

</details>

### D3 — Trusted log acceptance owns one non-recursive daily durability item

Daily windows are consecutive half-open UTC intervals. One atomic log-admission
transaction validates a declared durability-eligible owner-evidence event,
deduplicates it, records trusted acceptance time, selects the window from that
time, and assigns the next monotonic sequence. Acceptance time selects the
window; sequence orders events inside it. Source time is descriptive only. A
window close serializes after every admission assigned before its exclusive
boundary and before the first admission assigned to the next window, so midnight
cannot place one accepted event on both sides. The close transaction records a
signed-log sequence watermark and resolving checkpoint covering that watermark;
the validator derives the complete eligible admission set from that checkpoint,
so caller-supplied first/last/count summaries cannot hide an omitted suffix.

The owner-local dedupe key is stable and never public. Same key and same digest
returns the original admission acknowledgement (leaf sequence plus material
digest) without a new sequence or a pre-closure anchor receipt; same key and
different digest is refused before sequence assignment. A versioned eligibility registry
defines the neutral owner-evidence event kinds counted by this profile. The
registry is signed and append-only; each UTC window snapshots one active version,
content digest, activation checkpoint, and standing, and the canonical manifest
binds that snapshot. Successor activation atomically retires its predecessor and
closes the predecessor's half-open effective interval. Window open selects the
unique non-compromised entry covering that boundary with the greatest activation
checkpoint; zero/multiple matches and older-version rollback are refused.
Mid-window activation applies only to the next window. A
domain overlay maps its events into those kinds and cannot make a per-event
inclusion choice after acceptance. Anchor-state transitions, witness submissions,
confirmations, batch manifests, and continuity checkpoints are CONTROL leaves,
not inputs to the same batch they produce. They remain in the signed log and its
checkpoint anchors, which prevents recursive self-inclusion and allows genuine
consecutive empty days. Every eligible accepted sequence in the window appears
exactly once. An empty window emits a linked count-zero checkpoint so silence is
distinguishable from a missed scheduler run.

**The anchored-item unit is the closed canonical daily manifest, not each
constituent event or its raw Merkle root.** The proof chain is explicit: event
membership produces `daily_batch_root` under one released, immutable construction
profile that fixes canonical leaf encoding, SHA-256/domain separation, sequence
ordering, tree shape, odd-node handling, and the empty root. Canonical manifest
bytes bind that profile's id/version/content digest, the root, the immediately
preceding daily item's anchored digest, and all window/accounting fields; the
ratified construction hashes those bytes
to `material_digest`; the ratified configuration binding produces
`anchored_digest`; and the identity shared aggregation path yields
`aggregation_root == anchored_digest`. Both witness-specific commitment paths
begin at that SAME aggregation root (direct Kaspa payload binding and detached
OpenTimestamps operations path). Thus witness configuration, horizons, timing,
profile versions/digests/activation checkpoints, and standing evidence remain
inside the public proof. Different raw roots, uncommitted configuration, or
broken manifest/digest links are refused.

After window closure, the same configuration-bound aggregation root enters
direct Kaspa first, then Bitcoin-via-OpenTimestamps. The existing receipt's one
aggregation root and both-witness entries describe one item; no witness-specific
source item, cadence, or bespoke receipt is introduced. Different proof paths
are required; different aggregation roots are refused.
Kaspa's
operational value is the seconds-scale answer after a daily item closes; the
open window remains covered by the signed owner-local log, not by a false claim
that every constituent event already has a public witness. This explicitly
settles `add-chain-anchoring` task 5.1 for the daily profile.

### D4 — Submission lives in anchor state; confirmation earns a whole receipt entry

Network/interface acceptance is submitted evidence, not confirmation. A Kaspa
submission remains submitted while the overall item is pending until the
referenced approved confirmation profile is satisfied and all four receipt
elements are captured. An OpenTimestamps detached proof remains
submitted/pending until it is upgraded with independently verified Bitcoin
transaction, inclusion, header, and chain-acceptance evidence.

The confirmation rules are operator-approved profiles in an append-only signed
registry, not numbers selected during schema implementation. Registry entries
bind immutable version/content digest, approval, predecessor, activation log
checkpoint, effective interval, and active/retired/compromised standing. Each
UTC window snapshots one active profile per witness; every event and the final
daily item inherit that snapshot, and mid-window activation applies only to the
next window. Rollback, future, retired, compromised, or digest-substituted
profiles at window open are refused. Historical receipts retain as-of evidence
while current verification reports current standing and refuses new long-horizon
claims from non-active profiles.

The existing receipt/state split remains intact: submitted and in-flight facts
live in the anchor-state record; the receipt gains a per-chain entry only when
the entry is whole. Upgrade appends the completed durability entry against the
same anchored digest and does not re-anchor the item. Verification reports each
witness separately and long-horizon claims require confirmed durability
evidence.

**Alternative rejected:** store half-filled receipt entries. That conflicts with
the survivor's capture-time refusal and allows a caller to confuse incomplete
proof material with an independently verifiable receipt.

## Risks / Trade-offs

- **[A fixed daily window adds latency to durability completion]** → retain the
  signed owner-local log during the open window, then send the same closed daily
  item to the operational witness first; never promote pending to a long-horizon
  claim.
- **[Clock ambiguity changes membership]** → use trusted log acceptance time and
  atomic sequence, never source time.
- **[A self-consistent prefix omits accepted suffix events]** → bind the atomic
  close watermark and resolving signed-log checkpoint, then derive the complete
  eligible set from the checkpoint rather than trusting manifest summaries.
- **[Replay consumes sequence space or duplicates a batch leaf]** → enforce the
  stable owner-local dedupe rule before sequence assignment.
- **[Control leaves recursively make an empty batch non-empty]** → count only
  versioned durability-eligible owner-evidence events; keep anchoring-control
  leaves in the signed log/checkpoint path outside the batch they produce.
- **[Eligibility or confirmation policy changes inside an open day]** → snapshot
  immutable registry entries at window open, bind their content digests and
  activation checkpoints into the item, and activate replacements next window.
- **[An empty day is mistaken for scheduler failure]** → require a linked,
  signed count-zero checkpoint through the same durability path and link each
  manifest to the prior item's anchored digest rather than its repeatable empty
  event root.
- **[Different implementations derive different daily roots]** → approve and
  release one digest-bound Merkle construction profile before schema authoring;
  the canonical validator recomputes leaves, paths, and roots from it.
- **[A submitted proof is consumed as confirmation]** → use separate states and
  refuse long-horizon claims until complete independently verifiable evidence is
  captured.
- **[A weaker once-approved profile is selected after a stronger activation]** →
  bind registry activation checkpoint, content digest, and standing into the
  anchored configuration and refuse rollback/non-active versions.
- **[The event root is anchored without receipt configuration]** → recompute the
  full manifest → material digest → anchored digest → aggregation root chain and
  refuse any substituted node or uncommitted configuration.
- ~~**[PKI paperwork is mistaken for an operational plane]** → require evidence of
  issuance, verification, revocation, and custody, not repository artifacts.~~
  (D2's risk, DROPPED 2026-09-04 with D2 and requirement 1 — see Context above.)

## Migration Plan

(Steps 1-2 and 4 below were requirement 1's / D2's and are superseded, kept
struck for the record rather than renumbered or deleted — 2026-09-04, owner's
ruling on PR #548. `add-chain-anchoring` has realized without them, PR #629.)

1. ~~Ratify this amendment without commissioning implementation.~~ Ratify
   requirements 2 and 3 without commissioning implementation.
2. ~~Verify the released signed-execution-chain baseline, the live REQUIRED
   `signed-execution-chain-gate`, its broken-chain canary, and operational PKI.~~
3. Approve and publish append-only Kaspa and Bitcoin confirmation-profile
   registry entries and transition/refusal vectors before schema authoring.
4. ~~Link this amendment and `add-chain-anchoring` to ONE shared Speckit feature,
   so no unreleased "existing" schema is assumed and both packets map to one
   realization rather than competing implementations.~~ No shared-feature
   mandate survives requirement 1's drop; `add-chain-anchoring` already
   realized independently at PR #629.
5. Add deterministic fixtures for non-empty, empty, midnight-boundary, replay,
   conflicting-dedupe, late-source-time, submitted-only, and confirmed-upgrade
   cases.
6. Archive `add-chain-anchoring` first, then archive this dependent amendment,
   and cut their additive contract release only after both delta sets are
   present. If the basis releases without this amendment, stop and re-evaluate
   compatibility/versioning rather than claiming this path remains an additive
   first release.
7. Commission no participating runtime until its operational signed-log instance
   evidence resolves separately from the released contract artifacts.

Rollback removes the unreleased additive amendment. Once released, corrective
changes supersede the release; they do not rewrite prior receipts or inventories.

## Open Questions

None at authoring time. Ratification review may reject or amend the fixed daily
profile, but implementation receives no discretion to choose different window,
dedupe, lateness, or confirmation semantics after ratification.
