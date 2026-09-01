## ADDED Requirements

### Requirement: Realization waits for the released chain and an operational PKI plane

openxFactory SHALL NOT commission or realize the `chain-anchoring` capability
until the released signed-execution-chain contracts, canonical validator,
append-only signed transparency log, AND live evidence that
`signed-execution-chain-gate` is REQUIRED in the branch ruleset and that its
broken-chain canary fails are available,
AND until the signing plane consumed by anchoring is operational under released
`trust-anchor` contracts. Operational PKI evidence SHALL demonstrate governed
certificate issuance, verification, revocation handling, and declared chain
custody sufficient for every log, checkpoint, state, and receipt signature the
capability consumes.

A repository seed, contract pin, deployment topology, workflow file, or planned
service alone MUST NOT satisfy the operational PKI gate. A workflow file, a
green advisory run, or a declaration carrying `is_required_in_ruleset: false`
MUST NOT satisfy the signed-chain permission gate. The realization SHALL consume
released predecessor artifacts and SHALL NOT mint provisional leaf, digest,
signer-trust, or certificate-chain vocabularies.

Because `add-chain-anchoring` is ratified but unrealized, this amendment and its
basis SHALL link to ONE shared Speckit feature and ONE new-family additive
release. `add-chain-anchoring` SHALL archive first so its nine requirements
create the canonical capability; this amendment SHALL archive second and add its
three requirements; the release SHALL be cut only after both promotions are
present. If the basis releases before this amendment is ratified and included in
that realization, implementation SHALL stop and re-evaluate compatibility and
version class rather than assuming an additive first-release path.

#### Scenario: Released chain exists but operational PKI evidence does not

- **WHEN** signed-execution-chain is released but the only PKI evidence is a repository seed, contract pin, topology, workflow, or implementation plan
- **THEN** chain-anchoring realization remains blocked and no Speckit implementation is commissioned from this amendment

#### Scenario: Both realization gates are evidenced

- **WHEN** the released chain artifacts resolve, the live ruleset requires `signed-execution-chain-gate`, its broken-chain canary fails as designed, and the operational PKI plane proves issuance, verification, revocation handling, and chain custody
- **THEN** one chain-anchoring realization may consume those exact artifacts without defining provisional substitutes

#### Scenario: A provisional predecessor shape is proposed

- **WHEN** a realization supplies its own leaf, digest, log, signer-trust, or certificate-chain shape because a released predecessor artifact is unavailable
- **THEN** the realization is REFUSED rather than creating a parallel signed-execution-chain or trust-anchor vocabulary

#### Scenario: A workflow exists but the reader is not required

- **WHEN** the signed-chain workflow is green but the live ruleset does not require `signed-execution-chain-gate` or its broken-chain canary has not failed
- **THEN** chain-anchoring realization remains blocked because advisory execution confers no permission

#### Scenario: The amendment attempts to archive before its basis

- **WHEN** this amendment is prepared for archive while `add-chain-anchoring` has not promoted the canonical `chain-anchoring` capability
- **THEN** archive is BLOCKED until the shared feature lands and the basis archives first

### Requirement: Fixed UTC durability batches account for every accepted event exactly once

The durability profile SHALL divide time into consecutive non-overlapping UTC
windows from `00:00:00Z` inclusive to the next `00:00:00Z` exclusive. One
atomic log-admission transaction SHALL validate a declared durability-eligible
owner-evidence event, apply the dedupe rule, record trusted acceptance time,
select the window from that acceptance time, and assign the next monotonic leaf
sequence. Acceptance time SHALL select the window and sequence SHALL order
events within that window. Owner source time SHALL be descriptive only and MUST
NOT select or reopen a window.

