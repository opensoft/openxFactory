Status: ratified
Ratified: 2026-07-08 — record: the archive act, commit `d5ada44` "Reconcile domain-neutral spec ownership", which applied this change's spec delta into `openspec/specs/memory-gateway/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. That one commit both archived this change and created the promoted capability, so the archive act and the promotion are the same act here. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Customer Hermes needs a governed brain/memory/personality layer, but the stack
must not become coupled to any one memory product. Hermes should be able to use
GBrain, Honcho, AgentMemory, Postgres, graph stores, vector stores, or future
providers through xFactory rails that preserve consent, privacy, source
authority, traceability, promotion, and audit.

Domain Omnigent needs the same abstraction for external expert memory and
knowledge DBs. Expert workers should receive bounded expert context packets,
not unrestricted root-truth DB, vector index, source workspace, or case-pattern
store access. xFactory should own expert provider bindings, source-authority
rails, billing, migration, and audit while Domain Hermes owns reusable expert
truth and review policy.

## What Changes

- Introduce a product-neutral xFactory Memory Gateway architecture for the
  Customer Hermes memory boundary and the Omnigent expert memory/knowledge
  boundary.
- Define xFactory as the memory rail that mediates Hermes access to memory
  providers such as GBrain.
- Define provider profiles and adapters so memory products can map to canonical
  Customer Hermes objects without becoming the authority model.
- Define expert provider profiles and adapters so external knowledge DBs,
  source corpora, case stores, policy stores, tool memory, and evaluation
  memory can map to Omnigent expert context without becoming the authority
  model.
- Define read, write, context-packet, promotion, revocation, and audit rails for
  governed memory operations.
- Define customer memory fill and maintenance modes so customer interaction,
  structured input, external ingestion, third-party messages, telemetry,
  staff notes, non-Hermes agents, Omnigent outputs, workflow outcomes, and
  backfills are classified consistently across DomainxFactories.
- Define provider authentication, provider binding, short-lived grant, usage
  metering, budget, billing, migration, dual-write, shadow-read, cutover, and
  rollback rails as xFactory-owned concerns.
- Define a subject-safety rail for adult versus child/minor handling, including
  guardian/delegated authority, minor-safe redaction, interaction-mode limits,
  personalization limits, retention, and enhanced audit.
- Document how Hermes should route governed memory access through xFactory
  memory tools instead of directly calling GBrain for authoritative memory.
- Preserve AgentMemory as worker-local Omnigent memory and GBrain/Honcho as
  Hermes memory helpers behind xFactory governance.
- Preserve external expert memory and knowledge DBs as xFactory-governed
  providers used by Omnigent through bounded expert context packets.
- Group all requirements into conformance tiers (M0 core boundary through M4
  migration) so a minimally conformant gateway is a small, buildable target
  and governed reads/context packets can start before lifecycle and migration
  features are implemented.
- Define a threat model (over-broad packet requests, purpose gaming, confused
  deputy, gateway bypass, memory laundering, cross-tenant residue) with each
  abuse case mapped to the rail that defeats it.
- Require authenticated caller identity on every gateway call and structural
  credential custody: worker and Hermes-role identities never hold provider
  credentials; diagnostic access is operator-scoped, read-only, and
  non-production.
- Define a first-class, versioned consent profile contract (backed by Hermes
  operational state initially) as the first schema deliverable.
- Define explicit fail modes per operation class (writes fail closed; reads
  may degrade to cached redacted packets) and audited, rail-gated break-glass
  for domain-declared emergency workflows.
- Distinguish revocation (block future use) from erasure (provider-side
  content deletion) and require provider profiles to declare erasure
  capability per port.
- Leash context packets after issuance: TTL, purpose binding, and redaction
  inheritance for packet-derived worker-local memory.

## Capabilities

### New Capabilities

- `memory-gateway` (formerly `customer-memory-gateway`): Defines the
  product-neutral xFactory memory gateway, rails, provider profiles, provider
  bindings, adapter contracts, caller auth, credential custody, consent
  contract, fail modes, billing, erasure, migration, Hermes wiring, Omnigent
  expert knowledge wiring, and tiered conformance expectations for Customer
  Hermes memory and expert memory/knowledge providers. Renamed because half
  the capability governs Omnigent expert knowledge, not customer memory; the
  spec directory now lives at `specs/memory-gateway/`.

### Modified Capabilities

- None.

## Impact

- Adds an architecture proposal document under `docs/`.
- Adds OpenSpec capability requirements for the xFactory Memory Gateway.
- Extends the Customer Hermes memory model with implementation organization,
  Hermes-to-xFactory wiring, provider profile expectations, and GBrain mapping.
- Extends the gateway scope to include provider authentication, billing/metering,
  and memory-model migration so Hermes can keep using the same memory tools
  while xFactory changes provider routes underneath.
- Adds concrete adult/minor examples so DomainxFactories can treat protected
  subjects differently without encoding those rules in a memory provider.
- Adds a general fill and maintenance taxonomy that DomainxFactory repos map
  into patient, managed-system, project, ledger, campaign, or other local
  customer-layer terms.
- Adds Omnigent expert memory and knowledge DB examples so DomainxFactories can
  govern expert DB access, source authority, migration, and billing without
  binding Omnigent workers to a specific product.
- Does not mandate GBrain, AgentMemory, Honcho, or any other product as the
  canonical memory or expert knowledge model.
- Future implementation will affect Hermes memory tooling, xFactory gateway
  schemas, provider bindings, provider adapters, usage ledgers, migration
  manifests, audit events, Omnigent expert context wiring, and domain stack
  configuration.
