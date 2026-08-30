# signed-execution-chain-anchoring Specification (delta)

## ADDED Requirements

### Requirement: Realization waits for the tranche-one chain and the real PKI plane

openxFactory SHALL NOT commission or realize the anchoring capability until the
ratified `add-signed-execution-chain` tranche has durable realization evidence,
including its released contracts, append-only signed transparency log,
canonical validator, required-check ruleset state, and realization verification,
AND until the PKI plane that ratified predecessor names is real. PKI evidence
SHALL demonstrate `trust-anchor`-conformant governed certificate issuance,
verification, revocation handling, and declared chain custody sufficient for
the log, checkpoint, and receipt signatures this capability consumes. An
install-repository seed, contract pin, planned deployment topology, or workflow
file alone SHALL NOT satisfy the PKI gate.

The anchoring capability SHALL consume those realized leaf, digest, checkpoint,
verifier, and signer-trust contracts rather than substitute provisional forms.
Once BOTH gates are satisfied, this change SHALL hand off to exactly one
Speckit feature.

#### Scenario: tranche one remains ratified but unrealized

- **WHEN** the predecessor has ratified text but lacks any required realization evidence
- **THEN** no Speckit implementation feature is commissioned for this change and no anchoring contract is realized

#### Scenario: tranche one is realized but the PKI plane is not

- **WHEN** all tranche-one evidence exists but the only PKI evidence is a repository seed, contract pin, planned topology, or workflow
- **THEN** no Speckit implementation feature is commissioned because the operational PKI predecessor remains unproven

#### Scenario: both predecessor gates are evidenced

- **WHEN** every named tranche-one artifact and required-check fact and every named PKI-plane fact is durably evidenced
- **THEN** this change may commission one Speckit feature that consumes those artifacts as its baseline

#### Scenario: a provisional predecessor shape is offered

- **WHEN** an anchoring design supplies its own leaf, digest, or log shape because the tranche-one form is unavailable
- **THEN** the realization is REFUSED rather than creating a parallel signed-execution-chain vocabulary

### Requirement: The off-chain provider-neutral gateway is the enforcement point

The contract family SHALL model a provider-neutral off-chain policy gateway as
the enforcement point for protected operations. A conforming owner runtime
SHALL route provider access through that gateway, which authenticates actor and
workload, reads the governed permissioned consent and policy plane, evaluates
owner-held purpose, scope, consent, role, expiry, revocation, and key authority
as applicable, enforces the provider call, and emits signed allow, deny, use,
and revoke evidence. The gateway SHALL fail closed when a required policy input
cannot be evaluated. Public witnesses SHALL NOT grant or refuse access and
SHALL NOT be accepted as proof that an event was truthful, authorized, retained,
deleted, clinically correct, or legally sufficient.

Network publication SHALL be asynchronous to an otherwise authorized operation.
A publication delay or outage SHALL produce `anchor_pending`, durable retry, and
escalation evidence; it SHALL NOT become an authorization result in either
direction. Direct provider credentials that permit bypass of the gateway are
non-conforming, while the deployable gateway, credentials, adapters, and domain
policy remain outside openxFactory ownership.

#### Scenario: policy authority cannot be evaluated

- **WHEN** the gateway cannot evaluate required policy, consent, identity, revocation, or key authority
- **THEN** it REFUSES the protected operation before provider access and does not ask a public witness to decide

#### Scenario: an authorized operation cannot reach a witness network

- **WHEN** the gateway authorizes and enforces an operation but Kaspa or OpenTimestamps publication is unavailable
- **THEN** the evidence receipt records `anchor_pending` with retry and escalation state without reversing or fabricating the authorization result

#### Scenario: provider access bypasses the gateway

- **WHEN** a caller uses direct provider credentials to perform a protected operation without the gateway
- **THEN** the owner runtime is non-conforming even if a later commitment is successfully anchored

#### Scenario: an anchor is offered as proof of consent

- **WHEN** a consumer treats a valid witness proof as proof that the event was authorized or consented
- **THEN** the verifier REFUSES that conclusion and reports only the existence, timing, and integrity claim the proof supports

### Requirement: Permissioned consent checkpoints expose a neutral state-root seam

The contract family SHALL define a domain-neutral seam from a governed
permissioned consent and policy plane into the evidence lifecycle. Consent rows,
granular access state, stable subject identifiers, salts, and policy meaning
SHALL remain off chain under the domain or product owner. The permissioned plane
SHALL emit a signed checkpoint envelope carrying an opaque state root,
checkpoint sequence, predecessor root, policy-contract version, and signer
reference. The signer and its chain SHALL resolve under the evidenced PKI plane
through released `trust-anchor` contracts.

