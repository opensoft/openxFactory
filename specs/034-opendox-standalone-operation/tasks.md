# Tasks: openDox standalone operation (release 1)

Status: draft

**Input**: [`spec.md`](./spec.md), [`plan.md`](./plan.md), [`research.md`](./research.md),
[`clarify-questions.md`](./clarify-questions.md), and #1144's ratified
`openspec/changes/add-neutral-product-standalone-operability/tasks.md`, which
holds the boxes and every falsifier.
**Lane**: `openxfactory-4`

## Format

`- [ ] T### [P?] [US#] [repo] Title`, followed by up to seven lines:

- **Realizes**: the #1144 boxes the task closes, or advances when marked
  "(part)".
- **Falsifier**: the #1144 falsifier or named test the task must pass, quoted
  in its PR.
- **Blocked by**: the open `R1Q` questions, if any. No task starts while one
  of these is open (FR-012).
- **Ruled**: the answered `R1Q` questions whose answers the task carries out.
  All eleven were answered on `#656`, comment `5817152735` (2026-09-24T15:31:46Z,
  verbatim *"(a) on all eleven, (d) on R1Q6"*). A ruled question no longer
  blocks.
- **Ruling needed**: a change to #1144's requirement or scenario TEXT that an
  answer implies. It goes back to Brett Heap (plan.md § "Ruling needed"), and
  it holds only the part of the task it names.
- **After**: tasks that must land first.
- **Lands with**: a task whose change rides in the same PR. Neither task waits
  for the other, so neither names the other on its `After:` line.

A task with no `[P]` either shares a file with a neighbour or depends on one.

- **Stories**: US1 (it runs), US2 (useful alone), US3 (installs) and US4 (the
  governed host unchanged). Holder tasks carry no story tag.
- **Repositories**:
  - `[oDc]` opensoft/openDox-code
  - `[oXc]` opensoft/openXdox-code
  - `[oD]` opensoft/openDox (root)
  - `[oX]` opensoft/openXdox (root)
  - `[oxF]` opensoft/openxFactory
  - `[oDs]` opensoft/openDox-spec
  - `[oXs]` opensoft/openXdox-spec (only under R1Q12 (b); see T053)
- **Falsifier labels**: `F<g>.<n>` is the n-th `FALSIFIED BY` box of #1144's
  Group g, in document order. `research.md` § Appendix `box_census.py` prints
  every label.

Every realization task lands through its repository's own PR, with the `Arc:`
and `Lane:` trailers (T091). Only the holder lands. Every writer works in its
OWN clone, runs `cd <clone> || exit 1` in every call, and names the repository
with `-R` in every `gh` call.

## What can start

Brett Heap answered the eleven questions that blocked phase 1 (`#656`, comment
`5817152735`, verbatim *"(a) on all eleven, (d) on R1Q6"*). T004 encoded them
in this revision, so **no phase-1 task is blocked by an open question**.

- **The holder starts now**: T002, T003, T005, T008, and T007's batches A and C.
  T007's batch B waits on T041, T006 follows T003 and T005, and T004 is
  done.
- **Each phase-1 task** starts once T006 has found no CRITICAL issue and its
  slice has been claimed (T002). **T020** and **T030** never needed an answer.
  **T030** lands with T011, because it fails until 2.1 lands.
- **Phase 1's CLOSE** (T049) also waits on RN-1, a ruling on a scenario's text
  (plan.md § "Ruling needed").

**Phases 2 and 3 are PROVISIONAL.** They are an outline and authorize no
implementation. They wait on R1Q10–R1Q19 and R1Q23, which stay OPEN. Each
opens with its own round task: T009 for phase 2 and T069 for phase 3. That task
encodes the phase's answers, re-plans the phase, and re-runs analyze before
any other task of the phase starts (plan.md § Summary).

---

## Phase 0: preconditions (holder)

- [x] T001 [oxF] **Ratification record, and 3.0.** DONE: #1151 landed as
  `cd494e4c` (2026-09-24T14:54:27Z), under its own Rule 6 window. It ticks 1.8
  and 3.0, citing `5815412869` (*"ratify #1144"*, which struck nothing) and
  `review/ratification-2026-09-24.md` § 2.
  - **Realizes**: 3.0.
- [ ] T002 **Claims, per slice.** Post a `CLAIMED` on `#656` before each slice's
  PR (Rule 1), naming its task ids. Do the three sibling reads first:
  - the claims on `#656`;
  - `gh pr list -R <repo> --state all --search <slug>`;
  - `git ls-remote --heads origin | grep <slug>`.

  Lane 4's C3 and C4 have landed, so a slice starts from them and duplicates
  neither (plan.md § "In-flight overlaps").
- [ ] T003 **ARC_BASE.** Record, per repository, a `main` commit before the
  arc's first landing there: openDox-code, openXdox-code, openDox, openXdox,
  openxFactory, openDox-spec and openXdox-spec. The two spec legs' bases are
  recorded unconditionally, so they are already in place if T009 later selects
  T053; under R1Q12 (b), re-homing the snapshot schema also touches
  openXdox-spec. Any commit before a repository's first arc landing serves:
  `$ARC_BASE..HEAD` leaves ARC_BASE itself out, and the guards read only
  trailered landings. So it is recorded now, before phase 1 starts. For
  openxFactory's guard,
  `PACKET_MERGE` is `94b6f7f1` (11.1). Record them in `evidence/arc-base.md`,
  with no `Arc:` trailer.
  - **Ruled**: R1Q20 (a), `5817152735`.
- [x] T004 **Round 1a: encode the eleven phase-1 answers.** DONE in this
  revision. The answers of `5817152735` (R1Q1–R1Q9, R1Q20, R1Q22) are in
  `spec.md` § Clarifications, in `clarify-questions.md`, and in this file as
  `Ruled:` lines.
  - Every answer that amends a #1144 falsifier or task line is handed to T007.
  - The one scenario text an answer touches is RULING NEEDED RN-1 (plan.md
    § "Ruling needed").
  - Phase 1 is re-planned on the answers.

  The later rounds are T009 (phase 2) and T069 (phase 3).
- [ ] T005 **Re-measure.** Re-run research R1–R15 at the then-current `main`s,
  using the persisted tools. Record the drift from the 2026-09-24 figures in
  `evidence/remeasure-<date>.md`, with no trailer (R13 already shows one pin
  drifting). A figure that moved re-plans the slice it feeds, before T006.
  - It runs openXdox-code's WHOLE suite at the then-current tip, not only the
    22 protected suites research ran under the shim, and records whether
    `tests/test_snapshot.py`'s three failures (research R11) cleared once C3's
    PR 2 landed (T043).
- [ ] T006 **Analyze round 1a.** Run `/speckit-analyze` over spec, plan and
  tasks. No CRITICAL finding may stand before any phase-1 task starts (the
  constitution's workflow gate).
  - First set the feature context. `.specify/feature.json` is gitignored, so
    a fresh openxFactory clone has no feature pointer, and the prerequisite
    resolver refuses without one. Run from that clone, with this feature's
    files at the branch's head or on `main` once #1155 lands:

        export SPECIFY_FEATURE_DIRECTORY=specs/034-opendox-standalone-operation
        bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

    The check must print this feature's `FEATURE_DIR` before analyze runs.
  - Record that output and analyze's verdict in
    `evidence/analyze-round-1a.md`, with no trailer.
  - T003, T005 and T006 can land their evidence together, in one bookkeeping
    PR. It touches only this feature's directory, so it needs no Rule 6
    window.
  - **After**: T003, T004, T005.
- [ ] T007 [oxF] **Record the ruled amendments in #1144's `tasks.md`, and one
  addendum in its `design.md`.** The answers of `5817152735` amend falsifiers,
  task lines and one design note (§ D4). They amend no requirement and no
  scenario. The full list is in § "Ruled amendments" below. Each batch is its
  own bookkeeping PR. Batch D, below, carries scenario text, and only on
  Brett's ruling of RN-1.
  - Every PR touches `openspec/changes/`, so it lands under a Rule 6
    `LANDING`/`LANDED` window.
  - It carries no `Arc:` trailer (R1Q20 (a)), so 11.1's guard never reads it.
  - It carries no closing keyword. It cites `5817152735` in each amended line.

  - **Batch A** holds the F3.1, 2.2, 3.2, 4.3, 10.1, 11.0, 11.1 and F11.1
    amendments. It lands before T047, whose openxFactory landing edits the
    parity test that batch A names in F11.1, and so before T049.
  - **Batch B** holds F9.1 for openXdox-code, and 9.4. It lands once T041
    names its exclusion file, and before T049.
  - **Batch C** holds F5.2 and 12.5's falsifier. It lands before the first
    respelling edit to a protected suite, and before T059, whose falsifier
    reads the allow-list.
  - **Batch D**, only if Brett rules RN-1 (a): requirement 3's fourth scenario
    as ruled, and the added after-build refusal scenario, in #1144's spec
    delta. It lands before T049.

  A realization PR that lands before its batch still quotes the falsifier as
  the answer records it, citing `5817152735`.
  - **Realizes**: none of the 69 boxes. It records the word the realization
    carries out.
  - **Ruled**: R1Q1, R1Q2, R1Q3, R1Q5, R1Q6, R1Q7, R1Q9, R1Q20 and R1Q22,
    `5817152735`.
  - **After**: batch A and batch C wait on nothing. Batch B waits on T041,
    which names the exclusion file. Batch D waits on RN-1's ruling.
- [ ] T008 **Raise the `doc_health` direction arc (R1Q6 (d)).** R1Q6 (d)
  makes the direction question its own arc: openXdox-code's modules import
  openxFactory's `doc_health`, and openxFactory packages nothing (research
  R10). The arc must be decided before 12.5 (release 2) needs the 16 governed
  suites to run, or before phase 2 closes if R1Q23 is answered (b). The
  holder files it as a staging topic or a proposal, which cites `5817152735`
  and names that deadline.
  - **Ruled**: R1Q6 (d), `5817152735`.
- [ ] T009 **Phase 2's round.** Run it once Brett has answered phase 2's
  questions. No task of phase 2 starts before it is done.
  - Encode the answers in `spec.md` § Clarifications and
    `clarify-questions.md`.
  - Hand every #1144 falsifier or task-line amendment to a T007 batch. Bring
    any requirement or scenario text back as RULING NEEDED.
  - Re-plan phase 2 in `plan.md` and in this file, and lift its PROVISIONAL
    marker.
  - Run `/speckit-analyze` with T006's feature context, and find nothing
    CRITICAL.
  - **Blocked by**: R1Q10, R1Q11, R1Q12, R1Q13, R1Q14, R1Q23.
  - **After**: T004.

