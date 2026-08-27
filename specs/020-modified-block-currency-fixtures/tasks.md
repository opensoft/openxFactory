---

description: "Task list for 020-modified-block-currency-fixtures (F2 of add-modified-block-currency-check)"
---

# Tasks: the modified-block-currency regression-fixture catalogue

**Input**: design documents in `specs/020-modified-block-currency-fixtures/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/coverage-audit.md`, `contracts/fixture-provenance.md`,
`quickstart.md` — all landed.

**Tests**: **REQUESTED AND MANDATORY.** This feature IS a test catalogue
(FR-025: every test RED-first). Every `[TEST]` task names its test functions
and is paired with the task that makes it pass.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallelizable — different file, no dependency on an incomplete task
- **[TEST]**: a test task, written and shown RED before its pair
- **[Story]**: US1–US5 from `spec.md`; Setup, Foundational and Polish carry none

## Paths

- production module, **read-only**: `scripts/doc_health/modified_block_currency.py`
- F1's tests, **untouched**: `tests/doc-health/test_modified_block_currency.py`
- **the one new test file**: `tests/doc-health/test_modified_block_currency_fixtures.py`
- new fixture trees: `tests/doc-health/fixtures/modified-block-currency-<case>/`

## The RED convention this feature uses

A fixture test written before its fixture fails by ERROR (the directory is
absent), which is a weak RED — it proves nothing about the assertion. So the
two rows that carry the feature use a **two-stage RED**, recorded per task:

1. **stage 1** — test written, fixture absent: the test errors. Records that
   the test runs at all.
