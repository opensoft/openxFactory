# Ideation Work Area

Status: ratified
Kind: process
Ratified by: [add-document-lifecycle-vocabulary](../openspec/changes/archive/2026-07-09-add-document-lifecycle-vocabulary/proposal.md)
Repository context: openxFactory
Purpose: provide the governed pre-proposal pipeline that turns free-form
thinking into OpenSpec proposals, so prose never silently becomes (or
contradicts) policy.

## Lifecycle

```text
brainstorm/<topic>.md      free-form discussion and design exploration;
                           explicitly NON-NORMATIVE — nothing here is policy,
                           and doc-health checks ignore contradictions here
      |
      |  organize gate: pieces get identity, duplicates merge,
      |  each fragment names the spec or capability it targets
      v
staging/<topic>/           structured fragments ready for proposal drafting:
                           claim, target capability, delta type
                           (ADDED / MODIFIED / REMOVED), evidence links
      |
      |  proposal gate: selected files move with Git history
      v
openspec/changes/<name>/   a normal OpenSpec change proposal with source
  supporting-docs/        material and a manifest; from here the standard
                           flow applies (approve -> implement -> archive)
      |
      |  archive gate: support becomes a verified tar-gzip bundle
      v
openspec/changes/archive/  proposal history + promoted spec delta + bundle
```

Rules while this convention is in draft:

- Content in `brainstorm/` may contradict promoted specs freely; that is what
  the area is for. Everywhere else, prose that changes promoted policy must be
  an explicit delta (see the doc-health pipeline brainstorm).
- Moving material from `brainstorm/` to `staging/` and from `staging/` to an
  OpenSpec change are deliberate, reviewed steps. Selected staged files are
  moved, not copied, into the change's `supporting-docs/` folder. Unselected
  files remain staged for a later proposal.
- `ideation/staging/` lists only organized work that has not crossed a proposal
  gate. Completed proposal source is retained with the active or archived
  OpenSpec change, not as a stale staged topic.
- Each DomainxFactory keeps its own `ideation/` area for domain-scoped topics;
  cross-factory and contract-level topics belong here in openxFactory.

## Ideation Header Format

Every file under `brainstorm/` uses this title and header, in this order:

- Title: `# <Title> — Brainstorm` — always end the H1 with the
  ` — Brainstorm` suffix (imported/evidence files keep an identifying
  prefix, e.g. `# NotebookLM Ideas: <workspace> — Brainstorm`), so
  `grep '— Brainstorm$'` finds every brainstorm doc by title alone.
- `Status:` — `brainstorm` (raw capture) or `staged` (organized; kept as
  design history) per the [document lifecycle](../docs/document-lifecycle.md)
  taxonomy. Status tracks lifecycle state, not folder — an organized
  brainstorm file stays physically in `brainstorm/` with `Status: staged`.
- `Kind:` — required; one of the recommended vocabulary (`architecture |
  plan | process | runbook | report | register | template | reference`).
- `Summary:` — required; one sentence stating what the document concludes or
  proposes, not its intent — write it so a reader never has to open
  `## Problem` to know what's inside.
- `Topics:` — required; a comma-separated list of subject keywords (target
  capability names where one exists, plus free-text terms), so `grep
  'Topics:'` across `ideation/` surfaces every doc touching a subject
  without reading prose bodies.
- `Repository context:` — required.
- `Captured:` — the date free-form thinking was captured here. Imported
  evidence (e.g. a NotebookLM export) uses `Source workspace:` / `Source
  workspace id:` / `Origin:` instead, since it wasn't authored in-session.
- `Organized:` — present once the ideas move on; the date plus a link to
  every destination (OpenSpec change, doc, or staged topic) they landed in,
  and each link's current lifecycle word (`proposed` / `ratified`). Point
  destination links at the change's *current* location (active vs.
  archived) — a link left pointing at an active path after that change
  archives, or a status word left saying "proposed" after it ratifies, is
  the defect this format exists to catch.
- `Participants:` — optional; who was in the design session.
- `Purpose:` — optional; use in place of a `Problem` section for
  evidence/reference-gathering brainstorms rather than design-exploration
  ones.

Every file under `staging/<topic>/` carries the same `Status:` (always
`staged`), `Kind:`, `Summary:`, and `Topics:` fields, in that order, before
`Repository context:`, followed by the staging-specific fields: `Staging ID:`
(`<repo>:staging:<topic-slug>`, durable after the folder moves or is
compressed), `Source:`, and — wherever the doc declares deltas —
`Target capabilities:` naming each target with its delta type
(ADDED / MODIFIED / REMOVED). The topic's primary doc H1 uses the
`# Staged: <Title>` prefix; supporting fragments use plain titles. `Topics:`
complements `Target capabilities:` — free subject keywords versus declared
deltas — so a subject grep spans both stages with one field name.

