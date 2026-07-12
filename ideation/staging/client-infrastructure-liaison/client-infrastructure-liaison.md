# Staged: Client Infrastructure Liaison

Status: staged
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Source: Southside Clinic MedxFactory and OpsxFactory operating-model review,
2026-07-09.
Target capabilities: `client-infrastructure-liaison` (ADDED),
`client-infrastructure-request` (ADDED), and
`roles-authority-model` (MODIFIED).

## Problem

Every DomainxFactory can depend on infrastructure controlled by the client or
by a separately contracted operations provider. Examples include Cloud PCs,
Intune applications, Entra identities, endpoint policies, networks, storage,
and integration services. The current Client Hermes scaffold owns client
contacts, tenant configuration, local policy, integrations, and escalation,
but it does not define a neutral role or lifecycle for coordinating privileged
infrastructure work.

Without a shared capability, domain stacks face two unsafe choices:

1. give a medical, accounting, marketing, or engineering agent tenant
   administration authority; or
2. handle required infrastructure through informal email with no durable
   owner, deadline, validation, or completion evidence.

The neutral layer needs a Client Hermes capability that coordinates this work
without becoming the privileged executor.

## Proposed Capability

Add a base Client Hermes capability named **Client Infrastructure Liaison**.
It is a named coordination profile with one accountable owner, composed from
the existing integration, policy, fulfillment, communication, and quality
roles rather than a new always-running autonomous agent. Domain factories may
give the capability a contextual display name, but they specialize the same
neutral contract.

| Domain stack | Client Hermes | Example display name |
|---|---|---|
| MedxFactory | Care Hermes | Care Infrastructure Liaison |
| LedgerxFactory | Firm Hermes | Firm Infrastructure Liaison |
| AdxFactory | Marketing Company Hermes | Marketing Infrastructure Liaison |
| codexFactory | Software Company Hermes | Engineering Infrastructure Liaison |
| OpsxFactory | Organization IT Hermes | IT Infrastructure Liaison |

The role is present in every Client Hermes scaffold. A deployment may disable
active routing when it has no external infrastructure dependencies, but it
must still declare the responsible operator and escalation path.

## Responsibilities

The Client Infrastructure Liaison:

- tracks infrastructure dependencies of installed factory components;
- identifies the client's authorized system administrators and approvers;
- generates structured provisioning, change, remediation, and deprovisioning
  requests;
- routes requests through an approved ticketing, Teams, or email adapter;
- attaches approved packages, manifests, and runbooks by reference;
- tracks acknowledgment, ownership, deadlines, change windows, and escalation;
- runs non-privileged readiness validation;
- records completion evidence and validation results;
- notifies the requesting factory when capacity becomes ready or unavailable;
- binds execution to OpsxFactory when contracted; and
- binds execution to the client's system administrator when OpsxFactory is
  absent.

The liaison MUST NOT:

- hold standing Intune, Entra, Azure, endpoint, or global-administrator
  authority merely because the role exists;
- execute a privileged change through a domain worker;
- place passwords, tokens, or secret values in requests, email, artifacts, or
  Hermes memory;
- treat request submission or administrator acknowledgment as proof that the
  target system is ready; or
- bypass client approval, local change policy, or an OpsxFactory gate.

## Authority and Execution Boundary

```text
Requesting DomainxFactory
  -> declares required capability and service level
  -> Client Infrastructure Liaison coordinates the dependency
  -> approved execution owner performs privileged work
  -> neutral readiness validator verifies the outcome
  -> requesting DomainxFactory consumes the ready capability
```

The execution owner is selected per client binding:

| Operating model | Execution owner | Privileged authority |
|---|---|---|
| Customer-managed | Client system administrator | Client tenant |
| Managed-host add-on | Contracted Opensoft operations profile | Narrow host-management scope |
| Full OpsxFactory | OpsxFactory Managed System workflow | Approved OpsxFactory capability grant |

The requesting domain receives readiness and capacity status, not Intune or
tenant-administration credentials. OpsxFactory is a peer domain stack and is
the canonical privileged execution path when purchased; it is not silently
embedded in MedxFactory or another domain.

## Hermes Placement

A client may run several logical overlays in one physical Hermes installation.
For example:

```text
Southside Clinic Hermes installation
  -> MedxFactory
     -> Patient Hermes (customer layer)
     -> Care Hermes (client layer)
        -> Care Infrastructure Liaison
     -> Medicine Hermes (domain layer)
  -> optional OpsxFactory
     -> Managed System Hermes for Omni001
     -> Southside IT Hermes for Southside policy and contacts
     -> Managed Service Hermes for MedxOmni or another dependent system
     -> Operations Domain Hermes
```

The physical co-location does not merge authority. Client, customer, and
domain memory, permissions, manifests, and approvals remain logically scoped.

## Request Contract

Add a domain-neutral `client_infrastructure_request` artifact. It is a durable
service-coordination record, not a Hermes job envelope. One infrastructure
request may later authorize or correlate to multiple bounded job envelopes.
It references secrets and installation assets; it never embeds secret
material.

```yaml
schema_version: 1
kind: client_infrastructure_request
request_id: cir-southside-omni001-provision
client_ref: southside-clinic
requesting_factory: MedxFactory
requesting_component: MedxOmni
request_type: provision
managed_system_ref: omni001
requirements_profile: omnigent-cloudpc-host-v1
execution_binding:
  type: client_sysadmin
  actor_ref: southside-primary-sysadmin
  capability_ref: southside-endpoint-administration
approval:
  required: true
  owner_ref: southside-it-director
required_by: 2026-08-01T17:00:00Z
change_window_ref: southside-standard-endpoint-window
package_refs:
  - cloudpc-install://packages/omni-host/1.0.0
runbook_refs:
  - cloudpc-install://runbooks/omni-cloudpc-provisioning-v1
validation_profile: omnigent-cloudpc-ready-v1
status: submitted
```