2. **stage 2** — fixture built, then PERTURBED in the one way that matters
   (the omitted scenario restored; the widened bullet replaced by canon's;
   the merge marker's bullets carried): the test must FAIL on its ASSERTION.
   Then the perturbation is reverted and the test is green.

Stage 2 is what proves the assertion is load-bearing. It is recorded in the
task's evidence line, and the mutation round (T060) re-runs it mechanically.

---

## Phase 1: Setup

**Purpose**: fix the baseline, prove the base is still valid, and open the one
new file.

- [ ] T001 Record the baseline in this file's § Evidence: `python3 -m pytest tests/doc-health -q | tail -3` (expect `1077 passed`) and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict 2>&1 | tail -3` (record the count). Never run the whole-tree `pytest tests` from this worktree — it needs a live Postgres (orchestrator decision D5).
- [ ] T002 Confirm the audit's base is still valid: `git diff --stat 19e3f6b5 origin/main -- scripts/doc_health/ tests/doc-health/ openspec/specs/doc-health/ openspec/changes/add-modified-block-currency-check/` must be EMPTY. It was empty when `plan.md` was written although `origin/main` had advanced nine commits. **If it is now non-empty, STOP and re-take `contracts/coverage-audit.md` against the moved file before any other task** — an audit of a file that moved is worse than no audit.
- [ ] T003 Create `tests/doc-health/test_modified_block_currency_fixtures.py` with only its module docstring: what the file is (F2's catalogue, not a second copy of F1's rules), the U/F assertion discipline from `data-model.md` § 4, the two reconstructions named with their commits, and an explicit line saying the four synthesized trees are synthesized. Mirrors `test_promotion_fidelity.py`'s habit of declaring a reconstruction as one.
- [ ] T004 [P] Run `quickstart.md` § 6's audit check — every `test_*` name cited in `contracts/coverage-audit.md` exists in `tests/doc-health/test_modified_block_currency.py`. `comm -23` must print nothing. Fix the audit, never the F1 file, if it does.

**Checkpoint**: baseline recorded, base proved unmoved, new file exists and
imports.

---

## Phase 2: Foundational (blocking every story)

**Purpose**: the shared harness in the new file. Everything after this depends
on it.

- [ ] T005 [TEST] Add `test_the_tree_enumeration_finds_every_tree` to `tests/doc-health/test_modified_block_currency_fixtures.py`: `ALL_TREES` must be DERIVED by globbing `conftest.FIXTURES` for `modified-block-currency*` and must contain every such directory on disk, asserted against an independent `os.listdir` read. **RED**: `ALL_TREES` does not exist. *Why derived and not listed: a hardcoded list rots the moment F3 or a later change adds a tree, and rots silently — the determinism and partition invariants would simply stop covering it.*
- [ ] T006 Add `ALL_TREES` and the `_tree(name)` runner helper to `tests/doc-health/test_modified_block_currency_fixtures.py`. `_tree` calls `conftest.make_ctx(name)` and `mbc.fam_modified_block_currency`, returning the finding list (or the `Skip`). T005 green.
- [ ] T007 [TEST] Add `test_every_finding_falls_into_exactly_one_class` to `tests/doc-health/test_modified_block_currency_fixtures.py`: over every tree in `ALL_TREES`, each emitted `Finding` matches exactly ONE of the four classifiers — scenario-title, ledger, marker-defect, resolution/ordering — never two and never zero. **RED**: the classifiers do not exist. *This is decision O2: the invariant that pays for re-spelling F1's `_titles` / `_ledger` in a second file. F1's own `_ledger` docstring records having swept up a resolution finding, which is exactly what this catches.*
- [ ] T008 Add the four finding classifiers to `tests/doc-health/test_modified_block_currency_fixtures.py`, each keyed on the arm's own distinguishing phrase. T007 green. Do NOT import from `test_modified_block_currency.py` — see O2 for why the cross-test-file import is refused.
- [ ] T009 [P] Add `_units(tree, capability, requirement)` to `tests/doc-health/test_modified_block_currency_fixtures.py`: the U-class helper returning `mbc.carried(basis.units, block.units)` for one requirement, so full clause text can be asserted past the ledger's 140-character quote width (`research.md` R4).

**Checkpoint**: `python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q` green with 2 tests; the partition invariant already holds over F1's six trees.

---

## Phase 3: User Story 1 — the two real instances cannot regress silently (P1) 🎯 MVP

**Goal**: freeze #351 and #329 in their real text, with provenance, and assert
what the family says about them.

**Independent test**: build the two trees and run
`python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k "history_351 or history_329"`.
Delivers the regression protection with no other § 3 item present.

### Fixture A — #351 (audit row A1, packet § 3.1)

- [ ] T010 [TEST] [US1] Add `test_the_351_block_omits_exactly_the_two_scenarios_canon_kept` to `tests/doc-health/test_modified_block_currency_fixtures.py`. F-class: one `warning` on the tree, its rule naming `The menu offers a routing rule` AND `A fourth provider verb is proposed` AND `openspec/specs/ideation-dashboard/spec.md`; and asserting that `The intake affordance is submitted as a model` — the block's OWN addition — is NOT named as missing. **RED stage 1**: tree absent.
- [ ] T011 [US1] Build `tests/doc-health/fixtures/modified-block-currency-history-351/intakeFactory/`: `openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md` copied WHOLE from `git show bcfc26a0:openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md` (decision O4); `openspec/specs/ideation-dashboard/spec.md` carrying the requirement `doxBench model catalog and provider boundary` VERBATIM from `git show bcfc26a0:openspec/specs/ideation-dashboard/spec.md` inside a `# ideation-dashboard Specification` / `## Purpose` / `## Requirements` scaffold (decision O3); and `openspec/changes/add-doxchat-model-intake/proposal.md` with a `Status: ratified` line only. T010 green. **RED stage 2**: restore the omitted `The menu offers a routing rule` scenario into the block and confirm T010 fails on its assertion, then revert.
- [ ] T012 [TEST] [P] [US1] Add `test_the_351_ledger_carries_every_clause_the_repair_commit_named` to `tests/doc-health/test_modified_block_currency_fixtures.py`. U-class via `_units`: the returned units' texts must contain each clause `f68261f7` enumerated — the three-member port-surface enumeration, `MUST NOT be added as a fourth provider verb`, the `auto` routing-rule clause, the broker-lane credential clause, and `thread file`. **Assert on TEXT INSIDE the units, never on how many units carry them**: the five clauses lie inside THREE body sentences because the derivation splits on sentences (`research.md` R3), and a count assertion would encode the wrong reading of § 3.1. Also assert F-class that exactly one `info` finding exists for the requirement and that its rule carries the arm's `CANNOT distinguish` hedge.
- [ ] T013 [TEST] [P] [US1] Add `test_the_351_reverted_scenario_line_is_reported` to `tests/doc-health/test_modified_block_currency_fixtures.py`: the bullet `**AND** every loaded editor MUST remain usable` is among the uncarried units — § 3.1's "one reverted scenario line", the narrowing to "the Outline and Document editors" that `f68261f7` records. Assert too that `**WHEN** doxBench runs on the hosted plane` is uncarried (the block drifted to "hosted/read-only plane"), which is the same defect on a WHEN line.
- [ ] T014 [TEST] [P] [US1] Add `test_the_351_widened_bullet_is_reported_although_the_block_contains_it` to `tests/doc-health/test_modified_block_currency_fixtures.py`: canon's `**THEN** the selector MUST show exactly the available catalog entries and their data-handling badges` is uncarried, AND the test asserts IN THE TEST BODY that the block's replacement contains canon's text as a strict prefix (`canon_text in block_text and canon_text != block_text`), so the containment relation is a fact the test checks rather than a claim in a docstring. **This closes audit row A5(b)** — § 3.4's mechanism exercised END TO END through the family, on the real instance, which F1 had only at `carried()` level with synthetic text. It is also § 6.4's single-bullet residue: the finding PR #358's manual `canon ⊆ intake ⊆ B` verification reported. **RED stage 2**: replace the block's bullet with canon's verbatim and confirm the test fails, then revert.
- [ ] T015 [TEST] [P] [US1] Add `test_the_351_findings_land_on_the_delta_path_at_the_right_severities` to `tests/doc-health/test_modified_block_currency_fixtures.py`: every finding's `path` is the active delta's own path, `repo` is `intakeFactory`, `family` is `modified-block-currency`; the scenario-arm finding is `warning` and the ledger finding is `info`; and no finding is `error` or `critical`. Assert the list is NON-EMPTY first — on an empty list every one of those is vacuous, and an empty list is what a broken discovery returns.
- [ ] T016 [US1] Write `tests/doc-health/fixtures/modified-block-currency-history-351/README.md` per `contracts/fixture-provenance.md`'s RECONSTRUCTION template: issue #351; recovered at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`; ended at `f68261f775eb74455a16f7d4d67b576fd76618f0`, merged `87d0b95ae2970733f273cbac15beb847a5b562c5` (PR #358); one runnable `git show` line per file; the scope of the verbatim guarantee (requirement byte-identical, scaffold synthetic); and one line per arm on what the family reports.

### Fixture B — #329 (audit row A2, packet § 3.2)

- [ ] T017 [TEST] [US1] Add `test_the_329_block_omits_all_seven_titles_by_name` to `tests/doc-health/test_modified_block_currency_fixtures.py`. F-class: one `warning` naming, title by title, `Lifecycle conformance checks fire`, `A register carries staged status`, `Drift checks fire`, `Catalog conformance checks fire`, `Routing conformance checks fire`, `Origin conformance checks fire` and `Roster composition is checked across domains`; and asserting `A run executes the check families` — the one the block DID restate — is not named as missing. **RED stage 1**: tree absent.
- [ ] T018 [US1] Build `tests/doc-health/fixtures/modified-block-currency-history-329/driftFactory/`: `openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md` copied WHOLE from `git show d5f447e8:openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md` — **whole is load-bearing here: its `## ADDED Requirements` section is where the seven offsetting scenarios live** (decision O4); `openspec/specs/doc-health/spec.md` carrying `Deterministic check families` VERBATIM from `git show d5f447e8:openspec/specs/doc-health/spec.md` inside the minimal scaffold; and a `proposal.md` with `Status: ratified`. T017 green. **RED stage 2**: restore one omitted scenario into the block and confirm T017 fails on that title, then revert.
- [ ] T019 [TEST] [P] [US1] Add `test_the_329_flat_file_level_count_buys_no_silence` to `tests/doc-health/test_modified_block_currency_fixtures.py`: canon's `Deterministic check families` states 8 scenario titles; the delta FILE contains 8 `#### Scenario:` lines; and the family fires anyway. **This is the one place a count IS the assertion** (`plan.md` D3's stated exception) — asserted precisely because it does NOT predict the outcome, which is why counting could not see this class.
- [ ] T020 [TEST] [P] [US1] Add `test_the_329_ledger_names_canon_s_body_sentences` to `tests/doc-health/test_modified_block_currency_fixtures.py`. U-class: the uncarried units include canon's enumeration sentence (`seventeen check families`) and its `Four of the seventeen` sentence, and include scenario bullets from more than one of the seven dropped scenarios. Add a docstring line noting the coincidence of FORM with the packet's own § 2.1 block (which also fails to carry two body sentences) and stating that this fixture is not evidence about § 2.1.
- [ ] T021 [US1] Write `tests/doc-health/fixtures/modified-block-currency-history-329/README.md` per the RECONSTRUCTION template: issue #329; recovered at `d5f447e89cf619fd12113bcf03525468ece4470d`; ended at `38b548d46153e5e39c855aa105aa77cbb550894a`, merged `b03b9992d519dbfab78fa63a00c5c6e2413ae0e0` (PR #331). **It MUST say that packet § 3.2's phrase "reverted first archive attempt" describes nothing in this history**: the truncated block lived in the ACTIVE change from `e06b066b` through `57c26e1a` and was rewritten scenario-complete inside the archive commit itself, so the recoverable state is the archive's PARENT and no revert exists to find (`research.md` R1).

