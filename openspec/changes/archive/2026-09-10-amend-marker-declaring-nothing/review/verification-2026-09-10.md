# Verification record: amend-marker-declaring-nothing, ratified tree 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Ratified by: amend-marker-declaring-nothing — 2026-09-10, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-10.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-10.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one. The distinction is MECHANICAL as well as
contractual: since `804a9170` (#878) `ratified-provenance` reads a
`review/ratification-*` record's SUBJECT whatever status it carries, and it
leaves a `verification-*` capture alone.

**IT IS ALSO A ONE-SHOT CAPTURE.** `document-lifecycle` holds that a dated run
report keeps `record` and that *"a second run of such a generator writes a
different path rather than rewriting the same one"*. This is the packet's FIRST
and only gate capture; a later re-run writes `verification-<later date>.md`
beside it rather than editing this file.

**AND IT IS ALREADY A POST-MERGE RUN, SO NO SECOND CAPTURE IS OWED AT LANDING.**
`origin/main` advanced from `e0638f11` — the tree every figure in the pull
request body and in `tasks.md` § 2 and § 5 was measured on — by THREE commits
while the branch sat frozen at `5dd724f5`: `40d2f821` and `bd1c54c6`, merged into
the branch as `480fb996`, and then `ea34f22a` (three merge-master scripts
hardened, PR #911), merged as `6aebb296`. **BOTH MERGES WERE TAKEN FIRST, EACH AS
ITS OWN COMMIT**, and the ratification encode landed on top of them, so every
figure below is derived on a tree that already carries `main` @ `ea34f22a`. That
is the opposite order from this packet's predecessor, where the encode preceded
the merge and a second capture was owed at its own path.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE, AFTER THE ENCODE, IN AN
ISOLATED CLONE, WITH BOTH RECORDS INSIDE THE LIFECYCLE SCAN SET.** Nothing is
carried forward from the pull request body's earlier gate tables; where a figure
matches one of those, it matches because it was measured again and came out the
same.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | a fresh clone isolated from any shared checkout, `origin` pointed at `https://github.com/opensoft/openxFactory.git`, with `main` and the change branch fetched from there |
| head the ratification was authorized on | `5dd724f5` — the frozen bench head, unchanged from the tree Brett Heap ruled on |
| merges from `main` | **TWO, AND BOTH TAKEN FIRST**: `480fb996` (merging `bd1c54c6`) and `6aebb296` (merging `ea34f22a`), each its own commit BEFORE the ratification encode |
| tree these figures were taken on | the ratification encode, committed on `change/amend-marker-declaring-nothing` on top of `6aebb296` and carrying this file |
| `origin/main` at this verification | `ea34f22a` |
| `--all --strict` control | a separate worktree of `origin/main` `ea34f22a` |
| `doc-health` controls | TWO: the PRE-RATIFICATION tree `6aebb296` (the same tree minus this encode) and `origin/main` `ea34f22a`, each in a worktree whose directory name matches this clone's so the `Repo-Identity` label is identical and the diff is literal |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `TZ=UTC`, `openspec` CLI on PATH **1.2.0**, pinned CLI **1.12.0**, Python **3.12.3**, npm **11.19.0** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-marker-declaring-nothing --strict`

```
Change 'amend-marker-declaring-nothing' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the ratified tree.
The encode touched no file under the packet's `specs/` directory — § 9 measures
that as an EMPTY diff — so this is the same delta the bench reviewed, validated
again.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 97 passed, 4 failed (101 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
four failures, on both sides:

| failing item | on `origin/main` `ea34f22a` | on the ratified tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `change/disposition-codexfactory-floor-relocation-retitle` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `ea34f22a`, reports
`Totals: 96 passed, 4 failed (100 items)`. **The ratified tree differs by
exactly ONE item and that item PASSES** — this change itself, which is the 101st
item and renders `✓ change/amend-marker-declaring-nothing`. **This packet adds
nothing to the failure set and removes nothing from it**: `diff` over the two
sorted `✗` lists emits NOTHING, and `diff` over the two full item lists emits
exactly one line, `> ✓ change/amend-marker-declaring-nothing`.

### The four failures are pre-existing and none of them is this packet's

None of the four is a `doc-health` item, and this packet edits no file any of
them reads. The `spec/neutral-product-pin` failure is the `requirements.16.text`
*"Requirement must contain SHALL or MUST keyword"* defect openxFactory
[#882](https://github.com/opensoft/openxFactory/issues/882) names — the parser
reads only the FIRST LINE of a requirement's body — and the other three are
likewise items this packet does not touch. They fail identically with and
without this change on the tree.

## 3. The PINNED CLI, which is the one the gate runs

The `openspec` on PATH is **1.2.0** and the contract pin is **1.12.0**, so both
were run and this is the pinned one.

`python3 scripts/validate-openspec-cli-pin.py --change amend-marker-declaring-nothing --no-cache`
— **exit 0**:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/prefix/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` — the gate's
literal invocation — **exit 0**, `Totals: 99 passed, 2 failed (101 items)` with
**both failures DISPOSITIONED**:

```
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The two accepted exceptions are `add-chain-attestation` and
`add-composed-view-authoring`, both dispositioned *accepted by: Brett Heap,
2026-09-05, "take exit 2"*, and **NEITHER IS THIS CHANGE. THIS BLOCK OMITS NO
SCENARIO AND RETITLES NONE**, so it adds no 1.12 finding of its own — measured
here, not assumed. The two counts differ from § 2's by construction and both are
stated rather than reconciled away: 1.12 reads the corpus with an extra arm, so
the same 101 items give `97 / 4` on the CLI on PATH and `99 / 2` through the pin.

## 4. `python3 scripts/proposal-support.py . verify amend-marker-declaring-nothing`

```
proposal support verification ok
```

**Exit code 0.** This is the gate that reads the support manifest against the
packet, and it is the one most exposed to the `.openspec.yaml` edit: the approval
pair was ADDED beside a fixed `kind` and `id`, so the manifest that repeats them
does not come to disagree with the packet. § 9 measures the addition-only shape
by `--numstat`.

## 5. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0**, both archive-date arms passing.

### `--ledger-diff`

**Exit code 0**:

```
change ids (39 active + 156 archived): 195
co-modified at requirement granularity (each would owe a declaration): 141
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 25 / 14
declaring `sequenced_after:`: 20 (… amend-marker-declaring-nothing …)
declaring an explicit `[]` root claim: 4
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 3 hop(s), from amend-mirror-floor-regeneration-merge-authority

per-change sweep ledger consistent with the corpus (195 rows).
```

**The ledger is consistent at 195 rows and ZERO rows moved by this encode**:
the row this packet seeded at § 4.8 is unchanged, and the ratification edits no
`sequenced_after:` value anywhere. This change is one of the corpus's four
explicit `[]` root claims and is listed among the twenty declaring the field.
Both of this gate's scripts — `scripts/sequenced_after.py` and, in § 6,
`scripts/scope_globs.py` — are the ones `ea34f22a` hardened, so these two runs
exercise the current `main` implementation rather than the pre-#911 one.

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 7. `python3 scripts/doc-health.py --single-repo .`

**Exit code 0.** Report headline, verbatim:

```
Canon share by words: 39.7% (367584 canon words / 924910 governance words, promoted specs included).
Findings: 32 critical, 5 error, 47 warning, 16 info. New regressions vs previous report: 0.
```

350 report lines, 100 finding lines.

### The two controls, and both reports are BYTE-IDENTICAL to this one

The same command was run on the PRE-RATIFICATION tree `6aebb296` — the same tree
minus this encode — and on `origin/main` `ea34f22a`, each in a worktree whose
directory name matches this clone's so the `Repo-Identity:` label reads
identically. **ALL THREE REPORTS ARE THE SAME BYTES**: `diff` over the two
350-line report bodies emits NOTHING in both directions, and the three bodies
share one `md5sum` (`2c82072428b11461be5f83f3b7527622`) — same headline, same
canon share, same per-stage census, same 100 finding lines. **THIS RATIFICATION
ADDS NO DOC-HEALTH FINDING AND REMOVES NONE**, and neither does either merge from
`main`.

### Why the two new records move no census figure, and it is a mechanism rather than a coincidence

`scripts/doc_health/corpus.py` declares two disjoint reads. `GOVERNED_ROOTS` is
`("contracts", "docs", "examples", "ideation", "templates")` plus promoted
specs, and it is *"the SOLE input to the per-stage census, the governance and
canon word totals, the canon-share headline, the shared inventory, and the
document catalog"*. The **lifecycle scan set** is separate: *"each OpenSpec
change packet's `proposal.md` and EVERY `review/` record under it — whatever
that record's subject"*, read by exactly four families — status validity,
standard backing, ratified provenance, succession integrity — and *"it never
enters `load_docs`, so no census, word total, canon-share figure, inventory
entry, or catalog record moves because it exists."* The byte-identical report
above is that invariance measured on this packet.

### The records ARE inside the scan set — probed, not assumed

`corpus.load_lifecycle_docs("openxFactory", root)` over the ratified tree returns
**307** documents, **THREE** of them this packet's, so neither record is silently
skipped:

| path | status | kind |
| --- | --- | --- |
| `openspec/changes/amend-marker-declaring-nothing/proposal.md` | `ratified` | — |
| `openspec/changes/amend-marker-declaring-nothing/review/ratification-2026-09-10.md` | `ratified` | `report` |
| `openspec/changes/amend-marker-declaring-nothing/review/verification-2026-09-10.md` | `record` | `report` |

### The `ratified-provenance` family — the family this encode is most exposed to

**28 critical findings on this tree, and NOT ONE OF THEM NAMES THIS CHANGE.**
`grep` for `amend-marker-declaring-nothing` over the whole 350-line report
returns **ZERO** lines. The 28 are 21 *"a review record that records a
ratification must carry Status: ratified and one citation"*, 5 *"ratified header
carries no citation in either sanctioned spelling"*, 1 *"Ratified: names none of
an approver, a date, or a resolvable record path"* and 1 *"Ratified by: missing
or does not resolve to an OpenSpec change"* — every one of them on another
packet. That is the family that would fire on a missing or doubled citation
line, and it reads all three scan-set entries above: the three `Status: ratified`
documents each carry **EXACTLY ONE** citation line (`Ratified:` in
`proposal.md`, `Ratified by:` in `design.md` and `tasks.md`), the ratification
record carries exactly one `Ratified:` line, and the verification capture keeps
`Status: record` so the *not about a ratification* scenario governs it. Had any
of those been wrong the count would have moved; it did not, and the report is
byte-identical to the pre-ratification control.

### `record-immutability` and `proposal-origin` — measured, and neither reaches this packet

**`record-immutability`: 4 critical findings on this tree, none of them this
packet's** (all four are `docs/` captures). Both records are NEW files, created
by the ratification commit, so there is no prior committed version for the
family to compare against; and no committed record anywhere is edited by this
encode (§ 9). **`proposal-origin`: *No findings*** — the family that reads
`.openspec.yaml` origin declarations is silent on the approval pair this commit
adds.

## 8. `modified-block-currency` — the family that reads this very block

**ZERO marker-defect findings on the whole corpus**, before and after. The
family's own class census, verbatim from the report:

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 11 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

So both grounds this packet RATIFIES have a population of zero at landing,
re-measured on the ratified tree rather than carried forward from the design.

**AND THE BLOCK'S OWN STANDING FLIPPED, WHICH IS THE LOAD-BEARING MEASUREMENT
HERE.** The family reads a block's `standing` from the packet's documents, so
before this encode this block was `standing: draft` and after it the probe reads
`standing: ratified` — and **the arms stay silent either way**, which is what the
byte-identical report proves. This is not incidental: the delta's own retired
lifecycle-standing clause is about exactly that (*"A `draft` packet's block is as
capable of restating stale canon as a `ratified` one"*), so an encode that
flipped the standing and moved a finding would have contradicted the text it
ratifies.

The family's own derivation, re-run over the ratified tree through
`active_blocks` / `sibling_titles` / `promoted` / `resolve` / `suppression` —
the shipping functions, called as the runner calls them:

| measure | value |
| --- | --- |
| active `## MODIFIED` blocks the family reads | **31** (30 before this packet, plus this block) |
| of those, blocks resolving to a promoted basis | **25** (the other 6 are pending or unresolved, which the comparison arms skip on `main` too) |
| of those, blocks carrying a unit-naming marker | **3** — `add-chain-attestation` (`merged`, 1 name), `add-composed-view-authoring` (`merged`, 1 name) and this block (`removed`, 2 names) |
| marker defects over the whole corpus, from `suppression`'s own output | **0** |
| this block: resolution state | `canon` |
| this block: `standing` | **`ratified`** (was `draft` before the encode) |
| canon units in the resolved basis | **154** |
| block units | **165** |
| canon units the block does not carry | **2** |
| of those, suppressed by the marker | **2** |
| uncarried AND unsuppressed (each would be a finding) | **0** |
| markers on this block | **1** — `form=removed`, `names=2`, `quoted=0`, reason **826** characters carrying **NO** code span |
| **marker defects on this block** | **0** |
| canon scenario titles | **19** |
| of those, carried by the block | **19 of 19** |
| `_ARM_TEMPLATES` | **8** |
| `_LEDGER_SEVERITY` | `info` |

Those figures reproduce `tasks.md` § 4.1 and § 4.3 exactly, re-derived after both
merges and after the encode. The marker's reason carrying no code span is why
ground TWO has nothing to resolve over it, and its two names each matching a
canon unit the block does not carry is why grounds ONE, THREE, FOUR and FIVE
cannot fire on it — the block survives its own new rules, measured rather than
asserted.

## 9. The test suite

`python3 -m pytest tests/doc-health -q` — **exit 0**:

```
1689 passed, 7 warnings in 444.33s (0:07:24)
```

`python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs tests/proposal-support -q`
— the four-directory selection `tasks.md` § 5.8 and § 5.9 ran — **exit 0**:

```
2178 passed, 7 warnings, 66 subtests passed in 505.92s (0:08:25)
```

**THE COUNT MOVED FROM 2173 TO 2178 AND THE FIVE ARE MAIN'S, NOT THIS
PACKET'S.** `ea34f22a` (PR #911) added exactly five test functions —
`git diff bd1c54c6..ea34f22a -- tests/ | grep -cE '^\+def test_'` reads **5**,
three in `tests/scope_globs/test_integrity.py` and two in
`tests/sequenced_after/test_integrity.py`, all of them about OS-level failures in
the merge-master scripts — so 2173 + 5 = 2178 with nothing of this packet's
moving. `tests/doc-health` alone is unchanged from the frozen tree's run at
**1689 passed**, which is the directory this packet's realization lives in, and
`test_modified_block_currency.py` inside it still carries the **144** tests
§ 3.6 records.

## 10. What the encode does NOT move — verified by diff, not by assertion

| measured | command | result |
| --- | --- | --- |
| the ratified delta | `git diff 5dd724f5 -- openspec/changes/amend-marker-declaring-nothing/specs/` | **EMPTY** — byte-identical to the tree Brett Heap ruled on |
| the realization | `git diff 5dd724f5 -- scripts/doc_health/ tests/doc-health/` | **EMPTY** — no code and no test moved |
| promoted canon | `git diff 5dd724f5 -- openspec/specs/` | **EMPTY** — nothing is promoted |
| the drafting provenance | `git diff --numstat 5dd724f5 -- …/.openspec.yaml` | **`46 0`** — 46 insertions, **ZERO deletions**: the approval pair is a pure ADDITION and `kind`, `id`, `reason`, `proposed_by` and `proposed_on` are byte-unmoved |
| the merges' reach into this packet | `git diff --stat 5dd724f5 6aebb296 -- README.md openspec/ scripts/doc_health/ tests/doc-health/` | **EMPTY** — main's three commits touch none of it |

**AND NOTHING ELSE MOVES.** No contract, no schema, no workflow, no ledger row,
no archived change and no other active change's files are touched; no committed
record is edited; `tasks.md` § 6 (archive) and § 7 (residue) stay UNTICKED. The
files the ratification commit changes are exactly seven: `README.md`, the
packet's `proposal.md`, `design.md`, `tasks.md` and `.openspec.yaml`, and the two
new files under `review/`.

## 11. Independent review

The bench is recorded in `review/ratification-2026-09-10.md` § 5: six Copilot
rounds and one Codex request, **THREE inline threads and all three TAKEN** —
two before the word and resolved at the freeze of 18:11:11Z, the third (a README
tense finding on the merge head) taken by the ratification commit itself and
resolved with a reply. Codex's usage-limit refusal is recorded there as an
ABSENCE rather than as assent, and Copilot's 🔵 *"Needs a closer look"* on the
frozen head as the standing of a packet awaiting a ratification word. A further
bench round on the ratified head is recorded on the pull request rather than
here — this capture's subject is the gate run.
