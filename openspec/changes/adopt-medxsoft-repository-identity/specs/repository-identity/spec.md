# repository-identity Delta: Adopt MedxSoft repository identity

## ADDED Requirements

### Requirement: Canonical repository identity
A governed repository SHALL be named on live normative surfaces by its CURRENT canonical `<owner>/<repo>` identity, and a host-provided redirect from a former identity MUST NOT be treated as that identity.
A live normative surface is any surface a reader or a validator resolves as
current: contract files and their fixtures, examples, tests that pin those
fixtures, and governance documents whose `Status:` is `draft`, `staged`,
`ratified`, `standard`, or `record`-in-force. The owner segment is part of the
identity: a repository whose owner changes has a new canonical identity even
though its name, its history, its commits and its blob digests are unchanged.
A redirect published by the hosting provider is a grace period, because it
lapses when the former owner reuses the name.

#### Scenario: A governed repository is transferred to another organization
- **WHEN** a governed repository moves to a different owning organization
- **THEN** every live normative surface naming it MUST be updated to the new canonical `<owner>/<repo>` before the transfer is treated as governed
- **AND** the update MUST NOT be deferred on the grounds that the provider redirect still resolves

#### Scenario: Only the owner segment moved
- **WHEN** a transfer changes the owner segment and leaves the repository name unchanged
- **THEN** surfaces that name the repository WITHOUT an owner remain correct and MUST NOT be edited
- **AND** recorded commits, paths, and blob digests remain valid, the repository content being unchanged by the transfer

### Requirement: Published repository transfer mapping
openxFactory SHALL publish every governed repository transfer machine-readably in `contracts/policies/repository-identity.yaml`, recording the former identity, the current identity, and the transfer date.
The file carries `schema_version` and `kind` like every other contract policy,
and is registered in `contracts/manifest.yaml` with a per-file digest and a
consumption rule, the way `contracts/policies/layer-vocabulary.yaml` is. Its
purpose is the same as that policy's `legacy_mapping`: a frozen former spelling
encountered anywhere in the corpus resolves to a current identity by lookup
rather than by a reader's memory.

#### Scenario: A reader encounters a former identity
- **WHEN** a tool or a reviewer encounters a repository identity that names a former owner
- **THEN** `contracts/policies/repository-identity.yaml` MUST resolve it to the current canonical identity without modifying the surface that carries it

#### Scenario: A transfer leaves no live surface to rename
- **WHEN** a transferred repository is named nowhere in openxFactory in owner-qualified form
- **THEN** the transfer MUST still be recorded in the mapping, the mapping being the resolver for identities carried by any repository rather than an index of this one's edits

### Requirement: Immutable and dated records keep their recorded identity
An archived change packet, a dated decision record, and a point-in-time verification table MUST NOT be rewritten to carry a repository's new identity, and MUST be interpreted through the published transfer mapping instead.
This extends no new immutability to those records; it states the consequence of
the immutability they already have. A verification table recording that a named
repository was validated at a named commit with a named digest asserts what was
read at a stated moment. Editing the repository column would make it assert that
a verification ran against an address that did not exist when it ran, which
destroys the evidence rather than updating it.

#### Scenario: An archived packet names a former identity
- **WHEN** an archived change packet or its `evidence/` records a repository under its former identity
- **THEN** the bytes MUST NOT change
- **AND** the mapping supplies the current identity to any reader who needs it

#### Scenario: A dated verification table names a former identity
- **WHEN** a dated table pins a repository together with a commit, a path, and a blob digest
- **THEN** the repository column MUST keep the identity recorded at the verification
- **AND** a later reader resolves it through the mapping rather than by trusting the table to be current

### Requirement: A transfer is an additive content change
A repository transfer SHALL be realized as an ADDITIVE content change and MUST NOT change any schema, field name, identifier, or digest-identity rule.
Only values move. Where a transfer edits a member of the declared release
bundle's digest inventory, the bundle is re-cut through the versioning policy's
realization order, which allocates the version late; a proposal MUST NOT reserve
a minor. Published bundles are never rewritten, so a consumer pinned to a bundle
cut before the transfer continues to resolve byte-identically, and
`release-surface-integrity`'s obligation that the declared bundle describes the
release surface is discharged by the cut rather than restated here.

#### Scenario: A transfer edits a release-surface member
- **WHEN** the rename changes the bytes of a file listed in the declared bundle's digest inventory
- **THEN** the change MUST re-cut the bundle as an additive minor with the version allocated at realization
- **AND** it MUST NOT hand-edit an existing inventory so that the comparison passes

#### Scenario: A pinned consumer holds a pre-transfer bundle
- **WHEN** a consumer resolves a bundle published before the transfer
- **THEN** every pinned path, digest, and identifier resolves byte-identically, and the former identity it carries is interpreted through the mapping

#### Scenario: An ordered inventory holds the transferred repository
- **WHEN** a transferred repository appears in an inventory whose entries are ordered by canonical identity
- **THEN** the entry MUST be re-sorted in the same change that respells it
- **AND** every pinned copy of that ordering MUST be re-sorted in the same commit, so the inventory and the artifacts that pin it never disagree
