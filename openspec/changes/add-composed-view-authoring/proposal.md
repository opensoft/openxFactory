---
code_surface: openxFactory (the serve declares its writable repository on /capabilities; the lens's drafted-seed hand-off and the workbench's openDraft read the unstripped capability; tests)
target_release: none
Status: ratified
Ratified by: Brett, 2026-08-08 — "yes, we need to draft from a project view", after the hand-off was found unavailable on every project-scoped view
---

# Proposal: add-composed-view-authoring

## Why

`Composed views are read-only with a repository jump` states its own reason:

> a gate verb binds to one served checkout, and a composed view has none

That is true of a verb bound to a TILE. Acting on a document from AdxFactory
requires a writable AdxFactory checkout, and a serve rooted at openxFactory
has none — which is exactly why the requirement exists and why it stays.

It is NOT true of creating a NEW document. A new staging fragment binds to no
tile: it lands in the serve's OWN checkout, which exists, is writable, and is
the same tree the create would have used on an unscoped view. The blanket
rule over-generalises from "no per-tile checkout" to "no checkout", and the
cost of that is concrete — every project-scoped view, including a
single-member one, refused the lens's drafted-seed hand-off. Since a project
view is where the cross-repository convergences are actually visible, the one
place the hand-off is most useful is the one place it was unavailable.

Brett, 2026-08-08: "yes, we need to draft from a project view."

## What changes

**The serve DECLARES its writable repository.** `/capabilities` gains
`repository`, reported from `_session_repository()` — the same authority a
create is refused against — so the capability and the refusal cannot
disagree. The browser previously had to infer it, and under a composed view
it inferred the PROJECT id, which is not a repository at all and is refused
by `refuse_foreign_repository`. A serve knows what it serves; the client
stops guessing.

**One affordance reads the unstripped capability.** The lens's drafted-seed
hand-off and the workbench's `openDraft` ask whether the SERVE can create,
not whether the VIEW is a projection. Every other surface keeps the stripped
capabilities exactly as today — the tile-bound verbs genuinely have no
checkout to bind to on a composed view, and none of them changes.

**The created document names the served repository**, never the project.

## Impact

- Affected specs: `ideation-dashboard` (MODIFIED: `Composed views are
  read-only with a repository jump`)
- Affected code: `serve.py` capabilities route, `app.js`, `views/lens.js`,
  `views/staging-workbench.js`
- The cross-repository write hazard this narrows around is UNCHANGED:
  `refuse_foreign_repository` still refuses any create naming a repository
  this serve does not write to, and it is now comparing against the value the
  client was handed rather than one it guessed.
