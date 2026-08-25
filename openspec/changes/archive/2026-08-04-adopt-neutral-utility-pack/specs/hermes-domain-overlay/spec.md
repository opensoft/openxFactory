# hermes-domain-overlay Delta: The Layer-Template Schema Joins the Family

## ADDED Requirements

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
