# Existing codex MCP Conformance Mapping — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Use the two codex tools as compatibility witnesses without changing their closed schemas or transport behavior.
Topics: factory-mcp, codex-mapping, transport-neutral-mcp-tool-contract, mcp-transport-adapters, compatibility
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Record a source-pinned conformance mapping with explicit gaps for the shipped codex boundary.

## Focus

Which existing codex guarantees can inform a neutral profile without being mistaken for universal requirements?

## Proposed model and evidence

The engineering domain's patch-inspection tool checks binding and patch containment without runner/store use. The engineering domain's candidate-verification tool adds ordered host-owned checks and idempotent replay. Both retain authority_effect: none, eligible/blocked findings and sanitized evidence. The domain core is a single shared implementation; stdio and HTTP carry the same domain objects.

## Interfaces and boundaries

Repository/base digests, the patch, the worker result and check-profile details remain engineering vocabulary. No neutral profile adds fields to these tool requests or outcomes. Static documentation of a mapping is not domain adoption or certification of the deployed service.

## Alternatives and tensions

The existing schema-derived descriptors and lossless output mapping are strong reuse candidates. The code-specific runner and content-screening step cannot be extracted unchanged and called domain-neutral merely because another tool needs validation.

## Open questions

Scope-tuple derivation, revocation behavior and outward accepted-artifact provenance need explicit evidence or gap entries in any future adoption record.

## Relationships

See [the related synthesis](factory-mcp-synthesis-three-tool-fit.md) and [the packet overview](factory-mcp-overview.md).
