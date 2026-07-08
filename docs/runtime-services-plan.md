# Runtime Services Plan

Status: draft
Kind: plan
Repository context: openxFactory
Purpose: define the minimum runtime service set needed to move xFactory from
contracts and domain repos to a runnable stack.

## Goal

Provide a control plane and execution plane that can accept approved intent,
issue bounded job envelopes, route work to Omnigent workers, enforce Hermes
approvals, resolve credential references through a broker, write audit records,
and produce dry-run evidence before any live action.

## Service Topology

Required services for the first runnable stack:

1. Hermes API
   - owns approval records, policy decisions, memory references, and audit views
   - exposes approval, revocation, and decision-record endpoints

2. openxFactory control API
   - owns workflow state, gates, routing, job envelopes, readiness state, and traceability
   - validates domain stack contracts and runtime binding manifests

3. Job scheduler and queue
   - persists workflow jobs and retry state
   - supports dry-run jobs before live execution

4. Omnigent worker gateway
   - launches bounded worker sessions
   - injects only scoped job envelopes and runtime grants
   - blocks raw secret access

5. Credential broker
   - resolves secret references against an approved provider
   - issues short-lived runtime capability grants
   - supports revoke and audit

6. Adapter registry and adapter runner
   - loads declared adapter contracts
   - runs read-only health checks
   - enforces adapter capability limits and dry-run posture

7. Operational Postgres
   - stores jobs, runs, events, approvals, worker status, artifacts, and traceability records
   - uses the canonical schema under `contracts/schemas/hermes-operational-postgres.sql`

8. Artifact store
   - stores packets, validation reports, approval packets, dry-run evidence, and support bundles
   - never stores raw credentials

9. Audit/event stream
   - captures job events, credential-grant events, adapter health results, approvals, revocations, and dry-run outcomes

10. Readiness service
   - computes L0-L8 readiness from schema, service, binding, grant, adapter, dry-run, approval, and live gates
   - emits gap reports with exact next actions

## MVP Sequence

### Phase 1: State And Contracts

- Implement Postgres migrations for job/run/event/approval/worker/artifact tables.
- Add manifest validation for domain stack, runtime binding, adapters, and credentials.
- Add readiness classifier for L0 schema-valid through L2 services-start.

Exit criteria:

- `openx validate-runtime --manifest <file>` can load contracts and return a structured L0-L2 report.

### Phase 2: Control Plane

- Implement openxFactory control API.
- Implement job envelope creation.
- Persist job runs and events.
- Add local dry-run job creation without external adapters.

Exit criteria:

- A dry-run job can be created, recorded, moved through states, and audited.

### Phase 3: Hermes And Approval Enforcement

- Implement Hermes approval API or adapter to existing Hermes runtime.
- Enforce approval gates before privileged workflows.
- Implement emergency stop and revocation endpoints.

Exit criteria:

- A privileged workflow remains blocked until approval is recorded and revocable.

### Phase 4: Credential Broker

- Support local-dev vault references first.
- Add provider interface for Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, and enterprise vaults.
- Issue short-lived runtime capability grants.
- Write grant and revocation audit events.

Exit criteria:

- A test grant can be issued and revoked without printing or persisting raw secret material.

### Phase 5: Adapter Runner

- Load adapter contracts from a domain repo.
- Run read-only health checks.
- Enforce allowed workflow/action scope.
- Return adapter health evidence to readiness.

Exit criteria:

- At least one Ledgerx read-only adapter health check can pass in dry-run mode.

### Phase 6: Worker Gateway

- Launch bounded Omnigent worker sessions.
- Pass job envelope, artifact output path, and runtime grant references.
- Capture worker events and artifacts.

Exit criteria:

- A Ledgerx `bank_feed_review` dry-run produces an audit trail and evidence packet.

### Phase 7: Readiness And Support Bundle

- Compute L0-L8 readiness.
- Emit blocked gap reports.
- Generate redacted support bundle.

Exit criteria:

- The stack can distinguish `runtime_ready`, `workflow_ready`, and `live_ready` without operator interpretation.

## Non-Goals For First Runtime

- No live filing submission.
- No money movement.
- No long-lived worker credentials.
- No raw credential storage in repos, workspaces, logs, artifacts, or support bundles.
- No production multi-region HA until the single-node runtime proves the contract.
