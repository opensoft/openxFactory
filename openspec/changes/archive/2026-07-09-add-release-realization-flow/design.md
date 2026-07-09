# Design: Add Release Realization Flow

## Decision 1: Codify the pilot, not a speculative model

Every rule here has a pilot precedent: realization archival (the checker
change, active through three failed runs), release-definition location
(the aggregation repo hosted the runner), and the scale rule (the checker
executed its own tasks — no DAG needed). The brainstorm's speculative
parts that the pilot did not exercise (multi-feat decomposition, batched
release branches, delta stacking) enter as rules with declared shape but
no claimed operational history.

## Decision 2: Front-matter over folders

`code_surface`/`target_release` live in proposal front-matter rather than
a registry: the change folder is already the unit of governance, the
declarations travel with it into the archive, and the doc-health run can
grep them (a future check family: active code-surface changes older than
N days without realization evidence).

## Decision 3: Failed-run archival is contested-class

The archive gate's teeth reuse the contested-finding machinery rather than
inventing new enforcement: archiving an unrealized code-surface change is
a deliberate-state change, so it requires an explicit disposition — which
makes violations visible in the regression diff.

## Decision 4: The flow visualization ships in the doc

The brainstorm's mermaid lifecycle diagram moves into the ratified doc —
first sanctioned use of the workflow-visualization standard's Mermaid rule
for a governance document.