### Provenance verified mechanically

- [ ] T022 [TEST] [US1] Add `test_the_reconstructed_fixtures_are_the_history_they_claim` to `tests/doc-health/test_modified_block_currency_fixtures.py`: for each reconstruction, `subprocess.run(["git", "-C", str(conftest.REPO_ROOT), "show", f"{sha}:{path}"])` — `REPO_ROOT` is already defined at module level in `tests/doc-health/conftest.py` and compare — the delta files byte-for-byte, the canon files on the extracted `### Requirement:` section. **Follow `test_ideation_readiness.py`'s precedent for the two failure modes**: a checkout that CAN resolve the SHA but disagrees is a defect and FAILS naming the file; a checkout that cannot resolve the SHA at all (a shallow or truncated clone) is a fact about the clone and SKIPS with that reason. Shelling out to `git show` is permitted — the hermeticity guard refuses only `nlm`, `gh` and the session `git push`, and two doc-health tests already run `git` this way.

**Checkpoint**: US1 complete and independently valuable. The two defects that motivated the packet are frozen in their own text, and every assertion is on named units or rule text.

---

## Phase 4: User Story 2 — the audit is checkable, not decorative (P1)

**Goal**: the § 3 → F1-test mapping is committed, complete, and mechanically
verified.

**Independent test**: read `contracts/coverage-audit.md` against § 3 and
against the landed F1 test file; run the two checks below.

