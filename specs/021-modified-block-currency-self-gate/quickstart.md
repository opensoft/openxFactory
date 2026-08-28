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

Expected: green. The baseline at `76a2ad27` is **1115 passed**; the count with
this feature is recorded in `evidence/self-gate.md` rather than predicted here —
one number, one home, measured by task T026.

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

Expected: 5 hunks, 24 changed lines — the headline, the skipped-family notice,
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

- **THIS CHANGE ITSELF ARCHIVED.** The nearest movement of all, and nearer than
  the composed-view rename: `add-modified-block-currency-check` archives after
  F4 lands (its § 8.1), and on that day
  `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`
  stops being an ACTIVE delta. Four assertions fall due together —
  `test_this_change_s_own_delta_is_among_the_blocks_the_family_examined`,
  `test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists`,
  `test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences`, and
  the self-finding triple inside `_LEDGER_SUBJECTS`. **Expected disposition**:
  the § 4.2 group has no live subject once the packet is archived, so either
  re-aim it at the archived path (`openspec/changes/archive/<date>-add-modified-block-currency-check/…`,
  which the family deliberately does NOT read — so this is a change of subject,
  not a path edit) or RETIRE the group at the archive gate with a dated record
  saying what it proved and when, in the shape
  `test_family_enumeration.py::test_canon_is_the_statement_under_test` used when
  its own subject was promoted. Do not delete it silently: § 4.2 is the
  assertion that discovery reached the packet that introduced the family.
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

**THE TWO HALVES CAN EMPTY SEPARATELY, AND THEY DID.** The warning band emptied
first, on 2026-08-27 (#444); the ledger has not — the movement-pin re-aim below
is conditioned on zero FINDINGS and does not yet apply.

**THE MOVEMENT PIN HAS TO BE RE-AIMED IN THE SAME COMMIT, and it is easy to
miss.** `test_the_report_moves_only_in_this_family_s_lines` carries two vacuity
guards — `assert f"### {mbc.FAMILY}" in differing` ("this family's own section
did not move") and `assert plan_moved` ("the ranked plan did not move") — which
exist to stop the two report runs passing when they rendered the same thing. At
zero findings **they are true of the desired state**, so the documented end
state is unreachable by the documented mechanism until they are re-aimed: at
zero, the family's section renders identically in both runs except for the
`--skip-family` notice, so the guard becomes an assertion about that one line
rather than about the section moving. The band comparison
(`movement == (0, 0, mine_warning, mine_info)`) needs no change — it reads
`(0, 0, 0, 0)` and is correct.