When OpsxFactory is present, the request remains the same except for its
execution binding:

```yaml
execution_binding:
  type: opsxfactory
  actor_ref: southside-opsx-omnigent
  capability_ref: southside-omni-host-management
  capability_grant_ref: vaultref://southside/opsx/omni-host-management
```

The neutral contract SHOULD also support `managed_host_provider` for a limited
infrastructure add-on that does not activate the full OpsxFactory product.

## Lifecycle

The controlled request lifecycle is:

```text
identified
  -> request_drafted
  -> awaiting_client_approval
  -> submitted
  -> acknowledged
  -> scheduled
  -> implementing
  -> validation_pending
  -> completed
```

Exceptional states are:

```text
blocked
declined
validation_failed
cancelled
```

`overdue` and `escalated` are orthogonal conditions/events, not lifecycle
states. They may apply while a request remains submitted, acknowledged,
scheduled, implementing, blocked, or validation-pending. The transition
matrix, resume paths, cancellation rules, and escalation conditions are
defined in [Request Contract And Transition Matrix](request-contract-and-transition-matrix.md).

Each transition records actor, timestamp, owning Hermes layer, reason, and
evidence references. `completed` requires the named validation profile to pass;
an email reply or ticket resolution alone is insufficient.

## Readiness and Incident Routing

The liaison consumes non-privileged readiness contracts. For an Omnigent Cloud
PC, readiness may combine:

- Windows 365 and Intune device state;
- required package and compliance status;
- GitHub self-hosted runner state;
- Omni host heartbeat freshness;
- Omnigent runtime and dependency health;
- authentication state represented as valid/invalid/refresh-required, never as
  a credential; and
- current capacity, maintenance, and drain state.

When a dependency becomes unavailable:

1. the requesting factory stops dispatching affected work;
2. the liaison opens a remediation request with the bound execution owner;
3. queued work follows its data-boundary and expiration policy;
4. the liaison tracks acknowledgment and escalation;
5. readiness validation repeats after remediation; and
6. dispatch resumes only after the dependency returns to `ready`.

A domain MAY use an explicitly approved fallback. It MUST NOT route protected
or client-scoped data to an unapproved fallback merely because infrastructure
is unavailable.

## Client Binding Requirements

Before a factory installation with external infrastructure dependencies is
activated, Client Hermes MUST record:

- the selected operating model;
- the accountable infrastructure operator;
- authorized administrator and approver contact references;
- supported request channels and escalation order;
- expected response and restoration targets;
- permitted maintenance windows;
- package and runbook delivery mechanisms;
- validation profiles;
- evidence-retention policy; and
- whether OpsxFactory or a managed-host provider is contracted.

If the client declines OpsxFactory and managed-host service, activation is
blocked until the client accepts responsibility and supplies an authorized
system-administrator contact.

## Repository Ownership

| Repository or layer | Ownership |
|---|---|
| openxFactory | Liaison role, request schema, lifecycle, authority boundary, evidence and escalation contracts |
| DomainxFactory | Domain-specific dependency profiles, readiness needs, aliases, and safe fallback policy |
| Client Hermes | Contacts, local policies, channels, approvals, deadlines, and request history |
| OpsxFactory | Privileged IT execution workflows and Managed System operations |
| CloudPC-Install | Cloud PC installation packages, runbooks, detection, remediation, and host readiness validators |
| Omnigent-Install | Worker runtime requirements, worker packs, and application health contract |

## Required Proposal Deltas

The proposal for this staged topic should:

1. add a `client-infrastructure-liaison` capability spec;
2. extend the roles-and-authority model with the coordination-versus-execution
   boundary;
3. define the separate `client_infrastructure_request` schema, its references
   to bounded job envelopes, and its transition rules;
4. add the liaison to the base Client Hermes scaffold and templates;
5. define customer-managed, managed-host, and OpsxFactory bindings;
6. add validation and escalation requirements;
7. add examples for at least one domain without OpsxFactory and one with it;
8. define adoption work for each DomainxFactory; and
9. add deterministic checks for forbidden embedded secrets and invalid
   `completed` transitions.

## Required Tests

- a customer-managed request routes to an authorized client sysadmin;
- an OpsxFactory-bound request retains the same neutral envelope;
- a request cannot complete before its validation profile passes;
- privileged execution is rejected when assigned to the liaison itself;
- missing operator/contact binding blocks activation;
- overdue requests follow the configured escalation path;
- secret values in the request are rejected;
- unavailable infrastructure stops affected dispatch without weakening data
  boundaries; and
- domain aliases resolve to the neutral liaison role.

## Exit

Create an OpenSpec change, recommended ID
`add-client-infrastructure-liaison`, that ratifies the neutral role, request
contract, lifecycle, templates, authority boundary, and adoption plan. At the
proposal gate, move this file to:

```text
openspec/changes/add-client-infrastructure-liaison/supporting-docs/
  client-infrastructure-liaison.md
```

The proposal must preserve this staging origin:

```yaml
origin:
  kind: staged
  id: openxFactory:staging:client-infrastructure-liaison
  path: ideation/staging/client-infrastructure-liaison
```

## Staging Packet

- [Request Contract And Transition Matrix](request-contract-and-transition-matrix.md)
- [Role Authority And Operating Models](role-authority-and-operating-models.md)
- [Opsx Handoff And Readiness Contract](opsx-handoff-and-readiness-contract.md)
- [Proposal Impact And Adoption Map](proposal-impact-and-adoption-map.md)
- [Southside Clinic Infrastructure Liaison Scenarios](southside-operating-model-scenarios.md)
