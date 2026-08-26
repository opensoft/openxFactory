# hermes-domain-overlay — Spec Delta

## ADDED Requirements

### Requirement: A domain overlay validates against the neutral schema
openxFactory SHALL define a neutral `hermes_domain_overlay` schema requiring `schema_version`, domain identity (`id`, `display_name`), non-empty `approval_scope_kinds`, non-empty `required_approval_fields`, and `authority_boundaries` carrying a non-empty domain-owned list, `xfactory_owns`, and `repository_owns` with no item appearing in more than one boundary list.

#### Scenario: The live codexFactory overlay validates
- **WHEN** the canonical validator runs against codexFactory's `hermes/domain/overlay.yaml`
- **THEN** it passes without modification

#### Scenario: A missing required block fails closed
- **WHEN** an overlay omits `authority_boundaries` or declares an empty `approval_scope_kinds`
- **THEN** validation fails with a finding naming the missing or empty block

#### Scenario: Overlapping authority boundaries fail closed
- **WHEN** the same authority item appears in more than one boundary list (e.g. both domain-owned and `repository_owns`)
- **THEN** validation fails naming the duplicated item

### Requirement: The role→path rule is declarable, with a safe fallback
A domain repo MAY ship `hermes/overlay-descriptor.yaml` (`kind: hermes_overlay_descriptor`) declaring, per layer role, the overlay document path within the repo; when the descriptor is absent, consumers SHALL fall back to the documented convention (domain → `hermes/domain/overlay.yaml`), and a descriptor entry whose declared path does not exist in the repo SHALL fail validation.

#### Scenario: Descriptor declares the domain path
- **WHEN** a descriptor declares `domain: hermes/domain/overlay.yaml` and the file exists
- **THEN** validation passes and consumers use the declared path

#### Scenario: Missing descriptor falls back to convention
- **WHEN** a domain repo ships no `hermes/overlay-descriptor.yaml`
- **THEN** consumers use the documented role→path convention and validation does not fail for the descriptor's absence

#### Scenario: Dangling declared path fails closed
- **WHEN** a descriptor declares a path that does not exist in the repo
- **THEN** validation fails naming the role and the dangling path

### Requirement: A canonical validator ships with fixtures
openxFactory SHALL ship `scripts/validate-hermes-domain-overlay.py` implementing the schema and descriptor checks, with positive and negative fixtures under the contract directory, consumable by domain validate chains like the other canonical validators.

#### Scenario: Positive fixture passes, mutated fixture fails
- **WHEN** the validator runs over the contract fixtures
- **THEN** the positive fixture passes and each negative fixture fails with its expected finding

#### Scenario: Domain validate chains can consume it
- **WHEN** a DomainxFactory validate chain resolves the openxFactory checkout
- **THEN** the validator is invocable against that domain repo the same way as the existing canonical validators

### Requirement: The contract publishes as a versioned additive bundle
The schemas and validator SHALL publish as a versioned additive contract bundle per the contract-versioning policy, so consumers pin an exact release before relying on it.

#### Scenario: Consumers pin the bundle
- **WHEN** hermes-install's seeding materialization increment adopts schema validation
- **THEN** it validates against a pinned contract release rather than a copied schema
