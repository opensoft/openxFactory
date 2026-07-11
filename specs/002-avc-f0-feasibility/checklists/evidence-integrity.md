# Evidence Integrity & Classification Requirements Checklist: 002-avc-f0-feasibility

**Purpose**: Release-gate validation of the *requirements quality* for evidence artifacts,
schema validity, terminal classification, schema ownership, and the sole evidence path.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Scope**: FR-015, FR-016, FR-018, FR-021; SC-008, SC-010, SC-011; Clarifications Q3/Q5; plan §Structure Decision

## Requirement Completeness

- [ ] CHK001 Are all three required evidence artifacts enumerated with their formats (`f0-results.json`, `f0-results.md`, `f0-interface-impact.yaml`)? [Completeness, Spec §FR-015]
- [ ] CHK002 Is the requirement to emit the interface-impact document on every run (empty `variances` on a clean pass) stated? [Completeness, Spec §FR-018/§SC-010]
- [ ] CHK003 Are the required top-level fields of the machine-readable record specified or bound to the registered schema? [Completeness, Spec §FR-015/§Key Entities]
- [ ] CHK004 Is the binding between the human-readable report and its SHA-256 in the results record specified? [Completeness, Spec §FR-015/§Key Entities]
- [ ] CHK005 Is ownership of `f0-results.schema.yaml` and `f0-interface-impact.schema.yaml` by this feature specified, with a defined home within the owned surface? [Completeness, Plan §Structure Decision]
- [ ] CHK006 Is the schema drift-guard (owned `f0-results.schema.yaml` byte-identical to the registered supporting-docs copy) specified? [Completeness, Plan §Structure Decision]
- [ ] CHK007 Is the per-variance content (affected `ACR-*` IDs, observed behavior, evidence refs, severity, proposed correction, continuation status) enumerated? [Completeness, Spec §FR-018]

## Requirement Clarity

- [ ] CHK008 Is the classification rule stated unambiguously with precedence (PASS requires all mandatory pass; any contrary observation ⇒ FAIL; missing/insufficient ⇒ INCONCLUSIVE)? [Clarity, Spec §FR-016]
- [ ] CHK009 Is "sufficient observable evidence" (the INCONCLUSIVE-vs-FAIL boundary) defined precisely enough to classify a trial deterministically? [Ambiguity, Spec §FR-016/§US3]
- [ ] CHK010 Is "at least one affected `ACR-*` ID" per variance, sourced from the digest-verified map, clearly required (no placeholders)? [Clarity, Spec §SC-010/§FR-018]

## Requirement Consistency

- [ ] CHK011 Are the classification rules consistent across FR-016, the US3 scenarios, SC-008, and the Edge Cases? [Consistency, Spec §FR-016/§US3]
- [ ] CHK012 Is the sole committed evidence location consistent across FR-015, FR-021, SC-011, Assumptions, and Clarifications Q5? [Consistency, Spec §FR-015/§SC-011]
- [ ] CHK013 Are the schema-driven counts (exactly six groups, 70 trials) consistent between FR-006 and the referenced result schema constraints? [Consistency, Spec §FR-006]

## Acceptance Criteria Quality / Measurability

- [ ] CHK014 Is schema validity measurable (validates against the registered result schema with zero errors)? [Measurability, Spec §SC-008]
- [ ] CHK015 Is "no second evidence copy" objectively checkable? [Measurability, Spec §Clarifications Q5/§FR-021]
- [ ] CHK016 Is "zero files outside the two owned locations modified by a run" objectively measurable? [Measurability, Spec §SC-011]
- [ ] CHK017 Is the "overall status is exactly one of PASS/FAIL/INCONCLUSIVE" outcome enumerable and mutually exclusive? [Measurability, Spec §SC-008]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK018 Primary — Are requirements defined for a clean PASS that still emits the interface-impact document with an empty variance list? [Coverage/Primary, Spec §US3-S1/§FR-018]
- [ ] CHK019 Exception — Are requirements defined for a contradicted mandatory assertion ⇒ overall FAIL? [Coverage/Exception, Spec §US3-S2]
- [ ] CHK020 Exception — Are requirements defined for missing mandatory evidence ⇒ INCONCLUSIVE (never PASS)? [Coverage/Exception, Spec §US3-S3]
- [ ] CHK021 Alternate — Are requirements defined for a variance requiring a neutral correction recorded without editing canonical contracts or sibling files? [Coverage/Alternate, Spec §US3-S4]
- [ ] CHK022 Recovery — Is behavior specified when the harness's own output fails schema validation (evidence not committed)? [Coverage/Recovery/Gap, Spec §SC-008]

## Edge Case Coverage

- [ ] CHK023 Is behavior specified when `report_sha256` cannot be computed/bound to the results record? [Edge Case/Gap, Spec §FR-015]
- [ ] CHK024 Is behavior specified when the interface-impact schema itself is absent or unreadable? [Edge Case/Gap, Plan §Structure Decision]
- [ ] CHK025 Is the atomic/direct write requirement for evidence specified to avoid partial artifacts? [Edge Case, Spec §FR-015]

## Dependencies & Assumptions

- [ ] CHK026 Is the dependency on the registered result schema (and its expected digest) documented? [Dependency, Spec §Dependencies/Plan]
- [ ] CHK027 Is the assumption that evidence is publishable by construction (allowlist rejects prohibited content before writing) stated? [Assumption, Spec §Assumptions]

## Ambiguities & Conflicts

- [ ] CHK028 Is a requirement/acceptance ID scheme established so every evidence artifact is traceable to FR/SC/ACR IDs? [Traceability, Spec §Requirements/§Success Criteria]
