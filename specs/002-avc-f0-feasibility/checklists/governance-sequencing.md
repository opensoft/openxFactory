# Governance, Boundary & Sequencing Requirements Checklist: 002-avc-f0-feasibility

**Purpose**: Release-gate validation of the *requirements quality* for the Definition of Done,
the non-qualification boundary, scope/ownership isolation, and the contract-kernel handoff.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Scope**: FR-004, FR-005, FR-018–FR-021; SC-011, SC-012, SC-013; US5; Clarifications Q1/Q5; Out of Scope; Plan §Constitution Check

## Requirement Completeness

- [ ] CHK001 Is the Definition of Done explicitly stated (harness + offline self-tests + redaction tests + a schema-valid terminal record), and is INCONCLUSIVE-without-key an accepted completion state? [Completeness, Spec §SC-013/§Clarifications Q1]
- [ ] CHK002 Is "feature completion is never represented as provider qualification" stated? [Completeness, Spec §SC-013/§FR-019]
- [ ] CHK003 Are the non-qualification prohibitions enumerated (no profile promotion, no internal-live/production media, no production-latency-budget satisfaction, no waiver of successor gates)? [Completeness, Spec §FR-019]
- [ ] CHK004 Is scope isolation enumerated (all code under `experiments/avatar-brokered-call/`; committed evidence only under the change's `evidence/` dir; no edits to canonical contracts, release metadata, reference-runtime, UI, DomainxFactory, or deployment files; no reusable-runtime imports)? [Completeness, Spec §FR-021/§SC-011]
- [ ] CHK005 Is the contract-kernel handoff specified (owner disposes every variance; the F0 result gates that kernel's publication; F0 cannot edit the kernel)? [Completeness, Spec §FR-018/§FR-020/§Dependencies]
- [ ] CHK006 Is the successor-change boundary (`qualify-avatar-live-voice` owns live-profile promotion, production topology, latency budgets) documented? [Completeness, Spec §FR-020/§Dependencies/§Out of Scope]
- [ ] CHK007 Is the ownership of the two F0 schema deliverables (result + interface-impact) and their placement within the owned surface specified? [Completeness, Plan §Structure Decision]

## Requirement Clarity

- [ ] CHK008 Is "the F0 result gates contract publication but does not qualify live use" stated unambiguously? [Clarity, Spec §US5/§FR-020]
- [ ] CHK009 Is the distinction between "feature completion" and "kernel publication gate opened" clear and non-conflated? [Clarity, Spec §SC-013/§US5-S1]
- [ ] CHK010 Is "provider profile remains disabled for live rings on PASS" clearly stated as a post-PASS constraint? [Clarity, Spec §US5-S1/§FR-020]

## Requirement Consistency

- [ ] CHK011 Is the non-qualification boundary consistent across US5, FR-019, FR-020, SC-012, and the Out of Scope section? [Consistency, Spec §US5/§FR-019]
- [ ] CHK012 Is the ownership/scope boundary consistent between FR-021, SC-011, Clarifications Q5, and Out of Scope? [Consistency, Spec §FR-021/§SC-011]
- [ ] CHK013 Are the two justified constitution deviations (runtime-code-under-experiments; JSON-Schema `$schema`/`$id` vs `schema_version`+`kind`) consistent with the spec's stated constraints and non-goals? [Consistency, Plan §Constitution Check/§Complexity Tracking]

## Acceptance Criteria Quality / Measurability

- [ ] CHK014 Is "zero live rings enabled from F0 evidence alone" objectively measurable? [Measurability, Spec §SC-012]
- [ ] CHK015 Is "zero files outside the two owned locations modified" objectively measurable? [Measurability, Spec §SC-011]
- [ ] CHK016 Is the completion criterion (terminal record exists + validates) objectively checkable independent of a live PASS? [Measurability, Spec §SC-013]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK017 Primary (completion) — Are requirements defined for an INCONCLUSIVE-without-key run satisfying feature completion? [Coverage/Primary, Spec §SC-013]
- [ ] CHK018 Primary (gate) — Are requirements defined for a PASS allowing the publication gate to proceed after variance disposition while the profile stays disabled for live rings? [Coverage/Primary, Spec §US5-S1]
- [ ] CHK019 Exception — Are requirements defined for an attempt to enable internal-live/production media from F0 evidence alone (rejected; requires `qualify-avatar-live-voice`)? [Coverage/Exception, Spec §US5-S2/§SC-012]
- [ ] CHK020 Alternate — Are requirements defined so a FAIL/INCONCLUSIVE result blocks only contract publication, not parallel sibling implementation? [Coverage/Alternate, Spec §Input/§FR-018]
- [ ] CHK021 Recovery — Are requirements defined for a terminal FAIL/INCONCLUSIVE being a valid, archivable experiment record (rerun-only path)? [Coverage/Recovery, Spec §SC-013/§FR-004]

## Edge Case Coverage

- [ ] CHK022 Is behavior specified when a variance's continuation status blocks affected sibling work behind a closed default? [Edge Case, Spec §FR-018]
- [ ] CHK023 Is behavior specified for the candidate unavailable / interrupted run so cleanup and non-qualification both hold? [Edge Case, Spec §FR-004/§FR-005]

## Dependencies & Assumptions

- [ ] CHK024 Is constitution alignment (fail-closed authority, redacted evidence, OpenSpec-before-implementation, single Speckit feature per change) documented and traceable? [Traceability, Plan §Constitution Check]
- [ ] CHK025 Is the assumption that the OpenSpec `tasks.md` (governance handoff) and the Speckit `tasks.md` (implementation) are not duplicated stated? [Assumption, Plan §Constitution Check]

## Ambiguities & Conflicts

- [ ] CHK026 Is there any residual conflict between "harness writes evidence under `openspec/changes/.../evidence/`" and the scope rule against modifying `openspec/` content that must be reconciled? [Conflict, Spec §FR-021/§Clarifications Q5]
