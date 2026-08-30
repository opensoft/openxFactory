## Context

The ratified `add-signed-execution-chain` change defines tranche one: signed
ratification and chain inception, a traveling contract, an append-only signed
transparency log, and a short-chain required check. Its specification declares
one remaining integrity limit: a fresh reader cannot detect deletion of an
unobserved log suffix until a tree head is witnessed outside the governed
store. That change names this exact successor id for the anchoring tranche.

The staged topic subsequently fixed the witness ordering: Kaspa first as the
operational witness, under proof-retention and corroborating-only conditions,
and Bitcoin via OpenTimestamps on every item as the durability witness. The
usage-controlled-evidence-chain brainstorm packet further fixes a provider-
neutral off-chain gateway as the enforcement point, direct Kaspa L1 as the v1
publication surface, asynchronous publication, and a fixed-UTC 24-hour
durability cadence.

The predecessor also places consent and policy state in a governed permissioned
plane whose checkpoint state roots are anchored, and says tranche three remains
held until the PKI plane is real. This design can govern contracts before those
inputs exist, but it cannot be handed to implementation as if they already do.
Realization evidence for tranche one and for a `trust-anchor`-conformant PKI
plane are therefore hard predecessor gates. The existing
`implement-openxpki-install-repo` seed is an ownership and repository boundary;
it is not by itself evidence that an issuing, verifying, revoking, chain-custody-
declaring PKI plane is operational.

## Goals / Non-Goals

**Goals:**

- Close tranche one's declared unobserved-suffix gap with independently
  verifiable external witnesses.
- Define domain-neutral evidence, checkpoint, witness-state, retained-proof,
  receipt, and verification-result contracts.
- Preserve owner-local enforcement and payload custody while making witness
  publication complete, progressive, and independently checkable.
- Preserve a domain-neutral permissioned consent-checkpoint/state-root seam
  without moving consent rows, identifiers, salts, or medical meaning on chain.
- Deliver immediate direct Kaspa L1 operational evidence and complete daily
  OpenTimestamps/Bitcoin durability evidence for every accepted event.
- Keep the network-facing lifecycle asynchronous and explicit about pending,
  submitted, confirmed, failed, and invalid states.
- Require operator-approved, versioned Kaspa and Bitcoin confirmation profiles
  before schemas or validators encode submitted-to-confirmed transitions.
- Hand all realization work to exactly one Speckit feature after the predecessor
  gate is satisfied.

**Non-Goals:**

- Implementing or operating a policy gateway, Kaspa client or node,
  OpenTimestamps calendar, Bitcoin client, scheduler, retry worker, archival
  service, key service, provider adapter, or monitoring system.
- Defining clinical consent, medical policy, reimbursement policy, retention
  periods, or the meaning and authorization of an owner-local event.
- Publishing PHI, encrypted PHI, financial detail, plain hashes, stable public
  subject or resource identifiers, consent rows, salts, keys, or payloads.
- Treating an anchor as proof that an event was truthful, authorized, retained,
  deleted, clinically correct, or legally sufficient.
- Giving Toccata, Kasplex, Igra, or any public-chain contract runtime a
  production role in v1.

## Decisions

### D1 — Tranche-one realization and the real PKI plane are hard handoff gates

The OpenSpec packet may be prepared now, but no Speckit feature is commissioned
and no realization starts until both gates have durable evidence. First,
`add-signed-execution-chain` has released contracts, a running transparency-log
and chain-validator surface, required-check ruleset state, and predecessor
realization verification. Second, the PKI plane named by that ratified packet is
real under released `trust-anchor` contracts, with evidence of governed
certificate issuance, verification, revocation handling, and declared chain
custody sufficient for the signatures this capability consumes. A repository
seed, contract pin, planned topology, or workflow file alone does not satisfy
the second gate. The successor consumes the evidenced artifacts rather than
designing against placeholders.

