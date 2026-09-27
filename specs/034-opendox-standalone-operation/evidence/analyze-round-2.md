# Analyze, round 2 (T019, T009 and T069)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Tasks**: T019,
T009 and T069 ([`tasks.md`](../tasks.md)) · **Run**: 2026-09-27, both passes
00:18–01:17Z over `a241bb3a`, and the dispositions until 02:15Z ·
**Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## Verdict

**CRITICAL: 0.** No finding breaks a MUST of the constitution or leaves a
requirement without a task.

The analysis raised two questions that the answers do not settle, **R1Q26**
and **R1Q27** (V2-1, V2-2). Both go to Brett Heap in
[`clarify-questions.md`](../clarify-questions.md), each with a recommendation,
and neither is answered by assumption. The four tasks they reach, T059, T060,
T061 and T066, carry them as `Blocked by:` lines (FR-012), so the plan
authorizes none of the four. T067, the third round, encodes the answers, and
T007's batch I records the #1144 lines they amend. This is the plan's one
deviation from the constitution's workflow gate, which plan.md § Complexity
Tracking records, as the Governance section requires.

The verifier made its count conditional on exactly that. Had this revision
claimed a PASS without raising the two questions, it would have counted both
as CRITICAL, because V2-2 would change the enforcement of three contract rows
with no OpenSpec change (Principle II).

Phase 1 does not wait on either question, and neither do phase 2's openDox-side
slices (P2-S, P2-F, P2-G, P2-V, P2-P, P2-R and P2-D). Phase 3 starts after
T063, so it follows them through phase 2.

The author's pass found 1 HIGH, 4 MEDIUM and 7 LOW (U2-1 to U2-12). The
verifier's pass found 4 HIGH, 8 MEDIUM and 14 LOW (V2-1 to V2-26). Seven
defects were found by both, so the tables below hold 31 rows: 5 HIGH, 10
MEDIUM and 16 LOW. The author found one more, U2-13 (MEDIUM), while carrying
V2-1. Every finding is dispositioned below. Two raise the new questions, and
the rest change this revision.

## How it was run

**What was analyzed.** Brett Heap answered the fourteen open questions, and
RN-1, on `#656`, comment `5850003126` (2026-09-26T21:23:03Z), verbatim: *"go
with recommendations on all the open questions"*. Commit `a241bb3a`, on
`main` at `79a720a2`, encodes the answers:
- T019 applies R1Q14, R1Q24 and R1Q25 to phase 1's openXdox-code tail;
- T009 applies R1Q10–R1Q13 and R1Q23 to phase 2;
- T069 applies R1Q15–R1Q19 to phase 3, and records R1Q21.

