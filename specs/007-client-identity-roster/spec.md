# Feature Specification: Client identity roster neutral contracts and conformance wiring

**Feature Branch**: `007-client-identity-roster`

**Created**: 2026-08-14

**Status**: Draft

**Input**: User description: "client-identity-roster" — realize the ratified
`add-client-identity-roster` OpenSpec change as neutral contract records, a
canonical validator with a negative-confirmation fixture corpus, and the three
conformance wirings the change ratified (blocking intra-repo conformance,
reporting cross-domain composition, grant-issuance refusal on open drift),
together with the `consent-instrument` cascade realization.

**Governing change**: `openspec/changes/add-client-identity-roster/` — ratified
2026-08-14 by Brett Heap, verbatim "a, ratified", answering all five questions
in `clarify-questions.md`. That change's `tasks.md` is the governed handoff
sketch and the authority for SCOPE; this specification neither extends it nor
restates its task list, which Speckit owns and regenerates. `design.md`'s
rejected alternatives and `review/decision-review-2026-08-14.md` are binding
history: nothing here may contradict them.

**Capabilities realized**: `client-identity-roster` (ADDED, thirteen
requirements), `consent-instrument` (MODIFIED — termination cascade reaches
governed identities and their provider-side admission), `doc-health` (MODIFIED
— a sixteenth deterministic family, cross-domain scope only).

**Ratified constraints (binding; encoding them is the work, relitigating them
is failure)**:

1. **Residency is class-independent.** Client-resident single-tenant is the
   default for EVERY authority class; `vendor_tenant_multi` is admissible only
   through the governed model carrying its full obligations.
2. **Blocking scope is all three.** Intra-repo entry conformance BLOCKS the
   owning domain's gate; cross-domain composition REPORTS via doc-health; an
   open drift finding REFUSES grant issuance for that identity.
3. **The enrollment axis stays permissive.** `planned` entries are legal and
   indefinite; per-unit and per-duty identities are permitted, never penalised.
   If cost bites, the lever is the multi-tenant model with obligations — never
   a quiet relaxation of the axis.
4. **Done means contract records AND the consent cascade AND the doc-health
   family**, all landed and green. Contract-only is not a stopping point.
5. **First-release `admission_surface` vocabulary is CLOSED to
   `business_central` and `exchange`.**
6. **Uniqueness is keyed on (domain, admission surface, authority class,
   blast-radius unit, duty); authority classes are `observe|mutate` ONLY.**
   Two flaws a cross-model review killed must not return: a key that forbade a
   per-blast-radius-unit identity, and a `destructive` authority class. If any
   schema, validator, fixture, or example produced here makes a per-unit or
   duty-separated identity a finding, the work has regressed.
7. **`granted_permissions[]` and `admission[]` (a LIST) survive into the
   record.** They are what make the axis falsifiable and what let the Business
   Central worked case describe itself at all.
8. **This feature authorizes no client-tenant act, no credential minting, and
   no live provider call.**

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A domain declares an identity standing in a client's tenant that cannot claim less reach than it achieves (Priority: P1)

A domain factory holding an app registration or service principal inside a
paying client's Microsoft tenant writes one roster fragment per client. Each
entry names the admission surface it stands on, the blast-radius unit and duty
it serves, its intended authority class, the provider-native permissions it was
actually granted, and the achieved class those permissions produce. Every
admission act performed in a provider console appears as its own list member
with the scope that act achieves, whether the resulting bound is enforced by
the provider or only by our gate logic, and evidence that a call actually
succeeded — with the time it was verified. Where the achieved reach exceeds the
intended reach, the entry declares the excess, the provider reason no narrower
permission exists, the gate obligation that bounds it, and the test proving
that gate refuses an out-of-unit target.

**Why this priority**: This is the whole contract, and it is the slice that
stands alone: with only this, a domain can write a truthful identity record and
receive a real refusal when the record understates what the identity can do.
It also carries the measured finding the change exists for — provider consent
is not provider admission, so consent recorded as access is a lie the check
must catch.

**Independent Test**: Author the Business Central worked case as a fragment —
one provider-enforced per-environment application user in Sandbox1 plus the
tenant-wide admin-center Entra-app authorization with no scope selector — and
confirm the canonical validator accepts it with the union reach, the declared
excess, and the resolving gate obligation. Then author each named violation in
turn and confirm the validator refuses it, naming that rule and not another.

**Acceptance Scenarios**:

1. **Given** an entry declaring provider consent and no admission act, **When**
   it is validated, **Then** validation fails stating that consent is not
   admission.
2. **Given** an admission act carrying no evidence of a successful call,
   **When** the entry is validated, **Then** the act is recorded in a distinct
   unverified state and excluded from the identity's effective reach, and the
   effective reach reported is the union of the VERIFIED acts only.