## Contents

Brainstorm (design history; fully organized into staging or an archived
proposal):

- [Doc Health Pipeline](brainstorm/doc-health-pipeline.md) — split into the
  prose-tagging, doc-health-checks, and semantic-health-sweep staged topics;
  its lifecycle/ideation sections were ratified by
  add-document-lifecycle-vocabulary.
- [Domain-To-Neutral Concept Promotion](brainstorm/domain-to-neutral-promotion.md)
  — organized into the promotion process doc, the candidate register, and the
  promotion-refinements staged topic.
- [Workflow Visualization Tooling](brainstorm/workflow-visualization-tooling.md)
  — organized into the workflow-visualization staged topic; kept as license
  evidence.
- [OpenSpec × Speckit Release Flow](brainstorm/openspec-speckit-release-flow.md)
  — organized into the archived
  [add-release-realization-flow](../openspec/changes/archive/2026-07-09-add-release-realization-flow/proposal.md)
  change: release targets, delta-driven feat decomposition, and the archive
  gate binding to merge evidence.
- [Ideation Cross-Reference Readiness Index](brainstorm/ideation-cross-reference-readiness.md)
  — organized 2026-07-12 after all seven open questions were decided, and
  promoted the same day into the add-ideation-cross-reference-readiness
  proposal; kept as design history with the decisions inline.
- [Ideation Area Dashboard](brainstorm/ideation-dashboard.md) — organized
  2026-07-12 into the ideation-dashboard staged topic (six-column docs-first
  realization funnel over a possibles register, pipeline board, doc list,
  and non-mutating workbench; drafts gate artifacts, never executes gates)
  and promoted the same day into the add-ideation-dashboard proposal; kept
  as design history with the in-session decisions inline.

Brainstorm (active):

- none currently.

Staged topics: see the [Staging Index](staging/INDEX.md), the kept-current
inventory of every topic under `staging/` — update it, not this list, when a
staged file is added, removed, or promoted.

Active proposals promoted from staging:

- [define-avatar-client-contract-kernel](../openspec/changes/define-avatar-client-contract-kernel/proposal.md)
  — owns the historical staged avatar packet and proposes only the canonical
  eight-contract AVC kernel, registries, fixtures, validator, and release.
- [qualify-avatar-brokered-call-feasibility](../openspec/changes/qualify-avatar-brokered-call-feasibility/proposal.md)
  — approved split owning the isolated F0 harness and empirical evidence.
- [implement-avatar-reference-runtime](../openspec/changes/implement-avatar-reference-runtime/proposal.md)
  — approved split owning the non-deployable deterministic broker reference.
- [align-avatar-first-ui-standard](../openspec/changes/align-avatar-first-ui-standard/proposal.md)
  — approved split owning the avatar-first standard, profile, examples, and
  validator. All four workstreams may start in parallel; publication and final
  conformance pins remain ordered.
- [add-cross-factory-ideation-routing](../openspec/changes/add-cross-factory-ideation-routing/proposal.md)
  — owns the former `ideation-routing` staged packet under
  `supporting-docs/` and proposes capture-first claim routing, destination
  acceptance, deterministic routing validation, and a bounded organizer.
- [add-document-cataloging](../openspec/changes/add-document-cataloging/proposal.md)
  — user-approved split from the former umbrella proposal; owns external
  controlled tagging, immutable catalog snapshots, deterministic catalog
  validation, and the bounded document cataloger.
- [add-proposal-origin-contract](../openspec/changes/add-proposal-origin-contract/proposal.md)
  — owns the former `proposal-origin-contract` primary doc under
  `supporting-docs/` and proposes the mandatory staged/ad-hoc origin
  declaration, gate rejections, archive retention, migration, and the
  proposal-origin doc-health family; the FDA SaMD rationale deliberately
  remains staged.
- [add-ideation-cross-reference-readiness](../openspec/changes/add-ideation-cross-reference-readiness/proposal.md)
  — owns the former `ideation-cross-reference-readiness` staged packet under
  `supporting-docs/` and proposes the unified cross-stage topic index,
  three-tier Hermes readiness panel, minimum-score recommendation gate, and
  nightly readiness lane.
- [add-ideation-dashboard](../openspec/changes/add-ideation-dashboard/proposal.md)
  — owns the former `ideation-dashboard` staged packet (primary doc plus the
  interactive mockup) under `supporting-docs/` and proposes the realization
  funnel snapshot, possibles register, workbench, interactivity boundary,
  and nightly snapshot lane.

Proposal source and completed design history are retained with their active or
archived OpenSpec changes under `supporting-docs/` or
`supporting-docs.tar.gz`, with readable manifests.
