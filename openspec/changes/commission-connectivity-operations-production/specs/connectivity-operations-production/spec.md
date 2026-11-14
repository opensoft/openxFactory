# Commission production connectivity execution and operations

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-connectivity-operations-production](../../proposal.md).

## Purpose

Provide opensoft/opsXfactory's production behavior and verifiable source, release and qualification boundary while retaining neutral private-connectivity and rollout authority requirements.

## ADDED Requirements

### Requirement: Existing managed-subject authority controls execution

Execution SHALL reuse registered-subject intake, accepted requests, correlation and current channel-required grants or reviewed pull reconciliation. It MUST NOT introduce universal minting or standing producer deployment credentials.

#### Scenario: Existing managed-subject authority controls execution succeeds within scope
- **WHEN** a current accepted request reaches its managing-factory channel
- **THEN** only its scoped Ops executor acts and trusted readback remains distinct

#### Scenario: Existing managed-subject authority controls execution refuses invalid scope or proof
- **WHEN** a subject is inactive/unregistered or required authority is missing
- **THEN** execution is refused before effects

### Requirement: Recovery and cutover preserve authorization

Recovery/cutover SHALL fence, quarantine, restore, reconcile authoritative current revocations and verify before activation. Original cleanup subjects MUST persist and invalid prior bindings cannot return.

#### Scenario: Recovery and cutover preserve authorization succeeds within scope
- **WHEN** an authorized bounded restore/cutover completes
- **THEN** verification and renewed authority precede activation

#### Scenario: Recovery and cutover preserve authorization refuses invalid scope or proof
- **WHEN** a stale writer, failed cleanup or revoked prior is found
- **THEN** the affected state remains contained and neighbors are preserved

### Requirement: Measurements account for missing time

Proof SHALL use independent legitimate/denial/neighbor controls, actual clock/event anchors and accepted finite metric/window/gap limits. Omitted time MUST NOT count as healthy observation.

#### Scenario: Measurements account for missing time succeeds within scope
- **WHEN** the approved actual run is measured
- **THEN** coverage, values and gaps are compared with accepted limits

#### Scenario: Measurements account for missing time refuses invalid scope or proof
- **WHEN** coverage, a control or a valid measurement is missing
- **THEN** acceptance fails instead of inferring health

### Requirement: Bounded incidents and fresh resume

Containment SHALL preserve unrelated authorized scope and immutable incident/cleanup history, with reviewed remediation, affected/adjacent reruns and fresh resume authority.

#### Scenario: Bounded incidents and fresh resume succeeds within scope
- **WHEN** a scoped incident is repaired/requalified
- **THEN** genuine reruns and current fresh authority govern resume

#### Scenario: Bounded incidents and fresh resume refuses invalid scope or proof
- **WHEN** a failed window or old approval is reused
- **THEN** resume and affected eligibility are refused

### Requirement: Required private coverage and guarded runtime

The private suite SHALL run explicitly in an additional required GitHub Actions context while all existing native checks remain enforced. Live qualification MUST require manual dispatch and a current approved run, never ordinary PR/push events.

#### Scenario: Required private coverage and guarded runtime succeeds within scope
- **WHEN** the validation workflow is present on main
- **THEN** the actual Actions context is required and collected at the exact head

#### Scenario: Required private coverage and guarded runtime refuses invalid scope or proof
- **WHEN** an unapproved/source event attempts target operations
- **THEN** the live runner refuses effects and source proof stays source-only
