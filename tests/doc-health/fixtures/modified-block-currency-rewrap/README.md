# Fixture: a scenario-complete block that re-wraps everything it carries

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-modified-block-currency-check` § 3.6, audit row **A7**.

> Normalization collapses runs of whitespace to a single space and strips
> leading and trailing whitespace, so a re-wrapped paragraph compares equal to
> the same paragraph wrapped differently; no normalization beyond it applies.
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## Why not a reconstruction

There is no historical instance because this is the NEGATIVE case — a block
doing the right thing. PR #358's manual verification of #351 worked only because
that repair copied canon verbatim, preserving its wrapping, and a rule that
works only when the author preserved wrapping is not a rule.

F1 asserts this at `mbc.carried()`, on units its own test body synthesizes from
canon, and its `-quiet` tree carries **no MODIFIED block at all** — so a wiring
regression between `derive_units` and the arms leaves both F1 tests green. This
tree closes that: a real MODIFIED block, run through the family.

## What the family reports here

**Nothing.** The block restates its requirement completely — every paragraph,
body bullet, dated note, scenario title and scenario bullet — while re-wrapping
each at a different column width, one paragraph mid-sentence and one bullet
after its `**THEN**`.

And it is **not SKIPPED**: the tree has an `openspec/changes/` directory and one
MODIFIED block whose units were derived. The two silences are different states,
and canon's skip rule is "cannot run", not "found nothing".

Tests: `test_a_rewrapped_scenario_complete_block_reports_nothing_through_the_family`,
`test_the_rewrap_tree_is_not_reported_skipped`.
