# Subject-Aware Chat Feedback Loop — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The dashboard chat should bind a subject field, conversation,
selected model, source snapshot, and current human-edited draft into an
explicit next-turn envelope.
Topics: dashboard-workbench, ideation-dashboard, document-chat, subject, model-selector
Repository context: openxFactory dashboard workbench and AI document editing
Captured: 2026-07-28

## Possible feats

- **Workbench chat composer** — subject field, chat input, model selector,
  context preview, and explicit send action.
- **Draft-aware next turn** — include the exact human-edited draft revision
  and change summary in the next AI request.
- **Turn provenance panel** — show model, subject, source revision, draft
  revision, selected context, and response application status.

## Focus

This document isolates how chat and human edits become another AI turn. The
AI must receive what the user actually changed, not a stale document snapshot
or an unbounded repository dump.

## Proposed model

Each send creates a turn envelope containing:

- stable conversation and turn identities;
- a required or explicitly inherited subject;
- user message;
- selected model and permitted generation settings;
- selected repository, ref, document, and source revision;
- current draft revision plus a human-change summary or patch;
- bounded supporting context and why it was selected;
- requested output mode: advice, outline proposal, document patch, or full
  draft replacement.

The response records proposed operations against the input draft revision.
The user previews and accepts, edits, or rejects them. Accepted edits become a
new draft revision and therefore input to a later turn.

## Interfaces and boundaries

The chat composer reads the draft owned by the
[Integrated Editor Canvas](dashboard-workbench-integrated-editor-canvas.md).
It emits a model request and proposed draft operations. It does not commit
the document or execute ideation gate actions.

The subject field is semantic focus, not hidden authority. Changing it must
not silently switch tenant, repository, project, or document scope.

## Alternatives and tensions

- Automatically sending every keystroke gives continuous collaboration but
  creates cost, privacy, and unstable-turn problems.
- Sending only a full document is simple but hides what the person changed.
- Sending only a patch is efficient but may omit necessary surrounding
  meaning.
- A global model selector is convenient; per-turn selection is more
  reproducible and visible.

## Open questions

- Is subject required on the first turn and inherited thereafter?
- Which models are eligible for advice versus document mutation proposals?
- How much draft context accompanies a small outline edit?
- Can one response propose edits to both outline structure and document prose?
- When is an accepted AI operation automatically applied versus previewed?

## Relationships

The complete human-edit → AI-turn → preview → accept cycle is described in
[Collaborative Document Turns](dashboard-workbench-synthesis-collaborative-document-turns.md).
