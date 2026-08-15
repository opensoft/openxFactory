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
history: nothing here may contradict them. The packet was AMENDED 2026-08-14
(Decisions A and B, `review/amendment-record-2026-08-14.md`), adding two
MODIFIED capability deltas the ratified proposal had not declared. ARCHIVE
BLOCKERS are therefore the contract records, the consent-instrument cascade
(OpenSpec task 3.2), the doc-health sixteenth family (OpenSpec task 3.4), pack
enrollment (OpenSpec task 3.1, Decision A), and the neutral refusal fixture
(OpenSpec task 3.3, Decision B); only section 4 — the domain fragments — is
exempt. Every "OpenSpec task N" citation in this specification is a task number
in the GOVERNING CHANGE's `tasks.md` (the governed sketch, and the numbering
ruling C2 uses); it has no relation to this feature's Speckit task ids, where
3.1–3.6 are the packaged-example tasks.

**Capabilities realized**: `client-identity-roster` (ADDED, thirteen
requirements), `consent-instrument` (MODIFIED — termination cascade reaches
governed identities and their provider-side admission), `doc-health` (MODIFIED
— a sixteenth deterministic family, cross-domain scope only),
`domain-conformance-checks` (MODIFIED, Decision A — the neutral pack grows to
four checks so intra-repo conformance is blocking), `credential-contracts`
(MODIFIED, Decision B — the neutral schema gains an `issuance_preconditions`
vocabulary carrying the roster-drift member).

**Governing rulings**: `clarify-rulings-2026-08-14.md` (this directory) — the
architect's clarify round 1 rulings after cross-model adversarial review, plus
Brett's two escalated decisions. Where that file and this specification
disagree, the rulings win; every `[NEEDS CLARIFICATION]` marker this
specification carried is ruled and removed. The packet's amendment record is
`openspec/changes/add-client-identity-roster/review/amendment-record-2026-08-14.md`.

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
9. **Two ratified amendments, Brett 2026-08-14.** DECISION A: the
   `domain-conformance-checks` pack grows to FOUR checks and the roster check
   joins it, because pack membership is the only promoted mechanism conferring
   blocking status — pack enrollment is an archive blocker, not a successor.
   DECISION B: the refusal gets a neutral home — `credential-contracts` gains a
   closed `issuance_preconditions` vocabulary with a roster-drift member,
   proven at the neutral level by fixture. Reducing either to a successor was
   offered and declined.
10. **No roster completeness rule ships in this release.** Absence of a
    fragment, or of an entry, is NEVER a finding (the permissive axis,
    ratified answer 3). Scoped completeness is a named successor change, not
    work here.

## Clarifications

### Session 2026-08-14 (architect seat; cross-model adversarial review applied)

Full text and rationale: `clarify-rulings-2026-08-14.md`. Rulings marked
(amended) or (superseded) reflect the review's verdicts on the architect's
first pass; two were escalated to Brett as ratified-scope decisions.

- Q: Where do domain roster fragments live, and what stops a stray instance
  from passing unexamined? → A (R1): declared placement is
  `credentials/client-identity-roster/<client_ref>.yaml` in the domain repo —
  inside the tree `validate-credential-contracts.py` already scans recursively,
  whose skip-with-notice for unknown kinds is expected and blessed by the
  promoted credential-contracts spec. Placement is MECHANIZED: the canonical
  roster validator sweeps the WHOLE target repo for the roster kind and reports
  any instance outside the declared placement as a misplacement finding.
- Q: Does the roster check join the `domain-conformance-checks` pack, when the
  promoted pack spec enumerates three scripts exhaustively? → A (R2 →
  DECISION A, Brett): yes — AMEND the ratified change, declare the capability
  MODIFIED, pack grows to four, blocking stays an archive blocker.
- Q: doc-health says fifteen families promoted and sixteen in the delta — does
  this feature edit promoted text? → A (R3): no. Agreement is measured against
  the RATIFIED DELTA wording; the promoted spec text is rewritten by the
  OpenSpec archive step, which runs after this feature lands. The feature
  updates only the prose sites it owns, at minimum
  `scripts/doc_health/families.py:1` ("The fifteen contract check families.")
  and that module's registration note.
- Q: Where does the grant-issuance refusal live, given the feature is
  openxFactory-only? → A (R4 → DECISION B, Brett): the neutral schema gains the
  `issuance_preconditions` vocabulary with the roster-drift member. No live
  producer of drift findings exists at archive time, so the neutral criterion
  is a conformant requirement-record FIXTURE; live refuse-then-allow is proven
  in the domain follow-up at the mint surface.
- Q: Is a live client-tenant identity with no roster entry a finding? → A (R5,
  superseded — the invented predicate fired permanently on 14 of OpsxFactory's
  16 requirement classes and re-admitted a killed flaw): NO completeness
  enforcement in this release. Absence is never a finding; scoped completeness
  becomes a named successor.
- Q: Does `verified_at` decay? → A (R6): no admission-freshness decay in v1.
  The timestamp is recorded; verified versus unverified is the only distinction
  the checks draw.
- Q: Which enumerated fields are closed, and what stops a free token from
  making the uniqueness key unfalsifiable? → A (R7): `admission_surface`,
  `residency_model`, `enforcement_mode`, authority class, `lifecycle_state` and
  `identity_kind` are CLOSED; `blast_radius_unit` and `duty` are
  domain-declared pattern-bound tokens, each declared once in a fragment legend
  binding the token to its provider-native identifier. The ALIAS RULE bounds
  the free tokens without re-killing per-unit and duty-separated identities.
- Q: Does this feature ship the drift-finding record shape? → A (R8,
  superseded): yes — a governed record in the roster contract family with its
  own `kind` and `schema_version`, carrying `roster_value` and
  `observed_value`. It does NOT claim alignment with any doc-health findings
  register, because none exists (doc-health is a stateless recompute).