The public witness path SHALL receive only a keyed commitment to the checkpoint
and state root. It SHALL NOT receive the consent state, a patient or other stable
identifier, a salt, or medical semantics. The provider-neutral gateway SHALL
evaluate the permissioned state directly; a confirmed public witness SHALL
corroborate checkpoint existence and continuity without becoming the consent
decision.

#### Scenario: a permissioned checkpoint enters the witness lifecycle

- **WHEN** a governed permissioned plane emits a signed checkpoint whose predecessor, sequence, signer chain, and opaque state root validate
- **THEN** the evidence kernel admits a keyed commitment to that checkpoint and state root without admitting the underlying consent state

#### Scenario: consent rows are offered to the public witness

- **WHEN** a checkpoint anchor request contains granular consent rows, stable subject identifiers, salts, or policy details
- **THEN** the reference validator REFUSES the public shape before publication

#### Scenario: a public checkpoint is offered as the authorization decision

- **WHEN** a gateway or consumer treats a confirmed checkpoint witness as a substitute for evaluating current permissioned consent state
- **THEN** it is REFUSED because the state-root witness corroborates continuity and does not decide authorization

#### Scenario: a medical interpretation is added to the neutral checkpoint

- **WHEN** a checkpoint schema or validator interprets treatment purpose, disclosure eligibility, or another medical meaning
- **THEN** it is REFUSED while the opaque state-root and continuity seam remains conforming

### Requirement: Public witnesses receive only opaque keyed commitments

For every accepted event, the owner SHALL derive an algorithm-tagged keyed
commitment using a unique high-entropy owner-held secret input. Keys, salts,
secret inputs, payloads, policy details, granular consent state, and domain
semantics SHALL remain off chain. A direct Kaspa L1 event payload SHALL contain
only a versioned domain separator and the opaque commitment. Public checkpoint
and batch witnesses SHALL contain only opaque roots and non-identifying
continuity material.

The public artifact schemas SHALL be closed against PHI, encrypted PHI,
financial detail, plaintext or ciphertext payload fields, plain record hashes,
reusable authorization tokens, and stable public subject, patient, payer,
provider, wallet, grant, resource, or owner-event identifiers. The canonical
reference validator SHALL refuse a payload-shaped record, an encrypted-payload
shape, a plain-hash commitment mode, a missing or reused secret-input claim, and
any stable public identifier field.

Consent-checkpoint and state-root anchors SHALL use the same keyed-commitment
boundary. A permissioned state root SHALL NOT be published as a plain hash or
alongside the state, salts, or stable identifiers it summarizes.

#### Scenario: plaintext PHI is offered for publication

- **WHEN** a public anchor request contains PHI or any plaintext domain payload
- **THEN** the reference validator REFUSES the request before network submission

#### Scenario: encrypted PHI is offered for publication

- **WHEN** a public anchor request contains ciphertext, an encrypted payload, or payload decryption metadata
- **THEN** the reference validator REFUSES it because encryption does not make permanent public payload publication conforming

#### Scenario: a plain record hash is offered

- **WHEN** an anchor request commits with an unkeyed plain hash of a record
- **THEN** the reference validator REFUSES it even when the hash algorithm is approved for other digest subjects

#### Scenario: a stable public identifier is included

- **WHEN** a public witness artifact carries a stable subject, patient, payer, provider, wallet, grant, resource, or owner-event identifier
- **THEN** the reference validator REFUSES the artifact rather than treating the identifier as harmless metadata

#### Scenario: a conforming opaque commitment is offered

- **WHEN** an event uses a unique high-entropy secret input and exposes only the versioned domain separator and opaque keyed commitment
- **THEN** the reference validator admits the public shape without claiming to validate the hidden event or policy

### Requirement: Confirmation profiles are approved before schemas and validators

Before any anchoring schema or validator is authored, the operator SHALL approve
versioned Kaspa and Bitcoin confirmation profiles. Each profile SHALL define the
objective evidence that distinguishes submitted from confirmed, required proof
capture, reorganization or replacement handling, an approval record, and
positive and refusal test vectors at the transition boundary. The profile SHALL
be referenced by identifier and version from every receipt evaluated under it.

