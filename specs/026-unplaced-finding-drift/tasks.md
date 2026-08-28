# Tasks: the fifth finding class — unplaced-finding drift (F5)

**Feature**: `026-unplaced-finding-drift` | **Branch point**: `86b7ca3f` |
**Merge base at landing**: `22f15cdf` (catch-up merge, never a rebase)
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**Realizes**: `openspec/changes/add-unclassified-finding-class` § 2 (boxes
2.1–2.15). Every task below cites the packet box it realizes. Nothing is added
beyond what Speckit's template requires (setup, evidence, gates); nothing in the
packet is dropped.

**Tests ARE requested, RED-FIRST, and this is not optional here.** The packet
says so in § 2 ("RED first on every box that asserts behaviour: the test is
written against the delta's words, run, and seen to fail for the stated reason
before the module moves") and the constitution's Principle V requires
deterministic evidence rather than assertion.

## THE RED GATE (a hard ordering constraint across phases)

`T007`–`T009`, `T017`–`T019`, `T021`–`T022` and `T023`–`T025` are the RED tests
of **all four behavioural stories**. Every one of them MUST be written, run, and
recorded as failing for its stated reason — in `evidence/red-log.md` — **before
`T010`**, the first module task, is started.
The per-story phases below are therefore an organization of the WORK, not a
permission to land the module early: US2, US3 and US4's tests go red in Phase 3's
window alongside US1's, and go green together when T018–T022 land.

The reason is the packet's, not a preference: the module edit, the pins it moves
and the tests that hold it are one vertical slice over one module and one report
block, and splitting them produces halves neither of which is green alone.

## THE LIVE-TRIGGER HONESTY NOTE (repeat it in every docstring it applies to)

No corpus-supplied requirement title can produce an unplaced rule text while the
class map is complete: every rule text this family constructs is one of five
fixed prefixes plus `{title!r}`, and `_TITLE_REPR` admits every `repr` Python
can emit. Measured at packet review (§ 3.5): 20,065 constructed rule texts, **0
unplaceable**. So every behavioural test of the fifth class induces the drift by
REMOVING one entry from `_CLASS_PATTERNS`, which is precisely the live condition
"the map has drifted behind the arms". This sentence belongs in the docstring of
every test that monkeypatches the map, and it is in `plan.md` § O2.

---

## Phase 1: Setup and evidence baseline

- [x] T001 Record the branch point and the BEFORE self-gate figure taken at it (NOT copied from packet § 3.1) in `specs/026-unplaced-finding-drift/evidence/self-gate-before.txt`, from `python3 scripts/doc-health.py --single-repo . --family modified-block-currency` — packet § 2.13, § 3.1
- [x] T002 Record the BEFORE test count in `specs/026-unplaced-finding-drift/evidence/test-counts.md` from `python3 -m pytest tests/doc-health -q` — constitution Principle V
- [x] T003 Create `specs/026-unplaced-finding-drift/evidence/red-log.md` with one section per RED test, each to carry the test name, the command, and the failure reason observed — packet § 2 preamble

---

## Phase 2: Foundational — the fixture tree (blocks every behavioural test)

**Blocking**: T004–T017 all read this tree. It is INERT until the fifth class
exists — over the unmodified map it contributes only PLACED findings — so it
lands before any RED test and makes those tests assertable over MEASURED
findings rather than constructed `Finding` objects.

- [x] T004 Create the fixture tree `tests/doc-health/fixtures/modified-block-currency-unplaced/<repo>/openspec/` with a promoted spec and one active change carrying a MODIFIED block that produces at least one carriage-ledger finding and one scenario-title finding, ALL REQUIREMENT TITLES PLAIN — no title may contain `omits`, `does not carry`, `carries a … marker by`, `resolves to no promoted requirement`, `the ordering of MODIFIED blocks`, or the fifth class's own opening phrase — packet § 2.8
- [x] T005 Write `tests/doc-health/fixtures/modified-block-currency-unplaced/README.md` with `SYNTHESIZED` (case-sensitive, whole word) on LINE 3 per F2's convention, naming this feature and this packet rather than an F2 audit row — packet § 2.8, plan § O5
- [x] T006 Confirm the new tree joins `ALL_TREES` by glob in BOTH test files and breaks neither F2's unanchored `CLASSIFIERS` partition (`test_every_finding_falls_into_exactly_one_class`) nor F4's production-pattern partition, by running `tests/doc-health/test_modified_block_currency_fixtures.py` and `..._reporting.py` — packet § 2.8

---

## Phase 3: User Story 1 — the drift reaches the ranked plan (P1) 🎯 MVP

**Goal**: a nonzero residual becomes work: one `warning` per distinct unplaced
rule shape per run, naming the count, quoting the first instance verbatim, and
carrying its repository and delta path.

**Independent test**: induce a drift over the new tree and read the rendered
report — a `warning` row for this family appears in the ranked plan with the
count, the verbatim rule text, the repo, the path and the action line.

### RED tests (before any module change)

- [x] T007 [P] [US1] Write `test_a_run_the_map_places_entirely_emits_no_additional_finding` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 1, over every fixture tree and the real tree, asserting the counts still sum — packet § 2.6(1)
- [x] T008 [P] [US1] Write `test_a_rule_text_the_map_does_not_place_emits_one_warning_naming_it` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 2: one `warning` per shape, the shape's count, the FIRST instance's rule text VERBATIM (`first.rule` a suffix of the drift rule), its repo and path, and `_DRIFT_ACTION`; carries the live-trigger honesty note in its docstring — packet § 2.6(2)
- [x] T009 [P] [US1] Write `test_the_drift_warning_is_worked_from_the_ranked_plan` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 5: the finding renders as a ranked-plan item with its severity, repo, path and `action="…"`, AND the residual row still renders in the family's own block — packet § 2.6

### Implementation (the vertical slice — starts only after the RED gate)

- [x] T010 [US1] Add `_DRIFT_SEVERITY = WARNING` as the module's FOURTH severity constant in `scripts/doc_health/modified_block_currency.py`, with the comment stating why it is NOT `_LAUNCH_SEVERITY` (§ 7.2's flip must not drag it, and the drag would be invisible), and update the section header's "THREE OF THEM" to four — packet § 2.1
- [x] T011 [US1] Add `_DRIFT_ACTION` in `scripts/doc_health/modified_block_currency.py`, verbatim "extend the class map in \`scripts/doc_health/modified_block_currency.py\`, or fix the drifted rule text the finding names", with NO interpolated path — packet § 2.1
- [x] T012 [US1] Append the fifth `FindingClass` to `CLASSES` in `scripts/doc_health/modified_block_currency.py` — id `unplaced`, label `unplaced-finding drift`, band `_DRIFT_SEVERITY`, action `_DRIFT_ACTION`, NO gloss, LAST — and update the gloss sentence's numerals (two of FIVE carry one, three do not) — packet § 2.2
- [x] T013 [US1] Append the anchored pattern to `_CLASS_PATTERNS` in `scripts/doc_health/modified_block_currency.py` — packet § 2.3
- [x] T014 [US1] Add `_shape()` to `scripts/doc_health/modified_block_currency.py`: mask every single- and double-quoted span, then every digit run, with two DIFFERENT fixed placeholders, reusing `_TITLE_REPR`'s own alternation rather than re-spelling it — packet § 2.4, research R3
- [x] T015 [US1] Add the emit to `fam_modified_block_currency` in `scripts/doc_health/modified_block_currency.py`: after the arms and after the existing severity-first sort, group the `UNCLASSIFIED` findings by shape, append EXACTLY ONE `warning` per shape carrying the count, the first instance's rule text verbatim, its repo, its delta path and `_DRIFT_ACTION`, then sort again — packet § 2.4
- [x] T016 [US1] Verify `classify`, `class_counts` and `class_summary` keep their signatures and their no-context discipline, and that the residual row is neither replaced, moved nor reworded, by running `test_the_summary_reads_the_findings_and_nothing_else` UNTOUCHED — packet § 2.5

