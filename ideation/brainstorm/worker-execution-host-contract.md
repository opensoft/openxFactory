# Governed Worker Host Contract — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A worker host should advertise digest-pinned benches, supported
execution features, health, identity, and resource bounds without receiving
unscoped tenant credentials or decision authority.
Topics: worker-execution, worker-host, tech-benches, enrollment
Repository context: openxFactory neutral worker execution and enrollment exploration
Captured: 2026-07-28

## Possible feats

- **Worker-host inventory contract** — report host identity, enrollment state,
  bench digests, architectures, capacities, health, and policy compatibility.
- **Bench preparation action** — pre-pull and verify an approved toolchain
  without accepting a job or tenant secret.

## Focus

This document isolates the machine boundary that makes a workstation, Cloud
PC, or other host eligible to run governed workers.

## Proposed model

A host enrolls through a broker and receives a scoped host identity. It
periodically publishes:

- host and installation identity;
- supported isolation and credential-broker features;
- verified bench images and toolchain manifests;
- CPU, memory, accelerator, disk, and concurrency capacity;
- heartbeat, draining, maintenance, and quarantine state;
- policy and contract versions it can enforce.

The inventory is evidence for scheduling, not permission to fetch project
content. Job-specific leases arrive only after routing and authorization.

## Interfaces and boundaries

The host contract extends
[Tech-Stack Benches](tech-stack-benches.md) and provides a realization target
for [Worker Enrollment Broker](../../openspec/changes/add-worker-enrollment-broker/proposal.md).
It does not choose jobs or approve outputs.

## Alternatives and tensions

- Long-lived hosts improve cache efficiency but expand persistent attack
  surface.
- Ephemeral hosts improve isolation at provisioning and cold-start cost.
- Rich inventory improves routing while exposing operational metadata.

## Open questions

- Which attestation level is needed for each job class?
- Can personal workstations host tenant jobs?
- How are stale or compromised bench digests quarantined?

## Relationships

The [Governed Job Lifecycle](worker-execution-governed-job-lifecycle.md)
uses an eligible host for one bounded execution.
