# Commission the production private-connectivity installer

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-connectivity-installer-production](../../proposal.md).

## Purpose

Provide opensoft/xFactory-Installer's production behavior and verifiable source, release and qualification boundary while retaining neutral private-connectivity and rollout authority requirements.

## ADDED Requirements

### Requirement: Usable optional installation choices

The installer SHALL expose a usable command/package for supported install-new, connect-existing, managed and qualified unbound choices. Optional absence and independent local operation MUST preserve ratified behavior.

#### Scenario: Usable optional installation choices succeeds within scope
- **WHEN** an authorized operator selects a supported local or unbound choice
- **THEN** the command performs only that choice without a hosted subscription requirement

#### Scenario: Usable optional installation choices refuses invalid scope or proof
- **WHEN** a caller attempts to downgrade a trusted binding requirement
- **THEN** selection refuses unsafe publication

### Requirement: Actual managed selection authority

Managed selection SHALL use the actual supported service and current customer/environment/entitlement/attachment authority. Credentials and route authority MUST remain protected and separately scoped.

#### Scenario: Actual managed selection authority succeeds within scope
- **WHEN** a legitimate current choice uses the exact released service/content
- **THEN** actual enrollment/readiness follows its approved scope

#### Scenario: Actual managed selection authority refuses invalid scope or proof
- **WHEN** a foreign, expired, replayed or changed choice is retried
- **THEN** the installer refuses it and preserves original subjects

### Requirement: Durable migration and rollback

The installer SHALL durably retain original operation/cleanup identity across restart, remove partial target access before restoration and freshly reauthorize the prior binding. Invalid prior access MUST NOT reactivate.

#### Scenario: Durable migration and rollback succeeds within scope
- **WHEN** an approved migration resumes after interruption
- **THEN** cleanup and cutover act on original subjects in order

#### Scenario: Durable migration and rollback refuses invalid scope or proof
- **WHEN** the previous binding is revoked, expired or unentitled
- **THEN** rollback refuses restoration and reports the affected state

### Requirement: Supported distribution and compatibility proof

Distribution SHALL retain deterministic build, actual collected source CI and exact supported neutral/package/service content identity. Workstation-intake, Store and visibility changes remain outside this scope.

#### Scenario: Supported distribution and compatibility proof succeeds within scope
- **WHEN** the command/package candidate is published by its owner
- **THEN** compatible content and provenance are independently readable

#### Scenario: Supported distribution and compatibility proof refuses invalid scope or proof
- **WHEN** only copied bytes, a mutable reference or an uncollected suite is offered
- **THEN** supported release readiness fails
