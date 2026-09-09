# Tasks: govern-archived-record-edits

Status: ratified
Ratified by: govern-archived-record-edits — 2026-09-08, Brett Heap, CLI approval
`gh pr review 788 --approve` (review 5141756427, APPROVED 2026-09-08T12:38:36Z,
empty body) (record `review/ratification-2026-09-08.md`)
Lane: opsXfactory-1
Edited (bookkeeping): 2026-09-09 by archive-govern-archived-record-edits — archive move

**NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
PACKET RATHER THAN AN OVERSIGHT.** This is a PROPOSAL. No archived byte is
edited, no pin is re-derived, no checker is written, no repository's local
convention is amended, and no spec delta is promoted.

**AMENDED 2026-09-08 by this change's realization
(`govern-archived-record-edits`, lane `opsXfactory-1`), on the precedent of
commit `3b530009`; the superseded sentence is
quoted rather than rewritten.** The preamble above opened:

> **NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
> PACKET RATHER THAN AN OVERSIGHT.**

That is SUPERSEDED. The packet was ratified on 2026-09-08 and realized on the
same day, so the list below now reads: **19 boxes ticked with dated evidence, 8
carrying a dated NOT-OWED line, and 1 — box 4.2 — run, recorded and deliberately
left open for the archive act.** Leaving the list untouched would now be as false
as ticking a box on another repository's behalf.

**NOT SUPERSEDED, and re-verified at this head rather than assumed:** the
neighbouring sentence *"No archived byte is edited, no pin is re-derived, no
checker is written, no repository's local convention is amended, and no spec
delta is promoted."* Every clause of it still holds. The realization's whole diff
is six paths — this file, the packet's `proposal.md` and its new `evidence/`
file, `docs/document-lifecycle.md`, one appended README sentence, and the Speckit
feature directory — and the delta reaches promoted canon only at the archive act.

**Tags.** Untagged = openxFactory. `[OpsxFactory]` = `opensoft/OpsxFactory` and
its own OpenSpec instance — listed as the domain twin's acts, outside this
change's archive gate. `[OPERATOR]` = only Brett Heap can perform it.

**DISPOSITION 2026-09-09, AT THE ARCHIVE — THE THIRD AND LAST DISPOSITION UNDER
THIS PREAMBLE, AND THE ONE THAT MOVES CANON.** The realization's amendment above
closed the "EVERY BOX IS UNTICKED" sentence and re-verified the sentence beside
it; THIS one is the archive, so the clause it discharges is quoted in place
rather than deleted:

> No archived byte is edited, no pin is re-derived, no checker is written, no
> repository's local convention is amended, and no spec delta is promoted.

**EXACTLY ONE OF ITS FIVE CLAUSES MOVES, AND IT IS THE LAST.** The delta IS
promoted at this commit — one `## MODIFIED` requirement replaced wholesale and
two `## ADDED` requirements appended in
`openspec/specs/document-lifecycle/spec.md`, which goes **18 → 20**
requirements. **THE OTHER FOUR HOLD UNQUALIFIED AND ARE RE-MEASURED HERE, NOT
ASSUMED:** no pin is re-derived, because **NO IN-REPO `sha256` PIN NAMES ANY
FILE THIS PULL REQUEST TOUCHES** — measured at base `9a67d42c` by searching every
`*.yaml`/`*.yml`/`*.json` in the tree for each touched path as a literal string.
**THE ONE NEAR MISS IS NAMED RATHER THAN LEFT TO BE FOUND:**
`contracts/review-lane-floor-snapshot.yaml:217` DOES name
`openspec/specs/document-lifecycle/spec.md`, and it is **A PATH LIST, NOT A
DIGEST** — the floor enumerates the CODEOWNERS-gated paths and carries no
`sha256` of any of them, its own bytes being what
`contracts/review-lane-pin.yaml` witnesses, and that file is not touched here.
The spec path is ALREADY in the list and stays in it; **NO FILE IS ADDED UNDER
`openspec/specs/`**, so no floor advance is owed either — the shape
`refresh-install-repository-enumerations` measured at its own archive. No checker is written
(nothing under `scripts/`, `.github/` or `tests/` other than the one ledger
row); no repository's local convention is amended (nothing outside this
repository is touched at all); and **no archived byte is edited** — for the
reason the next paragraph gives, which is this packet's whole subject.

