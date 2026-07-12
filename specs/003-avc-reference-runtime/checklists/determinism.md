# Determinism & Reproducibility Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing determinism, injected
dependencies, and reproducible evidence — testing whether these requirements are complete, clear,
consistent, and measurable (NOT whether the code is deterministic).
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / release approver

## Requirement Completeness

- [ ] CHK001 Are the seven injected ports (clock, ID, provider, policy, consent, operation, usage) each enumerated as a requirement with a defined responsibility? [Completeness, Spec §FR-007, §Key Entities]
- [ ] CHK002 Is the injected clock specified as *both* a monotonic and a wall clock, with their distinct roles stated? [Completeness, Spec §Assumptions, contracts/ports.md]
- [ ] CHK003 Are the categories of forbidden ambient dependencies (wall-clock time, randomness, sleep, filesystem persistence, network, Hermes) each explicitly listed? [Completeness, Spec §FR-007, §SC-004]
- [ ] CHK004 Is every time-dependent transition class (readiness, heartbeat, lease, cache TTL, confirmation, duration) named as requiring injected-clock advancement? [Completeness, Spec §FR-008]
- [ ] CHK005 Is a requirement present that repeated runs and randomized test order produce identical authoritative results? [Completeness, Spec §SC-003, §FR-008]
- [ ] CHK006 Is the requirement to record multiple randomization seeds documented as evidence? [Completeness, Spec §Clarifications Q1, §SC-003]
- [ ] CHK007 Is the requirement that a failing seed be reproducible from reported output stated? [Completeness, Spec §Clarifications Q1]
- [ ] CHK008 Are the deterministic ID-source semantics (queued/stable, no random UUID) specified? [Completeness, Spec §Assumptions, contracts/ports.md]

## Requirement Clarity & Measurability

- [ ] CHK009 Is "deterministic" defined in measurable terms (identical authoritative results across repeat + reorder) rather than as an adjective? [Clarity, Spec §SC-003]
- [ ] CHK010 Is the "five-second" revocation bound unambiguously defined as measured on the injected clock, not real elapsed time? [Ambiguity, Spec §Assumptions, §FR-023]
- [ ] CHK011 Is "no test depends on wall time/randomness/network/persistence/Hermes" phrased as an objectively countable criterion (count = 0)? [Measurability, Spec §SC-004]
- [ ] CHK012 Is the number/selection policy for recorded seeds specified precisely enough to reproduce (e.g., how many, where recorded)? [Clarity, Spec §Clarifications Q1, contracts/conformance-artifacts.md]
- [ ] CHK013 Are "identical authoritative results" scoped to a defined set of observable outputs (events, outcomes, telemetry) rather than left open? [Clarity, Spec §SC-003]
- [ ] CHK014 Is the distinction between "authoritative results" and non-authoritative observations defined for determinism comparison purposes? [Clarity, Spec §FR-026]

## Requirement Consistency

- [ ] CHK015 Is the stdlib-only-core requirement consistent with the determinism requirement (no third-party source of nondeterminism)? [Consistency, Spec §FR-001, §SC-005]
- [ ] CHK016 Do the injected-port requirements and the "core never calls ambient wall time/random/sleep" requirement agree without contradiction? [Consistency, Spec §FR-007, contracts/ports.md]
- [ ] CHK017 Are clock-advancement requirements consistent across all modules that own deadlines (attempt, control, grant cache, consent, usage)? [Consistency, Spec §FR-008, data-model.md]
- [ ] CHK018 Is the reproducibility requirement (seeds) consistent between the spec Clarifications and the realization-pin evidence schema? [Consistency, Spec §Clarifications Q1, contracts/conformance-artifacts.md]

## Scenario Coverage (Primary / Alternate / Exception / Recovery / Non-Functional)

- [ ] CHK019 [Primary] Are requirements defined for the normal case where a deadline fires exactly at the advanced clock value? [Coverage, Spec §FR-008]
- [ ] CHK020 [Alternate] Are requirements defined for provider/sideband operations completed in a *different order*, requiring declared transitions over ambient scheduling? [Coverage, Spec §FR-009, §US1-2]
- [ ] CHK021 [Exception] Are requirements defined for when an authority port returns "unavailable/unknown" during a deterministic run (fail-closed outcome)? [Coverage, Spec §FR-010, §Edge Cases]
- [ ] CHK022 [Recovery] Are requirements defined so that re-running with a pinned seed reproduces a prior failure state? [Recovery, Spec §Clarifications Q1]
- [ ] CHK023 [Non-Functional] Is the hermeticity requirement (no external dependency of any kind in tests) stated as a gate, not a preference? [Coverage, Spec §SC-004]
- [ ] CHK024 [Edge] Are boundary conditions for clock advancement (zero advance, exact-deadline, past-deadline) addressed in the requirements? [Edge Case, Gap]
- [ ] CHK025 [Edge] Is behavior specified when two deadlines fall on the same injected tick (ordering determinism)? [Edge Case, Gap]

## Acceptance Criteria & Traceability

- [ ] CHK026 Does every determinism-related success criterion (SC-003, SC-004) map to at least one functional requirement? [Traceability, Spec §SC-003, §SC-004]
- [ ] CHK027 Are determinism requirements traceable to the ARR scenarios that exercise them (ARR-003-S01/S02, ARR-008-S02)? [Traceability, Spec §US1, acceptance map]
- [ ] CHK028 Is the requirement that the deterministic suite maps to acceptance IDs (not ad-hoc tests) stated? [Traceability, Spec §FR-034]

## Dependencies & Assumptions

- [ ] CHK029 Is the assumption that fixture-configured limits (cache TTL, buffer bound, caps, confirmation windows) are deterministic test values (not production tuning) documented? [Assumption, Spec §Assumptions]
- [ ] CHK030 Is the dependency on the pinned test toolchain (pytest, pytest-randomly) documented and version-pinned in requirements? [Dependency, Spec §Dependencies, §Clarifications Q1/Q3]
- [ ] CHK031 Is the assumption that the runtime creates no durable state (so re-runs start clean) stated and consistent with SC-009? [Assumption, Spec §FR-003, §SC-009]

## Ambiguities & Conflicts

- [ ] CHK032 Is there any unresolved ambiguity about whether wall-clock timestamps may influence control decisions (they must not)? [Ambiguity, Spec §Assumptions, contracts/ports.md]
- [ ] CHK033 Is it unambiguous that "randomized test order" refers to test ordering only, not randomized inputs to the runtime? [Ambiguity, Spec §SC-003]

## Notes

- Items are requirements-quality questions ("is X specified/measurable/consistent?"), never implementation tests.
- ≥80% of items carry a traceability reference (`[Spec §…]`, `[Gap]`, `[Assumption]`, etc.).
