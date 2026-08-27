# Research: modified-block currency — reporting and workflow (F4)

Phase 0 of `specs/022-modified-block-currency-reporting`. Every decision below
was **measured against the tree at this branch point** (`f728d57f` + this
worktree), not inferred from the packet. Where a decision is reversible it is
flagged for veto and says what reverting costs.

## The measurements this feature starts from

Taken before any decision, so the decisions answer facts rather than
predictions.

| measurement | value | command |
| --- | --- | --- |
| `tests/doc-health` at the branch point | **1178 passed** (192.9s) | `python3 -m pytest tests/doc-health -q` |
| the family over this checkout | **1 `warning`, 8 `info`** (9 findings, 22 blocks) | `fam_modified_block_currency` through F3's two-attribute stand-in |
| classes populated | scenario-title 1, ledger 8, resolution 0, marker 0 | the class map below, over those 9 |
| this family in `.github/` | **0 mentions**, either spelling | `grep -rn "modified.block.currency\|modified_block_currency" .github/` |
| per-family options in the workflow | **exactly one**: `--promotion-fidelity-basis live-main` | `grep -n "doc-health.py" -A 12 .github/workflows/doc-health-reusable.yml` |

## R1 — THE MECHANISM: a per-family SUMMARY registry, rendered in the notes position

