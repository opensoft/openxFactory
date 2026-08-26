## MODIFIED Requirements

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

## ADDED Requirements

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
