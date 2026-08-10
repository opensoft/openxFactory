# lifecycle-notebook-projection Specification

## Purpose

Define the derived NotebookLM books over the governance corpus: membership
derived from document lifecycle states, authority framing, grounding
context, and sync implementation ownership.
## Requirements
### Requirement: Derived notebook membership
Lifecycle notebooks SHALL derive their source membership from document
`Status:` headers via the canonical projection: `brainstorm` and `staged`
into the owning repository's Ideation book — one Ideation book per governed
repository, title family `xFactory Ideation — <RepoName>`, alias family
`xf-ideation-<repo-slug>` (repository name lowercased) — `draft` into the
shared Working Drafts book, and `ratified`, `standard`, and promoted
OpenSpec capability specs into the shared Canon book. Documents with
`record`, `superseded`, or `retired` status SHALL be excluded. A
repository's ideation membership is the status-derived set alone: charter
and grounding seeds do not constitute membership and SHALL NOT cause a
book's creation. Books SHALL be resolved by notebook title (the provider's
truth); the alias family is a machine-local operator convenience whose
registration is idempotent per run and whose absence is never fatal.
Membership SHALL be reconciled by the sync implementation, never
hand-curated. A repository's Ideation book SHALL be created — with contract
title, tags, chat framing, charter and grounding seeds, and its source
workspace record — on the first apply-mode sync where that repository has
ideation membership; a dry run SHALL report the pending creation without
mutating the provider. At implementation the legacy shared Ideation book
leaves the sync's book set; after per-repository parity is verified the
legacy book and its `xf-ideation` alias SHALL be retired by a recorded
manual act, and the alias SHALL NOT be repointed to any successor book.

#### Scenario: An ideation document projects into its owning repository's book
- **WHEN** a document with `brainstorm` or `staged` status lives in governed repository R
- **THEN** the sync projects its source into R's Ideation book
- **AND** no other repository's Ideation book receives it

#### Scenario: A repository gains its first ideation document
- **WHEN** an apply-mode sync finds a governed repository with status-derived ideation membership and no existing book with the contract title
- **THEN** the sync MUST create the book, apply the contract title, tags, and chat framing, seed charter and grounding, write its source workspace record, and project into it in the same run
- **AND** a dry-run sync over the same state MUST report the pending creation and MUST NOT mutate the provider

#### Scenario: A repository has seeds but no ideation documents
- **WHEN** a governed repository has zero `brainstorm` or `staged` documents
- **THEN** no Ideation book is created for it, regardless of charter or grounding seeding rules

#### Scenario: A book's alias is missing on this machine
- **WHEN** the sync runs on a machine whose local alias store lacks a book's alias
- **THEN** the sync resolves the book by its contract title and re-registers the alias
- **AND** the missing alias MUST NOT abort the book or the run

#### Scenario: A document changes lifecycle state
- **WHEN** a governance document's `Status:` header changes to a state mapped to a different book
- **THEN** the next sync MUST remove its source from the previous book and add it to the book mapped for its new state and owning repository

#### Scenario: A source is added by hand
- **WHEN** a source matching the managed title prefixes exists in a lifecycle notebook without a corresponding repo document
- **THEN** the sync MUST remove it (or report it when running in dry-run mode)

#### Scenario: A document's content changes without a state change
- **WHEN** a projected document is edited in the repository
- **THEN** the sync MUST replace the notebook source so notebook content matches the repository

#### Scenario: The legacy shared Ideation book after the split
- **WHEN** the per-repository book family is implemented
- **THEN** the legacy shared book is no longer a sync target in any mode
- **AND** after every governed repository's Ideation book holds parity with the corpus scan, the legacy book and the `xf-ideation` alias are retired by a recorded manual act
- **AND** no later sync creates, repoints, or writes to that alias

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
`openxFactory` SHALL own this projection contract, the workflow
documentation, and the conforming sync implementation
(`scripts/sync-notebooklm-books.py`). Book identity, charter text, title
prefixes, and chat framing SHALL be treated as contract conformance, not
implementation preference.

#### Scenario: The sync implementation is modified

- **WHEN** the sync implementation changes book definitions, prefixes, charter, exclusions, or chat framing
- **THEN** the change MUST be preceded by an OpenSpec delta to this capability

#### Scenario: A workspace names the sync manager

- **WHEN** a lifecycle notebook declares its `managed_by` implementation
- **THEN** the declared path resolves inside openxFactory, and the invocation is run from the workspace root against every pinned repo

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

### Requirement: Projection capacity guard
The sync implementation SHALL treat the platform per-notebook source cap as
a first-class, preflighted constraint over each book's projected occupancy —
defined as the desired managed set plus the charter plus every unmanaged
source observed in that book's source listing — where the cap is a named
constant declared in the sync implementation and recorded in the workflow
documentation. The sync SHALL warn when a book's remaining headroom (cap
minus projected occupancy) falls to thirty sources or fewer, naming the
book, the occupancy, the cap, and — for any book with no successor split
defined by this capability — the owed remedy: a further OpenSpec delta to
this capability defining that book's split. When projected occupancy would
exceed the cap, the sync SHALL project the deterministic in-cap prefix of
the desired set (stable path order), report the book and the exact excess
sources that cannot project, complete every other book, and exit nonzero.
Predictable, preflightable conditions — a book over its cap, an
unresolvable book, a refused notebook creation — SHALL be contained to the
affected book and reported; they SHALL never abort the remaining books,
fail silently, or surface first as a provider error mid-book.

#### Scenario: A book's headroom runs low
- **WHEN** a book's projected occupancy comes within thirty sources of the cap
- **THEN** the sync emits a warning naming the book, the projected occupancy, and the cap
- **AND** if no successor split is defined for that book, the warning names the owed OpenSpec delta

#### Scenario: A book would exceed the cap
- **WHEN** a book's projected occupancy exceeds the platform cap
- **THEN** the sync projects only the deterministic in-cap prefix of the desired set and reports the exact excess sources
- **AND** it completes the sync of every other book
- **AND** the run exits nonzero

#### Scenario: Unmanaged sources occupy real capacity
- **WHEN** a book holds hand-added sources that the reconciliation deliberately preserves
- **THEN** those sources count toward projected occupancy in both the warning and the overflow computation

#### Scenario: A book fails a preflightable condition
- **WHEN** a book cannot be resolved or its creation is refused by the provider
- **THEN** the sync reports that book's condition, skips it, completes every other book, and exits nonzero

