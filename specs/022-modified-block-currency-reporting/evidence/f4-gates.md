# Evidence: F4 gates, mutation round, and archive readiness

Status: record
Kind: report

Feature `022-modified-block-currency-reporting`, packet
`add-modified-block-currency-check` § 5. Every number below was produced by the
command printed beside it, in the feature worktree, on 2026-08-27.

## 1. The branch-point baseline (T001)

The single home for the before-figures. `research.md` § "The measurements this
feature starts from" carries the same table by reference; nothing else restates
them.

| measurement | value | command |
| --- | --- | --- |
| `tests/doc-health` before | **1178 passed** (192.9s) | `python3 -m pytest tests/doc-health -q` |
| the family over this checkout | **1 `warning`, 8 `info`** (9 findings) | the family through F3's two-attribute stand-in |
| classes populated | titles 1, ledger 8, resolution 0, markers 0 | the class map, over those 9 |
| this family in `.github/` | **0 mentions**, either spelling | `grep -rn "modified.block.currency\|modified_block_currency" .github/` |
| per-family options in the workflow | **1** (`--promotion-fidelity-basis live-main`) | the § 5.3 probe, W2 |
| fixture-corpus findings by class | titles 3, ledger 13, markers 1, resolution 2, ordering 9 (28 over 13 trees) | the family over each of F2's trees |

## 2. RED-first evidence, per group

Every test was written before the code it asserts and shown failing. Where the
subject ALREADY EXISTED (F1's action line, the workflow's silence), a test cannot
be RED against a missing implementation — those were shown RED by mutating the
subject, and each such mutant is in § 3 with the test it killed.

| group | tests | observed RED |
| --- | --- | --- |
| the class map + tally (T002–T009) | 10 | `10 failed in 1.16s` — every one an `AttributeError` on `mbc.CLASSES` / `mbc.classify` / `mbc.class_summary`, which did not exist |
| the block reaches the report (T010–T017) | 6 | `6 failed, 10 passed` — registry absent, block absent, and the two skip tests RED on their own positive controls |
| the action line + byte identity (T019–T022) | 5 | subject pre-existed; RED shown by mutants M1, M4, M5, M8 (§ 3) |
| the workflow boundary (T023–T025) | 4 | subject pre-existed; RED shown by mutant M3, and by a genuine first-cut defect (§ 2a) |

### 2a. The § 5.3 probe's first cut was wrong, and its own positive control caught it

The first `_family_mentions` read step `run` text plus `env`/`with` VALUES. The
positive control — a scratch workflow with `MODIFIED_BLOCK_CURRENCY_BASIS:
live-main` inserted — FAILED: `AssertionError: []`. An env KEY is conventionally
UPPER_SNAKE, so the only read that sees it is a case-insensitive read of the KEY,
which the probe did not do. Fixed to walk keys AND values, case-insensitively,
and the control now exercises all three shapes a per-family option can arrive in
(the flag in `run`; an env key named for the family; an env value carrying the
flag text). **This is why the positive control is a permanent test rather than a
step of the mutation round.**

## 3. The mutation round

Applied one at a time to the working tree, targeted pytest run, reverted. The
harness is 30 lines and lives in the session scratchpad, not in the repository.

