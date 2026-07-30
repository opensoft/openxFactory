## ADDED Requirements

### Requirement: Neutral semantic kernel ownership
openxFactory SHALL define a domain-neutral semantic kernel that identifies
shared cross-factory concepts and relation primitives while leaving
domain-specific meaning to the owning DomainxFactory. The kernel SHALL
distinguish ontology from taxonomy, record schema, policy, evidence, and
instance knowledge, and it SHALL reference rather than redefine the contracts
that own runtime shape, authority, consent, approval, isolation, and
traceability. Every kernel term SHALL name the contract that owns its runtime
shape. A published kernel term SHALL record cross-factory adoption evidence —
at least two independent resolvable adopters, each an exact DomainxFactory
package identity or shared-subsystem contract identity that specializes or
references the term; a draft kernel term MAY record pending adoption instead,
and kernel publication SHALL fail for any term still lacking its adopters.
openxFactory SHALL own kernel revision classification; no DomainxFactory
classifies a kernel change.

#### Scenario: A domain specializes a neutral concept
- **WHEN** MedxFactory declares Patient as a specialization of the neutral Subject concept and Treatment as a specialization of Focal Item
- **THEN** the domain package validates without adding either domain term to the xFactory kernel

#### Scenario: The kernel attempts to own a domain term
- **WHEN** a kernel term reaches publication with fewer than two independent resolvable adopters, or names a clinical, accounting, marketing, operations, or engineering meaning with no cross-factory neutral role
- **THEN** kernel publication MUST reject the term with a stable finding
- **AND** review MUST move the term to the owning DomainxFactory rather than admit it under a promise of future adoption

#### Scenario: The initial kernel is drafted before any domain package exists
- **WHEN** the core kernel is assembled from the semantic inventory before any DomainxFactory ontology package exists
- **THEN** draft kernel terms MAY record pending adoption in place of resolved adopters
- **AND** the kernel package MUST NOT publish until every term's adopters resolve, such as through the two contrasting pilot packages

### Requirement: Content-addressed ontology package contract
The semantic kernel SHALL define a provider-neutral ontology package contract
covering a manifest, stable concept and relation identifiers, exact imports,
namespace owner, definitions, lifecycle state, source and steward references,
external mappings, compatibility class, file inventory, and raw-content
digests. An active or published package SHALL be immutable, and every compiled
representation SHALL identify the exact source package and digest. Every
inventoried file SHALL be an ontology-family document; a package inventorying a
document of another contract family SHALL fail validation. A published version
SHALL remain retrievable byte-identically at its recorded digest from its
owning repository while any pin, historical artifact, or superseding package
references it; supersession, deprecation, and retirement change lifecycle state
without removing package bytes.

#### Scenario: A package is published
- **WHEN** Domain Hermes promotes a validated draft ontology package
- **THEN** the published package records an exact kernel import, byte-complete inventory, unique stable identifiers, steward and source references, compatibility class, and content digests

#### Scenario: Published package bytes drift
- **WHEN** a package file differs from the file inventory or recorded digest
- **THEN** validation and runtime loading MUST fail closed

#### Scenario: A package inventories foreign content
- **WHEN** an ontology directory declared as `domain_ontology` content inventories an overlay, policy, credential, approval, or other non-ontology document
- **THEN** validation MUST reject the package naming the foreign kind, and no consumer seeds that document as ontology content

#### Scenario: A superseded package is still referenced
- **WHEN** a newer version supersedes an earlier package that historical artifacts or an active pin still reference
- **THEN** the earlier version stays retrievable at its recorded digest and resolves to the same concepts, relations, and definitions
- **AND** deleting or rewriting it MUST fail validation as a retention violation

#### Scenario: The kernel publishes a breaking revision
- **WHEN** the xFactory kernel package starts a new compatibility line
- **THEN** existing domain packages remain valid under their pinned kernel import
- **AND** openxFactory records the kernel compatibility classification, which no DomainxFactory may restate or relax
- **AND** a domain package adopts the new kernel line only through its own reviewed revision with migration evidence

### Requirement: External terminology mappings are by-reference
Ontology packages SHALL map concepts to external terminologies and code
systems by stable reference — system identifier, system version, code, and a
recorded license class — and SHALL NOT embed a mirrored external code system
or licensed source content beyond the permitted use recorded in the source
inventory. A refresh of an external source SHALL be expressible as a mapping
revision without rewriting unrelated package content.

#### Scenario: A concept maps to an external clinical code
- **WHEN** a medical domain concept declares a mapping to an external terminology entry by system, version, and code with a recorded license class
- **THEN** the package validates and the mapping resolves without the package containing the external system's content

#### Scenario: A package embeds a licensed code system
- **WHEN** a package inventory contains a mirrored external terminology or licensed source content beyond the recorded permitted use
- **THEN** validation MUST reject the package with a stable finding

### Requirement: Stable specialization and relation semantics
Ontology identity SHALL be independent of display labels and external source
codes. A domain term SHALL specialize an existing neutral or domain-owned term
through an exact reference; relation definitions SHALL name valid domain and
range concepts; and missing parents, namespace collisions, invalid
specialization cycles, identity reuse, and undeclared mappings SHALL fail
validation. Specialization SHALL form a directed acyclic graph in which every
declared parent is an exact reference; a term MAY declare more than one parent.
Adding or removing a parent of a published term, and widening or narrowing a
relation's declared domain or range, SHALL each be breaking. Preferred labels
and aliases SHALL be unique within a package namespace, and a label or alias
colliding with another term's label or alias SHALL fail validation rather than
resolve to either term.