---

## Phase 1: it runs (US1 and US4)

**Goal**: openDox-code imports, builds its parser on its own default profile,
registers its own default adapter, and runs its whole suite green. openXdox-code
runs its whole suite green less the declared `doc_health` exclusion, which is
reported with its count and its reason (R1Q6 (d)). The `opendox` console
script exists. openxFactory is unchanged in behaviour.

**Independent test**: T049.

### Lane A: the route seam (`src/opendox/serve.py`, `src/route_extension.py`; single writer)

- [ ] T010 [US1] [oDc] **Declare the handler-contribution facet (R1Q1 (a)).**
  A profile or an extension declares the mixin classes that hold the methods
  its bindings name. `build_server` composes them into
  `BoundDashboardHandler`'s bases. `resolve_handlers` is unchanged, so every
  binding is still checked against the class that will dispatch it, and no
  core module names a contributor. Tests:
  - a binding naming a method that only a contributed mixin has resolves;
  - a binding naming a method no class has is refused at wiring time.
  - **Realizes**: 2.2 (the mechanism).
  - **Falsifier**: a new `tests/test_route_handler_contribution.py`.
  - **Ruled**: R1Q1 (a), R1Q22 (a), `5817152735`. The edits to carved files
    need no declared-edit act.
  - **After**: T006.
- [ ] T011 [US1] [oDc] **Remove the two import-time reaches.**
  - Delete `serve.py:199` and the `:206` re-export block (2.1).
  - Take `serve_openxfactory_lanes.LaneRoutes` off `DashboardHandler`'s bases.
  - Move every openDox-side reader of the five names to the lanes column's own
    spelling, or to a neutral one (2.2).
  - Do NOT vendor the module (2.1a).
  - Land T030 in the same PR.
  - **Realizes**: 2.1, 2.1a, 2.2 (openDox half).
  - **Falsifier**: F2.1's generated sweep; `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`.
  - **Ruled**: R1Q1 (a), R1Q22 (a).
  - **After**: T010.
- [ ] T012 [US1] [oDc] **`serve.py:713`** (`doc_health.corpus.RealGit` in
  `_head_of`). Replace it with openDox's own HEAD reader. It must keep
  degrading to `None`.
  - **Realizes**: 4.3 (1 of the 8 reaches into openxFactory).
  - **Falsifier**: F4.1's scan no longer lists `serve.py:713`.
  - **Ruled**: R1Q22 (a).
  - **After**: T011.

### Lane B: the default profile

- [ ] T015 [P] [US1] [oDc] **Ship openDox's default profile for its own domain**
  (documents and ideas).
  - It carries none of openxFactory's `Status:` taxonomy, change/spec/delta
    nouns or act verbs, and its `DISPLAY` is `NEUTRAL_DISPLAY` unchanged.
  - It contributes openDox's OWN verbs and routes (R1Q4 (a)). For now that
    means the runtime verbs, through `RuntimeSubcommand` in its
    `SUBCOMMAND_EXTENSIONS` (R1Q5 (a), wired by T038). Release 2 adds its
    `submit`, `land` and `health`. It is never an empty default (design.md
    § D5).
  - A test holds the vocabulary out (requirement 3, second scenario).
  - **Realizes**: 3.1.
  - **Falsifier**: F3.1; the new vocabulary test.
  - **Ruled**: R1Q4 (a), R1Q5 (a).
  - **After**: T006.
