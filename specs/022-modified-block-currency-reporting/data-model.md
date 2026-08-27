# Data model: F4 reporting and workflow

No persisted data, no schema, no new artifact on disk. F4's entities are a
CLASSIFICATION over findings that already exist and a RENDERING of it. This file
names them, their fields, and the rules that hold over them.

## 1. FindingClass — the family's four, closed

The family's own module docstring already declares the set: "THREE ARMS, FOUR
FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE". F4 makes it a value.

| id | label rendered | band | producer | action carried |
| --- | --- | --- | --- | --- |
| `scenario-titles` | `scenario-title completeness` | `warning` (`_LAUNCH_SEVERITY`) | `_arm_titles` | `_ACTION` |
| `carriage-ledger` | `carriage ledger` | `info` (`_LEDGER_SEVERITY`) | `_arm_ledger` | `_ACTION` |
| `title-resolution` | `title resolution and ordering` | `warning` (`_RESOLUTION_SEVERITY`) | `_unresolved_finding`, `_arm_ordering` | `_ACTION` |
| `marker-defects` | `marker defects` | `info` (`_LEDGER_SEVERITY`) | `_arm_marker_defects` | `_MARKER_ACTION` |

**CLOSED SET (constitution VII, fail-closed registries).** A finding that matches
no class is not silently absorbed into a neighbouring one: it is counted in the
residual below.

**Two producers, one class**, for `title-resolution`: a block resolving to
nothing and an ordering no declaration settles are the two shapes of the delta's
third arm ("Title resolution and ordering"), they share a severity and an action,
and the delta names them as one arm. Splitting them in the report would claim a
fifth class the delta does not define.

**The band is a property of the class, not of the finding.** It is rendered from
the class table rather than read off the findings, so a subtotal line stating
`(warning)` beside a class whose findings had somehow become `info` would be
caught by the invariant below rather than papered over.

## 2. ClassTally — the counted result

Fields:

- `counts: {class id -> int}` — every class present, including zeros.
- `residual: int` — findings of this family that matched no class.
- `total: int` — `sum(counts.values()) + residual`.

Invariants, each asserted:

- **I1**: `total == len(the family's findings in this report)`. The tally can
  never omit a row.
- **I2**: every finding matches AT MOST one class (the repr anchor of research
  R2 is what makes this hold over corpus-supplied titles).
- **I3**: over the F2 fixture corpus and over this repository's real tree,
  `residual == 0`.
- **I4**: for every class, every finding in it carries that class's band and that
  class's action. This is what ties the rendered `(warning)` / `(info)` label to
  the rows.

## 3. The rendered subtotal block

See `contracts/report-section.md` for the byte-level grammar. Structurally:

```text
### modified-block-currency
                                      <- blank line (pre-existing)
<lead line>
- <label>: <count> (<band>[ — <gloss>])   x4, in the table's order
[- unclassified: <n> — <explanation>]     only when residual > 0
                                      <- blank line (pre-existing note idiom)
- [warning] repo:path — rule …            <- the findings, unchanged
```

State rules:

- **S1**: rendered when the family RAN, whether or not it found anything.
- **S2**: NOT rendered when the family is skipped — by run configuration or by
  its own scope guard. Both land in `skips`; one guard covers both.
- **S3**: never rendered for a family with no registry entry, which is every
  other family. That is the byte-identity guarantee, and it is structural: the
  lines come from a registry lookup that returns nothing.

## 4. The family-summary registry

`families.FAMILY_SUMMARIES: {family id -> callable}` where the callable takes the
list of THAT family's findings, in report order, and returns note lines.

- One entry today, and the reason is the same shape as `FAMILY_NOTES`' one entry:
  this is the only family whose findings a reader must split by class to read the
  section at all, because it is the only family whose gate-bearing arm shares a
  section with a standing editorial population.
- `FAMILY_NOTES` stays as it is: `(ctx) -> lines`, a fact about the RUN.
  `FAMILY_SUMMARIES` is `(findings) -> lines`, a fact about the FINDINGS. Two
  signatures because they answer two questions; see research R1.

## 5. The action lines

Not new entities — F1's constants, pinned here.

| constant | text | carried by |
| --- | --- | --- |
| `_ACTION` | restate the requirement as canon currently states it, or declare the deletion with a `` `Removed from canon by` `` marker | the three arms |
| `_MARKER_ACTION` | name a unit the block does not restate, or drop the declaration — a marker that does not describe the block declares nothing | the marker-defect class |

Rendered by `report.plan_line` into `## Ranked Plan` as `action="…"`. There is no
per-family action registry in this suite; a family's action lives at its own
finding construction (research R7).

## 6. What F4 does NOT model

- No change to `Finding` (fields, sort key, or match key).
- No change to `RunResult` fields.
- No change to any severity, band, or resolution class.
- No new file, no new report section, no new CLI option, no new workflow input.
