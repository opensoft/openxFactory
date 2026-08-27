# ledgerxwallet-overlay-boundary Specification

## ADDED Requirements

### Requirement: LedgerxWallet pins an independent openXwallet repository, by commit, twice, in one commit
`LedgerxWallet` SHALL be a standalone Git repository that pins the upstream
`opensoft/openXwallet` product at an IMMUTABLE COMMIT declared TWICE — once as a
nested submodule gitlink at `openXwallet/`, and once as a committed pin manifest
at `contracts/openxwallet-pin.yaml` carrying `schema_version: 1`,
`kind: ledgerxwallet_openxwallet_pin`, `submodule_path: openXwallet`,
`revision_kind: commit` and `relationship: pinned_upstream_composition` — and
BOTH declarations SHALL be changed in the SAME commit. The pin MUST identify the
repository and revision without depending on a host-absolute filesystem path. A
release tag MAY be recorded beside the commit as a human-readable label
(`contract_bundle_tag`), never as the thing being trusted, and the pin SHALL NOT
express a version range. This instantiates
`domain-descendant-boundary`'s "A descendant pins the product by commit, twice",
whose kind form `<descendant_repo_snake>_<product_snake>_pin` and whose
`relationship:` field are taken from the live example
`MedxChart/contracts/openchart-pin.yaml`; the differently shaped
`MedxAvatar/pins/openavatar.yaml` is NOT retro-fitted and is NOT followed.

#### Scenario: LedgerxWallet is checked out
- **WHEN** a developer checks out LedgerxWallet and initializes its submodules
- **THEN** the nested `openXwallet/` checkout resolves to the commit recorded in `contracts/openxwallet-pin.yaml`
- **AND** the pin manifest and the gitlink name the same commit

#### Scenario: The pin manifest and the gitlink disagree
- **WHEN** `contracts/openxwallet-pin.yaml` and the nested `openXwallet/` gitlink name different commits
- **THEN** the tree is REFUSED rather than either being preferred, because an unanswerable question is never an implicit pass

#### Scenario: Only one of the two pins moves
- **WHEN** a commit changes the gitlink without changing the pin manifest, or changes the pin manifest without moving the gitlink
- **THEN** the change is refused, because the same-commit rule is what makes the two declarations one act

#### Scenario: The pin names a tag and no commit
- **WHEN** the pin file records `wallet-vN.M` but no 40-hex commit
- **THEN** the pin is refused, because a tag can be moved and a commit cannot

#### Scenario: Upstream openXwallet advances
- **WHEN** `opensoft/openXwallet` receives a new commit or a new bundle tag
- **THEN** the existing LedgerxWallet checkout remains at its prior recorded commit
- **AND** adopting the new revision is a PIN BUMP that moves both declarations together, never a moving reference

### Requirement: The Ledgerx domain consumes openXwallet only through the nested LedgerxWallet descendant
`LedgerxFactory` SHALL consume `openXwallet` exclusively through a
`LedgerxWallet` descendant nested as a submodule at `LedgerxWallet`, and SHALL
NOT resolve that product's contracts, schemas, corpus or validator by any path
outside the descendant — no directory-adjacency walk, no candidate list reaching
into another repository's checkout, and no in-tree copy. LedgerxFactory's
`stack.yaml` DECLARED `openxwallet:` block SHALL record
`contract_source: LedgerxWallet-nested-submodule-pin`, and its `contract_ref`
SHALL EQUAL both LedgerxWallet declarations, so that the commit governing the
Ledgerx estate has ONE answer stated in THREE places. The nested placement is the
RATIFIED placement of `domain-descendant-boundary` (`MedxAvatar` in
`MedxFactory`, DTN-022); the aggregation's `xFactories/` placement is NOT taken
here, and if it is ever added the two gitlinks SHALL name the same commit.

