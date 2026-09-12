# Verification record: amend-merged-into-empty-tail-standing, final re-run 2, 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**THIS FILE SUPERSEDES `review/verification-2026-09-11-final.md` AS THE CURRENT
EVIDENCE. IT DOES NOT EDIT IT** — `document-lifecycle`'s one-shot-capture rule
means a further re-run writes a further dated path. Two Copilot threads on
that capture are answered here rather than by editing it in place:

1. `PRRT_kwDOTAvnrs6hefH9` (`review/verification-2026-09-11-final.md:54`):
   that capture's § 2a closing sentence read *"both otherwise 2 dispositioned
   + 97 clean"*, which cannot follow from its own table — a control of 100
   items with 2 failed has 98 passing, and a branch of 101 items with 2
   failed has 99 passing. **This was an arithmetic slip in a committed
   capture**, not a re-measurement; § 2 below states the decomposition for
   THIS head's own numbers correctly, with the arithmetic shown.
2. `PRRT_kwDOTAvnrs6hfKTQ` (`review/verification-2026-09-11-final.md:24`):
   that capture measured `7ce0c70b`+`a6d373e9`, not the head the PR now
   submits. This file is the requested new one-shot verification record for
   the final head, `a8235295`, and every gate below is a fresh, real run on
   that tree.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| tree these figures were taken on | `change/amend-merged-into-empty-tail-standing` at `a8235295` — the merge of `main` `34bb5c71` (PR #945's landing) into `57b95b15` (the branch's prior head, itself `7ce0c70b`+`a6d373e9`+`4f2ca5c6`+`afbdc511`+`b1c92b50`+`f50b3fc8` beyond the ratification encode `7215c207`) |
| merges from `main` carried since the content freeze at `546e2c97` | `9dfa36f3` (main `1fb6d5cd`) and `6d10daed` (main `22efcbe8`), each by a lane pass that died before its own FREEZE; `1229006a` (main `22a2ecbc`, immediately before the ratification encode `7215c207`); `83dbd402` (main `78d2c6f5`, after the encode, when `gh pr ready` found the branch CONFLICTING); this lane's own `7ce0c70b` (main `38c076d1`); and this pass's own `a8235295` (main `34bb5c71`) — SIX merges from `main` in total since `546e2c97` |
| `origin/main` at this verification | `34bb5c71` (PR #945's merge of `honour-grandfather-dispositions-in-ratified-provenance`), unmoved since this lane's own merge |
| what moved on `main` since the prior capture (`review/verification-2026-09-11-final.md`, taken against `main` `38c076d1`) | PR #945 landed (`34bb5c71`), adding one active change and moving a README `## OpenSpec Records` row and one `tests/sequenced_after/corpus-ledger.yaml` row — this is why every `--all --strict` item count below is exactly one higher, on BOTH binaries and on BOTH sides (branch and control), than the prior capture recorded |
| `--all --strict` (both binaries) control | a `git worktree add` of `origin/main` `34bb5c71` inside this clone (`../enc-947g-main-control`), directory-basename-independent comparisons |
| `doc-health` control | the same `origin/main` `34bb5c71` worktree, findings compared by line content after normalizing the `Repo-Identity` label |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`; `openspec` on PATH **1.2.0**; pinned `openspec` **1.12.0** via `scripts/validate-openspec-cli-pin.py --cache-dir` (reused verified cache at `…/1aff33ce-…/scratchpad/pin-cache-937archive`); Python **3.12.3** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-merged-into-empty-tail-standing --strict`

```
Change 'amend-merged-into-empty-tail-standing' is valid
```

**Exit code 0.**

## 2. `openspec validate --all --strict`, both binaries — DECOMPOSITION SHOWN, NOT ASSERTED

### 2a. The pinned CLI, `1.12.0`, via `scripts/validate-openspec-cli-pin.py --all --cache-dir <reused cache>`

Branch (`a8235295`):

```
Totals: 100 passed, 2 failed (102 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

`origin/main` `34bb5c71` control, same command:

```
Totals: 99 passed, 2 failed (101 items)
```

same two dispositioned exceptions, **0 undispositioned failures**, exit 0 on
both. Failure set identical by name on both sides.

**THE DECOMPOSITION, ARITHMETIC SHOWN:** branch = 100 passed + 2 dispositioned-failed
= **102 items** (100 + 2 = 102); control = 99 passed + 2 dispositioned-failed
= **101 items** (99 + 2 = 101). The one-item difference (102 vs 101) is this
packet's own item — `change/amend-merged-into-empty-tail-standing` itself,
present and passing on the branch, absent from `main` — confirmed directly:
`grep -c '^✓\|^✗'` on the PATH run below counts 102 lines on the branch and
101 on the control, and `grep 'amend-merged-into-empty-tail-standing'` on the
PATH branch run (§ 2b) matches exactly the one line `✓
change/amend-merged-into-empty-tail-standing`, absent from the control run.
So: **branch = 2 dispositioned + 100 clean = 102; control = 2 dispositioned +
99 clean = 101.** (The superseded capture's "97 clean" — on its own, older
tree of 100/101 items — was arithmetically impossible for either side; the
correct reading of ITS numbers would have been 98 clean [control, 100 items]
and 99 clean [branch, 101 items], never 97 for either.)

### 2b. PATH, `1.2.0`, `openspec validate --all --strict`

Branch:

```
Totals: 100 passed, 2 failed (102 items)
```
Failing: `change/disposition-codexfactory-declared-renames`,
`change/disposition-codexfactory-floor-relocation-retitle`.

`origin/main` `34bb5c71` control:

```
Totals: 99 passed, 2 failed (101 items)
```
Failing: the same two names.

**FAILURE SET IDENTICAL BY NAME ON BOTH BINARIES**, on both branch and
control; the one-item difference (102 vs 101) is this packet's own item, as
in § 2a. `spec/repo-boundary-governance`, present in both binaries' failure
sets at the earlier (`final.md`) capture's tree, remains ABSENT from both
binaries' failure sets here — cleared on `main` itself by PR #958 before that
capture was taken, and unchanged since.

## 3. `python3 scripts/proposal-support.py . verify amend-merged-into-empty-tail-standing`

```
proposal support verification ok
```

Exit code 0.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

Exit code 0. (The active-change count rose from 39 to 40 and the ledger's
row count from 200 to 201 since the prior capture, entirely from PR #945's
own landing — one active change and one ledger row, neither this packet's.)

### 4a. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
change ids (40 active + 161 archived): 201
co-modified at requirement granularity (each would owe a declaration): 148
sole modifiers (each would declare `sequenced_after: []`): 53
ACTIVE changes: co-modified / sole: 25 / 15
declaring `sequenced_after:`: 26
declaring an explicit `[]` root claim: 8
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (201 rows).
```

Exit code 0.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

Exit code 0.

## 6. `python3 scripts/doc-health.py --single-repo .`

Headline: `Findings: 32 critical, 5 error, 47 warning, 16 info. New
regressions vs previous report: 0.` Marker defects: **0**. This change named
**0** times. Canon share by words: 39.5%.

**BYTE-IDENTICAL TO A FRESH `origin/main` `34bb5c71` CONTROL RUN**, after
normalizing the `Repo-Identity` label (`sed 's/enc-947g-main-control/REPO/g;
s/enc-947g/REPO/g'` on both, then `diff`): the diff is EMPTY. Exit code 0 on
both. (The info-finding count rose from 15, at the prior capture's tree, to
16 here, identically on both branch and control — a corpus-wide change from
PR #945's landing, not from this packet.)

## 7. `python3 -m pytest tests/doc-health -q`

```
1711 passed, 7 warnings in 488.13s (0:08:08)
```

Exit code 0. A prior run on this same tree, taken while several other
sessions' pytest suites were concurrently running on this shared machine
(observed via `ps aux`: at least seven other `pytest` invocations mid-flight
at the same wall-clock minute), reported `1 failed, 1710 passed` —
`tests/doc-health/test_release_tag_publication.py::test_a_successor_that_is_not_strictly_later_is_walked_around_backwards`,
a self-contained fixture test with no dependency on this packet. Re-run
alone it passed in 0.49s, and the full suite re-run above is clean at 1711
passed, 0 failed — recorded as a transient contention flake, not a defect,
and the clean re-run is what this capture certifies. Test count differs from
the prior capture's 1689 because the corpus itself grew (PR #945, #958)
between the two captures, not from anything in this packet.

## 8. What this capture does NOT change

**NOTHING ABOUT THE RATIFICATION'S OWN SUBSTANCE MOVED.** `git diff
--name-only 546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/`
remains EMPTY on this head; the packet's own delta, marker and scenario are
byte-identical to what Brett Heap's word ratified, carried through six
merges from `main` and the fix commits beneath it, unchanged. This capture
touches only this file and the README's active-list citation row — bookkeeping
about the state of the pull request, not the delta itself.

## 9. Independent review, disposed on this head

**TWO THREADS OPEN AT THE START OF THIS PASS, BOTH RESOLVED BY THIS FILE**
(see the opening section above for the substance of each):

- `PRRT_kwDOTAvnrs6hefH9` (`review/verification-2026-09-11-final.md:54`) —
  the impossible "97 clean" decomposition. **TAKEN** by writing this new
  capture with the arithmetic shown (§ 2a); `verification-2026-09-11-final.md`
  itself is NOT edited (committed captures are never edited — lane hard
  limit, #887 `e65aed15` precedent).
- `PRRT_kwDOTAvnrs6hfKTQ` (`review/verification-2026-09-11-final.md:24`) —
  that capture measured an earlier head. **TAKEN** by this file, the
  one-shot verification record of the head that lands, at its own dated
  path (`-final-2`), per `document-lifecycle`'s one-shot-capture rule.

**CODEX: ABSENCE, unchanged.** One review request (2026-09-11T03:24:38Z) drew
a usage-limit refusal (2026-09-11T03:24:48Z), recorded verbatim at
`review/ratification-2026-09-11.md` § 5.3. No second request was made by
this or any later pass.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The Rule 6
LANDING/LANDED post belongs to the landing lane, on Brett Heap's standing word
"land each when green."
