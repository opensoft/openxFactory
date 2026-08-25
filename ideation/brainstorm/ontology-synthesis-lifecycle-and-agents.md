# Synthesis: Ontology Lifecycle and Maintenance Agents — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A governed ontology needs an explicit exploration map, stable
foundations, and bounded maintenance agents that propose rather than silently
rewrite semantic authority.
Topics: ontology, domain-ontology-lifecycle, maintenance, micro-agents, synthesis
Repository context: openxFactory ontology lifecycle exploration
Captured: 2026-07-28

## Possible feats

- **Ontology maintenance council queue** — collect agent-proposed additions,
  conflicts, aliases, and deprecations with evidence and disposition state.
- **Semantic drift sentinel** — detect when observed language or outcomes no
  longer fit the pinned ontology revision.

## Members and their joints

Atomic members:
[Ontology and Omnigent Micro-Agent Exploration Map](ontology-and-micro-agent-exploration-map.md),
[Ontology Layer Foundations](ontology-layer-foundations.md),
[Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md),
and [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md).

### The map bounds the program

The exploration map separates ontology ownership, generation, compilation,
routing, evaluation, and maintenance so no single worker becomes an
unreviewed semantic authority.

### Agents produce evidence-bearing proposals

Maintenance agents may observe unknown terms, relation conflicts, coverage
gaps, or drift. Their output is a proposal with evidence and affected
concepts. Human or governed domain authority decides whether the ontology
changes and publishes a new revision.

### Compilation exposes lifecycle pressure

Repeated compilation misses and manual context repairs become evidence for
maintenance. They do not themselves mutate the ontology; they enter the same
reviewable queue as other observations.

## Emergent behavior

The combined loop lets execution improve the semantic layer while conserving
authority: use generates observations, agents structure them, and a governed
decision produces a new pinned revision.

## Tensions to hold

- Automatic discovery is valuable, but automatic semantic promotion would
  make execution results self-authorizing.
- Strict revision pinning improves reproducibility but can slow correction of
  urgent domain terminology gaps.

## Recombination opportunities

The lifecycle can reuse the
[practice-adoption packet](practice-adoption-overview.md) for suggest,
clear, and realize states, while retaining ontology-specific evidence.

## Open questions

- Which authority may approve neutral versus domain ontology changes?
- How are aliases distinguished from genuinely new concepts?
- When does accumulated drift force re-compilation of stored contexts?
