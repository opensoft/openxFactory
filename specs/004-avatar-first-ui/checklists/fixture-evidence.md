# Fixture & Evidence Coverage Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for deterministic
fixtures, negative-fixture rule coverage, stable error/evidence IDs, and
requirement-to-evidence traceability. "Unit tests for the requirements" —
checking whether the evidence requirements are complete, clear, consistent, and
measurable, NOT whether fixtures run.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / QA-governance

## Requirement Completeness

- [ ] CHK001 Is the deterministic fixture shape fully specified (fixed clock, IDs, font, locale, platform capabilities, canonical AVC command/event/snapshot inputs, expected view-state/record shapes, AFU evidence IDs)? [Completeness, Spec §FR-023]
- [ ] CHK002 Is the fixtures location (`examples/avatar-first-ui/fixtures/`) explicitly stated and distinct from the profile examples? [Completeness, Spec §FR-023]
- [ ] CHK003 Is the required negative-fixture set defined as ≥1 per enforced rule class, with the rule classes enumerated? [Completeness, Spec §FR-019]
- [ ] CHK004 Is the compatibility-fixture requirement (≥1 pre-alignment profile that stays valid) present? [Completeness, Spec §FR-019, §SC-003]
- [ ] CHK005 Is the requirement that each `AFU-*` requirement/scenario maps to owned evidence or a named successor complete for all 8 requirements / 25 scenarios? [Completeness, Spec §FR-022, §SC-001]
- [ ] CHK006 Are the successor-owned evidence classes (Flutter widget, golden, platform-accessibility, live-provider) explicitly excluded from this feature's claims? [Completeness, Spec §FR-022]

## Requirement Clarity

- [ ] CHK007 Is "stable error/evidence ID" defined precisely (each negative fixture fails exactly one primary rule with a stable ID)? [Clarity, Spec §FR-019, §FR-020]
- [ ] CHK008 Is "deterministic" defined by an observable property (identical inputs → equivalent shapes + identical evidence IDs across two runs)? [Clarity, Spec §SC-006]
- [ ] CHK009 Is the distinction between automated, manual, and successor evidence types unambiguous? [Clarity, Spec §FR-022, acceptance-map]
- [ ] CHK010 Is "canonical AVC command/event/snapshot inputs" clear that no provider DTO/model name is used? [Clarity, Spec §FR-023, §US3]

## Requirement Consistency

- [ ] CHK011 Do the rule classes in `contracts/validator-rules.md` match the negative-fixture list in `contracts/fixture-shape.md`? [Consistency, contracts/]
- [ ] CHK012 Are the stable error IDs consistent between the data-model catalog, the validator rules, and the fixtures' `expect_error`? [Consistency, data-model.md, contracts/validator-rules.md]
- [ ] CHK013 Is the acceptance-map count (8 requirements / 25 scenarios) consistent between the spec, SC-008, and the supporting-docs map? [Consistency, Spec §SC-008]

## Acceptance Criteria Quality

- [ ] CHK014 Is there a measurable criterion that the validator passes on the template + four examples + compatibility fixture and fails on every negative fixture? [Measurability, Spec §SC-002]
- [ ] CHK015 Is there a measurable criterion for byte-stable verdict/error-IDs/expected-shapes across two identical runs? [Measurability, Spec §SC-006]
- [ ] CHK016 Is acceptance-map parity expressed as an objectively countable check (8/25)? [Measurability, Spec §SC-008, quickstart §4]
- [ ] CHK017 Is 100%-of-requirements-owned expressed as zero unowned items? [Measurability, Spec §SC-001]

## Scenario Coverage (Primary / Alternate / Exception)

- [ ] CHK018 Primary: Are requirements defined for replaying the same fixture/seed/decisions/contract-version twice yielding equivalent canonical shapes? [Coverage, Spec §US3]
- [ ] CHK019 Exception: Are requirements defined for a widget/golden test depending on a provider DTO/model name being rejected by architecture validation? [Coverage, Exception Flow, Spec §US4/§FR-022 (successor-owned, referenced)]
- [ ] CHK020 Exception: Are requirements defined for a required viewport/accessibility mode/control-loss/confirmation/handoff state lacking evidence marking the slice incomplete? [Coverage, Exception Flow, Spec §US3 acceptance]
- [ ] CHK021 Alternate: Are requirements defined for a deferred scenario retaining a named successor owner + closed default? [Coverage, Spec §US3]

## Edge Case Coverage

- [ ] CHK022 Is one negative fixture per enforced rule class (nine, incl. retention-unresolved) listed so no enforced rule is left without fixture-level evidence? [Edge Case, Coverage, contracts/validator-rules.md]
- [ ] CHK023 Is the boundary of a fixture referencing an unknown `AFU-*` scenario ID addressed (parity failure)? [Edge Case, contracts/validator-rules.md]
- [ ] CHK024 Is the held-answer-rendered-as-active negative case explicitly required as a fixture? [Edge Case, Spec §FR-008, §FR-019]
- [ ] CHK029 Is the unresolvable-retention-policy-reference case required as a dedicated negative fixture (`AFUV-RETENTION-UNRESOLVED`) enforcing FR-027's fail-closed rule? [Edge Case, Spec §FR-027, §FR-019]
- [ ] CHK030 Is the evidence-ID convention specified (fixtures declare `AFU-*` scenario IDs; evidence IDs derive via the acceptance map's `TEST-{scenario_id}` template)? [Clarity, Consistency, contracts/fixture-shape.md]

## Dependencies & Assumptions

- [ ] CHK025 Is the assumption that fixtures use no live model/provider/clock/RNG documented? [Assumption, Spec §Assumptions, §FR-023]
- [ ] CHK026 Is the dependency on the OpenSpec acceptance map (supporting-docs) as the parity source documented? [Assumption, quickstart §4]

## Ambiguities & Conflicts

- [ ] CHK027 Is there any ambiguity about whether fixtures live under examples/ vs a top-level fixtures/ directory? [Ambiguity, Spec §FR-023, plan Project Structure]
- [ ] CHK028 Is there any conflict between "no golden tests here" and the deterministic-shape requirement (shapes vs pixel goldens)? [Conflict, Spec §FR-023, §US3]
