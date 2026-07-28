## ADDED Requirements

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
conflicting against existing candidate identifiers.

#### Scenario: An empty domain repository is scaffolded
- **WHEN** the starter runs against a new repository with valid domain metadata
- **THEN** it creates a draft ontology package, source inventory, candidate and gap report, example fixtures, and Domain Hermes content-manifest declaration

#### Scenario: The starter reruns after domain review
- **WHEN** the repository already contains a domain-owned ontology package
- **THEN** the starter MUST preserve it, report proposed additions or conflicts separately, and MUST NOT overwrite active definitions

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
aggregation floor required by subject and tenant knowledge separation.

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

#### Scenario: An additive concept is published
- **WHEN** a reviewed concept adds a non-conflicting specialization and leaves existing valid classifications unchanged
- **THEN** Domain Hermes may publish an additive package while existing consumers retain their prior pin

#### Scenario: A relation meaning changes
- **WHEN** a revision changes a relation's domain, range, hierarchy, or valid interpretation, in either the widening or the narrowing direction
- **THEN** it MUST be classified as breaking and publication MUST fail without migration and consumer-impact evidence

#### Scenario: A published concept gains a parent
- **WHEN** a revision adds or removes a specialization parent of an already published concept
- **THEN** it MUST be classified as breaking with a migration map, because ancestor traversal and valid classification change for existing consumers

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

#### Scenario: Generated domain remains a scaffold
- **WHEN** the starter has emitted an ontology tree but review, fixtures, source authority, or publication evidence is incomplete
- **THEN** readiness MUST remain `domain_scaffold_required` or an equivalent non-operational state

#### Scenario: Generated domain becomes ontology-ready
- **WHEN** Domain Hermes ratifies the package and all deterministic acceptance checks pass
- **THEN** the DomainxFactory may publish the package and installation consumers may explicitly pin it
