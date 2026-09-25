# Analyze, round 1a (T006)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T006
([`tasks.md`](../tasks.md)) · **Run**: 2026-09-25, 14:19–15:20Z · **Lane**:
`openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## Verdict

**CRITICAL: 0.** No finding breaks a MUST of the constitution or leaves a
requirement without a task, so phase 1 may start slice by slice, each once it
is claimed (T002). T061 and T043 stay PROVISIONAL until T019 has run, and
phases 2 and 3 until T009 and T069 have.

The analysis found 7 HIGH, 20 MEDIUM and 8 LOW findings. Every one is
dispositioned below. One puts a new question to Brett, R1Q25 (F1). Four leave
the plan as it is (F12, B2, A1 and U4), each for the reason its row gives. The
rest change this revision.

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

## Findings, and what this revision does with each

Severity follows the skill: CRITICAL breaks a constitution MUST or leaves a
requirement uncovered. HIGH is a conflict with the authority, or an acceptance
criterion that cannot be tested. MEDIUM is drift, a missing step or an
underspecified case. LOW is wording.

### HIGH

| ID | finding | disposition |
|---|---|---|
| F1 | The re-plan closes 7.3 and F7.1 in phase 1. #1144's RULED release map (`5799646419`, `5800995035`) puts Group 7 in phase 2, and no question put the move to Brett. It rests on #1155's own contingency. 9.2's phase-3 close is the same kind of reading. | **Put to Brett as R1Q25**, which blocks T019 and T061. spec.md's header, plan.md's Summary, T061, T043, T049 and the checkpoint row now say the move is pending. Under R1Q25 (b), T061 returns to phase 2 and T019 re-plans T043 and T049. |
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
| C3 | The named composition tests grow through an unnamed "later batch" that gates T047 from no `After:` line, and no run at the new pin was planned before T047. | That batch is **batch E**, on T047's `After:` line. T045 starts by running openxFactory's `pytest-suite` at the new openDox pin and names every red test. `test_route_extension.py` and `test_intent_plane_boundary.py:572-588` are the likely ones. |
| C4 | No task owns openXdox-code's reviewed allow-list file, and an entry cannot name its own landing's commit. | T019 gives it to the first task that makes an admitted edit to a protected suite, and an entry names its landing by PR number. |
| E1 | T018, T065, T098 and T096 create evidence records with no README-index step (Principle IV). | Each now links its record from this feature's README entry. |
| D1 | The README linked `analyze-round-1a.md` before it existed. | This note is that file, in the same PR. |
| D2 | The analyze runs of T009, T019 and T069 were recorded nowhere, and T006 was asked for a verdict alone. | T006 records every finding with its disposition, here. T009, T019 and T069 each write `evidence/analyze-<task>.md`. |
| D3 | plan.md row V said every check on the PR was green before any PR existed. | The row now says the PR is green on every check before it lands, and its READY comment quotes them. |
| D4 | The constitution's Repository Constraints had no row. Lifecycle commands run from a private clone, not the git extension's sibling worktree, and nothing named the aggregation pin-sync. | plan.md's Constitution Check gains the row. The clone is a deviation justified in Complexity Tracking, and each openxFactory landing is followed by the aggregation's ordinary, trailer-free pin-sync. |
| C5 | T046 registered a "session-notebook implementation" with T025's seams, but T025 declared none, and where the hosted membership rule came from was unsaid. | Measured: the host's adapter lists 794 documents under `all`, and exactly the notebook's 398 under `documents`. T025 declares where the scope it lists is registered, with `all` as openDox's default. T046 registers `documents`. |
| C6 | The phase-1 `opendox --help` proof named no install, while the default profile now imports `RuntimeSubcommand`. | T038's two runs follow a plain `pip install .`, as F10.1 installs (measured to import). T015's test asserts that the default imports with no extra. |
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

**Unmapped tasks.** T002, T004, T006–T009, T019, T048 and T069 map to no box.
They are the holder's and process tasks, by design.

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
| findings | CRITICAL 0, HIGH 7, MEDIUM 20, LOW 8 |
| new questions for Brett | 1 (R1Q25) |

## The checks after the dispositions

Run from `specs/034-opendox-standalone-operation/`, with the persisted tools:

| check | result |
|---|---|
| `qcheck.py` over `qmap.py` (R1Q1–R1Q25) | `headers checked; mismatches: 0` |
| `depcheck.py` | `tasks: 88 edges: 173`, `cycles: none` |
| `arrowcheck.py` | `arrow mismatches: 0`, 54 arrows |
| `phasecover.py` | every task before its phase's checkpoint; T048 after T049, by design |
| `chaincheck.py` | `single-writer chain gaps: 0` |
| `chaindirect.py` | 25 pairs DIRECT, and `validate.yml`'s T037 → T095 transitive, through the checkpoints |
| `sharedfiles.py` | the coarse check's known pairs, each ordered by a single-writer chain |

The added lines of the PR hold no host-absolute path and no closing keyword.

## Next

- **T019** asks Brett R1Q14, R1Q24 and R1Q25, then encodes, re-plans and
  re-analyzes phase 1's openXdox-code tail. Its findings go in
  `evidence/analyze-t019.md`.
- **G1** (P1-A, P1-B, P1-C and P1-E) starts on its claims. None of the open
  questions reaches it.
