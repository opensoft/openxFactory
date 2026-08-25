# Dashboard Integrated Document Workbench Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The dashboard workbench is proposed as a subject-aware chat and
document collaboration surface with a shared Outline/Document canvas,
revisioned human and AI turns, and explicit handoff to governed actions.
Topics: dashboard-workbench, ideation-dashboard, workbench, integrated-editor, document-chat
Repository context: openxFactory dashboard and document-workflow evolution
Captured: 2026-07-28

## Possible feats

- **Integrated document editor chat** — one workbench containing subject,
  conversation, model selector, Outline/Document tabs, draft history, and
  response preview.
- **Branch-session handoff** — move an accepted draft into a governed branch
  session without giving the model direct merge or promotion authority.

## Motivation

The dashboard can discover and organize ideation, but document refinement
still fragments across viewers, external editors, chat, and branch tools.
Users need to edit the rendered structure or full artifact, feed those exact
changes back to the AI, and take another turn without losing provenance.

## Goals

- Present one editable draft through Outline and Document tabs.
- Keep subject, message, model, source snapshot, and draft revision visible.
- Feed human edits into the next AI turn explicitly.
- Treat AI changes as previewable operations against a known base.
- Preserve the external-editor path for main-resident documents.
- Separate collaborative drafting from commit, proposal, and gate authority.

## Non-goals

- Chat cannot merge, promote, stage, or approve documents.
- The outline is not a second independent document.
- Subject selection does not grant repository or tenant access.
- V1 need not round-trip every document format.
- This packet does not replace the existing dashboard or workbench proposals.

## What the system delivers

A user selects a document and subject, edits either its structure or prose,
chooses a model, sends a message with the current draft revision, previews the
response, applies selected changes, and repeats. The complete chain retains
source and turn provenance.

## System model

```text
repository/ref/document snapshot
  → revisioned draft buffer
  ↔ Outline tab / Document tab
  → subject + message + model + exact draft revision
  → AI advice or edit operations
  → preview / accept / edit / reject
  → next draft revision and next turn
  → explicit save or branch-session handoff
```

## Cluster map

- [Collaborative Document Turns](dashboard-workbench-synthesis-collaborative-document-turns.md)
  — joins the shared canvas to the draft-aware conversation loop.

## How it fits

This packet extends rather than silently amends the active dashboard and
workbench changes. Relevant context includes
[Ideation Dashboard](../../openspec/changes/archive/2026-07-29-add-ideation-dashboard/proposal.md),
[Staging Workbench](../../openspec/changes/archive/2026-08-01-add-staging-workbench/proposal.md),
[Workbench Branch Sessions](../../openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/proposal.md),
[Dashboard Repository Selector](../../openspec/changes/archive/2026-08-01-add-dashboard-repo-selector/proposal.md),
and [Ideation Intent Plane](../../openspec/changes/add-ideation-intent-plane/proposal.md).
Accepted product behavior should become an explicit OpenSpec delta before
implementation.

## Key decisions and open questions

The main decision is whether Outline and Document remain projections of one
source buffer; this packet recommends yes. Open issues include supported
formats, structural operation encoding, partial response acceptance, model
eligibility, turn retention, and branch-session save semantics.

## Document map

### Synthesis

- [Collaborative Document Turns](dashboard-workbench-synthesis-collaborative-document-turns.md)

### Atomic explorations

- [Integrated Outline and Document Editor Canvas](dashboard-workbench-integrated-editor-canvas.md)
- [Subject-Aware Chat Feedback Loop](dashboard-workbench-chat-feedback-loop.md)

### Related active leaves

- [Brainstorm Session Launch](lens-brainstorm-session-launch.md)
- [Keyword Search and Ad-Hoc Keywords](lens-keyword-search-and-adhoc.md)
- [Ring Combination Explorer](lens-ring-combination-explorer.md)
- [Topic Compilation Tree](topic-compilation-tree.md)
