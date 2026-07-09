## ADDED Requirements

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