- [ ] T016 [US1] [oDc] **Registration semantics (R1Q3 (a)).**
  - `build_parser()`, `build_server()` and `main()` REGISTER the default where
    nothing is registered, so `is_registered()` then answers True. The default
    is an entry-point registration and never a fallback inside `current()`.
  - A bare process that builds nothing still meets `ProfileNotRegistered`,
    which is the library caller's case. `profile_proxy`'s nothing-registered
    refusal is kept, and never weakened into `()`. That is the case the file
    was written for (R1Q3 (i)).
  - A host registration made before anything is built replaces the default.
    After a parser or server was built from the default, a host registration
    meets today's `AlreadyRegistered` refusal (R1Q3 (ii)), which T016 leaves
    in place.
  - `tests/test_profile_registration.py` asserts the bare-process refusal, the
    replacement before a build, and the refusal after one.
  - The one-line entry-point calls in `serve.py` and `cli.py` rebase onto Lane
    A.
  - **Realizes**: 3.2.
  - **Falsifier**: F3.1 with line 2 as amended (T007 batch A); `tests/test_profile_registration.py`.
  - **Ruled**: R1Q3 (a), with (i) and (ii); R1Q22 (a).
  - **Ruling needed**: RN-1 asks Brett to align requirement 3's fourth
    scenario with (ii). It holds phase 1's CLOSE (T049), not T016's landing,
    because the after-build refusal is existing behaviour. If Brett rules
    RN-1 (b), T016 is amended before T049, so that a registration after a
    build also replaces the default.
  - **After**: T015, T012 (Lane A's last `serve.py` edit).
- [ ] T017 [US4] [oxF] **3.3, read-only.** At every openxFactory arc
  landing, confirm that the carve manifest's `deleted_at_carve` row for
  `scripts/ideation_dashboard/profile_openxfactory.py` is byte-identical. F11.1's
  content check already refuses any row change, so the interim F11.1 runs are
  the evidence: T018, T065 and T098. The first is phase 1's, after T047.
  Phases 2 and 3 repeat the check through T065 and T098, after their own
  consumer pins, and T097 ticks 3.3 on all three.
  - **Realizes**: 3.3.
  - **Falsifier**: F11.1 (interim: T018, T065, T098).
  - **After**: T047, which is phase 1's openxFactory landing.

### Lane C: the home-corpus seam

- [ ] T020 [P] [US1] [oDc] **`corpus_adapter.register_home(factory)` and
  `corpus_adapter.home()`.**
  - `factory` has `home_corpus`'s shape: `adapter, ref = factory(root)`.
  - With nothing registered, `home()` raises `CorpusRefused` of the NEW kind
    `ADAPTER_NOT_REGISTERED` (added to `REFUSAL_KINDS`, `:135`). Its `subject`
    is `opendox.corpus_adapter` and its `detail` names `register_home(...)`.
  - **Realizes**: 4.1 (the seam), 4.2.
  - **Falsifier**: F4.1's first block (nothing registered: exactly one outcome);
    `tests/test_authoring_seam.py::test_required_header_fields_come_from_the_registered_adapter`.
  - **After**: T006. It never needed an answer.
- [ ] T021 [US1] [oDc] **`authoring.py:318`** resolves the home corpus through
  `corpus_adapter.home()`.
  - **Realizes**: 4.1, 4.3 (1 of 8).
  - **Falsifier**: F4.1's first block.
  - **Ruled**: R1Q22 (a).
  - **After**: T020.
- [ ] T022 [US1] [oDc] **4.1a: openDox's own default adapter.** Where no host
  called `register_home`, the entry points register a `home_corpus`-shaped
  factory over `LocalGitCorpus`. Like the default profile, it is an
  entry-point registration (R1Q3 (a)). It starts at `LocalGitCorpus()`'s
  defaults (`required_fields=()`), and phase 2's T054 sets the neutral fields
  that R1Q13 decides. A bare process still refuses.
  - **Realizes**: 4.1a.
  - **Falsifier**: `tests/test_authoring_seam.py::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has`.
  - **Ruled**: R1Q3 (a), R1Q22 (a).
  - **After**: T020, T021, T016.

### Lane D: the other openxFactory reaches (`workbench.py`, `serve_wire.py`, `doxbench_packet.py`)

- [ ] T025 [US1] [oDc] **`workbench.py:746`** (`session_documents`), in
  phase 1 (R1Q9 (a)). It resolves through the registered adapter's
  `list_documents`: openDox's `LocalGitCorpus` standalone, and openxFactory's
  adapter when hosted. With nothing registered it refuses, as 4.2 does. The
  hosted membership rule (the governed roots plus a `Status:` header) is
  proved unchanged by T046.
  - **Realizes**: 4.3 (1 of 8).
  - **Falsifier**: F4.1's scan; a session-notebook membership test.
  - **Ruled**: R1Q9 (a), R1Q22 (a).
  - **After**: T020, T026 (both edit `workbench.py`).
- [ ] T026 [US1] [oDc] **`workbench.py:1407-1409`** (`run_scoped_doc_health`).
  Route it through a declared health-check seam that, with nothing registered,
  returns `status = not-available`, naming the seam and its remedy (the
  registration call), which is 4.2's discipline. It stays that way until Group
  6 (release 2) registers openDox's own check.
  - **Realizes**: 4.3 (3 of 8).
  - **Falsifier**: F4.1's scan; a seam test.
  - **Ruled**: R1Q22 (a).
  - **After**: T006.
- [ ] T027 [P] [US1] [oDc] **`serve_wire.py:1369` and `doxbench_packet.py:177`.**
  - The doxBench schema validators and the status-exemption rail become seams.
    Each fails closed, naming itself, when nothing is registered.
  - openxFactory registers its own (T046).
  - The standalone defaults are T085's (phase 3).
  - **Realizes**: 4.3 (2 of 8).
  - **Falsifier**: F4.1's scan; seam tests.
  - **Ruled**: R1Q22 (a).
  - The phase-1 seam fails closed exactly as 4.2 does. The standalone defaults
    are T085's, which the open questions on the doxBench defaults decide.
  - **After**: T006.

### Lane E: the instrument and the README

- [ ] T030 [P] [US1] [oDc] **2.4: the import-every-module test.**
  `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`
  walks the package with `pkgutil`. It fails naming the first module that needs
  a sibling, and it first asserts the siblings are absent.
  - **Realizes**: 2.4; 9.2a (the instrument; T036 makes a required check run
    it).
  - **Falsifier**: F2.1's last line.
  - **After**: T006.
  - **Lands with**: T011, in T011's PR, because it fails until 2.1 lands.
- [ ] T031 [US1] [oDc] **2.6: `README.md:39-42`.** State the live cause
  (`ideation_dashboard`, not the openDox → openXdox inversion). Once the
  narrowing ends, rewrite the paragraph.
  - **Realizes**: 2.6.
  - **Falsifier**: review.
  - **After**: T035.
  - **Lands with**: T036, in T036's PR.

### Join: the sweep, the suite, the console script

- [ ] T032 [US1] [oDc] **2.3: the sweep.** Grep `src/` for `ideation_dashboard`,
  `corpus_adapter_openxfactory`, `doc_health` and `openxdox` in import
  position. Record, for each hit, whether it is closed or deferred, with its
  reason, in the PR body. The expected state is: no import-time reach, and 19
  deferred reaches, all into `openxdox`.
  - **Realizes**: 2.3.
  - **Falsifier**: F4.1's scan, which lists only `openxdox` targets.
  - **After**: T011, T012, T016, T021, T022, T025–T027 (every lane joins
    here).
- [ ] T034 [US1] [oDc] **Repair the nine files that go red once 2.1 lands**
  (research R3; 86 failures and errors). Update the Node harnesses to the
  views; replace carve-residue paths and module literals; re-derive
  `test_consumer_reach.py`'s `STILL_REACHING`; re-pin `test_boundary.py`'s
  census.
  - `test_provider_boundary.py` is repaired for 16.6's three reasons (*"the file
    is repaired in phase 1"*).
  - `test_outline_model.py`'s `doc_health` case is either rewritten against
    openDox's own contract, or becomes a NAMED openxFactory composition test
    (R1Q2 (a)). In the second case, it takes the same route as T035's
    `test_session_harness.py`. This PR removes the case and lists it, with its
    destination, in its body. A T007 batch adds its openxFactory path to
    F11.1's named set. T047's openxFactory PR lands it, and T049 checks that
    it arrived.
  - **Realizes**: 9.1 (part), 16.6 (the phase-1 repair).
  - **Falsifier**: `python -m pytest -q` over the nine files.
  - **Ruled**: R1Q2 (a); R1Q22 (a). Eight of the nine are carved
    `moved_with_declared_edit` rows (research R12). The ninth,
    `test_consumer_reach.py`, was created at the destination and has no row.
    None needs a declared-edit act.
  - **After**: T032, whose sweep fixes the import inventory that the
    re-derived censuses must match.
- [ ] T035 [US1] [oDc] **Empty the root `conftest.py`'s `collect_ignore`**
  (seven modules; research R4).
  - The six that import `openxdox` each leave `collect_ignore` in one of two
    ways:
    - rewritten in place as a neutral openDox test that imports no sibling;
    - or removed from openDox-code in this PR, and re-landed by T042 in
      openXdox-code's `tests/integration/`. A module whose imports reach
      `doc_health` cannot run there in release 1, because F9.2 runs every file
      in `tests/integration/`. It goes into T041's declared exclusion, with its
      reason, instead (R1Q6 (d)).
  - `test_session_harness.py` runs a script only openxFactory has. It is
    either rewritten, or removed here and moved to openxFactory as a NAMED
    composition test (R1Q2 (a)). In the second case, a T007 batch adds its
    path to F11.1's named set first, and it lands in T047's openxFactory PR.
  - This PR's body lists each removed module with its destination:
    openXdox-code's `tests/integration/` (T042), openXdox-code's declared
    exclusion (T041), or openxFactory (T047). Each destination task lands
    exactly its part of that list, and T049 checks that every listed module
    arrived where the list sends it, so none is dropped from both suites
    (requirement 9, second scenario).
  - **Realizes**: 9.1 (part), 9.3 (part).
  - **Falsifier**: F9.1 (openDox-code).
  - **Ruled**: R1Q2 (a), R1Q6 (d), R1Q22 (a). All seven are carved rows.
  - **After**: T034.
- [ ] T036 [US1] [oDc] **The required check runs the whole suite.**
  - Remove `validate.yml`'s three `--noconftest` steps and their file lists.
    Also remove the 15 comment lines that name the flag, because F9.1's
    `grep -c` counts comments.
  - Set `testpaths = ["tests", "tests_runtime"]`, and give the required
    `validate` job the PostgreSQL service and the `.[runtime,test]` install
    that the `runtime` job has today (R1Q8 (a)). The separate `runtime` job may
    then be folded in.
  - F9.1 is unchanged, and it installs `.[test]` alone. So the `test` extra
    gains the `runtime` extra's packages. Without them,
    `tests_runtime/conftest.py` fails every runtime case under `CI` and skips
    it elsewhere, and a skipped case does not make a whole suite. Keeping
    `test` lean would instead need F9.1's install line changed, which R1Q8 (a)
    left alone, so that route goes to Brett.
  - F9.1's runs (here, and in T049) export the database's DSN the way the job
    does, and quote the variables they set.
  - T095's clean-machine harness is not a test module, so it stays out of this
    job: it runs in its own job, with no database service.
  - Re-pin the floors to the measured whole-suite counts.
  - T031 lands in the same PR.
  - **Realizes**: 2.5, 9.1, 9.2a (a required check now runs T030).
  - **Falsifier**: F9.1 (openDox-code), both of its assertions.
  - **Ruled**: R1Q8 (a).
  - **After**: T035, T038 (both edit `pyproject.toml`, and T038's
    `[project.scripts]` lands first).
- [ ] T037 [US1] [oDc] **9.4, openDox's half.** Restore the margin over the
  floors. The two skips that mirror openXdox's gap assert for real.
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple in `validate.yml`.
  - **After**: T036.
- [ ] T038 [US1] [oDc] **10.1: `[project.scripts] opendox = "opendox.cli:main"`**,
  with Q-R4's runtime verbs wired through the default profile's
  `SUBCOMMAND_EXTENSIONS` (`RuntimeSubcommand`, R1Q5 (a)).
  - `opendox runtime …` works standalone, and `opendox-runtime` stays as an
    alias.
  - A host that registers its own profile keeps its 31-entry `--help` tree, so
    neither golden is regenerated.
  - The same landing corrects two comments in `src/opendox/runtime/cli.py`.
    The `:17-19` claim, that a line added to `cli.py` needs a declared edit
    first, is retired by R1Q22 (a). The `:39-42` record of Q-R4 now says
    where the verbs were wired.
  - **Realizes**: 10.1.
  - **Falsifier**: `opendox --help` exits 0 (F10.1's first assertion, which is
    phase 1's proof); `opendox runtime --help` exits 0.
  - **Ruled**: R1Q4 (a), R1Q5 (a), R1Q22 (a).
  - **After**: T016, T022 (`cli.py`'s single-writer order).

### The openDox root pin (9.5, steps 1–2)

- [ ] T039 [US4] [oD] **Phase 1's openDox root pin** (T090 steps 1–2). ONE
  commit in opensoft/openDox moves the `code` gitlink, `contracts/code-pin.yaml`
  and every workflow `@<sha>` to the openDox-code commit carrying phase 1.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T022, T032, T037, T038 (every phase-1 openDox-code landing).

### openXdox-code: green alone, less the declared `doc_health` exclusion

- [ ] T040 [US1] [oXc] **Move the pin; clear the residue.**
  - Move `pyproject.toml`'s `opendox @` to the phase-1 openDox-code commit
    (plan.md § Pins, step 3). The ratchet is unchanged, since phase 1 closes no
    openXdox reach.
  - Give `test_create_project.py`, `test_edit_project.py` and
    `test_register_edit_lane.py` a helper of their own, in place of the
    openxFactory-only `test_gate_routes` module (research R10).
  - Declare `rfc3339-validator` in the `test` extra.
  - Add `tests/fixtures/base-repo` (research R11). These are added files, and
    no protected suite is edited.
  - **Realizes**: 9.2 (part), 9.5 (step 3).
  - **Falsifier**: collection no longer fails on `test_gate_routes`.
  - **After**: T039.
- [ ] T041 [US1] [oXc] **The declared `doc_health` exclusion (R1Q6 (d)).**
  Requirement 9's first scenario applies.
  - A committed exclusion file lists each test file that cannot run without
    openxFactory's `doc_health`, with its reason and the total count. T041
    names the file, and T007 batch B records that name in F9.1. The reason is
    `doc_health` reachability, pending the direction arc (T008).
  - The root `conftest.py` derives its `collect_ignore` from that file, so
    `validate.yml` names no file list and no `--noconftest`.
  - The required check PRINTS the exclusion as an open extraction, with its
    count and its reason, on every run.
  - A test asserts that each listed file fails, without `doc_health`, for
    exactly that reason. The list therefore cannot hide any other failure,
    and a file that stops needing `doc_health` leaves the list.
  - **Realizes**: 9.2 (part).
  - **Falsifier**: F9.1 (openXdox-code) as amended by T007 batch B.
  - **Ruled**: R1Q6 (d).
  - **After**: T040.
- [ ] T042 [US1] [oXc] **9.3: `tests/integration/`.**
  - Add the 31-entry assembled `--help` tree:
    `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`.
  - Add those of T035's relocated modules that run without `doc_health`,
    exactly as T035's PR body lists them. The others are in T041's declared
    exclusion (R1Q6 (d)).
  - Each test names the pin it composes at.
  - The tree stays at 31 entries because a host that registers its own
    profile does not get the default's runtime verbs (R1Q5 (a)).
  - **Realizes**: 9.3.
  - **Falsifier**: F9.2.
  - **Ruled**: R1Q5 (a), R1Q6 (d).
  - **After**: T040, T041 (whose exclusion decides which relocated modules
    belong here).
- [ ] T043 [US1] [oXc] **9.2: the required check runs the whole suite, less
  the declared exclusion.** Remove the file list and all 8 `--noconftest`
  lines. Re-pin `MIN_SELECTED`/`MIN_PASSED` (now 564/558) and
  `EXPECT_SKIPPED` to the triple measured over the whole suite less T041's
  exclusion.
  - `test_branch_session.py` fails on `doc_health` (research R11), so in
    release 1 it sits in the exclusion. Its stale `getsource` assertion is
    respelled when it becomes runnable.
  - Any respelling edit that release 1 makes to a protected suite is entered
    in R1Q7 (a)'s reviewed allow-list (T007 batch C).
  - `tests/test_snapshot.py` needs no `doc_health`, so this check runs it, and
    as one of 5.4a's protected suites it cannot be edited to pass. At
    `626f2c8d` three of its cases failed on the validator lookup and the
    schema path (research R11). C3's PR 2 (openXdox-code#28, landed as
    `e28930bf`) moved that lookup into the product's own tree, and T005
    records whether the three now pass. If any stays red, T005's re-plan,
    before T006, moves T061 into phase 1, between T040 and T043 (see T061).
    T061 is blocked by R1Q14, so T043 then waits for that answer.
  - **Realizes**: 9.2.
  - **Falsifier**: F9.1 (openXdox-code), as amended by T007 batch B.
  - **Ruled**: R1Q6 (d), R1Q7 (a).
  - **After**: T041, T042, and C3's openXdox-code PR 2 (openXdox-code#28,
    landed as `e28930bf`).
- [ ] T044 [US1] [oXc] **9.4, openXdox's half.** Restore the margin over the
  floors T043 re-pinned. Each of the six skips defers *"`doc_health`
  reachability"*. Each one either asserts for real, or its file joins T041's
  declared exclusion with that reason (R1Q6 (d)). No skip is left carrying the
  gap. A file that joins the exclusion here lowers the collected counts, so
  T044 first re-pins T043's floors over the new whole suite less the
  exclusion, and then restores the margin.
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple.
  - **Ruled**: R1Q6 (d).
  - **After**: T043.

### openxFactory: the host keeps working (US4)

- [ ] T045 [US4] [oxF] **The lanes column, through the handler-contribution
  facet (R1Q1 (a)).** `scripts/profile_openxfactory.py` declares `LaneRoutes`,
  with tests under `tests/domain_profile/`.
  - `tests/ideation-dashboard/test_extension_point_parity.py`'s MRO assertion
    (`:404-425`) is updated. It is the first NAMED composition test that R1Q2
    (a) admits to 11.1's surfaces, and T007 batch A widens F11.1 to name it.
  - `tests/ideation-dashboard/test_serve_column_split.py`'s
    `test_every_moved_handler_still_resolves_on_the_request_handler` resolves
    six `LaneRoutes` methods on `DashboardHandler` (`:97-110`, `:189-195`).
    Once T011 lands they no longer resolve there, so the test is updated to
    resolve them where the facet binds them. It is the second NAMED
    composition test, and T007 batch A names it too.
  - Any other openxFactory test that pins openDox internals and fails at
    T047's pin joins F11.1's named set through a T007 batch before T047 lands
    (R1Q2 (a)). T047's whole `pytest-suite` run at the new pin finds them.
  - This lands in T047's PR.
  - **Realizes**: 2.2 (openxFactory half), 11.1 (surface).
  - **Falsifier**: openxFactory's `pytest-suite`; the five lane routes are
    served.
  - **Ruled**: R1Q1 (a), R1Q2 (a).
  - **After**: T011.
  - **Lands with**: T047, in T047's PR.
- [ ] T046 [US4] [oxF] **The other host wiring.** The host registers
  `corpus_adapter_openxfactory.home_corpus` via `register_home` (4.1), and
  registers its `doc_health`, session-notebook, doxBench-validator and
  status-exemption implementations with T025–T027's seams.
  - Its session-notebook membership rule (the governed roots plus a `Status:`
    header) stays exactly as today (R1Q9 (a)).
  - Its own start, in `scripts/opendox_host.py`, asserts that its profile is
    the registered one (R1Q4 (a)).
  - Tests go under `tests/domain_profile/`. This lands in T047's PR.
  - **Realizes**: 4.1 (host half), 4.3 (host half).
  - **Falsifier**: `pytest-suite`; the hosted session notebook is unchanged.
  - **Ruled**: R1Q2 (a), R1Q4 (a), R1Q9 (a).
  - **After**: T020–T022 and T025–T027.
  - **Lands with**: T047, in T047's PR.
- [ ] T047 [US4] [oX] [oxF] **Phase 1's consumer pins and host wiring** (T090
  steps 5–6). The openXdox root moves to T044's commit and to T039's root
  commit. openxFactory then moves both pin pairs in ONE PR, which also carries
  T045 and T046. It also carries, as named composition tests,
  `test_session_harness.py` if T035 moved it here and `test_outline_model.py`'s
  `doc_health` case if T034 did. C3's openXdox pin bump landed as #1157 →
  `1edbb3dd`, so T047 starts from that pin.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openXdox root; `verify-opendox-pin.py` and
    `verify-openxdox-pin.py`; `pytest-suite`.
  - **After**: T039, T044, T007 (batch A).
  - **Lands with**: T045, T046.