#### Scenario: A resolver reaches outside the descendant
- **WHEN** a LedgerxFactory tool resolves the openXwallet validator at a path outside `LedgerxWallet/openXwallet/`, such as a parent directory's `openxFactory/openXwallet/` or the aggregation's root gitlink
- **THEN** the resolution is a direct integration of the product and is refused, because only the descendant's own gitlink is governed by `contracts/openxwallet-pin.yaml`

#### Scenario: The declared pin and the descendant's pin disagree
- **WHEN** LedgerxFactory's `stack.yaml` `openxwallet.contract_ref` names a commit other than the one LedgerxWallet's pin manifest and gitlink name
- **THEN** the disagreement REFUSES rather than picking a winner, and the estate is not validated against either

#### Scenario: openxFactory's own pin moves independently
- **WHEN** `openxFactory`'s `contracts/openxwallet-pin.yaml` is bumped to a different openXwallet commit than LedgerxWallet pins
- **THEN** that is PERMITTED, because openxFactory and LedgerxWallet are independent consumers of the same product
- **AND** the divergence is REPORTED, AND the commit governing the Ledgerx estate remains the one LedgerxWallet pins

#### Scenario: A third placement is proposed
- **WHEN** LedgerxWallet is aggregated anywhere other than nested in LedgerxFactory or under the aggregation's `xFactories/`
- **THEN** the placement is refused until a change ratifies it

### Requirement: LedgerxWallet carries the Ledgerx wallet PROFILE and never the tenant estate, and never a fork
`LedgerxWallet` SHALL carry ONLY the Ledgerx interpretation of the wallet product
— the exercise-record instantiation template, the distinct-holder constraint
sets, the declared custody posture, branding and deploy configuration, and domain
validators over those profile artifacts — and SHALL NOT carry a fork, an edited
copy or a re-authoring of openXwallet's contracts, schemas, corpus or validator.
The TENANT ESTATE — wallet records, capability grants, keys, exercise records and
any other artifact carrying a tenant's holder ids, DIDs, key ids, issuance or
expiry — SHALL remain in `LedgerxFactory` under `tenants/<tenant>/wallets/`,
because a profile repository holding one tenant's identity estate is reusable by
construction and un-reusable in fact. The PLATFORM SEAM — the Business Central
holder-registry contract and the enforcement projection it declares — SHALL also
remain in LedgerxFactory. Anything the profile cannot express SHALL be an
UPSTREAM change in `opensoft/openXwallet`, released and re-pinned, never a local
edit.

#### Scenario: A tenant estate record is proposed into the descendant
- **WHEN** a wallet record, capability grant or exercise record carrying a tenant's holder id, DID or key id is added to LedgerxWallet
- **THEN** it is refused and filed in LedgerxFactory's tenant estate, because the profile/instance line is what makes the descendant reusable across tenants

#### Scenario: The profile cannot express what the domain needs
- **WHEN** the Ledgerx domain needs wallet behaviour its profile shape cannot express
- **THEN** the work is an upstream change in `opensoft/openXwallet` followed by a release and a pin bump, and never a local edit of pinned content

#### Scenario: An edited copy of pinned content appears in the descendant
- **WHEN** LedgerxWallet's tree holds a modified copy of a file the openXwallet pin covers
- **THEN** the descendant is a fork, the copy is refused, and the pin's recorded commit is what detects it

#### Scenario: A domain-wide constraint is filed under a tenant path
- **WHEN** a distinct-holder constraint set naming no tenant, no wallet and no key sits under `tenants/<tenant>/wallets/`
- **THEN** it is MIS-FILED domain policy, and it belongs in the descendant's profile rather than in the tenant estate

#### Scenario: The descendant adds a domain validator
- **WHEN** LedgerxWallet adds a validator that checks its own profile artifacts and the domain vocabulary against the pinned product's schemas
- **THEN** that is permitted, because it interprets the product rather than re-authoring it

