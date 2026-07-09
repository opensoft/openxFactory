## ADDED Requirements

### Requirement: Proposal-owned supporting documents
When staged material crosses the proposal gate, the selected source documents SHALL
move from `ideation/staging/<topic>/` into
`openspec/changes/<change-id>/supporting-docs/`. The active change SHALL own a
machine-readable manifest recording the original staging path, source revision,
transition date, selected files and hashes, optional NotebookLM workspace
provenance, and any material remaining staged. Proposed prose SHALL carry
`Status: draft` and name the change; immutable evidence SHALL carry
`Status: record`.

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

### Requirement: Supporting-document archive retention
Before an OpenSpec change with supporting documents archives, its supporting folder SHALL
be packaged into a deterministic compressed bundle beside the
archived change and a readable manifest SHALL remain outside the bundle with
the bundle and per-file hashes. Historical bundles MUST NOT be stored under
canonical `openspec/specs/`.

#### Scenario: A supported change archives
- **WHEN** an active change with `supporting-docs/` reaches its archive gate
- **THEN** the archived change MUST contain `supporting-docs.tar.gz` and `supporting-docs.manifest.yaml`
- **AND** the uncompressed active supporting folder MUST no longer remain

#### Scenario: A bundle is placed with canonical specs
- **WHEN** a supporting-document archive is found under `openspec/specs/`
- **THEN** lifecycle validation MUST reject it as misplaced historical material
