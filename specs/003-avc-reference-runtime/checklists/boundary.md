# Boundary & Non-Deployability Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing the non-deployable package
boundary, stdlib-only core, provisional-import prohibition, and the static boundary gate — testing
requirement quality, not the scanner's behavior.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Security / governance reviewer

## Requirement Completeness

- [ ] CHK001 Are the forbidden deployment surfaces each enumerated (network listener, application factory, deployment manifest, persistent repository, provider-credential loading, live provider SDK)? [Completeness, Spec §FR-001]
- [ ] CHK002 Is the runtime package's designated path (`xfactory/avatar_runtime/`) and the test tree (`tests/avatar_runtime/`) explicitly specified as the only allowed locations? [Completeness, Spec §FR-001]
- [ ] CHK003 Is the stdlib-only requirement for the runtime package stated, with third-party/test/provider/network imports enumerated as forbidden? [Completeness, Spec §FR-001, §Clarifications Q3]
- [ ] CHK004 Is the provisional-adapter confinement (`tests/avatar_runtime/provisional/`) specified as a hard requirement? [Completeness, Spec §FR-004]
- [ ] CHK005 Is the requirement that package code depend on internal typed values (not copied canonical schemas) documented? [Completeness, Spec §FR-004]
- [ ] CHK006 Is the detection *method* (execution-free static AST/import/export/file-surface analysis) specified rather than left to implementer choice? [Completeness, Spec §FR-004a, §Clarifications Q4]
- [ ] CHK007 Is the standalone gate `scripts/validate-avatar-runtime.py` named as a required deliverable? [Completeness, Spec §FR-004a, §Clarifications Q4]
- [ ] CHK008 Are all detection targets of the gate enumerated (provisional imports, network/provider SDKs, listeners, app factories, persistence, credential loading, deployment files, forbidden entrypoints)? [Completeness, Spec §FR-004a]
- [ ] CHK009 Is the requirement that destroying the runtime needs no migration/cleanup/secret-grant recovery stated? [Completeness, Spec §FR-003, §SC-009]

## Requirement Clarity & Measurability

- [ ] CHK010 Is "non-deployable" defined by concrete absence criteria (no listener/entrypoint/key/persistence/SDK) rather than as a label? [Clarity, Spec §FR-001, §SC-010]
- [ ] CHK011 Is "reviewer can confirm the boundary from automated output alone" expressed as a measurable outcome (single gate output)? [Measurability, Spec §SC-010]
- [ ] CHK012 Is the stdlib-only criterion measurable as an import count (0 third-party/test/provider/network imports)? [Measurability, Spec §SC-005]
- [ ] CHK013 Is "no import path reaches the provisional adapter or any live provider SDK" quantified (count = 0 reachable paths)? [Measurability, Spec §SC-005]
- [ ] CHK014 Is "execution-free" clearly defined (static analysis, no importing/running runtime code)? [Clarity, Spec §FR-004a, contracts/ports.md]
- [ ] CHK015 Is the term "forbidden entrypoint" defined precisely enough to be detectable (e.g., `__main__`, console-script, ASGI/WSGI callable)? [Ambiguity, Gap]

## Requirement Consistency

- [ ] CHK016 Is the in-suite boundary test consistent with the standalone gate (same rules via a shared scanner) per the requirements? [Consistency, Spec §FR-004a, plan.md §Structure]
- [ ] CHK017 Does the stdlib-only-core requirement stay consistent with the tests/validator allowance to use pinned third-party libs? [Consistency, Spec §Clarifications Q3, §Dependencies]
- [ ] CHK018 Is the boundary requirement consistent with the "no sibling-owned path edits" ownership requirement (only the one gate script is the exception)? [Consistency, Spec §FR-036, §SC-008]
- [ ] CHK019 Are the deployment-surface prohibitions consistent with the Out-of-Scope declarations (no HTTP server, no provider key, no persistence, no UI)? [Consistency, Spec §Out of Scope]

## Scenario Coverage (Primary / Alternate / Exception / Recovery / Non-Functional)

- [ ] CHK020 [Primary] Are requirements defined for a clean scan of a compliant package (no surfaces found)? [Coverage, Spec §ARR-001-S01]
- [ ] CHK021 [Exception] Are requirements defined for reference code that attempts to load a provider key or make a network call (must fail + route to a live-runtime change)? [Coverage, Spec §FR-002, §ARR-001-S02]
- [ ] CHK022 [Exception] Are requirements defined for a package module importing the provisional path (import-boundary failure)? [Coverage, Spec §FR-004, §ARR-002-S02]
- [ ] CHK023 [Alternate] Are requirements defined for a runtime module importing a *permitted-in-tests-only* dependency (must still fail for the core)? [Coverage, Spec §Edge Cases "Runtime pulls a forbidden dependency"]
- [ ] CHK024 [Recovery] Are requirements defined for runtime destruction leaving no durable state to recover? [Recovery, Spec §FR-003, §ARR-001-S03]
- [ ] CHK025 [Non-Functional] Is the gate's role in the Principle V push gate specified (guards intermediate commits)? [Coverage, Spec §Clarifications Q8, §SC-008]
- [ ] CHK026 [Edge] Is behavior specified for transitive/indirect imports (a permitted module that itself pulls a forbidden dep)? [Edge Case, Gap]
- [ ] CHK027 [Edge] Is behavior specified for dynamic import constructs (importlib, `__import__`) that a static scan must still catch or flag? [Edge Case, Gap]

## Acceptance Criteria & Traceability

- [ ] CHK028 Do boundary success criteria (SC-005, SC-008, SC-010) each map to functional requirements? [Traceability, Spec §SC-005/008/010]
- [ ] CHK029 Are boundary requirements traceable to ARR-001/ARR-002 scenarios? [Traceability, Spec §US3, acceptance map]
- [ ] CHK030 Is the requirement that the gate be linked into the README validator index stated (documentation-index obligation)? [Traceability, Spec §Clarifications Q8, §FR-036]

## Dependencies & Assumptions

- [ ] CHK031 Is the assumption that the shared scanner is pure/stdlib (so the gate itself introduces no forbidden dependency in the runtime) documented? [Assumption, plan.md §Structure]
- [ ] CHK032 Is the dependency on the README validator-index location (single line) documented as the declared governance exception? [Dependency, Spec §FR-036, §SC-008]

## Ambiguities & Conflicts

- [ ] CHK033 Is there any conflict between "package exposes no application factory" and the requirement that `runtime.py` provides an in-process assembly? [Conflict, Spec §FR-001, plan.md — clarify "factory" ≠ deployable app factory]
- [ ] CHK034 Is it unambiguous which paths count as "sibling-owned" versus feature-owned for the boundary/ownership rule? [Ambiguity, Spec §FR-036, §Dependencies]

## Notes

- Every item interrogates whether the boundary *requirements* are well-specified — not whether the scanner passes.
