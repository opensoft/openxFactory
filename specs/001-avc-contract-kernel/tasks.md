---
description: "Task list for AVC Contract Kernel implementation"
---

# Tasks: AVC Contract Kernel

**Input**: Design documents from `specs/001-avc-contract-kernel/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/README.md

**Tests**: Conformance for this feature IS the fixture suite + the reference
validator (constitution Principle V). There is no separate application test
tier; fixtures are self-describing and executed by `validate-avatar-client.py`.
No TDD test tasks were requested, so none are added beyond the fixtures/validator
that the spec itself mandates (FR-019/FR-020).

**Organization**: Tasks are grouped by user story (spec.md US1–US5) to enable
independent implementation and testing. Final publication is an explicitly
**F0-gated, serialized** phase that is NOT runnable until F0 `PASS` evidence
exists.

**README disambiguation (analyze A1 / plan Design Note 4)**: three distinct
files — `contracts/avatar-client/README.md` (family contract index),
`contracts/README.md` (release-metadata index), repo-root `README.md`
(repository document index per Principle IV). Tasks name the exact file.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US5 (setup/foundational/realization/polish carry no story label)
- Paths are repo-root-relative; this change's exclusive write surface is
  `contracts/avatar-client/` and `scripts/validate-avatar-client.py`. Shared
  release metadata (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
  `contracts/README.md`) and the repo-root `README.md` doc-index link are touched
  ONLY in Phase 8 (serialized realization) with explicit-path staging.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Directory scaffolding and validator/config skeletons.

- [ ] T001 Create the `contracts/avatar-client/` tree (`registries/`, `fixtures/`, `redaction/`) per plan.md Project Structure
- [ ] T002 [P] Create `scripts/validate-avatar-client.py` skeleton (`#!/usr/bin/env python3`, `from __future__ import annotations`, guarded `jsonschema`/`yaml` imports, `ROOT = Path(__file__).resolve().parents[1]`, `argparse --strict`, accumulate-then-report, exit codes 0/1/2) per research §D1
- [ ] T003 [P] Scaffold `contracts/avatar-client/redaction/denylist-patterns.yaml` and `redaction/sentinels.yaml` (schema_version, kind, empty `patterns[]`/`sentinels[]`) per data-model §G

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared definitions, closed vocabularies, and the validator harness that ALL user stories depend on.

**⚠️ CRITICAL**: No user-story work can begin until this phase is complete.

- [ ] T004 Author `contracts/avatar-client/shared-definitions.schema.yaml` with every `$defs` group (actor/client/subject, workflow purpose, consent ref/version/purpose IDs, trace, session epoch, media leg/attempt, server-derived offer fingerprint, state revision, last-event sequence, media authorization, session outcomes, retention class, redaction, retry-equivalence) per data-model §A / research §D8 / spec §FR-003
- [ ] T005 Add the closed **speech-gate enum** (`confirmation_before_action` default, `streaming_monitor`, reserved `pre_speech_review`) to `contracts/avatar-client/shared-definitions.schema.yaml` and reference it from the relevant policy/speech fields — NOT a registry file (analyze A3) per spec §FR-015 / design Decision 11 — depends on T004 (same file)
- [ ] T006 [P] Author `registries/session-result-reasons.registry.yaml` — exactly the 15 ratified reasons per data-model §B / spec §FR-004
- [ ] T007 [P] Author `registries/events.registry.yaml` — types + producers + observation/authoritative class
- [ ] T008 [P] Author `registries/commands.registry.yaml` — types + revision-guarded flag
- [ ] T009 [P] Author `registries/retention-classes.registry.yaml` — ephemeral/telemetry/structured + reserved-forbidden classes
- [ ] T010 [P] Author `registries/capabilities.registry.yaml` — logical capability ids
- [ ] T011 [P] Author `registries/interaction-modes.registry.yaml` — includes `provider_vad`; excludes push-to-talk
- [ ] T012 [P] Author `registries/session-outcomes.registry.yaml` — terminal/lifecycle outcomes
- [ ] T013 [P] Author `registries/fallback-modes.registry.yaml` — text, human_handoff, retry_later, upgrade_required, none
- [ ] T014 [P] Author `registries/consent-purposes.registry.yaml` — exactly the 3 neutral purposes per spec §FR-005/§FR-015
- [ ] T015 Implement validator core harness in `scripts/validate-avatar-client.py` (artifact discovery, offline `$ref` store built from on-disk files, YAML loading, finding accumulation) — depends on T002, T004
- [ ] T016 Define the fixture-case envelope + `fixtures/index.yaml` convention (fields: case_id, target, target_kind, expect, scenario_ids, evidence_id, instance) per research §D2 / data-model §F

