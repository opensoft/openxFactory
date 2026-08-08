---
code_surface: openxFactory (lens matrix selection + cross-view document highlight; collapsed signature grid with a stated finding; doc_health.staging_seed drafter and its serve route; the theme-token guards; tests)
target_release: none
Status: ratified
Ratified by: Brett's three annotations of 2026-08-08 — the unreadable relationship tiles and their unlabelled count, "this is taking up too much space. what value does it bring?", and "when I hover on one of these documents, the corresponding dot should light up. I should have a checkbox on each one to generate the seed from checked"
---

# Proposal: add-lens-document-selection

## Why

Three findings from one session on the keyword lens, and they share a root:
the lens can now SHOW a convergence but cannot yet be USED to act on one.

**A document has three views and no join.** The radar draws it as a dot, the
matrix states it as a row, the signature grid draws it as a strip. All three
number it identically, and the reader still has to hold "#17" in their head
while their eye travels between them. That is arithmetic the machine should
be doing.

**A finding was being drawn instead of stated.** The signature grid occupied
220px of the most valuable space on the screen to show something that is
true or false in one sentence — whether any documents carry exactly the same
checked terms. On the live corpus that sentence is "32 documents share 3
signatures (largest 17)", which is a finding worth reading; the picture is
the evidence for it, wanted only sometimes.

**A convergence had no exit.** The register seed added by
`add-shared-identity-seeds` answers the DTN question — do two factories
carry the same artifact — which is not the question a reader of the keyword
radar has. Theirs is "these documents keep meeting; what is the topic?", and
the queue that question belongs in is `ideation/staging/`. Until now the
only way out of the lens was to write the fragment by hand from a screen of
numbers.

Beneath all three, two dark-theme defects of one class: a `<button>` reset
that never stated its colour (black on the dark panel at contrast 1.18) and
six uses of custom properties this stylesheet never defines, whose silent
fallbacks painted a white popover behind light text. Both are invisible in
the light theme, which is why they need a guard rather than an eye.

## What changes

- The lens matrix gains a per-document selection: a checkbox on every row, a
  select-all over the listed rows, and a bar stating how many are chosen.
- Every view of a document publishes the same key, so pointing at any one of
  them lights the others.
- The signature grid states its finding in its summary and collapses; the
  drawing opens on request.
- A selection drafts a STAGING-QUEUE fragment — the queue's own format, as
  text, with the evidence computed and the argument left explicitly to the
  human.
- The theme owns every colour: no view writes a lightness, and every custom
  property the stylesheet reads is one it defines.

## Impact

- Affected specs: `ideation-dashboard`
- Affected code: `web/views/lens.js`, `web/views/lens-model.js`,
  `web/views/bullseye.js`, `web/styles.css`,
  `scripts/doc_health/staging_seed.py`, `scripts/ideation_dashboard/serve.py`
- No schema, contract, or register change. The new route writes nothing.
