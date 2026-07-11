# Tasks: AVC Reference Runtime

**Input**: Design documents from `specs/003-avc-reference-runtime/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ports.md, contracts/conformance-artifacts.md, quickstart.md

**Tests**: Tests are the **primary deliverable** of this feature (the whole point is a deterministic
suite mapped to every applicable `ACR-*`/`ARR-*` acceptance ID). Test tasks are therefore first-class
and appear within each user-story phase; each behavioral test encodes the ARR/ACR scenarios it maps to
via `conformance/scenario-test-map.yaml`.

**Organization**: Tasks are grouped by user story (US1=P1, US2=P2, US3=P3) so each story is
independently implementable and testable. Shared infrastructure is in Setup/Foundational.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1 / US2 / US3 (Setup, Foundational, and Polish carry no story label)
- Every task names an exact file path. Ownership boundary: only `xfactory/avatar_runtime/`,
  `tests/avatar_runtime/`, and the declared exception `scripts/validate-avatar-runtime.py` + its
  single `README.md` validator-index line. No sibling-owned path is written (FR-036, SC-008).

## Path Conventions

Single-project internal library. Runtime core at `xfactory/avatar_runtime/`, tests at
`tests/avatar_runtime/`, standalone gate at `scripts/validate-avatar-runtime.py`. Python 3.11+,
stdlib-only runtime; tests/validator may use pinned `pytest`, `pytest-randomly`, `PyYAML`, `jsonschema`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Directory structure and toolchain configuration.

- [x] T001 Create the package and test-tree structure (`xfactory/avatar_runtime/`, `tests/avatar_runtime/{fakes,provisional,boundary,conformance}/`) per plan.md §Project Structure
- [x] T002 [P] Author `xfactory/avatar_runtime/__init__.py` reference-only docstring stating non-deployable / no application factory / no listener / no provider key
- [x] T003 [P] Pin and document test-only dev dependencies and the `pytest` + `pytest-randomly` configuration (Python 3.11+, no 3.12-only syntax) in `tests/avatar_runtime/README.md`
- [x] T004 [P] Document the recorded-seed convention (how many seeds, where recorded) for `pytest-randomly` runs in `tests/avatar_runtime/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The injected ports, typed values, deterministic sources, fakes, and runtime assembly that ALL user stories depend on.

**⚠️ CRITICAL**: No user-story work can begin until this phase is complete.

- [x] T005 [P] Implement the seven injected-port `Protocol`s (`ClockPort`, `IdPort`, `ProviderPort`, `PolicyPort`, `ConsentPort`, `OperationPort`, `UsagePort`) in `xfactory/avatar_runtime/ports.py` (per contracts/ports.md, FR-007)
- [x] T006 [P] Implement frozen typed values + closed fail-closed registries (`SessionState`, `AttemptStatus`, `PreflightKind`, `OutcomeCode`, `PurposeId`, `EventKind`, `ProducerAuthority`, `ReasonCode`, `DispositionKind`) in `xfactory/avatar_runtime/values.py` (per data-model.md, FR-010/§VII)
- [x] T007 [P] Implement `ManualClock` (monotonic + wall, `advance()`) in `xfactory/avatar_runtime/clocks.py` (FR-008)
- [x] T008 [P] Implement `QueuedIdSource` (deterministic id sequence, no randomness) in `xfactory/avatar_runtime/ids.py` (FR-007)
- [x] T009 Implement structured `TelemetryRecord` + redaction validator (reject-and-do-not-publish on SDP/credential/payload/media/high-cardinality id) in `xfactory/avatar_runtime/telemetry.py` (FR-033, SC-007) — depends on T006
- [x] T010 [P] Implement in-memory `FakeProvider` (create / sideband-open / sideband-verified / hangup) and fail-closed policy/consent/operation/usage fixtures in `tests/avatar_runtime/fakes/` (design D2/D6)
- [x] T011 Implement the in-process `runtime.py` assembly wiring ports + modules, with `destroy()` creating no durable state, in `xfactory/avatar_runtime/runtime.py` (FR-001/FR-003) — depends on T005–T009
- [x] T012 Implement `tests/avatar_runtime/conftest.py` fixtures (manual clock, id source, fake provider, authority fixtures) + seed recording — depends on T007, T008, T010

**Checkpoint**: Foundation ready — user-story implementation can begin.

---

## Phase 3: User Story 1 — Deterministic proof of race-sensitive protocol behavior (Priority: P1) 🎯 MVP

