# Verification record: amend-marker-declaring-nothing, SECOND RUN after the merge of 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Rerun of: `review/verification-2026-09-10.md` (the pre-merge capture, preserved unedited and NOT superseded)
Ratified by: amend-marker-declaring-nothing — 2026-09-10, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-10.md`)

**A SECOND RUN WRITES A DIFFERENT PATH, AND THIS IS THAT PATH.**
`document-lifecycle` holds that a one-shot capture — *"a simulation report, an
audit output, a dated run report, a byte-exact evidence snapshot"* — keeps
`record`, and that **"a second run of such a generator writes a different path
rather than rewriting the same one"**. Both runs fall on 2026-09-10, so the two
paths are distinguished by SUFFIX rather than by date, exactly as this packet's
predecessor did at `e65aed15`: the first capture at
`review/verification-2026-09-10.md` is the record of the tree `705cecef`, and
this file is the SECOND run, on the tree `ff44d3bc`.

**THE FIRST CAPTURE IS NOT EDITED AT ALL — NOT EVEN BY A POINTER.** It keeps
`Status: record`, is not moved to `superseded`, and is not deleted. It differs
from its predecessor's handling in one way and the difference is deliberate:
`amend-modified-block-currency-standing` appended a one-line ADDENDUM to its
first capture pointing at its second, and **this lane appends nothing**, a
committed `review/*.md` being a reserved act here. The forward-looking
sentences the first capture wrote — *"the packet's FIRST and only gate
capture"*, *"IT IS ALREADY A POST-MERGE RUN, SO NO SECOND CAPTURE IS OWED AT
LANDING"*, and its § 0 row *"merges from `main`: **TWO, AND BOTH TAKEN
FIRST**"* — were **TRUE OF THE TREE THEY WERE WRITTEN ON** and are answered
HERE rather than rewritten there. A third merge landed after that file was
committed; the reconciliation is this file's job, and § 0 does it.

## 0. Why there is a second run at all

**`origin/main` MOVED AFTER THE RATIFICATION ENCODE WAS COMMITTED.** The encode
`705cecef` was written on a branch that already carried `main` @ `ea34f22a`
through two merges taken FIRST — `480fb996` (merging `bd1c54c6`) and `6aebb296`
(merging `ea34f22a`) — which is what the first capture recorded and why it was
right to call itself a post-merge run. `main` then advanced by three more
commits:

| commit | what it is |
| --- | --- |
| `9149301c` | `disposition-codexfactory-floor-relocation-retitle`: verify group-5 bookkeeping (PR #913) |
| `05c706d6` | files `admit-review-lane-repin-to-merge-approval-envelope` as a PROPOSAL, `Status: draft` (PR #910) |
| `52e42be9` | ticks boxes 1.3, 1.4 and 4.3 of `relocate-review-authority-floor-mirror`, bookkeeping only (PR #916) |

**THE MERGE WAS TAKEN AS ITS OWN COMMIT AT `ff44d3bc`** (parents `705cecef` —
the ratification encode — and `52e42be9`). It is a clean merge: nothing
conflicted, and the README `## OpenSpec Records` block took a pure ADDITION of
another lane's new row.

**THE MERGE MOVES NO BYTE OF THIS PACKET.**
`git diff --stat 705cecef ff44d3bc -- openspec/changes/amend-marker-declaring-nothing scripts/doc_health tests/doc-health`
is **EMPTY**, and this packet's own README `## OpenSpec Records` row is
byte-identical across the merge (the row extracted from both trees hashes to
`732d873c0ef2946fd303988d1bebd731`). The only README movement is the 42-line
row `05c706d6` added for a different change in a different lane.

**SO THE RE-MEASURE IS OWED FOR THE CORPUS, NOT FOR THE DELTA.** Every figure
below is taken again from zero on `ff44d3bc`; nothing is carried forward from
the first capture. Where a figure MOVED, § 9 names the commit on `main` that
moved it and shows the movement is main's own and not this packet's.

| item | value |
| --- | --- |
| clone | a fresh clone isolated from any shared checkout, `origin` pointed at `https://github.com/opensoft/openxFactory.git` |
| tree these figures were taken on | `ff44d3bc` — the merge commit, head of `change/amend-marker-declaring-nothing` |
| head the ratification was authorized on | `5dd724f5` — the frozen bench head, unchanged |
| the ratification encode | `705cecef` |
| merges from `main` | **THREE**: `480fb996` and `6aebb296` BEFORE the encode, `ff44d3bc` AFTER it |
| `origin/main` at this verification | `52e42be9` |
| `--all --strict` control | a separate worktree of `origin/main` `52e42be9` |
| `doc-health` controls | TWO, each in a worktree whose directory basename matches this clone's so the `Repo-Identity` label is identical and the diff is LITERAL: `origin/main` `52e42be9`, and the PRE-MERGE ratified tree `705cecef` |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `openspec` CLI on PATH **1.2.0**, pinned CLI **1.12.0**, Python **3.12.3** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-marker-declaring-nothing --strict`

```
Change 'amend-marker-declaring-nothing' is valid
```

**Exit code 0.** Unchanged from the first capture, and it is the same delta: the
merge edits no file of this packet, so the block the bench reviewed and the word
ratified is validated again, byte for byte.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 98 passed, 4 failed (102 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
four failures, on both sides:

| failing item | on `origin/main` `52e42be9` | on `ff44d3bc` |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `change/disposition-codexfactory-floor-relocation-retitle` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `52e42be9`, reports
`Totals: 97 passed, 4 failed (101 items)`, exit 1. **The branch differs by
exactly ONE item and that item PASSES** — this change itself, rendering
`✓ change/amend-marker-declaring-nothing`. `diff` over the two sorted `✗` lists
emits NOTHING.

**BOTH SIDES ROSE BY ONE ITEM SINCE THE FIRST CAPTURE** (branch 101 → 102,
control 100 → 101) and the added item is `admit-review-lane-repin-to-merge-approval-envelope`,
filed on `main` by `05c706d6`. It passes on both sides. The failure set did not
move: same four names, same count, as recorded at `ea34f22a`.

`spec/neutral-product-pin` remains the `requirements.16.text` *"Requirement must
contain SHALL or MUST keyword"* defect openxFactory
[#882](https://github.com/opensoft/openxFactory/issues/882) names. None of the
four is a `doc-health` item and this packet edits no file any of them reads.

## 3. The PINNED CLI, which is the one the gate runs

The `openspec` on PATH is **1.2.0** and the pin is **1.12.0**, so both arms were
run through the pinned artifact.

`python3 scripts/validate-openspec-cli-pin.py --change amend-marker-declaring-nothing --no-cache`
— **exit 0**:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact; integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

The gate's literal invocation `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`
— **exit 0**:

```
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The two accepted exceptions are the PRE-EXISTING pair — `add-chain-attestation`
and `add-composed-view-authoring`, both `Merged into` marker dispositions
accepted by Brett Heap on 2026-09-05, *"take exit 2"* — and **neither is this
change**. This block omits no scenario and retitles none, so it adds no 1.12
finding of its own.

## 4. `python3 scripts/proposal-support.py . verify amend-marker-declaring-nothing`

```
proposal support verification ok
```

**Exit code 0.** This is the gate that reads the `.openspec.yaml` origin
declaration, so it is the one most exposed to the approval pair the encode
added: it passes with the pair present and the drafting provenance unmoved.

## 5. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0**, both archive-date arms passing.

### `--ledger-diff`

**Exit code 0**:

```
change ids (40 active + 156 archived): 196
co-modified at requirement granularity (each would owe a declaration): 141
sole modifiers (each would declare `sequenced_after: []`): 55
ACTIVE changes: co-modified / sole: 25 / 15
declaring `sequenced_after:`: 21 (… amend-marker-declaring-nothing …)
declaring an explicit `[]` root claim: 4
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (196 rows).
```

**THE LEDGER IS CONSISTENT AT 196 ROWS AND THIS PACKET MOVED NONE OF THEM.**
The ledger grew 195 → 196 and **the diff against the first capture's tree is
exactly ONE line**, which is not this packet's:

```
admit-review-lane-repin-to-merge-approval-envelope: {state: active, class: sole, declares: [amend-mirror-floor-regeneration-merge-authority, extend-merge-master-envelope-to-floor-bot-lanes], depth: 4, prose: false, moved_by: "#910", moved_on: "2026-09-10"}
```

`moved_by: "#910"` names the pull request that seeded it. This packet's own row
is unchanged, still `moved_by: "#908"`, and this change remains one of the
corpus's four explicit `[]` root claims. The deepest declared chain moved from 3
hops to 4 for the same reason — the new change declares two partners at depth 4
— and no row of this packet's participates in it.

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 7. `python3 scripts/doc-health.py --single-repo .`

**Exit code 0.**

```
Findings: 32 critical, 5 error, 47 warning, 16 info. New regressions vs previous report: 0.
```

**NO FINDING NAMES THIS CHANGE.** `grep -c 'amend-marker-declaring-nothing'`
over the whole 350-line report reads **0**.

### The two controls, and both reports are BYTE-IDENTICAL to this one

Each control ran in a worktree whose directory basename is `encode-908d`, the
same as this clone's, so the report's `Repo-Identity:` header matches and the
comparison is a LITERAL byte diff with nothing normalized away:

| control | tree | `md5` of the report | result |
| --- | --- | --- | --- |
| this tree | `ff44d3bc` | `4e25037a656543b76727afc9a7c00e13` | — |
| `origin/main` | `52e42be9` | `4e25037a656543b76727afc9a7c00e13` | **IDENTICAL**, 350 lines both, `diff` emits nothing |
| the PRE-MERGE ratified tree | `705cecef` | `4e25037a656543b76727afc9a7c00e13` | **IDENTICAL**, 350 lines both, `diff` emits nothing |

All three carry `Repo-Identity: encode-908d` and all three exit **0**.

The first control says **this branch adds no doc-health finding to `main` and
removes none**. The second says **the merge changed no finding either** — which
is what isolates the merge from the encode, the encode having been measured
against its own controls in the first capture.

### THIS FILE IS INSIDE THE SCAN SET — probed, not assumed

The three reports above were taken on the tree BEFORE this record existed, so
the run was repeated once more with this file, the `tasks.md` § 5.11 tick and
the README records-list edit all present. **Exit 0, 350 lines, and the SAME
`md5` `4e25037a656543b76727afc9a7c00e13`.** A `record`-status report under
`review/` is read by the lifecycle families and scores nothing against them, so
**this capture adds no doc-health finding and removes none** — which is checked
here rather than assumed, the first capture having made the same probe for the
two records the encode added. `grep -c 'amend-marker-declaring-nothing'` over
the post-edit report still reads **0**.

### `ratified-provenance`, `record-immutability` and `proposal-origin`

| family | count | any of them this packet's? |
| --- | --- | --- |
| `ratified-provenance` | 28 critical | **NO** |
| `record-immutability` | 4 critical | **NO** |
| `proposal-origin` | 0 findings | — |

`ratified-provenance` is the family this encode is most exposed to, since
`804a9170` (#878) made it read a `review/ratification-*` record's SUBJECT
whatever status it carries. **This packet's ratification record enters that
population and CLEARS it**, carrying `Status: ratified` plus exactly one
`Ratified:` citation from the commit that created it. The 28 are other packets'
records — among them the predecessor's own
`openspec/changes/archive/2026-09-09-amend-marker-defect-reporting/review/ratification-2026-09-09.md`,
a standing population this ratification neither adds to nor relieves.

## 8. `modified-block-currency` — the family that reads this very block

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 11 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**MARKER DEFECTS: 0 OVER THE WHOLE CORPUS**, on this tree and on both controls —
so both grounds this packet ratifies still have a population of ZERO at landing,
which is D0's measurement holding on a corpus that has moved since D0 was taken.
**The gate-bearing arm reports 0**, and none of the eleven carriage-ledger rows
names this packet's block. `_ARM_TEMPLATES` stays at eight and the seventh class,
`unplaced-finding drift`, stays silent — the probe that would catch a finding
this packet's template failed to place.

## 9. The test suite

`python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs tests/proposal-support -q`
— the four-directory selection `tasks.md` § 5.8, § 5.9 and § 5.10 ran:

```
2178 passed, 7 warnings, 67 subtests passed
```

Per directory, collected on this tree: `tests/doc-health` **1689**,
`tests/sequenced_after` **273**, `tests/scope_globs` **88**,
`tests/proposal-support` **128** — and `tests/doc-health/test_modified_block_currency.py`
still carries the **144** this packet's realization brought it to (139 → 144).
The three fast directories were also run alone, each **exit 0**:
`tests/sequenced_after` 273 passed, `tests/scope_globs` 88 passed,
`tests/proposal-support` 128 passed with all 67 subtests.

**THE ONE FIGURE THAT MOVED IS THE SUBTEST COUNT, 66 → 67, AND IT IS MAIN'S.**
Every subtest in the selection comes from
`tests/proposal-support/test_proposal_support.py`, whose ratifying-commit sweep
runs *"one subtest per change"* over the directories of `openspec/changes/` —
`with self.subTest(change=directory.name)`. Active changes went 39 → 40 when
`05c706d6` filed a new proposal on `main`, so the sweep gained exactly one
subtest. **The passing-test total did not move at all** (2178 on both trees):
`05c706d6` added no test function.

## 10. What this merge does NOT move — verified by diff, not by assertion

| claim | how it is checked | result |
| --- | --- | --- |
| no packet file moves | `git diff --stat 705cecef ff44d3bc -- openspec/changes/amend-marker-declaring-nothing` | EMPTY |
| no realization code moves | `git diff --stat 705cecef ff44d3bc -- scripts/doc_health tests/doc-health` | EMPTY |
| no promoted canon moves | `git diff 5dd724f5 ff44d3bc -- openspec/specs/` | EMPTY |
| this packet's README row unmoved | row extracted from both trees, hashed | identical, `732d873c…` |
| no committed record edited | `git diff 705cecef ff44d3bc -- openspec/changes/amend-marker-declaring-nothing/review/` | EMPTY |

**PROMOTED CANON STILL STATES THREE GROUNDS.** Nothing under
`openspec/specs/` is edited by the ratification or by the merge; the
`## MODIFIED` block writes over canon AT THE ARCHIVE, which is a separate act on
merged-plus-green realization evidence and a separate word. `tasks.md` § 6
(archive) and § 7 (residue) stay ENTIRELY OPEN, and openxFactory #856 and #860
close at that archive rather than at this landing — which is why this pull
request carries `refs #856, refs #860` and no closing keyword.

## 11. What this record does not claim

It does not claim the landing is done, and it is not a landing record. It does
not archive the packet and ticks no box of `tasks.md` § 6 or § 7. It does not
supersede `review/verification-2026-09-10.md`, which stands as the measurement
of the tree it was taken on. And it records no bot round of its own: the bench
disposition for the frozen head `5dd724f5` is written in
`review/ratification-2026-09-10.md`, and whatever a reviewer says about the
ratified head is recorded on the pull request rather than rewritten into a
committed capture.
