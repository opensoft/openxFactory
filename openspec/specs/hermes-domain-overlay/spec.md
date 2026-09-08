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

### Requirement: The subject/tenant layer-template schema is part of the overlay family
openxFactory SHALL own the neutral subject/tenant Hermes layer-template schema as part of this contract family, published at `contracts/hermes-domain-overlay/hermes-layer-template.schema.json`.
The schema (JSON Schema draft 2020-12, JSON format retained — design D4)
covers the two layer-template kinds that carry no top-level domain object,
`subject_hermes_template` and `client_hermes_template`; the domain layer
stays governed by `hermes-domain-overlay.schema.yaml`. The kind values and
the `role: client` const keep the frozen v1 machine spellings per
`contracts/policies/layer-vocabulary.yaml`.

#### Scenario: A domain layer template validates against it

- **WHEN** a domain repo ships a subject or client Hermes layer template (`kind: subject_hermes_template` or `client_hermes_template`)
- **THEN** the template validates against the neutral layer-template schema rather than against a domain-local schema copy

#### Scenario: Bundle publication is additive

- **WHEN** the next contract bundle release after this adoption publishes
- **THEN** the layer-template schema enters `contracts/manifest.yaml` as an additive entry per the contract-versioning policy
- **AND** until a consuming domain repo re-pins, its local schema copy remains authoritative (document-lifecycle mid-promotion rule) and the register entry stays below `adopted`

### Requirement: A subject overlay validates against a neutral subject-overlay contract
openxFactory SHALL define a neutral `hermes_subject_overlay` schema in the hermes-domain-overlay contract family for the seedable document of a Subject Hermes layer.
The schema requires `schema_version`, `kind`, and a `subject` block carrying
`id`, `subject_kind`, `display_name`, `policy_namespace`,
`relation_to_baseline`, and a non-empty `policies` mapping. The `subject` block
SHALL permit additional domain-declared identity fields rather than closing
over a neutral field list. The kind name uses the canonical Subject/Tenant/Domain
vocabulary while the runtime layer role remains the frozen machine key
`customer`; the schema SHALL record that mapping explicitly with reference to
`contracts/policies/layer-vocabulary.yaml`, and SHALL NOT rename either side.

#### Scenario: A subject overlay validates
- **WHEN** a domain repo ships a document of `kind: hermes_subject_overlay` declaring subject identity, a policy namespace, a declared relation to baseline, and at least one named policy
- **THEN** the canonical validator accepts it
- **AND** no `domain` block, `authority_boundaries`, or fabricated domain identity is required of it

#### Scenario: A subject overlay omitting a required identity block fails closed
- **WHEN** a subject overlay omits `policy_namespace`, omits `relation_to_baseline`, or declares an empty `policies` mapping
- **THEN** validation fails with a finding naming the missing or empty block

#### Scenario: The frozen role key and the canonical kind name coexist
- **WHEN** a reviewer reads a descriptor declaring `customer: hermes/subject/<id>/overlay.yaml` alongside a document of `kind: hermes_subject_overlay`
- **THEN** the contract states that `customer` is the frozen runtime role key mapping to the canonical `subject` layer
- **AND** neither the released descriptor role key nor the new kind name is renamed to match the other

### Requirement: A subject policy is addressable by policy namespace and policy id
A subject overlay SHALL make every named policy addressable as `<policy_namespace>/<policy_id>`, and the neutral contract MUST NOT enumerate a closed set of policy names.
Policy ids SHALL be unique within the document, each `policies` key SHALL equal
its policy's declared `policy_id`, and each policy's declared
`policy_namespace` SHALL equal the subject's `policy_namespace`. The policy
BODY is domain-owned: the contract governs the addressing envelope and leaves
the body open, because enumerating policy names is exactly what prevents the
tenant-layer policy contract from carrying a domain's named policy.

#### Scenario: A named policy resolves to exactly one payload
- **WHEN** a subject declares `policy_namespace: opensoft.codexfactory.project-alfa` and a policy keyed `admission-conditions`
- **THEN** the address `opensoft.codexfactory.project-alfa/admission-conditions` resolves to exactly one policy payload

#### Scenario: A policy name the neutral contract has never seen still validates
- **WHEN** a domain declares a named policy whose id appears in no neutral vocabulary
- **THEN** validation passes, because the contract governs the addressing envelope and not the policy vocabulary

#### Scenario: A mismatched or duplicated address fails closed
- **WHEN** a `policies` key differs from its declared `policy_id`, or a policy declares a `policy_namespace` different from the subject's
- **THEN** validation fails naming the inconsistent address

### Requirement: Subject identity conforms to the domain's own subject template
The canonical validator SHALL enforce a subject overlay's identity against the domain repository's own `subject_hermes_template` rather than against a neutral field list.
When a repo path is supplied and the repo ships a subject template at the
documented convention path `hermes/subject/template.yaml`, `subject.subject_kind`
MUST be a declared member of `subject_hermes.subject_kinds`, and every entry of
`subject_hermes.required_subject_fields[subject_kind]` MUST be present and
non-empty on the `subject` block. A repo with no subject template SHALL be
skipped with notice, introducing no new refusal class.

