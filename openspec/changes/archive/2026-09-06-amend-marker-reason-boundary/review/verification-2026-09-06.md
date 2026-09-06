# Verification record: amend-marker-reason-boundary, 2026-09-06

Status: record
Kind: report
Captured: 2026-09-06, in lane `openxfactory-1`, on branch
`change/amend-marker-reason-boundary` (openxFactory PR #719).

**This record is CAPTURED AT MERGE, not at first push, and EVERY NUMBER BELOW WAS
RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, after this branch's
**SECOND** merge from `main` (taking `origin/main` **`d179cc0d`**: #717
`register-gate-rules-council-seats` and #718 intent-plane 4.4 PR-1, on top of
`6295e387`, which the first merge took) and after the ratification was encoded.
`record-immutability` forbids editing a `Status: record` document AFTER capture;
capture is the merge of the pull request that establishes it, and nothing is
merged yet. A commit cannot write its own hash into its own tree, so the
ratification commit is named by its subject and its position on the branch rather
than by a hash.

**None of the numbers the pull request body carried at head `c5d33422` is taken
on trust.** They were measured before either merge from `main`; every one is
re-derived here, and the item counts moved because `main` brought its own change
directories — not because anything in this packet did.

**If `main` moves again before this pull request lands**, the branch takes another
merge and every number here is re-derived a second time, with § 9 extended to say
so, before capture.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-marker-reason-boundary --strict`

```
Change 'amend-marker-reason-boundary' is valid
```

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 97 passed, 1 failed (98 items)
```

**THE ONE FAILURE IS NOT THIS PACKET'S, AND IT IS NOT A FAILURE UNDER THE CLI CI
ACTUALLY RUNS.** This invocation is the `PATH` CLI, which in this session is
`@fission-ai/openspec` **1.2.0**; the refusal is

```
✗ change/disposition-codexfactory-declared-renames
  [ERROR] file: Change must have at least one delta. No deltas found.
```

— a change that deliberately declares no spec-level behaviour and sets
`skip_specs` in its `.openspec.yaml`. The PINNED 1.12 entrypoint, which is what
`openspec-cli-pin-gate.yml` runs, honours `skip_specs` and reports it as an INFO
instead (§ 3). Both readings are recorded rather than the flattering one alone.
The item count is **98** rather than the 97 measured after the first merge
because #717 added a change directory; the failure count did not move.

## 3. THE PINNED 1.12 ENTRYPOINT, EXACTLY AS `openspec-cli-pin-gate.yml` RUNS IT

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`:

```
Totals: 96 passed, 2 failed (98 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied)
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures.
THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.

change/disposition-codexfactory-declared-renames
  ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no
           spec-level behavior changes, zero deltas accepted
```

**NEITHER DISPOSITIONED FINDING IS THIS CHANGE'S**, and no third appears. Both
are `#677`'s standing dispositions — 1.12's scenario-currency check is
MARKER-BLIND, so it refuses two landed `Merged into` renames that canon's own
worked example defines, and Brett Heap accepted them on *"take exit 2"*.

**AND THAT IS THE PREDICTION THIS RUN CONFIRMS.** 1.12 refuses a `## MODIFIED`
block that OMITS a SCENARIO the current spec still has. This block **omits none
and retitles none** — it carries all 14 promoted titles, replaces one BODY
sentence, and ADDS two scenarios at the end, none of which that check can see.
The **two added scenarios add no undispositioned failure**, which is the reading
the review round owed and this run settles.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (38 active changes, 3 declaring the field).
```

`python3 scripts/validate-sequenced-after.py . --ledger-diff`:

```
per-change sweep ledger consistent with the corpus (178 rows).
```

**RATIFICATION MOVES NO ROW.** A row's derived keys are `state`, `class`,
`declares`, `depth` and `prose`; none of them reads a lifecycle status, so a
`draft` → `ratified` transition is invisible to the ledger by construction. This
change's row stands exactly as `7e156829` seeded it —

```
amend-marker-reason-boundary: {state: active, class: co-modifier,
                               declares: absent, prose: false,
                               moved_by: "#719", moved_on: "2026-09-06"}
```

`class: co-modifier` because the `## MODIFIED` block writes `doc-health`
§ *Currency of an active change's MODIFIED requirement blocks*, a key
`add-modified-block-currency-check`, `add-unclassified-finding-class` and
`govern-sibling-added-modified-deltas` already write; **all three are ARCHIVED**,
so no partner flips and no MOVEMENT LOG entry is owed. **ROWS MOVED BY THE
RATIFICATION COMMIT: ZERO.** 177 → 178 rows is #717's row, arriving with the
second merge.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

## 6. `python3 scripts/doc-health.py --single-repo .` — TWO CONTROLS, NOT ONE

Measured against controls minutes apart on the same clock, not against a stale
baseline. The control is a worktree at `origin/main` **`d179cc0d`** — the `main`
this branch has merged.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `origin/main` `d179cc0d` (worktree control) | 9 | 8 | 44 | 13 |
| this branch, BEFORE the ratification was encoded | 9 | 8 | 44 | 13 |
| this branch, AFTER it was encoded, at the merged head | 9 | 8 | 44 | 13 |

All three read `9 critical, 8 error, 44 warning, 13 info`, with `New regressions
vs previous report: 0`.

- **Against `origin/main` `d179cc0d`:** a line-by-line diff of the two whole
  reports is **EMPTY** once the checkout's own directory-name token is
  normalized — not merely the finding lines, but the headline, the canon-share
  figure and the Per-Stage Counts table as well.
- **AND THE REASON IS STRUCTURAL RATHER THAN LUCKY, which is why it is stated
  rather than left to look like an error.** `corpus.GOVERNED_ROOTS` is
  `contracts`, `docs`, `examples`, `ideation`, `templates` — **`openspec/` is not
  in it.** An OpenSpec change packet is read by the separately declared
  LIFECYCLE SCAN SET (`openspec/changes/**/proposal.md` and
  `openspec/changes/**/review/*.md`, minus byte-exact-evidence segments), which
  `corpus.py` documents as never entering `load_docs`, "so no census, word total,
  canon-share figure, inventory entry, or catalog record moves because it
  exists". So this packet — its delta, its four packet files and both records —
  **cannot** move a word total, and the word totals are not offered here as
  evidence of anything. What the lifecycle scan set DOES reach is
  `proposal.md` and both `review/` records, read by exactly four families:
  status validity, standard backing, **ratified provenance**, succession
  integrity. Those are the families this ratification could have broken, and § 6
  probes two of them by making them fire.
- **Against the pre-ratification branch:** the diff of the FINDING lines is
  **EMPTY** — the status flip, the citation lines, the approval pair, the README
  row and both new record files together add **not one finding**.
- **The families that could have spoken about this transition say nothing:**
  `doc-health` names `amend-marker-reason-boundary` **zero** times in the whole
  report.

### PROBE 1 — `proposal-origin` class 7, made to fire and then cleared

`proposal-origin`'s class 7 reports an ERROR for *"a proposal declaring
`Status: ratified` while its origin still carries drafting provenance and asserts
no approval"*. With `Status: ratified` set and the approval pair REMOVED from
`.openspec.yaml`, `--family proposal-origin` reported exactly that and nothing
else:

```
Findings: 0 critical, 1 error, 0 warning, 0 info.
- [error] openspec/changes/amend-marker-reason-boundary — proposal declares
  `Status: ratified` while its origin asserts no approval — approval MUST
  appear when the status claims it
```

Restoring `approved_by` + `approved_on` BESIDE the retained
`proposed_by`/`proposed_on` — `kind` and `id` unmoved, the addition-not-rewrite
shape `add-drafted-proposal-origin` defined — clears it:

```
Findings: 0 critical, 0 error, 0 warning, 0 info.
```

and the restored file is byte-identical to the one this branch carries.

### PROBE 2 — `ratified-provenance`, made to fire and then cleared

The rule is EXACTLY ONE citation line per document, counted across both sanctioned
spellings. A second line added to `proposal.md`'s front matter fires it, and the
finding names this proposal:

```
Findings: 6 critical, 0 error, 0 warning, 0 info.
- [critical] openspec/changes/amend-marker-reason-boundary/proposal.md —
  carries 2 ratification citation lines, not one
```

Removed again:

```
Findings: 5 critical, 0 error, 0 warning, 0 info.
```

— the five that remain are the corpus's pre-existing ones, identical on
`origin/main`. So the ONE `Ratified:` line this proposal carries is checked by a
family that is demonstrably live on it, and it passes.

**THAT IS ALSO WHY THE STATUS FLIP AND THE APPROVAL PAIR MOVE IN ONE COMMIT.**
The archive gate's origin-retention arm resolves the RATIFYING COMMIT — the first
commit whose `proposal.md` declares `Status: ratified` — and compares the origin
declaration there against the one being archived. Run on this branch it answers:

```
ORIGIN RETAINED amend-marker-reason-boundary
(declaration unchanged since the ratifying commit 805d2c0e8079)
```

### PROBE 3 — `--family modified-block-currency`, the marker both ways

```
Findings: 0 critical, 0 error, 0 warning, 8 info.
```

Identical to the `origin/main` control line for line, and the family names this
change **zero** times. Zero alone cannot be distinguished from a block the family
never read, so it was probed:

- **the block's `Removed from canon` marker deleted** → *"active MODIFIED block
  for 'Currency of an active change's MODIFIED requirement blocks' does not carry
  **1** of the 90 body units and scenario bullets `openspec/specs/doc-health/spec.md`
  currently states for it"* — one unit dropped, and the marker is what declares
  it;
- **restored** → silent again, and the delta byte-identical to the one committed.

**So the block raises ZERO carriage findings from its own family while genuinely
being read by it.**

## 7. The self-reference discharge, re-run on the merged tree

The packet's own marker parsed by BOTH modules — this branch's amended
`parse_marker` and `origin/main` `d179cc0d`'s retired one — over the delta as
committed:

```
AMENDED (branch):                names=1, reason 550 chars
   NAME  : The parser SHALL extract the code spans following the colon, in
           order, per CommonMark; the reason is everything after the last code
           span's following ` — `.
   REASON: 'the sentence measures the reason from the LAST code span, …'
RETIRED (origin/main d179cc0d):  names=1, reason 550 chars
   NAME  : (identical)
   REASON: (identical)
IDENTICAL: True
```

The named unit's own ` — ` lies INSIDE its doubled-backtick fence, and the reason
carries no code span at all, so both grammars cut at the same separator. **This is
a constraint on amendment markers generally while both grammars are in the
estate** (`design.md` D4).

## 8. `python3 -m pytest tests/doc-health -q`

```
1587 passed, 7 warnings in 280.13s (0:04:40)
```

`tests/doc-health/test_modified_block_currency.py` alone: **128 passed** (121 →
128, seven ADDED and none edited).

**1584 → 1587 IS `main`, NOT THIS PACKET.** The pull request body reported 1584
at head `c5d33422`; the first merge from `main` brought #724's
`tests/doc-health/test_import_direction.py` with it, and the second merge added
no test under this directory. The count is identical before and after the
ratification was encoded — a status flip adds no test.

## 9. The branch's merge history

**TWO merges from `main`.**

1. The first took `origin/main` **`6295e387`** — #723 (the scope-globs
   archive-gate repair), #721, #724, #720 and #716. **Every hunk auto-merged**:
   `README.md` kept both sides and `tests/sequenced_after/corpus-ledger.yaml`
   took no conflict.
