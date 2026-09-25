# Analyze, round 1a (T006)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T006
([`tasks.md`](../tasks.md)) · **Run**: 2026-09-25, 14:19–15:20Z, and the
second pass 15:21–15:43Z · **Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## Verdict

**CRITICAL: 0.** No finding breaks a MUST of the constitution or leaves a
requirement without a task, so phase 1 may start slice by slice, each once it
is claimed (T002). T061 and T043 stay PROVISIONAL until T019 has run, and
phases 2 and 3 until T009 and T069 have. The second pass, over the commit that
carried the first dispositions, found no CRITICAL either.

The first pass found 7 HIGH, 20 MEDIUM and 8 LOW findings. Every one is
dispositioned below. One puts a new question to Brett, R1Q25 (F1). Four leave
the plan as it is (F12, B2, A1 and U4), each for the reason its row gives. The
rest change this revision.

The second pass found 2 HIGH and 1 MEDIUM, and 12 LOW. Copilot's review of the
same commit found 1 MEDIUM, and the author 1 LOW while carrying them. § Second
pass dispositions all seventeen, and each changes this revision. None puts a
new question. One changes R1Q25's recommendation to (b) (V2).

## How it was run

**The feature context.** The prerequisite check was run in a fresh clone of
this branch at `0daaa7f6`, T005's re-plan, where `.specify/feature.json` does
not exist. `<clone>` stands for the clone's root.

Without the feature context:

    $ bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
    ERROR: Feature directory not found. Set SPECIFY_FEATURE_DIRECTORY or run the specify command to create .specify/feature.json.
    ERROR: Failed to resolve feature paths
    (exit 1)

With it:

    $ export SPECIFY_FEATURE_DIRECTORY=specs/034-opendox-standalone-operation
    $ bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
    {"FEATURE_DIR":"<clone>/specs/034-opendox-standalone-operation","AVAILABLE_DOCS":["research.md","quickstart.md","tasks.md"]}
    (exit 0)

