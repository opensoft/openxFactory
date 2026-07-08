## MODIFIED Requirements

### Requirement: Canonical contract home
`openxFactory` SHALL define the canonical home for shared factory contracts that
govern behavior between factory subsystems or across DomainxFactories. Migrated
contracts SHALL preserve source provenance and consumer compatibility
expectations. Domain-specific artifact schemas and workflow gate contracts MAY
live in the owning DomainxFactory when they preserve upstream `openxFactory`
references.

#### Scenario: Shared schema is introduced
- **WHEN** a schema or contract governs behavior between two or more factory subsystems or DomainxFactories
- **THEN** the canonical contract MUST be defined or referenced from `openxFactory/contracts/`

#### Scenario: Domain artifact schema is introduced
- **WHEN** a schema defines a domain-specific artifact such as a software PR admission packet, clinical review package, operations runbook result, ledger close packet, or campaign workflow artifact
- **THEN** the canonical implementation schema MUST live in the owning DomainxFactory
- **AND** the artifact MUST retain required upstream `openxFactory` scope, gate, and traceability references

#### Scenario: Subsystem adapter needs a contract
- **WHEN** an install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema copy
- **THEN** the install repo MAY keep an implementation copy but MUST identify the corresponding `openxFactory` contract version or owning DomainxFactory contract version

#### Scenario: Existing schema is migrated
- **WHEN** a shared schema is copied from an install repo into `openxFactory/contracts/`
- **THEN** the canonical copy MUST identify the source path, intended consumers, compatibility reference, and adapter ownership rule
