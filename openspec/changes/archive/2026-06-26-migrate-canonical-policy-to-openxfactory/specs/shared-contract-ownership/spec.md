## MODIFIED Requirements

### Requirement: Canonical contract home
`openxFactory` SHALL define the canonical home for shared factory contracts
used between Hermes, Omnigent/Polly, Spec Kit, OpenSpec, GitHub, and merge
council workflows. Migrated contracts SHALL preserve source provenance and
consumer compatibility expectations.

#### Scenario: Shared schema is introduced
- **WHEN** a schema or contract governs behavior between two or more factory subsystems
- **THEN** the canonical contract MUST be defined or referenced from `openxFactory/contracts/`

#### Scenario: Subsystem adapter needs a contract
- **WHEN** an install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema copy
- **THEN** the install repo MAY keep an implementation copy but MUST identify the corresponding `openxFactory` contract version

#### Scenario: Existing schema is migrated
- **WHEN** a shared schema is copied from an install repo into `openxFactory/contracts/`
- **THEN** the canonical copy MUST identify the source path, intended consumers, compatibility reference, and adapter ownership rule

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