#### Scenario: A project subject satisfies its domain's declared required fields
- **WHEN** a domain template declares `required_subject_fields.project: [id, owner, repositories]` and a subject overlay declares `subject_kind: project`
- **THEN** validation requires `id`, `owner`, and `repositories` on the subject block
- **AND** those field names come from the domain's template, never from the neutral schema

#### Scenario: An undeclared subject kind fails closed
- **WHEN** a subject overlay declares a `subject_kind` that the domain's template does not list in `subject_kinds`
- **THEN** validation fails naming the undeclared kind and the declared set

#### Scenario: A repo with no subject template is not newly broken
- **WHEN** a domain repo ships a subject overlay but no `hermes/subject/template.yaml`
- **THEN** the cross-document check is skipped with an explicit notice and the structural checks still run

### Requirement: A subject overlay adds constraints and never relaxes
A subject overlay SHALL declare `relation_to_baseline: additive_constraints_only` and SHALL NOT carry authority-granting, permission-widening, or credential-value content.
The invariant is enforced structurally on the document rather than by importing
the tenant layer's `relation_to_domain: stricter_only` comparability engine,
whose defined partial orders are keyed to tenant-policy keys and would return
`review_required` for additive named constraints that have no baseline
counterpart. A subject overlay MUST NOT carry `authority_boundaries`,
`approval_scope_kinds`, or `required_approval_fields` — the Domain layer's
enforceable slice — and `relation_to_baseline` is a single-value enum so a
future relation can be added additively.

#### Scenario: A relaxing or authority-claiming subject overlay fails closed
- **WHEN** a subject overlay carries `authority_boundaries`, `approval_scope_kinds`, `required_approval_fields`, or a credential value
- **THEN** validation fails naming the prohibited block

#### Scenario: An undeclared relation fails closed
- **WHEN** a subject overlay omits `relation_to_baseline` or declares a value outside the ratified enum
- **THEN** validation fails, and no relation is inferred by default

#### Scenario: The tenant comparability engine is not applied to a subject
- **WHEN** a subject declares additive named constraints with no counterpart key in any baseline document
- **THEN** they validate as constraints
- **AND** they are not run through the client-content stricter-only comparison, which would return `review_required` for every one of them

### Requirement: The canonical validator governs descriptor-declared subject paths
The canonical validator SHALL validate a descriptor-declared subject path against the subject-overlay contract instead of skipping it.
Today `scripts/validate-hermes-domain-overlay.py` checks that a declared
customer path EXISTS and then skips any document whose kind is not
`hermes_domain_overlay`, leaving its content governed by nothing. After this
change the validator SHALL dispatch by kind at every declared path, and SHALL
retain the skip-with-notice for kinds owned by another canonical validator so
that canonical meaning is never forked. Positive and indexed negative fixtures
SHALL ship in the family's self-testing idiom, each negative declaring its
`# expected_failure:` reason.

#### Scenario: A declared subject path is validated, not skipped
- **WHEN** a descriptor declares the customer role path and the document there carries `kind: hermes_subject_overlay`
- **THEN** the validator validates it and reports it as validated rather than printing a skip line

#### Scenario: A kind owned by another canonical validator is still skipped with notice
- **WHEN** a declared path carries `kind: hermes_client_overlay`, owned by `scripts/validate-client-content.py`
- **THEN** the validator prints its skip-with-notice and does not re-implement that family's rules

#### Scenario: The self-test covers the new kind in both directions
- **WHEN** the validator's self-test runs
- **THEN** the packaged subject-overlay example passes and every packaged subject negative fails for its declared reason

### Requirement: The subject overlay's enforceable slice is specified, and materialization is not
The contract SHALL state what a conforming subject overlay contributes as enforceable content, and SHALL leave the mechanics of materializing it to the consuming install repository.
A conforming subject overlay contributes a `subject_identity` payload (the
declared identity without the policies) and a `policy_position` payload keyed
by policy id, reusing the already-ratified `policy_position` content kind so a
consumer resolving a namespaced address reads the same kind of content
whichever layer holds it. Each policy payload SHALL restate its own
`policy_namespace` and `policy_id` so it is address-resolvable without joining
to a sibling record. Extraction, transaction shape, provenance, digest
verification, and refusal vocabulary remain the consumer's; openxFactory owns
document shape and canonical validation.

#### Scenario: A conforming document yields a non-empty enforceable slice
- **WHEN** a consumer splits the enforceable slice of a validated subject overlay carrying one named policy
- **THEN** the slice carries a subject identity payload and a policy payload keyed by that policy's id, and is non-empty

#### Scenario: A materialized policy row is address-resolvable on its own
- **WHEN** a reader holds only the materialized policy payload
- **THEN** the payload carries its policy namespace and policy id, so the address resolves without reading the subject identity record

#### Scenario: Materialization mechanics are not specified by this contract
- **WHEN** a consuming install repository changes how it extracts, transacts, or records provenance for a seeded slice
- **THEN** no requirement of this contract changes, because the contract governs the document and the slice it contributes, not the mechanism

