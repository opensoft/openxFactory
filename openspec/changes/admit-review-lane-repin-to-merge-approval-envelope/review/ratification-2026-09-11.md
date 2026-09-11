# Proposal Ratification: admit-review-lane-repin-to-merge-approval-envelope

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-11T01:15Z (approx.) by Brett Heap (openxFactory repository
owner) — a SELECTION, not a typed sentence, made via the lane's multi-choice
question: the option *"Ratify with amendment"*, whose text read: *"Ratify
the text now; hold realization until the third unattended codexFactory cycle
is measured and the unrecorded-class fix is observed on a live approval."*,
first-hand, in session, lane `openxfactory-2` (display `openXfactory-2`),
recorded at openxFactory #745
(https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628376484,
the CLAIMED comment).

## Decision

RATIFIED, WITH AMENDMENT, by Brett Heap.

## The word, and why it is both a ratification and an amendment at once

Brett Heap's instruction was a SELECTION, not a typed sentence. Presented
with the lane's multi-choice question, he chose the option:

> **"Ratify with amendment"**

whose text read:

> **"Ratify the text now; hold realization until the third unattended
> codexFactory cycle is measured and the unrecorded-class fix is observed on
> a live approval."**

— 2026-09-11T01:15Z (approx.), first-hand, in session, lane
`openxfactory-2` (display `openXfactory-2`), first recorded in writing on
openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628376484)
(the CLAIMED comment this lane posted on claiming the ratification work).

**ONE SELECTION CARRIES THREE ACTS, AND THEY ARE KEPT DISTINCT BELOW.**
"Ratify the text now" ratifies this packet's text as written — the
enrolment, the four measured safeguards, the never-clearable ground answered
by delivery-not-choosing, decision **N-1** re-opened toward its own recorded
alternative **N-1 (b)** ("admit BOTH") with condition **N-1b (ii)** —
exactly as `design.md` D-1 through D-8 recommend, with **no veto exercised
on any of them**. "hold realization until the third unattended codexFactory
cycle is measured and the unrecorded-class fix is observed on a live
approval" is a SEPARATE act, taken AT this same ratification rather than
after it: it amends task **1.5** and `design.md` **D-3**, so that
REALIZATION (`tasks.md` § 3 — the envelope entry, the `sole_candidate()`
replacement, the witness edit) — not the paper ratification — is HELD until
two further preconditions are met, beyond and in addition to the
preconditions the packet's own § 4 already named. The two clauses are not
in tension: D-3's own recommendation (land the enrolment inert) is NOT
reversed by the amendment, and the amendment's hold is stated as a
sequencing decision over WHEN realization may be taken, not a reopening of
whether the enrolment's design is sound.

