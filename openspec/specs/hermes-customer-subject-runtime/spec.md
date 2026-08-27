# hermes-customer-subject-runtime Specification

## Purpose
Define the domain-neutral Hermes runtime topology, Customer-subject identity,
lifecycle, assembly-pinning, provisioning, and Gate G0 consumer-handoff
requirements shared across xFactory installations.

## Requirements

### Requirement: Static role templates and runtime instances are distinct
The canonical DomainxFactory stack contract SHALL treat its Customer, Client, and Domain Hermes layer declarations as reusable role templates, while the Hermes runtime-topology contract SHALL represent concrete layer instances. The static stack SHALL continue to require exactly one template for each canonical role and SHALL reject duplicate canonical role declarations.

#### Scenario: One Customer template produces multiple runtime instances
- **WHEN** a valid DomainxFactory declares one Customer role template and an operational topology instantiates that template for two customer subjects
- **THEN** both runtime instances MUST validate without adding a second Customer declaration to `stack.yaml`

#### Scenario: Duplicate static Customer role remains invalid
- **WHEN** a DomainxFactory declares two `role: customer` entries in `stack.yaml`
- **THEN** canonical DomainxFactory validation MUST fail

#### Scenario: Extension role is not used to evade the model
- **WHEN** a topology attempts to represent a second customer subject through a static `extension` layer
- **THEN** runtime conformance MUST reject it as an invalid customer-subject instantiation

### Requirement: Customer-subject identity and aliases are domain-neutral
Every Customer runtime instance SHALL identify its subject with domain-owned `customer_subject.kind`, `customer_subject.issuer`, `customer_subject.namespace`, a constrained pseudonymous `customer_subject.ref` in `urn:xfactory:subject:<uuid>` form, and a pinned issuer attestation to the reference policy. The policy SHALL require an independently generated cryptographically random UUIDv4/UUIDv7 surrogate or approved keyed tokenization and SHALL prohibit UUIDv3/v5, reversible encoding, raw or unkeyed hashes, and other deterministic derivation from source identifiers. Client and Domain runtime instances MUST NOT carry a customer-subject identity. Project, patient, client-company, ledger, campaign, and similar names SHALL remain DomainxFactory aliases and MUST NOT become required neutral fields or enumerations. Deterministic validation SHALL enforce syntax, length, issuer/namespace policy, and deny-pattern/sentinel evidence but MUST NOT claim universal semantic PII detection.

#### Scenario: codexFactory maps a Project Hermes instance
- **WHEN** codexFactory instantiates Customer Hermes for a repository or project
- **THEN** the neutral record MUST use the governed customer-subject kind, issuer, namespace, pseudonymous reference, and policy attestation
- **AND** Project Hermes terminology MAY be supplied by the codexFactory overlay

#### Scenario: MedxFactory maps a Patient Hermes instance
- **WHEN** MedxFactory instantiates Customer Hermes for a patient
- **THEN** the same neutral schema MUST validate with a patient-owned subject kind and opaque reference
- **AND** no project field MUST be required

#### Scenario: LedgerxFactory maps a client-company instance
- **WHEN** LedgerxFactory instantiates Customer Hermes for an accounting client company
- **THEN** the same neutral schema MUST validate with a client-company subject kind and opaque reference

#### Scenario: Subject reference violates its governed profile
- **WHEN** a topology uses a ref outside the constrained surrogate syntax, lacks issuer attestation, or matches a deterministic forbidden sentinel or secret pattern
- **THEN** conformance validation MUST fail closed

#### Scenario: Subject reference is deterministically derived without a key
- **WHEN** issuer evidence declares or a fixture proves that a surrogate uses UUIDv3/v5, reversible encoding, or an unkeyed derivation from a source identifier
- **THEN** conformance validation MUST fail closed

### Requirement: Runtime topology has durable identity and lifecycle cardinality
The runtime topology SHALL record immutable installation, stack, and layer identity registrations plus append-only installation, stack, and layer lifecycle events. Current lifecycle state SHALL be derived from the immutable initial registration and one linear, predecessor-linked event chain; any materialized current-state projection SHALL be non-authoritative, reconciled to that chain, and writable only through a governed transition operation. Direct identity/state mutation, event update/delete, a forked predecessor, and every transition out of `retired` SHALL fail. Topology states SHALL be the closed set `installing`, `configured`, `operational`, `suspended`, and `retired`; layer states SHALL be `provisioning`, `active`, `suspended`, `failed`, and `retired`, with terminal retirement and defined transitions. Provisioning may activate, fail, or retire; active and suspended layers may fail; failed layers may re-enter provisioning through governed recovery or retire. Installing permits at most one non-retired Client and Domain registration and no Customer registration; configured requires exactly one active Client and one active Domain and permits zero or more active Customers; operational additionally requires at least one active Customer. Suspended preserves registrations but permits no new jobs; retired requires every layer to be retired. Layer IDs, policy namespaces, and Customer subject tuples SHALL be protected by durable tombstones and unique for the lifetime of the stack.

