# canonical-contract-migration Specification (delta)

## MODIFIED Requirements

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
