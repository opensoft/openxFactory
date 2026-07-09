## ADDED Requirements

### Requirement: Hybrid analysis notebooks
The lifecycle notebook projection SHALL support temporary hybrid NotebookLM
notebooks that combine exactly one Canon release line with exactly one origin
idea target. The origin target SHALL be either a brainstorm folder under
`ideation/brainstorm/<topic>/` or a staged folder under
`ideation/staging/<topic>/`. Hybrid notebooks SHALL be derived analysis
workspaces, not canonical lifecycle books.

#### Scenario: A brainstorm hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/brainstorm/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/brainstorm/<topic>/` as the origin folder for any returned source material

#### Scenario: A staged hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/staging/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/staging/<topic>/` as the origin folder for any returned source material

#### Scenario: Hybrid output is consumed
- **WHEN** any chat answer, note, report, mind map, audio, or other output from a hybrid notebook is used in xFactory work
- **THEN** the output MUST carry `L1 notebook synthesis` authority
- **AND** it MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output

### Requirement: Hybrid source return imports
Hybrid notebook source return SHALL be based on NotebookLM source membership.
Any non-seed source in a hybrid notebook SHALL be eligible to import back into
the hybrid's origin folder. Eligible sources include notes converted to
sources, web sources, sources discovered through NotebookLM research, files,
Drive sources, and any other NotebookLM source type exposed to the importer.
NotebookLM notes that have not been converted to sources SHALL remain scratch
material inside NotebookLM and SHALL NOT be imported.

#### Scenario: A note is converted to a source
- **WHEN** a human creates a NotebookLM note inside a hybrid notebook and converts that note to a source
- **THEN** the converted source MUST be eligible for import into the hybrid's origin folder
- **AND** the source title MUST NOT need manual renaming or export tagging

#### Scenario: A source is added through research or upload
- **WHEN** an operator adds a web, research, file, Drive, or other source to a hybrid notebook after the seed set is created
- **THEN** that source MUST be eligible for import into the hybrid's origin folder
- **AND** the importer MUST preserve the NotebookLM source title and source id in the imported entry

#### Scenario: A scratch note remains unconverted
- **WHEN** a NotebookLM note exists only as a note and has not been converted into a source
- **THEN** the importer MUST NOT import that note into the repository

### Requirement: Hybrid seed source exclusions
Hybrid importers SHALL skip seed sources that exist only to provide analysis
context. Seed sources include the hybrid charter, copied Canon sources,
grounding sources, and originally projected lifecycle sources. Managed seed
titles SHALL include `00 [charter]`, `00 [hybrid charter]`, and titles
beginning `[brainstorm]`, `[staged]`, `[draft]`, `[ratified]`, `[standard]`,
`[spec]`, or `[grounding]`.

#### Scenario: Canon context exists in the hybrid
- **WHEN** a hybrid notebook contains copied Canon sources with `[ratified]`, `[standard]`, or `[spec]` titles
- **THEN** the importer MUST NOT write those sources back into the origin brainstorm or staged folder as new ideas

#### Scenario: Grounding context exists in the hybrid
- **WHEN** a hybrid notebook contains `[grounding]` sources or the lifecycle charter source
- **THEN** the importer MUST treat those sources as seed context
- **AND** it MUST NOT import them as new source material

### Requirement: Imported source material provenance
Every imported hybrid source entry SHALL be written to the origin folder as
governed ideation material. The imported file SHALL carry the origin lifecycle
status (`brainstorm` for brainstorm origins and `staged` for staged origins),
`Kind: reference`, the source workspace id or alias, `Authority: L1 notebook
synthesis`, the NotebookLM source id, and the NotebookLM source title. Import
MUST be idempotent by NotebookLM source id.

#### Scenario: A source imports into a brainstorm origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/brainstorm/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: brainstorm`

#### Scenario: A source imports into a staged origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/staging/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: staged`

#### Scenario: The importer is run twice
- **WHEN** a NotebookLM source id already appears in an imported ideation file
- **THEN** a subsequent import run MUST skip that source id
- **AND** it MUST NOT duplicate the imported entry

### Requirement: Hybrid import review gate
Changes to hybrid notebook import behavior SHALL be review-ready only after
implementation tests for the touched tooling pass, the owning repo validation
suite passes, and OpenSpec validation passes in that order.

#### Scenario: An implementation change modifies hybrid import behavior
- **WHEN** a change modifies the hybrid importer, seed-source rules, imported file shape, or return-path workflow
- **THEN** local implementation tests for the importer MUST run before OpenSpec validation
- **AND** the owning repo validation suite MUST pass before the change is marked ready for review
