# Feature Specification: openxWallet neutral contracts

**Feature Branch**: `006-openxwallet-contracts`

**Created**: 2026-08-07

**Status**: Draft

**Input**: Implement the ratified `add-openxwallet` OpenSpec change as neutral
contracts, a validator, and a negative-confirmation fixture corpus. Scope is
exactly OpenSpec tasks 3.1 and 3.2.

**Governing change**: `openspec/changes/add-openxwallet/` — ratified by Brett
Heap on 2026-08-07, authorizing exactly one Speckit feature. The change's
`tasks.md` is the authority for scope; this specification does not extend it.

**Capabilities realized**: `openxwallet` (core, eight requirements) and
`openxwallet-agent-profile` (first profile, three requirements).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A domain declares a wallet whose authority cannot exceed what its key custody evidences (Priority: P1)

A domain adopting wallets records, for each holder, a reference to a signing
key and the custody model that key is held under. The contract states what
each custody model evidences — that the holder acted, or merely that the
holder's execution environment acted — and refuses any authority claim the
declared custody cannot support. Raising authority becomes a custody question
rather than a trust assertion.

**Why this priority**: This is the ruling the change turns on and the reason
the capability is honest rather than decorative. Without the custody ceiling
a wallet record is a claim about identity that nothing checks; with it, an
audit record cannot assert something the key custody could not have proved.
It is also the smallest slice that stands alone: a domain can declare wallets
and get a real refusal on over-claimed authority with nothing else built.

**Independent Test**: Author a wallet record declaring a key readable by the
holder's own execution context, attach a grant claiming unsupervised
authority, and confirm the validator refuses and names the custody ceiling.
Repeat with isolated, per-use-authorized custody and confirm it passes.

**Acceptance Scenarios**:

1. **Given** a wallet record carrying a key reference and a declared custody
   model, **When** it is validated, **Then** it passes, and **When** the same
   record is given private key material in any field, **Then** validation
   fails naming the embedded key material.
2. **Given** a wallet whose custody evidences only that the environment acted,
   **When** a grant claims authority to complete an irreversible act with no
   approval before apply, **Then** validation fails and names the custody
   ceiling that authority exceeded.
3. **Given** a custody member that declares a key readable by the holder's
   execution context, **When** that member also claims to evidence that the
   holder acted, **Then** validation fails — the enumeration cannot be
   collapsed even by a future editor.
4. **Given** a grant derived from a parent grant, **When** the derived grant
   widens scope or extends lifetime beyond the parent, **Then** validation
   fails naming the widened dimension.
5. **Given** a grant exercised against a revoked parent, **When** the exercise
   record is validated, **Then** it fails — revocation is checked at exercise,
   not trusted from issuance.

---

### User Story 2 - A consuming capability expresses segregation of duties without reimplementing it (Priority: P2)

A capability that needs "the holder who did A may not be the holder who does
B" declares a distinct-holder constraint between two named acts on the same
object. The constraint is available and never implied: a capability declaring
none is not subject to one.

**Why this priority**: This is what the first consumer is blocked on.
LedgerxFactory lost its platform-level refusal when posting went
agent-executed, and the replacement control is unbuildable while every agent
reaches the platform through one shared credential. It is second only because
User Story 1 must exist for a holder to be identifiable at all.

**Independent Test**: Declare a distinct-holder constraint between a "create"
act and a "post" act, then record an exercise naming the same holder for both,
and confirm the validator refuses and names the constraint. Separately confirm
a capability declaring no constraint validates without one.

**Acceptance Scenarios**:

1. **Given** a declared distinct-holder constraint between two acts, **When**
   an exercise names the same holder for both, **Then** validation fails and
   names the constraint that was violated.
2. **Given** a capability that declares no distinct-holder constraint, **When**
   its grants are exercised, **Then** no distinctness is inferred or required.
3. **Given** an act reaching an external platform through a shared service
   credential, **When** the exercise record is validated, **Then** the
   presenting wallet key is recorded as the actor and the shared credential is
   recorded as transport; an act with no establishable wallet key is recorded
   as unattributed rather than assigned to a holder.

---

### User Story 3 - An agent holder declares what constitutes its identity, and a change to it ends its authority (Priority: P3)

