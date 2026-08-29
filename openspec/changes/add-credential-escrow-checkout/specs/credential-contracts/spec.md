# credential-contracts

## MODIFIED Requirements

### Requirement: Canonical credential record shapes
Credential contract records SHALL validate against the canonical
`contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns
the six record kinds: `xfactory_credential_requirements`,
`xfactory_runtime_capability_grant_template`,
`xfactory_credential_binding_template`,
`xfactory_credential_broker_contract`,
`xfactory_credential_audit_policy`, and
`xfactory_credential_escrow_entry`. Domain content — credential families,
scopes, providers, workflow and action names — is domain-local; the schema
constrains shape only, and semantic invariants remain owned by the
credential access model.
The schema SHALL additionally own an `issuance_preconditions` vocabulary: a
CLOSED set of neutral precondition tokens that a credential requirement
record MAY declare, each naming a governed condition which must hold before a
grant is issued against that requirement. Its first member is the
ROSTER-DRIFT precondition — an open drift finding recorded against the roster
entry covering the identity a grant would name blocks issuance of that grant.
Declaring a precondition is optional and additive; declaring a member outside
the vocabulary is invalid, because a free-text precondition riding a schema
that neither declares nor forbids it is unenforceable and invisible to every
consumer of the pinned contract. Precondition EVALUATION — which drift
records exist and who reads them — stays with the owning contract families
and the domain mint surface that issues the grant; this schema owns the
vocabulary and the declaration shape only.
The schema SHALL FURTHER own an ADDITIVE OPTIONAL `escrow:` block on
`xfactory_credential_binding_template`, whose shape and meaning are stated in
the escrow-relationship requirement, and the sixth record kind
`xfactory_credential_escrow_entry` the block refers to. BOTH ADDITIONS ARE
ADDITIVE AND NEITHER NARROWS AN EXISTING SHAPE: a binding template that
declares no `escrow:` block remains valid unchanged, and a repository holding
none of the sixth kind remains conformant, so every consumer pinned at the
prior bundle stays conformant until it upgrades.

#### Scenario: A domain authors a credential contract
- **WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the six kinds
- **THEN** it MUST validate against the pinned canonical schema

#### Scenario: A file lacks the envelope
- **WHEN** a credentials file has no `kind`
- **THEN** the validator MUST report an error

#### Scenario: A domain policy record is present
- **WHEN** a credentials file carries a kind outside the six contract kinds
- **THEN** the validator MUST skip it with notice — such kinds are candidates for future promotion, not silent failures

#### Scenario: A requirement record declares the roster-drift precondition
- **WHEN** a credential requirement record declares the roster-drift member of `issuance_preconditions`
- **THEN** it validates, and the declaration is the neutral expression of the ratified refusal: an open drift finding on the covering roster entry blocks issuance of a grant naming that identity
- **AND** a requirement record declaring no preconditions remains valid, because the vocabulary is optional and additive

#### Scenario: A precondition outside the vocabulary
- **WHEN** a requirement record declares an `issuance_preconditions` member that is not in the closed vocabulary
- **THEN** the validator MUST report an error naming the closed vocabulary rather than accepting an unenforceable free-text condition

#### Scenario: The neutral layer proves the precondition by fixture
- **WHEN** the neutral realization of the roster-drift precondition is demonstrated
- **THEN** the demonstration is a conformant requirement-record fixture declaring it, because the neutral layer holds no producer of live drift findings and issues no grant itself
- **AND** at this capability's modification no live drift producer existed anywhere in the family, so the fixture is the whole neutral criterion and live refuse-then-allow behaviour is proven at the domain mint surface as a follow-up

#### Scenario: A binding template predating the escrow block is revalidated
- **WHEN** an existing `xfactory_credential_binding_template` carrying no `escrow:` block is validated against the schema that owns the sixth kind
- **THEN** it MUST validate unchanged, because the addition is optional and additive and a pinned consumer is not obliged to move

#### Scenario: The sixth kind appears under `credentials/`
- **WHEN** a repository adds a file carrying `kind: xfactory_credential_escrow_entry`
- **THEN** it is a contract record validated against the canonical schema, not a domain policy record skipped with notice

## ADDED Requirements

### Requirement: Break-glass escrow checkout is an administration-tier custody act
A break-glass checkout of an escrow decryption identity SHALL be governed as an
administration-tier credential custody act under the canonical
`credential-contracts` record shapes — a requirement record naming the identity,
a binding recording its custody, a time-boxed and scope-named runtime capability
grant, and an audit policy — with human AND domain approval recorded BEFORE the
grant issues, and an audit record for every checkout carrying an evidence
reference to the incident or drill that authorized it.

THE ESCROW DECRYPTION IDENTITY IS ITSELF A CREDENTIAL, and that is the whole of
why this requirement needs no new record shape. Its durable private half SHALL
live only in an approved secret provider, exactly as
`roles-authority-model`'s administration-tier custody requires of an
administration App's private key; its checkout SHALL be short-lived and scoped
to the named client escrow scope it opens; and a grant whose scope exceeds the
objects the authorizing incident or drill names SHALL be narrowed or refused.

THE AUTHORIZING ROLE IS AN ADMINISTRATION-TIER ONE. A client-layer credential
steward — a role that holds credential REFERENCES and never secrets — SHALL NOT
be the authorizing authority for an escrow checkout, because the checkout grants
custody of values rather than custody of references, and a role defined never to
hold the second cannot approve release of the first.

WRITING ESCROW IS NOT A CHECKOUT AND SHALL NOT REQUIRE ONE. Encryption needs only
the committed public recipient, so a routine escrow write — at credential
creation or rotation — SHALL proceed with no access to any private half. A
request for a checkout in order to WRITE escrow is over-scope on its face.

#### Scenario: A checkout is requested without recorded approval
- **WHEN** a runtime capability grant for an escrow decryption identity is requested with no human and domain approval recorded
- **THEN** grant issuance MUST be rejected, on the same rule that governs any other administration-tier custody act

#### Scenario: A checkout is granted
- **WHEN** the checkout grant issues
- **THEN** a runtime capability grant and a credential access audit record are produced
- **AND** the audit record's evidence reference identifies the incident or drill that authorized the checkout, never the checkout's own request

#### Scenario: A reference-holding client-layer role authorizes a checkout
- **WHEN** a client-layer credential steward, whose records hold references and never secrets, is named as the approving authority for an escrow checkout
- **THEN** the authorization MUST be rejected, because the checkout releases values into custody the role is defined never to hold

#### Scenario: A routine escrow write requests a checkout
- **WHEN** a credential is created or rotated and the escrow write is proposed as a reason to check out an escrow decryption identity
- **THEN** the request MUST be refused as over-scope; the write encrypts to the committed public recipient and touches no private half

### Requirement: A break-glass checkout leaves three correlated records
A break-glass escrow checkout SHALL leave three records sharing ONE correlation
identifier: the retroactive `client_infrastructure_request` that accounts for the
out-of-band action, a credential access audit record that ENUMERATES EVERY escrow
object decrypted under the checkout, and the incident or drill record that
authorized it. A checkout that leaves fewer than three, or three that do not
correlate, SHALL be a first-class finding.

THE ENUMERATION IS THE LOAD-BEARING FIELD, because everything downstream reads
it: it is the rotation worklist, it is the blast-radius statement, and it is the
only artifact that distinguishes what was decrypted from what was merely
reachable. A break-glass audit policy record SHALL therefore declare that
enumeration among its `minimum_fields`, so the obligation is carried by the
promoted `xfactory_credential_audit_policy` shape rather than asserted in prose.

NO NEW REQUEST KIND IS INTRODUCED. The retroactive request is a
`client_infrastructure_request` — `request_type: remediation` fits an
after-the-fact accounting of an out-of-band change — because
`deployment-handoff-boundary` already rules that a new record kind SHALL NOT be
introduced to carry a crossing, and a retroactive crossing is still a crossing.

#### Scenario: The audit under-reports what was decrypted
- **WHEN** a checkout decrypts three escrow objects and the audit record names one
- **THEN** the audit is non-conforming, because the enumeration is what the rotation obligation and the blast-radius statement are both computed from

#### Scenario: A drill leaves the same evidence as an incident
- **WHEN** a rehearsed drill checks out an escrow decryption identity with no incident in progress
- **THEN** all three records are still produced and still correlate, and the drill record stands where the incident record would

#### Scenario: The evidence set correlates
- **WHEN** the correlation audit joins observed break-glass actions against accepted requests
- **THEN** each checkout resolves to its retroactive request, its audit record and its authorizing incident or drill by one shared correlation identifier

#### Scenario: An audit policy omits the enumeration
- **WHEN** a break-glass credential audit policy does not declare the decrypted-object enumeration among its minimum fields
- **THEN** the policy MUST be rejected, because a checkout under it could conform while saying nothing about what it opened

### Requirement: The retroactive request for a break-glass checkout lands inside a two-bound policy window
A retroactive `client_infrastructure_request` for a break-glass escrow checkout SHALL be OPENED — existing and carrying the checkout's correlation identifier — within 24 HOURS of the checkout grant's expiry or revocation, whichever comes first, and SHALL reach an accepted terminal disposition with after-use rotation evidence attached within 5 BUSINESS DAYS of that same instant.

BOTH BOUNDS RUN FROM THE CHECKOUT'S END, NEVER ITS START, so a long checkout buys
no later filing.

THE WINDOW DOES NOT TOLL. An unavailable approver, a pending change window, or
any other wait SHALL be recorded as a `conditions` entry on the request —
orthogonal to its status, exactly as the request contract already models holds —
and SHALL NOT extend either bound. Exceeding either bound SHALL be a first-class
finding under out-of-band detectability, and a late filing SHALL NOT retroactively
authorize the act: the request still correlates the change, and the lateness is
its own separate finding.

THE TWO BOUNDS ARE DIFFERENT ACTS AND THAT IS WHY THERE ARE TWO. Opening the
record is unilateral, takes minutes, needs no counterparty, and is transcribed
from the audit record the operator already holds — so it is bounded in calendar
hours. Reaching disposition needs a second party's acceptance AND needs rotation
to have COMPLETED, which can require a change window on a client surface — so it
is bounded in business days.

#### Scenario: A break-glass action is accounted for on time
- **WHEN** an operator's checkout grant is revoked at the end of an incident and a `client_infrastructure_request` carrying its correlation identifier is opened the same day
- **THEN** the opening bound is met, and the change correlates at the next evidence-correlation audit rather than surfacing as an unstamped-change finding

#### Scenario: The disposition waits on an approver
- **WHEN** the retroactive request cannot be accepted because the approving authority is unavailable
- **THEN** the wait is recorded as a condition on the request and the 5-business-day bound still runs; the condition does not extend it

#### Scenario: The request lands late
- **WHEN** a retroactive request for a break-glass checkout is opened after the 24-hour bound
- **THEN** the change correlates once filed, AND the lateness is recorded as its own finding, because a late account is still an account and is not an authorization

#### Scenario: A long checkout is used to defer filing
- **WHEN** a checkout grant is held open across several days and the filing is timed from its start
- **THEN** the filing is non-conforming; both bounds run from expiry or revocation

### Requirement: After-use rotation covers every credential decrypted
Every credential DECRYPTED under a break-glass escrow checkout SHALL be rotated,
and completion of that rotation SHALL be the evidence on which the retroactive
request reaches its accepted disposition. The audit record's decrypted-object
enumeration IS the rotation worklist; a credential that was reachable under the
checkout but not decrypted SHALL NOT be swept into it, because an obligation that
scales with reachability rather than with exposure is one nobody completes.

THE ESCROW IDENTITY ITSELF ROTATES ON A NARROWER TRIGGER: only where its private
half LEFT approved custody onto a non-ephemeral host. An identity fetched into
ephemeral scope and destroyed with it has not left custody and SHALL NOT trigger
its own rotation, and the record SHALL say so. A private half written to durable
storage on an operator workstation, a shared runner, or any host that outlives
the checkout HAS left custody, and the already-promoted exposure rule then applies
at full force and unmodified: the identity MUST be rotated AND every credential
encrypted to it MUST be rotated, because historical repository ciphertext remains
recoverable with the exposed identity.

#### Scenario: A checkout decrypts part of a client's escrow
- **WHEN** a checkout decrypts 3 objects of a client scope holding 40
- **THEN** exactly those 3 credentials MUST be rotated, and the other 37 MUST NOT be swept in

#### Scenario: The identity stays in ephemeral scope
- **WHEN** the escrow decryption identity is fetched into ephemeral job or session scope and destroyed with it
- **THEN** the identity itself is not rotated, and the retroactive request records that custody was not left

#### Scenario: The identity lands on a durable host
- **WHEN** the private half of an escrow decryption identity is written to durable storage on a host that outlives the checkout
- **THEN** the identity MUST be rotated AND every credential encrypted to it MUST be rotated, under the exposure rule this capability already carries

#### Scenario: Rotation is incomplete at disposition
- **WHEN** the retroactive request is proposed for acceptance with rotation of an enumerated credential outstanding
- **THEN** it MUST NOT reach its accepted disposition, because rotation completion is the disposition's evidence

### Requirement: Escrow recipients are disjoint from runtime decryption controllers
Every escrowed object SHALL be encrypted to AT LEAST TWO recipients — one
per-client escrow recipient and one operator root recipient — and the escrow
recipient set SHALL be DISJOINT from every runtime decryption-controller recipient
in the family. A recipient that decrypts running workloads SHALL NOT decrypt
escrow, and a proposal to reuse one as the other MUST be rejected.

THIS IS THE PROMOTED PER-BOUNDARY RECIPIENT RULE APPLIED, NOT A NEW ONE. Escrow is
a stronger trust boundary than any environment: the runtime store deliberately
holds derivatives where escrow holds the recoverable values, so escrow is the
superset. Reusing a runtime controller's recipient would silently promote a
controller compromise — which this capability already defines as compromise of
every secret that controller can decrypt — into a whole-estate compromise, which
is precisely the event escrow exists to survive.

DRILLS ARE RESTRICTED TO THE PER-CLIENT RECIPIENT. The operator root is a
last-resort recipient, and a rehearsal that uses it has not rehearsed the path a
real per-client recovery takes. THE ROOT'S COST IS RECORDED RATHER THAN HIDDEN:
its worst-case blast radius is every client, and that is the accepted price of
surviving loss of a single per-client key.

#### Scenario: A live runtime recipient is proposed for escrow
- **WHEN** the age recipient a running reconciler already uses to decrypt workload secrets is proposed as an escrow recipient
- **THEN** the binding MUST be rejected, because escrow is a stronger trust boundary and the runtime controller would gain the recoverable values

#### Scenario: An object carries only one recipient
- **WHEN** an escrowed object is encrypted to a per-client recipient alone, or to the operator root alone
- **THEN** it is non-conforming: the first is unrecoverable if the per-client key is lost, and the second forces every routine recovery through the widest-radius key

#### Scenario: A drill uses the operator root
- **WHEN** a rehearsal decrypts using the operator root recipient
- **THEN** it does not discharge the drill obligation, because the per-client recovery path was not exercised

#### Scenario: The root's radius is declared
- **WHEN** the operator root recipient is established
- **THEN** its worst-case blast radius — every client scope it appears on — is recorded as an accepted cost rather than left implicit

### Requirement: A rehearsed drill is the realization gate for the checkout path
The break-glass checkout path SHALL NOT be treated as realized until ONE REHEARSED
DRILL has been performed and recorded end to end, and standing administrative
access SHALL NOT be removed before that drill is recorded.

THE DRILL IS DEFINED BY WHAT IT ACTUALLY EXERCISES, so that a walkthrough cannot
pass for one. It SHALL comprise: a fresh clone holding no prior local state; the
per-client escrow decryption identity retrieved from its custody through a REAL
approval-and-grant cycle rather than a simulated one; at least one escrowed object
DECRYPTED and its recovered value verified against its declared restore target;
AT LEAST ONE LIVE REFUSAL DEMONSTRATED, so that the authorization half is proven
to BITE rather than merely to have been walked past; the three correlated records
produced; after-use rotation dispatched for every enumerated object; and the
retroactive request completed inside the policy window.

ONE DRILL DISCHARGES TWO GATES. Its evidence is this change's archive gate AND the
milestone that `deployment-handoff-boundary`'s phased-never-gapped adoption waits
on; on its recording, a dated milestone removes the standing assignments and that
capability's named, dispositioned exception closes.

#### Scenario: A tabletop walkthrough is offered as the drill
- **WHEN** the rehearsal reviews the runbook without retrieving an identity or decrypting an object
- **THEN** it does not discharge the gate, because neither the custody path nor the recovery was exercised

#### Scenario: The drill succeeds
- **WHEN** a fresh clone plus a real checkout recovers a verified value and the full evidence set is recorded
- **THEN** the checkout path is realized, a dated milestone removes standing administrative assignments, and the boundary's standing-admin exception closes

#### Scenario: Standing access is removed first
- **WHEN** standing administrative assignments are removed before a drill has been recorded
- **THEN** the removal violates the phased-never-gapped rule, because the emergency path has not provably worked

#### Scenario: The drill proves only the success path
- **WHEN** a rehearsal recovers a verified value through a real approval-and-grant cycle but demonstrates no refusal
- **THEN** it does not discharge the gate, because a path that has never been observed to refuse has been shown to work and not shown to govern

#### Scenario: The drill demonstrates a refusal
- **WHEN** the rehearsal attempts a checkout with no recorded human-and-domain approval and the issuance is refused
- **THEN** the refusal is recorded as drill evidence alongside the successful recovery, and the authorization requirement is proven live rather than by fixture alone

#### Scenario: The drill's rotation is treated as optional
- **WHEN** a drill decrypts a real escrowed object and the credential it recovered is not rotated afterwards
- **THEN** the drill does not discharge the gate, because a rehearsal that skips the obligation has rehearsed the wrong procedure

### Requirement: The re-mint test decides MUST-escrow from SHOULD-escrow
Whether a credential MUST be escrowed SHALL be decided by the RE-MINT TEST: a
credential the operator can regenerate from an authority it will STILL HOLD after
total loss of the client estate is SHOULD-escrow; every other credential whose
loss blocks rebuild of the install is MUST-escrow.

A SHOULD-ESCROW CLASSIFICATION SHALL NAME THE RETAINED AUTHORITY IT DEPENDS ON,
and a classification that names none SHALL be read as MUST-escrow. The dependency
is the entire content of the claim: the same credential flips to MUST-escrow the
moment the naming authority moves inside the client estate, because the estate's
loss then takes the re-mint path with it.

#### Scenario: A regenerable deploy key is classified
- **WHEN** a repository deploy key can be regenerated by the operator from an organization ownership the operator holds outside the client estate
- **THEN** it is SHOULD-escrow, and the classification names that ownership as the retained authority it depends on

#### Scenario: The retained authority moves inside the client estate
- **WHEN** the authority a SHOULD-escrow classification named comes to sit inside the client estate
- **THEN** the credential is reclassified MUST-escrow, because the event escrow exists for now destroys the re-mint path too

#### Scenario: A classification names no authority
- **WHEN** a credential is classified SHOULD-escrow with no retained authority named
- **THEN** it MUST be treated as MUST-escrow, because an unnamed re-mint path cannot be verified after the estate is gone

#### Scenario: A vault-held value has no re-mint path
- **WHEN** a credential's only copy is the runtime vault value and no authority can re-mint it
- **THEN** it is MUST-escrow, and its absence from the registry blocks the managed install's readiness

### Requirement: The escrow relationship rides the credential binding, never a custody tier
A credential's escrow relationship SHALL be expressed ONLY as an additive optional `escrow:` block on its credential binding template, which a binding MAY declare and MAY omit; a custody model, an assurance tier, or any other axis SHALL NOT carry an escrow discriminator.

THE BLOCK NAMES THREE THINGS AND NO MORE: the escrow entry that holds the
recoverable value, the escrow scope the entry lives in, and the MUST-escrow or
SHOULD-escrow classification with, for a SHOULD, the retained authority the
re-mint test requires it to name. It carries no value, no recipient private
half, and no restore instruction — those belong to the entry.

THIS IS BRETT'S RATIFIED TRUST-ANCHOR RULING APPLIED WHERE IT POINTED. Escrow
answers "WHO ELSE can obtain this credential", which is orthogonal to the
question a custody axis asks — "can the using host read it". The family already
carries the executable proof of what conflating them costs: the negative fixture
`contracts/trust-anchor/examples/negative/custody-registry-escrow-as-a-custody-tier.yaml`
shows an escrow member forced to declare exactly the same two booleans as the
member above it, because the escrow fact is invisible to that axis. Two members
that differ only in something their axis cannot express make both unreadable,
and the reading that gets lost is the one at the point of use.

THE ADDITION IS OPTIONAL AND ADDITIVE. A binding template declaring no `escrow:`
block remains valid, so the relationship's arrival narrows nothing.

#### Scenario: A binding declares its escrow relationship
- **WHEN** a credential binding template declares an `escrow:` block naming an escrow entry, its scope, and a MUST-escrow classification
- **THEN** it validates, and the credential's escrow relationship resolves from the binding rather than from any custody or assurance axis

#### Scenario: A binding declares no escrow relationship
- **WHEN** a credential binding template carries no `escrow:` block
- **THEN** it remains valid, because the block is optional and additive and its absence asserts nothing

#### Scenario: An escrow discriminator is added to a custody axis
- **WHEN** a custody model, assurance tier, or comparable axis gains a member whose only distinction is that an operator holds a recoverable copy
- **THEN** it MUST be rejected, on the ratified ruling that operator escrow is a relationship on the credential record and not a custody tier

#### Scenario: A SHOULD classification names no retained authority
- **WHEN** an `escrow:` block declares SHOULD-escrow without naming the retained authority its re-mint path depends on
- **THEN** it MUST be rejected, because an unnamed re-mint path cannot be verified after the estate that would have needed it is gone

### Requirement: The escrow entry records what was escrowed and where it restores
An escrow entry record SHALL name its source credential, the runtime target it
restores into, and the escrow artifact holding the recoverable value — and SHALL
carry no secret value, no private decryption identity, and no decrypted output.

THE SHAPE IS THE RUNNING PRIOR ART MADE NEUTRAL, because a contract invented
ahead of practice is a guess and this one has been in service. The entry SHALL
carry: a SOURCE naming the credential's kind, owner and requirement reference,
with non-secret identifying material only (a fingerprint or thumbprint, never
the material it identifies); a RUNTIME TARGET naming the provider coordinates
and secret name the value is restored into; an ESCROW artifact reference naming
its format, its file, and the ENCRYPTED FIELD NAMES it holds; and a RESTORE
declaration naming the target and the structural validations a restore must
pass before the recovered value is trusted.

EVERY FIELD IS NON-SECRET METADATA, AND THAT IS THE POINT RATHER THAN A
SIDE-EFFECT: it is what lets a check verify an escrow estate — that entries
exist, that recipients are the declared ones, that no plaintext is present, that
every entry has a restore target — WITHOUT any decryption capability. Field
names are metadata; field values are not, and an entry naming a value has become
the thing it exists to avoid.

WHERE THE RUNTIME STORE HOLDS A DERIVATIVE, THE ENTRY HOLDS THE RECOVERABLE
VALUE. A runtime vault legitimately holding only a hash of a credential does not
discharge the escrow duty, because a hash restores nothing.

#### Scenario: An entry names its encrypted fields
- **WHEN** an escrow entry names the fields its artifact encrypts, without their values
- **THEN** it validates, because field names are non-secret metadata and are what a decryption-free check reads

#### Scenario: An entry carries a value or a private identity
- **WHEN** an escrow entry carries a secret value, a decrypted output, or a private decryption identity
- **THEN** it MUST be rejected as a raw credential under the rule this capability already carries, which no escrow context relaxes

#### Scenario: An entry names no restore target
- **WHEN** an escrow entry declares a source and an artifact but no runtime target to restore into
- **THEN** it MUST be rejected, because a recoverable value nobody can put back is not escrow

#### Scenario: The runtime store holds only a derivative
- **WHEN** the runtime vault holds a hash or other derivative of a credential and the escrow entry mirrors that derivative
- **THEN** the entry does not discharge the escrow duty, because restoring a derivative restores nothing; the entry MUST hold the recoverable value
