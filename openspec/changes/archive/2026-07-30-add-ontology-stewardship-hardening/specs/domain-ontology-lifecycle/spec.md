# domain-ontology-lifecycle — add-ontology-stewardship-hardening deltas

## MODIFIED Requirements

### Requirement: Reproducible ontology scaffold and fill pipeline
The domain starter SHALL provide an idempotent pipeline that imports the exact
xFactory kernel, creates the conventional Domain Hermes ontology tree, seeds
neutral specializations from intake, ingests approved structured
vocabularies and existing domain artifacts, produces model-assisted
candidates only from approved sources, resolves duplicates and mappings,
records conflicts and gaps, and emits review fixtures and a rerun report.
Structured authoritative imports SHALL take precedence over model-generated
candidates, and reruns SHALL preserve domain-owned active content. The
deterministic stage — kernel import, intake-seeded specializations, and
structured vocabulary imports — SHALL be byte-reproducible from the same answer
set and the same pinned sources. The model-assisted stage SHALL write only to
the candidate register, recording an extraction-run identity per candidate, and
a rerun SHALL NOT delete, replace, or resurrect an existing candidate or its
recorded disposition; new model output SHALL be reported as new, duplicate, or
conflicting against existing candidate identifiers. The starter SHALL provide
an ontology-only adoption mode for existing repositories that writes ONLY the
ontology tree and the content-manifest declaration (candidate ingestion
included) and never emits the whole-repository scaffold — the rerun report
prints to standard output instead of landing in the repository. The starter
provenance marker SHALL be inventoried package content (digest-covered, so
deleting it fails closed) and SHALL structurally record every placeholder
term id and placeholder steward id the run seeded.

#### Scenario: An empty domain repository is scaffolded
- **WHEN** the starter runs against a new repository with valid domain metadata
- **THEN** it creates a draft ontology package, source inventory, candidate and gap report, example fixtures, and Domain Hermes content-manifest declaration

#### Scenario: The starter reruns after domain review
- **WHEN** the repository already contains a domain-owned ontology package
- **THEN** the starter MUST preserve it, report proposed additions or conflicts separately, and MUST NOT overwrite active definitions

#### Scenario: A mature repository adopts the ontology only
- **WHEN** the starter runs in ontology-only mode against an existing repository
- **THEN** it writes only `hermes/domain/ontology/**` and the content-manifest `domain_ontology` declaration, leaves every other repository surface untouched, and prints the rerun report to standard output
- **AND** the manual delete-the-strays step the whole-repository scaffold would otherwise require does not exist

#### Scenario: The provenance marker is deleted
- **WHEN** a generated package's inventoried starter marker is deleted or moved beside the inventory
- **THEN** the canonical validator fails the package (a missing inventoried file breaks the digest; an uninventoried content-kind file is flagged), so a generated domain cannot silently shed its generated status

#### Scenario: Model extraction proposes a term
- **WHEN** an agent extracts a candidate concept or relation from approved source material
- **THEN** the candidate records source references, extraction method, confidence, conflicts, and review state and cannot enter the active package directly

#### Scenario: A rerun proposes different model candidates
- **WHEN** the model-assisted stage runs again over unchanged approved sources and proposes a different candidate set
- **THEN** the deterministic stage's output is byte-identical, the differing proposals are added as new candidates carrying their own extraction-run identity, and previously dispositioned candidates keep their disposition
- **AND** the rerun report names them as new, duplicate, or conflicting rather than reporting a changed scaffold

### Requirement: Measurable ontology quality accountability
Domain Hermes SHALL publish a quality report with every ontology release and
SHALL monitor active-package quality at a domain-declared cadence between
releases. Every signal SHALL be computable and reproducible: it SHALL declare
its numerator, denominator, observation window, and the recorded procedure and
pinned fixture-set identity used to produce it, so the same package, fixture
set, and telemetry window yield the same values. The report SHALL cover at
least intake-scope coverage (declared intake items with at least one mapped
concept, over declared intake items), unknown or unmapped term rate (unmapped
or ambiguously mapped term observations, over term observations in the
window), mapping resolution rate (mapping references resolving to a live
target, over mapping references resolved in the window), classification
fixture accuracy (labeled review-fixture cases whose produced classification
equals the case's recorded expected classification, over all cases in the
pinned fixture set, under the recorded classification procedure), and
open-candidate age. Deterministic validator conformance SHALL remain a
separate pass/fail release gate and SHALL NOT be reported as a quality ratio.
Domain-defined thresholds over these signals SHALL act as maintenance triggers,
and quality signals SHALL be computed from governed telemetry under the
aggregation floor required by subject and tenant knowledge separation. A
required quality signal SHALL declare at least one bound — a floor
(`min_value`) or a ceiling (`max_value`) — so rate signals that must stay
LOW are expressible directly and no required signal is vacuous. When the
policy declares a source-review cadence, every external-kind registered
source SHALL carry a review deadline for that cadence to apply to.

