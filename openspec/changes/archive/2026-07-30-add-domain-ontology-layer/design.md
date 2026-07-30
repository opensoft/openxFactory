## Context

The current xFactory architecture already contains the pieces of an ontology,
but they are implicit and distributed:

- `docs/xfactory-domain-factory-model.md` defines the neutral Subject, Focal
  Item, Interaction, Journey State, Outcome, and Intervention model.
- `docs/factory-taxonomy-model.md` classifies factory, target-domain, tenant,
  and subject kinds.
- `docs/openxfactory-installation-spine.md` assigns domain ontology ownership
  to a DomainxFactory installation overlay and uses ontology during
  `current_state_inference`.
- `docs/customer-hermes-memory-model.md` separates source claims, evidence
  graphs, state, memory, and promotion candidates.
- The Hermes runtime contracts define neutral topology, authority, jobs,
  artifacts, approvals, and traceability, with semantic validators for
  invariants that JSON Schema cannot express.
- Domain overlay examples already name inputs such as
  `medx_activity_ontology`, but no shared contract defines their shape,
  ownership, generation, publication, or maintenance.

This leaves two operational gaps. First, `scripts/apply-domain-starter.py` can
scaffold a DomainxFactory but cannot produce a reviewable initial ontology from
the domain questionnaire, approved sources, and xFactory core concepts.
Second, an active domain has no standard way to observe semantic drift, propose
changes, decide compatibility, publish a new immutable version, or migrate
runtime pins.

Ontology is meaning, not authority. The design must keep these concerns
separate:

```text
taxonomy       classifies a domain or template
schema         validates record shape
ontology       defines concepts, relationships, and valid specialization
knowledge graph stores scoped instances, claims, and evidence
policy         determines what actors may do
```

The stakeholders are openxFactory contract maintainers, Domain Hermes and its
review councils, DomainxFactory authors, domain-starter tooling, Hermes
Install, the memory gateway, Omnigent workers, and downstream tenant/subject
runtimes.

## Goals / Non-Goals

**Goals:**

- Establish a small, domain-neutral xFactory semantic kernel.
- Define a Git-native, content-addressed ontology package contract.
- Give each new DomainxFactory a reproducible ontology scaffold and fill
  process.
- Make Domain Hermes explicitly accountable for ontology stewardship and
  release decisions.
- Define event-driven and scheduled ontology maintenance without silent
  mutation.
- Bind every emitted semantic classification to an exact ontology package.
- Preserve subject isolation, tenant privacy, evidence provenance, and
  existing authority gates.
- Keep the representation storage-neutral and permit future JSON-LD/RDF
  interchange without requiring it for the first implementation.

**Non-Goals:**

- Build a universal ontology containing clinical, accounting, engineering,
  marketing, or operations truth in openxFactory.
- Select a graph database, vector database, ontology reasoner, or memory
  provider.
- Make ontology inference an authorization, consent, approval, or policy
  mechanism.
- Put tenant-private mappings or subject-instance facts in a published domain
  ontology.
- Automatically promote model-extracted concepts into an active package.
- Replace existing schemas, evidence graphs, taxonomies, source-authority
  rules, or runtime semantic validators.
- Require legacy DomainxFactory consumers to adopt a new ontology pin without
  an explicit compatibility migration.

## Decisions

### 1. Use four semantic strata with explicit owners

```text
xFactory semantic kernel
  owner: openxFactory
  content: neutral concepts, relation primitives, extension rules,
           package/context contracts, validation and release rules

domain ontology package
  owner: Domain Hermes in the DomainxFactory repository
  content: domain concepts, activities, state models, mappings,
           definitions, provenance and review ownership

tenant semantic binding
  owner: Tenant Hermes
  content: local system codes, field mappings, aliases and operating terms

subject knowledge graph
  owner: Subject Hermes
  content: isolated instances, claims, evidence, state and history
```

Domain Hermes owns the reusable meaning of a domain. Tenant Hermes may bind
local terminology to that meaning but cannot redefine the published domain
ontology. Subject Hermes instantiates the ontology but does not publish private
facts as domain concepts.

**Alternative considered:** one combined global/domain/tenant/subject graph.
Rejected because ownership, privacy, update cadence, and authority differ at
every layer.

### 2. Treat Domain Hermes as accountable steward, not sole author

Domain Hermes owns:

- authoritative source registration and review cadence;
- ontology review councils and steward assignments;
- acceptance or rejection of proposed concepts, relations, mappings, and
  corrections;
