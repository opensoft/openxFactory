# Conformance & Traceability Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing acceptance-ID mapping, ACR
sourcing, the scenario→test map, and the realization pin — testing requirement quality, not the
checker's behavior.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Contract-kernel owner / release approver

## Requirement Completeness

- [ ] CHK001 Is the requirement that *every* runtime-owned `ARR-*` scenario map to deterministic evidence stated? [Completeness, Spec §FR-034, §SC-001]
- [ ] CHK002 Is the requirement that *every applicable* kernel `ACR-*` scenario map to a test or a recorded non-applicability disposition stated? [Completeness, Spec §FR-034, §SC-002]
- [ ] CHK003 Is the source of the applicable `ACR-*` set specified as an acceptance map (not a second hand-maintained enumeration)? [Completeness, Spec §FR-034a, §Clarifications Q5]
- [ ] CHK004 Is the parallel-work acceptance source path (`…/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`) specified with commit + digest verification? [Completeness, Spec §FR-034a, §Dependencies]
- [ ] CHK005 Is the realization acceptance source (`contracts/avatar-client/acceptance-map.yaml`, digest-pinned) specified? [Completeness, Spec §FR-034a, §Dependencies]
- [ ] CHK006 Is the mapping artifact (`scenario-test-map.yaml`) required with `schema_version` + `kind`? [Completeness, Spec §Clarifications Q6, contracts/conformance-artifacts.md]
- [ ] CHK007 Are all checker failure conditions enumerated (missing, duplicate, dangling, skipped-required, unknown)? [Completeness, Spec §FR-034, §Clarifications Q6]
- [ ] CHK008 Is the realization-pin artifact (`realization-pin.yaml`) required with `schema_version` + `kind` and the five coordinates? [Completeness, Spec §FR-005, §SC-006, contracts/conformance-artifacts.md]
- [ ] CHK009 Are the five release coordinates each named (tag, exact commit, per-file digests, interface-lock digest, acceptance-map digest)? [Completeness, Spec §FR-005, §SC-006]
- [ ] CHK010 Is the requirement to run final evidence with the provisional adapter disabled against canonical fixtures stated? [Completeness, Spec §FR-035]

## Requirement Clarity & Measurability

- [ ] CHK011 Is "applicable ACR-* scenario" defined precisely (how applicability is determined and where non-applicability is recorded)? [Clarity, Spec §FR-034a, §Assumptions]
- [ ] CHK012 Is a non-applicability disposition required to carry a rationale, and is that requirement explicit? [Clarity, Spec §Clarifications Q6, contracts/conformance-artifacts.md]
- [ ] CHK013 Is "conformance fails" defined as an objective checker outcome for each failure class? [Measurability, Spec §FR-034]
- [ ] CHK014 Is coverage measurable as "0 unmapped applicable scenarios" and "0 duplicate/dangling/skipped-required/unknown"? [Measurability, Spec §SC-002]
- [ ] CHK015 Is a bare tag (without exact commit + digests) unambiguously specified to fail realization? [Clarity, Spec §FR-005, §ARR-002-S03]
- [ ] CHK016 Is "canonical execution disagrees with provisional behavior" defined as a measurable realization-fail trigger? [Measurability, Spec §FR-035, §ARR-008-S03]

## Requirement Consistency

- [ ] CHK017 Is the single-source-of-truth rule (one acceptance map, no second enumeration) consistent across spec Assumptions, FR-034a, and the artifact schema? [Consistency, Spec §Assumptions, §FR-034a, contracts/conformance-artifacts.md]
- [ ] CHK018 Are the provisional→released source-switch requirements consistent between the mapping artifact and the realization-pin? [Consistency, contracts/conformance-artifacts.md]
- [ ] CHK019 Is the evidence-ID convention consistent with the acceptance map's `evidence_id_template: TEST-{scenario_id}`? [Consistency, Spec §FR-034, acceptance map]
- [ ] CHK020 Are the realization coordinates consistent with constitution Principle VI's five-value release identity? [Consistency, Spec §FR-005, constitution §VI]

## Scenario Coverage (Primary / Alternate / Exception / Recovery / Non-Functional)

- [ ] CHK021 [Primary] Are requirements defined for the fully-mapped, fully-passing conformance run? [Coverage, Spec §SC-001/002]
- [ ] CHK022 [Exception] Are requirements defined for an applicable ACR scenario that is unmapped and lacks a disposition (must fail)? [Coverage, Spec §FR-034, §ARR-008-S01]
- [ ] CHK023 [Exception] Are requirements defined for a dangling mapping (references a non-existent test node)? [Coverage, Spec §Clarifications Q6]
- [ ] CHK024 [Exception] Are requirements defined for a skipped-required or reordered test producing changed results? [Coverage, Spec §FR-034, §ARR-008-S02]
- [ ] CHK025 [Alternate] Are requirements defined for accepting a kernel variance that reopens only the named acceptance IDs? [Coverage, Spec §FR-006, §ARR-002-S04]
- [ ] CHK026 [Recovery] Are requirements defined for correcting mapped behavior when canonical fixtures diverge from provisional? [Recovery, Spec §FR-035, §ARR-008-S03]
- [ ] CHK027 [Non-Functional] Is the digest/commit verification of the acceptance source specified as a precondition, not optional? [Coverage, Spec §FR-034a]
- [ ] CHK028 [Edge] Is behavior specified when the acceptance source's `expected_scenario_count` disagrees with the enumerated scenarios? [Edge Case, Gap]

## Acceptance Criteria & Traceability

- [ ] CHK029 Do conformance success criteria (SC-001, SC-002, SC-006) each map to functional requirements? [Traceability, Spec §SC-001/002/006]
- [ ] CHK030 Is there a bidirectional traceability requirement (scenario→test and test→scenario) so dangling tests are caught? [Traceability, Spec §Clarifications Q6]
- [ ] CHK031 Are ARR-008 scenarios (unmapped, order-change, canonical-vs-provisional, sibling-file-change) all reflected in requirements? [Traceability, Spec §US2, acceptance map]

## Dependencies & Assumptions

- [ ] CHK032 Is the dependency on the sibling-owned acceptance maps (read-only, never edited) documented? [Dependency, Spec §FR-036, §Dependencies]
- [ ] CHK033 Is the assumption that the shared baseline map is present and digest-stable during parallel work validated/stated? [Assumption, Spec §Assumptions, §Dependencies]
- [ ] CHK034 Is the assumption that ARR IDs (8 requirements / 34 scenarios) are fixed by the runtime acceptance map documented? [Assumption, acceptance map]

## Ambiguities & Conflicts

- [ ] CHK035 Is it unambiguous whether an `ACR-*` scenario with no runtime surface is "non_applicable" versus simply out of scope? [Ambiguity, Spec §FR-034, design Non-Goals]
- [ ] CHK036 Is there any conflict between "F0 variance reopens only mapped tests" and "conformance fails on any missing mapping"? [Conflict, Spec §FR-006, §Dependencies]

## Notes

- These items test whether the conformance/traceability *requirements* are complete and unambiguous — not whether the checker runs green.