A wallet holder of class agent declares the composition that constitutes its
identity as a hash over a declared component set, so a reader can tell what a
matching hash was actually asserting. Any change to that declared composition
revokes the agent's outstanding grants through the core's propagation rule,
with no tolerance band and no grace period.

**Why this priority**: It is the profile layer, and by ratification it must
sit above a holder-class-agnostic core rather than inside it. It is genuinely
independent — the core is usable by a domain with no agent holders at all.

**Independent Test**: Author an agent holder record carrying a composition
hash with no component set and confirm validation fails; author one with both
and confirm it passes; change one declared component and confirm the
attestation no longer matches the declaration.

**Acceptance Scenarios**:

1. **Given** an agent holder record, **When** it carries a composition hash
   without the component set that hash covers, **Then** validation fails.
2. **Given** a holder of a class other than agent, **When** it is validated,
   **Then** no composition is required of it and the core imposes none.
3. **Given** an agent grant whose scope names an approval posture, **When**
   that posture uses a term outside the neutral job envelope's
   `approval_policy` property set, **Then** validation fails as a parallel
   authority vocabulary.

---

### Edge Cases

- **A wallet reference used where a subject identifier belongs.** A subject or
  record may carry an optional wallet reference as attestation; resolution
  that treats it as the identifier is a validation failure. A domain adopting
  no wallets at all remains conformant and is refused by nothing.
- **A signature that is present but does not verify.** Recorded as a
  verification failure, distinctly from an unauthenticated request — the two
  describe different events and collapsing them loses the distinction that
  makes a stolen grant visible.
- **A grant presented without proof of possession.** Refused naming the
  missing proof, not the missing grant: the grant was supplied and is not what
  was lacking.
- **A retrieval corpus whose contents change hourly.** Covered by reference
  (identity and governing configuration) rather than by content, so ordinary
  corpus churn does not fire revocation while a change to what the agent may
  retrieve does. See Assumptions.
- **A future editor adding a custody member.** The enumeration's derivation
  rule is enforced, so a member cannot be added that is readable by the
  holder's execution context yet claims to evidence the holder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The contracts MUST define a wallet record carrying the holder's
  identifier, a reference to a signing key, and a declared custody model, and
  MUST refuse any record carrying private key material.
- **FR-002**: The contracts MUST define a CLOSED custody enumeration in which
  each member declares what it evidences and the authority it caps.
- **FR-003**: The custody enumeration MUST distinguish a key readable by the
  holder's own execution context from a key isolated from it, and MUST make
  that distinction structurally unforgeable: `evidences` is derived from
  declared properties and checked, never asserted independently.
- **FR-004**: The contracts MUST define a capability grant carrying audience,
  scope, expiry, and parent, and MUST refuse a derived grant that widens scope
  or extends lifetime beyond its parent.
- **FR-005**: The contracts MUST require proof of possession for exercise, and
  MUST record a verification failure distinctly from an unauthenticated
  request.
- **FR-006**: The contracts MUST cap the authority a wallet may hold by its
  declared custody model, and a refusal MUST name the custody ceiling.
- **FR-007**: The contracts MUST record, per exercise, the key that presented
  the grant, and MUST record an act attributable only to a shared credential
  as unattributed rather than assigned to a holder.
- **FR-008**: The contracts MUST express revocation propagating through
  derivation, checked at exercise rather than trusted from issuance.
- **FR-009**: The contracts MUST allow a consuming capability to declare a
  distinct-holder constraint between two named acts, and MUST NOT imply one
  where none is declared.
- **FR-010**: The contracts MUST NOT make a wallet a prerequisite for
  reconstructing a record, resolving a subject, or operating a domain, and
  MUST refuse a wallet identifier used as a subject identifier.
- **FR-011**: The agent profile MUST require an agent holder to declare a
  composition hash together with the component set that hash covers, and MUST
  refuse a hash without its set.
- **FR-012**: The agent profile MUST express agent authority as grant scope
  drawing approval terms from the neutral job envelope's `approval_policy`
  property set, and MUST refuse a parallel authority vocabulary.
- **FR-013**: A single validator MUST enforce every rule above, following the
  repository's existing `scripts/validate-*.py` shape and exit-code convention
  (0 clean, 1 findings, 2 harness error).