3. **Given** an identity admitted through one act scoped to a blast-radius unit
   and a second act with no scope selector, **When** the entry is validated,
   **Then** both acts appear with their own achieved scopes and enforcement
   modes and the effective reach is their union, not the narrower act.
4. **Given** an entry whose stated purpose or name describes observation while
   its `granted_permissions[]` achieve mutation, **When** it is validated,
   **Then** validation fails naming the permissions that achieve the higher
   class, and passes only once the excess, its provider reason, and its
   bounding mechanism are declared.
5. **Given** an entry declaring a bound as provider-enforced where no principal
   scoped to the governed blast-radius unit exists at that surface, **When** it
   is validated, **Then** validation fails; and **Given** a surface that DOES
   offer such a principal while the entry declares logical enforcement
   instead, **Then** validation fails naming the available principal.
6. **Given** an entry proposing a destructive authority class, **When** it is
   validated, **Then** validation fails — the class enumeration is closed to
   `observe` and `mutate` — and the conformant expression is destructive
   capability declared as the achieved class of the `mutate` entry with its
   gate obligation.
7. **Given** an entry whose registration is homed outside the client tenant
   while declaring a client-resident single-tenant residency model, **When** it
   is validated, **Then** validation fails naming the registration's home
   tenant; and **Given** an entry declaring `vendor_tenant_multi`, **Then** it
   is refused unless it carries the tenant allow-list enforced at token
   validation, per-client authorization state, per-client revocation evidence,
   the cross-client credential-span statement, and the consent amendment per
   affected client.
8. **Given** two entries differing only in blast-radius unit, and two differing
   only in duty, **When** they are validated, **Then** both pairs pass with no
   overlap finding; and **Given** two entries sharing the whole uniqueness
   tuple, **Then** the duplicate is reported naming every element of the tuple.
9. **Given** an entry naming a ratified capability and no consent instrument,
   **When** it is validated, **Then** validation fails stating that consent —
   not our own ratification — authorizes standing in another party's tenant.
10. **Given** an entry in `planned` state, **When** the fragment is validated,
    **Then** it passes and is not reported as missing or incomplete; and
    **Given** an entry whose standing-credential attestation is contradicted by
    a credential held outside an approved grant window, **Then** the attestation
    is reported false against that entry.
11. **Given** an `admission_surface` value outside the closed first-release
    vocabulary, **When** the fragment is validated, **Then** validation fails
    naming the closed vocabulary and the extension route (a surface enters with
    its capability's promotion; a client-org GitHub App installation is the
    named successor routed by `client-infrastructure-liaison`).

---

### User Story 2 - The contract is consumable by a pinned domain repo, and no instance can land where nothing validates it (Priority: P2)

A domain factory consumes the roster contract the way it consumes every other
neutral contract: through its pinned `xfactory.contract_ref`, against a
manifest row carrying a per-file digest, with a packaged example to instantiate
from. The contract declares WHERE a domain's fragments live, so a fragment
cannot land in a directory whose only validator skips unknown kinds as out of
scope and therefore passes unexamined.

**Why this priority**: Without registration and a declared placement the
contract exists but is unreachable and unenforced — the failure mode the
governing change's first draft was rewritten to fix. It is second because the
schema and validator must exist before they can be registered.

**Independent Test**: Place a conformant fragment at the declared location in a
fixture domain repo and confirm exactly one canonical validator claims and
checks it; place the same fragment outside that location and confirm it is
reported as misplaced rather than silently skipped. Verify the manifest row's
digest against the file on disk and confirm the contract-bundle release
inventory validates.

**Acceptance Scenarios**:

1. **Given** a fragment at the declared placement, **When** the domain
   validation chain runs, **Then** the roster validator checks it and reports a
   count of records checked, and no validator reports it as an out-of-scope
   skip that nothing else covers.
2. **Given** a fragment carrying the roster kind outside the declared
   placement, **When** validation runs, **Then** it is reported as misplaced.
3. **Given** the new schema file, **When** manifest digest verification runs,
   **Then** the recorded sha256 matches the file and the bundle release
   inventory for the new bundle version validates.
4. **Given** the packaged example, **When** the canonical validator runs over
   the examples directory, **Then** every packaged example validates clean.

---

### User Story 3 - A nonconformant entry fails the owning domain's gate rather than warning nightly (Priority: P3)

The canonical roster check runs from the pinned openxFactory checkout against a
domain repository as an explicit target, and a nonzero exit fails that domain's
conformance gate. A `mutate` entry whose capability is not ratified blocks; it
does not become an advisory report.

