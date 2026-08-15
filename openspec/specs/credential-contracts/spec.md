# credential-contracts Specification

## Purpose

Define the canonical shapes of the five credential contract record kinds,
domain content locality, and grant accountability requirements.
## Requirements
### Requirement: Canonical credential record shapes
Credential contract records SHALL validate against the canonical
`contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns
the five record kinds: `xfactory_credential_requirements`,
`xfactory_runtime_capability_grant_template`,
`xfactory_credential_binding_template`,
`xfactory_credential_broker_contract`, and
`xfactory_credential_audit_policy`. Domain content — credential families,
scopes, providers, workflow and action names — is domain-local; the schema
constrains shape only, and semantic invariants remain owned by the
credential access model.

#### Scenario: A domain authors a credential contract
- **WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds
- **THEN** it MUST validate against the pinned canonical schema

#### Scenario: A file lacks the envelope
- **WHEN** a credentials file has no `kind`
- **THEN** the validator MUST report an error

#### Scenario: A domain policy record is present
- **WHEN** a credentials file carries a kind outside the five contract kinds
- **THEN** the validator MUST skip it with notice — such kinds are candidates for future promotion, not silent failures

### Requirement: Grant shape neutrality
The runtime capability grant SHALL express scope through neutral references
(job, domain, requirement, client, customer, allowed workflows and actions,
expiry, audit) and SHALL NOT require any single domain's nouns; a grant
without issuer, approver, expiry, and audit reference is invalid.

#### Scenario: A grant omits accountability fields
- **WHEN** a grant template lacks `issued_by`, `approved_by`, `expires_at`, or `audit_ref`
- **THEN** the validator MUST report an error

#### Scenario: Another domain issues grants
- **WHEN** a non-operations domain defines grant templates for its credential families
- **THEN** the same canonical shape applies with that domain's content

### Requirement: SOPS ciphertext repository pattern
A SOPS document with AES-256-GCM-encrypted credential leaves SHALL NOT be classified as a raw credential, and SOPS plus an
externally custodied decryption identity SHALL be an approved
secret-provider pattern, only while every one of the following controls
holds: the repository stores only ciphertext, non-secret object metadata,
SOPS integrity metadata and MAC, and public recipients; the private
decryption identity lives durably only in an approved secret provider and
is projected separately into the runtime decryption controller; recipients
are unique per environment or stronger trust boundary; repository policy
rejects plaintext secret values and private decryption identities before
commit; a compromise of the decryption controller is treated as a
compromise of every secret that controller can decrypt; and an exposed
decryption identity triggers rotation of both the identity and every
credential encrypted to it, because historical git ciphertext remains
recoverable with the exposed identity. Base64 encoding, ad hoc encryption
without SOPS integrity metadata, a private decryption identity present in
any repository, and any value decryptable without the approved external
identity remain raw credentials and stay prohibited.

#### Scenario: A compliant SOPS-encrypted secret is committed
- **WHEN** a repository commits a secret manifest whose secret-bearing leaves are SOPS AES-256-GCM ciphertext, only public recipients are committed, and the private identity is custodied in an approved secret provider
- **THEN** the commit does not violate the no-raw-credentials core rule

#### Scenario: A plaintext or trivially encoded secret is committed
- **WHEN** a commit introduces a secret value in plaintext or bare base64, or introduces a private decryption identity
- **THEN** repository policy MUST reject it as a raw credential

#### Scenario: A decryption identity is exposed
- **WHEN** a private decryption identity is exposed outside its approved custody
- **THEN** the identity MUST be rotated
- **AND** every credential encrypted to it MUST be rotated, because historical ciphertext in git remains recoverable

#### Scenario: A recipient is reused across environments
- **WHEN** a deployment proposes encrypting one environment's secrets to another environment's recipient
- **THEN** the binding MUST be rejected; recipients are per-environment or per stronger trust boundary

### Requirement: Worker credentials are distributed by reference into ephemeral job scope

A credential consumed by a worker lane (a model-provider token or comparable worker-consumed secret) SHALL be distributed by reference: the secret is held in a vault as a LONG-LIVED, NON-ROTATING headless token, the lane fetches it per job using the runner's own federated workload identity, and the fetched value lives only in ephemeral job scope (environment plus a per-job configuration directory) — never written to host state, never persisted past the job. Rotation SHALL be a vault write (effective the next job, no host administration), the vault's access log SHALL serve as the per-fetch audit record, and a refreshable session-state credential (one its consumer rewrites in place) SHALL NOT be distributed by any channel: it is the wrong class, because an ephemeral copy's refresh silently stales the master. Where a per-install fetch identity does not yet exist, service-scoped materialization of the same non-rotating class into the same ephemeral job scope is a permitted degraded mode whose rotation cost (host administration) SHALL be recorded as a gap.

#### Scenario: Rotation is one vault write

- **WHEN** the operator writes a new token version to the vault secret
- **THEN** the next job's fetch consumes the new version with no host access, no service restart, and no lane change

#### Scenario: The session-file class is refused distribution

- **WHEN** a refreshable session-state credential is proposed for vault distribution or per-job copying
- **THEN** it is non-conforming — the conforming distribution is a non-rotating headless token, and the session file remains at most host-profile state

#### Scenario: Host state stays clean

- **WHEN** a worker job that fetched its credential completes or crashes
- **THEN** no credential material persists outside the discarded job scope, and a stale host-profile credential cannot affect the lane

#### Scenario: The degraded mode is permitted and recorded

- **WHEN** an install has no per-job fetch identity and materializes the token at service scope instead
- **THEN** the lane conforms (same secret class, same ephemeral job consumption) and the install records rotation-requires-host-administration as an open gap

### Requirement: The credential vault operator is an execution binding, never contract content

Who operates the worker-credential vault SHALL be a per-install execution binding following the client-infrastructure operating models — the operations factory where one is licensed, the client's own authorized IT channel where not — and the consuming lane SHALL be identical in both cases, receiving only bindings: an opaque secret reference and a fetch-identity identifier. Contract artifacts, lane definitions, and domain repositories SHALL NOT hard-code a vault operator, a vault product, or any secret value, and the bootstrap material for this pattern SHALL be reachable by a client licensing a single domain factory without the operations factory.

#### Scenario: An operations-factory-operated install

- **WHEN** the install's execution binding is operations-factory-executed
- **THEN** that factory operates the vault, mints and rotates the token, and grants the fetch identity read on exactly the lane's secret — and the lane consumes bindings only

#### Scenario: A client-operated install

- **WHEN** the client licenses the domain factory without an operations factory
- **THEN** the client's authorized IT channel operates a vault of its choice under the same contract, no licensor identity performs the privileged acts, and the identical lane consumes the client's bindings

### Requirement: Dispatch-only credential least privilege and serving-tier separation
A dispatch-only credential — one that exists to TRIGGER execution (a workflow dispatch or job kickoff) — SHALL be scoped to exactly the minimal permission required to trigger its one named target and nothing more (for a GitHub-hosted factory, `actions: write` on the single repository that owns the workflow), carrying no repository-contents authority. It SHALL be a DISTINCT binding from any content-write credential the same capability uses, and a zero-write-authority serving surface holding a dispatch-only credential MUST NOT hold — nor hold key material capable of minting — a content-write credential.

#### Scenario: A dispatch credential requests contents authority
- **WHEN** a dispatch-only credential requirement or binding grants repository-contents write, or any scope beyond triggering its one named target
- **THEN** the validator MUST report an error

#### Scenario: A dispatch credential reuses the content credential's identity
- **WHEN** a dispatch binding names the same App or key identity as a content-write binding
- **THEN** it MUST be rejected, because the serving tier would then hold key material capable of minting a content-write token

#### Scenario: A correctly separated dispatch credential
- **WHEN** a dispatch-only credential is scoped to trigger exactly one named workflow on one repository, held as a binding distinct from the content-write credential
- **THEN** it is valid

### Requirement: Reference-delivered credential with operator-as-binding
A runtime credential an install materializes SHALL be delivered BY REFERENCE — a
vault URI plus the runtime's own fetch identity — and materialized EPHEMERALLY,
named at call time and never baked into an image, committed config, or log. The
vault OPERATOR SHALL be a per-install execution binding rather than a fixed
party: the licensed operator when the tenant licenses one (for example
OpsxFactory), or the client's own IT channel when self-hosted, where no
operator-domain identity performs the privileged change. The neutral contract —
reference shape, fetch-identity requirement, ephemeral materialization, and
audit-by-vault-log — SHALL live in openxFactory and MUST NOT be an
operator-domain capability, so a domain licensed WITHOUT the operator can still
realize it; the serving and lane code SHALL be identical across bindings, with
the vault URI and fetch identity riding as bindings.

#### Scenario: A credential value is baked into an image or config
- **WHEN** a credential contract materializes a secret value into a container image, committed config, or log instead of by vault reference at call time
- **THEN** repository policy MUST reject it

#### Scenario: The operator is fixed to one domain
- **WHEN** a credential contract requires a specific operator domain as the only permissible vault operator
- **THEN** it MUST be rejected, because the operator is a per-install binding and a self-hosted client's IT channel is an equally valid operator

#### Scenario: The neutral contract is authored in an operator domain
- **WHEN** the reference-delivery credential contract is authored in an operator DomainxFactory rather than openxFactory
- **THEN** it MUST be relocated to openxFactory, so a domain licensed without the operator still reaches the contract

