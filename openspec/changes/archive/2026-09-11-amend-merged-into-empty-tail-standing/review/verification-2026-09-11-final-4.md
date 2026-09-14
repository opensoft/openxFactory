# Verification record: amend-merged-into-empty-tail-standing, aggregate-gate capture on the submitted tree, 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**ONE SENTENCE:** `review/verification-2026-09-11-final-3.md` carried
`review/verification-2026-09-11-final-2.md`'s aggregate-gate figures forward
across a merge that added a new active packet; this capture measures the
submitted tree for real (including two further merges from `main` picked up
while this capture was being taken) and supersedes both `final-2` and
`final-3` as the current aggregate-gate evidence. Neither superseded file is
edited (committed captures are never edited — lane hard limit, #887
`e65aed15` precedent).

## 0. Why FINAL-3 was wrong to carry the figures forward, and the merge this capture itself picked up

`final-3` re-verified only `validate-sequenced-after.py . --ledger-diff` and
`validate-scope-globs.py .` after the `596eb05f` merge (PR #960,
`amend-register-act-5b-projection-proof`, into this branch), reasoning that
PR #960's own diff touched only its own packet directory, one README row and
one ledger row. That reasoning is correct as far as it goes, but it does not
cover two gates it left unre-run: `openspec validate --all --strict` is
documented (`scripts/validate-openspec-cli-pin.py:1908-1910`) to validate
**every** change and specification in the corpus, and `doc-health.py`
(`scripts/doc_health/corpus.py:16-23`) likewise loads every packet's
`proposal.md` and `review/` records — so a merge that adds a new **active**
packet moves both gates' absolute item/finding counts even though it touches
none of this packet's own files. `final-2`'s aggregate figures were measured
on `a8235295` (main `34bb5c71`, before PR #960 landed).

While this capture was being taken, `origin/main` advanced a second time,
`ac688c40` → `29d4bebd` (PR #969, archiving
`honour-grandfather-dispositions-in-ratified-provenance`, landed at
`bc1f25c4` and merged at `29d4bebd`). That archive moves one change from
active to archived (`openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/`
→ `openspec/changes/archive/2026-09-11-honour-grandfather-dispositions-in-ratified-provenance/`,
a pure rename per its own commit `772d11c7`) and PROMOTES nine lines to
`openspec/specs/doc-health/spec.md` — a new scenario, *A finding is
grandfathered by a recorded disposition*, under the Release-inventory-drift
family's neighbouring requirement. `git diff ac688c40 29d4bebd -- openspec/specs/doc-health/spec.md`
shows this is the ENTIRE canon delta; it is a different requirement (the
lifecycle-scan/disposition family) from the one this packet's own delta
touches (*Currency of an active change's MODIFIED requirement blocks*, the
`Merged into`-marker fifth ground), so it does not conflict with or shadow
this packet's own sentence. This capture therefore merges `origin/main`
`29d4bebd` into the branch FIRST (merge commit, README's active-list
conflict resolved by dropping the now-archived row and keeping every other
row, matching `main`'s own resolution; `tests/sequenced_after/corpus-ledger.yaml`
auto-merged cleanly) and measures every gate below on that merged tree.

`origin/main` advanced a THIRD time while this capture's own commit was
being prepared, `29d4bebd` → `45bd9ee2` (PR #970, cutting contract release
`contract-v3.7`; `contracts/CHANGELOG.md`, `contracts/manifest.yaml`,
`contracts/releases/contract-v3.7.digests.yaml`,
`docs/contract-versioning-policy.md`, one other packet's `tasks.md`, and a
`tests/intent-compliance` test — no file under `openspec/changes/`,
`openspec/specs/` or `tests/doc-health/` moves). This capture merges that
commit too (clean, no conflicts, nothing under this packet's own directory
touched) and re-measures every gate a second time on the result, because
`doc-health`'s release-inventory-drift and release-tag-publication families
read exactly the `contracts/` files this merge changed — and indeed the
`info` finding count moves (§ 7) — while `--all --strict` (§ 3, unaffected:
no `openspec/` path touched) and `pytest tests/doc-health` (§ 8, unaffected:
no `tests/doc-health` path touched) do not. **The figures below are
measured on this final tree** (branch merge commit over `b97f6dd0` +
`29d4bebd` + `45bd9ee2`; `origin/main` `45bd9ee2` control) — a third
carry-forward was checked for and ruled out rather than assumed away.

## 1. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| tree these figures were taken on | `change/amend-merged-into-empty-tail-standing`, two merge commits over `b97f6dd0`: `origin/main` `29d4bebd` then `origin/main` `45bd9ee2` |
| `origin/main` at this verification | `45bd9ee2` (PR #970's merge, cutting contract release `contract-v3.7`) |
| what moved on `main` since `final-2`'s capture (taken against `main` `34bb5c71`) | PR #960 landed (`ac688c40`, one new active packet — already accounted for and re-verified by `final-3` for the two ledger/scope gates); PR #969 landed (`29d4bebd`, § 0 above, one active→archived move plus a doc-health canon addition); PR #970 landed (`45bd9ee2`, § 0 above, a contract release cut touching `contracts/`) — together these explain every item-count and finding-count delta from `final-2`'s numbers recorded below |
| `--all --strict` (both binaries) control | a `git worktree add` / `checkout` of `origin/main` `45bd9ee2` inside this clone (`../enc-947h-main-control`), directory-basename-independent comparisons |
| `doc-health` control | the same `origin/main` `45bd9ee2` worktree, findings compared by line content after normalizing the `Repo-Identity` label |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`; `openspec` on PATH **1.2.0**; pinned `openspec` **1.12.0** via `scripts/validate-openspec-cli-pin.py --cache-dir` (reused verified cache at `…/1aff33ce-…/scratchpad/pin-cache-937archive`); Python **3.12.3** |

## 2. `OPENSPEC_TELEMETRY=0 openspec validate amend-merged-into-empty-tail-standing --strict`

```
Change 'amend-merged-into-empty-tail-standing' is valid
```

Exit code 0.

## 3. `openspec validate --all --strict`, both binaries — branch vs. `origin/main` control

### 3a. PATH, `1.2.0`

Branch (this merge):

```
Totals: 100 passed, 2 failed (102 items)
```
Failing: `change/disposition-codexfactory-declared-renames`,
`change/disposition-codexfactory-floor-relocation-retitle`.

`origin/main` `45bd9ee2` control, same command:

```
Totals: 99 passed, 2 failed (101 items)
```
Failing: the same two names.

**FAILURE SET IDENTICAL BY NAME.** Unmoved by the third merge (PR #970
touches no `openspec/` path). The one-item difference (102 vs 101) is
this packet's own item, confirmed directly as in `final-2`'s method:
`grep -c '^✓\|^✗'` counts 102 lines on the branch run and 101 on the control
run, and `grep 'amend-merged-into-empty-tail-standing'` on the branch run
matches exactly the one line `✓ change/amend-merged-into-empty-tail-standing`,
absent from the control run. Both item counts are one LOWER than the
pre-second-merge measurement taken mid-capture (branch 101/103, control
100/102) because PR #969's archive removed one packet from the active set
counted by `--all` on both sides alike — never this packet's own count.

### 3b. The pinned CLI, `1.12.0`, via `scripts/validate-openspec-cli-pin.py --all --cache-dir <reused cache>`

Branch:

```
Totals: 100 passed, 2 failed (102 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

`origin/main` `45bd9ee2` control, same command:

```
Totals: 99 passed, 2 failed (101 items)
```
same two dispositioned exceptions, **0 undispositioned failures**, exit 0 on
both. Failure set identical by name on both sides, and identical to § 3a's
PATH run on both sides.

**THE DECOMPOSITION, ARITHMETIC SHOWN:** branch = 100 passed + 2
dispositioned-failed = **102 items** (100 + 2 = 102); control = 99 passed +
2 dispositioned-failed = **101 items** (99 + 2 = 101). The one-item
difference is this packet's own item, as in § 3a.

## 4. `python3 scripts/proposal-support.py . verify amend-merged-into-empty-tail-standing`

```
proposal support verification ok
```

Exit code 0.

## 5. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

Exit code 0. (Active-change count is 40, one lower than `final-3`'s 41,
entirely from PR #969's own archive move — one fewer active change, not
this packet's.)

### 5a. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
sequenced_after corpus sweep
----------------------------
change ids (40 active + 162 archived): 202
co-modified at requirement granularity (each would owe a declaration): 148
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 24 / 16
declaring `sequenced_after:`: 27 (accept-sequenced-after-header-line, add-consent-custody-rederivation-record, add-per-change-sweep-ledger, add-sequenced-after-substrate, admit-review-lane-repin-to-merge-approval-envelope, adopt-codexfactory-repository-identity, adopt-configured-notebook-hosting-identity, amend-chain-anchoring-readiness-and-durability, amend-marker-declaring-nothing, amend-merged-into-empty-tail-standing, amend-mirror-floor-regeneration-merge-authority, amend-modified-block-currency-standing, amend-neutral-product-pin-interim-copy-vocabulary, amend-neutral-product-pin-lockfile-first-line, amend-register-act-5b-projection-proof, amend-repo-boundary-governance-scope-first-line, disposition-codexfactory-floor-relocation-retitle, extend-merge-master-envelope-to-floor-bot-lanes, govern-archived-record-edits, honour-grandfather-dispositions-in-ratified-provenance, mirror-floor-addition-grace, mirror-floor-regeneration-automation, publish-openspec-cli-pin-as-contract-member, refresh-install-repository-enumerations, register-gate-rules-council-seats, relocate-review-authority-floor-mirror, state-header-window-budget)
declaring an explicit `[]` root claim: 8
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (202 rows).
```

Exit code 0. Total row count (202) is unchanged from `final-3`'s own figure
— PR #969's archive moves one row's classification (active → archived)
without adding or removing a row, so 40 active + 162 archived = 202,
against `final-3`'s 41 active + 161 archived = 202.

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

Exit code 0.

## 7. `python3 scripts/doc-health.py --single-repo .`

Branch: `Findings: 32 critical, 5 error, 47 warning, 14 info. New
regressions vs previous report: 0.` Marker defects: **0**. This change named
**0** times. Canon share by words: 39.6% (371184 canon words / 938477
governance words, promoted specs included).

**BYTE-IDENTICAL TO A FRESH `origin/main` `45bd9ee2` CONTROL RUN**, after
normalizing the `Repo-Identity` label (`sed 's/enc-947h-main-control/REPO/g;
s/enc-947h/REPO/g'` on both, then `diff`): the diff is EMPTY (346 lines each
side). Exit code 0 on both. **The `info` count DROPS from `final-2`'s 16 to
14 here, identically on branch and control** — not this packet's doing: PR
#970 (§ 0) cut `contract-v3.7`, and the release-inventory-drift family's two
`info` findings this repo carried (`contracts/README.md` and
`contracts/manifest.yaml` reading "bytes differ from the digest
`contract-v3.6` records — editorial member — expected between cuts") clear
once the tree matches the newly-cut `contract-v3.7` inventory instead. `32
critical, 5 error, 47 warning` are unchanged; canon share rose from 39.5%
(`final-2`) to 39.6% (PR #969's nine promoted lines), identically on both
sides.

## 8. `python3 -m pytest tests/doc-health -q`

```
1711 passed, 7 warnings in 419.27s (0:06:59)
```

Exit code 0. Unchanged from `final-2`'s capture (`1711 passed`) and from the
run taken before the third merge (§ 0) — no file under `tests/doc-health/`
moved across any of the three merges since `a8235295`.

## 9. What this capture does NOT change

**NOTHING ABOUT THE RATIFICATION'S OWN SUBSTANCE MOVED.** `git diff
--name-only 546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/`
remains EMPTY on this head; the packet's own delta, marker and scenario are
byte-identical to what Brett Heap's word ratified. `.openspec.yaml`'s
`origin:` block remains byte-identical to the ratifying commit `7215c207`
(`git diff 7215c207 -- .../.openspec.yaml` EMPTY). `git diff --stat` of this
pass's own two merge commits touches nothing under this packet's own
directory (§ 0). This capture commit itself touches only this file, the
README's active-list citation row and (via the separate merge commits) the
merges' own README/ledger reconciliation — bookkeeping about the state of
the pull request, not the delta itself.

## 10. Independent review, disposed on this head

**ONE THREAD OPEN AT THE START OF THIS PASS, RESOLVED BY THIS FILE:**

- `PRRT_kwDOTAvnrs6hhDsZ` (`review/verification-2026-09-11-final-3.md:78`) —
  the aggregate gates in `final-3` were carried forward from `final-2`
  (measured on `a8235295`) rather than re-measured on the merged head, even
  though `--all` and `doc-health` both load the whole corpus and PR #960 had
  added a new active packet. **TAKEN** by this file: every aggregate gate
  (§ 3, § 7, § 8) plus every single-change gate (§ 2, § 4, § 5, § 6) is a
  real run on the submitted tree — which, per § 0, itself picked up two
  further merges (PR #969, then PR #970) while this capture was being taken,
  each re-measured rather than assumed unaffected, so the figures above are
  measured on the final merged tree rather than on an intermediate one.

**CODEX: ABSENCE, unchanged.** One review request (2026-09-11T03:24:38Z) drew
a usage-limit refusal (2026-09-11T03:24:48Z), recorded verbatim at
`review/ratification-2026-09-11.md` § 5.3. No second request was made by
this or any later pass.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The Rule 6
LANDING/LANDED post belongs to the landing lane, on Brett Heap's standing word
"land each when green."