#### Scenario: A release includes its quality baseline
- **WHEN** Domain Hermes publishes a package version
- **THEN** the release records the quality report, its per-signal denominators, window, procedure, and fixture-set identity, and the domain's readiness claim references it as the active quality baseline

#### Scenario: Quality degrades below a domain threshold
- **WHEN** governed telemetry shows the unknown-term rate or mapping failure rate crossing a domain-defined threshold
- **THEN** Domain Hermes opens a reconcile or extend candidate identifying the degraded signal, affected terms, and consumers

#### Scenario: A well-formed package fits the domain poorly
- **WHEN** a package passes all deterministic validation but a required signal is missing or its fixture accuracy or coverage falls below the domain-declared threshold
- **THEN** the quality report records the shortfall and publication and readiness MUST fail on that signal unless the release carries a recorded, reviewed exception naming it
- **AND** a validator pass alone MUST NOT satisfy the quality gate

#### Scenario: A ceiling-bounded signal is declared directly
- **WHEN** the policy requires the unknown-term rate to stay under a domain ceiling
- **THEN** the gate declares `max_value` without a fabricated floor, and a required signal declaring neither bound fails schema validation

#### Scenario: The cadence has no deadline to apply to
- **WHEN** the policy declares `source_review` while an external-kind source registers no `review_by` deadline
- **THEN** the canonical validator fails the package naming the source

### Requirement: Generated-domain ontology acceptance
A newly generated DomainxFactory SHALL NOT claim ontology readiness until its
package validates, imports an exact compatible kernel, declares its Domain
Hermes stewards and sources, passes positive and negative classification
fixtures, contains no unresolved publication blockers, is declared in the
Domain Hermes content manifest, and records a ratification and release pin.
Placeholder detection SHALL be structural: readiness blocks on any
placeholder term or steward the starter marker records as seeded and still
present, and naming heuristics remain defense-in-depth only — renaming a
placeholder SHALL NOT make a scaffold read ready.

#### Scenario: Generated domain remains a scaffold
- **WHEN** the starter has emitted an ontology tree but review, fixtures, source authority, or publication evidence is incomplete
- **THEN** readiness MUST remain `domain_scaffold_required` or an equivalent non-operational state

#### Scenario: A renamed placeholder does not read ready
- **WHEN** a marker-recorded placeholder term is renamed or relabeled without Domain Hermes review resolving it
- **THEN** readiness still blocks on the recorded placeholder until the marker records it resolved or the term is removed by review

#### Scenario: Generated domain becomes ontology-ready
- **WHEN** Domain Hermes ratifies the package and all deterministic acceptance checks pass
- **THEN** the DomainxFactory may publish the package and installation consumers may explicitly pin it

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
A retained snapshot SHALL declare `lifecycle_state: superseded` from its
creation — a snapshot is history from birth and is never mutated afterward —
and a retained manifest claiming an active lifecycle SHALL fail validation.
The governed release transition SHALL rewrite the manifest faithfully,
carrying every declared field of the ratified shape (including `adoption`
and `notes`), and every release-evidence reference (migration map, quality
report, consumer-impact report) SHALL resolve INSIDE the package directory —
a path escaping the package fails the release.

#### Scenario: An additive concept is published
- **WHEN** a reviewed concept adds a non-conflicting specialization and leaves existing valid classifications unchanged
- **THEN** Domain Hermes may publish an additive package while existing consumers retain their prior pin

#### Scenario: A relation meaning changes
- **WHEN** a revision changes a relation's domain, range, hierarchy, or valid interpretation, in either the widening or the narrowing direction
- **THEN** it MUST be classified as breaking and publication MUST fail without migration and consumer-impact evidence

#### Scenario: A published concept gains a parent
- **WHEN** a revision adds or removes a specialization parent of an already published concept
- **THEN** it MUST be classified as breaking with a migration map, because ancestor traversal and valid classification change for existing consumers

#### Scenario: A retained snapshot is honest about being history
- **WHEN** a consumer reads `retained/<version>/package.yaml`
- **THEN** its `lifecycle_state` is `superseded`, distinguishing the snapshot from the active manifest without consulting anything else
- **AND** a retained manifest claiming `published` or `draft` fails validation

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
