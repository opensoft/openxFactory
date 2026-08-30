---

description: "Implementation tasks for the resolved council-seats contract family"
---

# Tasks: Resolved Council Seats

**Input**: Design documents from `specs/026-add-resolved-council-seats/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`

**Tests**: Required. The feature specification defines independent tests and
measurable conformance outcomes. Write each marked test first and confirm it
fails for the intended reason before implementing the corresponding behavior.

**Organization**: Tasks are grouped by user story. This feature owns only the
openxFactory neutral realization. Hermes Install and codexFactory runtime work
must be created and executed in separately identified successor features.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes a different file and does not
  depend on another incomplete task.
- **[Story]**: Maps work to one user story from `spec.md`.
- Every task includes an exact repository-relative file path.

## Phase 1: Setup (Shared Contract Structure)

**Purpose**: Establish the contract-family and focused test surfaces without
changing release metadata or downstream repositories.

- [x] T001 Create the contract-family orientation, ownership boundary, artifact inventory, and prohibited-data rules in `contracts/council-convening/README.md`
- [x] T002 [P] Create the indexed fixture catalog skeleton with `schema_version`, `kind`, deterministic ordering, and no unindexed paths in `contracts/council-convening/fixtures/index.yaml`
- [x] T003 [P] Create the focused test module and reusable repository-relative fixture path helpers in `tests/council_convening/test_contract.py`
- [x] T004 [P] Create CLI invocation/result helpers and temporary-fixture support in `tests/council_convening/test_validator_cli.py`

**Checkpoint**: Contract, fixture, and test paths exist; no manifest, changelog,
bundle, or downstream source has changed.

---

## Phase 2: Foundational (Blocking Conformance Primitives)

**Purpose**: Build the test-first parsing and deterministic result foundation
used by every story.

**CRITICAL**: No story implementation begins until these tasks pass.

- [x] T005 Add failing tests for fixture-index schema metadata, unique case IDs/paths, path containment, exact file parity, and stable expected-result fields in `tests/council_convening/test_contract.py`
- [x] T006 Add failing tests for deterministic JSON output, CLI exit codes 0/1/2, and complete indexed-corpus validation under 30 seconds in `tests/council_convening/test_validator_cli.py`
- [x] T007 Implement strict fixture-index loading, repository-relative path containment, case selection, and deterministic result/finding ordering in `scripts/validate-council-convening.py`
- [x] T008 Implement `--strict`, `--case`, and `--json` CLI handling with exit 2 for invocation/harness failures in `scripts/validate-council-convening.py`
- [x] T009 Make the foundational fixture-index and CLI protocol tests pass in `tests/council_convening/test_contract.py` and `tests/council_convening/test_validator_cli.py`

**Checkpoint**: The harness can enumerate an indexed corpus and report stable
machine outcomes before roster semantics are implemented.

---

## Phase 3: User Story 1 - Admit The Correct Roster Before Work Starts (Priority: P1) MVP

**Goal**: Publish and validate the closed convening shape and prove that
standing-only and condition-triggered rosters contain exactly the required
unique declared seats before any consumer issues work.

**Independent Test**: Run the focused schema/corpus suite for `standing-roster`,
`conditional-seat-required`, absent, duplicate, unknown, incomplete, and
mismatched roster cases. Both positives accept with zero findings and every
negative refuses for its declared primary code.

### Tests For User Story 1

- [x] T010 [P] [US1] Add failing Draft 2020-12 meta-schema, closed-shape, required-field, seat-identifier, non-empty-roster, and unique-roster tests in `tests/council_convening/test_contract.py`
- [x] T011 [P] [US1] Add failing positive corpus tests for standing-only and condition-triggered roster set arithmetic in `tests/council_convening/test_validator_cli.py`
- [x] T012 [US1] Add failing negative corpus tests for absent, empty, malformed, duplicate, unknown, standing-incomplete, and rule-inconsistent rosters in `tests/council_convening/test_validator_cli.py`

### Implementation For User Story 1

