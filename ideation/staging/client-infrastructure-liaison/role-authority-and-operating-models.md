# Client Infrastructure Liaison Role, Authority, And Operating Models

Status: staged
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Target capabilities: `client-infrastructure-liaison` (ADDED) and
`roles-authority-model` (MODIFIED)

## Capability Shape

The liaison is a named Client Hermes capability profile with one accountable
owner. It composes existing Client Hermes responsibilities rather than adding
an always-running autonomous agent for each concern.

| Existing Client Hermes role | Liaison contribution |
|---|---|
| Client Profile Steward | accountable operator, contacts, tenant and deployment profile |
| Integration And Credential Steward | system bindings, package channels, permission and grant readiness |
| Policy And Approval Gatekeeper | approval, change-window, risk, and outbound-send policy |
| Fulfillment Or Delivery Coordinator | assignment, deadline, acknowledgment, status, and dependency tracking |
| Communication And Handoff Agent | ticket, email, Teams, reminders, and escalation messages |
| Quality And Outcome Monitor | readiness validation, SLA, evidence, and completion criteria |
| Client Memory Steward | retention and promotion of client-level operating history |

One deployment may assign several responsibilities to one human-assisted role;
another may distribute them across services and people. The capability must
always expose one accountable owner and the same request contract.

## Authority Matrix

| Action | Liaison | Client approver | Client sysadmin | Managed host provider | OpsxFactory |
|---|---:|---:|---:|---:|---:|
| Identify dependency | R | I | I | I | I |
| Draft request | R | C | C | C | C |
| Approve privileged change | C | A | C | C | C |
| Send external request | R, subject to policy | A when required | I | I | I |
| Execute tenant change | no | no | R in client-managed mode | R in managed-host mode | R in Opsx mode |
| Assert implementation complete | no | no | R | R | R |
| Assert readiness | C | I | C | C | C |
| Accept readiness for factory use | R under validation policy | A when required | I | I | I |
| Deprovision or weaken security | no | A | R when authorized | R when authorized | R when authorized |

`A` is accountable approval authority; `R` performs the action; `C` is
consulted; `I` is informed. The liaison never receives standing tenant-admin
authority by virtue of coordinating the work.

## Operating Models

### Customer Managed

The client owns its tenant and performs privileged work. The liaison sends a
structured request through the client's approved channel, correlates the
external ticket, and independently validates readiness.

### Managed Host Add-On

A contracted provider manages only the factory's required infrastructure. Its
capability grant is limited to the named hosts and action classes. The provider
does not become the client's general IT operator.

### Full OpsxFactory

OpsxFactory receives the handoff, applies its domain and client policy, creates
bounded execution jobs, and returns evidence and readiness results. The
requesting domain still receives no tenant-administration credential.

## Bootstrap And Recovery Independence

The liaison's durable request state and alert path must not exist solely on the
same system it manages. If Omni001 hosts part of the client runtime, an
Omni001 outage must still be observable and actionable.

Each installation declares one out-of-band control path:

- another healthy Hermes/Omnigent host;
- a hosted xFactory control service;
- OpsxFactory managed-service control plane;
- client ticketing or monitoring automation; or
- a human-admin notification path with durable external tracking.

The out-of-band path needs enough authority to detect stale heartbeat, create
or update the request, notify the accountable operator, and validate recovery.
It does not automatically receive authority to perform the privileged repair.

## Activation Gate

A factory dependency cannot become production-ready until Client Hermes has:

- selected an operating model;
- assigned the liaison capability owner;
- assigned execution and approval authorities;
- configured primary and out-of-band communication paths;
- named validation profiles and trusted validators;
- recorded response, restoration, and escalation targets; and
- successfully exercised one failure-and-recovery scenario.