#### Scenario: Operational topology contains two Customer instances
- **WHEN** one installation has one active Client layer, one active Domain layer, and two active Customer layers with distinct subject tuples and policy namespaces
- **THEN** the topology MUST validate

#### Scenario: Configuration precedes subject onboarding
- **WHEN** a `configured` topology has one active Client, one active Domain, and no Customer instance
- **THEN** the topology MUST validate as non-operational

#### Scenario: Operational topology has no Customer
- **WHEN** an `operational` topology has no active Customer instance
- **THEN** validation MUST fail

#### Scenario: Singleton role cardinality is violated
- **WHEN** a configured or operational topology has zero or two active Client instances or zero or two active Domain instances
- **THEN** validation MUST fail

#### Scenario: Retired identity is reused
- **WHEN** a retired registration is deleted or a new layer attempts to reuse its layer ID, policy namespace, or customer-subject tuple
- **THEN** validation MUST fail

#### Scenario: Lifecycle history is bypassed or retirement is reversed
- **WHEN** an actor directly changes an identity/current-state row, updates or deletes a lifecycle event, forks an event predecessor, or appends a transition out of `retired`
- **THEN** persistence and conformance validation MUST fail
- **AND** the derived lifecycle projection MUST remain reconciled to the immutable event chain

### Requirement: Runtime assembly pins are content-addressed
Every canonical contract and single-file template used by a topology SHALL be
pinned by canonical repository identity, repository-relative regular-file path,
exact 40-hex commit, schema identifier/version where applicable, and SHA-256 digest.
A directory overlay SHALL be pinned through a governed overlay manifest declaring
one repository-relative `overlay_root`, a bytewise-sorted inventory of every
regular file recursively below that root, per-file raw-byte SHA-256 digests, and
the closed exclusions `.gitkeep` and an optional colocated generated digest
inventory; the topology SHALL pin that manifest by commit and digest. Movable
branches, tag-only references, missing or extra overlay members, symlink escapes,
path traversal, and digest drift SHALL fail closed.

#### Scenario: Exact assembly pin resolves
- **WHEN** every declared path exists as a regular in-repository file at the exact commit and its bytes match the declared digest
- **THEN** assembly-pin validation MUST pass

#### Scenario: Branch-only or tag-only pin is supplied
- **WHEN** a topology supplies a movable branch or a tag without the exact commit and digest
- **THEN** validation MUST fail

#### Scenario: Pinned content drifts
- **WHEN** the resolved bytes do not match the declared SHA-256 digest
- **THEN** validation MUST fail before runtime realization

#### Scenario: Overlay manifest omits a runtime file
- **WHEN** an overlay tree contains a required runtime file that is absent from its pinned manifest or contains an inventoried file whose digest drifts
- **THEN** assembly-pin validation MUST fail

### Requirement: Customer-subject lifecycle preserves identity and evidence
Provisioning and retirement SHALL be idempotent operations over the neutral customer-subject identity. Provisioning the same idempotency key and subject SHALL return the same layer identity; conflicting reuse SHALL fail. Retirement SHALL stop new work, append a terminal tombstone, preserve immutable evidence and the subject-to-layer identity, prohibit hard deletion, and SHALL NOT permit later identity reuse.

#### Scenario: Provision request is retried
- **WHEN** the same authorized provisioning request is submitted repeatedly with the same idempotency key and subject tuple
- **THEN** it MUST resolve to one Customer layer identity and one lifecycle record

#### Scenario: Provision key is reused for another subject
- **WHEN** an existing idempotency key is submitted with a different customer-subject tuple
- **THEN** provisioning MUST fail closed

#### Scenario: Customer subject is retired
- **WHEN** an active Customer instance is retired
- **THEN** new jobs for that layer MUST be rejected
- **AND** its artifacts, approvals, traces, audit evidence, layer ID, subject tuple, and policy namespace MUST remain preserved

### Requirement: Canonical validation proves cross-domain conformance
openxFactory SHALL publish a canonical structural and semantic validator plus indexed positive and negative fixtures for the customer-subject runtime contract. The validator SHALL prove at least two Customer instances in one installation and SHALL demonstrate that codexFactory, MedxFactory, and LedgerxFactory aliases specialize the same neutral contract.

#### Scenario: Two-subject positive fixture is checked
- **WHEN** the canonical fixture suite runs
- **THEN** an operational installation with two isolated Customer instances MUST pass

#### Scenario: Domain-neutral mapping fixtures are checked
- **WHEN** project, patient, and client-company examples are validated
- **THEN** all MUST use the same canonical schema without adding domain nouns to required neutral vocabulary

#### Scenario: Negative topology fixture is accidentally accepted
- **WHEN** any indexed invalid cardinality, identity, sensitive-reference, pin, or lifecycle fixture returns success
- **THEN** the conformance suite MUST fail
