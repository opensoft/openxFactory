# Synthesis: Domain Services and Shared Conformance — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Separate domain capability ownership from shared conformance and operational hosting.
Topics: factory-mcp, ownership, service-identity, tool-catalog, synthesis
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Let an agent discover several independently owned domain catalogs using one conformance vocabulary.

## Members and their joints

Atomic members: [ownership](factory-mcp-ownership.md), [service identity](factory-mcp-service-identity.md), and [tool catalog](factory-mcp-tool-catalog.md).

### Ownership determines catalog meaning

A service's domain owns its tools, schemas, policy meanings and release evidence.
openxFactory would specify what a declaration must explain, without accepting a
universal payload. OpsxFactory operates deployments under its hosting governance;
operating a codexFactory deployment does not transfer its engineering authority.

### Installation identity connects a catalog to a deployment

The declaration describes a domain and a versioned catalog. A host associates it
with an installation, environment, canonical resource URI and accepted artifact.
Authorized tenant and subject scope still comes from trusted bindings.
A shared issuer or a familiar hostname cannot substitute for that binding.

### Separate catalogs permit separate adoption

Agents may connect to multiple domain services. A software change that edits DNS
can need both engineering and infrastructure evidence. A neutral discovery
service is optional future work; common conventions alone need no listener.
Separate services need not imply separate clusters or one deployment per tenant.

## Emergent behavior

The family can offer consistent discovery and interpretation while retaining
independent domain releases, output policies and hosting decisions.

## Tensions to hold

A central router could simplify discovery but creates an additional authority and
release boundary. Future public .com names are desired naming options, not
changes to the approved codex hosting plan.

## Recombination opportunities

Combine this cluster with [evaluation safety](factory-mcp-synthesis-evaluation-safety.md)
to explain what a discovered tool may actually access, and with the
[three-tool comparison](factory-mcp-synthesis-three-tool-fit.md) to test reuse.

## Open questions

Whether neutral discovery has useful tools of its own, how tenant partitions are
deployed, and when resource URI migrations happen remain hosting decisions.

See the [overview](factory-mcp-overview.md).
