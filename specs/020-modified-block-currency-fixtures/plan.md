# Implementation Plan: the modified-block-currency regression-fixture catalogue

**Branch**: `020-modified-block-currency-fixtures` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/020-modified-block-currency-fixtures/spec.md`

## Summary

**F2 of four** Speckit features realizing the ratified OpenSpec change
`add-modified-block-currency-check`. Scope is that packet's § 3, items 3.1
through 3.13, and nothing else. F1 is on `main` at `19e3f6b5`: the family
module registered as the twenty-second family, 97 tests, six fixture trees.

F1's implementation review found F1 already realizes every scenario of the
ratified delta with a test. So the approach is **audit first, then close the
gaps**:

1. **`contracts/coverage-audit.md`** maps all fourteen § 3 rows to the F1 test
   functions that discharge them, taken from the landed test file rather than
   from any of F1's three self-descriptions (which disagree — research R10).
   **Result, over 18 rows covering 14 items: 10 satisfied, 1 satisfied-and-
   extended, 4 partial, 3 gapped.** An item F1 covers gets a row and no second
   test.
2. **Six new fixture trees and two unit-level assertions close the seven
   non-satisfied rows**, RED-first — § 3.4's widening needs no tree of its own,
   because fixture A carries the real instance and the two synthetic widenings
   are `carried()`-level. The two
   that carry the feature are the historical reconstructions: **both histories
   were verified recoverable and both were run through the family before this
   plan was written** (research R1, R2), so § 3.2's "else synthesize faithfully
   and say so" branch does not fire.

**No behaviour is added to the module.** A fixture that exposes a defect
becomes its own task with its own RED test and its own line in the PR body
(orchestrator decision 1) — never a quiet accommodation in `scripts/`.

## Technical Context

**Language/Version**: Python 3.11+ (the `doc_health` package's floor; the
module uses `int | None` unions)

**Primary Dependencies**: `scripts/doc_health/modified_block_currency.py` (F1,
consumed read-only), `scripts/doc_health/promotion_fidelity.py` (`norm`,
`parse_delta`), `tests/doc-health/conftest.py` (`make_ctx`, `FIXTURES`,
`FakeGit`)

**Storage**: none. Fixture trees are Markdown files on disk under
`tests/doc-health/fixtures/`

**Testing**: `python3 -m pytest tests/doc-health -q`. **Baseline 1077 passed**
at this branch point. The whole-tree `pytest tests` is never run from a
worktree — it needs a live Postgres this checkout has no access to
(orchestrator decision 5)

**Target Platform**: developer checkout and CI (`doc-health-reusable.yml`),
which this feature does not touch

**Project Type**: governance tooling — a deterministic checker and its test
suite, inside a documentation-and-contracts repository

**Performance Goals**: none stated. The six new trees are small; the suite's
54-second wall time must not materially move

**Constraints**: no change to `scripts/`, `openspec/`, `.github/`,
`report.py`, `runner.py` or thresholds (FR-022, FR-024). Assertions on rule
text and named units, never counts (FR-008). Every test RED-first (FR-025)

**Scale/Scope**: 6 new fixture trees, 1 new test file, ~26 new tests, 2
contracts. Zero lines of production code

## Constitution Check

*GATE: passed before Phase 0, re-checked after Phase 1.*

| principle | verdict | basis |
| --- | --- | --- |
| **I — Contract-first, domain-neutral core** | PASS | Nothing domain-specific lands. The fixtures use synthetic capability names (`merge-gut`, `token-cases`, `fence-cases`, `rewrap-cases`) plus two real openxFactory capabilities recovered from this repository's own history. No DomainxFactory content, no `stack.yaml` change |
| **II — OpenSpec before implementation** | PASS | `add-modified-block-currency-check` is ratified (2026-08-27, "Ratify as-is"). This feature builds § 3 through Spec Kit, which is what the packet's own tasks.md instructs ("Build with Speckit, not `/opsx:apply`"). No governance decision is taken here; the five orchestrator decisions below are implementation choices, flagged for veto |
| **III — Document lifecycle and status discipline** | PASS | No governed document is created, edited or re-statused. The six fixture `README.md` files sit under `tests/`, which `corpus.EXCLUDED_PARTS` excludes and no `GOVERNED_ROOTS` entry covers — **verified against `scripts/doc_health/corpus.py`**, not assumed (research R6), so they carry no `Status:` header and draw no lifecycle finding |
| **IV — Schema and artifact discipline** | PASS | No YAML added, so no `schema_version`/`kind` obligation. No credential. **No host-absolute path in any committed file** — checked across all seven artefacts; `quickstart.md`'s worktree reference was rewritten repo-relative when this gate found it |
| **V — Validation gates (NON-NEGOTIABLE)** | PASS | `python3 -m pytest tests/doc-health -q` and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` are the two gates, both recorded before and after (§ Predicted evidence). Evidence is deterministic fixtures and test output, never assertion. `/speckit-analyze` must report no critical finding before implementation |
| **VI — Versioned, content-addressed releases** | N/A | No contract release, no manifest, no tag |
| **VII — Fail-closed authority boundaries** | PASS | No registry is widened. The family's advisory launch is untouched — F2 adds no severity, no `FAMILY_RESOLUTION` entry, and audit row A16 explicitly forbids a second copy of F1's launch pin |

