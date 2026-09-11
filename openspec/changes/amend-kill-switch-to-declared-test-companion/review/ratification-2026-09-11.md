# Proposal Ratification: amend-kill-switch-to-declared-test-companion

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-11 at approximately 11:58Z by Brett Heap
(openxFactory repository owner) — a SELECTION, not a typed sentence, made
via the lane's multi-choice question: the option *"Ratify as filed
(Recommended)"*, whose description read: *"Ratify the text as landed.
Realization (the codexFactory companion) and archive stay separate later
acts on your word, per the three-act pattern."*, first-hand, in session,
lane `openxfactory-2` (display `openXfactory-2`), recorded on openxFactory
#745 (comment https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736).
Confirmed: 2026-09-11 at approximately 12:16Z by Brett Heap — a
SECOND SELECTION, not a typed sentence, made via the lane's multi-choice
question: the option *"Yes, ratify with the tightening (Recommended)"*,
confirming that the 11:58Z ratification covers the packet WITH round 5's
tightening (below), first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`), recorded on openxFactory #745 (comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736).
Directed: 2026-09-11 at approximately 12:34Z by Brett Heap — a THIRD
act, this one TYPED VERBATIM, *"land it when green and apply the
ratify"*, given after the lane reported round 6's three deltas and
reaffirmed verbatim through the afternoon; the lane reads it as covering
rounds 6 through 21. Recorded in the SAME openxFactory #745 comment as
words one and two — 5634512736, https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736
— so ONE comment carries all THREE acts.

## Decision

RATIFIED AS FILED, WITH ROUND 5'S TIGHTENING CONFIRMED COVERED, by Brett
Heap — on THREE acts of his word: two selections and one typed line.

## The three acts, and exactly what each ratifies

THREE acts of Brett Heap's word bear on this packet: TWO SELECTIONS and
ONE TYPED LINE. Words one and two were SELECTIONS, not typed sentences;
word three was typed verbatim.

**Word one.** Presented with the lane's multi-choice question — which
presented the packet as it stood with the four round-4 rulings (R1–R4)
already encoded — he chose:

> **"Ratify as filed (Recommended)"**

whose description read:

> **"Ratify the text as landed. Realization (the codexFactory companion)
> and archive stay separate later acts on your word, per the three-act
> pattern."**

— 2026-09-11 at approximately 11:58Z, first-hand, in session, lane
`openxfactory-2` (display `openXfactory-2`), recorded on openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745) (comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736).

**Word two.** Round 5 then landed a further tightening on the same
packet — EACH DECLARED COMPANION ARTEFACT NOW CARRIES ITS OWN REGENERATION
COMMAND, and the conformance test asserts that THE SET OF PATHS CHANGED BY
REGENERATING IN THE SCRATCH TREE EQUALS THE DECLARED ARTEFACT SET,
replacing the earlier existence check (`design.md` D-2/D-3, the declared
companion and the golden-digest decisions). Brett Heap was presented with a
second multi-choice question asking whether word one's ratification reaches
this tightening, and chose:

> **"Yes, ratify with the tightening (Recommended)"**

— 2026-09-11 at approximately 12:16Z, first-hand, in session, lane
`openxfactory-2` (display `openXfactory-2`), recorded on openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745) (comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736). Word two does not stand alone: it CONFIRMS word
one's scope. Word one remains the ratifying act; word two settles that it
reaches the packet's head as of round 5.

**Word three.** The third act is not a selection but a TYPED LINE:

> *Word three — 2026-09-11 at approximately 12:34Z, typed verbatim **"land
> it when green and apply the ratify"**, given after the lane reported round
> 6's three deltas (the allowlisted regeneration identifier is resolved only
> in reviewed test code; the artefact diff is taken against a committed
> post-withdrawal baseline; the requirement gains an explicit non-emptiness
> clause with its own scenario) and reaffirmed verbatim through the
> afternoon; the lane reads it as covering those deltas and every later fix
> round. Rounds 7 through 21 (ruled 2026-09-11 ~12:52Z through ~16:52Z;
> encoded by pushes 12:57Z through 16:55Z, the last being `c6008f10`; all
> Copilot findings RULED accept by the lane) changed no mechanism: rounds
> 7–11 fixed the
> ORDER of the conformance procedure (capture the declarations, commit a
> hermetic post-withdrawal baseline, measure the whole pinning suite with
> the conformance module excluded by path, regenerate every allowlisted
> artefact one tool at a time with the index and worktree reset between runs
> and compare (identifier, path) pairs against the baseline, record),
> DEFINED applying the companion at the throw (re-target each declared
> assertion's expectation, regenerate each declared artefact, remove the
> mapping and its comments, nothing else), DEFINED the restore as a forward
> change by the same procedure rather than a revert (so the golden digest
> records both movements), HARDENED the declaration grammar (one lexical
> refusal set for artefact paths, then containment before any open;
> allowlisted identifiers; a scratch git repository with inherited GIT_*
> control variables cleared), and STATED in D-2e that this packet fixes the
> invariants while the codexFactory companion's design owns the exact
> commands; rounds 12–21 tightened the same procedure's measurement
> invariants (the per-identifier inventory is the full working-tree delta
> including untracked and ignored paths; a reset barrier begins every tool
> run, the first included; every allowlisted invocation must exit zero
> within a finite constant timeout taken from the trusted allowlist before
> its delta is read; a control run on the committed pre-withdrawal tree must
> produce empty inventories, so every allowlisted tool is a deterministic
> byte-identical no-op run with interpreter caches suppressed; declared
> artefacts are tracked paths and are refused otherwise; declared paths
> reach git only as literal pathspecs after `--`, with a leading `-` and
> glob characters refused; the hermetic environment always nulls global git
> config and nulls or disables system config; the assertion run fails
> outright on any collection, import or internal error, on any exit status
> other than 0 or 1, or on timeout; the "nothing else" bound of the throw
> holds at both path and assertion level; the § 4 observation boxes tick on
> their recording and § 5 gains prerequisite (e)). All three acts are
> recorded in ONE #745 comment, 5634512736.*

**THE HEAD THIS RATIFIES.** PR #959's final head `c6008f10` (committed
2026-09-11T16:55:31Z; rounds 1–21 encoded), landed on main as squash commit
`07a8a45b62f063fe08625ad9c1fbb38762e6f85b`, merged 2026-09-11T17:19:09Z (that
squash commit committed 17:19:08Z) — this
packet's text with rounds 1–21 encoded in full (the initial filing plus fix
rounds answering Copilot and the independent verifier's review threads:
round 4's four rulings R1–R4 — every enrolled candidate class gets its own
declared companion and passing equality test with none grandfathered, the
companion declaration site fixed to the envelope's own comment block with a
stated `# companion:` / `# companion-artefact:` grammar, and the equality
check stated as assertion-set equality; round 5's tightening, named above
and confirmed covered by word two; and rounds 6 through 21's ordering,
definition, hardening and measurement deltas, named in word three's
paragraph above and covered by word three). No text this packet carries at
that head is excepted from the ratification: the amended requirement at
`specs/roles-authority-model/spec.md`, `proposal.md`'s account of decision
N-4's supersession, `design.md`'s D-1 through D-6, and every scenario and
task the packet states.

