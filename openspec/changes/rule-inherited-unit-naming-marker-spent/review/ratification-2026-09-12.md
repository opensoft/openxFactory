# Proposal Ratification: rule-inherited-unit-naming-marker-spent

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-12 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"do all as
recomended"*, given in the lane's window in answer to a list of open rulings
each put with its recommendation first (`design.md` **D1** among them), and
recorded on openxFactory PR
[#962](https://github.com/opensoft/openxFactory/pull/962#issuecomment-5646922185)
at **2026-09-12T15:45:16Z** (comment `5646922185`). **D1 = Option 1, "Ratify
as encoded"** — the block as frozen at `51edde81` (the five added carriage
sentences, the LIMIT sentence, and the two scenarios *A later block drops an
inherited unit-naming marker* / *A later block carries an inherited
unit-naming marker forward*) is the ratified text; option 2 (a third
suppression option, a code surface) is NOT taken. **D2b = no marker owed**,
confirmed rather than chosen — an added sentence retires no unit
(`derive_units`: 0 uncarried). **THE OPTION TAKEN IS THE PACKET'S OWN
RECOMMENDATION, SO THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS
SUBSTITUTED, RESTORED OR DELETED.**

**THIS RATIFICATION IS SEPARATE FROM, AND LATER THAN, THE WORD THAT
COMMISSIONED THE AUTHORING.** Brett Heap's earlier word of 2026-09-11 at
12:08:24Z, verbatim *"land each when green, archive both when landed, claim
955 and 956"*, recorded on openxFactory
[#955](https://github.com/opensoft/openxFactory/issues/955), directed this
lane to CLAIM the issue — it decided no sentence, no scenario and no scoping,
none of which existed when it was given, and it is not read as an approval.
It stays recorded as the ORIGIN of the AUTHORING in `proposal.md`'s
`Proposed:` line, in `.openspec.yaml`'s `proposed_by`, and in `tasks.md`
§ 1.1.

Ratified baseline: this change as committed on the branch
`change/rule-inherited-unit-naming-marker-spent` at the frozen head
**`51edde81`** (full `51edde817930c9c584a4c6a585305019fc78aee2`) —
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE `## MODIFIED` requirement**, *Currency of an
active change's MODIFIED requirement blocks*, a PURE ADDITION of five
carriage sentences and two scenarios over its ordered-delta parent's outcome,
naming no new marker and dropping the parent's inherited one under the rule
the block itself writes). Between that freeze and this ratification the
branch took FIVE commits, none of them touching the delta's own `specs/`
directory (verified below, § 4): two merges of `origin/main` (`67b8011f`,
then `78a5d2dc` after a second corpus move mid-encode), a per-change
sweep-ledger re-seed (`b42eb65d`), a self-gate fix made necessary by the
first merge (`396bca94`, § 5), and this ratification commit itself.

## 1. The two words, and exactly what each decided

### 1.1 The origin word — given and recorded 2026-09-11T12:08:24Z

Brett Heap, 2026-09-11, verbatim:

> land each when green, archive both when landed, claim 955 and 956