---

## Phase 4: User Story 2 — the tally still sums, and the anchor holds (P1)

**Goal**: the drift finding is placed by the map into the fifth class, so it is
never counted by the residual it reports, and the counts still sum to the rows.

**Independent test**: over a drifted run, the block's five class counts plus the
residual equal the rows printed beneath it, and the drift finding is in the
fifth class.

### RED tests (written in Phase 3's window, before T010)

- [x] T017 [P] [US2] Write `test_the_drift_finding_is_placed_by_the_map_and_never_by_the_residual` in `tests/doc-health/test_modified_block_currency_reporting.py` — the drift finding classifies `unplaced`; the residual counts ONLY the induced-unplaced arm findings; the rendered counts equal the rendered rows in the drifted state — packet § 2.6(2)
- [x] T018 [P] [US2] Write `test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 4: the quoted rule text itself begins `active MODIFIED block for '…' omits …`; the drift finding classifies `unplaced`, NOT `scenario-titles`, with the unanchored-probe positive control beside it in F4's own idiom; and the unplaced finding it names is still counted by the residual — packet § 2.3, § 2.6(4)
- [x] T019 [P] [US2] Write `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern` in `tests/doc-health/test_modified_block_currency_reporting.py` — a corpus-supplied requirement title carrying the fifth class's own opening phrase; exactly ONE production pattern matches the resulting carriage-ledger finding. This is what makes the anchor falsifiable and is what mutation (d) reds — research R2

### Verification

- [x] T020 [US2] Confirm the existing `test_the_summary_counts_sum_to_the_findings_it_was_handed` and `test_the_rendered_counts_equal_the_rendered_rows` stay green UNTOUCHED over the extended registry, in `tests/doc-health/test_modified_block_currency_reporting.py` — FR-016

---

## Phase 5: User Story 3 — the finding disappears cleanly, and the flip cannot drag it (P2)

**Goal**: extending the map removes the finding and the residual row, and that
disappearance is never an uncited resolution; and the reserved flip of the
scenario-title arm to `error` leaves this class's band alone.

**Independent test**: extend the map over the same tree — no drift finding, no
residual row; and simulate the flip over the module's own source — the
scenario-title class moves, the drift class does not.

### RED tests (written in Phase 3's window, before T010)

- [x] T021 [P] [US3] Write `test_extending_the_map_removes_both_the_finding_and_the_residual_row` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 6: restore the removed pattern, re-run over the same tree, assert both are gone and the family is still absent from `FAMILY_RESOLUTION` so nothing is classified `contested` — packet § 2.6(5)
- [x] T022 [P] [US3] Write `test_the_reserved_flip_of_the_launch_severity_does_not_drag_the_drift_class` in `tests/doc-health/test_modified_block_currency.py` — execute the module's OWN source with `_LAUNCH_SEVERITY = WARNING` textually replaced by the package's `error` constant, in the `doc_health` package namespace, and assert the scenario-title class's band became `error` while the drift class's band is still `warning`. This is the pin § 2.14(e) says is owed — packet § 2.1, § 2.14(e), § 4.1, plan § O6

---

## Phase 6: User Story 4 — two shapes are two remedies (P2)

**Goal**: one finding per DISTINCT unplaced rule shape — not one per run, not
one per repository, not one per unplaced finding.

**Independent test**: two unplaced findings equal after masking → ONE additional
finding naming the count two; two that differ outside the masked spans → TWO.

### RED tests (written in Phase 3's window, before T010)

- [x] T023 [P] [US4] Write `test_two_unplaced_findings_of_one_shape_are_one_remedy` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 3, first half: rule texts equal after every quoted span and digit run is masked → ONE finding naming the count two — packet § 2.6(3)
- [x] T024 [P] [US4] Write `test_two_unplaced_shapes_are_two_remedies` in `tests/doc-health/test_modified_block_currency_reporting.py` — delta scenario 3, second half: rule texts differing OUTSIDE their quoted spans and digit runs → TWO findings — packet § 2.6(3)
- [x] T025 [P] [US4] Write `test_the_drift_finding_names_the_first_instance_in_report_order_and_is_deterministic` in `tests/doc-health/test_modified_block_currency_reporting.py` — the repo and path are the FIRST instance's in the family's own report order, and two runs over the same tree agree byte for byte — FR-004, packet § 2.4

---

## Phase 7: User Story 5 — the corpus stays true about the code (P3)

**Goal**: the byte-level report contract and every prose numeral agree with the
five-class module.

**Independent test**: read the contract's four enumeration sites and grep the
module and its tests for a numeral the code contradicts.

**ORDERING NOTE (analyze F1)**: this phase is numbered by story priority but RUNS
AFTER Phase 8. A byte-level contract written from a plan rather than from landed
code is how a contract becomes false — the defect this family exists to catch. See
the Dependencies block.

- [x] T026 [US5] Amend `specs/022-modified-block-currency-reporting/contracts/report-section.md` at ALL FOUR class-enumeration sites — the per-class bullet list, the worked example, the class-map grammar, and the action-line table — leaving the residual bullet unchanged — packet § 2.9
- [x] T027 [P] [US5] Sweep the module numerals in `scripts/doc_health/modified_block_currency.py`: the docstring's "THREE ARMS, FOUR FINDING CLASSES", the severity block's "THREE OF THEM" (T010), `_arm_marker_defects`'s "Three arms, four classes", the F4 section comment's "The four classes above", `FindingClass`'s "four finding classes", the gloss sentence (T012), and "FOUR ENTRIES FOR FIVE RULE SHAPES" — packet § 2.12
- [x] T028 [P] [US5] Sweep the test numerals: `tests/doc-health/test_modified_block_currency.py` line 16; `tests/doc-health/test_modified_block_currency_reporting.py` at its docstring, the class-registry docstring, the five-rule-shapes docstring, and `test_the_block_renders_on_a_run_that_found_nothing`'s "All four counts read 0" (a DOCSTRING numeral whose assertions survive — § 2.12's, deliberately NOT § 2.7's); `tests/doc-health/test_modified_block_currency_fixtures.py`'s "its four finding classes" — packet § 2.12, § 3.6

---

## Phase 8: The standing pins that red on realization (moved BY NAME, never by re-running until green)

The packet enumerated these before the feature started so none is discovered as
a surprise (§ 3.6). A pin moved by iteration is a pin nobody read.

- [x] T029 [P] Move `test_the_class_registry_is_closed_ordered_and_states_a_band_per_class` in `tests/doc-health/test_modified_block_currency_reporting.py` — five ids, five bands (the fifth reading `mbc._DRIFT_SEVERITY`), five actions, five distinct labels — packet § 2.7
- [x] T030 [P] Move `test_each_of_the_five_rule_shapes_classifies_into_its_own_class` in `tests/doc-health/test_modified_block_currency_reporting.py` — five shapes and four classes become SIX and FIVE; the sixth shape is the drift rule text, reached through the induced drift rather than hand-copied. **RENAME the function to `test_each_of_the_six_rule_shapes_classifies_into_its_own_class`**: the packet cites the `def` line and a function name stating a count the code contradicts is the same defect § 2.12 sweeps out of the prose — packet § 2.7, plan § O8, analyze U1
- [x] T031 [P] Move `test_the_summary_states_every_class_with_its_count_and_band` in `tests/doc-health/test_modified_block_currency_reporting.py` — the VERBATIM four-row list becomes five, the new row `- unplaced-finding drift: 0 (\`warning\`)` — packet § 2.7
- [x] T032 [P] Move `test_the_block_renders_under_the_heading_before_the_first_row` in `tests/doc-health/test_modified_block_currency_reporting.py` — the LAST-row assertion and the blank-line-after assertion both move from `marker defects` to the new row — packet § 2.7
- [x] T033 Move `test_every_finding_carries_its_class_s_band_and_action` in `tests/doc-health/test_modified_block_currency_reporting.py`: add a MONKEYPATCHED PASS over the new fixture tree with one `_CLASS_PATTERNS` entry removed, so `all(checked.values())` reads a MEASURED `unplaced` count. **The amended pass MUST NOT index `by_id` with `UNCLASSIFIED`** — it partitions explicitly, asserting over the induced-unplaced arm findings directly and sending everything else, the drift finding included, through `by_id` as before — packet § 2.7, § 2.8, research R5
- [x] T034 [P] Move the `len(block) == 5` pin to 6 inside `test_the_block_is_not_a_finding_and_cannot_become_one` in `tests/doc-health/test_modified_block_currency_reporting.py` — and the test's SUBJECT, that the block never re-enters `report.parse_previous`, must not weaken by one assertion — packet § 2.7
- [x] T035 [P] Add the FOURTH probe WITH its positive control to `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` in `tests/doc-health/test_modified_block_currency_self_gate.py` — the probe string is first asserted to be the module's own wording (and is distinct from the residual line's wording, plan § O3), then the drift class is asserted to read zero over the real tree; the docstring's "THREE CLASSES" becomes four — packet § 2.10
- [x] T036 [P] Add `_DRIFT_SEVERITY` to the FR-023 severity tuple in `test_this_feature_touches_no_production_module` in `tests/doc-health/test_modified_block_currency_fixtures.py`, and assert the public-callable list is UNCHANGED rather than editing it — packet § 2.11
- [x] T037 [P] Add a provenance pin for the new fixture tree in `tests/doc-health/test_modified_block_currency_reporting.py` — line 3 carries `SYNTHESIZED` (case-sensitive, whole word) — since F2's `NEW_TREES` checker requires an F2 audit-row citation this tree honestly cannot make. The SAME task also sweeps the new tree's bands (`warning`/`info` only, non-empty first), because F2's `test_no_new_tree_reports_an_error_or_critical_finding` iterates `NEW_TREES` and therefore does not reach it — plan § O5, analyze C2