- [ ] T018 [US4] [oxF] **Phase 1's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T047's landing. Record the output in
  `evidence/f11.1-phase1.txt`, with no trailer.
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T047.
- [ ] T048 **The F4 re-measure (holder).** After phase 1 lands, re-measure
  openxFactory's direct `opendox` imports and bring Brett the direct-arrow
  question (F4, outside both releases; `5799494355`).
  - **After**: T049.
- [ ] T049 **Phase 1 checkpoint.** Run and quote:
  - F2.1, and F3.1 with line 2 as amended (T007 batch A);
  - F9.1 in each leg (openXdox-code's as amended by batch B, openDox-code's
    with the database DSN exported), and F9.2;
  - `opendox --help`;
  - F4.1's scan, which must list only `openxdox` targets;
  - every module or case T034 or T035 removed, found where its PR's list
    sends it: openXdox-code's `tests/integration/` or its declared exclusion,
    or openxFactory, with its path in F11.1's named set;
  - T018's interim F11.1 output.

  Tick nothing; T097 ticks.
  - **Ruling needed**: RN-1. Requirement 3 is not reported as realized until
    RN-1 is ruled and T016 matches the ruling.
  - **After**: T047, T017, T018, T007 (batches A and B), and RN-1 ruled.

---

## Phase 2: useful alone (US2 and US4)

**PROVISIONAL.** This phase is an outline and authorizes no implementation.
T009 re-plans and re-analyzes it once its answers are in: R1Q10–R1Q14 and
R1Q23. Every phase-2 task comes after T009.

**Goal**: with no consumer installed, openDox generates its own neutral
snapshot from a plain repository, serves it standalone, and validates it
against schemas that are on disk. The governed projection is unchanged.

**Independent test**: T063.

- [ ] T050 [P] [US2] [oDc] **5.0: `tests/fixtures/plain-documents`.**
  - A handful of `.md` documents, spread across the six stations as R1Q13
    decides, with at least one group so that AT-R1 can open the chat pane.
  - It carries none of the declared vocabulary: the eight `Status:` words and
    the change/spec/delta nouns.
  - A test keeps the fixture free of those words.
  - **Realizes**: 5.0.
  - **Falsifier**: the vocabulary test; used by F5.3, F7.2, F10.1 and F13.1.
  - **Blocked by**: R1Q11, R1Q13.
  - **After**: T049, T009.
- [ ] T051 [US2] [oDc] **7.0: `tests/fixtures/malformed`.** Exactly one
  rule violation of the snapshot contract R1Q12 selects, and an
  `EXPECTED_RULE` file holding that rule's identifier.
  - **Realizes**: 7.0.
  - **Falsifier**: used by F7.2.
  - **Blocked by**: R1Q12.
  - **After**: T050.
- [ ] T052 [P] [US2] [oDc] **5.4: declare the generator seam.** Declare the
  operation handed over, the registration point beside
  `domain_profile.register()`, and the conformance a contributed generator
  must meet. The conformance clause cites R1Q11's contract. `CorpusAdapter`
  stays closed at six members.
  - **Realizes**: 5.4.
  - **Falsifier**: seam tests; F5.2 through T059.
  - **Blocked by**: R1Q11 (the conformance clause only).
  - **After**: T049, T009.