- [ ] T023 [US2] Verify `contracts/coverage-audit.md` covers packet § 3 completely: every one of 3.1, 3.2, 3.3, 3.3a, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 appears in the `§ 3 item` column of at least one row, none appears in two rows with conflicting verdicts, and every row carries exactly one verdict. Record the check in this file's § Evidence.
- [ ] T024 [TEST] [P] [US2] Add `test_no_audit_row_cites_a_test_that_does_not_exist` to `tests/doc-health/test_modified_block_currency_fixtures.py`: parse `test_[a-z0-9_]+` names out of `specs/020-modified-block-currency-fixtures/contracts/coverage-audit.md` and assert each is defined in `tests/doc-health/test_modified_block_currency.py`. *An audit citing a renamed or deleted test is an audit that reads as coverage and is not. This makes the citation a live reference rather than prose.*
- [ ] T025 [US2] Add to `contracts/coverage-audit.md` a short closing section recording that rows A1, A2, A3, A5, A6, A7 and A11 were closed by this feature, naming the task ids that closed each — so the audit reads as a completed ledger rather than a plan. Do not restate what the rows already say.
- [ ] T026 [US2] Record in `contracts/coverage-audit.md` the F1 residue this audit found, as a short list with no remediation claimed: F1's `spec.md` SC-003 says "widened at either end" while F1's test widens at the end only (closed here by T014 and T038); F1's `spec.md` § Out of Scope contradicts F1's `tasks.md` hand-off on three items (`research.md` R10); and the hand-off's own claim that "the tokenization invariant" and "the full marker matrix" are done is true only in the narrower form rows A6 and A11 record.

**Checkpoint**: the audit is complete, self-checking, and closed.

---

## Phase 5: User Story 3 — the `Merged into` gut is pinned (P2)

**Goal**: close audit row A3 — the one true hole. A `Merged into` marker names
TITLES only, so a bullet a merge makes redundant must be carried somewhere or
declared as a bullet, one at a time. Nothing tests that today.

**Independent test**: `python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k merge_gut`.

- [ ] T027 [TEST] [US3] Add `test_a_merge_marker_does_not_declare_the_bullets_it_makes_redundant` to `tests/doc-health/test_modified_block_currency_fixtures.py`: on requirement `A merge that guts its source` the ledger reports EXACTLY the two bullets of the superseded four-bullet scenario that the replacement does not carry, by text, and does not report the two it does carry. **RED stage 1**: tree absent.
- [ ] T028 [TEST] [P] [US3] Add `test_the_scenario_arm_is_quiet_because_the_merge_marker_is_valid` to `tests/doc-health/test_modified_block_currency_fixtures.py`: no scenario-title finding for that requirement, and no marker-defect finding either — the marker is well formed and names an absent title, so it declares what it says it declares.
- [ ] T029 [US3] Build `tests/doc-health/fixtures/modified-block-currency-merge-gut/mergeFactory/` with capability `merge-gut`. Canon carries requirement `A merge that guts its source` with a four-bullet scenario `The old shape` plus a second scenario that survives. The block carries a ``**Merged into `The new shape` by add-merge-gut (2026-08-27):** `The old shape` `` marker, the destination scenario `The new shape` present with TWO of the four bullets, and the surviving scenario restated whole. Plus `proposal.md` with `Status: ratified`. T027 and T028 green. **RED stage 2**: add the two missing bullets to `The new shape` and confirm T027 fails, then revert.
- [ ] T030 [TEST] [US3] Add `test_naming_the_redundant_bullets_in_a_removal_marker_silences_them` to `tests/doc-health/test_modified_block_currency_fixtures.py`: on the companion requirement `A merge that declares its redundant bullets`, the ledger reports nothing and no marker defect is emitted. **RED stage 1**: the companion requirement is absent.
- [ ] T031 [US3] Extend `tests/doc-health/fixtures/modified-block-currency-merge-gut/mergeFactory/` with the companion requirement: the same merge shape, PLUS a second marker `**Removed from canon by add-merge-gut (2026-08-27):** <the two bullets as code spans> — <reason>`. One of the two bullets must itself contain a backtick so its code span needs a longer fence, which makes the companion carry § 3.7's fence rule as well. T030 green.
- [ ] T032 [TEST] [US3] Add `test_the_companion_is_quiet_because_of_its_marker_and_not_by_carriage` to `tests/doc-health/test_modified_block_currency_fixtures.py`: rebuild the companion's block text in the test body with the `Removed from canon` marker paragraph DELETED, derive units from it, and assert the two bullets are then reported. *Silence proves nothing unless the thing that causes it is removed and the noise returns. Without this, a build that suppressed the bullets for the wrong reason — or for no reason — passes.*

