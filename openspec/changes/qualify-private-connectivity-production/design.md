# Design: Private connectivity production qualification

Status: draft

## Context

See [proposal](proposal.md) for scope and the
[qualification requirements](specs/private-connectivity-production-qualification/spec.md)
for behavior. This policy adds a production acceptance path while retaining the
ratified product boundaries and the completed 040 lab record.

The landed source cohort is Headscale-Install #1, xFactory-Installer #2,
codeXfactory #578, openXsoft-Hosted-Services #1, OpsxFactory #622 and openXfactory
#1303. The [merge record](../../../specs/040-private-connectivity/merge-preparation.md)
describes source equivalence; the PRs record the later landings and CI outcomes.
The accepted [G4 decision](../../../specs/040-private-connectivity/evidence/G4-reviewed-repairs-approval.json)
remains acceptance of the synthetic Eagle lab.

Production gaps have identifiable owners:

- Headscale-Install's [local pilot runbook](https://github.com/opensoft/Headscale-Install/blob/11bd61fe665cf40f2bbf02980c512475329b3151/docs/runbooks/local-pilot.md)
  describes unpublished Docker fixtures and two-day self-signed certificates.
- The hosted [candidate boundary](https://github.com/opensoft/openXsoft-Hosted-Services/blob/3876812fb06f3352b62eb663c3e1cea15c41b2fe/README.md)
  restricts its provider adapter to synthetic Eagle tenants. Its durable operation
  core is useful source, but that adapter does not realize production provisioning.
- The domain [pilot profile](https://github.com/codeXfactory/codeXfactory/blob/c3a2d0e23bbe62659df94e3e422e4eb77e62680f/profiles/hosted/private-connectivity.yaml)
  is a synthetic test profile with customer release disabled.
- The shared binding is an approved pilot candidate. Supported contract publication,
  owner releases and consumer pins require their existing release processes.

## Goals / Non-Goals

**Goals**

Provide one reviewable qualification chain with exact candidate evidence, owner
acceptance, controlled customer exposure and bounded expansion. Make local and
standalone use independently operable, preserve per-domain eligibility and route
managed changes through the owning execution authority.

**Non-goals**

This packet does not implement a provider, publish a package, choose a commercial
price or service promise, allocate infrastructure, migrate customers, issue a
credential or admit a catalog profile. It does not complete the unrelated
workstation-intake client or configure Sonar baselines. Existing G4 evidence and
T001–T021 remain historical inputs.

## Decisions

### 1. Add a production qualification profile and a new implementation handoff

The production capability supplements private-connectivity rather than changing
what the accepted lab run proved. Its realization gets one new coordinating
Speckit feature; the creation hook allocates the next available number at handoff.
Do not rename 040, reopen its completed checklist, or relabel G4 as production.

The new feature records owner scopes and verification entry points first. Owner
implementation decisions reference the existing repository boundaries and follow
their owning OpenSpec process when a new governed surface is needed. An OpenSpec
handoff records those decisions; executable implementation tasks live only in the
new Speckit feature. Reusing 040's checklist would mix accepted observations with
new platform, release and customer authority, obscuring which evidence was valid.

### 2. Qualify an immutable release set with explicit compatibility

Identify each required released artifact by version, immutable source and content
digest, together with the supported server/client/platform matrix, provider,
identity/entitlement integration and policy/profile revisions. Mutable labels
can describe channels but cannot identify the qualified bytes.

The neutral publisher uses its atomic versioning/release inventory process before
a supported consumer adopts the contract. Install and product owners publish their
own independently supported artifacts and verify the resulting pins. A qualified
Git commit is not automatically a published package or a supported contract release.

This avoids coupling independently released products to a single source branch.
Component qualification can proceed in parallel. The shared staging exit proves
their compatible composition across all four offering paths.

### 3. Keep platform effects and credentials in their existing owners

Production provider integration belongs in openXsoft-Hosted-Services. Packaging
and supported instance/state operations belong in Headscale-Install, installation
selection/distribution in xFactory-Installer, and domain workloads and access
declarations with each DomainxFactory.

The existing [deployment-handoff boundary](../../specs/deployment-handoff-boundary/spec.md)
determines who executes by whether the target is a registered managed subject.
Staging is not an exemption. Its accepted client_infrastructure_request names the
released artifact and digests; the managing factory governs the configuration
channel, scoped deployment grant, correlation evidence and grant closure.
An unmanaged customer-operated target remains under its customer's authorized
operator. No new deployment-request record kind or standing builder write
credential is introduced.

An intended platform is selected before commissioning its concrete implementation.
Keeping this policy provider-neutral preserves the established ownership boundary;
it does not allow a lab adapter to satisfy a production provider's conformance.

### 4. Use six explicit gates

Gate identifiers below are this capability's labels, not new wire-format kinds.
Every pass and approval is immutable, scoped and linked to its prerequisites.

| Gate | Required outcome | Effect of acceptance |
| --- | --- | --- |
| Q0 commission and scope | Ratified policy; commissioned owners and concrete work surfaces; named intended platform, staging targets, release/support scope, custody, operating objectives and cost/capacity bounds. | Allows only the specifically commissioned implementation and preparation. Live operation still needs its applicable target request. |
| Q1 staging entry | Supported compatible candidate set, owner conformance/CI passes, required identity/provider/entitlement integrations, accepted staging execution authority, independent probes and evidence custody. | Allows the bounded staging run. |
| Q2 staging exit | Four offering paths and supported matrix pass on the intended platform; two managed customer boundaries and environment separation; lifecycle, failure, capacity and recovery observations meet approved limits; incidents are closed and reviewed. | Makes the exact candidate eligible for a separate canary decision. |
| Q3 production canary entry | Q2 plus explicit customer/site/domain/region/resource/data scope, consent, spend and duration bounds, monitors, support and rollback roles; accepted managing-factory execution requests and live grants where required. | Allows only that canary, within its approved limits. It grants no general sale or expansion. |
| Q4 production canary exit | Offered paths meet operating objectives throughout the approved observed window; isolation and app authorization remain effective; incident, operational and cleanup evidence pass; affected owners sign off. | Makes the accepted scope eligible for a commercial-release or expansion decision. |
| Q5 commercial release and expansion | Named service offer or wave, exact eligible profiles and candidate pins, customer/region/scale bounds, applicable commercial release decision, Q4 evidence and owner approval. | Admits only the named offer and wave. Later waves require their own decisions. |

Q0 can identify later operating decisions as prerequisites, but an absent value
blocks the gate that consumes it. A draft decision, placeholder, expired request
or an assertion that a value will be chosen later is not an entry pass.

Canary schedules can differ between tracks and sites. Customer-operated local
service needs no hosted entitlement. A local managed attachment or private hosted
domain cannot activate before its managed service is eligible. An unbound hosted
profile still needs its own domain release evidence and does not acquire a
private-network subscription requirement.

### 5. Preserve independent network and application authority

A managed boundary has dedicated Headscale state, endpoint, keys and policy;
production and non-production are separate by default. Sharing among a customer's
installations requires an explicit installation/access scope. Route approval is
separate from enrollment and application permission remains necessary after the
network allows a connection.

Identity and entitlement decisions are checked before effects and again before
activation or a sensitive retry. Stable operation identity and immutable original
subjects prevent interrupted provisioning or cancellation from changing scope.
Short-lived, single-use enrollment credentials resolve through declared custody.
Bindings, logs, telemetry and support artifacts carry references, never secret values.

A standalone network can outlive a factory attachment. Cancellation/detachment
revokes only the authorized original attachment subjects; terminating a managed
network is a separately authorized lifecycle action.

### 6. Measure the intended operating model

Staging uses supported release artifacts, the intended platform and actual service
integrations. Synthetic accounts/data can be used there with approved custody;
replacing a provider with an Eagle fixture cannot qualify provider behavior.

Use independent positive controls before counting denied probes. Exercise direct
and forced-relay paths, including loss of control-plane access while an existing
data path persists. Measure actual revocation, backup age/data loss, upgrade,
restore, endpoint migration and rollback with event anchors and bounded sampling.

Protected recovery fences the old writer and quarantines the replacement.
Retain authoritative current revocations outside the restored instance snapshot.
Recheck entitlement and policy before activation. If SQLite remains the supported
store, retain one writer to each writable state; any alternative availability
design requires its own support and recovery qualification.

For the live canary, choose a minimum observed window and explicit capacity/error
and alert thresholds before entry. A probe outage does not count as observed
healthy time. Destructive drills have their own approved targets/windows; reuse
staging evidence honestly when a production drill is not authorized, and do not
claim the unobserved production result.

### 7. Admit catalog entries by exact domain and release scope

The committed synthetic profile and pending inventory remain historical candidates.
The selected domain owner qualifies a production profile for its actual workload,
application authorization, minimum sources/destinations/ports, deployment,
onboarding and retirement. New-network, existing-network and applicable unbound
choices are tested explicitly.

Before a production profile qualifies, its owner establishes strict schema and
semantic validation, exact definition-time protection and required CI wiring
under the owning governance. The pilot's protected definition does not enroll a
new production path automatically. Eligibility is computed from current approved
release evidence, never from a caller-supplied eligible flag.

Catalog evidence names the domain/profile revision and the allowed offer, region,
customer scope and release decision. An unrelated profile cannot inherit another
domain's acceptance. A change to the profile, provider, identity integration,
region, artifact or material policy receives impact review and renewed qualification
of affected controls and adjacent boundary probes. The owner decides whether a new
bounded canary is required; no affected scope resumes without renewed authority.

A passing canary is evidence for review, not an automatic catalog state change.

### 8. Contain first, then qualify recovery and resumption

A failed isolation, credential, authorization, idempotency, revocation, readiness,
drift or timing control freezes affected enrollment and expansion. The managing
operator contains the affected scope, preserves redacted observations and current
authority, and retains independently authorized neighbors.

Rollback removes partial target grants, fences competing writers, and verifies
the prior binding is still authorized before restoring it. Expired, revoked or
unentitled access stays unavailable. Resume requires reviewed remediation, passing
affected and neighboring boundary controls, and explicit current resume authority.
A waiver can document a disposition but cannot count an unobserved or failed test
as a passing safety control.

## Required realization decisions

These are compulsory inputs to the gates, not production defaults supplied by the
lab or approval to proceed while values are missing.

| Decision | Recorded by | Due before |
| --- | --- | --- |
| Concrete repository/code/CI/schema surfaces, owner acceptance and the single Speckit feature | Coordinator and component owners | Implementation commissioning at Q0 |
| Platform/provider, managed subjects, staging topology, production regions and residency constraints | Hosted product and managing factory | Target/provider implementation and Q1; production scope at Q3 |
| Identity, customer/operator roles, entitlement source, credential/backup custody, DNS/TLS renewal and relay ownership | Product, install and Ops owners | Q1 |
| Contract and artifact releases, provenance/digests, supported server/client/platform matrix and update compatibility | Publisher, install, installer, product and domain owners | Q1 |
| Numeric availability/error, capacity/spend, revocation, restore, backup age/data-loss, rollback and probe limits | Rollout lead and accountable service/Ops owners | Q1 for staging; confirmed production objectives at Q3 |
| Canary customers/sites/domains, consent/data scope, count/region/resource limits, observed window, fault scopes and rollback/support coverage | Rollout lead, customers and affected owners | Q3 |
| Commercial offer, expansion cohorts, region/scale bounds and exact catalog profiles | Product, rollout lead and each affected domain owner | Q5 |

The five lab-role approvals do not sign these decisions. A person can hold multiple
production roles, but the decision identifies every role and its scope explicitly.

## Risks / Trade-offs

- A second release environment costs time and resources: authorize bounded
  staging/canary spend and lifecycle cleanup before creating resources.
- Endpoint/relay behavior varies by site and client: qualify the declared matrix
  and retain failed cases instead of generalizing from one Docker network.
- Fleet availability and instance consistency pull in different directions:
  qualify the chosen failover model while retaining fenced, authorized state.
- A shared service can accidentally couple subscriptions and network lifetimes:
  retain original cancellation subjects and independently test surviving devices.
- Historical source or lab success can be mistaken for current deployment evidence:
  bind each result to the actual candidate, execution plane and current authority.
- Material change invalidation can slow expansion: use scoped impact analysis,
  rerun affected controls and adjacent isolation, and record the new decision.

## Migration Plan

Preserve the completed lab packet. After policy ratification and owner commissioning,
the new Speckit feature produces supported owner releases and verifies their pins.
Deploy only within accepted staging execution scopes, complete Q1–Q2, then request
Q3 for a bounded canary. Record Q4 before seeking a named commercial offer or Q5 wave.
Existing installations remain opt-in and unbound behavior stays available.

Release artifacts, deployment acceptance, service/catalog eligibility and commercial
availability are distinct transitions. Promotion and rollback records correlate to
their existing managing-factory requests. Archive only after the governing policy's
realization and handoff satisfy the shared workflow; an archive never supplies
missing release or operational approval.