**AS FILED, WITH NO AMENDMENT AND NO VETO.** Unlike
`admit-review-lane-repin-to-merge-approval-envelope`'s "Ratify with
amendment" (that packet's own `review/ratification-2026-09-11.md`), none of
the three acts here carries a condition on any later act and none reopens
any decision: word one ratifies the text plainly and in full; word two only
CONFIRMS SCOPE over round 5's tightening, which is itself part of the
packet's own text at the landed head, not a condition laid on top of it;
and word three directs only the landing and the application of the
ratification, reaching rounds 6 through 21, which changed no mechanism.

## What is ratified

The proposal as written at `07a8a45b62f063fe08625ad9c1fbb38762e6f85b`, and every decision `design.md`
§ 2 carries — **D-1 through D-6 STAND AS RECOMMENDED, NO VETO EXERCISED ON
ANY OF THEM**, INCLUDING round 5's tightening of the mechanism D-2 and D-3
describe, and rounds 6 through 21's ordering, definition, hardening and
measurement deltas to that same mechanism:

- **D-1** — alternative (A), "one reviewed edit plus its declared test
  companion", over alternative (B) "make the pinning suite
  kill-switch-aware" (rejected: a suite that adapts to the entry leaving no
  longer notices it leaving).
- **D-2** — the declaration site is the envelope's own banner/comment block
  beside the candidate: no schema change, `active:` refused again. AS
  TIGHTENED IN ROUND 5: each declared companion artefact also carries its
  own regeneration command.
