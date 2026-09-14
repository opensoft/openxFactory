# Verification record: amend-merged-into-empty-tail-standing, final re-run 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**THIS FILE SUPERSEDES `review/verification-2026-09-11-post-merge.md`'s
CLAIM OF COMPLETENESS.** That capture's prose said "EVERY GATE WAS RE-RUN FROM
ZERO on `83dbd402`" but its own table listed only the PATH **1.2.0** `--all
--strict` run; the pinned **1.12.0** run it tabulated was still the
PRE-MERGE one, carried over from `review/verification-2026-09-11.md` rather
than re-run on `83dbd402` (Copilot thread `PRRT_kwDOTAvnrs6hdKKF`,
`review/verification-2026-09-11-post-merge.md:38`). Nothing in that file is
edited by this one — `document-lifecycle`'s one-shot-capture rule means a
further re-run writes a further dated path — and every figure it recorded for
`83dbd402` stays true of `83dbd402`; this file measures a LATER tree.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| tree these figures were taken on | `change/amend-merged-into-empty-tail-standing` at this lane's own further merge `7ce0c70b` (main `38c076d1`) plus the fix commit `a6d373e9` (restoring the README row, closing the #915/FR-018 residue, narrowing the § 1 status claim, fixing the § 5.6 cross-reference) — this file is committed on top of both |
| merges from `main` carried since the content freeze at `546e2c97` | `9dfa36f3` (main `1fb6d5cd`, a sibling lane pass that died before its own FREEZE); `6d10daed` (main `22efcbe8`, a second lane pass that also died before its own FREEZE); `1229006a` (main `22a2ecbc`, done immediately before the ratification encode `7215c207`); `83dbd402` (main `78d2c6f5`, taken after the encode when `gh pr ready` found the branch CONFLICTING); and this lane's own `7ce0c70b` (main `38c076d1`), taken at the start of this fourth author's pass |
| `origin/main` at this verification | `38c076d1` (PR #958's archive of `amend-repo-boundary-governance-scope-first-line`), unmoved since this lane's own merge |
| `--all --strict` (both binaries) control | a `git worktree add` of `origin/main` `38c076d1` inside this clone (`../enc-947c-main-control`), directory-basename-independent comparisons |
| `doc-health` control | the same `origin/main` `38c076d1` worktree, findings compared by line content after normalizing the `Repo-Identity` label |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`; `openspec` on PATH **1.2.0**; pinned `openspec` **1.12.0** via `scripts/validate-openspec-cli-pin.py --cache-dir` (reused verified cache at `…/1aff33ce-…/scratchpad/openspec-cli-pin-cache`); Python **3.12.3** |
| what moved since the ratification's own tabulation | `spec/repo-boundary-governance`'s `requirements.1` SHALL/MUST failure, KNOWN on `main` per `openxFactory` #931, was CLEARED by PR #958's archive landing on `main` between the post-merge capture and this one — so the PATH 1.2.0 `--all --strict` failure count drops from three names to two, on BOTH the branch and `main`, and the two remaining names are unchanged |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-merged-into-empty-tail-standing --strict`

```
Change 'amend-merged-into-empty-tail-standing' is valid
```

**Exit code 0.**

## 2. `openspec validate --all --strict`, both binaries

### 2a. The pinned CLI, `1.12.0`, via `scripts/validate-openspec-cli-pin.py --all --cache-dir <reused cache>`

Branch (`7ce0c70b`+`a6d373e9`):

```
Totals: 99 passed, 2 failed (101 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

`origin/main` `38c076d1` control, same command, same two dispositioned exceptions, **0 undispositioned failures**, exit 0. Failure set identical by name; item count differs by exactly this change's own item (101 vs 100 on main, both otherwise 2 dispositioned + 97 clean).

### 2b. PATH, `1.2.0`, `openspec validate --all --strict`

Branch:

```
Totals: 99 passed, 2 failed (101 items)
```
Failing: `change/disposition-codexfactory-declared-renames`, `change/disposition-codexfactory-floor-relocation-retitle`.

`origin/main` `38c076d1` control:

```
Totals: 98 passed, 2 failed (100 items)
```
Failing: the same two names. **FAILURE SET IDENTICAL BY NAME ON BOTH BINARIES**; the one-item difference (101 vs 100) is this packet's own item, passing on the branch and absent from `main`. `spec/repo-boundary-governance`, present in both binaries' failure sets at the pre-merge and post-merge captures, is ABSENT from both here — cleared on `main` itself by PR #958 between the post-merge capture and this one, not by anything this packet touches.

## 3. `python3 scripts/proposal-support.py . verify amend-merged-into-empty-tail-standing`

```
proposal support verification ok
```

Exit code 0.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

Exit code 0.

### 4a. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
change ids (39 active + 161 archived): 200
co-modified at requirement granularity (each would owe a declaration): 147
sole modifiers (each would declare `sequenced_after: []`): 53
ACTIVE changes: co-modified / sole: 24 / 15
declaring `sequenced_after:`: 25
declaring an explicit `[]` root claim: 7
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (200 rows).
```

Exit code 0.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

Exit code 0.

## 6. `python3 scripts/doc-health.py --single-repo .`

Headline: `Findings: 32 critical, 5 error, 47 warning, 15 info. New regressions vs previous report: 0.` Marker defects: **0**. This change named **0** times. Canon share by words: 39.5%.

