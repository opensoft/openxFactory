# Quickstart: validating F4

Run from the feature worktree root
(`/home/brett/projects/xFactory/openxFactory-worktrees/022-modified-block-currency-reporting`).
Nothing here needs a network, a token, or the aggregation checkout.

## 1. See the section the feature exists for

```bash
python3 scripts/doc-health.py --single-repo . \
  --family modified-block-currency --report-out /tmp/f4.md
sed -n "/^### modified-block-currency/,/^### /p" /tmp/f4.md | head -20
```

Expected: the heading, the lead line, four class bullets whose counts sum to the
rows below, then the rows. At this branch point the counts are 1 / 8 / 0 / 0.

## 2. The three states the block has

```bash
# ran, with findings           -> block present
python3 scripts/doc-health.py --single-repo . --family modified-block-currency \
  --report-out /tmp/f4-ran.md
grep -c "Finding classes, counted apart" /tmp/f4-ran.md     # 1

# skipped by run configuration -> block ABSENT, skip reason present
python3 scripts/doc-health.py --single-repo . \
  --skip-family modified-block-currency --report-out /tmp/f4-skipped.md
grep -c "Finding classes, counted apart" /tmp/f4-skipped.md  # 0
```

The third state (ran, found nothing) needs a tree with active changes but no
lossy MODIFIED block; it is covered in-process by the test suite rather than by a
command here, because constructing that tree by hand is slower than reading the
assertion.

## 3. The feature's own tests

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_reporting.py -q
```

## 4. The whole suite, which is also archive-gate evidence

```bash
python3 -m pytest tests/doc-health -q
```

The branch-point baseline lives in `research.md` § "The measurements this feature
starts from" and nowhere else; `evidence/f4-gates.md` records the after-figure
beside it, so the added tests are visible as a delta.

## 5. The report-movement gate (packet section 4.5, F3's, re-run here)

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py \
  -q -k report_moves_only
```

F4's new lines land INSIDE `### modified-block-currency`, which that gate already
permits. If it reds, F4 has leaked outside the family's section — read the
failure's `differing - permitted` list before changing anything.

## 6. No workflow, no openspec change

```bash
git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/
```

Expected: empty output. Any line here is a scope violation, not a finding to
disposition.

## 7. OpenSpec validation

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

## WHEN A TEST FAILS

- **`test_every_finding_classifies_into_exactly_one_class`** — a rule text moved
  and the class map did not. Fix the map, not the assertion: an unmatched finding
  becomes an `unclassified` row on the nightly report, which is the visible half
  of the same defect.
- **`test_no_other_family_s_section_or_action_line_moves`** — the render
  generalisation leaked. It must emit NOTHING for a family with no registry
  entry; a stray blank line for every family fails here and is the intended
  catch.
- **the subtotal counts disagree with the rows** — that is invariant I1
  (`data-model.md`). The tally is computed from the same list the rows are
  rendered from, so a disagreement means the class map dropped a finding.
- **F3's self-gate reds on a corpus subject** — not F4's. F3's
  `quickstart.md` section WHEN THE GATE FAILS owns that path, and F3's hand-off
  records which four assertions fall due when the packet archives.
