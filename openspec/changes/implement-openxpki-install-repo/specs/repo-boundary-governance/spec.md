# repo-boundary-governance Specification (delta)

## MODIFIED Requirements

### Requirement: OpenXPKI install repository boundary
The deployable certificate-authority runtime SHALL live in a private,
independently released repository named `OpenXPKI-Install`, created
2026-08-21 by the `implement-openxpki-install-repo` successor change as
`opensoft/OpenXPKI-Install` and following the
`xFactory-Hermes-Install` pattern. From creation it SHALL own the OpenXPKI server, client,
and web deployment topology for QA and any later environment, the
per-client instantiation at `config/clients/<tenant>/runtime-manifest.yaml`
(generated, never hand-edited, digest-pinned by its consumers), and its own
install, verification, upgrade, backup, restore, and disaster-recovery
procedures. It SHALL consume ONLY the digest-pinned container image whose
custody — build sources, release / package / configuration / base-image
pins, and the offline and integration test harness — remains in
`opensoft/Opensoft-Tenant`, because deciding what binary a tenant's
certificate authority runs is a tenant trust decision. It MUST NOT contain
image build sources, a pipeline producing that image, a mutable image tag
reference, secrets, credentials, or certificate-authority key material.

`openxFactory` SHALL remain the canonical owner of the neutral
`trust-anchor` contract and the OpsxFactory `pki-administration` capability
SHALL remain the owner of the governed administration procedure; the
install repository realizes both and owns neither.

#### Scenario: Install repository is created
- **WHEN** the successor change creates `OpenXPKI-Install`
- **THEN** it MUST be private and independently releasable, identify `openxFactory` as neutral contract owner and `opensoft/Opensoft-Tenant` as image-custody owner, and contain no image build sources, secrets, credentials, or key material

#### Scenario: Image custody is proposed inside the install repository
- **WHEN** a change would add a container build, image pinning logic, or a mutable tag reference to the install repository
- **THEN** repository-boundary validation MUST reject it and route it to `opensoft/Opensoft-Tenant`
- **AND** the install repository MUST consume the resulting immutable digest rather than reproduce the decision that produced it

#### Scenario: Aggregation admission is proposed
- **WHEN** xFactory proposes pinning the repository at `installs/openxpki-install`
- **THEN** a separate reviewed change MUST define and verify gitlink path, remote, visibility, exact validated commit, recursive checkout, compatibility, update, and rollback behavior
- **AND** repository creation MUST NOT be treated as aggregation admission
