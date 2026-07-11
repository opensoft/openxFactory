# Schema & Compatibility Integrity Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for the profile
schema's field shapes, closed defaults, backward compatibility, and
content-addressed runtime compatibility. "Unit tests for the requirements" —
checking whether the schema requirements are complete, clear, consistent, and
measurable, NOT whether YAML parses.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / contracts

## Requirement Completeness

- [ ] CHK001 Is the full set of carrier blocks the profile must add enumerated (runtime compatibility, surface default, interaction mode, speech gate, timing, outcome/fallback slots, media-authorization pending, consent-purpose mappings, persona reference, retention overlay, accessibility baseline, handoff roles)? [Completeness, Spec §FR-013]
- [ ] CHK002 Is the content-addressed runtime-compatibility coordinate set fully specified for both phases (baseline identity + digests; released tag + commit + registry/interface-lock digests)? [Completeness, Spec §FR-025]
- [ ] CHK003 Is the requirement that no second hand-maintained capability list is introduced explicitly stated? [Completeness, Spec §FR-025, research §D5]
- [ ] CHK004 Are the timing requirements complete (selected readiness/heartbeat/lease values carried; ceilings kernel-owned; fail closed on unresolvable bound)? [Completeness, Spec §FR-026]
- [ ] CHK005 Are the persona-reference fields fully specified (persona id, version, optional non-secret catalog locator)? [Completeness, Spec §FR-011, §FR-013]
- [ ] CHK006 Are the retention-overlay fields fully specified (external policy references + presentation flags/labels; no inline durations)? [Completeness, Spec §FR-027]
- [ ] CHK007 Is the requirement that the schema carries `schema_version` and `kind` and remains a registered contract present? [Completeness, Spec §FR-017, Constitution §IV]

## Requirement Clarity

- [ ] CHK008 Is "additive with a closed default" defined as "omitted new field resolves to the most restrictive fail-closed value"? [Clarity, Spec §FR-016, §Assumptions]
- [ ] CHK009 Is "no loose released version range" unambiguous vs the allowed parallel-baseline identity? [Clarity, Spec §FR-025]
- [ ] CHK010 Is the reserved/forbidden interaction-mode taxonomy clear (provider_vad default; server_vad reserved; push_to_talk reserved+disabled with required fallback)? [Clarity, Spec §FR-015]
- [ ] CHK011 Is "non-secret catalog locator" defined precisely enough to reject a tokenized/secret locator? [Clarity, Spec §FR-011, research §D7]
- [ ] CHK012 Is the consent-purpose mapping shape clear (references three neutral IDs + optional stricter domain IDs; no consent evidence)? [Clarity, Spec §FR-014]

## Requirement Consistency

- [ ] CHK013 Do FR-013 (field list) and the schema outline in `contracts/profile-schema-outline.md` list the same blocks with matching closed defaults? [Consistency, contracts/profile-schema-outline.md]
- [ ] CHK014 Are existing required top-level keys preserved unchanged, consistent with the additive-only claim? [Consistency, Spec §FR-016, research §D12]
- [ ] CHK015 Is the persona model consistent across FR-011, FR-013, the key entity, and the compatibility strategy (reference-only forward; legacy embedded catalog still accepted)? [Consistency, research §D7]
- [ ] CHK016 Are timing/ceiling ownership statements consistent between FR-013, FR-026, and FR-021 (read-only kernel resolution)? [Consistency, Spec §FR-013, §FR-021, §FR-026]

## Acceptance Criteria Quality

- [ ] CHK017 Is there a measurable criterion that 100% of existing static profiles remain valid, confirmed by ≥1 compatibility fixture? [Measurability, Spec §SC-003]
- [ ] CHK018 Is there a measurable criterion that the validator reports zero fields defaulting open? [Measurability, Spec §SC-004]
- [ ] CHK019 Can "every referenced ID validated against exact bytes" be objectively verified? [Measurability, Spec §FR-021, §FR-025]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK020 Primary: Are requirements defined for a full profile that carries every new block and passes with full field coverage reported? [Coverage, Spec §US1]
- [ ] CHK021 Alternate: Are requirements defined for a legacy/static profile (pre-alignment) that omits new fields and stays valid? [Coverage, Spec §US1, Edge Cases]
- [ ] CHK022 Exception: Are requirements defined for an out-of-range readiness/heartbeat/lease value failing closed? [Coverage, Exception Flow, Spec §FR-026]
- [ ] CHK023 Exception: Are requirements defined for an unresolvable persona / retention / consent-purpose reference failing closed? [Coverage, Exception Flow, Spec §FR-011, §FR-014, §FR-027]
- [ ] CHK024 Recovery: Are requirements defined for consuming an accepted kernel variance through mapped UI fields only (no sibling edits)? [Coverage, Recovery, Spec §US4]

## Edge Case Coverage

- [ ] CHK025 Is the boundary of a released profile missing runtime-compatibility coordinates addressed (must carry them)? [Edge Case, Spec §FR-025]
- [ ] CHK026 Is the case of a reserved mode selected without a fallback covered? [Edge Case, Spec §FR-015]
- [ ] CHK027 Is a legacy embedded `persona_catalog` alongside a new `persona_reference` addressed (precedence / deprecation)? [Edge Case, research §D7]

## Dependencies & Assumptions

- [ ] CHK028 Is the assumption that the schema is already registered in `contracts/manifest.yaml` documented? [Assumption, Spec §Assumptions]
- [ ] CHK029 Is the dependency on kernel-owned ceilings/registries (read-only) stated for both baseline and realization resolution? [Assumption, Spec §FR-021, §FR-026]

## Ambiguities & Conflicts

- [ ] CHK030 Is there any ambiguity about whether new blocks are optional or required? [Ambiguity, Spec §FR-016]
- [ ] CHK031 Is there a potential conflict between "reference-only persona" (Q1) and "existing static profiles remain valid" (FR-016) that the compatibility strategy must resolve explicitly? [Conflict, research §D7]
