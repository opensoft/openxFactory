## ADDED Requirements

### Requirement: Realization waits for the released chain and an operational PKI plane

openxFactory SHALL NOT commission or realize the `chain-anchoring` capability
until the released signed-execution-chain contracts, canonical validator,
append-only signed transparency log, and required-check evidence are available,
AND until the signing plane consumed by anchoring is operational under released
`trust-anchor` contracts. Operational PKI evidence SHALL demonstrate governed
certificate issuance, verification, revocation handling, and declared chain
custody sufficient for every log, checkpoint, state, and receipt signature the
capability consumes.

A repository seed, contract pin, deployment topology, workflow file, or planned
service alone MUST NOT satisfy the operational PKI gate. The realization SHALL
consume released predecessor artifacts and SHALL NOT mint provisional leaf,
digest, signer-trust, or certificate-chain vocabularies.

#### Scenario: Released chain exists but operational PKI evidence does not

- **WHEN** signed-execution-chain is released but the only PKI evidence is a repository seed, contract pin, topology, workflow, or implementation plan
- **THEN** chain-anchoring realization remains blocked and no Speckit implementation is commissioned from this amendment

#### Scenario: Both realization gates are evidenced

- **WHEN** the released chain artifacts and required-check facts resolve and the operational PKI plane proves issuance, verification, revocation handling, and chain custody
- **THEN** one chain-anchoring realization may consume those exact artifacts without defining provisional substitutes

#### Scenario: A provisional predecessor shape is proposed

- **WHEN** a realization supplies its own leaf, digest, log, signer-trust, or certificate-chain shape because a released predecessor artifact is unavailable
- **THEN** the realization is REFUSED rather than creating a parallel signed-execution-chain or trust-anchor vocabulary

### Requirement: Fixed UTC durability batches account for every accepted event exactly once

The durability profile SHALL divide time into consecutive non-overlapping UTC
windows from `00:00:00Z` inclusive to the next `00:00:00Z` exclusive. The
trusted signed log's acceptance timestamp and atomically assigned monotonic leaf
sequence SHALL determine batch membership. Owner source time SHALL be descriptive
only and MUST NOT select or reopen a window.

At acceptance, the log SHALL bind the next sequence exactly once to the
acceptance timestamp, material digest, and stable owner-local dedupe key. Replay
of the same dedupe key with the same digest SHALL return the existing leaf,
sequence, and receipt without consuming another sequence. Reuse of that key with
different content SHALL be REFUSED. The dedupe key SHALL remain off public
chains.

Every event accepted during a window SHALL appear exactly once in that window's
ordered Merkle batch, with no per-event selectivity. The signed manifest SHALL
bind the window boundaries, first and last sequence when present, event count,
batch root, previous batch root, close reason, dedupe rule, and late-arrival
rule. Every event SHALL carry a Merkle path into the daily root. A closed window
MUST NOT be reopened or rewritten.

An event whose source time belongs to an earlier closed window but whose trusted
acceptance occurs in the current window SHALL enter the current window exactly
once and SHALL record its source-time lateness off chain. A window with no
accepted events SHALL still emit a signed, linked count-zero checkpoint using a
deterministic empty root, and that checkpoint SHALL enter the same durability
witness path.

#### Scenario: A non-empty UTC window closes

- **WHEN** a fixed UTC window closes with one or more accepted events
- **THEN** its signed manifest accounts for every accepted sequence exactly once and every event has a valid Merkle path into the one daily root

#### Scenario: An empty UTC window closes

- **WHEN** a fixed UTC window closes with no accepted event
- **THEN** a signed count-zero checkpoint with the deterministic empty root and previous batch root enters the durability witness path

#### Scenario: A source-time event arrives after its earlier day closed

- **WHEN** an event's source time belongs to a closed prior window but its trusted log acceptance belongs to the current open window
- **THEN** the prior manifest remains unchanged and the event enters the current window exactly once with source-time lateness recorded off chain

