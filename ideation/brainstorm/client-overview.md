# Client Hermes Layer Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The Client Hermes layer is proposed as a tenant-specific authority,
policy, memory, integration, and assurance overlay produced from a neutral
scaffold through governed human tuning.
Topics: client, client-hermes, company-policy, layer-content-seeding
Repository context: openxFactory neutral client/company-policy layer
Captured: 2026-07-28

## Possible feats

- **Client Hermes scaffold and tuning kit** — neutral schema, roster,
  question set, validators, evidence-adapter bindings, and change preview.

## Motivation

Domain policy cannot encode each company's risk posture, integrations,
approval envelope, house roles, and private memory boundaries. Free-form
tenant prompts are difficult to review, reproduce, or safely retune.

## Goals

- Separate neutral client structure from domain defaults and tenant choices.
- Give company-level decisions named authorities and escalation paths.
- Materialize bounded policy and memory decisions through a wizard.
- Govern source ingestion through tenant consent and assurance.
- Preserve stricter-only inheritance and explicit change history.

## Non-goals

- The client layer does not own domain truth or project acceptance.
- It does not store raw credentials in layer content.
- It does not let a wizard invent policy beyond human answers.
- It does not make Hermes legal counsel a substitute for human counsel.

## What the system delivers

For each tenant, the system can produce a versioned Client Hermes overlay:
role objects, policy overrides, memory boundaries, source inventory,
credential references, integration constraints, risk escalation, and an
auto-clearance envelope.

## System model

```text
neutral client scaffold + domain specialization
  → bounded policy wizard + human answers
  → validation and assurance review
  → pinned client overlay
  → seeding into authority, memory, and integration surfaces
  → observed dispositions feed later retuning
```

## Cluster map

- [Client Authority and Policy Tuning](client-synthesis-authority-and-policy.md)
  — joins structure, roster, content, elicitation, and assurance.
- [Client Knowledge Ingestion and Assurance](client-synthesis-ingestion-and-assurance.md)
  — joins source adapters to tenant memory and risk boundaries.

## How it fits

The client layer sits between reusable Domain Hermes content and one
Project/Subject Hermes instance. The Hermes runtime seeds validated content;
the memory gateway enforces consent and tenant isolation; project authorities
retain acceptance and subject-specific decisions.

## Key decisions and open questions

The core choice is to store the tenant's governed delta rather than a generic
policy textbook. Open decisions include role concurrence, retuning consent,
exception handling, and the boundary between company-wide and project-private
memory.

## Document map

### Syntheses

- [Client Authority and Policy Tuning](client-synthesis-authority-and-policy.md)
- [Client Knowledge Ingestion and Assurance](client-synthesis-ingestion-and-assurance.md)

### Atomic explorations

- [Client Layer Scaffold](client-layer-scaffold.md)
- [Client Layer Roster](client-layer-roster-draft.md)
- [Client Layer Content](client-layer-content-draft.md)
- [Client Policy Wizard](client-policy-wizard.md)
- [Client Risk and Assurance Model](client-risk-and-assurance-model.md)
- [Client Ingestion-Adapter Contract](client-ingestion-adapter-contract.md)
