# Feature Specification: Council Review for Feature PRs (Lane Intake)

**Feature Branch**: `011-council-feature-clearance`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "Intake act extending the substantive-review lane: council review covers feature PRs on governed repos via merge-approval-envelope candidate classes."

**Governance source**: Implements the intake-act obligation ratified in
`add-substantive-review-lane` / `roles-authority-model` ("extending the lane is an
intake act rather than a restructuring act") and the universal-jurisdiction scenario
("a pull request's diff is software regardless of the domain"). Today exactly ONE
governed candidate exists anywhere (`doc-health/nightly`, bot-authored, `health/**`);
no feature PR — human or agent authored — has ever been a council subject. This
feature makes feature PRs lane subjects without weakening any existing control.

## Clarifications

### Session 2026-08-23

- Q: Which repositories form the first tranche, and are feature-PR verdicts advisory or clearable? → A: BOTH `opensoft/xFactory` AND `opensoft/openxFactory` enter the first tranche (openxFactory is the ratified pilot home of the lane and where real feature PRs occur; xFactory-only would be a rehearsed-but-dormant intake act). Verdicts are ADVISORY-only for every first-tranche class — no feature PR has ever been a council subject, so no evidence base exists for any clearable class, and flipping classification intent IS the tier-2 activation gate-flip reserved to the convener. Floor classes untouched under either ruling.
- Q: The envelope schema v1 supports only EXACT-string `expected_head_ref` (no ref patterns; `additionalProperties: false`; no classification-intent field) — how is an open-ended feature-PR class expressed? → A: Intake-per-effort, literally. Each feature effort records ONE reviewed exact-ref envelope entry when its branch opens; auto-commissioning engages immediately for that candidate; revocation deletes one entry. No schema change (codexFactory-minor explicitly rejected as premature cross-repo chain; relaxing ref binding refused outright as spoofing surface against Principle VII). If pilot evidence shows per-effort friction is real, promoting `head_ref_pattern` becomes its own evidence-backed successor change — noted in tasks, not built here.

### Correction 2026-08-25 — Q2's first ground evaporated; the answer stands on its second

The answer above is NOT rewritten: it is the record of what was decided on
2026-08-23 and on what basis. This note records that one of its two grounds was
false at the time it was written, and that the convener has reaffirmed the answer
on the remaining ground.

WHAT WAS FALSE. Q2's premise — "the envelope schema v1 supports only EXACT-string
`expected_head_ref` (no ref patterns)" — was already untrue when the question was
asked. `head_ref_pattern` is part of schema **v1 itself** (`schema_version` is
`{"const": 1}`; the member is a `oneOf` alternative to `expected_head_ref`), with
glob matching in **codexFactory's** `scripts/merge_master/envelope.py` — that tree
exists in `opensoft/codexFactory`, not in this repository. It shipped in codexFactory
`9ebe805` on **2026-08-21**, two days before this clarify, and codexFactory runs a
pattern class in production today (`head_ref_pattern: change/**`). So the ground
"no schema change (codexFactory-minor explicitly rejected as premature cross-repo
chain)" describes a cost that does not exist: expressing an open-ended class needs
no schema work at all. The other two premises HOLD — `additionalProperties: false`
is real, and there is still no classification-intent field anywhere.

WHAT STANDS, AND WHY. **Brett reaffirmed intake-per-effort on 2026-08-25**, on the
answer's second ground alone: relaxing ref binding is a spoofing surface, refused
against Principle VII. That is a security judgment about what SHOULD be bound, not
a claim about what the schema CAN express, so the false premise does not disturb
it. First-tranche classes therefore remain one reviewed exact-ref entry per effort
— now a deliberate refusal of an available mechanism rather than an accommodation
of a missing one.

The successor clause is likewise unchanged in effect but not in meaning: promoting
`head_ref_pattern` would no longer be a schema change, so any future proposal to
use it is purely a request to revisit the Principle VII judgment on recorded pilot
evidence, and must be argued on that footing.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A feature PR gets a recorded council verdict (Priority: P1)

A contributor opens a feature pull request matching the newly declared candidate
class. The approval workflow evaluates it, reaches `awaiting_verdict`, and the
convening lane automatically commissions a merge-readiness council on the Hermes
runtime; once resolved, the recorded verdict lands as the SHA-bound
`council-verdict/merge-readiness` check-run on the PR — the first live convening
against a non-nightly candidate.

**Why this priority**: This is the intake act's entire purpose — converting the
lane from single-candidate rehearsal posture to covering real feature work.

**Independent Test**: Open one qualifying PR; observe commission, deliberation,
and emitted verdict check-run bound to the lane App identity.

**Acceptance Scenarios**:

1. **Given** a PR matching the declared candidate class, **When** the approval
   workflow completes its evaluation, **Then** the convening lane commissions
   without manual dispatch.
2. **Given** the commissioned convening resolves, **When** the emit half runs,
   **Then** the verdict check-run appears on the head SHA with `.app.id` equal to
   `vars.COUNCIL_LANE_APP_ID`.

---

### User Story 2 - Floor classes are refused, loudly and correctly (Priority: P2)

Any PR whose changed paths fall inside assembly-class surfaces (workflows, gates,
credentials, registers) is classified by the preflight as never-clearable and
REFUSED before any runtime commissioning — with the named refusal outcome. The
refusal proves the widened lane still honors the constitutional floor.

