# Governance-Gates & Ownership Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing OpenSpec→Speckit handoff,
constitution gates, artifact discipline, content-addressed release pinning, ownership boundaries,
and parallel/realization sequencing — testing requirement quality, not process execution.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Governance reviewer / release approver

## Governed Change Flow & Handoff

- [ ] CHK001 Is the single-OpenSpec-change → single-Speckit-feature handoff reflected (this feature derives from `implement-avatar-reference-runtime`)? [Traceability, Spec §Input, constitution §II]
- [ ] CHK002 Is the requirement that OpenSpec and Speckit task lists are not duplicated reflected? [Consistency, Spec §Assumptions "Task-list separation", constitution §II]
- [ ] CHK003 Is the `code_surface`/`target_release` semantics (archive only on merged, green realization evidence) acknowledged in the requirements? [Completeness, constitution §II, Spec §FR-005]
- [ ] CHK004 Are the deferred sibling changes (live-voice qualification, Hermes hardening) documented as out of scope with owners? [Completeness, Spec §Out of Scope, research.md]

## Validation Gates (Principle V)

- [ ] CHK005 Is the requirement that the standalone validator + deterministic suite form the feature's push gate specified? [Completeness, Spec §Clarifications Q8, constitution §V]
- [ ] CHK006 Is "run for every feature commit and before push" specified as the gate cadence? [Clarity, Spec §Clarifications Q8]
- [ ] CHK007 Is behavior proven by deterministic reviewable evidence (tests/fixtures/validator output) rather than assertion, per the requirements? [Consistency, constitution §V, Spec §SC-003]
- [ ] CHK008 Is the requirement that OpenSpec artifacts pass strict validation acknowledged as a precondition? [Completeness, constitution §V]

## Artifact & Schema Discipline (Principle IV)

- [ ] CHK009 Is the `schema_version` + `kind` requirement stated for `scenario-test-map.yaml` and `realization-pin.yaml`? [Completeness, Spec §Clarifications Q6/Q7, contracts/conformance-artifacts.md]
- [ ] CHK010 Is the requirement that the new validator be linked into the README validator index stated? [Completeness, Spec §Clarifications Q8, constitution §IV]
- [ ] CHK011 Is the prohibition on host-absolute paths in committed files reflected (repo-relative references only)? [Consistency, constitution §IV]
- [ ] CHK012 Is the prohibition on storing raw credentials reflected in the telemetry/redaction requirements? [Consistency, Spec §FR-033, constitution §IV/VII]

## Content-Addressed Release Pinning (Principle VI)

- [ ] CHK013 Is the five-coordinate release identity (per-file `contract_schema_version`, bundle version, tag, exact commit + digests, changelog) reconciled with the runtime's five-coordinate pin? [Consistency, Spec §FR-005, constitution §VI]
- [ ] CHK014 Is "consumers pin the exact commit and digests — a movable branch/tag is not a pin" reflected in the realization requirement? [Clarity, Spec §FR-005, §ARR-002-S03, constitution §VI]
- [ ] CHK015 Is the requirement that this feature allocates no contract version (consumes only) stated? [Completeness, plan.md §Constitution Check, constitution §VI]

## Ownership & Boundary Discipline

- [ ] CHK016 Are the feature-owned paths (`xfactory/avatar_runtime/`, `tests/avatar_runtime/`) explicitly bounded? [Completeness, Spec §FR-036, §SC-008]
- [ ] CHK017 Is the single governance exception (`scripts/validate-avatar-runtime.py` + one README index line) declared and bounded? [Clarity, Spec §FR-036, §SC-008]
- [ ] CHK018 Is the prohibition on editing canonical contracts / F0 / UI / DomainxFactory / deployment / release-metadata paths specified? [Completeness, Spec §FR-036, §Dependencies]
- [ ] CHK019 Is "sibling-owned files consumed read-only" specified for the acceptance maps and kernel? [Consistency, Spec §Dependencies, §FR-034a]
- [ ] CHK020 Is the shared-tree / worktree discipline (explicit-path staging, current-branch check) reflected as a working constraint? [Completeness, constitution §Repository Constraints]

## Parallel Work vs Ordered Realization Sequencing

- [ ] CHK021 Is the separation between parallel implementation and ordered realization specified (cannot realize until kernel has a published commit + digests)? [Completeness, Spec §US2, design D10]
- [ ] CHK022 Is the accepted-variance rule (name affected acceptance IDs; reopen only mapped tests/adapters) specified? [Completeness, Spec §FR-006, §ARR-002-S04]
- [ ] CHK023 Is the requirement that the provisional adapter be disabled for final conformance specified? [Completeness, Spec §FR-035, §Clarifications Q5]
- [ ] CHK024 Is serialization of final integration for parallel features touching shared release metadata acknowledged? [Consistency, constitution §Workflow]

## Scenario Coverage & Analyze Gate

- [ ] CHK025 [Exception] Are requirements defined for a diff that touches a sibling-owned path (realization fails)? [Coverage, Spec §FR-036, §ARR-008-S04]
- [ ] CHK026 [Non-Functional] Is the precondition that `/speckit.analyze` reports no critical findings before implementation reflected? [Coverage, constitution §Workflow]
- [ ] CHK027 [Edge] Is behavior specified for the aggregation-repo submodule pin update (commit here first, then sync) if/when relevant? [Edge Case, constitution §Repository Constraints, likely out of scope — confirm]

## Traceability, Ambiguities & Conflicts

- [ ] CHK028 Do governance requirements trace to the constitution principles they enforce (II, IV, V, VI, VII)? [Traceability, constitution]
- [ ] CHK029 Is it unambiguous that adding the README validator-index line is a *required* documentation-index update, not a scope violation? [Ambiguity, Spec §FR-036, constitution §IV]
- [ ] CHK030 Is there any conflict between "modifies 0 sibling files" (SC-008) and "README index entry" — and is the exception explicitly reconciled? [Conflict, Spec §SC-008, §FR-036]

## Notes

- Items test whether the governance/ownership *requirements* are complete, consistent with the constitution, and unambiguous — not whether the process was followed.
