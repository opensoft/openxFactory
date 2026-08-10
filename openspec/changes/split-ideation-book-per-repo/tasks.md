# Tasks: split-ideation-book-per-repo

## 1. Contract and ratification (BRETT RATIFY GATE)

- [ ] 1.1 `OPENSPEC_TELEMETRY=0 openspec validate split-ideation-book-per-repo
      --strict` and `--all --strict` green; change listed in the README
      OpenSpec Records block.
- [x] 1.2 Brett ratification of the decisions the delta fixes: per-repo
      Ideation books (vs. a coarser two-book split), legacy-alias retirement
      (vs. repointing `xf-ideation`), and headroom-warn + further-delta as
      the growth policy (the declined alternative — pre-authorizing
      mechanical splits in this delta — is recorded in
      `review/decision-review-2026-08-10.md`). — RATIFIED 2026-08-10 by
      Brett, in-session, verbatim "ratified"; the declined judgment stands
      as authored. Gate open.

## 2. Sync implementation (code_surface: openxFactory)

- [x] 2.1 `scripts/sync-notebooklm-books.py`: derive ideation book identity
      per governed repository (`xFactory Ideation — <RepoName>` /
      `xf-ideation-<repo-slug>`); membership = status-derived set only
      (charter/grounding are seeds, never membership); resolve books by
      TITLE with idempotent, non-fatal alias re-registration; re-cut
      `--book` for the dynamic book family; key the manifest by the new
      book identities, drop the stale `ideation` key, and FLUSH the
      manifest after each book (not once at the end) so an interrupted run
      resumes without delete/re-add churn.
- [x] 2.2 Lazy creation, apply-mode only, via the centralized create
      adapter pattern (`scripts/ideation_dashboard/workbench.py`
      `_create_titled` — no `--json` on create, title-listing fallback):
      create, tag `xfactory,lifecycle`, apply chat framing (`CHAT_PROMPT`
      via `nlm chat configure`), seed charter + grounding, and write the
      book's `external_source_workspace` record
      (`examples/lifecycle-notebook-workspaces.yaml`) with the provider
      notebook id. Dry-run reports the pending creation and mutates
      nothing.
- [x] 2.3 Capacity guard per the ADDED requirement: projected occupancy =
      desired managed + charter + observed unmanaged; cap as a named
      constant recorded in the doc; headroom warning at ≤ 30 with the
      owed-delta naming for any book without a defined successor split;
      deterministic in-cap prefix + exact-excess report + nonzero on
      overflow; unresolvable-book and refused-create contained per book.
- [x] 2.4 Deterministic checks in the script's existing test pattern
      (network-free): repo→book routing, seeds-don't-create-books, dry-run
      vs apply creation, occupancy math including the charter and an
      unmanaged source, headroom/overflow thresholds, stable excess
      selection, per-book failure containment. Update the suites that bind
      to the retired key/alias: `tests/notebooklm/test_sync_notebooklm_books.py`
      (exact notebook-listing assertions) and
      `tests/ideation-dashboard/test_authoring_agent.py` (drives
      `sync_book` with `xf-ideation` for the ideation-dashboard
      "Notebook set-removal semantics" requirement) — and if the
      `ideation-dashboard` spec text names the legacy book or alias, author
      the companion delta rather than silently retargeting its test.

## 3. Migration and retirement

- [ ] 3.1 Sequenced migration, one book per `--book` invocation, fresh nlm
      auth per session (~20-minute session lifetime vs. ~2s per source
      operation): seed the four small books first, openxFactory last;
      expected op budget ≈ 325 member adds + charters/grounding/framing —
      record the actual op counts and wall clock as evidence. The legacy
      book is NOT a sync target in any of these runs (it left the book set
      at 2.1).
- [ ] 3.2 Parity per repo by TITLE-SET equality (not count): each book's
      managed titles equal the repo's scanned ideation membership, and the
      union across books reconciles against the corpus scan total —
      reconciliation is against the corpus, never against the legacy book
      (which was at cap and had already dropped an unknown set).
- [ ] 3.3 Retire the legacy "xFactory — Ideation" book and the
      `xf-ideation` alias as a recorded manual act: archive-rename or
      delete the notebook, remove the alias, retire its
      `external_source_workspace` record. Never repoint.
- [x] 3.4 `docs/lifecycle-notebook-projection.md`: book table and alias
      inventory (title-resolution rule, alias-as-convenience), tags, the
      cap constant and headroom policy, grounding fan-out note (an edit to
      a grounding doc now re-projects into every book), migration record,
      §11 Known Limitations updated; doc carries `Ratified by:` this
      change on ratification.

## 4. Evidence and exit

- [ ] 4.1 One full post-migration sync from the workspace root: green,
      zero-change on immediate re-run (idempotence), guard silent above
      headroom; output recorded as realization evidence, including
      per-book occupancy (openxFactory expected ≈ 216/300 at migration).
- [ ] 4.2 Cross-repo follow-up recorded (non-blocking): aggregation-repo
      CLAUDE.md NotebookLM note updated to the alias family and
      title-resolution rule.
- [ ] 4.3 Archive on realization evidence per `release-realization`.