**Checkpoint**: audit row A3 closed, in both directions, with the silence shown to be caused.

---

## Phase 6: User Story 4 — the derivation gaps, at § 3's own granularity (P2)

**Goal**: close audit rows A5(a), A6 and A7 — containment widened before and at
both ends, the tokenization fixture § 3.5 actually describes, and re-wrap quiet
END TO END. Row A11 (the longer fence through the family) is closed here too.

**Independent test**: `python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k "containment or tokens or rewrap or fence"`.

### Containment at either end (row A5(a), § 3.4)

- [ ] T033 [TEST] [P] [US4] Add `test_a_block_unit_widened_before_canon_s_does_not_carry_it` and `test_a_block_unit_widened_at_both_ends_does_not_carry_it` to `tests/doc-health/test_modified_block_currency_fixtures.py`: `mbc.carried` returns canon's unit in both cases. **RED**: not until they run — these are pure `carried()` assertions and will be green immediately if the implementation is right, so their RED evidence is the MUTATION in T060, not a pre-state. Record that honestly rather than claiming a RED that did not happen. *§ 3.4 and F1's own SC-003 both say "either end"; F1's test widens at the end only, so the prefix and both-ends directions are untested and a one-sided implementation would pass.*

### Tokenization (row A6, § 3.5)

- [ ] T034 [TEST] [US4] Add `test_no_unit_boundary_falls_inside_a_versioned_token` to `tests/doc-health/test_modified_block_currency_fixtures.py`: over the tokens tree, run through the family, no reported unit's text has unbalanced backticks, and none of `contract-v1.45`, `.openspec.yaml` or `promotion_fidelity.py` is split across two reported units. **RED stage 1**: tree absent. *`contract-v1.45` is the token shape F1's fixture lacks — its period sits BETWEEN DIGITS, which is exactly what a naive `\d\.\d` sentence guard would wave through while `.openspec.yaml` and `promotion_fidelity.py` are caught by a leading-dot or word-boundary rule.*
- [ ] T035 [TEST] [P] [US4] Add `test_each_body_bullet_is_its_own_reported_unit` to `tests/doc-health/test_modified_block_currency_fixtures.py`: canon's three-item body bullet list, of which the block carries one, yields exactly two reported `body` units whose texts are the two dropped bullets with their list markers stripped — never one unit carrying both, and never a unit carrying the marker.
- [ ] T036 [TEST] [P] [US4] Add `test_a_note_edited_in_its_third_sentence_is_reported_once` to `tests/doc-health/test_modified_block_currency_fixtures.py`: canon carries a dated bold note of FOUR sentences; the block restates it with the THIRD sentence altered; the ledger reports the note ONCE and no fragment of any other sentence of it appears as a separate unit. **This is § 3.5's last clause and the assertion F1 does not have** — F1's block DROPS its two-sentence note, and dropped is a weaker case than edited: an implementation that split the note into sentences would report a dropped note as N rows but would also report an edited note as 1 row out of N, so only the edit distinguishes "one undivided unit" from "sentence-wise comparison that happened to agree".
- [ ] T037 [US4] Build `tests/doc-health/fixtures/modified-block-currency-tokens/tokenFactory/` with capability `token-cases`: canon's requirement body carrying `` `.openspec.yaml` ``, `` `promotion_fidelity.py` `` and `` `contract-v1.45` `` in sentences (each token's period inside the span), a three-item body bullet list, and a four-sentence dated bold note. The block restates the tokened sentences VERBATIM (so they must not be reported), carries one of the three bullets, and restates the note with its third sentence altered. Plus `proposal.md` with `Status: ratified`. T034, T035, T036 green. **RED stage 2 for T034**: remove the backticks around `contract-v1.45` in BOTH canon and the block, and confirm T034 fails — the version token then splits at its internal period and the two halves are reported as separate units, which is exactly the boundary the mask exists to prevent. **RED stage 2 for T036**: revert the block's third-sentence edit so the note is restated verbatim, and confirm the note stops being reported at all. Then revert both.
- [ ] T037a [TEST] [P] [US4] Add `test_masking_governs_boundaries_and_not_equality` to `tests/doc-health/test_modified_block_currency_fixtures.py`: derive units from a copy of the tokens tree's canon paragraph in which one tokened sentence's text is altered INSIDE its backticks, and assert the sentence is reported as uncarried while STILL being one unit rather than two. *Separated from T037's RED evidence because it is a distinct property, not a perturbation: the mask decides where units END, and says nothing about whether two units are equal. Conflating the two was analyze finding F6.*

### Re-wrap quiet, end to end (row A7, § 3.6)

