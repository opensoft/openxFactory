# chain-anchoring Specification (delta)

## ADDED Requirements

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
window. The SAME atomic close transaction SHALL record a
`close_sequence_watermark` equal to the greatest signed-log sequence covered by
that serialization point AND the immutable reference to a signed resolving log
checkpoint whose tree size/root covers every log leaf through that watermark. A
sequence MUST NOT cross or invert that acceptance-time partition. At
acceptance, the log SHALL bind the next sequence exactly once to the acceptance
timestamp, material digest, and stable owner-local dedupe key. Replay of the
same dedupe key with the same digest SHALL return the existing leaf and sequence
without consuming another sequence. Reuse of that key with different content
SHALL be REFUSED before sequence assignment. The dedupe key SHALL remain off
public chains.

A signed append-only eligibility registry SHALL enumerate the neutral owner-
evidence event kinds counted by this profile. Each immutable registry entry SHALL
bind its version, canonical content digest, approval record, predecessor when
present, activation log sequence and checkpoint, half-open effective UTC-window
interval, and standing `active`, `retired`, or `compromised`. Activating a
successor SHALL atomically close its predecessor's effective interval and mark
the predecessor retired; two entries MUST NOT be active for the same boundary.
At each UTC window open, the runtime SHALL select the unique entry with
`standing == active` whose effective interval contains that boundary and whose activation
checkpoint is greatest; zero or multiple matches SHALL be REFUSED. The runtime
SHALL snapshot exactly that entry;
every admission assigned to that window SHALL use that same version, content
digest, activation checkpoint, and standing. A registry activation during an
open window SHALL apply only to the next window and MUST NOT change eligibility
for the current window. A domain overlay MAY map its event kinds into the
snapshotted registry but MUST NOT select among events after an eligible event is
accepted. Anchor-state transitions, witness submissions, confirmations, batch
manifests, and continuity checkpoints SHALL be control leaves outside the event
count and MUST NOT enter the same batch they produce; they remain covered by the
signed log and its log-checkpoint anchors. This exclusion prevents recursive
self-inclusion and permits genuine consecutive empty windows.

Every durability-eligible event accepted during a window SHALL appear exactly
once in that window's ordered Merkle batch, with no per-event selectivity. Every
included event SHALL carry a membership path into `daily_batch_root`. A closed
window MUST NOT be reopened or rewritten.

Before schema or validator authoring, the operator SHALL approve one immutable
`daily-merkle` construction profile. The profile SHALL fix canonical event-leaf
encoding, SHA-256 as the hash algorithm, distinct leaf and internal-node domain-
separation byte strings, sequence ordering, tree shape, odd-node handling, and
the deterministic empty root. The released profile SHALL carry an identifier,
version, canonical content digest, and approval record. Each UTC window SHALL
snapshot that profile at open, and every admission and the canonical manifest
SHALL bind the same identifier, version, and content digest. An unresolved,
unknown, mutable, or digest-mismatched construction profile SHALL block schema
authoring or REFUSE admission/closure. The canonical validator SHALL resolve the
pinned released profile and mechanically recompute every leaf, membership path,
and `daily_batch_root`.

The proof chain SHALL contain distinct, mechanically recomputable nodes in this
order:

1. accepted event leaves and membership paths produce `daily_batch_root`;
2. canonical signed daily-manifest bytes bind the snapshotted eligibility-
   registry version, canonical content digest, activation checkpoint and
   standing, window boundaries, first and last sequence when present, event
   count, `daily_batch_root`, daily-Merkle profile id/version/content digest,
   `previous_daily_anchored_digest`, `close_sequence_watermark`, resolving signed-
   log checkpoint identity/tree size/root/signature, close reason, dedupe rule,
   and late-arrival rule;
3. the ratified digest construction produces `material_digest` from those exact
   canonical manifest bytes;
4. the ratified construction produces `anchored_digest` from `material_digest`
   plus the COMPLETE mint-time configuration block, including configured
   witnesses, horizons, timing inputs, confirmation-profile ids, versions,
   content digests, activation checkpoints, and standing evidence;
