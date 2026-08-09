---
code_surface: openxFactory (create-document carries an optional authored body; authoring.create_scaffold writes it below the header; the doxBench draft view's body becomes editable and lands with the create; tests)
target_release: none
Status: draft
Ratified by: pending — Brett asked for create-then-edit on 2026-08-09; this proposes the shape that actually works
---

# Proposal: add-authored-body-on-create

## Why

Brett, 2026-08-09: "do the create-then-edit so I can write the body." The
attempt found a wall that is a CONTRACT, not a bug, so it is proposed rather
than worked around.

- `create-document` writes the HEADER CONTRACT. `authoring.create_scaffold`
  takes title, summary, topics, area, kind, status — and no body.
- `edit-document` writes bodies, but it is TILE-SCOPED: `_edit_body` requires
  `scope_kind` and `scope_id`, and the verb resolves a LIVE branch session for
  that tile, refusing outright where none resolves. It has no session-less
  path, and says so in its own source.
- A LENS DRAFT HAS NO TILE. It is a set of documents selected on a radar, and
  the staging topic it would become does not exist in the snapshot yet — so
  there is no scope to name. Naming the topic it is about to create is
  circular.

Measured on a fixture plane: the create returns 200 and lands the header; the
edit returns 400 for the missing scope. So the sequence Brett asked for cannot
be assembled from the verbs as they stand, and the draft view's body is
read-only until one of them changes.

## What changes

`create-document` gains an OPTIONAL `body`: the prose written below the
header, in the same write, the same commit, and the same governed dispatch.

This is the shape that fits what a lens draft IS. A drafted fragment arrives
whole — a computed header and a body whose sections are marked `TO WRITE` —
and it becomes one document. Splitting that into create-then-edit buys a
half-written state (a header with no body, if the second verb refuses) and an
extra governed action, in exchange for nothing the human asked for.

What does NOT change: the header stays the create's own, generated from its
fields, so a body cannot smuggle in a different `Status:` or `Topics:` line
than the one the create recorded. The create stays create-only — an existing
target still refuses — and stays human-only.

## Alternative considered

Letting `edit-document` accept a scope-free FIRST save against a document the
same session just created. Rejected as the primary: it widens the verb whose
whole safety story is "a session lives in one tree and a tile owns it", and it
would still leave the two-verb half-state. Worth revisiting if bodies are ever
needed for documents this dashboard did not create.

## Impact

- Affected specs: `ideation-dashboard` (MODIFIED: human document authoring)
- Affected code: `authoring.create_scaffold`, `gate_routes._create_body` +
  `execute_create_document`, `views/staging-workbench.js` (the draft view's
  body becomes an editable buffer that lands with the create), CLI parity
- The body is TEXT the human wrote. It is never generated, and the `TO WRITE`
  markers the seed leaves are the human's prompts, not the machine's claims.
