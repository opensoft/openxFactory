# shared-contract-ownership Specification

## Purpose
Defines how `openxFactory` owns shared factory contracts, how install repos pin
contract compatibility, how submodules are sequenced, and how evidence is
preserved from proposal through merge readiness.
## Requirements
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

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract versions or commits from
`openxFactory` before runtime adapters are treated as compatible.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract
- **THEN** it MUST document which `openxFactory` contract version or commit it is compatible with

#### Scenario: Contract changes incompatibly
- **WHEN** a shared contract change would break an install repo adapter or smoke test
- **THEN** the change MUST be split from adapter migration or explicitly approved as a breaking change

### Requirement: Submodule sequencing
`openxFactory` SHALL document submodule intent and update procedures before
adding install repositories as submodules.

#### Scenario: Submodule is proposed
- **WHEN** a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule
- **THEN** a decision record MUST document the remote, path, pinned commit, update process, and rollback process

#### Scenario: Hermes-Install remote is unresolved
- **WHEN** `Hermes-Install` still points to a non-Opensoft remote and the target umbrella repo is `opensoft/openxFactory`
- **THEN** the Hermes submodule MUST NOT be added until the move, fork, mirror, or external remote decision is approved

### Requirement: Evidence preservation
Each repo-boundary feature SHALL preserve traceability evidence from proposal
through merge readiness. Content migration features SHALL also preserve source
inventory and post-merge install repo link/update evidence where applicable.

#### Scenario: Feature proceeds to PR admission
- **WHEN** a repo-boundary feature is ready for PR
- **THEN** the feature MUST have a proposal or change record, acceptance criteria, implementation diff, local check result, branch review result, and PR admission packet

#### Scenario: Feature proceeds to merge
- **WHEN** a repo-boundary feature is considered for merge
- **THEN** merge council MUST have a merge readiness report that references the relevant OpenSpec change, feature slice, and evidence artifacts

#### Scenario: Content migration feature proceeds to merge
- **WHEN** a dogfood content migration feature is considered for merge
- **THEN** merge readiness MUST include source provenance, copy-first compliance, and evidence that source repos were not destructively changed in the same PR
