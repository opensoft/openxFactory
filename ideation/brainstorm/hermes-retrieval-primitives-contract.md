# Hermes Retrieval Primitives: governed search over evidence, planner→executor→synthesizer — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Details the read side of the knowledge base — the governed retrieval
primitives and query pipeline, the complement to the ingestion adapters.
Following Cerebras, the system exposes low-level search *primitives*
(`search`, `search_<source>`, `who_knows`, `recall`) that return governed
**context-packets**, not a monolithic answer endpoint; a planner→executor→
synthesizer pipeline orchestrates them, and the synthesizer only *advises* —
the Hermes persona decides (the MoA mantra). Every stage enforces the gateway
rails: consent checked **per query** (not just at ingest), tenant isolation,
source-ACL → visibility, source-authority weighting with a floor, and a
usage-event audit. Ranking is the Cerebras recipe: hybrid (full-text + vector +
IDF + age decay) fused by reciprocal rank fusion. Primitives are exposed as
governed MCP tools so orchestrators compose them. Parent:
`hermes-knowledge-base-architecture.md`; ingestion side:
`client-ingestion-adapter-contract.md`.
Topics: retrieval, search-primitives, context-packet, planner-executor-synthesizer,
hybrid-search, rrf, age-decay, source-authority, consent, tenant-isolation,
who-knows, mcp, memory-gateway
Repository context: openxFactory (neutral retrieval contract; gateway-adjacent, all layers)
Captured: 2026-07-21

## Possible feats

- **Neutral retrieval-primitive contract** (`search`, `search_<source>`,
  `who_knows`, `recall`) returning governed context-packets.
- **Planner→executor→synthesizer** query pipeline (the MoA "advises" path).
- **The ranking recipe** (hybrid + RRF + age decay) as gateway retrieval config.
- **MCP tool exposure** of the primitives, consent/tenant-bounded.

## Principle: primitives, not an answer endpoint

Cerebras deliberately publishes low-level primitives (`search_slack`,
`search_code`, `who_knows`) returning raw evidence rows, and lets clients
orchestrate — rather than a single "answer" endpoint. xFactory does the same,
for a governance reason as much as a flexibility one: the primitives return
**governed context-packets** (consent-checked, tenant-scoped, authority-tagged),
and a **Hermes persona decides** on them. An answer endpoint would collapse the
"advises vs. decides" line the whole model rests on.

## The primitives

Each returns `context-packet`s (the ratified retrieval unit), never raw secrets,
always carrying provenance + `source_authority`:

```text
search(query, {tenant, projects, source_classes?, k, recency_weight})   → [context_packet]
search_chat | search_code | search_tickets | search_docs | search_crm    → source-class-scoped search
who_knows(topic, {tenant, projects})                                     → [expertise_packet]   # who worked on / owns this
recall(subject_ref)                                                      → [context_packet]     # a subject's memory + journey_state
```

- `search` is hybrid across permitted sources; `search_<source>` scopes to one
  class (Cerebras' `search_slack`/`search_code`).
- `who_knows` maps to the client `staff_capability_map` + authorship in evidence
  rows — expertise/ownership lookup, not content.
- `recall` pulls a subject's private memory and journey state (subject-layer),
  consent-gated per the subject.

## The query pipeline (planner → executor → synthesizer), governed

```text
planner(query, caller_context)  → plan{primitives[], source_classes[]}
executor(plan)                  → evidence[]        # parallel; hybrid rank; normalized to context-packets
synthesizer(evidence)           → advisory_answer{summary, citations[], authority_flags}
```

- **Planner** (lightweight LLM) picks which primitives/sources matter — but only
  over sources the caller has consent + tenant + ACL access to (it cannot plan
  into what it may not see).
- **Executor** runs primitives in parallel, applies the ranking recipe, and
  **enforces the filters at retrieval time**: tenant, consent, ACL, revocation.
- **Synthesizer** composes a cited summary, weighting by source-authority and
  flagging anything below the floor. It is **advisory** — the output is context
  for a Hermes decider, never itself a governance decision.

This pipeline *is* an MoA `panel_synthesis` over sources (see
`codexfactory-domain-deliberation.md`): it advises; Hermes decides.

## Ranking recipe (Cerebras)

Hybrid: full-text + embedding + IDF weighting + **age decay**, fused by
**reciprocal rank fusion**. Age decay is load-bearing for operational client
knowledge (recent truth wins) and is client-tunable (`recency_weight`), within a
domain-set band. `key_excerpts` ("burst") surface high-signal raw items
alongside the structured summary.

## Governance at retrieval (the delta from Cerebras)

Cerebras is internal; xFactory governs every read:

- **Consent per query** — not only at ingest; a person-subject's (patient's)
  consent is checked on each `recall`.
- **Tenant isolation** — a query never returns another tenant's rows.
- **ACL / visibility** — the source-derived `visibility` on each row is honored;
  the caller sees only what its permissions allow.
- **Source-authority floor** — evidence below `source_authority_minimum`
  (`cited_source` in the domain expert gateway) cannot silently drive synthesis;
  it may appear, flagged, but not as load-bearing.
- **Audit + erasure** — a `usage-event` per retrieval; revoked/erased rows are
  never returned.

## MCP exposure & plane placement

The primitives are published as **governed MCP tools** (Cerebras exposes via
MCP), so orchestrators — the deployed Hermes, omnigent workers, or an operator's
Claude Code — compose them, each call consent/tenant-bounded. Plane placement:
the primitives are called by **Plane-1 personas** gathering evidence to decide
(e.g. the Change Approvals Authority calling `search` + `recall` before a
clearance) and by **Plane-2 workers**; the planner/executor/synthesizer is the
advisory retrieval path, and the persona makes the call.

## Open questions

- **Planner cost/latency** — an LLM planning pass per query (Cerebras' design)
  vs. a cheap router for simple `search_<source>` calls; reserve the planner for
  cross-source questions?
- **expertise_packet shape** — is `who_knows` a distinct packet kind or a
  `context-packet` profile over the staff-capability map + authorship?
- **Synthesis authority weighting** — exact function mapping `source_authority`
  to rank weight, and the floor's default per layer.
- **recall consent granularity** — per-field consent on a subject's memory
  (a patient consents to some memory being recalled, not all)?
- **Cross-tenant domain learning** — how does the domain query its de-identified
  `domain_learning` (cross-client) without breaching tenant isolation — a
  separate authority-scoped primitive?
