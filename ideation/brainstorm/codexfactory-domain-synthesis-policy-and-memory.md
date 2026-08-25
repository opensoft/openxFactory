# Synthesis: codexFactory Domain Policy and Memory — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Domain policy, memory boundaries, and the practice catalog form a
small governed delta that makes software-engineering decisions repeatable
without storing a generic textbook.
Topics: codexfactory-domain, codexfactory, domain-policy, domain-memory, practice-catalog, synthesis
Repository context: openxFactory exploration for codexFactory Domain Hermes
Captured: 2026-07-28

## Possible feats

- **Domain content compiler** — validate and package policy positions,
  memory boundaries, and practice-adoption profiles for deterministic seeding.

## Members and their joints

Atomic members:
[Domain Hermes Content](codexfactory-domain-hermes-content.md),
[Domain Policy Model](codexfactory-domain-policy-model.md),
and [Domain Memory and Practices](codexfactory-domain-memory-and-practices.md).

### Policy stores consistency-critical choices

The policy model stores rules, staked positions, fail-closed boundaries, and
gate semantics that must remain stable. Generic software knowledge remains a
model capability rather than duplicated domain content.

### Memory separates learning from tenant data

Domain memory may retain de-identified cross-client learning only through a
governed promotion path. Client-private evidence and subject-private recall
remain outside the domain store.

### Practices convert learning into suggestions

The practice catalog expresses adoption profiles over promoted capabilities.
It can identify a gap and suggest a change, but client clearance and project
realization remain downstream authorities.

## Emergent behavior

The domain layer can learn and recommend while preserving tenant isolation
and keeping its stored content compact, reviewable, and seedable.

## Tensions to hold

- Sparse stored policy relies more heavily on model behavior.
- Cross-client learning is valuable only if de-identification and promotion
  are credible.
- Practice profiles can become stale as promoted capabilities evolve.

## Recombination opportunities

This cluster feeds the
[practice-adoption packet](practice-adoption-overview.md) and the
[Hermes layer runtime](hermes-overview.md).

## Open questions

- What evidence threshold permits cross-client promotion?
- How are practice profiles versioned against capability releases?
- Which accumulated lessons deserve policy rather than memory status?