This differs from a plain "ratify as encoded" (`disposition-codexfactory-
floor-relocation-retitle`'s shape) precisely because the selected option
itself carries a condition on a LATER act (realization) rather than
accepting the packet whole. It differs from a REFUSAL (`proposal.md` §
*Options*, option 3) because the packet's text is not rejected — it stands,
ratified, and N-1 is re-opened toward (b) on the strength of it.

## What is ratified

The proposal as written at the head this record's own commit carries, and
**decisions D-1 through D-8 STAND AS RECOMMENDED, D-3 AMENDED**:

- **D-1 (ask at all)** — STANDS. Filed and now ratified, on the word that
  commissioned the filing and the word that ratifies the text.
- **D-2 (where the delta lives)** — STANDS. Four `## ADDED` requirements in
  `review-lane-floor-mirror`, no `## MODIFIED` block.
- **D-3 (inert on landing, or wait for the carve)** — STANDS **AS
  RECOMMENDED, AND IS AMENDED.** The enrolment still lands INERT — that
  answer is unchanged. The amendment adds a SECOND, independent hold on
  REALIZATION's timing: `tasks.md` § 3 may not be started by an agent until
  BOTH of the following are met (`tasks.md` task 1.5; `design.md` § *Amended
  at ratification*):
  1. A third consecutive measured cycle exists — per
     `extend-merge-master-envelope-to-floor-bot-lanes` `tasks.md` box
     **4.2**'s own count, of which codexFactory #314 (`b08958ae`) and #325
     (`df42f803`) are the first two — AND that third cycle is itself fully
     unattended: opened by `openxfactory[bot]`, approved by the
     merge-master App, and merged by `app/openxfactory`, with ZERO human
     acts on it — no `workflow_dispatch`, no click, no admin merge. #314
     counts toward box 4.2's three but does NOT itself satisfy the
     unattended condition, on its one hand-dispatched approval leg; #325
     does, carrying no human act at all. TWO cycles are measured as of
     this record and NEITHER is yet the qualifying third; box 4.2's own
     addendum states the box stays open on two.
  2. The `Candidate class: unrecorded` rendering defect
     (`extend-merge-master-envelope-to-floor-bot-lanes`
     `review/gate-rules-council-admitting-record-2026-09-10.md` § 3.5, box §
     3.1 row) is fixed — codeXfactory/codexFactory PR #369 — AND observed
     fixed on one live approval that renders the matched candidate class by
     name rather than `unrecorded`.
- **D-4 (merge method)** — STANDS AS THE PACKET STATES IT (SQUASH), not
  individually named by the word; ratified under the blanket disposition,
  per the `accept-sequenced-after-header-line` 0.4/0.5 precedent for a
  decision the ratifying word does not call out by number.
- **D-5 (the realization surface is three files)** — STANDS.
- **D-6 (witness text when the class lands but the carve has not)** —
  STANDS, and is UNCHANGED by the D-3 amendment: D-6 answers what the
  witness says once the class is enrolled but the carve is missing; the
  amendment defers WHEN the class may be enrolled at all, a strictly
  earlier gate than the one D-6 addresses.
- **D-7 (replace, don't relax, `sole_candidate()`)** — STANDS.
- **D-8 (scope refusals — the carve, the surface narrowing, the precondition
  measurement, the completion-path word)** — STANDS; none of the four is
  taken by this ratification.

**Decision N-1 is RE-OPENED TOWARD N-1 (b), "admit BOTH", with its condition
N-1b (ii)**, on the ratification of this packet's text — the packet's whole
ask is that re-opening, so ratifying the text performs it (`tasks.md` 1.1).
Brett Heap's 2026-09-10 § 6.3 rulings (codexFactory #232 comment
5618469628; openxFactory #745 comment 5618883586) STOOD until this word and
are superseded by it, exactly as `proposal.md` said they would be on
ratification.

## What this ratification does NOT do

- **NO REALIZATION.** No candidate class is enrolled in
  `.github/merge-approval-envelope.yml`, no `sole_candidate()` byte moves,
  no witness text changes, in this ratifying commit or by this word. Every
  box in `tasks.md` § 3 remains unticked, and — by the amendment — may not
  be started by an agent until 1.5.a and 1.5.b both tick.
- **NOT THE CARVE.** `tasks.md` box 4.1 (codexFactory's decision core) is
  untouched, unasked-for by this word, and would remain a precondition even
  had the amendment not been made.
- **NOT THE `Bounded autonomous surface` NARROWING**, box 4.2 — codexFactory's
  text, not this repository's to move.
- **NOT THE PRECONDITION MEASUREMENT (auto-merge on a rulesets-only `main`)**,
  box 4.3, nor **THE COMPLETION-PATH WORD**, box 4.4 — both remain open,
  Brett Heap's or an agent's later measurement, unaffected by this record.
- **NO MERGE.** This record ratifies text at one head. Landing PR #910 (or
  its successor pull request carrying this ratifying commit) is a SEPARATE
  act under this repository's Rule 6 landing-window protocol, because this
  change touches `openspec/changes/`.
- **NOTHING IN `amend-mirror-floor-regeneration-merge-authority` MOVES.**
  Box 4.3 there ticked already, on the FILING (2026-09-10, on "file it");
  this ratification does not re-tick it and ticks no other box in that
  packet.

## Order of events

1. Brett Heap, 2026-09-10 ~17:2xZ, "do 1 and 2, sign, file it, do 744" —
   commissions the FILING of this packet (openxFactory #745 comment
   5622848416). Filing is not ratifying, and the packet said so throughout.
2. This packet filed, `Status: draft`, PR #910, merged as a DRAFT filing at
   `05c706d6` (2026-09-10).
3. A decision brief was prepared for Brett Heap naming three options —
   ratify as encoded, ratify with amendment, refuse — and recommending
   RATIFY WITH AMENDMENT on the packet's own evidence bar (three cycles
   named, two measured) and the sibling lane's own observed rendering
   defect.
4. Brett Heap, presented with the lane's multi-choice question, selects
   **"Ratify with amendment"** — 2026-09-11T01:15Z (approx.), in session.
   The lane records the selection in writing on openxFactory #745 (the
   CLAIMED comment,
   https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628376484)
   on claiming this ratification work.
5. This record, and the edits to `proposal.md`, `design.md`, `tasks.md`,
   `.openspec.yaml` and `README.md` it describes, are authored against that
   word and land in one ratifying commit.

## Records

- Governing issue: openxFactory
  [#745](https://github.com/opensoft/openxFactory/issues/745) — the filing
  comment (5622848416) and, on ratification, the CLAIMED comment recording
  the selection quoted above ([comment
  5628376484](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628376484)).
- Origin record: codexFactory
  [#232](https://github.com/codeXfactory/codexFactory/issues/232) — the
  § 6.3 rulings this ratification supersedes. THE RATIFICATION SELECTION
  ITSELF WAS GIVEN IN SESSION AND HAS NO SEPARATE CODEXFACTORY POSTING:
  unlike the earlier filing word, it is recorded only on openxFactory #745
  (above).
- The packet this ratifies: openxFactory pull request
  [#910](https://github.com/opensoft/openxFactory/pull/910), filed draft,
  merged `05c706d6`, 2026-09-10.
- The amendment's two evidence obligations: `tasks.md` 1.5.a (the third
  cycle) and 1.5.b (codeXfactory/codexFactory PR #369, merged and observed
  fixed on a live approval).
- Parent packets: `amend-mirror-floor-regeneration-merge-authority` (box
  4.3, ticked on filing, untouched here) and
  `extend-merge-master-envelope-to-floor-bot-lanes` (box 4.2, the
  three-cycle gate this amendment leans on; § 3.1's `Candidate class:
  unrecorded` finding, per `review/gate-rules-council-admitting-record-
  2026-09-10.md` § 3.5).
