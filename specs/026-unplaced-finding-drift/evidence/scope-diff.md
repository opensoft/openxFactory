# Scope diff — nothing outside the named surface moved (T044, packet § 2.15)

Merge base: `86b7ca3f4600f5771c48b2baeb2adf85f556fb82`.

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

```bash
$ git diff --stat $(git merge-base HEAD origin/main) -- scripts/ tests/ \
      specs/022-modified-block-currency-reporting/contracts/
 scripts/doc_health/modified_block_currency.py      | 203 ++++++++-
 .../contracts/report-section.md                    |  79 +++-
 tests/doc-health/test_modified_block_currency.py   |  65 ++-
 .../test_modified_block_currency_fixtures.py       |  18 +-
 .../test_modified_block_currency_reporting.py      | 492 +++++++++++++++++++--
 .../test_modified_block_currency_self_gate.py      |  41 +-
 6 files changed, 837 insertions(+), 61 deletions(-)
```

Plus two additions, untracked at the time of this measurement:

- `tests/doc-health/fixtures/modified-block-currency-unplaced/` — the new
  behavioural tree (4 files)
- `specs/026-unplaced-finding-drift/` — this feature's own Speckit artifacts

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
