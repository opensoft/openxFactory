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
green run of that surface. Where realization deploys onto a surface that is
a registered managed subject of another factory, the realization evidence
SHALL reference the completed deployment handoff request by correlation
identifier — correlation, not duplication: the request record remains with
the executing factory. Until then the change remains active as
approved-but-unrealized intent, preserving the invariant that promoted
specs describe what the code does.

#### Scenario: Implementation is merged but the run fails
- **WHEN** a code-surface change's artifacts are merged but its runnable surface has not run green
- **THEN** the change remains active
- **AND** archiving it is a contested-class act requiring an explicit disposition

#### Scenario: Realization completes
- **WHEN** merge evidence and a green run exist on the implemented target
- **THEN** the change archives and its deltas promote, exactly as doc-only changes do on landing

#### Scenario: Realization deploys onto a managed subject
- **WHEN** a change's realization includes deployment onto a registered managed subject of another factory
- **THEN** the realization evidence references the completed handoff request's correlation identifier
- **AND** a deployment claim with no correlatable accepted request MUST NOT count as realization evidence

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

### Requirement: Proposal support archive gate
An OpenSpec change with proposal supporting documents SHALL NOT archive until
all accepted normative claims have been represented in its proposal, design, or
spec delta; any proposal hybrid has completed its final source import; strict
validation passes; and the supporting folder has been converted into a
deterministic bundle with a readable, verifiable manifest. Packaging SHALL wrap
the normal OpenSpec archive operation rather than replace spec promotion.

#### Scenario: Supporting material contains uncaptured accepted claims
- **WHEN** accepted normative content exists only in `supporting-docs/`
- **THEN** the change MUST remain active until that content is represented in the proposal, design, or spec delta

#### Scenario: Archive preflight succeeds
- **WHEN** implementation and repository tests pass, strict OpenSpec validation passes, final source returns complete, and the support bundle verifies
- **THEN** the normal OpenSpec archive operation MAY run
- **AND** canonical spec promotion MUST proceed unchanged

### Requirement: Origin retention at archive
The archive gate SHALL verify that a change's `.openspec.yaml` still carries
its original origin declaration unchanged. For staged origins, the
compressed supporting-document manifest SHALL retain the same origin id and
path; for ad-hoc origins, the archived change SHALL retain the reason and
approval provenance even when no support bundle exists. Mutation of an
origin declaration after ratification SHALL be rejected at the archive gate.

#### Scenario: A staged-origin change archives
- **WHEN** a change with a staged origin reaches its archive gate
- **THEN** the archived `.openspec.yaml` and the readable support manifest MUST carry the identical origin id and path declared at creation

#### Scenario: An ad-hoc change without a support bundle archives
- **WHEN** a change with an ad-hoc origin and no supporting documents reaches its archive gate
- **THEN** the archived packet MUST retain the origin's reason, approving authority, and approval date

#### Scenario: An origin was mutated after ratification
- **WHEN** the archive gate finds the origin declaration differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** restoring or accepting the mutation is a contested-class act requiring an explicit disposition

