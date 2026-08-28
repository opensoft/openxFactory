# Contract: the fifth class and its finding

Byte-level, in F4's own idiom. Everything here is asserted by a test; nothing is
a suggestion. This contract EXTENDS
`specs/022-modified-block-currency-reporting/contracts/report-section.md`, which
this feature amends at its four class-enumeration sites; where the two overlap,
the amended F4 contract is the one the report is read against.

## 1. The class-block row

Appended LAST, after `marker defects`, verbatim except the count:

```text
- unplaced-finding drift: {n} (`warning`)
```

No gloss. The row renders at a count of zero, like every other class row.
The residual bullet, unchanged, still renders only when nonzero and still sits
after all five class rows.

## 2. The rule text

Verbatim except `{n}`, `{s}` and `{rule}`:

```text
this family's own class map has no pattern for {n} finding{s} this run emitted, which share one rule shape the map has drifted behind; the first of them in this family's own report order reads, verbatim: {rule}
```

- `{n}` — the number of this run's findings carrying that shape.
- `{s}` — `""` when `{n}` is 1, otherwise `"s"`.
- `{rule}` — the rule text of the FIRST finding of that shape in the family's
  own report order, included PLAIN. `first.rule` is a suffix of the drift
  finding's rule, byte for byte.

## 3. The class-map entry

Appended LAST:

```text
<REPR>      = '(?:[^'\\]|\\.)*'  |  "(?:[^"\\]|\\.)*"      (unchanged)

unplaced    ^this family's own class map has no pattern for \d+ findings? this run emitted,<space>
```

Anchored at the start of the rule text. The anchor is load-bearing against a
corpus-supplied requirement title that embeds the phrase: unanchored, the
resulting carriage-ledger finding matches TWO patterns.

## 4. The action line

| class | `action` field, verbatim |
| --- | --- |
| unplaced-finding drift | extend the class map in `scripts/doc_health/modified_block_currency.py`, or fix the drifted rule text the finding names |

Rendered as `action="…"` in the family's ranked-plan row for this finding. The
constant interpolates no path.

## 5. Emission rules

| condition | emitted |
| --- | --- |
| the class map places every finding of the run | nothing |
| k findings share ONE unplaced shape | exactly 1 finding, `{n}` = k |
| j and k findings in TWO unplaced shapes | exactly 2 findings, `{n}` = j and k |
| the map is then extended to place them | nothing, and the residual row does not render |

Each emitted finding carries the repository and delta path of the first finding
of its shape in the family's own report order. Two runs over the same tree agree
byte for byte.

## 6. Severity and classification

- `severity` is `warning`, from `_DRIFT_SEVERITY`, a module constant distinct
  from `_LAUNCH_SEVERITY`. Under a simulated flip of `_LAUNCH_SEVERITY` to
  `error`, the scenario-title class's band moves and this one does not.
- The family stays absent from `FAMILY_RESOLUTION`, so this finding is never
  classified `contested` and its disappearance is never an uncited resolution.
- No run configured `--fail-on error` changes verdict: every finding this family
  emits is `warning` or `info`.

## 7. Invariants the fifth class must not break

- The rendered class counts, residual included, equal the rendered rows — in the
  placed state, the drifted state, and the quiet state.
- No line of the class block matches `report.PLAN_RE`; `report.parse_previous`
  reads the report with and without the summary registry identically; no line of
  the block appears in the ranked plan; the headline severity counts do not move
  because of it. The block is six lines now (lead + five class rows) plus the
  residual row when nonzero.
- `classify`, `class_counts` and `class_summary` keep their signatures and read
  the findings and nothing else.
- The module adds no public callable.
