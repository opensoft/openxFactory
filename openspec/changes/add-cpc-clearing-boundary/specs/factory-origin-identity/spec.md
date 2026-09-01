# factory-origin-identity — Spec Delta

## ADDED Requirements

### Requirement: A factory's origin identity is one registered key per originating factory
Each ORIGINATING FACTORY authorized to submit sealed bounded requests SHALL hold exactly ONE origin identity — a single Ed25519 key pair — and its PUBLIC half SHALL be registered in a neutral FACTORY-IDENTITY REGISTER held in this repository. The register SHALL be a SIBLING of the review-authority intake register, not an extension of it: a separate register file with its own rows, its own reader invocation, and its own staleness bound. The register SHALL record, per factory, the factory's holder reference, its wallet reference, the act the key is registered for, the grant backing it, an expiry, and the row state. A factory with no registered origin identity SHALL be unable to clear a sealed bounded request.

#### Scenario: A factory is admitted as an originator
- **WHEN** a factory is authorized to originate cross-boundary work
- **THEN** exactly one origin key is registered for it in the factory-identity register, public half only
- **AND** the row names the holder, wallet, act, grant, expiry, and state

#### Scenario: A second origin key is added for the same factory
- **WHEN** a second concurrently active origin row is proposed for one factory
- **THEN** it MUST be refused — one factory, one origin identity — and key rotation proceeds by superseding the existing row, not by holding two

#### Scenario: An unregistered factory submits a request
- **WHEN** a sealed bounded request names an originating factory with no active row in the register
- **THEN** clearing refuses the request

### Requirement: The register holds public key references only, never private key material
The factory-identity register and every record beside it SHALL hold KEY REFERENCES only — a public key and its algorithm, the custody model, and the grant that confers authority — and MUST NOT contain a private key, a seed, a passphrase, a secret name resolvable to key material, or any credential value. Origin key records SHALL reuse the pinned neutral wallet-record and grant shapes rather than inventing a second key vocabulary, and the register file itself SHALL follow the intake register's established discipline for this family.

#### Scenario: Key material is proposed for the register
- **WHEN** any record under the factory-identity register would carry a private key, seed, or credential value
- **THEN** it MUST be refused

#### Scenario: An origin key record is read
- **WHEN** an origin key record is inspected
- **THEN** it carries the public key, its algorithm, the declared custody model, and the grant reference
- **AND** possession of the record confers no ability to sign

### Requirement: The origin key private half is custodied in the factory's hosted environment and declared
The PRIVATE half of a factory's origin key SHALL live only in that factory's own HOSTED packaging environment — the environment its hosted packaging workflow runs in — and its CUSTODY MODEL SHALL be declared from the closed custody registry, exactly as wallet custody is declared for review authority. The private half MUST NOT be placed on any execution target, any workstation, any shared runner, or in any bundle. An origin key whose custody is undeclared or unattested SHALL be capped at the lower authority the custody vocabulary assigns to unattested custody, and MUST NOT be treated as evidence that the factory itself acted.

#### Scenario: An origin key is proposed for a runner
- **WHEN** a design would place an origin private key on an execution target so bundles can be signed where they are staged
- **THEN** it MUST be refused — origin signing happens in the factory's hosted environment or not at all

#### Scenario: Custody is undeclared
- **WHEN** an origin key record declares no custody model, or declares one with no attestation beside it
- **THEN** the row is capped at the lower authority the custody vocabulary assigns
- **AND** the cap is a contract outcome, not a finding to be waived

#### Scenario: Custody is declared and attested
- **WHEN** an origin key's custody model is declared from the closed registry and attested
- **THEN** an origin signature from that key evidences that the factory's hosted environment acted

### Requirement: Origin attestation and review attestation are distinct keys and distinct acts
An ORIGIN attestation ("this bounded request came from factory X") and a REVIEW or SEAT attestation ("this reviewer or seat rendered this verdict") SHALL be distinct ACTS carried by distinct KEYS in distinct registers. A key registered for the origin act SHALL be REFUSED when presented for a review or seat act, and a key registered for a review or seat act SHALL be REFUSED when presented for the origin act, whatever else about the presentation verifies. Cross-register satisfaction SHALL NOT be possible: a reader for one act MUST NOT resolve identities from the other act's register.

