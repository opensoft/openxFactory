# Verification record: amend-modified-block-currency-standing, SECOND RUN after the merge of 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Rerun of: `review/verification-2026-09-10.md` (the pre-merge capture, preserved unedited and NOT superseded)
Ratified by: amend-modified-block-currency-standing — 2026-09-10, Brett Heap, "Ratify as encoded, all four sites" (record `review/ratification-2026-09-10.md`)

**A SECOND RUN WRITES A DIFFERENT PATH, AND THIS IS THAT PATH.**
`document-lifecycle` holds that a one-shot capture — *"a simulation report, an
audit output, a dated run report, a byte-exact evidence snapshot"* — keeps
`record`, and that **"a second run of such a generator writes a different path
rather than rewriting the same one"**. Both runs fall on 2026-09-10, so the
paths are distinguished by suffix rather than by date: the pre-merge capture at
`review/verification-2026-09-10.md` is **PRESERVED BYTE-FOR-BYTE** as it was
committed at `c95b9e50`, and this file is the SECOND run at its own path.

**AND IT IS A LATER RUN, NOT A SUPERSESSION.** `document-lifecycle`'s *A
document is superseded* puts the obligation on the PREDECESSOR — it would have
to move to `superseded` naming its successor, or be deleted — which is an edit
to the very capture the rule above orders preserved. So this file claims no
supersession. **`review/verification-2026-09-10.md` keeps `Status: record`, is
not moved to `superseded`, and is not deleted.** What it carries is what was
measured on the pre-merge tree; what this file carries is the CURRENT
measurement. Both are true of their own trees. Its § 0 row *"merge from main:
NONE OWED"* was true when written and is answered by this run: an addendum
pointer at the foot of that file names this path, and adds nothing else.

## 0. Why there is a second run at all

**`origin/main` MOVED WHILE THE ENCODE WAS BEING WRITTEN AND VERIFIED, AND THE
PULL REQUEST WENT CONFLICTING.** `main` was `804a9170` at the clone, at the
frozen bench head `ab8247fa`, and at every figure in the pre-merge capture. It
advanced to `b91af6ea` — PR #886 (`accept-sequenced-after-header-line`,
ratified and realized) together with #891 and #883 — after those figures were
taken and before this branch was pushed. GitHub reported the pull request
`CONFLICTING` on `README.md`.

**THE MERGE WAS TAKEN HERE RATHER THAN LEFT TO LANDING**, at `2e84325a`
(parents `c95b9e50` — the ratification encode — and `b91af6ea`), so the
re-measure is owed at THIS act and not at the landing act.

**AND THE RE-MEASURE IS NOT A FORMALITY, BECAUSE `main` MOVED THREE OF THE
GATES THEMSELVES.** What `b91af6ea` brings that the pre-merge tree did not have:

