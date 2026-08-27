# Tasks: The modified-block-currency self-gate

**Input**: Design documents from `/specs/021-modified-block-currency-self-gate/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/self-gate-contract.md`, `quickstart.md`

**Packet**: `openspec/changes/add-modified-block-currency-check/tasks.md` § 4
(4.1–4.5). This file **references** those boxes; it does not restate them
(Constitution II).

**Tests are the deliverable.** FR-020 requires every test to have been shown
failing first, and `contracts/self-gate-contract.md` carries the RED form for
each. Every `[TEST]` task below names its test functions — "add tests" is how a
test file ends up asserting that a module imports.

## Progress

**ALL 31 TASKS DONE (T001–T030, T024a).** One test module,
`tests/doc-health/test_modified_block_currency_self_gate.py`, 15 tests. The
suite moved 1115 → 1130; `openspec validate --all --strict` reads 76; the report
moves +1 `warning` / +9 `info` in three sections and nowhere else. Six mutants,
all killed. Numbers, commands and RED output in `evidence/self-gate.md`.

**Two tests went RED on their own first run**, both on the same mistake in
opposite directions — matching a probe on a MENTION rather than a USE — and both
are recorded as evidence rather than quietly fixed (`evidence/self-gate.md`
§ 5, N1 and N2). One of them was the positive control on the zero-class probes
doing exactly its job.

**The mutation round's finding**: this machine carries FIFTEEN other measurable
openxFactory checkouts, so "point the resolver at another checkout" is not a
hypothetical mutant. Pointed at the shared submodule tree — the exact tree
`harden-ideation-readiness-check`'s ancestor walk always landed on — the gate is
killed by FOUR independent tests, and that tree is a genuinely different corpus:
two warnings, five ledger subjects this branch does not have, and
`add-family-enumeration-check` still ACTIVE in it.

---

## Phase 1: Setup

- [x] T001 Record the baseline: `python3 -m pytest tests/doc-health -q` and
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, both green, both
      counts written into `specs/021-modified-block-currency-self-gate/evidence/self-gate.md`
      against the head SHA. **Measured before any test exists**, so the added
      tests are visible as a delta (SC-006) and so a pre-existing red cannot be
      attributed to this feature.
- [x] T002 Create `tests/doc-health/test_modified_block_currency_self_gate.py`
      with the module docstring only: what the file measures, that its subjects
      are dated to `76a2ad27`, the packet's STALE § 4.1 figure (1 warning / 11
      info at `9be81a40` over 23 blocks) named as **history**, the re-measured
      figure (+1 / +9 over 22 blocks) as the live claim, and a pointer to
      `plan.md` § THE FIGURES as the single home for both. No test functions
      yet. *The docstring is where D1's reconciliation becomes readable to
      someone who finds the file without the feature directory.*

**Checkpoint**: the baseline is recorded and the file exists with no assertions.

---

## Phase 2: Foundational — the resolver, and the two helpers everything routes through

**BLOCKING.** Every corpus assertion reads the root this phase resolves, so a
resolver that lands on the wrong tree makes every later green meaningless. This
is the defect `harden-ideation-readiness-check` fixed and the one this gate must
not reintroduce.

- [x] T003 Add `_repo_under_test(under_test=None)` to the new module: resolve
      `Path(under_test or Path(__file__).resolve().parents[2])`, require
      `<root>/openspec/changes` to be a directory AND
      `<root>/openspec/specs/doc-health/spec.md` to be a file, and on failure
      raise with a message naming BOTH markers and the path searched. **No
      ancestor walk, in either direction** — mirror
      `test_ideation_readiness.py::_openxfactory_root`'s FIRST RUNG and its
      failure mode only, per decision D4. Do not import that function (R3: three
      copies already exist deliberately, its marker is the wrong one for this
      family).
- [x] T004 Add `_ctx(root)` returning the two-attribute stand-in
      (`repo_paths={"openxFactory": root}`, `agg_root=None`), on
      `test_family_enumeration.py:165-170`'s pattern, with a docstring recording
      the MEASURED reason it is faithful (`ctx.repo_paths` is the module's only
      `ctx.` access; `load_dispositions` reads `agg_root` and nothing else) and
      pointing at T024's structural pin.
