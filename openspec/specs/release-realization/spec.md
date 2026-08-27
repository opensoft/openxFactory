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

### Requirement: A history-rewriting landing re-derives the pins its rewrite orphans
A history-rewriting landing SHALL re-derive or re-pin every committed artifact
whose derivation pin names a commit that landing orphans, as part of the landing
itself, and MUST NOT move a pin by hand without regenerating the artifact the
pin describes. A history-rewriting landing is one that lands a branch by rebase,
squash, amend, or force-update.

The obligation belongs to the LANDING and not to a later sweep, and the reason
is mechanical rather than stylistic. Before the rewrite, the pinned commit is
reachable and the artifact can be regenerated from it, so the equivalence
between old pin and new pin is measurable. After the rewrite, the old commit may
be reachable from nothing, and the very state a regeneration would read is gone.
A rule that says "fix it afterwards" therefore describes a repair that may no
longer be performable, which is why this reads as a landing obligation and why
the check that discharges it belongs on the branch rather than on `main`.

RE-PINNING IS DEFINED BY REPRODUCTION, not by the pin's value. Where the
artifact's own tooling defines how the artifact is derived — the cross-reference
derivation and its strict index validator are this repository's worked example —
the re-pin SHALL reproduce the committed body BYTE-FOR-BYTE at the new pin, and
the landing SHALL record that it ran the reproduction rather than asserting the
equivalence. Where no tool defines reproduction, the re-pin SHALL name the
measurement that established equivalence at the new pin, or the artifact SHALL
be regenerated so that the question does not arise. A pin edited to a value that
happens to be reachable, with no reproduction and no measurement, satisfies
nothing: it converts an unverifiable claim into a plausible one, which is worse,
because the next reader has no signal that the claim was never checked.

The rewrite's own commits are not the only pins in question. A landing SHALL
consider every artifact its branch touched AND every artifact already on `main`
whose pin names a commit the rewrite orphans, because a branch can orphan a
commit that a previously landed artifact pins without touching that artifact's
file at all.

Where a landing completes and leaves an orphaned pin behind, accepting it SHALL
be a contested-class act requiring an explicit disposition, and the repair route
SHALL be the one the pinned artifact's own class allows rather than whichever is
convenient.

#### Scenario: A branch whose commits are pinned lands rebased
- **WHEN** a branch is landed by rebase or squash, and a committed artifact pins one of the commits that landing rewrites
- **THEN** the landing MUST re-derive or re-pin that artifact as part of itself, before the rewritten commits become unreachable
- **AND** the landing MUST NOT be treated as complete while the artifact still names an orphaned commit

#### Scenario: A pin is moved by hand without regeneration
- **WHEN** a pin is edited to a new commit and the artifact's body is not regenerated at that commit
- **THEN** the reproduction obligation MUST reject the re-pin, because reproduction was neither run nor recorded
- **AND** the pin's reachability MUST NOT be accepted as evidence that the body matches the state it now claims

#### Scenario: The rewrite orphans no pinned commit
- **WHEN** a landing rewrites history and no committed artifact pins any commit the rewrite orphans
- **THEN** no re-derivation is owed and the landing proceeds unchanged
- **AND** the absence MUST be established by looking, not assumed from the branch's file list

#### Scenario: A landing completes with an orphaned pin on main
- **WHEN** a landing has completed and an artifact on `main` names a commit no ref reaches
- **THEN** accepting that state MUST be a contested-class act carrying an explicit disposition
- **AND** the repair MUST follow the route the artifact's own class allows, which for captured evidence is retention of the commit rather than an edit to the pin

