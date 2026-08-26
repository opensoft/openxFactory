# client-identity-roster — add-client-identity-roster deltas

## ADDED Requirements

### Requirement: Identities are enumerated by admission surface, not by product name
Governed identities in a client tenant SHALL be enumerated against
**admission surfaces**, where an admission surface is defined extensionally
as a provider-side administrative surface that owns an independent admission
act and its own scoping mechanism. A roster SHALL NOT enumerate identities
against product or marketing names, because provider boundaries overlap
(channel files in a collaboration workload are sites in a content workload)
while admission acts do not. The closed surface vocabulary SHALL be extended
only by the change that governs a new surface, and each surface entry SHALL
name the admission act and scoping mechanism that make it a surface.

#### Scenario: Two product names share one admission act
- **WHEN** two provider product names are administered through a single admission act with a single scoping mechanism
- **THEN** they are one admission surface in the roster
- **AND** an identity serving both is not a spanning identity

#### Scenario: One product name has two admission acts
- **WHEN** a provider product is admitted through two independent admission acts with different scoping mechanisms
- **THEN** each act is its own admission surface

### Requirement: Identity uniqueness is keyed on surface, class, blast-radius unit and duty
Roster uniqueness SHALL be keyed on the tuple (owning domain, admission
surface, authority class, blast-radius unit, duty). Authority class SHALL be
one of `observe` or `mutate`. Two entries sharing that whole tuple SHALL be a
finding; entries differing in ANY element SHALL be conformant, so that
per-blast-radius-unit identities and duty-separated identities are permitted
rather than penalised. A roster SHALL NOT force reuse of one identity across
blast-radius units, because doing so converts a bound the provider enforces
into a bound only gate logic enforces.

#### Scenario: One identity per environment where the provider offers a per-environment principal
- **WHEN** a provider offers a principal scoped to one blast-radius unit and a domain governs two such units
- **THEN** two entries differing only in blast-radius unit are conformant
- **AND** neither is reported as an overlap

#### Scenario: Duty separation inside one surface and class
- **WHEN** a domain deliberately separates duties inside one surface and authority class
- **THEN** the entries differing only in duty are conformant

#### Scenario: A genuine duplicate
- **WHEN** two entries share owning domain, admission surface, authority class, blast-radius unit and duty
- **THEN** the check reports the duplicate naming the full tuple

### Requirement: Structural scoping is preferred and its absence must be declared
Each entry SHALL declare, per admission surface, whether a principal scoped
to the governed blast-radius unit is available, and MAY declare that a bound
is enforced by gate logic only where no such principal exists, recording the
provider reason. Where such a principal IS available it SHALL be used and
the bound SHALL be recorded as provider-enforced. A bound recorded as
provider-enforced when no per-unit principal exists SHALL be a finding.

#### Scenario: A per-unit principal exists and is unused
- **WHEN** a surface offers a principal scoped to the governed blast-radius unit and an entry declares logical enforcement instead
- **THEN** the check reports the finding naming the available principal

#### Scenario: No per-unit principal exists
- **WHEN** a surface offers no principal scoped to the governed blast-radius unit
- **THEN** the entry declares that absence with the provider reason
- **AND** the entry declares the gate obligation enforcing the narrower bound

### Requirement: Provider-forced breadth is declared, never silently absorbed
An entry SHALL declare any breadth the provider forces upon it — the spanned
admission surfaces or the achieved authority class — together with the
provider reason that no narrower permission exists and the gate obligation
that bounds it. This applies where a provider offers no permission narrow
enough to keep an identity within one admission surface or within its
intended authority class. Declared forced breadth SHALL be conformant;
undeclared breadth SHALL be a finding.
A roster SHALL NOT invalidate a deliberately narrow identity merely because
the provider's own permission granularity is coarser than the roster axis.

#### Scenario: A single provider permission spans surfaces
- **WHEN** the narrowest available permission reaches more than one admission surface
- **THEN** the entry declares the spanned surfaces, the provider reason, and the gate obligation
- **AND** the entry is conformant

