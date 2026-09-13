# Verification: rule-inherited-unit-naming-marker-spent

Status: record
Kind: report

**THE TREE THIS RECORD CERTIFIES IS THE FOURTH-MERGE TREE, BRANCH `98bd74e9`,
CONTROL BASE `a72f0a76`** — branch `change/rule-inherited-unit-naming-marker-spent`
after FOUR merges from `main` (`67b8011f` → `1f068646`, `78a5d2dc` →
`5972c8f3`, `4a246872` → `45a98faa`, and the fourth, `98bd74e9` →
`a72f0a76b14588e3cbc7b313af6222683daea72f` via PR #1005), the
per-change sweep ledger re-seed (`b42eb65d`: `depth` 0 → 1), the self-gate fix
(`396bca94`), and this ratification's own content commit. **§§ 1–11 BELOW
WERE TAKEN ON THE THIRD-MERGE TREE** — branch `4a246872`, against a fresh
control clone of `origin/main` at `45a98faa5f89f48a3d0b1842d111681b85e7f0ad`,
taken at `scratchpad/NEW/ctrl-main-962` — **AND ARE SUPERSEDED BY § 12**, which
re-derives every one of the same gates on the fourth-merge tree against the
same control clone fast-forwarded to `a72f0a76b14588e3cbc7b313af6222683daea72f`,
appended rather than retyped over them (`tasks.md` § 4.11, § 4.12's own
convention). Every command line and tail below is pasted from the actual run,
not recalled.

## 1. `openspec validate <change> --strict`

```
$ OPENSPEC_TELEMETRY=0 openspec validate rule-inherited-unit-naming-marker-spent --strict
Change 'rule-inherited-unit-naming-marker-spent' is valid
```

**Exit 0.**

## 2. `validate-openspec-cli-pin.py --change ... --no-cache`

```
$ python3 scripts/validate-openspec-cli-pin.py --change rule-inherited-unit-naming-marker-spent --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (...); integrity ... verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity ... verified; installed with `npm ci --ignore-scripts`
-> .../openspec validate rule-inherited-unit-naming-marker-spent --strict --json  (in .../enc-962)
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

**Exit 0.**

## 3. `openspec validate --all --strict` — branch vs. control

Branch (this checkout):

```
Totals: 102 passed, 3 failed (105 items)
```

**Real exit code 1** (captured directly, not through a pipe — an earlier
attempt piped through `tail` and silently reported the pipe's own exit
status; corrected). The 3 failures:

```
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
✗ change/disposition-codexfactory-regular-pr-council-clearance-archive
```

Control (`origin/main` @ `45a98faa`, fresh clone):

```
Totals: 101 passed, 3 failed (104 items)
```

**Exit 1**, the SAME 3 named failures, in the same order. The branch carries
exactly ONE more item than control (this packet's own change) and it PASSES;
the failing set is IDENTICAL between branch and control — **this packet adds
zero new `openspec validate --all --strict` failures**. All three named
failures are themselves ratified `disposition-*` packets already on
`origin/main`, unrelated to this packet.

## 4. `validate-openspec-cli-pin.py --all --no-cache`

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
...
✗→D add-chain-attestation / signed-execution-chain/spec.md
      ... accepted by: Brett Heap, 2026-09-05, "take exit 2"
✗→D add-composed-view-authoring / ideation-dashboard/spec.md
      ... accepted by: Brett Heap, 2026-09-05, "take exit 2"
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**Exit 0.** Both named exceptions are pre-existing, dispositioned by Brett
Heap on 2026-09-05 ("take exit 2"), and neither names this packet or its
requirement (`doc-health` § *Currency of an active change's MODIFIED
requirement blocks*). This packet contributes no new named exception here.

## 5. `proposal-support.py . verify rule-inherited-unit-naming-marker-spent`

```
proposal support verification ok
```

**Exit 0.**

## 6. `validate-sequenced-after.py .` and `--ledger-diff`

```
$ python3 scripts/validate-sequenced-after.py .
sequenced_after validation passed (43 active changes, 13 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit 0. NOW PASSES** — this validator was BLOCKED at the freeze
(`51edde81`) with *"a dangling parent reference is unwalkable"* because the
declared parent `amend-merged-into-empty-tail-standing` was still an open
pull request. It resolves cleanly now that the parent has both landed
(`87fd33d6`) and archived (PR #973): the declaration is unchanged, and
`scripts/validate-sequenced-after.py` resolves a declared parent in the
ACTIVE and the ARCHIVED corpora both, exactly as designed.

```
$ python3 scripts/validate-sequenced-after.py . --ledger-diff
change ids (43 active + 163 archived): 206
co-modified at requirement granularity (each would owe a declaration): 152
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 27 / 16
declaring `sequenced_after:`: 31 (... amend-merged-into-empty-tail-standing, ...
  decide-disposition-reading-per-family, ...
  rule-inherited-unit-naming-marker-spent, ...)
declaring an explicit `[]` root claim: 10
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (206 rows).
```

**Exit 0, no re-seed owed.** This packet's own row (re-seeded at commit
`b42eb65d`, before the second and third merges) reads, in
`tests/sequenced_after/corpus-ledger.yaml`:

```
rule-inherited-unit-naming-marker-spent: {state: active, class: co-modifier, declares: [amend-merged-into-empty-tail-standing], depth: 1, prose: false, moved_by: "#962", moved_on: "2026-09-12"}
```

`depth: 1`, `moved_on: "2026-09-12"` — matching the corpus exactly; the two
later merges (PR #1004, PR #978) each seeded their OWN row and moved no
figure of this one.

## 7. `validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit 0.**

## 8. `doc-health.py --single-repo .` — branch vs. control

Branch:

```
Findings: 31 critical, 9 error, 23 warning, 16 info. New regressions vs previous report: 0.
Canon share by words: 40.1% (372741 canon words / 929791 governance words, promoted specs included).
```

Control (`origin/main` @ `45a98faa`):

```
Findings: 31 critical, 9 error, 23 warning, 16 info. New regressions vs previous report: 0.
Canon share by words: 40.1% (372741 canon words / 929791 governance words, promoted specs included).
```

**Both exit 0. The two reports are BYTE-FOR-BYTE IDENTICAL** after
normalizing the `Repo-Identity:` label (`enc-962` vs `ctrl-main-962`, the
only difference `diff` finds) — `diff` on the normalized texts returns
nothing, exit 0. This delta's own transient `info` carriage-ledger row
(§ 3.7 of `tasks.md`), which the packet disclosed as open while its parent
sat off `main`, has already retired: it cleared on the parent's archive (PR
#973) reaching the active corpus, independent of this ratification
(`design.md` D2b's event (b)), and the self-gate fix at commit `396bca94`
removed the row from `tests/doc-health/test_modified_block_currency_self_gate.py`'s
`_LEDGER_SUBJECTS` to match. **The branch therefore adds ZERO findings and
removes ZERO relative to a clean `origin/main`.**

## 9. `doc-health.py --single-repo . --family modified-block-currency`

```
Findings: 0 critical, 0 error, 0 warning, 9 info. New regressions vs previous report: 0.
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**Exit 0. MARKER-DEFECT FINDINGS ARE 0.** The family's 9 `info` findings
(down from the TEN the freeze measured — this packet's own transient row
retired, per § 8 above) name `add-chain-attestation`,
`add-composed-view-authoring`, `add-credential-escrow-checkout`,
`add-doxchat-model-intake`, `amend-mirror-floor-regeneration-merge-authority`,
`declare-client-standing-policy-contract`, `qualify-avatar-live-voice` (×3,
different requirements) — **this packet's own path is named ZERO times**
(`grep -c rule-inherited-unit-naming-marker-spent` on the report: `0`).

## 10. `pytest tests/doc-health tests/sequenced_after -q --tb=no` — branch vs. control

Branch: **7 failed, 2003 passed, 1 skipped, 7 warnings in 398.03s (0:06:38)**.
Control: **7 failed, 2003 passed, 1 skipped, 7 warnings in 414.69s (0:06:54)**.

The failed set is IDENTICAL on both sides, all pre-existing and unrelated to
this packet:

```
FAILED tests/doc-health/test_ideation_readiness.py::test_validate_index_finds_pinned_validator_and_checks_bootstrap
FAILED tests/doc-health/test_ideation_readiness.py::test_validate_index_rejects_a_broken_index
FAILED tests/doc-health/test_ideation_readiness.py::test_pipeline_proof_scores_real_clusters_and_validates_clean
FAILED tests/doc-health/test_readiness_dispatch.py::test_merge_wires_the_real_validator_for_a_genuinely_scored_index
FAILED tests/doc-health/test_sentinel_vocabulary.py::test_the_declared_emitters_are_measured_rather_than_believed
FAILED tests/doc-health/test_sentinel_vocabulary.py::test_unknown_is_not_folded_into_the_unreadable_repository_condition
FAILED tests/doc-health/test_status_reader_real_lines.py::test_the_reader_finds_what_the_writer_just_wrote_through_an_exotic_header
```

**THE TWO DANGLING-PARENT FAILURES ARE GONE ON BOTH SIDES**:
`tests/sequenced_after/test_validate.py::test_corpus_sequenced_after_all_validate`
and
`tests/sequenced_after/test_archive_commit_dates.py::test_THE_LIVE_PLAIN_RUN_IS_GREEN_WITH_ZERO_UNDISPOSITIONED`
do not appear in either FAILED list — they cleared the moment the parent
landed and archived, exactly as § 4.7 (`tasks.md`) describes, and this is
true on `origin/main` itself, independent of this packet.

**THE SELF-GATE IS GREEN**: a targeted run of
`tests/doc-health/test_modified_block_currency_self_gate.py` alone reads
**19 passed** in 30.82s, zero failures — the exact-set assertion over
`_LEDGER_SUBJECTS` (now NINE named subjects, this packet's own row having
retired) holds.

## 11. `pytest tests/scope_globs tests/proposal-support -q --tb=no` — branch vs. control

Branch: **217 passed, 70 subtests passed in 46.88s.**
Control: **217 passed, 69 subtests passed in 46.78s.**

**Both exit 0, zero failures either side.** The ONE subtest difference is
`tests/proposal-support/test_proposal_support.py::test_the_guard_refuses_nothing_on_this_repository_today`,
which runs `with self.subTest(change=directory.name):` once per active
`openspec/changes/` directory — its own docstring: *"NO COUNT IS WRITTEN
DOWN, because the corpus gains and loses packets with every landing and a
number here is stale by the next one — the invariant is zero refusals over
WHATEVER is active, one subtest per change."* The branch carries one more
active change directory than the control (this packet itself), hence 70 vs
69; **zero refusals on either side**, which is the test's actual invariant.

## 12. Fourth merge from `main` (`a72f0a76`, PR #1005) — full re-run

A fourth merge from `main` followed this record being written (commit
`98bd74e9`, `main` having moved again from `45a98faa` to
`a72f0a76b14588e3cbc7b313af6222683daea72f` via PR #1005,
`repoint-chain-anchoring-medxchain-citation` — verified disjoint: it adds its
own change directory, edits `split-opendox-two-layer-product/tasks.md`
(ticking boxes, no requirement delta) and its own
`tests/sequenced_after/corpus-ledger.yaml` row; it touches neither
`openspec/specs/doc-health/spec.md` nor
`scripts/doc_health/modified_block_currency.py`). **ONE real conflict**,
`tests/doc-health/test_modified_block_currency_self_gate.py`: both sides had
extended the same trailing narrative comment and the same chained history
string immediately after it (this packet's own retirement narrative;
`repoint-chain-anchoring-medxchain-citation`'s three new rows). Resolved by
keeping BOTH extensions in full, this packet's first, chaining the history
string 10 SINCE 2026-09-11 → 9 SINCE 2026-09-12 (this packet's retirement) →
12 SINCE 2026-09-12 (the three new rows), nothing dropped either side.
README's `## OpenSpec Records` conflicted at the same insertion point as
every prior merge; resolved keeping main's `repoint-chain-anchoring-
medxchain-citation` row immediately after this packet's own, no reflow.
Every gate below is RE-DERIVED on the resulting tree (commit `98bd74e9`)
against a FRESH control clone fast-forwarded to the same `a72f0a76`
(`scratchpad/NEW/ctrl-main-962`), command lines and output pasted from the
actual run:

- `openspec validate rule-inherited-unit-naming-marker-spent --strict` (PATH
  `1.2.0`): **exit 0**, `Change 'rule-inherited-unit-naming-marker-spent' is
  valid` — unchanged.
- `validate-openspec-cli-pin.py --change ... --no-cache` (PINNED `1.12.0`):
  **exit 0**, `Totals: 1 passed, 0 failed (1 items)` — unchanged.
- `openspec validate --all --strict`: branch `Totals: 103 passed, 3 failed
  (106 items)` vs. control `Totals: 102 passed, 3 failed (105 items)` — the
  SAME three named failures on both
  (`disposition-codexfactory-declared-renames`,
  `disposition-codexfactory-floor-relocation-retitle`,
  `disposition-codexfactory-regular-pr-council-clearance-archive`, all
  pre-existing dispositioned packets, none of them this packet or
  `repoint-chain-anchoring-medxchain-citation`); `diff` of the two sorted `✗`
  lists is empty. Item and passed counts each move by exactly ONE on both
  sides — `repoint-chain-anchoring-medxchain-citation`'s own arrival in the
  active corpus, present on both branch and control alike since it came in
  via `main`.
- `validate-openspec-cli-pin.py --all --no-cache`: branch **exit 0**,
  `Totals: 104 passed, 2 failed (106 items)`, `0 UNDISPOSITIONED failures` —
  the SAME two accepted exceptions as every prior reading
  (`add-chain-attestation`, `add-composed-view-authoring`, Brett Heap,
  2026-09-05, "take exit 2"), neither this packet nor
  `repoint-chain-anchoring-medxchain-citation`. (Not re-run on control: this
  gate is self-contained — 0 undispositioned failures is the whole of what
  it asserts, unaffected by which other active changes a tree carries.)
- `proposal-support.py . verify rule-inherited-unit-naming-marker-spent`:
  **exit 0**, `proposal support verification ok` — unchanged.
- `validate-scope-globs.py .`: **exit 0**, `scope_globs validation passed
  (all active changes conform)` — unchanged.
- `validate-sequenced-after.py .`: **exit 0** (44 active changes now, 13
  declaring — up one active change, `repoint-chain-anchoring-medxchain-
  citation`, from the 43 this record's § 6 read). `--ledger-diff`: **exit
  0**, `per-change sweep ledger consistent with the corpus (207 rows)` (up
  from 206 — PR #1005 seeded its own row). This packet's own row is
  UNCHANGED: `rule-inherited-unit-naming-marker-spent: {state: active,
  class: co-modifier, declares: [amend-merged-into-empty-tail-standing],
  depth: 1, prose: false, moved_by: "#962", moved_on: "2026-09-12"}` —
  confirmed by direct read of `tests/sequenced_after/corpus-ledger.yaml`
  after the merge, no re-seed owed.
- `doc-health.py --single-repo .`: branch `Findings: 31 critical, 9 error,
  23 warning, 19 info. New regressions vs previous report: 0.` — control,
  same tree, reads IDENTICALLY: `31 critical, 9 error, 23 warning, 19 info`,
  `New regressions: 0`. **Both exit 0, BYTE-FOR-BYTE IDENTICAL** after
  normalizing the `Repo-Identity:` label (`enc-962` vs. `ctrl-main-962`, the
  only difference `diff` finds on the two full reports). The `info` count
  moves 16 → 19 relative to § 8 above — the three new
  `repoint-chain-anchoring-medxchain-citation` `modified-block-currency`
  rows, present identically on both branch and control since they arrived
  via `main`, not via this packet.
- `doc-health.py --single-repo . --family modified-block-currency`:
  `Findings: 0 critical, 0 error, 0 warning, 12 info. New regressions vs
  previous report: 0.` **Exit 0, marker defects 0.** The family's population
  moves 9 → 12 (the same three `repoint-chain-anchoring-medxchain-citation`
  rows named above); this packet's own path is named **ZERO** times
  (`grep -c rule-inherited-unit-naming-marker-spent` on the report: `0`),
  unchanged from § 9.
- `pytest tests/doc-health tests/sequenced_after tests/scope_globs
  tests/proposal-support -q --tb=no`: branch **7 failed, 2220 passed, 1
  skipped, 71 subtests passed in 454.00s**; control **7 failed, 2220 passed,
  1 skipped, 70 subtests passed in 463.17s**. `diff` of the sorted `FAILED`
  lines is EMPTY — the SAME seven pre-existing, unrelated failures § 10
  names (`test_ideation_readiness` ×3, `test_readiness_dispatch`,
  `test_sentinel_vocabulary` ×2, `test_status_reader_real_lines`); the
  passed count rises from 2003+217=2220 on both sides (the corpus itself
  grew by landed PRs between the two baselines, identically on branch and
  control); the one-subtest difference is the same documented
  per-active-change design § 11 describes, branch carrying one more active
  change (this packet) than control. The self-gate alone:
  `tests/doc-health/test_modified_block_currency_self_gate.py` — **19
  passed** in 30.36s, matching § 10 exactly.

**NO GATE NAMES THIS PACKET AS THE SOURCE OF A NEW FINDING OR A NEW FAILURE
ON THIS FOURTH-MERGE TREE.** Every population increase (the `all --strict`
item count, the `modified-block-currency` info count, the sweep-ledger row
count) is `repoint-chain-anchoring-medxchain-citation`'s arrival via `main`,
present identically on branch and control; every failure set is identical
between the two; this packet's own row in every ledger stays exactly where
§§ 1–11 above measured it.

## Summary

Every gate this packet's own `tasks.md` § 4 lists has been re-run on the
final tree — after a fourth merge from `main` (§ 12) — and produces either an
EXACT match with a fresh `origin/main` control (validate --all, doc-health,
the pytest failure sets) or a clean pass with a fully-accounted,
non-substantive difference (the sequenced_after ledger row's own history; the
one subtest that counts active changes by design). No gate reads this packet
as the source of a new finding, a new failure or a new marker defect anywhere
in the corpus, on any of the four merged trees measured.
