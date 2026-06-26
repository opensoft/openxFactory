# repo-boundary-governance Specification

## Purpose
Defines how `openWorkflow`, `Hermes-Install`, and `Omnigent-Install` assign
canonical workflow policy ownership, install repository scope, copy-first
migration rules, and guarded repo-boundary execution.

## Requirements
### Requirement: Canonical workflow authority
`openWorkflow` SHALL be the canonical repository for factory-level workflow
policy, authority rules, role definitions, traceability rules, merge policy,
and cross-system operating contracts.

#### Scenario: Factory policy is introduced
- **WHEN** a new policy affects Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub, or merge council behavior together
- **THEN** the canonical policy MUST be created or updated in `openWorkflow`

#### Scenario: Install repo needs policy context
- **WHEN** `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openWorkflow` policy rather than become the policy source of truth

### Requirement: Install repository scope
`Hermes-Install` and `Omnigent-Install` SHALL be scoped to subsystem install,
operations, backup, restore, upgrade, verification, and disaster recovery.

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`

### Requirement: Copy-first migration
Repo-boundary migration SHALL use copy-first migration until canonical
replacements, scope links, and validation checks are in place.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install` or `Omnigent-Install`
- **THEN** the policy MUST be copied or summarized into `openWorkflow` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

### Requirement: Guarded pilot execution
The initial repo-boundary pilot SHALL be doc-only, start in `openWorkflow`,
and avoid deletions, submodules, runtime code movement, secrets, credentials,
generated state, databases, and runtime workspaces.

#### Scenario: First pilot feature is executed
- **WHEN** FEAT-RB-001 is implemented
- **THEN** it MUST touch `openWorkflow` only and MUST NOT change install repo files, runtime code, or submodules

#### Scenario: Stop condition is encountered
- **WHEN** a change proposes deleting install repo files, touching secrets, combining submodules with file moves, or modifying runtime state
- **THEN** the pilot MUST stop until Hermes approves a separate scoped feature

### Requirement: Install repo scope links
Install repositories SHALL explicitly link back to `openWorkflow` for canonical
factory workflow policy once their scope clarification feature is approved.

#### Scenario: Omnigent-Install scope is clarified
- **WHEN** the Omnigent install scope feature is implemented
- **THEN** its README MUST state that `openWorkflow` owns factory workflow policy and that `Omnigent-Install` owns Omnigent/Polly install and DR

#### Scenario: Hermes-Install scope is clarified
- **WHEN** the Hermes install scope feature is implemented
- **THEN** its README MUST state that `openWorkflow` owns factory workflow policy and that `Hermes-Install` owns Hermes install and DR
