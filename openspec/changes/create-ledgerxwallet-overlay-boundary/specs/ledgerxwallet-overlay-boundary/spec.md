# ledgerxwallet-overlay-boundary Specification

## ADDED Requirements

### Requirement: LedgerxWallet pins an independent openXwallet repository, by commit, twice, in one commit
`LedgerxWallet` SHALL be a standalone Git repository that pins the upstream
`opensoft/openXwallet` product at an IMMUTABLE COMMIT declared TWICE — once as a
nested submodule gitlink at `openXwallet/`, and once as a committed pin manifest
at `contracts/openxwallet-pin.yaml` carrying `schema_version: 1`,
`kind: ledgerxwallet_openxwallet_pin` and a `pin:` mapping holding `repository`,
`remote`, `revision`, `revision_kind: commit`, `submodule_path: openXwallet` and
`relationship: pinned_upstream_composition` — and BOTH declarations SHALL be
changed in the SAME commit. The pin MUST identify the repository and revision
without depending on a host-absolute filesystem path. A release tag MAY be
recorded beside the commit as a human-readable label, never as the thing being
trusted, and the pin SHALL NOT express a version range. Where the pinned tag is
ANNOTATED, the recorded revision SHALL be the dereferenced commit and never the
tag object.

#### Scenario: LedgerxWallet is checked out
- **WHEN** a developer checks out LedgerxWallet and initializes its submodules
- **THEN** the nested `openXwallet/` checkout resolves to the commit recorded in `contracts/openxwallet-pin.yaml`

#### Scenario: The pin manifest and the gitlink disagree
- **WHEN** `contracts/openxwallet-pin.yaml` and the nested `openXwallet/` gitlink name different commits
- **THEN** the descendant's OWN validator REFUSES the tree rather than preferring either, because an unanswerable question is never an implicit pass

#### Scenario: Only one of the two pins moves
- **WHEN** a commit changes the gitlink without changing the pin manifest, or changes the pin manifest without moving the gitlink
- **THEN** the descendant's own validator REFUSES, because the same-commit rule is what makes the two declarations one act

#### Scenario: The pin names a tag and no commit
- **WHEN** the pin file records a bundle tag but no 40-hex commit, or records an annotated tag's object id in place of the commit
- **THEN** the descendant's own validator REFUSES, because a tag can be moved and a commit cannot

#### Scenario: Upstream openXwallet advances
- **WHEN** `opensoft/openXwallet` receives a new commit or a new bundle tag
- **THEN** the existing LedgerxWallet checkout remains at its prior recorded commit
- **AND** adopting the new revision is a PIN BUMP moving both declarations together, never a moving reference

### Requirement: The Ledgerx domain resolves openXwallet only through the nested LedgerxWallet descendant
`LedgerxFactory` SHALL resolve `openXwallet`'s validator, contracts, schemas and
corpus exclusively through a `LedgerxWallet` descendant nested as a submodule at
`LedgerxWallet`, at a FIXED relative path, and SHALL NOT resolve them by
directory adjacency — no upward walk, no candidate list reaching into another
repository's checkout, and no in-tree copy. This binds every resolution site in
the domain tree, tooling and written procedure alike. LedgerxFactory's declared
`stack.yaml` `openxwallet:` block SHALL record
`contract_source: LedgerxWallet-nested-submodule-pin` and a `contract_ref` equal
to both LedgerxWallet declarations, so the commit governing the Ledgerx estate
has ONE answer stated in THREE places. The nested placement is the RATIFIED
placement of `domain-descendant-boundary`; the aggregation's `xFactories/`
placement is not taken here, and if it is ever added the two gitlinks SHALL name
the same commit.

#### Scenario: A resolver reaches outside the descendant
- **WHEN** a LedgerxFactory tool or documented procedure resolves the openXwallet validator at a path outside `LedgerxWallet/openXwallet/` — a parent directory's `openxFactory/openXwallet/`, the aggregation's root gitlink, or a pre-carve in-tree copy
- **THEN** the resolution is a direct integration of the product and is refused, because only the descendant's own gitlink is governed by `contracts/openxwallet-pin.yaml`

#### Scenario: Candidate order stands in for a pin
- **WHEN** more than one checkout of the product is reachable and the domain resolves between them by ORDERING candidates
- **THEN** the ordering is a tie-break rather than a pin, and it does not satisfy this requirement

#### Scenario: The declared pin and the descendant's pin disagree
- **WHEN** `stack.yaml` `openxwallet.contract_ref` names a commit other than the one LedgerxWallet's pin manifest and gitlink name
- **THEN** the disagreement is a finding of the domain's own estate bar when that bar is run, and the estate is not validated against either

#### Scenario: openxFactory's own pin moves independently
- **WHEN** `openxFactory`'s pin or the aggregation's root gitlink names a different openXwallet commit than LedgerxWallet pins
- **THEN** that is PERMITTED and is NOT an error, because they are independent consumers governed by different pins
- **AND** it falls OUTSIDE `neutral-product-pin`'s root-equals-nested rule, so no existing check compares them and none SHALL be described as doing so

#### Scenario: A ratified illustration stops describing this consumer
- **WHEN** `neutral-product-pin`'s illustration says a walk-up resolver in a consumer repository "resolves the NESTED checkout, because that is the one the consuming repository's pin governs"
- **THEN** after this change that sentence no longer describes LedgerxFactory, whose governing pin is its DESCENDANT's rather than `openxFactory`'s nested one
- **AND** the neutral requirement is NOT amended by this capability, because it is a statement about `openxFactory`'s own consumption and the illustration's consumer example is not its normative content

