# Governance, Lifecycle & Release Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for document
lifecycle status, ownership boundaries, read-only kernel consumption, and the
serialized content-addressed release. "Unit tests for the requirements" —
checking whether the governance requirements are complete, clear, consistent,
and measurable, NOT whether a release is cut.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / release governance

## Requirement Completeness

- [ ] CHK001 Are the five owned artifacts explicitly enumerated as this feature's write scope (standard, profile schema, template, examples, validator)? [Completeness, Spec §US1/plan Structure Decision]
- [ ] CHK002 Is the read-only consumption boundary for kernel registries (capability, outcome, consent-purpose, state) fully stated? [Completeness, Spec §FR-017, §FR-021]
- [ ] CHK003 Are the serialized final-release steps enumerated (rebase, allocate next bundle version at realization, atomic manifest/CHANGELOG/README, matching annotated tag)? [Completeness, Spec §FR-024]
- [ ] CHK004 Is the "no version pre-reserved in the proposal" requirement present? [Completeness, Spec §FR-024, Constitution §VI]
- [ ] CHK005 Is the set of files that MUST NOT change during parallel work enumerated (kernel, reference-runtime, F0, DomainxFactory, Flutter, deployment, shared contract metadata)? [Completeness, Spec §FR-024, §SC-007]
- [ ] CHK006 Is the document `Status:` lifecycle transition (draft → ratified + Ratified by) specified as a deliberate step? [Completeness, Constitution §III, plan Constitution Check]

## Requirement Clarity

- [ ] CHK007 Is "serialized after the kernel release" unambiguous about ordering vs parallel work? [Clarity, Spec §FR-024, §US4]
- [ ] CHK008 Is "atomically for the profile-schema revision" clear about which files change together? [Clarity, Spec §FR-024, Constitution §VI]
- [ ] CHK009 Is "allocate the next available bundle version at realization" clear about timing (never reserved)? [Clarity, Spec §FR-024]
- [ ] CHK010 Is "accepted kernel variance reopens only mapped UI fields" precise about what may change? [Clarity, Spec §US4]

## Requirement Consistency

- [ ] CHK011 Is the ownership boundary consistent between the spec Assumptions, the plan Project Structure, and the deferred Phase 3? [Consistency, plan §Phases]
- [ ] CHK012 Are the content-addressed release coordinates (tag + commit + digests) consistent between FR-024, FR-025, and FR-021? [Consistency, Spec §FR-021, §FR-024, §FR-025]
- [ ] CHK013 Is the single-Speckit-feature-per-OpenSpec-change mapping consistent (no duplicated task lists)? [Consistency, Constitution §II]

## Acceptance Criteria Quality

- [ ] CHK014 Is there a measurable criterion of zero edits to kernel/reference-runtime/F0/DomainxFactory/Flutter/deployment files during parallel work? [Measurability, Spec §SC-007]
- [ ] CHK015 Is there a measurable criterion that manifest/CHANGELOG/README change together for exactly one profile-schema revision? [Measurability, Spec §SC-007]
- [ ] CHK016 Is OpenSpec strict validation (target and `--all`) named as a pass/fail gate? [Measurability, Spec §SC-008]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK017 Primary: Are requirements defined for the serialized release landing atomically with the next bundle version and a matching tag? [Coverage, Spec §US4]
- [ ] CHK018 Exception: Are requirements defined for registry drift between the parallel baseline and released IDs failing closed in realization mode? [Coverage, Exception Flow, Spec §FR-021, §US4]
- [ ] CHK019 Recovery: Are requirements defined for consuming an accepted kernel variance without editing sibling kernel paths? [Coverage, Recovery, Spec §US4]
- [ ] CHK020 Alternate: Are requirements defined for parallel work proceeding against the frozen baseline without the kernel release? [Coverage, Spec §Assumptions, research §D13]

## Edge Case Coverage

- [ ] CHK021 Is the boundary of a movable branch/tag (not a compatibility pin) addressed (consumers pin exact commit + digests)? [Edge Case, Constitution §VI, Spec §FR-025]
- [ ] CHK022 Is the case of parallel siblings touching shared release metadata addressed (serialize final integration commits)? [Edge Case, Constitution §Workflow, Spec §FR-024]
- [ ] CHK023 Is the aggregation-repo submodule pin update scoped OUT of this feature? [Edge Case, plan Constitution Check §Repo Constraints]

## Dependencies & Assumptions

- [ ] CHK024 Is the dependency on the AVC kernel release existing before Phase 3 documented? [Assumption, Spec §Assumptions, §US4]
- [ ] CHK025 Is the assumption that the validator is a governed, ratified validator (permitted runtime code) documented? [Assumption, plan Constitution Check §Repo Constraints]
- [ ] CHK026 Is the doc-index linkage requirement (new docs/fixtures README indexed in repo README) captured? [Assumption, Constitution §IV, plan §IV]

## Ambiguities & Conflicts

- [ ] CHK027 Is there any ambiguity about whether shared contract metadata may be touched during parallel work? [Ambiguity, Spec §FR-024]
- [ ] CHK028 Is there any conflict between allocating a bundle version and the "never pre-reserved" rule that must be resolved? [Conflict, Constitution §VI, Spec §FR-024]
- [ ] CHK029 Is the `Status:` header claim (draft vs ratified) consistent with what backs it (this OpenSpec change) to avoid an unbacked `standard` claim? [Conflict, Constitution §III]
