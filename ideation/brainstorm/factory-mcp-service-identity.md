# Factory MCP Service Identity — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Keep domain identity, installation scope, environment, and canonical endpoint identity separate.
Topics: factory-mcp, service-identity, factory-identity, neutral-job-envelope, identity
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Describe a service installation without treating its hostname as tenant authority.

## Focus

What does an endpoint such as mcp.codexfactory.opensoft.dev actually identify?

## Proposed model and evidence

Proposed: a deployment identifies its domain, installation, environment, canonical resource URI and accepted artifact. Authorized subject scope is resolved separately. One logical service per domain/environment may have several replicas or tenant partitions; hostname count does not determine tenant isolation.

## Interfaces and boundaries

The current codex plan names .opensoft.dev first and .opensoft.one at production. Brett's future .com names are an intended naming option, not a deployed fact or an amendment to the approved plan. URI migration must account for resource audience and client configuration.

## Alternatives and tensions

Stable domain identity supports endpoint moves, while credentials remain bound to the intended deployment resource. Sharing an issuer does not make credentials interchangeable between domain services.

## Open questions

Future .com ownership, production naming migration, and tenant-dedicated deployments need their own deployment decisions.

## Relationships

See [the related synthesis](factory-mcp-synthesis-family-surface.md) and [the packet overview](factory-mcp-overview.md).
