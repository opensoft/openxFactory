# Tasks: Avatar Brokered-Call F0 Feasibility Experiment

**Input**: Design documents from `specs/002-avc-f0-feasibility/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: INCLUDED — the feature's Definition of Done (SC-013) explicitly requires offline
self-tests and redaction tests, so test tasks are first-class here.

**Organization**: Grouped by user story (US1–US5 from spec.md) so each is an independently
testable increment. The independent test for every story is its **offline** test set — a run
with no lab key yields a schema-valid `INCONCLUSIVE` record, which satisfies feature completion
(SC-013). A live `PASS` is never required for completion and never represents provider
qualification.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: parallelizable (different files, no dependency on an incomplete task)
- **[Story]**: US1…US5 (user-story phases only; Setup/Foundational/Polish carry no story label)

## Owned surface & guardrails (apply to every task)

- Code lives ONLY under `experiments/avatar-brokered-call/`.
- Committed run evidence goes ONLY to `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` (no second copy — Q5/FR-021/SC-011).
- The two schemas (`f0-results.schema.yaml`, `f0-interface-impact.schema.yaml`) are 002-owned and live at `experiments/avatar-brokered-call/schemas/`; `f0-results.schema.yaml` stays byte-identical (sha256 `a52f2abe…`) to the registered supporting-docs copy (drift-guarded).
- Never edit `openspec/` supporting-docs/contracts, reference-runtime, UI, DomainxFactory, or deployment files.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and pinned, reproducible tooling.

- [x] T001 Create the project tree (`src/avatar_f0/`, `src/avatar_f0/trials/`, `tests/offline/`, `tests/live/`, `schemas/`) under `experiments/avatar-brokered-call/` per plan.md
- [x] T002 Add `experiments/avatar-brokered-call/.python-version` (3.12) and `pyproject.toml` declaring aiortc, websockets, httpx, jsonschema, PyYAML, and the pinned offline TTS engine
- [x] T003 [P] Generate `experiments/avatar-brokered-call/requirements.lock` with hashes (its digest feeds the candidate-profile `dependency_lock_sha256`)
- [x] T004 [P] Configure pytest + lint/format settings in `experiments/avatar-brokered-call/pyproject.toml`
- [x] T005 [P] Place `experiments/avatar-brokered-call/schemas/f0-results.schema.yaml` byte-identical to the registered supporting-docs copy
- [x] T006 [P] Author `experiments/avatar-brokered-call/schemas/f0-interface-impact.schema.yaml` from `contracts/f0-interface-impact.schema.yaml` (carries `schema_version` + `kind`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The story-neutral harness substrate every trial needs.

**⚠️ CRITICAL**: No user-story phase can complete until this phase is done.

- [x] T007 [P] Implement the monotonic clock + marker recorder in `experiments/avatar-brokered-call/src/avatar_f0/clock.py` (FR-011; t=0 at provider-create acceptance)
- [x] T008 [P] Implement the env-only `OPENAI_API_KEY` credential loader in `experiments/avatar-brokered-call/src/avatar_f0/credential.py` (FR-001; reject non-env sources; never log/print)
- [x] T009 [P] Implement the `RunConfig` model (fields per data-model.md) in `experiments/avatar-brokered-call/src/avatar_f0/config.py`
- [x] T010 [P] Implement the immutable candidate profile + `profile_digest` in `experiments/avatar-brokered-call/src/avatar_f0/candidate.py` (FR-002)
- [x] T011 [P] Implement the deterministic audio-fixture generator + byte digest in `experiments/avatar-brokered-call/src/avatar_f0/fixture.py` (FR-002/Q7; no committed binary) — implementation note: pin the specific offline TTS engine + voice + version and fold it into the candidate `profile_digest`
- [x] T012 [P] Implement the in-harness simulated control/lease stub in `experiments/avatar-brokered-call/src/avatar_f0/control_stub.py` (FR-007/Q6; no Hermes/external control-plane)
- [x] T013 [P] Implement the sideband WSS client in `experiments/avatar-brokered-call/src/avatar_f0/sideband.py` (open vs verified markers)
- [x] T014 Implement brokered call creation + call-ID registry in `experiments/avatar-brokered-call/src/avatar_f0/broker.py` (register call ID before next step) — depends on T008
- [x] T015 Implement the WebRTC media peer + held-answer gate in `experiments/avatar-brokered-call/src/avatar_f0/media.py` (FR-007; answer withheld until authorized) — depends on T012, T013
- [x] T016 [P] Implement the bounded cleanup registry/routine in `experiments/avatar-brokered-call/src/avatar_f0/cleanup.py` (FR-005; terminate every known call ID)
- [ ] T017 Implement the CLI entrypoint skeleton (config → run → evidence wiring, exit codes) in `experiments/avatar-brokered-call/src/avatar_f0/cli.py` — depends on T009

**Checkpoint**: Substrate ready — user-story phases can begin.

---

## Phase 3: User Story 1 - Complete brokered-call trial matrix (Priority: P1) 🎯 MVP

**Goal**: Prove ordering, failure-containment, and retry behavior across the trial matrix
(F0-A baseline, F0-B delayed-sideband, F0-C sideband-failure, F0-E exact-retry, F0-F
changed-retry) plus cross-cutting interrupted-run cleanup.

**Independent Test**: Offline runs (provider double) show the ordering invariant holds, sideband
failure authorizes no media and terminates, retries neither duplicate a call nor disclose a
prior answer, and an interruption terminates every known call ID.

### Tests for User Story 1

- [ ] T018 [P] [US1] Offline test — baseline ordering invariant (`sideband_verified ≤ answer_released ≤ lease_ack ≤ media_authorized ≤ answer_applied ≤ first_input_sent`) in `experiments/avatar-brokered-call/tests/offline/test_baseline_ordering.py` (US1-S1/FR-008/SC-001)
- [ ] T019 [P] [US1] Offline test — sideband-failure authorizes no media, applies no answer, terminates call in `experiments/avatar-brokered-call/tests/offline/test_sideband_failure.py` (US1-S3/FR-009/SC-004)
- [ ] T020 [P] [US1] Offline test — exact-retry at-most-one call; changed-retry no prior-answer disclosure and no second call in `experiments/avatar-brokered-call/tests/offline/test_retry.py` (US1-S4/S5/FR-010/SC-006)
- [ ] T021 [P] [US1] Offline test — interrupted run terminates every known call ID and records outcome in `experiments/avatar-brokered-call/tests/offline/test_interrupt_cleanup.py` (US1-S6)

### Implementation for User Story 1

- [ ] T022 [US1] Implement the shared trial-runner scaffold + deterministic `F0-<A–F>-NN` IDs and the per-group run-count orchestration (F0-A=20; F0-B–F0-F=10; 70 total) in `experiments/avatar-brokered-call/src/avatar_f0/trials/base.py` (FR-006) — depends on T015, T012, T016
- [ ] T023 [P] [US1] Implement the F0-A baseline runner (held answer, ordered authorization, single call) in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0a_baseline.py` (FR-006/FR-008)
- [ ] T024 [P] [US1] Implement the F0-B delayed-sideband runner (injected delay within deadline) in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0b_delayed.py`
- [ ] T025 [P] [US1] Implement the F0-C sideband-failure runner (no media, terminate; hosts the readiness-timeout path used by US4) in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0c_sideband_failure.py`
- [ ] T026 [P] [US1] Implement the F0-E exact-retry runner in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0e_exact_retry.py`
- [ ] T027 [P] [US1] Implement the F0-F changed-retry runner in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0f_changed_retry.py`
- [ ] T028 [US1] Implement ordering / retry / no-media assertions + the cross-cutting interrupted-run cleanup assertion in `experiments/avatar-brokered-call/src/avatar_f0/assertions.py` (FR-006/FR-008/FR-009/FR-010) — depends on T023–T027

