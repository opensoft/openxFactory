---
code_surface: none — this change moves PROSE IN CANON and nothing else. The behaviour the amended scenario describes is already implemented and already pinned: `add-release-tag-publication-check`'s family gained `obtain_commit` and the present-but-empty arm in PR #646 (`2177b2a2`, 2026-09-04), and `tests/doc-health/test_release_tag_publication.py` already asserts the TWO skip texts apart from each other as fresh literals (`_UNFETCHED_WORDS` + `_FETCH_TRIED_WORDS` against `_PRESENT_WORDS` + `_ANSWERED_WORDS`, over a `_StoreGit` fake object store that can express "the commit is not here"). NOTHING under `scripts/` changes, no test changes, no workflow changes, no contract member moves, and no severity, threshold, enforcement floor or finding path moves. **NO TEST ASSERTS THE OLD SCENARIO PROSE** — checked before this was written: the only occurrence of "commonest cause" anywhere outside canon is a code COMMENT in `scripts/doc_health/release_tag_publication.py`, not an assertion.
target_release: none — no contract bundle is cut, no release tag is owed, and nothing under `contracts/` is touched. Under `release-realization` a change whose `code_surface` is `none` archives ON LANDING; there is no realization to wait for, because the realization is what this amendment is catching up to.
Status: ratified
Proposed: 2026-09-05
Ratified: 2026-09-05 by Brett Heap (openxFactory operator authority) — "ratify 678, use openxfactory-1, land it when green"; record at review/ratification-2026-09-05.md
Origin: openxFactory issue **#662**, filed by lane `doxbench-stewardship` as a follow-up carried out of PR #646's reviewer note (issue #612), and Brett Heap's ruling of 2026-09-05, in session, verbatim: *"do both as a batch on one word"* — this packet being one of the two. THAT INSTRUCTION ADMITTED THE PACKET TO THE QUEUE AND DID NOT RATIFY ITS CONTENT; ratification followed as a separate act the same day.
---

# Proposal: amend-published-tip-unreadable-scenario

Status: ratified
Proposed: 2026-09-05, on Brett Heap's in-session ruling of the same day — lane
`openxfactory-1` (renamed this day from `openxfactory-max001`; spelled lowercase
because the required `lane-line` check enforces
`^Lane: [a-z0-9-]+( \(.*\))?$` and every lane id in this corpus is lowercase —
see § Lane spelling), verbatim *"do both
as a batch on one word"* — over openxFactory
issue **#662**, which states the defect and names the remedy. **That instruction
supplied the origin and approval pair the proposal-origin contract requires and
nothing more: it ADMITTED this packet to the queue and did not ratify its
content.** Ratification was a SEPARATE act later the same day and it has now
happened; the front matter carries its citation — ONE citation line for the
document, which is what `ratified-provenance` requires — and § Ratification
records the act, its verbatim word, and the two things it settled.

## Why

**Canon names a cause the checker has since proved is the wrong one.**

`doc-health`'s promoted *Release-tag publication* carries the scenario *The
manifest cannot be read at the published tip*, whose `WHEN` reads:

> the blob read for the manifest at the published tip answers nothing — **the
> commonest cause being a checkout that has not fetched that commit**

**The rule is right and nothing here weakens it.** The clause after the dash is
the problem: it asserts which of two causes is commonest, and the measurement
ran the other way. openxFactory **#612** found that on the aggregation nightly
the commit **WAS** fetched — the workflow's own *"Fetch each governed submodule's
live origin/main"* step had put all ten published tips in the store — and that
**nine of the ten governed repositories simply carry no
`contracts/manifest.yaml` at all**. Every night those nine were reported in the
words of a checkout that had not fetched their tips, sending anyone who read the
report to look for a fetch defect the workflow had already ruled out.

**PR #646 (`2177b2a2`, 2026-09-04) fixed the family; canon has not caught up.**
The family now ESTABLISHES which fact holds before it chooses words:
`obtain_commit` asks whether the commit is present and attempts one bounded
fetch of exactly that commit where it is not, and the two outcomes are reported
in two different skips — *"a bounded fetch of exactly that commit was attempted
and did not obtain it"* against *"the published tip … IS present in this clone
and carries no `contracts/manifest.yaml`"*. The scenario still tells a reader
that the first is the commonest cause.

## What Changes

**ONE scenario's bullets, inside ONE `## MODIFIED` requirement. Nothing else.**

The delta restates `doc-health`'s *Release-tag publication* in full — all 30
promoted scenarios, every body unit, byte-faithful — and changes exactly this:

- the scenario's `WHEN` bullet is **REPLACED**, from naming one cause as
  commonest to naming **both facts** the single answer stands for;
- an `AND` bullet is **ADDED** requiring that the family have **established
  which of the two holds** before choosing its words — asking presence, and
  attempting one bounded fetch where the commit is absent — *rather than naming
  a cause it did not check*;
- a second `AND` bullet is **ADDED** saying that where the commit IS present and
  carries no manifest, the skip must say THAT and state the presence, because a
  tip the checkout holds is an ANSWER rather than a read that failed.