**Checkpoint**: Foundation ready — user stories can proceed (in parallel if staffed).

---

## Phase 3: User Story 1 - Publish the neutral AVC contract kernel (Priority: P1) 🎯 MVP

**Goal**: The eight AVC schemas exist over shared-definitions with closed registries, forming the canonical avatar-session surface.

**Independent Test**: All eight schema files resolve their `$ref`s offline, each declares id + `contract_schema_version`, every registry is closed, and schema enums set-equal their registry files (spec US1 Independent Test; SC-001/SC-004).

- [ ] T017 [P] [US1] Author `contracts/avatar-client/avc-01-session-request.schema.yaml` (transient `sdp_offer`; resume {logical session, epoch, last-applied seq}; body fields are references) per data-model §A / spec §FR-009
- [ ] T018 [P] [US1] Author `contracts/avatar-client/avc-02-session-result.schema.yaml` (discriminated `grant|denial|terminal`; inline capabilities on grant; media-authorization state + offer-fingerprint binding + heartbeat/lease fields; denial/terminal STRUCTURALLY cannot carry SDP/answer/credential) per spec §FR-007/§FR-006/§FR-010
- [ ] T019 [P] [US1] Author `contracts/avatar-client/avc-04-session-event.schema.yaml` (immutable; observation|authoritative + registered producer; AVC-05 transcript-segment payload) per spec §FR-002/§FR-011
- [ ] T020 [P] [US1] Author `contracts/avatar-client/avc-06-structured-confirmation.schema.yaml` (challenge fields; no binding digest) per spec §FR-013
- [ ] T021 [P] [US1] Author `contracts/avatar-client/avc-07-retention-profile.schema.yaml` (retention classes + reserved-forbidden; schema only, no instances) per spec §FR-001(Q2)/§FR-017
- [ ] T022 [P] [US1] Author `contracts/avatar-client/avc-08-persona-profile.schema.yaml` (immutable-per-session persona; schema only, no catalog instances) per spec §FR-001(Q2)/§FR-014
- [ ] T023 [P] [US1] Author `contracts/avatar-client/avc-11-session-command.schema.yaml` (command id idempotency key; optional `expected_state_revision`; opaque attachment reference only) per spec §FR-011/§FR-016
- [ ] T024 [P] [US1] Author `contracts/avatar-client/avc-12-state-snapshot.schema.yaml` (`last_event_sequence` cursor; `state_revision`; leased-control/recovery fields; client-local presentation non-authoritative) per spec §FR-011/§FR-012
- [ ] T025 [US1] Implement validator checks: draft-2020-12 schema validity, offline `$ref` resolution, and AVC-09/AVC-10 reserved-identifier guard in `scripts/validate-avatar-client.py` — depends on T015, T017–T024
- [ ] T026 [US1] Implement validator schema↔registry parity + exact-count checks (15 reasons / 3 purposes) + speech-gate enum closure in `scripts/validate-avatar-client.py` — depends on T025

**Checkpoint**: US1 independently testable — canonical schema + registry surface exists and self-validates.

---

## Phase 4: User Story 2 - Prove conformance with fixtures, validator, and acceptance map (Priority: P2)

**Goal**: Self-describing fixtures, the realized acceptance map, and the consolidated evidence register make every requirement/scenario traceable and machine-checkable, including dual redaction.

**Independent Test**: `validate-avatar-client.py --strict` passes valid fixtures, rejects invalid/adversarial/redaction-violating ones, and fails on any unmapped/duplicated/renamed/evidence-free scenario (spec US2 Independent Test; SC-002/SC-003/SC-005/SC-008).

