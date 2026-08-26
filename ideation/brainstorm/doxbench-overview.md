# doxBench Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: doxBench is the proposed human-facing dashboard workspace that joins scoped document context, dual-buffer Markdown editing, grounded model conversation, reviewed AI proposals, and branch-governed persistence.
Topics: doxbench, ideation-dashboard, workbench, doc-management, doc-workflow
Repository context: openxFactory cross-factory dashboard experience with codexFactory realization
Captured: 2026-07-28

## Possible feats

- **Integrated doxBench v1** — Deliver the complete local loop from scoped
  context through editing, grounded chat, reviewed Apply, governed Save, and
  branch-session continuation.
- **Hosted governed doxBench** — Add hosted identity, tenant-aware model
  brokerage, data policy, and write application only through a separately
  approved successor.

## Motivation

The dashboard workbench can already show scoped documents and relationships,
and its branch-session lineage can create and edit governed material. The
earlier AI document-editor brainstorm separately imagines inline and side-panel
model assistance. Without one joined surface, a human must shuttle context,
drafts, and model output between tools and cannot be sure the next turn sees
the current unsaved work.

This packet reorganizes that design into a recombinable, non-normative graph.
The active
[OpenSpec change](../../openspec/changes/add-workbench-integrated-editor-chat/proposal.md)
remains the authority for proposed requirements, decisions, prerequisites, and
implementation tasks.

## Goals

- Give a human one named workspace for scoped context, outline/document
  editing, and model discussion.
- Make every turn reflect the exact current buffers, including unsaved edits.
- Keep AI output advisory until a human applies a typed proposal locally.
- Preserve a separate deliberate Save through existing branch-session gates.
- Keep model credentials and routing policy server-side.
- Degrade honestly to editor-only or read-only modes when capabilities are
  absent.

## Non-goals

- Autonomous model writes, direct changes to `main`, autosave commits, delete,
  merge, approval, or lifecycle-transition authority.
- Real-time multi-cursor collaboration or conflict-free replicated editing.
- Rich Office/Google document editing, realm add-ins, or replacement of the
  broader standalone AI document-editor product.
- Mandatory NotebookLM grounding, hosted chat, or a general family-wide model
  gateway.
- Renaming stable `ideation-dashboard`, `workbench-*`, route, schema, module,
  or branch-session identifiers merely to match the product name.

## What the system delivers

doxBench presents a context region for the active tile's `docs` and `lens`, an
authoring canvas with independent `Outline` and `Document` buffers, and a chat
rail with Working subject, transcript, server-declared model choice, and
composer.

A turn contains the current buffers and their hashes. A valid response contains
assistant prose and may contain typed outline or document proposals. Human
Apply changes only a browser buffer; stale hashes refuse. Human Save uses
existing create/edit gate actions in a branch session, after which refreshed
repository state grounds further work.

## System model

```text
dashboard tile and source
          |
          v
 scoped docs/lens context ---> Outline + Document buffers
                                      |
                         current text and hashes
                                      v
 server-confined model turn ---> prose + typed proposals
                                      |
                              human review / Apply
                                      |
                              explicit human Save
                                      v
                   existing branch-session gate actions
```

The model path and write path remain separate. The local browser may hold
ephemeral working state, but governed corpus state changes only through the
existing human gate boundary.

## Cluster map

- [Human/AI authoring loop](doxbench-synthesis-human-ai-authoring-loop.md) —
  relates context, current buffers, grounded turns, and proposal review into one
  iterative workspace.
- [Governed runtime](doxbench-synthesis-governed-runtime.md) — relates scope
  confinement, model-provider policy, branch-backed persistence, and honest
  deployment degradation.

## How it fits

doxBench is the exact product name for the integrated authoring evolution of
the `ideation-dashboard` staging workbench, not a new capability or protocol
namespace. It reuses dashboard scope, health, and lens projections; the
branch-session worktree; existing `create-document` and `edit-document` gates;
and the external-editor escape hatch.

openxFactory owns the cross-factory contract and this brainstorm packet.
codexFactory is expected to realize the dashboard UI, local backend routes,
provider adapter, save wiring, and tests after the predecessor change chain is
promoted and the active change is ratified. The broader standalone AI
document-editor vision remains separate design history in codexFactory.

## Key decisions and open questions

The current proposal selects exact `doxBench` casing, a three-region shell, two
independent buffers, explicit Save, full current-buffer grounding, typed
hash-bound proposals, a server-declared model catalog, local-console chat, and
stable legacy technical identifiers.

Implementation constants such as request limits and responsive breakpoints
remain to be calibrated. Successor questions include bounded-selection
grounding, collaboration, richer editing, shared model infrastructure,
multi-document save contracts, and the prerequisites for hosted authoring.

## Document map

### Syntheses

- [Human/AI authoring loop](doxbench-synthesis-human-ai-authoring-loop.md)
- [Governed runtime](doxbench-synthesis-governed-runtime.md)

### Atomic documents

- [Surface and scope](doxbench-surface-and-scope.md)
- [Dual-buffer editor](doxbench-dual-buffer-editor.md)
- [Grounded chat](doxbench-grounded-chat.md)
- [Typed proposal review](doxbench-typed-proposal-review.md)
- [Governed persistence](doxbench-governed-persistence.md)
- [Provider boundary](doxbench-provider-boundary.md)