#### Scenario: Breadth is present but undeclared
- **WHEN** an identity's granted permissions reach a surface the entry does not declare
- **THEN** the check reports undeclared reach naming the surface and the permission

### Requirement: Destructive authority holds no provider identity by default
A roster SHALL NOT carry a destructive authority class. Destructive action
authority SHALL remain an action class governed at the gate, whose default
is an externally authorized actor with no factory-held provider identity. A
destructive-capable identity SHALL be admissible only where the provider
demonstrably offers a delete-scoped permission distinct from its write
permission, declared with that demonstration; absent that, destructive
capability rides the `mutate` entry's declared achieved class and its gate
obligation.

#### Scenario: A destructive identity is proposed
- **WHEN** a roster entry proposes an identity for destructive acts without demonstrating a delete-scoped permission distinct from write
- **THEN** the entry is invalid and the finding names the missing demonstration

#### Scenario: Write permission implies delete
- **WHEN** a provider's write permission necessarily includes delete
- **THEN** the destructive capability is declared as achieved class on the `mutate` entry with its gate obligation
- **AND** no separate destructive identity is created

### Requirement: Admission is a verified list, and consent is never recorded as access
Each entry SHALL carry admission as a LIST of acts, each declaring the
surface, the act performed in that surface's own administrative console, the
scope that act achieves, whether the resulting bound is provider-enforced or
logic-enforced, and evidence of a successful call on that surface with the
time it was verified. Provider consent alone SHALL NOT be recorded as
access. An admission act with no verification evidence SHALL be recorded in
a distinct unverified state and SHALL NOT count as admission. The identity's
effective reach SHALL be the union of its verified admission acts.

#### Scenario: Consent exists but no admission act is recorded
- **WHEN** an entry declares provider consent and no admission act
- **THEN** the entry is invalid and the finding states that consent is not admission

#### Scenario: An admission act is asserted but never verified
- **WHEN** an admission act carries no evidence of a successful call on that surface
- **THEN** it is recorded as unverified and excluded from effective reach

#### Scenario: One surface bounds structurally while another does not
- **WHEN** an identity is admitted through one act scoped to the blast-radius unit and another act with no scope selector
- **THEN** both acts appear in the list with their own achieved scopes and enforcement modes
- **AND** the effective reach is the union, not the narrower act

### Requirement: Achieved authority is derived from granted permissions and its excess declared
Each entry SHALL record its granted permissions in provider-native
identifiers, and SHALL declare both the intended authority class and the
achieved authority class derived from those permissions. Where achieved
exceeds intended, the entry SHALL declare the excess with the reason no
narrower permission exists and the mechanism that bounds it, and the
identity's stated purpose SHALL NOT describe a narrower authority than it
achieves.

#### Scenario: An identity's purpose understates its reach
- **WHEN** an entry's stated purpose or name describes observation while its granted permissions achieve mutation
- **THEN** the check reports the class excess naming the permissions that achieve it
- **AND** the entry is invalid until the excess and its bounding mechanism are declared

#### Scenario: Achieved equals intended
- **WHEN** granted permissions achieve exactly the intended class
- **THEN** no excess declaration is required

### Requirement: A gate obligation resolves to an enforced, tested gate
Every gate obligation named by an entry SHALL resolve to an existing gate in
the owning domain's governed workflow records, and SHALL name a test that
proves refusal of a target outside the governed blast-radius unit. An
obligation that resolves to nothing, or that names no such test, SHALL be a
finding, because an unenforced obligation converts an undetected widening
into a documented one.

#### Scenario: An obligation names no resolvable gate
- **WHEN** an entry's gate obligation does not resolve to a gate in the owning domain's workflow records
- **THEN** the check reports the unresolvable obligation

#### Scenario: An obligation has no refusal test
- **WHEN** a gate obligation resolves but names no test proving refusal of an out-of-unit target
- **THEN** the check reports the missing enforcement test

