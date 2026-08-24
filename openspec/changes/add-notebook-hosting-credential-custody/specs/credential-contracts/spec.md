# credential-contracts (delta) — add-notebook-hosting-credential-custody

## ADDED Requirements

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

Per-system bindings are what make the consequential acts separable. With one shared route, revoking either system's access revokes both, the store's access log cannot say which system read the secret, and a compromise of one is indistinguishable from a compromise of the other. Separate bindings SHALL be revocable independently, and revoking one SHALL NOT disturb the other.

A shared ambient session SHALL NOT be used as a substitute for a second binding. This restates, for operated identities, what this capability already refuses for worker credentials: a refreshable session-state credential is the wrong class to distribute, because an ephemeral copy's refresh silently stales the master. Two systems sharing one live session is that same defect with the copy left implicit.

#### Scenario: A second system needs the same identity
- **WHEN** a second system must authenticate as an operated identity a first system already uses
- **THEN** it is given its own binding — its own access identity, grant, rotation visibility and audit trail
- **AND** it does not reuse the first system's binding or its established session

#### Scenario: One system's access is revoked
- **WHEN** one consuming system's access to the operated identity is revoked
- **THEN** the other system's binding is unaffected and its lane keeps working
- **AND** the revocation is attributable to exactly one system

#### Scenario: The access log is asked which system read the secret
- **WHEN** the secret store's access log is examined after a fetch
- **THEN** it names which consuming system's identity performed it, because each has its own

#### Scenario: A shared session is proposed instead of a second binding
- **WHEN** a second system proposes to consume the identity through a session the first system established
- **THEN** it is refused as the wrong credential class, on the same grounds this capability already refuses distributing refreshable session state
