# Verification record: amend-marker-defect-reporting, 2026-09-09

Status: record
Kind: report
Captured: 2026-09-09, in lane `openxfactory-1`, on branch
`change/amend-marker-defect-reporting` (openxFactory PR #850).

**This record is CAPTURED AT MERGE, not at first push, and EVERY NUMBER BELOW WAS
RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, after the
fix-before-encode commit and after the ratification was encoded.
`record-immutability` forbids editing a `Status: record` document AFTER capture;
capture is the merge of the pull request that establishes it, and nothing is
merged yet. A commit cannot write its own hash into its own tree, so the
ratification commit is named by its subject and its position on the branch rather
than by a hash.

**NONE OF THE NUMBERS THE ADVERSARIAL PASS REPORTED AT THE FROZEN HEAD
`9d4cf85b` IS TAKEN ON TRUST.** Every command below was re-run on the ratifying
tree. Where a figure differs from the pass's, the reason is named.

**THE CONTROL IS `origin/main` `183d1b43`, AND THE BRANCH IS BEHIND IT.** The
branch's last merge from `main` took `e86eca35` (#801) at 15:44Z; the two pull
requests the ratification word's first two clauses name landed after that —
**#842** `4cdadd56` at 16:11:57Z and **#846** `183d1b43` at 16:12:40Z, with #847
between them — so this branch does not yet carry them. **A merge from `main` and
a re-measure are owed AT LANDING**, and § 9 states exactly which figures move
when it is taken. Every difference between this tree and the control below is
attributed to that gap rather than left to look like this packet's.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-marker-defect-reporting --strict`

```
Change 'amend-marker-defect-reporting' is valid
```

Exit 0.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 100 passed, 3 failed (103 items)
```

Exit 1, and **THE THREE FAILURES ARE BYTE-IDENTICAL TO `origin/main`'s AND NONE
IS THIS PACKET'S:**

```
✗ change/disposition-codexfactory-declared-renames
✗ change/pin-openspec-cli-dependency-closure
✗ spec/repo-boundary-governance
```

The same three, spelled the same way, are what `origin/main` `183d1b43` reports
under the same command:

```
Totals: 98 passed, 3 failed (101 items)
✗ change/disposition-codexfactory-declared-renames
✗ change/pin-openspec-cli-dependency-closure
✗ spec/repo-boundary-governance
```

**The FAILURE SET is identical; only the ITEM COUNT moves, and it moves for
`main`'s reason rather than this packet's.** 103 against 101 is the arithmetic of
the gap named above: this branch still carries active change directories that
#847 archived on `main`, and it adds exactly ONE item of its own — this packet,
which PASSES (§ 1). `amend-marker-defect-reporting` appears in neither failure
list.

This invocation is the `PATH` CLI. The PINNED entrypoint, which is what
`openspec-cli-pin-gate.yml` runs, is § 3, and both readings are recorded rather
than the flattering one alone.

## 3. `python3 scripts/validate-openspec-cli-pin.py --change amend-marker-defect-reporting --strict`

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

Exit 0. **AND THAT IS THE PREDICTION THIS RUN CONFIRMS.** 1.12's
scenario-currency check refuses a `## MODIFIED` block that OMITS a scenario the
current spec still has. This block **omits none and retitles none** — it carries
every promoted title, replaces one BODY sentence, and ADDS two scenarios at the
end, none of which that check can see. The two added scenarios add **no
undispositioned failure**.

## 4. `python3 scripts/proposal-support.py . verify amend-marker-defect-reporting`

```
proposal support verification ok
```

Exit 0 — on the ratified tree, with `Status: ratified` on all three documents and
the approval pair present. This is the gate that reads the packet's support
manifest against its origin declaration, and it is the reason the status flip and
the approval pair move in ONE commit: the archive gate's origin-retention arm
resolves the RATIFYING COMMIT — the first commit whose `proposal.md` declares
`Status: ratified` — and compares the origin declaration there against the one
being archived. A tree carrying `Status: ratified` over drafting-only provenance
is exactly the shape `proposal-origin`'s class 7 reports.

## 5. `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`

```
sequenced_after validation passed (42 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

```
per-change sweep ledger consistent with the corpus (190 rows).
```

Both exit 0. **RATIFICATION MOVES NO ROW.** A row's derived keys are `state`,
`class`, `declares`, `depth` and `prose`; none of them reads a lifecycle status,
so a `draft` → `ratified` transition is invisible to the ledger by construction.
This change's row stands exactly as `766d5c44` seeded it —

```
amend-marker-defect-reporting: {state: active, class: co-modifier,
                                declares: absent, prose: false,
                                moved_by: "#850", moved_on: "2026-09-09"}
```

`class: co-modifier` because the `## MODIFIED` block writes `doc-health`
§ *Currency of an active change's MODIFIED requirement blocks*, a key
`add-modified-block-currency-check`, `add-unclassified-finding-class`,
`govern-sibling-added-modified-deltas` and `amend-marker-reason-boundary` already
write; **all four are ARCHIVED**, so no partner flips and no MOVEMENT LOG entry
is owed. **ROWS MOVED BY THE RATIFICATION COMMIT: ZERO.**

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

Exit 0.

## 7. `python3 scripts/doc-health.py --single-repo . --family modified-block-currency`

```
Findings: 0 critical, 0 error, 0 warning, 9 info. New regressions vs previous report: 0.
```

Exit 0, and **the control reads the same line**:

```
origin/main 183d1b43 (worktree control):
Findings: 0 critical, 0 error, 0 warning, 9 info. New regressions vs previous report: 0.
```

**A LINE-BY-LINE DIFF OF THE TWO WHOLE FAMILY REPORTS IS EMPTY across every
finding line**, once the checkout's own directory-name token is normalized. The
only lines that differ at all are the corpus HEADLINE figures — canon share
39.6% against 39.7%, the `standard` stage's word total 16,904 against 17,057, the
promoted-spec total 257,096 against 258,167 — and those move for `main`'s
content, not for this packet's. `corpus.GOVERNED_ROOTS` is `contracts`, `docs`,
`examples`, `ideation`, `templates`: **`openspec/` is not in it**, and neither is
a root-level `README.md`, so an OpenSpec change packet — its delta, its four
packet files and both of these records — **cannot** move a census figure, a word
total or the canon-share headline. The word totals are therefore not offered here
as evidence of anything. What the separately declared LIFECYCLE SCAN SET does
reach is `proposal.md` and both `review/` records, read by exactly four families:
status validity, standard backing, **ratified provenance**, succession integrity.
Those are the families this ratification could have broken.

**AND THE FAMILY NAMES THIS CHANGE ZERO TIMES**, in the family report and in the
whole-repository report alike — `grep -c amend-marker-defect-reporting` returns
**0** against both. So the block raises no carriage finding from its own family
while the family is demonstrably reading it: the adversarial pass proved the
reading with a mutation probe against the base tree, which fails 12 tests
including both new scenarios and all three flipped assertions.

## 8. `python3 scripts/doc-health.py --single-repo .` — THE WHOLE REPOSITORY, TWO CONTROLS

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `origin/main` `183d1b43` (worktree control) | 10 | 7 | 57 | 16 |
| this branch at `33907c73`, BEFORE the ratification was encoded | 10 | 8 | 57 | 16 |
| this branch, AFTER it was encoded | 10 | 8 | 57 | 16 |

All three report `New regressions vs previous report: 0`, and all three exit 0.

- **Against the PRE-RATIFICATION branch, the diff of the finding lines is
  EMPTY.** The status flips, the three citation lines, the approval pair, the
  README row and both new record files together add **not one finding**. That is
  the measurement that matters here, because it is the only one that isolates the
  ratification act.
- **Against `origin/main` `183d1b43`, the finding-line diff is ONE LINE, and it
  is not this packet's:**

  ```
  > - [error] REPO:openspec/changes/bump-openspec-cli-pin-to-1.12/review/ratification-2026-09-05.md — missing status header
  ```

  That is a pre-existing defect in ANOTHER change's ratification record, which
  #847 (`archive-bump-openspec-cli-pin-to-1.12`) archived out of the active
  lifecycle scan set on `main` after this branch's last merge from it. It is
  present on this branch for the same reason the item count in § 2 differs, it
  accounts for the entire 7 → 8 error delta, and **it disappears when the
  merge from `main` owed at landing is taken.** No finding line names any file
  of this packet.

### The families that could have spoken about this transition

`ratified-provenance` is live on this corpus and demonstrably so: the report
already carries SIX `critical` findings of its own against OTHER packets —
*"Ratified by: missing or does not resolve to an OpenSpec change"* once,
*"ratified header carries no citation in either sanctioned spelling"* four times,
and *"Ratified: names none of an approver, a date, or a resolvable record path"*
once — identically on `origin/main`, on the pre-ratification branch and here. The
count is **unchanged at 10 critical** (those six plus four `record-immutability`
findings against `docs/`) with this packet's three newly-`ratified` documents in
the scan set, so the ONE citation line each carries — `Ratified:` in
`proposal.md`'s front matter naming an approver, a date AND a resolvable record
path; `Ratified by: amend-marker-defect-reporting …` in `design.md` and
`tasks.md` — is checked by a family that is provably firing on this corpus, and
it passes. Both new `review/` records carry `Status: record` from the controlled
taxonomy, which is conforming and owes no citation, and each carries a `Ratified:`
line anyway rather than a third spelling.

## 9. What the merge from `main` owed at landing will move

Stated in advance so the re-measure can be checked rather than trusted:

1. **§ 2's item count** rises or falls with the change directories #842, #846 and
   #847 add and archive. **The failure SET is expected to stay these three**; if a
   fourth appears it is `main`'s and must be attributed there.
2. **§ 8's error count** falls 8 → 7 as the
   `bump-openspec-cli-pin-to-1.12/review/ratification-2026-09-05.md` finding
   leaves the active scan set with #847's archive.
3. **§ 7's and § 8's headline word totals** take `main`'s figures.
4. **Nothing in § 1, § 3, § 4, § 5 or § 6 is expected to move**, and § 5's row
   count rises only by rows `main` brings.
5. **#846 rewrote the origin-retention walk** (*"refuses a moved path instead of
   silently re-basing to the rename commit"*) and **#842 added the
   disposition `cited_to` arm**. Both are `main`'s code and neither is on this
   branch yet, so § 4's `proposal-support verify` is recorded here as the OLD
   walk reads it; the merge re-runs it under the new one. This packet's directory
   has never moved or been copied, and its `cited_to` declarations are none, so
   no interaction is expected — which is a prediction, and the re-run is what
   settles it.

## 10. `python3 -m pytest`

```
tests/doc-health/test_modified_block_currency.py tests/doc-health/test_modified_block_currency_fixtures.py -q
178 passed in 4.47s
```

`tests/doc-health/test_modified_block_currency_fixtures.py` alone therefore
carries the remaining **39**, one of them the flipped REAL instance
`test_the_inner_backtick_does_not_truncate_the_named_unit`.

```
tests/doc-health -q
1646 passed, 7 warnings in 360.51s (0:06:00)
```

`tests/doc-health/test_modified_block_currency.py` alone: **139 passed**
(128 → 139, eleven ADDED and three assertions FLIPPED, none loosened).
**THE COUNT REPRODUCES THE ADVERSARIAL PASS'S 1646 AT THE FROZEN HEAD
`9d4cf85b`**, which is the check that matters: neither the fix commit nor the
ratification commit touches a test file or a production module — the fix moves
four Markdown documents and the encode moves three of those plus
`.openspec.yaml`, `README.md` and two new records — so a status flip, a citation
line, an approval pair and two record files add, edit and remove no test, and the
suite is expected to be unmoved. It is.

## 11. Independent review

**CODEX ABSENT, recorded as absence and not as clearance** — `@codex review`
requested at 14:22:07Z, refused at 14:22:18Z on usage limits. **No Codex round
ran on this packet.** **Sourcery** (14:21:43Z) is the private-repo upsell stub.
**Copilot ran THREE times**: 14:24:51Z *"Changes recommended"* with two concrete
findings (a stale return-type annotation on `suppression`, a duplicated `basis`
comment), **both taken in `97a0c5e3`**; 14:31:56Z **"Approval recommended"**, 0
new comments, 10/10 files reviewed; and 15:47:46Z, after the merge from `main`,
*"Needs a closer look"* with 0 new comments on the ground that the packet amends
promoted normative behaviour and warrants final human review. No inline thread
stands unresolved. The **adversarial pass** (Opus, read-only, frozen head
`9d4cf85b`, 16:44:18Z) returned **READY TO ENCODE** with one fix-before-encode
finding — taken in the commit immediately preceding the ratification — one taken
nit and three recorded dispositions. The full disposition is
`ratification-2026-09-09.md` § 5.
