# Private connectivity production qualification

Status: ratified
Ratified: 2026-11-12 by Brett Heap. [Ratification record](../../review/ratification-2026-11-12.md)

## Purpose

Define the evidence and authority required to offer local Headscale, independent
Hosted Headscale and hosted DomainxFactories to customers, progressing through
staging, a bounded production canary and explicitly approved expansion.

## ADDED Requirements

### Requirement: Production decisions are separate from lab acceptance

The rollout SHALL preserve feature 040 lab observations and approvals as historical
lab evidence. Proposal ratification, implementation commissioning, staging entry,
production canary, commercial availability and expansion SHALL have distinguishable
decisions. No earlier decision SHALL imply a later decision.

#### Scenario: A source merge is offered as production permission
- **WHEN** a release request cites the accepted G4 packet, merged PRs or passing CI without the applicable production decision
- **THEN** customer enrollment and production activation SHALL remain unauthorized

#### Scenario: A policy is ratified
- **WHEN** this production qualification policy is ratified
- **THEN** its requirements SHALL become governing policy without provisioning a resource or granting a staging, canary, commercial or expansion permission

### Requirement: Owner commissioning precedes realization

The coordinating feature SHALL identify accountable owners, approved repository
and code surfaces, verification commands and the single Speckit implementation
list before runtime work. A release SHALL retain the established neutral,
installation, product, domain and operational ownership boundaries.

#### Scenario: A proposed runtime surface lacks owner authority
- **WHEN** implementation would edit a repository, schema, workflow or runtime surface absent from the recorded owner scope
- **THEN** that work SHALL wait for the owning governance decision rather than inheriting authority from this policy packet

### Requirement: Deployment follows the managed-subject boundary

Staging and production deployments SHALL use the existing managed-subject test.
A managed target SHALL require an accepted client_infrastructure_request and
execution by its managing factory through the governed channel. A channel that
requires a deployment grant SHALL use a valid request-scoped grant, revoked on
completion. Pull-only reconciliation SHALL retain the accepted-request and
reviewed-merge boundary without requiring a push credential. An unmanaged
customer-operated target SHALL require its customer's current authorized operator.
Release builders SHALL hold no standing deployment write credentials.

#### Scenario: Staging is a registered managed target
- **WHEN** a candidate is ready to deploy to a registered staging subject
- **THEN** deployment SHALL require the same managing-factory handoff boundary as production, with the applicable staging approval depth

#### Scenario: A managed production canary lacks an accepted request
- **WHEN** a canary release decision exists for a registered managed target but no accepted deployment request exists
- **THEN** the deployment SHALL remain blocked

#### Scenario: A managed production canary lacks a required execution grant
- **WHEN** a managed canary has an accepted request but its execution channel requires a deployment grant and no valid request-scoped grant exists
- **THEN** the deployment SHALL remain blocked

#### Scenario: A managed canary uses governed pull reconciliation
- **WHEN** a managed canary has an accepted deployment request and the approved change is a reviewed merge into the managing factory's governed configuration tree, applied by its pull-only reconciler
- **THEN** that channel SHALL NOT require an additional push credential, and all other canary entry conditions SHALL remain required

### Requirement: Release candidates identify supported immutable artifacts

Each release candidate SHALL identify exact compatible contract, package, server,
client, service, provider adapter, policy and domain profile revisions and digests.
Published neutral contracts SHALL follow their existing release policy. A
feature-local draft schema, mutable branch name or container tag alone SHALL NOT
constitute a supported production release.

#### Scenario: A consumer uses the pilot schema directly
- **WHEN** a customer release candidate names only the feature 040 draft binding schema
- **THEN** release eligibility SHALL require the supported contract publication and verified consumer pins before acceptance

#### Scenario: Running configuration differs from the candidate
- **WHEN** an operator observes an unapproved artifact, policy or profile revision during qualification
- **THEN** the affected gate SHALL fail and its observations SHALL NOT qualify the declared candidate

### Requirement: Local Headscale supports customer operation

