# domain-descendant-boundary Specification

## Purpose

Bound how a DomainxFactory consumes a neutral `open*` product: through a
`<Domainx><Product>` descendant repository, never by integrating the
product's contracts, schemas, corpus or validator into the domain's own
tree. The capability governs the descendant itself — that it pins the
product by commit twice, as a nested gitlink and a pin manifest moved in
the same commit; that it carries profile, overlay, branding, deploy
configuration and its own validators and never a fork; that it is
aggregated only at a placement a change has ratified; and that it is
created lazily on the domain's first profile artifact rather than stood up
as an empty boundary. openxFactory's own consumption of an external
neutral product is deliberately outside this boundary, because
openxFactory is the neutral layer and not a domain, and sits with
`neutral-product-pin` instead.

## Requirements

### Requirement: A domain consumes a neutral product through a descendant repository
A DomainxFactory SHALL consume a neutral `open*` product through a
`<Domainx><Product>` DESCENDANT repository and SHALL NOT integrate that product's
contracts, schemas, corpus or validator directly into its own tree; the descendant
is the only place a domain's interpretation of the product may live. The corpus
fact behind the rule is that no DomainxFactory consumes any `open*` product by
direct integration and there is no counter-example: the only direct consumer of
neutral contracts is `openxFactory`-as-layer through `stack.yaml`, and
`openxFactory` is the neutral layer rather than a domain, so its own consumption
of an EXTERNAL neutral product is governed by `neutral-product-pin` and not by
this requirement.

#### Scenario: A domain integrates a neutral product directly
- **WHEN** a DomainxFactory adds a neutral product's contracts, schemas, corpus or validator under its own tree instead of pinning a descendant
- **THEN** the integration is refused, and the content is relocated into that domain's `<Domainx><Product>` descendant

#### Scenario: openxFactory consumes an external neutral product
- **WHEN** `openxFactory` consumes a neutral product it does not publish
- **THEN** this requirement does not apply, because `openxFactory` is the neutral layer and not a domain, and the consumption is governed by `neutral-product-pin` instead

#### Scenario: The descendant is named
- **WHEN** a descendant repository is created for a domain
- **THEN** its name takes the `<Domainx><Product>` form every existing descendant uses, so that one casing scheme covers the org rather than two

### Requirement: A descendant pins the product by commit, twice
A descendant SHALL pin the neutral product BY COMMIT TWICE — once as a nested
gitlink and once as a pin manifest at `contracts/<product>-pin.yaml` carrying
`kind: <descendant_repo_snake>_<product_snake>_pin` and, where the pin covers a
whole tree, `relationship: pinned_upstream_composition` — and BOTH SHALL be
changed in the SAME commit, so that a gitlink can never silently disagree with a
declared pin. The kind form follows the two live examples
(`medxchart_openchart_pin`, `medx_avatar_openavatar_pin`). This rule settles the
shape FORWARD only: the three live pin files disagree on directory and kind form
(`MedxChart/contracts/openchart-pin.yaml`; `MedxAvatar/pins/openavatar.yaml`,
which carries `source_repo`/`resolved_ref` and no `relationship:`; openAvatar's
`avatar-client-lab-contract-pin`), and it SHALL NOT be read as retro-fitting them.

#### Scenario: The pin manifest and the gitlink disagree
- **WHEN** a descendant's `contracts/<product>-pin.yaml` and its nested gitlink name different commits of the product
- **THEN** the descendant's own validator REFUSES the tree rather than preferring either, because an unanswerable question is never an implicit pass

#### Scenario: Only one of the two pins moves
- **WHEN** a commit changes the gitlink without changing the pin manifest, or changes the pin manifest without moving the gitlink
- **THEN** the change is refused, because the same-commit rule is what makes the two pins one act

#### Scenario: An existing descendant carries an older pin shape
- **WHEN** a descendant created before this capability carries a differently named pin file or a differently formed kind
- **THEN** it is NOT retro-fitted, and this shape binds descendants created from this ratification forward

### Requirement: A descendant carries profile, never fork
A descendant SHALL carry ONLY profiles, overlays, branding, deploy configuration
and domain validators over its own profile artifacts, and SHALL NOT carry a fork,
an edited copy or a re-authoring of the neutral product's contracts, schemas,
corpus or validator — pin and profile, NEVER fork, in DTN-022's own words that
"domain descendants are pin-and-profile DISTRIBUTIONS … never code forks".
Anything the profile cannot express SHALL be an UPSTREAM change in the product
repository, released and re-pinned, rather than a local edit.