- Q: Where do packaged examples live? → A (C3): `examples/client-identity-roster/`
  with a `negative/` subdirectory and a README, spanning at least two fragment
  files because fragments are per (client, domain) and the mandated case is a
  two-domain client.
- Q: Does the consent-instrument status enum need `withdrawn`? → A (N1/N2):
  yes — the delta requires behaviour on "terminated or withdrawn", and the
  enum is closed. Grow it additively with a `contract_schema_version` bump and
  manifest rows at `contract-v1.32`; no aliasing, because withdrawal and
  termination are distinct events.
- Q: What is the new doc-health family called? → A (N4): the ratified delta
  names no family id, so the id is `client-identity-composition` (module
  `client_identity_composition.py`) — it MUST NOT collide with
  `scripts/doc_health/shared_identity.py`, an active separate lane. "Shared
  identity material" is a finding CLASS inside the family, not its name.
- Q: Does the canonical validator resolve `evidence_ref`? → A (N7): no. It is a
  declared pointer (repo + path, optionally sha); the canonical validator is
  network-free and single-repo. Resolution belongs to the cross-domain
  doc-health family, which assembles from pinned repos.

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
8. **Given** two entries differing only in blast-radius unit (with different
   achieved scopes), and two differing only in duty (with different permissions
   or a declared duty-separation rationale), **When** they are validated,
   **Then** both pairs pass with no overlap finding; **Given** two entries
   sharing the whole uniqueness tuple, **Then** the duplicate is reported naming
   every element of the tuple; and **Given** two entries differing solely in a
   free token while observationally identical and declaring no rationale,
   **Then** the alias is reported — the only case in which a free-token
   difference is a finding.
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

**Independent Test**: Place a conformant fragment at
`credentials/client-identity-roster/<client_ref>.yaml` in a fixture domain repo
and confirm exactly one canonical validator claims and checks it — while
`validate-credential-contracts.py`, which scans that tree recursively, emits
its blessed skip-with-notice for the unknown kind. Place the same fragment
anywhere else in the repo and confirm the whole-repo kind sweep reports it as
misplaced rather than leaving it unexamined. Verify the manifest row's digest
against the file on disk and confirm the contract-bundle release inventory
validates.

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

The canonical roster check joins the `domain-conformance-checks` pack as its
fourth member (Decision A), runs from the pinned openxFactory checkout against a
domain repository as an explicit target, and a nonzero exit fails that domain's
conformance gate. A `mutate` entry whose capability is not ratified blocks; it
does not become an advisory report. In a repo publishing no roster fragment the
check passes with an explicit notice — the added blocking surface cannot fire on
absence.

**Why this priority**: It is the ratified blocking half of Decision 7 and the
difference between a governed axis and documentation. Pack membership is the
only promoted mechanism that confers blocking status, which is why Decision A
amended the ratified change rather than deferring enrollment. It depends on the
validator existing (P1) but on nothing else.

**Independent Test**: Run the check against a fixture domain repo containing a
`mutate` entry with no ratified capability and confirm a nonzero exit with the
finding named; run it against the conformant fixture repo and confirm exit 0
with no findings; run it against a fixture repo with no fragment at all and
confirm exit 0 with an explicit notice, no finding.

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
4. **Given** a domain repo publishing no roster fragment, **When** the pack
   runs, **Then** the roster check passes with an explicit notice and exits 0 —
   neither a missing fragment nor a missing entry is a finding in this release.

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
withdrawal and confirm it passes. Repeat with the instrument in `withdrawn` —
the status member this feature adds — and confirm the cascade fires
identically, since withdrawal and termination are distinct events with the same
obligation. Confirm the existing consent-instrument fixtures and instances
validate unchanged, which the additive growth guarantees.

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
sixteenth doc-health family the change MODIFIES into existence — family id
`client-identity-composition`, which must not collide with the active
`shared_identity` lane. It is last of the checking work because it composes
artifacts the earlier stories produce.

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
entry, the divergence is recorded as a governed drift-finding record — carrying
the roster value and the observed value — and nothing in the client's tenant is
touched. Instead, grant issuance for that identity is refused as an issuance
precondition: the one lever we own that is not a mutation of the client's
estate. Decision B gives that precondition a neutral home in
`credential-contracts`, so the refusal is declarable against a pinned contract
rather than as a domain-local extra key.

**Why this priority**: It is the third ratified blocking behaviour and the
answer to "report-only means a drifted identity keeps getting fresh JIT
credentials". It depends on the roster entry and on the drift-finding record
shape, which this feature ships.

**Independent Test**: Validate a conformant credential requirement-record
fixture declaring the roster-drift precondition, and a negative fixture
declaring a precondition outside the closed vocabulary; confirm the drift
record's own schema accepts a complete finding and refuses one missing
`roster_value` or `observed_value`. No live refuse-then-allow can be measured
here — no producer of live drift findings exists in the family at archive time,
and issuance happens at a domain mint surface this feature does not touch.
Confirm no code path in the feature can create, modify, widen, narrow, or
remove an identity, permission, or admission.

**Acceptance Scenarios**:

1. **Given** a detected divergence between roster and observed state, **When**
   it is recorded, **Then** the governed drift-finding record carries
   `roster_value` and `observed_value` alongside the identity reference, and
   the recording performs no mutation and no automated remediation.
2. **Given** an open drift finding against an identity, **When** grant issuance
   is attempted for that identity, **Then** issuance is refused naming the
   finding — the behaviour the neutral declaration specifies and the domain
   mint surface performs.
3. **Given** the refusal, **When** it is expressed neutrally, **Then** it is the
   roster-drift member of the closed `issuance_preconditions` vocabulary in
   `credential-contracts` — one mechanism, declared on the credential
   requirement record, never a second parallel one.
4. **Given** a requirement record declaring a precondition token outside that
   closed vocabulary, **When** it is validated, **Then** it is refused naming
   the vocabulary, because a free-text precondition is unenforceable.

---

### Edge Cases

