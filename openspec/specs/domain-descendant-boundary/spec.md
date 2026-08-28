# domain-descendant-boundary Specification

## Purpose
TBD - created by archiving change split-openxwallet-repo. Update Purpose after archive.
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

#### Scenario: The profile cannot express what the domain needs
- **WHEN** a domain needs behaviour its profile shape cannot express
- **THEN** the work is an upstream change in the neutral product repository followed by a release and a re-pin, and never a local edit of pinned content

#### Scenario: A descendant carries an edited copy of pinned content
- **WHEN** a descendant's tree holds a modified copy of a file the pin covers
- **THEN** the descendant is a fork, the copy is refused, and the pin's digests are what detect it

#### Scenario: A descendant adds a domain validator
- **WHEN** a descendant adds a validator that checks its own profile artifacts against the pinned product's schemas
- **THEN** that is permitted, because it interprets the product rather than re-authoring it

### Requirement: A descendant is placed at a ratified placement
A descendant SHALL be aggregated at one of exactly two placements, whose STANDING
differs and SHALL be stated rather than blended, and it MAY carry both.
**RATIFIED:** nested into its DomainxFactory as a submodule (`MedxAvatar` in
`MedxFactory`, DTN-022, 2026-08-03). **REALIZED BUT NOT YET RATIFIED:** the
aggregation's `xFactories/` (`MedxChart`, 2026-08-23, whose establishing act
`create-medxchart-overlay-boundary` is still `Status: draft`) — permitted here,
and confirmed as ratified precedent when that change archives. The choice between
them is the owning domain's, on whether the descendant needs standalone cloning.
A third placement SHALL NOT be used until a change ratifies it.

#### Scenario: A descendant is placed under the aggregation's xFactories/
- **WHEN** a descendant is aggregated at `xFactories/<Descendant>`
- **THEN** the placement is permitted, AND its standing is recorded as REALIZED-but-not-yet-ratified until `create-medxchart-overlay-boundary` archives

#### Scenario: The draft establishing act archives
- **WHEN** `create-medxchart-overlay-boundary` archives
- **THEN** the `xFactories/` placement becomes ratified precedent, and this requirement is amended by an explicit delta to say so rather than by re-reading

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

#### Scenario: A domain has no profile artifact yet
- **WHEN** a domain holds no artifact of the product's profile kind
- **THEN** its descendant repository is NOT created, and only the name is registered

#### Scenario: The first profile artifact appears
- **WHEN** the domain tree acquires its first artifact of the product's profile kind
- **THEN** the descendant is created and that artifact relocates into it

#### Scenario: An empty descendant exists
- **WHEN** a descendant repository exists carrying no profile artifact of the product
- **THEN** it is an empty boundary, and it is reported rather than cited as precedent for creating more

