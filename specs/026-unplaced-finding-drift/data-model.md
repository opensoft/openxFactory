# Data model — F5, the fifth finding class

Phase 1. Every entity below lives in
`scripts/doc_health/modified_block_currency.py`. Nothing here is a new type: the
fifth class is an instance of the existing `FindingClass`, and the drift finding
is an instance of the package's shared `Finding`.

## 1. The two new module constants

| Name | Value | FR | Why it is its own name |
|---|---|---|---|
| `_DRIFT_SEVERITY` | `WARNING` | FR-010 | The module's fourth severity constant. NOT `_LAUNCH_SEVERITY`: § 7.2 of `add-modified-block-currency-check` flips that one to `error`, and this class must not ride the flip. The module already states this reason for `_RESOLUTION_SEVERITY` and `_LEDGER_SEVERITY`. |
| `_DRIFT_ACTION` | `"extend the class map in \`scripts/doc_health/modified_block_currency.py\`, or fix the drifted rule text the finding names"` | FR-007 | A class-level constant with NO interpolated path, because `test_every_finding_carries_its_class_s_band_and_action` compares `f.action == klass.action`. The delta path is already the finding's own `path` field and is quoted inside its rule text. |

## 2. The fifth `FindingClass`

| Field | Value | FR |
|---|---|---|
| `id` | `"unplaced"` | FR-011 — must not contain `unclassified` |
| `label` | `"unplaced-finding drift"` | FR-011 — same |
| `band` | `_DRIFT_SEVERITY` | FR-010 |
| `action` | `_DRIFT_ACTION` | FR-007 |
| `gloss` | `""` (absent) | FR-012 |
| position | LAST in `CLASSES` | FR-012 |

**Why last.** `CLASSES` is ordered and the order is the contract: "the
gate-bearing arm reads FIRST". The fifth class is not an arm, so it appends. The
pin that reads the last row of the block (`marker defects` today) moves to it.

**Why no gloss.** The module's own rule, stated where the glosses are defined: a
gloss "would pad a line whose whole value is being short enough to read at a
glance". Two of five classes carry one; three do not.

**Why not `unclassified`.** `test_a_finding_the_map_cannot_place_is_counted_and_named`
asserts that substring's ABSENCE from a fully-classified summary, and a class
label renders even at a count of zero. The obvious name reddens a standing pin
for a real reason.

## 3. The class map entry

```text
unplaced   ^this family's own class map has no pattern for \d+ findings? this run emitted, 
```

Appended LAST to `_CLASS_PATTERNS`, anchored at the start of the rule text and
past the variable part, in the shape `_BLOCK_HEAD` established (FR-009).
Load-bearing against a corpus-supplied requirement title that embeds the phrase
— see `research.md` R2 for the measurement.

## 4. Rule shape — the identity two unplaced findings are grouped by

**AMENDED 2026-08-28 on Brett's ruling** ("Amend: shape = arm template, all
interpolations masked"), landed on `main` as `6d100e51` / PR #461. What is
described below is the amended rule; the superseded one — quoted spans and digit
runs masked, and nothing else — survives only as the FALLBACK in step 3.

### 4a. The arm templates

Six, registered in one place, and every arm RENDERS its rule text through its
own. That is what makes the mask derivable rather than guessed: the fixed prose
has exactly one definition, so the arm that prints it cannot drift from the mask
that reads it.

| template id | arm |
|---|---|
| `template:scenario-titles` | scenario-title completeness |
| `template:carriage-ledger` | the carriage ledger |
| `template:marker-defects` | marker defects |
| `template:title-resolution` | a block resolving to nothing |
| `template:ordering` | an undecided ordering between two writers |
| `template:unplaced-drift` | the fifth class's own finding |

### 4b. `_shape`, in three steps

```text
1. masked = mask_repr_spans(rule)
      every `repr`-emitted span -> one placeholder, LEFT TO RIGHT.
      A quote OPENS a span only at index 0 or after a NON-ALPHANUMERIC, so the
      apostrophe inside the fixed prose `sibling's` is never an opener.
2. first template whose FIXED SEGMENTS match `masked`, in registry order
      -> the shape IS that template's id
3. no template matches
      -> fall back to digits_masked(masked): the superseded lexical rule,
         kept as the FAIL-CLOSED default and nothing else
```

**The order of 1 and 2 is load-bearing.** Requirement titles and quoted body
units come from the CORPUS and may contain another arm's whole fixed prose, so
matching templates against RAW text files one arm's finding under another's —
measured, and pinned by
`test_a_title_that_embeds_another_arm_s_template_prose_matches_one_template`.

Two unplaced findings are ONE SHAPE iff their shapes are equal (FR-006), which
now means: iff they came from the same arm template. Scoped to this family by
the packet's § 4.4; nothing else may import it as a general finding-identity
rule.

## 5. The drift `Finding`

| Field | Value | FR |
|---|---|---|
| `severity` | `_DRIFT_SEVERITY` (`warning`) | FR-010 |
| `family` | `FAMILY` (`modified-block-currency`) | FR-018 — no new family |
| `repo` | the repo of the FIRST finding of that shape in report order | FR-004 |
| `path` | the delta path of that same first finding | FR-004 |
| `rule` | the template below | FR-001, FR-002, FR-003 |
| `action` | `_DRIFT_ACTION` | FR-007 |

**Rule template:**

```text
this family's own class map has no pattern for {n} finding{s} this run emitted, which share one rule shape the map has drifted behind; the first of them in this family's own report order reads, verbatim: {rule}
```

- `{n}` — how many of this run's findings carry that shape (FR-002).
- `{s}` — `""` when `n == 1`, `"s"` otherwise. The pattern admits both.
- `{rule}` — the first instance's rule text, PLAIN and unescaped, so `verbatim`
  is literally true (FR-003; research R1b).

**Identity** is `(family, repo, path of the first instance of that shape)`,
which is deterministic. Because the band is `warning`, that identity never
reaches `regressions()`, which matches `critical` and `error` only — so no issue
is opened and no per-run identity churn can create one (packet D3).

## 6. Cardinality — the state table

| Run state | drift findings emitted | `unplaced` count | residual count |
|---|---|---|---|
| every finding placed (the normal state, and this tree's) | 0 | 0 | 0 (row absent) |
| one unplaced shape, k findings | 1 | 1 | k |
| two unplaced shapes, j and k findings | 2 | 2 | j + k |
| no findings at all | 0 | 0 | 0 (row absent) |
| family skipped | — | no block renders | — |

In every row the class counts plus the residual sum exactly to the rows the
report prints (FR-016).

## 7. What does NOT change

`classify`, `class_counts` and `class_summary` keep their signatures and their
no-context discipline (FR-014). `_UNCLASSIFIED_LINE` and its render condition
are untouched (FR-013). `Finding` gains no field; `report.render`, the ranked
plan and the finding grammars are untouched; `FAMILY_SUMMARIES` and
`FAMILY_RESOLUTION` are untouched (FR-015, FR-024). The module's public-callable
surface is unchanged — the fifth class is a `FindingClass` instance and both new
constants are private (FR-022).
