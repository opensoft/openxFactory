# Research: Production qualification coordination

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

## Evidence basis

Read-only inspection used the ratified production packet, feature 040 source/evidence interfaces and preserved owner implementation worktrees. Some standalone primary checkouts are stale and omit the landed pilot files; no checkout was reset, fetched or moved to disguise that state. GitHub readback confirmed the relevant owner PRs are merged:

- [Headscale-Install #1](https://github.com/opensoft/Headscale-Install/pull/1).
- [xFactory-Installer #2](https://github.com/opensoft/xFactory-Installer/pull/2).
- [openXsoft-Hosted-Services #1](https://github.com/opensoft/openXsoft-Hosted-Services/pull/1).
- [opsXfactory #622](https://github.com/opensoft/opsXfactory/pull/622).
- [codeXfactory #578](https://github.com/codeXfactory/codeXfactory/pull/578).

These are historical source references, not feature 043 supported release pins or acceptance. C-01/C-05 reverify the selected owner revision, exact scope, release and content pins before implementation/integration and Q1. No owner tests, provider calls or lab drivers were run during research.

## R-01 — Reuse owned semantics, not a copied neutral runtime

**Decision**: Keep existing binding readiness, original-subject retries, current-authority checks and recovery ordering in their owners, with one coordinating feature.

**Rationale**: The neutral validator and feature 040 schema cover binding shape/readiness; Installer selection and managed-provider code retain cleanup/rollback identity; hosted operations retain durable state. These are useful inputs but do not constitute production qualification.

**Alternatives considered**: Duplicating runtimes into openXfactory would violate neutral ownership. Reopening completed 040 tasks would conflate lab acceptance and production scope.

## R-02 — Gate actual platform, domain and runtime scope choices

**Decision**: Resolve the coordination design now; require C-01 accepted runtime scope and C-02 provider/platform/domain choices before their dependent implementation.

**Rationale**: The ratified policy deliberately leaves those decisions to accountable owners. The current request commissions planning, not an Azure subscription, production domain, paid resource or target. Current customer/runtime support and installer distribution choices also require C-05.

**Alternatives considered**: Inheriting Eagle Docker, selecting Azure from unrelated history, choosing the lab domain, or inventing budgets/SLOs would manufacture authority. Blocking all independent local preparation on an unrelated provider choice would unnecessarily couple the offerings.

## R-03 — Retain durable operation invariants; qualify the selected persistence topology

**Decision**: Preserve the current SQLite-backed operation/installer semantics and one-writer locking as an implementation baseline. The owner may retain or replace storage only through accepted scope and demonstrated durability/fencing/recovery on the chosen platform.

**Rationale**: Hosted OperationStore persists operation IDs, input fingerprints, results, revocation tombstones and hashed single-use credential tracking. Hosted cancellation freezes original subjects, and installer/onboarding use scoped locks and conditional updates. Source fixtures do not prove deployed storage durability or HA. An old instance snapshot is never the source of current authority.

**Alternatives considered**: A mandatory new database adds unjustified scope. Treating process-local locking or a lab SQLite pass as production HA would omit platform-specific fencing and backup/revocation proof.

## R-04 — Qualify production package and installer adapters separately from the lab

**Decision**: Commission supported package/identity/renewal/state surfaces and a production local adapter/setup distribution in their owners. Preserve lab code and current lifecycle regressions.

**Rationale**: Headscale deploy/pilot.py and packaging/pilot-images.json fix synthetic boundaries, internal Docker networks, a local helper and short self-signed TLS. deploy/recovery.py supplies backup/quarantine configuration rehearsal rather than complete customer restore. Installer LocalPilotProvider fixes the lab endpoint and limited protocol/route behavior. Its managed adapter delegates to injected service and probes. The repository explicitly leaves the application framework/distribution undecided.

**Alternatives considered**: Renaming a lab helper or removing its guardrails is not qualification. Pulling the unrelated workstation-intake application or Store submission into this feature exceeds scope.

## R-05 — Supply actual hosted integrations and trusted-profile decisions

**Decision**: Preserve the hosted durable core while commissioning real provider, identity, entitlement, custody and actual-workload bindings. Production private requirements derive from the selected trusted exact profile, not a caller Boolean.

**Rationale**: Principal is a data object, entitlement is a local administrative table, and effects are injected. DockerPilot/DockerNodes are synthetic; PilotBinder loads the lab application. Onboarding currently accepts private_required as input. Actual production authentication, entitlement authority, custody and workload permission must replace those assumptions.

**Alternatives considered**: Trusting a caller-created principal, a Boolean privacy flag or a fixture entitlement source would let untrusted inputs choose authority.

## R-06 — Extend exact-profile release semantics through new owner governance

**Decision**: Establish owner-approved production profile/qualification schemas and semantic checks, exact definition-time protection, mandatory dependencies and fail-closed required validation before customer eligibility.

**Rationale**: Catalog eligibility currently restricts environment to test and checks exact profile bytes/revision, current interval and six evidence cases with a trusted owner callback. The historical domain schema fixes test/synthetic/customer_release false. Its narrow protection enrolls the one lab path, not a profiles directory prefix. Generic example validation warns successfully for unknown kinds and can skip schema checking when the dependency is absent; the existing required pilot suite closes only that specific pilot case.

**Alternatives considered**: Replacing test with prod, widening the lab schema, adding a caller eligibility flag or relying on generic warning-only validation does not establish production trust.

## R-07 — Publish supported neutral artifacts before production consumer pinning

**Decision**: Commission publication into the normal neutral contract bundle and qualify compatible package/service/profile consumer pins through the existing release process. Allocate no version here.

**Rationale**: The binding remains under specs/040-private-connectivity/contracts/private-connectivity, outside the published bundle. scripts/validate-private-connectivity.py still reads it there. Consumers currently vendor/pin pilot bytes.

**Alternatives considered**: Calling a feature-local schema supported, advancing pins before publication, hand-writing a release inventory or reserving a bundle number would bypass existing release gates.

## R-08 — Reuse managed-subject execution and current custody

**Decision**: Retain client_infrastructure_request, the managing factory's governed channel and existing approval/correlation/custody rules. A channel-required grant remains request-scoped; reviewed pull reconciliation needs no extra push credential. Unmanaged customer targets use their current authorized operator and consent.

**Rationale**: Ops has existing intake, state mapping, readiness profiles, deployment and broker contracts. Executor completion projects to validation_pending; trusted readiness and actual observations still establish acceptance. Existing AKS workload-grant code is a channel-specific implementation, not permission to select AKS here.

**Alternatives considered**: A new deployment-request kind, standing builder credential or blanket managing-factory requirement for unmanaged local operation would contradict the ratified boundary.

## R-09 — Commission explicit required CI and independent observed evidence

**Decision**: Bind each affected owner suite/production check to its required validation path, then separately collect live qualification. Do not infer private-connectivity coverage from generic green CI.

**Rationale**: Ops make test uses scripts/run_test_shards.py with top-level tests/test_*.py discovery; it does not collect tests/private_connectivity. Hosted/package make targets are fixture checks. Domain production profiles need their own strict required entry point and exact protection. All source/CI proof remains distinct from Q2/Q4 observations.

**Alternatives considered**: Treating a passing generic job as proof of an uncollected suite or treating fixtures as a live run would leave the requested acceptance unproved.

## R-10 — Commission a feature-specific evidence verifier and narrow shared registration

**Decision**: Plan a verifier/registration interface for 043 under separately accepted coordinator scope. Obtain owning authorization before changing shared pin classification, regression/census or required CI surfaces.

**Rationale**: The 040 verifier freezes T001–T021, cases, pilot run/pins and timing/sign-off assumptions. It validates records but never runs owner commands. Its shared pin registration covers only specs/040-private-connectivity/evidence/*.json, and tests explicitly reject applying it to another feature.

**Alternatives considered**: Reusing 040 registration, broadening a prefix silently, copying lab timing/role defaults or trusting self-reported pass strings would bypass provenance and live-evidence obligations.

## Research disposition

Coordination decisions are resolved and the [single task list](tasks.md) is generated for cross-artifact analysis. Execution inputs C-01–C-13 remain explicit owner decisions at their consuming gates, with no default or pass asserted. Provider/domain-specific implementation, live execution and release remain blocked until their decisions are accepted.