- [ ] T038 [TEST] [US4] Add `test_a_rewrapped_scenario_complete_block_reports_nothing_through_the_family` to `tests/doc-health/test_modified_block_currency_fixtures.py`: the family returns `[]` over the rewrap tree — asserted on the WHOLE tree, through `fam_modified_block_currency`, not on `carried()`. **RED stage 1**: tree absent. *F1 asserts this at `carried()` on units its test body synthesizes, and F1's `-quiet` tree carries no MODIFIED block at all, so a wiring regression between `derive_units` and the arms leaves both F1 tests green.*
- [ ] T039 [TEST] [P] [US4] Add `test_the_rewrap_tree_is_not_reported_skipped` to `tests/doc-health/test_modified_block_currency_fixtures.py`: the return value is a list and not a `Skip`. *The two silences are different states — canon's skip rule is "cannot run", not "found nothing" — and a tree that returned `Skip` would satisfy T038's `== []` under a naive comparison.*
- [ ] T040 [US4] Build `tests/doc-health/fixtures/modified-block-currency-rewrap/rewrapFactory/` with capability `rewrap-cases`: canon's requirement carries several prose paragraphs, a body bullet list, a dated note, and two scenarios with bullets. The block restates ALL of it, complete, with every paragraph, bullet and scenario line RE-WRAPPED at different column widths — including one paragraph wrapped mid-sentence and one bullet wrapped after its `**THEN**`. Plus `proposal.md`. T038 and T039 green. **RED stage 2**: change one word in one re-wrapped paragraph and confirm T038 fails, then revert — which proves the tree is quiet because normalization works, not because nothing was compared.

### The longer fence, end to end (row A11, § 3.7(d))

- [ ] T041 [TEST] [US4] Add `test_a_longer_fenced_named_unit_suppresses_the_whole_unit` to `tests/doc-health/test_modified_block_currency_fixtures.py`: the block drops a canon body unit that itself cites `` `openxFactory` ``, names it in a `Removed from canon` marker fenced with a double-backtick run, and the ledger reports NOTHING for that requirement. **RED stage 1**: tree absent.
- [ ] T042 [TEST] [P] [US4] Add `test_the_inner_backtick_does_not_truncate_the_named_unit` to `tests/doc-health/test_modified_block_currency_fixtures.py`: a SECOND requirement in the same tree names the same unit with a SINGLE-backtick span, which under CommonMark ends at the unit's first inner backtick. The marker then names a fragment that is no unit at all, so it suppresses nothing AND is itself reported as a marker defect. *This is the pair that makes the fence rule falsifiable: without the single-backtick sibling, a build that ignored fences entirely and matched the whole paragraph would pass T041.*
- [ ] T043 [US4] Build `tests/doc-health/fixtures/modified-block-currency-fence/fenceFactory/` with capability `fence-cases`, carrying both requirements above. Plus `proposal.md`. T041 and T042 green.

**Checkpoint**: audit rows A5, A6, A7 and A11 closed at § 3's own granularity, each through the family rather than through a helper.

---

## Phase 7: User Story 5 — provenance and determinism over the whole catalogue (P3)

**Goal**: every new tree says where it came from, mechanically; determinism
holds over every tree.

**Independent test**: `python3 -m pytest tests/doc-health/test_modified_block_currency_fixtures.py -q -k "provenance or byte_for_byte"`.

- [ ] T044 [TEST] [US5] Add `test_every_fixture_tree_this_feature_adds_carries_a_provenance_note` to `tests/doc-health/test_modified_block_currency_fixtures.py`: each of the six new trees has a `README.md`; each names either a 40-hex commit or the word `SYNTHESIZED` in its first three lines; each cites its audit row id (`A<n>`) and its packet § 3 item. **RED stage 1**: the four synthesized trees have no README yet. *A convention nothing checks is a convention that lasts one feature.*
- [ ] T045 [P] [US5] Write `tests/doc-health/fixtures/modified-block-currency-merge-gut/README.md` per the SYNTHESIS template: audit row A3, § 3.3, the delta rule quoted with its source, and "no instance of this shape exists in this corpus — which is itself why the rule is worth pinning before one arrives".
- [ ] T046 [P] [US5] Write `tests/doc-health/fixtures/modified-block-currency-tokens/README.md` per the SYNTHESIS template: audit row A6, § 3.5.
- [ ] T047 [P] [US5] Write `tests/doc-health/fixtures/modified-block-currency-rewrap/README.md` per the SYNTHESIS template: audit row A7, § 3.6.
- [ ] T048 [P] [US5] Write `tests/doc-health/fixtures/modified-block-currency-fence/README.md` per the SYNTHESIS template: audit row A11, § 3.7(d). T044 green after T045–T048 and T016, T021.
- [ ] T049 [TEST] [US5] Add `test_two_runs_agree_byte_for_byte_on_every_tree` to `tests/doc-health/test_modified_block_currency_fixtures.py`: for every tree in `ALL_TREES`, two runs produce identical `Finding.__dict__` lists including ORDER; for a tree that skips, two identical `Skip`s. This is audit row A18's extension (FR-020) — F1 pins one tree, this pins the catalogue. *A new fixture is exactly where nondeterminism enters: dict iteration over a freshly parsed document, or a sort key that ties.*
- [ ] T050 [TEST] [P] [US5] Add `test_no_new_tree_reports_an_error_or_critical_finding` to `tests/doc-health/test_modified_block_currency_fixtures.py`: across all six new trees, no finding is `error` or `critical`. *SC-009 of F1 says no `--fail-on` run reds on this family "on any tree"; six new trees are six new chances to break that by accident.*

