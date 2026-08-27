# Contract: the family's report section, and the registry that fills it

Byte-level. Everything here is asserted by a test; nothing is a suggestion.

## 1. The rendered subtotal block

Rendered under `### modified-block-currency`, after any `FAMILY_NOTES` lines,
before the first finding row, followed by one blank line (the existing note
idiom in `report.render`).

**Lead line, verbatim:**

```text
Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
```

**One bullet per class, in this order, verbatim except the counts:**

```text
- scenario-title completeness: {n} (`warning` — the arm carrying this family's gate)
- carriage ledger: {n} (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: {n} (`warning`)
- marker defects: {n} (`info`)
```

**The residual bullet, rendered ONLY when its count is nonzero, verbatim except
the count:**

```text
- unclassified: {n} — findings this family emitted that its own class map does not place; the map has drifted from the arms and the counts above are short by this many
```

### Worked example — this checkout at F4's branch point

```text
### modified-block-currency

Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 1 (`warning` — the arm carrying this family's gate)
- carriage ledger: 8 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)

- [warning] openxFactory:openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' omits 1 of the 2 scenarios …
- [info] openxFactory:openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' does not carry 2 of the 6 body units …
…
```

## 2. State rules

| state | subtotal block | rest of section |
| --- | --- | --- |
| family ran, findings present | rendered | the rows, unchanged |
| family ran, no findings | rendered, all counts `0` | `No findings.`, unchanged |
| skipped by `--skip-family` | **NOT rendered** | `Skipped: skipped by run configuration` |
| skipped by the family's own scope guard | **NOT rendered** | the family's own scope reason |
| any other family, any state | **NOT rendered** | byte-identical to today |

## 3. Not a finding

- No subtotal line matches `report.PLAN_RE`, so `report.parse_previous` cannot
  read one back as a ranked-plan item, cannot enter `previous_keys`, and cannot
  reach `regressions()` or `uncited_resolutions()`.
- No subtotal line appears in `## Ranked Plan`.
- No `## Headline` severity count moves because of it.
- Nothing in it reaches `--new-findings-out`.

## 4. The registry

```python
# families.py
FAMILY_SUMMARIES = {
    "modified-block-currency": modified_block_currency.class_summary,
}
```

**Signature:** `class_summary(findings: list[Finding]) -> list[str]`.

- Input: exactly the findings the report is rendering for that family, in report
  order.
- No `ctx`, no filesystem read, no corpus read, no second run of the family.
- Output: the lines of section 1 — never empty for a family with an entry that
  ran.

**Render contract (`report.render`), additive:**

```text
notes  = list(family_notes.get(family, ()))
notes += FAMILY_SUMMARIES[family](fam_findings)   if family in FAMILY_SUMMARIES
                                                 and the family was not skipped
render notes, then one blank line, ONLY if notes is non-empty
```

The last clause is the byte-identity guarantee: for a family with neither notes
nor a summary, `notes` is empty and not one character is emitted — the same
condition the current code already applies to `family_notes`.

## 5. The class map

```text
<REPR>      = '(?:[^'\\]|\\.)*'  |  "(?:[^"\\]|\\.)*"
<TITLED>    = ^active MODIFIED block for <REPR><space>

scenario-titles   <TITLED>omits \d+ of the \d+ scenarios<space>
carriage-ledger   <TITLED>does not carry \d+ of the \d+ body units and scenario bullets<space>
marker-defects    <TITLED>carries a '\w+' marker by<space>
title-resolution  <TITLED>resolves to no promoted requirement,<space>
title-resolution  ^the ordering of MODIFIED blocks for <REPR> is undecided:<space>
```

Every pattern is anchored at the start of the rule and past the closing quote of
the requirement title's `repr`, so a corpus-supplied title containing another
class's phrase cannot misfile the finding (research R2; measured against a
constructed case and against the real nine).

## 6. The action lines, pinned not added

| class | `action` field, verbatim |
| --- | --- |
| scenario-title completeness | restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker |
| carriage ledger | same |
| title resolution and ordering | same |
| marker defects | name a unit the block does not restate, or drop the declaration — a marker that does not describe the block declares nothing |

Rendered as `action="…"` in every one of the family's ranked-plan rows.
