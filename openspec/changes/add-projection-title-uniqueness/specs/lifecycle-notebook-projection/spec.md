# lifecycle-notebook-projection Specification Delta

## MODIFIED Requirements

### Requirement: Authority framing
Every lifecycle notebook SHALL frame its content against the running system:
source titles carry a `[status]` prefix, a charter source states the
projection and the L1-synthesis rule, and the notebook chat configuration
instructs answers to distinguish running-system claims from proposals.

A source title is also the projection's IDENTITY KEY. The sync derives a
desired set keyed by document path but reconciles it against a book's live
source list BY TITLE, and holds each title at one source. The title
derivation SHALL therefore be INJECTIVE over each book's desired set: every
projected document SHALL receive a title distinct from every other projected
document's, so that a book holds exactly one source per member document and
no member is silently displaced by a namesake. A derivation from a
document's file stem ALONE is not injective, and a filename-by-filename
exception to it is not a rule — the obligation is stated over the whole
derived set precisely so that the next repeated stem is answered by the rule
rather than by a further exception.

The derivation SHALL qualify a stem with the SHORTEST repository-relative
path suffix that distinguishes the document from every other projected
document of the same repository, and a `README` stem SHALL carry no fewer
than its parent directory. The uniqueness scope SHALL be the repository's
whole projected document set rather than one book or one lifecycle status,
so that a document is never retitled because a same-stem sibling's `Status:`
header changed. The `[spec]` and `[grounding]` title families are keyed by
the capability directory name and by a fixed document set rather than by a
file stem, and SHALL be outside this scope.

The sync's parity mode SHALL prove membership at the DOCUMENT level, not at
the title level. Comparing a set of derived titles against a set of live
titles cannot observe a document that never received a title of its own, so
equality of those two sets alone SHALL NOT be reported as parity; the mode
SHALL report a derived title carrying more than one document as a parity
FAILURE that names those documents.

#### Scenario: An idea is discussed in chat
- **WHEN** notebook chat answers a question involving `[brainstorm]`, `[staged]`, or `[draft]` sources
- **THEN** the configured framing MUST cause the answer to label those claims as proposals layered on the running system, not current behavior

#### Scenario: Output is consumed downstream
- **WHEN** any lifecycle notebook output (answer, report, mind map, audio) is used in xFactory work
- **THEN** it carries `L1 notebook synthesis` authority per the source-workspaces model and MUST NOT directly drive gates, memory, policy, or customer-facing output

#### Scenario: Two documents of one repository share a file stem
- **WHEN** two or more projected documents of the same repository derive the same bare stem
- **THEN** each MUST receive a distinct title, qualified by the shortest repository-relative path suffix that distinguishes it from the others
- **AND** the book MUST hold one source per document, never one source standing for several
- **AND** the sync MUST NOT record a document as synced in its manifest unless that document holds a source of its own

#### Scenario: A stem repeats but the documents carry different statuses
- **WHEN** two documents of one repository share a stem and their `Status:` headers place them in different books
- **THEN** both MUST still be qualified, because the uniqueness scope is the repository's whole projected set
- **AND** a later change to either document's status MUST NOT change either title

#### Scenario: Parity is proven over documents
- **WHEN** the parity mode compares the corpus scan against a live book
- **THEN** it MUST report a derived title that carries more than one document as a parity failure naming those documents
- **AND** a book whose live title set equals the derived title set MUST NOT be reported as at parity while any derived title carries more than one document

#### Scenario: The derivation changes and titles move
- **WHEN** a projected document's derived title changes because the derivation changed
- **THEN** the next apply-mode sync MUST delete the source carrying the old title and add one carrying the new title
- **AND** the manifest MUST carry the new title for that document
- **AND** a dry run over the same state MUST report those operations without mutating the provider
