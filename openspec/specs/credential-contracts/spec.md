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
The schema SHALL additionally own an `issuance_preconditions` vocabulary: a
CLOSED set of neutral precondition tokens that a credential requirement
record MAY declare, each naming a governed condition which must hold before a
grant is issued against that requirement. Its first member is the
ROSTER-DRIFT precondition — an open drift finding recorded against the roster
entry covering the identity a grant would name blocks issuance of that grant.
Declaring a precondition is optional and additive; declaring a member outside
the vocabulary is invalid, because a free-text precondition riding a schema
that neither declares nor forbids it is unenforceable and invisible to every
consumer of the pinned contract. Precondition EVALUATION — which drift
records exist and who reads them — stays with the owning contract families
and the domain mint surface that issues the grant; this schema owns the
vocabulary and the declaration shape only.

#### Scenario: A domain authors a credential contract
- **WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds
- **THEN** it MUST validate against the pinned canonical schema

#### Scenario: A file lacks the envelope
- **WHEN** a credentials file has no `kind`
- **THEN** the validator MUST report an error

#### Scenario: A domain policy record is present
- **WHEN** a credentials file carries a kind outside the five contract kinds
- **THEN** the validator MUST skip it with notice — such kinds are candidates for future promotion, not silent failures

#### Scenario: A requirement record declares the roster-drift precondition
- **WHEN** a credential requirement record declares the roster-drift member of `issuance_preconditions`
- **THEN** it validates, and the declaration is the neutral expression of the ratified refusal: an open drift finding on the covering roster entry blocks issuance of a grant naming that identity
- **AND** a requirement record declaring no preconditions remains valid, because the vocabulary is optional and additive

#### Scenario: A precondition outside the vocabulary
- **WHEN** a requirement record declares an `issuance_preconditions` member that is not in the closed vocabulary
- **THEN** the validator MUST report an error naming the closed vocabulary rather than accepting an unenforceable free-text condition

#### Scenario: The neutral layer proves the precondition by fixture
- **WHEN** the neutral realization of the roster-drift precondition is demonstrated
- **THEN** the demonstration is a conformant requirement-record fixture declaring it, because the neutral layer holds no producer of live drift findings and issues no grant itself
- **AND** at this capability's modification no live drift producer existed anywhere in the family, so the fixture is the whole neutral criterion and live refuse-then-allow behaviour is proven at the domain mint surface as a follow-up

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

### Requirement: An operated identity's credential is held in governed custody and reached only by reference
Where the family stands up an OPERATED IDENTITY on a third-party platform, the credential that authenticates it SHALL be held in a governed secret store and SHALL be reached only BY REFERENCE — an opaque secret reference resolved through a binding, never a value carried in a repository, an environment baked into an image, a person's password manager, or a human's memory alone. The existing prohibition on hard-coding an operated identity's credential states what must not happen; this states what must: an operated identity with no declared custody is not governed, it is merely undocumented.

Custody SHALL cover every secret the identity actually needs to authenticate, not the primary factor alone. Where the platform enforces a second factor, that factor's seed is part of the credential set and SHALL be held under the same custody: a password in a vault beside a TOTP seed on someone's phone is a single point of failure wearing governance.

The binding SHALL name the provider, the secret reference, the owner and the rotation policy, following the credential binding-template shape this capability already promotes. Naming a concrete vault and secret in a per-client BINDING INSTANCE is what a binding is for and does not breach the no-hard-coding rule, which binds contract artifacts, lane definitions and domain repositories — the neutral obligation lives in the contract, the concrete estate fact lives in the binding.

Custody SHALL NOT be claimed to deliver automation. Holding a password governs WHO MAY OBTAIN IT and proves who did; it does not by itself make an interactive sign-in unattended, and a custody record MUST NOT be read as evidence that an automated login exists.

#### Scenario: An operated identity is stood up with no declared custody
- **WHEN** an install declares an operated identity whose credential is held in no governed store
- **THEN** the identity is non-conforming — its credential is undocumented rather than governed
- **AND** the remedy is a custody binding, not a note recording where the password is kept

