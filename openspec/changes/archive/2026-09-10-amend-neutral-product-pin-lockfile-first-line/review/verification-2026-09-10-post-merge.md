# Verification record: amend-neutral-product-pin-lockfile-first-line, SECOND RUN after the merge of 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Rerun of: `review/verification-2026-09-10.md` (the pre-merge capture, preserved unedited and NOT superseded)
Ratified by: amend-neutral-product-pin-lockfile-first-line — 2026-09-10, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-10.md`)

**A SECOND RUN WRITES A DIFFERENT PATH, AND THIS IS THAT PATH.**
`document-lifecycle` holds that a one-shot capture — *"a simulation report, an
audit output, a dated run report, a byte-exact evidence snapshot"* — keeps
`record`, and that **"a second run of such a generator writes a different path
rather than rewriting the same one"**. Both runs fall on 2026-09-10, so the two
paths are distinguished by SUFFIX rather than by date, exactly as PR #908 did at
`60a3b23e` and PR #887 at `e65aed15`: the first capture at
`review/verification-2026-09-10.md` is the record of the tree `d6877c00`, and
this file is the SECOND run, on the merged tree `ec3612fa`.

**THE FIRST CAPTURE IS NOT EDITED AT ALL — NOT EVEN BY A POINTER.** It keeps
`Status: record`, is not moved to `superseded`, and is not deleted. Editing a
committed `review/*.md` is a reserved act in this lane, so the forward-looking
sentences that file wrote — *"This is the packet's FIRST and only gate
capture"*, *"a later re-run writes `verification-<later date>.md` beside it
rather than editing this file"*, and its § 0 row *"merge from `main`: **ONE, AND
IT IS ITS OWN COMMIT**"* — are **ANSWERED HERE rather than rewritten where they
stand**. Each was TRUE OF THE TREE IT WAS WRITTEN ON. Two of the three are
answered by this file existing at the suffixed path the first capture predicted;
the § 0 row is answered in § 0 below, which counts the merges from the branch's
own history rather than from that row.

**AND TWO FIGURES OF THE FIRST CAPTURE ARE CORRECTED HERE, IN PLACE OF EDITING
IT.** § 3 corrects an INFO count that never moved, and § 0 corrects a merge
count. Both are stated with the measurement that settles them, and neither
touches a delta byte, a requirement, a marker or a decision.

**ON PATHS.** Command lines are pasted as run. Where a tool echoes the absolute
path of the working clone or of a temporary npm prefix, that path is written
here as `<clone>` or `<tmp>` — machine-local scratch directories of no interest
to a later reader — and nothing else in any pasted line is altered.

## 0. Why there is a second run at all

**`origin/main` MOVED AFTER THE RATIFICATION ENCODE WAS COMMITTED**, and the
pull request went `mergeable: CONFLICTING`. The encode `d6877c00` was written on
a branch that already carried `main` @ `52e42be9`. `main` then advanced by FOUR
first-parent commits:

| commit | what it is |
| --- | --- |
| `edf0e24f` | mounts `opensoft/openXdox` as a submodule and pins it (PR #917, `split-opendox` task 5.1) |
| `90beb006` | signs the Gate-Rules Council admitting record, reconciled against the live tree (PR #912) |
| `d32509d3` | MERGES `amend-marker-declaring-nothing` — ratified, **with its realization**: the FOURTH and FIFTH marker-defect grounds (PR #908) |
| `17a3b816` | archives `relocate-review-authority-floor-mirror` (PR #925) |

**THE MERGE WAS TAKEN AS ITS OWN COMMIT AT `ec3612fa`** (parents `d6877c00` —
the ratification encode — and `17a3b816`).

### The merge count, corrected

The first capture's § 0 row reads *"merge from `main`: **ONE, AND IT IS ITS OWN
COMMIT**"*. **THE BRANCH CARRIED TWO MERGES AT THAT POINT, NOT ONE**, both
their own commits, and `git log --merges` says so:

```
$ git log --merges --oneline 0286c76c~1..d6877c00
45b02e31 Merge origin/main into change/amend-neutral-product-pin-lockfile-first-line
acecc773 Merge origin/main into change/amend-neutral-product-pin-lockfile-first-line
$ git log -1 --format='%h parents=[%p]' acecc773
acecc773 parents=[0286c76c 05c706d6]
$ git log -1 --format='%h parents=[%p]' 45b02e31
45b02e31 parents=[0125741d 52e42be9]
```

`acecc773` merged `05c706d6` BEFORE the bench — the merge the first capture's
own `tasks.md` § 4.9 describes, README conflict and all — and `45b02e31` merged
`52e42be9` BEFORE the encode. The row was counting the merge taken AT THE
RATIFICATION, which is the one it measured on, and it undercounts the branch's
history by one. **WITH THIS MERGE THE BRANCH CARRIES THREE**, two before the
encode and one after it.

### THE MERGE MOVES NO BYTE OF THIS PACKET

| diff | result |
| --- | --- |
| `git diff --stat d6877c00 ec3612fa -- openspec/changes/amend-neutral-product-pin-lockfile-first-line` | **EMPTY** |
| `git diff --stat d6877c00 ec3612fa -- openspec/changes/amend-neutral-product-pin-lockfile-first-line/review/` | **EMPTY** — no committed record edited |
| `git diff --stat d6877c00 ec3612fa -- openspec/changes/amend-neutral-product-pin-lockfile-first-line/.openspec.yaml` | **EMPTY** — the `origin:` block and the approval pair both unmoved |
| `git diff --stat 0125741d ec3612fa -- openspec/changes/amend-neutral-product-pin-lockfile-first-line/specs/` | **EMPTY** — the delta the bench reviewed is the delta on this tree |
| `git diff --stat 0125741d ec3612fa -- openspec/specs/neutral-product-pin/` | **EMPTY** — this requirement's promoted canon is unmoved |

and this packet's README `## OpenSpec Records` row is byte-identical across the
merge, the row extracted from both trees hashing to `c127e8a3…`. The merge's
ONE conflict was in that block and it was resolved as a UNION: main's ratified
`amend-marker-declaring-nothing` row keeps the position `main` gave it, this
packet's row sits directly below it, and the resolution with this packet's 84
lines removed is BYTE-EQUAL to `origin/main`'s README — 9,214 lines on both
sides. `tests/sequenced_after/corpus-ledger.yaml` auto-merged as the same
union, both sides' rows kept.

### SO THE RE-MEASURE IS NOT A FORMALITY: `main` MOVED THE FAMILY THAT READS THIS VERY BLOCK

`d32509d3` lands PR #908's realization.
`scripts/doc_health/modified_block_currency.py` gains **122 lines** and
`tests/doc-health/test_modified_block_currency.py` **236** — grounds FOUR and
FIVE, the arm's docstring now reading *"FIVE GROUNDS, ONE CLASS, ONE ACTION"*.
**THIS PACKET'S `tasks.md` § 3.6 CLAIMED ITS MARKER CANNOT FIRE EITHER NEW
GROUND, AND IT CLAIMED IT AGAINST A DRAFT.** That draft is now the SHIPPING
predicate, so § 9 re-derives the claim against the shipped code rather than
against the proposal. `17a3b816` and `d32509d3` also move the corpus every
`--all --strict`, ledger and `doc-health` total is taken over.

Every figure below is taken again from zero on `ec3612fa`; nothing is carried
forward from the first capture. Where a figure MOVED, the section names the
commit on `main` that moved it and shows the movement is main's own.

| item | value |
| --- | --- |
| clone | a fresh clone isolated from any shared checkout, `origin` pointed at `https://github.com/opensoft/openxFactory.git` |
| tree these figures were taken on | `ec3612fa` — the merge commit, head of `change/amend-neutral-product-pin-lockfile-first-line` |
| head the ratification was authorized on | `0125741d` — the frozen bench head, unchanged |
| the ratification encode | `d6877c00` |
| merges from `main` | **THREE**: `acecc773` and `45b02e31` BEFORE the encode, `ec3612fa` AFTER it |
| `origin/main` at this verification | `17a3b816` |
| `--all --strict` and pinned-CLI control | a separate worktree of `origin/main` `17a3b816` |
| `doc-health` controls | TWO, each in a worktree whose directory basename matches this clone's so the `Repo-Identity` label is identical and the diff is LITERAL: `origin/main` `17a3b816`, and the PRE-MERGE ratified tree `d6877c00` |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `openspec` CLI on `PATH` **1.2.0**, pinned CLI **1.12.0**, Python **3.12.3**, node **v22.22.2**, npm **11.19.0** |

**BOTH BINARIES ARE MEASURED AGAIN, BECAUSE `design.md` D6 IS ABOUT THE
DIFFERENCE BETWEEN THEM** and D6 is the decision the word resolved first. § 2 is
the 1.2.0 binary on `PATH`, where this specification FAILS; § 3 is the pinned
1.12.0 the required check actually runs, where it PASSES.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-neutral-product-pin-lockfile-first-line --strict`

```
Change 'amend-neutral-product-pin-lockfile-first-line' is valid
```

**Exit code 0.** Unchanged from the first capture, and it is the same delta: the
merge edits no file of this packet, so the block the bench reviewed and the word
ratified is validated again, byte for byte.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` (1.2.0 on `PATH`)

```
Totals: 98 passed, 4 failed (102 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
four failures, on both sides:

| failing item | on `origin/main` `17a3b816` | on `ec3612fa` |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `change/disposition-codexfactory-floor-relocation-retitle` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `17a3b816`, reports
`Totals: 97 passed, 4 failed (101 items)`, exit 1. **The branch differs by
exactly ONE item and that item PASSES** — this change itself, rendering
`✓ change/amend-neutral-product-pin-lockfile-first-line`. `diff` over the two
sorted `✗` lists emits NOTHING (exit 0), and `diff` over the two sorted FULL
item lists emits exactly the one added line:

```
$ diff all-main.txt all-branch.txt
25a26
> ✓ change/amend-neutral-product-pin-lockfile-first-line
```

**NEITHER TOTAL MOVED SINCE THE FIRST CAPTURE, AND THAT IS AN ACCIDENT OF
ARITHMETIC RATHER THAN A STILL CORPUS** — branch `102 items` both times, control
`101 items` both times. `d32509d3` added `amend-marker-declaring-nothing` to the
validated set and `17a3b816` took `relocate-review-authority-floor-mirror` out
of it by archiving, so the two movements cancel. **The failure set did not move
either: same four names, same count, as recorded on `45b02e31`.**

### `spec/neutral-product-pin` STILL FAILS, AND THAT IS THE CORRECT STATE

It is the very failure this packet exists to answer, and the merge does not
touch it:

```
$ OPENSPEC_TELEMETRY=0 openspec validate neutral-product-pin --strict --type spec
Specification 'neutral-product-pin' has issues
✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST keyword
Next steps:
  - Ensure spec includes ## Purpose and ## Requirements sections
  - Each requirement MUST include at least one #### Scenario: block
  - Re-run with --json to see structured report
```

**Exit code 1.** **A DELTA DOES NOT EDIT THE PROMOTED SPECIFICATION.** Nothing
under `openspec/specs/neutral-product-pin/` is touched by this pull request —
the file's blob is `e75ec6a1` on `0125741d`, `45b02e31`, `d6877c00`, `ec3612fa`
AND `17a3b816`, one identical object across all five trees — so the promoted
requirement still opens its body with `Where a pinned external neutral product
…` and 1.2.0 still errors on it. **THE ARCHIVE ACT IS WHAT CLEARS THIS**, by
promoting the `## MODIFIED` block into the specification — a separate act on a
separate word, `tasks.md` § 5. This record states it rather than letting a later
reader discover a red item and read it as a regression. The other three failures
are pre-existing, none is a `doc-health` item, and this packet edits no file any
of them reads.

## 3. The PINNED CLI, which is the one the gate runs

The `openspec` on `PATH` is **1.2.0** and `contracts/openspec-cli-pin.yaml:255`
pins **1.12.0**, so the required arm was run through the pinned artifact.
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` — the literal
form `.github/workflows/openspec-cli-pin-gate.yml` runs — **exit 0**:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<tmp>/prefix/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
-> <tmp>/prefix/node_modules/.bin/openspec validate --all --strict --json  (in <clone>)
…
Totals: 100 passed, 2 failed (102 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The `origin/main` `17a3b816` control, run the same way in its own worktree,
reports `Totals: 99 passed, 2 failed (101 items)`, **exit 0** — one item fewer,
and the one item is this change, which passes.

The two failures are the two DISPOSITIONED scenario-omission findings accepted
on Brett Heap's word of 2026-09-05 *"take exit 2"* — `add-chain-attestation` /
`signed-execution-chain` and `add-composed-view-authoring` /
`ideation-dashboard`. Neither is this packet's, neither is related to this
requirement, and this packet neither renews nor retires either one.

### `spec/neutral-product-pin` IS AMONG THE PASSES ON THIS BINARY — AND THE INFO COUNT IS CORRECTED

It carries INFO notes only and **no `✗`**: a `grep -c '✗'` over its section of
the pinned run reads **0** on the branch and **0** on the control. **THAT IS
D6's WHOLE POINT**: the failure this amendment answers is real on the binary an
engineer or an agent has on `PATH` and is reported by NO required check. The
ruling of 2026-09-10 amended anyway, with this measurement in front of the
owner.

**THE FIRST CAPTURE'S § 3 SAID THOSE NOTES WERE "nineteen of them across the
file". THE COUNT IS SEVENTEEN, AND IT NEVER MOVED.** Measured on this tree and
on the `17a3b816` control, a `grep -c 'INFO'` over that section of the pinned
run reads **17** on BOTH; the notes are `requirements[0]` … `requirements[3]`,
`requirements[5]` … `requirements[17]`, one per requirement except index **4**,
each *"Requirement text is very long (>500 characters)"*. An independent count
straight off the file agrees: of the specification's **18** requirements, **17**
have a body of more than 500 characters. And the figure could not have moved
between the two captures, the spec blob being the single object `e75ec6a1` on
all five trees. **THE FIRST CAPTURE MISCOUNTED IT.** Nothing else in that
section is affected: the exit code, the totals, the zero `✗` and the two
dispositioned exceptions were each re-measured and each came out the same.

## 4. `python3 scripts/proposal-support.py . verify`

The whole-corpus form, which is what the gate runs:

```
proposal support verification ok
```

**Exit code 0.** And named at this change,
`python3 scripts/proposal-support.py . verify amend-neutral-product-pin-lockfile-first-line`:

```
proposal support verification ok
```

**Exit code 0.** This is the gate that reads the `.openspec.yaml` origin
declaration, so it is the one most exposed to the approval pair the encode
added: it passes with the pair present and the drafting provenance unmoved —
and it passes again now that `main` has landed a second ratified packet of the
same shape beside it.

## 5. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0**, both archive-date arms passing — including on `17a3b816`'s new
archive directory `2026-09-10-relocate-review-authority-floor-mirror`.

### `--ledger-diff`

**Exit code 0**:

```
change ids (40 active + 157 archived): 197
co-modified at requirement granularity (each would owe a declaration): 143
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 25 / 15
declaring `sequenced_after:`: 22 (… amend-marker-declaring-nothing, … amend-neutral-product-pin-lockfile-first-line, …)
declaring an explicit `[]` root claim: 5
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (197 rows).
```

**THE LEDGER IS CONSISTENT AT 197 ROWS AND THIS PACKET MOVED NONE OF THEM AT
THIS MERGE.** The ledger grew 196 → 197 and **the diff against the first
capture's tree is exactly THREE lines, none of them this packet's**:

```
$ git diff d6877c00 ec3612fa -- tests/sequenced_after/corpus-ledger.yaml
+  amend-marker-declaring-nothing: {state: active, class: co-modifier, declares: [], depth: 0, prose: false, moved_by: "#908", moved_on: "2026-09-10"}
-  relocate-review-authority-floor-mirror: {state: active,   … moved_by: "#817", moved_on: "2026-09-09"}
+  relocate-review-authority-floor-mirror: {state: archived, … moved_by: "#925", moved_on: "2026-09-10"}
```

`moved_by: "#908"` and `moved_by: "#925"` name the pull requests that moved
them. **THIS PACKET'S TWO ROWS ARE BYTE-IDENTICAL ACROSS THE MERGE** — its own
`amend-neutral-product-pin-lockfile-first-line: {state: active, class:
co-modifier, declares: [], depth: 0, prose: false, moved_by: "#923", moved_on:
"2026-09-10"}` and the partner flip on the archived promoter
`pin-openspec-cli-dependency-closure: {state: archived, class: co-modifier,
declares: absent, prose: false, moved_by: "#923", moved_on: "2026-09-10"}`, both
seeded at `44020530` through the sanctioned `--seed-ledger --moved-by '#923'`
path before the freeze.

The three derived totals that moved are main's arithmetic: archived 156 → 157
and active 40 → 40 (`relocate-review-authority-floor-mirror` leaving the active
set as `amend-marker-declaring-nothing` enters it), `declaring
sequenced_after:` 21 → 22 and explicit `[]` root claims 4 → 5 (the new active
packet declares `[]` too). **This change remains one of those root claims.**

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 7. `python3 scripts/doc-health.py --single-repo .`

**Exit code 0.**

```
Canon share by words: 39.8% (368379 canon words / 925705 governance words, promoted specs included).
Findings: 32 critical, 5 error, 47 warning, 15 info. New regressions vs previous report: 0.
```

**NO FINDING NAMES THIS CHANGE.** `grep -c
'amend-neutral-product-pin-lockfile-first-line'` over the whole 348-line report
reads **0**, and reads **0** on both controls too.

### The two controls: the branch is IDENTICAL to `main`, and the MERGE is what moved the report

Each control ran in a worktree whose directory basename is `merge-923`, the same
as this clone's, so all three reports carry `Repo-Identity: merge-923` and the
comparison is a LITERAL byte diff with nothing normalized away:

| control | tree | lines | `md5` of the report | result |
| --- | --- | --- | --- | --- |
| this tree | `ec3612fa` | 348 | `22f7ead9d784ecc4cf5feee1d7120218` | — |
| `origin/main` | `17a3b816` | 348 | `22f7ead9d784ecc4cf5feee1d7120218` | **IDENTICAL**, `diff` emits nothing |
| the PRE-MERGE ratified tree | `d6877c00` | 350 | `b56efd5bebe64e914dd600d2a4f4bca6` | differs by 2 finding lines, ALL of them main's |

All three exit **0**. The first control says **this branch adds no doc-health
finding to `main` and removes none** — which is the claim that matters, and it
is byte-exact. The second says the MERGE moved two finding lines, and **both
movements are `17a3b816`'s archive of another lane's packet, not this
packet's**: `relocate-review-authority-floor-mirror`'s `ratified-provenance`
critical follows its record from `openspec/changes/…` to
`openspec/changes/archive/2026-09-10-…` (a MOVE, not a new finding — the
critical total stays 32), and its `modified-block-currency` carriage-ledger
`info` DISAPPEARS because an archived change no longer has an active MODIFIED
block, taking the carriage ledger 11 → 10, `info` 16 → 15 and the finding count
100 → 99. Canon share moved 39.7% → 39.8% because that archive promoted a block
into `openspec/specs/review-lane-floor-mirror/spec.md` (+795 promoted words).

### By family on the merged tree, and none of it this packet's

| family | count | any of them this packet's? |
| --- | --- | --- |
| `ratified-provenance` | 28 | **NO** |
| `staged-candidate-aging` | 24 | **NO** |
| `staged-topic-template` | 22 | **NO** |
| `modified-block-currency` | 10 | **NO** |
| `tag-hygiene` | 4 | **NO** |
| `record-immutability` | 4 | **NO** |
| `ideation-routing` | 4 | **NO** |
| `status-validity` | 1 | **NO** |
| `release-tag-publication` | 1 | **NO** |
| `document-catalog` | 1 | **NO** |
| **`marker-defect`** | **0 in the whole run** | — |

`ratified-provenance` is the family this encode is most exposed to, since it
reads a `review/ratification-*` record's SUBJECT whatever status it carries.
**This packet's ratification record is in that population and CLEARS it**,
carrying `Status: ratified` plus exactly one `Ratified:` citation. The 28 are
other packets' records.

### THIS FILE IS INSIDE THE SCAN SET — probed, not assumed

The three reports above were taken on trees before this record existed, so the
run was repeated once more with this file, the `tasks.md` § 4.11 line and the
README records-list edit all present. **Exit 0, 348 lines, and the SAME `md5`
`22f7ead9d784ecc4cf5feee1d7120218`.** A `record`-status report under `review/`
is read by the lifecycle families and scores nothing against them, so **this
capture adds no doc-health finding and removes none** — checked here rather than
assumed. `grep -c` over the post-edit report still reads **0**.

## 8. The test suites

`python3 -m pytest tests/sequenced_after tests/scope_globs tests/proposal-support -q`
— the three suites `tasks.md` § 4.8 names:

```
489 passed, 67 subtests passed in 62.98s (0:01:02)
```

**Exit code 0**, and the counts are UNMOVED from the first capture. Per
directory, collected on this tree: `tests/sequenced_after` **273**,
`tests/scope_globs` **88**, `tests/proposal-support` **128**. The 67 subtests
all come from `tests/proposal-support`'s ratifying-commit sweep, one per
directory of `openspec/changes/`; active changes stayed at 40 across the merge
(one archived, one arriving), so the sweep gained none.

`python3 -m pytest tests/doc-health -q` — **run because `main` moved this very
suite**:

```
1689 passed, 7 warnings in 430.09s (0:07:10)
```

**Exit code 0.** It was **1684** on the pre-merge tree, and the **+5** is
`d32509d3`'s: `tests/doc-health/test_modified_block_currency.py` collects
**144** on this tree and on `origin/main`, and **139** on `d6877c00` — PR #908's
139 → 144, arriving through the merge. **NOT ONE OF THE FIVE IS THIS PACKET'S**,
and this packet adds no test: § 10's diff shows it touches nothing under
`tests/`.

## 9. THE CLAIM THAT MOST NEEDED RE-MEASURING: the marker against the SHIPPING predicate

`tasks.md` § 3.6 claimed that neither the existing second marker-defect ground
nor **either ground the then-ACTIVE draft `amend-marker-declaring-nothing`
adds** can fire on this block's marker — a claim made against a PROPOSAL,
because that packet might land first. **IT DID LAND FIRST, at `d32509d3`, and
the claim is now re-derived against the code that ships.** Run against
`scripts/doc_health/modified_block_currency.py` AS MERGED, resolving this block
against promoted canon (`resolve` status `canon`, basis
`openspec/specs/neutral-product-pin/spec.md`):

| measure | value |
| --- | --- |
| the family's `_ARM_TEMPLATES` | **8**, unmoved — grounds four and five are one class, not two more templates |
| the arm's own docstring | *"FIVE GROUNDS, ONE CLASS, ONE ACTION"* |
| canon units in the promoted requirement | **25** — 9 body, 4 scenario titles, 12 scenario bullets |
| units in this change's block | **25** — 9 body, 4 scenario titles, 12 scenario bullets |
| uncarried canon units | **1** — `Where a pinned external neutral product is distributed as a published artifact …` |
| added block units | **1** — `The pin SHALL carry a VENDORED RESOLUTION where a pinned external neutral product …` |
| markers in the block | **1** |
| `suppression()` suppressed | **1** |
| **`suppression()` marker defects on this block** | **0** |
| marker form / change id / date | `removed` / `amend-neutral-product-pin-lockfile-first-line` / `2026-09-10` |
| marker names / quoted spans | **1** / **0** |
| code spans in the marker's reason | **0**, in a **1,167**-character reason |
| the four canon scenario titles | carried, **equal in order** (`True`) |

**EVERY NUMBER `tasks.md` § 3.3 AND § 3.6 CLAIM IS REPRODUCED, AND NOW AGAINST
THE SHIPPED GROUNDS RATHER THAN THE PROPOSED ONES.** Ground four needs a name
matching a unit the block itself ADDS; this marker's one name is the single
uncarried CANON unit, so it cannot reach it. Ground five needs a `Removed from
canon` marker whose tail carries no code span AND parses to `names = []`; this
marker names one unit, so it cannot reach that either.

**AND THE CLASS IS AT ZERO OVER THE WHOLE CORPUS.** Swept across all **31**
active `## MODIFIED` blocks on this tree, `suppression()` returns **0** marker
defects in total — `{}`, no change contributing one — which is why § 7's
`marker-defect` row reads 0 findings. Four blocks now carry unit-naming markers
(`add-chain-attestation`, `add-composed-view-authoring`,
`amend-marker-declaring-nothing` and this one), up from three, and all four are
sound.

## 10. What this merge does NOT move — verified by diff, not by assertion

| claim | how it is checked | result |
| --- | --- | --- |
| no packet file moves | `git diff --stat d6877c00 ec3612fa -- openspec/changes/amend-neutral-product-pin-lockfile-first-line` | EMPTY |
| no committed record edited | same, restricted to `review/` | EMPTY |
| the `.openspec.yaml` origin block unmoved | same, restricted to `.openspec.yaml` | EMPTY |
| the ratified delta unmoved since the frozen head | `git diff --stat 0125741d ec3612fa -- …/specs/` | EMPTY |
| this requirement's promoted canon unmoved | `git diff --stat 0125741d ec3612fa -- openspec/specs/neutral-product-pin/` | EMPTY |
| this packet's README row unmoved | row extracted from both trees, hashed | identical, `c127e8a3…` |
| the packet touches no script or test | `git diff --name-only 0125741d d6877c00 -- scripts/ tests/` | EMPTY |
| this packet touches no archived change | `git diff --name-only 0125741d ec3612fa -- openspec/changes/archive/` grepped for this change id | 0 hits |

The merge changes **30** files against `d6877c00` and **every one of them is
main's**, the union resolutions in `README.md` and
`tests/sequenced_after/corpus-ledger.yaml` included. The one movement under
`openspec/specs/` is `review-lane-floor-mirror/spec.md` (+31/−2), `17a3b816`
promoting another lane's block.

**PROMOTED CANON FOR THIS REQUIREMENT STILL OPENS WITH THE CONDITION.** Nothing
under `openspec/specs/neutral-product-pin/` is edited by the ratification or by
the merge; the `## MODIFIED` block writes over canon AT THE ARCHIVE, which is a
separate act on a separate word. `tasks.md` § 5 (archive) and § 6.1 stay OPEN,
and openxFactory #882 closes at that archive rather than at this landing —
which is why this pull request carries `refs #882`, no closing keyword, and
`closingIssuesReferences` `[]`.

## 11. What this record does not claim

It does not claim the landing is done, and it is not a landing record: no
landing word is recorded for this pull request. It does not archive the packet
and ticks no box of `tasks.md` § 5 or § 6. It does not supersede
`review/verification-2026-09-10.md`, which stands as the measurement of the tree
it was taken on — the two figures § 0 and § 3 correct are corrected HERE, and
that file is not edited. And it records no bot round of its own: the bench
disposition for the frozen head `0125741d` is written in
`review/ratification-2026-09-10.md`, and whatever a reviewer says about the
merged head is recorded on the pull request rather than rewritten into a
committed capture.