| brought by `main` | why it reaches this packet |
| --- | --- |
| `scripts/doc_health/families.py` + `corpus.py` (#890, `804a9170`) | the `ratified-provenance` **SUBJECT arm** (#878): a `review/ratification-*` record is read whatever status it carries. The pre-merge tree's `doc_health` predated this, so the pre-merge capture's `ratified-provenance` figures were taken WITHOUT the arm that scores this packet's own new ratification record |
| `scripts/proposal-support.py` (#886, +657 lines) | § 3's gate, re-run here against the new implementation |
| `scripts/sequenced_after.py` + `scripts/frontmatter_strict.py` (#886) | § 4's gates, and the header-line reader the same change promoted |
| `tests/sequenced_after/corpus-ledger.yaml` (one row, `#886`) | the sweep ledger grows to 193 rows; both sides' rows are present after the merge |
| `docs/document-lifecycle.md` (#886) | the lifecycle document this packet's records are written against |

**THE MERGE MOVED NO BYTE OF THIS PACKET.**
`git diff --stat c95b9e50 2e84325a -- openspec/changes/amend-modified-block-currency-standing/`
is **EMPTY**: no delta byte, no record body, no `.openspec.yaml` field, no task
box. The one conflict was pure adjacency in the README `## OpenSpec Records`
block — `main` had archived `amend-neutral-product-pin-interim-copy-vocabulary`
(removing its row) and added `accept-sequenced-after-header-line`'s row at the
top of Active changes, while this branch had rewritten the
`amend-modified-block-currency-standing` row in the same region. **RESOLVED BY
KEEPING BOTH ROWS**, `main`'s first byte-for-byte as `main` states it, then this
branch's ratified row byte-for-byte as `c95b9e50` wrote it; neither row's text
is edited by the merge, and the archived packet's row stays removed as `main`
removed it.

| item | value |
| --- | --- |
| tree these figures were taken on | `2e84325a` — the merge of the ratification encode `c95b9e50` with `origin/main` `b91af6ea` |
| `origin/main` at this run | `b91af6ea` |
| `--all --strict` control | a separate worktree of `origin/main` `b91af6ea` |
| `doc-health` control | `d5d8a2f3` — a separate worktree of `ab8247fa` with `b91af6ea` merged into it, resolved the same way: **the DRAFT packet on current `main`**, which isolates this encode's effect from `main`'s |
| the earlier run this one follows | `review/verification-2026-09-10.md`, preserved byte-identical to `c95b9e50`, `Status: record`, NOT superseded |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `TZ=UTC`, `openspec` CLI **1.2.0**, Python **3.12.3** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-modified-block-currency-standing --strict`

```
Change 'amend-modified-block-currency-standing' is valid
```

**Exit code 0.**

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 99 passed, 3 failed (102 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
three failures, on both sides:

| failing item | on `origin/main` `b91af6ea` | on the merged tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control reports `Totals: 98 passed, 3 failed (101 items)` —
`main` gained one PASSING item of its own since `804a9170`
(`accept-sequenced-after-header-line`). **The merged tree differs from it by
exactly ONE item and that item PASSES**: this change, the 102nd, rendering
`✓ change/amend-modified-block-currency-standing`. **This packet adds nothing to
the failure set and removes nothing from it**, and the two `✗` lists `diff` to
zero. The `spec/neutral-product-pin` failure is still the `requirements.16.text`
SHALL/MUST defect openxFactory #882 names, and none of the three is a
`doc-health` item.

## 3. `python3 scripts/proposal-support.py . verify amend-modified-block-currency-standing`

```
proposal support verification ok
```

**Exit code 0 — against `main`'s NEW `proposal-support.py`**, six hundred and
fifty-seven lines larger than the one the pre-merge capture ran. The
origin-retention arm still reads `kind`, `id`, `reason` and `proposed_by` as the
drafting lane declared them: the approval pair is an ADDITION beside them
(`git diff --numstat ab8247fa -- …/.openspec.yaml` = `37 0`), so nothing the
gate holds byte-stable moved. `tests/proposal-support` was run beside it and is
green (§ 7).

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0.**

### `--ledger-diff`

```
change ids (40 active + 153 archived): 193
co-modified at requirement granularity (each would owe a declaration): 140
sole modifiers (each would declare `sequenced_after: []`): 53
ACTIVE changes: co-modified / sole: 26 / 14
declaring an explicit `[]` root claim: 2
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 3 hop(s), from amend-mirror-floor-regeneration-merge-authority

per-change sweep ledger consistent with the corpus (193 rows).
```

**Exit code 0.** The ledger is consistent at **193 rows** — 192 before the
merge plus the one row `main` brought for `accept-sequenced-after-header-line`
(`moved_by "#886"`), with this packet's own row (`moved_by "#887"`) unmoved. The
merge auto-merged that file and **both sides' rows are present**. This change
remains one of the corpus's **two** explicit `[]` root claims.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

```
Findings: 32 critical, 5 error, 47 warning, 14 info. New regressions vs previous report: 0.
```

**Exit code 0.** **NO FINDING NAMES THIS CHANGE** —
`grep -c 'amend-modified-block-currency-standing'` over the full report returns
**0**, with all three of this packet's `review/` records inside the lifecycle
scan set.

**THE CRITICAL COUNT ROSE FROM 11 TO 32 AND NONE OF THE RISE IS THIS PACKET'S.**
It is `main`'s own standing population, newly VISIBLE rather than newly created:
#890's subject arm reads ratification records that were always out of contract
and that a value-scoped family never opened (#877 measured fourteen archived
ones). The control run proves the attribution:

### The control that matters: the finding-line diff against the DRAFT packet on the SAME main

`doc-health --single-repo` was run on `d5d8a2f3` — `ab8247fa` with `b91af6ea`
merged in and the README resolved identically, i.e. **the same tree carrying the
DRAFT packet instead of the ratified one** — and the two reports' finding lines
were normalized for the worktree name and compared:

```
--- draft-packet-on-main (d5d8a2f3) vs ratified-packet-on-main (2e84325a) ---
IDENTICAL   (98 finding lines on both sides)
```

**THE FINDING-LINE DIFF IS EMPTY.** Flipping three documents to
`Status: ratified` with one citation each, adding the approval pair, and adding
three `review/` records adds **ZERO** findings and removes **ZERO**, measured on
current `main` with the subject arm ACTIVE. Both sides report
`32 critical, 5 error, 47 warning, 14 info` and *"New regressions vs previous
report: 0"*.

### The `ratified-provenance` family, with the SUBJECT arm now live

`python3 scripts/doc-health.py --single-repo . --family ratified-provenance`,
**exit code 0**: **28 critical, and NONE of them this change** (named 0 times).
The control reports the same **28**. Broken down by rule:

```
21  document-lifecycle, *A review record records a ratification*      <- the #878 SUBJECT arm
 5  ratified header carries no citation in either sanctioned spelling
 1  Ratified: names none of an approver, a date, or a resolvable record path
 1  Ratified by: missing or does not resolve to an OpenSpec change
```

**THIS PACKET'S NEW RATIFICATION RECORD ENTERS THE SUBJECT ARM'S POPULATION AND
CLEARS IT AT NO COST** — twenty-one other records fail the rule it satisfies.
`review/ratification-2026-09-10.md` carried `Status: ratified`, `Kind: report`,
`Decision date:`, `Ratifier:` and exactly ONE `Ratified:` citation from its
first commit, and its H1 is the `# Proposal Ratification: <change>` form the arm
recognizes — so both recognizers (path and H1) find it and the rule passes. The
two `verification-*` captures keep `Status: record` and the arm does not reach
them: their subject is the GATE RUN, which is the sibling scenario *A review
record is not about a ratification*.

### `record-immutability` and `status-validity`

`--family record-immutability`, **exit code 0**: **4 critical**, all `docs/`
documents, **none this change**. `--family status-validity`, **exit code 0**:
**1 error**, pre-existing and not this change
(`openspec/changes/disposition-codexfactory-declared-renames/review/ratification-2026-09-05.md`
— missing status header). Both counts are identical on the control.

## 7. pytest

```
2036 passed, 7 warnings in 416.92s (0:06:56)
```

**Exit code 0** for `python3 -m pytest tests/sequenced_after tests/scope_globs
tests/doc-health -q` — 2,036 tests, up from the pre-merge capture's 1,979
because `main` brought `tests/sequenced_after/test_header_line.py` with #886.

```
128 passed, 67 subtests passed in 50.64s
```

**Exit code 0** for `python3 -m pytest tests/proposal-support -q`, run because
`main` rewrote the gate that suite covers. **No test was added, changed, skipped
or xfailed by this ratification or by the merge** — `code_surface: none`, and
§ 9 shows the branch touches no file under `scripts/` or `tests/` other than the
one sweep-ledger row.

## 8. `modified-block-currency` — the family that reads this very block

`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`,
**exit code 0**:

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 9 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**ALL SEVEN CLASSES ARE ZERO ON THIS BLOCK**, `marker defects: 0`, and this
change is named **0** times in the family report. `main` moved no byte of
`openspec/specs/doc-health/spec.md` and no byte of
`scripts/doc_health/modified_block_currency.py`, so the block is still written
over the canon it was sliced from and the family still reads it as 143 canon
units, 154 block units, 5 uncarried, all 5 named by the marker and suppressed.

## 9. What the merged branch changes against current `main` — the whole surface

`git diff --stat b91af6ea 2e84325a`:

```
README.md                                          |  66 +
openspec/changes/amend-modified-block-currency-standing/.openspec.yaml       | 124 +
openspec/changes/amend-modified-block-currency-standing/design.md            | 284 +
openspec/changes/amend-modified-block-currency-standing/proposal.md          | 250 +
openspec/changes/amend-modified-block-currency-standing/review/ratification-2026-09-10.md  | 386 +
openspec/changes/amend-modified-block-currency-standing/review/verification-2026-09-10.md  | 326 +
openspec/changes/amend-modified-block-currency-standing/specs/doc-health/spec.md           | 556 +
openspec/changes/amend-modified-block-currency-standing/tasks.md            | 235 +
specs/019-modified-block-currency-family/spec.md   |  26 +-
tests/sequenced_after/corpus-ledger.yaml           |   1 +
```

(plus this file, added by the commit that carries it.) **NOTHING UNDER
`openspec/specs/` IS TOUCHED** — no promoted canon moves, which is what makes
the archive a separate act. `git diff --name-only b91af6ea 2e84325a --
openspec/specs/ scripts/ .github/ contracts/` is **EMPTY**; the only files
outside the packet are the README row, the one sweep-ledger row, and
`specs/019-modified-block-currency-family/spec.md` — the SEVERABLE FR-018
commit `2f384fd1`, a Speckit build record catching up with canon promoted at
`250d93d7`, unmoved since it landed.

## 10. Independent review

Unchanged by the merge and stated in full at
`review/ratification-2026-09-10.md` § 4: **six threads across seven bench
rounds, all six TAKEN, zero unresolved**, with the ONE refusal (per-class
disappearance tracking in the checker) argued at § 4.3 and owed as an open box
at `tasks.md` § 5.3. Copilot's last verdict on the frozen head `ab8247fa` is
🔵 *"Needs a closer look"* with zero new comments; Codex never reviewed
`ab8247fa`, a second request having drawn a usage-limit notice (§ 4.4). The
merge and this second capture are a NEW head, so a fresh bench round is
requested on it and dispositioned before the freeze.

**THIS LANE ENCODES, MERGES, RE-MEASURES AND FREEZES; IT DOES NOT MERGE THE
PULL REQUEST.** The Rule 6 LANDING/LANDED post belongs to the landing lane on a
separate landing word.