**BYTE-IDENTICAL TO A FRESH `origin/main` `38c076d1` CONTROL RUN**, after
normalizing the `Repo-Identity` label (`sed 's/enc-947c-main-control/REPO/g;
s/enc-947c/REPO/g'` on both, then `diff`): the diff is EMPTY. Exit code 0 on
both.

## 7. `python3 -m pytest tests/doc-health -q`

```
1689 passed, 7 warnings in 467.93s (0:07:47)
```

Exit code 0. Identical count to every prior capture on this branch (pre-merge, post-merge) and to the pre-encode control run.

## 8. What this capture does NOT change

**NOTHING ABOUT THE RATIFICATION'S OWN SUBSTANCE MOVED.** `git diff --stat
546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/`
remains EMPTY on this head; the packet's own delta, marker and scenario are
byte-identical to what Brett Heap's word ratified, carried through five
merges from `main` and one fix commit untouched. This capture, and the fix
commit beneath it, touch only `README.md`, `review/ratification-2026-09-11.md`
and `tasks.md` — bookkeeping about the state of the pull request, not the
delta itself.

## 9. Independent review, disposed on this head

**THIRTEEN THREADS TOTAL ACROSS THE FULL BENCH; THE THREE STILL OPEN AT THE
START OF THIS PASS ARE NOW RESOLVED:**

- `PRRT_kwDOTAvnrs6hc6pZ` (`review/ratification-2026-09-11.md:395`) —
  the § 6.2 residue paragraph named openxFactory #915 as open and FR-018 as
  needing restatement; #915 is CLOSED (2026-09-11T01:29:59Z) and FR-018
  (`specs/019-modified-block-currency-family/spec.md:442`) already states
  FIVE grounds. **TAKEN** in `a6d373e9`; replied and RESOLVED.
- `PRRT_kwDOTAvnrs6hdDcm` (`tasks.md:230`) — the README `## OpenSpec Records`
  active-list row for this change was dropped by `83dbd402`'s conflict
  resolution. **TAKEN** in `a6d373e9`, restoring the row verbatim as the
  ratification commit `7215c207` wrote it; replied and RESOLVED.
- `PRRT_kwDOTAvnrs6hdKKF` (`review/verification-2026-09-11-post-merge.md:38`)
  — that capture's "every gate" claim outran its own table, which omitted the
  pinned 1.12.0 re-run. **TAKEN** by this file, which runs both binaries on a
  later head and states the correction in this file's own opening paragraph.

**NINE FURTHER SUPPRESSED COMMENTS ON `83dbd402` (no threads opened),
disposed here:**

1. `.openspec.yaml:49` — same README-row claim as thread 2. Disposition:
   TAKEN (see thread 2, above).
2. `.openspec.yaml:109` / `proposal.md:10` / `tasks.md:3` — flagged that the
   pull request's TITLE/BODY still read as draft / not-ratified / no
   approval pair. Verified directly: the title already reads "Ratify
   amend-merged-into-empty-tail-standing: rule the Merged-into empty tail
   silent in canon (refs #914)" and the body (rebuilt 11:46Z, before this
   review round) carries no "draft" / "NOT RATIFIED" / "no approval pair"
   sentence — `grep -ni "draft\|not ratified\|no approval pair\|awaiting"`
   on the fetched body returns only true, past-tense mentions of the
   ratification's own mechanics. Disposition: NO ACTION NEEDED, verified
   rather than assumed; the body is further updated in this pass only to
   name this lane's later commits and the final head.
3. `ratification-2026-09-11.md:395` — same as thread 1. TAKEN.
4. `ratification-2026-09-11.md:321` — the § 5.6 cross-reference pointed at
   "§ 10" for the API sweep, which is actually § 9. TAKEN in `a6d373e9`.
5. `ratification-2026-09-11.md:101` — "every status-bearing document flips
   to `Status: ratified`" is false of `review/verification-2026-09-11.md`,
   which stays `record`. TAKEN in `a6d373e9`, narrowed to name the four
   documents that do flip.
6. `tasks.md:343` — § 5.1 still read "RATIFY, THEN ARCHIVE" after the
   ratification had already landed. TAKEN in `a6d373e9`: rewritten to state
   that § 1 is done and only the archive act remains.
7. `tasks.md:318` — § 4.10 said "after two merges" when four (now five) had
   landed. TAKEN in `a6d373e9`, enumerating `9dfa36f3`, `6d10daed` and
   `1229006a` as the three preceding the encode, `83dbd402` as the fourth
   (after it), and this file records the fifth (`7ce0c70b`) and the fix
   commit `a6d373e9` in its own § 0 above.
8. (README row, `.openspec.yaml:49` restated) — see thread 2 / item 1.
9. (title/body draft language, restated across three files) — see item 2.

**CODEX: ABSENCE, unchanged.** One review request (2026-09-11T03:24:38Z) drew
a usage-limit refusal (2026-09-11T03:24:48Z), recorded verbatim at
`review/ratification-2026-09-11.md` § 5.3. Per the relaunch instructions in
force, no second request was made by this or any later pass.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The Rule 6
LANDING/LANDED post belongs to the landing lane, on Brett Heap's standing word
"land each when green."
