# Synthesis: Hermes Governed Practice Loop — Brainstorm

Status: brainstorm
Kind: process
Summary: Seeded Hermes authority and the governed nightly sweep can turn
observed gaps into suggestions while keeping clearance and realization
outside the domain's autonomous boundary.
Topics: hermes, nightly-sweep, practice-adoption, layer-content-seeding, synthesis
Repository context: openxFactory three-layer Hermes and practice-adoption exploration
Captured: 2026-07-28

## Possible feats

- **Hermes practice-suggestion run** — pin layer content, scan declared
  evidence, emit suggestions, and record cost without applying changes.

## Members and their joints

Atomic members:
[Hermes-Governed Nightly Sweep](hermes-governed-nightly-sweep.md),
[Three-Layer Hermes Content and Seeding](hermes-layer-content-seeding.md),
and [Hermes Layer Seeding Mechanism](hermes-layer-seeding-mechanism.md).

### Seeded authority bounds the sweep

The sweep loads pinned Domain, Client, and Project Hermes content so it can
distinguish domain suggestions, tenant clearance conditions, and project
realization state.

### Observation remains non-mutating

The run may read health, capability, and adoption evidence and emit structured
suggestions. It cannot approve its own proposal, alter policy, or merge the
realization.

## Emergent behavior

The factory gains a recurring learning trigger whose output enters the same
governance path as human-originated improvement ideas.

## Tensions to hold

- Nightly cadence improves freshness but can generate repetitive noise and
  spend.
- Layer pins improve reproducibility while long-running scans may observe
  newer repository state.
- Suggestion quality should improve without normalizing auto-approval.

## Recombination opportunities

The full suggest-clear-realize lifecycle is in the
[practice-adoption packet](practice-adoption-overview.md).

## Open questions

- Which evidence snapshots are pinned for a sweep?
- How are duplicate suggestions suppressed without hiding recurrence?
- Which layer pays and accounts for a cross-layer scan?