The analysis read `spec.md`, `plan.md` and `tasks.md` at that commit. It used
`clarify-questions.md`, `quickstart.md`, `research.md`, the checklist and the
round-1a record as context. The authority is #1144 at `79a720a2`, which
carries batch D (#1170). The constitution is `.specify/memory/constitution.md`,
version 1.0.0.

**One record for three tasks.** Round 1a's D2 had T009, T019 and T069 each
write `evidence/analyze-<task>.md`. The three ran as one round, over one
revision, on one ruling, so they share this record (V2-24). The round-1a
record is left as it was.

**The feature context.** The check was run in the lane's clone. `<clone>`
stands for the clone's root. `.specify/feature.json` already held the value,
and it is gitignored (`.gitignore:17`):

    $ bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
    {"FEATURE_DIR":"<clone>/specs/034-opendox-standalone-operation","AVAILABLE_DOCS":["research.md","quickstart.md","tasks.md"]}
    (exit 0)

The optional `before_analyze` and `after_analyze` hooks, which offer an
automatic git commit, were not run. This feature commits by hand, with
pathspecs.

**Two passes.** The author ran `/speckit-analyze`. An independent Opus
verifier ran it again, read-only, over a separate clone of `a241bb3a`, with
#1144 at `79a720a2` and the measurement trees at openDox-code `1e4a57fb` and
openXdox-code `e28930bf`. It also re-ran the plan-consistency tools, twice,
with byte-identical output. The two sets of findings are merged below. The
verifier's are `V2-1` onwards, and the author's are `U2-1` onwards. Where both
passes found the same defect, the row names both.

**The dispositions** are in commit `488c7d31`. `main` then moved to
`b060d400` (#1174, an archive whose one README edit is in the OpenSpec Records
block, away from this feature's entry), and the branch merged it cleanly.
While carrying V2-1, the author checked the dispositions against both passes
and found U2-13, which the commit that adds this note carries. The checks at
the end of this note were run on that commit.

**Measurements made for the analysis.** Each was run in a scratch clone or
read from a measurement tree, and none touches a shared tree.
- **The facet simulation (V2-1).** The verifier imported the trees' sources
  with bytecode writing off, and changed only `SNAPSHOT_VALUES` in memory. At
  openXdox-code `e28930bf`, `view_extensions.DISPLAY` has the keys
  `['stages']`. With T060's `values` block it has `['stages', 'values']`, so
  it no longer equals a stages-only dict. At the old pin the facet changes five
  leaves of the served display (`host_facet` and four `stages.completion.*`
  fields). At the new pin, with neutral defaults, it changes eleven: the five
  and six `values.*` leaves. Without the block it changes the five. `git status
  --porcelain --ignored` on both trees was the same before and after.
- **12.5's computed set.** At `e28930bf`, `git grep -l -e 'open-pr' -e
  'open_pr' -e 'FakePullRequests' -- 'tests/test_*.py'` lists 16 files, and
  `tests/test_gate_loop_views.py` is one of them (it drives `open-pr` at
  `:672`). No task, plan, research or re-measure line named it before.
- **openxFactory's facet composition.** `scripts/profile_openxfactory.py:218`:
  *"ONLY `stages` IS COMPOSED"*. `tests/test_engineering_profile_display_facet.py`
  asserts `"values" not in facet` (`:272`) and `set(view_extensions.DISPLAY) ==
  {"stages"}` (`:566`).
- **What names the consumer's validator in openxFactory.**
  `contracts/manifest.yaml` calls it *"still this family's conformance
  validator"*, and three RETAINED rows name it in their `consumption_rule`.
  `ideation-possibles-register` and `gate-intent` say their rules are
  *"enforced by scripts/validate-ideation-dashboard-contracts.py"*, and
  `demotion-execution-receipt` says that consumers *"run"* it.
  `scripts/validate-ideation-cross-reference.py` delegates the register's
  transitions to it (`:77`, `:449`), and `contracts/README.md:138` documents
  its `--transition OLD NEW`. The script reads *"this tree's own
  `contracts/`"* first (`validate-ideation-dashboard-contracts.py:119-121`, at
  `e28930bf`).
- **F5.3 before T055 (V2-4).** openDox-code `1e4a57fb`, `cli.py:90`:
  `generate_snapshot = consumer_reach.generate_snapshot`, called at `:217`.
  `consumer_reach.py:435`: `generate_snapshot = function(generator,
  "generate_snapshot")`, the consumer's generator.
- **The consumer gate's floors (V2-25).**
  `.github/workflows/openxdox-consumer-gate.yml` holds `MIN_PASSED: "1137"`
  (`:505`) and `EXPECT_SKIPPED: "0"` (`:532`) for its consumer suite,
  `pytest tests/ideation-dashboard -m "not postgres"`.
- **`collect_ignore` and a named file.** Re-probed with pytest 9.1.1: a file
  that the root conftest's `collect_ignore` lists still runs when named by
  node id (`1 passed`), as pytest 8.4.2 did for T006.

## Findings, and what this revision does with each

Severity follows the skill: CRITICAL breaks a constitution MUST or leaves a
requirement uncovered. HIGH is a conflict with the authority, or an acceptance
criterion that cannot be tested. MEDIUM is drift, a missing step or an
underspecified case. LOW is wording.

### HIGH

| ID | finding | disposition |
|---|---|---|
| V2-1 | T060 adds a `values` block to openXdox's `DISPLAY` facet (R1Q11 (a)). `tests/test_gate_loop_views.py`, one of the 16 suites 12.5's falsifier computes, pins that facet. `test_the_display_facet_declares_one_stage_entry_and_nothing_else` asserts `DISPLAY == {"stages": …}`, so it goes red at T060's landing. `test_the_overlay_changes_four_words_and_the_named_absence_and_nothing_else` asserts exactly five changed leaves, so it goes red at T059's pin, where the defaults are neutral. Editing the file in an `Arc:` landing fails 12.5's falsifier. R1Q7 (a)'s allow-list admits only respellings, and batch F admits only F7.1's two F5.2 edits. The plan never named the file. | **Put to Brett as R1Q26**, on T043's own rule that a protected suite red for a cause no answer takes goes to him as a question. Recommended (a): batch I amends 12.5's falsifier to admit the two edits, each with its reason, as batch F does for F7.1. T060 names both tests, and T060 and T059 carry `Blocked by: R1Q26` and follow T067. spec.md, plan.md and the checklist say what the question holds. |
| V2-2 | 7.3 narrows the consumer's validator from the family's ten schemas to its three (T061). Four of the ten are openxFactory's own, and openxFactory's contracts name this script as their validator: three RETAINED manifest rows, the cross-reference validator's hand-off and the contracts README. T061's *"as 7.1b requires"* misread 7.1b, which is about what openDox needs, and its line that every kind given up *"already has a validator of its own"* was false for these four. No test would catch it, and three contract rules would become untrue with no OpenSpec change. | **Put to Brett as R1Q27.** Recommended (a): the validator checks its own three from its installed distribution everywhere, and the other kinds only where the tree it runs from supplies their schemas, so no contract row changes. T061 and T066 carry `Blocked by: R1Q27` and follow T067. The misreading is struck, and T061 says openxFactory's four kinds have no other validator. |
| V2-3 | Batch H amends F10.1 to a `.[local]` install and `generate-and-open --local`. T075 quoted "F10.1's fetch" but waited only on T056, T038, T063 and T069, and ran in G1 beside P3-I, so it could land before T070 (`--local`) and T072 (the extra). T056 quoted "F10.1's generate half", though `--local` does not exist until T070. Neither could be tested at its own landing. | T075 follows T072 and batch H, and its falsifier is F10.1's fetch as batch H amends it. P3-E moves to G2, after P3-I, in the slice table and in plan.md's graph (T072 → T075 → T077). T056 runs F10.1's `generate-and-open` with a plain install and no `--local`, and leaves F10.1 as amended to T077. |
| V2-4 | T054's falsifier was F5.3, which runs `python -m opendox.cli generate`. Until T055 the generate verb reaches the consumer's generator (`cli.py:90`), and T054 edits no `cli.py`. | T054's falsifier is an in-process test: its projection over T050's fixture, with neither sibling importable, validates against T053's schema and carries none of F5.3's words. F5.3 is quoted at T056 and T063, as the box accounting already had it. |
| U2-1, V2-6 | The refusal of a `--local` flag and an `OPENDOX_INSTALL_MODE` setting that disagree appeared in no option or recommendation, yet batch H's 13.4 row recorded it as Brett's amendment, and R1Q15's answer line narrated it as his. The verifier rated this MEDIUM and the author HIGH. It is kept HIGH, as a conflict with the authority: a ruled amendment would have carried a rule the ruling does not. | Batch H's 13.4 row carries the answer alone: `--local` selects the local mode as the setting does, and with neither the install is hosted. T070 keeps the refusal as the plan's fail-closed reading (Principle VII), with a test of its own, and says that no answer rules it. spec.md's edge case and R1Q15's answer line say the same. § "Lines the answers imply" records it for Brett. |

### MEDIUM

| ID | finding | disposition |
|---|---|---|
| V2-5 | openxFactory composes only openXdox's `stages`, and its facet test asserts that no `values` section exists. At T064's pins, openxFactory's served views would match neutral values against the governed snapshot. So T064's *"none is expected"* and T059's *"governed views keep matching"* were false for openxFactory. Neither file is an 11.1 surface. | Folded into R1Q26. Under its option (a), T066 composes the `values` block into openxFactory's profile and updates the facet test, in its both-pins form. P2-H lists both files. T059 and T064 say that openxFactory's views match only through T066. |
| V2-7, U2-3 | Nothing defined "groups derive from shared topics" for a document with no front matter, yet AT-R1's repository (b) has none and must yield a grouping tile. The author also found no rule for a `stage:` value outside the six role keys. | T054 names the topic rule and tests it over a copy of repository (b), which must yield at least one group. A `stage:` value outside the six is not a declaration: the generate verb reports it, naming the document, and reads the document as a source, and the closed schema admits only the six. spec.md gains the edge case, and T054's falsifier both tests. |
| V2-8 | T061 kept three answers of the lookup, but openxFactory's farm and the refresh lane's seal rely on a fourth: a tree's own `contracts/schemas/` is read first. | Folded into R1Q27, whose option (a) keeps it. T061 names the fourth answer and says that R1Q27 decides it. |
| V2-9 | `evidence/analyze-round-2.md` did not exist, while twelve places cited it and the README linked it. | This note is that file, in the same PR. Its verdict agrees with the cited lines: nothing CRITICAL, and R1Q26 and R1Q27 raised. |
| V2-10 | `tests/test_validate_ideation_dashboard_contracts.py` imports in a lone checkout, but its `ROOT` is `parents[2]`, above the checkout, left from the carve. A new test that reused its paths would fail, or adopt an enclosing tree, which is the class of defect 7.3 closes. | T061's new test resolves the validator and its schemas through the installed distribution, never through the module's paths, and T061 records the `ROOT` note. |
| V2-11 | T057's falsifier, "F7.2's schema half", marked off no part of F7.2, which runs the generate verbs. | T057's falsifier is the packaged-copy digest test and the 7.1b test. F7.2 stays with T058 and T063. |
| V2-12 | `find_openxfactory_validator` returns one script path, which callers run for openDox's kinds and for the consumer's. T066 said it sends each kind to its own validator but gave no mechanism, and openDox-code has no `scripts/` (7.2). | T066 names the choice: a script that dispatches by kind, or a second finder with its callers moved. T067's re-plan of T066 makes it, and says which of openDox's validators is on disk at T064's pins. |
| U2-2 | T008 was to inherit T061's list of excluded files that validate a kind the narrowed validator gives up, but T008 runs at the start of phase 1 and T061 in phase 2. | T061's PR body lists the files. The holder then adds the list to the direction arc's record, as bookkeeping. |
| U2-11 | Batch F extends lines that other batches add first: F5.2's allow-list is batch C's, and F9.1's exclusion is batch B's. The order of the three batches was unsaid. | Each batch-F line names what it extends by the ruling behind it, R1Q7 (a) or R1Q6 (d), so it reads the same whichever batch lands first. Of two batches that amend one line, the later rebases onto the earlier. |
| U2-12 | T058 writes the generate verbs' post-render validator into `cli.py`, but `cli.py`'s single-writer order left it out. | The order is T016 → T022 → T038 → T055 → T058 → T070 → T084, in plan.md's table and in the persisted chain checks. T058 already followed T055, through T056. |
| U2-13 | The author, while carrying V2-1: batch G carried 5.3a's `values` block as a ruled amendment, and batches A–H were said not to wait on R1Q26. Under R1Q26 (b), 5.3a is not amended, so batch G could have landed a line that the answer undoes. The checkpoint T063 also quoted F7.1, which R1Q27 may re-read, without following batch I. | 5.3a's `values` block moves to batch I, which records it under R1Q26's answer. Batch G keeps 5.3, 7.0, 7.1, 9.5, 4.3 and F5.2's environment line, which neither question touches. T063 follows batch I and quotes F7.1 as batch I reads it, and SC-002 says so. R1Q26's options say what each does to 5.3a. |

### LOW

| ID | finding | disposition |
|---|---|---|
| V2-13, U2-6 | T038's *"as F10.1 installs, so no extra is present"* was stale once batch H amends F10.1. | T038 keeps its plain `pip install .`, and says it does so after batch H too. |
| V2-14 | research.md said R1Q25 *"puts"* the move to Brett. | It says he answered (b), and that T061 is back in phase 2. |
| V2-15, U2-9 | The checklist said SC-001 *"needs RN-1 ruled"*, cited only phase 1's slice table, and read *"Every finding either raised"*. The README's link text named only the phase-1 writer slices. | The checklist cites requirement 3 as #1170 amended it, each phase's slice table, and *"either run"*. The link text reads *"with each phase's writer slices"*, and the entry says that four phase-2 tasks wait on R1Q26 and R1Q27. |
| V2-16, U2-4 | *"RN-1 holds phase 1's close"* was present tense in spec.md, in R1Q3's answer line and in P1-B's row, though RN-1 is ruled and landed (#1170 → `79a720a2`). | Past tense in the first two. P1-B's row drops the clause. |
| V2-17, U2-5 | Batch G's bullet and plan.md's R1Q11 and R1Q12 rows left out 7.0, which batch G's table row amends. | Added to the bullet, both rows and R1Q12's answer line. |
| V2-18 | T091's repository tags left out openDox-spec. | `[oDs]` is added. |
| V2-19 | § Dependencies had T053 first and then T050, though T050 follows only T049 and T009. | *"T053 and T050 first, in parallel"*, and T051 after both. |
| V2-20 | T059's partial F5.2 named neither the two deselected cases nor the run form, and F5.2's loop stops at the first red file under `set -e`. | T059 names both node ids in the `--deselect` form, and says every other suite runs whole. |
| V2-21 | *"names no broker"* did not say whether `broker_argv` becomes optional or forbidden. It is required today. | T080: a record whose reference the built-in resolver takes does not need `broker_argv`, one given beside such a reference is refused, and a test holds both. Batch H's 16.3 row and R1Q17's answer line now read *"needs no broker"*. The refusal is the plan's reading (§ "Lines the answers imply"). |
| V2-22 | spec.md's *"seven such files … Each joins"* read as a fixed list, but R1Q24 (a) was ruled by class. | *"the files of those two classes at T040's pin"*, with seven at `e28930bf` and T005's eighth. |
| V2-23, U2-7 | plan.md's single-writer table left out `doxbench_binding.py` (T078 → T079 → T080), and § Dependencies' list of single-writer files left out `tests/test_consumer_reach.py`. | Both are added. |
| V2-24 | Round 1a's D2 had each round task write its own record, and one record now serves the three. | Noted in § How it was run. The round-1a record is unedited. |
| V2-25 | T066's check at the candidate pins named only `pytest-suite`, which passes on skips, while the consumer gate requires `MIN_PASSED` 1137 and `EXPECT_SKIPPED` 0. | T066 and T064 also run the consumer gate's suite at its floors. |
| V2-26 | *"If no earlier task has created that file"* pointed at `tests/test_snapshot_validator_home.py`, which exists, where it meant the allow-list. | *"… created the reviewed allow-list"*. |
| U2-8 | Batch B's 9.2 row reported the exclusion with *"its reason"*, but its entries carry reasons of their own, and R1Q24 (a) adds more. | *"each entry's reason"*. |
| U2-10 | Several replacements joined lines past the file's width, in § What can start, T038, T061, § Dependencies and the quickstart. | Reflowed. |

## Lines the answers imply

Four lines of the encoding are not an option's own words. Each was checked
against the ruling and the plan's rules, and each follows from what Brett
answered, so none goes back to him. The verifier checked the same four and
found each lawful.

- **F10.1 installs `.[local]` (T069, batch H).** R1Q16 (iii) makes the
  standalone install `pip install "opendox[local]"`, and its sub-question
  names F13.1 as the line amended. #1144's F13.1 says of its own install
  *"the install is group 10's, unchanged — one entry point, one command"*, so
  F10.1 and F13.1 share one install line. F10.1 also passes `--local` (R1Q15
  (b)), and the local mode starts the bundled server, which arrives only with
  the extra (R1Q16 (i), (iii)). Both routes give F10.1 `.[local]`.
- **T059 passes F5.2 less `tests/test_snapshot.py`'s two schema cases, and
  T061 passes it whole.** Under R1Q25 (b) the two cases pass only once 7.3
  lands (T061). The plan's rule since round 1a is that a falsifier moves to the
  task that makes it reachable (C7, U1). F5.2 still runs whole in phase 2, at
  T061 and at the checkpoint T063, so 5.4a closes where the map puts it.
- **T066 is a non-arc openxFactory act.** R1Q14's T006 paragraph, which the
  answered recommendation carried, listed three lawful routes and said T019
  records which the answer takes. T019 took the first and the third. F3's
  overlays are the precedent R1Q20 names for a non-arc act.
- **5.3a admits a `values` block on openXdox's facet.** R1Q11 (a)'s option
  says that openXdox's *"facet maps roles to governed values"*, and it names
  5.3 as the cost. 5.3a's *"and NOTHING ELSE"* needs the addendum, and F5.1
  reads only the facet's stages, so it is unchanged. How the block lands past
  12.5's protected suite is R1Q26, so batch I records it (U2-13).

Two more lines are the plan's own, and **no answer rules them**. Both fail
closed (Principle VII). They are recorded here so that Brett can overrule
either, and batch H writes neither into #1144.
- **T070 refuses a `--local` flag and an `OPENDOX_INSTALL_MODE` setting that
  disagree**, naming both, so no explicit selection is silently overridden
  (U2-1, V2-6). No task before T070 depends on it.
- **T080 refuses a `broker_argv` given beside a reference that the built-in
  resolver takes**, so each record has one resolver (V2-21). That such a record
  needs no broker does follow from R1Q17 (b), since `broker_argv` is required
  today and the built-in resolver would otherwise be unusable.

## The measured claims

The commit added six measured claims, and the verifier checked each against
the trees.
- **(a)** openXdox-code's `tests/test_validate_ideation_dashboard_contracts.py`
  only computes paths at module level, so it imports in a lone checkout.
  **Holds**: a docstring, 8 imports, 9 path or literal assignments and 22
  function definitions, with no I/O. Its paths are the carve's (V2-10).
- **(b)** openxFactory's `delegated_semantic_validation` and
  `find_openxfactory_validator` compose the consumer's shed script with
  schemas. **Holds**: `conftest._shed_validator` is `carved_source(...)`
  followed by `_composed_validator(moved)`, and
  `delegated_semantic_validation` calls `_composed_validator(checkout /
  VALIDATOR_IN_CHECKOUT)`. The farm is built at `doxbench_contracts.py:521-530`.
- **(c)** `test_the_confined_locator_never_adopts_the_sealed_validator` asserts
  `find_validator(start) is None` for starts in the seal. **Holds**, at
  `test_dashboard_source_seal.py:502` and `:520-521`.
- **(d)** None of openxFactory's four kinds is among what its callers of this
  validator validate. **Holds for the code callers**, which validate
  snapshots, gate records, workbench manifests and doxBench kinds. The
  contract rows that name the validator are V2-2.
- **(e)** openXdox-code's `test_aggregation_register_instance.py` skips in a
  lone checkout. **Holds**: the recorded runs show 4 of 4 skipped, *"aggregation
  checkout (seed register + pinned validator) not reachable"*.
- **(f)** `display_profile.py`'s `SNAPSHOT_VALUES` and its facet `values`
  override exist as described. **Holds**, at openDox-code
  `display_profile.py:227-233` and `:588-608`.

## Coverage

| key | tasks | note |
|---|---|---|
| FR-001 | T010, T011, T030, T031, T032, T036, T049 | |
| FR-002 | T001, T015, T016, T017, T049 | requirement 3 as #1170 amended it |
| FR-003 | T012, T020–T022, T025–T027, T046, T055, T084–T086, T089 | |
| FR-004 | T050, T052–T056, T059, T060, T063 | T059 and T060 wait on R1Q26 |
| FR-005 | T051, T053, T057, T058, T061, T063 | T061 waits on R1Q27; T066 keeps openxFactory's callers working at T064's pins |
| FR-006 | T034–T037, T040–T044, T049, T061, T086, T090 | T061 clears `tests/test_snapshot.py`'s entry |
| FR-007 | T038, T075–T077 | |
| FR-008 | T070–T074 | |
| FR-009 | T034, T078–T083, T085 | |
| FR-010 | T017, T018, T045, T065, T091–T093, T098 | |
| FR-011 | T095, T096 (T088 is its precondition) | |
| FR-012 | T002, T009, T019, T067, T069, and every `Blocked by:` line | T059, T060, T061, T066, T067 and T007's batch I carry R1Q26 or R1Q27 |
| SC-001–SC-007 | T049, T063, T089, T095 and T096, T018, T065 and T098, T097, T047, T064, T066 and T094 | |

All 69 release-1 boxes map to a task. `box_census.py` over #1144's `tasks.md`
at `b060d400` still prints `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`.

**Unmapped tasks.** T002–T009, T019, T048, T067 and T069 map to no box. They
are the holder's and the process tasks, by design. T018, T065, T066, T088 and
T095–T098 map to no box either, and each maps to an FR or an SC above.

## Constitution alignment

No finding breaks a MUST at this revision.
- **I–VII.** No committed host-absolute path, and no credential. This record
  is linked from the README entry (IV). The PR adds no `openspec/` path.
  `openspec validate --all --strict` gives `110 passed, 1 failed (111 items)`,
  and the enforced gate, `scripts/validate-openspec-cli-pin.py --all`, exits 0
  with the one accepted exception, `add-chain-attestation` (V). R1Q11 (a)'s
  `dox-v1.x` bundle is cut under the openDox root's own rule, after batch G's
  9.5 addendum (VI). The two plan readings fail closed (VII).
- **Principle II.** V2-2 would have changed what three contract rows enforce
  with no OpenSpec change. It is a question now, and T061 cannot land before
  it is answered. R1Q27's option (b), the only one that moves the rows, names
  its own OpenSpec change.
- **The workflow gate.** *"Material ambiguities MUST be resolved before
  planning"* holds for phase 1, phase 3 and every other task of phase 2. T059,
  T060, T061 and T066 are planned while R1Q26 and R1Q27 are open, and they
  authorize no implementation. That is the deviation plan.md § Complexity
  Tracking justifies, as the Governance section requires. It is round 1a's
  deviation in a narrower form: then phases 2–3, T061 and T043 waited.
- **Complexity Tracking** gains two rows: the four held tasks, and T066, a
  non-arc act inside the arc's sequence, each with its reason and the
  rejected alternatives.

## Metrics

| metric | value |
|---|---|
| requirements | 19 (12 FR, 7 SC) |
| tasks | 90, T001–T098 with eight ids unused (T013, T014, T023, T024, T028, T029, T033, T068); eight done (T001, T003–T006, T009, T019, T069) |
| coverage | 19 of 19 |
| questions | 27: 25 answered (11 on `5817152735`, 14 on `5850003126`), and R1Q26 and R1Q27 open; RN-1 ruled (a) and landed |
| held tasks | T059, T060, T061 and T066, with T067 and T007's batch I |
| findings, author's pass | CRITICAL 0, HIGH 1, MEDIUM 4, LOW 7 (U2-1 to U2-12) |
| findings, verifier's pass | CRITICAL 0, HIGH 4, MEDIUM 8, LOW 14 (V2-1 to V2-26) |
| findings, merged | 31 rows: HIGH 5, MEDIUM 10, LOW 16 |
| findings, the author while carrying them | MEDIUM 1 (U2-13) |
| new questions for Brett | 2 (R1Q26, R1Q27), each recommended (a) |

## The checks after the dispositions

Run from `specs/034-opendox-standalone-operation/` with the persisted tools,
which read each of T007's nine batches as a node of its own:

| check | result |
|---|---|
| `qcheck.py` over `qmap.py` (R1Q1–R1Q27) | `headers checked: 27 of 27; mismatches: 0` |
| `depcheck.py` | `tasks: 90 nodes: 99 (T007's batches are nodes: T007.A, …, T007.I) edges: 216`; `cycles: none`; and `none` with the Lands-with groups `[T011, T030]`, `[T031, T036]` and `[T045, T046, T047]` merged |
| `arrowcheck.py` | `arrow mismatches: 0`, `arrows checked: 69` |
| `phasecover.py` | every task before its phase's checkpoint (phase 1: 32 tasks, phase 2: 17, phase 3: 23); T048 after T049, by design; T095–T097 follow T076 and T089 |
| `chaincheck.py` | `single-writer chain gaps: 0` |
| `chaindirect.py` | 27 pairs DIRECT and 12 transitive, each through a printed path, among them `cli.py`'s T055 → T058 through T056 |
| `sharedfiles.py` | the coarse check's 4 known NOT ORDERED pairs, all in phase 1 (`serve.py` and `cli.py` among P1-A, P1-B and P1-D; `pyproject.toml` between P1-H and P1-G), each ordered by a single-writer chain |

The added lines of the PR hold no host-absolute path and no closing keyword.

## The phase-1 tail (T019)

T019's part of phase 1 is openXdox-code's tail, T040 → T041 → T042 → T043 →
T044, with T047 and the checkpoint T049 after it. Re-analyzed on its own:
- **No new question reaches it.** R1Q26 and R1Q27 hold only phase-2 tasks.
- **R1Q24 (a) is by class.** T043's triage at T040's pin enters each file that
  reaches openxFactory's status-exemption rail or its contracts, each with its
  own reason (V2-22). T041 admits the four reasons, and batch F admits the
  last three in F9.1 and 9.2 (U2-8).
- **R1Q25 (b).** T043 declares `tests/test_snapshot.py` in the exclusion, with
  its own reason, and T061 clears the entry in phase 2.
- **The batches.** T043 follows batches C and F, and T049 follows A, B, D and
  F. Batch F reads the same whichever of B and C lands first (U2-11).
- **T008** records the rail and contracts classes now. T061's list of the
  excluded files that validate a kind the narrowed validator gives up reaches
  the arc's record in phase 2, through the holder (U2-2).

Nothing in the tail is held, and the tail's checks above are clean.

## Next

- **Brett Heap** is asked R1Q26 and R1Q27. T067 then encodes the answers,
  re-plans T059, T060, T061, T064 and T066, and records its analyze in
  `evidence/analyze-round-3.md`.
- **T007's batches F, G and H** land next, each its own bookkeeping PR under a
  Rule 6 window, before the tasks their `After:` lines name. Batch F is due
  before T043. Batch I follows T067.
- **G1** (P1-A, P1-B, P1-C and P1-E) is in flight. No answer of round 2 and
  neither new question changes it.