**Goal**: Prove every race-sensitive AVC invariant (broker outcomes, retry idempotency, two-channel
media authorization, single-log ordering, snapshot recovery, control-lease loss, consent revocation,
quota/duration, credential-free terminal replay) with deterministic tests that touch no wall time,
randomness, network, persistence, or Hermes.

**Independent Test**: Run `pytest tests/avatar_runtime -p randomly` over multiple recorded seeds; all
protocol tests pass identically across repeats and reorders with in-memory ports only (SC-003/004).

### Runtime modules for User Story 1

- [ ] T013 [P] [US1] Implement `LogicalSession` state machine (epoch, ≤1 instance, ≤1 pending/connected leg, fresh-resume replacement) in `xfactory/avatar_runtime/session.py` (FR-011/FR-015/FR-017)
- [ ] T014 [P] [US1] Implement `MediaAttempt` state machine + transition tables (reject unknown predecessor / terminal mutation) in `xfactory/avatar_runtime/attempt.py` (data-model.md, design D4)
- [ ] T015 [US1] Implement AVC-02 total preflight (`grant|denial|terminal`, exact-offer idempotency, changed-offer conflict, tenant caps, `second_instance_denied`) in `xfactory/avatar_runtime/broker.py` (FR-012/013/014/017) — depends on T013, T014
- [ ] T016 [P] [US1] Implement process-memory-only TTL grant retry cache + credential-free terminal record with cache destruction on connect/expiry/abandon/revoke in `xfactory/avatar_runtime/grant_cache.py` (FR-013/016, SC-009)
- [ ] T017 [P] [US1] Implement control lease (epoch fencing, transport-identity `lease_ack` check, heartbeat, expiry, reconnect credential rotation) in `xfactory/avatar_runtime/control.py` (FR-019/021/022)
- [ ] T018 [US1] Implement the two-channel media-authorization barrier (single `media_authorized` only on sideband + identity-matched `lease_ack`; readiness timeout; idempotent termination) in `xfactory/avatar_runtime/media_authz.py` (FR-018/020) — depends on T014, T017
- [ ] T019 [P] [US1] Implement the single sequenced event log + producer-authority checks in `xfactory/avatar_runtime/events.py` (FR-026)
- [ ] T020 [US1] Implement command validation (lease/epoch/allowlist/expected-revision) + dedupe by command id in `xfactory/avatar_runtime/commands.py` (FR-024/025) — depends on T019
- [ ] T021 [US1] Implement the atomic snapshot barrier `B` (projection through B, bounded post-barrier buffer, ordered drain, overflow restart, no historical replay) in `xfactory/avatar_runtime/snapshots.py` (FR-027) — depends on T019
- [ ] T022 [P] [US1] Implement fail-closed policy resolution (required purposes, speech gates, retention, quotas, confirmation rules) in `xfactory/avatar_runtime/authority.py` (FR-010/028)
- [ ] T023 [US1] Implement versioned consent binding + invalidation → revocation within the injected 5-second bound in `xfactory/avatar_runtime/consent.py` (FR-023/030) — depends on T017, T018
- [ ] T024 [P] [US1] Implement the fixture operation handler (external-operation idempotency key, confirmation validity) in `xfactory/avatar_runtime/operations.py` (FR-029)
- [ ] T025 [P] [US1] Implement in-memory append-only usage records + quota/duration outcomes in `xfactory/avatar_runtime/usage.py` (FR-032)
- [ ] T026 [US1] Implement all-session + per-profile kill switches (deny new; revoke leases per policy) in `xfactory/avatar_runtime/killswitch.py` (FR-031) — depends on T017

### Deterministic tests for User Story 1

