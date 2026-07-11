# Redaction & Security Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for redaction /
secret-exclusion, bounded synthetic sentinels, and fail-closed authority — tests
whether the security requirements are complete, unambiguous, measurable, and
aligned to the threat model and constitution Principle VII.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [ ] CHK001 Are both redaction layers (structural schema exclusion AND committed-content scan) required, not just one? [Completeness, Spec §FR-018 (Q3); research §D4]
- [ ] CHK002 Is the prohibited-content set enumerated (credential, SDP, raw provider payload, raw transcript/media, prohibited high-cardinality identifier)? [Completeness, Spec §FR-018/§SC-008]
- [ ] CHK003 Are the scan surfaces specified (fixtures AND evidence AND all committed `contracts/avatar-client/` files)? [Completeness, Spec §FR-018/§FR-020; data-model §G]
- [ ] CHK004 Is a requirement present that the denylist patterns are themselves a versioned, reviewable artifact? [Completeness, data-model §G]
- [ ] CHK005 Is the bounded-sentinel mechanism (declared reserved forms in `sentinels.yaml`) required for any synthetic secret used in adversarial fixtures? [Completeness, Spec §FR-018 (Q3); research §D4]

## Requirement Clarity

- [ ] CHK006 Is "structurally invalid where prohibited" defined concretely (e.g., prohibited fields absent, `additionalProperties: false`) rather than aspirational? [Clarity, research §D4; data-model §A]
- [ ] CHK007 Is "bounded so it cannot become a bypass" quantified (reserved prefix + fixed/max length) so it is testable? [Clarity, Spec §FR-018; research §D4; data-model §G]
- [ ] CHK008 Is "prohibited high-cardinality identifier" defined precisely enough to distinguish it from permitted references (opaque IDs, digests)? [Clarity, Ambiguity, Spec §FR-018]
- [ ] CHK009 Is the distinction clear between permitted opaque references (attachment reference, offer fingerprint) and prohibited raw content? [Clarity, Spec §FR-016; data-model §A]

## Requirement Consistency

- [ ] CHK010 Does the redaction requirement align with the credential-free non-grant requirement (FR-007) without gaps between them? [Consistency, Spec §FR-007/§FR-018]
- [ ] CHK011 Is the telemetry-redaction expectation (ACR-011) consistent with the committed-file scan (SC-008) so neither contradicts the other? [Consistency, Spec §SC-008; ACR-011-S01]
- [ ] CHK012 Are the "no raw credentials anywhere in the tree" constitution rule and the sentinel exception reconciled (bounded sentinels are not real credentials)? [Consistency, Constitution §IV/§VII; research §D4]

## Acceptance Criteria Quality (Measurability)

- [ ] CHK013 Is the secret-exclusion outcome measurable as an absolute (0 committed files pass while containing prohibited content)? [Measurability, Spec §SC-008]
- [ ] CHK014 Is the "unbounded sentinel that widens into a real pattern fails" outcome expressed as a testable criterion? [Measurability, Spec §SC-008; §Edge Cases]
- [ ] CHK015 Are the structural-exclusion outcomes measurable per-schema (denial/terminal cannot validate with a secret)? [Measurability, Spec §SC-005]

## Scenario & Edge-Case Coverage

- [ ] CHK016 Are requirements defined for a secret pasted into an otherwise-valid fixture (scan must catch it)? [Coverage, research §D4; Spec §SC-008]
- [ ] CHK017 Are requirements defined for a sentinel that exceeds its bounded form (must fail, not bypass)? [Edge Case, Spec §Edge Cases "Bounded test sentinel"]
- [ ] CHK018 Are adversarial fixtures required as a first-class scenario class for every schema? [Coverage, Spec §FR-019; data-model §F]
- [ ] CHK019 Are requirements defined for redaction of telemetry/log/support-bundle artifacts that a consumer might commit as evidence? [Coverage, Spec §SC-008; ACR-011-S01]
- [ ] CHK020 Is the fail-closed default for deferred/unknown security-relevant vocabulary covered (Principle VII)? [Coverage, Spec §FR-008; Constitution §VII]

## Dependencies & Assumptions

- [ ] CHK021 Is the dependency on the registered threat model (accepted before publication) stated as a security precondition? [Dependency, Spec §Dependencies/§FR-031]
- [ ] CHK022 Is the assumption that the reference validator's denylist is authoritative-yet-tooling (unpinned) documented, so security posture does not silently depend on an unpinned file? [Assumption, plan Design Note 3]

## Ambiguities & Conflicts

- [ ] CHK023 Is there residual ambiguity about who owns the denylist pattern set and how it is updated safely? [Ambiguity, data-model §G]
- [ ] CHK024 Does placing redaction config outside the per-file-digested set conflict with the guarantee that redaction is reproducible? Is that trade-off explicitly justified? [Conflict, plan Design Note 3]
