## Context

`add-chain-anchoring` is the ratified tranche-three packet and the sole surviving
anchoring capability. The repository owner rejected the stale competing
`add-signed-execution-chain-anchoring` draft as superseded. A requirement-by-
requirement comparison found that the survivor already covers or strengthens
the competing packet's receipt integrity, configured-witness binding,
permissioned consent seam, keyed commitments, pruning-resistant proof capture,
claim-level witness failure, programmable-chain boundary, and neutral ownership.

Three useful obligations remain unique. First, the survivor records the PKI
prerequisite in design/tasks but not in normative contract text. Second, it
requires Bitcoin-via-OpenTimestamps on every anchored item but does not define
deterministic daily membership, replay, lateness, or empty-window continuity.
Third, it has a strong receipt/state split but does not state the network-facing
submitted-versus-confirmed distinction that prevents interface acceptance or a
detached timestamp proof from being consumed as completed witness evidence.

## Goals / Non-Goals

**Goals:**

- Preserve the single `chain-anchoring` capability identity.
- Make the remaining PKI realization dependency normative and fail closed.
- Define one deterministic fixed-UTC durability batch for every accepted event.
- Preserve immutable membership under replay and late source-time arrival.
- Make submitted and confirmed witness evidence mechanically distinguishable.
- Reuse the survivor's receipt, anchor-state, timing, and proof-capture model.

**Non-Goals:**

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

### D2 — The PKI dependency becomes a normative realization gate

Tranche-one signed-execution-chain contracts are now realized at
`contract-v2.5`, so the old "ratified but unrealized" branch is historical. The
surviving live gate is the operational PKI plane: governed issuance,
verification, revocation handling, and chain custody under released
`trust-anchor` contracts. Repository seeds, topology plans, workflow files, or
contract pins alone do not establish that plane.

The gate blocks commissioning/realization, not authorship or ratification of
this amendment. This preserves the repository's distinction between governing a
contract and falsely claiming its dependencies already operate.

### D3 — Trusted log acceptance owns daily membership

Daily windows are consecutive half-open UTC intervals. The signed log's trusted
acceptance timestamp and atomically assigned monotonic sequence determine
membership; source time is descriptive only. This prevents a late event from
reopening history and prevents a caller-controlled timestamp from selecting a
batch.

The owner-local dedupe key is stable and never public. Same key and same digest
returns the original leaf/receipt without a new sequence; same key and different
digest is refused. Every accepted sequence in the window appears exactly once.
An empty window emits a linked count-zero checkpoint so silence is distinguishable
from a missed scheduler run.

This does not weaken Q3's "Bitcoin-via-OTS on everything" ruling. Every event
has a Merkle path into the one daily root, and that root enters the durability
witness. Aggregation is how every event is covered without per-event Bitcoin
transactions.

### D4 — Submission lives in anchor state; confirmation earns a whole receipt entry

Network/interface acceptance is submitted evidence, not confirmation. A Kaspa
submission remains pending until the configured acceptance rule is satisfied and
all four receipt elements are captured. An OpenTimestamps detached proof remains
submitted/pending until it is upgraded with independently verified Bitcoin
transaction, inclusion, header, and chain-acceptance evidence.

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
  operational witness and explicit pending state; never promote pending to a
  long-horizon claim.
- **[Clock ambiguity changes membership]** → use trusted log acceptance time and
  atomic sequence, never source time.
- **[Replay consumes sequence space or duplicates a batch leaf]** → enforce the
  stable owner-local dedupe rule before sequence assignment.
- **[An empty day is mistaken for scheduler failure]** → require a linked,
  signed count-zero checkpoint through the same durability path.
- **[A submitted proof is consumed as confirmation]** → use separate states and
  refuse long-horizon claims until complete independently verifiable evidence is
  captured.
- **[PKI paperwork is mistaken for an operational plane]** → require evidence of
  issuance, verification, revocation, and custody, not repository artifacts.

## Migration Plan

1. Ratify this amendment without commissioning implementation.
2. Verify the released signed-execution-chain baseline and operational PKI gate.
3. Extend the existing chain-anchoring schemas, examples, refusal corpus, and
   validator through the surviving packet's one Speckit realization path.
4. Add deterministic fixtures for non-empty, empty, midnight-boundary, replay,
   conflicting-dedupe, late-source-time, submitted-only, and confirmed-upgrade
   cases.
5. Run strict OpenSpec and repository validation, then cut the additive contract
   minor allocated by merge order.

Rollback removes the unreleased additive amendment. Once released, corrective
changes supersede the release; they do not rewrite prior receipts or inventories.

## Open Questions

None at authoring time. Ratification review may reject or amend the fixed daily
profile, but implementation receives no discretion to choose different window,
dedupe, lateness, or confirmation semantics after ratification.
