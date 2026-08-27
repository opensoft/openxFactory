# Tasks: modified-block currency — reporting and workflow (F4)

**Feature**: `022-modified-block-currency-reporting`
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Packet**: `add-modified-block-currency-check` `tasks.md` section 5 (5.1–5.3)

**RED-FIRST IS MANDATORY.** Every `[TEST]` task is written and SHOWN FAILING
before the implementation task beneath it. The RED form of each is recorded in
`contracts/report-section.md` / `contracts/workflow-boundary.md` and its observed
output in `evidence/f4-gates.md`. A `[TEST]` task ticked without a recorded RED
is the defect F1's, F2's and F3's mutation rounds each found once.

**One test file**: `tests/doc-health/test_modified_block_currency_reporting.py`.
Tasks that add to it are NOT `[P]` with each other — they share a file.

---

## Phase 1 — Setup

- [x] T001 Record the branch-point baseline in `specs/022-modified-block-currency-reporting/evidence/f4-gates.md`: `python3 -m pytest tests/doc-health -q` count, the family's per-class counts over this checkout, and `grep -rn "modified.block.currency\|modified_block_currency" .github/` returning nothing — each with the command that produced it, so every later number is a delta against a recorded one.

## Phase 2 — Foundational: the class map and the tally

**BLOCKS Phases 3–5.** Nothing can be rendered before a finding can be
classified, and the classification is the only part of this feature with a
correctness question in it.

