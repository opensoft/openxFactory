# identity-brokering Specification (delta)

## ADDED Requirements

### Requirement: One persona per human within a broker instance

openxFactory SHALL require that a conformant identity broker resolve every
human it authenticates to exactly ONE persona within that broker instance,
with every federated upstream identity that human uses attached to that
persona as a linked identity rather than standing up a second one. A
surface in scope SHALL NOT hold a human account the broker cannot resolve
to a persona, because an account that resolves nowhere is an identity the
governed layer cannot name.

The persona is the durable unit. Upstream accounts are contingent — they
are created, retired, renamed and reassigned by organisations the family
does not control — so nothing durable may be built on one.

#### Scenario: the same human arrives from a second upstream

- WHEN a human who authenticated through one upstream provider later
  authenticates through another and that identity is linked
- THEN both logins resolve to the same persona
- AND no second persona exists for that human in the instance

#### Scenario: a surface proposes its own human accounts

- WHEN a surface proposes holding human accounts of its own
- THEN the proposal is refused because human identity resolves at the
  broker
- AND the surface consumes persona assertions instead

### Requirement: Organizations realize company boundaries, on the persona

openxFactory SHALL model every company boundary — the tenant/operator
company and the subject/served company alike — as an ORGANIZATION that a
persona belongs to, never as a separate persona and never as a separate
identity population. Membership is many-to-many: one persona may belong to
several organizations at once, and an organization MAY federate its own
upstream identity provider with domain-routed login so its people reach
their own provider from a shared entry point.

Membership records association, not authority. Which organizations a
persona belongs to is an input to an authorization decision taken
elsewhere, never the decision itself.

#### Scenario: one human works for several companies

- WHEN a human works for more than one company in scope
- THEN the human holds one persona carrying one organization membership
  per company
- AND leaving a company removes a membership, never the persona

#### Scenario: a client organization requires its own provider

- WHEN an organization requires its own upstream identity provider
- THEN that organization federates its provider and its domains route to
  it
- AND personas authenticating through it remain single personas with
  memberships

#### Scenario: membership is offered as authority

- WHEN a surface treats an organization membership as permission to act
- THEN the treatment is a validation failure
- AND the surface MUST resolve authorization in the governed layer

### Requirement: The broker asserts identity and membership only

A conformant identity broker SHALL assert exactly two things about an
authenticated human — the persona's stable identity and its organization
memberships — and MUST NOT represent stacks, layers, domains, projects,
subjects, roles, grants, or any other part of the tenancy and authority
graph. Authorization SHALL resolve in the governed layer, against the
governed tenancy graph and the grants already recorded there.

An organization MAY carry a single reference to the governed record it
corresponds to, so the governed layer can resolve the boundary the broker
named. That reference is a pointer, not a projection: replicating the
graph's contents into broker state is the prohibited act.

Reasoning carried from the ruling: a second copy of the tenancy graph
inside an identity product is a copy that will disagree with the first
one, and the disagreement will be discovered by an authorization decision
going the wrong way.

#### Scenario: a surface needs an authorization decision

- WHEN a surface must decide whether a persona may perform an action
- THEN the decision resolves in the governed layer against the tenancy
  graph and the grants recorded there
- AND the broker's assertion contributes identity and memberships only

#### Scenario: tenancy is proposed as broker state

- WHEN a change proposes encoding stacks, layers, domains, projects, or
  grants as broker groups, roles, or attributes
- THEN it is refused as a second authority copy
- AND the governed layer remains the single authority

#### Scenario: an organization points at its governed record

- WHEN an organization declares the governed subject or tenant it
  corresponds to
- THEN the declaration is a single resolvable reference
- AND copying that record's contents into broker state is a validation
  failure

### Requirement: Identities link explicitly or merge by decision, never silently

openxFactory SHALL admit exactly two ways for a federated identity to
join an existing persona — an EXPLICIT link initiated by the human from a
session already holding that persona, or an ADMINISTRATIVE MERGE approved
through the governed administration workflow and recorded — and SHALL
forbid linking identities on an attribute match, an email address above
all, however convenient.

An upstream provider may assert an address it never verified, and
addresses are reassigned; attribute-match auto-linking is therefore an
account-takeover primitive, and the resulting merge cannot be undone from
the audit record. A merge SHALL produce a record naming the approver, the
identities merged, and the time, and the pre-merge subject identifiers
SHALL remain resolvable to the surviving persona so records already
written against them stay attributable.

#### Scenario: an upstream asserts a familiar address

- WHEN a new federated identity presents an attribute matching an
  existing persona
- THEN no link is created
- AND the identity stays separate until the human links it or an
  administrator approves a merge

#### Scenario: duplicates are merged

- WHEN an administrator approves a merge of two personas
- THEN a merge record names the approver, both prior subject identifiers,
  and the time
- AND records written against the pre-merge identifiers remain resolvable
  to the surviving persona

#### Scenario: a link record cannot name who acted

- WHEN a link or merge record names neither an initiating human nor an
  approving administrator
- THEN validation fails
- AND the link is not treated as established

### Requirement: A governed record binds its actor to a stable opaque subject

A governed record naming a human actor SHALL carry the STABLE OPAQUE
SUBJECT IDENTIFIER the broker issued for that persona together with the
display name as it stood when the record was written, and MUST NOT use a
display name, an email address, or an upstream account name as the
identifier. Display names change and upstream accounts are reassigned;
only the opaque subject is durable, and the denormalized display name
exists so a record stays readable without a live broker.

An actor recorded before a broker existed carries a bare username. Such a
record SHALL NOT be presented as a broker-asserted persona: it is either
resolved through an explicitly recorded mapping or marked as predating the
persona boundary.

