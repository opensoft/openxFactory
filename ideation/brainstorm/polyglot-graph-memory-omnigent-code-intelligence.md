# Omnigent Code-Intelligence Graph Composition — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Omnigent can assign CodeGraph, codebase-memory-mcp, and optionally GitNexus to different worker roles so generation, verification, and challenge use complementary graph evidence rather than one shared index by default.
Topics: polyglot-graph-memory, omnigent-code-intelligence, omnigent, omnigent-domain-overlay, codegraph, codebase-memory-mcp, gitnexus, worker-archetypes
Repository context: openxFactory (neutral Omnigent provider composition, with codexFactory as the first natural domain specialization)
Captured: 2026-07-30

## Possible feats

- **Code-intelligence provider bindings** — bind approved graph roles to Omnigent worker profiles and task purposes.
- **Dual-evidence coding lane** — use one provider to navigate and another to verify change impact or call structure.
- **Specialist graph checks** — add licensed, purpose-specific process, API-shape, data-dependence, or taint analysis without making them universal worker dependencies.

## Focus

This document isolates how multiple code-graph products can improve Omnigent
execution. Using several providers is valuable only if each has a declared
responsibility. Sending the same broad request to every graph and concatenating
their results creates cost and disagreement without independent assurance.

The relevant products are:

- [CodeGraph](https://github.com/colbymchenry/codegraph), oriented around
  automatically synchronized, compact source context, paths, and blast radius;
- [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp),
  exposing explicit search, architecture, trace, diff-impact, schema, snippet,
  and read-only graph-query operations;
- [GitNexus](https://github.com/nxpatterns/gitnexus), adding process-grouped
  search, cross-repository contracts, API analysis, and optional program/data
  dependence tooling.

GitNexus currently carries a
[PolyForm Noncommercial license](https://raw.githubusercontent.com/nxpatterns/gitnexus/main/LICENSE);
commercial use is an adoption gate, not a detail to defer.

## Proposed model

Bind providers to worker responsibilities:

```text
Hermes-approved engineering job
  |
  +-- frame / generate
  |     -> primary navigator
  |        e.g. CodeGraph current source + paths + blast radius
  |
  +-- verify
  |     -> independent structural verifier
  |        e.g. codebase-memory-mcp trace + diff impact + graph query
  |
  +-- challenge
  |     -> optional specialist
  |        e.g. GitNexus contract, API-shape, PDG or taint analysis
  |
  +-- assemble_for_admission
        -> cited findings, disagreements and coverage
           never raw unrestricted graph databases
```

The concrete provider assignments are defaults, not permanent product
semantics. A profile may reverse CodeGraph and codebase-memory-mcp after
evaluation, or use only one for a small bounded task.

A provider invocation should be selected from:

- worker archetype and class;
- requested artifact and validation type;
- repository/ref and worktree identity;
- language/framework coverage;
- required freshness and diff baseline;
- tool and token budget;
- independence requirement;
- provider admission and licensing status.

The assembler should receive provider findings with source references,
queries, graph revision, coverage, and unresolved disagreement. It should not
receive two complete graph dumps.

## Interfaces and boundaries

The Omnigent orchestrator chooses from provider bindings declared by an
approved worker profile. Workers do not install, configure, broaden, or grant
themselves access to graph servers.

Graph tools may:

- navigate a repository and return bounded source;
- trace call, import, route, type, or process relationships;
- estimate a change blast radius;
- report coverage, uncertainty, or missing resolution;
- generate advisory architecture or impact evidence.

They may not:

- widen the job scope or worker permission matrix;
- turn a detected relationship into approval or admission;
- mutate an authoritative graph or source repository outside the job's tools;
- conceal index staleness or branch mismatch;
- promote worker observations directly into Domain Hermes memory.

Provider installers often edit agent instructions, MCP configuration, or
hooks. Omnigent installations should use explicit, digest-pinned toolchain
bindings rather than run several interactive auto-installers inside a shared
checkout.

## Alternatives and tensions

**One primary graph for every worker** is operationally simpler and may be
enough for low-risk tasks, but generation and verification then share the same
parser and resolution errors.

**Two providers on every task** improves independence only when their
extraction and query paths actually differ. It can double indexing and context
cost without improving the decision.

**Raw-source verification only** provides the strongest final evidence but is
too expensive as the default exploration strategy. Graph-first navigation
followed by targeted source validation preserves efficiency.

**GitNexus as the universal multi-repository engine** is technically
interesting for the xFactory family, but its current licensing posture must be
resolved before it becomes a commercial runtime dependency.

## Open questions

- Which worker classes require an independent graph verifier rather than a
  single provider plus targeted raw-source reads?
- Does provider independence require distinct parsers/resolvers, or is a
  distinct query and worker sufficient?
- Which graph findings qualify as acceptance evidence versus navigation
  hints?
- How are branch changes, worktree moves, and concurrent edits reflected in
  graph freshness before a worker acts?
- Should provider disagreements trigger a challenge worker, raw-source
  adjudication, or a Hermes review packet?

## Relationships

- [Graph Provider Portfolio](polyglot-graph-memory-provider-portfolio.md)
  supplies the `primary`, `verifier`, `companion`, and `fallback` roles.
- [Graph Provider Contract](polyglot-graph-memory-provider-contract.md) defines
  bounded provider inputs and outputs.
- [Synthesis: Surface and Layer Placement](polyglot-graph-memory-synthesis-surface-and-layer-placement.md)
  relates the execution graph lane to Hermes ownership.
- Existing design context:
  [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md).