- [ ] T027 [P] [US1] `tests/avatar_runtime/test_broker_preflight.py` — grant|denial|terminal totality, second-instance denial (ARR-004-S05, FR-012/017)
- [ ] T028 [P] [US1] `tests/avatar_runtime/test_media_attempts.py` — lifecycle, fresh-resume replacement, one-leg (ARR-004-S03, FR-011/015)
- [ ] T029 [P] [US1] `tests/avatar_runtime/test_avc02_outcomes.py` — exact-offer idempotency, changed-offer conflict, caps/duration (ARR-004-S01/S02, FR-013/014)
- [ ] T030 [P] [US1] `tests/avatar_runtime/test_grant_retry.py` — retry cache, credential-free terminal replay, cache destruction (ARR-004-S04, SC-009)
- [ ] T031 [P] [US1] `tests/avatar_runtime/test_control_leases.py` — lease/epoch/heartbeat/expiry/reconnect rotation (ARR-005-S03/S04, FR-021/022)
- [ ] T032 [P] [US1] `tests/avatar_runtime/test_media_authorization.py` — two-channel barrier, sideband timeout, hostile identity (ARR-005-S01/S02, FR-018/019/020)
- [ ] T033 [P] [US1] `tests/avatar_runtime/test_commands.py` — validation, dedupe, revision guard (ARR-006-S01/S02, FR-024/025)
- [ ] T034 [P] [US1] `tests/avatar_runtime/test_event_log.py` — single sequence, producer-authority rejection (ARR-006-S05, FR-026)
- [ ] T035 [P] [US1] `tests/avatar_runtime/test_snapshots.py` — barrier B, ordered drain, overflow restart (ARR-006-S03/S04, FR-027)
- [ ] T036 [P] [US1] `tests/avatar_runtime/test_authority_ports.py` — fail-closed policy/consent/operation, purpose mapping (ARR-003-S03/ARR-007-S01, FR-010/028)
- [ ] T037 [P] [US1] `tests/avatar_runtime/test_consent_revocation.py` — invalidation → revoke within injected 5s (ARR-005-S05, FR-023)
- [ ] T037a [P] [US1] `tests/avatar_runtime/test_operation_confirmation.py` — a stale/superseded confirmation blocks the fixture operation and requires a fresh confirmation; execution is idempotent under the external-operation key (ARR-007-S02, FR-029) — depends on T024
- [ ] T038 [P] [US1] `tests/avatar_runtime/test_usage.py` — quota/duration outcomes, attributed credential-free records (ARR-007-S05, FR-032)
- [ ] T039 [P] [US1] `tests/avatar_runtime/test_kill_switches.py` — all-session/per-profile deny + lease revoke (ARR-007-S03, FR-031)
- [ ] T040 [P] [US1] `tests/avatar_runtime/test_determinism.py` — clock-driven transitions, order-independence over recorded seeds (ARR-003-S01/S02, ARR-008-S02, SC-003/004)

**Checkpoint**: US1 is a fully functional, independently testable MVP proving the protocol invariants.

---

## Phase 4: User Story 2 — Parallel implementation with ordered final conformance (Priority: P2)

**Goal**: Build/test against the provisional `avatar-client-parallel-v1` baseline before the kernel
releases, then realize by pinning the released kernel, disabling the provisional seam, and proving
acceptance-ID conformance with no drift.

**Independent Test**: With canonical schemas unpublished, run the suite through the provisional adapter,
confirm it claims no canonical contract, and confirm `check_conformance.py` binds every applicable
scenario; then simulate realization and confirm a bare tag / provisional-vs-canonical divergence fails.

- [ ] T041 [P] [US2] Implement the test-only `avatar-client-parallel-v1` provisional adapter (unreachable from the package) in `tests/avatar_runtime/provisional/` (FR-004, ARR-002-S01)
- [ ] T042 [US2] Implement acceptance sourcing (read-only) in `tests/avatar_runtime/conformance/acceptance_source.py` reading BOTH required-set sources with source-commit + digest verification: (a) the runtime ARR map `openspec/changes/implement-avatar-reference-runtime/supporting-docs/avatar-reference-runtime-acceptance-map.yaml` (34 ARR) and (b) the client ACR baseline map `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml` (applicable ACR). Record each map's content digest in `realization-pin.yaml` so the required-set stays content-addressed after the change dirs archive on landing (FR-034/FR-034a) — depends on T041
- [ ] T043 [US2] Author `tests/avatar_runtime/conformance/scenario-test-map.yaml` binding every `ARR-*` and every applicable `ACR-*` scenario to exactly ONE entry whose disposition is `mapped` (a LIST of one-or-more test node ids — dual-story coverage of a scenario is a single entry listing all its nodes, never duplicate entries), `non_applicable` (with rationale), or `gate` (a checker/gate evidence reference for non-pytest evidence) (FR-034, SC-001/002) — depends on T027–T040, T037a, T042
- [ ] T044 [US2] Implement `tests/avatar_runtime/conformance/check_conformance.py` failing on missing / duplicate / dangling / skipped-required / unknown mappings (FR-034) — depends on T043
- [ ] T045 [P] [US2] Author the `tests/avatar_runtime/conformance/realization-pin.yaml` schema/skeleton (`schema_version` + `kind`, five release coordinates + conformance-result fields; populated at realization) (FR-005, SC-006)
- [ ] T046 [US2] Add realization-pin validation to the checker (bare tag → fail; require `provisional_adapter_disabled: true` and all five coordinates) (FR-005, ARR-002-S03) — depends on T044, T045
- [ ] T047 [US2] Implement the final-conformance flow (provisional adapter disabled, run against released canonical fixtures, fail on canonical-vs-provisional divergence) as a `--final` mode in `tests/avatar_runtime/conformance/check_conformance.py` (FR-035, ARR-008-S03) — depends on T044
- [ ] T048 [P] [US2] Implement accepted-kernel-variance handling: reopen only the mapped tests/adapters named by the variance, editing no sibling files (FR-006, ARR-002-S04)
- [ ] T049 [P] [US2] `tests/avatar_runtime/conformance/test_check_conformance.py` — assert the checker fails on each of unmapped/duplicate/dangling/skipped/unknown (ARR-008-S01, FR-034)

