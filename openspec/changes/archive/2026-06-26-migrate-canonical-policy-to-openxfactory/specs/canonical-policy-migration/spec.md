## ADDED Requirements

### Requirement: Copy-first policy migration
The system SHALL migrate canonical factory policy into `openxFactory` using
copy-first feature slices.

#### Scenario: Source policy is migrated
- **WHEN** policy currently lives in an install or proof repo
- **THEN** the canonical policy MUST be copied or summarized into `openxFactory` before the source copy is deleted or marked legacy

#### Scenario: Source repo keeps implementation context
- **WHEN** a policy source also contains install-specific context
- **THEN** `openxFactory` MUST keep canonical policy while the install repo MAY retain implementation notes that link back to `openxFactory`

### Requirement: Feature-sliced migration
The system SHALL decompose content migration into independently reviewable
feature slices.

#### Scenario: Migration feature is approved
- **WHEN** Hermes approves a migration feature
- **THEN** the feature MUST have a bounded source inventory, target files, acceptance criteria, validation plan, and stop conditions

#### Scenario: Feature exceeds safe scope
- **WHEN** a feature combines policy migration with deletion, runtime code movement, submodule pointer changes, or generated adapter updates
- **THEN** the feature MUST be split before implementation

### Requirement: Canonical role and authority model
`openxFactory` SHALL own the canonical cross-factory role and authority model.

#### Scenario: Role policy is migrated
- **WHEN** roles such as PO, PM, CA, PA, LA, LE, LC, LQ, LI, LS, Merge Master, or Merge Council are defined
- **THEN** their canonical responsibility, authority, and escalation boundaries MUST live in `openxFactory`

#### Scenario: Install repo uses role policy
- **WHEN** an install repo needs role-specific implementation behavior
- **THEN** it MUST link to the canonical `openxFactory` role policy and document only subsystem-specific implementation details

### Requirement: Canonical stage and merge policy
`openxFactory` SHALL own canonical Spec Kit stage ownership, clarification
routing, PR admission, merge council, and merge master policy.

#### Scenario: Spec Kit ownership is migrated
- **WHEN** `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, or `/speckit.implement` ownership is defined
- **THEN** the canonical ownership and consultation policy MUST live in `openxFactory`

#### Scenario: Merge authority is migrated
- **WHEN** PR admission, merge readiness, merge risk, or human escalation rules are defined
- **THEN** the canonical policy MUST live in `openxFactory`

### Requirement: Source provenance
Each migrated policy document SHALL preserve source provenance.

#### Scenario: Canonical document is created
- **WHEN** a canonical policy document is created in `openxFactory`
- **THEN** it MUST list the source repo files reviewed or state that there was no source file

#### Scenario: Source doc remains
- **WHEN** a source install repo document remains after migration
- **THEN** a later feature MUST either link it to the canonical policy or mark it as legacy, implementation notes, or operational runbook
