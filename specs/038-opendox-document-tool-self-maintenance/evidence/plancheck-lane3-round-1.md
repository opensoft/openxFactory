# Plan check, round 1: lane openXfactory-3's PLANCHECK of `6d6911e1`

Status: record

**Feature**: [`038-opendox-document-tool-self-maintenance`](../spec.md) ·
**Reviewed**: plan 038 at `6d6911e1`, draft PR #1245 · **Run**: 2026-10-05,
22:40:40Z to 22:42:30Z, read-only, by lane `openXfactory-3` · **Folded in**: the
revision that commits this file · **Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## Verdict

Lane openXfactory-3 checked the plan in four parts (A: phase 4; B: Groups 6 and
14; C: Group 15; D: the arc and the 63 decisions) and sent 125 lines to lane
openxfactory-4's coordination log: 34 FIX, 4 MISLABEL, 9 SHARED, 4 NOT REACHED,
72 OK, one SPLIT line and one DONE line. It found 0 MISSING. It **accepted the
proposed lane split on three conditions**, each applied in this revision
(plan.md § "Two lanes").

On the holder's rulings (conform to ratified text wherever possible), this
revision:

- **applies** 33 of the 34 FIX lines (three of them repeat another line: L80
  repeats L70, L97 repeats L67, L121 repeats L105), and puts the other, L15, to
  Brett as tier 2's CF-5, with batch Q item 3 worded as that reading;
- **conforms** on MISLABEL row 31 (L116), so it is no longer a question, and puts
  the other three to Brett: row 49 as tier 1's ARC-5 (L117), row 36 as tier 1's
  I-2 (L118, recommending (a)), and row 17 as tier 2's CF-6 (L119);
- **applies** the four SHARED lines that found a gap (L2, L31, L32, L115); the
  other five record orders that already held;
- **answers** what it can of the four NOT REACHED lines, and leaves the rest to
  T003's round 2;
- **disagrees with no line.** Two notes on how a FIX was applied are in the
  table: L4's packaged-reader suggestion applies to one schema of the two, and
  split condition 1's stated reason no longer holds, though the order is kept.

Lane openXfactory-3 is credited for the check in research.md R13. Its T021, T022
and rows 42–43 FIXes also corrected its own inventory's copy-record proposal
(R2-INV-P4F § schema).

## How it was read

The lines were read from the coordination log with the coordinator's command:

    $ awk '$1>="2026-10-05T22:40:40" && $1<="2026-10-05T22:42:30Z"' lane3-to-lane4.log | wc -l
    125