**Checkpoint**: US1 trial matrix runs and asserts offline against a provider double.

---

## Phase 4: User Story 2 - Isolated, tenant-data-free, reproducible environment (Priority: P1)

**Goal**: Refuse unsafe/unpinned runs before any provider call, and report INCONCLUSIVE (never
infer) when the candidate or acceptance map is unavailable/mismatched.

**Independent Test**: Bad configs are rejected at preflight; a candidate-unavailable run and an
absent/mismatched acceptance map both yield INCONCLUSIVE with no inference and no placeholder IDs.

### Tests for User Story 2

- [ ] T029 [P] [US2] Offline test — preflight rejects tenant data, enabled tools, key-in-args/tracked files, readiness > 5000 ms, non-lab/unpinned profile in `experiments/avatar-brokered-call/tests/offline/test_preflight.py` (US2-S2/SC-009)
- [ ] T030 [P] [US2] Offline test — candidate unavailable / API-shape mismatch → INCONCLUSIVE, no inferred behavior in `experiments/avatar-brokered-call/tests/offline/test_candidate_unavailable.py` (US2-S3/FR-004)
- [ ] T031 [P] [US2] Offline test — acceptance-map digest gate: match → ACR IDs loaded; absent/mismatch/wrong baseline → INCONCLUSIVE, no placeholders in `experiments/avatar-brokered-call/tests/offline/test_acceptance_map.py` (FR-018/Q3)