- **D-3** — the golden behaviour digest IS part of the declared companion,
  with the throw and the restore each recorded as a movement. AS TIGHTENED
  IN ROUND 5: the conformance test's equality check moves from an existence
  check to asserting that the set of paths changed by regenerating in the
  scratch tree equals the declared artefact set.
- **D-4** — `## MODIFIED`, not `REMOVED` + `ADDED`; the requirement header
  is unchanged.
- **D-5** — the realization surface is a codexFactory COMPANION change,
  authored by that repository's own lane; this lane authors none of it.
- **D-6** — the packet's stated refusals (no schema member, no ruleset
  edit, no bypass actor, no repository variable, no relaxed assertion, no
  contract bundle, no pin or tag movement, no tick of the parent's box
  3.6).

Decision **N-4** of `extend-merge-master-envelope-to-floor-bot-lanes`
(ratified 2026-09-07, PR #746, still unarchived) is amended BY THIS
RATIFICATION exactly as the packet's text states: the kill switch is now
canon as **the candidate entry TOGETHER WITH its declared test companion**,
not "one edit" alone — the ratification of this packet's text performs that
supersession, on the `## MODIFIED` delta at
`specs/roles-authority-model/spec.md`.

## What this ratification does NOT do

- **NO REALIZATION, IN EITHER REPOSITORY.** No byte of
  `.github/merge-approval-envelope.yml` moves, no `# companion:` /
  `# companion-artefact:` comment is written, no regeneration command is
  run, no conformance test is authored, in this ratifying commit or by any
  of the three acts. Realization is a codexFactory COMPANION change,
  authored by that repository's own lane, after ratification — none of
  the three words commissions it and none performs it; word three directs
  the landing and the application of the ratification, nothing more.
- **NO ARCHIVE.** `target_release` names a code surface, so under
  `release-realization` this packet archives only on merged-plus-green
  realization evidence — not on this ratifying commit. Every box in
  `tasks.md` § 2, § 3, § 4 and § 5 stays unticked; this ratification ticks
  nothing there.
- **NO THROW OF THE KILL SWITCH, ANYWHERE, BY ANYONE.** The candidate entry
  stays intact on codexFactory `main`. Nothing in either repository's
  enrolment, ruleset, or workflow moves.
- **THE PARENT'S BOX 3.6 STAYS OPEN.**
  `extend-merge-master-envelope-to-floor-bot-lanes` box 3.6 is an
  OBSERVATION box, not an owed-successor box: it does not tick on this
  ratification, and no box anywhere in the parent packet is touched by any
  of the three acts.
- **NO MERGE BY THIS RECORD.** This record ratifies text at one head. PR
  #959 landed 2026-09-11T17:19:09Z as a separate act under this
  repository's Rule 6 landing-window protocol (FILED record: openxFactory
  #745 comment 5638082322); landing the pull request that carries this
  ratifying commit is likewise a separate Rule 6 act, on the same recorded
  word, and is not performed by this record — the Rule 6 window binds
  because this change touches `openspec/changes/`.
- **NOTHING IN `extend-merge-master-envelope-to-floor-bot-lanes` OR
  `admit-review-lane-repin-to-merge-approval-envelope` MOVES.** Neither
  sibling packet is edited, and no box of either is ticked, by any of the
  three acts.

## Order of events

1. Brett Heap, 2026-09-11 ~03:40Z, SELECTION **"Accept the finding; file a
   successor"** — commissions the FILING of this packet (openxFactory #745
   comment 5632569506; codexFactory #232). Filing is not ratifying, and the
   packet said so throughout.
2. This packet filed `Status: draft`, then carried through fix rounds 1–4
   (Copilot and independent-verifier review threads; round 4's four
   rulings R1–R4 encoded every-class companion coverage, the
   comment-grammar declaration site, and the assertion-only equality
   check).
3. A decision brief was prepared for Brett Heap naming the packet as it
   stood at that round-4 head, with options including ratify as filed,
   ratify with amendment, and refuse.
4. Brett Heap, presented with the lane's multi-choice question, selects
   **"Ratify as filed (Recommended)"** — 2026-09-11 at approximately
   11:58Z, in session (word one).
5. Round 5 lands on the same packet: each declared companion artefact
   gains its own regeneration command, and the conformance test's equality
   check moves from an existence check to a regenerate-and-diff-paths
   equality check against the declared artefact set.
6. Brett Heap is presented with a second multi-choice question asking
   whether word one's ratification reaches round 5's tightening, and
   selects **"Yes, ratify with the tightening (Recommended)"** —
   2026-09-11 at approximately 12:16Z, in session (word two).
7. Round 6's six Copilot threads are RULED accept by the lane and
   REPORTED to Brett Heap (~12:30Z): the regeneration command becomes an
   allowlisted identifier resolved only in reviewed test code; the artefact
   diff is taken against a committed post-withdrawal baseline; the
   requirement gains an explicit non-emptiness clause with its own
   scenario.
8. Brett Heap, ~12:34Z, TYPES VERBATIM **"land it when green and apply the
   ratify"** (word three) — given after that report, read as covering those
   deltas, and reaffirmed verbatim through the afternoon; the lane reads it
   as reaching every later fix round too.
9. Round 6 is encoded by commit `62d9c99a`, pushed 12:35:51Z; rounds 7
   through 21 then land (ruled 2026-09-11 ~12:52Z through ~16:52Z; encoded
   by pushes 12:57Z through 16:55Z, the last being `c6008f10`; all Copilot
   findings RULED accept by the lane): the ORDER of the conformance
   procedure, the DEFINITION of applying the companion at the throw and
   of the restore as a forward change, the HARDENING of the declaration
   grammar, and the measurement invariants of that same procedure. No
   mechanism changes.
10. PR #959's final head `c6008f10` (committed 2026-09-11T16:55:31Z; rounds
    1–21 encoded) lands on main as squash commit
    `07a8a45b62f063fe08625ad9c1fbb38762e6f85b`, merged 2026-09-11T17:19:09Z
    (that squash commit committed 17:19:08Z).
