# repo-boundary-governance Specification

## Purpose
Defines how `openxFactory`, `Hermes-Install`, and `Omnigent-Install` assign
canonical workflow policy ownership, install repository scope, copy-first
migration rules, and guarded repo-boundary execution.
## Requirements
### Requirement: Canonical workflow authority
`openxFactory` SHALL be the canonical repository for domain-neutral factory
workflow policy, authority rules, role definitions, traceability rules,
admission concepts, merge authority concepts, and cross-system operating
contracts. Domain-specific execution policy SHALL live in the owning
DomainxFactory.

#### Scenario: Factory policy is introduced
- **WHEN** a new policy affects Hermes, Omnigent/Polly, OpenSpec, GitHub, merge council behavior, or more than one DomainxFactory at the domain-neutral workflow layer
- **THEN** the canonical policy MUST be created or updated in `openxFactory`

#### Scenario: Domain execution policy is introduced
- **WHEN** a policy defines software engineering Spec Kit mechanics, clinical review mechanics, operations runbook execution, accounting close workflow execution, marketing campaign execution, or another domain-specific workflow implementation
- **THEN** the canonical implementation policy MUST be created or updated in the owning DomainxFactory
- **AND** `openxFactory` MUST reference it only as a specialization of neutral workflow gates

#### Scenario: Install repo needs policy context
- **WHEN** `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openxFactory` policy for neutral workflow concerns
- **AND** it MUST link to the owning DomainxFactory policy when implementing domain-specific execution behavior

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
replacements, scope links, and validation checks are in place. Content
migration SHALL be dogfooded through OpenSpec, Hermes approval,
Omnigent/Polly decomposition, PR admission, merge council, and GitHub PRs.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install` or `Omnigent-Install`
- **THEN** the policy MUST be copied or summarized into `openxFactory` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

#### Scenario: Content migration starts
- **WHEN** canonical policy or contract content is migrated after the repo-boundary pilot
- **THEN** the work MUST be proposed, decomposed, reviewed, admitted to PR, and merged using the factory workflow itself

### Requirement: Guarded pilot execution
The initial repo-boundary pilot SHALL be doc-only, start in `openxFactory`,
and avoid deletions, submodules, runtime code movement, secrets, credentials,
generated state, databases, and runtime workspaces. Later dogfood migration
features SHALL keep the same stop conditions unless Hermes approves a narrower
exception for a specific feature.

#### Scenario: First pilot feature is executed
- **WHEN** FEAT-RB-001 is implemented
- **THEN** it MUST touch `openxFactory` only and MUST NOT change install repo files, runtime code, or submodules

#### Scenario: Stop condition is encountered
- **WHEN** a change proposes deleting install repo files, touching secrets, combining submodules with file moves, or modifying runtime state
- **THEN** the pilot MUST stop until Hermes approves a separate scoped feature

#### Scenario: Dogfood migration feature reaches a stop condition
- **WHEN** a dogfood migration feature proposes deleting source docs, moving runtime code, changing submodule pointers, or touching generated state
- **THEN** the feature MUST stop and return to Hermes approval before implementation continues

### Requirement: Install repo scope links
Install repositories SHALL explicitly link back to `openxFactory` for canonical
factory workflow policy once their scope clarification feature is approved.

#### Scenario: Omnigent-Install scope is clarified
- **WHEN** the Omnigent install scope feature is implemented
- **THEN** its README MUST state that `openxFactory` owns factory workflow policy and that `Omnigent-Install` owns Omnigent/Polly install and DR

#### Scenario: Hermes-Install scope is clarified
- **WHEN** the Hermes install scope feature is implemented
- **THEN** its README MUST state that `openxFactory` owns factory workflow policy and that `Hermes-Install` owns Hermes install and DR
