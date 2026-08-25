# domain-ontology-lifecycle — add-ontology-term-lifecycle-enforcement deltas

## ADDED Requirements

### Requirement: Term-level lifecycle and version enforcement
Term-level `lifecycle_state` and `effective_version` declarations SHALL be enforced by the canonical validator and the governed release transition, never decorative.
A package whose `lifecycle_state` is `published` or `deprecated` SHALL NOT
contain a `draft` term: publication is a per-term steward decision made
before release, and the release transition SHALL refuse to publish a
package while any term remains `draft` rather than silently promoting it.
Across consecutive package versions (whenever the previous version's
retained bytes are resolvable) a term's lifecycle SHALL only move forward
along `draft → published → deprecated → retired` — skipping states is
permitted, moving backward is a validation failure, and resurrecting a
retired identifier remains forbidden (identity reuse is a breaking change
under a NEW identifier). A revision that changes a term's meaning-bearing
content — label, aliases, definition, or parents for a concept; label,
definition, domain, range, characteristics, or parents for a relation —
SHALL bump that term's `effective_version`, and an `effective_version`
SHALL never move backward. These rules apply to every compatibility
class, including breaking and retiring revisions. A `draft` package
remains the workshop: it MAY hold terms in any lifecycle state.

#### Scenario: A published package carries a draft term
- **WHEN** a package whose `lifecycle_state` is `published` or `deprecated` contains a concept or relation whose `lifecycle_state` is `draft`
- **THEN** the canonical validator fails the package
- **AND** the release tool refuses the publication naming each draft term, so Domain Hermes marks every term published (or removes or retires it) before release

#### Scenario: A retired term is resurrected
- **WHEN** a revision changes a term's `lifecycle_state` backward relative to the retained previous version — including `retired` back to `published` or `published` back to `draft`
- **THEN** validation fails naming the term and both states, regardless of the revision's declared compatibility class

#### Scenario: A term's meaning changes without a version bump
- **WHEN** a revision changes a term's meaning-bearing content while `effective_version` stays equal to the retained previous version's, or moves `effective_version` backward
- **THEN** validation fails naming the term, so consumers can rely on `effective_version` movement as the per-term change signal