**Checkpoint**: US2 makes coverage machine-checkable and realization gated, independently of US3.

---

## Phase 5: User Story 3 — Non-deployable, fail-closed, redacted safety boundary (Priority: P3)

**Goal**: Let a governance/security reviewer confirm — from automated output alone — no deployment
surface, stdlib-only core, no provisional reach, fail-closed authority, and redacted telemetry.

**Independent Test**: Run `scripts/validate-avatar-runtime.py` and the boundary/redaction tests; confirm
zero deployment surfaces, zero third-party runtime imports, zero provisional reach, and zero protected
content in telemetry.

- [ ] T050 [P] [US3] Implement the pure stdlib AST / import / export / file-surface scanner in `tests/avatar_runtime/boundary/scanner.py` (FR-004a, execution-free)
- [ ] T051 [US3] Implement `tests/avatar_runtime/boundary/test_package_boundary.py` asserting no listener/app-factory/deployment/persistence/SDK/credential surface, stdlib-only runtime, and no provisional import (FR-001/004, ARR-001-S01, ARR-002-S02, SC-005/010) — depends on T050
- [ ] T052 [US3] Implement the standalone execution-free gate `scripts/validate-avatar-runtime.py` importing `boundary/scanner.py` (FR-004a, Clarifications Q4) — depends on T050
- [ ] T053 [US3] Add the single `scripts/validate-avatar-runtime.py` line to the README validator index (declared governance exception; no other sibling path touched) in `README.md` (FR-036, SC-008)
- [ ] T054 [P] [US3] `tests/avatar_runtime/test_redaction_telemetry.py` — redaction validator rejects SDP/credential/payload/media/high-cardinality id and does not publish (ARR-007-S04, FR-033, SC-007)
- [ ] T055 [P] [US3] `tests/avatar_runtime/boundary/test_live_provider_rejected.py` — reference code attempting provider-key load / network call fails and routes to a live-runtime change (ARR-001-S02, FR-002)
- [ ] T056 [P] [US3] `tests/avatar_runtime/boundary/test_state_discarded.py` — runtime destruction requires no migration/cleanup/secret-grant recovery (ARR-001-S03, FR-003, SC-009)
- [ ] T057 [P] [US3] `tests/avatar_runtime/test_failclosed_inspection.py` — purpose-mapping-absent denial before provider creation (ARR-007-S01) and kill-switch deny/lease-revoke (ARR-007-S03), reusing US1 modules. NOTE (F1): ARR-007-S01/S03 are also covered by US1 tests (T036/T039); `scenario-test-map.yaml` MUST record each as a SINGLE entry listing both the US1 and US3 test nodes, not duplicate entries.

**Checkpoint**: US3 provides the reviewer-facing boundary + redaction guarantees, independently runnable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Whole-feature gate, coverage, and evidence.

- [ ] T058 Run the Principle V feature gate (`scripts/validate-avatar-runtime.py` + `pytest tests/avatar_runtime -p randomly` + `check_conformance.py`) and record the used seeds in `realization-pin.yaml`
- [ ] T059 [P] Run the `quickstart.md` validation end-to-end and reconcile expected outcomes
- [ ] T060 Run `git diff --check` and confirm 0 canonical-contract / F0 / UI / DomainxFactory / deployment / release-metadata files changed (FR-036, SC-008); record this gate result as the mapped evidence for `ARR-008-S04` in `scenario-test-map.yaml` (evidence type: `gate`) (E1)
- [ ] T060a [P] Implement a suite-wide test-lint guard scanning `tests/avatar_runtime/` for wall-clock time / randomness / network / filesystem-persistence usage (strengthens SC-004; complements the package boundary scanner, which targets the runtime package not the tests) in `tests/avatar_runtime/boundary/test_suite_hygiene.py`
- [ ] T061 [P] Verify mapping completeness: all 34 `ARR-*` scenarios mapped and every applicable `ACR-*` mapped or dispositioned with rationale (SC-001/002)
- [ ] T062 [P] Cross-check FR/SC coverage against `scenario-test-map.yaml`; add/adjust non-applicability dispositions with rationale where needed
- [ ] T063 Final determinism sweep across multiple recorded seeds via `tests/avatar_runtime/test_determinism.py`; record the seeds in `tests/avatar_runtime/conformance/realization-pin.yaml` and confirm the reproducible-failing-seed procedure from reported output (SC-003)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup — **blocks all user stories**.
- **US1 (Phase 3)**: depends on Foundational. MVP.
- **US2 (Phase 4)**: depends on Foundational; needs the US1 tests (T027–T040, T037a) to bind in `scenario-test-map.yaml` (T043).
- **US3 (Phase 5)**: depends on Foundational; boundary tooling (T050–T053) is fully independent; the fail-closed/redaction tests (T054–T057) reuse Foundational + US1 modules.
- **Polish (Phase 6)**: depends on all desired stories complete.

