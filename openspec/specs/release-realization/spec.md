# release-realization Specification

## Purpose
TBD - created by archiving change add-release-realization-flow. Update Purpose after archive.
## Requirements
### Requirement: Realization axis declaration
Every OpenSpec change proposal SHALL declare `code_surface:` — `none` or
the repositories whose runtime artifacts it changes — and
`target_release:` — `implemented` (the affected repositories' main lines)
or a named release defined in the aggregation repository. A proposal
without the declarations is a doc-only change (`code_surface: none`,
`target_release: implemented`) by default.

#### Scenario: A doc-only change is proposed
- **WHEN** a change alters only governance documents, schemas-as-documents, or contract prose
- **THEN** its code_surface is `none` and it archives when its artifacts land, as before

#### Scenario: A code-surface change is proposed
- **WHEN** a change alters scripts, workflows, services, or other runtime artifacts
- **THEN** its proposal MUST declare the affected repositories as code_surface and its target release

### Requirement: Realization archive gate
A change with a non-empty code surface SHALL NOT archive until realization
evidence exists: its code merged on the implemented target through the
owning domain's engineering gates, and — where the surface is runnable — a
green run of that surface. Until then the change remains active as
approved-but-unrealized intent, preserving the invariant that promoted
specs describe what the code does.

#### Scenario: Implementation is merged but the run fails
- **WHEN** a code-surface change's artifacts are merged but its runnable surface has not run green
- **THEN** the change remains active
- **AND** archiving it is a contested-class act requiring an explicit disposition

#### Scenario: Realization completes
- **WHEN** merge evidence and a green run exist on the implemented target
- **THEN** the change archives and its deltas promote, exactly as doc-only changes do on landing

### Requirement: Decomposition scale rule
A ratified code-surface change SHALL be an admitted engineering intent
record for the owning domain's intake. Changes whose tasks are executable
directly MAY realize through their own task list; multi-feature changes
SHALL go through feature decomposition into Spec Kit feats; changes
targeting a batched release SHALL decompose late, from the release delta
against the implemented target at release-merge time.

#### Scenario: A small change realizes
- **WHEN** a ratified change's tasks are individually executable without a feature DAG
- **THEN** executing the tasks through the engineering gates satisfies decomposition

#### Scenario: A batched release becomes ready
- **WHEN** a release branch is ready to merge into the implemented line
- **THEN** the feats to implement are decomposed from the delta between the release and the implemented target

### Requirement: Ordered deltas and branch vocabulary
Changes SHALL sequence explicitly: a proposal modifying a requirement
already modified by an active ratified change references that change and
declares its deltas relative to that change's outcome. The three branch
kinds SHALL be used as distinct vocabulary: the change folder (content
branch), Spec Kit feature branches, and release branches (integration);
releases are branches while open and tags at promotion.

#### Scenario: Two changes touch one requirement
- **WHEN** a proposal modifies a requirement that an active ratified change already modifies
- **THEN** the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome

#### Scenario: A release promotes
- **WHEN** a release branch merges to the implemented line and realization completes for its changes
- **THEN** the release is tagged and the branch is retired

