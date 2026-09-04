# Feature Specification: contracts/clearing — the neutral clearing-dispatch contract family

**Feature Branch**: `028-clearing-contracts`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Realize the neutral openxFactory contracts for the ratified change add-clearing-dispatch-boundary (PR #555, merged 2026-09-02) as the new contract family contracts/clearing/, registered at the next additive bundle cut."

## Context and authority

This feature is a REALIZATION, not a proposal. It authors no requirement of its
own and adds no spec delta. Its authority is two ratified OpenSpec changes:

- `add-clearing-dispatch-boundary` — RATIFIED 2026-09-01 by Brett Heap
  (record `openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md`),
  merged as PR **#555**, squash `ab0bb2dd`, 2026-09-02. Its `code_surface`
  paragraph DECLARES the neutral artifacts and defers them: *"The neutral
  openxFactory artifacts are DECLARED here and REALIZED POST-RATIFICATION at
  their own additive cut, because ratification authorizes realization and does
  not perform it."* Its `tasks.md` §6 is the artifact list this feature builds.
- `add-cpc-clearing-boundary` — RATIFIED 2026-09-02, merged `c0270d28`. Its
  MODIFIED requirements TIGHTEN two things this realization must honour:
  field (10) becomes a REQUIRED ORIGIN SIGNATURE where the originating
  repository holds an active row in the factory-identity register, and the
  policy-checked fields are RESOLVED FROM the permitted-operations register
  rather than read from the bundle. It also ADDS a workspace-disposal field to
  the dispatch record and names the tranche-3 `digest_subject` widening
  (its `tasks.md` §2.9) that the manifest digest needs.

The capability `clearing-dispatch-boundary` is NOT yet promoted under
`openspec/specs/` (the change is ratified but unarchived, its archive gate
being merged-plus-green realization evidence — which is what this feature
produces). The authoritative text is therefore the ratified delta
`openspec/changes/add-clearing-dispatch-boundary/specs/clearing-dispatch-boundary/spec.md`
as MODIFIED by `openspec/changes/add-cpc-clearing-boundary/specs/clearing-dispatch-boundary/spec.md`.

## User Scenarios & Testing *(mandatory)*

The "users" of a neutral contract family are: a PRODUCER factory authoring a
sealed bundle, a CLEARING implementation validating one, a REVIEWER asked to
approve an operation or a widening, and a CONSUMER pinning a contract bundle
version.

### User Story 1 - A clearing implementation can validate a sealed bundle manifest against a shipped contract (Priority: P1)

An implementer of the clearing workflow (in `opensoft/xFactory`, or any future
clearing repository) has a sealed-bundle manifest in hand and needs to decide,
mechanically, whether it may be dispatched. Today the ten declared fields exist
only as ratified prose; there is no schema to validate against, no register to
resolve the operation from, and no canonical validator to run. This story ships
all three, so that "the boundary refuses X" becomes a command that exits
non-zero and names X.

**Why this priority**: Every other artifact in the family is either an input to
this decision (the register) or an output of it (the ledger record, the
attestation). Without it the ratified boundary has no machine-checkable form at
all, and the ratified change cannot archive.

**Independent Test**: Run the canonical validator over the packaged positive
example — it exits 0. Run it over each packaged negative fixture — it exits
non-zero and names the refusal ground from the closed enumeration.

**Acceptance Scenarios**:

1. **Given** a manifest carrying all ten declared fields with a well-formed
   origin signature, **When** the canonical validator runs over it, **Then** it
   reports no finding and exits 0.
2. **Given** a manifest missing any one declared field, **When** the validator
   runs, **Then** it refuses and NAMES the missing field.
3. **Given** a manifest whose `expires_at` has passed relative to the declared
   evaluation instant, **When** the validator runs, **Then** it refuses with an
   expiry ground distinct from a transient failure.
4. **Given** a manifest naming an operation with no register entry, **When** the
   validator runs, **Then** it refuses with the unknown operation named and
   reports that no lane was selected.
5. **Given** a manifest whose declared worker profile, lane, or output schema
   disagrees with the register entry its operation id names, **When** the
   validator runs, **Then** it refuses and records the disagreement, and it does
   NOT silently substitute the register's value.
6. **Given** a manifest whose originating repository holds an ACTIVE origin row
   and whose field (10) carries only hosted-workflow provenance, **When** the
   validator runs, **Then** it refuses naming the MISSING ORIGIN SIGNATURE
   rather than reporting field (10) present.
7. **Given** a manifest whose originating repository holds NO origin row and
   whose field (10) carries hosted-workflow provenance, **When** the validator
   runs, **Then** field (10) is satisfied and the absence of a registered
   identity does not by itself refuse.

---

### User Story 2 - A reviewer can see that the permitted-operations register is closed and holds exactly one member (Priority: P1)

A reviewer asked whether some new host job is permitted must be able to read a
CLOSED register that today contains exactly one operation, `readiness-diagnostic`,
and to see that adding a second is a governed contract change rather than an
edit. The register ships as a SCHEMA plus a single INSTANCE, on the same
schema-plus-instance convention `trust-anchor`'s chain-custody registry uses
against `openxwallet-custody`.

**Why this priority**: The closed register is the CONTAINMENT the ratified text
names — explicitly in preference to the dispatch credential's scope. A register
that any lane author can extend would make the boundary decorative.

**Independent Test**: Add a second member to the shipped instance and run the
canonical validator — it refuses by name. Remove the addition — it passes.

**Acceptance Scenarios**:

1. **Given** the shipped register instance, **When** the validator runs, **Then**
   it validates and reports exactly one member, `readiness-diagnostic`.
2. **Given** an instance carrying any member not present in the ratified text,
   **When** the validator runs, **Then** it REFUSES, names the unratified member,
   and states that adding an operation is a governed contract change.
3. **Given** the `readiness-diagnostic` entry, **When** it is read, **Then** it
   declares its worker profile, its execution group and dispatch label(s), its
   class constraints (no checkout, no writes, no secret reference, no token
   scopes, a bounded timeout), its output schema reference, its data-handling
   classification, and `repository_affecting_output: false`.
4. **Given** an entry declaring `repository_affecting_output: false` together
   with a repository-affecting effect, **When** the validator runs, **Then** it
   refuses.

---

### User Story 3 - A dispatch and a refusal are both recordable in one shipped record shape (Priority: P2)

An implementation that clears a dispatch, and one that refuses a request, must
write the SAME kind of record — carrying resolved provenance beside claimed
values, the refusal ground drawn from a CLOSED enumeration, the declared-versus-
observed distinction in the field names, a reference to a signed execution chain
where one governs the work, and the workspace-disposal evidence `add-cpc-clearing-boundary`
made a field of this record.

**Why this priority**: The ledger is what makes the boundary auditable, but no
implementation writes one until the clearing lane's first operation dispatches;
P2 rather than P1 reflects that ordering, not lesser importance.

**Independent Test**: Validate a positive cleared-dispatch example and a positive
refusal example; then validate a negative fixture whose refusal ground is free
text and one whose disposal field is empty — both refuse.

**Acceptance Scenarios**:

1. **Given** a cleared dispatch, **When** its record is written, **Then** it
   carries the resolved originating repository and workflow, the resolved source
   commit, job id, operation, runner group, dispatch label, handling
   classification and outcome, plus any CLAIMED value that differed.
2. **Given** a refusal, **When** its record is written, **Then** its ground is a
   member of the closed refusal-ground enumeration and free text is refused.
3. **Given** a bundle-less dispatch, **When** its record is written, **Then**
   group, label and classification are typed as DECLARED and cannot be read as
   observed group membership.
4. **Given** a record whose workspace-disposal field is absent or empty, **When**
   it is validated, **Then** it is refused as an unattested disposal.

---

### User Story 4 - The single door can be attested, and the two divergence directions stay distinct (Priority: P2)

An attestation implementation reads each governed runner group's admitted
repositories and workflow allowlist from the provider and compares against an
expected set COMPUTED PER GROUP. The record it writes must be able to express
three outcomes that the ratified text refuses to conflate: a WIDENING (a breach),
a DARK LANE (an enumerated member with no allowlist entry — already failing
closed, a disposition item), and NOT-YET-CONVERGED (the clearing path not yet
admitted).

**Why this priority**: The ledger's completeness claim is conditioned on this
record, and the ratified text spends more words on keeping these three apart
than on any other distinction in the capability.

**Independent Test**: Validate a positive attestation carrying all three finding
classes; validate a negative fixture that files a dark lane as a widening — it
refuses.

**Acceptance Scenarios**:

1. **Given** an attestation record, **When** it is validated, **Then** each
   finding carries its group, the observed value, the expected set, and a finding
   class from a closed enumeration.
2. **Given** a finding that classes an enumerated member with no allowlist entry
   as a single-door breach, **When** it is validated, **Then** it is refused.
3. **Given** an attestation whose expected set is computed once for the estate
   rather than per group, **When** it is validated, **Then** it is refused.
4. **Given** an attestation that claims the FULL completeness strength while the
   clearing path is not yet admitted, **When** it is validated, **Then** it is
   refused.

---

### User Story 5 - A consumer can pin the family at a numbered bundle release (Priority: P3)

A consumer repository pins the contract bundle version it consumes. The new
family must therefore be registered in `contracts/manifest.yaml`, described in
`contracts/CHANGELOG.md`, and enumerated in a new
`contracts/releases/<version>.digests.yaml` inventory, at the next additive
minor allocated AT REALIZATION per `docs/contract-versioning-policy.md`.

**Why this priority**: Registration is the last step and depends on every
artifact above being final, but without it the family ships outside the release
surface and `release-surface-integrity` fails.

**Independent Test**: `python3 scripts/validate-contract-release.py` verifies the
new inventory at the realized commit; the release-surface tests pass.

**Acceptance Scenarios**:

1. **Given** the new family, **When** the manifest is read, **Then** every file
   of `contracts/clearing/` is registered.
2. **Given** the new inventory, **When** the release verifier runs, **Then** every
   registered member's digest matches its blob.

### Edge Cases

- **A second digest construction.** The manifest digest MUST use
  `xfc-jcs-sha256-1`. Because that construction's `digest_subject` enumeration is
  CLOSED and admits no manifest subject, this realization adds the manifest
  subject to THAT enumeration under the chain's own tranche rule, and defines no
  construction of its own. Inventing a second construction is the defect the
  chain's own header names.
- **Per-file hashes are not JSON values.** They are algorithm-tagged SHA-256 over
  the file BYTES. Applying the canonical-JSON construction to a byte stream is a
  category error and is refused.
- **An existing `dispatch-record.schema.yaml`.** `contracts/schemas/dispatch-record.schema.yaml`
  already exists and is a DIFFERENT record: the capability-steward junction
  decision. The clearing ledger is a distinct subject with a distinct owner, so
  it ships as `contracts/clearing/dispatch-record.schema.yaml` with its own
  `$id`; neither file is moved or renamed.
- **The register instance is a floor, not a ceiling.** codexFactory's
  `deliberation` operation (codexFactory #165) is a LATER governed change and is
  NOT added here; a validator refusal is what keeps it out.
- **An origin row that is expired or revoked.** The register view has a declared
  staleness bound; a view older than the bound, unreadable, or absent REFUSES
  rather than proceeding, and an unreachable store is diagnosed distinctly from
  an absent one.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The family MUST ship a SEALED-BUNDLE MANIFEST record schema under
  `contracts/clearing/` declaring EXACTLY the ten ratified fields, with the
  expiration required, the per-file hashes required alongside the file list, and
  the bundle digest expressed BY REFERENCE to the `signed-execution-chain` digest
  construction rather than redefined.
- **FR-002**: Field (10) MUST be modelled so that an ORIGIN SIGNATURE is REQUIRED
  when the originating repository holds an active registered origin identity, and
  trusted hosted-workflow provenance satisfies it only when no such identity is
  registered. A partial signature — one not covering all ten fields including the
  per-file hashes — MUST NOT validate as a signed manifest.
- **FR-003**: The `digest_subject` enumeration of
  `contracts/signed-execution-chain/digest-construction.schema.yaml` MUST gain
  the manifest subject as a TRANCHE ADDITION OF SUBJECTS, under that file's own
  stated rule, so the manifest digest has an admitted subject. No second
  construction is defined.
- **FR-004**: The family MUST ship the PERMITTED-OPERATIONS REGISTER as a SCHEMA
  plus a single closed INSTANCE, on the schema-plus-instance convention the
  `openxwallet-custody` composition uses.
- **FR-005**: The register instance MUST contain EXACTLY ONE member,
  `readiness-diagnostic`, declaring its worker profile, execution group and
  permitted dispatch lanes, its permitted-operation semantics (what it may and
  may not do), its class constraints, its output schema reference, its
  data-handling classification, and `repository_affecting_output: false`.
- **FR-006**: The canonical validator MUST REFUSE any register instance member not
  present in the ratified text, and the family's documentation MUST state that
  adding an operation is a governed contract change.
- **FR-007**: The family MUST ship an OPERATION REPORT schema for
  `readiness-diagnostic` describing the COMPOSED report of record — one report per
  dispatch across however many lanes were probed, per-lane facts as a keyed
  collection — with each lane's group and label typed as DECLARED values, and
  with NO eligibility verdict field.
- **FR-008**: The family MUST ship a DISPATCH LEDGER record schema covering
  cleared dispatches AND refusals, carrying resolved values beside claimed values,
  refusal grounds from a CLOSED NAMED enumeration seeded with exactly the two
  grounds the current realization emits (`unregistered_operation`,
  `unknown_lane_selector`), a reference to a signed execution chain where one
  governs the work, and the workspace-disposal evidence field.
- **FR-009**: The family MUST ship a SINGLE-DOOR ATTESTATION record schema
  carrying, per governed runner group, the expected and observed admitted
  repositories and allowlist entries, with the finding class carried from a closed
  enumeration that keeps WIDENING, DARK LANE and NOT-YET-CONVERGED distinct, and
  the completeness-claim strength stated.
- **FR-010**: The family MUST ship PACKAGED POSITIVE examples for every record
  shape and a NEGATIVE fixture per refusal the validator implements, under the
  repository's `examples/.../negative/` packaging convention.
- **FR-011**: The family MUST ship a canonical
  `scripts/validate-clearing-dispatch.py` implementing the cross-shape rules the
  schemas cannot express: ten-field completeness naming the missing field, expiry,
  classification, per-file-hash presence, unknown-operation refusal, register
  closure, bundle-versus-register disagreement, origin-signature presence, and
  origin-signature VERIFICATION against `governance/factory-identity/`.
- **FR-012**: The validator MUST REUSE existing implementations rather than
  re-deriving: the chain's digest code for `xfc-jcs-sha256-1`, and the pinned
  openXwallet key decoders for public-key decoding and signature verification. It
  MUST refuse rather than fall back when a dependency is absent.
- **FR-013**: The family MUST be registered in `contracts/manifest.yaml`, described
  in `contracts/CHANGELOG.md`, and enumerated in a new
  `contracts/releases/<minor>.digests.yaml`, at the next additive minor allocated
  AT REALIZATION by merge order at this branch's tip.
- **FR-014**: The canonical validator MUST be wired into CI in the same pattern as
  the existing `wallet-validation` and `signed-execution-chain-gate` jobs.
- **FR-015**: The family MUST ship pytest tests covering: schema positive and
  negative cases, register-closure refusal, each validator refusal BY NAME,
  digest-by-reference (no second construction), and origin-signature verification
  with an obviously-fake fixture key that does not trip secret scanning.

### Key Entities

- **Sealed bundle manifest**: the ten-field short-lived request object. Not a
  committed folder of copied data.
- **Permitted-operations register**: the closed set of operations a governed host
  may be asked to perform; entry #1 is `readiness-diagnostic`.
- **Operation report**: the composed structured evidence `readiness-diagnostic`
  emits. Evidence, never a readiness decision.
- **Dispatch record (clearing ledger)**: one record per cleared dispatch and per
  refusal, resolved beside claimed, ground from a closed enumeration.
- **Single-door attestation**: the periodic per-group comparison that keeps the
  ledger's completeness claim honest.
- **Origin identity**: the row in `governance/factory-identity/register.yaml` whose
  public key verifies field (10).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every artifact named in `add-clearing-dispatch-boundary`'s
  `code_surface` paragraph for openxFactory exists in the tree, or is recorded as
  already-realized with the file that realizes it named.
- **SC-002**: Each refusal the canonical validator implements has a NAMED code, a
  negative fixture that triggers it, and a test asserting the code by name — a
  refusal with no fixture and no test does not count as implemented.
- **SC-003**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes, and
  `python3 scripts/proposal-support.py . verify` passes.
- **SC-004**: `python3 -m pytest tests/ -q -m "not postgres"` passes with no new
  failure attributable to this feature.
- **SC-005**: The doc-health families prior work uses (proposal-origin,
  status-validity, location-conformance, modified-block-currency,
  promotion-fidelity, standard-backing, document-catalog) report no new finding.
- **SC-006**: A reviewer can determine, from the tree alone, that the register
  holds one member and that adding a second is refused mechanically.

## Out of Scope

Named here because the ratified `code_surface` names them as NOT this surface:

- `realize-factory-bundle-packaging` — the codexFactory hosted packaging workflow
  that produces a conformant sealed bundle, and the CODING operation's register
  entry.
- The HOSTED FINALIZER for patch-returning operations (gated on the above:
  `readiness-diagnostic` returns nothing a finalizer would validate).
- Any runner, runner group, dispatch label, host, or credential provisioning.
- The `deliberation` register member (codexFactory #165) — a LATER governed
  change.
- Any change to `opensoft/xFactory` workflows, the grandfather enumeration, the
  L4 authoring-time guard, or the L5 attestation IMPLEMENTATION. This feature
  ships the attestation RECORD SHAPE only.
- Any spec delta. This is a realization; it authors no requirement.

## Assumptions

- The next additive minor is allocated at THIS branch's tip by reading
  `contracts/manifest.yaml:contract_bundle_version`. If another cut lands first,
  the number is re-derived before merge rather than reserved now.
- The `sealed return` digest subject named in `add-cpc-clearing-boundary`
  `tasks.md` §2.9 is NOT added here: no artifact in this realization computes a
  digest over a sealed return, and adding an enum member with no consumer would be
  a widening no shipped shape exercises. It lands with the finalizer/packaging
  successor that first produces one.
- `governance/factory-identity/register.yaml` is live on `main` with a minted
  codexFactory origin key, so origin-signature verification is testable against a
  real register shape using a fixture key of the test's own.
- The clearing REPOSITORY is `opensoft/xFactory`, but the neutral contracts name
  no repository: they carry the clearing repository as data.