**Alternative rejected:** starting the anchoring feature in parallel. That
would force the receipt and checkpoint contracts to guess at leaf identity,
digest construction, verifier behavior, and signer trust that the predecessors
still own.

### D2 — The provider-neutral off-chain gateway enforces; chains witness

The owner runtime routes protected provider operations through a provider-
neutral gateway that authenticates actor and workload, evaluates the owning
policy, reads the governed permissioned consent/policy plane, enforces the
provider call, and emits signed outcome evidence. Missing policy, consent,
identity, revocation, or key authority fails closed there.

Kaspa and Bitcoin attest only that opaque committed bytes existed by a witnessed
time and remain consistent with retained proof. A network failure creates
`anchor_pending`, retry, and escalation; it neither grants a refused operation
nor retroactively refuses an otherwise authorized one. Direct credentials that
bypass the gateway are non-conforming owner-runtime behavior, not a condition a
public chain can repair.

**Alternative rejected:** using a public-chain contract as the authorization
engine. It cannot directly control an EMR, FHIR server, KMS, or other provider
credential and adds public metadata and a second execution trust boundary.

### D3 — The neutral kernel accepts opaque owner evidence

An owner signs and admits an event to its append-only evidence log before either
network acts. The neutral contracts bind a stable off-chain event identity to a
leaf digest, log sequence, checkpoint range, predecessor checkpoint, contract
version, and progressive receipt. Event meaning and authorization remain with
the owner; the shared surface receives no domain purpose or policy semantics.

Checkpoint continuity binds an exact ordered leaf range and the previous
checkpoint root. This extends tranche one's signed log without replacing it and
makes omission, reordering, and silent restart detectable against a retained or
externally witnessed checkpoint.

**Alternative rejected:** a universal cross-domain event schema. It would leak
medical, financial, and provider semantics into the neutral layer and transfer
policy ownership to openxFactory.

### D4 — Permissioned consent checkpoints expose a neutral state-root seam

Consent rows, granular access state, subject identifiers, salts, and policy
meaning remain in the governed permissioned plane. That plane emits a signed,
domain-neutral checkpoint envelope carrying its opaque state root, checkpoint
sequence, predecessor root, policy-contract version, and signer reference. The
public witness receives only a keyed commitment to that checkpoint and state
root, never the state itself. The provider-neutral gateway consumes the
permissioned plane directly; a public anchor corroborates checkpoint existence
and continuity and does not make the authorization decision.

The seam does not mandate a consortium-ledger product and does not define
clinical consent semantics. It defines the checkpoint and adapter contract a
domain-owned permissioned implementation supplies. The checkpoint signer and
its chain resolve through the evidenced PKI plane under `trust-anchor`.

**Alternative rejected:** omitting the seam because medical policy is out of
scope. The ratified tranche-three boundary includes the permissioned consent
plane's anchored state roots; preserving its neutral checkpoint interface does
not transfer domain meaning or runtime ownership to openxFactory.

### D5 — Public material is a high-entropy keyed commitment only

Each accepted event derives an algorithm-tagged keyed commitment using a unique,
high-entropy owner-held secret input. The key, salt or secret input, event
payload, policy state, and consent state stay off chain. The public Kaspa payload
contains only a versioned domain separator and the opaque commitment; daily
public witnesses contain only checkpoint or batch commitments and
non-identifying continuity material.

The contracts are closed against payload-shaped, ciphertext-shaped,
plain-hash, and stable-identifier fields. The reference validator refuses raw
PHI, encrypted PHI, plain record hashes, and stable public subject, patient,
payer, provider, wallet, grant, resource, or event identifiers. Salt destruction
can make a commitment no longer testable against its source, but an anchor proves
only that the commitment existed; it does not prove deletion.

**Alternative rejected:** encrypted payloads or plain SHA digests. Encryption
makes permanent ciphertext depend forever on key secrecy, while plain hashes of
predictable personal data remain correlatable and dictionary-testable.

### D6 — Direct Kaspa L1 is the primary operational witness

