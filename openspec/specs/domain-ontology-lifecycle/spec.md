# domain-ontology-lifecycle Specification

## Purpose

Govern the life of a DomainxFactory's own ontology package under Domain
Hermes stewardship: the answer set and source inventory a new domain
supplies, the idempotent scaffold-and-fill pipeline whose deterministic
stage is byte-reproducible and whose model-assisted stage may only propose
candidates, and the seed, extend, refresh, reconcile, correct, deprecate
and retire modes each domain maps to its own authorities, reviewers and
cadence. It makes publication an accountable steward act rather than an
agent's — carrying a computable quality report, an immutable
content-addressed revision with its compatibility class and migration
evidence, truthful retention of superseded bytes, and per-term lifecycle
and `effective_version` movement the canonical validator enforces. It also
holds the privacy line: subject facts and tenant-local operating detail
stay in their owning layers and reach the ontology only as reviewed,
de-identified candidates, with an aggregation floor over every term-level
signal reported beside them.
## Requirements
### Requirement: New-domain ontology generation inputs
The domain starter SHALL collect or import a machine-readable ontology answer
set before generating a new DomainxFactory ontology. The answer set SHALL
include the factory taxonomy tuple, canonical layer aliases, subject and focal
item kinds, activities and workflows, journey states, outcomes,
interventions, evidence and source-authority families, external
terminologies, domain boundaries, required reviewers, unresolved assumptions,
and answer-quality state.

#### Scenario: A new domain has sufficient inputs
- **WHEN** a new DomainxFactory has approved or explicitly qualified answers and an authorized ontology-source inventory
- **THEN** the starter can generate a traceable draft package and coverage-gap report

#### Scenario: Required semantic inputs are unresolved
- **WHEN** subject kind, domain boundary, source authority, or accountable ontology reviewer is missing
- **THEN** generation MAY create placeholders but MUST keep the package in draft state and mark it not publishable

#### Scenario: A source has redistribution limits
- **WHEN** the ontology-source inventory registers an external terminology with a restrictive license class
- **THEN** generation records the license class and permitted use, and the draft package maps to the source by reference without embedding restricted content

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

### Requirement: Domain Hermes ontology stewardship
Domain Hermes SHALL be accountable for the reusable domain ontology, including
source registration, steward assignments, review councils, candidate
disposition, semantic compatibility decisions, correction, deprecation,
retirement, publication, migration guidance, and adoption evidence. Agents
and Omnigent workers MAY discover, normalize, compare, and recommend ontology
changes but MUST NOT promote or publish them. Every publication record SHALL
name the accountable steward identity that decided it, and a publication or
promotion attributed to a worker or agent identity SHALL fail validation.

#### Scenario: Domain Hermes accepts a candidate
- **WHEN** the assigned stewards complete required source, conflict, fixture, and domain-authority review
- **THEN** Domain Hermes may include the candidate in a new validated package version and records the decision evidence
- **AND** the publication record names the accountable steward identity rather than the agent or worker that prepared the diff

#### Scenario: A high-impact domain requires accountable human review
- **WHEN** domain policy reserves the semantic change for a licensed or otherwise accountable human authority
- **THEN** Domain Hermes MUST block publication until that approval evidence is present

#### Scenario: An automated maintainer finds an apparent correction
- **WHEN** an agent detects that an active definition conflicts with a newer authoritative source
- **THEN** it creates a correction candidate and impact report but the active ontology remains unchanged

### Requirement: Canonical ontology fill and maintenance modes
Every DomainxFactory SHALL map the neutral ontology modes `seed`, `extend`,
`refresh`, `reconcile`, `correct`, `deprecate`, and `retire` to its
authoritative sources, steward groups, reviewer policy, cadence, and expected
outputs. Maintenance SHALL respond to source changes or expiry, unknown terms,
mapping failures, repeated low-confidence classification, semantic conflicts,
workflow drift, new sub-domain profiles, appeals, and reviewed promotion
candidates.

#### Scenario: An authoritative source changes
- **WHEN** a pinned source authority publishes a relevant revision or reaches its review deadline
- **THEN** Domain Hermes opens a refresh or reconcile candidate identifying affected terms, mappings, fixtures, consumers, and urgency

#### Scenario: Runtime repeatedly encounters an unknown term
- **WHEN** governed telemetry reaches the domain-defined threshold for an unmapped or ambiguously mapped term
- **THEN** Domain Hermes receives an extend or reconcile candidate carrying only aggregated term counts that meet the domain's aggregation floor, without subject-private source material or the surrounding text

#### Scenario: No maintenance trigger fires
- **WHEN** scheduled reconciliation finds no source, mapping, fixture, usage, or compatibility drift
- **THEN** it records the completed check and leaves the active package and consumer pins unchanged

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

### Requirement: Subject and tenant knowledge cannot silently become ontology
The system SHALL keep subject facts, raw records, identifiers, private
evidence, and tenant-local operating details in their owning layers, out of
published ontology packages and out of every artifact this capability emits
beside them — candidate registers, conflict, coverage-gap and consumer-impact
reports, generated review fixtures, quality reports, and quality-signal
telemetry. A reusable pattern derived from those layers MAY become a domain
ontology candidate only after applicable consent, de-identification,
provenance, promotion, and Domain Hermes review gates succeed; the candidate
SHALL contain the reusable abstraction and evidence references rather than the
private source payload. A
mapping target SHALL name a system registered in the package's source inventory
as an externally identified system with a license class; tenant system names,
hostnames, endpoints, and local code-system identifiers SHALL NOT appear in a
published package. Term-level quality and unknown-term signals SHALL be
reported as counts over normalized term forms that meet a domain-declared
minimum distinct-subject and distinct-tenant aggregation floor, carrying no
surrounding free text and no subject, tenant, or record identifier; terms below
the floor SHALL appear only inside an aggregate unreportable count, and a
declared floor below two distinct subjects SHALL be a recorded, reviewed
privacy exception rather than a default.

#### Scenario: Subject pattern appears reusable
- **WHEN** Subject Hermes identifies a pattern that may improve reusable domain interpretation
- **THEN** the system creates a promotion candidate and does not add the subject fact or identifier to the domain ontology
- **AND** any generated review fixture derived from that pattern carries only the de-identified abstraction and evidence references, never the source payload

#### Scenario: A rare term would identify a subject
- **WHEN** an unknown-term or quality signal for a rare term falls below the domain's distinct-subject or distinct-tenant aggregation floor, or would carry the free text it was observed in
- **THEN** the signal MUST be withheld from the term-level report and counted only in the aggregate unreportable total

#### Scenario: Tenant mapping is local
- **WHEN** one tenant maps an internal CRM, EHR, ledger, or repository field to a domain concept
- **THEN** the mapping remains a tenant semantic binding unless Domain Hermes separately reviews and publishes a reusable domain mapping

#### Scenario: A tenant system name reaches a published mapping
- **WHEN** a candidate mapping names a tenant-internal system, host, or local code system that is not a registered externally identified source
- **THEN** validation MUST reject the published mapping naming the unregistered system, and the mapping stays a tenant semantic binding

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

