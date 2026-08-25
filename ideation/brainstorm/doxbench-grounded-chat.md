# doxBench Grounded Chat — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Each doxBench chat turn can be grounded on the exact current outline and document buffers, including unsaved edits, while clearly distinguishing working text from governed corpus state.
Topics: doxbench, grounded-chat, ideation-dashboard, working-subject, model-routing
Repository context: openxFactory doxBench chat-turn concept and local dashboard model interaction
Captured: 2026-07-28

## Possible feats

- **Current-buffer chat turn** — Let the next model turn see intervening human edits and locally applied proposals without requiring an early save.
- **Bounded-selection turn** — Add an explicit successor mode for oversized documents that identifies exactly which selection the model received.

## Focus

This document isolates what a doxBench conversation knows and how ephemeral
working text crosses the browser/server boundary. The central requirement is
honesty: the model may see unsaved text, but neither side may call that text
committed or governed.

## Proposed model

A versioned turn includes repository/ref and tile scope, active document path,
free-form `working_subject`, the new message, bounded prior transcript, selected
model id, a client turn id, and complete outline/document buffer descriptors
with text and hashes.

The server independently resolves repository, ref, tile, and allowed paths;
verifies hashes; enforces request and provider limits; and records which hashes
the model saw. One turn is in flight per conversation key. A repeated client
turn id is idempotent only when the content and hashes are identical.

Working subject, selected model, and bounded transcript remain browser-session
state keyed by repository/ref/tile. `working_subject` is prompt focus, never a
customer `subject_ref`, actor, patient, tenant, or authority-bearing identity.

## Interfaces and boundaries

Grounded chat consumes both current buffers and scope metadata, then emits
assistant prose and optional typed proposals. It does not read credentials from
the browser, persist a shared conversation, mutate either buffer, call a gate
verb, or silently truncate a document to fit a model.

Provider or response-validation failure returns a fixed redacted error. Logs
and errors must not expose credentials, provider payloads, prompts, corpus
content, or unsaved text.

## Alternatives and tensions

- Server-side worktree reads are simpler, but omit precisely the unsaved human
  changes the author wants to discuss.
- Silent truncation keeps a chat responsive, but misrepresents the evidence the
  model considered.
- Persisted shared transcripts could support collaboration, but would introduce
  a new governed record, retention policy, and identity boundary.

## Open questions

- What byte, turn-count, and output limits preserve useful full-buffer turns?
- When a selection mode arrives, how should its visible scope and hashes be
  represented so it cannot be mistaken for full-document review?
- Is ephemeral transcript export valuable enough to justify a separate,
  explicitly governed artifact flow?

## Relationships

- The [dual-buffer editor](doxbench-dual-buffer-editor.md) supplies the working
  text for every turn.
- [Typed proposal review](doxbench-typed-proposal-review.md) constrains the
  actionable part of a response.
- The [provider boundary](doxbench-provider-boundary.md) determines which
  models may receive the turn.
- The [human/AI loop synthesis](doxbench-synthesis-human-ai-authoring-loop.md)
  explains the feedback cycle created by these seams.
