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

THE AUTHORITY IS A RECORD FACT, NOT AN ASSERTION ABOUT THE ESTATE. Each such binding SHALL declare, in its own record, the consuming system that holds it and the identity that system USES TO AUTHENTICATE to the secret store, so that which system a binding belongs to and what its revocation reaches are READ rather than inferred. A binding that declares neither is not thereby non-conforming while the declaration is optional under the contract's own migration posture, but the per-system authority it participates in is then unproven, and a change adopting this requirement SHALL NOT describe an undeclared pair as proven. THAT LAST OBLIGATION IS THE REQUIREMENT'S AND NOT A CHECKER'S: whether a document "describes a pair as proven" is a judgment over prose, so any check offered against it MUST state which shapes it actually detects and MUST NOT be described as deciding the general case.

WHAT REVOCATION REACHES, STATED HONESTLY, because a shared bearer secret bounds it. Revoking a binding stops that system's FUTURE fetches and nothing more: it cannot un-disclose a password already fetched, and it cannot terminate a session already established with it. Evicting a consumer that has already read the secret requires ROTATING it, and rotation necessarily reaches EVERY consumer of that identity — the one act per-system bindings cannot make independent. A change adopting this requirement SHALL record that cost rather than let per-system bindings read as per-system containment, and SHALL NOT claim an isolation the credential class cannot deliver. Declaring the consuming system and its fetch identity SHALL NOT be read as narrowing that limit: it makes the revocable thing nameable, not the disclosed thing recallable.

A shared ambient session SHALL NOT be used as a substitute for a second binding. This restates, for operated identities, what this capability already refuses for worker credentials: a refreshable session-state credential is the wrong class to distribute, because an ephemeral copy's refresh silently stales the master. Two systems sharing one live session is that same defect with the copy left implicit.

**Modified over `add-notebook-hosting-credential-custody`'s addition by add-binding-consumer-identity (2026-08-31):** — this change is the successor that packet named three times and could not perform itself, so the requirement it adds is restated here with the per-system authority declared in the binding's own record rather than asserted by the binding's owner and its estate wiring.

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

#### Scenario: The binding shape expresses the consuming system and its fetch identity
- **WHEN** two bindings for one operated identity are recorded in the promoted binding-template shape
- **THEN** each names the consuming system that holds it and the identity it fetches with, so the per-system authority is READ from the record rather than asserted by the binding's owner and its estate wiring
- **AND** what the record proves stays bounded: it states the declared authority, and reconciling that declaration against the store's actual grants remains a live-estate act this shape does not perform

#### Scenario: A shared session is proposed instead of a second binding
- **WHEN** a second system proposes to consume the identity through a session the first system established
- **THEN** it is refused as the wrong credential class, on the same grounds this capability already refuses distributing refreshable session state

### Requirement: A credential binding declares the consuming system that holds it and the identity it fetches with
The canonical credential schema SHALL own an ADDITIVE OPTIONAL `consumer:` block on each entry of `credential_bindings` in `xfactory_credential_binding_template`, carrying the consuming system's HOLDER REFERENCE and the FETCH IDENTITY that system USES TO AUTHENTICATE to the secret store — and the block SHALL be DECLARED AT THE INTRODUCING MINOR AND CONSTRAINED AT THE MAJOR: at the minor the schema imposes no type, no member grammar, no requiredness and no closure on it, and every one of those arrives together at the next major.

THE TWO IDENTIFIERS ARE VOCABULARY THIS FAMILY ALREADY USES, and a second naming
scheme SHALL NOT be introduced for either. The holder reference is the
`holder_ref` spelling the identity-brokering contract family already ships in its
`credential_reference` block; a consuming system SHALL NOT be spelled as a
persona or as a broker actor subject, because non-human identity is kept out of
the persona population and its authority comes from credential grants and wallet
holders instead. The fetch identity is the "fetch-identity identifier" this
capability's own promoted text already names as one of the two bindings a
consuming lane receives — the other being the opaque secret reference the shape
already carries.