| mutant | change | result |
| --- | --- | --- |
| **M1** drop the subtotal | remove the `FAMILY_SUMMARIES` branch from `report.render` | **KILLED** — 7 failed / 19 passed |
| **M2** change another family's action line | `promotion_fidelity._ACTION` → `"MUTANT apply the ratified delta…"` | **SURVIVED — 85 passed.** See § 3a |
| **M3** a per-family option for this family | a SCRATCH copy of the workflow carrying `--modified-block-currency-basis live-main`; the tracked file verified unchanged after | **KILLED** — `test_the_workflow_passes_no_per_family_option_to_this_family` failed, 3 passed |
| **M4** leak one blank line per family | `if notes: out.append("")` → unconditional | **SURVIVED FIRST, THEN KILLED.** See § 3b |
| **M5b** a JOB-level `env` carries the flag | a SCRATCH copy with `MODIFIED_BLOCK_CURRENCY_BASIS: live-main` inserted into `jobs.prepare.env` (which already exists) | **SURVIVED, THEN KILLED.** See § 3c |
| **M5** drop the residual bullet | delete the `if counts[UNCLASSIFIED]:` branch | **KILLED** — 1 failed |
| **M6** drop the skip guard | `if not skipped and family in …` → `if family in …` | **KILLED** — both skip tests failed |
| **M7** drop the repr anchor (blunt form) | `_BLOCK_HEAD` loses the title matcher entirely | **KILLED** — 13 failed (the map matches nothing; a break-everything mutant) |
| **M7b** greedy head instead of the anchor | `_BLOCK_HEAD` → `^active MODIFIED block for .*` | **KILLED** — exactly 1 failed, the title-embeds test. The precise anchor mutant |
| **M8** `classify` never returns `UNCLASSIFIED` | fall through to `CLASS_LEDGER` | **KILLED** — 1 failed |

### 3a. M2 survived, and the brief's expectation for it cannot hold

The brief predicted "change another family's action line → the byte-identity test
reds". **It cannot, by construction**, and the round proves it: the byte-identity
test compares registry-ON with registry-OFF over ONE finding set, so any mutation
that affects both renders equally is invisible to it. A changed action CONSTANT
is exactly that.

**And it is worse than that, which is the finding worth carrying to review.**
Mutating `promotion_fidelity._ACTION` reds NOTHING in `tests/doc-health` — 85
tests green over that family's own suite and F4's. No test in this repository
pins that family's action text. That is a gap in `promotion-fidelity`'s suite,
and closing it from F4 would mean snapshotting twenty-one other families' action
texts in this feature's test file, which would then red on their authors' PRs for
their own legitimate edits — the blast-radius cost F3's open question is about.

**What F4 does instead**, recorded in the test itself: § 5.2's "no other family's
action line changed" is realized as "F4's change cannot alter them", proved two
ways — a differential comparison over a fixed multi-family finding set, and
ABSOLUTE assertions stating another family's whole section and whole ranked-plan
rows (`action="…"` included) byte-for-byte.

### 3b. M4 survived the first cut, and that is why the absolute assertions exist

The first byte-identity test was purely differential. A mutant appending one
unconditional blank line to EVERY family's section — perturbing all twenty-two —
passed **26 green tests**. Same reason as M2: it moved both sides of the
comparison identically.

Fixed by stating the before-state instead of differencing it: for a family with
neither a note nor a summary entry, the section is its heading, ONE blank line,
then its rows — which is what `report.render` emitted before this feature
existed. M4 re-run: **KILLED**, 1 failed. The two absolute assertions are the
only ones in the file whose value is that a relative comparison cannot satisfy
them.

### 3c. M5b survived, and the probe had two blind spots

**Found by the combined review of 2026-08-27, not by this session's round.** The
first `_family_mentions` walked `jobs.*.steps.*` only. GitHub Actions resolves
`env` at THREE levels — workflow, job, step — and a variable set at any of them
is visible to every `run` beneath it, so a job-level
`MODIFIED_BLOCK_CURRENCY_BASIS: live-main` passed the pin green. **Both jobs in
this workflow already carry a job-level `env` block** (`HAS_APP_KEY`,
`HAS_ANTHROPIC_KEY`), so the missed shape was one line from an existing one.

Fixed by adding `_scopes`, which walks workflow-level `env`, each
`jobs.<id>.env` and `jobs.<id>.with` (for a job calling a reusable workflow), and
every step's `env`/`with`, beside the step `run` sweep. M5b re-run: **KILLED** —
`test_the_workflow_passes_no_per_family_option_to_this_family` failed, tracked
file verified byte-identical afterwards. The positive control now exercises four
shapes at three scopes.

