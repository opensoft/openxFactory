# Client Infrastructure Liaison

Status: draft
Kind: architecture
Repository context: openxFactory
Purpose: define the neutral Client Hermes role that coordinates privileged
infrastructure dependencies on a client tenant, a contracted managed host, or
OpsxFactory — and the `client_infrastructure_request` lifecycle it drives —
without any domain agent or the liaison itself ever holding
tenant-administration authority.

> This document is the normative prose home for the liaison role, its
> authority boundary, the three operating models, and the request lifecycle +
> transition matrix. It is authored under the active change
> `add-client-infrastructure-liaison` (capabilities `client-infrastructure-liaison`
> and `client-infrastructure-request`); it flips to `Status: ratified` with a
> `Ratified by:` pointer at that change's ratification gate. The machine-checked
> shape lives in `contracts/schemas/xfactory-client-infrastructure-request.schema.yaml`
> and `contracts/schemas/xfactory-infrastructure-readiness-result.schema.yaml`,
> enforced by `scripts/validate-client-infrastructure.py`.

## 1. Role

Every DomainxFactory install depends on infrastructure someone else controls —
a customer's own tenant, a contracted managed host, or a purchased OpsxFactory
instance. The **Client Infrastructure Liaison** is the neutral Client Hermes
coordination profile that owns that dependency end to end without becoming its
privileged executor.

- **One accountable owner.** The liaison is a named coordination profile with
  exactly one accountable owner per install.
- **Composed, not a new agent.** It is composed from existing Client Hermes
  roles (profile steward, integration and credential steward, policy and
  approval gatekeeper, fulfillment coordinator, communication and handoff
  agent, quality and outcome monitor, memory steward — see
  [Client Hermes Product And Service Scaffold](client-hermes-product-service-scaffold.md)
  §4), never a new always-running autonomous agent.
- **Present in every Client Hermes scaffold.** An install MAY disable active
  routing when it has no external infrastructure dependency, but it MUST still
  declare the responsible operator and an escalation path.
- **Domain aliases resolve to the neutral contract.** A domain scaffold may
  show a contextual display name; every alias resolves to this same neutral
  role, with the same authority boundary and lifecycle obligations — never a
  domain-defined variant.

| Domain stack | Client Hermes | Display alias |
|---|---|---|
| MedxFactory | Care Hermes | Care Infrastructure Liaison |
| LedgerxFactory | Firm Hermes | Firm Infrastructure Liaison |
| AdxFactory | Marketing Company Hermes | Marketing Infrastructure Liaison |
| codexFactory | Software Company Hermes | Engineering Infrastructure Liaison |
| OpsxFactory | Organization IT Hermes | IT Infrastructure Liaison |

## 2. Authority Boundary

Privileged infrastructure work has **three parties that are never collapsed
into one**: the coordinating liaison, the approved execution owner, and the
neutral readiness validator. The liaison only coordinates.

The liaison **IS NOT** and **MUST NOT**:

- hold standing tenant-administration authority (Intune / Entra / Azure /
  endpoint / global-admin or any equivalent) merely because the role exists;
- execute a privileged change directly or through a domain worker;
- place a secret value (password, token, refresh token, raw provider profile)
  in any request field, condition, communication, artifact, or Hermes memory —
  references only;
- treat request submission or an administrator's acknowledgment as proof the
  target is ready; or
- bypass client approval, local change policy, or an OpsxFactory gate.

Ownership confers no authority: when the liaison owns an open request targeting
a client tenant, it gains no tenant-administration authority from that
ownership, and any privileged action still requires the binding's approved
execution owner and grant. The requesting domain receives readiness and
capacity status only — never tenant-administration credentials.

Structurally, the request record separates the identity classes so this
boundary is machine-checkable: `execution_binding.actor_ref` is never equal to
`approval.authority_ref` nor to the coordinating creator, and a served subject
identifier never appears in an actor, capability, or authority field.

## 3. Operating Models

The request supports three execution bindings. `client_managed` and
`opsxfactory_executed` are MUST-support bindings; `managed_host` is
SHOULD-support (design D1).

