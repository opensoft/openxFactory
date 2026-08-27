# Fixture: a named unit that contains backticks, fenced two ways

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-modified-block-currency-check` § 3.7(d), audit row **A11**.

> **Every unit a marker names, and the `Merged into` destination, SHALL be
> written as a CommonMark code span, and a unit that itself contains backticks
> SHALL be fenced with a longer run of them.** … a single-backtick span around
> such a unit ends at its first inner backtick and names a fragment, so the
> marker would name something that is not a unit at all.
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## Why not a reconstruction

No committed marker in this corpus has been mis-fenced, because the marker form
is new with this very change. F1 pins the rule at `extract_code_spans` — the
right unit test — but no fixture exercised it THROUGH the family and none showed
it SUPPRESSING anything.

## What the family reports here

Two requirements, one clause, two fences — and the pair is what makes the rule
falsifiable:

- **`A longer fence names the whole unit`** — the dropped clause (which cites
  `openxFactory`) is named inside a **double-backtick** fence. It suppresses the
  whole unit: **nothing is reported**.
- **`A single backtick names a fragment`** — the SAME clause named with a
  **single-backtick** span, which under CommonMark ends at the clause's first
  inner backtick. The marker therefore names `An adapter that reaches a hosted
  provider SHALL obtain its credential through the`, which matches no canon unit
  at all, so it suppresses nothing and **the clause is reported**.

The second requirement emits **no marker defect**, and that is correct rather
than an oversight: the delta reports a marker only where it names a unit the
block STILL CARRIES. A name matching no canon unit declares nothing and is
silent — the three-way resolution in `suppression()`.

Without the single-backtick sibling, a build that ignored fences entirely and
matched the whole paragraph would pass the first case.

Tests: `test_a_longer_fenced_named_unit_suppresses_the_whole_unit`,
`test_the_inner_backtick_does_not_truncate_the_named_unit`.
