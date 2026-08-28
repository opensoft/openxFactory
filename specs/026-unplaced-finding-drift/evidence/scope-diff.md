# Scope diff — nothing outside the named surface moved (T044, packet § 2.15)

Merge base: `22f15cdf341cac0ec89ed7e4e56f75ecaebc8585` (after the catch-up
merge; the original branch point was `86b7ca3f`, the packet's own merge commit,
and the diff below is unchanged by the merge).

## The forbidden surfaces are EMPTY

```bash
$ git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/
$
```

No workflow file, and no `openspec/` edit of any kind. **The packet's own
`tasks.md` boxes are deliberately NOT ticked here**: the archive act is a
separate later commit that follows the merge, per packet § 5.1 and the precedent
of `add-modified-block-currency-check` and `add-promotion-fidelity-check`.

## The permitted surface, and only it

**RE-RUN after every round, and the numbers below are the last re-run's.** The first recording of this file quoted a 492-line reporting-test
diff that later grew to 498 without the file being re-run — a stale figure in an
evidence file, which is the same defect class this family exists to catch, so
the command is re-run and its output pasted rather than edited.

```bash
$ git diff --cached --stat $(git merge-base HEAD origin/main) -- scripts/ tests/ \
      specs/022-modified-block-currency-reporting/contracts/
 scripts/doc_health/modified_block_currency.py      | 414 +++++++++-
 .../contracts/report-section.md                    | 125 ++-
 .../modified-block-currency-unplaced/README.md     |  97 +++
 .../openspec/changes/add-a-drift-case/proposal.md  |   3 +
 .../add-a-drift-case/specs/drift-cases/spec.md     |  15 +
 .../openspec/changes/add-drift-cases/proposal.md   |   3 +
 .../add-drift-cases/specs/drift-cases/spec.md      |  37 +
 .../openspec/specs/drift-cases/spec.md             |  61 ++
 tests/doc-health/test_modified_block_currency.py   |  65 +-
 .../test_modified_block_currency_fixtures.py       |  85 +-
 .../test_modified_block_currency_reporting.py      | 884 ++++++++++++++++++++-
 .../test_modified_block_currency_self_gate.py      |  41 +-
 12 files changed, 1744 insertions(+), 86 deletions(-)
```

RE-RUN AGAIN after Brett's shape amendment (2026-08-28); the module grew by the
arm-template registry and the five arms' rule construction moved into it.

Six of those twelve are the new fixture tree (`--diff-filter=A` over `tests/`
names exactly those six and nothing else). The other six are the module, the F4
contract, and the four `test_modified_block_currency*.py` files. Plus
`specs/026-unplaced-finding-drift/` — this feature's own Speckit artifacts.

**The fixture tree carries TWO change directories.** `add-a-drift-case/` exists
so the tree's emission order disagrees with the family's report order; without
that disagreement the "first instance in report order" pin cannot fail, and the
mutation round proved it by surviving the single-directory version.

**FOUR test files, not three.** The packet's § 2.15 says "the three
`tests/doc-health/test_modified_block_currency*.py` files". There are four, and
the packet already names all four between its own § 2.6–§ 2.12:
`test_modified_block_currency.py` is named by § 2.12 for its `:16` numeral, and
it is also where the simulated-flip pin § 2.14(e) asks for belongs, beside the
family's other severity pins. Recorded as a mechanical inaccuracy in the packet
rather than a scope change (plan § O7).

## What did NOT move, checked by name

- `scripts/doc_health/families.py` — `FAMILIES`, `FAMILY_SUMMARIES`,
  `FAMILY_NOTES` and `FAMILY_RESOLUTION` are untouched. No new family, no new
  registry entry: the fifth class is a value inside the family that already
  exists.
- `scripts/doc_health/report.py` — the renderer, `PLAN_RE`, `parse_previous`,
  `plan_line`, `regressions`, `uncited_resolutions`: untouched.
- `scripts/doc_health/__init__.py` — `Finding` gains no field; the severity
  constants and `SEVERITY_RANK` are untouched.
- Every other family module: untouched.
- FR-018's own pin, which is what proves no deterministic check family was
  added: `test_modified_block_currency.py::test_the_reporting_list_mirrors_the_registry`
  still reads `len(FAMILY_IDS) == len(FAMILIES) == 22`, UNCHANGED and passing.

## Public surface unchanged

Every name this feature adds to the module is private —
`_DRIFT_SEVERITY`, `_DRIFT_ACTION`, `_DRIFT_RULE`, `_SHAPE_QUOTED`,
`_SHAPE_DIGITS`, `_shape`, `_drift_findings`, `_report_order` — plus the public
class-id constant `CLASS_DRIFT`, which is a string and not a callable. The
FR-023 public-callable snapshot in
`test_modified_block_currency_fixtures.py::test_this_feature_touches_no_production_module`
is therefore UNCHANGED, and that is asserted rather than edited (packet § 2.11).
