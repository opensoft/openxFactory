# Design: Ideation Cross-Reference Readiness Index

## Context

The ideation area now has consistent, grep-able headers (`Topics:` on
brainstorm and staging docs, `Target capabilities:` on staging docs) and a
kept-current staged-file inventory (`staging/INDEX.md`). What it lacks is the
join: which subjects recur across stages, whether a promoted capability
already exists that a cluster would extend, and whether any cluster is mature
enough that a human should be asked to open a proposal.

The design was brainstormed and staged on 2026-07-12 with all seven open
questions decided the same day (project-layer lens, score rule, index
placement, re-run trigger, tag source, rationale format, citation
strictness); the supporting document carries the decision record. The active
`add-doc-health-semantic-sweep`, `add-document-cataloging`, and
`add-cross-factory-ideation-routing` changes supply the bounded-worker
pattern, the future controlled tag source, and the evidence-contract shape
this capability deliberately reuses.

Delta sequencing: the doc-health "Deterministic check families" requirement
is modified, in declared order, by the semantic-sweep, cataloging (13th
family), routing (14th family), and proposal-origin (15th family) changes.
This change is proposed together with `add-proposal-origin-contract` and
declares its enumeration delta relative to that change's outcome — it keeps
fifteen deterministic families and adds only the readiness *lane*; index
validation runs as an openxFactory strict validator in the existing per-repo
preflight, not as a sixteenth family.

## Goals / Non-Goals

**Goals:**

- One glanceable, topic-clustered answer to "what is mature enough to
  propose?" spanning brainstorm, staging, and archive.
- Three genuinely independent readiness lenses whose minimum — not average —
  gates the recommendation, so no tier can be outvoted into silence.
- Full reuse of the organizer/cataloger evidence contract and the
  bounded-worker execution split; no new rationale format, no new authority.

**Non-Goals:**

- Ownership or destination resolution (`ideation-routing` owns that; a topic
  can be routing-resolved yet unready, or ready yet unrouted).
- Tag taxonomy definition (`document-cataloging` owns that; this index
  bootstraps from headers and folds catalog tags in later).
- Any autonomous lifecycle action — the gate emits a recommendation for a
  human authority; proposing remains a deliberate, authorized step.
- Rendering. The separate ideation-dashboard brainstorm may later consume
  this index; this change defines the data contract only.

## Decisions

- **Unified cross-stage file** (`ideation/cross-reference.md`) rather than a
  per-folder sibling of `staging/INDEX.md`: clusters span stages by design,
  and the inventory and the cluster index serve different purposes.
- **Minimum >= 8 gate** with a spread-conflict flag below threshold —
  mirroring the domain-to-neutral-promotion stance that inter-tier
  disagreement is signal, not noise to average away.
- **Project tier = engineering buildability** (codexFactory feature
  decomposition); aggregation/composition concerns stay with the company
  tier.
- **Nightly doc-health lane, snapshot-consistent:** the pass consumes the
  deterministic run's inventory so scores cite the same corpus the report
  describes; report-only in v1 like every other agentic lane.
- **An unscoreable tier blocks the gate:** where a tier cannot score (for
  example no owning domain resolves), the entry records why and the topic
  cannot be flagged — an undefined minimum is not a passing one.
