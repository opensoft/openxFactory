## MODIFIED Requirements

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