Each claim was re-measured before it was applied, in the plan writer's clones
(openDox-code `a9ac96f9`, openXdox-code `56e1c238`, openDox-spec `f7ee3c76`)
and this branch's worktree; the decisive output is quoted in
[`analyze-round-1.md`](./analyze-round-1.md) § "How the review was run". Two
NOT REACHED items were measured for this note:

    $ sed -n 2817p $T; sed -n 2824,2825p $T          (T = #1144's tasks.md)
      below, and `gh` NOT installed, which is the student's machine):
          if command -v gh >/dev/null 2>&1; then                # the precondition, ASSERTED: the student's machine
            echo "FAIL: gh is installed; this acceptance must run without it"; exit 1
    $ ls openDox-spec/contracts/schemas/              (at f7ee3c76)
    ideation-workbench.schema.yaml
    opendox-snapshot.schema.yaml
    xfactory-workbench-chat-turn.schema.yaml
    xfactory-workbench-model-catalog.schema.yaml
    $ grep -n 'DISPLAY_SCHEMA_VERSION\s*=' src/opendox/*.py   (openDox-code a9ac96f9)
    src/opendox/display_profile.py:134:DISPLAY_SCHEMA_VERSION = 1

## Dispositions

`L<n>` is the line's number in the verbatim block below. Tier numbers refer to
plan.md § "Design decisions for Brett to rule with this plan".

### FIX

| line | target | disposition | where |
|---|---|---|---|
| L4 | T021: openXdox-code's copy record cannot hold the receipt schema | Applied, in the holder's conforming form (ADV-10): nothing is vendored. `gate-action-record` is read from openXdox-code's own package (lane 3's "the reader moves to the packaged `contracts/schemas/`" applies to this one); the receipt schema, which is openxFactory's and not packaged, is read from a schema source the host registers (the composed conftest, then host wiring at T030); a lone checkout refuses by name. | T021, T030; tier 3 P4F-4; conflict C-19 |
| L5 | T022: the runbook cannot be a row in openXdox-spec's record | Applied: the runbook is placed from the composed tree by `scripts/composed_placements.py`, git-ignored; nothing vendored. | T022; tier 3 P4F-3 |
| L9 | T050: the model's inlined tables can drift from `display.js` | Applied: T050 adds a guard that the inlined tables equal `display.js`'s, if W-1 rules (A). | T050; plan.md single-writer row for `display.js` |
| L10 | T026: the oracle's path | Applied: `scripts/protected_suites.py` (`_inside_the_test` at `:294`). | T026; tier 1 R-1 |
| L11 | Row 38 (R-1) overclaims; two nodes are not harness text | Applied: R-1 (a) closes the 21 harness nodes and the route claims only TOGETHER with W-1; the 'cluster' node takes an ordinary entry; the `SystemExit: 2` node is traced first in T026. | tier 1 R-1; T026; conflict C-11 |
| L13 | Rows 42, 43 (P4F-3, P4F-4) say "under copies.yaml" | Applied, as L4 and L5. | tier 3 P4F-3, P4F-4 |
| L14 | T029: recursive submodules | Applied: openxFactory's nested `openDox` and `openXdox`, and `openXwallet`, initialized recursively. | T029; tier 3 N-7a; research.md R2 |
| L15 | T005 item 3 quotes R2Q8 (a)'s expiring limit | To Brett, as a reading to confirm: "F12.1 runs composed; ARC-Q2 (a) makes the composition its permanent home". Item 3 is worded so. | tier 2 CF-5; T005 item 3 |
| L17 | `spec.md:1193`: "10 files" | Applied: 11 files, and the 5 suites that pass composed (210 cases). | spec.md § Assumptions; plan.md C-1 (FIXED) |
| L25 | R2Q7: T012 should name the two refusals as test nodes | Applied: `test_a_repository_with_no_main_is_unknown_and_refused_naming_it`, `test_no_declaration_refuses_naming_the_file_and_its_content`. | T012 |
| L27 | T011: the push core is `_push_to_remote_with` (`:1742`) | Applied: T011 factors `_push_to_remote_with` with `_bound_local_destination` (`:1613`) and `_receive_pack_for` (`:1720`), keeping the command-config refusal (`:1335`, `:1372`). | T011; tier 3 OQ-12-12 |
| L34 | T047: name the copy record; 15.1a's refusal of a corpus-relative entry with `commit` | Applied, both. | T047; contracts/health-packs-manifest.md § Rules |
| L35 | T048: the mount set; where the fail-not-skip helper lives | Applied: the interpreter, its standard library and `opendox.health_contract` only, never `site-packages`; the helper in its own test module. | T048; data-model.md § Sandbox probe and canary; contracts/health-packs-manifest.md |
| L36 | T049: 15.2a's full refusal list and the 65,536-byte bound | Applied. | T049; data-model.md § Patch |
| L37 | `data-model.md:187`: whole-text patches | Applied: unified diffs only (ADV-12). | data-model.md § Patch |
| L38 | T055: not 15.6a's eight packs | Applied: the eight, by exact name (ADV-03). | T055 |
| L39 | T055: the canary hunt and the planted symlink | Applied, and the canary's definition corrected to a CANARY variable and a CANARY descriptor. | T055; data-model.md § Sandbox probe and canary; contracts/health-packs-manifest.md |
| L47 | T050: After T045 | Applied. | T050 |
| L52 | R2Q16: batch Q carries only part of the reading | Applied: item 9 carries the full reading. | T005 item 9; tier 2 CF-2 item 9; conflict C-4 |
| L54 | R2Q17: no owner for the 26.04 measurement | Applied: new task T068 (non-gating); release 2 stays on `ubuntu-24.04`. | T068; tier 3 N-18 |
| L63 | `RLIMIT_NPROC` is per user, not per sandbox | Applied: never `RLIMIT_NPROC`; `pids.max` where a cgroup is delegated, else the PID namespace and the time budget; T056 measures the defaults. | tier 3 OQ-H15-5; contracts/health-packs-manifest.md § Rules; T056 |
| L64 | Per-entry `timeout_seconds` and `bounds` are a second source | Applied: budget and bounds are the engine's; no per-entry budget or bounds in the manifest; `--timeout` defaults to 60 seconds, ceiling 600. | contracts/health-packs-manifest.md; tier 3 OQ-H15-5; conflict C-20 |
| L67 | T052: the `workbench.py` cite | Applied: `run_scoped_doc_health` `:1666`, `register_health_check` `:1622`. | T052; research.md; conflict C-9 |
| L70 | T042: add OQ-H15-19 | Applied. | T042 |
| L71 | T042: the suite-ripple wording | Applied: the five suites `0003_` moves, each with its reason. | T042 |
| L75 | T057: After T052 | Applied. | T057; plan.md single-writer row for `serve.py` |
| L80 | Part 10 E resolution 5 | Applied, as L70. | T042 |
| L85 | T005 item 1: 6.2's superseded description | Applied. | T005 item 1; tier 2 CF-2 item 1 |
| L89 | R2Q12: `unclassed` makes the "three classes" read as open | Applied: `unclassed` exists only if tier 1's I-2 is ruled (b), said in the R2Q12 row, the data model and the finding contract. | plan.md § Ruled answers (R2Q12); data-model.md § Finding; contracts/health-finding.md |
| L97 | T052's cite | Applied, as L67. | T052 |
| L105 | T072 makes T061 wait on the arc's ratify word | Applied: T072 is opportunistic; T061 never waits; a late T072 rides the arc's own pin (ADV-06). | T061, T072; tier 3 ARC-6 |
| L106 | T073 belongs to #1144, not the arc | Applied (split condition 3): T073 moves to § "Requirement 9 for openXdox-code", carries #1144's `Arc:` value, stays lane 3's and is not gated on T071. | tasks.md § Requirement 9; plan.md § Two lanes |
| L120 | Row 47 (ARC-3): "as the ruling allows" | Applied: dropped. An openXdox-spec delta, if the seams need one, is written into the change T070 authors, and Brett's ratify word (T071) is the word for it. | tier 3 ARC-3; T070, T071 |
| L121 | Row 50 (ARC-6) | Applied, as L105. | tier 3 ARC-6 |

### MISLABEL

| line | row | disposition | where |
|---|---|---|---|
| L116 | Row 31 (OQ-H15-20, with row 20's `patch` column) stores pack patches, document text | Conformed to 14.3 and R2Q25 (a): no `patch` column in `0003_`; a patch is validated at `run` (a refusal stored as a finding with no text) and RE-OBTAINED at `fix` by re-running that one pinned pack in the sandbox, then validated again. L40's and L43's notes on the `patch` column are superseded by this. | tier 3 OQ-H-22, OQ-H15-20; data-model.md; T042, T053, T056 |
| L117 | Row 49 (ARC-5) settles a conflict between two of Brett's rulings | To Brett: tier 1's ARC-5, merged with row 34 and the Opus review's ADV-20. | tier 1 ARC-5; conflict C-6 |
| L118 | Row 36 (I-2) suspends requirement 6's baseline where there is no `main` | To Brett: tier 1's I-2, recommending (a), "the baseline branch is `main`, else the branch HEAD names". | tier 1 I-2; conflict C-14 |
| L119 | Row 17 (OQ-H-18) reduces "optionally on commit" to a documented hook line (low confidence) | To Brett: tier 2's CF-6, the hook-line reading first, with an opt-in hook verb as the alternative. | tier 2 CF-6 |

### SHARED

| line | file | disposition |
|---|---|---|
| L2 | openXdox-code `src/openxdox/contracts/copies.yaml` (T021, T022) | Applied: the file has NO writer in release 2 (L4, L5), stated in the single-writer table; T021 still precedes T022 (split condition 1). |
| L30 | `src/opendox/health_contract.py` (T041, T045) | Already ordered; the cross-lane hand-off is now named in plan.md. |
| L31 | openDox-code `src/opendox/contracts/copies.yaml` and `schemas/` (T041, T047, T054) | Applied (split condition 2; ADV-05): T041 → T047 → T054, at the commit the root pins (T060); the files are in the table and each task's Files. |
| L32 | openDox-code `pyproject.toml` (T048, T055, T061) | Applied: in the table; T055 After T048. |
| L111–L114 | openXdox-code `tests/conftest.py`, `declared_exclusion.yaml`, `composed.yml`, `test_host_plane.py` | Already ordered; no change. |
| L115 | openXdox-code `tests/composed_host_pin.yaml` | Applied: a row in the single-writer table; T073 re-runs after each advance (T030, T064, T075). |

### NOT REACHED

| line | part | disposition |
|---|---|---|
| L29 | A: the submit-land contract and data model against the code; T008's codexFactory cites | Covered by the Opus review (ADV-01, ADV-02, ADV-41) and dispositioned there; codexFactory's rules were measured (research.md R13). |
| L68 | C: quickstart's Group 15 steps; the finding contract beyond its classes; T058's 24 node names against batch Q; T051's per-wave re-pins | The Opus review read the quickstart and the finding contract in full (ADV-27, ADV-31). T058's node names follow batch Q's amended F15.1 by construction (T058 After T005). T051 re-pins after each wave's last openDox-code landing. Left for T003's round 2 to check. |
| L98 | B: OQ-H-3's "a scoped run is not stored", I-2, the `0003_` ripple, phase 5 against protected suites | OQ-H-3's clause is part of R2Q16 (a)'s full reading (batch Q item 9). I-2 is tier 1. The ripple is measured in T042's PR. Phase 5 writes openXdox-code only at T063 (`pyproject.toml`) and in the arc (T074, "none protected"). |
| L123 | D: row 28 (OQ-H15-15), row 6 (OQ-12-16), row 56 (N-6) | Row 28: the display facet's version is openDox-code's `DISPLAY_SCHEMA_VERSION` (`display_profile.py:134`), and openDox-spec at `f7ee3c76` holds no display schema, so the bump is no spec-leg schema change. Row 6: F12.2 asserts its precondition with `command -v gh` (`:2824-2825`), which a PATH without `gh` satisfies; its prose says "`gh` NOT installed" (`:2817`); tier 3 OQ-12-16 records the reading. Row 56: now tier 1's N-6. |

### SPLIT and DONE

| line | disposition |
|---|---|
| L1 | Recorded: the split matches lane 3's slice outline file for file. |
| L48 | Recorded: the pack track matches Part B's outline. |
| L124 | Applied, all three conditions. (1) T021 before T022: kept, although its stated reason (both write a copy record) no longer holds, because under L4 and L5 neither writes one. (2) T054 After T047, with openDox-code's copy record in the table. (3) T073 moves out of the arc's section as #1144's requirement-9 work. `tests/composed_host_pin.yaml` is in the table. |
| L125 | No separate action: its items are the rows above. |

### OK

L1 and L48 (in the table above), and L3, L6–L8, L12, L16, L18–L24, L26, L28,
L33, L40–L46, L49–L51, L53, L55–L62, L65, L66, L69, L72–L74, L76–L79, L81–L84,
L86–L88, L90–L96, L99–L104, L107–L110 and L122: 72 lines, no change. Three
carry a note:

- **L40 and L43** describe a `patch` column that L116's conformance removes.
- **L122** finds row 60 (N-10) consistent with F14.1. The Opus review found
  that row narrowed R2Q12 (a)'s run kinds (ADV-16), and N-10 now supports all
  three kinds, only default-tip runs forming the baseline; F14.1, which commits
  before each run, is unaffected. Row 57 (N-7), which L122 notes "needs this
  word", is now N-7a and N-7b.

## The PLANCHECK lines, verbatim

From lane openxfactory-4's coordination log, `lane3-to-lane4.log`, the 125
lines stamped from 2026-10-05T22:40:40Z to 22:42:30Z, in order, unchanged.

```text
2026-10-05T22:40:40Z PLANCHECK split OK: T020–T026 and T029 match U-1..U-7 and U-9 file for file. U-8 is T027, T028 and T030, all lane 4. Every file both lanes write is ordered: `tests/fixtures/web_boundary_census.yaml` T025→T015 (T015 After T025), openXdox-code `tests/conftest.py` T020→T073→T074, `src/openxdox/gate_console.py` T021→T074, `.github/workflows/composed.yml` T029→T073, `tests/composed_host_pin.yaml` T029→T030. No lane-3 file is written in the same wave by a lane-4 task.
2026-10-05T22:40:40Z PLANCHECK SHARED src/openxdox/contracts/copies.yaml T021 T022 <both lane 3, both [P] after T004, so same wave; plan.md's single-writer table has no copies.yaml row>
2026-10-05T22:40:40Z PLANCHECK T020 OK
2026-10-05T22:40:40Z PLANCHECK T021 FIX <copies.yaml cannot hold this receipt-schema row: it records one source (`spec_leg: opensoft/openXdox-spec`, `commit: f088b097`, `src/openxdox/contracts/copies.yaml:1-33`) and says openXdox-spec owns these schemas (R1Q12 (a)); `tests/test_packaged_validator.py:81-92` pins the copies to the validator's three own kinds, "no fourth kind rides in as a copy". Use a separate record, or list that test in Files. Also "where it reads it" is the checkout root (`gate_console.py:642-643`): say the reader moves to the packaged `contracts/schemas/`. The copies.yaml idea came from R2-INV-P4F § schema, which was wrong.>
2026-10-05T22:40:40Z PLANCHECK T022 FIX <the same copies.yaml problem: an openDox-spec runbook cannot be a row in openXdox-spec's copy record (`copies.yaml:1-33`; `test_packaged_validator.py:81-92`)>
2026-10-05T22:40:40Z PLANCHECK T023 OK
2026-10-05T22:40:40Z PLANCHECK T024 OK
2026-10-05T22:40:40Z PLANCHECK T025 OK
2026-10-05T22:40:40Z PLANCHECK T050 FIX <under W-1 (A), T025 inlines `display.js`'s tables into `staging-workbench-model.js`, but T050 is the only writer of `web/views/display.js` (plan.md single-writer row) and does not list the model, so the two copies can drift; add the model to T050's Files, or a guard that the inlined tables equal display.js>
2026-10-05T22:40:40Z PLANCHECK T026 FIX <`tests/protected_suites.py` is `scripts/protected_suites.py` (openXdox-code `scripts/protected_suites.py:279-302`)>
2026-10-05T22:40:40Z PLANCHECK plan.md decisions row 38 (R-1) FIX <"All 26 … then close" overclaims. The 23 display-js nodes first fail on the `./display.js` import at the helper copy sites (`test_staging_workbench.py:98`, `:565`, `:1242`, `:2000`, `:2507`), outside the named spans, so R-1 (a) closes them only together with W-1. Two of the 23 are not harness text: `test_staged_scope_adds_cluster_neighbourhood_section` expects a different word ('group' vs 'cluster') inside the test, and `test_the_hostile_descriptors_still_parse_into_the_real_cli` fails `SystemExit: 2`, untraced (R2-INV-P4F § display-js). T026's R-1 list has the same gap.>
2026-10-05T22:40:40Z PLANCHECK plan.md decisions rows 39, 40, 41, 44 OK
2026-10-05T22:40:40Z PLANCHECK plan.md decisions rows 42, 43 FIX <P4F-3 and P4F-4 say "under copies.yaml", which conflicts with copies.yaml's single-source contract and `test_packaged_validator.py:81-92` (see T021)>
2026-10-05T22:40:40Z PLANCHECK T029 FIX <the composed checkout must initialize openxFactory's nested `openDox` and `openXdox` submodules recursively (the one-off part adds `openXwallet`); without them `corpus_adapter_openxfactory` refuses at import with "the pinned openDox corpus-adapter interface is not at …openDox/code/src/opendox/corpus_adapter.py", measured in R2-INV-12's first composed run>
2026-10-05T22:40:40Z PLANCHECK T005 item 3 FIX <it quotes R2Q8 (a) verbatim, "composed … until the direction arc's realization lands", while ARC-Q2 (a) (`6003918488`, the later ruling) makes the composed run permanent (T029; plan.md:46). Batch Q should say how the two compose, so F12.1's line does not read as expiring.>
2026-10-05T22:40:40Z PLANCHECK research.md R2 OK
2026-10-05T22:40:40Z PLANCHECK spec.md:1193 FIX <still "174 red across 10 files"; it is 11 files and 5 green suites (210 cases), as plan.md C-1 and R2-INV-P4F's errata record>
2026-10-05T22:40:40Z PLANCHECK tasks.md box accounting Group 12 OK <12.1, 12.1a, 12.2, 12.3, 12.4, 12.4a, 12.5, F12.1, 12.6, 12.6a, F12.2 each map to a task (`tasks.md:1063-1070`)>
2026-10-05T22:40:40Z PLANCHECK R2Q1 OK
2026-10-05T22:40:40Z PLANCHECK R2Q2 OK
2026-10-05T22:40:40Z PLANCHECK R2Q3 OK
2026-10-05T22:40:40Z PLANCHECK R2Q4 OK
2026-10-05T22:40:40Z PLANCHECK R2Q5 OK
2026-10-05T22:40:40Z PLANCHECK R2Q6 OK
2026-10-05T22:40:40Z PLANCHECK R2Q7 FIX <T012 should name, as test nodes, the two refusals R2Q7 (a) adds: a repository with no `main` reads `unknown` and is refused naming it; no declaration refuses naming the exact file and content. F12.2's thirteen guardrail nodes cover neither the no-`main` case nor that wording.>
2026-10-05T22:40:40Z PLANCHECK R2Q8 OK <T005 item 3 encodes the composed line; T020–T029 hold the repair slice>
2026-10-05T22:40:40Z PLANCHECK T011 FIX <`runtime/repository_act.py:1335-1372` is only the repository-local command-config refusal (`_EXECUTED_LOCAL_KEYS` `:1335`, `_refuse_repository_local_command_config` `:1372`). The push core to factor out is `_push_to_remote_with` at `:1742`, with `_bound_local_destination` `:1613` and `_receive_pack_for` `:1720`.>
2026-10-05T22:40:40Z PLANCHECK cites OK <checked at the plan's pins (openDox-code a9ac96f9, openXdox-code 56e1c238; both still `main`): openDox-code `validate.yml:272` (MIN_SELECTED), `:273` (MIN_PASSED), `:306` (EXPECT_SKIPPED "11"); `tests/test_session_git.py:523`, `:563-564`; `session_git.py:99` (with `:93` inside its rule comment); openXdox-code `tests/conftest.py:413-421`; `tests/test_session_snapshot.py:893-916`; `_CREATE_HARNESS` `:492-553`; `_SESSION_HARNESS` `:1008-1094`; T074's "none protected" holds (no governed suite imports `doc_health` directly)>
2026-10-05T22:40:40Z PLANCHECK A NOT REACHED: contracts/cli-http-submit-land.md and data-model.md not checked against the code, nor T008's codexFactory cites; no separate fix-round text found in clarify-questions.md, so R2Q1..R2Q8 were checked against their (a) answers only.
2026-10-05T22:41:17Z PLANCHECK SHARED src/opendox/health_contract.py T045 T041 not same wave: T041 is W1, T045 is W2 and "After: T041" (tasks.md:576 orders T041 → T045)
2026-10-05T22:41:17Z PLANCHECK SHARED src/opendox/contracts/copies.yaml (+ src/opendox/contracts/schemas/) T047 T041/T054 not same wave if waves are strict barriers: T041 W1, T047 W3, T054 W4, but T054 does not depend on T047. The file is unnamed in all three tasks' Files lines; it is openDox-code's registry of digest-checked copies (openDox-code:src/opendox/contracts/copies.yaml:1-5, one `commit:` per file)
2026-10-05T22:41:17Z PLANCHECK SHARED pyproject.toml T048/T055 T061 not same wave: T048 W3 → T055 W4 → T061 W6, ordered at tasks.md:686
2026-10-05T22:41:17Z PLANCHECK T045 OK files: src/opendox/health_contract.py (appended second), tests/test_check_pack_contract.py; no other W2 task writes either
2026-10-05T22:41:17Z PLANCHECK T047 FIX files: src/opendox/check_pack_manifest.py, the schema copy, tests/test_check_pack_manifest.py; also name src/opendox/contracts/copies.yaml (see SHARED). Neither T047 nor contracts/health-packs-manifest.md names 15.1a's refusal of a corpus-relative entry that carries `commit` (#1144 tasks.md:3417-3421)
2026-10-05T22:41:17Z PLANCHECK T048 FIX files: src/opendox/check_pack_sandbox.py, src/opendox/check_pack_shim.py, tests/test_check_pack_sandbox.py, pyproject.toml (first). Not stated: the read-only mount set R2Q18 (a) fixes (the install's interpreter, its standard library and opendox.health_contract only; never site-packages), and where the CI fail-not-skip helper lives. Keep that helper in its own test module, not a shared conftest.py
2026-10-05T22:41:17Z PLANCHECK T049 FIX files: src/opendox/check_pack_patch.py, tests/test_check_pack_patch.py. The task names only "own document" and "base_blob". It must carry 15.2a's full refusal list: absolute path, `..`, `.git` in any case, symlink target or below, create/delete/rename/copy/re-mode/binary headers, and the 65,536-byte bound (#1144 tasks.md:3465-3476). "65,536" appears nowhere in plan.md, data-model.md or contracts/
2026-10-05T22:41:17Z PLANCHECK T049 FIX data-model.md:187: a Patch's `content` may be "the replacement document text, or a unified diff". 15.2a checks each patch "as a unified diff" and refuses by diff headers (#1144 tasks.md:3463-3472). A whole-text form changes the ratified mechanism, so drop it or put it to Brett
2026-10-05T22:41:17Z PLANCHECK T055 FIX files: tests/fixtures/pack-corpus/**, tests/test_pack_corpus_digests.py, pyproject.toml (second). Its pack list (tasks.md:762-765: a well-behaved pack, plus writes / connects / reads outside / forks / hangs / babbles / crashes / restore) is not 15.6a's eight, and batch Q does not amend that list. F15.1 asserts the eight by id: fixture-crashing/slow/writing/escaping/forking/garbage/anonymous/patching-pack. fixture-anonymous-pack (no version) and fixture-patching-pack (patch-ok plus five refused patches) are missing (#1144 tasks.md:3503-3532, :3581-3612)
2026-10-05T22:41:17Z PLANCHECK T055 FIX the escaping pack must also hunt the engine's CANARY environment variable and the CANARY descriptor through /proc/self/fd, and follow a planted symlink (#1144 tasks.md:3511-3515). data-model.md § "Sandbox probe and canary" (:192-199) and contracts/health-packs-manifest.md define the canary only as a write/connect/read self-check
2026-10-05T22:41:17Z PLANCHECK T056 OK files: src/opendox/check_pack_engine.py, tests/test_check_pack_engine.py; it calls T046's hook in health/engine.py without editing it; the patch column comes from T042's 0003_
2026-10-05T22:41:17Z PLANCHECK T058 OK files: tests/test_check_packs.py, single owner; after T005, so it uses batch Q's amended F15.1
2026-10-05T22:41:17Z PLANCHECK validate.yml OK no lane-3 task writes it (T010 → T017 → T051 → T080, all lane 4; plan.md:294)
2026-10-05T22:41:17Z PLANCHECK 0003_ OK T042 is the single owner, with 15.7's NOT NULL columns and `patch` from its first landing; no lane-3 task writes it
2026-10-05T22:41:17Z PLANCHECK cli.py OK no lane-3 writer (T046, T052)
2026-10-05T22:41:17Z PLANCHECK serve.py OK no lane-3 writer (T052, T057)
2026-10-05T22:41:17Z PLANCHECK display facet OK T050 single owner, lane 4
2026-10-05T22:41:17Z PLANCHECK T050 FIX add "After: T045": the pack declaration's label keys are defined there (data-model.md:174-177), but T050 depends only on T027/T033
2026-10-05T22:41:17Z PLANCHECK split OK slices match Part B's outline: G15-A T045, G15-B T047, G15-C T048, G15-D T049, G15-H T050, G15-F folded into T042, G15-G T055, G15-E T056, G15-I split into T010 + T051 + T058. One deviation: G15-A extends health_contract.py instead of a new check_pack.py, which is consistent with R2Q18 (a) and N-3
2026-10-05T22:41:17Z PLANCHECK coverage OK every box 15.1..15.7 (15.1b and 15.6a included) and F15.1 maps to a task (tasks.md box table, lines 22-33 of § Box accounting)
2026-10-05T22:41:17Z PLANCHECK F15 OK batch Q item 1 carries the platform precondition, the forking child's pack id, the unsteerable export and restore-is-a-write (tasks.md:111-118); the built-in canary is T048 plus decision row 23 (plan.md:539), with no text change
2026-10-05T22:41:17Z PLANCHECK R2Q16 OK T052 encodes "a scoped run is not stored; a host's check … runs in process there only"; spec.md:132 carries the full answer
2026-10-05T22:41:17Z PLANCHECK R2Q16 FIX batch Q item 9 (tasks.md:136-137) and plan.md:476 carry only "a host's check is trusted code, not a pack". Encode (a)'s full reading in #1144: the product's own checks run in process, attributed `opendox`; the host check runs at the scoped seam only and is NEVER STORED; the sandbox clause governs manifest-listed packs; the attribution clause is attribution only (clarify-questions.md R2Q16 (a))
2026-10-05T22:41:17Z PLANCHECK R2Q17 OK T010 pins ubuntu-24.04, installs bubblewrap, sets the sysctl, proves the sandbox live, keeps EXPECT_SKIPPED at "11" (validate.yml:306, enforced at :344), adds no macOS job, and defers 26.04 to a measurement
2026-10-05T22:41:17Z PLANCHECK R2Q17 FIX no task owns the 26.04 runner measurement (tasks.md:194 says only "waits"); name an owner, or record that release 2 stays on 24.04 with no measurement task
2026-10-05T22:41:17Z PLANCHECK R2Q18 OK plan.md:478, contracts/health-packs-manifest.md "What a pack may import"; but see the T048 mount-set FIX
2026-10-05T22:41:17Z PLANCHECK R2Q19 OK kept as ratified, no amendment task (plan.md:479; T048)
2026-10-05T22:41:17Z PLANCHECK R2Q20 OK kept as ratified, model-free (plan.md:480; T045)
2026-10-05T22:41:17Z PLANCHECK R2Q21 OK packs.yaml authoritative; the lockstep check is F2's (plan.md:481; T047)
2026-10-05T22:41:17Z PLANCHECK R2Q22 OK T040 → T041/T047/T054 → T060 (plan.md:482); see the copies.yaml SHARED line
2026-10-05T22:41:17Z PLANCHECK R2Q23 OK T061, then T084 LAST (plan.md:483)
2026-10-05T22:41:17Z PLANCHECK R2Q24 OK T080, T081 (plan.md:484)
2026-10-05T22:41:17Z PLANCHECK bwrap-facts OK nothing assumes bwrap works by default: plan.md:98-100, research.md:257-263, spec.md:1276-1292; 26.04 is held as unmeasured
2026-10-05T22:41:17Z PLANCHECK bwrap-facts FIX plan.md:538 (row 22) and contracts/health-packs-manifest.md `processes: 16` use RLIMIT_NPROC as a per-pack bound. setrlimit(2) counts it "for the real user ID of the calling process", not per sandbox. Measure it under bwrap's user namespace before fixing a default; prefer pids.max where a cgroup is delegated
2026-10-05T22:41:17Z PLANCHECK bwrap-facts FIX contracts/health-packs-manifest.md: per-entry `timeout_seconds` and `bounds` are a second source beside 14.5's `health run --timeout`. State which wins, and whether a corpus may raise them above an engine ceiling. 15.6 says the budget is "enforced by the engine rather than by the caller" (#1144 tasks.md:3496-3497)
2026-10-05T22:41:17Z PLANCHECK OQ-H15 OK every R-class OQ-H15 is answered (clarify-questions.md:1082-1092): -2 by R2Q18, -3 by R2Q19, -4 by R2Q20, -6 by R2Q15, -7 by R2Q16, -8 by R2Q17, -9 by a plan default that moves no text (plan.md:539), -13 by R2Q21, -16 by R2Q12, -22 (a)–(d) by R2Q9 items 3–6. No row changes ratified text under a "default" label
2026-10-05T22:41:17Z PLANCHECK cites OK at a9ac96f9 / 0f2a87f6: validate.yml:272 MIN_SELECTED, :306 EXPECT_SKIPPED "11", :344 the enforcement; tests_runtime/conftest.py:130 `_skip_or_fail`; scripts/opendox_host.py:524 register_health_check; #1144 tasks.md:3546, :3427-3428, :3240-3241, :4046-4050; spec.md:557; scripts/doc_health/corpus.py:420, :434, :683
2026-10-05T22:41:17Z PLANCHECK T052 FIX (Group 6, cross-reference) `workbench.py:1542-1557` is the DEFAULT_SCOPED_FAMILIES block; `run_scoped_doc_health` itself is at openDox-code:src/opendox/workbench.py:1666
2026-10-05T22:41:17Z PLANCHECK C NOT REACHED: quickstart.md's Group 15 steps; contracts/health-finding.md beyond its class and baseline rows; T058's 24 node names checked against batch Q's amended wording; how T051's per-wave re-pins interact with lane-3 PRs landing mid-wave; research.md beyond lines 257-263
2026-10-05T22:41:44Z PLANCHECK T042 OK: `0003_` has one owner, HA-1. It carries 15.7's NOT NULL `pack_id`/`pack_version` and the `patch` column from its first landing (tasks.md:579-595; plan.md:220, :308).
2026-10-05T22:41:44Z PLANCHECK T042 FIX: the Decisions line (tasks.md:592) lists OQ-H15-18 and -20 but not -19. R2-INV-HEALTH Part 10 E resolution 5 makes HA-1 wait on all three. Row 30 (plan.md:546) sets what the store must admit: an install-level finding with `pack_id` `opendox` and an empty `path`. Add OQ-H15-19.
2026-10-05T22:41:44Z PLANCHECK T042 FIX: tasks.md:585-587 says all five `tests_runtime/` suites hard-code `["0001","0002"]`. At openDox-code a9ac96f9, only test_runtime_cli.py:277, test_bundled_postgres.py:540 and :924, and test_migrations_apply.py do. test_schema_shape.py's closure reads `0001` only (:36-59), and test_deploy_shape.py derives its lists from `identity.TABLES` (:1850, :2222). Reword it as "the five suites `0003_` moves", with each suite's reason.
2026-10-05T22:41:44Z PLANCHECK T010 OK: N-4 gives validate.yml one owner from day one (plan.md:590, :294): T010 → T017 → T051 → T080. R2Q17's change is the first edit. EXPECT_SKIPPED stays 11 at tasks.md:193, :341, :681 and :708. T010 exports the fail-not-skip switch and T048 uses it (:678). N-4 replaces the inventory's W3 placement of G15-I1 and names that placement as its rejected alternative.
2026-10-05T22:41:44Z PLANCHECK T041 OK: U-0 runs first in W1 and owns the stdlib-only `src/opendox/health_contract.py`, after T040's schema. T045 appends the pack protocol to that file afterwards (tasks.md:633). That departs from Part 10 E resolution 1, but R2Q18 (a)'s "stdlib and the contract module only" justifies it.
2026-10-05T22:41:44Z PLANCHECK plan.md § Parallel slices OK: cli.py runs T014 → T016 → T046 (HA-5) → T052 (HA-4) (plan.md:299). serve.py runs T014 → T015 → T016 → T052 (HA-4) → T057 (HA-8) (plan.md:298). Both match R2-INV-HEALTH Part 12 A.
2026-10-05T22:41:44Z PLANCHECK T057 FIX: its After line (tasks.md:806) omits T052. T052 is serve.py's fourth edit and plan.md:298 orders it before T057's fifth. Add T052; the wave order implies it but does not state it.
2026-10-05T22:41:44Z PLANCHECK Part10E-1 OK: T041 owns the finding vocabulary, and T044 owns the families only (tasks.md:566-578, :610-623).
2026-10-05T22:41:44Z PLANCHECK Part10E-2 OK: G15-I1 is split between T010 and T051 (tasks.md:551-552). G15-I2 is T058, which alone owns tests/test_check_packs.py (:821).
2026-10-05T22:41:44Z PLANCHECK Part10E-3 OK: T050 (G15-H) sits in W3, and T057 waits on T050 (tasks.md:806).
2026-10-05T22:41:44Z PLANCHECK Part10E-4 OK: T046 owns the engine hook (tasks.md:642), and T056 waits on T046 (:782).
2026-10-05T22:41:44Z PLANCHECK Part10E-5 FIX: see T042's Decisions line above (OQ-H15-19 missing).
2026-10-05T22:41:44Z PLANCHECK box 6.1 6.1a 6.2 OK: they map to T052, with 6.2's body in T044 (tasks.md:1071, :723-725).
2026-10-05T22:41:44Z PLANCHECK box 14.1-14.9 OK: T042, T044/T046, T046/T057, T041/T053, T053, T054, T043 (tasks.md:1072-1078).
2026-10-05T22:41:44Z PLANCHECK F6.1 OK: T052 and T065, with batch Q item 1 (tasks.md:1105). #1144 tasks.md:1143 checked at ce64afc9 and at openxFactory origin/main ba89e046.
2026-10-05T22:41:44Z PLANCHECK F14.1 OK: T065, with T005 item 1 (the document server starts first, R2Q9 item 2). That covers `runtime reset`/`runtime migrate` at #1144 tasks.md:3360-3361, checked at both pins (tasks.md:1109).
2026-10-05T22:41:44Z PLANCHECK T005 FIX: item 1 (tasks.md:111-116) and plan.md:469 leave out part of R2Q9 item 1: the note that 6.2's matching description (#1144 tasks.md:1138-1142) is superseded (clarify-questions.md:469). Add it to batch Q.
2026-10-05T22:41:44Z PLANCHECK R2Q10 OK: T041's id rule, `--json` carrying `kind` (T046), and selection by fixture document (T005 item 4; plan.md:470; N-13 at plan.md:599).
2026-10-05T22:41:44Z PLANCHECK R2Q11 OK: role-key top-level directories, and `auto-fix` edits only `stage:` (plan.md:471; T044).
2026-10-05T22:41:44Z PLANCHECK R2Q12 OK: the baseline is the previous default-tip run. Its classes are new, pack-upgrade and persistent. Disappearance is measured only between default-tip runs, with citations and a single uncited re-raise (data-model.md:141-150; spec.md:805-822).
2026-10-05T22:41:44Z PLANCHECK R2Q12 FIX: plan.md:472 and spec.md:128 say "three classes". contracts/health-finding.md:33 and data-model.md:149 add a fourth `baseline_class` value, `unclassed`, from I-2 (plan.md:557), which is a proposal until T004. Name `unclassed` as I-2's in plan.md:472 so the R2Q12 row does not read as a closed three-value enum.
2026-10-05T22:41:44Z PLANCHECK R2Q13 OK: DOMAIN; `identity.TABLES`; the closure reads `0001` with `0003_` in one change (T042; plan.md:473).
2026-10-05T22:41:44Z PLANCHECK R2Q14 OK: 6.1a is satisfied vacuously; T052 records it at the tick (tasks.md:723-725; plan.md:474).
2026-10-05T22:41:44Z PLANCHECK R2Q15 OK: the hosted plane refuses by name and the schema still migrates (T042, T046, T057; plan.md:475).
2026-10-05T22:41:44Z PLANCHECK R2Q25 OK: evidence holds locators only, and the message never quotes the document (T041 at tasks.md:570; contracts/health-finding.md:31-32; plan.md:485).
2026-10-05T22:41:44Z PLANCHECK OQ-H-R OK: every R-tagged OQ-H maps to an R2Q (clarify-questions.md:1070-1081), never to a default row alone: OQ-H-1 → R2Q9 item 1; OQ-H-3 → R2Q16; OQ-H-4 → R2Q13; OQ-H-5 → R2Q15; OQ-H-6 → R2Q9 item 2; OQ-H-7 → R2Q10; OQ-H-9 → R2Q11; OQ-H-12 → R2Q12; OQ-H-17 → R2Q14; OQ-H-19 → R2Q25.
2026-10-05T22:41:44Z PLANCHECK cite T010 OK: validate.yml:272 `MIN_SELECTED "3977"`, :273 `MIN_PASSED "3966"` and :306 `EXPECT_SKIPPED "11"`, at openDox-code a9ac96f9 (still origin/main after a fetch).
2026-10-05T22:41:44Z PLANCHECK cite R2Q9 OK: workbench.py:1594 (`HEALTH_CHECK_NOT_REGISTERED`) and test_health_check_seam.py:143-144, at a9ac96f9.
2026-10-05T22:41:44Z PLANCHECK T052 FIX: workbench.py:1542-1557 is the comment block and constant for `DEFAULT_SCOPED_FAMILIES` (:1557), not `run_scoped_doc_health`. At a9ac96f9 that function is at :1666, and `register_health_check` is at :1622. The wrong cite came from R2-INV-HEALTH Part 12's HA-4 row (:1434); that file's own source line (:135) names the constant.
2026-10-05T22:41:44Z PLANCHECK B NOT REACHED: tasks.md was read at :1-420 and :542-886 plus targeted greps, not in full; plan.md, data-model.md, research.md, quickstart.md and the other four contracts files were read only by grep. Not checked: whether OQ-H-3's default half (plan.md:525, "a scoped run is not stored") or I-2 (plan.md:557) changes ratified #1144 text; the roughly-20-assertion ripple of `0003_`, which was not re-measured; and whether any phase-5 task touches a 12.5 protected suite.
2026-10-05T22:42:30Z PLANCHECK ARC-Q1 OK. Realized by T072 (the generic `lines` slice plus `RealGit`'s few git reads, re-authored in openDox-code), T074 (all eight modules; seams for corpus loading and status reading, `derive_possibles`' index and disposition, the readiness renderer and the pin sentinel; the 7 tests respelled, none protected; `DOC_HEALTH_SURFACE` emptied) and T075 (the host registers the seams). Row 47 makes no `corpus-adapter-seam` change. This matches #656 6003918488 and R2-ARC-ASK option (a).
2026-10-05T22:42:30Z PLANCHECK ARC-Q2 OK. T029 makes the composed workflow permanent, T073 adds the 3 rail files and 5 contracts files as declared integration tests, and T005 item 6 amends F9.1 in batch B's form.
2026-10-05T22:42:30Z PLANCHECK ARC-Q3 OK. T070 names `code_surface:` as openXdox-code, openDox-code and openxFactory host wiring. T071 records the ratify word, T077 archives by merge commit and exits the staged topic. The lane is 4. T005 item 3 keeps F12.1 composed.
2026-10-05T22:42:30Z PLANCHECK ARC-Q4 OK. T006 is done and T005 item 3 keeps the realization off 12.5's path.
2026-10-05T22:42:30Z PLANCHECK T070 OK
2026-10-05T22:42:30Z PLANCHECK T071 OK
2026-10-05T22:42:30Z PLANCHECK T072 FIX T072 is "After: T071" yet must land "before T061" under ARC-6 (a). That makes release 2's 0.2.0 bump (T061) wait on the arc's ratify word, which ARC-Q3 (a) rules out: "It gates neither release 2's close nor #1144's archive" (#656 6003918488). Say that T061 never waits for T072, and that a late T072 rides the arc's own pin, the fallback T074's `pyproject.toml` line already names.
2026-10-05T22:42:30Z PLANCHECK T073 FIX T073 sits in the arc section. That section's preamble says the arc's realization landings carry the arc's own trailer (ARC-4), and T071 says "No realization slice starts before it". But T073 is "Not gated on T071" and is Lane 3, while ARC-Q3 (a) says the arc "is owned by lane openxfactory-4". T073 realizes #1144's requirement 9 (F9.1 as batch Q amends it), so it is #1144 work. Move it out of the arc section, give it #1144's `Arc:` value (11.0) and drop ARC-4 from it. Or, if it belongs to the arc, gate it on T071 and give it to lane 4.
2026-10-05T22:42:30Z PLANCHECK T074 OK
2026-10-05T22:42:30Z PLANCHECK T075 OK
2026-10-05T22:42:30Z PLANCHECK T076 OK
2026-10-05T22:42:30Z PLANCHECK T077 OK
2026-10-05T22:42:30Z PLANCHECK SHARED openXdox-code tests/conftest.py T073 T074 no: not the same wave, because T074 is After T073 (single-writer chain T020 → T073 → T074)
2026-10-05T22:42:30Z PLANCHECK SHARED openXdox-code tests/declared_exclusion.yaml T073 T074 no: not the same wave, because T074 is After T073 (T073 writes first, T074 second)
2026-10-05T22:42:30Z PLANCHECK SHARED openXdox-code .github/workflows/composed.yml T073 T074 no: not the same wave, because T074 is After T073 (chain T029 → T073 → T074)
2026-10-05T22:42:30Z PLANCHECK SHARED openXdox-code tests/test_host_plane.py T073 T074 no: not the same wave; it is in the same single-writer chain as tests/conftest.py
2026-10-05T22:42:30Z PLANCHECK SHARED openXdox-code tests/composed_host_pin.yaml T029 T030,T064 no write overlap (T030 is After T029, and T073 does not write the file). But the file is missing from plan.md's single-writer table even though two lanes write it. T064's pin advance can also land while T073's PR is open, which moves the openxFactory commit T073's composed run checks out, so T073 must re-run after it. Add the file to the table.
2026-10-05T22:42:30Z PLANCHECK MISLABEL row 31 (OQ-H15-20, with row 20's `patch` column) This stores each pack patch, which is document text, in the store. 14.3 says "The store holds NO DOCUMENT and stays DISPOSABLE (Q1's principle, untouched)" (#1144 tasks.md:3233-3235). Brett's R2Q25 (a) on #656 6003486656 chose "Locators only … no text of a document" over option (b), whose own consequence was that "the store then holds fragments of documents". Either re-obtain the patch at `fix` (the row's Alt.), or put it to Brett as a ruling.
2026-10-05T22:42:30Z PLANCHECK MISLABEL row 49 (ARC-5) This lets #1144 archive with F9.2 open. That changes F9.2's ruled notes: #656 5859927858 says "It runs again once the doc_health direction arc (T008) lands. F9.2 is unchanged.", and #656 5870594693 says "T008 removes it together with the workflow deselect". Reconciling those notes with ARC-Q3 (a)'s "gates neither … #1144's archive" settles a conflict between two of Brett's rulings, so it belongs with the RULINGS in T004, not with "the rest as proposals".
2026-10-05T22:42:30Z PLANCHECK MISLABEL row 36 (I-2) This lists every finding UNCLASSED and measures no disappearance in any repository without `main`. That suspends requirement 6's "SHALL be BASELINE-RELATIVE so that new findings get attention while persistent ones stay quiet and an uncited disappearance is re-raised" (#1144 specs/neutral-product-standalone-operability/spec.md:188-190). By C-14, the `git init -q` repository in F14.1 itself may have no `main`.
2026-10-05T22:42:30Z PLANCHECK MISLABEL row 17 (OQ-H-18) Low confidence, since lane 3's inventory classed OQ-H-18 as P. The row reduces "optionally on commit" (#1144 tasks.md:3239-3240; ruling 5784155201: "It runs on demand from the dashboard and the command line and optionally on commit") to a hook line in the documentation, so the product itself gains no on-commit run.
2026-10-05T22:42:30Z PLANCHECK row 47 (ARC-3) FIX The row says an openXdox-spec delta "rides along, as the ruling allows". #656 6003918488 says nothing about an openXdox-spec delta, and ARC-Q3 (a)'s `code_surface:` names openXdox-code, openDox-code and openxFactory host wiring only. Drop "as the ruling allows", or put that delta to Brett.
2026-10-05T22:42:30Z PLANCHECK row 50 (ARC-6) FIX The same problem as T072: ARC-6 (a) puts the arc's ratify word (T071 → T072) ahead of T061, which contradicts ARC-Q3 (a)'s "gates neither release 2's close". Make the arc's own pin the fallback whenever T072 is not ready.
2026-10-05T22:42:30Z PLANCHECK rows 1-5, 7-16, 18-19, 21-27, 29-30, 32-35, 37-46, 48, 51-63 OK. None changes ratified text. Rows 38-41 (R-1, W-1, H-1, H-2), 35 (I-1), 45 (ARC-1) and 57 (N-7, "needs this word") are already put to Brett explicitly. Row 61 (N-11) restates 12.6a's ratified "refuses when there is none" (#1144 tasks.md:2800-2801). Row 60 (N-10) is consistent with F14.1, which commits before each run (#1144 tasks.md:3354-3355). #1144's change directory and the staged topic are unchanged from 0f2a87f6 to openxFactory main ba89e046.
2026-10-05T22:42:30Z PLANCHECK D NOT REACHED: row 28 (OQ-H15-15): whether the display facet's schema-version bump is an openDox-spec schema change beyond R2Q22 (a)'s three; there was no openDox-spec clone to check. Row 6 (OQ-12-16): whether hiding `gh` on the PATH meets F12.2's ratified wording about `gh` being absent. Row 56 (N-6): checked only against plan.md's 9.5 table, not against #1144's 9.5 text on phase order.
2026-10-05T22:42:30Z PLANCHECK SPLIT lane 3 ACCEPTS the proposed split, with three conditions: (1) T020-T026 and T029 as proposed; lane 3 orders its own T021 before T022 because both write a copy record in the same wave (and both need the separate record the T021/T022 FIX asks for, not copies.yaml); (2) the pack track T045, T047, T048, T049, T055, T056, T058 as proposed, provided T054 is ordered After T047 (or T047 After T054), because both write openDox-code src/opendox/contracts/copies.yaml and schemas/ with no dependency between them, and the file goes into the single-writer table; (3) T073 as #1144 requirement-9 work, moved out of the arc section with #1144's Arc value, per the T073 FIX; if it stays arc work it goes to lane 4, gated on T071. Also add tests/composed_host_pin.yaml to the single-writer table. No other file is written by a lane 3 task and a lane 4 task in the same wave
2026-10-05T22:42:30Z PLANCHECK DONE plan 038 at 6d6911e1, four parts (A phase 4, B Groups 6 + 14, C Group 15, D arc + 63 decisions), about 34 FIX lines, 0 MISSING, 4 MISLABEL. For Brett, not defaults: MISLABEL row 31 (stores pack patch text, against 14.3 and R2Q25 (a)), row 49 (ARC-5 archives #1144 with F9.2 open, which reconciles two rulings), row 36 (I-2 UNCLASSED suspends requirement 6 baseline-relative, and F14.1 own repo may have no main), row 17 (low confidence, on-commit run reduced to a doc hook); also T049 FIX: data-model.md:187 whole-text patch form changes 15.2a mechanism. Ordering against ARC-Q3 (a): T072 and row 50 make T061 wait on the arc ratify word; must not. Biggest task fixes: T021/T022/rows 42-43 copies.yaml misuse (from lane 3 P4F's own error), T055 pack list is not 15.6a's eight (anonymous and patching packs missing, canary hunt), T049 refusal list and 65,536-byte bound, T029 recursive submodules, T005 composed-is-permanent wording, row 38 R-1 closes only with W-1, T042 OQ-H15-19 and suite ripple wording, T057 After T052, T050 After T045, R2Q16 full reading in batch Q, R2Q17 26.04 measurement owner, RLIMIT_NPROC is per user not per sandbox. SPLIT accepted with the three conditions above. Read-only; nothing edited, posted or pushed
```
