# Feature Specification: The Register and Its Reader (S4)

**Feature Branch**: `014-register-and-reader`

**Created**: 2026-08-25

**Status**: Draft

**Input**: Tasks §5.1–5.3 and §5.5 of the ratified OpenSpec change
`add-wallet-carried-review-authority`: the register and its reader, in ONE
change.

**Governance source**: Implements the ratified requirement *"The register and
the reader are ratified together"* — MVP shape normative: one file at a fixed
path in openxFactory, one holder (codexFactory's `merge_readiness_council` as
a body), one target repository, one review act, `authority_tier: act`, one
`expires_at` — plus *"A grant with no reader in a required check confers
nothing"*. Format ruled by design D11: NO contract schema; the register is
kindless YAML whose shape THIS reader enforces ("a register with a reader IS
a shape"). Operator rulings 2026-08-25: S4 includes issuing the FIRST root
review-authority grant (without it the row is "documentation that confers
nothing"); target repository `opensoft/openxFactory`; `expires_at` ~90 days.
Task §5.4 (floor entry by name) is codexFactory-side and travels as this
register's standing pointer, not performed here.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A register with no active backing fails admission (Priority: P1)

The reader's single ratified obligation: fail a convening that admits a
holder carrying no active row. In CI terms: any active REVIEW-class grant in
the scanned tree without a backing active register row fails the required
check, and an empty or malformed register does NOT silently skip that sweep.

**Why this priority**: This is the capability's own ratification condition -
a register alone realizes nothing.

**Independent Test**: Mutation probe (run once, restored): rename
`register.yaml` away → sweep errors `register-no-active-row` naming the
grant; restore → green. Pinned permanently by self-test probes.

**Acceptance Scenarios**:

1. **Given** the checkout, **When** the required wallet-validation sweep runs,
   **Then** it exits 0 with the live grant+wallet validated AND the register
   reader reporting clean.
2. **Given** the register renamed away, **When** the sweep runs, **Then** it
   FAILS with `register-no-active-row`.
3. **Given** `rows: []`, **When** the sweep runs, **Then** it still evaluates
   the headline obligation (no silent early return).

### User Story 2 - Expiry is COMPUTED, never trusted from state (Priority: P2)

Per clarifications N8: nothing recomputes `state`; the reader computes expiry
from `expires_at` at read time. A past `expires_at` refuses the row as
expired regardless of its stored `state: active`, and flags the stale stored
state as its own finding on the grant.

**Why this priority**: An expired authority honored off a stale flag is the
vacuous-pass class in time form.

**Independent Test**: Self-test probe with `expires_at` in the past expects
`register-row-expired` + `grant-state-stale` + `register-no-active-row`.

### User Story 3 - The act tier stands only on a parseable attestation (Priority: P3)

The row claims `authority_tier: act`, which the ratified unattested-custody
rule caps at `request` absent attestation. The reader parses the kindless
attestation rows (013's recorded obligation): subject resolution, closed-set
model, verifier fields, honest isolation posture. Missing OR malformed ⇒ loud
refusal (`register-tier-act-unattested` / `attestation-malformed`) - never a
silent degrade to the cap.

**Independent Test**: Self-test probe without the attestation file expects
`register-tier-act-unattested`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `governance/review-authority/register.yaml` exists at the fixed
  path, `register_version: 1`, exactly ONE row matching the MVP shape
  (holder `agent:merge-readiness-council`, wallet `wal-agent-mrc-0001`,
  target `opensoft/openxFactory`, act `review`, tier `act`, grant_ref
  `grant-mrc-0001`).
- **FR-002**: The register carries, IN ITS OWN DOCUMENTATION: the Q1c
  constraint verbatim-in-substance (file cannot satisfy
  revocation-at-exercise; revocation surface home = live Hermes lookup, S5)
  and the explicit permanently-human-only declaration with by-name floor
  entry noted.
- **FR-003**: The FIRST root review-authority grant
  (`governance/review-authority/grants/grant-mrc-0001.yaml`): audience
  `wal-agent-mrc-0001`, acts `[review]`, objects `[opensoft/openxFactory]`,
  tier `act`, approval posture requiring approval-before-apply,
  `issued_by: Brett.Heap@opensoft.one` (the anchored operator - first
  positive exercise of OXWR-R2), expires ~90 days, state active.
- **FR-004**: The validator gains a register reader inside the EXISTING
  required check: strict row shape (this reader IS the shape per D11),
  wallet/grant resolution + reconciliation, computed-expiry semantics (N8),
  act-tier attestation coupling, minimal-shape bound, and the inverse
  headline obligation (active REVIEW-class grant ⇒ active backing row).
- **FR-005**: Absent register + no review-class grants remains clean (every
  consumer repo that has not cold-started the arc stays conformant); absent
  register WITH such grants refuses.
- **FR-006**: No contract bytes move: no schema edit, no manifest entry, no
  CHANGELOG line, no bundle cut (D11); the register and grant are INSTANCES.

### Success Criteria

- **SC-001**: Whole-checkout `--strict` sweep exits 0; repo-scan reports the
  grown live-artifact count (wallet + grant).
- **SC-002**: Packaged corpus unchanged: 17 positives / 36 negatives across
  13/13 requirements.
- **SC-003**: All register refusal codes pinned by self-test probes
  (clean / computed-expiry / no-active-row / unattested / minimal-shape /
  malformed-row / absent-register postures) - the synthesized trees ARE the
  negative coverage, since a kindless register cannot be a corpus fixture.
- **SC-004**: Live mutation probe proves the production wiring fires
  `register-no-active-row` when the register vanishes (run once, restored).
- **SC-005**: Boundary proofs: contracts/.github diff vs branch base empty;
  zero private material anywhere in the diff.

## Scope boundaries (recorded, not performed)

Floor entry BY NAME in codexFactory gate rules (§5.4); revocation surface +
staleness bound declaration (S5); exercise records (S3); composition mapping
(task 4.4, codexFactory); register CONTRACT SCHEMA (D11 successor);
multi-holder/multi-target registers (named successors). Grant-side
unattested-cap enforcement inside check_grant stays successor work - the cap
binds at the register reader where admission happens.
