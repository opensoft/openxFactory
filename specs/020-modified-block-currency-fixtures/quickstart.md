# Quickstart: validating the fixture catalogue (F2)

Every command runs from the ROOT of this feature's worktree — the checkout
whose `git status -sb` reads `020-modified-block-currency-fixtures`. Paths below
are repo-relative (Constitution Principle IV: no host-absolute paths in
committed files).

**Never run `pytest tests` from a worktree.** Parts of that suite need a live
Postgres this checkout has no access to; a red there says nothing about this
feature. The gate for this feature is `tests/doc-health` (orchestrator
decision 5).

---

## 0. Baseline, before anything

```bash
python3 -m pytest tests/doc-health -q | tail -3
# expect: 1077 passed
OPENSPEC_TELEMETRY=0 openspec validate --all --strict 2>&1 | tail -3
# record the count; this feature must not move it
```

## 1. Re-derive the two reconstructions from git

Neither fixture is trusted because a file exists — it is trusted because these
commands reproduce it. Both SHAs are in the fixture's `README.md`.

```bash
# fixture A — #351, pre-repair
git show bcfc26a0:openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md \
  | diff - tests/doc-health/fixtures/modified-block-currency-history-351/intakeFactory/openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md
# expect: no output (the delta file is copied WHOLE)

# fixture A — the canon requirement, byte-identical inside synthetic scaffolding
git show bcfc26a0:openspec/specs/ideation-dashboard/spec.md \
  | awk '/^### Requirement: doxBench model catalog and provider boundary/{f=1} f&&/^### Requirement:/&&!/doxBench model catalog and provider boundary/{exit} f' \
  | diff - <(awk '/^### Requirement: /{f=1} f' tests/doc-health/fixtures/modified-block-currency-history-351/intakeFactory/openspec/specs/ideation-dashboard/spec.md)
# expect: no output

# fixture B — #329, pre-archive
git show d5f447e8:openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md \
  | diff - tests/doc-health/fixtures/modified-block-currency-history-329/driftFactory/openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md
git show d5f447e8:openspec/specs/doc-health/spec.md \
  | awk '/^### Requirement: Deterministic check families/{f=1} f&&/^### Requirement:/&&!/Deterministic check families/{exit} f' \
  | diff - <(awk '/^### Requirement: /{f=1} f' tests/doc-health/fixtures/modified-block-currency-history-329/driftFactory/openspec/specs/doc-health/spec.md)
```

If any of those four diffs is non-empty, the fixture is not the history it
claims to be and the provenance note is wrong. That is a blocking failure, not
a fixture to be adjusted until the diff is empty.

## 2. The #351 acceptance, by hand

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k "_351"
```

What must hold (audit row **A1**, § 3.1):

- one `warning`, naming `The menu offers a routing rule` AND
  `A fourth provider verb is proposed`, and naming
  `openspec/specs/ideation-dashboard/spec.md`
- one `info` for the requirement whose returned units carry the repair
  commit's clauses — the three-member port surface, "MUST NOT be added as a
  fourth provider verb", the `auto` routing rule, the broker lane, and
  `thread file`
- canon's bullet `**THEN** the selector MUST show exactly the available
  catalog entries and their data-handling badges` reported as uncarried,
  although the block's replacement contains it verbatim as a prefix
- the reverted line `**AND** every loaded editor MUST remain usable` reported
- **no assertion is on a count** (orchestrator decision 3)

## 3. The #329 acceptance, by hand

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k "_329"
```

What must hold (audit row **A2**, § 3.2):

- one `warning` naming all seven omitted titles, asserted title by title
- canon states 8 scenarios for `Deterministic check families`; the delta FILE
  carries 8; the family fires regardless — the assertion that pins the flat
  count as not what the family reads

## 4. The four gap trees

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q \
  -k "merge or redundant or companion or widened or versioned_token or body_bullet \
      or note_edited or masking_governs or rewrap or fenced or inner_backtick \
      or name_order or marker_templates"
```

**Every `-k` selector above is checked against the test names as `tasks.md`
writes them** (analyze finding F1: the first cut selected on TREE names —
`history_351`, `merge_gut` — which appear in no test name, so each command
selected zero tests and exited 5). T056 re-checks that every selector picks a
non-zero count.

| what | must hold |
| --- | --- |
| merge-and-gut (A3, § 3.3) | scenario arm quiet; ledger reports the two uncarried bullets of four |
| its companion (A3) | ledger quiet, no marker defect, and the silence shown to be caused by the marker |
| tokens (A6, § 3.5) | no unit is a backtick fragment; each body bullet is its own unit; the 3+ sentence note reports ONCE when its THIRD sentence is edited |
| rewrap (A7, § 3.6) | the family returns `[]` over the tree and is NOT skipped |
| fence (A11, § 3.7d) | a `` `` ``-fenced named unit citing `openxFactory` suppresses the WHOLE unit through the family; the single-backtick sibling suppresses nothing and is reported |
| name-order (A15, § 3.10) | the DECLARER `add-zz-first` is the later writer, so the finding lands on ITS path — a test that fails under name-ascending ordering |
| packet templates (A10, § 3.7c) | the packet's own two `- ` template bullets are NOT marker-form, read from the real file |
| containment (A5, § 3.4) | canon's unit widened BEFORE it, and at both ends, is uncarried |

## 5. Determinism over every tree

```bash
python3 -m pytest tests/doc-health -q -k "byte_for_byte"
```

Two runs per tree, `Finding.__dict__` lists compared. Covers F1's trees and
the six new ones (FR-020).

## 6. The audit is checkable, not decorative

```bash
# every F1 test name the audit cites must exist in the landed test file
grep -oE 'test_[a-z0-9_]+' specs/020-modified-block-currency-fixtures/contracts/coverage-audit.md \
  | sort -u > /tmp/cited.txt
grep -oE '^def (test_[a-z0-9_]+)' tests/doc-health/test_modified_block_currency.py \
  | sed 's/^def //' | sort -u > /tmp/present.txt
comm -23 /tmp/cited.txt /tmp/present.txt
# expect: no output — nothing cited that does not exist
```

## 7. The scope guard

```bash
git diff --stat origin/main -- scripts/ openspec/ .github/
# expect: EMPTY, unless a defect task under FR-023 exists and names the file
git diff --stat origin/main -- tests/ specs/020-modified-block-currency-fixtures/
# expect: only this feature's fixtures, its one test file, and its spec dir
```

`scripts/` moving with no defect task is the failure mode orchestrator decision
1 exists to catch: a fixture that exposed a defect and was quietly accommodated
by editing the module.

## 8. The closing gates

```bash
python3 -m pytest tests/doc-health -q | tail -3
# expect: 1077 + <tests this feature adds> passed
OPENSPEC_TELEMETRY=0 openspec validate --all --strict 2>&1 | tail -3
# expect: the same count as step 0
```
