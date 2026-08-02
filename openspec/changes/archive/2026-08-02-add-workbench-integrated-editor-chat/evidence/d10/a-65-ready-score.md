# Step A — READY_MIN_SCORE (0.60) calibration observations

Status: record (in progress — accumulating during the 2026-07-31 session)
Serve: http://127.0.0.1:46129 · corpus d09d582 · snapshot VALIDATED

## Observation 1 — dashboard-repo-selector (correct-refusal cell)

- Displayed readiness score: **0.4** (below the 0.60 bar).
- Brett's verdict, live: "This is accurate based off my analysis. It means
  this should not have moved forward to proposal. There are too many open
  questions to be a proposal."
- Specimen classification note: the fragment Brett actually took to
  proposal (exit 1, `add-dashboard-repo-selector`, 2026-07-26) was promoted
  OUT of staging per the partial-promotion lifecycle; today's tile scores
  the RETAINED REMAINDER (exit 2, the runtime-plane capability), which is
  genuinely open-questions-heavy. The bar reading it as unready — and Brett
  agreeing — is a correct-refusal calibration point, not a should-pass
  failure. A gate refusal here would be one Brett agrees with.

## Observation 2 — workbench-branch-sessions (should-pass cell: CALIBRATION MISS)

- Displayed readiness score: **0.5** (below the 0.60 bar).
- Brett's verdict, live: "the score shown is 0.5. I think this is actually
  too low. The open questions are not blockers and only mid level. So
  probably 0.6 is more appropriate for this doc."
- Classification: this fragment WAS taken to proposal (`add-workbench-branch-sessions`,
  ratified 2026-07-26 with zero parked decisions) and Brett judges the
  retained doc proposal-worthy — yet the scorer places it at 0.5, so the
  0.60 gate WOULD refuse it. This is a top-side calibration miss: the
  threshold is judged right, the SCORER undervalues this document.
- Improvement direction (Brett, live): better analysis; a runbook for each
  staged packet; each packet's overview should include every issue RANKED
  with what-to-do-to-overcome-it. Carried to the session findings file.

## Observation 3 — consent-instrument-contract (accurate low score; P5 consequence)

- Displayed readiness score: **0.458** (below the 0.60 bar; snapshot health
  lists 2 blockers).
- Brett's verdict, live: "I think this is accurate. The open questions are
  core to the feat. So we should not proceed until those are addressed.
  There are also other non-listed open questions that probably also need to
  be addressed... for now it is pretty good analysis and accurate rating
  at .458."
- Consequence: the P5 Step E plan (propose commission from this topic) is
  HONESTLY BLOCKED today — the gate would refuse and Brett agrees the
  refusal is right. Recorded per the no-laundering rule; Step E disposition
  decided in the session plan below.
- Analysis-depth note (Brett): the scorer misses open questions that are
  not explicitly listed — strengthening doc analysis is V2 material
  (session-findings F2/F3).

## Observation 3a — full-roster sweep (from the served snapshot)

- 21 staged topics: 19 `developing` (1-5 blockers each); only
  `github-administration-plane` and `proposal-origin-contract` are `ready`
  with 0 blockers — both COMPLETED topics retained as provenance, so the
  only gate-clearing topics are vacuous propose candidates. Readiness-to-
  propose and done-ness are currently indistinguishable to the scorer
  (session-findings F3).

## Observation 4 — live refusal click: SKIPPED (Brett, end of Step A)

The optional live `▶ draft proposal` refusal on `avatar-pilot-hardening`
was skipped. Refusal-agreement evidence rests on observations 1 and 3,
where Brett explicitly endorsed the would-be refusals.

## Clause verdict (recorded at end of Step A, 2026-07-31)

- **Bars credible on known documents:** TRUE — 5/5 credible
  (`a-65-completeness.md`; one refinement: branch-sessions ~0.05-0.1 low).
- **0.60 passes the proposal-worthy fragments:** NOT DEMONSTRABLE AS
  STATED — by partial-promotion design, fragments actually taken to
  proposal leave staging, so no such specimen exists to score (obs 3a).
  The nearest retained specimen (obs 2) scores 0.5 vs Brett's 0.55-0.6
  judgment — recorded as calibration finding F2 (scorer depth), while the
  0.60 THRESHOLD itself is affirmed by Brett.
- **0.60 refuses the unready ones:** TRUE — obs 1 (repo-selector remainder
  0.4) and obs 3 (consent-instrument 0.458), both scores judged accurate.
- **Refusals encountered are ones Brett agrees with:** TRUE — obs 1
  ("should not have moved forward") and obs 3 ("we should not proceed
  until those are addressed"), agreement explicit both times.
- **Read-only posture:** TRUE — before/after fingerprints byte-identical
  (`a-65-readonly-before.txt` / `a-65-readonly-after.txt`).

Overall: three of four clause elements cleanly true; the should-pass cell
is structurally untestable as written and yielded findings F2/F3 instead.
The Pass/Fail cell in the sign-off matrix is Brett's call: PASS WITH
FINDINGS (clause intent exercised, calibration findings recorded) or
PARTIAL (strict all-elements-true reading). No evidence was laundered
either way.