**THIS IS THE FIRST ARCHIVE PERFORMED UNDER THE RULE THIS PACKET PROMOTES, AND
THE FIRST RECORD THAT RULE BINDS IS THIS PACKET'S OWN.** *An archived record is
edited only as a bookkeeping correction under a recorded ruling* names, among
the edits it REFUSES, "a task record or its tick state" — so ticking a box on
this file AFTER it moves under `openspec/changes/archive/` is an edit the
requirement forbids, whatever ruling authorizes it. **THE RESOLUTION IS
ORDERING, NOT AN EXCEPTION**, and it is the precedent's:
`refresh-install-repository-enumerations` closed its boxes in the commit BEFORE
its archive commit (openxFactory PR [#825](https://github.com/opensoft/openxFactory/pull/825)
→ `ca4a1558`). **EVERY TICK IN THIS FILE IS AUTHORED WHILE THE PACKET IS STILL
LIVE**, in the commit that precedes the move; the archive commit that follows is
a PURE MOVE plus the promotion, and it edits no byte of any file it moves. So
the rule's refusal is never engaged and no exception to it is claimed, taken or
needed.

**THE `Edited (bookkeeping):` LINE IN THE HEADER ABOVE IS CARRIED ANYWAY, AND
THAT IS STRICTER THAN THE MINIMUM RATHER THAN LOOSER.** On the ordering above
the neutral minimum is not owed at all — nothing under `archive/` is edited —
but this file's diff is presented at its ARCHIVED path across the pull request,
and a reader who sees `openspec/changes/archive/2026-09-09-…/tasks.md` modified
deserves the record rather than the inference. The line names the change and the
class; the RULING it records under is the ratified packet itself, whose § 6
boxes reserve exactly these acts to the archive act and were approved by Brett
Heap on 2026-09-08 — recorded BEFORE the edit, which is what the requirement
asks of a ruling. The note says WHAT changed and never THAT IT MAY.

**PRECONDITIONS, MEASURED BEFORE THE MOVE AND NOT AFTER IT.** (1) Box 4.2's
currency check: canon **5,815 characters**, unchanged since ratification, **0
canon lines removed** under both bounds — canon did NOT move, so the block is
carried forward as ratified and no re-derivation is owed. (2) Neither `## ADDED`
title collides with anything promoted: an exact-title grep over all of
`openspec/specs/` returns nothing for either. (3) The packet's open boxes at
this commit are exactly **3.2, 3.3, 3.5, 4.2, 5.2, 5.3, 6.1, 6.2 and 6.3** —
nine, which is the 8 dated NOT-OWED plus box 4.2 — and the ones this act closes
are **4.2, 6.1 and 6.2**. **BOX 6.3 STAYS OPEN AND IS NOT TICKED BY THIS ACT**,
for the reason its own clause now gives.

## 0. Bookkeeping this branch carries, and the one stamp that is provisional

- [x] 0.1 **RE-STAMP THE SWEEP LEDGER ROW WITH THE REAL PULL-REQUEST NUMBER.**
  `tests/sequenced_after/corpus-ledger.yaml` carries this change's row and its
  DERIVED keys are measured and correct (`--ledger-diff` exits 0 at this
  branch's head). Its `moved_by` is **PROVISIONAL** — no pull request existed
  when the seeder ran, and the value is a placeholder rather than an observed
  number. The ledger's own doctrine makes `moved_by` AUTHOR-SUPPLIED AND
  UNVERIFIED (only its `#<digits>` shape is checked), so this reds no gate; it
  is a pointer a human follows and it should be true.
  **IT IS ALREADY KNOWN TO BE WRONG, SO THIS BOX IS MANDATORY AND NOT TIDY-UP.**
  `#785` was the next number free when the seeder ran; it is now
  `ideation/remove-moved-domain-files`, another lane's OPEN pull request. This
  is the second time the trap has sprung on this lane —
  `add-consent-custody-rederivation-record`'s provisional `#757` was taken the
  same way while that packet was in review — and it will spring again for
  anyone who reads a placeholder as provenance.
  **DO NOT RE-RUN THE SEEDER FOR THIS — IT IS A NO-OP HERE, AND THAT IS
  MEASURED, NOT ASSUMED.** `--seed-ledger --moved-by '#<real>'` re-derives the
  corpus and stamps provenance only on rows whose DERIVED keys actually moved;
  this row's derived keys are already correct, so the seeder PRESERVES its
  existing provenance. Run at this head with a different number it reported
  `184 rows, 0 moved by #999` and produced a **ZERO-LINE DIFF**, leaving
  `moved_by: "#785"` in place — the documented recipe would look like a
  re-stamp and change nothing. **The re-stamp is a DIRECT ONE-FIELD EDIT** of
  this row's `moved_by` in `tests/sequenced_after/corpus-ledger.yaml`, followed
  by `python3 scripts/validate-sequenced-after.py . --ledger-diff`, which MUST
  report `per-change sweep ledger consistent with the corpus` — also measured at
  this head with the field edited by hand. That is legitimate because the
  ledger's own doctrine makes `moved_by` AUTHOR-SUPPLIED AND UNVERIFIED,
  shape-checked (`#<digits>`) and never resolved.

  **PERFORMED 2026-09-08.** openxFactory PR
  [#788](https://github.com/opensoft/openxFactory/pull/788) was opened by
  `openxfactory[bot]` on head `97d1e7fa`, so the real number is known. The row's
  `moved_by` was edited directly from `"#785"` to `"#788"` — ONE field, ONE
  line, nothing else in the file — and
  `python3 scripts/validate-sequenced-after.py . --ledger-diff` reports
  `per-change sweep ledger consistent with the corpus (184 rows)`. `moved_on`
  is NOT re-stamped: it records when the row's derived keys moved, which was
  2026-09-08, not when its provenance pointer was corrected.

  **THE BOX STAYS UNTICKED, AND THAT IS THE CONVENTION RATHER THAN AN
  OVERSIGHT.** This file's own preamble holds that every box is unticked while
  the packet is a proposal, and this packet is `Status: draft` awaiting
  ratification at task 1.1. The corpus precedent is exact:
  `add-consent-custody-rederivation-record` is `Status: ratified`, its ledger
  row carries the REAL pull request `#774`, and its `tasks.md` has ZERO ticked
  boxes — the ledger carrying a true number and the box staying unticked are
  not in tension, because the row is bookkeeping the branch carries and the box
  is a claim about the packet having begun.

  **AMENDED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`); the superseded
  sentence is quoted rather than rewritten.** The
  paragraph above opened:

  > **THE BOX STAYS UNTICKED, AND THAT IS THE CONVENTION RATHER THAN AN
  > OVERSIGHT.**

  That is SUPERSEDED: the act it describes is DONE and independently recorded,
  and the packet is no longer a proposal awaiting ratification. **NOT
  superseded:** the neighbouring statement that "the row is bookkeeping the
  branch carries and the box is a claim about the packet having begun" — that
  distinction is exactly why the box is ticked NOW, when the packet HAS begun,
  and was rightly unticked before.

  **CORRECTED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`) —
  stale-but-true-when-written text, quoted and never rewritten
  in place.** The paragraph above states:

  > this packet is `Status: draft` awaiting ratification at task 1.1

  That was TRUE WHEN WRITTEN and is FALSE NOW. This file has carried
  `Status: ratified` with its `Ratified by:` citation since 2026-09-08 (header,
  lines 3-4), ratified by Brett Heap on reviews `5141756427`
  (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
  `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
  subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
  dismissal message — so the ratification stands on
  `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
  review. The
  corpus-precedent sentence beside it is a statement about
  `add-consent-custody-rederivation-record` at its own head and is NOT corrected
  here; measured at openxFactory `main` `6cc06288` on 2026-09-09 UTC that packet
  still carries 46 unticked boxes and 0 ticked, so it remains true as written.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the re-stamp is
  DONE and landed with PR #788. UTC DATE:
  2026-09-08. EVIDENCE: `tests/sequenced_after/corpus-ledger.yaml:214` reads
  `moved_by: "#788", moved_on: "2026-09-08"` on openxFactory `main`, and
  `python3 scripts/validate-sequenced-after.py . --ledger-diff` reports
  `per-change sweep ledger consistent with the corpus (185 rows)` at this
  branch's head (packet evidence file `evidence/realization-2026-09-08.md`
  § 4.3). The ledger file is READ here and NOT rewritten.

## 1. Ratification — OWED, NOT GIVEN — AMENDED 2026-09-08

**GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED.** Brett Heap ratified
this packet by CLI approval on PR #788 (GitHub review 5141756427, APPROVED
2026-09-08T12:38:36Z, empty body); record
`review/ratification-2026-09-08.md`. The heading is left as written because it
names what the section was raised to hold, and the boxes are left unticked
because that is the convention this corpus keeps: the sibling packet
`add-consent-custody-rederivation-record` is `Status: ratified` with ZERO of its
46 boxes ticked, its § 1 among them. Ratification is not realization, and a
half-ticked list would say the packet had begun.

**AMENDED 2026-09-08 by this change's realization
(`govern-archived-record-edits`, lane `opsXfactory-1`); each superseded sentence
is quoted rather than rewritten.**

Superseded, from the paragraph above:

> **GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED.**

and its re-assertion:

> the boxes are left unticked because that is the convention this corpus keeps:
> the sibling packet `add-consent-custody-rederivation-record` is
> `Status: ratified` with ZERO of its 46 boxes ticked, its § 1 among them.
> Ratification is not realization, and a half-ticked list would say the packet
> had begun.

Both are superseded by the same fact: the packet HAS begun. Ratification is
still not realization — realization is what happened next, on the same day, and
the boxes below are ticked against the ratification RECORD rather than against
the approval being read as realization.

**THE APPROVAL STATE ITSELF WAS RE-MEASURED, AND IT IS NOT WHAT A READER WOULD
ASSUME.** Measured 2026-09-09 UTC with a read-only
`gh api repos/opensoft/openxFactory/pulls/788/reviews` and the issue timeline,
PR #788 carries **TWO** approving reviews by `brettheap`, not one:
`5141756427`, APPROVED `2026-09-08T12:38:36Z` on commit `d0f8cccf`, and
`5142530432`, APPROVED `2026-09-08T13:45:56Z` on commit `158a4d3b`. **BOTH now
read `DISMISSED`**, dismissed by GitHub on the pushes that followed them — at
`2026-09-08T12:53:23Z` and `2026-09-08T13:53:22Z`, each with `state_was:
approved` and NO dismissal message, which is the signature of automatic
stale-approval dismissal under branch protection rather than a withdrawal.
Both bodies are EMPTY. **THE RATIFICATION STANDS** on
`review/ratification-2026-09-08.md`, not on a currently-APPROVED review, and
this realization records that rather than leaving a reader to find a dismissed
review behind an unqualified "APPROVED". The RATIFIED text above, the record and
the ratified README row sentences are FROZEN and are not edited for this; the
clause lives in the realization's own notes and evidence. (The record names one
review and gives the ratified baseline as `8cc76e1b`, where the API reports
`d0f8cccf` as review `5141756427`'s commit; the record's own § on the two clocks
already measures the packet's bytes as identical at both heads, so nothing here
resolves that and nothing needs to.)

