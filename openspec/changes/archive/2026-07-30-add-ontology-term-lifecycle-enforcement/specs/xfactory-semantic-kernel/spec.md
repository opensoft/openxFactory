# xfactory-semantic-kernel — add-ontology-term-lifecycle-enforcement deltas

## MODIFIED Requirements

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
SHALL fail when a subset is neither closed nor explicitly truncated. A term
subset SHALL NOT include a term the pinned package retires: compilation
refuses a retired term in the requested set or the computed closure, a worker
profile naming a retired required term is invalid, and the canonical
validator rejects a context pinned at the current package digest whose
subset carries a retired term — while historical contexts pinned at prior
digests keep their original interpretation unchanged. An
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

#### Scenario: A requested subset includes a retired term
- **WHEN** a requested or profiled term subset, or its computed closure, includes a term whose `lifecycle_state` is `retired` in the pinned package version
- **THEN** compilation MUST fail closed naming the retired term, and the canonical validator MUST reject a context pinned at the current package digest that carries it
- **AND** a context compiled under a prior pin in which the term was not retired keeps its original interpretation and is not retroactively invalidated

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