- semantic compatibility classification;
- package promotion, supersession, deprecation, and retirement;
- migration guidance and consumer adoption evidence.

Domain Hermes may use Omnigent workers, reference agents, and deterministic
importers to discover, extract, normalize, compare, and test candidates.
Their output is advisory, and "advisory" is enforced rather than asserted:
every publication record names the accountable steward identity that decided
it, and a publication or promotion attributed to a worker or agent identity
fails validation. A domain policy may additionally require a licensed
or otherwise accountable human authority before a high-impact semantic change
is accepted.

**Alternative considered:** allow the generator or maintenance agent to
publish low-risk additions. Rejected because even apparently additive terms
can change routing, retrieval, state inference, and downstream interpretation.

### 3. Use YAML-serialized JSON contracts as the canonical first format

The first contract family lives under `contracts/domain-ontology/` and uses
the repository's established YAML/JSON Schema, semantic-validator, fixture,
release-manifest, and digest-pinning patterns. Runtime consumers may compile a
package into maps, relational tables, property graphs, JSON-LD, RDF, or search
indexes, but the compiled representation is derivative and identifies its
source package digest.

The package family contains at least:

- an ontology package manifest;
- a concept registry;
- a relation registry;
- external and tenant-mapping contracts;
- source and steward references;
- an ontology candidate/change record;
- an ontology release/adoption record;
- a bounded semantic-context artifact;
- positive and negative conformance fixtures.

**Alternative considered:** make OWL/RDF and a triple store the operational
authority. Rejected for the first release because open-world inference and
provider-specific behavior conflict with xFactory's deterministic,
content-addressed, fail-closed control plane. A lossless JSON-LD/RDF export can
be added after interoperability requirements are concrete.

### 4. Stable semantic identity is separate from labels

Core terms use an xFactory-owned namespace. Domain terms use a domain-owned
sub-namespace under the neutral identifier grammar. Identifiers are immutable
and labels, aliases, descriptions, and external code mappings may evolve
without changing identity.

Each term records:

- stable ID and semantic kind;
- owning namespace and steward;
- definition and lifecycle state;
- exact parent/specialization references;
- source-authority and provenance references;
- effective version;
- supersession/deprecation references when applicable.

Relations additionally declare exact domain and range concept references and
any supported deterministic characteristics. Arbitrary executable rules,
credential scopes, grants, and policy effects are forbidden from ontology
authority.

Specialization is a directed acyclic graph. A term may declare more than one
parent, each an exact reference, because domain hierarchies (clinical ones
especially) are legitimately polyhierarchical; the cost of that choice is paid
in the compatibility rubric (Decision 8) and in bounded-context closure
(Decision 9), not in a single-parent restriction. Preferred labels and aliases
are unique within a package namespace: a collision is a validation error, not a
compatibility class, because an ambiguous label makes classification
non-deterministic.

**Alternative considered:** use display names or source-system codes as stable
identity. Rejected because labels and external systems change independently of
domain meaning.

### 5. Keep the xFactory semantic kernel small

The initial kernel is an upper model over existing neutral contracts:

```text
party/layer:  subject, tenant, domain
work:         workflow, activity, state, transition, gate, artifact
subject view: focal item, interaction, journey state, outcome, intervention
knowledge:    source, claim, evidence, hypothesis, observation, knowledge atom
governance:   policy, consent, authority, approval, trace reference
```

The kernel points to the contracts that own record shape and behavior. It does
not restate runtime lifecycle, authority, approval, or isolation invariants.
A DomainxFactory specializes these neutral terms; it cannot redefine or
shadow them.

Scope creep is held off procedurally and mechanically. Every kernel term names
its owning contract and records cross-factory adoption evidence: at least two
independent adopters, each an exact DomainxFactory package identity or
shared-subsystem contract identity that specializes or references the term.
The validator counts and resolves those references at kernel publication — a
draft term may carry pending adoption, so the initial kernel can be assembled
before any domain package exists, but nothing publishes on promised future
adoption; the two contrasting pilot packages are what first make the core
terms publishable. openxFactory owns kernel revision classification; a
DomainxFactory can request a kernel term but never classify a kernel change.

**Alternative considered:** migrate every existing enum and schema definition
into the ontology. Rejected because it would create a competing source of
truth and an unbounded initial migration.

### 6. Extend the domain starter with an ontology generation pipeline