| Operating model | `execution_binding.mode` | Execution owner | Privileged authority |
|---|---|---|---|
| Customer-managed | `client_managed` | Client system administrator | Client tenant |
| Managed-host add-on | `managed_host` | Contracted Opensoft operations profile | Narrow host-management scope over named hosts only, never the tenant |
| Full OpsxFactory | `opsxfactory_executed` | OpsxFactory Managed System workflow | Approved OpsxFactory capability grant |

OpsxFactory is a peer domain stack and the canonical privileged execution path
when purchased; it is never silently embedded in another domain. Vocabulary
coined upstream (the typed actor/capability/authority projection, subject
kinds, and OpsxFactory workflow/credential/subject tokens) is **consumed, not
renamed**: the neutral request maps onto it at the handoff boundary.

## 4. The Request Contract

`client_infrastructure_request` is a **durable coordination record**, distinct
from a Hermes job envelope: one request may authorize or correlate to zero or
more bounded jobs, but is never one. It carries six never-conflated identity
reference classes:

| Reference | Meaning |
|---|---|
| `organization_ref` | Client or contracted provider organization |
| `subject_ref` | System, service, identity, person, or other served subject |
| `actor_ref` | Person, service, agent, or group performing an action |
| `authority_ref` | Role, group, council, or person authorized to approve |
| `capability_ref` | Scoped action class the execution actor may exercise |
| `credential_grant_ref` | Opaque reference to a short-lived grant; never a secret value |

Required invariants (enforced by the validator where schema cannot): a unique
`request_id`; a duplicate `idempotency_key` returns the existing open request;
every external ticket stores the internal `request_id` and `correlation_id`; a
`package_refs` entry carries an immutable digest from an approved publisher;
secrets are forbidden everywhere; `completed` requires a fresh passing
readiness result. The full source shape is the change's
[Request Contract And Transition Matrix](../openspec/changes/add-client-infrastructure-liaison/supporting-docs/request-contract-and-transition-matrix.md).

## 5. Lifecycle And Transition Matrix

The `status` lifecycle is a closed enum. The controlled path is:

```text
identified -> request_drafted -> awaiting_client_approval -> submitted
  -> acknowledged -> scheduled -> implementing -> validation_pending -> completed
```

Exceptional states are `blocked`, `declined`, `validation_failed`, and
`cancelled`. `completed`, `declined`, and `cancelled` are **terminal**:
reopening completed work — or a material scope change (changed target,
requirements profile, or security boundary) on an open request — is a **new
request carrying `supersedes_request_ref`**, never a mutation of the
predecessor. Every transition is legal only for its authorized actor class
under its guard:

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

## 6. Conditions

`overdue`, `escalated`, `maintenance_hold`, and `awaiting_external_response`
are **conditions, not states**. Each records `type`, `active`, `observed_at`,
`policy_ref`, and clearing evidence, and coexists with any nonterminal
workflow state. Expressing overdue or escalation as a `status` value fails
validation. An active `overdue` condition escalates **along the request's
configured escalation path, in order**, each step recorded as condition
evidence, while the workflow `status` is unchanged by the escalation itself.

## 7. Handoff Contract

A request bound to an external execution system keeps the **neutral request
and the execution system's own record as separate records with separate
owners**. Client Hermes remains the source of truth for the requested outcome
and client communication; the execution system becomes the source of truth for
privileged execution **only after it returns an accepted work-item
identifier**. Acceptance is recorded in the request's `handoff` block
(`infrastructure_request_ref`, `correlation_id`, `receiving_system`, the
external work-item reference, `accepted_by_actor_ref`, `projected_status`).

- Projection never overwrites the execution system's internal state; old or
  duplicate sequences are ignored (`mapping_version` orders them).
- Loss of connection to the execution system moves the request to `blocked`
  (or activates an awaiting condition) — **never toward success**.
- Cancellation and material scope changes propagate to every active child job
  and external work item; each system's acknowledgment (`stopped` /
  `partially_applied` / `completed`) is recorded in `child_acks`, and history
  is never rewritten.

See the change's
[Opsx Handoff And Readiness Contract](../openspec/changes/add-client-infrastructure-liaison/supporting-docs/opsx-handoff-and-readiness-contract.md).