This specification SHALL NOT invent unsupported numeric confirmation depths.
If the evidence needed to approve either profile is unresolved, schema and
validator authoring SHALL remain blocked. A profile revision SHALL create a new
version and SHALL NOT retroactively reinterpret a receipt evaluated under an
earlier version.

#### Scenario: schema authoring begins without approved profiles

- **WHEN** either network lacks a versioned operator-approved confirmation profile and transition vectors
- **THEN** schema and validator authoring is BLOCKED rather than allowing an implementer to choose a threshold

#### Scenario: a submitted proof is below the approved confirmation condition

- **WHEN** network submission evidence exists but the referenced profile's objective confirmation condition is not satisfied
- **THEN** the receipt remains submitted or pending and the validator REFUSES confirmed state

#### Scenario: the approved confirmation condition and proof requirements are satisfied

- **WHEN** all conditions and retained-proof requirements in the referenced approved profile verify
- **THEN** the validator admits confirmed state and records the profile identifier and version used

#### Scenario: an operator approves a new profile version

- **WHEN** confirmation policy changes after receipts already exist
- **THEN** new receipts reference the new version and prior receipts retain their original interpretation

### Requirement: Direct Kaspa L1 is the primary operational witness

Every event accepted into the owner evidence log SHALL enter a direct Kaspa L1
commitment path as the primary operational witness. `Primary` SHALL mean the
first operational witness and SHALL NOT mean sole long-horizon evidence. The v1
path SHALL NOT depend on Toccata, Kasplex, Igra, or public-chain contract
execution.

The event receipt SHALL begin in `anchor_pending`. It SHALL record Kaspa
submission separately from Kaspa confirmation: submitted means the serialized
transaction was accepted for processing by the declared Kaspa interface;
confirmed means the referenced versioned operator-approved Kaspa confirmation
profile has been satisfied and the independently verifiable retained proof
bundle is complete. A submitted transaction SHALL NOT be reported as confirmed.

#### Scenario: an accepted event awaits network publication

- **WHEN** an owner event is admitted to the signed log and no Kaspa submission has succeeded yet
- **THEN** its stable receipt records `anchor_pending` and the event remains queued for durable retry

#### Scenario: Kaspa accepts a transaction

- **WHEN** the direct L1 interface accepts the serialized commitment transaction
- **THEN** the receipt records Kaspa submitted evidence without recording Kaspa confirmation

#### Scenario: the confirmation policy is satisfied

- **WHEN** the declared Kaspa confirmation policy is satisfied and the complete retained proof bundle verifies
- **THEN** the receipt appends Kaspa confirmed state while preserving the earlier pending and submitted history

#### Scenario: a Toccata or EVM path is offered as the v1 witness

- **WHEN** a realization routes a production event through Toccata, Kasplex, Igra, or another contract runtime instead of direct Kaspa L1
- **THEN** the reference validator REFUSES the witness profile as outside this capability

### Requirement: Kaspa proof material survives ordinary-node pruning

The receipt SHALL retain enough Kaspa material for independent verification
after an ordinary node no longer serves the transaction. As the witness
progresses, the retained bundle SHALL capture the exact serialized transaction
and public payload, transaction identifier, accepting DAG reference,
transaction-to-DAG inclusion proof, relevant headers, node and protocol
versions, confirmation-policy identifier and result, and local signed receipt
material. Confirmation SHALL NOT be complete until the reference verifier can
verify the retained bundle without an explorer, hosted receipt service, or
ordinary historical-node lookup.

#### Scenario: an ordinary node has pruned the transaction

- **WHEN** a later verifier cannot retrieve the historical transaction from an ordinary Kaspa node
- **THEN** it verifies the witness from the retained transaction, DAG inclusion proof, headers, and versioned policy material

#### Scenario: only a transaction identifier is retained

- **WHEN** a purported confirmed receipt carries only a transaction id, explorer URL, or accepting-node assertion
- **THEN** the reference verifier REFUSES confirmed status because the retained material cannot independently prove inclusion after pruning

#### Scenario: proof capture is incomplete at confirmation time

- **WHEN** the confirmation policy is satisfied but any required retained proof component is unavailable
- **THEN** the receipt remains submitted or pending-proof and does not advance to Kaspa confirmed

### Requirement: Every fixed UTC day produces a complete durability batch

The durability profile SHALL divide time into consecutive, non-overlapping
24-hour UTC windows from `00:00:00Z` inclusive to the next `00:00:00Z`
exclusive. The trusted signed log's UTC acceptance timestamp and atomically
assigned monotonic leaf sequence SHALL be authoritative for batch admission.
Owner source time SHALL be descriptive only and SHALL NOT select or reopen a
window. At acceptance, the log SHALL assign the next sequence exactly once and
bind it permanently to the acceptance timestamp, leaf digest, and stable
owner-local dedupe key. The dedupe key SHALL remain off public chains.

