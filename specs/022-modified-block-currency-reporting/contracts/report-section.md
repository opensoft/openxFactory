# Contract: the family's report section, and the registry that fills it

Byte-level. Everything here is asserted by a test; nothing is a suggestion.

**AMENDED 2026-08-28 by `add-unclassified-finding-class`, realized as Speckit
feature `026-unplaced-finding-drift`.** That change adds a FIFTH finding class,
`unplaced-finding drift`, and this contract enumerated the four classes FOUR
TIMES OVER — the per-class bullets, the worked example, the class map and the
action-line table. A fifth class landing without this amendment would leave the
corpus carrying a byte-level contract that is FALSE about the code it describes,
which is the class of defect the family this contract describes exists to catch.
All four enumerations below carry the fifth class; the residual bullet is
unchanged.

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
- unplaced-finding drift: {n} (`warning`)
```

The fifth bullet is LAST and carries NO gloss: the ordering comment's contract
is "the gate-bearing arm reads FIRST", which appending leaves untouched, and two
of the five classes carry a gloss where three do not.

**The residual bullet, rendered ONLY when its count is nonzero, verbatim except
the count:**

```text
- unclassified: {n} — findings this family emitted that its own class map does not place; the map has drifted from the arms and the counts above are short by this many
```

### Worked example — this checkout at F5's merge base (`22f15cdf`)

Measured with
`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`.

```text
### modified-block-currency

Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 0 (`warning` — the arm carrying this family's gate)
- carriage ledger: 7 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- unplaced-finding drift: 0 (`warning`)

- [info] openxFactory:openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' does not carry 2 of the 6 body units …
…
```

**The scenario-title row read `1` and the ledger row `8` at F4's own branch
point**, against `add-composed-view-authoring` / "Composed views are read-only
with a repository jump". PR #444 declared that rename with a `Merged into`
marker and the arm's standing population reached zero; the ledger's moved from 8
to 7 as packets archived. Both are the arms working, and neither is anything to
do with the fifth class, whose row has read `0` at every measurement.

### Worked example — the fifth class firing

The class reads `0` wherever the map is complete, so the only way to see it is
the drift itself — one entry removed from `_CLASS_PATTERNS`, which is the live
condition it reports. Over
`tests/doc-health/fixtures/modified-block-currency-unplaced/` with the
`carriage-ledger` pattern removed:

```text
Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 1 (`warning` — the arm carrying this family's gate)
- carriage ledger: 0 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- unplaced-finding drift: 1 (`warning`)
- unclassified: 3 — findings this family emitted that its own class map does not place; the map has drifted from the arms and the counts above are short by this many
```

Five class rows plus the residual, summing to the five rows printed beneath —
the three ledger findings the map no longer places, the titles finding it still
does, and the one drift `warning` naming them. **The residual row and the drift
finding are counted APART**: the row counts the arms' unplaced findings, the
class counts the finding that reports them, and the two are two readings of one
fact rather than alternatives.

**THE GRAIN: ONE FINDING PER ARM TEMPLATE, WHICH IS ONE PER REMEDY.** Two rule
texts are one shape where they come from the same template, whatever their
interpolated values — the requirement title, the counts, the promoted spec's
path, the unit-kind list, a change-id list, an unresolved block's `why` clause.
One template is one entry somebody adds to the class map. Amended 2026-08-28 on
Brett's ruling; the rule as first ratified masked quoted spans and digit runs
only, and the same dropped map entry on the openxFactory tree then yielded SIX
findings for seven unplaced ones where it now yields ONE.

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
- No subtotal line appears in `## Ranked Plan`. **The drift finding is not part
  of the block**: it is an ordinary `Finding`, so it DOES appear there, on the
  same terms as every other row. The block and the finding are separate objects
  and this bullet is about the block.
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
unplaced          ^this family's own class map has no pattern for \d+ findings? this run emitted,<space>
```

Every pattern is anchored at the start of the rule and past the closing quote of
the requirement title's `repr`, so a corpus-supplied title containing another
class's phrase cannot misfile the finding (research R2; measured against a
constructed case and against the real nine).

The fifth entry is anchored for BOTH directions of that hazard, and both are
measured. Its finding QUOTES a rule text the map could not place, and that
quotation may itself begin in the shape of an arm's — so an unanchored probe
would file the drift finding under whichever class its quotation resembles. And
a requirement may be TITLED with the fifth class's own opening phrase, in which
case its ledger finding's rule text contains that phrase and a `.*`-prefixed
probe matches BOTH — two patterns on one rule, which reds the partition pin.

### 5b. The arm templates, and the shape mask derived from them

The class map above decides which CLASS a finding is. A second, separate
registry decides which SHAPE it is — that is, which findings the fifth class
groups together. They are not the same question and not the same table: a class
is a band and an action, a shape is a remedy.

```text
template:scenario-titles   active MODIFIED block for {title!r} omits {missing} of the {total} scenarios {spec_rel} currently states for it: {named}
template:carriage-ledger   active MODIFIED block for {title!r} does not carry {missing} of the {total} body units and scenario bullets {spec_rel} currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: {listed}
template:marker-defects    active MODIFIED block for {title!r} carries a {form!r} marker by {change_id} ({date}) naming {named}, which the block still restates — a declaration that does not describe the block
template:title-resolution  active MODIFIED block for {title!r} resolves to no promoted requirement, no rename of its own, and no active sibling's addition: {why}
template:ordering          the ordering of MODIFIED blocks for {title!r} is undecided: {names} — {why}; each block is meanwhile measured against canon, the only basis a reader can name
template:unplaced-drift    this family's own class map has no pattern for {n} finding{s} this run emitted, which share one rule shape the map has drifted behind; the first of them in this family's own report order reads, verbatim: {rule}
```

**Every arm RENDERS through its template**, so the fixed prose has exactly one
definition and no arm can emit a rule text the mask cannot read.

**`_shape` is two steps and the order is load-bearing:**

```text
1. mask every `repr`-emitted span, left to right — a quote opens a span only at
   the start of the text or after a NON-ALPHANUMERIC, so the apostrophe inside
   the fixed prose `sibling's` is never an opener and a corpus-supplied title
   can never carry another arm's phrase into step 2
2. first template whose fixed segments match the masked text, in order
   -> the shape IS that template's id
3. no template matches -> fall back to the lexical mask (quoted spans + digit
   runs), fail-closed: an unrecognized text is never merged into a template
```

The six templates are mutually exclusive over masked text, asserted at template
level over every fixture tree and the real corpus rather than through `_shape`'s
single return — a class-level comparison can never exceed one hit however many
templates match.

## 6. The action lines, pinned not added

| class | `action` field, verbatim |
| --- | --- |
| scenario-title completeness | restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker |
| carriage ledger | same |
| title resolution and ordering | same |
| marker defects | name a unit the block does not restate, or drop the declaration — a marker that does not describe the block declares nothing |
| unplaced-finding drift | extend the class map in `scripts/doc_health/modified_block_currency.py`, or fix the drifted rule text the finding names |

Rendered as `action="…"` in every one of the family's ranked-plan rows.

The fifth action names BOTH remedies and interpolates NO path of its own: the
delta path is already the finding's own `path` field, the drifted rule text is
quoted in the finding itself, and
`test_every_finding_carries_its_class_s_band_and_action` compares each finding's
action with its CLASS's constant — which a per-finding path would break.
