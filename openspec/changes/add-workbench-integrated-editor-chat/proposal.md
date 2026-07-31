---
code_surface: codexFactory (the ideation-dashboard doxBench shell, editable outline/document canvas, chat rail, same-origin turn routes, model-provider adapter, branch-session save/apply integration, and tests), openxFactory (the ideation-dashboard contract delta and chat-turn schemas)
target_release: next additive contract bundle after the five predecessor dashboard changes archive
status: proposed
---

## Why

The dashboard workbench has the right pieces but not the authoring loop they
were meant to become. This change names its integrated authoring evolution
**doxBench**. The inherited surface can render a scoped outline, open documents,
create a document, and safely edit branch-session material, while the older
AI-editor concept separately specifies inline/side-panel AI and model choice;
the human still has to leave the surface or mentally shuttle changes between
those pieces.

This change joins them into one governed loop: edit the outline or document in
the doxBench canvas, discuss the current buffers with a selected model, apply an AI
proposal only by an explicit human gesture, and use the resulting buffers as
the exact input to the next turn.

The non-normative
[doxBench brainstorm packet](../../../ideation/brainstorm/doxbench-overview.md)
preserves the underlying ideas as atomic and synthesis documents for later
recombination. This change remains the authority for proposed scope,
requirements, dependencies, and realization.

## What Changes

- NAME the integrated dashboard workbench **doxBench** in product copy,
  documentation, accessibility labels, and realization evidence. Existing
  technical identifiers (`ideation-dashboard`, `staging workbench`,
  `workbench-chat-turn`, routes, schemas, and branch-session records) remain
  stable; the name does not create a second capability or migrate persisted
  data.
- Replace the staging workbench's read-only authoring area with the doxBench
  desktop surface while retaining its scoped `docs` and `lens` context:
  - an editable canvas with `Outline` and `Document` tabs;
  - a chat rail containing a **Working subject** field, transcript, model
    selector, and message composer;
  - an explicit active-document selector sourced from doxBench's scoped
    document set.
- Treat the outline and active document as two independently editable buffers.
  The outline is seeded from the scope's existing outline material when it
  exists; the document is the selected or newly created corpus document.
  Neither buffer is silently treated as the other or silently persisted.
- On every chat submission, ground the turn on the current working subject,
  conversation, outline buffer, document buffer, scope metadata, active
  repository/ref, and content hashes. Unsaved human edits are therefore visible
  to the next AI turn without first becoming governed corpus state.
- Return normal assistant prose plus optional typed proposals for the outline,
  document, or both. AI output never writes a file. A human may apply a proposal
  to an editor buffer, inspect it, and then save it through the existing
  branch-session `create-document` / `edit-document` path.
- Refuse a stale proposal when either target buffer changed after the turn was
  issued. The human may keep the newer buffer, re-run the turn, or explicitly
  replace it after reviewing the current and proposed text; there is no silent
  merge.
- Make persistence batch-based rather than keystroke-based. Chat turns and
  buffer edits are non-mutating; **Save** creates one existing gate-action
  commit per changed corpus document, refreshes the session snapshot, and
  advances the grounding revision. No autosave commit occurs per keypress.
- Expose model choices from a server-side allowlist. Provider credentials and
  raw provider configuration never enter browser state, chat payloads, git, or
  dashboard snapshots. The initial provider adapter reuses the family's
  rider/subscription-primary and zero-retention hosted-fallback posture where
  available, but chat remains unavailable rather than weakening the configured
  data-handling policy.
- Keep v1 local-plane and branch-backed for persistence. The human may edit
  buffers and chat before a branch exists, but no existing `main` document is
  mutated: the first Save materializes/joins the tile's session and applies the
  existing create/edit gate action there. The hosted dashboard retains the
  existing read-only doxBench posture until a separately governed hosted identity,
  model broker, and write-apply lane exist.
- Rename the free-form UI control **Working subject** in contracts and copy so it
  cannot be confused with a customer `subject_ref`, authenticated actor, tenant,
  or any identity-bearing subject field.
- Preserve the current external-editor escape hatch for main-resident documents
  and unsupported local editors. The integrated editor does not weaken the
  existing `edit-apply` path or grant in-workbench mutation of `main`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `ideation-dashboard`: evolve the staging workbench into **doxBench**, changing
  the read-only `docs / lens / outline` viewer into a branch-session authoring surface with an
  `Outline / Document` editable canvas, integrated grounded chat, server-declared
  model selection, explicit human application, stale-output protection, and
  save-through-existing-gates semantics.

## Impact

- **Governed implementation-start exception (Brett, 2026-07-29)**:
  `add-ideation-dashboard`, `add-propose-verb`, `add-staging-workbench`,
  `add-workbench-bullseye-and-create`, `add-dashboard-repo-selector`, and
  `add-workbench-branch-sessions` still owe their remaining contract
  registration/live acceptance work and dependency-ordered archive. Their
  codexFactory realizations are already merged, but the `ideation-dashboard`
  capability is not yet promoted under `openspec/specs/`. Brett explicitly
  approved starting the doxBench Speckit/code lane without cutting a one-item
  predecessor contract bundle first. This exception starts implementation
  only: it does not close those tasks, permit this change to archive against an
  unpromoted capability, or permit doxBench realization to merge before its
  own contract package is registered and pinned.
- **Immediate code baseline**: codexFactory `008-fix-dashboard-edit` landed
  through PR #56 as merge commit `d2c16b1` and is included in the recorded
  common baseline `34bfc2f`. Its select-to-edit action remains the
  main/outside-session editor escape hatch and gives this feature one stable
  viewer edit seam to preserve.
- **openxFactory**: a MODIFIED `ideation-dashboard` delta; additive JSON Schemas
  for the model catalog, chat-turn request/response, buffer hashes, and typed AI
  proposals; examples and validation coverage; contract manifest registration
  at the eventual release cut.
- **codexFactory**: doxBench editor/chat view modules; a same-origin local
  backend route; a model allowlist and provider adapter; bounded context
  assembly; sessionStorage transcript state; save/apply wiring through existing
  branch-session ports; renderer-boundary, confinement, stale-turn, privacy,
  accessibility, and browser acceptance tests.
- **No required dependency** on the standalone generation-engine lane, realm
  integrations, NotebookLM, or a hosted chat broker. They may become additional
  context/tools later but are not allowed to block the local doxBench loop.
- **Compatibility**: hosted and gate-off surfaces stay read-only; existing
  snapshots remain valid; existing `docs`, `lens`, viewer, create, external-edit,
  session, and pull-request flows remain available. No existing document is
  rewritten merely by opening doxBench or sending a chat turn.