- [x] T013 [US1] Implement the closed Draft 2020-12 convening, roster, seat-resolution, candidate, rule-reference, fact, and provenance shapes in `contracts/council-convening/resolved-council-convening.schema.yaml`
- [x] T014 [P] [US1] Add the standing-only accepted case with deterministic rule/head resolver inputs and traceability metadata in `contracts/council-convening/fixtures/positive/standing-roster.yaml`
- [x] T015 [P] [US1] Add the condition-triggered accepted case with the conditional seat and exact consumed facts in `contracts/council-convening/fixtures/positive/conditional-seat-required.yaml`
- [x] T016 [P] [US1] Add invalid roster cases in `contracts/council-convening/fixtures/negative/roster-absent.yaml`, `contracts/council-convening/fixtures/negative/roster-empty.yaml`, `contracts/council-convening/fixtures/negative/roster-malformed.yaml`, `contracts/council-convening/fixtures/negative/roster-duplicate.yaml`, `contracts/council-convening/fixtures/negative/roster-unknown-seat.yaml`, `contracts/council-convening/fixtures/negative/roster-standing-incomplete.yaml`, and `contracts/council-convening/fixtures/negative/roster-mismatch.yaml`
- [x] T017 [US1] Register every User Story 1 case, expected outcome, primary finding, governed scenario, feature requirement, and evidence ID in `contracts/council-convening/fixtures/index.yaml`
- [x] T018 [US1] Implement schema validation, closed seat declarations, deterministic standing-plus-true-conditional set construction, uniqueness, and roster equality findings in `scripts/validate-council-convening.py`
- [x] T019 [US1] Make all User Story 1 tests pass and confirm each negative fails for only its intended primary reason in `tests/council_convening/test_contract.py` and `tests/council_convening/test_validator_cli.py`

**Checkpoint**: User Story 1 is a complete provider MVP. The neutral contract
accepts both valid roster modes and refuses malformed or inconsistent rosters;
runtime freeze/job issuance remains an explicit Hermes successor gate.

---

## Phase 4: User Story 2 - Reproduce Why Each Seat Was Required (Priority: P1)

**Goal**: Make every accepted roster reproducible from one exact candidate head,
one immutable governed rule locator, one matched class, and the normalized facts
that its conditions consume.

**Independent Test**: Re-run the accepted fixtures through deterministic
fixture-supplied rule/head resolvers, then run conclusion-only, unavailable-rule,
missing-fact, condition-result-drift, and stale-head cases. Only complete,
independently reproduced inputs accept.

### Tests For User Story 2

- [x] T020 [P] [US2] Add failing tests for canonical repository names, positive pull-request numbers, normalized relative rule paths, lowercase 40-hex revisions, matched class, and prohibited secret/path fields in `tests/council_convening/test_contract.py`
- [x] T021 [P] [US2] Add failing resolver tests for exact rule lookup, candidate-head comparison, consumed-fact completeness, independent condition evaluation, and producer-result drift in `tests/council_convening/test_validator_cli.py`
- [x] T022 [US2] Add failing acceptance-map parity tests for exactly 3 governed requirements, 11 scenarios, 14 FRs, and 7 SCs in `tests/council_convening/test_contract.py`

### Implementation For User Story 2

- [x] T023 [P] [US2] Add conclusion-only provenance and unavailable immutable-rule negative cases in `contracts/council-convening/fixtures/negative/provenance-opaque.yaml` and `contracts/council-convening/fixtures/negative/rule-revision-unavailable.yaml`
- [x] T024 [P] [US2] Add provenance drift cases in `contracts/council-convening/fixtures/negative/fact-missing.yaml`, `contracts/council-convening/fixtures/negative/condition-result-drift.yaml`, and `contracts/council-convening/fixtures/negative/candidate-head-stale.yaml`
- [x] T025 [US2] Register every User Story 2 case and its exact primary finding/traceability in `contracts/council-convening/fixtures/index.yaml`
- [x] T026 [US2] Implement deterministic fixture-backed immutable-rule resolution, candidate-head comparison, fact completeness, independent condition evaluation, and provenance findings in `scripts/validate-council-convening.py`
- [x] T027 [US2] Add the complete required shape, independent validation sequence, refusal semantics, and non-goals to `contracts/council-convening/README.md`
- [x] T028 [US2] Make all User Story 2 tests pass with no network access, shared producer evaluator code, opaque conclusions, raw provider payloads, secrets, or host-absolute paths in `tests/council_convening/test_contract.py` and `tests/council_convening/test_validator_cli.py`

**Checkpoint**: Every provider-accepted roster is provenance-complete and
reproducible; a trusted producer assertion alone never establishes correctness.