- **A fragment placed where only a skip-with-notice validator looks.** The
  governed hazard: `validate-credential-contracts.py` scans `credentials/`
  recursively and skips unknown kinds as out of scope, so a misplaced roster
  instance would pass unexamined. The answer is a declared placement
  (`credentials/client-identity-roster/<client_ref>.yaml`) plus a WHOLE-REPO
  kind sweep that reports any instance outside it. The skip-with-notice from
  the credential-contracts validator over the declared placement is EXPECTED
  and blessed by that promoted spec — it is not a gap, because the roster
  validator covers exactly that path. A placement change is a contract change.
- **An admission act verified once, long ago.** The record carries
  `verified_at` and this release adds no decay: verified versus unverified is
  the only distinction the checks draw (ruling R6). An interval, and whether
  staleness would report or refuse issuance, is deliberately not invented here.
- **An identity on a surface outside the first-release vocabulary.** An
  existing `microsoft_endpoint_*` or managed-node-inventory class, a Windows
  365 or Entra-directory identity, or a client-org GitHub App installation is
  OUT of roster scope in this release. It is neither rosterable nor a
  completeness finding; it enters with its capability's promotion, or through
  the named successor for non-Entra providers. This case is retained precisely
  because a completeness rule would have fired on it — demanding an entry for a
  class whose ratified position is that the factory holds NO identity would
  re-admit the killed destructive-class flaw.
- **A live client-tenant identity with no roster entry at all.** Not a finding
  in this release (ruling R5). The permissive axis makes silence and
  legitimate not-yet-enrolled indistinguishable by construction, and any
  predicate derived from the domain's credential requirement classes fires
  permanently on the classes the ratified answers place outside roster scope.
  Scoped completeness — factory-held identity classes, on first-release
  surfaces, in client tenants, with issued grants — is recorded as a named
  successor change.
- **A retired entry.** Its record is retained rather than deleted, which must
  not collide with record-immutability expectations elsewhere in the corpus.
- **A single-domain client.** The cross-domain family has nothing to compose
  and must skip with a reason; the intra-repo gate still applies fully.
- **Two entries differing only in a free token.** `blast_radius_unit` and
  `duty` are domain-declared, so a domain could split one identity into two by
  inventing token spellings. The alias rule is the bound: a finding is raised
  only when two entries differ solely in a free token AND are observationally
  identical — same granted permissions and same admission acts — AND declare no
  duty-separation rationale. A genuine per-unit pair differs in
  `achieved_scope`; a genuine duty pair differs in permissions or declares the
  rationale. Anything stricter re-kills the flaw the review already killed.
- **A provider whose narrowest permission spans surfaces.** Conformant when the
  spanned surfaces, the provider reason, and the gate obligation are declared;
  the check must not invalidate a deliberately narrow identity because the
  provider's granularity is coarser than the axis.
- **A gate obligation naming a gate that was renamed or removed.** The
  obligation no longer resolves and is a finding: an unenforced obligation
  converts an undetected widening into a documented one.
- **A domain that holds no client-tenant identities.** Publishes no fragment
  and is refused by nothing: the pack's roster check passes with an explicit
  notice, so admitting a fourth blocking check into every domain's gate cannot
  break a repo that has nothing to declare.
- **An `evidence_ref` pointing into another repository.** It is a declared
  pointer, not a resolved link: the canonical validator is network-free and
  single-repo, so it checks the pointer's SHAPE only. Resolution is the
  cross-domain doc-health family's, which assembles from pinned repos.

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
  `consent_ref`. The fragment MUST additionally carry the free-token LEGEND
  required by FR-034, binding each `blast_radius_unit` and `duty` token used in
  that fragment to its provider-native identifier, and each entry MAY carry the
  OPTIONAL `duty_separation_rationale` required by FR-038's alias rule. The
  field list above is the ratified one (OpenSpec task 2.1) and MUST NOT be
  reduced; the legend and the duty-separation rationale are the only additions
  to THIS ENTRY LIST, and each exists because ruling R7's own rule cannot be
  evaluated without it. The one addition to the ADMISSION ACT's list —
  `exceeds_governed_unit`, FR-002 — is a different list and is justified on the
  same footing: the ratified requirement that a structural-to-logical
  degradation be a "declared, CHECKABLE, tested fact" cannot be evaluated
  without it.
- **FR-002**: `admission` MUST be a LIST whose members each declare the
  surface, the act performed in that surface's own administrative console, the
  scope that act achieves, whether the resulting bound is provider-enforced or
  logic-enforced, an evidence reference for a successful call, and the time it
  was verified. A record MUST NOT express admission as a single act.
  Each member MUST ADDITIONALLY declare whether the scope that act achieves
  reaches BEYOND the entry's governed blast-radius unit
  (`exceeds_governed_unit`). That declaration is required because
  `achieved_scope` is provider-native and opaque to the neutral layer, so a
  check may compare scope tokens for equality but MUST NOT read breadth out of
  one — and without it the ratified obligation that a structural-to-logical
  degradation be a "declared, CHECKABLE, tested fact" has nothing to check. It
  is an addition to the act's field list on the same footing as the free-token
  legend: the ratified rule cannot be evaluated without it.
- **FR-003**: Provider consent alone MUST NOT be recordable as access; an
  admission act without verification evidence MUST be represented in a distinct
  unverified state and MUST be excluded from the identity's effective reach;
  effective reach MUST be the union of verified acts. That union MUST be
  computed and REPORTED, and — because its members are opaque tokens — it is
  defined concretely as the set of `(surface, achieved_scope)` pairs over
  VERIFIED acts only, together with the derived exceedance flag: the entry's
  reach exceeds the governed blast-radius unit if ANY verified act declares
  `exceeds_governed_unit`. That derivation is what makes the ratified "the
  effective reach is their union, NOT the narrower act" a computation rather
  than an assertion.
