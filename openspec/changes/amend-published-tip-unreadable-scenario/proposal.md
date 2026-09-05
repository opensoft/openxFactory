---
code_surface: none — this change moves PROSE IN CANON and nothing else. The behaviour the amended scenario describes is already implemented and already pinned: `add-release-tag-publication-check`'s family gained `obtain_commit` and the present-but-empty arm in PR #646 (`2177b2a2`, 2026-09-04), and `tests/doc-health/test_release_tag_publication.py` already asserts the TWO skip texts apart from each other as fresh literals (`_UNFETCHED_WORDS` + `_FETCH_TRIED_WORDS` against `_PRESENT_WORDS` + `_ANSWERED_WORDS`, over a `_StoreGit` fake object store that can express "the commit is not here"). NOTHING under `scripts/` changes, no test changes, no workflow changes, no contract member moves, and no severity, threshold, enforcement floor or finding path moves. **NO TEST ASSERTS THE OLD SCENARIO PROSE** — checked before this was written: the only occurrence of "commonest cause" anywhere outside canon is a code COMMENT in `scripts/doc_health/release_tag_publication.py`, not an assertion.
target_release: none — no contract bundle is cut, no release tag is owed, and nothing under `contracts/` is touched. Under `release-realization` a change whose `code_surface` is `none` archives ON LANDING; there is no realization to wait for, because the realization is what this amendment is catching up to.
Status: draft
Proposed: 2026-09-05
Origin: openxFactory issue **#662**, filed by lane `doxbench-stewardship` as a follow-up carried out of PR #646's reviewer note (issue #612), and Brett Heap's ruling of 2026-09-05, in session, verbatim: *"do both as a batch on one word"* — this packet being one of the two. THAT INSTRUCTION ADMITTED THE PACKET TO THE QUEUE AND DID NOT RATIFY ITS CONTENT; ratification is a separate act and has not happened.
---

# Proposal: amend-published-tip-unreadable-scenario

Status: draft
Proposed: 2026-09-05, on Brett Heap's in-session ruling of the same day — lane
`openXfactory-1`, verbatim *"do both as a batch on one word"* — over openxFactory
issue **#662**, which states the defect and names the remedy. **That instruction
supplied the origin and approval pair the proposal-origin contract requires and
nothing more: it ADMITTED this packet to the queue and did not ratify its
content.**

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

## Orchestrator Decisions — FLAGGED FOR VETO

**D1** in `design.md`: whether the establishing obligation is written as a
`WHEN`-side bullet (what the family has already done by the time the scenario
applies) or as a `THEN`-side one (what it must do). This packet writes it on the
`WHEN` side and says why. It is the only decision the issue did not settle.

## What this proposal does NOT claim

- It does not change what the family reads, reports, or at which severity.
- It does not claim the promoted `THEN` bullet is now unambiguous on its own —
  it is carried verbatim precisely because it is canon, and the added `AND`
  below it is what disambiguates *"saying so"*. `design.md` D1 records that
  reading rather than leaving it to be discovered.
- It does not touch the sibling scenario *The changelog cannot be read at the
  published tip*, which carries no equivalent misnamed cause.
