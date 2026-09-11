---
code_surface: openxFactory — `scripts/doc_health/families.py` (four module constants and ONE new function, `_stale_grandfather_dispositions`, plus a two-line tail on `fam_ratified_provenance`) and the tests that pin them in `tests/doc-health/test_grandfather_dispositions.py` (the parent packet's own rig, extended). ONE SECOND LAST PASS IS ADDED TO ONE FAMILY AND NOTHING ELSE MOVES: `fam_ratified_provenance` returns `graded + _stale_grandfather_dispositions(ctx, graded)` instead of `graded`, and that pass reports — at `warning`, against the AGGREGATION's `health/dispositions.yaml` under the repository id `xFactory` that `fam_submodule_pin_drift` and `fam_notebook_projection_drift` already report the aggregation as — every entry this family HONOURS whose `(repo, path)` names no finding the run raised. The admission rule is NOT re-decided and NOT copied: the honoured set is `_grandfather_cites`, the same map the downgrade reads, so one rule serves both halves of the comparison. Two narrowings, each measured: an entry naming a repository absent from `ctx.repo_paths` is passed over (an unmaterialized submodule reports nothing, and every entry naming it would otherwise be called stale on a measurement nobody took), and a `--single-repo` run reports nothing at all (no aggregation root, no file, no entries). NOTHING ELSE MOVES: no arm, no scope, no document set, no threshold, no resolution class, no other family, no report field, no workflow, no contract member, no schema and no path; every finding the five arms and the downgrade pass build is returned as they built it, by identity, and the new rows are APPENDED. TWELVE tests are ADDED to the parent's file (22 -> 34 test functions, both counts re-measured on this tree and on an `origin/main` `8015d45f` worktree beside it). TWO existing tests in that file MOVE, and both moves are this change's own behaviour rather than a repair — `tasks.md` § 4.4 carries them individually.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` run at the tree the merge carries.
sequenced_after: []
---

# Proposal: report-stale-grandfather-dispositions

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`),
session `c44b04` (team-01f), on Brett Heap's word of 2026-09-11 at
approximately 18:20Z, verbatim **"usage reset, resume all. read handoff and
resume and fan out wide and do as much as possible in parallel"**.
Origin: openxFactory
[#965](https://github.com/opensoft/openxFactory/issues/965), filed by this lane
AT the archive of
[`honour-grandfather-dispositions-in-ratified-provenance`](../archive/2026-09-11-honour-grandfather-dispositions-in-ratified-provenance/proposal.md)
as the successor that packet's `tasks.md` § 7.1 owes, standing on
[#939](https://github.com/opensoft/openxFactory/issues/939) (the parent's
origin) and [#945](https://github.com/opensoft/openxFactory/pull/945) (the
parent's landing).

**THAT WORD COMMISSIONS THE AUTHORING, NOT THE CONTENT. RATIFICATION IS OWED
AND IT IS BRETT HEAP'S ACT.** Nothing below is ratified by being authored; no
requirement here may be cited as approved until he rules on this packet itself;
`.openspec.yaml` declares drafting provenance with **no approval pair**, and
every document in this packet carries `Status: draft`. **NOTHING IS PROMOTED** —
this pull request edits no file under `openspec/specs/`. Every judgment this
authoring session took is listed in `design.md` as **D0 through D5**, each with
a recommendation and each put for veto; the one most worth one is **D1**, put as
a MULTIPLE-CHOICE question over what a stale entry IS.

## Why

**THREE RECORDED RULINGS DISPOSE OF NOTHING, AND NO ARTIFACT ANYBODY READS SAYS
SO.**

The grandfather pass landed by PR [#945](https://github.com/opensoft/openxFactory/pull/945)
reads the aggregation's `health/dispositions.yaml` and downgrades a finding to
`info` exactly when the finding's `(repo, path)` carries a dated, cited
`family: ratified-provenance` entry and the path is archived. **The converse is
reported nowhere.** An entry naming a record that has since been REPAIRED, or a
path that has since VANISHED, matches no finding, moves no severity, and
appears in no row. It stops doing anything, silently, and the file keeps it.

The rule that arm implements is a **set equality** over *whatever the file
records* and *whatever the run reports*. It honours the intersection and
neither half of the difference — not the stale entry, and not the unrecorded
finding. This packet takes the first half. The second is a question about every
family at once and belongs to the other successor,
[#966](https://github.com/opensoft/openxFactory/issues/966).

**AND THE PARENT NAMED THIS CLASS RATHER THAN SMUGGLING IT IN.** `design.md` D6
of the archived packet:

> **No stale-entry check is added.** An entry naming a path that no longer
> exists, or a record since repaired, produces no `info` row and no complaint —
> the entry simply matches nothing. A family that reported stale dispositions
> would be a new finding class with its own severity and its own population,
> and it is named here as a successor rather than smuggled in. Measured today:
> all eighteen entries match a live finding, so the population of that
> successor is ZERO and there is nothing to lose by deferring it.

**IT IS NO LONGER ZERO.** That sentence was true at the parent's § 2.1 rig and
false by its § 5.13 rig, which is why § 7.1 re-measured the split rather than
carrying it, and why #965 exists.

## The measurement, taken before the design

Measured at authoring against the REAL aggregation dispositions file —
`opensoft/xFactory` `main` **`0ecb370e8fec2c1ac78498adf8f6a4ea3ca1c9bb`**, 49
entries, **18** of them `family: ratified-provenance` (15 `openxFactory`, 3
`codexFactory`), every one dated, cited, and naming a path under
`openspec/changes/archive/` — with each repository materialized under an
aggregation checkout at the pin that aggregation holds (`openxFactory`
`b91af6ea`, `codexFactory` `2dd4e5a3`):

| | entries | matching a finding | matching NOTHING |
| --- | ---: | ---: | ---: |
| `family: ratified-provenance` | 18 | 15 | **3** |

All **three** are codexFactory's, and all three are stale **by repair**: each
record now carries `Status: ratified` with a `Ratified:` line naming an
approver and a date, so no arm of this family opens a finding against it and
the entry that grandfathered it reaches nothing. **Zero are stale by a vanished
path** today; the arm reports both because it cannot tell them apart and does
not need to — its whole predicate is that the entry matched no finding.

**THE SPLIT IS NOT AN ARTEFACT OF A LAGGING PIN, AND THAT IS MEASURED RATHER
THAN ASSUMED.** The aggregation's `openxFactory` pin is **233 commits** behind
that repository's `origin/main` at the first authoring, so the same rig was
rebuilt with each repository at its own `origin/main` (`openxFactory`
`8015d45f`, `codexFactory` `dc67ad82`) and returns the **identical** 15/3
split — and rebuilt a THIRD time at the encode, both repositories having moved
since (`openxFactory` `c521504c`, the pin now **237** commits behind it;
`codexFactory` `c3108adc`), returning that **same** 15/3 split over the same
three codexFactory paths. The aggregation is byte-unmoved at `0ecb370e`
throughout.

## What changes

**ONE `## MODIFIED` REQUIREMENT, ONE SCENARIO ADDED AT ITS END, AND NOT ONE
BYTE OF PROMOTED TEXT EDITED.** The block is canon's own bytes — lines
**878–945** of `openspec/specs/doc-health/spec.md`, sliced rather than
transcribed, `sha256
138a0d51f42f77aa9f0418c5ec1570681f63e0409bc0a43596e8356dca06e5dd` on both sides
(canon's lines 878–945 at `origin/main` `c521504c`, and this delta's lines
5–72; taking the blank separator line 946 with them gives `sha256 ce2e4b13`
either side, which is the same equality one line longer) — with one
`#### Scenario:` appended. No body paragraph is added, edited or
removed; no promoted scenario moves, is retitled or loses a bullet; no marker is
declared, there being nothing removed to declare.

The added scenario, *A recorded disposition matches no finding*, says five
things: an honoured entry naming no finding this run raised is reported at
**`warning`** against the dispositions file's own path, quoting the entry's
target and the recorded citation; the finding is NOT raised against the record
the entry names; an entry naming a repository the run did not enumerate is not
reported; an entry this family would not honour is not reported either, one
admission rule serving both halves; and a run with no aggregation checkout
reports nothing of this class.

**THE REALIZATION RIDES THIS PULL REQUEST.** `scripts/doc_health/families.py`
gains four constants and one function, `_stale_grandfather_dispositions`, and
`fam_ratified_provenance`'s one-line tail becomes two. The pass runs AFTER the
downgrade, and that ordering is what makes the two compose: canon requires a
grandfathered finding to keep "its family, its repository and its path", so the
key set of the finding list is identical before and after the downgrade and the
difference reads the same either way.

## What this proposal does NOT do

- **It does not repair a record, and it does not prune an entry.**
  `health/dispositions.yaml` lives in `opensoft/xFactory` and is not touched by
  this pull request at all. The report says which line has stopped working; who
  prunes it, and whether, is the lifecycle owner's act.
- **It does not re-litigate a ruling.** Whether each grandfather's ground was
  sound was the lifecycle owner's act at `opensoft/xFactory` PR #420 and PR
  #412. This arm reads an entry as a record of a ruling and asks only whether it
  still reaches anything (`doc-health`, *Semantic finding disposition
  authority*).
- **It does not change what the downgrade honours.** Not one entry is admitted
  or refused differently: the stale set is the complement of the matched set
  over the SAME honoured map, `_grandfather_cites`.
- **It does not widen the mechanism to another family.** The 31 entries the
  other eight families carry at `0ecb370e` are #966's subject
  (`design.md` D5).
- **It does not give `--single-repo` a route to an aggregation dispositions
  file.** That is a CLI surface, an argument, a contract line and a test matrix,
  and it is [#968](https://github.com/opensoft/openxFactory/issues/968)'s open
  question rather than this packet's act.
- **It does not promote anything.** No file under `openspec/specs/` is edited.
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 965 is closed THERE, by a closing
  keyword written in the archive pull request and in no commit message on this
  branch.