### Implementation for User Story 2

- [ ] T032 [US2] Implement preflight rejection rules + safe-config-records-only-digests in `experiments/avatar-brokered-call/src/avatar_f0/config.py` (FR-001/FR-003/SC-009) — depends on T009
- [ ] T033 [P] [US2] Implement the digest-verified acceptance-map reader → concrete ACR IDs (ACR-003/008/011/012) in `experiments/avatar-brokered-call/src/avatar_f0/acceptance_map.py` (FR-018/Q3)
- [ ] T034 [US2] Wire candidate-unavailable / API-shape → INCONCLUSIVE into the broker/run flow in `experiments/avatar-brokered-call/src/avatar_f0/broker.py` (FR-004) — depends on T014

**Checkpoint**: US2 safety gates and reproducibility guards hold offline.

---

## Phase 5: User Story 3 - Redacted terminal evidence & variance handoff (Priority: P1)

**Goal**: Emit schema-valid, redacted evidence to the sole evidence path with correct
PASS/FAIL/INCONCLUSIVE classification and an always-present interface-impact report citing
digest-verified ACR IDs.

**Independent Test**: With synthetic trial inputs, the writer produces schema-valid artifacts
in the change evidence dir only; injected prohibited content fails closed; classification and
variance citation match the rules.

### Tests for User Story 3

- [ ] T035 [P] [US3] Offline test — redaction allowlist + prohibited-content scan fail closed (run FAIL, no commit, exit 3) across evidence/logs/traces in `experiments/avatar-brokered-call/tests/offline/test_redaction.py` (FR-017/SC-007)
- [ ] T036 [P] [US3] Offline test — `f0-results.json` validates against the owned schema (zero errors) and the drift-guard equals the registered digest in `experiments/avatar-brokered-call/tests/offline/test_schema_valid.py` (SC-008)
- [ ] T037 [P] [US3] Offline test — classification derivation (PASS needs all mandatory pass; contrary ⇒ FAIL; missing ⇒ INCONCLUSIVE; a p95/ceiling miss is never averaged away) in `experiments/avatar-brokered-call/tests/offline/test_classify.py` (FR-016)
- [ ] T038 [P] [US3] Offline test — interface-impact emitted on every run (empty on clean pass); variances cite concrete ACR IDs and validate against the schema in `experiments/avatar-brokered-call/tests/offline/test_interface_impact.py` (FR-018/SC-010)

### Implementation for User Story 3

- [ ] T039 [P] [US3] Implement the redaction allowlist writer + prohibited-content scan in `experiments/avatar-brokered-call/src/avatar_f0/redaction.py` (FR-017/SC-007)
- [ ] T040 [US3] Implement the PASS/FAIL/INCONCLUSIVE classification derivation in `experiments/avatar-brokered-call/src/avatar_f0/classify.py` (FR-016) — depends on T028
- [ ] T041 [US3] Implement the evidence writer for `f0-results.json` + `f0-results.md` (with `report_sha256`), written directly/atomically to the change `evidence/` dir only, in `experiments/avatar-brokered-call/src/avatar_f0/evidence.py` (FR-015/Q5/SC-011) — depends on T039, T040
- [ ] T042 [US3] Implement the `f0-interface-impact.yaml` writer citing digest-verified ACR IDs, and record the acceptance-map `source_commit` + `content_sha256` into the evidence's `acceptance_map` block, in `experiments/avatar-brokered-call/src/avatar_f0/evidence.py` (FR-018) — depends on T033, T041

**Checkpoint**: US3 produces publishable, schema-valid, correctly classified evidence offline.

---

## Phase 6: User Story 4 - Readiness & revocation timing (Priority: P2)

