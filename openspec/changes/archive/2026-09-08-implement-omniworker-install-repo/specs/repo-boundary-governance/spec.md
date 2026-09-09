# repo-boundary-governance Specification (delta)

## ADDED Requirements

### Requirement: OmniWorker install repository boundary

The worker-host product SHALL live in a private, independently released
repository named `OmniWorker-Install`, created as `opensoft/OmniWorker-Install`
by this change's realization on Brett Heap's ruling of 2026-09-05 that the
name `omniWorker` covers "the worker-host product only", and, when admitted,
pinned into the top-level xFactory aggregation at `installs/omniworker-install`.

From creation it SHALL own the worker host application that converges a Cloud
PC or workstation into a worker host, its deployment and detection scripts and
their test harnesses, the worker pack and the worker profiles and prompt sets a
host materializes, the worker-host manifest schema and the per-client host
manifests as `clients/<tenant>/worker-hosts/<host>.worker-host-manifest.yaml`,
the artifact-worker heartbeat schema and its reference publisher, and the
host-facing runbooks for Cloud PC licensing, worker-pack install, credential
auth profiles, and worker-persona credential onboarding. It SHALL pin the
compatible openxFactory contract bundle tag plus exact contract commit and
digests for the neutral contracts it consumes, and it SHALL name `openxFactory`
as the canonical owner of those contracts.

`Omnigent-Install` SHALL remain the orchestrator's install repository under its
own name and its own `repo-boundary-governance` requirement. It SHALL retain
the control-plane services, the container, compose and Kubernetes topology, the
agent and pilot flows, the intent inbox and dispatch minter, and the
`omnigent-install-manifest` realization. The split SHALL NOT rename
`Omnigent-Install`, SHALL NOT rename or re-digest the neutral
`contracts/omnigent/` contract family, and SHALL NOT alter the
`omnigent-domain-overlay` or `omnigent-install-manifest` specifications or the
per-domain `omnigent/` overlay directories that pin them.

The migration SHALL be copy-first under this capability's existing "Copy-first
migration" requirement: the worker-host paths SHALL be copied into
`OmniWorker-Install` with the proof harnesses that validate them and SHALL be
retired from `Omnigent-Install` only after every declared consumer has been
re-pinned in its own reviewed change and its validation path is green at the
new location. An active change whose declared `code_surface` consists entirely
of migrating paths SHALL be re-homed by an explicit named act — landing in the
source repository before the copy, or re-targeting to the new repository with
an amendment to its `code_surface` — and SHALL NOT arrive in the new
repository as an untracked side effect of a file copy.

`OmniWorker-Install` MUST NOT contain a model-provider credential, a runner
registration token, an enrollment lease secret, a Key Vault secret value, a
host-local service-account password, or any other credential value — each of
those is a `credential-contracts` record with declared custody, and the
repository holds only the prepared-profile and vault-reference SHAPES that
name them. It MUST NOT restate neutral contract meaning, which `openxFactory`
continues to own. It MUST NOT carry the orchestrator's control-plane services
or the governed administration workflow that the owning DomainxFactory owns.

Adding the repository to the aggregation SHALL be a separate reviewed change
that records path, remote, visibility, exact validated commit, checkout,
compatibility, update, and rollback behavior. Repository creation SHALL NOT be
treated as aggregation admission.

#### Scenario: Worker-host install repository is created

- **WHEN** this change's realization creates `opensoft/OmniWorker-Install`
- **THEN** it MUST be private and independently releasable, identify `openxFactory` as the owner of the neutral contracts it pins, and contain no credential values or key material
- **AND** the repository's README MUST state that `openxFactory` owns factory workflow policy and that `OmniWorker-Install` owns worker-host install, operations, and disaster recovery

#### Scenario: Worker-host paths are migrated out of the orchestrator repository

- **WHEN** a worker-host path is copied from `Omnigent-Install` into `OmniWorker-Install`
- **THEN** the proof harness or smoke test that validates it MUST be copied in the same change and MUST be green at the new location
- **AND** the source path MUST NOT be deleted from `Omnigent-Install` until every declared consumer has been re-pinned and verified

#### Scenario: A consumer still pins a migrated worker-host path

- **WHEN** a consumer repository names a migrating path — an aggregation submodule entry or workflow reference, a code-surface repository vocabulary, a sibling-checkout environment seam, or a derived-notebook projection
- **THEN** the consumer MUST be re-pinned to `OmniWorker-Install` in its own reviewed change before the retirement change lands
- **AND** a re-pin whose validation SKIPS when the target is absent MUST be verified by a run that does not skip, because a skipping check cannot distinguish a correct re-pin from a missing one

#### Scenario: Omnigent-Install is proposed for rename or emptying

- **WHEN** a change proposes renaming `Omnigent-Install`, retiring it, moving the control-plane services or the container, compose or Kubernetes topology out of it, or renaming the neutral `contracts/omnigent/` family or the `omnigent-domain-overlay` or `omnigent-install-manifest` specifications
- **THEN** the proposal MUST be rejected as outside the ruled scope "the worker-host product only", because `Omnigent-Install` remains the orchestrator repository under its own name

#### Scenario: Worker-host aggregation pin is proposed

- **WHEN** xFactory proposes pinning `installs/omniworker-install`
- **THEN** a dedicated reviewed change MUST define and verify gitlink path, remote, visibility, exact validated commit, checkout, compatibility, update, and rollback behavior
- **AND** the repository's own creation change MUST NOT be accepted as that record

#### Scenario: A credential value is proposed in the worker-host repository

- **WHEN** a change proposes committing a model-provider credential, a runner registration token, an enrollment lease secret, a Key Vault secret value, or a host service-account password
- **THEN** repository-boundary validation MUST reject it and route the material to a `credential-contracts` record with declared custody
