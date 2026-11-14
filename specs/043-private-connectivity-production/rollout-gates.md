# Production qualification gates Q0–Q5

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

These gates apply across the three delivery tracks and four offering paths. Labels describe existing capability decisions, not new wire-format request kinds. This document defines acceptance; it records no successful run or operating approval. The [implementation plan](plan.md) defines dependencies and the [validation matrix](validation-matrix.md) defines source versus observed proof.

## Gate register

| Gate | Entry and acceptance evidence | Required decision roles | Resulting authority | Current state |
| --- | --- | --- | --- | --- |
| Q0 — commission and scope | Ratified policy; accepted owner/code/CI/schema/verification scopes and one feature; intended platform and dependent domain/target decisions; release/support scope, custody, operating objectives and cost/capacity constraints; remaining decisions assigned to consuming gates | Rollout lead and each affected neutral/package/installer/product/operational/domain owner | Only the named implementation and preparation; target effects remain separately governed | Not accepted; required commissioning decisions absent |
| Q1 — staging entry | Q0; supported compatible immutable candidates; owner conformance and CI; actual approved provider/identity/entitlement/custody integrations; supported matrix and numeric region/cost/capacity/operating limits; scoped target execution; independent probes and protected evidence custody | Rollout lead, qualification/evidence custodians and affected owners/executor | Only the bounded staging run | Not entered |
| Q2 — staging exit | All four offering paths and supported matrix on the intended platform with real clients; two managed customer boundaries and environment separation; positive and denial controls; direct/relay, interruption, lifecycle, capacity, revocation, restore, upgrade, cutover/rollback and neighbor results within limits; reviewed incident closure | Qualification lead and affected package/installer/product/domain/operational owners | Exact candidate may be considered for a separate Q3 decision | Not entered |
| Q3 — production canary entry | Accepted Q2 candidate/evidence; separate named customer/site/network/domain/environment/region/resource/data/consent/spend/duration scope; current target-appropriate execution authority; working monitoring, support/on-call and rollback authority; approved fault scope/windows | Rollout lead, affected customers and component/domain/operational owners | Only that bounded canary; no general offer or expansion | Not entered |
| Q4 — production canary exit | Approved actually observed window and objectives; actual offered paths and isolation/application authorization; reviewed incidents and repairs; support readiness; cleanup/rollback readback and fresh affected-owner sign-offs | Rollout lead and fresh affected-owner acceptances | Accepted scope may be considered for a commercial offer or wave decision | Not entered |
| Q5 — commercial offer or expansion | Exact eligible service/profile/candidate pins and accepted Q4 evidence; named offer or wave with customer/region/resource bounds; applicable commercial decision and current owner approvals; impact/requalification disposition | Hosted-product/commercial authority, rollout lead and each affected domain/operational owner | Only the named offer/wave within bounds; later waves need decisions | Not entered |

## Dependency and scope rules

1. Ratified policy and historical lab acceptance do not pass Q0 or any live gate.
2. Q0 commissions exact work; Q1 authorizes staging; Q2 establishes qualification; Q3 separately authorizes a canary; Q4 accepts its evidence; Q5 separately admits an offer/wave.
3. All four paths must be covered at Q2: local factory/customer-operated Headscale, local factory/Hosted Headscale, standalone Hosted Headscale and hosted DomainxFactory. Private domain profiles cover managed-new and managed-existing; a domain without private access requirements additionally qualifies its own unbound path.
4. Managed service eligibility for the same approved phase/scope precedes managed attachment/private-domain activation. Track/site canary schedules may differ; this does not waive the governing staging requirements or an offering's own canary/release decisions.
5. A managed staging or production target needs an accepted client_infrastructure_request and managing-factory governed execution. Grant-required channels need valid scoped grants. Pull-only reconciliation uses a reviewed governed merge without an extra push credential. Unmanaged customer-operated targets instead need current customer authority and required consent.
6. Source tests, CI and lab fixtures qualify their own evidence class. They do not substitute for unobserved staging or production behavior. A denied probe without a successful legitimate control proves nothing about isolation.
7. Every numeric limit, support/candidate matrix, scope, consent and authority must be approved before the gate consuming it. Drafts, placeholders and expired decisions are not passes.
8. Every actual profile needs its own protection, required validation, current owner acceptance and exact-scope release evidence. A caller flag or another profile's canary cannot grant eligibility.

## Observation and failure rules

A gate record includes exact candidate/profile and customer/environment/target scope, current authority/policy, actual commands/probes, expected and observed outcomes, timestamps and event/clock anchors, monitoring coverage, incidents and accountable sign-offs. Evidence references are immutable and secret-free.

Missing or wrong-scope evidence fails acceptance. Monitoring outages do not count as healthy observation. Exceeded approved limits or an unreviewed incident block exit. No waiver can manufacture an observed success.

Boundary violations, public exposure of private endpoints, credential disclosure, unauthorized/duplicate effects, revived access, drift or missed limits halt affected enrollment and expansion. Contain/quarantine that scope, preserve current revocations and redacted evidence, and verify authorized neighbors remain available.

Resume requires reviewed remediation, affected-control and neighboring-isolation reruns and fresh scoped authority. A prior revoked/expired/no-longer-entitled binding stays unavailable during rollback. Fault/destructive drills never exceed separately approved targets, customer scope or windows.

## Change and expansion rules

Any material candidate, profile, provider, identity, region or policy change gets an impact review. Withhold affected eligibility until required Q2/Q4 requalification and renewed decisions exist. Successful evidence for one domain/profile does not qualify another.

Q5 names a commercial offer or an individual expansion wave; it is not a blanket fleet authorization. Customer cohort, profile, region, resources, spend and current release authority constrain admission. The next wave needs its own decision against current evidence.

Decision ownership and missing inputs are recorded in [commissioning](commissioning.md); offering-specific cases are in the [local](local-headscale.md), [standalone managed](standalone-hosted-headscale.md) and [hosted domain](hosted-domainxfactories.md) specifications. The [instance dependency contract](contracts/task-evidence.md#per-instance-q3q5-dependencies) permits only a genuinely passed same-scope child to advance independently of unrelated pending aggregates. All program Q2 coverage remains required; commercial offer admission precedes its first expansion wave, and aggregate completion requires all commissioned instances.