One follow-on defect the mutant exposed in the control itself: its first
injection asserted `all("run" in f for f in found)`, which fails for the wrong
reason once the base file carries a mention of another shape. Relaxed to `any`,
which is what each injection actually claims.

### 3d. The partition assertion was tautological, and the true figure is 0 of 37

Also the combined review's. The first cut read

```python
hits = [c.id for c in mbc.CLASSES if mbc.classify(f) == c.id]
assert len(hits) == 1
```

`classify` returns ONE id, so `hits` can never exceed one however many patterns
match: the assertion proved "classify returns something in CLASSES" and was blind
to the property it was named for. Rewritten to iterate `_CLASS_PATTERNS` and
assert one MATCH, with `classify`'s answer checked against it.

**Measured on the corrected assertion: 37 findings (13 fixture trees + the real
corpus), 0 with anything other than exactly one matching pattern.**

## 4. Gates

| gate | result | command |
| --- | --- | --- |
| doc-health suite | **1204 passed** in 138.1s (+26 vs 1178) | `python3 -m pytest tests/doc-health -q` |
| OpenSpec | **76 passed, 0 failed** | `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` |
| F1 + F2 + F3 + promotion-fidelity + F4 | **235 passed** | `python3 -m pytest tests/doc-health/test_modified_block_currency{,_fixtures,_self_gate,_reporting}.py tests/doc-health/test_promotion_fidelity.py -q` |
| `.github/` + `openspec/` diff | **empty** | `git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/` |
| repo-local validators | **none affected** | every `scripts/validate-*.py` validates contract or governance YAML; this feature adds none and edits none |

### 4a. F2's production-surface guard reddened, and was amended rather than loosened (T040)

`test_modified_block_currency_fixtures.py::test_this_feature_touches_no_production_module`
snapshots the module's public callable surface. F4 adds four names —
`FindingClass`, `classify`, `class_counts`, `class_summary` — so the snapshot
failed:

```text
E   At index 1 diff: 'FindingClass' != 'Marker'
E   Left contains 4 more items, first extra item: 'resolve'
1 failed, 208 passed
```

**The guard worked and its own instruction was followed.** Its docstring says: "If
this test needs changing, a behaviour changed and FR-023 applies — the fix is its
own task with its own RED test, named as a defect in the PR, never folded into a
fixture commit." F4 DOES add behaviour, deliberately, by packet § 5.1. The
snapshot was extended with the four names and a dated paragraph recording who
added them and why. F2's own claim — that *F2* adds no behaviour — is untouched,
and no severity, rule text or fixture assertion moved.

## 5. Report movement (T028) — archive-gate evidence

Two single-repo runs of this checkout differing only by
`--skip-family modified-block-currency`:

```text
without:  5 critical,  7 error, 40 warning,  4 info
with:     5 critical,  7 error, 41 warning, 12 info
          ------------------------------------------
movement:  0           0        +1          +8
```

Equal to the family's own per-severity counts (1 `warning`, 8 `info`) and to
F3's re-measured figure at `175682e2`. **The `error` and `critical` bands do not
move**, so a `--fail-on error` run is unaffected.

**Confined, section by section.** The report carries a dated H1 and **30**
`##`/`###` headings; exactly **three** of the thirty differ:

| section | what moved |
| --- | --- |
| `## Headline` | the counts line, and the `- \`modified-block-currency\` — skipped by run configuration` notice on the skipped run |
| `### modified-block-currency` | 1 line → 14: the 5-line subtotal block and the 9 rows |
| `## Ranked Plan` | 9 rows, **all** carrying `family=modified-block-currency` |

Census, per-stage counts, preflight, catalog, and every one of the other
twenty-one family sections are byte-identical.

## 6. The rendered section, as a reader sees it