---

## Phase 5: User Story 3 - Complete Only From The Frozen Roster (Priority: P2)

**Goal**: Publish the neutral obligations and machine-checkable handoff that keep
the admitted roster authoritative through job issuance, return admission,
substantive counting, unanimity, signing isolation, recovery, and hard cutover.

**Independent Test**: Validate that the neutral schema excludes private key and
obsolete compatibility fields, all relevant requirements/outcomes map to an
external blocking gate, and named successor feature records pin this provider
without claiming their runtime evidence before it lands.

### Tests For User Story 3

- [x] T029 [P] [US3] Add failing tests that private-key/root-key/shared-key and obsolete roster-reconstruction fields are rejected by the closed contract schema in `tests/council_convening/test_contract.py`
- [x] T030 [US3] Add failing tests that every FR-008 through FR-014 and SC-003 through SC-007 maps to a blocking successor or cutover gate in `tests/council_convening/test_contract.py`

### Implementation For User Story 3

- [x] T031 [US3] Add frozen-snapshot, one-job-per-seat, unlisted/missing return, rich outcome, recovery, job-local-key, no-compatibility, and rollback obligations to `docs/roles-and-authority.md`
- [x] T032 [US3] Add provider, Hermes consumer, codexFactory producer, coordinated activation, paired rollback, and evidence-ownership instructions to `contracts/council-convening/README.md`
- [x] T033 [US3] Create the Hermes Install successor feature in its own repository/worktree and record its exact feature identifier and provider dependency in `openspec/changes/add-resolved-council-seats/tasks.md`
- [x] T034 [US3] Create the codexFactory successor feature in its own repository/worktree and record its exact feature identifier, governed reusable-workflow subject, and provider dependency in `openspec/changes/add-resolved-council-seats/tasks.md`
- [x] T035 [US3] Make User Story 3 provider tests pass while leaving Hermes runtime, codexFactory signing, live OIDC, deployment, and merged-successor evidence explicitly external/open in `tests/council_convening/test_contract.py`

**Checkpoint**: The provider-side contract and handoff are complete. User Story 3
is not end-to-end complete until the two recorded successor features land and
their independent evidence passes.

---

## Phase 6: Release Registration And Cross-Cutting Validation

**Purpose**: Register the new family, prove repository-wide consistency, and
prepare honest provider evidence without reserving or claiming external acts.

- [x] T036 Add the council-convening family, intended consumers, schema path, validator command, fixture index, and successor handoff to `contracts/README.md`
- [x] T037 Run strict OpenSpec, the complete council-convening validator, focused pytest including the under-30-second corpus assertion, existing non-PostgreSQL repository tests, and YAML `schema_version`/`kind` checks from `specs/026-add-resolved-council-seats/quickstart.md`
- [x] T038 Record only actually performed provider-local checks and exact artifact digests with mandatory `schema_version` and `kind` in `openspec/changes/add-resolved-council-seats/evidence/provider-local-validation.yaml`
- [x] T039 Mark OpenSpec handoff tasks 2.1 and 2.2 complete only after this executable ledger and both exact successor feature identifiers exist in `openspec/changes/add-resolved-council-seats/tasks.md`
- [x] T040 With explicit authorization, preserve the complete uncommitted provider candidate, refresh remote main/tags, rebase the clean feature branch, restore the candidate without loss, and establish the next available additive bundle under `docs/contract-versioning-policy.md`
- [ ] T041 In one serialized candidate commit, add the family/schema/semantic members to `contracts/manifest.yaml`, add the allocated bundle and hard-cutover note to `contracts/CHANGELOG.md`, build `contracts/releases/${bundle_tag}.digests.yaml`, and include all reviewed contract/validator/test/document changes
- [ ] T042 Run every provider gate and independent review against the exact unchanged candidate commit and verify it with `scripts/validate-contract-release.py verify-commit --commit "$candidate_commit"`
- [ ] T043 With explicit authorization, land the exact reviewed candidate, verify remote-main reachability and the annotated tag with `scripts/validate-contract-release.py verify-promotion` and `verify-tag`, then complete OpenSpec realization task 3.1 in `openspec/changes/add-resolved-council-seats/tasks.md`
- [ ] T044 Record exact landed Hermes and codexFactory commits plus standing, conditional, invalid-provenance, stale-head, missing-return, signing-isolation, and hard-cutover results with mandatory `schema_version` and `kind` in `openspec/changes/add-resolved-council-seats/evidence/successor-conformance.yaml`
- [ ] T045 Independently reproduce every object and result cited by successor conformance evidence before completing OpenSpec realization task 3.2 in `openspec/changes/add-resolved-council-seats/tasks.md`
- [ ] T046 Archive `add-resolved-council-seats` so the archive operation promotes the ratified delta only after T043 and T045 pass and OpenSpec task 3.3 is satisfied under `openspec/changes/archive/`
- [ ] T047 Re-run strict OpenSpec and repository document-health validation after archive and record no unresolved change/spec contradiction in `openspec/changes/archive/`

