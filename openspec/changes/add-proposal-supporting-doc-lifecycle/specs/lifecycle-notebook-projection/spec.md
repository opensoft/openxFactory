## MODIFIED Requirements

### Requirement: Hybrid analysis notebooks
The lifecycle notebook projection SHALL support temporary hybrid NotebookLM
notebooks that combine exactly one Canon release line with exactly one origin
idea or proposal-support target. The origin target SHALL be a brainstorm folder
under `ideation/brainstorm/<topic>/`, a staged folder under
`ideation/staging/<topic>/`, or an active proposal folder under
`openspec/changes/<change-id>/supporting-docs/`. Hybrid notebooks SHALL be
derived analysis workspaces, not canonical lifecycle books.

#### Scenario: A brainstorm hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/brainstorm/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/brainstorm/<topic>/` as the origin folder for any returned source material

#### Scenario: A staged hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/staging/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/staging/<topic>/` as the origin folder for any returned source material

#### Scenario: A proposal hybrid is continued
- **WHEN** a staged topic moves into `openspec/changes/<change-id>/supporting-docs/`
- **THEN** its hybrid MUST identify the active supporting-documents folder as the new origin for returned source material
- **AND** the hybrid MUST retain the Canon release line being compared

#### Scenario: Hybrid output is consumed
- **WHEN** any chat answer, note, report, mind map, audio, or other output from a hybrid notebook is used in xFactory work
- **THEN** the output MUST carry `L1 notebook synthesis` authority
- **AND** it MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output

### Requirement: Imported source material provenance
Every imported hybrid source entry SHALL be written to the origin folder as
governed lifecycle material. The imported file SHALL carry the origin lifecycle
status (`brainstorm` for brainstorm origins, `staged` for staged origins, and
`draft` for active proposal supporting-document origins), `Kind: reference`,
the source workspace id or alias, `Authority: L1 notebook synthesis`, the
NotebookLM source id, and the NotebookLM source title. An operator MAY classify
immutable evidence as `record`. Import MUST be idempotent by NotebookLM source
id.

#### Scenario: A source imports into a brainstorm origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/brainstorm/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: brainstorm`

#### Scenario: A source imports into a staged origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/staging/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: staged`

#### Scenario: A source imports into a proposal origin
- **WHEN** an eligible source is imported from a hybrid whose origin is an active change's `supporting-docs/` folder
- **THEN** the imported file MUST be written under that folder
- **AND** the imported file MUST carry `Status: draft` unless explicitly classified as immutable evidence

#### Scenario: The importer is run twice
- **WHEN** a NotebookLM source id already appears in imported lifecycle material
- **THEN** a subsequent import run MUST skip that source id
- **AND** it MUST NOT duplicate the imported entry

## ADDED Requirements

### Requirement: Hybrid finalization before proposal archive
An active proposal hybrid SHALL receive one final source-return import before
its supporting documents are packaged. After the proposal archives, the hybrid
SHALL be retired from active analysis use.

#### Scenario: A proposal reaches its archive gate
- **WHEN** an active change with a proposal hybrid is ready to archive
- **THEN** the archive checklist MUST record a final source-return import
- **AND** packaging MUST run only after that import completes