- **FR-004**: `granted_permissions[]` in provider-native identifiers MUST be
  required on every entry, and `authority_class_achieved` MUST be checkable
  against it — the record MUST NOT be able to assert an achieved class its
  permissions contradict. Checkability MUST be RECORD-INTERNAL: each member
  carries the provider-native identifier verbatim PLUS the class it confers and
  the admission surfaces it reaches, because a network-free validator cannot
  resolve an opaque identifier against a provider catalogue and MUST NOT infer
  provider semantics from an identifier's spelling. This is the Assumptions
  block's "the mapping … is declared in the record", given a shape.
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
- **FR-008**: Each entry MUST declare, per admission surface — as a MAPPING
  keyed by admission-surface member, not a single boolean, because a
  provider-forced multi-surface identity needs one answer per surface —
  whether a principal scoped to the governed blast-radius unit is available.
  A bound MAY be recorded as logic-enforced only where no such principal
  exists, with the provider reason recorded. A bound recorded as
  provider-enforced where no such principal exists MUST be a finding, and an
  available per-unit principal left unused while logical enforcement is
  declared MUST be a finding naming the available principal.
- **FR-009**: Provider-forced breadth — spanned admission surfaces or an
  achieved class above the intended one — MUST be declarable with the provider
  reason and a gate obligation, and MUST be conformant when so declared.
  Undeclared reach MUST be a finding naming the surface and the permission that
  reaches it. The checks MUST NOT invalidate a deliberately narrow identity
  merely because the provider's permission granularity is coarser than the
  axis.
- **FR-010**: Where achieved authority exceeds intended authority, the entry
  MUST declare the excess with the reason no narrower permission exists, the
  bounding mechanism, the gate obligation, and the enforcement-test reference.
  The SAME obligation MUST bind a scope excess: a VERIFIED admission act
  declaring `exceeds_governed_unit` (FR-002) MUST be covered by a
  `declared_excess`, and an act that exceeds the governed unit with no such
  declaration MUST be a finding naming the act, its achieved scope, and the
  unit it exceeds. This is the rule that makes the change's own motivating
  measurement enforceable — a no-scope-selector admission act that silently
  converts a provider-enforced bound into a gate-logic one — rather than merely
  expressible. An entry's name MUST NOT describe a narrower authority than it
  achieves.
  The ratified field list carries no `purpose` field, so the name check reads
  `identity_ref` and fires in ONE direction only — an observation-suggesting
  token in the name while `authority_class_achieved` is `mutate` — against a
  small closed token list declared in the validator and naming the token it
  matched, so the rule stays deterministic and inspectable rather than
  becoming an open-ended reading of prose.
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
  The INSTRUMENT citation MUST actually resolve — presence of a citation is not
  resolution — and that resolution MUST be INTRA-REPO, against the TARGET domain
  repository's own consent-instrument records, which makes it a repo-context
  rule of the same class as FR-011's gate obligation and explicitly NOT a
  cross-repository read of the kind FR-037 forbids. "In force" MUST be read
  against the consent family's own closed lifecycle: an instrument that is
  `executed` or `amended`, never one that is `draft`, `pending_signatures`,
  `terminated`, or `withdrawn`. Because the consent family declares no domain
  placement, resolution MUST use the mechanism its own validator uses — a kind
  sweep for `xfactory_consent_instrument` over the target repo, matching the
  citation against each record's `instrument_id`. The CAPABILITY citation MUST
  be present and
  domain-qualified; this release does NOT additionally resolve it against the
  target repository's promoted capability set, because the ratified resolution
  clause attaches to the instrument citation alone and the ratified scenario for
  the capability is an absence test ("names no ratified capability"). That
  omission is a recorded reading, not an oversight.

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
  surface, an entry with no consent instrument, a genuine full-tuple
  duplicate, a roster instance outside the declared placement, and an
  ALIAS PAIR (two entries differing solely in a free token while
  observationally identical, with no duty-separation rationale). Each negative
  MUST fail for its own reason rather than incidentally.
- **FR-017**: The corpus MUST carry POSITIVE regression fixtures that keep the
  two killed flaws killed: two entries differing only in blast-radius unit
  (a GENUINE per-unit pair, differing in `achieved_scope`), two entries
  differing only in duty (a GENUINE duty pair, differing in granted permissions
  or declaring the duty-separation rationale), a provider-forced multi-surface
  reader with its declaration, and a `planned` entry — each validating clean
  with zero findings. These fixtures MUST stand alongside the alias-pair
  negative of FR-016, so the alias rule is measured as a discrimination and not
  merely as a refusal.
- **FR-018**: The validator MUST refuse a negative fixture that validates
  cleanly, a negative fixture that fails for the wrong reason, and a corpus
  where a registered probe has no file or a file has no registration.
- **FR-019**: The feature MUST package instantiable examples under
  `examples/client-identity-roster/`, with a `negative/` subdirectory and a
  README following the sibling families, covering the Business Central
  two-admission-act worked case — a provider-enforced per-environment
  application user in Sandbox1 with no production application user, PLUS the
  admin-center Entra-app authorization that has no scope selector and therefore
  reaches every environment, with the resulting excess, gate obligation, and
  enforcement test declared — together with a provider-forced multi-surface
  reader, a duty-separated pair, and one `planned` entry, for a client held by
  two domains. Because a fragment is per (client, domain), the four mandated
  cases MUST span at least TWO fragment files. The directory convention is
  `examples/<family>/` because the schema lives in `contracts/schemas/`; the
  rival `contracts/<family>/examples/` convention belongs to families owning a
  `contracts/` subdirectory and MUST NOT be adopted here.
- **FR-020**: The contract MUST declare the placement of a domain's roster
  fragments as `credentials/client-identity-roster/<client_ref>.yaml` in the
  domain repository — inside the tree `scripts/validate-credential-contracts.py`
  already scans recursively — one file per (client, domain) pair. That
  validator's skip-with-notice over these files is EXPECTED behaviour blessed
  by the promoted `credential-contracts` spec, not a coverage gap, because the
  canonical roster validator claims exactly that path. The consumption rule
  registered with the schema MUST state the placement and note the expected
  skip.

**Release registration**

