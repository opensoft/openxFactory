# canonical-contract-migration Specification

## Purpose
Govern how shared contract schemas move from source repos (e.g.
Omnigent-Install) into `openxFactory/contracts/` as the canonical home:
copy-first slices, recorded source commits, and manifest entries that keep
adapter ownership with the install repos while openxFactory owns meaning,
versioning, and compatibility.

## Requirements

### Requirement: Copy-first contract migration
The system SHALL migrate shared contracts into `openxFactory/contracts/` using
copy-first feature slices.

#### Scenario: Shared schema is copied
- **WHEN** a schema from an install repo governs behavior between factory subsystems
- **THEN** it MUST be copied or summarized into `openxFactory/contracts/` before install repo copies are removed

#### Scenario: Generated adapter exists
- **WHEN** an install repo has generated clients, adapters, smoke fixtures, or runtime configs derived from a contract
- **THEN** those implementation files MUST remain in the install repo unless a separate approved feature moves them

### Requirement: Contract provenance and compatibility
Each migrated contract SHALL document source provenance and compatibility
expectations.

#### Scenario: Contract is migrated
- **WHEN** a contract is added to `openxFactory/contracts/`
- **THEN** it MUST identify its source path, intended consumers, compatibility version or commit, and adapter ownership rule

#### Scenario: Contract breaks an adapter
- **WHEN** a contract change would break Hermes, Omnigent, Keycloak, OpenXPKI, worker-host, or Ops-gateway runtime adapters
- **THEN** the contract change MUST be split from adapter migration or explicitly approved as a breaking change

**Removed from canon by refresh-install-repository-enumerations-opsxfactory-gateway (2026-10-08):** `**WHEN** a contract change would break Hermes, Omnigent, Keycloak, OpenXPKI, or worker-host runtime adapters` — the bullet is REPLACED rather than deleted, by the widened trigger above it. The edit is a list extension and nothing else: canon's grammar `would break <families> runtime adapters` is kept, one adapter family is appended in canon's own style of naming a family and not a repository, and canon's own `or` moves to stand before the last family. The requirement's body and its other scenario are canon's words.

### Requirement: Contract validation evidence
Each contract migration feature SHALL record validation evidence.

#### Scenario: Contract feature is ready for PR
- **WHEN** a contract migration feature is ready for PR
- **THEN** it MUST include OpenSpec validation, file/syntax validation where applicable, and evidence that install repo copies were not deleted