- **FR-014**: The fixture corpus MUST carry a NEGATIVE CONFIRMATION for each
  of the ten named violations — a recorded probe proving the check fails on
  the violation it exists to catch, and fails for that reason rather than
  incidentally.
- **FR-015**: The validator MUST refuse a negative fixture that validates
  cleanly AND a negative fixture that fails for the wrong reason, and MUST
  refuse a corpus where a registered probe has no file or a file has no
  registration.
- **FR-016**: No runtime, wallet infrastructure, key storage, issuance
  service, or signing implementation is created; no existing capability is
  modified; no patient or practitioner profile, certification battery,
  measured drift, or qualification tier is defined.

### Key Entities

- **Wallet record**: a holder identifier, a key reference, and a declared
  custody model. Never key material.
- **Custody model**: a member of a closed enumeration declaring whether the
  key is readable by the holder's execution context, whether use requires an
  authorization that context cannot supply, what a signature therefore
  evidences, and the authority ceiling that follows.
- **Capability grant**: audience, scope, expiry, and optional parent.
  Derivation narrows monotonically.
- **Grant exercise record**: the presenting key, the grant, the act, the
  custody model in force, and the verification outcome.
- **Distinct-holder constraint**: two named acts on one object that must be
  exercised by different holders, declared by a consuming capability.
- **Agent composition declaration**: a composition hash plus the component set
  it covers, each component declaring how it is bound.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All ten named violations are refused by the validator, each with
  a recorded probe naming the reason it was refused — zero pass silently.
- **SC-002**: A reader of any conformant wallet record can determine, without
  consulting anything outside the record and the custody enumeration, whether
  a signature evidences the holder or its environment.
- **SC-003**: A capability declaring no distinct-holder constraint validates
  unchanged, and a domain adopting no wallets is refused by nothing — measured
  by the existing capabilities' fixtures continuing to pass untouched.
- **SC-004**: The first consumer's control becomes expressible: the
  LedgerxFactory posting segregation-of-duties case can be written entirely in
  these contracts, with no domain-local authority vocabulary.
- **SC-005**: The validation bar is green with no new findings: repository
  validators pass, `openspec validate --all --strict` passes, and doc-health
  reports no new finding against the change or the staging topic.

## Assumptions

- **The composition component set covers corpora by reference, not content.**
  Every declared component states its binding mode. Components bound by
  content contribute their own digest to the composition hash (model version,
  prompt contract, tool manifest, policy version, parameters). A retrieval
  corpus is bound by reference: its identity and governing configuration —
  which corpus, what may be retrieved, under what selection rules — enter the
  hash; its row-level contents do not. Swapping the corpus or widening
  retrieval changes identity and revokes; documents arriving in an
  already-governed corpus do not. This settles OpenSpec task 3.2 and is
  recorded in `research.md`; both binding modes stay available for every
  component, so the contract makes the choice visible and checkable without
  making it for any domain.
- **The custody enumeration reads "only custody isolating the key" as a
  necessary condition, not a sufficient one.** This admits a third member —
  isolated but invocable without limit by the holder's execution context —
  that evidences the environment rather than the holder. A two-member set
  would satisfy the ratified text while letting a local signing daemon claim a
  hardware key's authority, which is the same collapse one level down. Full
  reasoning in `research.md`.
- **`approval_policy` is an object, not a flat enum.** The neutral job
  envelope defines it with three properties
  (`hermes_approval_required_before_apply`, `authority_agents_may_approve`,
  `human_escalation_required_for`). "An authority term outside
  `approval_policy`" therefore means a key outside that property set. The
  validator reads the legal vocabulary from the canonical envelope schema at
  runtime rather than restating it, so the two cannot drift.
- **Software custody reaches `act` rather than stopping below it.** Capping
  software custody lower would stall the first consumer, which is the outcome
  the ruling rejected when it declined to mandate hardware backing.
  Approval-before-apply is the compensating control; only unsupervised
  irreversible action requires evidence that the holder acted.
- **Contract registration follows the repository's release discipline.** New
  schemas are registered in `contracts/manifest.yaml` with per-file digests, a
  `contracts/CHANGELOG.md` entry, and a bundle version allocated at
  realization rather than reserved here.
- The `openxVault` boundary set by Brett on 2026-07-16 holds unchanged: the
  vault owns custody and its gate consumes these grants; this feature owns
  identity, keys, and authority.