**Why this priority**: It is the ratified blocking half of Decision 7 and the
difference between a governed axis and documentation. It depends on the
validator existing (P1) but on nothing else.

**Independent Test**: Run the check against a fixture domain repo containing a
`mutate` entry with no ratified capability and confirm a nonzero exit with the
finding named; run it against the conformant fixture repo and confirm exit 0
with no findings.

**Acceptance Scenarios**:

1. **Given** a domain repo whose fragment contains any intra-repo
   nonconformance, **When** the check runs from the pinned checkout with that
   repo as its target, **Then** it exits nonzero and the domain gate fails.
2. **Given** a `mutate` entry naming no ratified capability, **When** the check
   runs, **Then** it is an error that fails the gate rather than a report-only
   finding.
3. **Given** a conformant domain repo, **When** the check runs, **Then** it
   exits 0, and a copy of the check inside the domain repo is itself a
   conformance defect (the pack's no-copy rule).

---

### User Story 4 - Withdrawing consent reaches the identity, not only its credentials (Priority: P4)

An instrument that authorizes a governed identity standing in the consenting
party's tenant declares that identity as a first-class dependent reference. On
termination or withdrawal the identity falls due alongside its credential
grants, and the cascade evidence must cover the identity's removal or
retirement AND the withdrawal of its provider-side admission — not merely the
revocation of its credentials.

**Why this priority**: It closes the gap the ratifier refused to defer:
revoking a credential leaves the identity registered and still admitted in the
provider's own console. It is independent — it is expressible and testable
against the consent-instrument family alone.

**Independent Test**: Author a terminated instrument declaring a governed
identity dependent whose cascade evidence covers only credential revocation and
confirm a finding; extend the evidence to identity removal plus admission
withdrawal and confirm it passes. Confirm the existing consent-instrument
fixtures and instances validate unchanged.

**Acceptance Scenarios**:

1. **Given** an instrument authorizing a governed identity, **When** it enters
   `terminated` or `withdrawn`, **Then** the identity's roster entry falls due
   with the other dependent references under the record's revocation SLA.
2. **Given** cascade evidence covering credential revocation only, **When** the
   instrument is validated, **Then** it is a finding naming the missing
   identity-removal and admission-withdrawal evidence.
3. **Given** a governed identity discovered as an undeclared dependent, **When**
   the instrument is validated, **Then** the finding lands against the
   instrument, not against the identity.
4. **Given** every existing conformant instrument in the corpus, **When**
   validation runs after this change, **Then** none of them acquires a new
   finding.

---

### User Story 5 - Cross-domain composition is visible without duplicating the domain gate (Priority: P5)

Two domain factories hold identities in the same client tenant. A nightly
deterministic pass assembles their published fragments per client and reports
only the genuinely cross-domain concerns: identity material shared between
domains, and reach into a surface a domain did not declare. Two domains each
holding their own separate identity on one surface and class is explicitly NOT
a finding — separate identities are what preserve provider-side attribution and
independent revocation.

**Why this priority**: It is the reporting half of the ratified split and the
sixteenth doc-health family the change MODIFIES into existence. It is last of
the checking work because it composes artifacts the earlier stories produce.

**Independent Test**: Give the pass two fragments for one client naming the same
identity and confirm a shared-identity-material finding naming both domains;
give it two fragments with separate identities on the same surface and class
and confirm no finding; give it a corpus with fewer than two fragments for any
client and confirm an explicit skip with a reason.

**Acceptance Scenarios**:

1. **Given** two pinned domain repositories publishing fragments for one
   client, **When** the deterministic pass runs, **Then** the family assembles
   them and reports shared identity material or undeclared cross-domain reach.
2. **Given** the same corpus, **When** the family reports, **Then** no
   intra-repo entry rule appears among its findings — those fail the owning
   domain's gate instead.
3. **Given** a corpus with no client having two or more fragments, **When** the
   family runs, **Then** it emits an explicit skip with a reason rather than
   silence or a false pass.
4. **Given** identical inputs run twice, **When** the family runs, **Then** the
   findings are identical and no model call or network access occurs.
5. **Given** a finding that contradicts a ratified capability, **When** it is
   classified, **Then** it carries the contested resolution class rather than
   auto-fixable.

---

### User Story 6 - A drifted identity stops receiving fresh credentials (Priority: P6)

Where an identity's observed permissions or admission diverge from its roster
entry, the finding is recorded and nothing in the client's tenant is touched.
Instead, grant issuance for that identity is refused as an issuance
precondition — the one lever we own that is not a mutation of the client's
estate.

**Why this priority**: It is the third ratified blocking behaviour and the
answer to "report-only means a drifted identity keeps getting fresh JIT
credentials". It rides an existing mechanism, so it is small, but it depends on
the roster entry and the drift-finding representation.

**Independent Test**: Record an open drift finding against a fixture identity,
request issuance of a grant naming it, and confirm refusal that names the
finding; clear the finding and confirm issuance proceeds. Confirm no code path
in the feature can create, modify, widen, narrow, or remove an identity,
permission, or admission.

**Acceptance Scenarios**:

1. **Given** a detected divergence between roster and observed state, **When**
   it is recorded, **Then** it records the roster value and the observed value
   and performs no mutation and no automated remediation.
2. **Given** an open drift finding against an identity, **When** grant issuance
   is attempted for that identity, **Then** issuance is refused naming the
   finding.
3. **Given** the refusal, **When** it is expressed, **Then** it uses the
   existing `issuance_preconditions` mechanism rather than a second parallel
   mechanism.

---

### Edge Cases

- **A fragment placed where only a skip-with-notice validator looks.** The
  governed hazard: `validate-credential-contracts.py` skips unknown kinds as
  out of scope, so a misplaced roster instance would pass unexamined. Declared
  placement plus a misplacement finding is the answer; a placement change is a
  contract change.
- **An admission act verified once, long ago.** The record carries
  `verified_at`; whether an old verification decays is an open question (see
  FR-033). Until it is settled the only distinction the check draws is
  verified vs unverified.
- **An identity on a surface outside the first-release vocabulary.** An
  existing `microsoft_endpoint_*` or managed-node-inventory class, a Windows
  365 or Entra-directory identity, or a client-org GitHub App installation is
  OUT of roster scope in this release. It is neither rosterable nor a
  completeness finding; it enters with its capability's promotion, or through
  the named successor for non-Entra providers.
- **A live client-tenant identity with no roster entry at all.** Whether
  omission is itself a finding, and against what expected set, is the open
  completeness question (FR-032). A permissive axis with `planned` entries
  means silence and legitimate not-yet-enrolled look alike until it is settled.
- **A retired entry.** Its record is retained rather than deleted, which must
  not collide with record-immutability expectations elsewhere in the corpus.
- **A single-domain client.** The cross-domain family has nothing to compose
  and must skip with a reason; the intra-repo gate still applies fully.
- **A provider whose narrowest permission spans surfaces.** Conformant when the
  spanned surfaces, the provider reason, and the gate obligation are declared;
  the check must not invalidate a deliberately narrow identity because the
  provider's granularity is coarser than the axis.
- **A gate obligation naming a gate that was renamed or removed.** The
  obligation no longer resolves and is a finding: an unenforced obligation
  converts an undetected widening into a documented one.
- **A domain that holds no client-tenant identities.** Publishes no fragment
  and is refused by nothing.

## Requirements *(mandatory)*

### Functional Requirements

**The neutral record**

- **FR-001**: The feature MUST define a canonical schema
  `contracts/schemas/xfactory-client-identity-roster.schema.yaml` carrying
  `schema_version` and `kind`, describing a per-client, per-domain roster
  fragment with `client_ref`, `domain`, and `entries[]`, where each entry
  carries `identity_ref`, `identity_kind`, `home_tenant`,
  `principal_locations[]`, `residency_model`, `admission_surface`, `duty`,
  `blast_radius_unit`, `authority_class_intended`, `authority_class_achieved`,
  `granted_permissions[]`, `admission[]`, `declared_excess`,
  `per_unit_principal_available`, `lifecycle_state`,
  `standing_credential_attestation`, `ratified_by` (domain-qualified), and
  `consent_ref`.
- **FR-002**: `admission` MUST be a LIST whose members each declare the
  surface, the act performed in that surface's own administrative console, the
  scope that act achieves, whether the resulting bound is provider-enforced or
  logic-enforced, an evidence reference for a successful call, and the time it
  was verified. A record MUST NOT express admission as a single act.
- **FR-003**: Provider consent alone MUST NOT be recordable as access; an
  admission act without verification evidence MUST be represented in a distinct
  unverified state and MUST be excluded from the identity's effective reach;
  effective reach MUST be the union of verified acts.
- **FR-004**: `granted_permissions[]` in provider-native identifiers MUST be
  required on every entry, and `authority_class_achieved` MUST be checkable
  against it — the record MUST NOT be able to assert an achieved class its
  permissions contradict.
- **FR-005**: The authority-class enumeration MUST be CLOSED to `observe` and
  `mutate`. A destructive class MUST be unrepresentable. A destructive-capable
  identity is admissible only where the provider demonstrably offers a
  delete-scoped permission distinct from write, declared with that
  demonstration; otherwise destructive capability rides the `mutate` entry's
  declared achieved class and gate obligation.
- **FR-006**: Uniqueness MUST be keyed on the tuple (owning domain, admission
  surface, authority class, blast-radius unit, duty). Entries sharing the whole
  tuple MUST be a finding naming every element; entries differing in ANY
  element MUST validate clean. The checks MUST NOT report a per-blast-radius-
  unit identity or a duty-separated identity as an overlap, a duplicate, or any
  other finding.
- **FR-007**: `admission_surface` MUST be a CLOSED vocabulary containing
  exactly `business_central` and `exchange` in this release, each entry naming
  the admission act and the scoping mechanism that make it a surface. Any other
  value MUST be refused, naming the extension route: a surface enters with the
  promotion of the capability that governs it, and non-Entra providers are a
  named successor routed by `client-infrastructure-liaison`.
- **FR-008**: Each entry MUST declare, per admission surface, whether a
  principal scoped to the governed blast-radius unit is available. A bound MAY
  be recorded as logic-enforced only where no such principal exists, with the
  provider reason recorded. A bound recorded as provider-enforced where no such
  principal exists MUST be a finding, and an available per-unit principal left
  unused while logical enforcement is declared MUST be a finding naming the
  available principal.
- **FR-009**: Provider-forced breadth — spanned admission surfaces or an
  achieved class above the intended one — MUST be declarable with the provider
  reason and a gate obligation, and MUST be conformant when so declared.
  Undeclared reach MUST be a finding naming the surface and the permission that
  reaches it. The checks MUST NOT invalidate a deliberately narrow identity
  merely because the provider's permission granularity is coarser than the
  axis.
- **FR-010**: Where achieved authority exceeds intended authority, the entry
  MUST declare the excess with the reason no narrower permission exists, the
  bounding mechanism, the gate obligation, and the enforcement-test reference;
  and an entry's name or stated purpose MUST NOT describe a narrower authority
  than it achieves.
- **FR-011**: Every gate obligation MUST resolve to an existing gate in the
  owning domain's governed workflow records and MUST name a test proving
  refusal of a target outside the governed blast-radius unit. An unresolvable
  obligation and a missing enforcement test MUST each be findings.
- **FR-012**: Each entry MUST declare `identity_kind`, `home_tenant`,
  `principal_locations[]`, and a `residency_model`. Client-resident
  single-tenant MUST be the default for EVERY authority class, with no
  class-dependent relaxation anywhere in schema, validator, examples, or
  documentation. A `vendor_tenant_multi` model MUST additionally require a
  tenant allow-list enforced at token validation, per-client authorization
  state, per-client revocation evidence, a statement that one credential set
  spans every consenting client, and a consent amendment per affected client. A
  registration homed outside the client tenant MUST NOT be declarable as
  client-resident on the grounds that its principal appears in the client
  tenant.
- **FR-013**: Each entry MUST carry `lifecycle_state` of `planned`, `enrolled`,
  or `retired` and a standing-credential attestation. A `planned` entry MUST
  validate and MUST NOT be reported as missing or incomplete; a retired entry
  MUST retain its record; a credential held outside an approved grant window
  MUST make the attestation false and be reported against that entry.
- **FR-014**: Each entry MUST name both the domain-qualified ratified
  capability that justifies the identity and the consent instrument that
  authorizes its standing in the client's tenant, with the instrument citation
  resolving to an instrument in force. An entry citing a capability and no
  instrument MUST be invalid. A `mutate` entry naming no ratified capability
  MUST fail the owning domain's gate rather than emit a report-only finding.

**The canonical validator and its corpus**

- **FR-015**: A single canonical validator
  `scripts/validate-client-identity-roster.py` MUST enforce every intra-repo
  rule above. It MUST be deterministic and network-free, MUST take its target
  domain repository as an explicit argument, MUST follow the repository's
  existing `scripts/validate-*.py` shape and exit-code convention (0 clean, 1
  findings, 2 harness error), MUST run from the pinned openxFactory checkout,
  and MUST NOT be copied into domain repositories.
- **FR-016**: The fixture corpus MUST carry one positive roster and one
  NEGATIVE CONFIRMATION per rule — at minimum: cross-domain shared identity,
  undeclared reach, an unverified admission act counted as access, achieved
  authority exceeding intended without a declared excess, an unresolvable gate
  obligation, a missing enforcement test, a provider-enforced claim with no
  per-unit principal, a vendor-homed registration declared client-resident, a
  `mutate` entry with no ratified capability, a false standing-credential
  attestation, a proposed destructive class, an out-of-vocabulary admission
  surface, an entry with no consent instrument, and a genuine full-tuple
  duplicate. Each negative MUST fail for its own reason rather than
  incidentally.
- **FR-017**: The corpus MUST carry POSITIVE regression fixtures that keep the
  two killed flaws killed: two entries differing only in blast-radius unit, two
  entries differing only in duty, a provider-forced multi-surface reader with
  its declaration, and a `planned` entry — each validating clean with zero
  findings.
- **FR-018**: The validator MUST refuse a negative fixture that validates
  cleanly, a negative fixture that fails for the wrong reason, and a corpus
  where a registered probe has no file or a file has no registration.
- **FR-019**: The feature MUST package an instantiable example covering the
  Business Central two-admission-act worked case — a provider-enforced
  per-environment application user in Sandbox1 with no production application
  user, PLUS the admin-center Entra-app authorization that has no scope
  selector and therefore reaches every environment, with the resulting excess,
  gate obligation, and enforcement test declared — together with a
  provider-forced multi-surface reader, a duty-separated pair, and one
  `planned` entry, for a client held by two domains.
- **FR-020**: The contract MUST declare WHERE a domain publishes its roster
  fragments, and an instance carrying the roster kind outside that declared
  placement MUST be reported rather than silently skipped as out of scope by
  the credential-contracts validator. [NEEDS CLARIFICATION: the governed packet
  requires "a declared placement" but names no path — is it
  `credentials/client-identity-roster/<client_ref>.yaml` inside the tree
  `validate-credential-contracts.py` already scans, or the domain `tenants/`
  tree where client-tenant evidence lives today?]

**Release registration**

- **FR-021**: The new schema MUST be registered in `contracts/manifest.yaml`
  with `path`, `source_path`, `type`, `schema_version`, `sha256`,
  `compatibility`, `adapter_owner`, and a `consumption_rule`, MUST carry a
  `contracts/CHANGELOG.md` entry, and MUST bump the contract bundle from its
  current `contract-v1.31` to `contract-v1.32` with the matching release digest
  inventory, such that digest verification passes.

**The three wirings**

- **FR-022**: Intra-repo entry conformance MUST be BLOCKING: the canonical
  check MUST be registered so that a nonzero exit fails the owning domain's
  conformance gate. [NEEDS CLARIFICATION: the promoted
  `domain-conformance-checks` spec enumerates the pack as exactly three
  `check-*.py` scripts, so adding a fourth blocking check appears to modify
  that capability, which the governing change does not declare as MODIFIED — is
  the roster check registered as a canonical validator invoked by the domain
  gate (the `validate-*.py` shape the packet specifies), or does the pack
  enumeration grow, requiring a `domain-conformance-checks` delta before
  archive?]
- **FR-023**: Cross-domain composition MUST land as a sixteenth deterministic
  doc-health family, registered in the doc-health family registry with a
  resolution class, that assembles per-client fragments published by pinned
  domain repositories and reports ONLY shared identity material and undeclared
  cross-domain reach. It MUST NOT duplicate any intra-repo rule, MUST skip
  explicitly with a reason when there is nothing to compose, MUST make no model
  call or network request, and MUST classify a finding that contradicts a
  ratified capability as contested rather than auto-fixable.
- **FR-024**: Two domains each holding their own separate identity on one
  admission surface and authority class in one client tenant MUST NOT be a
  finding at any level.
- **FR-025**: The implementation's family set and every count-bearing statement
  in the corpus MUST agree with the promoted `doc-health` wording, so
  doc-health does not self-gate against the change. [NEEDS CLARIFICATION: the
  promoted `openspec/specs/doc-health/spec.md` still says "fifteen check
  families" and is normally rewritten by the OpenSpec archive step, which
  happens AFTER this feature lands — does this feature edit the promoted spec
  text and the docs that state the count, or must the window be tolerated?]
- **FR-026**: The `consent-instrument` family MUST admit a governed identity
  standing in the consenting party's tenant as a first-class dependent-artifact
  reference kind — a named member of the closed dependent-kind enumeration, not
  the `other` escape — and its cascade evidence obligation MUST cover the
  identity's removal or retirement AND the withdrawal of its provider-side
  admission, not merely credential revocation. The canonical consent validator
  MUST learn the new kind and its evidence obligation.
- **FR-027**: Drift handling MUST NOT create, modify, widen, narrow, or remove
  any identity, permission, or admission, and MUST NOT trigger automated
  remediation; a drift finding MUST record the roster value and the observed
  value only.
- **FR-028**: An open drift finding against an identity MUST refuse grant
  issuance for that identity as an issuance precondition naming the finding,
  expressed through the existing `issuance_preconditions` mechanism rather than
  a second parallel mechanism. [NEEDS CLARIFICATION: the mechanism instance
  lives in a domain repo's `credentials/requirements.yaml`
  (`deployment_operator` / `aks_workload_administration`), while this feature is
  openxFactory-only — is the neutral deliverable the precondition vocabulary
  plus a fixture proving refusal, with the domain application a follow-up, or
  something more?]

**Boundaries this feature must not cross**

- **FR-029**: No client-tenant act, credential minting, live provider call, or
  network access MUST be performed or enabled by any artifact, check, or test
  in this feature; enrollment automation and drift remediation MUST NOT be
  built.
- **FR-030**: No credential record shape, grant neutrality rule, or JIT
  discipline MUST change; both MODIFIED capabilities' existing suites and
  fixtures MUST remain green and unmodified in behaviour; no domain repository
  file MUST be edited by this feature — the OpsxFactory and LedgerxFactory
  fragments, and live client-tenant drift detection, are named follow-ups, not
  deliverables here.
- **FR-031**: Surfaces outside the first-release vocabulary MUST NOT be added,
  and identities on them MUST NOT be treated as missing roster entries.

**Open scope questions carried to the architect**

- **FR-032**: Roster completeness. [NEEDS CLARIFICATION: is a live
  client-tenant identity with no roster entry itself a finding, and if so does
  the canonical check derive the expected entry set from the domain's credential
  requirement classes that declare a provider identity on a first-release
  surface? Without a completeness rule, omitting an identity entirely passes,
  while the `planned` scenario in the governed delta ("is not reported as
  missing") implies some missing-entry check exists.]
- **FR-033**: Admission-evidence freshness. [NEEDS CLARIFICATION: does
  `verified_at` decay — a maximum age or re-verification interval after which an
  act is stale — and if so is staleness a finding, a report, or an
  issuance-precondition failure? The governed packet requires the timestamp but
  sets no interval.]
- **FR-034**: Vocabulary closedness for the remaining enumerated fields.
  [NEEDS CLARIFICATION: which of `identity_kind`, `residency_model`,
  `blast_radius_unit`, `duty`, and `enforcement_mode` are CLOSED neutral
  enumerations and which are domain-declared free tokens? `admission_surface`
  and authority class are ratified closed; the others are unstated, and
  closedness determines whether a domain can invent values that make the
  uniqueness key unfalsifiable.]
- **FR-035**: Drift-finding representation. [NEEDS CLARIFICATION: does this
  feature ship the record shape of a drift finding (so the refusal in FR-028
  has something to read), or is the shape a domain concern with only the
  refusal rule expressed neutrally?]

### Key Entities

- **Roster fragment**: one client (`client_ref`) as seen by one owning domain,
  carrying that domain's entries. The unit a domain publishes and a cross-domain
  pass assembles.
- **Roster entry**: one governed identity, identified by the uniqueness tuple
  (domain, admission surface, authority class, blast-radius unit, duty), with
  its granted permissions, admission list, residency declaration, lifecycle
  state, attestation, and its two roots (ratified capability and consent
  instrument).
- **Admission surface**: a provider-side administrative surface owning an
  independent admission act and its own scoping mechanism — a member of a
  closed vocabulary, defined by the act rather than by a product name, and
  named together with that act and mechanism.
- **Admission act**: one entry in the admission list — surface, act, achieved
  scope, enforcement mode, evidence of a successful call, and verification
  time. Verified acts union into effective reach; unverified acts are a
  distinct state that contributes nothing.
- **Declared excess**: the record of provider-forced breadth or achieved-class
  overshoot — provider reason, bounding mechanism, gate obligation, enforcement
  test — which converts an undeclared widening into a declared, tested one.
- **Gate obligation**: a reference to an existing gate in the owning domain's
  workflow records plus the test proving that gate refuses an out-of-unit
  target.
- **Residency declaration**: identity kind, registration home tenant, principal
  locations, and the residency model with its per-model obligations.
- **Drift finding**: a recorded divergence between roster value and observed
  value, which mutates nothing and refuses grant issuance for its identity.
- **Governed-identity dependent reference**: the consent instrument's
  first-class reference to an identity standing in the consenting party's
  tenant, whose cascade evidence covers identity removal or retirement and
  withdrawal of provider-side admission.
- **Assembled cross-domain roster**: the per-client composition of every
  domain's fragment, whose only findings are shared identity material and
  undeclared cross-domain reach.
- **Fixture corpus**: the positive roster, the per-rule negative confirmations,
  and the killed-flaw regression positives, each registered so a probe cannot
  exist without a file or a file without a probe.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every named violation in FR-016 is refused by the canonical
  validator, each naming its own rule — zero pass silently, and no negative
  fixture passes for a coincidental reason.
- **SC-002**: The killed-flaw regression positives (FR-017) validate with ZERO
  findings: a per-unit pair, a duty-separated pair, a declared provider-forced
  multi-surface reader, and a `planned` entry. Any finding against these is a
  regression of the two flaws the cross-model review killed.
- **SC-003**: The Business Central worked case is fully expressible in the
  neutral contract with no domain-local vocabulary: two admission acts with
  different achieved scopes and enforcement modes, a union effective reach, and
  a declared excess whose gate obligation resolves and whose enforcement test is
  named.
- **SC-004**: A reader of any conformant entry can determine, without leaving
  the record and the surface vocabulary, what the identity actually reaches,
  who enforces each bound, when each admission was last verified, which consent
  authorizes it, and whether it holds any standing credential.
- **SC-005**: A fragment at the declared placement is claimed and checked by
  exactly one canonical validator, and a fragment outside it is reported —
  measured by a misplacement fixture, with no path by which a roster instance
  is skipped as out of scope and covered by nothing.
- **SC-006**: The blocking/reporting split holds in measurement: an intra-repo
  nonconformance yields a nonzero exit from the domain gate, while a
  cross-domain shared-identity case yields a doc-health finding and leaves the
  domain gate exit unchanged.
- **SC-007**: A terminated instrument whose governed-identity dependent shows
  credential-only cascade evidence is a finding; the same instrument with
  identity-removal and admission-withdrawal evidence passes; and every existing
  instrument and fixture in the corpus validates unchanged.
- **SC-008**: An open drift finding refuses grant issuance for that identity
  naming the finding, and the refusal path performs no client-tenant mutation.
- **SC-009**: doc-health runs sixteen families with the implementation and the
  promoted count in agreement, the new family reporting or skipping with an
  explicit reason, producing identical findings on repeated identical runs, and
  containing no intra-repo rule.
- **SC-010**: The green bar: repository validators pass,
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes, contract
  digests verify at `contract-v1.32`, both MODIFIED capabilities' existing test
  suites pass, and doc-health reports no new finding against the change or its
  documents.
- **SC-011**: Every new check and test runs with no outbound network access and
  no model call, and produces byte-identical findings across runs.
- **SC-012**: No file in any domain repository is modified by this feature, and
  no credential is minted and no provider call is made at any point in its
  execution or tests.

## Assumptions

- **The record kind is `xfactory_client_identity_roster`** and the fragment
  granularity is one file per (client, domain) pair, following `client_ref` +
  `domain` at the top of the record; the cross-domain family assembles N such
  fragments rather than reading a single multi-domain file.
- **Packaged examples follow the repository's per-family directory
  convention** (`examples/<family>/*.example.yaml`, the shape the sibling
  canonical validators glob), even though the governed sketch names a single
  file path.
- **The validator follows the sibling `validate-*.py` contract** for arguments,
  output, and exit codes (0 clean, 1 findings, 2 harness error), and is
  invoked against a target repository from the pinned checkout — the same
  consumption shape as the existing canonical validators and the conformance
  pack.
- **The current bundle is `contract-v1.31`**, verified in
  `contracts/manifest.yaml`, so this feature registers at `contract-v1.32`.
- **`granted_permissions[]` is provider-native and opaque to the neutral
  contract**: the schema constrains shape, while the mapping from a permission
  identifier to an achieved authority class is declared in the record and
  checked for internal consistency, not resolved against any provider catalogue
  (which would require network access this feature forbids).
- **Promoted-spec text is rewritten by the OpenSpec archive step, not by this
  feature**, unless FR-025's clarification says otherwise; the feature's
  obligation is that the implementation matches the ratified delta wording.
- **Scope excludes the domain fragments.** OpsxFactory's fragment (with its
  three surfaced findings: the `opsx-farheap-bc-observer` name/purpose
  mismatch, the inert Microsoft Graph delegated scope absent from its identity
  record, and the tenant-wide admin-center excess), LedgerxFactory's
  `ledgerx-farheap-bc-*` fragment, and live client-tenant drift detection are
  named follow-ups executed in the domain repositories.
- **The LedgerxFactory residency conflict is not this feature's to resolve.**
  The ratified class-independent residency default makes that domain's
  multi-tenant Reader/Poster pair non-conformant as designed; whether it
  declares `vendor_tenant_multi` with full obligations (including a consent
  amendment per affected client) or moves client-resident is Brett's decision,
  because it touches live client consent instruments.
- **The Business Central evidence chain motivating the contract lives on an
  OpsxFactory branch** (`evidence/bc-general-verify-probe-20260810`, PR #19),
  not on that repo's main, so the worked case is authored from the packet's
  description of it rather than by reading those records from a pinned main.
