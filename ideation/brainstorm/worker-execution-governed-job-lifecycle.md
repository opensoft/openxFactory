# Governed Worker Job Lifecycle — Brainstorm

Status: brainstorm
Kind: process
Summary: A worker job should move through admit, lease, prepare, run, observe,
close, and revoke states with pinned task, bench, identity, evidence, cost,
and external-enforcement boundaries.
Topics: worker-execution, job-lifecycle, omnigent-lane, external-enforcement
Repository context: openxFactory neutral Omnigent execution exploration
Captured: 2026-07-28

## Possible feats

- **Governed job state machine** — admit, route, lease, prepare, run, collect,
  evaluate, hand off, close, cancel, and revoke one job.
- **Execution evidence bundle** — pin task envelope, host, bench, worker,
  tool calls, artifacts, spend, verdicts, and external acceptance.

## Focus

This document isolates one job after a task has been proposed. It defines the
execution lifecycle without assigning Hermes decision or repository merge
authority to the worker.

## Proposed model

The lifecycle is:

1. validate the task envelope and required authority;
2. choose an eligible worker class, host, and bench;
3. issue short-lived content and tool leases;
4. prepare a clean execution scope;
5. run with observable resource and tool boundaries;
6. collect artifacts, evidence, spend, and worker status;
7. hand the result to external evaluation and enforcement;
8. close, revoke leases, and retain the governed record.

Cancellation and timeout remain terminal evidence, not missing records.

## Interfaces and boundaries

The lifecycle consumes a qualified host from the
[Worker Host Contract](worker-execution-host-contract.md) and sequencing ideas
from [Omnigent Lane Activation](omnigent-lane-activation-path.md). It emits
artifacts for Hermes, review councils, CI, humans, or other external
authorities.

## Alternatives and tensions

- A universal job state machine aids portability but domain jobs need
  specialized evidence and enforcement.
- Streaming tool access improves responsiveness while short-lived leases and
  isolation become harder.
- Self-hosting proves maturity but creates circular recovery risks.

## Open questions

- Which lifecycle states belong in the neutral contract?
- How are retries distinguished from new jobs for accounting?
- What evidence is mandatory when a worker exits unexpectedly?

## Relationships

Host and job behavior combine in the
[governed execution-lane synthesis](worker-execution-synthesis-governed-lane.md).
