# Southside Clinic Infrastructure Liaison Scenarios

Status: staged
Kind: reference
Summary: Works the liaison request lifecycle through Southside Clinic's
customer-managed, managed-host, and OpsxFactory-bound operating scenarios as
concrete reference traces.
Topics: client-infrastructure-liaison, southside-clinic, operating-model-scenarios, medxfactory
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Target capabilities: `client-infrastructure-liaison` (ADDED) and
`client-infrastructure-request` (ADDED)

## Customer-Managed Provisioning

Southside buys MedxFactory but not OpsxFactory. Care Hermes identifies the
Omni001 dependency. Its Care Infrastructure Liaison drafts a request, obtains
Southside approval, and submits it to Southside's service desk. Southside IT
performs the Intune and Windows 365 work. A trusted read-only validator checks
the resulting host. The request completes only when the readiness result is
fresh and passing.

Expected evidence: approved request digest, external ticket correlation,
package digest, administrator completion evidence, and readiness result.

## Managed-Host Add-On

Southside contracts Opensoft only for the Omni host. The execution binding
grants the managed-host provider capability over named Omni devices, not the
entire tenant. The liaison tracks the same neutral request and validation
contract used in customer-managed mode.

Expected evidence: service entitlement, scoped capability grant, execution
record, and readiness result.

## Full OpsxFactory

Care Hermes hands the request to Southside IT Hermes. OpsxFactory acknowledges
it with an Opsx service-request ID, applies Southside and Operations Domain
policy, performs bounded work through Opsx Omnigent, and returns execution
evidence. Care Hermes closes the neutral request only after readiness passes.

Expected evidence: handoff acceptance, Opsx request and job references,
approval records, capability grants, execution evidence, and readiness result.

## Omni001 Outage

Omni001 stops heartbeating before the nightly sweep. The out-of-band monitor
marks the dependency unavailable and creates or updates one idempotent
remediation request. MedxFactory stops routing affected work. The liaison
notifies the bound operator, tracks escalation independently of Omni001, and
validates recovery before dispatch resumes.

Expected evidence: last healthy heartbeat, failed checks, notification and
acknowledgment, remediation record, new readiness result, and dispatch-resume
event.

## Validation Failure

The administrator reports completion, but the GitHub runner is offline. The
request moves to `validation_failed`, not `completed`. The failed check and
evidence are returned to the execution owner, who schedules remediation. A new
readiness result is required after repair.

## Cancellation During Execution

Southside cancels provisioning after an Opsx job starts. The liaison propagates
cancellation to the Opsx service request and child job. The final neutral
record reports whether execution stopped, partially completed, or completed
before cancellation; it never rewrites historical evidence.
