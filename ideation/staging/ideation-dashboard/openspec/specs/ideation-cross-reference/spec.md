# ideation-cross-reference Delta: Possibles Register And Human-Seen Clusters

Status: draft
Kind: architecture
Summary: Draft spec-delta slice (MODIFIED ideation-cross-reference, possibles register and human-seen clusters) for the add-ideation-dashboard re-proposal, iterating in staging.
Topics: ideation-dashboard, ideation-cross-reference, doc-management, doc-workflow
Repository context: openxFactory
Draft slice of: [ideation-dashboard staged topic](../../../ideation-dashboard.md) — demoted from the ratified proposal 2026-07-13 (Brett).

## ADDED Requirements

### Requirement: Possibles register consolidation
The cross-reference index SHALL consolidate every `Possible feats:`
declaration into the canonical possibles register, one register entry per
possible with explicit many-to-many edges to its claiming topic clusters —
the same bootstrap posture as the index's tag sources, with no third
standalone register file. Each possible SHALL carry exactly one state:
`latent` (enumerated, unpicked — backlog, not failure), `picked` (citing
the staged topic's staging ID and inheriting the change ID at the proposal
gate), `rejected`, or `superseded`; `rejected` and `superseded` SHALL
require a recorded reason plus a citation, mirroring the contested-finding
disposition rule.

#### Scenario: Declarations are consolidated
- **WHEN** the index pass runs over documents carrying `Possible feats:` sections
- **THEN** the register carries one canonical entry per possible with edges to every claiming cluster

#### Scenario: A possible is rejected without citation
- **WHEN** a register entry transitions to `rejected` or `superseded` without a recorded reason and citation
- **THEN** strict register validation MUST fail the transition

#### Scenario: A picked possible's topic crosses the proposal gate
- **WHEN** the staged topic cited by a `picked` possible becomes an OpenSpec change
- **THEN** the pick citation inherits the change ID while retaining the original staging ID

### Requirement: Human-seen cluster intake
An ad-hoc workbench reference set matching no machine cluster SHALL be
accepted as a human-seen cluster proposal into the same recommendation
queue as machine clustering, carrying the full evidence contract already
used by the panel's scores — committed source revision, passage hash and
section reference, rationale, confidence, alternatives, and
`pending_review` disposition. Human-seen submissions MUST NOT bypass
review: they are recommendations disposed by the same authorities as
machine suggestions.

#### Scenario: A human submits an ad-hoc set
- **WHEN** a workbench user submits a reference set as a human-seen cluster
- **THEN** the submission enters the recommendation queue with the full evidence contract and `pending_review` disposition

#### Scenario: A submission lacks evidence
- **WHEN** a human-seen submission arrives without the complete evidence contract
- **THEN** it MUST be rejected before persistence

#### Scenario: A human-seen cluster is accepted
- **WHEN** the disposing authority accepts a human-seen cluster
- **THEN** it becomes a topic cluster in the index like any machine-derived cluster, recording its human-seen provenance