- [ ] T027 [P] [US2] Realize `contracts/avatar-client/acceptance-map.yaml` from the supporting-docs map (17 requirements / 72 scenarios; ACR-*/SCO-*/RBG-*) per data-model §C / spec §FR-021
- [ ] T028 [US2] Author self-describing valid + invalid + boundary fixture cases for every schema under `contracts/avatar-client/fixtures/` and register them in `fixtures/index.yaml` per spec §FR-019 / data-model §F — depends on T016, T017–T024
- [ ] T029 [US2] Author compatibility + unknown-field + unknown-authority fixture cases (ACR-001-S01/S02/S03, event-producer misuse) and index them per spec §FR-008 — depends on T028
- [ ] T030 [US2] Author redaction + adversarial fixture cases per schema and per owned scenario using ONLY bounded sentinels from `redaction/sentinels.yaml`, and index them — depends on T003, T028
- [ ] T031 [US2] Author `contracts/avatar-client/evidence-register.yaml` resolving all 72 scenarios — automated→fixture id; manual→result+reviewer+disposition; live_f0/successor→owner_change+fail_closed_default — where the manual-recorded vs deferred(owner+fail-closed) split FOLLOWS the acceptance-map `owner_changes`/`evidence_types` (analyze A7) per spec §FR-032 / data-model §D — depends on T027
- [ ] T032 [US2] Implement validator fixture execution (each case validated to its declared `expect`) + per-schema/per-scenario coverage check in `scripts/validate-avatar-client.py` — depends on T025, T028–T030
- [ ] T033 [US2] Implement validator acceptance-map parity (17/72; unmapped/duplicate/renamed) + evidence-register completeness, legal status transitions, and referenced-artifact existence in `scripts/validate-avatar-client.py` — depends on T027, T031
- [ ] T034 [US2] Populate `redaction/denylist-patterns.yaml` and implement validator dual redaction (structural confirmation + content scan with bounded-sentinel allowlist) in `scripts/validate-avatar-client.py` per spec §FR-018 / research §D4 — depends on T003, T032

**Checkpoint**: US2 independently testable — conformance + traceability + redaction all enforced by the validator.

---

## Phase 5: User Story 3 - Govern a content-addressed contract release (Priority: P3)

**Goal**: The release mechanics — the family index, per-file digests over the semantic consumed set, and consumer-pinning conformance — are in place and validator-checked (the actual tag/version is Phase 8).

**Independent Test**: The validator computes per-file digests over the consumed set and confirms manifest/digest identity **against a provisional/fixture manifest** (the real manifest is authored at realization, T046 — analyze A6); a tag-only pin fails; a consumer can execute fixtures with any draft-2020-12 implementation (spec US3 Independent Test; SC-006/SC-009).

- [ ] T035 [US3] Author `contracts/avatar-client/README.md` — the FAMILY contract index (`Status:` header, `kind`) — and define the manifest-entry format for the semantic consumed set per data-model §H / spec §FR-022 (this is NOT the release-metadata `contracts/README.md` nor the repo-root README — see plan Design Note 4)
- [ ] T036 [US3] Implement validator per-file SHA-256 digest computation over the semantic consumed set (8 schemas, shared-defs, 9 registries, fixtures+index, acceptance-map, interface-lock, evidence-register) + manifest/digest identity check against a provisional/fixture manifest (tag-only pin fails; full-manifest-green only at realization — analyze A6) in `scripts/validate-avatar-client.py` per spec §FR-022/§FR-023/§SC-006 — depends on T033
- [ ] T037 [US3] Author portable consumer-pinning conformance notes + a tag-only-pin negative fixture demonstrating draft-2020-12 execution without the Python validator per spec §FR-023/§SC-009 — depends on T036

**Checkpoint**: US3 independently testable — release mechanics verifiable without publishing a tag.

---

## Phase 6: User Story 4 - Gate publication on F0 feasibility while allowing parallel work (Priority: P4)

**Goal**: The interface lock (with the F0 evidence pin) and the validator's fail-closed F0 gate ensure the bundle tag cannot be published without valid F0 `PASS` evidence, while parallel implementation proceeds.

**Independent Test**: With schemas/fixtures green, the gate blocks the tag when F0 evidence is absent/FAIL/INCONCLUSIVE, a variance is undispositioned, or a pinned-schema digest/commit/instance check fails (spec US4 Independent Test; SC-007/SC-010).

- [ ] T038 [US4] Author `contracts/avatar-client/interface-lock.yaml` — frozen field/registry/ordering/timeout/lease/closed-default decisions + `f0_evidence_pin` block `{f0_source_commit, f0_results_schema_sha256, f0_interface_impact_schema_sha256}` per spec §FR-030/§FR-033 / data-model §E
- [ ] T039 [US4] Implement validator F0 gate in `scripts/validate-avatar-client.py`: resolve pinned F0 schemas, verify digests + source commit, validate consumed evidence instances, read `PASS`/dispositions, and FAIL CLOSED on missing schema / digest mismatch / commit mismatch / instance-validation failure / unknown status / unknown variance field per spec §FR-033/§SC-007/§SC-010 — depends on T036, T038
- [ ] T040 [US4] Author F0-gate fixtures simulating adverse conditions (digest mismatch, invalid instance claiming `PASS`, unknown status/variance, absent/INCONCLUSIVE) and index them per spec §Edge Cases — depends on T039