Recorded on openxFactory issue #955. **THIS WORD COMMISSIONED THE AUTHORING
AND SETTLED NOTHING OF `design.md`'s CONTENT.** It directed this lane to claim
the issue; no sentence, no scenario and no scoping existed when it was given.
The packet was therefore authored as a `Status: draft` proposal with no
approval pair, the lawful unapproved shape `add-drafted-proposal-origin`
(issue #318) defined, and `design.md` recorded **D1** (the wording) as the
veto point that could end the packet, put as a multiple choice with the
recommendation first, and **D2b** (the marker) as decided by measurement
rather than preference.

### 1.2 The ratifying word — given and recorded 2026-09-12T15:45:16Z

Brett Heap, 2026-09-12, verbatim:

> do all as recomended

A multiple-choice ruling given in the lane's window in answer to a list of
open rulings across several packets this lane held, each put with its
recommendation first — `design.md` D1 among them, presented as: **"Option 1
(recommended, encoded): rule the two-option state correct in five sentences
and two scenarios, no code surface"** vs. **"Option 2: add a third
option — a suppression, a code surface — which would re-author the
packet."** **THIS IS THE FIRST WORD TO REACH THE PACKET'S CONTENT.** It
ratifies the packet — `.openspec.yaml` gains the approval pair, every
status-bearing document flips to `Status: ratified` — and it takes the
recommended option, so **THE RULING IS APPLIED BY LEAVING THE TEXT ALONE**,
verified by diff rather than asserted (§ 4).

## 2. D1 as it was put, and D1 as it is resolved

### What was on the table

`design.md` D1 — **the veto point: the wording, and the code surface it is
not**:

- **OPTION 1 (RECOMMENDED, and what the delta encodes).** Five sentences
  added to the carriage paragraph that already rules a marker no carriage
  unit — a unit-naming marker is SPENT once EVERY unit it names has left
  canon by a declared act, so dropping it is the lawful carriage and a
  third-ground report on a carried one is the class working as written — plus
  two scenarios, one per half of the rule. No ground added, no suppression
  moved, no code, archives on landing.
- **OPTION 2 — add a THIRD option**: a suppression for an inherited marker
  every one of whose named units left canon by a declared act, resolvable
  against the archived delta that declared it. One predicate, one `_WHY_*`
  template, its own scenario, a CODE SURFACE in `scripts/doc_health/` plus
  `tests/doc-health/`, a checker basis widened to a third document class, a
  fail-OPEN direction, and an archive rule of merged-plus-green. Written out
  in `design.md` D1 with its cost; **if taken, the packet is RE-AUTHORED, not
  amended.**

### The resolution

**OPTION 1.** The recommended and already-encoded option, so the ruling is
applied **by leaving the text alone**. A veto to option 2 would have cost the
five added sentences and the two scenarios and left the block a pure
carriage-rule restatement with no wording move; none of that was performed.
The five sentences and two scenarios are ratified **exactly as the bench
reviewed them**, verified by diff rather than asserted:
`git diff --name-only 51edde81 -- .../specs/doc-health/spec.md` is **EMPTY**
(§ 4).

## 3. D2b as it was put, and D2b as it is resolved

### What was on the table

`design.md` D2b — **the inherited marker: dropped, and decided by measurement
rather than by preference**:

- **DROP the parent's inherited `Removed from canon` marker (encoded)** —
  under the rule this block itself writes: a marker is not a carriage unit in
  either direction, and the durable record of the parent's deletion is the
  parent's own archived delta.
- **CARRY the marker forward instead (the counterfactual, not encoded)** —
  which `design.md` D2b's own table measures at exactly one third-ground
  marker defect against the parent's outcome (the basis canon now carries,
  the parent having archived), against zero for the drop.

### The resolution

**THE MARKER STAYS DROPPED, AS WRITTEN.** Brett Heap's word did not re-derive
the counts; it confirmed them as measured at authoring and re-measured across
both merges: this block carries **0 markers**, `derive_units` reads **0
canon units uncarried** by this amendment, and no `Removed from canon` marker
is owed or written. The one transient `info` carriage-ledger finding this
amendment's basis-override gap opened while the parent was off `main` (D2b's
own disclosed cost) has since cleared on the parent's own archive — event
(b) of the two D2b named, not event (a) — independent of this ratification
(§ 5).

## 4. THE RATIFIED SURFACE — verified by diff, not by assertion

