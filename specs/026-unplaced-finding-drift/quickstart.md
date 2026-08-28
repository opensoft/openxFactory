# Quickstart — seeing the fifth class work, and seeing it not fire

Run everything from this feature's worktree
(`../openxFactory-worktrees/026-unplaced-finding-drift`), never the root
checkout.

## Prerequisites

Python 3 with `pytest`. No other dependency; the checker is stdlib-only.

## 1. The normal state — the class reads zero (this is the shipped prediction)

```bash
python3 scripts/doc-health.py --single-repo . --family modified-block-currency
```

Expected, at this feature's branch point and after it:

```text
Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 0 (`warning` — the arm carrying this family's gate)
- carriage ledger: 7 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- unplaced-finding drift: 0 (`warning`)
```

Seven `info` rows follow, and NO residual row. Zero movement in every band: the
only difference from the before run is the fifth row. Both runs are recorded in
`evidence/`.

## 2. The drifted state — inducing the condition the class exists to report

No corpus-supplied requirement title can produce an unplaced rule text while the
map is complete (measured: 20,065 constructed rule texts, 0 unplaceable), so the
honest trigger is the drift itself — one entry removed from `_CLASS_PATTERNS`,
which is precisely "the map has drifted behind the arms".

```python
import sys; sys.path.insert(0, "scripts")
from doc_health import modified_block_currency as mbc

# drop the carriage-ledger pattern: the map has now drifted behind that arm
mbc._CLASS_PATTERNS = tuple(p for p in mbc._CLASS_PATTERNS
                            if p[0] != mbc.CLASS_LEDGER)

findings = mbc.fam_modified_block_currency(ctx)     # any tree with ledger findings
drift = [f for f in findings if mbc.classify(f) == "unplaced"]
print(len(drift), drift[0].severity, drift[0].rule[:80])
print("\n".join(mbc.class_summary(findings)))
```

Expected: exactly ONE drift finding (all the induced-unplaced ledger findings
share one shape), `warning`, its rule text opening
`this family's own class map has no pattern for N findings this run emitted,`
and ending with the first ledger finding's rule text verbatim. The block shows
`unplaced-finding drift: 1` AND a residual row counting the N induced findings —
the two are counted apart, which is the point.

## 3. The tests

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_reporting.py -q
python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py -q
python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q
python3 -m pytest tests/doc-health/test_modified_block_currency.py -q
```

The full gate, which takes about half an hour:

```bash
python3 -m pytest tests/doc-health -q
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

## 4. The fixture tree

`tests/doc-health/fixtures/modified-block-currency-unplaced/` joins `ALL_TREES`
by glob and, over the UNMODIFIED map, contributes only PLACED findings — its
titles are deliberately plain so F2's unanchored `CLASSIFIERS` still partition
it. It becomes the fifth class's exercise only under the monkeypatched pass
described above, which is what drives one drift finding through the family, the
classifier, the summary and the renderer.
