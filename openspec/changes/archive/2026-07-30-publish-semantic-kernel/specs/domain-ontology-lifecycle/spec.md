# domain-ontology-lifecycle — publish-semantic-kernel deltas

## MODIFIED Requirements

### Requirement: Immutable ontology evolution and compatibility
An active ontology package SHALL never be mutated in place. Every accepted
change SHALL produce a new content-addressed package classified as `additive`,
`clarifying`, `breaking`, or `retiring`. Adding or removing a parent of a
published concept, and widening or narrowing a relation's declared domain or
range, SHALL each be breaking. Breaking revisions SHALL include a migration
map, affected-term and consumer report, updated fixtures, and a new
compatibility line; consumers SHALL adopt any revision through an explicit
pin update. Deprecated or retired identifiers SHALL remain historically
resolvable for interpreting artifacts produced under their original pin, while
new classification, mapping, or binding against a retired identifier fails
closed; the owning repository SHALL retain every published version's bytes at
its recorded digest while any pin or historical artifact references it. Two
pins MAY coexist during a migration window provided every artifact records the
exact pin it used. A consumer-impact report SHALL name affected domain-owned
terms and consumer pins only; tenant bindings are tenant-private, and each
tenant SHALL re-validate its own bindings against the new pin at adoption.
Retention SHALL be truthful in both directions: the ACTIVE version's
self-retained snapshot states `published` (a snapshot never asserts the
live version is superseded), the governed release transition flips exactly
that snapshot's lifecycle line to `superseded` when the next version
publishes — every other snapshot byte stays immutable and digest-verified —
and every retained snapshot SHALL be either a referenced superseded version
or the active version's own self-retention; an orphan snapshot fails
validation. The rewrite SHALL carry every declared manifest field
(including `adoption` and `notes`), and every release-evidence reference
(migration map, quality report, consumer-impact report) SHALL resolve
INSIDE the package directory — a path escaping the package fails the
release.

#### Scenario: An additive concept is published
- **WHEN** a reviewed concept adds a non-conflicting specialization and leaves existing valid classifications unchanged
- **THEN** Domain Hermes may publish an additive package while existing consumers retain their prior pin

#### Scenario: A relation meaning changes
- **WHEN** a revision changes a relation's domain, range, hierarchy, or valid interpretation, in either the widening or the narrowing direction
- **THEN** it MUST be classified as breaking and publication MUST fail without migration and consumer-impact evidence

#### Scenario: A published concept gains a parent
- **WHEN** a revision adds or removes a specialization parent of an already published concept
- **THEN** it MUST be classified as breaking with a migration map, because ancestor traversal and valid classification change for existing consumers

#### Scenario: Retention is truthful in both directions
- **WHEN** a consumer reads `retained/<version>/package.yaml`
- **THEN** a superseded version's snapshot declares `superseded` and the active version's own snapshot declares `published` — the repository never simultaneously asserts a live version is history
- **AND** a snapshot claiming the live version is superseded, and a retained directory that is neither referenced nor the active version, each fail validation

#### Scenario: Supersession flips exactly one line
- **WHEN** the next version publishes over a self-retained active snapshot
- **THEN** the governed release transition changes exactly that snapshot's `lifecycle_state` line to `superseded`, and every other snapshot byte remains immutable and digest-verified

#### Scenario: A kernel release keeps its adoption evidence
- **WHEN** the release transition rewrites a manifest that declares `adoption` or `notes`
- **THEN** the rewritten manifest carries them unchanged — the tool never silently drops a ratified field

#### Scenario: Release evidence cannot escape the package
- **WHEN** a release names a migration map, quality report, or consumer-impact path that resolves outside the package directory
- **THEN** the release is refused naming the path

#### Scenario: Runtime rolls back a package
- **WHEN** a newly adopted ontology causes an operational regression
- **THEN** new operations may re-pin the previous compatible package while historical records retain the exact ontology identity under which they were produced
- **AND** work already admitted under the newer pin either completes under the identity recorded on it or is re-materialized against the restored pin, and rollback MUST NOT rewrite a recorded ontology identity or remove the rolled-back package's bytes
