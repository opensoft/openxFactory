# Design: Ideation Area Dashboard

## Context

The 2026-07-12 design session (Brett + Claude, with an interactive mockup
iterated live) settled the dashboard's shape: a realization funnel as the
centerpiece — not a document list with charts. The funnel's left hops are
many-to-many (one doc feeds several clusters via `Topics:`; one possible can
be claimed by several clusters), so the model draws explicit edges and
counts links, not cards. The decision record in the supporting document
carries D1-D6 (locked in session) and R1-R14 (drafted recommendations
confirmed unchanged by Brett on 2026-07-12).

Two contracts this change deliberately reuses rather than invents: the
organizer/cataloger evidence contract (for human-seen-cluster intake) and
the projection discipline of the lifecycle-notebook capability (derived
artifacts are regenerated, never edited). The possibles register lives in
the cross-reference index — the same consolidation posture as the readiness
index's tag bootstrap — so no third standalone register file exists.

Delta sequencing: `ideation-cross-reference` exists only as deltas of the
active ratified `add-ideation-cross-reference-readiness` change, so this
change's `ideation-cross-reference` delta is declared relative to that
change's outcome per the ordered-deltas rule and archives after it. The
doc-health delta adds a deterministic output lane only (like the report
itself), so it does not touch the contested check-family enumeration.

## Goals / Non-Goals

**Goals:**

- One glanceable governance picture: what exists, at which stage, heading
  where — and what each cluster could still become.
- Make unpicked possibles durable backlog instead of evaporating prose,
  with organize-gate picks recorded as cited edges.
- Give humans a bounded way to assemble doc sets and point existing tools
  (NotebookLM, readiness scoring, doc-health) at them, feeding human-seen
  patterns back into the machine queue as evidence-backed signal.
- Make the dashboard the human's authoring cockpit over the ideation
  corpus: scaffolded header-compliant creation and select-to-edit in the
  human's own editor — the dashboard launches edits, it never rewrites
  content itself.

**Non-Goals:**

- Executing any lifecycle gate — permanent boundary, not a v1 limitation.
  The strongest allowed concession is drafting a gate artifact for human
  review.
- Semantic content analysis (NotebookLM's job) or readiness judgment (the
  readiness panel's job) — the dashboard renders their outputs.
- Domain factory coverage in v1 — the `repository` field keeps that
  additive.
- Exhaustive historical backfill — only the worked examples become renderer
  fixtures (R4).

## Decisions

- **Snapshot as the only data path** (D6/R13): generator scans `ideation/`
  + active and archived changes; renderers read the snapshot only; both
  snapshot and workbench manifests are promoted schema-versioned contracts.
- **Workbench, not "temp staging"** (R5): the contract word avoids
  collision with the `staged` status and `ideation/staging/`; nothing is
  ever written under `ideation/staging/` except by the human organize gate.
- **Per-actor mutation authority** (D7-D9): the automated machinery
  (generator, renderers, workbench actions) stays non-mutating over
  existing source docs; humans create and edit corpus docs through the
  dashboard, with lifecycle discipline and doc-health applying to those
  edits unchanged; agents — any Hermes tier or Omni worker — create new
  corpus docs but never modify or delete existing ones; deleting a
  doc/source in a corpus-bound notebook removes it from that set only, and
  lifecycle projections restore their sets on the next sync.
- **Gitignored workbench manifests** (R6): committed manifests are
  disallowed to prevent pseudo-staging; browser state may hold unsaved
  sets.
- **Scratch notebooks are derived artifacts** (R7): `xf-wb-*` notebooks die
  with their manifest; the notebook sync gains an orphan sweep.
- **v0 = the mockup grown up** (R12): the staged `dashboard-mockup.html` is
  the renderer skeleton; a Mermaid stage-count summary is an optional
  byproduct.
- **Nightly + on-demand regeneration only** (R14): no per-commit
  regeneration in v1.