**WHERE THE PINNED PRODUCT CARRIES A DATABASE SCHEMA, THE MIGRATION SET IS
PINNED CONTENT AND THE DESCENDANT SHALL NOT ADD TO IT, EDIT IT OR REORDER IT.**
A descendant of a runtime product SHALL express every domain-specific field
through an EXTENSION POINT THE NEUTRAL SCHEMA DECLARES — a reserved extension
column or document whose shape the neutral product owns — and a domain field
that the declared extension point cannot express SHALL be an upstream schema
change in the product, released as a new ordered migration and re-pinned, exactly
as a contract change is. A descendant that ships a migration of its own is a
FORK OF THE SCHEMA, and it is the harder fork to detect because a database
diverges silently and only at the next upgrade: the pin's digests catch an edited
file, and nothing catches an extra `ALTER TABLE` that has already run. The
descendant MAY carry deploy configuration for the migration RUN — when it
executes, against which instance, under whose credential — because that is
deploy configuration, which this requirement has always permitted.

#### Scenario: The profile cannot express what the domain needs
- **WHEN** a domain needs behaviour its profile shape cannot express
- **THEN** the work is an upstream change in the neutral product repository followed by a release and a re-pin, and never a local edit of pinned content

#### Scenario: A descendant carries an edited copy of pinned content
- **WHEN** a descendant's tree holds a modified copy of a file the pin covers
- **THEN** the descendant is a fork, the copy is refused, and the pin's digests are what detect it

#### Scenario: A descendant adds a domain validator
- **WHEN** a descendant adds a validator that checks its own profile artifacts against the pinned product's schemas
- **THEN** that is permitted, because it interprets the product rather than re-authoring it

#### Scenario: A descendant of a runtime product needs a domain field the neutral schema does not carry
- **WHEN** a descendant of a product with a database schema needs a column, table or document shape the pinned migration set does not declare
- **THEN** it is expressed through the extension point the neutral schema declares, or the work is an upstream schema change released as a new ordered migration and re-pinned
- **AND** a migration authored in the descendant is refused as a fork of the schema, whether or not it has already been applied to a live instance

### Requirement: A descendant is placed at a ratified placement
A descendant SHALL be aggregated at one of exactly two placements, each with a
stated standing and a stated ratifying act, and it MAY carry both.
**RATIFIED:** nested into its DomainxFactory as a submodule (`MedxAvatar` in
`MedxFactory`, DTN-022, 2026-08-03). **RATIFIED 2026-09-03:** the aggregation's
`xFactories/`, realized 2026-08-23 and ratified by its establishing act
`create-medxchart-overlay-boundary` on Brett Heap's in-session ruling of
2026-09-03, whose REALIZED placements are BOTH `xFactories/MedxChart` (gitlink
`68d2f1f5db932cb5099ceac75dab66316ef22579`) and `xFactories/MedxPractice`
(gitlink `d8d73195609df3b567643a7bf1252eac352d9996`), each entered in
`opensoft/xFactory`'s `.gitmodules` at its own `git@github.com:opensoft/` remote
rather than at a relative URL. The choice between
them is the owning domain's, on whether the descendant needs standalone cloning.
A third placement SHALL NOT be used until a change ratifies it. What this
ratification settles is the PLACEMENT and nothing beside it: a placement being
ratified SHALL NOT be read as ratifying the CREATION of a descendant, which the
lazy-creation requirement below governs on its own terms, and both `xFactories/`
descendants are REPORTED EMPTY BOUNDARIES under that requirement rather than
precedent for creating more.

**Removed from canon by create-medxchart-overlay-boundary (2026-09-03):** ``A descendant SHALL be aggregated at one of exactly two placements, whose STANDING differs and SHALL be stated rather than blended, and it MAY carry both.``; ``**REALIZED BUT NOT YET RATIFIED:** the aggregation's `xFactories/` (`MedxChart`, 2026-08-23, whose establishing act `create-medxchart-overlay-boundary` is still `Status: draft`) — permitted here, and confirmed as ratified precedent when that change archives.``; ``**THEN** the placement is permitted, AND its standing is recorded as REALIZED-but-not-yet-ratified until `create-medxchart-overlay-boundary` archives``; ``**THEN** the `xFactories/` placement becomes ratified precedent, and this requirement is amended by an explicit delta to say so rather than by re-reading`` — all four units named the pending condition this ratification discharges, and the amendment the last of them deferred to the archive act is this block. The FIRST unit is replaced because its clause "whose STANDING differs and SHALL be stated rather than blended" asserted that the two placements are of UNEQUAL standing, which stopped being true the moment the second was ratified; it reads "each with a stated standing and a stated ratifying act" instead, which keeps the obligation to STATE standing and drops the claim that the two differ. And the trigger canon set at ARCHIVE is moved to RATIFICATION on the ruling of 2026-09-03; archive still waits on tasks §5.