THE BLOCK MAY ALSO CARRY a reference to the requirement the binding resolves, an
acknowledgment that the credential is deliberately reached by more than one
consumer, and a declaration that the record is an instantiation stub. The
acknowledgment and the stub declaration SHALL each be a DECLARED-OR-ABSENT token
whose only valid value is true, on the same reasoning this schema already applies
to issuance preconditions: a false-valued declaration reads as governance while
asserting nothing.

THE REQUIREMENT REFERENCE SHALL BE QUALIFIED, NOT A BARE IDENTIFIER, and it
SHALL take the shape the identity-brokering family already ships for this
pointer: a requirement id TOGETHER WITH the requirements document that declares
it. A bare id resolves ambiguously — this schema requires only a string `id` on a
requirement and imposes no repository-wide uniqueness, while the canonical
validator scans a whole `credentials/` tree, so one id may match records in
several documents with DIFFERENT access modes.

AND THE DOCUMENT REFERENCE SHALL CARRY A GRAMMAR AND A RESOLUTION RULE, because
the shape it borrows carries neither. In identity-brokering
`requirements_document_ref` is an unconstrained string that no script and no test
resolves; promoting it to a resolution input feeding a security precondition
without a grammar would rest that precondition on an unenforced convention —
which is the very objection this requirement raises against the map key. So:
the reference SHALL be a REPOSITORY-RELATIVE path to a YAML document, SHALL NOT
be absolute, SHALL NOT traverse upward, and SHALL NOT carry a foreign-repository
prefix; it SHALL resolve ONLY against `xfactory_credential_requirements` records
the validator itself discovered and schema-checked in the scanned tree; and the
validator SHALL NEVER OPEN A PATH TAKEN FROM A RECORD. A reference that is
ungrammatical, that names a repository other than the one under validation, or
that resolves to zero or to more than one requirement SHALL be reported and SHALL
NOT be treated as resolved.

THE PHASING IS THE VERSIONING POLICY'S RATHER THAN A PREFERENCE, AND IT COVERS
EVERY NARROWING VECTOR RATHER THAN ONE OF THEM. The binding object is OPEN on the
current major, so a `consumer:` key of any shape validates today. Three distinct
acts would each refuse a shape the current major accepts — requiring members
within the block, closing the block's member set, and imposing a grammar on the
members' values — and each is therefore the BREAKING class however additive the
new vocabulary looks. All three SHALL land together at the next MAJOR. At the
introducing minor the conformance validator SHALL emit WARNINGS instead —
naming a DISTINCT finding for EVERY shape the major will refuse, and every such
record SHALL REMAIN VALID. The set is ENUMERATED against the refusals rather than
summarised, and the enumeration is the requirement: a binding that declares no
block; a block that EXISTS but omits either identifier; a block carrying an
undeclared member; a member whose value does not match the identifier grammar; a
const-true token declared false; a `credential_bindings` MAP KEY outside the key
grammar; an `access_mode` outside the closed vocabulary; and a
`requirements_document_ref` outside the path grammar. **A WARNING SET THAT LEAVES
ANY REFUSED-AT-THE-MAJOR SHAPE UNWARNED DOES NOT SERVE THE DEPRECATION THE MAJOR
DEPENDS ON**, and the shapes that go missing are the ones no single arm happens
to look at — a block present but empty matches none of the first four, and a
constraint written on a neighbouring record matches none of them at all.

THE SAME PHASING GOVERNS EVERY NARROWING THIS CHANGE INTRODUCES, WHEREVER IT
SITS — on the block, on the map that holds the block, or on a neighbouring
record. Constraining the map key, closing `access_mode`, and constraining
`requirements_document_ref` each refuse a value the current major accepts, so
each warns at the minor and is enforced only at the major. **None is exempt for
sitting outside the block, and none is exempt for being a validator rule rather
than a schema rule**: the test is whether the current major accepts the value,
not where the refusal is written. The removal version SHALL be stated where a consumer
upgrading across it will read it, and it SHALL name EVERY act that lands there
rather than only the first.