`scripts/apply-domain-starter.py` remains an idempotent scaffolder. For a new
domain, it creates a conventional `hermes/domain/ontology/` package in draft
state and declares it in `hermes/domain/content-manifest.yaml`. It never
overwrites a domain-owned active package.

Generation consumes a machine-readable answer set derived from the existing
pre-run questionnaire plus an ontology-source inventory:

- factory type/subtype and target domain/subtype;
- Subject, Tenant, and Domain aliases;
- subject kinds and focal-item kinds;
- primary activities, workflows, states, outcomes, and interventions;
- evidence types, source authorities, external terminologies, and local code
  systems;
- domain boundaries, prohibited interpretations, and required reviewers;
- closest and worst domain analogies;
- unresolved assumptions and readiness level.

The fill pipeline is:

```text
intake and taxonomy binding
  -> import exact xFactory kernel
  -> deterministic scaffold from neutral concepts
  -> ingest approved structured vocabularies and existing domain artifacts
  -> model-assisted candidate extraction from approved source material
  -> entity resolution, deduplication and kernel mapping
  -> conflict, ambiguity, source and coverage-gap reports
  -> generated positive/negative/example classification fixtures
  -> Domain Hermes review and required human/domain-authority approval
  -> deterministic validation
  -> immutable package publication
  -> explicit installation/runtime pin
```

Structured, authoritative imports take precedence over model extraction. Every
generated term remains a candidate until reviewed. The generator extends the
starter's existing rerun report with conflicting and unresolved categories
alongside its created, updated, and skipped outputs.

The determinism boundary is drawn between the two halves of that pipeline and
is what makes the idempotency claim honest. The deterministic stage — kernel
import, intake-seeded specializations, structured vocabulary imports — is
byte-reproducible from the same answer set and the same pinned sources. The
model-assisted stage is not reproducible and therefore writes only to the
candidate register, one extraction-run identity per candidate. A rerun that
proposes different candidates leaves the scaffold byte-identical, adds the new
proposals, and reports them as new, duplicate, or conflicting against existing
candidate identifiers; it never deletes, replaces, or resurrects a candidate
whose disposition Domain Hermes already recorded.

**Alternative considered:** start with a blank ontology file. Rejected because
it does not make domain generation repeatable and pushes the same discovery
work into every DomainxFactory.

### 7. Define canonical fill and maintenance modes

Every DomainxFactory supports these neutral modes and maps them to its own
sources, stewards, reviewers, and cadence:

```text
seed        establish the first reviewed package for a new domain
extend      add a new concept, relation, mapping, profile, or sub-domain
refresh     re-evaluate terms whose authoritative sources changed or expired
reconcile   compare sources, runtime usage, mappings, and active definitions
correct     supersede an inaccurate definition or mapping with evidence
deprecate   stop recommending new use while preserving interpretation
retire      prohibit new use while retaining historical resolvability
```

Maintenance triggers include authoritative-source change, source expiry,
unknown-term frequency, mapping failure, repeated low-confidence
classification, conflicting interpretations, workflow drift, new sub-domain
profiles, appeals/corrections, and reviewed de-identified promotion
candidates.

Domain Hermes operates a candidate queue and scheduled reconciliation. It may
monitor continuously, but it publishes only through a governed review and
release transition.

### 8. Make ontology change append-only and compatibility-classified

An active package is immutable. A change creates a new candidate and then a new
package version. Existing terms remain resolvable with their original package
identity.

Changes are classified:

- `additive`: new non-conflicting terms or mappings;
- `clarifying`: definition/provenance improvement that does not change valid
  classification;
- `breaking`: identity reuse, changed meaning, hierarchy change, a relation
  domain/range change in either direction, incompatible mapping, or removal;
- `retiring`: deprecation or retirement with a replacement or rationale.

Edge cases are classified rather than left to reviewer taste:

```text
add or remove a parent of a published concept   breaking
widen a relation's domain or range              breaking
narrow a relation's domain or range             breaking
add a non-colliding alias or synonym            clarifying
alias or label colliding in the namespace       invalid (not a class)
refresh an external mapping to a new source ver mapping revision, classified
                                                by its effect on classification
```

Adding a parent is breaking even though nothing existing becomes invalid,
because ancestor traversal and the set of valid classifications both change
for an already-pinned consumer; `clarifying` is reserved for changes that
provably leave valid classification untouched.

Breaking changes require a migration map, new compatibility line, affected
fixture updates, consumer impact report, and explicit re-pin. The
consumer-impact report names domain-owned terms and consumer pins only —
tenant bindings are tenant-private, so each tenant re-validates its own
bindings against the new pin at adoption rather than being enumerated in a
published report.

