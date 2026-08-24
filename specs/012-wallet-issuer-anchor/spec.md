# Feature Specification: Wallet Issuer Anchor (S2)

**Feature Branch**: `012-wallet-issuer-anchor`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "S2 of the ratified OpenSpec change add-wallet-carried-review-authority (@ main): the issuer anchor."

**Governance source**: Implements ratified requirement *"Every review-authority grant
names its issuer, and a root grant's issuer is anchored outside the register"*
(`openspec/changes/add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:84-106`)
and substrate item **S2** of that change. Per its tasks §3.1: **no `contracts/` edit,
no manifest entry, no CHANGELOG line, no bundle cut** — this is a composing-capability
restriction enforced by the validator, never a schema change.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A review-authority grant without an issuer is refused (Priority: P1)

A grant whose `scope.acts` names the review act is issued with no `issued_by`. The
validator rejects it with the named failure code. Today the field is read by zero
rules — this scenario proves the first real enforcement of the issuer anchor.

**Why this priority**: The issuer anchor is the root of the entire authority chain;
without it, monotonic attenuation below an unbounded root is meaningless.

**Independent Test**: Negative specimen `grant-review-authority-omits-issued-by.yaml`
fails validation with `expected_failure: issuer-unrecorded`.

**Acceptance Scenarios**:

1. **Given** a review-class grant lacking `issued_by`, **When** validation runs,
   **Then** it FAILS with code `issuer-unrecorded`.
2. **Given** the packaged corpus, **When** the validator runs, **Then** the new
   negative fails for exactly its declared reason and the coverage-closure invariant
   holds (every claimed REQ-ID exists).

---

### User Story 2 - Root grants answer to the operator anchor alone (Priority: P2)

A ROOT grant (no `parent_grant_ref`) naming anything other than the recorded
responsible operator is refused — whether the value is a machine/broker token or the
legacy org-level string `opensoft` that every existing example happens to carry.
Legacy values do not grandfather into the anchor.

**Why this priority**: Root bounds the whole attenuation tree; an unanchored or
machine-named root makes every downstream property strictly local fiction.

**Independent Test**: Two negative specimens fail with `root-issuer-unanchored`
(detail-pinned separately: machine token vs `opensoft`), while an anchored root
naming `Brett Heap` validates clean.

**Acceptance Scenarios**:

1. **Given** a root review-class grant with `issued_by: sub-8f2c41d60a974d3b`,
   **When** validation runs, **Then** it FAILS `root-issuer-unanchored` with the
   machine-token detail pin.
2. **Given** a root review-class grant with `issued_by: opensoft`, **When**
   validation runs, **Then** it FAILS `root-issuer-unanchored` with the
   legacy-value detail pin.
3. **Given** a root review-class grant with `issued_by: Brett Heap`, **When**
   validation runs, **Then** it PASSES.

---

### User Story 3 - Non-review grants stay untouched (Priority: P3)

The class condition does not over-trigger: a transaction-act grant with NO
`issued_by` continues to validate cleanly, exactly as all five packaged grant
positives do today. The widening costs other domains nothing.

**Why this priority**: Proves the composing-capability restriction is scoped, per the
ratified "no other consumer disturbed" clause.

**Independent Test**: Boundary-guard assertion in the self-test: post_transaction
grant without `issued_by` passes.

**Acceptance Scenarios**:

1. **Given** the packaged corpus unchanged, **When** the full two-layer sweep runs,
   **Then** exit 0 with zero new findings versus pre-S2 behavior.

---

### Edge Cases

- A review-class grant WITH `parent_grant_ref` and no `issued_by`: child grants
  inherit issuer context from their parent chain — requiredness applies to the class,
  but the root check only fires on roots; child behavior follows attenuation rules
  (surfaced at clarify if the ratified text demands more).
- An `issued_by` value with whitespace/case drift (` brett heap`) — exact match
  against the anchored token, fail-closed; no normalization (identity strings do not
  get fuzzy).
- The canonical review act token appearing inside a NON-review grant's acts list:
  presence triggers class membership by design; authors of unrelated grants must not
  borrow the token.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The validator MUST define ONE canonical review-act token — `review` —
  as a named module constant beside the custody-registry path reference, cited to
  `review-authority-intake` requirement 1.
- **FR-002**: A grant is REVIEW-CLASS when and only when its parsed `scope.acts`
  contains that token. Class detection reads scope content; nothing else triggers it.
- **FR-003**: A REVIEW-CLASS grant with no `issued_by` MUST FAIL with code
  `issuer-unrecorded` (scenario: "A grant omits its issuer").
- **FR-004**: A ROOT review-class grant (no `parent_grant_ref`) whose `issued_by`
  is not exactly `Brett Heap` MUST FAIL with code `root-issuer-unanchored`; the
  message distinguishes machine-token values from other unanchored values (detail
  pin support). The accepted operator constant cites `docs/roles-and-authority.md:103-140`
  (Human Escalation Contract) as its authority — the code points at the standing
  record rather than duplicating it.
- **FR-005**: Three negative specimens MUST join the packaged corpus under
  `contracts/openxwallet/examples/negative/`, each declaring `expected_failure`,
  detail pin where applicable, and `requirement:` attribution against the new
  REQ-IDs: `grant-review-authority-omits-issued-by.yaml`,
  `grant-review-root-issuer-is-a-machine.yaml`,
  `grant-review-root-issuer-says-opensoft.yaml`.
- **FR-006**: The validator's REQUIREMENTS map MUST register the new REQ-IDs so the
  coverage-closure invariant stays satisfied in both directions.
- **FR-007**: The five existing packaged grant positives (transaction-act class)
  MUST continue to pass unchanged; no schema file, manifest, CHANGELOG line, or
  bundle version is touched.
- **FR-008**: A self-test assertion MUST prove the boundary guard: a
  post_transaction-style grant with no `issued_by` passes (US3 regression guard).

## Key Entities *(include if feature involves data)*

- **Review-class grant**: `kind: xfactory_wallet_grant` whose `scope.acts` contains
  the canonical `review` token.
- **Root grant**: review-class grant with no `parent_grant_ref`.
- **Operator anchor token**: the literal string `Brett Heap` — the only accepted
  root-issuer value, backed by the Human Escalation Contract citation.
- **Negative specimens**: three packaged fixtures with declared expected failures
  feeding the layer-1 corpus assertion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All three new negatives fail for exactly their declared reasons
  (rehearsed in CI self-test, evidenced in implementation notes).
- **SC-002**: Full sweep exits 0 on the tree — 17→20 positives-equivalent coverage,
  33→36 negative confirmations, 11/11→13/13 requirements coverage (counts asserted
  at implementation; recorded as evidence).
- **SC-003**: Zero behavior change for non-review grants (boundary guard green).

## Assumptions

- Canonical review act token is `review` (named once here per the architect's
  obligation); confirmed by architect mini-consult before implementation.
- Operator token `Brett Heap` ruled by convener 2026-08-23 (exact match, no
  normalization).
- Child-grant issuer inheritance beyond root checks remains governed by existing
  attenuation logic; S2 adds no child-specific rule unless clarify surfaces a
  ratified gap.
