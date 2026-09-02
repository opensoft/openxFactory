# factory-origin-identity — Spec Delta

## ADDED Requirements

### Requirement: One registered origin identity per originating repository, in a sibling register
An originating repository authorized to present sealed bounded requests SHALL hold exactly ONE origin identity — a single Ed25519 key pair — whose PUBLIC half is registered in a neutral FACTORY-IDENTITY REGISTER at `governance/factory-identity/`. That register SHALL be a SIBLING of the review-authority intake register and SHALL NOT be an extension of it: a separate register file, its own rows, its own reader invocation, and its own declared staleness bound. Each row SHALL name the holder, the wallet reference, the act, the grant conferring it, an expiry, and the row state. Two concurrently active origin rows for one originating repository SHALL be refused; rotation supersedes a row rather than adding a second.

The register SHALL declare its holders with `holder_class: organisation`, and SHALL NOT adopt the seat-council holder spelling, the agent-holder prefix, or the per-seat key-block shape that the review-authority register uses for council seats — an originating repository is an organisation holder, not a seated agent, and inheriting a seat vocabulary would make every conformant origin row fail a rule written for a different subject.

#### Scenario: An originating repository is admitted
- **WHEN** a repository is authorized to present sealed bounded requests
- **THEN** exactly one origin row is registered for it, carrying the public half only
- **AND** the row names holder, wallet, act, grant, expiry, and state

#### Scenario: A second concurrent origin row is proposed
- **WHEN** a second active origin row is proposed for one originating repository
- **THEN** it MUST be refused
- **AND** rotation MUST proceed by superseding the existing row

#### Scenario: The seat-council spelling is applied to an origin row
- **WHEN** an origin row is written with a seated-agent holder spelling or a per-seat key-block shape
- **THEN** it MUST be refused as a misfiled row
- **AND** the register's holder class MUST be `organisation`

### Requirement: The register holds public key references only
The factory-identity register and every record beside it SHALL hold KEY REFERENCES only — a public key with its algorithm, a decentralized identifier, a key id, the declared custody model, and the grant that confers authority — and SHALL NOT contain a private key, a seed, a passphrase, a secret name resolvable to key material, or any credential value. Origin records SHALL reuse the pinned neutral wallet-record and grant vocabulary rather than defining a second key vocabulary.

#### Scenario: Key material is proposed for the register
- **WHEN** any record under `governance/factory-identity/` would carry a private key, seed, or credential value
- **THEN** it MUST be refused

#### Scenario: An origin record is read
- **WHEN** an origin record is inspected
- **THEN** it carries the public key, its algorithm, the identifier, the custody model, and the grant reference
- **AND** possession of the record MUST confer no ability to sign

### Requirement: The origin private half is custodied in the originating repository's hosted environment
The PRIVATE half of an origin key SHALL exist only in the originating repository's own HOSTED PACKAGING ENVIRONMENT, and its CUSTODY MODEL SHALL be declared from the closed custody registry. It SHALL NOT be placed on a governed execution host, a workstation, a shared runner, or in any bundle. An origin key whose custody is undeclared or unattested SHALL be capped at the lower authority the custody vocabulary assigns to unattested custody, and SHALL NOT be read as evidence that the originating repository itself acted.

#### Scenario: An origin key is proposed for a host
- **WHEN** a design would place an origin private key on a governed execution host so bundles can be signed where they are staged
- **THEN** it MUST be refused

#### Scenario: Custody is undeclared
- **WHEN** an origin record declares no custody model, or declares one with no attestation beside it
- **THEN** the row MUST be capped at the lower authority the custody vocabulary assigns

#### Scenario: Custody is declared and attested
- **WHEN** an origin key's custody model is declared from the closed registry and attested
- **THEN** a verifying origin signature evidences that the originating repository's hosted environment acted

### Requirement: The two registers share no key, and that disjointness is checked
The origin act and the review or seat act SHALL be distinct acts carried by distinct keys in distinct registers, and the ENFORCEABLE HALF OF THAT DISTINCTNESS SHALL BE A CHECKED DISJOINTNESS RULE: a validator SHALL assert that no `key_id`, no decentralized identifier, and no public-key fingerprint appears in both the factory-identity register family and the review-authority register family, and SHALL fail when one does. Disjointness is asserted over the RECORDS, because that is enforceable today by reading two trees.