Published tags or digests are never moved, and the owning repository retains
every published version's bytes at its recorded digest while any pin or
historical artifact still references it; retirement forbids new use, it does
not delete content. Two pins may coexist during a migration window as long as
every artifact records the exact pin it used. Rollback changes the active
runtime pin for new operations; work already admitted under the newer pin
either completes under the identity recorded on it or is re-materialized
against the restored pin, and historical records retain the ontology identity
under which they were produced.

The xFactory kernel is itself a package and follows the same rubric. A
breaking kernel revision starts a new kernel compatibility line; existing
domain packages remain valid under their pinned kernel import and adopt the
new line only through their own reviewed revision with migration evidence.
Kernel changes therefore cascade explicitly, never implicitly.

**Alternative considered:** update the active package in place and rebuild
indexes. Rejected because historical semantic interpretation would become
non-reproducible.

### 9. Bind semantic context to exact package identity

Runtime work does not receive an unrestricted ontology corpus by default.
xFactory compiles a purpose-bounded semantic-context artifact from:

- the exact xFactory kernel pin;
- the exact DomainxFactory ontology package pin;
- an approved tenant binding, when relevant;
- the requested workflow/purpose and required concept subset;
- source, freshness, redaction, and lifecycle metadata.

A term subset is closed, or explicitly truncated. "Only the required terms" is
not well defined on its own: classifying against a concept requires its
specialization ancestors up to the kernel, and using a relation requires the
concepts its domain and range name. Compilation therefore closes the requested
subset over those members, or records an itemized truncation naming each
omitted member so the consumer knows its classifications are partial; a subset
that is neither closed nor explicitly truncated fails compilation.

A tenant binding included in a context declares the exact domain package
identity it binds against, and every bound target identifier must resolve in
that package. A binding pinned to a different package than the context, or
naming an identifier the pinned package retired or never had, fails closed —
which is also how a tenant discovers, at adoption rather than at runtime, that
a supersession invalidated one of its local mappings.

Claims, state hypotheses, workflow maps, jobs, and derived artifacts that use
domain semantic types record the semantic-context or package ID and digest.
Memory gateway customer and expert context packets carry this identity when
semantic context is present.

### 10. Semantic inference never crosses the authority plane

Ontology may support classification, normalization, retrieval, entity
resolution, current-state hypotheses, and suggested routing. It cannot:

- grant or widen authority;
- establish consent or approval;
- create a cross-layer binding;
- bypass memory gateway rails;
- convert a hypothesis into authoritative state;
- promote tenant or subject data;
- authorize an external action.

Every such action continues through the existing policy, evidence, consent,
grant, approval, promotion, and trace contracts.

The validator enforces that structurally rather than by judging prose, because
"claims an authorization effect" is not machine-checkable from a label. Two
mechanical rules do the work: ontology records use a closed field vocabulary
with no effect, permission, grant, credential, scope, routing-decision, or
executable-rule field (unknown fields are rejected, so an effect cannot be
attached); and no ontology term may name an authority-plane record — a grant,
credential, consent record, approval decision, cross-layer binding, provider
binding, or route — as a relation endpoint, mapping target, or attribute
value. A concept labelled `auto_approved` is then merely a badly named
concept, not a bypass, and the consumer-side rule above still applies.

### 11. External terminologies are referenced, never mirrored

Domain packages map concepts to external code systems — clinical
terminologies, charts of accounts, vulnerability registries, ad taxonomies,
local coding schemes — by stable reference: system identifier, system
version, code, and a recorded license class. A package must not embed a
mirrored external code system, and definitions quoted from licensed sources
appear only within the permitted use recorded in the source inventory.
Refreshing an external source is a mapping revision, not a package rewrite.

This keeps packages reviewable at Domain Hermes scale (a package holds the
domain's own concepts and mappings, not hundreds of thousands of imported
terms), avoids redistribution violations — decisive for clinical
terminologies whose licenses prohibit republication — and keeps
external-source churn from destabilizing package identity.

**Alternative considered:** import approved terminologies wholesale into the
package. Rejected because such packages are unreviewable, licensing commonly
forbids redistribution, and every upstream release would force a full package
revision.

### 12. Every Hermes layer consumes ontology; Domain Hermes answers for quality

