# Tasks: amend-published-tip-unreadable-scenario

Status: draft
Kind: tasks

`code_surface: none`. There is no realization group: the behaviour this
amendment describes landed in PR #646 (`2177b2a2`), and this packet is canon
catching up to it.

## 1. Ratification

- [ ] 1.1 RATIFICATION IS OWED AND HAS NOT HAPPENED. Issue #662 is the origin;
      Brett's *"do both as a batch on one word"* ADMITTED this packet to the
      queue and is not a ratification of its content. `proposal.md`,
      `design.md` and this file carry `Status: draft` until a separate act.
- [ ] 1.2 **D1 IS FLAGGED FOR VETO** and this box stays open until Brett has
      read `design.md`: the establishing obligation is written as a `WHEN`-side
      `AND` rather than a `THEN`-side `MUST`, which is weaker as a compliance
      hook and non-circular as a rule. If vetoed, the remedy is mechanical —
      move the bullet below the `THEN` and reword it as a `MUST`.

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