A BLOCK-SHAPED HOLE IS NOT A FIELD, and DECLARING it is what this minor does.
The reason the block is declared rather than left to convention is that an
undeclared key on this object already validates: the binding object is not
closed, so a `consumer:` key carrying anything at all passes the pinned schema
today, unenforceable and invisible to every consumer of that contract. Declaring
it — as a named, described property of the pinned contract — gives the hole a
name, a meaning and a warning. CONSTRAINING it is the breaking half, and it waits
for the major. Closing the BINDING OBJECT around the block is a further, separate
breaking act and SHALL NOT ride either release.

A TEMPLATE IS NOT AN INSTANTIATED BINDING, AND ITS EXEMPTION SHALL BE A DECLARED
TOKEN RATHER THAN A FILENAME. An instantiation stub declares no consuming system
because none exists yet, and neither the omission warning nor the major's
requiredness SHALL apply to one. But the exemption SHALL be keyed on a
declared-or-absent const-true token IN THE RECORD, never on a `*.template.yaml`
or `*.example.yaml` path: a filename-keyed exemption is one the author writes by
naming, invisible in the bytes a pinned consumer validates, and it would let a
record carrying live values escape a required field by what it is called. The
declared token is also the only form that can reach the layer where the refusal
lands — a filename is invisible to a pinned schema, while a token is a property
the schema can condition on, so the exemption holds at the major as well as at
the minor. A stub SHALL NOT satisfy the field with a placeholder instead: a
grammar-passing sentinel reads as an authority declaration while naming nothing,
and scaffolding that manufactures conformance is worse than scaffolding that
omits it, because only the second is visible.

#### Scenario: A binding declares its consumer
- **WHEN** a credential binding declares a `consumer:` block naming a holder reference and a fetch identity
- **THEN** it validates, and which consuming system holds the binding and which identity it authenticates with are facts of the record

#### Scenario: A binding declares no consumer at the introducing minor
- **WHEN** a credential binding carries no `consumer:` block at the release that introduces it
- **THEN** it remains VALID and the validator emits a warning naming the omission and the release at which it becomes an error
- **AND** a consumer pinned at the prior bundle remains conformant without changing anything

#### Scenario: An existing record already carries a locally shaped consumer key
- **WHEN** a domain's binding already carries a `consumer:` value of its own shaping — an object with neither declared member, a scalar, or a list — written while the binding object was open
- **THEN** it stays VALID at the introducing minor and is warned rather than refused, in EVERY one of those shapes, because the schema constrains nothing about the block at that release
- **AND** the migration path is stated where a consumer upgrading across the major will read it

#### Scenario: A member's value does not match the identifier grammar, at the minor
- **WHEN** a `consumer:` block at the introducing minor carries a `holder_ref` or `fetch_identity` whose value does not match the identifier grammar
- **THEN** the record remains VALID and the validator warns, because imposing the grammar is one of the three breaking acts deferred to the major
- **AND** a release that imposed the grammar while declaring the block additive would be a narrowing wearing an additive label

#### Scenario: A consumer block is present but declares neither identifier
- **WHEN** a binding carries a `consumer:` block that exists and omits `holder_ref` or `fetch_identity`, at the introducing minor
- **THEN** it remains VALID and the validator emits its OWN warning for that shape, distinct from the no-block warning
- **AND** a warning set in which this shape matches nothing MUST be treated as incomplete, because it is refused at the major and would otherwise cross the whole minor unwarned

#### Scenario: The block is constrained at the major
- **WHEN** the major release that constrains the block is validated against
- **THEN** a `consumer:` value that is not an object, a block missing either identifier, a block carrying an undeclared member, and a member failing the identifier grammar are each an ERROR
- **AND** that release MUST have been preceded by a full minor in which every one of those produced a warning, because a required field or a narrowed shape arriving without one is a breaking change served with no deprecation

#### Scenario: A binding key does not match the grammar the lift depends on
- **WHEN** a `credential_bindings` map key does not match the identifier grammar
- **THEN** it WARNS at the introducing minor and remains VALID, and is refused only at the major — the map accepts arbitrary keys today, so constraining it is a narrowing like any other and is not exempt for sitting outside the block
- **AND** the lift's binding-link condition still holds at the minor, because it compares the reference's id to the key as a string and needs no grammar to do so

