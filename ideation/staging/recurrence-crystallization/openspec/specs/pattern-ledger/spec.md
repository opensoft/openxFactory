# pattern-ledger Delta: Sensing Contracts for Recurrence Crystallization

Status: draft
Draft slice of: ../../../recurrence-crystallization.md

## ADDED Requirements

### Requirement: Episode Capture Is Universal And Derived
Every governed job run SHALL be representable as exactly one `episode`
record — derived from the runtime's existing audit, run-event, metering, and
label streams rather than written to a second authoritative store — carrying
an envelope snapshot, the plan record as data, a step/tool trace (digests
always; payload retention per the tenant dial), a cost vector including
human touches, a replayability class (`pure | record-replay | live-only`)
declared at capture, and a consent scope. Multi-agent activity appears as
sub-spans of the one job-level episode.

#### Scenario: A multi-agent job completes

- **WHEN** a governed job completes on the expensive path with several
  agents contributing
- **THEN** exactly one episode record MUST be derivable for the job, keyed
  by its fingerprint
- **AND** each agent's activity MUST appear as a sub-span of that episode,
  never as a sibling episode

#### Scenario: Payload retention expires

- **WHEN** a tenant's `payload_retention` window elapses for an episode's
  tool I/O
- **THEN** retained payloads MAY be dropped
- **AND** digests, cost vector, labels, and lineage MUST remain

### Requirement: Outcome Labels Are Append-Only Events
Episode outcome SHALL be an append-only stream of `outcome_label` events
with source vocabulary `praise | gate_outcome | correction | adjudication`,
each carrying actor reference, grade, and evidence reference; episode
quality SHALL be computed as a fold over the stream and never stored as a
single immutable verdict.

#### Scenario: A praised episode is later corrected

- **WHEN** an episode labeled with `praise` at close later receives a
  `correction` event (the artifact was reverted or reopened)
- **THEN** the episode's computed quality MUST reflect the correction
- **AND** the original praise event MUST remain in the stream unaltered

### Requirement: Recurrence Families Are Governed Register Entries
The system SHALL maintain recurrence families as tenant-scoped register
entries with lifecycle vocabulary `seed | forming | established |
crystallizing | served | dormant`, mined in two lanes (whole-job and
fragment), whose merges and splits are recorded transitions carrying
provenance, and whose matcher is a versioned artifact with a visible
dispatch-time precision metric.

#### Scenario: Two families merge

- **WHEN** accumulated evidence shows two family entries describe one
  pattern
- **THEN** the merge MUST be a recorded register transition preserving both
  histories and re-keying forecasts and future corpora to the merged
  identity
- **AND** a silent re-clustering that discards either history is
  nonconformant

#### Scenario: A fragment family is mined

- **WHEN** the same step subsequence recurs inside episodes of different
  whole-job families
- **THEN** the fragment lane MAY register it as its own family with
  provenance to the containing episodes

#### Scenario: Families never mix tenants

- **WHEN** structurally identical work arrives from two tenants
- **THEN** each tenant's instances MUST land in that tenant's family entry

### Requirement: Forecasts Are Scored Predictive Records
A recurrence forecast SHALL be a stored record carrying a predictive
distribution over a declared horizon, its evidence window, its cost-regime
assumption, and a stability half-life estimate; it SHALL be emitted only at
or above the minimum-evidence dial, SHALL report fence-eligible volume
alongside raw family volume wherever a fence exists, and SHALL be scored
against actuals when its maturity date passes.

#### Scenario: Insufficient evidence

- **WHEN** a family has fewer instances than `min_family_forecast`
- **THEN** no forecast record is emitted
- **AND** the family remains `forming`

#### Scenario: A forecast matures

- **WHEN** a forecast's horizon elapses
- **THEN** a score record MUST be produced comparing predicted and realized
  counts under the declared cost-regime assumption

### Requirement: The Ledger Is A Single Derived Substrate
The pattern ledger SHALL be computed as a governed derived projection —
declared recipe, source stream digests, deterministic regeneration — and
every consumer (family mining, forecasting, corpus curation, accounting)
SHALL reference episodes by digest rather than holding private copies.

#### Scenario: A label correction propagates

- **WHEN** an episode receives a late `correction` label
- **THEN** every consumer keying that episode by digest MUST observe the
  re-graded quality without any second store being updated

#### Scenario: Deterministic regeneration

- **WHEN** the projection is regenerated from the same source streams and
  recipe version
- **THEN** the resulting ledger records MUST be identical

### Requirement: Candidates Nominate And Never Spend
A `crystallization_candidate` record SHALL be the ledger's only mutating
output, carried in the suggestion grammar — idempotency key of family plus
evidence window, suppression while one is open, and a rationale citing
episodes and the forecast — and its creation SHALL NOT schedule work,
consume budget, or execute any capability; nomination thresholds SHALL be
declared dials owned by policy layers.

#### Scenario: A candidate cannot trigger spend

- **WHEN** a family crosses the nomination threshold and a candidate record
  is created
- **THEN** no job is scheduled, no budget is consumed, and no capability is
  executed until a separate decision record (successor change) funds it

#### Scenario: Duplicate nomination is suppressed

- **WHEN** the sweep re-evaluates a family that already has an open
  candidate for the same evidence window
- **THEN** regeneration MUST be a no-op on the open candidate

#### Scenario: Praise alone is insufficient evidence

- **WHEN** a candidate's rationale cites only `praise` labels without
  episode counts and a forecast record
- **THEN** the candidate is invalid and MUST be rejected by the validator

### Requirement: Consent Scope Gates Downstream Use
Every episode SHALL carry a consent scope with independently grantable
tiers `episode_use | automation | pooling`, default deny, stamped at
capture; family mining and corpus curation SHALL honor `episode_use`, and
the `pooling` tier is frozen into the vocabulary now but has no consumer
until the cross-tenant wave.

#### Scenario: Episode-use consent is denied

- **WHEN** a tenant has not granted `episode_use`
- **THEN** that tenant's episodes MUST be excluded from family mining,
  forecasts, and corpora
- **AND** the episodes still exist as derived audit projections

### Requirement: The Sweep Is Bounded And Read-Only
Ledger computation SHALL run as a bounded, read-only lane on the nightly
cadence with event-driven reconcile on family milestones, whose only writes
are ledger records and candidate records, and which SHALL fail closed to a
skipped-and-reported state that leaves the prior ledger state standing.

#### Scenario: The sweep mutates nothing else

- **WHEN** the sweep lane runs
- **THEN** no source document, policy object, job, or budget is mutated

#### Scenario: A sweep failure is a skip

- **WHEN** the lane fails or its worker output is invalid
- **THEN** the run MUST be recorded as skipped with a reason
- **AND** the prior ledger state remains authoritative
