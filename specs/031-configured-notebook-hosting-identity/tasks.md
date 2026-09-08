# Tasks: The hosting declaration becomes a configured value

**Input**: Design documents from `specs/031-configured-notebook-hosting-identity/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`
**Packet**: `openspec/changes/adopt-configured-notebook-hosting-identity/tasks.md`
— every task below names the packet group it discharges. Packet boxes are ticked
in that file, not here.

**Tests are requested and they are the point.** The change removes the only
automatic conformance check the live declaration has, and is obliged to replace it
rather than lose it.

## Path Conventions

Single repository. Paths are repository-root-relative.

## Phase 1: Setup and premise re-check (packet Group 0.3)

- [x] T001 Re-measure the packet's premises at realization head and record them in
      `specs/031-configured-notebook-hosting-identity/research.md` § 0.3 — the four
      addresses' line counts by file, the release-inventory non-membership, PR #786's
      landing, and the `openspec validate --all --strict` baseline.
- [x] T002 Take the two suite baselines the realization will be measured against:
      `pytest tests/notebooklm tests/doc-health tests/sequenced_after -q` and
      `scripts/doc-health.py --single-repo .`. Recorded in `research.md`.

## Phase 2: Foundational — the resolver (packet Group 2) 🎯 BLOCKS EVERYTHING ELSE

- [x] T003 [P] Add `hosting_declaration_path(root)` to
      `scripts/sync-notebooklm-books.py`: `$XFACTORY_NOTEBOOK_HOSTING_DECLARATION`
      (absolute or workspace-relative), then `<root>/.xfactory/notebook-hosting.yaml`'s
      `declaration_path:`, then None. Standard library only. An empty environment
      value is unset. (packet 2.1)
- [x] T004 `HOSTING_REL` stops being the declaration's path and becomes
      `EXAMPLE_REL`, naming the SHIPPED FIXTURE for prose and remedies only;
      `read_hosting_declaration()` takes its path from the resolver, returns None
      when nothing is configured or the configured path is not a file, and keeps its
      parse UNCHANGED in shape. `instance` joins `_HOSTING_SCALARS` — without it the
      reader cannot see the marker at all. (packet 2.2)
- [x] T005 `_refuse_unusable_declaration()` gains the example refusal, worded like
      its siblings — what was found, why it is refused, the exact remedy — and it
      runs immediately after the unreadable-declaration branch so the message is
      about the fixture rather than about some later missing field.
      `enforce_hosting_profile()`'s five steps and every existing refusal message
      are untouched. (packet 2.2)
- [x] T006 `scripts/validate-notebook-projection-hosting.py`: precedence becomes
      `argv[1]`, then the resolver, then `DEFAULT_REL` **as a fixture**; add
      `--resolved` so the operator check is one scriptable command; keep the
      not-found message's meaning — an install that has declared nothing is a
      transition state, not a passing one. (packet 2.3)
- [x] T007 `.gitignore` the workspace configuration file and state in the ignore
      entry's own comment that it is per-machine and carries no secret — a path is
      not a credential and nothing about this file should invite one. (packet 2.6)

## Phase 3: User Story 1 — the operator's binding survives the move (Priority: P1)

### Tests for User Story 1

- [x] T008 [P] `test_the_env_var_resolves_the_declaration` — an absolute path in
      `$XFACTORY_NOTEBOOK_HOSTING_DECLARATION` binds the run. (packet 2.4)
- [x] T009 [P] `test_a_workspace_relative_env_var_resolves_from_the_root` — the
      same declaration reached by the relative spelling binds identically.
- [x] T010 [P] `test_the_workspace_configuration_resolves_the_declaration` — the
      `.xfactory/notebook-hosting.yaml` arm binds the run. (packet 2.4)
- [x] T011 [P] `test_the_env_var_wins_over_the_workspace_configuration` — D-1's
      precedence, asserted rather than assumed.
- [x] T012 [P] `test_a_configured_path_that_does_not_exist_is_undeclared` — the
      uninitialized-submodule case the packet's OQ-A table calls correct.
- [x] T013 [P] `test_a_resolved_declaration_is_validated` — the validator's
      resolved-path mode over a synthetic declaration in a temporary tree, which is
      one of the three things replacing the lost check. (packet design § 3.4)

### Implementation for User Story 1

- [x] T014 Make `_declare_hosting()` in `tests/notebooklm/test_sync_notebooklm_books.py`
      write the workspace configuration beside the declaration it writes, so every
      EXISTING test in that module keeps its body and its assertions unchanged and
      passes through the resolver. This is packet 2.5, the box that makes the
      operator move safe.
- [x] T015 Run the whole `tests/notebooklm` suite and confirm no existing
      assertion changed and none failed. (packet 2.5)

## Phase 4: User Story 2 — a public cloner carries a shape (Priority: P1)

### Tests for User Story 2

- [x] T016 [P] `test_absent_configuration_is_undeclared_and_does_not_break` — the
      clone case: reported as a transition state, run continues unbound. (packet 2.4)
- [x] T017 [P] `test_a_configured_path_resolving_to_the_shipped_example_is_refused`
      — the fail-closed arm; the message names the file and the remedy. (packet 2.4)
- [x] T018 [P] Re-aim and rename `test_the_committed_record_conforms` to
      `test_the_committed_example_conforms`, keeping its assertion and changing its
      subject to the synthetic instance. (packet 3.5, design § 3.4)

### Implementation for User Story 2

