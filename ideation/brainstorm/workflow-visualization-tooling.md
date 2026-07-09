# Workflow Visualization Tooling Exploration

Status: staged
Organized: 2026-07-09 into
[adopt-workflow-visualization-stack](../../openspec/changes/archive/2026-07-09-adopt-workflow-visualization-stack/proposal.md);
kept as evidence (license sources checked).
Repository context: openxFactory
Purpose: capture MIT-licensed open source visualization candidates for the Client
Hermes user validation walkthrough.

## Selection Rule

Only treat a tool as a candidate when its current project source or package
metadata declares an MIT license. Recheck license, transitive dependencies, and
commercial-use terms before adding a dependency.

## Candidate Tools

| Tool | License signal found | Best fit for validation walkthrough | Notes |
| --- | --- | --- | --- |
| Mermaid | MIT license in project source | Generated flowcharts, state diagrams, sequence diagrams, and diffable documentation. | Best first pass for audit-friendly current/target workflow diagrams in Markdown. |
| React Flow / xyflow | Project says React Flow/xyflow is MIT licensed | Interactive workflow validation canvas with editable nodes, edges, comments, confidence, and source links. | Strong candidate for the main conventional visual editor. |
| Cytoscape.js | Project site says MIT for core and first-party extensions | Evidence graph, relationship graph, variants, loops, bottlenecks, and source-to-step trace visualization. | Better for graph analysis than linear process editing. |
| XState | MIT license in project source | Statechart-backed workflow semantics, transition simulation, and executable validation. | Good candidate for the underlying workflow state model, paired with another renderer. |
| Rete.js | Project/package declares MIT | Node-based workflow authoring or visual programming for advanced operators. | Heavier than React Flow; useful if workflows become composable executable blocks. |
| Excalidraw | MIT license in project source | Whiteboard-style review, annotation, meeting walkthroughs, and informal correction sessions. | Useful for collaboration; not authoritative by itself. |
| Dagre | GitHub project shows MIT license | Automatic directed graph layout for current/target workflows. | Layout helper, not a full UI. Could pair with React Flow or generated SVGs. |
| Drawflow | npm/jsDelivr package metadata shows MIT | Lightweight flow editor prototype. | Explore for simple install UI; likely less suitable for complex audited workflow validation. |

## Not On The MIT Shortlist

| Tool | Reason |
| --- | --- |
| bpmn-js | Useful BPMN renderer/modeler, but project metadata points to the bpmn.io license rather than MIT. Keep out of the MIT shortlist unless license review approves it. |
| JointJS | Community license is not MIT. Exclude unless a separate product/license decision is made. |
| GoJS | Commercial, not open source MIT. Exclude. |

## Recommended Exploration Order

1. Mermaid for generated read-only diagrams in docs and audit packets.
2. React Flow for interactive validation and correction of workflow definition
   packets.
3. XState for state/transition semantics when workflows need simulation or
   executable checks.
4. Cytoscape.js for evidence graphs and variant/bottleneck visualization.
5. Excalidraw for collaborative annotation during early user walkthroughs.

## Workflow Walkthrough Views

The validation UI should support these views:

- current-state flow
- target-state flow
- current-to-target delta
- evidence graph showing which resources support each step
- role swimlane or responsibility view
- approval gate view
- exception path view
- bottleneck and rework loop view
- consent and acknowledgement view

Mermaid can cover the read-only version of most views. React Flow should be the
first candidate for editable views. Cytoscape.js should be explored where the
source evidence graph is more important than the process sequence.

## Sources Checked

- Mermaid: https://github.com/mermaid-js/mermaid/blob/develop/LICENSE
- React Flow / xyflow: https://xyflow.com/open-source
- Cytoscape.js: https://js.cytoscape.org/
- XState: https://github.com/statelyai/xstate/blob/main/LICENSE
- Rete.js: https://retejs.org/
- Excalidraw: https://github.com/excalidraw/excalidraw/blob/master/LICENSE
- Dagre: https://github.com/dagrejs/dagre
- Drawflow: https://www.jsdelivr.com/package/npm/drawflow
- bpmn-js license note: https://github.com/bpmn-io/bpmn-js
