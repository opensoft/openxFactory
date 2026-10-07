# Factory MCP Implementation Boundaries — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Realize a neutral declaration validator and an Ops DNS callable contract before extracting transport code or deploying another service.
Topics: factory-mcp, implementation-boundaries, release-realization, contracts-versioning, mcp
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Prove conformance through schemas, mappings and deterministic fixtures before runtime extraction.

## Focus

What can the first implementation honestly deliver?

## Proposed model and evidence

Proposed neutral slice: conformance schema, semantic validator, neutral fixtures, mapping guidance and explicit codex compatibility observations. Proposed Ops slice: domain request/result/error schemas, injected observation boundary, DNS evaluator, tool descriptor/result mapping, tests and runbook. Domain code stays outside openxFactory.

## Interfaces and boundaries

No shared transport package, medical tool, central router, listener, live reader, hostname publication, token minting, release cut, acceptance or pin advance is included. Each future consumer adoption follows its own reviewed version/pin change.

## Alternatives and tensions

A schema-valid declaration proves structure, not runtime safety. Conformance claims need behavioral evidence and cannot describe an unimplemented endpoint as ready. Domain-independent synthetic fixtures exercise the neutral validator without shipping DNS behavior in the neutral repository.

## Open questions

The repository constitutions require ratified OpenSpec authority before code. These documents preserve design intent; exact proposals carry the approval boundary and later Speckit features own implementation tasks.

## Relationships

See [the related synthesis](factory-mcp-synthesis-three-tool-fit.md) and [the packet overview](factory-mcp-overview.md).
