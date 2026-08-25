# Feature Specification: The First Wallet (wallet arc cold start)

**Feature Branch**: `013-first-wallet`

**Created**: 2026-08-24

**Status**: Draft

**Input**: Tasks §4.1–4.3 of the ratified OpenSpec change
`add-wallet-carried-review-authority`: the first wallet.

**Governance source**: Implements §4 of
[add-wallet-carried-review-authority](../../openspec/changes/add-wallet-carried-review-authority/proposal.md)
— "Cold start. One holder, not eight." — the day-one order step between S2
(landed, PR #299) and S4 (the register and its reader). Task 4.1 carries an
`[OPERATOR]` tag; its operator decisions were ruled by Brett Heap in-session
2026-08-24 and are recorded in
[implementation-notes.md](./implementation-notes.md). This step issues NO
grant, builds NO register, and moves NO contract bytes — those are S4.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A live wallet record exists for the council body (Priority: P1)

codexFactory's `merge_readiness_council`, as a body, becomes the first wallet
holder in the stack: one `xfactory_wallet_record` instance in openxFactory,
custody `holder_readable`, state `active`. Zero wallet instances exist outside
the packaged teaching corpus today; this is the deliberate, narrow exception
that starts the register's world.

**Why this priority**: Nothing downstream — grants, register rows, exercises,
revocation — can exist before a wallet does.

**Independent Test**: `repo_scan` over the checkout validates the new record
green (the repo-scan artifact count grows by exactly one) while the packaged
corpus counts stay exactly at their S2 baseline.

**Acceptance Scenarios**:

1. **Given** the checkout, **When** `scripts/validate-openxwallet.py <checkout>
   --strict` runs, **Then** it exits 0 and reports the live record validated.
2. **Given** the record, **When** schema validation runs, **Then** every field
   conforms: closed-set custody member, closed-set holder class, key REFERENCE
   with no key material anywhere.
3. **Given** the packaged corpus sweep, **When** it runs, **Then** counts are
   unchanged from S2 evidence (17 positives / 36 negatives across 13/13
   requirements) — this change touches no corpus fixture.

---

### User Story 2 - The custody attestation row records who verified, against what, when (Priority: P2)

The ratified unattested-custody rule caps review-authority grants at `request`
when no attestation exists. The row that prevents the cap lands beside the
wallet: verifier identity and standing, verification basis, time, the
compensating control, and the cap it avoids. It is deliberately KINDLESS — no
contract schema for custody attestation exists in the family, §4 authorizes
none, and inventing one would be an unauthorized contract release.

**Why this priority**: Without the row, any future grant to this wallet caps
below the MVP tier S4 will target (`act`) — the cold start would be born
already throttled.

**Independent Test**: Manual inspection confirms the row names the wallet ref and states
`isolation_claimed: none` honestly for `holder_readable`, and names the
approval-before-apply compensating control. No validator logic reads the row
today (kindless files are skipped by repo_scan); machine enforcement is S4
successor work.

**Acceptance Scenarios**:

1. **Given** the attestation row, **When** read, **Then** it names the wallet
   by ref, the custody model attested, the verifier (name, role, standing),
   the basis, and the date.
2. **Given** the family's schemas, **When** checked, **Then** no new schema,
   manifest entry, CHANGELOG line, or bundle was created for the row.

---

### User Story 3 - Residency obeys N7: same tree as the future register (Priority: P3)

`repo_scan` builds its context from the scanned repository's own records; a
cross-repository audience wallet has no resolution path today. Both artifacts
live under `governance/review-authority/` in openxFactory — outside every
packaged `examples/` corpus so the scanner treats them as live records — where
S4's register will join them in the same directory.

**Why this priority**: Placement is what makes the wallet RESOLVE instead of
silently validating nothing; wrong placement would reproduce the vacuous-pass
class this change exists to prevent.

**Independent Test**: The two files sit outside any `examples/` path and
inside the scanned tree; a targeted scan names both.

**Acceptance Scenarios**:

1. **Given** the file paths, **When** inspected, **Then** neither carries an
   `examples` path segment and both sit under `governance/review-authority/`.
2. **Given** a whole-checkout sweep, **When** run, **Then** the live record is
   discovered, indexed, and cross-validated in-tree (not skipped as packaged
   corpus).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: One `xfactory_wallet_record` instance exists for holder
  `agent:merge-readiness-council` (class `agent`, body of the codexFactory
  merge readiness council), custody model `holder_readable` from the canonical
  registry, state `active`.
- **FR-002**: Its `key_reference` carries an OPERATOR-MINTED public identity
  only — `did:key:<multibase>` plus optional `public_key_multibase` — with no
  private material anywhere in the diff; the private half never enters any
  governed repository or agent session.
- **FR-003**: A custody attestation row exists recording `verified_by`
  (name, role, standing), `verified_at`, `verified_against` (method, basis,
  `isolation_claimed: none`), the compensating control, and the cap its
  absence would trigger.
- **FR-004**: Both artifacts live under `governance/review-authority/`
  (wallets/, attestations/) in openxFactory — the same tree S4's register will
  occupy, outside every packaged `examples/` corpus.
- **FR-005**: NO grant is issued, NO register or reader is built, NO schema
  bytes / manifest entry / CHANGELOG line / bundle version move (§4 boundary;
  composition declaration stays task 4.4, codexFactory-side).
- **FR-006**: A whole-checkout validator run exits 0 with the live record
  counted among scanned artifacts, and the packaged-corpus self-test remains
  green at S2 baseline counts.

### Success Criteria

- **SC-001**: `python3 scripts/validate-openxwallet.py . --strict` exits 0 and
  the repo-scan note reports the live artifact(s) validated.
- **SC-002**: Packaged corpus counts unchanged from S2: 17 positives / 36
  negatives across 13/13 requirements, exit 0.
- **SC-003**: Diff inspection proves zero private key material and zero
  contract-file modifications (`contracts/**` untouched except nothing).

## Scope boundaries (recorded, not performed)

Composition declaration for the agent-class holder (task 4.4), the first
review-authority grant, the register + reader (S4), exercise records (S3),
revocation reconciliation (S5).