#### Scenario: A display label changes compatibly
- **WHEN** Domain Hermes adds a synonym or changes a display label without changing the stable identifier, definition, valid classifications, or relations
- **THEN** the change MAY be classified as clarifying and historical references remain valid
- **AND** the new label or alias MUST NOT equal any other term's label or alias in the namespace

#### Scenario: An alias collides with another term's label
- **WHEN** a revision adds an alias equal to another term's preferred label or alias in the same namespace
- **THEN** validation MUST reject the revision naming both identifiers

#### Scenario: A stable identifier is reused
- **WHEN** a revision assigns an existing concept identifier a different meaning or incompatible parent
- **THEN** validation MUST classify the revision as breaking and require a new identifier plus migration mapping

### Requirement: Deterministic semantic conformance
openxFactory SHALL provide a canonical semantic validator and indexed positive
and negative fixtures. Validation SHALL cover structural schema conformance,
package and import closure, namespace ownership, identifier uniqueness,
specialization, relation domain/range, lifecycle and supersession,
provenance/stewardship, compatibility and migration evidence, overlay pin
agreement, private-instance exclusion, and semantic-authority separation.
Semantic-authority separation SHALL be checked structurally, not by reading
label or definition prose: ontology records SHALL use a closed field vocabulary
containing no effect, permission, grant, credential, scope, routing-decision,
or executable-rule field, and SHALL NOT name an authority-plane record — a
grant, credential, consent record, approval decision, cross-layer binding,
provider binding, or route — as a relation endpoint, mapping target, or
attribute value. Validation SHALL reject unknown fields and such references
with stable findings, and repeated validation of the same bytes SHALL produce
identical findings.

#### Scenario: Two unlike domains use the same kernel
- **WHEN** the fixture suite validates one medical specialization and one software-engineering specialization
- **THEN** both MUST resolve their domain terms through the same neutral kernel without importing the other domain's vocabulary

#### Scenario: Package claims an authorization effect
- **WHEN** an ontology relation or mapping carries a field outside the closed vocabulary, or names a grant, credential, consent record, approval decision, cross-layer binding, provider binding, or route as an endpoint, mapping target, or attribute value
- **THEN** semantic validation MUST reject it with a stable finding, without depending on how the term is labelled or described

### Requirement: Bounded semantic context
xFactory SHALL materialize purpose-bounded semantic-context artifacts rather
than exposing an unrestricted ontology corpus to every workflow or worker. A
semantic context SHALL identify the exact kernel and domain package pins, any
approved tenant binding, the requested purpose and term subset, lifecycle and
freshness metadata, and its own content digest. A term subset SHALL be closed:
it SHALL contain the specialization ancestors of every included concept up to
the kernel and the domain and range concepts of every included relation, or
record an explicit itemized truncation naming each omitted closure member, so
consumers can treat the artifact's classifications as partial. Compilation
SHALL fail when a subset is neither closed nor explicitly truncated. An
included tenant binding SHALL declare the exact domain package identity it
binds against, every bound target identifier SHALL resolve in that package, and
a binding whose declared package identity differs from the context's package
pin SHALL fail closed.

#### Scenario: Workflow receives semantic context
- **WHEN** an approved workflow needs domain classification or entity-resolution context
- **THEN** xFactory supplies a bounded artifact containing only the required terms and exact package identities

#### Scenario: A requested subset is not closed
- **WHEN** a requested or profiled term subset omits a specialization ancestor of an included concept or a domain or range concept of an included relation
- **THEN** compilation MUST close the subset over those members or emit an explicit truncation record naming each omitted member, and MUST fail when it can do neither

#### Scenario: A tenant binding references a retired term
- **WHEN** an approved tenant binding maps a local code to a domain identifier the pinned package has retired or does not contain
- **THEN** compilation MUST fail closed naming the unresolved identifier, and the tenant MUST update the binding before adopting that pin

#### Scenario: Context is used under another package
- **WHEN** a semantic context is presented with a job, claim, or output whose ontology package identity differs from the context
- **THEN** the consumer MUST reject the mismatch and require a newly materialized context

#### Scenario: A bounded worker receives worker-scoped context
- **WHEN** an Omnigent worker class with a declared semantic-context profile performs an approved job
- **THEN** the compiled artifact contains only that profile's term subset with exact kernel and package identities
- **AND** the worker's permission matrix and authority boundaries are unchanged by the presence of semantic context

### Requirement: Semantic inference cannot authorize
The semantic plane SHALL keep classification, equivalence, specialization,
graph traversal, and inference descriptive or advisory only. No semantic
result SHALL create or widen authority, establish consent or approval, create
a cross-layer binding, bypass memory rails, promote scoped data, convert a
hypothesis into authoritative state, or authorize an external action.

#### Scenario: Inferred relation suggests access
- **WHEN** an ontology inference says that one concept is related to a resource in another layer
- **THEN** the operation remains blocked unless the existing exact grants, bindings, consent, policy, and approval gates independently authorize it

#### Scenario: Classification produces a state hypothesis
- **WHEN** source claims classify into a candidate journey state
- **THEN** the result remains an evidence-linked hypothesis until the owning state and review contracts accept it

### Requirement: Storage and reasoner neutrality
The canonical ontology contract SHALL NOT require a graph database, vector
database, RDF store, OWL reasoner, memory provider, or specific query engine.
Any JSON-LD, RDF, property-graph, relational, vector, or in-memory projection
SHALL be derivative, reproducible from a pinned package, and unable to change
canonical meaning or authority.

#### Scenario: A domain changes graph providers
- **WHEN** a DomainxFactory rebuilds the same pinned ontology in a different graph or retrieval provider
- **THEN** stable identifiers, deterministic conformance results, semantic-context digests, and authority behavior remain unchanged