Replay of a dedupe key with the same event digest SHALL resolve to the existing
leaf, sequence, and receipt without consuming another sequence. Reuse of the
same key with different content SHALL be REFUSED. Accepted leaf sequences SHALL
be strictly monotonic and SHALL NOT be reassigned or reused.

Every event accepted into the signed evidence log during a window SHALL appear
exactly once in that window's ordered Merkle batch, with no per-event
selectivity. The signed batch manifest SHALL bind the window boundaries, first
and last leaf sequence when present, event count, batch root, previous batch
root, close reason, dedupe rule, and late-arrival rule. Each event receipt SHALL
carry its Merkle path into the batch root.

A closed batch SHALL NOT be reopened or rewritten. An event whose source time
falls in an earlier window but whose trusted log acceptance occurs in the
current open window SHALL enter the current open window exactly once and SHALL
record prior-window lateness in off-chain evidence. Every window SHALL produce
a checkpoint: when no event was accepted, the system SHALL emit a signed
count-zero continuity checkpoint with the deterministic empty root and previous
batch root and SHALL submit that checkpoint through the same
OpenTimestamps/Bitcoin durability path.

#### Scenario: a day contains accepted events

- **WHEN** a fixed UTC window closes with one or more accepted events
- **THEN** its manifest accounts for every event exactly once and every event receipt carries a valid path to the one closed batch root

#### Scenario: a day contains no events

- **WHEN** a fixed UTC window closes with no accepted event
- **THEN** a signed empty continuity checkpoint with count zero, deterministic empty root, and previous batch root enters the durability path

#### Scenario: a source-time event arrives after its earlier window closes

- **WHEN** an event's source time belongs to a closed prior window but its trusted log acceptance timestamp belongs to the current open window
- **THEN** the prior manifest remains unchanged and the event enters the current open window exactly once with prior-window lateness recorded off chain

#### Scenario: an event is accepted exactly at UTC midnight

- **WHEN** the trusted log acceptance timestamp is exactly `00:00:00Z`
- **THEN** the event enters the new UTC window because the prior window's exclusive boundary has passed

#### Scenario: an identical dedupe key and digest are replayed

- **WHEN** the log receives an event with a dedupe key and digest already accepted
- **THEN** it returns the existing leaf sequence and receipt and creates no second batch admission

#### Scenario: a dedupe key is reused for different content

- **WHEN** the log receives an already accepted dedupe key with a different event digest
- **THEN** admission is REFUSED and no leaf sequence is assigned

#### Scenario: one event is selectively omitted

- **WHEN** reconciliation finds an accepted event in the window with no path into the closed batch
- **THEN** the batch is REFUSED as incomplete even if its root has a valid Bitcoin timestamp

### Requirement: OpenTimestamps submission and Bitcoin confirmation remain distinct

Every daily batch checkpoint, including an empty continuity checkpoint, SHALL be
submitted through OpenTimestamps for Bitcoin durability. The progressive receipt
SHALL record OpenTimestamps submitted state separately from Bitcoin confirmed
state. Submitted means a detached timestamp proof has been accepted and
retained; Bitcoin confirmed means that proof has been upgraded with the declared
Bitcoin transaction, inclusion, header, and confirmation evidence and verifies
under the referenced versioned operator-approved Bitcoin confirmation profile.
Long-horizon durability claims SHALL cite Bitcoin confirmed evidence and SHALL
NOT cite an unupgraded OpenTimestamps submission or Kaspa alone.

#### Scenario: a timestamp proof has been submitted but not upgraded

- **WHEN** a daily checkpoint has a retained OpenTimestamps submission proof but no confirmed Bitcoin inclusion evidence
- **THEN** the receipt reports OpenTimestamps submitted and Bitcoin pending, never Bitcoin confirmed

#### Scenario: the Bitcoin proof upgrades and verifies

- **WHEN** the detached proof is upgraded with independently verifiable Bitcoin inclusion and satisfies the declared confirmation policy
- **THEN** the receipt appends Bitcoin confirmed state without replacing its prior submission history

#### Scenario: an empty checkpoint reaches Bitcoin

- **WHEN** an empty-window continuity checkpoint completes the OpenTimestamps and Bitcoin path
- **THEN** the confirmed receipt proves continuity for that UTC window without inventing an event

