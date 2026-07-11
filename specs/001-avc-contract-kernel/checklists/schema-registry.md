# Schema & Registry Integrity Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for the eight AVC
schemas, the shared-definitions module, and the closed registries — completeness,
clarity, consistency, measurability, and coverage of the requirements as written
(not implementation verification).
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [ ] CHK001 Are all eight AVC contracts (AVC-01/-02/-04/-06/-07/-08/-11/-12) individually enumerated with a stated purpose? [Completeness, Spec §FR-001]
- [ ] CHK002 Is the requirement that every contract declares a contract identifier AND a `contract_schema_version` stated for all eight? [Completeness, Spec §FR-001]
- [ ] CHK003 Are the shared-definitions `$defs` groups enumerated exhaustively (actor/client/subject, purpose, consent, trace, epoch, media leg/attempt, offer fingerprint, state revision, last-event sequence, media authorization, outcomes, retention, redaction, retry-equivalence)? [Completeness, Spec §FR-003; data-model §A]
- [ ] CHK004 Is the absorption of AVC-03 (inline capabilities on AVC-02 grant) and AVC-05 (AVC-04 payload) specified rather than left implicit? [Completeness, Spec §FR-002]
- [ ] CHK005 Is the reserved status of AVC-09 and AVC-10 (identifiers never reused) stated as a requirement? [Completeness, Spec §FR-002]
- [ ] CHK006 Are all nine registries named (8 vocabularies + consent purposes) with their member scope defined? [Completeness, Spec §FR-004/FR-005; data-model §B]
- [ ] CHK007 Is the requirement for a single shared-definitions module referenced by `$ref` (not per-contract duplication) explicit? [Completeness, Spec §FR-003; research §D8]
- [ ] CHK008 Are the discriminated AVC-02 variants (`grant | denial | terminal`) and their per-variant field sets specified? [Completeness, Spec §FR-007; data-model §A]

## Requirement Clarity

- [ ] CHK009 Is "closed registry" defined precisely enough to be testable (unknown value rejected, not merely discouraged)? [Clarity, Spec §FR-004, §Edge Cases]
- [ ] CHK010 Is the exact membership of the session-result reason registry (the 15 enumerated reasons) unambiguous and free of synonyms? [Clarity, Spec §FR-004]
- [ ] CHK011 Is the exact membership of the consent-purpose registry (the 3 neutral purposes) stated without domain-specific additions? [Clarity, Spec §FR-005]
- [ ] CHK012 Is the `$ref` resolution requirement clear that it is offline/local (no host-absolute or network `$id`)? [Clarity, research §D8; plan Constraints]
- [ ] CHK013 Is "structurally invalid" for secret-bearing denial/terminal results defined so it can be objectively checked (schema validation fails)? [Clarity, Spec §FR-007]
- [ ] CHK014 Are the terms distinguishing `state_revision` vs `last_event_sequence` defined so their roles cannot be conflated? [Clarity, Spec §FR-011; data-model §A]

## Requirement Consistency

- [ ] CHK015 Does the schema/registry parity requirement (schema enum == registry members) appear consistently across the spec, plan, research, and data-model? [Consistency, research §D3; data-model §B]
- [ ] CHK016 Are the registries referenced by the acceptance/validation requirements the same set enumerated in FR-004/FR-005 (no orphan or missing registry)? [Consistency, Spec §FR-004/§FR-020]
- [ ] CHK017 Do the "no provider DTO / model id / widget state / secret as required field" rules apply consistently to every contract and the shared module? [Consistency, Spec §FR-006]
- [ ] CHK018 Is the interaction-mode registry consistently stated to include `provider_vad` and exclude push-to-talk (which fails preflight)? [Consistency, Spec §Edge Cases; data-model §B]

## Acceptance Criteria Quality (Measurability)

- [ ] CHK019 Is "all cross-references resolve" expressed as a measurable outcome (0 unresolved references)? [Measurability, Spec §SC-001]
- [ ] CHK020 Are the exact registry counts measurable (session-result reasons = 15, consent purposes = 3)? [Measurability, Spec §SC-004]
- [ ] CHK021 Is "every closed registry rejects unrecognized values" stated as a 100%-verifiable criterion? [Measurability, Spec §SC-004]
- [ ] CHK022 Can "no denial/terminal result carrying SDP/answer/credential passes validation" be objectively measured (0 leaks)? [Measurability, Spec §SC-005]

## Scenario & Edge-Case Coverage

- [ ] CHK023 Are requirements defined for the additive-optional-field compatibility case (preserve/ignore on same major)? [Coverage, Spec US1-AS1, §FR-008; ACR-001-S01]
- [ ] CHK024 Are requirements defined for the incompatible-major case (preflight fails before media/commands)? [Coverage, Spec US1-AS2; ACR-001-S02]
- [ ] CHK025 Are requirements defined for unknown command/event/state/confirmation-decision (fail closed, no permissive inference)? [Coverage, Spec §FR-008; ACR-001-S03]
- [ ] CHK026 Is the boundary behavior for numeric bounds encoded in schemas (readiness 1000–5000 ms; heartbeat >0..5000; lease ≤10000) covered by a requirement and a boundary fixture class? [Edge Case, Spec §FR-010/§FR-012; data-model §F]
- [ ] CHK027 Is an unknown-authority (wrong producer) scenario class required as a fixture for event producer classification? [Coverage, Spec §FR-011/§FR-019]
- [ ] CHK028 Are requirements defined for AVC-07 reserved/forbidden retention classes appearing in a schema without becoming valid? [Edge Case, Spec §FR-017; ACR-010-S02]

## Dependencies & Assumptions

- [ ] CHK029 Is the assumption that "YAML-serialized JSON Schema draft 2020-12" is the mandated artifact format documented (not a discretionary choice)? [Assumption, Spec §Assumptions; plan Technical Context]
- [ ] CHK030 Is the dependency on the frozen `avatar-client-parallel-v1` baseline for the schema field/registry decisions stated? [Dependency, Spec §Dependencies]

## Ambiguities & Conflicts

- [ ] CHK031 Is there any ambiguity about whether registries are inline enums, standalone files, or both — and is the chosen model (both, parity-checked) stated unambiguously? [Ambiguity, research §D3]
- [ ] CHK032 Is it unambiguous that AVC-07/AVC-08 deliver schemas + fixtures ONLY (no instances/examples/templates), avoiding conflict with domain ownership? [Conflict, Spec §FR-001 (Q2); §Out of Scope]
