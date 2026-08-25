# document-lifecycle Delta: Cross-Factory Ideation Routing

## MODIFIED Requirements

### Requirement: Ideation work area convention
Each repository that authors governance documents SHALL host its pre-proposal
pipeline in `ideation/brainstorm/` (non-normative capture) and
`ideation/staging/` (organized fragments). Content in `ideation/brainstorm/`
MAY contradict promoted specs; that area is the only place where contradiction
is sanctioned. Known-domain ideas SHALL be captured in their owning
DomainxFactory; clearly neutral or already cross-domain ideas SHALL be captured
in openxFactory; and genuinely unknown-owner ideas SHALL be captured as
independent items under
`openxFactory/ideation/brainstorm/inbox/<idea-id>/`. A domain-origin idea that
later crosses boundaries SHALL retain its original source while an openxFactory
routing hub is created under
`ideation/brainstorm/cross-domain/<idea-id>/`. The xFactory aggregation
repository MUST NOT host a general ideation backlog, and a monolithic tagged
inbox MUST NOT replace independently routable items.

#### Scenario: Brainstorm content is organized
- **WHEN** brainstorm material is selected for progression
- **THEN** it MUST be organized into `ideation/staging/` or a candidate register with identified targets and deduplicated claims
- **AND** the brainstorm source MUST be marked `staged` (or note what was extracted) rather than silently duplicated

#### Scenario: Staged content becomes a proposal
- **WHEN** a staged topic is ready for ratification
- **THEN** an OpenSpec change MUST be created carrying the spec deltas
- **AND** the staged material MUST reference that change

#### Scenario: Clearly neutral or cross-domain topic is captured
- **WHEN** ideation is known at capture to concern the neutral layer or multiple DomainxFactories
- **THEN** it MUST be captured in openxFactory's brainstorm area

#### Scenario: Ownership is genuinely unknown
- **WHEN** an idea's owner cannot yet be determined
- **THEN** it MUST be captured as an independent openxFactory inbox item without guessing an owner

#### Scenario: Domain-origin topic expands
- **WHEN** a DomainxFactory brainstorm later develops neutral or other-domain claims
- **THEN** its original domain source MUST remain in place as design history and authority for local meaning
- **AND** an openxFactory cross-domain routing hub MUST reference the source and coordinate extracted claims

#### Scenario: General backlog is placed in aggregation
- **WHEN** a general brainstorm area, unclassified inbox, or monolithic tagged backlog is created in the xFactory aggregation repository
- **THEN** lifecycle validation MUST reject the placement

### Requirement: Proposal-owned supporting documents
When staged material crosses the proposal gate, the selected source documents SHALL
move from `ideation/staging/<topic>/` into
`openspec/changes/<change-id>/supporting-docs/`. The active change SHALL own a
machine-readable manifest recording the original staging path, source revision,
transition date, selected files and hashes, optional NotebookLM workspace
provenance, and any material remaining staged. When selected material derives
from routed claims, the manifest SHALL additionally carry an
`ideation_provenance` entry for each source idea, naming the Idea ID, selected
Claim IDs, and a routing-record reference with canonical repository ID,
repository-relative path, and full committed revision. The Claim IDs SHALL
resolve in that pinned routing record. Unrelated proposals MUST NOT invent
ideation provenance. Proposed prose SHALL carry `Status: draft` and name the
change; immutable evidence SHALL carry `Status: record`.

#### Scenario: A complete staged topic becomes a proposal
- **WHEN** every file in a staged topic is selected for an OpenSpec change
- **THEN** the files MUST move into that change's `supporting-docs/` folder
- **AND** the empty staging topic MUST be removed so it no longer appears in the organized-work queue

#### Scenario: Part of a staged topic becomes a proposal
- **WHEN** only some staged files or fragments are selected for a change
- **THEN** only the selected material MUST move into the change's `supporting-docs/` folder
- **AND** the manifest MUST identify material remaining in staging

#### Scenario: Supporting material is non-normative evidence
- **WHEN** a generated report, imported source, or other immutable evidence supports a proposal
- **THEN** it MUST retain `Status: record` rather than becoming draft policy

#### Scenario: Routed material enters a proposal
- **WHEN** staged material derived from routed claims crosses the proposal gate
- **THEN** its manifest MUST name every source Idea ID and selected Claim ID
- **AND** each routing-record repository, path, and full committed revision MUST resolve

#### Scenario: Proposal cites a missing routed claim
- **WHEN** proposal provenance names a Claim ID absent from its pinned routing record
- **THEN** strict proposal validation MUST fail

#### Scenario: Proposal omits a routing revision
- **WHEN** routed proposal provenance does not pin a full committed revision for the routing record
- **THEN** strict proposal validation MUST fail

#### Scenario: Proposal has no routed source
- **WHEN** a proposal did not derive from routed claims
- **THEN** its support manifest MUST remain valid without `ideation_provenance`