#### Scenario: Kaspa alone is offered for a durability claim

- **WHEN** a consumer makes a long-horizon durability claim from a valid Kaspa proof with Bitcoin still pending
- **THEN** the verifier REFUSES the durability claim while preserving the valid operational-witness result

### Requirement: One progressive receipt preserves witness history

The owner event and receipt SHALL receive stable off-chain identities before
network submission. Pending, submitted, confirmed, failed, retried, and
superseded witness updates SHALL append to that same receipt and SHALL NOT create
competing event identities or erase prior states. The receipt envelope SHALL be
chain-agnostic, while each witness entry SHALL retain its chain-specific
transaction, inclusion, header or timestamp proof, adapter profile, verifier
profile, state, and evidence time.

The reference verifier SHALL report each path as valid, invalid, pending, or
unevaluable and SHALL report daily completeness separately. Pending or
unevaluable evidence SHALL NOT be converted into a pass, and an invalid path
SHALL NOT erase a separately valid path.

#### Scenario: a pending receipt later confirms on both paths

- **WHEN** one event progresses from `anchor_pending` through Kaspa submitted and confirmed and later through OpenTimestamps submitted and Bitcoin confirmed
- **THEN** all transitions remain in one append-only receipt under the original event identity

#### Scenario: one witness is valid and the other remains pending

- **WHEN** the Kaspa retained proof verifies and the Bitcoin durability path is still pending
- **THEN** the verifier reports a valid operational witness and pending durability without collapsing them into one result

#### Scenario: retained proof is unevaluable

- **WHEN** required proof bytes, versions, or policy identifiers cannot be evaluated
- **THEN** the verifier reports unevaluable and does not treat network references or prior status labels as a pass

### Requirement: Programmable Kaspa surfaces are outside the v1 production path

Toccata SHALL have no production role in v1 and MAY be used only for an isolated
non-production experiment carrying no PHI, production authority, provider
credential, or conforming-path dependency. Kasplex and Igra SHALL remain outside
v1. This capability SHALL state no future adoption or promotion trigger for any
of the three. Any future contract-code change SHALL decide on then-current
merits and evidence under its own governance, as ratified Q5 requires.

#### Scenario: Toccata is used for a non-production experiment

- **WHEN** an isolated experiment contains no sensitive payload, production authority, provider credential, or conforming-path dependency
- **THEN** this capability permits the experiment without recognizing it as production evidence

#### Scenario: Toccata is proposed for the v1 production path

- **WHEN** a v1 realization gives Toccata production authority or a dependency in the conforming witness path
- **THEN** the realization is REFUSED and direct Kaspa L1 remains the v1 production witness

#### Scenario: Kasplex or Igra is proposed for v1

- **WHEN** a v1 realization assigns Kasplex or Igra any production role
- **THEN** the realization is REFUSED because both surfaces are outside v1

#### Scenario: a future change considers contract code

- **WHEN** a later governed change considers Toccata, Kasplex, Igra, or another contract-code surface
- **THEN** this capability imposes no pre-written trigger and that change decides on then-current merits and evidence

### Requirement: openxFactory owns contracts and reference validators only

openxFactory SHALL own the neutral artifact schemas, examples, adapter ports,
state-transition and consistency rules, and canonical reference validators for
this capability. It SHALL NOT claim ownership of a deployable gateway or
anchoring service, provider or chain credentials, Kaspa or Bitcoin nodes,
OpenTimestamps calendars, schedulers, retries, proof-storage operations,
monitoring, service levels, incident response, event authorization, consent
policy, or medical policy. Runtime and domain owners SHALL supply those concerns
without changing the neutral contract semantics.

#### Scenario: a deployable service is included in the realization handoff

- **WHEN** the Speckit feature proposes a production gateway, network daemon, credential store, scheduler, or monitoring service in openxFactory
- **THEN** the work is REFUSED as outside this change while the neutral contract and reference-validator work remains in scope

#### Scenario: a medical rule is added to the neutral validator

- **WHEN** a schema or reference validator decides clinical purpose, treatment consent, disclosure eligibility, or another medical policy
- **THEN** it is REFUSED because the domain owner owns that policy and the neutral validator checks only contract conformance

#### Scenario: a domain supplies a conforming adapter

- **WHEN** a domain or runtime owner implements network and provider operations behind the neutral adapter ports
- **THEN** openxFactory validates the exchanged artifacts without assuming ownership of that runtime or its policy