---

## Phase 9: Gates, evidence and the mutation round

- [x] T038 Run `python3 -m pytest tests/doc-health -q` and record the AFTER count beside the before in `specs/026-unplaced-finding-drift/evidence/test-counts.md`; the count moves only by the tests this feature adds — constitution Principle V, SC-007
- [x] T039 Run `python3 scripts/doc-health.py --single-repo . --family modified-block-currency` and record it as `specs/026-unplaced-finding-drift/evidence/self-gate-after.txt`; assert against T001's before figure that movement is ZERO in every band and the ONLY difference is the fifth class row reading `0` — packet § 2.13
- [x] T040 Prove the CI shape of every environment-sensitive test with `git archive HEAD | tar -x` into a bare directory plus `git init`, and record the result in `specs/026-unplaced-finding-drift/evidence/ci-shape.md` — never a whole-tree `pytest tests` from a worktree
- [x] T041 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` from `openxFactory/` and record the totals in `specs/026-unplaced-finding-drift/evidence/validate.md` — constitution Principle V
- [x] T042 Run the dogfood pair — the report WITH and WITHOUT `--skip-family modified-block-currency` — and record that the block renders in one and not the other, in `specs/026-unplaced-finding-drift/evidence/dogfood.md` — F4's state table
- [x] T043 MUTATION ROUND, all of packet § 2.14 plus three reviewer-style extras, each mutation reverted and each failure recorded in `specs/026-unplaced-finding-drift/evidence/mutation-round.md`: (a) delete the fifth class's pattern from `_CLASS_PATTERNS` → the drift finding counts itself, T017 reds; (b) make the emit unconditional → T007 reds; (c) collapse the per-shape grouping to one finding per run → T024 reds; (d) make the pattern unanchored → T019 reds; (e) point `_DRIFT_SEVERITY` at `_LAUNCH_SEVERITY` → T022 reds; (f) put the substring `unclassified` in the class label → `test_a_finding_the_map_cannot_place_is_counted_and_named` reds; (g) drop the anchor from the TITLES pattern → T018's adversarial-title test reds; (h) `repr`-wrap the quoted rule text → T008's verbatim assertion reds — packet § 2.14
- [x] T044 SCOPE DIFF, proved mechanically and recorded in `specs/026-unplaced-finding-drift/evidence/scope-diff.md`: `git diff --stat $(git merge-base HEAD origin/main) -- .github/ openspec/` MUST be EMPTY, and `git diff --stat $(git merge-base HEAD origin/main) -- scripts/ tests/ specs/022-modified-block-currency-reporting/contracts/` MUST name only the module, the four `test_modified_block_currency*.py` files, the new fixture tree and `report-section.md`. Name FR-018's own pin in the evidence: `test_the_reporting_list_mirrors_the_registry` still reads `len(FAMILY_IDS) == 22` UNTOUCHED, which is what proves this feature added no deterministic check family — packet § 2.15, plan § O7, analyze C1

---

## Dependencies

```text
Phase 1 (T001–T003)  ─┐
Phase 2 (T004–T006)  ─┴─> THE RED GATE: T007–T009, T017–T019, T021–T025 all RED
                                        │
                                        v
                          Phase 3 impl (T010 → T011 → T012 → T013 → T014 → T015 → T016)
                                        │
                          ┌─────────────┼─────────────┬──────────────┐
                          v             v             v              v
                     US1 green     US2 green     US3 green      US4 green
                     (T007–T009)   (T017–T020)   (T021–T022)    (T023–T025)
                                        │
                                        v
                          Phase 8 pins (T029–T037)  — T033 depends on T004–T006
                                        │
                                        v
                          Phase 7 contract + numerals (T026–T028)
                                        │
                                        v
                          Phase 9 gates + mutation (T038–T044)