---

## Dependencies And Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup; blocks every story.
- **User Story 1 (Phase 3)**: Depends on Foundational; provider MVP.
- **User Story 2 (Phase 4)**: Depends on the User Story 1 schema and harness.
- **User Story 3 (Phase 5)**: Depends on the final User Story 1/2 contract shape;
  successor creation may then proceed in parallel across repositories.
- **Release (Phase 6)**: T036-T039 may begin after all provider story tests pass;
  T040-T047 are serialized realization/external-evidence tasks.

### User Story Dependency Graph

```text
Setup -> Foundation -> US1 provider MVP -> US2 reproducibility -> US3 handoff
                                                             |-> Hermes successor
                                                             |-> codexFactory successor
All provider stories -> release registration -> candidate verification
Both successors + provider release -> external conformance -> archive
```

### Parallel Opportunities

- T002-T004 create disjoint setup files.
- T010 and T011 write disjoint User Story 1 test files before implementation.
- T014-T016 create independent fixture files after the schema contract is fixed.
- T020 and T021 write disjoint User Story 2 test files.
- T023-T024 create independent provenance fixture files.
- T029 and T030 are sequential because they share one test file.
- T033 and T034 may research separate successor scopes concurrently, but their
  writes to the shared OpenSpec task ledger are serialized.
- T036 and T038 update distinct documentation/evidence files; versioned release
  surfaces remain serialized together in T041.

## Parallel Example: User Story 1

```text
Task: T010 schema and closure tests in tests/council_convening/test_contract.py
Task: T011 positive corpus tests in tests/council_convening/test_validator_cli.py

After T013 fixes the schema contract:
Task: T014 standing-roster fixture
Task: T015 conditional-seat-required fixture
Task: T016 malformed/inconsistent roster fixtures
```

T012 follows T011 because both target `test_validator_cli.py`.

## Parallel Example: User Story 2

```text
Task: T020 provenance shape/security tests
Task: T021 independent resolver tests

After tests establish the contract:
Task: T023 opaque/unavailable provenance fixtures
Task: T024 missing-fact/result-drift/stale-head fixtures
```

T022 follows T020 because both target `test_contract.py`.

## Implementation Strategy

### Provider MVP First

1. Complete Setup and Foundational phases.
2. Implement User Story 1 test-first.
3. Stop and run only the focused schema/corpus suite.
4. Continue to User Story 2 after the roster shape is stable.

### Incremental Delivery

1. **US1**: Closed roster and deterministic set arithmetic.
2. **US2**: Immutable provenance and independent reproduction.
3. **US3**: Frozen-lifecycle/cutover obligations and named successor handoffs.
4. **Provider release**: Register, validate, allocate late, verify exact commit.
5. **Successors**: Implement in their own features and attach landed evidence.
6. **Archive**: Only after provider and both successors are independently proven.

### Stop Conditions

- Stop before T033/T034 if a downstream repository/worktree cannot be created
  without modifying a dirty root checkout.
- Stop before T040 if the next available bundle cannot be established from
  refreshed remote release surfaces.
- Keep T043-T047 open when merge, tag, live OIDC, deployment, or successor
  evidence is unavailable. Never replace external proof with a local assertion.

## Notes

- `[P]` means file-safe parallelism, not permission to bypass dependencies.
- Tests precede implementation for every story.
- No task adds a compatibility parser or reconstructs a missing roster.
- No task stores or transports private signing key material.
- Do not commit, merge, tag, publish, deploy, or archive without explicit
  authorization even when an implementation task has otherwise passed.
