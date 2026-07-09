# Design: Adopt Workflow Visualization Stack

## Decision 1: Ratify the shortlist as-is

The staged fragment's license verification (sources checked 2026-07-02, links
retained in the brainstorm) stands. No new evaluation round: the risk this
change retires is unreviewed dependency drift, not tool optimality — the
stack can be revised by a later delta if implementation experience demands.

## Decision 2: Roles, not a single tool

Each tool is sanctioned FOR a role (read-only generation, editable canvas,
state semantics, evidence graphs) rather than blessing a toolbox loosely.
This keeps "use Mermaid for docs" enforceable while leaving React Flow the
default — not the only — canvas ("first-choice" wording).

## Decision 3: Nine views are acceptance criteria, not architecture

The view list binds feature acceptance (each feat names its views; the
walkthrough completes at nine) without constraining information architecture
or navigation, which belong to the avatar-first UI standard and the eventual
Spec Kit design work.
