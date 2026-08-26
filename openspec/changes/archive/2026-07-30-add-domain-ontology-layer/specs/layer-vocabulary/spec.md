## MODIFIED Requirements

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
