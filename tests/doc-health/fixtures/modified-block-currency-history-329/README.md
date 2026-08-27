# Fixture: the #329 one-of-eight case, reconstructed

**Recovered at `d5f447e89cf619fd12113bcf03525468ece4470d`** — reconstructed from this repository's git history.

Issue #329. `add-release-inventory-drift-check`'s `## MODIFIED Requirements`
block restated ONE of `doc-health`'s eight `Deterministic check families`
scenarios, while the change's own `## ADDED Requirements` brought SEVEN — so the
**file-level scenario count stayed flat at eight** and nothing that counted
could see the loss.

**The truncation was caught by a byte-for-byte promotion verification run by
hand at the archive gate, BEFORE anything was committed, and the block was
rewritten scenario-complete inside the archive commit `38b548d4` itself.** There
is therefore no reverted commit in this history to find, and no ratified
document claims one: the recoverable state is the archive commit's PARENT.

## Provenance

| file | recovered from |
| --- | --- |
| `driftFactory/openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md` | `git show d5f447e8:openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md` |
| `driftFactory/openspec/specs/doc-health/spec.md` | `git show d5f447e8:openspec/specs/doc-health/spec.md` |

- **recovered at** `d5f447e89cf619fd12113bcf03525468ece4470d` (the same commit
  named in line 3) — the PARENT of the archive commit.
- **the defect ended at** `38b548d46153e5e39c855aa105aa77cbb550894a` ("Archive
  add-release-inventory-drift-check: the drift gate is canon"), merged as
  `b03b9992d519dbfab78fa63a00c5c6e2413ae0e0` (PR #331).
- The truncated block lived in the ACTIVE change directory from `e06b066b`
  (draft) through `57c26e1a` (PR #319) and was rewritten inside the archive
  commit, which is also where the path leaves `openspec/changes/` — so
  `d5f447e8` is the last commit at which both sides of the comparison exist.
- `proposal.md` is scaffolding: a `Status:` line only.

## Scope of the verbatim guarantee

The **requirement** `Deterministic check families` is byte-identical to the
recovered text; the `# doc-health Specification` / `## Purpose` /
`## Requirements` lines are synthetic scaffolding. That spec is 50,505 bytes at
this commit — smaller than #351's canon, so size is not the argument here; what
is, is that every other requirement in the file would be frozen canon this
fixture asserts nothing about.

The **delta file is copied WHOLE, and that is load-bearing**: its
`## ADDED Requirements` section is where the seven offsetting scenarios live,
and the flat count only exists because of them.

## What the family reports here

- scenario-title arm — **one `warning`**, naming all SEVEN omitted titles:
  `Lifecycle conformance checks fire`, `A register carries staged status`,
  `Drift checks fire`, `Catalog conformance checks fire`,
  `Routing conformance checks fire`, `Origin conformance checks fire`,
  `Roster composition is checked across domains`.
- carriage ledger — **one `info`**, listing 17 of canon's 28 units: 2 body
  sentences (the `seventeen check families` enumeration and the
  `Four of the seventeen` sentence) and 15 scenario bullets.
- title resolution, ordering, marker defects — **none**.

The two-body-sentence shape coincides with the packet's own § 2.1 block, which
also fails to carry two body sentences. That is a coincidence of FORM. **This
fixture is not evidence about § 2.1.**

## Which rule this exists for

`add-modified-block-currency-check` § 3.2, audit row **A2**.
Tests: `test_the_329_block_omits_all_seven_titles_by_name`,
`test_the_329_flat_file_level_count_buys_no_silence`,
`test_the_329_ledger_names_canon_s_body_sentences`,
`test_the_reconstructed_fixtures_are_the_history_they_claim`.

This fixture pins behaviour. It does not resolve #329 (already repaired) and it
does not close #330.
