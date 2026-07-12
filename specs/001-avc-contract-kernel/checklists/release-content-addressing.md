# Release & Content-Addressing Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for the
content-addressed release — bundle identity, per-file digest scope, versioning,
tag, shared metadata, and consumer pinning. Tests whether the release
requirements are complete, unambiguous, consistent with the versioning policy,
and measurable.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Are all five coordinated release values required (per-file `contract_schema_version`, `contract_bundle_version`, annotated tag, exact commit + per-file digests, CHANGELOG entry)? [Completeness, Spec §FR-022/§FR-024; Constitution §VI]
- [x] CHK002 Is the exact membership of the per-file-digested semantic consumed set enumerated (8 schemas, shared-defs, 9 registries, fixtures+index, acceptance map, interface-lock, evidence register)? [Completeness, Spec §FR-022 (Q1); data-model §H]
- [x] CHK003 Is it stated which artifacts ship in the commit but are NOT pinned-semantic (validator, redaction config)? [Completeness, plan Design Note 3; research §D7]
- [x] CHK004 Are the three shared metadata files (`manifest.yaml`, `CHANGELOG.md`, `README.md`) and their atomic-update requirement specified? [Completeness, Spec §FR-024]
- [x] CHK005 Is the requirement that version is allocated only at realization (never reserved in the proposal) stated? [Completeness, Spec §FR-024/§Out of Scope; Constitution §VI]
- [x] CHK006 Are consumer pinning obligations (exact commit + per-file digests) fully specified? [Completeness, Spec §FR-023/§SC-006]

## Requirement Clarity

- [x] CHK007 Is "the same realized bundle" defined clearly enough to test disagreement among manifest/changelog/tag/commit/digests? [Clarity, Spec §FR-022; SCO-001-S02]
- [x] CHK008 Is "a tag alone is not a content-addressed pin" unambiguous (tag-only pin fails conformance)? [Clarity, Spec §FR-023/§SC-006; SCO-001-S03]
- [x] CHK009 Is the additive-change classification (minor increment) clearly tied to the versioning policy rather than restated ambiguously? [Clarity, research §D10; docs/contract-versioning-policy.md]
- [x] CHK010 Is the projected `contract-v1.7` clearly labeled as provisional (actual number at realization after merge order)? [Clarity, plan §Structure Decision/research §D7]

## Requirement Consistency

- [x] CHK011 Is the enumerated digested set consistent across spec FR-022, research §D7, and data-model §H? [Consistency, Spec §FR-022; research §D7; data-model §H]
- [x] CHK012 Is the "shared metadata touched only at serialized final step" rule consistent with the parallel-workstream ownership (UI sibling touches them later)? [Consistency, Spec §Assumptions; plan §Constraints]
- [x] CHK013 Are the digest-scope decisions consistent with the redaction-config-is-tooling decision (redaction files not in the digested set)? [Consistency, plan Design Note 3]

## Acceptance Criteria Quality (Measurability)

- [x] CHK014 Is bundle-identity agreement measurable (all five values identify one realized bundle; mismatch fails in 100% of checks)? [Measurability, Spec §SC-006]
- [x] CHK015 Is "every file in the consumed set carries a per-file digest" measurable as an absolute? [Measurability, Spec §SC-006]
- [x] CHK016 Is portable-consumer conformance measurable without the Python validator (any draft-2020-12 implementation, 0 extra coordination)? [Measurability, Spec §SC-009; §FR-023]

## Scenario & Edge-Case Coverage

- [x] CHK017 Are requirements defined for release-identity disagreement (validation fails, consumers not told to upgrade)? [Coverage, Spec US3-AS1; SCO-001-S02]
- [x] CHK018 Are requirements defined for a consumer recording only a tag (conformance fails)? [Coverage, Spec US3-AS2; SCO-001-S03]
- [x] CHK019 Are requirements defined for consumer models drifting from the pinned fixtures (release validation fails)? [Coverage, Spec US3-AS3; SCO-001-S04]
- [x] CHK020 Is the rollback-before-vs-after-publication behavior specified (delete unreleased vs new additive/breaking release)? [Coverage, Recovery, quickstart §5; design.md Migration Plan]
- [x] CHK021 Is the recovered-legacy baseline (`contract-v1.1..v1.6` with no tags; next realized allocates next minor) accounted for? [Edge Case, docs/contract-versioning-policy.md; research §D7]

## Dependencies & Assumptions

- [x] CHK022 Is the dependency on `docs/contract-versioning-policy.md` and constitution Principle VI stated rather than re-derived? [Dependency, Spec §Dependencies]
- [x] CHK023 Is the assumption that the aggregation-repo pin is a later, separate sync step (not this feature) documented? [Assumption, plan §Constitution Check Repository Constraints]

## Ambiguities & Conflicts

- [x] CHK024 Is there any ambiguity about whether the acceptance map / evidence register / interface-lock are part of the pinned set — and is inclusion stated unambiguously? [Ambiguity, Spec §FR-022; data-model §H]
- [x] CHK025 Does the two-completion-state model (pending F0 vs realized) conflict with "release identified by a tag"? Is it clear the tag exists only at realization? [Conflict, Spec §FR-034; research §D7]
