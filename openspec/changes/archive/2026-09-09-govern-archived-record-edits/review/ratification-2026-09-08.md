# Proposal Ratification: govern-archived-record-edits

Status: ratified
Kind: report
Decision date: 2026-09-08
Ratifier: Brett Heap (reviewer of record; openxFactory operator authority) — in session
Ratified: 2026-09-08 by Brett Heap (reviewer of record) — in session, first-hand
to lane `opsXfactory-1` (harness session `ee808615-4d8a-475f-bcb3-6f92a89909f0`,
`session_01SdF4BiCNseq3B2HFzkN3SJ`), by CLI approval
`gh pr review 788 --repo opensoft/openxFactory --approve` on openxFactory pull
request [#788](https://github.com/opensoft/openxFactory/pull/788) — GitHub
review id **5141756427**, state **APPROVED**, submitted **2026-09-08T12:38:36Z**
by `brettheap`, **with an empty body**; this record.

**THE APPROVAL CARRIES NO WORDS, AND THIS RECORD DOES NOT INVENT ANY.** The
sibling packet's ratification quoted a verbatim sentence because one was spoken.
Here the act is a CLI approval with a zero-length body, so what is recorded is
the ACT and its API-verifiable identity, not a reconstructed phrase. The
`Ratified:` header above therefore names an approver, a date and a resolvable
record, which is the three-way floor the `document-lifecycle` citation rule sets
for this spelling.

Ratified baseline: this change as committed at
**`8cc76e1b0833908b544b31ce27520d735ccda46a`** — `proposal.md`, `design.md`,
`tasks.md`, `.openspec.yaml` and `specs/document-lifecycle/spec.md`, five files
and no others. The delta is **ONE `## MODIFIED` and TWO `## ADDED` requirements,
18 scenarios** (7 + 5 + 6), no `## REMOVED` and no `## RENAMED`. `design.md`
carries **EIGHT decisions** — D-1 through D-8 — plus **FIVE readings not taken**.
`tasks.md` carries **28 boxes, NONE ticked**. The change's row in
`tests/sequenced_after/corpus-ledger.yaml` reads
`{state: active, class: co-modifier, declares: [govern-openspec-corpus-membership],
depth: 1, prose: false, moved_by: "#788"}`. Validated strict through the pinned
entrypoint (`scripts/validate-openspec-cli-pin.py`,
`@fission-ai/openspec@1.12.0` verified against its content address) at this
baseline.

**THE BASELINE IS CARRIED UNCHANGED INTO THE MERGE COMMIT, AND THAT IS MEASURED
RATHER THAN ASSERTED.** `git diff 8cc76e1b d0f8cccf --
openspec/changes/govern-archived-record-edits/` is **EMPTY**. `d0f8cccf` is a
`--no-ff` merge of `origin/main` at `e8021fed` taken before landing; it moves no
byte of this packet.

**ONE DISCREPANCY IN THE APPROVAL'S OWN RECORD, STATED RATHER THAN SMOOTHED.**
The GitHub API reports the review's `commit_id` as **`d0f8cccf`** while its
`submitted_at` is `2026-09-08T12:38:36Z`, and `d0f8cccf`'s committer date is
`2026-09-08T12:39:58Z` — the merge appears to be ~82 seconds LATER than the
approval that names it. The lane's own account is that the head at the moment of
approval was `8cc76e1b`. This record does not resolve which clock is right,
because it does not have to: **the packet's bytes are identical at both heads**,
by the measurement above, so the ratified TEXT is the same whichever head the
approval is read against. The discrepancy is recorded so that a later reader
finds it already noticed rather than appearing to have been missed.

## Decision

**ONE ACT, NOT TWO.** The sibling packet's word had two clauses and its record
split them; this one has a single act and this record says so rather than
manufacturing a symmetry:

- **THE APPROVAL IS THE RATIFICATION.** It approves the packet's text as
  committed at `8cc76e1b`: the three requirement blocks, the eight decisions and
  the task list as written.
- **THE LANDING IS THE LANE'S ACT, under Brett Heap's STANDING authorization to
  land ruled successors** — it is NOT part of this approval and is not read out
  of it. Nothing in the approval ticks a task, promotes a delta, amends a
  convention or reaches any consumer repository. What landing puts on `main` is
  a ratified PROPOSAL.

**RATIFICATION HYGIENE — WITNESSED AND RECORDED BY THE SAME LANE, NOTHING
RELAYED.** The approval was run by Brett Heap from the CLI in the harness
session named in the header, and this record is written by that same lane from
that same session. No intermediary carried it. The API fields above are
independently checkable by anyone with the repository.

## What was ratified, and the three vetoes that were NOT exercised

Immediately before the approval, in the same session, the lane put the packet's
three open decisions to him in these terms:

> "pin scope (every declared family, or custody pins only), the no-rule
> consequence (report until the family declares, refuse from landing, or
> strike), and the one-vs-two ADDED split against your 'one ADDED'. Each choice
> forces the OpsxFactory twin to move the same way."

**He approved without exercising any of the three, so the packet is ratified AS
WRITTEN and the defaults stand:**

- **PIN SCOPE — every pin of every declared family.** The narrower CUSTODY PINS
  ONLY reading, which matches his 2026-09-06 wording exactly, is NOT taken. The
  basis for the width is his own 2026-09-07 restatement, which drops the
  qualifier, read with his F.2 scope selection of the same day — *"Every in-repo
  sha256 pointer to an in-repo target"*.
- **THE NO-RULE CONSEQUENCE — REPORT-THEN-REFUSE.** An edit whose pin family has
  declared no re-derivation rule is REPORTED, naming the family, the target and
  the register or neutral contract that owes the rule, and becomes a REFUSAL for
  that family the day that family declares. REFUSE FROM LANDING is not taken;
  STRIKE is not taken.
- **THE SPLIT — TWO `## ADDED` REQUIREMENTS.** His F.3 wording named "an ADDED
  requirement", singular. The split stands, on the measured ground that the two
  failures are invisible to each other: one of the three custody pins the
  motivating commit broke names a target in a change directory that has never
  been archived, so a single archive-scoped requirement would report itself
  satisfied while that pin stayed broken.

Every one of the eight decisions D-1..D-8 likewise stands as recommended, and
the five readings recorded as NOT taken stay not taken: a strict read-only
archive; keeping OpsxFactory's convention as the whole governance; enforcing via
the bookkeeping note alone; a new small capability; and leaving the promoted
`## Purpose` sentence unnarrowed.

## What this ratification authorizes

- **The 28 realization tasks, as a LATER and SEPARATELY CLAIMED act.** They are
  not performed by this approval and not performed by landing #788. Every box
  stays unticked on `main`.
- **The landing of #788** — by the lane, under standing authorization, not by
  this approval.
- **The domain twin's ratification as a SEPARATE act.** OpsxFactory's
  `govern-archived-record-edits` states the same rule at its own altitude and is
  ratified in that repository, on its own PR. This word reaches it only through
  the lockstep the three vetoes named: had any been exercised here, that half
  would have had to move the same way.

## What this ratification does NOT authorize

- **No document is edited by this record.** `docs/document-lifecycle.md` is
  untouched and the neutral minimum is not yet adopted there (task 3.4).
- **No archived byte is edited**, including under the rule this packet states.
- **No pin is re-derived**, no family register is authored, and no checker is
  written — detection remains OpsxFactory's citation gate and its proposed
  `add-content-address-integrity-gate`.
- **No spec delta is promoted.** Promotion happens at the archive act, which is
  a later act with its own gate.
- **No task is ticked.** 28 of 28 remain open, § 1's ratification boxes included
  — the sibling packet did the same, and for the same reason: a half-ticked list
  would say the packet had begun.

## Ratified requirements text, by heading

`specs/document-lifecycle/spec.md`:

- `## MODIFIED Requirements` → **Proposal packets carry the lifecycle header** —
  restated against promoted canon with **every canon byte carried verbatim**
  (canon 5,815 chars, delta 7,186, **1,371 inserted, 0 canon lines removed**,
  all six promoted scenarios restated), grown by TWO PURE INSERTIONS: a
  paragraph naming the route its own text had dangled since 2026-08-24
  ("takes the route archived-record edits take"), and one added scenario, *A
  header defect is discharged on an archived packet*.
- `## ADDED Requirements` → **An archived record is edited only as a bookkeeping
  correction under a recorded ruling** — the route. The bookkeeping class defined
  BY EFFECT rather than by a list of filenames; the ruling recorded BEFORE the
  edit; the note explicitly not the authorization; and the NEUTRAL MINIMUM,
  a dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line
  in the edited file's own lifecycle-header block, which a local convention may
  add to and may not fall below.
- `## ADDED Requirements` → **A change that edits a pinned target re-derives
  every dependent pin in the same change** — archived OR live, per family, by
  the rule the family declares in its content-address register or in the neutral
  contract that owns it, with the report-then-refuse transition above and the
  cross-boundary deferral rule.

## The review this record rests on

**SIX adversarial rounds preceded the approval**, each landing on this branch
before the next was run. **No round was clean**, and — measured across all six —
**every finding after round 1 was the same class: a fix applied to one half of
the matched pair and not mirrored to the other.**

| Round | Head | Found |
| --- | --- | --- |
| 1 | `d600b020` | The first packet. |
| 2 | `f318b5d3` | **G1 MAJOR** — the no-rule refusal would have frozen every pinned-target edit in the estate on landing; plus G2–G8 (archive-path hedge, provisional `moved_by`, missing merge trailers, a mislabelled character count, a homeless contract rule, an overstated discharge, an unclocked "same day"). |
| 3 | `c4a66eee` | **J1–J6** — the refusal posture surviving in four more places; a measurably wrong re-stamp procedure; an asserted archive path; and **J4**, the note obligation delegated to a convention openxFactory does not have. |
| 4 | `2b012bee` | **L5–L7, L10–L12** — the twin's veto boxes absent here; the transition 33 lines from its claim; the minimum written as substitutable. |
| 5 | `674f4b42` | **M2** — an archive-gate sentence falsified by this packet's own later addition. |
| 6 | `97d1e7fa` | **N1** — the round-5 correction itself over-claimed, filing an openxFactory obligation under another repository's name. |

`8cc76e1b` re-stamped the sweep-ledger row from a provisional `#785` — a guess
at this packet's pull-request number, which another lane's PR then took — to the
real `#788`, by a direct one-field edit after the seeder was MEASURED to be a
no-op for a provenance-only correction.

**Gates at the ratified baseline:** pinned CLI `--change … --strict` 1 passed /
0 failed and `--all --strict` 99 passed / 2 failed with 0 UNDISPOSITIONED (two
pre-existing accepted exceptions); MODIFIED-block currency 0 canon lines
removed; `validate-sequenced-after` 41 active changes and `--ledger-diff`
consistent at 184 rows; `validate-scope-globs` pass; `validate-manifest-digests`
188 digests verify; doc-health finding set diff-identical to `main`; `pytest
tests/sequenced_after tests/proposal-support tests/scope_globs` 330 passed.
