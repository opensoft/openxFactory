# Hermes Knowledge-Base Architecture: federate-and-structure inside the memory gateway — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Applies the Cerebras "How we built our knowledge base" pattern to how
each Hermes layer builds and queries its knowledge base — most usefully the
client layer. The core fit: xFactory's ratified customer memory gateway already
embodies Cerebras' load-bearing principle (keep information where it lives,
federate through one retrieval layer), and Cerebras supplies the concrete
mechanics the gateway leaves open — a unified evidence-row schema, per-source
ingestion adapters, structure-before-embed, hybrid retrieval with reciprocal-
rank-fusion + age decay, a planner→executor→synthesizer query pipeline, and
low-level search *primitives* rather than a monolithic answer endpoint. The
xFactory delta over Cerebras (internal, permissive) is the governance wrap:
consent, tenant isolation, and source-authority/provenance. Especially useful
for the client layer, whose knowledge lives across the operating org's real,
messy systems. Parent: `client-layer-scaffold.md`; consumes the ratified memory
gateway.
Topics: knowledge-base, memory-gateway, retrieval, embeddings, ingestion,
evidence-rows, planner-executor-synthesizer, hybrid-search, tenant-isolation,
consent, source-authority, client-hermes, cerebras
Repository context: openxFactory (memory gateway + client scaffold; applies to all layers)
Captured: 2026-07-21
Updated: 2026-07-22 (row-kernel / adapter-authority / rank-params decisions; cost hook; exit path)

## Decided (2026-07-22)

- **Evidence row = new kernel; context-packets compose from it.** Rows are the
  internal storage/ingest shape; the ratified `context-packet` stays the
  governed *output* form retrieval returns. No amendment to a ratified
  contract; clean storage/output separation.
- **Adapter authoring: steward proposes, ICS accepts, CSC clears surface.**
  `source_inventory_agent` proposes an adapter from discovery; the
  Integrations & Credentials Steward accepts it; any new external call or
  credential surface additionally needs CSC clearance (already required by
  `integration-boundaries`). The propose/accept pattern, applied to sources.
- **Ranking: domain-default recipe, client-tunable values in ranges.** The
  mechanics (hybrid + RRF + age decay) are neutral/domain; the parameter
  *values* (recency weight per source class) are client-tunable within
  declared ranges — the facts rule applied to ranking.
- **Planner is tiered (cost hook).** Cheap governed primitives are the
  default query path; the full planner→executor→synthesizer pass is reserved
  for the deliberative path (council-tier triggers) — mirroring
  `council_small`/`council_large`. Every retrieval, and especially a planner
  pass, is a **spend event** that clocks in
  (`cost-accountability-and-efficiency-model.md`); FAO's tracking granularity
  covers query spend like any other.