#### Scenario: The parent's capabilities are promoted
- **WHEN** `split-openxwallet-repo` archives and `domain-descendant-boundary` and `neutral-product-pin` enter `openspec/specs/`
- **THEN** this capability's citations resolve against the promoted specs unchanged, because it restates none of their requirements as its own law
- **AND** any conflict discovered at that point is resolved in the neutral capability by an explicit delta, never by re-reading this one

### Requirement: LedgerxWallet carries profile, never the tenant estate, and never a fork
`LedgerxWallet` SHALL carry ONLY the Ledgerx interpretation of the wallet product
— instantiation templates, overlays, branding, deploy configuration and domain
validators over its own artifacts — and SHALL NOT carry a fork, an edited copy or
a re-authoring of openXwallet's contracts, schemas, corpus or validator. The
TENANT ESTATE — wallet RECORDS, capability GRANTS, keys and exercise RECORDS
carrying a tenant's holder ids, DIDs, key ids, issuance or expiry — SHALL remain
in `LedgerxFactory`. The PLATFORM SEAM — the Business Central holder-registry
contract and the enforcement projection it declares — SHALL also remain there.
Anything the profile cannot express SHALL be an UPSTREAM change in
`opensoft/openXwallet`, released and re-pinned, never a local edit.

#### Scenario: A tenant estate record is proposed into the descendant
- **WHEN** a wallet record, capability grant or exercise record carrying a tenant's holder id, DID or key id is added to LedgerxWallet
- **THEN** it is refused and filed in LedgerxFactory's tenant estate, because the profile/instance line is what makes the descendant reusable across tenants

#### Scenario: A template names its domain's live ids as placeholder guidance
- **WHEN** an instantiation template carries this domain's wallet, grant, key or holder ids as example strings inside placeholder markers rather than as declared facts
- **THEN** it remains profile, because a stub that shows which ids to substitute is guidance and not an estate record

#### Scenario: The profile cannot express what the domain needs
- **WHEN** the Ledgerx domain needs wallet behaviour its profile shape cannot express
- **THEN** the work is an upstream change in `opensoft/openXwallet` followed by a release and a pin bump, and never a local edit of pinned content

#### Scenario: An edited copy of pinned content appears in the descendant
- **WHEN** LedgerxWallet's tree holds a modified copy of a file the openXwallet pin covers
- **THEN** the descendant is a fork and the copy is refused
- **AND** because this pin records a commit and no per-file digests, what detects it is the descendant's own validator comparing the CHECKED-OUT `openXwallet/` revision and cleanliness to the pin — not the digest comparison `domain-descendant-boundary`'s scenario names, whose detector this pin deliberately does not carry (declared as a reduction in effect, not as an amendment to that rule)

### Requirement: A relocation into the descendant SHALL reduce no coverage and break no prepared procedure
Relocating an artifact from `LedgerxFactory` into `LedgerxWallet` SHALL NOT
reduce the checking that artifact and its neighbours received before the move,
and SHALL NOT leave a written procedure pointing at a path that no longer exists.
Because the pinned product's own sweep PRUNES NESTED REPOSITORIES from
adjudication, an artifact the sweep adjudicates SHALL NOT be relocated into the
nested descendant until a scan pass exists that reaches it there; and any
count-based or lookup-based check whose inputs the relocation changes SHALL be
restated in the same act. Every reference to a relocated path — tooling, README,
runsheet, quickstart — SHALL be repointed IN THE SAME COMMIT as the relocation,
and where reaching the new location requires initializing a submodule, the
procedures that reach it SHALL gain that initialization as a stated precondition
with its exact command.

#### Scenario: An adjudicated artifact is proposed for relocation
- **WHEN** relocating an artifact that the pinned product's repo scan adjudicates as a live record
- **THEN** the relocation is deferred until a scan pass reaches the descendant, because a nested repository is pruned from that sweep and the artifact would be adjudicated by nothing

#### Scenario: A relocation changes a check's inputs
- **WHEN** a relocation removes an input from a count floor or a keyed lookup that another check performs
- **THEN** the check is restated in the same act, and a relocation that reds the bar is not complete

#### Scenario: A prepared procedure references a relocating path
- **WHEN** an un-executed runsheet or quickstart references an artifact by a path the relocation changes
- **THEN** the reference is repointed in the same commit, because a prepared live window whose paths moved underneath it is a broken procedure rather than a stale link

#### Scenario: Reaching the new location needs an uninitialized submodule
- **WHEN** a procedure or tool must read a relocated artifact through a submodule that may be uninitialized
- **THEN** it REFUSES with a named exit rather than skipping, AND names the exact initializing command, recursively where the artifact sits more than one gitlink deep

### Requirement: LedgerxWallet is created on the Ledgerx profile artifact that already exists
`LedgerxWallet` SHALL be created because `LedgerxFactory` already carries a
wallet profile artifact, and this capability SHALL NOT be cited as precedent for
creating any other `<Domainx>Wallet` repository. The creation gate for sibling
descendants is `domain-descendant-boundary`'s lazy, consumer-gated rule and not
this capability's; their names are registered under R7 of
`split-openxwallet-repo` while no repository is created.

#### Scenario: LedgerxWallet is created
- **WHEN** this change creates the descendant
- **THEN** at least one Ledgerx wallet profile artifact relocates into it in the same wave, so the boundary is not stood up empty

#### Scenario: Another domain's descendant is proposed on this precedent
- **WHEN** a `<Domainx>Wallet` repository is proposed citing this capability
- **THEN** the citation does not carry, and the proposal is measured against `domain-descendant-boundary`'s creation gate on that domain's own profile artifacts

#### Scenario: An empty wallet descendant exists
- **WHEN** a `<Domainx>Wallet` repository exists carrying no wallet profile artifact
- **THEN** it is an empty boundary, and it is not cited as precedent for creating more
