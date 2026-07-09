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
      |  proposal gate: the staged set is coherent and complete
      v
openspec/changes/<name>/   a normal OpenSpec change proposal; from here the
                           standard flow applies (approve -> implement ->
                           archive -> promoted specs)
```

Rules while this convention is in draft:

- Content in `brainstorm/` may contradict promoted specs freely; that is what
  the area is for. Everywhere else, prose that changes promoted policy must be
  an explicit delta (see the doc-health pipeline brainstorm).
- Moving material from `brainstorm/` to `staging/` and from `staging/` to an
  OpenSpec change are deliberate, reviewed steps — never bulk copies.
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

Staged topics (orthogonal feats; each exits through an OpenSpec change):

- [prose-tagging](staging/prose-tagging/tag-syntax.md) — concrete xspec
  candidate/supersedes tag syntax.
- [doc-health-checks](staging/doc-health-checks/nightly-run-shape.md) — the
  deterministic nightly run, report, and ranked plan
  (+ [status-check-rules](staging/doc-health-checks/status-check-rules.md)).
- [semantic-health-sweep](staging/semantic-health-sweep/agentic-pass.md) —
  the agentic contradiction/normative-prose pass; deliberately sequenced
  after the deterministic run.
- [promotion-refinements](staging/promotion-refinements/open-questions.md) —
  drafting ownership, stack.yaml provenance fields, mid-promotion pins.
- [workflow-gate-contract](staging/workflow-gate-contract/neutralization-draft.md)
  — DTN-001 + DTN-002 neutralization (workflow schema + gate vocabulary).
- [workflow-visualization](staging/workflow-visualization/validation-ui-tooling.md)
  — MIT tooling decision for the client validation walkthrough UI.