#### Scenario: A consuming system is offered as a persona
- **WHEN** a binding names its consuming system by a broker persona or actor-subject reference
- **THEN** the record is NON-CONFORMING, because a workload is not a persona and its authority comes from this capability's grants and from wallet holders
- **AND** the refusal is the REQUIREMENT'S rather than the validator's wherever the identifier's form does not distinguish the two — a check offered against this scenario MUST state which shapes it actually detects and MUST NOT be described as deciding the general case

#### Scenario: The consumer is a wallet-carrying governed actor
- **WHEN** the consuming system is a governed actor that carries a wallet
- **THEN** its wallet's identifier is an admissible holder reference and nothing further is required
- **AND** a wallet reference MUST NOT be made the required type of the field, because the wallet family is consumed here at a pin rather than owned, and most consumers of a credential binding carry no wallet

#### Scenario: A const-true token is declared false
- **WHEN** a `consumer:` block declares the shared-credential acknowledgment, or the instantiation-stub token, with the value false
- **THEN** it WARNS at the introducing minor and remains VALID, and is refused at the major — a false-valued token reads as governance while asserting nothing, but the binding object is open today so `{shared_credential_acknowledged: false}` validates on the current major and refusing it in a minor would narrow like any other act
- **AND** the lift is UNAVAILABLE to a pair carrying a false-valued acknowledgment at either release, because the lift requires the token DECLARED TRUE and a false value is not a declaration — withholding a lift is not the same act as refusing a record

#### Scenario: An instantiation stub declares itself
- **WHEN** a record that is an instantiation stub carries the const-true stub token and no identifiers
- **THEN** neither the omission warning nor the major's requiredness applies to it, and it validates at both releases
- **AND** a record carrying LIVE values MUST NOT declare the token, and a `*.template.yaml` filename alone MUST NOT exempt anything

#### Scenario: A document reference escapes the tree under validation
- **WHEN** a `requirement_ref` names a document reference that is absolute, that traverses upward, or that carries a foreign-repository prefix
- **THEN** it is ungrammatical, it is reported, and it is NOT treated as resolved
- **AND** the validator MUST NOT open the path — resolution is against records the validator itself discovered in the scanned tree, never against a path a record supplies

### Requirement: Two bindings on one secret are refused unless every pair declares distinct consumers, acknowledges the sharing, and names a requirement bound to the binding
Bindings in one credential binding template that share a `secret_ref` SHALL be REFUSED by default, and that refusal SHALL be lifted ONLY where every one of six conditions holds together, OVER EVERY PAIR that shares that reference: both bindings declare a `consumer:` block; their holder references DIFFER; their fetch identities DIFFER; both declare the shared-credential acknowledgment; both name a QUALIFIED requirement reference resolving, in the repository under validation, to EXACTLY ONE requirement whose ACCESS MODE IS A MEMBER OF THE DECLARED VOCABULARY, equal across the pair and not dispatch-only; and each reference's `requirement_id` EQUALS THE MAP KEY of the binding that carries it.

THE SIXTH CONDITION IS THE ONE THAT MAKES THE OTHER FIVE MEAN ANYTHING, and it
exists because the fifth alone is the author's own unverified word. Severing the
lift from the map key removed an unenforced convention and put nothing in its
place: the binding's author chooses which requirement the reference names, so a
pair may point both references at whichever requirement lets them through, and
the packaged negative that is this capability's only red proof of serving-tier
separation is admitted with four declarations added and its shared secret
untouched. THE REMEDY IS NOT TO TRUST THE KEY BUT TO ENFORCE IT: the schema SHALL
constrain the `credential_bindings` map key to the identifier grammar so the key
stops being a convention, and the reference SHALL be required to name the
binding it sits on. A precondition an author can satisfy by choosing where to
point is not a precondition — the same sentence this requirement already uses
against the map key, applied to its replacement. If no such binding link can be
specified, the lift SHALL NOT ship.

