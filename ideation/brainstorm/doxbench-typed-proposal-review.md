# doxBench Typed Proposal Review — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can separate conversational AI output from typed buffer-replacement proposals and use content hashes to prevent late responses from overwriting newer human work.
Topics: doxbench, typed-proposal-review, ideation-dashboard, human-in-the-loop, stale-output
Repository context: openxFactory doxBench AI-response and human-review boundary
Captured: 2026-07-28

## Possible feats

- **Independent proposal cards** — Review, apply, or reject outline and document proposals separately even when one turn produces both.
- **Stale proposal comparison** — Show current and proposed text side by side after a hash mismatch without offering an authority-bypassing force apply.

## Focus

This document isolates the transition from model response to local edit. Normal
assistant prose can inform a human but is not replacement content. Only a
schema-valid proposal naming one target buffer can become an Apply candidate.

## Proposed model

A typed proposal carries one target (`outline` or `document`), complete proposed
content, the target buffer hash supplied to the turn, a summary, and response
identity. Immediately before Apply, the browser recomputes the current target
hash.

When hashes match, Apply replaces only that browser buffer, marks it dirty, and
remains reversible through Discard or further editing. When hashes differ,
Apply refuses as stale and offers honest review choices: keep current text,
inspect current versus proposed text, or ask for a new turn. Saving remains a
separate human action.

## Interfaces and boundaries

Proposal review consumes schema-valid response objects and current buffer
hashes. It emits a local buffer transition only after a human gesture.

It does not infer replacement content from Markdown prose, silently merge,
force-apply stale output, write a file, create a branch, or attribute final
write authority to the model provider.

## Alternatives and tensions

- Inferring edits from assistant Markdown feels flexible, but makes the
  boundary between advice and action ambiguous.
- Patch proposals may be smaller than full replacements, but complicate
  deterministic review, stale detection, and cross-editor portability.
- Automatic three-way merge could retain more work, but hides conflict choices
  that the current human-review posture deliberately exposes.

## Open questions

- Should a future proposal format permit structured patches in addition to
  complete content, and what proof would preserve review clarity?
- Which comparison presentation remains accessible for very large documents?
- Should a human be able to annotate why a proposal was rejected without
  turning ephemeral chat into a governance record?

## Relationships

- The [grounded chat](doxbench-grounded-chat.md) provides the response and the
  base hashes it attests to.
- The [dual-buffer editor](doxbench-dual-buffer-editor.md) receives an accepted
  local replacement.
- [Governed persistence](doxbench-governed-persistence.md) remains the only
  route from reviewed buffer state to corpus change.
- The [human/AI loop synthesis](doxbench-synthesis-human-ai-authoring-loop.md)
  positions Apply as review, not persistence.