**NOT superseded, and unchanged:** the sentence naming the ratification itself —
*"Brett Heap ratified this packet by CLI approval on PR #788 (GitHub review
5141756427, APPROVED 2026-09-08T12:38:36Z, empty body); record
`review/ratification-2026-09-08.md`."* That is the record every § 1 tick below
cites, and no word of the approval is quoted anywhere, because the body is EMPTY.

**THE HEADING IS AMENDED TOO, AND IT SUPERSEDES A DELIBERATE DECISION, WHICH IS
WHY THAT DECISION IS NAMED.** The heading now reads `## 1. Ratification — OWED,
NOT GIVEN — AMENDED 2026-09-08`, the marker being the pair's closed
vocabulary `AMENDED <UTC date>` as a whole token rather than a bare
parenthetical or a `[SUPERSEDED …]` form. The clause superseded is this
section's own:

> The heading is left as written because it names what the section was raised to
> hold

That was a decision taken on purpose, not an oversight, and it is superseded on
one ground only: the heading asserts that ratification is OWED, and it was GIVEN
on the day this packet was ratified. What the section was raised to hold is
unchanged and the original words are kept in front of the marker. (Mirror ruling
M-A7; this amendment is VETO POINT 5, reversible by restoring the heading and
striking this block with a dated line.)

**THE THREE VETO POINTS AT 1.2 WERE PUT TO HIM VERBATIM IMMEDIATELY BEFORE THE
APPROVAL AND NONE WAS EXERCISED**, so the packet is ratified AS WRITTEN: every
declared family (not custody pins only), report-then-refuse (not refuse from
landing, not strike), and TWO `## ADDED` requirements (not one).