5. the shared aggregation path begins at `anchored_digest` and produces
   `aggregation_root`; for this one-item daily profile that path SHALL be the
   identity path, so `aggregation_root == anchored_digest`;
6. each per-chain entry carries a witness-specific commitment path from that SAME
   `aggregation_root` to the commitment encoded in its transaction bytes, then
   the ratified transaction, inclusion, header, and chain-acceptance proofs.

The CLOSED DAILY MANIFEST represented by the configuration-bound
`anchored_digest` SHALL be the anchored item for this profile; constituent
events SHALL be membership leaves and SHALL NOT receive separate multi-anchor
receipts. After closure, the same `aggregation_root` SHALL enter BOTH configured
witnesses: direct Kaspa first and Bitcoin-via-OpenTimestamps as the durability
witness. Different witness commitment paths are mandatory where encoding differs;
a raw `daily_batch_root`, different source root, omitted manifest/digest link,
uncommitted configuration, different cadence, or bespoke receipt shape SHALL be
REFUSED. The open window remains evidenced by the signed owner-local log and
MUST NOT be presented as already publicly anchored.

Every daily manifest after the first SHALL bind the immediately preceding
daily item's `anchored_digest`, not its `daily_batch_root`. The first manifest
SHALL bind one contract-defined genesis sentinel. This continuity link commits
to the previous window identity, accounting fields, registry snapshots, and
configuration even when consecutive empty windows share the same deterministic
empty `daily_batch_root`. A missing, duplicated, reordered, or substituted daily
item SHALL therefore break the next manifest's continuity proof.

The canonical validator SHALL verify the resolving signed-log checkpoint, walk
all log records through `close_sequence_watermark`, apply the window's bound
eligibility snapshot and trusted acceptance-time partition, and reproduce the
complete ordered admission set. `first sequence`, `last sequence`, and `event
count` are summaries of that checkpoint-derived set, not a caller-selected
denominator. Any omitted eligible prefix, middle record, or suffix SHALL be
REFUSED even when the supplied summaries and Merkle root are self-consistent.

An event whose source time belongs to an earlier closed window but whose trusted
acceptance occurs in the current window SHALL enter the current window exactly
once and SHALL record its source-time lateness off chain. A window with no
eligible accepted events SHALL still emit a signed, linked count-zero checkpoint
using a deterministic empty root, and that daily item SHALL enter both configured
witnesses through the same receipt path.

#### Scenario: A non-empty UTC window closes

- **WHEN** a fixed UTC window closes with one or more accepted events
- **THEN** its signed manifest accounts for every eligible accepted sequence exactly once, every event has a valid path into `daily_batch_root`, and the recomputed configuration-bound `anchored_digest` becomes the one item whose aggregation root enters both witnesses

#### Scenario: An empty UTC window closes

- **WHEN** a fixed UTC window closes with no eligible accepted events
- **THEN** a signed count-zero manifest binds the deterministic empty `daily_batch_root` and immediately preceding `previous_daily_anchored_digest`, and its configuration-bound `anchored_digest` enters both configured witness paths as the daily anchored item

#### Scenario: A source-time event arrives after its earlier day closed

- **WHEN** an event's source time belongs to a closed prior window but its trusted log acceptance belongs to the current open window
- **THEN** the prior manifest remains unchanged and the event enters the current window exactly once with source-time lateness recorded off chain

#### Scenario: Acceptance occurs exactly at UTC midnight

- **WHEN** the trusted log acceptance timestamp is exactly `00:00:00Z`
- **THEN** the event enters the new UTC window because the prior window's exclusive boundary has passed

#### Scenario: Admission races the midnight close

- **WHEN** event admission and window closure execute concurrently at the exclusive UTC boundary
- **THEN** the atomic admission/close order places the event in exactly one window, and its sequence cannot appear on both sides or invert the acceptance-time partition

#### Scenario: A minter omits the final eligible admissions

- **WHEN** a manifest lowers its last sequence and event count to match a retained prefix while the bound signed-log checkpoint covers later eligible admissions before `close_sequence_watermark`
- **THEN** canonical checkpoint reconciliation detects the omitted suffix and REFUSES the batch before witness verification

