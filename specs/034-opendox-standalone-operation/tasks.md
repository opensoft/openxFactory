# Tasks: openDox standalone operation (release 1)

**Input**: [`spec.md`](./spec.md), [`plan.md`](./plan.md), [`research.md`](./research.md),
[`clarify-questions.md`](./clarify-questions.md), and #1144's ratified
`openspec/changes/add-neutral-product-standalone-operability/tasks.md`, which
holds the boxes and every falsifier.
**Lane**: `openxfactory-4`

## Format

`- [ ] T### [P?] [US#] [repo] Title`, followed by up to four lines:

- **Realizes**: the #1144 boxes the task closes, or advances when marked
  "(part)".
- **Falsifier**: the #1144 falsifier or named test the task must pass, quoted
  in its PR.
- **Blocked by**: the open `R1Q` questions, if any. No task starts while one
  of these is open (FR-012).
- **After**: tasks that must land first.

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
- **Falsifier labels**: `F<g>.<n>` is the n-th `FALSIFIED BY` box of #1144's
  Group g, in document order. `research.md` § Appendix `box_census.py` prints
  every label.

Every realization task lands through its repository's own PR, with the `Arc:`
and `Lane:` trailers (T091). Only the holder lands. Every writer works in its
OWN clone, runs `cd <clone> || exit 1` in every call, and names the repository
with `-R` in every `gh` call.

## Unblocked today

These need no answer: **T002**, **T003** and **T005** (holder; T001 is done), **T017** (a
read-only check), and **T020** (`corpus_adapter.py` was created at the
destination, so it has no carve row, and 4.1 and 4.2 specify it completely).
**T030** can be authored now and lands with T011, because it fails until 2.1
lands. Nothing else starts until T004 has applied the answers its
`Blocked by` line names.

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

  Lane 4's C3 and C4 are live objects (plan.md § "In-flight overlaps").