**Post-Phase-1 re-check: still PASS.** Phase 1 added two contracts, a data
model and a quickstart, all under `specs/020-…/`. The only gate Phase 1 moved
was IV, and it moved to PASS by removing the absolute path.

No violation requires a Complexity Tracking entry. Two complexities are
recorded there anyway, because a reviewer will ask.

## Project Structure

### Documentation (this feature)

```text
specs/020-modified-block-currency-fixtures/
├── spec.md                        # 5 user stories, FR-001..FR-028, SC-001..SC-012
├── plan.md                        # this file
├── research.md                    # R1–R11: the history recovery, the measurements, the readings
├── data-model.md                  # fixture-tree invariants, the two assertion classes
├── quickstart.md                  # how to re-derive and validate, command by command
├── contracts/
│   ├── coverage-audit.md          # § 3 → F1 tests, 14 rows, verdicts  ← THE deliverable of US2
│   └── fixture-provenance.md      # the shape of a fixture README
├── checklists/
│   └── requirements.md            # spec quality gate
└── tasks.md                       # /speckit-tasks output
```

### Source Code (repository root)

```text
scripts/doc_health/
└── modified_block_currency.py          # UNTOUCHED (FR-022). Read-only input

tests/doc-health/
├── conftest.py                          # UNTOUCHED. make_ctx, FIXTURES, FakeGit
├── test_modified_block_currency.py      # UNTOUCHED (F1's 97 tests)
├── test_modified_block_currency_fixtures.py   # NEW — every test this feature adds
└── fixtures/
    ├── modified-block-currency-history-351/   # NEW  A1 · § 3.1 · reconstructed @ bcfc26a0
    │   ├── README.md
    │   └── intakeFactory/openspec/{specs,changes}/…
    ├── modified-block-currency-history-329/   # NEW  A2 · § 3.2 · reconstructed @ d5f447e8
    ├── modified-block-currency-merge-gut/     # NEW  A3 · § 3.3 · synthesized
    ├── modified-block-currency-tokens/        # NEW  A6 · § 3.5 · synthesized
    ├── modified-block-currency-rewrap/        # NEW  A7 · § 3.6 · synthesized
    ├── modified-block-currency-fence/         # NEW  A11 · § 3.7(d) · synthesized
    ├── modified-block-currency/               # UNTOUCHED (F1)
    ├── modified-block-currency-markers/       # UNTOUCHED (F1)
    ├── modified-block-currency-noscope/       # UNTOUCHED (F1)
    ├── modified-block-currency-quiet/         # UNTOUCHED (F1)
    ├── modified-block-currency-resolution/    # UNTOUCHED (F1)
    └── modified-block-currency-two-writers/   # UNTOUCHED (F1)
```

**Structure Decision.** Six new fixture trees, one new test file, zero
production files. One tree per case rather than additions to F1's trees,
because `make_ctx` loads every repository under a tree into one `Context` and
F1's whole-tree assertions (several `== []`) would silently change meaning
(research R7, invariant I1).

## The audit, in one table

Full detail and every F1 test name: [`contracts/coverage-audit.md`](./contracts/coverage-audit.md).
**That file is the single home for the mapping** — nothing else restates it.

| verdict | rows | audit rows, with the § 3 item each covers |
| --- | --- | --- |
| **satisfied** — F1 covers it as § 3 phrases it; F2 adds nothing | 10 | A4 (3.3a), A8 (3.7a), A9 (3.7b), A10 (3.7c), A12 (3.7e–k), A13 (3.8), A14 (3.9), A15 (3.10), A16 (3.11), A17 (3.12) |
| **satisfied, extended** | 1 | A18 (3.13) — satisfied as phrased; F2 extends byte-identity to every tree |
| **partial** — the rule is tested, but narrower or through a helper | 4 | A5 (3.4), A6 (3.5), A7 (3.6), A11 (3.7d) |
| **gapped** — a clause has no test at all | 3 | A1 (3.1), A2 (3.2), A3 (3.3) |

