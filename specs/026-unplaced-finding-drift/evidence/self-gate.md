# Self-gate — the predicted movement, measured (T039, packet § 2.13)

## The prediction

**ZERO in every band.** The class map is complete on this tree, so the fifth
class reads `0` and the only difference a reader sees is one more row in the
class block.

## How the BEFORE was taken

**Not copied from packet § 3.1**, per § 2.13's own instruction — the arms'
population moves as active changes land, and it had already moved once under
that packet. Taken at THIS feature's own base, from a clean extraction of it so
no working-tree edit could contaminate it:

```bash
git archive $(git merge-base HEAD origin/main) | tar -x -C <scratch>/026-unplaced-finding-drift
cd <scratch>/026-unplaced-finding-drift && git init -q .
python3 scripts/doc-health.py --single-repo . --family modified-block-currency
```

The extraction directory is NAMED `026-unplaced-finding-drift` so the report's
repo field matches the worktree's, which is what makes the two reports
line-comparable.

## The result

`self-gate-before.txt` (merge base `6d100e51`, the amendment PR #461) versus
`self-gate-after.txt`
(this branch, the feature landed):

```text
$ diff self-gate-before.txt self-gate-after.txt
126a127
> - unplaced-finding drift: 0 (`warning`)
```

**ONE LINE, and it is the new class row reading zero.** Nothing else in the
report moved: not the headline (`0 critical, 0 error, 0 warning, 7 info` in
both), not the canon-share figure, not the per-stage census, not one of the
seven `info` rows, not the ranked plan, and not one of the twenty-one other
family sections — the before run is a FULL report, so the comparison covers all
of them rather than only this family's block.

| band | before | after | movement |
|---|---|---|---|
| critical | 0 | 0 | 0 |
| error | 0 | 0 | 0 |
| warning | 0 | 0 | 0 |
| info | 7 | 7 | 0 |

| class | before | after |
|---|---|---|
| scenario-title completeness | 0 | 0 |
| carriage ledger | 7 | 7 |
| title resolution and ordering | 0 | 0 |
| marker defects | 0 | 0 |
| unplaced-finding drift | — (no such class) | **0** |
| `unclassified` residual | 0 (row absent) | 0 (row absent) |

This reproduces packet § 3.1's figure exactly, which is the state § 2.13 asked
this feature to reproduce.

## Re-taken after the catch-up merge, and it did not move

The pair was first measured at the original branch point `86b7ca3f` (the
packet's own merge commit) and read `0 warning, 7 info`, classes `0 / 7 / 0 / 0`
and residual `0`. `origin/main` then advanced six commits, one of them a new
proposal (`adopt-medxsoft-repository-identity`), so the branch took a catch-up
MERGE — never a rebase — and **both figures were re-taken at the new merge base
`22f15cdf`**. Identical, and the diff is still the same single line. Recorded
because § 3.1 warns that this figure moves as active changes land: here it did
not, because the incoming packets carry no `## MODIFIED Requirements` block, and
that is the only thing this family reads.

## Dogfood — the block renders in one run and not the other (T042)

```bash
python3 scripts/doc-health.py --single-repo . --family modified-block-currency
#   -> "Finding classes, counted apart …" present, five class rows

python3 scripts/doc-health.py --single-repo . --skip-family modified-block-currency
#   -> "### modified-block-currency\n\nSkipped: skipped by run configuration"
#      and ZERO occurrences of the lead line
```

A skip is the absence of a measurement, so `0 · 0 · 0 · 0 · 0` beside one would
claim a measurement nobody took. The fifth class does not change that, and the
`--skip-family` run confirms it on the artifact.

## OpenSpec validation (T041)

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
Totals: 78 passed, 0 failed (78 items)
```

77 items at the original branch point; 78 after the catch-up merge, which
brought `adopt-medxsoft-repository-identity` in. Both runs green.

## Unmoved by Brett's shape amendment (2026-08-28)

The amendment changes how UNPLACED findings group, and there are none wherever
the class map is complete — which is every run on this tree. Re-measured after
it landed in this feature: the diff is still exactly the one line, the headline
is still `0 critical, 0 error, 0 warning, 7 info`, and the class block still
reads `0 / 7 / 0 / 0` plus `unplaced-finding drift: 0`.