THE ACCESS MODE SHALL BE READABLE, AND UNREADABLE SHALL MEAN UNAVAILABLE. The
schema types the discriminator as an unconstrained string and one line of code
compares it to one exact spelling, so today an ABSENT access mode compares equal
to another absent one, and a variant spelling compares equal to itself — both
"equal, and not dispatch-only", both lifting. The schema SHALL therefore close
`access_mode` to a DECLARED VOCABULARY, and an access mode that is absent,
non-string, or outside that vocabulary on either resolved record SHALL make the
lift UNAVAILABLE rather than satisfied. This is the rule this capability's own
estate already learned from a fail-open drift check — an entry that cannot answer
the question is not a matching entry — applied to the field the lift turns on
rather than only to the reference that reaches it.

EVERY CONDITION FAILS CLOSED, and the list is the whole six rather than a sample:
an absent block, a shared holder reference, a shared fetch identity, a one-sided
or missing acknowledgment, a reference resolving to zero or to more than one
record, a reference whose id does not equal its binding's key, an ungrammatical
or escaping document reference, and an access mode that is absent, unrecognised,
mixed or dispatch-only each leave the default refusal standing. An unreadable
precondition makes the lift UNAVAILABLE and never merely UNCHECKED, because a
check that treats what it could not read as satisfied is the fail-open shape this
family has already had to repair once.

THE ARITY IS EVERY PAIR, NOT THE FIRST AGAINST THE REST. The predicate this rule
inherits keeps the FIRST binding seen for each secret reference and compares
every later one against it, so with three bindings on one secret the second and
third are never compared with each other — and a record in which those two share
a fetch identity carries the authority collapse and is accepted on both examined
pairs. The conditions above SHALL hold over EVERY PAIR sharing the reference, and
the inherited first-against-rest shape SHALL be REPLACED rather than extended.

THE FIFTH CONDITION'S ACCESS-MODE EXCLUSION OVER-REFUSES DELIBERATELY. Excluding
dispatch-only on both sides means two consumers of ONE dispatch-only credential
are refused too, which nothing else in this capability forbids. That is a chosen
conservatism, not an oversight: the dispatch class is where serving-tier
separation lives, and a rule that refuses a shape no consumer currently needs is
cheaper to relax on evidence than a rule that admits one nobody checked.
Relaxing it SHALL be a separate act carrying its own case.

A REFUSAL SHALL NAME THE FAULT IT FOUND, AND NAME IT ONCE. Two bindings whose
FETCH IDENTITIES are the same while their HOLDER REFERENCES DIFFER SHALL be
refused under a distinct finding that names two systems sharing one authority,
rather than under the finding about two credentials collapsing into one. They are
different faults with different remedies, and a reader told about the wrong one
repairs the wrong thing. Where the distinct finding applies it REPLACES the
default finding for that pair rather than accompanying it: one fault SHALL
produce one finding, or a reader repairing the named fault is left with a second
refusal describing the same record.

AND THAT FAULT IS NOT THE SHARED SECRET REFERENCE. Two different holders
declaring one fetch identity is the authority collapse WHATEVER their
`secret_ref`s, because a shared secret reference is a proxy for the rule and not
the rule; scoping the finding to a shared reference leaves the same collapse
unreported when two spellings name one secret. The finding SHALL be raised on the
holder/fetch-identity pair within one document, independently of the secret
reference. One holder reusing its own fetch identity across its own bindings is
NOT the fault and SHALL NOT be reported.

THE COMPARISON IS WITHIN ONE RECORD. These conditions are evaluated across the
bindings of a single template by a validator that reads one repository, and
SHALL NOT be claimed to compare bindings held in different repositories. Where
an operated identity's consumers are declared in separate repositories — which
the residency model makes the ordinary case — the declaration is what makes the
authority readable at each site, and reconciling the sites is an estate-level
act this requirement does not perform.

#### Scenario: Two consuming systems reach one operated identity
- **WHEN** two bindings share a `secret_ref`, declare different holder references and different fetch identities, both declare the shared-credential acknowledgment, and both name a qualified requirement whose id equals their own map key and whose access mode is the same declared non-dispatch member
- **THEN** the record validates, and it states two consumers of one deliberately shared credential rather than two credentials collapsed into one