2. The second, carried in this pull request after the ratification commit, took
   `origin/main` **`d179cc0d`** — #717 `register-gate-rules-council-seats` and
   #718 intent-plane 4.4 PR-1. **ONE conflict, in `README.md`'s OpenSpec Records
   block**: #717 inserted its own Active row at the same insertion point as this
   packet's. **Resolved by keeping BOTH, this branch's row first**, in the
   established ordering. The corpus ledger auto-merged and kept both rows — this
   change's at `"#719"` and #717's at `"#717"`. **No row moved and no partner
   flipped.**

## 10. Independent review

**Codex ABSENT, twice, recorded as absence and not as clearance** — `@codex
review` requested at 10:52:12Z and at 12:09:00Z, refused both times on usage
limits (10:52:20Z, 12:09:08Z). **No Codex round ran on this packet.**
**Sourcery** is the private-repo upsell stub (10:16:22Z). **Copilot ran twice**
(10:19:12Z, 11:30:49Z) and opened ONE inline thread — a precedence pitfall in the
pairing branch's conditional, `normalize(tail[3:])` evaluated even when the tail
carries no separator — which was **taken and the thread RESOLVED**. Three
adversarial review lenses returned **MERGEABLE_AFTER_FIXES** with four MINOR and
five NOTE-level findings; six were folded in `c5d33422`, three were refused with
their reasons, and the re-verification returned **MERGEABLE**. The full
disposition is `ratification-2026-09-06.md` § 5.
