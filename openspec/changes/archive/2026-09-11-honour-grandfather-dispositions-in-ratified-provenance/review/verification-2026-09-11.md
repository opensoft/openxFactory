# Verification record: honour-grandfather-dispositions-in-ratified-provenance, ratified tree 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: honour-grandfather-dispositions-in-ratified-provenance — 2026-09-11, Brett Heap, D1 "info row carrying the citation" / D2 "Archived-only boundary" (record `review/ratification-2026-09-11.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-11.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** A dated run report keeps `record`, and a second
run writes a different path rather than rewriting this one. This is the
packet's FIRST and only gate capture; a later re-run writes
`verification-<later date>.md` beside it.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE, AFTER THE ENCODE AND
AFTER THE MERGE FROM `main`, IN A FRESH CLONE.** Nothing is carried forward
from the pull request body's earlier gate tables or from `tasks.md`
§ 5.1–5.9; where a figure matches one of those, it matches because it was
measured again and came out the same. `tasks.md` § 5.13 is the task-list entry
this file is the evidence for.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| branch | `change/honour-grandfather-dispositions-in-ratified-provenance` |
| head the ratification word was given over | `468df2ef` |
| bench fix after the word (round 3) | `cd27180c` |
| bench fix after the word (round 4) | `5a8bba3e` |
| merge-from-`main` commits on this branch | `468df2ef` (`1fb6d5cd`), `a343f017` (`22efcbe8`), `f281c1fa` (`78d2c6f5`), `ad6d542c` (`38c076d1`) |
| `origin/main` merged in last | `38c076d1` |
| control worktree for `--all --strict`, `doc-health` and the pytest baseline | a second worktree at `origin/main` `38c076d1` |
| CLI on `PATH` | `openspec` **1.2.0** |
| pinned CLI | `@fission-ai/openspec@1.12.0`, content-verified, 80-package closure |
| aggregation used for § 10 and § 11 | `opensoft/xFactory` `f5dba67f`, `health/dispositions.yaml` blob `1f4e1cef`, `xFactories/codexFactory` `ef180510` (the pin that head carries) |

**WHAT THIS CAPTURE DOES NOT CLAIM.** The locally-run suites below are the
`doc-health`, `sequenced_after`, `scope_globs` and `proposal-support`
selections, not the whole repository suite. The `pytest-suite` required check
runs on the pull request in CI and is the authority for the green this landing
and this packet's realization evidence need.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate honour-grandfather-dispositions-in-ratified-provenance --strict`

```
$ OPENSPEC_TELEMETRY=0 openspec validate honour-grandfather-dispositions-in-ratified-provenance --strict
Change 'honour-grandfather-dispositions-in-ratified-provenance' is valid
```

**exit 0.**

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the 1.2.0 binary on `PATH`

```
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
✓ change/honour-grandfather-dispositions-in-ratified-provenance
…
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
Totals: 99 passed, 2 failed (101 items)
```

**exit 1**, and the exit code is expected rather than a regression. **THE
FAILURE SET IS IDENTICAL TO `main`'s, NAME BY NAME.** Control run in a second
worktree at `origin/main` `38c076d1`:

```
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
Totals: 98 passed, 2 failed (100 items)
```

**exit 1.** Two failed on both sides, the SAME two, and **this change is the
one extra item** — 100 items on `main`, 101 here — **and it PASSES**.

**`spec/repo-boundary-governance` IS NO LONGER IN EITHER SET**, which is a
change on `main` and not here: `amend-repo-boundary-governance-scope-first-line`
archived at PR #958 and promoted the amended first line, so the 1.2.0 reading
that used to fail is gone from both sides. This packet neither caused it nor
depends on it; it is recorded because the failure set is the figure this
section compares and a reader of an earlier capture would otherwise expect
three.

## 3. `python3 scripts/proposal-support.py . verify honour-grandfather-dispositions-in-ratified-provenance`