A REFUSAL AT READ TIME — an origin-registered key presented for a review act being rejected by the review reader, and the converse — SHALL be a FURTHER obligation that is NOT satisfied by this requirement and SHALL NOT be claimed as in force until the reader that resolves review authority is changed to scope its wallet and grant resolution to its own register. That reader is pinned vocabulary owned outside this repository, and until it is scoped, an origin wallet record placed in a sibling tree is resolvable BY IT: the fail-open direction SHALL be stated here rather than papered over, and the disjointness rule above is what holds the line meanwhile.

#### Scenario: One key id appears in both register families
- **WHEN** a `key_id`, identifier, or public-key fingerprint appears in both the factory-identity and review-authority record trees
- **THEN** the validator MUST fail and name the shared value
- **AND** the condition MUST NOT be waivable by declaring different acts on the two rows

#### Scenario: The two families are disjoint
- **WHEN** no identifier is shared between the two register families
- **THEN** the disjointness rule MUST pass

#### Scenario: Read-time refusal is claimed before the reader is scoped
- **WHEN** a document, gate, or report states that an origin key is refused for a review act at read time
- **THEN** that claim MUST be refused while the review reader still resolves wallet and grant records from the whole tree
- **AND** the outstanding reader change MUST be named as the open dependency it is

### Requirement: The factory-identity register declares its own staleness bound and ceiling
The factory-identity register SHALL declare its OWN revocation staleness bound and its own ceiling on that bound, and SHALL NOT inherit them from the review-authority register or from any revocation mechanism realized for that register. A projection or reader consuming the factory-identity register SHALL refuse when the view it holds is older than the declared bound, unreadable, or absent, and SHALL diagnose an unreachable store distinctly from an absent one though both refuse.

REVOCATION CHECKED AT THE MOMENT OF CLEARING SHALL BE DECLARED UNREALIZABLE UNTIL A PROJECTION PATH EXISTS, and SHALL NOT be asserted as in force before then. Until that path is settled, an origin row's revocation propagates no faster than the register view a consumer holds, the declared bound is the honest ceiling on that lag, and any statement that revocation is effective at clearing SHALL be refused as unsupported.

#### Scenario: A consumer holds a view older than the bound
- **WHEN** the register view a consumer holds is older than the declared staleness bound, unreadable, or absent
- **THEN** the consumer MUST refuse rather than proceed on that view
- **AND** an unreachable store MUST be diagnosed distinctly from an absent one

#### Scenario: At-clearing revocation is claimed before a projection path exists
- **WHEN** a document or gate states that origin revocation takes effect at clearing
- **THEN** the claim MUST be refused as unsupported while no projection path with a bounded refresh exists
- **AND** the declared bound MUST be stated as the actual ceiling on propagation

#### Scenario: A row is revoked
- **WHEN** an origin identity is revoked
- **THEN** it MUST NOT return to active
- **AND** resumption MUST be a NEW row naming the row it supersedes

### Requirement: The factory-identity register is a permanently human-only surface
Changes to the factory-identity register and the records beside it SHALL be landable only by a human act, and SHALL NEVER be landed by an autonomous or council-cleared approval path. Where a gate enumerates never-clearable floor members, `governance/factory-identity/` SHALL be entered BY NAME rather than matched by a path-shaped clause, and where a consuming repository's floor file is compared as an EXACT SET, that file SHALL be updated in the same governed act that creates the register — an exact-set comparison against a floor that does not yet name the new register fails closed on every candidate, so the two are one change and not two.

#### Scenario: An autonomous approval targets the register
- **WHEN** a candidate editing `governance/factory-identity/` reaches an autonomous or council-cleared approval path
- **THEN** it MUST be refused by a by-name floor entry rather than by a path pattern

#### Scenario: The register lands without the consuming floor file
- **WHEN** the register is created and a consuming repository's exact-set floor file is not updated in the same governed act
- **THEN** the omission MUST be treated as an incomplete change
- **AND** the exact-set comparison MUST NOT be left failing against every candidate

#### Scenario: A repository is admitted as an originator
- **WHEN** a new originating repository is registered
- **THEN** a human issues the backing grant and is named as its issuer
