# Domain Worker Routing Model

`openWorkflow` is domain-neutral. This document defines the neutral control-plane and worker-routing concept for xFactory domains.

Engineering-specific worker deployment now lives in:

- `opensoft/opencodexFactory/docs/engineering-worker-model.md`

## Neutral Control/Execution Split

```text
Hermes / openWorkflow control plane
  -> governance, approvals, contracts, gates, routing, traceability, queues, dashboards, audit

Domain factory workers
  -> domain-specific execution under approved workflow contracts
```

## Domain Examples

```text
opencodexFactory workers
  run coding agents, repository checks, branch review, test execution, and PR-readiness tasks.

MedxFactory workers
  run clinical agents, specialist pods, Dream DB generation, patient simulation, reliability assessment, and clinician package drafting.
```

## Neutral Worker Requirements

All domain workers should:

```text
receive bounded job envelopes
respect consent/policy/scope constraints
write structured outputs
preserve traceability
avoid storing secrets or production runtime state
return status and evidence to the workflow rail
```

## openWorkflow Ownership

openWorkflow owns the routing and audit contract. Domain factory repos own the worker sizing, runtime tools, agent population, and domain-specific execution details.