**Goal**: Measure the neutral timing bounds (3000 ms default / 5000 ms ceiling, first-playable
p95 ≤ 2000 ms, revocation terminal ≤ 5000 ms) and prove the readiness-timeout and revocation
paths, keeping request vs observed offsets distinct.

**Independent Test**: With synthetic monotonic markers, metric summaries and bound checks are
correct; the F0-C readiness-timeout path withholds/terminates; F0-D revocation records separate
offsets and an unconfirmed terminal is FAIL/INCONCLUSIVE, never success.

### Tests for User Story 4

- [ ] T043 [P] [US4] Offline test — p50/p95/max summary math for the three metrics in `experiments/avatar-brokered-call/tests/offline/test_metrics.py` (SC-002/SC-003/SC-005)
- [ ] T044 [P] [US4] Offline test — readiness-timeout (F0-C path): withhold authorization, terminate, fail if any media/answer occurred in `experiments/avatar-brokered-call/tests/offline/test_readiness_timeout.py` (FR-012/US4-S2)
- [ ] T045 [P] [US4] Offline test — revocation records separate revocation/hangup/terminal offsets and terminal ≤ 5000 ms; unconfirmed ⇒ FAIL/INCONCLUSIVE in `experiments/avatar-brokered-call/tests/offline/test_revocation.py` (FR-013/FR-014/US4-S4)

### Implementation for User Story 4

- [ ] T046 [P] [US4] Implement the metrics summary (`sideband_ready_ms`, `first_playable_after_authorized_ms`, `hangup_to_terminal_ms`) in `experiments/avatar-brokered-call/src/avatar_f0/metrics.py` (SC-002/SC-003/SC-005) — depends on T007
- [ ] T047 [US4] Add the readiness-timeout threshold assertion to the F0-C path in `experiments/avatar-brokered-call/src/avatar_f0/assertions.py` (FR-012) — depends on T025, T028
- [ ] T048 [P] [US4] Implement the F0-D revocation runner with separate revocation/hangup/terminal offsets in `experiments/avatar-brokered-call/src/avatar_f0/trials/f0d_revocation.py` (FR-013/FR-014) — depends on T022
- [ ] T049 [US4] Fold timing-bound checks (p95/ceiling, never averaged) into classification in `experiments/avatar-brokered-call/src/avatar_f0/classify.py` (SC-002/SC-003) — depends on T040, T046

**Checkpoint**: US4 timing/revocation measurement and bounds hold offline.

---

## Phase 7: User Story 5 - Non-qualification boundary & Definition of Done (Priority: P2)

**Goal**: Guarantee a no-key run completes as a valid INCONCLUSIVE terminal record (feature
completion), and that the result never enables live/production use and never escapes the owned
write locations.

**Independent Test**: A no-key run exits 0 with a schema-valid INCONCLUSIVE record, zero
provider calls, and zero fabricated artifacts; a scope-isolation check confirms nothing is
written outside the two owned locations.

### Tests for User Story 5

- [ ] T050 [P] [US5] Offline test — no-key run → INCONCLUSIVE, exit 0, zero provider calls, zero fabricated artifacts (DoD) in `experiments/avatar-brokered-call/tests/offline/test_no_key_completion.py` (SC-013/Q1)
- [ ] T051 [P] [US5] Offline test — scope-isolation guard: a run writes nothing outside `experiments/avatar-brokered-call/` and the change `evidence/` dir in `experiments/avatar-brokered-call/tests/offline/test_scope_isolation.py` (SC-011)

### Implementation for User Story 5

- [ ] T052 [US5] Implement the no-key / completion path (terminal INCONCLUSIVE, exit 0, no fabricated artifacts; completion ≠ qualification) in `experiments/avatar-brokered-call/src/avatar_f0/cli.py` (SC-013/Q1/FR-019) — depends on T017, T041
- [ ] T053 [P] [US5] Enforce the evidence write-path allowlist and document the non-qualification boundary (no profile promotion / no live-prod media) in `experiments/avatar-brokered-call/src/avatar_f0/evidence.py` and `experiments/avatar-brokered-call/README.md` (FR-019/FR-020/FR-021/SC-011/SC-012)

**Checkpoint**: US5 completion and boundary guarantees hold offline.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finalize docs, run the full gate, and (only if a key is present) execute the live
matrix.