### User Story Dependencies

- **US1 (P1)**: independent after Foundational — the MVP.
- **US2 (P2)**: independent after Foundational; its `scenario-test-map.yaml` references US1 test node IDs (a one-directional mapping dependency, not a code dependency).
- **US3 (P3)**: boundary tooling independent after Foundational; redaction/fail-closed proof tests integrate US1 modules but remain independently runnable.

### Within Each User Story

- Runtime modules before the tests that exercise them; `broker` after `session`+`attempt`; `media_authz` after `attempt`+`control`; `commands`/`snapshots` after `events`; `consent`/`killswitch` after `control`.
- US2: adapter → acceptance source → scenario-test-map → checker → realization-pin validation.
- US3: scanner → boundary test + gate script → README index line.

### Parallel Opportunities

- Setup: T002, T003, T004 in parallel.
- Foundational: T005, T006, T007, T008, T010 in parallel (T009 after T006; T011 after T005–T009; T012 after T007/T008/T010).
- US1 modules: T013, T014, T016, T017, T019, T022, T024, T025 in parallel; then T015/T018/T020/T021/T023/T026 per their deps.
- US1 tests: T027–T040 + T037a all [P] (distinct files) once their modules exist.
- US2: T041, T045, T048, T049 [P]; T042→T043→T044→T046/T047 sequential.
- US3: T050 then T054, T055, T056, T057 [P]; T051/T052/T053 per deps.
- Polish: T059, T060a, T061, T062 [P].
- Once Foundational is done, US1 / US2 / US3 can be staffed in parallel by different developers.

---

## Parallel Example: User Story 1 tests

```bash
# After US1 modules exist, launch the deterministic tests together (distinct files):
Task: "test_broker_preflight.py"      # T027
Task: "test_media_attempts.py"        # T028
Task: "test_avc02_outcomes.py"        # T029
Task: "test_grant_retry.py"           # T030
Task: "test_control_leases.py"        # T031
Task: "test_media_authorization.py"   # T032
Task: "test_commands.py"              # T033
Task: "test_event_log.py"             # T034
Task: "test_snapshots.py"             # T035
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1 (Setup) → Phase 2 (Foundational — blocks all).
2. Complete Phase 3 (US1): runtime modules + deterministic tests.
3. **STOP and VALIDATE**: run the suite over multiple seeds; the protocol invariants are proven with no ambient dependency. This is a demonstrable MVP even before conformance tooling exists.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 → the deterministic proof (MVP).
3. US2 → machine-checkable acceptance-ID conformance + ordered realization gating.
4. US3 → the non-deployable / fail-closed / redacted boundary guarantees.
5. Polish → full gate, seed recording, diff/ownership verification.

### Parallel Team Strategy

After Foundational: Developer A → US1 (largest); Developer B → US2 conformance tooling (mapping filled once US1 test IDs stabilize); Developer C → US3 boundary + redaction. Stories integrate independently.

---

## Notes

- `[P]` = different files, no incomplete-task dependency.
- Every task names an exact path; runtime tasks touch only `xfactory/avatar_runtime/`, tests touch only `tests/avatar_runtime/`, and the sole out-of-tree writes are `scripts/validate-avatar-runtime.py` (T052) + its README index line (T053) — the declared governance exception.
- The runtime core stays stdlib-only; only tests/validator use pinned `pytest`/`pytest-randomly`/`PyYAML`/`jsonschema`.
- Every behavioral test maps to its `ARR-*`/`ACR-*` scenario(s) via `scenario-test-map.yaml`; a missing/duplicate/dangling/skipped-required/unknown mapping fails conformance.
- Commit after each task or logical group; run the Principle V gate before every push.
