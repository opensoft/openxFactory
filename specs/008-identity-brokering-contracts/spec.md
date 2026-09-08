# Feature Specification: identity-brokering neutral contracts

**Feature Branch**: `008-identity-brokering-contracts`

**Created**: 2026-08-21

**Status**: Draft

**Input**: Implement the ratified `add-identity-brokering` OpenSpec change as
neutral contracts, a validator, and a negative-confirmation fixture corpus.
Scope is exactly OpenSpec tasks 1.1–1.10 plus the promotion bookkeeping in 3.1
and 3.2.

**Governing change**: `openspec/changes/add-identity-brokering/` — ratified by
Brett Heap on 2026-08-21 ("ratify both proposals"), authorizing exactly one
Speckit realization feature for phase 1. The change's `tasks.md` is the
authority for scope; this specification does not extend it.

**Capabilities realized**: `identity-brokering` (nine requirements). The
change's second delta — one ADDED `repo-boundary-governance` requirement
admitting the install repository — creates no code surface and is realized by
the change's own spec text.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One human, several companies, one persona (Priority: P1)

A person who works for the operator company and with a client company
authenticates through whichever upstream provider each organization chose, and
arrives as ONE persona carrying one membership per company. A second upstream
identity attaches to that persona explicitly; it never stands up a second one.
A surface consuming the assertion learns exactly two things — who this persona
is, and which organizations it belongs to.

**Why this priority**: This is the human reality the whole capability exists
for, and the smallest slice that stands alone. Without it, identity-per-surface
and identity-per-tenant fragment a person into unlinkable accounts, which is
the outcome the topic was organized to prevent. It is also where the
never-mirror rule has to hold, because the assertion is where a tenancy
projection would arrive first.

**Independent Test**: Author a persona assertion with two linked upstream
identities and two organization memberships and confirm it validates. Add a
`roles` array — or a `projects` list inside a membership — and confirm
validation fails naming the undeclared property and the never-mirror rule.
Author a second persona in the same instance sharing one of those upstream
identities and confirm validation fails naming the shared identity.

**Acceptance Scenarios**:

1. **Given** a persona assertion carrying two linked upstream identities and
   two organization memberships, **When** it is validated, **Then** it passes,
   and **When** the same record is given a role, group, grant, project, stack
   or layer at any depth, **Then** validation fails naming the property and the
   never-mirror rule.
2. **Given** two persona assertions in one broker instance, **When** both carry
   the same federated upstream identity, **Then** validation fails — one human
   resolves to exactly one persona within an instance.
3. **Given** a surface adoption record, **When** it declares that the surface
   holds human accounts of its own, **Then** validation fails: human identity
   resolves at the broker, and an account that resolves nowhere is an identity
   the governed layer cannot name.
4. **Given** an organization, **When** it declares more than one reference to a
   governed record, or copies that record's contents beside the reference,
   **Then** validation fails — the line is pointer versus projection.
5. **Given** an organization, **When** its company role is spelled with a
   reserved layer term (`client`, `customer`), **Then** validation fails
   against the ratified layer vocabulary read from the policy file.

---

### User Story 2 - An identity joins a persona only by an act somebody took (Priority: P2)

A federated identity joins an existing persona in exactly two ways: the human
links it from a session already holding that persona, or an administrator
approves a merge through the governed workflow and the merge is recorded with
every prior subject identifier. An attribute match — an email address above all
— links nothing.

**Why this priority**: It is the ruling with the sharpest failure mode. Silent
auto-linking is an account-takeover primitive, and the resulting merge cannot
be undone from the audit record; a merge that drops a prior subject silently
orphans every record written against it. It is second only because User Story 1
must exist for there to be a persona to join.

**Independent Test**: Author a self-link record whose initiating session holds
the surviving persona and confirm it validates; change the session to a
different persona and confirm it fails. Author a merge naming both prior
subjects and confirm it validates; drop one and confirm it fails naming the
dropped subject. Author a record whose basis is an attribute match and confirm
it fails against the bases read from the contract.

