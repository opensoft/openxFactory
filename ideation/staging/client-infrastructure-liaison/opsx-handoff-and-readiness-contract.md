# Opsx Handoff And Readiness Contract

Status: staged
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Target capabilities: `client-infrastructure-request` (ADDED) and
`client-infrastructure-liaison` (ADDED)

## Handoff Boundary

The neutral infrastructure request and an OpsxFactory service request are
separate records with separate owners.

```text
Client Hermes request                      OpsxFactory service request
  neutral desired outcome                   domain risk and execution detail
  client deadline and communication         subjects, actors, grants, jobs
  acceptance validation                     operational evidence
          |                                             |
          +----------- correlation ---------------------+
```

Client Hermes remains the source of truth for the requested outcome and client
communication. OpsxFactory becomes the source of truth for privileged
execution only after it returns an accepted work-item identifier.

## Acceptance Record

```yaml
handoff:
  infrastructure_request_ref: cir-southside-omni001-remediate
  correlation_id: medx-omni001-outage-003
  receiving_system: OpsxFactory
  receiving_client_ref: southside-clinic
  opsx_service_request_ref: opsx-southside-incident-8821
  accepted_by_actor_ref: southside-opsx-intake
  accepted_at: 2026-07-09T23:05:00Z
  projected_status: acknowledged
```

Projection updates include source record, source sequence, observation time,
and mapping version. Old or duplicate sequences are ignored. A projected state
never overwrites the execution system's internal state.

## Readiness Result

Readiness is a signed or otherwise traceable evidence artifact, not a boolean
message.

```yaml
schema_version: 1
kind: infrastructure_readiness_result
result_id: ready-southside-omni001-20260709T231000Z
subject_ref: southside-omni001
profile:
  id: omnigent-cloudpc-ready
  version: 1
status: ready
observed_at: 2026-07-09T23:10:00Z
valid_until: 2026-07-09T23:12:00Z
validator:
  actor_ref: southside-omni-readiness-validator
  trust_policy_ref: southside-readiness-validators-v1
checks:
  - id: windows365_connectivity
    status: pass
    evidence_ref: intune-evidence://device/XFACTORY-OMNI001/health/123
  - id: github_runner_online
    status: pass
    evidence_ref: github-evidence://opensoft/xFactory/runners/xFactory-omni001/456
  - id: omnigent_runtime
    status: pass
    evidence_ref: omni-evidence://southside-omni001/heartbeat/789
failed_checks: []
evidence_digest: sha256:<digest>
```

Allowed overall statuses are `ready`, `degraded`, `not_ready`, `unknown`, and
`maintenance`. A result is usable only before `valid_until`, under the named
trust policy, and when every mandatory profile check passes.

## Trust And Privilege

“Non-privileged validation” means the validator cannot change the target. It
may still require explicitly granted read-only access to Intune, GitHub, the
Omni heartbeat registry, or another status provider. Each check identifies the
trusted asserting system and evidence source.

## Failure And Cancellation Propagation

- OpsxFactory reports accepted, scheduled, implementing, validation-pending,
  completed-claim, blocked, declined, and cancelled projections.
- Client Hermes determines neutral request completion from readiness evidence,
  not from an Opsx “closed” status alone.
- Cancellation propagates to OpsxFactory and every active child job; each
  system acknowledges whether work stopped, already completed, or could not be
  cancelled.
- A changed target, requirement profile, or security boundary creates a
  superseding request unless the change policy explicitly permits an in-place
  amendment with a new approved digest.
- Loss of the Opsx connection leaves the neutral request blocked or awaiting
  response; it never implies success.