Every accepted event enters direct Kaspa L1 publication without Toccata,
Kasplex, Igra, or another execution layer. `primary` means first operational
answer, not sole or superior long-horizon evidence. The receipt begins with
`anchor_pending`, records a distinct Kaspa submitted state only after network
acceptance, and records Kaspa confirmed only after the declared confirmation
policy is satisfied.

The transition policy is not implementation discretion. Before schemas or
validators are authored, the operator approves versioned Kaspa and Bitcoin
confirmation profiles that define objective submitted and confirmed evidence,
reorganization or replacement handling, required proof capture, and conformance
vectors. Receipts bind the profile version used. This packet does not invent
numeric depths while the supporting evidence is unresolved; absent approved
profiles, schema and validator authoring remains blocked.

The retained Kaspa proof bundle grows with that progression. It preserves the
serialized transaction and payload, transaction identifier, accepting DAG
reference, transaction-to-DAG inclusion proof, relevant headers, node and
protocol versions, confirmation-policy identifier and result, and local signed
receipt material. Confirmation is not complete until the proof bundle needed by
the reference verifier has been captured. Ordinary-node pruning is treated as a
retention obligation, never as a future lookup plan.

**Alternative rejected:** a bespoke Kaspa receipt containing only a transaction
id or explorer URL. After pruning, neither proves inclusion, and it would make a
provider dependency part of the evidence contract.

### D7 — Every fixed UTC day produces one complete Bitcoin durability batch

The durability profile uses non-overlapping windows `[00:00:00Z, 00:00:00Z)`
on consecutive UTC dates. Admission is determined only by the trusted signed
log's UTC acceptance timestamp and atomically assigned monotonic leaf sequence;
owner source time is descriptive and never selects a batch. The log maintains a
stable owner-local dedupe key: replay of the same key and content resolves to the
existing leaf and receipt without consuming another sequence, while reuse with
different content is refused. Accepted leaves receive the next sequence exactly
once, and sequence and acceptance timestamp never change.

Every event accepted during a window is included, without selectivity, in one
ordered Merkle batch. The signed manifest binds the window boundaries, first and
last sequence when present, event count, batch root, previous batch root, close
reason, and late-arrival rule. A source-time event describing a prior window but
accepted now enters the current open acceptance window exactly once and records
its prior-window lateness off chain. A closed window is never reopened or
rewritten, including for such a late source-time event.

An empty window still emits a signed count-zero continuity checkpoint with a
deterministic empty root and the previous batch root, and that checkpoint follows
the same OpenTimestamps/Bitcoin path. This makes silence distinguishable from a
missing scheduler run or an omitted day.

OpenTimestamps submission and confirmed Bitcoin durability are separate states.
The former records the detached timestamp proof returned at submission; the
latter is reached only when the proof is upgraded with independently verifiable
Bitcoin inclusion and confirmation evidence. Each non-empty event receipt
carries its Merkle path into the daily root. Ten-year durability claims cite the
confirmed Bitcoin path, never Kaspa alone.

**Alternative rejected:** a rolling maximum-age policy or selective Bitcoin
anchoring. Both make completeness harder to reconcile, and selectivity recreates
the per-item judgment the Q3 ruling explicitly removed.

### D8 — One progressive, chain-agnostic receipt preserves state distinctions

Event and receipt identities are minted before network publication and do not
change as evidence progresses. Witness updates append to one receipt. Each
witness entry names its adapter and verifier profile, state, submission evidence,
confirmation evidence, retained proof, and failure or retry information. The
reference verifier reports valid, invalid, and pending paths separately; it
never converts pending or unevaluable evidence into confirmation.

The receipt format is chain-agnostic at the envelope and witness-specific inside
each proof entry. This allows later target changes without changing evidence-leaf
identity or weakening Kaspa- and Bitcoin-specific verification.

**Alternative rejected:** replacing a receipt at each phase or normalizing all
proofs into one lowest-common-denominator shape. The first creates competing
histories; the second discards the proof details needed after pruning.

