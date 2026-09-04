# Verification record: add-per-change-sweep-ledger, 2026-09-04

Status: record
Kind: report
Captured: 2026-09-04, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch `change/add-per-change-sweep-ledger`
(openxFactory PR #623).

**This record is CAPTURED AT MERGE, not at first push, and every number below
was RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, after the
branch's FOURTH merge from `main` (to `95c2cf6a`, #622). `record-immutability`
forbids editing a `Status: record` document AFTER capture; capture is the merge
of the pull request that establishes it, and nothing is merged yet. A commit
cannot write its own hash into its own tree, so the ratification commit is named
by its subject and its position on the branch rather than by a hash. § 7 lists
the merges that moved these numbers and what each moved.

**If `main` moves again before this pull request lands**, the branch takes
another merge and every number here is re-derived a second time, with § 7
extended to say so, before capture.

## 1. `openspec validate add-per-change-sweep-ledger --strict`

```
Change 'add-per-change-sweep-ledger' is valid
```

## 2. `openspec validate --all --strict`

```
Totals: 88 passed, 0 failed (88 items)
```

## 3. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (33 active changes, 2 declaring the field).
```

The two declaring changes are `add-sequenced-after-substrate` (the parent) and
this packet, which declares `sequenced_after: [add-sequenced-after-substrate]`
ELECTIVELY — it is a SOLE modifier and no rule compels the field.

## 4. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
per-change sweep ledger consistent with the corpus (161 rows).
```

Exit 0. One row per change id across the active and archived corpora both, every
row's `state`, `class`, `declares`, `depth` and `prose` equal to the live
reading, the file sorted, and the totals DERIVED from the rows equal to
`corpus_sweep`'s independent measurement field by field.

**RATIFICATION MOVED NO ROW, and that is a property rather than a coincidence.**
A ratified ALL-ADDED sole modifier keeps its `state: active` and its
`class: sole`: ratification changes the document's standing, not what the sweep
reads about it. The ledger is byte-identical across the ratification commit, and
`--ledger-diff` was re-run after it to confirm rather than assume.

## 5. `python3 -m pytest tests/sequenced_after -q`

```
158 passed
```

## 6. doc-health parity — `python3 scripts/doc-health.py --single-repo .`

Compared against `origin/main` at `95c2cf6a`, both runs on the same day with the
repository-identity token normalized (the checkout directory name differs
between the two working trees and appears in every finding line).

**The report is identical to `main`'s apart from the word counts of the
documents this packet adds or edits.** No new finding of any severity, and none
suppressed. Headline on both trees: `6 critical, 5 error, 29 warning, 16 info`,
`New regressions vs previous report: 0`.

**One finding was raised and fixed BEFORE this capture**, and it is recorded
rather than quietly removed: the first ratification draft carried a `Ratified:`
line in BOTH the front matter and the body, which
`ratified-provenance` reports as CRITICAL — *"carries 2 ratification citation
lines, not one"*. The rule counts both spellings as ONE TOTAL per document. The
body line was removed; the front matter carries the single citation, which is
also where `create-medxchart-overlay-boundary` carries its own.

## 7. The corpus readings, and the four merges that moved them

`python3 scripts/validate-sequenced-after.py . --sweep`, on both trees:

| tree | change ids | co-modified | sole | active co-mod / sole | declaring | deepest |
| --- | --- | --- | --- | --- | --- | --- |
| `origin/main` `95c2cf6a` | 32 active + 128 archived = **160** | 112 | 48 | 21 / 11 | 1 | 1 hop |
| this branch, merged | 33 active + 128 archived = **161** | 112 | 49 | 21 / 12 | 2 | 2 hops |

**The difference is this packet and nothing else** — one more ACTIVE SOLE
modifier and one more declaration, taking the deepest declared chain from 1 hop
to 2 (this change → `add-sequenced-after-substrate` →
`add-structured-scope-substrate`). Prose headers hold at 3 (3 archived) and root
claims at 0 on both.

The branch took FOUR merges from `main` while open. Each is live evidence for
the mechanism being ratified:

| merge | what landed | rows moved | entry owed |
| --- | --- | --- | --- |
| `19d00872` (#616) | contract-v3.1 cut; `add-project-repo-schema` archived | 1 (`state`) | no |
| `c271caa2` (#615) | `update-standards-body-current-publications` archived | 1 (`state`) | no |
| `6a39d2ab` (#617) | `amend-owner-layer-severity` ratified and archived | 2 (new row + PARTNER FLIP) | **yes** |
| `95c2cf6a` (#622) | `add-consumer-identity-namespace` authored | 1 (new row, no flip) | no |

In every case `main`'s own MOVEMENT LOG additions merged cleanly and were
retained VERBATIM, verified line by line against `origin/main`'s docstring on
each merge — 436, 592, 721 and 721 lines respectively, **zero missing every
time**.

## 8. What could NOT be reproduced here

**The CI `pytest-suite` run for the ratification commit does not exist yet at
capture time**, because the commit carrying this file is the one that creates
it. The last full run before it, on `4d32b788`, was run `33818749006`:
**pass, 21m26s, zero failures**, with all five checks green. The ratification
commit changes documents, one test docstring and no executable behaviour; its
own run is reported on the pull request rather than predicted here.

**The full local suite** is `1 failed, 8974 passed, 35 skipped` — the single
failure being `tests/ideation-dashboard/test_snapshot.py::`
`test_find_validator_locates_pinned_checkout`, which asserts a SIBLING
`openxFactory/` checkout is reachable (the xFactory workspace layout) and fails
identically on pristine `origin/main` in a standalone clone. Environmental, not
this packet's, and green in CI where the layout holds.

## 9. One OPEN inherited defect, named rather than carried silently

`tests/doc-health/test_modified_block_currency_self_gate.py::`
`test_the_report_moves_only_in_this_family_s_lines` charges to the
`modified-block-currency` family an `info` row that appears only in the FIRST
render of a COLD checkout: the first run makes the published release tip
reachable and the second no longer reports it, so the two renders differ by one
row that is not the family's. Diagnosed by a four-configuration bisect (checkout
directory name × published tip present × submodule present); the
with-minus-without diff shows exactly 8 family rows in every configuration
measured. It is the same defect shape #614 already fixed once in that file
("ONE CLOCK, NOT TWO"), with the object store in place of the clock.

**Not this packet's, and deliberately not touched by it.** Filed separately.