#### Scenario: An identical dedupe key and digest are replayed

- **WHEN** the log receives a dedupe key and material digest it already accepted
- **THEN** it returns the existing admission acknowledgement carrying leaf sequence and material digest, returns no pre-closure anchor receipt, and creates no second batch admission

#### Scenario: A dedupe key is reused for different content

- **WHEN** the log receives an accepted dedupe key with a different material digest
- **THEN** admission is REFUSED and no leaf sequence is assigned

#### Scenario: An accepted event is omitted from the daily root

- **WHEN** reconciliation finds an accepted sequence in the window with no path into the closed batch
- **THEN** the batch is REFUSED as incomplete even if its root has valid witness evidence

#### Scenario: Eligibility changes during an open window

- **WHEN** a new eligibility-registry entry activates after the current UTC window opened
- **THEN** the current window continues using its bound version, content digest, activation checkpoint, and standing, and the new entry applies only when the next window opens

#### Scenario: Two eligibility entries claim the same boundary

- **WHEN** zero entries or more than one entry with `standing == active` has an effective interval containing the UTC window boundary
- **THEN** window opening is REFUSED and no event is admitted under an ambiguous denominator

#### Scenario: An older eligibility version is offered after successor activation

- **WHEN** a successor's activation checkpoint and effective interval cover the UTC window boundary but the runtime offers its retired predecessor
- **THEN** window opening is REFUSED as eligibility rollback

#### Scenario: Eligibility content is substituted under the same version

- **WHEN** an admission or manifest supplies registry contents whose digest differs from the snapshotted append-only registry entry
- **THEN** admission or closure is REFUSED before the batch root can be accepted

#### Scenario: Merkle construction profile is missing or substituted

- **WHEN** an admission or manifest omits the daily-Merkle profile id, version, or content digest, or the resolved profile bytes do not match that digest
- **THEN** admission or closure is REFUSED before any membership or completeness claim is accepted

#### Scenario: Independent validator recomputes a non-empty root

- **WHEN** a validator receives accepted event bytes, sequences, membership paths, and a manifest naming the released daily-Merkle profile
- **THEN** canonical leaf encoding, domain separation, ordering, tree shape, odd-node handling, and SHA-256 deterministically reproduce the manifest's `daily_batch_root` or verification is REFUSED

#### Scenario: An intermediate empty day is omitted

- **WHEN** two or more consecutive empty windows share the deterministic empty `daily_batch_root` but an intermediate daily manifest is omitted
- **THEN** the later manifest's `previous_daily_anchored_digest` does not resolve to the immediately preceding item and continuity verification is REFUSED

#### Scenario: An anchoring control leaf is offered as a source event in its own batch

- **WHEN** a witness submission, confirmation, batch manifest, continuity checkpoint, or other anchoring-control leaf is offered as a durability-eligible event in the batch it produces
- **THEN** admission to that batch is REFUSED as recursive while the control leaf remains retained in the signed log/checkpoint path

#### Scenario: Different roots are proposed for the two configured witnesses

- **WHEN** a realization proposes a rapid Kaspa aggregation root and a different OpenTimestamps aggregation root for the same configuration-bound daily item
- **THEN** the profile REFUSES the split and requires both witness commitment paths to begin at the same `aggregation_root == anchored_digest`

#### Scenario: A witness-specific commitment path is omitted

- **WHEN** a per-chain entry carries transaction and chain inclusion evidence but no proof that its transaction commitment derives from the same configuration-bound `aggregation_root` named by the receipt
- **THEN** that witness entry is REFUSED even when the transaction itself is canonically accepted

#### Scenario: Batch root or mint-time configuration is substituted

- **WHEN** event membership proves one `daily_batch_root` but the manifest, previous daily anchored digest, close watermark, resolving log checkpoint, Merkle profile, material digest, witness set, horizon, timing input, confirmation-profile version, profile digest, activation checkpoint, or standing evidence differs from the values committed by `anchored_digest`
- **THEN** receipt verification REFUSES the item before evaluating either witness proof

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

