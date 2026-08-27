---
description: "Task list for F1 — the modified-block-currency family module and its registrations"
---

# Tasks: F1 — the modified-block-currency family module and its registrations

**Input**: Design documents from `specs/019-modified-block-currency-family/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Realizes**: `openspec/changes/add-modified-block-currency-check` § 2 (boxes
2.1–2.10). Those boxes are referenced, never restated — the OpenSpec change
owns the governance record and this file owns the execution order.

**Tests**: REQUIRED, and RED-FIRST. Orchestrator decision **O1** (plan.md
§ Decisions taken by the orchestrator) makes every F1 behaviour ship behind a
test that FAILED first. Task IDs are paired throughout: an odd-numbered `[TEST]`
task writes the failing test, and the next task makes it pass. A `[TEST]` task
is not done until the failure has been SEEN and its message recorded.

**The one honest limit on RED-first, stated rather than papered over**: a
POSITIVE behaviour can be proven by a pre-code failure. A NEGATIVE — "the
family must stay QUIET here" — often cannot, because the family is quiet before
the code exists too. For every negative assertion the equivalent proof is the
MUTATION named beside it in `quickstart.md`'s mutation table: the negative earns
its keep only if a named mutation makes it fail. Phase 9's mutation round is
therefore not polish; it is the RED proof for every quiet test in this list.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: parallelizable (different files, no dependency on an incomplete task)
- **[TEST]**: writes a test that must FAIL before the next task runs
- **[Story]**: US1–US5 from spec.md
- **A lettered suffix** (`T055a`) marks a task inserted by the adversarial plan
  review of 2026-08-27, keeping every earlier ID stable. The convention is the
  packet's own — its `tasks.md` § 3.3a does the same thing for the same reason.

## Path Conventions

- Module: `scripts/doc_health/modified_block_currency.py`
- Tests: `tests/doc-health/test_modified_block_currency.py`
- Fixtures: `tests/doc-health/fixtures/modified-block-currency*/<repo>/…`
- Registration: `scripts/doc_health/families.py`, `scripts/doc_health/__init__.py`
- The owed block: `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

**Test entry point convention, and it matters for ordering**: F1's behavioural
tests call `modified_block_currency.fam_modified_block_currency(ctx)` DIRECTLY.
Only Phase 8's registration tests route through `families.FAMILIES[FAMILY]`.
Without that split, every behavioural test would depend on the registration and
Phase 8 could not be the last phase it has to be.

---

## Progress

**Phases 1–8 are DONE (T001–T057, T055a).** The sequencing gate OPENED —
`add-family-enumeration-check` archived on `main` at `f027d3b3` and this branch
merged it — so the registration landed with § 2.1's block written against canon.
T051a is the one box that will never be ticked, and its line says why.

Phase 9 is done except T063's PR body (written) and the PR itself (deliberately
not opened). `tests/doc-health` was 980 at T001's baseline and is **1077** now,
+97. The measured movement lives in `plan.md` § Predicted movement — the single
home for it — and the mutation round found THREE missing tests, which are now in
the file.

## Phase 1: Setup

**Purpose**: record the before-state, and land the module's skeleton behind a
test that fails on its absence.

