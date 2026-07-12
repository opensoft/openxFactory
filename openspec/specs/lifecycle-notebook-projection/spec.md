# lifecycle-notebook-projection Specification

## Purpose

Define the derived NotebookLM books over the governance corpus: membership
derived from document lifecycle states, authority framing, grounding
context, and sync implementation ownership.
## Requirements
### Requirement: Derived notebook membership
Lifecycle notebooks SHALL derive their source membership from document
`Status:` headers via the canonical projection: `brainstorm` and `staged`
into the Ideation book, `draft` into the Working Drafts book, `ratified`,
`standard`, and promoted OpenSpec capability specs into the Canon book.
Documents with `record`, `superseded`, or `retired` status SHALL be excluded.
Membership SHALL be reconciled by the sync implementation, never hand-curated.

#### Scenario: A document changes lifecycle state
- **WHEN** a governance document's `Status:` header changes to a state mapped to a different book
- **THEN** the next sync MUST remove its source from the previous book and add it to the new book

#### Scenario: A source is added by hand
- **WHEN** a source matching the managed title prefixes exists in a lifecycle notebook without a corresponding repo document
- **THEN** the sync MUST remove it (or report it when running in dry-run mode)

#### Scenario: A document's content changes without a state change
- **WHEN** a projected document is edited in the repository
- **THEN** the sync MUST replace the notebook source so notebook content matches the repository

### Requirement: Authority framing
Every lifecycle notebook SHALL frame its content against the running system:
source titles carry a `[status]` prefix, a charter source states the
projection and the L1-synthesis rule, and the notebook chat configuration
instructs answers to distinguish running-system claims from proposals.

#### Scenario: An idea is discussed in chat
- **WHEN** notebook chat answers a question involving `[brainstorm]`, `[staged]`, or `[draft]` sources
- **THEN** the configured framing MUST cause the answer to label those claims as proposals layered on the running system, not current behavior

#### Scenario: Output is consumed downstream
- **WHEN** any lifecycle notebook output (answer, report, mind map, audio) is used in xFactory work
- **THEN** it carries `L1 notebook synthesis` authority per the source-workspaces model and MUST NOT directly drive gates, memory, policy, or customer-facing output

### Requirement: Grounding context
Every lifecycle notebook SHALL include the grounding source set — the
document lifecycle doc, the terminology and topology doc, and the
architecture doc — with `[grounding]` titles, regardless of those documents'
own lifecycle states, so chat can compare ideas against the system's shape.

#### Scenario: Grounding doc changes state
- **WHEN** a grounding document's own `Status:` changes
- **THEN** it remains in every book under its `[grounding]` title while also appearing in its state's book under its `[status]` title

### Requirement: Projection implementation ownership
`openxFactory` SHALL own this projection contract and the workflow
documentation; `codexFactory` SHALL own the sync implementation that
conforms to it. Book identity, charter text, title prefixes, and chat
framing SHALL be treated as contract conformance, not implementation
preference.

#### Scenario: The sync implementation is modified
- **WHEN** the sync implementation changes book definitions, prefixes, charter, exclusions, or chat framing
- **THEN** the change MUST be preceded by an OpenSpec delta to this capability

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

### Requirement: Hybrid import review gate
Changes to hybrid notebook import behavior SHALL be review-ready only after
implementation tests for the touched tooling pass, the owning repo validation
suite passes, and OpenSpec validation passes in that order.

#### Scenario: An implementation change modifies hybrid import behavior
- **WHEN** a change modifies the hybrid importer, seed-source rules, imported file shape, or return-path workflow
- **THEN** local implementation tests for the importer MUST run before OpenSpec validation
- **AND** the owning repo validation suite MUST pass before the change is marked ready for review

### Requirement: Hybrid finalization before proposal archive
An active proposal hybrid SHALL receive one final source-return import before
its supporting documents are packaged. After the proposal archives, the hybrid
SHALL be retired from active analysis use.

#### Scenario: A proposal reaches its archive gate
- **WHEN** an active change with a proposal hybrid is ready to archive
- **THEN** the archive checklist MUST record a final source-return import
- **AND** packaging MUST run only after that import completes

### Requirement: Corpus scan scope
The projection SHALL scan exactly the governed corpus: the openxFactory
repository and each DomainxFactory checked out under `xFactories/`. Nested
git working copies below a scanned repository root — feature-branch
worktree checkouts (including `<repo>-worktrees/` containers), embedded
clones, and nested submodule installs — MUST be excluded, so an unmerged or
duplicate checkout can never project sources into a lifecycle book. OpenSpec
change artifacts remain excluded from status scanning while promoted
capability specs project into the Canon book, and deliberate-violation test
fixture corpora remain excluded.

#### Scenario: A worktree container sits under the scan root
- **WHEN** a directory under `xFactories/` holds git worktree checkouts rather than being a governed repository
- **THEN** the sync MUST NOT scan it
- **AND** no source or repository title may derive from its contents

#### Scenario: A nested working copy sits inside a governed repository
- **WHEN** a directory below a scanned repository root carries its own `.git` entry
- **THEN** documents below that directory MUST be excluded from every book

#### Scenario: A governed document also exists in a checkout
- **WHEN** an excluded working copy contains a document that also exists in the governed corpus
- **THEN** only the governed copy projects and no duplicate or colliding source title is created