*(**18 rows for 14 items**: § 3.7 carries eleven distinct obligations and is
split into five rows, A8–A12. Every row has exactly one verdict, and the
`§ 3 item` column covers 3.1–3.13 plus 3.3a with no gap and no duplicate.)*

**The two that carry the feature.** A1 and A2 are `gapped` only in FIDELITY:
F1 covers both SHAPES, including § 3.2's flat-count pin, in synthesized text
that borrows the two real #351 titles. § 3.1 and § 3.2 ask for the instances,
F1's own SC-001/SC-002 assign the reconstructions to F2 by name, and both are
recoverable.

**The one that is a true hole.** A3 (§ 3.3). F1's only end-to-end `Merged into`
case has a one-bullet merged source that the block carries, so the delta's own
rule — "a `Merged into` marker names titles only, so a bullet a merge makes
redundant … has to be declared as a bullet, one at a time" — is asserted
nowhere. That is the one place a refactor could silently permit an
undeclared bullet deletion.

## Decisions taken by the orchestrator — FLAGGED FOR VETO

**D1–D5 were given to this session; O1–O4 are taken here.** Each is
independently reversible and none is a governance ruling. A veto on any is an
edit to this plan, not a new change.

**D1 — F2 adds NO behaviour to the module.** If a § 3 fixture exposes a real
defect in F1's implementation, the fix is a separate task in F2 with its own
RED test, minimal, and named as a defect in the PR — never silently folded.
Realized as FR-022, FR-023 and the scope-guard task; `quickstart.md` § 7 makes
the violation detectable by `git diff --stat`.

**D2 — historical fixtures are reconstructed from git where the history
exists, with the commit SHAs in the fixture's README; synthesized only where
history is gone, and labelled so.** Both histories exist (research R1), so all
four synthesized trees are synthesized because *no instance of their shape
exists in this corpus*, which the provenance contract requires them to say.

**D3 — assertions on rule text and named units, never counts** (§ 3.1's own
ACCEPTANCE) — applied to every new test, not only to the two reconstructions.
The one exception is the count that IS the rule: § 3.2's flat file-level eight,
asserted precisely because it does not predict the outcome. `data-model.md` § 4
makes this the U/F assertion-class discipline.

**D4 — no changes to the packet's delta text, the § 2.1 block, canon, or any
other family.** Scope guard as in F1 (the T059 pattern).

**D5 — the whole-tree `pytest tests` is never run from a worktree** (live
Postgres); evidence is `python3 -m pytest tests/doc-health -q`, baseline
**1077** — measured at this branch point, not quoted.

---

**O1 — every test this feature adds goes in ONE NEW FILE,
`tests/doc-health/test_modified_block_currency_fixtures.py`, and F1's file is
not touched.** F1's file is ~1400 lines organized by rule group, with
module-level constants (`CAP`, `REQ`, `LOSSY`, `FIXTURE_REPO`) and helpers
(`_run`, `_titles`, `_ledger`, `_markers_run`, `_res_run`, `_tw_run`) all bound
to its own trees. Six more trees would either collide on those names or force a
rename inside a landed file, which turns a fixture diff into a refactor diff
and makes the review unable to see what F2 actually asserts. A separate file
also keeps the D1 scope guard trivially checkable. **Cost, stated rather than
hidden:** the finding-classifier helpers are re-spelled, and two spellings of
one classifier is the "second grammar" defect this corpus keeps paying for
(`align-status-reader-to-real-lines`). O2 pays it down.

**O2 — the re-spelled classifiers are pinned by a PARTITION invariant rather
than by importing F1's test module.** One test asserts that, over every fixture
tree this family owns, each emitted finding falls into exactly one of the four
classes — scenario-title, ledger, marker-defect, resolution/ordering — none
into two and none into zero. That is a stronger property than "my helper
matches F1's helper", it needs no cross-test-file import (which depends on
pytest's `prepend` import mode inserting the test directory on `sys.path`, a
mechanism this suite should not start relying on), and it fails loudly if an
arm's wording drifts in either file. A classifier that swallowed a resolution
finding into the ledger is exactly the bug F1's own `_ledger` docstring records
having had.

**O3 — a reconstructed fixture freezes the REQUIREMENT verbatim, not the whole
source file** (research R5). Canon for #351 is 279 KB of mostly unrelated
requirements and the family reads per requirement. The requirement section is
byte-identical; the `# … Specification` / `## Purpose` / `## Requirements`
scaffolding around it is synthetic and the provenance note says so, with
`quickstart.md` § 1 giving the `diff` that proves the scoped guarantee. A veto
here means committing ~300 KB of frozen canon and accepting that every later
canon edit looks like a fixture concern.

