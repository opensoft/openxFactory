# shared-contract-ownership Specification

## Purpose
Defines how `openWorkflow` owns shared factory contracts, how install repos pin
contract compatibility, how submodules are sequenced, and how evidence is
preserved from proposal through merge readiness.

## Requirements
### Requirement: Canonical contract home
`openWorkflow` SHALL define the canonical home for shared factory contracts
used between Hermes, Omnigent/Polly, Spec Kit, OpenSpec, GitHub, and merge
council workflows.

#### Scenario: Shared schema is introduced
- **WHEN** a schema or contract governs behavior between two or more factory subsystems
- **THEN** the canonical contract MUST be defined or referenced from `openWorkflow/contracts/`

#### Scenario: Subsystem adapter needs a contract
- **WHEN** an install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema copy
- **THEN** the install repo MAY keep an implementation copy but MUST identify the corresponding `openWorkflow` contract version

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract versions or commits from
`openWorkflow` before runtime adapters are treated as compatible.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract
- **THEN** it MUST document which `openWorkflow` contract version or commit it is compatible with

#### Scenario: Contract changes incompatibly
- **WHEN** a shared contract change would break an install repo adapter or smoke test
- **THEN** the change MUST be split from adapter migration or explicitly approved as a breaking change

### Requirement: Submodule sequencing
`openWorkflow` SHALL document submodule intent and update procedures before
adding install repositories as submodules.

#### Scenario: Submodule is proposed
- **WHEN** a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule
- **THEN** a decision record MUST document the remote, path, pinned commit, update process, and rollback process

#### Scenario: Hermes-Install remote is unresolved
- **WHEN** `Hermes-Install` still points to a non-Opensoft remote and the target umbrella repo is `opensoft/openWorkflow`
- **THEN** the Hermes submodule MUST NOT be added until the move, fork, mirror, or external remote decision is approved

### Requirement: Evidence preservation
Each repo-boundary feature SHALL preserve traceability evidence from proposal
through merge readiness.

#### Scenario: Feature proceeds to PR admission
- **WHEN** a repo-boundary feature is ready for PR
- **THEN** the feature MUST have a proposal or change record, acceptance criteria, implementation diff, local check result, branch review result, and PR admission packet

#### Scenario: Feature proceeds to merge
- **WHEN** a repo-boundary feature is considered for merge
- **THEN** merge council MUST have a merge readiness report that references the relevant OpenSpec change, feature slice, and evidence artifacts