The second run also writes the value to `.specify/feature.json`
(`common.sh`'s `_persist_feature_json`). That file is gitignored
(`.gitignore:17`), so the tree stays clean, and a later run in the same clone
resolves without the variable.

**The artifacts.** `spec.md`, `plan.md` and `tasks.md` at `0daaa7f6`, with
`research.md`, `clarify-questions.md` and the two T005 evidence notes as
context. The constitution is `.specify/memory/constitution.md`, version 1.0.0.
The optional `before_analyze` and `after_analyze` hooks, which offer an
automatic git commit, were not run. This feature commits by hand, with
pathspecs.

**Two passes.** The author ran `/speckit-analyze`. An independent Opus
verifier ran it again, read-only, over a separate copy of the same commit. The
two sets of findings are merged below. The verifier's identifiers are kept,
and the author's own findings are `U1`–`U4`. Where both passes found the same
defect, the row names both.

**The second pass.** A second independent Opus verifier then re-ran the
analysis, read-only, over `5192201c`, the commit that carried the first
dispositions. It checked that each was carried, and its findings are
`V1`–`V15`. Copilot's review of the same commit found one more, `CP1`, and
the author found `U5` while carrying them.

**Measurements made for the analysis.** Each was run in a scratch clone, and
none touches a shared tree.
- In a lone openDox-code checkout at `1e4a57fb`, `import opendox.serve` and
  `import opendox.cli` raise `ModuleNotFoundError: No module named
  'ideation_dashboard'`. `opendox.authoring`, `workbench`, `serve_wire`,
  `doxbench_packet`, `domain_profile`, `profile_proxy`, `corpus_adapter` and
  `route_extension` import.
- `python -m pytest -q tests/test_profile_registration.py` gives `30 errors`
  with the root conftest in play, and `30 passed` under `--noconftest`.
- `opendox.runtime.cli`, and its `RuntimeSubcommand`, import under a plain
  `pip install .` (PyYAML alone) and under `.[test]`. With the Group 2 shim,
  `opendox.cli` and `opendox.serve` import under `.[test]`, and only
  `runtime.app`, `runtime.db` and `runtime.oidc` want the `runtime` extra.
- At openxFactory `c415c3d1`, the host's corpus adapter lists 794 documents
  under `all`, 398 under `documents` and 396 under `lifecycle`.
  `doc_health.corpus.load_docs` gives the same 398, each with a `Status:`
  header. `LocalGitCorpus` declares `all` alone.
- With pytest 8.4.2, a file listed in the root conftest's `collect_ignore` is
  skipped by a whole run, but collected when it is named on the command line,
  by file or by node id.
- None of T040's files is protected by 5.4a or 12.5. At openXdox-code
  `e28930bf`, 12.5's `git grep` set has 16 files and 5.4a's glob has 7.
- The carve manifest at `c415c3d1` gives `snapshot.py`'s row one `edits[]`
  entry, and the validator script's row two.
- openXdox-code's plain run at `e28930bf` stops with `57 errors during
  collection`.
- For the second pass: openDox-code's required `validate` job runs
  `tests/test_consumer_reach.py` by name (`validate.yml:394`, at `1e4a57fb`).
  Its `STILL_REACHING` lists `opendox.cli` and `opendox.serve`, and
  `test_the_reaching_modules_are_recorded_as_reaching` asserts that importing
  each one fails. Its message says to move a module that imports into
  `NEUTRAL_MODULES` *"in the same act"*.

## Findings, and what this revision does with each

Severity follows the skill: CRITICAL breaks a constitution MUST or leaves a
requirement uncovered. HIGH is a conflict with the authority, or an acceptance
criterion that cannot be tested. MEDIUM is drift, a missing step or an
underspecified case. LOW is wording.

### HIGH

| ID | finding | disposition |
|---|---|---|
| F1 | The re-plan closes 7.3 and F7.1 in phase 1. #1144's RULED release map (`5799646419`, `5800995035`) puts Group 7 in phase 2, and no question put the move to Brett. It rests on #1155's own contingency. 9.2's phase-3 close is the same kind of reading. | **Put to Brett as R1Q25**, which blocks T019 and T061, and T043 since the second pass (U5). spec.md's header, plan.md's Summary, T061, T043, T049 and the checkpoint row now say the move is pending. Under R1Q25 (b), T061 returns to phase 2, and T019 re-plans T043, T049, T063 and T064 (CP1). Since the second pass, R1Q25 recommends (b) (V2). |
| F2 | This revision said T006 was done while T006 was still `[ ]`, and the checklist and the plan said it was pending. | Resolved in the same PR: T006 is ticked, this note exists, and the checklist item and plan.md's Constitution Check say so. |
| C1 | openxFactory's nightly lane, the refresh lane's seal, and their two tests read openXdox's `find_validator`, `VALIDATOR_RELPATH` and `product_root`. The seal test asserts `find_validator(start) is None` for starts outside the product, which is what F7.1 needs answered otherwise under R1Q14 (a). None of those files is an 11.1 surface. C3's #1157 had to edit three of them. | R1Q14 gains a T006 paragraph that weighs this against (a) and (b). T061 names the files, and the three ways its landing stays lawful. T019 must record which way the answer takes. T047 and P1-K carry whatever T019 decides. Also found by the author (T061's first draft bullet). |
| C2 | F7.1's second named test goes into `test_validate_ideation_dashboard_contracts.py`, a contract-family file whose home R1Q24 decides, yet T061 was not blocked by R1Q24. The test also needs the consumer's validator narrowed from the family's ten schemas to its three, which T061 did not say. | T061 is blocked by R1Q24, and R1Q24's header lists it. R1Q24 gains F7.1's fate under each option: under (a) the listed file still runs the one test by node id (measured), and under (b) batch F moves F7.1's test with it. T061 states the ten-to-three narrowing, and routes its effect on openxFactory's composed validator to T019. |
| B1 | "R1Q12's part" cannot be answered on its own, since R1Q12's recommendation turns on R1Q11. Under R1Q12 (b), T061 would package schemas that T053 re-homes after T049. | R1Q12 no longer holds T061 or T019. T061 packages the three schemas from where they stand when it lands. Under R1Q12 (b), T053 re-homes two of them in phase 2, and the package data follows them in a step T009 plans. R1Q12's header, answer line and a T006 paragraph say so. |
| C7, U1 | Four falsifiers could not pass at their own task's landing. T015 quoted F3.1, which needs T016's registration and T011's import fix. T020 quoted F4.1's first block and its named test, which need T021's routing of `authoring.py:318`. T035 quoted F9.1 whole, which needs T036's `validate.yml` and `testpaths`. T041 quoted F9.1 whole, which needs T043's `validate.yml`, T042 and T061. The verifier rated this MEDIUM and the author HIGH. It is kept HIGH, as a criterion that cannot be tested at landing. | Each falsifier moves to the task that makes it reachable: F3.1 to T016, which already quoted it; F4.1's first block and `test_required_header_fields_come_from_the_registered_adapter` to T021; F9.1 to T036 and T043. Each of the four tasks gets a falsifier it can pass. T015 gets the vocabulary test and a `RuntimeSubcommand` test. T020 gets seam tests: nothing registered is refused `ADAPTER_NOT_REGISTERED`, and a registered factory is what `home()` returns. T035 gets `pytest -q tests/` with the root conftest in play. T041 gets its exclusion test and batch B's three exclusion assertions. `tests/test_authoring_seam.py`'s writer chain becomes T020 → T021 → T022, and the slice rows follow. |
| U2 | Until T011 lands, `opendox.serve` and `opendox.cli` do not import in a lone checkout, and every run with the root conftest in play fails, because the autouse `declared_human_console` fixture imports `opendox.cli`. T010's test, as written, would drive `build_server`, which lives in `serve.py`. Nothing said whether the G1 slices add their new tests to `validate.yml`'s `--noconftest` list, where four parallel slices would collide. | Phase 1 gains a note. A test from a task that can land before T011 (T010, T015, T020, T025, T026 and T027) imports neither module, and its PR quotes a `--noconftest` run. A module it cannot import it may read with `ast`. No slice edits openDox-code's `validate.yml` before T036, and plan.md's single-writer table gains that file (T036 → T037, then T095). T010's test drives the facet in `src/route_extension.py`, and T011's PR adds a `build_server` case. |

### MEDIUM

| ID | finding | disposition |
|---|---|---|
| F3 | Batch C "waits on nothing", yet T019 sent R1Q14's amendment to it. The rule that C lands before the first protected-suite edit sat on no `After:` line. | T019's amendments are a new **batch F**. T061 and T043 now wait on T007's batches C and F. |
| F4 | T049's `After:` left out batch D, which is due before T049. | T049 and the checkpoint row name batch D, if RN-1 is ruled (a). |
| C3 | The named composition tests grow through an unnamed "later batch" that gates T047 from no `After:` line, and no run at the new pin was planned before T047. | That batch is **batch E**, on T047's `After:` line. T045 starts by running openxFactory's `pytest-suite` at T047's new openDox and openXdox pins (V5), and names every red test. `test_route_extension.py` and `test_intent_plane_boundary.py:572-588` are the likely ones. |
| C4 | No task owns openXdox-code's reviewed allow-list file, and an entry cannot name its own landing's commit. | T019 gives it to the first task that makes an admitted edit to a protected suite, and an entry names its landing by PR number. |
| E1 | T018, T065, T098 and T096 create evidence records with no README-index step (Principle IV). | Each now links its record from this feature's README entry. |
| D1 | The README linked `analyze-round-1a.md` before it existed. | This note is that file, in the same PR. |
| D2 | The analyze runs of T009, T019 and T069 were recorded nowhere, and T006 was asked for a verdict alone. | T006 records every finding with its disposition, here. T009, T019 and T069 each write `evidence/analyze-<task>.md`. |
| D3 | plan.md row V said every check on the PR was green before any PR existed. | The row now says the PR is green on every check before it lands, and its READY comment quotes them. |
| D4 | The constitution's Repository Constraints had no row. Lifecycle commands run from a private clone, not the git extension's sibling worktree, and nothing named the aggregation pin-sync. | plan.md's Constitution Check gains the row. The clone is a deviation justified in Complexity Tracking, and each openxFactory landing is followed by the aggregation's ordinary pin-sync, which carries no `Arc:` trailer (V11). |
| C5 | T046 registered a "session-notebook implementation" with T025's seams, but T025 declared none, and where the hosted membership rule came from was unsaid. | Measured: the host's adapter lists 794 documents under `all`, and exactly the notebook's 398 under `documents`. T025 declares where the scope it lists is registered, with `all` as openDox's default. T046 registers `documents`. |
| C6 | The phase-1 `opendox --help` proof named no install, while the default profile now imports `RuntimeSubcommand`. | T038's two runs follow a plain `pip install .`, as F10.1 installs (measured to import). They also show that the default imports with no extra, which a pytest run cannot, since it always has the `test` extra (V14). |
| F5, U3 | Between T016's landing and T038's, main would register a default profile that contributes no verbs, which is R1Q4 (b), refused. Found by both passes. | T015 puts `RuntimeSubcommand` in the default's `SUBCOMMAND_EXTENSIONS` from its first landing. T038 adds the console script, and P1-H's file list drops the extension tuple. |
| F6 | T097 would tick 9.2, whose text still says whole suite, while FR-006 keeps the exclusion open to the archive. Batch B did not amend 9.2. | Batch B gains a 9.2 addendum. T097 ticks 9.2 with an open-extraction note, and requirement 9 stays open for openXdox-code until T008's arc lands. |
| C8 | The re-measure's own experiment found an eighth file that reaches openxFactory's contracts, `test_doxbench_blank_reason.py`, but R1Q24 listed seven. | R1Q24 is now about the two classes, and T043's triage at T040's pin names the files. spec.md's edge case says so. |
| C9 | That T016 clears `test_snapshot_validation_launch.py`'s `ProfileNotRegistered` was not measured, and a protected suite left red has no lawful bucket. | T043 notes that the suite builds its parser through `build_parser()` (`:98`), which T016 makes register the default. That was read, not run. A protected suite still red for a cause no bucket takes stops T043, and the holder raises it as a question. |
| C10 | T019's re-plan list left out T008, T027, T046 and T085, which R1Q24's options change, and it included tasks that may land first. | T019 re-plans every task its answers touch that has not landed. A landed task's change rides with the next task on its files. |
| F7 | plan.md still called C4's runbook work in progress. | It now names `docs/openxdox-pin-resync-runbook.md`, landed as #1154. |
| F8 | The re-measure gave `snapshot.py`'s row two `edits[]` entries. | Measured one. The second entry #1153 added is on the validator script's row. Corrected. |
| F9 | R1Q12's answer line said phases 2–3 while its header named phase 1. R1Q6 and R1Q7 quoted moved figures with no "Re-measured" paragraph. | R1Q12 is phases 2–3's again (B1), so its header and answer line agree. R1Q6 and R1Q7 gain their paragraphs. |
| F10 | The lanes of the task headings and the slices share letters and differ: lane D is slice P1-E. | The slice section maps the two. |

### LOW

| ID | finding | disposition |
|---|---|---|
| F11 | R10 said 57 collection errors while R11 said the new suite also fails plainly. | 57 stands: the new suite fails at setup, not at collection (the plain run stops with `57 errors during collection`). R11's cell says so. |
| F12 | 7.3 is tagged US4 though it changes the consumer's lookup. | **No change.** US4's independent test already names F7.1, and the consumer is part of the composition openxFactory runs. |
| B2 | Some plan surfaces use deferred names, such as the default-profile module or the exclusion file. | **No change.** Each is named by the task that creates it (T015, T041), and the allow-list's owner is set by T019 (C4). |
| F13 | R1Q22's list claimed every carved-file task, and missed some. | T037 and T044 now carry `Ruled: R1Q22 (a)`, and R1Q22's header lists them. T009 and T069 add the line to T056, T058, T075 and T085. |
| D5 | plan.md said every feature file carries `Status: draft`, but `evidence/` is `record`. | Reworded. |
| C11 | The re-measure recorded no digest for `classify_whole_suite.py` or the shim. | Both recorded (`3a76945d…`, and `e00c4c5f…` for the shim's one non-empty file). |
| A1 | Two copies of the start-state block, in `tasks.md` and `clarify-questions.md`. | **No change.** Both are accurate once F2 is resolved, and each serves its own file's reader. |
| U4 | `runtime/cli.py` also ships `ProjectSubcommand`, § 3.6's `project create-repository`, whose docstring names the same assembly line. R1Q5 (a) names `RuntimeSubcommand` alone. | **Recorded, not resolved.** T015 carries only what R1Q5 (a) names, so the `project` verbs stay on the `opendox-runtime` alias. No release-1 falsifier reaches `opendox project`. Whether the default should carry them too is Brett's to say, if he wants it asked. |

## Second pass: the re-verification of `5192201c`

The second verifier checked every first-pass disposition against the files and
against the sources, and re-ran the tools. Five were not carried in full: C2
and C1's file list, C3, F10, U2, and this note's checks table. V2, V4 and V5,
V10, V1, and V8 and V9 carry them. It confirmed the rest from source, among
them #1157's three files, `build_parser()` at
`test_snapshot_validation_launch.py:98`, the runbook's landing as #1154, the
manifest's `edits[]` entries, the recorded digests, and pytest 8.4.2's
collection of a named file that `collect_ignore` lists.

| ID | severity | finding | disposition |
|---|---|---|---|
| V1 | HIGH | T011 could not pass openDox-code's required `validate` check. The check runs `tests/test_consumer_reach.py` under `--noconftest`, and the file fails as soon as `opendox.cli` and `opendox.serve` import, asking for both to move into `NEUTRAL_MODULES` *"in the same act"*. The plan left the file to T034, which comes after T011. U2's rule, that no slice edits `validate.yml` before T036, removed the only other way out. | T011's PR moves the two modules into `NEUTRAL_MODULES`, and its falsifier names the file. T034 re-derives the rest of `STILL_REACHING`. plan.md's single-writer table gains the file (T011 → T034), and P1-A's files list it. |
| V2 | HIGH | T061's narrowing of the consumer's validator, from the family's ten schemas to its three, was weighed only for openxFactory's nightly lane. Three phase-1 callers still validate other kinds through the same script: openDox-code's `workbench.py:442` (`validate_manifest`), openxFactory's `doxbench_contracts.delegated_semantic_validation`, and `tests/ideation-dashboard/conftest.py`'s `find_openxfactory_validator`, which `test_lens.py` uses. R1Q25's recommendation, (a), did not weigh them. | T061 names the three callers, and T019 records what the answer means for each. P1-K and T047 add their tests (`test_doxbench_contracts.py` and `test_lens.py`) as named composition tests if batch E names them. R1Q25's **Measured** gains the fact, and its recommendation is now **(b)**: the map keeps 7.3 beside openDox's own validator, which arrives with T057 and T058 in phase 2. |
| V3 | MEDIUM | `After: T007 (batches C and F)`, on T061 and T043, is read by the tools as all of T007. That makes T041 an ancestor of T061, against the plan's T061 ∥ T041–T042. | tasks.md § Format now says that such an entry waits for the named batches alone, and that the tools read it as all of T007, so their graph is the stricter one. A task that waits on some of T007's batches may still run beside a task another batch waits for. |
| V4 | LOW | plan.md and tasks.md still gave T047 batch A alone, T049 no batch D and T061 no batches C and F, and plan.md spoke of three batches. | They now say A and E; D; C and F. plan.md lists the six batches, A–F, and what each carries. |
| V5 | LOW | T045 ran `pytest-suite` at the new openDox pin only, while the red tests T061 causes arrive with the openXdox pin. | It runs at T047's new openDox and openXdox pins. C3's row says so too. |
| V6 | LOW | P1-K, an arc slice, listed `nightly_lane.py` and the refresh lane's seal. Neither is an 11.1 surface, and T047 never edits them. | P1-K and T047 list only the tests, as named composition tests if batch E names them. No arc landing edits the scripts. |
| V7 | LOW | T021's named test runs with the root conftest in play, so it needs T011, but T021 waited on T020 alone. | T021 is `After: T020, T011`, and its falsifier says why. |
| V8 | LOW | This note's checks table gave `edges: 173` where the tool printed 172 at `5192201c`. It also said `validate.yml`'s transitive pair ran through the checkpoints, where the printed path runs through the root pins. | Corrected in § The checks. The count is 173 again now, from V7's new edge. |
| V9 | LOW | This note's unmapped-task list left out T003 and T005, and the tasks that map only to an FR or an SC. | Completed in § Coverage. |
| V10 | LOW | The slice section mapped lane B to P1-B, but lane B also holds T017, which is P1-L's. | It reads "Lane B is P1-B, less T017, which is P1-L's". |
| V11 | LOW | plan.md and this note called the aggregation pin-sync trailer-free, but the lane protocol puts `Lane:` on every commit. | Both now say it carries no `Arc:` trailer. tasks.md and plan.md name the `Arc:` trailer wherever they meant it, batch A's 11.0 addendum among them, which now matches the ruling's words (*"do not carry the `Arc:` trailer"*). |
| V12 | LOW | R1Q25 (b) had batch B's F9.1 admit the new exclusion reason. T019 sends every such amendment to batch F, and batch B may already have landed. | R1Q25 (b) says T007's batch F amends F9.1. |
| V13 | LOW | Three places stated 7.3's move with no R1Q25 caveat: T063, the phase-2 line of § Dependencies, and plan.md's phase-3 row for 9.2's close. | Each carries the caveat. plan.md's phase-2 row lists 7.3 and F7.1 if R1Q25 is ruled (b). |
| V14 | LOW | T015's falsifier asserted that the default profile imports with no extra. No pytest run can show that, since the `test` extra is always installed. | That half moved to T038, whose two runs follow a plain `pip install .` into a fresh venv. T015 keeps the vocabulary test and the `RuntimeSubcommand` test. |
| V15 | LOW | plan.md said T005's re-measure and T006's analyze raised the three open questions, but R1Q14 dates from round 1. | It says "raised or brought in", as the checklist does. |
| CP1 | MEDIUM | Copilot, on T064's note: T061 precedes T047 only while R1Q25 keeps it in phase 1. Under (b) T061 returns to phase 2, so T064's note must be conditional, and phase 2 must restore F7.1. | T064's note is conditional on R1Q25. Under (b), T019 puts T061 back on T064's `After:` line and gives it back its own `After: T049, T009`, with F7.1 back in T063. T063's note and T019's re-plan list say so, and spec.md's SC-002 has F7.1 exit 0 in phase 2 if R1Q25 returns 7.3 there. |
| U5 | LOW | The author, while carrying V2 and V12: under R1Q25 (b), T043's exclusion declares `tests/test_snapshot.py`, so T043's content turns on R1Q25. Yet T043 was blocked by R1Q24 alone, and waited on R1Q25 only through T019 and T061. | T043 is blocked by R1Q24 and R1Q25, and says why. R1Q25's header, the start-state block and its table, plan.md's Summary and Workflow row, and P1-J's row list T043. R1Q25 (b) now says that it widens R1Q6 (d)'s `doc_health`-only exclusion, as R1Q24 (a) would, so the answer is what admits it. |

## Coverage

| key | tasks | note |
|---|---|---|
| FR-001 | T010, T011, T030, T031, T032, T036, T049 | |
| FR-002 | T001, T015, T016, T017, T049 | RN-1 holds its report |
| FR-003 | T012, T020–T022, T025–T027, T046, T055, T084–T086, T089 | |
| FR-004 | T050, T052–T056, T059, T060, T063 | provisional |
| FR-005 | T051, T053, T057, T058, T061, T049, T063 | T061 waits on R1Q14, R1Q24 and R1Q25 |
| FR-006 | T034–T037, T040–T044, T086, T090, T049 | |
| FR-007 | T038, T075–T077 | |
| FR-008 | T070–T074 | provisional |
| FR-009 | T034, T078–T083, T085 | provisional |
| FR-010 | T017, T018, T045, T065, T091–T093, T098 | |
| FR-011 | T095, T096 (T088 is its precondition) | |
| FR-012 | T002, T009, T019, T069, and every `Blocked by:` line | process |
| SC-001–SC-007 | T049, T063, T089, T095 and T096, T018, T065 and T098, T097, T047, T064 and T094 | |

All 69 release-1 boxes map to a task. `box_census.py` over #1144's `tasks.md`
still prints `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`.

**Unmapped tasks.** T002–T009, T019, T048 and T069 map to no box. They are
the holder's and process tasks, by design. T018, T065, T088 and T095–T098 map
to no box either, and each maps to an FR or an SC in the table above (V9).

## Constitution alignment

No finding breaks a MUST at this revision.
- **I–VII.** No committed host-absolute path, and no credential. The new
  evidence documents are linked from the README entry (IV). `git diff --stat
  c415c3d1 -- openspec/` is empty. `openspec validate --all --strict` gives
  `111 passed, 1 failed (112 items)`. The one failure is `add-chain-attestation`,
  an accepted disposition in `contracts/openspec-cli-pin.yaml`, and the
  enforced gate, `scripts/validate-openspec-cli-pin.py --all`, exits 0 (V).
- **The workflow gate.** Phases 2–3, T061 and T043 are planned while their
  questions are open. That is the deviation plan.md § Complexity Tracking
  justifies, as the Governance section requires, and those parts authorize no
  implementation.
- **Repository Constraints.** The new row and its Complexity Tracking entry
  (D4).

## Metrics

| metric | value |
|---|---|
| requirements | 19 (12 FR, 7 SC) |
| tasks | 88, T001–T098 with ten ids unused; five done (T001, T003–T006) |
| coverage | 19 of 19 |
| ambiguities | 2 (B1, B2) |
| duplications | 1 (A1) |
| findings, first pass | CRITICAL 0, HIGH 7, MEDIUM 20, LOW 8 |
| findings, second pass | CRITICAL 0, HIGH 2, MEDIUM 1, LOW 12 (V1–V15) |
| findings, Copilot's first review | MEDIUM 1 (CP1) |
| findings, the author while carrying them | LOW 1 (U5) |
| new questions for Brett | 1 (R1Q25), recommended (b) since the second pass |

## The checks after the dispositions

Run from `specs/034-opendox-standalone-operation/` after both passes'
dispositions, with the persisted tools:

| check | result |
|---|---|
| `qcheck.py` over `qmap.py` (R1Q1–R1Q25) | `headers checked; mismatches: 0` |
| `depcheck.py` | `tasks: 88 edges: 173`, `cycles: none` (172 at `5192201c`; V7 adds T021's edge to T011) |
| `arrowcheck.py` | `arrow mismatches: 0`, 54 arrows |
| `phasecover.py` | every task before its phase's checkpoint; T048 after T049, by design |
| `chaincheck.py` | `single-writer chain gaps: 0` |
| `chaindirect.py` | 25 pairs DIRECT, and two transitive: `validate.yml`'s T037 → T095, through the root pins (`T095 → T076 → T087 → T062 → T039 → T037`), and `test_consumer_reach.py`'s T011 → T034, through T032 |
| `sharedfiles.py` | the coarse check's 4 known NOT ORDERED pairs (`serve.py` and `cli.py` among P1-A, P1-B and P1-D; `pyproject.toml` between P1-H and P1-G), each ordered by a single-writer chain |

The added lines of the PR hold no host-absolute path and no closing keyword.

## Next

- **T019** asks Brett R1Q14, R1Q24 and R1Q25, then encodes, re-plans and
  re-analyzes phase 1's openXdox-code tail. Its findings go in
  `evidence/analyze-t019.md`.
- **G1** (P1-A, P1-B, P1-C and P1-E) starts on its claims. None of the open
  questions reaches it.