**Why this priority**: Widening coverage must demonstrably widen nothing the floor
protects; the refusal IS the compliance evidence.

**Independent Test**: Dispatch the lane against a PR touching `.github/workflows/**`;
observe named refusal (`parked_never_clearable` class), no commission created.

**Acceptance Scenarios**:

1. **Given** a floor-touching PR, **When** the lane classifies it, **Then** it
   refuses with the named tier-2 outcome and creates no runtime job.
2. **Given** the same PR, **When** re-dispatched, **Then** the refusal repeats
   idempotently (no duplicate guard ambiguity).

---

### User Story 3 - Coverage extends beyond a single repository (Priority: P3)

At least one additional governed repository's feature PRs become lane subjects:
the lane resolves candidates across repos, and the transport can emit onto their
head SHAs (App installation extended accordingly — an operator act where GitHub
requires it).

**Why this priority**: Doctrine says every governed repo; first-tranche pragmatism
starts narrow, but the spec binds the direction so the widening cannot quietly stop
at one repo.

**Independent Test**: A qualifying PR in the second covered repo traverses the same
commission→emit loop end-to-end.

**Acceptance Scenarios**:

1. **Given** the lane target resolution generalized past its current hardwired
   repository, **When** a qualifying PR opens in the additional repo, **Then** the
   same commission→emit loop applies unchanged.
2. **Given** the operator has extended the lane App installation, **When** a verdict
   is emitted onto that repo's head SHA, **Then** identity binding holds
   (`.app.id` match) identically.

---

### Edge Cases

- What happens when a candidate PR is merged/closed between evaluation and
  commissioning? The preflight/classification refuses with the named stale-target
  outcome; nothing is commissioned against dead SHAs.
- What happens when two qualifying PRs await simultaneously? Each is an independent
  candidate; the lane's convene-at-most-once guard applies per head SHA.
- What happens when the runtime is unreachable at commission time? Fail-closed job
  creation error surfaces in the lane run; no silent skip.
- What about PRs authored BY the lane/content Apps themselves? Author-expectation
  fields in each candidate entry decide admissibility; self-authored clearance is
  structurally prevented by the three-identity separation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: New candidate classes MUST be declared in the reviewed
  merge-approval-envelope rules-as-code, read from base branch only; no runtime or
  workflow-code change may carry the widening on its own.
- **FR-002**: Feature-PR candidates MUST classify through the existing tier-1/tier-2
  fact pipeline unchanged; this feature adds NO new fact sources and NO new
  classification logic.
- **FR-003**: Commissioning MUST engage automatically (workflow_run signal) for
  qualifying candidates; operator dispatch remains available but is never required.
- **FR-004**: Assembly-class PRs MUST be refused pre-commissioning with the named
  never-clearable outcome, idempotently.
- **FR-005**: Emitted verdicts MUST bind to the lane App identity exactly as the
  nightly candidate's do (anti-spoofing predicate unchanged).
- **FR-006**: Coverage is per-effort and explicit: each feature effort's envelope
  entry (exact head ref, named author expectation, path scope) IS the intake act.
  Extending to further repositories or classes is a follow-up intake act, never a
  silent default; ref-pattern generalization is explicitly OUT of scope (named
  successor if pilot evidence justifies it).
- **FR-007**: Documentation MUST state which repos/classes are covered after this
  feature, and that floor classes remain permanently human-only.
- **FR-008**: The lane App installation required for emission onto additional
  repositories is an OPERATOR act (GitHub UI); this feature declares it as a named
  prerequisite step, never performs it in CI.

## Key Entities *(include if feature involves data)*

- **Candidate class**: an envelope entry — target repo(s), expected author(s),
  ref pattern, changed-path scope, classification intent (advisory vs clearable).
- **Verdict check-run**: the existing SHA-bound evidence artifact; unchanged shape.
- **Refusal record**: named preflight outcomes for non-clearable classifications.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The first qualifying feature PR traverses commission→deliberation→emit
  end-to-end with an identity-bound verdict check-run (rehearsed during implementation
  on a scratch PR, then observed on a real one).
- **SC-002**: Zero floor-class commissions occur after widening — verified by the
  named-refusal rehearsal plus absence of runtime jobs for refused targets.
- **SC-003**: Existing nightly-candidate behavior is byte-identical before/after
  (regression proof by identical classification output on a fixture).

## Assumptions

- ~~First-tranche scope starts with feature PRs on `opensoft/xFactory` itself~~
  RESOLVED (Q1): first tranche = `opensoft/xFactory` + `opensoft/openxFactory`.
- ~~First-tranche verdicts are ADVISORY evidence~~ CONFIRMED by ruling (Q1):
  advisory-only for every first-tranche class; classification intent cannot live in
  the envelope (schema fact) and clearable-now would invert evidence-before-autonomy.
- The merge-approval-envelope schema already expresses the needed candidate shapes
  (multi-repo `target_repos` lists exist); if clarify finds a schema gap, that is
  escalated rather than patched locally.
- Human-authored PRs raise the author≠approver question: under intake-per-effort
  (Q2), expected-author is decided per entry at effort-open, alongside whichever
  authorship route (direct push vs session-open-pr bot route) the effort uses.
  Per-entry decision, not a global assumption.
