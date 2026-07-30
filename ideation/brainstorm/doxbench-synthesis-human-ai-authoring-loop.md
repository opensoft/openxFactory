# Synthesis: doxBench Human/AI Authoring Loop — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The doxBench authoring loop becomes coherent when scoped context, two current buffers, grounded conversation, and hash-bound proposal review remain distinct but continuously feed one another.
Topics: doxbench, human-ai-authoring-loop, surface-and-scope, dual-buffer-editor, grounded-chat, typed-proposal-review, synthesis
Repository context: openxFactory doxBench interactive authoring experience
Captured: 2026-07-28

## Possible feats

- **Continuous reviewed authoring loop** — Move from context to edit to model
  discussion to reviewed local proposal and back to editing without leaving
  doxBench or prematurely persisting work.
- **Turn-grounding inspector** — Let a human verify the scope, buffer hashes,
  and working-state labels a completed turn actually used.

## Members and their joints

Atomic members:
[surface and scope](doxbench-surface-and-scope.md),
[dual-buffer editor](doxbench-dual-buffer-editor.md),
[grounded chat](doxbench-grounded-chat.md), and
[typed proposal review](doxbench-typed-proposal-review.md).

```text
tile scope -> current buffers -> bounded model turn -> typed proposal
    ^              |                                      |
    |              +--------- human edits ----------------+
    +---------------- current context remains visible -----+
```

### Context establishes meaning without becoming an edit target

The surface supplies owned, cited, and inherited documents plus the scoped
keyword lens. The editor selects exactly one active document and one independent
outline buffer from that context. Keeping these roles separate prevents
document discovery from being confused with write authority.

### Current buffers become turn evidence

The chat request takes the complete buffer state that exists at submission
time, including unsaved human changes and locally applied proposals. Hashes
connect the response to that exact evidence while working-state labels prevent
the model or UI from claiming it was already committed.

### Proposal review closes the feedback loop

Assistant prose remains conversation. A typed, hash-bound proposal may replace
one local buffer only after a human Apply gesture. The edited buffer then
becomes the input to the next turn, so the loop advances without pretending the
model wrote a repository artifact.

## Emergent behavior

Together, the four parts create a workspace where human and model can iterate
over the same evolving outline and document while the human retains control of
both action and persistence. None of the atomics alone can guarantee that the
next turn sees the actual current draft and that late output cannot erase newer
work.

## Tensions to hold

- Full-buffer grounding is honest but constrained by model/request budgets.
- Ephemeral browser conversation protects governance boundaries but limits
  collaboration and cross-device continuity.
- Complete-content proposals are easy to validate but potentially unwieldy for
  large documents.
- A responsive three-region loop must retain focus and editor state as layout
  changes.

## Recombination opportunities

- Combine turn-grounding evidence with the existing document-health signals so
  a future model can discuss a named finding without changing who owns the
  score.
- Combine explicit bounded selections with diagram or formal-document
  generation from the broader AI editor product.
- Combine proposal comparison with accessible review patterns from the
  existing gate console while keeping Apply local.

## Open questions

- What visible evidence gives users confidence about exactly what the model saw?
- How should large-document selection work without weakening full-buffer
  honesty?
- Which collaboration needs belong in doxBench versus the broader standalone
  editor product?
