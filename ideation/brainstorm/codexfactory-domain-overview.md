# codexFactory Domain Hermes Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: codexFactory Domain Hermes is proposed as the reusable
software-engineering decision layer containing personas, deliberation,
policy deltas, governed memory, and practice-adoption knowledge.
Topics: codexfactory-domain, codexfactory, domain-hermes, three-layer-hermes-runtime
Repository context: openxFactory neutral/domain boundary; codexFactory realizes content
Captured: 2026-07-28

## Possible feats

- **Seedable codexFactory Domain Hermes bundle** — versioned personas,
  councils, policy, memory rules, practice catalog, and validation evidence.

## Motivation

Every codexFactory installation needs consistent software-engineering
authority and practice knowledge, but that reusable domain content should not
be rebuilt per client or mixed into worker images.

## Goals

- Define domain deciders and their owned decisions.
- Keep worker execution separate from Plane-1 authority.
- Store only consistency-critical policy and governed learning.
- Make deliberation profiles and council boundaries explicit.
- Publish content that can be pinned and seeded across installations.

## Non-goals

- Domain Hermes does not own client policy or project acceptance.
- Persona prose does not override enforceable rules.
- The domain layer does not receive raw tenant-private memory.
- This packet does not ratify the drafted roster.

## What the system delivers

A codexFactory domain bundle can provide role objects, council definitions,
deliberation profiles, policy positions, memory boundaries, and a practice
catalog to every installation while keeping client and project overlays
separate.

## System model

```text
codexFactory-authored domain bundle
  → digest pin and validation
  → Domain Hermes authority and memory records
  → directs governed workers and issues decisions
  → outcomes enter bounded learning and practice suggestions
```

## Cluster map

- [Domain Authority and Deliberation](codexfactory-domain-synthesis-authority-and-deliberation.md)
  — joins role ownership, councils, and agent-mix profiles.
- [Domain Policy and Memory](codexfactory-domain-synthesis-policy-and-memory.md)
  — joins stored policy, memory boundaries, and practice knowledge.

## How it fits

openxFactory owns neutral contracts; codexFactory authors the
software-engineering overlay; Hermes Install seeds it; Omnigent runs Plane-2
workers; Client and Project Hermes add narrower authority and policy.

## Key decisions and open questions

The packet favors explicit role and policy artifacts over a monolithic domain
prompt. The drafted roster, council verdict rules, memory-promotion threshold,
and domain bundle release process remain open until governed.

## Document map

### Syntheses

- [Domain Authority and Deliberation](codexfactory-domain-synthesis-authority-and-deliberation.md)
- [Domain Policy and Memory](codexfactory-domain-synthesis-policy-and-memory.md)

### Atomic explorations

- [Domain Hermes Content](codexfactory-domain-hermes-content.md)
- [Domain Roster](codexfactory-domain-roster-draft.md)
- [Domain Deliberation](codexfactory-domain-deliberation.md)
- [Domain Policy Model](codexfactory-domain-policy-model.md)
- [Domain Memory and Practices](codexfactory-domain-memory-and-practices.md)