- **FR-021**: The new schema MUST be registered in `contracts/manifest.yaml`
  with `path`, `source_path`, `type`, `schema_version`, `sha256`,
  `compatibility`, `adapter_owner`, and a `consumption_rule`, MUST carry a
  `contracts/CHANGELOG.md` entry, and MUST bump the contract bundle from its
  current `contract-v1.31` to `contract-v1.32` with the matching release digest
  inventory, such that digest verification passes. Every OTHER schema this
  feature edits — the consent-instrument family under FR-039, and the canonical
  credential-contracts schema under FR-028 — MUST have its manifest row
  refreshed in the same bundle: new `sha256`, the bumped
  `schema_version`/`contract_schema_version`, and `compatibility` declared in
  the shape the last bump's rows use, so no consumer resolves a stale digest.

**The three wirings**

- **FR-022**: Intra-repo entry conformance MUST be BLOCKING through PACK
  MEMBERSHIP: `scripts/validate-client-identity-roster.py` MUST join the
  `domain-conformance-checks` pack as its fourth member, so that a nonzero exit
  fails the owning domain's conformance gate under the pack's own rule.
  Registration MUST be accompanied by the `domain-conformance-checks` MODIFIED
  delta this packet now carries (Decision A) — the promoted pack requirement
  enumerates its scripts exhaustively, so enrollment without the delta is an
  undeclared modification of a promoted capability. The pack's existing rules
  apply unchanged to the new member: it takes its target repo as an explicit
  argument, runs from the pinned openxFactory checkout, and MUST NOT be copied
  into a domain repo. In a target repo publishing no roster fragment the check
  MUST exit 0 with an explicit notice.
- **FR-023**: Cross-domain composition MUST land as a sixteenth deterministic
  doc-health family with family id `client-identity-composition`, implemented
  in `scripts/doc_health/client_identity_composition.py` and registered in the
  family registry (`FAMILIES`, and `FAMILY_IDS` so it renders a report section)
  with EACH FINDING carrying its own resolution class — the family MUST NOT
  take a blanket `FAMILY_RESOLUTION` entry, because that registry assigns one
  class per family and this requirement's contested rule below needs mixed
  classes; per-finding classification is the precedent of the three other late
  families. It assembles per-client fragments
  published by pinned domain repositories and reports ONLY shared identity
  material and undeclared cross-domain reach. The id and module name MUST NOT
  collide with `scripts/doc_health/shared_identity.py`, which belongs to the
  active `add-shared-identity-seeds` lane: "shared identity material" is a
  finding CLASS inside this family, never the family's name. The family MUST
  NOT duplicate any intra-repo rule, MUST skip explicitly with a reason when
  there is nothing to compose, MUST make no model call or network request, and
  MUST classify a finding that contradicts a ratified capability as contested
  rather than auto-fixable.
- **FR-024**: Two domains each holding their own separate identity on one
  admission surface and authority class in one client tenant MUST NOT be a
  finding at any level.
- **FR-025**: The implementation's family set MUST agree with the RATIFIED
  DELTA wording (`openspec/changes/add-client-identity-roster/specs/doc-health/spec.md`,
  "sixteen check families"), NOT with the promoted spec text, which still says
  fifteen and is rewritten by the OpenSpec archive step after this feature
  lands. This feature MUST NOT edit
  `openspec/specs/doc-health/spec.md`. It MUST update the count-bearing prose
  sites it owns — at minimum the `scripts/doc_health/families.py` module
  docstring ("The fifteen contract check families." on line 1, plus that
  docstring's note naming which module owns which late family, which must name
  the sixteenth) — and MUST leave ordinal statements about earlier families
  (for example "the fifteenth deterministic family" in
  `scripts/doc_health/proposal_origin.py` and the README) untouched, because an
  ordinal is not a count. doc-health MUST report no new finding against the
  feature, which is the operative measurement: no automated assertion compares
  the implemented family count against promoted text.
- **FR-026**: The `consent-instrument` family MUST admit a governed identity
  standing in the consenting party's tenant as a first-class dependent-artifact
  reference kind — a named member of the closed dependent-kind enumeration
  (`consent_profile`, `credential_grant`, `adapter_activation`, `other`), not
  the `other` escape — and its cascade evidence obligation MUST cover the
  identity's removal or retirement AND the withdrawal of its provider-side
  admission, not merely credential revocation. The canonical consent validator
  MUST learn the new kind and its evidence obligation. The status-enumeration
  growth this obligation requires is FR-039.
- **FR-027**: Drift handling MUST NOT create, modify, widen, narrow, or remove
  any identity, permission, or admission, and MUST NOT trigger automated
  remediation; a drift finding MUST record the roster value and the observed
  value only.
- **FR-028**: An open drift finding against an identity MUST refuse grant
  issuance for that identity as an issuance precondition naming the finding.
  The NEUTRAL deliverable (Decision B) is a CLOSED `issuance_preconditions`
  vocabulary added to `contracts/schemas/xfactory-credential-contracts.schema.yaml`
  whose first member is the roster-drift precondition, declarable — optionally
  and additively — on an `xfactory_credential_requirements` record, plus the
  `credential-contracts` MODIFIED delta this packet now carries. A member
  outside the closed vocabulary MUST be refused. Declaring nothing MUST leave
  every existing requirement record valid. The vocabulary MUST be the only
  neutral expression of the refusal — no second parallel mechanism — and this
  feature MUST NOT edit the domain-local instance on OpsxFactory's
  `deployment_operator` / `aks_workload_administration`, whose extra-key
  precedent this vocabulary regularizes rather than replaces in place.
  REALIZATION IS FIXTURE-PROVEN: no producer of live drift findings exists
  anywhere in the family at archive time, so the neutral criterion is a
  conformant requirement-record fixture declaring the precondition plus a
  negative for an out-of-vocabulary token. Live refuse-then-allow behaviour is
  proven in the domain follow-up at the domain mint surface and MUST NOT be
  claimed as realized here.

**Boundaries this feature must not cross**

