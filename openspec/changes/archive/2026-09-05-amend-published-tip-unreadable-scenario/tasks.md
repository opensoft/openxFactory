# Tasks: amend-published-tip-unreadable-scenario

Status: ratified
Ratified by: amend-published-tip-unreadable-scenario — 2026-09-05, Brett Heap, "ratify 678, use openxfactory-1, land it when green" (record `review/ratification-2026-09-05.md`)
Kind: tasks

`code_surface: none`. There is no realization group: the behaviour this
amendment describes landed in PR #646 (`2177b2a2`), and this packet is canon
catching up to it.

## 1. Ratification

- [x] 1.1 **RATIFIED 2026-09-05 by Brett Heap** (openxFactory operator
      authority), in session, verbatim: **_"ratify 678, use openxfactory-1, land
      it when green"_**. Issue #662 is the origin and Brett's earlier *"do both
      as a batch on one word"* was the ADMISSION to the queue, not this;
      ratification was a separate act. `proposal.md`, `design.md` and this file
      now carry `Status: ratified` against ONE citation line each. Record:
      `review/ratification-2026-09-05.md`; verification:
      `review/verification-2026-09-05.md`.
- [x] 1.2 **RATIFIED AS DESIGNED — D1 was the packet's veto point and it was NOT
      vetoed.** The word was given with the decision standing, so the
      `WHEN`-side `AND` and the weakening it admits (weaker as a compliance
      hook, non-circular as a rule) are ratified KNOWINGLY rather than by
      silence. The mechanical remedy — move the bullet below the `THEN` and
      reword it as a `MUST` — was NOT taken and is kept in `design.md` D1 so the
      cost of reversing the decision sits beside it.
- [x] 1.3 **THE LANE SPELLING IS SETTLED BY THE SAME WORD.** *"use
      openxfactory-1"* makes the LOWERCASE id canonical — the spelling the
      ratified `lane-line` grammar can express and the one this packet already
      wrote — so `openXfactory-1` is a display form and not a second lane.
      **`.github/workflows/lane-line.yml` is NOT amended**, which this packet
      never proposed and still does not.

## 2. The delta

- [x] 2.1 `specs/doc-health/spec.md` carries ONE `## MODIFIED Requirements`
      block over the promoted *Release-tag publication*, restating it in full —
      every body unit and all 30 promoted scenario titles — and changing exactly
      one scenario: the `WHEN` bullet REPLACED, two `AND` bullets ADDED.
- [x] 2.2 **THE ONE DROPPED UNIT IS DECLARED.** The block carries
      `**Removed from canon by amend-published-tip-unreadable-scenario
      (2026-09-05):**` naming the old `WHEN` bullet verbatim as a code span,
      with the reason. This is the difference from `add-release-tag-gate`, which
      only added and owed no marker.
- [x] 2.3 NO FILE IS ADDED UNDER `openspec/specs/` — no codexFactory floor
      advance is owed.
- [x] 2.4 The sibling scenario *The changelog cannot be read at the published
      tip* is NOT touched: it carries no equivalent misnamed cause.

## 3. Verification

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-published-tip-unreadable-scenario --strict` and `--all --strict`.
- [x] 3.2 `python3 -m pytest tests/doc-health -q` — expected UNCHANGED, because
      no test asserts the old scenario prose. Checked before authoring: the only
      "commonest cause" outside canon is a code comment.
- [x] 3.3 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`.
- [x] 3.4 `python3 scripts/doc-health.py --single-repo .` against a SAME-CLOCK
      control at this branch's base, identical except this change's own effects.
- [x] 3.5 **THE MUTATION PROBE.** `modified-block-currency` reporting nothing
      about this block cannot be told from a block it never read, so one
      promoted scenario title is deliberately mutated, the family re-run and
      seen to FIRE, and the delta restored. Recorded in the pull request.
- [x] 3.6 The corpus-sweep ledger row, seeded with the real pull request number.

## 4. The landing and archive acts

- [x] 4.1 **RATIFIED AND LANDED BY openxFactory PR #678**, merge
      **`87c15baa`** (2026-09-05T16:41:11Z), on Brett Heap's word *"ratify 678,
      use openxfactory-1, land it when green"*. That pull request carried the
      delta, the two records, the README row, the ledger row, the merge of
      `main` after #677, and the correction of § 4.2's false claim.
- [x] 4.2 **A FALSE CLAIM IN THE RATIFIED PROSE WAS CORRECTED BEFORE LANDING,
      AND THE SIBLING IT MISSED IS AN OWED SUCCESSOR.** `proposal.md` § *What
      this proposal does NOT claim* had said the sibling scenario *The changelog
      cannot be read at the published tip* carries no equivalent misnamed cause.
      It does — the identical clause, over `contracts/CHANGELOG.md`. Found by
      REHEARSING this archive act on a throwaway worktree, whose assertion that
      the retired clause no longer appears in canon found it still there, in the
      sibling. The scope was NOT widened: widening a ratified packet after the
      word that ratified it is a different change. The successor owes one
      reading first — the changelog read has no presence probe of its own, it
      inherits the manifest read's.
- [x] 4.3 **ARCHIVED 2026-09-05 BY openxFactory PR #685**,
      `change/archive-amend-published-tip-unreadable-scenario`, cut from `main`
      at `87c15baa`, on Brett Heap's word *"do both as a batch on one word"* and
      the `release-realization` rule that a change with `code_surface: none`
      archives ON LANDING. Performed with
      `scripts/proposal-support.py . archive amend-published-tip-unreadable-scenario
      --date 2026-09-05 --yes`, never a bare `openspec archive`.
- [x] 4.4 **THE PROMOTION IS DIFF-CLEAN AND THE SPEC COUNT DID NOT MOVE.** The
      requirement as promoted into `openspec/specs/doc-health/spec.md` is
      BYTE-IDENTICAL to the delta's `## MODIFIED` block — 535 lines, 30
      scenarios, compared programmatically rather than eyeballed — the
      `Removed from canon by` marker promotes WITH the block, and the retired
      clause survives in canon only inside that marker's code span, with ZERO
      live bullets carrying it in the amended scenario. `openspec/specs/` holds
      the same **59** capability directories before and after, so **no
      codexFactory floor advance is owed**.
- [x] 4.5 **A MISQUOTED REGEX IN THE PACKET'S OWN PROSE, REPAIRED IN THE ARCHIVE
      COMMIT AND NOT IN THE RECORDS.** Copilot on PR #685 found that
      `proposal.md` and `.openspec.yaml` quoted `lane-line`'s grammar as
      `^Lane: [a-z0-9-]+$`, dropping the optional parenthetical group. The
      real check is `^Lane: [a-z0-9-]+( \(.*\))?$` — and that group is exactly
      what makes this packet's own pull-request first line,
      `Lane: openxfactory-1 (openXfactory-1)`, legal, so the truncated quote
      made the packet look non-conforming to a check it passes. The CONCLUSION
      the quote supports is unaffected: no form of that group admits an
      uppercase letter, so lowercase-only stands.
      **THE TWO `Status: record` FILES WERE NOT TOUCHED and did not need to be**
      — `review/ratification-2026-09-05.md` already quotes the grammar in full,
      `review/verification-2026-09-05.md` does not quote it, and
      `record-immutability` forbids editing either after capture, which happened
      at the merge of #678. Only the two non-record files were repaired.