The promoted `THEN` and the promoted closing `AND` (the `verify_tag` / #338
conflation clause) are carried **byte-identical**.

**ONE canon unit is dropped, and it is declared.** Replacing a bullet drops it,
so the block carries the reserved marker
`**Removed from canon by amend-published-tip-unreadable-scenario
(2026-09-05):**` naming the old `WHEN` verbatim as a code span, with the reason.
This is the one thing that differs from `add-release-tag-gate`, whose block only
added and therefore owed no marker.

## Impact

**No behaviour changes and no code moves** (`code_surface: none`, front matter).
The family already does what the amended wording describes; the tests already
pin the two skip texts apart from each other. This is canon catching up with the
checker.

**Doc-health:** the `modified-block-currency` family reads this new active
delta. It drops one canon unit, that unit is named by the reserved marker, and
every other unit and all 30 scenario titles are carried — so the block is
expected to raise **no** currency finding. § Verification records the run and
the mutation probe that proves the family read the block at all.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance
is owed.

## Orchestrator Decisions — FLAGGED FOR VETO, AND NOT VETOED

**D1** in `design.md`: whether the establishing obligation is written as a
`WHEN`-side bullet (what the family has already done by the time the scenario
applies) or as a `THEN`-side one (what it must do). This packet writes it on the
`WHEN` side and says why. It was the only decision the issue did not settle, and
it was put to the ratifier as the packet's veto point.

**It was not vetoed.** The word of 2026-09-05 was given with D1 standing, so the
`WHEN`-side reading is **ratified knowingly** rather than by silence, together
with the cost D1 states in its own terms: a `WHEN`-side obligation is weaker as
a compliance hook than a `THEN`-side `MUST`.

## Ratification

**Ratified 2026-09-05 by Brett Heap (openxFactory operator authority), in
session, verbatim: *"ratify 678, use openxfactory-1, land it when green"*.** The
record is `review/ratification-2026-09-05.md`; the verification it cites is
`review/verification-2026-09-05.md`.

The word settles **two** things and nothing else. It ratifies the delta with D1
standing. And it settles the lane spelling § Lane spelling raised: **the
canonical lane id is the lowercase `openxfactory-1`** — the spelling the ratified
`lane-line` grammar can express and the one this packet already wrote — so the
capitalised `openXfactory-1` is a display form and not a second lane. **It does
NOT amend `lane-line.yml`**, which this packet never proposed and still does
not.

## Lane spelling — surfaced, not papered over

This lane was renamed on 2026-09-05 and circulated in session as
**`openXfactory-1`**, with a capital X. **The ratified `lane-line` check cannot
express that**: `.github/workflows/lane-line.yml` requires a pull request body to
open with `Lane: <name>` matching `^Lane: [a-z0-9-]+( \(.*\))?$`, lowercase
only, and every other lane id in this corpus is lowercase
(`openxfactory-max001`, `openxfactory-opendox`, `doxbench-stewardship`). The
capitalised spelling failed that required check on this packet's first push
(run `33970709751`).

**This packet therefore writes `openxfactory-1` and changes no check.**
Weakening a required gate so a name fits is a governed change, not a side effect
of an unrelated prose amendment; if the capitalised spelling is the one that
should stand, `lane-line.yml`'s grammar needs its own packet. Recorded here
rather than left in a pull request comment, because a lane id split across two
spellings is exactly the kind of thing that goes unnoticed until someone greps
for one of them.

## What this proposal does NOT claim

- It does not change what the family reads, reports, or at which severity.
- It does not claim the promoted `THEN` bullet is now unambiguous on its own —
  it is carried verbatim precisely because it is canon, and the added `AND`
  below it is what disambiguates *"saying so"*. `design.md` D1 records that
  reading rather than leaving it to be discovered.
- It does not touch the sibling scenario *The changelog cannot be read at the
  published tip*. **CORRECTED 2026-09-05, AFTER RATIFICATION AND BEFORE
  LANDING:** an earlier draft of this bullet said that sibling "carries no
  equivalent misnamed cause". **That was false, and the correction is recorded
  rather than quietly made.** `openspec/specs/doc-health/spec.md:2788` carries
  the SAME clause word for word — *"the blob read for `contracts/CHANGELOG.md`
  at the published tip answers nothing — the commonest cause being a checkout
  that has not fetched that commit"*. The error was mine: at authoring I
  searched for the manifest phrasing rather than for the clause, and found only
  one of its two sites. It was caught by a rehearsal of the archive act, which
  asserted that the retired clause no longer appears in canon and found that it
  still does — in the sibling.

  **The SCOPE is unchanged and deliberately so.** Issue #662 asks about the
  manifest scenario; the ratified delta amends that scenario and no other, and
  widening a ratified packet after the word that ratified it is not a
  correction, it is a different change. **The sibling is therefore an OWED
  SUCCESSOR**, named here so it is not lost: it needs the same treatment, and it
  is one line plus a marker. The two cases are not identical — the changelog
  read has no `obtain_commit`-style presence probe of its own, it inherits the
  manifest read's — so the successor owes a reading of that before it copies
  this wording across.
