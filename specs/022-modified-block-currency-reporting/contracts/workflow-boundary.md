# Contract: the workflow boundary (packet section 5.3)

**NO WORKFLOW CHANGE.** `.github/workflows/doc-health-reusable.yml` is read by a
test and edited by nothing. The mechanical proof is
`git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/`
returning empty.

## What the pin asserts

| # | assertion | why it is not vacuous |
| --- | --- | --- |
| W1 | the workflow parses to a non-empty `jobs` map | a pin over an unparsed or empty file asserts nothing |
| W2 | `--promotion-fidelity-basis live-main` IS present in exactly one step's `run` | proves the file demonstrably carries per-family options, so W3's absence is measured against a real population of one |
| W3 | no step's `run` names this family, in either spelling (`modified-block-currency`, `modified_block_currency`) | W2 |
| W4 | no step's `env` value and no step's `with` value names this family, either spelling | the untrusted-input idiom in this workflow passes values through `env:`, so a `run`-only pin would miss the shape the workflow actually uses |
| W5 | the checker's own option surface names no option after this family | W6 |
| W6 | `--family modified-block-currency` and `--skip-family modified-block-currency` are accepted | a generic option taking every family's id is not a per-family option; without W6 the pin would be satisfied by a family nothing can run |

## What it deliberately does NOT re-assert

Cited by name in the test, not duplicated:

- `test_modified_block_currency.py::test_the_promoted_reader_cannot_reach_a_measurement_basis`
  (F1) — the family's readers take a root and a capability; there is no parameter
  a basis could arrive through, and the module names no git-ref reader.
- `test_modified_block_currency.py::test_the_advisory_launch_is_pinned_in_both_halves`
  (F1) — the severities and the `FAMILY_RESOLUTION` absence.
- `test_workflow_contract.py::test_only_the_reporting_run_declares_the_live_main_basis`
  — that the ONE per-family option belongs to the reporting run only. That pin is
  written in `promotion-fidelity`'s shape and is that family's; section 5.3 asks
  for a new assertion of THIS family's own, which W3–W6 are.

## The mutation that must red it

A scratch copy of the workflow (never the tracked file) with
`--modified-block-currency-basis live-main` added to the
`Run doc-health suite` step's `run`. W3 must fail against it. Recorded in
`../evidence/f4-gates.md`.