#### Scenario: A descendant is placed under the aggregation's xFactories/
- **WHEN** a descendant is aggregated at `xFactories/<Descendant>`
- **THEN** the placement is permitted, AND its standing is recorded as RATIFIED, on the 2026-09-03 ratification of `create-medxchart-overlay-boundary`

#### Scenario: The draft establishing act archives
- **WHEN** `create-medxchart-overlay-boundary` archives
- **THEN** the promoted requirement carries THIS block, written at ratification rather than derived at archive by re-reading
- **AND** `tasks.md` § 5's realization evidence EXISTS — the descendant pin validator, its required `pin-validation` check, its ruleset id and one green run — because that evidence is what opens this change's archive gate, and an archive without it is a gate that did not hold

#### Scenario: A third placement is proposed
- **WHEN** a descendant is placed anywhere other than nested in its DomainxFactory or under the aggregation's `xFactories/`
- **THEN** the placement is refused until a change ratifies it

#### Scenario: A descendant carries both placements
- **WHEN** a descendant needs standalone cloning AND presence in its domain tree
- **THEN** it MAY carry both gitlinks, AND the two gitlinks SHALL name the same commit, so that "which checkout was read" has one answer

### Requirement: A descendant is created on its first profile, not before
A `<Domainx><Product>` repository SHALL NOT be created before the domain tree
carries at least one artifact of the product's profile kind: descendants are
created LAZILY and CONSUMER-GATED, so that an empty boundary is never stood up as
precedent. Until that first artifact exists the descendant's NAME MAY be
registered in the naming record while no repository is created.

**WHERE THE PRODUCT IS A RUNTIME, THE DESCENDANT IS ALSO THE DEPLOYMENT UNIT FOR
ONE TENANT, AND A TENANT INSTALL IS A PROFILE ARTIFACT.** RULING Q3
(`opensoft/openxFactory` issue #656, 2026-09-04T15:32Z) is that every domain
install brings its own descendant instance and its own database inside the
tenant, in BOTH operating cases — whether the operator hosts it or the tenant
does — and no cross-tenant data ever shares a store. A domain that has committed
to standing an instance up for a tenant therefore HAS its first profile artifact:
the tenant's own instance declaration. The laziness rule is not weakened by this
and its direction is unchanged — a descendant with neither a profile artifact NOR
a committed tenant install is still not created, and its name is still registered
in the naming record instead. What this clause settles is which fact discharges
the gate for a runtime product, so that a ruling commissioning a consumer and a
standard describing today's state stop appearing to disagree.

**A DESCENDANT THAT IS A DEPLOYMENT UNIT COSTS PER TENANT AND THE COST IS
DECLARED, NOT DISCOVERED.** A descendant of a runtime product SHALL declare, at
creation, the per-tenant operating obligations its instances carry — at least the
migration run per release, the backup and restore policy, and the credential set
— because N instances is N of each, and a boundary that is a deployment unit
without a declared operating cost is an empty boundary with a bill attached.

#### Scenario: A domain has no profile artifact yet
- **WHEN** a domain holds no artifact of the product's profile kind
- **THEN** its descendant repository is NOT created, and only the name is registered

#### Scenario: The first profile artifact appears
- **WHEN** the domain tree acquires its first artifact of the product's profile kind
- **THEN** the descendant is created and that artifact relocates into it

#### Scenario: An empty descendant exists
- **WHEN** a descendant repository exists carrying no profile artifact of the product
- **THEN** it is an empty boundary, and it is reported rather than cited as precedent for creating more

#### Scenario: A domain commits to a tenant install of a runtime product
- **WHEN** a DomainxFactory install stands up an instance of a runtime neutral product for a tenant
- **THEN** the tenant's instance declaration IS the domain's first profile artifact, the descendant is created, and the declaration lives in it
- **AND** a domain with neither a profile artifact nor a committed tenant install still gets a registered NAME and no repository

#### Scenario: A runtime descendant is created without declaring its operating cost
- **WHEN** a descendant of a product carrying a database schema is created with no declared per-tenant migration, backup-and-restore and credential obligations
- **THEN** the creation is refused, because a per-tenant deployment unit whose operating cost is undeclared is discovered one tenant at a time