- [ ] T003 **ARC_BASE.** Record, per repository, the `main` commit before the
  arc's first landing there: openDox-code, openXdox-code, openDox, openXdox and
  openxFactory. For openxFactory's guard, `PACKET_MERGE` is `94b6f7f1` (11.1).
  Record them in `evidence/arc-base.md`, with no `Arc:` trailer (R1Q20).
  - **Blocked by**: R1Q20 (the commit's form only).
- [ ] T004 **Apply the answers.**
  - Encode each R1Q answer into `spec.md`, in the commit that records it.
  - Land every answer that amends a #1144 falsifier or task line in #1144's
    `tasks.md`, under a Rule 6 window, citing Brett's word.
  - Bring any answer that would change a requirement's text back to Brett as
    a ruling.
  - Re-plan `plan.md` and this file on the answers.
- [ ] T005 **Re-measure.** Re-run research R1–R15 at the then-current `main`s,
  using the persisted tools. Record the drift from the 2026-09-24 figures
  (R13 already shows one pin drifting).
- [ ] T006 **Analyze.** `/speckit-analyze` over spec, plan and tasks after
  T004. No CRITICAL finding may stand before any realization task starts (the
  constitution's workflow gate).
  - **After**: T004.

---

## Phase 1: it runs (US1 and US4)

**Goal**: openDox-code imports, builds its parser on its own default profile,
registers its own default adapter, and runs its whole suite green. openXdox-code
runs its whole suite green, or the declared exclusion R1Q6 (d) admits. The
`opendox` console script exists. openxFactory is unchanged in behaviour.

**Independent test**: T049.

### Lane A: the route seam (`src/opendox/serve.py`, `src/route_extension.py`; single writer)

- [ ] T010 [US1] [oDc] **Declare the handler contribution R1Q1 selects.** The
  recommended form: a profile or extension facet that names mixin classes;
  `build_server` composes them into `BoundDashboardHandler`'s bases; and
  `resolve_handlers` is unchanged. Tests:
  - a binding naming a method that only a contributed mixin has resolves;
  - a binding naming a method no class has is refused at wiring time.
  - **Realizes**: 2.2 (the mechanism).
  - **Falsifier**: a new `tests/test_route_handler_contribution.py`.
  - **Blocked by**: R1Q1, R1Q22.
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
  - **Blocked by**: R1Q1, R1Q22.
  - **After**: T010.
- [ ] T012 [US1] [oDc] **`serve.py:713`** (`doc_health.corpus.RealGit` in
  `_head_of`). Replace it with openDox's own HEAD reader. It must keep
  degrading to `None`.
  - **Realizes**: 4.3 (1 of the 8 reaches into openxFactory).
  - **Falsifier**: F4.1's scan no longer lists `serve.py:713`.
  - **Blocked by**: R1Q22.
  - **After**: T011.

### Lane B: the default profile

- [ ] T015 [P] [US1] [oDc] **Ship openDox's default profile for its own domain**
  (documents and ideas).
  - It carries none of openxFactory's `Status:` taxonomy, change/spec/delta
    nouns or act verbs, and its `DISPLAY` is `NEUTRAL_DISPLAY` unchanged.
  - Its extension contents follow R1Q4; recommended: openDox's own verbs,
    including `RuntimeSubcommand` (R1Q5).
  - A test holds the vocabulary out (requirement 3, second scenario).
  - **Realizes**: 3.1.
  - **Falsifier**: F3.1; the new vocabulary test.
  - **Blocked by**: R1Q4.
  - **After**: T006.
- [ ] T016 [US1] [oDc] **Registration semantics, per R1Q3.**
  - Recommended: `build_parser()`, `build_server()` and `main()` register the
    default where nothing is registered, and a registered profile replaces it.
  - `profile_proxy`'s refusals are kept, and never weakened into `()`.
  - A late registration after a build is handled as R1Q3 (ii) decides.
  - The one-line entry-point calls in `serve.py` and `cli.py` rebase onto Lane
    A.
  - **Realizes**: 3.2.
  - **Falsifier**: F3.1 (line 2 as amended per R1Q3), `tests/test_profile_registration.py`.
  - **Blocked by**: R1Q3, R1Q22.
  - **After**: T015, T011.
- [ ] T017 [P] [US4] [oxF] **3.3, read-only.** At every openxFactory arc
  landing, confirm that the carve manifest's `deleted_at_carve` row for
  `scripts/ideation_dashboard/profile_openxfactory.py` is byte-identical. F11.1's
  content check already refuses any row change, so T093's run is the evidence.
  - **Realizes**: 3.3.
  - **Falsifier**: F11.1 (interim, T093).
  - **After**: —.

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
  - **After**: —. Unblocked today.
- [ ] T021 [US1] [oDc] **`authoring.py:318`** resolves the home corpus through
  `corpus_adapter.home()`.
  - **Realizes**: 4.1, 4.3 (1 of 8).
  - **Falsifier**: F4.1's first block.
  - **Blocked by**: R1Q22.
  - **After**: T020.
- [ ] T022 [US1] [oDc] **4.1a: openDox's own default adapter.** Where no host
  called `register_home`, the entry points register a `home_corpus`-shaped
  factory over `LocalGitCorpus`. It starts at `LocalGitCorpus()`'s defaults
  (`required_fields=()`), and phase 2's T054 sets the neutral fields that
  R1Q13 decides. A bare process still refuses.
  - **Realizes**: 4.1a.
  - **Falsifier**: `tests/test_authoring_seam.py::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has`.
  - **Blocked by**: R1Q3, R1Q22.
  - **After**: T020, T016.

### Lane D: the other openxFactory reaches (`workbench.py`, `serve_wire.py`, `doxbench_packet.py`)

- [ ] T025 [P] [US1] [oDc] **`workbench.py:746`** (`session_documents`), per
  R1Q9. Recommended: resolve through the registered adapter's
  `list_documents`, and prove the hosted membership rule unchanged.
  - **Realizes**: 4.3 (1 of 8).
  - **Falsifier**: F4.1's scan; a session-notebook membership test.
  - **Blocked by**: R1Q9, R1Q22.
  - **After**: T020.
- [ ] T026 [P] [US1] [oDc] **`workbench.py:1407-1409`** (`run_scoped_doc_health`).
  Route it through a declared health-check seam that, with nothing registered,
  returns `status = not-available` and names the seam. It stays that way until
  Group 6 (release 2) registers openDox's own check.
  - **Realizes**: 4.3 (3 of 8).
  - **Falsifier**: F4.1's scan; a seam test.
  - **Blocked by**: R1Q22.
  - **After**: T006.
- [ ] T027 [P] [US1] [oDc] **`serve_wire.py:1369` and `doxbench_packet.py:177`.**
  - The doxBench schema validators and the status-exemption rail become seams.
    Each fails closed, naming itself, when nothing is registered.
  - openxFactory registers its own (T046).
  - The standalone defaults are T085's (phase 3).
  - **Realizes**: 4.3 (2 of 8).
  - **Falsifier**: F4.1's scan; seam tests.
  - **Blocked by**: R1Q22. The phase-1 seam fails closed exactly as 4.2
    does; R1Q10 and R1Q12 decide only T085's standalone defaults.
  - **After**: T006.

### Lane E: the instrument and the README

- [ ] T030 [P] [US1] [oDc] **2.4: the import-every-module test.**
  `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`
  walks the package with `pkgutil`. It fails naming the first module that needs
  a sibling, and it first asserts the siblings are absent. It is authored now
  and lands with T011.
  - **Realizes**: 2.4; 9.2a (the instrument; T036 makes a required check run
    it).
  - **Falsifier**: F2.1's last line.
  - **After**: —.
- [ ] T031 [US1] [oDc] **2.6: `README.md:39-42`.** State the live cause
  (`ideation_dashboard`, not the openDox → openXdox inversion). Once the
  narrowing ends, rewrite the paragraph. Lands with T036.
  - **Realizes**: 2.6.
  - **Falsifier**: review.
  - **After**: T036.

### Join: the sweep, the suite, the console script

- [ ] T032 [US1] [oDc] **2.3: the sweep.** Grep `src/` for `ideation_dashboard`,
  `corpus_adapter_openxfactory`, `doc_health` and `openxdox` in import
  position. Record, for each hit, whether it is closed or deferred, with its
  reason, in the PR body. The expected state is: no import-time reach, and 19
  deferred reaches, all into `openxdox`.
  - **Realizes**: 2.3.
  - **Falsifier**: F4.1's scan, which lists only `openxdox` targets.
  - **After**: T011, T012, T021, T025–T027.
- [ ] T034 [US1] [oDc] **Repair the nine files that go red once 2.1 lands**
  (research R3; 86 failures and errors). Update the Node harnesses to the
  views; replace carve-residue paths and module literals; re-derive
  `test_consumer_reach.py`'s `STILL_REACHING`; re-pin `test_boundary.py`'s
  census.
  - `test_provider_boundary.py` is repaired for 16.6's three reasons (*"the file
    is repaired in phase 1"*).
  - `test_outline_model.py`'s `doc_health` case becomes an integration test
    where the composition is declared (R1Q2, R1Q6), or is rewritten against
    openDox's own contract.
  - **Realizes**: 9.1 (part), 16.6 (the phase-1 repair).
  - **Falsifier**: `python -m pytest -q` over the nine files.
  - **Blocked by**: R1Q2 (for `test_outline_model.py` only).
  - **After**: T011.
- [ ] T035 [US1] [oDc] **Empty the root `conftest.py`'s `collect_ignore`**
  (seven modules; research R4).
  - The six that import `openxdox` become openXdox-code `tests/integration/`
    tests (T042), or are rewritten as neutral tests.
  - `test_session_harness.py`, which runs a script only openxFactory has,
    moves where that script lives (R1Q2), or is rewritten.
  - **Realizes**: 9.1 (part), 9.3 (part).
  - **Falsifier**: F9.1 (openDox-code).
  - **Blocked by**: R1Q2, R1Q6.
  - **After**: T034.
- [ ] T036 [US1] [oDc] **The required check runs the whole suite.**
  - Remove `validate.yml`'s three `--noconftest` steps and their file lists.
    Also remove the 15 comment lines that name the flag, because F9.1's
    `grep -c` counts comments.
  - Set `testpaths` per R1Q8.
  - Re-pin the floors to the measured whole-suite counts.
  - T031 lands in the same PR.
  - **Realizes**: 2.5, 9.1, 9.2a (a required check now runs T030).
  - **Falsifier**: F9.1 (openDox-code), both of its assertions.
  - **Blocked by**: R1Q8.
  - **After**: T035.
- [ ] T037 [US1] [oDc] **9.4, openDox's half.** Restore the margin over the
  floors. The two skips that mirror openXdox's gap assert for real.
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple in `validate.yml`.
  - **After**: T036.
- [ ] T038 [US1] [oDc] **10.1: `[project.scripts] opendox = "opendox.cli:main"`**,
  with Q-R4's runtime verbs wired as R1Q5 decides. Recommended: through the
  default profile's `SUBCOMMAND_EXTENSIONS`, keeping `opendox-runtime` as an
  alias.
  - **Realizes**: 10.1.
  - **Falsifier**: `opendox --help` exits 0 (F10.1's first assertion, which is
    phase 1's proof); `opendox runtime --help` exits 0.
  - **Blocked by**: R1Q4, R1Q5, R1Q22.
  - **After**: T016.

### openXdox-code: green alone

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
  - **After**: T047's step 2.
- [ ] T041 [US1] [oXc] **`doc_health` reachability, per R1Q6.** Recommended
  for release 1: a DECLARED exclusion list, with its count and its reason
  (requirement 9, first scenario), with F9.1 amended by T004. Otherwise, the
  option Brett chooses.
  - **Realizes**: 9.2 (part).
  - **Falsifier**: F9.1 (openXdox-code) as amended.
  - **Blocked by**: R1Q6.
  - **After**: T040.
- [ ] T042 [US1] [oXc] **9.3: `tests/integration/`.**
  - Add the 31-entry assembled `--help` tree:
    `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`.
  - Add T035's relocated modules.
  - Each test names the pin it composes at.
  - **Realizes**: 9.3.
  - **Falsifier**: F9.2.
  - **Blocked by**: R1Q5.
  - **After**: T040.
- [ ] T043 [US1] [oXc] **9.2: the required check runs the whole suite.**
  Remove the file list and all 8 `--noconftest` lines. Re-pin
  `MIN_SELECTED`/`MIN_PASSED` (now 564/558) and `EXPECT_SKIPPED` to the
  measured whole-suite triple.
  - **Realizes**: 9.2.
  - **Falsifier**: F9.1 (openXdox-code).
  - **Blocked by**: R1Q6, R1Q7 (for `test_branch_session.py`).
  - **After**: T041, T042.
- [ ] T044 [US1] [oXc] **9.4, openXdox's half.** The six skips, each deferring
  *"`doc_health` reachability"*, either assert for real or become the declared
  exclusion R1Q6 decides.
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple.
  - **Blocked by**: R1Q6.
  - **After**: T043.

### openxFactory: the host keeps working (US4)

- [ ] T045 [US4] [oxF] **The lanes column, through R1Q1's mechanism.**
  `scripts/profile_openxfactory.py` declares `LaneRoutes`, with tests under
  `tests/domain_profile/`. `test_extension_point_parity.py`'s MRO assertion is
  updated as R1Q2 decides. This lands in T047's PR.
  - **Realizes**: 2.2 (openxFactory half), 11.1 (surface).
  - **Falsifier**: openxFactory's `pytest-suite`; the five lane routes are
    served.
  - **Blocked by**: R1Q1, R1Q2.
  - **After**: T011.
- [ ] T046 [US4] [oxF] **The other host wiring.** The host registers
  `corpus_adapter_openxfactory.home_corpus` via `register_home` (4.1), and
  registers its `doc_health`, session-notebook, doxBench-validator and
  status-exemption implementations with T025–T027's seams. Its own start
  asserts that its profile is the registered one (R1Q4 (a)). Tests go under
  `tests/domain_profile/`. This lands in T047's PR.
  - **Realizes**: 4.1 (host half), 4.3 (host half).
  - **Falsifier**: `pytest-suite`; the hosted session notebook is unchanged.
  - **Blocked by**: R1Q2, R1Q4, R1Q9.
  - **After**: T020–T027.
- [ ] T047 [US4] [oD] [oX] [oxF] **Phase 1's pin advance**, run as T090's
  procedure. openxFactory's PR carries T045 and T046.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in each root; `verify-opendox-pin.py` and
    `verify-openxdox-pin.py`; `pytest-suite`.
  - **After**: T038, T043.
- [ ] T048 **The F4 re-measure (holder).** After phase 1 lands, re-measure
  openxFactory's direct `opendox` imports and bring Brett the direct-arrow
  question (F4, outside both releases; `5799494355`).
  - **After**: T049.
- [ ] T049 **Phase 1 checkpoint.** Run and quote:
  - F2.1 and F3.1;
  - F9.1 in each leg, and F9.2;
  - `opendox --help`;
  - F4.1's scan, which must list only `openxdox` targets;
  - T093's interim F11.1.

  Tick nothing; T097 ticks.
  - **After**: T047.

---

## Phase 2: useful alone (US2 and US4)

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
  - **After**: T049.
- [ ] T051 [P] [US2] [oDc] **7.0: `tests/fixtures/malformed`.** Exactly one
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
  - **After**: T049.
- [ ] T053 [P] [US2] [oDs] [oD] **The neutral snapshot contract. CONDITIONAL:
  only on R1Q11 (a) or R1Q12 (b).** The schema lands in openDox-spec, then the
  openDox root's spec pin moves, then the bundle is cut if Brett's answer
  requires it (a `dox-v1.x` minor under the root's four-value rule).
  - **Realizes**: 5.1 and 7.1 (their contract).
  - **Falsifier**: the root's `make validate`.
  - **Blocked by**: R1Q11, R1Q12.
  - **After**: T004.
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
  - **Blocked by**: R1Q10, R1Q22.
  - **After**: T054.
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
  - **Blocked by**: R1Q12, R1Q22.
  - **After**: T049.
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
    any arc landing.
  - **Blocked by**: R1Q6, R1Q7.
  - **After**: T052, T055, T062's step 2.
- [ ] T060 [US4] [oXc] **5.3a: re-run F5.1 against the realized openDox.** The
  facet landed before the arc (#26 and #27), so no code change is expected.
  - **Realizes**: 5.3a, F5.1.
  - **Falsifier**: F5.1.
  - **After**: T054.
- [ ] T061 [US4] [oXc] **7.3: the consumer's validator lookup through the
  installed distribution**, with no parent walk. C3's
  `test_a_start_outside_the_product_is_refused_not_walked` is revised in the
  same landing (R1Q14 (a)).
  - **Realizes**: 7.3.
  - **Falsifier**: F7.1, including its two named tests.
  - **Blocked by**: R1Q14.
  - **After**: C3's openXdox-code PR (PR 2) has landed.
- [ ] T062 [US4] [oD] [oX] [oxF] **Phase 2's pin advance** (T090). Host wiring
  is needed only if openxFactory's composite has to register a generator
  contribution. It composes openXdox's profile, so none is expected; confirm
  that by `pytest-suite`.
  - **Realizes**: 9.5 (part).
  - **After**: T058, T059.
- [ ] T063 **Phase 2 checkpoint.** Run and quote F5.1, F5.2, F5.3, F7.1 and
  F7.2, then a standalone `generate-and-open` serving the fixture, then T093.
  - **After**: T062, T060, T061.

---

## Phase 3: it installs (US3 and US4)

**Goal**: one documented command installs and starts the whole product, with
its bundled datastore, the local mode, the served bundle, and chat with a clear
no-model state. `consumer_reach.py` is gone.

**Independent test**: T089, then T095 and T096.

### Group 13: the install's shape (`runtime/`)

- [ ] T071 [US3] [oDc] **13.2 and 13.3.** `load_settings` refuses a
  non-PostgreSQL DSN, naming the one dialect kept. It refuses the same
  credential in both settings, naming `OPENDOX_MIGRATION_DATABASE_URL`. The
  migration DSN stops being optional.
  - **Realizes**: 13.2, 13.3.
  - **Falsifier**: F13.1's `load_settings` block.
  - **After**: T063.
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
  - **Falsifier**: F13.1's `/proc/net/tcp` and `runtime status` blocks.
  - **Blocked by**: R1Q16.
  - **After**: T070.
- [ ] T073 [US3] [oDc] **13.4a: `/capabilities` gains an `install` block**,
  read from the serving process's own settings. `serve.py` is a single-writer
  file.
  - **Realizes**: 13.4a.
  - **Falsifier**: F13.1's `caps.json` block.
  - **Blocked by**: R1Q16, R1Q22.
  - **After**: T072.
- [ ] T074 [US3] [oDc] **Run F13.1**, as amended per R1Q15 and R1Q16.
  - **Realizes**: F13.1.
  - **Blocked by**: R1Q15, R1Q16.
  - **After**: T073.

### Group 10: the door

- [ ] T075 [US3] [oDc] **10.2 and 10.2a.** The entry point serves the 42-file
  bundle, reachable in a browser from an openDox-only install. `intent-feed.js`
  is not owed (10.2a is a declaration, recorded in the PR).
  - **Realizes**: 10.2, 10.2a.
  - **Falsifier**: F10.1's fetch.
  - **After**: T056, T038.
- [ ] T076 [US3] [oD] **10.3: the openDox root's `README.md` documents the one
  command.** No `Makefile` target is added, since it has a shape-pin row.
  - **Realizes**: 10.3.
  - **Falsifier**: review, and AT-R1 step 4 follows it literally.
  - **Blocked by**: R1Q15.
  - **After**: T074, T075.
- [ ] T077 [US3] [oDc] **Run F10.1**, as amended per R1Q15.
  - **Realizes**: F10.1.
  - **Blocked by**: R1Q15.
  - **After**: T075, T070.

### Group 16: chat's model configuration (`doxbench_binding.py`, then `doxbench_provider.py`)

- [ ] T078 [US3] [oDc] **16.1: `openai-chat-v1`.** A second `DIALECTS` member.
  The chat-completions request (`model`, `messages`) and its answer
  (`choices[0].message.content`) are spoken by an arm in
  `doxbench_provider.py` alone. An unknown dialect is still refused.
  - **Realizes**: 16.1.
  - **Falsifier**: F16.1's dialect assertion.
  - **Blocked by**: R1Q22 (`doxbench_binding.py` is `moved_verbatim`).
  - **After**: T063.
- [ ] T079 [US3] [oDc] **16.2: a `model` field**, sent as the request's model
  and set by `model-binding add|edit --model`. The record grows from nine
  fields to ten, and none of them can hold a secret.
  - **Realizes**: 16.2.
  - **Falsifier**: F16.1's `BINDING_FIELDS` assertion.
  - **Blocked by**: R1Q22.
  - **After**: T078.
- [ ] T080 [US3] [oDc] **16.3: refuse a raw key when it is declared.**
  - Keys in the URL and in extra fields are refused, via `carries_a_credential`.
  - The no-credential declaration follows R1Q18, and the reference resolver
    follows R1Q17.
  - **Realizes**: 16.3.
  - **Falsifier**: F16.1's three refusals.
  - **Blocked by**: R1Q17, R1Q18, R1Q22.
  - **After**: T079.
- [ ] T081 [P] [US3] [oDc] **16.4: "no model configured" is a state.**
  - With no binding and no harness, the catalog offers no available entry.
  - The chat rail shows "no model configured" AND how to configure one, before
    any turn. Today's copy (research R15) does not name how.
  - A turn is refused `model_capability_unavailable` before any spawn or
    contact.
  - The harness route stays, for an install where it is present.
  - The SERVED catalog route answers standalone; that needs T085.
  - **Realizes**: 16.4.
  - **Falsifier**: F16.1's catalog block; `tests/test_chat_model_configuration.py`.
  - **Blocked by**: R1Q10, R1Q22.
  - **After**: T063.
- [ ] T082 [US3] [oDc] **16.5: every other surface works with no model.** The
  named test covers documents, generation, the views, sessions and saving.
  - **Realizes**: 16.5.
  - **Falsifier**: `tests/test_chat_model_configuration.py`.
  - **Blocked by**: R1Q10.
  - **After**: T081, T084, T085.
- [ ] T083 [US3] [oDc] **16.6, then F16.1.** `tests/test_provider_boundary.py`
  stays green as 16.1 joins the one module. Then run F16.1 whole.
  - **Realizes**: 16.6, F16.1.
  - **After**: T080, T081, T082.

### 4.3's last reaches, and the consumer's columns

- [ ] T084 [US3] [oDc] **Route everything left, and retire `consumer_reach.py`.**
  - Route `serve_workbench.py`'s seven (`:347`, `:407`, `:408`, `:544`,
    `:1215`, `:1665`, `:2607`), `serve_project.py:246/:247`, and
    `branch_session.py:1587/:2005`.
  - Route the `gate_console` names (27 uses), `hosted_ref_refused` (2), and the
    `LateGateRoutes` and `LateProjectionRoutes` bases, through declared seams
    with openDox defaults (R1Q10 (a)).
  - Hand the gate and projection columns to R1Q1's mechanism.
  - **Realizes**: 4.3.
  - **Falsifier**: F4.1 whole: `consumer_reach.py` is absent, and the scan
    prints `no deferred reach names the consumer or the publisher`.
  - **Blocked by**: R1Q1, R1Q10, R1Q22.
  - **After**: T055.
- [ ] T085 [US3] [oDc] **The standalone doxBench defaults for T027's seams.**
  openDox's own validators run over openDox-spec's `xfactory-workbench-chat-turn`
  and `xfactory-workbench-model-catalog` copies (R1Q12). There is no status
  exemption by default.
  - **Realizes**: 4.3 (part), 16.4 (part).
  - **Falsifier**: the served catalog route answers, with no available entry.
  - **Blocked by**: R1Q10, R1Q12.
  - **After**: T057.
- [ ] T086 [US4] [oXc] **openXdox contributes its columns.** It contributes the
  gate and projection mixins, `doxbench_scope` and its gate primitives through
  the seams. `OPENDOX_BACK_IMPORTS` becomes `(0, 0)` in the SAME landing that
  moves the pin to T084's commit (4.3's wording).
  - **Realizes**: 4.3 (consumer half), 9.2 (the ratchet).
  - **Falsifier**: `tests/test_dependency_direction.py`; F9.1 (openXdox-code).
  - **Blocked by**: R1Q1, R1Q7.
  - **After**: T084, T087's step 2.
- [ ] T088 [US3] [oDc] **The lens's two seed actions**, handled as R1Q19
  decides. Recommended: offered only where a binding answers them.
  - **Realizes**: none of the 69; this is the precondition for AT-R1 step 6.
  - **Falsifier**: AT-R1 step 6.
  - **Blocked by**: R1Q19, R1Q22.
  - **After**: T063.
- [ ] T087 [US4] [oD] [oX] [oxF] **Phase 3's pin advance** (T090). openxFactory's
  PR carries whatever host wiring the retired columns need, such as the parity
  test per R1Q2.
  - **Realizes**: 9.5 (part).
  - **Blocked by**: R1Q2.
  - **After**: T084, T086.
- [ ] T089 **Phase 3 checkpoint.** Run and quote F4.1, F10.1, F13.1 and F16.1,
  then T093.
  - **After**: T087, T074, T077, T083.

---

## Every phase

- [ ] T090 [US4] **The pin procedure (9.5)**, run once per phase as T047, T062
  and T087. The order is:
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

  Follow C4's runbook once it lands. Every one of these is an ancestor move,
  cutting no bundle unless T053 applies.
  - **Realizes**: 9.5, which is ticked at ARC close.
- [ ] T091 **The trailer (11.0).** Every realization commit and every landing,
  in all five repositories, carries `Arc: neutral-product-standalone-operability`
  as well as `Lane: openxfactory-4`. A merge landing writes the trailer into
  the merge message. Land by squash or merge, never rebase. Bookkeeping
  follows R1Q20 (recommended: no trailer).
  - **Realizes**: 11.0, which is ticked at ARC close.
  - **Blocked by**: R1Q20 (bookkeeping only).
- [ ] T092 [oxF] **11.1's notes.** One `edits[].note` per closed reach, added
  where an existing `edits[]` entry has none, or extended, and never rewritten.
  No row, field or digest changes. Whether carved-file edits need more than
  this is R1Q22.
  - **Realizes**: 11.1, which is ticked at ARC close.
  - **Blocked by**: R1Q22.
- [ ] T093 [oxF] **An interim F11.1** after each phase's openxFactory landings,
  with `PACKET_MERGE=94b6f7f1` and `ARC_TIP` set to the phase's last arc
  landing. Record the output in `evidence/f11.1-phase<n>.txt`, with no
  trailer.
  - **Realizes**: F11.1, which is ticked at ARC close.
  - **Blocked by**: R1Q20 (the evidence commit's form).

---

## Acceptance: AT-R1

- [ ] T095 [US3] [oDc] **AT-R1, the HTTP half, in CI.**
  `tests/test_release1_acceptance.py` does the following:
  - installs openDox alone, as R1Q16 decides, into a fresh venv;
  - ASSERTS that the four siblings, `omp`, a database and a binding are all
    absent;
  - copies both plain repositories into fresh `git init`s (spec.md AT-R1
    step 3);
  - runs the documented command (R1Q15) on loopback;
  - fetches `/` (it must be HTML), `/snapshot.json` (non-empty, neutral per
    F5.3) and `/capabilities` (`install.mode == local`);
  - fetches the model-catalog route, which must answer with no available
    entry;
  - fetches every route the wheel, the lens and the chat rail request on load,
    none of which may answer 5xx.
  - **Realizes**: FR-011 (HTTP half).
  - **Falsifier**: the test itself.
  - **Blocked by**: R1Q10, R1Q15, R1Q16.
  - **After**: T089.
- [ ] T096 [US3] **AT-R1, the browser half, on the host.** Drive the same
  install with Playwright (quickstart.md § 3). The verdict comes from
  openDox-code's `tests/smoke_signals.py` oracle:
  - the wheel renders the fixture's tiles;
  - the lens renders the radar with the documents as dots, and its seed
    actions behave as R1Q19 decides;
  - opening the workbench from a grouping tile shows the chat rail's "no model
    configured" state, with how to configure one, before any turn;
  - a turn is refused `model_capability_unavailable`;
  - there is zero `pageerror`, and nothing undeclared.

  Record the evidence in `evidence/at-r1/`, with no trailer.
  - **Realizes**: FR-011 (browser half).
  - **Blocked by**: R1Q13, R1Q19, R1Q20 (the evidence commit's form).
  - **After**: T095.
- [ ] T097 [oxF] **Bookkeeping.**
  - Tick #1144's release-1 boxes, each with its evidence note: the 63 in the
    table below. 3.0 is already ticked (#1151).
  - Leave 9.5, 11.0, 11.1 and F11.1 open for the arc's close.
  - The PR touches `openspec/changes/`, so it lands under a Rule 6
    `LANDING`/`LANDED` window. It carries no `Arc:` trailer (R1Q20) and no
    closing keyword.
  - Record the non-normative corrections from research R16 in the evidence
    notes.
  - **Blocked by**: R1Q20.
  - **After**: T096.

---

## Box accounting (#1144 `tasks.md`: 124 boxes)

`python3 box_census.py openspec/changes/add-neutral-product-standalone-operability/tasks.md`
(from research.md § Appendix) printed `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`
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
| 4 (5) | 4.1 → T020, T021, T046 · 4.1a → T022 · 4.2 → T020 · 4.3 → T012, T021, T025–T027, T055, T084–T086 · F4.1 → T089 |
| 5 (12) | 5.0 → T050 · 5.1 → T054 · 5.2 → T054 · 5.3 → T054 · 5.3a → T060 · F5.1 → T060 · 5.4 → T052 · 5.4a → T059 · F5.2 → T059, T063 · 5.5 → T055 · 5.6 `[x]` · F5.3 → T063 |
| 7 (8) | 7.0 → T051 · 7.1 → T057 · 7.1b → T057 · 7.1a → T057 · 7.2 → T057, T058 · 7.3 → T061 · F7.1 → T061 · F7.2 → T058, T063 |
| 9 (8) | 9.1 → T034–T036 · 9.2 → T040, T041, T043, T086 · 9.2a → T030, T036 · 9.3 → T042 · 9.4 → T037, T044 · 9.5 → T090 (arc close) · F9.1 → T049 · F9.2 → T049 |
| 10 (5) | 10.1 → T038 · 10.2 → T075 · 10.2a → T075 · 10.3 → T076 · F10.1 → T077 |
| 11 (3) | 11.0 → T091 · 11.1 → T092 · F11.1 → T093 (all at arc close) |
| 13 (8) | 13.1 → T072 · 13.2 → T071 · 13.3 → T071 · 13.4 → T070 · 13.4a → T073 · 13.5 → T070 · 13.6 → T070 · F13.1 → T074 |
| 16 (7) | 16.1 → T078 · 16.2 → T079 · 16.3 → T080 · 16.4 → T081, T085 · 16.5 → T082 · 16.6 → T034, T083 · F16.1 → T083 |

8 + 5 + 5 + 12 + 8 + 8 + 5 + 3 + 8 + 7 = **69**.

## Dependencies and execution order

- **Phase 0** gates everything. T004 must apply the answers a task's
  `Blocked by` line names before that task starts, and T006 must report no
  CRITICAL finding.
- **Phase 1**: lanes A–E run in parallel, subject to plan.md's single-writer
  table for `serve.py` and `cli.py`. They join at T032 and then run
  T034 → T035 → T036 → T037. openXdox-code (T040–T044) follows once openDox's
  phase-1 commit is in the openDox root (T047 step 2). openxFactory's host
  wiring (T045, T046) lands inside T047's openxFactory PR.
- **Phase 2**: T050 ∥ T052 ∥ T057 (∥ T053), then T054 → T055 → T056 → T058;
  T059 after T052 and the phase-2 root pin; T060 after T054; T061 after C3.
- **Phase 3**: Group 13 (T071 → T070 → T072 → T073 → T074) ∥ Group 16's
  binding slice (T078 → T079 → T080) ∥ T081 ∥ T084 → T085 ∥ T075 → T077; then
  T082, T083, T086 → T087 → T089.
- **Acceptance**: T095 → T096 → T097.

### Parallel slices, summarised

| phase | runs in parallel | is serialized |
|---|---|---|
| 1 | T010–T012 ∥ T015–T016 ∥ T020–T022 ∥ T025–T027 ∥ T030 ∥ T017 | `serve.py` and `cli.py` writers; T032 → T037; openXdox after the root pin |
| 2 | T050 ∥ T052 ∥ T057 (∥ T053) | T054 → T055 → T056 → T058; ratchet writers |
| 3 | Group 13 ∥ 16.1–16.3 ∥ 16.4 ∥ 4.3's end (T084–T085) ∥ T075 | `serve.py` (T073 before T084); `doxbench_binding.py` (T078 → T080) |

## Phase 1 writer slices (for the fan-out)

Each slice is one writer, one claim (T002), one PR in one repository, and one
falsifier quoted in that PR. "Opus" marks a slice that designs a seam or makes
a judgement the packet does not settle. "Sonnet" marks a slice that is fully
specified. No slice starts before T004 has applied the answers its line names.

| slice | tasks | repo | files | depends on | falsifier it must pass | size |
|---|---|---|---|---|---|---|
| P1-A route seam | T010, T011 (with T030), T012 | oDc | `src/route_extension.py`; `src/opendox/serve.py`; readers of the five lane names; new `tests/test_route_handler_contribution.py` and `tests/test_imports_standalone.py` | R1Q1, R1Q22; T006 | F2.1 (sweep and named test); the new seam tests | Opus |
| P1-B default profile | T015, T016 | oDc | `src/opendox/domain_profile.py`, `profile_proxy.py`, a new default-profile module; one-line entry calls in `cli.py`/`serve.py` (rebased on P1-A); `tests/test_profile_registration.py` and a vocabulary test | R1Q3, R1Q4, R1Q5, R1Q22; P1-A for the `serve.py` line | F3.1 (as amended per R1Q3) | Opus |
| P1-C home-corpus seam | T020 | oDc | `src/opendox/corpus_adapter.py`; `tests/test_authoring_seam.py` | none; startable today | F4.1's first block; `…::test_required_header_fields_come_from_the_registered_adapter` | Sonnet |
| P1-D authoring and the default adapter | T021, T022 | oDc | `src/opendox/authoring.py`; entry registration in `cli.py`/`serve.py`; `tests/test_authoring_seam.py` | R1Q3, R1Q22; P1-C, P1-B | `…::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has`; F4.1's first block | Sonnet |
| P1-E openxFactory reaches | T025, T026, T027 | oDc | `src/opendox/workbench.py`, `serve_wire.py`, `doxbench_packet.py`, with seam tests | R1Q9 (T025), R1Q22; P1-C (T025) | F4.1's scan without `workbench.py:746/1407-1409`, `serve_wire.py:1369` or `doxbench_packet.py:177` | Opus |
| P1-F sweep and nine-file repair | T032, T034 | oDc | the nine files in research R3 and their Node harnesses | P1-A–P1-E landed; R1Q2 (for `test_outline_model.py`) | the nine files green; F4.1's scan lists only `openxdox` targets | Opus (the `test_consumer_reach`/`test_boundary` re-pins alone would be Sonnet) |
| P1-G whole suite in CI | T035, T036, T037, T031 | oDc | `conftest.py`, `pyproject.toml` (`testpaths`), `.github/workflows/validate.yml`, `README.md`; the seven ignored modules | P1-F; R1Q2, R1Q6, R1Q8 | F9.1 (openDox-code), both assertions | Opus |
| P1-H console script | T038 | oDc | `pyproject.toml` `[project.scripts]`; the default profile's `SUBCOMMAND_EXTENSIONS` | P1-B; R1Q4, R1Q5, R1Q22 | `opendox --help` and `opendox runtime --help` exit 0 | Sonnet |
| P1-I openXdox pin and residue | T040 | oXc | `pyproject.toml` (the `opendox @` pin, `rfc3339-validator`); a local helper for the three `test_gate_routes` importers; `tests/fixtures/base-repo` | openDox root code pin at the phase-1 commit (T047 step 2) | no `test_gate_routes` collection error; `test_snapshot_validation_launch` finds its fixture | Sonnet |
| P1-J openXdox green alone | T041, T042, T043, T044 | oXc | `tests/integration/` (new, including `test_assembled_surface.py` and P1-G's relocated modules); `.github/workflows/validate.yml`; the `doc_health` declaration R1Q6 selects | P1-I, P1-G; R1Q5, R1Q6, R1Q7 | F9.1 (openXdox-code, as amended), F9.2 | Opus |
| P1-K pins and host wiring | T045, T046, T047 | oD, oX, oxF | openDox root: `code`, `contracts/code-pin.yaml`, workflow `@sha`. openXdox root: `code`, `contracts/code-pin.yaml`, `contracts/opendox-pin.yaml`. openxFactory: both pin pairs, plus `scripts/opendox_host.py`, `scripts/profile_openxfactory.py`, `tests/domain_profile/` and the parity test (R1Q2) | P1-A–P1-J; R1Q1, R1Q2, R1Q4, R1Q9 | `make pins` in both roots; `verify-opendox-pin.py`, `verify-openxdox-pin.py`; openxFactory `pytest-suite`; T093 | Opus |
| P1-L read-only checks | T017, T093 | oxF | `evidence/` only | P1-K | interim F11.1 prints `requirement 1 holds` | Sonnet |
| checkpoint | T049 | — | none (a verifier) | P1-K | F2.1, F3.1, F9.1 in both legs, F9.2, `opendox --help` | Opus (verifier) |

**Fan-out order.** P1-C can start today. After T004:

1. P1-A, P1-B, P1-E and P1-C run in parallel.
2. Then P1-D and P1-H.
3. Then P1-F and P1-G.
4. Then P1-I and P1-J, once the openDox root has its code pin.
5. Then P1-K, P1-L and T049.
