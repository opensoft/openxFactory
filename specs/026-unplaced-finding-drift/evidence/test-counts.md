# Test counts, before and after (T002, T038)

```bash
python3 -m pytest tests/doc-health -q
```

| point | result |
|---|---|
| branch point `86b7ca3f`, module untouched | **1215 passed**, 7 warnings |
| after the RED tests, before the module | 11 failed, 124 passed *(family files only — see `red-log.md`)* |
| feature landed | **1227 passed**, 7 warnings |
| after the mutation round, module restored | **1227 passed**, 7 warnings |
| after the catch-up merge to `22f15cdf` | **1227 passed**, 7 warnings |

The merge moves neither figure: `git diff 86b7ca3f 22f15cdf -- tests/doc-health/
scripts/doc_health/` is EMPTY, so the 1215 baseline still stands against the
merged base.

**+12, and every one is named.** Eleven in
`test_modified_block_currency_reporting.py`:

1. `test_a_run_the_map_places_entirely_emits_no_additional_finding` (delta sc. 1)
2. `test_a_rule_text_the_map_does_not_place_emits_one_warning_naming_it` (sc. 2)
3. `test_the_drift_warning_is_worked_from_the_ranked_plan` (sc. 5)
4. `test_the_drift_finding_is_placed_by_the_map_and_never_by_the_residual` (sc. 2)
5. `test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled` (sc. 4)
6. `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern`
7. `test_two_unplaced_findings_of_one_shape_are_one_remedy` (sc. 3, first half)
8. `test_two_unplaced_shapes_are_two_remedies` (sc. 3, second half)
9. `test_the_drift_finding_names_the_first_instance_in_report_order_and_is_deterministic`
10. `test_extending_the_map_removes_both_the_finding_and_the_residual_row` (sc. 6)
11. `test_the_new_fixture_tree_declares_its_provenance_and_stays_advisory`

and one in `test_modified_block_currency.py`:

12. `test_the_reserved_flip_of_the_launch_severity_does_not_drag_the_drift_class`

**No test was deleted.** One was RENAMED —
`test_each_of_the_five_rule_shapes_classifies_into_its_own_class` →
`test_each_of_the_six_rule_shapes_classifies_into_its_own_class` — which is a
count, not a delta.

**All six of the delta's scenarios have a named test**, and each was seen to
fail before the module moved (`red-log.md`).

## The runtime figure, corrected

The branch-point run took 27 minutes and every run since has taken about 2. The
first one was competing with a concurrent full doc-health run on the same
machine; the suite's real cost is ~2 minutes. Recorded so the first figure is
not read as a regression this feature fixed.