#### Scenario: Acceptance occurs exactly at UTC midnight

- **WHEN** the trusted log acceptance timestamp is exactly `00:00:00Z`
- **THEN** the event enters the new UTC window because the prior window's exclusive boundary has passed

#### Scenario: An identical dedupe key and digest are replayed

- **WHEN** the log receives a dedupe key and material digest it already accepted
- **THEN** it returns the existing leaf sequence and receipt and creates no second batch admission

#### Scenario: A dedupe key is reused for different content

- **WHEN** the log receives an accepted dedupe key with a different material digest
- **THEN** admission is REFUSED and no leaf sequence is assigned

#### Scenario: An accepted event is omitted from the daily root

- **WHEN** reconciliation finds an accepted sequence in the window with no path into the closed batch
- **THEN** the batch is REFUSED as incomplete even if its root has valid witness evidence

### Requirement: Witness submission and confirmation remain distinct evidence states

The anchor-state record SHALL distinguish interface submission from independently
verified confirmation for every configured witness. Kaspa submitted SHALL mean
that the serialized commitment transaction was accepted for processing by the
declared interface; it MUST NOT mean Kaspa confirmed. Kaspa confirmed SHALL
require the configured chain-acceptance rule to pass and all four per-chain
receipt elements to be captured whole.

OpenTimestamps submitted SHALL mean that the detached timestamp proof for the
daily root was accepted and retained; it MUST NOT mean Bitcoin confirmed.
Bitcoin confirmed SHALL require the detached proof to be upgraded with the
declared Bitcoin transaction, inclusion proof, header, and chain-acceptance
evidence, verified under the configured witness rules. A long-horizon durability
claim SHALL cite Bitcoin-confirmed evidence and MUST NOT cite an unupgraded
OpenTimestamps submission or Kaspa alone.

Submitted and in-flight state SHALL remain in the anchor-state record. The
chain-agnostic receipt SHALL gain a per-chain entry only when that entry's proof
material is captured whole, preserving the existing receipt/state split. A
later proof upgrade SHALL append the completed durability entry against the same
anchored digest and MUST NOT re-anchor the item or erase prior state transitions.

#### Scenario: Kaspa accepts a transaction for processing

- **WHEN** the declared Kaspa interface accepts the serialized commitment transaction but configured chain acceptance or proof capture is incomplete
- **THEN** the anchor-state record reports Kaspa submitted or pending and the receipt gains no confirmed Kaspa entry

#### Scenario: Kaspa confirmation evidence becomes complete

- **WHEN** the configured Kaspa acceptance rule passes and transaction bytes, DAG inclusion proof, block header, and chain-acceptance evidence are captured whole
- **THEN** the completed Kaspa entry is appended to the receipt without replacing its prior submitted state

#### Scenario: OpenTimestamps proof is submitted but not upgraded

- **WHEN** the daily checkpoint has a retained detached timestamp proof but no independently verified Bitcoin inclusion evidence
- **THEN** the anchor-state record reports OpenTimestamps submitted and Bitcoin pending and no long-horizon durability claim is admitted

#### Scenario: Bitcoin upgrade verifies

- **WHEN** the detached proof is upgraded with complete Bitcoin transaction, inclusion, header, and chain-acceptance evidence that satisfies the configured rules
- **THEN** the completed durability entry is appended to the same receipt and Bitcoin confirmed becomes available without re-anchoring the item

#### Scenario: Pending evidence is offered as confirmed

- **WHEN** a consumer presents interface acceptance, a detached timestamp proof, a transaction identifier, or a prior status label as confirmed witness evidence
- **THEN** verification REFUSES confirmation and reports the actual submitted, pending, invalid, or unevaluable state

#### Scenario: Kaspa alone is offered for a long-horizon claim

- **WHEN** a consumer makes a long-horizon durability claim from valid Kaspa evidence while Bitcoin remains pending or unevaluable
- **THEN** the claim is REFUSED while the valid operational witness result remains independently reportable
