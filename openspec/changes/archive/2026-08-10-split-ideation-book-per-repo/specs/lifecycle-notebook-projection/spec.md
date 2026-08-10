# lifecycle-notebook-projection — split-ideation-book-per-repo deltas

## MODIFIED Requirements

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

## ADDED Requirements

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
