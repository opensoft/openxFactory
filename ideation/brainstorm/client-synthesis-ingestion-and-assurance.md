# Synthesis: Client Knowledge Ingestion and Assurance — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Client content boundaries, governed source adapters, and the
assurance bench can admit organizational evidence without turning source
access into unrestricted memory.
Topics: client, client-hermes, ingestion-adapter, evidence-rows, risk-and-assurance, synthesis
Repository context: openxFactory Client Hermes evidence boundary
Captured: 2026-07-28

## Possible feats

- **Client source-admission review** — bind a source inventory entry,
  credential reference, consent rule, adapter version, and assurance
  disposition before ingestion begins.

## Members and their joints

Atomic members:
[Client Ingestion-Adapter Contract](client-ingestion-adapter-contract.md),
[Client Layer Content](client-layer-content-draft.md),
and [Client Risk and Assurance Model](client-risk-and-assurance-model.md).

### Stored boundaries drive adapter behavior

Client content declares which source classes, memory buckets, retention
policies, and promotion boundaries apply. The adapter translates those
decisions into tenant-scoped evidence rows with source authority and
provenance.

### Assurance governs exceptional risk

The assurance bench reviews high-risk sources, licenses, personal data,
reputation exposure, and product-liability implications. It may park or
escalate ingestion but does not rewrite source records.

## Emergent behavior

The organization can federate knowledge from real systems while each row
retains enough authority, consent, and provenance information for governed
retrieval.

## Tensions to hold

- Source breadth improves recall but expands consent, retention, and leakage
  risk.
- Structure-before-embed improves auditability at higher ingestion cost.
- Client policy must distinguish authoritative records from conversational
  evidence without discarding useful context.

## Recombination opportunities

This cluster feeds the
[Hermes memory and retrieval packet](memory-retrieval-overview.md).

## Open questions

- Which source classes need recurring assurance review?
- How are deletions and corrections propagated into derived indexes?
- Can one adapter serve several tenants without sharing mutable state?