A local production offering SHALL qualify install-new and connect-existing without
a hosted subscription, preserve unbound installations, and offer managed selection
only against an eligible hosted service. It SHALL verify operator authority,
supported platform/client compatibility, approved access and denied access before
readiness.

#### Scenario: A customer selects its own Headscale
- **WHEN** an authorized customer installs a supported new instance or supplies an existing endpoint
- **THEN** setup SHALL complete without openXsoft.com subscription credentials and SHALL keep failed endpoint, enrollment or policy attempts unready

#### Scenario: A local factory selects Hosted Headscale
- **WHEN** the customer selects a managed network
- **THEN** setup SHALL require the network entitlement and scoped attachment approval, reconcile retries and preserve unrelated existing bindings

### Requirement: Local packages qualify HTTPS and state lifecycle

The supported package SHALL qualify endpoint identity, certificate renewal,
reachability, isolated protected state, backup, upgrade and fenced recovery.
Customer operation SHALL retain policy, route, credential and recovery authority.
Lab-only certificates and fixture adapters SHALL NOT qualify customer delivery.

#### Scenario: A certificate renews or an endpoint changes
- **WHEN** the supported installation renews its HTTPS identity or performs an approved endpoint cutover
- **THEN** clients SHALL verify the resulting identity without disabling TLS checks and failed cutover SHALL remove partial access before restoring a still-authorized prior binding

#### Scenario: An instance restores older state
- **WHEN** a supported instance restores a protected backup or rolls back an upgrade
- **THEN** recovery SHALL reconcile current revocations before activation, preserve network identity and prevent concurrent writers to the same writable state

### Requirement: Hosted Headscale uses qualified production integrations

Hosted Headscale SHALL qualify its actual provider, identity, entitlement and
credential-custody integrations on the intended platform. Each customer trust
boundary SHALL have its dedicated instance, endpoint, keys, durable state and
policy. Production and non-production SHALL be separate by default.

#### Scenario: The only adapter is the Eagle lab adapter
- **WHEN** a candidate offers the synthetic Docker provisioning adapter as its production provider
- **THEN** the hosted release gate SHALL reject the candidate

#### Scenario: A customer or environment crosses a boundary
- **WHEN** enrollment, administration, routes or traffic exceed the approved customer and environment scope
- **THEN** the service SHALL deny the action and leave other boundaries unaffected

### Requirement: Hosted network and factory lifetimes remain independent

A standalone managed network SHALL be usable without a factory subscription.
Provisioning and cleanup retries SHALL converge on the original approved subject
set and recheck current authority. Factory removal SHALL revoke only its attachment;
network service termination SHALL require its own scoped customer authority.

#### Scenario: A factory subscription ends
- **WHEN** an authorized cancellation or detachment completes or retries after interruption
- **THEN** the service SHALL remove the original factory access within its approved limit and preserve independently entitled networks and unrelated authorized devices

#### Scenario: A stale operation retries after authority changes
- **WHEN** a retry presents changed input, expired or replayed credentials, or revoked entitlement
- **THEN** the service SHALL reject unauthorized effects without duplicating resources or reviving prior access

### Requirement: Hosted domains qualify their actual profile

Each hosted DomainxFactory SHALL qualify its actual workload and exact profile
revision for deployment, customer scope, application authorization and lifecycle.
Private profiles SHALL prove managed-new and managed-existing onboarding and no
public ingress. A profile without a private access requirement SHALL qualify
its unbound path without forcing a network subscription.

#### Scenario: A synthetic profile is proposed for customer release
- **WHEN** catalog admission cites only the feature 040 synthetic workload or another domain's evidence
- **THEN** the domain SHALL remain ineligible until its actual workload and exact profile qualify and its owner approves release

#### Scenario: Network access succeeds without application permission
- **WHEN** a connected client lacks the domain application's required authorization
- **THEN** the application SHALL deny access despite the permitted network path