```

**Forced orderings inside Phase 3**: T010 → T012 (the class cannot be
constructed before its band constant), T011 → T012 (nor before its action),
T012 → T013 (the pattern names the class id), T014 → T015 (the emit groups by
shape). T016 is a verification, not an edit.

**Phase 7 after Phase 8**: the contract describes what the code now does. Writing
it from the plan rather than from the landed code is how a byte-level contract
becomes false, which is the defect this whole family exists to catch.

## Parallel opportunities

- **T007, T008, T009, T017, T018, T019, T021, T023, T024, T025** — all RED
  tests, all in `..._reporting.py` except T022 (`test_modified_block_currency.py`).
  Parallel in AUTHORING; they land in one file, so they are committed together.
- **T029, T030, T031, T032, T034, T035, T036, T037** — the standing pins, across
  three files. T033 is NOT parallel: it depends on the fixture tree and carries
  the monkeypatched pass.
- **T027, T028** — the two halves of the numeral sweep, different files.

## Independent test criteria per story

| Story | Independently testable by |
|---|---|
| US1 (P1) | induce a drift; a `warning` naming the count, quoting the first rule text verbatim, carrying its repo and path, reaches the ranked plan |
| US2 (P1) | over that drifted run, the five class counts plus the residual equal the rendered rows, and the drift finding is in the fifth class |
| US3 (P2) | restore the pattern → finding and residual row both gone, nothing `contested`; simulate the flip → the drift band does not move |
| US4 (P2) | two masked-equal unplaced findings → one finding naming two; two masked-different → two findings |
| US5 (P3) | the contract enumerates five classes at all four sites; no prose numeral in the module or its tests states a count the code contradicts |

## Implementation strategy

**MVP is US1 + US2 together, and they cannot be split.** US1's emit is incoherent
without US2's placement — a drift finding the map cannot place would be counted
by the residual it reports, the count would name itself, and the tally would stop
summing. That is decision D2(a) of the ratified packet, rejected there as
incoherent, and it is why this whole change is ONE feature.

US3 and US4 add no production code beyond what US1's slice already lands; their
value is that the behaviour is PINNED — the disappearance is clean, the flip
cannot drag the band, and the per-shape count is the count of remedies.

US5 is documentation fidelity and lands last, after the code it describes.

---

## Completion record

All 44 boxes are done. Evidence lives in `evidence/`:

| file | task |
|---|---|
| `self-gate-before.txt`, `self-gate-after.txt`, `self-gate.md` | T001, T039, T041, T042 |
| `test-counts.md` | T002, T038 |
| `red-log.md` | T003, and the RED gate over T007–T025 |
| `ci-shape.md` | T040 |
| `mutation-round.md` | T043 |
| `scope-diff.md` | T044 |

**Headline results.** Test suite 1215 → **1227 passed** (+12, every one named).
Self-gate before/after diff: **exactly one line**, the fifth class row reading
`0` — zero movement in every band, over a FULL report so the comparison covers
all twenty-two families. `openspec validate --all --strict`: **78 passed, 0
failed** (77 before the catch-up merge). Mutation round: **9 applied, 9 killed, 0 survivors** (one, the
unanchored-pattern mutant, survived the first attempt and exposed a near-miss
adversarial title, now fixed). `.github/` and `openspec/` diffs: **empty**.

## Where the packet was wrong or incomplete, recorded rather than absorbed

1. **§ 2.15 says "the three `test_modified_block_currency*.py` files"; FOUR
   move** — the packet itself names all four across § 2.6–§ 2.12 (plan § O7).
2. **§ 3.6 predicted eight reddening pin sites; FIVE actually reddened.** All
   five are in `..._reporting.py`. The other three named sites are AMENDMENTS
   the packet described as reds: `test_each_of_the_five_rule_shapes_…`'s
   assertions survive a fifth class untouched (only its name and docstring were
   false — the same call § 2.7 made for `:429`, applied one test too narrowly);
   the self-gate's three-classes-read-zero test needed a probe ADDED, not
   corrected; and the FR-023 snapshot is a POSITIVE list, so a new PRIVATE
   constant does not red it. Worth knowing about that guard's reach.
3. **§ 2.7 moves the five-rule-shapes pin to "six and five" without saying the
   FUNCTION NAME must move** — recorded as plan § O8 and done.
4. **§ 2.8 names F2's provenance checker as though it would cover the new
   tree; it would not** — that checker iterates `NEW_TREES` and requires an F2
   audit-row citation this tree honestly cannot make (plan § O5).
5. **§ 2.14(e)'s mutant cannot be killed by any value comparison**, because the
   two constants are value-identical until § 7.2 flips one. The pin it says is
   owed was written: a simulated flip over the module's own source (plan § O6).
6. **An unforeseen pin moved**: the self-gate's
   `test_the_gate_reaches_the_corpus_only_through_the_family` allowlist. The
   fourth probe's positive control has to reach `_DRIFT_RULE` and
   `_UNCLASSIFIED_LINE` — it cannot use the other three probes' `in source`
   form, because the module source carries BOTH constants and a probe matching
   only the ROW would pass that control and then read a vacuous zero. Two names
   declared, with the reason, in the allowlist's own convention.
