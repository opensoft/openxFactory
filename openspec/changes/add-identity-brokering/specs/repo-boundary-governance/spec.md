# repo-boundary-governance Specification (delta)

## ADDED Requirements

### Requirement: Keycloak install repository boundary

The identity-broker runtime SHALL live in a private, independently
released repository named `xFactory-Keycloak-Install`, created by the
`implement-keycloak-install-repo` successor change and, when admitted,
pinned into the top-level xFactory aggregation at
`installs/keycloak-install`.

From creation it SHALL own the broker deployment topology — manifests,
ingress and routing, datastore topology, backup, restore, upgrade,
verification, and disaster recovery — and the per-client instantiation of
that topology as `config/clients/<tenant>/runtime-manifest.yaml` on the
`xFactory-Hermes-Install` precedent: generated from the deployed stack,
never hand-edited, and digest-pinned by its consumers. It SHALL pin the
compatible openxFactory contract bundle tag plus exact contract commit and
digests for the neutral `identity-brokering` contracts it consumes.

It MUST NOT contain a service-client secret, an upstream identity-provider
credential, a datastore credential, an administrative bootstrap
credential, key material, or a broker configuration or realm export
carrying credential values — each of those is a `credential-contracts`
record with declared custody. It MUST NOT restate neutral contract
meaning, which `openxFactory` continues to own as the canonical
`identity-brokering` authority, and it MUST NOT carry the governed
administration workflow, which the owning DomainxFactory owns as
`keycloak-administration`.

Adding the repository to the aggregation SHALL be a separate reviewed
change that records path, remote, visibility, exact validated commit,
checkout, compatibility, update, and rollback behavior — the same
separate-reviewed-act discipline this capability already applies to
deferred aggregation integration. Repository creation SHALL NOT be treated
as aggregation admission.

#### Scenario: Broker install repository is created

- **WHEN** the `implement-keycloak-install-repo` successor change creates `xFactory-Keycloak-Install`
- **THEN** it MUST be private and independently releasable, identify `openxFactory` as the owner of the neutral identity contracts it pins, and contain no credential values or key material

#### Scenario: Per-client broker instance is instantiated

- **WHEN** a tenant's broker instance is instantiated
- **THEN** its stack identity MUST be a generated `config/clients/<tenant>/runtime-manifest.yaml` in the install repository
- **AND** consumers MUST pin that manifest by digest rather than copy its contents

#### Scenario: Credential-bearing configuration is proposed in the install repo

- **WHEN** a change proposes committing a client secret, identity-provider credential, datastore credential, key material, or a configuration or realm export containing credential values
- **THEN** repository-boundary validation MUST reject it and route the material to a `credential-contracts` record

#### Scenario: Broker aggregation pin is proposed

- **WHEN** xFactory proposes pinning `installs/keycloak-install`
- **THEN** a dedicated reviewed change MUST define and verify gitlink path, remote, visibility, exact validated commit, checkout, compatibility, update, and rollback behavior
- **AND** the repository's own creation change MUST NOT be accepted as that record

#### Scenario: Neutral contract meaning drifts into the install repo

- **WHEN** the install repository would restate or redefine `identity-brokering` requirement meaning rather than pin it
- **THEN** the restatement MUST be rejected and the canonical text MUST remain in `openxFactory`
