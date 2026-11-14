# Validation matrix: Sources, releases and rollout gates

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

Every row is a planned proof obligation, not an executed test or accepted gate. Owner source commands below were discovered from the landed lab implementation; they do not qualify an actual provider or customer release.

## Requirement and gate coverage

| ID | Required proof | Feature requirements | Cases / gates |
| --- | --- | --- | --- |
| V-01 | Current accepted human owner/path/command scopes and consumed platform/domain decisions; reject absent/expired authority and lab substitutions | FR-001–FR-004, FR-026, FR-028–FR-030 | US1; C-01–C-02; Q0 |
| V-02 | Supported compatible neutral/package/service/profile release, content pins, final consumer/harness matrix and observed-drift rejection after all integrations | FR-005–FR-006, FR-030 | C-05; T049 before preparation/Q1; Q1–Q5 |
| V-03 | Local new/existing/unbound, valid/invalid identity, renewal, access denial, state/upgrade/fenced recovery, cutover/rollback/current revocations and managed selection | FR-007–FR-009, FR-012–FR-013, FR-024, FR-027 | L-01–L-06; Q2 and applicable Q4 |
| V-04 | Actual provider/identity/entitlement/custody, two dedicated managed boundaries, standalone use, original-subject retry/restart, independent cancellation/termination | FR-010–FR-013, FR-018, FR-027 | H-01–H-06; Q2 and Q4 |
| V-05 | Actual exact workload/profile, strict semantic/schema/protection/required validation, trusted privacy, application permission, private new/existing and qualified unbound paths | FR-014–FR-015, FR-021–FR-022, FR-027 | D-01–D-06; Q1–Q5 |
| V-06 | Supported candidate/integrations/CI, target authority, numeric bounds/matrix, probes/custody before bounded staging | FR-002–FR-005, FR-016, FR-018, FR-025–FR-026 | C-03–C-08; Q1 |
| V-07 | All four paths with real clients, two managed boundaries/environment separation, legitimate controls plus denials, direct/relay and applicable disconnected-peer checks, lifecycle/drills/neighbor availability | FR-017–FR-018, FR-025, FR-027 | All L/H/D cases; Q2 |
| V-08 | Separate bounded canary/consent/support/rollback/monitoring decision and current target authority; managed missing-request/grant and unmanaged missing-customer-authority refusals; pull reconciliation without extra push credential | FR-001, FR-004, FR-019, FR-025–FR-026 | L-05; C-09; Q3 |
| V-09 | Actual approved window/objectives, measured maxima/gaps/coverage, incident closure, offered paths/isolation/application permission, cleanup/readback and fresh owner acceptance | FR-018, FR-020, FR-025–FR-026 | H-06; C-10; Q4 |
| V-10 | Named commercial offer or individual wave, exact current eligible candidates/profiles and bounded cohort; changed/foreign profile or region requalification | FR-021–FR-022, FR-025–FR-028 | D-06; C-11–C-12; Q5 |
| V-11 | Detect/halt/contain affected scope, current revocations, no duplicate/revived access, preserved neighbors, scoped reviewed remediation/reruns and fresh resume | FR-009, FR-013, FR-023–FR-024 | L-03–L-04, H-06; C-13; Q2/Q4/resume |
| V-12 | Frozen case registry, authenticated bootstrap imports, command/revision/output equality, immutable scoped child/aggregate dependency checks, correct evidence class, secret safety and protected custody; reject fixtures as live proof | FR-025–FR-026, FR-029–FR-030 | C-08; every gate |
| V-13 | Explicit required owner CI entry points, dependency availability and fail-closed validation; prove affected suite was collected | FR-002, FR-015–FR-017, FR-029 | Q0 scope and Q1 source-readiness; not a live pass |

[Policy coverage](policy-coverage.md) maps all 18 governing requirements and 39 scenarios to the FR and L/H/D cases above. The [single task list](tasks.md) maps all 30 feature requirements to implementation/acceptance tasks, and its [evidence registry](contracts/task-evidence.md) freezes task/owner/dependency/case identities. Approved commands and actual expected outcomes remain necessary; counts alone do not establish coverage or a pass.

## Existing source validation commands

Each command is relative to its owning repository and requires its declared bench/dependencies. These commands were inspected, not run against owners during planning.