Reference: Cerebras, "How we built our knowledge base"
(https://www.cerebras.ai/blog/how-we-built-our-knowledge-base).

## Possible feats

- **Unified evidence-row schema** across all layer sources (extends the gateway's
  context-packet).
- **Per-source ingestion adapters** (the Cerebras plugin pattern) governed by the
  gateway's provider-binding.
- **Structure-before-embed** ingestion for the client's noisy sources.
- **Governed retrieval primitives** (search_* over context-packets) instead of a
  monolithic answer endpoint — detailed in `hermes-retrieval-primitives-contract.md`.

## The fit: the gateway is the wrapper, Cerebras is the mechanism

The ratified customer memory gateway (`customer-memory-gateway-architecture.md`)
says memory lives in external providers reached through ports (Identity, Consent,
MemoryItem, Promotion) — i.e. *federate, don't centralize*, which is exactly
Cerebras' first principle. But the gateway is deliberately abstract about the
*retrieval and ingestion mechanics*. Cerebras fills that in. So: adopt the
Cerebras mechanics **inside** the gateway's governance rails.

## Cerebras techniques → xFactory mapping

| Cerebras | xFactory home |
| --- | --- |
| Keep info where it lives; one retrieval layer over many sources | the memory gateway (ratified) — already this |
| Unified embeddings table (content + vector + metadata) | a shared **evidence-row** schema; the gateway's `context-packet` is its governed form |
| Plugin scripts per source emit rows to the shared schema | **per-source ingestion adapters**, bound via the gateway's `provider-binding` / `provider-profile` |
| Structure-before-embed (Slack thread → question/summary/resolution) | the client `workflow_definition_agent` + `client_memory_steward` decide what becomes memory |
| Hybrid search (full-text + vector + IDF + age decay) → Reciprocal Rank Fusion | the gateway's retrieval rail — a concrete ranking recipe |
| Planner → Executor → Synthesizer per query | a persona's query: an LLM plans which sources matter, tools run in parallel, results synthesize with citations (the MoA "advises" side) |
| Low-level primitives (`search_slack`, `search_code`, `who_knows`) via MCP, not an answer endpoint | expose **governed retrieval primitives** returning context-packets; the Hermes persona decides (mantra: MoA advises, Hermes decides) |
| "Project" scopes related channels/repos/docs | the **layer + tenant** scoping is native — a client tenant scopes to its subjects/projects |

## The xFactory delta: govern what Cerebras left open

Cerebras is internal and permissive; xFactory is multi-tenant and governed, so
three rails wrap the mechanics — and they are the reason not to just bolt on a
generic RAG stack:

- **Consent.** Every ingest and every retrieval passes the gateway's
  `consent-profile`; a source can be revoked/erased (`revocation`, `erasure`).
- **Tenant isolation.** Evidence rows are tenant-scoped; one client never
  retrieves another's (the client memory-boundaries invariant). Cerebras' single
  internal table becomes a per-tenant-partitioned one.
- **Source authority / provenance.** Every evidence row carries a
  `source_authority` tag using the gateway's **ratified** `authority_levels`
  vocabulary (`self_reported | observed | source_backed | reviewed |
  domain_authoritative | below_threshold`,
  `contracts/memory-gateway/vocabularies.yaml`) — not an invented one — and the
  expert rails already enforce a minimum-authority floor
  (`source_authority_below_threshold` is a ratified denial). Synthesis cites,
  and low-authority evidence cannot silently drive a decision.

## Client layer — the star use case

The client (operating org) is where federation earns its keep: its knowledge
lives across Slack/chat, wiki, tickets, CRM, calendars, and repos — messy, real,
and already-somewhere. The client scaffold *already anticipates this*:

- **Ingestion adapters** = the scaffold's `source_inventory_agent` +
  `installation_discovery` workflow: onboard each org system as an adapter that
  emits governed evidence rows (Cerebras' plugin pattern, consent-bound).
- **Structure-before-embed** = `workflow_definition_agent` turning source
  evidence into structured `workflow_definition_packet`s, and
  `client_memory_steward` deciding what becomes `client_private_memory`,
  `customer_relationship_memory`, or a `domain_learning_candidate`. The client's
  raw chatter is summarized into structured records before embedding — exactly
  Cerebras' "don't embed raw Slack."
- **Evidence surface** = the scaffold's `evidence_claim_table` and
  `current_state_evidence` bucket are the evidence-row store made visible.
- **Retrieval** = hybrid + age decay matters doubly here: operational truth is
  recent (today's roster, this week's tickets), so age decay is not optional.
- **Scoping** = tenant-scoped by client, project-scoped by subject — noise from
  other tenants/projects is structurally excluded.

So the client-layer KB is: federate over the org's real systems via
consent-bound adapters → structure-before-embed → tenant/project-scoped hybrid
retrieval → governed context-packets the house team decides on. The adapter
side is specified in `client-ingestion-adapter-contract.md`.

## Domain & subject layers (briefer)

- **Domain** — its KB is more *curated* (authored practices, policies, the
  practice catalog) plus the cross-client `domain_learning` promoted through the
  gateway gate. Cerebras' structure-before-embed still applies to the recurring-
  findings memory; source-authority is central (the domain cites its own specs).
- **Subject** — narrowest scope (one subject) and the most consent-sensitive when
  the subject is a person (a Medx patient): retrieval must honor the patient's
  consent profile per query, not just at ingest.

## Exit path (concrete contracts this becomes)

1. **openxFactory memory-gateway contract extension** — the evidence-row
   kernel schema (new, composes into the ratified `context-packet`) + the
   ranking-recipe defaults with per-parameter tunable ranges.
2. **`client-ingestion-adapter-contract.md`** (sibling brainstorm) carries the
   adapter shape → an openxFactory contract; adapter instances are client
   config accepted per the §Decided authority chain.
3. **`hermes-retrieval-primitives-contract.md`** (sibling brainstorm) carries
   the governed primitives; the tiered-planner rule lands there.

## Open questions

- ~~**Evidence-row vs. context-packet**~~ — DECIDED 2026-07-22: new kernel,
  packets compose (§Decided).
- ~~**Adapter authoring authority**~~ — DECIDED 2026-07-22: steward proposes,
  ICS accepts, CSC clears new surface (§Decided).
- ~~**RRF/age-decay parameters**~~ — DECIDED 2026-07-22: domain-default
  recipe, client-tunable values in declared ranges (§Decided).
- ~~**Planner cost**~~ — DECIDED 2026-07-22: tiered — primitives by default,
  planner on the deliberative path only; all retrieval clocks in (§Decided).
- **Structure-before-embed ownership** — confirmed shape: a Plane-2 worker
  summarizes, a Plane-1 authority accepts the promotion (the propose/accept
  pattern) — still open: which worker per source class, drafted when the
  adapter contract lands.
- **Per-tenant partitioning mechanics** — Cerebras' single table becomes
  per-tenant-partitioned; physical partitioning vs. row-level scoping is a
  gateway-provider decision to record.