```
$ python3 scripts/proposal-support.py . verify honour-grandfather-dispositions-in-ratified-provenance
proposal support verification ok
```

**exit 0.** This is the gate that reads the origin declaration, so it is the
mechanical confirmation that the approval pair was ADDED beside a fixed `kind`
and `id` rather than substituted for them.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
$ python3 scripts/validate-sequenced-after.py .
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**exit 0.**

```
$ python3 scripts/validate-sequenced-after.py . --ledger-diff
sequenced_after corpus sweep
----------------------------
change ids (39 active + 161 archived): 200
co-modified at requirement granularity (each would owe a declaration): 147
sole modifiers (each would declare `sequenced_after: []`): 53
ACTIVE changes: co-modified / sole: 24 / 15
declaring `sequenced_after:`: 25 (… honour-grandfather-dispositions-in-ratified-provenance …)
declaring an explicit `[]` root claim: 7
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (200 rows).
```

**exit 0.** The ledger row seeded at the bench survives both later merges from
`main`. The corpus grew from 198 rows to 200 because `main` archived two
changes (`state-header-window-budget` at PR #953,
`amend-repo-boundary-governance-scope-first-line` at PR #958); the merge
commit `ad6d542c` carries both of their moved rows from `main` and this
change's own active row unchanged, which is what the conflict resolution in
that commit's message records.

## 5. `python3 scripts/validate-scope-globs.py .`

```
$ python3 scripts/validate-scope-globs.py .
scope_globs validation passed (all active changes conform).
```

**exit 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

**exit 0.** Headline, verbatim:

```
Canon share by words: 39.5% (369915 canon words / 935344 governance words, promoted specs included).
Findings: 32 critical, 5 error, 47 warning, 15 info. New regressions vs previous report: 0.
```

**THE `ratified-provenance` FAMILY REPORTS 28 ROWS IN THIS SCOPE, EVERY ONE AT
`critical` AND NONE AT `info`** — which is `design.md` D6 measured rather than
asserted. `health/dispositions.yaml` lives at the AGGREGATION root, a
`--single-repo` run has `Context.agg_root is None`, and this arm does nothing
at all in that scope, so this repository's own gate is untouched by the whole
packet.

`modified-block-currency`, the family whose `derive_units` proved the delta's
carriage, reports by class:

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 9 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**MARKER-DEFECT FINDING COUNT: 0.** `tasks.md` § 4.2's claim is that no
promoted byte is edited, so no `Removed from canon` marker is owed and none is
written; a marker written where none was owed would draw a ground-three
finding here, and none is drawn.

**NOT ONE FINDING IN THE WHOLE REPORT NAMES THIS PACKET.** `grep -c
honour-grandfather-dispositions-in-ratified-provenance` over the report returns
**0**.

**THE FINDING-LINE REPORT IS IDENTICAL TO `main`'s, NOT MERELY EQUAL IN
COUNT.** Control run in the `origin/main` `38c076d1` worktree: both reports
carry **99** finding lines and, after normalising the `Repo-Identity` /
`repo=` token (the checkout directory's name, which differs between checkouts
by construction), `diff` returns **0 lines** over the whole report — headline,
per-stage table, preflight, findings and ranked plan alike. The ratification
encode introduced no finding and cleared none.

**WHY THE CANON SHARE IS BYTE-IDENTICAL PRE AND POST, WHICH IS CORRECT AND NOT
A STALE READ.** Those figures come from the governed DOCUMENT corpus (**399**
documents: `docs/`, `ideation/` and their kin) and that corpus contains
**0** documents under `openspec/changes/` — loaded directly from
`doc_health.corpus` rather than inferred. This packet's files live in the
separate LIFECYCLE SCAN SET (**324** documents), and all three of this
ratification's lifecycle documents are in it with the statuses this encode gave
them:

```
openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/proposal.md                       status='ratified' kind=None
openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/review/ratification-2026-09-11.md status='ratified' kind='report'
openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/review/verification-2026-09-11.md status='record'   kind='report'
```

So the families that read lifecycle documents — `ratified-provenance`,
`status-validity` — did see all three and reported nothing against any of them.
**WHAT A LATER EDIT TO THIS FILE'S PROSE COULD MOVE, AND WHY IT IS NOTHING**:
this capture was taken with both `review/` records present at the statuses
above, and the governed-corpus word totals do not read `openspec/changes/` at
all, so completing this record's own body after the run cannot move the canon
share or the finding set. The status headers — the only bytes of these two
files the report's families read — are the ones the run saw.

## 7. `python3 -m pytest tests/doc-health -q`

```
$ python3 -m pytest tests/doc-health -q
1710 passed, 7 warnings in 530.68s (0:08:50)
```

**exit 0.** Control in the `origin/main` `38c076d1` worktree:

```
$ python3 -m pytest tests/doc-health -q
1689 passed, 7 warnings in 517.55s (0:08:37)
```

**exit 0.** **1689 → 1710, +21, AND THE RISE IS THE NEW FILE ENTIRE**:
`grep -c '^def test_' tests/doc-health/test_grandfather_dispositions.py`
returns **21**. No existing test is edited, renamed, flipped or deleted. This
pair is the packet's ONE test count; `proposal.md`'s front matter, `tasks.md`
§ 3.7, § 3.8, § 5.8 and § 5.13, and the pull request body all state it and no
other.

## 8. `python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs tests/proposal-support -q`

```
$ python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs tests/proposal-support -q
2199 passed, 7 warnings, 66 subtests passed in 610.04s (0:10:10)
```

**exit 0.** The `tests/doc-health` share of that total is the 1710 of § 7; the other three selections contribute 489 and the 66 subtests.

## 9. The PINNED 1.12.0 binary — `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
…
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
Totals: 99 passed, 2 failed (101 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**exit 0.** Both failures are the PRE-EXISTING dispositioned scenario-omission
findings accepted on Brett Heap's word of 2026-09-05 *"take exit 2"*; neither
is this change and neither is touched here. `spec/doc-health` — the
specification this packet's block is written over — is among the passes, with
three `INFO` length notes and no `ERROR`.

## 10. THE AGGREGATION MEASUREMENT, RE-TAKEN ON THE RATIFIED TREE

**THE RIG, NAMED SO IT CAN BE REBUILT.** `opensoft/xFactory` cloned at
`f5dba67f` (today's `main`); its `health/dispositions.yaml` is blob
`1f4e1cef236dc4d2cbcbd0197e67397cca803b47`, **41 entries across 8 families,
18 of them `family: ratified-provenance`** (15 `openxFactory`, 3
`codexFactory`), every one dated, cited and naming a path under
`openspec/changes/archive/`; `xFactories/codexFactory` materialized at
`ef180510`, **the pin that aggregation head carries**; `openxFactory`
materialized under it at each side of the comparison. Command, on each side:
`python3 scripts/doc-health.py --repo-root <aggregation> --family
ratified-provenance --as-of 2026-09-11`.

| run | scripts from | `openxFactory` under the aggregation | rows | critical | info | exit |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| **R1** | `origin/main` `38c076d1` | `origin/main` `38c076d1` | 35 | **35** | 0 | 0 |
| **R2** | this ratified tree | `origin/main` `38c076d1` | 35 | **20** | **15** | 0 |
| **R3** | this ratified tree | this ratified tree | 35 | **20** | **15** | 0 |

- **R1 → R3 is the before/after.** Same 35 `(repo, path)` keys on both sides
  (`SAME KEY SETS: True`); `rows whose severity moved: 15`; `rows
  byte-identical: 20`; **`moved == the disposition keys that are reported:
  True`** — a set equality, not a count that happens to agree; `all moved paths
  archived: True`; **every moved row carries a `Cite:`**. The whole report diff
  is **62 changed lines**: the fifteen findings in each of the TWO places the
  report renders them (`## Findings By Family` and `## Ranked Plan`, 30 lines a
  side) and the one headline each side,
  `35 critical, 0 error, 0 warning, 0 info` →
  `20 critical, 0 error, 0 warning, 15 info`. The Ranked Plan keeps all **35**
  rows: an `info` row is re-banded there, not dropped.
- **R2 == R3 BYTE FOR BYTE** — all 35 finding lines identical — so **the
  packet's own new documents add no finding of their own in the aggregation
  scope either**, which is the aggregation-scope counterpart of § 6's
  normalized-identical single-repo report.
- **The downgraded row survives the report grammar.**
  `report.unparsed_plan_rows` over R3 returns `[]`, and `report.parse_previous`
  returns **20** keys and **0** contested — the fifteen leaving the regression
  axis (only `critical`/`error` rows enter `keys`) and entering no other.
- **All fifteen moved rows carry the SUBJECT-arm rule** (#878's shape) behind
  the `GRANDFATHERED by a recorded disposition — ` prefix, keeping their
  family, repo, path and `auto-fixable` resolution class.

**ONE FIGURE HAS MOVED SINCE `design.md` D0 AND IT IS RECORDED RATHER THAN
SMOOTHED.** D0 measured **18** rows moving, against `opensoft/xFactory`
`bc84d325` with `codexFactory` @ `a67fb0ae`; today **15** move. The file still
records eighteen entries for this family and every one of them is still dated,
cited and archived — what changed is the CORPUS, not the packet: **codexFactory's
three records have since been REPAIRED** and now carry a `Ratified:` citation
at the pin this aggregation head holds, so they draw no `ratified-provenance`
finding for a disposition to downgrade:

```
codexFactory openspec/changes/archive/2026-09-05-add-floor-addition-grace/review/ratification-2026-09-05.md
codexFactory openspec/changes/archive/2026-09-09-adopt-openspec-cli-pin-gate/review/ratification-2026-09-05.md
codexFactory openspec/changes/archive/2026-09-09-prepare-openspec-1.12-readiness/review/ratification-2026-09-05.md
```

`dispositioned AND currently reported: 15`; `dispositioned but NOT reported:
3`. **THAT IS THE STALE-DISPOSITION POPULATION `tasks.md` § 7.1 NAMES, AND IT
IS NO LONGER ZERO** — § 7.1 recorded it as zero when it was measured and stays
UNTICKED as the successor's act; this capture is the evidence a successor
starts from. **NOTHING IN THE PACKET DEPENDS ON THE NUMBER**: the rule is a set
equality over whatever the file records and whatever the run reports, and the
arm honours neither a stale entry nor an unrecorded finding.

## 11. The malformed-FILE guards, measured end to end on the ratified tree

`tasks.md` § 3.9's claim, re-taken here rather than recalled. Over the same
aggregation with `health/dispositions.yaml` replaced by a single scalar
(`42`):

```
$ python3 scripts/doc-health.py --repo-root <aggregation> --family ratified-provenance --as-of 2026-09-11   # origin/main 38c076d1
Traceback (most recent call last):
  …
  File ".../scripts/doc_health/runner.py", line 758, in main
    for d in (_yaml.safe_load(dispo_path.read_text()) or []):
TypeError: 'int' object is not iterable
```

**exit 1 on `origin/main`**, at the runner's own unconditional read — which
fires on every aggregation run with or without this packet. The same command
from this tree:

```
Findings: 35 critical, 0 error, 0 warning, 0 info. New regressions vs previous report: 0.
```

**exit 0** — the file records nothing, so nothing is honoured and every row
stays `critical`.

**AND THE GUARDS CHANGE NO REPORT OVER THE REAL FILE, WHICH IS PROVED BY DIFF
RATHER THAN ASSERTED.** A probe build of this tree's `scripts/` with BOTH
guards removed, run against the real aggregation, produces a report
**byte-identical** to R3 (`diff` exit 0, 0 lines). The guards change only
whether a malformed FILE aborts the run.

The unit pin is asserted both ways:
`test_a_malformed_dispositions_FILE_is_ignored_rather_than_aborting_the_run`
FAILS on the pre-fix module with
`TypeError: 'int' object is not iterable` at
`scripts/doc_health/promotion_fidelity.py:757` and PASSES on the fix.

## 12. Independent review

**COPILOT** reviewed five times — 2026-09-11T02:44Z, 03:27Z, 10:18Z, 11:01Z and
11:44Z — opening **five threads across three of those rounds, ALL FIVE TAKEN,
ZERO UNRESOLVED**. Two of the rounds arrived after the ratifying word and both
were repairs to the realization and to this packet's accounting, reaching no
byte of the delta. The dispositions, including the two items REFUSED in round 3
with their reasons, are in `review/ratification-2026-09-11.md` § 4 and in
`tasks.md` § 5.10, § 5.11 and § 5.12 rather than repeated here. Round 5
(11:44Z) opened no thread; its two suppressed comments are the single count
inconsistency, settled by `5a8bba3e`.

**SOURCERY** posted a reviewer's guide and a summary at 2026-09-11T02:40:09Z
and **no finding**.

**SONARCLOUD's QUALITY GATE PASSED** at 2026-09-11T11:41:31Z — 0 accepted
issues, 0 security hotspots, 3 new issues raised, none blocking the gate.

**CODEX NEVER REVIEWED THIS PULL REQUEST AT ANY HEAD.** Exactly ONE review
request was made by this lane, at 2026-09-11T12:34:54Z on head `ad6d542c`
(comment
[`5634508719`](https://github.com/opensoft/openxFactory/pull/945#issuecomment-5634508719)),
and the connector answered nine seconds later at **2026-09-11T12:35:03Z**
(comment
[`5634510364`](https://github.com/opensoft/openxFactory/pull/945#issuecomment-5634510364)),
verbatim:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard.
> To continue using code reviews, you can upgrade your account or add credits
> to your account and enable them for code reviews in your settings.

**THAT IS AN ABSENCE AND IT IS RECORDED AS ONE, NEVER AS APPROVAL.** No second
request was made: a further request would draw the same refusal and the estate
allows one.

## 13. What the encode does NOT move — verified by diff, not by assertion

| claim | proof |
| --- | --- |
| **The delta's bytes are untouched since the word.** | `git diff --name-only 468df2ef..HEAD -- openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/specs/` → **0 files**. D1 and D2 were ruled to the options already encoded, so the ruling is applied by leaving the text alone. |
| **Nothing under `openspec/specs/` moves by this encode.** | No promoted file is in the ratification commit's change set; promotion is the ARCHIVE's act. |
| **The `origin:` block is byte-unmoved.** | `.openspec.yaml` lines 1–86 (`kind`, `id`, `reason`, `proposed_by`, `proposed_on`) hash to sha256 `486829b1c9571584e9bed5d299b7283a70af697068d35b3b9bf8648139691def` both before and after the encode. |
| **The approval pair is an ADDITION, not a rewrite.** | `git diff --numstat` on `.openspec.yaml` reads **`42  0`** — forty-two lines added, zero removed. |
| **No `tasks.md` box outside § 1 is ticked by the encode.** | § 6 and § 7 remain entirely `- [ ]`. |
| **The pull request closes no issue.** | `closingIssuesReferences` is `[]`, re-read after the body rebuild; `refs #939` only, in the body and in every commit message on this branch. |

Whole-encode `git diff --numstat` (the ratification commit):

```
34	11	README.md
42	0	openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/.openspec.yaml
57	22	openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/design.md
19	11	openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/proposal.md
126	43	openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/tasks.md
```

plus the two new files under `review/` — this record and
`review/ratification-2026-09-11.md`, both ADDED in this commit, nothing removed.