- [x] T005 Add `_moved(subject, detail)` — the shared failure-message helper
      (FR-016). Every corpus assertion's message goes through it, and it names:
      the resolved root, the subject, that **corpus movement is the expected
      cause**, the re-measure command
      (`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`),
      and the zero end-state instruction.
- [x] T006 [TEST] `test_the_repository_under_test_is_the_tree_this_test_file_lives_in` —
      the resolved root equals `Path(__file__).resolve().parents[2]`, both markers
      are present, and `git rev-parse --show-toplevel` at that root equals the
      root itself. **RED**: assert it equals `root.parent` (the worktrees
      container) and watch it fail naming both paths.
- [x] T007 [TEST] `test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up` —
      `_repo_under_test(root.parent)` raises, with both markers and the searched
      path in the message; and if an ancestor carrying `xFactories/` is reachable,
      it is refused too rather than resolved. **RED**: wrap the GOOD root in
      `pytest.raises` and watch it fail. **KEEP THIS TEST** — it is the permanent
      assertion that there is no ancestor walk; a gate that only proves the right
      tree resolves cannot tell a correct resolver from a lucky one.

**Checkpoint**: the tree under test is proven, and pointing the gate anywhere
else fails.

---

## Phase 3: User Story 2 — the gate cannot pass on an empty read (Priority: P1)

**Goal**: no assertion in this feature can be satisfied by a family that
discovered nothing.

**Independent test**: the floor is asserted in its own test mentioning no
severity, no change id and no requirement title — so removing every named-subject
assertion leaves it still failing on a vacuous read.

**Ordered before US1 despite equal priority**: US1's non-vacuity claim rests on
this floor. Building US1 first would mean asserting named subjects with nothing
proving discovery ran.

- [x] T008 [TEST] [US2] `test_the_family_examined_at_least_one_modified_block_over_the_real_tree` —
      `len(mbc.active_blocks(root)) >= 1`, with the root, `mbc.DELTA_GLOB`, and
      the distinct change and capability counts in the failure message. **A
      FLOOR, NOT A COUNT**, and the reason is F1's own scar: pinning the exact
      population "broke the moment `add-family-enumeration-check` archived",
      making an unrelated archive look like this family's regression. **RED**:
      assert `>= 10_000` and watch it fail with the real population.
- [x] T009 [TEST] [US2] `test_the_family_returns_findings_and_not_a_skip_over_a_tree_that_carries_changes` —
      the return value is a `list`, not a `Skip`, asserted APART from whether it
      is empty. Canon's skip rule is "cannot run", not "found nothing", and the
      two states are different by the family's own delta. **RED**: assert
      `isinstance(out, Skip)`.

**Checkpoint**: a broken read fails the gate, saying discovery found nothing
rather than that a count moved.

---

## Phase 4: User Story 1 — the corpus verdict is a named claim (Priority: P1)

**Goal**: every row the family draws over this checkout is named in a test.

**Independent test**: delete any one name from the expected set and the test
fails naming it; add a fabricated one and it fails naming the absence.

- [x] T010 [US1] Add the subject constants at module level: `_SCENARIO_SUBJECT`
      (the 4-tuple: change `add-composed-view-authoring`, capability
      `ideation-dashboard`, requirement `Composed views are read-only with a
      repository jump`, omitted scenario `Gate verbs hide on a composed view`)
      and `_LEDGER_SUBJECTS` (the nine `(change, capability, requirement)`
      triples from `plan.md` § The named subjects). One comment above them dating
      them to `76a2ad27` and pointing at `quickstart.md` § WHEN THE GATE FAILS.
- [x] T011 [US1] Add `_subject(finding)` — derive `(change, capability)` from
      `finding.path` on `mbc.DELTA_GLOB`'s shape and the requirement title from
      the family's own quoting in `finding.rule`. **Read what the family wrote;
      do not re-parse the spec** — a second parser in the gate would prove
      something about the gate.