- [ ] T054 [P] Finalize `experiments/avatar-brokered-call/README.md` run/redaction/safety notes and align with `specs/002-avc-f0-feasibility/quickstart.md`
- [ ] T055 Run the full offline suite green (`pytest experiments/avatar-brokered-call/tests/offline`) — the DoD offline gate (SC-013)
- [ ] T056 [P] Add the live suite (skipped → INCONCLUSIVE when `OPENAI_API_KEY` absent) in `experiments/avatar-brokered-call/tests/live/`
- [ ] T057 Execute the validation gate: repo-local validators, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, `git diff --check`, supporting-doc hash verification, and confirm no canonical-contract/reference-runtime/UI/DomainxFactory/deployment file changed (SC-011)
- [ ] T058 Execute the live trial matrix when `OPENAI_API_KEY` is present and write terminal evidence to the change `evidence/` dir; otherwise commit the schema-valid INCONCLUSIVE record — completion per SC-013 — depends on T055, T057

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (P1)**: no dependencies.
- **Foundational (P2)**: depends on Setup; BLOCKS all user stories.
- **User stories (P3–P7)**: depend on Foundational. US1/US2/US3 are all P1; US4/US5 are P2.
  Cross-story build dependencies (kept minimal): US3 classification consumes US1 assertions
  (T040←T028); US4 extends the F0-C runner and classification (T047←T025/T028, T049←T040/T046);
  US2 acceptance-map feeds US3's variance writer (T042←T033); US5 completion path consumes the
  US3 evidence writer (T052←T041). Each story's **offline tests** remain independently runnable.
- **Polish (P8)**: depends on the desired user stories; T058 depends on T055 + T057.

### Within each user story

- Tests are written first and must FAIL before implementation.
- Runners before assertions; assertions before classification; classification before evidence.

### Parallel opportunities

- Setup T003–T006 run in parallel.
- Foundational T007–T013 and T016 run in parallel (distinct files); T014/T015/T017 follow their deps.
- Every story's `[P]` tests (different files) run together; `[P]` runners within US1 (T023–T027) run together.
- Being P1, US1/US2/US3 can be staffed in parallel once Foundational completes (respecting the few cross-story deps above).

---

## Parallel Example: User Story 1

```bash
# Tests together (write first, expect FAIL):
Task: "Offline test — baseline ordering invariant (test_baseline_ordering.py)"
Task: "Offline test — sideband-failure no-media/terminate (test_sideband_failure.py)"
Task: "Offline test — exact/changed retry (test_retry.py)"
Task: "Offline test — interrupted-run cleanup (test_interrupt_cleanup.py)"

# Group runners together (distinct files):
Task: "F0-A baseline runner (trials/f0a_baseline.py)"
Task: "F0-B delayed-sideband runner (trials/f0b_delayed.py)"
Task: "F0-C sideband-failure runner (trials/f0c_sideband_failure.py)"
Task: "F0-E exact-retry runner (trials/f0e_exact_retry.py)"
Task: "F0-F changed-retry runner (trials/f0f_changed_retry.py)"
```

---

## Implementation Strategy

### MVP first (User Story 1)

1. Setup (Phase 1) → Foundational (Phase 2).
2. US1 (Phase 3) → validate the ordering/retry/containment proof offline against a provider double.
3. This is the core feasibility signal; stop and validate before layering timing/evidence.

### Incremental delivery

Foundation → US1 (matrix correctness) → US2 (safety/isolation) → US3 (evidence) → US4 (timing/
revocation) → US5 (completion/boundary) → Polish. Each story adds value; the offline suite stays
green throughout, so a no-key `INCONCLUSIVE` record is always a valid terminal state.

### Definition of Done (SC-013)

Complete = harness + full offline self-tests + redaction tests + a schema-valid terminal record
committed. Without a lab key the record is `INCONCLUSIVE` (T058 falls back), no provider call is
attempted, and nothing is fabricated. A live `PASS` is NOT required for completion, and
completion is never represented as provider qualification.

## Notes

- `[P]` = different files, no incomplete dependency.
- Evidence writes go to the change `evidence/` dir ONLY; schemas are 002-owned under
  `experiments/avatar-brokered-call/schemas/`; `f0-results.schema.yaml` is drift-guarded to the
  registered digest.
- Verify each story's offline tests fail before implementing; commit after each task or logical group.
