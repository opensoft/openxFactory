# Acceptance-Evidence Traceability Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for the acceptance
map, the consolidated evidence/disposition register, self-describing fixtures,
and the validator's parity/traceability checks. Tests whether the traceability
requirements are complete, unambiguous, measurable, and cover every evidence type.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Is the acceptance map required to cover every normative requirement AND scenario across all three deltas (ACR/SCO/RBG)? [Completeness, Spec §FR-021/§SC-003]
- [x] CHK002 Is the parity target (17 requirements / 72 scenarios) stated as the authoritative count? [Completeness, Spec §SC-003/§Assumptions; acceptance map]
- [x] CHK003 Is the consolidated evidence/disposition register required with a resolution for every evidence type (automated, manual, live_f0, successor)? [Completeness, Spec §FR-032 (Q4); data-model §D]
- [x] CHK004 Are the required fields per evidence type specified (automated→fixture id; manual→result+reviewer+disposition; live_f0/successor→owner change + fail-closed default)? [Completeness, Spec §FR-032; research §D5]
- [x] CHK005 Is the fixture-case envelope (target, target_kind, expect, scenario_ids, evidence_id, instance) fully specified? [Completeness, research §D2; data-model §F]
- [x] CHK006 Is the fixture coverage matrix specified (valid/invalid/boundary/compatibility/unknown-field/unknown-authority/redaction/adversarial per schema, plus per owned scenario)? [Completeness, Spec §FR-019; data-model §F]
- [x] CHK007 Is a machine-readable `fixtures/index.yaml` required so the suite is enumerable? [Completeness, research §D2; data-model §F]

## Requirement Clarity

- [x] CHK008 Is "evidence-free" defined precisely for each evidence type so the validator's failure condition is testable? [Clarity, Spec §FR-020/§FR-032; research §D5]
- [x] CHK009 Is "self-describing fixture" defined concretely (declares target + expect + stable IDs) rather than by intent? [Clarity, Spec §FR-019 (Q5); research §D2]
- [x] CHK010 Are the allowed evidence-register status transitions defined as an explicit graph (planned→evidenced→accepted; planned→deferred)? [Clarity, data-model §D; research §D5]
- [x] CHK011 Is "renamed" scenario failure clearly distinguished from "missing" and "duplicated"? [Clarity, Spec §FR-020; ACR-012-S03]

## Requirement Consistency

- [x] CHK012 Is the acceptance-map location (realized under `contracts/avatar-client/`) consistent between spec, plan, data-model, and the traceability supporting-doc? [Consistency, data-model §C; plan §Structure]
- [x] CHK013 Are evidence IDs consistent between the acceptance map, the evidence register, and `fixtures/index.yaml` (e.g., `TEST-<scenario>`)? [Consistency, data-model §C/§D/§F]
- [x] CHK014 Is the bijective mapping (one register entry per acceptance-map scenario) stated consistently so counts cannot diverge? [Consistency, data-model §D; Spec §SC-003]
- [x] CHK015 Do the "owned by this change" fixture obligations (FR-019) and the sibling `owner_changes` in the map reconcile without contradiction? [Consistency, Spec §FR-019; acceptance map owner_changes]

## Acceptance Criteria Quality (Measurability)

- [x] CHK016 Is traceability measurable (0 unmapped, duplicated, renamed, or evidence-free entries)? [Measurability, Spec §SC-003]
- [x] CHK017 Is fixture conformance measurable (100% valid pass, 100% invalid/adversarial/redaction rejected)? [Measurability, Spec §SC-002]
- [x] CHK018 Can "every scenario resolves to fixture / recorded manual result / named owner + fail-closed default" be objectively verified? [Measurability, Spec §SC-003; data-model §D]

## Scenario & Edge-Case Coverage

- [x] CHK019 Are requirements defined for a scenario missing from the register (fails as evidence-free)? [Coverage, Spec §FR-032; §Edge Cases "Evidence register gap"]
- [x] CHK020 Are requirements defined for a manual scenario with no recorded result/reviewer/disposition? [Edge Case, data-model §D]
- [x] CHK021 Are requirements defined for a live_f0/successor scenario missing its owner or fail-closed default? [Edge Case, data-model §D]
- [x] CHK022 Are requirements defined for an illegal status transition in the register? [Edge Case, data-model §D; research §D5]
- [x] CHK023 Are requirements defined for a fixture referencing a non-existent evidence_id, or an index entry pointing at a missing file? [Coverage, Exception, data-model §F/§D]
- [x] CHK024 Is the non-automatable evidence class (manual/live_f0/successor) explicitly covered so it is not silently treated as automated? [Coverage, Gap, Spec §FR-032]

## Dependencies & Assumptions

- [x] CHK025 Is the dependency on stable ACR-*/SCO-*/RBG- identifiers (never renamed) stated? [Dependency, Spec §FR-021; traceability doc]
- [x] CHK026 Is the assumption that consumers execute fixtures with any draft-2020-12 implementation (no Python dependency) documented? [Assumption, Spec §FR-023 (Q5)/§Assumptions]

## Ambiguities & Conflicts

- [x] CHK027 Is there any ambiguity about whether an automated scenario may ALSO carry a manual evidence entry, or is the evidence_type single-valued per scenario? [Ambiguity, data-model §D]
- [x] CHK028 Does the requirement that the validator is "not a required consumer dependency" conflict with it being the reference runner for fixtures? Is the reconciliation explicit? [Conflict, Spec §FR-020/§FR-023]