- [ ] T053 [P] [US2] [oDs] [oD] **The neutral snapshot contract. CONDITIONAL:
  only on R1Q11 (a) or R1Q12 (b).** The schema lands in openDox-spec, then the
  openDox root's spec pin moves, then the bundle is cut if Brett's answer
  requires it (a `dox-v1.x` minor under the root's four-value rule).
  - openDox-spec then becomes a sixth repository of the arc. Its landings
    carry the `Arc:` and `Lane:` trailers and land by squash or merge, like
    every realization landing (T091). It allows all three methods and
    requires only `validate`. T003 records its ARC_BASE.
  - Under R1Q12 (b) the schemas are RE-HOMED, so openXdox-spec `[oXs]` changes
    as well. It retires its own `ideation-dashboard-snapshot` and `-index` in
    favour of openDox-spec's, the openXdox root's spec pin moves, and
    openXdox-spec joins the arc as a seventh repository. Its landings carry
    the trailers too (T091), and T003 records its base. T009 plans that slice
    once the answer is known.
  - **Realizes**: 5.1 and 7.1 (their contract).
  - **Falsifier**: the root's `make validate`.
  - **Blocked by**: R1Q11, R1Q12.
  - **After**: T049, T009.
- [ ] T054 [US2] [oDc] **5.1–5.3: openDox's small neutral projection** over
  `CorpusAdapter`. It is bound to `LocalGitCorpus` (5.2) and renders the six
  words only (5.3), with `display_profile.py` unchanged unless R1Q11 amends
  that. It is new code, not a copy of openXdox's.
  - **Realizes**: 5.1, 5.2, 5.3.
  - **Falsifier**: F5.3.
  - **Blocked by**: R1Q11, R1Q13.
  - **After**: T050, T052 (and T053, if chosen).
- [ ] T055 [US2] [oDc] **Serve and generate standalone; route 4.3's
  generator-facing reaches.**
  - Give the snapshot source and registry, the corpus-root predicate, and the
    writer and validator lookup seams with openDox defaults (R1Q10 (a)). Their
    uses are `serve.py:1647`, `:629`, `:1687` and `:1993`, `cli.py:610` and
    `branch_session.py:1568`, `:2105`, `:2151`, `:2228` and `:3573`.
  - Retire the `consumer_reach` names `snapshot_registry` (22 uses),
    `snapshot` (6), `generate_snapshot` (2), `is_rfc3339_datetime` (1),
    `corpus_root_refusal` (1), `scanned_roots` (1) and `find_validator` (1),
    plus the core `/snapshot.json` arm's `LateProjectionRoutes` forwarding.
  - **Realizes**: 5.5, 4.3 (part).
  - **Falsifier**: F4.1's scan, down by these reaches.
  - **Blocked by**: R1Q10.
  - **Ruled**: R1Q22 (a).
  - **After**: T054, T022 and T038 (`serve.py`'s and `cli.py`'s single-writer
    order).
- [ ] T056 [US2] [oDc] **The standalone generate path, end to end.**
  `python -m opendox.cli generate` and `generate-and-open --no-open` run on
  the fixture with neither sibling importable, and the server STARTS (the limit
  measured in research R7 is lifted).
  - **Realizes**: 5.1 (part).
  - **Falsifier**: F5.3; F10.1's generate half, without the console script.
  - **After**: T055.
- [ ] T057 [P] [US2] [oDc] **7.1, 7.1a, 7.1b, 7.2: the validator's input set.**
  - Narrow it to openDox's own kinds.
  - Ship them as package data, digest-checked against the spec-leg commit the
    root pins (R1Q12).
  - Record why the old script cannot be reused (7.1a).
  - A test asserts that `gate-intent` and `ideation-possibles-register` are
    NOT in the set (7.1b).
  - The validator is new surface at the code leg (7.2).
  - **Realizes**: 7.1, 7.1a, 7.1b, 7.2.
  - **Falsifier**: F7.2's schema half.
  - **Blocked by**: R1Q12.
  - **Ruled**: R1Q22 (a).
  - **After**: T049, T009.
- [ ] T058 [US2] [oDc] **The post-render validator in the generate verbs.**
  `--strict` makes a validator that cannot run fatal, and `--no-validate`
  skips validation.
  - **Realizes**: 7.2 (part).
  - **Falsifier**: F7.2. The good fixture exits 0; the malformed one exits
    non-zero, naming `EXPECTED_RULE`, with no `No such file or directory`.
  - **Blocked by**: R1Q11, R1Q12.
  - **After**: T051, T056, T057.
- [ ] T059 [US4] [oXc] **5.4a: openXdox contributes its governed generator,
  registry and source through the seams.**
  - It keeps `generator.py`, `snapshot.py`, `snapshot_registry.py`,
    `completeness.py` and `corpus_root.py`.
  - The ratchet is lowered for T055's closed reaches, in the landing that moves
    the pin.
  - **Realizes**: 5.4a, 9.5 (step 3, part).
  - **Falsifier**: F5.2, with the six generator suites passing and unedited by
    any arc landing except edits in R1Q7 (a)'s allow-list (T007 batch C).
  - **Blocked by**: R1Q23. Four of the six suites fail on `doc_health`
    (research R11), and the ruled exclusion leaves that reach in place.
  - **Ruled**: R1Q6 (d), R1Q7 (a).
  - **After**: T052, T055, T062, T007 (batch C), T040 (the ratchet's
    single-writer order).
- [ ] T060 [US4] [oXc] **5.3a: re-run F5.1 against the realized openDox.** The
  facet landed before the arc (#26 and #27), so no code change is expected.
  - **Realizes**: 5.3a, F5.1.
  - **Falsifier**: F5.1.
  - **After**: T054.
- [ ] T061 [US4] [oXc] **7.3: the consumer's validator lookup through the
  installed distribution**, with no parent walk. C3's
  `test_a_start_outside_the_product_is_refused_not_walked` is revised in the
  same landing (R1Q14 (a)).
  - 7.3's falsifier names
    `tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own`,
    which does not exist yet. T061 adds it to one of 5.4a's protected suites,
    and F5.2 refuses that edit, because R1Q7 (a)'s allow-list admits only
    respellings. So R1Q14's answer must also say how F5.2 admits it.
  - **The phase-1 contingency.** If T005 finds `tests/test_snapshot.py` still
    red after C3's PR 2 (T043), T005's re-plan, before T006, moves this task
    into phase 1. It then comes after T040 and before T043, and its
    `After: T049, T009` is dropped, so phase 1's checkpoint never waits on a
    phase-2 task. It needs R1Q14 answered first.
  - **Realizes**: 7.3.
  - **Falsifier**: F7.1, including its two named tests.
  - **Blocked by**: R1Q14.
  - **Ruled**: R1Q22 (a).
  - **After**: T049, T009, and C3's openXdox-code PR 2 (openXdox-code#28,
    landed as `e28930bf`).
- [ ] T062 [US4] [oD] **Phase 2's openDox root pin** (T090 steps 1–2).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T054–T058 (every phase-2 openDox-code landing), T039 (the root
    pin's single-writer order).
- [ ] T064 [US4] [oX] [oxF] **Phase 2's consumer pins** (T090 steps 5–6). Host
  wiring is needed only if openxFactory's composite has to register a generator
  contribution. It composes openXdox's profile, so none is expected; confirm
  that by `pytest-suite`.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: as T047's.
  - **After**: T059, T060, T061, T062, T047 (the pin pairs' single-writer
    order).
- [ ] T065 [US4] [oxF] **Phase 2's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T064's landing. Record the output in
  `evidence/f11.1-phase2.txt`, with no trailer.
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T064.
- [ ] T063 **Phase 2 checkpoint.** Run and quote F5.1, F5.2 (as amended by
  T007 batch C, and as R1Q23 decides), F5.3, F7.1 and F7.2, then a standalone
  `generate-and-open` serving the fixture, then T065's interim F11.1 output.
  - **Blocked by**: R1Q23 (F5.2's four `doc_health` suites).
  - **After**: T064, T065, T007 (batch C).

---

## Phase 3: it installs (US3 and US4)

**PROVISIONAL.** This phase is an outline and authorizes no implementation.
T069 re-plans and re-analyzes it once its answers are in: R1Q10, R1Q12 and
R1Q15–R1Q19. Every phase-3 task comes after T069.

**Goal**: one documented command installs and starts the whole product, with
its bundled datastore, the local mode, the served bundle, and chat with a clear
no-model state. `consumer_reach.py` is gone.

**Independent test**: T089, then T095 and T096.

- [ ] T069 **Phase 3's round.** T009's steps for phase 3: encode the answers,
  hand amendments to a T007 batch, bring any requirement or scenario text back
  as RULING NEEDED, re-plan phase 3 and lift its PROVISIONAL marker, and run
  `/speckit-analyze` with T006's feature context, finding nothing CRITICAL. No
  task of phase 3 starts before it is done.
  - **Blocked by**: R1Q10, R1Q12, R1Q15, R1Q16, R1Q17, R1Q18, R1Q19.
  - **After**: T009.

### Group 13: the install's shape (`runtime/`)

- [ ] T071 [US3] [oDc] **13.2 and 13.3.** `load_settings` refuses a
  non-PostgreSQL DSN, naming the one dialect kept. It refuses the same
  credential in both settings, naming `OPENDOX_MIGRATION_DATABASE_URL`. The
  migration DSN stops being optional.
  - **Realizes**: 13.2, 13.3.
  - **Falsifier**: F13.1's `load_settings` block.
  - **After**: T063, T069.
- [ ] T070 [US3] [oDc] **13.4, 13.5 and 13.6: `OPENDOX_INSTALL_MODE`.**
  - `local` or `hosted`, defaulting to `hosted`, and read beside
    `OPENDOX_OIDC_ISSUER`.
  - `local` needs no broker, binds loopback only, and refuses a non-loopback
    `--host` with no opt-in.
  - `hosted`, or unset, with no issuer refuses, naming the setting.
  - Hosted mode is otherwise unchanged.
  - The documented command selects local as R1Q15 decides.
  - **Realizes**: 13.4, 13.5, 13.6.
  - **Falsifier**: F13.1's refusals.
  - **Blocked by**: R1Q15, R1Q16.
  - **After**: T071.
- [ ] T072 [US3] [oDc] **13.1: the bundled PostgreSQL server.**
  - Its data and socket directories live under `OPENDOX_STATE_DIR`, with NO TCP
    listener; both DSNs are supplied.
  - `runtime status` reports `database_bundle` (`data_dir`, `socket_dir`,
    `pid`).
  - The packaging follows R1Q16.
  - **Realizes**: 13.1.
  - **Falsifier**: F13.1's TCP-listener block, which reads the kernel's socket
    table at run time, and its `runtime status` block.
  - **Blocked by**: R1Q16.
  - **After**: T070.
- [ ] T073 [US3] [oDc] **13.4a: `/capabilities` gains an `install` block**,
  read from the serving process's own settings. `serve.py` is a single-writer
  file.
  - **Realizes**: 13.4a.
  - **Falsifier**: F13.1's `caps.json` block.
  - **Blocked by**: R1Q16.
  - **Ruled**: R1Q22 (a).
  - **After**: T072, T055 (`serve.py`'s single-writer order).
- [ ] T074 [US3] [oDc] **Run F13.1**, as amended per R1Q15 and R1Q16.
  - **Realizes**: F13.1.
  - **Falsifier**: F13.1 itself, as amended. This task is that run, quoted in
    its PR.
  - **Blocked by**: R1Q15, R1Q16.
  - **After**: T073.

### Group 10: the door

- [ ] T075 [US3] [oDc] **10.2 and 10.2a.** The entry point serves the 42-file
  bundle, reachable in a browser from an openDox-only install. `intent-feed.js`
  is not owed (10.2a is a declaration, recorded in the PR).
  - **Realizes**: 10.2, 10.2a.
  - **Falsifier**: F10.1's fetch.
  - **After**: T056, T038, T063, T069.
- [ ] T076 [US3] [oD] **10.3: the openDox root's `README.md` documents the one
  command.** No `Makefile` target is added, since it has a shape-pin row.
  - **Realizes**: 10.3.
  - **Falsifier**: review, and AT-R1 step 4 follows it literally.
  - **Blocked by**: R1Q15.
  - **After**: T074, T075, T087 (the README documents the command the root
    pins).
- [ ] T077 [US3] [oDc] **Run F10.1**, as amended per R1Q15 and R1Q16.
  - **Realizes**: F10.1.
  - **Falsifier**: F10.1 itself, as amended. This task is that run, quoted in
    its PR.
  - **Blocked by**: R1Q15, R1Q16.
  - **After**: T075, T070.

### Group 16: chat's model configuration (`doxbench_binding.py`, then `doxbench_provider.py`)

- [ ] T078 [US3] [oDc] **16.1: `openai-chat-v1`.** A second `DIALECTS` member.
  The chat-completions request (`model`, `messages`) and its answer
  (`choices[0].message.content`) are spoken by an arm in
  `doxbench_provider.py` alone. An unknown dialect is still refused.
  - **Realizes**: 16.1.
  - **Falsifier**: F16.1's dialect assertion.
  - **Ruled**: R1Q22 (a). `doxbench_binding.py` is a `moved_verbatim` row,
    and editing it needs no declared-edit act.
  - **After**: T063, T069.
- [ ] T079 [US3] [oDc] **16.2: a `model` field**, sent as the request's model
  and set by `model-binding add|edit --model`. The record grows from nine
  fields to ten, and none of them can hold a secret.
  - **Realizes**: 16.2.
  - **Falsifier**: F16.1's `BINDING_FIELDS` assertion.
  - **Ruled**: R1Q22 (a).
  - **After**: T078.
- [ ] T080 [US3] [oDc] **16.3: refuse a raw key when it is declared.**
  - Keys in the URL and in extra fields are refused, via `carries_a_credential`.
  - The no-credential declaration follows R1Q18, and the reference resolver
    follows R1Q17.
  - **Realizes**: 16.3.
  - **Falsifier**: F16.1's three refusals.
  - **Blocked by**: R1Q17, R1Q18.
  - **Ruled**: R1Q22 (a).
  - **After**: T079.
- [ ] T081 [US3] [oDc] **16.4: "no model configured" is a state.**
  - With no binding and no harness, the catalog offers no available entry.
  - The chat rail shows "no model configured" AND how to configure one, before
    any turn. Today's copy (research R15) does not name how.
  - A turn is refused `model_capability_unavailable` before any spawn or
    contact.
  - The harness route stays, for an install where it is present.
  - The SERVED catalog route answers standalone. That needs T085's
    validators, so T081 lands after T085.
  - **Realizes**: 16.4.
  - **Falsifier**: F16.1's catalog block; `tests/test_chat_model_configuration.py`.
  - **Blocked by**: R1Q10; R1Q12, for the served route (through T085).
  - **Ruled**: R1Q22 (a).
  - **After**: T063, T085.
- [ ] T082 [US3] [oDc] **16.5: every other surface works with no model.** The
  named test covers documents, generation, the views, sessions and saving.
  - **Realizes**: 16.5.
  - **Falsifier**: `tests/test_chat_model_configuration.py`.
  - **Blocked by**: R1Q10.
  - **After**: T081, T084, T085.
- [ ] T083 [US3] [oDc] **16.6, then F16.1.** `tests/test_provider_boundary.py`
  stays green as 16.1 joins the one module. Then run F16.1 whole.
  - **Realizes**: 16.6, F16.1.
  - **Falsifier**: `tests/test_provider_boundary.py` for 16.6, then F16.1 whole.
  - **After**: T080, T081, T082.

### 4.3's last reaches, and the consumer's columns

- [ ] T084 [US3] [oDc] **Route everything left, and retire `consumer_reach.py`.**
  - Route `serve_workbench.py`'s seven (`:347`, `:407`, `:408`, `:544`,
    `:1215`, `:1665`, `:2607`), `serve_project.py:246/:247`, and
    `branch_session.py:1587/:2005`.
  - Route the `gate_console` names (27 uses), `hosted_ref_refused` (2), and the
    `LateGateRoutes` and `LateProjectionRoutes` bases, through declared seams
    with openDox defaults (R1Q10 (a), still open).
  - Hand the gate and projection columns to the handler-contribution facet
    (R1Q1 (a)).
  - **Realizes**: 4.3.
  - **Falsifier**: F4.1 whole: `consumer_reach.py` is absent, and the scan
    prints `no deferred reach names the consumer or the publisher`.
  - **Blocked by**: R1Q10.
  - **Ruled**: R1Q1 (a), R1Q22 (a).
  - **After**: T055, T073 (`serve.py`'s single-writer order).
- [ ] T085 [US3] [oDc] **The standalone doxBench defaults for T027's seams.**
  openDox's own validators run over openDox-spec's `xfactory-workbench-chat-turn`
  and `xfactory-workbench-model-catalog` copies (R1Q12). There is no status
  exemption by default.
  - **Realizes**: 4.3 (part), 16.4 (part).
  - **Falsifier**: the served catalog route answers, with no available entry.
  - **Blocked by**: R1Q10, R1Q12.
  - **After**: T057, T063, T069.
- [ ] T088 [US3] [oDc] **The lens's two seed actions**, handled as R1Q19
  decides. Recommended: offered only where a binding answers them.
  - **Realizes**: none of the 69; this is the precondition for AT-R1 step 6.
  - **Falsifier**: AT-R1 step 6.
  - **Blocked by**: R1Q19.
  - **Ruled**: R1Q22 (a).
  - **After**: T063, T069.
- [ ] T087 [US4] [oD] **Phase 3's openDox root pin** (T090 steps 1–2).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T074, T077, T083, T084, T085, T088 (every phase-3 openDox-code
    landing), T062 (the root pin's single-writer order).
- [ ] T086 [US4] [oXc] **openXdox contributes its columns.** It contributes the
  gate and projection mixins, `doxbench_scope` and its gate primitives through
  the seams. `OPENDOX_BACK_IMPORTS` becomes `(0, 0)` in the SAME landing that
  moves the pin to the openDox-code commit T087 pins, which carries T084 (4.3's
  wording).
  - It contributes the columns through the handler-contribution facet (R1Q1
    (a)). A protected suite that names a moved seam is respelled only under
    R1Q7 (a)'s allow-list.
  - **Realizes**: 4.3 (consumer half), 9.2 (the ratchet), 9.5 (step 3, part).
  - **Falsifier**: `tests/test_dependency_direction.py`; F9.1 (openXdox-code,
    as amended by T007 batch B).
  - **Ruled**: R1Q1 (a), R1Q7 (a), R1Q22 (a).
  - **After**: T084, T087, T059 (the ratchet's single-writer order).
- [ ] T094 [US4] [oX] [oxF] **Phase 3's consumer pins and host wiring** (T090
  steps 5–6). openxFactory's PR carries whatever host wiring the retired
  columns need. That includes the parity test's MRO assertion and
  `test_serve_column_split.py`'s gate and projection rows, updated again once
  `consumer_reach.py` is gone. Both are named composition tests under R1Q2
  (a).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: as T047's.
  - **Ruled**: R1Q2 (a).
  - **After**: T086, T087, T064 (the pin pairs' single-writer order).
- [ ] T098 [US4] [oxF] **Phase 3's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T094's landing. Record the output in
  `evidence/f11.1-phase3.txt`, with no trailer.
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T094.
- [ ] T089 **Phase 3 checkpoint.** Run and quote F4.1, F10.1, F13.1 and F16.1,
  then T098's interim F11.1 output.
  - **After**: T094, T098, T076 (so every phase-3 task is done).

---

## Every phase

- [ ] T090 [US4] [oD] [oXc] [oX] [oxF] **The pin procedure (9.5)**, run once
  per phase: T039 then T047 (phase 1), T062 then T064 (phase 2), T087 then T094
  (phase 3). The openDox-root step always precedes the consumer's. The order
  is:
  1. openDox-code lands.
  2. The openDox root moves its gitlink, `contracts/code-pin.yaml` and every
     workflow `@<sha>` in ONE commit (`make pins`).
  3. openXdox-code's `pyproject.toml` pin moves to the SAME openDox-code
     commit, and the ratchet is lowered.
  4. openXdox-code lands.
  5. The openXdox root moves its `code` gitlink and `code-pin.yaml`, and moves
     `contracts/opendox-pin.yaml` to step 2's root commit.
  6. openxFactory moves both pin pairs, one commit each, in ONE PR together
     with that phase's host wiring.

  Follow C4's runbook, `docs/openxdox-pin-resync-runbook.md` (landed as
  #1154). Every one of these is an ancestor move, cutting no bundle unless
  T053 applies.
  - **Realizes**: 9.5, which is ticked at ARC close.
  - **Falsifier**: `make pins` in the openDox root (step 2) and in the openXdox
    root (step 5), and openxFactory's `scripts/verify-opendox-pin.py` and
    `scripts/verify-openxdox-pin.py` (step 6).
- [ ] T091 [oDc] [oXc] [oD] [oX] [oxF] **The trailer (11.0).** Every
  realization commit and every landing carries `Arc:
  neutral-product-standalone-operability` as well as `Lane: openxfactory-4`.
  That holds in every repository the arc touches: the five, openDox-spec
  when T053 applies, and openXdox-spec too under R1Q12 (b). 11.0's own words
  are *"in EVERY repository it touches"*. A merge landing writes the trailer
  into the merge message. Land by squash or merge, never rebase. Bookkeeping
  carries NO trailer: this feature's files, #1144's ticks, evidence notes and
  amendments (T007), and interim guard output (R1Q20 (a)).
  - **Realizes**: 11.0, which is ticked at ARC close.
  - **Falsifier**: each PR's review, as for the `Lane:` line (11.0). F11.1
    finds the arc's landings by the trailer, and the falsifiers of 5.4a and
    12.5 assert that the set is non-empty in openXdox-code.
  - **Ruled**: R1Q20 (a).
- [ ] T092 [oxF] **11.1's notes.** One `edits[].note` per closed reach, added
  where an existing `edits[]` entry has none, or extended, and never rewritten.
  The note is the only field that changes: with every `edits[].note` removed,
  the manifest is unchanged, so no row, other field or digest moves. The
  manifest records the carve as it arrived, so an arc edit to a carved file
  needs nothing more (R1Q22 (a)). Each phase's notes ride in that phase's
  openxFactory PR (T047, T064, T094), for the reaches the phase closed.
  - **Realizes**: 11.1, which is ticked at ARC close.
  - **Falsifier**: F11.1's manifest check. With every `edits[].note` removed,
    the two documents must be equal, and a note that already existed may only
    be extended. Each interim run (T018, T065, T098) applies it.
  - **Ruled**: R1Q22 (a).
- [ ] T093 [oxF] **The interim F11.1 procedure, and F11.1 at the arc's
  close.** Run F11.1 with `PACKET_MERGE=94b6f7f1` and `ARC_TIP` set to the last
  arc landing measured. Use the guard as widened by T007 batch A (R1Q2 (a)'s
  named composition tests). Record the output in this feature's `evidence/`,
  with no trailer. It runs once per phase, as T018 (phase 1), T065 (phase 2)
  and T098 (phase 3), each with its own `After:` line. It runs once more at the
  arc's close, after release 2, where the box is ticked.
  - **Realizes**: F11.1, which is ticked at ARC close.
  - **Falsifier**: F11.1 itself, which must print `requirement 1 holds`.
  - **Ruled**: R1Q2 (a), R1Q20 (a).

---

## Acceptance: AT-R1

- [ ] T095 [US3] [oDc] **AT-R1, the HTTP half, in CI.** An acceptance harness,
  `acceptance/at_r1_http.py`, run by its own `acceptance` job in openDox-code's
  `validate.yml`.
  - That job has NO database service, because the harness asserts a clean
    machine. The `validate` job's PostgreSQL service (T036) would break that
    precondition.
  - The harness is not a pytest module, and it sits outside `tests/` and
    `tests_runtime/`. Like the browser half (T096), it installs the product and
    drives it from outside. So the harness changes neither `testpaths`, which
    T036 sets in phase 1, nor F9.1, and FR-006's "no exclusion" for
    openDox-code still holds.
  - Making `acceptance` a required check is a ruleset change for the
    repository's owner.

  It does the following:
  - installs openDox alone, as R1Q16 decides, into a fresh venv;
  - ASSERTS that the four siblings, `omp`, an identity broker, a database and
    a binding are all absent, in a fresh `OPENDOX_STATE_DIR`;
  - copies both plain repositories into fresh `git init`s (spec.md AT-R1
    step 3), and gives each a git identity (`git config user.name` and
    `user.email`), which the served actor is read from;
  - runs the documented command (R1Q15) on loopback;
  - fetches `/` (it must be HTML), `/snapshot.json` (non-empty, neutral per
    F5.3) and `/capabilities` (`install.mode == local`);
  - fetches the model-catalog route, presenting `/capabilities`'
    `console_token` in `X-XF-Console-Token`, and it must answer with no
    available entry;
  - fetches every route the wheel, the lens and the chat rail request on load,
    none of which may answer 5xx.
  - **Realizes**: FR-011 (HTTP half).
  - **Falsifier**: the harness itself, which exits non-zero on the first failed
    assertion.
  - **Blocked by**: R1Q10, R1Q12 (the catalog's validators, T085), R1Q15,
    R1Q16.
  - **After**: T089, T076 (the root README's one documented command, which the
    harness runs).
- [ ] T096 [US3] [oxF] **AT-R1, the browser half, on the host.** Drive the
  same install with Playwright (quickstart.md § 4, against the server § 3
  starts). The verdict comes from
  openDox-code's `tests/smoke_signals.py` oracle:
  - the wheel renders the fixture's tiles;
  - the lens renders the radar with the documents as dots, and its seed
    actions behave as R1Q19 decides;
  - opening the workbench from a grouping tile shows the chat rail's "no model
    configured" state, with how to configure one, before any turn;
  - a turn is refused `model_capability_unavailable`, and both editors stay
    usable;
  - there is zero `pageerror`, and nothing undeclared.

  Record the evidence in openxFactory, in this feature's `evidence/at-r1/`, with
  no trailer: this run's oracle verdict, and the URL and verdict of T095's
  `acceptance` job at the same openDox-code commit. Together they are SC-004's
  evidence for both halves.
  - **Realizes**: FR-011 (browser half).
  - **Falsifier**: the oracle's verdict, which must pass: zero `pageerror`, and
    nothing undeclared.
  - **Blocked by**: R1Q13, R1Q19.
  - **Ruled**: R1Q20 (a).
  - **After**: T095.
- [ ] T097 [oxF] **Bookkeeping.**
  - Tick #1144's release-1 boxes, each with its evidence note: the 63 in the
    table below. 3.0 is already ticked (#1151).
  - Leave 9.5, 11.0, 11.1 and F11.1 open for the arc's close.
  - The PR touches `openspec/changes/`, so it lands under a Rule 6
    `LANDING`/`LANDED` window. It carries no `Arc:` trailer (R1Q20 (a)) and no
    closing keyword.
  - Record the non-normative corrections from research R16 in the evidence
    notes.
  - **Ruled**: R1Q20 (a).
  - **After**: T096, T007 (every batch).

---

## Box accounting (#1144 `tasks.md`: 124 boxes)

`python3 "$W/tools/box_census.py" openspec/changes/add-neutral-product-standalone-operability/tasks.md`,
run from an openxFactory checkout (research.md § Appendix writes the tool),
printed `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`
at `cd494e4c`. At `dd2466ad` the counts were 106, 9 and 9, before #1151 ticked
1.8 and 3.0.

| scope | groups | boxes |
|---|---|---|
| **release 1 (this feature)** | 2, 3, 4, 5, 7, 9, 10, 11, 13, 16 | **69** |
| release 2 (a later feature, R1Q21) | 6 (4), 12 (11), 14 (10), 15 (12) | 37 |
| outside both releases | 1 (9, all `[x]` since #1151), 8 (5 `[~]`), F1–F4 (4 `[~]`) | 18 |
| **total** | | **124** |

Release 1's 69 boxes, by class:

| class | count | boxes |
|---|---|---|
| closed by a realization task in release 1 | 63 | every other box below |
| discharged by the ratification | 1 | 3.0 (ticked by #1151, T001) |
| already `[x]` | 1 | 5.6 (openDox-code#35 → `3c3a9e31`) |
| performed in every phase, ticked at ARC close | 4 | 9.5 (T090), 11.0 (T091), 11.1 (T092), F11.1 (T093) |
| **total** | **69** | |

Every release-1 box, with the task that closes it:

| group | box → task |
|---|---|
| 2 (8) | 2.1 → T011 · 2.1a → T011 · 2.2 → T010, T011, T045 · 2.3 → T032 · 2.4 → T030 · 2.5 → T036 · 2.6 → T031 · F2.1 → T049 |
| 3 (5) | 3.0 → T001 · 3.1 → T015 · 3.2 → T016 · 3.3 → T017 · F3.1 → T049 |
| 4 (5) | 4.1 → T020, T021, T046 · 4.1a → T022 · 4.2 → T020 · 4.3 → T012, T021, T025–T027, T046, T055, T084–T086 · F4.1 → T089 |
| 5 (12) | 5.0 → T050 · 5.1 → T054, T056 (and T053 if chosen) · 5.2 → T054 · 5.3 → T054 · 5.3a → T060 · F5.1 → T060 · 5.4 → T052 · 5.4a → T059 · F5.2 → T059, T063 · 5.5 → T055 · 5.6 `[x]` · F5.3 → T063 |
| 7 (8) | 7.0 → T051 · 7.1 → T057 (and T053 if chosen) · 7.1b → T057 · 7.1a → T057 · 7.2 → T057, T058 · 7.3 → T061 · F7.1 → T061 · F7.2 → T058, T063 |
| 9 (8) | 9.1 → T034–T036 · 9.2 → T040, T041, T043, T086 · 9.2a → T030, T036 · 9.3 → T035, T042 · 9.4 → T037, T044 · 9.5 → T039, T040, T047, T059, T062, T064, T086, T087, T094 (T090's steps; arc close) · F9.1 → T049 · F9.2 → T049 |
| 10 (5) | 10.1 → T038 · 10.2 → T075 · 10.2a → T075 · 10.3 → T076 · F10.1 → T077 |
| 11 (3) | 11.0 → T091 · 11.1 → T045, T092 · F11.1 → T093 (all at arc close) |
| 13 (8) | 13.1 → T072 · 13.2 → T071 · 13.3 → T071 · 13.4 → T070 · 13.4a → T073 · 13.5 → T070 · 13.6 → T070 · F13.1 → T074 |
| 16 (7) | 16.1 → T078 · 16.2 → T079 · 16.3 → T080 · 16.4 → T081, T085 · 16.5 → T082 · 16.6 → T034, T083 · F16.1 → T083 |

8 + 5 + 5 + 12 + 8 + 8 + 5 + 3 + 8 + 7 = **69**.

## Dependencies and execution order

- **Phase 0** gates phase 1. T003, T004 (done) and T005 come before T006, and
  T006's round-1a analyze comes before every phase-1 task. T007's batches land
  before the landings and checkpoints that need them: batch A before T047,
  both A and B before T049, C before T059, and D (if RN-1 is ruled (a)) before
  T049. T016, T041 and T043 may land first, quoting the amended falsifier as
  the answer records it (T007).
- **The provisional phases** each open with a round task, T009 for phase 2 and
  T069 for phase 3. It encodes the phase's answers, re-plans the phase and
  re-runs analyze before any other task of that phase starts.
- **Phase 1**: lanes A–E run in parallel, subject to plan.md's single-writer
  table (`serve.py`, `cli.py`, `workbench.py`, `pyproject.toml` and
  `tests/test_authoring_seam.py` in phase 1). They join at T032 and then run
  T034 → T035 → T036 → T037. T031 co-lands in T036's PR. T039 then pins
  openDox's phase-1 commit in the openDox root, after T022, T032, T037 and
  T038. openXdox-code follows: T040 → T041 → T042 → T043 → T044. T047 moves
  the consumer pins after T039, T044 and T007's batch A, and openxFactory's
  host wiring (T045, T046) lands inside T047's openxFactory PR. T017 and T018
  run after T047. T049 closes the phase once RN-1 is ruled.
- **Phase 2**: T009, then T050 → T051 ∥ T052 ∥ T057 (∥ T053), then T054 →
  T055 → T056 → T058; T062 (the phase-2 openDox root pin) after T054–T058; T059 after
  T052, T055, T062 and T007's batch C; T060 after T054; T061 after T049 and
  C3; T064 after T059–T062; T065 after T064; T063 after T064 and T065.
- **Phase 3**: T069, then Group 13 (T071 → T070 → T072 → T073 → T074), with T084 after
  T073 for `serve.py`. In parallel: Group 16's binding slice (T078 → T079 →
  T080), T085 → T081, T075 → T077, and T088. Then T082, which comes after
  T081, T084 and T085, and T083. Then T087 (the phase-3 openDox root pin) →
  T086 → T094 → T098 → T089, and T087 → T076 → T089.
- **Acceptance**: T095 (after T089 and T076) → T096 → T097.

### Parallel slices, summarised

| phase | runs in parallel | is serialized |
|---|---|---|
| 1 | T010–T012 ∥ T015–T016 ∥ T020–T022 ∥ T025–T027 ∥ T030 | `serve.py` and `cli.py` writers; `pyproject.toml` (T038 → T036); `tests/test_authoring_seam.py` (T020 → T022); T020 → T025 and T026 → T025; T032 → T037; T039 (root pin) → openXdox (T040–T044) → T047 → T017, T018 |
| 2 | T050 ∥ T052 ∥ T057 (∥ T053) | T054 → T055 → T056 → T058; T062 → T059 → T064; ratchet writers |
| 3 | Group 13 ∥ 16.1–16.3 ∥ T085 → 16.4 (T081) ∥ T075 ∥ T088 | `serve.py` (T073 before T084); `doxbench_binding.py` (T078 → T080); T085 → T081; T087 → T086 → T094 |

## Phase 1 writer slices (for the fan-out)

Each slice is one writer and one claim (T002) in one repository. Its tasks land
in their `After:` order, one PR each unless a `Lands with:` line joins them, and
each PR quotes its task's falsifier. "Opus" marks a slice that designs a seam or
makes a judgement the packet does not settle. "Sonnet" marks a slice that is
fully specified. Every question phase 1 needed is answered (`5817152735`), so a
slice waits only on T006's round-1a analyze, its claim, and the slices in its
"depends on" column. The **group** column is the parallel group: slices in one
group run at the same time, and a group starts once the one before it has
landed, except where a row says otherwise.

| slice | group | tasks | repo | files | depends on | falsifier it must pass | size |
|---|---|---|---|---|---|---|---|
| P1-A route seam | G1 | T010, T011 (with T030), T012 | oDc | `src/route_extension.py`; `src/opendox/serve.py`; readers of the five lane names; new `tests/test_route_handler_contribution.py` and `tests/test_imports_standalone.py` | T006 | F2.1 (sweep and named test); the new seam tests | Opus |
| P1-B default profile | G1 | T015, T016 | oDc | `src/opendox/domain_profile.py`, `profile_proxy.py`, a new default-profile module; one-line entry calls in `cli.py`/`serve.py`; `tests/test_profile_registration.py` and a vocabulary test | T006; T016 lands after P1-A (T012 is its last `serve.py` edit). RN-1 holds only phase 1's close | F3.1 with line 2 as amended (T007 batch A) | Opus |
| P1-C home-corpus seam | G1 | T020 | oDc | `src/opendox/corpus_adapter.py`; `tests/test_authoring_seam.py` | T006 (it never needed an answer) | F4.1's first block; `…::test_required_header_fields_come_from_the_registered_adapter` | Sonnet |
| P1-E openxFactory reaches | G1; T025 after P1-C | T026, T027, then T025 | oDc | `src/opendox/workbench.py`, `serve_wire.py`, `doxbench_packet.py`, with seam tests | T006; P1-C for T025 | F4.1's scan without `workbench.py:746/1407-1409`, `serve_wire.py:1369` or `doxbench_packet.py:177`; a session-notebook membership test | Opus |
| P1-D authoring and the default adapter | G2 | T021, T022 | oDc | `src/opendox/authoring.py`; entry registration in `cli.py`/`serve.py`; `tests/test_authoring_seam.py` | P1-C, P1-B | `…::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has`; F4.1's first block | Sonnet |
| P1-H console script | G2; rebases onto P1-D for `cli.py` | T038 | oDc | `pyproject.toml` `[project.scripts]`; the default profile's `SUBCOMMAND_EXTENSIONS`; `cli.py`; two comments in `src/opendox/runtime/cli.py` | P1-B; P1-D for `cli.py` | `opendox --help` and `opendox runtime --help` exit 0 | Sonnet |
| P1-F sweep and nine-file repair | G3; it need not wait for P1-H | T032, T034 | oDc | the nine files in research R3 and their Node harnesses | P1-A–P1-E landed | the nine files green; F4.1's scan lists only `openxdox` targets | Opus (the `test_consumer_reach`/`test_boundary` re-pins alone would be Sonnet) |
| P1-G whole suite in CI | G3, after P1-F | T035, T036, T037, T031 | oDc | `conftest.py`; `pyproject.toml` (`testpaths`); `.github/workflows/validate.yml` (a PostgreSQL service and the `.[runtime,test]` install in `validate`); `README.md`; the seven ignored modules | P1-F; P1-H, since both edit `pyproject.toml` | F9.1 (openDox-code), both assertions, with the database DSN exported | Opus |
| P1-R openDox root pin | G4 | T039 | oD | the `code` gitlink, `contracts/code-pin.yaml` and every workflow `@sha`, in ONE commit | every phase-1 openDox-code slice landed (T022, T032, T037, T038) | `make pins` | Sonnet |
| P1-I openXdox pin and residue | G5 | T040 | oXc | `pyproject.toml` (the `opendox @` pin, `rfc3339-validator`); a local helper for the three `test_gate_routes` importers; `tests/fixtures/base-repo` | P1-R | no `test_gate_routes` collection error; `test_snapshot_validation_launch` finds its fixture | Sonnet |
| P1-J openXdox green alone, less the declared exclusion | G5, after P1-I | T041, T042, T043, T044 | oXc | the declared exclusion file and `conftest.py`; `tests/integration/` (new, with `test_assembled_surface.py` and P1-G's relocated modules); `.github/workflows/validate.yml` | P1-I, P1-G; T007 batch B lands once T041 names its file | F9.1 (openXdox-code, as amended by batch B), F9.2 | Opus |
| P1-K pins and host wiring | G6 | T045, T046, T047 | oX, oxF | openXdox root: `code`, `contracts/code-pin.yaml`, `contracts/opendox-pin.yaml`. openxFactory: both pin pairs, plus `scripts/opendox_host.py`, `scripts/profile_openxfactory.py`, `tests/domain_profile/`, `tests/ideation-dashboard/test_extension_point_parity.py` and `tests/ideation-dashboard/test_serve_column_split.py` (and, as named composition tests, `test_session_harness.py` or `test_outline_model.py`'s `doc_health` case if T035 or T034 moves one here) | P1-R, P1-J; T007 batch A (F11.1 names both composition tests) | `make pins` in the openXdox root; `verify-opendox-pin.py`, `verify-openxdox-pin.py`; openxFactory `pytest-suite` | Opus |
| P1-L read-only checks | G6, after P1-K | T017, T018 | oxF | `evidence/` only | P1-K | interim F11.1 (T018, by T093's procedure), as widened by batch A, prints `requirement 1 holds` | Sonnet |
| checkpoint | G6, last | T049 | — | none (a verifier) | P1-K, P1-L; T007 batches A and B; RN-1 ruled | F2.1; F3.1 as amended; F9.1 in both legs; F9.2; `opendox --help`; F4.1's scan | Opus (verifier) |

**Fan-out order.** Before any slice: T006's round-1a analyze, and the slice's
claim (T002).

1. **G1**: P1-A, P1-B, P1-C and P1-E in parallel. P1-B's T016 lands after
   P1-A, because both write `serve.py`, and P1-E's T025 waits for P1-C.
2. **G2**: P1-D and P1-H in parallel. P1-H rebases onto P1-D for `cli.py`.
3. **G3**: P1-F, then P1-G.
4. **G4**: P1-R, the openDox root pin.
5. **G5**: P1-I, then P1-J.
6. **G6**: P1-K, then P1-L, then T049.

P1-K's host wiring (T045, T046) can be authored once P1-A and P1-C–P1-E have
landed, and it lands inside T047's PR. The holder works beside the slices:
T007's batches A and C and T008 now, and T007 batch B with P1-J.

## Ruled amendments (`5817152735`)

Brett Heap's answers amend #1144's falsifiers, task lines and one design note.
They amend no requirement and no scenario. T007 records each amendment in
#1144's `tasks.md` (and the D4 addendum in `design.md`) as bookkeeping, and the
realization tasks beside it carry it out. The one
scenario text an answer touches is not listed here: it is RN-1 (plan.md
§ "Ruling needed"), and T007's batch D lands it only if Brett rules RN-1 (a).

| batch | #1144 line | the amendment | from | carried out by |
|---|---|---|---|---|
| A | F3.1, line 2 | The line asks after `build_parser()`: `python -c "from opendox.cli import build_parser; from opendox import domain_profile as d; build_parser(); print('OK', d.name_of(d.current()))"`. The prose under it adds that a bare process that builds nothing still meets `ProfileNotRegistered`, which `tests/test_profile_registration.py` asserts. | R1Q3 (a) | T016, T049 |
| A | 3.2 | "fall back to it" becomes "register it", because the default is a registration the entry point makes. The refusal `profile_proxy.py` keeps is the one it was written for, NOTHING REGISTERED (`profile_proxy.py:42-46`). It is not "an ambiguous registration": that case is `AlreadyRegistered`. A host registration made before a build replaces the default. (ii)'s after-build refusal joins 3.2 only with RN-1. | R1Q3 (a), (i), (ii) | T016 |
| A | 2.2; `design.md` § D4 | An addendum. The routes still travel through the `RouteBinding` seam. The methods they name travel through a handler-contribution facet that openDox declares, which D4's "no new mechanism" did not foresee. openxFactory's half gains the `LaneRoutes` declaration. | R1Q1 (a) | T010, T011, T045 |
| A | 4.3 | Of `workbench.py`'s four reaches, only three (`:1407-1409`) are the ones `run_scoped_doc_health` makes. The fourth, `session_documents` (`:746`), resolves through the registered adapter's `list_documents` in phase 1, and the hosted membership rule is unchanged. | R1Q9 (a) | T025, T026, T046 |
| A | 10.1 | An addendum. Q-R4's condition is discharged through the default profile's `SUBCOMMAND_EXTENSIONS` (`RuntimeSubcommand`). `opendox-runtime` stays as an alias, and a host's own profile keeps the 31-entry tree. | R1Q5 (a) | T038, T042 |
| A | 11.0 | An addendum. Bookkeeping is not an arc landing and carries no trailer: the Speckit feature files, #1144's ticks, evidence notes and amendments, and interim guard output. | R1Q20 (a) | T091 |
| A | 11.1; F11.1 | A fourth declared surface: NAMED openxFactory composition tests, which may be edited or added and are never removed. The guard gains `COMPOSITION_TESTS = {"tests/ideation-dashboard/test_extension_point_parity.py", "tests/ideation-dashboard/test_serve_column_split.py"}` beside `HOST`. A later batch adds a path before the landing that adds it (T034, T035), or that T047's `pytest-suite` run finds. Also an addendum to 11.1: the manifest records the carve as it arrived, so an arc edit to a carved file needs no declared-edit act. | R1Q2 (a); R1Q22 (a) | T045, T093, T094 |
| B | F9.1 (openXdox-code) | `python -m pytest -q` collects the whole suite less the files in T041's declared exclusion file. The falsifier asserts three things: the file's count equals its entries, every entry carries its reason, and the run prints the exclusion as an open extraction. The two `validate.yml` assertions stay. openDox-code's F9.1 is unchanged (R1Q8 (a)). | R1Q6 (d) | T041, T043, T049 |
| B | 9.4 | An addendum: each of openXdox's six skips either asserts, or its file joins the declared exclusion. | R1Q6 (d) | T044 |
| C | F5.2; 12.5's falsifier | The "unedited by the arc" check subtracts the edits entered in a reviewed allow-list in openXdox-code, such as `tests/protected_suite_respellings.yaml`. Each entry names the suite, the landing, the reference it respelled, and its review. No edit that weakens an assertion is entered. | R1Q7 (a) | T043, T059, T086 |

R1Q4 (a) and R1Q8 (a) amend nothing in #1144. They shape T015, T038, T046 and
T036 only.
