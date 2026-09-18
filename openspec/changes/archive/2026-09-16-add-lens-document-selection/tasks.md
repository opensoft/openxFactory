# Tasks: add-lens-document-selection

## 1. The dark-theme defect class

- [x] 1.1 `.relrow` states its colour — a `<button>` takes the UA's
      `buttontext`, so the relationship tiles rendered black on the dark
      panel at contrast 1.18.
- [x] 1.2 Repoint all six uses of custom properties the stylesheet never
      defines (`--bg` ×3, `--st-blocked` ×2, `--st-neutral`) at real tokens.
      Two of them were the repository-filter and new-project POPOVERS, which
      fell back to `#fff` behind `--ink` text in dark mode.
- [x] 1.3 Guard both classes by test: every `var(--x)` is defined, and every
      button reset states a colour.
- [x] 1.4 Label the relationship count (`14 docs`, and the note says what it
      counts) — a number that has to be hovered to be understood has not
      been labelled.

## 2. The join

- [x] 2.1 The bullseye publishes `data-doc` on each dot group.
- [x] 2.2 The matrix row and the signature-grid row publish the same key.
- [x] 2.3 One delegated listener per pane lights every view of a document;
      document ids are paths, so escape them before they enter a selector.

## 3. The stated finding

- [x] 3.1 `signatureSummary` in the pure model: distinct signatures, repeated
      groups, largest group, and the groups themselves.
- [x] 3.2 The grid renders as a collapsed `<details>` whose summary carries
      the finding and what it means.

## 4. The staging seed

- [x] 4.1 `doc_health/staging_seed.py` — convergence, collision-free topic
      slug, and a deterministic fragment SCAFFOLD.
- [x] 4.2 `/actions/staging-seed` — loopback, write-nothing, evidence
      recomputed from the serve's own snapshot, unknown documents refused by
      name.
- [x] 4.3 Matrix checkboxes, select-all, the selection bar, and the drafted
      fragment rendered read-only with a copy control.
- [ ] 4.4 Brett drafts and places the first staging seed from a real
      convergence, and the fragment gets its INDEX.md row.

## 5. Verification

- [x] 5.1 Full suites green (2806 passed) and `openspec validate --all
      --strict` green.
- [x] 5.2 Live in dark mode: relationship text `rgb(231,234,239)`, popover
      ground `rgb(28,32,40)`, grid closed at 22px stating "32 docs share 3
      signatures (largest 17)", hover lighting dot + grid row + table row,
      and a real drafted fragment with 9 unwritten sections. Zero page
      errors.

## Ratification-citation respell (2026-08-23)

- `proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by
  `govern-openspec-corpus-membership` slice 5A.1, under OQ-4's 2026-08-23
  ruling — prefix only, the bytes after the colon carried verbatim. The record
  that justifies the line is Brett's three annotations of 2026-08-08, all three
  quoted on the line itself — the unreadable relationship tiles and their
  unlabelled count, "this is taking up too much space. what value does it
  bring?", and "when I hover on one of these documents, the corresponding dot
  should light up. I should have a checkbox on each one to generate the seed
  from checked".
