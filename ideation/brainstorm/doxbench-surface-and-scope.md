# doxBench Surface and Scope — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can turn one dashboard tile into a focused three-region authoring surface without changing how the dashboard derives scope, document health, or keyword relationships.
Topics: doxbench, surface-and-scope, ideation-dashboard, workbench, doc-workflow
Repository context: openxFactory ideation dashboard and its cross-factory document-authoring surface
Captured: 2026-07-28

## Possible feats

- **Responsive doxBench shell** — Present the same scoped context, authoring canvas, and chat rail across desktop and narrow layouts without losing state or keyboard reachability.
- **Scope provenance inspector** — Explain whether each visible document is owned material, cited evidence, inherited cluster material, or a cluster-neighbourhood document.

## Focus

This document isolates the question: what is doxBench a surface *over*?
The current proposal treats it as the named authoring evolution of the
dashboard's staging workbench, opened from exactly one cluster, possible, or
staged-topic tile.

## Proposed model

The proposed desktop shell has three coordinated regions:

```text
Context                 Authoring canvas              Chat rail
docs / lens             Outline | Document            Working subject
scope + active doc      source + preview              transcript + model
```

The context region reuses the dashboard's existing document edges, completeness
signals, and keyword-lens derivation. It does not recalculate health or invent a
new relevance score. The canvas owns the two editable targets. The chat rail
discusses the current canvas state.

`doxBench` is the exact human-facing name. Existing `ideation-dashboard`,
`workbench-*`, route, schema, and branch-session identifiers remain technical
compatibility surfaces rather than candidates for a cosmetic rename.

## Interfaces and boundaries

doxBench consumes the active repository/ref, tile identity, tile-derived
document set, declared outline material, completeness data, and keyword index.
It emits browser interaction and, only through separately authorized save
actions, branch-session changes.

The surface does not own document membership, health scoring, readiness,
lifecycle transitions, or the distinction between owned and inherited
material. Missing source access leaves the snapshot-derived context readable
and makes unavailable authoring capabilities explicit.

## Alternatives and tensions

- Treating `docs`, `lens`, `outline`, and `document` as four peer tabs is
  visually simpler, but confuses context browsers with authoring targets.
- A completely new doxBench capability could have cleaner internal names, but
  would fork the existing dashboard contract and require needless migration.
- A dense three-column desktop layout supports the complete loop, while narrow
  screens require careful stacking and focus restoration to preserve meaning.

## Open questions

- Which breakpoints and minimum region sizes keep all three regions useful?
- How much provenance explanation belongs inline versus in a details drawer?
- Should a future user be able to pin context from a neighbouring scope without
  changing the tile that owns the authoring session?

## Relationships

- The [dual-buffer editor](doxbench-dual-buffer-editor.md) defines the canvas
  inside this shell.
- The [grounded chat](doxbench-grounded-chat.md) defines the chat rail.
- The [governed runtime synthesis](doxbench-synthesis-governed-runtime.md)
  relates surface capability to local-plane authority and degradation.
- The governed continuation is the
  [integrated editor/chat design](../../openspec/changes/add-workbench-integrated-editor-chat/design.md).
