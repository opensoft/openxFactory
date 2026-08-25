# Integrated Outline and Document Editor Canvas — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The dashboard workbench should expose one editable draft through
Outline and Document tabs so users can revise either representation without
creating competing sources of truth.
Topics: dashboard-workbench, ideation-dashboard, integrated-editor, outline, document-canvas
Repository context: openxFactory dashboard workbench and main-resident documents
Captured: 2026-07-28

## Possible feats

- **Outline/Document canvas tabs** — switch one workbench canvas between a
  rendered hierarchical outline and the full editable document.
- **Bidirectional draft projection** — reconcile edits from either tab into
  one revisioned document state with visible conflicts and validation.
- **Main-resident external-editor action** — retain the existing escape hatch
  for documents better handled in a local editor.

## Focus

This document isolates the canvas where a person reads and edits the artifact
being discussed with the AI. The key design requirement is not two editors;
it is one draft with two projections.

## Proposed model

The workbench owns a revisioned draft buffer:

- **Outline tab** renders headings and bounded section summaries as a tree.
  Users may rename, reorder, add, remove, or edit outline nodes.
- **Document tab** renders the full source and supports direct document edits.
- Each edit produces a draft operation against a known base revision.
- A projection service updates the other view and reports information loss or
  structural ambiguity instead of silently rewriting.
- Save, discard, compare, and external-editor actions remain explicit.

The outline is a structural projection, not an independent stored artifact.
For Markdown, heading identity needs a stable internal key so a title edit
does not appear as delete-plus-create.

## Interfaces and boundaries

The canvas consumes a selected repository/ref/document snapshot and emits
draft revisions. It does not commit, stage, promote, or merge documents.
Those actions remain governed by the existing workbench and gate surfaces.

Related active leaves:
[Brainstorm Session Launch](lens-brainstorm-session-launch.md),
[Keyword Search and Ad-Hoc Keywords](lens-keyword-search-and-adhoc.md),
[Ring Combination Explorer](lens-ring-combination-explorer.md), and
[Topic Compilation Tree](topic-compilation-tree.md).

Related staged work:
[Workbench Branch Sessions](../staging/workbench-branch-sessions/workbench-branch-sessions.md)
and [Ideation Action Plane](../staging/ideation-action-plane/ideation-action-plane.md).

## Alternatives and tensions

- **Shared source buffer** is simplest, but outline edits need robust
  structural transforms.
- **Separate outline model with round-trip conversion** enables richer
  planning but creates synchronization and loss risks.
- **WYSIWYG document editing** improves accessibility while raw Markdown
  preserves exact source control.
- Immediate cross-tab projection feels responsive; explicit reconciliation
  gives clearer conflict control.

## Open questions

- Which document formats support safe outline round-tripping in v1?
- Are outline node moves represented as source patches or semantic operations?
- When an AI turn changes the draft, how are simultaneous human edits rebased?
- Does saving create a branch-session commit, a workbench draft, or both?

## Relationships

The [Chat Feedback Loop](dashboard-workbench-chat-feedback-loop.md) consumes
the current draft revision as turn input. Their joint behavior is described
in [Collaborative Document Turns](dashboard-workbench-synthesis-collaborative-document-turns.md).