- [x] T012 [TEST] [US1] `test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else` —
      exactly one `warning` in the run, and its subject is `_SCENARIO_SUBJECT` in
      all four fields, the omitted scenario title matched EXACTLY. **RED**: assert
      the omitted title is the rename DESTINATION
      `Tile-bound gate verbs hide on a composed view` and watch it fail — which
      also demonstrates that a containment reading would have passed, the
      family's own forbidden-containment rule applied to its own gate.
- [x] T013 [TEST] [US1] `test_every_carriage_ledger_finding_over_the_real_tree_is_named` —
      the set of `info` subjects equals `_LEDGER_SUBJECTS` exactly (`==`, never
      `<=`: a subset comparison would let a newly lossy MODIFIED block land
      unreported, which is the defect the family exists to catch). Failure message
      through `_moved`, naming the symmetric difference in both directions.
      **RED, BOTH DIRECTIONS**: drop one triple (fails naming an unexpected
      finding), then add a fabricated triple (fails naming a missing one).
- [x] T014 [TEST] [US1] `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` —
      three named classes each empty, identified by rule text: the unresolved
      arm (`resolves to no promoted requirement`), the ordering arm (`the
      ordering of MODIFIED blocks for`), the marker-defect class
      (`mbc._MARKER_ACTION`). **PLUS A POSITIVE CONTROL**: assert each probe
      string actually occurs in `inspect.getsource(mbc)`, so a typo'd probe fails
      on the probe rather than reading zero vacuously — F1's mutation round
      caught exactly this shape ("the `FAMILY_RESOLUTION` absence was documented
      in three places and asserted in none"). **RED**: assert one class has one
      finding.

**Checkpoint**: § 4.1 is discharged, by named subject, with no bare count.

---

## Phase 5: User Story 3 — the family reads its own packet, against canon (Priority: P1)

**Goal**: § 4.1 cannot pass because discovery quietly stopped at the packet's own
delta, and the basis the block is measured against is named rather than assumed.

**Independent test**: the own-delta path is in the discovered set; its resolved
basis is canon; the self-finding quotes both stale numeral sentences.

- [x] T015 [TEST] [US3] `test_this_change_s_own_delta_is_among_the_blocks_the_family_examined` —
      `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`
      is among `active_blocks(root)`, carrying the title
      `Deterministic check families`. This is the assertion **F1's T057 claimed
      to have written and did not** (decision D5, `research.md` R8) — the
      docstring says so, with the `grep` that establishes it. **RED**: assert a
      neighbouring packet path that carries no doc-health delta.
- [x] T016 [TEST] [US3] `test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists` —
      `mbc.resolve(own_block, mbc.promoted(root, "doc-health"), mbc.sibling_titles(root))`
      returns status `canon` with basis `openspec/specs/doc-health/spec.md`; AND
      `add-family-enumeration-check` is absent from `openspec/changes/` and
      present under `openspec/changes/archive/`; AND `_arm_ordering` applies no
      basis override to this change. **Decision D2 asserted rather than
      asserted-about**: the packet's § 4.2 asks for a basis that archived at
      `f027d3b3` before the family registered, so the gate asserts the basis that
      exists and asserts the sibling's absence, making § 4.2's wording visibly
      history. **RED**: assert status `pending`, then assert the sibling is
      active.
- [x] T017 [TEST] [US3] `test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences` —
      exactly one `info` on the own-delta path, quoting BOTH
      `twenty-one check families` and `Four of the twenty-one`. The docstring
      records that this finding is **expected evidence, never a regression and
      never to be dispositioned** (F1's O2, packet § 6.6). **RED**: assert it
      quotes `twenty-two` — the block's own wording rather than canon's — and
      watch it fail, which is the point: the ledger names what CANON states and
      the block does not carry.
- [x] T018 [TEST] [US3] `test_no_disposition_can_apply_in_the_single_repo_scope_the_gate_runs_in` —
      `promotion_fidelity.load_dispositions(_ctx(root), mbc.FAMILY)` is empty
      because `agg_root is None`. The inherited single-repo caveat, asserted here
      so the gate's silence about dispositions is understood rather than
      discovered (F1's A7 made the same point for T045). **RED**: assert the set
      is non-empty.

**Checkpoint**: § 4.2 is discharged and the stale basis is recorded as history.

---

## Phase 6: User Story 4 — the report moves in this family's lines and nowhere else (Priority: P2)

**Goal**: bound the blast radius of registering a twenty-second family.

**Independent test**: two single-repo report runs of this checkout differing only
by `--skip-family`, diffed.

- [x] T019 [US4] Add `_report(root, tmp_path, skip=False)` — run
      `python3 scripts/doc-health.py --single-repo <root> --report-out <file>`
      (plus `--skip-family modified-block-currency` when `skip`) via
      `subprocess.run`, assert exit 0, return the rendered text. Docstring records
      why this is hermetic: a `--single-repo` run sets `agg_root=None`, so
      `runner._real_notebook_dryrun` returns before reaching `nlm`, and `gh`/`omp`
      have no call site in the doc-health runner (`research.md` R6).
- [x] T020 [TEST] [US4] `test_the_report_moves_only_in_this_family_s_lines` — the
      ONE count assertion this feature permits, and it is a DIFF: `critical` and
      `error` movement are `0`; `warning` and `info` movement equal the family's
      own per-severity finding counts **taken from the same tree in the same
      test**, so the literals `1` and `9` appear nowhere; every differing line
      falls in one of the four permitted classes (headline, skipped-family
      notice, `### modified-block-currency` section, ranked-plan rows whose
      `family=` is this family); and `## Per-Stage Counts`, `## Preflight` and
      every other `### <family>` section are byte-identical. **RED**: run BOTH
      passes with `--skip-family modified-block-currency` — movement reads
      0/0/0/0 while the family reports one warning and nine info, so the pin
      fails. That is the same manoeuvre as mutant M5.
- [x] T021 [US4] Record § 4.5 in `evidence/self-gate.md`: both commands, both
      headlines, the 4-hunk / 24-line diff classification, and the note that
      **§ 4.5 is self-contradictory as written** — it asks for "+1 warning, +11
      info … headline unchanged", and the headline is the line those counts are
      printed on. The implemented reading: the `error` and `critical` BANDS do
      not move, census / inventory / catalog are untouched (`research.md` R7).

**Checkpoint**: § 4.5 is discharged as both a test and a recorded gate.

---

## Phase 7: User Story 5 — the gate says what to do when the corpus moves (Priority: P2)

**Goal**: the failure message is a deliverable, not a side effect.

**Independent test**: read the messages; each names the tree, the subject, the
expected cause and the two legitimate responses.

- [x] T022 [TEST] [US5] `test_every_corpus_assertion_explains_what_to_do_when_the_corpus_moves` —
      `_moved(...)`'s output names the resolved root, the subject, the phrase
      identifying corpus movement as the expected cause, the re-measure command,
      and the zero end-state instruction; and every corpus-facing test in the
      module routes its message through `_moved` (asserted by source inspection
      of the module's own `assert` sites). **RED**: assert the message names a
      command that is not in it.
- [x] T023 [US5] Write `quickstart.md` § WHEN THE GATE FAILS into the module as a
      short pointer comment beside `_SCENARIO_SUBJECT`, naming the ONE expected
      movement by name: `add-composed-view-authoring` declaring its rename with a
      `Removed from canon by` marker, which the packet's § 6.3 already calls the
      correct disposition. A gate whose expected future failure is undocumented
      gets deleted rather than updated.

**Checkpoint**: SC-001 is discharged — the failing gate teaches.

---

## Phase 8: Polish, mutation and the gates

- [x] T024 [TEST] `test_the_family_reads_exactly_two_things_from_its_run_context` —
      FR-018, at BOTH levels the surface exists at (analyze finding A4 — the
      first cut of this task covered only the first): (a) the family's own module
      reads exactly one context attribute —
      `set(re.findall(r"ctx\.(\w+)", inspect.getsource(mbc))) == {"repo_paths"}`
      — and (b) it hands the context to exactly one collaborator,
      `load_dispositions(ctx`, occurring once, whose own read is `agg_root` and
      nothing else. This is what makes T004's two-attribute stand-in **provably**
      faithful rather than faithful-because-read-once; a newly read attribute at
      either level reds this test, which is the signal to widen the stand-in.
      **RED**: add a second attribute to the expected set at each level in turn.
- [x] T024a [TEST] `test_the_gate_reaches_the_corpus_only_through_the_family` —
      FR-001 asserted structurally rather than left to authoring discipline
      (analyze finding A3): this module's own source carries no requirement or
      markdown parser of its own — no `## MODIFIED` pattern, no
      `### Requirement:` pattern, no `#### Scenario:` pattern, no `parse_delta`
      or `parse_spec_requirements` reimplementation — and every corpus read goes
      through a named `mbc.*` public function. **RED**: add a throwaway
      `re.compile(r"^## MODIFIED")` to the module and watch it fail. *A gate that
      re-parsed the corpus would prove something about the gate.*
- [x] T025 THE MUTATION ROUND, five mutants, each recorded in
      `evidence/self-gate.md` with the test that killed it and the tests that
      SURVIVED it (a mutant only one test catches is a mutant reported honestly):
      **M1** remove the named-subject assertions from T012/T013 → the discovery
      floor (T008) must still fail on a vacuous read (simulate by pointing
      `active_blocks` at an empty temp tree);
      **M2** point `_repo_under_test` at another checkout → T006/T007 must fail;
      **M3** make discovery skip the own packet's change → T015/T016 must fail;
      **M4** widen the context probe's allowed set → T024 must fail;
      **M5** run both movement passes with the family skipped → T020 must fail.
- [x] T026 The count-delta evidence: `python3 -m pytest tests/doc-health -q`
      green, recorded against T001's baseline so the added tests are a visible
      delta (SC-006). **This single-directory run IS the evidence** — `python3 -m
      pytest tests` is never run from a worktree (it drives live Postgres; F1
      ruling N12).
- [x] T027 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, count
      recorded, run from the repository root per the aggregation CLAUDE.md's
      authoring note. **The count at this branch point is 76, not the 75 F1
      recorded** — the tree moved between F1's branch point and this one; the
      evidence names the tree each figure was taken at.
- [x] T028 Scope guard, mechanically:
      `git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/`
      prints NOTHING (FR-019). The full diff touches only
      `tests/doc-health/test_modified_block_currency_self_gate.py` and
      `specs/021-modified-block-currency-self-gate/`. Also
      `python3 -m pytest tests/doc-health/test_modified_block_currency.py
      tests/doc-health/test_modified_block_currency_fixtures.py -q` green and
      unchanged in count — F1's and F2's suites are untouched.
- [x] T029 Complete `evidence/self-gate.md`: the head SHA, the three gates with
      their commands and numbers, the re-measured movement table, the named
      subjects, the RED evidence per test, the five mutants, and § 4's defects as
      found (§ 4.1 stale count, § 4.2 stale basis, § 4.5 self-contradictory
      headline clause, F1's T057 absent).
- [x] T030 Draft `pr-body.md` in this feature directory: the packet and its
      ratification, § 4.1–4.5 discharged, the five orchestrator decisions D1–D5
      still flagged for veto, the statement that this change does **not** close
      #330 (packet § 7.1 requires the PR to say so), F1 residue finding 6 (T057),
      and that this gate's `warning` assertion is **expected to fall due** when
      `add-composed-view-authoring` moves. **Do not open the PR** — a combined
      adversarial review comes first.

**Checkpoint**: all of § 4 discharged, every mutant killed, every gate numbered.

---

## Dependencies

```text
Phase 1 (T001–T002)              setup; T001 must precede any test code
        ↓
Phase 2 (T003–T007)              FOUNDATIONAL — the resolver and the helpers
        ↓
Phase 3 (T008–T009)  US2         the floor; underpins US1's non-vacuity
        ↓
Phase 4 (T010–T014)  US1  ─┐
Phase 5 (T015–T018)  US3  ─┼─    independent of each other, both need Phase 3
Phase 6 (T019–T021)  US4  ─┘
        ↓
Phase 7 (T022–T023)  US5         reads the messages Phases 4–6 wrote
        ↓
Phase 8 (T024–T030)              mutation, gates, evidence
```

**Story independence.** US1, US3 and US4 are independently testable and can be
built in any order once Phase 3 lands. US2 is ordered first among the P1s because
its floor is what makes US1's claim non-vacuous — the spec's own SC-003 says the
two must be independent, and building them in this order is how that independence
gets checked rather than assumed. US5's subject is the messages the earlier
phases produce, so it is last.

## Parallel execution

- **T012, T013, T014** [P] — three separate test functions in the same file, no
  shared state beyond the module-level constants T010 lands.
- **T015, T017, T018** [P] — same.
- **T019/T020** are NOT parallel with anything: two subprocess report runs at ~7s
  each dominate the file's runtime, and running them beside other work makes a
  timing failure hard to attribute.
- **Phases 4, 5 and 6** can proceed in parallel by three agents. Only Phase 4
  depends on T010's constants; Phases 5 and 6 use literal paths and their own
  helper, so the dependency is internal to Phase 4 rather than a gate on the
  other two (analyze finding A5 — the first cut said otherwise). Each agent
  appends its own section of the file.

## Implementation strategy

**MVP = Phases 1–4** (T001–T014). That is § 4.1 fully discharged: the family runs
over this repository through itself and its findings are asserted by named
subject, with a floor that makes the claim non-vacuous. It is a coherent,
reviewable, mergeable state on its own.

**Increment 2 = Phase 5** (§ 4.2, the own packet). **Increment 3 = Phase 6**
(§ 4.5, the movement pin). **Increment 4 = Phases 7–8** (the maintenance contract
and the recorded gates).

Commit after each phase, with explicit pathspecs — this checkout is shared.
Phase 8 is ONE commit regardless of its seven tasks.

## Requirement coverage

| requirement | tasks | requirement | tasks |
| --- | --- | --- | --- |
| FR-001 run through the family, asserted | T004, T024a | FR-011 sibling absent | T016 |
| FR-002 resolve under test, named failure | T003, T007 | FR-012 self-finding quotes both | T017 |
| FR-003 not the aggregation root | T006, T007 | FR-013 no disposition applies | T018 |
| FR-004 list not Skip | T009 | FR-014 movement as a diff | T019, T020 |
| FR-005 discovery floor | T008 | FR-015 bands and line classes | T020 |
| FR-006 scenario arm named | T012 | FR-016 failure messages | T005, T022, T023 |
| FR-007 ledger set named | T010, T011, T013 | FR-017 evidence with commands | T001, T021, T026, T027, T029 |
| FR-008 empty classes by rule text | T014 | FR-018 context surface, both levels | T024 |
| FR-009 own delta examined | T015 | FR-019 no module change | T028 |
| FR-010 basis is canon | T016 | FR-020 RED-first | every `[TEST]`, T025 |

| success criterion | discharged by |
| --- | --- |
| SC-001 the failing gate teaches | T005, T022, T023 |
| SC-002 broken discovery fails naming an empty read | T008 |
| SC-003 the two guards are independent | T025 M1 |
| SC-004 a wrong checkout fails | T025 M2 |
| SC-005 the movement pin fails with the family skipped | T025 M5 |
| SC-006 suite green, delta visible | T001, T026 |
| SC-007 validate green with its count | T001, T027 |
| SC-008 only the four line classes move | T020, T021 |
| SC-009 the scripts/openspec/.github diff is empty | T028 |

## Analyze pass (2026-08-27) — eleven findings, five fixed, six dispositioned

`/speckit-analyze` over `spec.md` / `plan.md` / `tasks.md`. **No CRITICAL
findings.** Recorded here rather than in a separate file because this is where
the remediation landed.

**FIXED before implementation:**

- **A1 (HIGH) — the spec's motivating claim was false.** It said "if
  `active_blocks` returned an empty list, every fixture test would still pass".
  The fixture trees carry `openspec/changes/`, an `archive/` directory and a
  `proposal.md` each, so they route through the same discovery and a total break
  reds them. `spec.md` § Why this feature exists now states the accurate and
  stronger case — fixtures prove the RULES, nothing proved the VERDICT — and
  names the four things fixtures genuinely cannot reach. *The overstatement is
  the class of defect this feature exists to catch, so it is recorded rather
  than quietly corrected.*
- **A2 (HIGH) — `quickstart.md` predicted a suite total of 1127** ("1115 + 12")
  while `tasks.md` defined fourteen `[TEST]` tasks. It now points at
  `evidence/self-gate.md` and predicts nothing: one number, one home.
- **A3 (MEDIUM) — FR-001 had no assertion.** "Through the family, not a
  reimplementation" was a construction constraint mapped to "all `[TEST]`". FR-001
  now requires a structural assertion and **T024a** carries it.
- **A4 (MEDIUM) — FR-018 was stated at a level its mechanism did not cover.**
  It said the family "reads exactly two things from its run context"; measured,
  `modified_block_currency.py` reads exactly ONE (`ctx.repo_paths`) and
  `agg_root` is read transitively inside
  `promotion_fidelity.load_dispositions`. FR-018 now states both levels and T024
  asserts both.
- **A5 (LOW) — the parallel-execution note claimed a dependency that does not
  exist.** T010 gates Phase 4 only.

**DISPOSITIONED, not remediated:**

- **A6 (MEDIUM) — `clarify` and `/speckit-checklist` did not run**, though the
  constitution's stated lifecycle includes both. No material ambiguity existed:
  the three questions that could have been asked were pre-settled as D1–D3,
  recorded in `plan.md` and flagged for veto rather than put to Brett twice. The
  requirements checklist exists from `specify`. The constitution's clarify clause
  is conditional ("material ambiguities MUST be resolved before planning") and is
  satisfied.
- **A7 (MEDIUM) — the MANDATORY `before_specify` hook (`speckit.git.feature`)
  was not run.** The branch and the feature directory pre-existed by
  instruction; running the hook would have created a second branch, which the
  git rules for this feature forbid. The hook's product is already present.
- **A8 (LOW) — the resolver guard depends on `git` on PATH** (`rev-parse
  --show-toplevel`). Kept hard rather than skip-guarded: every gate runs inside a
  git checkout, `git` is not one of the hermeticity-guarded binaries, and a skip
  would make the strongest anti-wrong-checkout assertion optional.
- **A9 (LOW) — US2's second acceptance scenario describes a mutation-round
  manoeuvre, not a test.** The spec now says so. A test that deleted its
  sibling's assertion would be a test of the test file.
- **A10 (LOW) — T030 (`pr-body.md`) maps to no FR.** By design: a process
  artefact, and packet § 7.1 requires the PR to state that this change does not
  close #330.
- **A11 (LOW) — `openspec validate` reads 76 here and F1 recorded 75.** The tree
  moved between the two branch points. T027 already names the discrepancy; every
  figure names the tree it was taken at.

**Metrics**: 29 requirements (20 FR + 9 SC), 31 tasks, 100% mapped, 0 CRITICAL.

---

## Hand-off to F4

**What F4 must NOT duplicate.** This feature asserts the report's *line
movement*, not its *rendering*. Packet § 5.1 (the three arms distinguishable
rather than summed) and § 5.2 (the action line) are untouched here and are F4's
alone. § 5.3's workflow pin is likewise untouched: `.github/` has no diff on this
branch and T028 asserts it.

**What F4 inherits.**

1. **The figures table** in `plan.md` § THE FIGURES is the single home. F4 asserts
   nothing about counts; if its rendering work moves a count, this gate reds and
   that is the correct signal.
2. **This gate's `warning` assertion is expected to fall due.**
   `add-composed-view-authoring` declaring its rename with a `Removed from canon
   by` marker is the packet's own § 6.3 disposition. When it lands, T012 fails
   with `_moved`'s instruction. F4 should not be surprised by it and must not
   "fix" it by loosening the assertion.
3. **§ 4's three defects and F1's T057 absence** are recorded in
   `evidence/self-gate.md`. F4's § 5 should be read with the same suspicion: it
   was written at `9be81a40` against a tree that no longer exists.
4. **The report subprocess helper** (`_report`) is reusable and its hermeticity
   argument is written down (`research.md` R6). F4 will want it.

**One thing to know.** F1's mutation round found three missing tests that
twenty-one green tests had not. F2 found five artefact discrepancies in F1. This
feature found a sixth — a task ticked `[x]` for a test that does not exist. Run
the round; do not assume a green suite means a covered rule, and do not assume a
ticked box means a landed artefact.