### Requirement: Residency is a declared model with per-model obligations
Each entry SHALL declare its identity kind, the tenant its registration is
homed in, and the tenants its principals occupy, and SHALL declare a
residency model. A client-tenant-single model makes the client the
blast-radius unit for identity compromise. A vendor-tenant-multi model —
one registration consented by many clients, whose principal lands in each
client tenant — SHALL additionally declare a tenant allow-list enforced at
token validation, per-client authorization state, per-client revocation
evidence, and a statement that one credential set spans every consenting
client; and each affected client's consent instrument SHALL be amended to
disclose that shared-identity access shape. A vendor-homed registration
SHALL NOT be declared client-resident on the grounds that its principal
appears in the client tenant.

#### Scenario: A multi-tenant registration is declared client-resident
- **WHEN** an entry homes its registration outside the client tenant and declares a client-tenant-single model
- **THEN** the entry is invalid and the finding names the registration's home tenant

#### Scenario: A vendor-tenant-multi identity is governed
- **WHEN** an entry declares a vendor-tenant-multi model
- **THEN** it declares the allow-list, per-client authorization state, per-client revocation evidence, and the cross-client credential-span statement
- **AND** each affected client's consent instrument carries an amendment disclosing the shared-identity access shape

### Requirement: Entries carry a lifecycle so a roster is a projection over time
Each entry SHALL carry a lifecycle state of `planned`, `enrolled`, or
`retired`, and SHALL carry a standing-credential attestation stating that no
credential persists outside an approved grant window. A roster SHALL NOT be
read as requiring every entry to be enrolled at once, and a retired entry
SHALL retain its record.

#### Scenario: A capability is ratified before its identity is enrolled
- **WHEN** a capability ratifies and its identity has not yet been created in the client tenant
- **THEN** the entry exists in `planned` state and is not reported as missing

#### Scenario: A standing credential is found
- **WHEN** an identity holds a credential outside an approved grant window
- **THEN** the attestation is false and the check reports it against that entry

### Requirement: Every entry names both its ratified capability and its consent instrument
Every entry SHALL name the domain-qualified ratified capability that
justifies the identity and the consent instrument that authorizes standing
inside the client's tenant, and the instrument citation SHALL resolve to an
instrument in force. Our own capability ratification SHALL NOT by itself
justify an identity in another party's tenant. A `mutate` entry whose
capability is not ratified SHALL block, not merely report.

#### Scenario: An entry cites a capability but no instrument
- **WHEN** an entry names a ratified capability and no consent instrument
- **THEN** the entry is invalid and the finding states that consent authorizes tenancy

#### Scenario: A mutate identity has no ratified capability
- **WHEN** an entry declares `mutate` authority and names no ratified capability
- **THEN** the owning domain's conformance gate fails rather than emitting a report-only finding

### Requirement: Identity drift reports, never remediates, and withholds our own credential
Drift detection over client-tenant identities SHALL NOT create, modify,
widen, narrow, or remove any identity, permission, or admission, and SHALL
NOT trigger automated remediation — automated remediation inside a client
tenant would itself require a broadly privileged identity there. Where drift
is open against an identity, grant issuance for that identity SHALL be
refused as an issuance precondition, because withholding our own credential
is the lever we own and is not a mutation of the client's tenant.

#### Scenario: Drift is detected
- **WHEN** the check finds an identity, permission, or admission diverging from the roster
- **THEN** it records the roster value and the observed value and performs no mutation

#### Scenario: A grant is requested against a drifted identity
- **WHEN** grant issuance is attempted for an identity with an open drift finding
- **THEN** issuance is refused naming the finding

### Requirement: The roster composes across domains from published fragments
The roster for a client SHALL be assembled from fragments published by each
domain factory holding identities in that client's tenant, and cross-domain
findings SHALL be limited to genuinely shared identity material and
undeclared cross-domain reach. Two domains each holding their own identity
on the same admission surface and authority class SHALL NOT be a finding,
because separate identities are what preserve provider-side attribution and
independent revocation.

#### Scenario: Two domains hold separate identities on one surface
- **WHEN** two domain factories each declare their own identity for one admission surface and authority class in one client tenant
- **THEN** both entries are conformant and appear in the assembled roster

#### Scenario: Two domains share one identity
- **WHEN** two domains declare entries naming the same identity
- **THEN** the check reports shared identity material naming both domains
