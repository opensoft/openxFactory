# doc-health — spec delta

## MODIFIED Requirements

### Requirement: Tag hygiene enforced by reference
The tag-hygiene check family SHALL enforce the canonical `xspec:` marker
grammar exactly as the `document-lifecycle` capability defines it, by
reference; this capability and its artifacts MUST NOT restate the grammar.
The family covers marker well-formedness, target and change-id resolution IN
BOTH DECLARED TARGET FORMS — the in-tree capability form and the pinned form
`pinned:<pin-id>/<capability>` — candidate fence structure, the code-fence and
inline-code example exclusion, the ban on doc-level candidacy status values,
and supersedes `change=` aging.

A FINDING SHALL NAME THE REMEDY ITS OWN TARGET FORM ADMITS. An unresolved
IN-TREE target is remedied by naming a capability under `openspec/specs/` or an
active change; an unresolved PINNED target is remedied in the pin registry, and
the family MUST NOT emit the in-tree remedy for it. A single fixed remedy string
across both forms is a defect in this family, because for a target whose
capability has left the corpus the in-tree remedy instructs the author to write
something false.

#### Scenario: A marker violates the grammar
- **WHEN** a live `xspec:` marker fails any rule of the grammar as defined by `document-lifecycle`
- **THEN** the run MUST emit a tag-hygiene finding citing the grammar's owning capability, not a locally restated rule

#### Scenario: A pinned target fails to resolve
- **WHEN** a live marker names a pinned target whose pin id the repository carries no record for
- **THEN** the run MUST emit a tag-hygiene finding
- **AND** its remedy text MUST name the pin registry rather than `openspec/specs/` or an active change

#### Scenario: The grammar evolves
- **WHEN** an OpenSpec change modifies the marker grammar in `document-lifecycle`
- **THEN** the tag-hygiene family follows it with no delta to this capability required
