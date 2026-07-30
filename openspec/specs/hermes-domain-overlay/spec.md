# hermes-domain-overlay Specification

## Purpose
The neutral contract for a domain's seedable Hermes overlay: the
`hermes_domain_overlay` schema (identity, approval scopes, authority
boundaries with the `<domain.id>_owns` naming and no-overlap rules), the
`hermes_overlay_descriptor` role→path declaration with a
documented-convention fallback, the canonical validator with self-testing
fixtures, and versioned publication (realized at `contract-v1.15`;
realization proof: codexFactory's live overlay passes unmodified). Consumer
handoff: hermes-install's seeding materialization increment pins the release
and replaces its minimal structural check. (Created by archiving change
add-hermes-domain-overlay-contract.) The declarable content set
(`hermes_domain_content_manifest`, convention-then-contract successor to the
increment-4a well-known-path list; realized at `contract-v1.18` by archiving
change add-hermes-domain-content-manifest) extends the family.
## Requirements
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

### Requirement: The domain content set is declarable, with the documented convention as fallback
A domain repository SHALL be able to declare its seedable content set in a
`hermes/domain/content-manifest.yaml` document of kind
`hermes_domain_content_manifest`, mapping each declared `content_kind` from
the ratified vocabulary to a document `path` or per-file `directory` within
the archive. The vocabulary SHALL include `domain_ontology` for a package that
validates against the xFactory semantic-kernel contract. A consumer SHALL
honor the declaration when present, fall back to the documented convention
when absent for a legacy archive, fail closed when a declared path is missing
or an ontology package is invalid or digest-drifted, and never load an
undeclared kind silently.

#### Scenario: A declared manifest is honored
- **WHEN** a domain archive ships `hermes/domain/content-manifest.yaml` declaring `practice_adoption: {path: hermes/domain/practice-catalog.yaml}`
- **THEN** the consumer loads the practice catalog from the declared path and the manifest validates against the neutral schema

#### Scenario: A domain ontology directory is declared
- **WHEN** the content manifest declares `domain_ontology: {directory: hermes/domain/ontology}`
- **THEN** the consumer validates the ontology manifest, exact kernel import, package inventory, and digests before seeding it

#### Scenario: A missing manifest falls back to convention
- **WHEN** a legacy domain archive carries no `hermes/domain/content-manifest.yaml`
- **THEN** the consumer loads the documented conventional set exactly as before, with no new refusal class, and does not invent or infer an ontology package

#### Scenario: A declared path missing from the archive fails closed
- **WHEN** the manifest declares a kind whose path does not exist in the archive
- **THEN** validation fails closed naming the kind and path, and no content loads for that archive

#### Scenario: An unknown content kind fails validation
- **WHEN** the manifest declares a `content_kind` outside the ratified vocabulary
- **THEN** the canonical validator rejects the manifest naming the unknown kind

### Requirement: Generated domains declare a Domain Hermes ontology package
An ontology-aware domain starter SHALL make every generated DomainxFactory
declare a `domain_ontology` content location and SHALL keep that
content in draft status until Domain Hermes ratifies and publishes it. The
starter SHALL record its own ontology-aware starter version in the generated
repository so the completeness check is deterministic rather than inferred, and
SHALL preserve active domain-owned ontology content on rerun and report
candidates and conflicts separately.

#### Scenario: New domain is generated
- **WHEN** the current domain starter creates a new DomainxFactory repository
- **THEN** it emits the draft ontology content tree, records the ontology-aware starter version, and declares `domain_ontology` in the Domain Hermes content manifest

#### Scenario: Generated domain omits ontology content
- **WHEN** a repository records an ontology-aware starter version but its content manifest lacks `domain_ontology`
- **THEN** generated-domain validation MUST fail with a finding that the semantic scaffold is incomplete

#### Scenario: Legacy domain has not migrated
- **WHEN** an existing DomainxFactory predates the ontology-aware starter and has no ontology declaration
- **THEN** its existing content remains consumable under the prior pin, but it cannot claim ontology readiness until it completes explicit migration

