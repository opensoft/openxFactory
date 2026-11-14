# Production approval preparation register

Status: draft
Kind: review-packet
Prepared: 2026-11-14

This is a review index for the remaining owner and operating decisions. It does not replace the frozen task contract, authenticate unseen output or advance a gate. The sole implementation list is [043 tasks](../tasks.md); current acceptance remains T001–T009 and partial Q0-E. Brett accepted the five exact component source scopes and source-only custody on 2026-11-14; their task dependencies, consumed operating choices and freeze reconciliation remain required before implementation. PR #1310 remains draft.

## Prepared source decisions

| Owner | Reviewable scope | State |
| --- | --- | --- |
| E | [Accepted evidence commissioning](../../../openspec/changes/commission-private-connectivity-production-evidence/design.md) | Accepted at T006; T007–T009 source complete; actual bootstrap authentication and T010 pending |
| E amendment | [Exact source-only bootstrap records and T010 refinement](../../../openspec/changes/amend-private-connectivity-evidence-bootstrap/design.md) | Separate scope question pending; no new record/format or frozen-definition edit implemented |
| Neutral publication | [Exact neutral publication and release scope](../../../openspec/changes/publish-private-connectivity-production-contract/design.md) | Separate owner/scope question pending; no release version allocated |
| L | [Supported Headscale package](../../../openspec/changes/commission-headscale-production/design.md) | Brett Heap accepted as source/package/release owner and source-evidence custodian; exact scope ratified 2026-11-14; T011 remains pending |
| I | [Local and managed installer](../../../openspec/changes/commission-connectivity-installer-production/design.md) | Brett Heap accepted as installer source/release owner and source-evidence custodian; exact scope ratified 2026-11-14; T012 remains pending |
| H | [Standalone hosted service and hosted-factory product](../../../openspec/changes/commission-hosted-headscale-production/design.md) | Brett Heap accepted as hosted-product source/release owner and source-evidence custodian; exact scope ratified 2026-11-14; T013 remains pending |
| D | [Actual hosted MCP domain/profile](../../../openspec/changes/commission-hosted-domain-production/design.md) | Brett Heap accepted as domain/profile source/release owner and source-evidence custodian; coordinating and [owner-local PR #583](https://github.com/codeXfactory/codeXfactory/pull/583) source scopes ratified; T014 remains pending |
| O | [Current-authority execution, recovery and operations](../../../openspec/changes/commission-connectivity-operations-production/design.md) | Brett Heap accepted as Ops source/release owner and source-evidence custodian; coordinating and [owner-local PR #628](https://github.com/opensoft/opsXfactory/pull/628) source scopes ratified; T015 remains pending |

Source consent is recorded in each component packet's review/ratification.md before T010, but does not complete T011–T016 without their dependencies and actual authenticated outputs. Proposed task-file refinements must be reconciled into the reviewed freeze before use. Source approval does not create target credentials, paid resources, enrollment, customer eligibility or an automatic merge grant.

## Operating decisions still to consume

The [frozen decisions register](../commissioning.md), [task evidence contract](../contracts/task-evidence.md) and individual gate requirements remain authoritative.

| Decision | Preparation direction or actual gap | Acceptance boundary |
| --- | --- | --- |
| C-01 | Exact named E/L/I/H/D/O and neutral scopes above | Actual owner acceptance and required refreeze before source consumers; no approval inferred from drafting |
| C-02 | Inspect existing Azure QA in West US and production in Central US; real MCP workload and Linux Docker with Windows/macOS/Linux clients proposed | Exact provider/subscription/target/residency/domain/platform identities still require acceptance |
| C-03 | Existing Ops accepted-request/channel and request-scoped grant lifecycle | Each bounded preparation/staging/canary operation needs current target authority; source ratification is insufficient |
| C-04 | Reuse suitable Opensoft services; QA has an observed two-ready-replica Keycloak service at keycloak.opensoft.dev and a Ready letsencrypt-prod issuer | Exact realms/clients/audiences, entitlement and current-revocation sources, DNS/TLS/relay services and accountable owners remain unaccepted; public DNS nameservers do not establish Azure DNS authority |
| C-05 | Proposed supported released Headscale/package/client/service/workload/profile matrix | Exact immutable compatible content and distribution choices require owner review and actual release/readback; an upstream candidate is not qualified |
| C-06 | Availability/error, capacity/spend, revocation, backup/data-loss, recovery/rollback and observation objectives | Exact finite numeric bounds, units, event anchors, sampling, allowed gaps and minimum observed windows require owner approval before Q1; production objectives are confirmed at Q3 |
| C-07 | Existing QA capacity, two isolated synthetic customer boundaries, synthetic data and no new resource spend selected for preparation | No available dedicated persistent volume or qualified Mac target identified; numeric resources/objectives/faults/window/cleanup require a concrete approved envelope |
| C-08 | Source-only reviewed/redacted Git policy accepted for E; matching component source custody accepted 2026-11-14 | Protected live/customer/provider custody, retention, access, original output authentication and custodian decisions remain separate |
| C-09 | Internal Opensoft canary first | Exact offering/site/customer/candidate/targets, finite observation/rollback bounds and current authority must be accepted before each activation |
| C-10 | Q4 acceptance follows actual observation | Human acceptance of unseen results cannot be recorded now; gaps, incidents and affected-owner reviews remain mandatory |
| C-11 | Then one named customer per offering proposed | Actual named offer/customer, commercial terms, support and eligible scope need their own decision; no paid launch or eligibility inferred |
| C-12 | Gated expansion after admitted offers | Every wave requires exact bounds and authority; a canary or another offering supplies no inherited pass |
| C-13 | Failure-dependent containment and resumption | Preserve failed attempts, current revocations and neighbors; actual remediation/reruns and fresh affected authority before resume |

The operating rows are preparation status, not approved acceptance inputs. Actual result-dependent Q2/Q4 sign-offs and incident/resume decisions must remain later reviews. Missing storage, platforms, identity or custody does not permit weakening durability, substituting a lab result or skipping an offering/platform.

## Current infrastructure questions

The [operating service candidates](operating-service-candidates.md) record current Azure/OIDC candidates, the real MCP signing compatibility gap, identity-versus-authority constraints and remaining DNS/TLS/relay/custody choices. These are preparation inputs, not accepted operating decisions.

All 23 observed QA persistent volumes are Bound, and the inspected QA node resource group reports no unattached disk. No dedicated available service volume has been identified. Brett approved preparing a minimal dedicated-storage budget for review on 2026-11-14. The resulting financial envelope still requires its own acceptance; existing no-new-spend staging authority is unchanged. No provisioning or spend was authorized.

Brett approved investigating GitHub macOS runners within included capacity, with paid overages prohibited, on 2026-11-14. The investigation must establish exact runner/image/architecture, current allowance and an effective zero-overage stop before a bounded job can be proposed. No runner job, enrollment or live test is authorized by this preparation choice.

The [storage budget for review](staging-storage-budget.md) proposes a USD 10 storage-only ceiling for a bounded 14-day QA run with separately reserved retained capacity. The [Mac runner packet](macos-runner-options.md) proposes standard macos-15 arm64/Intel clients, finite job limits and an exact repository-scoped USD 0 actions_macos hard budget. Both proposals require their own decisions. The existing organization Actions guard allows positive paid spend and therefore cannot establish the selected zero-overage qualification constraint.

## Decisions supplied on 2026-11-14

Brett selected: "Prepare a minimal dedicated-storage budget for review (Recommended)"; "Investigate GitHub macOS runners within included capacity, with paid overages prohibited (Recommended)"; and "Approve all five roles and ratify the matching source scopes (Recommended)". The final answer accepts the five coordinating component packets, matching native Ops/domain packets, exact listed source refinements and private source-only custody. It does not accept the separate E bootstrap amendment or neutral publication scope, which remain pending. The 16-input task freeze is unchanged and T010 remains incomplete; approved refinements are reconciled before use.