11. This record, and the edits to `proposal.md`, `design.md`, `tasks.md`,
    `.openspec.yaml` and `README.md` it describes, are authored against
    that head, which the three acts together ratify.

## Records

- Governing issue: openxFactory
  [#745](https://github.com/opensoft/openxFactory/issues/745) — the filing
  comment (5632569506) and the ONE comment carrying all THREE ratifying
  acts — 5634512736, https://github.com/opensoft/openxFactory/issues/745#issuecomment-5634512736
  — word one's selection, word two's selection, and word three's typed
  line.
- Origin record: codexFactory
  [#232](https://github.com/codeXfactory/codexFactory/issues/232) — the
  companion posting of the filing word.
- The packet this ratifies: openxFactory pull request
  [#959](https://github.com/opensoft/openxFactory/pull/959) — FINAL HEAD
  `c6008f10` (committed 2026-09-11T16:55:31Z; rounds 1–21 encoded), landed on
  main as squash commit `07a8a45b62f063fe08625ad9c1fbb38762e6f85b`, merged
  2026-09-11T17:19:09Z (that squash commit committed 17:19:08Z). The figure
  2026-09-11T17:19:14Z carried by the FILED landing records (openxFactory #745
  comment 5638082322 and codexFactory #232 comment 5638082613) is the LANDER'S
  OBSERVATION time — the moment the landing script read the merge back — and
  not the merge time; those posted records stand as filed, and this record
  states the merge time.
- Parent packets: `extend-merge-master-envelope-to-floor-bot-lanes` (box
  3.6, the OBSERVATION this packet's realization will unblock, untouched by
  this ratification) and
  `admit-review-lane-repin-to-merge-approval-envelope` (ratified with
  amendment, PR #943; the companion-declaration rule this packet ratifies
  will bind its enrolment too at realization).
