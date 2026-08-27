# Quickstart: running and re-measuring the self-gate

Every command below runs from the worktree root
`/home/brett/projects/xFactory/openxFactory-worktrees/021-modified-block-currency-self-gate`.

## Prerequisites

- Python 3.12, `pytest`
- `openspec` on PATH (for the validate gate)
- **Never** run `python3 -m pytest tests` (the whole tree) from a worktree — it
  drives live Postgres containers. `tests/doc-health` is the suite of record
  (F1 ruling N12).

## 1. Run the gate

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py -q
```

Expected: all green. The two report subprocess runs make this file the slowest in
the directory (~15s); everything else in it is sub-second.

## 2. Run the suite it belongs to

```bash
python3 -m pytest tests/doc-health -q
```

Expected at `76a2ad27` + this feature: **1127 passed** (baseline 1115 + 12).

## 3. See what the family says about this checkout

```bash
python3 scripts/doc-health.py --single-repo . --family modified-block-currency
```

This is the command the gate's failure messages tell you to run. Expected at
`76a2ad27`: 1 `warning`, 9 `info`, listed in `plan.md` § The named subjects.

## 4. Reproduce the movement pin by hand

```bash
python3 scripts/doc-health.py --single-repo . --report-out /tmp/with.md
python3 scripts/doc-health.py --single-repo . \
        --skip-family modified-block-currency --report-out /tmp/without.md
diff /tmp/without.md /tmp/with.md
```

Expected: 4 hunks, 24 changed lines — the headline, the skipped-family notice,
the `### modified-block-currency` section, and the ranked-plan rows for this
family. Nothing else.

## 5. The other two gates

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict     # 76 passed at 76a2ad27
git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/
```

The second must print **nothing**: this feature touches tests and specs only
(FR-019).

---

## WHEN THE GATE FAILS — read this before editing anything

The gate asserts **named subjects in a live corpus**. It is designed to fail when
the corpus legitimately moves, and the failure message says which of these it is.

### "the named subject … no longer appears"

The corpus moved. Most likely one of:

- **`add-composed-view-authoring` declared its rename.** Expected, and correct:
  the packet's § 6.3 identifies the finding as a deliberate rename and the
  `Removed from canon by` marker as its proper disposition. The `warning` goes
  away. Update `_SCENARIO_SUBJECT` to `None` and let the test assert the
  scenario-arm band is empty — by the same named mechanism, with the discovery
  floor still proving the family ran.
- **A change in the ledger table archived.** Drop its triple from
  `_LEDGER_SUBJECTS`.
- **A new active change landed a lossy MODIFIED block.** Add its triple. Read the
  finding first: if the block genuinely dropped an obligation, the right fix is in
  *that change*, not here.

Re-measure with step 3, then update the named set. Commit the re-measurement in
the same commit as the update, and say which subject moved and why.

### "discovery examined 0 MODIFIED blocks"

**This is not corpus movement.** The family's discovery broke —
`active_blocks`, `DELTA_GLOB`, or the resolved root. No corpus state produces
zero MODIFIED blocks in a repository with active changes; check the family, not
the table.

### "the repository under test is not the tree this test file lives in"

The resolver was changed, or the test is being run from a copied tree. The gate
must measure the checkout containing it — never an ancestor, never the
aggregation checkout, never another worktree.

### the movement pin fails

Something outside this family moved a report line. Diff the two reports by hand
(step 4) and look at which hunk is new. A moved `error` or `critical` count means
a `--fail-on error` run has newly started failing, which is a release-blocking
fact and not a test to relax.

## The end state

If a future corpus reads **zero** findings from this family, that is the
**desired** outcome, not a reason to delete the gate. Assert zero by the same
named-subject mechanism — an empty warning band, an empty ledger set — and keep
the discovery floor, which is the only assertion that then distinguishes "clean
corpus" from "broken reader". `test_family_enumeration.py`'s
`test_the_real_corpus_reads_zero_on_both_halves` is that shape after its own
subject was promoted, and its docstring records the re-aiming rather than hiding
it.