**DECISION (the brief's candidate (a); FLAGGED FOR VETO).** The subtotal reaches
the report through a new registry `families.FAMILY_SUMMARIES`, keyed by family id
exactly like the existing `FAMILY_NOTES`, whose value is
`(that family's findings) -> [note lines]`. `report.render` renders its lines in
the same position `FAMILY_NOTES` already renders in — under the family's own
heading, before its finding rows.

**Why a sibling registry rather than `FAMILY_NOTES` itself.** `FAMILY_NOTES` is
`(ctx) -> lines` and is called by `runner.run_suite` BESIDE the family call, with
a comment explaining that a note describes "the run a family ACTUALLY performed".
A subtotal is not that: it is a function of the findings and of nothing else.
Widening `FAMILY_NOTES`' signature to `(ctx, findings)` would change
`promotion_fidelity.basis_notes`' contract for no gain and would put a
findings-derived line behind a ctx-derived channel. Two registries, two honest
signatures, one shared render position.

**Why `report.render` and not `runner.run_suite`.** Both places have what is
needed, and the render side is better on three counts:

1. **Correct dependency.** The subtotal is derived purely from the findings the
   renderer is about to print. Computing it where they are printed removes the
   possibility of the tally and the rows disagreeing.
2. **Testable without a subprocess.** `report.render(...)` is callable in-process
   (the precedent is `test_promotion_fidelity.py::test_the_report_states_the_basis_under_the_family_heading`).
   The skip cases, the zero case and the byte-identity proof are all reachable
   without spawning a checker run.
3. **In stated scope.** The brief scopes F4 to `report.py` (additive only) and
   the `families.py` / `__init__.py` registries. `runner.py` is not in it.

**Why not candidate (b), arm-prefixed rule text.** Rejected on three grounds.
It changes rule text, which F3's self-gate pins by subject and F1's plan
forbade; it changes every ranked-plan row, so the report diff would move far
outside the family's own lines; and it does not actually satisfy § 5.1 — a
reader would still have to read nine long rows and tally the prefixes. § 5.1
asks for the split to be visible "without counting".

**Cost of a veto.** The registry is four lines in `families.py`, a five-line
additive branch in `report.render`, and one function in
`modified_block_currency.py`. Reverting is a clean deletion; no other family and
no finding is touched.

## R2 — THE CLASS MAP: repr-anchored rule-text patterns, with a fail-loud residual

**DECISION.** A finding's class is derived from its `rule` text by an ordered
tuple of patterns anchored on the rule's OPENING PHRASE and on the closing quote
of the requirement title's `repr`:

```text
<REPR>  = '(?:[^'\]|\.)*'  |  "(?:[^"\]|\.)*"
titles      ^active MODIFIED block for <REPR> omits \d+ of the \d+ scenarios
ledger      ^active MODIFIED block for <REPR> does not carry \d+ of the \d+ body units and scenario bullets
marker      ^active MODIFIED block for <REPR> carries a '\w+' marker by
resolution  ^active MODIFIED block for <REPR> resolves to no promoted requirement,
resolution  ^the ordering of MODIFIED blocks for <REPR> is undecided:
```

**Why the repr anchor is not decoration.** Requirement titles come from the
corpus, so a title may contain any phrase — including another class's. Measured:
a LEDGER finding whose block title is
`'X omits 1 of the 2 scenarios Y'` matches an unanchored titles pattern AND the
ledger pattern, and a first-match-wins classifier misfiles it. With the anchor it
matches the ledger pattern only. Verified against the real nine (each matched
exactly one class) and against that constructed case.

**Why not a new field on `Finding`.** `Finding` is shared by twenty-two families
and the semantic lanes; a field added for one family's report line is a change to
a shared grammar for a local need, and the brief forbids changing the finding
grammar.

**Why not have the arms tag their own output.** They cannot: `fam_*(ctx)` returns
a flat `list[Finding]` and the runner sorts it into a report-wide list. A tag
would have to ride on the `Finding`, which is R2's rejected option.

**Why a rule-text read is nonetheless safe here.** Because the drift it could
suffer is made LOUD in two independent ways: (1) every finding must classify into
exactly one class, asserted over the F2 fixture corpus and over the real tree,
so a rule-text edit that escapes the map reds a test; and (2) an unclassified
finding is counted in a named residual line that renders whenever it is nonzero,
so even an unasserted path cannot quietly shrink a class.

## R3 — POSITION: before the rows, after a basis note if a family ever has both

**DECISION.** Subtotal lines render after any `FAMILY_NOTES` lines and before the
findings, in one block, followed by one blank line. No family has both today; the
order is fixed anyway so that adding one later is not a layout decision taken
under time pressure. Rationale is the same as the notes precedent's: a line a
reader meets AFTER the rows is a line they have already done without.

## R4 — A SKIP CARRIES NO SUBTOTAL, and this deliberately differs from a basis note

**DECISION.** Neither skip shape — `--skip-family`, or the family's own
`Skip(FAMILY, "no repository in scope carries an `openspec/changes/`
directory…")` — renders a subtotal.

**Why this is the opposite call from `FAMILY_NOTES`.** A basis note answers
"which tree WOULD this family have measured", which is true of a skipped run and
is exactly why `test_the_report_states_the_basis_on_a_family_with_no_findings`
asserts a note beside a `Skipped:` line. A subtotal answers "how many findings
did each class produce", and on a skip the answer is not zero — it is *not
measured*. Rendering `0 · 0 · 0 · 0` there would state a measurement nobody
took, which is precisely the failure canon's skip rule exists to prevent
("cannot run", not "found nothing"). Implementation consequence: the guard is
`if not skipped`, which covers both shapes because both land in `skips`.

## R5 — A SINGLE-FAMILY RUN OF ANOTHER FAMILY: parity with `No findings.`, and canon already discloses it

**KNOWN WART, ACCEPTED, RECORDED.** In a `--family promotion-fidelity` run this
family never executes, yet `report.render` walks all of `FAMILY_IDS` and prints
`### modified-block-currency` / `No findings.` — pre-existing behaviour for all
twenty-one other families. The subtotal inherits it and would read all zeros.

**Why it is not fixed here.** Fixing it needs the runner to record WHICH families
ran and thread that into `render`, which is a change to a shared reader for a
condition canon already handles: the "Health report contract" requires a run with
non-default scope to state the deviation, and it does — `- scope limited to
family promotion-fidelity` renders in the headline block above. A reader who has
been told the scope is one family does not read another family's section as a
measurement. Making the subtotal stronger than `No findings.` on this point
would be inventing a guarantee the report does not otherwise offer.

## R6 — THE RESIDUAL CLASS

**DECISION.** A fifth line, rendered ONLY when nonzero, naming the count and
saying what it means: findings the family emitted that its own class map does not
place. The counts therefore always sum to the rows.

**Why not silence.** A tally that can silently omit rows is worse than no tally:
a reader who trusts `1 / 8 / 0 / 0` on a report where two rows went uncounted has
been told something false by a line whose whole purpose is to be trusted without
counting.

**Why not an exception.** The renderer must not be able to abort a nightly report
over a presentational defect. Loud in the artifact, not fatal to it.

## R7 — § 5.2 IS A PIN, NOT AN ADDITION — and the family has TWO action lines

**FINDING, recorded because it changes what F4 owes.** § 5.2 reads as if the
action line were F4's to add. It is not: F1 landed it as
`modified_block_currency._ACTION`, verbatim § 5.2's wording, and it has been
rendering in the ranked plan since. Read as "add", F4's § 5.2 is a no-op; read as
"pin", it is a real deliverable. F4 implements the pin.

**AND § 5.2 IS IMPRECISE.** It says "The action line", singular. The family has
two:

| class | action |
| --- | --- |
| scenario-title completeness, carriage ledger, title resolution and ordering | `_ACTION` — "restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" |
| marker defects | `_MARKER_ACTION` — "name a unit the block does not restate, or drop the declaration — a marker that does not describe the block declares nothing" |

The split is correct and F1 argued it: the remedy for an uncarried unit is not
the remedy for a declaration that does not describe the block. F4 pins both and
records that § 5.2's singular is the imprecision, not the code.

**Where action lines live.** There is no per-family action registry to add a row
to. Each family constructs its findings with an `action=` argument, and
`report.plan_line` renders it into the ranked plan as `action="…"`. So "find
where per-family action lines live and add this family's" resolves to: they live
at each family's own finding construction, this family's is already there, and
F4's work is the assertion.

## R8 — PROVING "NO OTHER FAMILY MOVED": two independent proofs, both already available

**DECISION.** Both, because they fail differently.

1. **In-process, deterministic, corpus-free.** Render one synthetic finding set
   spanning several families twice — once with the summary registry active, once
   with it empty — and assert the two texts differ ONLY inside
   `### modified-block-currency`. This is the byte-identity proof for the
   MECHANISM: it cannot be perturbed by the corpus, and it fails on a
   generalisation that leaks (e.g. a stray blank line for every family).
2. **End-to-end, over the real tree.** F3's
   `test_the_report_moves_only_in_this_family_s_lines` already renders two
   single-repo reports differing only by `--skip-family` and permits movement in
   exactly `## Headline`, `### modified-block-currency` and `## Ranked Plan`. The
   subtotal lands inside the second, so that gate passes unchanged and is F4's
   corpus-level proof. **It is not duplicated here.**

## R9 — THE § 5.3 PIN: two halves, and a non-vacuity clause on each

**DECISION.** A new test file of this family's own, asserting:

- **the workflow half** — parse `.github/workflows/doc-health-reusable.yml`, walk
  every job's every step, and assert no `run`, `env` value or `with` value names
  this family in either spelling. Non-vacuity: assert the same walk FINDS
  `--promotion-fidelity-basis live-main`, so "absent" is measured over a file
  that demonstrably carries per-family options, and assert the workflow parsed to
  a non-empty job map.
- **the surface half** — enumerate the checker's own command-line options and
  assert none names this family, while `--family modified-block-currency` and
  `--skip-family modified-block-currency` remain accepted. A generic option that
  takes every family's id is not a per-family option, and a pin that could not
  tell them apart would forbid the family being runnable at all.

**Cited, not duplicated.** F1's
`test_the_promoted_reader_cannot_reach_a_measurement_basis` pins that the
family's readers have no parameter a basis could arrive through, and F1's
`test_the_advisory_launch_is_pinned_in_both_halves` pins the severities and the
`FAMILY_RESOLUTION` absence. F4 cites both by name and asserts the two things
they do not: what the WORKFLOW passes, and what the CLI ACCEPTS.

**Reading the workflow in a test is fine; editing it is not.** § 5.3 says no
workflow change, and the diff assertion (FR-018) is the mechanical proof.

## R10 — THE SUBTOTAL IS FAMILY-WIDE, NOT PER-REPOSITORY

**DECISION.** One block per family section, counting across every repository in
scope. The section it heads is family-wide and every row already names its repo;
a per-repo tally would grow the block to 4×N lines in the aggregation run for a
question ("which repo?") the rows answer.

## R11 — HERMETICITY OF THE WORKFLOW READ

`.github/workflows/doc-health-reusable.yml` is a tracked file, so it is present
in a `git archive HEAD` extraction and the § 5.3 test runs in CI shape without a
network, a token or a checkout of anything else. F3's lesson (prove
environment-sensitive tests through `git archive HEAD | tar -x` into a bare dir)
applies and is cheap here; the test reads one tracked file and `yaml.safe_load`s
it, exactly as `test_workflow_contract.py` already does.

## What remains OPEN (not decided by this feature)

**F3's blast-radius question.** Whether the six corpus-facing tests of
`test_modified_block_currency_self_gate.py` belong in the REQUIRED `pytest-suite`
check or in the nightly lane. Brett's call. Arguments both ways are recorded in
F3's `tasks.md` § OPEN QUESTION FOR BRETT, including the event on PR #427 that is
evidence for both sides. F4 changes nothing about it and repeats it in its
hand-off and PR body.