**Checkpoint**: the catalogue is self-describing and deterministic.

---

## Phase 8: Polish, gates and the review passes

- [ ] T051 [P] [TEST] Add `test_this_feature_touches_no_production_module` to `tests/doc-health/test_modified_block_currency_fixtures.py` — the scope guard, in F1's T059 shape: assert that `scripts/doc_health/modified_block_currency.py`'s module-level constants and public function names are exactly what F1 landed (a signature-and-constant snapshot, not a byte hash, so an unrelated comment edit does not red it), and that `mbc.FAMILY not in FAMILY_NOTES` still holds. **If this test needs changing, a behaviour changed and FR-023 applies.**
- [ ] T052 Run `git diff --stat origin/main -- scripts/ openspec/ .github/` and record the output in § Evidence. It MUST be empty. A non-empty result with no defect task under FR-023 is orchestrator decision D1 violated — the failure mode is a fixture that exposed a defect and was quietly accommodated in the module.
- [ ] T053 **THE DEFECT SLOT — leave OPEN unless it fires.** If any task in Phases 3–7 found the family behaving other than the ratified delta states, add here: one task naming the defect, one `[TEST]` task carrying its RED, the minimal fix, and a line in `pr-body.md` calling it a defect found by F2 rather than a fixture adjustment. Do not fold such a fix into a fixture task. If nothing fired, write "nothing fired" and say what was checked.
- [ ] T054 Run the suite: `python3 -m pytest tests/doc-health -q | tail -3`. Record before (1077) and after in § Evidence, and confirm the delta equals the number of tests this feature added — counted from the file, not estimated.
- [ ] T055 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict 2>&1 | tail -3`. Record the count. It MUST equal T001's — this feature touches no `openspec/` path.
- [ ] T056 [P] Run `quickstart.md` end to end, § 0 through § 8, and fix `quickstart.md` wherever a command as written does not work. **Including: every `-k` selector must select a NON-ZERO number of tests** — analyze finding F1 found four selectors written on TREE names (`history_351`, `merge_gut`) that appear in no test name, so each command exited 5 having validated nothing. Check with `pytest … -k "<sel>" --collect-only -q | tail -1` per selector. *A quickstart nobody ran is a quickstart that does not work; F1's own review found this class too.*
- [ ] T057 [P] Confirm the family's findings on the REAL corpus are unchanged: the six new trees live under `tests/`, which `DELTA_GLOB` (`openspec/changes/*/specs/*/spec.md`) never reaches. Assert by running `python3 -m pytest tests/doc-health/test_family_enumeration.py -q` and the F1 file, both green and unchanged in count.
- [ ] T058 **THE MUTATION ROUND.** For each assertion this feature added, invert or weaken it in turn — restore an omitted scenario, replace a widened bullet with canon's, carry a gutted merge bullet, delete a marker, un-edit the note's third sentence, un-wrap a re-wrapped paragraph, swap the single-backtick and double-backtick markers — and confirm the paired test FAILS. Record every surviving mutant with either the new assertion that kills it or the reason it is accepted. **F1's round found three missing tests that twenty-one green tests had not; do not assume a green suite means a covered rule.**
- [ ] T059 **THE ADVERSARIAL REVIEW**, with four steps that are concrete rather than aspirational, because "hunt for problems" is how a review reports none:
      1. **Every `satisfied` row spot-checked, not merely name-checked** (FR-002's other half). For each of A4, A8, A9, A10, A12–A18, open the cited F1 test and confirm it asserts what the row claims — T024 proves only that the NAME exists, and a `satisfied` verdict citing a test that asserts something else is the one way this audit can be wrong while looking right.
      2. **FR-008's count check, mechanically.** `grep -nE 'len\(|== [0-9]|count\(' tests/doc-health/test_modified_block_currency_fixtures.py` and require every hit to be one of the declared exceptions — T019's flat file-level eight, and "exactly one finding for this requirement", which is the ledger's own at-most-one rule. Anything else is a count assertion that slipped past decision D3.
      3. **FR-002's duplication check.** Confirm no test in the new file re-asserts a rule an audit row marks `satisfied`; the new file's tests must each trace to a `gapped` or `partial` row, to the catalogue-wide invariants (T007, T049, T050), or to the audit and scope guards (T024, T051).
      4. **A fresh read** of the six fixtures against packet § 3 and the ratified delta, for: a fixture that passes for a reason other than the rule; a synthesized fixture that reads as a reconstruction; and any § 3 clause with no row.
      Record findings and dispositions in `plan.md` § Adversarial review residue.
- [ ] T060 Write `specs/020-modified-block-currency-fixtures/pr-body.md`: the audit result (18 rows, 10 satisfied / 1 extended / 4 partial / 3 gapped) and the seven rows closed; both reconstructions with their SHAs and the two-stage RED evidence; the four synthesized trees labelled as such; the suite count delta; the empty `scripts/`+`openspec/` diff; T053's defect line (or "nothing fired"); and an explicit statement that **this feature does not close #330** (packet § 7.1) and proposes no severity flip (§ 7.2).
- [ ] T061 Update `contracts/coverage-audit.md`'s closing section and `plan.md` § Predicted evidence with the MEASURED figures, replacing every predicted number. Any figure that moved gets a line saying why.

---

## Dependencies

```text
Phase 1 (T001–T004)  ─┐
                      ├─→ Phase 2 (T005–T009) ─→ every story phase
                      │
