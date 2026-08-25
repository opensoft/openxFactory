# omnigent-domain-overlay Specification (delta)

## ADDED Requirements

### Requirement: Domain-expert display terminology for declared vocabulary

A domain overlay's optional `terminology` block SHALL be presentation only, and every label it declares SHALL resolve to an id that same overlay declares.
Terminology gives domain-expert display labels for the ids the overlay
declares — `workers`, `job_types`, `stop_conditions`, and `routing`
ambiguity classes. A display label SHALL NOT change a worker's archetype,
its permission matrix, its credential tier, or any authority, exactly as the
Hermes layer model permits a specialized `display_name` without changing
`role` or authority ownership. Every terminology key SHALL resolve to an id
the same overlay declares, and display labels SHALL be unique within their
vocabulary.

#### Scenario: a label for an undeclared id is rejected

- **WHEN** a terminology entry names an id the overlay does not declare
- **THEN** validation fails naming the vocabulary and the orphan key
- **AND** the overlay is not consumable, because a notice would name a class
  that does not exist

#### Scenario: two ids may not share a display label

- **WHEN** two ids in the same vocabulary declare the same display label
- **THEN** validation fails naming both ids
- **AND** the duplicate is treated as a defect, because the two would read
  identically in a human-facing notice

#### Scenario: a label carries no authority

- **WHEN** a worker class declares a display label
- **THEN** its archetype, permission matrix, and credential families are
  unchanged
- **AND** the label is used for presentation only

### Requirement: Human-facing surfaces render domain terminology

Human-facing surfaces SHALL render the declared display label for any id they report where a label exists.
Notices, logs, approval packets, escalations, and refusals presented to a
human therefore show the well-adopted vocabulary of the domain expert's own
field rather than internal identifiers. Ids SHALL remain the
machine identifiers used in configuration, evidence correlation, and
validation, and the neutral worker-archetype vocabulary SHALL NOT be renamed
to match any external framework — the cross-domain spine stays neutral while
presentation is domain-idiomatic.

#### Scenario: a notice names a worker in domain terminology

- **WHEN** a human-facing notice, log line, approval packet, or refusal
  reports a worker class, job type, stop condition, or routing class that has
  a declared label
- **THEN** it renders the display label
- **AND** the underlying id remains available for machine correlation

#### Scenario: the neutral spine is not renamed

- **WHEN** a domain adopts best-practice terminology for its workers
- **THEN** the neutral archetype vocabulary is unchanged across every domain
- **AND** cross-domain consistency continues to rest on the archetypes, not
  on any single industry framework

### Requirement: Standards alignment is a descriptive crosswalk, never an identity or a claim

A worker class's optional `standards_alignment` SHALL be descriptive crosswalks only, keyed by standards-body id, with at most one entry per body and every id resolving to `contracts/policies/standards-bodies.yaml`.
MULTIPLE bodies are expected where a domain has more than one widely adopted
one — the registry records what each body's terms denote (`practices`,
`processes`, `skills`, `roles`, `controls`, `competencies`,
`clinical_concepts`), because mapping a worker class to a PROCESS is a
different claim than mapping it to a ROLE, and conflating the two is how a
crosswalk silently overstates what a worker is.
A crosswalk SHALL NOT assert conformance, certification, or
endorsement of or by that framework, SHALL NOT confer or imply any
authority, and SHALL NOT replace the class id. Where a class has no honest
counterpart in the framework, the overlay SHALL declare the literal
`no_clean_equivalent` together with a note stating why, rather than forcing
a mapping onto an ill-fitting term.

#### Scenario: an unmapped class must say why, per body

- **WHEN** a worker declares `no_clean_equivalent` for a body without a note
- **THEN** validation fails naming that body
- **AND** the honest no-counterpart declaration is required to state its
  reason, because a forced mapping onto an ill-fitting term is worse than an
  acknowledged absence

#### Scenario: a crosswalk to an unregistered body is rejected

- **WHEN** a crosswalk names a body id that does not resolve to
  `contracts/policies/standards-bodies.yaml`
- **THEN** validation fails naming the unresolved id
- **AND** free-text framework naming cannot drift across domain repos

#### Scenario: a crosswalk makes no conformance claim

- **WHEN** an overlay declares a crosswalk to a named framework
- **THEN** it is recorded as descriptive alignment only
- **AND** it is not treated as conformance with, certification by, or
  endorsement from that framework
