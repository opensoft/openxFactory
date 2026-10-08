# Factory MCP Tool Catalog — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A domain publishes a closed tool catalog from its authoritative schemas without a universal domain payload.
Topics: factory-mcp, tool-catalog, tool-descriptors, contracts-versioning
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Validate a domain capability declaration and its schema references.

## Focus

What must an agent learn about each tool without forcing all domains into one argument schema?

## Proposed model and evidence

Proposed: every declared tool identifies its owning domain, input/output schema references, contract version, effects, binding rule, failure mapping, evidence policy and repetition policy. These declarations belong to a versioned conformance artifact. They are not invented required fields on the MCP wire descriptor.

## Interfaces and boundaries

Existing codex descriptors advertise exactly the engineering domain's patch-inspection tool and candidate-verification tool, and load the published schemas of the engineering domain's MCP contract package. New tools require a domain contract change. No adapter accepts arbitrary tool plugins or a generic execute-anything argument.

## Alternatives and tensions

Neutral declaration fields improve comparison; domain payloads preserve useful nouns. A mandatory generic submit_job tool would also impose asynchronous lifecycle on small synchronous checks.

## Open questions

A shared descriptor compiler is worth considering only after two domains demonstrate equivalent implementation needs.

## Relationships

See [the related synthesis](factory-mcp-synthesis-family-surface.md) and [the packet overview](factory-mcp-overview.md).
