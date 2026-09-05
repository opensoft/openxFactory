# layer-vocabulary Specification

## Purpose

Fix the canonical, domain-neutral names of the three Hermes layers — Subject
Hermes for the served party or work subject, Tenant Hermes for the
tenant-operator organization running the installation, and Domain Hermes for
reusable expert-domain policy — retiring a Customer/Client/Domain vocabulary
in which the same commercial word denoted opposite layers in different
DomainxFactories. Change only the names: each layer's responsibility
boundary is identical before and after, and a domain specializes the
vocabulary through declared aliases such as Patient Hermes or Project Hermes,
each bound to exactly one canonical layer, never by redefining or replacing a
canonical name. Reserve "Customer" and "Client" against reuse as layer names
on new or substantively revised governance surfaces, while both remain legal
in prose describing commercial relationships. Freeze the released machine
identifiers that encode the legacy spellings until the next major contract
bundle so pinned consumers resolve byte-identically, and publish
`contracts/policies/layer-vocabulary.yaml` as the mapping through which a
`customer_subject_ref` or a `client` role kind is interpreted rather than
rewritten.
## Requirements
### Requirement: Canonical Hermes layer vocabulary
The three Hermes layers SHALL be named, in canonical domain-neutral vocabulary, **Subject Hermes**, **Tenant Hermes**, and **Domain Hermes**.
Their role definitions retain the prior Customer/Client/Domain model: Subject
Hermes owns subject-specific context, consent, preferences, journey state, and
private memory for the served party or work subject (a patient, a project, a
managed system, a client company); Tenant Hermes owns tenant-operator policy,
staff, integrations, local constraints, credentials, organizational memory,
and tenant semantic bindings for local systems; Domain Hermes owns reusable
expert-domain policy, source authority, domain ontology stewardship, domain
memory boundaries, review standards, and escalation. openxFactory retains
ownership of the neutral semantic kernel, extension and validation contracts,
and cross-layer governance rules.

#### Scenario: A governance document names the layers
- **WHEN** a new or substantively revised governance document, spec, or contract describes the three-layer Hermes model
- **THEN** it names the layers Subject Hermes, Tenant Hermes, and Domain Hermes
- **AND** any reference to the legacy Customer/Client/Domain names appears only as an explicitly labeled legacy-vocabulary note

#### Scenario: Layer semantics are unchanged by the rename
- **WHEN** a consumer compares a layer's responsibility boundary before and after vocabulary adoption
- **THEN** the responsibility boundary is identical; only the canonical name differs
- **AND** naming domain-ontology stewardship and tenant semantic bindings makes responsibilities the layers already held explicit rather than relocating any of them

#### Scenario: Layer semantics include ontology stewardship
- **WHEN** a DomainxFactory creates or updates reusable domain concepts, relations, state models, or semantic mappings
- **THEN** Domain Hermes owns the review and lifecycle decision
- **AND** Subject Hermes retains private instances, Tenant Hermes retains local bindings, and openxFactory retains neutral contract ownership

### Requirement: Domain alias model
Each DomainxFactory SHALL specialize the canonical layer names through declared aliases and MUST NOT redefine or replace the canonical names.
An alias declaration binds a domain-facing name (for example Patient Hermes,
Project Hermes, Care-Organization Hermes) to exactly one canonical layer name.

#### Scenario: A domain declares its subject alias
- **WHEN** MedxFactory presents Subject Hermes to its users as Patient Hermes
- **THEN** its overlay declares the alias against the canonical layer name `subject`
- **AND** cross-domain contracts and validators continue to use the canonical name

#### Scenario: A domain-facing name conflicts with a canonical name
- **WHEN** a domain proposes an alias whose name equals a canonical layer name of a different layer
- **THEN** the alias MUST be rejected

### Requirement: Reserved ambiguous layer terms
The terms "Customer" and "Client" MUST NOT be used as Hermes layer names in new or substantively revised governance surfaces.
Both terms remain legal in prose describing commercial relationships (for
example, a client of Opensoft, a customer engagement) and inside frozen legacy
machine identifiers governed by the machine-identifier freeze.

#### Scenario: A new document names a layer "Client Hermes"
- **WHEN** a new governance document introduces a layer named Client Hermes or Customer Hermes
- **THEN** review MUST reject the name and require the canonical vocabulary or a declared domain alias

#### Scenario: Commercial prose is not a layer name
- **WHEN** a document says a client company purchased an xFactory installation
- **THEN** the reserved-terms rule does not apply, because the term describes a commercial relationship rather than a layer

### Requirement: Machine identifier freeze and mapping
Released machine identifiers that encode the legacy vocabulary SHALL remain byte-stable until the next major contract bundle, and openxFactory SHALL publish the legacy-to-canonical mapping machine-readably in `contracts/policies/layer-vocabulary.yaml`.
Frozen identifiers include, at minimum, role kinds `customer|client|domain`,
`customer_subject` and `customer_subject_ref`, contract `$id`s and
`contract_id`s under `contracts/hermes-runtime/`, and released schema field
names. Within an existing contract family, spellings stay internally
consistent with that family's released version; wholesale identifier
migration happens only as a dedicated major-version change. New contract
families authored after adoption use the canonical vocabulary from their
first version.

#### Scenario: A pinned consumer resolves a released bundle
- **WHEN** an install repository pins a released contract bundle that predates the vocabulary adoption
- **THEN** every pinned path, schema, digest, and identifier resolves byte-identically

#### Scenario: A new contract family is authored after adoption
- **WHEN** a new contract family is created in openxFactory
- **THEN** its identifiers use `subject` and `tenant` spellings from its first published version

#### Scenario: A legacy identifier needs interpretation
- **WHEN** a tool or reviewer encounters `customer_subject_ref` or a role kind of `client` in a released contract
- **THEN** `contracts/policies/layer-vocabulary.yaml` maps it to the canonical layer name without modifying the released file

