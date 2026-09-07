# Factory MCP Results and Evidence — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Preserve domain results and distinguish negative findings from failure to evaluate, with bounded provenance and disclosure.
Topics: factory-mcp, results-evidence, evidence-observability, privacy, contracts-versioning
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Define lossless result mappings and evidence disclosures for domain tools.

## Focus

How can an agent interpret outcomes consistently without erasing domain meaning or leaking private data?

## Proposed model and evidence

Proposed: a completed evaluation may have a negative domain finding; inability to evaluate is a declared failure. Each domain maps its statuses and codes explicitly. Evidence identifies evaluated input, trusted context and observation time; accepted artifact provenance may be associated through protected host records rather than inserted into an existing digested result.

## Interfaces and boundaries

The codex adapter places the domain object verbatim in structuredContent and classifies DomainError as an execution error. Its suppression of raw paths is domain-specific. Ops DNS findings can identify bounded authorized record references; raw provider payloads, credentials and raw exceptions are not returned.

## Alternatives and tensions

Useful DNS details and medical confidentiality require distinct output policies. Hashes provide integrity references but do not make low-entropy names confidential or grant access to a stored evidence record.

## Open questions

Audit sink implementation, retention and access policy remain host-owned; an opaque event ID is not proof that a resolving sink exists.

## Relationships

See [the related synthesis](factory-mcp-synthesis-evaluation-safety.md) and [the packet overview](factory-mcp-overview.md).