- **FR-029**: No client-tenant act, credential minting, live provider call, or
  network access MUST be performed or enabled by any artifact, check, or test
  in this feature; enrollment automation and drift remediation MUST NOT be
  built.
- **FR-030**: No EXISTING credential record shape, grant neutrality rule, or
  JIT discipline MUST change; ALL FOUR MODIFIED capabilities' existing suites
  and fixtures MUST remain green and unmodified in behaviour; no domain
  repository file MUST be edited by this feature — the OpsxFactory and
  LedgerxFactory fragments, and live client-tenant drift detection, are named
  follow-ups, not deliverables here. The two amendments are reconciled with
  this boundary by ADDITIVITY, which is the condition of their conformance: the
  `issuance_preconditions` vocabulary (FR-028) adds an OPTIONAL property, so no
  existing record becomes invalid and no existing record's meaning changes; the
  consent status growth (FR-039) adds an enum member, so no existing instrument
  changes state. A change to either that is not purely additive breaks this
  requirement and must be escalated rather than absorbed.
- **FR-031**: Surfaces outside the first-release vocabulary MUST NOT be added,
  and identities on them MUST NOT be treated as missing roster entries.

**Scope questions ruled by the architect, 2026-08-14**

- **FR-032**: Roster completeness — NONE IN THIS RELEASE. The canonical check
  MUST NOT enforce any completeness rule: neither the absence of a fragment nor
  the absence of an entry MUST be a finding, and no expected entry set MUST be
  derived from the domain's credential requirement classes or from any other
  source. The `planned` scenario's "is not reported as missing" MUST be read as
  the permissive guarantee it is, not as evidence that a missing-entry check
  exists. FR-031 and the out-of-scope-surface edge case are RETAINED as the
  guards that keep this from silently becoming a completeness rule later.
  Scoped completeness — factory-held identity classes, on first-release
  surfaces, in client tenants, with issued grants — MUST be recorded as a NAMED
  SUCCESSOR change and MUST NOT be built here, because on the estate as it
  stands an invented predicate fires permanently on 14 of 16 requirement
  classes and would demand an entry for a class whose ratified position is that
  the factory holds no identity at all.
- **FR-033**: Admission-evidence freshness — NO DECAY IN THIS RELEASE.
  `verified_at` MUST be recorded on every admission act, and verified versus
  unverified MUST be the only distinction any check draws. No maximum age, no
  re-verification interval, and no staleness finding, report, or
  issuance-precondition failure MUST be introduced.
- **FR-034**: Vocabulary closedness. The following MUST be CLOSED neutral
  enumerations, each enumerated explicitly in the schema: `admission_surface`
  (`business_central`, `exchange`), authority class (`observe`, `mutate`),
  `residency_model` (`client_tenant_single`, `vendor_tenant_multi` — the two
  models the ratified delta governs, whose prose names there are
  client-tenant-single and vendor-tenant-multi), `enforcement_mode`
  (`provider_enforced`, `logic_enforced` — its two members named explicitly
  rather than left to a free string), `lifecycle_state` (`planned`, `enrolled`,
  `retired`), and `identity_kind`. Members are spelled snake_case, the dialect
  every other member in this feature uses (`business_central`,
  `entra_app_registration`); the hyphenated English forms that appear in prose
  here and in the ratified delta name the same members and are deliberate
  prose, never a second token spelling. `identity_kind`'s members MUST be taken
  VERBATIM from the
  ratified delta or OpenSpec task 2.1 where those enumerate them; they do NOT
  (task 2.1 names the field only), so its members MUST be exactly the kinds the
  four mandated example cases require, closed at that set for this release, and
  the builder MUST NOT invent an unratified kind vocabulary. Extension of any
  closed set MUST follow the `admission_surface` route: the change that governs
  the new member adds it.
  `blast_radius_unit` and `duty` MUST be domain-declared tokens rather than
  neutral enumerations, constrained by pattern (`^[a-z0-9][a-z0-9_-]*$`), and
  each token used in a fragment MUST be declared exactly once in that
  fragment's LEGEND, which binds the token to its provider-native identifier
  (for example `sandbox1` → `Sandbox1`). Provider fidelity lives in the legend;
  `granted_permissions[]` and `achieved_scope` MUST stay provider-native. A
  token used without a legend entry, or declared twice, MUST be a finding.
- **FR-035**: Drift-finding representation — SHIPPED HERE, as a governed record
  in the roster contract family with its own `kind` and `schema_version`. The
  record MUST carry: `identity_ref` (the five-element uniqueness tuple that
  identifies the entry), `fragment_ref`, the rule id that produced it,
  `roster_value`, `observed_value`, `observed_at`, `opened_at`, a `status` of
  `open`, `resolved`, or `disposed`, and a disposition citation. `roster_value`
  and `observed_value` are mandatory because the ratified delta scenario says
  the check "records the roster value and the observed value". Field NAMES MUST
  borrow from doc-health where they apply, but the record MUST NOT claim
  alignment with, or storage in, any doc-health findings register: none exists,
  because doc-health is a stateless recompute and `health/dispositions.yaml`
  holds advice text rather than on-disk finding records. The FR-028 refusal
  MUST consume this record deterministically — an `open` status against the
  covering entry is the whole predicate. Whether the record ships as a second
  `kind` inside the roster schema or as its own schema file is an
  implementation choice, but either way it MUST be registered under FR-021
  (manifest row with sha256 and consumption rule, CHANGELOG entry, same
  `contract-v1.32` bundle) and MUST carry at least one packaged example and one
  negative fixture like every other record this feature ships.

**Requirements added by the 2026-08-14 rulings**

- **FR-036**: The canonical validator MUST sweep the ENTIRE target repository
  for files carrying `kind: xfactory_client_identity_roster`, not only the
  declared placement, and MUST report any instance outside
  `credentials/client-identity-roster/` as a MISPLACEMENT finding naming the
  offending path and the declared placement. Placement is mechanized, not
  advisory: without the sweep a stray fragment is covered by no kind-aware
  validator anywhere in the target repo, whatever tree it lands in.
