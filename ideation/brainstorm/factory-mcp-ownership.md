# Factory MCP Ownership — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Share neutral MCP conformance rules while each domain owns its tool semantics and OpsxFactory governs hosting.
Topics: factory-mcp, ownership, domain-boundaries, hosted-domain-service-governance
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Define separate conformance, domain-tool, and hosting responsibilities.

## Focus

Which repository owns a capability when every factory uses MCP and OpsxFactory operates the deployments?

## Proposed model and evidence

Proposed: openxFactory owns the neutral conformance profile; codexFactory, OpsxFactory and MedxFactory own their respective tool contracts, schemas, implementations and tests. OpsxFactory separately governs hosting plans, artifact acceptance, ingress and deployment. A common implementation library is a later extraction decision.

## Interfaces and boundaries

Existing evidence: OpsxFactory's host-codexfactory-mcp-contract-service design D2 leaves the codex package with its author and the deployment with the host governor. Hosting a medical or software service conveys no authority over its tool meanings.

## Alternatives and tensions

One universal server centralizes discovery but also couples releases and authority. Separate domain services preserve those boundaries without requiring separate clusters.

## Open questions

Whether an independently useful neutral discovery service is needed remains open; shared conventions alone do not require a listener.

## Relationships

See [the related synthesis](factory-mcp-synthesis-family-surface.md) and [the packet overview](factory-mcp-overview.md).
