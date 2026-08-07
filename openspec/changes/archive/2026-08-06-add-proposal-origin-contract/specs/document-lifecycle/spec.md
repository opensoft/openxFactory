# document-lifecycle Delta: Proposal Origin Contract

## ADDED Requirements

### Requirement: Proposal origin declaration
Every OpenSpec change proposal SHALL declare exactly one origin in its
`.openspec.yaml`, fixed when the proposal is created and unchanged for the
life of the change. A `staged` origin carries `kind: staged`, a durable
`id` of the form `<repo>:staging:<topic-slug>`, and a `path` naming the
original repository-relative staging folder; at the proposal transition the
staged folder MUST contain a document whose `Staging ID:` equals
`origin.id`. An `ad_hoc` origin carries `kind: ad_hoc`, a durable `id` of
the form `<repo>:adhoc:<date>-<sequence-or-slug>`, and required `reason`,
`approved_by`, and `approved_on` fields. Ad-hoc status is an explicit,
approved exception — it MUST NOT substitute for staging when organized
source material exists, and a proposal MUST NOT declare both origin kinds.
Durable ids remain valid after the staging folder moves, is compressed, or
is removed; `origin.path` is the historical record of the transition
source, not a live link.

#### Scenario: A staged proposal is created
- **WHEN** an OpenSpec change is created from a staged topic
- **THEN** its `.openspec.yaml` MUST declare `kind: staged` with the topic's durable id and original staging path
- **AND** the staged folder MUST contain, at transition, a document whose `Staging ID:` equals the declared id

#### Scenario: An ad-hoc proposal is created
- **WHEN** an OpenSpec change is deliberately created without a staging source
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, the approving authority, and the approval date
- **AND** supporting evidence MAY still live under `supporting-docs/` but MUST NOT claim a fabricated staging source

#### Scenario: The proposal gate rejects a malformed origin
- **WHEN** a proposal's origin is missing, declares an unknown kind, declares both kinds, carries a staged id or path that does not resolve before transition, disagrees with the staging header or support manifest, or lacks ad-hoc reason or approval provenance
- **THEN** strict proposal validation MUST fail

#### Scenario: The staging folder later disappears
- **WHEN** a declared staged origin's topic folder moves, is compressed, or is removed after the proposal transition
- **THEN** the origin id and path remain unchanged as historical provenance and MUST NOT be rewritten to track the new location

## MODIFIED Requirements

### Requirement: Proposal-owned supporting documents
When staged material crosses the proposal gate, the selected source documents SHALL
move from `ideation/staging/<topic>/` into
`openspec/changes/<change-id>/supporting-docs/`. The active change SHALL own a
machine-readable manifest recording the original staging path, source revision,
transition date, selected files and hashes, optional NotebookLM workspace
provenance, and any material remaining staged. The manifest SHALL repeat
`origin.kind` and `origin.id` — and, for staged origins, `origin.path` — and
those values MUST match the change's `.openspec.yaml`. When selected material
derives from routed claims, the manifest SHALL additionally carry an
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

#### Scenario: Manifest origin disagrees with the packet
- **WHEN** a support manifest's repeated origin fields differ from the change's `.openspec.yaml` declaration
- **THEN** strict proposal validation MUST fail

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