- **FR-037**: `evidence_ref` MUST be a DECLARED POINTER — repository, path, and
  optionally a sha — whose SHAPE the canonical validator checks and whose
  TARGET it MUST NOT resolve, because that validator is network-free and reads
  one repository. Resolution of a cross-repository pointer MUST belong solely
  to the cross-domain doc-health family, which assembles from pinned repos and
  can therefore see the referenced tree. FR-011's requirement that a gate
  obligation resolve within the owning domain's workflow records is unchanged
  and unaffected: that target is intra-repo.
- **FR-038**: The alias rule MUST be implemented as stated and MUST NOT be
  broadened. A finding MUST be raised ONLY when two entries differ solely in a
  free token (`blast_radius_unit` or `duty`) AND are observationally identical
  — the same `granted_permissions[]` set and the same admission acts by
  (surface, act, `achieved_scope`, `enforcement_mode`) — AND declare no
  duty-separation rationale. The rationale MUST be a declarable field:
  `duty_separation_rationale`, an OPTIONAL entry property (FR-001), because a
  predicate over a declaration nothing can declare is unevaluable. Entries
  differing in `achieved_scope`, in granted permissions, or declaring the
  rationale MUST validate clean. The fixture
  obligation is threefold and inseparable: a genuine per-unit pair and a
  genuine duty pair each passing with ZERO findings, alongside one alias-pair
  negative that is refused. A rule that fires on either genuine pair has
  regressed the flaw the cross-model review killed.
- **FR-039**: The `consent-instrument` closed status enumeration MUST grow by
  `withdrawn`, because the ratified delta requires cascade behaviour on
  "terminated or withdrawn" while the enumeration admits only `terminated`
  today. `withdrawn` MUST be a distinct member and MUST NOT be aliased onto
  `terminated`: withdrawal by the consenting party and termination are distinct
  events. The cascade obligation MUST fire on both. Every declaration of that
  closed set MUST grow together, including the repetition in
  `contracts/schemas/consent-instrument-class-registry.schema.yaml`. Growth
  MUST follow the schema's own stated rule — a `contract_schema_version` bump —
  with the affected rows re-registered at `contract-v1.32` and `compatibility`
  declared in the shape the previous bump's rows use. Because the growth is
  ADDITIVE, every existing conformant instrument and fixture MUST remain valid
  unchanged, which is how FR-030's "existing suites unaffected" is honoured
  alongside a modification this change declares.

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
  scope, enforcement mode, evidence of a successful call, verification time,
  and whether that achieved scope exceeds the entry's governed blast-radius
  unit. Verified acts union into effective reach — the set of their
  (surface, achieved scope) pairs plus the OR of their exceedance
  declarations, which is how "the union, not the narrower act" is computed
  rather than asserted; unverified acts are a distinct state that contributes
  nothing.
- **Declared excess**: the record of provider-forced breadth, achieved-class
  overshoot, or a scope that reaches beyond the governed blast-radius unit —
  provider reason, bounding mechanism, gate obligation, enforcement test —
  which converts an undeclared widening into a declared, tested one. The third
  case is the one this change exists for: an admission act with no scope
  selector, converting a bound the provider enforced into one only gate logic
  enforces.
- **Gate obligation**: a reference to an existing gate in the owning domain's
  workflow records plus the test proving that gate refuses an out-of-unit
  target.
- **Residency declaration**: identity kind, registration home tenant, principal
  locations, and the residency model with its per-model obligations.
- **Drift finding**: a governed record in the roster contract family with its
  own `kind` and `schema_version` — identity reference, fragment reference,
  rule id, `roster_value`, `observed_value`, `observed_at`, `opened_at`,
  `status` (`open|resolved|disposed`), disposition citation — which mutates
  nothing and, while `open`, refuses grant issuance for its identity. It is not
  a doc-health register entry: no such register exists.
- **Issuance precondition**: a member of the closed neutral
  `issuance_preconditions` vocabulary a credential requirement record may
  declare. Its first member is roster drift; declaring it is how the refusal
  becomes a property of a pinned contract rather than of one domain's file.
- **Free-token legend**: the per-fragment declaration binding each
  `blast_radius_unit` and `duty` token to its provider-native identifier —
  declared once per token, the place provider fidelity lives for values the
  neutral layer deliberately leaves open.
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
  findings: a genuine per-unit pair, a genuine duty-separated pair, a declared
  provider-forced multi-surface reader, and a `planned` entry — while the
  alias-pair negative in the same corpus is refused by the alias rule. The
  measurement is the DISCRIMINATION between those cases; any finding against
  the genuine pairs is a regression of the two flaws the cross-model review
  killed, and a clean pass on the alias pair means the free tokens are
  unbounded.
- **SC-003**: The Business Central worked case is fully expressible in the
  neutral contract with no domain-local vocabulary: two admission acts with
  different achieved scopes and enforcement modes, a union effective reach, and
  a declared excess whose gate obligation resolves and whose enforcement test is
  named.
- **SC-004**: A reader of any conformant entry can determine, without leaving
  the record and the surface vocabulary, what the identity actually reaches,
  who enforces each bound, when each admission was last verified, which consent
  authorizes it, and whether it holds any standing credential.
- **SC-005**: A fragment at `credentials/client-identity-roster/<client_ref>.yaml`
  is claimed and checked by exactly one canonical validator, and a fragment
  carrying the roster kind ANYWHERE ELSE in the target repo is reported as
  misplaced by the whole-repo sweep — measured by a misplacement fixture placed
  outside `credentials/` entirely, with no path by which a roster instance is
  skipped as out of scope and covered by nothing.
- **SC-006**: The blocking/reporting split holds in measurement: an intra-repo
  nonconformance yields a nonzero exit from the domain gate, while a
  cross-domain shared-identity case yields a doc-health finding and leaves the
  domain gate exit unchanged.
