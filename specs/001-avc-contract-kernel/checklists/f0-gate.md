# F0 Publication-Gate Correctness Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for the F0
publication gate — pinned F0-owned evidence schemas, digest/commit verification,
fail-closed conditions, and the parallel-work-vs-tag-block boundary. Tests whether
the gate requirements are complete, unambiguous, measurable, and fail-closed.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Is F0 ownership of both evidence schemas (`f0-results.schema.yaml`, `f0-interface-impact.schema.yaml`) stated, with the kernel explicitly NOT co-owning them? [Completeness, Spec §FR-033 (Q6); plan Design Note 2]
- [x] CHK002 Is the pin content fully specified (F0 source commit + both schema SHA-256 digests) and its storage location (`interface-lock.yaml` `f0_evidence_pin` block)? [Completeness, Spec §FR-033; data-model §E]
- [x] CHK003 Are all gate steps enumerated (resolve pinned schemas → verify digests/commit → validate instances → read PASS/dispositions)? [Completeness, research §D6; quickstart §4]
- [x] CHK004 Is the complete set of fail-closed triggers enumerated (missing schema, digest mismatch, commit mismatch, instance validation failure, unknown status, unknown variance field)? [Completeness, Spec §FR-033/§SC-010]
- [x] CHK005 Are the F0 outcomes that block the tag enumerated (absent, FAIL, INCONCLUSIVE, undispositioned variance)? [Completeness, Spec §FR-029/§SC-007]
- [x] CHK006 Is the mandatory F0 evidence content (answer ordering, sideband-failure containment, readiness timing, five-second hangup) specified as a publication precondition? [Completeness, Spec §FR-031]

## Requirement Clarity

- [x] CHK007 Is the boundary between "parallel implementation may proceed" and "tag is blocked" unambiguous? [Clarity, Spec §FR-029; ACR-012-S02]
- [x] CHK008 Is "fail closed" defined operationally (the gate refuses the tag; it does not warn-and-continue)? [Clarity, Spec §SC-010; research §D6]
- [x] CHK009 Is "disposition" of an interface variance defined precisely enough to be checkable? [Clarity, Spec §FR-029; workstream variance protocol]
- [x] CHK010 Is "unknown variance field" clearly a fail trigger (schema-validated against the pinned F0 schema), not a tolerated extra? [Clarity, Spec §FR-033]

## Requirement Consistency

- [x] CHK011 Is the F0-owns-schemas decision consistent across spec (FR-033), research (§D6), plan (Design Note 2), and Out of Scope? [Consistency, Spec §FR-033/§Out of Scope; research §D6]
- [x] CHK012 Is the pin's placement in `interface-lock.yaml` consistent with interface-lock being part of the digested consumed set? [Consistency, plan §Structure Decision; data-model §E/§H]
- [x] CHK013 Does the gate's "validate instances against pinned schemas" align with the general "validate against a conformant draft-2020-12 schema" approach (no special-casing)? [Consistency, research §D1/§D6]

## Acceptance Criteria Quality (Measurability)

- [x] CHK014 Is "0 tags published under adverse F0 conditions" measurable? [Measurability, Spec §SC-007]
- [x] CHK015 Is "gate fails closed in 100% of adverse F0 cases" expressed as a measurable, enumerable set of cases? [Measurability, Spec §SC-010]
- [x] CHK016 Is "never treats the change as realized before tag + digests exist" objectively verifiable? [Measurability, Spec §SC-010/§FR-034]

## Scenario & Edge-Case Coverage

- [x] CHK017 Are requirements defined for a digest mismatch on a pinned F0 schema (tag blocked)? [Edge Case, Spec §Edge Cases "F0 evidence shape mismatch"]
- [x] CHK018 Are requirements defined for an F0 evidence instance that claims PASS but fails schema validation? [Coverage, Exception, Spec §Edge Cases; §FR-033]
- [x] CHK019 Are requirements defined for a source-commit mismatch between the pin and the F0 change? [Edge Case, data-model §E; research §D6]
- [x] CHK020 Are requirements defined for incomplete deterministic-lab evidence blocking live qualification (ring ordering)? [Coverage, Spec US4-AS3; ACR-012-S01]
- [x] CHK021 Is the recovery path defined when F0 reports a variance (update interface-lock only in this change, notify siblings)? [Recovery, Spec §FR-030; workstream variance protocol]

## Dependencies & Assumptions

- [x] CHK022 Is the dependency on the sibling `qualify-avatar-brokered-call-feasibility` (its commit + schema artifacts) stated as the external input? [Dependency, Spec §Dependencies/§FR-033]
- [x] CHK023 Is the assumption that the F0 schema files are resolvable from the F0 change path at gate time documented (and its failure mode = fail closed)? [Assumption, research §D6; quickstart §4]

## Ambiguities & Conflicts

- [x] CHK024 Is there any ambiguity about whether the kernel may proceed to realization on `INCONCLUSIVE` with a disposition? Is it clear that only PASS + full disposition unblocks the tag? [Ambiguity, Spec §FR-029]
- [x] CHK025 Does "F0 owns schemas" conflict anywhere with the kernel validating against them? Is it clear pinning+validating ≠ owning? [Conflict, Spec §FR-033; plan Design Note 2]