| Owner | Existing command / source | What a pass establishes |
| --- | --- | --- |
| openXfactory | python3 scripts/validate-private-connectivity.py; python3 -m pytest tests/private_connectivity -q | Historical feature-local binding conformance; no published production artifact or live observation |
| Headscale-Install | make validate; make test | Documents/links, fixture qualification and whitespace under Makefile/.github/workflows/qualification.yml |
| xFactory-Installer | make validate; make test | Repository validation and unit tests under Makefile/.github/workflows/validate.yml; required schema dependency must be installed from owner requirements |
| openXsoft-Hosted-Services | make validate; make test | Fixture service/operation/onboarding/catalog tests under .github/workflows/qualification.yml; no actual provider/identity or customer-domain acceptance |
| opsXfactory | python3 scripts/client_infrastructure_execution.py; python3 scripts/evidence_correlation_audit.py self-check; python3 -m pytest tests/private_connectivity -q | Deterministic intake/correlation and private-connectivity fixture tests; source proof only |
| Historical codeXfactory lab profile | python3 scripts/validate-examples.py; python3 -m pytest tests/private_connectivity -q; python3 -m pytest tests/merge-master/test_hosted_profile_floor.py -q; bash scripts/validate-docs.sh | Historical profile/schema/protection and required doc validation with exact neutral pin/dependencies; no new production profile enrollment |

Ops generic make test is not evidence that its nested private-connectivity suite ran: its shard discovery inspects only top-level test modules. Commission the required explicit invocation/collection proof in the accepted Ops scope. New production domain kinds cannot rely on the generic example validator's warning/skip behavior; schema dependencies and exact validation entry points must fail closed.

## Required source, CI and release validation

Source/fixture suites retain regressions for current scope, retry identity, cancellation subjects, locks/fencing, application permission and exact-profile authority. Add commissioned production-adapter and negative semantic cases, including:

- A caller-supplied unbound/privacy or eligibility flag cannot downgrade a trusted private profile or release an unqualified one.
- Missing dependency, unknown profile kind/field, missing exact protection or omitted required suite cannot pass by warning or skip.
- Changed retry input, expiry/replay, restart, stale conditional update and independently authorized network lifetime preserve original subjects.
- Concurrent/old writers, stale restored revocations, failed target cleanup and revoked prior bindings cannot reactivate access.
- Evidence from a different candidate/run/profile/customer/environment or a missing positive control cannot satisfy acceptance.

Run required CI on the exact owner candidate and verify the actual collected suites. Publish through each owner's approved release path and verify provenance/content pins separately. No required check, skip count, measured witness, floor, hash or release inventory changes merely to obtain green status.

## Required observed validation

Only accepted Q1 authority permits the bounded intended-platform staging run. Collect all four offering paths with actual integrations/clients and independent positive and denial controls. Include direct/relay and applicable disconnected-client revocation, upgrade, state protection, backup age/data loss, restore/quarantine/fencing/current revocations, cutover/rollback, neighbor availability and measured capacity/availability/error behavior.

Q3 requires fresh customer/target scope and consent. Q4 repeats applicable offered-path/isolation/operational proof through the approved actual observation window, with missing monitoring time excluded, no unreviewed incident and fresh affected-owner acceptance. Destructive drills require their own approved targets/windows.

Q5 checks current exact eligibility and the bounded commercial offer/wave. A material change invalidates affected evidence until impact review, required reruns and renewed authority. Every failed/blocked attempt remains available to the reviewer with remediation and clean rerun/resume links.

## Current disposition

Local planning validation is separate from the source commands and observed cases above. Q0 is not accepted and Q1–Q5 have not run. No owner source test, required CI, release publication, target execution or live result is claimed by this matrix.

T005 freezes this matrix for owner review together with the task/owner/case/dependency registry in the [review freeze](contracts/task-evidence.md#t005-review-freeze). The [evidence scope](../../openspec/changes/commission-private-connectivity-production-evidence/proposal.md) is now ratified at T006 with the source-only custody policy; the [neutral publication scope](../../openspec/changes/publish-private-connectivity-production-contract/proposal.md) remains draft and T016 is unaccepted. This pass stops before T007. A document freeze supplies no owner or live-gate authority by itself.