```text
### modified-block-currency

Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 1 (`warning` — the arm carrying this family's gate)
- carriage ledger: 8 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)

- [warning] …/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' omits 1 of the 2 scenarios …
- [info] …/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' does not carry 2 of the 6 body units …
… seven more info rows …
```

## 7. Archive readiness (packet § 8.1) — RECORDED, NOT DISCHARGED

§ 8's boxes are **NOT** ticked by this feature and the change is **NOT**
archived. What § 8.1 asks for is here:

| § 8.1 requirement | status |
| --- | --- |
| `pytest tests/doc-health` green | **1204 passed** (§ 4) |
| `openspec validate --all --strict` green | **76 passed, 0 failed** (§ 4) |
| a doc-health run moving by exactly the prediction | **+1 `warning`, +8 `info`**, 0/0 in the gated bands, movement confined to 3 of 30 headings (§ 5) |

**§ 4.5's own prediction was `+1 warning, +11 info`** and is history: it was
measured at `9be81a40` over 23 blocks, F3 re-measured 9 then 8 as the corpus
moved, and the ledger arm is advisory precisely because that population moves.
The invariant that must hold — and does — is that the movement EQUALS the
family's own counts and that the `error`/`critical` bands do not move.

**Still owed at the archive gate, and F4 does not touch it**: § 8.2's
byte-for-byte verification of this change's own promotion, and F3's list of four
assertions that fall due on the archive day.

## 8. CI shape, proved outside a worktree (T035)

F3's lesson: an environment-sensitive test must be run the way CI runs it, not
the way a developer's worktree happens to allow. This feature's test file reads a
tracked workflow file and spawns two `scripts/doc-health.py` subprocesses, so it
was run in a checkout with **no worktree, no history and no remote**:

```bash
git archive HEAD | tar -x -C <bare-dir>
cd <bare-dir> && git init -q .
python3 -m pytest tests/doc-health/test_modified_block_currency_reporting.py -q
#  => 26 passed in 2.68s
```

Cheap here because the workflow file is tracked, and the two subprocess runs are
pointed at F2's smallest fixture tree rather than at this repository — 0.17s per
invocation instead of seconds, and no dependency on the corpus for a question
about argparse.

## 9. RE-MEASURED AFTER MERGING `origin/main` — THE FIGURES DID NOT MOVE

`origin/main` advanced five commits while this feature was in flight, and two of
them touch the corpus this family reads: `govern-derived-pin-reachability`
ARCHIVED (so its deltas left the active set) and `supersede-lost-pin-baseline`
arrived as a new active change carrying a `doc-health` delta. Merged at
`origin/main` `94933adf`; **no rebase, per the feature's git rules.**

| measurement | before the merge | after |
| --- | --- | --- |
| active MODIFIED blocks examined | 22 (12 changes, 13 capabilities) | **22** (12 changes, 13 capabilities) |
| scenario-title completeness | 1 `warning` | **1** `warning` |
| carriage ledger | 8 `info` | **8** `info` |
| title resolution / ordering / markers | 0 / 0 / 0 | **0 / 0 / 0** |
| report movement | +1 `warning`, +8 `info` | **+1 `warning`, +8 `info`** |
| `.github/` + `openspec/` diff | empty | **empty** |
| F1 + F2 + F3 + F4 suites | 235 with promotion-fidelity | **176 passed** (the four family suites) |
| `pytest tests/doc-health` | 1204 passed | **1209 passed** (main brought five) |
| `openspec validate --all --strict` | 76 passed / 0 failed | **76 passed / 0 failed** |

**F3's exact-set gate survived the merge**, which is worth recording precisely
because it is the gate F3's open question is about: the new active change's
`doc-health` delta drew no carriage finding, so `_LEDGER_SUBJECTS` needed no row.
Had it drawn one, the remedy would have been F3's — re-measure and update the row
with the cause beside it, never loosen — and it would have landed on this PR.
