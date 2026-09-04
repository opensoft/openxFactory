# domain-descendant-boundary Specification

Two MODIFIED requirements. **NO ACTIVE CHANGE CARRIES A DELTA ON THIS
CAPABILITY** — checked over all 31 active change directories at `origin/main`
`a858e5b0`, 2026-09-04 — so both blocks are written over CANON, restated as canon
states it today, and no `Modified over` marker is owed.

**Why this capability has to grow.** Every descendant the standard was written
for is a CONTRACT-FAMILY descendant: `MedxAvatar`, `MedxChart`, `MedxPractice`,
`LedgerxWallet` — YAML profiles over pinned YAML contracts, where "profile,
never fork" is easy to honour because a profile is a file and a fork is a diff.
`MedxDox` is the first descendant of a RUNTIME product with a DATABASE SCHEMA,
ORDERED MIGRATIONS and a DEPLOYMENT, and RULING Q3 (2026-09-04T15:32Z) makes it
the per-tenant deployment unit — *"one instance and one database per tenant,
always … No cross-tenant data ever shares a store."* Neither fact is expressible
in the standard as it stands: "pin and profile, never fork" is easy to honour in
YAML and hard to honour in DDL, and nothing in the capability says a descendant
is a thing you DEPLOY.

**What is deliberately NOT modified here.** *A domain consumes a neutral product
through a descendant repository*, *A descendant pins the product by commit,
twice* and *A descendant is placed at a ratified placement* are unchanged. The
two-level pin chain (a descendant pinning openXdox, which pins openDox) is
carried by `neutral-product-pin` instead, because it is a statement about the PIN
and not about the descendant; and open question Q10 — whether a consumer may pin
openDox DIRECTLY, which would add a "which layer" declaration to the pin — is
NOT decided here and travels to the ratification read (`design.md` § OQ-2).

## MODIFIED Requirements

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