#### Scenario: A pair points its references at a requirement neither binding is
- **WHEN** two bindings sharing a `secret_ref` name requirement references whose ids do not equal their own map keys — for instance both pointing at the content requirement so their access modes compare equal
- **THEN** the lift is UNAVAILABLE and the default refusal stands, because a condition the author satisfies by choosing where to point is no condition at all
- **AND** the packaged dispatch-versus-content negative MUST stay refused however many declarations are added to it

#### Scenario: A resolved requirement cannot answer the access-mode question
- **WHEN** a resolved requirement carries no access mode, a non-string access mode, or a spelling outside the declared vocabulary
- **THEN** the lift is UNAVAILABLE and the record is reported — never "equal, and not dispatch-only"
- **AND** two records that both cannot answer MUST NOT compare equal to each other

#### Scenario: Three bindings share one secret and two of them share an authority
- **WHEN** three bindings share a `secret_ref` and the second and third declare the same fetch identity while the first differs from both
- **THEN** the record MUST be refused, because the conditions hold over every pair and not merely over each pair containing the first binding
- **AND** an implementation carrying the inherited first-against-rest shape MUST be replaced rather than extended

#### Scenario: Two bindings on one secret share a fetch identity
- **WHEN** two bindings declare different holder references and the same fetch identity
- **THEN** they MUST be rejected under a finding naming two systems on one authority, because one identity may be shared and one authority may not
- **AND** the finding fires whether or not their `secret_ref`s are equal, and MUST NOT be the one about two credentials collapsing into one

#### Scenario: One holder reuses its fetch identity across its own bindings
- **WHEN** one holder reference declares the same fetch identity on more than one of its own bindings
- **THEN** nothing is reported, because a system legitimately authenticates as itself across the credentials it holds

#### Scenario: One binding acknowledges the sharing and the other does not
- **WHEN** two bindings share a `secret_ref` and only one declares the shared-credential acknowledgment
- **THEN** the default refusal stands, because a one-sided declaration exempts a pair on one party's word

#### Scenario: A dispatch credential and a content credential declare themselves shared
- **WHEN** two bindings share a `secret_ref` and name requirements whose access modes differ, one of them dispatch-only
- **THEN** they MUST be rejected however they are declared, because the serving tier would hold key material capable of minting a content-write token and no acknowledgment can make that intentional

#### Scenario: The requirement reference cannot be resolved
- **WHEN** two bindings share a `secret_ref` and a named requirement reference resolves to nothing in the repository under validation
- **THEN** the lift is UNAVAILABLE and the default refusal stands
- **AND** the unresolvable reference is reported rather than treated as an absent condition that happens not to fail

#### Scenario: The requirement reference resolves to more than one record
- **WHEN** a named requirement reference matches requirement records in more than one document, or more than one record in a document
- **THEN** the lift is UNAVAILABLE and the ambiguity is reported, exactly as a reference resolving to nothing is
- **AND** an implementation MUST NOT resolve the ambiguity by picking one — the two matches may carry different access modes, and a rule whose outcome depends on which was found first is not a rule

#### Scenario: A bare requirement id is offered instead of a qualified reference
- **WHEN** a `consumer:` block names a requirement by id alone, with no requirements document
- **THEN** the reference does not satisfy the lift's condition, because a bare id is not unique in the tree the validator scans

#### Scenario: Two bindings share a secret and declare nothing
- **WHEN** two bindings share a `secret_ref` and neither declares a `consumer:` block
- **THEN** the existing refusal fires exactly as it does today, because this change tightens before it lifts and nothing that is refused today becomes accepted by silence

### Requirement: A declared consumer makes access revocation readable and does not make a bearer secret unshared
A consuming system's declaration on a binding SHALL be treated as establishing WHICH ACCESS is revoked and WHOSE FUTURE FETCHES stop, and SHALL NOT be treated as establishing containment of a credential a consumer has already obtained.

WHAT IT BUYS, precisely. With the consuming system and its fetch identity on the
record, an eviction decision resolves to a named grant at the secret store, its
effect is bounded to one consumer's future fetches, and the store's access log
becomes reconcilable against a declaration rather than against an assumption.
Before it, the same decision is an inference from estate wiring that no record
carries.