- [x] 1.1 **[OPERATOR] Ratify or veto.** The F.3 ruling came in TWO comments on
  OpsxFactory PR #248 — the SHAPE
  (*"Header/bookkeeping edits only + re-derive pins"*) on 2026-09-06T23:42Z,
  comment 5563099832, and the HOME (*"Both at once"*) on 2026-09-07T13:51Z,
  comment 5571629298. It chose no requirement title, no delta shape, no
  definition of the bookkeeping class, no ordering between ruling and edit, and
  no refusal posture. Each is `design.md`'s D-1..D-8 and each is a veto point.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: Brett Heap
  ratified this packet. UTC DATE: 2026-09-08.
  EVIDENCE, cited as the record cites it and re-measured against the GitHub API
  on 2026-09-09: reviews `5141756427`
  (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
  `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
  subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
  dismissal message — so the ratification stands on
  `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
  review; ratified baseline `8cc76e1b`. **NO WORD IS
  QUOTED**: the approval body is EMPTY, so no verbatim word exists, and this note
  restates what the record states rather than attributing a sentence to him.
- [x] 1.2 **[OPERATOR] TWO named widenings and one split, each a veto point.**
  Mirrored from the domain twin's 1.2a/1.2b/1.2c, because the same three
  decisions are open in both halves and a ruling on one is a ruling on both.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: all three were
  put to him verbatim immediately before the
  approval and NONE was exercised, so the packet is ratified AS WRITTEN. UTC
  DATE: 2026-09-08. EVIDENCE: reviews `5141756427`
  (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
  `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
  subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
  dismissal message — so the ratification stands on
  `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
  review; the
  not-exercised finding is the record's, not this note's inference. No word
  quoted — the body is empty.
  - [x] 1.2a **The pin SCOPE.** Your 2026-09-06 shape selection (comment
    5563099832) says "every dependent **custody** pin". The second ADDED
    requirement reaches EVERY pin of EVERY declared family. Basis: your
    2026-09-07 restatement (comment 5571629298) drops the qualifier — "every
    edit of a pinned target re-derives dependent pins in the same change" —
    read with your F.2 scope selection of the same day, "Every in-repo sha256
    pointer to an in-repo target", the widest option put to you and the scope
    the OpsxFactory gate is built to. **The narrower reading — CUSTODY PINS
    ONLY — is available**: it matches the 2026-09-06 wording exactly, and its
    cost is that evidence digests, plan-acceptance references, fence baselines
    and contract pins are obliged by nothing while that gate re-derives them.
    Narrowing here forces the same narrowing on the OpsxFactory half.

    **TICKED 2026-09-08 by this change's realization
    (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the veto was
    NOT exercised, so the DEFAULT STANDS —
    every pin of every declared family, not custody pins only. UTC DATE:
    2026-09-08. EVIDENCE: reviews `5141756427`
    (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
    `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
    subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
    dismissal message — so the ratification stands on
    `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
    review. No word quoted.
  - [x] 1.2b **The no-rule consequence, and WHEN it bites.** As written the
    requirement REPORTS such an edit — naming the family, the target and the
    home that owes the rule — and refuses only once that family declares.
    **THREE options, not two.** (i) Report-then-refuse, as written. (ii)
    **REFUSE FROM LANDING**: coherent, and measured it refuses EVERY
    pinned-target edit in the estate the day this change archives, because no
    family has a declared rule and `code_surface: none` means it archives on
    landing with nothing to sequence behind — the routine lifecycle-header
    discharge and the F.1/F.2 repairs included. (iii) **STRIKE the consequence**,
    leaving the obligation with no consequence for the families that need it
    most. Either alternative forces the OpsxFactory half to move in LOCKSTEP: it
    states the same rule at its own altitude, and a downstream `MUST` may not
    contradict a neutral `MUST NOT`.

    **TICKED 2026-09-08 by this change's realization
    (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the veto was
    NOT exercised, so the DEFAULT STANDS —
    option (i), report-then-refuse as written; (ii) refuse-from-landing and (iii)
    strike were not taken. UTC DATE: 2026-09-08. EVIDENCE: reviews `5141756427`
    (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
    `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
    subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
    dismissal message — so the ratification stands on
    `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
    review.
    No word quoted.
  - [x] 1.2c **The ONE-vs-TWO ADDED split.** Your F.3 wording names "an ADDED
    requirement" — singular — carrying both halves of the rule. This packet
    splits them into TWO, and `.openspec.yaml` flags the delta shape for veto.
    The measured reason is that the failures are invisible to each other: one of
    the three custody pins the motivating commit broke names a target in a
    change directory that has never been archived, so a single requirement
    scoped to `openspec/changes/archive/` would report itself satisfied while
    that pin stayed broken. **If one requirement is wanted**, the cost is that
    its scope sentence must reach outside the archive tree, and the OpsxFactory
    half must collapse the same way.

    **TICKED 2026-09-08 by this change's realization
    (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the veto was
    NOT exercised, so the DEFAULT STANDS — TWO
    `## ADDED` requirements, not one; the delta was not collapsed. UTC DATE:
    2026-09-08. EVIDENCE: reviews `5141756427`
    (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
    `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
    subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
    dismissal message — so the ratification stands on
    `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
    review; the shape is measured at this
    head as 1 `## MODIFIED` + 2 `## ADDED` blocks, 18 scenarios. No word quoted.
- [x] 1.3 **[OPERATOR] Rule on D-3 specifically** — whether the `## MODIFIED`
  block closing *Proposal packets carry the lifecycle header*'s dangling "takes
  the route archived-record edits take" is wanted. Declining it leaves canon
  naming a route it does not define, which is the state that produced the
  finding; taking it means a MODIFIED block that must stay current until
  archive (task 4.2).

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: ruled by the
  same approval, and the veto was not
  exercised — the `## MODIFIED` block is WANTED and stands, which is exactly why
  task 4.2's currency obligation is live until archive and why box 4.2 below is
  left open. UTC DATE: 2026-09-08. EVIDENCE: reviews `5141756427`
  (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
  `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
  subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
  dismissal message — so the ratification stands on
  `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
  review. No word
  quoted.
- [x] 1.4 **[OPERATOR] Rule on the reading NOT taken** — a STRICT READ-ONLY
  ARCHIVE. `design.md` § *Readings not taken* 1 records why this packet declines
  it (it would make the pre-existing header population permanently unfixable,
  contradicting canon in force, and it would overturn the F.3 selection). It
  remains available and would be a different change.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: ruled by the
  same approval, and the veto was not
  exercised — the strict read-only archive reading remains NOT TAKEN and would be
  a different change. UTC DATE: 2026-09-08. EVIDENCE: reviews `5141756427`
  (APPROVED `2026-09-08T12:38:36Z` on `d0f8cccf`) and `5142530432` (APPROVED
  `2026-09-08T13:45:56Z` on `158a4d3b`), BOTH since DISMISSED by GitHub on the
  subsequent pushes — stale-approval dismissal at 12:53:23Z and 13:53:22Z, no
  dismissal message — so the ratification stands on
  `review/ratification-2026-09-08.md` rather than on a currently-APPROVED
  review;
  the declining reasons are `design.md` § *Readings not taken* 1. No word quoted.
- [x] 1.5 Write `review/ratification-<date>.md` recording the word verbatim, the
  head it was given against, and what it does and does not authorize.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the record was
  written and is in this packet. UTC DATE:
  2026-09-08. EVIDENCE: `review/ratification-2026-09-08.md`, which names the
  ratified baseline `8cc76e1b`, the review id `5141756427`, the APPROVED state
  and its `2026-09-08T12:38:36Z` timestamp (the record names ONE review; the
  realization measured TWO and both are now DISMISSED — see the § 1 amendment
  above and the evidence file, neither of which edits the record), and what the
  approval does and does
  not authorize. **WHERE THIS BOX SAYS "the word verbatim", THE RECORD RECORDS
  THAT THERE IS NONE**: the approval carried an EMPTY body, so the record names
  the act and its resolvable identifiers instead and states in its own words that
  it quotes nothing and invents nothing. A verbatim quotation is not owed where
  no words exist, and inventing one to satisfy the box would be the defect this
  packet exists to refuse.

## 2. The delta — three requirement blocks, authored

- [x] 2.1 `## ADDED` — *An archived record is edited only as a bookkeeping
  correction under a recorded ruling*. Authored.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the block is
  authored and ratified as written. UTC DATE:
  2026-09-08. EVIDENCE: `specs/document-lifecycle/spec.md` at the ratified
  baseline `8cc76e1b`, unchanged at this branch's head (`git log 3504287a..HEAD`
  over the packet, promoted canon and the § 3.4 target is EMPTY); the delta's
  measured shape is 1 `## MODIFIED` + 2 `## ADDED` blocks and 18 scenarios, of
  which this requirement carries five.
- [x] 2.2 `## ADDED` — *A change that edits a pinned target re-derives every
  dependent pin in the same change*. Authored.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the block is
  authored and ratified as written, TWO
  `## ADDED` requirements rather than one, the split having survived veto point
  1.2c. UTC DATE: 2026-09-08. EVIDENCE: `specs/document-lifecycle/spec.md` at the
  ratified baseline `8cc76e1b`, unchanged at this head; five scenarios in this
  block, within the delta's measured 18.
- [x] 2.3 `## MODIFIED` — *Proposal packets carry the lifecycle header*.
  Authored. Verified against canon: **canon's block is 5,815 characters, the
  delta block is 7,186, and the 1,371-character difference is entirely
  INSERTED** (slice from the requirement heading to the next, trailing newlines
  stripped both sides). EVERY canon byte is carried verbatim, all six promoted
  scenarios restated, and exactly two hunks of difference — both PURE INSERTIONS
  (one paragraph naming the route, one added scenario). Nothing is reworded and
  nothing is deleted, so no
  ``**Removed from canon by …**`` marker is owed and doc-health's
  `modified-block-currency` arm reports nothing against this block.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the block is
  authored and ratified as written. UTC DATE:
  2026-09-08. EVIDENCE: `specs/document-lifecycle/spec.md` at the ratified
  baseline `8cc76e1b`, unchanged at this head; the currency re-measurement is
  recorded in the packet evidence file `evidence/realization-2026-09-08.md`
  § *Measurement 2*, which reproduces **canon 5,815 characters and 0 canon lines
  removed**. **ONE FIGURE ABOVE IS CORRECTED THERE RATHER THAN HERE, and this box
  is ticked on the result rather than on the figure:** the "7,186" delta length
  above is the block bounded at `## ADDED Requirements`; the re-measurement's own
  script terminates at the next `### Requirement:` heading and returns 7,209, the
  23-character difference being exactly that heading line. Both bounds give the
  same load-bearing result — every canon byte carried, nothing removed — so the
  authored claim stands. **TICKING 2.3 IS NOT TICKING 4.2**: this box records
  that the block was authored current; 4.2 keeps the obligation live until
  archive and is deliberately left open below.

## 3. Composition — named here; 3.4 alone is this packet's own act — AMENDED 2026-09-08

**AMENDED 2026-09-08 by this change's realization
(`govern-archived-record-edits`, lane `opsXfactory-1`); the superseded clause is
quoted rather than rewritten.** The
heading asserted:

> 3.4 alone is this packet's own act

That is SUPERSEDED by box 3.1's tick below. It stopped being true not because
this packet took on another repository's work, but because 3.1's act — "the
citations are re-checked to resolve once both heads settle" — is a CHECK this
repository performs, and the heads have now settled. **NOT superseded:** the
first clause, *"Composition — named here"*, which is still exactly what § 3 does
for 3.2, 3.3 and 3.5. (Mirror ruling M-A3.)

- [x] 3.1 **[OpsxFactory]** The domain twin `govern-archived-record-edits`
  lands and is ratified. Both packets cross-cite by change id and repository;
  the citations are re-checked to resolve once both heads settle.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`), ON A PERFORMED CHECK
  RATHER THAN ON THE MERGE ALONE.** ACT: the
  twin landed AND the cross-citations were re-checked in both directions. UTC
  DATE: 2026-09-08 (the landing); the check was run 2026-09-09 UTC and both heads
  are named. EVIDENCE: the twin merged into OpsxFactory `main` as
  **`bbbef015cd394e2de31586b9718356586c413884`** ("Merge pull request #279 from
  opensoft/change/govern-archived-record-edits", 2026-09-08T15:28:23Z; PR #279 is
  a convenience pointer and the SHA is the identity). The two heads the check was
  taken at: OpsxFactory `origin/main` `bbbef015…` and openxFactory `origin/main`
  `6cc06288`. RESULT: **every cross-citation resolves in both directions** — this
  packet's citations of the twin and of OpsxFactory's `packet-lifecycle-headers`
  convention, `add-pre-archive-citation-gate` and `add-content-address-integrity-gate`;
  and the twin's citations of this packet, of PR #788 → openxFactory `main`
  `3504287a`, and of this packet's ratification record. Tabulated citation by
  citation in the packet evidence file `evidence/realization-2026-09-08.md` §
  *Measurement 3*, which also records the
  two that had MOVED under the packet and still resolve: the integrity-gate change
  lives on an OpsxFactory branch rather than `main`, exactly as this packet says,
  and `add-pre-archive-citation-gate` has since archived into the second path this
  packet deliberately named beside the first.
- [ ] 3.2 **[OpsxFactory]** `add-content-address-integrity-gate`'s family
  register declares a re-derivation rule per family. The second ADDED
  requirement REPORTS an edit whose family has declared no rule — naming the
  family, the target and the home that owes it — and becomes a REFUSAL for that
  family the day it declares. So each family the register leaves undeclared is a
  standing report this packet creates and that register closes, and the day the
  register lands is the day those families' edits start being refused.

  **NOT OWED HERE, and named so it is not silently assumed.** Dated 2026-09-08.
  This is OpsxFactory's act, in OpsxFactory's own change
  `add-content-address-integrity-gate`, whose task 2.1 creates the register file
  `models/content-address-families.yaml`. MEASURED 2026-09-09 UTC at OpsxFactory
  `main` `bbbef015…`: that change is NOT on `main` — it lives on the branch
  `change/add-content-address-integrity-gate` (`cbbe5b48`) — and the register file
  is absent from BOTH, which is what this packet already states. Nothing here
  performs it and nothing here surveys its progress. NOT-OWED-YET rather than
  permanently another's: it is due when that change lands, in that repository.
- [ ] 3.3 The consent family's rule is `add-consent-custody-rederivation-record`'s
  `custody_rederivations[]`, merged 2026-09-08 as `543d47a9`. This packet NAMES
  it and restates none of it. Its contract cut and OpsxFactory's re-pin are that
  packet's tasks, not these.

  **NOT OWED HERE, and named so it is not silently assumed.** Dated 2026-09-08.
  This is ANOTHER openxFactory PACKET'S act:
  `add-consent-custody-rederivation-record`, merged `543d47a9` (PR #774,
  2026-09-07), whose contract cut carries the consent family's
  `custody_rederivations[]` rule. MEASURED 2026-09-09 UTC at openxFactory `main`
  `6cc06288`: that packet is an ACTIVE change carrying **46 unticked boxes and 0
  ticked**, so its rule is proposed and not yet declared. This packet NAMES it and
  restates none of it. NOT-OWED-YET: it is due in that packet, in this repository.
- [x] 3.4 **openxFactory ADOPTS THE NEUTRAL MINIMUM IN ITS OWN DOCS.** The
  first ADDED requirement states a neutral minimum for the bookkeeping note — a
  dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in
  the edited file's own lifecycle-header block. **This repository has no
  archived-packet convention at all**, which is why the minimum exists: an
  earlier spelling delegated the note to "the editing repository's own
  convention", leaving the obligation absent in the very repository promoting
  the rule, with only OpsxFactory having written one down. Record the minimum in
  `docs/document-lifecycle.md` beside the `Status:` / `Ratified by:` header
  rules, as a form the lifecycle header block accepts. A governance document, so
  `code_surface` stays `none`.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the neutral
  minimum is recorded in this repository's own
  lifecycle document. UTC DATE: 2026-09-08. EVIDENCE: commit
  **`645e88ec41c271b002376017e810540f5e1912b1`** ("Adopt the neutral
  bookkeeping-note minimum in the lifecycle document (S1)"), which appends ONE
  top-level bullet at the END of `docs/document-lifecycle.md` § *Status Claim
  Rules* — immediately after the byte-exact-evidence bullet, at line 138, with two
  sub-bullets, in the shape the `govern-openspec-corpus-membership` bullet already
  uses in that section. The note form is quoted BYTE-EXACT (extracted
  programmatically from this packet's own delta rather than retyped, em dash and
  placeholders included, unreflowed on one line as a code span), the bullet says
  the line belongs in the EDITED FILE'S OWN lifecycle-header block and is not the
  authorization for the edit, and its parent prose ends "Ratified by
  `govern-archived-record-edits` (2026-09-08)." The passage records the minimum on
  the ratifying change's authority and says the requirement reaches promoted canon
  at the archive act rather than today. `code_surface` stays `none`: no checker,
  pin, workflow or test was written. Gate 4.4 confirms the adoption moved
  doc-health's finding set by NOTHING (`evidence/realization-2026-09-08.md` § 4.4).
- [ ] 3.5 Every OTHER DomainxFactory reads its own archived-packet convention
  against the first ADDED requirement and amends whatever is looser, by a dated
  amendment keeping the stale text. Named as owed; not surveyed here.

  **NOT OWED HERE, and named so it is not silently assumed.** Dated 2026-09-08.
  This is owed by **every other DomainxFactory, as a class** — not by any named
  repository, because naming one would imply a survey. **NO SURVEY WAS PERFORMED
  HERE and none is implied**: this realization read OpsxFactory only, and only for
  the cross-citation check box 3.1 required. Each such repository amends its own
  convention in its own change, by a dated amendment keeping the stale text, which
  is the form the ratified requirement's last scenario states. NOT-OWED-YET: it
  falls due for each repository as it reads its own convention against the
  promoted requirement.

## 4. Gates

**PINNED-TARGET NOTE, dated 2026-09-08 and added by this change's realization
(lane `opsXfactory-1`).** The second ADDED requirement's re-derivation obligation
is discharged for every file this realization edits, as a MEASUREMENT rather than
an assumption: **no IN-REPO `sha256` pin names `docs/document-lifecycle.md`,
measured at base `68712924`.** "In-repo" is load-bearing — task 1.2a's ratified
scope is in-repo pointers to in-repo targets, and a broader claim would overstate
what was measured; nothing here is a claim about a pin held in a consuming
repository. Method and full working, including the FIVE files that name the path
and why none of them is a pin, are in the packet evidence file
`evidence/realization-2026-09-08.md`
§ *Measurement 1*; the measurement is re-taken at the branch's final head, because
a pin arriving with a forward merge is a pin.

- [x] 4.1 `python3 scripts/validate-openspec-cli-pin.py --change openspec/changes/govern-archived-record-edits --strict`
  and `--all --strict` with no undispositioned finding.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: both runs
  performed through the pinned-CLI entrypoint with
  `@fission-ai/openspec@1.12.0` on `PATH` (PATH's 1.2.0 never used). UTC DATE:
  2026-09-08. EVIDENCE: `evidence/realization-2026-09-08.md` § 4.1, which
  carries the exact command text with its
  environment, the pinned CLI's verified provenance, both return codes and both
  summary lines, and the dispositioned-exception count compared with the
  ratification record's baseline in BOTH directions. Result recorded there:
  `--change` rc 0, `--all --strict` rc 0 with **ZERO UNDISPOSITIONED** findings.
- [x] 4.2 **Currency of the MODIFIED block, continuously until archive.**
  `A MODIFIED requirement block restates the requirement as canon currently
  states it` attaches for as long as this change is active. Re-run the
  byte-identity check against `openspec/specs/document-lifecycle/spec.md` before
  archive and bring the block forward if canon moved.

  **RUN, RECORDED, AND DELIBERATELY LEFT OPEN FOR THE ARCHIVE ACT.** Dated
  2026-09-08. The check WAS run and its result IS recorded —
  `evidence/realization-2026-09-08.md`
  § *Measurement 2*: canon 5,815 characters, **0 canon lines removed**, the
  difference entirely inserted, re-taken at the branch's final head. **THE BOX IS
  NOT TICKED, AND THAT IS THE POINT**: this requirement demands currency
  CONTINUOUSLY until archive, so a realization tick would retire the clearance
  signal the `modified-block-currency` family exists to keep live, and the archive
  act would inherit a ticked box instead of an obligation. Evidence without a tick
  is permitted; a tick without evidence is not, and this box is the former.

  **TICKED 2026-09-09 AT THE ARCHIVE ACT (`archive-govern-archived-record-edits`,
  lane `opsXfactory-1`) — THE RE-RUN THIS BOX WAS HELD OPEN FOR, AND IT IS A
  RE-RUN RATHER THAN AN INHERITANCE.** ACT: the byte-identity check re-run
  against `openspec/specs/document-lifecycle/spec.md` at base `9a67d42c`,
  immediately before the move and not after it. UTC DATE: 2026-09-09.
  EVIDENCE, verbatim from the run: **canon 5,815 characters**, delta **7,209**
  (the quickstart script's own `\n### Requirement:` bound) / **7,186** (bounded
  at `## ADDED Requirements`), **0 canon lines removed** under BOTH bounds, 17
  and 15 lines added respectively. **CANON DID NOT MOVE.** The figure is
  character-for-character the one `evidence/realization-2026-09-08.md`
  § *Measurement 2* recorded on 2026-09-08 and the one the README row states, so
  the MODIFIED block is carried forward AS RATIFIED and **no re-derivation is
  owed** — had canon moved, this box would have stopped the archive rather than
  been brought forward inside it. **THE PROMOTION IS THEN VERIFIED IN THE OTHER
  DIRECTION TOO**, after the move: all three delta blocks are byte-identical to
  the blocks the archive wrote into canon, extracted programmatically and
  compared rather than eyeballed (§ 6.2).
- [x] 4.3 `python3 scripts/validate-sequenced-after.py .`, `--ledger-diff`,
  `validate-scope-globs.py .`, `validate-manifest-digests.py .` all clean.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: all four
  validators run. UTC DATE: 2026-09-08. EVIDENCE:
  `evidence/realization-2026-09-08.md` § 4.3, which records each command, its
  return code and its summary line
  verbatim; all four exit **rc 0**, `--ledger-diff` reporting `per-change sweep
  ledger consistent with the corpus`.
- [x] 4.4 `python3 scripts/doc-health.py --single-repo . --fail-on error` with
  the finding set diff-identical to `main`'s.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: doc-health run
  on the branch and its FINDING SET diffed
  against `main`'s. UTC DATE: 2026-09-08. EVIDENCE:
  `evidence/realization-2026-09-08.md` § 4.4, which records the
  identity-safe recipe (both baseline checkouts carry the branch checkout's own
  directory basename, because doc-health stamps that basename into every finding
  line; `--previous-report` never used), the main-vs-main PROOF at zero
  differences taken before the comparison was trusted, the baseline's named `main`
  sha `68712924`, and one superseded interim run struck rather than deleted.
  Result recorded there: **the finding set is IDENTICAL** — zero differing finding
  lines, headline unchanged at 10 critical / 9 error / 55 warning / 16 info. The
  only differing lines are word totals that moved because the document GREW by 199
  words, which the evidence file states separately and does not count as findings.
- [x] 4.5 `pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q`
  green.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the three test
  paths run. UTC DATE: 2026-09-08. EVIDENCE:
  `evidence/realization-2026-09-08.md` § 4.5 — **rc 0** captured as a return
  code rather than inferred from a
  pipeline, summary `330 passed, 2 subtests passed`.

## 5. Bookkeeping and landing

- [x] 5.1 One row in README's "OpenSpec Records" block in the neighbours' DRAFT
  form; re-derive at the union if another lane's substrate claim lands first
  (Rule 7). Note `main` moves hourly here: merge forward, never rebase pushed
  commits.

  **TICKED 2026-09-08 by this change's realization
  (`govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the row is
  written and landed with PR #788. UTC DATE:
  2026-09-08. EVIDENCE: `README.md:659` carries this change's "OpenSpec Records"
  row on openxFactory `main`. It is not re-authored here; realization appends ONE
  dated superseding sentence at the END of that row, because that row makes the
  now-false claim TWICE — once at `README.md:671` ("all 28 boxes in `tasks.md`
  stay unticked, § 1's ratification boxes included") and again at
  `README.md:689-692` ("**NOTHING IS REALIZED** … and **all 28 boxes in
  `tasks.md` stay unticked**") — and this file falsifies BOTH: 19 boxes are
  ticked, and `docs/document-lifecycle.md` IS amended, so "NOTHING IS REALIZED"
  is false in its own right and not only in its box clause. The single appended
  amendment block-quotes both. **The Rule 7 union
  re-derivation, if another lane's substrate claim lands first, is the LANE'S act
  at landing and is not performed here.**
- [ ] 5.2 Rule 6 LANDING notice on the PR and in `LANES.md` before merging into
  `main`; LANDED with the merge sha after.

  **NOT OWED HERE, and named so it is not silently assumed.** Dated 2026-09-08.
  This is **lane `opsXfactory-1`'s** act, not this realization's: the realization
  opens no pull request, posts no comment on any GitHub surface, and performs no
  merge. The LANDING notice and the LANDED sha follow the lane's own landing
  window.
- [ ] 5.3 Discharge the object and substrate claims on openxFactory issue #630
  naming the PR and the merge sha.

  **NOT OWED HERE, and named so it is not silently assumed.** Dated 2026-09-08.
  This is **lane `opsXfactory-1`'s** act. The claim on issue #630 was made by the
  lane before this branch existed and covers this authoring; discharging it names
  a PR and a merge sha that do not exist yet, and posting it would be a GitHub
  comment this realization does not make.

## 6. Archive

- [x] 6.1 **Archive WHEN ITS ARTIFACTS LAND**, per `release-realization`: the
  declared `code_surface` is `none`, so the archive gate is not merged-plus-green
  realization evidence. **This box said "nothing in § 3 gates it: those are
  other packets' acts", and § 3 holds THREE different kinds of act, not one.**
  3.1, 3.2 and 3.5 are OTHER REPOSITORIES' acts, all OpsxFactory's or a further
  DomainxFactory's. **3.3 is ANOTHER PACKET'S ACT IN THIS REPOSITORY** —
  `add-consent-custody-rederivation-record` is an ACTIVE openxFactory change
  (untagged, per the Tags note above; `543d47a9` resolves in this tree), so its
  contract cut is owed here even though its consumer re-pin is OpsxFactory's.
  **3.4 is THIS PACKET'S OWN act in this repository**: adopting the neutral
  minimum in `docs/document-lifecycle.md`. Only the last of the three can hold
  this packet open, and it does — what the archive act reads is the UNTICKED BOX
  3.4, with 3.1/3.2/3.3/3.5 named beside it for the chain's readability and
  gating nothing here.

  **AMENDED 2026-09-08 by this change's realization; the superseded clause is
  quoted rather than rewritten.** This box states:

  > what the archive act reads is the UNTICKED BOX 3.4

  That is SUPERSEDED: box 3.4 IS NOW TICKED, on commit `645e88ec`, so what the
  archive act reads there is a box whose act is done. **NOT superseded, and
  still exactly right:** the reasoning around it — that § 3 holds three
  different kinds of act, that "Only the last of the three can hold this packet
  open", and that 3.1/3.2/3.3/3.5 are named beside it "for the chain's
  readability and gating nothing here". The box was the gate; the gate is now
  clear. (Caught by the `grep -n -i untick` re-derivation over the packet rather
  than by reading, which is why that sweep is run.)

  **NOT OWED HERE — THE ARCHIVE ACT IS THE LANE'S.** Dated 2026-09-08. The
  realization runs no `openspec archive`. **WHAT IT DID DO IS CLEAR THIS BOX'S
  GATE**: the box this one names as holding the packet open — 3.4 — IS NOW TICKED
  above, so the condition this box waits on is met and the archive act is
  unblocked on that ground. 3.1 is ticked too; 3.2, 3.3 and 3.5 remain other
  repositories' or other packets' acts and gate nothing here, exactly as this box
  says.

  **TICKED 2026-09-09 ON THE DOING, AT THE ARCHIVE ACT
  (`archive-govern-archived-record-edits`, lane `opsXfactory-1`).** ACT: the
  archive is TAKEN IN THIS PULL REQUEST, in the commit after this one, by
  `openspec archive govern-archived-record-edits --yes` run through the PINNED
  CLI `@fission-ai/openspec@1.12.0` with `OPENSPEC_TELEMETRY=0` from the
  repository root — never `PATH`'s 1.2.0. UTC DATE: 2026-09-09. EVIDENCE: the
  packet moves to
  `openspec/changes/archive/2026-09-09-govern-archived-record-edits/` and the CLI
  reports `added 2, modified 1, removed 0, renamed 0`, `specsUpdated: true`.
  **THE GATE THIS BOX NAMES IS RE-READ AT THIS COMMIT AND IS CLEAR**:
  `code_surface: none`, so `release-realization` archives this packet ON LANDING;
  box 3.4 — the only § 3 box that could hold it open, and this repository's own
  act — is ticked; the THREE remaining § 3 boxes (3.2, 3.3, 3.5) and the two § 5
  boxes (5.2, 5.3) are other repositories', other packets' or the LANDING LANE's
  acts and gate nothing here, exactly as this box's own text says. **THE ARCHIVE
  DATE IS UTC AND AGREES WITH THE CLOCK THE ESTATE READS**: the CLI stamps the
  directory from the LOCAL clock (it has no date option — the trap `#790`
  recorded), and the run was made at 2026-09-09 ~02:1x local = ~06:1xZ, so both
  clocks read 2026-09-09 and the directory needs no correction.
- [x] 6.2 Confirm at the archive act that the three requirement blocks reach
  `openspec/specs/document-lifecycle/spec.md` — *Ratified spec deltas reach the
  promoted specification* is checked against the archived delta's own bytes,
  which is the reason this packet exists.

  **NOT OWED HERE — THE ARCHIVE ACT IS THE LANE'S.** Dated 2026-09-08. This
  confirmation is performed AT the archive act, against the archived delta's own
  bytes, and cannot be performed before it. What this realization contributes is
  the input: box 4.2's currency measurement is run and recorded
  (`evidence/realization-2026-09-08.md`
  § *Measurement 2*) and its box is deliberately left open so the archive act
  re-runs it rather than inheriting a tick.

  **TICKED 2026-09-09 AT THE ARCHIVE ACT (`archive-govern-archived-record-edits`,
  lane `opsXfactory-1`) — THE CONFIRMATION IS PERFORMED, NOT PROMISED, AND IT IS
  MEASURED AGAINST THE ARCHIVED DELTA'S OWN BYTES.** ACT: after the move, all
  three requirement blocks were extracted PROGRAMMATICALLY from the archived
  delta at
  `openspec/changes/archive/2026-09-09-govern-archived-record-edits/specs/document-lifecycle/spec.md`
  and from the promoted `openspec/specs/document-lifecycle/spec.md`, and compared
  as strings — never read side by side. UTC DATE: 2026-09-09. EVIDENCE:

  - *Proposal packets carry the lifecycle header* (the `## MODIFIED`) — the
    promoted block is **byte-identical** to the archived delta's block. The
    requirement is replaced WHOLESALE, as `openspec`'s MODIFIED semantics
    require. **ITS SEVEN SCENARIOS ARE ALL PRESENT, AND CANON'S SIX ARE ALL
    AMONG THEM, BYTE-IDENTICAL** — the seventh, *A header defect is discharged
    on an archived packet*, is the block's one addition. A MODIFIED delta
    REPLACES the named requirement wholesale, so a scenario it failed to restate
    would be a scenario silently deleted from canon; none is.
  - *An archived record is edited only as a bookkeeping correction under a
    recorded ruling* (`## ADDED`) — **byte-identical**, appended.
  - *A change that edits a pinned target re-derives every dependent pin in the
    same change* (`## ADDED`) — **byte-identical**, appended.

  **AND NOT ONE OTHER REQUIREMENT MOVED.** The capability goes **18 → 20**
  requirements; the 17 the delta does not name are byte-identical before and
  after; nothing is REMOVED, so no ``**Removed from canon by …**`` marker is
  owed. The file's whole diff is **+238 / −0** lines, and the ONLY change outside
  the three blocks is a single blank line the CLI's serializer inserts before
  `## Requirements` — the same normalization
  `refresh-install-repository-enumerations` took at its archive
  (`ca4a1558`, hunk `@@ -4,7 +4,9 @@`). **THIS IS THE REASON THIS PACKET
  EXISTS**: *Ratified spec deltas reach the promoted specification* is checked
  against the ARCHIVED delta's bytes, so those bytes are now canon's authority,
  and the requirement promoted one commit earlier is what forbids editing them.
- [ ] 6.3 [OPERATOR] The archive word.

  **NOT OWED HERE — ONLY BRETT HEAP GIVES IT.** Dated 2026-09-08. No approval,
  ruling or word is read out of the ratification for this: the 2026-09-08
  approval ratified the packet and is not an archive word. This realization
  neither gives it nor asks for it, and ticks nothing against it.

  **STILL NOT OWED, AND STILL NOT TICKED — RE-READ 2026-09-09 AT THE ARCHIVE ACT
  (`archive-govern-archived-record-edits`, lane `opsXfactory-1`), WHICH IS THE
  ONE BOX THIS ACT LEAVES OPEN AND SAYS SO RATHER THAN CLOSING IT QUIETLY.** The
  archive act searched for a recorded archive word and **FOUND NONE**: the
  governing issue [#630](https://github.com/opensoft/openxFactory/issues/630)
  carries the lane's own CLAIM of the archive act (comment `5596604879`,
  2026-09-09T06:01:38Z) and its correction, and NO word of Brett Heap's
  authorizing it; the 2026-09-08 approval on PR #788 ratified the packet and this
  box already refuses to read an archive word out of it. **A LANE'S DISPATCH IS
  NOT THE OPERATOR'S WORD**, and inventing one here would be exactly the
  fabricated provenance the MODIFIED requirement above forbids. **WHAT WOULD
  DISCHARGE IT, NAMED SO IT IS NOT GUESSED AT:** Brett Heap's approval of THIS
  archive pull request, or a separate word of his recorded on a citable surface —
  the shape `refresh-install-repository-enumerations` had, whose archive ran on a
  word verbatim *"archive refresh-install-repository-enumerations"* recorded on
  openxFactory #591 and distinct from its ratifying word. **THE PACKET THEREFORE
  ARCHIVES WITH ONE OPEN BOX AND THE OPENNESS IS THE RECORD**: the merge of this
  pull request cannot happen without his approval, so the word arrives before the
  archive lands even though it does not exist at this commit — and the landing
  lane owes the tick, as a header/bookkeeping edit of an archived file under the
  ruling that approval IS, carrying the neutral minimum, or a successor change
  records it. Neither is claimed here.
