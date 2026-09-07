# Ops DNS Pre-change MCP Check — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Evaluate proposed DNS record changes against trusted observations using OpsxFactory's existing planning rules.
Topics: factory-mcp, dns-check, dns-zone-administration, observation-freshness, mcp
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Add ops_dns_check_change as a bounded advisory domain capability.

## Focus

What does test a DNS change mean for the first Ops MCP tool?

## Proposed model and evidence

Selected proposal: pre-change planning evaluation. Caller supplies schema/tool/request/correlation IDs, binding_ref, zone_ref and a bounded change_set. Trusted configuration resolves the zone, reader, policy and registry; the reader supplies observed state and delegation. Ops planning determines eligible or blocked; unavailable, malformed or stale observations produce typed errors.

## Interfaces and boundaries

This is not post-change propagation verification, an apply action, a DNS mutation grant, or a live endpoint. Reuse supported record types and create/update/delete_record_set vocabulary from dns_zone_administration. Preserve its registry, reach and refusal precedence rather than adding a parallel policy engine.

## Alternatives and tensions

The existing core is provider-silent, while the live ceremony is elsewhere. A synthetic reader proves the boundary, not live readiness. The first implementation should deliver the callable contract and synthetic tests; hosted transport and an operational reader remain separately governed.

## Open questions

Later reader integration must prove provenance and bounded cancellation. A public resolver response alone may not satisfy a provider-read-back requirement.

## Relationships

See [the related synthesis](factory-mcp-synthesis-three-tool-fit.md) and [the packet overview](factory-mcp-overview.md).