```text
Subject Hermes    interprets claims, journey state, and history against the
                  pinned domain package; never edits it
Tenant Hermes     binds local system codes and operating terms to published
                  domain concepts; binding validity depends on package quality
Domain Hermes     stewards the package and answers for its fitness
xFactory layer    routes, gates, compiles context, and audits via exact pins
Omnigent workers  receive bounded, worker-scoped semantic context
```

Because every layer's interpretation quality depends on the domain package,
Domain Hermes owns measurable quality, not only process. Each release
publishes a quality report, and each signal declares numerator, denominator,
observation window, and the procedure and pinned fixture-set identity that
produced it, so the same package, fixture set, and window recompute the same
values:

```text
intake-scope coverage   declared intake items with >=1 mapped concept
                        / declared intake items
unknown-term rate       unmapped or ambiguously mapped term observations
                        / term observations in the window
mapping resolution rate mapping references resolving to a live target
                        / mapping references resolved in the window
fixture accuracy        labeled fixture cases whose produced classification
                        equals the recorded expected classification
                        / cases in the pinned fixture set, under the recorded
                        classification procedure
open-candidate age      age distribution of undispositioned candidates
```

Fixture accuracy is deliberately not the validator's result. Deterministic
validator conformance is pass/fail and stays a separate release gate;
accuracy measures how the domain's actual classification procedure performs
against a labeled review set, which is the only signal that can catch a
well-formed package that fits the domain poorly. Domain-defined thresholds
over these signals are maintenance triggers in their own right, publication
fails on a missing or below-threshold required signal unless the release
carries a recorded reviewed exception, a readiness claim references the active
quality baseline, and signals are computed from governed telemetry under the
aggregation floor in Decision 14 rather than from subject-private material.

**Alternative considered:** treat quality as implicit in review process and
validator passes. Rejected because process compliance cannot detect a
well-formed package that fits the domain poorly; fitness must be observed
from governed usage.

### 13. Semantic context is the Omnigent consumption seam

The bounded semantic-context artifact (Decision 9) is how the Omnigent
layer consumes ontology. A semantic-context profile can be declared per
neutral worker archetype (`frame`, `generate`, `verify`, `challenge`,
`assemble_for_admission`) or per domain worker class, naming the purpose and
required term subset; compilation then yields a small digest-pinned artifact
per worker rather than one corpus per run. Small bounded workers plus narrow
semantic context is the intended structural advantage: a `verify` worker
sees the classification terms it checks, not the full generation vocabulary,
which shrinks its prompt surface, sharpens its judgments, and limits what a
compromised or drifting worker can misinterpret.

The worker permission matrix is untouched: semantic context never widens any
permission boolean, and `execute_final_action`/`access_secrets` remain
constitutionally false. The profile is a neutral artifact in this change's
own contract family, so compilation is exercisable by fixture here — a
profile plus a pinned package compiles to a closed, digest-pinned subset —
without any omnigent schema change. Which surface declares a profile for a
live worker (the omnigent domain overlay is the leading answer) and the worker
runtime wiring belong to the follow-up omnigent change.

### 14. Reusable learning enters only through reviewed promotion

Subject facts remain in Subject Hermes and tenant-local mappings remain in
Tenant Hermes. A reusable pattern discovered from operation may become an
ontology candidate only after the existing consent, de-identification,
provenance, and promotion gates succeed. The candidate contains the reviewed
reusable abstraction and evidence references, not raw subject or
tenant-private records.

The published package is not the only leak surface, so the same rule covers
every artifact this capability emits beside it: candidate registers, conflict,
coverage-gap and consumer-impact reports, generated review fixtures, quality
reports, and quality-signal telemetry. Three vectors are closed explicitly.
A rare term plus its surrounding context can identify one subject, so
term-level signals report normalized term forms as counts only, carry no free
text and no subject, tenant, or record identifier, and appear only at or above
a domain-declared minimum distinct-subject and distinct-tenant aggregation
floor; terms below the floor land in an aggregate unreportable count. Tenant
system names, hosts, endpoints, and local code systems cannot reach a
published mapping, because a mapping target must name a system registered in
the source inventory as an externally identified system with a license class.
Generated review fixtures derived from real material carry the de-identified
abstraction and evidence references, never the source payload.

### 15. Conformance is deterministic and release-gated

The canonical validator checks schema structure plus:

- package inventory, foreign-kind exclusion, and digest closure;
- retention of superseded versions still referenced by a pin or artifact;
- namespace ownership, stable-ID uniqueness, and label/alias uniqueness;
- exact kernel imports and kernel adoption evidence;
- missing or circular specialization;
- relation domain/range validity;
- source/steward completeness;
- lifecycle and supersession validity;
- compatibility classification and migration-map requirements;
- undeclared external mappings and unregistered mapping targets;
- prohibited subject/tenant-instance material in packages, candidates,
  reports, fixtures, and quality signals;
- semantic-context/package agreement, subset closure or recorded truncation,
  and tenant-binding resolution;
- closed field vocabulary and forbidden authority-plane references;
- content-manifest and installation-overlay pin agreement.

Fixtures include at least two distinct domain specializations of the same
kernel, a generated new-domain package, additive and breaking revisions
(including a parent addition and a relation domain widening),
unknown/misaligned terms, digest drift, an alias collision, a foreign document
inventoried as ontology content, forbidden private-instance content, a
below-floor term signal, an unclosed context subset, and an attempted
semantic-authority bypass.

## Risks / Trade-offs

- **The kernel becomes a universal domain model** → Keep it limited to neutral
  cross-factory anchors and require every new core term to record two
  independent resolvable adopters (Decision 5), which the validator counts.
- **Ontology duplicates schemas or policy** → Require each core term to name
  the owning contract and forbid authorization effects in ontology packages.
- **Generated content looks authoritative** → Emit draft candidates with
  provenance, confidence, conflicts, and explicit Domain Hermes review state.
- **Domain Hermes becomes a bottleneck** → Permit delegated steward groups,
  scheduled review councils, and automated diff/fixture generation while
  retaining accountable promotion.
- **Semantic changes break historical interpretation** → Use immutable package
  pins, compatibility classes, migration maps, and per-artifact ontology refs.
- **Private data leaks into domain truth** → Validate package content, require
  promotion evidence, and keep subject/tenant instance stores separate.
- **RDF/graph interoperability is delayed** → Preserve stable IDs and explicit
  relations so export can be added without changing canonical meaning.
- **Existing domains lack an ontology** → Use additive migration: scaffold a
  draft beside current content, review it, then explicitly adopt the new
  content kind and runtime pin.

## Migration Plan

1. Ratify the semantic-kernel and ontology-lifecycle requirements.
2. Inventory existing neutral terms and record their authoritative contract
   owners without changing released schemas.
3. Add the ontology schemas, core package, validator, fixtures, and versioned
   contract registration.
4. Extend the pre-run questionnaire and domain starter to generate a draft
   ontology source inventory, package, candidate report, fixtures, and content
   manifest declaration.
5. Extend the Hermes domain content manifest with the additive
   `domain_ontology` content kind and validate generated-domain completeness.
6. Pilot generation against at least two structurally different domains and
   reconcile their shared concepts into the minimal kernel.
7. Add semantic-context compilation and memory-gateway metadata with
   fail-closed pin and authority-plane tests.
8. Provide an explicit migration command/report for existing DomainxFactory
   repositories; never overwrite a domain-owned ontology.
9. Publish the exact reviewed contract bundle and have consumers re-pin
   explicitly.

Rollback keeps the previous contract and ontology pins active for new work.
Published ontology packages remain immutable and historical artifacts retain
their original semantic identity. A failed generator or migration leaves the
existing domain content manifest and active ontology untouched.

## Open Questions

- Whether JSON-LD export belongs in the first release or in an interoperability
  follow-up; it is not required for canonical operation.
- Which two domain pilots provide the best semantic contrast for kernel
  minimization. MedxFactory and codexFactory are the leading pair because
  their subject, focal-item, workflow, and authority vocabularies differ
  substantially.
- Whether tenant semantic bindings should publish through the memory gateway
  first or through a later dedicated tenant-configuration contract. The core
  design requires their separation and pinning but does not require a storage
  choice.
- How a shared-but-not-neutral concept needed by two domains (billing
  concepts in medical and accounting factories, incident concepts in
  operations and engineering) is handled: promotion into the kernel, a
  governed cross-domain import contract, or deliberate duplication with
  cross-domain mappings. The first release permits no cross-domain imports;
  the pilots should record where this pressure actually appears.
- Which surface declares a live worker's semantic-context profile: the domain
  ontology package or the omnigent domain overlay. The profile artifact and
  its compilation are defined here either way (Decision 13). Leading answer:
  the overlay declares worker-class profiles and the ontology validator proves
  the referenced term subsets exist — decided in the follow-up omnigent
  change that wires worker runtimes.
