# client-infrastructure-liaison Specification

## Purpose

Establish the Client Infrastructure Liaison — the neutral coordination
profile every Client Hermes scaffold declares for a dependency someone else
controls, with exactly one accountable owner composed from existing Client
Hermes roles rather than a new always-running agent, and domain display
aliases resolving to this same contract. Hold the boundary that makes such
coordination safe: the liaison coordinates only, never holding
tenant-administration authority, executing privileged change, carrying
secret values, or bypassing client approval or an OpsxFactory gate, so
coordination, execution and validation stay three parties and are never
collapsed into one. Fix the three execution bindings a dependency may be
coordinated under — client-managed, managed-host, and OpsxFactory-executed —
the activation gate an instance must satisfy before it goes live, and the
out-of-band recovery path required wherever a managed dependency hosts the
very control plane used to coordinate it.
## Requirements
### Requirement: Liaison coordination profile
Every Client Hermes scaffold SHALL declare a Client Infrastructure Liaison — a neutral coordination profile with exactly one accountable owner, composed from existing Client Hermes roles (profile steward, integration and credential steward, policy and approval gatekeeper, fulfillment coordinator, communication and handoff agent, quality and outcome monitor, memory steward) rather than a new always-running agent, and domain display aliases (Care/Firm/Marketing/Engineering/IT Infrastructure Liaison) SHALL resolve to this same neutral contract. An install MAY disable active routing, but MUST still declare the responsible operator and an escalation path.

#### Scenario: Domain alias resolves to the neutral role
- **WHEN** a domain scaffold declares "Care Infrastructure Liaison" (or any domain alias)
- **THEN** it MUST resolve to the neutral liaison contract with the same authority boundary and lifecycle obligations, not to a domain-defined variant

#### Scenario: Routing disabled without an operator
- **WHEN** a Client Hermes install disables the liaison's active routing but declares no responsible operator or escalation path
- **THEN** scaffold validation MUST fail

### Requirement: Coordination, execution, and validation separation
The liaison SHALL only coordinate: it MUST NOT hold standing tenant-administration authority (Intune/Entra/Azure/endpoint/global-admin or equivalent), MUST NOT execute privileged change directly or via a domain worker, MUST NOT place secret values in requests, communications, artifacts, or Hermes memory, and MUST NOT bypass client approval, change policy, or an OpsxFactory gate. Privileged work SHALL be performed only by the request's approved execution owner, and outcome SHALL be verified only by a neutral readiness validator — three parties, never collapsed into one.

#### Scenario: Privileged execution assigned to the liaison
- **WHEN** a request's execution binding names the liaison (or any identity it holds) as the executing actor for privileged work
- **THEN** validation MUST reject the request

#### Scenario: Secret value placed in a request
- **WHEN** any request field, condition, or communication record carries a secret value rather than an opaque reference
- **THEN** deterministic validation MUST fail the record

#### Scenario: Ownership does not confer authority
- **WHEN** the liaison owns an open request targeting a client tenant
- **THEN** the liaison gains no tenant-administration authority from that ownership, and any privileged action still requires the binding's approved execution owner and grant

### Requirement: Operating models
The request contract SHALL support three execution bindings — client-managed (the client's own sysadmin under client-tenant authority) and OpsxFactory-executed (a bounded Managed System workflow under an approved capability grant) as MUST-support bindings, and managed-host (a contracted Opensoft operations profile scoped to named hosts and action classes, never the tenant) as a SHOULD-support binding. The requesting domain SHALL receive readiness and capacity status only, never tenant-administration credentials.

#### Scenario: Client-managed request routes to the client's sysadmin
- **WHEN** a client-managed request is submitted
- **THEN** it routes to the client's authorized sysadmin channel, and no Opensoft identity performs the privileged change

#### Scenario: OpsxFactory-bound request keeps the neutral envelope
- **WHEN** the same dependency is instead bound to OpsxFactory execution
- **THEN** the neutral request record is unchanged in shape — only the execution binding and correlation differ

#### Scenario: Managed-host grant exceeds its host scope
- **WHEN** a managed-host binding's grant reference covers actions or hosts beyond the named set
- **THEN** the request MUST NOT proceed past approval

### Requirement: Activation gate
A liaison instance SHALL activate only when its activation gate is satisfied: operating model selected; accountable owner assigned; execution and approval authorities assigned; primary and out-of-band coordination paths configured; validation profiles and trusted validators named; response, restoration, and escalation targets recorded; and one failure-and-recovery scenario successfully exercised. Defaults are configured-but-inactive; activation becomes blocking when any declared component requires an external operator.

#### Scenario: Component requires an external operator
- **WHEN** an install declares a component whose infrastructure requires an external operator and the liaison activation gate is unsatisfied
- **THEN** install activation MUST block on the gate, not proceed with an unowned dependency

#### Scenario: Activation without an exercised recovery scenario
- **WHEN** activation is attempted with every field configured but no failure-and-recovery scenario exercised
- **THEN** the gate MUST fail with the missing-evidence reason

### Requirement: Bootstrap and out-of-band recovery independence
Where a managed dependency hosts any part of its own control plane, the liaison configuration SHALL declare an out-of-band recovery path that does not depend on the managed dependency itself, and loss of the primary coordination path MUST degrade to that out-of-band path rather than to silence.

#### Scenario: Managed host carries its own control plane
- **WHEN** the dependency being coordinated hosts the very channel used to coordinate it (e.g. the Omni host running the Hermes runtime)
- **THEN** the configuration MUST name an independent out-of-band monitor and remediation path, and its absence fails validation

#### Scenario: Outage produces one idempotent remediation request
- **WHEN** the out-of-band monitor detects the dependency unavailable
- **THEN** it marks availability, creates or updates exactly one idempotent remediation request, and routing to the dependency stops without weakening any data boundary