**O4 — the delta side of each reconstruction is copied WHOLE.** A delta file is
small, and for § 3.2 the `## ADDED Requirements` section is load-bearing: the
flat file-level count of eight only exists because the change's own ADDED
requirement brings seven. Trimming the delta to its MODIFIED block would
destroy the very property § 3.2 asks to pin.

## Predicted evidence

**One home for each figure.** F3 asserts the live-corpus movement against
F1's `plan.md` § Predicted movement; **this feature asserts nothing about the
live corpus** and does not restate that table.

| gate | before | after | why |
| --- | --- | --- | --- |
| `python3 -m pytest tests/doc-health -q` | **1077 passed** (measured at this branch point) | 1077 + the tests this feature adds | the only figure this feature moves |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | recorded at implementation | **unchanged** | this feature touches no `openspec/` path |
| `git diff --stat origin/main -- scripts/ openspec/ .github/` | — | **empty** | D1/D4, unless a defect task exists and names the file |
| the family's findings on the real corpus | — | **unchanged** | six new trees live under `tests/`, which the delta glob never reaches |

**Planned test inventory**, so the count is derivable rather than promised.
Names are the plan's proposal; `tasks.md` fixes them.

| tree / area | tests |
| --- | --- |
| history-351 (A1) | `test_the_351_block_omits_exactly_the_two_scenarios_canon_kept`, `test_the_351_ledger_carries_every_clause_the_repair_commit_named`, `test_the_351_reverted_scenario_line_is_reported`, `test_the_351_widened_bullet_is_reported_although_it_contains_canon_s`, `test_the_351_finding_lands_on_the_active_delta_path_at_warning`, `test_the_351_fixture_is_the_history_it_claims` |
| history-329 (A2) | `test_the_329_block_omits_all_seven_titles_by_name`, `test_the_329_flat_file_level_count_buys_no_silence`, `test_the_329_ledger_names_canon_s_two_body_sentences`, `test_the_329_fixture_is_the_history_it_claims` |
| merge-gut (A3) | `test_a_merge_marker_does_not_declare_the_bullets_it_makes_redundant`, `test_the_scenario_arm_is_quiet_because_the_merge_marker_is_valid`, `test_naming_the_redundant_bullets_in_a_removal_marker_silences_them`, `test_the_companion_is_quiet_because_of_its_marker_and_not_by_carriage` |
| containment (A5) | `test_a_block_unit_widened_before_canon_s_does_not_carry_it`, `test_a_block_unit_widened_at_both_ends_does_not_carry_it` |
| tokens (A6) | `test_no_unit_boundary_falls_inside_a_versioned_token`, `test_each_body_bullet_is_its_own_reported_unit`, `test_a_note_edited_in_its_third_sentence_is_reported_once` |
| rewrap (A7) | `test_a_rewrapped_scenario_complete_block_reports_nothing_through_the_family`, `test_the_rewrap_tree_is_not_reported_skipped` |
| fence (A11) | `test_a_longer_fenced_named_unit_suppresses_the_whole_unit`, `test_the_inner_backtick_does_not_truncate_the_named_unit` |
| cross-cutting | `test_every_finding_falls_into_exactly_one_class` (O2), `test_two_runs_agree_byte_for_byte_on_every_tree` (A18/FR-020), `test_every_new_fixture_tree_carries_a_provenance_note`, `test_this_feature_touches_no_production_module` (scope guard) |

**~26 tests.** The last four are the ones a later session will thank this plan
for: the partition invariant, whole-catalogue determinism, the provenance
requirement made mechanical, and the scope guard.

## Complexity Tracking

*No Constitution Check violation requires justification.* Two complexities are
recorded because a reviewer will ask about both.

| item | why needed | simpler alternative rejected because |
| --- | --- | --- |
| A second test file with re-spelled finding classifiers (O1) | F1's file binds six helpers and four constants to its own trees; six more trees collide or force a rename inside landed code, and the D1 scope guard stops being a one-line diff check | Extending F1's file makes the review read a refactor instead of a fixture set, and a rename inside a landed 1400-line file is exactly the change D4 exists to prevent. The cost — two spellings of one classifier — is paid down by O2's partition invariant, which is a stronger pin than helper equality |
| Six fixture trees where two or three might do (research R7) | `make_ctx` loads every repository under a tree into ONE context, and F1's existing tests assert over whole-tree results including several `== []` | Merging the six cases into fewer trees makes every assertion in a tree conditional on every other case in it — and one of the six (rewrap) asserts the tree returns `[]`, which no other case can share by construction |

## Analyze residue

*(filled by `/speckit-analyze`)*
