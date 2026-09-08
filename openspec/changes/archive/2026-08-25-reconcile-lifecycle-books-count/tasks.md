# Tasks: Reconcile The Lifecycle-Books Count

## 1. Establish the defect and its lawful fix

- [x] 1.1 Confirm no change already reconciles this count before authoring:
      the open and closed pull-request list and a corpus-wide grep for the
      phrase and its variants ("three lifecycle books", "the three books",
      case variants), re-run immediately before pushing. Nothing found in
      either run
- [x] 1.2 Locate every instance in the two governed surfaces this change may
      touch. Promoted spec: `Corpus scan scope` (one) and
      `Branch-session notebooks` (one). Workflow doc
      `docs/lifecycle-notebook-projection.md`: §1 main-only rule (line 67),
      §7 hybrid exclusion (198), §9 session-notebook exclusion (266), §9
      shared-quota note (285), §10 workspace records (344). Five, matching
      the residual PR #317 recorded
- [x] 1.3 Confirm the two other appearances of "three" in that doc are NOT
      this defect and stay untouched: the three GROUNDING DOCS (§3, §11).
      `3+N books` in §11 is already post-split and correct
- [x] 1.4 Derive the replacement wording from the ratified source rather
      than inventing it: `2026-08-10-split-ideation-book-per-repo`'s
      `Derived notebook membership` delta — "one Ideation book per governed
      repository", "the shared Working Drafts book", "the shared Canon book"

## 2. Restate the two requirements, count phrase excepted

- [x] 2.1 Build the delta by EXTRACTING both requirement blocks from canon
      and substituting only the count phrase, so no other byte can drift.
      Verified against the hashes `apply-branch-sessions-deltas` recorded for
      the same blocks when it promoted them:

      | requirement | canon block sha256 | this delta's block sha256 |
      | --- | --- | --- |
      | Corpus scan scope | `99fa2a84…d66dc8c` | `94565264…1253c50` |
      | Branch-session notebooks | `107ede78…8d42057e` | `f5be6d40…09cbd85a` |

      The canon column matches the promoting change's recorded hashes
      exactly, which is what proves the extraction took the ratified text and
      not a paraphrase of it
- [x] 2.2 Prove the delta differs from canon in the count phrase and nowhere
      else, by word-diff: two edits total — `three` deleted plus the topology
      clause inserted in `Corpus scan scope`, `three` deleted in
      `Branch-session notebooks`. Every scenario byte-identical; all four and
      all five restated so the promotion replaces the blocks whole

## 3. Validation

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate reconcile-lifecycle-books-count --strict`
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — 76 items
      with the change active, 75 after archive, against a 75 baseline
- [x] 3.3 List this change in the README's OpenSpec Records block

## 4. The standard doc

- [x] 4.1 Correct the five instances consistently: each becomes "the
      lifecycle books". None gains an enumeration — §1's book table states
      the topology two paragraphs above the first of them
- [x] 4.2 Record the amending act on the doc's header with an `Amended by:`
      line, the convention `split-ideation-book-per-repo` set on this same
      document when it amended it

## 5. Promotion and archive

- [x] 5.1 Promote the delta into
      `openspec/specs/lifecycle-notebook-projection/spec.md` through
      `openspec archive` and archive this packet (promotion-only;
      `code_surface: none`, so it archives on landing)
- [x] 5.2 Prove the promotion by sha256 rather than asserting it: each
      requirement block extracted from canon after promotion hashes identical
      to this packet's delta block, and the post-promotion word-diff against
      pre-promotion canon shows the count change and nothing else
- [x] 5.3 Re-run the promotion-fidelity family through the real code path.
      This change is now the latest archived writer of both requirements, so
      the family measures it: openxFactory reads ZERO findings, and no
      finding appears anywhere else
- [x] 5.4 Re-run `python3 -m pytest tests/doc-health` at baseline, re-validate
      `--all --strict`, and confirm the single-repo doc-health report moves on
      no line

## 6. Owed elsewhere, not here

- [x] 6.1 The phrase survives in code comments and one operator message —
      `scripts/sync-notebooklm-books.py` (three),
      `scripts/ideation_dashboard/branch_session.py` (two, one of them a
      message a human reads), and their tests (two). That is code surface;
      this change declares `code_surface: none` and does not acquire one.
      Owed as a separate change, which may correct them and their tests
      together. — Discharged 2026-08-24 by the follow-on fix
      `fix/lifecycle-books-count-code-strings`, on Brett's ruling "fix the
      code-surface stragglers in §6.1": all eight instances aligned to this
      change's ratified vocabulary, each verified prose (docstring, comment,
      or operator notice) and none a book title or alias, since books resolve
      by title. Realization alignment to already-ratified vocabulary carries
      no packet, the shape PR #161 set when it swept stale `xf-ideation`
      references after `split-ideation-book-per-repo`. Box ticked here with
      this note rather than silently (document-lifecycle: contested findings
      resolve by citation), as that same sweep ticked §4.3 of the archived
      split packet
