# Staged: Workflow Validation UI Tooling

Status: staged
Kind: reference
Repository context: openxFactory
Source: [workflow-visualization-tooling brainstorm](../../brainstorm/workflow-visualization-tooling.md)
Target capability: relates to the avatar-first UI standard and the client
Hermes validation walkthrough (delta: ADDED — a UI tooling decision record
plus, later, codexFactory implementation feats). Orthogonal to doc-health:
this visualizes workflow contracts for client validation, not document
lifecycle state.

## Claims

1. MIT-only shortlist holds (license re-verified before any dependency add):
   Mermaid (read-only generated diagrams), React Flow (interactive
   validation/editing), XState (workflow state semantics/simulation),
   Cytoscape.js (evidence graphs), Excalidraw (collaborative annotation),
   Dagre (layout helper). Excluded: bpmn-js, JointJS, GoJS (non-MIT).
2. Adoption order: Mermaid first (audit-friendly, diffable, zero-runtime),
   React Flow for the editable validation canvas, XState when simulation is
   needed, Cytoscape.js for evidence graphs.
3. Nine walkthrough views (current-state, target-state, delta, evidence
   graph, swimlane, approval gates, exceptions, bottlenecks, consent) — the
   brainstorm's view list is the acceptance checklist for the eventual UI.
4. The same Mermaid pipeline can serve doc-health report diagrams later, but
   that is a consumer, not a requirement of this feat.

## Exit

Satisfied by
[adopt-workflow-visualization-stack](../../../openspec/changes/archive/2026-07-09-adopt-workflow-visualization-stack/proposal.md)
(2026-07-09), ratifying [docs/workflow-visualization-standard.md](../../../docs/workflow-visualization-standard.md).
Spec Kit feature work in codexFactory implements the validation walkthrough
UI against the nine-view checklist.