**Acceptance Scenarios**:

1. **Given** a link record, **When** it names neither an initiating human nor
   an approving administrator, **Then** validation fails and the link is not
   treated as established.
2. **Given** a new federated identity presenting an attribute that matches an
   existing persona, **When** a record claims that match as its basis, **Then**
   validation fails — the admissible bases are an explicit user action and a
   governed administration approval, and nothing else.
3. **Given** an approved merge, **When** a prior subject identifier is absent
   from the record, or resolves to anything other than the surviving persona,
   **Then** validation fails.
4. **Given** a self link, **When** the initiating session held a different
   persona from the one the identity joins, **Then** validation fails.
5. **Given** a merge record, **When** its subjects resolve to personas in
   different broker instances, **Then** validation fails — personas do not span
   instances.

---

### User Story 3 - A governed record names a human the system can name (Priority: P3)

A governed act — a ratification, a gate action, an administration apply —
records its actor as the broker-issued opaque subject, its issuer, and the
display name in force when the record was written. A record written before the
broker keeps its bare username, is marked as predating the persona boundary,
and is resolved through an explicitly recorded mapping only where a specific
record needs attribution.

**Why this priority**: It is what closes the gate console's forgeable-actor and
unauthenticated-`--actor` risks, and it is the field shape that costs a schema
major if guessed wrong (design OQ-3). It is third because it consumes the
persona the first two stories establish.

**Independent Test**: Author a broker-asserted actor reference and confirm it
validates; substitute the display name, an email address, or a bare username
the corpus records as pre-broker, and confirm each fails for its own reason.
Author a pre-broker reference and its mapped counterpart and confirm both
validate and that neither presents as a broker-asserted persona.

**Acceptance Scenarios**:

1. **Given** a governed act by a persona, **When** the actor reference carries
   the issuer, the opaque subject and the display name at record, **Then** it
   validates, and a later display-name change does not change who the record
   names.
2. **Given** an actor reference, **When** the identifier position holds a
   display name, an email address, or an upstream account name, **Then**
   validation fails naming what was substituted.
3. **Given** a record written before the broker, **When** it carries a bare
   username, **Then** it is either marked as predating the persona boundary or
   resolved through a recorded mapping, and it is never presented as a
   broker-asserted persona.
4. **Given** a governed record, **When** it names a broker service client as
   its human actor, **Then** validation fails and the act is unattributed
   unless a persona can be established.

---

### Edge Cases

- **A workload that needs authority.** It receives a `credential-contracts`
  grant or an `openxwallet` holder; no persona is created for it, and a service
  client provisioned for a surface's OIDC tokens is TRANSPORT — no membership
  as authority, never the actor of a governed act.
- **A configuration export used as reviewed desired state.** Credential-free by
  construction, never by redaction: the value scan covers names, values, and
  values reassembled from adjacent chunks, because a wrapped export or a
  deliberate split defeats a per-value scan.
- **A population that must not co-reside.** Served by a dedicated instance, not
  by a partition inside a shared one. The co-residence gate of 2026-08-21 found
  exactly one — HealthLinc clinical patients — so the escalation path is
  exercised by the corpus rather than described.
- **A single-organization deployment with no operator layer above it.** Runs
  its own broker with no restriction at all and is conformant; the contract's
  silence on instance count is load-bearing in both directions.
- **A read-only surface that later gains a write action.** Blocked until the
  surface resolves authorization in the governed layer, and the posture
  declaration is what makes that a visible change rather than an unremarked
  commit.
- **A surface with no broker at all.** Refused by nothing. No capability
  requires a domain to adopt a broker.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The contracts MUST define a persona assertion carrying the
  issuing broker instance, the stable opaque subject, the display name, the
  linked upstream identities (provider id plus upstream subject only), the
  organization memberships, and the assertion time — and MUST NOT provide any
  property, at any depth, in which a role, group, grant, project, stack, layer,
  domain or subject could be recorded.
