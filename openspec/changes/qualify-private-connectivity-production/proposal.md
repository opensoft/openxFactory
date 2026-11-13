---
code_surface: none (Production qualification and release policy only; owner-scoped realization and deployment requests remain separate.)
target_release: implemented (Policy promotion after ratification; customer releases retain their own release and operating authority.)
sequenced_after: [add-private-connectivity, implement-private-connectivity-binding, establish-headscale-install-ownership, establish-openxsoft-hosted-connectivity, register-private-connectivity-evidence-pins]
---

# Proposal: Qualify private connectivity for production

Status: ratified
Ratified: 2026-11-12 by Brett Heap. [Ratification record](review/ratification-2026-11-12.md)
Kind: proposal
Proposed: 2026-11-12

## Why

Feature 040's accepted Eagle lab demonstrates the connectivity and recovery model,
and its six implementation PRs have landed. Customer delivery still needs supported
artifacts, a production provider integration, qualification on the intended platform,
and explicit decisions for a bounded production canary and each expansion wave.

The [G4 acceptance](../../../specs/040-private-connectivity/evidence/G4-reviewed-repairs-approval.json)
accepts synthetic lab evidence and grants no production, commercial-release or
expansion authority. Preserve that record and the completed T001–T021 history.

## What Changes

- Establish one production qualification policy for customer-operated local
  Headscale, standalone Hosted Headscale on openXsoft.com, and hosted
  DomainxFactories, including local factories that select the hosted service.
- Require a released, compatible candidate set: neutral binding contract,
  Headscale/server and supported clients, installation package, hosted services,
  provider and identity integrations, policies and exact domain profiles.
  A release cut follows the existing contract versioning policy; this packet
  allocates no version and advances no consumer pin.
- Require staging on the intended hosting platform and service integrations.
  Requalify all four offering paths, including positive controls, cross-tenant
  and environment denial, direct/relay paths, lifecycle operations, capacity,
  revocation, restore, upgrades, endpoint cutover and rollback.
- Require a separately authorized production canary with named customers,
  installations, domains, environments, regions, limits, observation windows,
  operators and rollback authority. Staging approval does not admit customer traffic.
- Require strict production profile validation, exact definition-time protection
  and mandatory validation wiring before a profile can become customer eligible.
- Admit expansion only through a bounded wave decision tied to accepted canary
  evidence and exact qualified profiles. Changes invalidate affected evidence;
  failed controls halt the affected rollout until reviewed remediation and reruns.
- Preserve customer-operated choices without a hosted entitlement, independent
  Hosted Headscale subscription and attachment lifetimes, application authorization,
  deny-by-default policy, and separately approved routes.
- Apply the existing managed-subject deployment boundary to staging and production.
  A managed target crosses as an accepted client_infrastructure_request executed
  by its managing factory; producing repositories do not acquire standing
  deployment credentials or a new deployment-request record kind.
- Hand governance to one new coordinating Speckit feature. Its first planning
  record establishes owner-scoped realization authority and the operational
  decisions required at each gate; it contains the sole executable task list.

## Capabilities

### New Capabilities

- private-connectivity-production-qualification: supported release candidates,
  the three delivery tracks, staging qualification, production canary acceptance,
  per-profile expansion and withdrawal of release eligibility.

### Modified Capabilities

None. This supplements the ratified private-connectivity requirements without
rewriting the accepted pilot, changing binding semantics, or amending the existing
deployment-handoff-boundary and repo-boundary-governance capabilities.

## Impact

| Owner | Proposed realization and release responsibility |
| --- | --- |
| opensoft/openXfactory | Neutral qualification policy, coordination and any separately authorized contract publication through the existing release process. No hosted product runtime. |
| opensoft/Headscale-Install | Supported package, HTTPS identity/renewal, isolated instance and state lifecycle, backup, upgrade and quarantined recovery. |
| opensoft/xFactory-Installer | Production setup integration and supported distribution for install-new, connect-existing, managed selection and unbound compatibility. This does not commission the unrelated workstation-intake application or Store submission. |
| opensoft/openXsoft-Hosted-Services | Production provider adapter, identity/entitlement integration, durable managed operations, factory onboarding, service catalog and exact-profile eligibility. |
| opensoft/opsXfactory and the target's managing factory | Managed-subject deployment handoff, credential custody, operational acceptance, monitoring, emergency containment, recovery and rollback. |
| Each DomainxFactory owner | Actual hosted workload, minimum-access declaration, application authorization, lifecycle evidence and approval for its exact profile revision. codeXfactory is the current lab profile, not an approved production-domain selection. |

These are ownership boundaries and proposed work areas, not new path grants.
Before implementation, the coordinating feature records approved repository
identities, concrete code/CI/schema surfaces and verification commands; newly
governed owner changes follow their owning OpenSpec process. Repository creation,
aggregation admission, broad fleet migration, pricing and a blanket domain launch
are outside this packet.

Brett Heap commissioned this draft. Ratification, implementation commissioning,
staging operation, production canary, commercial offer and expansion decisions
remain distinguishable approvals. No infrastructure, paid resource, customer
enrollment, catalog eligibility, service commitment or credential is changed by
creating or ratifying this policy packet. See [design](design.md), the
[requirements](specs/private-connectivity-production-qualification/spec.md)
and the [Speckit handoff](tasks.md).
