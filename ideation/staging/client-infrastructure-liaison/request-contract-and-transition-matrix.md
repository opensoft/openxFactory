# Client Infrastructure Request Contract And Transition Matrix

Status: staged
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Target capability: `client-infrastructure-request` (ADDED)

## Artifact Boundary

`client_infrastructure_request` is a durable coordination artifact. It records
an infrastructure outcome that a factory requires from a client administrator,
a managed-host provider, or OpsxFactory. It is not a worker job envelope.

```text
client infrastructure request
  -> may authorize or correlate to zero or more bounded Hermes jobs
  -> receives execution evidence
  -> receives a separately signed readiness result
```

The request remains authoritative for client coordination. Each job envelope
remains authoritative for one bounded execution attempt.

## Identity Classes

The schema must not use one reference type for every participant.

| Reference | Meaning |
|---|---|
| `organization_ref` | Client or contracted provider organization |
| `subject_ref` | System, service, identity, person, or other served subject |
| `actor_ref` | Person, service, agent, or group performing an action |
| `authority_ref` | Role, group, council, or person authorized to approve |
| `capability_ref` | Scoped action class the execution actor may exercise |
| `credential_grant_ref` | Opaque reference to a short-lived grant; never a secret value |

An actor may also be a service subject, but the records remain separate and
link by durable identifier.

## Minimum Request Shape

```yaml
schema_version: 1
kind: client_infrastructure_request
request_id: cir-southside-omni001-provision
idempotency_key: southside:omni001:provision:v1
correlation_id: medx-install-southside-001
client_ref: southside-clinic
requesting_factory: MedxFactory
requesting_component: MedxOmni
request_type: provision
managed_subject_refs:
  - southside-omni001
requirements_profile:
  id: omnigent-cloudpc-host
  version: 1
execution_binding:
  mode: client_managed
  organization_ref: southside-clinic
  actor_ref: southside-primary-sysadmin
  capability_ref: southside-endpoint-administration
approval:
  required: true
  authority_ref: southside-it-director
communication:
  channel_ref: southside-it-service-desk
  external_ticket_ref: null
package_refs:
  - uri: cloudpc-install://packages/omni-host/1.0.0
    digest: sha256:<digest>
runbook_refs:
  - cloudpc-install://runbooks/omni-cloudpc-provisioning-v1
validation_profile:
  id: omnigent-cloudpc-ready
  version: 1
required_by: 2026-08-01T17:00:00Z
status: request_drafted
conditions: []
evidence_refs: []
created_by: southside-care-infrastructure-liaison
created_at: 2026-07-09T23:00:00Z
```

## Required Invariants

- `request_id` is globally unique within the client installation.
- Repeated intake with the same `idempotency_key` returns the existing open
  request rather than creating a duplicate.
- Every external ticket stores the internal `request_id` and `correlation_id`.
- A package reference includes an immutable digest and approved publisher.
- Secret values, passwords, refresh tokens, and raw provider profiles are
  forbidden in all fields and attachments.
- `execution_binding` identifies an actor and capability; it does not make the
  execution actor an approval authority.
- A request may reference job envelope IDs, but it may not embed a reusable
  credential in a job.
- `completed` requires a current, passing readiness result for the selected
  validation profile.

## State Transition Matrix

| From | To | Authorized actor | Guard and required evidence |
|---|---|---|---|
| `identified` | `request_drafted` | liaison capability owner | dependency, client, target, and requirement profile identified |
| `request_drafted` | `awaiting_client_approval` | liaison capability owner | execution binding and approval authority resolved |
| `request_drafted` | `submitted` | liaison capability owner | approval policy explicitly says approval is not required |
| `awaiting_client_approval` | `submitted` | approval authority | approval record and approved request digest present |
| `awaiting_client_approval` | `declined` | approval authority | decline reason present |
| `submitted` | `acknowledged` | execution actor or external adapter | acknowledgment and external ticket correlation present |
| `acknowledged` | `scheduled` | execution actor | execution owner and change window accepted |
| `scheduled` | `implementing` | execution actor | start event and active capability grant reference present when privileged |
| `implementing` | `validation_pending` | execution actor | implementation evidence and claimed outcome present |
| `validation_pending` | `completed` | trusted validator | passing readiness result within its freshness TTL |
| `validation_pending` | `validation_failed` | trusted validator | failed checks and evidence references present |
| `validation_failed` | `scheduled` | execution actor | remediation plan or retry decision present |
| any nonterminal state | `blocked` | current owner or policy gate | blocker class, owner, and next review time present |
| `blocked` | prior resumable state | blocker owner or policy gate | blocker-resolution evidence present |
| any nonterminal state | `cancelled` | requester plus required approval authority | cancellation reason and downstream propagation result present |

`declined`, `cancelled`, and `completed` are terminal for that request. Reopening
a completed outcome creates a new request with `supersedes_request_ref` rather
than mutating the historical record.

## Conditions And Timers

`overdue`, `escalated`, `maintenance_hold`, and `awaiting_external_response`
are conditions, not states. A condition records:

```yaml
condition:
  type: overdue
  active: true
  observed_at: 2026-08-01T17:05:00Z
  policy_ref: southside-infrastructure-escalation-v1
  evidence_refs: []
```

Escalation creates an event and notification without losing the underlying
workflow state. Clearing a condition records who cleared it and why.

## Correlation And Ownership

- Client Hermes owns the neutral request record.
- The execution system owns its internal ticket or Opsx service request.
- Status projection never transfers source-of-truth ownership.
- A handoff is accepted only after the execution system returns its durable
  work-item identifier.
- Duplicate external notifications reconcile by `request_id`,
  `idempotency_key`, and `correlation_id`.
- Cancellation and material scope changes propagate to every active child job
  or external work item and record each acknowledgment.

## Outbound Communication

Creating or updating an external ticket, email, or Teams message is an
externally visible action. The request must satisfy the client communication
policy and any human-review requirement before the adapter sends it. A draft
request alone never authorizes an external send.

## Proposal Acceptance Evidence

- schema accepts the minimum valid request;
- embedded secret-like values are rejected;
- duplicate idempotency keys do not create duplicate open requests;
- every transition outside the matrix is rejected;
- overdue and escalation remain orthogonal conditions;
- blocked and validation-failed requests can resume only with evidence;
- completed requires a fresh passing readiness result; and
- cancellation propagation records every child acknowledgment.