**Checkpoint**: US4 independently testable — the gate is enforced and fail-closed; realization remains blocked pending real F0 `PASS`.

---

## Phase 7: User Story 5 - Ratify repository and reference boundaries for successors (Priority: P5)

**Goal**: The shared-contract-ownership and repo-boundary-governance ratifications are verified against the realized files and the two completion states are declared.

**Independent Test**: The realized files satisfy the SCO-*/RBG-* scenarios (private client boundary, internal-live evidence gate, deferred aggregation/web-console), recorded as manual evidence in the register (spec US5 Independent Test).

- [ ] T041 [P] [US5] Verify the shared-contract-ownership delta (SCO-001/SCO-002) against realized files — ownership, content-addressed pinning, canonical-fixture execution, reference-vs-client boundaries — and record manual evidence in `evidence-register.yaml` per spec §FR-025
- [ ] T042 [P] [US5] Verify the repo-boundary-governance delta (RBG-001/002/003) against realized files — private `xfactory-avatar-client` boundary, internal-live release-evidence gate, deferred aggregation/web-console — and record manual evidence in `evidence-register.yaml` per spec §FR-026/§FR-027/§FR-028
- [ ] T043 [US5] Declare the two completion states (implementation-complete-pending-F0 vs realized) in `contracts/avatar-client/README.md` / `interface-lock.yaml` per spec §FR-034 — depends on T035, T038

**Checkpoint**: US5 independently testable — governance boundaries ratified and evidenced.

---

## Phase 8: F0-Gated Serialized Realization (⚠️ BLOCKED UNTIL F0 `PASS`)

**Purpose**: Publish the content-addressed release. This phase is **serialized**
(single final integration touching shared release metadata + the repo-root doc
index) and **MUST NOT run** until the gate is green. Stage explicit paths only.

**🚫 GATE PRECONDITION**: F0 `PASS`, every reported interface variance
dispositioned, the F0 evidence pin validates (Phase 6), AND the registered threat
model is accepted. If any is false, STOP — the tag stays blocked
(spec §FR-029/§FR-031/§FR-034; SC-007/SC-010).

- [ ] T044 [GATE] Confirm realization readiness: run `python3 scripts/validate-avatar-client.py --strict` with the F0 gate active and require (a) F0 `PASS`, (b) every interface variance dispositioned, (c) `f0_evidence_pin` green, AND (d) the registered threat model accepted (spec §FR-031; OpenSpec task 1.1). BLOCKS T045–T049.
- [ ] T045 Allocate the next available minor `contract_bundle_version` after `contract-v1.6` (→ `contract-v1.7`) once merge order is known (never reserved earlier) — depends on T044
- [ ] T046 Atomically update shared **release-metadata** files — `contracts/manifest.yaml` (avatar-client entries + per-file `sha256` over the semantic consumed set), `contracts/CHANGELOG.md` (`contract-v1.7` entry), `contracts/README.md` (release-metadata index) — as the serialized final integration, staging explicit paths, per spec §FR-024 — depends on T045
- [ ] T047 Publish the annotated `contract-v1.7` tag from the realized release commit and record per-file digests — depends on T046
- [ ] T048 Publish the machine-readable kernel handoff (release tag, exact commit, per-file digests, interface-lock digest, acceptance-map digest, compatibility instructions) for the reference-runtime and UI-standard siblings (OpenSpec task 4.2) — depends on T047
- [ ] T049 Link the avatar-client contract family into the **repo-root `README.md`** document index (Principle IV), staging that explicit path only (shared-tree discipline) — moved into serialized realization per analyze A2 — depends on T048

**Checkpoint**: Completion state = *realized*; the OpenSpec change may now archive.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Repo-wide gates and evidence closure.

