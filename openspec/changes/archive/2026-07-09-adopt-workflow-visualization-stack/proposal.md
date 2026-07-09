# Adopt Workflow Visualization Stack

## Why

The client Hermes validation walkthrough needs workflow visualization — the
avatar-first UI standard defines the interaction surface but no sanctioned
tooling exists for rendering and editing workflow contracts. The staged
topic `ideation/staging/workflow-visualization/` carries a license-verified
MIT shortlist and a nine-view acceptance checklist; without ratification,
every future UI feat re-litigates tool choice, and a non-MIT dependency
could slip in unreviewed.

## What Changes

- Sanction the visualization stack under an MIT-only rule: Mermaid for
  generated read-only diagrams, React Flow for the interactive validation
  canvas, XState for workflow state semantics and simulation, Cytoscape.js
  for evidence graphs, with Excalidraw (annotation) and Dagre (layout) as
  supporting tools.
- Exclude bpmn-js, JointJS, and GoJS (non-MIT) unless a separate license
  decision reverses it.
- Ratify the nine walkthrough views as the acceptance checklist for the
  validation UI.
- Require license re-verification (project source or package metadata
  declaring MIT, including transitive review) before any dependency lands.

## Capabilities

### New Capabilities

- `workflow-visualization`: sanctioned tooling, license rule, and walkthrough
  view coverage for workflow-contract visualization.

### Modified Capabilities

- None. (The avatar-first UI standard is referenced, not altered; this
  capability covers the conventional-UI companion surface.)

## Impact

- openxFactory: new `docs/workflow-visualization-standard.md`; README index
  link; staged topic closure.
- codexFactory: future Spec Kit feature work implements the validation UI
  against this standard — that implementation is NOT part of this change
  (doc-only; archives on doc landing; the UI feats will be code-surface
  work under whatever branch discipline is then in force).
- No runtime, schema, or credential impact.
