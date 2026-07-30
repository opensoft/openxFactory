# Synthesis: doxBench Governed Runtime — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench remains a governed dashboard surface when scope confinement, branch-backed persistence, and server-side model policy form separate fail-closed boundaries.
Topics: doxbench, governed-runtime, surface-and-scope, governed-persistence, provider-boundary, synthesis
Repository context: openxFactory doxBench local-console runtime and hosted degradation posture
Captured: 2026-07-28

## Possible feats

- **Capability-derived runtime posture** — Render local authoring, editor-only,
  or hosted read-only modes from available capabilities without showing
  disabled controls that imply authority.
- **Save-and-turn audit view** — Explain separately which model interaction
  occurred and which human gate action later persisted a buffer.

## Members and their joints

Atomic members:
[surface and scope](doxbench-surface-and-scope.md),
[governed persistence](doxbench-governed-persistence.md), and
[provider boundary](doxbench-provider-boundary.md).

```text
snapshot/source capability -> readable scoped surface
local model capability      -> confined chat turn
local gate capability       -> branch-session Save
hosted/gate-off posture     -> readable context, no implied authority
```

### Scope confinement precedes both disclosure and mutation

The tile-derived scope is not merely navigation. It is the common boundary for
which source content may enter a model turn and which owned document may reach a
save action. The server independently re-resolves this boundary rather than
trusting browser paths.

### Model authority and write authority never combine

The provider port may return prose and typed proposals but cannot call
`create-document` or `edit-document`. The persistence path accepts only an
explicit human Save and emits ordinary branch-session evidence. This separation
makes it possible to audit disclosure and mutation as different events.

### Degradation is a product posture

An empty model catalog leaves local editing useful. Missing local gate
capability leaves source content readable without edit controls. The hosted
plane remains read-only and offers no chat path until its identity, model
broker, data policy, and write application receive their own governance.

## Emergent behavior

These boundaries let doxBench provide a rich local authoring experience without
turning a model into an actor, moving the served checkout, or teaching the
browser provider secrets. The same shell can degrade honestly according to its
runtime capabilities instead of simulating authority with nonfunctional
buttons.

## Tensions to hold

- A local-console presence token demonstrates access to that console, not a
  stronger process identity.
- One commit per changed document preserves existing evidence but exposes
  partial success in a two-buffer save.
- The safest hosted posture delays functionality users may expect from a web
  dashboard.
- Server-side policy reduces browser flexibility and makes deployment
  configuration part of product readiness.

## Recombination opportunities

- Combine capability-derived posture with other dashboard tools that need
  honest hosted/local degradation.
- Reuse the narrow provider port only after another interactive consumer proves
  the shared abstraction.
- Generalize first-save branch materialization to other human-console editors
  if their scope and ownership checks are equally explicit.

## Open questions

- What stronger host identity should eventually replace the accepted
  local-console process residual?
- Which hosted prerequisites should be proposed together and which need
  independent changes?
- Would a future multi-document gate action improve evidence, or merely conceal
  useful per-document transitions?
