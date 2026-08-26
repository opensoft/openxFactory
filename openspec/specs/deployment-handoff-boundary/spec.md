# deployment-handoff-boundary Specification

## Purpose
TBD - created by archiving change add-deployment-handoff-boundary. Update Purpose after archive.
## Requirements
### Requirement: The managed-subject test routes deployment execution
A release deployment SHALL be executed by the factory that manages the target
surface, decided solely by the managed-subject test: does the deployment
target resolve to a registered subject in the managing factory's
service-subject model? A registered managed subject SHALL be reached only
through a governed handoff to the managing factory; a target inside the
producing factory's own execution lane — ephemeral CI containers, per-job
bench instances, state torn down with the job, no subject record — SHALL be
self-served with no handoff. Environment tier SHALL calibrate governance
depth only and SHALL NOT decide the executor. The rule SHALL bind every actor
class: factory workers, CI pipelines, and human engineers alike.

#### Scenario: A QA deployment targets the managed QA stack
- **WHEN** a producing factory releases onto a QA cluster that is a registered subject of the managing factory
- **THEN** the release crosses as a governed handoff that the managing factory executes, exactly as production would
- **AND** only the approval depth and accepted-risk posture differ from the production path

#### Scenario: An ephemeral CI container runs production-candidate code
- **WHEN** work runs in the producing factory's own execution lane and is torn down with the job, with no subject record
- **THEN** the producing factory self-serves and no handoff request exists, regardless of what code the container runs

#### Scenario: An actor bypasses the boundary directly
- **WHEN** any actor — factory worker, CI pipeline, or human engineer — mutates a surface carrying a registered managed subject without a governed handoff
- **THEN** the act is the same boundary violation for every actor class

#### Scenario: A preview environment outlives its job
- **WHEN** a preview surface gains exposure to real users or persists beyond its producing job, per the governing threshold policy
- **THEN** it acquires a subject record and subsequent changes flip to the handoff path

### Requirement: The handoff crosses as a client infrastructure request
The deployment handoff SHALL cross as a `client_infrastructure_request` — or
a deployment requirements-profile of it — with `execution_binding.mode` of
`opsxfactory_executed` or `managed_host`; a new record kind SHALL NOT be
introduced for this purpose. The producing factory's authority SHALL end at
the release: the built artifact, its immutable digests, and
release-realization evidence.

#### Scenario: A producing factory exits by handing off
- **WHEN** a release whose target is a registered managed subject completes its producing factory's gates
- **THEN** the factory's release exit emits the request draft and no direct deploy path executes

#### Scenario: A deployment is attempted without an accepted request
- **WHEN** an actor seeks to deploy onto a managed subject with no accepted request
- **THEN** no credential path exists to execute it, because deployment grants issue only against an accepted request

### Requirement: No standing deployment credentials outside the managing factory
Only the managing factory's execution identities SHALL hold standing write
credentials to managed surfaces. Producing-factory worker and CI identities
SHALL hold no credential that reaches a deployed surface — push rights extend
to their own build namespaces only, and promotion into deployed or bench
namespaces is the managing factory's act. Deployment-operator credentials
SHALL exist only as managing-factory grants under `credential-contracts`,
issued against an accepted request whose target resolves to a registered
subject, and revoked on completion. Human direct access SHALL be break-glass
only: a time-boxed credential checkout with evidence, followed by a
retroactive request within the governing policy window.

#### Scenario: Grant issuance is the authoritative gate
- **WHEN** the managing factory issues a deployment grant
- **THEN** the issuance verifies an accepted request whose target resolves to a registered subject, so the subject-registry lookup happens where the credential is born

#### Scenario: CI pushes an artifact
- **WHEN** producing-factory CI publishes a built artifact
- **THEN** the push lands in the factory's own build namespace and the identity holds no path into deployed or bench namespaces

#### Scenario: An operator breaks glass
- **WHEN** a human performs an emergency out-of-band action on a managed subject via a time-boxed credential checkout
- **THEN** a retroactive request correlating the change, with evidence and disposition, MUST land within the policy window

### Requirement: Managed surfaces admit change through structural channels
Where the surface supports it, the governed channel SHALL be structural:
pull-only reconciliation from a configuration tree the managing factory
governs — whose branch protection and review ownership are the external
enforcement — or managed assignment for endpoints. Deploying SHALL be merging
into the governed tree; push-path mutation SHALL be a grant-gated exception,
never the norm.

#### Scenario: A cluster deployment merges the governed tree
- **WHEN** a release deploys onto a managed cluster reconciling pull-only from the governed configuration tree
- **THEN** the deployment is a reviewed merge into that tree and the reconciler applies it, with no push credential involved

#### Scenario: A push-path mutation is attempted as the norm
- **WHEN** an actor mutates a structurally governed surface by direct push without a grant
- **THEN** the act is a boundary violation and the correlation audit surfaces it as a finding

### Requirement: Out-of-band change is detectable
Every observed change on a managed subject SHALL correlate to an accepted
request. Execution SHALL stamp the request's correlation identifier into the
change surfaces it touches — configuration-tree commit trailers, deployment
annotations, endpoint assignment metadata — and a periodic
evidence-correlation audit SHALL join observed changes against accepted
requests. An observed change with no correlated request SHALL be a
first-class finding under the established finding classes.

#### Scenario: A stamped change correlates trivially
- **WHEN** the audit joins observed changes against accepted requests
- **THEN** every governed change resolves by its stamped correlation identifier

#### Scenario: An unstamped change appears
- **WHEN** an observed change on a managed subject carries no correlation identifier or correlates to no accepted request
- **THEN** the audit records a first-class finding, which is how break-glass and bypass become visible rather than silent

### Requirement: Cadenced publication rides a standing maintenance request
Recurring publication onto a managed surface SHALL ride one standing approved
request per policy period rather than per-run approvals; each run SHALL stamp
the standing request's correlation identifier and its artifact digests as
evidence, and the standing request SHALL renew at the policy period.

#### Scenario: A scheduled rebuild publishes
- **WHEN** a scheduled or triggered rebuild publishes onto the managed surface during an approved policy period
- **THEN** the run stamps the standing request's correlation identifier and artifact digests without a per-run approval

#### Scenario: The policy period lapses
- **WHEN** the standing request's policy period ends without renewal
- **THEN** subsequent runs have no accepted request to correlate to and the credential and audit gates treat them as unauthorized

### Requirement: Adoption is phased, never gapped
The boundary SHALL ratify at full strength with the target state explicit,
while existing standing administrative access SHALL be a named, dispositioned
exception until the break-glass checkout path is realized and tested; a
dated milestone SHALL then remove standing assignments. Standing access
SHALL NOT be removed before the emergency path provably works.

#### Scenario: The break-glass path is not yet proven
- **WHEN** the escrow checkout path has not been realized and tested
- **THEN** existing standing admin remains as a recorded, dispositioned exception rather than an undocumented violation

#### Scenario: The break-glass path is proven
- **WHEN** the checkout path is realized and a test checkout has succeeded
- **THEN** a dated milestone removes the standing assignments and the exception closes