#### Scenario: A second factor is left outside custody
- **WHEN** the platform requires a second factor for the operated identity and only the primary credential is held under custody
- **THEN** the custody is incomplete, because the identity still cannot be authenticated from governed material alone

#### Scenario: A binding names the concrete vault
- **WHEN** a per-client binding instance names its provider, vault, secret reference, owner and rotation policy
- **THEN** that is conforming: the binding is exactly where a concrete estate fact belongs
- **AND** the same values appearing in a contract artifact or lane definition would not be

#### Scenario: Custody is mistaken for automation
- **WHEN** a custody record exists for an identity whose sign-in is an interactive browser flow
- **THEN** the sign-in remains interactive, and any claim that the credential's custody automates it is refused

### Requirement: Each consuming system reaches a shared operated identity through its own binding
Where more than one system authenticates as the SAME operated identity, each consuming system SHALL reach that identity's credential through its OWN binding: its own access identity against the secret store, its own grant, its own rotation visibility, and its own audit trail. One identity MAY be shared; one AUTHORITY SHALL NOT. A system SHALL NOT borrow another system's binding, and SHALL NOT consume the identity through a session another system established.

Per-system bindings are what make the consequential acts separable. With one shared route, revoking either system's access revokes both, the store's access log cannot say which system read the secret, and a compromise of one is indistinguishable from a compromise of the other. Each binding SHALL therefore be revocable on its own, and revoking one SHALL NOT disturb the other's ability to fetch.

WHAT REVOCATION REACHES, STATED HONESTLY, because a shared bearer secret bounds it. Revoking a binding stops that system's FUTURE fetches and nothing more: it cannot un-disclose a password already fetched, and it cannot terminate a session already established with it. Evicting a consumer that has already read the secret requires ROTATING it, and rotation necessarily reaches EVERY consumer of that identity — the one act per-system bindings cannot make independent. A change adopting this requirement SHALL record that cost rather than let per-system bindings read as per-system containment, and SHALL NOT claim an isolation the credential class cannot deliver.

A shared ambient session SHALL NOT be used as a substitute for a second binding. This restates, for operated identities, what this capability already refuses for worker credentials: a refreshable session-state credential is the wrong class to distribute, because an ephemeral copy's refresh silently stales the master. Two systems sharing one live session is that same defect with the copy left implicit.

#### Scenario: A second system needs the same identity
- **WHEN** a second system must authenticate as an operated identity a first system already uses
- **THEN** it is given its own binding — its own access identity, grant, rotation visibility and audit trail
- **AND** it does not reuse the first system's binding or its established session

#### Scenario: One system's access is revoked
- **WHEN** one consuming system's binding is revoked
- **THEN** that system can no longer FETCH the credential, the other system's binding is unaffected, and its lane keeps working
- **AND** the revocation is attributable to exactly one system

#### Scenario: A consumer that already holds the secret must be evicted
- **WHEN** a consuming system has already fetched the shared credential, or already established a session with it, and must be evicted
- **THEN** revoking its binding is insufficient — the credential is rotated, and the rotation reaches every consumer of that identity
- **AND** that shared cost is recorded rather than described as independent revocation

#### Scenario: The access log is asked which system read the secret
- **WHEN** the secret store's access log is examined after a fetch
- **THEN** it names which consuming system's identity performed it, because each has its own

#### Scenario: The published binding shape cannot yet express the access identity
- **WHEN** two bindings for one operated identity are recorded in the promoted binding-template shape
- **THEN** the shape carries no consumer or access-identity field, so the per-system authority is asserted by the binding's owner and its estate wiring rather than proven by the record
- **AND** the gap is recorded as owed to a successor that extends the shape, not left implied as enforced

#### Scenario: A shared session is proposed instead of a second binding
- **WHEN** a second system proposes to consume the identity through a session the first system established
- **THEN** it is refused as the wrong credential class, on the same grounds this capability already refuses distributing refreshable session state