The close operation SHALL serialize after every admission assigned before the
window's exclusive boundary and before the first admission assigned to the next
window. A sequence MUST NOT cross or invert that acceptance-time partition. At
acceptance, the log SHALL bind the next sequence exactly once to the acceptance
timestamp, material digest, and stable owner-local dedupe key. Replay of the
same dedupe key with the same digest SHALL return the existing leaf and sequence
without consuming another sequence. Reuse of that key with different content
SHALL be REFUSED before sequence assignment. The dedupe key SHALL remain off
public chains.

A versioned eligibility registry SHALL enumerate the neutral owner-evidence
event kinds counted by this profile. A domain overlay MAY map its event kinds
into that registry but MUST NOT select among events after an eligible event is
accepted. Anchor-state transitions, witness submissions, confirmations, batch
manifests, and continuity checkpoints SHALL be control leaves outside the event
count and MUST NOT enter the same batch they produce; they remain covered by the
signed log and its log-checkpoint anchors. This exclusion prevents recursive
self-inclusion and permits genuine consecutive empty windows.

Every durability-eligible event accepted during a window SHALL appear exactly
once in that window's ordered Merkle batch, with no per-event selectivity. The
signed manifest SHALL bind the eligibility-registry version, window boundaries,
first and last sequence when present, event count, batch root, previous batch
root, close reason, dedupe rule, and late-arrival rule. Every included event
SHALL carry a Merkle path into the daily root. A closed window MUST NOT be
reopened or rewritten.

The CLOSED DAILY MANIFEST AND ROOT SHALL be the anchored item for this profile;
its constituent events SHALL be membership leaves and SHALL NOT receive
separate multi-anchor receipts. After closure, the same daily root SHALL enter
BOTH configured witnesses: direct Kaspa first and Bitcoin-via-OpenTimestamps as
the durability witness. The receipt's shared top-level aggregation path SHALL be
the identity path for that daily root. Each per-chain entry's chain-acceptance
evidence SHALL carry the witness-specific commitment path from the SAME daily
root to the commitment encoded in its transaction bytes: direct payload binding
for Kaspa and the detached OpenTimestamps operations path for Bitcoin. Different
proof paths are mandatory where the witness encoding differs; a different source
root, cadence, or receipt shape SHALL be REFUSED. The open window remains
evidenced by the signed owner-local log and MUST NOT be presented as already
publicly anchored.

An event whose source time belongs to an earlier closed window but whose trusted
acceptance occurs in the current window SHALL enter the current window exactly
once and SHALL record its source-time lateness off chain. A window with no
eligible accepted events SHALL still emit a signed, linked count-zero checkpoint
using a deterministic empty root, and that daily item SHALL enter both configured
witnesses through the same receipt path.

#### Scenario: A non-empty UTC window closes

- **WHEN** a fixed UTC window closes with one or more accepted events
- **THEN** its signed manifest accounts for every eligible accepted sequence exactly once, every event has a valid Merkle path into the one daily root, and that root becomes the one anchored item sent to both witnesses

#### Scenario: An empty UTC window closes

- **WHEN** a fixed UTC window closes with no eligible accepted events
- **THEN** a signed count-zero checkpoint with the deterministic empty root and previous batch root enters both configured witness paths as the daily anchored item

#### Scenario: A source-time event arrives after its earlier day closed

- **WHEN** an event's source time belongs to a closed prior window but its trusted log acceptance belongs to the current open window
- **THEN** the prior manifest remains unchanged and the event enters the current window exactly once with source-time lateness recorded off chain

#### Scenario: Acceptance occurs exactly at UTC midnight

- **WHEN** the trusted log acceptance timestamp is exactly `00:00:00Z`
- **THEN** the event enters the new UTC window because the prior window's exclusive boundary has passed

#### Scenario: Admission races the midnight close

- **WHEN** event admission and window closure execute concurrently at the exclusive UTC boundary
- **THEN** the atomic admission/close order places the event in exactly one window, and its sequence cannot appear on both sides or invert the acceptance-time partition

#### Scenario: An identical dedupe key and digest are replayed

