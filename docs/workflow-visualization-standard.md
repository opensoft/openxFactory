# Workflow Visualization Standard

Status: ratified
Kind: reference
Repository context: openxFactory
Ratified by: [adopt-workflow-visualization-stack](../openspec/changes/adopt-workflow-visualization-stack/proposal.md)
Purpose: sanction the tooling for workflow-contract visualization and fix the
walkthrough view coverage that validation-UI feature work is accepted
against. Companion to the [Avatar-First UI Standard](avatar-first-ui-standard.md)
— the avatar owns the interaction surface; this standard covers the
conventional visualization surface beside it.

## License Rule

Only MIT-licensed tools may be adopted. License is verified at adoption time
from current project source or package metadata, including transitive
dependencies and commercial-use terms. Non-MIT tools — explicitly including
`bpmn-js` (bpmn.io license), `JointJS`, and `GoJS` — require their own
ratified decision before use. License evidence for the sanctioned stack:
[workflow-visualization-tooling brainstorm](../ideation/brainstorm/workflow-visualization-tooling.md)
(sources checked, links retained).

## Sanctioned Stack (by role)

| Role | Tool | Use |
| --- | --- | --- |
| Generated read-only diagrams | Mermaid | Flow/state/sequence diagrams in docs, audit packets, reports — diffable source, no runtime dependency |
| Interactive validation canvas | React Flow (xyflow) | First-choice editable canvas: nodes, edges, comments, confidence, source links |
| Workflow state semantics | XState | Statechart model behind the canvas when simulation or executable checks are needed |
| Evidence and relationship graphs | Cytoscape.js | Source-to-step traces, variants, loops, bottleneck analysis |
| Collaborative annotation | Excalidraw | Whiteboard review and correction sessions; never authoritative |
| Graph layout | Dagre | Layout helper paired with React Flow or generated SVG |

A read-only need is served by Mermaid before any runtime tool is reached
for. React Flow is first-choice — not sole-choice — for editable views; a
replacement requires a delta to the `workflow-visualization` capability.

## Walkthrough View Coverage

The client validation walkthrough UI is accepted against nine views; each
Spec Kit feature names the views it delivers, and the walkthrough is not
complete until all nine exist:

1. current-state flow
2. target-state flow
3. current-to-target delta
4. evidence graph (which resources support each step)
5. role swimlane / responsibility view
6. approval gate view
7. exception path view
8. bottleneck and rework loop view
9. consent and acknowledgement view

Views consumed only in review or audit context are satisfied by their
Mermaid-generated read-only form.

## Relation To Other Standards

- [Avatar-First UI Standard](avatar-first-ui-standard.md) — interaction
  surface, personas, safety; this standard never overrides it.
- `workflow-visualization` capability
  ([spec](../openspec/changes/adopt-workflow-visualization-stack/specs/workflow-visualization/spec.md)
  until promoted) — the normative requirements behind this doc.
- Future validation-UI implementation is codexFactory Spec Kit feature work,
  accepted against the nine views above.
