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

## Contents

Brainstorm (design history; both fully organized into staging):

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

Brainstorm (active):

- [OpenSpec × Speckit Release Flow](brainstorm/openspec-speckit-release-flow.md)
  — brownfield realization axis: release targets, delta-driven feat
  decomposition, and the archive gate binding to merge evidence.

Staged topics:

- None after the proposal-support migration. New organized work appears here
  only until its OpenSpec proposal is created.

Proposal source and completed design history are retained with their active or
archived OpenSpec changes under `supporting-docs/` or
`supporting-docs.tar.gz`, with readable manifests.
