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

- [client-infrastructure-liaison](staging/client-infrastructure-liaison/client-infrastructure-liaison.md)
  — adds a neutral Client Hermes coordination role and structured request
  lifecycle for client-managed, managed-host, or OpsxFactory-executed
  infrastructure dependencies without granting domain agents tenant
  administration authority.
- [proposal-origin-contract](staging/proposal-origin-contract/origin-contract.md)
  — requires every OpenSpec proposal to identify a durable staging origin or
  an explicitly approved ad-hoc origin; this topic must dogfood the staged
  origin path when it becomes a proposal. Its supporting
  [FDA SaMD traceability rationale](staging/proposal-origin-contract/fda-samd-traceability-rationale.md)
  records why origin provenance is necessary but not sufficient for regulated
  device-software traceability.

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

Proposal source and completed design history are retained with their active or
archived OpenSpec changes under `supporting-docs/` or
`supporting-docs.tar.gz`, with readable manifests.