- **FR-002**: The contracts MUST define an organization carrying the company
  role (`tenant` | `served`), routed domains, federated upstream provider
  references, and AT MOST ONE resolvable reference to the governed record it
  corresponds to, and MUST refuse a second reference or any projection of the
  referenced record's contents.
- **FR-003**: Membership MUST be expressible only as association: an
  organization membership carries an organization and a date, and no authority
  term. A surface MUST NOT be able to declare that authorization resolves in
  broker membership.
- **FR-004**: The contracts MUST define an actor subject reference carrying the
  issuer, the opaque subject, the display name at record, and a provenance
  discriminator separating a broker-asserted persona, a pre-broker bare
  username, and a mapped historical actor — with the wrong combinations
  unrepresentable.
- **FR-005**: The contracts MUST refuse a display name, an email address or an
  upstream account name in the identifier position, and MUST refuse provenance
  `broker_asserted` for a bare username the corpus records as pre-broker.
- **FR-006**: The contracts MUST define an identity link record whose mode
  (`self_link` | `admin_merge`) REQUIRES ITS ACTOR BY SHAPE, MUST admit exactly
  two bases (an explicit user action and a governed administration approval),
  and MUST carry every pre-merge subject with the surviving subject it remains
  resolvable to.
- **FR-007**: The contracts MUST refuse a self link initiated from a session
  not already holding the surviving persona, and MUST refuse a link record
  whose subjects resolve to personas in different broker instances.
- **FR-008**: The contracts MUST define a broker service-client declaration
  carrying the surface served, the stated reason OIDC tokens are required, a
  `credential-contracts` requirement reference, and required constant
  declarations that the client is transport, is never the actor of a governed
  act, and holds no organization membership as authority. No persona subject
  and no governed record's actor may be a declared client.
- **FR-009**: Every credential the contracts touch MUST be expressible only as
  a reference to a `credential-contracts` requirement naming its holder and the
  place custody is declared, and no schema may provide a property in which a
  credential VALUE could be recorded.
- **FR-010**: The contracts MUST define a surface adoption carrying the
  declared authorization posture (`authenticated_persona` |
  `resolved_authorization`), whether governed write actions are offered, the
  governed decision point when they are, the retired credential when adoption
  replaces a shared static secret, and the isolation the served population
  requires.
- **FR-011**: A surface offering a governed write action MUST be unable to
  declare the weaker posture, and MUST name its governed decision point.
- **FR-012**: An adoption naming a replaced shared credential MUST record it
  retired, with the time of retirement.
- **FR-013**: The contracts MUST express isolation escalating to a DEDICATED
  broker instance, MUST refuse a restricted population served by a shared
  instance, and MUST remain silent on instance count — a dedicated instance
  with no restriction stays conformant.
- **FR-014**: A single validator MUST enforce every rule above, following the
  repository's existing `scripts/validate-*.py` shape and exit-code convention
  (0 clean, 1 findings, 2 harness error), validating the persona-assertion and
  organization property sets as a CLOSED ALLOW-LIST derived from the schemas
  rather than as a denylist of forbidden names.
- **FR-015**: The validator MUST detect credential values BY CLASS across every
  packaged example, including values reassembled from adjacent chunks.
- **FR-016**: The validator MUST read the canonical layer ids and reserved
  layer terms from `contracts/policies/layer-vocabulary.yaml`, and the
  admissible link bases and authorization resolution point from the family's
  own schemas, at run time rather than restating them.
- **FR-017**: The fixture corpus MUST carry a NEGATIVE CONFIRMATION for each of
  the eighteen named violations and for each of the nine requirements — a
  recorded probe proving the check fails on the violation it exists to catch,
  and fails for that reason rather than incidentally.
- **FR-018**: The validator MUST refuse a negative fixture that validates
  cleanly AND one that fails for the wrong reason, and MUST refuse a corpus
  where a requirement has no probe or a fixture claims a requirement that does
  not exist.
