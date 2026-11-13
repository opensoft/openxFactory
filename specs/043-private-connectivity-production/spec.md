# Feature Specification: Private connectivity production qualification

**Feature Branch**: 043-private-connectivity-production

**Created**: 2026-11-13

Status: draft

**Input**: Create the coordinating Speckit feature for qualify-private-connectivity-production, covering local Headscale, standalone Hosted Headscale, hosted DomainxFactories, owner scopes, Q0 commissioning and Q1–Q5 rollout gates.

**Governed by**: [Ratified proposal](../../openspec/changes/qualify-private-connectivity-production/proposal.md), [production qualification requirements](../../openspec/changes/qualify-private-connectivity-production/specs/private-connectivity-production-qualification/spec.md), [design](../../openspec/changes/qualify-private-connectivity-production/design.md) and [ratification record](../../openspec/changes/qualify-private-connectivity-production/review/ratification-2026-11-12.md), landed in [PR #1309](https://github.com/opensoft/openXfactory/pull/1309).

**Historical baseline**: [Completed feature 040](../040-private-connectivity/spec.md) and its [approved revised lab packet](../040-private-connectivity/evidence/G4-reviewed-repairs-approval.json). That lab acceptance remains historical; it grants no production permission.

**Coordination**: This is the single successor implementation feature. Its [implementation plan](plan.md) defines the dependency and verification design; [tasks.md](tasks.md) is the sole executable task list. These specification documents define outcomes and acceptance, not a second implementation list. [Owner scopes](owner-scopes.md), [commissioning decisions](commissioning.md), [rollout gates](rollout-gates.md), [validation matrix](validation-matrix.md) and [policy coverage](policy-coverage.md) are part of this specification.

## User Scenarios & Testing

### User Story 1 - Commission work with accountable owners (Priority: P1)

The rollout lead commissions bounded work from the installation, installer, hosted-product, operational, neutral-contract and domain owners. Each owner knows which decisions, changes and evidence they may produce.

**Why this priority**: Qualification cannot start safely when ownership, the intended platform or the scope of a change is assumed from the lab.

**Independent Test**: Review one proposed commissioning packet against the owner and decision registers. A complete scope can admit its named preparation; a missing owner, authority or required platform decision blocks dependent work.

**Acceptance Scenarios**:

1. **Given** a repository or governed surface outside an accepted owner scope, **When** implementation is proposed, **Then** the work waits for the owning governance decision.
2. **Given** the user has commissioned this feature specification, **When** someone requests runtime effects, **Then** the specification and policy ratification supply no runtime or target-execution grant.
3. **Given** the intended platform or provider is unselected, **When** provider-specific implementation is requested, **Then** that implementation waits for its platform decision.
4. **Given** complete current Q0 decisions, **When** the lead accepts commissioning, **Then** only the named implementation and preparation become authorized; live operations still need their applicable target authority.

### User Story 2 - Deliver supported customer-operated Headscale (Priority: P1)

A customer installs supported Headscale locally or connects an existing server and operates it without a hosted subscription. A local factory may also select a separately eligible hosted network.

**Why this priority**: Local operation is an independent delivery track and must remain usable without purchasing the hosted product.

**Independent Test**: Qualify install-new and connect-existing on the approved support matrix, with legitimate and denied access, certificate renewal, protected-state recovery and endpoint rollback. Use the [local track acceptance cases](local-headscale.md).

**Acceptance Scenarios**:

1. **Given** current customer authority and a supported endpoint, **When** install-new or connect-existing completes its checks, **Then** the local offering can become ready without hosted subscription credentials.
2. **Given** an invalid endpoint identity, enrollment or policy result, **When** setup fails, **Then** the installation remains unready and TLS verification is never bypassed.
3. **Given** a local target resolves as unmanaged, **When** all canary gates, consent and current customer-operator authority exist, **Then** its bounded canary needs no managing-factory request or grant.
4. **Given** an existing unbound installation, **When** the production feature is released, **Then** existing behavior continues until an operator opts in.

### User Story 3 - Operate Hosted Headscale independently (Priority: P1)

An openXsoft.com customer operates a managed network without a factory subscription and authorizes individual factories to attach or detach without coupling their lifetimes to the network.

**Why this priority**: The standalone service is a separately offered product and the foundation for managed attachments.

**Independent Test**: Use the actual intended platform and integrations for two approved managed customer boundaries, including provision, enrollment, retry, revocation, attachment removal and independent network termination. Use the [Hosted Headscale acceptance cases](standalone-hosted-headscale.md).

**Acceptance Scenarios**:

1. **Given** an entitled customer without a factory subscription, **When** the qualified service provisions a network, **Then** the customer can use its dedicated endpoint, state, keys and policy independently.
2. **Given** an approved factory cancellation, **When** cleanup completes or retries, **Then** only its original attachment is removed and independently entitled networks and other authorized devices remain usable.
3. **Given** a foreign customer or environment, **When** it attempts enrollment, administration, routing or traffic, **Then** access is denied while legitimate controls prove the service is available.
4. **Given** an interrupted operation and changed or expired authority, **When** it retries, **Then** current authority and original subjects are enforced without duplicated resources or revived access.

### User Story 4 - Qualify each actual hosted DomainxFactory (Priority: P1)

A domain owner offers its actual workload on openXsoft.com under an exact qualified profile. Private profiles support new or existing managed networks; profiles without private access requirements can qualify an unbound offering.

**Why this priority**: A successful network or lab profile cannot establish eligibility for a customer's actual domain application.

**Independent Test**: Qualify the selected actual workload and exact profile, its definition protections, application authorization, onboarding and cancellation. Use the [hosted domain acceptance cases](hosted-domainxfactories.md).

**Acceptance Scenarios**:

1. **Given** only the feature 040 synthetic profile or another domain's evidence, **When** catalog admission is attempted, **Then** the actual domain remains ineligible.
2. **Given** a private profile, **When** onboarding uses managed-new or managed-existing networking, **Then** approved network access and application authorization must both pass and private endpoints have no public ingress.
3. **Given** network access but missing application permission, **When** a client requests protected application access, **Then** the application denies it.
4. **Given** an owner-qualified profile with no private access requirement, **When** its release is admitted, **Then** no private-network subscription is forced.
5. **Given** partial onboarding failure, **When** the operation reports or retries, **Then** it remains unready, exposes no secrets or public private-service access, and creates no duplicate network.

### User Story 5 - Establish staging qualification on the intended platform (Priority: P1)

The qualification owners fix a supported candidate and approved limits, then observe the real offering paths and operational behavior in bounded staging.

**Why this priority**: Source tests and the Eagle lab do not establish actual production-provider behavior or a supported release.

**Independent Test**: First refuse Q1 with a missing required decision. Then, under approved staging authority, measure all four offering paths and the supported matrix against approved limits and evaluate Q2.

**Acceptance Scenarios**:

1. **Given** a missing approved target, owner, candidate pin, support matrix, limit or execution authority, **When** Q1 is evaluated, **Then** qualification does not start and no lab default fills the gap.
2. **Given** legitimate controls and independent probes, **When** all four offering paths and required lifecycle drills run, **Then** Q2 needs passing measurements, two managed customer boundaries, environment separation and reviewed closure of failures.
3. **Given** a broken service without a successful legitimate control, **When** a denied connection is observed, **Then** that observation does not count as isolation evidence.
4. **Given** candidate drift, an omitted path or an exceeded operating limit, **When** acceptance is requested, **Then** the affected qualification fails.

### User Story 6 - Contain failures and resume with fresh authority (Priority: P1)

Operations contains an affected scope, preserves authorized neighbors and current revocations, and resumes only after reviewed remediation and qualification reruns.

**Why this priority**: Recovery that revives access or expands an incident would invalidate the qualification model.

**Independent Test**: Within an approved fault scope, interrupt provisioning, restore older state and perform a failed cutover. Verify containment, current revocations, neighbor availability and the evidence/authority needed for resume.

**Acceptance Scenarios**:

1. **Given** a boundary violation, public private-endpoint exposure, credential disclosure, duplicate effect, revived access, drift or missed limit, **When** the condition is detected, **Then** affected enrollment and expansion halt and the affected scope is contained.
2. **Given** a revoked, expired or no-longer-entitled prior binding, **When** rollback is requested, **Then** that binding stays unavailable.
3. **Given** reviewed remediation and reruns of affected and neighboring controls, **When** current resume authority is accepted, **Then** only that authorized scope may resume.
4. **Given** a proposed destructive drill outside approved customer scope, **When** execution is considered, **Then** it does not run.

### User Story 7 - Admit a bounded canary and explicit expansion (Priority: P2)

The rollout lead and affected owners admit a bounded production canary, evaluate actual observed results, and decide each commercial offer or expansion wave separately.

**Why this priority**: Production customer exposure follows staging qualification and requires decisions that cannot be inherited from a merge, a lab sign-off or another profile.

**Independent Test**: Evaluate Q3–Q5 against immutable scoped evidence and current approvals. Reject staging-only permission, an incomplete observation window and a wave containing an unqualified profile.

**Acceptance Scenarios**:

1. **Given** accepted Q2 evidence without a separate Q3 decision, **When** customer activation is attempted, **Then** provisioning and enrollment remain blocked.
2. **Given** an approved canary, **When** monitoring misses an interval or incidents remain unresolved, **Then** the interval does not count toward acceptance and Q4 cannot pass.
3. **Given** accepted Q4 evidence for one domain, **When** an offer or wave is proposed, **Then** Q5 admits only its approved candidate, exact profiles, customers, regions and resource bounds.
4. **Given** a material artifact, profile, provider, identity, region or policy change, **When** existing eligibility is reused, **Then** affected eligibility waits for impact review, required requalification and renewed authority.

### Edge Cases

- A managed staging target requires the same executor boundary as a managed production target; environment tier changes governance depth, not the executor.
- A managed pull-reconciled deployment retains an accepted request and reviewed governed merge without inventing a push credential. A channel requiring a grant still needs a valid request-scoped grant.
- Restoring a backup cannot restore revoked authority; a single writable state has one fenced writer.
- Enrollment approval does not approve subnet routes, and a permitted network path does not approve an application action.
- A timeout, cancellation or changed retry input cannot change the original approved subject set.
- A managed attachment cannot activate before its managed service is eligible for the same approved phase and scope.
- A missing observation, stale pin or wrong-scope sign-off is a failed gate, even if source tests pass.
- A five-role lab approval is not a production owner acceptance or a service commitment.
- A new region, domain or profile cannot inherit an earlier scope's qualification.
- A failure in one customer boundary does not authorize deleting or disabling unrelated entitled networks.

## Requirements

### Functional Requirements

- **FR-001**: Preserve feature 040 as historical lab evidence and keep policy ratification, feature preparation, Q0 commissioning, Q1–Q2 staging, Q3–Q4 production canary and Q5 offer/wave decisions distinguishable. No earlier decision grants a later one.
- **FR-002**: Before runtime work, record accountable human owners, accepted repository identities, concrete approved code/CI/schema surfaces, governing authority, verification commands and the one coordinating implementation list. Work outside those scopes MUST wait for its owning decision.
- **FR-003**: Select the intended platform/provider before commissioning its dependent implementation. Record targets, staging topology, custody, support/release scope, cost/capacity bounds and operating objectives before their consuming gate.
- **FR-004**: Route execution by the existing managed-subject test. Managed targets require an accepted client_infrastructure_request and managing-factory execution through its governed channel; grants are valid, request-scoped and closed on completion where required. Governed pull reconciliation retains reviewed merge without an additional push credential. Unmanaged customer-operated targets require current customer-operator authority. Release builders acquire no standing deployment write credential.
- **FR-005**: Identify exact compatible released contracts, packages, server/client versions, services, provider/identity integrations, policies and domain profiles with immutable revisions and digests. Existing release processes govern publication and consumer pins; a feature 040 draft schema, mutable branch or tag alone is insufficient.
- **FR-006**: Compare observed artifacts, policy and profile scope to the approved candidate throughout qualification. Unapproved drift MUST fail affected acceptance.
- **FR-007**: Qualify local install-new and connect-existing without hosted subscription credentials, preserve opt-in and unbound behavior, and permit managed selection only against an eligible service and authorized attachment.
- **FR-008**: Local readiness MUST prove endpoint identity and renewal, reachability, supported compatibility, approved access and denied access. Failed endpoint, enrollment or policy checks leave the result unready without disabling identity verification.
- **FR-009**: Qualify isolated protected state, backup, upgrade, fenced restore, current-revocation reconciliation, retained network identity and approved cutover/rollback. Remove partial access and reauthorize any prior binding before restoration.
- **FR-010**: Hosted Headscale MUST use actual qualified production-provider, identity, entitlement and custody integrations. Each managed customer boundary has dedicated instance, endpoint, keys, durable state and policy; production and non-production are separate by default. A synthetic lab adapter cannot satisfy this requirement.
- **FR-011**: A standalone network MUST work without a factory subscription. Factory cancellation revokes only its original attachment; independent network termination needs separate scoped authority and preserves unrelated authorized devices.
- **FR-012**: Managed attachments MUST have current identity/entitlement, scoped approval and verified minimum access. Enrollment uses existing credential custody and short-lived single-use secret references. Routes need separate authorization; application permission remains independently enforced.
- **FR-013**: Interrupted provisioning, enrollment, detachment and cleanup retries MUST converge on their original immutable subjects and recheck current authority before effects and activation. Changed inputs, expired/replayed credentials or revoked authority cannot widen scope, duplicate resources or revive access.
- **FR-014**: Each actual hosted domain workload and exact profile MUST qualify its customer scope, application authorization and lifecycle. Private profiles prove managed-new, managed-existing and no public ingress; profiles without private access requirements qualify an unbound path without a forced network subscription. Partial failures remain unready.
- **FR-015**: Production profiles MUST have owner-approved strict schema and semantic validation, exact definition-time protection and required validation wiring. Eligibility derives from current exact-profile evidence and release authority; unknown fields, caller flags, wrong domains/environments and stale or substituted evidence cannot grant eligibility.
- **FR-016**: Q1 MUST require commissioned scope, supported immutable candidates, actual approved integrations, target-appropriate execution authority, independent probes, protected evidence custody, supported matrix and approved region/cost/capacity/numeric limits before starting the run.
- **FR-017**: Q2 MUST prove all four offering paths on the intended platform with real clients, positive and denial controls, two isolated managed customer boundaries and environment separation. Required observations include direct/relay paths, interruption, upgrade, revocation, restore, endpoint cutover/rollback and authorized-neighbor availability.
- **FR-018**: Approve numeric availability/error, capacity/spend, revocation, backup age/data loss, restore, rollback, sampling, monitoring-gap and observation criteria before acceptance. Measure outcomes with event/clock anchors and monitoring coverage. Lab measurements do not silently become production commitments.
- **FR-019**: Q3 MUST require accepted Q2 evidence and a separate bounded decision naming candidate, customers, sites, networks, domains, environments, regions, resources, spend, duration, data use, consent, operators, monitoring, support and rollback authority. Execution authority follows FR-004; staging approval or this feature alone cannot activate a canary.
- **FR-020**: Q4 MUST require the approved actually observed window, measured objectives, offered-path and isolation outcomes, reviewed incident closure, support readiness, cleanup/rollback readback and fresh affected-owner sign-offs. Missing monitoring intervals do not count; fault or destructive drills execute only within separately approved targets and windows.
- **FR-021**: Q5 MUST authorize each named commercial offer or expansion wave separately against accepted canary evidence, exact eligible profiles/candidate pins, customer/region/resource bounds, current owner approvals and the applicable commercial release decision.
- **FR-022**: Material candidate, profile, provider, identity integration, region or policy changes MUST withhold affected eligibility pending reviewed impact assessment, required staging/canary reruns and renewed release authority. Another domain or profile cannot inherit acceptance.
- **FR-023**: Boundary violations, public private-endpoint exposure, credential disclosure, unauthorized/duplicate effects, revived access, drift or missed limits MUST halt affected enrollment and expansion, contain/quarantine affected scope, preserve redacted evidence and current revocations, and preserve unrelated authorized service.
- **FR-024**: Resume MUST require reviewed remediation, reruns of affected controls and neighboring isolation, and fresh scoped authority. Rollback MUST NOT restore a revoked, expired or no-longer-entitled binding.
- **FR-025**: Every gate decision MUST reference immutable secret-free evidence of exact candidate/profile, customer/environment/target scope, actual commands/probes, expected and observed outcomes, timestamps/event anchors, current authority/policy, incidents and accountable sign-offs. Missing, stale, substituted or wrong-scope evidence fails the gate; a waiver cannot manufacture an observation.
- **FR-026**: Record the actual state of commissioning and gate decisions. Draft, pending, absent, expired or failed decisions MUST NOT be represented as passed or active. Q0–Q5 are capability labels, not new deployment request kinds or an independent authority mechanism.
- **FR-027**: Preserve independent track/site schedules while enforcing dependencies: managed service eligibility precedes managed attachment/private-domain activation; each local or unbound offering retains its own qualification and release decisions without a forced hosted entitlement.
- **FR-028**: Keep broad fleet migration, pricing, service commitments, new repository creation/admission and blanket domain launch outside this feature's specification authority. Owning proposals and concrete realization decisions remain necessary where required.
- **FR-029**: Keep exactly one coordinating Speckit feature and one executable tasks.md. Owner governance, implementation PRs, release evidence and gate dependencies MUST be represented there once; acceptance documents do not duplicate implementation lists.
- **FR-030**: Do not reuse the feature 040 synthetic provider, draft schema, synthetic domain or five-role lab approvals as supported production artifacts, production-domain selection, current owner commissioning or live acceptance.

### Key Entities

- **Owner scope**: Accountable human role, owning repository, accepted change surfaces, governance authority, verification responsibility and excluded effects.
- **Commissioning decision**: A current accepted decision specifying which preparation or implementation is allowed and which later values remain prerequisites.
- **Release candidate**: Compatible supported artifacts and exact profile revisions/digests, support matrix and declared operating scope.
- **Execution authority**: The accepted managing-factory request/channel/grant, or current customer authority for an unmanaged target, separate from release eligibility.
- **Qualification run**: Actual target, candidate, scope, probe/command references, time/clock anchors, expected and observed outcomes and incidents.
- **Gate decision**: A scoped Q0–Q5 decision with prerequisites, evidence, accountable approvals, validity and disposition.
- **Offering path**: Local factory/customer Headscale, local factory/Hosted Headscale, standalone Hosted Headscale, or hosted DomainxFactory with its private or qualified unbound profile.
- **Release eligibility and wave**: Exact customer-eligible profile/candidate and a separately bounded commercial offer or expansion cohort.
- **Containment and resume decision**: Affected subjects, preserved neighbors/current revocations, reviewed repair evidence, reruns and renewed scope.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 18 governing requirements and 39 governing scenarios are traceable to feature requirements and planned acceptance cases in policy-coverage.md; none relies solely on the lab packet.
- **SC-002**: Before each runtime edit or operational effect, every owner affected by that scope has a current named scope/authority and verification record; zero actions occur outside those records. The program Q0 join requires all six owner classes before staging preparation/Q1. An unrelated owner's pending decision does not block an independently commissioned source scope.
- **SC-003**: Q2 passes all four offering paths and the approved support matrix, with two managed customer boundaries and successful legitimate controls; all attempted out-of-scope enrollment, administration, routes, traffic and application access are denied.
- **SC-004**: Every required operating limit is numeric and approved before its consuming gate; all accepted observations meet those approved limits with recorded event/clock anchors and coverage.
- **SC-005**: Applicable install, provisioning, retry, revocation, detachment, upgrade, renewal, restore and endpoint cutover/rollback cases pass for all three tracks, preserving current revocations and authorized neighbors.
- **SC-006**: Every passed Q0–Q5 decision has complete current prerequisites, immutable correct-scope evidence and accountable approvals; no missing interval or source/lab substitute counts as live observation.
- **SC-007**: Every admitted offer or wave matches its exact qualified profiles, candidate and approved cohort bounds; every material change receives its required impact review and requalification before admission.
- **SC-008**: All approved failure drills demonstrate bounded halt/containment, no revived or duplicate access, preserved authorized neighbors, and resume only after reviewed remediation, reruns and fresh authority.

## Assumptions

- Brett Heap's current requests authorize this coordinating specification, implementation plan, tasks and cross-artifact analysis/remediation. They do not select a production platform/domain, approve runtime code scopes, create paid resources or grant target execution.
- The ratified production policy and existing neutral, package, installer, product, domain and managing-factory boundaries govern subsequent planning. Historical feature 040 ownership is context, not new production authority.
- Concrete owner surfaces, verification commands and accountable human acceptances are commissioning outputs due before implementation, not defaults supplied by this draft.
- Provider/platform, supported production matrix, identity/entitlement/custody choices, actual domain, targets, budgets, numeric limits and canary/wave bounds are required gate decisions. Their due gates and current missing state are explicit in commissioning.md; their values are not invented here.
- Publication of supported neutral contracts and owner artifacts follows existing release processes; no version is reserved and no consumer pin is advanced by this specification.
- Local customer operation, standalone service use and qualified unbound domains remain independent offerings. Track/site canaries may have different schedules within their separate authority and dependencies.
- Source/local validation, CI, staging observations, production canary acceptance and commercial/wave release remain distinct evidence and decisions.
