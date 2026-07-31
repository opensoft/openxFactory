# doxBench Governed Persistence — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can persist reviewed buffers through existing branch-session create and edit actions while keeping the served checkout and main-resident documents outside its direct write authority.
Topics: doxbench, governed-persistence, ideation-dashboard, branch-session, gate-actions
Repository context: openxFactory dashboard governance and branch-backed document persistence
Captured: 2026-07-28

## Possible feats

- **First-save session materialization** — Create or join the tile's branch
  session atomically when the first eligible save edits existing owned
  material.
- **Exact partial-save recovery** — Preserve and explain the committed first
  buffer when the second of two ordered save actions refuses.

## Focus

This document isolates when doxBench working state becomes repository state.
Editing, chatting, and Apply remain non-mutating. Save is the deliberate seam
that invokes existing human-only gate actions.

## Proposed model

Save compares each dirty buffer with its base and routes a new path through
`create-document` or an existing path through `edit-document`. If no branch
session exists, an eligible first edit atomically materializes or joins the
tile's session and writes only inside its worktree.

When both buffers are dirty and backed, outline saves before document. Each
uses one existing action and produces its own commit and gate-action record.
After success, the session snapshot refreshes and the returned content,
revision, and hash become the new buffer base.

If the second action fails, the first commit stands, its buffer advances, the
second stays dirty, and the UI reports both outcomes. Failure during first-save
materialization leaves no orphan worktree, registry entry, record, or commit.

## Interfaces and boundaries

Persistence consumes an authorized local-console Save, scoped owned paths,
base ref/revision/hash, and current buffer content. It emits ordinary
branch-session commits and refresh state.

It grants no delete, merge, approval, lifecycle transition, inherited-context
edit, direct `main` write, or history-rewrite authority. Main-resident editing
outside integrated branch-backed authoring retains the existing redline or
external-editor path.

## Alternatives and tensions

- One transaction for both buffers would simplify the success story, but would
  invent a new multi-document governance verb.
- Rolling back a successful first commit after a second failure looks atomic,
  but rewrites evidentiary history.
- Autosave would reduce the chance of browser loss, but would turn exploratory
  keystrokes into governed commits without a deliberate human boundary.

## Open questions

- Should a future batch gate action be proposed if multi-document authoring
  becomes common enough to justify a new audited contract?
- How should session refresh failures be represented when the underlying save
  committed successfully?
- What recovery affordance best helps a human resume after an exact partial
  save without implying rollback?

## Relationships

- The [dual-buffer editor](doxbench-dual-buffer-editor.md) supplies dirty
  buffers and receives refreshed bases.
- [Typed proposal review](doxbench-typed-proposal-review.md) precedes Save but
  holds no persistence authority.
- The [surface and scope](doxbench-surface-and-scope.md) defines which material
  is owned versus inherited context.
- The [governed runtime synthesis](doxbench-synthesis-governed-runtime.md)
  relates persistence to the local-plane and provider boundaries.
