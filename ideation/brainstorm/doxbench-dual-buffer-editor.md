# doxBench Dual-Buffer Editor — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can keep outline material and the active document as separate browser-local buffers so humans and models can reason about both without silently conflating or persisting them.
Topics: doxbench, dual-buffer-editor, ideation-dashboard, document-editing, doc-workflow
Repository context: openxFactory doxBench authoring canvas and branch-backed document workflow
Captured: 2026-07-28

## Possible feats

- **Two-buffer Markdown canvas** — Edit and preview the outline and active document independently while preserving cursor, selection, scroll, focus, and dirty state.
- **Honest outline creation** — Offer an explicit new-outline path when a scope has no declared outline instead of manufacturing one from document headings.

## Focus

This document isolates the local editing model. An outline is topic or fragment
material; it is not necessarily a table of contents for the active document.
The two artifacts therefore need distinct identity, state, and save decisions.

## Proposed model

Each buffer records its kind, optional repository-relative path, repository,
base ref and revision, base content hash, current content and hash, and dirty
state. `Outline` loads declared outline material when it exists. `Document`
loads the active document selected from the scoped document set or starts from
an explicit create flow.

Typing and local proposal application change only the current buffer. Discard
restores the last loaded or saved base. Save compares base and current hashes
before asking the governed persistence path to create or edit the backing
artifact.

Both buffers use an accessible Markdown source control and the existing
sanitized preview path. A document switch with dirty content pauses for an
explicit save-or-discard choice.

## Interfaces and boundaries

The editor consumes source content and revisions from the active repository/ref
and exposes complete current buffer descriptors to grounded chat. It receives
typed proposals only through the proposal-review mechanism and sends dirty
backed buffers only through governed Save.

The editor does not derive an outline from headings, autosave keystrokes,
silently replace dirty content, create a multi-document write verb, or treat a
browser buffer as committed corpus state.

## Alternatives and tensions

- A single document buffer with a generated heading outline reduces state, but
  destroys independent outline meaning.
- Autosave improves continuity, but creates noisy commits and erases the
  deliberate boundary between exploration and persistence.
- A rich block editor may improve authoring later, but the current static
  no-bundler dashboard makes a local Markdown control the lower-risk first
  realization.

## Open questions

- What buffer size makes full-document editing uncomfortable enough to warrant
  a deliberate bounded-selection mode?
- Should discard be per-buffer only, or should the shell also offer a clearly
  labelled discard-all action?
- Which editor abstraction would permit a future rich editor without changing
  hashes, proposal semantics, or save authority?

## Relationships

- The [surface and scope](doxbench-surface-and-scope.md) places the two buffers
  in their dashboard context.
- [Typed proposal review](doxbench-typed-proposal-review.md) explains how AI
  output may replace one local buffer.
- [Governed persistence](doxbench-governed-persistence.md) owns the boundary
  between a dirty buffer and a branch commit.
- The [human/AI loop synthesis](doxbench-synthesis-human-ai-authoring-loop.md)
  relates editing, chat, and proposal review.