- [x] T002 [TEST] RED: the four class ids exist as a closed ordered registry with a label, a band and an action per class, and `classify()` places one constructed finding of each of the five rule shapes (titles, ledger, marker, unresolved, ordering) into the right class — in `tests/doc-health/test_modified_block_currency_reporting.py`. RED form: the names do not exist (ImportError/AttributeError).
- [x] T003 Implement the class registry and `classify()` in `scripts/doc_health/modified_block_currency.py`, ADDITIVE ONLY — no existing line edited, no rule text touched, no `datetime`/`time` import, no `ctx` read (F1's source probes forbid all three).
- [x] T004 [TEST] RED: EVERY finding the family emits over the F2 fixture corpus AND over this repository's real tree classifies into exactly one class, with `residual == 0` — invariants I2 and I3 of `data-model.md`. RED form: assert `residual == 1` and read the real count in the message.
- [x] T005 [TEST] RED: the repr anchor — a carriage-ledger finding whose requirement title EMBEDS the titles phrase (`'X omits 1 of the 2 scenarios Y'`) classifies as `carriage-ledger` and as nothing else. RED form: drop the anchor from the patterns and watch the finding match two classes. This is the case an unanchored classifier misfiles, measured in research R2.
- [x] T006 [TEST] RED: `class_summary(findings)` returns the lead line and the four bullets of `contracts/report-section.md` section 1 verbatim, with the counts of the findings handed to it, and its counts sum to `len(findings)` (invariant I1). RED form: the function does not exist.
- [x] T007 Implement `class_summary()` in `scripts/doc_health/modified_block_currency.py`, taking findings and nothing else.
- [x] T008 [TEST] RED: invariant I4 — for each class, every finding the family emits in it carries THAT class's severity band and THAT class's action string, so the rendered `(warning)` / `(info)` label cannot drift from the rows it describes. RED form: swap two classes' bands in the expectation.
- [x] T009 [TEST] RED: the `unclassified` bullet renders when and only when the residual is nonzero, and names the count — driven by a synthetic finding of this family whose rule matches no pattern. RED form: assert the bullet is present for a fully classified set.

## Phase 3 — User Story 1: the subtotal reaches the report (P1)

**Goal**: a reader of `### modified-block-currency` learns the per-class split
from one block, before the rows.

**Independent test**: render a report from a known finding set; the block is
under the heading, before the first row, and its counts equal the rows.

- [x] T010 [TEST] [US1] RED: `families.FAMILY_SUMMARIES` exists, carries exactly this family, and its value is callable with a findings list (and NOT with a ctx) — pinned beside `FAMILY_NOTES` still carrying exactly `promotion-fidelity`, so the two registries are asserted apart. **AND FR-007 STRUCTURALLY** (analyze finding A1): `inspect.signature(class_summary).parameters == ["findings"]`, and its source names no `ctx`, no `Path`, no `open`, no `read_text` and no `glob` — the guarantee that the tally is a function of the findings and of nothing else, in the shape F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis` uses. RED form: the registry does not exist; then, for the second half, add a filesystem read to `class_summary` and watch it fail.
- [x] T011 [US1] Add `FAMILY_SUMMARIES` to `scripts/doc_health/families.py` beside `FAMILY_NOTES`, with the comment recording WHY it is a sibling registry rather than a widening of `FAMILY_NOTES` (research R1) — the same shape `FAMILY_NOTES`' own comment uses.
- [x] T012 [TEST] [US1] RED: `report.render(...)` puts the block under `### modified-block-currency`, AFTER any notes and BEFORE the first finding row, followed by one blank line — asserted in-process on a synthetic finding set, the shape `test_promotion_fidelity.py::test_the_report_states_the_basis_under_the_family_heading` uses. RED form: the block is absent. **This is the test mutation M1 must red.**
- [x] T013 [US1] Implement the additive notes/summary branch in `scripts/doc_health/report.py` per `contracts/report-section.md` section 4 — one `notes` list, the registry consulted only when the family was not skipped, and the existing "blank line only if non-empty" condition preserved unchanged.
- [x] T014 [TEST] [US1] RED: a run in which the family reports NOTHING still renders the block, all four counts `0`, ABOVE `No findings.` — so a clean run states which classes were measured. RED form: assert the block is absent on a clean run.
- [x] T015 [TEST] [US1] RED: `--skip-family modified-block-currency` renders the skip reason and NO block — a skip is the absence of a measurement, and zeros beside it would claim one (research R4, and the opposite call from `FAMILY_NOTES`, which is asserted in the same test so the difference is deliberate rather than incidental). RED form: assert the block IS present on a skipped run.
- [x] T016 [TEST] [US1] RED: the family's OWN scope `Skip` (a scope with no `openspec/changes/` directory) likewise renders no block. Two skip shapes, two tests, because canon's skip rule is "cannot run" and the two reasons are different text.
- [x] T017 [TEST] [US1] RED: the counts in the rendered block equal the rows rendered beneath it in the SAME section text — parsed back out of the rendered report rather than compared with the input list, so the assertion cannot pass by both sides being wrong the same way.
- [x] T018 [US1] Extend the `RunResult.notes` docstring in `scripts/doc_health/__init__.py` to record the SECOND kind of note now rendered in that position (a tally derived from the findings) beside the first (a fact about the run), and which registry owns each.

## Phase 4 — User Story 2: the action line, and nothing else moves (P1)

**Goal**: every finding names its remedy, and the subtotal changes no other
family's output.

**Independent test**: the ranked plan carries the action for every one of the
family's rows; two renders differing only by the registry differ only inside this
family's section.

- [x] T019 [TEST] [US2] RED: every finding of the three comparison arms carries the action of `contracts/report-section.md` section 6 verbatim ("restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker") — asserted on the finding AND on the rendered `action="…"` in `## Ranked Plan`, over the real tree's nine findings and over constructed findings of the two empty classes. RED form: assert a truncated action string.
- [x] T020 [TEST] [US2] RED: a marker-defect finding carries `_MARKER_ACTION` and NOT `_ACTION`, the remedy for a defective declaration not being the remedy for an uncarried unit — section 5.2 says "the action line" and the family has two (research R7). RED form: assert it carries `_ACTION`.
- [x] T021 [TEST] [US2] RED: BYTE IDENTITY — render one finding set spanning several families twice, once with the summary registry active and once with it empty, and assert the two texts differ ONLY inside `### modified-block-currency`; every other family's section, every other family's ranked-plan row and every `action="…"` in them byte-identical. RED form: make the render emit one blank line for every family and watch it fail naming the sections. **This is the test mutations M2 and M4 must red.**
- [x] T022 [TEST] [US2] RED: the block is NOT a finding — no line of it matches `report.PLAN_RE`, none appears in `## Ranked Plan`, and the `## Headline` severity counts are identical with the registry on and off. **DIRECTLY, not transitively** (analyze finding A2): `report.parse_previous(text)` returns the SAME `(error_keys, contested_keys)` for the two renders, which is the actual door into `previous_keys`, `regressions()` and `uncited_resolutions()` — asserting only that `PLAN_RE` misses the lines proves it one inference short. The shape is `test_promotion_fidelity.py::test_the_basis_lines_can_never_be_read_back_as_findings`. RED form: assert a subtotal line DOES match `PLAN_RE`.

## Phase 5 — User Story 3: no workflow option reaches this family (P1)

**`[P]` with Phases 3 and 4** — a different subject, no shared code, and the only
shared file is the one test module (so serialize the writes, not the thinking).

**Goal**: the boundary that currently holds by accident holds on purpose.

**Independent test**: the pin fails against a scratch workflow copy carrying a
per-family option for this family.

- [x] T023 [TEST] [US3] RED: W1+W2 of `contracts/workflow-boundary.md` — `.github/workflows/doc-health-reusable.yml` parses to a non-empty `jobs` map, and `--promotion-fidelity-basis live-main` IS found in exactly one step's `run`. The non-vacuity clause: "absent" is measured against a file that demonstrably carries per-family options. RED form: assert the flag appears in two steps.
- [x] T024 [TEST] [US3] RED: W3+W4 — no step's `run`, no `env` value and no `with` value in any job names this family in either spelling. `env` and `with` are walked as well as `run` because this workflow's untrusted-input idiom passes values through `env:`, so a `run`-only pin would miss the shape it actually uses. The test cites F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis`, F1's `test_the_advisory_launch_is_pinned_in_both_halves` and `test_workflow_contract.py::test_only_the_reporting_run_declares_the_live_main_basis` by name rather than duplicating them. RED form: point the reader at a scratch copy carrying the option. **This is the test mutation M3 must red.**
- [x] T025 [TEST] [US3] RED: W5+W6 — the checker's own option surface names no option after this family, while `--family modified-block-currency` and `--skip-family modified-block-currency` are still accepted. MECHANISM, so the task is executable without further decisions: run `python3 scripts/doc-health.py --help` in a subprocess and read the option strings out of its output; assert `--promotion-fidelity-basis` IS among them (the non-vacuity clause), that no option string contains either spelling of this family, and that the two generic options list this family's id among their choices. A generic option that takes every family's id is not a per-family option, and without W6 the pin would be satisfied by a family nothing can run. RED form: assert an option named after the family exists.

## Phase 6 — User Story 4: archive readiness (P3)

The packet's section 8.1 gates the archive on these three, and F4 is the last
feature before it. **Recording them is F4's; ticking section 8 is not.**

- [x] T026 [US4] `python3 -m pytest tests/doc-health -q` green; record the count before and after this feature in `evidence/f4-gates.md` so the added tests are visible as a delta. **The baseline figure has ONE home** — `research.md` section "The measurements this feature starts from" — and `evidence/f4-gates.md` is where the after-figure lands beside it (analyze finding A3, which is F3's own lesson about a figure with four homes).
- [x] T027 [US4] `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green; record the count.
- [x] T028 [US4] A doc-health single-repo run diffed against the same run with `--skip-family modified-block-currency`; record the per-band movement and confirm it equals the family's own per-severity finding counts on the same tree.
- [x] T029 [US4] `git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/` empty; record the command and its empty output. Any line is a scope violation, not a finding to disposition.

## Phase 7 — Polish, mutation round, hand-off

- [x] T030 Mutation M1 — delete the subtotal block from the render. T012 must red; record which tests failed and which did not.
- [x] T031 Mutation M2 — change another family's action line at its construction site. T021 must red.
- [x] T032 Mutation M3 — a SCRATCH copy of the workflow (never the tracked file) carrying `--modified-block-currency-basis live-main` in the `Run doc-health suite` step. T024 must red when pointed at it.
- [x] T033 Mutation M4 — make the render emit one blank line for EVERY family. T021 must red; this is the leak a byte-identity test exists for.
- [x] T034 Mutation M5 — delete the `unclassified` bullet. T009 must red.
- [x] T035 Prove the section 5.3 test's CI shape: `git archive HEAD | tar -x` into a bare directory, `git init`, and run the new test file there — F3's lesson, and cheap here because the workflow file is tracked.
- [x] T036 Re-run F1's, F2's and F3's own test files to prove no rule text moved: `python3 -m pytest tests/doc-health/test_modified_block_currency.py tests/doc-health/test_modified_block_currency_fixtures.py tests/doc-health/test_modified_block_currency_self_gate.py -q`. Record the count. F3's self-gate pins rule text BY SUBJECT, so a byte change in a rule would red it.
- [x] T037 Write `pr-body.md`: what landed, R1 flagged for veto, section 5.2's two findings (already-landed action line; the singular is imprecise), the section 8 archive-readiness numbers, and F3's OPEN QUESTION carried forward verbatim and undecided.
- [x] T038 Write the § Hand-off section of this file: what the archive act still owes, which assertions fall due when the packet archives (F3's list of four, unchanged), and the open question again.
- [x] T039 Complete `evidence/f4-gates.md`: every gate, every RED form observed, the mutation round's results, and the archive-readiness table.
- [x] T040 F2's production-surface guard (`test_modified_block_currency_fixtures.py::test_this_feature_touches_no_production_module`) reddened on F4's first full run, because F4 adds four public callables. **ADDED BY THE RUN, not planned** — and the guard's own docstring is the instruction that was followed: extend the snapshot as its own task, with a dated paragraph naming who added the names and why, and name it in the PR body. Never fold it into another commit and never loosen it. Recorded in `evidence/f4-gates.md` § 4a.

---

## Dependencies and execution order

- **Phase 1** → no dependencies.
- **Phase 2** → depends on Phase 1 only for the recorded baseline. **BLOCKS Phases 3–5.** Internal order is forced: T002/T003 (classify) before T004/T005 (its properties), before T006/T007 (the summary that consumes it), before T008/T009.
- **Phase 3 (US1)** → depends on Phase 2. Internal order forced: T010/T011 (registry) → T012/T013 (render) → T014–T017 (its states). T018 is documentation and may land with T013.
- **Phase 4 (US2)** → T019/T020 depend on Phase 2 only and could run earlier; T021/T022 depend on Phase 3 (a byte-identity test over an unpopulated registry is vacuous — plan § Implementation order).
- **Phase 5 (US3)** → depends on NOTHING in Phases 2–4. Fully `[P]`, one shared test file.
- **Phase 6** → depends on Phases 2–5 complete.
- **Phase 7** → depends on Phase 6. A mutation round over a partially built feature kills mutants for the wrong reason.

### Parallel opportunities

- Phase 5 (T023–T025) against all of Phases 2–4: different subject, different
  source file (none), no shared state. Serialize only the WRITES to the test
  module.
- T019/T020 against Phase 3: they assert F1's landed constants and need nothing
  from the render.
- Nothing in Phase 2 is parallel with itself.

## Implementation strategy

**MVP = Phase 1 + Phase 2 + Phase 3.** At that point the report says what
§ 5.1 asks it to say, which is the whole reader-facing value of this feature.

**Then**: Phase 4 (the pins that make it safe) → Phase 5 (the boundary) →
Phase 6 (the archive gate's numbers) → Phase 7 (the round that finds what green
tests did not).

**Never**: edit `.github/`, edit `openspec/`, change a rule text, change a
severity, tick the packet's section 8, or decide F3's open question.

---

## Hand-off — to the archive act, and to whoever meets a red first

**F4 IS THE LAST FEATURE. The next act is the packet's § 8 archive, and it is
NOT F4's.** § 8.1's three gates are recorded in `evidence/f4-gates.md` § 7 with
the commands that produced them: `pytest tests/doc-health` **1204 passed**,
`openspec validate --all --strict` **76 passed / 0 failed**, and a report moving
**+1 `warning`, +8 `info`** with the `error` and `critical` bands still at 0.

**Still owed at that gate, untouched here.**

1. **§ 8.2** — verify this change's own promotion byte-for-byte, per requirement,
   in BOTH capabilities, and resolve § 2.1's ordering against
   `add-family-enumeration-check` explicitly rather than by whichever archives
   first. A change whose subject is lossy promotion that promoted lossily would
   be the worst possible entry in this record.
2. **F3's LIST OF FOUR, unchanged.** On the archive day this packet's delta stops
   being an active change, and
   `test_this_change_s_own_delta_is_among_the_blocks_the_family_examined`,
   `test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists`,
   `test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences` and
   the self-finding triple in `_LEDGER_SUBJECTS` all fall due together. F3's
   hand-off records the expected disposition (re-aim at the archived path — a
   change of SUBJECT, since the family excludes `archive/` — or retire the group
   with a dated record). **Deleting it silently is the one wrong answer.**
3. **The composed-view rename.** `add-composed-view-authoring` declaring its
   rename with a `Removed from canon by` marker is the packet's own § 6.3
   disposition. When it lands, the scenario-arm `warning` goes to 0 — F3's T012
   fails with `_moved`'s instruction, and F4's subtotal reads
   `scenario-title completeness: 0`. Neither is a defect and neither is to be
   "fixed" by loosening.

**What F4 leaves that the next reader will want.**

- `evidence/f4-gates.md` § 3 is the mutation round, including **two mutants that
  SURVIVED first** (M2 and M4) and what each one bought. Both survivals were
  structural, not sloppy: a registry-on/off differential comparison is blind to
  any change affecting every family equally. The absolute assertions in
  `test_no_other_family_s_section_or_action_line_moves` exist because of M4 and
  are the only ones in the file a relative comparison cannot satisfy.
- **A GAP THAT IS NOT F4's**: no test in this repository pins any other family's
  action text. `promotion_fidelity._ACTION` was mutated and 85 tests stayed
  green (§ 3a). Closing it from here would mean snapshotting twenty-one families'
  action strings in F4's test file, which would red on their authors' PRs.
- Two imprecisions in packet § 5, recorded rather than worked around: § 5.2 reads
  as if the action line were F4's to add (F1 landed it), and § 5.2 says "the
  action line" where the family has two (`research.md` R7).
- A known wart, accepted and argued (`research.md` R5): in a `--family <other>`
  run this family's section renders a zeros subtotal although the family never
  ran — the same over-claim `No findings.` already makes for all twenty-one
  others, and the headline's `- scope limited to family …` deviation line is
  canon's own answer to it.

---

## OPEN QUESTION FOR BRETT — carried forward from F3, undecided

**Not decided by F4, and F4 changes nothing about it.** Recorded by F3's
combined review of 2026-08-27 and repeated here verbatim in substance because
this is the last feature and the question would otherwise archive with the
packet.

`_LEDGER_SUBJECTS` in `tests/doc-health/test_modified_block_currency_self_gate.py`
is an **exact set of live corpus triples**, and `pytest-suite` is a REQUIRED
check on `main` (org ruleset 21538893). So any pull request that adds a lossy
MODIFIED block, archives one of the changes in that table, or edits canon in a
way an active block quotes will red this gate — on a branch whose author may
have nothing to do with doc-health. That is § 4's intent working exactly as
written, and a cost nobody has priced.

**The option, if the cost is judged too high**: a pytest marker routing the six
CORPUS-FACING tests to the nightly doc-health lane, keeping the resolver guard,
the discovery floor and the structural pins in `pytest-suite`. The trade is
explicit — it gives up the PR-gate intent in exchange for a required check that
only fails on defects in the gate's own logic.

**It already happened once.** On PR #427 — F3's own pull request —
`pytest-suite` read `1 failed, 6985 passed`, and the failure was
`test_every_carriage_ledger_finding_over_the_real_tree_is_named` naming a triple
that had stopped being reported because PR #424 renamed a repository in canon and
in the active delta that quotes it, in one commit. Correct authoring; fixed by
merging `main`, re-measuring, and updating one row. **The event is evidence for
both sides and settles nothing.**

**F4 adds one small datum to it.** F4's own tests deliberately avoid the shape:
every corpus-facing assertion in
`test_modified_block_currency_reporting.py` is a FLOOR or an invariant
(`>= 1` finding, "every finding classifies", "the counts equal the rows"), never
a named set and never an absolute count. That was a choice available to F4
because it asserts a RENDERING rather than a verdict — it is not an argument
that F3 could have made the same choice, and it is not a decision about F3's
tests.

**Until Brett rules, F3's tests stay where they are.**

---

## SECOND OPEN QUESTION FOR BRETT — the residual row is text, and the real corpus is measured on one repository

**Raised by the combined review of 2026-08-27. NOT implemented here, because the
cheapest close is a delta change.**

The `unclassified` residual row (`research.md` R6, `contracts/report-section.md`
§ 1) is **text, not a finding**. It carries no severity, it reaches no
ranked-plan item, and no `--fail-on` configuration can see it — which is
deliberate for a presentational defect that must not abort a nightly report, and
is also the whole of its weakness: a class map that had drifted would announce
itself in a line a reader has to notice.

**And the only real-corpus classification test reads openxFactory alone.** The
nightly runs eighteen repositories. A rule text this map does not recognize can
therefore first appear on a corpus no test in this repository measures, and the
only thing that would say so is the row.

**Cheapest close, and why it needs a ruling**: have a nonzero `UNCLASSIFIED`
count emit ONE `warning` finding. That makes the residual a FIFTH finding class
of this family — which the promoted requirement enumerates as three arms and four
classes, so it is a **delta change**, not an implementation choice. It also
brings the residual inside `--fail-on` reach and inside the regression diff,
which is the point of it and also a decision about this family's gate.

**F4 leaves it as text and says so in three places** (the contract, the research
record and here), which is the most an implementation feature can do about a
question that belongs to the delta.

---

## FOLLOW-UP FOR THE DOC-HEALTH STEWARD — not F4's, and not this packet's

**No test in this repository pins any OTHER family's action text.**
`promotion_fidelity._ACTION` was mutated to `"MUTANT apply the ratified delta…"`
and **zero tests failed** — 85 green across that family's own suite and F4's
(`evidence/f4-gates.md` § 3a).

**The correct home is one pin per family, in that family's own suite**, where a
change to it reds the PR that made it and nobody else's. It is emphatically NOT a
table of twenty-one action strings in F4's test file, which would red on other
authors' PRs for their own legitimate edits — the same blast-radius cost the
first open question above is about.

Recorded here because F4's § 5.2 work is what surfaced it. Owner: the doc-health
steward, at the next change touching a family's action text.
