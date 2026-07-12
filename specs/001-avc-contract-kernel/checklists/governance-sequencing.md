# Governance, Ownership & Sequencing Checklist: AVC Contract Kernel

**Purpose**: Release-gate validation of requirements *quality* for ownership
boundaries (shared-contract-ownership, repo-boundary-governance), sibling/
successor sequencing, two completion states, and constitution alignment. Tests
whether the governance requirements are complete, unambiguous, consistent, and
free of scope conflicts.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Is openxFactory's canonical ownership of the AVC kernel stated as a requirement? [Completeness, Spec §FR-022/§FR-025; SCO-001]
- [x] CHK002 Are the reference/overlay ownership boundaries specified (contracts + non-deployable reference in openxFactory; client holds no keys/tool handlers/server config; overlays don't fork the protocol)? [Completeness, Spec §FR-025; SCO-002]
- [x] CHK003 Is the future private `xfactory-avatar-client` boundary specified (private, independently released, created by a successor change, forbidden contents)? [Completeness, Spec §FR-026; RBG-001]
- [x] CHK004 Are the internal-live client release-evidence obligations enumerated (pinned contract, fixture conformance, dependency lock, secret scan, client integrity, tests, rollback)? [Completeness, Spec §FR-027; RBG-002]
- [x] CHK005 Is the deferral of aggregation and web-console integration to separate changes specified? [Completeness, Spec §FR-028; RBG-003]
- [x] CHK006 Are the two completion states (implementation-complete-pending-F0 vs realized) fully defined, including that the OpenSpec change stays active until realized? [Completeness, Spec §FR-034 (Q7)]
- [x] CHK007 Is this change's exclusive write surface (`contracts/avatar-client/`, `scripts/validate-avatar-client.py`) and the shared-metadata-only-at-final-step rule specified? [Completeness, plan §Constraints; Spec §Assumptions]

## Requirement Clarity

- [x] CHK008 Is each sibling/successor's ownership stated unambiguously (F0, reference runtime, UI standard, client lab, live voice, pilot hardening)? [Clarity, Spec §Out of Scope; design.md Ownership table]
- [x] CHK009 Is "domain-neutral" clear enough that persona/retention instances are unambiguously excluded from this change? [Clarity, Spec §FR-001 (Q2)/§Out of Scope; Constitution §I]
- [x] CHK010 Is "the change is not realized/archived at the earlier milestone" stated without ambiguity? [Clarity, Spec §FR-034; research §D7]
- [x] CHK011 Are the "two task lists, not duplicated" roles (OpenSpec governance vs Speckit implementation) clearly delineated? [Clarity, plan Design Note 1; Constitution §II]

## Requirement Consistency

- [x] CHK012 Are the sibling ownership boundaries consistent between the spec Out-of-Scope, the design ownership table, and the parallel-workstream plan? [Consistency, Spec §Out of Scope; design.md; workstream plan]
- [x] CHK013 Is the memory-gateway-consent-is-not-media-authority rule stated consistently wherever consent appears? [Consistency, Spec §FR-005; ACR-008-S02; SCO-002]
- [x] CHK014 Do the completion-state requirements align with `target_release: implemented` (archive only on merged + green realization)? [Consistency, Spec §FR-034; Constitution §II; proposal front-matter]
- [x] CHK015 Are the shared-metadata write-overlap rules consistent between this change and the UI sibling's later serialized release? [Consistency, Spec §Assumptions; workstream plan]

## Acceptance Criteria Quality (Measurability)

- [x] CHK016 Are the boundary ratifications expressed as verifiable requirements (e.g., client contains no provider keys/server tool handlers)? [Measurability, Spec §FR-026; RBG-001-S01/S02]
- [x] CHK017 Is "does not modify any DomainxFactory repository / sibling files" objectively checkable for this change? [Measurability, Spec §Out of Scope; design.md Non-Goals]
- [x] CHK018 Is the realized-vs-pending completion state objectively determinable (tag + digests exist)? [Measurability, Spec §FR-034/§SC-010]

## Scenario & Edge-Case Coverage

- [x] CHK019 Are requirements defined for privileged provider code proposed in the client (rejected, routed to server boundary)? [Coverage, Spec US5-AS2; RBG-001-S02]
- [x] CHK020 Are requirements defined for an aggregation-pin or web-console proposal (must be a dedicated change)? [Coverage, Spec US5-AS3; RBG-003-S01/S02]
- [x] CHK021 Are requirements defined for a client/server contract-pin mismatch (preflight blocks live media, offers upgrade/fallback)? [Coverage, Exception, RBG-002-S03]
- [x] CHK022 Are requirements defined for a domain overlay attempting to fork neutral authority/vocabulary (rejected)? [Coverage, Spec §FR-025; SCO-002-S02]
- [x] CHK023 Is the fail-closed default for every deferred feature (push-to-talk, offline drafts, attachments, takeover, web-console, GPT-Live) covered? [Coverage, Gap, Spec §Out of Scope; design.md Risks]

## Dependencies & Assumptions

- [x] CHK024 Is the dependency on constitution v1.0.0 principles (I contract-neutral, II governed flow, VI releases, VII fail-closed) recorded in the Constitution Check? [Dependency, plan §Constitution Check]
- [x] CHK025 Is the assumption that the aggregation pin and successor repos are out of scope for this change documented? [Assumption, Spec §Out of Scope; plan Repository Constraints]
- [x] CHK026 Is the dependency on the frozen `avatar-client-parallel-v1` baseline and the variance protocol for cross-sibling coordination stated? [Dependency, Spec §Dependencies/§FR-030]

## Ambiguities & Conflicts

- [x] CHK027 Is there any residual ambiguity about which change may edit shared release metadata first (kernel vs UI sibling serialization)? [Ambiguity, Spec §Assumptions; workstream plan]
- [x] CHK028 Does any requirement risk duplicating the OpenSpec `tasks.md` governance list in the Speckit `tasks.md`? Is the non-duplication rule explicit? [Conflict, plan Design Note 1; Constitution §II]
- [x] CHK029 Is it unambiguous that authority claims here are backed by the ratified change (no `standard`-status claim without backing)? [Ambiguity, Constitution §III/§VII]