### Requirement: Relocating the profile preserves the estate's coverage and declares its scan target
The relocation of the Ledgerx wallet profile out of `LedgerxFactory` SHALL NOT
reduce the coverage the estate had before it, and the moved validator SHALL take
its scan target as a DECLARED ESTATE ROOT rather than by walking directories.
LedgerxFactory's enforcement is a glob over `tests/validate_*.py`, so the path
`tests/validate_wallet_estate.py` SHALL continue to exist in LedgerxFactory as a
DELEGATING ENTRY that invokes the single implementation in
`LedgerxWallet/tests/validate_wallet_estate.py` and propagates its exit code —
never as a copy, an edited copy or a second implementation of any rule. Where the
delegating entry or the moved validator cannot reach what it needs — an
uninitialized `LedgerxWallet` submodule, an unresolvable estate root, or an
estate root holding no `tenants/*/wallets/` directory — it SHALL FAIL CLOSED with
a named exit and a REMEDIATION STRING naming the initializing command, and SHALL
NOT skip, pass, or degrade to "empty". Tenant-specific expectations SHALL be
declared in the estate that owns them, not hard-coded in the cross-tenant
profile validator.

#### Scenario: The bar is run after the relocation
- **WHEN** the LedgerxFactory bar runs its `tests/validate_*.py` glob
- **THEN** the wallet estate is checked, by the same rules, through the delegating entry
- **AND** the rules exist in exactly one place

#### Scenario: The LedgerxWallet submodule is uninitialized
- **WHEN** the delegating entry runs in a checkout where `LedgerxWallet` has not been initialized
- **THEN** it REFUSES with a named exit and names `git submodule update --init LedgerxWallet`
- **AND** it does not skip, because an unreadable surface must fail rather than degrade to "empty"

#### Scenario: A refusal carries no remediation
- **WHEN** a fail-closed path added by this relocation emits a refusal that names no command
- **THEN** the refusal is itself a defect of this capability, because it tells the operator that something is wrong without telling them what to run

#### Scenario: One tenant's wallet ids sit inside the profile validator
- **WHEN** the moved validator hard-codes a specific tenant's wallet or grant ids as its expected set
- **THEN** that expectation is relocated into the estate the ids belong to, and the validator READS it, because a cross-tenant profile cannot enumerate one tenant's estate

#### Scenario: A prepared runsheet references a relocating path
- **WHEN** an un-executed runsheet or quickstart in LedgerxFactory references a profile artifact by a path this relocation changes
- **THEN** the reference is repointed IN THE SAME ACT as the move, because a prepared live window whose paths moved underneath it is a broken procedure rather than a stale link

### Requirement: LedgerxWallet is created on the Ledgerx profile that already exists, and no sibling descendant is created without one
`LedgerxWallet` SHALL be created because `LedgerxFactory` already carries wallet
profile artifacts, and the sibling descendants `MedxWallet`, `codexWallet`,
`OpsxWallet` and `AdxWallet` SHALL NOT be created until their own domain tree
carries at least one wallet profile artifact — descendants are created LAZILY and
CONSUMER-GATED, so that an empty boundary is never stood up as precedent. Until
that first artifact exists a sibling's NAME MAY be registered while no repository
is created. This change creates exactly one repository and SHALL NOT be cited as
precedent for creating another without its own profile.

#### Scenario: A sibling domain has no wallet profile artifact
- **WHEN** a domain other than Ledgerx holds no artifact of the wallet product's profile kind
- **THEN** its descendant repository is NOT created, and only the name is registered

#### Scenario: A sibling domain acquires its first wallet profile artifact
- **WHEN** that domain's tree acquires its first wallet profile artifact
- **THEN** its descendant is created and that artifact relocates into it

#### Scenario: An empty wallet descendant exists
- **WHEN** a `<Domainx>Wallet` repository exists carrying no wallet profile artifact
- **THEN** it is an empty boundary, and it is REPORTED rather than cited as precedent for creating more
