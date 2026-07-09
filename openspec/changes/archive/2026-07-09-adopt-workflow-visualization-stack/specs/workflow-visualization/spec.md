## ADDED Requirements

### Requirement: Sanctioned visualization stack
Workflow-contract visualization SHALL use the sanctioned MIT-licensed stack:
Mermaid for generated read-only diagrams, React Flow (xyflow) for the
interactive validation canvas, XState for workflow state semantics and
transition simulation, and Cytoscape.js for evidence and relationship
graphs, with Excalidraw (collaborative annotation) and Dagre (graph layout)
as supporting tools. Tools whose current license is not MIT — including
bpmn-js, JointJS, and GoJS — SHALL NOT be adopted without a separate
ratified license decision.

#### Scenario: A read-only workflow diagram is generated
- **WHEN** documentation, an audit packet, or a report needs a workflow, state, or sequence diagram
- **THEN** it MUST be produced as Mermaid source so the artifact is diffable and renderable without a runtime dependency

#### Scenario: An editable validation canvas is built
- **WHEN** a validation UI lets a client walk through, correct, or annotate a workflow definition
- **THEN** React Flow MUST be the first-choice canvas, with XState backing the workflow state model when simulation or executable checks are needed

#### Scenario: A new visualization dependency is proposed
- **WHEN** any visualization library is proposed for adoption
- **THEN** its current project source or package metadata MUST declare an MIT license, verified at adoption time including transitive dependencies and commercial-use terms
- **AND** a non-MIT tool requires its own ratified decision before use

### Requirement: Walkthrough view coverage
The client validation walkthrough UI SHALL support the nine ratified views:
current-state flow, target-state flow, current-to-target delta, evidence
graph, role swimlane, approval gate view, exception path view, bottleneck
and rework loop view, and consent and acknowledgement view. These views are
the acceptance checklist for validation-UI feature work.

#### Scenario: A validation UI feature is accepted
- **WHEN** a Spec Kit feature implements part of the validation walkthrough
- **THEN** its acceptance criteria MUST name which of the nine views it delivers
- **AND** the walkthrough is not complete until all nine views exist

#### Scenario: A view only needs read-only rendering
- **WHEN** a view is consumed in review or audit context without editing
- **THEN** the Mermaid-generated form of that view satisfies the coverage requirement
