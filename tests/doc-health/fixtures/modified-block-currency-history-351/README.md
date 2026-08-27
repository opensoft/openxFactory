# Fixture: the #351 true positive, reconstructed

**Recovered at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`** — reconstructed from this repository's git history.

Issue #351. `add-doxchat-model-intake`'s `## MODIFIED Requirements` block for
`doxBench model catalog and provider boundary` was written on 2026-08-21, one
day before canon's own version of the same requirement landed via
`add-doxbench-editing-phase-b` (`02a71d6e`, 2026-08-22). The block was never
refreshed, so archiving it would have replaced canon with a pre-2026-08-22
rendering — deleting body clauses, two whole scenarios, and reverting one
scenario line. A human caught it and PR #358 repaired it by hand.

## Provenance

| file | recovered from |
| --- | --- |
| `intakeFactory/openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md` | `git show bcfc26a0:openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md` |
| `intakeFactory/openspec/specs/ideation-dashboard/spec.md` | `git show bcfc26a0:openspec/specs/ideation-dashboard/spec.md` |

- **recovered at** `bcfc26a0d2f182c652ed9054b82210ccbee8124a` (the same commit
  named in line 3) — the PARENT of the repair commit.
- **the defect ended at** `f68261f775eb74455a16f7d4d67b576fd76618f0` ("The
  intake delta restates current canon, so archiving it no longer reverts six
  clauses (#351)"), merged as
  `87d0b95ae2970733f273cbac15beb847a5b562c5` (PR #358).
- The repair touched only the delta and that change's `tasks.md` — **it did not
  touch canon** — so `openspec/specs/ideation-dashboard/spec.md` reads
  identically at `bcfc26a0` and at `f68261f7`, and one commit serves both sides.
- `proposal.md` is scaffolding: a `Status:` line only, because `_standing()`
  reads it and nothing else here depends on a proposal.

## Scope of the verbatim guarantee

The **requirement** `doxBench model catalog and provider boundary` is
byte-identical to the recovered text. The surrounding
`# ideation-dashboard Specification`, `## Purpose` and `## Requirements` lines
are synthetic scaffolding: the real promoted spec is 228,041 bytes at that
commit and carries dozens of requirements this fixture says nothing about, and
the family reads per requirement. The **delta file is copied WHOLE**.

`test_the_reconstructed_fixtures_are_the_history_they_claim` re-derives both
sides from git and enforces exactly this scoping.

## What the family reports here

- scenario-title arm — **one `warning`**, naming `The menu offers a routing
  rule` and `A fourth provider verb is proposed`.
- carriage ledger — **one `info`**, listing 11 of canon's 25 body units and
  scenario bullets: 3 body sentences, 8 scenario bullets. Among them canon's
  `**THEN** the selector MUST show exactly the available catalog entries and
  their data-handling badges`, which the block's replacement contains as a
  STRICT PREFIX — the packet's § 6.4 residue, and the case a containment rule
  loses.
- title resolution, ordering, marker defects — **none**.

## The clause count, stated honestly

`f68261f7`'s message CLAIMS "six body clauses" and NAMES five: the three-member
port surface enumeration; "MUST NOT be added as a fourth provider verb"; the
`auto` routing-rule clause; the broker-lane credential clause; and `thread
file` in the credential-leak list. The sixth is never named. Those five lie
inside THREE of canon's sentences, because the ratified derivation splits a body
paragraph into SENTENCES — so the tests assert the clause TEXT inside the
reported units and never a row count.

## Which rule this exists for

`add-modified-block-currency-check` § 3.1, audit row **A1** (and row **A5**'s
end-to-end half, § 3.4).
Tests: `test_the_351_block_omits_exactly_the_two_scenarios_canon_kept`,
`test_the_351_ledger_carries_every_clause_the_repair_commit_named`,
`test_the_351_reverted_scenario_line_is_reported`,
`test_the_351_widened_bullet_is_reported_although_the_block_contains_it`,
`test_the_351_findings_land_on_the_delta_path_at_the_right_severities`,
`test_the_reconstructed_fixtures_are_the_history_they_claim`.

This fixture pins behaviour. It does not resolve #351 (already repaired) and it
does not close #330.