## 8. Readiness Contract

The transition to `completed` requires a fresh passing
`infrastructure_readiness_result` — a signed / otherwise traceable artifact,
**never a bare boolean** — with overall status in
`ready | degraded | not_ready | unknown | maintenance`, produced by a trusted
validator named in the request's validation profile, used only before its
`valid_until`, and with **every mandatory check passing**. Validation is
**non-privileged**: the validator cannot change the target and holds at most
granted read-only access. Submission, acknowledgment, or an execution actor's
claim of completion does not count as readiness evidence. When a mandatory
check fails, the request moves to `validation_failed`, the failed checks return
to the execution owner, and a new passing result is required after
remediation.

## 9. Activation Gate

A liaison instance activates only when its activation gate is satisfied:

- operating model selected;
- accountable owner assigned;
- execution and approval authorities assigned;
- primary and out-of-band coordination paths configured;
- validation profiles and trusted validators named;
- response, restoration, and escalation targets recorded; and
- one failure-and-recovery scenario successfully exercised.

Defaults are **configured-but-inactive**. Activation becomes **blocking** when
any declared component requires an external operator: install activation MUST
block on the gate rather than proceed with an unowned dependency, and a gate
attempted with every field configured but no exercised recovery scenario fails
with the missing-evidence reason.

## 10. Bootstrap And Out-Of-Band Recovery

Where a managed dependency hosts any part of its own control plane (for
example, the Omni host that runs the Hermes runtime coordinating it), the
liaison configuration MUST declare an **out-of-band recovery path that does not
depend on the managed dependency itself**. Loss of the primary coordination
path degrades to that out-of-band path rather than to silence. When the
out-of-band monitor detects the dependency unavailable, it marks availability,
creates or updates **exactly one idempotent remediation request**, and routing
to the dependency stops without weakening any data boundary. A domain MAY use
an explicitly approved fallback but MUST NOT route protected or client-scoped
data to an unapproved fallback merely because infrastructure is unavailable.

## 11. Deterministic Validation

`scripts/validate-client-infrastructure.py` (openxFactory-owned, invoked from
the pinned checkout, never copied into domain repos) schema-validates both
kinds and enforces what schema cannot: embedded-secret rejection (via the
shared `contracts/avatar-client/redaction/` denylist), transition legality
including terminal immutability and readiness-gated completion, identity-class
separation (`execution_binding.actor_ref` never equal to
`approval.authority_ref` nor the coordinating creator; a subject identifier
never in a typed field), idempotency/supersedes integrity, and
cancellation-acknowledgment presence. It self-tests the packaged
`examples/client-infrastructure/` set on every run and fails closed if any
negative stops failing for its intended reason.

## 12. Worked Scenarios

Concrete Southside Clinic reference traces (synthetic org) for each operating
model, plus the outage, validation-failure, and cancellation cases, are in the
change's
[Southside Operating Model Scenarios](../openspec/changes/add-client-infrastructure-liaison/supporting-docs/southside-operating-model-scenarios.md).
The full role/lifecycle prose provenance is
[Client Infrastructure Liaison (staged)](../openspec/changes/add-client-infrastructure-liaison/supporting-docs/client-infrastructure-liaison.md)
and
[Role Authority And Operating Models](../openspec/changes/add-client-infrastructure-liaison/supporting-docs/role-authority-and-operating-models.md).

## 13. Repository Ownership

| Repository or layer | Ownership |
|---|---|
| openxFactory | Liaison role, request + readiness schemas, lifecycle, authority boundary, evidence and escalation contracts, deterministic validator |
| DomainxFactory | Domain-specific dependency profiles, readiness needs, display aliases, and safe fallback policy |
| Client Hermes | Contacts, local policies, channels, approvals, deadlines, and request history (instance records) |
| OpsxFactory | Privileged IT execution workflows and Managed System operations |
| CloudPC-Install | Cloud PC installation packages, runbooks, detection, remediation, and host readiness validators |
| Omnigent-Install | Worker runtime requirements, worker packs, and application health contract |
