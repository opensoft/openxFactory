# Feature Specification: Trust-anchor neutral contracts

**Feature Branch**: `009-trust-anchor-contracts`

**Created**: 2026-08-21

**Status**: Draft

**Input**: Implement the ratified `add-trust-anchor` OpenSpec change as neutral
contracts, a validator, and a negative-confirmation fixture corpus. Scope is
exactly the change's tasks §4 (the two pre-schema settlements) and §5.1–5.9.
Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md` (task
5.10) is the bundle cut's, not this feature's.

**Governing change**: `openspec/changes/add-trust-anchor/` — ratified by Brett
Heap on 2026-08-21 ("ratify both proposals"), all design decisions adopted as
written, with OQ1 and OQ2 ruled as recommended. The change's `tasks.md` is the
authority for scope; this specification does not extend it.

**Capability realized**: `trust-anchor` (eight requirements).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A governed system knows what a certificate it trusts is worth (Priority: P1)

A system records the anchors it holds, and every certificate it trusts names the
anchor it is trusted THROUGH. The certificate's declared chain custody DERIVES
what the certificate evidences — that the named holder acted, or only that the
host presenting it acted — and caps the assurance any consumer may rely on it
for. Raising assurance becomes a custody change rather than a claim.

**Why this priority**: This is the pair of rulings the change turns on, and the
smallest slice that stands alone. Without the anchor framing there is nowhere for
revocation and rotation to attach and no trust set anyone can enumerate; without
the derived custody a certificate record is a claim about identity that nothing
checks. Both realizations owe exactly this much on day one.

**Independent Test**: Author an anchor record and a certificate declaring
host-held custody, attach a dependent binding requiring hardware-bound assurance,
and confirm the validator refuses and names the custody ceiling. Repeat with a
certificate whose key is isolated and per-use authorized and confirm it passes.
Separately, record a certificate as trusted whose chain terminates in no held
anchor and confirm it is refused with the missing anchor named.

**Acceptance Scenarios**:

1. **Given** an anchor record naming identity, chain position, validity window
   and declared custody, **When** it is validated, **Then** it passes, and
   **When** the same record is given private key material in any field — in
   plaintext or in a reversible encoding — **Then** validation fails naming the
   embedded material.
2. **Given** a certificate whose chain terminates in no anchor the evaluating
   system holds, **When** it is recorded as trusted, **Then** validation fails;
   and **When** it is recorded as refused, **Then** the refusal names the missing
   anchor and well-formedness is not a representable basis for acceptance.
3. **Given** a certificate declaring host-held custody, **When** a dependent
   binding requiring holder-attributed assurance is recorded as admitted,
   **Then** validation fails and the refusal it should have carried names the
   CUSTODY CEILING rather than anything about the certificate's contents.
4. **Given** a certificate record with no custody declaration, **When** it is
   validated, **Then** its `evidences` and ceiling must be the registry floor's,
   and a ceiling above the floor's fails.
5. **Given** an anchor whose validity window closes or which is revoked,
   **When** a certificate chaining to it is recorded as trusted, **Then**
   validation fails, and a certificate whose own validity outlives its anchor's
   fails independently of that.

---

### User Story 2 - A renewal cannot report success while a dependent is broken (Priority: P2)

Every authority binding that references a certificate's key material is recorded
against that certificate, so the rebind set a renewal will create is computable
BEFORE the renewal. A renewal producing new key material is incomplete until each
dependent is re-bound and each rebind evidenced, and a renewal that succeeded at
the authority while leaving a dependent unbound is recorded as a failure of the
ISSUING WORKFLOW.

**Why this priority**: This is the obligation the live realization contributed by
walking into it, and the one with a live exposure window: the first renewals after
adoption are where an incomplete enumeration shows up. It is second only because a
certificate has to be a governed record with a known custody before anything can
be recorded against it.

**Independent Test**: Record a renewal with new key material, two enumerated
dependents and evidence for one, marked complete; confirm the validator refuses
and names the unevidenced dependent. Repeat with the renewal marked failed and
attributed to the issuing workflow and confirm it passes. Attempt to record the
failure as the dependent's and confirm the shape refuses it.

**Acceptance Scenarios**:

1. **Given** a renewal with new key material, **When** it is reported complete
   while an enumerated dependent carries no succeeded rebind evidence, **Then**
   validation fails — whether the renewal was requested or unattended, since no
   rule keys on the mode.
2. **Given** a renewal that left a dependent unbound, **When** the record
   attributes the failure to that dependent, **Then** the record cannot be
   authored: the attribution is a constant naming the issuing workflow.
3. **Given** a renewal that reused the existing key material, **When** it is
   validated, **Then** it passes with the obligation explicitly declared not to
   arise and the rebind list required to be empty, so the absence of evidence is
   not read as an omission.
4. **Given** a certificate whose dependent enumeration is declared incomplete,
   **When** a renewal is recorded as having proceeded, **Then** validation fails;
   and a renewal misdeclaring the enumeration state fails against the
   certificate record.
5. **Given** a dependent binding discovered by an authentication failure,
   **When** the certificate record carries no defect naming it, **Then**
   validation fails; and a defect resolved without the binding appearing in the
   enumeration fails, so the incident cannot be closed by re-binding alone.

---

### User Story 3 - A realization the family does not operate stays conformant by declaring what it cannot evidence (Priority: P3)

Each realization publishes a conformance declaration covering every obligation:
satisfied, partial, or cannot, with a reason. Records that fall short cite the
obligation entry that declares the shortfall, and a consumer that needs an
obligation the declaration cannot support refuses the certificate for that use
with the gap named.

**Why this priority**: It is what keeps the contract honest rather than
aspirational, and it is genuinely independent — the first two stories are
satisfiable by a self-hosted authority alone. It is third because a declaration is
only meaningful once there are records for it to be true or false about.

**Independent Test**: Author a declaration for an authority the family does not
operate, with the issuance obligation partial at the declared floor and the
authority-material obligation recorded as cannot; confirm an issuance record at
the floor citing that entry passes, that the same record citing a satisfied entry
fails, that an entry dated after the record it excuses fails, and that a dependent
binding requiring the cannot-obligation may not be recorded as admitted.

**Acceptance Scenarios**:

1. **Given** a realization running on an authority the family does not operate,
   **When** its declaration names each obligation it cannot fully satisfy and
   why, **Then** its records validate on the strength of that declaration.
2. **Given** a declaration omitting one obligation, **When** it is validated,
   **Then** it fails: the declaration is closed over all eight obligations, and
   the undeclared one is the shortfall.
3. **Given** an obligation declared `cannot`, **When** a dependent binding
   requiring it is recorded as admitted, **Then** validation fails; the
   conformant record is a refusal naming the gap entry.
4. **Given** a record that does not establish what an obligation requires,
   **When** it cites an entry recorded as satisfied, or an entry belonging to
   another realization, or an entry declared after the record's own moment,
   **Then** validation fails in each case.

---

### Edge Cases

- **A future editor adding a custody member.** The derivation is enforced, the
  top of the ladder must be earned on rank rather than on a level's name, no
  host-evidencing member may reach or exceed a holder-evidencing member's
  ceiling, and two members may not declare the same discriminator pair. Adding
  operator escrow as a tier trips the last of these, which is the ratified OQ2
  ruling made structural rather than editorial.
- **A hardware-resident key with no per-use gate.** Lands in the
  host-evidencing member and evidences the HOST. "Hardware" is not a
  discriminator, and the family's own live canary contains both cases.
- **An authority whose internals the family cannot read.** Its anchors carry no
  credential record for their key material, which the shape admits only alongside
  a declared shortfall — so the honest arrangement validates and the silent one
  does not.
- **A certificate nobody can explain.** Recorded with the question answered
  UNANSWERED and a revocation-candidate disposition, both constants, so an absent
  issuance record cannot be written up as an approval; and it may not be recorded
  as trusted.
- **A revocation whose propagation cannot be evidenced.** Escalated as an OPEN
  EXPOSURE against the record's own assessment moment, so the record is a stable
  statement rather than a claim that decays.
- **A domain that operates no certificate authority.** Refused by nothing. This
  capability imposes no obligation on a domain that has none.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The contracts MUST define an anchor record carrying identity, chain
  position, validity window, admitted issuance authorities and declared custody,
  and MUST refuse any record carrying private key material at any depth,
  including in a reversible encoding.
- **FR-002**: A certificate record MUST name the anchor it is trusted through,
  and trust MUST have exactly one representable basis — a held anchor record —
  with a refusal for a chain terminating nowhere naming the missing anchor.
- **FR-003**: The contracts MUST define a CLOSED chain-custody enumeration in
  which each member declares what it evidences and the assurance it caps, with
  `evidences` DERIVED from declared properties and checked, never asserted.
- **FR-004**: The enumeration MUST distinguish a key readable by the using host
  from one isolated from it, MUST make the distinction structurally unforgeable,
  and MUST NOT admit a second axis (operator escrow) as a member.
- **FR-005**: The enumeration MUST compose with `openxwallet`'s ratified custody
  rule rather than restate a second custody model — each member naming its
  openxWallet counterpart, resolved and checked against that registry at run
  time.
- **FR-006**: A certificate record with no custody declaration MUST resolve to
  the registry's declared floor and MUST NOT carry an assurance ceiling above it.
- **FR-007**: An issuance-evidence record MUST establish which anchor issued,
  under which admitted authority, on whose request and when, with exactly two
  establishment levels representable and nothing weaker; the floor level MUST
  require both the policy attestation and the authority's own log, and MUST make
  asserting per-certificate provenance unrepresentable.
- **FR-008**: Authorization MUST be derived from the anchor's admitted authority
  set, and a certificate whose issuance evidence is unauthorized MUST NOT be
  recorded as trusted.
- **FR-009**: A certificate with no issuance evidence MUST record the question as
  UNANSWERED with a revocation-candidate disposition, and MUST NOT be recorded as
  trusted.
- **FR-010**: A dependent-binding record MUST carry the holding system (inside
  the family or outside it), what it binds, the key GENERATION referenced, the
  assurance it requires and its rebind status; and a certificate record MUST
  enumerate its bindings with a declared completeness state.
- **FR-011**: A renewal record MUST NOT be able to read "complete" with an
  unevidenced dependent — structurally in the schema for a recorded rebind, and
  by comparison against the certificate's enumeration for an omitted one.
- **FR-012**: A renewal's failure attribution MUST be a constant naming the
  issuing workflow, and no rule may key on whether the renewal was unattended.
- **FR-013**: A key-preserving renewal MUST declare that no obligation arises and
  MUST carry an empty rebind list, so the absence of evidence is a declared fact.
- **FR-014**: A renewal planned against an enumeration declared incomplete MUST
  be refused, and a renewal misdeclaring that state MUST fail against the
  certificate record.
- **FR-015**: A dependent discovered by an authentication failure MUST oblige a
  defect entry on the certificate record, and a defect MUST NOT be resolvable
  without naming the binding added to the enumeration.
- **FR-016**: A revocation-propagation record MUST carry a declared bounded
  window whose arithmetic is checked, the downstream authority reached, and
  propagation evidence; MUST realize propagation through `openxwallet`'s
  derivation rule as a constant rather than a second vocabulary; and MUST record
  an escalated open exposure where the window closed unevidenced.
- **FR-017**: Revocation MUST reach the authority the revoked object supported,
  computed over the corpus rather than asserted, for BOTH target kinds the
  ratified requirement names: revoking an ANCHOR MUST reach the certificates
  chaining to it or to any anchor beneath it, and revoking a CERTIFICATE MUST
  reach the authority every admitted binding in that certificate's own dependent
  enumeration supported. (Corrected 2026-08-21: this requirement previously named
  anchors only, narrowing the ratified text — "revoking a certificate or an
  anchor revoke[s] the authority that certificate or anchor supported" — and left
  the ordinary case, one certificate revoked, resting on whatever the propagation
  record chose to list.)
- **FR-018**: Revocation standing MUST be checked at USE as the only
  representable basis, and a revoked certificate MUST NOT be recorded as trusted.
- **FR-019**: Anchor key material and issuance, revocation or administration
  credentials MUST exist only as `credential-contracts` references with vault
  bindings, at the strictest member of the closed set — or with the shortfall
  declared; and brokering into ephemeral scope MUST be a constant rather than a
  boolean.
- **FR-020**: A conformance declaration MUST cover all eight obligations exactly
  once, each with a satisfaction value and a reason, and MUST carry which
  issuance-evidence form the realization achieves.
- **FR-021**: A declared gap MUST NOT admit a use that requires it, a shortfall
  citation MUST resolve to an entry that actually declares it for the same
  realization, and an entry declared after the record citing it MUST fail.
- **FR-022**: A single validator MUST enforce every rule above, following the
  repository's `scripts/validate-*.py` shape and exit-code convention (0 clean,
  1 findings, 2 harness error), with a self-test layer and an optional repo-scan
  layer whose context is closed over the scanned repository.
- **FR-023**: The fixture corpus MUST carry a NEGATIVE CONFIRMATION for each of
  the ten named violations, and at least one per ratified requirement — a
  recorded probe proving the check fails on the violation it exists to catch, and
  fails for that reason rather than incidentally.
- **FR-024**: The validator MUST refuse a negative fixture that validates
  cleanly, one that fails for the wrong reason, a requirement with no probe, and
  a fixture claiming a requirement that does not exist.
- **FR-025**: No certificate authority, anchor, key, credential, issuance or
  revocation service, deployment topology or runtime is created; no existing
  capability is modified; no product profile is defined; no domain is obliged to
  operate a certificate authority.

### Key Entities

- **Trust anchor**: the governed record a system trusts. Identity, chain
  position, validity, admitted issuance authorities, declared custody. Never key
  material.
- **Certificate record**: the anchor it is trusted through, subject, validity,
  declared chain custody, derived `evidences` and ceiling, issuance evidence or
  its honest absence, the dependent-binding enumeration, record defects, and the
  evaluation with its at-use standing check.
- **Chain-custody model**: a member of a closed enumeration declaring whether the
  key is readable by the using host, whether use requires an authorization that
  host cannot supply, what a presentation therefore evidences, the assurance
  ceiling that follows, and its openxWallet counterpart.
- **Issuance evidence**: anchor, admitted authority, request provenance, time,
  and the establishment level actually achieved.
- **Dependent binding**: one authority binding referencing a certificate's key
  generation, in any system inside or outside the family, with the assurance it
  requires, its admission, and its rebind status.
- **Renewal record**: whether key material changed, the enumerated dependents,
  per-dependent rebind evidence, and a completion state that cannot read
  "complete" with an unevidenced dependent.
- **Revocation propagation**: what was revoked, the declared window, the
  downstream authority reached, the evidence, and the open-exposure escalation.
- **Conformance declaration**: per obligation, satisfied / partial / cannot with
  a reason and a date, closed over the capability's eight obligations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All ten named violations are refused by the validator, each with a
  recorded probe naming the reason it was refused — zero pass silently.
- **SC-002**: A reader of any conformant certificate record can determine,
  without consulting anything outside the record and the custody registry,
  whether the named holder or its host was evidenced — including where no custody
  was declared.
- **SC-003**: Both realizations in the change's impact map are expressible: the
  self-hosted authority conforms by construction, and the authority the family
  does not operate conforms on the strength of its declaration, with its
  shortfalls costing it something at point of use.
- **SC-004**: The custody enumeration cannot be collapsed by a future editor —
  the derivation, the earned top level, the ordering and the single-axis rule are
  each proven by a probe that goes red when its rule is neutered.
- **SC-005**: Every finding code the corpus depends on is load-bearing: neutering
  any one of them turns the packaged corpus red.
- **SC-006**: The validation bar is green with no new findings: the canonical
  validator self-tests and scans clean, `openspec validate --all --strict`
  passes, and doc-health reports no new finding against this feature.

## Assumptions

- **The chain-custody enumeration mirrors openxWallet's mechanism and asks its
  two questions of the USING HOST.** The hazard is identical — a key the thing
  presenting it can read cannot evidence who decided to present it — so the
  members map one-to-one onto openxWallet's, and the mapping is checked at run
  time rather than restated. Full reasoning in `research.md`.
- **The closed set needs a registry document, not an inline enum.** The ratified
  text requires a "defined set" whose members state what they evidence and derive
  it from declarations. That is a registry with rules over it; inlining an enum in
  each schema would duplicate the set and leave the derivation unenforceable.
  Recorded in `research.md` as a settlement.
- **Operator escrow is a relationship on the credential record, not a custody
  tier** (ratified OQ2). The compatibility with the
  `client-credential-escrow-registry` topic's direction is recorded in
  `research.md`: escrow has one writer-moment and one reader-moment on the
  credential record every custody block already references, and neither of them
  changes what the certificate evidences at point of use.
- **The issuance-evidence floor is two levels and no weaker form is
  representable** (ratified OQ1). The strict level requires per-certificate
  provenance; the floor requires the policy attestation AND the authority's log
  and forbids the per-certificate fields by shape. The conformance declaration
  carries which form was achieved.
- **A certificate's key custody is optional and an anchor's is not.** The
  ratified scenarios differ deliberately: an anchor record names declared custody,
  and an undeclared certificate resolves to the floor. Both are enforced.
- **Contract registration follows the repository's release discipline.** Schemas
  are registered in `contracts/manifest.yaml` with per-file digests, a
  `contracts/CHANGELOG.md` entry, and a bundle version allocated at the next
  additive cut — change task 5.10, deliberately outside this feature.