#### Scenario: Hosted onboarding fails after partial provisioning
- **WHEN** policy, enrollment, application or connectivity verification fails
- **THEN** onboarding SHALL report the failed step without secrets, retain an unready result and reconcile retries without public exposure or duplicate networks

### Requirement: Production profiles are protected and validated

Production profile definitions SHALL have owner-approved strict schema and semantic
validation, exact definition-time protection and required validation wiring.
Catalog eligibility SHALL derive from current release authority and evidence for
that exact domain/profile. Caller-declared eligibility or another profile's
qualification SHALL NOT authorize release.

#### Scenario: A new profile escapes required validation
- **WHEN** a proposed production profile lacks its approved schema, exact definition-time protection or required validation entry point
- **THEN** it SHALL remain ineligible and its owner SHALL establish the governed checks before release qualification

#### Scenario: Catalog evidence has the wrong scope
- **WHEN** admission presents unknown profile fields, stale evidence, a mismatched domain or an environment outside the accepted scope
- **THEN** validation or catalog admission SHALL reject the candidate without changing customer eligibility

### Requirement: Staging entry fixes the qualification scope

Staging entry SHALL require commissioned owner scope, supported candidate
artifacts, the approved platform and service integrations, scoped execution
authority, independent probes and protected evidence custody. Named regions,
cost/capacity bounds, supported platforms and numeric operating limits SHALL be
recorded before the run.

#### Scenario: A required decision is absent
- **WHEN** entry lacks an approved target, owner, limit, support matrix, execution authority or candidate pin
- **THEN** staging qualification SHALL not start and no lab default or placeholder SHALL supply the missing decision

### Requirement: Staging exit proves the offering paths and operations

Staging exit SHALL prove all four offering paths with real clients on the intended
platform and integrations, independent positive and denial controls, two isolated
managed customer boundaries and environment separation. It SHALL include
interrupted operations, direct/relay paths, upgrades, revocation, restore,
cutover/rollback and neighbor availability.

#### Scenario: Denial is observed against a broken service
- **WHEN** a negative probe lacks a successful control from its legitimate boundary
- **THEN** it SHALL NOT count as evidence of isolation

#### Scenario: Staging lacks a required path or drill
- **WHEN** a candidate omits standalone use, local operation, a local factory using Hosted Headscale, hosted-domain onboarding, or an applicable operational drill
- **THEN** the affected release SHALL remain unqualified and the staging exit SHALL not pass

### Requirement: Production operating objectives are approved and measured

Owners SHALL approve numeric availability, capacity, revocation, backup age/data
loss, restore, rollback, probe sampling and observation criteria before accepting
qualification. Evidence SHALL record measured outcomes, clock/event anchors and
monitoring coverage. Lab measurements SHALL NOT silently become service
commitments.

#### Scenario: A recovery exceeds the approved limit
- **WHEN** a measured restore, revocation, rollback or observation gap exceeds its approved limit
- **THEN** the drill SHALL fail and a source or fixture pass SHALL NOT replace the missing operational result

#### Scenario: Monitoring misses part of the observation window
- **WHEN** the canary's required independent probes or alerts are unavailable
- **THEN** the missing interval SHALL not count toward the required acceptance window

### Requirement: Production canary entry requires bounded release authority

Canary entry SHALL require accepted staging evidence and a separate decision
naming candidate artifacts, customers, sites, networks, domains, environments,
regions, capacity, spend, duration, data use, operators and rollback authority.
Required customer consent and working monitoring SHALL exist before activation.
Active execution authority SHALL follow the managed-subject boundary: an accepted
request and execution through the managing factory's governed channel for a
managed target, with valid request-scoped grants where that channel requires them;
or the customer's current authorized operator for an unmanaged customer-operated
target.

#### Scenario: A customer-operated local canary is an unmanaged target
- **WHEN** local Headscale resolves to an unmanaged customer-operated target and has accepted staging evidence, a bounded canary decision, required customer consent, current customer-operator authority and working monitoring
- **THEN** that canary MAY activate within its approved scope without a managing-factory deployment request or grant