The operator SHALL publish those approvals in an append-only signed confirmation-
profile registry. Every registry entry SHALL bind the network, profile id,
immutable version, canonical content digest, approval record, predecessor when
present, activation log sequence and checkpoint, effective interval, and closed
standing `active`, `retired`, or `compromised`. Registry history MUST NOT be
rewritten. At each UTC window open, the active registry checkpoint SHALL
deterministically select one profile version per witness for the entire daily
item. Every admission assigned to that window SHALL inherit the same profile ids,
versions, content digests, activation checkpoints, and standing. A profile
activation during an open window SHALL apply only to the next window. Selection
of an older, future, unknown, retired, compromised, digest-mismatched, or not-yet-
active version at the window-open checkpoint SHALL be REFUSED.

Every configured witness SHALL reference its window-snapshotted confirmation-
profile id, version, content digest, activation checkpoint, and standing evidence
in the mint-time configuration block committed by `anchored_digest`, and every
confirmed receipt entry and verification result SHALL name the profile under
which it was evaluated. A profile revision SHALL append a new immutable version
and activation record effective for a later UTC-window boundary. Prior receipts
retain immutable as-of evidence such as
`confirmed_under_<version>_at_<checkpoint>`; current verification SHALL also
report current registry standing. A retired or compromised profile MUST NOT mint
new receipts or support a new long-horizon claim, and current standing MUST NOT
rewrite the historical receipt.

The anchor-state record SHALL distinguish interface submission from independently
verified confirmation for every configured witness. Kaspa submitted SHALL mean
that the serialized commitment transaction was accepted for processing by the
declared interface; it MUST NOT mean Kaspa confirmed. Kaspa confirmed SHALL
require the configured chain-acceptance rule to pass and all four per-chain
receipt elements to be captured whole.

OpenTimestamps submitted SHALL mean that the detached timestamp proof committing
to the SAME configuration-bound `aggregation_root == anchored_digest` named by
the receipt was accepted and retained; a proof over raw `daily_batch_root` SHALL
be REFUSED and submission MUST NOT mean Bitcoin confirmed.
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
- **THEN** the witness deterministically remains `submitted`; `pending` is reserved for a witness with no accepted submission evidence, and the validator REFUSES confirmed state

#### Scenario: A profile handles a reorganization or replacement

- **WHEN** a previously observed transaction or block is reorganized, replaced, or no longer satisfies the referenced profile
- **THEN** the profile's declared transition rule determines the witness state, the change is written as evidence, and a stale confirmed label is not retained by assertion

#### Scenario: An operator approves a new profile version

- **WHEN** confirmation policy changes after receipts already exist
- **THEN** the registry appends the new content digest and a future UTC-window activation checkpoint, the current open window retains its snapshot, later windows use the new version, and prior receipts retain their immutable as-of result while current verification reports current standing

#### Scenario: A minter rolls back after a newer profile activates

- **WHEN** a UTC window opens after a new profile activation checkpoint but its snapshot selects an older profile version
- **THEN** minting is REFUSED before witness submission even if the older version was once approved

#### Scenario: A profile activates during an open window

- **WHEN** a new confirmation-profile version activates after a UTC window has opened and before its daily item closes
- **THEN** every event and the final item retain the window-open profile snapshot, and the new version applies only to the next window

#### Scenario: Profile content is substituted under an approved id and version

- **WHEN** the supplied profile content digest differs from the append-only registry entry committed by the anchored digest
- **THEN** verification REFUSES the receipt and does not evaluate the substituted confirmation rule

#### Scenario: A profile is retired or compromised after historical confirmation

- **WHEN** a historical receipt proved confirmation under its then-active profile but current registry standing is `retired` or `compromised`
- **THEN** the historical as-of evidence remains immutable, current verification reports `profile_retired` or `profile_compromised`, and no new long-horizon claim is admitted from that profile

#### Scenario: OpenTimestamps proof is submitted but not upgraded

- **WHEN** the daily item has a retained detached timestamp proof from its configuration-bound `aggregation_root == anchored_digest` but no independently verified Bitcoin inclusion evidence
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