- **WHEN** the log receives a dedupe key and material digest it already accepted
- **THEN** it returns the existing leaf sequence and receipt and creates no second batch admission

#### Scenario: A dedupe key is reused for different content

- **WHEN** the log receives an accepted dedupe key with a different material digest
- **THEN** admission is REFUSED and no leaf sequence is assigned

#### Scenario: An accepted event is omitted from the daily root

- **WHEN** reconciliation finds an accepted sequence in the window with no path into the closed batch
- **THEN** the batch is REFUSED as incomplete even if its root has valid witness evidence

#### Scenario: An anchoring control leaf is offered as a source event in its own batch

- **WHEN** a witness submission, confirmation, batch manifest, continuity checkpoint, or other anchoring-control leaf is offered as a durability-eligible event in the batch it produces
- **THEN** admission to that batch is REFUSED as recursive while the control leaf remains retained in the signed log/checkpoint path

#### Scenario: Different roots are proposed for the two configured witnesses

- **WHEN** a realization proposes a rapid Kaspa root and a separate daily OpenTimestamps root for the same daily item
- **THEN** the profile REFUSES the split and requires the same closed daily root and existing multi-anchor receipt for both witnesses

#### Scenario: A witness-specific commitment path is omitted

- **WHEN** a per-chain entry carries transaction and chain inclusion evidence but no proof that its transaction commitment derives from the same daily root named by the receipt
- **THEN** that witness entry is REFUSED even when the transaction itself is canonically accepted

### Requirement: Witness submission and confirmation remain distinct evidence states

Before any anchoring schema or validator is authored, the operator SHALL approve
versioned Kaspa and Bitcoin confirmation profiles. Each profile SHALL define the
objective evidence that distinguishes submitted from confirmed, the complete
proof material retained at confirmation, reorganization or transaction-
replacement handling, an approval record, and positive and refusal vectors at
every transition boundary. This specification MUST NOT invent an unsupported
numeric confirmation depth. If either profile is unresolved, schema and
validator authoring SHALL remain blocked rather than leaving finality to an
implementer.

Every configured witness SHALL reference its approved confirmation-profile
identifier and version in the mint-time configuration block committed by the
anchored digest, and every confirmed receipt entry and verification result SHALL
name the profile version under which it was evaluated. A profile revision SHALL
create a new immutable version for newly minted receipts and MUST NOT
retroactively reinterpret, upgrade, or downgrade a receipt minted under an
earlier profile.

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
- **THEN** the per-witness state deterministically reports Kaspa submitted while the overall item remains `anchor_pending`, and the receipt gains no confirmed Kaspa entry

#### Scenario: Kaspa confirmation evidence becomes complete

- **WHEN** the configured Kaspa acceptance rule passes and transaction bytes, DAG inclusion proof, block header, and chain-acceptance evidence are captured whole
- **THEN** the completed Kaspa entry is appended to the receipt without replacing its prior submitted state

#### Scenario: Schema authoring starts without approved confirmation profiles

- **WHEN** either configured network lacks a versioned operator-approved profile, approval record, transition vectors, or objective confirmation evidence
- **THEN** chain-anchoring schema and validator authoring is BLOCKED and no implementation-selected threshold is accepted

#### Scenario: A submitted proof is below its approved confirmation condition

- **WHEN** network submission evidence exists but the referenced profile's objective confirmation condition or retained-proof requirement is not satisfied
- **THEN** the witness remains submitted or pending and the validator REFUSES confirmed state

#### Scenario: A profile handles a reorganization or replacement

- **WHEN** a previously observed transaction or block is reorganized, replaced, or no longer satisfies the referenced profile
- **THEN** the profile's declared transition rule determines the witness state, the change is written as evidence, and a stale confirmed label is not retained by assertion

#### Scenario: An operator approves a new profile version

- **WHEN** confirmation policy changes after receipts already exist
- **THEN** newly minted receipts reference the new version and prior receipts retain the interpretation and verification result of their committed profile version

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