#### Scenario: An unmanaged local canary lacks customer authority
- **WHEN** an unmanaged customer-operated local canary lacks required customer consent or current customer-operator authority
- **THEN** activation SHALL remain blocked despite a canary release decision

#### Scenario: A canary exceeds its approved scope
- **WHEN** onboarding would add an unlisted customer, site, domain, region or exceed the approved node/resource bound
- **THEN** that onboarding SHALL be denied until a new scoped decision and applicable qualification exist

#### Scenario: Staging approval is reused as canary permission
- **WHEN** an operator has staging acceptance without the separate canary decision
- **THEN** production provisioning and customer enrollment SHALL remain blocked

### Requirement: Canary exit requires production evidence and owner acceptance

Canary exit SHALL require the approved observation window, measured operating
objectives, actual offered-path and isolation results, reviewed incident closure,
support readiness, cleanup/rollback readback and fresh affected-owner sign-offs.
Faults and destructive drills SHALL be confined to their separately approved
targets and windows.

#### Scenario: An incident remains unresolved
- **WHEN** a canary retains a failed control, unexplained alert, missing observation or unreviewed remediation
- **THEN** canary acceptance and expansion SHALL remain blocked

#### Scenario: A fault drill lacks customer scope
- **WHEN** a proposed destructive drill would affect a live customer outside the approved drill scope
- **THEN** it SHALL not execute, and staging evidence SHALL not be relabeled as a production drill result

### Requirement: Expansion is a separate per-wave decision

Each expansion wave SHALL identify its candidate, customer and region bounds,
capacity, exact domain profiles, accepted canary evidence and accountable owners.
Commercial offer eligibility SHALL require its own release decision. A domain,
region, provider or material policy/identity change SHALL trigger impact review
and requalification of affected controls before admission.

#### Scenario: One domain's canary succeeds
- **WHEN** a domain passes its approved canary
- **THEN** other domains SHALL remain ineligible until their exact profiles and release decisions qualify, and the accepted domain SHALL expand only within an approved wave

#### Scenario: A candidate changes after acceptance
- **WHEN** an artifact, profile, provider, identity integration, region or material policy differs from the accepted release scope
- **THEN** affected eligibility SHALL be withheld until reviewed impact assessment, required staging/canary reruns and renewed release authority are recorded

### Requirement: A failed control halts and contains the affected rollout

Boundary violations, public exposure of private endpoints, credential disclosure,
unauthorized or duplicate effects, revived access, candidate drift or missed
operating limits SHALL halt affected enrollment and expansion. Operators SHALL
contain or quarantine the affected scope, preserve redacted evidence and current
revocations, and obtain reviewed remediation, reruns and resume authority.

#### Scenario: Rollback encounters an unauthorized prior binding
- **WHEN** containment or rollback finds that the previous binding is expired, revoked or no longer entitled
- **THEN** it SHALL remain unavailable rather than being reactivated to restore availability

#### Scenario: One tenant fails qualification
- **WHEN** a tenant requires containment
- **THEN** operators SHALL preserve unrelated authorized networks and bindings, and SHALL verify affected controls and neighboring isolation after remediation before resuming

### Requirement: Acceptance evidence is immutable and scoped

Every gate decision SHALL identify the exact release/profile and environment,
actual commands or probes, expected and observed outcomes, evidence timestamps,
current policy, incidents and accountable sign-offs. References SHALL be immutable
and secret-free. Missing, stale, substituted or wrong-scope evidence SHALL fail
the gate; a waiver SHALL NOT manufacture a successful observation.

#### Scenario: A local fixture is offered as deployed evidence
- **WHEN** acceptance cites source tests or lab observations for a staging or production behavior that was not observed there
- **THEN** the gate SHALL reject that substitution

#### Scenario: Gate evidence changes scope
- **WHEN** a later decision points to a different run, customer, environment, profile or candidate than the evidence proves
- **THEN** acceptance SHALL fail until consistent evidence and approvals are supplied