- [x] T001 Record the baseline in this file, as a checked-off note: `python3 -m pytest tests/doc-health -q | tail -3` count, `python3 -m pytest tests -q | tail -3` count, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` result, taken BEFORE any edit. Without the before-number the added tests are an assertion rather than a delta (SC-007).
- [x] T002 [TEST] Create `tests/doc-health/test_modified_block_currency.py` with the module docstring the house style requires (what is under test and in which directions) and the first pins: `_LAUNCH_SEVERITY is WARNING`, `_RESOLUTION_SEVERITY is WARNING`, `_LEDGER_SEVERITY is INFO`, `FAMILY == "modified-block-currency"`. RED: `ImportError`. Test names: `test_the_three_launch_severities_are_named_apart`, `test_the_family_id_is_the_registry_id`.
- [x] T003 Create `scripts/doc_health/modified_block_currency.py` with the module docstring (what the family answers, why the class is not hypothetical, the three arms, why the launch is advisory in both halves — the shape `promotion_fidelity.py` and `family_enumeration.py` set), `FAMILY`, the three severity constants with the comment recording that § 7.2's flip moves `_LAUNCH_SEVERITY` ALONE (O8), `DELTA_GLOB`, `CANON_TEMPLATE`, `_ACTION`. T002 goes green.

**Checkpoint**: the module exists, has no behaviour, and its launch posture is pinned.

---

## Phase 2: Foundational — the derivation and the marker grammar

**⚠️ BLOCKS EVERY USER STORY.** All three arms read these functions. Contracts:
[unit-derivation.md](./contracts/unit-derivation.md),
[marker-parser.md](./contracts/marker-parser.md). Realizes packet § 2.2, § 2.3
and the parsing half of § 2.5.

- [x] T004 [TEST] `test_normalization_collapses_whitespace_and_nothing_else`, `test_unit_normalization_is_not_the_promotion_fidelity_spelling` (asserts `normalize("A") != promotion_fidelity.norm("A")` and says why in the docstring — `dh:84-90` forbids normalization beyond whitespace). RED.
- [x] T005 Implement `normalize(text)` in `scripts/doc_health/modified_block_currency.py`, with the docstring recording the deliberate divergence from `promotion_fidelity.norm` (research R3).
- [x] T006 [TEST] `test_masking_preserves_length`, `test_a_period_inside_a_backticked_token_never_ends_a_sentence`, `test_a_longer_fence_masks_its_inner_backticks`, `test_an_unterminated_backtick_run_masks_nothing`. RED.
- [x] T007 Implement `mask_code_spans(text)` — CommonMark run matching, length preserved, filler that is neither whitespace nor a terminator (research R4).
- [x] T008 [TEST] `test_sentences_split_on_a_terminator_followed_by_whitespace`, `test_the_terminator_stays_with_its_sentence`, `test_a_period_with_no_following_whitespace_is_not_a_boundary`, `test_boundaries_are_computed_on_the_mask_and_sliced_from_the_original`. RED.
- [x] T009 Implement `split_sentences(paragraph)`.
- [x] T010 [TEST] `test_code_spans_extract_in_document_order`, `test_a_unit_containing_backticks_is_extracted_whole_under_a_longer_fence`, `test_one_space_each_side_is_stripped_per_commonmark`. RED. Names the mutation `` `([^`]*)` `` that must break it.
- [x] T011 Implement `extract_code_spans(text)`.
- [x] T012 [TEST] `test_both_marker_forms_parse`, `test_a_marker_wrapped_across_lines_is_one_marker`, `test_a_marker_with_no_reason_is_still_a_marker`, `test_a_quoted_marker_template_is_not_a_marker`, `test_a_non_iso_date_is_not_a_marker`, `test_a_missing_closing_colon_is_not_a_marker`, `test_the_merge_destination_is_not_a_named_unit`, `test_a_dated_bold_note_that_is_not_a_reserved_form_parses_as_no_marker`, and the FENCED-BLOCK case ruled 2026-08-27 (N7): `test_the_deltas_own_fenced_marker_examples_never_reach_the_parser` — the two written-out example lines at `add-modified-block-currency-check/specs/doc-health/spec.md`:187-190 are COMPLETE markers (real change id, real ISO date, closing colon) and live inside a fenced block that PROMOTES INTO CANON; the test asserts `parse_marker` is form-blind on them in isolation AND that `fenced_regions` keeps them from ever being offered. RED. The quoted-template test uses THIS PACKET'S OWN delta prose, which promotes into canon (`dh:125-133`).
- [x] T013 Implement `parse_marker(paragraph)` and the `Marker` structure, with the change-id read as a TOKEN and not resolved against the tree (O7 / research R7); and `fenced_regions(lines)`, the fence scanner ruled 2026-08-27 (N7) whose output is step 0 of `derive_units` — three-or-more backticks or tildes, closed by a run at least as long, an unclosed fence running to the end of the block.
- [x] T014 [TEST] `test_a_dated_bold_note_is_recognized_by_form`, `test_an_undated_bold_lead_is_not_a_note`, `test_the_real_notes_this_corpus_carries_are_each_one_unit` — the last one reads `openspec/specs/doc-health/spec.md`'s own notes, so O6's predicate is MEASURED against the corpus rather than asserted. RED.
- [x] T015 Implement `is_dated_bold_note(paragraph)`, documented as the one rule the delta does not write (O6), evaluated only after `parse_marker` returns None.
- [x] T016 [TEST] `test_body_and_scenario_regions_split_at_the_first_scenario_heading`, `test_a_body_bullet_is_one_unit_with_its_marker_stripped`, `test_a_dated_note_is_one_unit_not_three`, `test_a_scenario_heading_is_one_title_unit`, `test_a_scenario_bullet_records_its_owning_scenario`, `test_prose_under_a_scenario_heading_is_a_body_unit` (decision O9 — population 2 in this corpus; without it a block could move an obligation into scenario prose and neither carriage arm would see it), `test_a_marker_paragraph_yields_no_unit_in_either_document`, `test_fenced_block_lines_are_neither_units_nor_markers` (N7 — the same :187-190 example, now through the derivation). RED.
- [x] T017 Implement `derive_units(lines) -> (units, markers)` and the `Unit` structure — the SINGLE derivation both documents go through (research R2, R5, R9).
- [x] T018 [TEST] `test_a_canon_unit_is_carried_only_by_a_unit_of_the_same_kind`, `test_a_block_unit_containing_canon_s_unit_does_not_carry_it` (the #351 widening mechanism — the case a containment rule loses), `test_case_is_significant`, `test_a_trailing_period_difference_is_not_forgiven` (FR-010's punctuation half — the normalization `promotion_fidelity.norm`'s docstring names as the one it refuses), `test_a_rewrapped_paragraph_is_carried`. RED for the first three; the last names its mutation.
- [x] T019 Implement `carried(canon_units, block_units)` — `(kind, key)` equality, nothing else.
- [x] T020 [TEST] `test_active_deltas_are_discovered_and_the_archive_is_excluded`, `test_a_draft_change_is_read_exactly_like_a_ratified_one`, `test_the_promoted_reader_returns_bodies_and_bullets_not_just_titles`, `test_the_delta_side_reads_through_promotion_fidelity_parse_delta`, `test_a_live_main_basis_request_changes_nothing` — FR-002's second half, made BEHAVIOURAL per N3: call the family twice over one fixture, once with a plain ctx and once with a ctx carrying `promotion_fidelity_basis="live-main"` and a `FakeGit` whose `ref_trees` hold DIFFERENT text, and assert the findings are identical — the family reads the checkout and the option cannot reach it. Plus `test_the_family_publishes_no_basis_note` (absent from `families.FAMILY_NOTES`). RED.
- [x] T021 Implement `active_blocks(root)`, `parse_spec_requirements(text)` and the cached `promoted(root, capability)`, importing `promotion_fidelity.parse_delta`, `norm`, `declared_standing` and the heading regexes rather than re-spelling any of them (research R1, R2).

**Checkpoint**: two documents can be read and reduced to units; the marker grammar parses. No arm exists yet.

---

## Phase 3: User Story 1 — the omitted scenario is reported (Priority: P1) 🎯 MVP

**Goal**: the arm that carries the family's gate. Realizes packet § 2.4's first
arm and delta scenario "An active block drops a scenario the requirement keeps".

**Independent Test**: one fixture, one lossy block, every omitted title named —
and no other arm built.

- [x] T022 [P] [US1] Create `tests/doc-health/fixtures/modified-block-currency/alphaFactory/` — a promoted `openspec/specs/<cap>/spec.md` requirement with eight scenarios, and an active change whose MODIFIED block restates one, with the change's own ADDED requirement bringing seven so the FILE-LEVEL scenario count does not move (the #329 shape at F1 grain; F2's § 3.2 owns the full reconstruction).
- [x] T023 [TEST] [US1] `test_a_block_that_drops_scenarios_names_every_one_of_them` — asserts the omitted titles BY NAME and the promoted spec named in the rule, never a bare count; `test_the_finding_lands_on_the_active_delta_s_own_path`; `test_the_scenario_arm_is_a_warning`. RED.
- [x] T024 [US1] Implement `fam_modified_block_currency(ctx)`'s spine — iterate repos, blocks, resolve against canon by `norm(title)`, and `_arm_titles(...)` at `_LAUNCH_SEVERITY`, one finding per requirement listing every omitted title in canon order, in full (no three-item truncation: the list is what a reader acts on).
- [x] T025 [TEST] [US1] `test_a_scenario_complete_block_that_rewraps_every_paragraph_is_quiet` (mutation: `normalize` becomes identity), `test_a_run_configured_fail_on_error_is_unaffected` — asserts the finding list is NON-EMPTY first and only then that no severity is in `{CRITICAL, ERROR}` (N4: the assertion is vacuous on an empty list, which is exactly what a broken discovery returns), `test_the_file_level_scenario_count_is_not_what_the_family_reads`. Negatives — each names its mutation.

**Checkpoint**: US1 is independently valuable. A packet author already cannot silently delete a titled scenario.

---

## Phase 4: User Story 2 — the carriage ledger (Priority: P2)

**Goal**: the clause-granular half. Realizes packet § 2.4's second arm and delta
scenarios "A block does not carry canon's body text or a scenario bullet" and
"A block retitles a scenario and drops its bullets".

- [x] T026 [P] [US2] Extend the `modified-block-currency` fixture with a block that WIDENS one canon bullet at both ends, drops two body sentences, and moves one bullet verbatim under a different scenario title.
- [x] T027 [TEST] [US2] `test_uncarried_body_units_and_bullets_are_one_info_finding_per_requirement` (asserts the unit list and that exactly ONE finding lands per requirement), `test_the_ledger_finding_does_not_assert_intent` (the hedge text is present), `test_the_widened_bullet_leaves_canon_s_bullet_uncarried`, `test_a_bullet_moved_under_a_different_scenario_is_carried`. RED for the first three.
- [x] T028 [US2] Implement `_arm_ledger(...)` at `_LEDGER_SEVERITY` — body units plus scenario bullets, bullets pooled across the whole block, at most one finding per requirement, deterministic elision of long unit texts (document order, fixed cut, count always stated in full).
- [x] T029 [TEST] [US2] `test_a_tokenized_body_reports_the_note_once_not_three_times`, `test_no_ledger_unit_boundary_falls_inside_a_backticked_span` — the tokenization behaviour end-to-end through the family rather than through `derive_units` alone, so a wiring regression cannot hide behind a green unit test. RED (the end-to-end path is new).

**Checkpoint**: US1 + US2 together reproduce the shape of both historical true positives at F1 grain.

---

## Phase 5: User Story 3 — the declaration (Priority: P2)

**Goal**: the author's instrument. Realizes packet § 2.5's suppression half and
delta scenarios "A deletion is declared by marker", "A genuinely removed
scenario title carries its bullets with it", "A removal marker is used where the
block adds a replacement scenario", "A marker names a unit the block still
carries".

- [x] T030 [P] [US3] Create `tests/doc-health/fixtures/modified-block-currency-markers/<repo>/` — five blocks in one tree: a valid `Removed from canon` naming two of three absent units; a marker naming a unit the block still restates; a GENUINE removal (marker names a scenario title, block adds no new title); the COMBINATION (marker names the title AND the block adds a replacement carrying two of four bullets); a valid `Merged into` whose destination is present.
- [x] T031 [TEST] [US3] `test_a_marker_suppresses_exactly_the_units_it_names`, `test_an_unnamed_sibling_unit_stays_reported`, `test_a_marker_naming_a_carried_unit_emits_one_info_finding` — the FOURTH FINDING CLASS ruled 2026-08-27 (B6): assert ONE finding at `_LEDGER_SEVERITY` naming the marker's change id, its date and the unit it wrongly names, and assert the finding does NOT carry the ledger's hedge (a marker naming a carried unit is wrong with certainty). RED.
- [x] T032 [US3] Implement `suppression(...)`, `marker_defects(...)` AND its emitter `_arm_marker_defects(...)` — name resolution against canon units of any kind, the three-way table in [marker-parser.md](./contracts/marker-parser.md), and the deliberate non-obligation for a name that resolves to no canon unit (research R10). **The emitter is not optional**: B6 found the first cut of this plan giving the defect a producer and no consumer, which is how a `SHALL itself be reported` ends up realized in a docstring.
- [x] T033 [TEST] [US3] `test_a_genuinely_removed_scenario_title_carries_its_bullets`, `test_a_surviving_bullet_of_a_removed_scenario_is_carried_and_reported_nowhere`. RED.
- [x] T034 [US3] Implement the genuine-removal extension — scenario-title suppression reaching that scenario's canon bullets, gated on the block adding NO scenario title canon does not carry.
- [x] T035 [TEST] [US3] `test_a_removal_marker_plus_a_replacement_scenario_still_reports_the_dropped_bullets` — the COMBINATION case (packet § 3.3a's shape at F1 grain), asserted beside the genuine-removal case so the two branches are pinned against each other. RED, and it must FAIL under any scenario-paired bullet comparison.
- [x] T036 [US3] Implement the retitle gate (FR-020) — where the block adds a new scenario title, the extension does not apply at all.
- [x] T037 [TEST] [US3] `test_the_merge_destination_is_never_read_as_a_named_unit_end_to_end`, `test_a_promoted_marker_is_not_a_carriage_unit`, `test_a_prose_dated_note_declares_nothing` — the guard that canon's own restoration notes are never read as declarations of deletion. Negatives with named mutations; the second is RED (the canon-side exclusion path is new).

**Checkpoint**: every finding US1 and US2 raise can be discharged by one line, and a declaration that does not describe the block earns its own finding.

---

## Phase 6: User Story 4 — resolution and ordering (Priority: P3)

**Goal**: compare the right thing, or say why you cannot. Realizes packet § 2.6
and § 2.7 and delta scenarios "A change renames a requirement and modifies it in
one delta", "A MODIFIED title resolves to an active sibling's addition", "A
MODIFIED title resolves to nothing at all", "Two active changes modify one
requirement and one declares", "Two active ratified changes modify one
requirement and the ordering is undeclared".

- [x] T038 [P] [US4] Create `tests/doc-health/fixtures/modified-block-currency-resolution/<repo>/` — a change carrying both `## RENAMED Requirements` and a MODIFIED block under the NEW title; a MODIFIED title an active sibling ADDS; a MODIFIED title nothing carries.
- [x] T039 [TEST] [US4] `test_a_change_s_own_rename_resolves_first_and_the_arms_compare_the_old_name` (asserts the arms RAN — a ledger finding against canon under the old title — not merely that nothing was reported), `test_a_title_pending_on_a_sibling_s_addition_is_quiet`, `test_a_title_resolving_to_nothing_is_reported`, `test_a_capability_with_no_promoted_spec_at_all_resolves_to_nothing` — a DISTINCT code path (`promoted()` returns None rather than a dict without the title), and the edge case spec.md names. RED.
- [x] T040 [US4] Implement `resolve(block, canon, sibling_titles)` — the three-step order, then the finding at `_RESOLUTION_SEVERITY`.
- [x] T041 [P] [US4] Create `tests/doc-health/fixtures/modified-block-currency-two-writers/<repo>/` — two active RATIFIED changes MODIFYING one promoted requirement, in four arrangements: exactly one declaring and carrying the sibling's addition; exactly one declaring and NOT carrying it; neither declaring; both declaring. Plus a sibling id that occurs only inside a LONGER id, an UNRATIFIED sibling, and a MODIFIED-over-a-sibling's-ADDED pair (for T042's B4 pin).
- [x] T042 [TEST] [US4] The ordering pins, with the two rulings of 2026-08-27 built in. `test_the_declaring_block_is_measured_against_the_sibling_s_outcome`; `test_the_declaring_block_missing_the_sibling_s_addition_is_reported_by_the_LEDGER_not_by_a_second_finding` — **ruling B3: a declaration is BASIS SUBSTITUTION ONLY**, so assert the missing addition appears in the `info` ledger finding AND that the resolution arm emitted nothing for it, because a second `warning` would report the same units the ledger already reports; `test_neither_declaring_fires_against_both_blocks`; `test_both_declaring_fires`; `test_a_change_id_inside_a_longer_id_declares_nothing`; `test_an_unratified_sibling_creates_no_declaration_obligation`; `test_a_group_of_three_writers_with_one_declaration_is_evaluated_over_the_group` (A4 / R11 — population zero, so the fixture has to be built); `test_the_sibling_s_outcome_is_canon_with_the_sibling_s_MODIFIED_block_applied_and_nothing_else` — **ruling B4**: assert that a MODIFIED-over-a-sibling's-ADDED title is compared against NOTHING and reported nowhere, because `dh:278-280` calls it pending rather than absent, and that no basis is synthesized from the sibling's ADDED text. RED.
- [x] T043 [US4] Implement `declares(...)` (importing `duplicate_packet._mention` — the matcher the delta names by reference, whose `[\w-]` boundary makes a bare path citation count as a declaration; accepted, see O10/N8), `writer_sets(blocks)` and `order(writer_set)`, evaluated over the GROUP (research R11 / A4). The resolution arm emits EXACTLY TWO things and nothing else (ruling B3): an unresolved title, and an undeclared or mutual ordering.
- [x] T044 [TEST] [US4] `test_no_date_folder_or_created_field_decides_the_ordering` — a pair constructed to order ONE way by `created:` date and the OTHER way by declaration, asserting the declaration wins. This is the test that stops the withdrawn date reading creeping back (packet § 7.3). RED under a date-ordered build; it is the pin, so write it even though the code never had that reading.

**Checkpoint**: the family compares the right document in every shape the corpus contains, and reports the two shapes where no reader could tell.

---

## Phase 7: Cross-cutting family behaviours

**Purpose**: the three behaviours every arm shares. Realizes packet § 2.8 and
the delta's disposition and skip scenarios.

- [x] T045 [TEST] `test_a_disposition_naming_this_family_suppresses_the_path`, `test_an_entry_narrowed_by_requirement_suppresses_only_that_requirement`, `test_an_uncited_entry_disposes_nothing`, `test_a_disposition_for_another_family_disposes_nothing`, `test_a_single_repo_run_has_no_aggregation_root_and_applies_no_disposition` (the inherited caveat, pinned so the self-gate's silence is understood rather than discovered) — written on `test_promotion_fidelity.py`'s `tmp_path` + `agg_root` pattern. RED.
- [x] T046 Wire `promotion_fidelity.load_dispositions(ctx, FAMILY)` and `promotion_fidelity.disposed(...)` into the entry point. **Write no reader** (O4 / research R12); `promotion_fidelity.py` must show no diff.
- [x] T047 [TEST] `test_a_scope_with_no_changes_directory_skips_with_its_reason`, `test_a_scope_with_active_changes_but_no_modified_block_is_not_skipped_and_reports_nothing` — the two states canon keeps apart ("cannot run", not "found nothing"). RED for the skip arm.
- [x] T048 Implement the skip arm and the quiet arm as distinct returns (`Skip(...)` vs `[]`).
- [x] T049 [TEST] `test_two_runs_agree_byte_for_byte` (findings and ordering, in the `test_suite.py::test_determinism_identical_runs` shape), `test_the_family_returns_its_findings_sorted`. RED for the sort assertion if the entry point does not yet sort.
- [x] T050 Sort the family's own return before handing it back, so a `--family` run is stable independently of `runner.run_suite`'s global sort.

**Checkpoint**: the module is behaviourally complete and still unregistered.

---

## Phase 8: User Story 5 — registration and the enumeration block (Priority: P1) — **GATED**

**Goal**: the acceptance condition of the whole feature. Realizes packet § 2.1,
§ 2.9 and § 2.10.

**⛔ THIS PHASE IS GATED AND CANNOT START YET. RULED 2026-08-27, option (a):
`add-family-enumeration-check` archives FIRST, as a separate parallel PR.**

`fam_family_enumeration` checks EVERY active delta's restatement of
"Deterministic check families" against the LIVE registry, independently
(`family_enumeration.py`:412-437). Registering a twenty-second family while that
change is active therefore emits three findings against THAT packet's delta
path — an omitted family name and two stale numerals — and a block inside THIS
change's delta cannot clear them, because each active delta is checked on its
own and this change has no standing to edit another ratified packet's text.
Measured on this branch: **0 findings at 21 registered, 3 at 22.** The packet's
§ 2.1 is unimplementable as written; this is the ruled sequencing that makes it
implementable.

**Entry condition**: that change archived on `main`, and `git merge origin/main`
run on this branch. **If it is delayed, F1 STOPS at the end of phase 7 and
waits** (N2) — a complete, tested, unregistered module is a coherent reviewable
state; a half-landed registration is not.

**T052–T056 plus T055a are ONE COMMIT** (O2 / packet § 2.1, which says so in
capitals).

- [x] T051 [TEST] [US5] Add the registration pins to `tests/doc-health/test_modified_block_currency.py`: `test_the_family_is_registered_and_reachable_through_the_registry` (`FAMILIES[FAMILY]` resolves and runs), `test_the_family_is_absent_from_family_resolution_at_launch` (NON-VACUOUS only after registration — assert membership in `FAMILIES` in the SAME test, or the absence assertion passes on an empty registry and proves nothing), `test_the_reporting_list_mirrors_the_registry` (`set(FAMILY_IDS) == set(FAMILIES)`). RED.
- [~] T051a [TEST] [US5] **NOT WRITTEN, and the reason is the best one: the gate it existed to hold OPENED.** `add-family-enumeration-check` archived on `main` (`f027d3b3`) while phase 6 was in flight, so the condition this test would assert — three findings against that packet's ACTIVE delta — can no longer be constructed without un-archiving another change, and a test asserting a condition that cannot recur is a test nobody can read. The measurement it was to encode is recorded in `plan.md` § Sequencing gate and in the review residue. Original text: `test_registering_a_22nd_family_while_the_enumeration_change_is_active_reds_that_packet` — the GATE, asserted rather than remembered: monkeypatch `family_enumeration._registry` to append this family's id, run `fam_family_enumeration` against the repository root, and assert three findings all on `openspec/changes/add-family-enumeration-check/specs/doc-health/spec.md`. **This test is deleted in the same commit that registers the family**, because once that change has archived the condition it describes cannot recur — and a test asserting a condition that cannot recur is a test nobody can read. Its purpose is to hold the gate while phases 1–7 are in flight.
- [x] T052 [US5] Write the owed `## MODIFIED Requirements` block on "Deterministic check families" into `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`, relative to **CANON** — which after the archive IS `add-family-enumeration-check`'s promoted outcome, so there is no second authority to reconcile and no two-writers instance is created. Move exactly six things: `twenty-one` → `twenty-two`; `modified-block currency` appended to the enumeration; `Four of the twenty-one` → `Four of the twenty-two`; `the other seventeen families` → `the other eighteen families`; one new sentence declaring that this family reads active change deltas and promoted specs and therefore takes neither the governed corpus nor the lifecycle scan set (in the shape the four preceding families' sentences use); and one new `AND` bullet in `A run executes the check families`. **Restate all EIGHT scenarios, named here so they are not counted (N1)**: `A run executes the check families`, `Lifecycle conformance checks fire`, `A register carries staged status`, `Drift checks fire`, `Catalog conformance checks fire`, `Routing conformance checks fire`, `Origin conformance checks fire`, `Roster composition is checked across domains`. **Carry the THREE dated bold notes VERBATIM** — at `add-family-enumeration-check/specs/doc-health/spec.md`:48 (`CORRECTED 2026-08-25 ON BRETT'S RULING`), :71 (`THE ORDERING DEPENDENCY RESOLVED`) and :86 (`FOURTH RESTATEMENT, AND THE FIRST ONE A CHECK VERIFIED`). Each is ONE undivided body unit under this family's own derivation, so dropping one would make this change commit the defect it exists to report.
- [x] T053 [US5] Register in `scripts/doc_health/families.py`: the module name added to the existing `from . import (…)` block, one `FAMILIES` entry, one comment recording the deliberate `FAMILY_RESOLUTION` absence in the shape the four preceding families use, and the module docstring's owner list extended to name the twenty-second family.
- [x] T054 [US5] Register in `scripts/doc_health/__init__.py`: one `FAMILY_IDS` entry with the twenty-second-family comment, so the family gets its own report section. Add NO `ALIASES` entry to `family_enumeration.py` — `modified-block currency` normalizes mechanically, and `test_every_alias_is_load_bearing` fails on an alias that is not needed.
- [x] T055 [US5] Classify the family in `tests/doc-health/test_lifecycle_scan_set.py`: add `"modified-block-currency"` to `NON_READERS` with its reason, move the `len(NON_READERS) == len(FAMILIES) - 4 == 17` literal to `18`, and add the named `in NON_READERS` assertion beside the four that exist. Confirm the module contains no `_lifecycle_scope(` call, which `test_the_reader_list_is_structural_not_incidental` asserts package-wide.
- [x] T055a [US5] **THE ENUMERATION COLLATERAL (ruling B2).** Move the numeral and family-name assertions in `tests/doc-health/test_family_enumeration.py` (assertion sites :65, :67, :75, :78, :79, :81, :118, :128, :136, :164, :178) and the enumeration text in the seven `tests/doc-health/fixtures/family-enumeration-*/` fixture specs from twenty-one to twenty-two. These files are `add-family-enumeration-check`'s OWN declared code surface (`openspec/changes/add-family-enumeration-check/proposal.md`:2 names `tests/doc-health/test_family_enumeration.py`, `tests/doc-health/fixtures/family-enumeration*/` and `tests/doc-health/test_lifecycle_scan_set.py`), so editing them is not scope creep: this change moves the registry they assert against and they have no other way to hear about it. A registration that moves the registry without moving these reds that family's suite.
- [x] T056 [US5] Verify and record, then COMMIT T052–T056 and T055a together, DELETING T051a's gate test in the same commit: `python3 -m pytest tests/doc-health/test_family_enumeration.py -q` green (`fam_family_enumeration` reads 0 against the tree); `python3 -m pytest tests/doc-health -q` green; the per-requirement scenario count 8 → 8 in the commit message; and the eight restated scenarios verified by DIFF against canon rather than by eye.
- [x] T057 [TEST] [US5] `test_the_family_reads_its_own_packet_s_delta` — the family's discovery finds this change's own doc-health delta among the blocks examined, and the carriage-ledger finding § 2.1's block draws against itself is PRESENT. Assert it as expected (see plan.md § Predicted movement, the single home for the figure), never suppressed and never dispositioned: a disposition here would hide the evidence that the family reads its own packet. (F3 § 4.1/§ 4.2 owns the full self-gate; this is the F1 hook it needs.)

**Checkpoint**: twenty-two families are registered, the report has a section for the new one, and canon's enumeration and the code registry agree.

---

## Phase 9: Gates, mutation, adversarial review, hand-off

- [x] T058 The count-delta evidence: `python3 -m pytest tests/doc-health -q` green, recorded against T001's baseline so the added tests are visible as a delta (SC-007). **This single-directory run IS the evidence (ruling N12). `python3 -m pytest tests` — the whole tree — is out-of-band and is NEVER run from a worktree: it drives live Postgres containers.**
- [x] T059 Scope guard, mechanically: `git diff --stat origin/main...HEAD` shows edits ONLY to this exact allowlist — `scripts/doc_health/modified_block_currency.py`, `tests/doc-health/test_modified_block_currency.py`, `tests/doc-health/fixtures/modified-block-currency*/`, `scripts/doc_health/families.py`, `scripts/doc_health/__init__.py`, `tests/doc-health/test_lifecycle_scan_set.py`, **`tests/doc-health/test_family_enumeration.py`**, **`tests/doc-health/fixtures/family-enumeration-*/` (7 dirs)**, `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`, and `specs/019-modified-block-currency-family/`. The two bold entries are ruling B2's correction and are in scope by citation: `add-family-enumeration-check/proposal.md`:2 declares them as that change's own surface, and this change moves the registry they assert against. `promotion_fidelity.py`, `duplicate_packet.py`, `report.py`, `.github/workflows/**` and every threshold show NO diff (FR-030 / O5). `python3 -m pytest tests/doc-health/test_promotion_fidelity.py tests/doc-health/test_duplicate_packet.py -q` green — promotion fidelity's 59 tests unchanged.
- [x] T060 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, count recorded — run from the repository root, per the aggregation CLAUDE.md's authoring note.
- [x] T061 THE MUTATION ROUND. Apply each mutation in `quickstart.md`'s table one at a time, confirm at least one NAMED test fails for each, and revert. A surviving mutant is a missing test and the fix is the test, not the note. This is the RED proof for every negative assertion in this list.
- [x] T062 ADVERSARIAL REVIEW PASS, before the PR: re-read the ratified delta line by line against the implementation and report where they diverge; hunt specifically for (a) a false NEGATIVE the arms cannot see, (b) a normalization that crept beyond whitespace, (c) a marker path that suppresses more than it names, (d) a vacuous test — one that passes against a stubbed-out module, and (e) any read of a date, folder name or `created:` field. Record every finding and its disposition in `plan.md` § Analyze residue.
- [x] T063 Draft the PR body in this feature directory (`pr-body.md`), naming: the packet and its ratification, the boxes closed (§ 2.1–2.10), the predicted report movement and that F3 asserts it, the statement that this change does NOT close #330 (packet § 7.1 requires the PR to say so), and the five orchestrator decisions plus O6–O8 as still-flagged. **Do not open the PR** — the plan gets a review pass first.
- [x] T064 Hand-off notes for the successors — see § Hand-off below.

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (Setup)**: no dependencies.
- **Phase 2 (Foundational)**: depends on Phase 1. **BLOCKS Phases 3–8.** Within it the order is forced: `normalize` → `mask_code_spans` → `split_sentences`; `extract_code_spans` → `parse_marker` → `is_dated_bold_note` → `derive_units` (the marker test must run BEFORE the note test, or every marker is swallowed as a note — research R5); `derive_units` → `carried`; readers last.
- **Phase 3 (US1)**: depends on Phase 2. Delivers the MVP.
- **Phase 4 (US2)**: depends on Phase 2; independent of Phase 3 in code, sequenced after it by value.
- **Phase 5 (US3)**: depends on Phases 3 AND 4 — suppression is only observable against findings that exist.
- **Phase 6 (US4)**: depends on Phase 2; independent of Phases 3–5.
- **Phase 7**: depends on the entry point existing (Phase 3 onward).
- **Phase 8 (US5)**: depends on EVERYTHING, **and on an external event** — `add-family-enumeration-check` archiving on `main` (ruling B1). Its T052–T056 + T055a commit is atomic, and it deletes T051a's gate test.
- **Phase 9**: depends on Phase 8.

### Story dependencies

- US1 (P1) → after Phase 2. Independently testable and independently valuable.
- US2 (P2) → after Phase 2. Independently testable.
- US3 (P2) → after US1 and US2 (it silences their findings).
- US4 (P3) → after Phase 2. Independently testable.
- US5 (P1) → last. It is the acceptance condition, not an increment.

### Parallel opportunities

- T022, T026, T030, T038, T041 — fixture trees, different directories, no shared file. All `[P]`.
- Phases 3/4 and Phase 6 can proceed in parallel after Phase 2 (different arms, different functions, one shared file — so serialize the WRITES to `modified_block_currency.py` or expect a conflict).
- Phase 2's pairs are NOT parallel, and for two different reasons worth keeping
  apart: `normalize` → `mask_code_spans` → `split_sentences` and
  `extract_code_spans` → `parse_marker` → `is_dated_bold_note` → `derive_units`
  → `carried` are genuine dependency chains, while the two chains are
  independent of each other and serialize only because they write ONE file.
- Nothing in Phase 8 is parallel: it is one commit.

## Implementation Strategy

**MVP = Phase 1 + Phase 2 + Phase 3.** At that point a packet author cannot
silently delete a titled scenario, which is the arm that carries the gate and
two of the nine items of the instance that produced #357.

**Then**: Phase 4 (the other seven items, advisory) → Phase 5 (so the findings
can be discharged) → Phase 6 (structural protection, zero population today) →
Phase 7 → Phase 8 (registration, atomic) → Phase 9 (gates, mutation,
adversarial review).

**Never**: split Phase 8's commit, and never start Phase 8 before the gate
opens. Either half of the commit alone reds a gate — the registration half
leaves canon naming a set the registry contradicts, and the block half reds
`test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves`.
And starting the phase early reds that same test on ANOTHER packet's delta path,
which nothing in this change can clear: measured 0 findings at 21 registered, 3
at 22.

## Traceability: every requirement to its tasks

Added after the analyze pass, which found the task-to-requirement mapping was
inferable but not written down — and an inferable mapping is one a later reader
re-infers differently.

| requirement | tasks | requirement | tasks |
| --- | --- | --- | --- |
| FR-001 read every active change | T020, T021 | FR-017 destination not a unit | T012, T013, T037 |
| FR-002 checked-out tree only | T020, T021 | FR-018 suppress only named+absent, + the marker-defect CLASS | T031, T032 |
| FR-003 finding path + spec named | T023, T024 | FR-019 genuine-removal extension | T033, T034 |
| FR-004 backtick masking | T006, T007 | FR-020 retitle gate | T035, T036 |
| FR-005 body units | T008–T017 | FR-021 prose note declares nothing | T037 |
| FR-006 scenario units | T016, T017 | FR-022 dispositions, reused reader | T045, T046 |
| FR-007 marker is no unit | T016, T017, T037 | FR-023 skip vs quiet | T047, T048 |
| FR-008 same-kind exact | T018, T019 | FR-024 severities + resolution absence | T002, T003, T051 |
| FR-009 containment forbidden | T018, T019 | FR-025 determinism | T049, T050 |
| FR-010 no similarity/case/punct | T004, T005, T018 | FR-026 FAMILIES + FAMILY_IDS | T053, T054 |
| FR-011 scenario-title arm | T023, T024 | FR-027 scan-set classification | T055 |
| FR-012 carriage ledger | T026–T029 | FR-028 the owed block, same commit | T052, T056 |
| FR-013 title resolution | T038–T040 | FR-029 the self-drawn finding | T057 |
| FR-014 two-writers by declaration, basis substitution ONLY | T041–T044 | FR-030 scope guard | T059 |
| FR-015 marker form anchor | T012, T013 | FR-031 RED-first evidence — **no code surface** (a process requirement, discharged by the `[TEST]` pairing and the mutation round rather than by a function) | every `[TEST]` task, T061 |
| FR-016 code spans + optional reason | T010–T013 | FR-028a the block against canon | T052, T056 |
| FR-028 the sequencing gate | T051a, T056 | FR-028b enumeration collateral | T055a |

| success criterion | tasks |
| --- | --- |
| SC-001 the #351 shape | T022, T026, T027 |
| SC-002 the #329 shape | T022, T023, T025 |
| SC-003 the widened bullet | T027 |
| SC-004 re-wrap is quiet | T025 |
| SC-005 one marker line silences exactly its units | T031 |
| SC-006 enumeration reads 0, suite green, one commit (GATED) | T051a, T056 |
| SC-007 test-count delta | T001, T058 |
| SC-008 openspec validate strict | T060 |
| SC-009 no `--fail-on` run reds | T025 |
| SC-010 no surviving mutant | T061 |

## Notes

- 66 tasks (64 plus T051a and T055a, inserted by the adversarial review with
  lettered suffixes so earlier IDs stayed stable); 27 of them `[TEST]` tasks,
  each paired with the task that makes it pass.
- **Phases 1–7 run now. Phase 8 is GATED** on
  `add-family-enumeration-check` archiving (ruling B1) and phase 9 follows it.
  Stopping at the end of phase 7 is a legitimate terminal state for this
  feature if that archive is delayed.
- Task count per story: US1 4, US2 4, US3 8, US4 7, US5 9; Setup 3,
  Foundational 18, Cross-cutting 6, Gates/review 7.
- Every `[TEST]` task names its test functions, because "add tests" is how a
  test file ends up asserting that a module imports.
- Commit after each phase, with explicit pathspecs — this checkout is shared.
  Phase 8 is ONE commit regardless of its five tasks.

## Hand-off to F2, F3 and F4

**What F2 must NOT duplicate.** F1 already carries, with tests: the structural
launch pin in BOTH halves (`test_the_three_launch_severities_are_named_apart`,
`test_the_family_is_absent_from_family_resolution_at_launch` — § 3.11 has
nothing left to add and should say so rather than write a second copy); the full
marker matrix (both forms, the wrapped marker, the optional reason, the quoted
template, the non-ISO date, the missing colon, the non-change-id author, the
longer fence, the destination exemption, the promoted marker, the prose note,
the genuine removal, the survivor, and the retitle COMBINATION); the containment
negative; the tokenization invariant; determinism; and the skip/quiet pair. F2's
remaining value is the two HISTORICAL reconstructions at byte fidelity (§ 3.1,
§ 3.2) — F1's fixtures carry those SHAPES but not the real text — plus whatever
the wider fixture corpus turns up.

**The hooks F3 needs.** `plan.md` § Predicted movement carries the MEASURED
movement (+1 `warning`, +9 `info`, 0 elsewhere) and is the single home for it —
F3 asserts that table and nothing else restates it. The own-packet assertion F3
§ 4.2 wants is live: the family reads
`openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`
and draws exactly one ledger finding naming two body units. Assert it by that
NAMED subject, not by a count, or the test passes vacuously when discovery
breaks.

**The boundary F4 owns**, untouched here: `report.py`'s section rendering, the
action-line wording, and the workflow pin (§ 5.3). F1 emits four distinct
finding classes so F4 can render the one `warning` next to the nine editorial
rows without a reader counting; F1 renders nothing. `.github/workflows/` has no
diff on this branch and must not gain one for this family — the live-`main`
basis belongs to promotion fidelity alone, and
`test_the_promoted_reader_cannot_reach_a_measurement_basis` pins that this
family has no way to consume such an option even if one were passed.

**One thing all three should know.** The mutation round (T061) found THREE
missing tests that twenty-one green tests had not: the `FAMILY_RESOLUTION`
absence was documented in three places and asserted in none; the marker's
change-id group was unpinned because the only quoted-template case also carried a
placeholder date; and the no-basis guarantee was asserted on an outcome rather
than on the reader's signature. Run the round; do not assume a green suite means
a covered rule.
