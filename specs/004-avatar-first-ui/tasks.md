# Tasks: Avatar-First UI Standard Alignment

**Input**: Design documents from `specs/004-avatar-first-ui/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/,
quickstart.md (all present)

**Tests**: This feature's "tests" ARE the offline validator plus deterministic
positive/compatibility/negative fixtures — they are deliverables, not a separate
TDD layer. No additional unit-test framework is requested.

**Organization**: Tasks are grouped by user story (from spec.md) so each story is
an independently testable increment. All work stays inside the five owned UI
artifacts + the new `examples/avatar-first-ui/fixtures/` directory; kernel
registries are consumed read-only; shared contract metadata is touched ONLY in
the gated Phase 6.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US4 (Setup / Foundational / Polish carry no story label)
- Every task names an exact file path.

## Owned artifacts (write scope)

- `docs/avatar-first-ui-standard.md`
- `contracts/schemas/avatar-first-ui-profile.schema.yaml`
- `templates/ui/avatar-first.yaml`
- `examples/avatar-first-ui/` (incl. new `fixtures/`)
- `scripts/validate-avatar-first-ui.py`

Read-only (never edited here): kernel registries under `contracts/avatar-client/**`
and all kernel/reference-runtime/F0/DomainxFactory/Flutter/deployment files.
Shared contract metadata (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
`contracts/README.md`) + annotated tag: Phase 6 (DEFERRED) only.

**Enforced rule classes**: nine (per Q6 + the 2026-07-11 analyze-gate disposition
adding `AFUV-RETENTION-UNRESOLVED` for FR-027). See contracts/validator-rules.md.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Scaffold the new fixtures area and fix the shared error-ID catalog.

- [X] T001 Create the deterministic fixtures scaffold `examples/avatar-first-ui/fixtures/` with `compatibility/` and `negative/` subdirectories and a placeholder `examples/avatar-first-ui/fixtures/README.md` (evidence-map stub) per contracts/fixture-shape.md
- [X] T002 [P] Record the stable validator error/evidence-ID catalog — the nine `AFUV-*` rule-class IDs plus parity/structure IDs — as an authoritative constants/reference block header in `scripts/validate-avatar-first-ui.py` per contracts/validator-rules.md (no logic yet)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The profile schema and the validator skeleton that the template,
examples, fixtures, standard, and every rule check depend on.

**⚠️ CRITICAL**: No user-story work may begin until this phase is complete.

- [X] T003 Update `contracts/schemas/avatar-first-ui-profile.schema.yaml` with the additive optional blocks (runtime_compatibility, presentation, media, outcome_slots, fallback_slots, interaction_mode, speech_gate, timing, consent_purpose_mappings, persona_reference, retention_overlay, accessibility_baseline, handoff) — each optional with a closed default; preserve the existing required top-level keys; keep the legacy embedded `persona_catalog` accepted (deprecated) per contracts/profile-schema-outline.md and data-model.md, satisfying spec §FR-013/§FR-014/§FR-015/§FR-025/§FR-026/§FR-027/§FR-028
- [X] T004 Extend `scripts/validate-avatar-first-ui.py` with the two-mode skeleton (`--mode baseline` default / `--mode realization`) and read-only resolution of kernel IDs and readiness/heartbeat/lease ceilings from the frozen `avatar-client-parallel-v1` baseline fixture data (no per-rule checks yet) per research §D4/§D13, satisfying spec §FR-017/§FR-026 (read-only registry + ceiling consumption)
- [X] T005 Extend `scripts/validate-avatar-first-ui.py` structural/parity checks (`AFUV-SCHEMA-SHAPE`, `AFUV-TEMPLATE-SHAPE`, `AFUV-PARITY-EXAMPLE`) to cover the new schema blocks and closed-default (fail-closed) resolution of omitted fields per contracts/validator-rules.md, satisfying spec §FR-016/§FR-020

**Checkpoint**: Schema + validator skeleton ready — user stories can begin.

---

## Phase 3: User Story 1 - Author a conformant avatar-first UI profile (Priority: P1) 🎯 MVP

**Goal**: A domain author can express a conformant profile from the aligned
schema/template/examples, and the offline validator confirms conformance, closed
defaults, and rule enforcement — positive profiles pass, negatives fail.

**Independent Test**: Run `python3 scripts/validate-avatar-first-ui.py` over the
template + four archetype examples + compatibility fixture (all PASS) and each of
the nine negative fixtures (each FAILS on its one primary rule with its stable
error ID), offline.

### Implementation for User Story 1

- [X] T006 [US1] Update `templates/ui/avatar-first.yaml` with the stable regions, standard controls, authority sources, media/recording awareness, fallback behavior, handoff boundary, and reserved-feature defaults (provider_vad default; server_vad + push_to_talk reserved) per spec §FR-018 and data-model.md
- [X] T007 [US1] Rewrite the four representative examples in `examples/avatar-first-ui/domain-overlays.example.yaml` as domain-neutral archetypes — customer avatar-first, client hybrid, domain conventional-first, and `confirmation-before-consequential-action` (neutral vocabulary, Ledgerx inspiration only) — using `persona_reference` and the new blocks per spec §FR-019 (Q2)
- [X] T008 [P] [US1] Author the compatibility fixture `examples/avatar-first-ui/fixtures/compatibility/legacy-persona-catalog.yaml` (pre-alignment profile incl. legacy embedded `persona_catalog`, no new blocks) that MUST still validate per spec §FR-016/§SC-003 (Q1 compatibility)
- [X] T009 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/authority-transition.yaml` (presentation authors an authoritative axis transition → `AFUV-AUTHORITY-TRANSITION`) per contracts/validator-rules.md
- [X] T010 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/timing-out-of-range.yaml` (selected readiness/heartbeat/lease exceeds kernel ceiling → `AFUV-TIMING-OUT-OF-RANGE`)
- [X] T011 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/control-fallback-missing.yaml` (required control missing its fallback → `AFUV-CONTROL-FALLBACK-MISSING`)
- [X] T012 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/persona-unresolved.yaml` (unknown/invalid persona reference → `AFUV-PERSONA-UNRESOLVED`)
- [X] T013 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/mode-reserved.yaml` (reserved/forbidden mode without fallback → `AFUV-MODE-RESERVED`)
- [X] T014 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/unsafe-render.yaml` (HTML/executable/unsafe URI → `AFUV-UNSAFE-RENDER`)
- [X] T015 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/purpose-invalid.yaml` (missing/invalid consent-purpose mapping → `AFUV-PURPOSE-INVALID`)
- [X] T016 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/held-answer-active.yaml` (held answer rendered as active → `AFUV-HELD-ANSWER-ACTIVE`)
- [X] T017 [P] [US1] Author negative fixture `examples/avatar-first-ui/fixtures/negative/retention-unresolved.yaml` (unresolvable retention-policy reference fails closed → `AFUV-RETENTION-UNRESOLVED`) per spec §FR-027 and the analyze-gate disposition (9th rule class)
- [X] T018 [US1] Implement the per-rule enforcement checks in `scripts/validate-avatar-first-ui.py` for all nine rule classes above (each emits `ERROR <AFUV-*>`; each negative fixture fails exactly its one primary rule) per contracts/validator-rules.md and data-model.md, satisfying spec §FR-020
- [X] T019 [US1] Implement per-fixture assertion in `scripts/validate-avatar-first-ui.py`: negative fixtures must fail their declared `expect_error`; template + four examples + compatibility fixture must pass clean; report zero fields defaulting open per spec §SC-002/§SC-004
- [X] T020 [US1] Run the US1 independent test (validator over template + examples + all fixtures, baseline mode) and confirm PASS/expected-FAIL matrix per quickstart.md §1

**Checkpoint**: Profile authoring is provably conformant, offline, with full nine-class rule coverage.

---

## Phase 4: User Story 2 - Read a precise, layered avatar-first standard (Priority: P1)

**Goal**: The standard document precisely defines the axes-vs-modes model,
Hermes-layer defaults, media/held-answer semantics, AVC-02 rendering, control vs
media loss, safe rendering, persona/disclosure, workflow boundary, and the
accessibility evidence boundary — with a named owner per behavior.

**Independent Test**: Review `docs/avatar-first-ui-standard.md` against the eight
`AFU-*` requirements; confirm each behavior has an owner and every deferred item
names a successor + closed default. (Independent of the schema/validator — a
different file.)

### Implementation for User Story 2

- [X] T021 [P] [US2] Update `docs/avatar-first-ui-standard.md` runtime section: define the four authoritative axes (session lifecycle, control health, media state, workflow projection) vs client-local `conversation|work|review` presentation modes, and mode-change context preservation + AVC-12 reconciliation per spec §FR-001/§FR-002
- [X] T022 [US2] Update `docs/avatar-first-ui-standard.md` Hermes-layer + controls + media sections: layer defaults and override attributes; required controls and missing-control fallback; media-authorization/held-answer; AVC-02 denial/terminal rendering; control-loss vs media-loss per spec §FR-003/§FR-004/§FR-007/§FR-008/§FR-009
- [X] T023 [US2] Update `docs/avatar-first-ui-standard.md` persona/disclosure, safe-rendering, workflow-boundary, and accessibility-evidence-boundary sections: persona reference-only + disclosure duties; untrusted-content rules; client/web-console split + handoff URL constraints; declarable a11y vs later platform qualification per spec §FR-005/§FR-006/§FR-010/§FR-011/§FR-012
- [X] T024 [US2] Review `docs/avatar-first-ui-standard.md` to confirm each of the eight `AFU-*` behaviors names a single owner (Hermes layer / runtime axis / kernel registry / named successor) with deferred items carrying a closed default per spec §SC-005/§US2

**Checkpoint**: The standard is precise and owner-complete, independent of the schema.

---

## Phase 5: User Story 3 - Prove full requirement-to-evidence traceability offline (Priority: P2)

**Goal**: Every `AFU-*` requirement/scenario maps to owned evidence
(standard/schema/template/fixture) or a named successor, with deterministic
fixture shapes and acceptance-map parity — all offline.

**Independent Test**: Run acceptance-map parity (8 requirements / 25 scenarios)
and the validator over schema/template/examples/fixtures; confirm every
requirement/scenario resolves to an owner and successor-owned evidence is
annotated as deferred.

### Implementation for User Story 3

- [X] T025 [US3] Complete `examples/avatar-first-ui/fixtures/README.md` as the evidence map binding each `AFU-*` scenario/requirement to its fixture(s) or named successor (`implement-avatar-client-lab`, `avatar-pilot-hardening`), mirroring the OpenSpec acceptance map (read-only) and using the map's `evidence_id_template: TEST-{scenario_id}` convention per spec §FR-022/§SC-001
- [X] T026 [US3] Populate each fixture's `evidence_ids` (acceptance-map scenario IDs, e.g. `AFU-001-S01`), `inputs` (fixed clock/ID/font/locale/platform), `canonical` AVC command/event/snapshot inputs, and `expected` view-state/record shapes per contracts/fixture-shape.md and spec §FR-023
- [X] T027 [US3] Implement acceptance-map parity check `AFUV-PARITY-ACCEPTANCE` in `scripts/validate-avatar-first-ui.py`: consume `openspec/changes/align-avatar-first-ui-standard/supporting-docs/avatar-first-ui-acceptance-map.yaml` read-only; assert 8 requirements / 25 scenarios; and resolve every fixture's scenario `evidence_ids` against the map via `evidence_id_template: TEST-{scenario_id}` (no hand-authored `TEST-` IDs) per spec §SC-008 (I1 disposition)
- [X] T028 [US3] Implement the determinism assertion in `scripts/validate-avatar-first-ui.py` (identical inputs → equivalent expected shapes + identical evidence IDs across two runs) per spec §SC-006/quickstart.md §6
- [X] T029 [US3] Run the US3 independent test (acceptance-map parity + validator over all artifacts + determinism spot-check) and confirm zero unowned requirements/scenarios per quickstart.md §4/§6

**Checkpoint**: Requirement-to-evidence traceability is complete and offline-reproducible.

---

## Phase 6: User Story 4 - Serialize the final contract release after the kernel (Priority: P3) ⛔ DEFERRED / GATED

**Goal**: After the AVC kernel release lands, serialize the content-addressed
profile-schema release and shared-metadata update atomically.

**⚠️ GATE — DO NOT RUN NOW**: Every task in this phase is blocked until the AVC
kernel release exists. These tasks are the ONLY ones permitted to touch shared
contract metadata, and they serialize against sibling changes. During parallel
work these files MUST NOT change (verified by T033 / SC-007).

**Independent Test**: In realization mode the validator fails closed on any
registry drift; manifest/CHANGELOG/README change together for exactly one
profile-schema revision with a version allocated at realization; no
kernel/reference-runtime/F0/DomainxFactory/Flutter/deployment file changed.

### Implementation for User Story 4 (deferred)

- [ ] T030 [US4] (GATED) Consume any accepted kernel variances through mapped UI fields only in `contracts/schemas/avatar-first-ui-profile.schema.yaml` and affected `examples/avatar-first-ui/fixtures/` — no sibling kernel path edited — per spec §US4
- [ ] T031 [US4] (GATED) Set `runtime_compatibility` released coordinates (bundle tag + exact commit + registry/interface-lock digests) and run `python3 scripts/validate-avatar-first-ui.py --mode realization`, failing closed on any drift, per spec §FR-021/§FR-025
- [ ] T032 [US4] (GATED) Rebase to the latest bundle, allocate the next available `contract_bundle_version` at realization (never pre-reserved), and update `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and `contracts/README.md` atomically for the profile-schema revision + publish the matching annotated `contract-v<major>.<minor>` tag per spec §FR-024/Constitution §VI
- [ ] T033 [US4] (GATED) Run `git status --porcelain` and `git diff --stat` to confirm no kernel (`contracts/avatar-client/**`)/reference-runtime/F0/DomainxFactory/Flutter/deployment file changed by the release commit (ownership cross-check) per spec §SC-007

**Checkpoint**: Serialized release lands atomically after the kernel — gated, not runnable during parallel work.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Doc-index linkage, lifecycle status, and the full offline gate.

- [ ] T034 [P] Update `examples/avatar-first-ui/README.md` and the repository `README.md` doc index to reference the new fixtures area per Constitution §IV
- [ ] T035 Set the standard's lifecycle header in `docs/avatar-first-ui-standard.md` to `Status: ratified` + `Ratified by: align-avatar-first-ui-standard` at the ratify/landing gate (deliberate transition, not a silent edit) per Constitution §III
- [ ] T036 Run the full offline gate per quickstart.md: `python3 scripts/validate-avatar-first-ui.py` (baseline), `OPENSPEC_TELEMETRY=0 openspec validate align-avatar-first-ui-standard --strict` and `--all --strict`, acceptance-map parity, and `git diff --check` — all green per spec §SC-008
- [ ] T037 Run the ownership-boundary cross-check (`git status --porcelain`): confirm changes are limited to the five owned artifacts + `examples/avatar-first-ui/fixtures/` during parallel work per spec §SC-007

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — start immediately.
- **Foundational (Phase 2)**: depends on Setup — BLOCKS all user stories (schema T003 + validator skeleton T004/T005 underpin template, examples, fixtures, rules, parity).
- **US1 (Phase 3)** and **US2 (Phase 4)**: both P1; depend only on Foundational. US2 edits a different file (`docs/…`) from US1, so US2 may run fully in parallel with US1.
- **US3 (Phase 5)**: P2; depends on US1 (fixtures/validator rules exist) and consumes the acceptance map read-only.
- **US4 (Phase 6)**: P3; GATED on the external AVC kernel release — not runnable now; serializes shared-metadata edits.
- **Polish (Phase 7)**: depends on US1–US3 complete (T035 is a landing/ratify-gate step).

### User Story Dependencies

- US1 (P1): after Foundational. Self-contained (template + examples + fixtures + validator rules).
- US2 (P1): after Foundational. Independent file (standard doc) — no dependency on US1.
- US3 (P2): after US1 (needs fixtures + validator rule engine); read-only on the OpenSpec acceptance map.
- US4 (P3): after US1–US3 land AND the kernel release exists (external gate).

### Within Each User Story

- Same-file tasks are sequential (e.g., all `scripts/validate-avatar-first-ui.py` tasks; all `docs/avatar-first-ui-standard.md` tasks).
- Fixture files are independent → parallelizable.
- Validator rule checks (T018/T019) depend on the fixtures they assert (T008–T017) and on the T004/T005 skeleton.

### Parallel Opportunities

- Setup: T002 [P] alongside T001.
- US1 fixtures: T008–T017 [P] (ten distinct fixture files — one compatibility + nine negative, after schema T003).
- US2 standard-doc work (T021 [P]) can proceed in parallel with the entire US1 phase (different file).
- Polish: T034 [P].

---

## Parallel Example: User Story 1 fixtures

```bash
# After Foundational (schema T003) is complete, author all fixtures in parallel:
Task: "Author compatibility fixture examples/avatar-first-ui/fixtures/compatibility/legacy-persona-catalog.yaml"
Task: "Author negative fixture .../negative/authority-transition.yaml"
Task: "Author negative fixture .../negative/timing-out-of-range.yaml"
Task: "Author negative fixture .../negative/control-fallback-missing.yaml"
Task: "Author negative fixture .../negative/persona-unresolved.yaml"
Task: "Author negative fixture .../negative/mode-reserved.yaml"
Task: "Author negative fixture .../negative/unsafe-render.yaml"
Task: "Author negative fixture .../negative/purpose-invalid.yaml"
Task: "Author negative fixture .../negative/held-answer-active.yaml"
Task: "Author negative fixture .../negative/retention-unresolved.yaml"
# Then implement the rule checks (T018) and per-fixture assertions (T019) in the validator (sequential — same file).
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Phase 1 Setup → 2. Phase 2 Foundational (schema + validator skeleton) →
3. Phase 3 US1 → **STOP and VALIDATE**: profiles authorable and rule-enforced
offline. This is the demonstrable MVP.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 (schema/template/examples/fixtures/validator) → validate → MVP.
3. US2 (standard doc) → review independently (can overlap US1).
4. US3 (evidence map + parity + determinism) → validate.
5. Polish (doc index, gate) → merge.
6. US4 (serialized release) → run ONLY after the kernel release (gated).

### Parallel Team Strategy

- After Foundational: Dev A drives US1 (schema/validator/fixtures); Dev B drives
  US2 (standard doc, different file); US3 follows US1.

---

## Notes

- [P] = different files, no incomplete dependency; same-file tasks stay sequential.
- Nine enforced rule classes (Q6's eight + `AFUV-RETENTION-UNRESOLVED` from the
  2026-07-11 analyze-gate disposition for FR-027).
- Evidence IDs follow the acceptance map's `evidence_id_template: TEST-{scenario_id}`;
  fixtures declare scenario IDs and the parity check derives evidence IDs.
- Kernel registries and ceilings are consumed read-only; the acceptance map is
  consumed read-only.
- Phase 6 is the ONLY place shared contract metadata changes, and it is gated on
  the external kernel release — keep it unchecked/unrun during parallel work.
- Commit after each task or logical group; stage explicit paths only (never
  `git add -A`); verify the current branch before each commit.
- This Speckit task list is the implementation breakdown for OpenSpec change
  `align-avatar-first-ui-standard`; it does not duplicate that change's
  governance task list (Constitution §II).