### D9 — Programmable Kaspa surfaces are outside the v1 production path

Toccata has no production role in v1 and may be used only for isolated
non-production experiments carrying no PHI, production authority, provider
credentials, or conforming-path dependency. Kasplex and Igra are outside v1.
This change states no condition for adopting any of them later. Under ratified
Q5, a future governed change may
adopt contract code on then-current merits and evidence without satisfying a
condition pre-written here. The v1 off-chain provider gateway remains the
enforcement point this change defines.

**Alternative rejected:** carrying the brainstorm study's future promotion
criteria into normative text. That would recreate the advance trigger condition
Q5 expressly refused.

### D10 — openxFactory owns contracts and reference validation, not operations

The realization surface is limited to neutral schemas, examples, adapter ports,
consistency and state-transition rules, and reference validators. Exactly one
Speckit feature owns that realization so task truth is not duplicated across
features. Runtime repositories and product owners separately own deployable
gateways, network clients, credentials, nodes, calendars, schedulers, retries,
proof storage, monitoring, service levels, and incident response. Domain owners
own medical and other policy.

**Alternative rejected:** shipping a nominal reference service here. A service
would silently assign credentials, network operations, and regulated policy
responsibility to a repository whose role is neutral contract ownership.

## Risks / Trade-offs

- **[The open daily batch has no confirmed Bitcoin durability yet]** → expose
  the state as pending, retain Kaspa operational evidence, and never label the
  OTS submission as Bitcoin-confirmed.
- **[Kaspa transaction history is pruned]** → capture the full proof bundle as
  the receipt progresses and verify from retained material rather than an
  ordinary-node lookup.
- **[Asynchronous publication can accumulate backlog]** → require durable
  `anchor_pending`, retry and escalation records while leaving operational
  service levels to the runtime owner.
- **[A repository seed can be mistaken for a real PKI plane]** → require
  operational issuance, verification, revocation, and chain-custody evidence;
  explicitly reject a seed, pin, topology, or workflow as sufficient evidence.
- **[Clock or replay ambiguity can change daily membership]** → make signed log
  acceptance time and atomically assigned monotonic sequence authoritative,
  keep source time descriptive, and enforce stable dedupe before sequencing.
- **[Opaque commitments can still be correlatable if inputs are weak or reused]**
  → require unique high-entropy secret inputs, closed public shapes, and refusal
  of stable identifiers and plain hashes.
- **[An empty-day checkpoint adds operational cost]** → accept the cost because
  it is the evidence that distinguishes an empty window from an omitted one.
- **[An anchor may be over-read as authorization or truth]** → make verifier
  results state the narrow existence-and-integrity claim and keep policy outcome
  evidence distinct.

## Migration Plan

1. Verify and record completion of tranche-one realization and of the real PKI
   plane; stop if either gate's evidence is absent.
2. Commission exactly one Speckit feature from this OpenSpec change.
3. Obtain and record operator approval of versioned Kaspa and Bitcoin
   confirmation profiles, then fix exact canonical serializations; author no
   schema or validator before those prerequisites are complete.
4. Add the neutral contracts, positive and refusal examples, and reference
   validators without adding a deployable runtime.
5. Validate backward compatibility and cut the additive contract release under
   the repository's release-realization rules.

Rollback removes or supersedes the unreleased additive contracts. Once a bundle
is released, contract history is not rewritten; a corrective additive version
supersedes it. Network anchors already published are immutable evidence and are
never presented as rolled back.

## Open Questions

No governance question blocks the packet. Numeric Kaspa and Bitcoin confirmation
thresholds are not invented here because their evidence remains unresolved;
they are operator-governance inputs, not arbitrary implementation choices. The
single Speckit feature remains blocked from schema and validator authoring until
versioned operator-approved profiles define both transitions and their tests.
Canonical byte encodings and adapter vectors are then fixed against those
profiles before schema authoring.
