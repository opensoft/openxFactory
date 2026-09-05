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