The exact field shape on each record family — a single opaque identifier
or a small structured reference carrying issuer, subject and display name
— is a NAMED OPEN DESIGN POINT settled at realization (design OQ-1 and
OQ-3). This requirement fixes what must hold, not the shape.

#### Scenario: a governed act is recorded

- WHEN a persona performs a governed act
- THEN the record carries the broker-issued opaque subject and the display
  name in force at the time
- AND a later display-name change does not change who the record names

#### Scenario: a display name is used as the identifier

- WHEN a record or a lookup uses a display name, email address, or
  upstream account name as the actor identifier
- THEN validation fails
- AND the opaque subject is required instead

#### Scenario: a pre-broker record is read

- WHEN a record written before the broker carries a bare username as its
  actor
- THEN it is resolved through an explicitly recorded mapping or marked as
  predating the persona boundary
- AND it is never presented as a broker-asserted persona

### Requirement: Workloads are not personas

openxFactory SHALL keep non-human identity out of the persona population:
a workload, agent, job, or service SHALL NOT be represented as a persona,
and its authority SHALL continue to come from `credential-contracts`
grants and `openxwallet` holders rather than from anything the broker
holds. A broker service client MAY be provisioned only where a surface
genuinely needs OIDC tokens — a confidential client for a web surface, for
instance — and such a client is TRANSPORT: it holds no organization
membership as authority and never appears as the actor of a governed act.

Reasoning carried from the ruling: the family already ratified an
authority model for non-human actors, and it is stronger than a user row —
attenuated grants, proof of possession, key-attributed audit, revocation
that propagates. A second, weaker authority vocabulary living next to it
would win by convenience.

#### Scenario: a workload needs authority

- WHEN a workload needs authority to act
- THEN it receives a grant under `credential-contracts` / `openxwallet`
- AND no persona is created for it

#### Scenario: a surface needs OIDC tokens

- WHEN a surface requires OIDC tokens for its users or for itself
- THEN a service client may be provisioned for that surface with its
  purpose declared
- AND the client is recorded as transport, never as the actor of a
  governed act

#### Scenario: a service client is offered as an actor

- WHEN a governed record names a service client as the human actor of an
  act
- THEN validation fails
- AND the act is recorded as unattributed unless a persona can be
  established

### Requirement: Broker credentials are credential-contract records

Every credential the broker holds or issues SHALL be a
`credential-contracts` record with declared custody and a named holder —
service-client secrets, upstream provider client credentials, datastore
credentials, and administrative bootstrap credentials alike — and MUST NOT
be committed to a repository, embedded in a configuration export, or
carried in a deployment manifest. A configuration export used as reviewed
state SHALL be credential-free by construction rather than by redaction
after the fact.

Adopting persona login for a surface that today runs on a shared static
secret SHALL RETIRE that secret rather than leaving both in service, so
the credential inventory shrinks by the adoption instead of growing.

#### Scenario: the broker is deployed

- WHEN broker deployment requires secrets
- THEN each is a credential record with declared custody and a named
  holder
- AND none appears in repository content

#### Scenario: configuration is exported as desired state

- WHEN broker configuration is exported for review or replay
- THEN the export carries no credential values
- AND an export containing one is a validation failure

#### Scenario: a shared static secret is replaced

- WHEN a surface moves from a shared static credential to persona login
- THEN the shared credential is retired as part of the adoption
- AND the inventory records one fewer shared secret, not one more

### Requirement: Isolation escalates by instance, never by fragmenting personas

Isolation SHALL escalate to a DEDICATED BROKER INSTANCE — its own
deployment, with its own datastore and its own administrative plane —
wherever a contract, a regulation, or a population's sensitivity forbids
co-residence, and SHALL NOT be met by partitioning personas inside a
shared instance. Partitioning inside one instance pays the full
persona-fragmentation cost while buying weaker isolation: the
administrative plane, the datastore, and the blast radius stay shared.

This capability is deliberately SILENT ON INSTANCE COUNT. A single shared
instance, a family of per-client instances, and a single-organization
deployment with no operator layer above it are all conformant. Personas do
not span instances, and no capability SHALL require that they do.

#### Scenario: a population must not co-reside

- WHEN a commitment forbids a population sharing a broker with others
- THEN that population is served by a dedicated broker instance
- AND partitioning personas inside a shared instance is refused as the
  answer

#### Scenario: a single-organization deployment runs its own broker

- WHEN a deployment with no operator layer above it operates its own
  broker
- THEN it is conformant
- AND nothing requires it to join a shared instance

#### Scenario: the same human exists in two instances

- WHEN a human holds a persona in two broker instances
- THEN each persona is single within its own instance
- AND no capability requires the two to be linked

### Requirement: A surface declares its authorization posture

A surface adopting persona login SHALL declare its authorization posture —
whether access is granted to any authenticated persona, or resolved per
action in the governed layer — and a surface offering a governed WRITE
action SHALL require a resolved authorization decision rather than
authentication alone.

The failure this closes is the quiet one: a surface ships read-only under
"any authenticated persona", then gains a write action before per-action
authorization exists, and the login is silently doing work it was never
designed to do. Declaring the posture makes acquiring a write action a
visible change of posture rather than an unremarked commit.

#### Scenario: a read-only surface adopts persona login

- WHEN a read-only surface moves behind persona login
- THEN it declares an authenticated-persona posture
- AND the declaration is part of its adoption record

#### Scenario: a declared read-only surface gains a write action

- WHEN a governed write action is added to a surface whose declared
  posture is authentication-only
- THEN the action is blocked until the surface resolves authorization in
  the governed layer
- AND the posture declaration is updated in the same change