- **FR-019**: No broker, realm, organization, deployment, credential, persona
  or user store is created; no existing capability is modified; no
  authorization model is defined; and no surface's authentication changes.

### Key Entities

- **Persona assertion**: the issuing instance, the opaque subject, the display
  name, the linked upstream identities, the organization memberships. Nothing
  else, at any depth.
- **Broker organization**: a company boundary — role, routed domains, federated
  providers by reference, and at most one pointer to its governed record.
- **Actor subject reference**: what a governed record embeds when it names a
  human actor, with provenance separating asserted, pre-broker and mapped
  actors.
- **Identity link record**: a self link or an administrative merge, each
  requiring its actor by shape, carrying every prior subject and the survivor
  it resolves to.
- **Broker client declaration**: a service client declared as transport, with
  its stated token need and its credential requirement by reference.
- **Surface adoption**: the declared posture, the instance and its deployment,
  the retired shared secret, and the isolation the served population requires.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All eighteen named violations are refused by the validator, each
  with a recorded probe naming the reason it was refused — zero pass silently —
  and every one of the nine requirements carries at least one probe.
- **SC-002**: A reader of any conformant persona assertion can determine,
  without consulting anything outside the record, who the persona is and which
  organizations it belongs to — and can determine that the record says nothing
  about authority, because there is no property in which it could.
- **SC-003**: The consuming changes can be written entirely in this
  vocabulary: the workbench adoption (posture plus a retired shared secret),
  the gate-console actor binding (a structured actor reference), and a
  dedicated-instance client (isolation by instance) each have a packaged
  positive.
- **SC-004**: A domain adopting no broker is refused by nothing — measured by
  the existing capabilities' fixtures continuing to pass untouched and by no
  validator requiring an identity-brokering record to exist.
- **SC-005**: The validation bar is green with no new findings:
  `scripts/validate-identity-brokering.py . --strict` reports 0 errors and 0
  warnings, `openspec validate --all --strict` passes, and doc-health reports
  no new finding against the change or the promoted supporting docs.
- **SC-006**: Every finding code the corpus exercises is load-bearing —
  recorded by a red proof that suppresses each code in turn and shows the
  corpus goes red.

## Assumptions

- **The `actor_subject` shape is the structured reference** (change task 2.3,
  design OQ-3's recommendation, adopted as written at ratification). A bare
  subject is ambiguous without knowing who issued it, and multiple instances
  are an expected state rather than a hypothesis. Recorded as settled in
  `research.md`.
- **History is marked at the boundary and mapped on demand** (change task 2.3,
  design OQ-1's recommendation, adopted as written). Never a blanket backfill.
  A pre-broker record stays readable and never presents as a persona. Recorded
  as settled in `research.md`.
- **`served` is this family's spelling of the served company boundary, and it
  bridges to the canonical `subject` layer.** The change's task 1.2 fixes the
  enumeration as `tenant | served`; `contracts/policies/layer-vocabulary.yaml`
  declares the canonical layer ids as `subject | tenant | domain`. The bridge
  (`tenant` -> `tenant`, `served` -> `subject`) is contract content, its targets
  are checked against the policy at run time, and the policy's reserved terms
  (`customer`, `client`) are refused from the same source. Full reasoning in
  `research.md`.
- **The opaque subject carries a length floor.** A broker-issued subject is not
  a name, and the floor is what makes a bare upstream username unrepresentable
  in the identifier position rather than merely discouraged. Reasoning and the
  accepted cost in `research.md`.
- **A credential reference names where custody is declared rather than
  restating it.** This family defines no custody vocabulary; composition means
  the `credential-contracts` record is the declaration and this record is the
  pointer.
- **Contract registration follows the repository's release discipline.** New
  schemas are registered in `contracts/manifest.yaml` with per-file digests, a
  `contracts/CHANGELOG.md` entry, the README contract index rows, and a bundle
  version allocated at realization rather than reserved here — the change's task
  1.11, executed at the next additive bundle cut and outside this feature's
  authoring surface.