Diffed against `51edde81`, the frozen content the word was given on (five
commits sit between that head and this ratification — merges, a ledger
re-seed, a self-gate fix, and this encode itself; none of them touching this
packet's own delta):

| surface | command | result |
| --- | --- | --- |
| the ratified delta | `git diff --name-only 51edde81 -- openspec/changes/rule-inherited-unit-naming-marker-spent/specs/` | **EMPTY** |
| `.openspec.yaml` | `git diff --numstat 51edde81 -- .../.openspec.yaml` | **`37  0`** — thirty-seven lines ADDED, zero removed |
| the promoted requirement this block writes over | `git diff --stat 51edde81 -- openspec/specs/doc-health/spec.md` | **NOT empty** — 95 insertions/34 deletions, but from TWO OTHER packets' own archive/realization commits carried in by the merges (`99f70e6e` archiving the parent `amend-merged-into-empty-tail-standing`, `bc1f25c4` archiving `honour-grandfather-dispositions-in-ratified-provenance`), neither of them this ratification's own edit — exactly the ordered-delta scenario this packet is written for |
| the predicate this delta cites | `git diff --stat 51edde81 -- scripts/doc_health/modified_block_currency.py` | **NOT empty** — two commits (`429f78cf`, `fc4629a9`), both the parent's own realization of its ruled wording, carried in by the merge; not this packet's edit |

**ONE `## MODIFIED` REQUIREMENT, FIVE ADDED CARRIAGE SENTENCES, TWO ADDED
SCENARIOS, ZERO MARKERS.** No promoted scenario moves, is retitled or loses a
bullet; no ground is added or withdrawn; no severity, threshold, arm, parse
or marker grammar moves; no code moves by this ratification.

## 5. What this encode also did, and why it is not a second ruling

**TWO MERGES OF `origin/main` WERE OWED AND TAKEN**, `main` having moved
twice since the freeze: first to `1f068646` (67b8011f), then to `5972c8f3`
after PR #1004 landed mid-encode (`78a5d2dc`). Both resolved a `README.md ##
OpenSpec Records` conflict by keeping BOTH rows in play (this packet's own
plus the other lane's), never dropping either.

**THE FIRST MERGE MADE THE PARENT'S ARCHIVE (PR #973) RESOLVABLE, WHICH
RE-SEEDED THE LEDGER AND RETIRED A TRANSIENT TEST ROW — NEITHER OF THESE IS A
RULING.** `tests/sequenced_after/corpus-ledger.yaml`'s row for this change was
re-seeded with the sanctioned tool (`--seed-ledger --moved-by '#962'`, commit
`b42eb65d`: `depth` 0 → 1, the parent now resolvable). Separately,
`design.md` D2b's own disclosed transient finding — the `info` carriage-ledger
row this amendment's basis-override gap opened while the parent was off
`main` — cleared the moment the parent's archive reached the active corpus,
which fired `tests/doc-health/test_modified_block_currency_self_gate.py`'s
exact-set assertion (`_LEDGER_SUBJECTS`): the row this packet had named at
authoring was no longer among the family's reported subjects. This is
D2b's own stated mechanism (event (b), the parent archiving, "needs nothing
of this packet at all") arriving exactly as designed, not a new decision —
fixed at commit `396bca94` by removing the retired row and recording the
retirement in the module's own established convention, the same one every
other retired row in that file already uses. Full detail:
`review/verification-2026-09-12.md`.

## 6. The bench, on the frozen head, and what it settled before either word arrived

**TWENTY-ONE THREADS ACROSS EIGHT COPILOT ROUNDS, ALL TWENTY-ONE TAKEN, ZERO
UNRESOLVED** — the full round-by-round table is this lane's own FREEZE
comment on PR #962
([issuecomment-5636697848](https://github.com/opensoft/openxFactory/pull/962#issuecomment-5636697848),
2026-09-11T15:23:45Z), reproduced here by citation rather than by copy:
round 1 (4 threads — the ledger row, the singular-condition wording, two
scope claims), round 2 (2 — `chain_depth()` measurement, a tasks.md mirror),
round 3 (2 — the sentence-merge emphasis, the no-name limit inversion), round
4 (2 — a unit-count record, stale figures), round 5 (1 — `.openspec.yaml`
`proposed_by` wording), round 6 (2 — a stale README baseline, a false
test-inventory claim), round 7 (3 — the D1 "no test" cost line, a bookkeeping
paragraph, a no-name summary; two already fixed at head, one taken), round 8
(5 — D2b/D4, a bookkeeping bullet, three tasks.md sites, the README row and
the self-gate test, all the SAME finding: ratification alone does not clear
the transient row while the parent is off `main`, corrected to the two-event
condition D2b now states). A ninth review (on `b1e0aebb`) found 0 new
comments. Re-verified independently on 2026-09-12 via GraphQL
(`reviewThreads`, PR #962): **21 total, 0 unresolved**, unchanged since the
freeze — nothing landed on this pull request between the freeze
(2026-09-11T15:23:45Z) and the ruling (2026-09-12T15:45:16Z) other than the
ruling comment itself.

**CODEX — ABSENCE, TWICE, VERBATIM, NEVER A SECOND REQUEST.** One review
request stands: posted 2026-09-11T12:39:30Z (comment `5634559674`), reply
2026-09-11T12:39:39Z (comment `5634561402`):

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard.
> To continue using code reviews, you can upgrade your account or add
> credits to your account and enable them for code reviews in your settings.

A second usage-limit reply arrived at 2026-09-11T15:23:58Z (comment
`5636700978`, near-identical text) with no further `@codex review` request
having been posted — recorded as a second ABSENCE against the standing
request, not a second solicitation. Per the relaunch instructions in force,
no third request was made by this encode.

## 7. Why the packet exists

**ONE RESIDUE, FILED BEFORE IT WAS CLAIMED AND CLAIMED BEFORE IT WAS
AUTHORED.** openxFactory issue #955 was filed UNCLAIMED by the lane that
archived `amend-repo-boundary-governance-scope-first-line` (PR #937 →
archive PR #958), which owed it at its own `tasks.md` § 6.1 and `design.md`
D2b rather than deciding it: a later amendment of a requirement whose
promoted text already carries a unit-naming marker every one of whose named
units has left canon has exactly two options and canon did not say which an
author owes (a marker only some of whose named units have left canon is not
spent, and is not what this residue is about). `design.md` D0 measured that
every one of the sixteen unit-naming markers already in promoted canon is
already spent, and this packet's own block is its own witness — inheriting a
spent marker from its ordered-delta parent and dropping it under the rule it
writes. This packet, and the word that ratified it, closes that residue in
wording; #955 itself closes at the ARCHIVE (§ 8).

## 8. What is NOT ratified, and the residue this word does not reach

- **NOTHING IS PROMOTED.** This ratification edits no file under
  `openspec/specs/`. The `## MODIFIED` block is a DELTA; canon still carries
  the pre-amendment text until the archive writes the block over it.
- **`tasks.md` § 5 (ARCHIVE) STAYS ENTIRELY OPEN.** `code_surface: none`
  means this packet archives ON LANDING plus its own task list under
  `release-realization`, rather than on merged-plus-green realization
  evidence — but that archive is a SEPARATE act on a SEPARATE word, not
  performed or authorized here. openxFactory #955 closes THERE, and this
  pull request's body carries `refs #955` and no closing keyword.
- **`tasks.md` § 6 STAYS UNTICKED.** Residue measured and deliberately not
  taken at authoring: the sixteen spent markers already in promoted canon are
  not swept, option 2's machinery is not built, `document-lifecycle` is not
  amended, and the `target_release:` divergence elsewhere in the corpus is
  not repaired.
- **NO PROMOTED MARKER AND NO ARCHIVED DELTA IS EDITED.** They are records of
  ratified removals, correct under the amended sentence once it is promoted.

## 9. Sequencing, and the landing obligation this word does NOT carry

**`sequenced_after: [amend-merged-into-empty-tail-standing]` IS UNCHANGED BY
THIS RATIFICATION.** The declared parent has both landed (`87fd33d6`) and
archived (PR #973) since the freeze, which is what let this branch's two
merges resolve it; the declaration itself is not re-derived or edited here,
and `scripts/validate-sequenced-after.py` resolves it in the ARCHIVED corpus
exactly as designed.

**THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD, AND #955 CLOSES THERE.**
`code_surface: none` archives on landing plus its own task list rather than
on merged-plus-green realization evidence, but neither landing nor archive is
performed or authorized by this commit.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** No word for the
landing has been recorded on this packet as of this ratification; the
orchestrator asks Brett Heap for it separately, per the lane-collision
protocol.
