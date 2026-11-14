# Commission Hosted Headscale and hosted-factory service production

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-hosted-headscale-production](../../proposal.md).

## Purpose

Provide opensoft/openXsoft-Hosted-Services's production behavior and verifiable source, release and qualification boundary while retaining neutral private-connectivity and rollout authority requirements.

## ADDED Requirements

### Requirement: Deployable authenticated product API

The hosted API SHALL derive customer/environment/permissions from verified issuer/audience/key material and authoritative entitlement. Caller-selected identity, privacy or eligibility MUST NOT supply authority.

#### Scenario: Deployable authenticated product API succeeds within scope
- **WHEN** a legitimate principal requests an in-scope entitled operation
- **THEN** the API retains its original subjects and applies the authorized path

#### Scenario: Deployable authenticated product API refuses invalid scope or proof
- **WHEN** a caller asserts another customer's entitlement or approval
- **THEN** the API refuses it without foreign-state or credential disclosure

### Requirement: Actual managed provider handoff

Provisioning SHALL use the selected actual provider and existing accepted-request/channel authority with dedicated state/endpoint/key/policy boundaries. The product MUST NOT acquire standing deployed write credentials or fall back to a synthetic provider.

#### Scenario: Actual managed provider handoff succeeds within scope
- **WHEN** the authorized Ops actor executes a current accepted request
- **THEN** actual trusted readback determines runtime readiness

#### Scenario: Actual managed provider handoff refuses invalid scope or proof
- **WHEN** configuration, authority or actual readback is missing
- **THEN** the operation stays pending/unready without synthetic readiness

### Requirement: Durable independent service lifetimes

The product SHALL preserve original operation/cancellation subjects, conditional state and current revocations through restart/concurrency. Standalone service, factory attachment and network termination MUST retain independent authority/lifetimes.

#### Scenario: Durable independent service lifetimes succeeds within scope
- **WHEN** an interrupted cancellation resumes
- **THEN** cleanup preserves independently entitled services and original subjects

#### Scenario: Durable independent service lifetimes refuses invalid scope or proof
- **WHEN** a retry changes subjects or attempts unrelated termination
- **THEN** it is refused/contained without duplicate or revived access

### Requirement: Trusted profile and phase-specific eligibility

Onboarding/catalog admission SHALL use exact trusted profile/candidate identity, independent application permission and current phase/scope qualification authority. Private requirements MUST NOT be downgraded and source publication MUST NOT grant commercial eligibility.

#### Scenario: Trusted profile and phase-specific eligibility succeeds within scope
- **WHEN** a real profile is eligible in the same approved phase/scope
- **THEN** its actual workload is bound and checked under application authority

#### Scenario: Trusted profile and phase-specific eligibility refuses invalid scope or proof
- **WHEN** a stale, foreign or caller-qualified profile is supplied
- **THEN** admission fails without pilot substitution

### Requirement: Buildable candidate and actual collection

The service SHALL retain a buildable pinned runtime/dependency candidate, explicitly collected source CI and guarded actual-platform runner. Target observations and later decisions remain distinct.

#### Scenario: Buildable candidate and actual collection succeeds within scope
- **WHEN** the candidate passes its actual owned source checks
- **THEN** supported content/provenance and runner identity are retained

#### Scenario: Buildable candidate and actual collection refuses invalid scope or proof
- **WHEN** generic CI omitted a private suite or a target was unobserved
- **THEN** the missing proof cannot satisfy source readiness or a live gate