- **SC-007**: A terminated instrument whose governed-identity dependent shows
  credential-only cascade evidence is a finding; the same instrument with
  identity-removal and admission-withdrawal evidence passes; and every existing
  instrument and fixture in the corpus validates unchanged.
- **SC-008**: The neutral refusal is proven BY FIXTURE: a conformant
  `xfactory_credential_requirements` fixture declaring the roster-drift member
  of `issuance_preconditions` validates, a fixture declaring an
  out-of-vocabulary token is refused naming the closed vocabulary, and a
  fixture declaring no preconditions at all still validates. Live
  refuse-then-allow is NOT measurable here and is not claimed: no producer of
  live drift findings exists in the family at archive time, and issuance
  happens at a domain mint surface this feature does not touch — that
  measurement belongs to the domain follow-up. The refusal path defined here
  performs no client-tenant mutation.
- **SC-009**: doc-health runs sixteen families, in agreement with the RATIFIED
  DELTA wording rather than with the promoted spec text (which still says
  fifteen until the archive step rewrites it), with the count-bearing prose
  sites this feature owns updated — at minimum the
  `scripts/doc_health/families.py` module docstring — the promoted
  `openspec/specs/doc-health/spec.md` left unedited, ordinal statements about
  earlier families left untouched, the new family reporting or skipping with an
  explicit reason, producing identical findings on repeated identical runs, and
  containing no intra-repo rule.
- **SC-010**: The green bar: repository validators pass,
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes, contract
  digests verify at `contract-v1.32` for every row the feature touches, all
  FOUR MODIFIED capabilities' existing test suites pass — `consent-instrument`
  and `doc-health` as declared at ratification, plus `domain-conformance-checks`
  and `credential-contracts` as amended by Decisions A and B — and doc-health
  reports no new finding against the change or its documents.
- **SC-011**: Every new check and test runs with no outbound network access and
  no model call, and produces byte-identical findings across runs.
- **SC-012**: No file in any domain repository is modified by this feature, and
  no credential is minted and no provider call is made at any point in its
  execution or tests.
- **SC-013**: Absence is never a finding, measured three ways: a fixture domain
  repo with no roster fragment exits 0 with an explicit notice; a fragment that
  omits an identity the domain demonstrably holds exits 0; and no code path in
  the validator derives an expected entry set from credential requirement
  classes or from any other inventory. A single finding produced by absence is
  a scope breach, not a strictness improvement.
- **SC-014**: Every closed vocabulary is enumerated in the schema and refuses a
  value outside it, while `blast_radius_unit` and `duty` accept any
  pattern-conformant token that carries a legend binding — measured by one
  negative per closed set plus a legend-missing negative and a
  legend-duplicated negative.

## Assumptions

- **The record kind is `xfactory_client_identity_roster`** and the fragment
  granularity is one file per (client, domain) pair, following `client_ref` +
  `domain` at the top of the record; the cross-domain family assembles N such
  fragments rather than reading a single multi-domain file.
- **Packaged examples follow the repository's per-family directory
  convention** (`examples/client-identity-roster/`, with `negative/` and a
  README like its siblings), even though the governed sketch names a single
  file path. The tree carries two conventions and this family takes the first:
  `examples/<family>/` where the schema lives in `contracts/schemas/` (it
  does), and `contracts/<family>/examples/` where the family owns a `contracts/`
  subdirectory (openxWallet, feature 006) — the latter is not a target to
  converge on.
- **The validator follows the sibling `validate-*.py` contract** for arguments,
  output, and exit codes (0 clean, 1 findings, 2 harness error), and is
  invoked against a target repository from the pinned checkout — the same
  consumption shape as the existing canonical validators and the conformance
  pack.
- **The current bundle is `contract-v1.31`**, verified in
  `contracts/manifest.yaml`, so this feature registers at `contract-v1.32` —
  re-confirmed 2026-08-14 against the manifest, with no intervening bump.
- **`granted_permissions[]` is provider-native and opaque to the neutral
  contract**: the schema constrains shape, while the mapping from a permission
  identifier to the facts the checks need — the achieved authority class it
  confers (FR-004) and the admission surfaces it reaches (FR-009) — is declared
  in the record beside the identifier and checked for internal consistency, not
  resolved against any provider catalogue (which would require network access
  this feature forbids) and never inferred from how the identifier is spelled.
  The same principle governs `achieved_scope`: the token rides verbatim, and
  the one fact a check needs about it — whether it exceeds the governed
  blast-radius unit — is declared on the act (FR-002).
- **Promoted-spec text is rewritten by the OpenSpec archive step, not by this
  feature** (ruled, FR-025): the feature's obligation is that the
  implementation matches the RATIFIED DELTA wording, and that it updates the
  count-bearing prose it owns. The window in which the promoted doc-health spec
  says fifteen while the code implements sixteen is tolerated and is already
  the tree's state — the README's OpenSpec Records block says "sixteenth
  family" today and doc-health is green, because no automated check asserts the
  count against promoted text.
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
- **The Business Central evidence chain motivating the contract IS on
  OpsxFactory `main`.** The seed handoff's claim that it lived only on
  `evidence/bc-general-verify-probe-20260810` (PR #19, open) is STALE and was
  corrected 2026-08-14: `c1a6270` is an ancestor of `origin/main`, the PR
  having merged. Packaged-example `evidence_ref` pointers therefore aim at real
  pinned content rather than at a branch that may never land — while remaining
  unresolved pointers at the canonical validator, per FR-037.
- **No producer of live drift findings exists anywhere in the family at
  archive time.** The drift-finding record shape ships here (FR-035) and the
  refusal's neutral declaration ships here (FR-028), but nothing yet observes a
  client tenant to emit one — live client-tenant drift detection is a named
  domain follow-up. Every drift-side criterion is therefore fixture-measured by
  construction, not by choice.
- **The ratified doc-health delta names no family id**, only the prose phrase
  "client identity roster composition", so the id is chosen here as
  `client-identity-composition` (FR-023) under the constraint that it must not
  collide with the concurrent `shared_identity` lane.