- [x] T019 Rewrite `examples/notebook-projection-hosting.yaml` as a SYNTHETIC
      instance: `hosting.account`, `hosting.migration.from_account`, every
      `share_out[].hosting_account` and `[].user`, and the `denied[]` row become
      `example.invalid` addresses; `hosting.domain` matches the synthetic account's
      domain because the validator compares those two fields. (packet 3.1)
- [x] T020 Mark it in the record — `hosting.instance: example` — at the two-space
      indent the sync's narrow reader parses, never in a comment. (packet 3.2, OQ-C)
- [x] T021 Keep the SHAPE: same keys, same order, same comment structure, same
      roster arity. Rewrite the prose comments to describe the SHAPE rather than one
      operator's history — the migration narrative, the 2026-08-27 rulings and the
      denial's reasoning belong to the live record, which now holds them. (packet 3.3)
- [x] T022 Take the actor names to role placeholders, keeping
      `share_out[].granted_by` equal to `approval.designated_actor` — the validator
      refuses them unequal, so this is one edit in two places. (packet 3.4, OQ-D)
- [x] T023 Add the pointer the public tree is allowed to carry: a comment saying a
      live roster of governed acts exists, that it lives with the live declaration in
      its configured private home, and naming NO value. (OQ-E)
- [x] T024 Prove it: `python3 scripts/validate-notebook-projection-hosting.py`
      exits 0 over the synthetic instance. (packet 3.5)
- [x] T025 Leave `examples/lifecycle-notebook-workspaces.yaml` ALONE — its two
      lines are comments and belong to the Q1 docs pull request. (packet 3.6)

## Phase 5: User Story 3 — the fixture literals (Priority: P2, packet Group 4)

- [x] T026 [P] `tests/notebooklm/test_nlm_auth.py`: `STORED` and `LEGACY` become
      synthetic. They are compared against each other and against captured values
      inside the harness, never against a live account. (packet 4.1)
- [x] T027 [P] `tests/notebooklm/test_sync_notebooklm_books.py`:
      `HOSTING_DECLARED`, `HOSTING_PENDING`, `MigrationStateVocabularyTests.BASE`
      and the assertions over them go synthetic. Keep the PENDING assertion that the
      run binds where the books actually live. (packet 4.2)
- [x] T028 [P] `tests/notebooklm/test_validate_hosting.py`: `BASE`, `ENTRY`,
      `FIELDS` and the assertions over them go synthetic. Keep every negative
      mutation firing for its stated reason — service account, consumer account,
      domain mismatch, roster-key collision, `granted_by` disagreement. (packet 4.3)
- [x] T029 Re-run the whole suite and check the `pytest-suite` pins: SKIPPED must
      not move, SELECTED and PASSED may only rise. Per that workflow's own comment
      the floors need no edit, so the workflow is NOT touched. (packet 4.4, and
      `research.md` § 5 for the reason)
- [x] T030 Sweep: `git grep -nE "<the four addresses>"` over `tests/`, `examples/`,
      `scripts/` and `openspec/specs/` and file the output as realization evidence.
      Expect exactly ONE line, in the promoted spec, reserved for the archive act.
      (packet 4.5)

## Phase 6: Documents and records (packet Group 6)

- [x] T031 `docs/lifecycle-notebook-projection.md` § *The declaration* and § *The
      approval lane*: describe the two-file model — the synthetic instance here, the
      live record resolved from configuration, the resolution order, and the operator
      check that replaces the CI one. (packet 6.1)
- [x] T032 [P] `docs/notebook-projection-migration-runbook.md` and
      `docs/notebooklm-sync-open-item.md`: update the path references that now
      resolve differently; touch only the structural claims. (packet 6.2)
- [x] T033 Tick the packet's own `tasks.md` boxes for work that will be TRUE when
      this pull request merges, and say in the pull-request body which ticks depend
      on the merge and which remain the operator's.
- [x] T034 `specs/031-configured-notebook-hosting-identity/quickstart.md`: the
      operator's two commands and the one file they write.

## Phase 7: The cross-repository half (packet Group 5 — OPERATOR)

- [x] T035 Verify the destination repository is PRIVATE before any real identity is
      committed to it. **Gate: if it is not private, stop.**
- [x] T036 Prepare the hermes-install pull request placing the live record INTACT at
      `config/clients/opensoft/notebook-projection-hosting.yaml` — `hosting:` block,
      `custody:` reference, `approval:` block, all seven `share_out` rows and the
      `denied` row, verbatim. Follow that repository's own `config/clients/opensoft/`
      conventions and run its tests. (packet 5.1)
- [x] T037 Label that pull-request body **OPERATOR step — Brett places/merges** and
      do NOT tick packet boxes 5.1–5.4. They are Brett's, in a private repository, on
      his own word.

## Dependencies & Execution Order

- Phase 2 blocks everything: no test of the resolver exists until the resolver does.
- T014/T015 (packet 2.5) must be green before T019 (packet 3.1) is worth trusting —
  proving the resolver behaviour-preserving is what makes the record's move safe.
- T018 depends on T019 (its new subject must exist).
- T031 depends on T019–T023 (the document describes what the record became).
- Phase 7 is independent of Phases 2–6 in code and dependent on them in ORDER: see
  `plan.md` § Ordering for the merge sequence and the declared deviation.

### Parallel Opportunities

T008–T013 and T016–T017 are one file each in the same module and are written
together; T026, T027 and T028 are three different files and genuinely parallel.