#### Scenario: An origin key is presented as review authority
- **WHEN** a verdict or review exercise presents a key whose registration is an origin identity
- **THEN** the exercise is refused, and the refusal names the act mismatch — not a missing-key error

#### Scenario: A seat key signs a bounded request manifest
- **WHEN** a sealed bounded request carries an origin signature made with a key registered for a seat or review act
- **THEN** clearing refuses the request

#### Scenario: One factory holds both kinds of key
- **WHEN** a factory legitimately holds an origin key and also holds seat or review keys
- **THEN** they remain separate key pairs with separate registrations, separate custody declarations, and separate revocation

### Requirement: Origin identities revoke under the ratified revocation lifecycle and are re-checked at exercise
An origin identity SHALL revoke under the ratified wallet revocation lifecycle: revocation propagates through the derivation chain at the moment it is taken rather than waiting for expiry; a revoked identity never returns to active, and resumption is a NEW registration naming what it supersedes; the reason class is recorded but never narrows propagation. Revocation SHALL be re-checked AT EXERCISE — at the moment a sealed bounded request is cleared — and never trusted from an admission stamp. Expiry SHALL be judged by computed time against the recorded expiry, and a row's own state field SHALL NOT be trusted as truth about expiry. A register or projection that is unreadable, unparseable, or staler than the declared staleness bound SHALL cause clearing to REFUSE, never to proceed.

#### Scenario: A factory's origin key is revoked mid-flight
- **WHEN** an origin identity is revoked after a bundle was packaged but before it is cleared
- **THEN** clearing refuses the request — revocation is checked at clearing, not at packaging

#### Scenario: The register projection is stale
- **WHEN** the projection the clearing boundary resolves against is older than the declared staleness bound, unreadable, or absent
- **THEN** clearing refuses every request rather than admitting on a stale view
- **AND** an unreachable store and an absent store are diagnosed distinctly, though both refuse

#### Scenario: A revoked identity is reinstated
- **WHEN** a factory whose origin identity was revoked is to originate again
- **THEN** a NEW origin identity is registered naming the row it supersedes — the revoked row never returns to active

### Requirement: The clearing boundary verifies origin signatures against the register, never instead of platform provenance
The clearing boundary SHALL verify a sealed bounded request's ORIGIN SIGNATURE against the public key registered for that factory in the factory-identity register — or against an operator-established PROJECTION of that register whose staleness is bounded — and this verification SHALL be conjunctive with, and never a substitute for, verification of the request's provenance against the hosting platform's authoritative API. The signature SHALL cover the manifest, including the bundle digest, so that neither the manifest nor the bundle can be altered after signing without detection.

#### Scenario: A signature covers only part of the manifest
- **WHEN** an origin signature does not cover the whole manifest including the bundle digest
- **THEN** clearing refuses the request

#### Scenario: A manifest is altered after signing
- **WHEN** any manifest field or the bundle digest differs from what the origin signature covers
- **THEN** verification fails and clearing refuses

#### Scenario: Both checks pass
- **WHEN** the origin signature verifies against the registered public key AND the platform API confirms the originating repository, workflow, and run
- **THEN** the origin verification requirement is satisfied
- **AND** neither check alone would have satisfied it

### Requirement: The factory-identity register is a permanently human-only governance surface
The factory-identity register and the records beside it SHALL be a PERMANENTLY HUMAN-ONLY surface: no autonomous or council-cleared approval SHALL ever land a change to them, and where gate rules enumerate never-clearable floor members, the register SHALL be entered BY NAME rather than inferred from any path-shaped clause. Admitting a factory as an originator, rotating its origin key, and revoking it are human acts, each anchored to an accountable operator through the grant that confers the authority.

#### Scenario: An autonomous approval targets the register
- **WHEN** a candidate that edits the factory-identity register reaches an autonomous or council-cleared approval path
- **THEN** it MUST be refused, and the refusal MUST come from a by-name floor entry, not from a path pattern

#### Scenario: A factory is admitted
- **WHEN** a new originating factory is registered
- **THEN** a human operator issues the backing grant and is named as its issuer
- **AND** the admission is traceable to that accountable human
