# canonical-contract-migration Specification (delta)

## MODIFIED Requirements

### Requirement: Contract provenance and compatibility
Each migrated contract SHALL document source provenance and compatibility
expectations.

#### Scenario: Contract is migrated
- **WHEN** a contract is added to `openxFactory/contracts/`
- **THEN** it MUST identify its source path, intended consumers, compatibility version or commit, and adapter ownership rule

#### Scenario: Contract breaks an adapter
- **WHEN** a contract change would break a runtime adapter in an admitted install repository — Hermes, Omnigent, Keycloak, OpenXPKI or worker-host
- **THEN** the contract change MUST be split from adapter migration or explicitly approved as a breaking change

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** `**WHEN** a contract change would break Hermes or Omnigent runtime adapters` — the bullet is REPLACED rather than deleted, by the widened trigger above it. This is the only unit in this capability that a fifth install repository made incomplete: the trigger enumerated TWO runtime adapter families while five install repositories now hold adapters over `openxFactory` contracts, the worker host's among them. The requirement's body and its *"Contract is migrated"* scenario are word for word what canon states.
