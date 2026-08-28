# RED log — every behavioural test seen to fail before the module moved

Taken at the branch point `86b7ca3f`, with the fixture tree landed (T004–T006)
and the module UNTOUCHED. Command:

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency_reporting.py \
                 tests/doc-health/test_modified_block_currency.py -q --tb=line
```

Result: **11 failed, 124 passed.**

| Task | Test | Observed failure |
|---|---|---|
| T007 | `test_a_run_the_map_places_entirely_emits_no_additional_finding` | `AttributeError: … has no attribute 'CLASS_DRIFT'` at the POSITIVE CONTROL — there is no fifth class, so the "no drift finding" assertion below it would have been vacuous. That is the intended red: the control fires before the subject. |
| T008 | `test_a_rule_text_the_map_does_not_place_emits_one_warning_naming_it` | `AttributeError: … has no attribute 'CLASS_DRIFT'` — the map places nothing into a class that does not exist |
| T009 | `test_the_drift_warning_is_worked_from_the_ranked_plan` | `AttributeError: … has no attribute '_DRIFT_ACTION'. Did you mean: '_MARKER_ACTION'?` — no action line exists for a finding the family cannot emit |
| T017 | `test_the_drift_finding_is_placed_by_the_map_and_never_by_the_residual` | `AttributeError: … has no attribute 'CLASS_DRIFT'` |
| T018 | `test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled` | `AttributeError: … has no attribute 'CLASS_DRIFT'` |
| T019 | `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern` | `AttributeError: … has no attribute 'CLASS_DRIFT'` at the positive control. Without that control this test would have PASSED vacuously against a four-entry map — recorded because it is the one test here whose subject (exactly one pattern matches) is already true before the feature. |
| T021 | `test_extending_the_map_removes_both_the_finding_and_the_residual_row` | `AttributeError: … has no attribute 'CLASS_DRIFT'` |
| T023 | `test_two_unplaced_findings_of_one_shape_are_one_remedy` | `AttributeError: … has no attribute '_shape'` — there is no shape function, so there is no identity to group by |
| T024 | `test_two_unplaced_shapes_are_two_remedies` | `AttributeError: … has no attribute '_shape'` |
| T025 | `test_the_drift_finding_names_the_first_instance_in_report_order_and_is_deterministic` | `AttributeError: … has no attribute 'CLASS_DRIFT'` |
| T022 | `test_the_reserved_flip_of_the_launch_severity_does_not_drag_the_drift_class` | `AttributeError: … has no attribute 'CLASS_DRIFT'` — the simulated flip runs and the registry it produces has four classes |

**What this red does and does not prove.** It proves every test reaches the
mechanism and none passes vacuously against the pre-feature module. It does NOT
discriminate between a correct emit and a wrong one — an `AttributeError` is a
structural red. The behavioural discrimination is the MUTATION ROUND (T043),
where each mutant is applied to the LANDED module and the named test is required
to red; that is recorded in `mutation-round.md`.

**Not red, and correctly so:**
`test_the_new_fixture_tree_declares_its_provenance_and_stays_advisory` passed
here. It pins a convention about the tree, not a behaviour of the class, and the
tree landed in Phase 2.
