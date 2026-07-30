# crystallized-capability-registry Specification

## Purpose
TBD - created by archiving change add-capability-steward. Update Purpose after archive.
## Requirements
### Requirement: The Registry Is Governed Truth With A Derived Index
The registry SHALL be git-resident governed records (one per capability:
identity, family refs, fence ref, rung, artifact digest + packaging +
residence, effect class, provenance ref, permission binding, consent
scope, cost profile, health ref, status with history, authority block,
owner, dry-run declaration), and the hot-path dispatch index SHALL be a
governed derived projection of those records — regenerated on change,
never hand-edited.

#### Scenario: The index is a projection

- **WHEN** a registry record changes
- **THEN** the dispatch index MUST be regenerated from the records
- **AND** a hand-edit to the index is nonconformant regardless of intent

### Requirement: Dispatch Reads Only The Registry
A capability absent from the registry SHALL NOT exist operationally: the
dispatch junction reads only the registry (via its derived index), and no
side registry, allowlist, or ad-hoc lookup may make a capability
reachable.

#### Scenario: An unregistered capability cannot serve

- **WHEN** an artifact exists in a repository but has no registry record
- **THEN** the junction MUST NOT route any instance to it

### Requirement: Records Reference And Never Embed
Registry records SHALL carry digests and references only — never episode
payloads, corpus content, or artifact bytes — so a registry leak leaks no
tenant data.

#### Scenario: An embedded payload is rejected

- **WHEN** a registry record embeds episode or corpus content instead of
  a digest reference
- **THEN** the record is invalid and MUST be rejected

### Requirement: The Status Spine Advances Only Through Proof Gates
The status vocabulary SHALL be `candidate | building | shadow | canary |
active | degraded | retired`, deliberately mirroring the document
lifecycle, and every transition SHALL be recorded in the status history
citing the gate outcome that caused it — a capability cannot reach
`active` without traversing its decision's proof obligations in order.

#### Scenario: A proof stage cannot be skipped

- **WHEN** a record's status history jumps from `candidate` or `building`
  directly to `active`
- **THEN** the record is invalid and MUST be rejected

#### Scenario: Transitions cite their gates

- **WHEN** a status transition is recorded
- **THEN** it MUST reference the workflow-gate outcome that authorized it

### Requirement: Artifacts Are Pinned While Authority Is Live
Registry consumers SHALL pin capability artifacts by digest with
deliberate re-pin, and the authority block (serving flag, demotion
reason) SHALL be live-read at every dispatch decision — a demotion or
retirement takes effect at the next junction decision and never waits for
a consumer re-pin.

#### Scenario: Demotion is immediate at the junction

- **WHEN** a capability's authority block is set to not-serving
- **THEN** the next dispatch decision for its family MUST route to the AI
  path even though consumers still pin the artifact digest

#### Scenario: Pins govern bytes, not authority

- **WHEN** a consumer's pinned artifact digest lags a newer capability
  version
- **THEN** that is pin lag on bytes only
- **AND** authority questions are always answered by the live block

### Requirement: Field Writes Follow The Authority Matrix
Registry fields SHALL have declared writers — build writes identity,
artifact, and provenance once; proof gates advance status; the steward
writes health; accounting writes the cost profile — and a writer touching
another's fields is nonconformant.

#### Scenario: A cross-writer edit is a finding

- **WHEN** a health update also modifies the artifact digest or status
- **THEN** the write is invalid and MUST be rejected