- [ ] T050 [P] Run `python3 scripts/validate-avatar-client.py --strict` and confirm all checks green
- [ ] T051 [P] Run `OPENSPEC_TELEMETRY=0 openspec validate define-avatar-client-contract-kernel --strict` and `--all --strict`
- [ ] T052 [P] Run `git diff --check` and confirm no host-absolute paths and no secrets in committed files (Principle IV/VII)
- [ ] T053 Run the recorded DomainxFactory compatibility validators; block only regressions introduced by this change, not dated pre-existing debt (OpenSpec task 4.3)
- [ ] T054 Execute the `quickstart.md` validation end-to-end (author loop, portable consumer conformance, F0 gate, realization dry-run)

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup — BLOCKS all user stories.
- **US1 (Phase 3)**: depends on Foundational.
- **US2 (Phase 4)**: depends on Foundational + US1 (fixtures target schemas/registries).
- **US3 (Phase 5)**: depends on US2 (digests cover fixtures/acceptance-map/evidence-register).
- **US4 (Phase 6)**: depends on US3 (digest machinery reused for the F0 pin).
- **US5 (Phase 7)**: depends on the realized files from US1–US4 (verification + declaration).
- **Realization (Phase 8)**: depends on US1–US5 complete AND the F0 gate green (incl. threat-model acceptance) — serialized, blocked until F0 `PASS`.
- **Polish (Phase 9)**: depends on all desired phases.

### Story independence notes

- US1 is the MVP: the canonical schema + registry surface stands alone.
- US2 adds conformance/traceability; US3 adds release mechanics; US4 adds the F0
  gate; US5 adds governance ratification. Each is independently testable at its
  checkpoint. The sequencing above reflects genuine artifact dependencies
  (shared `scripts/validate-avatar-client.py` file + digest reuse), not
  arbitrary ordering.

### Parallel opportunities

- Setup: T002, T003 in parallel.
- Foundational: the nine registry files T006–T014 in parallel (after T004; T005 edits shared-definitions and is serialized with T004).
- US1: the eight schema files T017–T024 in parallel (validator tasks T025/T026 are sequential — same file).
- US5: T041, T042 in parallel.
- Polish: T050, T051, T052 in parallel.
- **Serialized (never parallel)**: all validator-editing tasks (T015, T025, T026, T032, T033, T034, T036, T039 — same file); the shared-definitions edits (T004→T005 — same file); and the entire Phase 8 realization (incl. T049 repo-root README).

---

## Parallel Example: Foundational registries + US1 schemas

```bash
# After T004/T005 (shared-definitions + speech-gate enum), author the nine registries together:
Task: "Author registries/session-result-reasons.registry.yaml"   # T006
Task: "Author registries/events.registry.yaml"                    # T007
# ... T008–T014

# After Foundational, author the eight AVC schemas together:
Task: "Author avc-01-session-request.schema.yaml"                 # T017
Task: "Author avc-02-session-result.schema.yaml"                  # T018
# ... T019–T024
```

---

## Implementation Strategy

### MVP first (US1)

1. Phase 1 Setup → Phase 2 Foundational (shared-definitions + speech-gate enum + registries + harness).
2. Phase 3 US1 (eight schemas + schema/registry/enum validator checks).
3. **STOP and VALIDATE**: schemas resolve, registries closed, parity + speech-gate closure hold.

### Incremental delivery

US1 (canonical surface) → US2 (conformance/traceability) → US3 (release
mechanics) → US4 (F0 gate) → US5 (governance ratification). Each increment is
validator-green before the next. Phase 8 realization is withheld until F0 `PASS`.

### OpenSpec task mapping (governance handoff, not duplicated)

Per plan Design Note 1, the OpenSpec `tasks.md` (1.x–4.x) is the governance
handoff; this Speckit list is the implementation decomposition. Mapping:
- 1.1 → T038 (baseline in interface-lock), T044(d) (threat-model acceptance)
- 1.2/1.3 → T038, T039, T044
- 2.1 → T004 (+T005 speech-gate enum); 2.2–2.4 → T017–T024; 2.5 → T006–T014
- 3.1 → T027–T033; 3.2 → T015, T025, T026, T032–T034, T036, T039; 3.3 → T045–T047
- 4.1 → T041, T042; 4.2 → T048; 4.3 → T051, T053

---

## Notes

- `[P]` = different files, no incomplete dependency. Same-file tasks (all
  validator edits, the two shared-definitions edits, shared release metadata,
  repo-root README) are serialized.
- Conformance evidence = self-describing fixtures + validator output (Principle V).
- Commit after each task or logical group; keep this change's writes inside
  `contracts/avatar-client/` + `scripts/validate-avatar-client.py` until the
  serialized realization step, which additionally touches the three shared
  release-metadata files and the repo-root README with explicit-path staging.
- Total: 54 tasks — Setup 3, Foundational 13, US1 10, US2 8, US3 3, US4 3,
  US5 3, Realization 6, Polish 5. 25 tasks marked [P].