WHAT IT DOES NOT BUY, and this SHALL be stated by any change or document that
adopts the field. The credential is a shared BEARER secret. Revoking a fetch
identity's grant cannot un-disclose a value already read, cannot end a session
already established with it, and cannot prevent a consumer that copied it from
continuing to use it elsewhere. Evicting such a consumer still requires
ROTATION, and rotation still reaches every consumer of the identity. A record
that names consumers describes the authority structure; it does not change the
credential class.

THE FIELD SHALL NOT BE OFFERED AS EVIDENCE OF AN ENFORCED GRANT. A declared
fetch identity states what the binding's owner says the store's grant is. Where
the declaration and the store disagree, the store governs, and detecting that
disagreement is a live-estate reconciliation with its own home — the same
posture this family already takes for observed-versus-declared identity drift.

AND WHAT IT PUBLISHES SHALL BE STATED, because the reach is honest in one
direction only until it is. The binding already carries the vault, the secret
reference and the owner; this block adds the principal that can fetch that secret
and the system that holds it, IN THE SAME OBJECT. The defensive gain and the
exposure are the same fact read from two sides: for an operator, "which grant do
I revoke" becomes a lookup rather than an inference — and for anyone who can read
the record, so does "which principal reaches this secret". That is not
speculative; the family this vocabulary is borrowed from already publishes live
estate principal names in its packaged, digest-pinned examples. At the major the
declaration becomes REQUIRED, so the disclosure stops being opt-in and becomes
estate-wide. The disclosure is worth accepting and the residency model bounds it
by keeping instance records in the consuming installs — but it SHALL be stated
rather than omitted, and a packaged fixture SHALL carry SYNTHETIC identifiers and
SHALL NOT carry a live fetch identity merely because a live one would be more
illustrative.

#### Scenario: A consumer must be denied further access
- **WHEN** an operator must stop one consuming system fetching a shared operated identity's credential
- **THEN** the binding's declared fetch identity names the grant to revoke and the revocation's reach is bounded to that consumer's future fetches
- **AND** the other consumers' bindings are undisturbed

#### Scenario: A consumer that already holds the secret must be evicted
- **WHEN** the consumer to be evicted has already fetched the credential or established a session with it
- **THEN** revocation is insufficient and the credential is rotated, reaching every consumer
- **AND** the declared consumer field MUST NOT be presented as having made that eviction independent

#### Scenario: The declaration and the store disagree
- **WHEN** a binding declares a fetch identity that holds no matching grant at the secret store, or the store grants access to an identity no binding declares
- **THEN** the store's actual grants govern, and the divergence is a reconciliation finding rather than a validation pass
- **AND** the schema-level check MUST NOT be described as having verified the grant

#### Scenario: The record is read by someone who should not reach the secret
- **WHEN** a binding declares a fetch identity beside its vault and secret reference
- **THEN** the record publishes, in one object, which principal reaches which secret — and an adopting change SHALL record that as a consequence of the declaration rather than describing only the revocation gain
- **AND** at the major, where the declaration is required, that publication is estate-wide rather than per-record

#### Scenario: A packaged fixture is offered a live fetch identity
- **WHEN** a fixture destined for the packaged, digest-pinned corpus would name a live install's fetch identity or holder reference
- **THEN** it SHALL use a SYNTHETIC value instead, because the corpus is distributed to every consumer that pins the contract and illustrative realism is not a reason to widen a disclosure
- **AND** the live identifiers remain in the consuming installs' own credential trees, where the residency model already places an estate fact and where the readership is the install's rather than every pinning consumer

#### Scenario: An adopting document describes the field
- **WHEN** a change, runbook or contract document adopts the consumer field
- **THEN** it states all three halves — revocation of access becomes readable, a bearer secret already fetched stays shared until rotation, and the record now publishes which principal reaches which secret
- **AND** a description carrying only the first is non-conforming, because the omission is what turns a readability gain into a containment claim
- **AND** THIS OBLIGATION IS THE REQUIREMENT'S RATHER THAN A CHECKER'S — whether arbitrary prose "states all three" is a judgment over unbounded document space, so any check offered against this scenario MUST state which shapes it actually detects and MUST NOT be described as deciding the general case