Phase 3 US1 (T010–T022)   P1 · MVP · the reconstructions
Phase 4 US2 (T023–T026)   P1 · the audit  [independent of Phase 3]
Phase 5 US3 (T027–T032)   P2 · merge-gut
Phase 6 US4 (T033–T043, incl. T037a)   P2 · derivation gaps
Phase 7 US5 (T044–T050)   P3 · provenance + determinism  [needs 3,5,6 trees]
Phase 8      (T051–T061)  gates, mutation, adversarial review, PR body
```

- **T002 blocks everything.** If the base moved, the audit is stale.
- **Phase 2 blocks every story**: `ALL_TREES`, `_tree`, `_units` and the
  classifiers are used by every test after it.
- **Phase 4 (US2) is independent of Phases 3, 5, 6** — the audit needs no
  fixture. It can run first if the reconstructions stall.
- **T044 needs T016, T021 and T045–T048** — every tree's README.
- **T049 and T050 need every tree** to exist, so Phase 7 follows 3, 5 and 6.
- **T058 needs every assertion** to exist and be green.

## Parallel opportunities

- Phase 3: T012, T013, T014, T015 are `[P]` — four independent assertions over
  one tree, once T011 has built it.
- Phase 6: T033 is independent of every tree; the three trees (T037, T040,
  T043) are independent of each other, as are their tests once built; T037a is
  independent of every tree, deriving its units in the test body.
- Phase 7: T045–T048 are four independent files.
- Phase 8: T056 and T057 are independent of each other and of T051–T055.

## Implementation strategy

**MVP is Phase 1 + Phase 2 + Phase 3 (US1).** That alone freezes #351 and #329
in their real text with provenance and mechanical verification — the
irreducible content of this feature, and the part F1's own SC-001/SC-002
assign here by name. Stopping there is a legitimate terminal state.

**Then Phase 4 (US2)**, which is cheap and is what stops the next reader
writing duplicates.

**Then Phase 5 (US3)**, the one true hole, before the narrower partial rows —
A3 is where a refactor could silently permit an undeclared bullet deletion,
and A5/A6/A7/A11 are narrowings of rules that already have a test.

**Phase 8 is not optional polish.** T058's mutation round is the task that
decides whether the twenty-odd new tests assert anything, and F1's experience
is the argument: its round found three rules documented in three places and
asserted in none.

## Notes

- **62 tasks**; **29** of them `[TEST]` tasks — T005, T007, T010, T012–T015,
  T017, T019, T020, T022, T024, T027, T028, T030, T032–T037a, T038, T039, T041,
  T042, T044, T049–T051 — producing **30 test functions** (T033 adds two). Each
  is paired with the task that makes it pass, except T033, T037a and T051, whose
  RED evidence is the mutation round rather than a pre-state — recorded as such
  on the task rather than claimed. Per story: US1 13, US2 4, US3 6, US4 12,
  US5 7; Setup 4, Foundational 5, Polish/gates 11.
- **`tasks.md` is the ONE home for the test count.** `plan.md` used to carry a
  second inventory and it had already drifted (analyze finding F2); it now
  points here.
- **Commit after each phase**, with explicit pathspecs — this checkout is
  shared and `git add -A` sweeps other sessions' work
  (the aggregation repo's `CLAUDE.md` § Working rules 2).
- **Never `pytest tests` from this worktree** (D5). Never edit
  `tests/doc-health/test_modified_block_currency.py` or anything under
  `scripts/` (D1, D4) — except through T053.
- Every `[TEST]` task names its test functions, because "add tests" is how a
  test file ends up asserting that a module imports.

## Evidence

*(filled during implementation — T001, T023, T052, T054, T055, T058)*

| gate | before | after |
| --- | --- | --- |
| `pytest tests/doc-health -q` | | |
| `openspec validate --all --strict` | | |
| `git diff --stat origin/main -- scripts/ openspec/ .github/` | — | |
| surviving mutants | — | |
