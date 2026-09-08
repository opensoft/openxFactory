# canonical-contract-migration Specification (delta)

## MODIFIED Requirements

### Requirement: Contract provenance and compatibility
Each migrated contract SHALL document source provenance and compatibility
expectations.

#### Scenario: Contract is migrated
- **WHEN** a contract is added to `openxFactory/contracts/`
- **THEN** it MUST identify its source path, intended consumers, compatibility version or commit, and adapter ownership rule

#### Scenario: Contract breaks an adapter
- **WHEN** a contract change would break Hermes, Omnigent, Keycloak, OpenXPKI, or worker-host runtime adapters
- **THEN** the contract change MUST be split from adapter migration or explicitly approved as a breaking change

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** `**WHEN** a contract change would break Hermes or Omnigent runtime adapters` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION PLUS THE PUNCTUATION A LONGER LIST TAKES, AND NOTHING ELSE:** canon's grammar `would break <families> runtime adapters` is kept exactly and only the family list widens, from two to five, with the serial comma a five-item list takes before its final `or` where canon's two-item list correctly had none (measured style: `openspec/specs` carries 561 lines with that comma against 232 without). This is the only unit in this capability that a fifth install repository made incomplete: the trigger enumerated TWO runtime ADAPTER FAMILIES — not repositories — while five install repositories now hold adapters over `openxFactory` contracts, the worker host's among them. The requirement's body and its *"Contract is migrated"* scenario are word for word what canon states.
