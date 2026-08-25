# Synthesis: Collaborative Document Turns — Brainstorm

Status: brainstorm
Kind: process
Summary: A shared Outline/Document canvas and draft-aware chat envelope form
an explicit loop in which human edits become model input and AI edits remain
reviewable draft operations.
Topics: dashboard-workbench, integrated-editor, document-chat, draft-revision, synthesis
Repository context: openxFactory dashboard workbench
Captured: 2026-07-28

## Possible feats

- **Collaborative document turn engine** — coordinate draft revisions,
  outline projection, chat context, model responses, preview, acceptance, and
  conflict handling.
- **Human/AI change ledger** — retain authorship and base revision for every
  draft operation without treating draft history as a Git commit history.

## Members and their joints

Atomic members:
[Integrated Outline and Document Editor Canvas](dashboard-workbench-integrated-editor-canvas.md)
and [Subject-Aware Chat Feedback Loop](dashboard-workbench-chat-feedback-loop.md).

### Human editing advances the draft

The user edits either the outline or full document. The shared buffer produces
a new draft revision and a normalized change summary. The other projection
updates from the same state.

### Send freezes a turn input

Submitting the chat captures the subject, message, model, source snapshot, and
exact draft revision. Later typing advances the local draft but cannot change
the already-running turn's input.

### AI output is a proposal against a base

The response returns advice or structured edit operations tied to the sent
revision. If the local draft advanced, the workbench previews a rebase or
conflict rather than overwriting newer human work.

### Acceptance closes one loop, not the document lifecycle

Accepted operations create another draft revision. The next chat turn uses
that result. Saving or promoting the document remains a separate action with
its own branch, proposal, and gate rules.

## Emergent behavior

The user and model can take repeated, provenance-bearing turns over one
artifact while outline and full-document editing remain interchangeable entry
points.

## Tensions to hold

- Low-friction automatic application improves flow but weakens review.
- Rich turn provenance aids reproducibility while increasing retained
  conversation data.
- Rebase support is essential for concurrency but may be difficult for
  semantic outline operations.

## Recombination opportunities

The loop can launch from the keyword Lens, attach topic-compilation context,
and later hand accepted drafts to a branch session without giving chat direct
Git authority.

## Open questions

- What operation format spans raw text and structural outline edits?
- How long is draft and turn history retained?
- What is the UX for partial acceptance of a response?
- Which conflicts require returning to the Document tab?
