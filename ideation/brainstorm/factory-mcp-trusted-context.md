# Factory MCP Trusted Context — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Treat caller references as requests for scope while trusted bindings determine the scope actually available.
Topics: factory-mcp, trusted-context, credential-contracts, client-identity-roster, neutral-job-envelope
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Map a verified caller and binding to exact permitted subject scope.

## Focus

How can a caller name a repository or zone without being allowed to invent its policy?

## Proposed model and evidence

Proposed: the caller can supply a binding or subject reference; the trusted boundary resolves it under verified identity and checks permitted operations before external work. Policies, credentials, observed state and principal namespaces are not authoritative caller fields. Neutral installation/stack/layer references reuse the existing Hermes vocabulary.

## Interfaces and boundaries

Existing codex EvaluationContext is closed and host-derived. Its relation to the complete neutral scope tuple is a mapping gap, not an already shipped field set. A conformance mapping must describe the existing boundary honestly and retain unresolved mappings as explicit gaps.

## Alternatives and tensions

A startup-frozen binding is simple but does not implement live revocation. Sharing identity structure cannot silently claim that existing deployments perform runtime revocation checks.

## Open questions

The exact roster/register integration and revocation freshness remain host/runtime design questions; the first profile records their declared status.

## Relationships

See [the related synthesis](factory-mcp-synthesis-evaluation-safety.md) and [the packet overview](factory-mcp-overview.md).
